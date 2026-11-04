# -*- coding: utf-8 -*-
"""29本目 ⑥：サムネの地の候補を 640px の2列で並べて見る（札つき）。
    python -P qa_out/ep29_r01/thumb_ground_sheet.py 出力.jpg 名前 名前 …（ref/ep29/<名前>.jpg か src/eizou/<名前> の実パス）
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
CW, CH = 640, 360
out, names = sys.argv[1], sys.argv[2:]
rows = (len(names) + 1) // 2
sheet = Image.new("RGB", (CW * 2, CH * rows), (16, 16, 16))
font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
for i, n in enumerate(names):
    p = Path(n) if Path(n).exists() else ROOT / "ref" / "ep29" / f"{n}.jpg"
    im = Image.open(p).convert("RGB")
    w, h = im.size
    scale = min(CW / w, CH / h)      # 切らずに全体を入れる（地を選ぶのに端まで見たい）
    t = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    x, y = (i % 2) * CW, (i // 2) * CH
    sheet.paste(t, (x + (CW - t.width) // 2, y + (CH - t.height) // 2))
    d = ImageDraw.Draw(sheet)
    d.rectangle((x, y, x + 8 + d.textlength(f"{n} {w}x{h}", font=font), y + 30), fill=(0, 0, 0))
    d.text((x + 4, y + 1), f"{Path(n).stem} {w}x{h}", fill=(255, 230, 0), font=font)
sheet.save(out, quality=88)
print(out, sheet.size)
