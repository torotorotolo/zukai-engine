# -*- coding: utf-8 -*-
"""通し頁ファイルから頁を引く／語で引く。
  python pg.py 3004 3020-3021        # 頁を出す（空白を詰める）
  python pg.py -g "Crestview" [-w 300] [-r 3000-3099]   # 語で引く（前後 w 字）
"""
import re
import sys

F = 'C:/Users/konar/Desktop/zukai-engine/ref/ep19/src/ep19_pages.txt'
txt = open(F, encoding='utf-8').read()
parts = re.split(r'=== p(\d+) ===\n', txt)
P = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def comp(s):
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n\s*', ' / ', s.strip())
    return s


def rng(a):
    if '-' in a:
        x, y = a.split('-')
        return range(int(x), int(y) + 1)
    return [int(a)]


args = sys.argv[1:]
if args and args[0] == '-g':
    pat = re.compile(args[1], re.I)
    w = 300
    r = None
    if '-w' in args:
        w = int(args[args.index('-w') + 1])
    if '-r' in args:
        r = rng(args[args.index('-r') + 1])
    for n in sorted(P):
        if r is not None and n not in r:
            continue
        s = comp(P[n])
        for m in pat.finditer(s):
            a, b = max(0, m.start() - w), min(len(s), m.end() + w)
            print(f'p{n}: …{s[a:b]}…')
else:
    for a in args:
        for n in rng(a):
            if n in P:
                print(f'=== p{n} === {comp(P[n])}')
