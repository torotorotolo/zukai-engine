# -*- coding: utf-8 -*-
"""本編フレーム試作：「砂糖をやめて7日目・肝臓」。

目標様式（Vault Resources/参考-アニメ様式-ClaudeCode日本史-20260728.md）の7項目を満たす:
  地紋を敷く／四隅を落とす／低彩度／1シーン1動作／長く見せる／ラベルで名指し／細部を1つ
"""
import base64
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import anatomy as A

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
FONTS = Path(r"C:\Users\konar\Desktop\zankoku-sekkeizu\public\fonts")
ACCENT = "#b5442c"


def face(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


def label(x, y, text, sub=None):
    """濃茶の角丸ボックス＋白文字。目標様式の名前ラベルの作法。"""
    w = 44 + len(text) * 34
    out = (f'<g filter="url(#soft)"><rect x="{x}" y="{y}" width="{w}" height="66" rx="8" '
           f'fill="{A.INK}"/>'
           f'<text x="{x + 22}" y="{y + 47}" font-family="Mincho" font-size="36" '
           f'fill="#f6efdf" letter-spacing="2">{text}</text></g>')
    if sub:
        out += (f'<text x="{x + 4}" y="{y + 104}" font-family="Noto" font-size="27" '
                f'fill="{A.INK_SOFT}">{sub}</text>')
    return out


def timeline(active=2):
    marks = ["1日", "3日", "7日", "14日", "30日"]
    x0, gap = 268, 236
    out = [f'<rect x="{x0}" y="990" width="{gap * 4}" height="6" rx="3" fill="#cdbb9c"/>',
           f'<rect x="{x0}" y="990" width="{gap * active}" height="6" rx="3" fill="{ACCENT}"/>']
    for i, m in enumerate(marks):
        x, on = x0 + gap * i, i <= active
        out.append(
            f'<circle cx="{x}" cy="993" r="{14 if i == active else 9}" '
            f'fill="{ACCENT if on else "#cdbb9c"}" stroke="{A.WASHI}" stroke-width="4"/>'
            f'<text x="{x}" y="1046" font-family="Noto" font-size="28" font-weight="700" '
            f'fill="{A.INK if on else "#a2917a"}" text-anchor="middle">{m}</text>')
    return "".join(out)


SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{A.defs()}</defs>
{A.background(W, H)}

<g transform="translate(392,104) scale(0.82)">
  <path d="{A.torso_path()}" fill="{A.BODY}" stroke="{A.INK}" stroke-width="4.5"
        filter="url(#soft)"/>
  {A.ribs()}
  <g opacity="0.5">{A.colon()}{A.small_intestine()}{A.pancreas()}</g>
  <g opacity="0.72">{A.stomach()}</g>
  <g filter="url(#glow)">{A.liver()}</g>
</g>

<!-- 章タグ -->
<g filter="url(#soft)">
  <rect x="76" y="66" width="12" height="108" rx="6" fill="{ACCENT}"/>
  <text x="112" y="122" font-family="Dela" font-size="56" fill="{A.INK}">7日目</text>
  <text x="114" y="166" font-family="Noto" font-size="32" font-weight="700"
        fill="{A.INK_SOFT}">肝臓にたまった脂肪が減りはじめる</text>
</g>

<!-- 引き出し線とラベル（目標様式：要素を名指しする） -->
<path d="M846 452 H1338" fill="none" stroke="{A.INK}" stroke-width="3" opacity="0.7"/>
<circle cx="846" cy="452" r="9" fill="{ACCENT}"/>
{label(1348, 436, "肝臓")}

<path d="M1004 561 H1338" fill="none" stroke="{A.INK}" stroke-width="3" opacity="0.55"/>
<circle cx="1004" cy="561" r="7" fill="{A.INK}"/>
{label(1348, 528, "胃")}

<!-- 数値 -->
<g filter="url(#soft)">
  <rect x="1348" y="648" width="446" height="188" rx="10" fill="#fbf5e8"
        stroke="{A.INK}" stroke-width="3"/>
  <rect x="1348" y="648" width="446" height="8" rx="4" fill="{ACCENT}"/>
  <text x="1382" y="708" font-family="Noto" font-size="30" font-weight="700"
        fill="{A.INK_SOFT}">肝臓の脂肪</text>
  <text x="1382" y="800" font-family="Dela" font-size="92"
        fill="{ACCENT}">-20<tspan font-size="46" fill="{A.INK}">%</tspan></text>
</g>

{timeline(2)}
{A.overlay(W, H)}

<text x="{W // 2}" y="922" font-family="Noto" font-size="50" font-weight="700"
      fill="#fdf8ee" text-anchor="middle" stroke="{A.INK}" stroke-width="12"
      stroke-linejoin="round" paint-order="stroke fill">砂糖を断って一週間、肝臓はまず脂肪を手放しはじめます</text>
</svg>'''

out = HERE / "out" / "scene_liver.png"
out.parent.mkdir(exist_ok=True)
css = (face("Dela", "DelaGothicOne.woff2") + face("Noto", "NotoSansJP-Bold.woff2")
       + face("Mincho", "NotoSerifJP-SemiBold.woff2"))
html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
        f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{SVG}</body></html>')
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t.html"
    p.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={W},{H}",
                    f"--screenshot={out}", "--virtual-time-budget=4000", p.resolve().as_uri()],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print(out, out.exists())
