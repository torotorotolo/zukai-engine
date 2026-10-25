# -*- coding: utf-8 -*-
"""25本目 映像方針：見た画像を機械で記録する（1チャット40枚まで＝数えを手でしない）。
  python ref/ep25/eizou_build/seen25.py add <チャット番号> <画像> "<何を見たか>" [<画像> "<何>" ...]
  python ref/ep25/eizou_build/seen25.py count [<チャット番号>]
記録＝eizou_build/seen25.tsv（時刻・チャット・ファイル名・md5・大きさ・何）。画像そのものは git の外（scratchpad）。
"""
import hashlib
import os
import sys
import time

from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seen25.tsv')


def add(chat, pairs):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        if new:
            f.write('time\tchat\tfile\tmd5\tsize\twhat\n')
        for path, what in pairs:
            md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
            w, h = Image.open(path).size
            f.write('%s\t%s\t%s\t%s\t%dx%d\t%s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), chat, os.path.basename(path), md5, w, h, what))
    count(chat)


def count(chat=None):
    if not os.path.exists(LOG):
        print('0 枚')
        return 0
    rows = [ln.rstrip('\n').split('\t') for ln in open(LOG, encoding='utf-8') if not ln.startswith('time\t')]
    n = sum(1 for r in rows if chat is None or r[1] == str(chat))
    print('チャット%s で見た画像 %d 枚／40' % (chat if chat is not None else '（全部）', n))
    return n


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'add':
        add(a[1], list(zip(a[2::2], a[3::2])))
    else:
        count(a[1] if len(a) > 1 else None)
