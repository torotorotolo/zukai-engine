# -*- coding: utf-8 -*-
"""make_gsi17.py — 17本目 ⑤b-6：空港の地図（c727・c804・c812・c818）の地＝国土地理院の空中写真 A87（1987〜1990年撮影）を、
付図8（名古屋空港見取図＝p113）と同じ向き（滑走路を横・北を左）に**回して切り出した** 1920×1080 の絵にする。

■ なぜ回すか
  滑走路（約2.7km）は北北西〜南南東に延びる＝北を上にした 16:9 の額には、北門（滑走路の北の端の先）から事故の場所（南の端）までが入らない。
  付図8 も滑走路を横に描いている（北が左上）＝同じ向きにそろえ、地図に北の矢印を描く（`tools/satmap.py` の gsi の種類が自動で描く）。
  回す角度は「点が全部入り、回した窓が元の絵（4096×4096）からはみ出さない」範囲で、滑走路がいちばん横に近い角度を機械で探す（下の search）。

■ 位置の出どころ（`cuts/ss.GEO` に緯度経度で写す＝門番 check_sat）
  ・滑走路の両端（16 と 34 の末端の中心）＝空中写真の画素（末端の白い縞と番号の字の位置）
  ・事故の場所＝報告書 p6「滑走路34末端中心から東北東約110m」＝34 の末端から 110m・方位 67.5度（画素の大きさ＝緯度の地点の Web メルカトル）
  ・消防の待機所・北門＝付図8 の位置を、滑走路の両端で合わせた相似変換（拡大・回転・平行移動）で空中写真へ写した（付図8 は模式＝ずれは約40m。
    付図8 の涙形の折り返し〈p113 の北の端の東〉と写真の白い涙形で検算＝ずれ 38画素≒37m）
  ・誘導路 E4 の滑走路の側＝空中写真の画素（斜めの誘導路）／東の誘導路 EP1 の道すじ＝付図8 から写した（模式）

■ 使い方
    python ref/ep17/make_gsi17.py            → ref/ep17/gsi_ap17.jpg・gsi_ap17.json（元の絵は git の外＝ref/ep17/src/gsi/）
  出典の行＝「国土地理院撮影の空中写真（1987〜1990年撮影）を加工して作成」（回した・切り出した・縮めた＝加工）
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "src" / "gsi" / "gazo4_nagoya_z17.png"
META = HERE / "src" / "gsi" / "gazo4_nagoya_z17.json"
OUT = HERE / "gsi_ap17.jpg"
OUT_J = HERE / "gsi_ap17.json"
IW, IH = 1920, 1080
Z = 17

# 元の絵（4096×4096）の画素。how＝座標の出どころ
PTS = {
    "thr16": ((1321.0, 733.0), "空中写真の画素（滑走路16の末端の縞の中心）"),
    "thr34": ((2595.0, 3165.0), "空中写真の画素（滑走路34の末端の縞の中心）"),
    "loop": ((1755.0, 857.0), "空中写真の画素（北の端の東の涙形の折り返し＝付図8 との検算だけ）"),
    "e4rw": ((1702.0, 1460.0), "空中写真の画素（斜めの誘導路 E4 が滑走路に入る所）"),
    "e4tw": ((1880.0, 1370.0), "空中写真の画素（誘導路 E4 が東の誘導路に入る所）"),
}
# 付図8（4715×3350 の頁の画素）＝滑走路の両端で合わせて写す
FZ8 = {"thr16": (1056.0, 1814.0), "thr34": (4098.0, 1812.0), "loop": (1442.0, 1443.0),
       "station": (2095.0, 1385.0), "kitamon": (545.0, 1812.0),
       "ep1a": (3008.0, 1530.0), "ep1b": (3805.0, 1640.0)}
SITE_M, SITE_DEG = 110.0, 67.5            # 報告書 p6「滑走路34末端中心から東北東約110m」
MARGIN = 150.0                            # 点のまわりに残す元の画素（札の場所＝画面で約53画素。札は内側へ出す）


def gsi_meta():
    m = json.loads(META.read_text(encoding="utf-8"))
    return m["x_range"][0] * 256, m["y_range"][0] * 256


def wx(lon):
    return (lon + 180) / 360 * 256 * 2 ** Z


def wy(lat):
    p = math.radians(lat)
    return (1 - math.log(math.tan(p) + 1 / math.cos(p)) / math.pi) / 2 * 256 * 2 ** Z


def ll_of(px, py):
    ox, oy = gsi_meta()
    X, Y = px + ox, py + oy
    n = 256 * 2 ** Z
    lon = X / n * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * Y / n))))
    return lat, lon


def m_per_px(lat):
    return 156543.03392 * math.cos(math.radians(lat)) / 2 ** Z


def fz8_to_gsi(p):
    """付図8 の画素 → 元の絵の画素（滑走路の両端で合わせた相似変換）。"""
    (a0, b0), (a1, b1) = FZ8["thr16"], FZ8["thr34"]
    (p0x, p0y), (p1x, p1y) = PTS["thr16"][0], PTS["thr34"][0]
    zf = complex(a1 - a0, b1 - b0)
    zg = complex(p1x - p0x, p1y - p0y)
    k = zg / zf
    z = (complex(p[0] - a0, p[1] - b0)) * k + complex(p0x, p0y)
    return z.real, z.imag


def all_pts():
    P = {k: v[0] for k, v in PTS.items()}
    lat, _ = ll_of(*P["thr34"])
    r = SITE_M / m_per_px(lat)
    a = math.radians(SITE_DEG)
    P["site"] = (P["thr34"][0] + r * math.sin(a), P["thr34"][1] - r * math.cos(a))
    for k in ("station", "kitamon", "ep1a", "ep1b"):
        P[k] = fz8_to_gsi(FZ8[k])
    P["loop_fz8"] = fz8_to_gsi(FZ8["loop"])
    return P


def rot(phi):
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    return c, s


def to_img(p, g):
    """元の絵の画素 → 切り出した絵の画素（g＝cx・cy・phi・s）。左回り（見た目）に phi 度回す。"""
    c, s = rot(g["phi"])
    x, y = p[0] - g["cx"], p[1] - g["cy"]
    return IW / 2 + g["s"] * (x * c + y * s), IH / 2 + g["s"] * (-x * s + y * c)


def search(P):
    """点が全部入り、窓の4隅が元の絵の内側に収まる中で、いちばん大きく写す（s 最大）角度と中心を探す（角度は2度刻み）。
    ⚠️ 滑走路を真横（62度）にすると、窓が元の絵の上の端（北の端は絵の上に近い）からはみ出す＝36度あたりが最大（滑走路は額の中で約26度の斜め）。"""
    keep = [P[k] for k in ("thr16", "thr34", "site", "station", "kitamon")]
    best = None
    for phi in range(20, 66, 2):
        c, s = rot(phi)
        xs = [p[0] * c + p[1] * s for p in keep]
        ys = [-p[0] * s + p[1] * c for p in keep]
        w0 = max(max(xs) - min(xs) + 2 * MARGIN, (max(ys) - min(ys) + 2 * MARGIN) * IW / IH)
        for grow in [1.0 + 0.01 * i for i in range(40)]:
            W = w0 * grow
            H = W * IH / IW
            ok = None
            # 窓の中心（回した座標）を、点の箱＋余白が窓に収まる範囲で動かす
            for tx in range(0, int(W - (max(xs) - min(xs) + 2 * MARGIN)) + 1, 10):
                ux = min(xs) - MARGIN + W / 2 - tx
                for ty in range(0, int(H - (max(ys) - min(ys) + 2 * MARGIN)) + 1, 10):
                    uy = min(ys) - MARGIN + H / 2 - ty
                    corners = [(ux + sx * W / 2, uy + sy * H / 2) for sx in (-1, 1) for sy in (-1, 1)]
                    src = [(a * c - b * s, a * s + b * c) for a, b in corners]
                    if all(1 <= x <= 4094 and 1 <= y <= 4094 for x, y in src):
                        ok = (ux * c - uy * s, ux * s + uy * c)
                        break
                if ok:
                    break
            if ok:
                if best is None or IW / W > best[0]:
                    best = (IW / W, phi, ok)
                break
    s_, phi, (cx, cy) = best
    return dict(phi=phi, s=round(s_, 5), cx=round(cx, 2), cy=round(cy, 2))


def render(g):
    im = Image.open(SRC).convert("RGB")
    half = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)   # 先に半分へ（縮める bicubic の折り返しを避ける）
    c, s = rot(g["phi"])
    k = g["s"] * 2.0                                                  # 半分の絵の1画素 → 切り出した絵の画素
    cx, cy = g["cx"] / 2, g["cy"] / 2
    # 出力 (X, Y) → 半分の絵の画素：cx + (1/k)·Rot⁻¹((X, Y) − 中心)
    a, b = c / k, -s / k
    d, e = s / k, c / k
    data = (a, b, cx - a * IW / 2 - b * IH / 2, d, e, cy - d * IW / 2 - e * IH / 2)
    out = half.transform((IW, IH), Image.AFFINE, data, resample=Image.BICUBIC)
    out.save(OUT, quality=90)


def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def main():
    P = all_pts()
    lp = P["loop_fz8"]
    print(f"検算：付図8 の涙形 → {lp[0]:.0f},{lp[1]:.0f}（写真 {PTS['loop'][0][0]:.0f},{PTS['loop'][0][1]:.0f}）"
          f" ずれ {math.dist(lp, PTS['loop'][0]):.0f}画素")
    g = search(P)
    render(g)
    lat_c, _ = ll_of(g["cx"], g["cy"])
    ox, oy = gsi_meta()
    meta = dict(src="ref/ep17/src/gsi/gazo4_nagoya_z17.png", src_md5=md5(SRC), out="ref/ep17/gsi_ap17.jpg", out_md5=md5(OUT),
                z=Z, org=(ox, oy), phi=g["phi"], s=g["s"], c=(g["cx"], g["cy"]), size=(IW, IH),
                m_per_px=round(m_per_px(lat_c) / g["s"], 4),
                credit="国土地理院撮影の空中写真（1987〜1990年撮影）を加工して作成",
                pts={k: dict(gsi=(round(v[0], 1), round(v[1], 1)), ll=tuple(round(t, 6) for t in ll_of(*v)),
                             img=tuple(round(t, 1) for t in to_img(v, g))) for k, v in P.items()})
    OUT_J.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in meta.items() if k != "pts"}, ensure_ascii=False))
    for k, v in meta["pts"].items():
        print(f"  {k:9s} ll={v['ll']}  img={v['img']}")


if __name__ == "__main__":
    main()
