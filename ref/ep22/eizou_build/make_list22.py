# -*- coding: utf-8 -*-
"""22本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-14・映像方針チャット）。21本目の make_list21.py を写して22本目の型に替えた。

  python -I ref/ep22/eizou_build/make_list22.py

入力：台本 第2版 ref/ep22/daihon_v2.md §4 の見出し行（画の欄。語りは字数と秒を数え、深さの数を探すだけ）
      eizou_build/assign22.tsv（当て方＝実写は全部ここ・画の欄を替えたカットの新しい画）・sources22.tsv（出どころ）・shots22.tsv（映像のショットの境目）
出力：ref/ep22/eizou_list22.md（生成物＝手で直さない）・eizou_build/list22.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 実写のカットに素材の記号が無い／記号が sources22.tsv に無い／写真の一部の印（N18:左 など）が2つのカットで同じ
  E 映像の区間がショット1本に収まらない／倍率（区間の秒÷カットの秒）0.6 未満／同じ映像の区間が重なる
  E 第三者・BY-SA・共同の素材が「額装」でない／第三者・BY-SA の映像が「等速」と書いていない
  E 第三者（ROV）の映像を、語りが壊れた深さ（3,3xx メートル）を言うカットに当てる（焼き込みの 3,775m＝海底の深さと食い違う）
  E 冒頭（c101〜c109）に実写でない画／写真と実写（この事故の物）が 20% 未満／文字だけの画面が3つ続く
  ⚠️ 第三者・BY-SA の映像の倍率が 1.0 から 0.05 以上ずれる（⑤a の秒で区間を取り直す）／静止写真の動きが「寄る」に偏る（50%超）／章の写真と実写が 20% 未満
秒＝句読点なし÷365字/分（m22.py と同じ数え方）＝⑤a の実測で取り直す。audio/narration.json が22本目の並びなら実測を使う。
"""
import csv
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
DAIHON = os.path.join(EP, 'daihon_v2.md')
OUT_MD = os.path.join(EP, 'eizou_list22.md')
OUT_TSV = os.path.join(HERE, 'list22.tsv')
NARR = os.path.join(REPO, 'audio', 'narration.json')
PUNCT = '、。？！「」（）・'
CUT = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*')
OPENING = ['c10%d' % i for i in range(1, 10)]
MIN_SPEED = 0.6
PHOTO_LO = 0.20
LEAD, TAIL, CARD_SEC = 0.35, 0.50, 2.0
DEPTH_SAY = re.compile(r'3,3\d\d|3,3\d{2}|約3,350')   # 壊れた深さ（3,341〜3,363m）
FRAME_ONLY = ('第三者', 'BY-SA', '共同')


def nopunct(s):
    return ''.join(ch for ch in s if ch not in PUNCT and not ch.isspace())


def read_tsv(path):
    with open(path, encoding='utf-8') as f:
        lines = [ln for ln in f if not ln.startswith('#') and ln.strip()]
    return list(csv.DictReader(lines, delimiter='\t'))


def read_cuts():
    t = open(DAIHON, encoding='utf-8').read()
    body = t[t.index('## 4. 台本'):t.index('## 5. ')]
    rows, chap, cur = [], '', None
    for ln in body.split('\n'):
        if ln.startswith('### '):
            chap = ln[4:].strip()
            continue
        m = CUT.match(ln)
        if m:
            parts = ln.split(' ／ ')
            cur = dict(cid=m.group(1), chap=chap, ga=parts[1].strip() if len(parts) > 1 else '', n=0, first='', text='')
            rows.append(cur)
            continue
        if cur and ln.startswith('>'):
            s = ln[1:].strip()
            if s.startswith('Q:'):
                s = s[2:].strip()
            if not cur['first']:
                cur['first'] = s
            cur['text'] += s
            cur['n'] += len(nopunct(s))
    sec = 0.0
    for r in rows:
        r['start'] = sec
        r['dur'] = r['cont'] = r['n'] / 365 * 60
        sec += r['dur']
    note = '÷365 の見込み'
    if os.path.exists(NARR):
        dur = json.load(open(NARR, encoding='utf-8')).get('durations', {})
        if [r['cid'] for r in rows] == [c for c in dur if CUT.match('**%s**' % c) and c != 'ed01']:
            sec, prev, seen = 0.0, None, set()
            for r in rows:
                key = r['cid'][:2]
                card = CARD_SEC if (prev is not None and key != prev and key not in seen) else 0.0
                seen.add(key)
                prev = key
                r['start'] = sec
                r['cont'] = dur[r['cid']] + LEAD + TAIL
                r['dur'] = r['cont'] + card
                sec += r['dur']
            note = 'audio/narration.json の実測'
    return rows, note


def base_kind(ga):
    if ga.startswith('実写'):
        return '実写'
    if ga.startswith('panel'):
        return '文字だけ'
    for pre, k in (('図 再現', '再現'), ('図 線', '線'), ('図 模式', '模式'), ('図 地図', '地図'), ('図 棒', '棒'),
                   ('図 帯', '帯'), ('図 NTSB', 'NTSB図'), ('図 吹き出し', '吹き出し'), ('図 問い', '問い')):
        if ga.startswith(pre):
            return k
    return '?'


def motion_class(mo):
    if not mo or mo == '—':
        return ''
    if mo.startswith('映像'):
        return '映像'
    pre = '額ごと' if mo.startswith('額ごと') else ''
    for key, name in (('2点', '2点'), ('引', '引く'), ('左へ', '左へ'), ('右へ', '右へ'), ('上へ', '上へ'), ('下へ', '下へ'), ('寄', '寄る')):
        if key in mo:
            return pre + name
    return mo


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def main():
    cuts, secnote = read_cuts()
    E, W = [], []
    arows = read_tsv(os.path.join(HERE, 'assign22.tsv'))
    dup = [k for k, v in Counter(r['cid'] for r in arows).items() if v > 1]
    if dup:
        E.append('assign22.tsv に同じカットの行が2つ以上：%s' % '・'.join(sorted(dup)))
    assign = {r['cid']: r for r in arows}
    known = {c['cid'] for c in cuts}
    for k in assign:
        if k not in known:
            E.append('assign22.tsv のカット %s が台本に無い' % k)
    sources = {r['code']: r for r in read_tsv(os.path.join(HERE, 'sources22.tsv'))}
    shots = {}
    shp = os.path.join(HERE, 'shots22.tsv')
    if os.path.exists(shp):
        for r in read_tsv(shp):
            shots.setdefault(r['film'], []).append((float(r['start']), float(r['end']), r['shot']))

    for c in cuts:
        a = assign.get(c['cid'], {})
        g = lambda k: (a.get(k) or '').strip().replace('—', '')
        c['kind0'] = base_kind(c['ga'])
        c['kind'] = g('kind') or c['kind0']
        c['main'], c['frame'], c['motion'], c['view'], c['note'] = g('main'), g('frame'), g('motion'), g('view'), (a.get('note') or '').strip()
        c['ga_new'] = g('ga_new')
        c['sub'] = g('sub')
        if not c['sub'] and c['kind'] == '実写':
            m = re.search(r'副題「(.+?)」', c['ga'])
            c['sub'] = m.group(1) if m else ''
        c['changed'] = '🔧' in c['note']

    still_use, film_use = {}, {}
    for c in cuts:
        c['rights'] = c['credit'] = c['speed'] = c['window'] = c['shot'] = c['code'] = c['cls'] = c['part'] = ''
        c['src_sec'] = 0.0
        if c['kind'] != '実写':
            if c['main']:   # 衛星写真の地図（G01〜）など＝素材の記号だけ写す（門番は実写だけ）
                c['code'] = c['main']
            continue
        if not c['main']:
            E.append('%s 実写なのに素材の記号が無い（%s）' % (c['cid'], c['ga'][:40]))
            continue
        m = re.match(r'([A-Za-z0-9]+)@([\d.]+)-([\d.]+)$', c['main'])
        code, part = (m.group(1), '') if m else (c['main'].split(':')[0], c['main'].split(':')[1] if ':' in c['main'] else '')
        s = sources.get(code)
        if not s:
            E.append('%s 記号 %s が sources22.tsv に無い' % (c['cid'], code))
            continue
        c['code'], c['part'] = code, part
        c['rights'], c['credit'], c['cls'] = s['rights'], s['credit'], s['class']
        third = s['rights'].startswith(FRAME_ONLY)
        if third and not c['frame'].startswith('額装'):
            E.append('%s %s の素材（%s）が額装でない（%s）' % (c['cid'], s['rights'].split('（')[0], code, c['frame']))
        if s['class'] == 'film':
            if not m:
                E.append('%s 映像なのに区間が無い（%s）' % (c['cid'], c['main']))
                continue
            x, y = float(m.group(2)), float(m.group(3))
            c['src_sec'] = y - x
            c['window'] = '%.1f〜%.1f' % (x, y)
            if shots.get(code):
                hit = [sh for sh in shots[code] if sh[0] - 0.05 <= x and y <= sh[1] + 0.05]
                if not hit:
                    E.append('%s %s の区間 %.1f〜%.1f がショット1本に収まらない' % (c['cid'], code, x, y))
                else:
                    c['shot'] = hit[0][2]
            else:
                W.append('%s %s のショットの表が無い（shots22.tsv）＝区間の門番が働かない' % (c['cid'], code))
            sp = c['src_sec'] / c['cont'] if c['cont'] else 0
            c['speed'] = '%.2f' % sp
            if sp < MIN_SPEED:
                E.append('%s 倍率 %.2f（区間 %.1f秒÷カット %.1f秒）＜ %.1f＝止め絵になる' % (c['cid'], sp, c['src_sec'], c['cont'], MIN_SPEED))
            if third:
                if '等速' not in c['motion']:
                    E.append('%s 第三者・BY-SA の映像なのに「等速」と書いていない（%s）' % (c['cid'], c['motion']))
                if abs(sp - 1.0) >= 0.05:
                    W.append('%s %s の映像の倍率 %.2f＝等速で使う（⑤a の秒で区間の長さを合わせる）' % (c['cid'], code, sp))
                if s['rights'].startswith('第三者') and DEPTH_SAY.search(c['text']):
                    E.append('%s 語りが壊れた深さ（3,3xx m）を言うカットに ROV（焼き込み 3,775m＝海底）を当てている' % c['cid'])
            film_use.setdefault(code, []).append((x, y, c['cid']))
        else:
            if m:
                E.append('%s 写真に区間が付いている（%s）' % (c['cid'], c['main']))
            still_use.setdefault((code, part), []).append(c['cid'])

    for (code, part), cs in sorted(still_use.items()):
        if len(cs) > 1:
            E.append('写真 %s%s を2回使う：%s（1点1カット）' % (code, (':' + part) if part else '', '・'.join(cs)))
    for code, ivs in sorted(film_use.items()):
        ivs.sort()
        for i in range(1, len(ivs)):
            if ivs[i][0] < ivs[i - 1][1] - 0.01:
                E.append('映像 %s の区間が重なる：%s と %s' % (code, ivs[i - 1][2], ivs[i][2]))
    for c in cuts:
        if c['cid'] in OPENING and c['kind'] != '実写':
            E.append('%s 冒頭に実写でない画（%s）' % (c['cid'], c['kind']))

    last = None
    for c in cuts:
        c['signal'] = ''
        if c['view']:
            if last and last[1] != c['view']:
                c['signal'] = '🔁 %s→%s（前の図 %s）＝左上に見る向きの札・替わる瞬間に「%s見ると」' % (last[1], c['view'], last[0], c['view'])
            last = (c['cid'], c['view'])

    n = len(cuts)
    tot = sum(c['dur'] for c in cuts)
    photo = [c for c in cuts if c['kind'] == '実写']
    film = [c for c in photo if c.get('cls') == 'film']
    still = [c for c in photo if c.get('cls') in ('photo', 'fig')]
    text = [c for c in cuts if c['kind'] == '文字だけ']
    docs = [c for c in cuts if c['kind'] in ('再現', '吹き出し')]
    docs0 = [c for c in cuts if c['kind0'] == '再現']
    ratio = len(photo) / n
    if ratio < PHOTO_LO:
        E.append('写真と実写 %.1f%% ＜ 20%%' % (ratio * 100))
    run, mx = 0, 0
    for c in cuts:
        run = run + 1 if c['kind'] == '文字だけ' else 0
        mx = max(mx, run)
    if mx >= 3:
        E.append('文字だけの画面が %d つ続く' % mx)
    mc = Counter(motion_class(c['motion']) for c in still)
    if still and sum(v for k, v in mc.items() if k.endswith('寄る')) / len(still) > 0.5:
        W.append('静止写真の動きが「寄る」に偏る（%d/%d）' % (sum(v for k, v in mc.items() if k.endswith('寄る')), len(still)))
    chaps = []
    for c in cuts:
        if not chaps or chaps[-1] != c['chap']:
            chaps.append(c['chap'])
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = sum(1 for c in cs if c['kind'] == '実写')
        if k / len(cs) < PHOTO_LO:
            W.append('章「%s」の写真と実写 %d/%d（%.0f%%）＜ 20%%' % (ch.split('（')[0], k, len(cs), k / len(cs) * 100))
    framed = [c for c in photo if c['frame'].startswith('額装') or c['frame'].startswith('紙面')]
    fulls = [c for c in photo if c['frame'].startswith('全面')]
    kinds = Counter(c['kind'] for c in cuts)
    changed = [c for c in cuts if c['changed']]
    heads = {}
    for c in cuts:
        heads.setdefault(c['chap'], c)
    card0 = [h['cid'] for ch, h in heads.items() if not ch.startswith('つかみ') and h['kind'] == '実写' and h['rights'].startswith(FRAME_ONLY)]

    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['cid', 'chap', 'start', 'dur', 'kind', 'code', 'part', 'window', 'speed', 'frame', 'sub', 'motion', 'view', 'signal', 'rights', 'credit', 'note', 'ga', 'ga_new'])
        for c in cuts:
            w.writerow([c['cid'], c['chap'], '%.1f' % c['start'], '%.1f' % c['dur'], c['kind'], c['code'], c['part'], c['window'], c['speed'], c['frame'],
                        c['sub'], c['motion'], c['view'], c['signal'], c['rights'], c['credit'], c['note'], c['ga'], c['ga_new']])

    L = ['---', 'title: 22本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-10-14', 'tags: [project/jiko-kensho, ep22]', '---', '',
         '# 22本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % n, '',
         '> **生成物＝手で直さない**。作り方＝`python -I ref/ep22/eizou_build/make_list22.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄・当て方 `eizou_build/assign22.tsv`・出どころ `eizou_build/sources22.tsv`・映像のショット `eizou_build/shots22.tsv`）。直すのは入力の TSV。',
         '> 秒＝%s（⑤a の音で取り直す）。🔧＝台本の画の欄から替えたカット（assign22.tsv の note）。色味は原本（10-07）・写真は画面いっぱい（10-11）＝例外は額装（第三者・BY-SA・共同・報告書の図・紙面の引用）。第三者（ROV）と BY-SA の映像は等速・無加工。見た画像の記録＝`eizou_build/seen22.tsv`。決めと確かめの正本＝Vault `Projects/事故検証-22本目-映像方針-20261014.md`。' % secnote, '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真・実写（この事故の物） | **%d カット＝%.1f%%**（秒 %.0f＝%.1f%%）＝映像 %d・写真 %d | 20%%以上 %s |' % (
             len(photo), ratio * 100, sum(c['dur'] for c in photo), sum(c['dur'] for c in photo) / tot * 100, len(film), len(still), '✅' if ratio >= PHOTO_LO else '🔴'),
         '| 全面／額装・紙面の引用 | 全面 %d・額装と紙面 %d（%s） | 例外は了承② |' % (len(fulls), len(framed), '・'.join(sorted(Counter(c['frame'] for c in framed)))),
         '| 書類の再現図（再現・吹き出し） | **%d**（第2版の画の欄では %d）＝人の言葉・一節・要点の札・交信の吹き出し | §0-3「約35」 |' % (len(docs), len(docs0)),
         '| 文字だけ | %d カット（%s）・続く最長 %d | できる限り0に近く |' % (len(text), '・'.join(c['cid'] for c in text), mx),
         '| 🔧 台本の画の欄から替えたカット | %d（%s） | 台本は直さない＝⑤b はこの一覧に従う |' % (len(changed), '・'.join(c['cid'] for c in changed)),
         '| 種類 | %s | — |' % '・'.join('%s %d' % (k, v) for k, v in kinds.most_common()),
         '| 静止写真の動き | %s | 寄るだけにしない（10-07） |' % '・'.join('%s %d' % (k, v) for k, v in mc.most_common()),
         '| 扉の地を方眼だけにする章（頭のカットが額装専用） | %s | card_mix=0（⑤b） |' % ('・'.join(card0) or '—'),
         '| 合計 | %d カット・%s | — |' % (n, fmt_t(tot)), '']
    L += ['### 章ごと', '', '| 章 | カット | 秒 | 実写 | うち映像 | 再現・吹き出し | 模式・線・帯・棒・地図・問い | 文字だけ |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = Counter(c['kind'] for c in cs)
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d |' % (
            ch, len(cs), sum(c['dur'] for c in cs), k['実写'], sum(1 for c in cs if c.get('cls') == 'film'), k['再現'] + k['吹き出し'],
            sum(k[x] for x in ('模式', '線', '帯', '棒', '地図', '問い', 'NTSB図')), k['文字だけ']))
    L += ['', '## §1 冒頭（c101〜c109）＝実写だけ', '', '| カット | 秒 | 素材（区間・倍率） | 見せ方 | 副題 | 語りの頭 |', '|---|---|---|---|---|---|']
    for c in cuts:
        if c['cid'] in OPENING:
            mat = c['code'] + ('@%s（%s倍）' % (c['window'], c['speed']) if c['window'] else '')
            L.append('| %s | %.1f〜%.1f（%.1f） | %s | %s・%s | %s | %s |' % (
                c['cid'], c['start'], c['start'] + c['dur'], c['dur'], mat, c['frame'], c['motion'], c['sub'], c['first'][:24]))
    L += ['', '- 引き＝c105 の終わり %.1f秒（46秒より前）・最初の見出しの手前 c109 の終わり %.1f秒' % (
        next(c['start'] + c['dur'] for c in cuts if c['cid'] == 'c105'), next(c['start'] + c['dur'] for c in cuts if c['cid'] == 'c109')),
        '- 米沿岸警備隊と米空軍州兵の映像の区間は全部1秒1コマで見た（c102・c106・c109・c103・c107）。ROV は5秒おきの見本帳＋26秒の前後を1秒1コマ。遺体・遺品・私人の近い顔なし', '']
    L += ['## §2 映像の区間（字の無い区間＝焼き込みの有無）', '', '| カット | 映像 | 区間（元の秒） | ショット | 倍率 | 焼き込み | 副題 |', '|---|---|---|---|---|---|---|']
    for c in cuts:
        if c.get('cls') == 'film':
            burn = '左上の深さ・左下の日付と時刻・下の HDG／Alt（額装で残す）' if c['code'] in ('R04', 'R07') else ('書類の表紙の字（中身）' if c['cid'] == 'c107' else 'なし')
            L.append('| %s | %s | %s | %s | %s | %s | %s |' % (c['cid'], c['code'], c['window'], c['shot'] or '—', c['speed'], burn, c['sub']))
    L += ['']
    L += ['## §3 章ごと・カットごと', '']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        L += ['### %s（%d カット・%s から）' % (ch, len(cs), fmt_t(cs[0]['start'])), '',
              '| カット | 秒 | 種類 | 素材 | 見せ方 | 副題 | 動き | 見る向き・合図 | 権利 | 画（替えたカットは新しい画）・備考 |', '|---|---|---|---|---|---|---|---|---|---|']
        for c in cs:
            mat = c['code'] + ((':' + c['part']) if c['part'] else '') + ('@%s（%s倍）' % (c['window'], c['speed']) if c['window'] else '')
            view = c['view'] + ((' ' + c['signal']) if c['signal'] else '')
            if c['kind'] == '実写':
                rem = c['note']
            else:
                rem = (c['ga_new'] + ('｜' + c['note'] if c['note'] else '')) if c['ga_new'] else (c['ga'][:60] + ('…' if len(c['ga']) > 60 else ''))
            L.append('| %s%s | %.1f（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                c['cid'], ' 🔧' if c['changed'] else '', c['start'], c['dur'], c['kind'], mat or '—', c['frame'] or '—', c['sub'] or '—',
                c['motion'] or '—', view or '—', (c['rights'].split('（')[0] if c['rights'] else '—'), rem.replace('|', '／')))
        L.append('')
    L += ['## §4 素材の一覧（了承②の対象）', '', '| 記号 | 当てたカット | 取り方 | 置き場（git の外） | 大きさ | バイト | 権利 | 出典の表記（下書き） |', '|---|---|---|---|---|---:|---|---|']
    use = {}
    for c in cuts:
        if c['code']:
            use.setdefault(c['code'], []).append(c['cid'] + ((':' + c['part']) if c['part'] else ''))
    for code, s in sources.items():
        L.append('| %s | %s | %s | `%s` | %s | %s | %s | %s |' % (code, '・'.join(use.get(code, [])) or '（使わない）', s['get'].split(':')[0], s['file'], s['dims'], s['bytes'],
                                                       s['rights'].split('（')[0], s['credit']))
    L += ['', '## §5 門番', '']
    L += ['- 🔴 E %d 件' % len(E)] + ['  - ' + e for e in E]
    L += ['- ⚠️ %d 件' % len(W)] + ['  - ' + w for w in W]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    print('cuts=%d 実写=%d（%.1f%%）映像=%d 写真=%d 再現・吹き出し=%d（第2版 %d）文字だけ=%d 額装・紙面=%d 🔧=%d（%s）' % (
        n, len(photo), ratio * 100, len(film), len(still), len(docs), len(docs0), len(text), len(framed), len(changed), secnote))
    print('種類：', dict(kinds))
    print('動き：', dict(mc))
    print('見る向きの合図：', sum(1 for c in cuts if c['signal']), 'か所', [c['cid'] for c in cuts if c['signal']])
    print('扉を方眼だけ：', card0)
    print('E %d・⚠️ %d' % (len(E), len(W)))
    for e in E:
        print('  E', e)
    for w in W:
        print('  ⚠️', w)
    print('→', OUT_MD)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
