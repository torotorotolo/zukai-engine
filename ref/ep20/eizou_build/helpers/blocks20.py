# -*- coding: utf-8 -*-
"""1ビットの頁から「写真らしい濃い塊」の位置を機械で探す（20本目 映像方針・scratchpad）。

  python blocks20.py <頁.png> [格子px=24] [濃さ=0.18] [最小の面積比=0.01]

頁を格子に区切り、黒の割合が濃さを超えるマスをつないで塊にし、外接の箱を比率（0〜1）で印字する。
文字の行は薄い・写真の網点は濃い、の差を使う（見るのは人。これは当たりを付けるだけ）。
"""
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')


def main(path, g=24, th=0.18, amin=0.01):
    im = Image.open(path).convert('L')
    a = np.asarray(im) < 128
    h, w = a.shape
    gh, gw = h // g, w // g
    d = a[:gh * g, :gw * g].reshape(gh, g, gw, g).mean(axis=(1, 3))
    m = d > th
    seen = np.zeros_like(m)
    boxes = []
    for y in range(gh):
        for x in range(gw):
            if m[y, x] and not seen[y, x]:
                st = [(y, x)]
                seen[y, x] = True
                ys, xs = [], []
                while st:
                    cy, cx = st.pop()
                    ys.append(cy)
                    xs.append(cx)
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < gh and 0 <= nx < gw and m[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                st.append((ny, nx))
                y0, y1, x0, x1 = min(ys), max(ys) + 1, min(xs), max(xs) + 1
                area = (y1 - y0) * (x1 - x0) / (gh * gw)
                if area >= amin:
                    boxes.append((y0 / gh, x0 / gw, y1 / gh, x1 / gw, area, len(ys) / ((y1 - y0) * (x1 - x0))))
    boxes.sort()
    print('%s  %dx%d' % (path, w, h))
    for y0, x0, y1, x1, area, fill in boxes:
        print('  box x0=%.3f y0=%.3f x1=%.3f y1=%.3f  面積%.3f 埋まり%.2f  （%dx%dpx）' % (
            x0, y0, x1, y1, area, fill, (x1 - x0) * w, (y1 - y0) * h))


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args[0], *(int(args[1]),) if len(args) > 1 else (), *(float(v) for v in args[2:4]))
