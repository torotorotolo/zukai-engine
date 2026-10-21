# -*- coding: utf-8 -*-
"""17本目 ⑥ 通し検品：個人名義の19カットの出典の行（作者欄の名前＝Modal の本編で初めて入る）を、本編の mp4 から**原寸**で切り出して積む
（23本目 `ep23_r01_credcrop.py` の写し・17本目は額装＝右下と全画面＝左下が混ざる＝カットごとに箱を SPEC から決める）。

なぜ：Actions の検品の焼きは仮の字「〇〇〇」＝作者の名前の入った絵は誰も見ていない（19カット）。カットを丸ごと読むと画像が19枚になるので、
     出典の行の帯だけを原寸で切って2枚に積む。
     額装＝右端 `J.RIGHT`・基線 `scene_jiko.PANEL_CRED_Y`／全画面＝左端 `J.MG`・基線 `scene_jiko.CRED_Y`（下に暗い地）。幅は本番の字幅（fontmetrics）。
時刻＝`qa_out/ep17_r01/windows.json` のカットの真ん中（扉の後）。
⚠️ 名前はファイルに書かない（リポは公開）＝画面に出すだけ。見た枚は `qa_out/ep17_r01/seen.tsv` に機械で足す。

    python qa_out/ep17_r01_credcrop.py [--mp4=titan_audio-ep17-r01.mp4]   → out/jiko/sheet_ep17_r01/cred_names_1.png・_2.png
"""
import json
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
CUTS = "c102 c105 c106 c202 c204 c306 c315 c413 c418 c618 c802 c808 c913 c918 ca06 ca18 cb05 cb07 cb30".split()
WIN = HERE / "qa_out" / "ep17_r01" / "windows.json"
OUT = HERE / "out" / "jiko" / "sheet_ep17_r01"
PER = 10                                  # 1枚に積む帯の数


def frame(mp4, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"🔴 {t:.3f}秒のコマが取れない")
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def boxes():
    """カット → (x0, y0, x1, y1, 型)。本番の出典の行の置き方（scene_jiko.full_top）と字幅から。"""
    import os
    os.environ.pop("GITHUB_ACTIONS", None)
    import fontmetrics as fm
    import jiko_style as J
    import scene_jiko as S
    out = {}
    for c in CUTS:
        sp = S.SPEC[c]
        w = fm.width(S.credit_of(c, sp), 24, "Noto")
        if sp.get("panel"):
            y = S.PANEL_CRED_Y
            out[c] = (max(0, int(J.RIGHT - w) - 40), y - 52, min(1920, J.RIGHT + 40), y + 18, "額装・右下")
        else:
            y = S.CRED_Y
            out[c] = (max(0, J.MG - 40), y - 52, min(1920, int(J.MG + w) + 60), y + 18, "全画面・左下")
    return out


def main():
    mp4 = HERE / "out" / "jiko" / next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")),
                                       "titan_audio-ep17-r01.mp4")
    if not mp4.exists():
        raise SystemExit(f"🔴 {mp4} が無い")
    t, at = 0.0, {}
    for cid, sec, off in json.loads(WIN.read_text(encoding="utf-8")):
        at[cid] = t + off + (sec - off) / 2
        t += sec
    bx = boxes()
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    except OSError:
        font = ImageFont.load_default()
    lab = 30
    OUT.mkdir(parents=True, exist_ok=True)
    seen = HERE / "qa_out" / "ep17_r01" / "seen.tsv"
    for k in range(0, len(CUTS), PER):
        part = CUTS[k:k + PER]
        ww = max(bx[c][2] - bx[c][0] for c in part)
        hh = sum(bx[c][3] - bx[c][1] + lab for c in part)
        sheet = Image.new("RGB", (ww, hh), "#222")
        d = ImageDraw.Draw(sheet)
        y = 0
        for c in part:
            x0, y0, x1, y1, kind = bx[c]
            im = frame(mp4, at[c]).crop((x0, y0, x1, y1))
            d.text((6, y + 3), f"{c}  {int(at[c] // 60)}:{at[c] % 60:05.2f}  {kind}（原寸 x{x0}〜{x1}・y{y0}〜{y1}）",
                   fill="#ff0", font=font)
            sheet.paste(im, (0, y + lab))
            y += y1 - y0 + lab
        p = OUT / f"cred_names_{k // PER + 1}.png"
        sheet.save(p)
        with seen.open("a", encoding="utf-8") as f:
            f.write(f"{p.name}\t{','.join(part)}\t出典の行の帯（原寸）\n")
        print(f"→ {p.relative_to(HERE)}  {sheet.size}")


if __name__ == "__main__":
    main()
