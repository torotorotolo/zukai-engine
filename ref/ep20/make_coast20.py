# -*- coding: utf-8 -*-
"""make_coast20.py — 20本目 ⑤b-3：再現イラスト S2（上から見た経路の地図）の海岸線を、Natural Earth（パブリックドメインの地図データ）の
1:10m の陸地から**範囲を切り出して**小さな JSON にする（18本目 `ref/ep18/make_coast.py` と同じ作り＝切る・間引くは同じ関数）。

■ なぜ（台本 第2版 c209 の画の欄「海岸線は Natural Earth」・映像方針 20本目）
  報告書の付図-1（経路の略図）は手で引いた略図で、海岸線の形も目安。経路の点は付図-1 から読み、陸と海は Natural Earth で引く
  （付図-1 の画素と緯度経度の対応は `ref/ep20/route20.py` が海岸線どうしを重ねて求める）。
  Actions は git から焼く＝元のファイル（約10MB）はリポに入れず、切り出した数十KBだけ入れる。

■ 使い方（元のファイルは 2026-10-08 にカズヤくんの了承をもらって落とした＝1:10m を推奨どおり）
    python ref/ep20/make_coast20.py <ne_10m_land.geojson の道>
    → ref/ep20/coast_ne10m.json（経度・緯度の多角形・小数3桁＝約0.1km）
  取り元＝https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson
  （Natural Earth の公式の配布・10,157,965 バイト・md5 24846ec719e08158ef49593f8b97ca21＝2回取って一致）
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ep18"))
from make_coast import clip, simplify  # noqa: E402  （18本目と同じ切り方・間引き方）

OUT = HERE / "coast_ne10m.json"
# 切り出す範囲（経度・緯度）。地図（S2＝1画素 約217m・真ん中 東経139.055度 北緯35.378度）の画面いっぱい（左右 約±2.3度・上下 約±1.1度）より
#   一回り広く＝画面の端で陸が切れて海に見えない（⑤b-3 の1回目は経路の範囲だけ＝画面の左の 1/5 が海になった）
BBOX = (136.5, 34.0, 141.6, 36.8)
TOL = 0.002                          # 間引きの許し（度＝約0.2km。地図は1画素≈0.2km）
SRC_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson"


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
    out = dict(source=SRC_URL, license="Public domain（Natural Earth）", file="ne_10m_land.geojson",
               bytes=len(raw), md5=hashlib.md5(raw).hexdigest(), taken="2026-10-08", bbox=list(BBOX), tol_deg=TOL,
               note="20本目 ⑤b-3 再現イラスト S2（上から見た経路の地図）。経度・緯度の多角形。外側の輪だけ（湖の穴は捨てた）",
               polys=polys)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{OUT.name}: 多角形 {len(polys)}・点 {sum(len(p) for p in polys)}・{OUT.stat().st_size} バイト・元の md5 {out['md5']}")


if __name__ == "__main__":
    main()
