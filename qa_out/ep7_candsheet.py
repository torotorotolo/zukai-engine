# -*- coding: utf-8 -*-
"""ep7_candsheet.py — 差し替え候補を **640px の 2列×3行シート**にして目で確かめる（2026-09-14）。

■ なぜ要るか
    題名と説明だけで選ぶと別物を掴む（[[feedback-inventory-is-not-usable-material]]）。
    **「主題が写っているか」「大きな顔が主役になっていないか」は 640px で決まる**
    （640px で決まらないのは「図の比例」「小さな点」「札の切れ」の3型だけ
     ＝`qa_out/ep7_qa_look2.md` §C）。だから候補はシートで見る。

■ 使い方
    python qa_out/ep7_candsheet.py          # PLAN の候補を落としてシートを作る
    → out/jiko/ep7_cand/sheet_NN.jpg

■ 🔴 守っていること
    1コマ 640px 以上（縮めない）。2列×3行＝1280×1164（`qa_sheet.py` と同じ理由）。
"""
from __future__ import annotations

import io
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
OUT = HERE / "out" / "jiko" / "ep7_cand"
CW, CH = 640, 360                      # 1コマ（16:9）
COLS, ROWS = 2, 3
CAP = 28                               # 札の高さ

# 欄 → 候補（見る順）。⚠️ 題名は Commons の File: を外した形
PLAN: list[tuple[str, str]] = [
    ("pr10 駐機場", "Southwest 737s parked at Terminal A at DCA (39815401742).jpg"),
    ("c302 767離陸", "N352AA (15113637598).jpg"),
    ("c309 767客室", "Delta 767-400ER Economy Cabin.jpg"),
    ("c320 案内板ORD", "Departure Board at ORD.jpg"),
    ("c320 案内板NY", "Arrivals and departures (Unsplash).jpg"),
    ("pr09 ARTCC画面", "Scope of an ARTCC controller.png"),

    ("c412 中庭2025", "XQ-58A Valkrie displayed at the Pentagon Center Courtyard.jpg"),
    ("c412 中庭2008", "Defense.gov photo essay 080424-D-8901Q-007.jpg"),
    ("c622 野原(1)", "Flight 93 Memorial - panoramio (1).jpg"),
    ("c622 野原(11)", "Flight 93 Memorial - panoramio (11).jpg"),
    ("c622 野原(13)", "Flight 93 Memorial - panoramio (13).jpg"),
    ("c622 野原(15)", "Flight 93 Memorial - panoramio (15).jpg"),

    ("c707 F16駐機", "F-16s Arrive at NATO Air Base Geilenkirchen (8403619).jpg"),
    ("c711 F16離陸", "Colorado and Massachusetts Air National Guard fighter jets "
                     "depart Lithuania during exercise Air Defender 2023 (7867984).jpg"),
    ("c717 F16 2001", "F-16C NJ ANG in flight Oct 2001.jpg"),
    ("c809 記録簿", "Billy Strachan log book.jpg"),
    ("c901 検査場A", "20250507 TSA Security Checkpoint.jpg"),
    ("c901 検査場B(今)", "TSA Security Checkpoint - 54504384636.jpg"),
]

UA = "zukai-engine/1.0 (ep7 candidate sheet; contact via Commons)"


def thumb(name: str, width: int = 1280) -> Image.Image | None:
    url = ("https://commons.wikimedia.org/w/index.php?title=Special:Redirect/file/"
           + urllib.parse.quote(name.replace(" ", "_")) + f"&width={width}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    except Exception as e:                                      # noqa: BLE001
        print(f"  🔴 落とせない: {name[:60]} — {e}")
        return None


def fit(im: Image.Image) -> Image.Image:
    """1コマに**全体が入る**ように収める（切らない＝写っているものを落とさない）。"""
    c = Image.new("RGB", (CW, CH), (26, 28, 32))
    r = min(CW / im.width, CH / im.height)
    im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))),
                   Image.LANCZOS)
    c.paste(im, ((CW - im.width) // 2, (CH - im.height) // 2))
    return c


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
    except Exception:                                           # noqa: BLE001
        font = ImageFont.load_default()
    per = COLS * ROWS
    sheets = 0
    for i in range(0, len(PLAN), per):
        chunk = PLAN[i:i + per]
        sh = Image.new("RGB", (CW * COLS, (CH + CAP) * ROWS), (16, 17, 20))
        d = ImageDraw.Draw(sh)
        for j, (label, name) in enumerate(chunk):
            im = thumb(name)
            x = (j % COLS) * CW
            y = (j // COLS) * (CH + CAP)
            d.text((x + 8, y + 5), f"{label}  |  {name[:64]}", (235, 242, 246), font=font)
            if im is not None:
                sh.paste(fit(im), (x, y + CAP))
            else:
                d.text((x + 20, y + CAP + 160), "（落とせなかった）", (224, 80, 60), font=font)
        sheets += 1
        p = OUT / f"sheet_{sheets:02d}.jpg"
        sh.save(p, quality=92)
        print(f"  ✓ {p}  {sh.width}x{sh.height}  {len(chunk)}コマ")
    print(f"■ シート {sheets}枚 ／ 候補 {len(PLAN)}点")
    return 0


if __name__ == "__main__":
    sys.exit(main())
