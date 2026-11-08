# -*- coding: utf-8 -*-
"""31本目 ⑤b-3b：地図の描き足しの線（`ref/ep31/sat_lines31.json`＝`tools/cuts/ss.SAT_LINES`）を作る。標準ライブラリだけ。

  python -P ref/ep31/eizou_build/helpers/lines31.py          # json を書く（点は ss.GEO・画は gshot31.GMAP）
  python -P ref/ep31/eizou_build/helpers/lines31.py --print  # 書かずに、線ごとの点の数と緯度の範囲を出す

🔴 **どの線も概略**（資料の言葉から描いた＝位置の記録ではない）。額の下の断りに「概略」を書く（ss.SAT_LINE_NOTE）。
  ・J11L＝「函館（函館空港の住所の点）」と「松島（松島基地の住所の点）」を結ぶ直線（国会会議録 1971-10-07「J10L函館NDB、J11L松島NDB」）。
    NDB の位置は手元の資料に無い＝空港と基地の点で代えた。この直線で盛岡市役所の西 約7キロ・雫石町役場の東 約8キロ
    （判決の「実際のそれよりもかなり東方の盛岡市上空附近」・「J11Lの西側五海里内」と食い違わない＝確かめた）
  ・教官が思っていた線＝J11L と同じ向きで盛岡市役所の点を通る線（判決「かなり東方の盛岡市上空附近を通つているものと誤信」）
  ・西側の帯＝J11L から西へ 5海里（9.26キロ）までの帯（判決「J11Lの西側五海里内」）
  ・旅客機の道＝J11L の西へ約1.5キロに沿って南へ（判決「に沿つてその西側を南下航行中」＝幅は描き分けのため・値の記録ではない）
  ・訓練機の2機＝c501「北上 → 盛岡市の西北で右旋回 → 南下」（防衛庁長官の報告）・c506「旋回をくり返しながら盛岡市の西方を南下」
    （国会会議録 1971-10-07）＝道すじは模式（旅客機の線と交わらせない＝接触の場所を言い切らない）
  各画の線は**額の内側で切る**（門番 check_sat が線の外接の箱を額の内側・Google の部品の箱の外で測る）＝撮った絵の y 50〜960 の内
"""
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, HERE)
import gshot31 as G  # noqa: E402

OUT = os.path.join(REPO, "ref", "ep31", "sat_lines31.json")
NM5 = 9.26              # 5海里（キロ）
Y0, Y1 = 50, 960        # 線を置く撮った絵の y の範囲（上＝額の縁・下＝ロゴ y≥1000・左下の小窓 y≥985 の手前）


def geo():
    import cuts.ss as ss
    return ss.GEO


def km_lon(lat):
    return 111.32 * math.cos(math.radians(lat))


def j11l(lat, P):
    """J11L の概略（函館と松島を結ぶ直線）の、緯度 lat の経度。"""
    (a, b), (c, d) = P["hakodate"]["ll"], P["matsushima"]["ll"]
    t = (a - lat) / (a - c)
    return b + t * (d - b)


def tilt(P):
    """J11L の北からの傾きの余弦（垂直のずれ＝横のずれ×cos）。"""
    (a, b), (c, d) = P["hakodate"]["ll"], P["matsushima"]["ll"]
    dx = (d - b) * km_lon((a + c) / 2)
    dy = (c - a) * 111.32
    return abs(dy) / math.hypot(dx, dy)


def off(lat, lon, km, P):
    """J11L に垂直に km だけ西（負なら東）へずらした点（緯度は同じ・経度だけ＝傾き 約5度の余弦で割る）。"""
    return lat, lon - km / tilt(P) / km_lon(lat)


def lat_of_y(code, y):
    r = G.GMAP[code]
    (lat0, lon0), z = r["ll"], r["z"]
    n = 256 * 2 ** z
    p = math.radians(lat0)
    wy0 = (1 - math.log(math.tan(p) + 1 / math.cos(p)) / math.pi) / 2 * n
    wy = (y / G.DPR - G.CH / 2) + wy0
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * wy / n))))


def span(code, P, lo=None, hi=None, y0=Y0, y1=Y1):
    """その画の額の内側の緯度の範囲（北, 南）。lo・hi で端を絞る（線の端点＝函館・松島の緯度）。"""
    n, s = lat_of_y(code, y0), lat_of_y(code, y1)
    if hi is not None:
        n = min(n, hi)
    if lo is not None:
        s = max(s, lo)
    return n, s


def seq(n, s, step=0.05):
    k = max(2, int(math.ceil((n - s) / step)) + 1)
    return [n - (n - s) * i / (k - 1) for i in range(k)]


def r6(p):
    return (round(p[0], 6), round(p[1], 6))


def build():
    P = geo()
    hk, ms = P["hakodate"]["ll"][0], P["matsushima"]["ll"][0]
    L = {}

    def jline(code, **kw):
        n, s = span(code, P, lo=ms, hi=hk, **kw)
        return [r6((la, j11l(la, P))) for la in seq(n, s)]

    # J11L（各画で額の内側に切る）
    for code in ("G01", "G03", "G05", "G06", "G07", "G08"):
        L["j11l_" + code.lower()] = jline(code)
    # c201：計画の経路（千歳 → 函館 → 松島 → 大子 → 佐倉 → 木更津 → 羽田）＝点を結ぶ直線（国会議員のまとめの順）
    L["route_g02"] = [r6(P[k]["ll"]) for k in ("chitose", "hakodate", "matsushima", "daigo", "sakura", "kisarazu", "haneda")]
    L["j11l_g02"] = [r6(P[k]["ll"]) for k in ("hakodate", "matsushima")]
    # c318：教官が思っていた線（J11L と同じ向きで盛岡市役所の点を通る）
    mla, mlo = P["morioka"]["ll"]
    dlon = mlo - j11l(mla, P)
    n, s = span("G05", P)
    L["believed_g05"] = [r6((la, j11l(la, P) + dlon)) for la in seq(n, s)]
    # c408：西側 5海里の帯（J11L ↔ 西へ 9.26キロ）。北から南へ J11L、南から北へ西の縁
    n, s = span("G08", P, y0=70, y1=930)
    east = [(la, j11l(la, P)) for la in seq(n, s)]
    west = [off(la, lo, NM5, P) for la, lo in reversed(east)]
    L["band5_g08"] = [r6(p) for p in east + west]
    # c506：旅客機（J11L の西 約1.5キロに沿って南へ）・2機（旋回をくり返しながら南へ＝模式のジグザグ・J11L の西 約5〜8キロ）
    n, s = span("G08", P, y0=120, y1=900)
    L["air_g08"] = [r6(off(la, j11l(la, P), 1.5, P)) for la in (n, s)]
    zz = []
    for i, la in enumerate(seq(n, s, step=0.03)):
        km = 6.5 + 1.4 * math.sin(i * math.pi / 2.2)
        zz.append(r6(off(la, j11l(la, P), km, P)))
    L["two_g08"] = zz
    # c501：2機の進み方（松島から北上 → 盛岡市の西北で右旋回 → 南下）＝模式（ズーム8＝1キロ 約2画素＝見分けられる幅に広げた）。
    #   北上は J11L の西 最大 約22キロ・旋回は盛岡市の北西・南下は J11L の西 約8キロ（盛岡市の西方）
    up = []
    for la in seq(39.84, ms + 0.12, step=0.1)[::-1]:
        t = (la - ms) / (39.84 - ms)
        up.append(r6(off(la, j11l(la, P), 2 + 20 * min(1.0, t * 1.4), P)))
    turn = [r6(off(39.92, j11l(39.92, P), 20.0, P)), r6(off(39.95, j11l(39.95, P), 14.0, P)), r6(off(39.90, j11l(39.90, P), 8.5, P))]
    down = [r6(off(la, j11l(la, P), 8.0, P)) for la in (39.82, 39.70, 39.58)]
    # 段を分ける（語りの2行目＝北上・3行目＝右旋回と南下）。矢の先は各脚の最後の2点
    L["two_g09_up"] = [r6((ms, P["matsushima"]["ll"][1]))] + up
    L["two_g09_down"] = [up[-1]] + turn + down
    return L


def main():
    L = build()
    for k, v in L.items():
        print(f"{k}：{len(v)} 点・緯度 {min(p[0] for p in v):.3f}〜{max(p[0] for p in v):.3f}・経度 {min(p[1] for p in v):.3f}〜{max(p[1] for p in v):.3f}")
    if "--print" in sys.argv:
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(L, f, ensure_ascii=False, indent=0)
        f.write("\n")
    print("→", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
