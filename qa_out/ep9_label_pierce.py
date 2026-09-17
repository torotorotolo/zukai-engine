# -*- coding: utf-8 -*-
"""キー橋 §W-7-2 の物差しで分ける：線が字面の「真ん中6割」（縦横とも中央60%）に入る＝貫く／外接矩形にだけ触れる＝かすめる。"""
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import fontmetrics as fm  # noqa: E402
import scene_jiko as S  # noqa: E402

jobs, _ = S.build_layers()
CUTS = ["c201", "c316", "c408", "c416", "c510", "pr06", "pr08"]


def lines_of(cid):
    svg_all = "".join(v for k, v in jobs.items() if k.startswith(cid + "_") and not k.endswith("_base"))
    out = []
    for m in re.finditer(r'<path d="([^"]+)"([^>]*)>', svg_all):
        at = m.group(2)
        sw = re.search(r'stroke-width="([\d.]+)"', at)
        if not sw or 'fill="none"' not in at:
            continue
        col = re.search(r'stroke="(#[0-9a-f]{6})"', at).group(1)
        if col in ("#22333f", "#41606f", "#1c2a35") or float(sw.group(1)) < 4:
            continue
        pts = [(float(a), float(b)) for a, b in re.findall(r"([\d.]+) ([\d.]+)", m.group(1))]
        if len(pts) >= 2:
            out.append((pts, float(sw.group(1))))
    return out


for cid in CUTS:
    ls = lines_of(cid)
    for k in [k for k in jobs if re.fullmatch(rf"{cid}_a\d+", k)]:
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
            X0, X1, Y0, Y1 = x0, x0 + w, y - 0.80 * fs, y + 0.10 * fs
            cx0, cx1 = X0 + 0.2 * w, X1 - 0.2 * w
            cy0, cy1 = Y0 + 0.2 * (Y1 - Y0), Y1 - 0.2 * (Y1 - Y0)
            touch = pierce = 0.0
            for pts, sw in ls:
                for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                    seg = np.hypot(xb - xa, yb - ya)
                    for i in range(400):
                        t = (i + 0.5) / 400
                        px, py = xa + (xb - xa) * t, ya + (yb - ya) * t
                        h = sw / 2
                        if X0 - h <= px <= X1 + h and Y0 - h <= py <= Y1 + h:
                            touch += seg / 400
                        if cx0 <= px <= cx1 and cy0 - h <= py <= cy1 + h:
                            pierce += seg / 400
            if touch > 0:
                kind = "貫く" if pierce > 0 else "かすめる"
                print(f"{cid} 「{body}」 {kind}（矩形に触れる {touch:.0f}px・真ん中6割 {pierce:.0f}px）")
