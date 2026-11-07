# -*- coding: utf-8 -*-
"""31本目④'：第1版の語りにあって第2版の語りに無い語を、機械で一覧にする（30本目 c307 の型＝語を消して事実も消える、を全数で当てる・lost30.py を写した）。

  python -P ref/ep31/v2_build/lost31.py   → src/agents/wf31b/lost_words.txt（git の外）

語＝漢字・カタカナの2字以上のかたまりと、数字＋単位。語りの全体（聞き役を含む）で第2版に1度も出ない語だけ出す。カットごと。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build31_v2 import blocks  # noqa: E402

EP = os.path.dirname(HERE)
TOK = re.compile(r'[一-龥々ァ-ヶー]{2,}|[0-9][0-9,.]*[年月日時分秒人か本件回名両機度億万千円%]+')


def narr(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    out = {}
    for c, (a, b) in blocks(lines).items():
        out[c] = ' '.join(x[2:] for x in lines[a:b] if x.startswith('> '))
    return out


def main():
    a = sys.argv[1:]      # 🆕 --a 前の台本 --b 後の台本 --out 置き場（既定＝第1版→第2版・④ の直しの前後にも当てる）
    pa = a[a.index('--a') + 1] if '--a' in a else os.path.join(EP, 'daihon_v1.md')
    pb = a[a.index('--b') + 1] if '--b' in a else os.path.join(EP, 'daihon_v2.md')
    po = a[a.index('--out') + 1] if '--out' in a else os.path.join(EP, 'src', 'agents', 'wf31b', 'lost_words.txt')
    v1, v2 = narr(pa), narr(pb)
    all2 = ' '.join(v2.values())
    n = 0
    os.makedirs(os.path.dirname(po), exist_ok=True)
    with open(po, 'w', encoding='utf-8', newline='\n') as w:
        w.write('# 第1版の語りにあって、第2版の語りのどこにも無い語（カットごと）\n')
        for c in sorted(v1, key=lambda c: ('123456789abcd'.index(c[1]), c)):
            lost = []
            for t in TOK.findall(v1[c]):
                if t not in all2 and t not in lost:
                    lost.append(t)
            if lost:
                w.write('%s: %s\n' % (c, '・'.join(lost)))
                n += len(lost)
    print('消えた語 %d → src/agents/wf31b/lost_words.txt' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
