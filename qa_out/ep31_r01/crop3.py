# -*- coding: utf-8 -*-
"""31本目 ⑥ 受け取り：外れの3カットを本編のコマ（ep31_r01_frames）から切り出して1枚に並べる（原寸＝縮めない）。
  ① cc03＝検品の絵との照合の局所の最大 10.0（ほかは中央値 5.5）＝本編と ⑤c の検品の絵（qa_ep31_c）の差の大きい 48px の升を中心に、左右に並べる
  ② c404（7.29）・c510（7.43）＝地の暗さの最悪の升（ground の表の升の左上）を中心に、本編のコマを原寸で
    python -P qa_out/ep31_r01/crop3.py → qa_out/ep31_r01/crop3.png（1280×720）
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
FR = ROOT / "out" / "jiko" / "ep31_r01_frames"
QA = ROOT / "out" / "jiko" / "qa_ep31_c"
B = 48


def crop_at(im, cx, cy, w=640, h=360):
    x0 = min(max(cx - w // 2, 0), im.width - w)
    y0 = min(max(cy - h // 2, 0), im.height - h)
    return im.crop((x0, y0, x0 + w, y0 + h)), (x0, y0)


def main():
    sheet = Image.new("RGB", (1280, 720), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    # ① cc03：本編と検品の絵の差の大きい升
    a = Image.open(FR / "cut_cc03.jpg").convert("RGB")
    q = Image.open(QA / "cut_cc03.jpg").convert("RGB").resize(a.size)
    diff = np.abs(np.asarray(a, float) - np.asarray(q, float)).mean(-1)
    hb, wb = diff.shape[0] // B, diff.shape[1] // B
    bm = diff[:hb * B, :wb * B].reshape(hb, B, wb, B).mean((1, 3))
    by, bx = np.unravel_index(np.argmax(bm), bm.shape)
    cx, cy = int(bx * B + B // 2), int(by * B + B // 2)
    print(f"cc03 差の最大の升 x{bx * B}〜{bx * B + B}・y{by * B}〜{by * B + B}・平均の差 {bm.max():.1f}（全体 {diff.mean():.2f}）")
    ca, o = crop_at(a, cx, cy)
    cq, _ = crop_at(q, cx, cy)
    sheet.paste(ca, (0, 0))
    sheet.paste(cq, (640, 0))
    for x in (0, 640):
        d.rectangle([x + cx - o[0] - B // 2, cy - o[1] - B // 2, x + cx - o[0] + B // 2, cy - o[1] + B // 2], outline=(255, 0, 255), width=2)
    d.text((6, 4), "cc03 本編 r01", fill=(255, 0, 255))
    d.text((646, 4), "cc03 検品の絵（5c）", fill=(255, 0, 255))
    # ② c404・c510：地の暗さの最悪の升（表の升＝左上の座標・48px）
    for i, (cut, (gx, gy)) in enumerate((("c404", (1272, 648)), ("c510", (1128, 312))), start=0):
        im = Image.open(FR / f"cut_{cut}.jpg").convert("RGB")
        c, o = crop_at(im, gx + B // 2, gy + B // 2)
        sheet.paste(c, (640 * i, 360))
        d.rectangle([640 * i + gx - o[0], 360 + gy - o[1], 640 * i + gx - o[0] + B, 360 + gy - o[1] + B], outline=(255, 0, 255), width=2)
        d.text((640 * i + 6, 364), f"{cut} 本編 r01（升 {gx},{gy}）", fill=(255, 0, 255))
    out = ROOT / "qa_out" / "ep31_r01" / "crop3.png"
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
