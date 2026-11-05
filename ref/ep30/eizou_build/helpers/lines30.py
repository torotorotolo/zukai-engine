# -*- coding: utf-8 -*-
"""30本目 ⑤b-3：地図に描き足す線（路線3本・県の境）を国土数値情報（国土交通省）から作る。出力＝`ref/ep30/sat_lines30.json`（緯度・経度の組＝ss.SAT_LINES が読む・公開リポに入る）。

  python -X utf8 -I ref/ep30/eizou_build/helpers/lines30.py ref/ep30/src/ksj ref/ep30/sat_lines30.json

入力（git の外＝`ref/ep30/src/ksj/`・2026-11-05 に取った・公的な機関のファイル）：
  N02-24_GML.zip＝鉄道（路線の名つき）・N03-20250101_{13,14,19,20,43}_GML.zip＝行政区域（東京・神奈川・山梨・長野・熊本）
  許諾＝どちらも「オープンデータ（CC_BY_4.0）」（データの頁の欄）・サイトの規約＝PDL1.0＋「国土数値情報（○○データ）をもとに作成」の断り＝ss.SAT_LINE_NOTE

🔴 この回の線（§B2-12）＝路線は**線だけ**＝駅の点も区間の細部も足さない（駅の札は章ファイルの「霞ケ関」だけ）。
県の境＝市区町村の面を足し合わせて外周を取る（2つの面が共有する辺を消す）・海の側の線も残る（面の外周）＝額の中に切ってから間引く（Douglas–Peucker）。
額の外へ出る線は切る（門番 check_sat＝描き足しは額の中）。窓は撮った絵の範囲（中心・ズーム）＋内側の余白 KEEP（画素）。
"""
import json
import math
import os
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
CW, CH, DPR = 1280, 720, 1.5
KEEP = 30                 # 撮った絵の縁から内側へ（1920×1080 の画素）
SPLIT = 8                 # 大きな輪を割る点の数


def wx(lo, z):
    return (lo + 180) / 360 * 256 * 2 ** z


def wy(la, z):
    p = math.radians(la)
    return (1 - math.log(math.tan(p) + 1 / math.cos(p)) / math.pi) / 2 * 256 * 2 ** z


def to_px(la, lo, ll, z):
    return ((CW / 2 + wx(lo, z) - wx(ll[1], z)) * DPR, (CH / 2 + wy(la, z) - wy(ll[0], z)) * DPR)


def rdp(pts, tol):
    """Douglas–Peucker（pts＝画素の座標と元の点の組。tol＝画素）"""
    if len(pts) < 3:
        return pts
    keep = [0, len(pts) - 1]
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a][0], pts[b][0]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1e-9
        best, bi = 0.0, None
        for i in range(a + 1, b):
            x, y = pts[i][0]
            d = abs((x - x1) * dy - (y - y1) * dx) / n if (x1, y1) != (x2, y2) else math.hypot(x - x1, y - y1)
            if d > best:
                best, bi = d, i
        if bi is not None and best > tol:
            keep.append(bi)
            stack += [(a, bi), (bi, b)]
    return [pts[i] for i in sorted(keep)]


def clip_chain(chain, ll, z, top=KEEP):
    """緯度・経度の列を窓で切る＝窓の中の区間だけの列を返す（境の点は線分と窓の交点で足す）。top＝上の余白（左上の「マップで開く」の箱の下で切るとき）"""
    x0, y0, x1, y1 = KEEP, top, CW * DPR - KEEP, CH * DPR - KEEP

    def inside(p):
        return x0 <= p[0] <= x1 and y0 <= p[1] <= y1

    def cross(p, q):
        """p（中）→ q（外）の窓との交点の割合"""
        ts = []
        for v0, v1, lo, hi in ((p[0], q[0], x0, x1), (p[1], q[1], y0, y1)):
            if v1 > hi:
                ts.append((hi - v0) / (v1 - v0))
            elif v1 < lo:
                ts.append((lo - v0) / (v1 - v0))
        return min(ts) if ts else 1.0

    out, cur = [], []
    prev, prev_ll = None, None
    for la, lo in chain:
        p = to_px(la, lo, ll, z)
        if prev is not None:
            a, b = inside(prev), inside(p)
            if a and not b:
                t = cross(prev, p)
                cur.append((prev_ll[0] + (la - prev_ll[0]) * t, prev_ll[1] + (lo - prev_ll[1]) * t))
                out.append(cur)
                cur = []
            elif b and not a:
                t = cross(p, prev)
                cur = [(la + (prev_ll[0] - la) * t, lo + (prev_ll[1] - lo) * t)]
        if inside(p):
            cur.append((la, lo))
        prev, prev_ll = p, (la, lo)
    if cur:
        out.append(cur)
    return [c for c in out if len(c) >= 2]


def simplify(chain, ll, z, tol):
    pts = [(to_px(la, lo, ll, z), (la, lo)) for la, lo in chain]
    return [q for _, q in rdp(pts, tol)]


def walk(segs):
    """線分の列（端で続く）を、いちばん長く続く1本に並べる（枝は別に返す）。端の座標は丸めて照らす"""
    def key(p):
        return (round(p[0], 5), round(p[1], 5))
    left = list(segs)
    chains = []
    while left:
        cur = list(left.pop(0))
        grew = True
        while grew:
            grew = False
            for i, s in enumerate(left):
                if key(s[0]) == key(cur[-1]):
                    cur += s[1:]
                elif key(s[-1]) == key(cur[-1]):
                    cur += list(reversed(s))[1:]
                elif key(s[-1]) == key(cur[0]):
                    cur = s[:-1] + cur
                elif key(s[0]) == key(cur[0]):
                    cur = list(reversed(s))[:-1] + cur
                else:
                    continue
                left.pop(i)
                grew = True
                break
        chains.append(cur)
    chains.sort(key=len, reverse=True)
    return chains


def rail(ksj, company, names):
    z = zipfile.ZipFile(os.path.join(ksj, "N02-24_GML.zip"))
    d = json.load(z.open("UTF-8/N02-24_RailroadSection.geojson"))
    segs = []
    for f in d["features"]:
        p = f["properties"]
        if p.get("N02_004") == company and p.get("N02_003") in names:
            g = f["geometry"]
            parts = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
            for c in parts:
                segs.append([(float(la), float(lo)) for lo, la in c])
    return walk(segs)


def pref_outline(ksj, code):
    """都県の面（市区町村＋所属未定地）を足し合わせて外周の線にする＝2つの面が共有しない辺だけ"""
    z = zipfile.ZipFile(os.path.join(ksj, f"N03-20250101_{code}_GML.zip"))
    d = json.load(z.open(f"N03-20250101_{code}.geojson"))
    edges = {}
    for f in d["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                for a, b in zip(ring, ring[1:]):
                    ka, kb = (round(a[0], 6), round(a[1], 6)), (round(b[0], 6), round(b[1], 6))
                    if ka == kb:
                        continue
                    k = (ka, kb) if ka < kb else (kb, ka)
                    edges[k] = edges.get(k, 0) + 1
    # 辺をつないで輪にする
    nb = {}
    for (a, b), n in edges.items():
        if n == 1:
            nb.setdefault(a, []).append(b)
            nb.setdefault(b, []).append(a)
    rings = []
    while nb:
        start = next(iter(nb))
        ring, cur = [start], start
        while True:
            nxt = nb.get(cur)
            if not nxt:
                break
            n = nxt.pop()
            nb[n].remove(cur)
            if not nb[cur]:
                del nb[cur]
            if not nb.get(n):
                nb.pop(n, None)
            ring.append(n)
            cur = n
            if n == start:
                break
        rings.append([(la, lo) for lo, la in ring])
    # いちばん広い輪＝本土の外周（点の数で選ぶと入り組んだ島の海岸が勝つ＝東京で踏んだ）
    def area(r):
        las, los = [p[0] for p in r], [p[1] for p in r]
        return (max(las) - min(las)) * (max(los) - min(los))
    rings.sort(key=area, reverse=True)
    return rings


def main():
    ksj = sys.argv[1]
    G02 = ((35.685, 139.735), 12)      # c201 東京都心（gshot30 の表と同じ）
    G05 = ((34.75, 135.1), 7)          # c314 日本の広域
    G11 = ((35.57, 138.97), 10)        # cb05 山梨と東京
    out = {}
    for key, names, tol in (("hibiya", ("2号線日比谷線",), 1.6), ("marunouchi", ("4号線丸ノ内線",), 1.6), ("chiyoda", ("9号線千代田線",), 1.6)):
        chains = rail(ksj, "東京地下鉄", names)
        got = []
        for c in chains:
            for part in clip_chain(c, *G02):
                got.append(simplify(part, *G02, tol))
        got.sort(key=len, reverse=True)
        for i, c in enumerate(got):
            out[f"{key}{i if i else ''}"] = c
        print(f"# {key}: 区間 {len(chains)}本 → 額の中 {len(got)}本・点 {[len(c) for c in got]}", file=sys.stderr)
    for code, key, frame, tol, keep_big in (("14", "pref_kanagawa", G05, 2.0, 1), ("43", "pref_kumamoto", G05, 2.0, 1), ("19", "pref_yamanashi", G05, 2.0, 1), ("20", "pref_nagano", G05, 2.0, 1),
                                            ("19", "yamanashi_w", G11, 2.5, 1)):
        rings = pref_outline(ksj, code)[:keep_big]
        got = []
        for r in rings:
            for part in clip_chain(r, *frame, top=110 if frame is G11 else KEEP):
                got.append(simplify(part, *frame, tol))
        got.sort(key=len, reverse=True)
        # 大きな輪は短く割る＝門番 check_sat は線の外接の箱で測る（輪のままだと箱がロゴや帰属の行の箱を含む＝線は触れていないのに鳴る）
        if frame is G11:
            parts = []
            for c in got:
                parts += [c[i:i + SPLIT + 1] for i in range(0, len(c) - 1, SPLIT)]
            got = parts
        for i, c in enumerate(got):
            out[f"{key}{i if i else ''}"] = c
        print(f"# {key}: 輪の点 {len(rings[0])} → 額の中 {len(got)}本・点 {[len(c) for c in got]}", file=sys.stderr)
    with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as f:
        json.dump({k: [[round(la, 5), round(lo, 5)] for la, lo in c] for k, c in out.items()}, f, ensure_ascii=False, separators=(",", ":"))
    print(f"→ {sys.argv[2]}（{len(out)}本・点 {sum(len(c) for c in out.values())}）")


if __name__ == "__main__":
    main()
