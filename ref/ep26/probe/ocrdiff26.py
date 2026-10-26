# 26本目 ②：Windows OCR（頁の画像）の行を、PDF の文字の層と1行ずつ突き合わせ、文字の層に無い・崩れた行を出す
# 使い方: python -P ref/ep26/probe/ocrdiff26.py <ocr_win の出力> <頁の文字のフォルダ（pNNN.txt）> <出力.tsv> [--ratio 0.80]
import argparse, difflib, os, re, sys, unicodedata


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-z°'\". ]", " ", s)).strip()


def read_ocr(path):
    pages, cur = {}, None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            m = re.match(r"## .*?p(\d{3})\.png (\d+)x(\d+)", line)
            if m:
                cur = int(m.group(1))
                pages[cur] = []
                continue
            m = re.match(r"\[(\d+),(\d+)-(\d+),(\d+)\] (.*)", line)
            if m and cur is not None:
                pages[cur].append((tuple(int(m.group(i)) for i in range(1, 5)), m.group(5)))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ocr")
    ap.add_argument("txtdir")
    ap.add_argument("out")
    ap.add_argument("--ratio", type=float, default=0.80)
    a = ap.parse_args()
    pages = read_ocr(a.ocr)
    rows, total, flagged = [], 0, 0
    for p in sorted(pages):
        tp = os.path.join(a.txtdir, f"p{p:03d}.txt")
        layer = open(tp, encoding="utf-8").read() if os.path.exists(tp) else ""
        lnorm = norm(layer)
        llines = [norm(x) for x in layer.splitlines() if norm(x)]
        for box, text in pages[p]:
            n = norm(text)
            if len(n) < 4:
                continue
            total += 1
            if n in lnorm:
                continue
            best = max((difflib.SequenceMatcher(None, n, x).ratio() for x in llines), default=0.0)
            # 文字の層の1行より OCR の行が長いことがある＝窓をずらして部分一致も見る
            if best < a.ratio and lnorm:
                sm = difflib.SequenceMatcher(None, n, lnorm, autojunk=False)
                blk = sum(b.size for b in sm.get_matching_blocks())
                best = max(best, blk / max(1, len(n)) * 0.95)
            if best < a.ratio:
                flagged += 1
                rows.append((p, box, round(best, 2), text))
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("pdf_page\tbox\tbest\tocr_text\n")
        for p, box, b, t in rows:
            f.write(f"{p}\t{box[0]},{box[1]}-{box[2]},{box[3]}\t{b}\t{t}\n")
    print(f"ocr_lines {total} flagged {flagged} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
