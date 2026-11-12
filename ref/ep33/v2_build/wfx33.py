# -*- coding: utf-8 -*-
"""33本目④'：Workflow の記録（journal.jsonl）から、係の返した結果を git の外へ取り出す（親の文脈に全文を流さないため・32本目 wfx32.py を写した）。
  python -P ref/ep33/v2_build/wfx33.py <journal.jsonl> check    # 照合の係と通し読み → src/agents/wf33b/findings_Gn.json・meta_Gn.json・bad_all.txt
  python -P ref/ep33/v2_build/wfx33.py <journal.jsonl> review   # 当て直しの係 → src/agents/wf33b/findings_Rn.json・meta_Rn.json・bad_R.txt
ラベル（check:G3 …・review:R1 …）で係を決める。標準出力は件数と当て残しだけ（中身は bad_*.txt を要る所だけ読む）。
⚠️ 係の直しの案の行頭の「>」は「&gt;」に化けて返る＝ html.unescape で戻す。「⏎」は改行に戻す。形が読めなければ止める（fail closed）。
名前は書かない約束だが、念のため bad_*.txt に書く前に名前の網（src/names_private.txt・names_commons.txt の4字以上の語）で伏せる（〈名前の網〉）＝伏せた数を出す。
"""
import collections
import html
import json
import os
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
SRC = os.path.join(EP, 'src')
OUT = os.path.join(SRC, 'agents', 'wf33b')
SEV = {'🔴': 0, '⚠️': 1, '・': 2}
CUTS = re.compile(r'c[0-9a-c]\d{2}')


def net():
    words = []
    for p in ('names_private.txt', 'names_commons.txt'):
        fp = os.path.join(SRC, p)
        if os.path.exists(fp):
            words += [w.strip() for w in open(fp, encoding='utf-8') if w.strip() and not w.startswith('#') and len(w.strip()) >= 4]
    if not words:
        return None
    words.sort(key=len, reverse=True)
    return re.compile('|'.join(re.escape(w) for w in words), re.I)


RX = net()
MASKED = [0]


def unesc(x):
    if isinstance(x, str):
        return html.unescape(x).replace('⏎', '\n')
    if isinstance(x, list):
        return [unesc(y) for y in x]
    if isinstance(x, dict):
        return {k: unesc(v) for k, v in x.items()}
    return x


def mask(s):
    s = str(s or '')
    if RX is None:
        return s
    t, n = RX.subn('〈名前の網〉', s)
    MASKED[0] += n
    return t


def entries(path):
    label, out = {}, []
    for ln in open(path, encoding='utf-8'):
        if not ln.strip():
            continue
        d = json.loads(ln)
        if d.get('type') == 'started':
            label[d.get('key')] = d.get('label')
        elif 'result' in d:
            r = d.get('result')
            if isinstance(r, str):
                try:
                    r = json.loads(r)
                except Exception:
                    pass
            out.append((label.get(d.get('key')) or d.get('label'), unesc(r)))
    return out


def all_cuts():
    return re.findall(r'^\*\*(c[0-9a-c]\d{2})\*\*', open(os.path.join(OUT, 'cuts_v1.txt'), encoding='utf-8').read(), re.M)


def dump(kind, rows, bad_name):
    if RX is None:
        print('🔴 名前の網が無い＝止める')
        return 2
    pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)  # 名前の網の空鳴りを避ける書き方
    bad, got = [], {}
    for lab, r in rows:
        if not lab or not lab.startswith(kind + ':'):
            continue
        if not isinstance(r, dict) or 'findings' not in r:
            print('🔴 形が読めない:', lab, type(r).__name__)
            return 2
        g = lab.split(':', 1)[1].split(' ')[0]
        got[g] = r
        fs = r['findings']
        for k, x in enumerate(fs, 1):
            x['id'] = '%s-%03d' % (g, k)
        json.dump(fs, open(os.path.join(OUT, 'findings_%s.json' % g), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        meta = {k: r.get(k) for k in ('group', 'covered_cuts', 'times', 'answers', 'unreached', 'leaks', 'notes')}
        json.dump(meta, open(os.path.join(OUT, 'meta_%s.json' % g), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        s = collections.Counter(x.get('severity') for x in fs)
        print('%s 所見 %d（%s）・時刻 %d・答え %d・当てられなかった %d・線の申告 %d・当てたカット %d' % (
            g, len(fs), ' '.join('%s%d' % (k, v) for k, v in sorted(s.items(), key=lambda kv: SEV.get(kv[0], 9))),
            len(r.get('times') or []), len(r.get('answers') or []), len(r.get('unreached') or []), len(r.get('leaks') or []),
            len(r.get('covered_cuts') or [])))
        bad.extend(fs)
    bad.sort(key=lambda x: (SEV.get(x.get('severity'), 9), x.get('cut', ''), x['id']))
    with open(os.path.join(OUT, bad_name), 'w', encoding='utf-8', newline='\n') as f:
        for x in bad:
            f.write(mask('%s %s %s [%s/%s] 「%s」 ⇐ %s `%s` ｜ %s ｜ 案: %s → %s（%s）\n' % (
                x['id'], x.get('severity'), x.get('cut'), x.get('aspect'), x.get('kind'),
                (x.get('text') or '').replace('\n', '⏎'), x.get('source'), (x.get('fragment') or '').replace('\n', ' '),
                (x.get('problem') or '').replace('\n', ' '),
                (x.get('fix_old') or '').replace('\n', '⏎'), (x.get('fix_new') or '').replace('\n', '⏎'), x.get('char_delta'))))
    print('所見 %d件 → %s・名前の網で伏せた %d' % (len(bad), os.path.join(OUT, bad_name), MASKED[0]))
    if kind == 'check':
        cov = set()
        for g, r in got.items():
            if g != 'G6':
                cov |= set(r.get('covered_cuts') or []) | {c for x in r['findings'] for c in CUTS.findall(x.get('cut', ''))}
        miss = [c for c in all_cuts() if c not in cov]
        print('照合の係の当て残しカット %d: %s' % (len(miss), ' '.join(miss)))
    return 0


def main(path, kind):
    rows = entries(path)
    if kind == 'check':
        return dump('check', rows, 'bad_all.txt')
    if kind == 'review':
        return dump('review', rows, 'bad_R.txt')
    print('kind は check・review')
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
