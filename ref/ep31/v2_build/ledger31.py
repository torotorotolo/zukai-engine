# -*- coding: utf-8 -*-
"""31本目④'：所見の台帳（1行1粗）を、係の記録と ④' の本人の所見と差し替え表から組む（手で写さない・30本目 ledger30.py を写した）。

  python -P ref/ep31/v2_build/ledger31.py [--pre]   → v2_build/ledger31.md（--pre は直す前に一度出す版＝git の外 src/agents/wf31b/ledger31_pre.md）

入力＝git の外 src/agents/wf31b/findings_G1〜G7.json（照合の係）・findings_R*.json（当て直し）・findings_C*.json（最後の点検）／
      v2_build/own31.json（④' の本人＝P）／v2_build/patches31.json（各差し替えの from＝もとの所見の番号）／
      v2_build/ledger_ovr.json（扱いの上書き＝not_adopted：直さない・partial：一部・moved：映像方針や後の工程へ・done：別の差し替えで済み）／fix_F*.json の dispositions
扱い＝直した（差し替えの id）／一部（理由）／直さない（理由）／後の工程へ（理由）。OK 以外の所見で扱いが決まっていないものが1件でもあれば止める（exit 1・--pre を除く）。
台本の字・原文の片だけを載せる。名前は載せない（namecheck31.py が当てる）。
"""
import collections
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents', 'wf31b')
SEV = {'🔴': 0, '⚠️': 1, '・': 2}
GROUPS = ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'R1', 'R2', 'R3', 'R4', 'C1', 'C2')


def load():
    rows = []
    for g in GROUPS:
        p = os.path.join(AG, 'findings_%s.json' % g)
        if os.path.exists(p):
            rows += json.load(open(p, encoding='utf-8'))
    own = os.path.join(HERE, 'own31.json')
    if os.path.exists(own):
        rows += json.load(open(own, encoding='utf-8'))
    return rows


def dispositions():
    out = {}
    for p in sorted(glob.glob(os.path.join(AG, 'fix_F*.json'))):
        for d in json.load(open(p, encoding='utf-8')).get('dispositions') or []:
            out[d['id']] = d
    return out


def ids(xs):
    """差し替えの id の並び（多いときは頭の8つ＋数＝扱いの欄を字数で切らない・C2-025）。"""
    return '・'.join(xs) if len(xs) <= 8 else '・'.join(xs[:8]) + '…ほか%d件（計%d件）' % (len(xs) - 8, len(xs))


def main():
    pre = '--pre' in sys.argv
    rows = load()
    pp = os.path.join(HERE, 'patches31.json')
    patches = json.load(open(pp, encoding='utf-8')) if os.path.exists(pp) else []
    ovr_p = os.path.join(HERE, 'ledger_ovr.json')
    ovr = json.load(open(ovr_p, encoding='utf-8')) if os.path.exists(ovr_p) else {}
    not_adopted, partial, moved, done_o = ovr.get('not_adopted', {}), ovr.get('partial', {}), ovr.get('moved', {}), ovr.get('done', {})
    disp = dispositions()
    byf = collections.defaultdict(list)
    for p in patches:
        for f in p.get('from', []):
            byf[f].append(p['id'])
    ok = [x for x in rows if x.get('verdict') == 'OK']
    bad = [x for x in rows if x.get('verdict') != 'OK']
    bad.sort(key=lambda x: (SEV.get(x.get('severity'), 9), x.get('cut', ''), x['id']))
    out = ['# 31本目 ④\' 所見の台帳（ledger31.py が組む・手で直さない）', '',
           '- 入力＝係の記録 `src/agents/wf31b/findings_*.json`（git の外）＋④\' の本人の所見 `own31.json`（P）＋差し替え表 `patches31.json`＋扱いの上書き `ledger_ovr.json`＋直す係の扱い `fix_F*.json`（git の外）',
           '- 扱い＝**直した**（差し替えの id＝`patches31.json`）／**一部**／**直さない**（理由）／**後の工程へ**（理由）。原文の片は40字以内', '']
    cnt = collections.Counter()
    sev = collections.Counter()
    lines = []
    undecided = []
    for x in bad:
        fid = x['id']
        d = disp.get(fid) or {}
        if fid in moved:
            how = '後の工程へ（%s）' % moved[fid]
            cnt['後の工程へ'] += 1
        elif fid in not_adopted:
            how = '直さない（%s）' % not_adopted[fid]
            cnt['直さない'] += 1
        elif fid in partial:
            how = '一部（%s）' % partial[fid]
            if fid in byf:
                how += '＝%s' % ids(byf[fid])
            cnt['一部'] += 1
        elif fid in byf:
            how = '直した（%s）' % ids(byf[fid])
            cnt['直した'] += 1
        elif fid in done_o:
            how = '直した（別の差し替えで＝%s）' % done_o[fid]
            cnt['直した'] += 1
        elif d.get('v') == '採らない':
            how = '直さない（%s）' % d.get('why', '')
            cnt['直さない'] += 1
        elif d.get('v') == '一部':
            how = '一部（%s）' % d.get('why', '')
            cnt['一部'] += 1
        elif d.get('v') == '後の工程へ':
            how = '後の工程へ（%s）' % d.get('why', '')
            cnt['後の工程へ'] += 1
        elif d.get('v') == '済み':
            how = '直した（別の差し替えで＝%s）' % d.get('why', '')
            cnt['直した'] += 1
        else:
            how = '🔴 扱いが決まっていない' if not pre else '（直す前）'
            undecided.append(fid)
        sev[x.get('severity')] += 1
        frag = ('`%s`' % x['fragment'][:40].replace('`', '')) if x.get('fragment') else ''
        lines.append('| %s | %s | %s | %s／%s | %s | %s %s | %s |' % (
            fid, x.get('severity'), x.get('cut'), x.get('aspect'), (x.get('kind') or '')[:30],
            (x.get('text') or '').replace('|', '／').replace('\n', ' ')[:60], (x.get('source') or '')[:40].replace('|', '／'),
            frag.replace('|', '／'), how.replace('|', '／').replace('\n', ' ')[:260]))
    out.append('## 数')
    out.append('- 所見 %d件＝OK %d・OK 以外 %d（🔴 %d・⚠️ %d・・ %d）' % (len(rows), len(ok), len(bad), sev['🔴'], sev['⚠️'], sev['・']))
    out.append('- 扱い＝直した %d・一部 %d・直さない %d・後の工程へ %d・決まっていない %d' % (
        cnt['直した'], cnt['一部'], cnt['直さない'], cnt['後の工程へ'], len(undecided)))
    per = collections.Counter(x['id'].split('-')[0] for x in rows)
    per_bad = collections.Counter(x['id'].split('-')[0] for x in bad)
    out.append('- 係ごと（所見／OK 以外）＝' + '・'.join('%s %d／%d' % (g, per[g], per_bad[g]) for g in GROUPS + ('P',) if per[g])
               + '（G＝章ごとの照合と通し読み・P＝④\' の本人・R＝当て直し・C＝最後の点検）')
    out.append('- 差し替え %d件（カット %d・§ と章の外 %d）' % (len(patches), sum(1 for p in patches if p['cut'].startswith('c')),
                                                   sum(1 for p in patches if not p['cut'].startswith('c'))))
    out += ['', '## OK 以外の所見（🔴→⚠️→・）', '',
            '| id | 重さ | カット | 面／型 | 台本の句 | 原文（出典・片） | 扱い |', '|---|---|---|---|---|---|---|'] + lines
    text = '\n'.join(out) + '\n'
    dst = os.path.join(AG, 'ledger31_pre.md') if pre else os.path.join(HERE, 'ledger31.md')
    open(dst, 'w', encoding='utf-8', newline='\n').write(text)
    print('\n'.join(out[5:9]))
    print('→', dst)
    if undecided and not pre:
        print('🔴 扱いが決まっていない:', ' '.join(undecided))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
