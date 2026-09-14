# -*- coding: utf-8 -*-
"""ep7_cropsheet.py — 「寄せを変えれば使えるか」を 640px のシートで確かめる（2026-09-14）。

■ なぜ要るか
    c901（保安検査場）と c412（ペンタゴンの中庭）は、**自由に使える置き換えが1点も無い**。
    残る手は「いま持っている絵の別の場所を見せる」だけ。
    ⚠️ ただし [[feedback-subtitle-must-match-what-is-visible]]
      ＝**寄りを変えても写っていない物は出てこない**。だから焼く前にここで確かめる。

■ 使い方
    python qa_out/ep7_cropsheet.py
    → out/jiko/ep7_cand/crop_01.jpg
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
OUT = HERE / "out" / "jiko" / "ep7_cand"
CW, CH, CAP = 640, 360, 28

# (札, 元ファイル, (左, 上, 右, 下) の割合)
PLAN = [
    ("c901 検査場 右2/3", "ref/ep7/security_now.jpg", (0.52, 0.05, 1.00, 0.75)),
    ("c901 検査場 右上", "ref/ep7/security_now.jpg", (0.60, 0.00, 1.00, 0.55)),
    ("c412 ペンタゴン俯瞰 中心", "ref/ep7/pentagon_aerial_pre.jpg", (0.30, 0.22, 0.72, 0.86)),
    ("c412 ペンタゴン俯瞰 全体", "ref/ep7/pentagon_aerial_pre.jpg", (0.00, 0.00, 1.00, 1.00)),
    ("c412 いまの中庭(参考)", "ref/ep7/pentagon_court_pre.jpg", (0.00, 0.00, 1.00, 1.00)),
    ("pr09 ARTCC画面(候補)", "out/jiko/ep7_cand/_artcc_scope.png", (0.00, 0.00, 1.00, 1.00)),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
    except Exception:                                           # noqa: BLE001
        font = ImageFont.load_default()
    sh = Image.new("RGB", (CW * 2, (CH + CAP) * 3), (16, 17, 20))
    d = ImageDraw.Draw(sh)
    for j, (label, rel, box) in enumerate(PLAN):
        x, y = (j % 2) * CW, (j // 2) * (CH + CAP)
        d.text((x + 8, y + 5), label, (235, 242, 246), font=font)
        p = HERE / rel
        if not p.exists():
            d.text((x + 20, y + CAP + 160), f"（無い: {rel}）", (224, 80, 60), font=font)
            continue
        im = Image.open(p).convert("RGB")
        l, t, r, b = box
        im = im.crop((int(l * im.width), int(t * im.height),
                      int(r * im.width), int(b * im.height)))
        c = Image.new("RGB", (CW, CH), (26, 28, 32))
        k = min(CW / im.width, CH / im.height)
        im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))),
                       Image.LANCZOS)
        c.paste(im, ((CW - im.width) // 2, (CH - im.height) // 2))
        sh.paste(c, (x, y + CAP))
    q = OUT / "crop_01.jpg"
    sh.save(q, quality=92)
    print(f"  ✓ {q}  {sh.width}x{sh.height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
