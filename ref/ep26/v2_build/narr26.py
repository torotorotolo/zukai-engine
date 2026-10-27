# -*- coding: utf-8 -*-
"""26本目④'：台本の §4 から、章の見出し・カット番号・語りと聞き役の行だけを抜き出す（通し読みの係が「耳で聞く順」に読むため・
画の欄と出典の欄は入れない）。第1版は読むだけ。

  python -P ref/ep26/v2_build/narr26.py ref/ep26/daihon_v1.md ref/ep26/v2_build/narr_v1.txt
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')


def main(src, dst):
    on, out, n = False, [], 0
    for ln in open(src, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        if ln.startswith('### '):
            out.append('')
            out.append(ln)
        elif CUT.match(ln):
            out.append('[' + CUT.match(ln).group(1) + ']')
            n += 1
        elif ln.startswith('>'):
            out.append(ln)
    open(dst, 'w', encoding='utf-8', newline='\n').write('\n'.join(out).strip() + '\n')
    print(f'カット {n}・行 {sum(1 for x in out if x.startswith(">"))} → {dst}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
