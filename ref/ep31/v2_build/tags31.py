# -*- coding: utf-8 -*-
"""31本目④'：出典の欄の札を全部数える（ルール 4'-9＝台帳に無い資料を指す札・1カットしか使わない札は要注意）。読むだけ（30本目 tags30.py を写し、札の形を31本目に替えた）。

  python -P ref/ep31/v2_build/tags31.py ref/ep31/daihon_v2.md

札の形：判（最高裁 1983-09-22）・白（運輸白書 昭和47年度）・法（昭和50年法律第58号）・記（国交省 2002-09-04）・国〈issueID〉/〈発言の番号〉（国会会議録）・町（雫石町の頁）・会（全日空の頁）・画（画面の表示）。
出すもの：札ごとの使ったカット・1カットだけの札・国会の札のうち手元の写し（src/kokkai/*.jsonl）に無い発言・出典の欄が空か「―」のカット。名前は出さない（発言の中身は読まない＝番号だけ照らす）。
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
SRC = os.path.join(EP, 'src')
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
TAG = re.compile(r'(国\d{6,}X\d+/\d+|[判白法記町会画])(?=（|・|$|\s|、)')
KNOWN = {'判', '白', '法', '記', '町', '会', '画'}


def kokkai_ids():
    ids = set()
    for fn in ('meetings.jsonl', 'speeches.jsonl'):
        p = os.path.join(SRC, 'kokkai', fn)
        if os.path.exists(p):
            for ln in open(p, encoding='utf-8'):
                r = json.loads(ln)
                ids.add('%s/%s' % (r['issueID'], r['speechOrder']))
    return ids


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
    ids = kokkai_ids()
    empty = [c for c, s in src.items() if s.strip() in ('', '—', '―') or s.strip().startswith('―')]
    print('カット %d・出典の欄が空か「―」 %d %s' % (len(src), len(empty), ' '.join(empty)))
    print('札 %d種（国会の発言 %d・ほか %d）・手元の国会の写し %d発言' % (
        len(uses), sum(1 for t in uses if t.startswith('国')), sum(1 for t in uses if not t.startswith('国')), len(ids)))
    bad = 0
    for t, cs in sorted(uses.items()):
        mark = ''
        if len(cs) == 1:
            mark += ' ・1カットだけ'
        if t.startswith('国'):
            if t[1:] not in ids:
                mark += ' 🔴 手元の写しに無い発言'
                bad += 1
        elif t not in KNOWN:
            mark += ' 🔴 台帳に無い札'
            bad += 1
        print('%s %d%s  %s' % (t, len(cs), mark, ' '.join(sorted(cs)[:40])))
    print('置き場か台帳に無い札 %d' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
