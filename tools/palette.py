# -*- coding: utf-8 -*-
"""まちがい探し喫茶：配色。

シニア向けの絶対条件（コントラスト・視認性）を最優先する。
- 背景はクリーム（白は眩しい／テレビ視聴で目が疲れる）
- 線は黒でなく濃茶（きつく見えない）
- 「違い」に使う色は、色覚差があっても判別できる組み合わせに限定する
"""

# 基本色
INK = "#3a3128"        # 主線（濃茶）
INK_LIGHT = "#7a6d5c"  # 補助線
CREAM = "#f6efe2"      # 背景
PANEL = "#fffdf8"      # 絵の下地
SHADOW = "#e6dcc8"     # 影
ACCENT = "#e2643c"     # 差し色（朱赤）
GOLD = "#d8a13a"       # 差し色（山吹）
GREEN = "#6a8f4f"
BLUE = "#4a7fa5"
PINK = "#e08fa0"
PURPLE = "#8a6fa8"
WHITE = "#fffefb"

# 「色ちがい」の変異に使う対（色覚差があっても見分けられる組を選ぶ）
RECOLOR_PAIRS = {
    ACCENT: GOLD,
    GOLD: ACCENT,
    GREEN: GOLD,
    BLUE: ACCENT,
    PINK: BLUE,
    PURPLE: GREEN,
    WHITE: "#cfe3ef",
}

# 難易度ごとの帯色
LEVEL_COLOR = {"初級": GREEN, "中級": BLUE, "上級": ACCENT, "特別": PURPLE}


def recolor(c: str) -> str:
    """変異用の色を返す。対が無ければ朱赤へ倒す。"""
    return RECOLOR_PAIRS.get(c, ACCENT)


def shade(c: str, f: float) -> str:
    """色を暗く/明るくする。f<0 で暗く、f>0 で明るく（-1〜1）。

    輪郭線を「黒」でなく「その色を暗くした色」にするだけで、
    絵は一気にクリップアート臭さから抜ける。全プロップの既定の描き方にする。
    """
    h = c.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f < 0:
        r, g, b = (int(v * (1 + f)) for v in (r, g, b))
    else:
        r, g, b = (int(v + (255 - v) * f) for v in (r, g, b))
    return "#%02x%02x%02x" % (max(0, r), max(0, g), max(0, b))


def spread(n: int, w: float, h: float, pad: float, seed: int = 7):
    """n個の点を矩形内に決定論的に散らす。

    ※ 以前は (i*173) % 172 のような式で散らしていたが、173 mod 172 = 1 のため
       全点が数pxに重なって「正体不明の塊」になっていた（揚げパンのきなこ）。
       線形合同法で確実にばらす。
    """
    pts, s = [], seed * 2654435761 + 1
    for _ in range(max(0, n)):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        x = pad + (s >> 9) % max(1, int(w - 2 * pad))
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        y = pad + (s >> 9) % max(1, int(h - 2 * pad))
        pts.append((x, y))
    return pts
