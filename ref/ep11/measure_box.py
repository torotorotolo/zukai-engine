#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""コマの中で「本当に絵が出ている長方形」を測る。

🔴🔴 記憶 feedback-container-labels-lie-about-the-picture＝**幅そのものが嘘をつく**。
   器は 720x480 と名乗っていても、額（ピラーボックス）に入っていれば
   実効の絵は 450x480 しかない、ということが起きる。門番は1本も鳴らない。

⚠️ 「青でない最初の列」で測ると外側の黒い走査端に当たって幅100%と出る
   （2026-09-21 ⑤c で実際に踏んだ）。**中身のある列の最長の連なり**で測る。

使い方:
  python ref/ep11/measure_box.py <動画> --times 9,28 [--std 6] [--json out.json]
"""
import argparse
import io
import json
import subprocess
import sys

import numpy as np
from PIL import Image


def frame(path, t):
    p = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-ss", str(t), "-i", str(path),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True)
    return np.asarray(Image.open(io.BytesIO(p.stdout)).convert("RGB")).astype(float)


def longest_run(mask):
    """True の最長の連なりを (始まり, 終わり) で返す。"""
    best = cur = None
    bl = 0
    for i, v in enumerate(mask):
        if v:
            cur = i if cur is None else cur
        else:
            if cur is not None and i - cur > bl:
                bl, best = i - cur, (cur, i - 1)
            cur = None
    if cur is not None and len(mask) - cur > bl:
        bl, best = len(mask) - cur, (cur, len(mask) - 1)
    return best if best else (0, len(mask) - 1)


def active_rect(a, std_min):
    """列・行それぞれの ばらつき から、絵のある長方形を出す。

    帯（黒・単色の青・黄色の罫）は ばらつき が小さい。絵は大きい。
    """
    g = a.mean(axis=2)
    cols = g.std(axis=0)
    rows = g.std(axis=1)
    x0, x1 = longest_run(cols > std_min)
    y0, y1 = longest_run(rows > std_min)
    return x0, y0, x1, y1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--times", required=True)
    ap.add_argument("--std", type=float, default=6.0)
    ap.add_argument("--json")
    ap.add_argument("--min-frac", type=float, default=0.90,
                    help="この割合を下回ったら 🔴 を付ける")
    a = ap.parse_args()

    out = []
    bad = 0
    for t in (float(x) for x in a.times.split(",")):
        im = frame(a.src, t)
        h, w, _ = im.shape
        x0, y0, x1, y1 = active_rect(im, a.std)
        aw, ah = x1 - x0 + 1, y1 - y0 + 1
        frac = aw / w
        flag = "🔴 額入り" if frac < a.min_frac else "✅ 全画面"
        if frac < a.min_frac:
            bad += 1
        print(f"  {t:7.1f}s  器 {w}x{h} → 絵 {aw}x{ah}  "
              f"crop={aw}:{ah}:{x0}:{y0}  幅 {frac * 100:.1f}%  {flag}")
        out.append(dict(t=t, w=w, h=h, x=x0, y=y0, aw=aw, ah=ah, frac=round(frac, 4)))

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"\n額入り {bad} / {len(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
