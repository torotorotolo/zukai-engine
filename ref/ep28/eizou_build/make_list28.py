# -*- coding: utf-8 -*-
"""28本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-11-01・チャット5）。27本目の make_list27.py の型を28本目（会社のシステムが攻撃された事件の回）に替えた。

  python -P ref/ep28/eizou_build/make_list28.py
  python -P ref/ep28/eizou_build/make_list28.py --selftest     （陽性・陰性の対照＝門番が狙いの門で鳴ることを先に見る）

入力：台本 第2版 ref/ep28/daihon_v2.md §4（語りの字数・秒）
      eizou_build/assign28.psv（当て方・11列）・eizou_build/sources28.psv（出どころ・13列）・eizou_build/decisions28.md（§5）＝手で書く入力
出力：ref/ep28/eizou_list28.md（生成物＝手で直さない）・eizou_build/list28.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 写真の種類（実写・引用・公的・イメージ）に素材の記号が無い／記号が sources28.psv に無い／使わないと決めた点（NG）を使った／種類の名が無い
  E 会社の頁と PDF（引用）＝会社の素材でない・額装（引用）でない・動きがある・出典の行（「出典：」・会社の名・日付）が無い・8カットをこえた（承認①の4）
  E 公的な機関の頁（公的）＝公的な機関の素材でない・額装でない・動きがある・出典の行（「出典：」・日付）が無い
  E CC BY-SA の写真＝額装でない・動きがある・2カット以上（無加工・1点1カット＝ルール §5b-52）
  E 額装の写真に動きがある（額装は静止＝10-26）
  E 説明カットの地＝CC BY・CC0・PD の Commons の写真でない／図の型なのに地が無い（文字だけの画面になる＝§5b-117）
  E SNS のカード＝注釈の印・アカウント名なしの印が無い（§B2-9）
  E 副題・札に「犯人」「加害者」「流出」「真相」（「」の中の原文は除く＝§B2-11）／書かない名前（src/names_private.txt・src/names_commons.txt）
  E 冒頭（c101〜c107）が実写か実写を地にした画面でない（イメージを置かない）／イメージの副題が「イメージ」で始まらない・素材が stock でない
  E 同じ写真（全面・額装）を3回以上／同じ写真に別の副題／写真と紙面が 20% 未満／図の型（模式・SNS を除く）を3回以上
  ⚠️ 同じ写真を2回・2回が8カットより近い／同じ群の写真（駐車場・本社など）が3つ続く／続く図で型が同じ／写真の無い画面が5つ以上続く／
     4:3・縦長の写真を全面（切り出しが大きい）／人・ナンバーの印（⑤b で原寸）
  🆕 ⑤b-1：E 映像の区間＋止めがカットの中身（扉を除いた秒）に足りない・素材の実の長さをこえる／⚠️ まだ区間を書いていない映像（要る秒つき）・等速でない・止めが区間の半分をこえる
秒＝audio/narration.json の実測（⑤b-1 から・27本目 measured() の型）。narration.json が28本目の台本と合わないときは ÷365 の見込みのまま。
"""
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
DAIHON = os.path.join(EP, 'daihon_v2.md')
OUT_MD = os.path.join(EP, 'eizou_list28.md')
OUT_TSV = os.path.join(HERE, 'list28.tsv')
ASSIGN = os.path.join(HERE, 'assign28.psv')
SOURCES = os.path.join(HERE, 'sources28.psv')
DECIDE = os.path.join(HERE, 'decisions28.md')
NAME_FILES = [os.path.join(EP, 'src', 'names_private.txt'), os.path.join(EP, 'src', 'names_commons.txt')]
PUNCT = re.compile(r'[、。，．,.「」『』（）()？！?!…・\s　〈〉：:"“”]')
CUT = re.compile(r'^\*\*(c\d{3})\*\*')
OPENING = ['c10%d' % i for i in range(1, 8)]
RATE = 365.0
PHOTO_LO = 0.20
GAP_MIN = 8
QUOTE_MAX = 8
PICTURE = ('実写', '引用', '公的', 'イメージ')
COUNTED = ('実写', '引用', '公的')          # 20% に数える＝この事件に関わる物と場所の写真・会社と機関の紙面
FIGS = ('模式', '流れ', '時計', '並べ', '比べ', '棒', '箱', '札', '暦', '年表', '問答', '条文', '言葉', '式', '窓口', 'SNS')
FIG_FREE = ('模式', 'SNS')                  # 3回以上でもよい型（台本 §0 の数えと同じ）
JI_OK = ('CC BY 2.0', 'CC BY 3.0', 'CC BY 4.0', 'CC0', 'PD')
BAD_WORDS = ('犯人', '加害者', '流出', '真相')
KEYS = ['cid', 'kind', 'main', 'ji', 'frame', 'sub', 'motion', 'look', 'ga_new', 'note', 'mark']
SKEYS = ['code', 'type', 'grp', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
# 使わないと決めた点（見て外した理由・2026-11-01 に 640px の見本帳で見た）＝ assign28.psv で使ったら E
NG = {
    'CM072': '実在の人の免許証（名前と顔を塗った写し）＝使わない（materials §7）',
    'CM077': '実在の人の免許証（大阪・塗った写し）＝使わない',
    'CM083': '実在の人の免許証（塗った写し）＝使わない',
    'CM085': '実在の人の免許証（三重・塗った写し）＝使わない',
    'CM086': '実在の人の免許証（石川・塗った写し）＝使わない',
    'CM099': '見本の名前でも実在の人の顔写真が入っている＝使わない',
    'CM002': 'BY-SA でナンバーの一部が読める（BY-SA はモザイクも翻案＝かけられない）',
    'CM003': 'BY-SA でナンバーの一部が読める',
    'CM004': 'BY-SA でナンバーの一部が読める',
    'CM026': '博多の屋台＝話の対象でない',
    'CM033': '左下に男性の顔・料金の看板の字が多い（地に向かない）',
    'CM042': '歩行者6人ほどの顔',
    'CM043': '手前に男性2人',
}


def load_psv(path, keys):
    rows, bad = [], []
    for i, ln in enumerate(open(path, encoding='utf-8'), 1):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.startswith('#'):
            continue
        p = ln.split('|')
        if p[0] == keys[0]:
            continue
        if len(p) != len(keys):
            bad.append('%s:%d 列の数 %d（%d のはず）: %s' % (os.path.basename(path), i, len(p), len(keys), ln[:60]))
            continue
        rows.append(dict(zip(keys, [x.strip() for x in p])))
    return rows, bad


def read_cuts(path):
    cuts, cur, chap, on = [], None, '', False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        if ln.startswith('### '):
            chap = ln[4:].strip()
            continue
        m = CUT.match(ln)
        if m:
            cur = dict(cid=m.group(1), chap=chap, lines=[])
            cuts.append(cur)
        elif cur and ln.startswith('> '):
            x = ln[2:].strip()
            cur['lines'].append(x[2:].strip() if x.startswith('Q:') else x)
    t = 0.0
    for c in cuts:
        n = len(PUNCT.sub('', ''.join(c['lines'])))
        c['chars'], c['start'], c['sec'] = n, t, n * 60 / RATE
        c['cont'], c['card'] = c['sec'], 0.0
        c['head'] = ''.join(c['lines'])[:22]
        t += c['sec']
    return cuts


def measured(cuts, narr=NARR):
    """🆕 ⑤b-1（11-01）：秒を audio/narration.json の実測に（27本目 make_list27.measured() の型）。28本目の台本と合わないときは ÷365 の見込みのまま。
    start＝扉こみの頭・sec＝扉＋中身・cont＝扉を除いた中身（声＋LEAD＋TAIL＝映像の区間と比べる秒）。扉は check_script.door_key（28本目は INNER_CARDS なし）"""
    if not os.path.exists(narr):
        return '÷365 の見込み（narration.json が無い）'
    dur = json.load(open(narr, encoding='utf-8')).get('durations', {})
    if [c['cid'] for c in cuts] != [k for k in dur if k != 'ed01']:
        return '÷365 の見込み（narration.json は28本目の台本と合わない）'
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    import check_script as CSC
    t, prev = 0.0, None
    for c in cuts:
        key = CSC.door_key(c['cid'], slug='ep28')
        c['card'] = CSC.CARD_SEC if (prev is not None and key != prev) else 0.0
        prev = key
        c['start'] = t
        c['cont'] = dur[c['cid']] + CSC.LEAD + CSC.TAIL
        c['sec'] = c['cont'] + c['card']
        t += c['sec']
    return 'audio/narration.json の実測'


def video_window(motion):
    """「映像 22.7〜29.9秒（＋止め 1.0秒）（0.8倍速）」→ (22.7, 29.9, 1.0, 0.8)。区間を書いていなければ None"""
    m = re.search(r'映像\s*([\d.]+)〜([\d.]+)秒(?:（＋止め\s*([\d.]+)秒）)?(?:（([\d.]+)倍速）)?', motion or '')
    if not m:
        return None
    return float(m.group(1)), float(m.group(2)), float(m.group(3) or 0), float(m.group(4) or 1.0)


def media_len(path):
    """手元の素材（ref/ep28 からの道）の実の長さ（ffprobe）。道が無い・読めないなら None。置き場の欄の注は読まない（拡張子までの頭の道だけ）"""
    m = re.match(r'[\w./\-]+\.(?:mp4|webm|mkv|mov)', path or '')
    p = os.path.join(EP, m.group(0)) if m else ''
    if not p or not os.path.exists(p):
        return None
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def gate_video(cuts, A, S, E, W, length=media_len):
    """🆕 ⑤b-1：映像の長さの門番（23〜27本目 ⑤b-1 の型）。動きの欄が「映像」で始まるカット（28本目はイメージ15＝Pexels）。
    区間（秒）×速さ＋止め ≧ 扉を除いた中身（cont）か・素材の実の長さの内か。区間を書く前は ⚠️（要る秒つき）＝取ったら動きの欄に「映像 a〜b秒」と書く。
    音は全部使わない（-an＝合成の側）。等速が基本。"""
    for c in cuts:
        a = A.get(c['cid'])
        if not a or not a['motion'].startswith('映像'):
            continue
        cid, need, code = c['cid'], c.get('cont', c['sec']), base(a['main'])
        vw = video_window(a['motion'])
        if not vw:
            W.append('%s 映像の区間が未定（%s・要る秒 %.2f）' % (cid, code, need))
            continue
        st, en, hold, rate = vw
        span = (en - st) / rate
        if span + hold + 0.005 < need:
            E.append('%s 映像の区間 %.2f〜%.2f秒（%.2f倍速）＋止め %.2f秒＝%.2f秒が中身 %.2f秒に足りない' % (cid, st, en, rate, hold, span + hold, need))
        if hold > span / 2:
            W.append('%s 止め %.2f秒が区間 %.2f秒の半分をこえる' % (cid, hold, span))
        if rate != 1.0:
            W.append('%s 映像が等速でない（%.2f倍速）' % (cid, rate))
        real = length(S[code]['file']) if code in S else None
        if real is None:
            W.append('%s 素材 %s の実の長さを測れない（手元に無い）' % (cid, code))
        elif en > real + 0.05:
            E.append('%s 映像の区間の尻 %.2f秒が素材 %s の実の長さ %.2f秒をこえる' % (cid, en, code, real))


def base(code):
    return (code or '').split(':')[0].strip()


def names():
    out = []
    for f in NAME_FILES:
        if os.path.exists(f):
            out += [w.strip() for w in open(f, encoding='utf-8') if w.strip() and not w.startswith('#')]
    return out


def gates(cuts, A, S, name_list=()):
    E, W = [], []
    order = [c['cid'] for c in cuts]
    for cid in order:
        if cid not in A:
            E.append('%s 当て方が無い' % cid)
    for cid in A:
        if cid not in order:
            E.append('%s 台本に無いカット（当て方だけある）' % cid)
    use, subs, quotes = defaultdict(list), defaultdict(set), []
    for cid in order:
        a = A.get(cid)
        if not a:
            continue
        k, code, ji = a['kind'], base(a['main']), base(a['ji'])
        s = S.get(code)
        if k not in PICTURE and k not in FIGS:
            E.append('%s 種類「%s」が決まりの名に無い' % (cid, k))
        if k in PICTURE:
            if not code:
                E.append('%s %s なのに素材の記号が無い' % (cid, k))
            elif not s:
                E.append('%s 素材 %s が sources28.psv に無い' % (cid, code))
        for c2 in (code, ji):
            if c2 in NG:
                E.append('%s 使わないと決めた点 %s を使った（%s）' % (cid, c2, NG[c2]))
        frame, motion = a['frame'], a['motion']
        if k == '引用':
            quotes.append(cid)
            if s and not s['type'].startswith('company'):
                E.append('%s 引用なのに会社の素材でない（%s）' % (cid, s['type']))
            if frame != '額装（引用）':
                E.append('%s 会社の頁の引用が額装（引用）でない（%s）' % (cid, frame))
            if motion != '静止':
                E.append('%s 会社の頁の引用に動き（%s）' % (cid, motion))
            cr = s['credit'] if s else ''
            if not (cr.startswith('出典：') and re.search(r'タイムズモビリティ|パーク24', cr) and re.search(r'20\d\d-\d\d-\d\d', cr)):
                E.append('%s 会社の頁の出典の行に「出典：」・会社の名・日付が無い（%s）' % (cid, cr or '空'))
        if k == '公的':
            if s and not s['type'].startswith('public'):
                E.append('%s 公的なのに公的な機関の素材でない（%s）' % (cid, s['type']))
            if not frame.startswith('額装'):
                E.append('%s 公的な機関の頁が額装でない（%s）' % (cid, frame))
            if motion != '静止':
                E.append('%s 公的な機関の頁に動き（%s）' % (cid, motion))
            cr = s['credit'] if s else ''
            if not (cr.startswith('出典：') and re.search(r'20\d\d-\d\d|\d{4}年\d{1,2}月', cr)):
                E.append('%s 公的な機関の出典の行に「出典：」・日付が無い（%s）' % (cid, cr or '空'))
        if s and 'BY-SA' in s['rights'] and k in COUNTED:
            if not frame.startswith('額装'):
                E.append('%s BY-SA の写真 %s が額装でない（%s）' % (cid, code, frame))
            if motion != '静止':
                E.append('%s BY-SA の写真 %s に動き（%s）' % (cid, code, motion))
        if frame.startswith('額装') and motion not in ('静止',):
            E.append('%s 額装に動き（%s）＝額装は静止' % (cid, motion))
        if k == 'イメージ':
            if not a['sub'].startswith('イメージ'):
                E.append('%s イメージの副題が「イメージ」で始まらない' % cid)
            if s and s['type'] != 'stock':
                E.append('%s イメージの素材が stock でない（%s）' % (cid, s['type']))
        if k in FIGS:
            if not ji:
                E.append('%s 図（%s）なのに地の写真が無い＝文字だけの画面' % (cid, k))
            else:
                sj = S.get(ji)
                if not sj:
                    E.append('%s 地 %s が sources28.psv に無い' % (cid, ji))
                elif sj['type'] != 'commons-photo' or sj['rights'] not in JI_OK:
                    E.append('%s 地 %s が CC BY・CC0・PD の Commons の写真でない（%s・%s）' % (cid, ji, sj['type'], sj['rights']))
        elif ji:
            W.append('%s 図でないのに地の欄がある（%s）' % (cid, ji))
        if k == 'SNS' and not ('注釈' in a['mark'] and 'アカウント名なし' in a['mark']):
            E.append('%s SNS のカードに注釈・アカウント名なしの印が無い' % cid)
        outside = re.sub(r'「[^」]*」', '', a['sub'])
        for w in BAD_WORDS:
            if w in outside:
                E.append('%s 副題・札に「%s」（「」の外）' % (cid, w))
        for nm in name_list:
            for fld in ('sub', 'note', 'ga_new'):
                if nm and nm in a[fld]:
                    E.append('%s 書かない名前が %s の欄に' % (cid, fld))
        if cid in OPENING and k not in COUNTED and k not in FIGS:
            E.append('%s 冒頭は実写か実写を地にした画面だけ（%s）' % (cid, k))
        if k in COUNTED and s:
            use[code].append(cid)
            subs[code].add(a['sub'])
            if s['type'] == 'commons-photo' and frame == '全面':
                m = re.match(r'(\d+)x(\d+)', s['dims'])
                if m and int(m.group(1)) / float(m.group(2)) < 1.2:      # 縦長・正方形に近い点だけ（4:3 の上下を切るのは普通の扱い）
                    W.append('%s %s（%s）を全面＝切り出しが大きい（何が残るかを ⑤b で見る）' % (cid, code, s['dims']))
            if s['people'] and not s['people'].startswith(('なし', '—')):
                W.append('%s %s 人・ナンバー＝%s' % (cid, code, s['people']))
    for code, cids in use.items():
        s = S[code]
        if 'BY-SA' in s['rights'] and len(cids) > 1:
            E.append('BY-SA の写真 %s を %d カット（1点1カット）: %s' % (code, len(cids), ' '.join(cids)))
        if len(cids) >= 3:
            E.append('同じ写真 %s を %d 回: %s' % (code, len(cids), ' '.join(cids)))
        elif len(cids) == 2:
            gap = abs(order.index(cids[1]) - order.index(cids[0]))
            W.append('同じ写真 %s を2回: %s%s' % (code, ' '.join(cids), '（%dカット差＝近い）' % gap if gap < GAP_MIN else ''))
        if len(subs[code]) > 1:
            E.append('同じ写真 %s に別の副題: %s' % (code, ' ／ '.join(sorted(subs[code]))))
    for cid in OPENING:
        a = A.get(cid)
        if a and a['kind'] in FIGS and S.get(base(a['ji'])) is None:
            E.append('%s 冒頭の図の地が無い' % cid)
    if len(quotes) > QUOTE_MAX:
        E.append('会社の頁の引用 %d カット（%d まで＝承認①の4）: %s' % (len(quotes), QUOTE_MAX, ' '.join(quotes)))
    n_photo = sum(1 for cid in order if A.get(cid, {}).get('kind') in COUNTED)
    if order and n_photo / len(order) < PHOTO_LO:
        E.append('写真と紙面が %.1f%%（20%% 以上）' % (100.0 * n_photo / len(order)))
    cnt = Counter(A[c]['kind'] for c in order if c in A and A[c]['kind'] in FIGS)
    for t, n in sorted(cnt.items()):
        if t not in FIG_FREE and n > 2:
            E.append('図の型「%s」を %d 回（全編で2回まで）' % (t, n))
    seq = [A.get(c, {}) for c in order]
    for i in range(1, len(order)):
        k0, k1 = seq[i - 1].get('kind'), seq[i].get('kind')
        if k0 in FIGS and k0 == k1:
            W.append('図の型「%s」が続く: %s → %s' % (k1, order[i - 1], order[i]))
    run = []
    for i, cid in enumerate(order + ['_end']):
        a = A.get(cid, {})
        s = S.get(base(a.get('main', '')))
        g = s['grp'] if (s and a.get('kind') in COUNTED) else None
        if g and run and g == run[-1][1]:
            run.append((cid, g))
        else:
            if len(run) >= 3:
                W.append('同じ群「%s」の写真が %d つ続く: %s' % (run[0][1], len(run), ' '.join(x[0] for x in run)))
            run = [(cid, g)] if g else []
    gap = []
    for cid in order + ['_end']:
        k = A.get(cid, {}).get('kind')
        if cid != '_end' and k not in COUNTED:
            gap.append(cid)
        else:
            if len(gap) >= 5:
                W.append('写真の無い画面が %d つ続く: %s〜%s' % (len(gap), gap[0], gap[-1]))
            gap = []
    return E, W


def fmt(t):
    return '%d:%04.1f' % (int(t // 60), t % 60)


def build(cuts, A, S, E, W, tnote='÷365 の見込み'):
    order = [c['cid'] for c in cuts]
    total = sum(c['sec'] for c in cuts)
    kinds = Counter(A[c]['kind'] for c in order if c in A)
    n_cnt = sum(1 for c in order if A.get(c, {}).get('kind') in COUNTED)
    sec_cnt = sum(c['sec'] for c in cuts if A.get(c['cid'], {}).get('kind') in COUNTED)
    frames = Counter(A[c]['frame'] for c in order if c in A and A[c]['kind'] in PICTURE)
    motions = Counter(A[c]['motion'] for c in order if c in A and A[c]['kind'] in PICTURE)
    fixed = sum(1 for c in order if A.get(c, {}).get('ga_new', '').startswith('🔧'))
    figs = [c for c in order if A.get(c, {}).get('kind') in FIGS]
    use, ji_use = defaultdict(list), defaultdict(list)
    for c in order:
        a = A.get(c)
        if not a:
            continue
        if a['kind'] in COUNTED:
            use[base(a['main'])].append(c)
        if a['ji']:
            ji_use[base(a['ji'])].append(c)
    L = ['---', 'title: 28本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-11-01', 'tags: [project/jiko-kensho, ep28]', '---', '',
         '# 28本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % len(order), '',
         '> **生成物＝手で直さない**。作り方＝`python -P ref/ep28/eizou_build/make_list28.py`（入力＝台本 第2版 `daihon_v2.md` §4・当て方 `eizou_build/assign28.psv`・出どころ `eizou_build/sources28.psv`・決め `eizou_build/decisions28.md`）。直すのは入力。',
         '> 秒＝' + tnote + '（扉こみの頭・扉を除いた中身と扉を足した秒）。🔧＝台本の画の欄から替えたカット（⑤b はこの一覧に従う・台本は直さない）。色味は原本（10-07）・写真は画面いっぱい（10-11）・全面にできない点（4:3・縦長の BY-SA と引用・頁）は**高さいっぱいの額＋地は同じ絵のぼかし**（10-30）・額装はどれも静止（10-26）。説明カットの地＝CC BY・CC0・PD の写真を暗くするだけ・静止（§5b-117）。見た画像の記録＝`src/seen_log.tsv`（映像方針の印）。🔴 撮影者の名前はここに書かない（`{作者}`＝git の外の `src/credits_private.tsv` から ⑤b で差し込む）。',
         '', '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| この事件の写真と紙面（Commons の実写＋会社の頁の引用＋公的な機関の頁） | **%d カット＝%.1f%%**（実写 %d・引用 %d・公的 %d・秒 %.0f＝%.1f%%） | 20%%以上 ✅ |' % (
             n_cnt, 100.0 * n_cnt / len(order), kinds['実写'], kinds['引用'], kinds['公的'], sec_cnt, 100.0 * sec_cnt / total),
         '| フリー素材（イメージ） | %d カット（20%% に数えない・⑤b で1本ずつ探す） | 人の顔・ナンバー・店の名前・読める画面の字なし・生成 AI なし・「イメージ」と出す |' % kinds['イメージ'],
         '| 図（模式・型の図・SNS のカード） | %d カット（地＝写真 %d） | 地は CC BY・CC0・PD の写真を暗くするだけ・動かさない |' % (len(figs), sum(1 for c in figs if A[c]['ji'])),
         '| 文字だけ | 0 カット | 0 |',
         '| 見せ方（写真と紙面） | %s | 額装は静止 |' % '・'.join('%s %d' % kv for kv in frames.most_common()),
         '| 写真の動き | %s | 額装と引用・頁は動かさない・全面は寄る／流す |' % '・'.join('%s %d' % kv for kv in motions.most_common()),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % fixed,
         '| 種類 | %s | — |' % '・'.join('%s %d' % kv for kv in kinds.most_common()),
         '| 合計 | %d カット・%s（%s・ed01 を除く） | — |' % (len(order), fmt(total), tnote.split('（')[0]), '',
         '### 写真の使い回し（全面・額装で2回以上＝地は数えない）', '']
    rep = [(k, v) for k, v in use.items() if len(v) >= 2]
    L += ['- %s（%s）＝%s' % (k, S[k]['title'] if k in S else '?', ' '.join(v)) for k, v in sorted(rep)] or ['- なし']
    L += ['', '### 地に使った写真（説明カットの背景＝暗くするだけ）', '']
    L += ['- %s（%s）＝%s' % (k, S[k]['title'] if k in S else '?', ' '.join(v)) for k, v in sorted(ji_use.items())]
    L += ['', '## §1 冒頭（c101〜c107）＝実写と実写を地にした画面だけ（最初に設計した）', '', '| カット | 秒 | 語りの頭 | 画 |', '|---|---|---|---|']
    byid = {c['cid']: c for c in cuts}
    for cid in OPENING:
        c, a = byid.get(cid), A.get(cid)
        if not c or not a:
            continue
        what = a['kind'] + ' ' + (a['main'] or '') + ('（地 %s）' % a['ji'] if a['ji'] else '') + '＝' + a['sub']
        L.append('| %s | %s〜%s | %s | %s |' % (cid, fmt(c['start']), fmt(c['start'] + c['sec']), c['head'], what))
    L += ['', '## §2 章ごと・カットごと', '']
    chap = None
    for c in cuts:
        a = A.get(c['cid'])
        if not a:
            continue
        if c['chap'] != chap:
            chap = c['chap']
            L += ['', '### ' + chap, '', '| カット | 秒 | 語りの頭 | 種類 | 素材 | 地 | 見せ方 | 副題・札 | 動き | 🔧 | 備考 |', '|---|---|---|---|---|---|---|---|---|---|---|']
        L.append('| %s | %s（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            c['cid'], fmt(c['start']), c['sec'], c['head'], a['kind'], a['main'] or '—', a['ji'] or '—', a['frame'] or '—',
            a['sub'], a['motion'] or '—', a['ga_new'] or '—', (a['note'] + (' ［%s］' % a['mark'] if a['mark'] else '')) or '—'))
    L += ['', '## §3 素材の一覧（出どころ・権利・取得＝了承②の対象）', '',
          '| 記号 | 種類 | 群 | 見て確かめた中身 | 取り方 | 幅×高 | 権利 | 根拠 | 画面の出典の行 | 時代 | 人・ナンバー | ファイル | 使うカット | 備考 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for code, s in S.items():
        cs = [c for c in order if A.get(c) and (base(A[c]['main']) == code or base(A[c]['ji']) == code)]
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            code, s['type'], s['grp'], s['title'], s['get'], s['dims'], s['rights'], s['basis'], s['credit'], s['era'],
            s['people'], s['file'] or '—', ' '.join(cs) or '（使わない）', s['note'] or '—'))
    L += ['', '## §4 門番', '', '- E %d 件' % len(E)] + ['  - 🔴 ' + x for x in E] + ['- ⚠️ %d 件' % len(W)] + ['  - ⚠️ ' + x for x in W]
    L += ['', '## §5 映像方針で決めたこと', '']
    if os.path.exists(DECIDE):
        L += [ln.rstrip('\n') for ln in open(DECIDE, encoding='utf-8')]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        # 🆕 ⑤b-1：mark・card・cont を足した（門番 check_ground._sns_cuts が mark＝SNS のカットを読む＝列が無いと止まる・27本目の list27.tsv と同じ名）
        f.write('cid\tchap\tstart\tsec\tkind\tmain\tji\tframe\tsub\tmotion\tfixed\tmark\tcard\tcont\n')
        for c in cuts:
            a = A.get(c['cid'], {})
            f.write('%s\t%s\t%.2f\t%.2f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.2f\t%.2f\n' % (
                c['cid'], c['chap'], c['start'], c['sec'], a.get('kind', ''), a.get('main', ''), a.get('ji', ''), a.get('frame', ''),
                a.get('sub', ''), a.get('motion', ''), '🔧' if a.get('ga_new', '').startswith('🔧') else '',
                'SNS' if a.get('kind') == 'SNS' else a.get('mark', ''), c.get('card', 0.0), c.get('cont', c['sec'])))
    return n_cnt, len(order)


def selftest():
    cuts = [dict(cid='c10%d' % i, chap='つかみ', lines=['あ'], chars=1, start=0.0, sec=1.0, head='あ') for i in range(1, 8)]
    cuts += [dict(cid='c2%02d' % i, chap='第1章', lines=['い'], chars=1, start=0.0, sec=1.0, head='い') for i in range(1, 9)]
    S = {
        'P1': dict(zip(SKEYS, ['P1', 'commons-photo', 'parking', '駐車場', 'commons:CM001', '1920x1080', 'CC BY 3.0', '', '', '2015年', 'なし', '', ''])),
        'P2': dict(zip(SKEYS, ['P2', 'commons-photo', 'parking', '駐車場', 'commons:CM002', '1920x1080', 'CC BY 3.0', '', '', '2015年', 'なし', '', ''])),
        'P3': dict(zip(SKEYS, ['P3', 'commons-photo', 'parking', '駐車場', 'commons:CM003', '1920x1080', 'CC BY 3.0', '', '', '2015年', 'なし', '', ''])),
        'SA': dict(zip(SKEYS, ['SA', 'commons-photo', 'car', '車', 'commons:CM004', '3072x2304', 'CC BY-SA 4.0', '', '', '2015年', 'なし', '', ''])),
        'Q1': dict(zip(SKEYS, ['Q1', 'company-page', 'company', '頁', 'web:x', '—', '引用', '', '出典：タイムズモビリティ 第2報（2026-09-28）', '', 'なし', '', ''])),
        'Q2': dict(zip(SKEYS, ['Q2', 'company-page', 'company', '頁', 'web:x', '—', '引用', '', '会社の頁', '', 'なし', '', ''])),
        'X1': dict(zip(SKEYS, ['X1', 'stock', 'stock', 'イメージ', 'pexels:⑤b', '—', 'Pexels License', '', 'イメージ（Pexels）', '', 'なし', '', ''])),
    }

    def A_(rows):
        return {r[0]: dict(zip(KEYS, r)) for r in rows}
    ok_rows = [['c101', '実写', 'P1', '', '全面', '駐車場〈2015年〉', 'ゆっくり寄る', '', '', '', ''],
               ['c102', '引用', 'Q1', '', '額装（引用）', '会社の知らせ〈第2報〉', '静止', '', '', '', '引用'],
               ['c103', '札', '', 'P1', '—', '3つの数', '—', '', '', '', ''],
               ['c104', '実写', 'P2', '', '全面', '駐車場B〈2015年〉', 'ゆっくり寄る', '', '', '', ''],
               ['c105', '模式', '', 'P2', '—', '会社の説明', '—', '', '', '', ''],
               ['c106', '実写', 'SA', '', '額装（高さいっぱい）', '車〈2015年〉', '静止', '', '', '', ''],
               ['c107', '実写', 'P3', '', '全面', '駐車場C〈2015年〉', '静止', '', '', '', '']]
    ok_rows += [['c2%02d' % i, '模式', '', 'P1', '—', '図%d' % i, '—', '', '', '', ''] for i in range(1, 9)]
    ok_rows[7] = ['c201', 'イメージ', 'X1', '', '全面', 'イメージ：通路', '静止', '', '', '', '']
    ok_rows[8] = ['c202', 'SNS', '', 'P1', '—', '「ハッカーたちが犯人だよね？」', '—', '', '', '', 'SNS注釈・アカウント名なし']
    ok_rows[9] = ['c203', '実写', 'P1', '', '全面', '駐車場〈2015年〉', '静止', '', '', '', '']
    cases = [('陰性：正しい表', ok_rows, None)]

    def mod(i, col, val):
        rows = [list(r) for r in ok_rows]
        rows[i][KEYS.index(col)] = val
        return rows
    cases += [
        ('陽性：冒頭にイメージ', mod(3, 'kind', 'イメージ') and [r if r[0] != 'c104' else ['c104', 'イメージ', 'X1', '', '全面', 'イメージ：通路', '静止', '', '', '', ''] for r in ok_rows], '冒頭は実写'),
        ('陽性：引用が額装でない', mod(1, 'frame', '全面'), '額装（引用）でない'),
        ('陽性：引用の出典の行に会社と日付が無い', [r if r[0] != 'c102' else ['c102', '引用', 'Q2', '', '額装（引用）', '会社の知らせ', '静止', '', '', '', ''] for r in ok_rows], '出典の行に'),
        ('陽性：BY-SA に動き', mod(5, 'motion', 'ゆっくり寄る'), 'BY-SA の写真 SA に動き'),
        ('陽性：地が BY-SA', mod(2, 'ji', 'SA'), 'CC BY・CC0・PD の Commons の写真でない'),
        ('陽性：図に地が無い', mod(4, 'ji', ''), '文字だけの画面'),
        ('陽性：副題に流出', mod(0, 'sub', '流出した駐車場'), '「流出」'),
        ('陽性：SNS の印が無い', mod(8, 'mark', ''), '注釈・アカウント名なしの印が無い'),
        ('陽性：同じ写真に別の副題', mod(9, 'sub', '別の副題'), '別の副題'),
        ('陽性：イメージの副題', mod(7, 'sub', '通路'), '「イメージ」で始まらない'),
        ('陽性：札を3回', [r if r[0] not in ('c204', 'c205') else [r[0], '札', '', 'P1', '—', '札', '—', '', '', '', ''] for r in ok_rows], '図の型「札」を 3 回'),
    ]
    bad = 0
    for name, rows, want in cases:
        E, W = gates(cuts, A_(rows), S)
        if want is None:
            good = not E
        else:
            good = any(want in e for e in E)
        bad += 0 if good else 1
        print('%s %s → E %d%s' % ('OK' if good else 'NG', name, len(E), ('（' + E[0][:50] + '）') if E and not good else ''))
    # 🆕 ⑤b-1：映像の長さの門番（中身 10.00秒・素材の実の長さ 12秒）
    S_v = {'X1': dict(S['X1'], file='stock/x1.mp4')}
    cuts_v = [dict(cid='c301', cont=10.0, sec=12.0)]

    def run_v(motion, length=lambda p: 12.0):
        E_, W_ = [], []
        gate_video(cuts_v, {'c301': dict(zip(KEYS, ['c301', 'イメージ', 'X1', '', '全面', 'イメージ：通路', motion, '', '', '', '']))}, S_v, E_, W_, length)
        return E_, W_
    vcases = [('陰性：区間が中身に足りる', '映像 1.0〜11.0秒', None, None),
              ('陽性：区間が中身に足りない', '映像 1.0〜10.5秒', '足りない', None),
              ('陰性：止めで足りる', '映像 1.0〜10.5秒（＋止め 0.5秒）', None, None),
              ('陽性：素材の実の長さをこえる', '映像 3.0〜13.0秒', '実の長さ', None),
              ('陽性：区間が未定＝⚠️（要る秒つき）', '映像', None, '要る秒 10.00'),
              ('陽性：等速でない＝⚠️', '映像 1.0〜9.0秒（0.8倍速）', None, '等速でない'),
              ('陽性：止めが区間の半分をこえる＝⚠️', '映像 1.0〜7.0秒（＋止め 4.0秒）', None, '半分をこえる')]
    for name, motion, want_e, want_w in vcases:
        E_, W_ = run_v(motion)
        good = (any(want_e in e for e in E_) if want_e else not E_) and (not want_w or any(want_w in w for w in W_))
        bad += 0 if good else 1
        print('%s %s → E %d・⚠️ %d' % ('OK' if good else 'NG', name, len(E_), len(W_)))
    print('SELFTEST %s（%d 件）' % ('PASS' if not bad else 'FAIL', len(cases) + len(vcases)))
    return 1 if bad else 0


def main():
    if '--selftest' in sys.argv:
        return selftest()
    cuts = read_cuts(DAIHON)
    tnote = measured(cuts)
    arows, abad = load_psv(ASSIGN, KEYS)
    srows, sbad = load_psv(SOURCES, SKEYS)
    A = {r['cid']: r for r in arows}
    S = {r['code']: r for r in srows}
    E, W = gates(cuts, A, S, names())
    E = abad + sbad + E
    gate_video(cuts, A, S, E, W)
    n_cnt, n = build(cuts, A, S, E, W, tnote)
    print('秒＝%s・c103 の終わり %.1f・c107 の終わり %.1f・合計 %s' % (
        tnote, sum(c['sec'] for c in cuts if c['cid'] <= 'c103'), sum(c['sec'] for c in cuts if c['cid'] <= 'c107'), fmt(sum(c['sec'] for c in cuts))))
    print('カット %d・写真と紙面 %d（%.1f%%）・E %d・⚠️ %d → %s' % (n, n_cnt, 100.0 * n_cnt / max(n, 1), len(E), len(W), OUT_MD))
    for x in E:
        print('E', x)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
