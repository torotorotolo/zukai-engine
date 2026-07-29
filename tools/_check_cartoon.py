# -*- coding: utf-8 -*-
"""EHL5様式キャラの検証シート。参考フレームと並べて比率を確かめる。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
import cartoon as K
import render

W, H = 1900, 1200
cells = [("stand", "normal", "shirt", "short"), ("hips", "smile", "shirt", "short"),
         ("point", "worry", "coat", "short"), ("stand", "shock", "shirt", "curly")]
g = []
for i, (p, f, c, hr) in enumerate(cells):
    cx = 230 + i * 340
    g.append(f'<path d="M{cx} 60 V740" stroke="#d24" stroke-width="2" stroke-dasharray="9 9"/>')
    g.append(f'<g transform="translate({cx},700)">{K.character(p, f, costume=c, hair=hr, scale=0.62)}</g>')
    g.append(f'<text x="{cx}" y="770" font-size="26" fill="#333" text-anchor="middle" font-family="sans-serif">{p}/{f}/{hr}</text>')
for i, (f, sw, rn) in enumerate([("normal",0,0.0),("angry",3,0.25),("smile",0,0.0),("tired",1,0.0)]):
    cx = 1420 + (i % 2) * 260
    cy = 400 + (i // 2) * 520
    g.append(f'<g transform="translate({cx},{cy})">{K.kidney_char(f, sweat=sw, run=rn, scale=0.78, arms_up=(0.8 if f=="smile" else 0))}</g>')
    g.append(f'<text x="{cx}" y="{cy+250}" font-size="24" fill="#333" text-anchor="middle" font-family="sans-serif">kidney/{f}</text>')
SVG = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<rect width="{W}" height="{H}" fill="#f6e5ad"/>{"".join(g)}</svg>')
html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}'
        f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{SVG}</body></html>')
print("wrote", render.png(html, Path(__file__).parent.parent / "out" / "_check_cartoon.png", W, H))
