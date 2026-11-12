# -*- coding: utf-8 -*-
"""33本目④'：第1版の語りにあって第2版の語りに無い語を、機械で一覧にする（語を消して事実も消える、を全数で当てる・32本目 lost32.py を写した）。

  python -P ref/ep33/v2_build/lost33.py   → src/agents/wf33b/lost_words.txt（git の外）

語＝漢字・カタカナの2字以上のかたまりと、数字（＋単位の1〜3字）。語りの全体（聞き役を含む）で第2版に1度も出ない語だけ、カットごとに出す。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
OUT = os.path.join(EP, 'src', 'agents', 'wf33b', 'lost_words.txt')
CUT = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*')
WORD = re.compile(r'[一-龥々]{2,}|[ァ-ヶー]{2,}|[0-9][0-9,.]*[^\s0-9、。,.]{0,3}')


def speech(path):
    out, cur, order = {}, None, []
    text = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    s4 = text[text.index('## 4. 台本'):text.index('\n## 5.')]
    for l in s4.split('\n'):
        m = CUT.match(l)
        if m:
            cur = m.group(1)
            out[cur] = []
            order.append(cur)
            continue
        if l.startswith('#') or l.strip() == '---':
            cur = None
            continue
        if cur and l.startswith('>'):
            out[cur].append(re.sub(r'^>\s?(Q:\s)?', '', l))
    return out, order


def main():
    s1, o1 = speech(os.path.join(EP, 'daihon_v1.md'))
    s2, _ = speech(os.path.join(EP, 'daihon_v2.md'))
    all2 = '\n'.join('\n'.join(v) for v in s2.values())
    rows = []
    for c in o1:
        t1 = ''.join(s1[c])
        lost = []
        for w in WORD.findall(t1):
            if w not in all2 and w not in lost:
                lost.append(w)
        if lost:
            rows.append('%s\t%s' % (c, '・'.join(lost)))
    __import__('pathlib').Path(os.path.dirname(OUT)).mkdir(parents=True, exist_ok=True)  # 名前の網の空鳴りを避ける書き方
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 第1版の語りにあって第2版の語りに1度も出ない語（カットごと）\n' + '\n'.join(rows) + '\n')
    print('消えた語のあるカット %d → %s' % (len(rows), OUT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
