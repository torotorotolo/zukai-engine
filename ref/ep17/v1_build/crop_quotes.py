# -*- coding: utf-8 -*-
"""決め所の原文を、頁の画像から段落ごとに切り出して1枚に並べる（④で目で当てる用・画像は git に入れない）。

  crop_quotes.py text <出力.png> "<ラベル>|S1|<印刷頁>|<探す語>" ...   （S2 は PDF の頁）
      文字層の位置で段落を探し、前後1行を足して 200dpi で切る。当たった行は赤い枠
  crop_quotes.py img <出力フォルダ> <dpi> <印刷頁> ...                 （画像だけの頁＝付図・別添）
      probe/pagemap.json で PDF の頁を引いて書き出す（A3 の折り込み＝1枚で印刷頁2つ）
  crop_quotes.py box <出力.png> "<ラベル>|<png>|x0,y0,x1,y1" ...        （img の画素で切る）

⚠️ ラベルは ASCII だけ（PIL の既定の字体に日本語が無い）。
"""
import json
import os
import re
import sys
import unicodedata

import fitz
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'src'))
PROBE = os.path.normpath(os.path.join(HERE, '..', 'probe'))
OFF = {"ja_01": -17, "ja_02": 31, "ja_03": 63, "ja_04": 77}
DPI = 200


def n(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', s))


def s1_map():
    m = {}
    with open(os.path.join(SRC, 'ja_norm.txt'), encoding='utf-8') as f:
        for line in f:
            fn, pdf, _p, _t = line.split('\t', 3)
            if fn in OFF:
                m[int(pdf[3:]) + OFF[fn]] = (fn, int(pdf[3:]))
    return m


def open_page(src, page, cache={}):
    if src == 'S1':
        fn, pdf = s1_map()[page]
        path = os.path.join(SRC, 'jtsb_96-5_%s.pdf' % fn)
    elif src == 'S2':
        path, pdf = os.path.join(SRC, 'court_2003-12-26_H7wa4179.pdf'), page
    else:
        raise SystemExit('E 資料は S1 か S2: %s' % src)
    if path not in cache:
        cache[path] = fitz.open(path)
    return cache[path][pdf - 1]


def lines_of(pg):
    out = []
    for b in pg.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = ''.join(sp['text'] for sp in ln['spans'])
            if t.strip():
                out.append((fitz.Rect(ln['bbox']), t))
    out.sort(key=lambda r: (round(r[0].y0 / 4), r[0].x0))
    return out


def crop_text(spec):
    label, src, page, frag = spec.split('|', 3)
    pg = open_page(src, int(page))
    ls = lines_of(pg)
    joined, starts = '', []
    for _r, t in ls:
        starts.append(len(joined))
        joined += n(t)
    key = n(frag)
    i = joined.find(key)
    if i < 0:
        i = joined.find(key[:8])
        key = key[:8]
    if i < 0:
        raise SystemExit('E 当たらない: %s（%s p%s）' % (frag, src, page))
    a = max(k for k, s in enumerate(starts) if s <= i)
    b = max(k for k, s in enumerate(starts) if s <= i + len(key) - 1)
    hit = fitz.Rect(ls[a][0])
    for k in range(a, b + 1):
        hit |= ls[k][0]
    lh = max(12.0, (ls[a][0].height))
    left = min(r.x0 for r, _t in ls) - 6
    right = max(r.x1 for r, _t in ls) + 6
    clip = fitz.Rect(left, hit.y0 - 1.3 * lh, right, hit.y1 + 1.3 * lh) & pg.rect
    pix = pg.get_pixmap(dpi=DPI, clip=clip, colorspace=fitz.csGRAY)
    im = Image.frombytes('L', (pix.width, pix.height), pix.samples).convert('RGB')
    z = DPI / 72.0
    d = ImageDraw.Draw(im)
    d.rectangle([(hit.x0 - clip.x0) * z - 3, (hit.y0 - clip.y0) * z - 3,
                 (hit.x1 - clip.x0) * z + 3, (hit.y1 - clip.y0) * z + 3], outline=(220, 0, 0), width=3)
    return label, im


def crop_box(spec):
    label, png, box = spec.split('|')
    x0, y0, x1, y1 = (int(v) for v in re.split(r'[,\-]', box))
    return label, Image.open(png).convert('RGB').crop((x0, y0, x1, y1))


def stack(items, out):
    w = max(im.width for _l, im in items)
    h = sum(im.height + 34 for _l, im in items)
    sheet = Image.new('RGB', (w, h), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    y = 0
    for label, im in items:
        d.rectangle([0, y, w, y + 30], fill=(40, 40, 40))
        d.text((8, y + 8), label, fill=(255, 255, 255))
        sheet.paste(im, (0, y + 32))
        y += im.height + 34
    sheet.save(out)
    print('%s %dx%d（%d件）' % (out, w, h, len(items)))


def img_pages(outdir, dpi, pages):
    pm = json.load(open(os.path.join(PROBE, 'pagemap.json'), encoding='utf-8'))
    os.makedirs(outdir, exist_ok=True)
    docs = {}
    for p in pages:
        e = [r for r in pm if r['printed'] <= p <= r['printed_end']]
        if not e:
            raise SystemExit('E pagemap に無い頁: %d' % p)
        r = e[0]
        path = os.path.join(SRC, 'jtsb_96-5_ja_%02d.pdf' % r['file'])
        docs.setdefault(path, fitz.open(path))
        pix = docs[path][r['pdf'] - 1].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
        fn = os.path.join(outdir, 'pg_%03d.png' % p)
        pix.save(fn)
        print('%s ja_%02d pdf%d a3=%s %dx%d' % (fn, r['file'], r['pdf'], r['a3'], pix.width, pix.height))


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'text':
        stack([crop_text(s) for s in sys.argv[3:]], sys.argv[2])
    elif mode == 'box':
        stack([crop_box(s) for s in sys.argv[3:]], sys.argv[2])
    elif mode == 'img':
        img_pages(sys.argv[2], int(sys.argv[3]), [int(p) for p in sys.argv[4:]])
    else:
        raise SystemExit(__doc__)
