# -*- coding: utf-8 -*-
"""12本目 ⑤b-4（2026-09-23）：報告書の頁の文字の層（OCR）を、頁に対する 0〜1 の座標で1行ずつ出す。

なぜ要るか：頁の切り口（`trim=`・trace の `crop=`）は**行と行のすきま**で切る（§5b-40）。
画像を読まずに、図の題（Figure N.）と図の上下の行の位置から切り口を決められる。
⚠️ 行の箱は上下が少し重なることがある（表22 など）＝そのときは行の中心どうしの中ほどで切る。

使い方:
    python qa_out/ep12_pglines.py 219 227 2069   → 頁ごとに「y 上-下  x 左-右  先頭の文字」
    頁番号は台本の通し番号（DNA p1〜・WT p1001〜・DASA p2001〜）。[IMG] は画像の塊
"""
import sys
from pathlib import Path

import fitz

sys.stdout.reconfigure(encoding="utf-8")
SRC = Path(__file__).resolve().parents[1] / "ref" / "ep12" / "src"
DOCS = [(2000, "dasa1251_v2.pdf"), (1000, "project41_wt923.pdf"), (0, "dna6035f.pdf")]


def open_page(pr):
    for off, name in DOCS:
        if pr > off:
            doc = fitz.open(SRC / name)
            return doc[pr - off - 1]
    raise SystemExit(f"頁 {pr} が無い")


for a in sys.argv[1:]:
    pr = int(a)
    pg = open_page(pr)
    W, H = pg.rect.width, pg.rect.height
    rows = []
    for b in pg.get_text("dict")["blocks"]:
        if b.get("type") == 1:
            x0, y0, x1, y1 = b["bbox"]
            rows.append((y0 / H, y1 / H, x0 / W, x1 / W, "[IMG]"))
            continue
        for ln in b.get("lines", []):
            t = "".join(s["text"] for s in ln["spans"]).strip()
            if t:
                x0, y0, x1, y1 = ln["bbox"]
                rows.append((y0 / H, y1 / H, x0 / W, x1 / W, t[:70]))
    rows.sort()
    print(f"=== p{pr}  ({len(rows)} rows)")
    for y0, y1, x0, x1, t in rows:
        print(f"  y {y0:.3f}-{y1:.3f}  x {x0:.3f}-{x1:.3f}  {t}")
