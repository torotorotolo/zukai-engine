# -*- coding: utf-8 -*-
"""31本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-11-08・チャット5）。30本目 make_list30.py の型を31本目（241カット・事故の回）に合わせた。

  python -P ref/ep31/eizou_build/make_list31.py             一覧を書く（E があれば exit 1）
  python -P ref/ep31/eizou_build/make_list31.py --selftest  陽性・陰性の対照（門番が狙いの門で鳴ることを先に見る）
  python -P ref/ep31/eizou_build/make_list31.py --dump      台本の画の欄を読んだだけの形を出す（差し替えを書く前に見る）
  python -P ref/ep31/eizou_build/make_list31.py --ji        地の書き方の種類と数を出す
  python -P ref/ep31/eizou_build/make_list31.py --narr c214 c326   そのカットの語りだけを出す（見るだけ）

入力：台本 第2版 ref/ep31/daihon_v2.md §4（語りの字数・秒＋画の欄＝当て方の土台・台本は直さない）
      eizou_build/over31.psv（台本の画の欄から替えるカットだけ・11列＝「=」はそのまま）・eizou_build/sources31.psv（出どころ・13列）・eizou_build/decisions31e.md（§5）
出力：ref/ep31/eizou_list31.md（手で直さない）・eizou_build/list31.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E カットの過不足／種類の名／素材の記号が sources31.psv に無い／使わないと決めた点（NG＝P2・P4 は GFDL 1.2 only ほか）を使った
  E 防衛庁記録の外す秒（新聞の紙面・積み込み・参列者の近景＝前後 0.5秒をあける）に区間が触れる／同じ区間を2回／スローが 0.40倍より遅い（§5b-17b）
  E △ の秒（室内の式＝長官の式と見られる・滑走路＝どこの基地か未確認）の副題が、確かめていないこと（長官・辞任・離任・基地の名）を名乗る
  E BY-SA（JA8329・JA8344・62-7702）＝額装でない・動きがある・2カット以上・地に使った／JA8329 は1カットだけ
  E 公的（紙面）＝額装でない・動きがある・出典の行が無い
  E 額装に動き（10-26）／説明カットの地＝PDL1.0・CC BY・CC0・PD・Pexels・国土地理院でない（Google の衛星写真・BY-SA・SDASM を地にしない）／図なのに地が無い
  E 冒頭（c101〜c107）が実写でない／イメージの副題が「イメージ」で始まらない
  E 同型機・保存機の副題に「この機体ではない」か「同じ型」が無い／空中写真の副題に年が無い
  E 同じ写真を3回以上・同じ写真に別の副題・写真と映像と紙面が 20% 未満（§2-1＝紙面と衛星を数える）
  E 書かない名前（src/names_private.txt・src/names_commons.txt）が副題・備考・出どころに／言わない語が副題に
  E 映像の長さ：区間÷速さ＋止め ＜ カットの秒／素材の実の長さをこえる
  ⚠️ 同じ写真を2回・近い／写真の無い画面が5つ以上続く／札以外の図の型が続く／人の印（⑤b で原寸）／△ の秒／映像の区間が未定／止めが長い／等速でない
秒＝台本の ÷365 の見込み（31本目の音はまだ＝⑤a のあと audio/narration.json の実測に替える＝measured）。
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
OUT_MD = os.path.join(EP, 'eizou_list31.md')
OUT_TSV = os.path.join(HERE, 'list31.tsv')
OVER = os.path.join(HERE, 'over31.psv')
SOURCES = os.path.join(HERE, 'sources31.psv')
DECIDE = os.path.join(HERE, 'decisions31e.md')
NAME_FILES = (os.path.join(EP, 'src', 'names_private.txt'), os.path.join(EP, 'src', 'names_commons.txt'))
PUNCT = re.compile(r'[、。，．,.「」『』（）()？！?!…・\s　〈〉：:"“”]')
CUT = re.compile(r'^\*\*(c[0-9a-c]\d\d)\*\*(.*)$')
OPENING = ['c10%d' % i for i in range(1, 8)]
RATE = 365.0
PHOTO_LO = 0.20
GAP_MIN = 8
SLOW_MIN = 0.40                                   # §5b-17b＝0.33〜0.38倍は静止画に替える・0.40倍からはそのまま
# 防衛庁記録『昭和46年』（Commons の CC BY 3.0）＝元の秒（動画の頭から）。手元の切り出し＝元の秒−OFF（materials.md §2・§2b）
FOOT = {'MS': dict(off=1098.5, name='章「雫石事故」', ok=(1118.0, 1238.0)),
        'MK': dict(off=996.2, name='章「航空自衛隊部隊改編」', ok=(1010.0, 1073.0))}
# 外す秒（前後 0.5秒をあける）＝新聞の紙面（報道・犠牲者の顔写真）・包んだ物の積み込み（搬送と見る）・参列者の近景（私人の顔）
EXCLUDE = (('MS', 1114.0, 1118.0, '新聞の紙面＝報道の紙面と犠牲者の顔写真'), ('MS', 1131.2, 1135.2, '積み込み＝搬送と見て外す'),
           ('MS', 1222.5, 1227.6, '参列者の近景＝遺族が含まれうる'))
MARGIN = 0.5
# △＝中身を語りで確かめていない秒（副題は写っているものまで）
TRI = (('MS', 1135.2, 1194.4, '室内の式と送り出し＝長官の離任の式と見られる（語りで未確認）', ('長官', '辞任', '離任', '着任', '大臣')),
       ('MK', 1040.0, 1048.0, '滑走路＝どこの基地か未確認', ('松島', '浜松', '入間', '基地')))
EVENT = ('映像', '写真', '空中')                    # この事故と部隊と同じ型の写真・映像（紙面・衛星・場所を除く）
COUNT20 = EVENT + ('衛星', '公的', '場所')          # §2-1 の写真・映像（紙面 ss.page を数える・衛星写真も実写）＝20% に数える
PICTURE = COUNT20 + ('イメージ',)
FIGS = ('札', '模式', '帯', '年表', '比べ', '並べ', '流れ', '方位', '表', '条文', '言葉')
FIG_FREE = ('札', '模式', '言葉')                  # 型を続けてよい（札の型＝1つの描き手）
JI_OK = ('PDL1.0', 'CC BY 2.0', 'CC BY 2.5', 'CC BY 3.0', 'CC BY 4.0', 'CC0', 'PD', '国土地理院', 'Pexels')
SAY_NOT = ('犯人', '加害者', '胡麻粒', '黒い豆', '心霊', '見舞金', '死亡')
NG = {
    'P2': 'JA8335＝GFDL 1.2 only（許諾の全文を添える決まり＝動画に向かない）・1982年5月の撮影（11-08 に頁で確かめた）',
    'P4': 'JA8340＝GFDL 1.2 only・1980年10月の撮影（11-08 に頁で確かめた）',
    'P8': 'ブルーインパルスの塗装＝訓練機の塗装と違う（② の推奨＝使わない）',
}
KEYS = ['cid', 'kind', 'main', 'ji', 'frame', 'sub', 'motion', 'look', 'ga_new', 'note', 'mark']
SKEYS = ['code', 'type', 'grp', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
KK_MEET = {'内閣委員会': 'N', '運輸委員会': 'U', '決算委員会': 'K', '連合審査会': 'R'}
MOTIONS = ('静止に近い寄り', 'ゆっくり寄る', 'ゆっくり引く', '左へ流す', '右へ流す', '静止')
AERIAL = (('空中 現場今', 'A3'), ('空中 現場', 'A2'), ('空中 松島', 'A1'), ('空中 千歳', 'A4'), ('空中 羽田', 'A5'), ('空中 盛岡', 'A6'), ('空中 雫石町', 'A7'))


def load_psv(path, keys):
    rows, bad = [], []
    if not os.path.exists(path):
        return rows, bad
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


def hms(m, s):
    return int(m) * 60 + float(s)


def foot_code(text):
    return 'MK' if '航空自衛隊部隊改編' in text else 'MS'


def ji_code(desc):
    """台本の「地＝…」→ 地の素材の記号（空中＝A1〜・写真＝P…・記録映像のコマ＝MS=秒・イメージ＝G:…・衛星＝SAT:…）"""
    m = re.search(r'地＝(.*)$', desc)
    if not m:
        return ''
    s = m.group(1)
    for w, c in AERIAL:
        if s.startswith('実写 ' + w):
            return c
    m2 = re.match(r'実写 写真 (P\d+)', s)
    if m2:
        return m2.group(1)
    if s.startswith('実写 映像'):
        t = re.search(r'元 ?(\d+):(\d+(?:\.\d+)?)', s)
        return '%s=%.1f' % (foot_code(s), hms(*t.groups())) if t else foot_code(s)
    m2 = re.match(r'イメージ〈([^〉]*)〉', s)
    if m2:
        return 'G:' + m2.group(1)
    if s.startswith(('実写 衛星', '衛星')):
        return 'SAT:' + re.split(r'[（・）]', s.split('衛星', 1)[1].strip())[0]
    return '?' + s[:20]


def kk_code(text):
    m = re.search(r'国会（(\d{4})-(\d\d)-(\d\d) (参議院|衆議院) ?([^の（・]*?)の会議録', text)
    if not m:
        return '?国会'
    y, mo, d, house, meet = m.groups()
    return 'KK%s%s%s%s%s' % (y, mo, d, 'S' if house == '参議院' else 'H', KK_MEET.get(meet.strip(), '?'))


def parse_ga(cid, ga):
    """台本の画の欄 1つ → 当て方の土台（kind・main・ji・frame・sub・motion）"""
    a = dict(cid=cid, kind='', main='', ji='', frame='—', sub='', motion='', look='', ga_new='', note='', mark='')
    m = re.match(r'^(実写|イメージ|図)\s*(.*)$', ga, re.S)
    if not m:
        a['kind'] = '?'
        return a
    head, rest = m.group(1), m.group(2)
    inner = re.search(r'（(.*)）', rest, re.S)
    desc = inner.group(1) if inner else rest
    sub = re.search(r'副題「([^」]*)」', desc)
    a['sub'] = sub.group(1) if sub else ''
    if head == 'イメージ':
        a['kind'], a['main'], a['frame'] = 'イメージ', 'X' + cid[1:], '全面'
        what = re.sub(r'^フリー素材(の映像)?＝', '', desc).split('・')[0]
        a['sub'] = 'イメージ：' + what
        a['motion'] = '映像' if 'フリー素材の映像' in desc else 'ゆっくり寄る'
        return a
    if head == '図':
        a['kind'] = rest.split('（')[0].strip()
        a['ji'] = ji_code(desc)
        a['sub'] = a['sub'] or re.sub(r'・?地＝.*$', '', desc).strip('・ ')[:60]
        return a
    tok = rest.split('（')[0].split()
    k = tok[0] if tok else ''
    a['kind'] = k
    if k == '映像':
        a['main'] = foot_code(rest)
        a['frame'] = '額装（高さいっぱい）'
        wins = re.findall(r'元 ?(\d+):(\d+(?:\.\d+)?)(?:ごろ)?〜(\d+):(\d+(?:\.\d+)?)(?:ごろ)?', rest)
        a['motion'] = '映像 ' + '＋'.join('%.2f〜%.2f秒' % (hms(w[0], w[1]), hms(w[2], w[3])) for w in wins) if wins else '映像'
        if rest.lstrip().startswith('映像 防衛記録') and '△' in rest:
            a['mark'] = '△'
    elif k == '写真':
        num = re.search(r'P(\d+)', rest.split('（')[0])
        a['main'] = 'P' + num.group(1) if num else '?P'
        a['frame'] = '額装（高さいっぱい）' if '額装' in desc else '全面'
        a['motion'] = '静止' if a['frame'].startswith('額装') else next((w for w in MOTIONS if w in desc), 'ゆっくり寄る')
    elif k == '空中':
        name = ' '.join(tok[:2])
        a['main'] = next((c for w, c in AERIAL if name.startswith(w) and ' '.join(tok[:2]) == w), '?' + name)
        a['frame'] = '全面'
        a['motion'] = next((w for w in MOTIONS if w in desc), 'ゆっくり寄る')
    elif k == '衛星':
        a['main'] = 'SAT:' + ' '.join(tok[1:])
        a['frame'] = '額装（衛星）'
        a['motion'] = '静止'
    elif k == '公的':
        name = ' '.join(tok[1:])
        if name.startswith('国会'):
            a['main'] = kk_code(rest)
        elif name.startswith('判決'):
            a['main'] = 'JS'
        elif name.startswith('白書'):
            a['main'] = 'W47-1' if '「1 航空事故の発生状況」' in rest else 'W47-2'
        elif name.startswith('法律'):
            a['main'] = 'LAW58'
        elif name.startswith('記者発表'):
            a['main'] = 'MLIT2002'
        else:
            a['main'] = '?' + name
        a['frame'] = '額装（高さいっぱい）'
        a['motion'] = '静止'
    return a


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
            parts = m.group(2).split(' ／ ')
            cur = dict(cid=m.group(1), chap=chap, lines=[], ga=parts[1].strip() if len(parts) > 1 else '', fixed='🔧' in parts[0])
            cuts.append(cur)
        elif cur and ln.startswith('> '):
            x = ln[2:].strip()
            cur['lines'].append(x[2:].strip() if x.startswith('Q:') else x)
    t = 0.0
    for c in cuts:
        n = len(PUNCT.sub('', ''.join(c['lines'])))
        c['chars'], c['start'], c['sec'] = n, t, n * 60 / RATE
        c['cont'] = c['sec']
        c['head'] = ''.join(c['lines'])[:20]
        t += c['sec']
    return cuts


def base(code):
    return (code or '').split('=')[0].strip()


def words(paths):
    out = []
    for path in paths:
        if os.path.exists(path):
            out += [w.strip() for w in open(path, encoding='utf-8') if w.strip() and not w.startswith('#')]
    return out


def assemble(cuts, over):
    A = {c['cid']: parse_ga(c['cid'], c['ga']) for c in cuts}
    for a in A.values():
        # 札の型＝画の欄に「札」とある模式（見出し＋札1〜4枚＋矢印0〜2本＝描き手1つ・30本目 §5-4 の型）。ほかの模式は1枚ずつ描く
        if a['kind'] == '模式' and '札' in a['sub']:
            a['kind'] = '札'
    bad = []
    for o in over:
        a = A.get(o['cid'])
        if a is None:
            bad.append('%s 台本に無いカット（差し替えだけある）' % o['cid'])
            continue
        for k in KEYS[1:]:
            if o[k] != '=':
                a[k] = o[k]
    return A, bad


def windows(motion):
    """「映像 1118.50〜1121.00秒」→ [(1118.5, 1121.0)]（元の秒）。区間を書いていなければ空"""
    return [(float(a), float(b)) for a, b in re.findall(r'([\d.]+)〜([\d.]+)秒', motion or '')]


def video_opts(motion):
    """動きの欄の止めと速さ「（＋止め 1.0秒）（0.8倍速）」→ (止め, 速さ)"""
    h = re.search(r'＋止め\s*([\d.]+)秒', motion or '')
    r = re.search(r'（([\d.]+)倍速）', motion or '')
    return float(h.group(1)) if h else 0.0, float(r.group(1)) if r else 1.0


def measured(cuts, narr=NARR):
    """⑤a のあと：秒を audio/narration.json の実測に（30本目 make_list30.measured の型）。いまは31本目の音が無い＝÷365 の見込み"""
    if not os.path.exists(narr):
        return '÷365 の見込み（narration.json が無い）'
    dur = json.load(open(narr, encoding='utf-8')).get('durations', {})
    if [c['cid'] for c in cuts] != [k for k in dur if k != 'ed01']:
        return '÷365 の見込み（narration.json は31本目の台本と合わない＝音は ⑤a のあと）'
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    import check_script as CSC
    t, prev = 0.0, None
    for c in cuts:
        key = CSC.door_key(c['cid'], slug='ep31')
        c['card'] = CSC.CARD_SEC if (prev is not None and key != prev) else 0.0
        prev = key
        c['start'] = t
        c['cont'] = dur[c['cid']] + CSC.LEAD + CSC.TAIL
        c['sec'] = c['cont'] + c['card']
        t += c['sec']
    return 'audio/narration.json の実測'


def media_len(path):
    p = os.path.join(EP, path or '')
    if not path or not os.path.isfile(p):
        return None
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def gate_video(cuts, A, S, E, W, length=media_len):
    """映像の長さ・外す秒・△・速さの門番。動きの欄が「映像」で始まるカット（防衛庁記録 MS・MK・イメージ＝Pexels）"""
    for c in cuts:
        a = A.get(c['cid'])
        if not a or not a['motion'].startswith('映像'):
            continue
        cid, need, code = c['cid'], c.get('cont', c['sec']), base(a['main'])
        win = windows(a['motion'])
        if not win:
            W.append('%s 映像の区間が未定（%s・要る秒 %.2f）' % (cid, code, need))
            continue
        hold, rate = video_opts(a['motion'])
        span = sum(w[1] - w[0] for w in win) / rate
        if span + hold + 0.005 < need:
            E.append('%s 映像の区間 %.2f秒（%.2f倍速）＋止め %.2f秒＝%.2f秒がカットの %.2f秒に足りない' % (cid, sum(w[1] - w[0] for w in win), rate, hold, span + hold, need))
        if rate < SLOW_MIN - 1e-9:
            E.append('%s スローが %.2f倍＝0.40倍より遅い（§5b-17b＝0.33〜0.38倍は静止画に替える）' % (cid, rate))
        if hold > span / 2:
            W.append('%s 止め %.2f秒が区間 %.2f秒の半分をこえる' % (cid, hold, span))
        if rate != 1.0:
            W.append('%s 映像が等速でない（%.2f倍速）' % (cid, rate))
        if code in FOOT:
            lo, hi = FOOT[code]['ok']
            for s, e in win:
                if s < lo - 1e-6 or e > hi + 1e-6:
                    E.append('%s %s の区間 %.2f〜%.2f が使う章の外（%.1f〜%.1f）' % (cid, FOOT[code]['name'], s, e, lo, hi))
                for fc, xa, xb, why in EXCLUDE:
                    if fc == code and min(e, xb + MARGIN) - max(s, xa - MARGIN) > 1e-6:
                        E.append('%s 区間 %.2f〜%.2f が外す秒 %.1f〜%.1f（前後 0.5秒）に触れる＝%s' % (cid, s, e, xa, xb, why))
                for tc, ta, tb, why, claim in TRI:
                    if tc == code and min(e, tb) - max(s, ta) > 1e-6:
                        W.append('%s △ の秒 %.1f〜%.1f＝%s' % (cid, ta, tb, why))
                        bad = [w for w in claim if w in a['sub']]
                        if bad:
                            E.append('%s △ の秒の副題が確かめていないことを名乗る（%s）' % (cid, '・'.join(bad)))
            real = length(S[code]['file']) if code in S else None
            if real is None:
                W.append('%s 素材 %s の実の長さを測れない（手元に無い）' % (cid, code))
            elif max(w[1] for w in win) - FOOT[code]['off'] > real + 0.05:
                E.append('%s 映像の区間の尻が素材 %s の実の長さ %.2f秒をこえる' % (cid, code, real))


def stock_rows(A, S):
    """台本のイメージ（X…）と地のイメージ（G:…）は素材の表に1行ずつ足す＝⑤b で Pexels を1本ずつ探す"""
    for cid, a in A.items():
        if a['kind'] == 'イメージ' and base(a['main']) not in S:
            S[base(a['main'])] = dict(zip(SKEYS, [base(a['main']), 'stock', 'stock', a['sub'], '⑤b で Pexels を1本ずつ（原寸で見る）', '—', 'Pexels', 'Pexels のライセンス＝頁を credits に', 'イメージ（Pexels）', '現在', 'なし（顔・ナンバー・店の字なし）', '', '']))
        j = base(a['ji'])
        if j.startswith('G:') and j not in S:
            S[j] = dict(zip(SKEYS, [j, 'stock', 'ground', j[2:], '⑤b で Pexels を1本（地だけ・暗くする）', '—', 'Pexels', 'Pexels のライセンス＝頁を credits に', '地の写真：イメージ（Pexels）', '現在', 'なし（顔・ナンバー・店の字なし）', '', '']))


def gates(cuts, A, S, name_list=()):
    E, W = [], []
    order = [c['cid'] for c in cuts]
    use, subs, spans = defaultdict(list), defaultdict(set), []
    for cid in order:
        a = A[cid]
        k, code, ji = a['kind'], base(a['main']), base(a['ji'])
        s = S.get(code)
        if k not in PICTURE and k not in FIGS:
            E.append('%s 種類「%s」が決まりの名に無い' % (cid, k))
        if k in PICTURE:
            if not code:
                E.append('%s %s なのに素材の記号が無い' % (cid, k))
            elif not s:
                E.append('%s 素材 %s が sources31.psv に無い' % (cid, code))
        for c2 in (code, ji):
            if c2 in NG:
                E.append('%s 使わないと決めた点 %s を使った（%s）' % (cid, c2, NG[c2]))
        frame, motion = a['frame'], a['motion']
        if s and 'SA' in s['rights'] and (not frame.startswith('額装') or motion != '静止'):
            E.append('%s BY-SA の写真 %s は額装・静止（%s・%s）' % (cid, code, frame, motion))
        if k == '公的' and (not frame.startswith('額装') or motion != '静止'):
            E.append('%s 公的な機関の頁は額装・静止（%s・%s）' % (cid, frame, motion))
        if k == '公的' and s and not s['credit']:
            E.append('%s 公的な機関の頁の出典の行が無い' % cid)
        if frame.startswith('額装') and k != '映像' and motion != '静止':
            E.append('%s 額装に動き（%s）＝額装は静止' % (cid, motion))
        if k == 'イメージ' and not a['sub'].startswith('イメージ'):
            E.append('%s イメージの副題が「イメージ」で始まらない' % cid)
        if s and s['grp'] == 'same-type' and not any(w in a['sub'] for w in ('この機体ではない', '同じ型')):
            E.append('%s 同型機・保存機 %s の副題に「この機体ではない」か「同じ型」が無い（%s）' % (cid, code, a['sub']))
        if k == '空中' and not re.search(r'\d{4}', a['sub']):
            if '最新' in a['sub']:
                W.append('%s 最新の空中写真の撮影年が副題にまだ無い（⑤b で地理院の撮影の記録から）' % cid)
            else:
                E.append('%s 空中写真の副題に年が無い（%s）' % (cid, a['sub']))
        for w in SAY_NOT:
            if w in a['sub']:
                E.append('%s 言わない語「%s」が副題に' % (cid, w))
        if k in FIGS:
            if not ji:
                E.append('%s 図（%s）なのに地の写真が無い＝文字だけの画面' % (cid, k))
            else:
                sj = S.get(ji)
                if ji.startswith('SAT'):
                    E.append('%s Google の衛星写真を地にした（暗くすると見た目を変える＝決まりと当たる）' % cid)
                elif not sj:
                    E.append('%s 地 %s が sources31.psv に無い' % (cid, ji))
                elif sj['rights'] not in JI_OK:
                    E.append('%s 地 %s が地に使える権利でない（%s）' % (cid, ji, sj['rights']))
        if cid in OPENING and k not in COUNT20:
            E.append('%s 冒頭は実写だけ（%s）' % (cid, k))
        if k == '映像':
            spans += [(cid, code, w) for w in windows(motion)]
        for fld in ('sub', 'note', 'ga_new'):
            for nm in name_list:
                if nm and nm in a[fld]:
                    E.append('%s 書かない名前が %s の欄に' % (cid, fld))
        if k in COUNT20 and s:
            use[code].append(cid)
            subs[code].add(a['sub'])
            if s['people'] and not s['people'].startswith(('なし', '—')):
                W.append('%s %s 人＝%s' % (cid, code, s['people']))
    for code, s in S.items():
        for fld in ('title', 'credit', 'note'):
            for nm in name_list:
                if nm and nm in s[fld]:
                    E.append('素材 %s の %s の欄に書かない名前' % (code, fld))
    spans.sort(key=lambda x: (x[1], x[2][0]))
    for (c1, f1, s1), (c2, f2, s2) in zip(spans, spans[1:]):
        if f1 == f2 and s2[0] < s1[1] - 0.05:
            E.append('映像の区間が重なる（同じ秒を2回）: %s %.2f〜%.2f と %s %.2f〜%.2f' % (c1, s1[0], s1[1], c2, s2[0], s2[1]))
    for code, cids in use.items():
        s = S[code]
        if 'SA' in s['rights'] and len(cids) > 1:
            E.append('BY-SA の写真 %s を %d カット（1点1カット）: %s' % (code, len(cids), ' '.join(cids)))
        if code == 'P1' and len(cids) > 1:
            E.append('事故機 JA8329 の写真は1カットだけ: %s' % ' '.join(cids))
        if s['type'].startswith(('stock', 'public-page', 'google')) or code in FOOT:
            continue
        if len(cids) >= 3:
            E.append('同じ写真 %s を %d 回: %s' % (code, len(cids), ' '.join(cids)))
        elif len(cids) == 2:
            gap = abs(order.index(cids[1]) - order.index(cids[0]))
            W.append('同じ写真 %s を2回: %s%s' % (code, ' '.join(cids), '（%dカット差＝近い）' % gap if gap < GAP_MIN else ''))
        if len(subs[code]) > 1:
            E.append('同じ写真 %s に別の副題: %s' % (code, ' ／ '.join(sorted(subs[code]))))
    for cid in order:
        j = base(A[cid]['ji'])
        sj = S.get(j)
        if sj and 'SA' in sj['rights']:
            E.append('%s BY-SA の写真 %s を地にした（額装・無加工だけ）' % (cid, j))
    n20 = sum(1 for cid in order if A[cid]['kind'] in COUNT20)
    if order and n20 / len(order) < PHOTO_LO:
        E.append('写真・映像・紙面が %d／%d＝%.1f%%（20%% 以上）' % (n20, len(order), 100.0 * n20 / len(order)))
    seq = [A[c] for c in order]
    for i in range(1, len(order)):
        k0, k1 = seq[i - 1]['kind'], seq[i]['kind']
        if k0 in FIGS and k0 == k1 and k0 not in FIG_FREE:
            W.append('図の型「%s」が続く: %s → %s' % (k1, order[i - 1], order[i]))
    gap = []
    for cid in order + ['_end']:
        k = A[cid]['kind'] if cid != '_end' else ''
        if cid != '_end' and k not in PICTURE:
            gap.append(cid)
        else:
            if len(gap) >= 5:
                W.append('写真の無い画面が %d つ続く: %s〜%s' % (len(gap), gap[0], gap[-1]))
            gap = []
    return E, W


def fmt(t):
    return '%d:%04.1f' % (int(t // 60), t % 60)


def chap_rows(cuts, A):
    rows, cur = [], None
    for c in cuts:
        if c['chap'] != (cur or {}).get('chap'):
            cur = dict(chap=c['chap'], n=0, real=0, img=0, fig=0)
            rows.append(cur)
        k = A[c['cid']]['kind']
        cur['n'] += 1
        cur['real'] += k in COUNT20
        cur['img'] += k == 'イメージ'
        cur['fig'] += k in FIGS
    return rows


def build(cuts, A, S, E, W, tnote='÷365 の見込み'):
    order = [c['cid'] for c in cuts]
    total = sum(c['sec'] for c in cuts)
    kinds = Counter(A[c]['kind'] for c in order)
    n20 = sum(1 for c in order if A[c]['kind'] in COUNT20)
    n_event = sum(1 for c in order if A[c]['kind'] in EVENT)
    sec20 = sum(c['sec'] for c in cuts if A[c['cid']]['kind'] in COUNT20)
    figs = [c for c in order if A[c]['kind'] in FIGS]
    fixed = sum(1 for c in order if A[c]['ga_new'].startswith('🔧'))
    frames = Counter(A[c]['frame'] for c in order if A[c]['kind'] in PICTURE)
    motions = Counter(A[c]['motion'].split(' ')[0] for c in order if A[c]['kind'] in PICTURE)
    use, ji_use = defaultdict(list), defaultdict(list)
    for c in order:
        a = A[c]
        if a['kind'] in COUNT20:
            use[base(a['main'])].append(c)
        if a['ji']:
            ji_use[base(a['ji'])].append(c)
    L = ['---', 'title: 31本目 場面ごとの映像・写真の一覧（機械で組む）', 'created: 2026-11-08', 'tags: [project/jiko-kensho, ep31]', '---', '',
         '# 31本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % len(order), '',
         '> **機械で組む一覧＝手で直さない**。作り方＝`python -P ref/ep31/eizou_build/make_list31.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄＝土台・差し替え `eizou_build/over31.psv`・出どころ `eizou_build/sources31.psv`・決め `eizou_build/decisions31e.md`）。直すのは入力。',
         '> 秒＝%s（カットの頭・カッコはカットの秒）。🔧＝台本の画の欄から替えたカット' % tnote +
         '（⑤b はこの一覧に従う・台本は直さない）。色味は原本（10-07）・写真は画面いっぱい（10-11）・全面にできない点（BY-SA・4:3 の記録映像・縦長）は**高さいっぱいの額＋地は同じ絵のぼかし**（10-30）・額装はどれも静止（10-26）・衛星写真の額の地は方眼のまま（11-05）。説明カットの地＝写真を暗くするだけ・静止（§5b-117）。見た画像の記録＝`src/seen_log.tsv`（映像方針の印）。🔴 撮影者の個人名はここに書かない（`{作者}`＝git の外の `src/credits_private.tsv` から ⑤b で差し込む）。',
         '', '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真・映像・紙面（§2-1 で数える） | **%d カット＝%.1f%%**（映像 %d・写真 %d・空中 %d・衛星 %d・紙面 %d・場所 %d・秒 %.0f＝%.1f%%） | 20%%以上 ✅ |' % (
             n20, 100.0 * n20 / len(order), kinds['映像'], kinds['写真'], kinds['空中'], kinds['衛星'], kinds['公的'], kinds['場所'], sec20, 100.0 * sec20 / total),
         '| そのうち事故・部隊・同じ型の写真と映像（紙面・衛星・場所を除く） | %d カット＝%.1f%% | 参考（30本目の「この事件の写真と映像」と同じ物差し） |' % (n_event, 100.0 * n_event / len(order)),
         '| フリー素材（イメージ） | %d カット（20%% に数えない・⑤b で1本ずつ探す） | 人の顔・ナンバー・店の名前・読める画面の字なし・AI で作った絵なし・「イメージ」と出す |' % kinds['イメージ'],
         '| 図 | %d カット（札 %d・模式 %d・ほか %d＝地はすべて写真） | 札の型は描き手1つ（§5）・地は暗くするだけ・動かさない |' % (
             len(figs), kinds['札'], kinds['模式'], len(figs) - kinds['札'] - kinds['模式']),
         '| 見せ方（写真・映像・紙面・イメージ） | %s | 額装は静止 |' % '・'.join('%s %d' % kv for kv in frames.most_common()),
         '| 動き | %s | 全面は寄る／流す |' % '・'.join('%s %d' % kv for kv in motions.most_common()),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % fixed,
         '| 種類 | %s | — |' % '・'.join('%s %d' % kv for kv in kinds.most_common()),
         '| 合計 | %d カット・%s（%s・ed01 を除く） | — |' % (len(order), fmt(total), tnote), '',
         '### 章ごとの写真・映像・紙面（§2-1 は章ごとを見ない＝参考・20%% 未満の章に印）', '', '| 章 | カット | 写真・映像・紙面 | 割合 | イメージ | 図 |', '|---|---:|---:|---:|---:|---:|']
    for r in chap_rows(cuts, A):
        p = 100.0 * r['real'] / r['n']
        L.append('| %s | %d | %d | %s%.0f%% | %d | %d |' % (r['chap'], r['n'], r['real'], '⚠️ ' if p < 20 else '', p, r['img'], r['fig']))
    L += ['', '### 写真の使い回し（全面・額装で2回以上＝地は数えない・紙面と記録映像は別の頁と秒）', '']
    rep = [(k, v) for k, v in use.items() if len(v) >= 2 and k not in FOOT and not S.get(k, {}).get('type', '').startswith(('public-page', 'google', 'stock'))]
    L += ['- %s（%s）＝%s' % (k, S[k]['title'] if k in S else '?', ' '.join(v)) for k, v in sorted(rep)] or ['- なし']
    L += ['', '### 地に使った写真（説明カットの背景＝暗くするだけ）', '']
    L += ['- %s（%s）＝%d カット：%s' % (k, S[k]['title'][:40] if k in S else '?', len(v), ' '.join(v)) for k, v in sorted(ji_use.items(), key=lambda kv: -len(kv[1]))]
    L += ['', '## §1 冒頭（c101〜c107）＝実写だけ（最初に設計した）', '', '| カット | 秒 | 語りの頭 | 画 |', '|---|---|---|---|']
    byid = {c['cid']: c for c in cuts}
    for cid in OPENING:
        c, a = byid[cid], A[cid]
        L.append('| %s | %s〜%s | %s | %s %s＝%s（%s） |' % (cid, fmt(c['start']), fmt(c['start'] + c['sec']), c['head'], a['kind'], a['main'], a['sub'], a['motion']))
    L += ['', '## §2 章ごと・カットごと', '']
    chap = None
    for c in cuts:
        a = A[c['cid']]
        if c['chap'] != chap:
            chap = c['chap']
            L += ['', '### ' + chap, '', '| カット | 秒 | 語りの頭 | 種類 | 素材 | 地 | 見せ方 | 副題・札 | 動き | 🔧 | 備考 |', '|---|---|---|---|---|---|---|---|---|---|---|']
        L.append('| %s | %s（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            c['cid'], fmt(c['start']), c['sec'], c['head'], a['kind'], a['main'] or '—', a['ji'] or '—', a['frame'] or '—',
            a['sub'], a['motion'] or '—', a['ga_new'] or '—', (a['note'] + (' ［%s］' % a['mark'] if a['mark'] else '')) or '—'))
    L += ['', '## §3 素材の一覧（出どころ・権利・取得＝了承②の対象）', '',
          '| 記号 | 種類 | 群 | 見て確かめた中身 | 取り方 | 幅×高 | 権利 | 根拠 | 画面の出典の行 | 時代 | 人 | ファイル | 使うカット | 備考 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for code, s in S.items():
        cs = [c for c in order if base(A[c]['main']) == code or base(A[c]['ji']) == code]
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            code, s['type'], s['grp'], s['title'], s['get'], s['dims'], s['rights'], s['basis'], s['credit'], s['era'],
            s['people'], s['file'] or '—', ' '.join(cs) or '（使わない）', s['note'] or '—'))
    L += ['', '## §4 門番', '', '- E %d 件' % len(E)] + ['  - 🔴 ' + x for x in E] + ['- ⚠️ %d 件' % len(W)] + ['  - ⚠️ ' + x for x in W]
    L += ['', '## §5 映像方針で決めたこと', '']
    if os.path.exists(DECIDE):
        L += [ln.rstrip('\n') for ln in open(DECIDE, encoding='utf-8')]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        f.write('cid\tchap\tstart\tsec\tkind\tmain\tji\tframe\tsub\tmotion\tfixed\tmark\tcard\tcont\n')      # 列の名は list30.tsv と同じ
        for c in cuts:
            a = A[c['cid']]
            f.write('%s\t%s\t%.2f\t%.2f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.2f\t%.2f\n' % (c['cid'], c['chap'], c['start'], c['sec'], a['kind'], a['main'], a['ji'], a['frame'], a['sub'], a['motion'], '🔧' if a['ga_new'].startswith('🔧') else '', a['mark'], c.get('card', 0.0), c.get('cont', c['sec'])))
    return n20, len(order)


def selftest():
    def cut(cid, sec=1.0):
        return dict(cid=cid, chap='章', lines=['あ'], chars=1, start=0.0, sec=sec, cont=sec, head='あ', ga='')
    row = lambda code, typ, rights, credit='出典', grp='', people='なし': dict(zip(SKEYS, [code, typ, grp, '', '', '', rights, '', credit, '', people, '', '']))
    S = {'A1': row('A1', 'public-photo', 'PDL1.0'), 'P1': row('P1', 'commons-photo', 'CC BY-SA 4.0', grp='accident'),
         'P3': row('P3', 'commons-photo', 'CC BY-SA 4.0', grp='same-type'), 'P5': row('P5', 'commons-photo', 'SDASM（著作権の制限は知られていない）', grp='same-type'),
         'P6': row('P6', 'commons-photo', 'PD', grp='same-type'), 'SAT:x': row('SAT:x', 'google', 'Google'),
         'MS': row('MS', 'commons-video', 'CC BY 3.0'), 'MK': row('MK', 'commons-video', 'CC BY 3.0'), 'JS': row('JS', 'public-page', '著作権法13条')}
    ok = dict(kind='札', main='', ji='A1', frame='—', sub='札', motion='', look='', ga_new='', note='', mark='')
    aer = dict(kind='空中', main='A1', ji='', frame='全面', sub='松島基地〈1974〜78年〉', motion='ゆっくり寄る', look='', ga_new='', note='', mark='')
    sat = dict(aer, kind='衛星', main='SAT:x', frame='額装（衛星）', sub='衛星', motion='静止')

    def setup(extra):
        cuts = [cut(c) for c in OPENING] + [cut(c) for c in ('c201', 'c202')] + [cut(c) for c in extra if c not in OPENING]
        A = {c['cid']: dict(sat, cid=c['cid']) for c in cuts}
        return cuts, A

    def run(cid, r, name=''):
        cuts, A = setup([cid])
        A[cid] = dict(r, cid=cid)
        return gates(cuts, A, S, (name,) if name else ())[0]
    T = [
        ('陰性 札', 'c701', ok, None),
        ('陽性 NG の点 P2', 'c701', dict(aer, kind='写真', main='P2'), '使わないと決めた'),
        ('陽性 地が無い', 'c701', dict(ok, ji=''), '文字だけ'),
        ('陽性 Google を地に', 'c701', dict(ok, ji='SAT:x'), 'Google'),
        ('陽性 BY-SA を地に', 'c701', dict(ok, ji='P3'), 'BY-SA の写真 P3 を地に'),
        ('陽性 SDASM を地に', 'c701', dict(ok, ji='P5'), '地に使える権利'),
        ('陽性 BY-SA を全面', 'c701', dict(aer, kind='写真', main='P3', sub='同じ型の 727〈この機体ではない〉'), 'BY-SA の写真 P3 は額装'),
        ('陽性 同型機の断りなし', 'c701', dict(aer, kind='写真', main='P6', sub='公園の F-86F'), 'この機体ではない'),
        ('陰性 同型機の断りあり', 'c701', dict(aer, kind='写真', main='P6', sub='保存されている同じ型の F-86F〈この機体ではない〉'), None),
        ('陽性 空中に年なし', 'c701', dict(aer, sub='松島基地'), '年が無い'),
        ('陽性 額装に動き', 'c701', dict(aer, kind='写真', main='P6', frame='額装（高さいっぱい）', sub='同じ型'), '額装に動き'),
        ('陽性 冒頭にイメージ', 'c101', dict(aer, kind='イメージ', sub='イメージ：空', main='X101'), '冒頭は実写'),
        ('陽性 イメージの副題', 'c701', dict(aer, kind='イメージ', sub='空', main='X701'), 'イメージの副題'),
        ('陽性 書かない名前', 'c701', dict(ok, note='山田'), '書かない名前'),
        ('陽性 言わない語', 'c701', dict(ok, sub='犯人の機体'), '言わない語'),
        ('陽性 紙面に動き', 'c701', dict(aer, kind='公的', main='JS', frame='全面'), '公的な機関の頁は額装'),
    ]
    bad = 0
    for label, cid, r, want in T:
        E = run(cid, r, name='山田')
        hit = any(want in x for x in E) if want else not E
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E[:3]))
        bad += 0 if hit else 1
    # JA8329 は1カットだけ・BY-SA は1点1カット
    cuts, A = setup(['c701', 'c702'])
    A['c701'] = dict(aer, cid='c701', kind='写真', main='P1', frame='額装（高さいっぱい）', motion='静止', sub='事故機')
    A['c702'] = dict(aer, cid='c702', kind='写真', main='P1', frame='額装（高さいっぱい）', motion='静止', sub='事故機')
    E = gates(cuts, A, S)[0]
    hit = any('JA8329' in x for x in E) and any('1点1カット' in x for x in E)
    print(('OK  ' if hit else 'NG  ') + '陽性 JA8329 を2カット' + ('' if hit else ' → %s' % E[:3]))
    bad += 0 if hit else 1
    # 映像の区間の重なり（同じ秒を2回）
    for label, second, want in (('陽性 映像の区間が重なる', '映像 1120.00〜1123.00秒', True), ('陰性 映像の区間が離れている', '映像 1200.00〜1210.00秒', False)):
        cuts, A = setup(['c702'])
        A['c101'] = dict(aer, cid='c101', kind='映像', main='MS', frame='額装（高さいっぱい）', motion='映像 1118.50〜1121.00秒', sub='事故の現場')
        A['c702'] = dict(aer, cid='c702', kind='映像', main='MS', frame='額装（高さいっぱい）', motion=second, sub='事故の現場')
        E = gates(cuts, A, S)[0]
        hit = any('重なる' in x for x in E) == want
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E[:3]))
        bad += 0 if hit else 1
    # 映像の長さ・外す秒・△・速さ
    for label, code, motion, sub, sec, want in (
            ('陰性 映像の長さ 足りる', 'MS', '映像 1200.00〜1209.00秒', '半旗', 9.0, None),
            ('陰性 0.40倍＋止めで足りる', 'MS', '映像 1118.50〜1121.00秒（0.40倍速）（＋止め 1.35秒）', '事故の現場', 7.6, None),
            ('陽性 映像の長さ 足りない', 'MS', '映像 1200.00〜1205.00秒', '半旗', 9.0, '足りない'),
            ('陽性 スローが遅すぎる', 'MS', '映像 1118.50〜1121.00秒（0.30倍速）', '事故の現場', 8.0, '0.40倍より遅い'),
            ('陽性 新聞の紙面に触れる', 'MS', '映像 1117.80〜1121.00秒（0.40倍速）（＋止め 1.0秒）', '事故の現場', 8.0, '外す秒'),
            ('陽性 積み込みに触れる', 'MS', '映像 1123.80〜1131.00秒', '捜索', 7.0, '外す秒'),
            ('陽性 参列者の近景に触れる', 'MS', '映像 1218.00〜1222.30秒（0.50倍速）', '祭壇', 8.0, '外す秒'),
            ('陽性 △ の式に長官と書く', 'MS', '映像 1135.70〜1144.00秒', '防衛庁長官の離任の式', 8.0, '△ の秒の副題'),
            ('陰性 △ の式を写っている物まで', 'MS', '映像 1135.70〜1144.00秒', '防衛庁の式〈1971年〉', 8.0, None),
            ('陽性 △ の滑走路に基地の名', 'MK', '映像 1040.00〜1048.00秒', '松島基地の滑走路', 8.0, '△ の秒の副題')):
        c1 = dict(cut('c701', sec))
        A1 = {'c701': dict(aer, cid='c701', kind='映像', main=code, frame='額装（高さいっぱい）', motion=motion, sub=sub)}
        E1, W1 = [], []
        gate_video([c1], A1, {code: dict(S[code], file='x.webm')}, E1, W1, length=lambda p: 200.0)
        hit = any(want in x for x in E1) if want else not E1
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E1[:3]))
        bad += 0 if hit else 1
    print('selftest %s' % ('ok' if not bad else 'NG %d' % bad))
    return 1 if bad else 0


def main():
    if '--selftest' in sys.argv:
        return selftest()
    cuts = read_cuts(DAIHON)
    if '--narr' in sys.argv:
        want = set(sys.argv[sys.argv.index('--narr') + 1:])
        for c in cuts:
            if c['cid'] in want:
                print('%s（%s・%.1f秒）: %s' % (c['cid'], c['chap'].split('　')[0], c['sec'], '／'.join(c['lines'])))
        return 0
    over, bad1 = load_psv(OVER, KEYS)
    if '--dump' in sys.argv or '--ji' in sys.argv:
        A, _ = assemble(cuts, [] if '--dump' in sys.argv else over)
        if '--ji' in sys.argv:
            for k, v in Counter(base(A[c['cid']]['ji']) for c in cuts if A[c['cid']]['ji']).most_common():
                print('%3d %s' % (v, k))
            return 0
        for c in cuts:
            a = A[c['cid']]
            print('|'.join([a['cid'], a['kind'], a['main'], a['ji'][:16], a['frame'][:6], a['sub'][:34], a['motion'][:40], a['mark'], c['head'][:18]]))
        return 0
    src, bad2 = load_psv(SOURCES, SKEYS)
    S = {s['code']: s for s in src}
    A, bad3 = assemble(cuts, over)
    stock_rows(A, S)
    tnote = measured(cuts)
    E, W = gates(cuts, A, S, words(NAME_FILES))
    gate_video(cuts, A, S, E, W)
    E = bad1 + bad2 + bad3 + E
    n, m = build(cuts, A, S, E, W, tnote)
    print('秒＝%s／合計 %s' % (tnote, fmt(sum(c['sec'] for c in cuts))))
    print('カット %d／写真・映像・紙面 %d（%.1f%%）／E %d ／⚠️ %d → %s' % (m, n, 100.0 * n / m, len(E), len(W), OUT_MD))
    for x in E[:60]:
        print('E ', x)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
