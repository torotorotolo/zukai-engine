# -*- coding: utf-8 -*-
"""12本目②：「4K 56.9秒」の器の札が、絵について本当のことを言っているかを測る。

なぜ測るか
  ①はこの1点（3840x2160・PD・爆発そのもの）を題材選定の決め手にした。
  ところが Commons の頁は
    - 出どころ＝**YouTube の再アップ**（ペルーの ch `TheCentralnuclear`・video2commons 取り込み）
    - 隠しカテゴリ＝**Images with watermarks**（透かし入り）
    - 権利の根拠＝**PD US not renewed**（米連邦§105 ではない）
  と書いている。1954年の素材が本当に 3840x2160 で在るはずがない。
  → [[feedback-container-labels-lie-about-the-picture]]（幅そのものが嘘をつく）

測り方（実効解像度）
  原寸のコマを 1/k に縮めてから元の大きさへ戻し、原寸との差（RMSE）を測る。
  **本物の 4K** なら k を上げるほど差が大きくなる。
  **N倍に引き伸ばしただけ**なら、k=N まで差がほぼ 0 のまま＝そこが「実効の幅」。
  陽性対照＝同じコマを自分で 8倍に引き伸ばした画像（差が 0 に張り付くことを見る）。
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
TIMES = sys.argv[3:] or ["2", "10", "20", "30", "45", "55"]


def grab(t):
    p = OUT / ("f%s.png" % t.replace(".", "_"))
    if not p.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", str(SRC),
                        "-frames:v", "1", "-y", str(p)], check=True)
    return p


def rmse(a, b):
    return float(np.sqrt(np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2)))


def effective(img):
    """縮めて戻したときの差を k ごとに出す。"""
    g = np.asarray(img.convert("L"))
    h, w = g.shape
    res = []
    for k in (2, 3, 4, 5, 6, 8, 12):
        small = img.convert("L").resize((max(1, w // k), max(1, h // k)),
                                        Image.LANCZOS)
        back = small.resize((w, h), Image.LANCZOS)
        res.append((k, w // k, rmse(g, np.asarray(back))))
    return res


def main():
    print("== ffprobe ==")
    print(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_name,width,height,r_frame_rate,avg_frame_rate,pix_fmt",
         "-of", "default=noprint_wrappers=1", str(SRC)],
        capture_output=True, text=True).stdout.strip())

    print("\n== 実効解像度（縮めて戻した差 RMSE。0 に近い＝その幅より上に中身が無い）==")
    print("%-6s %-9s %s" % ("秒", "戻す幅", "  k=2      k=3      k=4      k=5      k=6      k=8      k=12"))
    for t in TIMES:
        img = Image.open(grab(t))
        r = effective(img)
        print("%-6s %-9s %s" % (t, "%dx%d" % img.size,
                                "  ".join("%7.3f" % v for _, _, v in r)))
    print("   （k の下の幅＝ %s）"
          % " / ".join("k%d:%d" % (k, ww) for k, ww, _ in r))

    # 陽性対照＝1/8 に縮めた絵を 8倍に戻したもの。本物でないことが分かる物差しか見る
    img = Image.open(grab(TIMES[len(TIMES) // 2]))
    w, h = img.size
    fake = img.convert("L").resize((w // 8, h // 8), Image.LANCZOS).resize((w, h), Image.LANCZOS)
    print("\n== 陽性対照（自分で 1/8 に落としてから8倍に戻した絵）==")
    print("%-6s %-9s %s" % ("対照", "%dx%d" % (w, h),
                            "  ".join("%7.3f" % v for _, _, v in effective(fake))))


if __name__ == "__main__":
    main()
