# -*- coding: utf-8 -*-
"""27本目 映像方針（2026-10-29・チャット5）：見た画像を1枚ずつ ref/ep27/src/seen_log.tsv に足す（②③・④ の行と同じ表・このチャットの分は「映像方針」の印で数える＝1チャット40枚）。

  python -P ref/ep27/eizou_build/seen27.py <画像> "<何のために>"   → このチャットの通しの番号と合計
"""
import hashlib
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
LOG = os.path.join(SRC, 'seen_log.tsv')
TAG = '映像方針'
LIMIT = 40


def main():
    path, why = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ''
    with open(path, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    w, h = Image.open(path).size
    with open(LOG, encoding='utf-8') as f:
        lines = [ln.rstrip('\n').split('\t') for ln in f if ln.strip()]
    n_all = sum(1 for r in lines if r[0] != 'n')
    n_here = sum(1 for r in lines if r[0] != 'n' and len(r) > 2 and r[2].startswith(TAG))
    rel = os.path.relpath(os.path.abspath(path), SRC).replace('\\', '/')
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        f.write('%d\t%s\t%s｜%s｜%dx%d｜md5=%s\n' % (n_all + 1, rel, TAG, why, w, h, md5[:12]))
    print('seen %d/%d（このチャット）  %dx%d  %s' % (n_here + 1, LIMIT, w, h, os.path.basename(path)))
    return 2 if n_here + 1 > LIMIT else 0


if __name__ == '__main__':
    sys.exit(main())
