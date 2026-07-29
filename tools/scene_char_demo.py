# -*- coding: utf-8 -*-
"""本編フレーム試作：キャラクター入り。「砂糖をやめて3日目・リビング」。

character.py が場面の中で本当に使えるかを確かめるための1枚。
Vault `Resources/参考-健康解説アニメ2本-分析-20260728.md` の共通原則を全部満たす：
  1 キャラが登場して演じる  2 背景は「場所」  3 画面上部に大きな見出し
  4 字幕は黄＋白の2色      5 比喩を絵にする  6 情報グラフィックを挟む
  7 純色を避けて濁らせる

日本史アニメから引き継ぐのは「1シーン1動作・低彩度・四隅を落とす」だけ（地紋は敷かない）。
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import character as C
import render

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
FONTS = Path(r"C:\Users\konar\Desktop\zankoku-sekkeizu\public\fonts")

INK = C.INK
WALL = "#e7dcc6"
WALL_LO = "#d8c9ad"
FLOOR = "#c2a179"
ACCENT = "#b5442c"
CARD = "#fbf5e8"


def face_css(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


HORIZON = 700          # 壁と床の境。家具の足はここより下に接地させる


def room():
    """リビング。家具は3つだけ置く。視聴者が自分の家に重ねられれば足りる。

    家具はすべて床（HORIZON）に接地させること。初稿はスタンドの脚が
    床に届かず宙に浮き、ソファは情報カードの裏に完全に隠れていた。
    """
    sofa = (f'<g transform="translate(96,{HORIZON - 230})">'
            f'<path d="M0 290 V96 q0 -34 36 -34 h392 q36 0 36 34 V290 Z" fill="#a98d6d" '
            f'stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M16 290 V152 q0 -26 30 -26 h380 q30 0 30 26 V290 Z" fill="#c0a483" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="M54 152 h372" fill="none" stroke="{INK}" stroke-width="5" opacity="0.4"/>'
            f'</g>')
    table = (f'<g transform="translate(690,{HORIZON + 96})">'
             f'<rect x="0" y="0" width="330" height="24" rx="9" fill="#b98d5c" '
             f'stroke="{INK}" stroke-width="6"/>'
             f'<rect x="28" y="24" width="18" height="96" rx="7" fill="#a67d4e" '
             f'stroke="{INK}" stroke-width="6"/>'
             f'<rect x="284" y="24" width="18" height="96" rx="7" fill="#a67d4e" '
             f'stroke="{INK}" stroke-width="6"/></g>')
    lamp = (f'<g transform="translate(1690,0)">'
            f'<rect x="-9" y="360" width="18" height="{HORIZON + 34 - 360}" fill="#8d7a5e" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="{HORIZON + 36}" rx="62" ry="16" fill="#8d7a5e" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-78 366 L-50 258 h100 l28 108 Z" fill="#e3d3ae" stroke="{INK}" '
            f'stroke-width="7" stroke-linejoin="round"/></g>')
    # 壁の幅木。壁と床の境に1本入れるだけで「部屋」に見える
    skirting = (f'<rect y="{HORIZON - 26}" width="{W}" height="26" fill="{WALL_LO}" '
                f'stroke="{INK}" stroke-width="5" opacity="0.85"/>')
    return (f'<rect width="{W}" height="{HORIZON}" fill="url(#wall)"/>'
            f'<rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="{FLOOR}"/>'
            f'{skirting}{lamp}{sofa}{table}')


def headline(t):
    """画面上部に常時出す大見出し（参考2本の共通原則3）。"""
    return (f'<rect x="0" y="0" width="{W}" height="132" fill="#fbf6ea" opacity="0.95"/>'
            f'<rect x="0" y="132" width="{W}" height="7" fill="{ACCENT}"/>'
            f'<text x="{W // 2}" y="97" font-family="Dela" font-size="76" fill="{INK}" '
            f'text-anchor="middle">砂糖をやめて3日目</text>')


def subtitle(hi, rest):
    """字幕は黄で強調語＋白。黒の太縁（参考2本の共通原則4）。"""
    y = 1006
    common = ('font-family="Noto" font-size="52" text-anchor="middle" '
              f'stroke="{INK}" stroke-width="13" stroke-linejoin="round" paint-order="stroke fill"')
    return (f'<text x="{W // 2}" y="{y}" {common}>'
            f'<tspan fill="#ffd83d">{hi}</tspan><tspan fill="#fffdf6">{rest}</tspan></text>')


def card(x, y):
    """情報グラフィック（参考2本の共通原則6）。棒3本で足りる。"""
    bars = [("1日目", 96, "#c9bda4"), ("3日目", 62, ACCENT), ("7日目", 34, "#7f9b62")]
    g = [f'<rect x="{x}" y="{y}" width="430" height="330" rx="14" fill="{CARD}" '
         f'stroke="{INK}" stroke-width="7"/>'
         f'<text x="{x + 30}" y="{y + 62}" font-family="Noto" font-size="36" '
         f'fill="{INK}">甘いものが欲しい気持ち</text>']
    for i, (lab, pct, col) in enumerate(bars):
        by = y + 100 + i * 72
        g.append(f'<text x="{x + 30}" y="{by + 34}" font-family="Noto" font-size="30" '
                 f'fill="{INK}">{lab}</text>'
                 f'<rect x="{x + 130}" y="{by + 8}" width="{pct * 2.6:.0f}" height="34" rx="8" '
                 f'fill="{col}" stroke="{INK}" stroke-width="5"/>')
    return "".join(g)


def mug(x, y, s=1.0):
    """小道具：湯のみ。character(...).anchors["hand"] の位置に置く。"""
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({s}) rotate(-8)">'
            f'<path d="M-42 -34 h84 l-10 76 q-4 22 -32 22 q-28 0 -32 -22 Z" fill="#e8e2d4" '
            f'stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<ellipse cx="0" cy="-34" rx="42" ry="13" fill="#8fae8a" stroke="{INK}" '
            f'stroke-width="8"/>'
            f'<path d="M-8 -74 q10 -18 0 -34 M14 -74 q10 -18 0 -34" fill="none" '
            f'stroke="#fffdf6" stroke-width="7" stroke-linecap="round" opacity="0.8"/></g>')


# ── 組み立て ──────────────────────────────────────────────
# 手前に「持つ」のキャラ、その手に湯のみを置く。anchors が場面から使えることの確認。
man = C.character("hold", "convinced", costume="casual", at=(1180, 946), scale=1.12)
hx, hy = man.anchors["hand"]

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  {C.defs()}
  <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{WALL}"/><stop offset="100%" stop-color="{WALL_LO}"/>
  </linearGradient>
  <radialGradient id="vig" cx="50%" cy="44%" r="72%">
    <stop offset="52%" stop-color="#3a2c18" stop-opacity="0"/>
    <stop offset="100%" stop-color="#3a2c18" stop-opacity="0.34"/>
  </radialGradient>
</defs>

{room()}
{card(168, 196)}
{man}
{mug(hx, hy - 8, 1.12)}

<rect width="{W}" height="{H}" fill="url(#vig)"/>
{headline("砂糖をやめて3日目")}
{subtitle("甘いものが欲しい気持ちは", "、3日目から静かになります")}
</svg>'''

css = (face_css("Dela", "DelaGothicOne.woff2") + face_css("Noto", "NotoSansJP-Bold.woff2"))
html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
        f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{SVG}</body></html>')
out = render.png(html, HERE / "out" / "scene_char_demo.png", W, H)
print("wrote", out)
