# -*- coding: utf-8 -*-
"""31本目④'：Workflow の記録（journal.jsonl）から、係の返した結果を git の外へ取り出す（親の文脈に全文を流さないため・30本目 wfx30.py を写した）。

  python -P ref/ep31/v2_build/wfx31.py <journal.jsonl> check    # 照合の係 → src/agents/wf31b/findings_Gn.json・meta_Gn.json・bad_all.txt
  python -P ref/ep31/v2_build/wfx31.py <journal.jsonl> fix      # 直す係 → src/agents/wf31b/fix_Fn.json
  python -P ref/ep31/v2_build/wfx31.py <journal.jsonl> review   # 当て直しの係 → src/agents/wf31b/findings_Rn.json・meta_Rn.json・bad_R.txt
  python -P ref/ep31/v2_build/wfx31.py <journal.jsonl> final    # 最後の点検の係 → src/agents/wf31b/findings_Cn.json・meta_Cn.json・bad_C.txt

ラベル（check:G3 …・fix:F3 …・review:R1 …・final:C1 …）で係を決める。標準出力は件数と当て残しだけ（中身は bad_*.txt を必要な所だけ読む）。
⚠️ 係の直しの案の行頭の「>」は「&gt;」に化けて返る（④ で分かった）＝ html.unescape で戻す。形が読めなければ止める（fail closed）。
"""
import collections
import html
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
OUT = os.path.join(EP, 'src', 'agents', 'wf31b')
SEV = {'🔴': 0, '⚠️': 1, '・': 2}
CUTS = re.compile(r'c[0-9a-d]\d{2}')


def unesc(x):
    if isinstance(x, str):
        return html.unescape(x)
    if isinstance(x, list):
        return [unesc(y) for y in x]
    if isinstance(x, dict):
        return {k: unesc(v) for k, v in x.items()}
    return x


def entries(path):
    label, out = {}, []
    for ln in open(path, encoding='utf-8'):
        if not ln.strip():
            continue
        d = json.loads(ln)
        if d.get('type') == 'started':
            label[d.get('key')] = d.get('label')
        elif d.get('type') == 'result':
            out.append((label.get(d.get('key')), unesc(d.get('result'))))
    return out


def all_cuts():
    return re.findall(r'^\*\*(c[0-9a-d]\d{2})\*\*', open(os.path.join(OUT, 'cuts_v1.txt'), encoding='utf-8').read(), re.M)


def dump_findings(kind, rows, bad_name):
    os.makedirs(OUT, exist_ok=True)
    bad_lines = []
    got = {}
    for lab, r in rows:
        if not lab or not lab.startswith(kind + ':'):
            continue
        if not isinstance(r, dict) or 'findings' not in r:
            print('🔴 形が読めない:', lab)
            return 2
        g = lab.split(':', 1)[1].split(' ')[0]
        got[g] = r
        fs = r['findings']
        for k, x in enumerate(fs, 1):
            x['id'] = '%s-%03d' % (g, k)
            x.setdefault('verdict', 'ずれ')
        json.dump(fs, open(os.path.join(OUT, 'findings_%s.json' % g), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        meta = {k: r.get(k) for k in ('group', 'covered_cuts', 'nets', 'opinions', 'unreached', 'leaks', 'notes')}
        json.dump(meta, open(os.path.join(OUT, 'meta_%s.json' % g), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        v = collections.Counter(x.get('verdict') for x in fs)
        s = collections.Counter(x.get('severity') for x in fs if x.get('verdict') != 'OK')
        print('%s 所見 %d（%s）・重さ %s・網 %d・開けなかった %d・線の申告 %d' % (
            g, len(fs), dict(v), dict(s), len(r.get('nets') or []), len(r.get('unreached') or []), len(r.get('leaks') or [])))
        for x in fs:
            if x.get('verdict') != 'OK':
                bad_lines.append(x)
    bad_lines.sort(key=lambda x: (SEV.get(x.get('severity'), 9), x.get('cut', ''), x['id']))
    with open(os.path.join(OUT, bad_name), 'w', encoding='utf-8', newline='\n') as f:
        for x in bad_lines:
            f.write('%s %s %s [%s/%s・%s] 「%s」 ⇐ %s `%s` ｜ 案: %s → %s ｜ %s\n' % (
                x['id'], x.get('severity'), x.get('cut'), x.get('aspect'), x.get('kind'), x.get('verdict'),
                x.get('text'), x.get('source'), x.get('fragment'), x.get('fix_old'), x.get('fix_new'), x.get('why')))
    print('OK 以外 %d件 → %s' % (len(bad_lines), os.path.join(OUT, bad_name)))
    if kind == 'check':
        cov = set()
        for g, r in got.items():
            if g != 'G7':
                cov |= set(r.get('covered_cuts') or []) | {c for x in r['findings'] for c in CUTS.findall(x.get('cut', ''))}
        miss = [c for c in all_cuts() if c not in cov]
        print('章ごとの係の当て残しカット %d: %s' % (len(miss), ' '.join(miss)))
    return 0


def dump_fix(rows):
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for lab, r in rows:
        if not lab or not lab.startswith('fix:'):
            continue
        if not isinstance(r, dict) or 'patches' not in r:
            print('🔴 形が読めない:', lab)
            return 2
        g = lab.split(':', 1)[1].split(' ')[0]
        json.dump(r, open(os.path.join(OUT, 'fix_%s.json' % g), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('%s 差し替え %d・扱い %d・字の増減 %s・E %s・線の申告 %d' % (
            g, len(r.get('patches') or []), len(r.get('dispositions') or []), r.get('char_delta'), r.get('try_errors'), len(r.get('leaks') or [])))
        n += 1
    print('直す係', n)
    return 0 if n else 2


def main(path, kind):
    rows = entries(path)
    if kind == 'check':
        return dump_findings('check', rows, 'bad_all.txt')
    if kind == 'review':
        return dump_findings('review', rows, 'bad_R.txt')
    if kind == 'final':
        return dump_findings('final', rows, 'bad_C.txt')
    if kind == 'fix':
        return dump_fix(rows)
    print('kind は check・fix・review・final')
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
