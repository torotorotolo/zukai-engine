# -*- coding: utf-8 -*-
"""目次（ja_01 の前付け）の「節番号 … 頁」と、本文で見出しが最初に出る PDF 頁を突き合わせ、
ファイルごとの「印刷頁＝PDF頁＋ずれ」を出す。ずれが1つに揃わなければ止める。"""
import re, sys, unicodedata, collections
import fitz

SRC = r"C:\Users\konar\Desktop\zukai-engine\ref\ep17\src"
docs = {i: fitz.open(f"{SRC}\\jtsb_96-5_ja_{i:02d}.pdf") for i in range(1, 5)}

def norm(s):
    return unicodedata.normalize("NFKC", s)

# 目次を探す：ja_01 の最初の17頁で「節番号 ... 数字」の行
toc = []
for p in range(0, 17):
    ls = [l.strip() for l in norm(docs[1][p].get_text("text")).splitlines() if l.strip()]
    cur = None
    for l in ls:
        m = re.match(r"^(\d+(?:\.\d+){1,3})\s*(.*?)\s*(?:\((\d{1,3})\))?$", l)
        pg = re.match(r"^\((\d{1,3})\)$", l)
        if m and not pg:
            cur = [m.group(1), m.group(2)]
            if m.group(3):
                toc.append((cur[0], cur[1], int(m.group(3)), p + 1)); cur = None
        elif pg and cur:
            toc.append((cur[0], cur[1], int(pg.group(1)), p + 1)); cur = None
        elif cur and not cur[1]:
            cur[1] = l
print("toc entries:", len(toc))

# 本文で見出しの最初の出現（目次の頁より後ろ）
def find_heading(sec):
    pat = re.compile(r"(^|\n)\s*" + re.escape(sec) + r"[\s　]")
    for i in range(1, 5):
        start = 17 if i == 1 else 0
        for p in range(start, docs[i].page_count):
            t = norm(docs[i][p].get_text("text"))
            if pat.search(t):
                return i, p + 1
    return None

offs = collections.defaultdict(collections.Counter)
rows = []
for sec, title, printed, tp in toc:
    hit = find_heading(sec)
    if not hit:
        rows.append((sec, title[:20], printed, "", "", ""))
        continue
    i, pdfp = hit
    d = printed - pdfp
    offs[i][d] += 1
    rows.append((sec, title[:20], printed, f"ja_{i:02d}", pdfp, d))

for r in rows:
    print("\t".join(str(x) for x in r))
print()
for i in sorted(offs):
    print(f"ja_{i:02d} offsets:", dict(offs[i]))
