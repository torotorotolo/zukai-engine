# -*- coding: utf-8 -*-
"""⑤c-2 原寸の切り出し。**等倍のまま**、見る場所だけを切る。

⚠️ 拡大しない（記憶 feedback-sheet-cannot-judge-three-types ＝ 縮小が作った見え方を粗と読まない。
   逆に拡大した見え方を粗と読むのも同じ間違い）。60px の目盛りを右下に焼いて、
   大きさを**目でなく数字で**言えるようにする。

使い方: python qa_out/ep10_crop.py <cid> <x0> <y0> <x1> <y1> [出す名前]
        python qa_out/ep10_crop.py --list        … 台帳に積んだ疑いの既定の窓を全部出す
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent.parent
SHOT = HERE / "out" / "jiko" / "qa_ep10-r01"
OUT = Path(__file__).resolve().parent / "crop"   # ⚠️ sys.argv[0] だと -c 実行で CWD に落ちる


def crop(cid, x0, y0, x1, y1, name=None, rule=True):
    p = SHOT / f"cut_{cid}.jpg"
    if not p.exists():
        raise SystemExit(f"🔴 {p} が無い。0で埋めずに止める")
    OUT.mkdir(exist_ok=True)
    with Image.open(p) as im:
        if im.size != (1920, 1080):
            raise SystemExit(f"🔴 {cid}: 焼けた絵が {im.size}。1920×1080 でない")
        c = im.crop((int(x0), int(y0), int(x1), int(y1))).convert("RGB")
    if rule:
        d = ImageDraw.Draw(c)
        w, h = c.size
        # 60px の目盛り（右下）。原寸であることの陽性対照でもある
        d.rectangle([w - 70, h - 18, w - 10, h - 14], fill=(255, 64, 64))
        d.rectangle([w - 70, h - 22, w - 68, h - 10], fill=(255, 64, 64))
        d.rectangle([w - 12, h - 22, w - 10, h - 10], fill=(255, 64, 64))
    q = OUT / (name or f"{cid}_{int(x0)}_{int(y0)}.png")
    c.save(q)
    print(f"{q.name}  {c.size[0]}×{c.size[1]}px  （元 {cid} の x{int(x0)}..{int(x1)} y{int(y0)}..{int(y1)}・等倍）")
    return q


if __name__ == "__main__":
    a = sys.argv[1:]
    crop(a[0], *[float(v) for v in a[1:5]], name=(a[5] if len(a) > 5 else None))
