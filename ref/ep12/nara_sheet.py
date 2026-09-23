# -*- coding: utf-8 -*-
"""NARA 51点（`ref/ep12/img/nara/<naId>.jpg`）を 640px のシート（2列×3行）に並べる（12本目 ⑤b-2）。

⚠️ シートで決めてよくない型が3つある（図の比例・小さな点・札の切れ）
   → 記憶 feedback-sheet-cannot-judge-three-types。人の顔の有無は**疑いだけ原寸**で見直す。
各コマの下に `番号 naId 寸法` と NARA の題名（scope）を出す（題名は当たりであって正本ではない）。

    python ref/ep12/nara_sheet.py <出力フォルダ>
"""
import csv
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
NARA = HERE / "img" / "nara"
FONT = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
CW, CH, COLS, ROWS, LAB = 640, 400, 2, 3, 44


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(NARA / "index.tsv", encoding="utf-8"), delimiter="\t"))
    if len(rows) != 51:
        raise SystemExit(f"🔴 index.tsv が {len(rows)} 行（51 のはず）")
    per = COLS * ROWS
    for i in range(0, len(rows), per):
        chunk = rows[i:i + per]
        sh = Image.new("RGB", (CW * COLS, (CH + LAB) * ROWS), (16, 16, 18))
        d = ImageDraw.Draw(sh)
        for k, r in enumerate(chunk):
            f = NARA / f"{r['naId']}.jpg"
            with Image.open(f) as im0:
                w, h = im0.size
                im = im0.convert("RGB")
                im.thumbnail((CW - 8, CH - 8), Image.LANCZOS)
            x, y = (k % COLS) * CW, (k // COLS) * (CH + LAB)
            sh.paste(im, (x + (CW - im.width) // 2, y + (CH - im.height) // 2))
            n = i + k + 1
            d.text((x + 6, y + CH + 2), f"#{n:02} {r['naId']}  {w}x{h}", fill=(255, 220, 90), font=FONT)
            d.text((x + 6, y + CH + 21), r["scope"][:78], fill=(235, 235, 235), font=FONT)
        p = out / f"nara_{i // per + 1:02}.jpg"
        sh.save(p, quality=90)
        print(f"✓ {p.name}  #{i + 1:02}〜#{i + len(chunk):02}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1]))
