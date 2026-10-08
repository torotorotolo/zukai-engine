# -*- coding: utf-8 -*-
"""見本帳（2列×3行・1コマ640px）を組む・見た画像を記録する（20本目 映像方針・scratchpad）。

  python sheet20.py frames <コマのフォルダ> <最初の秒> <出力の頭> <秒,秒,…|a-b,…>
      コマのフォルダの sNNN.png（NNN＝最初の秒からの番号）を、指定の秒だけ並べる。札は「mm:ss（秒）」
  python sheet20.py files <出力の頭> <ファイル>=<札> …         任意の画像を並べる（長辺640に収める）
  python sheet20.py seen <画像> <何を見たか>                     見た画像を seen20.tsv に足し、通し番号を印字

1枚の大きさ＝1280×(3×(360+28))。札は各コマの上の黒い帯に白字。
"""
import csv
import datetime
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SEEN = os.path.join(HERE, 'seen20.tsv')
CW, CH, BAR = 640, 360, 28
FONT = None
for f in ('C:/Windows/Fonts/meiryo.ttc', 'C:/Windows/Fonts/msgothic.ttc', 'C:/Windows/Fonts/arial.ttf'):
    if os.path.exists(f):
        FONT = ImageFont.truetype(f, 20)
        break


def parse_secs(spec):
    out = []
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-')
            out += list(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def build(items, head):
    pages = [items[i:i + 6] for i in range(0, len(items), 6)]
    outs = []
    for k, page in enumerate(pages, 1):
        sheet = Image.new('RGB', (CW * 2, (CH + BAR) * 3), (40, 40, 40))
        d = ImageDraw.Draw(sheet)
        for j, (path, label) in enumerate(page):
            x, y = (j % 2) * CW, (j // 2) * (CH + BAR)
            im = Image.open(path).convert('RGB')
            s = min(CW / im.width, CH / im.height)
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
            sheet.paste(im, (x + (CW - im.width) // 2, y + BAR + (CH - im.height) // 2))
            d.rectangle([x, y, x + CW - 1, y + BAR - 1], fill=(0, 0, 0))
            d.text((x + 6, y + 3), label, fill=(255, 255, 255), font=FONT)
        out = '%s_%02d.png' % (head, k)
        sheet.save(out)
        outs.append(out)
        print(out, ' / '.join(lbl for _, lbl in page))
    return outs


def main():
    cmd = sys.argv[1]
    if cmd == 'frames':
        folder, t0, head, spec = sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
        items = []
        for t in parse_secs(spec):
            p = os.path.join(folder, 's%03d.png' % (t - t0))
            if not os.path.exists(p):
                raise SystemExit('🔴 コマが無い：%s（%d秒）' % (p, t))
            items.append((p, '%02d:%02d（%d）' % (t // 60, t % 60, t)))
        build(items, head)
    elif cmd == 'files':
        head = sys.argv[2]
        items = [tuple(a.split('=', 1)) for a in sys.argv[3:]]
        build(items, head)
    elif cmd == 'seen':
        n = 0
        if os.path.exists(SEEN):
            n = sum(1 for _ in open(SEEN, encoding='utf-8'))
        with open(SEEN, 'a', encoding='utf-8', newline='') as f:
            csv.writer(f, delimiter='\t').writerow(
                [n + 1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), os.path.basename(sys.argv[2]), sys.argv[3]])
        print('見た画像 %d 枚目（上限40）：%s' % (n + 1, os.path.basename(sys.argv[2])))


if __name__ == '__main__':
    main()
