# -*- coding: utf-8 -*-
"""24本目②：取り出した本文（src/*.pages.tsv）を正規表現で探す。印刷頁＝PDF頁＋ずれ（OFF＝頁の数字で確かめた値）。
使い方: grep24.py [-c 前後の字数] [-f 資料の頭,…] [-m 1資料の最大件数] 正規表現 [正規表現 …]
  資料の頭＝保存名の頭（例 insag7・gc_spl1・ussr・forum・unscear2000・unscear2008）
出力: ### 正規表現 → 資料 PDF頁/印刷頁: …前後の文…"""
import os, re, sys

SRC = r"C:\Users\konar\Desktop\zukai-engine\ref\ep24\src"
# 印刷頁＝PDF頁＋OFF（② で頁の数字を見て決めた値。None＝未確認）
OFF = {
    "insag7_pub913e": -10,          # 本文の印刷 p.1 = PDF p.11（① と同じ・② で頁の数字を確認）
    "gc_spl1_3_insag1text": None,   # スキャン＝頁ごとに見る
    "ussr_report_part1": -4,
    "forum_legacy_2006": -2,         # 印刷＝PDF−2（① は「PDF頁＋2」と書いた＝② で確認する）
    "unscear2000_annexJ": 448,
    "unscear2008_annexD_corr": 40,
}


def load(prefixes):
    rows = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".pages.tsv"):
            continue
        base = fn[:-10]
        if prefixes and not any(base.startswith(p) for p in prefixes):
            continue
        with open(os.path.join(SRC, fn), encoding="utf-8") as f:
            for line in f:
                pdf, _n, text = line.rstrip("\n").split("\t", 2)
                rows.append((base, int(pdf), text))
    return rows


def main():
    args = sys.argv[1:]
    ctx, prefixes, mx = 110, [], 12
    while args and args[0] in ("-c", "-f", "-m"):
        if args[0] == "-c":
            ctx = int(args[1])
        elif args[0] == "-f":
            prefixes = args[1].split(",")
        else:
            mx = int(args[1])
        args = args[2:]
    rows = load(prefixes)
    for pat in args:
        rx = re.compile(pat, re.I)
        print(f"### {pat}")
        per = {}
        for base, pdf, text in rows:
            for m in rx.finditer(text):
                per[base] = per.get(base, 0) + 1
                if per[base] > mx:
                    continue
                off = OFF.get(base)
                pr = pdf + off if off is not None else "?"
                a, b = max(0, m.start() - ctx), min(len(text), m.end() + ctx)
                print(f"- {base} p.{pdf}/{pr}: …{text[a:b]}…")
        for base, n in per.items():
            if n > mx:
                print(f"  ({base}: {n}件中 {mx}件だけ表示)")
        if not per:
            print("  0件")


if __name__ == "__main__":
    main()
