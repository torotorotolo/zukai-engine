# -*- coding: utf-8 -*-
"""直したカットの**その場所だけ**を原寸で切り出して、1枚に縦へ並べる。

■ なぜ（[[feedback-subagents-must-not-read-images]]／CLAUDE.md 鉄則1）
  画像は読んだあともコンテキストに残り、**枚数の2乗**で効く。
  ⚠️ だからといって**縮小したコンタクトシートで判断するのは禁止**（37pxの人物を見逃した前例）。
  → **縮小はしない。** 原寸のまま、見たい所だけを切り出して縦に積む。
    1枚あたりの画素は減り、見る目は原寸のまま保てる。

    python -u qa_out/kb_z_strip.py <出力名> <cid:x0,y0,x1,y1> ...

  例）python -u qa_out/kb_z_strip.py map c105:120,330,960,520 c513:200,320,1040,510
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
SRC = ROOT / "out" / "jiko" / "qa_keybridge-r07"
OUT = ROOT / "out" / "jiko" / "_strip"


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    name, specs = argv[0], argv[1:]
    OUT.mkdir(parents=True, exist_ok=True)
    tiles = []
    for s in specs:
        cid, box = s.split(":")
        x0, y0, x1, y1 = (int(v) for v in box.split(","))
        p = SRC / f"cut_{cid}.jpg"
        if not p.exists():
            raise SystemExit(f"🔴 {p} が無い（0件と数えない）")
        im = Image.open(p).convert("RGB").crop((x0, y0, x1, y1))
        tiles.append((cid, im))
        print(f"  {cid}  {x1 - x0}×{y1 - y0}px  ← {p.name}")
    w = max(t[1].width for t in tiles)
    h = sum(t[1].height + 22 for t in tiles)
    sheet = Image.new("RGB", (w, h), (255, 0, 0))          # 継ぎ目は赤（切り出しの境が分かる）
    d = ImageDraw.Draw(sheet)
    y = 0
    for cid, im in tiles:
        d.rectangle([0, y, w, y + 20], fill=(255, 255, 255))
        d.text((6, 4 + y), f"{cid}  ({im.width}x{im.height} 原寸)", fill=(0, 0, 0))
        y += 22
        sheet.paste(im, (0, y))
        y += im.height
    dest = OUT / f"{name}.png"
    sheet.save(dest)
    print(f"\n✓ {dest}  {sheet.width}×{sheet.height}px（**縮小していない**）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
