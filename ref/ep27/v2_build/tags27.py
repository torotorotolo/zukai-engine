# -*- coding: utf-8 -*-
"""27本目④'：出典の欄の札を全部数える（ルール 4'-9＝台帳に無い資料を指す札・1カットしか使わない札は要注意）。読むだけ。

  python -P ref/ep27/v2_build/tags27.py ref/ep27/daihon_v1.md

札の形：T年月日-番号（TOS）／O・OAB・G・N・共・西日本＋日付／警察庁・県警（頁・YT・X）／そのほかの媒体名（NEWSポストセブン・ABEMA ほか）。
出すもの：札ごとの使ったカット・1カットだけの札・TOS の札で sources.md と ① の記号に無いもの（sources.md の本文に札の字が無い）。
"""
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
CUT = re.compile(r'^\*\*(c\d{3})\*\*')
PATS = [
    ('TOS', re.compile(r'T\d{6}-\d{2}')),
    ('局と日付', re.compile(r'(?:OAB|O|G|N|共|西日本)\s?\d{4}-\d{2}-\d{2}')),
    ('警察', re.compile(r'警察庁[^\s・（`]*|県警(?:YT-[A-C]|X|の頁|頁)?')),
    ('媒体', re.compile(r'NEWSポストセブン[^\s・（`]*|ABEMA[^\s・（`]*|弁護士JP[^\s・（`]*|弁護士ドットコム[^\s・（`]*|J-CAST[^\s・（`]*|'
                       r'日経[^\s・（`]*|共同[^\s・（`]*|coki[^\s・（`]*|FNN[^\s・（`]*|日テレ[^\s・（`]*|読売[^\s・（`]*|朝日[^\s・（`]*|NHK[^\s・（`]*')),
]


def main(path):
    on, cur, src = False, None, {}
    for ln in open(path, encoding='utf-8'):
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        m = CUT.match(ln) if on else None
        if m:
            parts = ln.rstrip('\n').split(' ／ ')
            src[m.group(1)] = parts[2] if len(parts) > 2 else ''
    uses = collections.defaultdict(list)
    for c, s in src.items():
        s2 = re.sub(r'`[^`]*`', '', s)              # 原文の片の中の字は札に数えない
        for kind, p in PATS:
            for t in set(p.findall(s2)):
                uses[(kind, t.strip())].append(c)
    srcmd = open(os.path.join(EP, 'sources.md'), encoding='utf-8').read()
    empty = [c for c, s in src.items() if s.strip() in ('', '—')]
    print('カット %d・出典の欄が空か「—」 %d %s' % (len(src), len(empty), ' '.join(empty)))
    print('札 %d種' % len(uses))
    for (kind, t), cs in sorted(uses.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        mark = ''
        if len(cs) == 1:
            mark += ' ・1カットだけ'
        if kind == 'TOS' and t not in srcmd:
            mark += ' ・sources.md に札の字なし'
        print('  %s %s ×%d %s%s' % (kind, t, len(cs), ' '.join(cs), mark))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
