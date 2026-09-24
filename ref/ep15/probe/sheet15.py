# -*- coding: utf-8 -*-
"""15本目②：候補を 640px のシート（2列×3行）にする。Commons の thumburl（640px）を使う。
python sheet15.py <出力フォルダ>  → sheetA.jpg … と index.tsv"""
import io, json, os, re, sys, time, urllib.request
from PIL import Image, ImageDraw, ImageFont

OUTDIR = sys.argv[1]
os.makedirs(OUTDIR, exist_ok=True)
UA = 'zukai-engine-research/1.0 (ep15 materials survey)'
rows = json.load(open(r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/commons_ep15.json', encoding='utf-8'))


def find(pat):
    hit = [r for r in rows if re.search(pat, r['title'])]
    assert len(hit) >= 1, pat
    return hit[0]


SHEETS = {
    'A': ['6361173745', '6361174209', '6450673359', '6361174323', '6452065605', "Jimmy Leeward's Galloping Ghost"],
    'B': ['6248416879', '6361174465', '6450673505', '6452065839', '6452063939', '6452062347'],
    'C': ['P-51n79111side69', 'P-51n79111side70', 'after damage 1970', r'^File:Galloping Ghost\.jpg', 'GallopingGhost 2010-09-18', 'GallopingGhostLocknut'],
    'D': [r'Strega.*N71FT', r'Vintage V-12', 'View west towards Reno Stead', r'Reno Stead Field \(3392833169\)', 'Pylon Racing Seminar by', 'Control Tower during the 2016'],
}
font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 18)
CW, CH, LH = 640, 427, 26
idx = open(os.path.join(OUTDIR, 'index.tsv'), 'w', encoding='utf-8')
for name, pats in SHEETS.items():
    sheet = Image.new('RGB', (CW * 2, (CH + LH) * 3), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for i, pat in enumerate(pats):
        r = find(re.escape(pat) if re.match(r'^\d+$', pat) else pat)
        req = urllib.request.Request(r['thumb'], headers={'User-Agent': UA})
        for k in range(6):
            try:
                data = urllib.request.urlopen(req, timeout=60).read(); break
            except Exception as e:
                print('  retry', k, e, flush=True); time.sleep(15 * (k + 1))
        im = Image.open(io.BytesIO(data)).convert('RGB')
        im.thumbnail((CW, CH))
        x, y = (i % 2) * CW, (i // 2) * (CH + LH)
        sheet.paste(im, (x + (CW - im.width) // 2, y + LH + (CH - im.height) // 2))
        lab = '%s%d %s %sx%s %s' % (name, i + 1, r['date_raw'][:16], r['w'], r['h'], re.sub(r'^File:', '', r['title'])[:34])
        d.text((x + 6, y + 3), lab, fill=(255, 255, 0), font=font)
        idx.write('%s%d\t%s\t%s\t%sx%s\t%s\t%s\n' % (name, i + 1, r['title'], r['date_raw'], r['w'], r['h'], r['lic'], r['artist']))
        time.sleep(2)
    p = os.path.join(OUTDIR, 'sheet%s.jpg' % name)
    sheet.save(p, quality=88)
    print('wrote', p, sheet.size, flush=True)
idx.close()
