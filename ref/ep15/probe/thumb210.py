# -*- coding: utf-8 -*-
"""15本目②：サムネ候補（継承なし＝切ってよいものだけ）を 16:9 に切り、横210px に縮めて並べる（ルール B5-3）。"""
import io, json, re, sys, time, urllib.request
from PIL import Image, ImageDraw

OUT = sys.argv[1]
UA = 'zukai-engine-research/1.0 (ep15 materials survey)'
rows = json.load(open(r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/commons_ep15.json', encoding='utf-8'))
# (題名の型, 切る窓＝縮小画像の幅・高さに対する割合 x0,y0,x1 ／ 高さは 16:9 で決める)
# ⚠️ 09-24 1回目は窓を 640px の画素で書いたが、thumburl は 960px で返った＝窓がずれた。割合で書く
CANDS = [
    (r'GallopingGhostLocknut', (0.0, 0.05, 1.0)),       # T1 NTSB のロックナット（PD）
    (r'^File:Galloping Ghost\.jpg', (0.06, 0.19, 0.73)),  # T2 2010年の事故機の機首（CC BY 2.0・右の人を外す）
    (r'GallopingGhost 2010-09-18', (0.25, 0.28, 1.0)),    # T3 2010年の事故機の横（CC BY 2.0・手前の人を外す）
]
tiles = []
for pat, (x0, y0, x1) in CANDS:
    r = [r for r in rows if re.search(pat, r['title'])][0]
    data = urllib.request.urlopen(urllib.request.Request(r['thumb'], headers={'User-Agent': UA}), timeout=60).read()
    im = Image.open(io.BytesIO(data)).convert('RGB')
    x0, y0, x1 = round(x0 * im.width), round(y0 * im.height), round(x1 * im.width)
    w = x1 - x0
    h = round(w * 9 / 16)
    y0 = min(y0, max(0, im.height - h))
    crop = im.crop((x0, y0, x1, y0 + h)).resize((210, 118), Image.LANCZOS)
    tiles.append(crop)
    print(r['title'][5:60], im.size, '→ crop', (x0, y0, x1, y0 + h))
    time.sleep(2)
strip = Image.new('RGB', (210 * len(tiles) + 10 * (len(tiles) - 1), 118), (255, 255, 255))
for i, t in enumerate(tiles):
    strip.paste(t, (i * 220, 0))
strip.save(OUT)
print('wrote', OUT, strip.size)
