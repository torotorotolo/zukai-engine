# -*- coding: utf-8 -*-
"""8本目 ⑤c'：原寸で「目で決めない」ものを画素で測る。

🔴 根拠＝記憶 [[feedback-sheet-cannot-judge-three-types]]。
   640px のシートで決めてはいけない3型（図の比例・小さな点・札の切れ）は
   **目でなく画素で測る**。7本目はこの型で疑い9件すべてが「粗ではなかった」。

⚠️ 図は**枠線だけ**を測る（色のマスクだけだと**同じ色の数字の字まで拾う**
   ＝7本目 c217 で高さ 540 と出たが正しくは 253）。
   ここでは「その色の純色が、帯の高さ/幅の 0.7 以上ある列/行」だけを縁と見なす。

幾何は本番の `titan_fig` の定数をそのまま使う
（[[feedback-gates-must-share-the-production-geometry]]）。
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


def mask_pure(a, col, tol=26):
    """その色の**純色**だけ（塗り op=0.30 の混色は拾わない）。"""
    c = np.array(hexrgb(col), dtype=np.int16)
    return (np.abs(a - c).max(axis=2) <= tol)


def edges_x(m, y0, y1, frac=0.70):
    """帯 y0..y1 のなかで、縦に frac 以上そろっている列＝縦の枠線。"""
    band = m[y0:y1, :]
    cnt = band.sum(axis=0)
    need = (y1 - y0) * frac
    cols = np.flatnonzero(cnt >= need)
    return (int(cols[0]), int(cols[-1]), cnt) if len(cols) else (None, None, cnt)


def edges_y(m, x0, x1, frac=0.70):
    band = m[:, x0:x1]
    cnt = band.sum(axis=1)
    need = (x1 - x0) * frac
    rows = np.flatnonzero(cnt >= need)
    return (int(rows[0]), int(rows[-1]), cnt) if len(rows) else (None, None, cnt)


print("=" * 78)
print("■ 1. breakdown の帯 ── 値どおりの幅か（c118 c212 c820）")
print("=" * 78)
print(f"  幾何: BX0={TF.BX0} BX1={TF.BX1} BW={TF.BW}")
y_top = TF.BY0 + 96 + 62          # 帯の上端
bh = 168
print(f"  帯の y = {y_top}..{y_top + bh}")
print()
for cid, tot, v, unit in [("c118", 44, 41, "枚"), ("c212", 12, 5, "か所"),
                          ("c820", 100, 38, "%")]:
    a = load(cid)
    m = mask_pure(a, J.AMBER)
    x0, x1, _ = edges_x(m, y_top + 6, y_top + bh - 6)
    want_w = TF.BW * v / tot
    if x0 is None:
        print(f"  {cid}: 枠線が見つからない")
        continue
    got_w = x1 - x0 + 1
    print(f"  {cid}  {v}/{tot} = {100 * v / tot:5.1f}%")
    print(f"      枠線 x = {x0} .. {x1}   幅 {got_w}px")
    print(f"      式の幅 {want_w:7.1f}px（BX0={TF.BX0} から）→ 右端は {TF.BX0 + want_w:.0f}")
    print(f"      画面の幅に対する帯の割合 = {100 * got_w / TF.BW:5.1f}%  "
          f"（値は {100 * v / tot:5.1f}%／差 {100 * got_w / TF.BW - 100 * v / tot:+.1f}pt）")
    print()

print("=" * 78)
print("■ 2. compare の柱 ── 高さが値どおりか（c112）")
print("=" * 78)
top = TF.BY0 + 34
barb = TF.BY1 - 74                # note あり・ratio なし
barh = barb - (top + 250)
n, gap = 3, 40
cw = (TF.BW - gap * (n - 1)) / n
vmax = 1600
items = [(1500, J.ALERT), (650, J.AMBER), (177, J.OK)]
print(f"  幾何: top={top} barb={barb} barh={barh} cw={cw:.1f} vmax={vmax}")
print(f"  BAR_FLOOR={TF.BAR_FLOOR} → 下限の高さ {barh * TF.BAR_FLOOR:.1f}px")
print()
a = load("c112")
for i, (v, col) in enumerate(items):
    x = TF.BX0 + i * (cw + gap) + cw * 0.16
    w = cw * 0.68
    m = mask_pure(a, col)
    y0, y1, _ = edges_y(m, int(x + 8), int(x + w - 8))
    want_h = max(barh * TF.BAR_FLOOR, barh * v / vmax)
    if y0 is None:
        print(f"  値{v}: 枠線が見つからない")
        continue
    got_h = y1 - y0 + 1
    print(f"  値 {v:>4}  ({100 * v / vmax:5.1f}% of vmax)")
    print(f"      枠線 y = {y0} .. {y1}   高さ {got_h}px（底は {barb} のはず）")
    print(f"      式の高さ {want_h:6.1f}px   差 {got_h - want_h:+.1f}px")
print()
print("  ▼ 柱どうしの比（絵の比 ÷ 値の比 が 1.00 なら図は正直）")

print()
print("=" * 78)
print("■ 3. c410 ── bar=False。数字の級数が値と逆を向いていないか")
print("=" * 78)
import fontmetrics as fm  # noqa: E402
n2 = 2
cw2 = (TF.BW - 40 * (n2 - 1)) / n2


def numfit(disp, u, w, cap):
    s = fm.fit(str(disp), w, "Dela", cap=cap, floor=40)
    while s > 40:
        nw = fm.width(str(disp), s, "Dela")
        uw = fm.width(u, s * 0.34, "Noto") + (s * 0.10 if u else 0)
        if nw + uw <= w:
            break
        s -= 4
    return s


for disp, v in [("1", 1), ("50", 50)]:
    s = numfit(disp, "ワット", cw2 * 0.86, 208)
    print(f"  「{disp}」ワット（値 {v}）… 級数 {s}px   "
          f"字の幅 {fm.width(disp, s, 'Dela'):.0f}px")
print()
