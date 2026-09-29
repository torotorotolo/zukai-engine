# -*- coding: utf-8 -*-
"""lash.py — 固縛の型「帯と鎖の本数」（2026-09-29 新設・14本目 ⑤b-7b）。

■ 何か（Vault `Projects/事故検証-14本目-映像方針-追補-文字の画面-20260926.md` §4 の c510〜c513「固縛の模式図」）
  荷を船に縛りつける帯・鎖を、**記録と同じ本数だけ**描く図解（上から見た車・横から見た2段のコンテナ）。
  記録＝海審 p1042（3.1.4.3〜3.1.4.5）・p1093（4.4.1〜4.4.5）：
    乗用車＝0.5トン用の帯を前・後ろに2本ずつ（基準）→ 実際は前・後ろに1本ずつ／各タイヤに木の止め
    25トン車＝2.5トン用の帯を前・後ろ・左・右など10本（基準）→ 実際は約2.5トン用の鎖4本／各タイヤに木の止め
    仮ナンバーの乗用車10台ほど＝固縛の帯なし／船首の甲板の2段のコンテナ＝留め金（Twist lock・Bridge fitting）なし・
    隅の穴をロープでつないだ
  🔴 **人は描かない**。車の形・帯の位置・車軸の数・コンテナの列は**模式**（記録は本数と「前・後ろ／前後左右」だけ）
     ＝左下の注に「模式」と書く（§5b-10・書かないと型が止まる）
  🔴 仮ナンバーの車は**面**で描く（1台ずつ描かない＝「10台ほど」は数えられない＝§5b-74①・hull と同じ）

■ 見え方（view）。🔴 左上に見る向きの札（§5b-80）
  car   … 乗用車1台を上から（c510）
  both  … 乗用車（左）と25トン車（右）を上から（c511）
  loose … 固縛した乗用車（左）と、仮ナンバーの乗用車の面（右）を上から（c512）
  box   … 船首の甲板に2段に積んだコンテナを横から（隅の穴・留め金の場所・ロープ＝c513）

■ 状態（段の鍵・前の段から引き継ぐ）。🔴 **足すだけ**（消す・戻す段は型が止める＝絵は段の層に重ねるので消せない）
  車（car・truck）… off（無い）→ body（形だけ）→ req（基準の帯＝点線）→ all（木の止め・実際の帯と鎖＝実線）
  zone … off → on（仮ナンバーの乗用車の面）
  lock … off → on（留め金の場所＝点線の枠）　rope … off → on（隅の穴をつなぐロープ）

■ SPEC の書き方
  fig=("lash", dict(view="car", start=dict(car="body"),
                    steps=[dict(state=dict(car="req"), tag=dict(t="…", xy=(x, y), to=(x, y))), …],
                    rel=[dict(t="25トン", src="海審 p1093")], note="模式図：…", src=ss.src([…])))
  tag … xy＝札の左下の画素・to＝指す先の画素（線）・anchor＝start／middle／end。🔴 札に出す数は rel に宣言（門番 check_mech）

■ 門番 `check_mech`（judge_lash）＝**描いた SVG の印 `data-l` を数える**（本数・木の止めの数＝タイヤの数・面の帯0・留め金0）
  ＝記録（門番の側の `REC_LASH`）。描く側の表（下の CAR_REQ など）を壊すと門番が捕まえる（陽性対照）
"""
import re

import jiko_style as J
import titan_fig as F

VIEWS = {
    "car": dict(lab="上から見た図（乗用車）"),
    "both": dict(lab="上から見た図（左：乗用車　右：25トン車）"),
    "loose": dict(lab="上から見た図（乗用車）"),
    # ⚠️ ⑤b-7b：最初の札「横から見た図（船首の甲板に2段に積んだコンテナ）」は c513 の語りの複写＝門番 echo が止めた
    "box": dict(lab="横から見た図（上下2段のコンテナ）"),
}
LEVELS = ("off", "body", "req", "all")
FIELDS = {
    "car": dict(car=LEVELS),
    "both": dict(car=LEVELS, truck=LEVELS),
    "loose": dict(car=LEVELS, zone=("off", "on")),
    "box": dict(lock=("off", "on"), rope=("off", "on")),
}
START = {"car": dict(car="body"), "both": dict(car="body", truck="off"), "loose": dict(car="all", zone="off"),
         "box": dict(lock="off", rope="off")}

# ══════════════════════════════════════════════════════════
#  帯の表（🔴 描く側。門番は別に REC_LASH を持つ）
#  (端, 左右)：端＝front（前）／rear（後ろ）／side（横）・左右＝-1（左）／+1（右）・横は前後の位置の割合
# ══════════════════════════════════════════════════════════
CAR_REQ = (("front", -1), ("front", +1), ("rear", -1), ("rear", +1))        # 前・後ろに2本ずつ（海審 p1093 4.4.1）
CAR_ACT = (("front", -1), ("rear", +1))                                      # 前・後ろに1本ずつ（同）
TRUCK_REQ = (("front", -1), ("front", +1), ("rear", -1), ("rear", +1),      # 前・後ろ・左・右など10本（p1093 4.4.2）
             ("side", -1, 0.12), ("side", -1, -0.12), ("side", -1, -0.36),  # 🔴 横の3本ずつの配りは模式
             ("side", +1, 0.12), ("side", +1, -0.12), ("side", +1, -0.36))
TRUCK_ACT = (("front", -1), ("front", +1), ("rear", -1), ("rear", +1))      # 鎖4本（同）。🔴 位置は模式（四隅）
CAR_WHEELS = ((0.31, -1), (0.31, +1), (-0.31, -1), (-0.31, +1))
TRUCK_WHEELS = ((0.38, -1), (0.38, +1), (-0.16, -1), (-0.16, +1), (-0.33, -1), (-0.33, +1))   # 車軸3本は模式

REQ_COL, ACT_COL = "LINE_DIM", "AMBER"


def _c(nm):
    return nm if str(nm).startswith("#") else getattr(J, nm)


def _g(tag, svg):
    """門番の印 data-l を付けた束（画面には出ない）。"""
    return f'<g data-l="{F.esc(tag)}">{svg}</g>'


# ══════════════════════════════════════════════════════════
#  車（上から・前が右）
# ══════════════════════════════════════════════════════════
def _veh_geom(kind, cx, cy, sc):
    if kind == "car":
        L, W = 500 * sc, 200 * sc
        return dict(L=L, W=W, wheels=CAR_WHEELS, req=CAR_REQ, act=CAR_ACT, x_front=cx + 0.44 * L, x_rear=cx - 0.44 * L)
    L, W = 760 * sc, 240 * sc
    return dict(L=L, W=W, wheels=TRUCK_WHEELS, req=TRUCK_REQ, act=TRUCK_ACT, x_front=cx + 0.47 * L, x_rear=cx - 0.47 * L)


def _belt(kind, g, cx, cy, sc, spec):
    """帯1本の（車の側の点, 甲板の側の点）。"""
    L, W = g["L"], g["W"]
    end, side = spec[0], spec[1]
    if end == "front":
        a = (g["x_front"], cy + side * 0.32 * W)
        b = (a[0] + 120 * sc, a[1] + side * 105 * sc)
    elif end == "rear":
        a = (g["x_rear"], cy + side * 0.32 * W)
        b = (a[0] - 120 * sc, a[1] + side * 105 * sc)
    else:
        x = cx + spec[2] * L
        a = (x, cy + side * 0.5 * W)
        b = (x, a[1] + side * 120 * sc)
    return a, b


def _vehicle_body(kind, cx, cy, sc):
    g = _veh_geom(kind, cx, cy, sc)
    L, W = g["L"], g["W"]
    s = []
    for fx, side in g["wheels"]:
        wx, wy = cx + fx * L, cy + side * W / 2
        s.append(_g(f"{kind}|wheel", F.rect(wx - 40 * sc, wy - 15 * sc, 80 * sc, 30 * sc, _c("INK_W"), None, 0, rx=6)))
    if kind == "car":
        s.append(F.rect(cx - L / 2, cy - W / 2, L, W, _c("BG2"), _c("INK_W"), 4, rx=46 * sc))
        s.append(F.rect(cx - 0.24 * L, cy - 0.36 * W, 0.44 * L, 0.72 * W, "none", _c("LINE"), 3, rx=24 * sc))
        s.append(F.line(cx + 0.20 * L, cy - 0.36 * W, cx + 0.20 * L, cy + 0.36 * W, _c("LINE"), 3))
    else:
        xc = cx + 0.27 * L
        s.append(F.rect(cx - L / 2, cy - W / 2, 0.77 * L - 8 * sc, W, _c("BG2"), _c("INK_W"), 4, rx=8))
        s.append(F.rect(xc, cy - 0.46 * W, 0.23 * L, 0.92 * W, _c("BG2"), _c("INK_W"), 4, rx=18 * sc))
        for k in range(1, 5):
            x = cx - L / 2 + k * (0.77 * L) / 5
            s.append(F.line(x, cy - W / 2 + 10, x, cy + W / 2 - 10, _c("LINE_DIM"), 2))
    return "".join(s)


def _vehicle_layer(kind, cx, cy, sc, what):
    """what＝req（基準の帯＝点線）／all（木の止め・実際の帯と鎖＝実線）。"""
    g = _veh_geom(kind, cx, cy, sc)
    s = []
    if what == "req":
        for spec in g["req"]:
            (ax, ay), (bx, by) = _belt(kind, g, cx, cy, sc, spec)
            s.append(_g(f"{kind}|req|{spec[0]}",
                        F.line(ax, ay, bx, by, _c(REQ_COL), 5, dash="12 9") + F.circ(bx, by, 9 * sc, _c("BG"), _c("TICK"), 3)))
        return "".join(s)
    for fx, side in g["wheels"]:
        wx, wy = cx + fx * g["L"], cy + side * g["W"] / 2
        s.append(_g(f"{kind}|chock", F.rect(wx + 44 * sc, wy - 16 * sc, 18 * sc, 32 * sc, _c("LINE"), _c("INK_W"), 2)))
    for spec in g["act"]:
        (ax, ay), (bx, by) = _belt(kind, g, cx, cy, sc, spec)
        s.append(_g(f"{kind}|act|{spec[0]}",
                    F.line(ax, ay, bx, by, _c(ACT_COL), 8) + F.circ(bx, by, 10 * sc, _c(ACT_COL), _c("INK_W"), 2)))
    return "".join(s)


# 置き場（画素）。🔴 札の位置もここから決める（SPEC は xy で上書きできる）
PLACE = {
    "car": dict(car=(960.0, 548.0, 1.25)),
    "both": dict(car=(430.0, 548.0, 0.85), truck=(1300.0, 548.0, 0.95)),
    "loose": dict(car=(470.0, 548.0, 0.85)),
}
ZONE = (900.0, 360.0, 1700.0, 740.0)          # 仮ナンバーの乗用車の面（loose）


def _zone_svg():
    x0, y0, x1, y1 = ZONE
    s = [F.rect(x0, y0, x1 - x0, y1 - y0, _c("LINE"), _c("LINE"), 3, rx=24, op=0.18),
         F.rect(x0, y0, x1 - x0, y1 - y0, "none", _c("LINE"), 3, rx=24, dash="14 10")]
    # 種類の印（車の形を1つ・数ではない）
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s.append(F.rect(cx - 150, cy - 60, 300, 120, "none", _c("INK_W"), 3, rx=30, op=0.8))
    return _g("zone|area", "".join(s))


# ══════════════════════════════════════════════════════════
#  2段のコンテナ（横から）
# ══════════════════════════════════════════════════════════
BOX_S = 100.0                 # 画素／メートル
BOX_L, BOX_H = 3.0, 2.59      # 10フィート（約3メートル）・高さ 8.6フィート（海審 p1043 注17）
BOX_X0, DECK_Y = 810.0, 800.0


def _box_geom():
    w, h = BOX_L * BOX_S, BOX_H * BOX_S
    lo = (BOX_X0, DECK_Y - h, BOX_X0 + w, DECK_Y)
    up = (BOX_X0, DECK_Y - 2 * h, BOX_X0 + w, DECK_Y - h)
    return lo, up


def _casting(x, y):
    return (F.rect(x - 13, y - 13, 26, 26, _c("BG2"), _c("INK_W"), 3)
            + f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="7" ry="4" fill="{_c("BG")}"/>')


def _box_base():
    lo, up = _box_geom()
    s = [F.line(560, DECK_Y, 1360, DECK_Y, _c("INK_W"), 6),
         F.rect(560, DECK_Y, 800, 40, _c("BG2"), None, 0, op=0.6)]
    for (x0, y0, x1, y1) in (lo, up):
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, _c("BG2"), _c("INK_W"), 4))
        k = 1
        while x0 + k * 26 < x1 - 20:
            s.append(F.line(x0 + k * 26, y0 + 16, x0 + k * 26, y1 - 16, _c("LINE_DIM"), 2))
            k += 1
        for x in (x0 + 13, x1 - 13):
            for y in (y0 + 13, y1 - 13):
                s.append(_g("box|casting", _casting(x, y)))
    return "".join(s)


def _box_layer(what):
    lo, up = _box_geom()
    y = lo[1]
    s = []
    for x in (lo[0] + 13, lo[2] - 13):
        if what == "lock":
            # 留め金の場所＝点線の枠（使っていない＝中身を描かない）
            s.append(_g("box|lock|empty", F.rect(x - 22, y - 30, 44, 60, "none", _c(REQ_COL), 4, dash="8 6")))
        else:
            # 上の箱の下の隅の穴と、下の箱の上の隅の穴をロープの輪でつなぐ
            s.append(_g("box|rope", f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="16" ry="30" fill="none" '
                                    f'stroke="{_c(ACT_COL)}" stroke-width="6"/>'))
    return "".join(s)


# ══════════════════════════════════════════════════════════
#  状態と段
# ══════════════════════════════════════════════════════════
def _states(view, start, steps):
    fields = FIELDS[view]
    cur = dict(START[view], **(start or {}))
    out = []
    for st in [dict(state={})] + list(steps):
        nxt = dict(cur, **(st.get("state") or {}))
        for f_, v in nxt.items():
            if f_ not in fields:
                raise ValueError(f"lash：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"lash：{f_}={v!r} は知らない値（{fields[f_]}）")
            if out and fields[f_].index(v) < fields[f_].index(cur[f_]):
                raise ValueError(f"lash：{f_} が {cur[f_]} → {v} と戻る（段は足すだけ＝消せない）")
        cur = nxt
        out.append(dict(cur))
    return out[0], out[1:]


def _layers(view, before, after):
    """before → after で新しく出る絵（足すだけ）。"""
    s = []
    for who in ("car", "truck"):
        if who not in FIELDS[view]:
            continue
        cx, cy, sc = PLACE[view][who]
        a, b = LEVELS.index(before.get(who, "off")), LEVELS.index(after[who])
        for lv in LEVELS[a + 1:b + 1]:
            if lv == "body":
                s.append(_vehicle_body(who, cx, cy, sc))
            elif lv in ("req", "all"):
                s.append(_vehicle_layer(who, cx, cy, sc, lv))
    if view == "loose" and before.get("zone", "off") == "off" and after["zone"] == "on":
        s.append(_zone_svg())
    if view == "box":
        for f_ in ("lock", "rope"):
            if before.get(f_, "off") == "off" and after[f_] == "on":
                s.append(_box_layer(f_))
    return "".join(s)


def _tags(st):
    s, texts = [], []
    for tg in F._many(st.get("tag")):
        x, y = tg["xy"]
        if tg.get("to"):
            tx, ty = tg["to"]
            s.append(F.line(x, y + 8, tx, ty, _c("AMBER"), 2))
        s.append(F.txtfit(x, y, tg["t"], tg.get("w", 520), cap=tg.get("cap", 34), col=_c(tg.get("col", "AMBER")),
                          anchor=tg.get("anchor", "start")))
        texts.append(tg["t"])
    return "".join(s), texts


def lash(view, steps, start=None, rel=(), note="", src=""):
    """固縛の型。view＝VIEWS の名前。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"lash：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if "模式" not in note:
        raise ValueError("lash：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    if not src:
        raise ValueError("lash：src（出典）を書くこと")
    st0, states = _states(view, start, steps)
    lab = [F.txtfit(F.BX0 + 8, F.BY0 + 34, VIEWS[view]["lab"], 1100, cap=28, col=J.TICK)]
    if view == "box":
        lab.append(_box_base())
        lab.append(F.txtfit(575, DECK_Y + 30, "船首の甲板", 300, cap=24, col=J.TICK))
    lab.append(_layers(view, {k: "off" for k in st0}, st0))
    lab.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = [], []
    prev = st0
    for st, step in zip(states, steps):
        t_svg, t_txt = _tags(step)
        stages.append((_layers(view, prev, st) + t_svg) or " ")
        texts += t_txt
        prev = st
    f = F.Fig("".join(lab), stages, "", (F.BX0, F.BX1))
    f.moves = []
    f.mech = dict(kind="lash", view=view, start=st0, states=states, rel=list(rel), tags=texts,
                  steps=[dict(s) for s in steps])
    return f


def count(svg):
    """描いた印 data-l の数（門番が使う）。"""
    out = {}
    for m in re.finditer(r'data-l="([^"]+)"', svg):
        out[m.group(1)] = out.get(m.group(1), 0) + 1
    return out


