# -*- coding: utf-8 -*-
"""15本目 ⑤b-1（2026-09-30）：Actions の試し焼き（字幕の入ったコマ）を機械で測る。

  python qa_out/ep15_b1/measure_subs.py out/jiko/qa_ep15_b1_subs

測るもの（14本目 ⑤b-1 の「焼いた絵で測った」と同じ）：コマの大きさ／帯（y 900〜1080）の中の
語りの黄（#ffe600 の近く）・聞き役の赤（#ff3030 の近く）の画素の数／字のある行の縦の範囲／帯の地の明るさ（字とフチの近くを除く）。
期待＝語りの行は黄だけ・聞き役の行は赤だけ・1行は y 952〜1004 あたり・2行は y 921〜1048 あたり（14本目の実測）・帯の地はほぼ真っ黒。
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
D = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "out" / "jiko" / "qa_ep15_b1_subs"
js = json.loads((ROOT / "audio" / "narration.json").read_text(encoding="utf-8"))


def near(a, rgb, tol=60):
    return (np.abs(a[..., :3].astype(int) - np.array(rgb)).sum(axis=2) <= tol)


want = {}      # at_<cid>_<百分率>.jpg → (行, 話者, 行の数の見込み)
for f in sorted(D.glob("at_*.jpg")):
    cid, pct = f.stem.split("_")[1], int(f.stem.split("_")[2])
    im = np.asarray(Image.open(f).convert("RGB"))
    h, w = im.shape[:2]
    band = im[900:1080]
    yel = near(band, (0xff, 0xe6, 0x00))
    red = near(band, (0xff, 0x30, 0x30))
    ink = yel | red
    rows = np.where(ink.any(axis=1))[0]
    yr = (int(rows.min()) + 900, int(rows.max()) + 900) if len(rows) else None
    # 帯の地＝字とフチの近く（字の画素から 16px 以内）を除いた所の明るさ
    lum = band.mean(axis=2)
    bright = lum > 40
    from scipy.ndimage import binary_dilation
    near_txt = binary_dilation(bright, iterations=16)
    ground = lum[~near_txt]
    print(f"{f.name:22s} {w}x{h}  黄 {int(yel.sum()):6d}  赤 {int(red.sum()):6d}  字の縦 {yr}  "
          f"帯の地 最大 {ground.max() if ground.size else '-':>5}・平均 {ground.mean() if ground.size else 0:.2f}")
