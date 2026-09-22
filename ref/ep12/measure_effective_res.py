# -*- coding: utf-8 -*-
"""12本目②：「3840x2160」に本当に中身があるかを、周波数で測る。

なぜ縮めて戻す方法をやめたか
  `measure_bravo4k.py` の縮小→拡大の差（RMSE）は、**陽性対照が0に張り付かなかった**
  （自分で1/8に落とした絵でも k=8 で 0.638 出た）＝**採否を決められない物差し**だった。
  → [[feedback-verify-your-own-instrument]]

ここで使う物差し＝**半径方向に平均した周波数の強さ**。
  引き伸ばした絵は、元の幅の折り返し（ナイキスト）から上に**中身が無い**ので、
  そこで強さが崖のように落ちる。落ちる位置＝**実効の幅**。

陽性対照を2本立てる（物差しが「何にでも崖がある」と言わないことを見る）
  - 対照A＝同じコマを自分で 1/6 に落として6倍に戻したもの（崖が 1/6 に立つはず）
  - 対照B＝同じコマそのもの（崖が立たない＝原寸に中身がある、が期待）
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")


def spectrum(gray):
    """半径方向に平均した |FFT|。戻り値は 0..0.5 の正規化周波数ごとの強さ。"""
    a = gray.astype(np.float64)
    a = a - a.mean()
    # 窓を掛けないと画面の端が偽の高域を作る
    wy = np.hanning(a.shape[0])[:, None]
    wx = np.hanning(a.shape[1])[None, :]
    F = np.fft.fftshift(np.abs(np.fft.fft2(a * wy * wx)))
    h, w = F.shape
    cy, cx = h // 2, w // 2
    y, x = np.ogrid[:h, :w]
    # 正規化半径（横方向の折り返しを 0.5 とする）
    r = np.sqrt(((y - cy) / h) ** 2 + ((x - cx) / w) ** 2)
    nb = 60
    idx = np.clip((r / 0.5 * nb).astype(int), 0, nb - 1)
    out = np.zeros(nb)
    cnt = np.zeros(nb)
    np.add.at(out, idx.ravel(), F.ravel())
    np.add.at(cnt, idx.ravel(), 1)
    return out / np.maximum(cnt, 1)


def report(name, gray, width):
    s = spectrum(gray)
    s = s / s[1]  # 低域で正規化
    db = 20 * np.log10(np.maximum(s, 1e-12))
    # 「崖」＝低域から -40dB を最初に割った位置
    below = np.nonzero(db < -40)[0]
    cut = below[0] / 60 * 0.5 if len(below) else 0.5
    eff = width * cut * 2
    print("%-28s 崖 %.3f（実効の幅 約 %4.0f px）  "
          "0.10:%6.1f  0.17:%6.1f  0.25:%6.1f  0.33:%6.1f  0.42:%6.1f dB"
          % (name, cut, eff,
             db[int(0.10 / 0.5 * 60)], db[int(0.17 / 0.5 * 60)],
             db[int(0.25 / 0.5 * 60)], db[int(0.33 / 0.5 * 60)],
             db[int(0.42 / 0.5 * 60)]))
    return db


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    times = sys.argv[3:] or ["10", "28", "45"]
    print("周波数 0.5＝画面の折り返し（＝1画素おき）。"
          "-40dB を割る位置が『そこから上に中身が無い』点\n")
    print("%-28s %s" % ("", "（右の数字＝その周波数での強さ dB。小さいほど中身が無い）"))
    for t in times:
        p = out / ("er%s.png" % t)
        if not p.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-ss", t, "-i", str(src),
                            "-frames:v", "1", "-y", str(p)], check=True)
        im = Image.open(p).convert("L")
        g = np.asarray(im)
        report("本物 %ss（%dx%d）" % (t, im.width, im.height), g, im.width)

    # 対照
    im = Image.open(out / ("er%s.png" % times[-1])).convert("L")
    w, h = im.size
    for k in (6, 3):
        fake = im.resize((w // k, h // k), Image.LANCZOS).resize((w, h), Image.LANCZOS)
        report("対照A 自分で1/%d→%d倍に戻す" % (k, k), np.asarray(fake), w)
    # 対照B＝白色雑音（崖が立たない物＝物差しが何にでも崖を言わないか）
    rng = np.random.default_rng(20260922)
    report("対照B 白色雑音（崖なしが正）", rng.integers(0, 256, (h, w)).astype(np.uint8), w)


if __name__ == "__main__":
    main()
