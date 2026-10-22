# -*- coding: utf-8 -*-
"""mech24.py — 24本目（チェルノブイリ原発事故）「図解」（2026-10-23 新設・⑤b-4＝第1〜3章の39カット）。

■ 何か
  17本目 `mech17` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。再現イラストではない＝「再現」の札は出さない。
  左上に見え方の名（見る向きのある見え方は頭に「横から」「上から」＝門番 check_mech が PLAN の「見る向き：」と照らす）・
  左下に注（模式の見え方は「模式」）と出典。
  🔴 人の形・顔・運転員の名前は描かない（名前は記録にある5人だけ＝台本 §1-4・この章の図は役職だけ）。
  🔴 **色は報告の色**（台本の帰属の呼び分け＝§1-5・記憶 project-jiko-ep24-chernobyl）：
     1986年の報告（INSAG-1）＝桃 bldg_a／1986年のソ連の報告（8月）＝橙 company／1991年の委員会（INSAG-7 の付属書I）＝紫 city／
     1992年の報告（INSAG-7 本文）＝青 state。意味の色＝赤 ALERT（危ない・切る・急落）・黄 AMBER（数・時刻）・緑 OK（許される・続く）。
     物の色＝水 ship（水色）・燃料 company（橙＝燃料の絵の中だけ。報告の札と同じ画面に置かない）・黒鉛 LINE。
     ⚠️ 新しい色の値は足していない（ROLE の名で引く＝門番 check_color・check_palette の物差しはそのまま）
  🔴 割れる時刻と数は台本 §1-5 の値だけ（1:06・1:00〈1986年の報告と帰属〉・13:05・14:00・23:10・0:05・0:28）。
     S3 の「試験のあいだ（約4時間）」は札にしない（台本 §1-5＝言わない）。200MW で止まった時刻は「1時ごろ」（c410＝出典の名で割れる）。

■ 見え方（view）＝映像方針の一覧 `ref/ep24/eizou_list24.md` の「見た目の型」（第1〜3章の図解 39カット＝地図 c203 は ⑤b-6）
  第1章  years（c205 年表）・cards7（c206 7つの札）・neutron（c209 粒）・void（c210 輪の矢印）・power20（c211 目盛り）・
         flow4（c214 流れ図）・decay（c215 横から＝燃料の管）・cal（c216 暦）・plan（c219 書類）・blame（c220 札の比べ）・
         cut（c222 帯と札）・site（c224 上から＝発電所の配置）
  第2章  dial（c301 針の計器）・ruler（c302 物差し）・orm（c306 線のグラフ）・turbine（c307 タービン2台）・eccs（c308 横から＝管と弁）・
         stamp（c310 承認の印）・off11（c311 時間の帯）・grid3（c312 3つの欄）・trigger（c313 札と×）・kiev（c314 矢印の流れ）・
         ring（c316 24時間の輪）・day（c317 日めくり）
  第3章  meter（c401 横の目盛りの針）・clock（c402 時計）・hold（c404 札）・swap（c406 札の入れ替え）・two91（c407 2つの札）・
         letter（c408 封筒）・docline（c409 書類の一行）・say3（c410 3つの言い方）・bars（c412 熱出力の棒）・page86（c414 頁の札）・
         limit（c415 あとで決まった下限）・pillars（c416 3つの欄）・inst（c417 横から＝計器）・thermo（c420 温度計）・balance（c421 天秤）
  🔴 同じ型は全編で2回まで・続けない（台本 §7）：年表 c205↔cb02・札 c206↔c714・流れ c214↔c507・暦 c216↔c911・時計 c402↔c614・棒 c412↔cb06＝
     相方は ⑤b-5・⑤b-6 で別の絵に。この章の中の似た形（針の計器 c301＝丸・c401＝横／時間の帯 c311＝帯・c316＝輪／3つの欄 c312＝表・c416＝書類3つ／
     2つの札 c407＝虫めがねと針・c421＝天秤）は形を替えた

■ SPEC の書き方（mech17 と同じ）
  fig=("m24", dict(view=…, start=dict(…), steps=[dict(state=dict(…)), …], rel=[dict(t="3,200", src="S2 p1008")], note="…", src=ss.src([…])))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。🔴 画面の字の数（時刻・数・年）は全部 `rel=` に同じ文字列で宣言する
  （門番 check_mech の judge_m24 が**基図と段の層の全部の字**から数を拾って照らす）。
  🔴 記録の値（報告の名と色・年と月・札の言葉と順・時刻・値・目盛り）は門番の側 REC_M24 が別に持つ（§5b-88）。描く側の表を書き換えると鳴る。
"""
from __future__ import annotations

import math
import re

import fontmetrics as fm
import jiko_style as J
import titan_fig as F
from mech21 import _P, _arrow, _check, _on, _qmark, _xmark

ONOFF = ("off", "on")
INK = J.INK_W
CX = 960.0
WATER = J.ROLE["ship"]            # 水＝水色
FUEL = J.ROLE["company"]          # 燃料＝橙（燃料の絵の中だけ）
STEEL = "#9aa4ac"                 # 制御棒・機械の鋼（mech17 の機の形と同じ灰）
GRAPH = J.LINE                    # 黒鉛

# 報告の色（台本の帰属の呼び分け）＝名・ROLE の名
REPS = dict(
    r86=("1986年の報告", "bldg_a"),          # INSAG-1（IAEA の専門家グループ・1986年9月）
    s86=("1986年のソ連の報告", "company"),   # ソ連の報告（ウィーンの会議の資料・1986年8月）
    c91=("1991年の委員会", "city"),          # ソ連の委員会の報告（INSAG-7 の付属書I）
    r92=("1992年の報告", "state"),           # INSAG-7（書き直し）
)
# 報告の名の数（年）の宣言＝SPEC の rel に足す（札の名の「1986」「1992」…＝門番 judge_m24 ③）。出どころ＝表紙の日付
REP_REL = dict(r86=dict(t="1986年の報告（1986年9月）", src="S2 p1001"), s86=dict(t="1986年のソ連の報告（1986年8月）", src="S3 p2003"),
               c91=dict(t="1991年の委員会（1991年）", src="S1 p39"), r92=dict(t="1992年の報告（1992年）", src="S1 p1"))


def rr(*keys):
    return [dict(REP_REL[k]) for k in keys]


# 7つの「違反」（台本 §4 c206 の画の欄＝①〜⑦の順）。右上の印（違反の札）と c206 の札で同じ言葉
VIOL = ("試験の計画", "非常用の冷却", "0時28分の急落", "700メガワット", "蒸気ドラムの保護", "タービンの保護", "残した制御棒の数")
CIRC = "①②③④⑤⑥⑦"


def rc(r):
    """役の名（ROLE）か意味の色の名（ALERT・LINE…）か #色 → 色の値。"""
    if not r:
        return INK
    if str(r).startswith("#"):
        return r
    return J.ROLE.get(r) or getattr(J, r)


def rep_col(key):
    return rc(REPS[key][1])


def _tline(x, y, t, cap=30, col=None, anchor="start", mw=600, fam="Noto", ol=0):
    return F.txtfit(x, y, t, mw, cap=cap, col=col or INK, anchor=anchor, fam=fam, ol=ol)


def _w(t, cap, fam="Noto"):
    return fm.width(str(t), cap, fam)


def _card(cx, cy, w, h, col, fill=None, sw=4, dash=None):
    return F.rect(cx - w / 2, cy - h / 2, w, h, fill or J.BG2, col, sw, rx=10, dash=dash)


def _rep(cx, cy, key, body=None, cap=28, w=None):
    """報告の札（縁と名は報告の色・中身は白）。body なし＝名だけ（高さ 60）・あり＝2行（高さ 108）。"""
    name, role = REPS[key]
    col = rc(role)
    if w is None:
        w = max(_w(name, cap - 2), _w(body or "", cap + 2)) + 56
    if body is None:
        return _card(cx, cy, w, 60, col, sw=5) + _tline(cx, cy + cap * 0.36, name, cap, col, "middle", w - 28)
    return (_card(cx, cy, w, 108, col, sw=5) + _tline(cx, cy - 12, name, cap - 2, col, "middle", w - 28)
            + _tline(cx, cy + 34, body, cap + 2, INK, "middle", w - 28))


def rep_box(cx, cy, key, body=None, cap=28, w=None):
    """_rep の箱（門番の幾何・ほかの絵とのすき間を測る）。"""
    name = REPS[key][0]
    if w is None:
        w = max(_w(name, cap - 2), _w(body or "", cap + 2)) + 56
    h = 60 if body is None else 108
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def _badge(n):
    """右上の違反の札（「違反とされた」＋丸数字＋名）。c206 の札と同じ言葉。"""
    t = f"{CIRC[n - 1]} {VIOL[n - 1]}"
    w = _w(t, 28) + 180               # 🔧 門番 layout：+150 だと「違反とされた」と 8px 重なった
    x1, y0 = F.BX1 - 4, F.BY0 + 8
    return (F.rect(x1 - w, y0, w, 52, J.BG2, J.AMBER, 4, rx=10)
            + _tline(x1 - w + 16, y0 + 36, "違反とされた", 22, J.TICK, "start", 130)
            + _tline(x1 - 16, y0 + 37, t, 28, J.AMBER, "end", w - 150))


def _bigtime(x, y, t, cap=96, col=None, anchor="middle"):
    """大きな時刻（Dela）。"""
    return F.txt(x, y, t, cap, col or J.AMBER, "Dela", anchor)


def _bolt(cx, cy, s=40.0, col=None):
    """電気の印（稲妻）。"""
    p = [(cx + 0.15 * s, cy - s), (cx - 0.45 * s, cy + 0.1 * s), (cx - 0.02 * s, cy + 0.1 * s), (cx - 0.2 * s, cy + s),
         (cx + 0.45 * s, cy - 0.15 * s), (cx + 0.02 * s, cy - 0.15 * s)]
    return F.poly(p, col or J.AMBER, None, close=True)


def _moon(cx, cy, r=30.0, col=None):
    c = col or "#f3e7a6"
    return F.circ(cx, cy, r, c, None) + F.circ(cx + r * 0.45, cy - r * 0.25, r * 0.85, J.BG, None)


def _doc(x, y, w, h, col, nlines=6, top=70.0, lw=None, gap=None):
    """書類の紙（縁・題の帯の下に灰の行）。"""
    g = [F.rect(x, y, w, h, J.BG2, col, 4, rx=8)]
    gap = gap or (h - top - 30) / max(nlines, 1)
    for i in range(nlines):
        yy = y + top + i * gap
        g.append(F.line(x + 30, yy, x + w - 30 - (lw or 0) * (i % 3 == 2), yy, J.LINE_DIM, 8))
    return "".join(g)


def _turbine(cx, cy, s=1.0, col=None, dim=False):
    """横から見たタービン（軸と羽根の列）＝模式。"""
    c = J.LINE_DIM if dim else (col or STEEL)
    g = [F.rect(cx - 170 * s, cy - 14 * s, 340 * s, 28 * s, c, None, None, rx=6)]
    for i, h in enumerate((70, 90, 110, 130, 150, 130)):
        x = cx - 120 * s + i * 48 * s
        g.append(F.rect(x - 9 * s, cy - h * s / 2, 18 * s, h * s, c, None, None, rx=4))
    return "".join(g)


def _pump(cx, cy, r=46.0, col=None):
    c = col or WATER
    g = [F.circ(cx, cy, r, J.BG2, c, 5)]
    for a in (0, 120, 240):
        t = math.radians(a)
        g.append(F.line(cx, cy, cx + (r - 10) * math.cos(t), cy + (r - 10) * math.sin(t), c, 6))
    return "".join(g)


def _gear(cx, cy, r=40.0, col=None):
    c = col or STEEL
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5)
        rr = r if i % 2 == 0 else r * 0.78
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return F.poly(pts, J.BG2, c, 5, close=True) + F.circ(cx, cy, r * 0.32, J.BG, c, 4)


def _arcpts(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def _arc_arrow(cx, cy, rx, ry, a0, a1, col, sw=6, head=22):
    p = _arcpts(cx, cy, rx, ry, a0, a1)
    return F.poly(p[:-1], "none", col, sw) + _arrow(p[-3][0], p[-3][1], p[-1][0], p[-1][1], col, sw, head)


# ══════════════════════════════════════════════════════════
#  years（c205）＝報告の年表（4つの点＝1986年8月 ソ連の報告〈細い点〉・1986年9月 1986年の報告・1991年 委員会・1992年 書き直し〈太い点〉）。
#  間隔は時間に比例しない（1986年の2つの点が近すぎる）＝順と年だけ・あいだに省略の印
# ══════════════════════════════════════════════════════════
YEARS = (("s86", "1986年8月", (1986, 8), False, "ウィーンの会議の資料", "ソ連の報告"),
         ("r86", "1986年9月", (1986, 9), True, "INSAG-1", "1986年の報告"),
         ("c91", "1991年", (1991, 0), True, "1992年の報告の付属書I", "ソ連の委員会の報告"),
         ("r92", "1992年", (1992, 0), True, "INSAG-7", "書き直しの報告"))
YR = dict(y=560.0, x0=200.0, x1=1720.0, xs=(330.0, 660.0, 1140.0, 1500.0), brk=900.0)


def years_base(st0):
    g = [F.line(YR["x0"], YR["y"], YR["brk"] - 26, YR["y"], J.LINE, 6), F.line(YR["brk"] + 26, YR["y"], YR["x1"], YR["y"], J.LINE, 6)]
    for dx in (-14, 14):     # 省略の印（≈）
        g.append(F.line(YR["brk"] + dx - 10, YR["y"] + 18, YR["brk"] + dx + 10, YR["y"] - 18, J.TICK, 5))
    g.append(_arrow(YR["x1"] - 40, YR["y"], YR["x1"] + 30, YR["y"], J.LINE, 6, 24))
    g.append(_tline(1690.0, 820.0, "● 主に追う3つ　○ ほかの報告", 24, J.TICK, "end", 520))
    return g


def _yr_pt(i):
    key, date, _ym, thick, sub, name = YEARS[i]
    x, y, col = YR["xs"][i], YR["y"], rep_col(key)
    g = []
    if thick:
        g.append(F.circ(x, y, 22, col, J.BG, 4))
        g.append(F.line(x, y - 24, x, y - 70, col, 4))
        g.append(_tline(x, y - 222, date, 34, J.AMBER, "middle", 300))
        g.append(_tline(x, y - 170, name, 32, col, "middle", 330))
        g.append(_tline(x, y - 124, sub, 24, J.TICK, "middle", 330))
    else:
        g.append(F.circ(x, y, 12, J.BG, col, 4))
        g.append(F.line(x, y + 14, x, y + 60, col, 3, dash="6 6"))
        g.append(_tline(x, y + 106, date, 30, J.AMBER, "middle", 280))
        g.append(_tline(x, y + 150, name, 28, col, "middle", 280))
        g.append(_tline(x, y + 190, sub, 22, J.TICK, "middle", 300))
    return "".join(g)


def years_stage(prev, st):
    s = []
    for i, (key, *_r) in enumerate(YEARS):
        if _on(prev, st, key):
            s.append(_yr_pt(i))
    if _on(prev, st, "arc"):
        xa, xb, y = YR["xs"][1], YR["xs"][3], YR["y"] + 40
        pts = [(xa + (xb - xa) * i / 24, y + 110 * math.sin(math.pi * i / 24)) for i in range(25)]
        s.append(F.poly(pts[:-1], "none", rep_col("r92"), 5, dash="14 10"))
        s.append(_arrow(pts[-3][0], pts[-3][1], xb, y + 4, rep_col("r92"), 5, 22))
        s.append(_tline((xa + xb) / 2, y + 160, "改めた", 30, rep_col("r92"), "middle", 300))      # 🔧 門番 dup：「書き直しの報告」と同じ語
    return s


# ══════════════════════════════════════════════════════════
#  cards7（c206）＝7つの札（①〜⑦＝台本 §4 c206 の画の欄の順）→ 3行目で各札に「？」と1992年の報告の札（評価と並べる）
# ══════════════════════════════════════════════════════════
C7 = dict(w=380.0, h=96.0, ys=(420.0, 576.0), xs4=(309.0, 743.0, 1177.0, 1611.0), xs3=(526.0, 960.0, 1394.0))


def c7_xy(i):
    return (C7["xs4"][i], C7["ys"][0]) if i < 4 else (C7["xs3"][i - 4], C7["ys"][1])


def cards7_base(st0):
    return []


def cards7_stage(prev, st):
    s = []
    if _on(prev, st, "cards"):
        for i, t in enumerate(VIOL):
            cx, cy = c7_xy(i)
            s.append(_card(cx, cy, C7["w"], C7["h"], J.LINE))
            s.append(F.txt(cx - C7["w"] / 2 + 38, cy + 15, CIRC[i], 42, J.AMBER, "Noto", "middle"))
            s.append(_tline(cx + 22, cy + 11, t, 30, INK, "middle", C7["w"] - 100))
    if _on(prev, st, "ask"):
        for i in range(7):                  # 🔧 geom_gap：「？」が札の縁に -15px＝丸を札の右下の角の外へ
            cx, cy = c7_xy(i)
            qx, qy = cx + C7["w"] / 2 + 22, cy + C7["h"] / 2 + 14
            s.append(F.circ(qx, qy, 22, J.BG, rep_col("r92"), 4))
            s.append(F.txt(qx, qy + 10, "？", 28, rep_col("r92"), "Noto", "middle"))
        s.append(_rep(CX, 740.0, "r92", "の評価と比べる", cap=28))
    return s


# ══════════════════════════════════════════════════════════
#  neutron（c209）＝1行目：炉が出す熱 3,200MW → 電気 1,000MW（S2 p1008）／2行目：ウラン → 速い中性子 → 黒鉛で遅く → 次のウランが割れる（粒の模式）
# ══════════════════════════════════════════════════════════
NT_HEAT, NT_ELEC = "3,200", "1,000"
NT = dict(y=380.0, gx=(560.0, 920.0), gy=(600.0, 780.0), u1=(330.0, 690.0), u2=(1180.0, 690.0))


def neutron_base(st0):
    return []


def _uranium(cx, cy, r=46.0):
    g = [F.circ(cx, cy, r, FUEL, J.BG, 3)]
    for dx, dy in ((-14, -12), (12, -16), (-6, 14), (16, 10)):
        g.append(F.circ(cx + dx, cy + dy, 9, "#ffd2a8", None))
    return "".join(g)


def neutron_stage(prev, st):
    s = []
    if _on(prev, st, "power"):
        s.append(F.rect(220.0, NT["y"] - 60, 300, 120, J.BG2, J.LINE, 4, rx=10))
        s.append(_tline(370.0, NT["y"] + 12, "4号炉", 34, INK, "middle", 260))
        s.append(_arrow(540.0, NT["y"], 660.0, NT["y"], J.ALERT, 6, 24))
        s.append(_card(890.0, NT["y"], 400, 120, J.ALERT, sw=5))
        s.append(_tline(890.0, NT["y"] - 16, "炉が出す熱", 28, J.ALERT, "middle", 360))
        s.append(_tline(890.0, NT["y"] + 40, f"{NT_HEAT}MW", 44, J.AMBER, "middle", 360, fam="Dela"))
        s.append(_arrow(1110.0, NT["y"], 1230.0, NT["y"], J.AMBER, 6, 24))
        s.append(_card(1450.0, NT["y"], 400, 120, J.AMBER, sw=5))
        s.append(_bolt(1300.0, NT["y"], 34))
        s.append(_tline(1480.0, NT["y"] - 16, "電気にすると", 28, J.AMBER, "middle", 300))
        s.append(_tline(1480.0, NT["y"] + 40, f"{NT_ELEC}MW", 44, J.AMBER, "middle", 300, fam="Dela"))
    if _on(prev, st, "chain"):
        (x0, x1), (y0, y1) = NT["gx"], NT["gy"]
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, "#2b3a44", GRAPH, 4, rx=6))
        for k in range(1, 6):
            s.append(F.line(x0 + 10, y0 + k * 30, x1 - 10, y0 + k * 30, J.LINE_DIM, 3))
        s.append(_tline((x0 + x1) / 2, y1 + 44, "黒鉛", 30, GRAPH, "middle", 300))
        s.append(_uranium(*NT["u1"]))
        s.append(_tline(NT["u1"][0], NT["u1"][1] + 92, "ウラン", 28, FUEL, "middle", 200))
        s.append(F.line(400.0, 690.0, 540.0, 690.0, INK, 3, dash="4 4"))          # 速い中性子（長い尾）
        s.append(F.circ(552.0, 690.0, 10, INK, None))
        s.append(_tline(470.0, 650.0, "速い中性子", 24, INK, "middle", 200))
        for k in range(4):                                                          # 黒鉛の中で遅くなる（尾が短く）
            xx = 620.0 + k * 80
            s.append(F.line(xx - 30 + k * 6, 690.0, xx, 690.0, INK, 3))
            s.append(F.circ(xx + 8, 690.0, 8, INK, None))
        s.append(F.circ(1010.0, 690.0, 9, INK, None))
        s.append(F.line(990.0, 690.0, 1002.0, 690.0, INK, 3))
        s.append(_tline(1010.0, 650.0, "遅くなる", 24, INK, "middle", 160))
        s.append(_arrow(1030.0, 690.0, 1120.0, 690.0, INK, 4, 18))
        s.append(_uranium(*NT["u2"]))
        for a in (-40, 0, 40):                                                      # 割れる
            t = math.radians(a)
            s.append(F.line(1180 + 60 * math.cos(t), 690 + 60 * math.sin(t), 1180 + 100 * math.cos(t), 690 + 100 * math.sin(t), J.ALERT, 6))
        s.append(_tline(1180.0, 782.0, "割れる", 28, J.ALERT, "middle", 200))
        s.append(_arc_arrow(1180.0, 600.0, 330.0, 110.0, -10.0, -170.0, J.OK, 5, 20))
        s.append(_tline(1560.0, 700.0, "反応が続く", 30, J.OK, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  void（c210）＝左：水の管（下の水が中性子を吸う・上ほど泡）／右：輪の矢印（沸く・泡 → 吸う水が減る → 反応が強まる → 熱が増える → 沸く）・
#  中に「正のボイド係数」（2行目）
# ══════════════════════════════════════════════════════════
VD_NODES = ("水が沸いて泡が増える", "中性子を吸う水が減る", "反応が強まる", "熱が増える")
VD = dict(cx=1170.0, cy=560.0, rx=390.0, ry=232.0, w=330.0, h=82.0, tube=(210.0, 330.0, 330.0, 800.0))


def vd_xy(i):
    a = math.radians(-90 + 90 * i)
    return VD["cx"] + VD["rx"] * math.cos(a), VD["cy"] + VD["ry"] * math.sin(a)


def void_base(st0):
    return []


def void_stage(prev, st):
    s = []
    if _on(prev, st, "tube"):
        x0, y0, x1, y1 = VD["tube"]
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, "#123a44", WATER, 4, rx=12))
        for i, (bx, by) in enumerate(((240, 360), (300, 392), (258, 430), (292, 470), (246, 520), (310, 548), (270, 600))):
            s.append(F.circ(bx, by, 16 - i * 1.6, "none", INK, 3))
        for bx, by in ((250, 690), (300, 740), (262, 770)):
            s.append(F.circ(bx, by, 9, INK, None))
            s.append(_xmark(bx + 14, by - 14, 8, WATER, 4))
        s.append(_tline(380.0, 370.0, "泡（蒸気）", 26, INK, "start", 200))
        s.append(_tline(380.0, 740.0, "吸われる中性子", 26, WATER, "start", 230))
    for k, (f_, ids) in enumerate((("n12", (0, 1)), ("n34", (2, 3)))):
        if _on(prev, st, f_):
            for i in ids:
                x, y = vd_xy(i)
                col = J.ALERT if i == 2 else (WATER if i == 1 else INK)
                s.append(_card(x, y, VD["w"], VD["h"], col, sw=5))
                s.append(_tline(x, y + 10, VD_NODES[i], 28, col if i else INK, "middle", VD["w"] - 30))
            arcs = ((-62, -22),) if k == 0 else ((22, 62), (118, 158), (202, 242))
            for a0, a1 in arcs:
                s.append(_arc_arrow(VD["cx"], VD["cy"], VD["rx"] - 20, VD["ry"] - 20, a0, a1, J.AMBER, 6, 22))
    if _on(prev, st, "name"):
        s.append(_tline(VD["cx"], VD["cy"] + 14, "正のボイド係数", 40, J.AMBER, "middle", 420))
    return s


# ══════════════════════════════════════════════════════════
#  power20（c211）＝出力の目盛り（低い → 最大の出力）・およそ20%より下を赤く（S2 p1009）→ 3行目：上がると、さらに上がる（2段の矢印）
# ══════════════════════════════════════════════════════════
PW_LOW = 20                       # 最大の出力に対する割合（%）＝S2 p1009「below approximately 20% of full power」
PW = dict(x0=260.0, x1=1660.0, y=560.0, h=60.0)


def pw_x(pct):
    return PW["x0"] + (PW["x1"] - PW["x0"]) * pct / 100.0


def power20_base(st0):
    x0, x1, y, h = PW["x0"], PW["x1"], PW["y"], PW["h"]
    g = [F.rect(x0, y - h / 2, x1 - x0, h, J.BG2, J.LINE, 4, rx=8)]
    for k in range(11):
        x = x0 + (x1 - x0) * k / 10
        g.append(F.line(x, y + h / 2, x, y + h / 2 + 18, J.TICK, 3))
    g.append(_tline(x0, y + h / 2 + 64, "低い", 28, J.TICK, "start", 200))
    g.append(_tline(x1, y + h / 2 + 64, "最大の出力", 28, J.TICK, "end", 300))
    g.append(_tline(x0, y - h / 2 - 22, "炉の出力", 28, INK, "start", 300))
    return g


def power20_stage(prev, st):
    s = []
    x0, y, h = PW["x0"], PW["y"], PW["h"]
    xl = pw_x(PW_LOW)
    if _on(prev, st, "low"):
        s.append(F.rect(x0 + 4, y - h / 2 + 4, xl - x0 - 8, h - 8, J.ALERT, None, None, rx=6))
        s.append(F.line(xl, y - h / 2 - 12, xl, y + h / 2 + 30, J.AMBER, 5))
        s.append(_tline(xl, y + h / 2 + 64, f"およそ{PW_LOW}%", 30, J.AMBER, "middle", 260))
        s.append(_rep(1190.0, 400.0, "r86", "この下は性質が変わる"))
    if _on(prev, st, "loop"):
        bx = (x0 + xl) / 2
        s.append(_arrow(bx - 70, 470.0, bx - 70, 380.0, J.ALERT, 10, 30))
        s.append(_arrow(bx + 30, 470.0, bx + 30, 330.0, J.ALERT, 14, 40))
        # 試し焼き 39867368772：札が矢印から離れて下に浮いた＝矢印の右へ
        s.append(_tline(bx + 90, 420.0, "上がると、さらに上がる", 30, J.ALERT, "start", 420))
    return s


# ══════════════════════════════════════════════════════════
#  flow4（c214）＝試験の中身（S3 p2019・S2 p1009）：外の電気が止まる（×）・ディーゼル発電機が動くまでの「あいだ」→
#  止まりかけのタービン → 電気 → ポンプ（2行目）→ 試験で確かめる「？」（3行目）
# ══════════════════════════════════════════════════════════
FL_BOX = (("ext", 240.0, "外から来る電気"), ("tb", 640.0, "止まりかけのタービン"), ("el", 1040.0, "電気"), ("pump", 1440.0, "ポンプ"))
FL = dict(y=430.0, w=310.0, h=120.0, ty=730.0, tx=(240.0, 1640.0), dg=(1640.0, 640.0))


def flow4_base(st0):
    return []


def flow4_stage(prev, st):
    s = []
    y, w, h = FL["y"], FL["w"], FL["h"]
    if _on(prev, st, "cut"):
        x = FL_BOX[0][1]
        s.append(_card(x, y, w, h, J.LINE))
        s.append(_tline(x, y + 10, FL_BOX[0][2], 28, INK, "middle", w - 30))
        s.append(_xmark(x + w / 2 - 6, y - h / 2 + 6, 22))
        # 時間の帯：止まる → ディーゼル発電機が動く。あいだ＝黄の破線
        t0, t1 = FL["tx"]
        s.append(F.line(t0, FL["ty"], t1, FL["ty"], J.TICK, 4))
        s.append(F.line(t0, FL["ty"] - 22, t0, FL["ty"] + 22, J.TICK, 4))
        s.append(F.line(t1, FL["ty"] - 22, t1, FL["ty"] + 22, J.TICK, 4))
        s.append(_tline(t0, FL["ty"] + 62, "外の電気が止まる", 26, J.TICK, "start", 360))
        s.append(_tline(t1, FL["ty"] + 62, "ディーゼル発電機が動く", 26, J.OK, "end", 400))
        s.append(F.rect(t0 + 20, FL["ty"] - 30, t1 - t0 - 40, 60, "none", J.AMBER, 4, rx=8, dash="12 8"))
        # 🔧 geom_gap：時間の線（ty）が字を貫いた＝破線の枠の上へ
        s.append(_tline((t0 + t1) / 2 - 100, FL["ty"] - 42, "このあいだ", 30, J.AMBER, "middle", 300))
    if _on(prev, st, "chain"):
        for k in (1, 2, 3):
            _id, x, t = FL_BOX[k]
            col = (STEEL, J.AMBER, WATER)[k - 1]
            s.append(_card(x, y, w, h, col, sw=5))
            s.append(_tline(x, y + h / 2 - 18, t, 26, col, "middle", w - 30))
            s.append(_arrow(FL_BOX[k - 1][1] + w / 2 + 6, y, x - w / 2 - 8, y, J.LINE, 5, 20))
        # 🔧 geom_gap：絵が札の下の字（y 446〜）に -9px＝小さく上へ
        s.append(_turbine(FL_BOX[1][1], y - 28, 0.48))
        s.append(_bolt(FL_BOX[2][1], y - 28, 28))
        s.append(_pump(FL_BOX[3][1], y - 28, 28))
        s.append(_tline(FL_BOX[1][1], y - h / 2 - 18, "回る勢いで", 24, STEEL, "middle", 260))
        # 帯の「このあいだ」から上の鎖へ＝つなぐ
        s.append(_arrow(1040.0, FL["ty"] - 34, 1040.0, y + h / 2 + 12, J.AMBER, 4, 18, dash="8 6"))
        s.append(_tline(1060.0, 615.0, "つなぐ", 26, J.AMBER, "start", 160))
    if _on(prev, st, "test"):
        # 🔧 geom_gap：括弧の上の線（y 280）が「試験で確かめる」と「？」を横切った＝括弧を下げる（字の下に 13px）
        s.append(F.poly([(500.0, 316.0), (500.0, 300.0), (1580.0, 300.0), (1580.0, 316.0)], "none", J.TICK, 4))
        s.append(_qmark(1040.0, 268.0, 44, J.AMBER))
        s.append(_tline(1100.0, 284.0, "試験で確かめる", 28, J.AMBER, "start", 300))
    return s


# ══════════════════════════════════════════════════════════
#  decay（c215）＝横から見た燃料の管（1本）：止めた炉（棒が入った）でも燃料は熱を出す（赤い波）→ ポンプで水を送り続ける（水色の矢印）
# ══════════════════════════════════════════════════════════
DC = dict(tube=(820.0, 320.0, 940.0, 820.0), rods=(700.0, 1060.0), pump=(480.0, 760.0))


def decay_base(st0):
    x0, y0, x1, y1 = DC["tube"]
    g = [F.rect(x0, y0, x1 - x0, y1 - y0, "#123a44", WATER, 4, rx=14),
         F.rect((x0 + x1) / 2 - 16, y0 + 40, 32, y1 - y0 - 80, FUEL, J.BG, 3, rx=8)]
    for x in DC["rods"]:
        g.append(F.rect(x - 18, y0 - 30, 36, y1 - y0 + 10, STEEL, J.BG, 3, rx=6))
    g.append(_tline(DC["rods"][1] + 40, y0 + 10, "制御棒（入っている＝止めた炉）", 26, STEEL, "start", 520))
    return g


def decay_stage(prev, st):
    s = []
    x0, y0, x1, y1 = DC["tube"]
    xm = (x0 + x1) / 2
    if _on(prev, st, "heat"):
        s.append(F.rect(xm - 16, y0 + 40, 32, y1 - y0 - 80, "none", J.ALERT, 6, rx=8))
        for yy in (420.0, 540.0, 660.0):
            for side in (-1, 1):
                pts = [(xm + side * (40 + k * 12), yy + 14 * math.sin(k * 1.4)) for k in range(6)]
                s.append(F.poly(pts, "none", J.ALERT, 4))
        s.append(_tline(DC["rods"][1] + 40, 520.0, "止めたあとも、燃料は熱を出す", 30, J.ALERT, "start", 640))
    if _on(prev, st, "pump"):
        px, py = DC["pump"]
        s.append(_pump(px, py, 50))
        s.append(F.poly([(px + 50, py), (xm - 70, py), (xm - 70, y1 + 30), (xm, y1 + 30)], "none", WATER, 8))
        s.append(_arrow(xm, y1 + 30, xm, y1 - 8, WATER, 8, 26))
        for yy in (740.0, 600.0, 460.0):
            s.append(_arrow(xm + 40, yy, xm + 40, yy - 70, WATER, 5, 18))
        s.append(_tline(px, py - 74, "ポンプ", 28, WATER, "middle", 200))
        s.append(_tline(DC["rods"][1] + 40, 650.0, "冷やす水を送り続ける", 30, WATER, "start", 560))
    return s


# ══════════════════════════════════════════════════════════
#  cal（c216）＝暦（1982〜1986年の5枚・S1 p61）：1982年 3号機で試験／1984年・1985年 改良した装置で試験／1983年12月 4号機の運転の始まり
#  （この試験をしないまま＝赤の破線）／1986年4月 この夜の試験（黄の輪）
# ══════════════════════════════════════════════════════════
CAL_YEARS = (1982, 1983, 1984, 1985, 1986)
CAL_MARK = {1982: ("ok", "3号機で試験"), 1984: ("ok", "改良した装置で試験"), 1985: ("ok", "同じく試験"),
            1983: ("start", "12月　4号機の運転の始まり"), 1986: ("night", "4月　4号機で試験")}
CAL = dict(w=290.0, h=380.0, y0=330.0, xs=(250.0, 590.0, 930.0, 1270.0, 1610.0))


def cal_base(st0):
    g = []
    for x, yr in zip(CAL["xs"], CAL_YEARS):
        g.append(F.rect(x - CAL["w"] / 2, CAL["y0"], CAL["w"], CAL["h"], J.BG2, J.LINE, 4, rx=10))
        g.append(F.rect(x - CAL["w"] / 2, CAL["y0"], CAL["w"], 70, J.LINE_DIM, None, None, rx=10))
        for dx in (-60, 60):
            g.append(F.circ(x + dx, CAL["y0"], 10, J.BG, J.LINE, 4))
        g.append(F.txt(x, CAL["y0"] + 54, f"{yr}年", 40, INK, "Dela", "middle"))
    return g


def _cal_mark(yr):
    kind, t = CAL_MARK[yr]
    x = CAL["xs"][CAL_YEARS.index(yr)]
    yc = CAL["y0"] + 210
    g = []
    if kind == "ok":
        g.append(_check(x, yc - 30, 34, J.OK))
        g.append(_tline(x, yc + 70, t, 26, J.OK, "middle", CAL["w"] - 30))
    elif kind == "start":
        a, b = t.split("　")
        g.append(F.circ(x, yc - 34, 40, "none", J.LINE, 5))
        g.append(F.poly([(x - 12, yc - 56), (x + 20, yc - 34), (x - 12, yc - 12)], J.LINE, None, close=True))
        g.append(_tline(x, yc + 46, a, 30, J.AMBER, "middle", CAL["w"] - 30))
        g.append(_tline(x, yc + 92, b, 24, INK, "middle", CAL["w"] - 24))
        g.append(F.rect(x - CAL["w"] / 2 + 12, CAL["y0"] + CAL["h"] + 20, CAL["w"] - 24, 56, "none", J.ALERT, 4, rx=8, dash="10 8"))
        g.append(_tline(x, CAL["y0"] + CAL["h"] + 58, "この試験をしないまま", 24, J.ALERT, "middle", CAL["w"] - 40))
    else:
        a, b = t.split("　")
        g.append(F.circ(x, yc - 30, 50, "none", J.AMBER, 7))
        g.append(_moon(x, yc - 30, 22))
        g.append(_tline(x, yc + 58, a, 30, J.AMBER, "middle", CAL["w"] - 30))     # 🔧 geom_gap：輪に 2px＝下へ
        g.append(_tline(x, yc + 102, b, 24, INK, "middle", CAL["w"] - 24))
    return "".join(g)


def cal_stage(prev, st):
    s = []
    for f_, yrs in (("y82", (1982,)), ("y8485", (1984, 1985)), ("y83", (1983,)), ("y86", (1986,))):
        if _on(prev, st, f_):
            for yr in yrs:
                s.append(_cal_mark(yr))
    return s


# ══════════════════════════════════════════════════════════
#  plan（c219）＝試験の計画の書類（模式）：安全の手当ての欄だけ薄い（破線・行が少ない）→ 1991年の委員会「十分でない」（1行目）・
#  1986年のソ連の報告「形だけ」（2行目）
# ══════════════════════════════════════════════════════════
PL = dict(x=340.0, y=300.0, w=520.0, h=520.0, sec=(640.0, 790.0))


def plan_base(st0):
    x, y, w, h = PL["x"], PL["y"], PL["w"], PL["h"]
    g = [F.rect(x, y, w, h, J.BG2, J.DOC, 4, rx=8), F.rect(x, y, w, 64, J.DOC_DIM, None, None, rx=8),
         _tline(x + w / 2, y + 46, "試験の計画", 32, INK, "middle", w - 40)]
    for i in range(7):
        yy = y + 110 + i * 34
        g.append(F.line(x + 30, yy, x + w - 30 - 90 * (i % 3 == 2), yy, J.LINE_DIM, 9))
    s0, s1 = PL["sec"]
    g.append(F.rect(x + 20, s0, w - 40, s1 - s0, "none", J.TICK, 3, rx=8, dash="8 8"))
    g.append(_tline(x + 40, s0 + 40, "安全の手当て", 28, J.TICK, "start", 300))
    g.append(F.line(x + 40, s0 + 86, x + 220, s0 + 86, J.GRID, 7))
    return g


def plan_stage(prev, st):
    s = []
    x, w = PL["x"], PL["w"]
    s0, s1 = PL["sec"]
    for f_, cy, body in (("c91", 520.0, "十分でなかった"), ("s86", 700.0, "形だけ")):
        if _on(prev, st, f_):
            key = f_
            bx0, _y0, _bx1, _y1 = rep_box(1330.0, cy, key, body)
            s.append(_rep(1330.0, cy, key, body))
            s.append(_arrow(bx0 - 10, cy, x + w + 10, (s0 + s1) / 2 + (-30 if f_ == "c91" else 30), rep_col(key), 5, 22))
    return s


# ══════════════════════════════════════════════════════════
#  blame（c220）＝1992年の報告がいちばん強く責めたもの（S1 p34）：「計画そのもの」（薄い）／「計画を変えた」（赤い印）＋3つの札
# ══════════════════════════════════════════════════════════
BL_CHIPS = ("承認なし", "その場で", "わざと")
BL = dict(y=520.0, l=(520.0, 440.0), r=(1320.0, 560.0), h=140.0, cy=700.0)


def blame_base(st0):
    return []


def blame_stage(prev, st):
    s = []
    if _on(prev, st, "hdr"):
        s.append(_rep(CX, 330.0, "r92", "いちばん強く責めたもの"))
    if _on(prev, st, "plan"):
        x, w = BL["l"]
        s.append(_card(x, BL["y"], w, BL["h"], J.LINE_DIM, dash="12 10"))
        s.append(_tline(x, BL["y"] + 12, "計画そのもの", 36, J.TICK, "middle", w - 40))
        s.append(_tline(x, BL["y"] + BL["h"] / 2 + 44, "ではない", 28, J.TICK, "middle", 300))
    if _on(prev, st, "chg"):
        x, w = BL["r"]
        s.append(_card(x, BL["y"], w, BL["h"], J.ALERT, sw=7))
        s.append(_tline(x, BL["y"] + 14, "計画を変えた", 40, INK, "middle", w - 60))
        s.append(F.circ(x + w / 2 - 6, BL["y"] - BL["h"] / 2 + 6, 26, J.ALERT, J.BG, 4))
        for i, t in enumerate(BL_CHIPS):
            cx = x - 190 + i * 190
            s.append(_card(cx, BL["cy"], 170, 60, J.ALERT, sw=4))
            s.append(_tline(cx, BL["cy"] + 10, t, 28, J.ALERT, "middle", 150))
            s.append(F.line(cx, BL["y"] + BL["h"] / 2 + 4, cx, BL["cy"] - 34, J.ALERT, 3))
    return s


# ══════════════════════════════════════════════════════════
#  cut（c222）＝試験の計画の中の「非常用の冷却を切る」（1行目）→ 1986年のソ連の報告：試験のあいだ、炉の安全が大きく下がる（2行目＝帯）。
#  🔴 S3 の「約4時間」は札にしない（台本 §1-5＝言わない）＝時間の数を出さない
# ══════════════════════════════════════════════════════════
CT = dict(doc=(160.0, 330.0, 440.0, 440.0), ax=(800.0, 1720.0), y_hi=470.0, y_lo=690.0, base=800.0, band=(1080.0, 1480.0))


def cut_base(st0):
    return []


def cut_stage(prev, st):
    s = []
    if _on(prev, st, "item"):
        x, y, w, h = CT["doc"]
        s.append(F.rect(x, y, w, h, J.BG2, J.DOC, 4, rx=8))
        s.append(F.rect(x, y, w, 60, J.DOC_DIM, None, None, rx=8))
        s.append(_tline(x + w / 2, y + 44, "試験の計画", 30, INK, "middle", w - 40))
        # 試し焼き 39867368772：灰の行（y+292）が「非常用の冷却を切る」の字を横切った＝行は赤い枠（y+250〜320）の上と下だけ
        for i, dy in enumerate((100.0, 134.0, 168.0, 202.0, 360.0, 394.0)):
            s.append(F.line(x + 30, y + dy, x + w - 30 - 80 * (i % 2), y + dy, J.LINE_DIM, 9))
        s.append(F.rect(x + 16, y + 250, w - 32, 70, "none", J.ALERT, 5, rx=8))
        s.append(_tline(x + w / 2, y + 296, "非常用の冷却を切る", 30, J.ALERT, "middle", w - 60))
    if _on(prev, st, "band"):
        a, b = CT["ax"]
        b0, b1 = CT["band"]
        s.append(F.rect(b0, CT["y_hi"] - 40, b1 - b0, CT["base"] - CT["y_hi"] + 40, J.ALERT_DIM, None, None, op=0.45))
        s.append(F.line(a, CT["base"], b, CT["base"], J.TICK, 4))
        s.append(F.poly([(a, CT["y_hi"]), (b0, CT["y_hi"]), (b0 + 30, CT["y_lo"]), (b1, CT["y_lo"])], "none", J.OK, 7))
        s.append(F.line(b1, CT["y_lo"], b, CT["y_lo"], J.OK, 5, dash="10 10"))
        s.append(_tline(a, CT["y_hi"] - 26, "炉の安全", 28, J.OK, "start", 240))
        s.append(_tline((b0 + b1) / 2, CT["base"] + 46, "試験のあいだ", 28, J.ALERT, "middle", 300))
        s.append(_arrow(b0 + 200, CT["y_hi"] + 10, b0 + 200, CT["y_lo"] - 20, J.ALERT, 6, 24))
        s.append(_rep(1380.0, 330.0, "s86", "大きく下がる", cap=26))
    return s


# ══════════════════════════════════════════════════════════
#  site（c224）＝上から見た発電所の4つの号機（模式＝並びと形は正確ではない）→ 4号機に黄の輪「ここから」
# ══════════════════════════════════════════════════════════
SITE_UNITS = 4
SITE_MARK = 4
ST = dict(y=540.0, xs=(400.0, 720.0, 1040.0, 1360.0), s=220.0)


def site_base(st0):
    g = [F.rect(220.0, 330.0, 1270.0, 440.0, "none", J.LINE_DIM, 3, rx=16, dash="10 10")]     # 右の札（ここから）が枠の線を横切らない幅
    for i, x in enumerate(ST["xs"]):
        g.append(F.rect(x - ST["s"] / 2, ST["y"] - ST["s"] / 2, ST["s"], ST["s"], J.BG2, J.LINE, 4, rx=8))
        g.append(F.circ(x, ST["y"], 60, "#2b3a44", GRAPH, 4))
        g.append(_tline(x, ST["y"] + ST["s"] / 2 + 50, f"{i + 1}号機", 30, INK, "middle", 200))
    return g


def site_stage(prev, st):
    s = []
    if _on(prev, st, "mark"):
        x = ST["xs"][SITE_MARK - 1]
        s.append(F.rect(x - ST["s"] / 2 - 16, ST["y"] - ST["s"] / 2 - 16, ST["s"] + 32, ST["s"] + 32, "none", J.AMBER, 8, rx=14))
        s.append(_tline(1520.0, 470.0, "ここから", 40, J.AMBER, "start", 300))
        s.append(_tline(1520.0, 530.0, "4月25日", 32, J.AMBER, "start", 300))
        s.append(_tline(1520.0, 580.0, "出力を下げ始める", 26, INK, "start", 300))
        s.append(_arrow(1510.0, 500.0, x + ST["s"] / 2 + 22, ST["y"] - 30, J.AMBER, 5, 22))
    return s


# ══════════════════════════════════════════════════════════
#  dial（c301）＝出力の針（丸の計器・数なし＝右の端が最大の出力）→ 1:06 に下げ始める（針が少し左へ＝動く部品）→ 1986年の報告：1:00
# ══════════════════════════════════════════════════════════
DL_T, DL_T86 = "1:06", "1:00"
DL = dict(cx=640.0, cy=720.0, r=330.0, drop=-22.0)


def dial_base(st0):
    cx, cy, r = DL["cx"], DL["cy"], DL["r"]
    g = [F.poly(_arcpts(cx, cy, r, r, 180, 360, 36), "none", J.LINE, 8)]
    for k in range(11):
        a = math.radians(180 + 18 * k)
        g.append(F.line(cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a), J.TICK, 4))
    g.append(F.circ(cx, cy, 22, J.LINE, None))
    g.append(_tline(cx - r, cy + 50, "低い", 26, J.TICK, "middle", 160))
    g.append(_tline(cx + r, cy + 50, "最大の出力", 26, J.TICK, "middle", 220))
    g.append(_tline(cx, cy + 60, "4号炉の出力", 30, INK, "middle", 300))
    return g


def dial_parts(st):
    cx, cy, r = DL["cx"], DL["cy"], DL["r"]
    rot = DL["drop"] if st.get("clock") == "on" else 0.0
    L = r - 40
    needle = _P("needle", "poly", [(cx, cy - 7), (cx + L, cy - 2), (cx + L, cy + 2), (cx, cy + 7)], pivot=[cx, cy], rot=rot,
                fill=J.AMBER, stroke=J.AMBER, w=3, alpha=1.0)
    return [needle]


def dial_stage(prev, st):
    s = []
    if _on(prev, st, "clock"):
        s.append(_tline(1330.0, 400.0, "4月25日", 34, INK, "middle", 300))
        s.append(_bigtime(1330.0, 520.0, DL_T, 104))
        s.append(_tline(1330.0, 584.0, "下げ始め", 30, J.AMBER, "middle", 400))
        s.append(_arc_arrow(DL["cx"], DL["cy"], DL["r"] + 40, DL["r"] + 40, -6, -24, J.AMBER, 5, 20))
    if _on(prev, st, "r86"):
        s.append(_rep(1330.0, 730.0, "r86", DL_T86))
    return s


# ══════════════════════════════════════════════════════════
#  ruler（c302）＝横から見た炉と残した棒（模式）：差したまま残す棒（深さはまちまち）→ 物差し「残した棒」（目盛り 30・26・15＝S1 p89）。
#  目盛りの色は分けない（決まりの色分けは次の c303＝時刻表）
# ══════════════════════════════════════════════════════════
RL_TICKS = (30, 26, 15)
RL = dict(core=(240.0, 400.0, 780.0, 780.0), x=1260.0, y0=800.0, k=12.0, rods=((300.0, 0.30), (380.0, 0.75), (460.0, 0.15), (540.0, 0.55),
                                                                              (620.0, 0.90), (700.0, 0.40)))


def rl_y(v):
    return RL["y0"] - v * RL["k"]


def ruler_base(st0):
    x0, y0, x1, y1 = RL["core"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, "#2b3a44", GRAPH, 4, rx=8), _tline((x0 + x1) / 2, y1 + 50, "炉", 30, INK, "middle", 200)]


def ruler_stage(prev, st):
    s = []
    x0, y0, x1, y1 = RL["core"]
    if _on(prev, st, "rods"):
        for x, d in RL["rods"]:
            s.append(F.rect(x - 14, 300.0, 28, (y0 - 300.0) + (y1 - y0) * d, STEEL, J.BG, 3, rx=6))
        s.append(_tline(x1 + 30, 340.0, "差したまま残す制御棒", 28, STEEL, "start", 380))
    if _on(prev, st, "scale"):
        x = RL["x"]
        s.append(F.line(x, rl_y(0), x, rl_y(34), J.LINE, 6))
        for v in range(0, 35, 5):
            s.append(F.line(x, rl_y(v), x + 18, rl_y(v), J.TICK, 3))
        for v in RL_TICKS:
            s.append(F.line(x - 26, rl_y(v), x + 30, rl_y(v), J.LINE, 5))
            s.append(_tline(x + 46, rl_y(v) + 12, str(v), 34, INK, "start", 120, fam="Dela"))
        s.append(_arrow(x1 + 20, 560.0, x - 50, 560.0, J.AMBER, 6, 24))
        s.append(_card(1540.0, 560.0, 300, 120, J.AMBER, sw=6))
        s.append(_tline(1540.0, 556.0, "残した棒", 40, J.AMBER, "middle", 270))
        s.append(_tline(1540.0, 600.0, "（本ぶん）", 26, INK, "middle", 270))
    return s


# ══════════════════════════════════════════════════════════
#  orm（c306）＝25日の残した棒（表I-I の点＝1:06 31本・7:10 13.2本＝S1 p63）と 15本の線（すぐ止める＝S1 p89）。
#  点のあいだは直線（記録は点だけ）・15本を下にくぐる所を赤く → 2行目：1992年の報告が引く新しい報告「何時間も」
# ══════════════════════════════════════════════════════════
OR_PTS = (("1:06", 31.0), ("7:10", 13.2))
OR_LINE = 15.0
OR = dict(x0=260.0, x1=1660.0, y0=800.0, k=12.0, h=24.0)


def or_x(t):
    h, m = (int(v) for v in t.split(":"))
    return OR["x0"] + (OR["x1"] - OR["x0"]) * (h + m / 60.0) / OR["h"]


def or_y(v):
    return OR["y0"] - v * OR["k"]


def orm_base(st0):
    g = [F.line(OR["x0"], OR["y0"], OR["x1"], OR["y0"], J.TICK, 4), F.line(OR["x0"], OR["y0"], OR["x0"], or_y(35), J.TICK, 4)]
    g.append(_tline(OR["x0"] - 16, or_y(35) - 16, "残した棒（本ぶん）", 26, J.TICK, "start", 300))
    g.append(_tline(OR["x1"], OR["y0"] + 56, "25日 → 26日へ", 26, J.TICK, "end", 300))
    y = or_y(OR_LINE)
    g.append(F.line(OR["x0"], y, OR["x1"], y, J.ALERT, 4, dash="14 10"))
    g.append(_tline(OR["x1"], y - 16, "15本（すぐ止める）", 28, J.ALERT, "end", 340))
    return g


def orm_stage(prev, st):
    s = []
    if _on(prev, st, "pts"):
        (ta, va), (tb, vb) = OR_PTS
        xa, ya, xb, yb = or_x(ta), or_y(va), or_x(tb), or_y(vb)
        xc = xa + (xb - xa) * (va - OR_LINE) / (va - vb)        # 15本をくぐる所（直線の上）
        s.append(F.poly([(xc, or_y(OR_LINE)), (xb, yb), (xb, or_y(OR_LINE))], J.ALERT, None, close=True, op=0.5))
        s.append(F.line(xa, ya, xb, yb, J.AMBER, 5, dash="12 8"))
        for t, v, x, y, dx in ((ta, va, xa, ya, 40), (tb, vb, xb, yb, 40)):
            s.append(F.circ(x, y, 14, J.AMBER, J.BG, 4))
            s.append(F.line(x, y + 16, x, OR["y0"], J.LINE_DIM, 3, dash="6 6"))
            s.append(_tline(x, OR["y0"] + 44, t, 30, J.AMBER, "middle", 140, fam="Dela"))
            s.append(_tline(x + dx, y + 12, f"{v:g}本", 32, J.AMBER, "start", 200, fam="Dela"))
    if _on(prev, st, "r92"):
        bx0, _y0, _x1, by1 = rep_box(1250.0, 420.0, "r92", "が引く新しい報告：25日に何時間も")
        s.append(_rep(1250.0, 420.0, "r92", "が引く新しい報告：25日に何時間も"))
        (ta, va), (tb, vb) = OR_PTS
        # 試し焼き 39867368772：矢印の先が「13.2本」の字に重なった＝先は 15本の線をくぐる赤い三角（7:10 の点の左上）
        xc = or_x(ta) + (or_x(tb) - or_x(ta)) * (va - OR_LINE) / (va - vb)
        s.append(_arrow(1100.0, by1 + 6, (xc + or_x(tb)) / 2 + 6, or_y(OR_LINE) - 14, rep_col("r92"), 5, 22))
    return s


# ══════════════════════════════════════════════════════════
#  turbine（c307）＝2台のタービン（羽根の絵2つ）：13:05 7号を止める（灰・■）→ 試験に使う8号だけ（黄の輪）＝表I-I p63
# ══════════════════════════════════════════════════════════
TB_T = "13:05"
TB_STOP, TB_KEEP = 7, 8
TB = dict(y=560.0, xs=(600.0, 1320.0))


def turbine_base(st0):
    g = []
    for x, n in zip(TB["xs"], (TB_STOP, TB_KEEP)):
        g.append(_turbine(x, TB["y"], 1.15))
        g.append(_tline(x, TB["y"] + 150, f"{n}号タービン", 32, INK, "middle", 300))
    return g


def turbine_stage(prev, st):
    s = []
    if _on(prev, st, "stop7"):
        x = TB["xs"][0]
        s.append(F.rect(x - 220, TB["y"] - 110, 440, 220, J.BG, None, None, op=0.6))
        s.append(F.rect(x - 34, TB["y"] - 34, 68, 68, J.ALERT, None, None, rx=6))
        s.append(_bigtime(CX, 350.0, TB_T, 80))
        s.append(_tline(x, TB["y"] - 136, "止める", 34, J.ALERT, "middle", 200))
    if _on(prev, st, "keep8"):
        x = TB["xs"][1]
        s.append(F.rect(x - 230, TB["y"] - 120, 460, 240, "none", J.AMBER, 7, rx=16))
        s.append(_tline(x, TB["y"] - 140, "試験に使う", 34, J.AMBER, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  eccs（c308）＝横から見た非常用の冷却の仕組み（模式）：水の槽 → 管 → 弁 → 炉（事故のときに水を送り込む）→ 14:00 弁を閉じて切り離す（赤い×）
# ══════════════════════════════════════════════════════════
EC_T = "14:00"
EC = dict(tank=(200.0, 440.0, 400.0, 760.0), y=640.0, valve=(860.0, 640.0), core=(1280.0, 380.0, 1600.0, 800.0))


EC_N = 2           # 2つ目の「違反」（右上の札）


def eccs_base(st0):
    return [_badge(EC_N)]


def eccs_stage(prev, st):
    s = []
    x0, y0, x1, y1 = EC["tank"]
    vx, vy = EC["valve"]
    c0, c1, c2, c3 = EC["core"]
    if _on(prev, st, "sys"):
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, "#123a44", WATER, 5, rx=16))
        s.append(_tline((x0 + x1) / 2, y1 + 46, "水", 30, WATER, "middle", 200))
        s.append(F.rect(c0, c1, c2 - c0, c3 - c1, "#2b3a44", GRAPH, 4, rx=10))
        s.append(_tline((c0 + c2) / 2, c3 + 46, "炉", 30, INK, "middle", 200))
        s.append(F.line(x1, EC["y"], c0, EC["y"], WATER, 14))
        s.append(F.poly([(vx - 40, vy - 34), (vx + 40, vy + 34), (vx + 40, vy - 34), (vx - 40, vy + 34)], STEEL, J.BG, 4, close=True))
        s.append(_tline(vx, vy - 60, "弁", 28, STEEL, "middle", 120))
        for x in (560.0, 1080.0):
            s.append(_arrow(x - 40, EC["y"] - 40, x + 40, EC["y"] - 40, WATER, 5, 18))
        s.append(_tline(CX, 360.0, "非常用炉心冷却系", 40, WATER, "middle", 600))
        s.append(_tline(CX, 412.0, "事故のときに働く", 26, J.TICK, "middle", 600))
        s.append(_bigtime(1700.0, 345.0, EC_T, 64, anchor="end"))      # 炉の箱（上の端 380）の上
    if _on(prev, st, "cut"):
        s.append(F.line(vx + 50, EC["y"], c0 - 4, EC["y"], J.BG, 16, op=0.7))
        s.append(_xmark(vx, vy, 52, J.ALERT, 12))
        s.append(_tline(vx, vy + 110, "切り離す", 36, J.ALERT, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  stamp（c310）＝試験の手順の書類（模式）：1992年の報告＝技師長の承認があれば許されていた（印）→ 承認された一歩（✓）＝S1 p20
# ══════════════════════════════════════════════════════════
SP_ROW = 2          # 手順の行（0から）＝「非常用の冷却を切る」
SP = dict(x=360.0, y=300.0, w=560.0, h=520.0, rows=5)


def sp_row_y(i):
    return SP["y"] + 130 + i * 76


def stamp_base(st0):
    x, y, w, h = SP["x"], SP["y"], SP["w"], SP["h"]
    g = [F.rect(x, y, w, h, J.BG2, J.DOC, 4, rx=8), F.rect(x, y, w, 64, J.DOC_DIM, None, None, rx=8),
         _tline(x + w / 2, y + 46, "試験の手順", 32, INK, "middle", w - 40)]
    for i in range(SP["rows"]):
        yy = sp_row_y(i)
        g.append(F.txt(x + 34, yy + 10, f"{CIRC[i]}", 28, J.TICK, "Noto", "start"))
        if i == SP_ROW:
            g.append(_tline(x + 80, yy + 11, "非常用の冷却を切る", 30, INK, "start", w - 120))
        else:
            g.append(F.line(x + 80, yy, x + w - 40 - 60 * (i % 2), yy, J.LINE_DIM, 9))
    return g


def stamp_stage(prev, st):
    s = []
    if _on(prev, st, "stamp"):
        cx, cy = 1460.0, 580.0          # 3行目の「承認された一歩」（x 1020〜1260・y 560 前後）を印の丸が覆わない位置
        s.append(F.circ(cx, cy, 110, "none", J.OK, 8))
        s.append(_tline(cx, cy - 6, "技師長", 36, J.OK, "middle", 190))
        s.append(_tline(cx, cy + 40, "の承認", 30, J.OK, "middle", 190))
        s.append(_rep(1460.0, 360.0, "r92", "承認があれば許されていた", cap=26))
    if _on(prev, st, "step"):
        yy = sp_row_y(SP_ROW)
        s.append(F.rect(SP["x"] + 14, yy - 30, SP["w"] - 28, 54, "none", J.OK, 5, rx=8))
        s.append(_check(SP["x"] + SP["w"] + 50, yy - 4, 26, J.OK))
        s.append(_tline(SP["x"] + SP["w"] + 100, yy + 10, "承認された一歩", 34, J.OK, "start", 400))
    return s


# ══════════════════════════════════════════════════════════
#  off11（c311）＝非常用の冷却を切ったままの時間（14:00〈25日〉→ 事故・約11時間＝S1 p20）・半分の出力・計画の外 → 1992年の報告：安全文化の欠け
# ══════════════════════════════════════════════════════════
OF_T0, OF_H = "14:00", 11
OF = dict(x0=300.0, x1=1600.0, y=560.0, h=100.0)


def off11_base(st0):
    return []


def off11_stage(prev, st):
    s = []
    x0, x1, y, h = OF["x0"], OF["x1"], OF["y"], OF["h"]
    if _on(prev, st, "band"):
        s.append(F.line(x0 - 60, y + h / 2 + 30, x1 + 120, y + h / 2 + 30, J.TICK, 4))
        s.append(F.rect(x0, y - h / 2, x1 - x0, h, J.ALERT_DIM, J.ALERT, 4, rx=8))
        s.append(_tline((x0 + x1) / 2, y + 12, "非常用の冷却を切ったまま", 34, INK, "middle", x1 - x0 - 60))
        s.append(F.line(x0, y - h / 2 - 20, x0, y + h / 2 + 50, J.AMBER, 5))
        s.append(F.line(x1, y - h / 2 - 20, x1, y + h / 2 + 50, J.ALERT, 5))
        s.append(_tline(x0, y + h / 2 + 92, OF_T0, 36, J.AMBER, "middle", 200, fam="Dela"))
        s.append(_tline(x0, y + h / 2 + 132, "25日", 26, J.TICK, "middle", 200))
        s.append(_tline(x1, y + h / 2 + 92, "事故", 36, J.ALERT, "middle", 200))
        s.append(_tline(x1, y + h / 2 + 132, "26日", 26, J.TICK, "middle", 200))
        s.append(_tline((x0 + x1) / 2, y - h / 2 - 34, f"約{OF_H}時間・半分の出力", 40, J.AMBER, "middle", 900))
        s.append(_card(1690.0, 380.0, 220, 70, J.ALERT, sw=5))
        s.append(_tline(1690.0, 392.0, "計画の外", 32, J.ALERT, "middle", 190))
    if _on(prev, st, "r92"):
        s.append(_rep(CX, 790.0, "r92", "安全文化の欠け"))
    return s


# ══════════════════════════════════════════════════════════
#  grid3（c312）＝3つの報告の見方の表（列＝1986年の報告・1991年の委員会・1992年の報告／行＝違反か・事故に効いたか）。
#  1行目：違反か（1991年の委員会を太く）→ 2行目：違反かは割れる（黄の括弧）・効いていない＝3つとも同じ（緑の括弧）
# ══════════════════════════════════════════════════════════
G3_COLS = ("r86", "c91", "r92")
G3_ROW1 = ("安全の原則に反する", "運転の規則に反する", "承認で許されていた")
G3_ROW2 = "どれも、事故の進み方には効いていない"     # 3つの列にまたがる1枚（🔧 同じ字を3枚並べると門番 dup）
G3_ROWS = ("違反か", "事故に効いたか")
G3 = dict(xs=(620.0, 1040.0, 1460.0), w=390.0, hy=330.0, ys=(470.0, 650.0), h=110.0, lx=190.0)   # 🔧 門番 layout：「割れる」が右の外


def grid3_base(st0):
    g = []
    for k, key in enumerate(G3_COLS):
        g.append(_rep(G3["xs"][k], G3["hy"], key, w=G3["w"]))
    for i, t in enumerate(G3_ROWS):
        g.append(_tline(G3["lx"], G3["ys"][i] + 10, t, 30, J.TICK, "start", 220))
    return g


def grid3_stage(prev, st):
    s = []
    if _on(prev, st, "row1"):
        for k, (key, t) in enumerate(zip(G3_COLS, G3_ROW1)):
            x, y = G3["xs"][k], G3["ys"][0]
            s.append(_card(x, y, G3["w"], G3["h"], rep_col(key), sw=(8 if key == "c91" else 3)))
            s.append(_tline(x, y + 11, t, 30, INK, "middle", G3["w"] - 30))
    if _on(prev, st, "row2"):
        x0, x1 = G3["xs"][0] - G3["w"] / 2, G3["xs"][2] + G3["w"] / 2
        y = G3["ys"][1]
        s.append(F.rect(x0, y - G3["h"] / 2, x1 - x0, G3["h"], J.BG2, J.OK, 6, rx=10))
        s.append(_check(x0 + 70, y - 4, 28, J.OK))
        s.append(_tline((x0 + x1) / 2 + 40, y + 12, G3_ROW2, 36, J.OK, "middle", x1 - x0 - 200))
        s.append(F.poly([(x1 + 20, G3["ys"][0] - 50), (x1 + 36, G3["ys"][0] - 50), (x1 + 36, G3["ys"][0] + 50), (x1 + 20, G3["ys"][0] + 50)],
                        "none", J.AMBER, 4))
        s.append(_tline(x1 + 50, G3["ys"][0] + 12, "割れる", 30, J.AMBER, "start", 120))
    return s


# ══════════════════════════════════════════════════════════
#  trigger（c313）＝「非常用の冷却を切った」→ 事故の引き金の印から外れる（×）→ 同じ 14:00、試験は延期
# ══════════════════════════════════════════════════════════
TG_T = "14:00"


def trigger_base(st0):
    return []


def trigger_stage(prev, st):
    s = []
    if _on(prev, st, "cut"):
        s.append(_card(560.0, 450.0, 520, 110, WATER, sw=5))
        s.append(_tline(560.0, 462.0, "非常用の冷却を切った", 32, INK, "middle", 480))
        cx, cy = 1380.0, 450.0
        for r in (90, 60, 30):
            s.append(F.circ(cx, cy, r, "none", J.ALERT, 6))
        s.append(_tline(cx, cy + 140, "事故の引き金", 30, J.ALERT, "middle", 300))
        s.append(F.line(830.0, 450.0, 1280.0, 450.0, J.TICK, 4, dash="12 10"))
        s.append(_xmark(1055.0, 450.0, 36, J.ALERT, 10))
    if _on(prev, st, "post"):
        s.append(_bigtime(560.0, 730.0, TG_T, 64))
        s.append(_tline(560.0, 782.0, "同じ時刻", 24, J.TICK, "middle", 200))
        s.append(_card(1080.0, 712.0, 440, 100, J.AMBER, sw=5))
        s.append(_tline(1080.0, 724.0, "試験は延期", 36, J.AMBER, "middle", 400))
        s.append(_arrow(740.0, 712.0, 852.0, 712.0, J.AMBER, 5, 20))
    return s


# ══════════════════════════════════════════════════════════
#  kiev（c314）＝キエフの電力の指令所 → 発電所「待って」（矢印）→ 半分の出力のまま夜まで（月）＝表I-I p63
# ══════════════════════════════════════════════════════════
KV = dict(a=(400.0, 520.0), b=(1460.0, 520.0))


def _pylon(cx, cy, s=1.0, col=None):
    c = col or J.LINE
    return (F.poly([(cx - 40 * s, cy + 90 * s), (cx, cy - 90 * s), (cx + 40 * s, cy + 90 * s)], "none", c, 5)
            + F.line(cx - 60 * s, cy - 50 * s, cx + 60 * s, cy - 50 * s, c, 5) + F.line(cx - 46 * s, cy - 10 * s, cx + 46 * s, cy - 10 * s, c, 5))


def kiev_base(st0):
    ax, ay = KV["a"]
    bx, by = KV["b"]
    g = [F.rect(ax - 140, ay - 80, 200, 160, J.BG2, J.INST, 4, rx=8), _pylon(ax + 130, ay, 0.9, J.INST),
         _tline(ax - 10, ay + 140, "キエフの電力の指令所", 30, J.INST, "middle", 420),
         F.rect(bx - 150, by - 90, 300, 180, J.BG2, J.LINE, 4, rx=8), F.circ(bx, by, 56, "#2b3a44", GRAPH, 4),
         _tline(bx, by + 140, "4号炉", 30, INK, "middle", 300)]
    return g


def kiev_stage(prev, st):
    s = []
    ax, ay = KV["a"]
    bx, by = KV["b"]
    if _on(prev, st, "ask"):
        s.append(_arrow(ax + 200, ay, bx - 170, by, J.INST, 8, 30))
        s.append(_card(CX, ay - 90, 260, 80, J.INST, sw=5))
        s.append(_tline(CX, ay - 78, "待って", 40, J.INST, "middle", 220))
    if _on(prev, st, "night"):
        s.append(_tline(bx, by - 150, "半分の出力のまま", 32, J.AMBER, "middle", 360))
        s.append(_moon(bx + 220, by - 160, 34))
        s.append(_tline(bx + 220, by - 86, "夜まで", 26, INK, "middle", 160))     # 🔧 geom_gap：月に 3.9px＝下へ
    return s


# ══════════════════════════════════════════════════════════
#  ring（c316）＝25日の24時間の輪（上＝0時・時計回り）：14:00 → 23:10 の弧を赤く（約9時間＝S2 p1028）
# ══════════════════════════════════════════════════════════
RG_A, RG_B, RG_H = "14:00", "23:10", 9
RG = dict(cx=960.0, cy=540.0, r=200.0)    # 🔧 門番 layout：「正午」が出典の行と重なった＝輪を小さく上へ


def rg_deg(t):
    h, m = (int(v) for v in t.split(":"))
    return (h + m / 60.0) / 24.0 * 360.0 - 90.0


def ring_base(st0):
    cx, cy, r = RG["cx"], RG["cy"], RG["r"]
    g = [F.circ(cx, cy, r, "none", J.LINE_DIM, 26)]
    for k in range(24):
        a = math.radians(k * 15 - 90)
        L = 26 if k % 6 == 0 else 12
        g.append(F.line(cx + (r + 18) * math.cos(a), cy + (r + 18) * math.sin(a), cx + (r + 18 + L) * math.cos(a),
                        cy + (r + 18 + L) * math.sin(a), J.TICK, 4))
    g.append(_tline(cx, cy - r - 70, "真夜中", 26, J.TICK, "middle", 200))
    g.append(_tline(cx, cy + r + 80, "正午", 26, J.TICK, "middle", 200))
    g.append(_tline(cx - 560, cy - 180, "4月25日", 34, INK, "middle", 300))
    return g


def ring_stage(prev, st):
    s = []
    cx, cy, r = RG["cx"], RG["cy"], RG["r"]
    if _on(prev, st, "arc"):
        a0, a1 = rg_deg(RG_A), rg_deg(RG_B)
        s.append(F.poly(_arcpts(cx, cy, r, r, a0, a1, 40), "none", J.ALERT, 26))
        for t, a, dx, dy in ((RG_A, a0, -60, 10), (RG_B, a1, -150, 30)):      # 23:10 は上の「真夜中」の札をよける
            rad = math.radians(a)
            x, y = cx + (r + 120) * math.cos(rad), cy + (r + 90) * math.sin(rad)
            s.append(_tline(x + dx, y + dy, t, 40, J.AMBER, "middle", 220, fam="Dela"))
        s.append(_tline(cx, cy + 4, f"約{RG_H}時間", 52, J.AMBER, "middle", 300))
        s.append(_tline(cx, cy + 56, "止まっていた", 30, INK, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  day（c317）＝日めくり（4月25日 → 4月26日）と出力の線（ゆっくり下がる → 日付が変わってすぐ急に落ちる「？」＝数を出さない）
# ══════════════════════════════════════════════════════════
DY = dict(c25=(520.0, 420.0), c26=(1400.0, 420.0), w=300.0, h=200.0, ly=(600.0, 780.0), mid=960.0)   # 「真夜中」を出典の行から離す


def _daycard(cx, cy, t, col):
    w, h = DY["w"], DY["h"]
    return (F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 5, rx=10) + F.rect(cx - w / 2, cy - h / 2, w, 50, col, None, None, rx=10)
            + _tline(cx, cy - h / 2 + 38, "4月", 28, J.BG, "middle", 120) + _tline(cx, cy + 60, t, 80, col, "middle", 260, fam="Dela"))


def day_base(st0):
    y0, y1 = DY["ly"]
    return [F.line(DY["mid"], y0 - 20, DY["mid"], y1 + 10, J.TICK, 3, dash="8 8"), _tline(DY["mid"], y1 + 50, "真夜中", 26, J.TICK, "middle", 200)]


def day_stage(prev, st):
    s = []
    y0, y1 = DY["ly"]
    if _on(prev, st, "d25"):
        s.append(_daycard(*DY["c25"], "25日", INK))
        s.append(_moon(DY["c25"][0] + 230, DY["c25"][1] - 60, 30))
        s.append(F.poly([(260.0, y0 + 20), (DY["mid"], y0 + 70)], "none", J.AMBER, 6))
        s.append(_tline(260.0, y0 - 6, "出力を下げながら", 26, J.AMBER, "start", 320))
    if _on(prev, st, "d26"):
        s.append(_arrow(DY["c25"][0] + 170, DY["c25"][1], DY["c26"][0] - 170, DY["c26"][1], J.LINE, 6, 24))
        s.append(_daycard(*DY["c26"], "26日", J.AMBER))
        s.append(F.poly([(DY["mid"], y0 + 70), (DY["mid"] + 80, y0 + 82), (DY["mid"] + 120, y1 - 10)], "none", J.ALERT, 7))
        s.append(_qmark(DY["mid"] + 210, y0 + 130, 72, J.ALERT))
    return s


# ══════════════════════════════════════════════════════════
#  meter（c401）＝横の目盛り（0 → 3,200MW＝最大の出力）：0:05 の針 720MW（表I-I p63）→ 試験の予定 700〜1,000MW の帯（S3 p2020＝炉が出す熱）
# ══════════════════════════════════════════════════════════
MT_T, MT_V, MT_MAX = "0:05", 720.0, 3200.0
MT_PLAN = (700.0, 1000.0)
MT = dict(x0=240.0, x1=1680.0, y=600.0, h=44.0)


def mt_x(v):
    return MT["x0"] + (MT["x1"] - MT["x0"]) * v / MT_MAX


def meter_base(st0):
    x0, x1, y, h = MT["x0"], MT["x1"], MT["y"], MT["h"]
    g = [F.rect(x0, y - h / 2, x1 - x0, h, J.BG2, J.LINE, 4, rx=8)]
    for v in range(0, 3201, 400):
        g.append(F.line(mt_x(v), y + h / 2, mt_x(v), y + h / 2 + 16, J.TICK, 3))
    g.append(_tline(x0, y + h / 2 + 56, "0", 30, J.TICK, "middle", 80, fam="Dela"))
    g.append(_tline(x1, y + h / 2 + 56, "3,200MW", 30, J.TICK, "end", 260, fam="Dela"))
    g.append(_tline(x1, y + h / 2 + 96, "最大の出力", 24, J.TICK, "end", 260))
    g.append(_tline(x0, y - h / 2 - 24, "炉の出力", 28, INK, "start", 300))
    return g


def meter_stage(prev, st):
    s = []
    y, h = MT["y"], MT["h"]
    if _on(prev, st, "ptr"):
        x = mt_x(MT_V)
        s.append(F.rect(MT["x0"] + 4, y - h / 2 + 4, x - MT["x0"] - 4, h - 8, J.AMBER, None, None, rx=6, op=0.55))
        s.append(F.poly([(x, y - h / 2 - 6), (x - 18, y - h / 2 - 40), (x + 18, y - h / 2 - 40)], J.AMBER, None, close=True))
        s.append(_tline(x, y - h / 2 - 56, f"{MT_V:,.0f}MW", 48, J.AMBER, "middle", 300, fam="Dela"))
        s.append(_tline(1380.0, 370.0, "4月26日", 32, INK, "middle", 300))
        s.append(_bigtime(1380.0, 470.0, MT_T, 88))
    if _on(prev, st, "plan"):
        a, b = (mt_x(v) for v in MT_PLAN)
        s.append(F.rect(a, y - h / 2 - 2, b - a, h + 4, "none", J.OK, 6, rx=4))
        s.append(F.line(a, y + h / 2, a, y + h / 2 + 110, J.OK, 4))
        s.append(F.line(b, y + h / 2, b, y + h / 2 + 110, J.OK, 4))
        s.append(_tline(a - 8, y + h / 2 + 100, f"{MT_PLAN[0]:,.0f}", 30, J.OK, "end", 120, fam="Dela"))
        s.append(_tline(b + 8, y + h / 2 + 100, f"{MT_PLAN[1]:,.0f}", 30, J.OK, "start", 160, fam="Dela"))
        s.append(_tline(b + 8, y + h / 2 + 150, "試験の予定（炉が出す熱）", 30, J.OK, "start", 520))
    return s


# ══════════════════════════════════════════════════════════
#  clock（c402）＝時計 0:28（針と画面の時刻）＋切り替え（炉の部分ごと → 全体をまとめて）→ 出力が一気に落ちる（赤い下向きの矢印）
# ══════════════════════════════════════════════════════════
CK_T = "0:28"
CK = dict(cx=470.0, cy=520.0, r=210.0)


def ck_angles(t):
    h, m = (int(v) for v in t.split(":"))
    return (h % 12) * 30.0 + m * 0.5, m * 6.0


def _hand(cx, cy, ang, L, w, col):
    a = math.radians(ang)
    return F.line(cx, cy, cx + L * math.sin(a), cy - L * math.cos(a), col, w)


def clock_base(st0):
    cx, cy, r = CK["cx"], CK["cy"], CK["r"]
    g = [F.circ(cx, cy, r, J.BG2, J.LINE, 7)]
    for k in range(12):
        a = math.radians(k * 30)
        L = 30 if k % 3 == 0 else 16
        g.append(F.line(cx + (r - L) * math.sin(a), cy - (r - L) * math.cos(a), cx + (r - 8) * math.sin(a), cy - (r - 8) * math.cos(a), J.TICK, 5))
    ha, ma = ck_angles(CK_T)
    g.append(_hand(cx, cy, ha, r * 0.52, 12, INK))
    g.append(_hand(cx, cy, ma, r * 0.82, 7, J.AMBER))
    g.append(F.circ(cx, cy, 12, J.AMBER, None))
    g.append(_bigtime(cx, cy + r + 104, CK_T, 80))
    return g


def clock_stage(prev, st):
    s = []
    if _on(prev, st, "sw"):
        for i in range(3):
            for j in range(3):
                s.append(F.rect(940.0 + i * 64, 330.0 + j * 64, 52, 52, J.BG2, J.LINE, 4, rx=6))
        s.append(_tline(1036.0, 560.0, "炉の部分ごと", 28, INK, "middle", 260))
        s.append(_arrow(1170.0, 426.0, 1330.0, 426.0, J.AMBER, 7, 28))
        s.append(F.rect(1360.0, 330.0, 192, 192, J.BG2, J.LINE, 5, rx=10))
        s.append(_tline(1456.0, 560.0, "全体をまとめて", 28, INK, "middle", 300))
        s.append(_tline(1250.0, 300.0, "出力を保つ自動の仕組み", 26, J.TICK, "middle", 520))
    if _on(prev, st, "drop"):
        s.append(F.poly([(920.0, 650.0), (1240.0, 650.0), (1290.0, 820.0)], "none", J.ALERT, 7))
        s.append(_arrow(1290.0, 700.0, 1290.0, 830.0, J.ALERT, 12, 34))
        s.append(_tline(1340.0, 760.0, "一気に落ちる", 40, J.ALERT, "start", 420))
    return s


# ══════════════════════════════════════════════════════════
#  hold（c404）＝③（右上の違反の札）・1986年の報告「運転員の誤り」→ 出力を保つ指示（ボタン「保つ」）を入れなかった（×）
# ══════════════════════════════════════════════════════════
HD_N = 3


def hold_base(st0):
    return [_badge(HD_N)]


def hold_stage(prev, st):
    s = []
    if _on(prev, st, "r86"):
        s.append(_rep(560.0, 520.0, "r86", "運転員の誤り", cap=32))
    if _on(prev, st, "cmd"):
        s.append(_arrow(800.0, 520.0, 960.0, 520.0, J.LINE, 6, 24))
        cx, cy = 1320.0, 520.0
        s.append(_card(cx, cy, 600, 260, J.LINE, sw=4))
        s.append(F.rect(cx - 230, cy - 80, 160, 100, J.BG, J.OK, 6, rx=14))
        s.append(_tline(cx - 150, cy - 18, "保つ", 34, J.OK, "middle", 140))
        s.append(_xmark(cx - 70, cy - 76, 26))
        s.append(_tline(cx + 40, cy - 30, "出力を保つ指示", 30, INK, "start", 260))
        s.append(_tline(cx - 260, cy + 92, "切り替えのときに入れなかった", 30, J.ALERT, "start", 540))
    return s


# ══════════════════════════════════════════════════════════
#  swap（c406）＝札の入れ替え：1986年の報告「運転員の誤り」（左）→ 書き直し → 1992年の報告「誤りと言えるもの：無かったようだ」（右）
# ══════════════════════════════════════════════════════════
def swap_base(st0):
    return []


def swap_stage(prev, st):
    s = []
    if _on(prev, st, "r86"):
        s.append(_rep(500.0, 520.0, "r86", "運転員の誤り", cap=34, w=560))
    if _on(prev, st, "r92"):
        s.append(F.rect(220.0, 454.0, 560, 132, J.BG, None, None, op=0.45))
        s.append(_arrow(800.0, 520.0, 1060.0, 520.0, rep_col("r92"), 8, 30))
        s.append(_tline(930.0, 480.0, "書き直し", 28, rep_col("r92"), "middle", 220))
        s.append(_rep(1420.0, 520.0, "r92", "誤りと言えるもの：無かったようだ", cap=30, w=620))
    return s


# ══════════════════════════════════════════════════════════
#  two91（c407）＝1991年の委員会の見方（INSAG-7 p21 が引く）：原因＝確かめられない（虫めがね「？」）・出力＝保てなかった（揺れる針）
# ══════════════════════════════════════════════════════════
def two91_base(st0):
    return [_rep(CX, 330.0, "c91")]


def two91_stage(prev, st):
    s = []
    if _on(prev, st, "cause"):
        cx, cy = 560.0, 570.0
        s.append(_card(cx, cy, 560, 300, rep_col("c91"), sw=4))
        s.append(F.circ(cx - 140, cy - 30, 60, "none", INK, 8))
        s.append(F.line(cx - 98, cy + 12, cx - 50, cy + 60, INK, 12))
        s.append(_qmark(cx - 140, cy - 30, 60, J.AMBER))
        s.append(_tline(cx + 30, cy - 40, "原因", 34, INK, "start", 220))
        s.append(_tline(cx + 30, cy + 10, "確かめられない", 30, J.AMBER, "start", 230))
    if _on(prev, st, "ctrl"):
        cx, cy = 1360.0, 570.0
        s.append(_card(cx, cy, 560, 300, rep_col("c91"), sw=4))
        s.append(F.poly(_arcpts(cx - 140, cy + 30, 90, 90, 200, 340, 20), "none", J.LINE, 6))
        for a in (-60, -100, -80):
            t = math.radians(a)
            s.append(F.line(cx - 140, cy + 30, cx - 140 + 80 * math.cos(t), cy + 30 + 80 * math.sin(t), J.ALERT, 4, op=(1.0 if a == -80 else 0.4)))
        s.append(_tline(cx + 30, cy - 40, "出力", 34, INK, "start", 220))
        s.append(_tline(cx + 30, cy + 10, "保てなかった", 30, J.ALERT, "start", 230))
    return s


# ══════════════════════════════════════════════════════════
#  letter（c408）＝私信の封筒（運転担当の元副技師長から）→ 開いた手紙：自動の仕組みが正しく働かなかった（歯車に×）＝S1 p21（1992年の報告が引く）
# ══════════════════════════════════════════════════════════
def letter_base(st0):
    return []


def letter_stage(prev, st):
    s = []
    if _on(prev, st, "env"):
        x, y, w, h = 300.0, 400.0, 460.0, 290.0
        s.append(F.rect(x, y, w, h, J.BG2, J.DOC, 5, rx=8))
        s.append(F.poly([(x, y), (x + w / 2, y + h * 0.55), (x + w, y)], "none", J.DOC, 5))
        s.append(_tline(x + w / 2, y - 26, "差出人：元副技師長", 30, J.DOC, "middle", 520))     # 🔧 門番 echo：語りの写し（83%）
        s.append(_card(x + w / 2, y + h + 56, 140, 56, J.DOC, sw=4))
        s.append(_tline(x + w / 2, y + h + 66, "私信", 30, J.DOC, "middle", 120))
    if _on(prev, st, "open"):
        x, y, w, h = 1000.0, 360.0, 620.0, 380.0
        s.append(_arrow(800.0, 545.0, 960.0, 545.0, J.DOC, 6, 24))
        s.append(F.rect(x, y, w, h, J.BG2, J.DOC, 4, rx=6))
        for i in range(5):
            yy = y + 50 + i * 40
            if i != 2:
                s.append(F.line(x + 40, yy, x + w - 40 - 80 * (i % 2), yy, J.LINE_DIM, 8))
        s.append(_gear(x + 90, y + 290, 46))
        s.append(_xmark(x + 90, y + 290, 30))
        s.append(_tline(x + 160, y + 284, "自動の仕組み", 30, INK, "start", 420))
        s.append(_tline(x + 160, y + 330, "正しく働かなかった", 30, J.ALERT, "start", 420))
        s.append(_rep(1310.0, 810.0, "r92", None, cap=24))
    return s


# ══════════════════════════════════════════════════════════
#  docline（c409）＝1991年の委員会の報告の本文（模式）：1行に赤い下線「上級の運転員　素早く直せず」（S1 p73）→ 同じ報告に2つの言い方（括弧）
# ══════════════════════════════════════════════════════════
DLN = dict(x=300.0, y=300.0, w=760.0, h=520.0, ya=430.0, yb=640.0)


def docline_base(st0):
    x, y, w, h = DLN["x"], DLN["y"], DLN["w"], DLN["h"]
    col = rep_col("c91")
    g = [F.rect(x, y, w, h, J.BG2, col, 5, rx=8), F.rect(x, y, w, 64, J.INST_DIM, None, None, rx=8),
         _tline(x + w / 2, y + 46, "委員会の報告書（付属書I）", 30, INK, "middle", w - 40)]     # 🔧 門番 echo：語りの写し（86%）＝色で1991年の委員会
    for yy in (380.0, 480.0, 530.0, 580.0, 690.0, 740.0):
        g.append(F.line(x + 40, yy, x + w - 40 - 120 * (int(yy) % 3 == 0), yy, J.LINE_DIM, 9))
    g.append(_tline(x + 40, DLN["ya"] + 10, "原因は確かめられない", 28, J.TICK, "start", w - 80))
    return g


def docline_stage(prev, st):
    s = []
    x, w = DLN["x"], DLN["w"]
    if _on(prev, st, "hl"):
        s.append(_tline(x + 40, DLN["yb"] + 10, "上級の運転員が　素早く直せず", 32, INK, "start", w - 80))
        s.append(F.line(x + 40, DLN["yb"] + 26, x + w - 60, DLN["yb"] + 26, J.ALERT, 6))
    if _on(prev, st, "two"):
        bx = x + w + 30
        s.append(F.poly([(bx, DLN["ya"]), (bx + 30, DLN["ya"]), (bx + 30, DLN["yb"]), (bx, DLN["yb"])], "none", J.AMBER, 5))
        s.append(_tline(bx + 56, (DLN["ya"] + DLN["yb"]) / 2 - 10, "同じ報告に", 32, J.AMBER, "start", 360))
        s.append(_tline(bx + 56, (DLN["ya"] + DLN["yb"]) / 2 + 40, "2つの言い方", 36, J.AMBER, "start", 360))
    return s


# ══════════════════════════════════════════════════════════
#  say3（c410）＝同じ急落に3つの言い方（1986年の報告・元副技師長の私信・1991年の委員会の本文）→ 出力は 200MW まで戻って止まる（1時ごろ）→
#  それ以上は上がらない（点線の天井と×）。🔴 200MW の時刻は「1時ごろ」（1:00 と 1:03 で割れる＝台本 §1-5）
# ══════════════════════════════════════════════════════════
S3_CARDS = (("r86", "運転員の誤り"), ("letter", "仕組みが働かず"), ("c91", "素早く直せず"))
S3_V, S3_T = 200, "1時ごろ"
S3 = dict(y=410.0, xs=(420.0, 960.0, 1500.0), w=460.0, h=108.0, gx=(300.0, 1600.0), gy0=780.0, gk=0.75)   # 「1時ごろ」を出典の行から離す


def say3_base(st0):
    return []


def say3_stage(prev, st):
    s = []
    if _on(prev, st, "cards"):
        for (key, t), x in zip(S3_CARDS, S3["xs"]):
            if key == "letter":
                s.append(_card(x, S3["y"], S3["w"], S3["h"], J.DOC, sw=5))
                s.append(_tline(x, S3["y"] - 12, "元副技師長の私信", 26, J.DOC, "middle", S3["w"] - 30))
                s.append(_tline(x, S3["y"] + 34, t, 30, INK, "middle", S3["w"] - 30))
            else:
                s.append(_rep(x, S3["y"], key, t, cap=26, w=S3["w"]))
        s.append(_tline(CX, 316.0, "0時28分の急落に", 28, J.TICK, "middle", 400))
    gx0, gx1 = S3["gx"]
    yv = S3["gy0"] - S3_V * S3["gk"]
    if _on(prev, st, "p200"):
        s.append(F.line(gx0, S3["gy0"], gx1, S3["gy0"], J.TICK, 3))
        s.append(F.poly([(gx0, S3["gy0"] - 20), (gx0 + 300, S3["gy0"] - 14), (gx0 + 700, yv), (gx1, yv)], "none", J.AMBER, 6))
        s.append(F.circ(gx0 + 700, yv, 10, J.AMBER, None))
        s.append(_tline(gx0 + 700, S3["gy0"] + 40, S3_T, 28, J.AMBER, "middle", 200))
        s.append(_tline(gx1, yv + 44, f"{S3_V}MW", 36, J.AMBER, "end", 200, fam="Dela"))
    if _on(prev, st, "cap"):
        s.append(F.line(gx0 + 700, yv - 46, gx1, yv - 46, J.ALERT, 4, dash="12 10"))
        s.append(_arrow(gx0 + 1000, yv - 10, gx0 + 1000, yv - 80, J.ALERT, 5, 18))
        s.append(_xmark(gx0 + 1000, yv - 46, 18, J.ALERT, 6))
        s.append(_tline(gx0 + 1040, yv - 66, "上がらない", 30, J.ALERT, "start", 240))
    return s


# ══════════════════════════════════════════════════════════
#  bars（c412）＝熱出力の棒（同じ縮尺・色を多く）：3,200 最大の出力・1,600 25日の朝・700 試験の予定の下の端・200 1時ごろ・30 0時28分（を下回る）
#  → 700MW の線（1行目＝④）→ 1986年の報告：ふだんの安全の手順で禁止（2行目＝帰属つき）
# ══════════════════════════════════════════════════════════
BR_ROWS = (("最大の出力", 3200, "LINE", "3,200MW"), ("25日 4時前", 1600, "ship", "1,600MW"), ("試験の予定の下の端", 700, "OK", "700MW"),
           ("その夜 1時ごろ", 200, "AMBER", "200MW"), ("0時28分", 30, "ALERT", "30MW を下回る"))
BR_N = 4
BR = dict(x0=600.0, x1=1560.0, vmax=3200.0, y0=330.0, dy=92.0, h=56.0)   # 🔧 門番 layout：「3,200MW」が右の外


def br_x(v):
    return BR["x0"] + (BR["x1"] - BR["x0"]) * v / BR["vmax"]


def bars_base(st0):
    return [_badge(BR_N)]


def bars_stage(prev, st):
    s = []
    if _on(prev, st, "bars"):
        for i, (t, v, r, lab) in enumerate(BR_ROWS):
            y = BR["y0"] + i * BR["dy"]
            s.append(F.rect(BR["x0"], y - BR["h"] / 2, max(br_x(v) - BR["x0"], 4), BR["h"], rc(r), None, None, rx=4))
            s.append(_tline(BR["x0"] - 20, y + 11, t, 28, INK, "end", 400))
            # 700MW の破線より短い棒の値の札は破線の右へ（破線が字を貫かない）
            s.append(_tline(max(br_x(v), br_x(700)) + 16, y + 11, lab, 28, rc(r) if r != "LINE" else INK, "start", 420))
        x = br_x(700)
        yb = BR["y0"] + 4 * BR["dy"] + 60
        s.append(F.line(x, BR["y0"] - 40, x, yb, J.OK, 4, dash="10 8"))
        s.append(_tline(x, yb + 40, "この線より下", 30, J.OK, "middle", 520))          # 🔧 門番 echo：語りの写し（83%）
    if _on(prev, st, "r86"):
        s.append(_rep(1420.0, 780.0, "r86", "線の下は「禁止」", cap=26))                 # 🔧 門番 echo：語りの写し（100%）＝帰属の札の中だけ
    return s


# ══════════════════════════════════════════════════════════
#  page86（c414）＝1986年の報告の頁（模式＝頁の絵は使わない）：ソ連の専門家の口頭の説明 → 頁の「禁止」の強調 → 1992年の報告「強調は当たらない」
# ══════════════════════════════════════════════════════════
PG = dict(x=520.0, y=330.0, w=480.0, h=500.0, yk=560.0)


def page86_base(st0):
    x, y, w, h = PG["x"], PG["y"], PG["w"], PG["h"]
    col = rep_col("r86")
    g = [F.rect(x, y, w, h, J.BG2, col, 5, rx=8), _tline(x + w / 2, y + 48, "1986年の報告", 30, col, "middle", w - 40)]
    for yy in (420.0, 470.0, 510.0, 620.0, 670.0, 720.0, 770.0):
        g.append(F.line(x + 40, yy, x + w - 40 - 100 * (int(yy) % 4 == 0), yy, J.LINE_DIM, 9))
    return g


def page86_stage(prev, st):
    s = []
    x, w = PG["x"], PG["w"]
    if _on(prev, st, "oral"):
        s.append(_card(250.0, 420.0, 300, 140, J.LINE, sw=4))
        s.append(F.poly([(320.0, 490.0), (300.0, 530.0), (360.0, 490.0)], J.BG2, J.LINE, 4, close=True))
        s.append(_tline(250.0, 410.0, "口頭の説明", 30, INK, "middle", 260))
        s.append(_tline(250.0, 452.0, "（ソ連の専門家）", 24, J.TICK, "middle", 260))
        s.append(_arrow(400.0, 450.0, x - 10, 520.0, J.LINE, 5, 20))
        s.append(F.rect(x + 30, PG["yk"] - 34, 150, 52, rep_col("r86"), None, None, rx=6, op=0.35))
        s.append(_tline(x + 105, PG["yk"] + 4, "禁止", 34, INK, "middle", 130))
    if _on(prev, st, "r92"):
        s.append(_rep(1420.0, PG["yk"], "r92", "強調は当たらない", cap=30))
        bx0, *_r = rep_box(1420.0, PG["yk"], "r92", "強調は当たらない", cap=30)
        s.append(_arrow(bx0 - 10, PG["yk"], x + 200, PG["yk"] - 8, rep_col("r92"), 5, 22))
    return s


# ══════════════════════════════════════════════════════════
#  limit（c415）＝事故の前（下限の線なし）／事故のあと（700MW の線＝ふだんの運転の下限＝S1 p38）→ 1992年の報告「禁止は、あるべきだった」（S1 p28）
# ══════════════════════════════════════════════════════════
LM_V, LM_MAX = 700.0, 3200.0
LM = dict(xa=(300.0, 860.0), xb=(1080.0, 1640.0), y0=780.0, y1=420.0)     # 下の札（事故の前・あと）を出典の行から離す


def lm_y(v):
    return LM["y0"] - (LM["y0"] - LM["y1"]) * v / LM_MAX


def limit_base(st0):
    g = []
    for (a, b), t in ((LM["xa"], "事故の前"), (LM["xb"], "事故のあと")):
        g.append(F.rect(a, LM["y1"], b - a, LM["y0"] - LM["y1"], J.BG2, J.LINE_DIM, 3, rx=8))
        g.append(_tline((a + b) / 2, LM["y0"] + 46, t, 30, INK, "middle", 300))
        g.append(_tline(a + 16, LM["y1"] + 40, "出力", 24, J.TICK, "start", 120))
    a, b = LM["xa"]
    g.append(F.line(a + 20, lm_y(LM_V), b - 20, lm_y(LM_V), J.TICK, 3, dash="8 10"))
    g.append(_tline((a + b) / 2, lm_y(LM_V) - 20, "下限の線なし", 28, J.TICK, "middle", 400))
    return g


def limit_stage(prev, st):
    s = []
    if _on(prev, st, "r92"):
        s.append(_rep(CX, 330.0, "r92", "禁止は、あるべきだった"))
    if _on(prev, st, "after"):
        a, b = LM["xb"]
        y = lm_y(LM_V)
        s.append(F.rect(a + 4, y, b - a - 8, LM["y0"] - y - 4, J.ALERT_DIM, None, None, op=0.5))
        s.append(F.line(a + 4, y, b - 4, y, J.OK, 8))
        s.append(_tline((a + b) / 2, y - 22, f"{LM_V:,.0f}MW　ふだんの運転の下限", 30, J.OK, "middle", b - a - 30))
    return s


# ══════════════════════════════════════════════════════════
#  pillars（c416）＝3つの書類（設計・規制・運転の指示書）＝どれにも「禁止なし」（空の破線の枠）→ 1991年の委員会も同じ見方（S1 p87）
# ══════════════════════════════════════════════════════════
PL3 = ("設計", "規制", "運転の指示書")
PL_EMPTY = "どれにも、禁止の項目なし"     # 🔧 各書類に同じ札を3枚描くと門番 dup＝空の破線の枠（字なし）＋下に1枚
PLR = dict(xs=(480.0, 960.0, 1440.0), y0=300.0, w=330.0, h=300.0, by=620.0)


def pillars_base(st0):
    g = []
    for x, t in zip(PLR["xs"], PL3):
        g.append(_doc(x - PLR["w"] / 2, PLR["y0"], PLR["w"], PLR["h"], J.DOC, nlines=2, top=110.0, gap=40.0))
        g.append(_tline(x, PLR["y0"] + 60, t, 34, J.DOC, "middle", PLR["w"] - 30))
        g.append(F.rect(x - 120, PLR["y0"] + 190, 240, 70, "none", J.TICK, 3, rx=8, dash="8 8"))
    x0, x1 = PLR["xs"][0] - PLR["w"] / 2, PLR["xs"][2] + PLR["w"] / 2
    g.append(F.poly([(x0, PLR["by"]), (x0, PLR["by"] + 16), (x1, PLR["by"] + 16), (x1, PLR["by"])], "none", J.TICK, 4))
    g.append(_tline(CX, PLR["by"] + 64, PL_EMPTY, 32, J.TICK, "middle", 700))
    return g


def pillars_stage(prev, st):
    s = []
    if _on(prev, st, "c91"):
        s.append(_rep(CX, 780.0, "c91", "も、事故の前は同じ見方"))
    return s


# ══════════════════════════════════════════════════════════
#  inst（c417）＝横から見た炉と計器（模式）：炉の中の計器＝低い出力では使えない（×）・外の計器＝どれも炉の真ん中の高さ（S1 p15）→
#  上と下は見えない（？）・1992年の報告：経験と勘に頼る
# ══════════════════════════════════════════════════════════
IN = dict(core=(780.0, 320.0, 1140.0, 790.0), ins=(380.0, 470.0, 560.0, 650.0, 740.0), out=(700.0, 1220.0))   # 「炉」の札を出典の行から離す


def in_mid():
    return (IN["core"][1] + IN["core"][3]) / 2


def inst_base(st0):
    x0, y0, x1, y1 = IN["core"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, "#2b3a44", GRAPH, 4, rx=8), _tline((x0 + x1) / 2, y1 + 44, "炉", 28, INK, "middle", 200)]


def inst_stage(prev, st):
    s = []
    x0, y0, x1, y1 = IN["core"]
    xm, ym = (x0 + x1) / 2, in_mid()
    if _on(prev, st, "det"):
        s.append(F.line(xm, y0 + 30, xm, y1 - 10, J.LINE_DIM, 4))
        for yy in IN["ins"]:
            s.append(F.rect(xm - 14, yy - 14, 28, 28, J.LINE_DIM, None, None, rx=4))
            s.append(_xmark(xm, yy, 12, J.ALERT, 4))
        s.append(_tline(x0 - 30, 380.0, "炉の中の計器", 28, INK, "end", 360))
        s.append(_tline(x0 - 30, 420.0, "低い出力では使えない", 26, J.ALERT, "end", 360))
        for x in IN["out"]:
            side = -1 if x < xm else 1
            s.append(F.rect(x - 22, ym - 22, 44, 44, J.AMBER, None, None, rx=6))
            s.append(F.poly([(x, ym), (x - side * 90, ym - 100), (x - side * 90, ym + 100)], J.AMBER, None, close=True, op=0.22))
        s.append(_tline(IN["out"][1] + 50, ym + 10, "外の計器", 30, J.AMBER, "start", 320))
        s.append(_tline(IN["out"][1] + 50, ym + 52, "（どれも真ん中の高さ）", 24, J.AMBER, "start", 320))
    if _on(prev, st, "blind"):
        for yy in (y0 + 70, y1 - 70):
            s.append(_qmark(x1 + 120, yy, 56, J.AMBER))
            s.append(F.line(x1 + 10, yy - 22, x1 + 80, yy - 22, J.TICK, 3, dash="6 6"))
        s.append(_tline(x1 + 160, in_mid() - 160, "上と下は見えない", 26, J.TICK, "start", 300))
        s.append(_rep(400.0, 760.0, "r92", "経験と勘に頼る", cap=26))
    return s


# ══════════════════════════════════════════════════════════
#  thermo（c420）＝炉の入口の水の温度計（模式＝数なし）：出力が低い＋水の流れが増える（ポンプ8台）→ 沸く温度のすぐ手前（S1 p18）→
#  1992年の報告：事故の条件の1つ
# ══════════════════════════════════════════════════════════
TH = dict(x=960.0, top=330.0, bot=760.0, boil=400.0, lvl=430.0)


def thermo_base(st0):
    x, top, bot = TH["x"], TH["top"], TH["bot"]
    g = [F.rect(x - 34, top, 68, bot - top, J.BG2, J.LINE, 5, rx=34), F.circ(x, bot + 34, 58, J.BG2, J.LINE, 5)]
    g.append(F.line(x - 120, TH["boil"], x + 120, TH["boil"], J.ALERT, 5, dash="12 8"))
    g.append(_tline(x + 140, TH["boil"] + 10, "沸く温度", 30, J.ALERT, "start", 300))
    g.append(_tline(x + 140, bot + 44, "炉の入口の水", 30, INK, "start", 300))
    return g


def thermo_stage(prev, st):
    s = []
    x, bot = TH["x"], TH["bot"]
    if _on(prev, st, "rise"):
        s.append(F.circ(x, bot + 34, 44, WATER, None))
        s.append(F.rect(x - 18, TH["lvl"], 36, bot - TH["lvl"] + 20, WATER, None, None, rx=18))
        s.append(F.poly([(x + 60, TH["boil"] + 4), (x + 74, TH["boil"] + 4), (x + 74, TH["lvl"]), (x + 60, TH["lvl"])], "none", J.AMBER, 4))
        s.append(_tline(x + 140, TH["lvl"] + 26, "沸く寸前", 30, J.AMBER, "start", 300))
        for cy, t in ((470.0, "出力が低い"), (640.0, "水の流れが増える（ポンプ8台）")):
            s.append(_card(500.0, cy, 520, 90, J.LINE, sw=4))
            s.append(_tline(500.0, cy + 10, t, 28, INK, "middle", 480))
            s.append(_arrow(770.0, cy, x - 70, (cy + TH["lvl"] + 120) / 2, J.LINE, 5, 20))
    if _on(prev, st, "r92"):
        s.append(_rep(1450.0, 640.0, "r92", "事故の条件の1つ", cap=28))
    return s


# ══════════════════════════════════════════════════════════
#  balance（c421）＝1991年の委員会の2つの見方を天秤に（S1 p87〜88）：一部のポンプの流れすぎ＝違反（赤）／8台のポンプ＝暴走を妨げたかも（緑）→
#  見方は割れる（天秤は水平＝どちらに寄せない）
# ══════════════════════════════════════════════════════════
BA_L = ("一部のポンプ", "流れすぎ＝違反")
BA_R = ("8台のポンプ", "暴走を妨げたかも")
BA = dict(cx=960.0, beam=470.0, xl=520.0, xr=1400.0, pan=600.0, base=770.0)   # 「見方は割れる」を出典の行から離す


def balance_base(st0):
    cx, by = BA["cx"], BA["beam"]
    g = [_rep(cx, 316.0, "c91"),
         F.poly([(cx, by + 10), (cx - 70, BA["base"]), (cx + 70, BA["base"])], J.BG2, J.LINE, 5, close=True),
         F.line(BA["xl"], by, BA["xr"], by, J.LINE, 8), F.circ(cx, by, 14, J.LINE, None)]
    for x in (BA["xl"], BA["xr"]):
        g.append(F.line(x, by, x - 110, BA["pan"] - 64, J.TICK, 3))
        g.append(F.line(x, by, x + 110, BA["pan"] - 64, J.TICK, 3))
    return g


def balance_stage(prev, st):
    s = []
    for f_, x, (a, b), col in (("left", BA["xl"], BA_L, J.ALERT), ("right", BA["xr"], BA_R, J.OK)):
        if _on(prev, st, f_):
            s.append(_card(x, BA["pan"], 400, 128, col, sw=6))
            s.append(_tline(x, BA["pan"] - 12, a, 30, INK, "middle", 360))
            s.append(_tline(x, BA["pan"] + 36, b, 30, col, "middle", 360))
    if _on(prev, st, "split"):
        s.append(_tline(BA["cx"], BA["base"] + 50, "見方は割れる", 34, J.AMBER, "middle", 400))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表（mech17 と同じ作り）
# ══════════════════════════════════════════════════════════
def _v(lab, fields, base, stage, parts=None):
    d = dict(lab=lab, fields={f_: ONOFF for f_ in fields}, base=base, stage=stage)
    if parts:
        d["parts"] = parts
    return d


VIEWS = dict(
    years=_v("報告の年表", ("s86", "r86", "c91", "r92", "arc"), years_base, years_stage),
    cards7=_v("7つの札（時刻の順）", ("cards", "ask"), cards7_base, cards7_stage),
    neutron=_v("横から見た粒（中性子と黒鉛）", ("power", "chain"), neutron_base, neutron_stage),   # PLAN の見る向き＝横から（c208 と同じ向き）
    void=_v("水・泡・中性子の輪", ("tube", "n12", "n34", "name"), void_base, void_stage),
    power20=_v("出力の目盛りと炉の性質", ("low", "loop"), power20_base, power20_stage),
    flow4=_v("試験の流れ", ("cut", "chain", "test"), flow4_base, flow4_stage),
    decay=_v("横から見た燃料の管（1本）", ("heat", "pump"), decay_base, decay_stage),
    cal=_v("試験の暦", ("y82", "y8485", "y83", "y86"), cal_base, cal_stage),
    plan=_v("計画の書類", ("c91", "s86"), plan_base, plan_stage),
    blame=_v("責めの比べ", ("hdr", "plan", "chg"), blame_base, blame_stage),
    cut=_v("計画の中身と安全", ("item", "band"), cut_base, cut_stage),
    site=_v("上から見た発電所の4つの号機", ("mark",), site_base, site_stage),
    dial=_v("出力の針", ("clock", "r86"), dial_base, dial_stage, dial_parts),
    ruler=_v("炉と残した棒", ("rods", "scale"), ruler_base, ruler_stage),
    orm=_v("25日の残した棒（表の点）", ("pts", "r92"), orm_base, orm_stage),
    turbine=_v("2台のタービン", ("stop7", "keep8"), turbine_base, turbine_stage),
    eccs=_v("横から見た水の通り道", ("sys", "cut"), eccs_base, eccs_stage),
    stamp=_v("手順の書類と承認", ("stamp", "step"), stamp_base, stamp_stage),
    off11=_v("切っていた時間の帯", ("band", "r92"), off11_base, off11_stage),
    grid3=_v("3つの報告の見方", ("row1", "row2"), grid3_base, grid3_stage),
    trigger=_v("引き金と延期", ("cut", "post"), trigger_base, trigger_stage),
    kiev=_v("指令所から発電所へ", ("ask", "night"), kiev_base, kiev_stage),
    ring=_v("25日の24時間", ("arc",), ring_base, ring_stage),
    day=_v("日めくりと出力", ("d25", "d26"), day_base, day_stage),
    meter=_v("出力の目盛り（熱）", ("ptr", "plan"), meter_base, meter_stage),
    clock=_v("時計と自動の仕組み", ("sw", "drop"), clock_base, clock_stage),
    hold=_v("1986年の見方", ("r86", "cmd"), hold_base, hold_stage),
    swap=_v("札の入れ替え", ("r86", "r92"), swap_base, swap_stage),
    two91=_v("委員会の2つの見方", ("cause", "ctrl"), two91_base, two91_stage),
    letter=_v("私信", ("env", "open"), letter_base, letter_stage),
    docline=_v("報告の本文の一行", ("hl", "two"), docline_base, docline_stage),
    say3=_v("3つの言い方と、その後の出力", ("cards", "p200", "cap"), say3_base, say3_stage),
    bars=_v("熱出力の棒（同じ縮尺）", ("bars", "r86"), bars_base, bars_stage),
    page86=_v("報告の頁と強調", ("oral", "r92"), page86_base, page86_stage),
    limit=_v("下限の線（前とあと）", ("r92", "after"), limit_base, limit_stage),
    pillars=_v("禁止があったか（3つの決まり）", ("c91",), pillars_base, pillars_stage),
    inst=_v("横から見た炉と計器", ("det", "blind"), inst_base, inst_stage),
    thermo=_v("水の温度計", ("rise", "r92"), thermo_base, thermo_stage),
    balance=_v("2つの見方の天秤", ("left", "right", "split"), balance_base, balance_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
# 原文の値・欄・項目の写し（左上に「模式」を付けない）
NOT_SCHEMATIC = ("years", "cards7", "cal", "orm", "off11", "grid3", "ring", "meter", "clock", "hold", "swap", "two91", "say3", "bars",
                 "pillars", "balance")
VIEW_DIR = ("横から", "上から", "斜めから", "正面")


def lab_of(view, st0):
    lab = VIEWS[view]["lab"]
    return lab(st0) if callable(lab) else lab


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
                raise ValueError(f"m24：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m24：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    return out[0], out[1:]


def stage_art(view, prev, st):
    return VIEWS[view]["stage"](prev, st)


def _base(view, st0):
    """基図＋頭の状態の層（頭で on にした欄は基図に描く＝前のカットの続き）"""
    return VIEWS[view]["base"](st0) + stage_art(view, dict(START[view]), st0)


def _stage_svgs(view, steps, start, states):
    stages = []
    prev = start
    for st, stt in zip(steps, states):
        s = stage_art(view, prev, stt)
        stages.append("".join(s) or " ")
        prev = stt
    return stages


def _static_part(sh):
    a = float(sh["keys"][0].get("alpha", 1.0))
    if a <= 0.01:
        return ""
    k0 = sh["keys"][0]
    pts = F.mech_pts(sh, k0)
    return F.poly(pts, k0.get("fill", sh.get("fill")) or "none", k0.get("stroke", sh.get("stroke")), sh.get("w") or None, close=True,
                  op=(round(a, 2) if a < 0.99 else None))


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")
_TEXT = re.compile(r"<text\s[^>]*>([^<]*)</text>")


def svg_texts(svg):
    """SVG の <text> の中身（門番が全部の字から数を拾う）。"""
    return [t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">") for t in _TEXT.findall(svg)]


def m24(view, steps, start=None, rel=(), note="", src=""):
    """24本目の図解。view は VIEWS の見え方。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m24：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view not in NOT_SCHEMATIC and "模式" not in note:
        raise ValueError("m24：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    seq = [st0] + states
    per = [parts_of(view, s) for s in seq]
    shapes, anim = [], []
    for j, p0 in enumerate(per[0]):
        keys = []
        for i, ps in enumerate(per):
            pj = ps[j]
            kk = {f_: pj[f_] for f_ in KEY_FIELDS if f_ in pj and pj[f_] is not None}
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
    lab = lab_of(view, st0)
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, lab + ("" if view in NOT_SCHEMATIC else "・模式"), 1000, cap=30, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages = _stage_svgs(view, steps, st0, states)
    base_svg = "".join(g)
    f = F.Fig(base_svg, stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    # 門番が数を拾う字＝基図（左上の札と出典の行を除く）と段の層の全部
    body = "".join(g[:-2]) + "".join(stages)
    f.mech = dict(kind="m24", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=shapes, lab=lab, note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states), texts_all=svg_texts(body))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M24）
# ══════════════════════════════════════════════════════════
def _on_any(allst, f_):
    return any(s.get(f_) == "on" for s in allst)


def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst], reps={k: (n, r) for k, (n, r) in REPS.items()})
    if view == "years":
        out.update(items=tuple((k, d, ym, th) for k, d, ym, th, _s, _n in YEARS), names=tuple(n for *_x, n in YEARS),
                   xs=tuple(YR["xs"]), shown=tuple(k for k, *_r in YEARS if _on_any(allst, k)))
    elif view == "cards7":
        out.update(cards=tuple(VIOL), xy=tuple(c7_xy(i) for i in range(7)))
    elif view == "neutron":
        out.update(heat=NT_HEAT, elec=NT_ELEC)
    elif view == "void":
        out.update(nodes=tuple(VD_NODES), xy=tuple(vd_xy(i) for i in range(4)))
    elif view == "power20":
        out.update(low=PW_LOW, xl=pw_x(PW_LOW), x0=PW["x0"], x1=PW["x1"])
    elif view == "flow4":
        out.update(boxes=tuple((k, t) for k, _x, t in FL_BOX), xs=tuple(x for _k, x, _t in FL_BOX))
    elif view == "cal":
        out.update(years=CAL_YEARS, marks={k: tuple(v) for k, v in CAL_MARK.items()}, xs=tuple(CAL["xs"]))
    elif view == "blame":
        out.update(chips=BL_CHIPS)
    elif view == "site":
        out.update(n=SITE_UNITS, mark=SITE_MARK, xs=tuple(ST["xs"]))
    elif view == "dial":
        rows = [p["rot"] for s in allst for p in parts_of("dial", s)]
        out.update(t=DL_T, t86=DL_T86, rots=tuple(rows))
    elif view == "ruler":
        out.update(ticks=RL_TICKS, ys=tuple(rl_y(v) for v in RL_TICKS), y0=RL["y0"], k=RL["k"])
    elif view == "orm":
        out.update(pts=OR_PTS, line=OR_LINE, px=tuple((or_x(t), or_y(v)) for t, v in OR_PTS), x0=OR["x0"], x1=OR["x1"], hours=OR["h"],
                   y0=OR["y0"], k=OR["k"], ly=or_y(OR_LINE))
    elif view == "turbine":
        out.update(t=TB_T, stop=TB_STOP, keep=TB_KEEP)
    elif view == "eccs":
        out.update(t=EC_T, n=EC_N, valve_x=EC["valve"][0], tank_x1=EC["tank"][2], core_x0=EC["core"][0])
    elif view == "stamp":
        out.update(row=SP_ROW)
    elif view == "off11":
        out.update(t0=OF_T0, h=OF_H)
    elif view == "grid3":
        out.update(cols=G3_COLS, row1=G3_ROW1, row2=G3_ROW2, rows=G3_ROWS, xs=tuple(G3["xs"]))
    elif view == "trigger":
        out.update(t=TG_T)
    elif view == "kiev":
        out.update(a=KV["a"], b=KV["b"])
    elif view == "ring":
        out.update(a=RG_A, b=RG_B, h=RG_H, deg=(rg_deg(RG_A), rg_deg(RG_B)))
    elif view == "day":
        out.update(order=(DY["c25"][0], DY["c26"][0]))
    elif view == "meter":
        out.update(t=MT_T, v=MT_V, vmax=MT_MAX, plan=MT_PLAN, x0=MT["x0"], x1=MT["x1"], xv=mt_x(MT_V), xp=tuple(mt_x(v) for v in MT_PLAN))
    elif view == "clock":
        out.update(t=CK_T, angles=ck_angles(CK_T))
    elif view == "hold":
        out.update(n=HD_N, viol=VIOL[HD_N - 1])
    elif view == "say3":
        out.update(cards=S3_CARDS, v=S3_V, t=S3_T)
    elif view == "bars":
        out.update(rows=tuple((t, v, r) for t, v, r, _l in BR_ROWS), labs=tuple(l for *_x, l in BR_ROWS), x0=BR["x0"],
                   unit=(BR["x1"] - BR["x0"]) / BR["vmax"], ends=tuple(br_x(v) for _t, v, _r, _l in BR_ROWS), n=BR_N, viol=VIOL[BR_N - 1])
    elif view == "limit":
        out.update(v=LM_V, y=lm_y(LM_V), y0=LM["y0"], y1=LM["y1"], vmax=LM_MAX)
    elif view == "pillars":
        out.update(items=PL3, empty=PL_EMPTY)
    elif view == "inst":
        out.update(mid=in_mid(), out_y=in_mid(), core=IN["core"])
    elif view == "thermo":
        out.update(boil=TH["boil"], lvl=TH["lvl"])
    elif view == "balance":
        out.update(left=BA_L, right=BA_R, xl=BA["xl"], xr=BA["xr"])
    return out
