# -*- coding: utf-8 -*-
"""28本目④'：原文照合の係に渡す「章ごとの写し」と「④の係が開いた頁の手がかり」を作る（読むだけ・第1版は触らない）。
27本目 hints27.py を写した。④ の係の記録が md（A.md・B.md・C.md）なので、カットごとの URL ではなく「読んだもの」の節だけを抜く形に替えた。

  python -P ref/ep28/v2_build/hints28.py

入力＝v2_build/cuts_v1.txt（narr28.py --full の写し）・git の外 src/agents/wf28/A.md・B.md・C.md（④ の係の記録）
出力＝git の外 src/agents/wf28b/in_G1.txt〜in_G5.txt（その組のカットの全行）と read_hints.txt
     （④ の係が開いた頁と開けなかった頁＝頭の注と「読んだもの」「読めなかった」の節だけ。判定の数と表・原文の片は入れない＝先入観を渡さない）
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
KEEP = ('読んだもの', '読めなかった')
DROP = re.compile(r'判定|数＝|OK \d|直す \d|🔴|⚠️')


def read_sections(path):
    """頭の注（最初の「## 」まで）と、KEEP の語を含む「## 」の節だけ。判定の数の行は落とす。"""
    out, head, on = [], True, False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('## '):
            head = False
            on = any(k in ln for k in KEEP)
        if (head or on) and not DROP.search(ln):
            out.append(ln)
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
    outdir = os.path.join(AG, 'wf28b')
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
    hint = ['# ④ の係（A＝c101〜c423・B＝c501〜c706・C＝通し読み）が開いた頁と開けなかった頁（判定は入れていない）', '']
    for name in ('A', 'B', 'C'):
        p = os.path.join(AG, 'wf28', name + '.md')
        hint += ['## 係%s' % name] + read_sections(p) + ['']
    p = os.path.join(outdir, 'read_hints.txt')
    open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(hint))
    print('手がかり', sum(1 for x in hint if x.strip()), '行 →', p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
