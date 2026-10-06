# -*- coding: utf-8 -*-
"""19本目④'：第1版→第2版の対照表（直したカットだけ・語りの行と画の欄の行を並べる）を作る。

  python make_diff19.py  → v2_build/diff_v1_v2.md

別の目（4'-18）に渡す。差し替え表 patches19.json の id と why も添える。
"""
import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build19_v2 import blocks  # noqa: E402

ROOT = os.path.dirname(HERE) + '/'
V1 = open(ROOT + 'daihon_v1.md', encoding='utf-8').read().split('\n')
V2 = open(ROOT + 'daihon_v2.md', encoding='utf-8').read().split('\n')
P = json.load(open(HERE + '/patches19.json', encoding='utf-8'))
B1, B2 = blocks(V1), blocks(V2)

out = ['# 第1版 → 第2版の対照（19本目 ④\'・直したカットだけ）', '',
       '- 行頭 `-` が第1版、`+` が第2版。`id` は差し替え表 `patches19.json` の番号（所見の id）',
       '- 出典の頁は `python ref/ep19/v1_build/tools19/pg.py <頁>` で引ける（TR行N→p(1000+N) など）', '']
n = 0
for c in sorted(B2):
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
            out.append('- id `%s`：%s' % (p['id'], p['why']))
    out.append('```diff')
    for d in difflib.unified_diff(t1, t2, lineterm='', n=0):
        if d.startswith(('---', '+++', '@@')):
            continue
        out.append(d)
    out.append('```')
    out.append('')

# カットの外（§ と章の見出し）＝カットの塊に入らない行だけ・空行は除く
def outside(lines, blk):
    inside = set()
    for a, b in blk.values():
        inside.update(range(a, b))
    return [x for i, x in enumerate(lines) if i not in inside and x.strip()]


out.append('## カットの外（§・章の見出し）')
for p in P:
    if p['cut'] in ('§', '*'):
        out.append('- id `%s`：%s' % (p['id'], p['why']))
out.append('```diff')
for d in difflib.unified_diff(outside(V1, B1), outside(V2, B2), lineterm='', n=0):
    if d.startswith(('---', '+++', '@@')):
        continue
    out.append(d)
out.append('```')
open(HERE + '/diff_v1_v2.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('直したカット', n, '→', HERE + '/diff_v1_v2.md')
