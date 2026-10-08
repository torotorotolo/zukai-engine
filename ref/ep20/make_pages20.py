# -*- coding: utf-8 -*-
"""make_pages20.py — 20本目 ⑤b-3：出典の頁の原文を1ファイル（`=== p<N> ===` で頁を割る）にする＝`cuts.ss.REC_PAGES`。

■ なぜ（門番 check_illu ①＝部品の出典 `rec=` の頁が原文に在るか・ほかの型の出典の行 `ss.src()` も同じ表 `ss.REC_DOCS`）
  ④ の頁の写し `ref/ep20/src/pages.jsonl`（報告書 ja_01〜ja_10・解説）は1行1頁の JSON。CVR（別添6＝ja_11）は文字の層が無く、
  OCR の表 `ja_11_cvr_ocr300.tsv`（印刷の頁の欄つき）にだけある。門番が読む形（`=== p<N> ===`）へ並べ直す。
■ 頁の番号（通し）
  報告書＝印刷の頁の番号そのまま（p1〜p309＝pages.jsonl の printed_page が数字の頁・p310〜p343＝別添6 CVR の OCR の印刷の頁）
  解説（2011年）＝1000＋印刷の頁（ローマ数字の前付けは入れない）
■ 使い方
    python ref/ep20/make_pages20.py      → ref/ep20/src/ep20_pages.txt（git の外＝手元だけ。Actions では門番を回さない）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = SRC / "ep20_pages.txt"
KAISETSU_BASE = 1000


def main():
    pages = {}
    for line in (SRC / "pages.jsonl").read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        pp = str(d.get("printed_page") or "")
        if not pp.isdigit():
            continue
        n = int(pp) + (KAISETSU_BASE if d["file"] == "jtsb_kaisetsu.pdf" else 0)
        if n in pages:
            print(f"⚠️ p{n} が2つ（{d['file']} PDF{d['pdf_page']}）＝後のものをつなぐ", file=sys.stderr)
            pages[n] += "\n" + (d.get("text") or "")
        else:
            pages[n] = d.get("text") or ""
    cvr = {}
    for line in (SRC / "ja_11_cvr_ocr300.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        f = line.split("\t")
        if len(f) >= 6 and f[1].isdigit():
            cvr.setdefault(int(f[1]), []).append(f[5])
    for n, chs in cvr.items():
        if n in pages:
            continue
        pages[n] = "［別添6 CVR 記録の OCR（文字の層なし）］\n" + "".join(chs)
    with OUT.open("w", encoding="utf-8") as fo:
        for n in sorted(pages):
            fo.write(f"=== p{n} ===\n{pages[n].rstrip()}\n")
    rep = [n for n in pages if n < KAISETSU_BASE]
    kai = [n for n in pages if n >= KAISETSU_BASE]
    print(f"{OUT.name}: 報告書 {len(rep)} 頁（p{min(rep)}〜p{max(rep)}・うち CVR の OCR {len([n for n in cvr if n not in rep or True])}）・"
          f"解説 {len(kai)} 頁（p{min(kai)}〜p{max(kai)}）")


if __name__ == "__main__":
    main()
