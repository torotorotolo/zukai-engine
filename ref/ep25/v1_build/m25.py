# -*- coding: utf-8 -*-
"""25本目 台本の机上の数え（24本目の m24.py を写し、25本目の章の目安・言わない語・帰属・秒の表に替えた）。

  python ref/ep25/v1_build/m25.py <台本.md> --roles ref/ep25/v1_build/roles.tsv
  python ref/ep25/v1_build/m25.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×9.05秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3 の目安と並べる。
⚠️ c1 は materials.md §6 の冒頭＝c101〜c107・約62秒で最初の見出し＝kousei §3 の c1（2.0分・13カット）の残り6カットは c2 の頭へ）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真（画の欄の頭が「実写」）・報告書の頁（「図 p〈PDF頁〉」）・フリー素材（「イメージ」）・文字だけの画面（Vault の count_text_screens）・
図の型（「図 〈型〉」＝全編で2回まで・続けない）・同じ写真の点の2回使い（BY-SA は1点1カット）・言わない語（sources.md §3・§6・legend §2-1・1通目）・
帰属（115・549・133・108・104・95・1分半・40メートル・9時17分57秒）・秒まで言う時刻（表の値だけ）・呼び名（JR西日本の呼び名・報告書の正式名を各1回）・
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
SEC_PER_CUT = 9.05                 # kousei.md §0（36.5分÷242カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（23・24本目の④で数えた値）
TARGET = 13320                     # kousei.md §0（ed01 こみ・合格の幅＝36分〜37分）
LO, HI = 13140, 13505
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで
# kousei.md §3（c1＝約1分に縮めた分 365字・6カットを c2 へ。cb は 730 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 365, 'c2': 1643, 'c3': 1643, 'c4': 1095, 'c5': 1825, 'c6': 1278, 'c7': 1460,
             'c8': 730, 'c9': 1278, 'ca': 1278, 'cb': 684}
CH_CUTS = {'c1': 7, 'c2': 29, 'c3': 30, 'c4': 20, 'c5': 33, 'c6': 23, 'c7': 27,
           'c8': 13, 'c9': 23, 'ca': 23, 'cb': 14}
CH_Q = {'c1': 1, 'c2': 8, 'c3': 7, 'c4': 4, 'c5': 9, 'c6': 6, 'c7': 7,
        'c8': 4, 'c9': 6, 'ca': 6, 'cb': 3}
# materials.md §0（この事故の写真・紙面 約60〜70カット＝25〜29%）の章への割り振り（目安＝W も出さない）
CH_PHOTO = {'c1': 6, 'c2': 9, 'c3': 5, 'c4': 9, 'c5': 5, 'c6': 7, 'c7': 5,
            'c8': 3, 'c9': 4, 'ca': 4, 'cb': 7}
CH_FREE = {'c1': 0, 'c2': 2, 'c3': 1, 'c4': 0, 'c5': 3, 'c6': 1, 'c7': 2, 'c8': 1, 'c9': 2, 'ca': 1, 'cb': 1}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す
TEMPLATE = {'断面', '平面', '帯', '年表', '暦', '時計', '地図', '棒', '箱', '札', '再現', '流れ', '比べ', '時刻表',
            '案C-A', '案C-B', '案C-C', '案C-D', '案C-E', '案C-F', '並べ', '路線'}
# 言わない語（sources.md §3・§6・legend §2-1・1通目・ルール §B2-4 の死の語と煽り・§B1-2 の単位・§4-13 の波ダッシュ）。
# 当たったら人が文脈を見る（W）＝「よく語られる話」で引いて記録で閉じる行・打ち消しの行は当たって正しい
NG = ['死亡', '即死', '絶命', '悲劇', '地獄', '戦慄', '驚愕', '恐怖', '惨劇', '瞬間', 'ﾀﾋ', '衝撃', '死因', '遺体', '遺族の',
      '軽い車体', '軽量', '草むしり', '見せしめ', '懲罰', '700人', '七百人', '付け替えが原因', '罪に問われ',
      '予見でき', '居眠り', '携帯', '賃金', '給料', 'ミス', '利益優先', '過密ダイヤ', '隠ぺい', '隠蔽', '隠した', '判明',
      '突っ込', '暴走', '最悪', '史上', '戦後最悪',
      'フィート', 'インチ', 'マイル', 'ポンド', 'ノット', '〜', '～']
NG_RE = [(r'急い.{0,14}(無い|ない|0件|一度も|出てこ)', '報告書に「急いで」は無い（p.194 に1件ある）'),
         (r'(?<![0-9])95キロから70キロ', '付け替え前の95km＝検察の主張'),
         (r'誰も.{0,8}(罪|責任|罰)', '誰も罪に問われなかった'),
         (r'(?<![0-9,])(約)?700(人|名)', '乗客約700人')]
# 帰属（同じカットの中に出どころの語が要る数）
ATTR = [(r'115キロ', r'判決|裁判|最高裁|地裁|裁判所', '115（判決）'),
        (r'549人', r'消防|兵庫県|県の', '549（消防・県）'),
        (r'133キロ', r'会社|JR西日本|公表', '133（会社の公表）'),
        (r'108キロ', r'判決|地裁|裁判', '108（神戸地裁）'),
        (r'104キロ', r'報告書|定員', '104（報告書 p.230・定員150名）'),
        (r'(?<![0-9])95キロから70キロ', r'検察', '95（検察の主張）'),
        (r'1分半', r'車掌|指令', '1分半（車掌の報告）'),
        (r'40メートル', r'社長|国会|申告|車掌', '40m（国会の答弁・車掌の見立て）'),
        (r'9時17分57秒', r'録音', '9:17:57（録音ファイルの時刻）'),
        (r'(?<![0-9])8メートル', r'車掌|報告|指令|復唱|メーター', '8m（車掌の報告）')]
WAZATO = re.compile(r'わざと|意識的に')
# 報告書の「ごろ」「前後」の時刻（p.9〜13）と、付図24 の帯から読んだ秒（sources.md §4）だけ
SEC_OK = {'8時54分43秒', '8時56分12秒', '8時56分14秒', '9時03分45秒', '9時04分00秒', '9時07分40秒', '9時11分20秒',
          '9時13分39秒', '9時15分43秒', '9時16分10秒', '9時17分38秒', '9時17分39秒', '9時17分57秒', '9時18分09秒', '9時18分9秒',
          '9時18分14秒', '9時18分22秒', '9時18分27秒', '9時18分29秒', '9時18分31秒', '9時18分35秒', '9時18分40秒',
          '9時18分50秒', '9時18分53秒', '9時18分54秒', '9時18分59秒', '9時19分04秒', '9時19分4秒', '9時19分15秒'}
SEC_RE = re.compile(r'\d+時\d+分\d+秒')
NAMES_FILE = r'C:\Users\konar\Desktop\zukai-engine\ref\ep25\src\names_private.txt'   # git の外（1行1名・# は注）
_spec = importlib.util.spec_from_file_location(
    'cts', r'C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証ch-案C見本\count_text_screens.py')
CTS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CTS)

# 写真の点の鍵（同じ鍵が2回＝BY-SA は E・ほかは W〈付図は PDL1.0 で切り出し可＝1点から2カットまで＝人が見る〉）
PHOTO_KEYS = [
    ('C', re.compile(r'Commons #(\d+)')),
    ('A', re.compile(r'(付図\d+[a-zア-ン]?|国交省 \w+|空中写真 \w+|衛星写真 \w+|後年 \w+)')),
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
    wazato = []
    names = load_names()
    jrw_name, rep_name = [], []
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
                if re.search(r'[0-9０-９〇一二三四五六七八九十百千]', c):
                    E.append('E %s 聞き役の行に数字（漢数字も）: %s' % (cid, c))
            if CS.STAR_RE.match(raw):
                E.append('E %s 決め所の行（25本目は決め所0）: %s' % (cid, c))
            for w in NG:
                if w in c:
                    W.append('W %s 言わない語「%s」: %s' % (cid, w, c))
            for rx, why in NG_RE:
                if re.search(rx, c):
                    W.append('W %s 言わない形（%s）: %s' % (cid, why, c))
            for s in SEC_RE.findall(c):
                if s not in SEC_OK:
                    W.append('W %s 秒まで言う時刻「%s」（表に無い）: %s' % (cid, s, c))
            if WAZATO.search(c):
                wazato.append(cid)
            if names:
                for nm in names:
                    if nm in c or nm in pic:
                        E.append('E %s 名前の網に当たった（git の外の表の %d字の名前）' % (cid, len(nm)))
            if '福知山線列車事故' in c:
                jrw_name.append(cid)
            if '列車脱線事故' in c:
                rep_name.append(cid)
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
    print('「わざと」「意識的に」の行があるカット（帰属か打ち消しかを人が見る）: %s' % (' '.join(wazato) or '0'))
    print('呼び名：JR西日本「福知山線列車事故」%d回 %s ／ 報告書の正式名「…列車脱線事故」%d回 %s'
          % (len(jrw_name), ' '.join(jrw_name), len(rep_name), ' '.join(rep_name)))
    if len(jrw_name) != 1 or len(rep_name) != 1:
        W.append('W 呼び名は本編で各1回（JR西日本 %d回・報告書 %d回）' % (len(jrw_name), len(rep_name)))
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
    ok &= nopunct('ATS は') == 5             # 空白は数える（aq_build と同じ8種だけ除く）
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= abs(sum(CH_TARGET.values()) + ED01 - TARGET) <= 10 and sum(CH_CUTS.values()) == 242
    ok &= 55 <= sum(CH_Q.values()) <= 75 and abs(SEC_PER_CUT * 242 - 36.5 * 60) < 3.0
    ok &= fig_type('図 帯（9時18分〜）') == '帯' and fig_type('図 p233 R1（印刷 p.222）') == '頁' and fig_type('実写 x') is None
    ok &= PHOTO_KEYS[0][1].search('実写 Commons #4（BY-SA 2.0）').group(1) == '4'
    ok &= PHOTO_KEYS[1][1].search('実写 付図12 R3（空撮）').group(1) == '付図12'
    ok &= bool(re.search(NG_RE[0][0], '報告書に急いでの字は一度も出てこない')) and not re.search(NG_RE[0][0], '急いでいても')
    ok &= bool(re.search(NG_RE[1][0], '時速95キロから70キロに')) and not re.search(NG_RE[1][0], '120キロから95キロに')
    ok &= bool(re.search(NG_RE[3][0], '乗客約700人')) and not re.search(NG_RE[3][0], '1,700人')
    ok &= SEC_RE.findall('9時18分54秒ごろに脱線') == ['9時18分54秒']
    ok &= not re.search(ATTR[0][1], '時速約115キロ') and bool(re.search(ATTR[0][1], '最高裁の決定は時速約115キロ'))
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
