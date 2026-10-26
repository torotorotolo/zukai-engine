# -*- coding: utf-8 -*-
"""25本目 ⑥：照合（`vs_qa.tsv`）で差が目立ったカットの「差が画面のどこにあるか」を原寸で測る（24本目 `ep24_r01_where.py` の写し）。

本編のコマ（t_mp4）と静止画を原寸で引き、48×48 の升目ごとの差の平均を出して、大きい升目の範囲（外接の箱）と上位の升目を並べる。
⚠️ 静止画は JPEG・本編は H.264 ＝0 にはならない。升目の差が 25 を超える所だけを数える。
⚠️ 動く絵（寄り・流し）は `-ss` の1コマが前後にずれて差が大きく出る（24本目 ⑥）＝`--shift` で前後±4コマを頭から復号して照らし直す。

    python qa_out/ep25_r01_where.py c416,c528 [--mp4=…] [--shift]
    python qa_out/ep25_r01_where.py --top=12 [--shift]   … vs_qa.tsv の局所の差の大きい順に12カット
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
TSV = HERE / "qa_out" / "ep25_r01" / "vs_qa.tsv"
G, TH = 48, 25.0


def frames(mp4, t, n=1):
    """t から n コマ（頭から正確に復号＝-ss を -i の後ろ）。"""
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0.0, t - 2):.3f}", "-i", str(mp4), "-ss", f"{min(2.0, t):.3f}",
                        "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    fb = 1920 * 1080 * 3
    if r.returncode or len(r.stdout) < fb:
        raise SystemExit(f"🔴 {t:.3f}秒のコマが取れない")
    return [np.frombuffer(r.stdout[k * fb:(k + 1) * fb], np.uint8).reshape(1080, 1920, 3).astype(np.int16)
            for k in range(len(r.stdout) // fb)]


def main():
    rows = {r["cut"]: r for r in csv.DictReader(TSV.open(encoding="utf-8"), delimiter="\t")}
    top = next((int(a.split("=", 1)[1]) for a in sys.argv[1:] if a.startswith("--top=")), 0)
    cuts = list(rows)[:top] if top else [c for c in sys.argv[1].split(",") if c]
    mp4 = HERE / "out" / "jiko" / next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")),
                                       "titan_audio-ep25-r01.mp4")
    shift = "--shift" in sys.argv
    for c in cuts:
        r = rows[c]
        name = f"{c}.png" if c.startswith("card_") else f"cut_{c}.jpg"
        b = np.asarray(Image.open(HERE / "out" / "jiko" / r["qa"] / name).convert("RGB"), np.int16)
        t = float(r["t_mp4"])
        cands = frames(mp4, t - 4 / 30, 9) if shift else frames(mp4, t, 1)
        best = None
        for k, a in enumerate(cands):
            d = np.abs(a - b).mean(axis=2)
            if best is None or d.mean() < best[0]:
                best = (float(d.mean()), k, d)
        mad, k, d = best
        hh, ww = (d.shape[0] // G) * G, (d.shape[1] // G) * G
        blk = d[:hh, :ww].reshape(hh // G, G, ww // G, G).mean(axis=(1, 3))
        ys, xs = np.where(blk > TH)
        tp = sorted(((float(blk[y, x]), x * G, y * G) for y, x in zip(ys, xs)), reverse=True)[:6]
        box = (int(xs.min()) * G, int(ys.min()) * G, int(xs.max() + 1) * G, int(ys.max() + 1) * G) if len(xs) else None
        sh = f"・ずらし {k - 4:+d}コマ" if shift else ""
        print(f"{c}: 全体の差 {mad:.2f}{sh}・升目>{TH:.0f} が {len(xs)} 個（全 {blk.size}）・範囲 {box}・"
              f"上位 {[(round(v, 1), x, y) for v, x, y in tp]}")


if __name__ == "__main__":
    main()
