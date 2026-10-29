# -*- coding: utf-8 -*-
"""27本目④'：原文照合の係（Workflow 6本＝章ごと5本 G1〜G5＋通し読み G6）の結果を保存し、表に出す（係は report を保存できない＝親が保存する）。

  python -P ref/ep27/v2_build/wf27b_dump.py <Workflow の出力（task の output ファイルか、結果の JSON）>

出すもの：
- git の外 src/agents/wf27b/wf27b_findings.json（全部・id を振る＝G1-001 …）
- git の外 src/news_frag_v2.txt＝④ の src/news_frag.txt ＋ この回の係の原文の片（出典ごとに `=== p<N> ===`＝check_facts 用）
- 標準出力＝係ごとの数（判定・重さ）・当て残したカット・開けなかった頁・OK 以外の所見の表（🔴→⚠️→・の順）・G6 の意見
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
OUTDIR = os.path.join(EP, 'src', 'agents', 'wf27b')
FRAG_V1 = os.path.join(EP, 'src', 'news_frag.txt')
FRAG_V2 = os.path.join(EP, 'src', 'news_frag_v2.txt')
EXPECT = {'G1': ('c1', 'c2'), 'G2': ('c3',), 'G3': ('c4',), 'G4': ('c5',), 'G5': ('c6', 'c7')}
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


def v1_cuts():
    cuts = []
    for ln in open(os.path.join(HERE, 'cuts_v1.txt'), encoding='utf-8'):
        m = re.match(r'^\*\*(c\d{3})\*\*', ln)
        if m:
            cuts.append(m.group(1))
    return cuts


def main(src):
    data = load(src)
    if not isinstance(data, dict) or not {'G1', 'G2', 'G3', 'G4', 'G5', 'G6'} <= set(data):
        print('🔴 形が読めない＝止める（fail closed）:', type(data), list(data)[:8] if isinstance(data, dict) else '')
        return 2
    os.makedirs(OUTDIR, exist_ok=True)
    allcuts = v1_cuts()
    rows = []
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'):
        r = data[g]
        if not r:
            print('🔴 %s は結果が無い（null）' % g)
            continue
        for k, x in enumerate(r.get('findings', []), 1):
            x['id'] = '%s-%03d' % (g, k)
            rows.append((g, x))
    with open(os.path.join(OUTDIR, 'wf27b_findings.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print('保存 →', os.path.join(OUTDIR, 'wf27b_findings.json'))
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'):
        r = data[g] or {}
        fs = r.get('findings', [])
        v = collections.Counter(x.get('verdict') for x in fs)
        s = collections.Counter(x.get('severity') for x in fs if x.get('verdict') != 'OK')
        line = '%s 所見 %d（%s）・OK 以外の重さ %s' % (g, len(fs), dict(v), dict(s))
        if g in EXPECT:
            exp = [c for c in allcuts if c[:2] in EXPECT[g]]
            cov = set(r.get('covered_cuts', [])) | {x.get('cut', '')[:4] for x in fs}
            miss = [c for c in exp if c not in cov]
            line += '・当て残し %d %s・開けなかった %d' % (len(miss), ' '.join(miss), len(r.get('unreached', [])))
        print(line)
    print()
    print('## 開けなかった頁・確かめられなかった事柄')
    for g in ('G1', 'G2', 'G3', 'G4', 'G5'):
        for u in (data[g] or {}).get('unreached', []):
            print('- %s %s' % (g, u))
    print()
    print('## OK 以外の所見（🔴→⚠️→・）')
    bad = [(g, x) for g, x in rows if x.get('verdict') != 'OK']
    bad.sort(key=lambda t: (SEV.get(t[1].get('severity'), 9), t[1].get('cut', ''), t[1]['id']))
    for g, x in bad:
        print('- %s %s %s [%s/%s・%s] 「%s」 ⇐ %s `%s` ｜ 案: %s → %s ｜ %s' % (
            x['id'], x.get('severity'), x.get('cut'), x.get('aspect'), x.get('kind'), x.get('verdict'),
            x.get('text'), x.get('source'), x.get('fragment'), x.get('fix_old'), x.get('fix_new'), x.get('why')))
    print()
    print('## G6 の意見と所感')
    for o in (data['G6'] or {}).get('opinions', []):
        print('- %s：%s ／ %s' % (o.get('item'), o.get('recommend'), o.get('why')))
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'):
        print('- %s notes：%s' % (g, (data[g] or {}).get('notes', '')))
    # 原文の片 → news_frag_v2.txt（④ の頁のあとに足す）
    base = open(FRAG_V1, encoding='utf-8').read().rstrip('\n')
    n0 = len(re.findall(r'^=== p\d+ ===', base, re.M))
    bysrc = collections.OrderedDict()
    for g, x in rows:
        fr = (x.get('fragment') or '').strip()
        if fr and g != 'G6':
            bysrc.setdefault((x.get('source') or '').strip() or '（出典の書き込みなし）', [])
            if fr not in bysrc[(x.get('source') or '').strip() or '（出典の書き込みなし）']:
                bysrc[(x.get('source') or '').strip() or '（出典の書き込みなし）'].append(fr)
    add = []
    for k, (s, frs) in enumerate(bysrc.items(), 1):
        add += ['=== p%d ===' % (n0 + k), '# ' + s] + frs
    open(FRAG_V2, 'w', encoding='utf-8', newline='\n').write(base + '\n' + '\n'.join(add) + '\n')
    print('\n原文の片 →', FRAG_V2, '（④ の %d頁 ＋ この回 %d頁・%d片）' % (n0, len(bysrc), sum(len(v) for v in bysrc.values())))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
