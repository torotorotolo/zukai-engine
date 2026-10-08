# -*- coding: utf-8 -*-
"""night20.py — 20本目 ⑤b-4：再現イラスト S4（夜の地図・上から）の点を、解説の図13（航空機による墜落場所の特定図・解説 p.20＝
`ref/ja123/kz013.png`）と表3（各航空機の測位結果・p.19）から読んで、緯度・経度にする → `ref/ep20/night20.json`。

■ なぜ（台本 第2版 c508「夜の4つの点と誤差の輪・墜落地点＝解説 表3・図13 を自前の地図に」・c501「扇平山・三国山・目撃した4人」）
  図13 の拡大図（右下に 0〜5km の目盛り＝1km 105画素）は、墜落位置と ①〜⑦ の測位の点・三国山・三国峠・扇平山を同じ地図に描いている
  ＝墜落位置（報告書 p.8 の緯度経度）からの東西・南北のずれ（km）で読む（拡大図の北は上）。
  🔴 拡大図の下の地図は今の地形図（左上の湖は 2005 年にできた南相木ダムの奥三川湖）＝**地形・川・湖は写さない**（1985 年に無い物を描かない）。
     写すのは点と山の印だけ
■ 測り方（⑤b-4）：赤い丸（①〜⑦・墜落位置の◎）＝赤い画素のかたまりの重心／山の▲△＝黒い画素のかたまりの重心（△は輪郭の三角の重心）／
  目盛り＝0 と 5km の刻みの列（103・628 画素）
■ 検算（表3 の「誤差」＝報告の位置と墜落位置の距離）：①3.12（表 3km）・②6.18（6）・③3.77（4）・④2.29（2）・⑤3.25（3）・⑥0.71（1以下）・
  ⑦1.16（1）。①〜④を TACAN の方位・距離（海里・磁方位＝西へ7度の偏差）から計算した位置とは 0.06〜1.22km
  ⚠️ 三国山は墜落位置から 2.49km・方位133度（報告書 2.3 p.8「三国山の北北西約2.5キロメートル」＝方位157.5度と 24度ちがう）＝地図は図13 のまま
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "night20.json"
CRASH = (138 + 41 / 60 + 49 / 3600, 35 + 59 / 60 + 54 / 3600)       # 報告書 p8「北緯35度59分54秒、東経138度41分49秒」
FIG_CRASH = (448.8, 827.8)                                          # 図13 の墜落位置の◎（赤い画素の重心）
FIG_KM = (628 - 103) / 5.0                                          # 1km の画素（目盛り 0〜5km）
# 表3 の点（図13 の画素）。時刻・航空機・報告・誤差（km）は表3 の字
POINTS = [
    dict(n=1, t="19:15", who="米軍（C-130）", what="火災発見", err=3.0, px=(648.6, 567.7), night=True),
    dict(n=2, t="19:21", who="航空自衛隊戦闘機（F-4EJ×2）", what="炎を確認", err=6.0, px=(918.2, 1276.6), night=True),
    dict(n=3, t="20:42", who="航空自衛隊ヘリコプター（V-107）", what="炎を確認", err=4.0, px=(198.5, 1134.2), night=True),
    dict(n=4, t="01:00", who="航空自衛隊ヘリコプター（V-107）", what="地上の県警を誘導、失敗", err=2.0, px=(378.5, 1057.5), night=True),
    dict(n=5, t="04:39", who="航空自衛隊ヘリコプター（V-107）", what="捜索", err=3.0, px=(173.0, 1028.0), night=False),
    dict(n=6, t="05:00", who="陸上自衛隊ヘリコプター（HU-1B）", what="捜索", err=1.0, px=(492.9, 887.4), night=False),
    dict(n=7, t="05:33", who="航空自衛隊ヘリコプター（V-107）", what="捜索", err=1.0, px=(506.9, 720.6), night=False),
]
PEAKS = dict(mikuni=("三国山", (639.8, 1006.2)), ougi=("扇平山", (168.6, 1133.3)), touge=("三国峠", (640.0, 1069.0)))
KX = math.cos(math.radians(CRASH[1])) * 111.32
KY = 110.57


def km(px):
    return ((px[0] - FIG_CRASH[0]) / FIG_KM, -(px[1] - FIG_CRASH[1]) / FIG_KM)


def ll(px):
    e, n = km(px)
    return (CRASH[0] + e / KX, CRASH[1] + n / KY)


def build():
    out = dict(note="20本目 ⑤b-4 night20.py の出力（手で直さない）。座標は［東経, 北緯］・km は墜落位置からの［東, 北］",
               src="解説 p20（図13 航空機による墜落場所の特定図）・p19（表3 各航空機の測位結果）", crash=list(CRASH), fig_km=FIG_KM,
               points=[dict(p, km=[round(v, 3) for v in km(p["px"])], ll=list(ll(p["px"])),
                            dist=round(math.hypot(*km(p["px"])), 2)) for p in POINTS],
               peaks={k: dict(name=nm, km=[round(v, 3) for v in km(px)], ll=list(ll(px))) for k, (nm, px) in PEAKS.items()})
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in out["points"]:
        print(p["n"], p["t"], p["km"], "距離", p["dist"], "表3", p["err"])


if __name__ == "__main__":
    build()
