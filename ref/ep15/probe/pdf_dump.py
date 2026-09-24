"""NTSB AAB-12/01 の全文を1回だけ起こす（以後は Grep で引く）。
出力: ref/ep15/src/AAB1201.txt（=== p<N> === 区切り・PDFの頁番号）
標準出力: 頁ごとの先頭・末尾の短い行（印字の頁番号を見る）／図の見出しとクレジット／埋め込み画像の実寸
"""
import re, sys, hashlib
import fitz

SRC = r"C:/Users/konar/Desktop/zukai-engine/ref/ep15/src/AAB1201.pdf"
OUT = r"C:/Users/konar/Desktop/zukai-engine/ref/ep15/src/AAB1201.txt"

doc = fitz.open(SRC)
print("pages", doc.page_count, "md5", hashlib.md5(open(SRC, "rb").read()).hexdigest())
parts = []
for i, pg in enumerate(doc, 1):
    t = pg.get_text("text")
    parts.append("=== p%d ===\n%s" % (i, t))
    lines = [l.strip() for l in t.splitlines() if l.strip()]
    head = lines[0][:60] if lines else ""
    tail = lines[-1][:60] if lines else ""
    imgs = pg.get_images(full=True)
    sizes = []
    for im in imgs:
        xref, w, h, bpc, cs = im[0], im[2], im[3], im[4], im[5]
        sizes.append("%dx%d/%s/%dbit" % (w, h, cs, bpc))
    print("p%02d | head=%r | tail=%r | imgs=%s" % (i, head, tail, ",".join(sizes)))
open(OUT, "w", encoding="utf-8").write("\n".join(parts))
print("wrote", OUT, sum(len(p) for p in parts), "chars")

# 図の見出しとクレジット（本文中の Figure N. ... と、(Source/Photo/Courtesy/©) を含む行）
full = "\n".join(parts)
print("\n--- figure captions (in body, not ToC) ---")
for m in re.finditer(r"=== p(\d+) ===", full):
    pass
for i, pg in enumerate(doc, 1):
    t = pg.get_text("text")
    for mm in re.finditer(r"(Figure \d+\.[^\n]*(?:\n[^\n]*){0,3})", t):
        s = re.sub(r"\s+", " ", mm.group(1))
        if "....." in s:
            continue  # 目次
        print("p%02d: %s" % (i, s[:400]))
print("\n--- credit-like lines ---")
for i, pg in enumerate(doc, 1):
    t = pg.get_text("text")
    for l in t.splitlines():
        if re.search(r"(?i)(source:|photo(graph)? (by|courtesy)|courtesy|©|copyright|used with permission|image credit|provided by)", l):
            print("p%02d: %s" % (i, l.strip()[:200]))
