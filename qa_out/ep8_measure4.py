# -*- coding: utf-8 -*-
"""ep8 ⑤c' ── 残り（ep01/ep02・c705系・c505/c414・c913・c309/c315）を測る。

⚠️ 「同じ絵か」は**素材そのもの**を突き合わせる（焼けた絵は見出しが違うので
   全画面の画素差では決まらない＝[[feedback-duplicate-art-needs-pixel-comparison]]）。
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
import check_slide as CS  # noqa: E402

REF = ROOT / "ref" / "ep8"
QA = ROOT / "out/jiko/qa_ep8-r01"
sm, po, bo, skip = CS.production_inputs()


def src(n, size=(480, 270)):
    with Image.open(REF / n) as im:
        return np.asarray(im.convert("RGB").resize(size, Image.LANCZOS)
                          ).astype(np.float64)


print("=" * 78)
print("■ 1. 素材そのものを突き合わせる（同じ大きさへそろえて比べる）")
print("=" * 78)
GROUPS = [("ひかえの静止画 ep01/ep02", ["fb_ep01.jpg", "fb_ep02.jpg"]),
          ("第7章の再現映像 4件", ["fb_c705.jpg", "fb_c711.jpg",
                                   "fb_c715.jpg", "fb_c717.jpg"]),
          ("陽性対照（別物）", ["fb_ep01.jpg", "fb_c725.jpg"])]
for title, names in GROUPS:
    print(f"  ▼ {title}")
    ims = {n: src(n) for n in names}
    for i, a_ in enumerate(names):
        for b_ in names[i + 1:]:
            d = np.abs(ims[a_] - ims[b_])
            g1 = ims[a_].mean(axis=2)
            g2 = ims[b_].mean(axis=2)
            corr = float(np.corrcoef(g1.ravel(), g2.ravel())[0, 1])
            v = ("🔴🔴 ほぼ同じ" if d.mean() < 4 else
                 "⚠️ 似ている" if d.mean() < 12 else "・ 別物")
            print(f"     {a_:<14} × {b_:<14} 平均差 {d.mean():6.2f}  "
                  f"相関 {corr:+.3f}  {v}")
    print()

print("=" * 78)
print("■ 2. people の札 ── c505 と c414（同じ作り）")
print("=" * 78)
print("  （people は札の幅が node の間隔で決まる。字数と、収まる級数を出す）")
for cid, nodes, n in [("c414", ["地上の担当", "機長", "乗員全員"], 3),
                      ("c505", ["写真作業班の長", "請負会社の管理者",
                                "ロッチャ技師", "飛行中の判断をする側"], 4)]:
    print(f"  {cid}（{n}人）")
    for t in nodes:
        for w in (240, 300, 360):
            pass
        s240 = fm.fit(t, 240, "Noto", cap=40, floor=18)
        s300 = fm.fit(t, 300, "Noto", cap=40, floor=18)
        print(f"      {t}（{len(t)}字）… 幅240で {s240:2.0f}px ／ 幅300で {s300:2.0f}px")
    print()

print("=" * 78)
print("■ 3. c913 panel ── 3段目だけ小さいか（式で出す）")
print("=" * 78)
blocks = [("勧告", "全部で", "29件"), ("そのうち", "次の打ち上げの前に", "15件"),
          ("中身の例", "3方向以上から撮る／RCCは全部調べる／"
                       "軌道の上でも調べて直す備え", "")]
for k, t, v in blocks:
    s = fm.fit(t, TF.BW / 3 * 0.92, "Noto", cap=44, floor=18)
    print(f"  「{k}」… 本文 {len(t):2d}字 → 級数 {s:2.0f}px   値={v or '（無し）'}")
print()

print("=" * 78)
print("■ 4. c309 / c315 ── 同じ素材・窓が少し違う。明るさの差")
print("=" * 78)
for cid in ("c309", "c315"):
    spec = sm[cid]
    with Image.open(QA / f"cut_{cid}.jpg") as im:
        a = np.asarray(im.convert("RGB")).astype(np.float64)
    box = bo[cid]
    sub = a[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
    print(f"  {cid}: 貼り箱 {box}  写真の明るさ 平均 {sub.mean():6.2f}／"
          f"標準偏差 {sub.std():6.2f}   veil={spec.get('veil')} zoom={spec.get('zoom',1.0)}")
