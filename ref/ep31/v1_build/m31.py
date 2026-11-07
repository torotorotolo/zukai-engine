# -*- coding: utf-8 -*-
"""31本目 台本の机上の数え（30本目の m30.py を写し、31本目＝全日空機雫石衝突事故・A 枠・36分00秒・12章と、この回の網に替えた）。

  python -P ref/ep31/v1_build/m31.py ref/ep31/daihon_v1.md --roles ref/ep31/v1_build/roles.tsv
  python -P ref/ep31/v1_build/m31.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×8.963秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真と映像（画の欄の頭が「実写」＝映像・写真・空中・衛星・公的の内わけ）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ絵の2回使い・
この回の網（kousei.md の線・materials.md §1〜§3）：
  ・名前（git の外の src/names_private.txt と names_commons.txt の語＝E）・敬称の網（さん・くん・ちゃん・氏 を W）
  ・使わない秒（防衛庁記録の新聞・積み込み〈搬送〉・参列者の近景＝E）・△ の秒（式・滑走路＝W で確かめを促す）
  ・BY-SA の写真（P1・P3・P7）は 額装・無加工 が無ければ E・地にしたら E・P1（事故機）は1カットだけ
  ・同型機と保存機（P2〜P8）は 副題に「この機体ではない」が無ければ E・P8（展示飛行の塗装）は W
  ・紙面（実写 公的）は 額装・出典 が無ければ E・映像は 副題 が無ければ E
  ・言わない語（当たったら人が文脈を見る W）・言わない形（「教官が指で決めた」ほか）
  ・帰属（7秒＝報告書・32秒＝防衛庁・指で示した＝最高裁 ほか＝同じカットに出どころの語が要る W）
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
SEC_PER_CUT = 8.963                # kousei.md §0（36.0分÷241カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（26本目の④で数えた値・30本目も同じ）
TARGET = 13140                     # kousei.md §0（ed01 こみ・36分00秒）
LO, HI = 13140, 13505              # 36〜37分＝目安の幅（A の枠 27〜40分の中）
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで
LAST_CUT = 'cc20'                  # 最後の問いのカット（です・ます はここだけ）
# kousei.md §3（cc は 1,095 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 365, 'c2': 913, 'c3': 1460, 'c4': 913, 'c5': 1460, 'c6': 1643, 'c7': 913, 'c8': 730,
             'c9': 1643, 'ca': 730, 'cb': 1278, 'cc': 1049}
CH_CUTS = {'c1': 7, 'c2': 17, 'c3': 27, 'c4': 17, 'c5': 27, 'c6': 30, 'c7': 17, 'c8': 13, 'c9': 30, 'ca': 13,
           'cb': 23, 'cc': 20}
CH_Q = {'c1': 2, 'c2': 5, 'c3': 7, 'c4': 5, 'c5': 7, 'c6': 8, 'c7': 3, 'c8': 4, 'c9': 8, 'ca': 4, 'cb': 6, 'cc': 4}
# materials.md §7 の章への割り振り（目安＝W も出さない）
CH_PHOTO = {'c1': 6, 'c2': 4, 'c3': 4, 'c4': 3, 'c5': 5, 'c6': 4, 'c7': 5, 'c8': 2, 'c9': 5, 'ca': 2, 'cb': 5, 'cc': 3}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す
TEMPLATE = {'帯', '年表', '暦', '時計', '地図', '棒', '線', '箱', '札', '流れ', '比べ', '並べ', '割合', '窓口',
            '問答', '条文', '言葉', '式', '表', '方位'}
# 防衛庁記録の区間の名（materials.md §2・§2b）＝「実写 映像 防衛記録 〈名〉」
CLIPS_OK = {'残骸', '部分', '隊員', '屋上', '半旗', '武道館外観', '祭壇礼', '祭壇寄り', '全景', '列', '札'}
CLIPS_CHECK = {'式A', '式B', '式C', '滑走路', '整列'}          # △＝確かめてから（W）
CLIPS_BAN = ('新聞', '積み込み', '搬送', '参列者', '近景')       # ✕＝E
BYSA = {'P1', 'P3', 'P7'}                                      # 額装・無加工・地にしない
SAME_TYPE = {'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'}          # 同型機・保存機＝「この機体ではない」
# 言わない語（kousei.md の線・§B4・§4-13 波ダッシュ）。当たったら人が文脈を見る（W）
NG = ['犯人', '加害者', '胡麻粒', '黒い豆', '心霊', '〜', '～', '死亡', '衝撃', '瞬間', '最悪', '史上', '地獄', '闇',
      '追突', '冤罪', '無罪', '撃墜', '突っ込', '58便', '五十八便']
NG_RE = [(r'教官が.{0,8}(指で|指し示)', '「教官が指で決めた」は崩れた（最高裁＝飛行班長補佐が示し飛行班長が承認）'),
         (r'(機長|副操縦士|乗員|操縦者).{0,12}(怠|ミス|失格|過失|落ち度|せい)', '亡くなった乗員を責める形にしない'),
         (r'訓練生.{0,10}(無罪|有罪|刑)', '訓練生の二審の結果は台本に入れない（sources.md §2-2）'),
         (r'幹部.{0,10}(起訴されな|裁かれな|不起訴)', '幹部の起訴の有無は資料に無い（言わない）')]
# 帰属（同じカットの中に出どころの語が要る数と見方）
ATTR = [(r'7秒|七秒', r'報告書|推定|調査委員会|委員長|防衛庁|運輸省', '7秒＝報告書の推定'),
        (r'32秒', r'防衛庁', '14時2分32秒＝防衛庁の主張'),
        (r'39秒', r'報告書|推定|調査委員会|運輸省|委員長', '14時2分39秒＝報告書の推定'),
        (r'指で示|指し示|手指', r'最高裁|判決', '指で示した＝最高裁'),
        (r'酷に過ぎる|一教官|幹部の責任', r'最高裁|判決', '最高裁の言葉'),
        (r'検討を加えることなく|念頭に', r'最高裁|判決', '最高裁の言葉'),
        (r'国が2|国は2|国2|二それから', r'東京高裁|高裁|防衛庁|答弁', '国2・全日空1＝防衛庁の答弁'),
        (r'54億', r'防衛庁|答弁', '約54億円＝防衛庁の答弁'),
        (r'16億', r'防衛庁|答弁', '16億5,200万円＝防衛庁の答弁'),
        (r'注視野', r'報告書|委員長|分析|図', '注視野＝報告書の分析'),
        (r'合意はございません', r'航空局長|運輸省', '「合意はございません」＝運輸省の航空局長'),
        (r'即断', r'防衛局長', '「即断することは適当ではなかろう」＝防衛局長'),
        (r'脱出であろう', r'警察庁', '「衝突後の脱出であろう」＝警察庁'),
        (r'五海里|5海里|(?<![0-9.])9キロ|九キロ', r'最高裁|判決|準則|自衛隊|防衛庁|参事官', '5海里＝自衛隊の準則・最高裁'),
        (r'16キロ|十六キロ', r'運輸省|航空局長|答弁', '16キロ＝運輸省の航空局長'),
        (r'155人', r'防衛庁|答弁|補償', '乗客155人＝防衛庁の答弁'),
        (r'3,660人|5,320人', r'長官|防衛庁', '派遣の人数＝防衛庁長官の報告'),
        (r'13時28分', r'長官|防衛庁', '13時28分＝防衛庁長官の報告'),
        (r'13時33分|13時46分|13時50分|14時11分', r'委員|国会', '全日空機の時刻＝国会の委員のまとめ'),
        (r'上昇、右旋回', r'長官|防衛庁', '「上昇、右旋回せよ」＝防衛庁長官の報告'),
        (r'謙虚', r'長官|防衛庁', '「謙虚に受けとめ」＝防衛庁長官'),
        (r'横切らざるを得', r'総理', '「民間航空路を横切らざるを得ない」＝総理大臣'),
        (r'47|119', r'国交省|国土交通省|記者発表', '民間訓練試験空域 47→119＝国交省'),
        (r'航空法', r'改正|条|法律', '航空法の改正＝法律の番号と条')]
TIME_RE = re.compile(r'まだ|されていない|分かっていない|決まっていない|出ていない|見当たらない|いまも|今も|現在も|いまは|今は')
TIME_OK = re.compile(r'2026年|令和8年|11月7日|2019年|2020年|令和元年|7月30日')
DESU_RE = re.compile(r'(です|(?<!だ)ます|でした|ました|ません)か?(?:[。、？！」]|$)')   # 「だます」は除く
HONOR_RE = re.compile(r'[一-龥ァ-ヶ]{1,4}(さん|くん|ちゃん|氏)')
QUOTE_SPAN = re.compile(r'「[^」]*」')
KIND_RE = re.compile(r'実写 (映像|写真|空中|衛星|公的)')
CLIP_RE = re.compile(r'実写 映像 防衛記録 ([^\s（(・]+)')
PHOTO_RE = re.compile(r'実写 写真 (P\d)')
PUB_RE = re.compile(r'実写 公的 ([^\s（(]+)')
GROUND_RE = re.compile(r'地＝([^）・]*)')
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
                E.append('E %s 映像の区間の名が無い（実写 映像 防衛記録 〈名〉）' % cid)
            else:
                name = mc.group(1)
                if any(b in name for b in CLIPS_BAN):
                    E.append('E %s 使わない秒（%s）' % (cid, name))
                elif name in CLIPS_CHECK:
                    W.append('W %s △の秒（%s）＝⑤b の前に確かめる' % (cid, name))
                elif name not in CLIPS_OK:
                    E.append('E %s 台帳に無い区間の名（%s）' % (cid, name))
                keys[('映像', name)].append(cid)
            # 「✕ の新聞の紙面＝0.5秒あける」のような境の注は数えない（11-07 の係C の直しで誤検出した）
            if re.search(r'(?<!✕ の)(?<!✕の)(新聞の紙面|積み込み|参列者の近景)', re.sub(r'✕\s*の[^・）]*', '', pic)):
                E.append('E %s 画の欄に使わない秒の語' % cid)
        elif kind == '写真':
            mp = PHOTO_RE.match(pic)
            if not mp:
                E.append('E %s 写真の番号が無い（実写 写真 P〈n〉）' % cid)
            else:
                no = mp.group(1)
                keys[('写真', no)].append(cid)
                if no in BYSA:
                    for need in ('額装', '無加工'):
                        if need not in pic:
                            E.append('E %s BY-SA の写真 %s に「%s」が無い' % (cid, no, need))
                if no in SAME_TYPE and 'この機体ではない' not in pic:
                    E.append('E %s 同型機・保存機 %s の副題に「この機体ではない」が無い' % (cid, no))
                if no == 'P8':
                    W.append('W %s P8（展示飛行の塗装）は推奨では使わない' % cid)
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
            for no in BYSA:
                if re.search(r'(?<![0-9])%s(?![0-9])' % no, g):
                    E.append('E %s BY-SA の写真 %s を地にした（字を重ねない）' % (cid, no))
            if re.search(r'夜|雪', g):
                E.append('E %s 晴れた昼の話の地に夜・雪の写真' % cid)
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
                E.append('E %s 決め所の行（31本目は決め所0）: %s' % (cid, c))
            outside = QUOTE_SPAN.sub('', c)
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」%s: %s' % (cid, w, '（引用の中）' if w not in outside else '', c))
            if cid != LAST_CUT and DESU_RE.search(outside):
                W.append('W %s です・ます（語りは言い切り）: %s' % (cid, c))
            if HONOR_RE.search(c):
                W.append('W %s 敬称の網（名前が入っていないか）: %s' % (cid, c))
        for rx, why in NG_RE:
            if re.search(rx, QUOTE_SPAN.sub('', cut_text)):
                W.append('W %s 言わない形（%s）' % (cid, why))
        for src_txt, where in ((cut_text, '語り'), (whole, '画と出典')):
            if names:
                for nm in names:
                    if nm in src_txt:
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
    for (kind, key), cids in sorted(keys.items()):
        if len(cids) > 1:
            (E if key == 'P1' else W).append('%s %s %s を %d回: %s' % ('E' if key == 'P1' else 'W', kind, key,
                                                                    len(cids), ' '.join(cids)))
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
    ok &= abs(sum(CH_TARGET.values()) + ED01 - TARGET) <= 10 and sum(CH_CUTS.values()) == 241
    ok &= 54 <= sum(CH_Q.values()) <= 72 and abs(SEC_PER_CUT * 241 - 36.0 * 60) < 2.0
    ok &= fig_type('図 帯（空域）') == '帯' and fig_type('図 模式（地図）') == '模式'
    ok &= bool(HONOR_RE.search('田中さんは')) and not HONOR_RE.search('みなさんへ')
    ok &= bool(CL.NUM_RE.search('七年の')) and not CL.NUM_RE.search('どこにいるの？')
    ok &= bool(TIME_RE.search('いまも続く')) and bool(TIME_OK.search('2026年7月30日'))
    ok &= bool(DESU_RE.search('ありますか。')) and not DESU_RE.search('ますます増えた')
    ok &= KIND_RE.match('実写 映像 防衛記録 残骸（…）').group(1) == '映像'
    ok &= CLIP_RE.match('実写 映像 防衛記録 残骸（…）').group(1) == '残骸'
    ok &= PHOTO_RE.match('実写 写真 P1（…）').group(1) == 'P1'
    e, w, k = [], [], collections.defaultdict(list)
    check_pic('c999', '実写 写真 P1（事故機・副題「JA8329」）', 'c9', e, w, k)
    ok &= any('額装' in x for x in e) and any('無加工' in x for x in e)
    e = []
    check_pic('c999', '実写 写真 P3（額装・無加工・副題「同型機」）', 'c9', e, w, k)
    ok &= any('この機体ではない' in x for x in e)
    e = []
    check_pic('c999', '図 模式（…・地＝写真 P7 を暗く）', 'c9', e, w, k)
    ok &= any('BY-SA' in x for x in e)
    e = []
    check_pic('c999', '実写 映像 防衛記録 新聞（…副題）', 'c9', e, w, k)
    ok &= any('使わない秒' in x for x in e)
    e = []
    check_pic('c999', '実写 映像 防衛記録 残骸（…・副題「…」）', 'c9', e, w, k)
    ok &= not e
    ok &= bool(re.search(NG_RE[0][0], '教官が地図の上で指で示した')) and not re.search(NG_RE[0][0], '飛行班長補佐が指で示した')
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
