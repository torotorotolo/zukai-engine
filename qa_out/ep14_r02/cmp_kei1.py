# -*- coding: utf-8 -*-
"""cfix1（r01 と同じ絵）と kei1（字幕だけ替えた版）の検品の焼きを1枚ずつ比べる。
帯（y900〜1080）の上と中で分けて差を数える＝上の差が0なら「変わったのは字幕の層だけ」。
使い方: python cmp_kei1.py <cfix1 のフォルダ> <kei1 のフォルダ>
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
A, B = Path(sys.argv[1]), Path(sys.argv[2])
TH = 24                     # JPEG の揺れより大きい差だけ数える（同じ入力なら 0 のはず）
pick = lambda d: {p.name for p in d.iterdir() if p.name.startswith(("cut_", "at_", "card_"))}
names = sorted(pick(A) & pick(B))
only_a, only_b = sorted(pick(A) - pick(B)), sorted(pick(B) - pick(A))
top_changed, band_changed, same, band_sub_a, band_sub_b = [], [], 0, 0, 0
for n in names:
    a = np.asarray(Image.open(A / n).convert("RGB")).astype(np.int16)
    b = np.asarray(Image.open(B / n).convert("RGB")).astype(np.int16)
    if a.shape != b.shape:
        top_changed.append((n, f"大きさ {a.shape}≠{b.shape}"))
        continue
    d = np.abs(a - b).max(axis=2)
    y0 = round(900 * a.shape[0] / 1080)
    t, bd = int((d[:y0] > TH).sum()), int((d[y0:] > TH).sum())
    # 帯の中に字があるか（明るい画素）＝字幕の出ているコマか
    band_sub_a += int((a[y0:].max(axis=2) > 80).sum() > 200)
    band_sub_b += int((b[y0:].max(axis=2) > 80).sum() > 200)
    if t:
        top_changed.append((n, f"帯の上 {t}画素（最大の差 {int(d[:y0].max())}）"))
    if bd:
        band_changed.append(n)
    if not t and not bd:
        same += 1
print(f"比べた {len(names)}枚（cfix1 だけ {len(only_a)}・kei1 だけ {len(only_b)}）")
print(f"帯の上が変わった {len(top_changed)}枚／帯の中だけ変わった {len(band_changed) - len([1 for n, _ in top_changed if n in band_changed])}枚／全く同じ {same}枚")
print(f"帯に字のあるコマ cfix1 {band_sub_a}枚・kei1 {band_sub_b}枚")
for n, why in top_changed[:30]:
    print("  🔴 上が変わった:", n, why)
print("kei1 だけ:", ", ".join(only_b[:20]))
print("cfix1 だけ:", ", ".join(only_a[:20]))
# 帯の中が変わらなかったのに字のあるコマ（＝字幕が替わっていない疑い）
unchanged_with_text = []
for n in names:
    if n in band_changed:
        continue
    b = np.asarray(Image.open(B / n).convert("RGB")).astype(np.int16)
    y0 = round(900 * b.shape[0] / 1080)
    if (b[y0:].max(axis=2) > 80).sum() > 200:
        unchanged_with_text.append(n)
print(f"字があるのに帯が変わっていないコマ {len(unchanged_with_text)}枚:", ", ".join(unchanged_with_text[:20]))
