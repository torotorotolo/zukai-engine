# 26本目 ②：PDF を頁ごとに「文字の層」と「頁の画像」に分ける（画像は OCR の入力・見るのは切り出しだけ）
# 使い方: python -P ref/ep26/probe/pages26.py <pdf> <出力フォルダ> [--dpi 300] [--pages 1-30] [--noimg]
import argparse, os, sys

import fitz


def page_list(spec, n):
    if not spec:
        return list(range(1, n + 1))
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return [p for p in out if 1 <= p <= n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--pages", default="")
    ap.add_argument("--noimg", action="store_true")
    a = ap.parse_args()
    doc = fitz.open(a.pdf)
    os.makedirs(a.out, exist_ok=True)
    log = []
    for p in page_list(a.pages, doc.page_count):
        pg = doc[p - 1]
        native = ";".join(f"{x[2]}x{x[3]}/bpc{x[4]}" for x in pg.get_images(full=True))
        txt = pg.get_text("text")
        with open(os.path.join(a.out, f"p{p:03d}.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        if not a.noimg:
            pix = pg.get_pixmap(dpi=a.dpi, colorspace=fitz.csGRAY)
            pix.save(os.path.join(a.out, f"p{p:03d}.png"))
        log.append(f"{p}\t{pg.rect.width:.0f}x{pg.rect.height:.0f}pt\t{native}\t{len(txt)}")
    with open(os.path.join(a.out, "pages.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("pdf_page\tsize\tnative_images\ttext_chars\n" + "\n".join(log) + "\n")
    print(f"pages {len(log)} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
