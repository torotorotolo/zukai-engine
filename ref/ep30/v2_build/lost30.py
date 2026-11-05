# -*- coding: utf-8 -*-
"""30本目④'：第1版の語りにあって第2版の語りに無い語を、機械で一覧にする（c307 の型＝語を消して事実も消える、を全数で当てる）。

  python -P ref/ep30/v2_build/lost30.py   → src/agents/wf30c/lost_words.txt（git の外）

語＝漢字・カタカナの2字以上のかたまりと、数字＋単位。語りの全体（聞き役を含む）で第2版に1度も出ない語だけ出す。カットごと。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build30_v2 import blocks  # noqa: E402

EP = os.path.dirname(HERE)
TOK = re.compile(r'[一-龥々ァ-ヶー]{2,}|[0-9][0-9,.]*[年月日時分秒人か本件回名両着床隊億万千%]+')


def narr(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    out = {}
    for c, (a, b) in blocks(lines).items():
        out[c] = ' '.join(x[2:] for x in lines[a:b] if x.startswith('> '))
    return out


def main():
    v1, v2 = narr(os.path.join(EP, 'daihon_v1.md')), narr(os.path.join(EP, 'daihon_v2.md'))
    all2 = ' '.join(v2.values())
    n = 0
    with open(os.path.join(EP, 'src', 'agents', 'wf30c', 'lost_words.txt'), 'w', encoding='utf-8', newline='\n') as w:
        w.write('# 第1版の語りにあって、第2版の語りのどこにも無い語（カットごと）\n')
        for c in sorted(v1, key=lambda c: ('123456789abcd'.index(c[1]), c)):
            lost = []
            for t in TOK.findall(v1[c]):
                if t not in all2 and t not in lost:
                    lost.append(t)
            if lost:
                w.write('%s: %s\n' % (c, '・'.join(lost)))
                n += len(lost)
    print('消えた語 %d' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
