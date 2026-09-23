# -*- coding: utf-8 -*-
"""原文 thy_pages.txt の指定頁から、語句の前後だけを抜き出す（④' の引き直し用・読むだけ）。
    python kwic.py QUERIES.txt  ← 1行1件「頁 語句(正規表現) [前字数 後字数]」
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
T = open("C:/Users/konar/Desktop/zukai-engine/ref/ep13/src/thy_pages.txt", encoding="utf-8").read()
parts = re.split(r"=== p ?(\d+) ===", T)
P = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.rstrip("\n")
    if not line.strip() or line.startswith("#"):
        continue
    bits = line.split("\t")
    pg, pat = bits[0], bits[1]
    b, a = (int(bits[2]), int(bits[3])) if len(bits) > 3 else (200, 300)
    pages = []
    for r in pg.split(","):
        if "-" in r:
            x, y = map(int, r.split("-")); pages += range(x, y + 1)
        else:
            pages.append(int(r))
    hit = 0
    for p in pages:
        s = re.sub(r"\s+", " ", P.get(p, ""))
        for m in re.finditer(pat, s, re.I):
            hit += 1
            print(f"--- p{p} /{pat}/ :: …{s[max(0, m.start() - b):m.end() + a]}…")
            if hit >= 3:
                break
        if hit >= 3:
            break
    if not hit:
        print(f"--- p{pg} /{pat}/ :: 0件")
