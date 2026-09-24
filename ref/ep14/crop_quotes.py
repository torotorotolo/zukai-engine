# -*- coding: utf-8 -*-
"""14本目④：決め所の原文を「頁の画像」から帯で切り出し、数件ずつ1枚のシートに積む。

なぜ要るか
  `check_facts.py` は文字の層に語句が在るかしか見ない。**意味と字面の最後の確認は頁の画像で読む**
  （記憶 feedback-absence-of-a-word-is-not-absence）。頁を丸ごと読むと画像が重い＝語句の帯だけを切り、
  数件を1枚に積む（`~/.claude/CLAUDE.md` 鉄則1）。13本目の `ref/ep13/crop_quotes.py` の14本目版。
  🔴 韓国語は文字の層で分かち書きの空白が揺れる＝**語（word）を並べて空白を取り除いた列の中で探し**、
  当たった語の枠を足し合わせて帯にする（`page.search_for` は空白の揺れで外れる）。

頁の番号は `make_pages.py` の通し番号（判決 p1〜p81／海審 p1001〜p1138／裁決 p2001〜p2174）。
casenote の転載（p5001〜）は PDF が無い＝この道具では切れない。

    python ref/ep14/crop_quotes.py OUTDIR 1055:"09시50분경" 18:"퇴선명령이나"
    python ref/ep14/crop_quotes.py OUTDIR 1047:"어,타가":pad=120     # 帯の上下を広げる（既定 70px）

出力＝OUTDIR/sheet_NN.png（1枚に最大 PER_SHEET 件）と OUTDIR/log.txt。
⚠️ 「当たらない」は「原文に無い」ではない（文字の層の並びが崩れている頁がある）。log に出す。
"""
import re
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
SRC = Path(__file__).resolve().parent / "src"
DOCS = [  # (足す数, PDF)
    (0, SRC / "sewol_scourt.pdf"),
    (1000, SRC / "kmst_sewol.pdf"),
    (2000, SRC / "later" / "kmst_2026_001_central_verdict.pdf"),
]
ZOOM, WIDTH, PAD, PER_SHEET = 2.0, 1100, 70, 4
WS = re.compile(r"\s+")


def locate(gp):
    for off, pdf in sorted(DOCS, key=lambda d: -d[0]):
        if gp > off:
            return pdf, gp - off
    raise SystemExit("E 頁の番号が範囲外: %d" % gp)


def band(page, key, pad):
    """語を読む順に並べ、空白なしの列の中で key を探す。当たった語の枠の縦の範囲を返す。"""
    words = page.get_text("words")          # (x0,y0,x1,y1,word,block,line,no)
    words.sort(key=lambda w: (w[5], w[6], w[7]))
    s, owner = "", []
    for i, w in enumerate(words):
        t = WS.sub("", w[4])
        s += t
        owner += [i] * len(t)
    k = s.find(WS.sub("", key))
    if k < 0:
        return None
    hit = {owner[j] for j in range(k, k + len(WS.sub("", key)))}
    y0 = min(words[i][1] for i in hit)
    y1 = max(words[i][3] for i in hit)
    r = page.rect
    return fitz.Rect(r.x0, max(r.y0, y0 - pad / ZOOM), r.x1, min(r.y1, y1 + pad / ZOOM))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    log, strips = [], []
    for spec in sys.argv[2:]:
        parts = spec.split(":")
        gp, key = int(parts[0]), parts[1]
        pad = PAD
        for extra in parts[2:]:
            if extra.startswith("pad="):
                pad = int(extra[4:])
        pdf, n = locate(gp)
        doc = fitz.open(pdf)
        page = doc[n - 1]
        clip = band(page, key, pad)
        if clip is None:
            log.append("✕ p%d「%s」 文字の層で当たらない（原文に無いとは限らない）" % (gp, key))
            continue
        pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=clip)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im = im.resize((WIDTH, int(im.height * WIDTH / im.width)))
        strips.append(("p%d  %s" % (gp, key), im))
        log.append("○ p%d「%s」 帯 y=%.0f〜%.0f" % (gp, key, clip.y0, clip.y1))
    for i in range(0, len(strips), PER_SHEET):
        group = strips[i:i + PER_SHEET]
        h = sum(im.height + 34 for _, im in group)
        sheet = Image.new("RGB", (WIDTH, h), "white")
        d, y = ImageDraw.Draw(sheet), 0
        for label, im in group:
            d.rectangle([0, y, WIDTH, y + 30], fill=(40, 40, 40))
            d.text((8, y + 8), label.encode("ascii", "replace").decode(), fill="white")
            sheet.paste(im, (0, y + 32))
            y += im.height + 34
        p = out / ("sheet_%02d.png" % (i // PER_SHEET + 1))
        sheet.save(p)
        log.append("→ %s（%d件・%dx%d）" % (p.name, len(group), WIDTH, h))
    (out / "log.txt").write_text("\n".join(log), encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
