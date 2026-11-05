# -*- coding: utf-8 -*-
"""30本目④'：§2（照合の表）と §3（章ごと）の数を、門番の出力 gates.md から写す差し替え patches_sec_num.json を書く（手で写さない）。

  python -P ref/ep30/v2_build/sec_nums30.py

順番＝final30.py → sec_nums30.py → merge30.py → final30.py（§ は語りの外なので2周目で数は動かない。動いたら止める）
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
V1 = open(os.path.join(EP, 'daihon_v1.md'), encoding='utf-8').read().split('\n')


def mmss(x):
    m, s = re.match(r'(\d+)分(\d+)秒', x).groups()
    return '%d:%02d' % (int(m), int(s))


def main():
    g = open(os.path.join(HERE, 'gates.md'), encoding='utf-8').read()
    rows = re.findall(r'^\s+(c[0-9a-d]) (\d+分\d+秒)\s+(\d+)（\s*\d+）\s+\d+\s+(\d+)（\s*(\d+)・\s*[+-]?\d+）\s+([\d.]+)\s+(\d+)（\s*\d+）\s*\d+%\s+(\d+)\s+\d+\s+(\d+)（\d+）', g, re.M)
    ed = re.search(r'^\s+ed01 (\d+分\d+秒)', g, re.M)
    total = re.search(r'カット (\d+) / 行 (\d+) / 句読点なし (\d+)字＋ed01 46＝(\d+)字', g)
    end = re.search(r'② 句読点なし÷365 (\d+分\d+秒)', g)
    photo = re.search(r'写真・映像（実写）(\d+)（[\d.]+%）.*?フリー素材（イメージ）(\d+)', g)
    q = re.search(r"'q': (\d+)", g)
    qt = re.search(r'片 (\d+): OK=(\d+) 字幕=(\d+)', g)
    noq = re.search(r'片の無いカット (\d+): (.*)', g)
    if not (len(rows) == 12 and ed and total and end and photo and q and qt and noq):
        print('🔴 門番の出力が読めない＝止める', len(rows))
        return 2
    out = []
    by = {r[0]: r for r in rows}
    for ln in V1:
        m = re.match(r'^\| (c[0-9a-d]) \| ([^|]+) \| [\d:]+ \| \d+ \| [\d,]+（[\d,]+） \| [\d.]+ \| \d+ \| \d+ \| \d+ \|$', ln)
        if m and m.group(1) in by:
            r = by[m.group(1)]
            new = '| %s | %s | %s | %s | %s（%s） | %s | %s | %s | %s |' % (
                r[0], m.group(2), mmss(r[1]), r[2], format(int(r[3]), ','), format(int(r[4]), ','), r[5], r[6], r[7], r[8])
            out.append({'id': 'SN-%s' % r[0], 'cut': '§', 'old': ln, 'new': new, 'why': '§3 の数（gates.md）', 'from': []})
    edl = next(x for x in V1 if x.startswith('| ed01 | 共通エンディング |'))
    out.append({'id': 'SN-ed', 'cut': '§', 'old': edl, 'new': '| ed01 | 共通エンディング | %s | — | 46 | 0.13 | — | — | — |' % mmss(ed.group(1)), 'why': '§3 の数', 'from': []})
    tol = next(x for x in V1 if x.startswith('| **計** | | **36:54**'))
    mins = int(total.group(4)) / 365.0
    out.append({'id': 'SN-total', 'cut': '§', 'old': tol, 'new': '| **計** | | **%s** | **%s** | **%s** | **%.2f** | **%s** | **%s** | **%s** |' % (
        mmss(end.group(1)), total.group(1), format(int(total.group(4)), ','), mins, photo.group(1), photo.group(2), q.group(1)), 'why': '§3 の数', 'from': []})
    f = {r[0]: float(r[5]) for r in rows}
    allm = sum(f.values()) + 0.13
    def part(*cs):
        v = sum(f[c] for c in cs)
        return '**%.1f分＝%d%%**' % (v, round(v * 100 / allm))
    rng = next(x for x in V1 if x.startswith('- 範囲の割合（kousei §0'))
    new_rng = re.sub(r'c1〜c2＝.*$', 'c1〜c2＝%s／c3〜c6＝%s／c7〜c9＝%s／ca〜cc＝%s' % (
        part('c1', 'c2'), part('c3', 'c4', 'c5', 'c6'), part('c7', 'c8', 'c9'), part('ca', 'cb', 'cc')), rng)
    out.append({'id': 'SN-range', 'cut': '§', 'old': rng, 'new': new_rng, 'why': '§3 の数', 'from': []})
    a = next(x for x in V1 if x.startswith('| OK（書いた資料にある） |'))
    out.append({'id': 'SN-q1', 'cut': '§', 'old': a, 'new': '| OK（書いた資料にある） | **%s** |' % qt.group(2), 'why': '§2 の数', 'from': []})
    b = next(x for x in V1 if x.startswith('| 字幕（無線と OH'))
    out.append({'id': 'SN-q2', 'cut': '§', 'old': b, 'new': '| 字幕（無線と OH＝語の字が崩れる＝機械で当てない） | %s |' % qt.group(3), 'why': '§2 の数', 'from': []})
    c = next(x for x in V1 if x.startswith('- 片の無いカット 15＝'))
    out.append({'id': 'SN-q3', 'cut': '§', 'old': c, 'new': '- 片の無いカット %s＝%s（第2版＝`v2_build/quotes30_v2.tsv`）' % (noq.group(1), '・'.join(noq.group(2).split())), 'why': '§2 の数', 'from': []})
    d = next(x for x in V1 if x.startswith('- 決め所（★）が0＝`tools/check_facts.py`'))
    out.append({'id': 'SN-q4', 'cut': '§', 'old': d, 'new': d.replace('（結果＝`v1_build/quotes30_result.tsv`）', '（第1版の結果＝`v1_build/quotes30_result.tsv`・第2版の結果＝`v2_build/quotes30_v2.tsv`）'), 'why': '§2 の置き場', 'from': []})
    json.dump(out, open(os.path.join(HERE, 'patches_sec_num.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('§2・§3 の差し替え %d件' % len(out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
