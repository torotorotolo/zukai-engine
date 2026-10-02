# -*- coding: utf-8 -*-
"""sub_center.py — 焼いたコマ（試し焼きの `cut_<cid>.jpg`）の**字幕が中央にそろっているか**を機械で測る（2026-10-02 16本目⑤b-7 新設）。

■ なぜ要るか：試し焼き 36943709915 で cb04 の字幕の2行目が「…水を抜く工」で欠けていた（後半が描かれていない）。
  字幕は SVG の中央そろえ（`scene_jiko.sub_row`＝text-anchor="middle"）＝欠けた行は字の範囲の真ん中が画面の中央（960）から
  ずれる。門番 subwrap は字幕の**文**の折り方を測るだけ＝焼いた絵の欠けは見ない（机上検査は絵を見ない）。
  全218コマのうち1行だけ＝640px のシートでは「2行目が短い」くらいにしか見えない。
■ 測るもの：字幕の帯（y 900〜1080）の黄色い字（語り）と水色の字（聞き役）を行ごとに分け、字の範囲の真ん中が
  中央から TOL px より離れた行を挙げる。

    python qa_out/sub_center.py <試し焼きの成果物のフォルダ>      # 例 out/jiko/qa_ep16_b7
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
TOL = 30          # 中央からのずれの許し（px）。字のフチと句読点の偏りは 10px 未満（⑤b-7 に217コマで測った）


def lines_of(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    band = a[900:1080]
    r, g, b = band[..., 0], band[..., 1], band[..., 2]
    ink = ((r > 170) & (g > 150) & (b < 110)) | ((b > 160) & (g > 140) & (r < 170))   # 黄（語り）・水色（聞き役）
    rows = ink.sum(axis=1)
    out, y = [], 0
    while y < len(rows):
        if rows[y] > 3:
            y0 = y
            while y < len(rows) and rows[y] > 3:
                y += 1
            if y - y0 >= 12:
                cols = np.where(ink[y0:y].sum(axis=0) > 0)[0]
                out.append((y0 + 900, y + 900, int(cols[0]), int(cols[-1])))
        y += 1
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    root = Path(sys.argv[1])
    files = sorted(root.rglob("cut_*.jpg"))
    if not files:
        raise SystemExit(f"🔴 {root} に cut_*.jpg が無い（0件を合格にしない）")
    bad = []
    for p in files:
        for y0, y1, x0, x1 in lines_of(p):
            c = (x0 + x1) / 2
            if abs(c - 960) > TOL:
                bad.append((p.stem, y0, x0, x1, round(c)))
    print(f"■ 焼いたコマ {len(files)} 枚の字幕の行を測った（中央 960 からのずれの許し {TOL}px）")
    for s, y0, x0, x1, c in bad:
        print(f"  🔴 {s}  y{y0}  字の範囲 x {x0}〜{x1}（真ん中 {c}）＝行の一部が描かれていない疑い")
    print("✓ どの字幕の行も中央にそろっている" if not bad else f"🔴 {len(bad)} 行")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
