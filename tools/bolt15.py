# -*- coding: utf-8 -*-
"""bolt15.py — 15本目「ねじ・ナット・フラッター」の動く模式図（2026-09-30 新設・15本目 ⑤b-4）。

■ 何か（Vault `Projects/事故検証-15本目-映像方針-絵コンテ-20260926.md` §4 の【ねじ】）
  `tools/tail15.py`・`tools/mod15.py` と同じ「基図＋段の鍵で動く部品」の図解（案C の絵ではない）。形は**模式**。
  章の色の線と面・左上に見る向き・左下に「模式」と出典（§5b-10）。人は描かない（整備の仲間・検査員も）。

■ 見え方（view）。🔴 見る向きの札を左上に必ず出す（§5b-80）
  nut    … ちょうつがいの断面（板を金具にとめるねじ1本とナット）。ねじの頭 → 板 → 金具 → 押し込んだナット（金属のねじ山の下に
            繊維の詰め物）。🔴 ねじの長さの比＝#40 の実測（左の板の真ん中：決まり NAS221-19＝頭の下 1.219インチ・
            実際 0.96インチ＝先がナットの端とそろう）。c709・c712・c720
  spring … 板の支え（ねじ・リンク）を「ばね」で見せた横から見た断面（機首が右）。ゆるむ → 支えのかたさが落ちる → 震え。
            揺れと空気の力がかみ合う（揺れの向きと力の向きがそろう）・続く震えと大きくなる震え。c715・c716
  chart  … 速さ（横）と支えのかたさ（縦）の図。フラッターが起きやすい所＝速いほど・かたさが落ちるほど（目盛りの数は無い）。c717

■ 記録（AAB＝NTSB AAB-12/01。頁は PDF の頁。#40＝ドケットの材料試験 12-029）
  p31 板ごとに3か所のちょうつがい・1か所にねじ1本／ねじは全部ゆるみ、ナットの手ごたえはほとんど無い／繊維の詰め物は
      ねじ山をほとんど締めつけず、どれも古く使い回しの跡（注37＝締めつけの力が決まりに届かない繊維やナイロンの詰め物の
      ナットは使い回さない＝AC 43.13-1B）／板と金具の合わせ目は塗装がはげて地の金属＝ゆるんだねじでこすれ合った跡／
      左の板の外側のねじは少し短く、真ん中のねじは決まりよりかなり短く先がナットの端とそろう
  p32 図14（左の板の外側のナット・赤い詰め物）・内側のねじはナットの面で折れ、ねじ山とナットのあいだにすき間・逆向きの曲げの疲労
  p40 古いナット → ねじのゆるみと1本の疲労の割れ → 板が動き、支えのかたさが落ちた／フラッター＝機体の揺れと空気の力が
      かみ合って速く震える・支えの揺れを抑える力が足りないと大きくなり続ける／うるさい震えから一瞬で壊れるまで／
      速さと支えのかたさの2つで決まる＝速いほど・かたさが落ちるほど起きやすい
  p41 ねじは事故の4日前の技術検査の指摘（右の板のねじ）で締め直された可能性が高い・そのあと事故の飛行を含めて3回だけ
  #40 p2（NAS221-19 は頭の下 1.219インチ・ナット MS51866 は金具に押し込んで留める）・p5〜p6（真ん中のねじ 0.96インチ・先が
      ナットの端とそろう・手で回るほど手ごたえが無い）

■ SPEC の書き方（`tail`・`mod` と同じ）
  fig=("bolt", dict(view="nut"|"spring"|"chart", start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…)), …],
                    rel=[dict(t="3回", src="AAB p41")], note="模式…", src="…"))
■ 門番 `check_mech`（judge_bolt）＝①状態の筋（記録）②本番の関数が置いた部品の画素 ③札の数
"""
from __future__ import annotations

import math

import jiko_style as J
import titan_fig as F
import tail15 as T
import mod15 as M

VIEWS = dict(nut=dict(lab="ちょうつがいの断面（ねじとナット・模式）"), spring=dict(lab="板の支えと震え（横から見た断面・模式）"),
             chart=dict(lab="速さと支えのかたさ（模式・目盛りの数は無い）"))
ONOFF = ("off", "on")
FIELDS = dict(
    nut=dict(screw=("spec", "short"), ghost=ONOFF, insert=("new", "old"), clamp=ONOFF, loose=ONOFF, paint=ONOFF, tip=ONOFF,
             tight=ONOFF, flights=("0", "1", "2", "3")),
    spring=dict(screw=("tight", "loose"), stiff=("high", "low"), wobble=ONOFF, shake=ONOFF, air=ONOFF, graph=ONOFF),
    chart=dict(region=ONOFF, arrows=ONOFF, acc=ONOFF, ring=ONOFF),
)
START = dict(nut=dict(screw="spec", ghost="off", insert="new", clamp="off", loose="off", paint="off", tip="off", tight="off",
                      flights="0"),
             spring=dict(screw="tight", stiff="high", wobble="off", shake="off", air="off", graph="off"),
             chart=dict(region="off", arrows="off", acc="off", ring="off"))

# ── nut の置き場（画素・模式）。ねじの軸 SX・頭の下 HEAD_B・ナットの端 NUT_END ──
SX = 500.0
HEAD_T, HEAD_B = 352.0, 392.0
TAB = (240.0, HEAD_B, 760.0, 440.0)            # 板（x0, y0, x1, y1）
FIT = (370.0, 440.0, 630.0, 560.0)             # ちょうつがいの金具
NUT = (432.0, 520.0, 568.0, 650.0)             # 押し込んだナット（金具の下に出る）
INS_Y = 612.0                                  # 繊維の詰め物の上の端（ナットの端の側＝下）
NUT_END = NUT[3]
SHANK_R = 20.0
SPEC_IN, SHORT_IN = 1.219, 0.96                # #40 p2・p6（頭の下の長さ・インチ）
L_SHORT = NUT_END - HEAD_B                     # 実際のねじ＝先がナットの端とそろう（AAB p31・#40 p5）
L_SPEC = L_SHORT * SPEC_IN / SHORT_IN          # 決まりのねじ（比は実測の値）
TIP = dict(spec=HEAD_B + L_SPEC, short=HEAD_B + L_SHORT)
INS_GAP = dict(new=0.0, old=7.0)               # 詰め物とねじのすき間（old＝締めつけない）
FLY_X = (1230.0, 1410.0, 1590.0)               # 締め直しのあとの飛行の印（3回＝AAB p41）
FLY_Y = 700.0


def _shank(tip):
    x0, x1 = SX - SHANK_R, SX + SHANK_R
    return [[x0, HEAD_B], [x1, HEAD_B], [x1, tip - 6.0], [x1 - 6.0, tip], [x0 + 6.0, tip], [x0, tip - 6.0]]


def _threads(tip):
    """ねじ山（軸を斜めに行き来する線）。点の数は決まりの長さで固定＝短いねじは先から下の点を先に寄せる（鍵の点の数をそろえる）。"""
    out = []
    y, k = 452.0, 0
    while y < TIP["spec"] - 8.0:
        if y < tip - 8.0:
            out.append([SX - SHANK_R if k % 2 == 0 else SX + SHANK_R, y - (0.0 if k % 2 == 0 else 6.0)])
        else:
            out.append([SX, tip - 10.0])          # 先より下の点は1点に寄せる（線の団子にしない）
        y += 6.0
        k += 1
    return out


def _rect(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def _plane(cx, cy, k=7.0):
    """飛行の印＝上から見た事故機（図2 から測った輪郭・機首が右）を小さく。"""
    return [[cx + (x + 4.6) * k, cy - y * k] for x, y in M.SH["top"]["mod"]]


def _head():
    return [[SX - 96.0, HEAD_B], [SX - 96.0, 372.0], [SX - 80.0, 358.0], [SX - 40.0, HEAD_T], [SX + 40.0, HEAD_T],
            [SX + 80.0, 358.0], [SX + 96.0, 372.0], [SX + 96.0, HEAD_B]]


def _arc_e(cx, cy, rx, ry, a0, a1, n=16):
    return [[cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))]
            for i in range(n + 1)]


# ── spring の置き場（画素・模式）。機首が右＝板は昇降舵の後ろ（左）。角度は画面で時計回りが正＝左へ伸びる板は正で後ろの縁が上 ──
ELEV_S = [[1510.0, 500.0], [1494.0, 470.0], [1200.0, 486.0], [906.0, 506.0], [906.0, 554.0], [1200.0, 574.0], [1494.0, 590.0],
          [1510.0, 560.0], [1496.0, 530.0]]
HINGE_S = (900.0, 530.0)
TAB_S = [[894.0, 510.0], [740.0, 518.0], [560.0, 526.0], [560.0, 534.0], [740.0, 542.0], [866.0, 548.0], [866.0, 612.0],
         [884.0, 612.0], [886.0, 550.0], [894.0, 550.0]]
HORN_TIP = (875.0, 612.0)
ANCHOR_S = (1060.0, 612.0)                      # 昇降舵の下の受け（ばねのもう一方の端）
TE_S = (560.0, 530.0)
GHOST_DEG = dict(wobble=5.0, shake=13.0)        # 板の揺れの幅（模式）
G_ROW = dict(steady=720.0, grow=812.0)          # 震えの続き方の2本（縦の真ん中）
G_X = (1400.0, 1790.0)


def _spring(n, amp):
    return M._zig(HORN_TIP[0], HORN_TIP[1], ANCHOR_S[0], ANCHOR_S[1], n, amp)


def _wave(row):
    """時間とともに：steady＝同じ幅で続く／grow＝どんどん大きくなる（p40）。"""
    cy = G_ROW[row]
    x0, x1 = G_X
    out = []
    n = 72
    for i in range(n + 1):
        u = i / n
        a = 20.0 if row == "steady" else 4.0 * math.exp(math.log(11.0) * u)     # 4 → 44画素（11倍）
        out.append([x0 + (x1 - x0) * u, cy - a * math.sin(u * 2 * math.pi * 9)])
    return out


# ── chart の置き場（画素）。u＝速さ 0〜1・v＝支えのかたさ 0〜1（数の目盛りは無い＝模式）──
C_O, C_W, C_H = (340.0, 820.0), 800.0, 500.0


def C(u, v):
    return [C_O[0] + C_W * u, C_O[1] - C_H * v]


def v_need(u):
    """フラッターを起こさないのに要る支えのかたさ（速さとともに上がる＝p40）。模式の曲線。"""
    return 0.12 + 0.72 * u ** 1.7


REGION = [C(i / 40, v_need(i / 40)) for i in range(41)] + [C(1.0, 0.0), C(0.0, 0.0)]
ACC_UV = (0.90, 0.22)                           # 事故機＝レースの速さ・ゆるんだねじ（かたさが落ちた）
# ⚠️ 下見：2本を同じ所で交えると「＋」の印に見えた＝交わらない位置（かたさの矢印は左・速さの矢印はその右）
ARROW_SPEED = (C(0.32, 0.42), C(0.86, 0.42))    # 速いほど（右へ）
ARROW_STIFF = (C(0.22, 0.90), C(0.22, 0.05))    # かたさが落ちるほど（下へ）


def _on(v):
    return 1.0 if v else 0.0


def parts_of(view, st):
    """状態 → 部品。🔴 門番（check_mech.judge_bolt）もこの関数を呼ぶ＝描く側と同じ幾何。"""
    _P = T._P
    if view == "nut":
        tip = TIP[st["screw"]]
        gap = INS_GAP[st["insert"]]
        old = st["insert"] == "old"
        ins_col = "ALERT" if old else "DOC"       # 古い詰め物＝欠陥の赤（ALERT_DIM は第7章の赤銅の地に沈む）・新品＝繊維の色
        nf = int(st["flights"])
        out = [
            _P("tab", "poly", _rect(*TAB), fill="BG2", stroke="INK_W", w=3),
            _P("fit", "poly", _rect(*FIT), fill="BG2", stroke="INK_W", w=3),
            _P("nut", "poly", _rect(*NUT), fill="BG", stroke="INK_W", w=3),
            _P("ins_l", "poly", _rect(NUT[0] + 4.0, INS_Y, SX - SHANK_R - gap, NUT_END - 3.0), fill=ins_col, stroke=ins_col, w=1),
            _P("ins_r", "poly", _rect(SX + SHANK_R + gap, INS_Y, NUT[2] - 4.0, NUT_END - 3.0), fill=ins_col, stroke=ins_col, w=1),
            _P("shank", "poly", _shank(tip), fill="#b9c3c9", stroke="INK_W", w=2),
            _P("thread", "line", _threads(tip), stroke="#6d7a82", w=2),
            _P("head", "poly", _head(), fill="#b9c3c9", stroke="INK_W", w=3),
            _P("ghost", "poly", _shank(TIP["spec"])[2:4] + [[SX - SHANK_R + 6.0, TIP["spec"]], [SX - SHANK_R, TIP["spec"] - 6.0],
                                                            [SX - SHANK_R, NUT_END], [SX + SHANK_R, NUT_END]],
               fill=None, stroke="TICK", w=3, alpha=_on(st["ghost"] == "on")),
            _P("tipring", "poly", T._ring((SX, tip), 30.0), fill=None, stroke="AMBER", w=4, alpha=_on(st["tip"] == "on")),
        ]
        for j, (y, s) in enumerate(((624.0, 1), (640.0, 1), (624.0, -1), (640.0, -1))):
            x0 = SX - s * (SHANK_R + 44.0)
            x1 = SX - s * (SHANK_R + 6.0)
            out.append(_P(f"clamp{j}", "line", [[x0, y], [x1, y]], stroke="AMBER", w=4, head=10, alpha=_on(st["clamp"] == "on")))
        # ゆるみ：頭のまわりの回る矢印（ゆるむ向き）と、板と金具のずれの両向きの矢印
        out.append(_P("turn", "line", _arc_e(SX, 372.0, 128.0, 30.0, 340.0, 200.0), stroke="ALERT", w=5, head=16,
                      alpha=_on(st["loose"] == "on")))
        out.append(_P("slip_a", "line", [[700.0, 470.0], [650.0, 470.0]], stroke="ALERT", w=4, head=12, alpha=_on(st["loose"] == "on")))
        out.append(_P("slip_b", "line", [[700.0, 470.0], [750.0, 470.0]], stroke="ALERT", w=4, head=12, alpha=_on(st["loose"] == "on")))
        # 塗装のはげ（合わせ目の地の金属）
        for j, (x0, x1) in enumerate(((378.0, 414.0), (440.0, 462.0), (548.0, 590.0), (604.0, 624.0))):
            out.append(_P(f"paint{j}", "poly", [[x0, 434.0], [x1, 434.0], [x1 + 4.0, 446.0], [x0 + 4.0, 446.0]], fill="#e6edf0",
                          stroke="#e6edf0", w=1, alpha=_on(st["paint"] == "on")))
        # 締め直し（締める向きの矢印）
        out.append(_P("tight", "line", _arc_e(SX, 372.0, 128.0, 30.0, 200.0, 340.0), stroke="AMBER", w=5, head=16,
                      alpha=_on(st["tight"] == "on")))
        for j, x in enumerate(FLY_X):
            out.append(_P(f"fly{j}", "poly", _plane(x, FLY_Y), fill="BG2", stroke="ALERT" if j == 2 else "INK_W", w=2,
                          alpha=_on(nf > j)))
        return out
    if view == "spring":
        th = GHOST_DEG["shake"] if st["shake"] == "on" else GHOST_DEG["wobble"] if st["wobble"] == "on" else 0.0
        ga = 0.38 if th else 0.0
        low = st["stiff"] == "low"
        out = [
            _P("elev", "poly", ELEV_S, fill="BG2", stroke="INK_W", w=3),
            _P("bracket", "line", [[ANCHOR_S[0], 566.0], [ANCHOR_S[0], ANCHOR_S[1]]], stroke="INK_W", w=5),
            _P("tab_up", "poly", TAB_S, fill="AMBER", stroke="AMBER", w=1, alpha=ga, pivot=list(HINGE_S), rot=th),
            _P("tab_dn", "poly", TAB_S, fill="AMBER", stroke="AMBER", w=1, alpha=ga, pivot=list(HINGE_S), rot=-th),
            _P("tab", "poly", TAB_S, fill="AMBER", stroke="INK_W", w=2.5),
            _P("spr_hi", "line", _spring(9, 14.0), stroke="INK_W", w=7, alpha=_on(not low)),
            _P("spr_lo", "line", _spring(4, 24.0), stroke="AMBER", w=3, alpha=_on(low)),
            _P("scr", "poly", T._ring(HINGE_S, 11.0), fill="#b9c3c9", stroke="INK_W", w=2),
            _P("scr_gap", "poly", T._ring(HINGE_S, 22.0), fill=None, stroke="ALERT", w=4, alpha=_on(st["screw"] == "loose")),
            _P("zz", "line", M._zig(520.0, 430.0, 520.0, 630.0, 6, 12.0), stroke="ALERT", w=4, alpha=_on(st["shake"] == "on")),
        ]
        up_te = T._rot(TE_S, HINGE_S, GHOST_DEG["shake"])
        dn_te = T._rot(TE_S, HINGE_S, -GHOST_DEG["shake"])
        a_air = _on(st["air"] == "on")
        out += [_P("air_up", "line", [[up_te[0] + 60.0, up_te[1] - 14.0], [up_te[0] + 60.0, up_te[1] - 84.0]], stroke="LINE", w=6,
                   head=18, alpha=a_air),
                _P("air_dn", "line", [[dn_te[0] + 60.0, dn_te[1] + 14.0], [dn_te[0] + 60.0, dn_te[1] + 84.0]], stroke="LINE", w=6,
                   head=18, alpha=a_air)]
        a_g = _on(st["graph"] == "on")
        out += [_P("g_steady", "line", _wave("steady"), stroke="AMBER", w=4, alpha=a_g),
                _P("g_grow", "line", _wave("grow"), stroke="ALERT", w=4, alpha=a_g),
                _P("g_time", "line", [[G_X[0], 872.0], [G_X[1], 872.0]], stroke="TICK", w=3, head=14, alpha=a_g)]
        return out
    # chart
    acc = C(*ACC_UV)
    return [
        _P("region", "poly", REGION, fill="ALERT", stroke="ALERT", w=1, alpha=0.26 * _on(st["region"] == "on")),
        _P("edge", "line", REGION[:41], stroke="ALERT", w=4, alpha=_on(st["region"] == "on")),
        _P("ar_speed", "line", list(map(list, ARROW_SPEED)), stroke="AMBER", w=6, head=20, alpha=_on(st["arrows"] == "on")),
        _P("ar_stiff", "line", list(map(list, ARROW_STIFF)), stroke="AMBER", w=6, head=20, alpha=_on(st["arrows"] == "on")),
        _P("acc", "poly", T._ring(acc, 13.0, 16), fill="INK_W", stroke="INK_W", w=2, alpha=_on(st["acc"] == "on")),
        _P("ring", "poly", T._ring(acc, 40.0), fill=None, stroke="AMBER", w=5, alpha=_on(st["ring"] == "on")),
    ]


def anchors(view, st):
    if view == "nut":
        tip = TIP[st["screw"]]
        return dict(tip=(SX + 30.0, tip), ins=(NUT[2] - 10.0, 632.0), head=(SX + 96.0, 372.0), paint=(610.0, 440.0),
                    paint_l=(396.0, 446.0), ghost=(SX - SHANK_R, (NUT_END + TIP["spec"]) / 2), fly=(FLY_X[2], FLY_Y - 40.0))
    if view == "spring":
        return dict(spring=((HORN_TIP[0] + ANCHOR_S[0]) / 2, 640.0), tab=(700.0, 520.0), scr=(HINGE_S[0], HINGE_S[1] - 24.0),
                    up=(TE_S[0] + 60.0, 380.0), dn=(TE_S[0] + 60.0, 700.0))
    acc = C(*ACC_UV)
    return dict(acc=(acc[0], acc[1] - 16.0), region=C(0.85, 0.3), speed=ARROW_SPEED[1], stiff=ARROW_STIFF[1])


# 札の置き場（x, y, 揃え, 幅）。⚠️ 引き出しの線は札の x から引く＝的より左の札は "end"（右の端から線を出す）。
#   nut：右の列 r1〜r5（x1110）は線を引くなら頭（上）だけ＝部品の名の引き出し線（y415〜631）を横切らない。
#        断面の下の空き（y660〜）に gh（決まりの長さの影の左）・tp（ねじの先の下）、金具の左に pl（塗装のはげ）
TAG_AT = dict(
    nut=dict(r1=(1110.0, 300.0, "start", 730.0), r2=(1110.0, 370.0, "start", 730.0), r3=(1110.0, 440.0, "start", 730.0),
             r4=(1110.0, 510.0, "start", 730.0), r5=(1110.0, 580.0, "start", 730.0), b1=(1110.0, 800.0, "start", 730.0),
             low=(260.0, 800.0, "start", 520.0), gh=(440.0, 722.0, "end", 230.0), tp=(560.0, 790.0, "start", 500.0),
             pl=(360.0, 500.0, "end", 280.0)),
    spring=dict(top=(560.0, 300.0, "start", 900.0), t2=(560.0, 356.0, "start", 900.0), r1=(1130.0, 420.0, "start", 700.0),
                s1=(1160.0, 732.0, "start", 230.0), s2=(1160.0, 824.0, "start", 230.0), lft=(100.0, 700.0, "start", 400.0),
                spr=(1090.0, 690.0, "start", 380.0)),
    chart=dict(r1=(1240.0, 330.0, "start", 580.0), r2=(1240.0, 400.0, "start", 580.0), r3=(1240.0, 470.0, "start", 580.0),
               r4=(1240.0, 540.0, "start", 580.0), reg=(C(0.70, 0.12)[0], C(0.70, 0.12)[1], "middle", 300.0),
               sp=(600.0, 596.0, "start", 260.0), st=(532.0, 392.0, "start", 330.0),
               acc=(C(*ACC_UV)[0], C(*ACC_UV)[1] - 50.0, "middle", 200.0)),
)


def _base(view, start):
    g = []
    if view == "nut":
        # 部品の名（いつも本当＝基図）。引き出しの線は部品の右の縁へ
        for y, t, x_to in ((424.0, "板（トリムタブ）", TAB[2]), (506.0, "ちょうつがいの金具", FIT[2]), (578.0, "ナット", NUT[2]),
                           (640.0, "繊維の詰め物", NUT[2] - 4.0)):
            g.append(F.line(x_to + 6.0, y - 9.0, 800.0, y - 9.0, J.LINE_DIM, 2))
            g.append(F.txtfit(810.0, y, t, 280, cap=26, col=J.TICK))
    elif view == "spring":
        # ⚠️ 下見：「板」を板の上に置くと上へ揺れた影に重なり、「昇降舵」は右上の札（空気の力）に近かった＝板の後ろの縁の左・昇降舵の右寄り
        g.append(F.txtfit(1330.0, 462.0, "昇降舵", 200, cap=26, col=J.TICK))
        g.append(F.txtfit(470.0, 545.0, "板", 80, cap=26, col=J.TICK, anchor="end"))
        g.append(F.arrow(1830.0, 400.0, 1640.0, 400.0, J.LINE_DIM, 3, 14))
        g.append(F.txtfit(1830.0, 388.0, "空気の流れ", 240, cap=22, col=J.TICK, anchor="end"))
    else:
        o = C_O
        g.append(F.arrow(o[0], o[1], o[0] + C_W + 30.0, o[1], J.TICK, 4, 18))
        g.append(F.arrow(o[0], o[1], o[0], o[1] - C_H - 30.0, J.TICK, 4, 18))
        # ⚠️ 下見：軸の下の「速さ」は出典の行に、軸の上の「支えのかたさ」は左上の見え方の名に重なった＝矢印の先の横へ
        g.append(F.txtfit(o[0] + C_W + 44.0, o[1] + 10.0, "速さ", 200, cap=28, col=J.TICK))
        g.append(F.txtfit(o[0] + 18.0, o[1] - C_H - 12.0, "支えのかたさ", 300, cap=28, col=J.TICK))
    return g


def bolt(view, steps, start=None, rel=(), note="", src="", base_tags=()):
    """ねじ・ナット・フラッターの模式図。view＝"nut"｜"spring"｜"chart"。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"bolt：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    return M.build("bolt", view, FIELDS[view], START[view], parts_of, _base, anchors, TAG_AT, VIEWS[view]["lab"], steps, start,
                   rel, note, src, base_tags)
