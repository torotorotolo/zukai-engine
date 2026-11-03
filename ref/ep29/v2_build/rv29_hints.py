# -*- coding: utf-8 -*-
"""29本目④'：当て直しの係（ルール 4'-18＝別の目で第1版→第2版の対照を原文に）に渡す写しを作る（読むだけ・28本目 rv28_hints.py を写した）。

  python -P ref/ep29/v2_build/rv29_hints.py

入力＝v2_build/diff_v1_v2.md（make_diff29.py の対照）・git の外 src/agents/wf29b/wf29b_findings.json（④' の係が開いた URL＝判定と原文の片は入れない）
出力＝git の外 src/agents/wf29b/rv_R1.txt（つかみ〜第3章＝c1〜c4）・rv_R2.txt（第4章〜締め＝c5〜c7・カットの外）
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents', 'wf29b')
GROUPS = {'R1': ('c1', 'c2', 'c3', 'c4'), 'R2': ('c5', 'c6', 'c7', '§')}


def main():
    urls = collections.defaultdict(list)
    data = json.load(open(os.path.join(AG, 'wf29b_findings.json'), encoding='utf-8'))
    for g in ('G1', 'G2', 'G3', 'G4', 'G5'):
        for x in (data.get(g) or {}).get('findings', []):
            u = (x.get('url') or '').strip()
            lab = (x.get('source') or '').strip()[:40]
            for c in re.findall(r'c\d{3}', x.get('cut', '')):
                if u and (lab, u) not in urls[c]:
                    urls[c].append((lab, u))
    text = open(os.path.join(HERE, 'diff_v1_v2.md'), encoding='utf-8').read()
    secs = re.split(r'(?m)^## ', text)
    head, body = secs[0], secs[1:]
    for g, keys in GROUPS.items():
        out = ['# %s の当て直しの写し（第1版 → 第2版の対照のうち、この組のカット）' % g, '',
               '- 行頭 `-` が第1版、`+` が第2版。`id` は差し替えの番号と理由。原文は自分で開いて当てる（下の「手がかり」は ④\' の係が開いた頁＝判定は入れていない）', '']
        n = 0
        for s in body:
            title = s.split('\n', 1)[0].strip()
            m = re.match(r'c\d{3}', title)
            key = title[:2] if m else '§'
            if key not in keys:
                continue
            n += 1
            out.append('## ' + s.rstrip())
            if m and urls.get(title[:4]):
                out.append('  （手がかり）' + ' ／ '.join('%s %s' % (l, u) for l, u in urls[title[:4]]))
            out.append('')
        p = os.path.join(AG, 'rv_%s.txt' % g)
        open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
        print(g, '節', n, '→', p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
