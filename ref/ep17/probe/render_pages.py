# -*- coding: utf-8 -*-
"""報告書の画像だけの頁を印刷頁の番号で PNG に書き出す（OCR と見本帳の元）。
使い方: render_pages.py <dpi> <印刷頁の範囲 106-163 のように> [...]"""
import os, sys
import fitz

S = r"C:\Users\konar\Desktop\zukai-engine\ref\ep17\src"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
os.makedirs(OUT, exist_ok=True)
counts = {i: fitz.open(os.path.join(S, f"jtsb_96-5_ja_{i:02d}.pdf")).page_count for i in range(4, 13)}
seq = []
for i in range(4, 13):
    for p in range(29 if i == 4 else 1, counts[i] + 1):
        seq.append((i, p))

def locate(printed):
    return seq[printed - 106]

dpi = int(sys.argv[1])
docs = {}
for rng in sys.argv[2:]:
    a, b = (int(x) for x in rng.split("-")) if "-" in rng else (int(rng), int(rng))
    for pr in range(a, b + 1):
        f, p = locate(pr)
        if f not in docs:
            docs[f] = fitz.open(os.path.join(S, f"jtsb_96-5_ja_{f:02d}.pdf"))
        pg = docs[f][p - 1]
        pix = pg.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
        fn = os.path.join(OUT, f"p{pr:03d}.png")
        pix.save(fn)
        print(f"p{pr:03d} ja_{f:02d} pdf{p} {pix.width}x{pix.height}")
