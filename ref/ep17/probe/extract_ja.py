# -*- coding: utf-8 -*-
"""報告書96-5 の日本語12分割から文字層を取り出す。
- 頁ごとに「印刷頁」を下端の頁番号（－ 5 － など）から読む（NFKC 後）
- ja_body.txt＝原文（頁印つき）／ja_norm.txt＝NFKC＋空白を潰した1頁1行（探す用）
- pages.tsv＝ファイル・PDF頁・印刷頁・文字数・画像の数・画像の大きさ"""
import os, re, sys, unicodedata
import fitz  # PyMuPDF

SRC = r"C:\Users\konar\Desktop\zukai-engine\ref\ep17\src"
out_body, out_norm, out_tsv = [], [], ["file\tpdf_page\tprinted\tchars\timages\timg_max_wh\tfirst_line"]
PNUM = re.compile(r"^[\-－ー‐―−~〜]?\s*(\d{1,3})\s*[\-－ー‐―−~〜]?$")

for i in range(1, 13):
    fn = f"jtsb_96-5_ja_{i:02d}.pdf"
    doc = fitz.open(os.path.join(SRC, fn))
    for pno in range(doc.page_count):
        pg = doc[pno]
        t = pg.get_text("text")
        n = unicodedata.normalize("NFKC", t)
        lines = [l.strip() for l in n.splitlines() if l.strip()]
        printed = ""
        for l in reversed(lines[-4:]):
            m = PNUM.match(l.replace(" ", ""))
            if m:
                printed = m.group(1)
                break
        imgs = pg.get_images(full=True)
        wh = ""
        if imgs:
            best = max(imgs, key=lambda x: x[2] * x[3])
            wh = f"{best[2]}x{best[3]}"
        first = lines[0][:40] if lines else ""
        out_tsv.append(f"{i:02d}\t{pno+1}\t{printed}\t{len(t.strip())}\t{len(imgs)}\t{wh}\t{first}")
        out_body.append(f"\n=== ja_{i:02d} pdf{pno+1} printed:{printed} ===\n{t}")
        flat = re.sub(r"\s+", "", n)
        out_norm.append(f"ja_{i:02d}\tpdf{pno+1}\tp{printed}\t{flat}")
    doc.close()

with open(os.path.join(SRC, "ja_body.txt"), "w", encoding="utf-8") as f:
    f.write("".join(out_body))
with open(os.path.join(SRC, "ja_norm.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out_norm) + "\n")
with open(os.path.join(SRC, "ja_pages.tsv"), "w", encoding="utf-8") as f:
    f.write("\n".join(out_tsv) + "\n")
print("pages:", len(out_norm))
