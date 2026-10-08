# -*- coding: utf-8 -*-
"""route20.py — 20本目 ⑤b-3：再現イラスト S2（上から見た経路の地図）の**経路と時刻の点**を、報告書の付図-1（JA8119 飛行経路略図・
印刷 p.137＝`ref/ja123/f001.jpg`）から読んで、緯度・経度にする。

■ なぜ（台本 第2版 c209 の画の欄「18:24:35 の点＝付図-1 の時刻と高度」・ルール §5b-74①＝描く物は1つずつ出典）
  付図-1 は手で引いた略図（縮尺・方位の目盛りが無い）。海岸線の形は目安だが、経路と海岸の位置の関係（伊豆半島の東の海岸の上・駿河湾・
  焼津の北・大月の上で1回転・奥多摩・三国山）は図のとおりに描きたい＝**図の海岸線を Natural Earth の海岸線に重ねる式**（アフィン変換＝
  縦横の伸び・回り・ずれ）を機械で求め、その式で経路と時刻の点を緯度・経度に直す。

■ やり方（`python ref/ep20/route20.py fit|trace|check <f001.jpg>`）
  fit   … Natural Earth の海岸線（`coast_ne10m.json`）を 0.5km おきの点にし、図の黒い画素までの距離（距離の変換）の和が小さくなる
          アフィン変換を探す（遠すぎる点は 12画素で頭打ち＝図に描いていない海岸・字に引かれない）。始めの値は羽田・熱海・焼津の目読み
  trace … 下の WAYPOINTS（目で読んだ経路の通り道＝図の画素）の隣どうしを、図の黒い画素を安く通る最短の道（ダイクストラ法）で
          つなぐ＝描いた線に吸い付く。海岸線と交わる所は通り道を細かく置いた
  check … 経路（赤）・Natural Earth の海岸線（青）・時刻の点（緑）を図に重ねた絵（目で照らす）
  → `ref/ep20/route20.json`（経路の緯度・経度の折れ線・時刻の点＝時刻・高度・速さ・緯度・経度・図の画素・式と残差）

■ 時刻の点（TICKS）＝付図-1 の札の字（時刻・高度・速さ）をそのまま。点の位置は札の引き出し線が経路に触れる所（目読み→経路の上の一番近い点）
  🔴 墜落の時刻（付図-1 の「18:56'30」）は資料で割れる（2.1 p.8「18時56分ごろ」＝台本 c421 の言い方）＝点は持つが札に時刻を出さない
     （`ss.ILLU_SPLIT_TIMES`）
"""
from __future__ import annotations

import heapq
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COAST = HERE / "coast_ne10m.json"
OUT = HERE / "route20.json"

LAT0, LON0 = 35.4, 139.0             # 平らにする基準（正距円筒＝km）
KX = math.cos(math.radians(LAT0)) * 111.32
KY = 110.57


def to_km(lon, lat):
    return ((lon - LON0) * KX, (lat - LAT0) * KY)


def to_ll(x, y):
    return (LON0 + x / KX, LAT0 + y / KY)


# 始めの値（図の画素 ← 緯度経度）＝目読みの3点。fit がこれから詰める
SEED = [((886.0, 240.0), (139.780, 35.549)),    # 東京国際空港（羽田）の点
        ((633.7, 444.9), (139.072, 35.096)),    # 熱海の点
        ((352.0, 548.0), (138.324, 34.867))]    # 焼津の点

# 目で読んだ経路の通り道（図の画素・付図-1 の 1200×780）。羽田の離陸 → 南 → 南西 → 伊豆 → 駿河湾 → 焼津の北 → 北 → 東 → 大月の1回転 →
#   東 → 北 → 北西 → 三国山 → 墜落。隣どうしは trace が黒い画素に沿ってつなぐ
#   読み方（2026-10-08）＝海岸線の近くを薄くし 25画素の目盛りを引いた拡大（北半分・南半分の2枚）を目で読んだ
WAYPOINTS = [
    (879, 232), (881, 273), (884, 320), (888, 380), (892, 425), (890, 447), (873, 457), (830, 488), (780.3, 521.1),
    (720, 550), (662.6, 577.1), (639.7, 588.6), (607.1, 604), (590, 612), (581.4, 616), (558.6, 608.6), (535.7, 594.3),
    (516.9, 580), (495.7, 569.7), (472.9, 566.9), (444.3, 567.4), (415.7, 557.1), (387, 548.6), (355.7, 536),
    (341.4, 528.6), (336, 512), (335.7, 491.4), (334.6, 460), (334.6, 434.3), (338.6, 388.6), (347.1, 362.9),
    (358.6, 348.6), (374.3, 340), (400, 334), (431.4, 328.6), (460, 318), (491.4, 301.1), (506, 294), (522.9, 268.6),
    (540, 240), (552.6, 216),
    # 大月の上の右へほぼ1回転（2.1 p.7＝右回り＝上から見て時計回り）
    (568.6, 210.3), (591.4, 208.6), (604.6, 218.9), (605.7, 231.4), (597.1, 248.6), (582.9, 257.1), (568.6, 255.4),
    (558.3, 242.9), (556, 225.7), (558.3, 211.4), (562.9, 198.9),
    (580, 193.1), (602.9, 189.7), (618.9, 190.3), (637.1, 188.6), (651.4, 182.9), (658.9, 168.6), (661.1, 154.3),
    (658.3, 142.9), (654.3, 137.1), (642.9, 120), (625.7, 108.6), (602.9, 104.6), (586.9, 104), (562.9, 102.9),
    (542.9, 98.3), (527.4, 91.4), (514.3, 80), (504.6, 64), (494.3, 54.3), (480, 46.9),
    # 扇平山・三国山のまわりの小さな輪（図の線は細かくて形を決めきれない＝墜落地点は 2.1 p.8 の緯度経度で置く＝CRASH）
    (478.3, 37.1), (485.7, 32.6), (493.1, 35.4), (491.4, 42.9)]

# 時刻の点＝(付図-1 の札の字, 時刻, 高度 ft, 速さ kt, 引き出し線が経路に触れる所の目読み〈図の画素〉)
TICKS = [
    ("18:13'55", "18:13:55", 3200, 170, (881, 273)),
    ("18:18'30", "18:18:30", 12200, 290, (892.9, 425.7)),
    ("18:21'36", "18:21:36", 18900, 300, (780.3, 521.1)),
    ("18:24'12", "18:24:12", 23400, 300, (662.6, 577.1)),
    ("18:24'35", "18:24:35", 23900, 300, (639.7, 588.6)),      # ◎＝異常事態発生推定位置
    ("18:25'18", "18:25:18", 23900, 310, (607.1, 604)),
    ("18:27'07", "18:27:07", 24400, 280, (516.9, 580)),
    ("18:28'36", "18:28:36", 22100, 280, (444.3, 567.4)),
    ("18:31'08", "18:31:08", 24900, 250, (341.4, 528.6)),
    ("18:34'53", "18:34:53", 21400, 270, (358.6, 348.6)),
    ("18:38'06", "18:38:06", 22400, 260, (491.4, 301.1)),
    ("18:40'30", "18:40:30", 22400, 220, (552.6, 216)),
    ("18:41'59", "18:41:59", 20900, 240, (605.7, 231.4)),
    ("18:43'05", "18:43:05", 18600, 240, (568.6, 255.4)),
    ("18:44'09", "18:44:09", 17000, 240, (564.6, 197.1)),
    ("18:45'48", "18:45:48", 13500, 220, (618.9, 190.3)),
    ("18:47'17", "18:47:17", 9000, 230, (662.9, 162.9)),
    ("18:48'03", "18:48:03", 6800, 230, (654.3, 137.1)),
    ("18:51'03", "18:51:03", 9600, 190, (586.9, 104)),
    ("18:53'03", "18:53:03", 13400, 180, (527.4, 91.4)),
    ("18:54'23", "18:54:23", 11000, 220, (504.6, 64)),
    ("18:55'03", "18:55:03", 11300, 180, (480, 46.9)),
    ("18:56'03", "18:56:03", 8400, 260, (493.1, 35.4))]

# 墜落地点＝報告書 2.1 p.8「北緯35度59分54秒、東経138度41分49秒」（付図-1 の ◎ の時刻 18:56'30 は資料で割れる＝札に出さない）
CRASH = (138 + 41 / 60 + 49 / 3600, 35 + 59 / 60 + 54 / 3600)


def _load_img(p):
    import numpy as np
    from PIL import Image
    return np.asarray(Image.open(p).convert("L"), dtype=np.float32)


FIT_BBOX = (137.6, 34.3, 140.6, 36.6)  # 重ねに使う海岸の範囲（付図-1 に描いてある範囲より一回り広く＝切り出しの範囲を広げても式が変わらない）


def _coast_pts(step_km=0.5):
    d = json.loads(COAST.read_text(encoding="utf-8"))
    bx0, by0, bx1, by1 = d["bbox"]
    pts = []
    for poly in d["polys"]:
        ring = poly + [poly[0]]
        for (a, b), (c, e) in zip(ring, ring[1:]):
            if not (FIT_BBOX[0] <= a <= FIT_BBOX[2] and FIT_BBOX[1] <= b <= FIT_BBOX[3]):
                continue
            # 切り出しの枠の辺（海岸ではない）は捨てる
            if (abs(a - c) < 1e-9 and min(abs(a - bx0), abs(a - bx1)) < 1e-6) or \
               (abs(b - e) < 1e-9 and min(abs(b - by0), abs(b - by1)) < 1e-6):
                continue
            p, q = to_km(a, b), to_km(c, e)
            n = max(1, int(math.hypot(q[0] - p[0], q[1] - p[1]) / step_km))
            for k in range(n):
                t = k / n
                pts.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return pts


def _affine_from(pairs):
    """図の画素 (u, v) ＝ A·(x, y, 1)（x, y＝km）。最小二乗"""
    import numpy as np
    X = np.array([[*to_km(*ll), 1.0] for _uv, ll in pairs])
    U = np.array([uv for uv, _ll in pairs])
    A, *_ = np.linalg.lstsq(X, U, rcond=None)
    return A.T                          # 2×3


def fit(img_path):
    import numpy as np
    from scipy import ndimage, optimize
    im = _load_img(img_path)
    dark = im < 140
    dt = ndimage.distance_transform_edt(~dark)
    pts = np.array(_coast_pts())
    X = np.c_[pts, np.ones(len(pts))]
    h, w = im.shape
    CAP = 12.0

    def cost(a):
        A = a.reshape(2, 3)
        uv = X @ A.T
        ok = (uv[:, 0] >= 0) & (uv[:, 0] < w - 1) & (uv[:, 1] >= 0) & (uv[:, 1] < h - 1)
        d = ndimage.map_coordinates(dt, [uv[ok, 1], uv[ok, 0]], order=1)
        return float(np.minimum(d, CAP).sum() + CAP * (~ok).sum())
    a0 = _affine_from(SEED).ravel()
    best = optimize.minimize(cost, a0, method="Powell", options=dict(maxiter=20000, xtol=1e-4, ftol=1e-6))
    A = best.x.reshape(2, 3)
    uv = X @ A.T
    ok = (uv[:, 0] >= 0) & (uv[:, 0] < w - 1) & (uv[:, 1] >= 0) & (uv[:, 1] < h - 1)
    d = ndimage.map_coordinates(dt, [uv[ok, 1], uv[ok, 0]], order=1)
    near = d[d < CAP]
    stats = dict(n=int(ok.sum()), near=int(len(near)), med=round(float(np.median(near)), 2),
                 p90=round(float(np.percentile(near, 90)), 2), cost0=round(cost(a0), 1), cost=round(best.fun, 1))
    return A, stats


def trace(img_path, A):
    """WAYPOINTS を黒い画素に沿ってつなぐ（コスト＝白いほど高い・8近傍）。返り値＝図の画素の折れ線"""
    import numpy as np
    im = _load_img(img_path)
    h, w = im.shape
    c = 1.0 + 40.0 * (im / 255.0) ** 2

    def path(a, b):
        (ax, ay), (bx, by) = (int(round(a[0])), int(round(a[1]))), (int(round(b[0])), int(round(b[1])))
        pad = 25
        x0, x1 = max(0, min(ax, bx) - pad), min(w - 1, max(ax, bx) + pad)
        y0, y1 = max(0, min(ay, by) - pad), min(h - 1, max(ay, by) + pad)
        dist = {(ax, ay): 0.0}
        prev = {}
        pq = [(0.0, ax, ay)]
        while pq:
            dd, x, y = heapq.heappop(pq)
            if (x, y) == (bx, by):
                break
            if dd > dist.get((x, y), 1e18):
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if not dx and not dy:
                        continue
                    nx, ny = x + dx, y + dy
                    if not (x0 <= nx <= x1 and y0 <= ny <= y1):
                        continue
                    nd = dd + c[ny, nx] * (1.4142 if dx and dy else 1.0)
                    if nd < dist.get((nx, ny), 1e18):
                        dist[(nx, ny)] = nd
                        prev[(nx, ny)] = (x, y)
                        heapq.heappush(pq, (nd, nx, ny))
        out = [(bx, by)]
        while out[-1] != (ax, ay):
            out.append(prev[out[-1]])
        return out[::-1]
    def snap(p, r=6):
        """⑤b-3：目読みの通り道が線から数画素ずれていると、最短の道がそこへ寄り道して「とげ」になった＝先に一番近い黒い画素へ寄せる"""
        x, y = int(round(p[0])), int(round(p[1]))
        best = None
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and im[ny, nx] < 120:
                    d = dx * dx + dy * dy
                    if best is None or d < best[0]:
                        best = (d, (nx, ny))
        return best[1] if best else (x, y)
    wps = [snap(p) for p in WAYPOINTS]
    pl = [wps[0]]
    for a, b in zip(wps, wps[1:]):
        pl += path(a, b)[1:]
    return pl


def inv(A, u, v):
    import numpy as np
    M = np.array([[A[0][0], A[0][1]], [A[1][0], A[1][1]]])
    x, y = np.linalg.solve(M, [u - A[0][2], v - A[1][2]])
    return to_ll(float(x), float(y))


def _simplify(pl, tol=1.0, win=7):
    """⑤b-3 の重ね絵：図の線の上の向きの矢じり（小さな「く」の字）に吸い付いた 3〜5画素のとげが残った＝移動平均（前後 win 画素）で
    ならしてから間引く（両端は動かさない）"""
    sys.path.insert(0, str(HERE.parent / "ep18"))
    from make_coast import simplify
    n, h = len(pl), win // 2
    sm = [pl[0]] + [(sum(p[0] for p in pl[max(0, i - h):i + h + 1]) / len(pl[max(0, i - h):i + h + 1]),
                     sum(p[1] for p in pl[max(0, i - h):i + h + 1]) / len(pl[max(0, i - h):i + h + 1]))
                    for i in range(1, n - 1)] + [pl[-1]]
    return simplify([(float(x), float(y)) for x, y in sm], tol)


def build(img_path):
    A, st = fit(img_path)
    pl = trace(img_path, A)
    sm = _simplify(pl)

    def nearest(u, v):
        k = min(range(len(pl)), key=lambda i: (pl[i][0] - u) ** 2 + (pl[i][1] - v) ** 2)
        return k, pl[k]
    ticks = []
    for lab, t, ft, kt, (u, v) in TICKS:
        k, (pu, pv) = nearest(u, v)
        lon, lat = inv(A, pu, pv)
        ticks.append(dict(label=lab, t=t, ft=ft, kt=kt, uv=[pu, pv], snap=round(math.hypot(pu - u, pv - v), 1), k=k,
                          lon=round(lon, 4), lat=round(lat, 4)))
    route = [[round(c, 4) for c in inv(A, u, v)] for u, v in sm]
    cx, cy = to_km(*CRASH)
    crash_uv = [A[0][0] * cx + A[0][1] * cy + A[0][2], A[1][0] * cx + A[1][1] * cy + A[1][2]]
    out = dict(crash=dict(lon=round(CRASH[0], 4), lat=round(CRASH[1], 4), uv=[round(float(c), 1) for c in crash_uv],
                          rec="報告書 2.1 p.8（北緯35度59分54秒、東経138度41分49秒）"),source="報告書 付図-1 JA8119飛行経路略図（印刷 p.137＝ref/ja123/f001.jpg・1200×780）", affine=[list(map(float, r)) for r in A],
               fit=st, proj=dict(lat0=LAT0, lon0=LON0), route=route, route_uv=[[float(u), float(v)] for u, v in sm], ticks=ticks,
               note="経路と時刻の点は付図-1 の略図から読んだ目安（図の海岸線を Natural Earth の海岸線に重ねた式で緯度・経度に直した）")
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out, pl


def check(img_path, out_png):
    from PIL import Image, ImageDraw
    out, pl = build(img_path)
    A = out["affine"]
    im = Image.open(img_path).convert("RGB")
    dr = ImageDraw.Draw(im)
    d = json.loads(COAST.read_text(encoding="utf-8"))
    for poly in d["polys"]:
        uv = []
        for lon, lat in poly + [poly[0]]:
            x, y = to_km(lon, lat)
            uv.append((A[0][0] * x + A[0][1] * y + A[0][2], A[1][0] * x + A[1][1] * y + A[1][2]))
        dr.line(uv, fill=(40, 90, 255), width=1)
    dr.line([tuple(p) for p in pl], fill=(230, 20, 20), width=1)
    for tk in out["ticks"]:
        u, v = tk["uv"]
        dr.ellipse([u - 4, v - 4, u + 4, v + 4], outline=(0, 170, 0), width=2)
    u, v = out["crash"]["uv"]
    dr.ellipse([u - 5, v - 5, u + 5, v + 5], outline=(220, 0, 220), width=2)
    x0, y0, x1, y1, sc = 250, 0, 950, 650, 1.6
    im = im.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * sc), int((y1 - y0) * sc)), Image.LANCZOS)
    im.save(out_png)
    print(json.dumps(out["fit"], ensure_ascii=False))
    for tk in out["ticks"]:
        print(tk["label"], tk["t"], tk["uv"], "snap", tk["snap"], tk["lon"], tk["lat"])


if __name__ == "__main__":
    cmd, img = sys.argv[1], sys.argv[2]
    if cmd == "fit":
        A, st = fit(img)
        print(st)
        print(A)
    elif cmd == "check":
        check(img, sys.argv[3])
