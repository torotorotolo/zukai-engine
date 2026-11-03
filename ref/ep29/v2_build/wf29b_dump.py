# -*- coding: utf-8 -*-
"""29本目④'：原文照合の係（Workflow 6本＝章ごと5本 G1〜G5＋通し読み G6）の結果を保存し、表に出す（28本目 wf28b_dump.py を写した）。
係は記録を保存できない＝親が Workflow の journal.jsonl（各係の返した値が入る）から抜いて保存する。

  python -P ref/ep29/v2_build/wf29b_dump.py <Workflow の journal.jsonl>

出すもの：
- git の外 src/agents/wf29b/wf29b_findings.json（全部・id は Workflow の返しと同じ＝G1-001 …）
- git の外 src/news_frag_v2.txt＝④ の src/news_frag.txt ＋ この回の係の原文の片（出典ごとに `=== p<N> ===`＝check_facts 用）
- 標準出力＝係ごとの数（判定・重さ）・当て残したカット・開けなかった頁・OK 以外の所見の表（🔴→⚠️→・の順）・G6 の意見
形が読めなければ止める（fail closed）。
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
OUTDIR = os.path.join(EP, 'src', 'agents', 'wf29b')
FRAG_V1 = os.path.join(EP, 'src', 'news_frag.txt')
FRAG_V2 = os.path.join(EP, 'src', 'news_frag_v2.txt')
GROUPS = ('G1', 'G2', 'G3', 'G4', 'G5', 'G6')
EXPECT = {'G1': ('c1', 'c2'), 'G2': ('c3',), 'G3': ('c4',), 'G4': ('c5',), 'G5': ('c6', 'c7')}
SEV = {'🔴': 0, '⚠️': 1, '・': 2}


def find_result(obj):
    """journal の1行の中から、係の返した値（findings を持つ dict）を探す。"""
    if isinstance(obj, dict):
        if 'findings' in obj and 'covered_cuts' in obj:
            return obj
        for v in obj.values():
            r = find_result(v)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_result(v)
            if r is not None:
                return r
    elif isinstance(obj, str) and '"findings"' in obj:
        try:
            return find_result(json.loads(obj))
        except ValueError:
            return None
    return None


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
        if g not in GROUPS:
            g = (r.get('group') or '').strip()[:2]
        if g in GROUPS:
            data[g] = r
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
    miss_g = [g for g in GROUPS if g not in data]
    if miss_g:
        print('🔴 係の結果が無い＝止める（fail closed）:', miss_g, '／読めた:', sorted(data))
        return 2
    os.makedirs(OUTDIR, exist_ok=True)
    allcuts = v1_cuts()
    rows = []
    for g in GROUPS:
        for k, x in enumerate(data[g].get('findings', []), 1):
            x['id'] = '%s-%03d' % (g, k)
            rows.append((g, x))
    with open(os.path.join(OUTDIR, 'wf29b_findings.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print('保存 →', os.path.join(OUTDIR, 'wf29b_findings.json'))
    for g in GROUPS:
        r = data[g]
        fs = r.get('findings', [])
        v = collections.Counter(x.get('verdict') for x in fs)
        s = collections.Counter(x.get('severity') for x in fs if x.get('verdict') != 'OK')
        line = '%s 所見 %d（%s）・OK 以外の重さ %s' % (g, len(fs), dict(v), dict(s))
        if g in EXPECT:
            exp = [c for c in allcuts if c[:2] in EXPECT[g]]
            cov = set(r.get('covered_cuts', [])) | {x.get('cut', '')[:4] for x in fs}
            miss = [c for c in exp if c not in cov]
            nof = [c for c in exp if c not in {x.get('cut', '')[:4] for x in fs}]
            line += '・当て残し %d %s・所見の無いカット %d %s・開けなかった %d' % (
                len(miss), ' '.join(miss), len(nof), ' '.join(nof), len(r.get('unreached', [])))
        print(line)
    print()
    print('## 開けなかった頁・確かめられなかった事柄')
    for g in GROUPS:
        for u in data[g].get('unreached', []):
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
    print('## 意見と所感')
    for g in GROUPS:
        for o in data[g].get('opinions', []):
            print('- %s %s：%s ／ %s' % (g, o.get('item'), o.get('recommend'), o.get('why')))
    for g in GROUPS:
        print('- %s notes：%s' % (g, data[g].get('notes', '')))
    # 原文の片 → news_frag_v2.txt（④ の頁のあとに足す）
    base = open(FRAG_V1, encoding='utf-8').read().rstrip('\n')
    n0 = len(re.findall(r'^=== p\d+ ===', base, re.M))
    bysrc = collections.OrderedDict()
    for g, x in rows:
        fr = (x.get('fragment') or '').strip()
        if fr and g != 'G6':
            s = (x.get('source') or '').strip() or '（出典の書き込みなし）'
            bysrc.setdefault(s, [])
            if fr not in bysrc[s]:
                bysrc[s].append(fr)
    add = []
    for k, (s, frs) in enumerate(bysrc.items(), 1):
        add += ['=== p%d ===' % (n0 + k), '# ' + s] + frs
    open(FRAG_V2, 'w', encoding='utf-8', newline='\n').write(base + '\n' + '\n'.join(add) + '\n')
    print('\n原文の片 →', FRAG_V2, '（④ の %d頁 ＋ この回 %d頁・%d片）' % (n0, len(bysrc), sum(len(v) for v in bysrc.values())))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
