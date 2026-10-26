# 26本目 ②：頁の中の「この語からこの語まで」を文字の層の座標で切り出して描き、縦に積む（表を頁の画像で確かめる）
# 使い方: python -P ref/ep26/probe/table26.py <pdf> <出力.png> "<頁>|<始まりの語>|<終わりの語>" ... [--dpi 200]
import argparse, sys

import fitz
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out")
    ap.add_argument("spec", nargs="+")
    ap.add_argument("--dpi", type=int, default=200)
    a = ap.parse_args()
    doc = fitz.open(a.pdf)
    parts = []
    for s in a.spec:
        p, start, end = s.split("|")
        pg = doc[int(p) - 1]
        r0, r1 = pg.search_for(start), pg.search_for(end)
        if not r0 or not r1:  # 見つからなければ止める（黙って別の所を切らない）
            print(f"NOT FOUND p{p}: {start if not r0 else end}")
            return 1
        y0 = max(0, r0[0].y0 - 8)
        y1 = min(pg.rect.height, r1[-1].y1 + 8)
        clip = fitz.Rect(pg.rect.x0 + 20, y0, pg.rect.x1 - 20, y1)
        pix = pg.get_pixmap(dpi=a.dpi, clip=clip, colorspace=fitz.csGRAY)
        parts.append((p, Image.frombytes("L", (pix.width, pix.height), pix.samples)))
    W = max(im.width for _, im in parts) + 60
    H = sum(im.height + 10 for _, im in parts) + 10
    sheet = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(sheet)
    y = 10
    for p, im in parts:
        d.text((4, y + 4), f"p{p}", fill=0)
        sheet.paste(im, (60, y))
        y += im.height + 10
    sheet.save(a.out)
    print(f"sheet {W}x{H} parts {len(parts)} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
