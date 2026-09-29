# -*- coding: utf-8 -*-
"""mech_preview.py — 動く模式図（drift・latch・section・hull）の**段ごとの止め絵**を並べて、ブラウザで下見するページを
書き出す（2026-09-29 新設・14本目 ⑤b-4）。

■ なぜ要るか（ルール §5b-76・§5b-85）
  レンダはローカルでやらない（§6-1）。`illu_preview.py` は案C の絵の動きしか再生しない＝drift・hull の**動く部品**
  （PIL で描く＝船の傾き・水位・針路の針・航路の点・無線の輪）が出ない。このページは本番と同じ層の SVG
  （`scene_jiko.layer_index`）に、動く部品を**段の鍵の終わりの状態**で SVG として描き足し、頭と各段の終わりを横に並べる。
  部品の形は本番と同じ関数（`titan_fig.mech_pts`）で計算する。
  ⚠️ 動く途中（点の流れ・輪の広がり・補間）は描かない＝止め絵。**本番の確認は Actions**（`at` で途中のコマ）。
  ⚠️ 本番は段の層を左→右のワイプで出す・動く部品は層の上に描く（このページも同じ重ね順）

■ 使い方
    python tools/mech_preview.py c401 c402 … --out="<Vault>/Resources/事故検証ch-案C見本/ep14" --name=f_c4
    → <out>/<name>.html（1カット1行・頭の状態＋段ごとの終わり）。Vault の `.claude/launch.json` の `jiko-anc-mock` で開く
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J  # noqa: E402
import scene_jiko as S  # noqa: E402
import titan_fig as F  # noqa: E402


def _col(name, pal):
    if not name:
        return None
    if name.startswith("#"):
        return name
    return pal[name] if name in pal else getattr(J, name)


def _last_key(sh, j):
    """段 j の終わりの鍵（j＝-1 は頭＝鍵0）。段 j の鍵が無ければ、それより前の最後の鍵。"""
    if j < 0:
        return sh["keys"][0]
    ks = [k for k in sh["keys"][1:] if k["stage"] <= j]
    return ks[-1] if ks else sh["keys"][0]


def _shape_svg(sh, k, pal):
    a = k.get("alpha", 1.0)
    a = 1.0 if a is None else float(a)
    if a <= 0.01:
        return ""
    fill = _col(k.get("fill", sh.get("fill")), pal)
    stroke = _col(k.get("stroke", sh.get("stroke")), pal)
    w = float(sh.get("w", 4))
    if sh["type"] == "circle":
        cx = sh["c"][0] + float(k.get("dx", 0) or 0)
        cy = sh["c"][1] + float(k.get("dy", 0) or 0)
        r = float(sh["r"])
        g = float(k.get("glow", 0) or 0)
        out = ""
        if g > 0.01 and (fill or stroke):
            out += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 2.2:.1f}" fill="{fill or stroke}" opacity="{0.22 * g * a:.3f}"/>'
        out += (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill or "none"}" stroke="{stroke or "none"}" '
                f'stroke-width="{w}" opacity="{a:.3f}"/>')
        return out
    q = F.mech_pts(sh, k)
    if len(q) < 2:
        return ""
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in q)
    if sh["type"] == "poly":
        return (f'<path d="{d} Z" fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{w}" '
                f'stroke-linejoin="round" opacity="{a:.3f}"/>')
    c = stroke or fill
    out = (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" '
           f'stroke-linejoin="round" opacity="{a:.3f}"/>')
    if sh.get("head"):
        (x1, y1), (x2, y2) = q[-2], q[-1]
        L = math.hypot(x2 - x1, y2 - y1) or 1.0
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        hs = float(sh["head"])
        pts = [(x2, y2), (x2 - ux * hs - uy * hs * 0.55, y2 - uy * hs + ux * hs * 0.55),
               (x2 - ux * hs + uy * hs * 0.55, y2 - uy * hs - ux * hs * 0.55)]
        out += f'<path d="M{pts[0][0]:.1f} {pts[0][1]:.1f} L{pts[1][0]:.1f} {pts[1][1]:.1f} L{pts[2][0]:.1f} {pts[2][1]:.1f} Z" fill="{c}" opacity="{a:.3f}"/>'
    return out


def _moves_svg(cid, moves, j, pal):
    """段 j の終わりまでに出ている動く部品（止め絵）。"""
    ink, amber = pal.get("INK_W", J.INK_W), J.AMBER
    out = []
    for mv in moves:
        k = mv["kind"]
        if k == "anim":
            for sh in mv["shapes"]:
                out.append(_shape_svg(sh, _last_key(sh, j), pal))
            continue
        if mv["stage"] > j:
            continue
        if k == "path":
            p = mv["pts"]
            out.append(f'<path d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in p) + f'" fill="none" stroke="{ink}" '
                       f'stroke-width="4" opacity="0.75"/><circle cx="{p[-1][0]:.1f}" cy="{p[-1][1]:.1f}" r="9" fill="{ink}"/>')
        elif k == "stream":
            (ax, ay), (bx, by) = mv["a"], mv["b"]
            out.append(f'<path d="M{ax:.1f} {ay:.1f} L{bx:.1f} {by:.1f}" stroke="{ink}" stroke-width="3" opacity="0.3"/>')
            out += [f'<circle cx="{ax + (bx - ax) * u:.1f}" cy="{ay + (by - ay) * u:.1f}" r="6" fill="{ink}" opacity="0.8"/>'
                    for u in (0.2, 0.45, 0.7, 0.95)]
        elif k == "sight":
            (ax, ay), (bx, by) = mv["a"], mv["b"]
            out.append(f'<path d="M{ax:.1f} {ay:.1f} L{bx:.1f} {by:.1f}" stroke="{amber}" stroke-width="4" '
                       f'stroke-dasharray="18 12"/><circle cx="{bx:.1f}" cy="{by:.1f}" r="26" fill="{amber}" opacity="0.35"/>')
        elif k == "ring":
            x, y = mv["at"]
            out += [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{mv["r"] * f:.1f}" fill="none" stroke="{amber}" stroke-width="4" '
                    f'opacity="{o}"/>' for f, o in ((0.45, 0.9), (1.0, 0.5))]
        elif k == "gather":
            x, y = mv["at"]
            rg = random.Random(f"{cid}-gather")
            for _ in range(int(mv.get("n", 24))):
                a0, ph = rg.uniform(0, math.tau), rg.random()
                rr = 26 + (mv["r"] - 26) * (1.0 - ph)
                out.append(f'<circle cx="{x + rr * math.cos(a0):.1f}" cy="{y + rr * math.sin(a0):.1f}" r="6" fill="{ink}" '
                           f'opacity="0.85"/>')
        elif k == "fall":
            x, y = mv["at"]
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="#fff" opacity="0.4"/>')
    return "".join(out)


def page(cids, idx, jobs, css_href, last=False):
    rows = []
    for cid in cids:
        v = idx[cid]
        pal = J.palette(S.palette_of(cid))
        L = lambda k: J.remap(jobs[k], S.pal_of_layer(k)) if k in jobs else ""  # noqa: E731
        base = L(f"{cid}_base") + L(f"{cid}_lab")
        cells = []
        for j in ([v["stages"] - 1] if last else range(-1, v["stages"])):
            tags = "".join(L(f"{cid}_a{i + 1}") for i in range(j + 1))
            svg = (f'<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg"><rect width="1920" height="1080" '
                   f'fill="{pal.get("BG", J.BG)}"/>{base}{tags}{_moves_svg(cid, v.get("moves") or [], j, pal)}'
                   f'<rect x="0" y="900" width="1920" height="180" fill="#000"/></svg>')
            cells.append(f'<div class="c"><div class="h">{cid}　{"頭" if j < 0 else f"段{j + 1}の終わり"}</div>{svg}</div>')
        rows.append("".join(cells) if last else f'<div class="r">{"".join(cells)}</div>')
    body = f'<div class="r w">{"".join(rows)}</div>' if last else "".join(rows)
    return ('<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>止め絵 ' + " ".join(cids) + '</title>'
            f'<link rel="stylesheet" href="{css_href}"><style>html,body{{margin:0;background:#16181a;color:#dfe6ea;'
            'font:14px sans-serif} .r{display:flex;gap:6px;margin:0 0 8px} .w{flex-wrap:wrap;width:1932px} '
            '.c{width:640px;flex:none} .h{padding:2px 4px} svg{display:block;width:640px;height:360px}</style></head><body>'
            + body + '</body></html>')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = Path(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), "out/mech_preview"))
    name = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--name=")), "f_" + (args[0] if args else "x"))
    out.mkdir(parents=True, exist_ok=True)
    css = out / "fonts.css"
    if not css.exists():
        S.ensure_css()
        css.write_text(S.CSS, encoding="utf-8")
    idx, jobs = S.layer_index(allow_missing=True)
    (out / f"{name}.html").write_text(page(args, idx, jobs, "fonts.css", last="--last" in sys.argv), encoding="utf-8")
    print(f"✓ {out / (name + '.html')}（{len(args)}カット）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
