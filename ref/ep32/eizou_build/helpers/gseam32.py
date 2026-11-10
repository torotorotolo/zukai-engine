"""32本目 ⑤b-3b：同じ地図を2回撮った A と B を比べる（31本目の `ref/ep31/eizou_build/helpers/gseam31.py` をそのまま写した＝22本目の gseam22 の型）。
  python -I gseam32.py <1回目のフォルダ> <2回目のフォルダ>
以下は31本目の説明のまま：
差の絵の中の「細い横・縦の直線」（瓦の読み込みの途中に撮れた継ぎ目）を探し、その線が A と B のどちらの絵の飛び出し（明るい細線）かを測る。
本物の線（国境・州境・ボタン）は2回とも同じ＝差に出ない。
  python -I gseam31.py <A のフォルダ> <B のフォルダ>     （どちらも gmap_*.png を置いたフォルダ）
🔧 22本目の型からの違い＝見る絵を `gmap_*.png` に（22本目は `gmap_g0*.png`＝G10 を見落とした・30本目 ⑤b-3 の落とし穴）・差の大きさ（平均の絶対差）も出す。
陽性対照（22本目 10-14）＝G03 の継ぎ目の入った1回目と2回目の比べで A 27.5／B 0.0 と出た。
⚠️ 2回とも同じ所に継ぎ目が出ると差に出ない（読み込みの継ぎ目は撮るたびに場所が変わる）"""
import glob
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
A, B = sys.argv[1], sys.argv[2]


def spike(g, ax):
    a = g if ax == 0 else g.T
    return a[2:-2] - (a[:-4] + a[4:]) / 2


def lines(diff, ax, thr=8.0, run=120):
    """差の絵で、明るさの飛び出し（絶対値）が thr を超える画素が run 以上続く行（列）"""
    s = np.abs(spike(diff, ax))
    out = []
    for i in range(s.shape[0]):
        m = s[i] > thr
        if not m.any():
            continue
        best, cur, start, bst = 0, 0, 0, 0
        for x, v in enumerate(m):
            if v:
                if cur == 0:
                    start = x
                cur += 1
                if cur > best:
                    best, bst = cur, start
            else:
                cur = 0
        if best >= run:
            out.append((i + 2, bst, bst + best))
    return out


miss = 0
for pa in sorted(glob.glob(os.path.join(A, "gmap_*.png"))):
    pb = os.path.join(B, os.path.basename(pa))
    if not os.path.exists(pb):
        print(os.path.basename(pa), "｜ 🔴 B に無い")
        miss += 1
        continue
    ga = np.asarray(Image.open(pa).convert("L"), dtype=np.float32)
    gb = np.asarray(Image.open(pb).convert("L"), dtype=np.float32)
    d = ga - gb
    res = []
    for ax, nm in ((0, "横"), (1, "縦")):
        for i, x0, x1 in lines(d, ax):
            sa = float(np.median(spike(ga, ax)[i - 2, x0:x1]))
            sb = float(np.median(spike(gb, ax)[i - 2, x0:x1]))
            res.append(f"{nm}{i}（{x0}〜{x1}）A {sa:.1f}／B {sb:.1f}")
    print(os.path.basename(pa), f"｜ 平均の差 {float(np.abs(d).mean()):.2f}｜", "・".join(res) if res else "差に線なし（2回とも同じ）")
sys.exit(1 if miss else 0)
