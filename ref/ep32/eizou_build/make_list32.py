# -*- coding: utf-8 -*-
"""32本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-11-10・チャット5）。31本目 make_list31.py の型を32本目（236カット・USエアウェイズ1549便）に合わせた。

  python -P ref/ep32/eizou_build/make_list32.py             一覧を書く（E があれば exit 1）
  python -P ref/ep32/eizou_build/make_list32.py --selftest  陽性・陰性の対照（門番が狙いの門で鳴ることを先に見る）
  python -P ref/ep32/eizou_build/make_list32.py --dump      台本の画の欄を読んだだけの形を出す（差し替えを書く前に見る）
  python -P ref/ep32/eizou_build/make_list32.py --ji        地の書き方の種類と数を出す
  python -P ref/ep32/eizou_build/make_list32.py --narr c915 ca06   そのカットの語りだけを出す（見るだけ）

入力：台本 第2版 ref/ep32/daihon_v2.md §4（語りの字数・秒＋画の欄＝当て方の土台・台本は直さない）
      eizou_build/over32.psv（台本の画の欄から替えるカットだけ・11列＝「=」はそのまま）・eizou_build/sources32.psv（出どころ・13列）・eizou_build/decisions32e.md（§5）
出力：ref/ep32/eizou_list32.md（手で直さない）・eizou_build/list32.tsv（列の名は list31.tsv と同じ）
門番（E があれば exit 1・⚠️ は止めない）：
  E カットの過不足／種類の名／素材の記号が sources32.psv に無い／使わないと決めた点（NG＝FirstFerry・[10]・[17]・[37]・[71]・[72] ほか）を使った
  E VTS（沿岸警備隊の監視カメラ）＝区間が素材の長さをこえる・同じ秒を2回・速さを変えた（等速だけ）・外す秒（背景のコンコルド）に触れる・副題に焼き込みの時計の時刻
  E BY-SA＝額装でない・動きがある・2カット以上・地に使った
  E 公的（紙面）・調査の写真＝額装でない・動きがある・出典の行が無い
  E 額装に動き（10-26）／説明カットの地＝CC BY・CC0・PD・Pexels でない（🔴 Google の衛星写真は地にしない＝暗くすると見た目を大きく変える〈Geo Guidelines・11-05 の決め〉）／夜の暗い写真を地に（29本目）／図なのに地が無い
  E 冒頭（c101〜c107）が実写でない／イメージの副題が「イメージ」で始まらない
  E 写真の副題の日付・夕方・夜が、確かめた時点（sources の era＝頁の説明か EXIF）と合わない（🔴 32本目で [8]・[7]・[40] が「その日の夕方」と食い違った）
  E 同じ写真を3回以上・同じ写真に別の副題・写真と映像と紙面が 20% 未満（§2-1＝紙面と衛星を数える）
  E 書かない名前（src/names_private.txt・src/names_commons.txt）が副題・備考・出どころに／言わない語が副題に
  E 映像の長さ：区間÷速さ＋止め ＜ カットの秒
  ⚠️ 同じ写真を2回・近い／写真の無い画面が5つ以上続く／図の型「模式」が続く（m32 の W と同じ物差し）／人の印（⑤b で原寸）／△／映像の区間が未定／区間がカメラの動く所に触れる／止めがある
秒＝台本の ÷365 の見込み（32本目の音はまだ＝⑤a のあと audio/narration.json の実測に替える＝measured）。
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
OUT_MD = os.path.join(EP, 'eizou_list32.md')
OUT_TSV = os.path.join(HERE, 'list32.tsv')
OVER = os.path.join(HERE, 'over32.psv')
SOURCES = os.path.join(HERE, 'sources32.psv')
DECIDE = os.path.join(HERE, 'decisions32e.md')
NAME_FILES = (os.path.join(EP, 'src', 'names_private.txt'), os.path.join(EP, 'src', 'names_commons.txt'))
PUNCT = re.compile(r'[、。，．,.「」『』（）()？！?!…・\s　〈〉：:"“”]')
CUT = re.compile(r'^\*\*(c[0-9a-c]\d\d)\*\*(.*)$')
OPENING = ['c10%d' % i for i in range(1, 8)]
RATE = 365.0
PHOTO_LO = 0.20
GAP_MIN = 8
# VTS（沿岸警備隊の監視カメラ＝Commons の4本・PD-USCG・384×288）。len＝ffprobe の長さ・ok＝カメラが落ち着いた区間
# （2026-11-10 映像方針＝隣のコマの灰色の差〈96×72・上下の焼き込みの帯を外す〉の秒ごとの最大で当たりを付け、原寸のコマ 48枚で見た＝src/look/seen_log.tsv）
FOOT = {
    'VC': dict(name='CrashAndRescue', len=487.667, ok=((0, 42), (48, 108), (128, 139), (153, 164), (184, 207), (208, 228), (230, 240),
                                                         (258, 269), (273, 283), (305, 325), (333, 348), (354, 364), (382, 396),
                                                         (414, 427), (450, 462), (464, 474))),
    'V15': dict(name='After15Minutes', len=44.75, ok=((7, 17), (24, 33))),
    'V20': dict(name='After20Minutes', len=150.333, ok=((0, 12), (16, 35), (36, 69), (76, 114), (133, 144))),
}
# 外す秒（前後 0.5秒あける）＝見る人が取り違える絵
# 🔧 ⑤b-2（11-10）：映像方針で見た 415〜427秒（1秒きざみ）を含むショットまるごとに広げた＝原本の全コマの灰色の差で測った切れ目
#    403.0〜403.3（カメラの振り）・427.3〜427.7・438.0（`qa_out/ep32_assets.py shots`）。前は 410〜428（見た秒の前後）＝同じショットの 403〜410・428〜438 にも写りうる
EXCLUDE = (('VC', 403.0, 438.0, '背景の艀の上に別の旅客機（コンコルド＝博物館の展示機と見られる）＝この機体と取り違えられる'),)
MARGIN = 0.5
EVENT = ('映像', '写真', '調査')                    # この事故の写真・映像（紙面・衛星を除く）
COUNT20 = EVENT + ('衛星', '公的')                  # §2-1 の写真・映像（紙面 ss.page を数える・衛星写真も実写）＝20% に数える
PICTURE = COUNT20 + ('イメージ',)
FIGS = ('模式', '札', '帯', '年表', '比べ', '並べ', '流れ', '表', '棒', '線', '割合', '時計', '言葉', '箱')
FIG_RUN = ('模式',)                                # 続くと ⚠️（m32 の「図の型『模式』の連続」と同じ物差し）
JI_OK = ('CC BY 2.0', 'CC0', 'PD', 'Pexels')
SAY_NOT = ('犠牲', '死亡', '208秒', '墜落', '奇跡')
NG = {
    'VF': 'VTS の FirstFerry＝CrashAndRescue の 3分37秒〜4分22秒と重なる（② の決め）',
    'C10': '[10]＝消防の隊長の上着に個人の名前の字',
    'C17': '[17]＝[18] を切って色を直した版＝原本の [18] を使う',
    'C37': '[37]＝[38] の切り抜き（同じ写真）＝[38] を使う',
    'C12': '[12]＝夜の岸壁で話す3人（頁の説明に役職と名前）＝作業の絵でない・顔が主役',
    'C28': '[28]〜[30]＝BY-SA の別の版の束（使わないと ② で決めた）', 'C29': '同上', 'C30': '同上',
    'C58': '[58]＝題と中身が別物（バス停の掲示）', 'C71': '[71]＝私人の顔の近景（BY-SA）', 'C72': '[72]＝私人の顔の近景（BY-SA）',
    'C69': '[69]＝荷物の札に乗客の名前の字が読める（⑤b-2〈11-10〉に原寸で見た）＝BY-SA で隠せない＝使わない（cc08 は差し替え＝Commons から取る点は了承を得てから）',
}
GROUND_MIN_W = 1200                                # 地は 1920 へ引き伸ばす＝これより小さい写真は柔らかい（⚠️）
KEYS = ['cid', 'kind', 'main', 'ji', 'frame', 'sub', 'motion', 'look', 'ga_new', 'note', 'mark']
SKEYS = ['code', 'type', 'grp', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
MOTIONS = ('ゆっくり寄る', 'ゆっくり引く', '左へ流す', '右へ流す', '静止')
PAGEMAP = (('付録B p', 'R'), ('付録C p', 'R'), ('報告書 p', 'R'))
# 地のイメージ〈…〉→ Pexels の記号（31本目 GMAP の型＝束の道具は記号の「:」の前しか見ない）。名は台本の地の欄と字まで同じ
GMAP = (('操縦室', 'GK1'), ('冬の空', 'GS1'), ('シミュレーター', 'GM1'), ('冊子の目次', 'GB1'), ('冊子の束', 'GB2'), ('雲の上', 'GC1'),
        ('冬の川面', 'GR2'), ('映画館の客席', 'GT1'), ('管制室のレーダーの画面', 'GA1'), ('冬の川を上から', 'GR1'), ('翼のうしろの板', 'GF1'),
        ('速さの計器', 'GK2'), ('救命胴衣', 'GL1'))
DATE = re.compile(r'(?:(\d{4})年)?(\d{1,2})月(\d{1,2})日')


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


def vts_code(text):
    if 'After15Minutes' in text:
        return 'V15'
    if 'After20Minutes' in text:
        return 'V20'
    if 'FirstFerry' in text:
        return 'VF'
    return 'VC'


def ji_code(desc):
    """台本の「地＝…」→ 地の素材の記号（写真＝C<n>・衛星＝SAT:…・イメージ＝GMAP の記号〈無い名は G:…〉）"""
    m = re.search(r'地＝(.*)$', desc)
    if not m:
        return ''
    s = m.group(1)
    m2 = re.match(r'実写 写真 \[(\d+)\]', s)
    if m2:
        return 'C' + m2.group(1)
    m2 = re.match(r'実写 衛星 (.*?) を暗く', s)
    if m2:
        return 'SAT:' + m2.group(1).strip()
    m2 = re.match(r'イメージ〈([^〉]*)〉', s)
    if m2:
        return next((c for w, c in GMAP if m2.group(1) == w), 'G:' + m2.group(1))
    return '?' + s[:20]


def page_code(name):
    if name.startswith('連邦官報'):
        return 'FR2023'
    if name.startswith('報告書の題の頁'):
        return 'R3'
    for w, c in PAGEMAP:
        if name.startswith(w):
            m = re.match(r'(\d+)', name[len(w):])
            return c + m.group(1) if m else '?' + name
    return '?' + name


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
        a['main'] = vts_code(rest)
        a['frame'] = '額装（高さいっぱい）'
        a['motion'] = '映像'
    elif k == '写真':
        num = re.search(r'\[(\d+)\]', rest.split('（')[0])
        a['main'] = 'C' + num.group(1) if num else '?C'
        a['frame'] = '額装（高さいっぱい）' if ('額装' in desc or 'BY-SA' in desc) else '全面'
        a['motion'] = '静止' if a['frame'].startswith('額装') else next((w for w in MOTIONS if w in desc), 'ゆっくり寄る')
    elif k == '調査':
        num = re.search(r'#(\d+)', rest)
        a['main'] = 'D%s-?' % (num.group(1) if num else '?')
        a['frame'] = '額装（高さいっぱい）'
        a['motion'] = '静止'
    elif k == '衛星':
        a['main'] = 'SAT:' + ' '.join(tok[1:])
        a['frame'] = '額装（衛星）'
        a['motion'] = '静止'
    elif k == '公的':
        a['main'] = page_code(' '.join(tok[1:]))
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
    """「映像 7.00〜20.50秒」→ [(7.0, 20.5)]（元の秒）。区間を書いていなければ空"""
    return [(float(a), float(b)) for a, b in re.findall(r'([\d.]+)〜([\d.]+)秒', motion or '')]


def video_opts(motion):
    h = re.search(r'＋止め\s*([\d.]+)秒', motion or '')
    r = re.search(r'（([\d.]+)倍速）', motion or '')
    return float(h.group(1)) if h else 0.0, float(r.group(1)) if r else 1.0


def measured(cuts, narr=NARR):
    """⑤a のあと：秒を audio/narration.json の実測に（31本目 make_list31.measured の型）。いまは32本目の音が無い＝÷365 の見込み"""
    if not os.path.exists(narr):
        return '÷365 の見込み（narration.json が無い）'
    dur = json.load(open(narr, encoding='utf-8')).get('durations', {})
    if [c['cid'] for c in cuts] != [k for k in dur if k != 'ed01']:
        return '÷365 の見込み（narration.json は32本目の台本と合わない＝音は ⑤a のあと）'
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    import check_script as CSC
    t, prev = 0.0, None
    for c in cuts:
        key = CSC.door_key(c['cid'], slug='ep32')
        c['card'] = CSC.CARD_SEC if (prev is not None and key != prev) else 0.0
        prev = key
        c['start'] = t
        c['cont'] = dur[c['cid']] + CSC.LEAD + CSC.TAIL
        c['sec'] = c['cont'] + c['card']
        t += c['sec']
    return 'audio/narration.json の実測'


def gate_video(cuts, A, E, W):
    """VTS の門番：長さ・速さ・止め・外す秒・カメラの動く所・時計の時刻（動きの欄が「映像」で始まり素材が VTS のカット）"""
    for c in cuts:
        a = A.get(c['cid'])
        if not a or not a['motion'].startswith('映像') or base(a['main']) not in FOOT:
            continue
        cid, need, code = c['cid'], c.get('cont', c['sec']), base(a['main'])
        if re.search(r'\d{1,2}:\d{2}|\d+時\d+分', a['sub']):
            E.append('%s VTS の副題に時刻（焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）' % cid)
        win = windows(a['motion'])
        if not win:
            W.append('%s 映像の区間が未定（%s・要る秒 %.2f）' % (cid, code, need))
            continue
        hold, rate = video_opts(a['motion'])
        span = sum(w[1] - w[0] for w in win) / rate
        if span + hold + 0.005 < need:
            E.append('%s 映像の区間 %.2f秒＋止め %.2f秒がカットの %.2f秒に足りない' % (cid, span, hold, need))
        elif span + hold - need < 0.5:
            W.append('%s 映像の区間のゆとりが %.2f秒（⑤a の実測で足りなくなるかも）' % (cid, span + hold - need))
        if rate != 1.0:
            E.append('%s VTS の速さを変えた（%.2f倍）＝記録の見た目のまま等速' % (cid, rate))
        if hold:
            W.append('%s 止め %.2f秒（VTS は等速の記録＝止めは最後の手段）' % (cid, hold))
        F = FOOT[code]
        for s, e in win:
            if s < -1e-6 or e > F['len'] + 0.05:
                E.append('%s %s の区間 %.2f〜%.2f が素材の長さ %.2f秒をこえる' % (cid, F['name'], s, e, F['len']))
            if not any(lo - 1e-6 <= s and e <= hi + 1e-6 for lo, hi in F['ok']):
                W.append('%s %s の区間 %.2f〜%.2f がカメラの落ち着いた区間に収まらない（振り・寄りが入る）' % (cid, F['name'], s, e))
            for fc, xa, xb, why in EXCLUDE:
                if fc == code and min(e, xb + MARGIN) - max(s, xa - MARGIN) > 1e-6:
                    E.append('%s 区間 %.2f〜%.2f が外す秒 %.1f〜%.1f（前後 0.5秒）に触れる＝%s' % (cid, s, e, xa, xb, why))


def stock_rows(A, S):
    """台本のイメージ（X…）と地のイメージ（G…）は素材の表に1行ずつ足す＝⑤b で Pexels を1本ずつ探す"""
    for cid, a in A.items():
        if a['kind'] == 'イメージ' and base(a['main']) not in S:
            S[base(a['main'])] = dict(zip(SKEYS, [base(a['main']), 'stock', 'stock', a['sub'], '⑤b で Pexels を1本ずつ（原寸で見る）', '—', 'Pexels', 'Pexels のライセンス＝頁を credits に', 'イメージ（Pexels）', '現在', 'なし（顔・ナンバー・店の字なし）', '', '']))
        j = base(a['ji'])
        if j.startswith('G') and not j.startswith('G:') and j not in S:
            name = next((w for w, c in GMAP if c == j), j)
            S[j] = dict(zip(SKEYS, [j, 'stock', 'ground', name, '⑤b で Pexels を1本（地だけ・暗くする）', '—', 'Pexels', 'Pexels のライセンス＝頁を credits に', '地の写真：イメージ（Pexels）', '現在', 'なし（顔・ナンバー・店の字なし）', '', '']))


def era_date(era):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', era or '')
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def gate_era(cid, a, s, E):
    """写真の副題の日付と時刻の語が、確かめた時点（era）と合うか"""
    if not s or a['kind'] not in ('写真', '調査'):
        return
    era = s['era']
    d = era_date(era)
    for y, mo, dd in DATE.findall(a['sub']):
        if not d:
            E.append('%s 副題に日付（%s月%s日）があるが、確かめた時点に日が無い（%s）' % (cid, mo, dd, era or '空'))
        elif (int(y) if y else d[0], int(mo), int(dd)) != d:
            E.append('%s 副題の日付（%s月%s日）が確かめた時点（%s）と合わない' % (cid, mo, dd, era))
    for w in ('夕方', '夜', '朝'):
        if w in a['sub'] and w not in era:
            E.append('%s 副題の「%s」が確かめた時点（%s）に無い' % (cid, w, era or '空'))


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
            if not code or code.endswith('?'):
                E.append('%s %s なのに素材の記号が決まっていない（%s）' % (cid, k, code))
            elif not s:
                E.append('%s 素材 %s が sources32.psv に無い' % (cid, code))
        for c2 in (code, ji):
            if c2 in NG:
                E.append('%s 使わないと決めた点 %s を使った（%s）' % (cid, c2, NG[c2]))
        frame, motion = a['frame'], a['motion']
        if s and 'BY-SA' in s['rights'] and (not frame.startswith('額装') or motion != '静止'):
            E.append('%s BY-SA の写真 %s は額装・静止（%s・%s）' % (cid, code, frame, motion))
        if k in ('公的', '調査') and (not frame.startswith('額装') or motion != '静止'):
            E.append('%s 紙面・調査の写真は額装・静止（%s・%s）' % (cid, frame, motion))
        if k in ('公的', '調査') and s and not s['credit']:
            E.append('%s 紙面・調査の写真の出典の行が無い' % cid)
        if frame.startswith('額装') and k != '映像' and motion != '静止':
            E.append('%s 額装に動き（%s）＝額装は静止' % (cid, motion))
        if k == 'イメージ' and not a['sub'].startswith('イメージ'):
            E.append('%s イメージの副題が「イメージ」で始まらない' % cid)
        for w in SAY_NOT:
            if w in a['sub']:
                E.append('%s 言わない語「%s」が副題に' % (cid, w))
        gate_era(cid, a, s, E)
        if k in FIGS:
            if not ji:
                E.append('%s 図（%s）なのに地の写真が無い＝文字だけの画面' % (cid, k))
            else:
                sj = S.get(ji)
                if ji.startswith('SAT'):
                    E.append('%s Google の衛星写真を地にした（暗くすると見た目を大きく変える＝Geo Guidelines・11-05 の決め）' % cid)
                elif not sj:
                    E.append('%s 地 %s が sources32.psv に無い' % (cid, ji))
                else:
                    if not any(sj['rights'].startswith(x) for x in JI_OK):
                        E.append('%s 地 %s が地に使える権利でない（%s）' % (cid, ji, sj['rights']))
                    if 'night' in sj['grp']:
                        E.append('%s 夜の暗い写真 %s を地にした（29本目＝暗くすると何の写真か分からない）' % (cid, ji))
                    wd = re.match(r'([\d,]+)×', sj['dims'] or '')
                    if wd and int(wd.group(1).replace(',', '')) < GROUND_MIN_W:
                        W.append('%s 地 %s が小さい（幅 %s＝1920 へ引き伸ばすと柔らかい）' % (cid, ji, wd.group(1)))
        if cid in OPENING and k not in COUNT20:
            E.append('%s 冒頭は実写だけ（%s）' % (cid, k))
        if k == '映像':
            spans += [(cid, code, w) for w in windows(motion)]
        for fld in ('sub', 'note', 'ga_new', 'look'):
            for nm in name_list:
                if nm and nm in a[fld]:
                    E.append('%s 書かない名前が %s の欄に' % (cid, fld))
        if k in COUNT20 and s:
            use[code].append(cid)
            subs[code].add(a['sub'])
            if s['people'] and not s['people'].startswith(('なし', '—')):
                W.append('%s %s 人＝%s' % (cid, code, s['people']))
        if '△' in a['mark']:
            W.append('%s △ %s' % (cid, a['note'][:60]))
    for code, s in S.items():
        for fld in ('title', 'credit', 'note', 'get', 'people'):
            for nm in name_list:
                if nm and nm in s[fld]:
                    E.append('素材 %s の %s の欄に書かない名前' % (code, fld))
    spans.sort(key=lambda x: (x[1], x[2][0]))
    for (c1, f1, s1), (c2, f2, s2) in zip(spans, spans[1:]):
        if f1 == f2 and s2[0] < s1[1] - 0.05:
            E.append('映像の区間が重なる（同じ秒を2回）: %s %.2f〜%.2f と %s %.2f〜%.2f' % (c1, s1[0], s1[1], c2, s2[0], s2[1]))
    for code, cids in use.items():
        s = S[code]
        if 'BY-SA' in s['rights'] and len(cids) > 1:
            E.append('BY-SA の写真 %s を %d カット（1点1カット）: %s' % (code, len(cids), ' '.join(cids)))
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
        if sj and 'BY-SA' in sj['rights']:
            E.append('%s BY-SA の写真 %s を地にした（額装・無加工だけ）' % (cid, j))
    n20 = sum(1 for cid in order if A[cid]['kind'] in COUNT20)
    if order and n20 / len(order) < PHOTO_LO:
        E.append('写真・映像・紙面が %d／%d＝%.1f%%（20%% 以上）' % (n20, len(order), 100.0 * n20 / len(order)))
    seq = [A[c] for c in order]
    for i in range(1, len(order)):
        k0, k1 = seq[i - 1]['kind'], seq[i]['kind']
        if k0 in FIG_RUN and k0 == k1:
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
    L = ['---', 'title: 32本目 場面ごとの映像・写真の一覧（機械で組む）', 'created: 2026-11-10', 'tags: [project/jiko-kensho, ep32]', '---', '',
         '# 32本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % len(order), '',
         '> **機械で組む一覧＝手で直さない**。作り方＝`python -P ref/ep32/eizou_build/make_list32.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄＝土台・差し替え `eizou_build/over32.psv`・出どころ `eizou_build/sources32.psv`・決め `eizou_build/decisions32e.md`）。直すのは入力。',
         '> 秒＝%s（カットの頭・カッコはカットの秒）。🔧＝台本の画の欄から替えたカット' % tnote +
         '（⑤b はこの一覧に従う・台本は直さない）。色味は原本（10-07）・写真は画面いっぱい（10-11）・全面にできない点（BY-SA・4:3 の記録映像〈VTS〉・縦長・小さい写真・紙面）は**高さいっぱいの額＋地は同じ絵のぼかし**（10-30）・額装はどれも静止（10-26）・衛星写真の額の地は方眼のまま（11-05）。説明カットの地＝写真を暗くするだけ・静止（§5b-117）・🔴 Google の衛星写真と夜の写真は地にしない。見た画像の記録＝`src/look/seen_log.tsv`。🔴 撮影者の個人名はここに書かない（`{作者}`＝git の外の `src/credits_private.tsv` から ⑤b で差し込む）。Commons の点は [n]＝記号 C<n>（`src/look/commons_index.tsv` の idx）。',
         '', '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真・映像・紙面（§2-1 で数える） | **%d カット＝%.1f%%**（映像 %d・写真 %d・調査 %d・衛星 %d・紙面 %d・秒 %.0f＝%.1f%%） | 20%%以上 ✅ |' % (
             n20, 100.0 * n20 / len(order), kinds['映像'], kinds['写真'], kinds['調査'], kinds['衛星'], kinds['公的'], sec20, 100.0 * sec20 / total),
         '| そのうちこの事故の写真と映像（紙面・衛星を除く） | %d カット＝%.1f%% | 参考 |' % (n_event, 100.0 * n_event / len(order)),
         '| フリー素材（イメージ） | %d カット（20%% に数えない・⑤b で1本ずつ探す） | 人の顔・社名・機種・読める画面の字なし・AI で作った絵なし・「イメージ」と出す |' % kinds['イメージ'],
         '| 図 | %d カット（模式 %d・ほか %d＝地はすべて写真） | 地は暗くするだけ・動かさない |' % (len(figs), kinds['模式'], len(figs) - kinds['模式']),
         '| 見せ方（写真・映像・紙面・イメージ） | %s | 額装は静止 |' % '・'.join('%s %d' % kv for kv in frames.most_common()),
         '| 動き | %s | 全面は寄る／流す |' % '・'.join('%s %d' % kv for kv in motions.most_common()),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % fixed,
         '| 種類 | %s | — |' % '・'.join('%s %d' % kv for kv in kinds.most_common()),
         '| 合計 | %d カット・%s（%s・ed01 を除く） | — |' % (len(order), fmt(total), tnote), '',
         '### 章ごとの写真・映像・紙面（§2-1 は章ごとを見ない＝参考・20%% 未満の章に印）', '', '| 章 | カット | 写真・映像・紙面 | 割合 | イメージ | 図 |', '|---|---:|---:|---:|---:|---:|']
    for r in chap_rows(cuts, A):
        p = 100.0 * r['real'] / r['n']
        L.append('| %s | %d | %d | %s%.0f%% | %d | %d |' % (r['chap'], r['n'], r['real'], '⚠️ ' if p < 20 else '', p, r['img'], r['fig']))
    L += ['', '### 写真の使い回し（全面・額装で2回以上＝地は数えない・紙面と VTS は別の頁と秒）', '']
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
          '| 記号 | 種類 | 群 | 見て確かめた中身 | 取り方 | 幅×高 | 権利 | 根拠 | 画面の出典の行 | 時点 | 人 | ファイル | 使うカット | 備考 |',
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
        f.write('cid\tchap\tstart\tsec\tkind\tmain\tji\tframe\tsub\tmotion\tfixed\tmark\tcard\tcont\n')      # 列の名は list31.tsv と同じ
        for c in cuts:
            a = A[c['cid']]
            f.write('%s\t%s\t%.2f\t%.2f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.2f\t%.2f\n' % (c['cid'], c['chap'], c['start'], c['sec'], a['kind'], a['main'], a['ji'], a['frame'], a['sub'], a['motion'], '🔧' if a['ga_new'].startswith('🔧') else '', a['mark'], c.get('card', 0.0), c.get('cont', c['sec'])))
    return n20, len(order)


def selftest():
    def cut(cid, sec=1.0):
        return dict(cid=cid, chap='章', lines=['あ'], chars=1, start=0.0, sec=sec, cont=sec, head='あ', ga='')
    row = lambda code, typ, rights, credit='出典', grp='', people='なし', era='': dict(zip(SKEYS, [code, typ, grp, '', '', '', rights, '', credit, era, people, '', '']))
    S = {'C26': row('C26', 'commons-photo', 'CC BY 2.0', era='2009-01-15'), 'C46': row('C46', 'commons-photo', 'CC BY-SA 3.0', grp='night', era='2009-01・夜'),
         'C40': row('C40', 'commons-photo', 'CC BY 2.0', grp='night', era='2009-01-17 00:07・夜'), 'C36': row('C36', 'commons-photo', 'PD', era='2009-01-16 13:57'),
         'C21': row('C21', 'commons-photo', 'PD（PD-USACE）', era='2009-01-15'),
         'SAT:x': row('SAT:x', 'google', 'Google'), 'R189': row('R189', 'public-page', 'PD'), 'VC': row('VC', 'commons-video', 'PD'),
         'D76-4': row('D76-4', 'docket-photo', 'PD の見込み'), 'GK1': row('GK1', 'stock', 'Pexels')}
    ok = dict(kind='模式', main='', ji='C26', frame='—', sub='札', motion='', look='', ga_new='', note='', mark='')
    pho = dict(kind='写真', main='C26', ji='', frame='全面', sub='翼の上に並んだ人たち〈2009年1月15日〉', motion='ゆっくり寄る', look='', ga_new='', note='', mark='')
    sat = dict(pho, kind='衛星', main='SAT:x', frame='額装（衛星）', sub='衛星', motion='静止')

    def setup(extra):
        cuts = [cut(c) for c in OPENING] + [cut(c) for c in ('c201', 'c202')] + [cut(c) for c in extra if c not in OPENING]
        A = {c['cid']: dict(sat, cid=c['cid']) for c in cuts}
        return cuts, A

    def run(cid, r, name=''):
        cuts, A = setup([cid])
        A[cid] = dict(r, cid=cid)
        return gates(cuts, A, S, (name,) if name else ())[0]
    T = [
        ('陰性 模式（地 CC BY）', 'c701', ok, None),
        ('陰性 写真（日付が合う）', 'c701', pho, None),
        ('陽性 NG の点 [37]', 'c701', dict(pho, main='C37'), '使わないと決めた'),
        ('陽性 地が無い', 'c701', dict(ok, ji=''), '文字だけ'),
        ('陽性 Google を地に', 'c701', dict(ok, ji='SAT:x'), 'Google'),
        ('陽性 夜の写真を地に', 'c701', dict(ok, ji='C40'), '夜の暗い写真'),
        ('陽性 BY-SA を地に', 'c701', dict(ok, ji='C46'), 'BY-SA の写真 C46 を地に'),
        ('陽性 BY-SA を全面', 'c701', dict(pho, main='C46', sub='引き上げられる機体〈2009年1月〉'), 'BY-SA の写真 C46 は額装'),
        ('陰性 PD-USACE（字に SA）を全面', 'c701', dict(pho, main='C21', sub='消防艇〈2009年1月15日〉'), None),
        ('陰性 PD-USACE（字に SA）を地に', 'c701', dict(ok, ji='C21'), None),
        ('陽性 副題の日付が違う', 'c701', dict(pho, main='C36', sub='岸壁の機体〈2009年1月15日〉'), '日付'),
        ('陽性 副題の夕方が無い', 'c701', dict(pho, main='C36', sub='夕方の機体〈2009年1月16日〉'), '夕方'),
        ('陰性 夜と書いて夜の写真', 'c701', dict(pho, main='C40', sub='夜の岸壁のそばの機体〈2009年1月17日〉'), None),
        ('陽性 額装に動き', 'c701', dict(pho, frame='額装（高さいっぱい）'), '額装に動き'),
        ('陽性 冒頭にイメージ', 'c101', dict(pho, kind='イメージ', sub='イメージ：空', main='X101'), '冒頭は実写'),
        ('陽性 イメージの副題', 'c701', dict(pho, kind='イメージ', sub='空', main='X701'), 'イメージの副題'),
        ('陽性 書かない名前', 'c701', dict(ok, note='山田'), '書かない名前'),
        ('陽性 言わない語', 'c701', dict(ok, sub='墜落した機体'), '言わない語'),
        ('陽性 紙面に動き', 'c701', dict(pho, kind='公的', main='R189', frame='全面', sub=''), '紙面・調査の写真は額装'),
        ('陽性 調査の写真を全面', 'c701', dict(pho, kind='調査', main='D76-4', sub='凹み'), '紙面・調査の写真は額装'),
        ('陽性 調査の記号が未定', 'c701', dict(pho, kind='調査', main='D76-?', frame='額装（高さいっぱい）', motion='静止', sub='凹み'), '決まっていない'),
    ]
    bad = 0
    for label, cid, r, want in T:
        E = run(cid, r, name='山田')
        hit = any(want in x for x in E) if want else not E
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E[:3]))
        bad += 0 if hit else 1
    # BY-SA は1点1カット・同じ写真に別の副題
    cuts, A = setup(['c701', 'c702'])
    A['c701'] = dict(pho, cid='c701', main='C46', frame='額装（高さいっぱい）', motion='静止', sub='引き上げられる機体〈2009年1月〉')
    A['c702'] = dict(pho, cid='c702', main='C46', frame='額装（高さいっぱい）', motion='静止', sub='吊られる機体〈2009年1月〉')
    E = gates(cuts, A, S)[0]
    hit = any('1点1カット' in x for x in E) and any('別の副題' in x for x in E)
    print(('OK  ' if hit else 'NG  ') + '陽性 BY-SA を2カット・別の副題' + ('' if hit else ' → %s' % E[:3]))
    bad += 0 if hit else 1
    # VTS の区間の重なり
    for label, second, want in (('陽性 VTS の区間が重なる', '映像 15.00〜25.00秒', True), ('陰性 VTS の区間が離れている', '映像 82.00〜95.50秒', False)):
        cuts, A = setup(['c702'])
        A['c101'] = dict(pho, cid='c101', kind='映像', main='VC', frame='額装（高さいっぱい）', motion='映像 7.00〜20.50秒', sub='沿岸警備隊の監視カメラ〈2009年1月15日・ハドソン川〉')
        A['c702'] = dict(pho, cid='c702', kind='映像', main='VC', frame='額装（高さいっぱい）', motion=second, sub='川に浮かぶ機体〈沿岸警備隊の監視カメラ〉')
        E = gates(cuts, A, S)[0]
        hit = any('重なる' in x for x in E) == want
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E[:3]))
        bad += 0 if hit else 1
    # VTS の長さ・速さ・外す秒・時計
    for label, motion, sub, sec, want in (
            ('陰性 VTS の長さ 足りる', '映像 82.00〜95.50秒', '川に浮かぶ機体', 9.2, None),
            ('陽性 VTS の長さ 足りない', '映像 82.00〜88.00秒', '川に浮かぶ機体', 9.2, '足りない'),
            ('陽性 VTS の速さを変えた', '映像 82.00〜86.00秒（0.50倍速）', '川に浮かぶ機体', 8.0, '速さを変えた'),
            ('陽性 コンコルドの秒に触れる', '映像 415.00〜427.00秒', '機体のまわりのフェリー', 9.0, '外す秒'),
            ('陽性 素材の長さをこえる', '映像 480.00〜495.00秒', '機体のまわりのフェリー', 9.0, '素材の長さ'),
            ('陽性 副題に時計の時刻', '映像 82.00〜95.50秒', '3:32 の機体', 9.2, '時刻')):
        c1 = dict(cut('c701', sec))
        A1 = {'c701': dict(pho, cid='c701', kind='映像', main='VC', frame='額装（高さいっぱい）', motion=motion, sub=sub)}
        E1, W1 = [], []
        gate_video([c1], A1, E1, W1)
        hit = any(want in x for x in E1) if want else not E1
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E1[:3]))
        bad += 0 if hit else 1
    # 地の記号の読み（台本の書き方）
    for desc, want in (('札・地＝実写 写真 [50] を暗く〈博物館の展示の格納庫〉', 'C50'), ('札・地＝実写 衛星 ハドソン川 を暗く', 'SAT:ハドソン川'),
                       ('札・地＝イメージ〈操縦室〉を暗く', 'GK1'), ('札・地＝実写 写真 [61]〈切出の版〉を暗く', 'C61')):
        got = ji_code(desc)
        hit = got == want
        print(('OK  ' if hit else 'NG  ') + '地の読み %s' % want + ('' if hit else ' → %s' % got))
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
    gate_video(cuts, A, E, W)
    E = bad1 + bad2 + bad3 + E
    n, m = build(cuts, A, S, E, W, tnote)
    print('秒＝%s／合計 %s' % (tnote, fmt(sum(c['sec'] for c in cuts))))
    print('カット %d／写真・映像・紙面 %d（%.1f%%）／E %d ／⚠️ %d → %s' % (m, n, 100.0 * n / m, len(E), len(W), OUT_MD))
    for x in E[:80]:
        print('E ', x)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
