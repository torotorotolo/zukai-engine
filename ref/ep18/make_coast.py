# -*- coding: utf-8 -*-
"""make_coast.py — 18本目 ⑤b-2：位置の小さな地図（置き場 SA の左上・SB を東海岸まで縮めた版）の海岸線を、
Natural Earth（パブリックドメインの地図データ）の 1:50m の陸地から**範囲を切り出して**小さな JSON にする。

■ なぜ（Vault 映像方針 18本目 §4 #1・§10／⑤b-1 引き継ぎ §4）
  証拠50（X p.131）は手描きの海図で、西経70度より西（ボストン・ポーツマスの造船所）が枠の外＝東海岸まで引けない。
  Natural Earth の陸地（PD）で引く。Actions は git から焼く＝元のファイル（1.6MB）はリポに入れず、切り出した数KBだけ入れる。

■ 使い方（元のファイルは 2026-10-04 にカズヤくんの了承をもらって落とした）
    python ref/ep18/make_coast.py <ne_50m_land.geojson の道>
    → ref/ep18/coast_ne50m.json（経度・緯度の多角形・小数3桁＝約0.1km）
  取り元＝https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson
  （Natural Earth の公式の配布・1,636,166 バイト・md5 e6a67ac9acdbc6e9437db594e9c2d0a1）
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "coast_ne50m.json"
# 切り出す範囲（経度 西が −・緯度）。位置の小さな地図の枠（illu.SA_INSET）より一回り広く＝枠の端で海岸線が切れて見えない
BBOX = (-72.5, 39.5, -61.5, 45.5)
TOL = 0.008                          # 間引きの許し（度＝約0.7km。小さな地図は1画素≈2.3km）
SRC_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson"


def clip(poly, bbox):
    """多角形を長方形で切る（Sutherland–Hodgman）。"""
    x0, y0, x1, y1 = bbox
    edges = ((lambda p: p[0] >= x0, lambda p, q: (x0, p[1] + (q[1] - p[1]) * (x0 - p[0]) / (q[0] - p[0]))),
             (lambda p: p[0] <= x1, lambda p, q: (x1, p[1] + (q[1] - p[1]) * (x1 - p[0]) / (q[0] - p[0]))),
             (lambda p: p[1] >= y0, lambda p, q: (p[0] + (q[0] - p[0]) * (y0 - p[1]) / (q[1] - p[1]), y0)),
             (lambda p: p[1] <= y1, lambda p, q: (p[0] + (q[0] - p[0]) * (y1 - p[1]) / (q[1] - p[1]), y1)))
    out = list(poly)
    for inside, cross in edges:
        src, out = out, []
        if not src:
            break
        prev = src[-1]
        for cur in src:
            if inside(cur):
                if not inside(prev):
                    out.append(cross(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cross(prev, cur))
            prev = cur
    return out


def simplify(pts, tol):
    """Douglas–Peucker（閉じた多角形は最初の点で開いて間引く）。"""
    if len(pts) < 4:
        return pts

    def dp(a, b):
        if b <= a + 1:
            return [pts[a]]
        (ax, ay), (bx, by) = pts[a], pts[b]
        dx, dy = bx - ax, by - ay
        L = (dx * dx + dy * dy) ** 0.5
        k, dmax = a, -1.0
        for i in range(a + 1, b):
            # 🔴 始点と終点が同じ点（切り出した輪は閉じる）だと線の距離が全部0＝輪が2点に潰れた（1回目の出力）
            #    ＝その区間は始点からの距離で測る
            d = (abs(dy * pts[i][0] - dx * pts[i][1] + bx * ay - by * ax) / L if L > 1e-9
                 else ((pts[i][0] - ax) ** 2 + (pts[i][1] - ay) ** 2) ** 0.5)
            if d > dmax:
                k, dmax = i, d
        if dmax <= tol:
            return [pts[a]]
        return dp(a, k) + dp(k, b)
    return dp(0, len(pts) - 1) + [pts[-1]]


def main():
    src = Path(sys.argv[1])
    raw = src.read_bytes()
    g = json.loads(raw.decode("utf-8"))
    polys = []
    for f in g["features"]:
        geo = f["geometry"]
        rings = [geo["coordinates"][0]] if geo["type"] == "Polygon" else [p[0] for p in geo["coordinates"]]
        for r in rings:
            xs, ys = [p[0] for p in r], [p[1] for p in r]
            if max(xs) < BBOX[0] or min(xs) > BBOX[2] or max(ys) < BBOX[1] or min(ys) > BBOX[3]:
                continue
            c = clip([(float(x), float(y)) for x, y in r], BBOX)
            if len(c) < 3:
                continue
            s = simplify(c, TOL)
            if len(s) >= 3:
                polys.append([[round(x, 3), round(y, 3)] for x, y in s])
    out = dict(source=SRC_URL, license="Public domain（Natural Earth）", file="ne_50m_land.geojson",
               bytes=len(raw), md5=hashlib.md5(raw).hexdigest(), taken="2026-10-04", bbox=list(BBOX), tol_deg=TOL,
               note="18本目 ⑤b-2 位置の小さな地図（置き場 SA の左上）。経度（西が −）・緯度の多角形。外側の輪だけ（湖の穴は捨てた）",
               polys=polys)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{OUT.name}: 多角形 {len(polys)}・点 {sum(len(p) for p in polys)}・{OUT.stat().st_size} バイト・元の md5 {out['md5']}")


if __name__ == "__main__":
    main()
