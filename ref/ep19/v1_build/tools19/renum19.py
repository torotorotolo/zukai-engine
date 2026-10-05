# -*- coding: utf-8 -*-
"""台本 §4 のカットIDを、章（IDの頭2字）ごとに出てくる順で振り直す。仮の番号（c4x1 など）を足したあとに回す。
章の見出しの「（Nカット）」も数え直す。字は変えない（IDと見出しの数だけ）。前後の本文の字数を照合する。
  python renum19.py <台本.md> [--dry]
"""
import re
import sys

path = sys.argv[1]
dry = '--dry' in sys.argv
src = open(path, encoding='utf-8').read()
lines = src.split('\n')
HDR = re.compile(r'^\*\*(c[0-9a-z][0-9a-z]{1,3})\*\*(\s*(?:🔧\s*)?／.*)$')
start = next(i for i, l in enumerate(lines) if l.startswith('## 4. 台本'))
end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
cnt, mapping = {}, []
for i in range(start, end):
    m = HDR.match(lines[i])
    if not m:
        continue
    old = m.group(1)
    ch = old[:2]
    cnt[ch] = cnt.get(ch, 0) + 1
    n = cnt[ch]
    new = ch + ('%02d' % n if ch[1] in 'abcdef' else '%02d' % n)
    if ch[1] not in 'abcdef':
        new = ch + '%02d' % n          # c101 の形＝頭2字＋2桁
    if old != new:
        mapping.append((old, new))
    lines[i] = '**' + new + '**' + m.group(2)
# 見出しの（Nカット）
cur = None
heads = {}
for i in range(start, end):
    if lines[i].startswith('### '):
        cur = i
    m = HDR.match(lines[i])
    if m and cur is not None:
        heads.setdefault(cur, set()).add(m.group(1)[:2])
for hi, chs in heads.items():
    n = sum(cnt[c] for c in chs)
    lines[hi] = re.sub(r'（\d+カット）', '（%dカット）' % n, lines[hi])
out = '\n'.join(lines)
body = lambda s: re.sub(r'\*\*c[0-9a-z]+\*\*|（\d+カット）', '', s)
assert body(out) == body(src), '本文の字が変わった'
print('振り直し', len(mapping), '件:', ' '.join(f'{a}→{b}' for a, b in mapping[:60]))
print('章ごと', cnt, '計', sum(cnt.values()))
if not dry and out != src:
    open(path, 'w', encoding='utf-8', newline='\n').write(out)
    print('書いた')
