# -*- coding: utf-8 -*-
"""21本目 台本の机上の数え（20本目の m20.py を写し、9.24秒・章の目安・言わない語の拾いを足した）。

  python ref/ep21/v1_build/m21.py <台本.md> --roles ref/ep21/v1_build/roles.tsv [--selftest]

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ の8種を除く＝ルール §5a-28・aq_build と同じ）・
3通りの尺（①カット×9.24秒 ②句読点なし÷365〈ed01 こみ〉 ③章ごとの合計）・章ごと（kousei.md §3-1 の目安と並べる）・
1行41字超・1カット1〜3行・冒頭の秒（÷365 を1カットずつ）・聞き役（tools/check_listener.judge をそのまま呼ぶ）・
写真（画の欄の頭が「実写」）・文字だけの画面（Vault の count_text_screens の分け方をそのまま使う）・
言わない語（kousei.md §7・ルール §B2-4）の拾い。
⚠️ check_script の尺の式は ElevenLabs／Otani の定数のまま＝ゆっくりの回は信じない（ルール §5a-28b）。尺はこの道具の②で見る。
"""
import collections
import importlib.util
import os
import re
import sys

sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
import check_script as CS          # noqa: E402  parse・clean を使う（道具は直さない）
import check_listener as CL        # noqa: E402  judge をそのまま呼ぶ
import speaker                     # noqa: E402

PUNCT = set('、。？！「」（）・')
CPM = 365.0
SEC_PER_CUT = 9.24                 # kousei.md §2（36.5分÷237カット）
ED01 = 46                          # 共通エンディング ed01 の句読点なし字数（tools/narration.py の3行）
TARGET = 13320                     # kousei.md §0（ed01 こみ・合格の幅 13,140〜13,505）
LO, HI = 13140, 13505
HOOK_SEC = 46.0                    # 冒頭の引きはこの秒より前（ルール §4-7）
CH_TARGET = {'c1': 365, 'c2': 1004, 'c3': 1095, 'c4': 1460, 'c5': 1186, 'c6': 1369, 'c7': 913,
             'c8': 1825, 'c9': 1186, 'ca': 1186, 'cb': 1095, 'cc': 639}
CH_CUTS = {'c1': 9, 'c2': 18, 'c3': 19, 'c4': 26, 'c5': 21, 'c6': 24, 'c7': 16,
           'c8': 32, 'c9': 21, 'ca': 21, 'cb': 19, 'cc': 11}
CH_Q = {'c1': 2, 'c2': 4, 'c3': 6, 'c4': 7, 'c5': 6, 'c6': 7, 'c7': 4,
        'c8': 8, 'c9': 6, 'ca': 6, 'cb': 5, 'cc': 2}
# 言わない語（kousei.md §7 の「言わない」の芯・§B2-4 の死の語・HYPE）。正規表現。当たったら人が文脈を見る（W）
#   「0分」は数字の後ろの0（20分・30分）と時刻の「10時0分」を拾わないよう、前が数字でも「時」でもない時だけ
NG = ['死亡', '即死', r'(?<![0-9０-９時])0分', 'ゼロ分', '満載', '誰もが', '一気に', '測っている量', '誰も見ていない',
      '誰も気づ', '1機も乗っ取られ', '冷戦のころの配置', '無線に乗ってしまった', 'その日のうちに', '寝泊まり',
      '足止め', '最後の1機にした', '9時5分に把握', '撃墜された', '乗客が操縦室に入', '隠蔽', '悲劇', '戦慄', '驚愕',
      '絶命', '恐怖の', '闇']
_spec = importlib.util.spec_from_file_location(
    'cts', r'C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証ch-案C見本\count_text_screens.py')
CTS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CTS)


def nopunct(s):
    return sum(1 for ch in s if ch not in PUNCT)


def fmt(s):
    return '%d分%02d秒' % (int(s) // 60, int(s) % 60)


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
    for k, (cid, pic, ls) in enumerate(cuts):
        ch = cid[:2]
        starts.setdefault(ch, t)
        d = per_ch.setdefault(ch, dict(cuts=0, lines=0, chars=0, photo=0, q=0))
        d['cuts'] += 1
        d['lines'] += len(ls)
        d['photo'] += pic.startswith('実写')
        if not 1 <= len(ls) <= 3:
            E.append('E %s 行数 %d' % (cid, len(ls)))
        for i, raw in enumerate(ls, 1):
            c = CS.clean(raw)
            if len(c) > 41:
                E.append('E %s 1行%d字: %s' % (cid, len(c), c))
            np_ = nopunct(c)
            who = speaker.split(raw)[0]
            rows.append((cid, i, who, speaker.bare(CS.STAR_RE.sub('', raw).replace('**', '').strip()), t))
            t += np_ / CPM * 60
            d['chars'] += np_
            tot += np_
            if who == speaker.WHO_Q:
                d['q'] += 1
            if CS.STAR_RE.match(raw):
                E.append('E %s 決め所の行（21本目は決め所0）: %s' % (cid, c))
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
    print('カット %d / 行 %d / 句読点なし %d字＋ed01 %d＝%d字（目標 %d・幅 %d〜%d＝%s）/ 写真（実写）%d（%.1f%%）'
          % (n, len(lines), tot, ED01, allch, TARGET, LO, HI, '内' if LO <= allch <= HI else '🔴外',
             nphoto, nphoto / max(1, n) * 100))
    allc = [CS.clean(l) for _, l in lines]
    print('1行 中央値 %d字・最長 %d字・1カット %.2f行' % (sorted(len(x) for x in allc)[len(allc) // 2],
                                               max(len(x) for x in allc), len(lines) / n))
    print('尺 ① カット×%.2f秒 %s ／ ② 句読点なし÷365 %s ／ ③ 章ごとの合計 %s → 開き %s'
          % (SEC_PER_CUT, fmt(d1), fmt(d2), fmt(d3), fmt(max(d1, d2, d3) - min(d1, d2, d3))))
    print('冒頭（÷365 を1カットずつ足した秒・カットの終わり）: ' + ' '.join(hook))
    print('章ごと: 章 始まり カット（目安） 行 句読点なし（目安・差） 分 写真 聞き役（目安）')
    for ch, v in per_ch.items():
        tg = CH_TARGET.get(ch, 0)
        print('  %s %s %3d（%3d） %3d %5d（%5d・%+4d） %5.2f %2d %2d（%d）'
              % (ch, fmt(starts[ch]), v['cuts'], CH_CUTS.get(ch, 0), v['lines'], v['chars'], tg,
                 v['chars'] - tg, v['chars'] / CPM, v['photo'], v['q'], CH_Q.get(ch, 0)))
    print('  ed01 %s' % fmt(t))
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
    print('E %d件（形）・聞き役 E %d件・W %d件・言わない語 %d件' % (len(E), len(e2), len(w2), len(W)))
    return len(E) + len(e2)


def selftest():
    ok = nopunct('「あ、い。」（う）・え？お！') == 5
    ok &= nopunct('NEADS は') == 7            # 空白は数える（aq_build と同じ8種だけ除く）
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= sum(CH_TARGET.values()) == 13323 and sum(CH_CUTS.values()) == 237 and sum(CH_Q.values()) == 63
    ok &= not re.search(NG[2], '8時20分に離陸') and bool(re.search(NG[2], '猶予は0分'))
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
