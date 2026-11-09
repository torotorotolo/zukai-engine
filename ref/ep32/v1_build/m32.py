# -*- coding: utf-8 -*-
"""32本目 台本の机上の数え（31本目の m31.py を写し、32本目＝USエアウェイズ1549便・A 枠・36分30秒・12章と、この回の網に替えた）。

  python -P ref/ep32/v1_build/m32.py ref/ep32/daihon_v1.md --roles ref/ep32/v1_build/roles.tsv
  python -P ref/ep32/v1_build/m32.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×9.125秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真と映像（画の欄の頭が「実写」＝映像・写真・調査・衛星・公的の内わけ）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ絵の2回使い・
この回の網（kousei.md の線・materials.md §1〜§4・§10）：
  ・名前（git の外の src/names_private.txt と names_commons.txt の語＝E・英字は大文字小文字を区別しない）・敬称の網（さん・くん・ちゃん・氏 を W）
  ・冒頭（c1）は実写だけ（E）
  ・VTS の映像＝台帳の区間の名（実写 映像 VTS 〈名〉）・副題が要る・副題にカメラの時計の時刻を書かない（E）・同じ区間を2回使わない（W）
  ・Commons の写真＝番号 [n]。使わない点（[10]・[28]〜[30]・[58]・[71]・[72]＝E）・BY-SA は 額装・無加工 が無ければ E・地にしたら E・
    名前の字を切る点（[47]・[48]・[61]）は「切」が無ければ E・同じ写真の束（[17][18]／[19][27]／[20][22]〜[26]）の2回使いは W
  ・ドケットの調査の写真（実写 調査 #N）＝額装が要る・当日の写真（#49 写真1〜18・#76 p20上／p31上・#68 写真1・2・#104・#77／#82 図1）は E
  ・紙面（実写 公的）は 額装・出典 が無ければ E・報告書の図2 は E
  ・言わない語（当たったら人が文脈を見る W）・言わない形（着水ボタンを押した・乗員を責める形・「約3分」で最初の船 ほか）
  ・帰属（シミュレーターの数＝報告書・着水ボタン＝副操縦士の聴取・偶然＝報告書・奇跡＝知事〈報道〉ほか＝同じカットに出どころの語が要る W）
  ・時点の言い切り（まだ・いまも ほか＝同じカットに日付が要る W）・地＝写真（「図」は「地＝」が無ければ W）・です・ます（最後の問いのカットのほかは W）
⚠️ check_script の尺の式は ElevenLabs／Otani の定数のまま＝ゆっくりの回は信じない（ルール §5a-28b）。尺はこの道具の②で見る。
"""
import collections
import importlib.util
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
import check_script as CS          # noqa: E402  parse・clean を使う（道具は直さない）
import check_listener as CL        # noqa: E402  judge をそのまま呼ぶ
import speaker                     # noqa: E402

PUNCT = set('、。？！「」（）・')
CPM = 365.0
SEC_PER_CUT = 9.125                # kousei.md §0（36.5分÷240カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（26本目の④で数えた値・31本目も同じ）
TARGET = 13320                     # kousei.md §0（ed01 こみ・36分30秒）
LO, HI = 13120, 13520              # kousei.md §3 の注＝13,320±200
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで
LAST_CUT = 'cc10'                  # 最後の問いのカット（です・ます はここだけ）
# kousei.md §3（cc は 550 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 730, 'c2': 910, 'c3': 1280, 'c4': 1280, 'c5': 1460, 'c6': 1640, 'c7': 1280, 'c8': 1280,
             'c9': 1100, 'ca': 910, 'cb': 910, 'cc': 504}
CH_CUTS = {'c1': 13, 'c2': 17, 'c3': 23, 'c4': 23, 'c5': 26, 'c6': 30, 'c7': 23, 'c8': 23, 'c9': 20, 'ca': 16,
           'cb': 16, 'cc': 10}
CH_Q = {'c1': 3, 'c2': 4, 'c3': 6, 'c4': 6, 'c5': 7, 'c6': 7, 'c7': 6, 'c8': 6, 'c9': 5, 'ca': 4, 'cb': 4, 'cc': 3}
# materials.md §8 の見込みを章へ割った目安（W は出さない）
CH_PHOTO = {'c1': 13, 'c2': 5, 'c3': 6, 'c4': 5, 'c5': 4, 'c6': 6, 'c7': 7, 'c8': 9, 'c9': 10, 'ca': 5, 'cb': 4,
            'cc': 5}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す
TEMPLATE = {'帯', '年表', '暦', '時計', '地図', '棒', '線', '箱', '札', '流れ', '比べ', '並べ', '割合', '窓口',
            '問答', '条文', '言葉', '式', '表', '方位'}
# VTS の区間の名（materials.md §2＝CrashAndRescue・After15Minutes・After20Minutes。FirstFerry は CrashAndRescue と重なる＝使わない）
CLIPS_OK = {'着水', '浮かぶ機体', '引き', '周り', '最初のフェリー', '横付けA', '横付けB', '横付けC', '横付けD', '15分後',
            '20分後A', '20分後B'}
BYSA = {28, 29, 30, 34, 44, 45, 46, 51, 53, 54, 55, 56, 57, 58, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72}
PHOTO_NG = {10: '上着に個人の名前', 28: '中身を見本帳で確かめていない', 29: '中身を見本帳で確かめていない',
            30: '中身を見本帳で確かめていない', 58: '題と中身が別物', 71: '私人の顔の近景（BY-SA）', 72: '私人の顔の近景（BY-SA）'}
CROP_NEED = {47: '札の発見者の名前', 48: '札の発見者の名前', 61: '袋の手書きの名前'}
SAME_PHOTO = [{17, 18}, {19, 27}, {20, 22, 23, 24, 25, 26}]
DOCK_NG = [(r'#49 ?写真([1-9]|1[0-8])(?![0-9])', '#49 の写真1〜18＝当日の避難（撮影者が NTSB の外）'),
           (r'#76 ?p(20|31) ?上', '#76 p20上・p31上＝当日の写真（撮影者の記載なし）'),
           (r'#68 ?写真[12](?![0-9])', '#68 の写真1・2＝当日（撮影者の記載なし）'),
           (r'#104', '#104＝BEA の映像の解析のコマ（持ち主が分からない）'),
           (r'#(77|82) ?図 ?1(?![0-9])', '#77・#82 の図1＝当日')]
# 言わない語（kousei.md の線・§B4・§4-13 波ダッシュ）。当たったら人が文脈を見る（W）
NG = ['犠牲', '死亡', '208', '墜落', '奇跡的', '拒否', '噂', '英雄', '衝撃', '瞬間', '最悪', '史上', '地獄', '闇', '〜', '～',
      '8.5マイル', 'マイナス7度の川', 'ピア88', 'Pier 88']
NG_RE = [(r'着水.{0,8}ボタン.{0,12}(押した|押して(?!いな)|押され)', '着水ボタンは押していない（副操縦士の聴取）'),
         (r'(機長|副操縦士|管制官|客室乗務員|乗員).{0,12}(ミス|失敗|過失|落ち度|せいで)', '乗員と管制官を責める形にしない（報告書の帰属で）'),
         (r'(全員|155人).{0,6}(無傷|けが(が|は)?(な|無)かった)', '重いけがの人は5人（全員が無傷ではない）'),
         (r'約?3分(で|後に?|ほどで)(最初の)?(船|フェリー)', '最初の船は約4分（3分57秒・計算）'),
         (r'(ラガーディア|空港)から.{0,4}(8\.5|13\.7)', '「LGA から8.5マイル」は使わない（sources.md §4-3）'),
         (r'(全員|155人).{0,8}救命胴衣を(着|つけ)', '救命胴衣を着水の前に着けたのは2人')]
# 帰属（同じカットの中に出どころの語が要る数と見方）
ATTR = [(r'着水.{0,3}ボタン.{0,10}押(した|して|さな|さず)', r'聴取|副操縦士|話し', '着水ボタン＝副操縦士の聴取（ドケット #7・報告書の本文に無い）'),
        (r'15回のうち|53%|53パーセント|のうち8回', r'シミュレーター|試し|報告書|NTSB', 'シミュレーターの数＝報告書 p50'),
        (r'35秒', r'シミュレーター|試し|報告書|NTSB|遅らせ', '35秒遅らせた1回＝報告書 p50・p89'),
        (r'偶然', r'報告書|NTSB', '一連の偶然＝報告書 p79・推定原因'),
        (r'奇跡', r'知事|呼び名|報道|映画|報告書|題|呼ばれ', '「奇跡」は呼び名＝知事（報道）・報告書は使わない'),
        (r'3\.6倍|3倍', r'報告書|認証|前提|設計|計算|表', '沈む速さ＝報告書の表2'),
        (r'5\.2', r'水温|水', '水温5.2℃＝報告書 p24'),
        (r'マイナス7|−7|-7|マイナス6', r'気温|セントラルパーク|空気', '−6／−7℃は気温（セントラルパーク）'),
        (r'34本|35本|で閉じ|閉じている|閉じた', r'2026年|勧告|NTSB|記録', '勧告の状態＝2026年11月の CAROL'),
        (r'受け入れられ', r'NTSB|勧告', 'NTSB の評価'),
        (r'14キロ', r'座標|計算|まっすぐ', '衝突点→着水点＝座標から計算（sources.md §4-3）'),
        (r'約20分', r'報告書|映像|NTSB', '約20分＝報告書 p103（映像から）'),
        (r'検察官|恥をかかせ', r'AP|報道|伝え', 'AP 通信の報道（2016年9月）'),
        (r'知事', r'報じ|報道|伝え', '知事の言葉＝報道の帰属'),
        (r'損なう', r'議長|公聴会', '公聴会の議長（ドケット #109 p9）'),
        (r'確かでは(なかった|ない)', r'公聴会|調査|報告書', '公聴会の調査の責任者（ドケット #109 p18）'),
        (r'溺れ', r'報告書|NTSB|可能性', '報告書の見立て（p103）'),
        (r'8ポンド|3\.6キロ', r'報告書|NTSB|平均|調べ', '鳥の重さ＝報告書 p80'),
        (r'4ポンド|1\.8キロ', r'試験|認証|基準', '当時の試験の鳥の重さ＝報告書 p17')]
TIME_RE = re.compile(r'まだ|されていない|分かっていない|決まっていない|出ていない|見当たらない|いまも|今も|現在も|いまは|今は')
TIME_OK = re.compile(r'2026年|2025年|2024年|2023年|2019年|2016年|2014年|2010年|2009年|11月')
DESU_RE = re.compile(r'(です|(?<!だ)ます|でした|ました|ません)か?(?:[。、？！」]|$)')   # 「だます」は除く
HONOR_RE = re.compile(r'[一-龥ァ-ヶ]{1,4}(さん|くん|ちゃん|氏)')
QUOTE_SPAN = re.compile(r'「[^」]*」')
KIND_RE = re.compile(r'実写 (映像|写真|調査|衛星|公的)')
CLIP_RE = re.compile(r'実写 映像 VTS ([^\s（(・]+)')
PHOTO_RE = re.compile(r'実写 写真 \[(\d+)\]')
DOCK_RE = re.compile(r'実写 調査 (#\d+[^（(]*)')
PUB_RE = re.compile(r'実写 公的 ([^\s（(]+)')
GROUND_RE = re.compile(r'地＝([^）]*?)(?:を暗く|）|$)')
SUBTIME_RE = re.compile(r'副題「[^」]*\d{1,2}:\d{2}')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
NAMES_FILES = [os.path.join(SRC, 'names_private.txt'), os.path.join(SRC, 'names_commons.txt')]   # git の外
_spec = importlib.util.spec_from_file_location(
    'cts', r'C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証ch-案C見本\count_text_screens.py')
CTS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CTS)


def nopunct(s):
    return sum(1 for ch in s if ch not in PUNCT)


def fmt(s):
    return '%d分%02d秒' % (int(s) // 60, int(s) % 60)


def fig_type(pic):
    m = re.match(r'図\s+([^\s（(]+)', pic)
    return m.group(1) if m else None


def load_roles(p):
    out = {}
    if not p or not os.path.exists(p):
        return None
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        cid, role, text = ln.rstrip('\n').split('\t')
        out[(cid, text)] = role
    return out


def load_names():
    if not os.path.exists(NAMES_FILES[0]):
        return None
    words = []
    for p in NAMES_FILES:
        if os.path.exists(p):
            words += [ln.strip() for ln in open(p, encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    return words


def raw_sources(text):
    """カットID → 出典の欄（check_script.parse は出典を返さない）。"""
    out = {}
    for m in re.finditer(r'^\*\*([a-z][0-9a-z]\d{2})\*\*\s*(?:🔧\s*)?／\s*(.*?)\s*／\s*(.*)$', text, re.M):
        out[m.group(1)] = m.group(3)
    return out


def check_pic(cid, pic, ch, E, W, keys):
    if ch == 'c1' and not pic.startswith('実写'):
        E.append('E %s 冒頭（c1）は実写だけ（ルール 4-16）' % cid)
    if '図2' in pic and ('報告書' in pic or 'AAR' in pic):
        E.append('E %s 報告書の図2（撮影者の記載なし）は使わない' % cid)
    if pic.startswith('実写'):
        mk = KIND_RE.match(pic)
        if not mk:
            W.append('W %s 実写の種類の語が無い' % cid)
            return None
        kind = mk.group(1)
        if kind == '映像':
            if '副題' not in pic:
                E.append('E %s 映像に副題が無い' % cid)
            if SUBTIME_RE.search(pic):
                E.append('E %s 副題に時刻（カメラの時計は約20秒進む＝画面の時刻を使わない）' % cid)
            mc = CLIP_RE.match(pic)
            if not mc:
                E.append('E %s 映像の区間の名が無い（実写 映像 VTS 〈名〉）' % cid)
            else:
                name = mc.group(1)
                if name not in CLIPS_OK:
                    E.append('E %s 台帳に無い区間の名（%s）' % (cid, name))
                keys[('映像', name)].append(cid)
        elif kind == '写真':
            mp = PHOTO_RE.match(pic)
            if not mp:
                E.append('E %s 写真の番号が無い（実写 写真 [n]）' % cid)
            else:
                no = int(mp.group(1))
                keys[('写真', no)].append(cid)
                if no in PHOTO_NG:
                    E.append('E %s 使わない写真 [%d]（%s）' % (cid, no, PHOTO_NG[no]))
                if no in BYSA:
                    for need in ('額装', '無加工'):
                        if need not in pic:
                            E.append('E %s BY-SA の写真 [%d] に「%s」が無い' % (cid, no, need))
                if no in CROP_NEED and '切' not in pic:
                    E.append('E %s 写真 [%d] は名前の字を切って使う（%s）' % (cid, no, CROP_NEED[no]))
        elif kind == '調査':
            md = DOCK_RE.match(pic)
            if not md:
                E.append('E %s 調査の写真の品目が無い（実写 調査 #N 〈写真〉）' % cid)
            else:
                keys[('調査', md.group(1).strip())].append(cid)
            for rx, why in DOCK_NG:
                if re.search(rx, pic):
                    E.append('E %s 使わない調査の写真（%s）' % (cid, why))
            if '額装' not in pic:
                E.append('E %s 調査の写真に「額装」が無い（撮影者の記載なし＝額装で使う）' % cid)
        elif kind == '公的':
            for need in ('額装', '出典'):
                if need not in pic:
                    E.append('E %s 紙面の印（%s）が無い' % (cid, need))
        return kind
    if pic.startswith('図'):
        mg = GROUND_RE.search(pic)
        if not mg:
            W.append('W %s 説明カットの地（地＝写真）が書いていない' % cid)
        else:
            g = mg.group(1)
            for no in re.findall(r'\[(\d+)\]', g):
                if int(no) in BYSA:
                    E.append('E %s BY-SA の写真 [%s] を地にした（字を重ねない）' % (cid, no))
                if int(no) in PHOTO_NG:
                    E.append('E %s 使わない写真 [%s] を地にした' % (cid, no))
            if '夜' in g and ch in ('c2', 'c3', 'c4', 'c5', 'c6', 'c7'):
                W.append('W %s 昼の話の地に夜の写真' % cid)
    return None


def main(path, roles_path=None):
    text = open(path, encoding='utf-8').read()
    cuts = CS.parse(text)
    srcs = raw_sources(text)
    n = len(cuts)
    lines = [(cid, l) for cid, _, ls in cuts for l in ls]
    E, W = [], []
    per_ch = collections.OrderedDict()
    tot = 0
    rows = []          # check_listener.judge の形 (cid, i, 話者, 文, 秒)
    t = 0.0
    hook = []
    starts = {}
    first_q = {}
    figs = collections.Counter()
    fig_seq = []
    keys = collections.defaultdict(list)
    names = load_names()
    kinds = collections.Counter()
    pub_docs = []
    for idx, (cid, pic, ls) in enumerate(cuts):
        ch = cid[:2]
        starts.setdefault(ch, t)
        d = per_ch.setdefault(ch, dict(cuts=0, lines=0, chars=0, photo=0, free=0, fig=0, q=0))
        d['cuts'] += 1
        d['lines'] += len(ls)
        is_photo = pic.startswith('実写')
        d['photo'] += is_photo
        d['free'] += pic.startswith('イメージ')
        ft = fig_type(pic)
        if pic.startswith('図'):
            d['fig'] += 1
            figs[ft] += 1
        fig_seq.append((cid, ft))
        kind = check_pic(cid, pic, ch, E, W, keys)
        if kind:
            kinds[kind] += 1
        if kind == '公的':
            mpub = PUB_RE.match(pic)
            pub_docs.append((cid, mpub.group(1) if mpub else '?'))
        whole = pic + ' ' + srcs.get(cid, '')
        if not 1 <= len(ls) <= 3:
            E.append('E %s 行数 %d' % (cid, len(ls)))
        cut_text = ''
        for i, raw in enumerate(ls, 1):
            c = CS.clean(raw)
            cut_text += c
            if len(c) > 41:
                E.append('E %s 1行%d字: %s' % (cid, len(c), c))
            np_ = nopunct(c)
            who = speaker.split(raw)[0]
            if who == speaker.WHO_Q:
                first_q.setdefault(ch, t)
            rows.append((cid, i, who, speaker.bare(CS.STAR_RE.sub('', raw).replace('**', '').strip()), t))
            t += np_ / CPM * 60
            d['chars'] += np_
            tot += np_
            if who == speaker.WHO_Q:
                d['q'] += 1
                if CL.NUM_RE.search(c):
                    E.append('E %s 聞き役の行に数字（漢数字も）: %s' % (cid, c))
            if CS.STAR_RE.match(raw):
                E.append('E %s 決め所の行（32本目は決め所0）: %s' % (cid, c))
            outside = QUOTE_SPAN.sub('', c)
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」%s: %s' % (cid, w, '（引用の中）' if w not in outside else '', c))
            if cid != LAST_CUT and DESU_RE.search(outside):
                W.append('W %s です・ます（語りは言い切り）: %s' % (cid, c))
            if [m for m in HONOR_RE.finditer(c) if not m.group(0).endswith('赤ちゃん')]:
                W.append('W %s 敬称の網（名前が入っていないか）: %s' % (cid, c))
        for rx, why in NG_RE:
            if re.search(rx, QUOTE_SPAN.sub('', cut_text)):
                W.append('W %s 言わない形（%s）' % (cid, why))
        for src_txt, where in ((cut_text, '語り'), (whole, '画と出典')):
            if names:
                low = src_txt.lower()
                for nm in names:
                    if nm.lower() in low:
                        E.append('E %s 名前の網に当たった（%s・git の外の表の %d字の語）' % (cid, where, len(nm)))
        for rx, need, why in ATTR:
            if re.search(rx, cut_text) and not re.search(need, cut_text):
                W.append('W %s 帰属の語が無い（%s）' % (cid, why))
        outside_cut = QUOTE_SPAN.sub('', cut_text)
        if TIME_RE.search(outside_cut) and not TIME_OK.search(cut_text) and cid != LAST_CUT:
            W.append('W %s 時点の言い切りに日付が無い: %s' % (cid, TIME_RE.search(outside_cut).group(0)))
        if ch == 'c1':
            hook.append('%s=%.1fs' % (cid, t))
    total_sec = t + ED01 / CPM * 60
    allch = tot + ED01
    d1 = n * SEC_PER_CUT
    d2 = allch / CPM * 60
    d3 = (sum(v['chars'] for v in per_ch.values()) + ED01) / CPM * 60
    nphoto = sum(v['photo'] for v in per_ch.values())
    nfree = sum(v['free'] for v in per_ch.values())
    print('カット %d / 行 %d / 句読点なし %d字＋ed01 %d＝%d字（目標 %d・幅 %d〜%d＝%s）'
          % (n, len(lines), tot, ED01, allch, TARGET, LO, HI, '内' if LO <= allch <= HI else '🔴外'))
    print('写真・映像・紙面（実写）%d（%.1f%%）＝%s ／ フリー素材（イメージ）%d ／ 図 %d'
          % (nphoto, nphoto / max(1, n) * 100, '・'.join('%s %d' % kv for kv in kinds.most_common()), nfree,
             sum(v['fig'] for v in per_ch.values())))
    if nphoto / max(1, n) < 0.20:
        W.append('W 写真・映像・紙面が %d/%d（20%%未満）' % (nphoto, n))
    pub = [cid for cid, _ in pub_docs]
    print('文字の頁の見込み（実写 公的＝紙面）%d（%.1f%%）: %s' % (len(pub), len(pub) / max(1, n) * 100, ' '.join(pub)))
    order = [cid for cid, _, _ in cuts]
    run = 0
    for cid in order:
        run = run + 1 if cid in pub else 0
        if run == 2:
            W.append('W 紙面が続く: %s まで2カット' % cid)
        if run == 3:
            E.append('E 紙面が3カット続く: %s まで（ルール＝3カット以上続けない）' % cid)
    allc = [CS.clean(l) for _, l in lines]
    if allc:
        print('1行 中央値 %d字・最長 %d字・1カット %.2f行' % (sorted(len(x) for x in allc)[len(allc) // 2],
                                                   max(len(x) for x in allc), len(lines) / max(1, n)))
    print('尺 ① カット×%.3f秒 %s ／ ② 句読点なし÷365 %s ／ ③ 章ごとの合計 %s → 開き %s'
          % (SEC_PER_CUT, fmt(d1), fmt(d2), fmt(d3), fmt(max(d1, d2, d3) - min(d1, d2, d3))))
    if max(d1, d2, d3) - min(d1, d2, d3) > 120:
        E.append('E 尺の3通りの開きが2分を超えた（どれかが壊れている）')
    print('冒頭（÷365 を1カットずつ足した秒・カットの終わり）: ' + ' '.join(hook))
    print('章ごと: 章 始まり カット（目安） 行 句読点なし（目安・差） 分 写真（目安）割合 イメージ 図 聞き役（目安） 頭から最初の聞き役')
    for ch, v in per_ch.items():
        tg = CH_TARGET.get(ch, 0)
        fq = first_q.get(ch)
        fqs = (fq - starts[ch]) if fq is not None else None
        if ch != 'c1' and (fqs is None or fqs > HEAD_Q_SEC):
            W.append('W %s 章の頭から最初の聞き役まで %s' % (ch, '無し' if fqs is None else '%.1f秒' % fqs))
        pp = v['photo']
        if pp / max(1, v['cuts']) < 0.20:
            W.append('W %s 写真が %d/%d（20%%未満）' % (ch, pp, v['cuts']))
        print('  %s %s %3d（%3d） %3d %5d（%5d・%+4d） %5.2f %2d（%2d）%3.0f%% %2d %2d %2d（%d） %s'
              % (ch, fmt(starts[ch]), v['cuts'], CH_CUTS.get(ch, 0), v['lines'], v['chars'], tg,
                 v['chars'] - tg, v['chars'] / CPM, pp, CH_PHOTO.get(ch, 0), pp / max(1, v['cuts']) * 100,
                 v['free'], v['fig'], v['q'], CH_Q.get(ch, 0), '-' if fqs is None else '%.1f秒' % fqs))
    print('  ed01 %s' % fmt(t))
    print('図の型: ' + '・'.join('%s %d' % (k, v) for k, v in figs.most_common()))
    for k, v in figs.items():
        if k in TEMPLATE and v > 2:
            E.append('E 図の型「%s」が %d 回（全編で2回まで）' % (k, v))
        if k not in TEMPLATE and k != '模式':
            W.append('W 図の型「%s」は表に無い（綴りで門番をかわしていないか）' % k)
    for (c0, f0), (c1, f1) in zip(fig_seq, fig_seq[1:]):
        if f0 and f0 == f1 and f0 in TEMPLATE:
            E.append('E 図の型「%s」が続く: %s → %s' % (f0, c0, c1))
        elif f0 and f0 == f1:
            W.append('W 図の型「%s」が続く（別の絵か人が見る）: %s → %s' % (f0, c0, c1))
    for (kind, key), cids in sorted(keys.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
        if len(cids) > 1:
            W.append('W %s %s を %d回: %s' % (kind, key, len(cids), ' '.join(cids)))
    used = {k for (kind, k) in keys if kind == '写真'}
    for grp in SAME_PHOTO:
        hit = sorted(grp & used)
        if len(hit) > 1:
            W.append('W 同じ写真の束 %s を2回以上（切り抜きの版）' % hit)
    for (c0, d0), (c1, d1_) in zip(pub_docs, pub_docs[1:]):
        if d0 == d1_ and order.index(c1) == order.index(c0) + 1:
            W.append('W 同じ紙面が2カット続く: %s → %s（%s）' % (c0, c1, d0))
    print('名前の網: ' + ('🔴 表が無い（src/names_private.txt）' if names is None else '%d語を当てた' % len(names)))
    if names is None:
        E.append('E 名前の網の表が無い（fail closed）')
    roles = load_roles(roles_path)
    if roles is None:
        print('🔴 roles.tsv が無い（--roles を付ける）＝聞き役は数えない')
        e2, w2 = ['roles.tsv が無い'], []
    else:
        e2, w2, info = CL.judge(rows, total_sec, roles)
        print('聞き役: %s' % {k: (round(v, 3) if isinstance(v, float) else v) for k, v in info.items()})
    for x in e2:
        print('  🔴 ' + x)
    for x in w2:
        print('  ⚠️ ' + x)
    tc = CTS.parse(path)
    CTS.report(tc, {}, None, '画の欄のまま')
    for x in W:
        print('⚠️ ' + x)
    for x in E:
        print('🔴 ' + x)
    print('E %d件（形）・聞き役 E %d件・W %d件・言わない語 %d件'
          % (len(E), len(e2), len(w2) + len(W), sum(1 for x in W if '言わない' in x)))
    return len(E) + len(e2)


def selftest():
    ok = nopunct('「あ、い。」（う）・え？お！') == 5
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= abs(sum(CH_TARGET.values()) + ED01 - TARGET) <= 10 and sum(CH_CUTS.values()) == 240
    ok &= 55 <= sum(CH_Q.values()) <= 73 and abs(SEC_PER_CUT * 240 - 36.5 * 60) < 2.0
    ok &= fig_type('図 帯（空域）') == '帯' and fig_type('図 模式（地図）') == '模式'
    ok &= bool(HONOR_RE.search('田中さんは')) and not HONOR_RE.search('みなさんへ')
    ok &= bool(CL.NUM_RE.search('七年の')) and not CL.NUM_RE.search('どこにいるの？')
    ok &= bool(TIME_RE.search('いまも続く')) and bool(TIME_OK.search('2026年11月'))
    ok &= bool(DESU_RE.search('ありますか。')) and not DESU_RE.search('ますます増えた')
    ok &= KIND_RE.match('実写 映像 VTS 着水（…）').group(1) == '映像'
    ok &= CLIP_RE.match('実写 映像 VTS 着水（…）').group(1) == '着水'
    ok &= PHOTO_RE.match('実写 写真 [31]（…）').group(1) == '31'
    e, w, k = [], [], collections.defaultdict(list)
    check_pic('c999', '実写 写真 [68]（後ろの胴体・副題「…」）', 'c9', e, w, k)      # 陽性＝BY-SA に額装・無加工なし
    ok &= any('額装' in x for x in e) and any('無加工' in x for x in e)
    e = []
    check_pic('c999', '実写 写真 [71]（額装・無加工）', 'c9', e, w, k)                # 陽性＝使わない点
    ok &= any('使わない写真' in x for x in e)
    e = []
    check_pic('c999', '図 模式（…・地＝実写 写真 [68] を暗く）', 'c9', e, w, k)       # 陽性＝BY-SA を地に
    ok &= any('BY-SA' in x for x in e)
    e = []
    check_pic('c999', '実写 映像 VTS 着水（…・副題「沿岸警備隊のカメラ 3:31」）', 'c9', e, w, k)   # 陽性＝副題に時刻
    ok &= any('副題に時刻' in x for x in e)
    e = []
    check_pic('c999', '実写 調査 #49 写真3（額装）', 'c9', e, w, k)                    # 陽性＝当日の写真
    ok &= any('使わない調査の写真' in x for x in e)
    e = []
    check_pic('c999', '実写 調査 #49 写真42（額装・副題「…」）', 'c9', e, w, k)        # 陰性＝NTSB の調査の写真
    ok &= not e
    e = []
    check_pic('c101', '図 模式（…・地＝実写 写真 [31] を暗く）', 'c1', e, w, k)        # 陽性＝冒頭に図
    ok &= any('冒頭' in x for x in e)
    e = []
    check_pic('c999', '実写 映像 VTS 着水（…・副題「沿岸警備隊のカメラ〈2009年1月15日〉」）', 'c9', e, w, k)  # 陰性
    ok &= not e
    ok &= bool(re.search(NG_RE[0][0], '着水のボタンを押した')) and not re.search(NG_RE[0][0], '着水のボタンは押していない')
    ok &= bool(re.search(NG_RE[3][0], '約3分で最初の船が')) and not re.search(NG_RE[3][0], '約4分で最初の船が')
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
