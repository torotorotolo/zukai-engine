# -*- coding: utf-8 -*-
"""24本目②：一覧（TSV＝label<TAB>src）から 640px の見本帳（2列×3行＝1280×1530）を作る。src は URL か手元の道。
sheet_cmx.py と同じ寸法（1コマ 640×480・札 30px）＝読み手に縮まずに届く（長辺 1280 ≤ 1568）。
使い方: sheet_list.py <list.tsv> <名前の頭>   → ref/ep24/src/sheets/<頭>_N.png と .txt（札の一覧）"""
import csv, hashlib, os, sys, time, urllib.request
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\konar\Desktop\zukai-engine\ref\ep24\src\sheets"
UA = 'zukai-engine/1.0 (ep24 material research)'
CW, CH, LAB = 640, 480, 30
FONT = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 18)


def local(src):
    if not src.startswith('http'):
        return src
    os.makedirs(os.path.join(OUT, 'thumbs'), exist_ok=True)
    p = os.path.join(OUT, 'thumbs', hashlib.md5(src.encode()).hexdigest()[:12] + os.path.splitext(src.split('?')[0])[1][:5])
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return p
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(src, headers={'User-Agent': UA}), timeout=90) as r:
                open(p, 'wb').write(r.read())
            time.sleep(2)
            return p
        except Exception as e:
            last = e
            time.sleep(6 * (i + 1))
    raise last


def main():
    lst, head = sys.argv[1], sys.argv[2]
    rows = [r for r in csv.reader(open(lst, encoding='utf-8'), delimiter='\t') if r and not r[0].startswith('#')]
    os.makedirs(OUT, exist_ok=True)
    for s in range(0, len(rows), 6):
        grp = rows[s:s + 6]
        sheet = Image.new('RGB', (CW * 2 + 10, (CH + LAB) * 3), (40, 40, 40))
        d = ImageDraw.Draw(sheet)
        meta = []
        for k, (label, src) in enumerate(grp):
            im = Image.open(local(src)).convert('RGB')
            w0, h0 = im.size
            im.thumbnail((CW, CH))
            x, y = (k % 2) * (CW + 10), (k // 2) * (CH + LAB)
            sheet.paste(im, (x + (CW - im.width) // 2, y + LAB + (CH - im.height) // 2))
            lab = f"#{s + k + 1:02d} {w0}x{h0} {label}"[:62]
            d.text((x + 4, y + 4), lab, fill=(255, 230, 80), font=FONT)
            meta.append(f"#{s + k + 1:02d}\t{w0}x{h0}\t{label}\t{src}")
        out = os.path.join(OUT, f'{head}_{s // 6 + 1}.png')
        sheet.save(out)
        open(out + '.txt', 'w', encoding='utf-8').write('\n'.join(meta))
        print(out, len(grp))


if __name__ == '__main__':
    main()
