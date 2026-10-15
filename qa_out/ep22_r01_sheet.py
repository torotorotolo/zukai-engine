# -*- coding: utf-8 -*-
"""22本目 ⑥ 通し検品：本編の mp4 からコマを抜いて 640px の2列×3行に並べる（事故検証ch の例外＝640px のシートで全数・疑いだけ原寸）。

時刻は `qa_out/ep22_r01/vs_qa.tsv` の t_mp4（そのカットの静止画といちばん合うコマ＝検品で見た瞬間）。
扉は `card_<cid>`。見た枚は `qa_out/ep22_r01/seen.tsv` に機械で足す（シートの名・中のカット）。

    python qa_out/ep22_r01_sheet.py <名> <cut,cut,…>      → out/jiko/sheet_ep22_r01/<名>_N.jpg
"""
import csv
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
MP4 = HERE / "out" / "jiko" / "titan_audio-ep22-r01.mp4"
TSV = HERE / "qa_out" / "ep22_r01" / "vs_qa.tsv"
OUT = HERE / "out" / "jiko" / "sheet_ep22_r01"
CW, CH, COLS, ROWS = 640, 360, 2, 3


def frame(t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(MP4), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"🔴 {t:.3f}秒のコマが取れない")
    from io import BytesIO
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def main():
    name, cuts = sys.argv[1], [c for c in sys.argv[2].split(",") if c]
    tm = {r["cut"]: float(r["t_mp4"]) for r in csv.DictReader(TSV.open(encoding="utf-8"), delimiter="\t")}
    miss = [c for c in cuts if c not in tm]
    if miss:
        raise SystemExit(f"🔴 vs_qa.tsv に無いカット: {miss}")
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    except OSError:
        font = ImageFont.load_default()
    seen = HERE / "qa_out" / "ep22_r01" / "seen.tsv"
    per = COLS * ROWS
    for k in range(0, len(cuts), per):
        part = cuts[k:k + per]
        sheet = Image.new("RGB", (CW * COLS, CH * ROWS), "#222")
        d = ImageDraw.Draw(sheet)
        for i, c in enumerate(part):
            t = tm[c]
            im = frame(t).resize((CW, CH), Image.LANCZOS)
            x, y = (i % COLS) * CW, (i // COLS) * CH
            sheet.paste(im, (x, y))
            lab = f"{c}  {int(t // 60)}:{t % 60:05.2f}"
            d.rectangle((x, y, x + 12 + 13 * len(lab), y + 30), fill="#000")
            d.text((x + 6, y + 2), lab, fill="#ff0", font=font)
        p = OUT / f"{name}_{k // per + 1}.jpg"
        sheet.save(p, quality=90)
        with seen.open("a", encoding="utf-8") as f:
            f.write(f"{p.name}\t{','.join(part)}\n")
        print(f"→ {p.relative_to(HERE)}  {','.join(part)}")


if __name__ == "__main__":
    main()
