# -*- coding: utf-8 -*-
"""32本目 ⑥：⑤c' 周2 のあとに直して焼いて見ていない所（扉 c800card・c900card と c801 の頭）を本編から抜く。
  ① 640px の 2×2＝扉 c801（c800card）・扉 c901（c900card）・c801 の頭（扉が明けた 0.1秒あと）・c801 の尻
  ② 扉2枚の下の端（y 860〜1080）を原寸のまま左右2つずつ＝前に焼き込みの方位の字（「279/ -5 x19.2」「282/ -5 x9.0」）が出ていた所
    python -P qa_out/ep32_r01/doors.py   → qa_out/ep32_r01/doors_640.jpg・doors_bottom.jpg
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
MP4 = ROOT / "out" / "jiko" / "titan_audio-ep32-r01.mp4"
OUT = ROOT / "qa_out" / "ep32_r01"
TMP = OUT / "_frames"
TMP.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)

win, t = {}, 0.0
for cid, sec, card in json.loads((OUT / "windows.json").read_text(encoding="utf-8")):
    win[cid] = (t, sec, card)
    t += sec


def grab(sec, name):
    p = TMP / f"{name}.png"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{sec:.3f}", "-i", str(MP4),
                    "-frames:v", "1", str(p)], check=True)
    return Image.open(p).convert("RGB")


s801, d801, c801 = win["c801"]
s901, d901, c901 = win["c901"]
print(f"c801 頭 {s801:.3f}秒・尺 {d801}・扉 {c801}／c901 頭 {s901:.3f}秒・尺 {d901}・扉 {c901}")
items = [("扉 c801（c800card）", s801 + c801 / 2), ("扉 c901（c900card）", s901 + c901 / 2),
         ("c801 の頭（扉の 0.1秒あと）", s801 + c801 + 0.1), ("c801 の尻（0.1秒前）", s801 + d801 - 0.1)]
frames = [(lab, sec, grab(sec, f"door{i}")) for i, (lab, sec) in enumerate(items)]
sheet = Image.new("RGB", (2 * 640 + 10, 2 * (360 + 30) + 10), "#222")
d = ImageDraw.Draw(sheet)
for i, (lab, sec, im) in enumerate(frames):
    x, y = (i % 2) * 650, (i // 2) * 390
    d.text((x + 4, y + 2), f"{lab}  {int(sec // 60)}:{sec % 60:05.2f}", font=FONT, fill="#ff0")
    sheet.paste(im.resize((640, 360), Image.LANCZOS), (x, y + 30))
sheet.save(OUT / "doors_640.jpg", quality=92)
# ② 扉2枚の下の端を原寸で（左右に分けて 960×220 を4段）
cells = []
for lab, sec, im in frames[:2]:
    for side, (x0, x1) in (("左", (0, 960)), ("右", (960, 1920))):
        cells.append((f"{lab} 下の端・{side}（原寸）", im.crop((x0, 860, x1, 1080))))
bot = Image.new("RGB", (960, len(cells) * (220 + 30)), "#222")
d = ImageDraw.Draw(bot)
for i, (lab, c) in enumerate(cells):
    y = i * 250
    d.text((4, y + 2), lab, font=FONT, fill="#ff0")
    bot.paste(c, (0, y + 30))
bot.save(OUT / "doors_bottom.jpg", quality=92)
print(OUT / "doors_640.jpg", OUT / "doors_bottom.jpg")
