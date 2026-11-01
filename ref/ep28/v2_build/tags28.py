# -*- coding: utf-8 -*-
"""28本目④'：出典の欄の札を全部数える（ルール 4'-9＝台帳に無い資料を指す札・1カットしか使わない札は要注意）。読むだけ（27本目 tags27.py を写し、札の形を28本目に替えた）。

  python -P ref/ep28/v2_build/tags28.py ref/ep28/daihon_v1.md

札の形：会社＝第1〜5報・開示0928／1023a／1023b・QA Qn・PR0817／公的な機関（金融庁・個人情報保護委員会・e-Gov・統括室・官邸・警察庁・県警・国交省）／
報道と媒体（弁護士ドットコム・時事・NHK・毎日・読売・日経・TBS・テレビ朝日・共同・ITmedia・ABEMA・Impress ほか）／そのほか（JICC・ニコニコレンタカー・銀行・WESTER・X の投稿）。
出すもの：札ごとの使ったカット・1カットだけの札・sources.md の本文に札の字が無いもの。
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
    ('会社', re.compile(r'第[1-5]報|開示(?:0928|1023[ab])|QA ?Q\d{1,2}|PR0817|新着情報')),
    ('公的', re.compile(r'金融庁|個人情報保護委員会|e-Gov|統括室|官邸|警察庁|[静岡三重富山福岡]{2}県警|県警|国交省|国土交通省|総務省')),
    ('媒体', re.compile(r'弁護士ドットコム|弁護士側の頁|時事|NHK|毎日|読売|日経|TBS|テレビ朝日|テレ朝|共同|ITmedia(?: NEWS| ビジネス)?|ABEMA|Impress|'
                       r'FNN|NNN|日本テレビ|テレ東|乗りものニュース|Yahoo')),
    ('そのほか', re.compile(r'JICC|ニコニコレンタカー|三井住友|みずほ|WESTER|X の投稿|PR TIMES')),
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
        if kind != '会社' and t not in srcmd:
            mark += ' ・sources.md に札の字なし'
        print('  %s %s ×%d %s%s' % (kind, t, len(cs), ' '.join(cs), mark))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
