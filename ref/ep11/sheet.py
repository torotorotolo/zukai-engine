#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""指定した秒のコマを焼いて、番号と秒を書いた一覧（コンタクトシート）にする。

⚠️ タイルは既定で素材の原寸。縮小すると見落とす（記憶 feedback-sheet-cannot-judge-three-types）。
   SAR が 1:1 でない素材は --sar で正方画素に直してから並べる
   （記憶 feedback-container-labels-lie-about-the-picture）。

使い方:
  python ref/ep11/sheet.py <mp4> <出力.jpg> --times 10,20,30 [--cols 3] [--tile 320x240] [--sar]
"""
import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/consolab.ttf"


def probe_sar(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,sample_aspect_ratio",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True).stdout.split()
    w, h, sar = int(out[0]), int(out[1]), out[2]
    if sar in ("N/A", "0:1"):
        num, den = 1, 1
    else:
        num, den = (int(x) for x in sar.split(":"))
    return w, h, num, den


def grab(path, t, size, sar):
    """t 秒のコマを size=(w,h) で取り出す。sar=True なら正方画素に直してから。"""
    w, h = size
    vf = f"scale={w}:{h}:flags=lanczos"
    if sar:
        vf = "scale=iw*sar:ih,setsar=1," + vf
    p = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-ss", str(t), "-i", str(path),
         "-frames:v", "1", "-vf", vf, "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True)
    import io
    return Image.open(io.BytesIO(p.stdout)).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--times", required=True, help="秒をカンマ区切りで")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--tile", default=None, help="WxH。既定は素材の原寸")
    ap.add_argument("--sar", action="store_true", help="SAR を当てて正方画素に直す")
    ap.add_argument("--labels", default=None, help="タイルの見出しをカンマ区切りで")
    a = ap.parse_args()

    sw, sh, sn, sd = probe_sar(a.src)
    if a.tile:
        tw, th = (int(x) for x in a.tile.lower().split("x"))
    elif a.sar:
        tw, th = round(sw * sn / sd), sh
    else:
        tw, th = sw, sh

    times = [float(x) for x in a.times.split(",")]
    labels = a.labels.split(",") if a.labels else [None] * len(times)
    pad, bar = 4, 22
    cols = a.cols
    rows = (len(times) + cols - 1) // cols
    W = cols * tw + (cols + 1) * pad
    H = rows * (th + bar) + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), (24, 24, 24))
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(FONT, 15)
    except OSError:
        font = ImageFont.load_default()

    for i, t in enumerate(times):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + bar + pad)
        try:
            im = grab(a.src, t, (tw, th), a.sar)
            sheet.paste(im, (x, y))
        except subprocess.CalledProcessError:
            dr.rectangle([x, y, x + tw, y + th], fill=(80, 0, 0))
        mm, ss = divmod(int(t), 60)
        cap = f"[{i + 1:02d}] {mm}:{ss:02d} ({int(t)}s)"
        if labels[i]:
            cap += " " + labels[i]
        dr.text((x + 2, y + th + 3), cap, fill=(255, 235, 120), font=font)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.out, quality=94)
    print(f"{a.out}  {W}x{H}  タイル {tw}x{th}  {len(times)}枚  "
          f"素材 {sw}x{sh} SAR {sn}:{sd}" + ("  → SAR 適用ずみ" if a.sar else "  ⚠️ SAR 未適用"))


if __name__ == "__main__":
    sys.exit(main())
