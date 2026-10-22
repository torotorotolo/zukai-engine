# -*- coding: utf-8 -*-
"""24本目 台本の机上の数え（23本目の m23.py を写し、24本目の章の目安・言わない語・名前・帰属の数えに替えた）。

  python ref/ep24/v1_build/m24.py <台本.md> --roles ref/ep24/v1_build/roles.tsv
  python ref/ep24/v1_build/m24.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×9.05秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる。
⚠️ c1 は 10-22 カズヤくんの決め「約1分で最初の見出し」で約1分・7カット＝残りは c2 の頭へ）・1行41字超・1カット1〜3行・
冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真（画の欄の頭が「実写」）・報告書の頁（「図 p〈PDF頁〉」）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ写真の点の2回使い（BY-SA は1点1カット）・言わない語（sources.md §3・legend §1-4・1通目）・
名前（10-22 カズヤくんの決め＝記録にある5人だけ・役職つき）・帰属（31人・30人・長期の推計）・秒まで言う時刻・呼び名「チョルノービリ」の回数。
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
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（23本目の④で数えた値＝tools/narration.py の3行）
TARGET = 13320                     # kousei.md §0（ed01 こみ・合格の幅＝36分〜37分）
LO, HI = 13140, 13505
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで
# kousei.md §3（c1＝約1分に縮めた分 548字・10カットを c2 へ。cc は 1,278 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 365, 'c2': 1461, 'c3': 913, 'c4': 1095, 'c5': 913, 'c6': 1095, 'c7': 913,
             'c8': 1278, 'c9': 1460, 'ca': 1278, 'cb': 1278, 'cc': 1232}
CH_CUTS = {'c1': 7, 'c2': 27, 'c3': 17, 'c4': 20, 'c5': 17, 'c6': 20, 'c7': 17,
           'c8': 23, 'c9': 27, 'ca': 23, 'cb': 23, 'cc': 21}
CH_Q = {'c1': 2, 'c2': 8, 'c3': 5, 'c4': 6, 'c5': 5, 'c6': 6, 'c7': 5,
        'c8': 7, 'c9': 8, 'ca': 7, 'cb': 6, 'cc': 6}
# materials.md §0（この事故の写真・映像・紙面 約66カット＝27%）の章への割り振り（目安＝W も出さない）
CH_PHOTO = {'c1': 5, 'c2': 6, 'c3': 4, 'c4': 4, 'c5': 4, 'c6': 4, 'c7': 10,
            'c8': 8, 'c9': 5, 'ca': 5, 'cb': 5, 'cc': 8}
CH_FREE = {'c1': 1, 'c2': 3, 'c3': 2, 'c4': 1, 'c5': 2, 'c6': 1, 'c7': 1, 'c8': 1, 'c9': 1, 'ca': 1, 'cb': 1, 'cc': 2}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す
TEMPLATE = {'断面', '平面', '帯', '年表', '暦', '時計', '地図', '棒', '箱', '札', '再現', '流れ', '比べ', '時刻表', '案C2', '案C4', '並べ'}
# 言わない語（sources.md §3・legend §1-4・1通目・ルール §B2-4 の死の語と煽り・§B1-2 の単位・§4-13 の波ダッシュ）。
# 当たったら人が文脈を見る（W）＝「よく語られる話」で引いて記録で閉じる行・打ち消しの行は当たって正しい
NG = ['死亡', '即死', '絶命', '悲劇', '地獄', '戦慄', '驚愕', '恐怖', '惨劇', '瞬間', 'ﾀﾋ', '衝撃',
      '核爆弾', '核爆発', '原爆', '23分44秒', '押さなければ', '押したせいで', '無実', '嘘', 'うそ',
      '禁止だった', '禁止されて', 'だけで見つか', 'でだけ', '早く壊れ', '脅', '準備不足', '経験の浅い', '法廷', '証言',
      '死の橋', '潜水', '墜落', '100倍', '30本', '自殺', '裁判', '懲役', '有罪', '刑務所', 'HBO', 'ドラマ',
      '隠した', '隠ぺい', '隠蔽', '暴いた', 'ボタンが爆発', 'ボタンで爆発', '判明',
      'フィート', 'インチ', 'マイル', 'ポンド', 'ノット', '〜', '～']
NG_RE = [(r'4[3-4]分\d+秒', '0時43分・1時24分の秒'), (r'1時24分\d', '1時24分の秒'),
         (r'やけど.{0,24}(6時|1時間)', 'やけどの1人の時刻'),
         (r'(?<![0-9万,])(4,000|4000|1万6,000|1万6000|9万3,000|9万3000)人(が|も)亡くな', '長期の推計を亡くなった数として')]
SEC_OK = {'1時22分30秒', '1時23分4秒', '1時23分04秒', '1時23分39秒', '1時23分40秒', '1時23分43秒'}
SEC_RE = re.compile(r'\d+時\d+分\d+秒')
# 名前（10-22 カズヤくん「記録にある名前は出す」＝一次資料・写真の記録にある5人だけ・役職つき）
NAMES_OK = ['レガソフ', 'ジャトロフ', 'ヴォルコフ', 'ブリクス', 'ルイシコフ']
# 二次資料にしか名前が無い人・出さない人（当たったら E）
NAMES_NG = ['アキーモフ', 'アキモフ', 'トプトゥノフ', 'トプツノフ', 'ブリュハーノフ', 'ブリュハノフ', 'フォーミン', 'フォミン',
            'プラヴィク', 'プラビク', 'キベノク', 'ホデムチュク', 'シャシェノク', 'テレチェンコ', 'イグナテンコ',
            'ゴルバチョフ', 'シチェルビナ', 'コブゾン', 'シテインベルグ', 'アバギャン']
_spec = importlib.util.spec_from_file_location(
    'cts', r'C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証ch-案C見本\count_text_screens.py')
CTS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CTS)

# 写真の点の鍵（同じ鍵が2回＝BY-SA は E・ほかは W〈寄りを変えれば別の絵＝人が見る〉）
PHOTO_KEYS = [
    ('BY-SA', re.compile(r'IAEA (0279\d{4})')),
    ('C', re.compile(r'Commons (c\d+)')),
    ('A', re.compile(r'(USGS U[1-4]|NASA [A-Za-z0-9-]+|RIVM \S+|SPOT \S+|NARA N[12])')),
]
PAGE_RE = re.compile(r'図\s*p(\d+)')


def nopunct(s):
    return sum(1 for ch in s if ch not in PUNCT)


def fmt(s):
    return '%d分%02d秒' % (int(s) // 60, int(s) % 60)


def fig_type(pic):
    if PAGE_RE.match(pic):
        return '頁'
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


def main(path, roles_path=None):
    text = open(path, encoding='utf-8').read()
    cuts = CS.parse(text)
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
    names_ok = collections.Counter()
    chor = []
    for cid, pic, ls in cuts:
        ch = cid[:2]
        starts.setdefault(ch, t)
        d = per_ch.setdefault(ch, dict(cuts=0, lines=0, chars=0, photo=0, page=0, free=0, fig=0, panel=0, q=0))
        d['cuts'] += 1
        d['lines'] += len(ls)
        d['photo'] += pic.startswith('実写')
        d['page'] += bool(PAGE_RE.match(pic))
        d['free'] += pic.startswith('イメージ')
        d['panel'] += pic.startswith('panel')
        ft = fig_type(pic)
        if pic.startswith('図') and ft != '頁':
            d['fig'] += 1
            figs[ft] += 1
        fig_seq.append((cid, ft))
        if pic.startswith('実写'):
            seen = set()
            for kind, rx in PHOTO_KEYS:
                for m in rx.finditer(pic):
                    k = kind
                    if kind == 'C':
                        k = 'BY-SA' if 'BY-SA' in pic else 'A'
                    seen.add((k, m.group(1)))
            for k in seen:
                keys[k].append(cid)
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
                if re.search(r'[0-9０-９]', c):
                    E.append('E %s 聞き役の行に数字: %s' % (cid, c))
            if CS.STAR_RE.match(raw):
                E.append('E %s 決め所の行（24本目は決め所0）: %s' % (cid, c))
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」: %s' % (cid, w, c))
            for rx, why in NG_RE:
                if re.search(rx, c):
                    W.append('W %s 言わない形（%s）: %s' % (cid, why, c))
            for s in SEC_RE.findall(c):
                if s not in SEC_OK:
                    W.append('W %s 秒まで言う時刻「%s」（表に無い）: %s' % (cid, s, c))
            for nm in NAMES_NG:
                if nm in c:
                    E.append('E %s 出さない名前「%s」: %s' % (cid, nm, c))
            for nm in NAMES_OK:
                if nm in c:
                    names_ok[nm] += 1
            if 'チョルノービリ' in c:
                chor.append(cid)
        # 帰属（同じカットの中に出どころの語があるか）
        if '31人' in cut_text and not re.search(r'ソ連|発表|INSAG|1986年の報告|フォーラム|国会', cut_text):
            W.append('W %s 「31人」に帰属の語が無い' % cid)
        if re.search(r'(?<![0-9,])30人', cut_text) and not re.search(r'UNSCEAR|国連', cut_text):
            W.append('W %s 「30人」に帰属の語が無い' % cid)
        if re.search(r'(?<![0-9万,])(4,000人|1万6,000人)', cut_text) and not re.search(r'推計|見積', cut_text):
            W.append('W %s 長期の数に「推計」の語が無い' % cid)
        if ch == 'c1':
            hook.append('%s=%.1fs' % (cid, t))
    total_sec = t + ED01 / CPM * 60
    allch = tot + ED01
    d1 = n * SEC_PER_CUT
    d2 = allch / CPM * 60
    d3 = (sum(v['chars'] for v in per_ch.values()) + ED01) / CPM * 60
    nphoto = sum(v['photo'] for v in per_ch.values())
    npage = sum(v['page'] for v in per_ch.values())
    nfree = sum(v['free'] for v in per_ch.values())
    print('カット %d / 行 %d / 句読点なし %d字＋ed01 %d＝%d字（目標 %d・幅 %d〜%d＝%s）'
          % (n, len(lines), tot, ED01, allch, TARGET, LO, HI, '内' if LO <= allch <= HI else '🔴外'))
    print('写真（実写）%d＋報告書の頁 %d＝%d（%.1f%%）・フリー素材（イメージ）%d・図 %d・panel %d'
          % (nphoto, npage, nphoto + npage, (nphoto + npage) / max(1, n) * 100, nfree,
             sum(v['fig'] for v in per_ch.values()), sum(v['panel'] for v in per_ch.values())))
    allc = [CS.clean(l) for _, l in lines]
    print('1行 中央値 %d字・最長 %d字・1カット %.2f行' % (sorted(len(x) for x in allc)[len(allc) // 2],
                                               max(len(x) for x in allc), len(lines) / n))
    print('尺 ① カット×%.2f秒 %s ／ ② 句読点なし÷365 %s ／ ③ 章ごとの合計 %s → 開き %s'
          % (SEC_PER_CUT, fmt(d1), fmt(d2), fmt(d3), fmt(max(d1, d2, d3) - min(d1, d2, d3))))
    print('冒頭（÷365 を1カットずつ足した秒・カットの終わり）: ' + ' '.join(hook))
    print('章ごと: 章 始まり カット（目安） 行 句読点なし（目安・差） 分 写真＋頁（目安）割合 イメージ（目安） 図 聞き役（目安） 頭から最初の聞き役')
    for ch, v in per_ch.items():
        tg = CH_TARGET.get(ch, 0)
        fq = first_q.get(ch)
        fqs = (fq - starts[ch]) if fq is not None else None
        if ch != 'c1' and (fqs is None or fqs > HEAD_Q_SEC):
            W.append('W %s 章の頭から最初の聞き役まで %s' % (ch, '無し' if fqs is None else '%.1f秒' % fqs))
        pp = v['photo'] + v['page']
        if pp / max(1, v['cuts']) < 0.20:
            W.append('W %s 写真＋頁が %d/%d（20%%未満）' % (ch, pp, v['cuts']))
        print('  %s %s %3d（%3d） %3d %5d（%5d・%+4d） %5.2f %2d（%2d）%3.0f%% %2d（%d） %2d %2d（%d） %s'
              % (ch, fmt(starts[ch]), v['cuts'], CH_CUTS.get(ch, 0), v['lines'], v['chars'], tg,
                 v['chars'] - tg, v['chars'] / CPM, pp, CH_PHOTO.get(ch, 0), pp / max(1, v['cuts']) * 100,
                 v['free'], CH_FREE.get(ch, 0), v['fig'], v['q'], CH_Q.get(ch, 0),
                 '-' if fqs is None else '%.1f秒' % fqs))
    print('  ed01 %s' % fmt(t))
    print('図の型: ' + '・'.join('%s %d' % (k, v) for k, v in figs.most_common()))
    for k, v in figs.items():
        if k in TEMPLATE and v > 2:
            E.append('E 図の型「%s」が %d 回（全編で2回まで）' % (k, v))
    for (c0, f0), (c1, f1) in zip(fig_seq, fig_seq[1:]):
        if f0 and f0 == f1 and f0 in TEMPLATE:
            E.append('E 図の型「%s」が続く: %s → %s' % (f0, c0, c1))
        elif f0 and f0 == f1:
            W.append('W 図の型「%s」が続く（別の絵か人が見る）: %s → %s' % (f0, c0, c1))
    for (kind, key), cids in sorted(keys.items()):
        if len(cids) > 1:
            (E if kind == 'BY-SA' else W).append('%s 写真の点 %s %s を %d回: %s'
                                                 % ('E' if kind == 'BY-SA' else 'W', kind, key, len(cids), ' '.join(cids)))
    print('名前（出してよい5人）: ' + ('・'.join('%s×%d' % kv for kv in names_ok.items()) or '0'))
    print('「チョルノービリ」: %d回 %s' % (len(chor), ' '.join(chor)))
    if len(chor) != 1:
        W.append('W 「チョルノービリ」は本編で1回（いま %d回）' % len(chor))
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
    ok &= nopunct('ORM は') == 5             # 空白は数える（aq_build と同じ8種だけ除く）
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= abs(sum(CH_TARGET.values()) + ED01 - TARGET) <= 10 and sum(CH_CUTS.values()) == 242
    ok &= 65 <= sum(CH_Q.values()) <= 75 and abs(SEC_PER_CUT * 242 - 36.5 * 60) < 3.0
    ok &= fig_type('図 帯（14:00〜）') == '帯' and fig_type('図 p34 S1（6章）') == '頁' and fig_type('実写 x') is None
    ok &= PHOTO_KEYS[0][1].search('実写 IAEA 02790015（BY-SA 2.0）').group(1) == '02790015'
    ok &= bool(re.search(NG_RE[0][0], '0時43分27秒')) and not re.search(NG_RE[0][0], '0時43分ごろ')
    ok &= SEC_RE.findall('1時23分40秒に押された') == ['1時23分40秒']
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
