# -*- coding: utf-8 -*-
"""make_coast17.py — 17本目 ⑤b-5：模式図の地図（c613＝イギリスの航空の当局 → エアバス社〈トゥールーズ〉）の陸の形を、
Natural Earth（パブリックドメインの地図データ）の 1:50m の陸地から**範囲を切り出して**小さな JSON にする
（18本目 `ref/ep18/make_coast.py`・21本目 `ref/ep21/make_coast21.py` と同じ切り方・間引き方を読み込んで使う）。

■ なぜ（映像方針 c613「地図（イギリスの当局 → エアバス社〈トゥールーズ〉）」＝海をはさんだ2つの国が見えないと伝わらない）
  Actions は git から焼く＝元のファイル（1.6MB）はリポに入れず、切り出した数十KBだけ入れる。
  ⚠️ 陸地のデータには国境が無い（フランスはスペイン・ベルギーと地続き）＝国の形の線ではなく「陸」＝図の札で断る。
  ⚠️ 湖は陸地の穴（湖の輪）＝外側の輪だけを使うので描かない（18本目と同じ）。

■ 使い方（元のファイルは 2026-10-20 にカズヤくんの了承をもらって落とした＝推奨どおり・scratchpad に置いた）
    python ref/ep17/make_coast17.py <ne_50m_land.geojson の道>
    → ref/ep17/coast_eu_ne50m.json（経度・緯度の多角形・小数3桁＝約0.1km）
  取り元＝https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson
  （1,636,166 バイト・md5 e6a67ac9acdbc6e9437db594e9c2d0a1＝2回取って一致・18本目・21本目と同じ版）
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ep18"))
from make_coast import SRC_URL, clip, simplify  # noqa: E402  （18本目と同じ切り方・間引き方）

OUT = HERE / "coast_eu_ne50m.json"
# 切り出す範囲（経度 西が −・緯度）＝イギリスとフランスの模式の地図（`tools/mech17.py` の MAP_VIEW["eu"]）より一回り広く
BBOX = (-14.0, 38.0, 12.0, 61.0)
TOL = 0.02                           # 間引きの許し（度＝約2km。地図は1画素≈2km）
MD5 = "e6a67ac9acdbc6e9437db594e9c2d0a1"


def main():
    sys.setrecursionlimit(100000)    # ユーラシアの輪は点が多い＝間引きの再帰が深くなる
    src = Path(sys.argv[1])
    raw = src.read_bytes()
    if hashlib.md5(raw).hexdigest() != MD5:
        raise SystemExit(f"元のファイルの md5 が {MD5} と違う（版が替わった＝確かめてから）")
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
               bytes=len(raw), md5=hashlib.md5(raw).hexdigest(), taken="2026-10-20", bbox=list(BBOX), tol_deg=TOL,
               note="17本目 ⑤b-5 模式図の地図（イギリスとフランス）。経度（西が −）・緯度の多角形。外側の輪だけ（湖の穴は捨てた）・国境なし",
               polys=polys)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{OUT.name}: 多角形 {len(polys)}・点 {sum(len(p) for p in polys)}・{OUT.stat().st_size} バイト・元の md5 {out['md5']}")


if __name__ == "__main__":
    main()
