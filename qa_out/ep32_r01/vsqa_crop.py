# -*- coding: utf-8 -*-
"""32本目 ⑥：絵の照合（vs_qa.tsv）で局所の差が大きいカットの「差のいちばん大きい所」を、本編のコマ（cutframes の原寸 jpg）と
⑤c' 周2 の検品の絵（`out/jiko/qa-ep32_c2/cut_<cid>.jpg`）から原寸で切り出して左右に並べる。差の場所は 16×16 の升（1920×1080 なら 96px 角相当）で探す。
    python -P qa_out/ep32_r01/vsqa_crop.py c411 c203 c205   → qa_out/ep32_r01/vsqa_crop.jpg
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
FR = ROOT / "out" / "jiko" / "ep32_r01_frames"
QA = ROOT / "out" / "jiko" / "qa-ep32_c2"
FONT = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
BOX = 300                                   # 切り出しの一辺（原寸）
rows = []
for cid in sys.argv[1:]:
    a = np.asarray(Image.open(FR / f"cut_{cid}.jpg").convert("RGB")).astype(np.int16)
    b = np.asarray(Image.open(QA / f"cut_{cid}.jpg").convert("RGB").resize((a.shape[1], a.shape[0]), Image.BILINEAR)).astype(np.int16)
    d = np.abs(a - b).mean(axis=2)
    bs = 96
    hh, ww = (d.shape[0] // bs) * bs, (d.shape[1] // bs) * bs
    blk = d[:hh, :ww].reshape(hh // bs, bs, ww // bs, bs).mean(axis=(1, 3))
    by, bx = np.unravel_index(np.argmax(blk), blk.shape)
    cy, cx = by * bs + bs // 2, bx * bs + bs // 2
    x0 = int(min(max(0, cx - BOX // 2), a.shape[1] - BOX))
    y0 = int(min(max(0, cy - BOX // 2), a.shape[0] - BOX))
    print(f"{cid}: 升の差の最大 {blk.max():.1f}（x{bx * bs}〜{bx * bs + bs}・y{by * bs}〜{by * bs + bs}）・全体 {d.mean():.2f} → 切り出し x{x0} y{y0}")
    ca = Image.fromarray(a[y0:y0 + BOX, x0:x0 + BOX].astype(np.uint8))
    cb = Image.fromarray(b[y0:y0 + BOX, x0:x0 + BOX].astype(np.uint8))
    rows.append((cid, x0, y0, ca, cb))
W = 2 * BOX + 30
im = Image.new("RGB", (W, len(rows) * (BOX + 28)), "#222")
dr = ImageDraw.Draw(im)
for i, (cid, x0, y0, ca, cb) in enumerate(rows):
    y = i * (BOX + 28)
    dr.text((4, y + 2), f"{cid} 本編（左）／周2 の検品（右）x{x0} y{y0} 原寸", font=FONT, fill="#ff0")
    im.paste(ca, (0, y + 26))
    im.paste(cb, (BOX + 30, y + 26))
out = ROOT / "qa_out" / "ep32_r01" / "vsqa_crop.jpg"
im.save(out, quality=94)
print(out, im.size)
