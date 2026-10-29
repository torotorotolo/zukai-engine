# -*- coding: utf-8 -*-
"""27本目 映像方針（2026-10-29・チャット5）：見本帳＝4点を1枚（2×2・1点は幅640×高480の枠に収める＝縮めすぎない）。
札＝記号・権利・撮影日・北浜のヨットハーバーからの距離（geo27.json の座標）。撮影者の名前は出さない。

  python -I ref/ep27/eizou_build/sheet27.py <出力.png> <画像> <画像> <画像> <画像>
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(os.path.dirname(HERE), 'src', 'commons', 'geo27.json')
HARBOR = (33.27823, 131.50798)        # 別府北浜ヨットハーバー（OpenStreetMap・2026-10-29）
CW, CH, BAR = 640, 480, 28


def label(path, geo):
    key = os.path.splitext(os.path.basename(path))[0].split('_')[0]
    g = geo.get(key)
    if not g:
        return key
    try:
        lat, lon = float(g['lat']), float(g['lon'])
        km = math.hypot((lat - HARBOR[0]) * 111.0, (lon - HARBOR[1]) * 111.0 * math.cos(math.radians(lat)))
        dist = '%.2fkm' % km
    except (TypeError, ValueError, KeyError):
        dist = '座標なし'
    return '%s｜%s｜%s｜%sx%s｜港から%s' % (key, g.get('lic') or '?', (g.get('date') or '?')[:16], g['w'], g['h'], dist)


def main():
    out, items = sys.argv[1], sys.argv[2:6]
    geo = json.load(open(GEO, encoding='utf-8')) if os.path.exists(GEO) else {}
    sheet = Image.new('RGB', (CW * 2 + 6, (CH + BAR) * 2 + 6), (255, 0, 255))
    font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 17)
    d = ImageDraw.Draw(sheet)
    for i, p in enumerate(items):
        x0, y0 = (i % 2) * (CW + 6), (i // 2) * (CH + BAR + 6)
        im = Image.open(p).convert('RGB')
        k = min(CW / im.width, CH / im.height)
        im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
        d.rectangle([x0, y0, x0 + CW - 1, y0 + BAR + CH - 1], fill=(0, 0, 0))
        d.text((x0 + 4, y0 + 3), label(p, geo), fill=(255, 255, 0), font=font)
        sheet.paste(im, (x0 + (CW - im.width) // 2, y0 + BAR + (CH - im.height) // 2))
    sheet.save(out)
    print(out, sheet.size)


if __name__ == '__main__':
    main()
