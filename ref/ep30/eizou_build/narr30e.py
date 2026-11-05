# -*- coding: utf-8 -*-
"""30本目 映像方針：カットの語りだけを1行ずつ出す（全文は読まない＝要るカットだけ）。

  python -P ref/ep30/eizou_build/narr30e.py c101 c102 ...          名指しのカット
  python -P ref/ep30/eizou_build/narr30e.py --from c301 --to c323   範囲
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.join(os.path.dirname(HERE), 'v2_build', 'narr_v2.txt')


def load():
    cuts, cur = [], None
    for ln in open(NARR, encoding='utf-8'):
        ln = ln.rstrip('\n')
        m = re.match(r'^\[(c[0-9a-c]\d\d|ed\d\d)\]$', ln)
        if m:
            cur = [m.group(1), []]
            cuts.append(cur)
        elif ln.startswith('###'):
            cur = None
        elif cur is not None and ln.strip():
            cur[1].append(ln.strip())
    return cuts


def main():
    a = sys.argv[1:]
    cuts = load()
    if a and a[0] == '--from':
        ids = [c[0] for c in cuts]
        i, j = ids.index(a[1]), ids.index(a[3])
        pick = ids[i:j + 1]
    else:
        pick = a
    d = dict((c[0], c[1]) for c in cuts)
    for cid in pick:
        print('%s %s' % (cid, ' ／ '.join(d.get(cid, ['（無い）']))))


if __name__ == '__main__':
    main()
