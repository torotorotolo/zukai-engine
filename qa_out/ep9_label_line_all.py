# -*- coding: utf-8 -*-
"""⑤c' 机上で全数：mapfig・graph の札（字の外接矩形）と、線（道すじ・折れ線）の最短距離。描画はしない。

字の外接矩形＝fontmetrics の幅 × [基線−0.80em, 基線+0.10em]。線の太さの半分を引いた「すき間」を出す。
"""
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import fontmetrics as fm  # noqa: E402
import scene_jiko as S  # noqa: E402

jobs, _ = S.build_layers()


def seg_rect_dist(xa, ya, xb, yb, r):
    """線分と矩形の最短距離（交われば 0）。"""
    best = 1e9
    for i in range(201):
        t = i / 200
        x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
        dx = max(r[0] - x, 0, x - r[2])
        dy = max(r[1] - y, 0, y - r[3])
        best = min(best, np.hypot(dx, dy))
    return best


rows = []
for cid in S.ORDER:
    fig = (S.SPEC.get(cid) or {}).get("fig")
    if not fig or fig[0] not in ("mapfig", "graph"):
        continue
    svg_all = "".join(v for k, v in jobs.items() if k.startswith(cid + "_") and not k.endswith("_base"))
    lines = []
    for m in re.finditer(r'<path d="([^"]+)"([^>]*)>', svg_all):
        attrs = m.group(2)
        sw = re.search(r'stroke-width="([\d.]+)"', attrs)
        if not sw or 'fill="none"' not in attrs:
            continue
        col = re.search(r'stroke="(#[0-9a-f]{6})"', attrs).group(1)
        if col in ("#22333f", "#41606f", "#1c2a35") or float(sw.group(1)) < 4:
            continue                                   # 地紋・目盛・枠は除く
        pts = [(float(a), float(b)) for a, b in re.findall(r"([\d.]+) ([\d.]+)", m.group(1))]
        if len(pts) >= 2:
            lines.append((pts, float(sw.group(1)), col))
    for k in [k for k in jobs if k.startswith(cid + "_") and re.fullmatch(rf"{cid}_a\d+", k)]:
        svg = re.sub(r"<tspan[^>]*>", "", jobs[k]).replace("</tspan>", "")
        for m in re.finditer(r"<text([^>]*)>(.*?)</text>", svg):
            at, body = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
            x = float(re.search(r'\bx="([\d.-]+)"', at).group(1))
            y = float(re.search(r'\by="([\d.-]+)"', at).group(1))
            fs = float(re.search(r'font-size="([\d.]+)"', at).group(1))
            an = re.search(r'text-anchor="(\w+)"', at)
            an = an.group(1) if an else "start"
            w = fm.width(body, fs, "Noto")
            x0 = x if an == "start" else (x - w if an == "end" else x - w / 2)
            r = (x0, y - 0.80 * fs, x0 + w, y + 0.10 * fs)
            outl = "stroke=" in at
            for pts, sw, col in lines:
                d = min(seg_rect_dist(*pts[i], *pts[i + 1], r) for i in range(len(pts) - 1))
                gap = d - sw / 2
                if gap < 4:
                    rows.append((cid, fig[0], body, gap, col, outl))
rows.sort(key=lambda r: (S.ORDER.index(r[0]), r[3]))
n_cut = len({r[0] for r in rows})
print(f"■ 札と線のすき間が 4px 未満（負＝線が字の外接矩形に入る）：{len(rows)} 件 ／ {n_cut} カット")
for cid, kind, body, gap, col, outl in rows:
    print(f"  {cid} {kind:6s} 「{body}」 すき間 {gap:6.1f}px  線 {col}" + ("  字にフチあり" if outl else ""))
n_all = len([c for c in S.ORDER if ((S.SPEC.get(c) or {}).get('fig') or ('',))[0] in ('mapfig', 'graph')])
print(f"（mapfig・graph のカットは全 {n_all}）")
