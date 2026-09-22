# -*- coding: utf-8 -*-
"""12本目②：動く映像に「焼き込まれた透かし・ロゴ」が在るかを機械で出す。

なぜ目で見ないか
  透かしは半透明で小さく、原寸で見ても見落とす。**コマをまたいで動かない**という
  性質のほうが確実に拾える。
  → 画面全体の**時間方向のばらつき（標準偏差）**を取り、
     周りが動いているのにそこだけ動かない区画を探す。

出すもの
  - 16x16 の区画ごとの「時間方向の標準偏差」の表
  - いちばん動かない区画の位置（＝透かしの当たり）
  - `wm_mean.png`（全コマの平均）と `wm_std.png`（ばらつき）＝最後に目で1回見る
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
N = int(sys.argv[3]) if len(sys.argv) > 3 else 40
DUR = float(sys.argv[4]) if len(sys.argv) > 4 else 56.0

# 小さく（幅960）取り出す。透かしの「位置」を出すのが目的なので原寸は要らない
W, H = 960, 540


def frames():
    pat = OUT / "wmf_%03d.png"
    if not (OUT / "wmf_001.png").exists():
        fps = N / DUR
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC),
                        "-vf", "fps=%.4f,scale=%d:%d" % (fps, W, H),
                        "-frames:v", str(N), "-y", str(pat)], check=True)
    return sorted(OUT.glob("wmf_*.png"))


def main():
    fs = frames()
    print("読んだコマ %d 枚" % len(fs))
    arr = np.stack([np.asarray(Image.open(f).convert("L"), dtype=np.float32)
                    for f in fs])
    std = arr.std(axis=0)
    mean = arr.mean(axis=0)

    Image.fromarray(mean.astype(np.uint8)).save(OUT / "wm_mean.png")
    # ばらつきは小さいので引き伸ばして見えるようにする
    s = std / max(std.max(), 1e-6) * 255.0
    Image.fromarray(s.astype(np.uint8)).save(OUT / "wm_std.png")

    # 区画ごと（16x16 マス）
    by, bx = H // 16, W // 16
    print("\n== 区画ごとの時間方向の標準偏差（小さい＝動いていない）==")
    grid = np.zeros((16, 16))
    for i in range(16):
        for j in range(16):
            grid[i, j] = std[i * by:(i + 1) * by, j * bx:(j + 1) * bx].mean()
    for i in range(16):
        print(" ".join("%5.1f" % v for v in grid[i]))

    flat = [(grid[i, j], i, j) for i in range(16) for j in range(16)]
    flat.sort()
    print("\n動かない区画 上位8（値 / 行 / 列 / 画面上の位置）")
    for v, i, j in flat[:8]:
        print("  %6.2f  行%2d 列%2d  x=%d..%d y=%d..%d"
              % (v, i, j, j * bx, (j + 1) * bx, i * by, (i + 1) * by))
    print("\n全体の標準偏差 中央値 %.2f / 最大 %.2f" % (np.median(grid), grid.max()))

    # 平均画像の中で「周りより明るく、かつ動かない」＝ロゴの当たり
    bright_static = (mean > np.percentile(mean, 75)) & (std < np.percentile(std, 10))
    ys, xs = np.nonzero(bright_static)
    print("『明るいのに動かない』画素 %d 個 / 全 %d" % (len(ys), mean.size))
    if len(ys):
        print("  かたまりの範囲  x=%d..%d  y=%d..%d（幅%d・画面比 %.3f）"
              % (xs.min(), xs.max(), ys.min(), ys.max(),
                 xs.max() - xs.min(), (xs.max() - xs.min()) / W))


if __name__ == "__main__":
    main()
