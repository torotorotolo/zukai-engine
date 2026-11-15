# -*- coding: utf-8 -*-
"""33本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-11-14・チャット5）。32本目 make_list32.py の型を33本目（241カット・グレンフェルタワー火災）に合わせた。

  python -P -X utf8 ref/ep33/eizou_build/make_list33.py             一覧を書く（E があれば exit 1）
  python -P -X utf8 ref/ep33/eizou_build/make_list33.py --selftest  陽性・陰性の対照（門番が狙いの門で鳴ることを先に見る）
  python -P -X utf8 ref/ep33/eizou_build/make_list33.py --dump      台本の画の欄を読んだだけの形（差し替えの前）
  python -P -X utf8 ref/ep33/eizou_build/make_list33.py --ji        地の写真の種類と数（差し替えと地の決まりを当てたあと）
  python -P -X utf8 ref/ep33/eizou_build/make_list33.py --runs      図の型「模式」の続き（台本のままと一覧の両方）

入力：台本 第2版 ref/ep33/daihon_v2.md §4（語りの字数・秒＋画の欄＝土台・台本は直さない）
      eizou_build/over33.psv（台本の画の欄から替えるカットだけ・11列＝「=」はそのまま）・eizou_build/sources33.psv（Commons と映像の出どころ・13列）
      eizou_build/decisions33e.md（§5）。紙面（報告の図）・公的（文字の頁）・衛星・イメージの行は、台本の出典の行から機械で足す
出力：ref/ep33/eizou_list33.md（手で直さない）・eizou_build/list33.tsv（列の名は list32.tsv と同じ）
地の決まり（§5b-117「その場面の直前の写真が自然」・11-14 映像方針）：図のカットの地は、差し替えで決めていなければ
  ①同じ章の直前の写真（Commons の写真かイメージ・地に使える権利・夜と暗い絵と画面でない）→ ②無ければ同じ章のあと → ③無ければ前の章の最後。
  1点の地は JI_MAX カットまで（こえたら次に近い写真）
門番（E があれば exit 1・⚠️ は止めない）：
  E カットの数（241）／種類の名／素材の記号が無い・表に無い／使わないと決めた点（NG＝追悼の場と支援の58点・組の片方・[2] ほか）
  E 冒頭（c101〜c113）が実写でない／引き（c105）の終わりが46秒をこえる
  E 紙面（報告の図＝第三者のコマ）・公的（文字の頁）＝額装でない・動きがある・出典の行が無い／紙面を地にした
  E 紙面の副題の時刻が、本文で確かめたコマの時刻（FIG_ERA）と合わない・確かめた時刻が無いのに副題に時刻
  E BY-SA＝額装でない・動きがある・2カット以上・地に使った
  E 額装に動き（10-26）／地が CC BY・CC0・PD・Pexels でない・夜や暗い絵や画面を地に・Google の衛星写真を地に／図なのに地が無い
  E イメージの副題が「イメージ」で始まらない／写真の副題の日付と時刻の語が、確かめた時点（era）と合わない
  E 同じ写真を3回以上・同じ写真や紙面に別の副題・写真と映像と紙面が 20% 未満（§2-1）
  E 書かない名前（src/names_private.txt・names_commons.txt）が副題・備考・出どころに／言わない語（犠牲・死亡・見捨て・史上最悪・60時間・殺）が副題に
  E 映像（#15）の区間が素材の長さをこえる・同じ秒を2回・カットの秒に足りない・外す秒（黒・空撮の切れ目）に触れる
  ⚠️ 同じ写真を2回／別の写真に同じ副題／写真の無い画面が5つ以上続く／図の型「模式」が続く／人の印／△／映像の区間が未定／額装の副題が20字をこえる
秒＝台本の 句読点なし÷365 の見込み（33本目の音はまだ＝⑤a のあと audio/narration.json の実測に替える）。
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
NARR = os.path.join(REPO, 'audio', 'narration.json')
DAIHON = os.path.join(EP, 'daihon_v2.md')
OUT_MD = os.path.join(EP, 'eizou_list33.md')
OUT_TSV = os.path.join(HERE, 'list33.tsv')
OVER = os.path.join(HERE, 'over33.psv')
SOURCES = os.path.join(HERE, 'sources33.psv')
DECIDE = os.path.join(HERE, 'decisions33e.md')
NAME_FILES = (os.path.join(EP, 'src', 'names_private.txt'), os.path.join(EP, 'src', 'names_commons.txt'))
PUNCT = re.compile(r'[、。，．,.「」『』（）()？！?!…・\s　〈〉：:"“”]')
CUT = re.compile(r'^\*\*(c[0-9a-c]\d\d)\*\*(.*)$')
OPENING = ['c1%02d' % i for i in range(1, 14)]
HOOK, HOOK_MAX = 'c105', 46.0
N_CUTS = 241
RATE = 365.0
PHOTO_LO = 0.20
GAP_MIN = 8
JI_MAX = 8
SUB_FRAME_MAX = 20
# #15 GRENFELL.webm（Commons・CC BY 3.0・1920×1080・4分10秒）。区間＝240p の1秒ごとのコマで決める（映像方針・了承②のあと）
FOOT = {'V15': dict(name='GRENFELL.webm', len=250.38)}
# 外す秒（11-15 に 240p の場面ごとのコマで見た・切れ目は 1080p の区間で 0.25秒の細かさに合わせた）
EXCLUDE = (('V15', 0.0, 8.5, '頭の黒'), ('V15', 35.5, 43.0, 'ビルの広告の幕の字'), ('V15', 75.0, 82.5, '歩く人の顔'),
           ('V15', 118.0, 125.0, '建物の名の看板'), ('V15', 187.75, 194.75, '塔の窓に作業の人'), ('V15', 235.0, 250.38, '尻の黒'))
MARGIN = 0.25                                      # 切れ目は 1080p の区間で 0.25秒の細かさに合わせた（11-15）＝区間は切れ目から 0.3秒あける
# 🆕 2026-11-15（33本目 ⑤b-1）：#15 の場面の切れ目（元の映像の秒）＝240p の全体を ffmpeg の場面の変わり目（scene＞0.20）で測った32か所。
#    1080p の区間3つでも同じ秒（区間ファイルの頭＝元の 18.327・118.207・172.327 秒＝頼んだ秒の手前のキーフレーム）。20.967・28.327・35.567・216.647 は
#    隣のコマの灰色の差が1コマだけ跳ねる＝硬いカット（中央値 0.53 に対し 24〜69）。174.887〜175.767 は動く空撮から T1 へのつなぎ（4つ）。
#    使う秒（区間の頭から、カットの画面の長さ cont のぶん）が切れ目をまたぐと、次の場面が一瞬入る＝止める（場面の替わりを決めて使うカットは ALLOW_CROSS）
SCENE_CUTS = {'V15': (8.727, 20.967, 28.327, 35.567, 42.967, 51.407, 59.567, 67.687, 74.887, 82.287, 89.527, 96.767, 104.047, 111.207, 118.207,
                      125.087, 132.127, 139.127, 146.127, 153.127, 159.967, 174.887, 175.007, 175.647, 175.767,
                      182.407, 187.767, 194.927, 202.087, 209.287, 216.647, 235.167)}
ALLOW_CROSS = {'c109': (182.407,), 'c431': (202.087,)}   # decisions33e §5-9＝T1→T2・T4→T5 は区間の中で1回替わる（決めて使う）
SCENE_EDGE = 0.04                                  # 1コマ（毎秒25コマ）＝これより内側に切れ目があれば「またぐ」
EVENT =('映像', '写真', '紙面')                     # この火事の写真・映像（報告の夜の図を含む）
COUNT20 = EVENT + ('衛星', '公的')                  # §2-1 の写真・映像（紙面 ss.page・衛星写真も実写）＝20% に数える
PICTURE = COUNT20 + ('イメージ',)
FIGS = ('模式', '立面', '断面', '比べ', '帯', '年表', '方位', '棒', '時計', '流れ', '表', '暦', '割合', '札', '言葉', '並べ', '箱', '線')
FIG_RUN = ('模式',)
JI_OK = ('CC BY 2.0', 'CC BY 3.0', 'CC BY 4.0', 'CC0', 'PD', 'Pexels')
SAY_NOT = ('犠牲', '死亡', '見捨て', '史上最悪', '60時間', '殺')
NG = {
    'C2': '[2]＝朝8時5分の遠景（手前は別の塔）＝c415 の語り（2時50分〜3時半）と合わない＝図18.1 に替えた（11-14）',
    'C6': '[6]＝[7] の切り抜き（同じ写真）＝[7] を使う', 'C1': '[1]＝[2] の切り抜き', 'C9': '[9]＝細すぎる切り抜き', 'C10': '[10]＝遠くの煙（[3] で足りる）',
    'C17': '#17＝制作者のロゴと私人の顔（映像）', 'C14': '#14＝ロゴの文字', 'C16': '#16＝地図（衛星写真で）',
    'C22': '[22]＝[21] と同じ撮影者・3分差の組（片方だけ）', 'C27': '[27]＝[26] と組', 'C56': '[56]＝[18] と組', 'C65': '[65]＝[61] と同じ分の組',
    'C52': '[52]＝[53] と6秒差の同じ構図', 'C38': '[38]＝追悼の柵（BY-SA＝隠せない）',
    'C59': '[59]＝11-15 に原寸で見た＝塔でなく工事の囲いの門の札（作業の窓口の電話番号）＝副題と合わない',
    'C60': '[60]＝11-15 に見た＝囲いの掲示にデモの人の顔の写真',
}
for _n in range(73, 127):
    NG['C%d' % _n] = '追悼の場（11-14 に見本帳で見た＝犠牲者の写真・名前の書き込み・私人の顔・政治の文句＝決め⑥で使わない）'
for _n in range(127, 131):
    NG['C%d' % _n] = '支援（11-14 に見本帳で見た＝私人の顔が主役＝ca03 はイメージのまま）'
NG['C82'] = '行方の分からない人の掲示＝顔と名前（決め⑥）'
GROUND_MIN_W = 1200
KEYS = ['cid', 'kind', 'main', 'ji', 'frame', 'sub', 'motion', 'look', 'ga_new', 'note', 'mark']
SKEYS = ['code', 'type', 'grp', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
MOTIONS = ('ゆっくり寄る', 'ゆっくり引く', '左へ流す', '右へ流す', '静止')
VOLNAME = {'P1ES': '第1段階の報告 要約', 'P1V1': '第1段階の報告 第1巻', 'P1V2': '第1段階の報告 第2巻', 'P1V3': '第1段階の報告 第3巻',
           'P1V4': '第1段階の報告 第4巻', 'P2V1': '第2段階の報告 第1巻', 'P2V2': '第2段階の報告 第2巻', 'P2V3': '第2段階の報告 第3巻',
           'P2V4': '第2段階の報告 第4巻', 'P2V5': '第2段階の報告 第5巻', 'P2V6': '第2段階の報告 第6巻', 'P2V7': '第2段階の報告 第7巻'}
# 報告の図のコマの時刻＝図の前の本文の1文（11-14 映像方針で PDF の字の層から読んだ・fig33.py＝scratchpad の道具）
FIG_ERA = {
    'P1V4-22.8': ('01:09',), 'P1V2-10.14': ('01:19',), 'P1V2-10.22': ('01:27',), 'P1V2-14.1': ('02:06',),
    'P1V2-10.6': ('01:05',), 'P1V2-10.7': ('01:06',), 'P1V2-10.8': ('01:08',), 'P1V2-10.9': ('01:09',),
    'P1V4-22.15': ('01:15',), 'P1V2-10.15': ('01:21',), 'P1V2-10.17': ('01:27',),
    'P1V2-11.4': ('01:40', '01:43'), 'P1V2-11.5': ('01:40', '01:43'), 'P1V2-11.6': ('01:40', '01:43'), 'P1V2-11.7': ('01:40', '01:43'), 'P1V2-11.8': ('01:40', '01:43'),
    'P1V2-12.1': ('01:44',), 'P1V2-12.2': ('01:48',),
    'P1V2-13.1': ('02:00',), 'P1V2-12.7': ('02:05',), 'P1V3-17.3': ('03:28',), 'P1V3-17.4': ('03:27',), 'P1V3-18.1': ('03:34',), 'P1V3-19.1': ('04:02',),
}
FIG_NIGHT = set(FIG_ERA)                            # 夜のコマ（地にしない・紙面はそもそも地にしない）
DATE = re.compile(r'(?:(\d{4})年)?(\d{1,2})月(\d{1,2})日')
HM = re.compile(r'(?<![\d:])(\d{1,2}):(\d{2})(?![\d:])')
NIGHT_WORDS = ('夜', '暗い', '夕暮れ', '夜明け')
SCREEN_WORDS = ('画面', 'ブログ', '証明書', 'パソコン')


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
            bad.append('%s:%d 列の数 %d（%d のはず）: %s' % (os.path.split(path)[1], i, len(p), len(keys), ln[:60]))
            continue
        rows.append(dict(zip(keys, [x.strip() for x in p])))
    return rows, bad


def base(code):
    return (code or '').split('=')[0].strip()


def ji_code(desc):
    """台本の「地＝実写 写真 [28] を暗く」→ C28"""
    m = re.search(r'地＝実写 写真 \[(\d+)\]', desc)
    if m:
        return 'C' + m.group(1)
    m = re.search(r'地＝実写 衛星 (.*?) を暗く', desc)
    if m:
        return 'SAT:' + m.group(1).strip()
    m = re.search(r'地＝(.*)$', desc)
    return ('?' + m.group(1)[:20]) if m else ''


def fig_credit(code):
    vol, fig = code[2:].split('-', 1)
    return 'グレンフェル・タワー調査 %s 図%s（%d）' % (VOLNAME.get(vol, vol), fig, 2019 if vol.startswith('P1') else 2024)


def parse_ga(cid, ga):
    """台本の画の欄 1つ → 当て方の土台"""
    a = dict(cid=cid, kind='', main='', ji='', frame='—', sub='', motion='', look='', ga_new='', note='', mark='', credit='', label='')
    m = re.match(r'^(実写|イメージ|図)\s*(.*)$', ga, re.S)
    if not m:
        a['kind'] = '?'
        return a
    head, rest = m.group(1), m.group(2)
    inner = re.search(r'（(.*)）', rest, re.S)
    desc = inner.group(1) if inner else rest
    sub = re.search(r'副題「([^」]*)」', desc)
    a['sub'] = sub.group(1) if sub else ''
    cr = re.search(r'出典の行「([^」]*)」', desc)
    a['credit'] = cr.group(1) if cr else ''
    if '△' in desc:
        a['mark'] = '△'
    if head == 'イメージ':
        what = re.sub(r'^フリー素材(の映像)?＝', '', desc).split('〈')[0].split('・')[0]
        a.update(kind='イメージ', main='X' + cid[1:], frame='全面', sub='イメージ：' + what, motion='ゆっくり寄る')
        return a
    if head == '図':
        a['kind'] = rest.split('（')[0].strip()
        a['ji'] = ji_code(desc)
        a['sub'] = a['sub'] or re.sub(r'・?地＝.*$', '', desc).strip('・ ')[:60]
        return a
    tok = rest.split('（')[0].split()
    k = tok[0] if tok else ''
    a['kind'] = k
    if k == '紙面':
        a.update(main='F:%s-%s' % (tok[1], tok[2].lstrip('図')), frame='額装（高さいっぱい）', motion='静止')
    elif k == '写真':
        num = re.search(r'\[(\d+)\]', rest.split('（')[0])
        a['main'] = 'C' + num.group(1) if num else '?C'
        framed = '額装' in desc or 'BY-SA' in desc or '高さいっぱい' in desc
        a['frame'] = '額装（高さいっぱい）' if framed else '全面'
        a['motion'] = '静止' if framed else next((w for w in MOTIONS if w in desc), 'ゆっくり寄る')
    elif k == '映像':
        lab = re.search(r'#15 (\S+?)（', rest)
        a.update(main='V15', frame='全面', motion='映像（区間は未定）', label=lab.group(1) if lab else '')
    elif k == '衛星':
        a.update(main='SAT:' + ' '.join(tok[1:]), frame='額装（衛星）', motion='静止')
    elif k == '公的':
        a.update(main='P:' + cid, frame='額装（高さいっぱい）', motion='静止')
        yaku = re.search(r'訳の札「([^」]*)」', desc)
        a['sub'] = a['sub'] or ('訳の札「%s」' % yaku.group(1) if yaku else '（訳なし・頁だけ）')
        a['look'] = ' '.join(tok[1:])
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


def words(paths):
    out = []
    for path in paths:
        if os.path.exists(path):
            out += [w.strip() for w in open(path, encoding='utf-8') if w.strip() and not w.startswith('#') and len(w.strip()) >= 4]
    return out


def assemble(cuts, over):
    A = {c['cid']: parse_ga(c['cid'], c['ga']) for c in cuts}
    bad, fixed_ji = [], set()
    for o in over:
        a = A.get(o['cid'])
        if a is None:
            bad.append('%s 台本に無いカット（差し替えだけある）' % o['cid'])
            continue
        for k in KEYS[1:]:
            if o[k] != '=':
                a[k] = '' if o[k] == '—空' else o[k]
        if o['ji'] != '=':
            fixed_ji.add(o['cid'])
        if o['kind'] != '=' and a['kind'] in FIGS and o['ji'] == '=' and not a['ji']:
            pass
    return A, bad, fixed_ji


def auto_rows(A, S):
    """紙面・公的・衛星・イメージの行を、台本の出典の行と記号から足す（sources33.psv に同じ記号があればそちらが勝つ）"""
    for cid, a in A.items():
        code, k = base(a['main']), a['kind']
        if not code or code in S:
            continue
        if k == '紙面':
            S[code] = dict(zip(SKEYS, [code, 'report-fig', 'night' if code[2:] in FIG_NIGHT else 'report', '報告の図 %s（%s）' % (code[2:], a['sub']),
                                       '手元の報告の PDF から頁を描いて切る（図の番号と題の行ごと）', '埋め込み 約880px', 'OGL v3.0（第三者のコマ・図を含む）',
                                       '紙面の引用（§2-6c・§2-42）＝額装・無加工・サムネに使わない', fig_credit(code),
                                       '2017-06-14 ' + '／'.join(FIG_ERA.get(code[2:], ())) if code[2:] in FIG_ERA else '報告の図',
                                       'なし（⑤b で原寸）', 'src/inquiry/%s.pdf' % code[2:].split('-')[0], '']))
        elif k == '公的':
            rights = '政府標準利用規約（日本）' if a['look'].startswith(('国', '消')) else '引用（頭の1文だけ・罪名と名前を入れない）' if a['look'].startswith('警') else 'OGL v3.0'
            S[code] = dict(zip(SKEYS, [code, 'public-page', 'page', '文字の頁 %s' % a['look'], '手元の PDF か頁の写しから描く（⑤b）', '頁', rights,
                                       '公的な機関の文書（許可不要＝11-12）', a['credit'] or '?', '頁の日付', 'なし（名前の行は入れない）', '', '']))
        elif k == '衛星':
            S[code] = dict(zip(SKEYS, [code, 'google', 'sat', code[4:], '⑤b で Google の衛星写真を撮る（帰属の行を絵の近くに・色を変えない）', '1920×1080', 'Google',
                                       'Geo Guidelines＝見た目を大きく変えない', 'Google の表示（絵のそば）', '撮影の時点は ⑤b で', 'なし', '', '']))
        elif k == 'イメージ':
            what = a['sub'].replace('イメージ：', '')
            grp = 'stock' + (' night' if any(w in what for w in NIGHT_WORDS) else '') + (' screen' if any(w in what for w in SCREEN_WORDS) else '')
            S[code] = dict(zip(SKEYS, [code, 'stock', grp, what, '⑤b で Pexels を1本ずつ（原寸で見る）', '—', 'Pexels', 'Pexels のライセンス＝頁を credits に',
                                       'イメージ（Pexels）', '現在', 'なし（顔・社名・字・機種なし）', '', '']))
        elif k == '映像' and code not in S:
            S[code] = dict(zip(SKEYS, [code, 'commons-video', 'video', '?', '?', '?', '?', '?', '?', '?', '?', '', '']))


def eligible_ground(code, S):
    s = S.get(code)
    if not s or s['type'] not in ('commons-photo', 'stock'):
        return False
    if not any(s['rights'].startswith(x) for x in JI_OK) or 'BY-SA' in s['rights']:
        return False
    return not any(w in s['grp'] for w in ('night', 'screen', 'noground'))


def assign_grounds(cuts, A, S, fixed):
    order = [c['cid'] for c in cuts]
    chap = {c['cid']: c['chap'] for c in cuts}
    uses = Counter(base(A[c]['ji']) for c in order if A[c]['kind'] in FIGS and c in fixed)
    pics = [(i, c) for i, c in enumerate(order) if A[c]['kind'] in ('写真', 'イメージ') and eligible_ground(base(A[c]['main']), S)]
    for i, cid in enumerate(order):
        a = A[cid]
        if a['kind'] not in FIGS or cid in fixed:
            continue
        # 11-14：文字どおり「直前の写真」＝章をまたいでも直前（扉をはさんでも、見る人が最後に見た写真）→ 無ければあと
        before = [base(A[c]['main']) for j, c in sorted(pics, key=lambda x: -x[0]) if j < i]
        after = [base(A[c]['main']) for j, c in sorted(pics, key=lambda x: x[0]) if j > i]
        cands = []
        for m in before + after:
            if m not in cands:
                cands.append(m)
        pick = next((m for m in cands if uses[m] < JI_MAX), cands[0] if cands else '')
        a['ji'] = pick
        a['ji_auto'] = True
        uses[pick] += 1


def windows(motion):
    return [(float(x), float(y)) for x, y in re.findall(r'([\d.]+)〜([\d.]+)秒', motion or '')]


def measured(cuts, narr=NARR):
    """🆕 2026-11-15（33本目 ⑤b-1）：秒を audio/narration.json の実測に（32本目 make_list32.measured の型を写した）。
    カットの秒＝声＋LEAD＋TAIL（cont）＋章の扉（card＝章が替わるカットの頭だけ）。倍率の分母（写真の割合）は扉を除く＝build の sec20 は sec のまま
    （32本目と同じ）。narration.json がこの回の台本と合わなければ ÷365 の見込みのまま（音が本線に無い作業ツリーでも落ちない）"""
    if not os.path.exists(narr):
        return '÷365 の見込み（narration.json が無い）'
    dur = json.load(open(narr, encoding='utf-8')).get('durations', {})
    if [c['cid'] for c in cuts] != [k for k in dur if k != 'ed01']:
        return '÷365 の見込み（narration.json は33本目の台本と合わない＝音は ⑤a のあと）'
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    import check_script as CSC
    t, prev = 0.0, None
    for c in cuts:
        key = CSC.door_key(c['cid'], slug='ep33')
        c['card'] = CSC.CARD_SEC if (prev is not None and key != prev) else 0.0
        prev = key
        c['start'] = t
        c['cont'] = dur[c['cid']] + CSC.LEAD + CSC.TAIL
        c['sec'] = c['cont'] + c['card']
        t += c['sec']
    return 'audio/narration.json の実測'


def gate_video(cuts, A, E, W):
    for c in cuts:
        a = A.get(c['cid'])
        if not a or a['kind'] != '映像':
            continue
        # 🆕 33本目 ⑤b-1：要る秒＝カットの画面の長さ（cont＝声＋LEAD＋TAIL・章の扉を除く）＝⑤a-2 で当てた値（c526 7.57 ほか）
        cid, need, code = c['cid'], c.get('cont', c['sec']), base(a['main'])
        win = windows(a['motion'])
        if not win:
            W.append('%s 映像の区間が未定（%s・要る秒 %.1f）' % (cid, a.get('label') or code, need))
            continue
        span = sum(y - x for x, y in win)
        if span + 0.005 < need:
            E.append('%s 映像の区間 %.2f秒がカットの %.2f秒に足りない' % (cid, span, need))
        elif span - need < 0.5:
            W.append('%s 映像の区間のゆとりが %.2f秒（⑤a の実測で足りなくなるかも）' % (cid, span - need))
        # 🆕 33本目 ⑤b-1：使う秒（区間の頭から need 秒）が場面の切れ目をまたがないか（等速・止めなし＝要る秒だけ頭から使う）
        left, used = need, []
        for x, y in win:
            if left <= 1e-9:
                break
            d = min(y - x, left)
            used.append((x, x + d))
            left -= d
        for x, y in used:
            for t in SCENE_CUTS.get(code, ()):
                if x + SCENE_EDGE < t < y - SCENE_EDGE and t not in ALLOW_CROSS.get(cid, ()):
                    E.append('%s 使う秒 %.2f〜%.2f が場面の切れ目 %.3f秒をまたぐ（切れ目の前 %.2f秒・後 %.2f秒＝別の場面が一瞬入る）' % (cid, x, y, t, t - x, y - t))
        F = FOOT.get(code)
        for s, e in win:
            if F and (s < -1e-6 or e > F['len'] + 0.05):
                E.append('%s %s の区間 %.2f〜%.2f が素材の長さ %.1f秒をこえる' % (cid, F['name'], s, e, F['len']))
            for fc, xa, xb, why in EXCLUDE:
                if fc == code and min(e, xb + MARGIN) - max(s, xa - MARGIN) > 1e-6:
                    E.append('%s 区間 %.2f〜%.2f が外す秒 %.1f〜%.1f に触れる＝%s' % (cid, s, e, xa, xb, why))


def era_date(era):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', era or '')
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def gate_era(cid, a, s, E):
    """写真の副題の日付と時刻の語・紙面の副題の時刻が、確かめた時点と合うか"""
    if not s:
        return
    if a['kind'] == '紙面':
        allowed = FIG_ERA.get(base(a['main'])[2:], ())
        for h, mi in HM.findall(a['sub']):
            hm = '%02d:%s' % (int(h), mi)
            if not allowed:
                E.append('%s 紙面の副題に時刻 %s があるが、本文で確かめたコマの時刻が無い（FIG_ERA）' % (cid, hm))
            elif hm not in allowed:
                E.append('%s 紙面の副題の時刻 %s が本文のコマの時刻 %s と合わない' % (cid, hm, '・'.join(allowed)))
        return
    if a['kind'] != '写真':
        return
    era = s['era']
    d = era_date(era)
    for y, mo, dd in DATE.findall(a['sub']):
        if not d:
            E.append('%s 副題に日付（%s月%s日）があるが、確かめた時点に日が無い（%s）' % (cid, mo, dd, era or '空'))
        elif (int(y) if y else d[0], int(mo), int(dd)) != d:
            E.append('%s 副題の日付（%s月%s日）が確かめた時点（%s）と合わない' % (cid, mo, dd, era))
    ym = re.findall(r'(\d{4})年(\d{1,2})月(?!\d)', a['sub'])
    for y, mo in ym:
        if not (era or '').startswith('%s-%02d' % (y, int(mo))):
            E.append('%s 副題の年月（%s年%s月）が確かめた時点（%s）と合わない' % (cid, y, mo, era or '空'))
    for w in ('夕方', '夜明け', '夜', '朝'):
        if w in a['sub'] and w not in (era or ''):
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
            if not code or code.endswith('?') or code.startswith('?'):
                E.append('%s %s なのに素材の記号が決まっていない（%s）' % (cid, k, code))
            elif not s:
                E.append('%s 素材 %s が表に無い' % (cid, code))
        for c2 in (code, ji):
            if c2 in NG:
                E.append('%s 使わないと決めた点 %s を使った（%s）' % (cid, c2, NG[c2]))
        frame, motion = a['frame'], a['motion']
        if s and 'BY-SA' in s['rights'] and (not frame.startswith('額装') or motion != '静止'):
            E.append('%s BY-SA の写真 %s は額装・静止（%s・%s）' % (cid, code, frame, motion))
        if k in ('紙面', '公的') and (not frame.startswith('額装') or motion != '静止'):
            E.append('%s 紙面・文字の頁は額装・静止（%s・%s）' % (cid, frame, motion))
        if k in ('紙面', '公的') and s and (not s['credit'] or s['credit'] == '?'):
            E.append('%s 紙面・文字の頁の出典の行が無い' % cid)
        if frame.startswith('額装') and k != '映像' and motion != '静止':
            E.append('%s 額装に動き（%s）＝額装は静止' % (cid, motion))
        if frame.startswith('額装') and k in ('写真', '紙面') and len(a['sub']) > SUB_FRAME_MAX:
            W.append('%s 額装の副題が %d 字（約%d字まで）' % (cid, len(a['sub']), SUB_FRAME_MAX))
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
                    E.append('%s Google の衛星写真を地にした（Geo Guidelines・11-05）' % cid)
                elif ji.startswith(('F:', 'P:')):
                    E.append('%s 紙面・文字の頁を地にした（第三者のコマ・字の上に字）' % cid)
                elif not sj:
                    E.append('%s 地 %s が表に無い' % (cid, ji))
                else:
                    if not any(sj['rights'].startswith(x) for x in JI_OK):
                        E.append('%s 地 %s が地に使える権利でない（%s）' % (cid, ji, sj['rights']))
                    if 'night' in sj['grp']:
                        E.append('%s 夜や暗い絵 %s を地にした（29本目＝暗くすると何の写真か分からない）' % (cid, ji))
                    if 'screen' in sj['grp']:
                        E.append('%s 画面や書類の字の絵 %s を地にした（字の上に字＝§5b-117）' % (cid, ji))
                    wd = re.match(r'([\d,]+)×', sj['dims'] or '')
                    if wd and int(wd.group(1).replace(',', '')) < GROUND_MIN_W:
                        W.append('%s 地 %s が小さい（幅 %s）' % (cid, ji, wd.group(1)))
        if cid in OPENING and k not in COUNT20:
            E.append('%s 冒頭は実写だけ（%s）' % (cid, k))
        if k == '映像':
            spans += [(cid, code, w) for w in windows(motion)]
        for fld in ('sub', 'note', 'ga_new', 'look'):
            for nm in name_list:
                if nm and nm in a[fld]:
                    E.append('%s 書かない名前が %s の欄に' % (cid, fld))
        if k in COUNT20 and s and k != '公的':
            use[code].append(cid)
            subs[code].add(a['sub'])
            if s['people'] and not s['people'].startswith(('なし', '—')):
                W.append('%s %s 人＝%s' % (cid, code, s['people']))
        if '△' in a['mark']:
            W.append('%s △ %s' % (cid, (a['note'] or a['sub'])[:60]))
    for code, s in S.items():
        for fld in ('title', 'credit', 'note', 'get', 'people', 'basis'):
            for nm in name_list:
                if nm and nm in s[fld]:
                    E.append('素材 %s の %s の欄に書かない名前' % (code, fld))
    spans.sort(key=lambda x: (x[1], x[2][0]))
    for (c1, f1, s1), (c2, f2, s2) in zip(spans, spans[1:]):
        if f1 == f2 and s2[0] < s1[1] - 0.05:
            E.append('映像の区間が重なる（同じ秒を2回）: %s %.2f〜%.2f と %s %.2f〜%.2f' % (c1, s1[0], s1[1], c2, s2[0], s2[1]))
    by_sub = defaultdict(set)
    for code, cids in use.items():
        s = S[code]
        if len(subs[code]) > 1 and s['type'] != 'commons-video':
            E.append('同じ写真・紙面 %s に別の副題: %s' % (code, ' ／ '.join(sorted(subs[code]))))
        if 'BY-SA' in s['rights'] and len(cids) > 1:
            E.append('BY-SA の写真 %s を %d カット（1点1カット）: %s' % (code, len(cids), ' '.join(cids)))
        if s['type'] in ('commons-photo',):
            for sb in subs[code]:
                by_sub[sb].add(code)
        if s['type'].startswith(('stock', 'public-page', 'google', 'commons-video')):
            continue
        if len(cids) >= 3:
            E.append('同じ写真・紙面 %s を %d 回: %s' % (code, len(cids), ' '.join(cids)))
        elif len(cids) == 2:
            gap = abs(order.index(cids[1]) - order.index(cids[0]))
            W.append('同じ写真・紙面 %s を2回: %s%s' % (code, ' '.join(cids), '（%dカット差＝近い）' % gap if gap < GAP_MIN else ''))
    for sb, codes in by_sub.items():
        if len(codes) > 1:
            W.append('別の写真に同じ副題「%s」: %s' % (sb, ' '.join(sorted(codes))))
    for cid in order:
        sj = S.get(base(A[cid]['ji']))
        if sj and 'BY-SA' in sj['rights']:
            E.append('%s BY-SA の写真 %s を地にした（額装・無加工だけ）' % (cid, base(A[cid]['ji'])))
    n20 = sum(1 for cid in order if A[cid]['kind'] in COUNT20)
    if order and n20 / len(order) < PHOTO_LO:
        E.append('写真・映像・紙面が %d／%d＝%.1f%%（20%% 以上）' % (n20, len(order), 100.0 * n20 / len(order)))
    for i in range(1, len(order)):
        k0, k1 = A[order[i - 1]]['kind'], A[order[i]]['kind']
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


def gate_hook(cuts, E):
    c = next((x for x in cuts if x['cid'] == HOOK), None)
    if c and c['start'] + c['sec'] > HOOK_MAX:
        E.append('引き %s の終わり %.1f秒が %.0f秒をこえる' % (HOOK, c['start'] + c['sec'], HOOK_MAX))


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


def runs(order, A):
    return sum(1 for i in range(1, len(order)) if A[order[i - 1]]['kind'] in FIG_RUN and A[order[i - 1]]['kind'] == A[order[i]]['kind'])


def build(cuts, A, S, E, W, base_A, tnote='÷365 の見込み'):
    order = [c['cid'] for c in cuts]
    total = sum(c['sec'] for c in cuts)
    kinds = Counter(A[c]['kind'] for c in order)
    n20 = sum(1 for c in order if A[c]['kind'] in COUNT20)
    n20_0 = sum(1 for c in order if base_A[c]['kind'] in COUNT20)
    n_event = sum(1 for c in order if A[c]['kind'] in EVENT)
    sec20 = sum(c['sec'] for c in cuts if A[c['cid']]['kind'] in COUNT20)
    figs = [c for c in order if A[c]['kind'] in FIGS]
    fixed = sum(1 for c in order if A[c]['ga_new'].startswith('🔧'))
    frames = Counter(A[c]['frame'] for c in order if A[c]['kind'] in PICTURE)
    motions = Counter(A[c]['motion'].split('（')[0].split(' ')[0] for c in order if A[c]['kind'] in PICTURE)
    use, ji_use = defaultdict(list), defaultdict(list)
    for c in order:
        a = A[c]
        if a['kind'] in COUNT20:
            use[base(a['main'])].append(c)
        if a['ji']:
            ji_use[base(a['ji'])].append(c)
    ji0 = Counter(base(base_A[c]['ji']) for c in order if base_A[c]['ji'])
    L = ['---', 'title: 33本目 場面ごとの映像・写真の一覧（機械で組む）', 'created: 2026-11-14', 'tags: [project/jiko-kensho, ep33]', '---', '',
         '# 33本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % len(order), '',
         '> **機械で組む一覧＝手で直さない**。作り方＝`python -P -X utf8 ref/ep33/eizou_build/make_list33.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄＝土台・差し替え `eizou_build/over33.psv`・出どころ `eizou_build/sources33.psv`・決め `eizou_build/decisions33e.md`）。直すのは入力。',
         '> 秒＝%s（カットの頭・カッコはカットの秒）。🔧＝台本の画の欄から替えたカット（⑤b はこの一覧に従う・台本は直さない）。' % tnote +
         '色味は原本（10-07）・写真は画面いっぱい（10-11）・全面にできない点（BY-SA・縦長・紙面＝報告の図と文字の頁）は**高さいっぱいの額＋地は同じ絵のぼかし**（10-30）・額装はどれも静止（10-26）・衛星写真の額の地は方眼のまま（11-05）。'
         '説明カットの地＝写真を暗くするだけ・静止（§5b-117）＝**その場面の直前の写真**（11-14 の決まり＝下の「地の決まり」）・🔴 Google の衛星写真・夜や暗い絵・紙面は地にしない。'
         '🔴 **報告の夜の図は第三者のコマ＝紙面の引用**（図の番号と題の行ごと・額装・無加工・サムネに使わない）。見た画像の記録＝`src/look/seen_log.tsv`。🔴 撮影者の個人名はここに書かない（`{作者}`＝git の外の `src/credits_private.tsv` から ⑤b で差し込む）。Commons の点は [n]＝記号 C<n>（`src/commons/cand33.json` の通し番号）・紙面は F:<巻>-<図>・文字の頁は P:<カット>・イメージは X<カット>。',
         '', '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真・映像・紙面（§2-1 で数える） | **%d カット＝%.1f%%**（映像 %d・写真 %d・紙面 %d・衛星 %d・公的 %d・秒 %.0f＝%.1f%%）／台本の画の欄 %d（%.1f%%） | 20%%以上 ✅ |' % (
             n20, 100.0 * n20 / len(order), kinds['映像'], kinds['写真'], kinds['紙面'], kinds['衛星'], kinds['公的'], sec20, 100.0 * sec20 / total, n20_0, 100.0 * n20_0 / len(order)),
         '| そのうちこの火事の写真と映像（報告の夜の図・Commons・#15） | %d カット＝%.1f%% | 参考 |' % (n_event, 100.0 * n_event / len(order)),
         '| フリー素材（イメージ） | %d カット（20%% に数えない・⑤b で1本ずつ探す） | 人の顔・社名・字・機種なし・AI で作った絵なし・「イメージ」と出す |' % kinds['イメージ'],
         '| 図 | %d カット（模式 %d・ほか %d＝地はすべて写真）・模式の続き %d（台本の画の欄 %d） | 地は暗くするだけ・動かさない |' % (
             len(figs), kinds['模式'], len(figs) - kinds['模式'], runs(order, A), runs(order, base_A)),
         '| 見せ方（写真・映像・紙面・イメージ） | %s | 額装は静止 |' % '・'.join('%s %d' % kv for kv in frames.most_common()),
         '| 動き | %s | 全面は寄る／流す |' % '・'.join('%s %d' % kv for kv in motions.most_common()),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % fixed,
         '| 地の偏り | いちばん多い地 %d カット（台本の画の欄 %s） | 1点 %d カットまで |' % (
             max(len(v) for v in ji_use.values()) if ji_use else 0, '・'.join('%s %d' % kv for kv in ji0.most_common(3)), JI_MAX),
         '| 種類 | %s | — |' % '・'.join('%s %d' % kv for kv in kinds.most_common()),
         '| 合計 | %d カット・%s（%s・ed01 を除く） | — |' % (len(order), fmt(total), tnote), '',
         '### 章ごとの写真・映像・紙面（§2-1 は章ごとを見ない＝参考・20%% 未満の章に印）', '', '| 章 | カット | 写真・映像・紙面 | 割合 | イメージ | 図 |', '|---|---:|---:|---:|---:|---:|']
    for r in chap_rows(cuts, A):
        p = 100.0 * r['real'] / r['n']
        L.append('| %s | %d | %d | %s%.0f%% | %d | %d |' % (r['chap'], r['n'], r['real'], '⚠️ ' if p < 20 else '', p, r['img'], r['fig']))
    L += ['', '### 写真・紙面の使い回し（2回以上＝地は数えない・文字の頁と #15 は別の頁と秒）', '']
    rep = [(k, v) for k, v in use.items() if len(v) >= 2 and k not in FOOT and not S.get(k, {}).get('type', '').startswith(('public-page', 'google', 'stock'))]
    L += ['- %s（%s）＝%s' % (k, S[k]['title'][:40] if k in S else '?', ' '.join(v)) for k, v in sorted(rep)] or ['- なし']
    L += ['', '### 地に使った写真（説明カットの背景＝暗くするだけ・🅰＝地の決まりで機械が選んだ）', '']
    for k, v in sorted(ji_use.items(), key=lambda kv: -len(kv[1])):
        L.append('- %s（%s）＝%d カット：%s' % (k, S[k]['title'][:36] if k in S else '?', len(v), ' '.join(c + ('' if A[c].get('ji_auto') else '＊') for c in v)))
    L += ['', '（＊＝差し替えで地を決めたカット・ほかは地の決まり）', '']
    L += ['## §1 冒頭（c101〜c113）＝実写だけ（最初に設計した）', '', '| カット | 秒 | 語りの頭 | 画 |', '|---|---|---|---|']
    byid = {c['cid']: c for c in cuts}
    for cid in OPENING:
        c, a = byid[cid], A[cid]
        L.append('| %s | %s〜%s | %s | %s %s＝%s（%s・%s） |' % (cid, fmt(c['start']), fmt(c['start'] + c['sec']), c['head'], a['kind'], a['main'], a['sub'], a['frame'], a['motion']))
    L += ['', '## §2 章ごと・カットごと', '']
    chap = None
    for c in cuts:
        a = A[c['cid']]
        if c['chap'] != chap:
            chap = c['chap']
            L += ['', '### ' + chap, '', '| カット | 秒 | 語りの頭 | 種類 | 素材 | 地 | 見せ方 | 副題・札 | 動き | 🔧 | 備考 |', '|---|---|---|---|---|---|---|---|---|---|---|']
        L.append('| %s | %s（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            c['cid'], fmt(c['start']), c['sec'], c['head'], a['kind'], a['main'] or '—', (a['ji'] + ('' if not a['ji'] or a.get('ji_auto') else '＊')) or '—',
            a['frame'] or '—', a['sub'], a['motion'] or '—', a['ga_new'] or '—', (a['note'] + (' ［%s］' % a['mark'] if a['mark'] else '')) or '—'))
    L += ['', '## §3 素材の一覧（出どころ・権利・取得＝了承②の対象）', '',
          '| 記号 | 種類 | 群 | 見て確かめた中身 | 取り方 | 幅×高 | 権利 | 根拠 | 画面の出典の行 | 時点 | 人 | ファイル | 使うカット | 備考 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for code, s in sorted(S.items(), key=lambda kv: (kv[1]['type'], kv[0])):
        cs = [c for c in order if base(A[c]['main']) == code or base(A[c]['ji']) == code]
        if not cs and s['type'] in ('public-page', 'report-fig', 'stock', 'google'):
            continue
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            code, s['type'], s['grp'], s['title'], s['get'], s['dims'], s['rights'], s['basis'], s['credit'], s['era'],
            s['people'], s['file'] or '—', ' '.join(cs) or '（使わない）', s['note'] or '—'))
    L += ['', '## §4 門番', '', '- E %d 件' % len(E)] + ['  - 🔴 ' + x for x in E] + ['- ⚠️ %d 件' % len(W)] + ['  - ⚠️ ' + x for x in W]
    L += ['', '## §5 映像方針で決めたこと', '']
    if os.path.exists(DECIDE):
        L += [ln.rstrip('\n') for ln in open(DECIDE, encoding='utf-8')]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        f.write('cid\tchap\tstart\tsec\tkind\tmain\tji\tframe\tsub\tmotion\tfixed\tmark\tcard\tcont\n')
        for c in cuts:
            a = A[c['cid']]
            f.write('%s\t%s\t%.2f\t%.2f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.2f\t%.2f\n' % (c['cid'], c['chap'], c['start'], c['sec'], a['kind'], a['main'], a['ji'], a['frame'], a['sub'], a['motion'], '🔧' if a['ga_new'].startswith('🔧') else '', a['mark'], c.get('card', 0.0), c.get('cont', c['sec'])))
    return n20, len(order)


def selftest():
    def cut(cid, sec=1.0, chap='章'):
        return dict(cid=cid, chap=chap, lines=['あ'], chars=1, start=0.0, sec=sec, cont=sec, head='あ', ga='')
    row = lambda code, typ, rights, credit='出典', grp='', people='なし', era='', dims='1920×1080': dict(zip(SKEYS, [code, typ, grp, '', '', dims, rights, '', credit, era, people, '', '']))
    S = {'C28': row('C28', 'commons-photo', 'CC BY 2.0', era='2017-06-16 14:34'), 'C30': row('C30', 'commons-photo', 'CC BY-SA 2.0', era='2017-06-18 09:56'),
         'C7': row('C7', 'commons-photo', 'CC BY 4.0', grp='dawn night', era='2017-06-14・夜明け'), 'C39': row('C39', 'commons-photo', 'CC BY-SA 4.0', era='2024-06-07 21:44・夕方'),
         'C20': row('C20', 'commons-photo', 'CC BY 2.0', era='2018-07-13'), 'C70': row('C70', 'commons-photo', 'CC BY 2.0', era='2017-06-20 16:31', dims='1372×2182'),
         'SAT:x': row('SAT:x', 'google', 'Google'), 'P:c701': row('P:c701', 'public-page', 'OGL v3.0'),
         'F:P1V2-10.9': row('F:P1V2-10.9', 'report-fig', 'OGL v3.0（第三者のコマ・図を含む）', grp='night'), 'F:P1V1-6.7': row('F:P1V1-6.7', 'report-fig', 'OGL v3.0（第三者のコマ・図を含む）'),
         'V15': row('V15', 'commons-video', 'CC BY 3.0'), 'X306': row('X306', 'stock', 'Pexels', grp='stock night'), 'X704': row('X704', 'stock', 'Pexels', grp='stock'),
         'X906': row('X906', 'stock', 'Pexels', grp='stock screen')}
    fig = dict(kind='模式', main='', ji='C28', frame='—', sub='札', motion='', look='', ga_new='', note='', mark='')
    pho = dict(kind='写真', main='C28', ji='', frame='全面', sub='焼けた塔〈2017年6月16日〉', motion='ゆっくり寄る', look='', ga_new='', note='', mark='')
    sat = dict(pho, kind='衛星', main='SAT:x', frame='額装（衛星）', sub='衛星', motion='静止')
    pap = dict(pho, kind='紙面', main='F:P1V2-10.9', frame='額装（高さいっぱい）', motion='静止', sub='台所の窓から外へ出た炎〈1:09〉')

    def setup(extra):
        cuts = [cut(c) for c in OPENING] + [cut(c) for c in ('c201', 'c202')] + [cut(c) for c in extra if c not in OPENING]
        A = {c['cid']: dict(sat, cid=c['cid']) for c in cuts}
        return cuts, A

    def run(cid, r, name=''):
        cuts, A = setup([cid])
        A[cid] = dict(r, cid=cid)
        return gates(cuts, A, S, (name,) if name else ())[0]
    T = [
        ('陰性 模式（地 CC BY）', 'c701', fig, None),
        ('陰性 写真（日付が合う）', 'c701', pho, None),
        ('陰性 紙面（時刻が合う）', 'c701', pap, None),
        ('陽性 紙面の時刻が違う', 'c701', dict(pap, sub='台所の窓から外へ出た炎〈1:15〉'), '合わない'),
        ('陽性 紙面に時刻・確かめた時刻なし', 'c701', dict(pap, main='F:P1V1-6.7', sub='窓のまわり〈1:09〉'), '確かめたコマの時刻が無い'),
        ('陽性 紙面を全面', 'c701', dict(pap, frame='全面', motion='ゆっくり寄る'), '紙面・文字の頁は額装'),
        ('陽性 紙面を地に', 'c701', dict(fig, ji='F:P1V1-6.7'), '紙面・文字の頁を地に'),
        ('陽性 文字の頁に動き', 'c701', dict(pho, kind='公的', main='P:c701', frame='額装（高さいっぱい）', motion='ゆっくり寄る', sub='訳の札「…」'), '紙面・文字の頁は額装'),
        ('陽性 NG の点 [82]', 'c701', dict(pho, main='C82'), '使わないと決めた'),
        ('陽性 NG の点 [2]', 'c701', dict(pho, main='C2'), '使わないと決めた'),
        ('陽性 地が無い', 'c701', dict(fig, ji=''), '文字だけ'),
        ('陽性 Google を地に', 'c701', dict(fig, ji='SAT:x'), 'Google'),
        ('陽性 夜明けの写真を地に', 'c701', dict(fig, ji='C7'), '夜や暗い絵'),
        ('陽性 夜のイメージを地に', 'c701', dict(fig, ji='X306'), '夜や暗い絵'),
        ('陽性 画面のイメージを地に', 'c701', dict(fig, ji='X906'), '画面や書類'),
        ('陰性 昼のイメージを地に', 'c701', dict(fig, ji='X704'), None),
        ('陽性 BY-SA を地に', 'c701', dict(fig, ji='C30'), 'BY-SA の写真 C30 を地に'),
        ('陽性 BY-SA を全面', 'c701', dict(pho, main='C30', sub='焼けた塔〈2017年6月18日〉'), 'BY-SA の写真 C30 は額装'),
        ('陽性 副題の日付が違う', 'c701', dict(pho, sub='焼けた塔〈2017年6月17日〉'), '日付'),
        ('陽性 副題の年月が違う', 'c701', dict(pho, main='C20', sub='火事から1年の塔〈2018年6月〉'), '年月'),
        ('陽性 副題の夕方が無い', 'c701', dict(pho, sub='夕方の塔〈2017年6月16日〉'), '夕方'),
        ('陰性 夕方と書いて夕方の写真', 'c701', dict(pho, main='C39', frame='額装（高さいっぱい）', motion='静止', sub='駅から見た塔〈2024年6月〉'), None),
        ('陽性 額装に動き', 'c701', dict(pho, frame='額装（高さいっぱい）'), '額装に動き'),
        ('陽性 冒頭にイメージ', 'c105', dict(pho, kind='イメージ', sub='イメージ：空', main='X704'), '冒頭は実写'),
        ('陽性 冒頭に図', 'c113', dict(fig), '冒頭は実写'),
        ('陽性 イメージの副題', 'c701', dict(pho, kind='イメージ', sub='空', main='X704'), 'イメージの副題'),
        ('陽性 書かない名前', 'c701', dict(fig, note='山田太郎'), '書かない名前'),
        ('陽性 言わない語', 'c701', dict(fig, sub='犠牲になった人'), '言わない語'),
        ('陽性 素材の記号が未定', 'c701', dict(pho, main='?C'), '決まっていない'),
    ]
    bad = 0
    for label, cid, r, want in T:
        E = run(cid, r, name='山田太郎')
        hit = any(want in x for x in E) if want else not E
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E[:3]))
        bad += 0 if hit else 1
    # BY-SA は1点1カット・同じ写真に別の副題・写真3回
    cuts, A = setup(['c701', 'c702', 'c703'])
    A['c701'] = dict(pho, cid='c701', main='C30', frame='額装（高さいっぱい）', motion='静止', sub='焼けた塔〈2017年6月18日〉')
    A['c702'] = dict(pho, cid='c702', main='C30', frame='額装（高さいっぱい）', motion='静止', sub='塔〈2017年6月18日〉')
    E = gates(cuts, A, S)[0]
    hit = any('1点1カット' in x for x in E) and any('別の副題' in x for x in E)
    print(('OK  ' if hit else 'NG  ') + '陽性 BY-SA を2カット・別の副題' + ('' if hit else ' → %s' % E[:3]))
    bad += 0 if hit else 1
    cuts, A = setup(['c701', 'c702', 'c703'])
    for c in ('c701', 'c702', 'c703'):
        A[c] = dict(pho, cid=c)
    E = gates(cuts, A, S)[0]
    hit = any('を 3 回' in x for x in E)
    print(('OK  ' if hit else 'NG  ') + '陽性 同じ写真を3回' + ('' if hit else ' → %s' % E[:3]))
    bad += 0 if hit else 1
    # 映像の区間
    # 🔧 33本目 ⑤b-1：陰性「足りる」は1場面の中の区間に替えた（176.30〜187.45 を10秒使うと T1→T2 の切れ目 182.407 をまたぐ＝新しい門番が鳴る）
    for label, motion, sec, want in (('陰性 映像の区間 足りる', '映像 202.20〜209.20秒', 6.5, None), ('陽性 映像の区間 足りない', '映像 176.30〜181.00秒', 10.0, '足りない'),
                                     ('陽性 頭の黒に触れる', '映像 5.00〜20.00秒', 10.0, '外す秒'), ('陽性 窓の作業の人に触れる', '映像 180.00〜192.00秒', 10.0, '作業の人'),
                                     ('陽性 長さをこえる', '映像 245.00〜255.00秒', 9.0, '素材の長さ'),
                                     ('陽性 場面の切れ目をまたぐ（T6→T7）', '映像 209.55〜219.50秒', 7.57, '場面の切れ目 216.647'),
                                     ('陽性 区間の頭が前の場面（28.327 の手前）', '映像 28.00〜35.00秒', 6.5, '場面の切れ目 28.327'),
                                     ('陰性 切れ目の1コマ内側は通す', '映像 21.03〜28.28秒', 7.22, None)):
        c1 = cut('c701', sec)
        A1 = {'c701': dict(pho, cid='c701', kind='映像', main='V15', motion=motion, sub='焼けた塔〈2017年7月公開の映像〉')}
        E1, W1 = [], []
        gate_video([c1], A1, E1, W1)
        hit = any(want in x for x in E1) if want else not E1
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E1[:3]))
        bad += 0 if hit else 1
    # 🆕 33本目 ⑤b-1：決めて使う場面の替わり（ALLOW_CROSS）は通す／同じ区間でも名簿に無いカットは止める
    for cid, want in (('c109', None), ('c702', '場面の切れ目 182.407')):
        E1, W1 = [], []
        gate_video([cut(cid, 9.30)], {cid: dict(pho, cid=cid, kind='映像', main='V15', motion='映像 176.30〜187.45秒', sub='焼けた塔〈2017年7月公開の映像〉')}, E1, W1)
        hit = any(want in x for x in E1) if want else not E1
        print(('OK  ' if hit else 'NG  ') + ('陰性 決めた替わり（%s の T1→T2）' % cid if not want else '陽性 名簿に無いカットの T1→T2（%s）' % cid) + ('' if hit else ' → %s' % E1[:3]))
        bad += 0 if hit else 1
    cuts, A = setup(['c701', 'c702'])
    A['c701'] = dict(pho, cid='c701', kind='映像', main='V15', motion='映像 180.00〜192.00秒', sub='焼けた塔〈2017年7月公開の映像〉')
    A['c702'] = dict(pho, cid='c702', kind='映像', main='V15', motion='映像 190.00〜200.00秒', sub='焼けた塔〈2017年7月公開の映像〉')
    E = gates(cuts, A, S)[0]
    hit = any('重なる' in x for x in E)
    print(('OK  ' if hit else 'NG  ') + '陽性 映像の区間が重なる' + ('' if hit else ' → %s' % E[:3]))
    bad += 0 if hit else 1
    # 地の決まり（直前の写真＝章をまたぐ・夜は飛ばす・頭はあと・上限 JI_MAX）
    cuts = [cut('c300', chap='A'), cut('c301', chap='A'), cut('c302', chap='A'), cut('c303', chap='A'), cut('c304', chap='B'), cut('c305', chap='B')]
    A = {'c300': dict(fig, cid='c300', ji=''), 'c301': dict(pho, cid='c301'), 'c302': dict(fig, cid='c302', ji=''),
         'c303': dict(pho, cid='c303', kind='イメージ', main='X306', sub='イメージ：夜'),
         'c304': dict(fig, cid='c304', ji=''), 'c305': dict(pho, cid='c305', main='C70', sub='焼けた塔〈2017年6月20日〉')}
    assign_grounds(cuts, A, S, set())
    hit = A['c300']['ji'] == 'C28' and A['c302']['ji'] == 'C28' and A['c304']['ji'] == 'C28'
    print(('OK  ' if hit else 'NG  ') + '地の決まり（頭はあと・直前・夜を飛ばす・章をまたぐ）' + ('' if hit else ' → %s %s %s' % (A['c300']['ji'], A['c302']['ji'], A['c304']['ji'])))
    bad += 0 if hit else 1
    cuts = [cut('c301')] + [cut('c3%02d' % k) for k in range(2, 2 + JI_MAX + 1)] + [cut('c399')]
    A = {'c301': dict(pho, cid='c301'), 'c399': dict(pho, cid='c399', main='C70', sub='焼けた塔〈2017年6月20日〉')}
    for c in cuts[1:-1]:
        A[c['cid']] = dict(fig, cid=c['cid'], ji='')
    assign_grounds(cuts, A, S, set())
    got = Counter(A[c['cid']]['ji'] for c in cuts[1:-1])
    hit = got['C28'] == JI_MAX and got['C70'] == 1
    print(('OK  ' if hit else 'NG  ') + '地の上限 %d（こえたら次に近い写真）' % JI_MAX + ('' if hit else ' → %s' % dict(got)))
    bad += 0 if hit else 1
    for desc, want in (('札・地＝実写 写真 [28] を暗く', 'C28'), ('札・地＝実写 衛星 団地 を暗く', 'SAT:団地')):
        got = ji_code(desc)
        print(('OK  ' if got == want else 'NG  ') + '地の読み %s' % want + ('' if got == want else ' → %s' % got))
        bad += 0 if got == want else 1
    for ga, want in (('実写 紙面 P1V4 図22.8（…・副題「台所の窓のまわりの炎〈1:09〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 図22.8（2019）」）', ('紙面', 'F:P1V4-22.8')),
                     ('実写 公的 P1V4 ¶28.3 の頁（PDF p96・額装・訳の札「燃える外装」・出典の行「…」）', ('公的', 'P:c416')),
                     ('実写 映像 #15 焼けた塔A（3:00〜3:50・副題「焼けた塔〈2017年7月〉」）', ('映像', 'V15'))):
        a = parse_ga('c416', ga)
        hit = (a['kind'], a['main']) == want
        print(('OK  ' if hit else 'NG  ') + '画の欄の読み %s' % want[0] + ('' if hit else ' → %s %s' % (a['kind'], a['main'])))
        bad += 0 if hit else 1
    print('selftest %s' % ('ok' if not bad else 'NG %d' % bad))
    return 1 if bad else 0


def main():
    if '--selftest' in sys.argv:
        return selftest()
    cuts = read_cuts(DAIHON)
    over, bad1 = load_psv(OVER, KEYS)
    src, bad2 = load_psv(SOURCES, SKEYS)
    S = {s['code']: s for s in src}
    base_A, _, _ = assemble(cuts, [])
    auto_rows(base_A, S)
    if '--dump' in sys.argv:
        for c in cuts:
            a = base_A[c['cid']]
            print('|'.join([a['cid'], a['kind'], a['main'], a['ji'], a['frame'][:6], a['sub'][:34], a['motion'][:20], a['mark'], c['head'][:18]]))
        return 0
    A, bad3, fixed_ji = assemble(cuts, over)
    auto_rows(A, S)
    assign_grounds(cuts, A, S, fixed_ji)
    order = [c['cid'] for c in cuts]
    if '--ji' in sys.argv:
        for k, v in Counter(base(A[c]['ji']) for c in order if A[c]['ji']).most_common():
            print('%3d %s %s' % (v, k, S.get(k, {}).get('title', '?')[:30]))
        return 0
    if '--runs' in sys.argv:
        for lab, X in (('台本', base_A), ('一覧', A)):
            rr = [order[i - 1] + '→' + order[i] for i in range(1, len(order)) if X[order[i - 1]]['kind'] in FIG_RUN and X[order[i - 1]]['kind'] == X[order[i]]['kind']]
            print('%s %d: %s' % (lab, len(rr), ' '.join(rr)))
        return 0
    tnote = measured(cuts)
    E, W = gates(cuts, A, S, words(NAME_FILES))
    if len(order) != N_CUTS:
        E.append('カットの数 %d（%d のはず）' % (len(order), N_CUTS))
    gate_video(cuts, A, E, W)
    gate_hook(cuts, E)
    E = bad1 + bad2 + bad3 + E
    n, m = build(cuts, A, S, E, W, base_A, tnote)
    print('秒＝%s／合計 %s' % (tnote, fmt(sum(c['sec'] for c in cuts))))
    print('カット %d／写真・映像・紙面 %d（%.1f%%）／E %d ／⚠️ %d → %s' % (m, n, 100.0 * n / m, len(E), len(W), OUT_MD))
    for x in E[:80]:
        print('E ', x)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
