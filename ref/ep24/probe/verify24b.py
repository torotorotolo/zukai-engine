# -*- coding: utf-8 -*-
"""24本目②：verify24.py の2回目＝1回目で文が切れた所・頁が違った所を、前後を広げて当て直す（CTX を項目ごとに）。"""
import re, sys
import verify24 as v

I7, GC, US, FO, J, D = v.I7, v.GC, v.US, v.FO, v.J, v.D
CHECKS = [
    # (記号, 資料, 頁, 正規表現, 前, 後, メモ)
    ("T02a2", US, range(1, 61), r"0[.:]28|28 hours|30 MW", 200, 260, "ソ連報告の 00:28"),
    ("E01b", I7, [20], r"\(1\) Isolation of the emergency core cooling", 0, 900, "INSAG-7 (1) ECCS の全文"),
    ("E02b", I7, [82, 83], r"Section 2\.10\.5", 300, 900, "付属書I の ECCS の評価"),
    ("T09d", I7, [21], r"\(4\) Turbogenerator trip signal blocked", 0, 900, "INSAG-7 (4) タービンの信号の全文"),
    ("T09e", I7, [21, 22], r"\(5\)", 0, 700, "INSAG-7 (5) の頭"),
    ("S01", I7, [20, 21, 22], r"steam separator drum|drum separator|00:36|01:19", 250, 400, "蒸気ドラムの保護 01:19→00:36"),
    ("Z02b", I7, range(70, 80), r"1-4\.6|1-4\.7", 0, 700, "付属書I 1-4.6・1-4.7"),
    ("D01b", US, [43, 44], r"died|not found|was found", 400, 300, "ソ連報告 事故の夜の2人"),
    ("D07b", J, [39, 40, 41], r"acute radiation syndrome|ARS", 150, 300, "UNSCEAR 2000 ARS の段落"),
    ("V01b", J, [24], r"On the evening of 26 April", 0, 700, "第92段落の続き"),
    ("V04b", FO, [9], r"220 000 people were relocated", 350, 50, "フォーラムの避難の文"),
    ("P03b", I7, [23, 24, 25], r"positive scram|1987", 250, 350, "1987年のウィーンで認めた"),
    ("P04b", I7, [14], r"1\.25|1,25|water column|metre", 300, 300, "棒の先の黒鉛と水のすき間"),
    ("O04b", I7, [64, 65], r"ORM equals|ORM was|equals \d", 120, 200, "表I-I の ORM"),
    ("TG01", I7, [62, 63, 64, 65], r"00:43", 60, 160, "表I-I の 00:43 前後"),
    ("TG02", I7, [123, 124], r"00:43", 60, 160, "表II-III の 00:43 前後"),
    ("X01", GC, range(20, 50), r"steam separator|drum", 200, 250, "INSAG-1 の蒸気ドラムの保護（01:19）"),
]


def main():
    only = set(sys.argv[1:])
    cache = {}
    for cid, base, pages, pat, pre, post, memo in CHECKS:
        if only and cid not in only:
            continue
        rows = cache.setdefault(base, v.load(base))
        rx = re.compile(pat, re.I | re.S)
        print(f"\n[{cid}] {memo} ／ {base}")
        n = 0
        for p in pages:
            if p not in rows:
                continue
            for m in rx.finditer(rows[p]):
                n += 1
                if n > 4:
                    break
                t = rows[p]
                print(f"   p.{p}/{v.pr(base, p, t)}: …{t[max(0, m.start() - pre):m.end() + post]}…")
        if n == 0:
            print("   0件")


if __name__ == "__main__":
    main()
