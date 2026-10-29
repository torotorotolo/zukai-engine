# -*- coding: utf-8 -*-
"""27本目 ④ 原文照合の係（Workflow 2本）の結果を、保存して表に出す（係は report を保存できない＝親が保存する）。

  python ref/ep27/v1_build/wf27_dump.py <task の output ファイル> <保存先フォルダ（git の外＝ref/ep27/src/agents/wf27）>

出すもの：所見の数（係ごと・判定ごと・重さごと）と、1件1行の表（OK 以外を先に）。原文の片は `news_frag.txt`（check_facts 用・`=== p<N> ===` は出典ごと）へ。
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')


def load(path):
    raw = open(path, encoding='utf-8').read()
    i = raw.find('{')
    data = json.loads(raw[i:]) if i >= 0 else None
    if isinstance(data, dict) and 'result' in data and isinstance(data['result'], (dict, str)):
        r = data['result']
        data = json.loads(r) if isinstance(r, str) else r
    return data


def main(src, outdir):
    data = load(src)
    if not isinstance(data, dict) or not {'A', 'B'} <= set(data):
        print('🔴 形が読めない＝止める（fail closed）:', type(data), list(data)[:5] if isinstance(data, dict) else '')
        return 2
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, 'wf27_findings.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    rows = []
    for who in ('A', 'B'):
        r = data[who] or {}
        for x in r.get('findings', []):
            rows.append((who, x))
        print('係%s 所見 %d・読めなかった %d・notes: %s' % (who, len(r.get('findings', [])), len(r.get('unreached', [])),
                                                 (r.get('notes') or '').replace('\n', ' ')))
        for u in r.get('unreached', []):
            print('   unreached: %s' % u)
    c = collections.Counter((w, x['verdict']) for w, x in rows)
    s = collections.Counter(x['severity'] for _, x in rows if x['verdict'] != 'OK')
    print('判定:', dict(c))
    print('OK 以外の重さ:', dict(s))
    order = {'🔴': 0, '⚠️': 1, '・': 2}
    key = lambda wx: (wx[1]['verdict'] == 'OK', order.get(wx[1]['severity'], 3), wx[1]['cut'])
    for who, x in sorted(rows, key=key):
        if x['verdict'] == 'OK':
            continue
        print('--- %s %s %s %s' % (x['cut'], x['severity'], x['verdict'], who))
        print('  主張: %s' % x['claim'])
        print('  出典: %s %s' % (x['source'], x['url']))
        print('  原文: %s' % x['fragment'])
        print('  直し: %s' % x['fix'].replace('&gt;', '>'))
    ok = [x['cut'] for _, x in rows if x['verdict'] == 'OK']
    print('OK のカット（%d件）: %s' % (len(ok), ' '.join(sorted(set(ok)))))
    # check_facts 用の原文の片（出典ごとに1頁）
    by_src = collections.OrderedDict()
    for _, x in rows:
        if x['fragment'].strip():
            by_src.setdefault(x['source'], []).append(x['fragment'].strip())
    with open(os.path.join(outdir, '..', '..', 'news_frag.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for n, (k, frs) in enumerate(by_src.items(), 1):
            f.write('=== p%d ===\n# %s\n%s\n' % (n, k, '\n'.join(frs)))
    print('news_frag.txt に %d 出典・%d 片' % (len(by_src), sum(len(v) for v in by_src.values())))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
