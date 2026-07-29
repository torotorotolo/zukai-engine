# -*- coding: utf-8 -*-
"""EHL5様式の再現テスト。3カット×5.6秒＝16.8秒。

■ 作り方（Chrome起動を減らして30fpsを出す）
参考は背景が不動でキャラだけが滑らかに動く。だから
  1. **背景＋前景の小物** を1枚レンダリング（1回起動）
  2. **キャラを透明背景で8変種** グリッド1枚にレンダリング（1回起動）
  3. あとは **PIL で合成**して30fpsのコマを作る（Chrome不要）
1カットあたり2回の起動で足りる。呼吸の上下・口パク・まばたきは合成側で作る。

■ 守る決まり（Vault 参考-EHL5秒単位分解-20260729）
  ・前景＝黒の太輪郭＋高彩度／**背景＝黒を使わず同系色の暗い線＋低彩度**
  ・1カットの中で主役だけ補色にする
  ・色調は2〜3カットごとに入れ替える（橙 → 橙赤 → 青緑）
  ・文字はUIで重ねず、**画面内の黒板・看板に載せる**
  ・見出し帯なし・焼き付け字幕なし
  ・カメラは動かさない（極小のパンのみ）
"""
import base64
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import cartoon as K
import render

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
FONTS = Path(r"C:\Users\konar\Desktop\zankoku-sekkeizu\public\fonts")
INK = K.INK
CSS = ""


def face_css(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


def _bgrect(x, y, w, h, fill, r=0, lw=9.0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
            f'stroke="{K.bg_ink(fill)}" stroke-width="{lw}"/>')


def _lamp(x, y, col="#e8b33c"):
    return (f'<g transform="translate({x},0)">'
            f'<path d="M0 0 V{y - 60}" stroke="{K.bg_ink(col, -0.55)}" stroke-width="7"/>'
            f'<path d="M-62 {y} q62 -86 124 0 Z" fill="{col}" '
            f'stroke="{K.bg_ink(col)}" stroke-width="9" stroke-linejoin="round"/>'
            f'<ellipse cy="{y + 6}" rx="62" ry="12" fill="{K.bg_ink(col, 0.30)}"/></g>')


def _potplant(x, y, s=1.0, pot="#c47a33", leaf="#5f8f48"):
    lv = "".join(f'<path d="M0 -10 Q{dx} {dy} {dx * 1.45:.0f} {dy - 30}" fill="none" '
                 f'stroke="{leaf}" stroke-width="26" stroke-linecap="round"/>'
                 for dx, dy in [(-54, -58), (-22, -92), (16, -96), (52, -64),
                                (-34, -24), (44, -22)])
    return (f'<g transform="translate({x},{y}) scale({s})">{lv}'
            f'<path d="M-52 -14 h104 l-14 84 q-3 16 -38 16 q-35 0 -38 -16 Z" fill="{pot}" '
            f'stroke="{K.bg_ink(pot)}" stroke-width="9" stroke-linejoin="round"/>'
            f'<rect x="-58" y="-28" width="116" height="22" rx="7" fill="{pot}" '
            f'stroke="{K.bg_ink(pot)}" stroke-width="9"/></g>')


# ── カット1：カフェ（橙系） ───────────────────────────────

def bg_cafe():
    WALL, WALL2 = "#eec089", "#e0ac6b"
    WOOD, WOOD2, WOOD3 = "#bd7f3f", "#a06835", "#8a5729"
    BOARD = "#4a3524"
    g = [f'<rect width="{W}" height="{H}" fill="{WALL}"/>',
         f'<rect y="0" width="{W}" height="430" fill="{WALL2}"/>',
         f'<rect y="424" width="{W}" height="14" fill="{K.bg_ink(WALL2)}" opacity="0.35"/>']
    # 奥の客（シルエット）。人がいる店に見せる
    for cx, sc, op in ((250, 1.0, 0.20), (420, 0.86, 0.16), (1640, 0.94, 0.18)):
        g.append(f'<g transform="translate({cx},560) scale({sc})" opacity="{op}">'
                 f'<circle cy="-250" r="76" fill="#4a3018"/>'
                 f'<path d="M-96 0 q0 -170 96 -170 q96 0 96 170 Z" fill="#4a3018"/></g>')
    for wx in (70, 1560):
        g.append(_bgrect(wx, 96, 300, 250, "#f6e2b0", 10))
        g.append(f'<path d="M{wx + 150} 96 V346 M{wx} 221 h300" '
                 f'stroke="{K.bg_ink("#f6e2b0")}" stroke-width="8" opacity="0.8"/>')
    # 黒板メニュー（文字は画面内の物に載せる）
    g.append(_bgrect(660, 60, 600, 350, BOARD, 14, 12))
    g.append(f'<rect x="684" y="84" width="552" height="302" rx="8" fill="none" '
             f'stroke="#efe0bc" stroke-width="5" opacity="0.45"/>')
    for t, sz, y in [("TODAY&apos;S", 44, 158), ("CARAMEL LATTE", 66, 244),
                     ("2 pumps vanilla", 38, 326)]:
        g.append(f'<text x="960" y="{y}" font-family="Dela" font-size="{sz}" '
                 f'fill="#efe0bc" text-anchor="middle" opacity="0.95">{t}</text>')
    g.append(f'<path d="M770 282 h380" stroke="#efe0bc" stroke-width="5" opacity="0.45"/>')
    for lx in (430, 960, 1490):
        g.append(_lamp(lx, 120))
    g.append(_bgrect(60, 392, 470, 15, WOOD2, 5))
    for i in range(6):
        c = ["#d2a066", "#bd8c55", "#c9a97a", "#a8763c"][i % 4]
        g.append(_bgrect(84 + i * 74, 336, 52, 56, c, 8))
    g.append(_bgrect(1400, 392, 460, 15, WOOD2, 5))
    for i in range(5):
        c = ["#8fa88c", "#b58a5c", "#a2856a"][i % 3]
        g.append(f'<path d="M{1430 + i * 88} 392 v-46 q0 -14 20 -14 q20 0 20 14 v46 Z" '
                 f'fill="{c}" stroke="{K.bg_ink(c)}" stroke-width="8"/>')
    g.append(_bgrect(0, 620, W, 46, WOOD, 0, 10))
    g.append(_bgrect(0, 666, W, 414, WOOD2))
    for x in range(0, W + 1, 240):
        g.append(f'<path d="M{x} 666 V1080" stroke="{K.bg_ink(WOOD2)}" stroke-width="7" '
                 f'opacity="0.55"/>')
    g.append(f'<rect y="1024" width="{W}" height="56" fill="{WOOD3}"/>')
    # ショーケース
    g.append(_bgrect(1330, 400, 520, 222, "#e7ddc6", 12))
    g.append(_bgrect(1354, 424, 472, 174, "#cfe6e8", 8))
    for i in range(4):
        cx = 1420 + i * 116
        g.append(f'<circle cx="{cx}" cy="500" r="34" '
                 f'fill="{["#d98a4a", "#c96a52", "#e0b45c", "#b57a3c"][i]}" '
                 f'stroke="{K.bg_ink("#d98a4a")}" stroke-width="8"/>')
        g.append(f'<rect x="{cx - 38}" y="540" width="76" height="34" rx="6" '
                 f'fill="{["#e0b45c", "#d98a4a", "#c96a52", "#cf9a5c"][i]}" '
                 f'stroke="{K.bg_ink("#d98a4a")}" stroke-width="8"/>')
    g.append(_bgrect(1010, 434, 290, 188, "#b6bcbe", 12))
    g.append(_bgrect(1044, 466, 100, 82, "#8f9698", 8))
    g.append(_bgrect(1166, 466, 100, 82, "#8f9698", 8))
    g.append(f'<path d="M1094 548 v34 M1216 548 v34" stroke="{K.bg_ink("#8f9698")}" '
             f'stroke-width="14" stroke-linecap="round"/>')
    g.append(_potplant(120, 1010, 1.0))
    return "".join(g)


def props_cafe():
    steam = "".join(f'<path d="M{1146 + i * 36} 468 q22 -40 0 -76 q-22 -38 0 -74" fill="none" '
                    f'stroke="#f6ead0" stroke-width="11" stroke-linecap="round" '
                    f'opacity="{0.5 - i * 0.12:.2f}"/>' for i in range(3))
    cup = (f'<g transform="translate(1180,596)">'
           f'<path d="M-62 -56 h124 l-15 138 q-4 28 -47 28 q-43 0 -47 -28 Z" '
           f'fill="#efe3cc" stroke="{INK}" stroke-width="14" stroke-linejoin="round"/>'
           f'<path d="M-58 -14 h116" stroke="{INK}" stroke-width="11" opacity="0.35"/>'
           f'<path d="M-66 -74 h132 q11 0 11 18 h-154 q0 -18 11 -18 Z" fill="#c0553a" '
           f'stroke="{INK}" stroke-width="14" stroke-linejoin="round"/>'
           f'<path d="M-4 -96 v-52" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
           f'<path d="M-4 -96 v-52" stroke="#e8564a" stroke-width="9" stroke-linecap="round"/></g>')
    return steam + cup


# ── カット2：体内＝工場（橙赤系） ─────────────────────────

def bg_factory():
    WALL, WALL2, WALL3 = "#cf6543", "#b44f34", "#9b4029"
    PIPE = "#c07352"
    g = [f'<rect width="{W}" height="{H}" fill="{WALL}"/>']
    for cx in (200, 700, 1220, 1740):
        g.append(f'<path d="M{cx - 230} 700 q0 -330 230 -330 q230 0 230 330 Z" '
                 f'fill="{WALL2}" stroke="{K.bg_ink(WALL2)}" stroke-width="10"/>')
        g.append(f'<path d="M{cx - 150} 700 q0 -230 150 -230 q150 0 150 230 Z" '
                 f'fill="{WALL3}" opacity="0.5"/>')
    for y in (86, 176):
        g.append(f'<path d="M0 {y} H{W}" stroke="{PIPE}" stroke-width="40" '
                 f'stroke-linecap="round"/>')
        g.append(f'<path d="M0 {y - 12} H{W}" stroke="{K.bg_ink(PIPE, 0.28)}" '
                 f'stroke-width="8" opacity="0.55"/>')
    for x in (240, 780, 1320, 1820):
        g.append(f'<path d="M{x} 86 V178" stroke="{PIPE}" stroke-width="30"/>')
        g.append(f'<circle cx="{x}" cy="132" r="34" fill="{K.bg_ink(PIPE, 0.18)}" '
                 f'stroke="{K.bg_ink(PIPE)}" stroke-width="9"/>')
        g.append(f'<path d="M{x - 24} 132 h48 M{x} 108 v48" stroke="{K.bg_ink(PIPE)}" '
                 f'stroke-width="9" stroke-linecap="round"/>')
    g.append(f'<rect y="856" width="{W}" height="224" fill="{WALL3}"/>')
    g.append(f'<path d="M0 856 H{W}" stroke="{K.bg_ink(WALL3)}" stroke-width="10"/>')
    for i in range(-2, 34):
        g.append(f'<path d="M{i * 64} 866 l40 0 l-40 46 l-40 0 Z" fill="#e0a83c" '
                 f'opacity="0.45"/>')
    for cx in (120, 1820):
        g.append(f'<circle cx="{cx}" cy="470" r="70" fill="#e0aa46" '
                 f'stroke="{K.bg_ink("#e0aa46")}" stroke-width="10"/>')
        g.append(f'<path d="M{cx - 46} 470 a46 46 0 0 1 92 0" fill="none" '
                 f'stroke="{K.bg_ink("#e0aa46")}" stroke-width="8" opacity="0.6"/>')
        g.append(f'<path d="M{cx} 470 l34 -30" stroke="#8c3a22" stroke-width="11" '
                 f'stroke-linecap="round"/>')
    return "".join(g)


def props_factory(alarm=1.0):
    g = [f'<g transform="translate(960,146)">'
         f'<rect x="-396" y="-88" width="792" height="196" rx="14" fill="#d1462f" '
         f'stroke="{INK}" stroke-width="15"/>'
         f'<rect x="-368" y="-62" width="736" height="144" rx="8" fill="none" '
         f'stroke="#f6e7c8" stroke-width="6" opacity="0.5"/>'
         f'<text y="-4" font-family="Dela" font-size="84" fill="#f6e7c8" '
         f'text-anchor="middle">OVERDRIVE</text>'
         f'<text y="80" font-family="Dela" font-size="84" fill="#f6e7c8" '
         f'text-anchor="middle">MODE</text></g>']
    for sx in (400, 1520):
        rays = "".join(f'<path d="M{dx * 60:.0f} {dy * 60 - 30:.0f} '
                       f'l{dx * 34:.0f} {dy * 34:.0f}" stroke="#f2c23c" stroke-width="13" '
                       f'stroke-linecap="round" opacity="{alarm:.2f}"/>'
                       for dx, dy in [(-1, -0.5), (-0.6, -1), (0.6, -1), (1, -0.5)])
        g.append(f'<g transform="translate({sx},150)">'
                 f'<rect x="-50" y="14" width="100" height="38" rx="9" fill="#7a7f82" '
                 f'stroke="{INK}" stroke-width="13"/>'
                 f'<path d="M-50 14 q50 -78 100 0 Z" fill="#e8503c" stroke="{INK}" '
                 f'stroke-width="13" stroke-linejoin="round" '
                 f'opacity="{0.4 + 0.6 * alarm:.2f}"/>{rays}</g>')
    g.append(f'<rect x="-20" y="946" width="1400" height="52" rx="18" fill="#5e3a2a" '
             f'stroke="{INK}" stroke-width="14"/>')
    for i in range(15):
        g.append(f'<circle cx="{40 + i * 96}" cy="972" r="19" fill="#8a5a44" '
                 f'stroke="{INK}" stroke-width="9"/>')
    g.append(f'<path d="M1500 1080 q50 -330 220 -456 q106 -80 200 -96 v552 Z" '
             f'fill="#f2dc95" stroke="{INK}" stroke-width="15" stroke-linejoin="round"/>')
    g.append(f'<path d="M1470 1080 q14 -256 168 -386 q-46 208 -22 386 Z" '
             f'fill="#8fc9e4" stroke="{INK}" stroke-width="15" stroke-linejoin="round"/>')
    for cx, cy, r, rot in [(1600, 660, 30, 18), (1712, 790, 25, -12),
                           (1540, 856, 22, 26), (1806, 686, 20, -22)]:
        g.append(f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" rx="5" '
                 f'fill="#fbf3dd" stroke="{INK}" stroke-width="11" '
                 f'transform="rotate({rot} {cx} {cy})"/>')
    return "".join(g)


# ── カット3：診察室（青緑系） ─────────────────────────────

def bg_clinic():
    WALL, WALL2 = "#8cc0cb", "#74aab6"
    CAB, CAB2 = "#d6e6e8", "#bcd6d8"
    g = [f'<rect width="{W}" height="{H}" fill="{WALL}"/>',
         f'<rect y="546" width="{W}" height="{H - 546}" fill="{WALL2}"/>',
         f'<rect y="540" width="{W}" height="14" fill="{K.bg_ink(WALL2)}" opacity="0.3"/>']
    g.append(_bgrect(96, 96, 290, 400, "#eef2ea", 8))
    g.append(f'<ellipse cx="241" cy="196" rx="44" ry="54" fill="none" '
             f'stroke="{K.bg_ink("#eef2ea")}" stroke-width="10"/>')
    g.append(f'<path d="M241 250 V370 M241 282 l-66 56 M241 282 l66 56 '
             f'M241 370 l-46 78 M241 370 l46 78" fill="none" '
             f'stroke="{K.bg_ink("#eef2ea")}" stroke-width="10" stroke-linecap="round"/>')
    for cx in (214, 268):
        g.append(f'<path d="M{cx} 300 q-16 22 0 44 q16 -22 0 -44 Z" fill="#c98a7c" '
                 f'stroke="{K.bg_ink("#c98a7c")}" stroke-width="7"/>')
    g.append(_bgrect(1560, 110, 290, 210, "#eef2ea", 8))
    for i in range(5):
        g.append(f'<path d="M1596 {158 + i * 38} h{[214, 180, 206, 150, 192][i]}" '
                 f'stroke="{K.bg_ink("#eef2ea")}" stroke-width="10" opacity="0.6"/>')
    g.append(_bgrect(500, 300, 860, 20, CAB, 6))
    for i in range(9):
        c = ["#a8c9cc", "#c6dcde", "#8fb8bd", "#b0cfd2"][i % 4]
        g.append(f'<path d="M{530 + i * 92} 300 v-58 q0 -16 24 -16 q24 0 24 16 v58 Z" '
                 f'fill="{c}" stroke="{K.bg_ink(c)}" stroke-width="8"/>')
    g.append(_bgrect(500, 154, 860, 18, CAB, 6))
    for i in range(6):
        g.append(_bgrect(536 + i * 138, 92, 96, 62,
                         ["#9fc3c7", "#bcd6d8", "#86b2b8"][i % 3], 6))
    g.append(_bgrect(0, 620, W, 34, CAB, 6))
    g.append(_bgrect(0, 654, W, 226, CAB2))
    for x in range(160, W, 300):
        g.append(f'<path d="M{x} 654 V880" stroke="{K.bg_ink(CAB2)}" stroke-width="8"/>')
        g.append(f'<rect x="{x - 140}" y="740" width="76" height="14" rx="7" '
                 f'fill="{K.bg_ink(CAB2)}" opacity="0.7"/>')
    g.append(_bgrect(1440, 700, 470, 60, "#e9e2d4", 14))
    g.append(_bgrect(1470, 760, 34, 180, "#9aa8ac", 6))
    g.append(_bgrect(1846, 760, 34, 180, "#9aa8ac", 6))
    g.append(_bgrect(1440, 640, 130, 66, "#e9e2d4", 14))
    g.append(_potplant(150, 1004, 0.92, "#c9a45c", "#5f8f48"))
    return "".join(g)


def props_clinic():
    """主役の腎臓断面。背景が青緑なので**補色の赤橙**にして視線を集める。"""
    KR = "#c0392b"
    dots = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f0c04a" stroke="{INK}" '
                   f'stroke-width="8"/>' for cx, cy, r in
                   [(-52, -66, 21), (-72, -6, 25), (-48, 56, 19), (12, -98, 16), (8, 94, 15)])
    spark = "".join(f'<path d="M{160 + i * 16} {-70 + i * 30} l26 -8" stroke="#f2d98a" '
                    f'stroke-width="9" stroke-linecap="round" opacity="0.8"/>' for i in range(4))
    return (f'<g transform="translate(1310,506)">'
            f'<path d="M-186 186 l-224 224" stroke="{INK}" stroke-width="72" '
            f'stroke-linecap="round"/>'
            f'<path d="M-186 186 l-224 224" stroke="#3a3330" stroke-width="48" '
            f'stroke-linecap="round"/>'
            f'<circle r="286" fill="#2b4f5e" stroke="{INK}" stroke-width="20"/>'
            f'<circle r="256" fill="#20404e"/>'
            f'<g transform="scale(1.42)">'
            f'<path d="M0 -150 C44 -152 76 -128 84 -92 C90 -60 60 -32 42 -6 '
            f'C38 0 38 0 42 6 C60 32 90 60 84 92 C76 128 44 152 0 150 '
            f'C-64 148 -108 92 -110 8 C-112 -74 -64 -148 0 -150 Z" fill="{KR}" '
            f'stroke="{INK}" stroke-width="13"/>'
            f'<path d="M14 -110 C-42 -96 -70 -40 -70 6 C-70 56 -46 104 6 118" fill="none" '
            f'stroke="#8f2a1f" stroke-width="13" opacity="0.75"/>{dots}'
            f'<path d="M44 -12 h74" stroke="#c9563e" stroke-width="17" stroke-linecap="round"/>'
            f'<path d="M44 16 h88" stroke="#5c86a8" stroke-width="19" stroke-linecap="round"/>'
            f'{spark}</g>'
            f'<path d="M-180 -160 q86 -86 202 -70 q-128 22 -180 118 Z" fill="#ffffff" '
            f'opacity="0.14"/></g>')


# ── レンダリングと合成 ────────────────────────────────────

CUTS = ["cafe", "factory", "clinic"]
SEC = 5.6
MOUTHS = [0.0, 0.35, 0.7, 1.0]
VARIANTS = [(m, b) for b in (0, 1) for m in MOUTHS]


def _page(svg, w, h):
    return (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{CSS}'
            f'body{{width:{w}px;height:{h}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')


def _svg(w, h, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{inner}</svg>')


def cut_layers(name):
    """(背景, セル幅, セル高, セル内原点, 画面での配置, セル生成関数)"""
    if name == "cafe":
        def cell(m, b, ph):
            return K.character("hips", "smile", costume="shirt", hair="short",
                               at=(350, 990), scale=0.95, mouth=m, blink=b,
                               look=0.25, tilt=-1.5)
        return bg_cafe() + props_cafe(), 700, 1020, (40, 60), cell
    if name == "factory":
        def cell(m, b, ph):
            return (K.kidney_char("angry", at=(330, 391), scale=1.70, mouth=m, blink=b,
                                  sweat=3, run=ph, tilt=-3)
                    + K.kidney_char("shock", at=(900, 380), scale=1.62, mouth=m * 0.6,
                                    blink=b, sweat=2, run=(ph + 0.5) % 1.0, tilt=2))
        return bg_factory() + props_factory(1.0), 1300, 900, (180, 120), cell

    def cell(m, b, ph):
        return K.character("point", "normal", costume="coat", hair="curly",
                           at=(380, 970), scale=0.92, mouth=m, blink=b, look=0.3,
                           raise_=0.25, tilt=1.0)
    return bg_clinic() + props_clinic(), 760, 1000, (60, 70), cell


def render_layers():
    out = HERE / "out" / "ehl5"
    out.mkdir(parents=True, exist_ok=True)
    for name in CUTS:
        bg, CW, CH, pos, cell = cut_layers(name)
        p = out / f"bg_{name}.png"
        if not p.exists():
            render.png(_page(_svg(W, H, bg), W, H), p, W, H)
            print("bg", name)
        p = out / f"ch_{name}.png"
        if not p.exists():
            cols = 4
            rows = (len(VARIANTS) + cols - 1) // cols
            cells = "".join(
                f'<g transform="translate({(i % cols) * CW},{(i // cols) * CH})">'
                f'{cell(m, b, i / len(VARIANTS))}</g>'
                for i, (m, b) in enumerate(VARIANTS))
            gw, gh = CW * cols, CH * rows
            # render.png は --default-background-color=00000000 なので、
            # 背景の矩形を描かなければそのまま透過PNGになる
            render.png(_page(_svg(gw, gh, cells), gw, gh), p, gw, gh)
            print("ch", name)
    print("layers done")


if __name__ == "__main__":
    CSS = face_css("Dela", "DelaGothicOne.woff2")
    render_layers()
