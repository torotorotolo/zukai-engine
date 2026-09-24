# -*- coding: utf-8 -*-
"""15本目②：事故の日（現地 2011-09-16）の tataquax の写真を 960px で落とし、空だけの写真を機械で分ける。
カメラ時計は日本時間のまま（現地＝JST−16時間・さらに数分進み）と見ている＝窓は JST 2011-09-16 23:00〜09-17 08:30。
出力：<出力フォルダ>/<id>.jpg・sky.tsv・sheet_NN.jpg（空でないものだけ・時刻順・2列×3行・640px）
python cday15.py <出力フォルダ（scratchpad の中に。🔴 リポの中に画像を置かない）>"""
import io, json, os, re, sys, time, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageStat

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
UA = 'zukai-engine-research/1.0 (ep15 materials survey; contact via github torotorotolo)'
rows = json.load(open(r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/commons_ep15.json', encoding='utf-8'))
SEEN = {'6361173745', '6361174209', '6450673359', '6361174323', '6452065605', '6248416879', '6361174465', '6450673505', '6452065839'}
sel = [r for r in rows if (r.get('artist') or '').startswith('tataquax') and '2011-09-16 23' <= r.get('date_raw', '') < '2011-09-17 08:3']
sel.sort(key=lambda r: r['date_raw'])
print('事故の日', len(sel), '点（うち見たもの', sum(1 for r in sel if any(s in r['title'] for s in SEEN)), '）', flush=True)


def fid(r):
    m = re.search(r'\((\d{8,})\)', r['title'])
    return m.group(1) if m else re.sub(r'\W+', '_', r['title'][5:40])


def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return True
    for i in range(6):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()
            open(path, 'wb').write(data)
            time.sleep(1.2)
            return True
        except Exception as e:
            wait = 30 + 15 * i
            print('  retry', i, type(e).__name__, getattr(e, 'code', ''), 'wait', wait, flush=True)
            time.sleep(wait)
    return False


def skyness(im):
    """16×16 のブロックで、明るさのばらつきが小さい（空・曇天）ブロックの割合。"""
    g = im.convert('L').resize((160, 106))
    n = flat = 0
    for y in range(0, 106 - 10, 10):
        for x in range(0, 160, 10):
            st = ImageStat.Stat(g.crop((x, y, x + 10, y + 10)))
            n += 1
            flat += st.stddev[0] < 6.0
    return flat / n


res = []
for r in sel:
    i = fid(r)
    p = os.path.join(OUT, i + '.jpg')
    ok = get(r['thumb'], p)
    if not ok:
        print('  取れず', r['title'], flush=True)
        res.append((r, i, None))
        continue
    im = Image.open(p).convert('RGB')
    res.append((r, i, skyness(im)))

with open(os.path.join(OUT, 'sky.tsv'), 'w', encoding='utf-8') as f:
    for r, i, s in res:
        f.write('%s\t%s\t%sx%s\t%s\t%s\n' % (i, r['date_raw'][:16], r['w'], r['h'], '' if s is None else '%.2f' % s, 'SEEN' if i in SEEN else ''))
todo = [(r, i, s) for r, i, s in res if s is not None and s < 0.70 and i not in SEEN]
sky = [(r, i, s) for r, i, s in res if s is not None and s >= 0.70 and i not in SEEN]
print('空でない（<0.70）', len(todo), '／空（>=0.70）', len(sky), '／取れず', sum(1 for x in res if x[2] is None), flush=True)

font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', 17)
TW, TH = 640, 430
for k in range(0, len(todo), 6):
    sheet = Image.new('RGB', (TW * 2, (TH + 26) * 3), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    for j, (r, i, s) in enumerate(todo[k:k + 6]):
        im = Image.open(os.path.join(OUT, i + '.jpg')).convert('RGB')
        im.thumbnail((TW, TH))
        x, y = (j % 2) * TW, (j // 2) * (TH + 26)
        sheet.paste(im, (x + (TW - im.width) // 2, y + 26))
        d.text((x + 4, y + 2), 'E%02d %s JST %s %sx%s sky%.2f' % (k + j + 1, i, r['date_raw'][11:16], r['w'], r['h'], s), fill=(255, 255, 0), font=font)
    sheet.save(os.path.join(OUT, 'sheet_%02d.jpg' % (k // 6 + 1)), quality=85)
with open(os.path.join(OUT, 'index.tsv'), 'w', encoding='utf-8') as f:
    for n, (r, i, s) in enumerate(todo, 1):
        f.write('E%02d\t%s\t%s\t%sx%s\t%.2f\t%s\n' % (n, i, r['date_raw'][:16], r['w'], r['h'], s, r['title']))
print('sheets', (len(todo) + 5) // 6)
