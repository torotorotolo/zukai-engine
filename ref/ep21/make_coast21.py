# -*- coding: utf-8 -*-
"""make_coast21.py — 21本目 ⑤b-3：模式図の地図（4便の行き先 c202・北東部の防空の基地 c318／c319／c419）の海岸線を、
Natural Earth（パブリックドメインの地図データ）の 1:50m の陸地から**範囲を切り出して**小さな JSON にする
（18本目 `ref/ep18/make_coast.py` と同じ切り方・間引き方を読み込んで使う）。

■ なぜ（台本 第2版 c202「東の海岸から西の海岸へ、大陸を横切る」・c319「海外から来る機だけ」＝海と陸が見えないと伝わらない）
  Actions は git から焼く＝元のファイル（1.6MB）はリポに入れず、切り出した数十KBだけ入れる。
  ⚠️ 陸地のデータには国境が無い（カナダ・メキシコと地続き）＝アメリカの形の線ではなく「北アメリカの陸」＝図の札で断る。
  ⚠️ 五大湖は陸地の穴（湖の輪）＝外側の輪だけを使うので描かない（18本目と同じ）。

■ 使い方（元のファイルは 2026-10-12 にカズヤくんの了承をもらって落とした＝推奨どおり）
    python ref/ep21/make_coast21.py <ne_50m_land.geojson の道>
    → ref/ep21/coast_ne50m.json（経度・緯度の多角形・小数3桁＝約0.1km）
  取り元＝https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson
  （1,636,166 バイト・md5 e6a67ac9acdbc6e9437db594e9c2d0a1＝2回取って一致・18本目と同じ版）
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ep18"))
from make_coast import SRC_URL, clip, simplify  # noqa: E402  （18本目と同じ切り方・間引き方）

OUT = HERE / "coast_ne50m.json"
# 切り出す範囲（経度 西が −・緯度）＝アメリカ本土の模式の地図（`tools/mech21.py` の MAP_VIEW["us"]）より一回り広く。
#   北東部の地図（MAP_VIEW["ne"]）もこの中に入る＝1つのファイルで2つの地図
BBOX = (-132.0, 20.0, -56.0, 54.0)
TOL = 0.02                           # 間引きの許し（度＝約2km。北東部の地図は1画素≈1.3km・本土の地図は1画素≈3km）


def main():
    sys.setrecursionlimit(100000)    # 北アメリカの輪は点が多い＝間引きの再帰が深くなる
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
               bytes=len(raw), md5=hashlib.md5(raw).hexdigest(), taken="2026-10-12", bbox=list(BBOX), tol_deg=TOL,
               note="21本目 ⑤b-3 模式図の地図（本土と北東部）。経度（西が −）・緯度の多角形。外側の輪だけ（湖の穴は捨てた）・国境なし",
               polys=polys)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{OUT.name}: 多角形 {len(polys)}・点 {sum(len(p) for p in polys)}・{OUT.stat().st_size} バイト・元の md5 {out['md5']}")


if __name__ == "__main__":
    main()
