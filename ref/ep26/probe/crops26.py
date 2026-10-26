# 26本目 ②：文字の層に無い語（数字・色の語）を含む OCR の行だけを頁の画像から切り出し、1枚に積む（見る枚数を減らす）
# 使い方: python -P ref/ep26/probe/crops26.py <ocr_win の出力> <頁のフォルダ> <出力.png> --pages 7,11 [--words red,white] [--width 1700]
import argparse, os, re, sys, unicodedata

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ocrdiff26 import norm, read_ocr  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ocr")
    ap.add_argument("pagedir")
    ap.add_argument("out")
    ap.add_argument("--pages", required=True)
    ap.add_argument("--words", default="red,white,green,colour")
    ap.add_argument("--width", type=int, default=1700)
    ap.add_argument("--margin", type=int, default=14)
    ap.add_argument("--pick", default="", help="自動で選んだ行の番号（1始まり）だけ残す")
    ap.add_argument("--grep", default="", help="この字句を含む OCR の行も足す（カンマ区切り）")
    a = ap.parse_args()
    pages = read_ocr(a.ocr)
    words = set(a.words.split(","))
    greps = [g for g in a.grep.split(",") if g]
    picks, extra = [], []
    for p in [int(x) for x in a.pages.split(",")]:
        layer = norm(open(os.path.join(a.pagedir, f"p{p:03d}.txt"), encoding="utf-8").read())
        lw = set(layer.split())
        for box, text in pages.get(p, []):
            toks = norm(text).split()
            miss = [t for t in toks if (re.search(r"\d", t) or t.strip(".") in words) and t not in lw and t.strip(".'") not in lw]
            if miss:
                picks.append((p, box, text, miss))
            elif any(g in text for g in greps):
                extra.append((p, box, text, ["grep"]))
    if a.pick:
        keep = {int(x) for x in a.pick.split(",")}
        picks = [x for i, x in enumerate(picks, 1) if i in keep]
    picks = sorted(picks + extra, key=lambda x: (x[0], x[1][1]))
    rows = []
    for p, box, text, miss in picks:
        im = Image.open(os.path.join(a.pagedir, f"p{p:03d}.png")).convert("L")
        x0, y0, x1, y1 = box
        m = a.margin
        rows.append((p, im.crop((max(0, x0 - m), max(0, y0 - m), min(im.width, x1 + m), min(im.height, y1 + m)))))
    lab = 70
    scaled = []
    for p, c in rows:
        k = min(1.0, (a.width - lab) / c.width)
        scaled.append((p, c.resize((max(1, int(c.width * k)), max(1, int(c.height * k))))))
    H = sum(c.height + 6 for _, c in scaled) + 6
    sheet = Image.new("L", (a.width, max(H, 10)), 255)
    d = ImageDraw.Draw(sheet)
    y = 6
    for i, (p, c) in enumerate(scaled, 1):
        d.text((4, y + 2), f"{i:02d} p{p}", fill=0)
        sheet.paste(c, (lab, y))
        y += c.height + 6
    sheet.save(a.out)
    with open(os.path.splitext(a.out)[0] + ".tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("n\tpdf_page\tbox\tocr_text\tmissing_tokens\n")
        for i, (p, box, text, miss) in enumerate(picks, 1):
            f.write(f"{i}\t{p}\t{box}\t{text}\t{' '.join(miss)}\n")
    print(f"lines {len(picks)} sheet {sheet.width}x{sheet.height} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
