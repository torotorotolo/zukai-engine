# -*- coding: utf-8 -*-
"""ep7_fixsheet.py — **直したカットだけ**を 640px の 2列×3行シートにする（2026-09-14 ⑤c'）。

■ なぜ要るか
    終わりの決まり（[[feedback-jiko-qa-must-have-an-end]]）＝最後の検品は**直したカットだけ**。
    ⚠️ 640px で決まらないのは「図の比例」「小さな点」「札の切れ」の3型だけ
      （`qa_out/ep7_qa_look2.md` §C）。**並びの直し**（段落ち・近さ・埋め草）は
      640px で決まるので、ここはシートで見て、原寸は素材と小さい字の欄に取っておく。

■ 使い方
    python qa_out/ep7_fixsheet.py --dir out/jiko/qa_ep7-r02 --ids c812,c105,...
    → out/jiko/ep7_fix/sheet_NN.jpg
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
OUT = HERE / "out" / "jiko" / "ep7_fix"
CW, CH, CAP = 640, 360, 26


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="out/jiko/qa_ep7-r02")
    p.add_argument("--ids", required=True)
    p.add_argument("--tag", default="")
    a = p.parse_args()
    src = HERE / a.dir
    ids = [x.strip() for x in a.ids.split(",") if x.strip()]
    OUT.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
    n = 0
    for i in range(0, len(ids), 6):
        chunk = ids[i:i + 6]
        sh = Image.new("RGB", (CW * 2, (CH + CAP) * 3), (16, 17, 20))
        d = ImageDraw.Draw(sh)
        for j, cid in enumerate(chunk):
            x, y = (j % 2) * CW, (j // 2) * (CH + CAP)
            f = src / f"cut_{cid}.jpg"
            d.text((x + 8, y + 4), f"{cid}", (235, 242, 246), font=font)
            if not f.exists():
                d.text((x + 20, y + CAP + 160), f"（無い: {f.name}）", (224, 80, 60), font=font)
                continue
            with Image.open(f) as im:
                sh.paste(im.convert("RGB").resize((CW, CH), Image.LANCZOS), (x, y + CAP))
        n += 1
        q = OUT / f"sheet_{a.tag or 'r02'}_{n:02d}.jpg"
        sh.save(q, quality=92)
        print(f"  ✓ {q}  {len(chunk)}コマ")
    print(f"■ シート {n}枚 ／ カット {len(ids)}件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
