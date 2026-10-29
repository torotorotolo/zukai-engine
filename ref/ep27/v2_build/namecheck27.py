# -*- coding: utf-8 -*-
"""27本目④'：書かない名前の網（git の外の src/names_private.txt の語）を、台本と v2_build のファイルに全部当てる。
名前そのものは出さない（当たった数とファイルとカット・行の番号だけ）。リポは公開＝commit の前に回す。

  python -P ref/ep27/v2_build/namecheck27.py ref/ep27/daihon_v2.md ref/ep27/v2_build/*.py ...
終了コード 0=0件 / 1=当たった / 2=網のファイルが無い（fail closed）
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = os.path.join(os.path.dirname(HERE), 'src', 'names_private.txt')


def main(files):
    if not os.path.exists(NAMES):
        print('🔴 網のファイルが無い＝止める:', NAMES)
        return 2
    words = [ln.strip() for ln in open(NAMES, encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    hits = 0
    for f in files:
        try:
            lines = open(f, encoding='utf-8').read().split('\n')
        except (OSError, UnicodeDecodeError) as e:
            print('⚠️ 読めない:', f, e)
            continue
        for i, ln in enumerate(lines, 1):
            for k, w in enumerate(words):
                if w and w in ln:
                    hits += 1
                    print('🔴 %s:%d に網の語 #%d' % (os.path.basename(f), i, k + 1))
    print('名前の網 %d語 × %dファイル → %d件' % (len(words), len(files), hits))
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
