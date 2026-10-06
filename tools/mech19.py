# -*- coding: utf-8 -*-
"""mech19.py — 19本目（サーフサイドのマンション崩壊のリメイク）「模式図」（2026-10-06 新設・⑤b-4）。

■ 何か
  18本目の `mech18`（仕組みの模式図）と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。
  案C の再現イラスト（illu の置き場 A1〜A5）ではない＝「再現」の札は出さない。左上に見る向き・左下に「模式」と出典。人は描かない。
  見え方（view）は29。上から見た敷地の図は **置き場 A2 の top と同じ並び**（`illu.A2T`・`A2_ROW`・`_a2_zone_fp`）を縮めて描く
  （`tp()`）＝絵のカットと模式図のカットで、塔・デッキ・駐車場・門・プランターの位置が食い違わない。

■ 位置の元（NIST の発表のスライド＝TF のコマ。🔴 18本目の型と同じく、記録の値は門番 check_mech の REC_M19 が別に持つ＝§5b-88）
  列（K・L・M…）と行（9.1・11.1・13.1・15）の交点は TF p9082（スライド74＝強さの不足の図）の格子から読んだ。
  A2 の模式の幅に合わせて、K より東はデッキの幅・K より西は駐車場の幅で伸ばした（`COLX`）。行は A2_ROW（12.1 と 14 は中間）。
  候補の6か所＝TF p9039（スライド48）・まわりの柱＝TF p9052（スライド56）・漏れの位置＝TF p9057（スライド58 の楕円）・
  見えた範囲＝TF p9069（スライド68）・11 の列と廊下＝TF p9127・p9134（スライド115・123）・Zone B＝TF p9139・p9144（スライド133・139）・
  梁 A と継ぎ目＝TF p9111・p9112（スライド92・93）・重ね＝TF p9090（スライド79）・プランター＝TF p9088（スライド78）・
  鉄筋＝TF p9085・p9087（スライド76・77）・87パーク＝TF p9169（スライド183）・揺れ＝TF p9173（スライド185）

■ SPEC の書き方（mech18 と同じ）
  fig=("m19", dict(view=…, start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…, d=…)), …],
                   rel=[dict(t="6か所", src="TR p1105")], note="…模式…", src="…"))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。札の数・時刻は `rel=` に同じ文字列（門番 check_mech の judge_m19）。
  ⚠️ 動く部品は段の層（札）より上に描かれる＝札は動く部品の通り道に置かない（`TAGS` の置き場は動く部品の外）
"""
from __future__ import annotations

import math

import jiko_style as J
import titan_fig as F
import illu as IL

ONOFF = ("off", "on")
A2T, A2_ROW, A2_COL, A1_COL = IL.A2T, IL.A2_ROW, IL.A2_COL, IL.A1_COL

# ── 意味の色（章の色に置き換わらない直書き）──
COL = dict(red="#e0503c", yel="#f2d03c", org="#f08c3c", grn="#5fbf8f", water="#6fb6e0", water_ln="#bfe3f5",
           conc="#8e979c", conc_ln="#3e464b", conc_lt="#b4babe", colg="#7fcf8f", colg_ln="#2f7a3f", bar="#2f7a3f",
           steel="#d8dde0", soil="#5c4d3a", soil_ln="#3a3024", lime="#a99f7c", lime_ln="#6d6449", sky="#101c26",
           tile="#e2b23c", paver="#7a3a2c", sand="#b9ab8c", memb="#141414", mark="#f2c14e", dim="#c9d3d9",
           white="#eef2f4", dark="#10161b", pit="#2a2219", ghost="#5a656c", blue="#5d92b4", lav="#a7a3d8",
           purple="#4a4a9e", green="#76a843", mesh="#e9eef2", rubble="#6b6f70")
INK = "#e3eaee"


def _P(ident, typ, pts=None, **kw):
    d = dict(id=ident, type=typ)
    if pts is not None:
        d["pts"] = [list(map(float, p)) for p in pts]
    d.update(kw)
    return d


def _rp(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _on(prev, st, f, v="on"):
    """この段で f が v になった（前の段は v でない）。"""
    return st.get(f) == v and prev.get(f) != v


def _t(x, y, t, size=24, col=INK, anchor="start"):
    return F.txt(x, y, t, size, col, anchor=anchor)


def _ring(x, y, r, col, w=5.0):
    return F.circ(x, y, r, "none", COL["dark"], w + 4) + F.circ(x, y, r, "none", col, w)


def _dot(x, y, r, col):
    return F.circ(x, y, r, col, COL["dark"], 2.5)


def _down(x, y0, y1, col, sw=6, head=20):
    return F.arrow(x, y0, x, y1, col, sw, head)


# ══════════════════════════════════════════════════════════
#  上から見た敷地（北が上）＝A2 の top を縮めた並び
# ══════════════════════════════════════════════════════════
TS, TY0 = 0.80, 300.0
TOPBOX = (F.BX0, 262.0, F.BX1, 862.0)
# 列の x（A2 の座標）＝TF p9082 の格子（スライドの x：F.1 165・G.1 225・I 303・K 393・L 478・M 567・N 643・O 722・O.1 770）を
#   K より西は駐車場の幅（スライド 230→393 ＝ A2 640→930）、K より東はデッキの幅（K→L ＝ 85 → 80）で伸ばした
COLX = {"F.1": 524.0, "G.1": 631.0, "I": 770.0, "K": 930.0, "L": 1010.0, "M": 1094.0, "N": 1165.0, "O": 1239.0,
        "O.1": 1284.0, "P": 1375.0}
ROWY = dict(A2_ROW, **{"12.1": 515.0, "14": 625.0})
DRIVE = (460.0, 600.0, 640.0, 800.0)          # 入口の車道（駐車場の南西の角・位置は模式＝TF p9069 の空から見た写真の西の角）
PLANTERS = [(975.0 + 80.0 * i, 366.0, 1033.0 + 80.0 * i, 420.0) for i in range(6)]   # 北の縁のプランターの列（TF p9088 の赤い点線）
LEAK = (1155.0, 478.0, 55.0, 35.0)            # 9時間前の漏れ（TF p9057 の楕円＝M と N のあいだ・11.1 の少し南）
VISIBLE = [(930.0, 432.0), (1113.0, 432.0), (1113.0, 350.0), (1460.0, 350.0), (1460.0, 800.0), (930.0, 800.0)]  # TF p9069
CAND = [("K", "13.1"), ("L", "13.1"), ("M", "13.1"), ("K", "15"), ("L", "15"), ("M", "15")]                  # TF p9039
FIRST2 = [("K", "13.1"), ("L", "13.1")]
AROUND = [("I", "12.1"), ("K", "11.1"), ("L", "11.1"), ("M", "13.1"), ("K", "15"), ("L", "15")]              # TF p9052
GRAY = [(785.0, 505.0), (930.0, 472.0), (1010.0, 472.0), (1082.0, 570.0), (1010.0, 668.0), (930.0, 668.0)]
# 強さの不足（TF p9082＝建てた当時の決まり）：● 継ぎ目（red＝ひどい・yel＝中くらい）
CODE_DOTS = dict(red=[("K", "13.1"), ("L", "13.1"), ("M", "13.1"), ("G.1", "15"), ("I", "15"), ("K", "15"), ("L", "15"),
                      ("M", "15")],
                 yel=[("N", "13.1"), ("O", "13.1"), ("O.1", "13.1"), ("N", "15")])
# ↔ 曲げ（スライドの座標 x・y・向き H/V・色）＝下の `_slide_xy` で A2 へ
CODE_FLEX = [(303, 187, "V", "red"), (418, 200, "V", "yel"), (390, 205, "H", "yel"), (478, 205, "H", "yel"),
             (567, 205, "H", "yel"), (643, 203, "H", "yel"), (443, 222, "H", "red"), (605, 222, "H", "red"),
             (737, 200, "V", "red"), (773, 200, "V", "red"), (824, 200, "V", "red"), (312, 240, "V", "yel"),
             (350, 232, "H", "yel"), (303, 283, "V", "yel"), (303, 332, "H", "yel"), (405, 300, "V", "red"),
             (500, 295, "V", "red"), (588, 295, "V", "red"), (657, 305, "V", "yel"), (715, 316, "H", "red"),
             (790, 316, "H", "red"), (865, 306, "H", "red"), (478, 318, "H", "yel"), (567, 320, "H", "yel"),
             (390, 360, "V", "red"), (478, 360, "V", "red"), (567, 360, "V", "red"), (643, 350, "V", "red"),
             (722, 350, "V", "red"), (790, 350, "V", "red"), (866, 350, "V", "red"), (236, 418, "V", "yel"),
             (313, 415, "V", "red"), (400, 418, "V", "red"), (468, 418, "V", "red"), (543, 418, "V", "red"),
             (622, 418, "V", "red"), (378, 438, "H", "yel"), (220, 475, "V", "red"), (300, 475, "V", "red"),
             (380, 475, "V", "red"), (455, 475, "V", "yel"), (528, 475, "V", "red")]


def _slide_xy(xs, ys):
    """TF p9082 のスライドの座標（1200px の縮小）→ A2 の座標。"""
    x = 640.0 + (xs - 230.0) * 290.0 / 163.0 if xs <= 393 else 930.0 + (xs - 393.0) * 0.94
    pts = [(143.0, 350.0), (222.0, 460.0), (300.0, 570.0), (415.0, 680.0), (475.0, 737.0)]
    for (a, A), (b, B) in zip(pts, pts[1:]):
        if ys <= b or (b, B) == pts[-1]:
            y = A + (ys - a) * (B - A) / (b - a)
            break
    return x, y


def tp(x, y):
    return (960.0 + (x - 960.0) * TS, TY0 + (y - 190.0) * TS)


def gp(c, r):
    return tp(COLX[c], ROWY[r])


def _tz(pts, fill, ln="#2a333a", sw=2.5, op=None, dash=None):
    return F.poly([tp(*p) for p in pts], fill, ln, sw, True, dash, op)


def _trect(r, fill, ln=None, sw=2.5, op=None, dash=None):
    a, b = tp(r[0], r[1]), tp(r[2], r[3])
    return F.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill, ln, sw, 0, op, dash)


def _top_bg():
    x0, y0, x1, y1 = TOPBOX
    s0, s1 = tp(310, 0)[0], tp(430, 0)[0]
    d0, d1 = tp(1460, 0)[0], tp(1610, 0)[0]
    g = [F.rect(x0, y0, x1 - x0, y1 - y0, A2_COL["ground"]), F.rect(s0, y0, s1 - s0, y1 - y0, A2_COL["street"]),
         F.rect(d0, y0, d1 - d0, y1 - y0, A2_COL["sand"]), F.rect(d1, y0, x1 - d1, y1 - y0, A2_COL["sea"])]
    for k in range(4):
        g.append(F.line(d1 + 50 + 80 * k, y0 + 50, d1 + 50 + 80 * k, y1 - 8, A2_COL["sea_ln"], 2, "18 26", 0.6))
    g.append(_t((s0 + s1) / 2, y0 + 30, "通り", 22, J.TICK, "middle"))
    g.append(_t(d1 + 16, y0 + 30, "海", 22, J.TICK))
    g.append(_t(x1 - 14, y0 + 30, "北↑", 24, INK, "end"))
    return g


def _top_site(op=1.0, pool=True, holes=False, lab=True):
    park, deck = IL._a2_zone_fp()
    w, m, e = IL._a2_tower_fp()
    g = [_tz(park, A2_COL["park"], op=op), _tz(deck, A2_COL["deck"], op=op)]
    if holes:
        g += [_trect(IL.A2_HOLE_PARK, A2_COL["hole"], A2_COL["hole_ln"]), _trect(IL.A2_HOLE_DECK, A2_COL["hole"], A2_COL["hole_ln"])]
    if pool:
        g.append(_top_pool())
    g += [_tz(w, A1_COL["west"]), _tz(m, A1_COL["mid"]), _tz(e, A1_COL["east"])]
    if lab:      # ⑤b-4 の layout：真ん中に置くと c610 の見通しの扇が字を通った＝東の部分へ
        cx, cy = tp(1300.0, 262.0)
        g.append(_t(cx, cy, "塔", 26, INK, "middle"))
    return g


def _top_pool():
    x0, y0, x1, y1 = IL.A2_POOL
    tx, ty, tr = IL.A2_TUB
    a, b = tp(x0, y0), tp(x1, y1)
    c = tp(tx, ty)
    return (F.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], A2_COL["pool"], A2_COL["pool_ln"], 3, 8)
            + F.circ(c[0], c[1], tr * TS, A2_COL["pool"], A2_COL["pool_ln"], 3))


def _top_fence():
    K = A2T["K"]
    g0, g1 = IL.A2_GATE
    a, b, c, d = tp(K, A2_ROW["11.1"]), tp(K, g0), tp(K, g1), tp(K, A2T["south"] - 10)
    return (F.line(a[0], a[1], b[0], b[1], A2_COL["fence"], 3, "3 5") + F.line(c[0], c[1], d[0], d[1], A2_COL["fence"], 3, "3 5")
            + F.rect(b[0] - 4, b[1], 8, c[1] - b[1], A2_COL["fence"], COL["dark"], 1.5))


def _top_planter():
    return _trect(IL.A2_PLANTER, A2_COL["planter"], "#3b3a36", 2.5)


def _top_grid(cols, rows, lab=True, rowlab=True):
    g = []
    ys, ye = tp(0, A2T["ts"])[1], tp(0, A2T["south"])[1]
    for c in cols:
        x = tp(COLX[c], 0)[0]
        g.append(F.line(x, ys, x, ye, "#dfe6ea", 1.5, "6 8", 0.6))
        if lab:
            g.append(_t(x, ye + 26, c, 22, INK, "middle"))
    for r in rows:
        y = tp(0, ROWY[r])[1]
        xa = tp(A2T["x0"] if ROWY[r] > A2T["legs"] else A2T["legx"], 0)[0]
        g.append(F.line(xa, y, tp(A2T["x1"], 0)[0], y, "#dfe6ea", 1.5, "6 8", 0.6))
        if lab and rowlab:
            g.append(_t(tp(A2T["x1"], 0)[0] + 10, y + 8, r, 22, INK))
    return g


def _in_zone(x, y):
    T = A2T
    if T["K"] <= x <= T["x1"] and T["ts"] < y <= T["south"]:
        return True
    if T["legx"] <= x < T["K"] and T["ts"] < y <= T["south"]:
        return True
    return T["x0"] <= x < T["legx"] and T["legs"] < y <= T["south"]


def basement_cols():
    """地下の柱（行 9.1・11.1・13.1・15 × 列）のうち、デッキと駐車場の下の点（A2 の座標）。"""
    out = []
    for r in ("11.1", "13.1", "15"):
        for c in COLX:
            x, y = COLX[c], ROWY[r]
            if _in_zone(x, y):
                out.append((c, r, x, y))
    return out


def _col_sq(x, y, col="#c9d3d9", s=12.0):
    X, Y = tp(x, y)
    return F.rect(X - s / 2, Y - s / 2, s, s, "#3a4248", col, 2, 0, None, "4 3")


def _weight(X, Y, s=1.0):
    pts = [(X - 13 * s, Y + 10 * s), (X + 13 * s, Y + 10 * s), (X + 8 * s, Y - 8 * s), (X - 8 * s, Y - 8 * s)]
    return F.poly(pts, "#d9d0c0", COL["dark"], 2, True) + F.circ(X, Y - 12 * s, 5 * s, "none", "#d9d0c0", 2.5)


def _palm(X, Y, r=19.0):
    pts = []
    for k in range(16):
        a = math.pi * 2 * k / 16
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((X + rr * math.cos(a), Y + rr * math.sin(a)))
    return pts


# ── 各見え方（上から）──
def site_base(st0):
    return _top_bg() + _top_site(op=0.45, pool=False)


def site_stage(prev, st):
    g = []
    if _on(prev, st, "zone"):
        park, deck = IL._a2_zone_fp()
        g += [_tz(park, A2_COL["park"]), _tz(deck, A2_COL["deck"])]
        g += [_tz(deck, "none", COL["mark"], 4)]
    if _on(prev, st, "cols"):
        g += [_col_sq(x, y) for _c, _r, x, y in basement_cols()]
    if _on(prev, st, "pool"):
        g.append(_top_pool())
    return g


def planter_base(st0):
    return _top_bg() + _top_site() + [_top_planter(), _top_fence()]


def planter_parts(st):
    out = []
    for i, (x0, y0, x1, y1) in enumerate(PLANTERS):
        X, Y = tp((x0 + x1) / 2, (y0 + y1) / 2)
        a = 1.0 if (st["box"] == "on" and st["palm"] == "on") else 0.0
        out.append(_P(f"palm{i}", "poly", _palm(X, Y), fill="#3f8f4a", stroke="#1d4a24", w=2, alpha=a))
    return out


def planter_stage(prev, st):
    g = []
    if _on(prev, st, "box"):
        for r in PLANTERS:
            g.append(_trect(r, A2_COL["planter"], "#3b3a36", 2.5))
            g.append(_trect((r[0] + 6, r[1] + 6, r[2] - 6, r[3] - 6), "#4a4a3a"))
        a, b = tp(PLANTERS[0][0] - 10, PLANTERS[0][1] - 10), tp(PLANTERS[-1][2] + 10, PLANTERS[0][3] + 10)
        g.append(F.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], "none", COL["dark"], 9, 4))
        g.append(F.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], "none", COL["red"], 5, 4, None, "16 9"))
    if st["weight"] in ("plant", "both") and prev.get("weight") not in ("plant", "both"):
        for (x0, y0, x1, y1) in PLANTERS[::2]:
            X, Y = tp((x0 + x1) / 2, y1 + 22)
            g.append(_weight(X, Y + 6))
    if _on(prev, st, "weight", "both"):
        park, deck = IL._a2_zone_fp()
        x0, y0 = tp(A2T["K"], 440)
        x1, y1 = tp(A2T["x1"], A2T["south"])
        for k in range(int((x1 - x0) // 22)):
            g.append(F.line(x0 + 22 * k, y0, x0 + 22 * k, y1, "#c98a6a", 1.2, None, 0.45))
        for k in range(int((y1 - y0) // 22)):
            g.append(F.line(x0, y0 + 22 * k, x1, y0 + 22 * k, "#c98a6a", 1.2, None, 0.45))
        for x, y in ((1000.0, 700.0), (1130.0, 740.0), (1290.0, 700.0), (1420.0, 620.0)):
            X, Y = tp(x, y)
            g.append(_weight(X, Y))
    return g


def dig_base(st0):
    return _top_bg() + _top_site() + [_top_planter(), _top_fence()] + [_trect(r, A2_COL["planter"], "#3b3a36") for r in PLANTERS]


def dig_stage(prev, st):
    g = []
    if _on(prev, st, "under"):
        g += [_col_sq(x, y, COL["mark"]) for _c, _r, x, y in basement_cols()]
    if _on(prev, st, "strip"):
        park, deck = IL._a2_zone_fp()
        for z in (park, deck):
            g.append(_tz(z, COL["mark"], COL["mark"], 4, 0.30, "14 8"))
    if _on(prev, st, "name"):
        g.append(_trect(DRIVE, "none", COL["white"], 4, None, "10 7"))
    return g


def cand_base(st0):
    return (_top_bg() + _top_site() + [_top_planter(), _top_fence()]
            + _top_grid(("K", "L", "M"), ("11.1", "13.1", "15")))


def cand_stage(prev, st):
    g = []
    if _on(prev, st, "cand"):
        g += [_dot(*gp(c, r), 12, COL["yel"]) for c, r in CAND]
    if _on(prev, st, "red"):
        g += [_ring(*gp(c, r), 24, COL["red"]) for c, r in FIRST2]
    return g


def _punched(c, r):
    X, Y = gp(c, r)
    return (F.circ(X, Y, 15, COL["red"], COL["dark"], 2.5) + F.line(X - 8, Y - 8, X + 8, Y + 8, COL["white"], 3.5)
            + F.line(X - 8, Y + 8, X + 8, Y - 8, COL["white"], 3.5))


def seq_base(st0):
    return (_top_bg() + _top_site() + [_top_planter(), _top_fence()]
            + _top_grid(("I", "K", "L", "M"), ("11.1", "13.1", "15")))


def seq_stage(prev, st):
    g = []
    if _on(prev, st, "around"):
        g.append(F.poly([tp(*p) for p in GRAY], "#c9cfd2", COL["dark"], 2, True, None, 0.45))
        g += [_ring(*gp(c, r), 17, COL["org"], 4.5) for c, r in AROUND]
    if _on(prev, st, "first"):
        g.append(_punched("K", "13.1"))
    if _on(prev, st, "second"):
        g.append(_punched("L", "13.1"))
    return g


def dmg_base(st0):
    # 行の番号は右の札の引き出し線が横切る（layout）＝この図は列の名だけ
    return (_top_bg() + _top_site() + [_top_planter(), _top_fence()]
            + _top_grid(("K", "L", "M", "N"), ("11.1", "13.1"), rowlab=False))


DMG_PTS = dict(gate=(930.0, 548.0), planter=(975.0, 590.0), water=(1010.0, 570.0), leak=(1155.0, 478.0))


def dmg_stage(prev, st):
    g = []
    if _on(prev, st, "leak"):
        x, y, rx, ry = LEAK
        X, Y = tp(x, y)
        g.append(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{rx * TS:.1f}" ry="{ry * TS:.1f}" fill="{COL["water"]}" '
                 f'fill-opacity="0.35" stroke="{COL["water_ln"]}" stroke-width="4" stroke-dasharray="10 6"/>')
    if _on(prev, st, "pts"):
        for k, (x, y) in DMG_PTS.items():
            X, Y = tp(x, y)
            g.append(_dot(X, Y, 10, COL["water"] if k in ("water", "leak") else COL["mark"]))
    return g


def sight_base(st0):
    return _top_bg() + _top_site() + [_top_planter(), _top_fence()]


def sight_stage(prev, st):
    g = []
    if _on(prev, st, "vis"):
        g.append(F.poly([tp(*p) for p in VISIBLE], COL["grn"], COL["grn"], 4, True, None, 0.45))
    if _on(prev, st, "lobby"):
        x0, y0, x1, y1 = IL.A2_LOBBY
        g.append(_trect(IL.A2_LOBBY, A2_COL["lobby"], COL["mark"], 4, 0.55))
        for k in range(3):                     # 風の印（曲がった矢印・模式）
            X, Y = tp(x0 + 60 + 80 * k, (y0 + y1) / 2)
            g.append(F.poly([(X - 22, Y + 6), (X - 6, Y - 6), (X + 10, Y + 4), (X + 24, Y - 4)], "none", COL["white"], 3))
    if _on(prev, st, "sound"):
        X, Y = tp(IL.A2_LOBBY[2] - 40, IL.A2_LOBBY[1] - 10)
        for k, r in enumerate((18, 32, 46)):
            g.append(F.poly(F._arc(X, Y, r, -150, -30, 12), "none", COL["white"], 3, op=0.9 - 0.2 * k))
    return g


def code_base(st0):
    return (_top_bg() + _top_site(pool=False)
            + _top_grid(("G.1", "I", "K", "L", "M", "N", "O", "O.1"), ("9.1", "11.1", "13.1", "15")))


def code_stage(prev, st):
    g = []
    if _on(prev, st, "flex"):
        for xs, ys, o, c in CODE_FLEX:
            X, Y = tp(*_slide_xy(xs, ys))
            col = COL["red"] if c == "red" else COL["yel"]
            if o == "H":
                g.append(F.arrow(X - 4, Y, X + 18, Y, col, 4, 10) + F.arrow(X + 4, Y, X - 18, Y, col, 4, 10))
            else:
                g.append(F.arrow(X, Y - 4, X, Y + 18, col, 4, 10) + F.arrow(X, Y + 4, X, Y - 18, col, 4, 10))
    if _on(prev, st, "dots"):
        for c, r in CODE_DOTS["red"]:
            g.append(_dot(*gp(c, r), 11, COL["red"]))
        for c, r in CODE_DOTS["yel"]:
            g.append(_dot(*gp(c, r), 11, COL["yel"]))
        # 凡例（右の海の側）
        x, y = 1500.0, 640.0
        g.append(F.rect(x - 14, y - 34, 360, 150, COL["dark"], "#5d6a72", 2, 6, 0.9))
        g.append(_dot(x + 10, y - 6, 10, COL["red"]) + _t(x + 32, y + 2, "継ぎ目（ひどい）", 22))
        g.append(_dot(x + 10, y + 30, 10, COL["yel"]) + _t(x + 32, y + 38, "継ぎ目（中くらい）", 22))
        g.append(F.arrow(x - 4, y + 72, x + 26, y + 72, COL["red"], 4, 10) + _t(x + 40, y + 80, "曲げ（矢印）", 22))
    return g


def _mesh(pts, step=14.0):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    g = []
    k = x0 + step
    while k < x1:
        g.append(F.line(k, y0, k, y1, COL["mesh"], 1, None, 0.28))
        k += step
    k = y0 + step
    while k < y1:
        g.append(F.line(x0, k, x1, k, COL["mesh"], 1, None, 0.28))
        k += step
    return g


MODEL_LOBBY = (640.0, 300.0, 1460.0, 350.0)    # 1階の床の一部（ロビー）＝TF p9096 の薄紫の帯


def model_base(st0):
    park, deck = IL._a2_zone_fp()
    w, m, e = IL._a2_tower_fp()
    g = _top_bg() + [_tz(w, A1_COL["west"], op=0.5), _tz(m, A1_COL["mid"], op=0.5), _tz(e, A1_COL["east"], op=0.5)]
    for z, c in ((park, COL["purple"]), (deck, COL["green"])):
        g.append(_tz(z, c))
        g += _mesh([tp(*p) for p in z if True])
    g.append(_trect(MODEL_LOBBY, COL["lav"], COL["dark"], 2))
    a, b = tp(MODEL_LOBBY[0], MODEL_LOBBY[1]), tp(MODEL_LOBBY[2], MODEL_LOBBY[3])
    g += _mesh([a, b])
    return g


def model_stage(prev, st):
    g = []
    if _on(prev, st, "calc"):
        for _c, _r, x, y in basement_cols():
            X, Y = tp(x, y)
            g.append(_ring(X, Y, 11, COL["mark"], 4))
    return g


# 塔の階の平面（TF p9134＝スライド123 の平面を 1.25 倍）
def cp(xs, ys):
    return (400.0 + (xs - 255.0) * 1.25, 270.0 + (ys - 160.0) * 1.25)


CAM_X = {"I": 515.0, "K": 580.0, "L": 640.0, "M": 710.0}
CAM_Y = {"4": 290.0, "8": 352.0, "9.1": 420.0}
CAM_UNIT = (640.0, 310.0, 710.0, 420.0)        # 11 の列（L と M のあいだ・廊下の南〜9.1）
CAM_EYE = (675.0, 400.0)                        # カメラ（位置は模式・向き＝北＝TR0337「L の線は左＝西」）


def cam_base(st0):
    out = [(255, 160), (885, 160), (885, 420), (445, 420), (445, 620), (255, 620)]
    g = [F.rect(F.BX0, 262.0, F.BW, 600.0, A2_COL["ground"]),
         F.poly([cp(*p) for p in out], A1_COL["mid"], COL["dark"], 3, True)]
    for k in range(8):                                     # 部屋の仕切り（模式）
        x = cp(255 + 78 * k, 0)[0]
        g.append(F.line(x, cp(0, 160)[1], x, cp(0, 290)[1] - 6, "#8a979e", 1.5, None, 0.5))
    ye = cp(0, 160)[1]
    for c, xs in CAM_X.items():
        x = cp(xs, 0)[0]
        g.append(F.line(x, ye, x, cp(0, 420)[1], "#dfe6ea", 1.5, "6 8", 0.7))
        g.append(_t(x, ye + 28, c, 22, INK, "middle"))
    for r, ys in CAM_Y.items():
        y = cp(0, ys)[1]
        g.append(F.line(cp(445, 0)[0], y, cp(885, 0)[0], y, "#dfe6ea", 1.5, "6 8", 0.7))
        g.append(_t(cp(885, 0)[0] + 12, y + 8, r, 22, INK))
    for c, xs in CAM_X.items():
        for r, ys in CAM_Y.items():
            X, Y = cp(xs, ys)
            g.append(F.rect(X - 7, Y - 7, 14, 14, "#2a3238", "#c9d3d9", 2))
    g.append(_t(cp(300, 0)[0], cp(0, 560)[1], "西の部分", 22, INK))
    g.append(_t(cp(885, 0)[0] - 10, cp(0, 160)[1] + 28, "東", 22, INK, "end"))
    return g


def cam_stage(prev, st):
    g = []
    if _on(prev, st, "unit"):
        a, b = cp(CAM_UNIT[0], CAM_UNIT[1]), cp(CAM_UNIT[2], CAM_UNIT[3])
        g.append(F.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], COL["blue"], COL["water_ln"], 3, 0, 0.6))
        X, Y = cp(*CAM_EYE)
        g.append(F.poly([(X, Y), (X - 34, Y - 92), (X + 34, Y - 92)], COL["mark"], None, None, True, None, 0.35))
        g.append(F.rect(X - 12, Y - 8, 24, 16, COL["dark"], COL["mark"], 3, 3))
    if _on(prev, st, "move"):
        for r in ("8", "9.1"):
            X, Y = cp(CAM_X["L"], CAM_Y[r])
            g.append(_dot(X, Y, 13, COL["red"]) + F.arrow(X, Y - 7, X, Y + 9, COL["white"], 3, 8))
            X, Y = cp(CAM_X["M"], CAM_Y[r])
            g.append(F.line(X - 9, Y - 9, X + 9, Y + 9, COL["water_ln"], 4) + F.line(X - 9, Y + 9, X + 9, Y - 9, COL["water_ln"], 4))
    return g


NORTH_EYE = (980.0, 165.0)                       # 北にいた人（位置は模式）
NORTH_FAR = ((900.0, 650.0), (1060.0, 650.0))    # 見通しの奥（模式）


def north_base(st0):
    return _top_bg() + _top_site(holes=True)


def north_stage(prev, st):
    g = []
    if _on(prev, st, "eye"):
        e = tp(*NORTH_EYE)
        a, b = tp(*NORTH_FAR[0]), tp(*NORTH_FAR[1])
        g.append(F.poly([e, a, b], COL["mark"], COL["mark"], 2, True, "10 7", 0.28))
        g.append(F.circ(e[0], e[1], 13, COL["white"], COL["dark"], 3) + F.circ(e[0], e[1], 5, COL["dark"]))
    if _on(prev, st, "debris"):
        for k, (x, y) in enumerate(((930, 668), (965, 690), (1000, 662), (1035, 700), (980, 720), (1050, 676))):
            X, Y = tp(x, y)
            g.append(F.poly([(X - 12, Y + 6), (X - 4, Y - 9), (X + 11, Y - 5), (X + 9, Y + 8)], COL["rubble"], "#c9cfd2", 2, True))
    return g


def sat_base(st0):
    return _top_bg() + _top_site(lab=False)        # 区画と輪が「塔」の字を覆う（layout）＝字は出さない


SAT_CELL = 40.0


def sat_cells():
    x0, y0, x1, y1 = TOPBOX
    out = []
    y = y0 + 50
    while y + SAT_CELL <= y1 - 10:
        x = x0 + 10
        while x + SAT_CELL <= tp(1610, 0)[0]:
            out.append((x, y))
            x += SAT_CELL
        y += SAT_CELL
    return out


SAT_NEUTRAL = "#8fa3ad"


def sat_stage(prev, st):
    g = []
    if _on(prev, st, "sat"):
        g += [F.rect(x + 1, y + 1, SAT_CELL - 2, SAT_CELL - 2, SAT_NEUTRAL, None, 0, 2, 0.16) for x, y in sat_cells()]
        X, Y = 1700.0, 330.0                                    # 人工衛星（模式）
        g.append(F.rect(X - 14, Y - 14, 28, 28, COL["steel"], COL["dark"], 2, 3)
                 + F.rect(X - 64, Y - 9, 44, 18, COL["blue"], COL["dark"], 2) + F.rect(X + 20, Y - 9, 44, 18, COL["blue"], COL["dark"], 2))
        g.append(F.line(X, Y + 16, X - 60, Y + 90, COL["mark"], 2, "6 6", 0.7))
    if _on(prev, st, "near"):
        X, Y = tp(960.0, 420.0)
        g.append(_ring(X, Y, 300 * TS, COL["mark"], 4))
    return g


# ══════════════════════════════════════════════════════════
#  横から（断面・立面）
# ══════════════════════════════════════════════════════════
def _ground_bg(y0=262.0, y1=862.0, col=None):
    return F.rect(F.BX0, y0, F.BW, y1 - y0, col or COL["sky"])


# ── flat（c207）＝フラットプレート ──
FLAT_COLS = (380.0, 700.0, 1020.0, 1340.0)
FLAT_FLOORS = ((450.0, 476.0), (610.0, 636.0), (770.0, 796.0))
FLAT_X = (260.0, 1460.0)
FLAT_CW = 36.0


def flat_base(st0):
    g = [_ground_bg(), F.rect(F.BX0, 846, F.BW, 16, "#2c3236")]
    for x in FLAT_COLS:
        g.append(F.rect(x - FLAT_CW / 2, 400, FLAT_CW, 446, COL["conc"], COL["conc_ln"], 2))
    for y0, y1 in FLAT_FLOORS:
        g.append(F.rect(FLAT_X[0], y0, FLAT_X[1] - FLAT_X[0], y1 - y0, COL["conc_lt"], COL["conc_ln"], 2))
    return g


def flat_joints():
    return [(x, (y0 + y1) / 2.0) for x in FLAT_COLS for y0, y1 in FLAT_FLOORS]


def flat_stage(prev, st):
    g = []
    if _on(prev, st, "plate"):
        for y0, y1 in FLAT_FLOORS:
            g.append(F.rect(FLAT_X[0], y0, FLAT_X[1] - FLAT_X[0], y1 - y0, "none", COL["white"], 3, 0, 0.8))
    if _on(prev, st, "joint"):
        for x, y in flat_joints():
            g.append(F.rect(x - FLAT_CW / 2 - 6, y - 19, FLAT_CW + 12, 38, COL["mark"], COL["dark"], 2, 4, 0.9))
    return g


# ── punch（c801・c804・c814）＝柱と床の板の継ぎ目（横から切った所）──
PU = dict(cx=960.0, cw=120.0, top=520.0, bot=600.0, x0=300.0, x1=1620.0, drop=110.0, bar=536.0, cone=110.0)


def _pu_side(sg):
    c, h = PU["cx"], PU["cw"] / 2
    if sg < 0:
        return _rp(PU["x0"], PU["top"], c - h, PU["bot"])
    return _rp(c + h, PU["top"], PU["x1"], PU["bot"])


def punch_parts(st):
    dy = PU["drop"] if st["drop"] == "on" else 0.0
    c, h = PU["cx"], PU["cw"] / 2
    out = []
    for sg, nm in ((-1, "l"), (1, "r")):
        out.append(_P(f"slab_{nm}", "poly", _pu_side(sg), fill=COL["conc_lt"], stroke=COL["conc_ln"], w=2, dy=dy))
        xa = c + sg * h
        bx = (PU["x0"] + 20, xa) if sg < 0 else (xa, PU["x1"] - 20)
        out.append(_P(f"bar_{nm}", "line", [(bx[0], PU["bar"]), (bx[1], PU["bar"])], stroke="#5a6470", w=5, dy=dy))
        top = (xa + sg * PU["cone"], PU["top"])
        bot = (xa, PU["bot"])
        thin = 1.0 if st["crack"] == "on" else 0.0
        wide = 1.0 if st["crack"] == "wide" else 0.0
        out.append(_P(f"crk_{nm}", "line", [top, bot], stroke=COL["red"], w=4, alpha=thin, dy=dy))
        out.append(_P(f"crw_{nm}", "line", [top, bot], stroke=COL["red"], w=11, alpha=wide, dy=dy))
    return out


def punch_base(st0):
    c, h = PU["cx"], PU["cw"] / 2
    return [_ground_bg(), F.rect(c - h, 300, PU["cw"], 560, COL["conc"], COL["conc_ln"], 2),
            F.line(c - h + 6, PU["bar"], c + h - 6, PU["bar"], "#5a6470", 5)]


PU_LOAD_X = (560.0, 700.0, 1220.0, 1360.0)


def punch_stage(prev, st):
    g = []
    c, h = PU["cx"], PU["cw"] / 2
    if _on(prev, st, "load"):
        g += [_down(x, 420, 512, COL["mark"]) for x in PU_LOAD_X]
    if _on(prev, st, "react"):
        g.append(F.arrow(c, 800, c, 640, COL["white"], 8, 24))
    if _on(prev, st, "hook"):
        for sg in (-1, 1):
            xa = c + sg * h
            g.append(F.poly([(xa - sg * 6, PU["bar"]), (xa + sg * 26, PU["bar"] + 18), (xa + sg * 40, PU["bar"] + 60),
                             (xa + sg * 44, PU["bar"] + PU["drop"])], "none", "#5a6470", 5))
            g.append(F.poly([(xa + sg * 20, PU["bar"] + 30), (xa + sg * 44, PU["bar"] + 50)], "none", COL["mark"], 3))
    if _on(prev, st, "scis"):
        x0, y0 = 1420.0, 262.0
        g.append(F.rect(x0, y0, 410, 190, COL["dark"], "#5d6a72", 2, 8, 0.92))
        g.append(F.rect(x0 + 30, y0 + 86, 180, 34, "#e9e2cf", COL["dark"], 2) + F.rect(x0 + 210, y0 + 106, 170, 34, "#e9e2cf", COL["dark"], 2))
        g.append(F.line(x0 + 150, y0 + 40, x0 + 300, y0 + 150, COL["steel"], 7) + F.line(x0 + 150, y0 + 170, x0 + 300, y0 + 60, COL["steel"], 7))
        g.append(F.circ(x0 + 135, y0 + 30, 16, "none", COL["red"], 6) + F.circ(x0 + 135, y0 + 180, 16, "none", COL["red"], 6))
    if _on(prev, st, "shear"):
        g.append(F.arrow(c - h + 20, 840, c - h + 20, 700, COL["white"], 7, 22))
        g.append(F.arrow(c - h - 70, PU["top"] + PU["drop"] - 70, c - h - 70, PU["bot"] + PU["drop"] + 60, COL["red"], 7, 22))
    if _on(prev, st, "gauge"):
        top = (c - h - PU["cone"], PU["top"])
        bot = (c - h, PU["bot"])
        mx, my = (top[0] + bot[0]) / 2, (top[1] + bot[1]) / 2
        g.append(F.line(mx - 28, my + 24, mx + 28, my - 24, COL["white"], 3) + F.line(mx - 20, my - 30, mx - 36, my - 10, COL["white"], 3)
                 + F.line(mx + 36, my + 10, mx + 20, my + 30, COL["white"], 3))
    return g


# ── gspan（c507・c508）＝西を向いて見た地下の駐車場（右が北）・プールデッキの床 ──
GS = dict(wall=200.0, top=440.0, bot=470.0, floor=800.0, cw=34.0, sag=16.0)
GS_ROW = {"15": 520.0, "13.1": 860.0, "11.1": 1200.0, "9.1": 1540.0}
GS_X = (226.0, 520.0, 860.0, 1200.0, 1540.0)


def _gs_slab(dy_mid):
    top = [(x, GS["top"] + (dy_mid if x == GS_ROW["13.1"] else 0.0)) for x in GS_X]
    bot = [(x, GS["bot"] + (dy_mid if x == GS_ROW["13.1"] else 0.0)) for x in reversed(GS_X)]
    return top + bot


def gspan_parts(st):
    return [_P("slab", "poly", _gs_slab(GS["sag"] if st["sag"] == "on" else 0.0), fill=A2_COL["deck"], stroke=COL["conc_ln"], w=2)]


def _inset(y, xline):
    """左上の小さな地図＝上から見た敷地（A2 の top を縮めた）＋切り口（xline の線）＋目の印（西を向く）。illu.a3_inset_svg と同じ式。"""
    x0, w = 72.0, 260.0
    sx = w / (A2T["x1"] + 160 - (A2T["x0"] - 60))
    ox = A2T["x0"] - 60

    def p(px, py):
        return (x0 + (px - ox) * sx, y + (py - A2T["tn"] + 30) * sx)
    h = (A2T["south"] + 40 - A2T["tn"] + 30) * sx
    wt, mt, et = IL._a2_tower_fp()
    park, deck = IL._a2_zone_fp()

    def poly(pts, fill):
        return F.poly([p(*q) for q in pts], fill, COL["dark"], 1.2, True)
    a, b = p(xline, A2T["ts"] - 20), p(xline, A2T["south"] + 10)
    ex, ey = p(xline + 90, (A2T["ts"] + A2T["south"]) / 2.0)
    c = COL["mark"]
    return (F.rect(x0, y, w, h, A2_COL["ground"]) + poly(park, A2_COL["park"]) + poly(deck, A2_COL["deck"])
            + poly(wt, A1_COL["west"]) + poly(mt, A1_COL["mid"]) + poly(et, A1_COL["east"])
            + F.line(a[0], a[1], b[0], b[1], COL["dark"], 7) + F.line(a[0], a[1], b[0], b[1], c, 4)
            + F.circ(ex, ey, 5, COL["white"], COL["dark"], 2) + F.arrow(ex - 6, ey, ex - 30, ey, c, 3, 9)
            + _t(x0 + w - 8, y + 22, "北↑", 18, INK, "end") + F.rect(x0, y, w, h, "none", "#e3eaee", 2))


def gspan_base(st0):
    # ⑤b-4 の下見：左上の小さな地図（y 262〜407）に壁と床が重なった＝壁の上の端を 418 へ・「南」は壁の左
    g = [_ground_bg(), F.rect(GS["wall"], 418, 26, GS["floor"] - 418, COL["conc"], COL["conc_ln"], 2),
         F.rect(GS["wall"], GS["floor"], F.BX1 - GS["wall"], 20, "#2c3236")]
    for r, x in GS_ROW.items():
        g.append(F.rect(x - GS["cw"] / 2, GS["bot"], GS["cw"], GS["floor"] - GS["bot"], COL["conc"], COL["conc_ln"], 2))
        g.append(_t(x, GS["floor"] + 46, r, 24, INK, "middle"))
    t = GS_ROW["9.1"]
    g.append(F.rect(t - 20, 300, 40, GS["top"] - 300, A1_COL["mid"], COL["conc_ln"], 2))
    g.append(F.rect(t + 20, GS["top"], F.BX1 - t - 20, GS["bot"] - GS["top"], A1_COL["mid"], COL["conc_ln"], 2))
    g.append(_t(t + 40, 330, "塔", 24, INK))
    g.append(_t(GS["wall"] - 8, 480, "南", 22, J.TICK, "end"))
    g.append(_t(F.BX1 - 12, 410, "北", 22, J.TICK, "end"))
    g.append(_inset(262.0, A2T["K"]))
    return g


def gspan_stage(prev, st):
    g = []
    x = GS_ROW["13.1"]
    if _on(prev, st, "crack"):
        y0 = GS["top"] + GS["sag"]
        g.append(F.poly([(x - 34, y0 - 2), (x - 24, y0 + 12), (x - 30, y0 + 26)], "none", COL["red"], 4))
        g.append(F.poly([(x + 34, y0 - 2), (x + 24, y0 + 12), (x + 30, y0 + 26)], "none", COL["red"], 4))
        g.append(_ring(x, y0 + 15, 46, COL["red"], 4))
    if _on(prev, st, "share"):
        y = GS["top"] - 26
        for xa in (GS_ROW["15"], GS_ROW["11.1"]):
            g.append(F.arrow(x + (40 if xa > x else -40), y, xa + (-36 if xa > x else 36), y, COL["mark"], 6, 22))
            g.append(_ring(xa, GS["bot"] + 10, 26, COL["org"], 4.5))
    if _on(prev, st, "dim"):
        xd = x + 80
        g.append(F.line(x - 140, GS["top"], x + 140, GS["top"], COL["white"], 2, "6 6", 0.8))
        g.append(F.line(xd, GS["top"], xd, GS["top"] + GS["sag"], COL["white"], 3)
                 + F.line(xd - 10, GS["top"], xd + 10, GS["top"], COL["white"], 3)
                 + F.line(xd - 10, GS["top"] + GS["sag"], xd + 10, GS["top"] + GS["sag"], COL["white"], 3))
    return g


# ── core（c303）＝床の重ね（TF p9090 のコアの模式・1インチ＝40画素）──
CORE = dict(x0=760.0, x1=1160.0, slab=700.0, inch=40.0, topping=2.125, tile=1.375, sand=0.5, paver=0.75)


def core_levels():
    c = CORE
    t0 = c["slab"]
    t1 = t0 - c["topping"] * c["inch"]
    t2 = t1 - c["tile"] * c["inch"]
    t3 = t2 - c["sand"] * c["inch"]
    t4 = t3 - c["paver"] * c["inch"]
    return dict(slab=t0, topping=t1, tile=t2, sand=t3, paver=t4)


def core_base(st0):
    c, L = CORE, core_levels()
    g = [_ground_bg()]
    g.append(F.poly([(c["x0"] - 60, L["slab"]), (c["x1"] + 60, L["slab"]), (c["x1"] + 40, L["slab"] + 110),
                     (c["x0"] - 40, L["slab"] + 120)], "#6f777b", COL["conc_ln"], 2, True))
    g.append(F.rect(c["x0"], L["topping"], c["x1"] - c["x0"], L["slab"] - L["topping"], COL["conc_lt"], COL["conc_ln"], 2))
    g.append(F.rect(c["x0"], L["tile"], c["x1"] - c["x0"], L["topping"] - L["tile"], COL["tile"], COL["conc_ln"], 2))
    for x in (c["x0"] - 400, c["x1"] + 120):                     # 床の続き（薄く・模式）
        g.append(F.rect(x, L["tile"], 280, L["slab"] - L["tile"], COL["conc"], None, 0, 0, 0.25))
    return g


def core_stage(prev, st):
    c, L = CORE, core_levels()
    g = []
    if _on(prev, st, "new"):
        g.append(F.rect(c["x0"], L["sand"], c["x1"] - c["x0"], L["tile"] - L["sand"], COL["sand"], COL["conc_ln"], 2))
        for k in range(24):
            g.append(F.circ(c["x0"] + 10 + 16 * k, L["sand"] + 6 + (k % 3) * 4, 2, "#7d7058"))
        g.append(F.rect(c["x0"], L["paver"], c["x1"] - c["x0"], L["sand"] - L["paver"], COL["paver"], COL["conc_ln"], 2))
        g.append(F.line(c["x0"], L["tile"], c["x1"], L["tile"], COL["memb"], 5, "14 8"))
    if _on(prev, st, "load"):
        g += [_down(x, L["paver"] - 120, L["paver"] - 10, COL["mark"]) for x in (c["x0"] + 70, (c["x0"] + c["x1"]) / 2, c["x1"] - 70)]
    return g


# ── water（c313・c314）＝平らな床の上の防水・直し方 ──
WA = dict(x0=200.0, x1=1720.0, top=600.0, bot=720.0, sand=582.0, paver=556.0)


def water_parts(st):
    gone = 0.0 if st["strip"] == "on" else 1.0
    pond = 1.0 if (st["pond"] == "on" and st["strip"] != "on") else 0.0
    out = [_P("paver", "poly", _rp(WA["x0"], WA["paver"], WA["x1"], WA["sand"]), fill=COL["paver"], stroke=COL["conc_ln"], w=2, alpha=gone),
           _P("sand", "poly", _rp(WA["x0"], WA["sand"], WA["x1"], WA["top"] - 3), fill=COL["sand"], stroke=COL["conc_ln"], w=1, alpha=gone),
           _P("memb", "line", [(WA["x0"], WA["top"] - 2), (WA["x1"], WA["top"] - 2)], stroke=COL["memb"], w=5, alpha=gone)]
    for k, x in enumerate((420.0, 820.0, 1180.0, 1520.0)):
        out.append(_P(f"pond{k}", "poly", [(x - 120, WA["top"] - 3), (x - 60, WA["top"] - 12), (x + 60, WA["top"] - 12),
                                          (x + 120, WA["top"] - 3)], fill=COL["water"], stroke=COL["water_ln"], w=2, alpha=pond))
    return out


def water_base(st0):
    return [_ground_bg(), F.rect(WA["x0"], WA["top"], WA["x1"] - WA["x0"], WA["bot"] - WA["top"], COL["conc"], COL["conc_ln"], 2),
            F.rect(WA["x0"], WA["bot"], WA["x1"] - WA["x0"], 30, "none", None, 0)]


WA_FIX = ((520.0, 640.0), (1120.0, 1260.0))
WA_SLOPE = [(WA["x0"], 528.0), (WA["x1"], 584.0), (WA["x1"], WA["top"]), (WA["x0"], WA["top"])]


def water_stage(prev, st):
    g = []
    if _on(prev, st, "level"):
        x, y = 960.0, 470.0
        g.append(F.rect(x - 110, y - 22, 220, 44, COL["dark"], COL["dim"], 3, 22) + F.circ(x, y, 12, COL["grn"], COL["dark"], 2)
                 + F.line(x - 26, y - 22, x - 26, y + 22, COL["dim"], 2) + F.line(x + 26, y - 22, x + 26, y + 22, COL["dim"], 2))
    if _on(prev, st, "fix"):
        for a, b in WA_FIX:
            g.append(F.rect(a, WA["top"], b - a, 44, "#b07a5a", COL["dark"], 2, 0, 0.9))
    if _on(prev, st, "slope"):
        g.append(F.poly(WA_SLOPE, "#a3abb0", COL["conc_ln"], 2, True))
        g.append(F.arrow(700, 520, 1300, 548, COL["water"], 6, 22))
    if _on(prev, st, "memb2"):
        g.append(F.line(WA_SLOPE[0][0], WA_SLOPE[0][1] - 2, WA_SLOPE[1][0], WA_SLOPE[1][1] - 2, COL["mark"], 5, "14 8"))
    return g


# ── drip（c521）＝地下の駐車場の天井のひびからの漏れ ──
DR = dict(x0=200.0, x1=1300.0, top=330.0, bot=420.0, cx=700.0, floor=820.0)


def drip_parts(st):
    d = 1.0 if st["flow"] == "drip" else 0.0
    t = 1.0 if st["flow"] == "tap" else 0.0
    cx = DR["cx"]
    out = [_P(f"drop{k}", "circle", c=[cx, y], r=8.0, fill=COL["water"], stroke=COL["water_ln"], w=2, alpha=d)
           for k, y in enumerate((470.0, 580.0, 700.0))]
    out.append(_P("stream", "poly", [(cx - 10, DR["bot"]), (cx + 10, DR["bot"]), (cx + 22, DR["floor"]), (cx - 22, DR["floor"])],
                  fill=COL["water"], stroke=COL["water_ln"], w=2, alpha=t))
    out.append(_P("pool", "poly", [(cx - 30 - 150 * t, DR["floor"] - 2), (cx + 30 + 150 * t, DR["floor"] - 2),
                                   (cx + 20 + 140 * t, DR["floor"] + 8), (cx - 20 - 140 * t, DR["floor"] + 8)],
                  fill=COL["water"], stroke=COL["water_ln"], w=2))
    return out


def drip_base(st0):
    cx = DR["cx"]
    return [_ground_bg(), F.rect(DR["x0"], DR["top"], DR["x1"] - DR["x0"], DR["bot"] - DR["top"], A2_COL["deck"], COL["conc_ln"], 2),
            F.rect(F.BX0, DR["floor"], DR["x1"] - F.BX0, 30, "#2c3236"),
            F.poly([(cx - 8, DR["top"]), (cx + 6, DR["top"] + 30), (cx - 6, DR["top"] + 58), (cx + 4, DR["bot"])], "none", COL["red"], 4),
            F.rect(330, DR["bot"], 34, DR["floor"] - DR["bot"], COL["conc"], COL["conc_ln"], 2),
            F.rect(1080, DR["bot"], 34, DR["floor"] - DR["bot"], COL["conc"], COL["conc_ln"], 2),
            _t(DR["x0"] + 10, DR["top"] - 14, "地下の駐車場の天井（デッキの床の裏）", 22, J.TICK)]


def drip_stage(prev, st):
    g = []
    if st["band"] != "off" and prev.get("band", "off") == "off":
        g.append(F.line(1560, 470, 1560, 640, COL["dim"], 3, "6 6") + F.arrow(1560, 600, 1560, 650, COL["dim"], 3, 14))
    return g


# ── edge（c611・c612・ca02・ca03）＝塔の南の面とプールデッキ（西を向く・右が北）＝TF p9111 の形 ──
ED = dict(wall=180.0, top=440.0, bot=470.0, floor=800.0, tcol=1360.0, cw=36.0, beam=500.0)
ED_ROW = {"15": 430.0, "13.1": 760.0, "11.1": 1060.0, "9.1": 1360.0}
ED_SLAB_X = (198.0, 430.0, 600.0, 760.0, 900.0, 1000.0, 1060.0)
ED_FALL = dict(off=(440.0,) * 7, part=(452.0, 700.0, 770.0, 640.0, 470.0, 440.0, 440.0),
               full=(452.0, 690.0, 772.0, 772.0, 730.0, 600.0, 520.0))


def _ed_slab(fall):
    ys = ED_FALL[fall]
    top = list(zip(ED_SLAB_X, ys))
    bot = [(x, y + 30.0) for x, y in reversed(top)]
    return top + bot


def edge_parts(st):
    t = ED["tcol"] - ED["cw"] / 2
    beam = _rp(ED_ROW["11.1"], ED["top"], t, ED["beam"])
    pull = st["pull"] == "on"
    dd = 34.0 if st["drop"] == "on" else 0.0
    tower = [(t, 262.0), (t + ED["cw"], 262.0), (t + ED["cw"], ED["top"]), (F.BX1, ED["top"]), (F.BX1, ED["bot"]),
             (t, ED["bot"])]
    return [_P("slab", "poly", _ed_slab(st["fall"]), fill=A2_COL["deck"], stroke=COL["conc_ln"], w=2),
            _P("beam", "poly", beam, fill=(COL["yel"] if st["beam"] == "on" else A2_COL["deck"]), stroke=COL["conc_ln"], w=2,
               pivot=[t, ED["top"]], rot=(-9.0 if pull else 0.0), dx=(-22.0 if pull else 0.0)),
            _P("tower", "poly", tower, fill=A1_COL["mid"], stroke=COL["conc_ln"], w=2, dy=dd)]


def edge_base(st0):
    g = [_ground_bg(), F.rect(ED["wall"], 418, 22, ED["floor"] - 418, COL["conc"], COL["conc_ln"], 2),
         F.rect(ED["wall"], ED["floor"], F.BX1 - ED["wall"], 20, "#2c3236")]
    for r, x in ED_ROW.items():
        if r != "9.1":
            g.append(F.rect(x - 15, ED["bot"], 30, ED["floor"] - ED["bot"], COL["conc"], COL["conc_ln"], 2))
        g.append(_t(x, ED["floor"] + 46, r, 24, INK, "middle"))
    g.append(F.rect(ED["tcol"] - ED["cw"] / 2, ED["bot"], ED["cw"], ED["floor"] - ED["bot"], A1_COL["mid"], COL["conc_ln"], 2))
    g.append(_t(ED["wall"] - 8, 480, "南", 22, J.TICK, "end"))
    g.append(_t(F.BX1 - 12, 300, "北", 22, J.TICK, "end"))
    g.append(_t(ED["tcol"] + 60, 330, "塔", 24, INK))
    g.append(_inset(262.0, A2T["L"]))
    return g


def edge_joint_xy():
    return ED["tcol"], (ED["top"] + ED["beam"]) / 2.0


def edge_stage(prev, st):
    g = []
    jx, jy = edge_joint_xy()
    if _on(prev, st, "joint", "hurt"):
        g.append(_ring(jx, jy, 44, COL["red"], 5))
        g.append(F.poly([(jx - 6, jy - 22), (jx + 6, jy - 6), (jx - 4, jy + 10)], "none", COL["red"], 4))
    if _on(prev, st, "joint", "crush"):
        g.append(F.rect(jx - 22, jy - 10, 44, 26, COL["red"], COL["dark"], 2, 0, 0.85))
        g.append(F.line(jx - 30, jy - 30, jx + 30, jy + 30, COL["white"], 3) + F.line(jx - 30, jy + 30, jx + 30, jy - 30, COL["white"], 3))
    if _on(prev, st, "load"):
        g.append(_down(ED["tcol"], 214, 256, COL["mark"], 8, 22))
    if _on(prev, st, "pull"):
        g.append(F.arrow(ED["tcol"] - 70, jy - 60, ED["tcol"] - 230, jy - 34, COL["red"], 7, 22))
    return g


# ── joint（ca04・ca05・ca10）＝継ぎ目の断面（TF p9112＝柱は緑・床は灰色）──
JO = dict(cx=960.0, cw=160.0, top=300.0, bot=800.0, f0=470.0, f1=640.0, s1=540.0, x0=260.0, x1=1660.0)
JO_BARS = (905.0, 935.0, 985.0, 1015.0)
JO_TIES = (330.0, 380.0, 430.0, 680.0, 730.0, 780.0)
JO_STRENGTH = (6000.0, 4000.0)                  # 設計の強さ（psi）＝柱・床（AC p.65）


def joint_parts(st):
    c, h = JO["cx"], JO["cw"] / 2
    crush = 30.0 if st["crush"] == "on" else 0.0
    colfill = COL["colg"] if st["color"] == "on" else COL["conc"]
    flfill = COL["conc_lt"] if st["color"] == "on" else COL["conc"]
    out = [_P("colA", "poly", _rp(c - h, JO["top"], c + h, JO["f0"]), fill=colfill, stroke=COL["conc_ln"], w=2, dy=crush),
           _P("jz", "poly", [(c - h, JO["f0"] + crush), (c + h, JO["f0"] + crush), (c + h, JO["f1"]), (c - h, JO["f1"])],
              fill=flfill, stroke=COL["conc_ln"], w=2)]
    bars = 1.0 if st["bars"] == "on" else 0.0
    bk = st["buckle"] == "on"
    for k, x in enumerate(JO_BARS):
        out_ = -1.0 if x < c else 1.0
        b = (24.0 if k in (0, 3) else 14.0) * out_ if bk else 0.0
        pts = [(x, JO["top"] + 6 + crush), (x, JO["f0"] + crush), (x + b, (JO["f0"] + JO["f1"]) / 2), (x, JO["f1"]), (x, JO["bot"] - 6)]
        out.append(_P(f"lbar{k}", "line", pts, stroke=COL["bar"], w=6, alpha=bars))
    return out


def joint_base(st0):
    c, h = JO["cx"], JO["cw"] / 2
    g = [_ground_bg(),
         F.rect(JO["x0"], JO["f0"], c - h - JO["x0"], JO["f1"] - JO["f0"], COL["conc"], COL["conc_ln"], 2),
         F.rect(c + h, JO["f0"], JO["x1"] - c - h, JO["s1"] - JO["f0"], COL["conc"], COL["conc_ln"], 2),
         F.rect(c - h, JO["f1"], JO["cw"], JO["bot"] - JO["f1"], COL["conc"], COL["conc_ln"], 2)]
    for k in range(9):                              # 梁の輪の鉄筋（縦の線・模式）
        x = JO["x0"] + 40 + 60 * k
        g.append(F.line(x, JO["f0"] + 12, x, JO["f1"] - 12, "#5d92b4", 3, None, 0.8))
    # ⑤b-4 の下見：床の上に置くと左の札（床のコンクリート）と詰まった＝床の下へ
    g.append(_t(JO["x0"], JO["f1"] + 30, "梁と床（南＝デッキの側）", 22, J.TICK))
    g.append(_t(JO["x1"], JO["s1"] + 30, "塔の床", 22, J.TICK, "end"))
    return g


def joint_stage(prev, st):
    c, h = JO["cx"], JO["cw"] / 2
    g = []
    if _on(prev, st, "color"):
        g.append(F.rect(c - h, JO["f1"], JO["cw"], JO["bot"] - JO["f1"], COL["colg"], COL["conc_ln"], 2))
        g.append(F.rect(JO["x0"], JO["f0"], c - h - JO["x0"], JO["f1"] - JO["f0"], COL["conc_lt"], COL["conc_ln"], 2))
        g.append(F.rect(c + h, JO["f0"], JO["x1"] - c - h, JO["s1"] - JO["f0"], COL["conc_lt"], COL["conc_ln"], 2))
    if _on(prev, st, "ties"):
        for y in JO_TIES:
            g.append(F.line(c - h + 10, y, c + h - 10, y, COL["bar"], 5))
        xb = c + h + 34
        g.append(F.line(xb, JO["f0"], xb, JO["f1"], COL["white"], 3) + F.line(xb - 10, JO["f0"], xb + 10, JO["f0"], COL["white"], 3)
                 + F.line(xb - 10, JO["f1"], xb + 10, JO["f1"], COL["white"], 3))
    if _on(prev, st, "bar2"):
        x0, y0 = 300.0, 740.0
        L = 330.0
        g.append(F.rect(x0, y0, L, 26, COL["colg"], COL["dark"], 2) + _t(x0 - 12, y0 + 22, "柱", 24, INK, "end"))
        g.append(F.rect(x0, y0 + 50, L * JO_STRENGTH[1] / JO_STRENGTH[0], 26, COL["conc_lt"], COL["dark"], 2)
                 + _t(x0 - 12, y0 + 72, "床", 24, INK, "end"))
        g.append(_down(c, 214, 290, COL["red"], 9, 24) + F.arrow(c, 870, c, 808, COL["red"], 9, 24))
    if _on(prev, st, "dense"):
        g.append(F.rect(c - h + 4, JO["f0"] + 4, JO["cw"] - 8, JO["f1"] - JO["f0"] - 8, "none", COL["mark"], 4, 4, None, "10 6"))
    if _on(prev, st, "crush"):
        g.append(F.poly([(c - h - 10, JO["f0"] + 46), (c - h + 30, JO["f0"] + 66), (c - h + 10, JO["f0"] + 90)], "none", COL["red"], 4))
        g.append(F.poly([(c + h + 10, JO["f0"] + 50), (c + h - 30, JO["f0"] + 74), (c + h - 8, JO["f0"] + 98)], "none", COL["red"], 4))
    return g


# ── front（ca11）＝南から見た塔（正面）──
FR = dict(gy=840.0, top=360.0, w0=300.0, w1=700.0, m1=1140.0, e1=1500.0, ph=(820.0, 1060.0, 314.0), drop=70.0,   # 右に札の場所
          heads=(905.0, 985.0))


def front_parts(st):
    d = FR["drop"] if st["roof"] == "down" else 0.0
    x0, x1, py = FR["ph"]
    hv = 1.0 if st["roof"] == "down" else 0.0
    out = [_P("roof", "poly", _rp(FR["w1"], FR["top"] - 8, FR["m1"], FR["top"] + 10), fill="#4b575c", stroke=COL["dark"], w=2, dy=d),
           _P("ph", "poly", _rp(x0, py, x1, FR["top"] - 8), fill=A1_COL["mid"], stroke=COL["dark"], w=2, dy=d)]
    for k, x in enumerate(FR["heads"]):
        out.append(_P(f"head{k}", "poly", _rp(x - 9, FR["top"] - 30, x + 9, FR["top"] + 30), fill=COL["conc_lt"], stroke=COL["dark"],
                      w=2, alpha=hv))
    return out


def _facade(x0, x1, col):
    g = [F.rect(x0, FR["top"], x1 - x0, FR["gy"] - FR["top"], col, COL["dark"], 2)]
    fh = (FR["gy"] - FR["top"]) / 12.0
    for k in range(1, 12):
        y = FR["top"] + fh * k
        g.append(F.line(x0 + 6, y, x1 - 6, y, A1_COL["bal"], 2, None, 0.7))
    return g


def front_base(st0):
    g = [F.rect(F.BX0, 262.0, F.BW, 600.0, A1_COL["sky0"])]
    g += _facade(FR["w0"], FR["w1"], A1_COL["west"]) + _facade(FR["w1"], FR["m1"], A1_COL["mid"]) + _facade(FR["m1"], FR["e1"], A1_COL["east"])
    g.append(F.rect(F.BX0, FR["gy"], F.BW, 22, A1_COL["ground"]))
    g.append(_t((FR["w0"] + FR["w1"]) / 2, FR["top"] - 16, "西の部分", 22, INK, "middle"))
    g.append(_t((FR["m1"] + FR["e1"]) / 2, FR["top"] - 16, "東の部分", 22, INK, "middle"))
    return g


def front_stage(prev, st):
    g = []
    if _on(prev, st, "q"):
        for x in FR["heads"]:
            g.append(F.rect(x - 10, FR["gy"] - 90, 20, 90, COL["conc_lt"], COL["dark"], 2))
            g.append(_t(x, FR["gy"] - 102, "？", 34, COL["mark"], "middle"))
    if _on(prev, st, "roof", "down"):
        yb = FR["gy"] - 150                         # layout：土ぼこりが下の「？」を覆った＝下の端を上げる
        g.append(F.poly([(FR["w1"] + 10, yb), (FR["w1"] + 30, FR["top"] + 160), (FR["m1"] - 40, FR["top"] + 130),
                         (FR["m1"] - 10, yb)], "#8a8378", None, None, True, None, 0.55))
    if _on(prev, st, "dir"):
        x0, y0, w, h = 1690.0, 300.0, 140.0, 200.0
        g.append(F.rect(x0, y0, w, h, COL["dark"], "#5d6a72", 2, 6, 0.92))
        for k, (lab, yy) in enumerate((("3", y0 + 34), ("4", y0 + 70), ("9.1", y0 + h - 30))):
            g.append(F.line(x0 + 14, yy, x0 + w - 44, yy, "#dfe6ea", 1.5, "5 5", 0.7) + _t(x0 + w - 10, yy + 7, lab, 18, INK, "end"))
        g.append(F.arrow(x0 + 50, y0 + h - 20, x0 + 50, y0 + 26, COL["mark"], 6, 18))
    return g


# ── zoneb（ca16）＝壁の無い境（北を向いて見る・左が西）＝TF p9144 の形 ──
ZB = dict(top=520.0, bot=546.0, x0=160.0, x1=1700.0, cw=34.0, brk=780.0, rot=5.0)
ZB_COL = {"D": 300.0, "E": 600.0, "H": 1060.0, "I": 1360.0}
ZB_TOP = ((160.0, 460.0), (440.0, 760.0), (900.0, 1220.0), (1200.0, 1520.0))      # 上の鉄筋（柱の上・模式）
ZB_BOT = ((640.0, 1020.0), (1100.0, 1320.0), (1400.0, 1680.0))


def zoneb_parts(st):
    r = ZB["rot"] if st["brk"] == "on" else 0.0
    pv = [ZB["brk"], ZB["bot"]]
    out = [_P("slab_e", "poly", _rp(ZB["brk"] + 2, ZB["top"], ZB["x1"], ZB["bot"]), fill=COL["conc_lt"], stroke=COL["conc_ln"], w=2,
              pivot=pv, rot=r)]
    for k, (a, b) in enumerate(t for t in ZB_TOP if t[0] > ZB["brk"]):
        out.append(_P(f"tb{k}", "line", [(a, ZB["top"] + 7), (b, ZB["top"] + 7)], stroke="#20262d", w=4, pivot=pv, rot=r))
    for k, (a, b) in enumerate(t for t in ZB_BOT if t[0] > ZB["brk"]):
        out.append(_P(f"bb{k}", "line", [(a, ZB["bot"] - 6), (b, ZB["bot"] - 6)], stroke="#20262d", w=4, pivot=pv, rot=r))
    return out


def zoneb_base(st0):
    g = [_ground_bg()]
    for c, x in ZB_COL.items():
        g.append(F.rect(x - ZB["cw"] / 2, 330, ZB["cw"], 520, COL["conc"], COL["conc_ln"], 2, 0, 0.9))
        g.append(_t(x, 316, c, 24, INK, "middle"))
    g.append(F.rect(ZB["x0"], ZB["top"], ZB["brk"] - ZB["x0"], ZB["bot"] - ZB["top"], COL["conc_lt"], COL["conc_ln"], 2))
    for a, b in ZB_TOP:
        if b <= ZB["brk"]:
            g.append(F.line(a, ZB["top"] + 7, b, ZB["top"] + 7, "#20262d", 4))
    for a, b in ZB_BOT:
        if b <= ZB["brk"]:
            g.append(F.line(a, ZB["bot"] - 6, b, ZB["bot"] - 6, "#20262d", 4))
    g.append(_t(ZB["x0"], 300, "西", 22, J.TICK))
    g.append(_t(ZB["x1"], 300, "東（崩れた真ん中の部分）", 22, J.TICK, "end"))
    return g


def zoneb_stage(prev, st):
    g = []
    if _on(prev, st, "zone"):
        g.append(F.rect(ZB_COL["E"] - 60, 330, ZB_COL["I"] - ZB_COL["E"] + 120, 520, COL["blue"], None, 0, 0, 0.12))
    if _on(prev, st, "mark"):
        g.append(_ring(ZB["brk"], ZB["top"] + 13, 30, COL["red"], 5) + _t(ZB["brk"], ZB["top"] - 30, "①", 34, COL["red"], "middle"))
        g.append(_ring(ZB_COL["E"], ZB["top"] + 13, 30, COL["white"], 4) + _t(ZB_COL["E"], ZB["top"] - 30, "②", 34, COL["white"], "middle"))
    if _on(prev, st, "bar"):
        g.append(F.circ(ZB_TOP[1][1], ZB["top"] + 7, 12, COL["mark"], COL["dark"], 2))
    return g


# ── rubble（c710）＝がれきの山と残った西の部分 ──
RB = dict(gy=840.0, b0=300.0, b1=700.0, top=330.0)
RB_PILE = [(700.0, 840.0), (760.0, 700.0), (880.0, 640.0), (1010.0, 668.0), (1120.0, 610.0), (1260.0, 660.0), (1400.0, 640.0),
           (1520.0, 720.0), (1620.0, 840.0)]
RB_EYES = ((1730.0, 560.0), (1700.0, 760.0))


def rubble_base(st0):
    g = [F.rect(F.BX0, 262.0, F.BW, 600.0, A1_COL["sky0"])] + _facade_rb()
    g.append(F.poly(RB_PILE, A1_COL["heap"], A1_COL["heap_ln"], 3, True))
    for k in range(10):
        x = 760 + 80 * k
        g.append(F.line(x, 760, x + 40, 720 - (k % 3) * 14, A1_COL["heap_ln"], 3))
    g.append(F.rect(F.BX0, RB["gy"], F.BW, 22, A1_COL["ground"]))
    return g


def _facade_rb():
    g = [F.rect(RB["b0"], RB["top"], RB["b1"] - RB["b0"], RB["gy"] - RB["top"], A1_COL["west"], COL["dark"], 2)]
    fh = (RB["gy"] - RB["top"]) / 12.0
    for k in range(1, 12):
        g.append(F.line(RB["b0"] + 6, RB["top"] + fh * k, RB["b1"] - 6, RB["top"] + fh * k, A1_COL["bal"], 2, None, 0.7))
    g.append(F.poly([(RB["b1"], RB["top"]), (RB["b1"] + 30, RB["top"] + 120), (RB["b1"] + 8, RB["top"] + 260), (RB["b1"], RB["top"] + 300)],
                    A1_COL["west"], COL["dark"], 2, True))
    return g


def rubble_stage(prev, st):
    g = []
    if _on(prev, st, "unst"):
        g.append(F.rect(RB["b0"] - 12, RB["top"] - 12, RB["b1"] - RB["b0"] + 54, RB["gy"] - RB["top"] + 12, "none", COL["red"], 5, 4, None, "16 9"))
    if _on(prev, st, "watch"):
        for ex, ey in RB_EYES:
            g.append(F.circ(ex, ey, 16, COL["white"], COL["dark"], 3) + F.circ(ex, ey, 6, COL["dark"]))
        g.append(F.line(RB_EYES[0][0] - 18, RB_EYES[0][1], RB["b1"] + 30, RB["top"] + 140, COL["mark"], 3, "10 8"))
        g.append(F.line(RB_EYES[1][0] - 18, RB_EYES[1][1], 1200.0, 660.0, COL["mark"], 3, "10 8"))
        g.append(F.poly(RB_PILE, "none", COL["mark"], 4, True, "12 8"))
    return g


# ── excav（cb02・cb03・cb05）＝87パークの掘削と鋼の板（西を向く・右が北）＝TF p9169 ──
EX = dict(gy=470.0, pit0=100.0, pit1=560.0, pit_b=760.0, pile=560.0, ctsp=690.0, wall=720.0, floor=830.0, deck_b=500.0)
EX_ROW = {"15": 1000.0, "13.1": 1340.0, "11.1": 1680.0}
EX_AMP = ((630.0, 26.0), (800.0, 10.0), (1300.0, 4.0))          # 揺れの大きさ（画素・模式）＝鋼の板の外・地下の壁の内・継ぎ目の手前


def excav_parts(st):
    p, d = EX["pile"], st["drive"] == "on"
    pile = _rp(p - 8, 290.0, p + 8, 470.0) if not d else _rp(p - 8, 460.0, p + 8, 800.0)
    ham = _rp(p - 30, 240.0, p + 30, 290.0) if not d else _rp(p - 30, 410.0, p + 30, 460.0)
    pit = 1.0 if st["pit"] == "on" else 0.0
    return [_P("pile", "poly", pile, fill=COL["steel"], stroke=COL["dark"], w=2, alpha=pit),
            _P("ham", "poly", ham, fill=COL["org"], stroke=COL["dark"], w=2, alpha=pit)]


def excav_base(st0):
    g = [_ground_bg(), F.rect(F.BX0, EX["gy"], F.BW, 862 - EX["gy"], COL["soil"])]
    g.append(F.rect(EX["ctsp"] - 4, EX["gy"], 8, 862 - EX["gy"], COL["steel"], COL["dark"], 1.5))
    g.append(F.rect(EX["wall"], EX["gy"], 24, EX["floor"] - EX["gy"], COL["conc"], COL["conc_ln"], 2))
    g.append(F.rect(EX["wall"] + 24, EX["gy"], F.BX1 - EX["wall"] - 24, EX["floor"] - EX["gy"], "#1a2228"))
    g.append(F.rect(EX["wall"], EX["gy"], F.BX1 - EX["wall"], EX["deck_b"] - EX["gy"], A2_COL["deck"], COL["conc_ln"], 2))
    g.append(F.rect(EX["wall"], EX["floor"], F.BX1 - EX["wall"], 20, COL["conc"], COL["conc_ln"], 2))
    for r, x in EX_ROW.items():
        g.append(F.rect(x - 15, EX["deck_b"], 30, EX["floor"] - EX["deck_b"], COL["conc"], COL["conc_ln"], 2))
        g.append(_t(x, EX["deck_b"] + 62, r, 22, INK, "middle"))    # layout：継ぎ目の輪（半径30）の下へ
    g.append(_t(EX["wall"] + 40, EX["gy"] - 14, "この建物（北）", 22, INK))
    g.append(_t(F.BX0 + 12, EX["gy"] - 14, "南", 22, J.TICK))      # ⑤b-4 の下見：札「87パークの掘った所」と詰まった＝向きだけ
    return g


def excav_stage(prev, st):
    g = []
    if _on(prev, st, "pit"):
        g.append(F.rect(EX["pit0"], EX["gy"], EX["pit1"] - EX["pit0"], EX["pit_b"] - EX["gy"], COL["pit"], COL["soil_ln"], 2))
    if _on(prev, st, "drive"):
        for k in range(3):
            y = 380 - 10 * k
            g.append(F.poly([(EX["pile"] - 52 - 8 * k, y), (EX["pile"] - 44 - 8 * k, y - 10), (EX["pile"] - 36 - 8 * k, y)], "none", COL["org"], 3))
    if _on(prev, st, "dist"):
        y = EX["gy"] - 54
        g.append(F.line(EX["pile"], y, EX["wall"], y, COL["white"], 3) + F.line(EX["pile"], y - 12, EX["pile"], y + 12, COL["white"], 3)
                 + F.line(EX["wall"], y - 12, EX["wall"], y + 12, COL["white"], 3))
    if _on(prev, st, "wave"):
        cx, cy = EX["pile"], 640.0
        for k, r in enumerate((60, 110, 160)):
            g.append(F.poly(F._arc(cx, cy, r, -80, 80, 16), "none", COL["red"], 4, op=0.9 - 0.2 * k))
    if st["damp"] in ("on", "more") and prev.get("damp") not in ("on", "more"):
        for (x, a) in EX_AMP[:2]:
            g.append(_wiggle(x, 650.0, a))
    if _on(prev, st, "damp", "more"):
        x, a = EX_AMP[2]
        g.append(_wiggle(x, 650.0, a))
        g.append(_ring(EX_ROW["13.1"], EX["deck_b"] + 4, 30, COL["mark"], 4))
    return g


def _wiggle(x, y, a, n=4, w=80.0):
    pts = [(x - w / 2 + w * k / (n * 8), y + a * math.sin(2 * math.pi * k / 8)) for k in range(n * 8 + 1)]
    return F.poly(pts, "none", COL["red"], 4)


# ── ground（cb12・cb13）＝くいと地下の床・石灰岩 ──
GR = dict(x0=360.0, x1=1400.0, gy=330.0, slab0=520.0, slab1=556.0, lime=640.0, pile_b=800.0, inset=(1480.0, 300.0, 1830.0, 640.0))
GR_PILES = tuple(420.0 + 140.0 * k for k in range(8))
GR_CAVE = [(1600.0, 520.0), (1650.0, 492.0), (1720.0, 500.0), (1760.0, 540.0), (1730.0, 580.0), (1650.0, 586.0), (1606.0, 560.0)]


def ground_base(st0):
    g = [_ground_bg(), F.rect(F.BX0, GR["slab1"], 1430 - F.BX0, GR["lime"] - GR["slab1"], COL["sand"], None, 0, 0, 0.55),
         F.rect(F.BX0, GR["lime"], 1430 - F.BX0, 862 - GR["lime"], COL["lime"])]
    g.append(F.rect(GR["x0"], GR["gy"], 24, GR["slab1"] - GR["gy"], COL["conc"], COL["conc_ln"], 2))
    g.append(F.rect(GR["x1"] - 24, GR["gy"], 24, GR["slab1"] - GR["gy"], COL["conc"], COL["conc_ln"], 2))
    g.append(F.rect(GR["x0"], GR["slab0"], GR["x1"] - GR["x0"], GR["slab1"] - GR["slab0"], COL["conc"], COL["conc_ln"], 2))
    g.append(F.rect(GR["x0"], GR["gy"], GR["x1"] - GR["x0"], 26, A2_COL["deck"], COL["conc_ln"], 2))
    for x in GR_PILES:
        g.append(F.rect(x - 10, GR["slab1"], 20, GR["pile_b"] - GR["slab1"], "#9aa3a8", COL["conc_ln"], 2))
    g.append(_t(GR["x0"] + 40, GR["slab0"] - 14, "地下の床", 22, INK))
    return g


def ground_stage(prev, st):
    g = []
    if _on(prev, st, "lime"):
        for k in range(14):
            x = 120 + 90 * k
            g.append(F.line(x, 700 + (k % 2) * 60, x + 40, 700 + (k % 2) * 60, COL["lime_ln"], 3))
    if _on(prev, st, "cave"):
        x0, y0, x1, y1 = GR["inset"]
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, COL["lime"], "#e3eaee", 2))
        g.append(F.poly(GR_CAVE, COL["dark"], COL["lime_ln"], 3, True))
        for k in range(3):
            g.append(F.circ(1640 + 40 * k, 440 - 10 * k, 7, COL["water"], COL["water_ln"], 2))
        g.append(_t(x0 + 12, y0 + 30, "例", 24, COL["dark"]))
    if _on(prev, st, "none"):
        for x in (560.0, 880.0, 1200.0):
            g.append(F.poly([(x - 18, 730), (x - 4, 746), (x + 20, 712)], "none", COL["grn"], 7))
    if _on(prev, st, "pile"):
        for x in GR_PILES:
            g.append(F.rect(x - 12, GR["slab1"], 24, GR["pile_b"] - GR["slab1"], "none", COL["mark"], 3))
    if _on(prev, st, "floor"):
        g.append(F.line(GR["x0"], GR["slab0"] - 3, GR["x1"], GR["slab0"] - 3, COL["mark"], 5))
    return g


# ── cover（c907・c908）＝鉄筋の上のコンクリートの厚さ（1インチ＝36画素）──
CV = dict(top=420.0, bot=700.0, inch=36.0, dwg=0.75, real=2.0, r=10.0, panels=((200.0, 860.0), (1060.0, 1720.0)))


def cover_bar_y(which):
    return CV["top"] + CV[which] * CV["inch"] + CV["r"]


def _cv_panel(x0, x1, which):
    g = [F.rect(x0, CV["top"], x1 - x0, CV["bot"] - CV["top"], COL["conc_lt"], COL["conc_ln"], 2)]
    y = cover_bar_y(which)
    for k in range(7):
        g.append(F.circ(x0 + 70 + 86 * k, y, CV["r"], "#5a6470", COL["dark"], 2))
    xd = x0 - 26
    g.append(F.line(xd, CV["top"], xd, y - CV["r"], COL["white"], 3) + F.line(xd - 10, CV["top"], xd + 10, CV["top"], COL["white"], 3)
             + F.line(xd - 10, y - CV["r"], xd + 10, y - CV["r"], COL["white"], 3))
    return g


def cover_base(st0):
    return [_ground_bg()]


def cover_stage(prev, st):
    g = []
    (a0, a1), (b0, b1) = CV["panels"]
    if _on(prev, st, "dwg"):
        g += _cv_panel(a0, a1, "dwg") + [_t((a0 + a1) / 2, CV["bot"] + 40, "図面", 26, INK, "middle")]
    if _on(prev, st, "real"):
        g += _cv_panel(b0, b1, "real") + [_t((b0 + b1) / 2, CV["bot"] + 40, "現場から運び出した床", 26, INK, "middle")]
    if _on(prev, st, "weak"):
        for (x0, x1), w in (((a0, a1), "dwg"), ((b0, b1), "real")):
            xe = x1 - 40
            g.append(F.line(xe, cover_bar_y(w), xe, CV["bot"], COL["mark"], 4) + F.line(xe - 10, cover_bar_y(w), xe + 10, cover_bar_y(w), COL["mark"], 4)
                     + F.line(xe - 10, CV["bot"], xe + 10, CV["bot"], COL["mark"], 4))
        g.append(F.arrow(b1 + 60, 470, b1 + 60, 640, COL["red"], 9, 26))
    return g


# ── ruler（c902・c905）＝2つの物差し ──
RU = dict(x0=420.0, x1=1560.0, need=1300.0, have=1000.0, y=(400.0, 620.0), h=22.0)


def ruler_base(st0):
    return [_ground_bg()]


def ruler_stage(prev, st):
    g = []
    if _on(prev, st, "rul"):
        for y in RU["y"]:
            g.append(F.rect(RU["x0"], y, RU["x1"] - RU["x0"], RU["h"], "#d9cfa8", COL["dark"], 2, 3))
            for k in range(int((RU["x1"] - RU["x0"]) // 38) + 1):
                x = RU["x0"] + 38 * k
                g.append(F.line(x, y, x, y + (12 if k % 5 else 20), COL["dark"], 2))
            g.append(F.poly([(RU["need"], y - 4), (RU["need"] - 12, y - 24), (RU["need"] + 12, y - 24)], COL["grn"], COL["dark"], 2, True))
            g.append(F.line(RU["need"], y - 4, RU["need"], y + RU["h"] + 70, COL["grn"], 3, "8 6"))
    if _on(prev, st, "short"):
        for y in RU["y"]:
            yb = y + RU["h"] + 18
            g.append(F.rect(RU["x0"], yb, RU["have"] - RU["x0"], 30, COL["blue"], COL["dark"], 2, 3))
            g.append(F.line(RU["have"], yb + 15, RU["need"], yb + 15, COL["red"], 5, "10 6"))
    if _on(prev, st, "gap"):
        y = RU["y"][0] + RU["h"] + 18
        g.append(F.rect(RU["have"], y - 4, RU["need"] - RU["have"], 38, "none", COL["red"], 5, 4))
    if _on(prev, st, "limit"):
        y = RU["y"][0]
        g.append(F.poly([(1160, y - 2), (1176, y + 10), (1166, y + RU["h"] + 2), (1240, y + RU["h"] + 2), (1232, y + 8),
                         (1246, y - 2)], A2_COL["ground"], COL["red"], 3, True))
    return g


# ── rebar（c911）＝柱のまわりの上の鉄筋（上から）──
RB_C = dict(y=540.0, half=60.0, span=200.0, sd=34.0, k=1.30, panels=(560.0, 1360.0))   # ⑤b-4 の下見：span 280 は下の札が出典の行に重なった


def rebar_offsets(which):
    s = RB_C["sd"] * (RB_C["k"] if which == "real" else 1.0)
    out, o = [], s / 2.0
    while o <= RB_C["span"]:
        out += [o, -o]
        o += s
    return sorted(out)


def _rb_panel(cx, which, hi=False):
    cy, h, sp = RB_C["y"], RB_C["half"], RB_C["span"]
    g = [F.rect(cx - sp - 20, cy - sp - 20, 2 * sp + 40, 2 * sp + 40, "#59626a", COL["conc_ln"], 2)]
    for o in rebar_offsets(which):
        over = abs(o) < h
        c = COL["mark"] if (hi and over) else "#20262d"
        g.append(F.line(cx + o, cy - sp, cx + o, cy + sp, c, 4) + F.line(cx - sp, cy + o, cx + sp, cy + o, c, 4))
    g.append(F.rect(cx - h, cy - h, 2 * h, 2 * h, "none", COL["white"], 4, 0, None, "8 6"))
    return g


def rebar_base(st0):
    return [_ground_bg()] + _rb_panel(RB_C["panels"][0], "dwg")


def rebar_stage(prev, st):
    g = []
    a, b = RB_C["panels"]
    if _on(prev, st, "real"):
        g += _rb_panel(b, "real")
    if _on(prev, st, "over"):
        g += _rb_panel(a, "dwg", True) + _rb_panel(b, "real", True)
    if _on(prev, st, "space"):
        for cx, w in ((a, "dwg"), (b, "real")):
            o = [x for x in rebar_offsets(w) if x > RB_C["half"]][:2]
            y = RB_C["y"] + RB_C["span"] + 34
            g.append(F.line(cx + o[0], y, cx + o[1], y, COL["white"], 3) + F.line(cx + o[0], y - 10, cx + o[0], y + 10, COL["white"], 3)
                     + F.line(cx + o[1], y - 10, cx + o[1], y + 10, COL["white"], 3))
    if _on(prev, st, "weak"):
        g.append(F.arrow(b + RB_C["span"] + 80, 420, b + RB_C["span"] + 80, 620, COL["red"], 9, 26))
    return g


# ══════════════════════════════════════════════════════════
#  見え方の表
# ══════════════════════════════════════════════════════════
TOPLAB = "上から見た敷地（北が上）"
VIEWS = dict(
    site=dict(lab=TOPLAB, fields=dict(zone=ONOFF, cols=ONOFF, pool=ONOFF), base=site_base, stage=site_stage),
    planter=dict(lab=TOPLAB, fields=dict(box=ONOFF, palm=("off", "on", "gone"), weight=("off", "plant", "both")),
                 base=planter_base, stage=planter_stage, parts=planter_parts),
    dig=dict(lab=TOPLAB, fields=dict(under=ONOFF, strip=ONOFF, name=ONOFF), base=dig_base, stage=dig_stage),
    cand=dict(lab=TOPLAB, fields=dict(cand=ONOFF, red=ONOFF), base=cand_base, stage=cand_stage),
    seq=dict(lab=TOPLAB, fields=dict(first=ONOFF, second=ONOFF, around=ONOFF), base=seq_base, stage=seq_stage),
    dmg=dict(lab=TOPLAB, fields=dict(leak=ONOFF, pts=ONOFF), base=dmg_base, stage=dmg_stage),
    sight=dict(lab=TOPLAB, fields=dict(vis=ONOFF, lobby=ONOFF, sound=ONOFF), base=sight_base, stage=sight_stage),
    code=dict(lab=TOPLAB, fields=dict(dots=ONOFF, flex=ONOFF), base=code_base, stage=code_stage),
    model=dict(lab="上から見たコンピュータの模型（北が上）", fields=dict(calc=ONOFF), base=model_base, stage=model_stage),
    cam=dict(lab="上から見た塔の階（北が上）", fields=dict(unit=ONOFF, move=ONOFF), base=cam_base, stage=cam_stage),
    north=dict(lab=TOPLAB, fields=dict(eye=ONOFF, debris=ONOFF), base=north_base, stage=north_stage),
    sat=dict(lab=TOPLAB, fields=dict(sat=ONOFF, near=ONOFF), base=sat_base, stage=sat_stage),
    flat=dict(lab="横から見た柱と床", fields=dict(plate=ONOFF, joint=ONOFF), base=flat_base, stage=flat_stage),
    punch=dict(lab="柱と床の継ぎ目を縦に切った断面", fields=dict(load=ONOFF, react=ONOFF, crack=("off", "on", "wide"), drop=ONOFF,
                                                    hook=ONOFF, scis=ONOFF, shear=ONOFF, gauge=ONOFF),
               base=punch_base, stage=punch_stage, parts=punch_parts),
    gspan=dict(lab="西を向いて見た地下の駐車場（右が北）", fields=dict(crack=ONOFF, sag=ONOFF, share=ONOFF, dim=ONOFF),
               base=gspan_base, stage=gspan_stage, parts=gspan_parts),
    core=dict(lab="プールデッキの床を縦に切った断面", fields=dict(new=ONOFF, load=ONOFF), base=core_base, stage=core_stage),
    water=dict(lab="プールデッキの床を縦に切った断面", fields=dict(pond=ONOFF, level=ONOFF, strip=ONOFF, fix=ONOFF, slope=ONOFF, memb2=ONOFF),
               base=water_base, stage=water_stage, parts=water_parts),
    drip=dict(lab="横から見た地下の駐車場の天井", fields=dict(flow=("drip", "tap"), band=("off", "on")), base=drip_base, stage=drip_stage,
              parts=drip_parts),
    edge=dict(lab="西を向いて見た塔の南の面（右が北）", fields=dict(fall=("off", "part", "full"), beam=ONOFF, pull=ONOFF,
                                                      joint=("ok", "hurt", "crush"), drop=ONOFF, load=ONOFF),
              base=edge_base, stage=edge_stage, parts=edge_parts),
    joint=dict(lab="継ぎ目を縦に切った断面（K-9.1・L-9.1）", fields=dict(color=ONOFF, bars=ONOFF, ties=ONOFF, buckle=ONOFF, dense=ONOFF,
                                                           crush=ONOFF, bar2=ONOFF),
               base=joint_base, stage=joint_stage, parts=joint_parts),
    front=dict(lab="南から見た塔（正面）", fields=dict(q=ONOFF, roof=("on", "down"), dir=ONOFF), base=front_base, stage=front_stage,
               parts=front_parts),
    zoneb=dict(lab="北を向いて見た床と柱（左が西）", fields=dict(zone=ONOFF, mark=ONOFF, brk=ONOFF, bar=ONOFF), base=zoneb_base,
               stage=zoneb_stage, parts=zoneb_parts),
    rubble=dict(lab="横から見た残った西の部分とがれき", fields=dict(unst=ONOFF, watch=ONOFF), base=rubble_base, stage=rubble_stage),
    excav=dict(lab="西を向いて見た地面の中（右が北）", fields=dict(pit=ONOFF, drive=ONOFF, dist=ONOFF, wave=ONOFF, damp=("off", "on", "more")),
               base=excav_base, stage=excav_stage, parts=excav_parts),
    ground=dict(lab="横から見た地面の中", fields=dict(lime=ONOFF, cave=ONOFF, none=ONOFF, pile=ONOFF, floor=ONOFF), base=ground_base,
                stage=ground_stage),
    cover=dict(lab="床を縦に切った断面", fields=dict(dwg=ONOFF, real=ONOFF, weak=ONOFF), base=cover_base, stage=cover_stage),
    ruler=dict(lab="強さの物差し", fields=dict(rul=ONOFF, short=ONOFF, gap=ONOFF, limit=ONOFF), base=ruler_base, stage=ruler_stage),
    rebar=dict(lab="上から見た柱のまわりの上の鉄筋", fields=dict(real=ONOFF, over=ONOFF, space=ONOFF, weak=ONOFF), base=rebar_base,
               stage=rebar_stage))
START ={v: {k: vs[0] for k, vs in d["fields"].items()} for v, d in VIEWS.items()}
# 戻さない欄（落ちた床は戻らない・抜いたヤシの木は戻らない・押しつぶれは戻らない）
#   ⚠️ 欄の名は見え方ごと（flat の joint は on/off・edge の joint は ok→hurt→crush）＝見え方で分ける
ORDER = dict(planter=dict(palm=("off", "on", "gone")), edge=dict(fall=("off", "part", "full"), joint=("ok", "hurt", "crush"),
                                                                 pull=ONOFF, drop=ONOFF),
             drip=dict(flow=("drip", "tap")), punch=dict(crack=("off", "on", "wide"), drop=ONOFF),
             excav=dict(damp=("off", "on", "more"), drive=ONOFF), joint=dict(crush=ONOFF, buckle=ONOFF),
             zoneb=dict(brk=ONOFF), front=dict(roof=("on", "down")), gspan=dict(sag=ONOFF))


# ── hall（c614）＝上の階の廊下（西→東を見るカメラ・横から＝左が西）──
HA = dict(x0=260.0, x1=1760.0, ftop=640.0, fbot=666.0, ctop=380.0, cbot=404.0, cam=(220.0, 470.0))
HA_COL = {"I": 600.0, "K": 900.0, "L": 1180.0, "M": 1500.0}
HA_X = (260.0, 600.0, 760.0, 900.0, 1040.0, 1180.0, 1340.0, 1500.0, 1760.0)
HA_SAG = (0.0, 0.0, 6.0, 16.0, 20.0, 16.0, 6.0, 0.0, 0.0)            # たわみ（画素・模式）＝K と L の辺りだけ（TF p9134：I は動かない）


def hall_floor(sag):
    top = [(x, HA["ftop"] + (d if sag else 0.0)) for x, d in zip(HA_X, HA_SAG)]
    bot = [(x, HA["fbot"] + (d if sag else 0.0)) for x, d in reversed(list(zip(HA_X, HA_SAG)))]
    return top + bot


def hall_parts(st):
    return [_P("floor", "poly", hall_floor(st["sag"] == "on"), fill=COL["conc_lt"], stroke=COL["conc_ln"], w=2)]


def hall_base(st0):
    g = [_ground_bg(), F.rect(HA["x0"], HA["ctop"], HA["x1"] - HA["x0"], HA["cbot"] - HA["ctop"], COL["conc_lt"], COL["conc_ln"], 2)]
    for c, x in HA_COL.items():
        g.append(F.rect(x - 18, HA["cbot"], 36, HA["ftop"] - HA["cbot"], COL["conc"], COL["conc_ln"], 2, 0, 0.75))
        g.append(F.rect(x - 18, HA["fbot"] + 22, 36, 40, COL["conc"], COL["conc_ln"], 2, 0, 0.75))   # 下の階の柱は短く（札の場所）
        g.append(_t(x, HA["ctop"] - 14, c, 24, INK, "middle"))
    cx, cy = HA["cam"]
    g.append(F.rect(cx - 18, cy - 12, 36, 24, COL["dark"], COL["mark"], 3, 3))
    g.append(F.poly([(cx + 18, cy), (cx + 520, cy - 60), (cx + 520, cy + 150)], COL["mark"], None, None, True, None, 0.16))
    g.append(_t(HA["x0"], 312, "西", 22, J.TICK))
    g.append(_t(HA["x1"], 312, "東", 22, J.TICK, "end"))
    return g


def hall_stage(prev, st):
    g = []
    if _on(prev, st, "ref"):
        g.append(F.line(HA["x0"], HA["ftop"], HA["x1"], HA["ftop"], COL["white"], 4, "16 8"))
    return g


VIEWS["hall"] = dict(lab="横から見た上の階の廊下（左が西）", fields=dict(ref=ONOFF, sag=ONOFF), base=hall_base, stage=hall_stage,
                     parts=hall_parts)
START["hall"] = {k: vs[0] for k, vs in VIEWS["hall"]["fields"].items()}


# ══════════════════════════════════════════════════════════
#  札の指し先と置き場
# ══════════════════════════════════════════════════════════
def anchors(view, st):
    if view in ("site", "planter", "dig", "cand", "seq", "dmg", "sight", "code", "model", "north", "sat"):
        out = dict(deck=tp(1300.0, 700.0), park=tp(760.0, 690.0), cols=tp(*basement_cols()[0][2:]), pool=tp(1290.0, 515.0),
                   tower=tp(970.0, 300.0), k131=gp("K", "13.1"), l131=gp("L", "13.1"), lobby=tp(785.0, 325.0),
                   drive=tp(550.0, 720.0), planters=tp(1200.0, 420.0), palm=tp(1046.0, 393.0),
                   leak=tp(LEAK[0], LEAK[1] + LEAK[3]), gate=tp(*DMG_PTS["gate"]), planter=tp(*DMG_PTS["planter"]),
                   water=tp(*DMG_PTS["water"]), vis=tp(1300.0, 600.0), eye=tp(*NORTH_EYE), debris=tp(1000.0, 700.0),
                   around=tp(785.0, 505.0), cand=gp("M", "15"), red=gp("M", "13.1"), yel=gp("N", "15"))
        return out
    if view == "cam":
        return dict(unit=cp(675.0, 360.0), eye=cp(*CAM_EYE), l8=cp(CAM_X["L"], CAM_Y["8"]), m8=cp(CAM_X["M"], CAM_Y["8"]))
    if view == "flat":
        return dict(joint=(FLAT_COLS[2] + 18, FLAT_FLOORS[0][0] + 13), slab=(FLAT_COLS[1] + 160, FLAT_FLOORS[0][0]))
    if view == "punch":
        c, h = PU["cx"], PU["cw"] / 2
        dy = PU["drop"] if st["drop"] == "on" else 0.0
        return dict(slab=(560.0, PU["top"] + dy), col=(c, 300.0), hook=(c - h - 40, PU["bar"] + 70),
                    crack=(c - h - PU["cone"] / 2, (PU["top"] + PU["bot"]) / 2 + dy), react=(c + 10, 700.0))
    if view == "gspan":
        return dict(k131=(GS_ROW["13.1"], GS["top"]), adj=(GS_ROW["11.1"], GS["top"]), sag=(GS_ROW["13.1"] + 80, GS["top"] + 8))
    if view == "core":
        L = core_levels()
        return dict(paver=(CORE["x1"], (L["paver"] + L["sand"]) / 2), sand=(CORE["x1"], (L["sand"] + L["tile"]) / 2),
                    memb=(CORE["x1"], L["tile"]), tile=(CORE["x0"], (L["tile"] + L["topping"]) / 2),
                    topping=(CORE["x0"], (L["topping"] + L["slab"]) / 2))
    if view == "water":
        return dict(pond=(820.0, WA["top"] - 8), slope=(400.0, 540.0), fix=(580.0, WA["top"] + 20), memb2=(1400.0, 572.0))
    if view == "drip":
        return dict(drip=(DR["cx"] + 12, 580.0), crack=(DR["cx"], DR["top"] + 30))
    if view == "edge":
        jx, jy = edge_joint_xy()
        return dict(joint=(jx - 40, jy), beam=(1200.0, ED["top"]), face=(ED["tcol"], 262.0), deck=(600.0, 772.0))
    if view == "joint":
        c, h = JO["cx"], JO["cw"] / 2
        return dict(col=(c + h, 380.0), floor=(600.0, JO["f0"]), zone=(c + h + 34, (JO["f0"] + JO["f1"]) / 2), bars=(c + 55, 555.0))
    if view == "front":
        return dict(q=(FR["heads"][1] + 12, FR["gy"] - 60), heads=(FR["heads"][1] + 10, FR["top"] + 20), dir=(1690.0, 400.0))
    if view == "zoneb":
        return dict(one=(ZB["brk"] + 30, ZB["top"] - 40), two=(ZB_COL["E"] - 30, ZB["top"] - 40), bar=(ZB_TOP[1][1], ZB["top"] + 7),
                    zone=(ZB_COL["H"], 340.0))
    if view == "rubble":
        return dict(bld=(RB["b1"], RB["top"] + 60), pile=(1200.0, 640.0), eye=RB_EYES[0])
    if view == "excav":
        return dict(pit=(330.0, 600.0), pile=(EX["pile"], 400.0), dist=((EX["pile"] + EX["wall"]) / 2, EX["gy"] - 54),
                    wave=(EX["pile"] + 110, 640.0), wall=(EX["wall"] + 12, 700.0), joint=(EX_ROW["13.1"], EX["deck_b"]))
    if view == "ground":
        return dict(lime=(300.0, 760.0), cave=(1680.0, 520.0), pile=(GR_PILES[3], 700.0), floor=(900.0, GR["slab0"]),
                    none=(880.0, 720.0))
    if view == "cover":
        (a0, a1), (b0, b1) = CV["panels"]
        return dict(dwg=(a0 - 26, (CV["top"] + cover_bar_y("dwg")) / 2), real=(b0 - 26, (CV["top"] + cover_bar_y("real")) / 2),
                    weak=(b1 + 60, 470.0))
    if view == "ruler":
        return dict(old=(RU["x0"], RU["y"][0]), new=(RU["x0"], RU["y"][1]), have=(RU["x0"] + 200, RU["y"][1] + 60),
                    gap=(RU["need"], RU["y"][0] + 60), limit=(1200.0, RU["y"][0]))
    if view == "rebar":
        a, b = RB_C["panels"]
        return dict(dwg=(a, RB_C["y"] - RB_C["half"]), real=(b, RB_C["y"] - RB_C["half"]), weak=(b + RB_C["span"] + 80, 420.0))
    if view == "hall":
        return dict(ref=(HA["x0"] + 300, HA["ftop"]), sag=(HA_COL["K"] + 140, HA["ftop"] + 20), cam=HA["cam"],
                    i=(HA_COL["I"], HA["ftop"]))
    return {}


L_, R_ = 88.0, 1500.0           # 上から見た図の左の余白（通りより西）・右の余白（海）
TAG_AT = dict(
    site=dict(tower=(L_, 330.0, "start", 330.0), deck=(R_, 650.0, "start", 330.0), park=(L_, 690.0, "start", 330.0),
              cols=(R_, 760.0, "start", 330.0), pool=(R_, 520.0, "start", 330.0)),
    planter=dict(box=(R_, 340.0, "start", 330.0), palm=(R_, 430.0, "start", 330.0), wp=(R_, 560.0, "start", 330.0),
                 wd=(R_, 680.0, "start", 330.0), q=(L_, 400.0, "start", 330.0), margin=(L_, 760.0, "start", 330.0)),
    dig=dict(under=(L_, 380.0, "start", 330.0), strip=(R_, 360.0, "start", 330.0), deck=(R_, 650.0, "start", 330.0),
             drive=(L_, 760.0, "start", 330.0), park=(L_, 600.0, "start", 330.0)),
    cand=dict(cand=(R_, 690.0, "start", 330.0), k131=(L_, 560.0, "start", 330.0)),
    seq=dict(l131=(R_, 470.0, "start", 330.0), k131=(L_, 560.0, "start", 330.0), l2=(R_, 580.0, "start", 330.0),
             around=(L_, 420.0, "start", 330.0), next=(R_, 720.0, "start", 330.0), n24=(R_, 720.0, "start", 330.0),
             two=(L_, 700.0, "start", 330.0)),
    dmg=dict(leak=(R_, 380.0, "start", 330.0), gate=(L_, 480.0, "start", 330.0), planter=(L_, 640.0, "start", 330.0),
             water=(R_, 600.0, "start", 330.0), leak2=(R_, 470.0, "start", 330.0)),
    sight=dict(vis=(R_, 600.0, "start", 330.0), lobby=(L_, 330.0, "start", 330.0), sound=(L_, 440.0, "start", 330.0)),
    code=dict(red=(R_, 360.0, "start", 330.0), yel=(R_, 470.0, "start", 330.0), orig=(L_, 760.0, "start", 330.0)),
    model=dict(calc=(R_, 600.0, "start", 330.0), nist=(L_, 330.0, "start", 330.0)),
    cam=dict(unit=(1250.0, 420.0, "start", 560.0), clock=(1250.0, 560.0, "start", 560.0), l8=(1250.0, 700.0, "start", 560.0)),
    # layout：上だと引き出し線が「通り」の字を横切った＝eye を下げる
    north=dict(eye=(L_, 430.0, "start", 330.0), debris=(R_, 680.0, "start", 330.0)),
    sat=dict(q=(L_, 330.0, "start", 330.0), sat=(R_, 430.0, "start", 330.0), near=(R_, 700.0, "start", 330.0)),
    flat=dict(name=(FLAT_X[0], 372.0, "start", 560.0), plate=(1500.0, 470.0, "start", 330.0), joint=(1500.0, 640.0, "start", 330.0)),
    punch=dict(q=(300.0, 330.0, "start", 520.0), slab=(300.0, 400.0, "start", 520.0), react=(1060.0, 760.0, "start", 520.0),
               hook=(300.0, 790.0, "start", 520.0), scis=(1430.0, 500.0, "start", 400.0), shear=(1060.0, 820.0, "start", 520.0),
               crack=(300.0, 790.0, "start", 520.0), wide=(1060.0, 400.0, "start", 520.0), code=(1060.0, 330.0, "start", 520.0)),
    # layout：punch が k131 の2行目と重なった＝下げる
    gspan=dict(k131=(980.0, 330.0, "start", 420.0), punch=(980.0, 414.0, "start", 520.0), ok=(980.0, 330.0, "start", 500.0),
               share=(560.0, 330.0, "start", 360.0), dim=(1000.0, 560.0, "start", 460.0)),
    core=dict(new=(1220.0, 470.0, "start", 560.0), tile=(300.0, 620.0, "start", 400.0), memb=(1220.0, 560.0, "start", 560.0),
              load=(1220.0, 360.0, "start", 560.0)),
    water=dict(q=(200.0, 330.0, "start", 640.0), flat=(1120.0, 470.0, "start", 640.0), err=(200.0, 790.0, "start", 900.0),
               strip=(200.0, 400.0, "start", 640.0), slope=(1000.0, 420.0, "start", 720.0), cost=(200.0, 790.0, "start", 900.0)),
    drip=dict(h9=(1400.0, 440.0, "start", 420.0), h3=(1400.0, 700.0, "start", 420.0)),
    edge=dict(q=(560.0, 330.0, "start", 640.0), face=(560.0, 330.0, "start", 640.0), deck=(560.0, 390.0, "start", 640.0),
              joint=(1460.0, 620.0, "start", 380.0), hold=(560.0, 330.0, "start", 640.0), crush=(560.0, 390.0, "start", 640.0),
              drop=(1460.0, 600.0, "start", 380.0), beam=(560.0, 390.0, "start", 640.0), pull=(560.0, 330.0, "start", 640.0),
              load=(1460.0, 600.0, "start", 380.0)),
    joint=dict(q=(1100.0, 330.0, "start", 560.0), col=(1100.0, 400.0, "start", 560.0), floor=(260.0, 400.0, "start", 560.0),
               ratio=(668.0, 800.0, "start", 200.0), ties=(1100.0, 600.0, "start", 560.0), buckle=(1100.0, 700.0, "start", 560.0),
               dense=(1100.0, 800.0, "start", 560.0), crush=(1100.0, 600.0, "start", 560.0), code=(1100.0, 760.0, "start", 560.0)),
    # layout：上に置くと2行目が「東の部分」の字に重なった＝東の部分の右（x 1520〜）
    front=dict(q=(1530.0, 780.0, "start", 310.0), heads=(1530.0, 640.0, "start", 310.0), dir=(1680.0, 540.0, "start", 160.0)),
    # 柱（330〜850）を横切らない＝E と H のあいだ（617〜1043）・D と E のあいだ（317〜583）に置く
    zoneb=dict(zone=(630.0, 380.0, "start", 400.0), one=(630.0, 455.0, "start", 400.0), two=(325.0, 455.0, "start", 250.0),
               bar=(630.0, 650.0, "start", 400.0)),
    rubble=dict(bld=(760.0, 330.0, "start", 560.0), watch=(1100.0, 480.0, "start", 560.0)),
    # 鋼の板と打つ機械（x 530〜590・y 240〜470）を横切らない
    excav=dict(pit=(110.0, 430.0, "start", 400.0), pile=(780.0, 330.0, "start", 640.0), dist=(780.0, 400.0, "start", 640.0),
               wave=(780.0, 330.0, "start", 640.0), damp=(780.0, 330.0, "start", 640.0), joint=(780.0, 400.0, "start", 640.0)),
    # ⑤b-4 の下見：下の札は石灰岩（薄茶）の上で読みにくく、くいの先に掛かった＝右の暗い所へ
    ground=dict(lime=(110.0, 300.0, "start", 240.0), cave=(1480.0, 700.0, "start", 360.0), none=(1480.0, 790.0, "start", 360.0),
                pile=(1480.0, 560.0, "start", 360.0), floor=(500.0, 400.0, "start", 860.0)),
    cover=dict(dwg=(200.0, 330.0, "start", 640.0), real=(1060.0, 330.0, "start", 640.0), weak=(1060.0, 820.0, "start", 640.0),
               diff=(200.0, 820.0, "start", 640.0)),
    ruler=dict(old=(420.0, 360.0, "start", 640.0), new=(420.0, 580.0, "start", 640.0), have=(420.0, 790.0, "start", 900.0),
               short=(1330.0, 520.0, "start", 500.0), gap=(1330.0, 470.0, "start", 500.0), limit=(1330.0, 330.0, "start", 500.0)),
    rebar=dict(dwg=(340.0, 300.0, "start", 560.0), real=(1140.0, 300.0, "start", 560.0), space=(340.0, 830.0, "start", 760.0),
               weak=(1140.0, 830.0, "start", 640.0)),
    hall=dict(ref=(300.0, 790.0, "start", 640.0), sag=(1000.0, 560.0, "start", 720.0), still=(1000.0, 790.0, "start", 700.0)),
)


# ══════════════════════════════════════════════════════════
#  組み立て（mech18 と同じ）
# ══════════════════════════════════════════════════════════
def parts_of(view, st):
    fn = VIEWS[view].get("parts")
    return fn(st) if fn else []


def _states(view, start, steps):
    fields = VIEWS[view]["fields"]
    cur = dict(START[view], **(start or {}))
    out = []
    for st in [dict(state={})] + list(steps):
        cur = dict(cur, **(st.get("state") or {}))
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m19：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m19：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    for f_, seq in ORDER.get(view, {}).items():
        if f_ in fields:
            idx = [seq.index(s[f_]) for s in out]
            if any(b < a for a, b in zip(idx, idx[1:])):
                raise ValueError(f"m19：{f_} は戻さない（{' → '.join(seq)}）")
    return out[0], out[1:]


def stage_art(view, prev, st):
    return VIEWS[view]["stage"](prev, st)


def _base(view, start):
    st = dict(START[view], **(start or {}))
    return VIEWS[view]["base"](st) + stage_art(view, START[view], st)


def _stage_svgs(view, steps, start, states, cap=34):
    pre = TAG_AT[view]
    stages, texts = [], []
    prev = start
    for st, stt in zip(steps, states):
        s = stage_art(view, prev, stt)
        an = anchors(view, stt)
        for tg in F._many(st.get("tag")):
            at = tg.get("at", next(iter(pre)))
            x, y, anchor, mw = pre[at] if isinstance(at, str) else (tuple(at) if len(at) == 4 else (at[0], at[1], "start", 420))
            c = tg.get("cap", cap)
            if tg.get("to"):
                tx, ty = an[tg["to"]] if isinstance(tg["to"], str) else tg["to"]
                sy = y - round(c * 0.9) if ty < y - c else y + 8
                sx = x if anchor == "start" else (x - mw / 2 if anchor == "middle" else x)
                s.append(F.line(sx, sy, tx, ty, J.AMBER, 2))
            s.append(F.txtfit(x, y, tg["t"], mw, cap=c, col=tg.get("col", J.AMBER), anchor=anchor))
            texts.append(tg["t"])
            if tg.get("d"):
                s.append(F.txtfit(x, y + round(c * 0.95), tg["d"], mw, cap=round(c * 0.62), col=J.TICK, anchor=anchor))
                texts.append(tg["d"])
        stages.append("".join(s) or " ")
        prev = stt
    return stages, texts


def _static_part(sh):
    a = float(sh["keys"][0].get("alpha", 1.0))
    if a <= 0.01:
        return ""
    if sh["type"] == "circle":
        return F.circ(sh["c"][0], sh["c"][1], sh["r"], sh.get("fill", "none"), sh.get("stroke"), sh.get("w"))
    pts = F.mech_pts(sh, sh["keys"][0])
    if sh["type"] == "poly":
        return F.poly(pts, sh.get("fill", "none"), sh.get("stroke"), sh.get("w") or None, close=True,
                      op=(round(a, 2) if a < 0.99 else None))
    return F.poly(pts, "none", sh.get("stroke"), sh.get("w"), op=(round(a, 2) if a < 0.99 else None))


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def m19(view, steps, start=None, rel=(), note="", src=""):
    """19本目の模式図。view は VIEWS の29種。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m19：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if "模式" not in note:
        raise ValueError("m19：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    seq = [st0] + states
    per = [parts_of(view, s) for s in seq]
    shapes, anim = [], []
    for j, p0 in enumerate(per[0]):
        keys = []
        for i, ps in enumerate(per):
            pj = ps[j]
            kk = {f_: pj[f_] for f_ in KEY_FIELDS if f_ in pj}
            kk.setdefault("alpha", 1.0)
            dl = 0.0 if i == 0 else float(steps[i - 1].get("delay", 1.0 if i == 1 else F.MECH_DELAY))
            keys.append(dict(stage=max(0, i - 1), delay=dl, **kk))
        sh = {f_: p0[f_] for f_ in p0 if f_ not in ("alpha", "dx", "dy", "rot")}
        sh["keys"] = keys
        moving = any({f_: kk.get(f_) for f_ in KEY_FIELDS} != {f_: keys[0].get(f_) for f_ in KEY_FIELDS} for kk in keys[1:])
        sh["anim"] = bool(moving)
        shapes.append(sh)
        if moving:
            anim.append(sh)
    g = _base(view, start or {})
    for sh in shapes:
        if not sh["anim"]:
            g.append(_static_part(sh))
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, VIEWS[view]["lab"] + "・模式", 1000, cap=28, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, st0, states)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="m19", view=view, start=st0, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M19）
# ══════════════════════════════════════════════════════════
def _grid_name(X, Y, tol=3.0):
    for c in COLX:
        for r in ROWY:
            gx, gy = gp(c, r)
            if abs(gx - X) <= tol and abs(gy - Y) <= tol:
                return f"{c}-{r}"
    return None


def geo_of(view, start, states):
    allst = [start] + list(states)
    last = allst[-1]

    def ever(f, v="on"):
        return any(s.get(f) == v for s in allst)
    out = dict(view=view)
    if view == "cand":
        out["cand"] = [_grid_name(*gp(c, r)) for c, r in CAND] if ever("cand") else []
        out["red"] = [_grid_name(*gp(c, r)) for c, r in FIRST2] if ever("red") else []
    elif view == "seq":
        out["punched"] = ([_grid_name(*gp("K", "13.1"))] if ever("first") else []) + ([_grid_name(*gp("L", "13.1"))] if ever("second") else [])
        out["around"] = [_grid_name(*gp(c, r)) for c, r in AROUND] if ever("around") else []
    elif view == "code":
        out["red"] = [_grid_name(*gp(c, r)) for c, r in CODE_DOTS["red"]] if ever("dots") else []
        out["yel"] = [_grid_name(*gp(c, r)) for c, r in CODE_DOTS["yel"]] if ever("dots") else []
    elif view == "dmg":
        out["leak"] = list(LEAK[:2])
        out["gate"] = list(DMG_PTS["gate"])
        out["water"] = list(DMG_PTS["water"])
        out["planter"] = list(DMG_PTS["planter"])
        out["planter_box"] = list(IL.A2_PLANTER)
    elif view == "sight":
        out["vis"] = [list(p) for p in VISIBLE] if ever("vis") else []
        out["deck"] = [list(p) for p in IL._a2_zone_fp()[1]]
    elif view == "planter":
        out["boxes"] = [list(b) for b in PLANTERS] if ever("box") else []
        out["band"] = [A2T["ts"], A2_ROW["11.1"]]
        out["deck_x"] = [A2T["K"], A2T["x1"]]
        out["palm_after"] = [p["alpha"] for p in planter_parts(last)]
    elif view == "cam":
        out["move"] = ["L-8", "L-9.1"] if ever("move") else []
        out["still"] = ["M-8", "M-9.1"] if ever("move") else []
        out["unit"] = [CAM_UNIT[0], CAM_UNIT[2]]
        out["grid"] = dict(L=CAM_X["L"], M=CAM_X["M"])
    elif view == "hall":
        f = hall_floor(last["sag"] == "on")
        out["dy"] = {c: next(y for x, y in f if x == HA_COL[c]) - HA["ftop"] for c in ("I", "K", "L")}
    elif view == "flat":
        out["joints"] = len(flat_joints()) if ever("joint") else 0
        out["n"] = len(FLAT_COLS) * len(FLAT_FLOORS)
        out["beams"] = 0
    elif view == "punch":
        c, h = PU["cx"], PU["cw"] / 2
        top, bot = (c - h - PU["cone"], PU["top"]), (c - h, PU["bot"])
        out["crack"] = [list(top), list(bot)]
        out["col_face"] = c - h
        out["shear"] = dict(col=(840.0, 700.0), slab=(PU["top"] + PU["drop"] - 70, PU["bot"] + PU["drop"] + 60)) if ever("shear") else None
        out["react"] = (800.0, 640.0) if ever("react") else None
    elif view == "gspan":
        s = parts_of("gspan", last)[0]["pts"]
        out["dy"] = {r: next(y for x, y in s[:5] if x == xx) - GS["top"] for r, xx in GS_ROW.items()}
        out["share_to"] = ["15", "11.1"] if ever("share") else []
    elif view == "core":
        L = core_levels()
        out["thick"] = dict(topping=L["slab"] - L["topping"], tile=L["topping"] - L["tile"],
                            top=(L["tile"] - L["paver"]) if ever("new") else 0.0)
    elif view == "water":
        out["slab_y"] = (WA["top"], WA["top"])
        out["pond_with_slope"] = any(s["pond"] == "on" and s["slope"] == "on" and s["strip"] != "on" for s in allst)
    elif view == "edge":
        out["beam_x"] = [ED_ROW["11.1"], ED["tcol"] - ED["cw"] / 2]
        out["joint_x"] = edge_joint_xy()[0]
        out["row91"] = ED_ROW["9.1"]
        out["fall_full_end"] = ED_SLAB_X[-1]
    elif view == "joint":
        out["ties"] = list(JO_TIES)
        out["floor"] = [JO["f0"], JO["f1"]]
        out["bar2"] = JO_STRENGTH[1] / JO_STRENGTH[0] if ever("bar2") else None
        out["colors"] = dict(col=COL["colg"], floor=COL["conc_lt"])
    elif view == "front":
        d = FR["drop"] if last["roof"] == "down" else 0.0
        out["roof_top"] = FR["top"] - 8 + d
        out["head_top"] = FR["top"] - 30
        out["heads_shown"] = last["roof"] == "down"
    elif view == "zoneb":
        out["brk"] = ZB["brk"]
        out["E"] = ZB_COL["E"]
        out["topbar_end"] = ZB_TOP[1][1]
        out["rot"] = [p.get("rot", 0.0) for p in zoneb_parts(last)]
        out["pivot_x"] = ZB["brk"]
    elif view == "excav":
        out["amps"] = [list(a) for a in EX_AMP]
        out["walls"] = [EX["ctsp"], EX["wall"]]
        out["pile"] = EX["pile"]
        out["joint"] = EX_ROW["13.1"]
    elif view == "ground":
        out["cave"] = [list(p) for p in GR_CAVE] if ever("cave") else []
        out["bld"] = [GR["x0"], GR["x1"]]
    elif view == "cover":
        out["cover"] = dict(dwg=cover_bar_y("dwg") - CV["r"] - CV["top"], real=cover_bar_y("real") - CV["r"] - CV["top"])
    elif view == "ruler":
        out["need"] = [RU["need"], RU["need"]]
        out["have"] = [RU["have"], RU["have"]] if ever("short") else []
    elif view == "rebar":
        h = RB_C["half"]
        out["over"] = dict(dwg=sum(1 for o in rebar_offsets("dwg") if abs(o) < h), real=sum(1 for o in rebar_offsets("real") if abs(o) < h))
        sd = sorted(rebar_offsets("dwg"))
        sr = sorted(rebar_offsets("real"))
        out["space"] = dict(dwg=sd[1] - sd[0], real=sr[1] - sr[0])
    elif view == "sat":
        out["cells"] = [SAT_NEUTRAL] * len(sat_cells()) if ever("sat") else []
        out["neutral"] = SAT_NEUTRAL
    elif view == "drip":
        out["flow"] = [s["flow"] for s in allst]
    return out
