# -*- coding: utf-8 -*-
"""30本目 ②：取ってあるストーリーボードの断片（<出力>/<id>_sb/）から、N秒おきの縮小画像を1枚に並べる（場面の判定用）。
  python -I -X utf8 sbgrid30.py <動画id> <yt-dlp -j の json> <出力フォルダ> <間隔秒> [列=6] [行=4] [幅=213]
"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')
vid, meta, out, step = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 6
rows = int(sys.argv[6]) if len(sys.argv) > 6 else 4
tw = int(sys.argv[7]) if len(sys.argv) > 7 else 213
d = json.load(open(meta, encoding='utf-8'))
sb = [f for f in d['formats'] if f['format_id'] == 'sb0'][0]
W, H, R, C = sb['width'], sb['height'], sb['rows'], sb['columns']
th = int(tw * H / W)
thumbs = []
t0 = 0.0
for n, fr in enumerate(sb['fragments']):
    im = Image.open(os.path.join(out, vid + '_sb', 'f%03d.jpg' % n)).convert('RGB')
    per = fr['duration'] / (R * C)
    k = 0
    for y in range(R):
        for x in range(C):
            box = (x * W, y * H, (x + 1) * W, (y + 1) * H)
            if box[2] <= im.width and box[3] <= im.height:
                thumbs.append((t0 + per * k, im.crop(box)))
            k += 1
    t0 += fr['duration']
keep, nxt = [], 0.0
for t, im in thumbs:
    if t >= nxt:
        keep.append((t, im))
        nxt = t + step
per_sheet = cols * rows
print('縮小画像 %d → %d（%g秒おき）' % (len(thumbs), len(keep), step))
for s in range(0, len(keep), per_sheet):
    sheet = Image.new('RGB', (cols * tw, rows * th), (30, 30, 30))
    g = ImageDraw.Draw(sheet)
    for i, (t, im) in enumerate(keep[s:s + per_sheet]):
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        g.rectangle((x, y, x + 40, y + 13), fill=(0, 0, 0))
        g.text((x + 2, y + 1), '%d:%02d' % (int(t) // 60, int(t) % 60), fill=(255, 255, 0))
    p = os.path.join(out, '%s_grid_%02d.jpg' % (vid, s // per_sheet))
    sheet.save(p, quality=90)
    print(p, sheet.size)
