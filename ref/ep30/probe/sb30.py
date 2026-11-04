# -*- coding: utf-8 -*-
"""30本目 ②：YouTube のストーリーボード（シーク用の縮小画像 320×180）を断片の URL から1枚ずつ取り、
ショットの変わり目だけを残した見本帳を作る（ルール §2-33＝手元の yt-dlp は本体が 403・mhtml の束は壊れる）。

  python -I -X utf8 sb30.py <動画id> <yt-dlp -j の json> <出力フォルダ> [しきい値=14] [1枚の列=4] [1枚の行=3]
出力＝<出力>/<id>_sb/（断片）・<出力>/<id>_sheet_NN.jpg（時刻の札つき）・<id>_shots.tsv（時刻と差）
入力は信用しないデータ＝画像として描くだけ。
"""
import json
import os
import sys
import time
import urllib.request

from PIL import Image, ImageDraw, ImageChops, ImageStat

sys.stdout.reconfigure(encoding='utf-8')
vid, meta, out = sys.argv[1], sys.argv[2], sys.argv[3]
th = float(sys.argv[4]) if len(sys.argv) > 4 else 14.0
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
rows = int(sys.argv[6]) if len(sys.argv) > 6 else 3
d = json.load(open(meta, encoding='utf-8'))
sb = [f for f in d['formats'] if f['format_id'] == 'sb0'][0]
W, H, R, C = sb['width'], sb['height'], sb['rows'], sb['columns']
frag_dir = os.path.join(out, vid + '_sb')
os.makedirs(frag_dir, exist_ok=True)
thumbs = []  # (秒, 画像)
t0 = 0.0
for n, fr in enumerate(sb['fragments']):
    p = os.path.join(frag_dir, 'f%03d.jpg' % n)
    if not os.path.exists(p):
        with urllib.request.urlopen(fr['url'], timeout=30) as r:
            open(p, 'wb').write(r.read())
        time.sleep(0.5)
    im = Image.open(p).convert('RGB')
    per = fr['duration'] / (R * C)
    k = 0
    for y in range(R):
        for x in range(C):
            box = (x * W, y * H, (x + 1) * W, (y + 1) * H)
            if box[2] <= im.width and box[3] <= im.height:
                thumbs.append((t0 + per * k, im.crop(box)))
            k += 1
    t0 += fr['duration']
keep = []
last = None
for t, im in thumbs:
    if last is None:
        keep.append((t, im, 999.0))
        last = im
        continue
    diff = sum(ImageStat.Stat(ImageChops.difference(im, last).convert('L')).mean)
    if diff >= th:
        keep.append((t, im, diff))
        last = im
print('縮小画像 %d → 残す %d（しきい値 %.1f）・尺 %.0f秒' % (len(thumbs), len(keep), th, d.get('duration') or 0))
with open(os.path.join(out, vid + '_shots.tsv'), 'w', encoding='utf-8') as f:
    for t, _, df in keep:
        f.write('%.1f\t%.1f\n' % (t, df))
per_sheet = cols * rows
for s in range(0, len(keep), per_sheet):
    sheet = Image.new('RGB', (cols * W, rows * H), (30, 30, 30))
    g = ImageDraw.Draw(sheet)
    for i, (t, im, _) in enumerate(keep[s:s + per_sheet]):
        x, y = (i % cols) * W, (i // cols) * H
        sheet.paste(im, (x, y))
        g.rectangle((x, y, x + 62, y + 14), fill=(0, 0, 0))
        g.text((x + 3, y + 1), '%d:%02d' % (int(t) // 60, int(t) % 60), fill=(255, 255, 0))
    p = os.path.join(out, '%s_sheet_%02d.jpg' % (vid, s // per_sheet))
    sheet.save(p, quality=88)
    print(p, sheet.size)
