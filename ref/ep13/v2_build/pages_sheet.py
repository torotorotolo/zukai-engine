# -*- coding: utf-8 -*-
"""仏の報告（S1）などの頁を、指定の縦範囲だけ描いて横に並べる（④' の確認用・読むだけ）。
    python pages_sheet.py OUT.png 92 90:0.0-0.7 17
頁は make_pages.py の通し番号。幅 W で描く。"""
import sys
from pathlib import Path
import fitz
from PIL import Image

SRC = Path("C:/Users/konar/Desktop/zukai-engine/ref/ep13/src")
DOCS = [(0, "faa_FinalAccidentReportinFrench.pdf"), (1000, "aib_8-76_TC-JAV.pdf"),
        (2000, "senate_cprt93_dc10.pdf"), (3000, "ntsb_AAR73-02_N103AA_erau.pdf"),
        (4000, "faa_AD74-08-04.pdf"), (4100, "faa_AD74-12-07.pdf"), (4200, "faa_AD75-15-05.pdf"),
        (4300, "fr_1974-04-02_11992.pdf"), (5000, "faa_SB52-37.pdf"), (5100, "faa_SB52-38.pdf")]
W = int(dict(a.split("=") for a in sys.argv if a.startswith("W=")).get("W", 640)) if any(a.startswith("W=") for a in sys.argv) else 640


def page_img(spec):
    if ":" in spec:
        p, r = spec.split(":")
        y0, y1 = map(float, r.split("-"))
    else:
        p, y0, y1 = spec, 0.0, 1.0
    gp = int(p)
    off, pdf = [d for d in sorted(DOCS, reverse=True) if gp > d[0]][0]
    doc = fitz.open(SRC / pdf)
    pg = doc[gp - off - 1]
    z = W / pg.rect.width
    pix = pg.get_pixmap(matrix=fitz.Matrix(z, z))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return im.crop((0, int(im.height * y0), im.width, int(im.height * y1)))


out = sys.argv[1]
ims = [page_img(s) for s in sys.argv[2:] if not s.startswith("W=")]
H = max(i.height for i in ims)
sheet = Image.new("RGB", (sum(i.width for i in ims) + 10 * (len(ims) - 1), H), "white")
x = 0
for i in ims:
    sheet.paste(i, (x, 0))
    x += i.width + 10
sheet.save(out)
print(out, sheet.size)
