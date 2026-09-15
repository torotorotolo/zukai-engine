# -*- coding: utf-8 -*-
"""ep8 ⑤c' ── 残りの「機械で決まる」疑いを測る。

対象
  A. `icons` の札の級数（c407 c905 c114 と、鳴らなかった6件＝陰性対照）
  B. `people` の札の級数（c505 対 c414）
  C. 焼けた絵の画素差（c305/pr07・c707/c817・ep01/ep02・c705系・c309/c315）
  D. 地に敷いた写真の見えかた（c730 c804）と c106 の彩度

⚠️ 陰性対照を必ず並べる（[[feedback-verify-your-own-instrument]]）。
   「鳴った3件」だけ見ると、その値がふつうなのか外れなのか決まらない。
"""
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import fontmetrics as fm  # noqa: E402
import titan_fig as TF  # noqa: E402

QA = ROOT / "out/jiko/qa_ep8-r01"


def load(cid):
    with Image.open(QA / f"cut_{cid}.jpg") as im:
        return np.asarray(im.convert("RGB")).astype(np.float64)


def fitsize(s, w, cap, floor=None):
    """titan_fig.txtfit と同じ決まりで級数を出す。"""
    return fm.fit(s, w, "Noto", cap=cap, floor=floor or 18)


print("=" * 78)
print("■ A. icons の札 ── 同じ図の中で級数がどれだけ違うか")
print("=" * 78)
cols = 5
cw = min(TF.BW / cols, 300)
cap = max(24, int(cw * 0.20))
lim = cw * 0.98
print(f"  cols={cols} → 欄の幅 cw={cw:.0f}px／札の上限 cap={cap}px／"
      f"収める幅 {lim:.0f}px")
print(f"  札は x（丸の中心）に anchor='middle'＝**真下に中央ぞろえ**")
print()

ICONS = {
    "c407": ["スペースハブへの通路", "研究室", "もう一つの実験装置",
             "加速度をはかる計器", "長く飛ぶための補給の台"],
    "c905": ["予算の不足", "揺れる優先順位", "日程の圧力",
             "開発中なのに完成品扱い", "過去の成功に頼った"],
    "c114": ["コロンビア号", "チャレンジャー号", "ディスカバリー号",
             "アトランティス号", "5機目（1992年）"],
}
for cid, labs in ICONS.items():
    sizes = [fitsize(t, lim, cap) for t in labs]
    print(f"  {cid}")
    for t, s in zip(labs, sizes):
        print(f"      {s:3.0f}px  ({len(t):2d}字)  {t}")
    print(f"      → 最大 {max(sizes):.0f} / 最小 {min(sizes):.0f} "
          f"＝ **{max(sizes) / min(sizes):.2f}倍**")
    print()

print("=" * 78)
print("■ B. people の札 ── c505 が c414 より小さいか")
print("=" * 78)
print("  （people は node ごとに幅が違うので、字数だけ並べる）")
for cid, nodes in [("c414", ["地上の担当", "機長", "乗員全員"]),
                   ("c505", ["写真作業班の長", "請負会社の管理者", "ロッチャ技師",
                             "飛行中の判断をする側"])]:
    print(f"  {cid}: {len(nodes)}人 … " +
          "／".join(f"{t}({len(t)}字)" for t in nodes))
print()

print("=" * 78)
print("■ C. 焼けた絵の画素差（0 に近いほど同じ絵）")
print("=" * 78)
PAIRS = [("c305", "pr07"), ("c707", "c817"), ("ep01", "ep02"),
         ("c705", "c711"), ("c705", "c715"), ("c705", "c717"),
         ("c711", "c715"), ("c715", "c717"), ("c309", "c315")]
for a_, b_ in PAIRS:
    A, B = load(a_), load(b_)
    d = np.abs(A - B)
    print(f"  {a_} 対 {b_}: 平均差 {d.mean():6.2f}／最大 {d.max():5.0f}／"
          f"差が2以上の画素 {100 * (d.max(axis=2) >= 2).mean():5.1f}%")
print()

print("=" * 78)
print("■ D. 地に敷いた写真の見えかた／c106 の彩度")
print("=" * 78)
print("  ▼ 地の写真（下半分のばらつき＝写真が見えているほど大きい）")
for cid in ["c730", "c804", "c109", "c115", "c117", "c208", "c416"]:
    a = load(cid)
    g = a.mean(axis=2)
    print(f"  {cid}: 全体の標準偏差 {g.std():6.2f}／"
          f"明るさの中央 {np.median(g):6.1f}")
print()
print("  ▼ c106 の彩度（見出しがオレンジ色を指す）")
for cid in ["c106", "c108", "c115"]:
    a = load(cid)
    mx, mn = a.max(axis=2), a.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    print(f"  {cid}: 彩度の平均 {sat.mean():.3f}／"
          f"彩度0.25超の画素 {100 * (sat > 0.25).mean():5.1f}%")
