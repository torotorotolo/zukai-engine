# -*- coding: utf-8 -*-
"""33本目 台本の机上の数え（32本目の m32.py を写し、33本目＝グレンフェルタワー火災・A 枠・36分30秒・12章と、この回の網に替えた）。

  python -P ref/ep33/v1_build/m33.py ref/ep33/daihon_v1.md --roles ref/ep33/v1_build/roles.tsv
  python -P ref/ep33/v1_build/m33.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28）・
3通りの尺（①カット×9.05秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge）・
写真と映像（画の欄の頭が「実写」＝映像・写真・紙面・衛星・公的の内わけ）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ絵の2回使い・
この回の網（kousei.md の線・materials.md §1〜§4・§10）：
  ・名前（git の外の src/names_private.txt と names_commons.txt の語＝E・大文字小文字を区別しない）・敬称の網（さん・くん・ちゃん・氏 を W）
  ・冒頭（c1）は実写だけ（E）
  ・映像＝Commons #15 だけ（実写 映像 #15 〈区間〉）・副題が要る・同じ区間を2回使わない（W）
  ・Commons の写真＝番号 [n]（src/commons/cand33.json の通し番号）。使わない点・未見の点（#73〜#130＝追悼の場と支援）＝E・
    BY-SA は 額装・無加工 が無ければ E・地にしたら E・同じ写真の切り抜きの対（[1][2]／[6][7]／[9][10]）は E・似た束を4点以上は W
  ・報告の図（実写 紙面 〈巻〉 図n.n）＝紙面の引用＝額装・無加工・出典 が無ければ E・ホワイトボードの図（P1V3 図16.4・16.5）は E（名前の有無が未確認）
  ・文字の頁（実写 公的）は 額装・出典 が無ければ E・3カット続けば E
  ・言わない語（当たったら人が文脈を見る W）・言わない形（見捨てた形・住人の責任・容疑の会社の名 ほか）
  ・帰属（すべて避けられた＝委員長と首相・01時30分〜50分＝報告・46人＝報告 ほか＝同じカットに出どころの語が要る W）
  ・時点の言い切り（まだ・いまも ほか＝同じカットに日付が要る W）・地＝写真（「図」は「地＝」が無ければ W・地に夜の写真と衛星は W）・
    です・ます（最後の問いのカットのほかは W）
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
SEC_PER_CUT = 9.05                 # kousei.md §0（36.5分÷242カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（26本目の④で数えた値・32本目も同じ）
TARGET = 13320                     # kousei.md §0（ed01 こみ・36分30秒）
LO, HI = 13120, 13520              # kousei.md §3 の注＝13,320±200
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで
# kousei.md §3（cc は 730 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 730, 'c2': 910, 'c3': 1100, 'c4': 1830, 'c5': 1460, 'c6': 1640, 'c7': 1280, 'c8': 1100,
             'c9': 730, 'ca': 910, 'cb': 910, 'cc': 684}
CH_CUTS = {'c1': 13, 'c2': 17, 'c3': 20, 'c4': 33, 'c5': 26, 'c6': 30, 'c7': 23, 'c8': 20, 'c9': 13, 'ca': 17,
           'cb': 17, 'cc': 13}
CH_Q = {'c1': 3, 'c2': 4, 'c3': 5, 'c4': 8, 'c5': 7, 'c6': 8, 'c7': 6, 'c8': 5, 'c9': 4, 'ca': 4, 'cb': 4, 'cc': 3}
# materials.md §8 の見込みを章へ割った目安（W は出さない）
CH_PHOTO = {'c1': 13, 'c2': 7, 'c3': 6, 'c4': 10, 'c5': 6, 'c6': 5, 'c7': 4, 'c8': 3, 'c9': 4, 'ca': 8, 'cb': 4,
            'cc': 3}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す
TEMPLATE = {'帯', '年表', '暦', '時計', '地図', '棒', '線', '箱', '札', '流れ', '比べ', '並べ', '割合', '窓口',
            '問答', '条文', '言葉', '式', '表', '方位', '断面', '立面'}
# Commons #15（GRENFELL.webm・CC BY 3.0）の区間の名（materials.md §2＝0:25〜2:40 空撮・3:00〜3:50 焼けた塔）
CLIPS_OK = {'空撮A', '空撮B', '空撮C', '焼けた塔A', '焼けた塔B', '焼けた塔C', '焼けた塔D'}
# cand33.json の許諾（#1〜#72＝② の見本帳で見た束。#73〜#130 は未見）
BYSA = {1, 2, 3, 5, 9, 10, 11, 13, 16, 18, 26, 27, 30, 31, 33, 34, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
        51, 52, 53, 54, 56, 57, 68}
PHOTO_NG = {1: '#2 の切り抜き（#2 を使う）', 4: '映像（沈黙の行進）＝未見', 5: '図（報告の図と自作で足りる）',
            6: '#7 の切り抜き（#7 を使う）', 9: '細すぎ', 11: '図（512px）', 13: 'SVG の図', 14: 'ロゴの文字',
            15: '映像は「実写 映像 #15 〈区間〉」で', 16: '地図（衛星写真で）', 17: 'ロゴと私人の顔',
            34: '640px', 36: '768px', 37: '620px', 38: '追悼の柵と掲示（名前の有無が未確認）', 57: '612px・追悼の花と人'}
for _n in range(73, 131):
    PHOTO_NG[_n] = '追悼の場・支援の束＝未見（映像方針で見本帳を見てから）'
SAME_PHOTO = [{1, 2}, {6, 7}, {9, 10}]
SIMILAR = [set(range(41, 55)), set(range(21, 26)), set(range(61, 68))]
FIG_NG = [(r'P1V3 ?図 ?16\.[45](?![0-9])', 'ホワイトボードの図＝名前の有無を原寸で未確認')]
# 言わない語（kousei.md の線・§B4・§4-13 波ダッシュ）。当たったら人が文脈を見る（W）
NG = ['犠牲', '死亡', '見捨て', '史上最悪', '最悪', '60時間', '噂', '英雄', '衝撃', '瞬間', '地獄', '闇', '〜', '～',
      '生きたまま', '焼死', '黒焦げ', '惨劇', '即死', '絶命', '殺']
NG_RE = [(r'(消防|隊員|消防士|指揮).{0,12}(見捨て|放置し|逃げ出)', '「見捨てた」の形にしない（報告の言葉で）'),
         (r'(住人|住民|出火した部屋).{0,10}(のせい|が原因|の責任だ|に責任がある|の過失)', '出火した部屋の住人に責任はない（bears no blame）'),
         (r'ガス.{0,12}(大きくし|広げ|爆発)', 'ガスの寄与は小さい（P1V4 ¶34.15）'),
         (r'(合法|適法)だった(?!、という)', '「合法だった」は崩れる話（規則に合っていなかった）＝言い切らない'),
         (r'(起訴|有罪|逮捕)(され|し)た(?!人は(い|居)ない)', '2026年11月の時点で起訴は無い'),
         (r'(アルコニック|セロテックス|キングスパン|ライドン|ハーレー|スタジオ・?イー|Arconic|Celotex|Kingspan|Rydon|Harley)'
          r'.{0,24}(容疑|捜査|書類|送致|起訴)', '容疑の対象の会社の名は言わない（警視庁は数だけ）'),
         (r'(容疑|捜査|書類|送致).{0,24}(アルコニック|セロテックス|キングスパン|ライドン|ハーレー|Arconic|Celotex|Kingspan|Rydon|Harley)',
          '容疑の対象の会社の名は言わない（警視庁は数だけ）')]
# 帰属（同じカットの中に出どころの語が要る数と見方）
ATTR = [(r'避けられた', r'委員長|首相', '「すべて避けられた」＝委員長の言葉（首相の議会での声明の引用）'),
        (r'1時30分から1時50分|1時半から', r'報告|調査', '01.30〜01.50＝報告の判断（P1V4 ¶28.6）'),
        (r'46人', r'報告|調査', '02.35 以降に逃げた46人＝報告（P1V4 ¶28.81 注72）'),
        (r'最悪', r'報告|調査', '「戦後の英国で最悪の災害の1つ」＝報告（P2V7 ¶98.1）'),
        (r'極めて危険', r'国交省|国土交通省|実験', '国交省の実験（F11 の報告 p.24）'),
        (r'168人が亡く|168人の死者', r'香港|警察', '香港の警察の発表（2026-01-15）'),
        (r'54人|57人|58人|19の団体|20の団体|20団体|19団体', r'警視庁|警察|2026年|2024年', '警視庁の発表（日付つき）'),
        (r'30件|61件|12件', r'政府|2026年|報告', '政府の進捗の報告（2026-09・2026-02）'),
        (r'1人の判断|下の役人|下位の', r'報告|調査', '報告の言葉（P2V2 ¶29.12）'),
        (r'勇気', r'報告|調査', '隊員の勇気＝報告（P1V4 ¶28.1）'),
        (r'1時間近く', r'報告|調査', '"the best part of an hour"＝報告（P1V4 ¶28.6）'),
        (r'偽り|うそ', r'報告|調査', '報告の言葉（P2V4 ¶55.72 ほか）'),
        (r'3時間足らず', r'報告|調査', '"under three hours"＝報告（P1ES ¶2.13）')]
TIME_RE = re.compile(r'まだ|されていない|分かっていない|決まっていない|出ていない|見当たらない|いまも|今も|現在も|いまは|今は')
TIME_OK = re.compile(r'2026年|2025年|2024年|2023年|2019年|2018年|2017年|11月')
DESU_RE = re.compile(r'(です|(?<!だ)ます|でした|ました|ません)か?(?:[。、？！」]|$)')   # 「だます」は除く
HONOR_RE = re.compile(r'[一-龥ァ-ヶ]{1,4}(さん|くん|ちゃん|氏)')
QUOTE_SPAN = re.compile(r'「[^」]*」')
KIND_RE = re.compile(r'実写 (映像|写真|紙面|衛星|公的)')
CLIP_RE = re.compile(r'実写 映像 #15 ([^\s（(・]+)')
PHOTO_RE = re.compile(r'実写 写真 \[(\d+)\]')
FIG_RE = re.compile(r'実写 紙面 (P[12](?:V\d|ES)) ?図 ?(\d+\.\d+)')
PUB_RE = re.compile(r'実写 公的 ([^\s（(]+)')
GROUND_RE = re.compile(r'地＝([^）]*?)(?:を暗く|）|$)')
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
    if pic.startswith('実写'):
        mk = KIND_RE.match(pic)
        if not mk:
            W.append('W %s 実写の種類の語が無い' % cid)
            return None
        kind = mk.group(1)
        if kind == '映像':
            if '副題' not in pic:
                E.append('E %s 映像に副題が無い' % cid)
            mc = CLIP_RE.match(pic)
            if not mc:
                E.append('E %s 映像の区間の名が無い（実写 映像 #15 〈名〉）' % cid)
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
                if '副題' not in pic:
                    W.append('W %s 写真に副題が無い' % cid)
        elif kind == '紙面':
            mf = FIG_RE.match(pic)
            if not mf:
                E.append('E %s 報告の図の巻と番号が無い（実写 紙面 P1V2 図10.9 の形）' % cid)
            else:
                keys[('紙面', mf.group(1) + ' 図' + mf.group(2))].append(cid)
            for need in ('額装', '無加工', '出典'):
                if need not in pic:
                    E.append('E %s 紙面の引用の印（%s）が無い（ルール §2-6c・§2-42）' % (cid, need))
            for rx, why in FIG_NG:
                if re.search(rx, pic):
                    E.append('E %s 使わない図（%s）' % (cid, why))
        elif kind == '公的':
            for need in ('額装', '出典'):
                if need not in pic:
                    E.append('E %s 紙面の印（%s）が無い' % (cid, need))
        elif kind == '衛星':
            if '副題' not in pic:
                W.append('W %s 衛星写真に副題が無い（「現在の衛星写真」）' % cid)
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
            if '紙面' in g:
                E.append('E %s 報告の図（第三者のコマ）を地にした（紙面の引用は額装だけ）' % cid)
            if '衛星' in g:
                W.append('W %s 地に衛星写真（Geo Guidelines＝暗くしない・32本目の決め）' % cid)
            if '夜' in g or re.search(r'\[(7|12|8|3|2)\]', g):
                W.append('W %s 地に夜（夜明け）の写真（暗い地は字が読めても何の写真か分からない＝29本目）' % cid)
    return None


def main(path, roles_path=None):
    text = open(path, encoding='utf-8').read()
    cuts = CS.parse(text)
    srcs = raw_sources(text)
    n = len(cuts)
    last_cut = cuts[-1][0] if cuts else None
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
                E.append('E %s 決め所の行（33本目は決め所0）: %s' % (cid, c))
            outside = QUOTE_SPAN.sub('', c)
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」%s: %s' % (cid, w, '（引用の中）' if w not in outside else '', c))
            if cid != last_cut and DESU_RE.search(outside):
                W.append('W %s です・ます（語りは言い切り）: %s' % (cid, c))
            if [m for m in HONOR_RE.finditer(c) if not m.group(0).endswith('赤ちゃん')]:
                W.append('W %s 敬称の網（名前が入っていないか）: %s' % (cid, c))
        for rx, why in NG_RE:
            if re.search(rx, QUOTE_SPAN.sub('', cut_text)):
                W.append('W %s 言わない形（%s）' % (cid, why))
        for rx, why in NG_RE[-2:]:
            if re.search(rx, whole):
                E.append('E %s 画と出典に容疑の会社の名（%s）' % (cid, why))
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
        if TIME_RE.search(outside_cut) and not TIME_OK.search(cut_text) and cid != last_cut:
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
    print('文字の頁の見込み（実写 公的）%d（%.1f%%）: %s' % (len(pub), len(pub) / max(1, n) * 100, ' '.join(pub)))
    order = [cid for cid, _, _ in cuts]
    run = 0
    for cid in order:
        run = run + 1 if cid in pub else 0
        if run == 2:
            W.append('W 文字の頁が続く: %s まで2カット' % cid)
        if run == 3:
            E.append('E 文字の頁が3カット続く: %s まで（ルール＝3カット以上続けない）' % cid)
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
            E.append('E 同じ写真の切り抜きの対 %s を両方使った' % hit)
    for grp in SIMILAR:
        hit = sorted(grp & used)
        if len(hit) > 3:
            W.append('W 似た写真の束 %s を4点以上（2〜3点に絞る）' % hit)
    for (c0, d0), (c1, d1_) in zip(pub_docs, pub_docs[1:]):
        if d0 == d1_ and order.index(c1) == order.index(c0) + 1:
            W.append('W 同じ文字の頁が2カット続く: %s → %s（%s）' % (c0, c1, d0))
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
    ok &= abs(sum(CH_TARGET.values()) + ED01 - TARGET) <= 10 and sum(CH_CUTS.values()) == 242
    ok &= 55 <= sum(CH_Q.values()) <= 73 and abs(SEC_PER_CUT * 242 - 36.5 * 60) < 2.0
    ok &= fig_type('図 帯（時刻）') == '帯' and fig_type('図 模式（外壁）') == '模式'
    ok &= bool(HONOR_RE.search('田中さんは')) and not HONOR_RE.search('みなさんへ')
    ok &= bool(CL.NUM_RE.search('七年の')) and not CL.NUM_RE.search('どこにいるの？')
    ok &= bool(TIME_RE.search('いまも続く')) and bool(TIME_OK.search('2026年11月'))
    ok &= bool(DESU_RE.search('ありますか。')) and not DESU_RE.search('ますます増えた')
    ok &= KIND_RE.match('実写 映像 #15 焼けた塔A（…）').group(1) == '映像'
    ok &= CLIP_RE.match('実写 映像 #15 焼けた塔A（…）').group(1) == '焼けた塔A'
    ok &= PHOTO_RE.match('実写 写真 [72]（…）').group(1) == '72'
    ok &= FIG_RE.match('実写 紙面 P1V2 図10.9（…）').group(2) == '10.9'
    e, w, k = [], [], collections.defaultdict(list)
    check_pic('c999', '実写 写真 [3]（夜明けの煙・副題「…」）', 'c9', e, w, k)            # 陽性＝BY-SA に額装・無加工なし
    ok &= any('額装' in x for x in e) and any('無加工' in x for x in e)
    e = []
    check_pic('c999', '実写 写真 [80]（額装・無加工）', 'c9', e, w, k)                   # 陽性＝未見の束
    ok &= any('使わない写真' in x for x in e)
    e = []
    check_pic('c999', '図 模式（…・地＝実写 写真 [39] を暗く）', 'c9', e, w, k)          # 陽性＝BY-SA を地に
    ok &= any('BY-SA' in x for x in e)
    e = []
    check_pic('c999', '実写 紙面 P1V2 図10.9（夜の窓・副題「…」）', 'c9', e, w, k)       # 陽性＝紙面の印なし
    ok &= any('額装' in x for x in e) and any('出典' in x for x in e)
    e = []
    check_pic('c999', '実写 紙面 P1V3 図16.4（額装・無加工・出典の行「…」）', 'c9', e, w, k)   # 陽性＝ホワイトボード
    ok &= any('使わない図' in x for x in e)
    e = []
    check_pic('c999', '実写 紙面 P1V2 図10.9（額装・無加工・図の番号と題の行ごと・出典の行「…」）', 'c9', e, w, k)  # 陰性
    ok &= not e
    e = []
    check_pic('c101', '図 模式（…・地＝実写 写真 [72] を暗く）', 'c1', e, w, k)          # 陽性＝冒頭に図
    ok &= any('冒頭' in x for x in e)
    e = []
    check_pic('c999', '実写 映像 #15 焼けた塔A（…・副題「焼けた塔〈2017年7月〉」）', 'c9', e, w, k)  # 陰性
    ok &= not e
    e = []
    check_pic('c999', '実写 映像 #15 夜の火（…・副題「…」）', 'c9', e, w, k)              # 陽性＝台帳に無い区間
    ok &= any('台帳に無い' in x for x in e)
    ok &= bool(re.search(NG_RE[0][0], '消防が住民を見捨てた')) and not re.search(NG_RE[0][0], '消防は1時間近くを失った')
    ok &= bool(re.search(NG_RE[1][0], '出火した部屋の住人に責任がある')) and not re.search(NG_RE[1][0], '住人に責任は無い')
    ok &= bool(re.search(NG_RE[5][0], 'セロテックスが容疑の対象')) and not re.search(NG_RE[5][0], 'セロテックスは試験を操作した')
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
