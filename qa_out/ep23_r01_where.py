# -*- coding: utf-8 -*-
"""23本目 ⑥：照合（`vs_qa.tsv`）で差が目立ったカットの「差が画面のどこにあるか」を原寸で測る（画像を読む前に当たりを付ける）。

本編のコマ（t_mp4）と静止画を原寸で引き、48×48 の升目ごとの差の平均を出して、大きい升目の範囲（外接の箱）と上位の升目を並べる。
⚠️ 静止画は JPEG・本編は H.264 ＝0 にはならない。升目の差が 25 を超える所だけを数える。

    python qa_out/ep23_r01_where.py c511,c602,c311 [--mp4=titan_audio-ep23-r01.mp4]
"""
import csv
import subprocess
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
TSV = HERE / "qa_out" / "ep23_r01" / "vs_qa.tsv"
G, TH = 48, 25.0


def frame(mp4, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"🔴 {t:.3f}秒のコマが取れない")
    return np.asarray(Image.open(BytesIO(r.stdout)).convert("RGB"), np.int16)


def main():
    cuts = [c for c in sys.argv[1].split(",") if c]
    mp4 = HERE / "out" / "jiko" / next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--mp4=")),
                                       "titan_audio-ep23-r01.mp4")
    rows = {r["cut"]: r for r in csv.DictReader(TSV.open(encoding="utf-8"), delimiter="\t")}
    for c in cuts:
        r = rows[c]
        still = HERE / "out" / "jiko" / r["qa"] / f"cut_{c}.jpg"
        a = frame(mp4, float(r["t_mp4"]))
        b = np.asarray(Image.open(still).convert("RGB"), np.int16)
        if a.shape != b.shape:
            print(f"{c}: 大きさが違う {a.shape} {b.shape}")
            continue
        d = np.abs(a - b).mean(axis=2)
        hh, ww = (d.shape[0] // G) * G, (d.shape[1] // G) * G
        blk = d[:hh, :ww].reshape(hh // G, G, ww // G, G).mean(axis=(1, 3))
        ys, xs = np.where(blk > TH)
        top = sorted(((float(blk[y, x]), x * G, y * G) for y, x in zip(ys, xs)), reverse=True)[:6]
        box = (int(xs.min()) * G, int(ys.min()) * G, int(xs.max() + 1) * G, int(ys.max() + 1) * G) if len(xs) else None
        print(f"{c}: 全体の差 {d.mean():.2f}・升目>{TH:.0f} が {len(xs)} 個（全 {blk.size}）・範囲 {box}・"
              f"上位 {[(round(v, 1), x, y) for v, x, y in top]}  静止画 {r['qa']}")


if __name__ == "__main__":
    main()
