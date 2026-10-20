# -*- coding: utf-8 -*-
"""make_ise17.py — 17本目 ⑤b-6：空港の地図（c727）の左上の**位置の小さな地図**（伊勢湾のまわり）の陸の形。

■ 元＝20本目の切り出し `ref/ep20/coast_ne10m.json`（Natural Earth 1:10m の陸地・パブリックドメイン・経度 136.5〜141.6・緯度 34.0〜36.8）を**読むだけ**
  （ほかの回の置き場には書かない）。名古屋空港（北緯 35.26・東経 136.92）は元の範囲の西の端に近い＝伊勢湾の西の岸の一部は元の範囲の外（136.5 より西は無い）。
  小さな地図は「伊勢湾の奥のどこか」を示すだけ＝範囲の外の陸は描かない（地図の枠で切る）。
■ 使い方：python ref/ep17/make_ise17.py → ref/ep17/coast_ise_ne10m.json（範囲に掛かる輪だけ・座標はそのまま）
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "ep20" / "coast_ne10m.json"
OUT = HERE / "coast_ise_ne10m.json"
BBOX = (136.50, 34.50, 137.40, 35.45)      # 経度0・緯度0・経度1・緯度1（c727 の小さな地図の範囲＝satmap の inset の bbox と同じ）
PAD = 0.3


def main():
    raw = SRC.read_bytes()
    d = json.loads(raw)
    lo0, la0, lo1, la1 = BBOX
    keep = [p for p in d["polys"] if any(lo0 - PAD <= lo <= lo1 + PAD and la0 - PAD <= la <= la1 + PAD for lo, la in p)]
    out = dict(source=d["source"], license=d["license"], file=d["file"], bytes=d["bytes"], md5=d["md5"], taken=d["taken"],
               derived_from="ref/ep20/coast_ne10m.json", derived_md5=hashlib.md5(raw).hexdigest(), bbox=list(BBOX), tol_deg=d["tol_deg"],
               note="17本目 ⑤b-6 位置の小さな地図（c727・伊勢湾のまわり）。20本目の切り出しから範囲に掛かる輪だけ。経度・緯度の多角形", polys=keep)
    OUT.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"{OUT.name}：輪 {len(keep)}／{len(d['polys'])}・点 {sum(len(p) for p in keep)}・{OUT.stat().st_size:,} バイト")


if __name__ == "__main__":
    main()
