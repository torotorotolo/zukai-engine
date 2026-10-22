# -*- coding: utf-8 -*-
"""24本目②：src/ の PDF の文字の層を頁ごとに取り出す（PyMuPDF）。
出力＝src/<名前>.pages.tsv（pdf頁<TAB>文字数<TAB>NFKC＋空白を1つに潰した本文）。
⚠️ スキャン＋OCR の資料（S2・S3・UNSCEAR 1988）は誤字・列崩れがある＝決め所は頁の画像で読む。"""
import os, re, sys, unicodedata
import fitz

SRC = r"C:\Users\konar\Desktop\zukai-engine\ref\ep24\src"


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u00ad", "")              # ソフトハイフン
    s = re.sub(r"-\s*\n\s*", "-", s)          # 行末のハイフンはそのまま残す（語を勝手に繋がない）
    return re.sub(r"\s+", " ", s).strip()


def main():
    names = sys.argv[1:] or sorted(f for f in os.listdir(SRC) if f.lower().endswith(".pdf"))
    for name in names:
        path = os.path.join(SRC, name)
        try:
            doc = fitz.open(path)
        except Exception as e:
            print("SKIP", name, type(e).__name__, e)
            continue
        out = os.path.join(SRC, name[:-4] + ".pages.tsv")
        total = 0
        empty = 0
        with open(out, "w", encoding="utf-8") as f:
            for i, page in enumerate(doc, 1):
                t = norm(page.get_text("text"))
                total += len(t)
                empty += (len(t) < 40)
                f.write(f"{i}\t{len(t)}\t{t}\n")
        print(f"{name}\tpages={doc.page_count}\tchars={total}\tnear_empty_pages={empty}")


if __name__ == "__main__":
    main()
