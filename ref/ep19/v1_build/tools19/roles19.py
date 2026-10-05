# -*- coding: utf-8 -*-
"""台本の聞き役の行から roles.tsv（cid・役割・文）を組む。役割は roles_map.tsv（文の一部 → 役割）を人が決める。
文は m19.py／check_listener と同じ関数で取り出す（照合の鍵がずれないように）。
  python roles19.py <台本.md> <roles.tsv の出力先>
"""
import os
import sys

sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
import check_script as CS   # noqa: E402
import speaker              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
rmap = []
for ln in open(os.path.join(HERE, 'roles_map.tsv'), encoding='utf-8'):
    if ln.strip() and not ln.startswith('#'):
        k, r = ln.rstrip('\n').split('\t')
        rmap.append((k, r))
text = open(sys.argv[1], encoding='utf-8').read()
rows, miss, used = [], [], set()
for cid, pic, ls in CS.parse(text):
    for raw in ls:
        who = speaker.split(raw)[0]
        if who != speaker.WHO_Q:
            continue
        t = speaker.bare(CS.STAR_RE.sub('', raw).replace('**', '').strip())
        hit = [(k, r) for k, r in rmap if k in t]
        if len(hit) != 1:
            miss.append((cid, t, len(hit)))
            continue
        used.add(hit[0][0])
        rows.append((cid, hit[0][1], t))
os.makedirs(os.path.dirname(sys.argv[2]), exist_ok=True)
with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as f:
    f.write('# cid\t役割\t文（19本目 台本第1版の聞き役・役割は人が決めた＝scratchpad の roles_map.tsv）\n')
    for r in rows:
        f.write('\t'.join(r) + '\n')
from collections import Counter
c = Counter(r[1] for r in rows)
print('行', len(rows), dict(c), {k: round(v / max(1, len(rows)), 2) for k, v in c.items()})
for m in miss:
    print('🔴 役割が決まらない（当たり %d）: %s %s' % (m[2], m[0], m[1]))
unused = [k for k, _ in rmap if k not in used]
if unused:
    print('⚠️ 使われなかった鍵:', unused)
