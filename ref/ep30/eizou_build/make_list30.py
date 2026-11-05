# -*- coding: utf-8 -*-
"""30本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-11-05・チャット5）。29本目 make_list29.py の型を事件の回（237カット）に合わせた。

  python -P ref/ep30/eizou_build/make_list30.py             一覧を書く（E があれば exit 1）
  python -P ref/ep30/eizou_build/make_list30.py --selftest  陽性・陰性の対照（門番が狙いの門で鳴ることを先に見る）
  python -P ref/ep30/eizou_build/make_list30.py --dump      台本の画の欄を読んだだけの形を出す（当て方の差し替えを書く前に見る）

入力：台本 第2版 ref/ep30/daihon_v2.md §4（語りの字数・秒＋画の欄＝当て方の土台）
      eizou_build/over30.psv（台本の画の欄から替えるカットだけ・11列＝「=」はそのまま）・eizou_build/sources30.psv（出どころ・13列）・eizou_build/decisions30.md（§5）
出力：ref/ep30/eizou_list30.md（手で直さない）・eizou_build/list30.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E カットの過不足／種類の名／素材の記号が sources30.psv に無い／使わないと決めた点（NG）を使った
  E 引用（東京消防庁・東京地下鉄・地元の個人）＝額装でない・動きがある・出典の行に「提供」が無い・地に使った（引用は本編の話している数秒だけ）
  E 公的（紙面）＝額装でない・動きがある・出典の行が無い
  E 額装に動き（10-26）／説明カットの地＝PDL1.0・CC BY・CC0・PD・Pexels でない（Google の衛星写真を地にしない）／図なのに地が無い
  E 夜の写真（#70・#72・#79）を c918〜c920 の外で使った／語りが朝の所に #81・#84 を地で／駅名の札が読める #71 を地で
  E 当日の陸自の写真を第2〜5章（c3〜c6）・第9〜11章（ca〜cc）の地に使った（§0-3 の17）
  E 冒頭（c101〜c107）が実写でない／イメージの副題が「イメージ」で始まらない
  E 同じ映像の区間を2回（『70年の歩み』は『平成6年』と同じ撮影＝使わない）
  E 同じ写真を3回以上・同じ写真に別の副題・この事件の写真と映像が 20% 未満
  E 書かない名前（src/names_private.txt）・線の語（src/line_words.txt）が副題と備考に
  ⚠️ 同じ写真を2回・2回が8カットより近い／写真の無い画面が5つ以上続く／札以外の図の型が続く／人の印（⑤b で原寸）／映像の区間と語りの秒の差
秒＝÷365 の見込み（⑤a のあと audio/narration.json の実測に替える＝make_list29.measured の型を ⑤b-1 で足す）。
"""
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
DAIHON = os.path.join(EP, 'daihon_v2.md')
OUT_MD = os.path.join(EP, 'eizou_list30.md')
OUT_TSV = os.path.join(HERE, 'list30.tsv')
OVER = os.path.join(HERE, 'over30.psv')
SOURCES = os.path.join(HERE, 'sources30.psv')
DECIDE = os.path.join(HERE, 'decisions30.md')
NAME_FILE = os.path.join(EP, 'src', 'names_private.txt')
LINE_FILE = os.path.join(EP, 'src', 'line_words.txt')
PUNCT = re.compile(r'[、。，．,.「」『』（）()？！?!…・\s　〈〉：:"“”]')
CUT = re.compile(r'^\*\*(c[0-9a-c]\d\d)\*\*(.*)$')
OPENING = ['c10%d' % i for i in range(1, 8)]
RATE = 365.0
PHOTO_LO = 0.20
GAP_MIN = 8
EVENT = ('陸自', '引用', '映像', '公立')      # この事件の写真と映像（20% に数える）
REAL = EVENT + ('公的', '衛星', '場所')       # 実写（紙面・衛星・語りに出る場所の写真を足す）
PICTURE = REAL + ('イメージ',)
FIGS = ('札', '模式', '無線帯', '言葉', '箱', '帯', '並べ', '棒', '年表', '表', '暦', '比べ', '窓口')
FIG_FREE = ('札', '模式', '無線帯', '言葉')    # 型を続けてよい（札の型＝1つの描き手）
JI_OK = ('PDL1.0', 'CC BY 2.0', 'CC BY 2.5', 'CC BY 3.0', 'CC BY 4.0', 'CC0', 'PD', '国土地理院', 'Pexels')
NIGHT = ('P70', 'P72', 'P79')
NIGHT_OK = ('c918', 'c919', 'c920')
NOT_JI = ('P81', 'P84', 'P71', 'P70', 'P72', 'P79')
NG = {
    'P59': '被害者が写る', 'P46': '被害者が写る', 'P47': '被害者が小さく写る', 'P48': '被害者が写る', 'P49': '被害者が写る',
    'P43': '手当てか片づけか分からない・被害を受けた職員の可能性＝Commons の写しの題（11-05 に見て外した）',
    'P30': '線', 'P33': '線', 'P34': '線', 'P35': '線', 'P36': '線', 'P37': '線', 'P38': '線',
    'P50': '宣伝に見える', 'P51': '宣伝に見える', 'P52': '宣伝に見える', 'P53': '宣伝に見える', 'P54': '宣伝に見える', 'P55': '宣伝に見える', 'P56': '宣伝に見える', 'P57': '宣伝に見える', 'P58': '宣伝に見える',
    'P82': '整列と敬礼＝④ で外した', 'P31': '弁護士一家の名前', 'P41': '弁護士一家の名前', 'P96': '機関紙', 'P97': '子ども向け教材', 'P100': '修行の器具', 'P101': '店舗',
    'P20': '白い筒が並ぶ＝中身が分からない（11-05）', 'P28': '白い筒が並ぶ＝中身が分からない（11-05）', 'P29': '工場の棟＝設備の話に近づく（11-05）',
    'M70': '『70年の歩み』は平成6年と同じ撮影＋隣が震災の場面＝同じ絵を別の素材で数えない（使うなら秒の換算の門番を通す）',
}
# 札の型にまとめない図（1枚ずつ描く）＝台本の「模式」のうち、形そのものが話になるカット。残りの模式は札の型＝見出し＋札1〜4枚＋矢印0〜2本＋誰の記録かの色（描き手1つ）
DRAWN = ('c202', 'c307', 'c315', 'c316', 'c407', 'c505', 'c506', 'c514', 'c519', 'c610', 'c611', 'c704', 'c706', 'c707', 'c719', 'c819', 'c906', 'cb07', 'cb08', 'cb12')
RADIO = ('c714', 'c715', 'c716', 'c718', 'c721', 'c730', 'c733', 'c734')    # 無線の帯＝同じ図が段ごとに伸びる（描き手1つ）
# 台本の「地＝イメージ〈…〉」→ 地の素材（語りに出る場所の写真が撮れている所は実写へ・ほかは同じ章のイメージと同じ絵）
GMAP = (('朝の霞が関の官庁街', 'KG1'), ('夜の東京の街', 'X618'), ('夜の住宅地', 'X404'), ('朝の大きな病院', 'SLH'), ('積まれた新聞', 'X512'), ('枯れた葉', 'X503'),
        ('東京のビル街', 'KS2'), ('救急外来の廊下', 'X803'), ('夜の机の上のノートパソコン', 'GPC'), ('冬の東京の夕方', 'X520'), ('神奈川の街', 'GA1'), ('朝の街', 'GA1'), ('冬の街', 'GA1'),
        ('朝の住宅地', 'GA2'), ('夜の高速道路', 'X609'), ('初夏の富士山', 'GF1'), ('富士山のふもと', 'GF1'), ('冬の晴れた信州', 'X513'), ('信州の山と街', 'MT'), ('病院の処置室', 'X809'),
        ('窓のないホール', 'X813'), ('病院の長い廊下', 'X812'), ('病院の廊下', 'X803'), ('熊本の山林', 'GK1'), ('無人の事務室', 'X705'), ('点滴の管', 'X905'), ('朝の電車の窓', 'Xc02'),
        ('朝の路地', 'HB'), ('朝の地下鉄の駅の通路', 'X703'), ('救急車の後ろの扉', 'X806'), ('夜の警察署', 'X404'))
KEYS =['cid', 'kind', 'main', 'ji', 'frame', 'sub', 'motion', 'look', 'ga_new', 'note', 'mark']
SKEYS = ['code', 'type', 'grp', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
PB = (('白書 第3節', 'W3'), ('白書 第5節', 'W5'), ('判決 判T', 'JT'), ('判決 判C', 'JC'), ('国会会議録', 'KK'), ('消防庁の資料', 'FD1'), ('消防庁の通知', 'FD2'),
      ('公安調査庁の年表', 'PA1'), ('特集ページ', 'PA2'), ('公安調査庁の発表', 'PA3'), ('公安調査庁のアーカイブ', 'PA4'))
MOTIONS = ('静止に近い寄り', 'ゆっくり寄る', 'ゆっくり引く', '左へ流す', '右へ流す', '静止')


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


def ji_code(desc):
    m = re.search(r'地＝写真 #(\d+)', desc)
    if m:
        return 'P' + m.group(1)
    m = re.search(r'地＝イメージ〈([^〉]*)〉', desc)
    if m:
        return next((c for w, c in GMAP if m.group(1).startswith(w)), 'G:' + m.group(1))
    m = re.search(r'地＝衛星 ?([^（・）]*)', desc)
    if m:
        return 'SAT:' + m.group(1).strip()
    return ''


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
        a['sub'] = re.sub(r'・?地＝[^・）]*(?:（[^）]*）)?[^・）]*', '', desc).strip('・ ')
        return a
    tok = rest.split('（')[0].split()
    k = tok[0] if tok else ''
    a['kind'] = k
    num = re.search(r'#(\d+)', rest.split('（')[0])
    if k == '映像':
        a['main'] = {'防衛6': 'M6', '防衛70': 'M70'}.get(tok[1] if len(tok) > 1 else '', '?')
        a['motion'], a['frame'] = '映像', '額装（高さいっぱい）'
    elif k == '衛星':
        a['main'] = 'SAT:' + ' '.join(tok[1:])
        a['frame'] = '額装（衛星）'
        a['motion'] = '静止'
    elif k == '公的':
        name = ' '.join(tok[1:])
        a['main'] = next((c for w, c in PB if name.startswith(w)), '?' + name)
        a['frame'] = '額装（高さいっぱい）'
        a['motion'] = '静止'
        cr = re.search(r'出典の行「([^」]*)」', desc)
        a['sub'] = a['sub'] or (cr.group(1) if cr else name)
    elif num:
        a['main'] = 'P' + num.group(1)
    elif '立入検査' in rest:
        a['main'] = 'INS?'
    if k in ('陸自', '引用', '公立'):
        a['frame'] = '額装（高さいっぱい）' if ('額装' in desc or '高さいっぱいの額' in desc) else '全面'
        a['motion'] = '静止' if a['frame'].startswith('額装') else next((w for w in MOTIONS if w in desc), 'ゆっくり寄る')
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
        c['head'] = ''.join(c['lines'])[:20]
        t += c['sec']
    return cuts


def base(code):
    return (code or '').split('=')[0].strip()


def words(path):
    if not os.path.exists(path):
        return []
    return [w.strip() for w in open(path, encoding='utf-8') if w.strip() and not w.startswith('#')]


def assemble(cuts, over):
    A = {}
    for c in cuts:
        a = parse_ga(c['cid'], c['ga'])
        if a['kind'] == '模式':
            a['kind'] = '無線帯' if c['cid'] in RADIO else ('模式' if c['cid'] in DRAWN else '札')
        A[c['cid']] = a
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
    """「映像 17:43〜17:49＋17:57〜18:03」→ [(1063, 1069), (1077, 1083)]。区間を書いていなければ空"""
    return [(int(a) * 60 + int(b), int(c) * 60 + int(d)) for a, b, c, d in re.findall(r'(\d+):(\d\d)〜(\d+):(\d\d)', motion or '')]


def stock_rows(A, S):
    """台本のイメージ（X…）は素材の表に1行ずつ足す＝⑤b で Pexels を1本ずつ探す"""
    for cid, a in A.items():
        if a['kind'] == 'イメージ' and base(a['main']) not in S:
            S[base(a['main'])] = dict(zip(SKEYS, [base(a['main']), 'stock', 'stock', a['sub'], '⑤b で Pexels を1本ずつ（原寸で見る）', '—', 'Pexels', 'Pexels のライセンス＝頁を credits に', 'イメージ（Pexels）', '現在', 'なし（顔・ナンバー・店の字なし）', '', '']))


def gates(cuts, A, S, name_list=(), line_list=()):
    E, W = [], []
    order = [c['cid'] for c in cuts]
    byid = {c['cid']: c for c in cuts}
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
                E.append('%s 素材 %s が sources30.psv に無い' % (cid, code))
        for c2 in (code, ji):
            if c2 in NG:
                E.append('%s 使わないと決めた点 %s を使った（%s）' % (cid, c2, NG[c2]))
        frame, motion = a['frame'], a['motion']
        if k == '引用':
            if not frame.startswith('額装') or motion != '静止':
                E.append('%s 引用は額装・静止（%s・%s）' % (cid, frame, motion))
            if s and '提供' not in s['credit']:
                E.append('%s 引用の出典の行に「提供」が無い（%s）' % (cid, s['credit']))
        if s and 'SA' in s['rights'] and (not frame.startswith('額装') or motion != '静止'):
            E.append('%s BY-SA の写真 %s は額装・静止（%s・%s）' % (cid, code, frame, motion))
        if k == '公的' and (not frame.startswith('額装') or motion != '静止'):
            E.append('%s 公的な機関の頁は額装・静止（%s・%s）' % (cid, frame, motion))
        if k == '公的' and s and not s['credit']:
            E.append('%s 公的な機関の頁の出典の行が無い' % cid)
        if frame.startswith('額装') and k != '映像' and motion not in ('静止',):
            E.append('%s 額装に動き（%s）＝額装は静止' % (cid, motion))
        if k == 'イメージ' and not a['sub'].startswith('イメージ'):
            E.append('%s イメージの副題が「イメージ」で始まらない' % cid)
        if k in FIGS:
            if not ji:
                E.append('%s 図（%s）なのに地の写真が無い＝文字だけの画面' % (cid, k))
            else:
                sj = S.get(ji)
                if not sj:
                    E.append('%s 地 %s が sources30.psv に無い' % (cid, ji))
                elif sj['rights'] not in JI_OK or sj['type'].startswith('quote'):
                    E.append('%s 地 %s が地に使える権利でない（%s・%s）' % (cid, ji, sj['type'], sj['rights']))
                if ji.startswith('SAT'):
                    E.append('%s Google の衛星写真を地にした（暗くすると見た目を変える＝決まりと当たる）' % cid)
                if ji in NOT_JI:
                    E.append('%s 地に %s（夜の写真・語りの朝に当てない点・駅名の札）' % (cid, ji))
                if ji.startswith('P') and ji[1:].isdigit() and 62 <= int(ji[1:]) <= 84 and cid[1] in '3456abc':
                    E.append('%s 当日の陸自の写真 %s を第2〜5章・第9〜11章の地に使った' % (cid, ji))
        if code in NIGHT and cid not in NIGHT_OK:
            E.append('%s 夜の写真 %s を c918〜c920 の外で使った' % (cid, code))
        if cid in OPENING and k not in REAL:
            E.append('%s 冒頭は実写だけ（%s）' % (cid, k))
        if k == '映像':
            win = windows(motion)
            if not win:
                W.append('%s 映像の区間が未定（%s）' % (cid, code))
            else:
                spans += [(cid, w) for w in win]
                rate = re.search(r'（([\d.]+)倍速）', motion)
                length = sum(w[1] - w[0] for w in win) / (float(rate.group(1)) if rate else 1.0)
                need = byid[cid]['sec']
                if length + 0.5 < need:
                    W.append('%s 映像の区間 %.1f秒が語り %.1f秒より短い（止めるか別の区間を足す＝⑤b-1）' % (cid, length, need))
                if rate:
                    W.append('%s 映像が等速でない（%s倍速）' % (cid, rate.group(1)))
        for fld in ('sub', 'note', 'ga_new'):
            for nm in name_list:
                if nm and nm in a[fld]:
                    E.append('%s 書かない名前が %s の欄に' % (cid, fld))
            for w in line_list:
                if w and w in a[fld]:
                    E.append('%s 線の語が %s の欄に' % (cid, fld))
        if k in REAL and s:
            use[code].append(cid)
            subs[code].add(a['sub'])
            if s['people'] and not s['people'].startswith(('なし', '—')):
                W.append('%s %s 人＝%s' % (cid, code, s['people']))
    spans.sort(key=lambda x: x[1][0])
    for (c1, s1), (c2, s2) in zip(spans, spans[1:]):
        if s2[0] < s1[1] - 0.5:
            E.append('映像の区間が重なる（同じ撮影）: %s %d〜%d と %s %d〜%d' % (c1, s1[0], s1[1], c2, s2[0], s2[1]))
    for code, cids in use.items():
        s = S[code]
        if s['type'].startswith(('stock', 'public-page', 'public-pdf', 'google')) or code.startswith(('M6', 'M70')):
            continue
        if 'SA' in s['rights'] and len(cids) > 1:
            E.append('BY-SA の写真 %s を %d カット（1点1カット）: %s' % (code, len(cids), ' '.join(cids)))
        if len(cids) >= 3:
            E.append('同じ写真 %s を %d 回: %s' % (code, len(cids), ' '.join(cids)))
        elif len(cids) == 2:
            gap = abs(order.index(cids[1]) - order.index(cids[0]))
            W.append('同じ写真 %s を2回: %s%s' % (code, ' '.join(cids), '（%dカット差＝近い）' % gap if gap < GAP_MIN else ''))
        if len(subs[code]) > 1:
            E.append('同じ写真 %s に別の副題: %s' % (code, ' ／ '.join(sorted(subs[code]))))
    n_event = sum(1 for cid in order if A[cid]['kind'] in EVENT)
    if order and n_event / len(order) < PHOTO_LO:
        E.append('この事件の写真と映像が %d／%d＝%.1f%%（20%% 以上）' % (n_event, len(order), 100.0 * n_event / len(order)))
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


def build(cuts, A, S, E, W):
    order = [c['cid'] for c in cuts]
    total = sum(c['sec'] for c in cuts)
    kinds = Counter(A[c]['kind'] for c in order)
    n_event = sum(1 for c in order if A[c]['kind'] in EVENT)
    n_real = sum(1 for c in order if A[c]['kind'] in REAL)
    sec_event = sum(c['sec'] for c in cuts if A[c['cid']]['kind'] in EVENT)
    figs = [c for c in order if A[c]['kind'] in FIGS]
    fixed = sum(1 for c in order if A[c]['ga_new'].startswith('🔧'))
    frames = Counter(A[c]['frame'] for c in order if A[c]['kind'] in PICTURE)
    motions = Counter(A[c]['motion'].split(' ')[0] for c in order if A[c]['kind'] in PICTURE)
    use, ji_use = defaultdict(list), defaultdict(list)
    for c in order:
        a = A[c]
        if a['kind'] in REAL:
            use[base(a['main'])].append(c)
        if a['ji']:
            ji_use[base(a['ji'])].append(c)
    L = ['---', 'title: 30本目 場面ごとの映像・写真の一覧（機械で組む）', 'created: 2026-11-05', 'tags: [project/jiko-kensho, ep30]', '---', '',
         '# 30本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % len(order), '',
         '> **機械で組む一覧＝手で直さない**。作り方＝`python -P ref/ep30/eizou_build/make_list30.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄＝土台・差し替え `eizou_build/over30.psv`・出どころ `eizou_build/sources30.psv`・決め `eizou_build/decisions30.md`）。直すのは入力。',
         '> 秒＝÷365 の見込み（⑤a のあと実測に替える）。🔧＝台本の画の欄から替えたカット（⑤b はこの一覧に従う・台本は直さない）。色味は原本（10-07）・写真は画面いっぱい（10-11）・全面にできない点（引用・縦長・4:3 の映像）は**高さいっぱいの額＋地は同じ絵のぼかし**（10-30）・額装はどれも静止（10-26）。説明カットの地＝写真を暗くするだけ・静止（§5b-117）。見た画像の記録＝`src/seen_log.tsv`（映像方針の印）。🔴 撮影者と提供者の個人名はここに書かない（`{作者}`・`{個人}`＝git の外の `src/credits_private.tsv` から ⑤b で差し込む）。',
         '', '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| この事件の写真と映像 | **%d カット＝%.1f%%**（陸自 %d・引用 %d・映像 %d・公立 %d・秒 %.0f＝%.1f%%） | 20%%以上 ✅ |' % (
             n_event, 100.0 * n_event / len(order), kinds['陸自'], kinds['引用'], kinds['映像'], kinds['公立'], sec_event, 100.0 * sec_event / total),
         '| 実写の全部（＋紙面 %d・衛星 %d・語りに出る場所 %d） | %d カット＝%.1f%% | — |' % (kinds['公的'], kinds['衛星'], kinds['場所'], n_real, 100.0 * n_real / len(order)),
         '| フリー素材（イメージ） | %d カット（20%% に数えない・⑤b で1本ずつ探す） | 人の顔・ナンバー・店の名前・読める画面の字なし・AI で作った絵なし・「イメージ」と出す |' % kinds['イメージ'],
         '| 図 | %d カット（札 %d・模式 %d・無線帯 %d・言葉 %d・ほか %d＝地はすべて写真） | 札の型は描き手1つ（§5）・地は暗くするだけ・動かさない |' % (
             len(figs), kinds['札'], kinds['模式'], kinds['無線帯'], kinds['言葉'], len(figs) - kinds['札'] - kinds['模式'] - kinds['無線帯'] - kinds['言葉']),
         '| 文字だけ | 0 カット（紙面 %d は語りが資料を名指しする所だけ） | 2割まで・3つ続けない |' % kinds['公的'],
         '| 見せ方（写真と紙面） | %s | 額装は静止 |' % '・'.join('%s %d' % kv for kv in frames.most_common()),
         '| 写真の動き | %s | 全面は寄る／流す |' % '・'.join('%s %d' % kv for kv in motions.most_common()),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % fixed,
         '| 種類 | %s | — |' % '・'.join('%s %d' % kv for kv in kinds.most_common()),
         '| 合計 | %d カット・%s（÷365・ed01 を除く） | — |' % (len(order), fmt(total)), '',
         '### 写真の使い回し（全面・額装で2回以上＝地は数えない）', '']
    rep = [(k, v) for k, v in use.items() if len(v) >= 2 and not k.startswith(('M6', 'M70'))]
    L += ['- %s（%s）＝%s' % (k, S[k]['title'] if k in S else '?', ' '.join(v)) for k, v in sorted(rep)] or ['- なし']
    L += ['', '### 地に使った写真（説明カットの背景＝暗くするだけ）', '']
    L += ['- %s（%s）＝%s' % (k, S[k]['title'] if k in S else '?', ' '.join(v)) for k, v in sorted(ji_use.items())]
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
        f.write('cid\tchap\tstart\tsec\tkind\tmain\tji\tframe\tsub\tmotion\tfixed\tmark\n')
        for c in cuts:
            a = A[c['cid']]
            f.write('%s\t%s\t%.2f\t%.2f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (c['cid'], c['chap'], c['start'], c['sec'], a['kind'], a['main'], a['ji'], a['frame'], a['sub'], a['motion'], '🔧' if a['ga_new'].startswith('🔧') else '', a['mark']))
    return n_event, len(order)


def selftest():
    def cut(cid):
        return dict(cid=cid, chap='章', lines=['あ'], chars=1, start=0.0, sec=1.0, head='あ', ga='')
    S = {
        'P65': dict(zip(SKEYS, ['P65', 'public-photo', '', '', '', '', 'PDL1.0', '', '出典', '', 'なし', '', ''])),
        'P70': dict(zip(SKEYS, ['P70', 'public-photo', '', '', '', '', 'PDL1.0', '', '出典', '', 'なし', '', ''])),
        'P62': dict(zip(SKEYS, ['P62', 'public-photo', '', '', '', '', 'PDL1.0', '', '出典', '', 'なし', '', ''])),
        'P60': dict(zip(SKEYS, ['P60', 'quote-photo', '', '', '', '', '引用', '', '提供：東京消防庁', '', 'なし', '', ''])),
        'P5': dict(zip(SKEYS, ['P5', 'quote-photo', '', '', '', '', '引用', '', '資料館の表示', '', 'なし', '', ''])),
        'SAT:x': dict(zip(SKEYS, ['SAT:x', 'google', '', '', '', '', 'Google', '', 'Google', '', 'なし', '', ''])),
        'M6': dict(zip(SKEYS, ['M6', 'commons-video', '', '', '', '', 'CC BY 3.0', '', '出典', '', 'なし', '', ''])),
        'M70': dict(zip(SKEYS, ['M70', 'commons-video', '', '', '', '', 'CC BY 3.0', '', '出典', '', 'なし', '', ''])),
    }
    ok = dict(kind='札', main='', ji='P65', frame='—', sub='札', motion='', look='', ga_new='', note='', mark='')
    photo = dict(kind='陸自', main='P65', ji='', frame='全面', sub='除染', motion='ゆっくり寄る', look='', ga_new='', note='', mark='')

    sat = dict(photo, kind='衛星', main='SAT:x', frame='額装（衛星）', motion='静止')

    def setup(extra):
        cuts = [cut(c) for c in OPENING] + [cut(c) for c in ('c201', 'c202', 'c203')] + [cut(c) for c in extra if c not in OPENING]
        A = {c['cid']: dict(sat, cid=c['cid']) for c in cuts}
        A['c201'] = dict(photo, cid='c201')          # 20% を満たす2カット（同じ写真2回＝⚠️ だけ）
        A['c202'] = dict(photo, cid='c202')
        A['c203'] = dict(photo, cid='c203', main='P62')
        return cuts, A

    def run(cid, row, name='', line=''):
        cuts, A = setup([cid])
        A[cid] = dict(row, cid=cid)
        return gates(cuts, A, S, (name,) if name else (), (line,) if line else ())[0]
    T = [
        ('陰性 札', 'c701', ok, None),
        ('陽性 NG の点', 'c701', dict(photo, main='P59'), '使わないと決めた'),
        ('陽性 地が無い', 'c701', dict(ok, ji=''), '文字だけ'),
        ('陽性 Google を地に', 'c701', dict(ok, ji='SAT:x'), 'Google'),
        ('陽性 当日の陸自を第3章の地に', 'c401', dict(ok, ji='P62'), '当日の陸自'),
        ('陰性 当日の陸自を第6章の地に', 'c701', dict(ok, ji='P62'), None),
        ('陽性 夜の写真を朝に', 'c701', dict(photo, main='P70'), '夜の写真'),
        ('陽性 夜の写真を地に', 'c701', dict(ok, ji='P70'), '地に P70'),
        ('陽性 引用を全面', 'c701', dict(photo, kind='引用', main='P60'), '引用は額装'),
        ('陽性 引用に提供なし', 'c701', dict(photo, kind='引用', main='P5', frame='額装（高さいっぱい）', motion='静止'), '提供'),
        ('陽性 引用を地に', 'c701', dict(ok, ji='P60'), '地に使える権利'),
        ('陽性 額装に動き', 'c701', dict(photo, frame='額装（高さいっぱい）'), '額装に動き'),
        ('陽性 冒頭にイメージ', 'c101', dict(photo, kind='イメージ', sub='イメージ：朝', main='P65'), '冒頭は実写'),
        ('陽性 書かない名前', 'c701', dict(ok, note='山田'), '書かない名前'),
    ]
    bad = 0
    for label, cid, row, want in T:
        E = run(cid, row, name='山田')
        hit = any(want in x for x in E) if want else not E
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E[:3]))
        bad += 0 if hit else 1
    # 映像の区間の重なり（同じ素材を2回）＝陽性と、離れていれば鳴らない陰性
    for label, second, want in (('陽性 映像の区間が重なる', '映像 17:40〜17:46', True), ('陰性 映像の区間が離れている', '映像 18:03〜18:12', False)):
        cuts, A = setup(['c702'])
        A['c101'] = dict(photo, cid='c101', kind='映像', main='M6', frame='全面', motion='映像 17:35〜17:43')
        A['c702'] = dict(photo, cid='c702', kind='映像', main='M6', frame='全面', motion=second)
        E = gates(cuts, A, S)[0]
        hit = any('重なる' in x for x in E) == want
        print(('OK  ' if hit else 'NG  ') + label + ('' if hit else ' → %s' % E[:3]))
        bad += 0 if hit else 1
    print('selftest %s' % ('ok' if not bad else 'NG %d' % bad))
    return 1 if bad else 0


def main():
    if '--selftest' in sys.argv:
        return selftest()
    cuts = read_cuts(DAIHON)
    over, bad1 = load_psv(OVER, KEYS)
    if '--dump' in sys.argv:
        A, _ = assemble(cuts, [])
        for c in cuts:
            a = A[c['cid']]
            print('|'.join([a['cid'], a['kind'], a['main'], a['ji'], a['frame'], a['sub'][:60], a['motion']]))
        return 0
    src, bad2 = load_psv(SOURCES, SKEYS)
    S = {s['code']: s for s in src}
    A, bad3 = assemble(cuts, over)
    stock_rows(A, S)
    E, W = gates(cuts, A, S, words(NAME_FILE), words(LINE_FILE))
    E = bad1 + bad2 + bad3 + E
    n, m = build(cuts, A, S, E, W)
    print('カット %d／この事件の写真と映像 %d（%.1f%%）／E %d ／⚠️ %d → %s' % (m, n, 100.0 * n / m, len(E), len(W), OUT_MD))
    for x in E[:40]:
        print('E ', x)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
