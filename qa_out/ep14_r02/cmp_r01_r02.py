# -*- coding: utf-8 -*-
"""r01（検品の焼き cfix1 と★指紋一致）と r02 を、帯より上（y0〜880）で全編比べる＝字幕以外が同じか。
2本を同時に 3秒おきに読み、1コマずつ比べる（生のコマは保存しない）。
"""
import subprocess
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
R = r"C:/Users/konar/Desktop/zukai-engine/out/jiko/titan_audio-ep14-{}.mp4"
W, H, STEP = 1920, 880, 3.0
N = W * H * 3


def pipe(tag):
    return subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", R.format(tag),
                             "-vf", f"fps=1/{STEP},crop={W}:{H}:0:0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                            stdout=subprocess.PIPE, bufsize=N * 2)


a, b = pipe("r01"), pipe("r02")
rows, i = [], 0
while True:
    x, y = a.stdout.read(N), b.stdout.read(N)
    if len(x) < N or len(y) < N:
        break
    fa = np.frombuffer(x, np.uint8).reshape(H, W, 3).astype(np.int16)
    fb = np.frombuffer(y, np.uint8).reshape(H, W, 3).astype(np.int16)
    d = np.abs(fa - fb).max(axis=2)
    rows.append((i * STEP, float(d.mean()), float((d > 64).mean() * 100), int(d.max())))
    i += 1
a.wait(), b.wait()
pct = sorted(r[2] for r in rows)
mean = sorted(r[1] for r in rows)
print(f"比べたコマ {len(rows)}（{STEP:.0f}秒おき・帯より上 y0〜{H}）")
print(f"差>64 の画素の割合（%）: 中央 {pct[len(pct) // 2]:.3f}・99% 点 {pct[int(len(pct) * 0.99)]:.3f}・最大 {pct[-1]:.3f}")
print(f"平均の差: 中央 {mean[len(mean) // 2]:.2f}・最大 {mean[-1]:.2f}")
for t, m, p, mx in sorted(rows, key=lambda r: -r[2])[:8]:
    print(f"  大きい順 {int(t // 60)}:{t % 60:04.1f}  平均 {m:.2f}・差>64 {p:.3f}%・最大 {mx}")
