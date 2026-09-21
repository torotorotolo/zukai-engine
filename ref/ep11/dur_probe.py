# -*- coding: utf-8 -*-
"""③尺の判断材料。母集団 1,815本から「尺と当たりの関係」を測る。

近所比＝その動画の再生数 ÷ 同じ局が前後45日に出した動画の再生数の中央値。
局の規模で割るので、尺だけの効きを見るのに使える（ref/themes/README.md §3 と同じ定義）。
"""
import json
import sys
from datetime import date
from statistics import median

POOL = "ref/themes/pool.json"
BANDS = [(0, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 50), (50, 999)]


def load():
    return json.load(open(POOL, encoding="utf-8"))


def d(s):
    y, m, dd = (int(x) for x in s.split("-"))
    return date(y, m, dd)


def neighbor_ratio(pool, win=45):
    """局ごとに前後 win 日の中央値で割る。中央値の母数が2本未満なら None（自分だけで割らない）。"""
    by_ch = {}
    for v in pool:
        by_ch.setdefault(v["channel"], []).append(v)
    out = []
    for ch, vs in by_ch.items():
        for v in vs:
            t = d(v["published"])
            near = [w["views"] for w in vs
                    if w["id"] != v["id"] and abs((d(w["published"]) - t).days) <= win]
            if len(near) < 2:
                continue
            m = median(near)
            if m <= 0:
                continue
            out.append((v, v["views"] / m))
    return out


def band(sec):
    mn = sec / 60
    for lo, hi in BANDS:
        if lo <= mn < hi:
            return "%d-%d分" % (lo, hi)
    return "?"


def table(rows, label):
    print("\n== %s（N=%d）" % (label, len(rows)))
    print("  %-10s %5s %12s %10s %10s" % ("尺帯", "本数", "再生中央値", "近所比中央", "近所比平均"))
    agg = {}
    for v, r in rows:
        agg.setdefault(band(v["sec"]), []).append((v["views"], r))
    for lo, hi in BANDS:
        k = "%d-%d分" % (lo, hi)
        if k not in agg:
            continue
        a = agg[k]
        print("  %-10s %5d %12.0f %10.2f %10.2f"
              % (k, len(a), median([x[0] for x in a]),
                 median([x[1] for x in a]), sum(x[1] for x in a) / len(a)))


SPACE = ("宇宙", "スペースシャトル", "シャトル", "ロケット", "NASA", "アポロ", "ソユーズ",
         "チャレンジャー", "コロンビア", "衛星", "宇宙飛行士", "打ち上げ", "無重力")


def main():
    pool = load()
    rows = neighbor_ratio(pool)
    table(rows, "母集団ぜんぶ")
    sp = [(v, r) for v, r in rows if any(w in v["title"] for w in SPACE)]
    table(sp, "宇宙もの（題名で拾った）")
    # 事故もの（このchの直接の競合帯）
    acc = [(v, r) for v, r in rows
           if any(w in v["title"] for w in ("事故", "墜落", "沈没", "崩落", "爆発", "惨事", "災害"))]
    table(acc, "事故もの")

    print("\n== 母集団のなかで 25-30分 と 35-40分 を直接くらべる")
    for lo, hi in ((25, 30), (30, 35), (35, 40)):
        a = [r for v, r in rows if lo <= v["sec"] / 60 < hi]
        if a:
            print("  %2d-%2d分 N=%4d  近所比 中央 %.2f / 平均 %.2f / 1.0超の割合 %.0f%%"
                  % (lo, hi, len(a), median(a), sum(a) / len(a),
                     100 * sum(1 for x in a if x >= 1.0) / len(a)))

    print("\n== チャレンジャー号の棚（題名に語が当たるもの）")
    for v in pool:
        if any(w in v["title"] for w in ("チャレンジャー", "73秒")):
            print("  %8d回 %5.1f分 %s %s" % (v["views"], v["sec"] / 60, v["published"], v["title"][:60]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
