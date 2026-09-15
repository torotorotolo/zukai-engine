# -*- coding: utf-8 -*-
"""ep8 ⑤c' 測り直し ── c112 の柱を「縦の枠線の続き」で測る。

⚠️ 1回目（`ep8_measure.py` §2）は**物差しが壊れていた**。
   「帯の幅の70%がその色の行」を縁と見なしたので、見出しの帯や下の罫まで拾い、
   柱の上端が y=132（図の枠 BY0=210 より上）と出た。
   ＝[[feedback-verify-your-own-instrument]]「全部おかしい値が出たら道具を疑う」。

直し方＝**柱の左の縦棒（線幅4）だけ**を見て、**いちばん長い連続**を柱の高さとする。
陽性対照＝底が barb（818）に来ること／3本の比が値の比に一致すること。
"""
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import jiko_style as J  # noqa: E402
import titan_fig as TF  # noqa: E402

QA = ROOT / "out/jiko/qa_ep8-r01"


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load(cid):
    with Image.open(QA / f"cut_{cid}.jpg") as im:
        return np.asarray(im.convert("RGB")).astype(np.int16)


def longest_run(col_bool):
    """縦1列の True の、いちばん長い連続を (開始, 終了, 長さ) で返す。"""
    best = (None, None, 0)
    s = None
    for i, v in enumerate(col_bool):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s > best[2]:
                best = (s, i - 1, i - s)
            s = None
    if s is not None and len(col_bool) - s > best[2]:
        best = (s, len(col_bool) - 1, len(col_bool) - s)
    return best


top = TF.BY0 + 34
barb = TF.BY1 - 74
barh = barb - (top + 250)
n, gap = 3, 40
cw = (TF.BW - gap * (n - 1)) / n
vmax = 1600
items = [(1500, J.ALERT, "機首と翼の前のふち"), (650, J.AMBER, "骨組みが溶ける"),
         (177, J.OK, "RCCの上限")]

print("=" * 78)
print("■ c112 compare の柱 ── 縦の枠線の「いちばん長い連続」で測る")
print("=" * 78)
print(f"  barb(柱の底)={barb}  barh={barh}  cw={cw:.1f}  vmax={vmax}")
print()
a = load("c112")
got = []
for i, (v, col, lab) in enumerate(items):
    x = TF.BX0 + i * (cw + gap) + cw * 0.16
    c = np.array(hexrgb(col), dtype=np.int16)
    # 左の縦棒（線幅4）の中を通る列を数本見て、いちばん長い連続を採る
    cand = []
    for dx in range(0, 6):
        colb = (np.abs(a[:, int(x) + dx, :] - c).max(axis=1) <= 26)
        cand.append(longest_run(colb))
    y0, y1, ln = max(cand, key=lambda t: t[2])
    want = max(barh * TF.BAR_FLOOR, barh * v / vmax)
    got.append((v, ln, want, y0, y1))
    print(f"  値 {v:>4}（{lab}）  x={int(x)}")
    print(f"      柱 y = {y0} .. {y1}   高さ {ln}px   底のずれ {y1 - barb:+d}px")
    print(f"      式の高さ {want:6.1f}px   差 {ln - want:+.1f}px")
print()
print("  ▼ 陽性対照＝柱どうしの比が、値の比と合うか")
for i in range(len(got)):
    for k in range(i + 1, len(got)):
        v1, h1, _, _, _ = got[i]
        v2, h2, _, _, _ = got[k]
        print(f"    値 {v1}:{v2} = 1:{v2 / v1:5.3f}   "
              f"絵 {h1}:{h2} = 1:{h2 / h1:5.3f}   "
              f"ずれ {100 * ((h2 / h1) / (v2 / v1) - 1):+6.1f}%")
