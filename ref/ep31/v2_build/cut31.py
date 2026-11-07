# -*- coding: utf-8 -*-
"""31本目④'：決めたカットだけを出す（台本の全文を親の文脈に入れないため＝ルール 4'-10・30本目 cut30.py を写した）。読むだけ。

  python -P ref/ep31/v2_build/cut31.py [--v2] [--pic] [--src] c408 c410-c418 ...

既定＝語りと聞き役の行だけ。--pic＝画の欄も・--src＝出典の欄も。--v2＝daihon_v2.md を読む。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
ORDER = '123456789abcd'


def key(c):
    return (ORDER.index(c[1]), int(c[2:]))


def load(path):
    out, cur, on = {}, None, False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        m = CUT.match(ln)
        if m:
            cur = m.group(1)
            out[cur] = [ln]
        elif ln.startswith('---') or ln.startswith('### '):
            cur = None
        elif cur and ln.strip():
            out[cur].append(ln)
    return out


def main(a):
    v2 = '--v2' in a
    pic, src = '--pic' in a, '--src' in a
    cs = load(os.path.join(EP, 'daihon_v2.md' if v2 else 'daihon_v1.md'))
    want = []
    order = sorted(cs, key=key)
    for x in a:
        if x.startswith('--'):
            continue
        if '-' in x:
            p, q = x.split('-')
            i, j = order.index(p), order.index(q)
            want += order[i:j + 1]
        else:
            want.append(x)
    for c in want:
        if c not in cs:
            print('🔴 無いカット', c)
            continue
        head = cs[c][0].split(' ／ ')
        mark = ' 🔧' if '🔧' in head[0] else ''
        print('[%s%s]' % (c, mark))
        if pic and len(head) > 1:
            print('  画: ' + head[1])
        for ln in cs[c][1:]:
            print(ln)
        if src and len(head) > 2:
            print('  源: ' + head[2])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
