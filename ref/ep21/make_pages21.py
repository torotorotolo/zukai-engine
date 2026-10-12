# -*- coding: utf-8 -*-
"""make_pages21.py — 21本目 ⑤b-3：出典の頁の原文を1ファイル（`=== p<N> ===` で頁を割る）にする＝`cuts.ss.REC_PAGES`。

■ なぜ（門番 check_illu ①＝部品の出典 `rec=` の頁が原文に在るか・ほかの型の出典の行 `ss.src()` も同じ表 `ss.REC_DOCS`）
  ① の写し（git の外 `ref/ep21/src/`）は資料ごとに形が違う（JSON の頁・OCR の頁の節・テキスト）＝門番が読む形へ並べ直す。
■ 頁の番号（通し＝`cuts/ss.py` の REC_DOCS の注と同じ）
  委員会報告＝印字の頁（GPO の PDF の頁−18・前付けは入れない）／スタッフ声明 No.17＝1000＋PDF の頁／NTSB の飛行経路の調べ＝11便 2000＋・
  175便 3000＋・77便 4000＋・93便 5000＋（PDF の頁・スキャン＝7本目の OCR `analytics/materials/ep7/s2/ocr/*.ocr.txt`）／
  93便の CVR の逐語 P200056T＝6000＋／NIST NCSTAR 1＝7000＋／運輸長官の証言（写し）＝8001。
  ⚠️ 頁なしの資料（ウェブの写し・RG237＝p1）は委員会報告の p1 と番号が重なる＝門番は「その番号の頁が在るか」だけを見る（範囲は REC_DOCS）
■ 使い方
    python ref/ep21/make_pages21.py      → ref/ep21/src/ep21_pages.txt（git の外＝手元だけ。Actions では門番を回さない）
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = HERE / "src"
RAW = SRC / "core_raw"
OUT = SRC / "ep21_pages.txt"
NTSB = {"AA11": 2000, "UA175": 3000, "AA77": 4000, "UA93": 5000}


def _jsonl(path):
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        out[int(d["pdf_page"])] = d.get("raw") or ""
    return out


def main():
    pages, n_of = {}, {}

    def put(n, text, what):
        pages[n] = (pages.get(n, "") + "\n" + text).strip("\n")
        n_of[what] = n_of.get(what, 0) + 1

    for p, t in _jsonl(RAW / "GPO-911REPORT.pages.jsonl").items():
        if p - 18 >= 1:
            put(p - 18, t, "委員会報告")
    for p, t in _jsonl(RAW / "staff17.pages.jsonl").items():
        put(1000 + p, t, "スタッフ声明")
    for code, base in NTSB.items():
        txt = (ROOT / "analytics" / "materials" / "ep7" / "s2" / "ocr" / f"{code}.ocr.txt").read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"^## .*?_p(\d+)\.png.*?$(.*?)(?=^## |\Z)", txt, re.M | re.S):
            put(base + int(m.group(1)), "［OCR（スキャン）］\n" + m.group(2).strip(), f"NTSB {code}")
    for p, t in _jsonl(RAW / "P200056T_ua93_cvr_transcript.pages.jsonl").items():
        put(6000 + p, t, "CVR")
    for p, t in _jsonl(RAW / "ncstar1.pages.jsonl").items():
        put(7000 + p, t, "NIST")
    put(8001, (SRC / "new" / "hearing2" / "transcript_0523.txt").read_text(encoding="utf-8", errors="replace"), "運輸長官の証言")
    with OUT.open("w", encoding="utf-8") as fo:
        for n in sorted(pages):
            fo.write(f"=== p{n} ===\n{pages[n].rstrip()}\n")
    print(f"{OUT.name}: {len(pages)} 頁＝" + "・".join(f"{k} {v}" for k, v in n_of.items()))


if __name__ == "__main__":
    main()
