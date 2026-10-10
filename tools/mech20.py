# -*- coding: utf-8 -*-
"""mech20.py — 20本目（日本航空123便のリメイク）「模式図」（2026-10-10 新設・⑤b-5）。

■ 何か
  18本目の `mech18`・19本目の `mech19` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。
  案C の再現イラスト（illu20 の置き場 S1〜S7）ではない＝「再現」の札は出さない。左上に見る向き・左下に「模式」と出典。人は描かない。
  横から見た機体は置き場 S1 の形（`illu20.S1_UP`・`S1_LO`・`S1_FIN`…＝付図-4 の横の図）を縮めて使う＝絵のカットと模式図のカットで形が食い違わない。
  上から見た機体は付図-4 の上の図（全長 231 FT 4 IN・全幅 195 FT 8 IN・後退角 37.5度・エンジンの横の位置 内側 12.07m／外側 21.15m・
  水平尾翼の幅 72 FT 9 IN）と付図-8（動翼・フラップの名称＝補助翼・フラップ・昇降舵・方向舵の並び）から（形は模式）。

■ 見え方（view）＝台本 第2版 §4 の画の欄
  seats  … 上から見た操縦室（前が上）＝付図-12（P1 機長席・P3 副操縦士席・P4 機関士の計器＝右の壁）          c206・c207
  xpdr   … 管制のレーダーと機体＝4桁の番号を送り返す（番号は書かない・「緊急」の札＝p6）                        c215
  hyd    … 上から見た機体（機首が上）と油圧の管4本（エンジン駆動ポンプ No.1〜No.4＝p51・4系統＝p112）           c307・c308・c622
  thrust … 横から（推力と機首の上げ下げ＝p117 の推定）と上から（左右の推力の差と揺れ＝p114）                c317・c318・c412
  alt    … 高さの線＝**記録の点だけ**（cruise＝付図-1 の時刻と高度／final＝p82 の 18:55:57・18:56:17 と付図-1 の 18:56:03）
           高度はフィートをメートルに直して描く（0.3048）                                                c320・c418・c419
  gear   … 横から見た機体の車輪とフラップ（電気の代わりの仕組み＝p113・p117）                                c321
  radio  … 無線の相手（東京コントロール＝p6・「羽田」＝別添6 p333）                                        c403
  fix    … 夜の測位（無線の目印からの方角と距離＝解説 p18）と読み取りの幅（飛行機 5度・1マイル／ヘリ 1度・0.1マイル）
           向きと長さは表3 の①（横田TACAN から 305°・35マイル）の例                                         c506・c507
  hoist  … 夜の山の斜面とヘリコプター（人は描かない・照明の無い斜面＝解説 p20・p21）                          c509
  press  … 横から見た尾部の断面（後部圧力隔壁 BS2360＝p29・客室の与圧が後ろへ押す＝p125）                     c607
  bag    … 尾翼の中の気圧と、海の近くと山の上の袋（解説 p17）                                                c620
  🆕 ⑤b-6（2026-10-10）＝第6〜8章（隔壁の継ぎ目・亀裂・点検）：
  fatigue… 穴のあいた板・くり返し引く力・穴の縁から横へ伸びるひび（3つに分けて順に）・針金のたとえ                  c705
  rows   … L18 の断面（付図-38(a)(b) を簡単に＝2列・1列）と強さの棒（本来＝1・約0.7＝p102・p124）            c711
  grow   … 亀裂の伸び方（1列は2列の2倍強＝p65・線は直線の模式）と、同じ長さに届くまで                        c712
  fs     … 隔壁を後ろから見た円（S6 の正面と同じ表）：1ベイの中の亀裂（p110）・1列の所＝左の第1〜第3ストラップ（別添1 p248） c714
  half   … 横から見た尾部の断面：隔壁の上半分（元のまま）と下半分（取り替え＝別添1 p246）・継ぎ目                 c805
  edge   … 板の縁とリベットの穴：余白・縁に近すぎる穴・手引きの決まり（長さは模式）                              c807
  seal   … 継ぎ目の断面（実際の継ぎ方＝S6_LAYERS）と縁を覆うシール材（p103・付図-38）・後ろの側の目              c816
  rear   … 隔壁を後ろから見た円：後面全体の目視検査・L18 は特別に指定されていない（p104）                        c902・c903
  clen   … リベットの頭と亀裂：長さ（約10ミリ）と見える長さ（約8ミリ）の比（p100）                              c904
  prob   … 見つける確率（1つ 10%程度・少なくとも1つ 14〜60%程度＝p100）＝幅は破線の枠                            c905・c906
  two    … 正しい作りと修理の壁／事故機の壁（p105（コ））                                                       c908
  lav    … 横から見た客室の後ろ：いちばん後ろの化粧室・コートルーム・1978年の変形の可能性（p103）              c913

■ SPEC の書き方（mech19 と同じ）
  fig=("m20", dict(view=…, start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…, d=…)), …],
                   rel=[dict(t="4系統", src="報告書 p112")], note="…模式…", src=ss.src([…])))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。札の数・時刻は `rel=` に同じ文字列（門番 check_mech の judge_m20）。
  🔴 記録の値（エンジンの位置・高さの点・扇の角度と幅・隔壁の位置ほか）は門番 check_mech の REC_M20 が別に持つ（§5b-88）。
  ⚠️ 動く部品は段の層（札）より上に描かれる＝札は動く部品の通り道に置かない
"""
from __future__ import annotations

import math

import jiko_style as J
import titan_fig as F
import illu as IL
import illu20 as I2

ONOFF = ("off", "on")
FT = 0.3048
C20 = I2.C20
# ── 意味の色（章の色に置き換わらない直書き）──
COL = dict(body=C20["body"], body_ln=C20["body_ln"], wing=C20["wing"], eng=C20["eng"], eng_dk=C20["eng_dk"], fin=C20["fin"],
           stab=C20["stab"], hyd=C20["hyd"], hyd_dim="#5d5470", red=C20["crack"], mark="#f2c14e", press=C20["press"],
           cabin=C20["cabin"], dark="#10161b", seat="#7d8a95", seat_ln="#2a333a", panel="#3b4a56", win=C20["win"],
           radar="#8fd3e8", night0="#0b1220", night1="#16243a", slope="#26332d", slope_ln="#4c5d52", tree="#1b2621",
           light="#fff3c4", sea="#2d5a7a", sea_ln="#8fc3e0", mount="#6f7d72", mount_ln="#a9b8ad", bag="#e9d9a6",
           bag_ln="#6b5a2c", white="#eef2f4", ghost="#5a656c", green="#5fbf8f", blue="#7fb8e6", dotc="#f6d77a")
INK = "#e3eaee"
L_X, R_X = F.BX0 + 40.0, 1270.0          # 札の左の列・右の列の x（図の左右の空き）


def _P(ident, typ, pts=None, **kw):
    d = dict(id=ident, type=typ)
    if pts is not None:
        d["pts"] = [list(map(float, p)) for p in pts]
    d.update(kw)
    return d


def _on(prev, st, f, v="on"):
    """この段で f が v になった（前の段は v でない）。"""
    return st.get(f) == v and prev.get(f) != v


def _t(x, y, t, size=24, col=INK, anchor="start"):
    return F.txt(x, y, t, size, col, anchor=anchor)


def _ring(x, y, r, col, w=5.0):
    return F.circ(x, y, r, "none", COL["dark"], w + 4) + F.circ(x, y, r, "none", col, w)


def _dot(x, y, r, col):
    return F.circ(x, y, r, col, COL["dark"], 2.5)


def _arc_pts(cx, cy, r, a0, a1, n=28):
    """方位の円弧（度・北＝0・時計回り＝画面の座標）"""
    return [(cx + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)),
             cy - r * math.cos(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def _rot(p, c, deg):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


# ══════════════════════════════════════════════════════════
#  横から見た機体（置き場 S1 の形を縮める＝機首が左・x＝機首からのメートル・z＝上）
# ══════════════════════════════════════════════════════════
def side_pts(K, X0, Y0, pts):
    return [(X0 + x * K, Y0 - z * K) for x, z in pts]


def side_body(K, X0, Y0, cut_front=None):
    up = IL._smooth(I2.S1_UP, per=6)
    lo = IL._smooth(I2.S1_LO, per=6)
    if cut_front is not None:
        def clip(pts):
            out = []
            for a, b in zip(pts, pts[1:]):
                if a[0] < cut_front <= b[0]:
                    out.append((cut_front, a[1] + (b[1] - a[1]) * (cut_front - a[0]) / (b[0] - a[0])))
            return out + [p for p in pts if p[0] >= cut_front]
        up, lo = clip(up), clip(lo)
    return side_pts(K, X0, Y0, up + list(reversed(lo)))


def side_engine(K, X0, Y0, e):
    x0, x1, zc, r = e
    return side_pts(K, X0, Y0, [(x0, zc + r), (x1 - 1.2, zc + r * 0.95), (x1, zc + r * 0.45), (x1, zc - r * 0.45),
                                (x1 - 1.2, zc - r * 0.95), (x0, zc - r)])


def side_plane_parts(K, X0, Y0, pre, pivot, rot, alpha=1.0, fin=True):
    """横から見た機体を動く部品に（機首の上げ下げ＝pivot のまわりに rot 度）。"""
    kw = dict(pivot=list(pivot), rot=rot, alpha=alpha)
    out = [_P(pre + "body", "poly", side_body(K, X0, Y0), fill=COL["body"], stroke=COL["body_ln"], w=2.5, **kw),
           _P(pre + "wing", "poly", side_pts(K, X0, Y0, I2.S1_WING), fill=COL["wing"], stroke=COL["body_ln"], w=2, **kw)]
    for i, e in enumerate(I2.S1_ENG):
        out.append(_P(pre + f"eng{i}", "poly", side_engine(K, X0, Y0, e), fill=COL["eng"], stroke=COL["body_ln"], w=2, **kw))
    if fin:
        out += [_P(pre + "stab", "poly", side_pts(K, X0, Y0, I2.S1_STAB), fill=COL["stab"], stroke=COL["body_ln"], w=2, **kw),
                _P(pre + "fin", "poly", side_pts(K, X0, Y0, I2.S1_FIN), fill=COL["fin"], stroke=COL["body_ln"], w=2.5, **kw)]
    return out


# ══════════════════════════════════════════════════════════
#  上から見た機体（機首が上・x＝機首からのメートル・y＝右の翼が正）＝付図-4 の上の図・付図-8 の動翼
# ══════════════════════════════════════════════════════════
TOP_LEN = I2.S1_LEN
TOP_HALF = [(0.0, 0.0), (0.8, 1.3), (2.5, 2.4), (5.0, 3.0), (8.0, 3.25), (50.0, 3.25), (56.0, 2.9), (61.0, 2.3), (65.0, 1.6),
            (68.5, 0.9), (TOP_LEN, 0.35)]                                       # 胴体の半分の幅（全幅 21 FT 4 IN＝6.5m）
TOP_WING = [(20.0, 3.25), (44.3, 29.8), (46.9, 29.8), (36.0, 12.1), (34.0, 3.25)]   # 右の翼（前縁の根元・前縁の先・後縁の先・折れ・後縁の根元）
TOP_ENG_Y = (12.07, 21.15)                     # 付図-4「有効エンジン・モーメントアーム」Y_EI・Y_EO（内側・外側）
TOP_ENG_X = ((21.4, 29.6), (31.9, 39.4))       # 前後の位置＝置き場 S1 の横の図と同じ（付図-4）
TOP_ENG_W = 1.35
TOP_STAB = [(58.0, 2.0), (65.6, 11.1), (68.4, 11.1), (68.6, 2.0)]                  # 水平尾翼（幅 72 FT 9 IN＝22.2m）
TOP_FIN = [(58.8, 0.0), (64.0, 0.5), (71.2, 0.15), (71.2, -0.15), (64.0, -0.5)]    # 垂直尾翼（上から見ると細い）
# 動翼（付図-8 の並び：内側フラップ・内側補助翼・外側フラップ・外側補助翼／内側昇降舵・外側昇降舵／方向舵）＝幅と奥行きは模式
TOP_SURF = dict(flap_in=(3.6, 11.6, 3.2), ail_in=(12.3, 14.4, 2.2), flap_out=(14.6, 22.4, 2.6), ail_out=(23.0, 28.6, 1.8))
TOP_ELEV = dict(elev_in=(2.2, 6.6, 2.0), elev_out=(6.6, 10.8, 1.6))
TOP_RUD = (66.2, 71.2, 0.35)
ENG_NO = {1: -TOP_ENG_Y[1], 2: -TOP_ENG_Y[0], 3: TOP_ENG_Y[0], 4: TOP_ENG_Y[1]}   # エンジンの番号 → 横の位置（左が負）＝No.1 は左の外側
CG_X = (104 + 2 / 12) * FT                      # 付図-4「104 FT 2 IN」＝機首から 0.25 MAC まで（回す中心＝模式）


def te_x(y):
    """後縁の x（右の翼・y＝横の位置）"""
    (x0, y0), (xk, yk), (xt, yt) = (TOP_WING[4][0], TOP_WING[4][1]), (TOP_WING[3][0], TOP_WING[3][1]), (TOP_WING[2][0], TOP_WING[2][1])
    y = abs(y)
    if y <= yk:
        return x0 + (y - y0) * (xk - x0) / (yk - y0)
    return xk + (y - yk) * (xt - xk) / (yt - yk)


class Top:
    """上から見た機体の座標（機首が上）"""
    def __init__(self, K, CX, Y0):
        self.K, self.CX, self.Y0 = K, CX, Y0

    def p(self, x, y):
        return (self.CX + y * self.K, self.Y0 + x * self.K)

    def ps(self, pts, mirror=False):
        return [self.p(x, -y if mirror else y) for x, y in pts]

    def body(self):
        r = [self.p(x, w) for x, w in TOP_HALF]
        l_ = [self.p(x, -w) for x, w in reversed(TOP_HALF)]
        return r + l_

    def engine(self, no):
        y = ENG_NO[no]
        x0, x1 = TOP_ENG_X[0] if abs(y) < 15 else TOP_ENG_X[1]
        w = TOP_ENG_W
        return self.ps([(x0, y - w), (x1, y - w * 0.8), (x1, y + w * 0.8), (x0, y + w)])

    def surf(self, ya, yb, c, mirror=False, te=None):
        f = te or te_x
        return self.ps([(f(ya) - c, ya), (f(yb) - c, yb), (f(yb), yb), (f(ya), ya)], mirror)


def _elev_te(y):
    (xa, ya), (xb, yb) = (TOP_STAB[3][0], TOP_STAB[3][1]), (TOP_STAB[2][0], TOP_STAB[2][1])
    return xa + (abs(y) - ya) * (xb - xa) / (yb - ya)


def top_plane_svg(T, wing_col=None, eng_col=None):
    g = [F.poly(T.ps(TOP_WING), wing_col or COL["wing"], COL["body_ln"], 2.5, True),
         F.poly(T.ps(TOP_WING, True), wing_col or COL["wing"], COL["body_ln"], 2.5, True),
         F.poly(T.ps(TOP_STAB), COL["stab"], COL["body_ln"], 2, True), F.poly(T.ps(TOP_STAB, True), COL["stab"], COL["body_ln"], 2, True),
         F.poly(T.body(), COL["body"], COL["body_ln"], 2.5, True), F.poly(T.ps(TOP_FIN), COL["fin"], COL["body_ln"], 2, True)]
    for no in (1, 2, 3, 4):
        g.append(F.poly(T.engine(no), eng_col or COL["eng"], COL["body_ln"], 2, True))
    return g


def top_surfaces(T):
    """動翼の多角形（名前 → 画素の点）"""
    out = {}
    for nm, (ya, yb, c) in TOP_SURF.items():
        out[nm + "_r"] = T.surf(ya, yb, c)
        out[nm + "_l"] = T.surf(ya, yb, c, True)
    for nm, (ya, yb, c) in TOP_ELEV.items():
        out[nm + "_r"] = T.surf(ya, yb, c, te=_elev_te)
        out[nm + "_l"] = T.surf(ya, yb, c, True, te=_elev_te)
    x0, x1, w = TOP_RUD
    out["rud"] = T.ps([(x0, -w), (x1, -w), (x1, w), (x0, w)])
    return out


# ══════════════════════════════════════════════════════════
#  seats（c206・c207）＝上から見た操縦室（前が上）＝付図-12
# ══════════════════════════════════════════════════════════
SE_OUT = [(700, 830), (700, 450), (745, 370), (840, 312), (960, 292), (1080, 312), (1175, 370), (1220, 450), (1220, 830)]
SE_SEAT = dict(left=(840.0, 505.0), right=(1080.0, 505.0))                  # 左の席・右の席の真ん中
SE_FE = (1085.0, 705.0)                                                     # 航空機関士の席（右の席の後ろ・右の壁を向く）
SE_P4 = (1168.0, 590.0, 40.0, 225.0)                                       # 機関士の計器（右の壁＝付図-12 の P4）
SE_NAMES = dict(left=dict(usual="機長", cop="副操縦士"), right=dict(cap="機長"))


def _seat(cx, cy, ln, fill=None, back="down"):
    g = [F.rect(cx - 55, cy - 60, 110, 120, fill or COL["seat"], ln, 3, rx=16)]
    if back == "down":
        g.append(F.rect(cx - 55, cy + 42, 110, 20, COL["seat_ln"], ln, 2, rx=6))
    else:
        g.append(F.rect(cx - 55, cy - 60, 20, 120, COL["seat_ln"], ln, 2, rx=6))
    return "".join(g)


def seats_base(st0):
    g = [F.poly(SE_OUT, "#1c2a35", COL["body_ln"], 3, True),
         F.poly([(760, 372), (860, 330), (960, 318), (1060, 330), (1160, 372)], "none", COL["win"], 9),
         F.rect(760, 384, 400, 36, COL["panel"], COL["body_ln"], 2, rx=6),
         F.rect(928, 440, 64, 170, COL["panel"], COL["body_ln"], 2, rx=8),
         F.rect(*SE_P4, COL["panel"], COL["body_ln"], 2, rx=6),
         _seat(*SE_SEAT["left"], COL["seat_ln"]), _seat(*SE_SEAT["right"], COL["seat_ln"]),
         _seat(*SE_FE, COL["seat_ln"], back="left"),
         _t(960, 276, "前", 24, J.TICK, "middle"), F.arrow(990, 282, 990, 254, J.TICK, 3, 10)]
    return g


def seats_stage(prev, st):
    g = []
    if _on(prev, st, "fe"):
        x, y = SE_FE
        g.append(F.rect(x - 75, 575, SE_P4[0] + SE_P4[2] + 12 - (x - 75), 250, "none", COL["mark"], 5, rx=14))
    for side in ("left", "right"):
        v = st.get(side)
        if v != "off" and v != prev.get(side):
            cx, cy = SE_SEAT[side]
            col = COL["mark"] if (side, v) in (("right", "cap"), ("left", "usual")) else COL["blue"]
            g.append(F.rect(cx - 62, cy - 67, 124, 134, "none", col, 5, rx=18, dash=("10 8" if v == "usual" else None)))
            g.append(F.txtfit(cx, cy + 12, SE_NAMES[side][v], 104, cap=28, col=INK, anchor="middle"))
    if _on(prev, st, "ask"):
        # ⚠️ 門番 layout：席の真ん中に置くと、次の段の席の名（副操縦士・機長）と重なった（層は残る）＝席の上へ
        for side in ("left", "right"):
            cx, cy = SE_SEAT[side]
            g.append(F.txt(cx, cy - 78, "？", 46, COL["mark"], anchor="middle"))
    if _on(prev, st, "cert"):
        cx, cy = SE_SEAT["right"]
        g.append(F.circ(cx + 60, cy - 70, 22, COL["mark"], COL["dark"], 3) + F.txt(cx + 60, cy - 61, "認", 24, COL["dark"], anchor="middle"))
    return g


# ══════════════════════════════════════════════════════════
#  xpdr（c215）＝管制のレーダーと機体
# ══════════════════════════════════════════════════════════
XP = dict(gy=800.0, rx=330.0, dish=(330.0, 628.0), pk=4.6, px0=1260.0, py0=380.0)
XP_FROM, XP_TO = (1290.0, 405.0), (420.0, 640.0)        # 返す矢印（機体 → レーダー）
XP_DIGITS = 4                                           # 4桁（7700＝p6）＝番号は書かない・枠だけ


def xp_code_boxes():
    (x0, y0), (x1, y1) = XP_FROM, XP_TO
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return [(mx + (i - (XP_DIGITS - 1) / 2) * 40 - 15, my - 15 - 40, 30, 30) for i in range(XP_DIGITS)]


def xpdr_base(st0):
    K, X0, Y0 = XP["pk"], XP["px0"], XP["py0"]
    g = [F.line(F.BX0 + 20, XP["gy"], F.BX1 - 20, XP["gy"], COL["mount_ln"], 3),
         F.rect(260, 700, 140, 100, COL["panel"], COL["body_ln"], 2, rx=6),
         F.line(330, 700, 330, 650, COL["eng"], 6),
         F.poly([(282, 600), (300, 640), (330, 652), (360, 640), (378, 600)], "none", COL["eng"], 6),
         F.poly(side_body(K, X0, Y0), COL["body"], COL["body_ln"], 2, True),
         F.poly(side_pts(K, X0, Y0, I2.S1_WING), COL["wing"], COL["body_ln"], 1.5, True),
         F.poly(side_pts(K, X0, Y0, I2.S1_FIN), COL["fin"], COL["body_ln"], 1.5, True),
         _t(330, 845, "管制のレーダー", 26, J.TICK, "middle")]
    return g


def xpdr_stage(prev, st):
    g = []
    if _on(prev, st, "ask"):
        cx, cy = XP["dish"]
        ang = math.degrees(math.atan2(XP_FROM[0] - cx, -(XP_FROM[1] - cy)))
        for r in (70, 110, 150):
            g.append(F.poly(_arc_pts(cx, cy, r, ang - 18, ang + 18), "none", COL["radar"], 5))
    if st.get("reply") != prev.get("reply") and st.get("reply") in ("on", "emg"):
        col = COL["red"] if st["reply"] == "emg" else COL["mark"]
        g.append(F.arrow(*XP_FROM, *XP_TO, col, 6, 24))
        for x, y, w, h in xp_code_boxes():
            g.append(F.rect(x, y, w, h, COL["dark"], col, 4, rx=4))
    return g


# ══════════════════════════════════════════════════════════
#  hyd（c307・c308・c622）＝上から見た機体と油圧の管4本
# ══════════════════════════════════════════════════════════
HY = Top(8.2, 960.0, 268.0)
HY_OFF = {1: -1.6, 2: -0.55, 3: 0.55, 4: 1.6}            # 胴体の中の4本の並び（模式）
HY_TAIL = 66.5                                          # 尾翼の根元（ここまで伸びる＝模式）
HY_CUT = 63.0                                           # 切れる所（垂直尾翼の中＝p113「垂直尾翼の損壊に伴う…配管の切断」・位置は模式）


def hyd_path(no):
    """系統 no の管（メートル）：ポンプ（エンジン）→ 胴体へ → 後ろへ → 尾翼の根元。返り値＝(本線, 翼の舵への枝)"""
    y = ENG_NO[no]
    x1 = (TOP_ENG_X[0] if abs(y) < 15 else TOP_ENG_X[1])[1] - 1.0
    o = HY_OFF[no]
    main = [(x1, y), (x1, o), (61.0, o), (HY_TAIL, o * 0.4)]
    branch = [(x1, y), (te_x(y) - 0.4, y)]
    return main, branch


def _split_at(pts, xc):
    """折れ線を x＝xc で前と後ろに分ける"""
    a, b = [pts[0]], []
    for p, q in zip(pts, pts[1:]):
        if not b and p[0] < xc <= q[0]:
            u = (xc - p[0]) / (q[0] - p[0])
            m = (xc, p[1] + (q[1] - p[1]) * u)
            a.append(m)
            b = [m, q]
        elif b:
            b.append(q)
        else:
            a.append(q)
    return a, b


def hyd_parts(st):
    out = []
    on = st["pipes"] == "on"
    for no in (1, 2, 3, 4):
        main, br = hyd_path(no)
        fr, af = _split_at(main, HY_CUT)
        cut = st["cut"] == "on"
        out.append(_P(f"p{no}a", "line", HY.ps(fr), stroke=COL["hyd"], w=5, alpha=1.0 if on else 0.0))
        out.append(_P(f"p{no}b", "line", HY.ps(af), stroke=COL["hyd_dim"] if cut else COL["hyd"], w=5,
                      alpha=(1.0 if on else 0.0), dx=0.0))
        out.append(_P(f"p{no}w", "line", HY.ps(br), stroke=COL["hyd"], w=4, alpha=1.0 if on else 0.0))
    return out


def hyd_base(st0):
    g = top_plane_svg(HY)
    for nm, pts in top_surfaces(HY).items():
        g.append(F.poly(pts, "#8d98a2", COL["body_ln"], 1.5, True))
    g.append(_t(HY.p(-1.5, 0)[0], HY.p(-1.5, 0)[1] - 4, "機首", 22, J.TICK, "middle"))
    return g


def hyd_stage(prev, st):
    g = []
    if _on(prev, st, "surf"):
        for nm, pts in top_surfaces(HY).items():
            g.append(F.poly(pts, COL["mark"], COL["dark"], 2, True, op=0.92))
    if _on(prev, st, "num"):
        for no in (1, 2, 3, 4):
            y = ENG_NO[no]
            x0 = (TOP_ENG_X[0] if abs(y) < 15 else TOP_ENG_X[1])[0]
            px, py = HY.p(x0 - 2.6, y)
            g.append(F.circ(px, py - 8, 17, COL["dark"], COL["hyd"], 3) + F.txt(px, py + 1, str(no), 24, COL["hyd"], anchor="middle"))
    if _on(prev, st, "ask"):
        x, y = HY.p(64.0, 0.0)
        g.append(_ring(x, y, 62, COL["mark"]))
    if _on(prev, st, "cut"):
        # ⚠️ 試し焼き ep20_b5：管ごとの小さな切れ目は胴体の幅（約53画素）の中で見えなかった＝4本をまとめて横切るぎざぎざと、
        #    両側へこぼれる油の点（大きく）。位置は HY_CUT（門番が測る切れる所）
        cx, cy = HY.p(HY_CUT, 0.0)
        zz = [(cx - 44 + 11 * k, cy + (-9 if k % 2 else 9)) for k in range(9)]
        g.append(F.poly(zz, "none", COL["dark"], 11) + F.poly(zz, "none", COL["red"], 6))
        for s in (-1, 1):
            for j in range(3):
                g.append(F.circ(cx + s * (54 + j * 14), cy + 14 + j * 16, 8 - j * 1.5, COL["hyd"], COL["dark"], 1.5))
    return g


# ══════════════════════════════════════════════════════════
#  thrust（c317・c318・c412）＝横から（推力と機首）・上から（左右の差と揺れ）
# ══════════════════════════════════════════════════════════
TH_SIDE = dict(both=(9.0, 150.0, 585.0), side=(13.0, 460.0, 600.0))          # 横の図（K・機首の x・真ん中の y）
TH_TOP = Top(6.0, 1400.0, 320.0)                # ⚠️ 下見の計算：6.2・330 だと尾の先（y 767）が下の札（y 766〜）に触れた
TH_PITCH = 7.0                                  # 機首を上げる角度（度・模式）
TH_YAW = 7.0                                    # 向きが変わる角度（度・模式）
TH_LEN = dict(base=5.0, up=10.0)                # 推力の矢印の長さ（m・模式）
TH_DIFF = dict(strong=9.0, weak=2.0)            # 左右の差（左が強い・m・模式）
TH_WAVE = (1720.0, 720.0, 360.0)                # 揺れの波（x・下の端の y・上の端の y＝機の右に縦に＝進む向きが上）


def th_side_geo(st):
    K, X0, Y0 = TH_SIDE[st["lay"]]
    return K, X0, Y0, (X0 + CG_X * K, Y0)


def th_top_arrow(no, L):
    y = ENG_NO[no]
    x0 = (TOP_ENG_X[0] if abs(y) < 15 else TOP_ENG_X[1])[0]
    return TH_TOP.ps([(x0 - 0.3, y), (x0 - 0.3 - L, y)])


def th_top_len(st, no):
    if st["diff"] == "off":
        return TH_LEN["base"]
    return TH_DIFF["strong"] if ENG_NO[no] < 0 else TH_DIFF["weak"]


def thrust_parts(st):
    K, X0, Y0, piv = th_side_geo(st)
    rot = TH_PITCH if st["nose"] == "up" else 0.0           # 画面の座標で正＝pivot より左（機首）が上がる（titan_fig.mech_pts）
    out = side_plane_parts(K, X0, Y0, "s_", piv, rot)
    L = TH_LEN["up"] if st["pwr"] == "up" else TH_LEN["base"]
    for i, (x0, x1, zc, r) in enumerate(I2.S1_ENG):
        out.append(_P(f"s_thr{i}", "line", side_pts(K, X0, Y0, [(x0 - 0.4, zc), (x0 - 0.4 - L, zc)]), stroke=COL["mark"], w=6,
                      head=18, pivot=list(piv), rot=rot))
    if st["lay"] == "both":
        a = 1.0 if st["top"] == "on" else 0.0
        T = TH_TOP
        piv2 = list(T.p(CG_X, 0.0))
        yaw = TH_YAW if st["yaw"] == "on" else 0.0
        kw = dict(pivot=piv2, rot=yaw, alpha=a)
        out += [_P("t_wingr", "poly", T.ps(TOP_WING), fill=COL["wing"], stroke=COL["body_ln"], w=2, **kw),
                _P("t_wingl", "poly", T.ps(TOP_WING, True), fill=COL["wing"], stroke=COL["body_ln"], w=2, **kw),
                _P("t_stabr", "poly", T.ps(TOP_STAB), fill=COL["stab"], stroke=COL["body_ln"], w=2, **kw),
                _P("t_stabl", "poly", T.ps(TOP_STAB, True), fill=COL["stab"], stroke=COL["body_ln"], w=2, **kw),
                _P("t_body", "poly", T.body(), fill=COL["body"], stroke=COL["body_ln"], w=2, **kw)]
        for no in (1, 2, 3, 4):
            out.append(_P(f"t_eng{no}", "poly", T.engine(no), fill=COL["eng"], stroke=COL["body_ln"], w=2, **kw))
            out.append(_P(f"t_thr{no}", "line", th_top_arrow(no, th_top_len(st, no)), stroke=COL["mark"], w=6, head=16, **kw))
    return out


def thrust_base(st0):
    g = []
    if st0["lay"] == "both":
        g += [F.line(960, F.BY0 + 60, 960, F.BY1 - 60, COL["ghost"], 2, "6 10"),
              _t(F.BX0 + 8, F.BY0 + 74, "横から（機首が左）", 24, J.TICK), _t(990, F.BY0 + 74, "上から（機首が上）", 24, J.TICK)]
    return g


def thrust_stage(prev, st):
    g = []
    K, X0, Y0, piv = th_side_geo(st)
    if _on(prev, st, "nose", "up"):
        nx, ny = X0 + 2.0 * K, Y0 - 1.0 * K
        pts = _arc_pts(nx + 120, ny + 40, 150, 250, 300)
        g.append(F.poly(pts, "none", COL["mark"], 5))
        a, b = pts[-2], pts[-1]
        g.append(F.arrow(a[0], a[1], b[0], b[1], COL["mark"], 5, 18))
    if st["lay"] == "both" and _on(prev, st, "diff", "ask") or (st["lay"] == "both" and st["diff"] == "ask" and _on(prev, st, "top")):
        x, y = TH_TOP.p(-3.5, 0)
        g.append(F.txt(x, y, "？", 44, COL["mark"], anchor="middle"))
    if _on(prev, st, "yaw"):
        x, y = TH_TOP.p(4.0, 0)
        pts = _arc_pts(x, y + 360, 360, -12, 14)
        g.append(F.poly(pts, "none", COL["red"], 5))
        g.append(F.arrow(pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], COL["red"], 5, 18))
    if _on(prev, st, "wave"):
        g.append(F.poly(th_wave_pts(), "none", COL["red"], 4))
    return g


def th_wave_pts(n=90):
    """揺れの波（下から上へ進むほど振れ幅が大きくなる＝ダッチロールが強まる・模式）"""
    x, ya, yb = TH_WAVE
    return [(x + (6 + 34 * i / n) * math.sin(i / n * 4.5 * 2 * math.pi), ya + (yb - ya) * i / n) for i in range(n + 1)]


# ══════════════════════════════════════════════════════════
#  alt（c320・c418・c419）＝高さの線（記録の点だけ）
# ══════════════════════════════════════════════════════════
AL = dict(x0=360.0, x1=1640.0, y0=300.0, y1=790.0)
AL_SPAN = dict(cruise=dict(t0="18:23:00", t1="18:49:00", ymax=8000.0, xt=("18:25", "18:30", "18:35", "18:40", "18:45"),
                           yt=(0, 2000, 4000, 6000, 8000)),
               final=dict(t0="18:55:50", t1="18:56:25", ymax=4000.0, xt=("18:55:50", "18:56:00", "18:56:10", "18:56:20"),
                          yt=(0, 1000, 2000, 3000, 4000)))
# 記録の点（時刻・フィート）＝cruise は付図-1 の時刻と高度の札（`ref/ep20/route20.json` の ticks）／final は p82 と付図-1
AL_PTS = dict(cruise=[("18:24:12", 23400), ("18:24:35", 23900), ("18:25:18", 23900), ("18:27:07", 24400), ("18:28:36", 22100),
                      ("18:31:08", 24900), ("18:34:53", 21400), ("18:38:06", 22400), ("18:40:30", 22400), ("18:41:59", 20900),
                      ("18:43:05", 18600), ("18:44:09", 17000), ("18:45:48", 13500), ("18:47:17", 9000), ("18:48:03", 6800)],
              final=[("18:55:57", 10000), ("18:56:03", 8400), ("18:56:17", 5500)])
AL_EARLY = dict(cruise="18:40:30", final="18:56:03")      # pts=early で描く最後の点
AL_MARK = dict(cruise=dict(m1="18:25:21", m2="18:40:00"), final=dict(m1="18:56:07", m2="18:56:17"))
AL_RATE = 15000.0                                         # 平均の降下率（フィート/分＝p82）
AL_RATE_FROM = "18:55:57"


def _sec(hms):
    p = [int(v) for v in hms.split(":")] + [0, 0]
    return p[0] * 3600 + p[1] * 60 + p[2]


def al_xy(span, hms, m):
    sp = AL_SPAN[span]
    t0, t1 = _sec(sp["t0"]), _sec(sp["t1"])
    x = AL["x0"] + (AL["x1"] - AL["x0"]) * (_sec(hms) - t0) / (t1 - t0)
    y = AL["y1"] - (AL["y1"] - AL["y0"]) * m / sp["ymax"]
    return x, y


def al_points(span, mode):
    if mode == "off":
        return []
    last = _sec(AL_EARLY[span]) if mode == "early" else 10 ** 9
    return [(t, ft) for t, ft in AL_PTS[span] if _sec(t) <= last]


def al_rate_line(span):
    t0 = AL_RATE_FROM
    ft0 = dict(AL_PTS[span])[t0]
    t1 = AL_MARK["final"]["m2"]
    ft1 = ft0 - AL_RATE * (_sec(t1) - _sec(t0)) / 60.0
    return [(t0, ft0), (t1, ft1)]


def alt_base(st0):
    span = st0["span"]
    sp = AL_SPAN[span]
    g = [F.line(AL["x0"], AL["y1"], AL["x1"], AL["y1"], COL["mount_ln"], 3), F.line(AL["x0"], AL["y0"] - 10, AL["x0"], AL["y1"], COL["mount_ln"], 3)]
    for v in sp["yt"]:
        x, y = al_xy(span, sp["t0"], v)
        g.append(F.line(AL["x0"], y, AL["x1"], y, COL["ghost"], 1.5, "4 8"))
        g.append(_t(AL["x0"] - 14, y + 9, f"{v:,}", 24, J.TICK, "end"))
    for h in sp["xt"]:
        x, _ = al_xy(span, h if h.count(":") == 2 else h + ":00", 0)
        g.append(F.line(x, AL["y1"], x, AL["y1"] + 10, COL["mount_ln"], 2))
        g.append(_t(x, AL["y1"] + 40, h, 24, J.TICK, "middle"))
    g.append(_t(AL["x0"] - 14, AL["y0"] - 30, "高度（メートル）", 24, J.TICK, "start"))
    return g


def alt_stage(prev, st):
    g = []
    span = st["span"]
    if st["pts"] != prev.get("pts"):
        had = {t for t, _ in al_points(span, prev.get("pts", "off"))}
        for t, ft in al_points(span, st["pts"]):
            if t not in had:
                x, y = al_xy(span, t, ft * FT)
                g.append(_dot(x, y, 8, COL["dotc"]))
    for m in ("m1", "m2"):
        if _on(prev, st, m):
            x, _ = al_xy(span, AL_MARK[span][m], 0)
            g.append(F.line(x, AL["y0"] - 4, x, AL["y1"], COL["red"] if (span, m) in (("final", "m2"),) else COL["mark"], 3, "10 8"))
    if _on(prev, st, "rate"):
        (ta, fa), (tb, fb) = al_rate_line(span)
        a, b = al_xy(span, ta, fa * FT), al_xy(span, tb, fb * FT)
        g.append(F.line(*a, *b, COL["red"], 4, "14 10"))
    if _on(prev, st, "stop"):
        t, ft = AL_PTS[span][-1]
        x, y = al_xy(span, t, ft * FT)
        g.append(F.arrow(x + 14, y, x + 120, y, COL["green"], 6, 20))
    return g


# ══════════════════════════════════════════════════════════
#  gear（c321）＝横から見た機体の車輪とフラップ
# ══════════════════════════════════════════════════════════
GE = (13.5, 420.0, 470.0)                        # K・機首の x・真ん中の y
GE_NOSE_X, GE_MAIN_X = 7.1, (31.9, 33.4)         # 付図-4 の横の図（前の脚・主脚＝前の脚から 83 FT 11.5 IN）
GE_LEG = 3.0                                     # 下ろした脚の長さ（m・模式）
GE_FLAP = [(33.0, -2.65), (36.0, -2.35), (37.6, -2.55), (34.6, -2.95)]
GE_FLAP_PIVOT = (34.5, -2.5)
GE_FLAP_DEG = 25.0                               # 下げた角度（模式）
GE_FLAP_LAG = 1.8                                # フラップは脚のあと（18:38〜脚・18:44〜フラップ＝p117）＝段の中で遅れて動く


GE_WHEEL = 0.8                                   # 車輪の半径（m・模式）＝⚠️ 試し焼き ep20_b5：0.55 では小さくて見えにくかった


def _leg(x, K, X0, Y0):
    zb = -3.35
    return side_pts(K, X0, Y0, [(x - 0.3, zb + 0.3), (x + 0.3, zb + 0.3), (x + 0.3, zb - GE_LEG), (x - 0.3, zb - GE_LEG)])


def gear_parts(st):
    K, X0, Y0 = GE
    down = st["gear"] == "down"
    dy = 0.0 if down else -GE_LEG * K * 0.7
    a = 1.0 if down else 0.0
    out = []
    for i, x in enumerate((GE_NOSE_X,) + GE_MAIN_X):
        out.append(_P(f"leg{i}", "poly", _leg(x, K, X0, Y0), fill=COL["eng_dk"], stroke=COL["dark"], w=1.5, dy=dy, alpha=a))
        cx, cy = side_pts(K, X0, Y0, [(x, -3.35 - GE_LEG)])[0]
        out.append(_P(f"whl{i}", "circle", c=[cx, cy], r=GE_WHEEL * K, fill="#2b3239", stroke=COL["mark"] if down else COL["dark"], w=4,
                      dy=dy, alpha=a))
    piv = side_pts(K, X0, Y0, [GE_FLAP_PIVOT])[0]
    out.append(_P("flap", "poly", side_pts(K, X0, Y0, GE_FLAP), fill=COL["mark"] if st["flap"] == "down" else COL["wing"],
                  stroke=COL["body_ln"], w=2, pivot=list(piv), rot=(GE_FLAP_DEG if st["flap"] == "down" else 0.0), lag=GE_FLAP_LAG))
    return out


def gear_base(st0):
    K, X0, Y0 = GE
    g = [F.poly(side_pts(K, X0, Y0, I2.S1_STAB), COL["stab"], COL["body_ln"], 2, True),
         F.poly(side_pts(K, X0, Y0, I2.S1_FIN), COL["fin"], COL["body_ln"], 2.5, True),
         F.poly(side_body(K, X0, Y0), COL["body"], COL["body_ln"], 2.5, True),
         F.poly(side_pts(K, X0, Y0, I2.S1_WING), COL["wing"], COL["body_ln"], 2, True)]
    for e in I2.S1_ENG:
        g.append(F.poly(side_engine(K, X0, Y0, e), COL["eng"], COL["body_ln"], 2, True))
    return g


def gear_stage(prev, st):
    g = []
    if _on(prev, st, "voice"):
        x, y = side_pts(*GE, [(5.0, 3.6)])[0]
        g.append(_ring(x, y, 46, COL["mark"]))
    return g


# ══════════════════════════════════════════════════════════
#  radio（c403）＝無線の相手（東京コントロール・羽田）
# ══════════════════════════════════════════════════════════
RA = dict(plane=(960.0, 360.0), left=(430.0, 720.0), right=(1490.0, 720.0))
RA_NAMES = dict(left="東京コントロール", right="羽田")


def _tower(x, y):
    return (F.rect(x - 34, y - 10, 68, 80, COL["panel"], COL["body_ln"], 2, rx=4) + F.line(x, y - 10, x, y - 60, COL["eng"], 5)
            + F.circ(x, y - 66, 8, COL["radar"], COL["dark"], 2))


def radio_base(st0):
    T = Top(2.6, RA["plane"][0], RA["plane"][1] - 92.0)
    g = [F.line(F.BX0 + 20, 790, F.BX1 - 20, 790, COL["mount_ln"], 3), _tower(*RA["left"]), _tower(*RA["right"])]
    g += top_plane_svg(T)
    for side in ("left", "right"):
        x, y = RA[side]
        g.append(F.txtfit(x, y + 116, RA_NAMES[side], 420, cap=32, col=INK, anchor="middle"))
    return g


def ra_link(side):
    (x0, y0), (x1, y1) = RA["plane"], RA[side]
    return (x0 + (x1 - x0) * 0.12, y0 + (y1 - y0) * 0.12), (x1 - (x1 - x0) * 0.06, y1 - 76 - (y1 - y0) * 0.02)


def radio_parts(st):
    a, b = ra_link("left")
    c, d = ra_link("right")
    return [_P("lk", "line", [a, b], stroke=COL["mark"], w=(9 if st["stay"] == "on" else 5), alpha=1.0 if st["link"] == "on" else 0.0),
            _P("ask", "line", [c, d], stroke=COL["radar"], w=5, alpha=(1.0 if st["ask"] == "on" and st["stay"] != "on" else
                                                                   (0.25 if st["stay"] == "on" else 0.0)))]


def radio_stage(prev, st):
    """線は動く部品（切り替えないと答えた段で薄くなる）＝段の層には描かない（層は残る）"""
    return []


# ══════════════════════════════════════════════════════════
#  fix（c506・c507）＝夜の測位と読み取りの幅
# ══════════════════════════════════════════════════════════
FX = dict(st=(1590.0, 800.0), k=22.0, brg=305.0, nm=35.0)       # 無線の目印・1マイルの画素・方位・距離（表3 の①）
FX_ZOOM = (110.0, 300.0, 700.0, 820.0)                           # 寄りの窓
FX_ZK = 150.0                                                    # 寄りの窓の1マイルの画素
FX_PLANE = (5.0, 1.0)                                            # 飛行機：方位の幅（度）・距離の幅（マイル）＝解説 p18
FX_HELI = (1.0, 0.1)                                             # ヘリコプター：同じ


def fx_end():
    sx, sy = FX["st"]
    L = FX["k"] * FX["nm"]
    a = math.radians(FX["brg"])
    return sx + L * math.sin(a), sy - L * math.cos(a)


def fx_fan(width_deg, depth_nm, n=10):
    """寄りの窓の中の扇（光線が上向き＝窓の真ん中が 35マイルの点）"""
    x0, y0, x1, y1 = FX_ZOOM
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 30
    R = FX["nm"]
    h = math.radians(width_deg / 2)
    pts = []
    for r, rng in ((R + depth_nm / 2, range(n + 1)), (R - depth_nm / 2, range(n, -1, -1))):
        for i in rng:
            a = -h + 2 * h * i / n
            pts.append((cx + r * math.sin(a) * FX_ZK, cy - (r * math.cos(a) - R) * FX_ZK))
    return pts


def fix_base(st0):
    sx, sy = FX["st"]
    return [F.rect(F.BX0 + 20, F.BY0 + 50, F.BW - 40, F.BH - 100, COL["night0"], None, 0, rx=12),
            F.circ(sx, sy, 16, COL["radar"], COL["dark"], 3),
            F.line(sx, sy - 20, sx, sy - 250, COL["ghost"], 2, "8 8"), _t(sx + 10, sy - 230, "北", 24, J.TICK)]


def fix_stage(prev, st):
    g = []
    sx, sy = FX["st"]
    ex, ey = fx_end()
    if _on(prev, st, "gps"):
        x, y = 300.0, 420.0
        g.append(F.rect(x - 36, y - 22, 72, 44, COL["panel"], COL["eng"], 3, rx=6) + F.line(x - 70, y, x - 36, y, COL["eng"], 6)
                 + F.line(x + 36, y, x + 70, y, COL["eng"], 6) + F.line(x - 80, y - 50, x + 80, y + 50, COL["red"], 7))
    if _on(prev, st, "ray"):
        g.append(F.line(sx, sy, ex, ey, COL["mark"], 5, "16 10"))
        g.append(F.poly(_arc_pts(sx, sy, 120, 360, FX["brg"]), "none", COL["mark"], 4))
        # ⚠️ 試し焼き ep20_b5：±7度では小さな機の印を長く横切った＝±3度
        g.append(F.poly(_arc_pts(sx, sy, FX["k"] * FX["nm"], FX["brg"] - 3, FX["brg"] + 3), "none", COL["radar"], 4))
        # ⚠️ 焼き直し ep20_b5fix の原寸：弧を ±3度にしても、読み取りの点に置いた小さな機の印を斜めに横切った＝機の印は光線の先へ
        #    48画素ずらす（読み取りの点＝弧と光線の端・門番が測るのは fx_end）
        a = math.radians(FX["brg"])
        T = Top(0.9, ex + 48 * math.sin(a), ey - 48 * math.cos(a) - 30)
        g += top_plane_svg(T)
    if _on(prev, st, "zoom"):
        x0, y0, x1, y1 = FX_ZOOM
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, COL["night1"], COL["radar"], 3, rx=10))
        g.append(F.rect(ex - 22, ey - 22, 44, 44, "none", COL["radar"], 3))
        g.append(F.line(ex - 22, ey - 22, x1, y0 + 20, COL["radar"], 2, "6 8") + F.line(ex - 22, ey + 22, x1, y0 + 120, COL["radar"], 2, "6 8"))
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 30
        g.append(F.line(cx, y1 - 6, cx, y0 + 6, COL["mark"], 2, "10 8"))
    if _on(prev, st, "pa"):
        x0, y0, x1, y1 = FX_ZOOM
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 30
        h = math.radians(FX_PLANE[0] / 2)
        for s in (-1, 1):
            g.append(F.line(cx + s * (FX["nm"] - 1.0) * math.sin(h) * FX_ZK, cy + 1.0 * FX_ZK,
                            cx + s * (FX["nm"] + 0.9) * math.sin(h) * FX_ZK, cy - 0.9 * FX_ZK, COL["mark"], 4))
    if _on(prev, st, "pd"):
        g.append(F.poly(fx_fan(*FX_PLANE), COL["mark"], COL["mark"], 3, True, op=0.45))
    if _on(prev, st, "heli"):
        g.append(F.poly(fx_fan(*FX_HELI), COL["green"], COL["white"], 2.5, True))
    return g


# ══════════════════════════════════════════════════════════
#  hoist（c509）＝夜の山の斜面とヘリコプター（人は描かない）
# ══════════════════════════════════════════════════════════
HO = dict(heli=(1000.0, 390.0), land=(990.0, 664.0), guide_to=(640.0, 742.0))
HO_SLOPE = [(F.BX0 + 20, 860.0), (F.BX0 + 20, 790.0), (420, 760), (760, 712), (1060, 660), (1400, 600), (F.BX1 - 20, 540), (F.BX1 - 20, 860.0)]
HO_TREES = [(300, 770), (380, 760), (520, 740), (600, 728), (820, 702), (900, 690), (1120, 650), (1190, 640), (1300, 620),
            (1480, 588), (1560, 575), (1700, 556)]


def hoist_base(st0):
    x, y = HO["heli"]
    g = [F.rect(F.BX0 + 20, F.BY0 + 50, F.BW - 40, F.BH - 100, COL["night0"], None, 0, rx=12),
         F.poly(HO_SLOPE, COL["slope"], COL["slope_ln"], 2, True)]
    for tx, ty in HO_TREES:
        g.append(F.poly([(tx - 18, ty + 6), (tx, ty - 46), (tx + 18, ty + 6)], COL["tree"], COL["slope_ln"], 1.5, True))
    g += [F.poly([(x - 30, y + 22), (x - 120, y + 260), (x + 90, y + 250), (x + 30, y + 22)], COL["light"], None, None, True, None, 0.16),
          f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="74" ry="30" fill="{COL["eng"]}" stroke="{COL["body_ln"]}" stroke-width="2.5"/>',
          F.line(x + 60, y - 6, x + 170, y - 18, COL["eng"], 9), F.circ(x + 172, y - 20, 16, "none", COL["eng"], 3),
          F.line(x - 120, y - 46, x + 120, y - 46, COL["eng"], 5), F.line(x, y - 30, x, y - 46, COL["eng"], 5),
          F.line(x - 50, y + 40, x + 50, y + 40, COL["eng"], 4)]
    return g


def hoist_stage(prev, st):
    g = []
    x, y = HO["heli"]
    if st["guide"] != prev.get("guide") and st["guide"] in ("on", "fail"):
        tx, ty = HO["guide_to"]
        g.append(F.line(x - 40, y + 30, tx, ty, COL["mark"], 4, "14 10"))
        g.append(_ring(tx, ty, 18, COL["mark"], 4))
        if st["guide"] == "fail":
            g.append(F.line(tx - 22, ty - 46, tx + 22, ty - 90, COL["red"], 7) + F.line(tx - 22, ty - 90, tx + 22, ty - 46, COL["red"], 7))
    if _on(prev, st, "hoist"):
        lx, ly = HO["land"]
        g.append(F.line(lx, y + 32, lx, ly - 30, COL["white"], 3, "10 8"))
        g.append(F.poly([(lx - 12, ly - 34), (lx + 12, ly - 34), (lx, ly - 18)], COL["white"], None, None, True))
        g.append(F.poly([(lx + 70, ly - 120), (lx + 110, ly - 50), (lx + 30, ly - 50)], COL["red"], COL["dark"], 2, True))
        g.append(F.txt(lx + 70, ly - 60, "！", 34, COL["white"], anchor="middle"))
    if _on(prev, st, "nvg"):
        # ⚠️ 試し焼き ep20_b5：ヘリの胴体の上に描くと、赤い斜線がヘリに「×」をつけたように見えた＝ヘリから離して札のそばに
        gx, gy = HO_NVG
        g.append(F.circ(gx - 20, gy, 16, "none", COL["radar"], 4) + F.circ(gx + 20, gy, 16, "none", COL["radar"], 4)
                 + F.line(gx - 4, gy, gx + 4, gy, COL["radar"], 4) + F.line(gx - 46, gy - 30, gx + 46, gy + 30, COL["red"], 6))
    return g


HO_NVG = (1290.0, 500.0)                          # 暗視装置の印（札「暗視装置（当時なし）」の下・ヘリの外）


# ══════════════════════════════════════════════════════════
#  press（c607）＝横から見た尾部の断面（後部圧力隔壁）
# ══════════════════════════════════════════════════════════
PR = (40.0, 430.0 - 44.0 * 40.0, 600.0)           # K・機首の x（画面の外）・真ん中の y（44m の所が x 430）
PR_X0 = 44.0                                       # ここから後ろを描く（前は切る）
PR_BULK = I2.S1_XB                                 # 後部圧力隔壁＝BS2360（p29）＝57.66m
PR_ARROWS = (2.0, 0.8, -0.4, -1.6)                 # 押す矢印の高さ（m・模式）
PR_Z = (3.05, -2.75)                               # 隔壁の弧の上の端・下の端（m・模式）＝🆕 ⑤b-6 で表に出した（値は同じ）


def pr_bulk_pts():
    zt, zb = PR_Z
    return [(PR_BULK + 1.25 * math.cos(math.radians(a)), (zt + zb) / 2 + (zt - zb) / 2 * math.sin(math.radians(a))) for a in range(-90, 91, 10)]


def press_base(st0):
    K, X0, Y0 = PR
    body = side_body(K, X0, Y0, cut_front=PR_X0)
    x0 = X0 + PR_X0 * K
    g = [F.poly(body, "#26313b", COL["body_ln"], 3, True),
         F.line(x0, Y0 - 3.6 * K, x0, Y0 + 3.6 * K, COL["ghost"], 3, "8 8")]
    q = side_pts(K, X0, Y0, pr_bulk_pts())
    g.append(F.poly(q, "none", COL["dark"], 11) + F.poly(q, "none", COL["mark"], 6))
    return g


def press_stage(prev, st):
    K, X0, Y0 = PR
    g = []
    if _on(prev, st, "press"):
        up = [p for p in IL._smooth(I2.S1_UP, per=6) if PR_X0 <= p[0] <= PR_BULK]
        lo = [p for p in IL._smooth(I2.S1_LO, per=6) if PR_X0 <= p[0] <= PR_BULK]
        bulk = pr_bulk_pts()
        reg = [(PR_X0, up[0][1])] + up + [(PR_BULK, bulk[-1][1])] + list(reversed(bulk)) + [(PR_BULK, bulk[0][1])] + list(reversed(lo)) + [(PR_X0, lo[0][1])]
        g.append(F.poly(side_pts(K, X0, Y0, reg), COL["press"], None, None, True, None, 0.55))
        for i in range(14):
            x = 380 + 95 * i
            g.append(F.circ(x, 300 + (i % 3) * 22, 3, COL["white"], None, None, 0.6))
    if _on(prev, st, "push"):
        for z in PR_ARROWS:
            a = side_pts(K, X0, Y0, [(PR_BULK - 4.2, z), (PR_BULK - 0.5, z)])
            g.append(F.arrow(*a[0], *a[1], COL["mark"], 7, 22))
    return g


# ══════════════════════════════════════════════════════════
#  bag（c620）＝尾翼の中の気圧と、海の近くと山の上の袋
# ══════════════════════════════════════════════════════════
BG_FIN = (24.0, 260.0 - 58.8 * 24.0, 790.0)       # 横から見た垂直尾翼（K・x0・根元の y）
BG_SEA, BG_MT = (1060.0, 640.0), (1600.0, 560.0)  # 袋の真ん中（海の近く・山の上）
BG_BAG = (120.0, 160.0)                            # 袋の幅・高さ（海の近く）
BG_SWELL = 1.28                                    # ふくらみ（山の上の袋の幅の倍率＝模式）


def bag_pts(cx, cy, k, n=48):
    """袋の形＝角の丸い四角（超楕円）。k＝幅の倍率（1＝海の近く）。ふくらむほど丸く・少し高く（模式）"""
    w, h = BG_BAG[0] * k, BG_BAG[1] * (1 + (k - 1) * 0.35)
    e = 4.0 - 1.6 * (k - 1.0) / (BG_SWELL - 1.0) if k > 1.0 else 4.0
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        c, s = math.cos(a), math.sin(a)
        pts.append((cx + w / 2 * math.copysign(abs(c) ** (2 / e), c), cy + h / 2 * math.copysign(abs(s) ** (2 / e), s)))
    return pts


def bag_parts(st):
    k = BG_SWELL if st["swell"] == "on" else 1.0
    a = 1.0 if st["bags"] == "on" else 0.0
    return [_P("bag_sea", "poly", bag_pts(*BG_SEA, 1.0), fill=COL["bag"], stroke=COL["bag_ln"], w=3, alpha=a),
            _P("bag_mt", "poly", bag_pts(*BG_MT, k), fill=COL["bag"], stroke=COL["bag_ln"], w=3, alpha=a)]


def bag_base(st0):
    K, X0, Y0 = BG_FIN
    fin = [(x, z - 3.1) for x, z in I2.S1_FIN]
    g = [F.poly(side_pts(K, X0, Y0, fin), COL["fin"], COL["body_ln"], 3, True),
         F.line(X0 + 56.0 * K, Y0, X0 + 72.5 * K, Y0, COL["body_ln"], 4),
         F.line(820, F.BY0 + 60, 820, F.BY1 - 60, COL["ghost"], 2, "6 10"),
         F.poly([(880, 800), (1240, 800), (1240, 830), (880, 830)], COL["sea"], None, None, True)]
    for i in range(6):
        g.append(F.poly(_arc_pts(910 + 60 * i, 812, 22, 300, 420, 8), "none", COL["sea_ln"], 3))
    g.append(F.poly([(1340, 830), (1600, 690), (1660, 720), (1800, 830)], COL["mount"], COL["mount_ln"], 2, True))
    return g


def bag_stage(prev, st):
    g = []
    if _on(prev, st, "inner"):
        K, X0, Y0 = BG_FIN
        cx, cy = X0 + 65.0 * K, Y0 - 5.0 * K
        for dx, dy in ((-1, 0), (1, 0), (-0.55, -0.85), (0.55, -0.85), (0, 0.9)):
            g.append(F.arrow(cx + dx * 18, cy + dy * 18, cx + dx * 66, cy + dy * 66, COL["red"], 6, 18))
    return g


# ══════════════════════════════════════════════════════════
#  apt（c315）＝3つの空港（東西の順）と、羽田を選んだ理由の言葉（p117 の字）
# ══════════════════════════════════════════════════════════
# 🔴 報告書に滑走路の長さの数は無い（p117 は「空港の規模、滑走路長及びその他の施設環境」という理由の言葉だけ）＝棒にしない。
#    並びは東西の順（経度＝一般の地図の値・illu20.S2_PTS と同じ。大阪＝伊丹）・間は模式
AP = dict(y=560.0, x0=200.0, x1=1720.0)
AP_PTS = dict(osaka=(380.0, "大阪国際空港", 135.438), nagoya=(820.0, "名古屋空港", 136.924), haneda=(1500.0, "東京国際空港", 139.780))
AP_WHY = ("空港の規模", "滑走路長", "その他の施設環境")            # p117 の字そのまま


def apt_base(st0):
    g = [F.line(AP["x0"], AP["y"], AP["x1"], AP["y"], COL["mount_ln"], 4), _t(AP["x0"], AP["y"] + 44, "西", 24, J.TICK),
         _t(AP["x1"], AP["y"] + 44, "東", 24, J.TICK, "end")]
    for k, (x, nm, _lon) in AP_PTS.items():
        g.append(F.circ(x, AP["y"], 16, COL["radar"], COL["dark"], 3))
        g.append(F.txtfit(x, AP["y"] + 64, nm, 360, cap=32, col=INK, anchor="middle"))
    return g


def apt_stage(prev, st):
    g = []
    if _on(prev, st, "pick"):
        x = AP_PTS["haneda"][0]
        g.append(_ring(x, AP["y"], 40, COL["mark"]))
        g.append(F.circ(AP_PTS["nagoya"][0], AP["y"], 30, "none", COL["ghost"], 3))
    if _on(prev, st, "why"):
        x = AP_PTS["haneda"][0]
        for i, w in enumerate(AP_WHY):
            y = AP["y"] + 140 + i * 58
            g.append(F.rect(x - 170, y - 38, 340, 50, COL["dark"], COL["mark"], 3, rx=10)
                     + F.txtfit(x, y - 2, w, 310, cap=30, col=INK, anchor="middle"))
    if _on(prev, st, "ok"):
        x = AP_PTS["haneda"][0]
        g.append(F.poly([(x - 30, AP["y"] - 120), (x - 6, AP["y"] - 94), (x + 40, AP["y"] - 150)], "none", COL["green"], 9))
    return g


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-10）：第6〜8章の模式（隔壁の継ぎ目・亀裂・点検）＝12の見え方
# ══════════════════════════════════════════════════════════
# 形のもと＝付図-32・付図-36（隔壁の円・L18・ストラップ＝illu20 の S6 正面と同じ表 S6F_STRAPS）・付図-38(a)(b)（p174＝L18 の断面の
#   2列と1列）・別添1 付図-3（実際の継ぎ方の板の並び＝illu20.S6_LAYERS）。🔴 数字は書かない（語りと字幕に任せる）。
#   記録の値（列の数・強さの比・速さの比・ストラップの番号・確率・見える長さの比ほか）は門番 check_mech の REC_M20 の側
WEB = dict(up=C20["web_up"], lo=C20["web_lo"], spl=C20["splice"], fil=C20["filler"], riv=C20["rivet"], seal="#e9d9a6",
           seal_ln="#6b5a2c")


def _eye(x, y, s=1.0, col=INK):
    """目の印（点検で見る向き＝人は描かない）"""
    n = 16
    up = [(x - 46 * s + 92 * s * i / n, y - 26 * s * math.sin(math.pi * i / n)) for i in range(n + 1)]
    lo = [(x + 46 * s - 92 * s * i / n, y + 26 * s * math.sin(math.pi * i / n)) for i in range(n + 1)]
    return (F.poly(up + lo, COL["dark"], col, 4, True) + F.circ(x, y, 13 * s, col, None, None)
            + F.circ(x, y, 5 * s, COL["dark"], None, None))


def _brk(x0, y0, x1, y1, col, w=5, dash=None, tick=12):
    """長さの括弧（両端に短い棒）"""
    ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
    dx, dy = tick * math.cos(ang), tick * math.sin(ang)
    return (F.line(x0, y0, x1, y1, col, w, dash) + F.line(x0 - dx, y0 - dy, x0 + dx, y0 + dy, col, w)
            + F.line(x1 - dx, y1 - dy, x1 + dx, y1 + dy, col, w))


def _zig(x0, y0, x1, y1, n=8, amp=7.0):
    """ひびのぎざぎざの点"""
    L = math.hypot(x1 - x0, y1 - y0) or 1.0
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    return [(x0 + (x1 - x0) * i / n + (0 if i in (0, n) else (amp if i % 2 else -amp)) * nx,
             y0 + (y1 - y0) * i / n + (0 if i in (0, n) else (amp if i % 2 else -amp)) * ny) for i in range(n + 1)]


def _crack(pts, w=6):
    return F.poly(pts, "none", COL["dark"], w + 5) + F.poly(pts, "none", COL["red"], w)


def _disk(c, R):
    """隔壁を後ろから見た円（付図-32・付図-36＝S6 の正面と同じ形）：上半分・下半分・36本の補強材（間隔は模式）・ストラップ（点線）"""
    cx, cy = c
    g = [F.poly(_arc_pts(cx, cy, R, -90, 90, 40), WEB["up"], None, None, True),
         F.poly(_arc_pts(cx, cy, R, 90, 270, 40), WEB["lo"], None, None, True)]
    for i in range(1, 36):
        y = cy - R + i * 2 * R / 36.0
        hw = math.sqrt(max(0.0, R * R - (y - cy) ** 2))
        g.append(F.line(cx - hw, y, cx + hw, y, COL["body_ln"], 1.2, op=0.35))
    for f_ in I2.S6F_STRAPS:
        g.append(F.poly(_arc_pts(cx, cy, R * f_, 0, 360, 72), "none", COL["body_ln"], 1.6, True, "6 7", 0.5))
    g.append(F.circ(cx, cy, R, "none", COL["dark"], 5))
    g.append(F.circ(cx, cy, 16, COL["eng"], COL["dark"], 2.5))
    return g


# ── fatigue（c705）＝くり返しの力で、穴の縁からひびが少しずつ伸びる（一般の仕組み＝p65「リベット孔縁より疲労亀裂」・数字は書かない）──
FA_PLATE = (330.0, 380.0, 1190.0, 760.0)
FA_HOLE = (760.0, 570.0, 44.0)                     # 穴（x・y・半径）
FA_LEN = dict(r=230.0, l=150.0)                    # 伸びきったひびの長さ（穴の縁から・画素・模式）
FA_GAP = 0.0                                       # ひびの根元と穴の縁のあいだ（🔴 門番の陽性対照がここを壊す）
FA_DIR = 0.0                                       # ひびの向き（度・0＝横）（同上）
FA_LOAD = 90.0                                     # 引く力の向き（度・90＝縦）＝ひびは力に直角に伸びる
FA_SEG, FA_LAG = 3, 0.7                            # ひびを3つに分け、0.7秒ずつ遅らせて伸ばす（少しずつ）
FA_WIRE = [(1390.0, 320.0), (1545.0, 465.0), (1700.0, 320.0)]


def fa_crack(side):
    """ひび（根元＝穴の縁 → 先）。side＝"r"（右）・"l"（左）"""
    x, y, r = FA_HOLE
    s = 1.0 if side == "r" else -1.0
    a = math.radians(FA_DIR)
    x0, y0 = x + s * (r + FA_GAP) * math.cos(a), y - s * (r + FA_GAP) * math.sin(a)
    L = FA_LEN[side]
    return (x0, y0), (x0 + s * L * math.cos(a), y0 - s * L * math.sin(a))


def fatigue_parts(st):
    out = []
    on = st["crack"] == "on"
    for side in ("r", "l"):
        (x0, y0), (x1, y1) = fa_crack(side)
        for i in range(FA_SEG):
            a = (x0 + (x1 - x0) * i / FA_SEG, y0 + (y1 - y0) * i / FA_SEG)
            b = (x0 + (x1 - x0) * (i + 1) / FA_SEG, y0 + (y1 - y0) * (i + 1) / FA_SEG)
            out.append(_P(f"cr{side}{i}", "line", [a, b if on else a], stroke=COL["red"], w=8, alpha=1.0 if on else 0.0,
                          lag=FA_LAG * i))
    return out


def _fa_arrows(xs, w):
    x0, y0, x1, y1 = FA_PLATE
    a = math.radians(FA_LOAD)
    dx, dy = math.cos(a), -math.sin(a)
    g = []
    for xx in xs:
        g.append(F.arrow(xx, y0 - 8, xx + 72 * dx, y0 - 8 + 72 * dy, COL["mark"], w, 22))
        g.append(F.arrow(xx, y1 + 8, xx - 72 * dx, y1 + 8 - 72 * dy, COL["mark"], w, 22))
    return g


def fatigue_base(st0):
    x0, y0, x1, y1 = FA_PLATE
    x, y, r = FA_HOLE
    return [F.rect(x0, y0, x1 - x0, y1 - y0, WEB["lo"], COL["dark"], 4, rx=6), F.circ(x, y, r, COL["dark"], "#5a6670", 4)]


def fatigue_stage(prev, st):
    g = []
    x = FA_HOLE[0]
    if st["load"] != "off" and prev["load"] == "off":
        g += _fa_arrows([x], 8)
    if _on(prev, st, "load", "rep"):
        g += _fa_arrows([x - 110, x + 110], 5)
    if _on(prev, st, "wire"):
        (ax, ay), (bx, by), (cx_, cy_) = FA_WIRE
        ghost = [(ax - 60, ay + 70), (bx, by), (cx_ + 60, cy_ + 70)]
        g.append(F.poly(ghost, "none", COL["ghost"], 6, False, "10 8"))
        g.append(F.poly(FA_WIRE, "none", COL["dark"], 16) + F.poly(FA_WIRE, "none", "#c9d0d6", 10))
        g.append(_crack(_zig(bx - 18, by - 4, bx + 18, by - 4, 4, 5.0), 5))
        for (px, py), (qx, qy) in (((ax, ay), ghost[0]), ((cx_, cy_), ghost[2])):
            g.append(F.arrow(px, py + 12, qx + 8, qy - 14, COL["mark"], 4, 16))
    return g


# ── rows（c711）＝L18 の継ぎ目の断面：2列で留めた所と1列で留めた所（付図-38(a)(b) を簡単に＝2枚の板の重なりと列の数だけ）・
#    強さの棒（本来＝1・1列の所＝約0.7＝p102・p124）──
RW_CX = dict(a=640.0, b=1280.0)
RW_T = 26.0                                         # 板の厚さ（画素・強調）
RW_TOP, RW_BOT = 290.0, 720.0
RW_LAP = dict(a=(430.0, 560.0), b=(468.0, 522.0))   # 重なり（下の板の上の端・上の板の下の端）
RW_ROWS = dict(a=(465.0, 525.0), b=(495.0,))        # リベットの列の高さ（🔴 門番の陽性対照がここを壊す）
RW_STR = dict(a=1.0, b=0.70)                        # 強さ（本来＝1）（同上）
RW_BAR = (800.0, 300.0)                             # 強さの棒の y・本来の長さ（画素）
RW_TIT = dict(a="2列で留めた所", b="1列で留めた所")


def rows_base(st0):
    g = []
    for k, cx in RW_CX.items():
        lap0, lap1 = RW_LAP[k]
        g.append(F.rect(cx, RW_TOP, RW_T, lap1 - RW_TOP, WEB["up"], COL["dark"], 3))            # 上の板（後ろの側）
        g.append(F.rect(cx - RW_T, lap0, RW_T, RW_BOT - lap0, WEB["lo"], COL["dark"], 3))        # 下の板（客室の側）
        for y in RW_ROWS[k]:
            g.append(F.rect(cx - RW_T - 14, y - 7, 2 * RW_T + 28, 14, WEB["riv"], COL["dark"], 2))
            g.append(F.rect(cx - RW_T - 24, y - 14, 10, 28, WEB["riv"], COL["dark"], 2, rx=3))
            g.append(F.rect(cx + RW_T + 14, y - 14, 10, 28, WEB["riv"], COL["dark"], 2, rx=3))
        g.append(F.txtfit(cx, RW_BOT + 44, RW_TIT[k], 420, cap=32, col=INK, anchor="middle"))
    return g


def rows_stage(prev, st):
    g = []
    if _on(prev, st, "bars"):
        y, L = RW_BAR
        for k, cx in RW_CX.items():
            g.append(F.rect(cx - L / 2, y - 14, L, 28, "none", COL["ghost"], 3, dash="8 6"))
            g.append(F.rect(cx - L / 2, y - 14, L * RW_STR[k], 28, COL["blue"] if k == "a" else COL["red"], COL["dark"], 2))
    if _on(prev, st, "crack"):
        cx, y = RW_CX["b"], RW_ROWS["b"][0]
        g.append(_crack(_zig(cx - 4, y + 17, cx + RW_T + 4, y + 17, 4, 4.0), 5))
    return g


# ── grow（c712）＝亀裂の伸び方の比べ（1列は2列の2倍強の速さ＝p65）。線の形は模式（直線）・数字は書かない ──
GR = dict(x0=330.0, y0=730.0, x1=1560.0, y1=320.0)
GR_YT = 470.0                                       # 同じ長さ（模式）
GR_X2 = 1400.0                                      # 2列の線が同じ長さに届く所
GR_RATIO = 2.1                                      # 1列の速さ ÷ 2列の速さ（「2倍強」の模式の値）（🔴 門番の陽性対照がここを壊す）


def gr_line(k):
    x0, y0 = GR["x0"], GR["y0"]
    s = (y0 - GR_YT) / (GR_X2 - x0) * (GR_RATIO if k == "one" else 1.0)
    xe = min(GR["x1"], x0 + (y0 - GR["y1"]) / s)
    return (x0, y0), (xe, y0 - s * (xe - x0))


def gr_hit(k):
    """その線が同じ長さ（GR_YT）に届く x"""
    (x0, y0), (x1, y1) = gr_line(k)
    return x0 + (y0 - GR_YT) * (x1 - x0) / (y0 - y1)


def grow_base(st0):
    x0, y0, x1, y1 = GR["x0"], GR["y0"], GR["x1"], GR["y1"]
    return [F.arrow(x0, y0, x1 + 40, y0, COL["mount_ln"], 4, 20), F.arrow(x0, y0, x0, y1 - 30, COL["mount_ln"], 4, 20),
            _t(x1 + 40, y0 + 46, "飛行の回数", 26, J.TICK, "end"), _t(x0 + 16, y1 - 6, "亀裂の長さ", 26, J.TICK)]


def grow_stage(prev, st):
    g = []
    for k, col in (("two", COL["blue"]), ("one", COL["red"])):
        if _on(prev, st, k):
            a, b = gr_line(k)
            g.append(F.line(*a, *b, COL["dark"], 13) + F.line(*a, *b, col, 8))
    if _on(prev, st, "same"):
        y0 = GR["y0"]
        h1, h2 = gr_hit("one"), gr_hit("two")
        g.append(F.line(GR["x0"], GR_YT, h2, GR_YT, COL["mark"], 3, "10 8"))
        for h, col, dy in ((h1, COL["red"], 34), (h2, COL["blue"], 66)):
            g.append(F.line(h, GR_YT, h, y0, col, 3, "6 6"))
            g.append(_brk(GR["x0"], y0 + dy, h, y0 + dy, col, 5))
    return g


# ── fs（c714）＝1ベイ・フェール・セーフ（p110）と、1列の所（左側の第1〜第3ストラップの間の2ベイ分＝別添1 p248）──
FS_C, FS_R = (760.0, 545.0), 290.0
FS_BAY_R = (0.60, 0.71)                             # 1ベイの中の亀裂（右側の継ぎ目の上・円の半径の比）（🔴 陽性対照）
FS_ONE = (0, 2)                                     # 1列の所＝S6F_STRAPS の番号（0 始まり）の間（同上）


def fs_base(st0):
    return _disk(FS_C, FS_R) + [_t(FS_C[0] - FS_R - 14, FS_C[1] + 9, "L18", 26, INK, "end")]


def fs_stage(prev, st):
    cx, cy = FS_C
    g = []
    if _on(prev, st, "bay"):
        a, b = FS_BAY_R
        lo = max([f_ for f_ in I2.S6F_STRAPS if f_ <= a], default=0.0)
        hi = min([f_ for f_ in I2.S6F_STRAPS if f_ >= b], default=1.0)
        for f_ in (lo, hi):
            g.append(F.poly(_arc_pts(cx, cy, FS_R * f_, 70, 110, 12), "none", COL["green"], 6))
        g.append(_crack(_zig(cx + FS_R * a, cy, cx + FS_R * b, cy, 6, 6.0), 5))
    if _on(prev, st, "one"):
        r0, r1 = (FS_R * I2.S6F_STRAPS[i] for i in FS_ONE)
        g.append(F.line(cx - r0, cy, cx - r1, cy, COL["dark"], 16) + F.line(cx - r0, cy, cx - r1, cy, COL["mark"], 9))
        n = 7
        for i in range(n):
            x = cx - r0 + (r0 - r1) * (i + 0.5) / n
            g.append(_crack([(x - 4, cy - 15), (x + 3, cy - 5), (x - 3, cy + 5), (x + 4, cy + 15)], 3))
    return g


# ── half（c805）＝横から見た尾部の断面：後部圧力隔壁の上半分（元のまま）と下半分（1978年に取り替え＝別添1 p246）──
HF_NEW = "lo"                                       # 取り替えた側（🔴 陽性対照）


def hf_lens(which):
    """隔壁（横から見た弧）と弦のあいだを上と下に分けた面（m）"""
    zm = sum(PR_Z) / 2
    arc = pr_bulk_pts()                              # 下（-90度）→ 上（+90度）
    pts = [p for p in arc if (p[1] >= zm - 1e-9 if which == "up" else p[1] <= zm + 1e-9)]
    return pts + [(PR_BULK, zm)]


def _tail_cut_base(K, X0, Y0):
    body = side_body(K, X0, Y0, cut_front=PR_X0)
    x0 = X0 + PR_X0 * K
    return [F.poly(body, "#26313b", COL["body_ln"], 3, True), F.line(x0, Y0 - 3.6 * K, x0, Y0 + 3.6 * K, COL["ghost"], 3, "8 8")]


def half_base(st0):
    K, X0, Y0 = PR
    q = side_pts(K, X0, Y0, pr_bulk_pts())
    return _tail_cut_base(K, X0, Y0) + [F.poly(q, "none", COL["dark"], 11) + F.poly(q, "none", WEB["up"], 6)]


def half_stage(prev, st):
    K, X0, Y0 = PR
    g = []
    if _on(prev, st, "name"):
        g.append(F.poly(side_pts(K, X0, Y0, pr_bulk_pts()), "none", COL["mark"], 6))
    if _on(prev, st, "half"):
        for w in ("up", "lo"):
            g.append(F.poly(side_pts(K, X0, Y0, hf_lens(w)), WEB["lo"] if w == HF_NEW else WEB["up"], COL["dark"], 3, True))
    if _on(prev, st, "join"):
        x, y = side_pts(K, X0, Y0, [(PR_BULK + 1.25, sum(PR_Z) / 2)])[0]
        g.append(_ring(x, y, 26, COL["mark"]))
    return g


# ── edge（c807）＝穴と板の縁の余白（エッジ・マージン）。測る起点の線は描かない・数字は書かない ──
ED_PLATE = (300.0, 470.0, 1560.0, 760.0)            # x0・縁の y・x1・下の y
ED_R = 22.0
ED_GOOD = (620.0, 600.0)                            # 余白の足りている穴
ED_BAD = (1180.0, 522.0)                            # 縁に近すぎる穴
ED_REQ = 70.0                                       # 手引きの決まり（模式の長さ・画素）（🔴 陽性対照）


def ed_margin(h):
    return h[1] - ED_R - ED_PLATE[1]


def edge_base(st0):
    x0, ye, x1, yb = ED_PLATE
    return [F.rect(x0, ye, x1 - x0, yb - ye, WEB["lo"], None, None), F.line(x0, ye, x1, ye, COL["dark"], 6),
            F.circ(*ED_GOOD, ED_R, COL["dark"], "#5a6670", 3), _t(x1 - 10, ye - 14, "板の縁", 24, J.TICK, "end")]


def edge_stage(prev, st):
    ye = ED_PLATE[1]
    g = []
    if _on(prev, st, "good"):
        x, y = ED_GOOD
        g.append(_brk(x + 50, y - ED_R, x + 50, ye, COL["mark"], 5))
    if _on(prev, st, "bad"):
        x, y = ED_BAD
        g.append(F.circ(x, y, ED_R, COL["dark"], "#5a6670", 3))
        g.append(_crack(_zig(x, y - ED_R, x + 6, ye, 4, 4.0), 4))
    if _on(prev, st, "req"):
        x, y = ED_BAD
        g.append(_brk(x + 70, ye, x + 70, ye + ED_REQ, COL["green"], 5, "8 6"))
    return g


# ── seal（c816）＝継ぎ目の断面（実際の継ぎ方＝illu20.S6_LAYERS の板の並び）と、縁を覆うシール材（フィレット・シール＝p103・付図-38）──
SL = dict(k=110.0, cx=700.0, cy=520.0, edge=2.3)
SL_EYE = (1210.0, 610.0)
SL_BEAD_DY = 0.0                                    # シールの位置のずれ（🔴 陽性対照）


def sl_geo():
    k, cx, cy = SL["k"], SL["cx"], SL["cy"]
    w = I2.S6_T * k
    xs = {nm: cx + (i - 1) * w for i, nm in enumerate(I2.S6_ORDER)}
    e = SL["edge"]
    L = {nm: (None if r is None else (max(-e, r[0]), min(e, r[1]))) for nm, r in I2.S6_LAYERS["real"].items()}
    return k, cx, cy, w, xs, L


def sl_beads():
    """シールの三角（板の端と、となりの板の面の角）＝[(板の名, 角の点, 三角の3点)]"""
    k, cx, cy, w, xs, L = sl_geo()
    lg = 1.6 * w
    out = []
    ye = cy + L["upper"][1] * k + SL_BEAD_DY           # 上の板の下の端（後ろの側）
    c = (xs["upper"] - w / 2, ye)
    out.append(("upper", c, [(xs["upper"] + w / 2, ye), (c[0], ye + lg), c]))
    ys = cy + L["splice"][1] * k + SL_BEAD_DY          # 継ぎ板の下の端（後ろの側）
    c = (xs["splice"] - w / 2, ys)
    out.append(("splice", c, [(xs["splice"] + w / 2, ys), (c[0], ys + lg), c]))
    yl = cy + L["lower"][0] * k + SL_BEAD_DY           # 下の板の上の端（客室の側）
    c = (xs["lower"] + w / 2, yl)
    out.append(("lower", c, [(xs["lower"] - w / 2, yl), (c[0], yl - lg), c]))
    return out


def seal_base(st0):
    k, cx, cy, w, xs, L = sl_geo()
    col = dict(lower=WEB["lo"], splice=WEB["spl"], upper=WEB["up"], filler=WEB["fil"])
    g = []
    for nm in ("lower", "upper", "splice", "filler"):
        rng = L[nm]
        if not rng:
            continue
        x = xs["splice" if nm == "filler" else nm]
        g.append(F.rect(x - w / 2, cy + rng[0] * k, w, (rng[1] - rng[0]) * k, col[nm], COL["dark"], 2.5))
    xl, xr = xs["lower"] - w / 2, xs["upper"] + w / 2
    for r in I2.S6_ROWS:
        y = cy + r * k
        g.append(F.rect(xl - 0.20 * k, y - 0.20 * k, 0.20 * k, 0.40 * k, WEB["riv"], COL["dark"], 2.5, rx=4))
        g.append(F.rect(xl, y - 0.07 * k, xr - xl, 0.14 * k, WEB["riv"], COL["dark"], 1.5))
        g.append(F.rect(xr, y - 0.19 * k, 0.12 * k, 0.38 * k, WEB["riv"], COL["dark"], 2.5, rx=4))
    yb = cy + SL["edge"] * k + 40
    g.append(_t(xl - 0.6 * k, yb, "客室の側", 24, J.TICK, "end"))
    g.append(_t(xr + 0.6 * k, yb, "後ろの側", 24, J.TICK))
    return g


def seal_stage(prev, st):
    g = []
    if _on(prev, st, "seal"):
        for nm, c, tri in sl_beads():
            g.append(F.poly(tri, WEB["seal"], WEB["seal_ln"], 3, True))
    if _on(prev, st, "eye"):
        ex, ey = SL_EYE
        g.append(_eye(ex, ey))
        for nm, c, tri in sl_beads():
            if nm in ("upper", "splice"):
                g.append(F.line(ex - 52, ey, tri[0][0] + 6, (tri[0][1] + tri[1][1]) / 2, INK, 3, "10 8"))
    return g


# ── rear（c902・c903）＝隔壁を後ろから見た円：後面全体の目視検査（G2 レベル相当）・L18 は特別な点検箇所に指定されていない（p104）──
RE_C, RE_R = (720.0, 545.0), 290.0
RE_EYE = (1200.0, 560.0)
RE_ALL = 1.0                                        # 目で見る範囲の半径の比（全体＝1）（🔴 陽性対照）


def rear_base(st0):
    return _disk(RE_C, RE_R) + [_t(RE_C[0] - RE_R - 14, RE_C[1] + 9, "L18", 26, INK, "end")]


def rear_stage(prev, st):
    cx, cy = RE_C
    g = []
    if _on(prev, st, "l18"):
        g.append(F.line(cx - RE_R, cy, cx - 18, cy, COL["mark"], 5, "14 10"))
    if _on(prev, st, "all"):
        g.append(F.circ(cx, cy, RE_R * RE_ALL, COL["mark"], None, None, op=0.22))
        ex, ey = RE_EYE
        g.append(_eye(ex, ey))
        for s in (-1, 1):
            g.append(F.line(ex - 52, ey, cx + RE_R * 0.2, cy + s * RE_R * 0.96, INK, 2.5, "10 8"))
    return g


# ── clen（c904）＝リベットの頭と亀裂：穴の両側の平均の長さ（約10ミリ）と見える長さ（約8ミリ）＝p100（数字は書かない・比だけ）──
#    隠れる所はリベットの頭で代表した（報告書＝頭とストラップで隠れる）
CL_C = (760.0, 540.0)
CL_HOLE = 80.0                                      # 穴の半径（画素・模式）
CL_MM = 32.0                                        # 1ミリの画素（模式）
CL_LEN, CL_VIS = 10.0, 8.0                          # 亀裂の長さ・見える長さ（ミリ）（🔴 陽性対照）
CL_PLATE = (300.0, 360.0, 1200.0, 720.0)


def cl_head():
    """頭の半径＝穴の縁から、隠れる長さ（長さ − 見える長さ）ぶん外"""
    return CL_HOLE + (CL_LEN - CL_VIS) * CL_MM


def clen_base(st0):
    x0, y0, x1, y1 = CL_PLATE
    cx, cy = CL_C
    return [F.rect(x0, y0, x1 - x0, y1 - y0, WEB["up"], COL["dark"], 3, rx=6),
            F.circ(cx, cy, cl_head(), WEB["riv"], COL["dark"], 4), F.circ(cx, cy, cl_head() - 14, "none", "#7d8a95", 3),
            F.poly(_arc_pts(cx, cy, CL_HOLE, 0, 360, 48), "none", INK, 2.5, True, "8 7", 0.8)]


def clen_stage(prev, st):
    cx, cy = CL_C
    g = []
    hd, L = cl_head(), CL_HOLE + CL_LEN * CL_MM
    if _on(prev, st, "crack"):
        for s in (-1, 1):
            g.append(F.line(cx + s * CL_HOLE, cy, cx + s * hd, cy, COL["red"], 5, "8 6"))
            g.append(_crack([(cx + s * hd, cy), (cx + s * L, cy)], 6))
    if _on(prev, st, "len"):
        g.append(_brk(cx + CL_HOLE, cy - 64, cx + L, cy - 64, COL["mark"], 5))
        g.append(_brk(cx + hd, cy + 64, cx + L, cy + 64, COL["green"], 5))
    return g


# ── prob（c905・c906）＝見つける確率の計算（p100：1つの亀裂 10パーセント程度・少なくとも1つ 14〜60パーセント程度）。
#    幅は破線の枠＝1つの値にしない。目盛りの数字だけ書く（記録の値そのもの＝左上に「模式」を付けない）──
PB = dict(x0=620.0, x1=1600.0, ax=740.0)
PB_ROW = dict(one=420.0, many=590.0)
PB_H = 76.0
PB_ONE = 10.0                                       # （🔴 陽性対照）
PB_MANY = (14.0, 60.0)                              # （同上）
PB_TICKS = (0, 20, 40, 60, 80, 100)


def pb_x(v):
    return PB["x0"] + (PB["x1"] - PB["x0"]) * v / 100.0


def prob_base(st0):
    g = [F.line(PB["x0"], PB["ax"], PB["x1"], PB["ax"], COL["mount_ln"], 4)]
    for v in PB_TICKS:
        x = pb_x(v)
        g.append(F.line(x, PB["ax"], x, PB["ax"] + 14, COL["mount_ln"], 3))
        g.append(F.line(x, PB_ROW["one"] - 70, x, PB["ax"], COL["ghost"], 1.5, "4 8"))
        g.append(_t(x, PB["ax"] + 50, f"{v}%", 26, J.TICK, "middle"))
    return g


def prob_stage(prev, st):
    g = []
    if _on(prev, st, "one"):
        y = PB_ROW["one"]
        g.append(F.rect(PB["x0"], y - PB_H / 2, pb_x(PB_ONE) - PB["x0"], PB_H, COL["mark"], COL["dark"], 2))
        g.append(F.txtfit(PB["x0"] - 24, y + 12, "1つの亀裂", 480, cap=34, col=INK, anchor="end"))
    if _on(prev, st, "many"):
        y = PB_ROW["many"]
        a, b = (pb_x(v) for v in PB_MANY)
        g.append(F.rect(a, y - PB_H / 2, b - a, PB_H, COL["mark"], None, None, op=0.25))
        g.append(F.rect(a, y - PB_H / 2, b - a, PB_H, "none", COL["mark"], 5, dash="14 9"))
        g.append(F.txtfit(PB["x0"] - 24, y + 12, "少なくとも1つ", 480, cap=34, col=INK, anchor="end"))
    if _on(prev, st, "q"):
        g.append(_t(pb_x(PB_MANY[1]) + 70, PB_ROW["many"] + 28, "？", 84, COL["red"], "middle"))
    return g


# ── two（c908）＝2つの場合の比べ（p105（コ）：正規に製作・適正な修理なら、C整備の時点で亀裂は多数できない＝妥当な点検方法）──
TW_C = dict(a=(520.0, 560.0), b=(1240.0, 560.0))
TW_R = 220.0
TW_CRACKS = dict(a=0, b=9)                          # L18 の左側（第1〜第3ストラップの間）の亀裂の印の数（模式）（🔴 陽性対照）
TW_TIT = dict(a="正しい作りと修理", b="事故機（誤った修理）")


def two_base(st0):
    g = []
    for k, c in TW_C.items():
        cx, cy = c
        g += _disk(c, TW_R)
        g.append(F.txtfit(cx, cy - TW_R - 30, TW_TIT[k], 520, cap=32, col=INK, anchor="middle"))
        n = TW_CRACKS[k]
        r0, r1 = TW_R * I2.S6F_STRAPS[0], TW_R * I2.S6F_STRAPS[2]
        for i in range(n):
            x = cx - r0 + (r0 - r1) * (i + 0.5) / n
            g.append(_crack([(x - 3, cy - 12), (x + 2, cy - 4), (x - 2, cy + 4), (x + 3, cy + 12)], 3))
    return g


def tw_check():
    cx, cy = TW_C["a"]
    x, y = cx + TW_R * 0.78, cy - TW_R * 0.78
    return [(x - 34, y), (x - 8, y + 28), (x + 44, y - 36)]


def two_stage(prev, st):
    cx, cy = TW_C["a"]
    g = []
    if _on(prev, st, "pick"):
        g.append(_ring(cx, cy, TW_R + 10, COL["green"]))
    if _on(prev, st, "ok"):
        g.append(F.poly(tw_check(), "none", COL["dark"], 16) + F.poly(tw_check(), "none", COL["green"], 10))
    return g


# ── lav（c913）＝横から見た客室の後ろ：いちばん後ろの化粧室・後ろのコートルーム（p103）・1978年の事故の変形（可能性＝p103）。
#    配置と変形の大きさは模式（変形は大きく描いた）──
LV = dict(lav=(54.2, 56.9), coat=(50.6, 53.6), floor=-1.2, top=1.6)   # 前後（m）・床・天井（m）（🔴 陽性対照＝lav）
LV_BEND = 1.6                                       # 変形の模式の角度（度）


def lav_box(nm):
    a, b = LV[nm]
    return [(a, LV["floor"]), (b, LV["floor"]), (b, LV["top"]), (a, LV["top"])]


def lav_tail():
    """隔壁より後ろの胴体の輪郭を、隔壁の下の端のまわりに LV_BEND 度だけ下げた線（m）"""
    up = [p for p in IL._smooth(I2.S1_UP, per=6) if p[0] >= PR_BULK]
    lo = [p for p in IL._smooth(I2.S1_LO, per=6) if p[0] >= PR_BULK]
    px, pz = PR_BULK, lo[0][1]
    th = math.radians(-LV_BEND)
    return [(px + (x - px) * math.cos(th) - (z - pz) * math.sin(th), pz + (x - px) * math.sin(th) + (z - pz) * math.cos(th))
            for x, z in up + list(reversed(lo))]


def lav_base(st0):
    K, X0, Y0 = PR
    q = side_pts(K, X0, Y0, pr_bulk_pts())
    g = _tail_cut_base(K, X0, Y0) + [F.poly(q, "none", COL["dark"], 9) + F.poly(q, "none", WEB["up"], 5)]
    fa, fb = side_pts(K, X0, Y0, [(PR_X0, LV["floor"]), (PR_BULK, LV["floor"])])
    g.append(F.line(*fa, *fb, COL["seat"], 4))
    for x in (45.0, 46.6, 48.2):                     # 座席の背（模式）
        p = side_pts(K, X0, Y0, [(x, LV["floor"]), (x + 0.5, LV["floor"]), (x + 0.6, LV["floor"] + 1.3), (x + 0.3, LV["floor"] + 1.35)])
        g.append(F.poly(p, COL["seat"], COL["seat_ln"], 2, True))
    for nm in ("coat", "lav"):
        g.append(F.poly(side_pts(K, X0, Y0, lav_box(nm)), "none", COL["ghost"], 3, True))
    return g


def lav_stage(prev, st):
    K, X0, Y0 = PR
    g = []
    if _on(prev, st, "lav"):
        p = side_pts(K, X0, Y0, lav_box("lav"))
        g.append(F.poly(p, COL["cabin"], COL["dark"], 3, True))
        (xa, ya), (xb, yb) = p[0], p[2]
        g.append(F.rect(xa + 6, yb + 14, 22, ya - yb - 20, "#c9a27a", COL["dark"], 2))     # ドア（模式）
        g.append(_ring((xa + xb) / 2, (ya + yb) / 2, 84, COL["mark"]))
    if _on(prev, st, "coat"):
        p = side_pts(K, X0, Y0, lav_box("coat"))
        g.append(F.poly(p, "#3a4652", COL["dark"], 3, True))
        (xa, ya) = p[0]
        for i in range(3):
            for j in range(2 if i < 2 else 1):
                g.append(F.rect(xa + 10 + i * 36, ya - 32 - j * 30, 32, 28, COL["mark"], COL["dark"], 2))
    if _on(prev, st, "bend"):
        g.append(F.poly(side_pts(K, X0, Y0, lav_tail()), "none", COL["red"], 4, False, "12 9"))
    return g


# ══════════════════════════════════════════════════════════
#  見え方の表
# ══════════════════════════════════════════════════════════
VIEWS = dict(
    seats=dict(lab="上から見た操縦室（前が上）", fields=dict(fe=ONOFF, left=("off", "usual", "cop"), right=("off", "cap"), ask=ONOFF,
                                                       cert=ONOFF), base=seats_base, stage=seats_stage),
    xpdr=dict(lab="管制のレーダーと機体", fields=dict(ask=ONOFF, reply=("off", "on", "emg")), base=xpdr_base, stage=xpdr_stage),
    hyd=dict(lab="上から見た機体（機首が上）", fields=dict(surf=ONOFF, pipes=ONOFF, num=ONOFF, ask=ONOFF, cut=ONOFF),
             base=hyd_base, stage=hyd_stage, parts=hyd_parts),
    thrust=dict(lab="推力の矢印と機体の向き", fields=dict(lay=("both", "side"), pwr=("base", "up"), nose=("lvl", "up"), top=ONOFF,
                                                     diff=("off", "ask", "on"), yaw=ONOFF, wave=ONOFF),
                base=thrust_base, stage=thrust_stage, parts=thrust_parts),
    alt=dict(lab="高さの記録の点", fields=dict(span=("cruise", "final"), pts=("off", "early", "all"), m1=ONOFF, m2=ONOFF, rate=ONOFF,
                                          stop=ONOFF), base=alt_base, stage=alt_stage),
    gear=dict(lab="横から見た機体（機首が左）", fields=dict(gear=("up", "down"), flap=("up", "down"), voice=ONOFF), base=gear_base,
              stage=gear_stage, parts=gear_parts),
    radio=dict(lab="無線の相手", fields=dict(link=ONOFF, ask=ONOFF, stay=ONOFF), base=radio_base, stage=radio_stage, parts=radio_parts),
    fix=dict(lab="上から見た方角と距離（北が上）", fields=dict(gps=ONOFF, ray=ONOFF, zoom=ONOFF, pa=ONOFF, pd=ONOFF, heli=ONOFF),
             base=fix_base, stage=fix_stage),
    hoist=dict(lab="夜の山の斜面（横から）", fields=dict(guide=("off", "on", "fail"), hoist=ONOFF, nvg=ONOFF), base=hoist_base,
               stage=hoist_stage),
    press=dict(lab="横から見た尾部の断面（機首が左）", fields=dict(press=ONOFF, push=ONOFF), base=press_base, stage=press_stage),
    bag=dict(lab="尾翼の中の気圧と袋のふくらみ", fields=dict(inner=ONOFF, bags=ONOFF, swell=ONOFF), base=bag_base, stage=bag_stage,
             parts=bag_parts),
    apt=dict(lab="3つの空港（東西の順・間は模式）", fields=dict(pick=ONOFF, why=ONOFF, ok=ONOFF), base=apt_base, stage=apt_stage),
    # 🆕 ⑤b-6：第6〜8章
    fatigue=dict(lab="穴のあいた金属の板", fields=dict(load=("off", "once", "rep"), crack=ONOFF, wire=ONOFF), base=fatigue_base,
                 stage=fatigue_stage, parts=fatigue_parts),
    rows=dict(lab="L18 の継ぎ目の断面（横から）", fields=dict(bars=ONOFF, crack=ONOFF), base=rows_base, stage=rows_stage),
    grow=dict(lab="亀裂の伸び方の比べ", fields=dict(two=ONOFF, one=ONOFF, same=ONOFF), base=grow_base, stage=grow_stage),
    fs=dict(lab="隔壁を後ろから見た図", fields=dict(bay=ONOFF, one=ONOFF), base=fs_base, stage=fs_stage),
    half=dict(lab="横から見た尾部の断面（機首が左）", fields=dict(name=ONOFF, half=ONOFF, join=ONOFF), base=half_base, stage=half_stage),
    edge=dict(lab="板の縁とリベットの穴", fields=dict(good=ONOFF, bad=ONOFF, req=ONOFF), base=edge_base, stage=edge_stage),
    seal=dict(lab="継ぎ目の断面（横から）", fields=dict(seal=ONOFF, eye=ONOFF), base=seal_base, stage=seal_stage),
    rear=dict(lab="隔壁を後ろから見た図", fields=dict(l18=ONOFF, all=ONOFF), base=rear_base, stage=rear_stage),
    clen=dict(lab="リベットの頭と亀裂（後ろから）", fields=dict(crack=ONOFF, len=ONOFF), base=clen_base, stage=clen_stage),
    prob=dict(lab="見つける確率の計算（報告書）", fields=dict(one=ONOFF, many=ONOFF, q=ONOFF), base=prob_base, stage=prob_stage),
    two=dict(lab="2つの場合（後ろから）", fields=dict(pick=ONOFF, ok=ONOFF), base=two_base, stage=two_stage),
    lav=dict(lab="横から見た客室の後ろ（機首が左）", fields=dict(lav=ONOFF, coat=ONOFF, bend=ONOFF), base=lav_base, stage=lav_stage))
START = {v: {k: vs[0] for k, vs in d["fields"].items()} for v, d in VIEWS.items()}
# 頭だけで決める欄（段で変えない）
HEAD_ONLY = dict(thrust=("lay",), alt=("span",))
# 戻さない欄（切れた管は戻らない・下ろした脚とフラップは戻らない・失敗は戻らない・伸びたひびは戻らない）
ORDER = dict(hyd=dict(cut=ONOFF), gear=dict(gear=("up", "down"), flap=("up", "down")), hoist=dict(guide=("off", "on", "fail")),
             xpdr=dict(reply=("off", "on", "emg")), alt=dict(pts=("off", "early", "all")),
             fatigue=dict(load=("off", "once", "rep"), crack=ONOFF))
# 左上の札に「模式」を付けない見え方（記録の値そのもの＝高さの記録の点・報告書の確率の計算）
NOT_SCHEMATIC = ("alt", "prob")


# ══════════════════════════════════════════════════════════
#  札の置き場（x, y, anchor, 幅）と、線を引く先（anchors）
# ══════════════════════════════════════════════════════════
TAG_AT = dict(
    seats=dict(fe=(1270.0, 700.0, "start", 520.0), hours=(1270.0, 330.0, "start", 520.0), usual=(L_X, 470.0, "start", 520.0),
               day=(1270.0, 470.0, "start", 520.0), train=(L_X, 700.0, "start", 560.0), cert=(1270.0, 330.0, "start", 520.0)),
    xpdr=dict(code=(560.0, 700.0, "start", 420.0), emg=(980.0, 420.0, "start", 400.0)),
    hyd=dict(surf=(R_X, 470.0, "start", 520.0), pipes=(L_X, 470.0, "start", 520.0), num=(L_X, 330.0, "start", 520.0),
             tail=(R_X, 720.0, "start", 520.0), cut=(R_X, 720.0, "start", 560.0), fast=(R_X, 600.0, "start", 560.0)),
    thrust=dict(pwr=(F.BX0 + 30.0, 330.0, "start", 760.0), nose=(F.BX0 + 30.0, 790.0, "start", 760.0),
                diff=(1000.0, 800.0, "start", 640.0), wave=(1000.0, 800.0, "start", 640.0), no=(1000.0, 850.0, "start", 820.0),
                clock=(F.BX0 + 30.0, 330.0, "start", 760.0), side_nose=(F.BX0 + 30.0, 790.0, "start", 900.0)),
    # alt の m1・m2 は印の縦の線の右（右の端に近いと左）＝`_stage_svgs` が線の x から決める（y は下の帯＝点の無い高さ）
    # ⚠️ 試し焼き ep20_b5：y 760 だと札の下の小さな字（時刻）が横軸の線（y 790）に乗った＝735
    alt=dict(m1=(0.0, 735.0, "start", 420.0), m2=(0.0, 735.0, "start", 420.0), why=(520.0, 600.0, "start", 660.0),
             rate=(1100.0, 420.0, "start", 520.0), stop=(1370.0, 660.0, "start", 460.0)),
    gear=dict(gear=(560.0, 720.0, "start", 520.0), flap=(1060.0, 720.0, "start", 560.0), voice=(L_X, 330.0, "start", 560.0)),
    radio=dict(link=(L_X, 430.0, "start", 520.0), ask=(1290.0, 430.0, "start", 520.0), stay=(L_X, 560.0, "start", 520.0)),
    fix=dict(gps=(410.0, 430.0, "start", 520.0), dir=(1250.0, 840.0, "start", 300.0), dist=(1300.0, 430.0, "start", 520.0),
             pa=(130.0, 350.0, "start", 560.0), pd=(130.0, 795.0, "start", 560.0), heli=(730.0, 700.0, "start", 480.0)),
    hoist=dict(guide=(L_X, 330.0, "start", 560.0), hoist=(1230.0, 330.0, "start", 560.0), nvg=(1230.0, 440.0, "start", 560.0)),
    press=dict(alt=(L_X, 330.0, "start", 560.0), cabin=(L_X, 820.0, "start", 560.0), bulk=(1330.0, 820.0, "start", 480.0),
               push=(1330.0, 330.0, "start", 480.0)),
    bag=dict(inner=(F.BX0 + 30.0, 330.0, "start", 700.0), sea=(880.0, 330.0, "start", 400.0), mt=(1360.0, 330.0, "start", 440.0)),
    apt=dict(pick=(1060.0, 410.0, "start", 360.0), ok=(1060.0, 300.0, "start", 340.0), why=(L_X, 800.0, "start", 640.0)),
    # 🆕 ⑤b-6
    fatigue=dict(once=(800.0, 330.0, "start", 400.0), crack=(1230.0, 690.0, "start", 560.0), wire=(1390.0, 560.0, "start", 440.0)),
    rows=dict(str=(F.BX0 + 30.0, 812.0, "start", 300.0), crack=(1480.0, 430.0, "start", 340.0)),
    grow=dict(two=(1580.0, 440.0, "start", 240.0), one=(1150.0, 340.0, "start", 300.0), same=(GR["x0"] + 20.0, GR_YT - 20.0, "start", 360.0)),
    fs=dict(bay=(1270.0, 420.0, "start", 560.0), one=(F.BX0 + 30.0, 800.0, "start", 560.0)),
    half=dict(name=(L_X, 380.0, "start", 560.0), up=(1150.0, 380.0, "start", 600.0), lo=(1150.0, 800.0, "start", 600.0),
              join=(L_X, 800.0, "start", 560.0)),
    edge=dict(good=(700.0, 410.0, "start", 440.0), bad=(1250.0, 410.0, "start", 440.0), req=(1290.0, 830.0, "start", 520.0)),
    seal=dict(seal=(1000.0, 360.0, "start", 600.0), eye=(1000.0, 780.0, "start", 640.0)),
    rear=dict(l18=(F.BX0 + 30.0, 330.0, "start", 300.0), all=(1290.0, 760.0, "start", 520.0), margin=(1290.0, 330.0, "start", 520.0),
              none=(1290.0, 430.0, "start", 520.0), corr=(F.BX0 + 30.0, 830.0, "start", 560.0)),
    clen=dict(date=(F.BX0 + 30.0, 320.0, "start", 600.0), len=(1230.0, 470.0, "start", 560.0), vis=(1230.0, 640.0, "start", 560.0)),
    prob=dict(title=(F.BX0 + 30.0, 320.0, "start", 640.0), asm=(F.BX0 + 30.0, 320.0, "start", 640.0), q=(1350.0, 600.0, "start", 440.0)),
    two=dict(pick=(F.BX0 + 30.0, 840.0, "start", 600.0), ok=(770.0, 410.0, "start", 300.0)),
    lav=dict(lav=(1150.0, 380.0, "start", 640.0), coat=(L_X, 380.0, "start", 560.0), bend=(1150.0, 800.0, "start", 640.0)))


def anchors(view, st):
    if view == "seats":
        return dict(fe=SE_FE, left=(SE_SEAT["left"][0] - 62, SE_SEAT["left"][1]), right=(SE_SEAT["right"][0] + 62, SE_SEAT["right"][1]),
                    right_top=(SE_SEAT["right"][0], SE_SEAT["right"][1] - 67), fe_r=(SE_P4[0] + SE_P4[2], 700.0))
    if view == "xpdr":
        (x, y, w, h) = xp_code_boxes()[0]
        return dict(code=(x + w / 2, y + h + 6), reply=((XP_FROM[0] + XP_TO[0]) / 2 + 120, (XP_FROM[1] + XP_TO[1]) / 2 - 30))
    if view == "hyd":
        s = top_surfaces(HY)
        ail = s["ail_out_r"]
        main1, br1 = hyd_path(1)
        fr, _ = _split_at(hyd_path(4)[0], HY_CUT)
        return dict(ail=(sum(p[0] for p in ail) / 4, sum(p[1] for p in ail) / 4), pipe=HY.p(*br1[-1]),
                    tail=(HY.p(64.0, 0)[0] + 62, HY.p(64.0, 0)[1]), cut=HY.p(*fr[-1]), eng1=HY.p(TOP_ENG_X[1][0] - 2.6, ENG_NO[1]))
    if view == "thrust":
        K, X0, Y0, piv = th_side_geo(st)
        return dict(eng=(X0 + (I2.S1_ENG[0][0] - 6.0) * K, Y0 + 3.55 * K), nose=(X0 + 1.0 * K, Y0 - 1.5 * K),
                    cockpit=(X0 + 4.5 * K, Y0 - 3.4 * K), top_nose=TH_TOP.p(-1.0, 0.0), wave=(TH_WAVE[0] - 44, (TH_WAVE[1] + TH_WAVE[2]) / 2),
                    top_eng=TH_TOP.p(TOP_ENG_X[1][0] - 3.0, -TOP_ENG_Y[1]))
    if view == "alt":
        span = st["span"]
        out = {m: (al_xy(span, AL_MARK[span][m], 0)[0], AL["y0"] + 40) for m in ("m1", "m2")}
        t, ft = AL_PTS[span][-1]
        out["last"] = al_xy(span, t, ft * FT)
        (ta, fa), (tb, fb) = al_rate_line(span) if span == "final" else (("18:55:57", 0), ("18:55:57", 0))
        if span == "final":
            a, b = al_xy(span, ta, fa * FT), al_xy(span, tb, fb * FT)
            out["rate"] = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        return out
    if view == "gear":
        K, X0, Y0 = GE
        return dict(main=side_pts(K, X0, Y0, [(GE_MAIN_X[0], -3.35 - GE_LEG - 0.6)])[0],
                    flap=side_pts(K, X0, Y0, [(36.4, -3.6)])[0], cockpit=side_pts(K, X0, Y0, [(4.0, 4.6)])[0])
    if view == "radio":
        a, b = ra_link("left")
        c, d = ra_link("right")
        return dict(link=((a[0] + b[0]) / 2 - 10, (a[1] + b[1]) / 2), ask=((c[0] + d[0]) / 2 + 10, (c[1] + d[1]) / 2))
    if view == "fix":
        sx, sy = FX["st"]
        ex, ey = fx_end()
        x0, y0, x1, y1 = FX_ZOOM
        fan = fx_fan(*FX_HELI)
        return dict(arc=_arc_pts(sx, sy, 120, 360, FX["brg"])[8], ray=((sx + ex) / 2, (sy + ey) / 2),
                    pfan=((x0 + x1) / 2 - 200, (y0 + y1) / 2 + 30), heli=(max(p[0] for p in fan), (y0 + y1) / 2 + 30),
                    gps=(380.0, 420.0))
    if view == "hoist":
        x, y = HO["heli"]
        return dict(guide=HO["guide_to"], land=(HO["land"][0] + 90, HO["land"][1] - 110), heli=(x - 22, y - 20))
    if view == "press":
        K, X0, Y0 = PR
        return dict(cabin=side_pts(K, X0, Y0, [(50.0, -1.5)])[0], bulk=side_pts(K, X0, Y0, [(PR_BULK + 1.1, -2.0)])[0],
                    push=side_pts(K, X0, Y0, [(PR_BULK - 1.0, 2.0)])[0])
    if view == "bag":
        return dict(sea=(BG_SEA[0], BG_SEA[1] - 90), mt=(BG_MT[0], BG_MT[1] - 110))
    if view == "apt":
        x = AP_PTS["haneda"][0]
        return dict(haneda=(x - 42, AP["y"] - 10), ok=(x - 34, AP["y"] - 126), why=(x - 172, AP["y"] + 160))
    # 🆕 ⑤b-6
    if view == "fatigue":
        (tx, ty) = fa_crack("r")[1]
        return dict(tip=(tx + 8, ty + 10), wire=(FA_WIRE[1][0], FA_WIRE[1][1] + 14), arrow=(FA_HOLE[0] + 12, FA_PLATE[1] - 50))
    if view == "rows":
        return dict(crack=(RW_CX["b"] + RW_T + 8, RW_ROWS["b"][0] + 17), bar=(RW_CX["a"] - RW_BAR[1] / 2 - 8, RW_BAR[0]))
    if view == "grow":
        return dict(two=gr_line("two")[1], one=gr_line("one")[1])
    if view == "fs":
        cx, cy = FS_C
        s = I2.S6F_STRAPS
        return dict(bay=(cx + FS_R * sum(FS_BAY_R) / 2, cy - 12), one=(cx - FS_R * (s[FS_ONE[0]] + s[FS_ONE[1]]) / 2, cy + 12))
    if view == "half":
        K, X0, Y0 = PR

        def mid(pts):
            q = side_pts(K, X0, Y0, pts)
            return (sum(p[0] for p in q) / len(q), sum(p[1] for p in q) / len(q))
        return dict(dome=side_pts(K, X0, Y0, [(PR_BULK + 0.3, PR_Z[0] - 0.4)])[0], up=mid(hf_lens("up")), lo=mid(hf_lens("lo")),
                    join=side_pts(K, X0, Y0, [(PR_BULK + 1.25, sum(PR_Z) / 2)])[0])
    if view == "edge":
        ye = ED_PLATE[1]
        return dict(good=(ED_GOOD[0] + 58, (ED_GOOD[1] - ED_R + ye) / 2), bad=(ED_BAD[0], ED_BAD[1] - ED_R - 4),
                    req=(ED_BAD[0] + 78, ye + ED_REQ / 2))
    if view == "seal":
        tri = sl_beads()[0][2]
        return dict(bead=(tri[0][0] + 6, tri[0][1] + 8), eye=(SL_EYE[0] - 20, SL_EYE[1] + 30))
    if view == "rear":
        cx, cy = RE_C
        return dict(l18=(cx - RE_R * 0.6, cy - 8), joint=(cx - 30, cy), eye=(RE_EYE[0], RE_EYE[1] + 30),
                    face=(cx + RE_R * 0.5, cy - RE_R * 0.5))
    if view == "clen":
        cx, cy = CL_C
        hd, L = cl_head(), CL_HOLE + CL_LEN * CL_MM
        return dict(len=(cx + (CL_HOLE + L) / 2, cy - 72), vis=(cx + (hd + L) / 2, cy + 72), crack=(cx + L, cy),
                    lcrack=(cx - L + 10, cy - 8))
    if view == "prob":
        return dict(one=(pb_x(PB_ONE) + 6, PB_ROW["one"]), many=(pb_x(PB_MANY[1]) + 6, PB_ROW["many"]))
    if view == "two":
        cx, cy = TW_C["a"]
        return dict(pick=(cx, cy + TW_R + 10), ok=tw_check()[1])
    if view == "lav":
        K, X0, Y0 = PR

        def top_mid(nm):
            a, b = LV[nm]
            return side_pts(K, X0, Y0, [((a + b) / 2, LV["top"])])[0]
        return dict(lav=top_mid("lav"), coat=top_mid("coat"), bend=side_pts(K, X0, Y0, [lav_tail()[-8]])[0])
    return {}


def parts_of(view, st):
    fn = VIEWS[view].get("parts")
    return fn(st) if fn else []


def _states(view, start, steps):
    fields = VIEWS[view]["fields"]
    cur = dict(START[view], **(start or {}))
    out = []
    for i, st in enumerate([dict(state={})] + list(steps)):
        new = st.get("state") or {}
        for f_ in HEAD_ONLY.get(view, ()):
            if i > 0 and f_ in new:
                raise ValueError(f"m20：{f_} は頭（start）だけで決める")
        cur = dict(cur, **new)
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m20：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m20：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    for f_, seq in ORDER.get(view, {}).items():
        if f_ in fields:
            idx = [seq.index(s[f_]) for s in out]
            if any(b < a for a, b in zip(idx, idx[1:])):
                raise ValueError(f"m20：{f_} は戻さない（{' → '.join(seq)}）")
    return out[0], out[1:]


def stage_art(view, prev, st):
    return VIEWS[view]["stage"](prev, st)


def _base(view, st0):
    """基図＋頭の状態の層（頭で on にした欄は基図に描く＝前のカットの続き）"""
    pre = dict(START[view], **{k: st0[k] for k in HEAD_ONLY.get(view, ())})
    return VIEWS[view]["base"](st0) + stage_art(view, pre, st0)


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
            if view == "alt" and isinstance(at, str) and at in ("m1", "m2"):
                mx = an[at][0]
                x, anchor = (mx + 14, "start") if mx < 1250 else (mx - 14, "end")
            c = tg.get("cap", cap)
            if tg.get("to"):
                tx, ty = an[tg["to"]] if isinstance(tg["to"], str) else tg["to"]
                below_d = tg.get("d") and ty > y + round(c * 0.95)
                sy = y - round(c * 0.9) if ty < y - c else y + 8 + (round(c * 0.95) if below_d else 0)
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
    k0 = sh["keys"][0]
    if sh["type"] == "circle":
        return F.circ(sh["c"][0] + float(k0.get("dx", 0) or 0), sh["c"][1] + float(k0.get("dy", 0) or 0), sh["r"],
                      k0.get("fill", sh.get("fill", "none")), k0.get("stroke", sh.get("stroke")), sh.get("w"))
    pts = F.mech_pts(sh, k0)
    if sh["type"] == "poly":
        return F.poly(pts, k0.get("fill", sh.get("fill", "none")), k0.get("stroke", sh.get("stroke")), sh.get("w") or None, close=True,
                      op=(round(a, 2) if a < 0.99 else None))
    return F.poly(pts, "none", k0.get("stroke", sh.get("stroke")), sh.get("w"), op=(round(a, 2) if a < 0.99 else None))


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def m20(view, steps, start=None, rel=(), note="", src=""):
    """20本目の模式図。view は VIEWS の24種（⑤b-5 の12＋⑤b-6 の12）。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m20：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if "模式" not in note:
        raise ValueError("m20：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
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
            dl = 0.0 if i == 0 else float(steps[i - 1].get("delay", 1.0 if i == 1 else F.MECH_DELAY)) + float(p0.get("lag", 0.0))
            keys.append(dict(stage=max(0, i - 1), delay=dl, **kk))
        sh = {f_: p0[f_] for f_ in p0 if f_ not in ("alpha", "dx", "dy", "rot", "lag")}
        sh["keys"] = keys
        moving = any({f_: kk.get(f_) for f_ in KEY_FIELDS} != {f_: keys[0].get(f_) for f_ in KEY_FIELDS} for kk in keys[1:])
        sh["anim"] = bool(moving)
        shapes.append(sh)
        if moving:
            anim.append(sh)
    g = _base(view, st0)
    for sh in shapes:
        if not sh["anim"]:
            g.append(_static_part(sh))
    # 高さの線（alt）は記録の点そのもの＝左上の札に「模式」を付けない（印の線と矢印が模式＝note で断る）。🆕 ⑤b-6：確率の計算（prob）も
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, VIEWS[view]["lab"] + ("" if view in NOT_SCHEMATIC else "・模式"), 1000, cap=28,
                      col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, st0, states)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="m20", view=view, start=st0, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M20）
# ══════════════════════════════════════════════════════════
def geo_of(view, start, states):
    allst = [start] + list(states)
    last = allst[-1]

    def ever(f, v="on"):
        return any(s.get(f) == v for s in allst)
    out = dict(view=view)
    if view == "seats":
        out["names"] = dict(left=sorted({SE_NAMES["left"][s["left"]] for s in allst if s["left"] != "off"}),
                            right=sorted({SE_NAMES["right"][s["right"]] for s in allst if s["right"] != "off"}))
        out["fe"] = list(SE_FE)
        out["pilots"] = [list(SE_SEAT["left"]), list(SE_SEAT["right"])]
        out["p4_x"] = SE_P4[0]
        out["day"] = [(s["left"], s["right"]) for s in allst]
    elif view == "xpdr":
        out["boxes"] = len(xp_code_boxes()) if ever("reply") or ever("reply", "emg") else 0
        out["emg_before_reply"] = any(s["reply"] == "emg" and i == 0 for i, s in enumerate(allst))
    elif view == "hyd":
        out["pipes"] = 4 if ever("pipes") else 0
        out["eng"] = {no: HY.p(sum(TOP_ENG_X[0] if abs(ENG_NO[no]) < 15 else TOP_ENG_X[1]) / 2, ENG_NO[no]) for no in (1, 2, 3, 4)}
        out["k"], out["cx"], out["y0"] = HY.K, HY.CX, HY.Y0
        out["starts"] = {no: hyd_path(no)[0][0] for no in (1, 2, 3, 4)}
        out["cut_x"] = HY_CUT if ever("cut") else None
        out["tail_x"] = max(p[0] for p in hyd_path(1)[0])
        out["nums"] = [no for no in (1, 2, 3, 4)] if ever("num") else []
        out["num_x"] = {no: HY.p(0, ENG_NO[no])[0] for no in (1, 2, 3, 4)}
    elif view == "thrust":
        out["side_eng"] = [list(e) for e in I2.S1_ENG]
        out["cg_x"] = CG_X
        out["top_eng_y"] = {no: ENG_NO[no] for no in (1, 2, 3, 4)}
        out["pitch"] = [(s["pwr"], s["nose"]) for s in allst]
        out["yaw"] = [(s["diff"], s["yaw"], {no: th_top_len(s, no) for no in (1, 2, 3, 4)}, TH_YAW if s["yaw"] == "on" else 0.0)
                      for s in allst]
        out["rot_nose_up"] = TH_PITCH
        # 画素で：機首を上げた段の機首の先と、真ん中（pivot）の高さの差（正＝機首が上）
        K, X0, Y0, piv = th_side_geo(start)
        nose_up = [p for p in thrust_parts(dict(start, nose="up")) if p["id"] == "s_body"][0]
        q = F.mech_pts(nose_up, nose_up)
        out["nose_dy"] = piv[1] - min(q, key=lambda p: p[0])[1]
        if start["lay"] == "both":
            yawed = [p for p in thrust_parts(dict(start, yaw="on", top="on")) if p["id"] == "t_body"][0]
            q2 = F.mech_pts(yawed, yawed)
            out["nose_dx"] = min(q2, key=lambda p: p[1])[0] - TH_TOP.CX
    elif view == "alt":
        span = start["span"]
        sp = AL_SPAN[span]
        out["span"] = span
        # 目盛りの画素（x＝時刻・y＝高度）と、描いた点の画素
        out["xt"] = [(h if h.count(":") == 2 else h + ":00", al_xy(span, h if h.count(":") == 2 else h + ":00", 0)[0]) for h in sp["xt"]]
        out["yt"] = [(v, al_xy(span, sp["t0"], v)[1]) for v in sp["yt"]]
        out["dots"] = [al_xy(span, t, ft * FT) for t, ft in al_points(span, last["pts"])]
        out["marks"] = {m: al_xy(span, AL_MARK[span][m], 0)[0] for m in ("m1", "m2") if ever(m)}
        if span == "final" and ever("rate"):
            (ta, fa), (tb, fb) = al_rate_line(span)
            out["rate"] = [al_xy(span, ta, fa * FT), al_xy(span, tb, fb * FT)]
        out["order"] = [s["pts"] for s in allst]
    elif view == "gear":
        out["seq"] = [(s["gear"], s["flap"]) for s in allst]
        out["main_x"] = list(GE_MAIN_X)
        out["nose_x"] = GE_NOSE_X
        out["lag"] = GE_FLAP_LAG
    elif view == "radio":
        out["names"] = dict(RA_NAMES)
        out["seq"] = [(s["link"], s["ask"], s["stay"]) for s in allst]
    elif view == "fix":
        sx, sy = FX["st"]
        ex, ey = fx_end()
        out["brg"] = (math.degrees(math.atan2(ex - sx, -(ey - sy))) + 360.0) % 360.0
        out["nm"] = math.hypot(ex - sx, ey - sy) / FX["k"]
        out["seq"] = [dict(s) for s in allst]

        def fan_geo(w, d):
            pts = fx_fan(w, d)
            n = len(pts) // 2
            x0, y0, x1, y1 = FX_ZOOM
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 30
            R = FX["nm"]
            # 外の弧の両端の角度・内と外の弧の半径（マイル）を画素から戻す
            def pol(p):
                X, Y = (p[0] - cx) / FX_ZK, R - (p[1] - cy) / FX_ZK
                return math.degrees(math.atan2(X, Y)), math.hypot(X, Y)
            a0, r0 = pol(pts[0])
            a1, _ = pol(pts[n - 1])
            _, r1 = pol(pts[n])
            return dict(width=a1 - a0, depth=r0 - r1)
        out["plane"] = fan_geo(*FX_PLANE) if ever("pd") else None
        out["heli"] = fan_geo(*FX_HELI) if ever("heli") else None
    elif view == "hoist":
        out["seq"] = [(s["guide"], s["hoist"], s["nvg"]) for s in allst]
        out["people"] = 0
    elif view == "press":
        out["bulk_x"] = PR_BULK
        out["arrows"] = [((PR_BULK - 4.2, z), (PR_BULK - 0.5, z)) for z in PR_ARROWS] if ever("push") else []
        out["seq"] = [(s["press"], s["push"]) for s in allst]
    elif view == "bag":
        def area(P):
            return abs(sum(P[i][0] * P[i - 1][1] - P[i - 1][0] * P[i][1] for i in range(len(P)))) / 2.0
        k = BG_SWELL if ever("swell") else 1.0
        out["ratio"] = area(bag_pts(*BG_MT, k)) / area(bag_pts(*BG_SEA, 1.0)) if ever("bags") else None
        out["seq"] = [(s["inner"], s["bags"], s["swell"]) for s in allst]
    elif view == "apt":
        out["order"] = [nm for k, (x, nm, lon) in sorted(AP_PTS.items(), key=lambda kv: kv[1][0])]
        out["lons"] = {nm: lon for k, (x, nm, lon) in AP_PTS.items()}
        out["why"] = list(AP_WHY) if ever("why") else []
        out["picked"] = AP_PTS["haneda"][1] if ever("pick") else None
    # 🆕 ⑤b-6（描く関数と同じ式）
    elif view == "fatigue":
        out["hole"] = list(FA_HOLE)
        out["load_deg"] = FA_LOAD
        out["cracks"] = {s: fa_crack(s) for s in ("r", "l")} if ever("crack") else {}
    elif view == "rows":
        out["rows"] = {k: len(v) for k, v in RW_ROWS.items()}
        out["lap"] = {k: list(v) for k, v in RW_LAP.items()}
        out["row_y"] = {k: list(v) for k, v in RW_ROWS.items()}
        out["bars"] = {k: RW_BAR[1] * RW_STR[k] for k in RW_CX} if ever("bars") else None
    elif view == "grow":
        out["x0"], out["y0"] = GR["x0"], GR["y0"]
        out["lines"] = {k: gr_line(k) for k in ("two", "one") if ever(k)}
        out["hits"] = {k: gr_hit(k) for k in ("two", "one")} if ever("same") else {}
    elif view == "fs":
        out["c"], out["R"], out["straps"] = list(FS_C), FS_R, list(I2.S6F_STRAPS)
        out["bay"] = list(FS_BAY_R) if ever("bay") else None
        if ever("one"):
            r0, r1 = (FS_R * I2.S6F_STRAPS[i] for i in FS_ONE)
            out["one"] = [(FS_C[0] - r0, FS_C[1]), (FS_C[0] - r1, FS_C[1])]
        else:
            out["one"] = None
    elif view == "half":
        out["new"] = HF_NEW if ever("half") else None
        out["lens_z"] = {w: (min(p[1] for p in hf_lens(w)), max(p[1] for p in hf_lens(w))) for w in ("up", "lo")}
    elif view == "edge":
        out["m"] = dict(good=ed_margin(ED_GOOD), bad=ed_margin(ED_BAD), req=ED_REQ)
        out["seq"] = [(s["good"], s["bad"], s["req"]) for s in allst]
    elif view == "seal":
        k, cx, cy, w, xs, L = sl_geo()
        out["ends"] = dict(upper=cy + L["upper"][1] * k, splice=cy + L["splice"][1] * k, lower=cy + L["lower"][0] * k)
        out["beads"] = [(nm, list(c)) for nm, c, tri in sl_beads()] if ever("seal") else []
        out["eye_x"] = SL_EYE[0] if ever("eye") else None
        out["stack_x1"] = xs["upper"] + w / 2
    elif view == "rear":
        out["R"] = RE_R
        out["all_r"] = RE_R * RE_ALL if ever("all") else None
    elif view == "clen":
        hd, L = cl_head(), CL_HOLE + CL_LEN * CL_MM
        out["sides"] = {s: dict(total=L - CL_HOLE, vis=L - hd) for s in (-1, 1)} if ever("crack") else {}
    elif view == "prob":
        out["xt"] = [(v, pb_x(v)) for v in PB_TICKS]
        out["one"] = pb_x(PB_ONE) if ever("one") else None
        out["many"] = [pb_x(v) for v in PB_MANY] if ever("many") else None
    elif view == "two":
        out["cracks"] = dict(TW_CRACKS)
        out["ok_on"] = "a" if ever("ok") or ever("pick") else None
    elif view == "lav":
        out["lav"], out["coat"], out["bulk"] = list(LV["lav"]), list(LV["coat"]), PR_BULK
    return out
