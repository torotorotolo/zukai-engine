# -*- coding: utf-8 -*-
"""33本目④'：所見の台帳（1行1粗）を、係の記録と ④' の本人の所見と差し替え表から組む（手で写さない・32本目 ledger32.py を写した）。

  python -P ref/ep33/v2_build/ledger33.py [--pre]   → v2_build/ledger33.md（--pre は直す前に一度出す版＝git の外 src/agents/wf33b/ledger33_pre.md）

入力＝git の外 src/agents/wf33b/findings_G1〜G6.json（照合と通し読みの係）・findings_R*.json（当て直しの係）／
      v2_build/own33.json（④' の本人＝P の所見）／v2_build/patches33.json（各差し替えの from＝もとの所見の番号）／
      v2_build/ledger_ovr.json（扱いの上書き＝{"G2-003": {"d": "直さない|一部|後の工程へ|済み|承認①へ", "why": "…"}}）
扱い＝直した（差し替えの id）／一部（理由）／直さない（理由）／後の工程へ（理由）／承認①へ（理由）／済み（別の差し替えで済んだ）。
🔴・⚠️ の所見で扱いが決まっていないものが1件でもあれば止める（exit 1・--pre を除く）。台本の字・原文の片だけを載せる（名前は載せない＝namecheck33.py が当てる）。
"""
import collections
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents', 'wf33b')
SEV = {'🔴': 0, '⚠️': 1, '・': 2}


def load(p, default):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default


def esc(s):
    return (s or '').replace('|', '｜').replace('\n', '⏎').strip()


def short(s, n):
    s = esc(s)
    return s if len(s) <= n else s[:n - 1] + '…'


def main():
    pre = '--pre' in sys.argv
    rows = []
    for p in sorted(glob.glob(os.path.join(AG, 'findings_G*.json'))) + sorted(glob.glob(os.path.join(AG, 'findings_R*.json'))):
        rows += load(p, [])
    rows += load(os.path.join(HERE, 'own33.json'), [])
    patches = load(os.path.join(HERE, 'patches33.json'), [])
    ovr = load(os.path.join(HERE, 'ledger_ovr.json'), {})
    by_from = collections.defaultdict(list)
    for p in patches:
        for f in p.get('from') or []:
            by_from[f].append(p['id'])
    out = ['# 33本目 ④' + "'" + ' 所見の台帳（ledger33.py が係の記録と差し替え表から組む・手で直さない）', '',
           '- 重さ＝🔴（原文と違う事実・帰属の切れ・線）／⚠️（意味のずれ・限定の落ち・分かりにくさ）／・（言い回し）。扱い＝直した（差し替えの id）・一部・直さない・後の工程へ・承認①へ・済み',
           '- 係＝G1 冒頭〜第2章・G2 第3〜4章・G3 第5章・G4 第6〜8章・G5 第9〜11章と§・G6 通し読み・R1〜R2 当て直し（別の目）・P ④' + "'" + ' の本人', '',
           '| id | 重さ | カット | 面・型 | 所見 | 扱い |', '|---|---|---|---|---|---|']
    undecided = []
    cnt = collections.Counter()
    disp = collections.Counter()
    rows.sort(key=lambda x: (SEV.get(x.get('severity'), 9), x.get('cut', ''), x.get('id', '')))
    for x in rows:
        fid = x.get('id', '?')
        sev = x.get('severity', '・')
        cnt[sev] += 1
        if fid in ovr:
            d = ovr[fid]
            how = '%s（%s）' % (d.get('d'), d.get('why', '')) if d.get('why') else d.get('d')
            if by_from.get(fid):
                how = '直した %s・%s' % ('・'.join(by_from[fid]), how)
            disp[d.get('d')] += 1
        elif by_from.get(fid):
            how = '直した %s' % '・'.join(by_from[fid])
            disp['直した'] += 1
        else:
            how = '（未決）'
            if sev in ('🔴', '⚠️'):
                undecided.append(fid)
            disp['未決'] += 1
        msg = short(x.get('problem'), 150)
        if x.get('text'):
            msg = '「%s」 %s' % (short(x.get('text'), 40), msg)
        out.append('| %s | %s | %s | %s/%s | %s | %s |' % (fid, sev, esc(x.get('cut')), x.get('aspect', ''), short(x.get('kind'), 12), msg, short(how, 120)))
    out.insert(4, '- 数＝所見 %d（%s）・扱い %s' % (len(rows), ' '.join('%s%d' % kv for kv in sorted(cnt.items(), key=lambda kv: SEV.get(kv[0], 9))),
                                                 '・'.join('%s %d' % kv for kv in disp.most_common())))
    dest = os.path.join(AG, 'ledger33_pre.md') if pre else os.path.join(HERE, 'ledger33.md')
    with open(dest, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    print('台帳 %d行（%s）・扱い %s → %s' % (len(rows), dict(cnt), dict(disp), dest))
    if undecided and not pre:
        print('🔴 扱いの決まっていない 🔴・⚠️ %d件: %s' % (len(undecided), ' '.join(undecided[:40])))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
