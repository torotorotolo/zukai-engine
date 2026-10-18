# -*- coding: utf-8 -*-
"""satmap.py — 地図の型「衛星写真＋描き足し」（2026-10-14 新設・22本目 ⑤b-3）。

■ 何か（22本目 了承② 決め7・10-14 カズヤくん「地図9カットは Google マップの衛星写真＋描き足し」）
  撮った衛星写真（`helpers/gshot22.py`＝CSS 1280×720・倍率1.5＝1920×1080）を**額装**で置き、点・×・線・矢印・囲み・札を
  **本番の描き手で**重ねる（絵には焼かない）。Google の決まり（記憶 reference-google-maps-satellite-capture）：
    ・帰属の行（右下）とロゴ（中央下）は**映している間ずっと・読める大きさで**＝隠さない・字幕の帯の下に入れない＝額は帯より上
    ・色を変えない（章の色に染めない＝color 1.0）・動かさない（寄らない）・地図そのものを大きく変えない・点と線と札は描き足してよい
  画は**写真のカット**として焼く（`photo=` の額装＋`sat=`）＝写真の箱は `box()`（`scene_jiko.photo_box` がここを呼ぶ＝同じ幾何）。
  描き足しは段（`steps`）ごとに1枚の層＝語りの行の頭でフェードで出る（実写の注記と同じ出し方）。

■ SPEC の書き方（`cuts/ss.sat()` が photo・panel・pw・color をそろえる）
  "c219": dict(**ss.sat("G02", steps=[[…], […]], note="…"), t="…", s="…（現在の衛星写真）")
  部品（段ごとに何個でも。場所は `cuts/ss.GEO` の名＝🔴 確かめていない場所に点を置かない）：
    dict(k="pt", at="stjohns", role="ship", t="母船の港", lab=(18, -16, "start"))   … 点（役の色）＋札
    dict(k="x", at="site", t="事故の現場", lab=(…))                                 … 赤の×（報告書の座標の場所だけ＝門番）
    dict(k="line", path=("stjohns", "site"), role="ship", dash=True, t="約700〜800キロ", lc="AMBER", lab=(…))
                                                                                    … 線（札は線の真ん中から lab・札の色だけ lc で替える）
    dict(k="arrow", fr=(緯度, 経度), to="site", t="…", lab=(…), dir=True)           … 向きの矢印（尾は場所でない＝dir=True）
    dict(k="area", at="harvey", r=120, role="company", t="…", lab=(…))              … 破線の囲み（r は撮った絵の画素）
    dict(k="icon", what="plane"|"ship", on=("buffalo", "stjohns", 0.5), role=…)     … 印（線の途中 u の位置・向きは線の向き）
    dict(k="wave", at="abaco47", t="…", lab=(…))                                    … 音の波の印（赤）
    dict(k="txt", at="marsh", t="…", lc="AMBER", lab=(…))                           … 印の無い札（前の段の点に数を足す）
  lab＝札の置き場（点からの dx・dy〈画面の画素〉・anchor）。role＝`jiko_style.ROLE` の名（uscg・ntsb・tsb・company・ship・sub）か
  色の名 c（INK_W・ALERT・AMBER）。

■ 門番 `tools/check_sat.py`（qa_all）＝`check()`：額の書き方（color 1.0・寄りなし・注記なし）・衛星写真の md5（手元に在るとき）・
  場所の表（出典と座標の出どころ）・×は報告書の座標だけ・描き足しが額の中・**ロゴと帰属の行と Google の部品の箱に入らない**・
  一般の座標を使ったら断り（note）に「一般の座標」・額の下の断りと出典の行が重ならない
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path

import fontmetrics as fm
import jiko_style as J
import titan_fig as F

HERE = Path(__file__).resolve().parents[1]
IW, IH = 1920, 1080                 # 撮った絵（gshot22：CSS 1280×720・倍率1.5）
CW, CH, DPR = 1280, 720, 1.5
PW = 1152                           # 額の幅＝0.6 倍（高さ 648＝scene_jiko.PANEL_MAXH と同じ）
LAB = 32                            # 札の字（画面の画素）
SUBTLE = 24                         # 額の下の断り（出典の行と同じ大きさ）
# 🔴 描き足しを入れない箱（撮った絵の画素・6画を原寸で見た＝⑤b-1／⑤b-3）。ロゴと帰属の行は Google の決まり（隠さない）・
#    「マップで開く」・左下のレイヤーの小窓・右下の全画面の印は Google の操作の部品（隠してよいが、描き足しを重ねると読みにくい）
KEEP_OUT = dict(logo=(860, 1000, 1060, 1080), attrib=(1000, 1046, 1920, 1080),
                open=(0, 0, 230, 72), layers=(0, 985, 95, 1080), full=(1828, 970, 1920, 1062))
HARD = ("logo", "attrib")           # 隠すと決まりに反する箱
EDGE = 8                            # 描き足しと額の縁のすき間の下限（画面の画素）
KINDS = ("pt", "x", "line", "arrow", "area", "icon", "wave", "txt")
COLS = ("INK_W", "ALERT", "AMBER")


# ══════════════════════════════════════════════════════════
#  幾何（Web メルカトル・gshot22.px と同じ式）
# ══════════════════════════════════════════════════════════
def _wx(lon, z):
    return (lon + 180) / 360 * 256 * 2 ** z


def _wy(lat, z):
    p = math.radians(lat)
    return (1 - math.log(math.tan(p) + 1 / math.cos(p)) / math.pi) / 2 * 256 * 2 ** z


def ipx(sat, lat, lon):
    """緯度経度 → 撮った絵の画素（1920×1080）。sat＝`cuts/ss.SAT` の1行（ll＝中心・z＝ズーム）。"""
    lat0, lon0 = sat["ll"]
    z = sat["z"]
    return ((CW / 2 + _wx(lon, z) - _wx(lon0, z)) * DPR, (CH / 2 + _wy(lat, z) - _wy(lat0, z)) * DPR)


def igeo(sat, x, y):
    """撮った絵の画素 → 緯度経度（ipx の逆）。"""
    lat0, lon0 = sat["ll"]
    z = sat["z"]
    n = 256 * 2 ** z
    wx = x / DPR - CW / 2 + _wx(lon0, z)
    wy = y / DPR - CH / 2 + _wy(lat0, z)
    lon = wx / n * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * wy / n))))
    return lat, lon


def m_per_px(sat):
    """🆕 23本目 ⑤b-4：撮った絵の1画素あたりのメートル（Web メルカトル・中心の緯度）。"""
    return 156543.03392 * math.cos(math.radians(sat["ll"][0])) / 2 ** sat["z"] / DPR


def r_of_area(sat, m2):
    """🆕 23本目 ⑤b-4：面積 m2（平方メートル）と同じ面積の円の半径（撮った絵の画素）＝`area` の r。形は模式（境の線が記録に無いとき）。"""
    return math.sqrt(m2 / math.pi) / m_per_px(sat)


def box():
    """額の箱（画面の画素）＝真ん中・本体の帯の中（`scene_jiko.photo_box` の額装と同じ式＝注記なし・pw=PW）。"""
    h = round(PW * IH / IW)
    hmax = J.BAND_B - J.BAND_T - 34
    return ((1920 - PW) // 2, J.BAND_T + (hmax - h) // 2, PW, h)


def spx(p):
    """撮った絵の画素 → 画面の画素。"""
    bx, by, bw, bh = box()
    return bx + p[0] * bw / IW, by + p[1] * bh / IH


def ibox_to_screen(b):
    x0, y0 = spx((b[0], b[1]))
    x1, y1 = spx((b[2], b[3]))
    return (x0, y0, x1, y1)


# ══════════════════════════════════════════════════════════
#  表（回の側＝cuts/ss の SAT・GEO）
# ══════════════════════════════════════════════════════════
def _tables():
    import cuts.ss as ss
    return getattr(ss, "SAT", {}), getattr(ss, "GEO", {})


def file_of(code):
    sat, _ = _tables()
    return sat[code]["file"]


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def have(code):
    """衛星写真が手元（ref/）に在るか。🔴 Actions は Modal の保管庫を読めない＝無い（build_jiko が理由を出して飛ばす）。"""
    return (HERE / "ref" / file_of(code)).exists()


def _col(el):
    if el.get("role"):
        return J.ROLE[el["role"]]
    return getattr(J, el.get("c") or "INK_W")


def _place(name):
    _, geo = _tables()
    return geo[name]


def _pt(sat, at):
    """場所の名か (緯度, 経度) → 画面の画素。"""
    ll = _place(at)["ll"] if isinstance(at, str) else at
    return spx(ipx(sat, *ll))


# ══════════════════════════════════════════════════════════
#  描く（段ごとの層）。返すのは SVG の文字列と、門番が測る「墨の箱」の一覧
# ══════════════════════════════════════════════════════════
def _label(x, y, el, col, inks):
    t = el.get("t")
    if not t:
        return ""
    dx, dy, anc = el.get("lab", (18, -16, "start"))
    size = el.get("size", LAB)
    tx, ty = x + dx, y + dy
    w = fm.width(t, size, "Noto")
    x0 = tx if anc == "start" else (tx - w if anc == "end" else tx - w / 2)
    a, b = fm.ink(t, size, "Noto")
    inks.append(("札「" + t + "」", (x0 - 4, ty - a - 4, x0 + w + 4, ty + b + 4)))     # 字面＝y-ink[0]〜y+ink[1]（縁取り 4px 込み）
    lc = getattr(J, el["lc"]) if el.get("lc") else col
    return J.outlined(round(tx, 1), round(ty, 1), t, lc, size, anc, sw=8)


def _dot(x, y, col, r=11):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 3}" fill="{J.BG}" opacity="0.85"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>')


def _cross(x, y, r=14):
    g = []
    for sw, c in ((13, J.BG), (7, J.ALERT)):
        g.append(f'<path d="M{x - r:.1f} {y - r:.1f} L{x + r:.1f} {y + r:.1f} M{x - r:.1f} {y + r:.1f} L{x + r:.1f} {y - r:.1f}" '
                 f'stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>')
    return "".join(g)


def _poly(pts, col, dash):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    da = ' stroke-dasharray="18 12"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{J.BG}" stroke-width="10" stroke-linecap="round" opacity="0.7"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"{da}/>')


def _along(pts, u):
    """折れ線の長さの割合 u の点と、その向き（度）。"""
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = [math.dist(a, b) for a, b in segs]
    s = u * sum(L)
    for (a, b), l in zip(segs, L):
        if s <= l or (a, b) == segs[-1]:
            k = 0 if l == 0 else min(1.0, s / l)
            return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k), math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        s -= l
    return pts[-1], 0.0


def _ext(pts, pad):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def draw(sat, el, inks):
    """部品1つ → SVG。inks に (名, 墨の箱) を足す（門番が額の中・部品の箱の外かを測る）。"""
    k = el["k"]
    col = _col(el)
    if k == "pt":
        x, y = _pt(sat, el["at"])
        inks.append((f"点 {el['at']}", (x - 14, y - 14, x + 14, y + 14)))
        return _dot(x, y, col) + _label(x, y, el, col, inks)
    if k == "x":
        x, y = _pt(sat, el["at"])
        inks.append((f"× {el['at']}", (x - 20, y - 20, x + 20, y + 20)))
        return _cross(x, y) + _label(x, y, el, J.ALERT, inks)
    if k in ("line", "arrow"):
        pts = [_pt(sat, p) for p in (el["path"] if k == "line" else (el["fr"], el["to"]))]
        inks.append((f"線 {el.get('path') or el.get('to')}", _ext(pts, 6)))
        if k == "line":
            g = _poly(pts, col, el.get("dash"))
        else:
            (x1, y1), (x2, y2) = pts
            a = math.atan2(y2 - y1, x2 - x1)
            gap = el.get("gap", 22)                  # 矢の先を点の手前で止める（×や点に重ねない）
            x2, y2 = x2 - gap * math.cos(a), y2 - gap * math.sin(a)
            g = (f'<g opacity="0.7">{F.line(x1, y1, x2, y2, J.BG, 11)}</g>' + F.arrow(x1, y1, x2, y2, col, 5, head=24))
        (mx, my), _ = _along(pts, el.get("u", 0.5))
        return g + _label(mx, my, el, col, inks)
    if k == "area":
        x, y = _pt(sat, el["at"])
        r = el["r"] * box()[2] / IW
        inks.append((f"囲み {el['at']}", (x - r - 4, y - r - 4, x + r + 4, y + r + 4)))
        return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{J.BG}" stroke-width="10" opacity="0.7"/>'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{col}" stroke-width="5" stroke-dasharray="16 10"/>'
                + _label(x, y, el, col, inks))
    if k == "icon":
        a, b, u = el["on"]
        pts = [_pt(sat, a), _pt(sat, b)]
        (x, y), deg = _along(pts, u)
        s = el.get("s", 0.42)
        if el["what"] == "plane":
            g = F._plane(x, y, head=deg, s=s, col=col)
            r = 54 * s
        else:
            g = F._ship_svg(x, y, deg=deg + 90, col=col, s=s / 0.42)
            r = 32 * s / 0.42
        if el.get("tow"):
            # 台を後ろに引く（船の後ろに短い引き綱と台の四角＝模式）
            rad = math.radians(deg)
            tx, ty = x - (r + 30) * math.cos(rad), y - (r + 30) * math.sin(rad)
            g += (F.line(x - r * math.cos(rad), y - r * math.sin(rad), tx, ty, col, 3, dash="6 5")
                  + f'<rect x="{tx - 9:.1f}" y="{ty - 9:.1f}" width="18" height="18" fill="{J.BG2}" stroke="{col}" stroke-width="4" '
                  f'transform="rotate({deg:.1f} {tx:.1f} {ty:.1f})"/>')
            inks.append(("台の印", (tx - 14, ty - 14, tx + 14, ty + 14)))
        inks.append((f"印 {el['what']}", (x - r, y - r, x + r, y + r)))
        return g + _label(x, y, el, col, inks)
    if k == "txt":
        # 印の無い札（その場所の近くに数や説明を足す＝前の段の点の続き）
        x, y = _pt(sat, el["at"])
        return _label(x, y, el, col, inks)
    if k == "wave":
        x, y = _pt(sat, el["at"])
        g = []
        for i, rr in enumerate((18, 32, 46)):
            for sgn in (1, -1):
                a0, a1 = (-40, 40) if sgn > 0 else (140, 220)
                p = [(x + rr * math.cos(math.radians(t)), y + rr * math.sin(math.radians(t))) for t in range(a0, a1 + 1, 8)]
                d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in p)
                g.append(f'<path d="{d}" fill="none" stroke="{J.BG}" stroke-width="9" opacity="0.7"/>'
                         f'<path d="{d}" fill="none" stroke="{J.ALERT}" stroke-width="4.5"/>')
        inks.append((f"波 {el['at']}", (x - 50, y - 36, x + 50, y + 36)))
        return "".join(g) + _label(x, y, el, J.ALERT, inks)
    raise ValueError(f"satmap：知らない部品 {k!r}（{KINDS}）")


def layers(spec):
    """SPEC の `sat` → 段ごとの層（SVG の文字列のリスト）。1段目に額の下の断り（note）を載せる。"""
    sat_tab, _ = _tables()
    sv = spec["sat"]
    sat = sat_tab[sv["code"]]
    out = []
    for i, st in enumerate(sv["steps"]):
        inks = []
        g = [draw(sat, el, inks) for el in st]
        if i == 0 and sv.get("note"):
            g.append(J.outlined(J.MG, J.BAND_B - 4, sv["note"], J.TICK, SUBTLE, sw=5))
        out.append("".join(g))
    return out


def inks_of(spec):
    """門番用：段ごとの (名, 墨の箱) の一覧。"""
    sat_tab, _ = _tables()
    sat = sat_tab[spec["sat"]["code"]]
    res = []
    for st in spec["sat"]["steps"]:
        inks = []
        for el in st:
            draw(sat, el, inks)
        res.append(inks)
    return res


# ══════════════════════════════════════════════════════════
#  門番（tools/check_sat.py が呼ぶ）
# ══════════════════════════════════════════════════════════
_NO = ("zoom", "cam", "fmove", "ann", "trim", "veil", "levels", "bias", "xbias", "mark", "intro", "tail", "focus", "hl", "fig")


def _hit(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def check(spec_all, credit=None):
    """SPEC の地図のカットを照らす。戻り値＝(問題の一覧, 照らしたカットの数, 照らした部品の数)。"""
    sat_tab, geo = _tables()
    bad, n_el = [], 0
    cuts = {c: s for c, s in spec_all.items() if s.get("sat")}
    bx, by, bw, bh = box()
    if by < J.BAND_T or by + bh > J.BAND_B - 30:
        bad.append(f"額の箱 {box()} が本体の帯（{J.BAND_T}〜{J.BAND_B - 30}＝下に断りと出典の行）の外")
    # 表の確かめ
    for code, s in sat_tab.items():
        for k in ("file", "ll", "z", "md5", "credit"):
            if not s.get(k):
                bad.append(f"SAT {code}：{k} が無い")
        p = HERE / "ref" / s.get("file", "")
        if p.exists() and md5_of(p) != s.get("md5"):
            bad.append(f"SAT {code}：{s['file']} の md5 {md5_of(p)} が表 {s.get('md5')} と違う（撮り直したら表と描き足しの座標を見直す）")
    for name, g in geo.items():
        if not (g.get("ll") and g.get("src") and g.get("how")):
            bad.append(f"GEO {name}：ll・src（報告書で名が出る所）・how（座標の出どころ）のどれかが無い")
    for cid, s in sorted(cuts.items()):
        sv = s["sat"]
        code = sv.get("code")
        if code not in sat_tab:
            bad.append(f"{cid}：衛星写真 {code!r} が SAT に無い")
            continue
        if s.get("photo") != sat_tab[code]["file"]:
            bad.append(f"{cid}：photo={s.get('photo')} が SAT {code} の file と違う")
        if not s.get("panel") or s.get("pw") != PW:
            bad.append(f"{cid}：panel=True・pw={PW} でない（額装で帯より上＝ロゴと帰属の行を字幕の帯の下に入れない）")
        if float(s.get("color") or 0) != 1.0:
            bad.append(f"{cid}：color={s.get('color')}（地図の色を変えない＝1.0）")
        for k in _NO:
            if s.get(k) is not None:
                bad.append(f"{cid}：{k} は書けない（地図を動かさない・切らない・上に注記を置かない）")
        if "現在の衛星写真" not in s.get("s", ""):
            bad.append(f"{cid}：副題に「現在の衛星写真」が無い（写っているのは今の衛星写真）")
        if not sv.get("steps"):
            bad.append(f"{cid}：steps が空")
            continue
        used_general = False
        for i, st in enumerate(sv["steps"]):
            for el in st:
                n_el += 1
                k = el.get("k")
                if k not in KINDS:
                    bad.append(f"{cid} 段{i + 1}：知らない部品 {k!r}")
                    continue
                if el.get("role") and el["role"] not in J.ROLE:
                    bad.append(f"{cid} 段{i + 1}：役 {el['role']!r} が jiko_style.ROLE に無い")
                for ck in ("c", "lc"):
                    if el.get(ck) and el[ck] not in COLS:
                        bad.append(f"{cid} 段{i + 1}：色 {ck}={el[ck]!r} は {COLS} だけ（役の色は role で）")
                names = ([el["at"]] if isinstance(el.get("at"), str) else []) + [p for p in el.get("path", ()) if isinstance(p, str)]
                names += [p for p in (el.get("on") or ())[:2] if isinstance(p, str)]
                if isinstance(el.get("to"), str):
                    names.append(el["to"])
                if k == "arrow" and not isinstance(el.get("fr"), str) and not (el.get("dir") and el.get("src")):
                    bad.append(f"{cid} 段{i + 1}：矢印の尾が場所の名でない＝dir=True と src（向きの根拠）が要る")
                for nm in names:
                    if nm not in geo:
                        bad.append(f"{cid} 段{i + 1}：場所 {nm!r} が GEO に無い（確かめていない場所に点を置かない）")
                        continue
                    if "一般" in geo[nm]["how"]:
                        used_general = True
                if k == "x" and isinstance(el.get("at"), str) and el["at"] in geo and "報告書" not in geo[el["at"]]["how"]:
                    bad.append(f"{cid} 段{i + 1}：×は報告書の座標の場所だけ（{el['at']} は {geo[el['at']]['how']}）")
                if (el.get("t") or "") and k in ("line", "arrow") and not el.get("lab"):
                    bad.append(f"{cid} 段{i + 1}：線・矢印の札は lab（置き場）を書く")
        if used_general and "一般の座標" not in (sv.get("note") or ""):
            bad.append(f"{cid}：一般の座標の場所を使った＝note に「一般の座標」の断りが要る")
        # 幾何（描く関数と同じ箱＝inks_of）
        try:
            steps = inks_of(s)
        except Exception as e:      # noqa: BLE001
            bad.append(f"{cid}：描けない（{type(e).__name__}: {e}）")
            continue
        inner = (bx + EDGE, by + EDGE, bx + bw - EDGE, by + bh - EDGE)
        keep = {k: ibox_to_screen(b) for k, b in KEEP_OUT.items()}
        for i, inks in enumerate(steps):
            for nm, b in inks:
                if b[0] < inner[0] or b[1] < inner[1] or b[2] > inner[2] or b[3] > inner[3]:
                    bad.append(f"{cid} 段{i + 1}：{nm} の墨 {tuple(round(v) for v in b)} が額の内側 {inner} の外")
                for kk, kb in keep.items():
                    if _hit(b, kb):
                        why = "Google の決まり＝隠さない" if kk in HARD else "Google の操作の部品"
                        bad.append(f"{cid} 段{i + 1}：{nm} が {kk} の箱（{why}）に重なる")
        # 額の下：断り（左）と出典の行（右）
        cr = credit or sat_tab[code].get("credit", "")
        nw = fm.width(sv.get("note") or "", SUBTLE, "Noto")
        cw = fm.width(cr, SUBTLE, "Noto")
        if J.MG + nw + 40 > J.RIGHT - cw:
            bad.append(f"{cid}：額の下の断り（幅 {nw:.0f}）と出典の行（幅 {cw:.0f}）が近い・重なる")
    return bad, len(cuts), n_el
