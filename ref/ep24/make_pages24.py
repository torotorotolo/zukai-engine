# -*- coding: utf-8 -*-
"""make_pages24.py — 24本目 ⑤b-3：出典の頁の原文を1ファイル（`=== p<N> ===` で頁を割る）にする＝`cuts.ss.REC_PAGES`。

■ なぜ（22本目 `ref/ep22/make_pages22.py` と同じ）
  ① の写し（git の外 `ref/ep24/src/*.pages.tsv`＝頁・字数・本文の3列）は資料ごとのファイル＝門番 check_illu・check_axis と出典の行が読む
  1つの形へ並べ直す（案C の部品の `rec=` が「資料 p頁」で原文に在るかを照らす）。
■ 頁の番号（通し＝`cuts/ss.py` の REC_DOCS の注と同じ。台本 §10 の「PDF の頁／印刷の頁」の PDF の頁に資料ごとの足し分）
  S1＝INSAG-7（IAEA 1992）の **PDF の頁**（台本の「S1 p.113／103」の 113）
  S2＝GC(SPL.I)/3（1986＝INSAG-1 と同じ本文）＝**1000＋PDF の頁**（「S2 p.8／~3」→ p1008）
  S3＝ソ連の報告 Part I（1986年8月）＝**2000＋PDF の頁**（「S3 p.20／16」→ p2020）
  L2＝UNSCEAR 2000 Annex J＝**3000＋PDF の頁**（「L2 p.24／472」→ p3024）
  L1＝チェルノブイリ・フォーラム『Chernobyl's Legacy』2006＝**4000＋PDF の頁**（「L1 p.14／16」→ p4014）
■ 使い方
    python ref/ep24/make_pages24.py      → ref/ep24/src/ep24_pages.txt（git の外＝手元だけ。Actions では門番を回さない）
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = SRC / "ep24_pages.txt"
DOCS = (("S1", "insag7_pub913e", 0), ("S2", "gc_spl1_3_insag1text", 1000), ("S3", "ussr_report_part1", 2000),
        ("L2", "unscear2000_annexJ", 3000), ("L1", "forum_legacy_2006", 4000))


def main():
    csv.field_size_limit(10 ** 8)
    pages, n_of = {}, {}
    for name, stem, add in DOCS:
        with (SRC / f"{stem}.pages.tsv").open(encoding="utf-8", newline="") as f:
            for row in csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
                if len(row) < 3 or not row[0].strip().isdigit():
                    continue
                n = add + int(row[0])
                if n in pages:
                    raise SystemExit(f"🔴 頁の番号がぶつかった：{name} p{row[0]} → p{n}")
                pages[n] = row[2].strip()
                n_of[name] = n_of.get(name, 0) + 1
    with OUT.open("w", encoding="utf-8") as fo:
        for n in sorted(pages):
            fo.write(f"=== p{n} ===\n{pages[n]}\n")
    print("✓", OUT.name, "＝", "・".join(f"{k} {v}頁" for k, v in n_of.items()), f"（計 {len(pages)}頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
