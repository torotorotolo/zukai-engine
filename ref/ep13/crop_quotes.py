# -*- coding: utf-8 -*-
"""13本目④：決め所の原文を「頁の画像」から切り出し、数件ずつ1枚のシートに積む。

なぜ要るか
  仏の最終報告（S1）の文字の層は2005年の OCR で崩れている（"La carlingue a éclaté" が "oarZingue a eelate"）。
  英訳（S2）と NTSB（S4）は画像だけの PDF。`check_facts.py` は文字の層に語句が在るかしか見ないので、
  **意味と綴りの最後の確認は頁の画像で読む**（記憶 feedback-absence-of-a-word-is-not-absence）。
  頁を丸ごと読むと画像が重い＝**語句の位置の帯だけを切り出し、数件を1枚に積む**（`~/.claude/CLAUDE.md` 鉄則1）。
  12本目の `ref/ep12/crop_quotes.py` の13本目版（資料の並びと、積む処理を足した）。

頁の番号は `make_pages.py` の通し番号（仏 p1〜／英 p1001〜／上院 p2001〜／NTSB p3001〜／AD・官報 p4001〜／SB p5001〜）。

    python ref/ep13/crop_quotes.py OUTDIR 146:"tout etait" 2030:"gentlemen" 1010:"burst"
    python ref/ep13/crop_quotes.py OUTDIR 88:"FORCEE":up=260          # 帯の上を広げる（図の見出しの上の絵まで）
    python ref/ep13/crop_quotes.py OUTDIR 141:y=0.20-0.60             # 語句で当たらない頁は縦の範囲（頁の高さに対する割合）

出力＝OUTDIR/sheet_NN.png（1枚に最大 PER_SHEET 件・高さ MAX_H まで）と OUTDIR/log.txt。
⚠️ 文字の層で当たらないとき（画像だけの PDF・OCR 崩れ）は、`make_pages.py` の本文の中の位置から
　 縦の位置を見積もって ±BAND の帯を切る（見積もり＝ずれる。読めなければ y= で指定し直す）。
　 **「当たらない」は「原文に無い」ではない。**
"""
import re
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
SRC = Path(__file__).resolve().parent / "src"
DOCS = [  # (足す数, PDF, 文字のファイル)
    (0, "faa_FinalAccidentReportinFrench.pdf", "faa_FinalAccidentReportinFrench.txt"),
    (1000, "aib_8-76_TC-JAV.pdf", "aib_8-76_TC-JAV.ocr.txt"),
    (2000, "senate_cprt93_dc10.pdf", "senate_cprt93_dc10.txt"),
    (3000, "ntsb_AAR73-02_N103AA_erau.pdf", "ntsb_AAR73-02_N103AA_erau.txt"),
    (4000, "faa_AD74-08-04.pdf", "faa_AD74-08-04.txt"),
    (4100, "faa_AD74-12-07.pdf", "faa_AD74-12-07.txt"),
    (4200, "faa_AD75-15-05.pdf", "faa_AD75-15-05.txt"),
    (4300, "fr_1974-04-02_11992.pdf", "fr_1974-04-02_11992.txt"),
    (5000, "faa_SB52-37.pdf", "faa_SB52-37.txt"),
    (5100, "faa_SB52-38.pdf", "faa_SB52-38.txt"),
]
ZOOM, WIDTH, MARGIN, BAND = 2.0, 1200, 46, 0.09
PER_SHEET, MAX_H = 5, 1560


def locate(gp):
    for off, pdf, txt in sorted(DOCS, reverse=True):
        if gp > off:
            return SRC / pdf, SRC / txt, gp - off
    raise SystemExit("E 頁の番号が範囲外: %d" % gp)


def text_of(txt, n):
    t = txt.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"=== p ?(\d+) ===", t)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}.get(n, "")


def band_for(page, txtfile, n, spec):
    """(clip, how)。spec＝語句か y=a-b。"""
    h = page.rect.height
    m = re.match(r"y=([\d.]+)-([\d.]+)$", spec)
    if m:
        return fitz.Rect(0, h * float(m.group(1)), page.rect.width, h * float(m.group(2))), "y指定"
    hits = page.search_for(spec)
    if hits:
        r = hits[0]
        return fitz.Rect(0, r.y0, page.rect.width, r.y1), "文字の層で当たった"
    body = re.sub(r"\s+", " ", text_of(txtfile, n))
    k = body.lower().find(re.sub(r"\s+", " ", spec).lower())
    if k < 0:
        return None, "当たらない（y= で指定し直す）"
    f = k / max(1, len(body))
    return (fitz.Rect(0, h * max(0, f - BAND), page.rect.width, h * min(1, f + BAND)),
            "本文の位置から見積もり（f=%.2f）" % f)


def crop(spec_all):
    gp, rest = spec_all.split(":", 1)
    up = down = MARGIN
    while re.search(r":(up|down)=(\d+)$", rest):
        k, v = re.search(r":(up|down)=(\d+)$", rest).groups()
        rest = re.sub(r":(up|down)=(\d+)$", "", rest)
        if k == "up":
            up = int(v)
        else:
            down = int(v)
    pdf, txt, n = locate(int(gp))
    doc = fitz.open(pdf)
    page = doc[n - 1]
    clip, how = band_for(page, txt, n, rest.strip('"'))
    if clip is None:
        return None, "p%s %s … %s" % (gp, rest, how)
    clip = fitz.Rect(clip.x0, max(0, clip.y0 - up), clip.x1, min(page.rect.height, clip.y1 + down))
    pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=clip)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im = im.resize((WIDTH, max(1, int(im.height * WIDTH / im.width))))
    lab = Image.new("RGB", (WIDTH, 26), (255, 235, 150))
    ImageDraw.Draw(lab).text((8, 6), "p%s  %s  [%s]" % (gp, rest[:60], pdf.name[:28]), fill=(0, 0, 0))
    out = Image.new("RGB", (WIDTH, im.height + 26), (255, 255, 255))
    out.paste(lab, (0, 0))
    out.paste(im, (0, 26))
    return out, "p%s %s … %s" % (gp, rest, how)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    outdir = Path(sys.argv[1])
    outdir.mkdir(parents=True, exist_ok=True)
    ims, log = [], []
    for s in sys.argv[2:]:
        im, msg = crop(s)
        log.append(msg)
        print(msg)
        if im is not None:
            ims.append(im)
    sheets, cur, h = [], [], 0
    for im in ims:
        if cur and (len(cur) >= PER_SHEET or h + im.height > MAX_H):
            sheets.append(cur)
            cur, h = [], 0
        cur.append(im)
        h += im.height + 8
    if cur:
        sheets.append(cur)
    for i, grp in enumerate(sheets, 1):
        H = sum(g.height + 8 for g in grp)
        sh = Image.new("RGB", (WIDTH, H), (90, 90, 90))
        y = 0
        for g in grp:
            sh.paste(g, (0, y))
            y += g.height + 8
        p = outdir / ("sheet_%02d.png" % i)
        sh.save(p)
        print("→ %s（%d件・%dx%d）" % (p.name, len(grp), WIDTH, H))
    (outdir / "log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
