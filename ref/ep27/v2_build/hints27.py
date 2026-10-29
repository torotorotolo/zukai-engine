# -*- coding: utf-8 -*-
"""27本目④'：原文照合の係に渡す「章ごとの写し」と「④の係が開いた URL の手がかり」を作る（読むだけ・第1版は触らない）。

  python -P ref/ep27/v2_build/hints27.py

入力＝v2_build/cuts_v1.txt（narr27.py --full の写し）・src/agents/wf27/wf27_findings.json（④の係の結果＝git の外）
出力＝src/agents/wf27b/in_G1.txt〜in_G5.txt（git の外）＝その組のカットの全行＋カットごとの URL（④の判定と原文の片は入れない＝先入観を渡さない）
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
CUT = re.compile(r'^\*\*(c[0-9]\d{2})\*\*')
GROUPS = {'G1': ('c1', 'c2'), 'G2': ('c3',), 'G3': ('c4',), 'G4': ('c5',), 'G5': ('c6', 'c7')}


def main():
    lines = open(os.path.join(HERE, 'cuts_v1.txt'), encoding='utf-8').read().split('\n')
    data = json.load(open(os.path.join(EP, 'src', 'agents', 'wf27', 'wf27_findings.json'), encoding='utf-8'))
    urls = collections.defaultdict(list)
    for who in ('A', 'B'):
        for x in data[who]['findings']:
            u = (x.get('url') or '').strip()
            for c in re.findall(r'c\d{3}', x.get('cut', '')):
                lab = (x.get('source') or '').strip()
                if u and (lab, u) not in urls[c]:
                    urls[c].append((lab, u))
    blocks = collections.defaultdict(list)
    cur = None
    for ln in lines:
        m = CUT.match(ln)
        if m:
            cur = m.group(1)
        if cur:
            blocks[cur].append(ln)
    outdir = os.path.join(EP, 'src', 'agents', 'wf27b')
    os.makedirs(outdir, exist_ok=True)
    for g, chs in GROUPS.items():
        cuts = [c for c in blocks if c[:2] in chs]
        out = ['# %s のカット（%d）＝台本 第1版の写し（画の欄／出典の欄／語り）' % (g, len(cuts)), '']
        for c in cuts:
            out += [x for x in blocks[c] if x.strip() and x.strip() != '---']
            if urls.get(c):
                out.append('  （手がかり＝④の係が開いた頁）' + ' ／ '.join('%s %s' % (l, u) for l, u in urls[c]))
            out.append('')
        p = os.path.join(outdir, 'in_%s.txt' % g)
        open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
        print(g, len(cuts), 'カット・手がかりのあるカット', sum(1 for c in cuts if urls.get(c)), '→', p)


if __name__ == '__main__':
    main()
