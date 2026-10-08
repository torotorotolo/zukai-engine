# -*- coding: utf-8 -*-
"""報告書の PDF の頁から、埋め込みの画像を原寸で取り出す（20本目 映像方針・scratchpad）。

  python pdfimg20.py <pdf> <PDFの頁(1から)> <出力.png>     いちばん大きい画像を原寸で
  python pdfimg20.py crop <入力.png> <x0> <y0> <x1> <y1> <出力.png> [長辺の上限px]   比率(0〜1)で切る

取り出した画像の幅・高さ・ビット深度・色空間・フィルタを印字する（JBIG2 の1ビットか確かめる）。
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')


def extract(pdf, pno, out):
    import fitz
    doc = fitz.open(pdf)
    page = doc[pno - 1]
    best = None
    for img in page.get_images(full=True):
        xref = img[0]
        info = doc.extract_image(xref)
        area = info['width'] * info['height']
        if best is None or area > best[0]:
            best = (area, xref, info)
    if best is None:
        raise SystemExit('画像なし')
    _, xref, info = best
    pix = fitz.Pixmap(doc, xref)
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    pix.save(out)
    r = page.rect
    print('page %.0fx%.0fpt  image %dx%d bpc=%s cs=%s ext=%s  → %s  (約%.0fdpi)' % (
        r.width, r.height, info['width'], info['height'], info.get('bpc'), info.get('colorspace'),
        info.get('ext'), out, info['width'] / (r.width / 72)))


def crop(src, x0, y0, x1, y1, out, cap=None):
    from PIL import Image
    im = Image.open(src)
    w, h = im.size
    box = (int(float(x0) * w), int(float(y0) * h), int(float(x1) * w), int(float(y1) * h))
    c = im.crop(box)
    if c.mode == '1':
        c = c.convert('L')
    if cap:
        cap = int(cap)
        s = min(1.0, cap / max(c.size))
        if s < 1.0:
            c = c.resize((max(1, int(c.size[0] * s)), max(1, int(c.size[1] * s))), Image.LANCZOS)
    c.save(out)
    print('crop %s of %dx%d → %dx%d  %s' % (box, w, h, c.size[0], c.size[1], out))


if __name__ == '__main__':
    if sys.argv[1] == 'crop':
        crop(*sys.argv[2:9]) if len(sys.argv) > 8 else crop(*sys.argv[2:8])
    else:
        extract(sys.argv[1], int(sys.argv[2]), sys.argv[3])
