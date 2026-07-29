# -*- coding: utf-8 -*-
"""立ち姿の骨格を単体で確かめる検証シート（本編では使わない）。中心線と肩幅の目安つき。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import character as C
import render

W, H = 1500, 780
cells = [("stand", "normal", "casual", 1.0), ("stand", "normal", "casual", 0.0),
         ("point", "convinced", "coat", 1.0), ("stand", "pain", "pajama", 1.0)]
g = []
for i, (pose, face, cos, stoop) in enumerate(cells):
    cx = 200 + i * 360
    g.append(f'<path d="M{cx} 70 V740" stroke="#d24" stroke-width="2" stroke-dasharray="8 8"/>')
    g.append(f'<g transform="translate({cx},700)">'
             f'{C.character(pose, face, costume=cos, stoop=stoop, scale=1.15)}</g>')
    g.append(f'<text x="{cx}" y="766" font-size="24" fill="#4a3b2a" text-anchor="middle" '
             f'font-family="sans-serif">{pose}/{cos} stoop={stoop}</text>')
SVG = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}"><defs>{C.defs()}</defs>'
       f'<rect width="{W}" height="{H}" fill="#f3ead7"/>{"".join(g)}</svg>')
html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}'
        f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{SVG}</body></html>')
print("wrote", render.png(html, Path(__file__).parent.parent / "out" / "_check_pose.png", W, H))
