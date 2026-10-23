# -*- coding: utf-8 -*-
"""make_map24.py — 24本目 ⑤b-6：地図の図解2つ（c203＝事故の前のソ連とウクライナ・c713＝日本）の国の形を、
Natural Earth（パブリックドメインの地図データ）の 1:50m の国（admin 0）から**範囲を切り出して**小さな JSON にする
（17本目 `ref/ep17/make_coast17.py`・18本目 `ref/ep18/make_coast.py` と同じ切り方・間引き方を読み込んで使う）。

■ なぜ（映像方針 c203「ソ連とウクライナ・色を多く」＝国の境が要る＝陸だけの ne_50m_land では描けない）
  Actions は git から焼く＝元のファイル（3MB）はリポに入れず、切り出した数十KBだけ入れる。
  ⚠️ 1986年の地図として描く＝**ソ連＝15の共和国（いまの15か国）をひとまとめの色**・その中のウクライナ（当時のウクライナ共和国）を別の色。
     🔴 **クリミア半島**：Natural Earth の既定の版はロシアの形の部品に入れている（ロシアの部品のうち、真ん中が経度 32〜37・緯度 44〜46.5 のもの）
        ＝1986年はウクライナ共和国（1954年に移った）＝**ウクライナの側へ移して描く**（事故の前の地図）。
     🔴 **北方領土（択捉島・国後島・色丹島・歯舞群島）**：Natural Earth の既定の版はロシアの形の部品に入れている
        （ロシアの部品のうち、真ん中が経度 145.2〜149.2・緯度 43.2〜45.8 のもの＝得撫島〈経度 149.8〉より南西）
        ＝**日本の側（組 jp）へ移して描く**（日本政府の立場＝日本の領土。c203 では日本と同じ灰・c713 では日本と同じ色）。
  ⚠️ 湖は国の穴（内側の輪）＝外側の輪だけを使うので描かない（17本目・18本目と同じ）。
  ⚠️ 経度 180 度をまたぐロシアの東の端（チュクチ半島）は、経度が −180〜−169 の部品＝360 を足して東へつなぐ。

■ 使い方（元のファイルは 2026-10-23 にカズヤくんの了承をもらって落とした＝推奨どおり・scratchpad に置いた）
    python ref/ep24/make_map24.py <ne_50m_admin_0_countries.geojson の道>
    → ref/ep24/map24_ne50m.json（経度・緯度の多角形・小数3桁＝約0.1km）
  取り元＝https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
  （3,083,490 バイト・md5 686def4ba546d1008ab4a75db581a81a＝2回取って一致）
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ep18"))
from make_coast import clip, simplify  # noqa: E402  （18本目と同じ切り方・間引き方）

SRC_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
MD5 = "686def4ba546d1008ab4a75db581a81a"
OUT = HERE / "map24_ne50m.json"
# 1986年のソ連＝15の共和国（いまの国の ADM0_A3）
USSR = ("RUS", "UKR", "BLR", "MDA", "LTU", "LVA", "EST", "GEO", "ARM", "AZE", "KAZ", "UZB", "TKM", "KGZ", "TJK")
CRIMEA = (32.0, 44.0, 37.0, 46.5)     # ロシアの部品のうち、真ん中（点の平均）がこの範囲のもの＝クリミア半島
NORTH4 = (145.2, 43.2, 149.2, 45.8)   # ロシアの部品のうち、真ん中がこの範囲のもの＝北方領土（択捉・国後・色丹・歯舞）
# 切り出す範囲（経度・緯度）と間引きの許し（度）。地図の範囲より一回り広く
#   o＝ソ連の全体（c203 の左の小さな地図＝1画素 ≈ 12km）・z＝ウクライナの北（c203 の右の地図＝1画素 ≈ 0.25km）・j＝日本（c713）
REGIONS = dict(o=((18.0, 33.0, 192.0, 83.0), 0.12), z=((28.8, 49.8, 32.0, 52.2), 0.006), j=((126.0, 28.0, 148.0, 47.0), 0.03))


def _rings(geo):
    return [geo["coordinates"][0]] if geo["type"] == "Polygon" else [p[0] for p in geo["coordinates"]]


def main():
    sys.setrecursionlimit(100000)
    src = Path(sys.argv[1])
    raw = src.read_bytes()
    if hashlib.md5(raw).hexdigest() != MD5:
        raise SystemExit(f"元のファイルの md5 が {MD5} と違う（版が替わった＝確かめてから）")
    g = json.loads(raw.decode("utf-8"))
    groups = {}                      # (範囲, 組) → 多角形の列。組＝ukr（ウクライナ・クリミアを含む）・su（ほかの14の共和国）・jp（日本）・oth（ほか）
    moved, north = 0, []
    for f in g["features"]:
        a3 = f["properties"]["ADM0_A3"]
        for r in _rings(f["geometry"]):
            pts = [(float(x), float(y)) for x, y in r]
            mx, my = sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)
            grp = "jp" if a3 == "JPN" else "ukr" if a3 == "UKR" else "su" if a3 in USSR else "oth"
            if a3 == "RUS" and CRIMEA[0] <= mx <= CRIMEA[2] and CRIMEA[1] <= my <= CRIMEA[3]:
                grp, moved = "ukr", moved + 1          # 🔴 1986年＝ウクライナ共和国
            if a3 == "RUS" and NORTH4[0] <= mx <= NORTH4[2] and NORTH4[1] <= my <= NORTH4[3]:
                grp = "jp"                             # 🔴 北方領土＝日本の側
                north.append((round(mx, 2), round(my, 2), len(pts)))
            for key, (BBOX, tol) in REGIONS.items():
                q = [(x + 360.0, y) for x, y in pts] if (key == "o" and a3 == "RUS" and mx < -160.0) else pts
                xs, ys = [p[0] for p in q], [p[1] for p in q]
                if max(xs) < BBOX[0] or min(xs) > BBOX[2] or max(ys) < BBOX[1] or min(ys) > BBOX[3]:
                    continue
                c = clip(q, BBOX)
                if len(c) < 3:
                    continue
                s = simplify(c, tol)
                if len(s) >= 3:
                    groups.setdefault(f"{key}_{grp}", []).append([[round(x, 3), round(y, 3)] for x, y in s])
    if moved != 1:
        raise SystemExit(f"クリミア半島の部品が {moved} 個（1つのはず＝版が替わった）")
    print(f"北方領土として日本の側へ移した部品（真ん中の経度・緯度・点の数）：{north}")
    if not 3 <= len(north) <= 6:
        raise SystemExit(f"北方領土の部品が {len(north)} 個（択捉・国後・色丹〈・歯舞〉のはず＝版が替わった）")
    out = dict(source=SRC_URL, license="Public domain（Natural Earth）", file="ne_50m_admin_0_countries.geojson",
               bytes=len(raw), md5=MD5, taken="2026-10-23", regions={k: dict(bbox=list(b), tol_deg=t) for k, (b, t) in REGIONS.items()},
               ussr=list(USSR), crimea=list(CRIMEA), north4=list(NORTH4), north4_parts=len(north),
               note="24本目 ⑤b-6 地図の図解（c203・c713）。経度（西が −）・緯度の多角形。外側の輪だけ（湖の穴は捨てた）。"
                    "組＝ukr（1986年のウクライナ共和国＝クリミア半島を含む）・su（ほかの14の共和国）・jp（北方領土を含む）・oth。範囲 o はチュクチ半島に 360 を足した",
               polys=groups)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for k in sorted(groups):
        print(f"{k}: 多角形 {len(groups[k])}・点 {sum(len(p) for p in groups[k])}")
    print(f"{OUT.name}: {OUT.stat().st_size} バイト・元の md5 {MD5}・クリミアの部品を移した {moved}")


if __name__ == "__main__":
    main()
