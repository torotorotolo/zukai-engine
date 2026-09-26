# -*- coding: utf-8 -*-
"""Commons の台帳（cmx.py files の TSV）の行番号で 640px の見本帳（2列×3行）を作る。
使い方: sheet_cmx.py <tsv> <名前の頭> <行番号...>   （行番号＝見出しを除いた1始まり）"""
import csv, os, sys, time, urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
UA = 'zukai-engine/1.0 (ep17 material research)'
CW, CH, LAB = 640, 480, 30
FONT = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 18)

def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r:
                open(path, 'wb').write(r.read())
            time.sleep(4); return
        except Exception as e:
            last = e; time.sleep(6 * (i + 1))
    raise last

tsv, head, nums = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]]
rows = list(csv.DictReader(open(tsv, encoding='utf-8'), delimiter='\t'))
os.makedirs(os.path.join(HERE, 'thumbs'), exist_ok=True)
for s in range(0, len(nums), 6):
    grp = nums[s:s + 6]
    sheet = Image.new('RGB', (CW * 2 + 10, (CH + LAB) * 3), (40, 40, 40))
    d = ImageDraw.Draw(sheet); meta = []
    for k, n in enumerate(grp):
        r = rows[n - 1]
        p = os.path.join(HERE, 'thumbs', f'{head}_{n:03d}.jpg')
        fetch(r['thumb'] or r['url'], p)
        im = Image.open(p).convert('RGB'); im.thumbnail((CW, CH))
        x, y = (k % 2) * (CW + 10), (k // 2) * (CH + LAB)
        sheet.paste(im, (x + (CW - im.width) // 2, y + LAB + (CH - im.height) // 2))
        lab = f"#{n:02d} {r['w']}x{r['h']} {r['lic'][:12]} {r['dto'][:10]} {r['title'][5:40]}"
        d.text((x + 4, y + 4), lab, fill=(255, 230, 80), font=FONT); meta.append(lab)
    out = os.path.join(HERE, f'{head}_{s // 6 + 1}.png'); sheet.save(out)
    open(out + '.txt', 'w', encoding='utf-8').write('\n'.join(meta)); print(out, len(grp))
