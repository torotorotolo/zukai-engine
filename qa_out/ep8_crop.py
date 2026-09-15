# -*- coding: utf-8 -*-
"""ep8 ⑤c' ── 原寸のまま切り出して1枚に貼る（拡大も縮小もしない）。

⚠️ これは「縮小したコンタクトシート」ではない。**画素は1:1のまま**で、
   離れた場所を1枚に集めるだけ（[[feedback-sheet-cannot-judge-three-types]] が
   禁じているのは**縮小して決めること**）。
   原寸を丸ごと読み直さないための道具（鉄則1「切り出してから読む」）。

使い方
  python qa_out/ep8_crop.py <出力名> <cid>:<x>,<y>,<w>,<h>[:見出し] ...
"""
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw  # noqa: E402

QA = ROOT / "out/jiko/qa_ep8-r01"
OUT = ROOT / "qa_out/crops"
OUT.mkdir(exist_ok=True)
PAD = 26          # 見出しの帯の高さ
GAP = 8


def main():
    name = sys.argv[1]
    specs = []
    for arg in sys.argv[2:]:
        cid, rest = arg.split(":", 1)
        parts = rest.split(":")
        box = [int(v) for v in parts[0].split(",")]
        cap = parts[1] if len(parts) > 1 else ""
        specs.append((cid, box, cap))

    tiles = []
    for cid, (x, y, w, h), cap in specs:
        with Image.open(QA / f"cut_{cid}.jpg") as im:
            im = im.convert("RGB")
            W, H = im.size
            x0, y0 = max(0, x), max(0, y)
            x1, y1 = min(W, x + w), min(H, y + h)
            tile = im.crop((x0, y0, x1, y1))
        tiles.append((cid, tile, cap, (x0, y0, x1, y1)))

    cw = max(t.width for _, t, _, _ in tiles)
    th = sum(t.height + PAD + GAP for _, t, _, _ in tiles)
    canvas = Image.new("RGB", (cw, th), (16, 16, 18))
    d = ImageDraw.Draw(canvas)
    yy = 0
    for cid, tile, cap, bx in tiles:
        d.text((4, yy + 6), f"{cid}  {bx[0]},{bx[1]}-{bx[2]},{bx[3]}  {cap}",
               fill=(255, 220, 120))
        yy += PAD
        canvas.paste(tile, (0, yy))
        yy += tile.height + GAP
    p = OUT / f"{name}.png"
    canvas.save(p)
    print(f"{p}   {canvas.width}x{canvas.height}   （画素は1:1・拡大縮小なし）")
    for cid, tile, cap, bx in tiles:
        print(f"   {cid}  切り出し {tile.width}x{tile.height}  at {bx[0]},{bx[1]}")


main()
