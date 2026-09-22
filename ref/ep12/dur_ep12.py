# -*- coding: utf-8 -*-
"""12本目③：尺の判断。11本目の道具（ref/ep11/dur_probe.py・dur_test.py）を再現したうえで、
そこで**残った疑問**を2つ潰す。

疑問1 ── 再現したら **50分超（N=26）の近所比が 1.94** で 35-40分（1.33）より高かった。
         「もっと長くすれば勝てるのか」を検定で確かめる。
         ⚠️ 上限40分は `check_script.py` の E（`DUR_MAX_DEFAULT`）＝ch の決めごと。
            数字がどう出ても、動かすのはカズヤくんの判断。ここは材料を出すだけ。
疑問2 ── この題材（核実験・水爆・ビキニ）の棚が、母集団の中でどの尺に居るか。
"""
import json
import random
import sys
from datetime import date
from statistics import median

sys.path.insert(0, "ref/ep11")
import dur_test as T  # noqa: E402  近所比の定義を1か所に保つため借りる

sys.stdout.reconfigure(encoding="utf-8")
random.seed(20260922)

POOL = "ref/themes/pool.json"
WORDS = ("水爆", "原爆", "核実験", "ビキニ", "福竜丸", "被ばく", "被曝", "放射能", "核")


def main():
    pool = json.load(open(POOL, encoding="utf-8"))
    rows = T.neighbor_ratio(pool)
    print("母集団 N=%d（近所比が出た本数）\n" % len(rows))

    print("== 疑問1：40分より長くすると勝てるのか")
    b3540 = T.band(rows, 35, 40)
    for lo, hi, name in [(40, 50, "40-50分"), (50, 999, "50分超"), (40, 999, "40分超")]:
        b = T.band(rows, lo, hi)
        T.perm(b, b3540, "%s vs 35-40分" % name)
    print("  → 50分超は本数が少ない（N=%d）。**有意でなければ「長くして勝てる」証拠にならない**"
          % len(T.band(rows, 50, 999)))

    print("\n== 疑問1b：50分超の中身（その26本が何なのかを見る）")
    long = sorted(T.band(rows, 50, 999, raw=True) if hasattr(T, "band") else [],
                  key=lambda x: -x[1]) if False else None
    ls = [(v, r) for v, r in rows if 50 <= v["sec"] / 60 < 999]
    for v, r in sorted(ls, key=lambda x: -x[1])[:10]:
        print("   近所比%6.2f  %5.1f分 %8d回  %s" %
              (r, v["sec"] / 60, v["views"], v["title"][:52]))

    print("\n== 疑問2：この題材（核実験・水爆・ビキニ）の棚")
    shelf = [(v, r) for v, r in rows if any(w in v["title"] for w in WORDS)]
    print("   当たった本数 %d" % len(shelf))
    for v, r in sorted(shelf, key=lambda x: -x[0]["views"])[:12]:
        print("   %8d回 近所比%6.2f %5.1f分 %s  %s" %
              (v["views"], r, v["sec"] / 60, v["published"], v["title"][:50]))
    if shelf:
        print("   棚の尺 中央値 %.1f分 / 近所比 中央値 %.2f"
              % (median(v["sec"] / 60 for v, _ in shelf),
                 median(r for _, r in shelf)))
        print("\n   棚（核・放射線 %d本）の尺帯ごと" % len(shelf))
        for lo, hi in [(0, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 50), (50, 999)]:
            b = [r for v, r in shelf if lo <= v["sec"] / 60 < hi]
            if b:
                print("     %3d-%3d分  N=%2d  近所比 中央 %.2f  1.0超 %.0f%%"
                      % (lo, hi, len(b), median(b),
                         100.0 * sum(1 for x in b if x > 1) / len(b)))


if __name__ == "__main__":
    main()
