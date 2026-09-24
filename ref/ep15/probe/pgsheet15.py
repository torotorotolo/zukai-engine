# -*- coding: utf-8 -*-
"""15本目②：一次資料の PDF の頁を 640px にして 2列×3行のシートにする。
python pgsheet15.py <出力.jpg> <pdf名>:<頁(1始まり)> ...（pdf名は ref/ep15/src/ の中）"""
import os, sys
import fitz
from PIL import Image, ImageDraw, ImageFont

SRC = r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/src/'
out, specs = sys.argv[1], sys.argv[2:]
TW, TH = 640, 500
font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 17)
sheet = Image.new('RGB', (TW * 2, (TH + 24) * 3), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for j, spec in enumerate(specs[:6]):
    name, pno = spec.rsplit(':', 1)
    doc = fitz.open(SRC + name)
    pg = doc[int(pno) - 1]
    # 画像の置き場（和集合）＋下の説明文 50pt だけを切り出す（頁全体だと写真が小さすぎる）
    clip = None
    for info in pg.get_images(full=True):
        for r in pg.get_image_rects(info[0]):
            if r.width * r.height < 80 * 80:
                continue
            clip = r if clip is None else clip | r
    clip = fitz.Rect(pg.rect) if clip is None else fitz.Rect(max(0, clip.x0 - 6), max(0, clip.y0 - 6), min(pg.rect.x1, clip.x1 + 6), min(pg.rect.y1, clip.y1 + 50))
    zoom = min(TW / clip.width, TH / clip.height) * 1.0
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    im.thumbnail((TW, TH))
    x, y = (j % 2) * TW, (j // 2) * (TH + 24)
    sheet.paste(im, (x + (TW - im.width) // 2, y + 24))
    d.text((x + 4, y + 2), '%s p%s' % (name.replace('ntsb_docket_', '#')[:40], pno), fill=(255, 255, 0), font=font)
sheet.save(out, quality=85)
print('ok', out)
