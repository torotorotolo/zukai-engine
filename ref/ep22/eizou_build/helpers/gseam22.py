"""22本目 ⑤b-1（2026-10-14）：同じ地図を2回撮った A と B を比べる＝差の絵の中の「細い横・縦の直線」（瓦の読み込みの途中に撮れた
継ぎ目）を探し、その線が A と B のどちらの絵の飛び出し（明るい細線）かを測る。本物の線（国境・州境・ボタン）は2回とも同じ＝差に出ない。
  python -I gseam22.py <A のフォルダ> <B のフォルダ>     （どちらも gmap_g0*.png を置いたフォルダ）
陽性対照（10-14）＝G03 の継ぎ目の入った1回目（y 751・x 1669〜1920・飛び出し 27.5）と2回目の比べで A 27.5／B 0.0 と出た。
⚠️ 2回とも同じ所に継ぎ目が出ると差に出ない（読み込みの継ぎ目は撮るたびに場所が変わる＝実測で G03・G05 とも別の所）"""
import glob, os, sys
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
        # いちばん長い連なり
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


for pa in sorted(glob.glob(os.path.join(A, "gmap_g0*.png"))):
    pb = os.path.join(B, os.path.basename(pa))
    ga = np.asarray(Image.open(pa).convert("L"), dtype=np.float32)
    gb = np.asarray(Image.open(pb).convert("L"), dtype=np.float32)
    d = ga - gb
    res = []
    for ax, nm in ((0, "横"), (1, "縦")):
        for i, x0, x1 in lines(d, ax):
            sa = float(np.median(spike(ga, ax)[i - 2, x0:x1]))
            sb = float(np.median(spike(gb, ax)[i - 2, x0:x1]))
            res.append(f"{nm}{i}（{x0}〜{x1}）A {sa:.1f}／B {sb:.1f}")
    print(os.path.basename(pa), "｜", "・".join(res) if res else "差に線なし（2回とも同じ）")
