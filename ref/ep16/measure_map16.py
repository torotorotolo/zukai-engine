# -*- coding: utf-8 -*-
"""measure_map16.py — 16本目の形のもと（#100 イタリア軍地理院 1934年の地形図・PD）を測る道具の**骨組み**（2026-10-01 ⑤b-1）。

映像方針 §7（Vault `Projects/事故検証-16本目-映像方針-絵コンテ-20261001.md`）：谷の平面（VA）と2本の断面（VB・VC）の地形は
#100 から起こす。⑤b-1 で原寸を見て「機械で測れるか」を決めた＝**方眼だけ機械・湖の700m の線は目で読んで記録で照らす**：
  ・1,600×845px の JPEG・茶と灰の単色刷り（青みの画素は全体で約285個＝川・道・等高線が色で分かれない）
  ・等高線は細い線で、森の記号（小さな丸）・崖の毛羽・道の二重線・標高の数字で何度も途切れる＝1本を機械で追えない
  ・1 km 方眼の縦線は列の明るさのくぼみとして約185画素おきに取れる（x≈118・303・487・670・854・1041・1227・1415・横線 y≈430）
    ＝1画素≈5.4m の見込み（1 km 方眼なら。地点の座標〈Wikidata〉で照らして決める）
→ 形を起こすのは ⑤b-2（置き場 VA）から。この道具は3つの仕事だけ持つ：

    python ref/ep16/measure_map16.py grid             # 方眼を機械で取る（くぼみ・間隔・ずれ）＝縮尺
    python ref/ep16/measure_map16.py sheet X0 Y0      # 原寸2倍＋10画素の目盛りの切り出し（目で読む用・qa_out/ep16_b1/）
    python ref/ep16/measure_map16.py check            # 目で読んだ点（ref/ep16/map16.json）を記録の距離で照らす
    python ref/ep16/measure_map16.py profile          # 🆕 ⑤b-3：断面 B・C の地形の線（水平距離・標高）を記録の高さで照らす
    python ref/ep16/measure_map16.py sheet X0 Y0 W H K AX AY BX BY   # 🆕 ⑤b-3：大きさ・倍率・切り口の線を選んだ切り出し

🔴 #100 の取得はカズヤくんの許可のあと（ファイル名・出どころ・大きさ）。置き場＝`ref/ep16/src/igm1934.jpg`（git の外）。
   無いあいだは止まる（黙って0件で通さない）。
⚠️ 目で読んだ点は「目で読んだ」と JSON に書く（`how`）。画面の出典の行は「地形＝1934年の地形図（イタリア軍地理院）から」・
   読めなかった所は「地形は模式」（映像方針 §7）。S8 の図・BY-SA・CC BY・Google Earth はなぞらない
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SRC = HERE / "ref" / "ep16" / "src" / "igm1934.jpg"          # #100（git の外）
POINTS = HERE / "ref" / "ep16" / "map16.json"                # 目で読んだ点（画素）＝⑤b-2 で作る
SHEETS = HERE / "qa_out" / "ep16_b1"
GRID_SPACING_GUESS = 185        # ⑤b-1 にブラウザの表示で測った見当（画素）。grid が実測で上書きする
DIP = 12                        # 列（行）の平均の明るさが全体より これ以上暗い所＝線の候補

# 記録の距離（照らす相手＝映像方針 §7 の 5b-109②・範囲ごとに記録の値を1つ以上）
# 🔴 2026-10-01（⑤b-2）：北の岸の印は「ダムの真横と約1.1キロ上流」の2か所＝2つの印のあいだを測る（ダムの点から斜面の上の印までは
#    斜めの距離になる）
REC_DIST = [
    dict(a="dam", b="tunnel_in", km=2.5, tol=0.25, rec="S1 PDF85（迂回トンネルの入口＝ダムの約2.5キロ上流）"),
    dict(a="north_dam", b="north_1100", km=1.1, tol=0.15, rec="S1 PDF146（北の岸の印＝ダムの真横と約1.1キロ上流）"),
    dict(a="slide_w", b="slide_e", km=1.7, tol=0.2, rec="S1 PDF144（崩れた斜面の幅およそ1.7キロ）"),
]
REC_AREA = dict(km2=1.9, tol=0.19, rec="S1 PDF144（崩れた斜面の面積およそ1.9平方キロ）")
# Wikidata の照合の許し（村の家並みの真ん中は ±100〜200m ずれる＝町が長いロンガローネは 250m まで）
WD_RESID_M = 250.0
WD_SCALE_TOL = 0.06          # 相似で当てた縮尺と方眼の縮尺の差（割合）
WD_ROT_TOL = 4.0             # 相似で当てた回転（度）＝方眼の投影のずれ（約2度）より大きく回っていたら北が上と言えない


def load():
    if not SRC.exists():
        raise SystemExit(f"🔴 {SRC.relative_to(HERE)} が無い＝#100 の取得はカズヤくんの許可のあと"
                         "（Mappa_Vajont_IGM_1934.jpg・Wikimedia Commons・1,600×845・579KB・PD）")
    from PIL import Image
    return Image.open(SRC).convert("RGB")


def dips(means, dip=DIP):
    """平均の明るさの列（行）から、まわりより暗い極小の位置を返す。"""
    avg = sum(means) / len(means)
    return [i for i, v in enumerate(means)
            if v < avg - dip and (i == 0 or v <= means[i - 1]) and (i == len(means) - 1 or v <= means[i + 1])]


def lattice(pos, guess=GRID_SPACING_GUESS):
    """くぼみの位置から等間隔の並び（方眼）を選ぶ＝隣どうしの差が見当の±10%の鎖。(間隔の平均, 線の位置)"""
    best = []
    for start in pos:
        chain = [start]
        for p in pos:
            if p > chain[-1] and abs((p - chain[-1]) - guess) <= guess * 0.1:
                chain.append(p)
        best = max(best, chain, key=len)
    if len(best) < 3:
        return None, best
    gaps = [b - a for a, b in zip(best, best[1:])]
    return sum(gaps) / len(gaps), best


def grid():
    im = load()
    w, h = im.size
    px = im.load()
    lum = [[0.299 * px[x, y][0] + 0.587 * px[x, y][1] + 0.114 * px[x, y][2] for x in range(w)] for y in range(h)]
    cols = [sum(lum[y][x] for y in range(h)) / h for x in range(w)]
    rows = [sum(lum[y]) / w for y in range(h)]
    sx, vx = lattice(dips(cols))
    sy, vy = lattice(dips(rows))
    print(f"■ #100 {w}×{h}px")
    print(f"  縦の線 {len(vx)}本 {vx} 間隔 {sx and round(sx, 1)}px")
    print(f"  横の線 {len(vy)}本 {vy} 間隔 {sy and round(sy, 1)}px")
    if not sx or not sy or abs(sx - sy) > 0.05 * sx:
        raise SystemExit("🔴 方眼が等間隔に取れない（縦と横の間隔が5%より違う）＝目で確かめてから")
    print(f"✓ 方眼の間隔 {round((sx + sy) / 2, 1)}px（1 km 方眼なら 1画素≈{1000 / ((sx + sy) / 2):.2f}m＝地点の座標で照らして決める）")
    return (sx + sy) / 2, vx, vy


def sheet(x0, y0, size=(400, 300), k=2, mark=None):
    """原寸 k 倍の切り出しに 10画素（原寸）ごとの目盛りを足す（目で読む用・qa_out/ep16_b1/）。
    🆕 ⑤b-3：size（幅・高さ）を選べる・mark＝断面の切り口の線（#100 の画素の2点）を細い赤の破線で重ねる（線の上の標高を読む用）"""
    from PIL import ImageDraw
    im = load().crop((x0, y0, x0 + size[0], y0 + size[1])).resize((size[0] * k, size[1] * k), 0)
    if mark:
        dm = ImageDraw.Draw(im)
        (ax, ay), (bx, by) = mark
        n = int(max(abs(bx - ax), abs(by - ay)) // 6)
        for i in range(0, n, 2):                       # 破線（6画素ごと・地図の線を隠さない）
            p = (ax + (bx - ax) * i / n, ay + (by - ay) * i / n)
            q = (ax + (bx - ax) * (i + 1) / n, ay + (by - ay) * (i + 1) / n)
            dm.line([((p[0] - x0) * k, (p[1] - y0) * k), ((q[0] - x0) * k, (q[1] - y0) * k)], fill=(220, 0, 0), width=1)
    d = ImageDraw.Draw(im)
    for i in range(0, size[0] + 1, 10):
        d.line([(i * k, 0), (i * k, 12 if i % 50 else 24)], fill=(220, 0, 0), width=1)
        if i % 50 == 0:
            d.text((i * k + 2, 26), str(x0 + i), fill=(220, 0, 0))
    for j in range(0, size[1] + 1, 10):
        d.line([(0, j * k), (12 if j % 50 else 24, j * k)], fill=(220, 0, 0), width=1)
        if j % 50 == 0:
            d.text((26, j * k + 2), str(y0 + j), fill=(220, 0, 0))
    SHEETS.mkdir(parents=True, exist_ok=True)
    out = SHEETS / f"igm1934_x{x0}_y{y0}_k{k}.png"
    im.save(out)
    print(f"✓ {out.relative_to(HERE)}（原寸 {size[0]}×{size[1]}px を {k} 倍・10画素の目盛り）")


def shore(rows, x, side):
    """湖の700mの線の概略（lake_stations の行）の、x での岸の y（side＝"n" 北／"s" 南）。行のあいだは直線で。"""
    rows = sorted(rows)
    for (x0, y0, n0, s0), (x1, y1, n1, s1) in zip(rows, rows[1:]):
        if x0 <= x <= x1:
            f = (x - x0) / (x1 - x0) if x1 > x0 else 0.0
            y, n, s = y0 + (y1 - y0) * f, n0 + (n1 - n0) * f, s0 + (s1 - s0) * f
            return y - n if side == "n" else y + s
    raise ValueError(f"x={x} は湖の範囲の外")


def slide_poly(js):
    """崩れた範囲（模式）＝前のふち（湖の南の岸・slide_w〜slide_e）＋後ろのふち（polys.slide_back）。"""
    p = js["points"]
    rows = js["lake_stations"]["rows"]
    x0, x1 = p["slide_w"]["x"], p["slide_e"]["x"]
    front = [(float(x), shore(rows, x, "s")) for x in range(int(x0), int(x1) + 1, 8)] + [(float(x1), shore(rows, x1, "s"))]
    return front + [tuple(map(float, q)) for q in js["polys"]["slide_back"]]


def area(poly):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(poly, poly[1:] + poly[:1]))) / 2


def wikidata(js):
    """地図の画素と Wikidata の座標を照らす（方眼の縮尺・北が上の当て＝残差／相似の当て＝縮尺と回転）。返り値＝食い違いの一覧。"""
    import cmath
    import math
    wd = js["scale"]["wikidata"]
    lat0, lon0 = wd["dam"]
    r0 = math.radians(lat0)
    mlat = 111132.954 - 559.822 * math.cos(2 * r0) + 1.175 * math.cos(4 * r0)
    mlon = 111412.84 * math.cos(r0) - 93.5 * math.cos(3 * r0) + 0.118 * math.cos(5 * r0)
    s = js["m_per_px"]
    use = {k: v for k, v in wd["points"].items() if v["use"]}
    en = {k: ((v["lon"] - lon0) * mlon, (v["lat"] - lat0) * mlat) for k, v in wd["points"].items()}
    dx = sum(v["x"] - en[k][0] / s for k, v in use.items()) / len(use)
    dy = sum(v["y"] + en[k][1] / s for k, v in use.items()) / len(use)
    bad = []
    print(f"■ Wikidata の照合（方眼の縮尺 {s}m・北が上）：ダム＝({dx:.1f}, {dy:.1f})・読んだダム "
          f"({js['points']['dam']['x']}, {js['points']['dam']['y']})")
    for k, v in wd["points"].items():
        r = math.hypot(v["x"] - (dx + en[k][0] / s), v["y"] - (dy - en[k][1] / s)) * s
        ok = r <= WD_RESID_M or not v["use"]
        print(f"  {'✓' if ok else '🔴'} {k} 残差 {r:.0f}m" + ("" if v["use"] else "（照合に使わない）"))
        if not ok:
            bad.append(f"{k} の残差 {r:.0f}m")
    z = [complex(*en[k]) for k in use]
    w = [complex(v["x"], -v["y"]) for v in use.values()]
    zm, wm = sum(z) / len(z), sum(w) / len(w)
    a = sum((wi - wm) * (zi - zm).conjugate() for wi, zi in zip(w, z)) / sum(abs(zi - zm) ** 2 for zi in z)
    sc, rot = 1 / abs(a), math.degrees(cmath.phase(a))
    ok = abs(sc / s - 1) <= WD_SCALE_TOL and abs(rot) <= WD_ROT_TOL
    print(f"  {'✓' if ok else '🔴'} 相似の当て：1画素 {sc:.3f}m（方眼と {(sc / s - 1) * 100:+.1f}%・許し ±{WD_SCALE_TOL * 100:.0f}%）・"
          f"回転 {rot:+.1f}度（許し ±{WD_ROT_TOL}度）")
    if not ok:
        bad.append(f"相似の当て 縮尺 {sc:.3f}・回転 {rot:+.1f}")
    d = math.hypot(js["points"]["dam"]["x"] - dx, js["points"]["dam"]["y"] - dy) * s
    ok = d <= WD_RESID_M
    print(f"  {'✓' if ok else '🔴'} 読んだダムと当てたダムの差 {d:.0f}m")
    if not ok:
        bad.append(f"ダムの差 {d:.0f}m")
    return bad


# 🆕 ⑤b-3（2026-10-01）：断面（VB＝谷を横切る・VC＝谷に沿う）の地形の線。照らす記録の高さ（門番 check_illu も別に持つ＝§5b-88）
REC_Z = dict(lake=(700.0, "S1 PDF96（その朝の水位＝約700m）"), north=(930.0, "S1 PDF146（北の岸で930m）"),
             crest=(725.5, "S9 PDF6（天端725.50m）"), height=(261.6, "S9 PDF6（高さ261.60m）"),
             crack=(930.0, 1260.0, "S1 PDF72（囲む亀裂＝1,200→930→1,260→1,030m）"))


def _river_len(pts):
    out, L = [0.0], 0.0
    for a, b in zip(pts, pts[1:]):
        L += ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        out.append(L)
    return out


def section_c(js):
    """C の谷の底＝川の線の点（ダムから上流と下流）を、川の長さで内挿した標高に。[(x, z)]（x の大きい＝東＝上流の順）。"""
    C = js["sections"]["C"]
    riv = [tuple(p) for p in js["lines"]["vajont"]]           # 上流（東）→ 下流（西）
    dam = (js["points"]["dam"]["x"], js["points"]["dam"]["y"])
    i = riv.index(dam)
    up = riv[:i + 1][::-1]                                     # ダム → 上流の端
    end = tuple(C["lake_end"][:2])
    up = up[:up.index(end) + 1]
    Lu = _river_len(up)
    z0, zu = C["dam_base"], C["lake_end"][2]
    out = [(p[0], z0 + (zu - z0) * L / Lu[-1]) for p, L in zip(up, Lu)]
    dn = riv[i:]
    ex = tuple(C["gorge_exit"][:2])
    dn = dn[:dn.index(ex) + 1]
    Ld = _river_len(dn)
    out += [(p[0], z0 + (C["gorge_exit"][2] - z0) * L / Ld[-1]) for p, L in zip(dn[1:], Ld[1:])]
    return sorted(out, key=lambda q: -q[0])


def section_b(js):
    """B の地形の線＝[(南の端からの水平距離 m, 標高 m)]（南→北）。"""
    B = js["sections"]["B"]
    y0 = B["line"][0][1]
    return [((y0 - y) * js["m_per_px"], z) for y, z, _h in B["pts"]]


def _interp(prof, u):
    for (u0, z0), (u1, z1) in zip(prof, prof[1:]):
        if u0 <= u <= u1:
            return z0 + (z1 - z0) * (u - u0) / (u1 - u0) if u1 > u0 else z0
    raise ValueError(f"u={u} は断面の外")


def profile():
    """断面の地形の線を「水平距離・標高」で示し、記録の高さで照らす（⑤b-3）。"""
    js = json.loads(POINTS.read_text(encoding="utf-8"))
    m = js["m_per_px"]
    rows = js["lake_stations"]["rows"]
    bad = []
    B = js["sections"]["B"]
    x = B["line"][0][0]
    y0 = B["line"][0][1]
    prof = section_b(js)
    print(f"■ B 谷を横切る断面（#100 の x={x}・{B['look']}）")
    for (u, z), (y, _z, how) in zip(prof, B["pts"]):
        print(f"  y{y:>4}  {u:7.0f}m  {z:6.0f}m  {how}")
    for side, nm in (("s", "南の岸"), ("n", "北の岸")):
        u = (y0 - shore(rows, x, side)) * m
        z = _interp(prof, u)
        ok = abs(z - REC_Z["lake"][0]) <= 15
        print(f"  {'✓' if ok else '🔴'} {nm}（湖の700mの線・y{shore(rows, x, side):.1f}）の地面 {z:.0f}m（{REC_Z['lake'][1]}）")
        if not ok:
            bad.append(nm)
    u = (y0 - js["points"]["north_1100"]["y"]) * m
    z = _interp(prof, u)
    ok = abs(z - REC_Z["north"][0]) <= 1
    print(f"  {'✓' if ok else '🔴'} 北の岸の印（y{js['points']['north_1100']['y']}）の地面 {z:.0f}m（{REC_Z['north'][1]}）")
    bad += [] if ok else ["北の岸の印"]
    hi = max(z for u2, z in prof if u2 > u)
    ok = hi > REC_Z["north"][0]
    print(f"  {'✓' if ok else '🔴'} 印より北の地面の最高 {hi:.0f}m（930m より高い＝水が越えない）")
    bad += [] if ok else ["北の端"]
    back = next(z for (u2, z), (y, _z, _h) in zip(prof, B["pts"]) if y == 814)
    lo, hi2, rec = REC_Z["crack"]
    ok = lo <= back <= hi2
    print(f"  {'✓' if ok else '🔴'} 崩れた範囲の後ろのふち（y814）{back:.0f}m（{rec}の {lo:.0f}〜{hi2:.0f}m の内）")
    bad += [] if ok else ["後ろのふち"]
    C = js["sections"]["C"]
    pc = section_c(js)
    xe = C["line"][0][0]
    print(f"\n■ C 谷に沿う断面（#100 の y={C['line'][0][1]}・{C['look']}）＝{C['how']}")
    for xx, z in pc:
        if C["line"][1][0] - 60 <= xx <= xe + 60:
            print(f"  x{xx:>5}  {(xe - xx) * m:7.0f}m  {z:6.1f}m")
    zd = dict(pc)[js["points"]["dam"]["x"]]
    want = REC_Z["crest"][0] - REC_Z["height"][0]
    ok = abs(zd - want) <= 0.05
    print(f"  {'✓' if ok else '🔴'} ダムの所の谷の底 {zd:.1f}m（天端−高さ＝{want:.1f}m・{REC_Z['crest'][1]}・{REC_Z['height'][1]}）")
    bad += [] if ok else ["ダムの底"]
    ok = all(a[1] >= b[1] for a, b in zip(pc, pc[1:]))
    print(f"  {'✓' if ok else '🔴'} 谷の底は上流ほど高い（東→西で下る）")
    bad += [] if ok else ["谷の底の向き"]
    zb = _interp(sorted(((xe - xx) * m, z) for xx, z in pc), (xe - x) * m)
    zb_b = next(z for y, z, _h in B["pts"] if y == 548)
    ok = abs(zb - zb_b) <= 3
    print(f"  {'✓' if ok else '🔴'} B と C の交わる所（x{x}）の谷の底：C {zb:.0f}m／B {zb_b:.0f}m")
    bad += [] if ok else ["B と C の谷の底"]
    sys.exit(1 if bad else 0)


def check():
    """目で読んだ点（画素）を km に直し、記録の距離・面積と照らす＋Wikidata の座標で縮尺と向きを照らす（⑤b-2）。"""
    if not POINTS.exists():
        raise SystemExit(f"🔴 {POINTS.relative_to(HERE)} が無い＝⑤b-2 で目で読んだ点を書いてから（how＝目で読んだ）")
    pts = json.loads(POINTS.read_text(encoding="utf-8"))
    m_per_px = pts["m_per_px"]          # grid と地点の座標で決めた値（JSON に根拠と一緒に書く）
    bad = []
    print("■ 記録の距離")
    for r in REC_DIST:
        a, b = pts["points"][r["a"]], pts["points"][r["b"]]
        km = ((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2) ** 0.5 * m_per_px / 1000
        ok = abs(km - r["km"]) <= r["tol"]
        print(f"  {'✓' if ok else '🔴'} {r['a']}→{r['b']} {km:.2f}km（記録 {r['km']}km±{r['tol']}・{r['rec']}）")
        if not ok:
            bad.append(r)
    km2 = area(slide_poly(pts)) * m_per_px ** 2 / 1e6
    ok = abs(km2 - REC_AREA["km2"]) <= REC_AREA["tol"]
    print(f"  {'✓' if ok else '🔴'} 崩れた範囲（模式）の面積 {km2:.2f}km²（記録 {REC_AREA['km2']}±{REC_AREA['tol']}・{REC_AREA['rec']}）")
    if not ok:
        bad.append(REC_AREA)
    rows = pts["lake_stations"]["rows"]
    L = sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in zip(rows, rows[1:])) * m_per_px / 1000
    print(f"  （参考）湖の700mの線の概略：ダムから上流の端まで川ぞいに {L:.1f}km（記録に長さは無い）")
    bad += wikidata(pts)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "grid"
    if cmd == "grid":
        grid()
    elif cmd == "sheet":
        # sheet X0 Y0 [W H [K [AX AY BX BY]]]＝切り出しの大きさ・倍率・重ねる切り口の線（⑤b-3）
        a = [int(v) for v in sys.argv[2:]]
        sheet(a[0], a[1], size=tuple(a[2:4]) if len(a) >= 4 else (400, 300), k=a[4] if len(a) >= 5 else 2,
              mark=((a[5], a[6]), (a[7], a[8])) if len(a) >= 9 else None)
    elif cmd == "check":
        check()
    elif cmd == "profile":
        profile()
    else:
        raise SystemExit(__doc__)
