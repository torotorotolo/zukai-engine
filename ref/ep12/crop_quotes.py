# -*- coding: utf-8 -*-
"""12本目④：決め所の原文を「頁の画像」から切り出す（OCR の文字層を信じないため）。

なぜ要るか
  `ref/ep12/src/*.txt` は OCR が崩れている（DNA 6035F の表紙は "CASTLE SERI s"）。
  `check_facts.py` は文字層に語句が在るかしか見ないので、**意味と綴りの最後の確認は頁の画像で読む**
  （記憶 feedback-absence-of-a-word-is-not-absence / feedback-verify-every-onscreen-quote）。
  頁を丸ごと読むと画像が重いので、**語句の位置だけを切り出す**（`~/.claude/CLAUDE.md` 鉄則1）。

頁の番号は `make_pages.py` の通し番号（DNA 6035F＝p1〜538 / WT-923＝p1001〜 / DASA 1251＝p2001〜）。

    python ref/ep12/crop_quotes.py OUTDIR 212:"much greater than" 209:"headed for Rongelap"
    python ref/ep12/crop_quotes.py OUTDIR --from-script <台本.md>     # §2 の表の原文を全部
    python ref/ep12/crop_quotes.py OUTDIR 220:y=0.05-0.45             # 語句で当たらない頁は縦の範囲（頁の高さに対する割合）

出力＝OUTDIR/p<頁>_<連番>.png（幅は頁の本文の幅・上下に数行の余白）。
⚠️ 語句が文字層で見つからない（OCR が崩れている）ときは **止めずに「見つからない」と出す**。
　 そのときは y= の形で範囲を指定して切り出し、目で読む（「当たらない＝原文に無い」ではない）。
"""
import re
import sys
from pathlib import Path

import fitz

sys.stdout.reconfigure(encoding="utf-8")
SRC = Path(__file__).resolve().parent / "src"
DOCS = [(0, "dna6035f.pdf"), (1000, "project41_wt923.pdf"), (2000, "dasa1251_v2.pdf")]
ROW_RE = re.compile(r'^\|\s*\d+\s*\|\s*\*\*([a-z]{1,2}\d{2,3})\*\*\s*\|(.*)$')


def locate(gp):
    """通し番号 → (PDF のパス, 0始まりの頁)。"""
    for off, name in sorted(DOCS, reverse=True):
        if gp > off:
            return SRC / name, gp - off - 1
    raise SystemExit("E 頁の番号が範囲外: %d" % gp)


def from_script(md):
    """台本 §2 の表から (頁, 原文) を全部取る（check_facts.py と同じ読み方）。"""
    out, on = [], False
    for line in open(md, encoding="utf-8").read().split("\n"):
        if re.match(r"^## 2[.\s]", line):
            on = True
            continue
        if on and re.match(r"^## (?!2)", line):
            break
        m = ROW_RE.match(line) if on else None
        if not m:
            continue
        cols = [c.strip() for c in m.group(2).split("|")]
        while cols and not cols[-1]:
            cols.pop()
        pages = [int(a) for a, _ in re.findall(r"p\.?\s*(\d+)(?:\s*[〜~\-–]\s*(\d+))?", cols[-1])]
        for q in re.findall(r"`([^`]+)`", " ".join(cols)):
            out.append((pages[0] if pages else None, q, m.group(1)))
    return out


def crop(outdir, gp, what, tag, n):
    pdf, pi = locate(gp)
    doc = fitz.open(pdf)
    page = doc[pi]
    W, H = page.rect.width, page.rect.height
    if what.startswith("y="):
        a, b = [float(x) for x in what[2:].split("-")]
        clip = fitz.Rect(0, H * a, W, H * b)
        note = "範囲指定"
    else:
        # 語句は長いと OCR の崩れで当たらないので、先頭の4語で探す
        key = " ".join(what.split()[:4])
        hits = page.search_for(key)
        if not hits:
            print("⚠️  p%d 文字層で見つからない（目で読む・y= で切る）: %s" % (gp, what[:60]))
            return None
        r = hits[0]
        clip = fitz.Rect(W * 0.04, max(0, r.y0 - 70), W * 0.96, min(H, r.y1 + 90))
        note = key
    pix = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)
    out = Path(outdir) / ("p%d_%02d%s.png" % (gp, n, ("_" + tag) if tag else ""))
    pix.save(out)
    print("OK  p%-5d %-6s %4dx%-4d %s ← %s" % (gp, tag or "", pix.width, pix.height, out.name, note[:50]))
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    outdir = Path(sys.argv[1])
    outdir.mkdir(parents=True, exist_ok=True)
    jobs = []
    if sys.argv[2] == "--from-script":
        jobs = from_script(sys.argv[3])
    else:
        for a in sys.argv[2:]:
            p, w = a.split(":", 1)
            jobs.append((int(p), w, ""))
    miss = 0
    for n, (gp, what, tag) in enumerate(jobs, 1):
        if gp is None:
            print("🔴 %s 頁の欄が読めない: %s" % (tag, what[:50]))
            miss += 1
            continue
        miss += crop(outdir, gp, what, tag, n) is None
    print("切り出し %d件 / 見つからない %d件" % (len(jobs) - miss, miss))
    return 0


if __name__ == "__main__":
    sys.exit(main())
