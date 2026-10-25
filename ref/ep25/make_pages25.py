# -*- coding: utf-8 -*-
"""make_pages25.py — 25本目 ⑤b-4：出典の頁の原文を1ファイル（`=== p<N> ===` で頁を割る）にする＝`cuts.ss.REC_PAGES`。

■ なぜ（24本目 `ref/ep24/make_pages24.py` と同じ）
  ① の写し（git の外 `ref/ep25/src/txt/*.json`＝頁ごとの pdf・printed・norm）は資料ごとのファイル＝案C の部品の `rec=` が
  「資料 p頁」で原文に在るかを門番 check_illu ① が照らすため、1つの形へ並べ直す。
■ 頁の番号（通し＝`cuts/ss.py` の REC_DOCS の注と同じ。台本 §10 の頁の書き方）
  R1＝鉄道事故調査報告書 RA2007-3-1 本文＝**印刷の頁**（PDF−11・表紙と目次は 0 以下）＝台本の「R1 p.13」がそのまま p13
  R2〜R7＝同 別冊（付図）＝**k000＋PDF の頁**（R2＝2000＋・R3＝3000＋ … R7＝7000＋）＝台本の「R5 p.23」→ p5023
  S3＝神戸地裁の判決（2012年1月）＝**8000＋PDF の頁**（PDF＝印刷）＝「S3 p.7」→ p8007
  S1＝検証報告書（2011-04-15）＝**9000＋PDF の頁**（印刷＝PDF−8）／S1k＝付録「事故調査報告書に関する解説」＝**10000＋PDF の頁**（印刷＝PDF−2）
  S2＝最高裁の決定（2017-06-12）＝**11000＋PDF の頁**（PDF＝印刷）
■ 使い方
    python ref/ep25/make_pages25.py      → ref/ep25/src/ep25_pages.txt（git の外＝手元だけ。Actions では門番を回さない）
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
TXT = HERE / "src" / "txt"
OUT = HERE / "src" / "ep25_pages.txt"
# (資料, 文字起こしの名, 足し分)。R1 だけ印刷の頁（足し分 −11＝PDF の頁から引く）
DOCS = (("R1", "RA07-3-1-1", -11),
        ("R2", "RA07-3-1-2", 2000), ("R3", "RA07-3-1-3", 3000), ("R4", "RA07-3-1-4", 4000),
        ("R5", "RA07-3-1-5", 5000), ("R6", "RA07-3-1-6", 6000), ("R7", "RA07-3-1-7", 7000),
        ("S3", "hanrei-pdf-82178", 8000), ("S1", "fu04-finalreport", 9000), ("S1k", "fu04-finalreport-annex-2-2", 10000),
        ("S2", "hanrei-pdf-86834", 11000))


def main():
    pages, n_of = {}, {}
    for name, stem, add in DOCS:
        for pg in json.loads((TXT / f"{stem}.json").read_text(encoding="utf-8")):
            n = add + int(pg["pdf"])
            if name == "R1" and pg.get("printed") is not None and int(pg["printed"]) != n:
                raise SystemExit(f"🔴 R1 の印刷の頁が PDF−11 でない：PDF {pg['pdf']} → 印刷 {pg['printed']}")
            if n in pages:
                raise SystemExit(f"🔴 頁の番号がぶつかった：{name} PDF {pg['pdf']} → p{n}")
            # 門番と照らし合わせで探しやすいように NFKC・空白なし（norm が無い頁は raw）
            pages[n] = "".join(unicodedata.normalize("NFKC", pg.get("norm") or pg.get("raw") or "").split())
            n_of[name] = n_of.get(name, 0) + 1
    with OUT.open("w", encoding="utf-8", newline="\n") as fo:
        for n in sorted(pages):
            fo.write(f"=== p{n} ===\n{pages[n]}\n")
    print("✓", OUT.name, "＝", "・".join(f"{k} {v}頁" for k, v in n_of.items()), f"（計 {len(pages)}頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
