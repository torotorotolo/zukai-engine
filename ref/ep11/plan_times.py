#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""場面の変わり目から「見るべき秒」の一覧を作る。

長いショットは変わり目が1つしか出ないので、そこだけ midpoint で済ませると
中身を見落とす（⑤bで ③の地図が1か所ちがっていた原因）。
→ 長いショットは step 秒ごとに割って全部見る。

使い方: python ref/ep11/plan_times.py <boundaries…> --dur <総秒> [--step 45] [--per 12]
"""
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bounds", help="変わり目の秒をカンマ区切りで")
    ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--step", type=float, default=45.0, help="長いショットを割る間隔")
    ap.add_argument("--per", type=int, default=12, help="1シートの枚数")
    ap.add_argument("--min", type=float, default=1.0, help="これより短いショットは飛ばす")
    a = ap.parse_args()

    b = [0.0] + [float(x) for x in a.bounds.split(",")] + [a.dur]
    b = sorted(set(b))
    times = []
    for s, e in zip(b, b[1:]):
        span = e - s
        if span < a.min:
            continue
        n = max(1, int(span // a.step))
        for i in range(n):
            times.append(round(s + span * (i + 0.5) / n, 1))
    times = sorted(set(times))

    print(f"ショット {len(b) - 1}／見る秒 {len(times)}／シート {-(-len(times) // a.per)}枚")
    for i in range(0, len(times), a.per):
        chunk = times[i:i + a.per]
        print(f"--- sheet {i // a.per + 1} ({len(chunk)}枚) ---")
        print(",".join(str(t) for t in chunk))


if __name__ == "__main__":
    main()
