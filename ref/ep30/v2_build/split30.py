# -*- coding: utf-8 -*-
"""30本目④'：原文照合の係に渡す写しを、章の組ごとに git の外へ書き出す（第1版は読むだけ）。

  python -P ref/ep30/v2_build/split30.py

出すもの（ref/ep30/src/agents/wf30c/）：
  in_Gn.txt     その組のカットの全行（見出し＝カット番号 ／ 画の欄 ／ 出典の欄、続く `> ` が語り、`> Q: ` は聞き役）
  fixed_Gn.txt  ④ が「直した」所（src/agents/wf30/patch1.json の 元の文→直した文）のうち、その組のカットのもの（ルール 4'-5＝ここから当たる）
  prior_Gn.txt  ④ の係の所見（src/agents/wf30/wf30_findings.txt）のうち、その組のカットのもの（扱いは第1版 §0-3）
組＝資料が近い章をまとめた。G1 c1〜c3／G2 c4・c5／G3 c7／G4 c8・c9／G5 c6・ca（判決の章）／G6 cb・cc。
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
V1 = os.path.join(EP, 'daihon_v1.md')
OLD = os.path.join(EP, 'src', 'agents', 'wf30')
OUT = os.path.join(EP, 'src', 'agents', 'wf30c')
GROUPS = {'G1': ('c1', 'c2', 'c3'), 'G2': ('c4', 'c5'), 'G3': ('c7',), 'G4': ('c8', 'c9'), 'G5': ('c6', 'ca'), 'G6': ('cb', 'cc')}
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')


def cuts():
    """カット番号 → その塊の行（空行を除く）。"""
    out, cur, on = {}, None, False
    for ln in open(V1, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        m = CUT.match(ln)
        if m:
            cur = m.group(1)
            out[cur] = [ln]
        elif ln.startswith('---') or ln.startswith('### '):
            cur = None
        elif cur and ln.strip():
            out[cur].append(ln)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    cs = cuts()
    patches = json.load(open(os.path.join(OLD, 'patch1.json'), encoding='utf-8'))
    where = {}
    lost = []
    for old, new in patches:
        key = new.lstrip('> ').strip()
        hit = [c for c, ls in cs.items() if key and key in '\n'.join(ls)]
        if hit:
            where.setdefault(hit[0], []).append((old, new))
        else:
            lost.append(new[:40])
    prior = {}
    for ln in open(os.path.join(OLD, 'wf30_findings.txt'), encoding='utf-8'):
        m = re.match(r'^(c[0-9a-d]\d{2})', ln)
        if m:
            prior.setdefault(m.group(1), []).append(ln.rstrip('\n'))
    for g, heads in GROUPS.items():
        mine = [c for c in cs if c[:2] in heads]
        with open(os.path.join(OUT, 'in_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            for c in mine:
                f.write('\n'.join(cs[c]) + '\n\n')
        with open(os.path.join(OUT, 'fixed_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            for c in mine:
                for old, new in where.get(c, []):
                    f.write('%s\n  元: %s\n  今: %s\n' % (c, old, new))
        with open(os.path.join(OUT, 'prior_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            for c in mine:
                for x in prior.get(c, []):
                    f.write(x + '\n')
        print('%s カット %d・④の直し %d・④の所見 %d' % (g, len(mine), sum(len(where.get(c, [])) for c in mine), sum(len(prior.get(c, [])) for c in mine)))
    print('カット計', len(cs), '・④の直し', len(patches), '・当て先が見つからない', len(lost))
    for x in lost:
        print('  ?', x)
    return 0


if __name__ == '__main__':
    sys.exit(main())
