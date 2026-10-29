# -*- coding: utf-8 -*-
"""27本目④'：当て直しの係（4'-18・Workflow 2本＝R1・R2）の結果を保存し、表に出す（係は report を保存できない＝親が保存する）。

  python -P ref/ep27/v2_build/rv27_dump.py <Workflow の出力（task の output ファイル）>

出すもの＝git の外 src/agents/wf27b/rv27_findings.json（全部・id を振る＝R1-001 …）と、標準出力の表（判定の数・当て残し・OK 以外の所見＝🔴→⚠️→・）。
fix_old が daihon_v2.md のそのカットの中でちょうど1回あるかも見る（当てられる形か）。
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from build27_v2 import blocks  # noqa: E402

SEV = {'🔴': 0, '⚠️': 1, '・': 2}


def load(path):
    raw = open(path, encoding='utf-8').read()
    i = raw.find('{')
    data = json.loads(raw[i:]) if i >= 0 else None
    for _ in range(3):
        if isinstance(data, dict) and 'result' in data and isinstance(data['result'], (dict, str)):
            r = data['result']
            data = json.loads(r) if isinstance(r, str) else r
    return data


def main(src):
    data = load(src)
    if not isinstance(data, dict) or not {'R1', 'R2'} <= set(data):
        print('🔴 形が読めない＝止める（fail closed）:', type(data), list(data)[:5] if isinstance(data, dict) else '')
        return 2
    v2 = open(os.path.join(EP, 'daihon_v2.md'), encoding='utf-8').read().split('\n')
    blk = blocks(v2)
    diff = open(os.path.join(HERE, 'diff_v1_v2.md'), encoding='utf-8').read()
    changed = re.findall(r'(?m)^## (c\d{3})', diff)
    rows = []
    for g in ('R1', 'R2'):
        r = data[g] or {}
        for k, x in enumerate(r.get('findings', []), 1):
            x['id'] = '%s-%03d' % (g, k)
            rows.append(x)
    with open(os.path.join(EP, 'src', 'agents', 'wf27b', 'rv27_findings.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    for g, rng in (('R1', ('c1', 'c2', 'c3', 'c4')), ('R2', ('c5', 'c6', 'c7'))):
        r = data[g] or {}
        fs = r.get('findings', [])
        v = collections.Counter(x.get('verdict') for x in fs)
        exp = [c for c in changed if c[:2] in rng]
        cov = set(r.get('covered', [])) | {x.get('cut', '')[:4] for x in fs}
        miss = [c for c in exp if c not in cov]
        print('%s 所見 %d（%s）・直したカット %d のうち当て残し %d %s・開けなかった %d' % (
            g, len(fs), dict(v), len(exp), len(miss), ' '.join(miss), len(r.get('unreached', []))))
    print('\n## 開けなかった頁')
    for g in ('R1', 'R2'):
        for u in (data[g] or {}).get('unreached', []):
            print('- %s %s' % (g, u))
    print('\n## OK 以外の所見（🔴→⚠️→・）')
    bad = [x for x in rows if x.get('verdict') != 'OK']
    bad.sort(key=lambda x: (SEV.get(x.get('severity'), 9), x.get('cut', ''), x['id']))
    for x in bad:
        c = x.get('cut', '')[:4]
        fo = x.get('fix_old') or ''
        if fo and c in blk:
            a, b = blk[c]
            n = '\n'.join(v2[a:b]).count(fo)
            hit = 'old ×%d' % n
        else:
            hit = 'old なし'
        print('- %s %s %s [%s・%s・%s] 「%s」 ⇐ %s `%s` ｜ 案: %s → %s ｜ %s' % (
            x['id'], x.get('severity'), x.get('cut'), x.get('kind'), x.get('verdict'), hit, x.get('text'),
            x.get('source'), x.get('fragment'), fo, x.get('fix_new'), x.get('why')))
    print('\n## notes')
    for g in ('R1', 'R2'):
        print('- %s：%s' % (g, (data[g] or {}).get('notes', '')))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
