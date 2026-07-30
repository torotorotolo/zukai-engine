# -*- coding: utf-8 -*-
"""画面の余白を機械的に測る。

🔴 2026-07-30 カズヤくん指摘「画面の余白が多い（特に実写カットの右側）」。
   目視だけで詰めると「詰めたつもり」で終わるので、**数字で測ってから直す**。

測り方：
  ⚠️ 「地の色に近いか」で判定しようとして失敗した。BG2(#16232e) が BG と GRID を結ぶ線上に
     ほぼ乗っているため、高度グラフの下地（BG2 の塗り）まで空きに数えていた（c6 が実際より
     10ポイント低く出た）。方眼線のアンチエイリアスも中間色になるので色では切れない。
  → **空の地そのものをクラウドで焼いて `_empty.png` として同じ検品フォルダに置き**、
     画素ごとの差で判定する。差が 8 未満なら「その画素は地のまま＝空き」。
     40px 角のセルに畳み、セル内の 1.5% 以上が地でなければ「使っている」セル。

    占有率        = 使っているセル / 全セル
    最大の空き矩形 = 連続して空いているいちばん大きい長方形（ここが「余白」の正体）

判定の目安：
  占有率 55% 以上 ／ 最大の空き矩形が画面の 8% 未満（8% ≒ 570×290px の穴）
  ⚠️ 中身が中空の線画（胴体断面の円など）は、内側が本当に空いているので占有率が下がる。
     数字を上げるために意味のない塗りを足さないこと。**空き矩形のほうを主に見る。**

使い方： python tools/check_space.py [検品PNGのあるディレクトリ]
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageChops

CELL = 40
OCC = 0.015              # セル内のこの割合以上が content なら「使っている」
FILL_MIN = 0.55          # 占有率の下限
HOLE_MAX = 0.08          # 最大の空き矩形の上限（画面面積比）
DIFF = 8                 # 地との差がこれ未満なら「空き」


def cells(path, ref):
    """(占有マップ, 列数, 行数)。占有マップは True=使っている。"""
    im = Image.open(path).convert("RGB")
    # 地との差。**輝度に落とすと青だけの差を取りこぼす**ので、3チャンネルの最大を取る
    r, g, b = ImageChops.difference(im, ref).split()
    d = ImageChops.lighter(ImageChops.lighter(r, g), b).point(
        lambda v: 255 if v >= DIFF else 0)
    w, h = d.size
    cx, cy = w // CELL, h // CELL
    need = int(CELL * CELL * OCC)
    grid = [[False] * cx for _ in range(cy)]
    for j in range(cy):
        for i in range(cx):
            cell = d.crop((i * CELL, j * CELL, (i + 1) * CELL, (j + 1) * CELL))
            grid[j][i] = sum(cell.getdata()) / 255 >= need
    return grid, cx, cy


def biggest_hole(grid, cx, cy):
    """空きセルだけで作れるいちばん大きい長方形。ヒストグラム法。"""
    best = (0, 0, 0, 0, 0)               # 面積, x, y, w, h（セル単位）
    up = [0] * cx
    for j in range(cy):
        for i in range(cx):
            up[i] = 0 if grid[j][i] else up[i] + 1
        st = []
        for i in range(cx + 1):
            hh = up[i] if i < cx else 0
            start = i
            while st and st[-1][1] >= hh:
                s, ph = st.pop()
                area = ph * (i - s)
                if area > best[0]:
                    best = (area, s, j - ph + 1, i - s, ph)
                start = s
            st.append((start, hh))
    return best


def report(d):
    d = Path(d)
    files = sorted(d.glob("cut_*.png"))
    if not files:
        print(f"検品PNGが無い: {d}")
        return 1
    rp = d / "_empty.png"
    if not rp.exists():
        print(f"🔴 地の基準画像が無い: {rp}（scene_jiko が焼く `_empty.png` を検品に入れる）")
        return 1
    ref = Image.open(rp).convert("RGB")
    bad, fills = [], []
    print(f"{'カット':<6}{'占有率':>8}{'最大の空き':>11}  場所（px）")
    for p in files:
        grid, cx, cy = cells(p, ref)
        fill = sum(sum(r) for r in grid) / (cx * cy)
        fills.append(fill)
        area, hx, hy, hw, hh = biggest_hole(grid, cx, cy)
        hole = area / (cx * cy)
        cut = p.stem[4:]
        flag = ""
        if fill < FILL_MIN:
            flag += " 🔴占有率"
        if hole > HOLE_MAX:
            flag += " 🔴空き矩形"
        if flag:
            bad.append((cut, round(fill, 3), round(hole, 3), flag.strip()))
        print(f"{cut:<6}{fill * 100:>7.1f}%{hole * 100:>10.1f}%  "
              f"x{hx * CELL}〜{(hx + hw) * CELL} y{hy * CELL}〜{(hy + hh) * CELL}{flag}")
    print(f"\n平均占有率 = {sum(fills) / len(fills) * 100:.1f}%")
    if bad:
        print(f"🔴 余白が多いカット {len(bad)}件：" + "、".join(b[0] for b in bad))
    else:
        print(f"✓ 全{len(files)}カットが占有率{FILL_MIN * 100:.0f}%以上／"
              f"空き矩形{HOLE_MAX * 100:.0f}%未満")
    return 0


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "out/jiko/qa"
    sys.exit(report(d))
