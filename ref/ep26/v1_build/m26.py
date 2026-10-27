# -*- coding: utf-8 -*-
"""26本目 台本の机上の数え（25本目の m25.py を写し、26本目の章の目安・言わない語・帰属・時計の当て方に替えた）。

  python ref/ep26/v1_build/m26.py <台本.md> --roles ref/ep26/v1_build/roles.tsv
  python ref/ep26/v1_build/m26.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×8.98秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真（画の欄の頭が「実写」）・報告書の頁（「図 p〈PDF頁〉」）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ写真の点の2回使い（BY-SA は1点1カット）・言わない語（sources.md §10・1通目）・
帰属（割れる数と見方＝同じカットに出どころの語）・時計（時刻を言う章は、その章の中で先に「〜号の時計」を言う＝sources.md §6）・
呼び名（「タイタニック号沈没事故」・3つの調べの呼び名・「商務省の調査」と呼ばない）・
名前（git の外の src/names_private.txt に書いた名前が台本に1つでもあれば E＝公開のリポに名前を書かないため、道具の側にも名前を書かない）。
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
SEC_PER_CUT = 8.98                 # kousei.md §0（36.5分÷244カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（23〜25本目の④で数えた値）
TARGET = 13320                     # kousei.md §0（ed01 こみ・合格の幅＝36分〜37分）
LO, HI = 13140, 13505
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで
# kousei.md §3（cb は 365 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 365, 'c2': 1095, 'c3': 1278, 'c4': 913, 'c5': 1095, 'c6': 2190, 'c7': 1278,
             'c8': 1460, 'c9': 2373, 'ca': 913, 'cb': 319}
CH_CUTS = {'c1': 7, 'c2': 20, 'c3': 23, 'c4': 17, 'c5': 20, 'c6': 40, 'c7': 23,
           'c8': 27, 'c9': 43, 'ca': 17, 'cb': 7}
CH_Q = {'c1': 2, 'c2': 5, 'c3': 6, 'c4': 4, 'c5': 5, 'c6': 10, 'c7': 4,
        'c8': 7, 'c9': 12, 'ca': 4, 'cb': 2}
# materials.md §0（この事故の写真・紙面 約70〜85カット＝29〜35%）の章への割り振り（目安＝W も出さない）
CH_PHOTO = {'c1': 6, 'c2': 12, 'c3': 7, 'c4': 5, 'c5': 6, 'c6': 8, 'c7': 12,
            'c8': 8, 'c9': 8, 'ca': 4, 'cb': 4}
CH_FREE = {'c1': 1, 'c2': 0, 'c3': 1, 'c4': 2, 'c5': 2, 'c6': 1, 'c7': 1, 'c8': 0, 'c9': 1, 'ca': 1, 'cb': 1}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す
TEMPLATE = {'断面', '平面', '帯', '年表', '暦', '時計', '地図', '棒', '箱', '札', '再現', '流れ', '比べ', '時刻表',
            '案C-1', '案C-2', '案C-3', '案C-4', '案C-5', '案C-6', '案C-7', '案C-8', '並べ', '航路', '氷域', '対照', '割合'}
# 案C の場面（materials.md §8 の ①〜⑥＝案C-1〜6。④で ① の船橋を時刻で3つに分けた＝案C-1 23時ごろ・案C-7 0時20分〜1時すぎ・案C-8 2時すぎ）
# 言わない語（sources.md §10・1通目・ルール §B2-4 の死の語と煽り・§4-13 の波ダッシュ）。
# 当たったら人が文脈を見る（W）＝「よく語られる話」で引いて記録で閉じる行・打ち消しの行は当たって正しい
NG = ['死亡', '即死', '絶命', '悲劇', '地獄', '戦慄', '驚愕', '恐怖', '惨劇', '瞬間', 'ﾀﾋ', '衝撃', '遺体', '死体',
      '見殺し', '無視', '真犯人', '隠ぺい', '隠蔽', '判明', '最悪', '史上', '不沈', '火箭', '設計ミス', 'リベット',
      '〜', '～']
NG_RE = [(r'(?<![0-9,])1,?500人', '「1,500人」は使わない（英 1,490／米 1,517）'),
         (r'以上が亡くな', '「〜人以上が亡くなった」は使わない'),
         (r'商務省の(調査|審問)', '「商務省の調査」と呼ばない（MAIB p.5）'),
         (r'救えなかった|救えなかっ', '「救えなかった」を言い切らない（帰属か打ち消しかを人が見る）'),
         (r'見えなかった(?!と)', '「見えなかった」の言い切り（帰属を人が見る）')]
# 帰属（同じカットの中に出どころの語が要る数と見方）
ATTR = [(r'1,?517', r'米国|上院|アメリカ', '1,517（米国上院）'),
        (r'見えていなかった', r'次長|たぶん|可能性|見方|考え', '見えていなかった（次長の見方）'),
        (r'見えていた', r'調査官|船長|航海士|証言|報告書|見方|考え|次長|見習い', '見えていた（帰属）'),
        (r'救えた', r'報告書|審問|1912|かもしれない|上院', '救えた（1912年の英国の報告）'),
        (r'約9キロから19キロ|約9キロから13キロ', r'調査官', '5〜10・5〜7マイル（調査官）'),
        (r'約31キロから37キロ|約33キロ', r'次長', '17〜20・約18マイル（次長）'),
        (r'約15キロから19キロ', r'1912|報告書|審問|助言', '8〜10マイル（1912年の報告）'),
        (r'約35キロ|約36キロ', r'船長|報告書|上院|米国', '19〜19½マイル（船長の数）'),
        (r'差.{0,8}数分|数分ほど', r'次長|調べ直し|1992|海難調査局', '時計の差は数分（MAIB）'),
        (r'変わらなかった', r'次長|距離|正しければ', '結果は変わらなかった（次長・条件つき）'),
        (r'ダース', r'四等航海士|ボックスホール|証言', '半ダースから1ダース（四等航海士）'),
        (r'8発|8つ', r'報告書|見習い|ストーン|二等航海士|審問|ギブソン', '8発（報告書・見習い）'),
        (r'37秒', r'試験|見積|オリンピック号', '37秒（姉妹船の試験からの見積もり）'),
        (r'Keep out|キープ・アウト', r'英国|報告書|審問', '「Keep out」（英国の報告）'),
        (r'黙れ|Shut up', r'米国|公聴会|上院', '「Shut up」（米国の公聴会）'),
        (r'カリフォルニアン号だった', r'報告書|1912|審問|疑い|見た', '見えた船＝カリフォルニアン号（1912年の報告）'),
        (r'第三の船|別の船だった|ほかの船だった', r'次長|たぶん|見方|可能性', '第三の船（次長の見方）')]
# 時刻（語り）。章の中で、最初の時刻より前に「〜号の時計」（またはニューヨークの時刻）を言っていなければ W
TIME_RE = re.compile(r'(?<![0-9])\d{1,2}時(\d{1,2}分)?')
CLOCK_RE = re.compile(r'(タイタニック号|カリフォルニアン号|カルパチア号|それぞれの船|船ごと|この船|その船|自分の船)の時計|ニューヨークの時刻')
PICCLOCK_RE = re.compile(r'(?<![0-9])\d{1,2}:\d{2}')
NAMES_FILE = r'C:\Users\konar\Desktop\zukai-engine\ref\ep26\src\names_private.txt'   # git の外（1行1名・# は注）
_spec = importlib.util.spec_from_file_location(
    'cts', r'C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証ch-案C見本\count_text_screens.py')
CTS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CTS)

# 写真の点の鍵（materials.md の番号 S1-002 ほか・NOAA の映像・NARA の番号）。同じ鍵が2回＝BY-SA は E・ほかは W（人が見る）
PHOTO_KEYS = [
    ('C', re.compile(r'(?<![A-Za-z0-9])(S\d{1,2}-[A-Z]?\d{2,3})(?![0-9])')),
    ('A', re.compile(r'(NOAA 20\d\d \S+|NARA \d+)')),
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


def load_names():
    if not os.path.exists(NAMES_FILE):
        return None
    return [ln.strip() for ln in open(NAMES_FILE, encoding='utf-8') if ln.strip() and not ln.startswith('#')]


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
    names = load_names()
    accident_name, inq = [], collections.Counter()
    clock_seen = {}
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
        if PICCLOCK_RE.search(pic) and '時計' not in pic:
            W.append('W %s 画の欄の時刻に「どの船の時計か」が無い: %s' % (cid, pic[:60]))
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
                E.append('E %s 決め所の行（26本目は決め所0）: %s' % (cid, c))
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」: %s' % (cid, w, c))
            for rx, why in NG_RE:
                if re.search(rx, c):
                    W.append('W %s 言わない形（%s）: %s' % (cid, why, c))
            if CLOCK_RE.search(c):
                clock_seen.setdefault(ch, cid)
            if TIME_RE.search(c) and ch not in clock_seen and who != speaker.WHO_Q:
                W.append('W %s この章でまだ「どの船の時計か」を言わずに時刻: %s' % (cid, c))
            if names:
                for nm in names:
                    if nm in c or nm in pic:
                        E.append('E %s 名前の網に当たった（git の外の表の %d字の名前）' % (cid, len(nm)))
            if 'タイタニック号沈没事故' in c:
                accident_name.append(cid)
            for k in ('英国の審問', '米国上院の調査', '海難調査局'):
                if k in c:
                    inq[k] += 1
        for rx, need, why in ATTR:
            if re.search(rx, cut_text) and not re.search(need, cut_text):
                W.append('W %s 帰属の語が無い（%s）' % (cid, why))
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
    if allc:
        print('1行 中央値 %d字・最長 %d字・1カット %.2f行' % (sorted(len(x) for x in allc)[len(allc) // 2],
                                                   max(len(x) for x in allc), len(lines) / max(1, n)))
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
        elif f0 and f0 == f1 and f0 != '頁':
            W.append('W 図の型「%s」が続く（別の絵か人が見る）: %s → %s' % (f0, c0, c1))
    for (kind, key), cids in sorted(keys.items()):
        if len(cids) > 1:
            (E if kind == 'BY-SA' else W).append('%s 写真の点 %s %s を %d回: %s'
                                                 % ('E' if kind == 'BY-SA' else 'W', kind, key, len(cids), ' '.join(cids)))
    print('呼び名：「タイタニック号沈没事故」%d回 %s ／ 調べの呼び名 %s'
          % (len(accident_name), ' '.join(accident_name), dict(inq)))
    if not accident_name:
        W.append('W 事件名「タイタニック号沈没事故」が本編に無い')
    for k in ('英国の審問', '米国上院の調査', '海難調査局'):
        if not inq[k]:
            W.append('W 調べの呼び名「%s」が本編に無い' % k)
    print('時計を先に言った章: ' + ' '.join('%s@%s' % kv for kv in clock_seen.items()))
    print('名前の網: ' + ('🔴 表が無い（src/names_private.txt）' if names is None else '%d名を当てた' % len(names)))
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
    ok &= nopunct('MAIB は') == 6            # 空白は数える（aq_build と同じ8種だけ除く）
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= abs(sum(CH_TARGET.values()) + ED01 - TARGET) <= 10 and sum(CH_CUTS.values()) == 244
    ok &= 55 <= sum(CH_Q.values()) <= 75 and abs(SEC_PER_CUT * 244 - 36.5 * 60) < 3.0
    ok &= fig_type('図 帯（カリフォルニアン号の時計）') == '帯' and fig_type('図 p60 G1（印刷 p.60）') == '頁'
    ok &= fig_type('実写 S1-002') is None
    ok &= PHOTO_KEYS[0][1].search('実写 S8-625（NARA・3000px）').group(1) == 'S8-625'
    ok &= PHOTO_KEYS[0][1].search('実写 S8-E03（977px）').group(1) == 'S8-E03'
    ok &= bool(re.search(NG_RE[0][0], '1,500人以上')) and not re.search(NG_RE[0][0], '11,500人')
    ok &= bool(re.search(NG_RE[2][0], '商務省の調査では')) and not re.search(NG_RE[2][0], '商務省の規則')
    ok &= bool(TIME_RE.search('1時10分ごろ')) and bool(TIME_RE.search('夜11時ごろ')) and not TIME_RE.search('1912年')
    ok &= bool(CLOCK_RE.search('カリフォルニアン号の時計で')) and not CLOCK_RE.search('カリフォルニアン号の甲板')
    ok &= bool(PICCLOCK_RE.search('札「1:10」')) and not PICCLOCK_RE.search('札「1,490人」')
    a = dict((w, (rx, need)) for rx, need, w in ATTR)
    ok &= not re.search(a['17〜20・約18マイル（次長）'][1], '約33キロ（18マイル）離れていた')
    ok &= bool(re.search(a['17〜20・約18マイル（次長）'][1], '次長は約33キロ（18マイル）と見た'))
    ok &= bool(CL.NUM_RE.search('一緒に')) and not CL.NUM_RE.search('どっちなの？')
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
