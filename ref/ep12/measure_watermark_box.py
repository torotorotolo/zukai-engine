# -*- coding: utf-8 -*-
"""12本目②：焼き込まれた透かしの正確な枠を測る（切って逃げられるかを決めるため）。

⚠️ 先に書いた `find_watermark.py`（コマ間の分散）は**この透かしを見落とした**。
   半透明の字が「動いている海」の上に乗っているので、区画の分散が下がらない。
   → [[feedback-verify-your-own-instrument]]（門番が0件でも目で見る／物差しをまず疑う）

ここで使う物差し＝**コマ間で動かない「輪郭」**。
   字の縁は毎コマ同じ位置に立つので、
   「各コマを高域通過（周りとの差）した絵」を**コマ方向の最小値**で畳むと、
   動く波の縁は消え、**動かない字の縁だけが残る**。
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
N = int(sys.argv[3]) if len(sys.argv) > 3 else 24


def frames():
    pat = OUT / "bx_%03d.png"
    if not (OUT / "bx_001.png").exists():
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC),
                        "-vf", "fps=%.4f" % (N / 56.0),
                        "-frames:v", str(N), "-y", str(pat)], check=True)
    return sorted(OUT.glob("bx_*.png"))


def highpass(a):
    """3x3 の平均との差の絶対値（原寸のまま）。"""
    p = np.pad(a, 1, mode="edge")
    m = (p[:-2, :-2] + p[:-2, 1:-1] + p[:-2, 2:] +
         p[1:-1, :-2] + p[1:-1, 1:-1] + p[1:-1, 2:] +
         p[2:, :-2] + p[2:, 1:-1] + p[2:, 2:]) / 9.0
    return np.abs(a - m)


def main():
    fs = frames()
    print("コマ %d 枚（原寸）" % len(fs))
    acc = None
    for f in fs:
        a = np.asarray(Image.open(f).convert("L"), dtype=np.float32)
        hp = highpass(a)
        acc = hp if acc is None else np.minimum(acc, hp)
    h, w = acc.shape
    print("画面 %dx%d / 動かない輪郭の 中央値 %.3f 最大 %.3f"
          % (w, h, float(np.median(acc)), float(acc.max())))

    thr = float(np.percentile(acc, 99.9))
    mask = acc > thr
    ys, xs = np.nonzero(mask)
    print("しきい値 %.3f（上位0.1%%）で残った画素 %d 個" % (thr, len(ys)))

    # 下半分・左半分に絞る（シートで見えた位置）
    sel = (ys > h * 0.5)
    ys2, xs2 = ys[sel], xs[sel]
    if len(ys2):
        print("画面の下半分に残ったもの: x=%d..%d y=%d..%d（%d個）"
              % (xs2.min(), xs2.max(), ys2.min(), ys2.max(), len(ys2)))
        # 行ごとの個数で帯を出す
        rows = np.bincount(ys2, minlength=h)
        band = np.nonzero(rows > np.percentile(rows[rows > 0], 50))[0]
        cols = np.bincount(xs2, minlength=w)
        cband = np.nonzero(cols > 0)[0]
        print("字の帯（行）: y=%d..%d  高さ %d（画面比 %.3f）"
              % (band.min(), band.max(), band.max() - band.min(),
                 (band.max() - band.min()) / h))
        print("字の帯（列）: x=%d..%d  幅   %d（画面比 %.3f）"
              % (cband.min(), cband.max(), cband.max() - cband.min(),
                 (cband.max() - cband.min()) / w))
        print("\n🔴 透かしを外す切り方")
        print("  下を切る  : 高さ %d まで残す → %dx%d" % (band.min(), w, band.min()))
        print("  左を切る  : x=%d から右 → %dx%d" % (cband.max() + 1,
                                                w - cband.max() - 1, h))

    Image.fromarray((np.clip(acc / max(acc.max(), 1e-6) * 255 * 6, 0, 255))
                    .astype(np.uint8)).save(OUT / "static_edges.png")
    print("\n書いた: %s" % (OUT / "static_edges.png"))


if __name__ == "__main__":
    main()
