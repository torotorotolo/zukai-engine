# -*- coding: utf-8 -*-
"""23本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-18・映像方針チャット）。22本目の make_list22.py を写して23本目の型（写真だけ・額装・図の見た目の型）に替えた。

  python ref/ep23/eizou_build/make_list23.py

入力：台本 第2版 ref/ep23/daihon_v2.md §4 の見出し行（画の欄。語りは字数と秒を数えるだけ）
      eizou_build/assign23.psv（当て方＝実写とイメージは全部ここ・図の見る向きと見た目の型）・sources23.psv（出どころ）・dup23_orb.tsv（同じ写真・同じ視点の組）
出力：ref/ep23/eizou_list23.md（生成物＝手で直さない）・eizou_build/list23.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 実写・イメージに素材の記号が無い／記号が sources23.psv に無い／同じ写真（記号＋寄りの名）を2回／A でない写真を寄りを変えて2回
  E 同じ写真・同じ視点の組（dup23_orb.tsv の一致点 40 以上でつながる組）から2点
  E BY-SA が「額装（BY-SA）」でない・動きが「額ごと」でない／小さい公共ヌリ（額装（小さい））を全面にする
  E 冒頭（c101〜c109）に実写でない画／写真と実写（この事故の物）が 20% 未満／文字だけの画面が3つ続く
  E 図の型（模式・文字だけ・実写・イメージのほか）が全編で3回以上（10-15「同じ図を何度も使わない」＝台本の設計で2回まで）
  ⚠️ 続く図（あいだの写真とイメージは飛ばす）で見た目の型が同じ／静止写真の動きが「寄る」に偏る（50%超）／章の写真が 20% 未満
  ⚠️ 別の写真なのに副題が同じ／素材が決まっていない（pending）
  🆕 ⑤b-1：E フリー素材の映像（mp4）が実測のカットの長さに足りない＝倍率（素材の秒÷カットの秒）が 0.6 未満（footage.py の決まり＝止め絵に）、
     または 1.0 未満なのに動きの欄が「映像（0.xx倍）」でない（等速のつもりで尻が足りない）／⚠️ 素材のファイルが手元に無い（長さを測れない）
秒＝⑤b-1（2026-10-18）から **audio/narration.json の実測**（カットの声＋前 0.35＋後 0.50・第2章からの章の頭の前に扉 2.0＝scene_jiko と同じ式・
  22本目 make_list22 の型）。narration.json のカットが台本と合わないときだけ句読点なし÷365字/分（映像方針の見込み）に落ちる＝出力に書く。
  倍率の分母（cont）は扉を除く。
"""
import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
NARR = os.path.join(REPO, 'audio', 'narration.json')
LEAD, TAIL, CARD_SEC = 0.35, 0.50, 2.0          # scene_jiko.LEAD・TAIL・CARD_SEC と同じ値（ep23 は TAIL_EXTRA〈quote〉のカットなし＝決め所0）
RATE_MIN = 0.6                                   # footage.py の注「rate が 0.6 を下回る欄は動画にせず止め絵」
DAIHON = os.path.join(EP, 'daihon_v2.md')
OUT_MD = os.path.join(EP, 'eizou_list23.md')
OUT_TSV = os.path.join(HERE, 'list23.tsv')
PUNCT = '、。？！「」（）・'
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
OPENING = ['c10%d' % i for i in range(1, 10)]
PHOTO_LO = 0.20
DUP_TH = 40
# 使わない点（使うと E）＝映像方針で絵を見て外した理由（10-18）
NG = {'C221': '左下に横たわる人（ジーンズの脚）', 'C69': '瓦礫の中に白い大きな袋（生存者の話のカットに置かない）',
      'C227': '手前に群衆の顔（BY-SA＝モザイク不可）', 'C154': '縞の服の私人', 'C163': '大きな袋を運ぶ', 'C32': '大きな袋を吊る',
      'C222': '大きな黄色い袋が並ぶ', 'C128': '大きな黄色い袋', 'C184': 'カメラに向かった記念写真（題に名前）',
      'C119': '休む隊員の横に黄色い大きな袋2つ', 'C236': 'C2K001（삼풍001）と同じ写真（相関 0.939）'}


def nopunct(s):
    return ''.join(ch for ch in s if ch not in PUNCT and not ch.isspace())


def read_psv(path):
    with open(path, encoding='utf-8') as f:
        lines = [ln.rstrip('\n') for ln in f if not ln.startswith('#') and ln.strip()]
    return lines


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
    note = '÷365 の見込み（narration.json が無い・台本と合わない）'
    if os.path.exists(NARR):
        dur = json.load(open(NARR, encoding='utf-8')).get('durations', {})
        if [r['cid'] for r in rows] == [c for c in dur if c != 'ed01']:
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


def media_len(path):
    """素材の長さ（秒）＝ffprobe。無い・読めないは None（門番は ⚠️＝測れない）"""
    p = os.path.join(REPO, path)
    if not os.path.exists(p):
        return None
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def base_kind(ga):
    if ga.startswith('実写'):
        return '実写'
    if ga.startswith('イメージ'):
        return 'イメージ'
    if ga.startswith('panel'):
        return '文字だけ'
    if ga.startswith('図 '):
        return ga.split()[1].split('（')[0]
    return '?'


def motion_class(mo):
    if not mo:
        return ''
    if mo.startswith('映像'):
        return '映像'
    pre = '額ごと' if mo.startswith('額ごと') else ('額の中で' if mo.startswith('額の中で') else '')
    for key, name in (('引', '引く'), ('左へ', '左へ'), ('右へ', '右へ'), ('上へ', '上へ'), ('下へ', '下へ'), ('寄', '寄る')):
        if key in mo:
            return pre + name
    return mo


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def clusters():
    par = {}

    def f(x):
        par.setdefault(x, x)
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    p = os.path.join(HERE, 'dup23_orb.tsv')
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        n, a, b = ln.rstrip('\n').split('\t')
        if int(n) >= DUP_TH:
            par[f(a)] = f(b)
    groups = defaultdict(list)
    for x in list(par):
        groups[f(x)].append(x)
    out = {}
    for k, v in groups.items():
        for x in v:
            out[x] = tuple(sorted(v, key=lambda s: (len(s), s)))
    return out


def code_key(code):
    """記号 → 組の鍵（Commons の y95 は #番号・研究院の手元は sire_NNNNN.jpg）"""
    if re.match(r'^C\d+$', code):
        return '#' + code[1:]
    if code in ('S52399', 'S52400'):
        return 'sire_%s.jpg' % code[1:]
    return code


def main():
    cuts, tnote = read_cuts()
    E, W = [], []
    arows = [ln.split('|') for ln in read_psv(os.path.join(HERE, 'assign23.psv'))]
    bad = [r[0] for r in arows if len(r) != 10]
    if bad:
        E.append('assign23.psv の列の数が10でない行：%s' % '・'.join(bad))
    keys = ['cid', 'kind', 'main', 'frame', 'sub', 'motion', 'view', 'look', 'ga_new', 'note']
    assign = {}
    for r in arows:
        if len(r) == 10:
            if r[0] in assign:
                E.append('assign23.psv に同じカットの行が2つ：%s' % r[0])
            assign[r[0]] = dict(zip(keys, [x.strip() for x in r]))
    known = {c['cid'] for c in cuts}
    for k in assign:
        if k not in known:
            E.append('assign23.psv のカット %s が台本に無い' % k)
    srows = read_psv(os.path.join(HERE, 'sources23.psv'))
    shead = srows[0].split('|')
    sources = {r.split('|')[0]: dict(zip(shead, r.split('|'))) for r in srows[1:]}
    clu = clusters()

    for c in cuts:
        a = assign.get(c['cid'], {})
        c['kind0'] = base_kind(c['ga'])
        for k in keys[1:]:
            c[k] = a.get(k, '')
        c['kind'] = c['kind'] or c['kind0']
        if c['kind'] == '実写' and not c['sub']:
            m = re.search(r'副題「(.+?)」', c['ga'])
            c['sub'] = m.group(1) if m else ''
        c['changed'] = '🔧' in c['note']

    use = defaultdict(list)
    for c in cuts:
        c['code'] = c['part'] = c['rights'] = c['credit'] = c['get'] = ''
        if c['kind'] not in ('実写', 'イメージ'):
            continue
        if not c['main']:
            E.append('%s %s なのに素材の記号が無い' % (c['cid'], c['kind']))
            continue
        code, part = (c['main'].split(':', 1) + [''])[:2]
        s = sources.get(code)
        if not s:
            E.append('%s 記号 %s が sources23.psv に無い' % (c['cid'], code))
            continue
        c['code'], c['part'], c['rights'], c['credit'], c['get'] = code, part, s['rights'], s['credit'], s['get']
        if s['file'].endswith('.mp4'):
            # 🆕 ⑤b-1：映像の素材は実測のカットの長さ（cont＝扉を除く）に足りるか。等速＝伸ばさない／足りなければ倍率を動きの欄に書く
            have = media_len(s['file'])
            c['src_len'] = have
            if have is None:
                W.append('%s 映像の素材 %s が手元に無い＝長さを測れない' % (c['cid'], s['file']))
            else:
                c['rate'] = have / c['cont']
                mr = re.search(r'映像（(\d\.\d+)倍）', c['motion'])
                if c['rate'] < RATE_MIN:
                    E.append('%s 映像の素材 %.2f秒 ÷ カット %.2f秒 ＝ %.2f倍 ＜ %.1f（止め絵にする・素材を替える）' % (c['cid'], have, c['cont'], c['rate'], RATE_MIN))
                elif c['rate'] < 1.0 and not (mr and float(mr.group(1)) <= c['rate'] + 1e-9):
                    E.append('%s 映像の素材 %.2f秒 がカット %.2f秒 に足りない（等速なら尻が %.2f秒 欠ける）＝動きの欄を「映像（%.2f倍）」以下に' % (
                        c['cid'], have, c['cont'], c['cont'] - have, int(c['rate'] * 100) / 100))
        if code in NG:
            E.append('%s 使わない点 %s（%s）' % (c['cid'], code, NG[code]))
        if s['get'] == 'pending':
            W.append('%s 素材が決まっていない（%s＝%s）' % (c['cid'], code, s['note']))
        use[code].append((c['cid'], part))
        r = s['rights']
        if r.startswith('BY-SA'):
            if c['frame'] != '額装（BY-SA）':
                E.append('%s BY-SA の %s が額装（BY-SA）でない（%s）' % (c['cid'], code, c['frame']))
            if not c['motion'].startswith('額ごと'):
                E.append('%s BY-SA の %s の動きが「額ごと」でない（%s）＝写真は常に全部見える動きだけ' % (c['cid'], code, c['motion']))
        if c['frame'] in ('額装（小さい）', '額装（縦長）') and c['motion'] and not (c['motion'].startswith('額')):
            E.append('%s 小さい・縦長の写真の動き（%s）＝額の中で' % (c['cid'], c['motion']))
        if c['kind'] == '実写' and c['frame'].startswith('全面') and not r.startswith('A'):
            E.append('%s 全面にしてよいのは A（公共ヌリ第1類型・CC BY）だけ（%s）' % (c['cid'], r))

    for code, us in sorted(use.items()):
        if len(us) > 1:
            parts = [p for _, p in us]
            rights = sources[code]['rights']
            if not rights.startswith('A') or len(set(parts)) < len(parts) or '' in parts:
                E.append('写真 %s を2回使う：%s（1点1カット・A は寄りの名を分ける）' % (code, '・'.join(x for x, _ in us)))
    seen_cl = defaultdict(list)
    for code, us in use.items():
        k = code_key(code)
        if k in clu:
            seen_cl[clu[k]].append((code, us[0][0]))
    for g, items in seen_cl.items():
        if len(items) > 1:
            E.append('同じ写真・同じ視点の組（%s）から %d 点：%s' % ('・'.join(g), len(items), '・'.join('%s（%s）' % (a, b) for a, b in items)))
    for c in cuts:
        if c['cid'] in OPENING and c['kind'] != '実写':
            E.append('%s 冒頭に実写でない画（%s）' % (c['cid'], c['kind']))

    # 図の型（模式は「別の絵の集まり」＝見た目の型で見る）
    tc = Counter(c['kind'] for c in cuts if c['kind'] not in ('模式', '実写', 'イメージ', '文字だけ'))
    for k, v in tc.items():
        if v > 2:
            E.append('図の型「%s」が %d 回（2回まで）' % (k, v))
    prev = None
    for c in cuts:
        if c['kind'] in ('実写', 'イメージ'):
            continue
        lk = c['look'] or c['kind']
        if prev and prev[1] == lk:
            W.append('続く図で見た目の型が同じ（%s）：%s→%s' % (lk, prev[0], c['cid']))
        prev = (c['cid'], lk)
    last = None
    for c in cuts:
        c['signal'] = ''
        if c['view'] and c['kind'] not in ('実写', 'イメージ'):
            if last and last[1] != c['view']:
                c['signal'] = '🔁 %s→%s（前の図 %s）' % (last[1], c['view'], last[0])
            last = (c['cid'], c['view'])

    n = len(cuts)
    tot = sum(c['dur'] for c in cuts)
    photo = [c for c in cuts if c['kind'] == '実写']
    stock = [c for c in cuts if c['kind'] == 'イメージ']
    text = [c for c in cuts if c['kind'] == '文字だけ']
    ratio = len(photo) / n
    if ratio < PHOTO_LO:
        E.append('写真と実写 %.1f%% ＜ 20%%' % (ratio * 100))
    run = mx = 0
    for c in cuts:
        run = run + 1 if c['kind'] == '文字だけ' else 0
        mx = max(mx, run)
    if mx >= 3:
        E.append('文字だけの画面が %d つ続く' % mx)
    mc = Counter(motion_class(c['motion']) for c in photo)
    if photo and sum(v for k, v in mc.items() if k.endswith('寄る')) / len(photo) > 0.5:
        W.append('静止写真の動きが「寄る」に偏る（%d/%d）' % (sum(v for k, v in mc.items() if k.endswith('寄る')), len(photo)))
    chaps = []
    for c in cuts:
        if not chaps or chaps[-1] != c['chap']:
            chaps.append(c['chap'])
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = sum(1 for c in cs if c['kind'] == '実写')
        if k / len(cs) < PHOTO_LO:
            W.append('章「%s」の写真と実写 %d/%d（%.0f%%）＜ 20%%' % (ch.split('（')[0], k, len(cs), k / len(cs) * 100))
    subs = defaultdict(set)
    for c in photo:
        subs[c['sub']].add(c['code'])
    for s, cs in subs.items():
        if len(cs) > 1:
            W.append('別の写真なのに副題が同じ「%s」：%s' % (s, '・'.join(sorted(cs))))
    framed = [c for c in photo if c['frame'].startswith('額装')]
    fulls = [c for c in photo if c['frame'].startswith('全面')]
    kinds = Counter(c['kind'] for c in cuts)
    looks = Counter(c['look'] for c in cuts if c['kind'] not in ('実写', 'イメージ', '文字だけ'))
    changed = [c for c in cuts if c['changed']]
    heads = {}
    for c in cuts:
        heads.setdefault(c['chap'], c)
    card0 = [h['cid'] for ch, h in heads.items() if not ch.startswith('つかみ') and h['kind'] == '実写' and h['rights'].startswith('BY-SA')]

    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['cid', 'chap', 'start', 'dur', 'kind', 'code', 'part', 'frame', 'sub', 'motion', 'view', 'look', 'signal', 'rights', 'credit', 'note', 'ga', 'ga_new',
                    'cont', 'src_len', 'rate'])
        for c in cuts:
            w.writerow([c['cid'], c['chap'], '%.2f' % c['start'], '%.2f' % c['dur'], c['kind'], c['code'], c['part'], c['frame'], c['sub'], c['motion'],
                        c['view'], c['look'], c['signal'], c['rights'], c['credit'], c['note'], c['ga'], c['ga_new'], '%.2f' % c['cont'],
                        ('%.2f' % c['src_len']) if c.get('src_len') else '', ('%.3f' % c['rate']) if c.get('rate') else ''])

    L = ['---', 'title: 23本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-10-18', 'tags: [project/jiko-kensho, ep23]', '---', '',
         '# 23本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % n, '',
         '> **生成物＝手で直さない**。作り方＝`python ref/ep23/eizou_build/make_list23.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄・当て方 `eizou_build/assign23.psv`・出どころ `eizou_build/sources23.psv`〈`make_sources23.py` が書く〉・同じ写真の組 `eizou_build/dup23_orb.tsv`）。直すのは入力。',
         '> 秒＝%s（⑤b-1 から＝声＋前 0.35・後 0.50・章の扉 2.0）。🔧＝台本の画の欄から替えたカット。' % tnote + '色味は原本（10-07）。写真は画面いっぱい（10-11）＝例外は BY-SA（高さいっぱいの額装＝10-17）と幅1000未満の公共ヌリ（額装）。動く映像なし（10-17）。見た画像の記録＝`eizou_build/seen23.tsv`。決めと確かめの正本＝Vault `Projects/事故検証-23本目-映像方針-20261018.md`。', '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真・実写（この事故の物） | **%d カット＝%.1f%%**（秒 %.0f＝%.1f%%） | 20%%以上 %s |' % (
             len(photo), ratio * 100, sum(c['dur'] for c in photo), sum(c['dur'] for c in photo) / tot * 100, '✅' if ratio >= PHOTO_LO else '🔴'),
         '| 全面／額装 | 全面 %d（A＝研究院）・額装 %d（%s） | 例外は了承② |' % (len(fulls), len(framed), '・'.join('%s %d' % (k, v) for k, v in Counter(c['frame'] for c in framed).most_common())),
         '| フリー素材（イメージ） | %d カット（20%% に数えない） | 人なし・字なし・生成AIなし |' % len(stock),
         '| 文字だけ | %d カット（%s）・続く最長 %d | できる限り0に近く |' % (len(text), '・'.join(c['cid'] for c in text), mx),
         '| 🔧 台本の画の欄から替えたカット | %d（%s） | 台本は直さない＝⑤b はこの一覧に従う |' % (len(changed), '・'.join(c['cid'] for c in changed)),
         '| 種類 | %s | — |' % '・'.join('%s %d' % (k, v) for k, v in kinds.most_common()),
         '| 図の見た目の型（模式ほか） | %s | 続く図で同じ型を続けない |' % '・'.join('%s %d' % (k, v) for k, v in looks.most_common()),
         '| 静止写真の動き | %s | 寄るだけにしない（10-07） |' % '・'.join('%s %d' % (k, v) for k, v in mc.most_common()),
         '| 扉の地を方眼だけにする章（頭のカットが BY-SA） | %s | card_mix=0（⑤b） |' % ('・'.join(card0) or '—'),
         '| 合計 | %d カット・%s | — |' % (n, fmt_t(tot)), '']
    L += ['### 章ごと', '', '| 章 | カット | 秒 | 実写 | うち全面 | イメージ | 図 | 文字だけ |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = Counter(c['kind'] for c in cs)
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d |' % (
            ch, len(cs), sum(c['dur'] for c in cs), k['実写'], sum(1 for c in cs if c['kind'] == '実写' and c['frame'].startswith('全面')), k['イメージ'],
            len(cs) - k['実写'] - k['イメージ'] - k['文字だけ'], k['文字だけ']))
    L += ['', '## §1 冒頭（c101〜c109）＝実写だけ（写真の動き）', '', '| カット | 秒 | 素材 | 見せ方・動き | 副題 | 語りの頭 |', '|---|---|---|---|---|---|']
    for c in cuts:
        if c['cid'] in OPENING:
            L.append('| %s | %.1f〜%.1f（%.1f） | %s%s | %s・%s | %s | %s |' % (
                c['cid'], c['start'], c['start'] + c['dur'], c['dur'], c['code'], (':' + c['part']) if c['part'] else '', c['frame'], c['motion'], c['sub'], c['first'][:24]))
    L += ['', '- 引き＝c105 の終わり %.1f秒（46秒より前）・最初の見出しの手前 c109 の終わり %.1f秒' % (
        next(c['start'] + c['dur'] for c in cuts if c['cid'] == 'c105'), next(c['start'] + c['dur'] for c in cuts if c['cid'] == 'c109')), '']
    L += ['## §2 図の見た目の型（続く所の見張り）', '', '| 見た目の型 | 回数 | カット |', '|---|---:|---|']
    by_look = defaultdict(list)
    for c in cuts:
        if c['kind'] not in ('実写', 'イメージ', '文字だけ'):
            by_look[c['look'] or c['kind']].append(c['cid'])
    for k, v in sorted(by_look.items(), key=lambda kv: -len(kv[1])):
        L.append('| %s | %d | %s |' % (k, len(v), '・'.join(v)))
    L += ['', '- 見る向きの合図（🔁）＝%s' % ('・'.join('%s（%s）' % (c['cid'], c['signal'].split('（')[0]) for c in cuts if c['signal']) or '—'), '']
    L += ['## §3 章ごと・カットごと', '']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        L += ['### %s（%d カット・%s から）' % (ch, len(cs), fmt_t(cs[0]['start'])), '',
              '| カット | 秒 | 種類 | 素材 | 見せ方 | 副題 | 動き | 見る向き・見た目 | 権利 | 画（替えたカットは新しい画）・備考 |', '|---|---|---|---|---|---|---|---|---|---|']
        for c in cs:
            mat = c['code'] + ((':' + c['part']) if c['part'] else '')
            vl = '・'.join(x for x in (c['view'], c['look']) if x) + ((' ' + c['signal']) if c['signal'] else '')
            if c['kind'] in ('実写', 'イメージ'):
                rem = c['note']
            else:
                rem = (c['ga_new'] + ('｜' + c['note'] if c['note'] else '')) if c['ga_new'] else (c['ga'][:60] + ('…' if len(c['ga']) > 60 else '') + ('｜' + c['note'] if c['note'] else ''))
            L.append('| %s%s | %.1f（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                c['cid'], ' 🔧' if c['changed'] else '', c['start'], c['dur'], c['kind'], mat or '—', c['frame'] or '—', c['sub'] or '—',
                c['motion'] or '—', vl or '—', (c['rights'].split('（')[0] if c['rights'] else '—'), rem.replace('|', '／')))
        L.append('')
    L += ['## §4 素材の一覧（了承②の対象）', '', '| 記号 | 当てたカット | 取り方 | 置き場（git の外） | 大きさ | 権利 | 出典の表記（下書き） | 何 |', '|---|---|---|---|---|---|---|---|']
    used_by = defaultdict(list)
    for c in cuts:
        if c['code']:
            used_by[c['code']].append(c['cid'] + ((':' + c['part']) if c['part'] else ''))
    for code, s in sources.items():
        L.append('| %s | %s | %s | `%s` | %s | %s | %s | %s |' % (code, '・'.join(used_by.get(code, [])) or '（控え）', s['get'], s['file'], s['dims'],
                                                              s['rights'], s['credit'], s['note']))
    L += ['', '## §5 門番', '']
    L += ['- 🔴 E %d 件' % len(E)] + ['  - ' + e for e in E]
    L += ['- ⚠️ %d 件' % len(W)] + ['  - ' + w for w in W]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    print('cuts=%d 実写=%d（%.1f%%）全面=%d 額装=%d イメージ=%d 文字だけ=%d 🔧=%d 合計 %s' % (
        n, len(photo), ratio * 100, len(fulls), len(framed), len(stock), len(text), len(changed), fmt_t(tot)))
    print('種類：', dict(kinds))
    print('見た目：', dict(looks))
    print('動き：', dict(mc))
    print('見る向きの合図：', [c['cid'] for c in cuts if c['signal']])
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
