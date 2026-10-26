# -*- coding: utf-8 -*-
"""25本目 ⑥ 通し検品：個人名義のカット（C3＝CC BY 3.0・c913・cb01）の出典の行（作者欄の名前＝Modal の本編で初めて入る）を、
本編の mp4 から**原寸**で切り出して積む（24本目 `ep24_r01_credcrop.py` の写し）。
なぜ：Actions の検品の焼きは仮の字「〇〇〇」＝作者の名前の入った絵は誰も見ていない。出典の行の帯だけを原寸で切って1枚に積む。
     全画面＝左端 `J.MG`・基線 `scene_jiko.CRED_Y`（下に暗い地）。幅は本番の字幅（fontmetrics）。
時刻＝`qa_out/ep25_r01/windows.json` のカットの真ん中（扉の後）と終わりの近く（2点）。
⚠️ 名前はファイルに書かない（リポは公開）＝画面に出すだけ。見た枚は `qa_out/ep25_r01/seen.tsv` に機械で足す。
    python qa_out/ep25_r01_credcrop.py [--mp4=…]   → out/jiko/sheet_ep25_r01/cred_names_1.png
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
# 作者の印 `{作者}` のある写真を使うカット（⑥ の模擬 ep25_credits_sim で数えた＝印の写真 1/1・それを使うカット 2・photo／ground 以外の鍵 0）
CUTS = ("c913", "cb01")
WIN = HERE / "qa_out" / "ep25_r01" / "windows.json"
OUT = HERE / "out" / "jiko" / "sheet_ep25_r01"


def frame(mp4, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"🔴 {t:.3f}秒のコマが取れない")
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def boxes():
    """カット → (x0, y0, x1, y1, 型)。本番の出典の行の置き方と字幅から。"""
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
    arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")), "titan_audio-ep25-r01.mp4")
    mp4 = HERE / "out" / "jiko" / arg
    if not mp4.exists():
        raise SystemExit(f"🔴 {mp4} が無い")
    t, at = 0.0, {}
    for cid, sec, off in json.loads(WIN.read_text(encoding="utf-8")):
        at[cid] = (t + off + (sec - off) / 2, t + sec - 0.5)
        t += sec
    bx = boxes()
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    lab = 30
    OUT.mkdir(parents=True, exist_ok=True)
    seen = HERE / "qa_out" / "ep25_r01" / "seen.tsv"
    rows = [(c, s) for c in CUTS for s in at[c]]
    ww = max(bx[c][2] - bx[c][0] for c in CUTS)
    hh = sum(bx[c][3] - bx[c][1] + lab for c, _ in rows)
    sheet = Image.new("RGB", (ww, hh), "#222")
    d = ImageDraw.Draw(sheet)
    y = 0
    for c, s in rows:
        x0, y0, x1, y1, kind = bx[c]
        im = frame(mp4, s).crop((x0, y0, x1, y1))
        d.text((6, y + 3), f"{c}  {int(s // 60)}:{s % 60:05.2f}  {kind}（原寸 x{x0}〜{x1}・y{y0}〜{y1}）", fill="#ff0", font=font)
        sheet.paste(im, (0, y + lab))
        y += y1 - y0 + lab
    p = OUT / "cred_names_1.png"
    sheet.save(p)
    with seen.open("a", encoding="utf-8") as f:
        f.write(f"{p.name}\t{','.join(CUTS)}\t出典の行の帯（原寸・真ん中と終わり）\n")
    print(f"→ {p.relative_to(HERE)}  {sheet.size}")


if __name__ == "__main__":
    main()
