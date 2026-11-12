# -*- coding: utf-8 -*-
"""33本目④'：決めたカットだけを出す（台本の全文を親の文脈に入れないため＝ルール 4'-10・32本目 cut32.py を写した）。読むだけ。

  python -P ref/ep33/v2_build/cut33.py [--v2] [--pic] [--src] c408 c410-c418 ...

既定＝語りと聞き役の行だけ。--pic＝画の欄も・--src＝出典の欄も（見出しの行を丸ごと）。--v2＝daihon_v2.md を読む。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
CUT = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*')


def blocks(path):
    out, cur = {}, None
    order = []
    for l in open(path, encoding='utf-8').read().replace('\r\n', '\n').split('\n'):
        m = CUT.match(l)
        if m:
            cur = m.group(1)
            out[cur] = [l]
            order.append(cur)
            continue
        if l.startswith('#') or l.strip() == '---':
            cur = None
            continue
        if cur and l.startswith('>'):
            out[cur].append(l)
    return out, order


def expand(args, order):
    want = []
    for a in args:
        if '-' in a:
            x, y = a.split('-', 1)
            if x in order and y in order:
                want += order[order.index(x):order.index(y) + 1]
        elif a in order:
            want.append(a)
    return want


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    path = os.path.join(EP, 'daihon_v2.md' if '--v2' in sys.argv else 'daihon_v1.md')
    b, order = blocks(path)
    for c in expand(args, order):
        hd = b[c][0]
        if '--src' in sys.argv:
            print(hd)
        elif '--pic' in sys.argv:
            parts = hd.split('／')
            print('%s ／%s' % (parts[0].strip(), parts[1] if len(parts) > 1 else ''))
        else:
            print(hd.split('／')[0].strip())
        for l in b[c][1:]:
            print(l)
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
