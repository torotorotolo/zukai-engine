# -*- coding: utf-8 -*-
"""27本目④'：当て直しの係（4'-18＝別の目）に渡す写しを作る（読むだけ）。

  python -P ref/ep27/v2_build/rv27_hints.py

入力＝v2_build/diff_v1_v2.md（make_diff27.py の対照）・src/agents/wf27/wf27_findings.json と src/agents/wf27b/wf27b_findings.json（④ と ④' の係が開いた URL＝判定と原文の片は入れない）
出力＝git の外 src/agents/wf27b/rv_R1.txt（つかみ〜第3章＝c1〜c4）・rv_R2.txt（第4章〜締め＝c5〜c7・カットの外）
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents')
GROUPS = {'R1': ('c1', 'c2', 'c3', 'c4'), 'R2': ('c5', 'c6', 'c7', '§')}


def urls():
    out = collections.defaultdict(list)
    for p, keys in ((os.path.join(AG, 'wf27', 'wf27_findings.json'), ('A', 'B')),
                    (os.path.join(AG, 'wf27b', 'wf27b_findings.json'), ('G1', 'G2', 'G3', 'G4', 'G5'))):
        d = json.load(open(p, encoding='utf-8'))
        for k in keys:
            for x in (d.get(k) or {}).get('findings', []):
                u = (x.get('url') or '').strip()
                if not u.startswith('http'):
                    continue
                for c in re.findall(r'c\d{3}', x.get('cut', '')):
                    lab = (x.get('source') or '').strip()[:60]
                    if (lab, u) not in out[c]:
                        out[c].append((lab, u))
    return out


def main():
    diff = open(os.path.join(HERE, 'diff_v1_v2.md'), encoding='utf-8').read()
    secs = re.split(r'(?m)^## ', diff)
    head, secs = secs[0], secs[1:]
    u = urls()
    for g, chs in GROUPS.items():
        out = ['# %s：第1版 → 第2版の対照（直したカット）＋カットごとの手がかりの URL（前の係が開いた頁・判定は書いていない）' % g, '']
        n = 0
        for s in secs:
            name = s.split('\n', 1)[0].strip()
            key = name[:2] if name.startswith('c') else '§'
            if key not in chs:
                continue
            n += 1
            out.append('## ' + s.rstrip())
            c = name[:4]
            if u.get(c):
                out.append('- 手がかり：' + ' ／ '.join('%s %s' % (l, x) for l, x in u[c][:6]))
            out.append('')
        p = os.path.join(AG, 'wf27b', 'rv_%s.txt' % g)
        open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        print(g, '節', n, '→', p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
