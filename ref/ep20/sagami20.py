# -*- coding: utf-8 -*-
"""sagami20.py — 20本目 ⑤b-4：再現イラスト S7（相模湾の地図・上から）の点と線を、報告書の付図-20（相模湾等の浮遊残骸揚収場所図・
印刷 p.156＝`ref/ja123/f020.jpg`）・付図-21（相模湾海底調査区域・p.157＝`f021.jpg`）と、解説の図15（相模湾及び駿河湾における海流概況と
日航機揚収物件の推定落下区域・解説 p.22＝`ref/ep20/src/jtsb_kaisetsu.pdf`）から読んで、緯度・経度にする。

■ なぜ（台本 第2版 cb02「調査区域の枠・浮遊残骸の揚収場所の点＝付図-20・21 から」・cb03「海の流れの矢印・推定落下区域」・
  cb07「17か所の点」・ルール §5b-74①＝描く物は1つずつ出典）
  ・付図-21 は緯度・経度の目盛り（1分おき）がある＝目盛りの線の画素から式を作り、調査区域の枠・17か所の点・推定飛行経路（244度）・
    推定異常音発生点・海岸線を読む。海岸線は図の線をたどる（Natural Earth 1:10m はこの範囲に頂点が10しか無い＝0.4km ずれる）
  ・付図-20 は目盛りが無い略図＝route20.py と同じく、図の海岸線を Natural Earth の海岸線（`coast_ne10m.json`）に重ねる式
    （アフィン変換）を機械で求め、揚収場所の点 1〜28 を緯度・経度にする
  ・図15 は 30分おきの経緯線がある＝線の画素から式を作り、推定落下区域（赤い楕円）と海流の矢印（青）を読む（形は目安）

■ やり方（`python ref/ep20/sagami20.py build|check`）
  build … 3つの図を読み → `ref/ep20/sagami20.json`
  check … 読んだ点と線を図に重ねた絵（目で照らす）→ 引数の png
  🔴 点の画素は図の丸（ハフ変換）・枠は辺ごとに黒い画素へ直線を当てて交点（⑤b-4 で測った値をここに書いた＝下の定数）。
     読み直すときは `measure` で同じ測り方を回す
"""
from __future__ import annotations

import heapq
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / "sagami20.json"
F20 = ROOT / "ref" / "ja123" / "f020.jpg"
F21 = ROOT / "ref" / "ja123" / "f021.jpg"
KAI = HERE / "src" / "jtsb_kaisetsu.pdf"
KAI_PAGE, KAI_DPI = 25, 250           # 解説 p.22（PDF の 26 枚目）・図15 の切り出しの解像度

# ══ 付図-21（1200×982）＝目盛りの線（⑤b-4 に画素の列・行の黒の数で測った）══
F21_V = [75.5, 198.0, 321.4, 444.5, 567.5, 691.5, 813.4, 937.0, 1060.0, 1182.6]      # 東経139度00分〜09分
F21_H = [(12.5, 49), (163.8, 48), (310.2, 47), (458.0, 46), (604.0, 45), (751.5, 44)]  # 北緯34度49分〜44分（いちばん下の線は枠と重なる＝使わない）
# えい航式深海カメラによる調査地点 ①〜⑰（図の丸の中心＝ハフ変換・目読みとの差は 0.7〜3.5画素）
F21_PTS = {1: (311.5, 780.5), 2: (333.5, 723.5), 3: (460.5, 674.5), 4: (469.5, 652.5), 5: (408.5, 645.5), 6: (422.5, 578.5),
           7: (413.5, 565.5), 8: (620.5, 239.5), 9: (619.5, 369.5), 10: (614.5, 518.5), 11: (612.5, 482.5), 12: (533.5, 700.5),
           13: (428.5, 699.5), 14: (467.5, 719.5), 15: (549.5, 730.5), 16: (531.5, 718.5), 17: (603.5, 471.5)}
# 調査区域の枠（8つの角＝辺ごとに黒い画素へ当てた直線の交点。辺の残差の中央値 0.4〜0.7画素）
F21_AREA = [(159.4, 662.5), (549.7, 467.5), (611.1, 235.6), (813.5, 60.5), (813.5, 393.9), (856.4, 493.2), (849.2, 581.7),
            (265.3, 873.9)]
# 推定飛行経路（レーダ航跡・図の字「244度」）＝黒い画素へ当てた直線（1,470画素・残差の中央値 0.56）。向きは東北東 → 西南西
F21_FLIGHT = dict(c=(621.4, 595.8), d=(-0.8958, 0.4445), x0=1180.0, x1=78.0)
F21_BOOM = (810.8, 499.5)              # 推定異常音発生点（小さな丸・半径約4画素＝経路の線から 2.1画素）

# ══ 付図-20（2480×1605）＝目盛りの無い略図。揚収場所の点 1〜28 の目読み（表示 2000 幅で読んだ値×1.24）══
F20_EST = {1: (339, 578), 2: (373, 422), 3: (609, 701), 4: (626, 601), 5: (658, 383), 6: (672, 461), 7: (739, 400), 8: (756, 798),
           9: (824, 604), 10: (882, 597), 11: (919, 496), 12: (512, 354), 13: (554, 346), 14: (590, 343), 15: (624, 342), 16: (681, 353),
           17: (703, 354), 18: (734, 354), 19: (756, 357), 20: (771, 385), 21: (770, 418), 22: (812, 574), 23: (800, 603), 24: (886, 531),
           25: (886, 508), 26: (927, 477), 27: (1064, 716), 28: (1187, 850)}
F20_SCALE = 1.24
F20_TABLE_X = 1690                     # これより右は品名の表（海岸ではない＝重ねに使わない）
# 重ねの始めの値（図の画素 ← 緯度経度）＝町の点の目読み。fit がこれから詰める
F20_SEED = [((350.0, 694.0), (139.137, 35.158)),     # 真鶴
            ((1013.0, 686.0), (139.617, 35.143)),    # 三崎
            ((1497.0, 955.0), (139.950, 34.975)),    # 千倉
            ((713.0, 1376.0), (139.400, 34.740))]    # 大島（島の真ん中）
F20_FIT_BBOX = (138.85, 34.55, 140.15, 35.45)

def km_xy(lon, lat, lat0=34.77):
    return (lon * math.cos(math.radians(lat0)) * 111.32, lat * 110.57)


# ── 付図-21 の式 ──
def _lsq(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return a, my - a * mx


F21_LON = _lsq(F21_V, list(range(10)))                      # 分 = a·x + b
F21_LAT = _lsq([h[0] for h in F21_H], [h[1] for h in F21_H])


def f21_ll(x, y):
    return (139.0 + (F21_LON[0] * x + F21_LON[1]) / 60.0, 34.0 + (F21_LAT[0] * y + F21_LAT[1]) / 60.0)


def f21_px(lon, lat):
    return (((lon - 139.0) * 60.0 - F21_LON[1]) / F21_LON[0], ((lat - 34.0) * 60.0 - F21_LAT[1]) / F21_LAT[0])


def _load(p):
    import numpy as np
    from PIL import Image
    return np.asarray(Image.open(p).convert("L"), dtype=np.float32)


def _dijkstra(cost, a, b, allow):
    h, w = cost.shape
    dist = {a: 0.0}
    prev = {}
    pq = [(0.0, a)]
    while pq:
        dd, (x, y) = heapq.heappop(pq)
        if (x, y) == b:
            break
        if dd > dist.get((x, y), 1e18):
            continue
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx and not dy:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h) or not allow[ny, nx]:
                    continue
                nd = dd + cost[ny, nx] * (1.4142 if dx and dy else 1.0)
                if nd < dist.get((nx, ny), 1e18):
                    dist[(nx, ny)] = nd
                    prev[(nx, ny)] = (x, y)
                    heapq.heappush(pq, (nd, (nx, ny)))
    out = [b]
    while out[-1] != a:
        out.append(prev[out[-1]])
    return out[::-1]


def _seg_dist(px, py, pl):
    import numpy as np
    best = np.full(px.shape, 1e9, dtype=np.float32)
    for (ax, ay), (bx, by) in zip(pl, pl[1:]):
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy
        u = np.clip(((px - ax) * vx + (py - ay) * vy) / L2, 0, 1)
        d = np.hypot(px - (ax + u * vx), py - (ay + u * vy))
        best = np.minimum(best, d)
    return best


def _simplify(pl, tol=1.2):
    """ダグラス・ポーカー（画素の折れ線を、tol 画素より細かい曲がりを捨てて間引く）"""
    if len(pl) < 3:
        return list(pl)
    (ax, ay), (bx, by) = pl[0], pl[-1]
    L = math.hypot(bx - ax, by - ay) or 1e-9
    k, dm = 0, -1.0
    for i, (x, y) in enumerate(pl[1:-1], 1):
        d = abs((bx - ax) * (ay - y) - (ax - x) * (by - ay)) / L
        if d > dm:
            k, dm = i, d
    if dm <= tol:
        return [pl[0], pl[-1]]
    return _simplify(pl[:k + 1], tol)[:-1] + _simplify(pl[k:], tol)


# 海岸線の通り道（目読み・約30画素おき）。⑤b-4 の1回目・2回目：帯（Natural Earth から 45画素）の中の最短の道だけでは、
#   目盛りの線・「稲取港」の字・岸の斜線を近道にして、稲取港の出っ張りを飛ばし白田の海岸で階段になった＝通り道を細かく置き、
#   隣どうしを 18画素の帯の中でつなぐ（目盛りの線は白く消す）
F21_COAST_WP = [(690, 15), (650, 60), (610, 105), (585, 150), (570, 175), (560, 205), (553, 240), (548, 270), (543, 300), (530, 330),
                (510, 355), (490, 375), (470, 390), (445, 410), (425, 430), (410, 440), (425, 447), (445, 457), (455, 470), (450, 490),
                (430, 503), (395, 505), (360, 500), (335, 490), (315, 480), (300, 495), (285, 515), (265, 545), (250, 575),
                (240, 600), (215, 620), (190, 630), (160, 630), (140, 645), (110, 665), (85, 690), (75, 720), (70, 760), (65, 800),
                (55, 830), (40, 850), (35, 880), (20, 900), (5, 920)]


def f21_coast():
    """付図-21 の海岸線＝目読みの通り道を一番近い黒い画素へ寄せ、隣どうしを黒い画素を安く通る最短の道でつなぐ（上の端 → 左下の端）"""
    import numpy as np
    im = _load(F21).copy()
    h, w = im.shape
    for x in F21_V:
        im[:, max(0, int(round(x)) - 2):int(round(x)) + 3] = 255.0
    for y in [hh[0] for hh in F21_H] + [907.0]:
        im[max(0, int(round(y)) - 2):int(round(y)) + 3, :] = 255.0
    cost = 1.0 + 40.0 * (im / 255.0) ** 2
    yy, xx = np.mgrid[0:h, 0:w]
    xx, yy = xx.astype(np.float32), yy.astype(np.float32)

    def snap(p, r=7):
        x, y = p
        best = None
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and im[ny, nx] < 120 and (best is None or dx * dx + dy * dy < best[0]):
                    best = (dx * dx + dy * dy, (nx, ny))
        return best[1] if best else (x, y)
    wps = [snap(p) for p in F21_COAST_WP]
    pl = [wps[0]]
    for a, b in zip(wps, wps[1:]):
        band = _seg_dist(xx, yy, [a, b]) < 18
        pl += _dijkstra(cost, a, b, band)[1:]
    # ⑤b-4 の3回目：通り道を岸の斜線の上に寄せた所で、道が斜線を上って下りる「とげ」になった＝来た道へ 1.5画素以内に戻ったら、その間を切る
    out = []
    for p in pl:
        cut = None
        for j in range(max(0, len(out) - 60), len(out) - 3):
            if (out[j][0] - p[0]) ** 2 + (out[j][1] - p[1]) ** 2 <= 2.25:
                cut = j
                break
        if cut is not None:
            del out[cut + 1:]
        else:
            out.append(p)
    return [(float(x), float(y)) for x, y in _simplify(out, 1.2)]


# ── 付図-20：Natural Earth に重ねる ──
LAT0F, LON0F = 35.0, 139.4


def _to_km(lon, lat):
    return ((lon - LON0F) * math.cos(math.radians(LAT0F)) * 111.32, (lat - LAT0F) * 110.57)


def _to_ll(x, y):
    return (LON0F + x / (math.cos(math.radians(LAT0F)) * 111.32), LAT0F + y / 110.57)


def f20_fit():
    import numpy as np
    from scipy import ndimage, optimize
    im = _load(F20)
    dark = im < 140
    dark[:, F20_TABLE_X:] = False
    dt = ndimage.distance_transform_edt(~dark)
    d = json.loads((HERE / "coast_ne10m.json").read_text(encoding="utf-8"))
    bx0, by0, bx1, by1 = d["bbox"]
    pts = []
    for poly in d["polys"]:
        ring = poly + [poly[0]]
        for (a, b), (c, e) in zip(ring, ring[1:]):
            if not (F20_FIT_BBOX[0] <= a <= F20_FIT_BBOX[2] and F20_FIT_BBOX[1] <= b <= F20_FIT_BBOX[3]):
                continue
            if (abs(a - c) < 1e-9 and min(abs(a - bx0), abs(a - bx1)) < 1e-6) or \
               (abs(b - e) < 1e-9 and min(abs(b - by0), abs(b - by1)) < 1e-6):
                continue
            p, q = _to_km(a, b), _to_km(c, e)
            n = max(1, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 0.4))
            for k in range(n):
                t = k / n
                pts.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    pts = np.array(pts)
    X = np.c_[pts, np.ones(len(pts))]
    h, w = im.shape
    CAP = 15.0
    Xs = np.array([[*_to_km(*ll), 1.0] for _uv, ll in F20_SEED])
    Us = np.array([uv for uv, _ll in F20_SEED])
    A0, *_ = np.linalg.lstsq(Xs, Us, rcond=None)

    def cost(a):
        A = a.reshape(2, 3)
        uv = X @ A.T
        ok = (uv[:, 0] >= 0) & (uv[:, 0] < F20_TABLE_X) & (uv[:, 1] >= 0) & (uv[:, 1] < h - 1)
        dd = ndimage.map_coordinates(dt, [uv[ok, 1], uv[ok, 0]], order=1)
        return float(np.minimum(dd, CAP).sum() + CAP * (~ok).sum())
    a0 = A0.T.ravel()
    best = optimize.minimize(cost, a0, method="Powell", options=dict(maxiter=30000, xtol=1e-4, ftol=1e-7))
    A = best.x.reshape(2, 3)
    uv = X @ A.T
    ok = (uv[:, 0] >= 0) & (uv[:, 0] < F20_TABLE_X) & (uv[:, 1] >= 0) & (uv[:, 1] < h - 1)
    dd = ndimage.map_coordinates(dt, [uv[ok, 1], uv[ok, 0]], order=1)
    near = dd[dd < CAP]
    stats = dict(n=int(ok.sum()), near=int(len(near)), med=round(float(np.median(near)), 2),
                 p90=round(float(np.percentile(near, 90)), 2), cost0=round(cost(a0), 1), cost=round(float(best.fun), 1))
    return A, stats


def f20_points():
    """揚収場所の丸（ハフ変換）を目読みの点へ当てる"""
    import cv2
    import numpy as np
    im = cv2.imread(str(F20), 0)
    cs = cv2.HoughCircles(cv2.GaussianBlur(im, (3, 3), 0), cv2.HOUGH_GRADIENT, dp=1, minDist=14, param1=120, param2=13,
                          minRadius=9, maxRadius=16)[0]
    out = {}
    for k, (x, y) in F20_EST.items():
        x, y = x * F20_SCALE, y * F20_SCALE
        d = np.hypot(cs[:, 0] - x, cs[:, 1] - y)
        i = int(d.argmin())
        if d[i] > 12:
            raise SystemExit(f"付図-20 の点 {k}：丸が目読みから {d[i]:.1f}画素（読み直す）")
        out[k] = (float(cs[i, 0]), float(cs[i, 1]), round(float(d[i]), 1))
    return out


def _inv(A, u, v):
    import numpy as np
    M = np.array([[A[0][0], A[0][1]], [A[1][0], A[1][1]]])
    x, y = np.linalg.solve(M, [u - A[0][2], v - A[1][2]])
    return _to_ll(x, y)


# ── 解説 図15 ──
def f15_image():
    import fitz
    import numpy as np
    d = fitz.open(str(KAI))
    p = d[KAI_PAGE]
    R = None
    for x in p.get_images(full=True):
        for r in p.get_image_rects(x[0]):
            R = r if R is None else R | r
    pix = p.get_pixmap(dpi=KAI_DPI, clip=R)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3].copy()


def f15_read():
    """経緯線（長い細い線）・赤い楕円（推定落下区域）・青い矢印（海流）"""
    import cv2
    import numpy as np
    from scipy import ndimage as nd
    rgb = f15_image().astype(int)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    gray = rgb.mean(axis=2)
    H, W = gray.shape
    dark = gray < 120

    def peaks(arr, thr):
        out, i = [], 0
        while i < len(arr):
            if arr[i] > thr:
                j = i
                while j < len(arr) and arr[j] > thr:
                    j += 1
                seg = np.arange(i, j)
                out.append(float((seg * arr[i:j]).sum() / arr[i:j].sum()))
                i = j
            else:
                i += 1
        return out
    vx = peaks(dark[int(H * 0.05):int(H * 0.95)].sum(axis=0), 0.55 * H)
    hy = peaks(dark[:, int(W * 0.05):int(W * 0.95)].sum(axis=1), 0.55 * W)
    red = (r > 170) & (g < 110) & (b < 120)
    lab, n = nd.label(red)
    ells = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 300:
            continue
        ys, xs = np.nonzero(m)
        cnt = np.c_[xs, ys].astype(np.float32)
        hull = cv2.convexHull(cnt)
        (cx, cy), (ma, mi), ang = cv2.fitEllipse(hull)
        ells.append(dict(c=(float(cx), float(cy)), axes=(float(ma), float(mi)), ang=float(ang), n=int(m.sum())))
    blue = (b > 170) & (r < 140) & (g > 120) & (b - r > 60)
    lab, n = nd.label(blue, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 400:
            continue
        ys, xs = np.nonzero(m)
        comps.append(dict(n=int(m.sum()), box=(int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))))
    return dict(size=(W, H), vlines=[round(v, 1) for v in vx], hlines=[round(v, 1) for v in hy], ellipses=ells, blue=comps)


def measure():
    print(json.dumps(f15_read(), ensure_ascii=False, indent=1))


def build():
    coast = f21_coast()
    A, st = f20_fit()
    pts20 = f20_points()
    out = dict(
        note="20本目 ⑤b-4 sagami20.py の出力（手で直さない）。座標は［東経, 北緯］",
        near=dict(
            src="報告書 付図-21 相模湾海底調査区域（p157）",
            calib=dict(lon=F21_LON, lat=F21_LAT),
            coast=[list(f21_ll(x, y)) for x, y in coast],
            area=[list(f21_ll(x, y)) for x, y in F21_AREA],
            pts={str(k): list(f21_ll(x, y)) for k, (x, y) in F21_PTS.items()},
            flight=[list(f21_ll(F21_FLIGHT["x0"], F21_FLIGHT["c"][1] + (F21_FLIGHT["x0"] - F21_FLIGHT["c"][0]) * F21_FLIGHT["d"][1] / F21_FLIGHT["d"][0])),
                    list(f21_ll(F21_FLIGHT["x1"], F21_FLIGHT["c"][1] + (F21_FLIGHT["x1"] - F21_FLIGHT["c"][0]) * F21_FLIGHT["d"][1] / F21_FLIGHT["d"][0]))],
            boom=list(f21_ll(*F21_BOOM)),
            bbox=[list(f21_ll(0, 981)), list(f21_ll(1199, 0))]),
        bay=dict(
            src="報告書 付図-20 相模湾等の浮遊残骸揚収場所図（p156）",
            fit=dict(A=[[float(v) for v in row] for row in A], stats=st, lat0=LAT0F, lon0=LON0F),
            pts={str(k): [*_inv(A, x, y), dd] for k, (x, y, dd) in pts20.items()}),
    )
    try:
        out["fig15"] = f15_build()
    except Exception as e:          # 解説の PDF は git の外（無ければ前の値を残す）
        old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
        if "fig15" not in old:
            raise
        print(f"⚠️ 図15 を読めない（{e}）＝前の値を残す")
        out["fig15"] = old["fig15"]
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {OUT.name}：海岸 {len(coast)} 点・枠 {len(F21_AREA)} 角・調査地点 {len(F21_PTS)}・揚収場所 {len(pts20)}・付図-20 の重ね {st}")


# 図15 の経緯線（⑤b-4 に確率的ハフ変換で測った＝0.7度ほど傾いた走査）。縦の線＝(下の点, 上の点)・横の線＝(左の点, 右の点)
F15_V = {138.5: ((266, 899), (272, 179)), 139.0: ((498, 902), (509, 25)), 139.5: ((735, 903), (750, 29)),
         140.0: ((979, 856), (990, 32))}
F15_H = {35.5: ((30, 177), (1138, 192)), 35.0: ((0, 463), (1138, 473)), 34.5: ((0, 743), (928, 751))}
# 海流の矢印（相模湾の中の5本）＝⑤b-4 に2倍の切り出し（目盛りつき）を目で読んだ線の中心。最後の点が矢の頭。kts＝図の字（流速・ノット）
#   （1回目は青い画素の骨を機械で取ったが、輪の矢印は線どうしが触れて頭の向きが決まらなかった＝目で読む）。駿河湾の矢印は画面の外
F15_ARROWS = {
    "loop": dict(kts="0.7〜0.8・0.3", px=[(602.5, 567.5), (635, 515), (670, 467.5), (710, 430), (745, 397.5), (762.5, 377.5),
                                         (766, 357.5), (755, 330), (730, 314), (690, 310), (650, 317.5), (622.5, 340),
                                         (615, 370), (620, 405), (635, 432.5), (660, 440), (687.5, 421)]),
    "east": dict(kts="0.8〜0.5", px=[(755, 412.5), (785, 407.5), (815, 415), (832.5, 435), (840, 460), (842.5, 487.5)]),
    "long": dict(kts="1.0〜1.2・1.5・1.1", px=[(542.5, 662.5), (595, 635), (645, 600), (685, 570), (715, 535), (740, 505),
                                              (765, 490), (795, 492.5), (830, 510), (860, 550), (885, 590), (915, 630),
                                              (950, 660), (992.5, 677.5)]),
    "hook": dict(kts="1.0", px=[(612.5, 517.5), (595, 517.5), (580, 535), (567.5, 562.5)]),
    "u": dict(kts="0.7〜1.0", px=[(820, 545), (830, 580), (835, 615), (825, 650), (805, 665), (780, 660), (760, 640),
                                  (747.5, 610)]),
    "west": dict(kts="1.5〜2.0", px=[(575, 690), (640, 617.5)]),          # 黒い矢印（大島の西・北東へ）
}


def _xline(seg, y):
    (x0, y0), (x1, y1) = seg
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


def _yline(seg, x):
    (x0, y0), (x1, y1) = seg
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def _pw(v, vals, ks):
    """折れ線の内挿（端は端の区間をのばす）。vals は増える順に並べ替える"""
    pr = sorted(zip(vals, ks))
    for (v0, k0), (v1, k1) in zip(pr, pr[1:]):
        if v <= v1 or (v1, k1) == pr[-1]:
            return k0 + (k1 - k0) * (v - v0) / (v1 - v0)
    return pr[-1][1]


def f15_ll(x, y):
    """図15 の画素 → 経緯度（隣の経緯線のあいだを直線で）"""
    lon = _pw(x, [_xline(F15_V[k], y) for k in F15_V], list(F15_V))
    lat = _pw(y, [_yline(F15_H[k], x) for k in F15_H], list(F15_H))
    return (lon, lat)


def f15_build():
    """赤い楕円（推定落下区域＝図の中の1つ・凡例の楕円は除く・赤い画素の凸包に楕円を当てる）と海流の矢印（F15_ARROWS）"""
    import cv2
    import numpy as np
    from scipy import ndimage as nd
    rgb = f15_image().astype(int)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    red = (r > 170) & (g < 110) & (b < 120)
    red[:400, :] = False                      # 凡例の楕円（y≈256）を除く
    ys, xs = np.nonzero(red)
    hull = cv2.convexHull(np.c_[xs, ys].astype(np.float32))
    (cx, cy), (aw, ah), ang = cv2.fitEllipse(hull)
    ell = []
    for k in range(48):
        t = 2 * math.pi * k / 48
        ex, ey = aw / 2 * math.cos(t), ah / 2 * math.sin(t)
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        ell.append(list(f15_ll(cx + ex * ca - ey * sa, cy + ex * sa + ey * ca)))
    arrows = [dict(name=k, kts=v["kts"], px=[list(p) for p in v["px"]], ll=[list(f15_ll(*p)) for p in v["px"]])
              for k, v in F15_ARROWS.items()]
    return dict(src="解説 p22（図15 相模湾及び駿河湾における海流概況と日航機揚収物件の推定落下区域）",
                ellipse=dict(px=dict(c=[round(cx, 1), round(cy, 1)], axes=[round(aw, 1), round(ah, 1)], ang=round(ang, 1)),
                             c=list(f15_ll(cx, cy)), ll=ell),
                arrows=arrows)


def check(png):
    """読んだ点と線を3つの図に重ねて1枚に（付図-21・付図-20・図15）"""
    import numpy as np
    from PIL import Image, ImageDraw
    d = json.loads(OUT.read_text(encoding="utf-8"))
    a = Image.open(F21).convert("RGB")
    dr = ImageDraw.Draw(a)
    nr = d["near"]
    cpx = [f21_px(*p) for p in nr["coast"]]
    dr.line(cpx, fill=(255, 0, 0), width=2)
    dr.line([f21_px(*p) for p in nr["area"] + nr["area"][:1]], fill=(0, 160, 255), width=2)
    for k, p in nr["pts"].items():
        x, y = f21_px(*p)
        dr.ellipse([x - 12, y - 12, x + 12, y + 12], outline=(0, 200, 0), width=2)
    dr.line([f21_px(*p) for p in nr["flight"]], fill=(255, 0, 255), width=1)
    x, y = f21_px(*nr["boom"])
    dr.ellipse([x - 7, y - 7, x + 7, y + 7], outline=(255, 120, 0), width=3)
    bimg = Image.open(F20).convert("RGB")
    db = ImageDraw.Draw(bimg)
    A = d["bay"]["fit"]["A"]
    cst = json.loads((HERE / "coast_ne10m.json").read_text(encoding="utf-8"))
    for poly in cst["polys"]:
        pts = []
        for lon, lat in poly + poly[:1]:
            x, y = _to_km(lon, lat)
            pts.append((A[0][0] * x + A[0][1] * y + A[0][2], A[1][0] * x + A[1][1] * y + A[1][2]))
        db.line(pts, fill=(0, 120, 255), width=3)
    for k, (lon, lat, _dd) in d["bay"]["pts"].items():
        x, y = _to_km(lon, lat)
        u, v = A[0][0] * x + A[0][1] * y + A[0][2], A[1][0] * x + A[1][1] * y + A[1][2]
        db.ellipse([u - 20, v - 20, u + 20, v + 20], outline=(0, 200, 0), width=4)
    bimg = bimg.resize((bimg.width // 2, bimg.height // 2))
    c = Image.fromarray(f15_image())
    dc = ImageDraw.Draw(c)
    f15 = d["fig15"]
    for ar in f15["arrows"]:
        dc.line([tuple(p) for p in ar["px"]], fill=(255, 0, 255), width=3)
        hx, hy = ar["px"][-1]
        dc.ellipse([hx - 8, hy - 8, hx + 8, hy + 8], fill=(255, 0, 255))
    for lon, seg in F15_V.items():
        dc.line(list(seg), fill=(0, 200, 0), width=1)
    for lat, seg in F15_H.items():
        dc.line(list(seg), fill=(0, 200, 0), width=1)
    e = f15["ellipse"]["px"]
    dc.ellipse([e["c"][0] - 4, e["c"][1] - 4, e["c"][0] + 4, e["c"][1] + 4], fill=(0, 0, 0))
    W = a.width + bimg.width
    out = Image.new("RGB", (W, max(a.height, bimg.height) + c.height), "white")
    out.paste(a, (0, 0))
    out.paste(bimg, (a.width, 0))
    out.paste(c, (0, max(a.height, bimg.height)))
    out.save(png)
    print(f"→ {png}（{out.size}）")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    {"build": build, "measure": measure, "check": lambda: check(sys.argv[2])}[cmd]()
