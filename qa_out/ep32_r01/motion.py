# -*- coding: utf-8 -*-
"""29本目 ⑥：名指しのカットの動きを本編の mp4 で数える（⑤c' は「コマだけ」で動きを見ていない＝c211 c318 c320 c706）。
コマどうしの差を 480x270 の灰色で測る：
  ・同じコマ（差 < DUP）の数と、1秒あたりの違う絵の枚数＝カクつき（c211 の 0.93倍速は setpts でコマが複製される）
  ・差の中央値に対する最大の比＝飛び（途中で絵が跳ぶ）
    python -P qa_out/ep32_r01/motion.py <mp4> c211 c318 c320 c706 [--raw]
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
W, H, FPS, DUP = 480, 270, 30, 0.02
args = [a for a in sys.argv[1:] if not a.startswith("--")]
mp4, cuts = args[0], args[1:]
win = json.loads((ROOT / "qa_out" / "ep32_r01" / "windows.json").read_text(encoding="utf-8"))
t, starts = 0.0, {}
for row in win:
    cid, dur = row[0], row[1]
    starts[cid] = (t, dur)
    t += dur      # 3列目は扉の秒で、尺の内＝足さない
for cid in cuts:
    s, d = starts[cid]
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", mp4, "-vf", f"scale={W}:{H}",
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.float32)
    # 字幕の帯と右上の札で差が出ないよう、画面の中ほど（縦 20〜78%・横 5〜78%）で測る
    roi = a[:, int(H * 0.20):int(H * 0.78), int(W * 0.05):int(W * 0.78)]
    df = np.abs(np.diff(roi, axis=0)).mean(axis=(1, 2))
    dup = int((df < DUP).sum())
    med = float(np.median(df))
    print(f"{cid}: {s:7.2f}s 尺 {d:5.2f}s コマ {len(a)}  同じコマ {dup}（{dup / max(1, len(df)) * 100:4.1f}%）"
          f"・違う絵 {(len(df) - dup) / d:4.1f} 枚/秒・差 中央値 {med:.3f}・最大 {df.max():.3f}（{df.max() / max(med, 1e-3):5.1f}倍・{np.argmax(df) / FPS:5.2f}秒）")
    if "--raw" in sys.argv:
        print("   " + " ".join(f"{x:.2f}" for x in df[:: max(1, len(df) // 40)]))
