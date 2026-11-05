# -*- coding: utf-8 -*-
"""30本目④'：直す係（F1〜F6）へ渡す表を書く（git の外の src/agents/wf30c/）。

  python -P ref/ep30/v2_build/prep_fix30.py

入力＝findings_G1〜G7.json・own30.json（所見）／patches_base.json（親の差し替え）
出力＝todo_Fn.txt（親の差し替えで済んでいない OK 以外の所見）・base_Fn.txt（親の差し替えのうち受け持ちのカット）・in2_Fn.txt（第1版＋親の差し替えの、受け持ちのカットの全文）
      base30.md（第1版＋親の差し替え）
受け持ち＝F1 c1〜c3／F2 c4・c5／F3 c7／F4 c8・c9／F5 c6・ca／F6 cb・cc（所見の cut が複数なら最初のカットで）
最後に、親の差し替えで済んでいない 🔴・⚠️ の数を出す（--list で一覧）。
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build30_v2 as B             # noqa: E402

EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents', 'wf30c')
GROUP = {'c1': 'F1', 'c2': 'F1', 'c3': 'F1', 'c4': 'F2', 'c5': 'F2', 'c7': 'F3', 'c8': 'F4', 'c9': 'F4', 'c6': 'F5', 'ca': 'F5', 'cb': 'F6', 'cc': 'F6'}
SEV = {'🔴': 0, '⚠️': 1, '・': 2}


def first_cut(x):
    m = re.search(r'c[0-9a-d]\d{2}', x.get('cut') or '')
    return m.group(0) if m else ''


def main():
    rows = []
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7'):
        rows += json.load(open(os.path.join(AG, 'findings_%s.json' % g), encoding='utf-8'))
    rows += json.load(open(os.path.join(HERE, 'own30.json'), encoding='utf-8'))
    base = json.load(open(os.path.join(HERE, 'patches_base.json'), encoding='utf-8'))
    done = {f for p in base for f in p.get('from', [])}
    v1 = open(B.V1, encoding='utf-8').read().split('\n')
    lines, _, _, bad, _ = B.apply(base, v1)
    if bad:
        print('🔴 親の差し替えが当たらない', bad)
        return 1
    open(os.path.join(AG, 'base30.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    blk = B.blocks(lines)
    todo = {k: [] for k in ('F1', 'F2', 'F3', 'F4', 'F5', 'F6')}
    other = []
    for x in rows:
        if x.get('verdict') == 'OK' or x['id'] in done:
            continue
        c = first_cut(x)
        g = GROUP.get(c[:2])
        if g:
            todo[g].append(x)
        else:
            other.append(x)
    for g, xs in todo.items():
        xs.sort(key=lambda x: (first_cut(x), SEV.get(x.get('severity'), 9), x['id']))
        with open(os.path.join(AG, 'todo_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as w:
            for x in xs:
                w.write('%s %s %s [%s/%s・%s] 「%s」\n  原文: %s `%s`\n  案: %s → %s\n  理由: %s\n' % (
                    x['id'], x.get('severity'), x.get('cut'), x.get('aspect'), x.get('kind'), x.get('verdict'), x.get('text'),
                    x.get('source') or '', x.get('fragment') or '', x.get('fix_old') or '', x.get('fix_new') or '', x.get('why') or ''))
        with open(os.path.join(AG, 'base_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as w:
            for p in base:
                c = p['cut']
                if GROUP.get(c[:2]) == g:
                    if p.get('move_after'):
                        w.write('%s %s の塊を %s の後ろへ移した（%s）\n' % (p['id'], c, p['move_after'], p['why']))
                    else:
                        w.write('%s %s\n  元: %s\n  今: %s\n  理由: %s\n' % (p['id'], c, p['old'][:300], p['new'][:300], p['why']))
        with open(os.path.join(AG, 'in2_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as w:
            order = sorted((a, c) for c, (a, b) in blk.items() if GROUP.get(c[:2]) == g)
            for a, c in order:
                b = blk[c][1]
                w.write('\n'.join(x for x in lines[a:b] if x.strip()) + '\n\n')
    n = {k: (len(v), sum(1 for x in v if x.get('severity') == '🔴'), sum(1 for x in v if x.get('severity') == '⚠️')) for k, v in todo.items()}
    print('親の差し替えで済んだ所見 %d／係へ渡す %d（受け持ち外 %d）' % (len(done), sum(v[0] for v in n.values()), len(other)))
    print(n)
    if '--list' in sys.argv:
        for g, xs in todo.items():
            for x in xs:
                if x.get('severity') in ('🔴', '⚠️'):
                    print('%s %s %s %s %s｜%s' % (g, x['id'], x.get('severity'), x.get('cut'), x.get('verdict'), (x.get('text') or '')[:40]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
