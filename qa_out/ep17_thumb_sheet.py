# -*- coding: utf-8 -*-
"""17本目 ⑥：サムネの候補を1枚に並べる（640px の2×2＋YouTube の一覧の幅 210px の4枚＝記憶 feedback-thumbnail-must-read-at-210px）。

    python qa_out/ep17_thumb_sheet.py out/thumb/ep17-ab/ep17_Hinv_t1.png,... [--out=out/thumb/ep17-ab/_sheet.png] [--labels=t1,k05,...]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")


def arg(k, d=""):
    return next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith(f"--{k}=")), d)


def main():
    paths = [HERE / p for p in sys.argv[1].split(",") if p]
    labels = arg("labels").split(",") if arg("labels") else [p.stem for p in paths]
    out = HERE / arg("out", "out/thumb/ep17-ab/_sheet.png")
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    except OSError:
        font = ImageFont.load_default()
    cols = 2
    rows = (len(paths) + cols - 1) // cols
    lab = 30
    big_w, big_h = 640, 360
    sm_w, sm_h = 210, 118
    H = rows * (big_h + lab) + lab + sm_h + 10
    W = max(cols * big_w, len(paths) * (sm_w + 20))
    sheet = Image.new("RGB", (W, H), "#222")
    d = ImageDraw.Draw(sheet)
    for i, (p, name) in enumerate(zip(paths, labels)):
        im = Image.open(p).convert("RGB")
        x, y = (i % cols) * big_w, (i // cols) * (big_h + lab)
        d.text((x + 6, y + 3), f"{i + 1}. {name}（640px）", fill="#ff0", font=font)
        sheet.paste(im.resize((big_w, big_h), Image.LANCZOS), (x, y + lab))
    y0 = rows * (big_h + lab)
    d.text((6, y0 + 3), "YouTube の一覧の幅（210px）", fill="#ff0", font=font)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((sm_w, sm_h), Image.LANCZOS)
        sheet.paste(im, (i * (sm_w + 20), y0 + lab))
        d.text((i * (sm_w + 20) + 4, y0 + lab + 2), str(i + 1), fill="#ff0", font=font)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"→ {out.relative_to(HERE)}  {sheet.size}")


if __name__ == "__main__":
    main()
