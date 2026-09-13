# -*- coding: utf-8 -*-
"""委員会報告の「印字ページ」を偶数頁の走りヘッダから内挿して当てる。
⚠️ ヘッダは本文の**前**に出る（実測で確認）。偶数頁ヘッダ `NN THE 9/11 COMMISSION REPORT` は
   全章に出るので、これだけを骨にして、間にある奇数頁は文字数で内挿する。
陽性対照は --selftest（答えの分かっている4件）。"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r"C:/Users/konar/Desktop/zukai-engine/analytics/materials/ep7/GPO-911REPORT.pdf.txt"
T = open(P, encoding='utf-8', errors='replace').read()
FLAT = re.sub(r'\s+', ' ', T)
MARK = re.compile(r'(\d{1,3}) THE 9/11 COMMISSION REPORT')
PAGES = [(m.start(), int(m.group(1))) for m in MARK.finditer(FLAT)]
PAGES = [p for p in PAGES if p[1] % 2 == 0]

def page_of(pos):
    lo = None
    for i, (st, num) in enumerate(PAGES):
        if st <= pos:
            lo = i
        else:
            break
    if lo is None:
        return None
    st, num = PAGES[lo]
    if lo + 1 < len(PAGES):
        nxt = PAGES[lo + 1][0]
        return num if pos < st + (nxt - st) / 2 else num + 1
    return num

def find(pat, limit=3):
    out = []
    for m in re.finditer(pat, FLAT, re.I):
        out.append((page_of(m.start()), FLAT[m.start():m.start() + 64]))
        if len(out) >= limit:
            break
    return out

if __name__ == '__main__':
    if '--selftest' in sys.argv:
        # 答えの分かっている4件（印字ページを目で確かめたもの）
        for pat, want in [("The plane took off at 7:59", 4), ("153 miles away", 20),
                          ("4,500 commercial", 29), ("Both towers had 110 stories", 278)]:
            got = find(pat, 1)[0][0]
            print('%s %-30s → p%s（想定 p%s±1）' %
                  ('✓' if got is not None and abs(got - want) <= 1 else 'E', pat, got, want))
        sys.exit(0)
    for pat in sys.argv[1:]:
        print('--- %s' % pat)
        for pg, s in find(pat):
            print('    p%s  %s' % (pg, s))
