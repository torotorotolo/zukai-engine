# -*- coding: utf-8 -*-
"""26本目④'：出典の欄の札（資料の記号）を全部数える（ルール 4'-9＝台帳に無い資料を指す札・1カットしか使わない札は要注意）。

  python -P ref/ep26/v2_build/tags26.py ref/ep26/daihon_v1.md

数えるもの：§4 の全カットの出典の欄（`**cNNN** ／ 画 ／ 出典`）の記号（G1〜G7・T1〜T3・N1〜N3・U1・A1・legend・materials など）。
sources.md §1 の表の記号と突き合わせ、台帳に無い記号・1カットだけの記号・出典の欄が空のカット・頁の無い G の札を出す。
"""
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
EP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*\s*(?:🔧\s*)?／(.*)$')
TOK = re.compile(r'(?<![A-Za-z0-9])(G[1-9]|T[1-9]|N[1-9]|U[1-9]|A[1-9])(?![0-9A-Za-z])')


def ledger_tags():
    tags = set()
    for ln in open(os.path.join(EP, 'sources.md'), encoding='utf-8'):
        m = re.match(r'^\|\s*\**([GTNUA][1-9])\**\s*\|', ln)
        if m:
            tags.add(m.group(1))
    return tags


def main(md):
    known = ledger_tags()
    on, per = False, collections.defaultdict(list)
    empty, nopage, extra = [], [], collections.defaultdict(list)
    for ln in open(md, encoding='utf-8'):
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        m = CUT.match(ln) if on else None
        if not m:
            continue
        cut, rest = m.group(1), m.group(2)
        parts = rest.split(' ／ ')
        src = parts[-1] if len(parts) >= 2 else ''
        src_wo_q = re.sub(r'`[^`]*`', '', src)
        if not src_wo_q.strip():
            empty.append(cut)
        toks = TOK.findall(src_wo_q)
        for t in sorted(set(toks)):
            per[t].append(cut)
        for t in ('legend', 'materials', 'kousei', 'sources'):
            if t in src_wo_q:
                extra[t].append(cut)
        for mm in re.finditer(r'(?<![A-Za-z0-9])(G[1-7])(?![0-9A-Za-z])(?!\s*(?:p\.?\s*\d|送り状|全文|\d))', src_wo_q):
            if mm.group(1) not in ('G4', 'G5', 'G6'):
                nopage.append(f'{cut}:{mm.group(1)}')
    print('台帳（sources.md §1）の記号:', ' '.join(sorted(known)))
    print('札ごとのカット数:')
    for t in sorted(per, key=lambda x: (x[0], int(x[1:]))):
        flag = '' if t in known else '  🔴 台帳に無い'
        one = '  ⚠️ 1カットだけ' if len(per[t]) == 1 else ''
        print(f'  {t} {len(per[t])}{flag}{one}  {" ".join(per[t][:12])}{" …" if len(per[t]) > 12 else ""}')
    unused = sorted(known - set(per))
    print('台帳にあるが使っていない記号:', ' '.join(unused) or 'なし')
    for t, cs in extra.items():
        print(f'記号でない札「{t}」: {len(cs)}カット {" ".join(cs)}')
    print('出典の欄が空のカット:', ' '.join(empty) or 'なし')
    print('頁の無い G の札（G4〜G6 は全文なので除く）:', ' '.join(nopage) or 'なし')


if __name__ == '__main__':
    main(sys.argv[1])
