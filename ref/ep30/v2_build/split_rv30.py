# -*- coding: utf-8 -*-
"""30本目④'：別の目（当て直しの係）に渡す写しを書く（git の外の src/agents/wf30c/）。

  python -P ref/ep30/v2_build/split_rv30.py

出力＝rv_R1〜R4.txt（対照表 diff_v1_v2.md を受け持ちで割ったもの）・rv_sec.txt（§ の差し替え）・narr_v2.txt・cuts_v2.txt（第2版の語りの通しと全カット）
受け持ち＝R1 c1〜c4／R2 c5・c6・ca／R3 c7〜c9／R4 cb・cc と §
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents', 'wf30c')
GROUP = {'c1': 'R1', 'c2': 'R1', 'c3': 'R1', 'c4': 'R1', 'c5': 'R2', 'c6': 'R2', 'ca': 'R2', 'c7': 'R3', 'c8': 'R3', 'c9': 'R3', 'cb': 'R4', 'cc': 'R4'}
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*( 🔧)?')


def main():
    d = open(os.path.join(HERE, 'diff_v1_v2.md'), encoding='utf-8').read()
    secs = re.split(r'^## ', d, flags=re.M)[1:]
    out = {k: [] for k in ('R1', 'R2', 'R3', 'R4')}
    n = 0
    for s in secs:
        c = s.split('\n', 1)[0].strip()
        g = GROUP.get(c[:2])
        if g:
            out[g].append('## ' + s)
            n += 1
    for g, xs in out.items():
        open(os.path.join(AG, 'rv_%s.txt' % g), 'w', encoding='utf-8', newline='\n').write(''.join(xs))
    P = json.load(open(os.path.join(HERE, 'patches30.json'), encoding='utf-8'))
    with open(os.path.join(AG, 'rv_sec.txt'), 'w', encoding='utf-8', newline='\n') as w:
        for p in P:
            if p['cut'] == '§':
                w.write('%s\n- %s\n+ %s\n理由: %s\n\n' % (p['id'], p['old'], p['new'], p['why']))
    lines = open(os.path.join(EP, 'daihon_v2.md'), encoding='utf-8').read().split('\n')
    on, cur = False, None
    narr, full = [], []
    for ln in lines:
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        if ln.startswith('### '):
            narr.append(ln)
            full.append(ln)
            continue
        m = CUT.match(ln)
        if m:
            cur = m.group(1)
            narr.append('[%s]' % cur)
            full.append(ln)
        elif ln.startswith('> '):
            narr.append(ln[2:])
            full.append(ln)
    open(os.path.join(HERE, 'narr_v2.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(narr) + '\n')
    open(os.path.join(HERE, 'cuts_v2.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(full) + '\n')
    print('対照のカット %d（受け持ちごと %s）・§ の差し替えと語りの通しを書いた' % (n, {g: len(x) for g, x in out.items()}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
