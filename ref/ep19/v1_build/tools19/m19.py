# -*- coding: utf-8 -*-
"""19本目 台本の机上の数え（m18.py を写して 365字/分・9.36秒・13,324字に替えた）（リポに入れない道具）。

  python m19.py <台本.md> [--roles roles.tsv] [--selftest]

数えるもの：カット・行・句読点なしの字（、。？！「」（）・ を除く＝ルール §5a-28）・3通りの尺・章ごと・
1行41字超・1カット1〜3行・決め所の字数（20字まで・★の行の全字）・冒頭の秒（÷365 を1カットずつ）・
聞き役（行・割合・1分あたり・空き・最初・役割＝tools/check_listener.judge をそのまま呼ぶ）・
写真（画の欄が「実写」）・文字だけの画面（Vault の count_text_screens の分け方をそのまま使う）。
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
SEC_PER_CUT = 9.36
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
    E = []
    per_ch = collections.OrderedDict()
    tot = 0
    rows = []          # check_listener.judge の形 (cid, i, 話者, 文, 秒)
    t = 0.0
    hook = []
    for k, (cid, pic, ls) in enumerate(cuts):
        ch = cid[:2]
        d = per_ch.setdefault(ch, dict(cuts=0, lines=0, chars=0, photo=0, quote=0, q=0))
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
                d['quote'] += 1
                if len(c) > 20:
                    E.append('E %s 決め所 %d字（20字まで）: %s' % (cid, len(c), c))
        if k < 8:
            hook.append('%s=%.1fs' % (cid, t))
    total_sec = t
    d1 = n * SEC_PER_CUT
    d2 = tot / CPM * 60
    d3 = sum(v['chars'] for v in per_ch.values()) / CPM * 60
    print('カット %d / 行 %d / 句読点なし %d字（目標 13,324・%.1f%%）/ 決め所 %d / 写真（実写）%d（%.1f%%）'
          % (n, len(lines), tot, tot / 13324 * 100, sum(v['quote'] for v in per_ch.values()),
             sum(v['photo'] for v in per_ch.values()), sum(v['photo'] for v in per_ch.values()) / max(1, n) * 100))
    allc = [CS.clean(l) for _, l in lines]
    print('1行 中央値 %d字・最長 %d字・1カット %.2f行' % (sorted(len(x) for x in allc)[len(allc) // 2], max(len(x) for x in allc), len(lines) / n))
    print('尺 ① カット×9.36秒 %s ／ ② 句読点なし÷365 %s ／ ③ 章ごとの合計 %s → 開き %s'
          % (fmt(d1), fmt(d2), fmt(d3), fmt(max(d1, d2, d3) - min(d1, d2, d3))))
    print('冒頭（÷365 を1カットずつ足した秒）: ' + ' '.join(hook))
    print('章ごと: 章 カット 行 句読点なし 分 写真 決め所 聞き役')
    for ch, v in per_ch.items():
        print('  %s %3d %3d %5d %5.2f %2d %d %2d' % (ch, v['cuts'], v['lines'], v['chars'], v['chars'] / CPM, v['photo'], v['quote'], v['q']))
    # 聞き役（tools/check_listener.judge をそのまま）
    roles = load_roles(roles_path)
    e2, w2, info = CL.judge(rows, total_sec, roles if roles is not None else {})
    print('聞き役: %s' % {k: (round(v, 3) if isinstance(v, float) else v) for k, v in info.items()})
    for x in e2:
        print('  🔴 ' + x)
    for x in w2:
        print('  ⚠️ ' + x)
    # 文字だけの画面（Vault の道具の分け方のまま）
    tc = CTS.parse(path)
    ratio, best = CTS.report(tc, {}, None, '画の欄のまま')
    for x in E:
        print('🔴 ' + x)
    print('E %d件（形）' % len(E))
    return len(E) + len(e2)


def selftest():
    ok = nopunct('「あ、い。」（う）・え？お！') == 5
    ok &= CS.clean('Q: そうなの？') == 'そうなの？'
    ok &= CS.clean('★**ダムは耐えた**') == 'ダムは耐えた'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    rp = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], rp) else 0)
