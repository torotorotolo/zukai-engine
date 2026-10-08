# -*- coding: utf-8 -*-
"""20本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-08・映像方針チャット）。

  python ref/ep20/eizou_build/make_list20.py

入力：台本 第2版 ref/ep20/daihon_v2.md §4 の見出し行（画の欄。本文は字数と秒を数えるだけ）
      eizou_build/assign20.tsv（当て方の上書き）・sources20.tsv（出どころ）・bv_shots20.tsv（防衛庁記録のショット）
出力：ref/ep20/eizou_list20.md（生成物＝手で直さない）・eizou_build/list20.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 素材の記号が出どころに無い／手元の取り出しが無い（報告書の P・F・A1P・A1F・K）
  E 防衛庁記録の区間が「使う」ショットの外・区間がほかのカットと重なる・倍率（素材の秒÷カットの秒）が 0.6 未満
  E 写真（P・A1P・J・O）を2つのカットで使う（1点1カット）／写真-124 を c408 の外で使う
  E 冒頭（c101〜c108）に実写でない画／BY-SA の写真の動きが「額ごと」でない
  E 写真と実写の割合が 20% 未満／文字だけの画面が3つ続く
  ⚠️ 同じショットを2つのカットで使う（区間は重ならない）／静止写真の動きが「寄る」に偏る（50%超）
秒＝句読点なし÷365字/分（narr20.py と同じ数え方）＝⑤a の実測で取り直す。
"""
import csv
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
DAIHON = os.path.join(EP, 'daihon_v2.md')
JA123 = os.path.join(REPO, 'ref', 'ja123')
OUT_MD = os.path.join(EP, 'eizou_list20.md')
OUT_TSV = os.path.join(HERE, 'list20.tsv')
PUNCT = '、。？！「」（）・'
CUT = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*')
OPENING = ['c10%d' % i for i in range(1, 9)]
MIN_SPEED = 0.6
PHOTO_LO = 0.20
SPLIT_OK = {'F': '2026-10-08 了承②＝c107 前半・c601 後半'}  # 同じショットを2カットに分けてよいと決まったもの
MOTIONS = ['下から上へ流す', '上から下へ流す', '左から右へ流す', '右から左へ流す', '前から後ろへ流す',
           '額ごと右へ流す', '額ごと左へ流す', '額ごと寄る', '孔を順に寄る', '点を順に寄る', '下から寄る',
           'ゆっくり寄る', 'ゆっくり引く', '左へ流す', '右へ流す', '上へ流す', '下へ流す', '横に流す',
           '順に寄る', '寄る', '引く', '流す']


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
            cur = dict(cid=m.group(1), chap=chap, ga=parts[1].strip() if len(parts) > 1 else '', n=0, q=0, first='')
            rows.append(cur)
            continue
        if cur and ln.startswith('>'):
            s = ln[1:].strip()
            if s.startswith('Q:'):
                cur['q'] += 1
                s = s[2:].strip()
            if not cur['first']:
                cur['first'] = s
            cur['n'] += len(nopunct(s))
    sec = 0.0
    for r in rows:
        r['start'] = sec
        r['dur'] = r['n'] / 365 * 60
        sec += r['dur']
    return rows


def derive(ga):
    """台本の画の欄から、種類・素材・副題・動き・見る向き・額装を読む。"""
    d = dict(kind='図', main='', sub='', motion='', view='', frame='')
    m = re.search(r'副題「(.+?)」', ga)
    d['sub'] = m.group(1) if m else ''
    m = re.search(r'【(横から|上から|正面から)】', ga)
    d['view'] = m.group(1) if m else ''
    if ga.startswith('実写'):
        d['kind'] = '実写'
        if '防衛庁記録' in ga:
            m = re.search(r'防衛庁記録 (\d+):(\d+)〜(\d+):(\d+)', ga)
            if m:
                a = int(m[1]) * 60 + int(m[2])
                b = int(m[3]) * 60 + int(m[4]) + 1
                d['main'] = 'BV@%d-%d' % (a, b)
        elif re.search(r'別添1 写真-(\d+)', ga):
            d['main'] = 'A1P' + re.search(r'別添1 写真-(\d+)', ga)[1]
        elif re.search(r'写真-(\d+)', ga):
            d['main'] = 'P' + re.search(r'写真-(\d+)', ga)[1]
        else:
            d['main'] = '?'
    elif '再現イラスト' in ga:
        d['kind'] = '再現'
        m = re.search(r'再現イラスト (S\d)', ga)
        d['main'] = m[1] if m else 'S?'
    elif '文字の頁' in ga:
        d['kind'] = '文字の頁'
        d['main'] = 'PG'
    elif ga.startswith('図 模式'):
        d['kind'] = '模式'
        d['main'] = '模式'
    elif re.match(r'図 p[\w\-]+ ', ga):
        d['kind'] = '頁'
        if re.search(r'別添1 付図-(\d+)', ga):
            d['main'] = 'A1F' + re.search(r'別添1 付図-(\d+)', ga)[1]
        elif re.search(r'付図-(\d+)', ga):
            d['main'] = 'F' + re.search(r'付図-(\d+)', ga)[1]
        elif '図18' in ga:
            d['main'] = 'K-kz018'
        else:
            d['main'] = 'PG'
    for kw in MOTIONS:
        if kw in ga:
            d['motion'] = kw
            break
    d['frame'] = '額装' if '額装' in ga else ('全画面' if '全画面' in ga else '')
    return d


def motion_class(mo):
    if not mo or mo == '—':
        return ''
    if mo.startswith('映像'):
        return '映像'
    if '順に' in mo or '2点' in mo:
        return '2点'
    if '引' in mo:
        return '引く'
    if '左へ' in mo or '右から左' in mo:
        return '左へ'
    if '右へ' in mo or '左から右' in mo:
        return '右へ'
    if '上へ' in mo:
        return '上へ'
    if '下へ' in mo or '上から下' in mo:
        return '下へ'
    if '流す' in mo:
        return '横へ（向き未定）'
    if '寄らない' in mo:
        return '止め（引用）'
    if '寄' in mo:
        return '寄る'
    return mo


def resolve(code, sources):
    """記号 → 出どころ（file・rights・credit・exists・class）。"""
    if code in sources:
        s = sources[code]
        path = os.path.join(REPO, s['file'])
        return dict(file=s['file'], rights=s['rights'], credit=s['credit'], cls=s['class'],
                    exists=os.path.exists(path), local=False, mb=s.get('mb', ''), page=s['page'])
    pats = [(r'P(\d+)$', 'p%03d.jpg', '報告書 写真-%s'), (r'A1P(\d+)$', 'a1p%03d.jpg', '報告書 別添1 写真-%s'),
            (r'F(\d+)$', 'f%03d.jpg', '報告書 付図-%s'), (r'A1F(\d+)$', 'a1f%03d.jpg', '報告書 別添1 付図-%s')]
    for pat, fn, cr in pats:
        m = re.match(pat, code)
        if m:
            f = fn % int(m[1])
            return dict(file='ref/ja123/' + f, rights='PDL1.0', credit='運輸安全委員会（%s）／縮小・切出' % (cr % m[1]),
                        cls='report', exists=os.path.exists(os.path.join(JA123, f)), local=True, mb='', page='')
    m = re.match(r'K-(\w+)$', code)
    if m:
        f = m[1] + '.png'
        return dict(file='ref/ja123/' + f, rights='PDL1.0', credit='運輸安全委員会（2011年の解説）', cls='report',
                    exists=os.path.exists(os.path.join(JA123, f)), local=True, mb='', page='')
    if re.match(r'S\d$', code) or code in ('模式', 'PG'):
        return dict(file='', rights='自作（形のもと＝報告書の付図）' if code != 'PG' else 'PDL1.0（文字の頁）',
                    credit='', cls='self', exists=True, local=True, mb='', page='')
    return None


def parse_bv(main):
    out = []
    for part in main.split('+'):
        m = re.match(r'BV@([\d.]+)-([\d.]+)$', part.strip())
        if m:
            out.append((float(m[1]), float(m[2])))
    return out


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def main():
    cuts = read_cuts()
    E, W = [], []
    arows = read_tsv(os.path.join(HERE, 'assign20.tsv'))
    dup = [k for k, v in Counter(r['cid'] for r in arows).items() if v > 1]
    if dup:
        E.append('assign20.tsv に同じカットの行が2つ以上（後の行が前の行を上書きする）：%s' % '・'.join(sorted(dup)))
    assign = {r['cid']: r for r in arows}
    known = {c['cid'] for c in cuts}
    for k in assign:
        if k not in known:
            E.append('assign20.tsv のカット %s が台本に無い' % k)
    sources = {r['code']: r for r in read_tsv(os.path.join(HERE, 'sources20.tsv'))}
    shots = read_tsv(os.path.join(HERE, 'bv_shots20.tsv'))
    for s in shots:
        s['a'], s['b'] = float(s['start']), float(s['end'])

    for c in cuts:
        d = derive(c['ga'])
        a = assign.get(c['cid'], {})
        for k in ('kind', 'main', 'sub', 'motion', 'view'):
            v = (a.get(k) or '').strip()
            if v and v != '—':
                d[k] = v
            elif v == '—' and k in ('sub', 'motion', 'view'):
                d[k] = ''
        d['note'] = (a.get('note') or '').strip()
        d['assigned'] = c['cid'] in assign
        c.update(d)

    # 素材の解決・映像の区間
    used_iv, still_use, shot_use = [], {}, {}
    for c in cuts:
        c['rights'], c['credit'], c['speed'], c['src_sec'] = '', '', '', 0.0
        codes = []
        if c['main'].startswith('BV@'):
            ivs = parse_bv(c['main'])
            if not ivs:
                E.append('%s 防衛庁記録の区間が読めない：%s' % (c['cid'], c['main']))
            src = 0.0
            for (x, y) in ivs:
                src += y - x
                hit = [s for s in shots if s['a'] - 0.05 <= x and y <= s['b'] + 0.05]
                if not hit:
                    E.append('%s 区間 %.1f〜%.1f がショット1本に収まらない' % (c['cid'], x, y))
                elif not hit[0]['use'].startswith('使う'):
                    E.append('%s 区間 %.1f〜%.1f は「使わない」ショット %s（%s）' % (c['cid'], x, y, hit[0]['shot'], hit[0]['reason']))
                else:
                    shot_use.setdefault(hit[0]['shot'], []).append(c['cid'])
                    if hit[0]['use'] == '使う（遠景だけ）' and y > hit[0]['b'] + 0.05:
                        E.append('%s 区間がショット %s の遠景の外' % (c['cid'], hit[0]['shot']))
                used_iv.append((x, y, c['cid']))
            c['src_sec'] = src
            sp = src / c['dur'] if c['dur'] else 0
            c['speed'] = '%.2f' % sp
            if sp < MIN_SPEED:
                E.append('%s 倍率 %.2f（素材 %.1f秒÷カット %.1f秒）＜ %.1f＝止め絵になる' % (c['cid'], sp, src, c['dur'], MIN_SPEED))
            codes = ['BV']
        elif c['main'] and c['main'] not in ('?',):
            codes = [c['main']]
        else:
            E.append('%s 素材が決まっていない（%s）' % (c['cid'], c['ga'][:40]))
        rs = []
        for code in codes:
            r = resolve(code, sources)
            if r is None:
                E.append('%s 記号 %s が sources20.tsv に無い' % (c['cid'], code))
                continue
            if r['local'] and not r['exists']:
                E.append('%s 手元の取り出しが無い：%s' % (c['cid'], r['file']))
            rs.append(r)
            if re.match(r'(P|A1P|J|O)\d+$', code):
                still_use.setdefault(code, []).append(c['cid'])
        c['rights'] = ' ＋ '.join(r['rights'] for r in rs)
        c['credit'] = ' ＋ '.join(r['credit'] for r in rs)
        if 'BY-SA' in c['rights'] and '額ごと' not in c['motion']:
            E.append('%s BY-SA の写真の動きが「額ごと」でない（%s）' % (c['cid'], c['motion']))
        if c['main'] == 'P124' and c['cid'] != 'c408':
            E.append('%s 写真-124（第三者の写真）は c408 の1カットだけ' % c['cid'])

    used_iv.sort()
    for i in range(1, len(used_iv)):
        if used_iv[i][0] < used_iv[i - 1][1] - 0.01:
            E.append('防衛庁記録の区間が重なる：%s（%.1f〜%.1f）と %s（%.1f〜%.1f）' % (
                used_iv[i - 1][2], used_iv[i - 1][0], used_iv[i - 1][1], used_iv[i][2], used_iv[i][0], used_iv[i][1]))
    for sh, cs in sorted(shot_use.items()):
        if len(set(cs)) > 1:
            if sh in SPLIT_OK:
                W.append('（了承ずみ＝%s）同じショット %s を %s で使う（区間は重ならない）' % (SPLIT_OK[sh], sh, '・'.join(sorted(set(cs)))))
            else:
                W.append('同じショット %s を %s で使う（区間は重ならない）＝カズヤくんに確かめる' % (sh, '・'.join(sorted(set(cs)))))
    for code, cs in sorted(still_use.items()):
        if len(cs) > 1:
            E.append('写真 %s を2回使う：%s（1点1カット）' % (code, '・'.join(cs)))
    for c in cuts:
        if c['cid'] in OPENING and c['kind'] != '実写':
            E.append('%s 冒頭に実写でない画（%s）' % (c['cid'], c['kind']))

    # 見る向きの合図
    last = None
    for c in cuts:
        c['signal'] = ''
        if c['kind'] == '再現' and c['view']:
            if last and last[1] != c['view']:
                c['signal'] = '🔁 %s→%s（前の再現 %s）＝左上に見る向きの札・替わる瞬間に「%s見ると」' % (
                    last[1].replace('から', ''), c['view'].replace('から', ''), last[0], c['view'].replace('から', 'から'))
            last = (c['cid'], c['view'])

    # 数
    n = len(cuts)
    tot = sum(c['dur'] for c in cuts)
    photo = [c for c in cuts if c['kind'] == '実写']
    film = [c for c in photo if c['main'].startswith('BV@')]
    still = [c for c in photo if not c['main'].startswith('BV@')]
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
    mc = Counter(motion_class(c['motion']) for c in still)
    if still and mc.get('寄る', 0) / len(still) > 0.5:
        W.append('静止写真の動きが「寄る」に偏る（%d/%d）' % (mc['寄る'], len(still)))
    bysa = [c for c in photo if 'BY-SA' in c['rights']]
    quote = [c for c in photo if c['main'] == 'P124']
    kinds = Counter(c['kind'] for c in cuts)

    # 出力（TSV）
    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['cid', 'chap', 'start', 'dur', 'kind', 'main', 'speed', 'sub', 'motion', 'view', 'signal', 'rights', 'credit', 'note', 'ga'])
        for c in cuts:
            w.writerow([c['cid'], c['chap'], '%.1f' % c['start'], '%.1f' % c['dur'], c['kind'], c['main'], c['speed'],
                        c['sub'], c['motion'], c['view'], c['signal'], c['rights'], c['credit'], c['note'], c['ga']])

    # 出力（md）
    L = ['---', 'title: 20本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-10-08', 'tags: [project/jiko-kensho, ep20]', '---', '',
         '# 20本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % n, '',
         '> **生成物＝手で直さない**。作り方＝`python ref/ep20/eizou_build/make_list20.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄・当て方 `eizou_build/assign20.tsv`・出どころ `eizou_build/sources20.tsv`・防衛庁記録のショット `eizou_build/bv_shots20.tsv`）。直すのは assign20.tsv などの入力。',
         '> 秒＝句読点なし÷365字/分（÷365 の見込み＝⑤a の実測で取り直す）。🔧＝assign20.tsv で台本の画の欄から変えたカット。報告書の写真・付図＝`ref/ja123/`（旧版の取り出し・長辺1200・ぼかし0.7）＝1ビット＝額装（横1200px 上限）・白黒のまま。色味は原本（10-07＝回の既定 keep=1.0）。', '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真・実写（この事故） | **%d カット＝%.1f%%**（秒 %.0f＝%.1f%%）＝映像 %d・写真 %d | 20%%以上 %s |' % (
             len(photo), ratio * 100, sum(c['dur'] for c in photo), sum(c['dur'] for c in photo) / tot * 100, len(film), len(still), '✅' if ratio >= PHOTO_LO else '🔴'),
         '| 動く映像（防衛庁記録） | %d カット・%.1f秒（素材の秒 %.1f） | 実効の幅 約544px＝【映像あり】の条件（1280以上）に届かない |' % (
             len(film), sum(c['dur'] for c in film), sum(c['src_sec'] for c in film)),
         '| 文字だけ（文字の頁） | %d カット（%s）・続く最長 %d | できる限り0に近く・3連続で E |' % (len(text), '・'.join(c['cid'] for c in text), mx),
         '| BY-SA（額装・無加工） | %d カット（%s） | 動きは額ごと |' % (len(bysa), '・'.join(c['cid'] for c in bysa)),
         '| 引用（第三者の写真） | %d カット（%s） | 写真-124 だけ・c408 だけ |' % (len(quote), '・'.join(c['cid'] for c in quote)),
         '| 種類 | %s | — |' % '・'.join('%s %d' % (k, v) for k, v in kinds.most_common()),
         '| 静止写真の動き | %s | 寄るだけにしない（10-07） |' % '・'.join('%s %d' % (k, v) for k, v in mc.most_common()),
         '| 合計 | %d カット・%s | — |' % (n, fmt_t(tot)), '']
    L += ['### 章ごと', '', '| 章 | カット | 秒 | 実写 | うち映像 | 再現 | 模式 | 頁 | 文字の頁 |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    chaps = []
    for c in cuts:
        if not chaps or chaps[-1] != c['chap']:
            chaps.append(c['chap'])
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = Counter(c['kind'] for c in cs)
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d | %d |' % (
            ch, len(cs), sum(c['dur'] for c in cs), k['実写'], sum(1 for c in cs if c['main'].startswith('BV@')),
            k['再現'], k['模式'], k['頁'], k['文字の頁']))
    L += ['', '## §1 冒頭（c101〜c108）＝実写だけ', '', '| カット | 秒 | 画 | 素材 | 副題 | 動き | 語りの頭 |', '|---|---|---|---|---|---|---|']
    for c in cuts:
        if c['cid'] in OPENING:
            L.append('| %s%s | %.1f〜%.1f（%.1f） | %s | %s%s | %s | %s | %s |' % (
                c['cid'], ' 🔧' if c['assigned'] else '', c['start'], c['start'] + c['dur'], c['dur'], c['kind'],
                c['main'], '（%s倍）' % c['speed'] if c['speed'] else '', c['sub'], c['motion'], c['first'][:30]))
    L += ['', '- 冒頭の映像＝c103（上空から見た墜落現場）・c104（ヘリの遠景）・c107（まつゆきのボート）。写真＝c101（JA8119・全画面）・c102・c105・c108（報告書・額装）・c106（登山道）',
          '- 秒は ÷365 の見込み（最初の見出し 59.3秒＝46秒の引きは c105〜c106）＝⑤a-2 の音で取り直す。映像の倍率も⑤a の秒で計算し直す', '']
    L += ['## §2 防衛庁記録「昭和６０年防衛庁記録」のショット（23:51〜25:22・1秒1コマで全部見た）', '',
          '| ショット | 秒 | 写っているもの | 画面の字 | 使う | 理由 | 当てたカット |', '|---|---|---|---|---|---|---|']
    for s in shots:
        L.append('| %s | %s〜%s（%s〜%s） | %s | %s | %s | %s | %s |' % (
            s['shot'], s['start'], s['end'], fmt_t(s['a']), fmt_t(s['b']), s['what'], s['text_in_frame'], s['use'], s['reason'],
            '・'.join(sorted(set(shot_use.get(s['shot'], [])))) or '—'))
    L += ['', '- 語の確かめ（音）＝映画の音を2つの認識器で：YouTube の自動字幕「最大の**最愛**派遣」／Windows の日本語音声認識（MS-1041-80-DESK）「航空機事故に対するものとしては最大の**災害**派遣」＋映画の中の新聞の見出し「最大規模の災派」＝**「最大の災害派遣」**（c522 の引用は正しい）。「発見」は2つとも一致。「まつゆき」は音では認識器が拾えない（Windows「夕刊松平…」）＝**ボートの舳先の字「まつゆき01」**で確かめた',
          '- 人数（記録映画の語り）＝約5万2千名・約1,200機は2つの認識器で一致・車両約1,800両は YouTube だけ（Windows は崩れた）＝台本は使っていない', '']

    L += ['## §3 章ごと・カットごと', '']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        L += ['### %s（%d カット・%s から）' % (ch, len(cs), fmt_t(cs[0]['start'])), '',
              '| カット | 秒 | 種類 | 素材（記号@区間・倍率） | 副題 | 動き | 見る向き・合図 | 権利 | 備考 |', '|---|---|---|---|---|---|---|---|---|']
        for c in cs:
            mat = c['main'] + ('（%s倍）' % c['speed'] if c['speed'] else '')
            view = c['view'] + ((' ' + c['signal']) if c['signal'] else '')
            note = c['note'] if c['note'] else (c['ga'][:60] + '…' if c['kind'] in ('再現', '模式', '頁', '文字の頁') else '')
            L.append('| %s%s | %.1f（%.1f） | %s | %s | %s | %s | %s | %s | %s |' % (
                c['cid'], ' 🔧' if c['assigned'] else '', c['start'], c['dur'], c['kind'], mat, c['sub'] or '—',
                c['motion'] or '—', view or '—', c['rights'] or '—', note.replace('|', '／')))
        L.append('')

    L += ['## §4 取得の一覧（了承②の対象）', '', '| 記号 | 当てたカット | 置き場（git の外） | 出どころ | 大きさ | 権利 |', '|---|---|---|---|---|---|']
    use_by_code = {}
    for c in cuts:
        code = 'BV' if c['main'].startswith('BV@') else c['main']
        if code in sources:
            use_by_code.setdefault(code, []).append(c['cid'])
    for code, s in sources.items():
        L.append('| %s | %s | `%s` | %s | %s・%sMB | %s |' % (
            code, '・'.join(use_by_code.get(code, [])) or '（使わない）', s['file'], s['page'], s['dims'], s['mb'], s['rights']))
    L += ['', '- 報告書の写真・付図・解説の図は手元の `ref/ja123/`（旧版の取り出し）と `ref/ep20/src/*.pdf`＝落とさない', '']

    L += ['## §5 門番', '']
    L += ['- 🔴 E %d 件' % len(E)] + ['  - ' + e for e in E]
    L += ['- ⚠️ %d 件' % len(W)] + ['  - ' + w for w in W]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    print('cuts=%d 実写=%d（%.1f%%）映像=%d（%.1f秒）文字の頁=%d BY-SA=%d 引用=%d' % (
        n, len(photo), ratio * 100, len(film), sum(c['dur'] for c in film), len(text), len(bysa), len(quote)))
    print('静止写真の動き：', dict(mc))
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
