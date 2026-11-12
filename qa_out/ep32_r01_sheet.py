# -*- coding: utf-8 -*-
"""28本目 ⑥：本編の mp4 からコマを抜いて 640px の 2列×3行 のシートにする（通し検品）。

    python -P qa_out/ep32_r01_sheet.py 出力名 c510@0.5 c510@3.5 c308@-0.2 c309@0.3 …      … <カット>@<カットの頭からの秒>（負はカットの尻から）
    python -P qa_out/ep32_r01_sheet.py --strips 出力名 "c105|78,217,322,252" …             … 原寸の切り出しを並べる（x0,y0,x1,y1）
出力＝qa_out/ep32_r01/<出力名>.jpg・札にカットと mp4 の秒を書く。帳は qa_out/ep32_r01_seen.py（見たら足す）
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
MP4 = HERE / "out" / "jiko" / next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")), "titan_audio-ep32-r01.mp4")
WIN = HERE / "qa_out" / "ep32_r01" / "windows.json"
OUT = HERE / "qa_out" / "ep32_r01"
TMP = OUT / "_frames"
FONT = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)


def windows():
    t, out = 0.0, {}
    for cid, sec, _ in json.loads(WIN.read_text(encoding="utf-8")):
        out[cid] = (t, sec)
        t += sec
    return out


def grab(sec, name):
    TMP.mkdir(exist_ok=True)
    p = TMP / f"{name}.png"
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{sec:.3f}", "-i", str(MP4),
                        "-frames:v", "1", str(p)], capture_output=True, text=True)
    if r.returncode or not p.exists():
        raise SystemExit(f"🔴 コマを抜けない {name}: {r.stderr[:200]}")
    return p


def sheet(name, items):
    win = windows()
    w, h = 640, 360
    cols, rows = 2, (len(items) + 1) // 2
    im = Image.new("RGB", (w * cols, h * rows), "#111")
    d = ImageDraw.Draw(im)
    for i, it in enumerate(items):
        cid, at = it.split("@")
        t0, sec = win[cid]
        off = float(at)
        s = t0 + (off if off >= 0 else sec + off)
        p = grab(s, f"{cid}_{at}")
        f = Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS)
        x, y = w * (i % cols), h * (i // cols)
        im.paste(f, (x, y))
        lab = f"{cid} @{at}  {int(s // 60)}:{s % 60:05.2f}"
        d.rectangle((x, y, x + 12 * len(lab) + 14, y + 30), fill="#000")
        d.text((x + 6, y + 1), lab, font=FONT, fill="#ff0")
    p = OUT / f"{name}.jpg"
    im.save(p, quality=90)
    print(p, im.size)


def strips(name, items):
    frames = HERE / "out" / "jiko" / "ep32_r01_frames"
    cells = []
    for it in items:
        cid, box = it.split("|")
        x0, y0, x1, y1 = map(int, box.split(","))
        cells.append((cid, Image.open(frames / f"cut_{cid}.jpg").convert("RGB").crop((x0, y0, x1, y1))))
    W, PAD, LAB = 1280, 6, 24
    x, y, rowh, rows = 0, 0, 0, []
    for cid, c in cells:
        cw, ch = c.size
        if x + cw + PAD > W:
            y += rowh + LAB + PAD
            x, rowh = 0, 0
        rows.append((cid, c, x, y))
        x += cw + PAD
        rowh = max(rowh, ch)
    H = y + rowh + LAB + PAD
    im = Image.new("RGB", (W, H), "#333")
    d = ImageDraw.Draw(im)
    small = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 16)
    for cid, c, x, y in rows:
        d.text((x + 2, y), cid, font=small, fill="#ff0")
        im.paste(c, (x, y + LAB))
    p = OUT / f"{name}.jpg"
    im.save(p, quality=92)
    print(p, im.size)


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--mp4=")]
    if a[0] == "--strips":
        strips(a[1], a[2:])
    else:
        sheet(a[0], a[1:])
