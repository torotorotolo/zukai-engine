# -*- coding: utf-8 -*-
"""21本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-12・映像方針チャット）。20本目の make_list20.py を写して素材の記号を21本目に替えた。

  python ref/ep21/eizou_build/make_list21.py

入力：台本 第2版 ref/ep21/daihon_v2.md §4 の見出し行（画の欄。本文は字数と秒を数えるだけ）
      eizou_build/assign21.tsv（当て方＝実写とイメージは全部ここ）・sources21.tsv（出どころ）・shots21.tsv（映像のショットの境目）
出力：ref/ep21/eizou_list21.md（生成物＝手で直さない）・eizou_build/list21.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 実写・イメージのカットに素材の記号が無い／記号が sources21.tsv に無い
  E 映像の区間がショット1本に収まらない／倍率（区間の秒÷カットの秒）0.6 未満
  E 写真を2つのカットで使う（1点1カット）／BY-SA の写真・映像の動きが「額装」でない
  E 冒頭（c101〜c109）に実写でない画／写真と実写（この事件の物）が 20% 未満／文字だけの画面が3つ続く
  ⚠️ BY-SA の映像の倍率が 1.0 から 0.05 以上ずれる（等速で使う）／静止写真の動きが「寄る」に偏る（50%超）／章の写真と実写が 20% 未満
秒＝句読点なし÷365字/分（m21.py と同じ数え方）＝⑤a の実測で取り直す。audio/narration.json が21本目の並びなら実測を使う（ほかの回の物なら使わない）。
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
OUT_MD = os.path.join(EP, 'eizou_list21.md')
OUT_TSV = os.path.join(HERE, 'list21.tsv')
NARR = os.path.join(REPO, 'audio', 'narration.json')
PUNCT = '、。？！「」（）・'
CUT = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*')
OPENING = ['c10%d' % i for i in range(1, 10)]
MIN_SPEED = 0.6
PHOTO_LO = 0.20
LEAD, TAIL, CARD_SEC = 0.35, 0.50, 2.0


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
            cur = dict(cid=m.group(1), chap=chap, ga=parts[1].strip() if len(parts) > 1 else '', n=0, first='')
            rows.append(cur)
            continue
        if cur and ln.startswith('>'):
            s = ln[1:].strip()
            if s.startswith('Q:'):
                s = s[2:].strip()
            if not cur['first']:
                cur['first'] = s
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
    if ga.startswith('イメージ'):
        return 'イメージ'
    if '文字の頁' in ga:
        return '文字の頁'
    if ga.startswith('図 模式'):
        return '模式'
    if ga.startswith('図 NTSB'):
        return 'NTSB'
    if ga.startswith('図 RG237'):
        return 'RG237'
    if ga.startswith('図'):
        return '頁'
    return '?'


def motion_class(mo):
    if not mo or mo == '—':
        return ''
    if mo.startswith('映像'):
        return '映像'
    if mo.startswith('額装'):
        return '額装'
    if '順に' in mo or '2点' in mo:
        return '2点'
    if '引' in mo:
        return '引く'
    if '左へ' in mo:
        return '左へ'
    if '右へ' in mo:
        return '右へ'
    if '上へ' in mo:
        return '上へ'
    if '下へ' in mo:
        return '下へ'
    if '寄' in mo:
        return '寄る'
    return mo


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def main():
    cuts, secnote = read_cuts()
    E, W = [], []
    arows = read_tsv(os.path.join(HERE, 'assign21.tsv'))
    dup = [k for k, v in Counter(r['cid'] for r in arows).items() if v > 1]
    if dup:
        E.append('assign21.tsv に同じカットの行が2つ以上：%s' % '・'.join(sorted(dup)))
    assign = {r['cid']: r for r in arows}
    known = {c['cid'] for c in cuts}
    for k in assign:
        if k not in known:
            E.append('assign21.tsv のカット %s が台本に無い' % k)
    sources = {r['code']: r for r in read_tsv(os.path.join(HERE, 'sources21.tsv'))}
    shots = {}
    for r in read_tsv(os.path.join(HERE, 'shots21.tsv')):
        shots.setdefault(r['film'], []).append((float(r['start']), float(r['end']), r['shot']))

    for c in cuts:
        a = assign.get(c['cid'], {})
        c['kind'] = (a.get('kind') or '').strip() or base_kind(c['ga'])
        if c['kind'] == '図':
            c['kind'] = base_kind(c['ga'])
        c['main'] = (a.get('main') or '').strip().replace('—', '')
        c['sub'] = (a.get('sub') or '').strip().replace('—', '')
        if not c['sub']:
            m = re.search(r'副題「(.+?)」', c['ga'])
            c['sub'] = m.group(1) if m and c['kind'] in ('実写', 'イメージ') else ''
        c['motion'] = (a.get('motion') or '').strip().replace('—', '')
        c['view'] = (a.get('view') or '').strip().replace('—', '')
        c['note'] = (a.get('note') or '').strip()
        c['assigned'] = c['cid'] in assign and c['kind'] in ('実写', 'イメージ')
        c['changed'] = '🔧' in c['note']

    still_use, film_use = {}, {}
    for c in cuts:
        c['rights'] = c['credit'] = c['speed'] = c['window'] = c['shot'] = ''
        c['src_sec'] = 0.0
        if c['kind'] not in ('実写', 'イメージ'):
            continue
        if not c['main']:
            E.append('%s 実写・イメージなのに素材の記号が無い（%s）' % (c['cid'], c['ga'][:40]))
            continue
        m = re.match(r'([A-Za-z0-9]+)@([\d.]+)-([\d.]+)$', c['main'])
        code = m.group(1) if m else c['main']
        s = sources.get(code)
        if not s:
            E.append('%s 記号 %s が sources21.tsv に無い' % (c['cid'], code))
            continue
        c['code'] = code
        c['rights'], c['credit'], c['cls'] = s['rights'], s['credit'], s['class']
        bysa = 'BY-SA' in s['rights']
        if bysa and not c['motion'].startswith('額装'):
            E.append('%s BY-SA の動きが「額装」でない（%s）' % (c['cid'], c['motion']))
        if s['class'] == 'film':
            if not m:
                E.append('%s 映像なのに区間が無い（%s）' % (c['cid'], c['main']))
                continue
            x, y = float(m.group(2)), float(m.group(3))
            c['src_sec'] = y - x
            c['window'] = '%.1f〜%.1f' % (x, y)
            hit = [sh for sh in shots.get(code, []) if sh[0] - 0.05 <= x and y <= sh[1] + 0.05]
            if not hit:
                E.append('%s %s の区間 %.1f〜%.1f がショット1本に収まらない' % (c['cid'], code, x, y))
            else:
                c['shot'] = hit[0][2]
            sp = c['src_sec'] / c['cont'] if c['cont'] else 0
            c['speed'] = '%.2f' % sp
            if sp < MIN_SPEED:
                E.append('%s 倍率 %.2f（区間 %.1f秒÷カット %.1f秒）＜ %.1f＝止め絵になる' % (c['cid'], sp, c['src_sec'], c['cont'], MIN_SPEED))
            if bysa and abs(sp - 1.0) >= 0.05:
                W.append('%s BY-SA の映像の倍率 %.2f＝等速で使う（⑤a の秒で区間の長さを合わせる）' % (c['cid'], sp))
            film_use.setdefault(code, []).append((x, y, c['cid']))
        else:
            if m:
                E.append('%s 写真に区間が付いている（%s）' % (c['cid'], c['main']))
            still_use.setdefault(code, []).append(c['cid'])

    for code, cs in sorted(still_use.items()):
        if len(cs) > 1:
            E.append('写真 %s を2回使う：%s（1点1カット）' % (code, '・'.join(cs)))
    for code, ivs in sorted(film_use.items()):
        ivs.sort()
        for i in range(1, len(ivs)):
            if ivs[i][0] < ivs[i - 1][1] - 0.01:
                E.append('映像 %s の区間が重なる：%s と %s' % (code, ivs[i - 1][2], ivs[i][2]))
    for c in cuts:
        if c['cid'] in OPENING and c['kind'] != '実写':
            E.append('%s 冒頭に実写でない画（%s）' % (c['cid'], c['kind']))

    # 見る向きの合図（図の上から↔横からの切り替わり）
    last = None
    for c in cuts:
        c['signal'] = ''
        if c['view']:
            if last and last[1] != c['view']:
                c['signal'] = '🔁 %s→%s（前の図 %s）＝左上に見る向きの札・替わる瞬間に「%s見ると」' % (
                    last[1], c['view'], last[0], c['view'].replace('から', 'から'))
            last = (c['cid'], c['view'])

    n = len(cuts)
    tot = sum(c['dur'] for c in cuts)
    photo = [c for c in cuts if c['kind'] == '実写']
    film = [c for c in photo if c.get('cls') == 'film']
    still = [c for c in photo if c.get('cls') == 'photo']
    image = [c for c in cuts if c['kind'] == 'イメージ']
    text = [c for c in cuts if c['kind'] == '文字の頁']
    ratio = len(photo) / n
    if ratio < PHOTO_LO:
        E.append('写真と実写 %.1f%% ＜ 20%%' % (ratio * 100))
    run, mx = 0, 0
    for c in cuts:
        run = run + 1 if c['kind'] == '文字の頁' else 0
        mx = max(mx, run)
    if mx >= 3:
        E.append('文字だけの画面が %d つ続く' % mx)
    mc = Counter(motion_class(c['motion']) for c in still + image)
    if still and mc.get('寄る', 0) / len(still + image) > 0.5:
        W.append('静止写真の動きが「寄る」に偏る（%d/%d）' % (mc['寄る'], len(still + image)))
    chaps = []
    for c in cuts:
        if not chaps or chaps[-1] != c['chap']:
            chaps.append(c['chap'])
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = sum(1 for c in cs if c['kind'] == '実写')
        if k / len(cs) < PHOTO_LO:
            W.append('章「%s」の写真と実写 %d/%d（%.0f%%）＜ 20%%' % (ch.split('（')[0], k, len(cs), k / len(cs) * 100))
    bysa = [c for c in photo if 'BY-SA' in c['rights']]
    kinds = Counter(c['kind'] for c in cuts)
    changed = [c for c in cuts if c['changed']]

    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['cid', 'chap', 'start', 'dur', 'kind', 'main', 'window', 'speed', 'sub', 'motion', 'view', 'signal', 'rights', 'credit', 'note', 'ga'])
        for c in cuts:
            w.writerow([c['cid'], c['chap'], '%.1f' % c['start'], '%.1f' % c['dur'], c['kind'], c.get('code', ''), c['window'], c['speed'],
                        c['sub'], c['motion'], c['view'], c['signal'], c['rights'], c['credit'], c['note'], c['ga']])

    L = ['---', 'title: 21本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-10-12', 'tags: [project/jiko-kensho, ep21]', '---', '',
         '# 21本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % n, '',
         '> **生成物＝手で直さない**。作り方＝`python ref/ep21/eizou_build/make_list21.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄・当て方 `eizou_build/assign21.tsv`・出どころ `eizou_build/sources21.tsv`・映像のショット `eizou_build/shots21.tsv`）。直すのは入力の TSV。',
         '> 秒＝%s（⑤a の音で取り直す）。🔧＝台本の画の欄から素材を替えたカット（assign21.tsv の note）。色味は原本（10-07）・写真は画面いっぱい（10-11）＝例外は BY-SA と 4:3 の映像（了承②）。見た画像の記録＝`eizou_build/seen21.tsv`。' % secnote, '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真・実写（この事件） | **%d カット＝%.1f%%**（秒 %.0f＝%.1f%%）＝映像 %d・写真 %d | 20%%以上 %s |' % (
             len(photo), ratio * 100, sum(c['dur'] for c in photo), sum(c['dur'] for c in photo) / tot * 100, len(film), len(still), '✅' if ratio >= PHOTO_LO else '🔴'),
         '| イメージ（数えない） | %d カット（%s） | 画面に「イメージ」 |' % (len(image), '・'.join(c['cid'] for c in image)),
         '| 文字だけ（文字の頁） | %d カット（%s）・続く最長 %d | できる限り0に近く |' % (len(text), '・'.join(c['cid'] for c in text), mx),
         '| BY-SA（額装・無加工） | %d カット（%s） | 寄り0・映像は等速 |' % (len(bysa), '・'.join(c['cid'] for c in bysa)),
         '| 🔧 素材を替えたカット | %d（%s） | 台本の画の欄は⑤b でこの一覧に従う |' % (len(changed), '・'.join(c['cid'] for c in changed)),
         '| 種類 | %s | — |' % '・'.join('%s %d' % (k, v) for k, v in kinds.most_common()),
         '| 静止写真とイメージの動き | %s | 寄るだけにしない（10-07） |' % '・'.join('%s %d' % (k, v) for k, v in mc.most_common()),
         '| 合計 | %d カット・%s | — |' % (n, fmt_t(tot)), '']
    L += ['### 章ごと', '', '| 章 | カット | 秒 | 実写 | うち映像 | イメージ | 模式 | NTSB・RG237・頁 | 文字の頁 |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = Counter(c['kind'] for c in cs)
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d | %d |' % (
            ch, len(cs), sum(c['dur'] for c in cs), k['実写'], sum(1 for c in cs if c.get('cls') == 'film'), k['イメージ'],
            k['模式'], k['NTSB'] + k['RG237'] + k['頁'], k['文字の頁']))
    L += ['', '## §1 冒頭（c101〜c109）＝実写だけ', '', '| カット | 秒 | 素材（区間・倍率） | 副題 | 動き | 語りの頭 |', '|---|---|---|---|---|---|']
    for c in cuts:
        if c['cid'] in OPENING:
            mat = c.get('code', '') + ('@%s（%s倍）' % (c['window'], c['speed']) if c['window'] else '')
            L.append('| %s | %.1f〜%.1f（%.1f） | %s | %s | %s | %s |' % (
                c['cid'], c['start'], c['start'] + c['dur'], c['dur'], mat, c['sub'], c['motion'], c['first'][:30]))
    L += ['', '- 引き＝c105 の終わり %.1f秒（46秒より前）・最初の見出しの手前 c109 の終わり %.1f秒' % (
        next(c['start'] + c['dur'] for c in cuts if c['cid'] == 'c105'), next(c['start'] + c['dur'] for c in cuts if c['cid'] == 'c109')),
        '- 映像の区間は全部1秒1コマで見た（c713 だけ1秒おき）。負傷者・担架・遺体・私人の近い顔なし', '']
    L += ['## §2 映像の区間', '', '| カット | 映像 | 区間（秒） | ショット | 倍率 | 副題 | 備考 |', '|---|---|---|---|---|---|---|']
    for c in cuts:
        if c.get('cls') == 'film':
            L.append('| %s | %s | %s | %s | %s | %s | %s |' % (c['cid'], c['code'], c['window'], c['shot'], c['speed'], c['sub'], c['note'].replace('|', '／')))
    L += ['']
    L += ['## §3 章ごと・カットごと', '']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        L += ['### %s（%d カット・%s から）' % (ch, len(cs), fmt_t(cs[0]['start'])), '',
              '| カット | 秒 | 種類 | 素材 | 副題 | 動き | 見る向き・合図 | 権利 | 備考 |', '|---|---|---|---|---|---|---|---|---|']
        for c in cs:
            mat = c.get('code', '') + ('@%s（%s倍）' % (c['window'], c['speed']) if c['window'] else '')
            view = c['view'] + ((' ' + c['signal']) if c['signal'] else '')
            note = c['note'] if c['note'] else (c['ga'][:50] + '…' if c['kind'] not in ('実写', 'イメージ') else '')
            L.append('| %s%s | %.1f（%.1f） | %s | %s | %s | %s | %s | %s | %s |' % (
                c['cid'], ' 🔧' if c['changed'] else '', c['start'], c['dur'], c['kind'], mat or '—', c['sub'] or '—',
                c['motion'] or '—', view or '—', c['rights'] or '—', note.replace('|', '／')))
        L.append('')
    L += ['## §4 素材の一覧（了承②の対象）', '', '| 記号 | 当てたカット | 置き場（git の外） | 大きさ | 権利 | 出典の表記（下書き） |', '|---|---|---|---|---|---|']
    use = {}
    for c in cuts:
        if c.get('code'):
            use.setdefault(c['code'], []).append(c['cid'])
    for code, s in sources.items():
        L.append('| %s | %s | `%s` | %s | %s | %s |' % (code, '・'.join(use.get(code, [])) or '（使わない）', s['file'], s['dims'], s['rights'], s['credit']))
    L += ['', '## §5 門番', '']
    L += ['- 🔴 E %d 件' % len(E)] + ['  - ' + e for e in E]
    L += ['- ⚠️ %d 件' % len(W)] + ['  - ' + w for w in W]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    print('cuts=%d 実写=%d（%.1f%%）映像=%d 写真=%d イメージ=%d 文字の頁=%d BY-SA=%d 🔧=%d（%s）' % (
        n, len(photo), ratio * 100, len(film), len(still), len(image), len(text), len(bysa), len(changed), secnote))
    print('動き：', dict(mc))
    print('見る向きの合図：', sum(1 for c in cuts if c['signal']), 'か所')
    print('E %d・⚠️ %d' % (len(E), len(W)))
    for e in E:
        print('  E', e)
    for w in W:
        print('  ⚠️', w)
    print('→', OUT_MD)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
