# -*- coding: utf-8 -*-
"""18本目 ⑤b-7a（2026-10-04）：Actions の試し焼き（`out/jiko/qa_ep18_b7a/`）の `at` のコマを 640px のシート（2列×3行）に並べる。
   python qa_out/ep18_b7a/make_sheets.py [qa_ep18_b7a] → qa_out/ep18_b7a/sheet_<n>.jpg（1280×1080・各コマの左上にファイル名）
   ＋ crop <名> <x0> <y0> <x1> <y1> [qa_dir] で原寸の切り出し（qa_out/ep18_b7a/crop_<名>_<x0>_<y0>.jpg）
   （⑤b-6b の qa_out/ep18_b6b/make_sheets.py を写して CUTS と置き場だけ替えた）"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CUTS = ("c114 c116 c201 c203 c208 c212 c215 c220 c301 c423 c601 c611 c627 c709 c722 c805 c812 c819 c822 "
        "c906 c911 c914 c920 ca05 ca06 ca13 ca20 cb01 cb23").split()
args = [a for a in sys.argv[1:]]
qa_dir = next((a for a in args if a.startswith("qa_")), "qa_ep18_b7a")
args = [a for a in args if not a.startswith("qa_")]
base = ROOT / "out" / "jiko" / qa_dir
hit = next(iter(base.rglob("at_*_095.jpg")), None)
SRC = hit.parent if hit else base
if args and args[0] == "crop":
    name, box = args[1], tuple(int(v) for v in args[2:6])
    Image.open(SRC / f"at_{name}.jpg").convert("RGB").crop(box).save(OUT / f"crop_{name}_{box[0]}_{box[1]}.jpg", quality=92)
    print("crop", name, box)
    sys.exit(0)
order = [n for n in args] or [f"{c}_095" for c in CUTS]
tag = "fix" if qa_dir.endswith("fix") else ""
for n in range(0, len(order), 6):
    sheet = Image.new("RGB", (1280, 1080), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for j, name in enumerate(order[n:n + 6]):
        p = SRC / f"at_{name}.jpg"
        if not p.exists():
            print("無い", p.name)
            continue
        im = Image.open(p).convert("RGB").resize((640, 360), Image.LANCZOS)
        x, y = (j % 2) * 640, (j // 2) * 360
        sheet.paste(im, (x, y))
        d.rectangle((x, y, x + 120, y + 16), fill=(0, 0, 0))
        d.text((x + 4, y + 2), name, fill=(255, 230, 0))
    fn = OUT / f"sheet{tag}_{n // 6 + 1}.jpg"
    sheet.save(fn, quality=90)
    print("sheet", fn.name, order[n:n + 6])
