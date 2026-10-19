# -*- coding: utf-8 -*-
"""23本目 ⑥ 通し検品：個人名義の10カットの出典の行（作者欄の名前＝Modal の本編で初めて入る）を、本編の mp4 から**原寸**で切り出して1枚に積む。

なぜ：Actions の検品の焼きは仮の字「〇〇〇」＝作者の名前の入った絵は誰も見ていない（10カット）。カットを丸ごと読むと画像が10枚になるので、
     出典の行の帯（額装は右下＝右端 x=1848・基線 y=888＝`scene_jiko.PANEL_CRED_Y`・24px）だけを原寸で切って積む。
時刻＝`qa_out/ep23_r01/windows.json` のカットの真ん中（扉の後）。
⚠️ 名前はファイルに書かない（リポは公開）＝画面に出すだけ。見た枚は `qa_out/ep23_r01/seen.tsv` に機械で足す。

    python qa_out/ep23_r01_credcrop.py [--mp4=titan_audio-ep23-r01.mp4]   → out/jiko/sheet_ep23_r01/cred_names.png
"""
import json
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
CUTS = ["c107", "c406", "c410", "c508", "c510", "c801", "ca10", "ca19", "cb10", "cb14"]
BOX = (640, 838, 1900, 906)          # 出典の行の帯（原寸・字幕帯 892〜の上端も少し入れる）
WIN = HERE / "qa_out" / "ep23_r01" / "windows.json"
OUT = HERE / "out" / "jiko" / "sheet_ep23_r01"


def frame(mp4, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"🔴 {t:.3f}秒のコマが取れない")
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def main():
    mp4 = HERE / "out" / "jiko" / next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")),
                                       "titan_audio-ep23-r01.mp4")
    if not mp4.exists():
        raise SystemExit(f"🔴 {mp4} が無い")
    t, at = 0.0, {}
    for cid, sec, off in json.loads(WIN.read_text(encoding="utf-8")):
        at[cid] = t + off + (sec - off) / 2
        t += sec
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    except OSError:
        font = ImageFont.load_default()
    bw, bh, lab = BOX[2] - BOX[0], BOX[3] - BOX[1], 30
    sheet = Image.new("RGB", (bw, (bh + lab) * len(CUTS)), "#222")
    d = ImageDraw.Draw(sheet)
    for i, c in enumerate(CUTS):
        im = frame(mp4, at[c]).crop(BOX)
        y = i * (bh + lab)
        d.text((6, y + 3), f"{c}  {int(at[c] // 60)}:{at[c] % 60:05.2f}（原寸 x{BOX[0]}〜{BOX[2]}・y{BOX[1]}〜{BOX[3]}）",
               fill="#ff0", font=font)
        sheet.paste(im, (0, y + lab))
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "cred_names.png"
    sheet.save(p)
    seen = HERE / "qa_out" / "ep23_r01" / "seen.tsv"
    with seen.open("a", encoding="utf-8") as f:
        f.write(f"{p.name}\t{','.join(CUTS)}\t出典の行の帯（原寸）\n")
    print(f"→ {p.relative_to(HERE)}  {sheet.size}")


if __name__ == "__main__":
    main()
