# -*- coding: utf-8 -*-
"""26本目 映像方針（2026-10-27・チャット5）：見た画像を1枚ずつ eizou_build/seen26e.tsv に残す（md5・大きさ・何のために）。
probe/seen26.py（②③）を写して、台帳をこのチャットの分だけに分けた（②③ の22枚と混ぜない＝1チャット40枚の数え）。

  python -P ref/ep26/eizou_build/seen26e.py <画像> "<何のために>"   → 通しの番号と合計（40枚まで）
"""
import datetime
import hashlib
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'seen26e.tsv')
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
LIMIT = 40


def main():
    path, why = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ''
    with open(path, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    w, h = Image.open(path).size
    n = 0
    if os.path.exists(LOG):
        with open(LOG, encoding='utf-8') as f:
            n = sum(1 for line in f if line.strip() and not line.startswith('n\t'))
    else:
        with open(LOG, 'w', encoding='utf-8', newline='\n') as f:
            f.write('n\twhen\tpath\tmd5\tsize\twhy\n')
    n += 1
    rel = os.path.relpath(os.path.abspath(path), REPO).replace('\\', '/')
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        f.write(f'{n}\t{datetime.datetime.now():%Y-%m-%d %H:%M}\t{rel}\t{md5}\t{w}x{h}\t{why}\n')
    print(f'seen {n}/{LIMIT}  {w}x{h}  {os.path.basename(path)}')
    return 2 if n > LIMIT else 0


if __name__ == '__main__':
    sys.exit(main())
