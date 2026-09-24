# -*- coding: utf-8 -*-
"""15本目②：cday15 の「空でない」85点から、機種の下位カテゴリに入っている点を外して シートを作り直す（時刻順・2列×3行・640px）。
ラベル＝E番号（cd15/index.tsv と同じ）・現地時刻（JST−16h）。
python cday15b.py <cday15.py の出力フォルダ>"""
import datetime, json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

D = sys.argv[1]
rows = json.load(open(r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/commons_ep15.json', encoding='utf-8'))
cats = {}
for r in rows:
    m = re.search(r'\((\d{8,})\)', r['title'])
    if m:
        cats.setdefault(m.group(1), set()).add(r['cat'][9:])
idx = [l.rstrip('\n').split('\t') for l in open(os.path.join(D, 'index.tsv'), encoding='utf-8')]
SUB = ('Tigercat', 'T-6', 'Patriots', 'Firefly', 'Precious Metal', 'Thunderbirds', 'Fw 190')
keep = [e for e in idx if not any(s in c for c in cats.get(e[1], set()) for s in SUB)]
print('残す', len(keep), '／外す', len(idx) - len(keep))
font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 17)
TW, TH = 640, 430
with open(os.path.join(D, 'keep.tsv'), 'w', encoding='utf-8') as f:
    for e in keep:
        f.write('\t'.join(e) + '\n')
for k in range(0, len(keep), 6):
    sheet = Image.new('RGB', (TW * 2, (TH + 26) * 3), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    for j, e in enumerate(keep[k:k + 6]):
        im = Image.open(os.path.join(D, e[1] + '.jpg')).convert('RGB')
        im.thumbnail((TW, TH))
        x, y = (j % 2) * TW, (j // 2) * (TH + 26)
        sheet.paste(im, (x + (TW - im.width) // 2, y + 26))
        t = datetime.datetime.strptime(e[2], '%Y-%m-%d %H:%M') - datetime.timedelta(hours=16)
        d.text((x + 4, y + 2), '%s %s 現地%s %s' % (e[0], e[1], t.strftime('%H:%M'), e[3]), fill=(255, 255, 0), font=font)
    sheet.save(os.path.join(D, 'k_%02d.jpg' % (k // 6 + 1)), quality=85)
print('sheets', (len(keep) + 5) // 6)
