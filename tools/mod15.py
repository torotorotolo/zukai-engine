# -*- coding: utf-8 -*-
"""mod15.py — 15本目「改造の比べ」の動く模式図（2026-09-30 新設・15本目 ⑤b-4）。

■ 何か（Vault `Projects/事故検証-15本目-映像方針-絵コンテ-20260926.md` §4 の【改造】・§11-2 の使い回し）
  AAB 図2（PDF 14頁＝事故機の形に、ふつうの P-51D の寸法を赤で重ねた図）の延長。13本目の `latch`・14本目の `hull`・
  15本目の `tail`（`tools/tail15.py`）と同じ「基図＋段の鍵で動く部品」の図解（案C の絵ではない）。
  章の色の線と面・左上に見る向き・左下に「模式」と出典（§5b-10）。人は描かない（操縦席の覆いは光る面）。

■ 見え方（view）。🔴 見る向きの札を左上に必ず出す（§5b-80）
  plan    … 上から見た機体（機首が右＝図2 と同じ向き）。形＝図2 の画素から機械で測った輪郭（`ref/ep15/fig2_shapes.json`＝
             `ref/ep15/measure_fig2.py`）。**ふつうの P-51D にだけある部分**（翼の外側・水平尾翼の端）は緑の面（ふつう＝OK の色。
             図2 の赤はこのチャンネルでは「壊れ・欠陥」の色＝使わない）。c502・c508・c516・c522
  side    … 横から見た機体（機首が右）。ふつうの胴の下の空気の取り入れ口（図2 の赤＝緑の面）・操縦席の後ろの沸かして冷やす箱。c505
  weights … おもりの重さの比べ（高さ＝重さ・同じ尺）。昇降舵の釣り合いのおもり（ふつうの最大と事故機の左）・
             動きを安定させるおもり（ふつうと事故機＝推定）・機首の上げ下げが敏感に。c509・c510

■ 記録（AAB＝NTSB AAB-12/01。頁は PDF の頁）
  p13 翼の幅 28フィート10インチ（ふつうは 37フィート5/16インチ）＝2011年の改造 P-51D でいちばん短い・補助翼は約3フィートに（ふつう約7）
      水平尾翼 12フィート1インチ（ふつう 13フィート2 1/8インチ）・沸かして冷やす仕組み（放熱器を水とメタノールの液に沈める・
      箱は操縦席の後ろで操縦席と仕切った所・注11＝熱を吸って沸き、湯気で外へ）・ふつうの胴の下の取り入れ口の代わりに胴の形
  p14 図2・事故のあと残骸で分かった改造（昇降舵のおもり・方向舵の上のおもり・垂直尾翼と水平尾翼の取り付け角・方向舵）・
      左の昇降舵のおもり 26ポンド（資料のふつうの最大 13.75ポンド）・右は 27.5ポンド（昇降舵の一部と外側のちょうつがいが付いたまま）
  p18 動きを安定させるおもり（inertia weight＝bob weight）は残骸で見つからず・写真では端を切った形
  p42 短い翼と尾翼で縦横比が下がり、速く飛べて大きな力に耐えられた＝17.3G でも翼が空中で壊れなかった（Gが一瞬だったことも）
  p43 400ノット近くで揺れの出方が変わった（テレメトリー）・左の補助翼はいつも後ろの縁が少し下＝取り付けが正しくない・
      おもり約2倍（ふつうの P-51D の）と動きを安定させるおもり半分未満で、機首の上げ下げが敏感に
  #53 p10（PDF の頁 p4010）ふつうの P-51D の bob weight 20ポンド・事故機は推定 8⅔ポンドに切り詰め
  勧告書 A-12-09〜12 p3（p6103）注5「bob weight＝動きの安定を増すための装置」

■ SPEC の書き方（`tail` と同じ）
  fig=("mod", dict(view="plan"|"side"|"weights", start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…)), …],
                   rel=[dict(t="約11.3メートル", src="AAB p13")], note="模式…", src="…"))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。欄と値は FIELDS。札の数（メートル・キロ・倍…）は `rel=` に同じ文字列
■ 門番 `check_mech`（judge_mod）＝①状態の筋（記録）②本番の関数が置いた部品の画素 ③札の数（基図の文字も数える）
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import jiko_style as J
import titan_fig as F
import tail15 as T

HERE = Path(__file__).resolve().parent.parent
SHAPES = HERE / "ref" / "ep15" / "fig2_shapes.json"

FT, LB = 0.3048, 0.45359237
SPAN_STOCK = (37 + (5 / 16) / 12) * FT      # 11.286 メートル（AAB p13）
SPAN_MOD = (28 + 10 / 12) * FT              # 8.788
CW_STOCK, CW_ACC = 13.75 * LB, 26.0 * LB    # 6.237・11.793 キロ（AAB p14）
BW_STOCK, BW_ACC = 20.0 * LB, (8 + 2 / 3) * LB   # 9.072・3.931 キロ（#53 p10＝推定）

VIEWS = dict(plan=dict(lab="上から見た機体（模式・報告書の図2から）"), side=dict(lab="横から見た機体（模式）"),
             weights=dict(lab="おもりの重さ（高さ＝重さ・模式）"))
ONOFF = ("off", "on")
FIELDS = dict(
    plan=dict(stock=ONOFF, span=ONOFF, tailring=ONOFF, cw=ONOFF, wing=ONOFF, shake=ONOFF, ail=ONOFF),
    side=dict(scoop=("on", "dim"), boiler=ONOFF, boil=ONOFF, vent=ONOFF),
    weights=dict(cw=("off", "acc", "both"), cwx2=ONOFF, sens=ONOFF, bw=ONOFF),
)
START = dict(plan=dict(stock="off", span="off", tailring="off", cw="off", wing="off", shake="off", ail="off"),
             side=dict(scoop="on", boiler="off", boil="off", vent="off"),
             weights=dict(cw="off", cwx2="off", sens="off", bw="off"))


def _load():
    if not SHAPES.exists():
        raise FileNotFoundError(f"mod15：形の正本が無い {SHAPES}（ref/ep15/measure_fig2.py で作る＝fail closed）")
    return json.loads(SHAPES.read_text(encoding="utf-8"))


SH = _load()


# ── plan の置き場（画素）。1メートル＝K_P 画素・機首の先＝X_N・胴の真ん中の線＝Y_C ──
K_P, X_N, Y_C = 50.0, 830.0, 562.0


def P(x, y):
    """上から見た図のメートル（x 前が正・y 機体の左が正）→ 画素（機首が右・機体の左が画面の上）。"""
    return [X_N + x * K_P, Y_C - y * K_P]


def _red(side, part):
    """図2 の赤の面（ふつうの P-51D にだけある部分）を選ぶ。side＝+1（左＝上）／−1、part＝"wing"｜"stab"。"""
    for poly in SH["top"]["red"]:
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        wing = min(xs) > -6.5
        if (part == "wing") == wing and (sum(ys) / len(ys)) * side > 0:
            return poly
    raise ValueError(f"mod15：図2 の赤の面が見つからない（{side}・{part}）")


def _hcross(poly, y):
    """多角形（メートル）と横の線 y の交点の x（小さい順）。"""
    xs = []
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 - y) * (y2 - y) < 0:
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    return sorted(xs)


MOD = [P(*p) for p in SH["top"]["mod"]]
GLASS = [P(*p) for p in SH["top"]["glass"]]
RED = {(s, part): [P(*p) for p in _red(s, part)] for s in (1, -1) for part in ("wing", "stab")}
MOD_Y = (min(p[1] for p in MOD), max(p[1] for p in MOD))              # 事故機の翼端（画面の上・下）
STK_Y = (min(p[1] for p in RED[(1, "wing")]), max(p[1] for p in RED[(-1, "wing")]))   # ふつうの翼端
DX_S, DX_M = 1010.0, 945.0                 # 寸法の線の x（ふつう・事故機）


def _tip_x(pts, y, band=8.0):
    """翼端のいちばん前（画面の右）の x＝寸法を伸ばす線の始まり（翼から離さない）。"""
    return max(p[0] for p in pts if abs(p[1] - y) <= band) + 6.0


TIP_X = dict(dim_s=(_tip_x(RED[(1, "wing")], STK_Y[0], 14.0), _tip_x(RED[(-1, "wing")], STK_Y[1], 14.0)),
             dim_m=(_tip_x(MOD, MOD_Y[0], 14.0), _tip_x(MOD, MOD_Y[1], 14.0)))


def _centroid(pts):
    return [sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)]
# 補助翼（p13＝約3フィートに短くした）：翼端の近くの後ろの縁（横の範囲は案C の B と同じ＝`illu.RB_AIL` 3.30〜4.20メートル）
AIL_Y = (3.30, 4.20)
AIL_C = 0.36                               # 補助翼の幅（メートル・模式）
# 昇降舵のおもり（p14＝外側のちょうつがいの近く）：外側の端・ちょうつがいの線の前（模式）
CW_AT = (-8.45, 1.62)
TAIL_C = P(-8.62, 0.0)


def _ail(side):
    ys = [AIL_Y[0] * side, AIL_Y[1] * side]
    te = [min(_hcross(SH["top"]["mod"], y)) for y in ys]
    return [P(te[0], ys[0]), P(te[1], ys[1]), P(te[1] + AIL_C, ys[1]), P(te[0] + AIL_C, ys[0])]


def _wing_edge(side):
    """事故機の翼の外まわり（胴の外・x −5.4〜−2.2 メートル）＝輪郭の点の続き。"""
    pts = SH["top"]["mod"]
    sel = [i for i, (x, y) in enumerate(pts) if y * side > 0.62 and -5.4 < x < -2.2]
    if not sel:
        raise ValueError("mod15：翼の輪郭が取れない")
    # 輪郭の番号は輪になっている＝いちばん長い続き（間の飛びが1の並び）を採る
    runs, cur = [], [sel[0]]
    for a, b in zip(sel, sel[1:]):
        if b == a + 1:
            cur.append(b)
        else:
            runs.append(cur)
            cur = [b]
    runs.append(cur)
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][-1] == len(pts) - 1:
        runs[0] = runs[-1] + runs[0]
        runs.pop()
    run = max(runs, key=len)
    return [P(*pts[i]) for i in run]


def _zig(x0, y0, x1, y1, n=6, amp=12.0):
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    out = []
    for i in range(n * 2 + 1):
        t = i / (n * 2)
        s = amp * (1 if i % 2 else -1) if 0 < i < n * 2 else 0.0
        out.append([x0 + (x1 - x0) * t - uy * s, y0 + (y1 - y0) * t + ux * s])
    return out


# 補助翼の断面（c522 の小窓）：機首が右・翼の断面の後ろ（左）に補助翼・ちょうつがいのまわりに回す。角度は模式（p43「少し」）
INS = (1150.0, 560.0, 650.0, 290.0)                     # 小窓の x, y, 幅, 高さ
INS_WING = [(1720.0, 700.0), (1700.0, 676.0), (1640.0, 664.0), (1520.0, 666.0), (1420.0, 676.0), (1420.0, 724.0),
            (1520.0, 730.0), (1640.0, 728.0), (1700.0, 718.0)]
INS_H = (1420.0, 700.0)                                 # 補助翼のちょうつがい
INS_AIL = [(1414.0, 678.0), (1300.0, 694.0), (1250.0, 700.0), (1300.0, 704.0), (1414.0, 722.0)]
AIL_DEG = -9.0                                          # 画面で時計回りが正＝左へ伸びる補助翼は負で後ろの縁が下がる（模式）
#   ⚠️ 下見：-6度（後ろの縁が約18画素下）は小窓の大きさで読めなかった＝-9度（約27画素・p43「少し」のうち）と下向きの矢印


# ── side の置き場。1メートル＝K_S 画素 ──
K_S, X_NS, Y_CS = 150.0, 1760.0, 548.0


def Q(x, y):
    return [X_NS + x * K_S, Y_CS - y * K_S]


SIDE_MOD = [Q(*p) for p in SH["side"]["mod"]]


def _scoop():
    """図2 の横の図の赤の面のうち、胴の下の取り入れ口（いちばん大きい・胴の下）。"""
    cand = [p for p in SH["side"]["red"] if max(q[1] for q in p) < -0.3]
    if not cand:
        raise ValueError("mod15：胴の下の取り入れ口（赤）が見つからない")
    return [Q(*p) for p in max(cand, key=len)]


SCOOP = _scoop()


def _side_glass():
    """横から見た操縦席の覆い＝事故機の輪郭の上の出っ張り（x −4.95〜−3.35・y 0.5 より上）を下の線で閉じる。"""
    pts = [p for p in SH["side"]["mod"] if -4.95 <= p[0] <= -3.35 and p[1] > 0.5]
    pts.sort(key=lambda p: p[0])
    return [Q(*p) for p in pts] + [Q(-3.35, 0.5), Q(-4.95, 0.5)]


SIDE_GLASS = _side_glass()
BOX = (-5.75, -0.40, -4.85, 0.30)                     # 沸かして冷やす箱（メートル・操縦席の後ろ＝模式）
LIQ_TOP = 0.12                                          # 液の面
WALL_X = -4.85                                          # 操縦席との仕切り


def _box_pts():
    x0, y0, x1, y1 = BOX
    return [Q(x0, y0), Q(x1, y0), Q(x1, y1), Q(x0, y1)]


def _liq_pts():
    x0, y0, x1, _ = BOX
    return [Q(x0 + 0.03, y0 + 0.03), Q(x1 - 0.03, y0 + 0.03), Q(x1 - 0.03, LIQ_TOP), Q(x0 + 0.03, LIQ_TOP)]


def _rad_pts():
    """放熱器（液の中に沈めた四角と縦の板）＝1本の折れ線。"""
    x0, y0, x1, _ = BOX
    a, b = Q(x0 + 0.15, y0 + 0.08), Q(x1 - 0.15, LIQ_TOP - 0.08)
    out = [[a[0], a[1]], [b[0], a[1]], [b[0], b[1]], [a[0], b[1]], [a[0], a[1]]]
    n = 6
    for i in range(1, n):
        x = a[0] + (b[0] - a[0]) * i / n
        out += [[x, a[1]], [x, b[1]], [x, a[1]]]
    return out


VENT = [Q(-5.30, 0.14), Q(-5.34, 0.42), Q(-5.26, 0.66), Q(-5.40, 0.92), Q(-5.46, 1.22)]   # 湯気の道（外へ・模式）


# ── weights の置き場。高さ＝重さ（1キロ＝K_W 画素・同じ尺）──
K_W, W_BASE, W_W = 30.5, 776.0, 200.0       # 台の線 y776＝下の名前（y826）が出典の行（y886）に近づきすぎない
W_X = dict(cw_stock=250.0, cw_acc=560.0, bw_stock=1180.0, bw_acc=1490.0)
W_KG = dict(cw_stock=CW_STOCK, cw_acc=CW_ACC, bw_stock=BW_STOCK, bw_acc=BW_ACC)


def _block(key):
    x, h = W_X[key], W_KG[key] * K_W
    return [[x, W_BASE], [x + W_W, W_BASE], [x + W_W, W_BASE - h], [x, W_BASE - h]]


def _sens_icon():
    """機首の上げ下げの印：横から見た事故機（小さく）の輪郭。"""
    k, cx, cy = 26.0, 1435.0, 360.0
    return [[cx + (x + 4.75) * k, cy - y * k] for x, y in SH["side"]["mod"]]


def _P(ident, typ, pts=None, **kw):
    return T._P(ident, typ, pts, **kw)


def _on(v):
    return 1.0 if v else 0.0


def parts_of(view, st):
    """状態 → 部品（id・形・色・濃さ）。🔴 門番（check_mech.judge_mod）もこの関数を呼ぶ＝描く側と同じ幾何。"""
    if view == "plan":
        out = [
            _P("mod", "poly", MOD, fill="BG2", stroke="INK_W", w=3),
            _P("glass", "poly", GLASS, fill="LINE", stroke="INK_W", w=1.5, alpha=0.75),
        ]
        for (s, part), pts in RED.items():
            nm = f"stk_{part}_{'l' if s > 0 else 'r'}"
            out.append(_P(nm, "poly", pts, fill="OK", stroke="OK", w=1, alpha=0.32 * _on(st["stock"] == "on")))
            out.append(_P(nm + "_ln", "line", pts + [pts[0]], stroke="OK", w=3, alpha=_on(st["stock"] == "on")))
        # 寸法の線（上の翼端 → 下の翼端）と翼端から伸ばす線
        sp = st["span"] == "on"
        for nm, x, (y0, y1), col in (("dim_s", DX_S, STK_Y, "OK"), ("dim_m", DX_M, MOD_Y, "AMBER")):
            mid = (y0 + y1) / 2
            ta, tb = TIP_X[nm]
            out += [_P(nm + "_a", "line", [[x, mid], [x, y0]], stroke=col, w=4, head=16, alpha=_on(sp)),
                    _P(nm + "_b", "line", [[x, mid], [x, y1]], stroke=col, w=4, head=16, alpha=_on(sp)),
                    _P(nm + "_ea", "line", [[ta, y0], [x + 14, y0]], stroke=col, w=2, alpha=0.8 * _on(sp)),
                    _P(nm + "_eb", "line", [[tb, y1], [x + 14, y1]], stroke=col, w=2, alpha=0.8 * _on(sp))]
        out.append(_P("tailring", "poly", T._ellipse(TAIL_C, 62.0, 128.0), fill=None, stroke="AMBER", w=4,
                      alpha=_on(st["tailring"] == "on")))
        for s in (1, -1):
            c = P(CW_AT[0], CW_AT[1] * s)
            out.append(_P(f"cw_{'l' if s > 0 else 'r'}", "poly", [[c[0] - 7, c[1] - 7], [c[0] + 7, c[1] - 7], [c[0] + 7, c[1] + 7],
                                                                  [c[0] - 7, c[1] + 7]], fill="AMBER", stroke="AMBER", w=1,
                          alpha=_on(st["cw"] == "on")))
            out.append(_P(f"cwring_{'l' if s > 0 else 'r'}", "poly", T._ring(c, 22.0), fill=None, stroke="AMBER", w=4,
                          alpha=_on(st["cw"] == "on")))
            out.append(_P(f"wing_{'l' if s > 0 else 'r'}", "line", _wing_edge(s), stroke="AMBER", w=6, alpha=_on(st["wing"] == "on")))
            out.append(_P(f"ail_{'l' if s > 0 else 'r'}", "poly", _ail(s), fill="AMBER", stroke="AMBER", w=1,
                          alpha=0.85 * _on(st["ail"] == "on")))
        # 揺れの印（翼端の外・尾の後ろ・機首の前）
        zz = [_zig(700, STK_Y[0] - 8, 760, STK_Y[0] - 8, 4, 9), _zig(700, STK_Y[1] + 8, 760, STK_Y[1] + 8, 4, 9),
              _zig(330, 470, 330, 654, 5, 10), _zig(860, 520, 860, 604, 3, 10)]
        for j, pts in enumerate(zz):
            out.append(_P(f"shake{j}", "line", pts, stroke="AMBER", w=4, alpha=_on(st["shake"] == "on")))
        # 補助翼の断面の小窓
        a = _on(st["ail"] == "on")
        x, y, w, h = INS
        # ⚠️ 下見：小窓を塗りつぶすと、段の層の見出し「補助翼の断面」を覆った（動く部品は段の層より上に描く）＝枠の線だけ
        te = T._rot(INS_AIL[2], INS_H, AIL_DEG)
        out += [
            _P("ins_box", "poly", [[x, y], [x + w, y], [x + w, y + h], [x, y + h]], fill=None, stroke="LINE_DIM", w=2, alpha=a),
            _P("ins_wing", "poly", INS_WING, fill="BG2", stroke="INK_W", w=3, alpha=a),
            _P("ins_ref", "line", [[1414.0, 700.0], [1236.0, 700.0]], stroke="TICK", w=2, alpha=0.9 * a),
            _P("ins_ail", "poly", [T._rot(p, INS_H, AIL_DEG) for p in INS_AIL], fill="AMBER", stroke="INK_W", w=2, alpha=a),
            _P("ins_down", "line", [[te[0] - 26.0, te[1] - 40.0], [te[0] - 26.0, te[1] + 6.0]], stroke="AMBER", w=4, head=12, alpha=a),
        ]
        return out
    if view == "side":
        dim = st["scoop"] == "dim"
        x0, y0, x1, y1 = BOX
        return [
            _P("mod", "poly", SIDE_MOD, fill="BG2", stroke="INK_W", w=3),
            _P("glass", "poly", SIDE_GLASS, fill="LINE", stroke="INK_W", w=1.5, alpha=0.75),
            _P("scoop", "poly", SCOOP, fill="OK", stroke="OK", w=1, alpha=0.12 if dim else 0.34),
            _P("scoop_ln", "line", SCOOP + [SCOOP[0]], stroke="OK", w=3, alpha=0.45 if dim else 1.0),
            _P("box", "poly", _box_pts(), fill="BG", stroke="INK_W", w=3, alpha=_on(st["boiler"] == "on")),
            _P("liq", "poly", _liq_pts(), fill="LINE", stroke="LINE", w=1, alpha=0.55 * _on(st["boiler"] == "on")),
            _P("rad", "line", _rad_pts(), stroke="INK_W", w=2, alpha=_on(st["boiler"] == "on")),
            _P("wall", "line", [Q(WALL_X, -0.52), Q(WALL_X, 0.50)], stroke="AMBER", w=4, alpha=_on(st["boiler"] == "on")),
        ] + [
            _P(f"bub{j}", "poly", T._ring(Q(x0 + 0.2 + 0.13 * j, LIQ_TOP - 0.05 - 0.04 * (j % 2)), 6.0, 12), fill="INK_W",
               stroke="INK_W", w=1, alpha=0.8 * _on(st["boil"] == "on")) for j in range(5)
        ] + [
            _P("vent", "line", VENT, stroke="TICK", w=5, head=18, alpha=_on(st["vent"] == "on")),
            _P("vent2", "line", [[p[0] + 30.0, p[1] + 6.0] for p in VENT[:-1]], stroke="TICK", w=3, alpha=0.7 * _on(st["vent"] == "on")),
        ]
    # weights
    cw, a_bw = st["cw"], _on(st["bw"] == "on")
    stock_y = W_BASE - CW_STOCK * K_W
    out = [
        # 台の線（⚠️ 下見：基図に描くと、使っていない右半分にも線だけ出た＝おもりを出すときに一緒に出す）
        _P("base_cw", "line", [[160.0, W_BASE], [860.0, W_BASE]], stroke="LINE_DIM", w=3, alpha=_on(cw != "off")),
        _P("base_bw", "line", [[1080.0, W_BASE], [1790.0, W_BASE]], stroke="LINE_DIM", w=3, alpha=a_bw),
        _P("cw_stock", "poly", _block("cw_stock"), fill="OK", stroke="OK", w=3, alpha=0.8 * _on(cw == "both")),
        _P("cw_acc", "poly", _block("cw_acc"), fill="AMBER", stroke="AMBER", w=3, alpha=0.85 * _on(cw in ("acc", "both"))),
        _P("cw_line", "line", [[W_X["cw_acc"] - 16, stock_y], [W_X["cw_acc"] + W_W + 16, stock_y]], stroke="INK_W", w=3,
           alpha=_on(st["cwx2"] == "on")),
        _P("bw_stock", "poly", _block("bw_stock"), fill="OK", stroke="OK", w=3, alpha=0.8 * a_bw),
        _P("bw_acc", "poly", _block("bw_acc"), fill="AMBER", stroke="AMBER", w=3, alpha=0.85 * a_bw),
        _P("sens", "poly", _sens_icon(), fill="BG2", stroke="INK_W", w=2, alpha=_on(st["sens"] == "on")),
        # 機首の上げ下げ：機体の真ん中のまわりの弧（上へ・下へ）
        _P("sens_up", "line", F._arc(SENS_C[0], SENS_C[1], 170.0, 352.0, 322.0, 12), stroke="ALERT", w=5, head=16,
           alpha=_on(st["sens"] == "on")),
        _P("sens_dn", "line", F._arc(SENS_C[0], SENS_C[1], 170.0, 8.0, 38.0, 12), stroke="ALERT", w=5, head=16,
           alpha=_on(st["sens"] == "on")),
    ]
    return out


SENS_C = (1435.0, 352.0)                   # 機首の上げ下げの印の真ん中（小さな事故機の重心のあたり）


def anchors(view, st):
    """札の指し先（段の終わりの状態で）。"""
    if view == "plan":
        return dict(stock=_centroid(RED[(1, "wing")]), tail=(TAIL_C[0], TAIL_C[1] - 128.0), cw=P(CW_AT[0], CW_AT[1]),
                    cw_r=P(CW_AT[0], -CW_AT[1]),
                    ail=_centroid(_ail(1)), wing=(640.0, 330.0), ins=(1330.0, 712.0), tip=(TIP_X["dim_m"][0], MOD_Y[0]))
    if view == "side":
        x0, _, x1, y1 = BOX
        return dict(box=Q((x0 + x1) / 2, y1), scoop=Q(-5.2, -0.9), vent=VENT[-1], rad=Q((x0 + x1) / 2, -0.1))
    return dict(cw_acc=(W_X["cw_acc"] + W_W / 2, W_BASE - CW_ACC * K_W), cw_stock=(W_X["cw_stock"] + W_W / 2, W_BASE - CW_STOCK * K_W),
                bw_acc=(W_X["bw_acc"] + W_W / 2, W_BASE - BW_ACC * K_W), sens=(1435.0, 330.0))


# 札の置き場（x, y, 揃え, 幅）。🔴 段の札は残る（§5b-89）＝1つのカットで同じ置き場に2段の札を置かない
TAG_AT = dict(
    plan=dict(r1=(1060.0, 300.0, "start", 760.0), r2=(1060.0, 360.0, "start", 760.0), r3=(1060.0, 430.0, "start", 760.0),
              r4=(1060.0, 490.0, "start", 760.0), b1=(1060.0, 780.0, "start", 760.0), b2=(1060.0, 832.0, "start", 760.0),
              ins=(1170.0, 600.0, "start", 610.0), lt=(100.0, 300.0, "start", 420.0), lb=(100.0, 830.0, "start", 520.0)),
    side=dict(top=(700.0, 300.0, "start", 760.0), t2=(700.0, 350.0, "start", 760.0), low=(100.0, 800.0, "start", 900.0),
              low2=(1000.0, 800.0, "start", 820.0), bot=(1000.0, 850.0, "start", 820.0)),
    weights=dict(cwl=(160.0, 300.0, "start", 760.0), cw1=(350.0, 826.0, "middle", 300.0), cw2=(660.0, 826.0, "middle", 300.0),
                 cwn1=(350.0, 568.0, "middle", 300.0), cwn2=(660.0, 398.0, "middle", 300.0), x2=(790.0, 600.0, "start", 280.0),
                 bwl=(1080.0, 470.0, "start", 760.0), bw1=(1280.0, 826.0, "middle", 300.0), bw2=(1590.0, 826.0, "middle", 300.0),
                 half=(1590.0, 638.0, "middle", 300.0), sens=(1080.0, 300.0, "start", 420.0)),
)


def _base(view, start):
    g = []
    if view == "plan":
        # 機首の向き（機首の上・翼より前・寸法の線より左＝形にも寸法の線にも重ねない）
        g.append(F.txtfit(752.0, 500.0, "機首", 120, cap=24, col=J.TICK))
        g.append(F.arrow(752.0, 516.0, 814.0, 516.0, J.TICK, 4, 14))
    elif view == "side":
        g.append(F.arrow(X_NS - 150.0, Y_CS + 200.0, X_NS - 60.0, Y_CS + 200.0, J.TICK, 4, 16))
        g.append(F.txtfit(X_NS - 160.0, Y_CS + 209.0, "機首", 120, cap=24, col=J.TICK, anchor="end"))
    return g


def build(kind, view, fields, start0, parts_fn, base_fn, anchors_fn, tag_at, lab, steps, start, rel, note, src, base_tags=()):
    """状態の段 → 部品の鍵 → Fig（`tail15.tail` と同じ作り）。15本目 ⑤b-4 の `mod`・`bolt` が使う。"""
    if "模式" not in note:
        raise ValueError(f"{kind}：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    cur = dict(start0, **(start or {}))
    seq = []
    for st in [dict(state={})] + list(steps):
        cur = dict(cur, **(st.get("state") or {}))
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"{kind}：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"{kind}：{f_}={v!r} は知らない値（{fields[f_]}）")
        seq.append(dict(cur))
    start_st, states = seq[0], seq[1:]
    per = [parts_fn(view, s) for s in seq]
    shapes, anim = [], []
    for j, p0 in enumerate(per[0]):
        keys = []
        for i, ps in enumerate(per):
            pj = ps[j]
            kk = {f_: pj[f_] for f_ in T.KEY_FIELDS if f_ in pj}
            kk.setdefault("alpha", 1.0)
            keys.append(dict(stage=max(0, i - 1), delay=(0.0 if i == 0 else (1.0 if i == 1 else F.MECH_DELAY)), **kk))
        sh = {f_: p0[f_] for f_ in p0 if f_ not in ("alpha",)}
        sh["keys"] = keys
        moving = any({f_: kk.get(f_) for f_ in T.KEY_FIELDS} != {f_: keys[0].get(f_) for f_ in T.KEY_FIELDS} for kk in keys[1:])
        sh["anim"] = bool(moving)
        shapes.append(sh)
        if moving:
            anim.append(sh)
    g = base_fn(view, start_st)
    g.append("".join(T._svg_of(sh, sh["keys"][0]) for sh in shapes if not sh["anim"]))
    texts = []
    for tg in base_tags:                                # 頭から出ている札（前のカットの続き）
        x, y, anchor, mw = tag_at[view][tg["at"]]
        g.append(F.txtfit(x, y, tg["t"], mw, cap=tg.get("cap", 34), col=tg.get("col", J.AMBER), anchor=anchor))
        texts.append(tg["t"])
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, lab, 1000, cap=28, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages = []
    for st, stt in zip(steps, states):
        s = []
        an = anchors_fn(view, stt)
        for tg in F._many(st.get("tag")):
            at = tg.get("at", next(iter(tag_at[view])))          # 書いていなければ、その見え方の最初の置き場
            x, y, anchor, mw = tag_at[view][at] if isinstance(at, str) else (tuple(at) if len(at) == 4 else (at[0], at[1], "start", 420))
            c = tg.get("cap", 34)
            if tg.get("to"):
                tx, ty = an[tg["to"]] if isinstance(tg["to"], str) else tg["to"]
                sy = y - round(c * 0.9) if ty < y - c else y + 8
                s.append(F.line(x if anchor != "end" else x, sy, tx, ty, J.AMBER, 2))
            s.append(F.txtfit(x, y, tg["t"], mw, cap=c, col=tg.get("col", J.AMBER), anchor=anchor))
            texts.append(tg["t"])
            if tg.get("d"):
                s.append(F.txtfit(x, y + round(c * 0.95), tg["d"], mw, cap=round(c * 0.62), col=J.TICK, anchor=anchor))
                texts.append(tg["d"])
        if st.get("svg"):
            s.append(st["svg"])
        stages.append("".join(s) or " ")
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind=kind, view=view, start=start_st, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(st) for st in steps])
    return f


def mod(view, steps, start=None, rel=(), note="", src="", base_tags=()):
    """改造の比べの模式図。view＝"plan"｜"side"｜"weights"。steps＝ナレーションの行ごとの段（上の「SPEC の書き方」）。
    base_tags＝頭から出しておく札（前のカットの続きで、段の札と同じ置き場の名）。"""
    if view not in VIEWS:
        raise ValueError(f"mod：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    return build("mod", view, FIELDS[view], START[view], parts_of, _base, anchors, TAG_AT, VIEWS[view]["lab"], steps, start,
                 rel, note, src, base_tags)
