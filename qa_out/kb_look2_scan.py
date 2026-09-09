# -*- coding: utf-8 -*-
"""⑤c 検品【見る】2周目の「当たり付け」を1本にまとめた物差し（2026-09-09）。

鉄則2＝目視の前に機械で当たりを付ける。⚠️ ただし **0件でも全数目視はやめない**。

測るもの（全部 r02 の JPG そのものから。SPEC ではなく **焼けた絵**を見る）:
  occ      … 占有率（地と差のあるセルの割合）
  hole     … 最大の空き矩形（画面比）
  band     … 下帯 y640-892 の空き率（型③）
  L/R/T/B  … 中身の外接矩形の余白（px）。安全域 BX0=72 / BX1=1848 / 上52 / 下906
  touch    … 余白を食っている辺（left/right/top/bottom）

⚠️ 地の判定は色でなく `out/jiko/_empty.png` との差（check_space と同じ根拠）。
使い方: python qa_out/kb_look2_scan.py c101 c103 ...
        python qa_out/kb_look2_scan.py --rest   # 帳の残り全部
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))

from PIL import Image, ImageChops  # noqa: E402

SRC = HERE / "out" / "jiko" / "qa_keybridge-r02"
EMPTY = HERE / "out" / "jiko" / "_empty.png"
CELL = 40
DIFF = 8          # この差未満なら「地のまま」
CELL_ON = 0.015   # セル内のこの割合以上が地でなければ「使っている」
BAND = (640, 892)
SAFE = dict(l=72, r=1848, t=52, b=906)


def load_mask(p):
    """使っている画素 True の 2値マップ（1920x1080 の list of list）を返す。"""
    im = Image.open(p).convert("RGB")
    bg = Image.open(EMPTY).convert("RGB").resize(im.size)
    d = ImageChops.difference(im, bg).convert("L")
    return d.point(lambda v: 255 if v >= DIFF else 0)


def cells(mask):
    w, h = mask.size
    cw, ch = w // CELL, h // CELL
    grid = []
    px = mask.load()
    for cy in range(ch):
        row = []
        for cx in range(cw):
            n = 0
            for y in range(cy * CELL, (cy + 1) * CELL, 4):
                for x in range(cx * CELL, (cx + 1) * CELL, 4):
                    if px[x, y]:
                        n += 1
            row.append(n / ((CELL // 4) ** 2) >= CELL_ON)
        grid.append(row)
    return grid


def largest_hole(grid):
    """連続して空いている最大の長方形（セル数）。"""
    h, w = len(grid), len(grid[0])
    heights = [0] * w
    best = 0
    for y in range(h):
        for x in range(w):
            heights[x] = 0 if grid[y][x] else heights[x] + 1
        stack = []
        for x in range(w + 1):
            cur = heights[x] if x < w else 0
            start = x
            while stack and stack[-1][1] >= cur:
                s, hh = stack.pop()
                best = max(best, hh * (x - s))
                start = s
            stack.append((start, cur))
    return best


def bbox(mask):
    b = mask.getbbox()
    return b  # (l, t, r, b) or None


def scan(cid):
    p = SRC / f"cut_{cid}.jpg"
    if not p.exists():
        return f"{cid}\t🔴 無い"
    mask = load_mask(p)
    grid = cells(mask)
    tot = len(grid) * len(grid[0])
    occ = sum(sum(r) for r in grid) / tot
    hole = largest_hole(grid) / tot
    y0, y1 = BAND[0] // CELL, BAND[1] // CELL
    bandcells = [grid[y][x] for y in range(y0, y1) for x in range(len(grid[0]))]
    band = 1 - (sum(bandcells) / len(bandcells))
    bb = bbox(mask)
    if bb is None:
        return f"{cid}\t🔴 まっさら"
    l, t, r, b = bb
    touch = []
    if l < SAFE["l"]:
        touch.append(f"left({l})")
    if r > SAFE["r"]:
        touch.append(f"right({r})")
    if t < SAFE["t"]:
        touch.append(f"top({t})")
    if b > SAFE["b"]:
        touch.append(f"bottom({b})")
    return (f"{cid}\tocc {occ*100:5.1f}%\thole {hole*100:5.2f}%\tband {band*100:5.1f}%\t"
            f"L{l} R{1920-r} T{t} B{1080-b}\t" + (" ".join(touch) if touch else "-"))


def main():
    args = sys.argv[1:]
    if not args or args[0] == "--rest":
        import qa_seen as q
        cfg = q.load_cfg("kb")
        allc = q.items(cfg, q.FULL)
        seen = [n for n, _ in q.read_seen("kb", q.FULL)]
        args = [n for n in allc if n not in seen]
    print("cid\t占有\t最大の穴\t下帯の空き\t外接の余白\t安全域を食う辺")
    for cid in args:
        print(scan(cid), flush=True)


if __name__ == "__main__":
    main()
