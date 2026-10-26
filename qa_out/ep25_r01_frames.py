# -*- coding: utf-8 -*-
"""25本目 ⑥ 通し検品：本編の mp4 から、カットの中の時刻（扉の後の割合）のコマを引き、決めた箱を**原寸**で切り出して縦に積む。
    python qa_out/ep25_r01_frames.py <名前> <カット>:<割合>:<x0>,<y0>,<x1>,<y1> […] [--mp4=…]
      例：ca10:0.97:1100,0,1920,1080 c324:0.5:0,0,520,1080   → out/jiko/sheet_ep25_r01/<名前>.png（横に並べる）
時刻＝`qa_out/ep25_r01/windows.json`（扉の後の頭 ＋ 割合 × 中身の秒）。見た枚は `qa_out/ep25_r01_seen.py` で帳に足す。
"""
import json
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
WIN = HERE / "qa_out" / "ep25_r01" / "windows.json"
OUT = HERE / "out" / "jiko" / "sheet_ep25_r01"


def frame(mp4, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"🔴 {t:.3f}秒のコマが取れない")
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    name, specs = args[0], args[1:]
    arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")), "titan_audio-ep25-r01.mp4")
    mp4 = HERE / "out" / "jiko" / arg
    t, at = 0.0, {}
    for cid, sec, off in json.loads(WIN.read_text(encoding="utf-8")):
        at[cid] = (t + off, sec - off)
        t += sec
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    tiles = []
    for s in specs:
        cid, frac, box = s.split(":")
        x0, y0, x1, y1 = map(int, box.split(","))
        head, body = at[cid]
        ts = head + float(frac) * body
        im = frame(mp4, ts).crop((x0, y0, x1, y1))
        tile = Image.new("RGB", (im.width, im.height + 30), "#222")
        ImageDraw.Draw(tile).text((6, 3), f"{cid} {int(ts // 60)}:{ts % 60:05.2f}（{float(frac):.2f}）x{x0}〜{x1} y{y0}〜{y1}",
                                  fill="#ff0", font=font)
        tile.paste(im, (0, 30))
        tiles.append(tile)
    W = sum(x.width for x in tiles) + 12 * (len(tiles) - 1)
    H = max(x.height for x in tiles)
    sheet = Image.new("RGB", (W, H), "#111")
    x = 0
    for tile in tiles:
        sheet.paste(tile, (x, 0))
        x += tile.width + 12
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.png"
    sheet.save(p)
    print(f"→ {p.relative_to(HERE)}  {sheet.size}")


if __name__ == "__main__":
    main()
