# -*- coding: utf-8 -*-
"""報告書96-5 の頁（印刷頁の番号）を幅640pxの見本帳にする（2列・高さ1850まで）。
使い方: sheet_pages.py <名前の頭> <印刷頁 ...>   /   sheet_pages.py --log <sheet.png>"""
import json, os, sys, time
import fitz
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = r"C:\Users\konar\Desktop\zukai-engine\ref\ep17\src"
FONT = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
W, MAXH, LAB = 640, 1880, 30
PM = json.load(open(os.path.join(HERE, "pagemap.json")))
FIG = {x[2]: x[0] + " " + x[1] for x in json.load(open(os.path.join(HERE, "figmap.json"), encoding="utf-8"))}

def locate(pr):
    for x in PM:
        if x["printed"] <= pr <= x["printed_end"]:
            return x
    raise KeyError(pr)

def render(pr):
    x = locate(pr)
    d = fitz.open(os.path.join(S, f"jtsb_96-5_ja_{x['file']:02d}.pdf"))
    pg = d[x["pdf"] - 1]
    z = W / pg.rect.width
    pix = pg.get_pixmap(matrix=fitz.Matrix(z, z))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return im, f"p.{pr} (ja_{x['file']:02d} pdf{x['pdf']}) {FIG.get(pr, '')}"

def main():
    if sys.argv[1] == "--log":
        png = sys.argv[2]
        meta = open(png + ".txt", encoding="utf-8").read().strip().splitlines()
        with open(os.path.join(HERE, "seen_log.tsv"), "a", encoding="utf-8") as fo:
            fo.write(f"{time.strftime('%H:%M')}\t{os.path.basename(png)}\t{len(meta)}\t{';'.join(meta)}\n")
        n = sum(1 for _ in open(os.path.join(HERE, "seen_log.tsv"), encoding="utf-8"))
        print(f"logged. images read in this chat = {n}")
        return
    head, prs = sys.argv[1], [int(a) for a in sys.argv[2:]]
    cells = [render(p) for p in prs]
    sheets, cur, col_h = [], [], [0, 0]
    for im, lab in cells:
        h = im.height + LAB
        c = 0 if col_h[0] <= col_h[1] else 1
        if col_h[c] + h > MAXH:
            sheets.append(cur); cur, col_h = [], [0, 0]; c = 0
        cur.append((c, col_h[c], im, lab)); col_h[c] += h
    if cur: sheets.append(cur)
    for k, sh in enumerate(sheets, 1):
        H = max(y + im.height + LAB for c, y, im, lab in sh)
        out = Image.new("RGB", (W * 2 + 10, H), (40, 40, 40))
        d = ImageDraw.Draw(out)
        for c, y, im, lab in sh:
            x = c * (W + 10)
            d.text((x + 4, y + 2), lab[:44], fill=(255, 230, 80), font=FONT)
            out.paste(im, (x, y + LAB))
        fn = os.path.join(HERE, f"{head}_{k}.png")
        out.save(fn)
        open(fn + ".txt", "w", encoding="utf-8").write("\n".join(lab for *_, lab in sh))
        print(fn, len(sh), out.size)

main()
