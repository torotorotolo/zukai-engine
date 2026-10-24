# -*- coding: utf-8 -*-
"""25本目②：PDF の頁を PNG にする（OCR・見本帳・切り出し用）。出力は src/ の下（git の外）。
使い方: python render25.py <pdf> <出力フォルダ> <dpi> <PDF頁 a-b | p1,p2> [rot=0|90|180|270]"""
import os, sys

import fitz


def main():
    pdf, outdir, dpi, sel = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    rot = 0
    for a in sys.argv[5:]:
        if a.startswith("rot="):
            rot = int(a[4:])
    os.makedirs(outdir, exist_ok=True)
    if "-" in sel:
        a, b = (int(x) for x in sel.split("-"))
        pages = list(range(a, b + 1))
    else:
        pages = [int(x) for x in sel.split(",")]
    doc = fitz.open(pdf)
    stem = os.path.splitext(os.path.basename(pdf))[0]
    for p in pages:
        pg = doc[p - 1]
        pix = pg.get_pixmap(dpi=dpi, matrix=None) if rot == 0 else pg.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72).prerotate(rot))
        fn = os.path.join(outdir, f"{stem}_p{p:03d}_{dpi}dpi{'_r%d' % rot if rot else ''}.png")
        pix.save(fn)
        print(fn, pix.width, pix.height, "page.rotation=", pg.rotation, flush=True)


if __name__ == "__main__":
    main()
