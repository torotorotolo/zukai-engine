# -*- coding: utf-8 -*-
"""23本目 映像方針：見るための画像を作り、見た枚を seen23.tsv に機械で記録する（2026-10-18・映像方針チャット）。

  python ref/ep23/eizou_build/helpers/sheet23.py sheet <出力.png> <メモ> <画像1> [<画像2> ...]   # 2列のシート（1枚の幅 --w 既定 800px・下に札）
  python ref/ep23/eizou_build/helpers/sheet23.py crop  <出力.png> <メモ> <画像> x0 y0 x1 y1         # 原寸の切り出し（拡大しない）
  python ref/ep23/eizou_build/helpers/sheet23.py one   <出力.png> <メモ> <画像>                       # 1枚を原寸のまま（CMYK は RGB に）
  python ref/ep23/eizou_build/helpers/sheet23.py count                                                # いままでに見た枚数

出力の画像は scratchpad など git の外へ。seen23.tsv（eizou_build/）に「番号・時刻・出力・メモ・元の画像」を1行足す＝見た枚の数はこの行の数。
"""
import datetime
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEN = os.path.join(HERE, 'seen23.tsv')


def _font(size):
    for p in (r'C:\Windows\Fonts\meiryo.ttc', r'C:\Windows\Fonts\msgothic.ttc', r'C:\Windows\Fonts\arial.ttf'):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()


def _rgb(path):
    im = Image.open(path)
    im.load()
    return im.convert('RGB') if im.mode != 'RGB' else im


def _log(out, note, srcs):
    n = 0
    if os.path.exists(SEEN):
        n = sum(1 for ln in open(SEEN, encoding='utf-8') if ln.strip() and not ln.startswith('#'))
    else:
        with open(SEEN, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# 23本目 映像方針：見た画像（sheet23.py が1枚ごとに1行足す・手で直さない）。番号・時刻・出力・メモ・元の画像\n')
    n += 1
    with open(SEEN, 'a', encoding='utf-8', newline='\n') as f:
        f.write('%d\t%s\t%s\t%s\t%s\n' % (n, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), os.path.basename(out), note,
                                         ' '.join(os.path.basename(s) for s in srcs)))
    print('見た枚 %d（上限40）→ %s' % (n, out))


def sheet(out, note, paths, w=800, cols=2):
    tiles = []
    f = _font(20)
    for p in paths:
        im = _rgb(p)
        W0, H0 = im.size
        if W0 >= H0:
            t = im.resize((w, round(H0 * w / W0)), Image.LANCZOS)
        else:
            h = round(w * 0.75)
            t = im.resize((round(W0 * h / H0), h), Image.LANCZOS)
        tiles.append((t, '%s  %dx%d' % (os.path.basename(p), W0, H0)))
    rows = [tiles[i:i + cols] for i in range(0, len(tiles), cols)]
    lab = 30
    H = sum(max(t.size[1] for t, _ in r) + lab for r in rows)
    canvas = Image.new('RGB', (w * cols + 10 * (cols - 1), H), (40, 40, 40))
    d = ImageDraw.Draw(canvas)
    y = 0
    for r in rows:
        rh = max(t.size[1] for t, _ in r)
        for i, (t, s) in enumerate(r):
            x = i * (w + 10)
            canvas.paste(t, (x + (w - t.size[0]) // 2, y))
            d.text((x + 4, y + rh + 4), s, fill=(255, 255, 0), font=f)
        y += rh + lab
    canvas.save(out)
    _log(out, note, paths)


def crop(out, note, path, box):
    im = _rgb(path)
    im.crop(tuple(int(v) for v in box)).save(out)
    _log(out, note, [path])


def one(out, note, path):
    _rgb(path).save(out)
    _log(out, note, [path])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == 'count':
        n = sum(1 for ln in open(SEEN, encoding='utf-8') if ln.strip() and not ln.startswith('#')) if os.path.exists(SEEN) else 0
        print('見た枚 %d（上限40）' % n)
    elif a[0] == 'sheet':
        w = 800
        if '--w' in a:
            i = a.index('--w')
            w = int(a[i + 1])
            a = a[:i] + a[i + 2:]
        sheet(a[1], a[2], a[3:], w=w)
    elif a[0] == 'crop':
        crop(a[1], a[2], a[3], a[4:8])
    elif a[0] == 'one':
        one(a[1], a[2], a[3])
    else:
        sys.exit(__doc__)
