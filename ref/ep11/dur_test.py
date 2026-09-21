# -*- coding: utf-8 -*-
"""尺帯の差が「たまたま」でないかを並べ替え検定で見る（記憶 project-jiko-next-themes と同じ作法）。

⚠️ 陽性対照と陰性対照を先に置く。道具が「何でも有意」と言わないことを確かめてから本番を読む。
"""
import json
import random
import sys
from datetime import date
from statistics import median

random.seed(20260921)
POOL = "ref/themes/pool.json"
ITER = 20000


def d(s):
    y, m, dd = (int(x) for x in s.split("-"))
    return date(y, m, dd)


def neighbor_ratio(pool, win=45):
    by_ch = {}
    for v in pool:
        by_ch.setdefault(v["channel"], []).append(v)
    out = []
    for vs in by_ch.values():
        for v in vs:
            t = d(v["published"])
            near = [w["views"] for w in vs
                    if w["id"] != v["id"] and abs((d(w["published"]) - t).days) <= win]
            if len(near) < 2:
                continue
            m = median(near)
            if m > 0:
                out.append((v, v["views"] / m))
    return out


def perm(a, b, label, iters=ITER):
    """a の中央値が b の中央値より大きいことが、偶然でどのくらい起きるか。"""
    obs = median(a) - median(b)
    pool = a + b
    na = len(a)
    hit = 0
    for _ in range(iters):
        random.shuffle(pool)
        if median(pool[:na]) - median(pool[na:]) >= obs:
            hit += 1
    p = (hit + 1) / (iters + 1)
    print("  %-34s N=%4d vs %4d  中央値 %.3f vs %.3f  差 %+.3f  p=%.4f %s"
          % (label, len(a), len(b), median(a), median(b), obs, p,
             "← 有意" if p < 0.05 else ""))
    return p


def band(rows, lo, hi):
    return [r for v, r in rows if lo <= v["sec"] / 60 < hi]


def main():
    pool = json.load(open(POOL, encoding="utf-8"))
    rows = neighbor_ratio(pool)

    print("== 物差しの検算（先に道具を疑う）")
    b2530 = band(rows, 25, 30)
    b3035 = band(rows, 30, 35)
    b3540 = band(rows, 35, 40)
    # 陰性対照＝同じ帯を無作為に2つに割る。ここで有意が出たら道具が壊れている
    x = b2530[:]
    random.shuffle(x)
    perm(x[:len(x) // 2], x[len(x) // 2:], "陰性対照（25-30分を半分に割る）")
    # 陽性対照＝明らかに違うもの（0-15分 と 50分超）
    perm(band(rows, 50, 999), band(rows, 0, 15), "陽性対照（50分超 vs 15分未満）")

    print("\n== 本番：尺帯の比べ（近所比の中央値）")
    perm(b3540, b2530, "35-40分 vs 25-30分")
    perm(b3540, b3035, "35-40分 vs 30-35分")
    perm(b3035, b2530, "30-35分 vs 25-30分")
    perm(band(rows, 33, 40), band(rows, 27, 33), "33-40分 vs 27-33分")

    print("\n== 事故ものだけ")
    acc = [(v, r) for v, r in rows
           if any(w in v["title"] for w in ("事故", "墜落", "沈没", "崩落", "爆発", "惨事", "災害"))]
    perm(band(acc, 35, 40), band(acc, 25, 30), "事故 35-40分 vs 25-30分")
    perm(band(acc, 33, 40), band(acc, 27, 33), "事故 33-40分 vs 27-33分")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
