# -*- coding: utf-8 -*-
"""25本目②：見本帳（2列×3行・1こま幅640px）を作る。こまの下に「番号・実寸・名前」を書く。
小さい絵は2倍まで拡大して入れる（実寸は札に書く＝拡大の分だけ甘く見えることに注意）。
使い方: python sheet25.py <出力png> <絵のファイル> [<絵のファイル> ...]   （6枚まで）"""
import os, sys

from PIL import Image, ImageDraw, ImageFont

CW, CH, CAP, PAD = 640, 480, 44, 12
FONTS = [r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\YuGothM.ttc", r"C:\Windows\Fonts\msgothic.ttc"]


def font(sz):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def main():
    out, files = sys.argv[1], sys.argv[2:8]
    cols, rows = 2, (len(files) + 1) // 2
    W = PAD + cols * (CW + PAD)
    H = PAD + rows * (CH + CAP + PAD)
    sheet = Image.new("RGB", (W, H), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    f = font(17)
    for i, fn in enumerate(files):
        im = Image.open(fn).convert("RGB")
        w, h = im.size
        s = min(CW / w, CH / h, 2.0)
        im2 = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
        cx = PAD + (i % 2) * (CW + PAD)
        cy = PAD + (i // 2) * (CH + CAP + PAD)
        sheet.paste(im2, (cx + (CW - im2.width) // 2, cy + (CH - im2.height) // 2))
        name = os.path.basename(fn)
        d.text((cx + 4, cy + CH + 4), f"#{i + 1}  {w}x{h}  x{s:.2f}", fill=(255, 230, 120), font=f)
        d.text((cx + 4, cy + CH + 23), name[:62], fill=(220, 220, 220), font=font(14))
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
