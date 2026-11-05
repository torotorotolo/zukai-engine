# -*- coding: utf-8 -*-
"""30本目 映像方針（2026-11-05・チャット5）：見た画像を1枚ずつ ref/ep30/src/seen_log.tsv に足し、このチャットの枚数を出す（上限40・手で数えない）。

  python -P ref/ep30/eizou_build/seen30e.py "<何のために>" <画像 または 画面写しの名前> ...
"""
import datetime
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(os.path.dirname(HERE), 'src', 'seen_log.tsv')
TAG = '映像方針'
LIMIT = 40


def main():
    why, items = sys.argv[1], sys.argv[2:]
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        for p in items:
            f.write('\t'.join([datetime.datetime.now().isoformat(timespec='seconds'), '%s｜%s' % (TAG, why), os.path.basename(p)]) + '\n')
    with open(LOG, encoding='utf-8') as f:
        n = sum(1 for ln in f if '\t%s｜' % TAG in ln)
    print('このチャット %d／%d 枚' % (n, LIMIT))
    return 2 if n > LIMIT else 0


if __name__ == '__main__':
    sys.exit(main())
