# -*- coding: utf-8 -*-
"""23本目 台本の机上の数え（22本目の m22.py を写し、23本目の章の目安・言わない語に替え、写真・フリー素材・図の型・点の重複・名前の数えを足した）。

  python ref/ep23/v1_build/m23.py <台本.md> --roles ref/ep23/v1_build/roles.tsv [--names <名前の一覧の md（git の外）>]
  python ref/ep23/v1_build/m23.py --selftest

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×9.28秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3-1 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・章の頭から最初の聞き役までの秒・
聞き役（tools/check_listener.judge をそのまま呼ぶ）・写真（画の欄の頭が「実写」）・フリー素材（「イメージ」）・
文字だけの画面（Vault の count_text_screens の分け方をそのまま使う）・図の型（「図 〈型〉」＝全編で2回まで・続けない）・
同じ写真の点の2回使い（BY-SA は1点1カット）・言わない語（kousei.md §7・§9・ルール §B2-4）・名前（--names の表の名前を全行に当てる＝出すのは頭の1字＋○だけ）。
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
SEC_PER_CUT = 9.28                 # kousei.md §2（36.5分÷236カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（tools/narration.py の3行＝22本目の④で数えた値）
TARGET = 13324                     # kousei.md §0（ed01 こみ・合格の幅 13,140〜13,505）
LO, HI = 13140, 13505
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
HEAD_Q_SEC = 20.0                  # 章の頭（扉の直後）から最初の聞き役まで（競合分析 §6-1「中」）
# kousei.md §3-1（cd は 548 から ed01 の46を引いた本文の目安）
CH_TARGET = {'c1': 365, 'c2': 1095, 'c3': 1095, 'c4': 1095, 'c5': 1278, 'c6': 1095, 'c7': 1095,
             'c8': 1095, 'c9': 1095, 'ca': 1095, 'cb': 1095, 'cc': 1278, 'cd': 502}
CH_CUTS = {'c1': 9, 'c2': 19, 'c3': 19, 'c4': 20, 'c5': 23, 'c6': 19, 'c7': 19,
           'c8': 19, 'c9': 19, 'ca': 19, 'cb': 19, 'cc': 23, 'cd': 9}
CH_Q = {'c1': 2, 'c2': 5, 'c3': 6, 'c4': 6, 'c5': 6, 'c6': 5, 'c7': 5,
        'c8': 5, 'c9': 5, 'ca': 5, 'cb': 5, 'cc': 6, 'cd': 2}
# kousei.md §5-1・§5-1b（写真90・フリー素材24の見込み）
CH_PHOTO = {'c1': 8, 'c2': 4, 'c3': 3, 'c4': 13, 'c5': 18, 'c6': 8, 'c7': 8,
            'c8': 3, 'c9': 4, 'ca': 3, 'cb': 7, 'cc': 8, 'cd': 3}
CH_FREE = {'c2': 4, 'c3': 4, 'c6': 2, 'c7': 2, 'c8': 4, 'c9': 3, 'ca': 2, 'cb': 2, 'cc': 1}
# 型の決まった図（10-15＝同じ型は全編で2回まで・続けない）。「模式」はどれも別の絵＝数だけ出す
TEMPLATE = {'断面', '平面', '帯', '年表', '暦', '時計', '地図', '棒', '箱', '札', '再現', '流れ', '比べ'}
# 言わない語（kousei.md §7・§9・ルール §B2-4 の死の語と煽り・§B1-2 の単位・§4-13 の波ダッシュ）。
# 当たったら人が文脈を見る（W）＝噂で引いて記録で閉じる行（c410・c414・c416・c610・c813・cc11）は当たって正しい
NG = ['死亡', '即死', '絶命', '悲劇', '地獄', '戦慄', '驚愕', '恐怖', '衝撃', '惨劇', '瞬間', 'ﾀﾋ',
      'すぐに交通', '交通が止められ', '客だけ', '石の椅子', '石でできた', '調理台', '40倍', '4人に3人',
      'その2日後', '瓦礫から助け', '報道は使わない', '全員が従業員', '3人とも', '崩れる前に逃げ',
      '4階建て', '12トン', '1993年', '1,300万', '1,500人', '42,000', '業界1位', '非常ベル', '20秒',
      '最後の救出', 'ここまでである', '正午', '5月に砂', '押し切', '社長が呼んだ', '違法', '下請け', '総額',
      'ロッテ', '高級', '4,000億', '3,000トン', '160トン', '1,000キロ', '100キロ',
      'フィート', 'インチ', 'マイル', 'ポンド', 'ノット', '坪', '〜', '～']
_spec = importlib.util.spec_from_file_location(
    'cts', r'C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証ch-案C見本\count_text_screens.py')
CTS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CTS)

# 写真の点の鍵（同じ鍵が2回＝BY-SA は E・A は W〈寄りを変えれば別の絵＝人が見る〉）
PHOTO_KEYS = [
    ('BY-SA', re.compile(r'BY-SA #(\d+)')),
    ('BY-SA', re.compile(r'(night_work|mourning|volunteers|crack_wall_01|屋上の跡|삼풍001|삼풍003|삼풍1\.jpg)')),
    ('A', re.compile(r'node/(\d+)')),
    ('A', re.compile(r'KOGL (\d+)')),
    ('A', re.compile(r'歴史編纂院 (\d{10}|崩壊後)')),
]


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


def load_names(p):
    """Vault の棚卸しノートの「## 2. 名前」の表から、名前の欄（2列目）を取る。名前は画面に出さない。"""
    if not p or not os.path.exists(p):
        return []
    on, names = False, []
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('## 2.'):
            on = True
            continue
        if on and ln.startswith('## '):
            break
        if on and ln.startswith('|') and not ln.startswith('|---'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if len(cells) >= 2 and cells[1] not in ('名前',):
                for nm in re.split(r'[・、,／/（）()\s]+', cells[1]):
                    nm = nm.strip('`*「」')
                    # 名前の欄に混じる名前でない語（時間・注・役の語）は除く（2026-10-18 に当たって確かめた3語）
                    if len(nm) >= 2 and not re.search(r'[0-9]', nm) and nm not in NAME_EXCLUDE:
                        names.append(nm)
    return sorted(set(names), key=len, reverse=True)


NAME_EXCLUDE = {'幹部', '記録に無い'}


def mask(nm):
    return nm[0] + '○' * (len(nm) - 1)


def main(path, roles_path=None, names_path=None):
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
    for cid, pic, ls in cuts:
        ch = cid[:2]
        starts.setdefault(ch, t)
        d = per_ch.setdefault(ch, dict(cuts=0, lines=0, chars=0, photo=0, free=0, fig=0, panel=0, q=0))
        d['cuts'] += 1
        d['lines'] += len(ls)
        d['photo'] += pic.startswith('実写')
        d['free'] += pic.startswith('イメージ')
        d['panel'] += pic.startswith('panel')
        ft = fig_type(pic)
        if pic.startswith('図'):
            d['fig'] += 1
            figs[ft] += 1
        fig_seq.append((cid, ft))
        if pic.startswith('実写'):
            seen = set()                 # 同じカットの画の欄で同じ鍵を2回書いても1回（副題に名前をくり返すため）
            for kind, rx in PHOTO_KEYS:
                for m in rx.finditer(pic):
                    seen.add((kind, m.group(1)))
            for k in seen:
                keys[k].append(cid)
        if not 1 <= len(ls) <= 3:
            E.append('E %s 行数 %d' % (cid, len(ls)))
        for i, raw in enumerate(ls, 1):
            c = CS.clean(raw)
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
            if CS.STAR_RE.match(raw):
                E.append('E %s 決め所の行（23本目は決め所0）: %s' % (cid, c))
            if who != speaker.WHO_Q:
                for w in NG:
                    if re.search(w, c):
                        W.append('W %s 言わない語「%s」: %s' % (cid, w, c))
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
    print('写真（実写）%d（%.1f%%）・フリー素材（イメージ）%d・図 %d・panel %d'
          % (nphoto, nphoto / max(1, n) * 100, nfree, sum(v['fig'] for v in per_ch.values()),
             sum(v['panel'] for v in per_ch.values())))
    allc = [CS.clean(l) for _, l in lines]
    print('1行 中央値 %d字・最長 %d字・1カット %.2f行' % (sorted(len(x) for x in allc)[len(allc) // 2],
                                               max(len(x) for x in allc), len(lines) / n))
    print('尺 ① カット×%.2f秒 %s ／ ② 句読点なし÷365 %s ／ ③ 章ごとの合計 %s → 開き %s'
          % (SEC_PER_CUT, fmt(d1), fmt(d2), fmt(d3), fmt(max(d1, d2, d3) - min(d1, d2, d3))))
    print('冒頭（÷365 を1カットずつ足した秒・カットの終わり）: ' + ' '.join(hook))
    print('章ごと: 章 始まり カット（目安） 行 句読点なし（目安・差） 分 写真（目安） イメージ（目安） 図 聞き役（目安） 頭から最初の聞き役')
    for ch, v in per_ch.items():
        tg = CH_TARGET.get(ch, 0)
        fq = first_q.get(ch)
        fqs = (fq - starts[ch]) if fq is not None else None
        if ch != 'c1' and (fqs is None or fqs > HEAD_Q_SEC):   # c1＝つかみ（扉の前）は冒頭46秒の決まりで見る
            W.append('W %s 章の頭から最初の聞き役まで %s' % (ch, '無し' if fqs is None else '%.1f秒' % fqs))
        print('  %s %s %3d（%3d） %3d %5d（%5d・%+4d） %5.2f %2d（%2d） %2d（%d） %2d %2d（%d） %s'
              % (ch, fmt(starts[ch]), v['cuts'], CH_CUTS.get(ch, 0), v['lines'], v['chars'], tg,
                 v['chars'] - tg, v['chars'] / CPM, v['photo'], CH_PHOTO.get(ch, 0), v['free'],
                 CH_FREE.get(ch, 0), v['fig'], v['q'], CH_Q.get(ch, 0),
                 '-' if fqs is None else '%.1f秒' % fqs))
    print('  ed01 %s' % fmt(t))
    # 図の型
    print('図の型: ' + '・'.join('%s %d' % (k, v) for k, v in figs.most_common()))
    for k, v in figs.items():
        if k in TEMPLATE and v > 2:
            E.append('E 図の型「%s」が %d 回（全編で2回まで）' % (k, v))
    for (c0, f0), (c1, f1) in zip(fig_seq, fig_seq[1:]):
        if f0 and f0 == f1 and f0 in TEMPLATE:
            E.append('E 図の型「%s」が続く: %s → %s' % (f0, c0, c1))
        elif f0 and f0 == f1:
            W.append('W 図の型「%s」が続く（別の絵か人が見る）: %s → %s' % (f0, c0, c1))
    # 写真の点の2回使い
    for (kind, key), cids in sorted(keys.items()):
        if len(cids) > 1:
            (E if kind == 'BY-SA' else W).append('%s 写真の点 %s %s を %d回: %s'
                                                 % ('E' if kind == 'BY-SA' else 'W', kind, key, len(cids), ' '.join(cids)))
    # 聞き役
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
    # 文字だけの画面（Vault の分け方）
    tc = CTS.parse(path)
    CTS.report(tc, {}, None, '画の欄のまま')
    # 名前
    names = load_names(names_path)
    if names_path:
        hits = collections.Counter()
        for ln in text.split('\n'):
            for nm in names:
                if nm in ln:
                    hits[nm] += 1
        print('名前の洗い出し: 一覧 %d語 → 当たり %d語 %s' % (len(names), len(hits),
                                                ' '.join('%s×%d' % (mask(k), v) for k, v in hits.items())))
        for k in hits:
            E.append('E 名前が台本の中にある: %s' % mask(k))
    for x in W:
        print('⚠️ ' + x)
    for x in E:
        print('🔴 ' + x)
    print('E %d件（形）・聞き役 E %d件・W %d件・言わない語 %d件'
          % (len(E), len(e2), len(w2) + len(W), sum(1 for x in W if '言わない語' in x)))
    return len(E) + len(e2)


def selftest():
    ok = nopunct('「あ、い。」（う）・え？お！') == 5
    ok &= nopunct('MBI は') == 5             # 空白は数える（aq_build と同じ8種だけ除く）
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= sum(CH_TARGET.values()) + ED01 == TARGET and sum(CH_CUTS.values()) == 236 and sum(CH_Q.values()) == 63
    ok &= sum(CH_PHOTO.values()) == 90 and sum(CH_FREE.values()) == 24
    ok &= abs(SEC_PER_CUT * 236 - 36.5 * 60) < 1.0
    ok &= fig_type('図 帯（14:00〜）') == '帯' and fig_type('図 柱の断面の比べ（…）') == '柱の断面の比べ' and fig_type('実写 x') is None
    ok &= bool(PHOTO_KEYS[0][1].search('実写 BY-SA #176（俯瞰）')) and PHOTO_KEYS[2][1].search('研究院 node/52399').group(1) == '52399'
    ok &= mask('가나다') == '가○○'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    npth = sys.argv[sys.argv.index('--names') + 1] if '--names' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp, npth) else 0)
