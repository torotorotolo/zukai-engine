# -*- coding: utf-8 -*-
"""31本目④'：当て直しの係（R1〜R4＝別の目・ルール 4'-18）へ渡す材料を、章の組ごとに git の外（src/agents/wf31b/）へ書き出す。

  python -P ref/ep31/v2_build/prep_review31.py

出すもの：
  diff_Rn.md   第1版→第2版の対照（直したカットだけ・消したカットも）＝make_diff31.py --only
  in3_Rn.txt   第2版の受け持ちのカットの全文（当て直しの案の old はここから取る）
  disp_Rn.txt  直す係と親が「採らない／一部／後の工程へ」にした所見（所見の中身つき＝その判断が正しいかも見る）
組＝R1 c1〜c3／R2 c4〜c6／R3 c7〜c9／R4 ca〜cc＋§（カットの外）
"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build31_v2 as B             # noqa: E402

EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
AG = os.path.join(EP, 'src', 'agents', 'wf31b')
GROUPS = {'R1': ('c1', 'c2', 'c3'), 'R2': ('c4', 'c5', 'c6'), 'R3': ('c7', 'c8', 'c9'), 'R4': ('ca', 'cb', 'cc')}
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')


def main():
    rows = {}
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7'):
        for x in json.load(open(os.path.join(AG, 'findings_%s.json' % g), encoding='utf-8')):
            rows[x['id']] = x
    for x in json.load(open(os.path.join(HERE, 'own31.json'), encoding='utf-8')):
        rows[x['id']] = x
    disp = []
    for f in ('F1', 'F2', 'F3', 'F4', 'F5', 'F6'):
        for d in json.load(open(os.path.join(AG, 'fix_%s.json' % f), encoding='utf-8')).get('dispositions') or []:
            if d['v'] != '済み':
                disp.append((f, d['id'], d['v'], d['why']))
    ovr = json.load(open(os.path.join(HERE, 'ledger_ovr.json'), encoding='utf-8'))
    for k, lab in (('not_adopted', '採らない（親）'), ('moved', '後の工程へ（親）')):
        for fid, why in ovr.get(k, {}).items():
            disp.append(('親', fid, lab, why))
    v2 = open(os.path.join(EP, 'daihon_v2.md'), encoding='utf-8').read().split('\n')
    blk = B.blocks(v2)
    for r, hs in GROUPS.items():
        out = os.path.join(AG, 'diff_%s.md' % r)
        p = subprocess.run([sys.executable, '-P', os.path.join(HERE, 'make_diff31.py'), '--only', ','.join(hs), '--out', out],
                           cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(r, p.stdout.strip().split('\n')[-1][:120])
        with open(os.path.join(AG, 'in3_%s.txt' % r), 'w', encoding='utf-8', newline='\n') as w:
            for a, c in sorted((a, c) for c, (a, b) in blk.items() if c[:2] in hs):
                w.write('\n'.join(x for x in v2[a:blk[c][1]] if x.strip()) + '\n\n')
        n = 0
        with open(os.path.join(AG, 'disp_%s.txt' % r), 'w', encoding='utf-8', newline='\n') as w:
            for who, fid, v, why in disp:
                x = rows.get(fid) or {}
                cut = x.get('cut') or ''
                if cut[:2] in hs or (r == 'R4' and not cut.startswith('c')):
                    n += 1
                    w.write('%s %s %s〔%s〕 所見: [%s/%s] 「%s」 ⇐ %s `%s` ｜ 案: %s → %s ｜ 理由: %s\n  扱いの理由: %s\n' % (
                        fid, x.get('severity'), cut, v, x.get('aspect'), x.get('kind'), x.get('text'), x.get('source'),
                        x.get('fragment'), x.get('fix_old'), x.get('fix_new'), x.get('why'), why))
        print('  %s 直さなかった所見 %d' % (r, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
