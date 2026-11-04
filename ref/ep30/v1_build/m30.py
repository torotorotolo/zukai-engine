# -*- coding: utf-8 -*-
"""30本目 台本の机上の数え（29本目の m29.py を写し、30本目＝判決が確定した事件の回・A 枠・36分30秒・12章と、§B2-12 の網に替えた）。

  python ref/ep30/v1_build/m30.py ref/ep30/daihon_v1.md --roles ref/ep30/v1_build/roles.tsv
  python ref/ep30/v1_build/m30.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×8.975秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真と映像（画の欄の頭が「実写」＝陸自・映像・引用・公的・衛星・公立の内わけ）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ写真の点の2回使い（W）・
🆕 判決が確定した事件の網（ルール §B2-12・記憶 feedback-jiko-incident-case-rules）：
  ・線の語（git の外の src/line_words.txt＝語りにも画の欄にも出典の欄にも出さない＝E）。⚠️ リポは公開＝語そのものはここに書かない
  ・名前（git の外の src/names_private.txt に書いた語が1つでもあれば E）・敬称の網（さん・くん・ちゃん・氏 を W）
  ・使わない絵（資料館の ✕ の番号＝E）・夜の写真（#70・#72・#79 は c9 の終わりのほかで E）
  ・引用の印（「実写 引用」は 額装・無加工・出典・静止 が無ければ E）・公的（額装・出典 が無ければ E）
  ・映像（「実写 映像」は 副題 が無ければ E＝映っているのは除染。「まいている所」を名乗らない）
  ・言わない語（当たったら人が文脈を見る W）・帰属（14人＝公安調査庁・12人＝判決 ほか＝同じカットに出どころの語が要る W）
  ・時点の言い切り（まだ・いまも ほか＝同じカットに日付が要る W）
  ・地＝写真（「図」の説明カットは「地＝」が無ければ W）・です・ます（最後の問いのカットのほかは W）
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
SEC_PER_CUT = 8.975                # kousei.md §0（36.5分÷244カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（26本目の④で数えた値）
TARGET = 13320                     # kousei.md §0（ed01 こみ・36分30秒）
LO, HI = 13140, 13505              # 36〜37分＝目安の幅（A の枠 27〜40分の中）
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで
LAST_CUT = 'cc19'                  # 最後の問いのカット（です・ます はここだけ）
# kousei.md §3（cc は 1,095 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 365, 'c2': 730, 'c3': 913, 'c4': 1278, 'c5': 1095, 'c6': 1095, 'c7': 2008, 'c8': 1460,
             'c9': 1095, 'ca': 1095, 'cb': 1095, 'cc': 1049}
CH_CUTS = {'c1': 7, 'c2': 13, 'c3': 17, 'c4': 23, 'c5': 20, 'c6': 20, 'c7': 37, 'c8': 27, 'c9': 20, 'ca': 20,
           'cb': 20, 'cc': 20}
CH_Q = {'c1': 2, 'c2': 4, 'c3': 5, 'c4': 7, 'c5': 6, 'c6': 6, 'c7': 10, 'c8': 8, 'c9': 6, 'ca': 5, 'cb': 5, 'cc': 4}
# materials.md §7（数える分 58）の章への割り振り（目安＝W も出さない）
CH_PHOTO = {'c1': 6, 'c2': 3, 'c3': 6, 'c4': 3, 'c5': 3, 'c6': 3, 'c7': 6, 'c8': 5, 'c9': 12, 'ca': 5, 'cb': 2, 'cc': 4}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す
TEMPLATE = {'帯', '年表', '暦', '時計', '地図', '棒', '線', '箱', '札', '流れ', '比べ', '並べ', '割合', '窓口',
            '問答', '条文', '言葉', '式', '表'}
# 使わない絵（materials.md §2-6・§2-2・§2-3）＝資料館の番号
BAN = {30, 31, 33, 34, 35, 36, 37, 38, 41, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
       85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 96, 97, 100, 101}
NIGHT = {70, 72, 79}               # 夜の写真（朝の場面に当てない）
# 言わない語（§B2-12・§B4-9・§4-13 波ダッシュ）。当たったら人が文脈を見る（W）
NG = ['放置', '防ぎようがなかった', '防げた', '隠蔽', '衝撃', '瞬間', '最悪', '史上', '闇', '地獄', '尊師', '最終解脱',
      'ポア', '修行', '教義', '犯人扱い', '約6,000', '6000人', '192人', '〜', '～', '死亡']
NG_RE = [(r'事前に知', '「事前に知っていた」を支える文は無い（sources.md §6）'),
         (r'知っていて', '「知っていて黙っていた」と読まない（sources.md §0）')]
# 帰属（同じカットの中に出どころの語が要る数と見方）
ATTR = [(r'14人', r'公安調査庁', '14人＝公安調査庁'),
        (r'12人', r'判決', '12人＝判決'),
        (r'13人(?!の死刑)', r'公安調査庁|警察庁', '13人＝公安調査庁・警察庁'),
        (r'5,800人', r'給付金|国が認め|公安調査庁', '5,800人＝給付金で認めた数'),
        (r'135人', r'消防庁', '135人＝消防庁'),
        (r'640人', r'手記|院長|病院の記録', '640人＝院長の手記'),
        (r'64着', r'手記|警部補', '64着＝警部補の手記'),
        (r'約190人', r'犯罪白書', '約190人＝犯罪白書'),
        (r'10億', r'公安調査庁|遺族|最高裁', '約10億円'),
        (r'一時しのぎ', r'判決', '一時しのぎ＝判決'),
        (r'病人2名|ガソリンの匂い|爆発物を使用|防毒マスク|毒ガス事案', r'無線', '無線の語＝記録の帰属'),
        (r'共謀', r'判決', '共謀＝判決の言葉'),
        (r'見込み捜査', r'国会|議員', '見込み捜査＝国会の批判'),
        (r'陰謀', r'公安調査庁', '陰謀の説＝公安調査庁が書く出どころ')]
TIME_RE = re.compile(r'まだ|されていない|分かっていない|決まっていない|出ていない|見当たらない|いまも|今も|現在も')
TIME_OK = re.compile(r'11月4日の時点|11月2日|2026年|令和8年|2021年|2024年|2月末|9月4日')
DESU_RE = re.compile(r'(です|(?<!だ)ます|でした|ました|ません)か?(?:[。、？！」]|$)')   # 「だます」は除く
HONOR_RE = re.compile(r'[一-龥ァ-ヶ]{1,4}(さん|くん|ちゃん|氏)')
QUOTE_SPAN = re.compile(r'「[^」]*」')
NO_RE = re.compile(r'(?<![0-9０-９])#(\d{1,3})')
KIND_RE = re.compile(r'実写 (陸自|映像|引用|公的|衛星|公立)')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
NAMES_FILE = os.path.join(SRC, 'names_private.txt')   # git の外（1行1語・# は注）
LINE_FILE = os.path.join(SRC, 'line_words.txt')       # git の外（1行1語・# は注）
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


def load_words(path):
    if not os.path.exists(path):
        return None
    return [ln.strip() for ln in open(path, encoding='utf-8') if ln.strip() and not ln.startswith('#')]


def raw_sources(text):
    """カットID → 出典の欄（check_script.parse は出典を返さない）。"""
    out = {}
    for m in re.finditer(r'^\*\*([a-z][0-9a-z]\d{2})\*\*\s*(?:🔧\s*)?／\s*(.*?)\s*／\s*(.*)$', text, re.M):
        out[m.group(1)] = m.group(3)
    return out


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
    names = load_words(NAMES_FILE)
    linew = load_words(LINE_FILE)
    kinds = collections.Counter()
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
            if '地＝' not in pic:
                W.append('W %s 説明カットの地（地＝写真）が書いていない' % cid)
        fig_seq.append((cid, ft))
        if is_photo:
            mk = KIND_RE.match(pic)
            if mk:
                kinds[mk.group(1)] += 1
            else:
                W.append('W %s 実写の種類の語が無い' % cid)
            if pic.startswith('実写 引用'):
                for need in ('額装', '無加工', '出典', '静止'):
                    if need not in pic:
                        E.append('E %s 引用の印（%s）が無い' % (cid, need))
            if pic.startswith('実写 公的'):
                for need in ('額装', '出典'):
                    if need not in pic:
                        E.append('E %s 公的な機関の紙面の印（%s）が無い' % (cid, need))
            if pic.startswith('実写 映像') and '副題' not in pic:
                E.append('E %s 映像に副題が無い（映っているのは除染＝断る）' % cid)
        for m in NO_RE.finditer(pic):
            no = int(m.group(1))
            if no in BAN:
                E.append('E %s 使わない絵 #%d（materials.md §2-6）' % (cid, no))
            if no in NIGHT and ch != 'c9':
                E.append('E %s 夜の写真 #%d を c9 のほかに当てた' % (cid, no))
            if is_photo and m.start() < 16:
                keys[('点', '#%d' % no)].append(cid)
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
                E.append('E %s 決め所の行（30本目は決め所0）: %s' % (cid, c))
            outside = QUOTE_SPAN.sub('', c)
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」%s: %s' % (cid, w, '（引用の中）' if w not in outside else '', c))
            for rx, why in NG_RE:
                if re.search(rx, outside):
                    W.append('W %s 言わない形（%s）: %s' % (cid, why, c))
            if cid != LAST_CUT and DESU_RE.search(outside):
                W.append('W %s です・ます（語りは言い切り）: %s' % (cid, c))
            if HONOR_RE.search(c):
                W.append('W %s 敬称の網（名前が入っていないか）: %s' % (cid, c))
        for src_txt, where in ((cut_text, '語り'), (whole, '画と出典')):
            if names:
                for nm in names:
                    if nm in src_txt:
                        E.append('E %s 名前の網に当たった（%s・git の外の表の %d字の語）' % (cid, where, len(nm)))
            if linew:
                for k, w in enumerate(linew):
                    if w in src_txt:
                        E.append('E %s 線の語の網に当たった（%s・git の外の表の #%d）' % (cid, where, k + 1))
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
    print('写真・映像（実写）%d（%.1f%%）＝%s ／ フリー素材（イメージ）%d ／ 図 %d'
          % (nphoto, nphoto / max(1, n) * 100, '・'.join('%s %d' % kv for kv in kinds.most_common()), nfree,
             sum(v['fig'] for v in per_ch.values())))
    # 公的な機関の紙面は count_text_screens では「写真」に数えられるが、中身は文字の頁（ルール §5b-117 の向き）＝別に数えて続きを見る
    pub = [cid for cid, pic, _ in cuts if pic.startswith('実写 公的')]
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
            W.append('W 写真の点 %s を %d回: %s' % (key, len(cids), ' '.join(cids)))
    print('名前の網: ' + ('🔴 表が無い（src/names_private.txt）' if names is None else '%d語を当てた' % len(names)))
    print('線の語の網: ' + ('🔴 表が無い（src/line_words.txt）' if linew is None else '%d語を当てた' % len(linew)))
    if names is None or linew is None:
        E.append('E 網の表が無い（fail closed）')
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
    ok &= nopunct('SNS上では') == 6
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= abs(sum(CH_TARGET.values()) + ED01 - TARGET) <= 10 and sum(CH_CUTS.values()) == 244
    ok &= 55 <= sum(CH_Q.values()) <= 73 and abs(SEC_PER_CUT * 244 - 36.5 * 60) < 2.0
    ok &= fig_type('図 帯（交差点）') == '帯' and fig_type('図 模式（カード1）') == '模式'
    ok &= fig_type('実写 陸自 #65') is None
    ok &= bool(HONOR_RE.search('田中さんは')) and not HONOR_RE.search('みなさんへ')
    ok &= bool(CL.NUM_RE.search('七年の')) and not CL.NUM_RE.search('どこにいるの？')
    ok &= bool(TIME_RE.search('まだ分かっていない')) and bool(TIME_OK.search('11月4日の時点で'))
    ok &= bool(DESU_RE.search('考えたことはありますか。')) and not DESU_RE.search('ますます増えた')
    ok &= KIND_RE.match('実写 引用 東消 #60（…）').group(1) == '引用'
    ok &= [int(m.group(1)) for m in NO_RE.finditer('実写 陸自 #65（…）')] == [65]
    ok &= 59 in BAN and 60 not in BAN and 70 in NIGHT
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
