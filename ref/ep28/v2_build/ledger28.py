# -*- coding: utf-8 -*-
"""28本目④'：所見の台帳（1行1粗）を、係の記録と ④' の本人の所見と差し替え表から組む（手で写さない・27本目 ledger27.py を写した）。

  python -P ref/ep28/v2_build/ledger28.py   → v2_build/ledger28.md

入力＝git の外 src/agents/wf28b/wf28b_findings.json（係6本＝G1〜G6）・v2_build/own28.json（④' の本人＝P）・
      v2_build/patches28.json（各差し替えの from＝もとの所見の番号）・v2_build/ledger_ovr.json（直さなかった所見と理由＝not_adopted／一部だけ採った＝partial）・
      当て直しがあれば src/agents/wf28b/rv28_findings.json（R1・R2）
扱い＝直した（差し替えの id）／一部（理由）／直さない（理由）。OK 以外の所見で扱いが決まっていないものが1件でもあれば止める（exit 1）。
台本の字・原文の片だけを載せる。名前は載せない（namecheck28.py が当てる）。
"""
import collections
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents', 'wf28b')
SEV = {'🔴': 0, '⚠️': 1, '・': 2}
GROUPS = ('G1', 'G2', 'G3', 'G4', 'G5', 'G6')


def load():
    d = json.load(open(os.path.join(AG, 'wf28b_findings.json'), encoding='utf-8'))
    rows = []
    for g in GROUPS:
        for k, x in enumerate((d.get(g) or {}).get('findings', []), 1):
            x = dict(x)
            x.setdefault('id', '%s-%03d' % (g, k))
            rows.append(x)
    own = os.path.join(HERE, 'own28.json')
    if os.path.exists(own):
        for x in json.load(open(own, encoding='utf-8')):
            rows.append(dict(x))
    rv = os.path.join(AG, 'rv28_findings.json')     # 当て直し（4'-18）＝R1・R2
    if os.path.exists(rv):
        r = json.load(open(rv, encoding='utf-8'))
        for g in ('R1', 'R2'):
            for k, x in enumerate((r.get(g) or {}).get('findings', []), 1):
                x = dict(x)
                x.setdefault('id', '%s-%03d' % (g, k))
                x.setdefault('aspect', 'B')
                rows.append(x)
    return rows


def main():
    rows = load()
    patches = json.load(open(os.path.join(HERE, 'patches28.json'), encoding='utf-8'))
    ovr_p = os.path.join(HERE, 'ledger_ovr.json')
    ovr = json.load(open(ovr_p, encoding='utf-8')) if os.path.exists(ovr_p) else {}
    not_adopted, partial = ovr.get('not_adopted', {}), ovr.get('partial', {})
    byf = collections.defaultdict(list)
    for p in patches:
        for f in p.get('from', []):
            byf[f].append(p['id'])
    ok = [x for x in rows if x.get('verdict') == 'OK']
    bad = [x for x in rows if x.get('verdict') != 'OK']
    bad.sort(key=lambda x: (SEV.get(x.get('severity'), 9), x.get('cut', ''), x['id']))
    out = ['# 28本目 ④\' 所見の台帳（ledger28.py が組む・手で直さない）', '',
           '- 入力＝係6本（G1〜G5＝章ごとの原文照合・G6＝通し読み）の記録 `src/agents/wf28b/wf28b_findings.json`（git の外）＋④\' の本人の所見 `own28.json`（P）＋差し替え表 `patches28.json`＋扱いの上書き `ledger_ovr.json`',
           '- 扱い＝**直した**（差し替えの id＝`patches28.json`）／**一部**／**直さない**（理由）。原文の片は40字以内。OK の所見は数だけ（記録は git の外）', '']
    cnt = collections.Counter()
    sev = collections.Counter()
    lines = []
    undecided = []
    for x in bad:
        fid = x['id']
        if fid in partial:
            how = '一部（%s）' % partial[fid]
            if fid in byf:
                how += '＝%s' % '・'.join(byf[fid])
            cnt['一部'] += 1
        elif fid in not_adopted:
            how = '直さない（%s）' % not_adopted[fid]
            cnt['直さない'] += 1
        elif fid in byf:
            how = '直した（%s）' % '・'.join(byf[fid])
            cnt['直した'] += 1
        else:
            how = '🔴 扱いが決まっていない'
            undecided.append(fid)
        sev[x.get('severity')] += 1
        frag = ('`%s`' % x['fragment'][:40]) if x.get('fragment') else ''
        lines.append('| %s | %s | %s | %s／%s | %s | %s %s | %s |' % (
            fid, x.get('severity'), x.get('cut'), x.get('aspect'), x.get('kind'),
            (x.get('text') or '').replace('|', '／')[:60], (x.get('source') or '')[:40].replace('|', '／'), frag.replace('|', '／'),
            how.replace('|', '／')))
    out.append('## 数')
    out.append('- 所見 %d件＝OK %d・OK 以外 %d（🔴 %d・⚠️ %d・・ %d）' % (len(rows), len(ok), len(bad), sev['🔴'], sev['⚠️'], sev['・']))
    out.append('- 扱い＝直した %d・一部 %d・直さない %d・決まっていない %d' % (cnt['直した'], cnt['一部'], cnt['直さない'], len(undecided)))
    per = collections.Counter(x['id'].split('-')[0] for x in rows)
    per_bad = collections.Counter(x['id'].split('-')[0] for x in bad)
    out.append('- 係ごと（所見／OK 以外）＝' + '・'.join('%s %d／%d' % (g, per[g], per_bad[g]) for g in GROUPS + ('P', 'R1', 'R2'))
               + '（P＝④\' の本人の通し読み・R＝当て直し＝第2版の直しを別の目で原文に）')
    out.append('- 差し替え %d件（カット %d・§ と章の外 %d）' % (len(patches), sum(1 for p in patches if p['cut'].startswith('c')),
                                                   sum(1 for p in patches if not p['cut'].startswith('c'))))
    out += ['', '## OK 以外の所見（🔴→⚠️→・）', '',
            '| id | 重さ | カット | 面／型 | 台本の句 | 原文（出典・片） | 扱い |', '|---|---|---|---|---|---|---|'] + lines
    open(os.path.join(HERE, 'ledger28.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out[5:9]))
    print('→', os.path.join(HERE, 'ledger28.md'))
    if undecided:
        print('🔴 扱いが決まっていない:', ' '.join(undecided))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
