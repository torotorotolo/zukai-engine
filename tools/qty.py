# -*- coding: utf-8 -*-
"""qty.py — 量の型「棒・マス目・人の形」（2026-09-29 新設・14本目 ⑤b-6）。

■ 何か（Vault `Projects/事故検証-14本目-映像方針-追補-文字の画面-20260926.md` §3 の【棒】【マス】【人の形】）
  数を**長さ・マス・形の数**で見せる図解。数字の読み上げは字幕に任せ、図は項目名・単位・目盛りだけを持つ（§5b-9）。
  13本目までの `titan_fig.compare`（棒の上に大きな数字）・`icons`（数を名乗る絵）は**数字を画面に書く**＝使わない。
  15本目も使い回す（棒）。記録の値と頁は `cuts/ss.py` の `QG`・`QB`・`PEOPLE_*`（§0b）。

■ 見え方（view）
  bar    … 棒。群（groups）ごとに尺（ticks＝0 から）と項目名（単位つき）。棒の長さ＝記録の値
  grid   … マス目。1マス＝1項目。段で ✓（ok）・✕（ng）を左から置く
  people … 人の形。🔴 **1つ＝1人**（顔の無い同じ形）で乗っていた人の全員を並べ、色で分ける
           🔴 **14本目 c204〜c206 だけ**（ルール §C-1 #59・§5b-74②の例外）＝亡くなった方の数には使わない・同じ並びを
              後の章で灰色にしない（門番 check_qty が `ss.PEOPLE_CUTS` の外で止める）

■ SPEC の書き方
  fig=("qty", dict(view="bar", groups=[ss.QG["cargo"]], past=[…], steps=[dict(add=[ss.qb("cargo_before"), …]), …],
                   note="…", src=ss.src([…])))
    部品：dict(k="bar", g="cargo", t="改造の前", v=2437, rec="海審 p1018", c="TICK")   … 棒（t＝行の名。数字は書かない）
          dict(k="ghost", g="cargo", row="改造の後", v=2437, rec="海審 p1018")        … その行に「もとの長さ」の破線の枠
    群：dict(id="cargo", t="積める貨物の上限（トン）", ticks=(0, 500, …), rows=("上限", "積み荷"))  … rows は行の順（省略＝出た順）
  fig=("qty", dict(view="grid", n=9, title="判定の項目", steps=[…, dict(add=dict(k="ok", n=5, rec="海審 p1080"))], src=…))
  fig=("qty", dict(view="people", order=ss.PEOPLE_ORDER, sets=ss.PEOPLE_SETS,
                   steps=[dict(add=[dict(k="lit", who="乗客", c="LINE", rec="海審 p1038"), …]), …], src=…))
    lit … who（order の区分か sets の名）の形を c の色に灯し、凡例に1行足す。parent＝凡例で字下げする親の名
  past … 前のカットの部品を基図に沈んだ色で（keep=True なら沈めない）

■ 門番 `check_qty`（🔴 焼く直前の SVG を読む＝この型が置いた `data-q`／`data-p` の要素の画素と色）
  ① 棒：目盛りの画素から一次式を当てて棒の端を値へ戻す＝記録の値（門番の側の `REC_QTY`）・棒は 0 から・目盛りの文字
  ② マス目：マスの数・✓・✕ の数＝記録  ③ 人の形：形の数を色ごとに数える（段ごと・章の色に置き換えたあと）＝記録・
  同じ大きさ・重ならない・色どうしが取り違えない距離・c204〜c206 の外で使わない  ④ 画面の数字は目盛りと「1つ＝1人」だけ
"""
from __future__ import annotations

import math
import re

import jiko_style as J
import titan_fig as F

VIEWS = ("bar", "grid", "people")

# ── 棒 ──────────────────────────────────────────────
BAR_X0 = F.BX0 + 330          # 0 の位置（左に行の名）
BAR_X1 = F.BX1 - 90           # 尺の右端（最後の目盛り）
LAB_X = BAR_X0 - 24           # 行の名の右端
TOP, BOT = F.BY0 + 40, F.BY1 - 50
GT_H, AX_H, G_GAP = 56, 58, 44
BAR_OP = 0.35                 # 棒の塗り（基図・段の層＝SVG＝動く部品ではない §5b-91）
# ── マス目 ──────────────────────────────────────────
CELL, CELL_GAP = 150, 24
# ── 人の形 ──────────────────────────────────────────
PCOLS = 34                    # 476＝34×14（1つ＝1人）
P_X0, P_X1 = F.BX0 + 20, F.BX0 + 1368
P_Y0, P_Y1 = F.BY0 + 64, F.BY1 - 56
LEG_X0, LEG_X1 = F.BX0 + 1392, F.BX1 - 8
LEG_Y0, LEG_STEP, LEG_IND = F.BY0 + 120, 62, 34
DIM = "LINE_DIM"              # 灯していない形（🔴 門番：灰色＝TICK などで「亡くなった」に読める色を使わない）
UNIT = "1つ＝1人"             # 🔴 門番の陽性対照がここを壊す
KIND_GRID = "1マス＝1項目"


def _c(name, dflt):
    nm = name or dflt
    return nm if nm.startswith("#") else getattr(J, nm)


def dq(svg, q):
    """SVG の最初の要素に門番の印 data-q を付ける（画面には出ない）。"""
    return re.sub(r"^<(\w+) ", lambda m: f'<{m[1]} data-q="{F.esc(q)}" ', svg, count=1)


def _kind(t):
    return dq(F.txt(F.BX0 + 8, F.BY0 + 34, t, 28, J.TICK), "kind")


def _foot(note, src):
    s = (note or "") + (("　" if note else "") + f"出典：{src}" if src else "")
    return dq(F.txtfit(F.BX0, F.BY1 - 6, s, F.BW, cap=26, col=J.TICK), "note") if s else ""


# ══════════════════════════════════════════════════════════
#  棒
# ══════════════════════════════════════════════════════════
def _bar(groups, past, steps, note, src):
    gs = {g["id"]: dict(g) for g in groups}
    parts = list(past) + [x for st in steps for x in F._many(st.get("add"))]
    for g in gs.values():
        tk = list(g["ticks"])
        if len(tk) < 2 or tk[0] != 0 or any(b <= a for a, b in zip(tk, tk[1:])):
            raise ValueError(f"qty：群 {g['id']} の目盛り {tk} は 0 から増える順に2つ以上（棒は 0 から＝途中から始まる軸は長さが嘘をつく）")
        rows = list(g.get("rows") or [])
        for p in parts:
            if p.get("g") == g["id"] and p["k"] == "bar" and p["t"] not in rows:
                rows.append(p["t"])
        g["_rows"] = rows
    for p in parts:
        if p["k"] not in ("bar", "ghost"):
            raise ValueError(f"qty：棒の見え方に知らない部品 {p['k']!r}")
        if not p.get("rec"):
            raise ValueError(f"qty：rec（記録の頁）が無い部品 {p}")
        if p["g"] not in gs:
            raise ValueError(f"qty：群 {p['g']!r} が groups に無い")
        if p["k"] == "bar" and not (0 < p["v"] <= gs[p["g"]]["ticks"][-1]):
            raise ValueError(f"qty：棒 {p['t']} の値 {p['v']} が尺 0〜{gs[p['g']]['ticks'][-1]} の外")
    nr = sum(len(g["_rows"]) for g in gs.values())
    ng = len(gs)
    rh = min(110.0, max(48.0, (BOT - TOP - ng * (GT_H + AX_H) - (ng - 1) * G_GAP) / (nr * 1.3)))
    step = rh * 1.3
    tot = sum(GT_H + len(g["_rows"]) * step - (step - rh) + AX_H for g in gs.values()) + (ng - 1) * G_GAP
    gy = TOP + max(0.0, (BOT - TOP - tot) / 2)
    for g in gs.values():
        g["_y"] = gy
        g["_ry"] = {r: gy + GT_H + i * step for i, r in enumerate(g["_rows"])}
        g["_ay"] = gy + GT_H + len(g["_rows"]) * step - (step - rh) + 14
        gy = g["_ay"] + AX_H - 14 + G_GAP

    def gx(g, v):
        return BAR_X0 + (BAR_X1 - BAR_X0) * v / g["ticks"][-1]

    live = {p["g"] for st in steps for p in F._many(st.get("add"))} | {p["g"] for p in past if p.get("keep")}
    lab = []
    for gid, g in gs.items():
        dim = gid not in live
        ink = J.TICK if dim else J.INK_W
        ln = J.LINE_DIM if dim else J.LINE
        lab.append(dq(F.txtfit(F.BX0 + 20, g["_y"] + 34, g["t"], BAR_X1 - F.BX0 - 20, cap=34, col=ink), f"gt|{gid}"))
        y0 = g["_y"] + GT_H - 10
        lab.append(F.line(BAR_X0, y0, BAR_X0, g["_ay"], ln, 4))
        lab.append(F.line(BAR_X0, g["_ay"], BAR_X1, g["_ay"], ln, 4))
        for v in g["ticks"]:
            x = gx(g, v)
            lab.append(dq(F.line(x, g["_ay"] - 10, x, g["_ay"] + 10, ln, 3), f"tick|{gid}|{v}"))
            lab.append(dq(F.txt(x, g["_ay"] + 40, str(v), 28, J.TICK, "Noto", "middle"), f"tlab|{gid}|{v}"))
    rec_parts = []

    def draw(p, dim):
        g = gs[p["g"]]
        col = J.LINE_DIM if dim else _c(p.get("c"), "LINE")
        out = []
        if p["k"] == "bar":
            y = g["_ry"][p["t"]]
            w = gx(g, p["v"]) - BAR_X0
            out.append(F.rect(BAR_X0, y, w, rh, col, op=0.25 if dim else BAR_OP))
            out.append(dq(F.rect(BAR_X0, y, w, rh, "none", col, 4), f"bar|{p['g']}|{p['t']}"))
            out.append(dq(F.txtfit(LAB_X, y + rh / 2 + 12, p["t"], LAB_X - F.BX0 - 20, cap=36,
                                   col=J.TICK if dim else J.INK_W, anchor="end"), f"rlab|{p['g']}|{p['t']}"))
        else:
            if p["row"] not in g["_ry"]:
                raise ValueError(f"qty：ghost の行 {p['row']!r} が群 {p['g']} に無い")
            y = g["_ry"][p["row"]]
            out.append(dq(F.rect(BAR_X0, y - 6, gx(g, p["v"]) - BAR_X0, rh + 12, "none", J.TICK, 3, dash="14 10"),
                          f"ghost|{p['g']}|{p['row']}"))
        rec_parts.append(dict(p, dim=dim))
        return "".join(out)

    for p in past:
        lab.append(draw(p, dim=not p.get("keep")))
    stages = []
    for st in steps:
        stages.append("".join(draw(p, False) for p in F._many(st.get("add"))) or " ")
    lab.append(_foot(note, src))
    f = F.Fig("".join(lab), stages, "", (F.BX0, F.BX1))
    f.mech = dict(kind="qty", view="bar", parts=rec_parts, groups={k: dict(t=g["t"], ticks=list(g["ticks"])) for k, g in gs.items()})
    return f


# ══════════════════════════════════════════════════════════
#  マス目
# ══════════════════════════════════════════════════════════
def _grid(n, title, steps, cols, note, src):
    cols = cols or n
    rows = math.ceil(n / cols)
    wtot = cols * CELL + (cols - 1) * CELL_GAP
    x0 = F.BCX - wtot / 2
    htot = rows * CELL + (rows - 1) * CELL_GAP
    y0 = F.BY0 + (F.BH - htot) / 2 + 10
    cells = [(x0 + (i % cols) * (CELL + CELL_GAP), y0 + (i // cols) * (CELL + CELL_GAP)) for i in range(n)]
    lab = [_kind(KIND_GRID)]
    if title:
        lab.append(dq(F.txtfit(x0, y0 - 30, title, wtot, cap=34, col=J.INK_W), "gt|grid"))
    for x, y in cells:
        lab.append(dq(F.rect(x, y, CELL, CELL, J.BG2, J.LINE, 4, rx=10), "cell"))
    used = 0
    stages, marks = [], []
    for st in steps:
        s = []
        for p in F._many(st.get("add")):
            if p["k"] not in ("ok", "ng"):
                raise ValueError(f"qty：マス目に知らない部品 {p['k']!r}（ok／ng）")
            if not p.get("rec"):
                raise ValueError(f"qty：rec（記録の頁）が無い部品 {p}")
            if used + p["n"] > n:
                raise ValueError(f"qty：印が {used + p['n']} 個＝マス {n} を超える")
            for x, y in cells[used:used + p["n"]]:
                if p["k"] == "ok":
                    pts = [(x + 34, y + 80), (x + 64, y + 112), (x + 118, y + 42)]
                    g = F.poly(pts, "none", J.OK, 14)
                else:
                    g = (F.line(x + 38, y + 38, x + 112, y + 112, J.ALERT, 14)
                         + F.line(x + 112, y + 38, x + 38, y + 112, J.ALERT, 14))
                s.append(f'<g data-q="{p["k"]}">{g}</g>')
            used += p["n"]
            marks.append(dict(p))
        stages.append("".join(s) or " ")
    lab.append(_foot(note, src))
    f = F.Fig("".join(lab), stages, "", (F.BX0, F.BX1))
    f.mech = dict(kind="qty", view="grid", n=n, marks=marks)
    return f


# ══════════════════════════════════════════════════════════
#  人の形（1つ＝1人）
# ══════════════════════════════════════════════════════════
def person(cx, top, cw, ch):
    """1人の形（顔なし）＝頭の12角形＋肩の角を落とした胴。M・L・Z だけ（門番が点から外接の箱を出せる）。"""
    r = cw * 0.17
    hy = top + ch * 0.25
    head = "M" + " L".join(f"{cx + r * math.cos(k * math.pi / 6):.1f} {hy + r * math.sin(k * math.pi / 6):.1f}"
                           for k in range(12)) + " Z"
    bw, sy, by = cw * 0.50, top + ch * 0.48, top + ch * 0.96
    k = bw * 0.28
    xa, xb = cx - bw / 2, cx + bw / 2
    body = (f"M{xa:.1f} {by:.1f} L{xa:.1f} {sy + k:.1f} L{xa + k:.1f} {sy:.1f} L{xb - k:.1f} {sy:.1f} "
            f"L{xb:.1f} {sy + k:.1f} L{xb:.1f} {by:.1f} Z")
    return head + " " + body


def slots(order, cols=PCOLS):
    """並びの全員の置き場（左上から行ごと）。戻り＝[(区分の名, cx, top, cw, ch)]。🔴 門番も同じ関数で数える。"""
    tot = sum(n for _, n in order)
    rows = math.ceil(tot / cols)
    cw = (P_X1 - P_X0) / cols
    ch = min(cw * 1.05, (P_Y1 - P_Y0) / rows)
    out = []
    for nm, n in order:
        for _ in range(n):
            i = len(out)
            out.append((nm, P_X0 + (i % cols + 0.5) * cw, P_Y0 + (i // cols) * ch, cw, ch))
    return out


def _who(who, order, sets):
    names = [nm for nm, _ in order]
    if who in names:
        return {who}
    if who in (sets or {}):
        return set(sets[who])
    raise ValueError(f"qty：人の形の区分 {who!r} が order にも sets にも無い")


def _people(order, sets, past, steps, note, src):
    sl = slots(order)
    lab = [_kind(UNIT)]
    lab += [f'<path data-p="{i}" d="{person(cx, top, cw, ch)}" fill="{_c(DIM, DIM)}"/>'
            for i, (_, cx, top, cw, ch) in enumerate(sl)]
    lits = list(past) + [p for st in steps for p in F._many(st.get("add"))]
    for p in lits:
        if p["k"] != "lit":
            raise ValueError(f"qty：人の形に知らない部品 {p['k']!r}（lit）")
        if not p.get("rec"):
            raise ValueError(f"qty：rec（記録の頁）が無い部品 {p}")
        if _c(p["c"], "LINE") in (J.TICK, J.LINE_DIM, J.GRID, J.ALERT, J.ALERT_DIM):
            raise ValueError(f"qty：人の形に沈んだ色・赤 {p['c']} を使わない（亡くなった方の数に読める）")
    # 凡例の並び（子は親のすぐ下に字下げ）
    order_leg = []
    for p in lits:
        if p.get("parent") and p["parent"] in [q["who"] for q in order_leg]:
            j = max(i for i, q in enumerate(order_leg) if q["who"] == p["parent"] or q.get("parent") == p["parent"])
            order_leg.insert(j + 1, p)
        else:
            order_leg.append(p)
    ly = {id(p): LEG_Y0 + i * LEG_STEP for i, p in enumerate(order_leg)}

    def draw(p, dim):
        col = _c(DIM, DIM) if dim else _c(p["c"], "LINE")
        keep = _who(p["who"], order, sets)
        g = [f'<path data-p="{i}" d="{person(cx, top, cw, ch)}" fill="{col}"/>'
             for i, (nm, cx, top, cw, ch) in enumerate(sl) if nm in keep]
        x = LEG_X0 + (LEG_IND if p.get("parent") else 0)
        y = ly[id(p)]
        g.append(dq(F.rect(x, y - 27, 30, 30, col, rx=4), f"key|{p['who']}"))
        g.append(dq(F.txtfit(x + 44, y, p["who"], LEG_X1 - x - 44, cap=32, col=J.TICK if dim else J.INK_W),
                    f"klab|{p['who']}"))
        return "".join(g)

    for p in past:
        lab.append(draw(p, dim=not p.get("keep")))
    stages = ["".join(draw(p, False) for p in F._many(st.get("add"))) or " " for st in steps]
    lab.append(_foot(note, src))
    f = F.Fig("".join(lab), stages, "", (F.BX0, F.BX1))
    f.mech = dict(kind="qty", view="people", n=len(sl), lits=[dict(p) for p in lits])
    return f


def qty(view, steps, groups=(), past=(), n=0, title="", cols=0, order=(), sets=None, note="", src=""):
    """量の型。steps＝ナレーションの行ごとの段（上の「SPEC の書き方」）。"""
    if view not in VIEWS:
        raise ValueError(f"qty：知らない見え方 {view!r}（{VIEWS}）")
    if not src:
        raise ValueError("qty：src（出典）を書くこと（図解は出典必須）")
    if view == "bar":
        return _bar(groups, past, steps, note, src)
    if view == "grid":
        return _grid(n, title, steps, cols, note, src)
    return _people(order, sets, past, steps, note, src)
