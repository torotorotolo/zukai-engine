# -*- coding: utf-8 -*-
"""28本目④'：当て直しの係（4'-18・Workflow 2本＝R1・R2）の結果を保存し、表に出す（27本目 rv27_dump.py を写した）。
係は記録を保存できない＝親が Workflow の journal.jsonl から抜いて保存する。

  python -P ref/ep28/v2_build/rv28_dump.py <Workflow の journal.jsonl>

出すもの＝git の外 src/agents/wf28b/rv28_findings.json（全部・id は Workflow の返しと同じ＝R1-001 …）と、標準出力の表
（判定の数・当て残し・OK 以外の所見＝🔴→⚠️→・）。fix_old が daihon_v2.md のそのカットの中でちょうど1回あるかも見る（当てられる形か）。
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
from build28_v2 import blocks  # noqa: E402
from wf28b_dump import find_result  # noqa: E402

AG = os.path.join(EP, 'src', 'agents', 'wf28b')
SEV = {'🔴': 0, '⚠️': 1, '・': 2}


def load(path):
    labels, data = {}, {}
    for ln in open(path, encoding='utf-8'):
        if not ln.strip():
            continue
        d = json.loads(ln)
        key = d.get('key') or d.get('agentId')
        if d.get('label'):
            labels[key] = d['label']
            if d.get('agentId'):
                labels[d['agentId']] = d['label']
        r = find_result(d)
        if r is None:
            continue
        lab = labels.get(key) or labels.get(d.get('agentId')) or d.get('label') or r.get('group', '')
        g = (lab or '').split(' ')[0]
        if g not in ('R1', 'R2'):
            g = (r.get('group') or '').strip()[:2]
        if g in ('R1', 'R2'):
            data[g] = r
    return data


def main(src):
    data = load(src)
    if not {'R1', 'R2'} <= set(data):
        print('🔴 当て直しの係の結果が無い＝止める（fail closed）:', sorted(data))
        return 2
    v2 = open(os.path.join(EP, 'daihon_v2.md'), encoding='utf-8').read().split('\n')
    blk = blocks(v2)
    rows = []
    for g in ('R1', 'R2'):
        for k, x in enumerate(data[g].get('findings', []), 1):
            x['id'] = '%s-%03d' % (g, k)
            rows.append((g, x))
    with open(os.path.join(AG, 'rv28_findings.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print('保存 →', os.path.join(AG, 'rv28_findings.json'))
    for g in ('R1', 'R2'):
        fs = data[g].get('findings', [])
        v = collections.Counter(x.get('verdict') for x in fs)
        s = collections.Counter(x.get('severity') for x in fs if x.get('verdict') != 'OK')
        print('%s 所見 %d（%s）・OK 以外の重さ %s・開けなかった %d' % (g, len(fs), dict(v), dict(s), len(data[g].get('unreached', []))))
    print()
    print('## 開けなかった頁')
    for g in ('R1', 'R2'):
        for u in data[g].get('unreached', []):
            print('- %s %s' % (g, u))
    print()
    print('## OK 以外の所見（🔴→⚠️→・）＝［当てられる形か］')
    bad = [(g, x) for g, x in rows if x.get('verdict') != 'OK']
    bad.sort(key=lambda t: (SEV.get(t[1].get('severity'), 9), t[1].get('cut', ''), t[1]['id']))
    for g, x in bad:
        c = (x.get('cut') or '')[:4]
        old = x.get('fix_old') or ''
        if c in blk and old:
            a, b = blk[c]
            n = '\n'.join(v2[a:b]).count(old)
            fit = 'ちょうど1回' if n == 1 else ('🔴 %d回' % n)
        else:
            fit = '—'
        print('- %s %s %s [%s・%s] 「%s」 ⇐ %s `%s` ｜ 案: %s → %s ｜ %s ［%s］' % (
            x['id'], x.get('severity'), x.get('cut'), x.get('kind'), x.get('verdict'), x.get('text'),
            x.get('source'), x.get('fragment'), old, x.get('fix_new'), x.get('why'), fit))
    for g in ('R1', 'R2'):
        print('- %s notes：%s' % (g, data[g].get('notes', '')))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
