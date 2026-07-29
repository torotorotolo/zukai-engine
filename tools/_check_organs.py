# -*- coding: utf-8 -*-
"""追加した腎臓・脳の形を1枚で確かめる検証シート（本編では使わない）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import anatomy as A
import render

W, H = 1400, 620
SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{A.defs()}</defs>
<rect width="{W}" height="{H}" fill="#f3ead7"/>
<g transform="translate(210,300) scale(0.86)">{A.kidney()}</g>
<g transform="translate(470,300) scale(0.86)">{A.kidney(flip=True)}</g>
<g transform="translate(950,300) scale(0.92)">{A.brain()}</g>
<text x="340" y="580" font-size="30" fill="#4a3b2a" text-anchor="middle" font-family="sans-serif">kidney / kidney(flip)</text>
<text x="950" y="580" font-size="30" fill="#4a3b2a" text-anchor="middle" font-family="sans-serif">brain</text>
</svg>'''
html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}'
        f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{SVG}</body></html>')
print("wrote", render.png(html, Path(__file__).parent.parent / "out" / "_check_organs.png", W, H))
