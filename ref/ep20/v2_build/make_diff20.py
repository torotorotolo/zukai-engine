# -*- coding: utf-8 -*-
"""20本目④'：第1版→第2版の対照表（直したカットだけ・語りの行と見出し行を並べる）を作る（19本目 make_diff19.py を写した）。

  python ref/ep20/v2_build/make_diff20.py [patches20.json] [--v2 台本]  → v2_build/diff_v1_v2.md

別の目（4'-18）に渡す。差し替え表の id と why も添える。
"""
import difflib
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build20_v2 import blocks  # noqa: E402

ROOT = os.path.dirname(HERE)
a = sys.argv[1:]
pf = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] != '--v2')]
P = json.load(open(pf[0] if pf else os.path.join(HERE, 'patches20.json'), encoding='utf-8'))
v2p = a[a.index('--v2') + 1] if '--v2' in a else os.path.join(ROOT, 'daihon_v2.md')
V1 = open(os.path.join(ROOT, 'daihon_v1.md'), encoding='utf-8').read().split('\n')
V2 = open(v2p, encoding='utf-8').read().split('\n')
B1, B2 = blocks(V1), blocks(V2)

out = ['# 第1版 → 第2版の対照（20本目 ④\'・直したカットだけ）', '',
       '- 行頭 `-` が第1版、`+` が第2版。`id` は差し替え表 `patches20.json` の番号（所見の id）',
       '- 原文は `python ref/ep20/v2_build/pg20.py page 報告書 98` ／ `find 語 --in 報告書` で引ける', '']
n = 0
lost = sorted(set(B1) - set(B2))
for c in sorted(B2, key=lambda c: (c[1], c)):
    if c not in B1:
        continue
    a1, b1 = B1[c]
    a2, b2 = B2[c]
    t1 = [x for x in V1[a1:b1] if x.strip()]
    t2 = [x.replace(' 🔧', '') for x in V2[a2:b2] if x.strip()]
    if t1 == t2:
        continue
    n += 1
    out.append('## ' + c)
    for p in P:
        if p['cut'] == c:
            out.append('- id `%s`：%s' % (p.get('id'), p.get('why', '')))
    out.append('```diff')
    for d in difflib.unified_diff(t1, t2, lineterm='', n=0):
        if d.startswith(('---', '+++', '@@')):
            continue
        out.append(d)
    out.append('```')
    out.append('')


def outside(lines, blk, start_at):
    inside = set()
    for x, y in blk.values():
        inside.update(range(x, y))
    s1 = next(i for i, ln in enumerate(lines) if ln.startswith(start_at))
    return [x for i, x in enumerate(lines) if i >= s1 and i not in inside and x.strip()]


out.append('## カットの外（§1〜§3・§5〜・章の見出し。頭と §0 は除く）')
for p in P:
    if p['cut'] in ('§', '*'):
        out.append('- id `%s`：%s' % (p.get('id'), p.get('why', '')))
out.append('```diff')
for d in difflib.unified_diff(outside(V1, B1, '## 1. '), outside(V2, B2, '## 1. '), lineterm='', n=0):
    if d.startswith(('---', '+++', '@@')):
        continue
    out.append(d)
out.append('```')
if lost:
    out.append('🔴 第2版に無いカット: ' + ' '.join(lost))
open(os.path.join(HERE, 'diff_v1_v2.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('直したカット', n, '→', os.path.join(HERE, 'diff_v1_v2.md'), '／消えたカット', lost or 'なし')
