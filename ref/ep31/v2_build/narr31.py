# -*- coding: utf-8 -*-
"""31本目④'：台本の §4 から、章の見出し・カット番号・語りと聞き役の行だけを抜き出す（30本目の narr30.py を写した＝中身は同じ）。
通し読み（耳で聞く順）と、最後の点検の係に渡す「語りだけの写し」に使う。画の欄と出典の欄は入れない。台本は読むだけ。

  python -P ref/ep31/v2_build/narr31.py ref/ep31/daihon_v2.md ref/ep31/src/agents/wf31b/narr_v2.txt
  python -P ref/ep31/v2_build/narr31.py ref/ep31/daihon_v2.md ref/ep31/src/agents/wf31b/cuts_v2.txt --full   # 画と出典の欄も
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')


def main(src, dst, full=False):
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
            out.append(ln if full else '[' + CUT.match(ln).group(1) + ']')
            n += 1
        elif ln.startswith('>'):
            out.append(ln)
    open(dst, 'w', encoding='utf-8', newline='\n').write('\n'.join(out).strip() + '\n')
    print(f'カット {n}・行 {sum(1 for x in out if x.startswith(">"))} → {dst}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], '--full' in sys.argv[3:])
