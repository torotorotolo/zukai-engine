# -*- coding: utf-8 -*-
"""30本目④'：出典の欄の札を全部数える（ルール 4'-9＝台帳に無い資料を指す札・1カットしか使わない札は要注意）。読むだけ（29本目 tags29.py を写し、札の形を30本目に替えた）。

  python -P ref/ep30/v2_build/tags30.py ref/ep30/daihon_v1.md

札の形：白2・白3・白5／判T・判A〜判E／国〈番号〉/〈発言〉／手助役・手運転士・手警部補・手機関員・手院長／声代表・声松本・声事務長・声兄・声丸ノ内／
公・特／消a・消b・東消／犯白・給a・給b／無線・OH／窓。
出すもの：札ごとの使ったカット・1カットだけの札・資料の置き場（quotes30.DOCS と src/kokkai/）に無い札・出典の欄が空か「―」のカット。
"""
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
SRC = os.path.join(EP, 'src')
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
TAG = re.compile(r'国\d{6,}X\d+/\d+|白[235]|判[TABCDE]|手(?:助役|運転士|警部補|機関員|院長)|声(?:代表|松本|事務長|兄|丸ノ内)|公|特|消[ab]|東消|犯白|給[ab]|無線|OH|窓')
KNOWN = {'白2', '白3', '白5', '判T', '判A', '判B', '判C', '判D', '判E', '手助役', '手運転士', '手警部補', '手機関員', '手院長',
         '声代表', '声松本', '声事務長', '声兄', '声丸ノ内', '公', '特', '消a', '消b', '東消', '犯白', '給a', '給b', '無線', 'OH', '窓'}


def main(path):
    on, src = False, {}
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
        s2 = re.sub(r'（[^（）]*）', '（）', s2)      # 括弧の中の説明の字も札に数えない
        for t in set(TAG.findall(s2)):
            uses[t].append(c)
    empty = [c for c, s in src.items() if s.strip() in ('', '—', '―') or s.strip().startswith('―')]
    print('カット %d・出典の欄が空か「―」 %d %s' % (len(src), len(empty), ' '.join(empty)))
    print('札 %d種' % len(uses))
    bad = 0
    for t, cs in sorted(uses.items()):
        mark = ''
        if len(cs) == 1:
            mark += ' ・1カットだけ'
        if t.startswith('国'):
            f = t[1:].replace('/', '_') + '.txt'
            if not os.path.exists(os.path.join(SRC, 'kokkai', f)):
                mark += ' 🔴 置き場に無い'
                bad += 1
        elif t not in KNOWN:
            mark += ' 🔴 台帳に無い札'
            bad += 1
        print('%s %d%s  %s' % (t, len(cs), mark, ' '.join(sorted(cs)[:40])))
    print('置き場か台帳に無い札 %d' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
