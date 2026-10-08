# -*- coding: utf-8 -*-
"""20本目④'：台本から「語りと聞き役の行だけ」を抜く（通し読みの係に全文の画と出典の欄を読ませない・2026-10-08）。

  python ref/ep20/v2_build/narr20.py ref/ep20/daihon_v1.md > 出力.txt

1行＝`cNNN  秒  [語|Q]  文`。秒＝そのカットの始まり（句読点なし÷365 の積み上げ・m20 の②と同じ数え方）。
章の見出し（### …）もそのまま出す。役割（質問／まとめ／反応）は v1_build/roles.tsv から添える。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
PUNCT = '、。？！「」（）・'
CUT = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*')


def nopunct(s):
    return ''.join(ch for ch in s if ch not in PUNCT and not ch.isspace())


def main(md):
    roles = {}
    rp = os.path.join(os.path.dirname(os.path.abspath(md)), 'v1_build', 'roles.tsv')
    if os.path.exists(rp):
        for ln in open(rp, encoding='utf-8'):
            if ln.startswith('#') or not ln.strip():
                continue
            c, r, t = ln.rstrip('\n').split('\t')
            roles[(c, t)] = r
    t = open(md, encoding='utf-8').read()
    body = t[t.index('## 4. 台本'):t.index('## 5. ')]
    sec = 0.0
    cur = None
    for ln in body.split('\n'):
        if ln.startswith('### '):
            print('\n' + ln)
            continue
        m = CUT.match(ln)
        if m:
            cur = m.group(1)
            first = True
            continue
        if cur and ln.startswith('>'):
            s = ln[1:].strip()
            isq = s.startswith('Q:')
            txt = s[2:].strip() if isq else s
            tag = 'Q:' + roles.get((cur, txt), '?') if isq else '語'
            print('%s  %6.1f  %s  %s' % (cur if first else '    ', sec, tag, txt))
            first = False
            sec += len(nopunct(txt)) / 365 * 60
    print('\n== 合計 %.1f 秒（句読点なし÷365）' % sec)


if __name__ == '__main__':
    main(sys.argv[1])
