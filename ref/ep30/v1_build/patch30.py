# -*- coding: utf-8 -*-
"""30本目 ④：直しの表（JSON＝[[元の文, 新しい文], ...]）を台本に当てる（ep17 の patch_review.py の考え＝元の文がちょうど1回なければ全部止める）。

  python ref/ep30/v1_build/patch30.py ref/ep30/daihon_v1.md <表.json>

1件でも当たらなければ1字も書かない。新しい文がもう入っていて元の文が無い行は「当て済み」として飛ばす（2回目の二重当てを止める）。
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')


def main(md, tbl):
    text = open(md, encoding='utf-8', newline='').read()
    rows = json.load(open(tbl, encoding='utf-8'))
    bad = []
    done = 0
    for i, (old, new) in enumerate(rows, 1):
        n = text.count(old)
        if n == 1:
            text = text.replace(old, new)
            done += 1
        elif n == 0 and new and text.count(new) >= 1:
            print('当て済み #%d: %s' % (i, new[:30]))
        else:
            bad.append('#%d 元の文が %d回: %s' % (i, n, old[:50]))
    if bad:
        print('🔴 止めた（1字も書いていない）')
        for b in bad:
            print(' ', b)
        return 1
    with open(md, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    print('当てた %d件 / 表 %d件' % (done, len(rows)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
