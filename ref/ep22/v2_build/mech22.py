# -*- coding: utf-8 -*-
"""22本目④'：呼び名をそろえる直し（行ごと）を、係と G0 の直しのあとの台本から作る → patches_mech.json（21本目 gen_g0.py --mech の考え方）。

  python ref/ep22/v2_build/mech22.py <試し組みの台本>

そろえ方（G0-M・2026-10-14）：語りの「アメリカの運輸安全委員会」→「米運輸安全委員会」、「アメリカ沿岸警備隊」→「米沿岸警備隊」。
初出の c102（アメリカ沿岸警備隊）と c203（3つの報告書の紹介）だけは「アメリカ」のまま。
なぜ：語りに「米沿岸警備隊」29回と「アメリカ沿岸警備隊」が混ざっていた（G7-022）＋字数（1回目の試し組みで上限を444字超えた）。
係の直しのあとの行に当てる（order 90）＝第1版の行でなく、組んだあとの行から作る。
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = {'c102', 'c203'}
RULES = [('アメリカの運輸安全委員会', '米運輸安全委員会'), ('アメリカ沿岸警備隊', '米沿岸警備隊')]
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')


def main(path):
    out, cur, on = [], None, False
    n = 0
    for ln in open(path, encoding='utf-8').read().split('\n'):
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        m = CUT.match(ln) if on else None
        if m:
            cur = m.group(1)
            continue
        if not (cur and ln.startswith('> ')) or cur in KEEP:
            continue
        new = ln
        for a, b in RULES:
            new = new.replace(a, b)
        if new != ln:
            n += 1
            out.append({'id': 'G0-M%02d' % n, 'cut': cur, 'old': ln, 'new': new, 'order': 90,
                        'why': '呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）'})
    json.dump(out, open(os.path.join(HERE, 'patches_mech.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('patches_mech.json に %d 件' % len(out))


if __name__ == '__main__':
    main(sys.argv[1])
