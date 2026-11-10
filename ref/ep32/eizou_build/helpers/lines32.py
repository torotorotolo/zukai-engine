# -*- coding: utf-8 -*-
"""32本目 ⑤b-3b：地図の描き足しの線と矢印（`ref/ep32/sat_lines32.json`＝`tools/cuts/ss.SAT_LINES`）を作る。標準ライブラリだけ。

  python -P ref/ep32/eizou_build/helpers/lines32.py          # json を書く（点は ss.GEO・画は gshot32.GMAP・レーダーは git の外の表）
  python -P ref/ep32/eizou_build/helpers/lines32.py --print  # 書かずに、線ごとの点の数と画素の範囲を出す

■ 出どころ
  ・飛んだ道＝NTSB のドケット #85（機体の動きの研究）p22 の EWR ASR のレーダーの表 55点（15:25:59.69〜15:30:27.17・緯度経度）
    ＝git の外 `ref/ep32/src/sat/radar85_p22.tsv`（取り出し `ref/ep32/src/sat/radar32b.py`）＋着水した所（ドケット #6 §4.0＝ss.GEO の ditch）。
    鳥とぶつかった所（#6）は 15:27:08.78 と 15:27:13.43 の点のあいだに入る（15:27:11）＝線に入れて折る。
    🔴 最初の点は 15:25:59.69（高さ 1,000フィート・滑走路22 の端の北北東 約0.9キロ）＝地上の滑走は描かない（記録が無い）
  ・矢印（向きの模式＝長さに意味は無い）：
      管制の「220度」（付録B p189 の 15:27:42）・「280度」（p195 の 15:29:21）＝その時刻の機体の位置（レーダーの点のあいだを時刻で割った位置）から。
      🔴 管制の向きは磁方位＝地図（真北が上）には FAA の資料の磁気の偏差 12度西（NASR の APT_BASE の MAG_VARN＝LGA・TEB とも 12W）を引いた向きで描く
      滑走路へ降りる向き・離陸の向き＝FAA の滑走路の端の座標と真方位（NASR 2026-10-29 の APT_RWY_END＝TRUE_ALIGNMENT）
  各画の線は**額の内側で切る**（門番 check_sat が線の外接の箱を額の内側・Google の部品の箱の外で測る）＝撮った絵の x 40〜1880・y 50〜960 の内
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
import gshot32 as G  # noqa: E402

OUT = os.path.join(REPO, "ref", "ep32", "sat_lines32.json")
RADAR = os.path.join(REPO, "ref", "ep32", "src", "sat", "radar85_p22.tsv")
MAGVAR_W = 12.0                     # FAA NASR（2026-10-29）の APT_BASE：LGA・TEB の MAG_VARN＝12 W
RECT = (40, 50, 1880, 960)          # 線を置く撮った絵の範囲（左上の「マップで開く」・下のロゴ y≥1000・左下の小窓 y≥985 の手前）
T_BIRD = 15 * 3600 + 27 * 60 + 11   # 鳥とぶつかった時刻（報告書・FDR）
T_DITCH = 15 * 3600 + 30 * 60 + 43  # 着水の時刻（報告書）


def geo():
    import cuts.ss as ss
    return ss.GEO


def sec(hms):
    h, m, s = hms.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def radar():
    out = []
    for ln in open(RADAR, encoding="utf-8"):
        if not ln.strip():
            continue
        t, alt, la, lo = ln.rstrip("\n").split("\t")
        out.append((sec(t), float(la), float(lo)))
    if len(out) != 55:
        raise SystemExit(f"🔴 レーダーの点が {len(out)}（55 のはず）")
    return out


def track(P):
    """時刻つきの道＝レーダー55点＋鳥とぶつかった所（15:27:11）＋着水した所（15:30:43）。"""
    pts = radar()
    pts.append((T_BIRD,) + tuple(P["bird"]["ll"]))
    pts.append((T_DITCH,) + tuple(P["ditch"]["ll"]))
    return sorted(pts)


def at(tr, t):
    """時刻 t の位置（前後の点を時刻で割る）。"""
    for (t0, a0, b0), (t1, a1, b1) in zip(tr, tr[1:]):
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            return (a0 + f * (a1 - a0), b0 + f * (b1 - b0))
    raise ValueError(t)


def part(tr, t0=None, t1=None):
    """時刻 t0〜t1 の道（端はその時刻の位置）。"""
    t0 = tr[0][0] if t0 is None else t0
    t1 = tr[-1][0] if t1 is None else t1
    mid = [(a, b) for t, a, b in tr if t0 < t < t1]
    return [at(tr, t0)] + mid + [at(tr, t1)]


def dest(ll, brg, km):
    """ll から真方位 brg 度へ km 進んだ点（球）。"""
    R = 6371.0088
    la1, lo1 = map(math.radians, ll)
    b = math.radians(brg)
    d = km / R
    la2 = math.asin(math.sin(la1) * math.cos(d) + math.cos(la1) * math.sin(d) * math.cos(b))
    lo2 = lo1 + math.atan2(math.sin(b) * math.sin(d) * math.cos(la1), math.cos(d) - math.sin(la1) * math.sin(la2))
    return (math.degrees(la2), math.degrees(lo2))


def pxy(code, ll):
    r = G.GMAP[code]
    return G.px(ll[0], ll[1], *r["ll"], r["z"])


def clip(code, pts, rect=RECT):
    """撮った絵の rect の内にある、いちばん長いひと続きの部分（縁で切れる所は縁の上の点を足す）。"""
    x0, y0, x1, y1 = rect

    def inside(p):
        x, y = pxy(code, p)
        return x0 <= x <= x1 and y0 <= y <= y1

    def cross(a, b):
        # a（内）と b（外）のあいだで縁に当たる所（20回の二分）
        lo, hi = 0.0, 1.0
        for _ in range(20):
            m = (lo + hi) / 2
            q = (a[0] + m * (b[0] - a[0]), a[1] + m * (b[1] - a[1]))
            lo, hi = (m, hi) if inside(q) else (lo, m)
        return (a[0] + lo * (b[0] - a[0]), a[1] + lo * (b[1] - a[1]))

    runs, cur = [], []
    for i, p in enumerate(pts):
        if inside(p):
            if not cur and i > 0:
                cur.append(cross(p, pts[i - 1]))
            cur.append(p)
        elif cur:
            cur.append(cross(pts[i - 1], p))
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    if not runs:
        raise SystemExit(f"🔴 {code}：線が額の内に入らない")
    return max(runs, key=len)


def r6(p):
    return (round(p[0], 6), round(p[1], 6))


def build():
    P = geo()
    tr = track(P)
    L = {}
    ll = {k: tuple(P[k]["ll"]) for k in ("lga04", "lga22", "lga13", "lga31", "teb01", "bird", "ditch", "top")}
    t_top = sec("15:27:30")
    # G01：全体（c109）
    L["path_g01"] = clip("G01", part(tr))
    # G04：最初の点から鳥とぶつかった所まで（c303）・滑走路13 の手前で届かない矢印（c509＝向き＝滑走路13 の真方位 122度の延長の上から）
    L["path_g04"] = clip("G04", part(tr, None, T_BIRD))
    L["arr13_g04"] = [dest(ll["lga13"], 302.0, 2.6), ll["lga13"]]
    # G05：鳥とぶつかった所 → いちばん高い所（c317 の段1）・その先の左への曲がり（c317 の段2＝15:28:31 まで）・15:27:42 まで（c401）・220度の矢印（c401）
    L["path_g05_up"] = clip("G05", part(tr, T_BIRD, t_top))
    L["path_g05_down"] = clip("G05", part(tr, t_top, sec("15:28:31")))
    L["path_g05_to2742"] = clip("G05", part(tr, T_BIRD, sec("15:27:42")))
    p2742 = at(tr, sec("15:27:42"))
    L["arr220_g05"] = [p2742, dest(p2742, 220.0 - MAGVAR_W, 3.2)]
    # G06：15:28:46 まで（c409）・15:29:21 から先（c415 の段3）・280度の矢印（c415）・滑走路1 へ降りる向き（c415＝真方位 3度＝南から）
    L["path_g06_to2846"] = clip("G06", part(tr, None, sec("15:28:46")))
    L["path_g06_from2921"] = clip("G06", part(tr, sec("15:29:21"), None))
    p2921 = at(tr, sec("15:29:21"))
    L["arr280_g06"] = [p2921, dest(p2921, 280.0 - MAGVAR_W, 4.6)]
    L["arr01_g06"] = [dest(ll["teb01"], 183.0, 2.4), ll["teb01"]]
    # G07：川の上で南へ（c421・c512）
    L["path_g07"] = clip("G07", part(tr))
    # G03：滑走路31 へ降りる向き（真方位 302度＝南東から）・滑走路4 へ降りる向き（真方位 32度＝南西から）（c406）
    L["arr31_g03"] = [dest(ll["lga31"], 122.0, 1.5), ll["lga31"]]
    L["arr04_g03"] = [dest(ll["lga04"], 212.0, 1.5), ll["lga04"]]
    return {k: [r6(p) for p in v] for k, v in L.items()}


def main():
    L = build()
    for k, v in L.items():
        code = "G" + k.rsplit("_g", 1)[1][:2]
        xs, ys = zip(*(pxy(code, p) for p in v))
        print(f"{k}：{len(v)} 点・画素 x {min(xs):.0f}〜{max(xs):.0f}・y {min(ys):.0f}〜{max(ys):.0f}")
    if "--print" in sys.argv:
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(L, f, ensure_ascii=False, indent=0)
        f.write("\n")
    print("→", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
