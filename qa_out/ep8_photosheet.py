# -*- coding: utf-8 -*-
"""ep8_photosheet.py — 写真74点の**中身**を1枚640pxのシートで見る（2026-09-15・⑤b-2）。

■ なぜ要るか
    `bias` / `side` / `focus()` は「主題が絵のどこにあるか」で決まる。
    ⑤b-1 は縦横比しか測っていないので、見ずに書くと
    **推定を実測の口調で書くこと**になる（→ [[feedback-dont-state-inferences-as-findings]]）。
    このch は 640px シートでの全数確認が認められている（`~/.claude/CLAUDE.md` 鉄則1の例外）。

■ ⚠️ これは検品ではない
    「主題がどこにあるか」を決める窓。粗を探す原寸目視の代わりにはしない
    （→ [[feedback-sheet-cannot-judge-three-types.md]]：図の比例・小さな点・札の切れ は
     シートでは決めない）。

■ 使い方
    python qa_out/ep8_photosheet.py            # 74点ぜんぶ（2列×3行）
    python qa_out/ep8_photosheet.py crew orb   # 名前に当たるものだけ
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parents[1]
REF = HERE / "ref" / "ep8"
OUT = HERE / "out" / "ep8_sheet"
TILE_W, COLS, ROWS, BAR = 640, 2, 3, 26
GRID = 4                                   # 主題の位置を言えるように格子を引く


def main():
    pats = sys.argv[1:]
    names = sorted(p.stem for p in REF.glob("*.jpg"))
    if pats:
        names = [n for n in names if any(p in n for p in pats)]
    OUT.mkdir(parents=True, exist_ok=True)
    per = COLS * ROWS
    for page in range((len(names) + per - 1) // per):
        chunk = names[page * per:(page + 1) * per]
        tiles = []
        for n in chunk:
            with Image.open(REF / f"{n}.jpg") as im:
                im = im.convert("RGB")
                sw, sh = im.size
                h = max(1, round(TILE_W * sh / sw))
                im = im.resize((TILE_W, h), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            for i in range(1, GRID):                       # 0.25 刻みの格子
                x, y = TILE_W * i / GRID, h * i / GRID
                d.line([(x, 0), (x, h)], fill=(255, 40, 40), width=1)
                d.line([(0, y), (TILE_W, y)], fill=(255, 40, 40), width=1)
            tiles.append((im, f"{n}   {sw}x{sh}"))
        th = max(im.height for im, _ in tiles)
        sh_im = Image.new("RGB", (TILE_W * COLS, (th + BAR) * ROWS), (16, 16, 16))
        dd = ImageDraw.Draw(sh_im)
        for i, (im, lab) in enumerate(tiles):
            x, y = (i % COLS) * TILE_W, (i // COLS) * (th + BAR)
            sh_im.paste(im, (x, y + BAR))
            dd.text((x + 6, y + 6), lab, fill=(255, 220, 120))
        p = OUT / f"ph_{page + 1:02d}.jpg"
        sh_im.save(p, quality=90)
        print(f"  ✓ {p.relative_to(HERE)}  {'／'.join(chunk)}")


if __name__ == "__main__":
    main()
