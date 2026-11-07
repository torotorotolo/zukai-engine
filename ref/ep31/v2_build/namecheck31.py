# -*- coding: utf-8 -*-
"""31本目：書かない名前の網（git の外の src/names_private.txt の語）を、台本と道具のファイルに全部当てる（ep30/v2_build/namecheck30.py を写した）。
名前そのものは出さない（当たった数とファイルと行の番号だけ）。リポは公開＝commit の前に回す。

  python -P ref/ep31/v2_build/namecheck31.py ref/themes/ledger.json ref/ep31/*.py ref/ep31/v2_build/*.py ...
終了コード 0=0件 / 1=当たった / 2=網のファイルが無い（fail closed）
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = os.path.join(os.path.dirname(HERE), 'src', 'names_private.txt')
# Commons の撮影者の網＝映像方針で作る。① の時点では無い＝あれば足す
NAMES_COMMONS = os.path.join(os.path.dirname(HERE), 'src', 'names_commons.txt')


def main(files):
    if not os.path.exists(NAMES):
        print('🔴 網のファイルが無い＝止める:', NAMES)
        return 2
    nets = [NAMES] + ([NAMES_COMMONS] if os.path.exists(NAMES_COMMONS) else [])
    print('網＝%s' % '・'.join(os.path.basename(p) for p in nets))
    words = [ln.strip() for p in nets for ln in open(p, encoding='utf-8') if ln.strip() and not ln.startswith('#')]
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
