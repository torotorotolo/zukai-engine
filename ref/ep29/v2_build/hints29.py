# -*- coding: utf-8 -*-
"""29本目④'：原文照合の係に渡す「章ごとの写し」と「④の係が開いた頁の手がかり」を作る（読むだけ・第1版は触らない）。
28本目 hints28.py を写した。④ の係の記録（A.md・B.md）に見出しの節が無い＝判定を渡さないために、置き場の字（URL）だけを抜く形に替えた。

  python -P ref/ep29/v2_build/hints29.py

入力＝v2_build/cuts_v1.txt（narr29.py --full の写し）・git の外 src/agents/wf29/A.md・B.md（④ の係の記録）・sources.md
出力＝git の外 src/agents/wf29b/in_G1.txt〜in_G5.txt（その組のカットの全行）と read_hints.txt
     （④ の係と ② が開いた頁の置き場だけ。判定の数と表・原文の片は入れない＝先入観を渡さない）
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents')
CUT = re.compile(r'^\*\*(c[0-9]\d{2})\*\*')
GROUPS = {'G1': ('c1', 'c2'), 'G2': ('c3',), 'G3': ('c4',), 'G4': ('c5',), 'G5': ('c6', 'c7')}
URL = re.compile(r'(?:https?://)?(?:[a-z0-9-]+\.)+(?:jp|com|gmo|net|org)(?:/[A-Za-z0-9_./?=&%-]*)?')


def urls(path):
    """置き場の字だけ（判定と片を渡さない）。ドメインだけのものと robots.txt は落とす。"""
    out = []
    for m in URL.finditer(open(path, encoding='utf-8').read()):
        u = m.group(0).rstrip('/.').replace('https://', '').replace('http://', '')
        if '/' in u and 'robots' not in u and u not in out:
            out.append(u)
    return out


def main():
    lines = open(os.path.join(HERE, 'cuts_v1.txt'), encoding='utf-8').read().split('\n')
    blocks, order, cur = {}, [], None
    for ln in lines:
        m = CUT.match(ln)
        if m:
            cur = m.group(1)
            order.append(cur)
            blocks[cur] = []
        elif ln.startswith('### '):
            cur = None
        if cur:
            blocks[cur].append(ln)
    outdir = os.path.join(AG, 'wf29b')
    os.makedirs(outdir, exist_ok=True)
    for g, chs in GROUPS.items():
        cuts = [c for c in order if c[:2] in chs]
        out = ['# %s のカット（%d）＝台本 第1版の写し（見出し行＝カット番号／画の欄／出典の欄、続く行＝語り。`> Q: ` は聞き役）' % (g, len(cuts)), '']
        for c in cuts:
            out += [x for x in blocks[c] if x.strip() and x.strip() != '---']
            out.append('')
        p = os.path.join(outdir, 'in_%s.txt' % g)
        open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
        print(g, len(cuts), 'カット →', p)
    hint = ['# ④ の係（A＝c101〜c420・B＝c501〜c706）と ② の sources.md に出てくる置き場（判定は入れていない・開く前に robots.txt を確かめる）', '']
    for name, p in (('係A', os.path.join(AG, 'wf29', 'A.md')), ('係B', os.path.join(AG, 'wf29', 'B.md')),
                    ('sources.md', os.path.join(EP, 'sources.md'))):
        hint += ['## %s' % name] + urls(p) + ['']
    p = os.path.join(outdir, 'read_hints.txt')
    open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(hint))
    print('手がかり', sum(1 for x in hint if x.strip()), '行 →', p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
