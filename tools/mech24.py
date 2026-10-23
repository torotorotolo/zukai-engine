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
  🆕 ⑤b-5（2026-10-23＝第4〜7章の38カット・地図 c713 は ⑤b-6）
  第4章  guard（c501 保護の仕組み）・drum（c502 横から＝蒸気ドラム）・drumtrip（c503 計器2つ・札⑤）・stage2（c504 ドラムの断面と2つの段）・
         marks5（c506 札と2つの印）・tg2（c507 上から下の絵の流れ・札⑥）・retry（c509 輪の矢印）・shift（c510 時刻の線と動く印）・
         shadow（c512 札と棒の影）・seesaw（c514 板と支点の天秤）・light（c515 書類と制御盤・羽）・test200（c516 縦の出力の目盛り）
  第5章  printout（c602 印字の紙）・rods15（c603 棒を1本ずつ・札⑦）・weight（c605 重り）・skala（c606 計算機の画面）・twosay（c607 左右の印字）・
         meaning（c608 分布の線と盾）・go（c609 開始の灯）・valve8（c610 横から＝弁とタービン）・flow35（c612 35秒の2本の線）・
         digital（c614 数字の時計と AZ-5）・spike（c616 縦の計器）・rodstop（c617 横から＝棒の通り道）・why8（c620 爆発と棒の影）
  第6章  roof（c701 上から＝建屋の屋根と火）・dayband（c706 空の色の24時間の帯）・notice（c714 掲示の紙と絵の札）
  第7章  table6（c806 違反の表の列と行）・pile（c808 重なる6つの札）・carry（c810 職員 → 規則の外の状態）・sizes（c813 大小の札）・door（c815 扉と錠）・
         venn3（c816 重なる3つの輪）・shield（c817 発電所と盾）・table86（c820 会議の机の空いた所）・rod12（c822 横から＝1.2m）・rodq（c824 棒の影と「？」）
  🔴 同じ型は全編で2回まで・続けない（台本 §7）：年表 c205↔cb02・札 c206↔c714・流れ c214↔c507・暦 c216↔c911・時計 c402↔c614・棒 c412↔cb06＝
     相方は ⑤b-5・⑤b-6 で別の絵に（⑤b-5：c507＝縦の絵の流れ・c614＝数字の時計とボタン・c714＝掲示の紙と絵の札）。この章の中の似た形（針の計器 c301＝丸・c401＝横／時間の帯 c311＝帯・c316＝輪／3つの欄 c312＝表・c416＝書類3つ／
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
#  🆕 ⑤b-5（2026-10-23）：第4〜7章の図解 38カット（c5 12・c6 13・c7 3〈c701・c706・c714〉・c8 10＝地図 c713 は ⑤b-6）
#   🔴 相方の型は ⑤b-4 と別の絵：流れ c507＝縦に並べた絵の流れ（⇔ c214 横の箱の鎖）／時計 c614＝数字の時計とボタン（⇔ c402 丸い時計）／
#      注意 c714＝掲示の紙と絵の札（⇔ c206 7枚の札の2段）。右上の違反の札＝語りが「N つ目」と言うカットだけ（⑤ c503・⑥ c507・⑦ c603）
#   🔴 時刻は台本 §1-5 の値だけ（1:19〈1986年の報告〉・0:36〈1991年の委員会の表〉・1:23:04・0時43分ごろ〈秒は出さない〉・1:23:40・1:23:43・22:00）
# ══════════════════════════════════════════════════════════
def _drum(x, y, w, h, full=True):
    """横から見た蒸気ドラム（横長の筒）＝上が蒸気・下が水。full=False は輪郭だけ（ほかのドラム）。"""
    if not full:
        return F.rect(x, y, w, h, J.BG2, J.LINE_DIM, 4, rx=h / 2)
    return (F.rect(x, y, w, h, "#cfd8dc", None, None, rx=h / 2, op=0.22)
            + F.rect(x + 8, y + h / 2, w - 16, h / 2 - 8, WATER, None, None, rx=h / 4, op=0.55)
            + F.rect(x, y, w, h, "none", J.LINE, 4, rx=h / 2))


# ── guard（c501）＝保護の仕組み（模式）：2行目＝残る2つの「違反」の札（⑤⑥）／3行目＝計器のランプが赤 → 止める信号 → 棒が落ちる（動く部品）
GD_N = (5, 6)
GD = dict(sensor=(320.0, 600.0), relay=700.0, core=(1080.0, 560.0, 1560.0, 790.0), rods=(1160.0, 1240.0, 1320.0, 1400.0, 1480.0),
          rtop=330.0, rlen=200.0, drop=210.0, cards=(400.0, 860.0), cy=330.0)


def guard_base(st0):
    sx, sy = GD["sensor"]
    x0, y0, x1, y1 = GD["core"]
    return [F.rect(sx - 110, sy - 90, 220, 180, J.BG2, J.LINE, 4, rx=12), F.circ(sx, sy - 20, 36, J.BG, J.LINE_DIM, 5),
            _tline(sx, sy + 62, "計器", 28, INK, "middle", 180),
            F.line(sx + 110, sy, x0 - 30, sy, J.LINE_DIM, 5), _arrow(x0 - 60, sy, x0 - 6, sy, J.LINE_DIM, 5, 18),
            F.rect(x0, y0, x1 - x0, y1 - y0, "#2b3a44", GRAPH, 4, rx=8), _tline(x1 + 24, (y0 + y1) / 2 + 10, "炉", 30, INK, "start", 120),
            F.line(GD["rods"][0] - 40, GD["rtop"], GD["rods"][-1] + 40, GD["rtop"], STEEL, 6)]


def guard_parts(st):
    dy = GD["drop"] if st.get("auto") == "on" else 0.0
    t0, L = GD["rtop"], GD["rlen"]
    return [_P(f"rod{i}", "poly", [(x - 12, t0 + 6), (x + 12, t0 + 6), (x + 12, t0 + L), (x - 12, t0 + L)], fill=STEEL, stroke=J.BG, w=3,
               alpha=1.0, dy=dy, lag=0.06 * i) for i, x in enumerate(GD["rods"])]


def guard_stage(prev, st):
    s = []
    if _on(prev, st, "two"):
        for cx, n in zip(GD["cards"], GD_N):
            s.append(_card(cx, GD["cy"], 420, 80, J.AMBER, sw=5))
            s.append(_tline(cx, GD["cy"] + 11, f"{CIRC[n - 1]} {VIOL[n - 1]}", 30, INK, "middle", 390))
    if _on(prev, st, "auto"):
        sx, sy = GD["sensor"]
        s.append(F.circ(sx, sy - 20, 36, J.ALERT, J.BG, 4))
        s.append(_tline(sx, sy - 116, "危ない値", 28, J.ALERT, "middle", 200))
        s.append(_bolt(GD["relay"], sy - 44, 34, J.AMBER))
        s.append(_tline(GD["relay"], sy + 52, "止める信号", 26, J.AMBER, "middle", 200))
        s.append(_tline(1600.0, 430.0, "自動で差し込む", 26, STEEL, "start", 240))
    return s


# ── drum（c502）＝横から見た蒸気ドラム（模式）：1行目＝1つのドラム（上が蒸気・下が水）／2行目＝左右の系統に2つずつ・蒸気はタービンへ・水は炉へ（S1 p17）
DR = dict(core=(780.0, 560.0, 1140.0, 790.0), w=380.0, h=84.0, ys=(330.0, 450.0), xl=180.0, xr=1360.0, ty=300.0)


def drum_base(st0):
    x0, y0, x1, y1 = DR["core"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, "#2b3a44", GRAPH, 4, rx=8), _tline((x0 + x1) / 2, y1 + 44, "炉", 28, INK, "middle", 200)]


def drum_stage(prev, st):
    s = []
    x0, y0, x1, y1 = DR["core"]
    w, h, yA, xl, xr = DR["w"], DR["h"], DR["ys"][0], DR["xl"], DR["xr"]
    if _on(prev, st, "sep"):
        s.append(F.poly([(x0 + 80, y0), (x0 + 80, yA + h / 2), (xl + w + 6, yA + h / 2)], "none", J.LINE, 6))   # 炉から上がる管
        s.append(_arrow(x0 + 110, y0 - 20, x0 + 110, y0 - 110, J.AMBER, 5, 18))
        s.append(_tline(x0 + 60, y0 - 60, "沸いた水と蒸気", 26, J.AMBER, "end", 300))
        s.append(_drum(xl, yA, w, h))
        s.append(_tline(xl + w / 2, yA + 32, "蒸気", 22, INK, "middle", 120))
        s.append(_tline(xl + w / 2, yA + h - 14, "水", 22, J.BG, "middle", 120))
        s.append(_tline(xl + w / 2, yA - 16, "蒸気ドラム", 30, J.LINE, "middle", 300))
    if _on(prev, st, "loop"):
        yB = DR["ys"][1]
        for xx, yy in ((xl, yB), (xr, yA), (xr, yB)):
            s.append(_drum(xx, yy, w, h, full=False))
        s.append(F.poly([(x1 - 80, y0), (x1 - 80, yA + h / 2), (xr - 6, yA + h / 2)], "none", J.LINE_DIM, 6))
        s.append(_arrow(xl + w - 40, yA - 6, 820.0, DR["ty"] - 10, J.LINE, 5, 20))         # 蒸気 → タービンへ
        s.append(_arrow(xr + 40, yA - 6, 1100.0, DR["ty"] - 10, J.LINE_DIM, 5, 20))
        s.append(_tline(CX, DR["ty"] - 4, "蒸気→タービンへ", 26, J.LINE, "middle", 260))
        for xd, xc, col in ((xl + 120, x0 - 10, WATER), (xr + w - 120, x1 + 10, J.LINE_DIM)):   # 水 → 炉へ
            s.append(F.poly([(xd, yB + h + 6), (xd, 700.0), ((xd + xc) / 2, 700.0)], "none", col, 6))
            s.append(_arrow((xd + xc) / 2, 700.0, xc, 700.0, col, 6, 22))
        s.append(_tline((xl + 120 + x0) / 2, 680.0, "水は炉へ", 26, WATER, "middle", 200))
        s.append(_tline(xl + w / 2 + 70, yB + h + 60, "左に2つ", 26, INK, "middle", 200))
        s.append(_tline(xr + w / 2 - 70, yB + h + 60, "右に2つ", 26, INK, "middle", 200))
    return s


# ── drumtrip（c503）＝右上の札⑤・ドラムの水位と圧力の保護（計器2つ → 炉を止める信号）→ 1986年の報告：1:19 に外した（線に×）・重い違反
DT_T, DT_N = "1:19", 5           # 1986年の報告の時刻（S1 p22「not at 01:19:00 as stated in INSAG-1」）
DT_G = ("水位", "圧力")
DT = dict(drum=(520.0, 320.0, 640.0, 100.0), gx=(660.0, 1020.0), gy=590.0, r=56.0, box=(840.0, 790.0, 340.0, 64.0), rep=(1500.0, 470.0))


def drumtrip_base(st0):
    x, y, w, h = DT["drum"]
    bx, by, bw, bh = DT["box"]
    g = [_badge(DT_N), _drum(x, y, w, h), _tline(x + w / 2, y + 36, "蒸気ドラム", 26, INK, "middle", 300)]
    for gx, t in zip(DT["gx"], DT_G):
        g.append(F.line(gx, y + h, gx, DT["gy"] - DT["r"], J.LINE, 5))
        g.append(F.circ(gx, DT["gy"], DT["r"], J.BG2, J.LINE, 5))
        g.append(F.line(gx, DT["gy"], gx + 30, DT["gy"] - 32, J.AMBER, 5))
        g.append(_tline(gx - DT["r"] - 18, DT["gy"] + 10, t, 28, INK, "end", 160))
        g.append(F.line(gx, DT["gy"] + DT["r"], bx + (gx - bx) * 0.45, by - bh / 2, J.LINE, 5))
    g.append(_card(bx, by, bw, bh, J.ALERT, sw=4))
    g.append(_tline(bx, by + 10, "炉を止める信号", 26, INK, "middle", bw - 30))
    return g


def dt_cuts():
    """2本の線の真ん中（×を付ける所）"""
    bx, by, _bw, bh = DT["box"]
    return [((gx + bx + (gx - bx) * 0.45) / 2, (DT["gy"] + DT["r"] + by - bh / 2) / 2) for gx in DT["gx"]]


def drumtrip_stage(prev, st):
    s = []
    if _on(prev, st, "r86"):
        s.append(_rep(*DT["rep"], "r86", "保護を外した", cap=28))
    if _on(prev, st, "off"):
        for x, y in dt_cuts():
            s.append(_xmark(x, y, 20, J.ALERT, 8))
        s.append(_bigtime(DT["rep"][0], 650.0, DT_T, 80))
        s.append(_tline(DT["rep"][0], 722.0, "重い違反", 30, J.ALERT, "middle", 300))
    return s


# ── stage2（c504）＝ドラムの断面（模式）：1行目＝1991年の委員会の表 0:36 圧力の保護の設定を変える／2行目＝水位の保護の2つの段・下の段は最後まで効いた（S1 p22）
S2_T = "0:36"
S2D = dict(x=260.0, y=400.0, w=760.0, h=300.0, wl=520.0, lv=(590.0, 650.0), gauge=(880.0, 336.0), rep=(1480.0, 410.0))


def stage2_base(st0):
    x, y, w, h = S2D["x"], S2D["y"], S2D["w"], S2D["h"]
    R = h / 2
    a = math.degrees(math.asin((S2D["wl"] - (y + R)) / R))          # 水面の高さの角度（左右の半円）
    pts = _arcpts(x + R, y + R, R, R, 180.0 - a, 90.0) + _arcpts(x + w - R, y + R, R, R, 90.0, a)
    gx, gy = S2D["gauge"]
    return [F.rect(x, y, w, h, J.BG2, None, None, rx=R), F.poly(pts, WATER, None, close=True, op=0.45),
            F.rect(x, y, w, h, "none", J.LINE, 5, rx=R),
            F.line(gx, gy + 34, gx, y, J.LINE, 5), F.circ(gx, gy, 34, J.BG2, J.LINE, 5), F.line(gx, gy, gx + 20, gy - 18, J.AMBER, 4),
            _tline(gx + 60, gy + 10, "圧力", 28, INK, "start", 140)]


def stage2_stage(prev, st):
    s = []
    x, w = S2D["x"], S2D["w"]
    if _on(prev, st, "p036"):
        gx, gy = S2D["gauge"]
        s.append(F.circ(gx, gy, 46, "none", J.AMBER, 5))
        s.append(_rep(*S2D["rep"], "c91", "圧力の設定を変更", cap=28))
        s.append(_bigtime(S2D["rep"][0], 580.0, S2_T, 80))
    if _on(prev, st, "lv2"):
        up, lo = S2D["lv"]
        s.append(F.line(x + 50, up, x + w - 50, up, J.LINE, 4, dash="14 10"))
        s.append(F.line(x + 80, lo, x + w - 80, lo, J.OK, 5, dash="14 10"))
        s.append(_tline(x + w + 34, up + 10, "上の段", 28, J.LINE, "start", 160))
        s.append(_tline(x + w + 34, lo + 10, "下の段", 28, J.OK, "start", 160))
        s.append(_check(x + w + 158, lo - 4, 18, J.OK))
        s.append(_tline(x + w + 190, lo + 10, "最後まで効いた", 28, J.OK, "start", 260))
    return s


# ── marks5（c506）＝5つ目の札と2つの印（形の上は違反／保護は効いた）→ 1992年の報告：外すことは許されたはず → 実際は外されず（S1 p28）
MK_N = 5
MK = dict(card=(960.0, 370.0, 640.0, 104.0), l=(680.0, 545.0), r=(1240.0, 545.0), rep=(680.0, 735.0), sw=(1160.0, 735.0))


def marks5_base(st0):
    cx, cy, w, h = MK["card"]
    lx, ly = MK["l"]
    rx_, _ry = MK["r"]
    return [_card(cx, cy, w, h, J.AMBER, sw=6), F.txt(cx - w / 2 + 50, cy + 17, CIRC[MK_N - 1], 48, J.AMBER, "Noto", "middle"),
            _tline(cx + 30, cy + 13, VIOL[MK_N - 1], 38, INK, "middle", w - 140),
            F.rect(lx - 170, ly - 44, 340, 88, J.BG2, J.ALERT, 5, rx=8), _tline(lx, ly + 11, "形の上は違反", 32, J.ALERT, "middle", 310),
            _check(rx_ - 140, ly - 4, 22, J.OK), _tline(rx_ - 100, ly + 11, "保護は効いた", 32, J.OK, "start", 320)]


def marks5_stage(prev, st):
    s = []
    if _on(prev, st, "ok92"):
        s.append(_rep(*MK["rep"], "r92", "外すことは許されたはず", cap=26))
    if _on(prev, st, "notdone"):
        x, y = MK["sw"]
        s.append(F.rect(x - 60, y - 28, 120, 56, J.OK, None, None, rx=28))
        s.append(F.circ(x + 32, y, 22, J.BG2, None))
        s.append(_tline(x + 90, y + 11, "実際は外されず", 30, J.OK, "start", 300))
    return s


# ── tg2（c507）＝右上の札⑥・上から下への絵の流れ（🔴 c214 の横の箱の鎖と別の形）：2台のタービンが止まる → 止める信号 → 炉も止まる／
#    2行目＝1986年の報告：試験を始めた 1:23:04 に外した（信号と炉のあいだに×）
TG_N, TG_T86 = 6, "1:23:04"
TG = dict(x=760.0, ys=(380.0, 570.0, 750.0), lx=1000.0, rep=(1470.0, 470.0), t=(1470.0, 650.0))


def tg2_base(st0):
    return [_badge(TG_N)]


def tg_xy():
    y1, y2, y3 = TG["ys"]
    return TG["x"], (y2 + 50 + y3 - 48) / 2


def tg2_stage(prev, st):
    s = []
    x, (y1, y2, y3) = TG["x"], TG["ys"]
    if _on(prev, st, "flow"):
        s.append(_turbine(x - 120, y1, 0.5, dim=True))
        s.append(_turbine(x + 120, y1, 0.5, dim=True))
        s.append(_arrow(x, y1 + 50, x, y2 - 50, J.LINE, 6, 22))
        s.append(_bolt(x, y2, 38, J.AMBER))
        s.append(_arrow(x, y2 + 50, x, y3 - 48, J.LINE, 6, 22))
        s.append(F.rect(x - 90, y3 - 40, 180, 80, "#2b3a44", GRAPH, 4, rx=8))
        for i in range(4):
            s.append(F.rect(x - 66 + i * 38, y3 - 56, 14, 60, STEEL, None, None, rx=3))
        for y, t in ((y1, "2台とも止まる"), (y2, "止める信号"), (y3, "炉も止まる")):
            s.append(_tline(TG["lx"], y + 11, t, 30, INK, "start", 260))
    if _on(prev, st, "r86"):
        xm, ym = tg_xy()
        s.append(_xmark(xm, ym, 24, J.ALERT, 9))
        s.append(_tline(xm - 50, ym + 10, "外した", 30, J.ALERT, "end", 200))
        s.append(_rep(*TG["rep"], "r86", "試験を始めた時に外した", cap=26))
        s.append(_bigtime(*TG["t"], TG_T86, 72))
    return s


# ── retry（c509）＝1行目（聞き役）：⑥ の札に×（外した）／2行目＝1986年のソ連の報告：必要なら、タービン2台を止めたまま試験をくり返す（輪の矢印）
RT_N = 2
RT = dict(chip=(960.0, 360.0), c=(960.0, 610.0), rx=330.0, ry=150.0, a=(205.0, 515.0), rep=(1540.0, 610.0))


def retry_base(st0):
    cx, cy = RT["chip"]
    t = f"{CIRC[TG_N - 1]} {VIOL[TG_N - 1]}"
    w = _w(t, 30) + 60
    return [_card(cx, cy, w, 80, J.LINE, sw=4), _tline(cx, cy + 11, t, 30, INK, "middle", w - 30),
            _xmark(cx + w / 2 + 44, cy, 22, J.ALERT, 8), _tline(cx + w / 2 + 84, cy + 10, "外した", 28, J.ALERT, "start", 160)]


def retry_stage(prev, st):
    s = []
    if _on(prev, st, "s86"):
        cx, cy = RT["c"]
        for i in range(RT_N):
            s.append(_turbine(cx - 120 + 240 * i, cy - 14, 0.5, dim=True))
        s.append(_tline(cx, cy + 80, "2台を止めたまま", 26, J.TICK, "middle", 300))
        s.append(_arc_arrow(cx, cy, RT["rx"], RT["ry"], RT["a"][0], RT["a"][1], J.AMBER, 7, 28))
        s.append(_tline(cx - RT["rx"] - 36, cy + 10, "くり返す", 30, J.AMBER, "end", 200))
        s.append(_rep(*RT["rep"], "s86", "必要なら、やり直す", cap=26))
    return s


# ── shift（c510）＝夜の時刻の線（0時〜1時30分＝時間に比例）：桃の印 1:23:04（1986年の報告）→ 1行目＝青い印が 0時43分ごろへ動く（動く部品・秒は出さない）／
#    2行目＝運転の手順と試験の手順に沿っていた（S1 p21）
SH_T86 = "1:23:04"
SH_M86, SH_M92 = 83 + 4 / 60.0, 43 + 27 / 60.0     # 0時からの分（1:23:04・0:43:27）
SH = dict(x0=300.0, x1=1620.0, y=560.0, span=90.0)


def sh_x(m):
    return SH["x0"] + (SH["x1"] - SH["x0"]) * m / SH["span"]


def sh_lab92():
    return f"0時{int(SH_M92)}分ごろ"


def shift_base(st0):
    x0, x1, y = SH["x0"], SH["x1"], SH["y"]
    g = [F.line(x0, y, x1, y, J.TICK, 5)]
    for m in range(0, 91, 15):
        big = m % 60 == 0
        g.append(F.line(sh_x(m), y - (16 if big else 9), sh_x(m), y + (16 if big else 9), J.TICK, 4 if big else 3))
    for m, t in ((0, "0時"), (60, "1時")):
        g.append(_tline(sh_x(m), y + 56, t, 28, J.TICK, "middle", 120))
    x, col = sh_x(SH_M86), rep_col("r86")
    g.append(F.poly([(x - 18, y - 52), (x + 18, y - 52), (x, y - 14)], col, None, close=True))
    g.append(_tline(x, y - 70, SH_T86, 40, col, "middle", 260, fam="Dela"))
    g.append(_rep(x - 20, y - 160, "r86", None, cap=24))
    return g


def shift_parts(st):
    x, y = sh_x(SH_M86), SH["y"]
    on = st.get("move") == "on"
    return [_P("pin92", "poly", [(x, y + 14), (x - 18, y + 52), (x + 18, y + 52)], fill=rep_col("r92"), stroke=None, w=2,
               alpha=1.0 if on else 0.0, dx=(sh_x(SH_M92) - x) if on else 0.0)]


def shift_stage(prev, st):
    s = []
    y = SH["y"]
    x86, x92 = sh_x(SH_M86), sh_x(SH_M92)
    if _on(prev, st, "move"):
        s.append(_xmark(x86, y - 33, 20, J.ALERT, 7))
        s.append(_arrow(x86 - 50, y - 40, x92 + 40, y - 40, rep_col("r92"), 4, 18, dash="10 8"))
        s.append(_tline(x92, y + 100, sh_lab92(), 34, rep_col("r92"), "middle", 300))
        s.append(_rep(x92, y + 170, "r92", None, cap=24))
    if _on(prev, st, "proc"):
        for i, t in enumerate(("運転の手順", "試験の手順")):
            x = 1240.0 + i * 260
            s.append(_doc(x - 100, 680.0, 200, 140, J.DOC, nlines=2, top=84.0, gap=30.0))
            s.append(_tline(x, 724.0, t, 26, J.DOC, "middle", 180))
            s.append(_check(x + 86, 664.0, 20, J.OK))        # 🔧 geom_gap：題の字に 5px＝紙の右上の外へ
        s.append(_tline(1630.0, 760.0, "手順どおり", 28, J.OK, "start", 200))      # 机上：✓を紙の右上へ出したので、字は紙の右へ
    return s


# ── shadow（c512）＝1行目：1986年の報告の札「保護が働けば救われた」と1992年の報告／2行目＝止める棒の影が札の右の余白に落ちる・成り立たないようだ（S1 p21）。
#    🔴 影と割れ目は札の字にかけない（札を広く取り、右の余白だけ）
SD = dict(card=(760.0, 500.0), cw=720.0, rod=(1300.0, 330.0, 1360.0, 760.0), r92=(1560.0, 330.0))
SD_BODY = "保護が働けば救われた"


def shadow_stage(prev, st):
    s = []
    cx, cy = SD["card"]
    if _on(prev, st, "card"):
        s.append(_rep(cx, cy, "r86", SD_BODY, cap=32, w=SD["cw"]))
        s.append(_rep(*SD["r92"], "r92", None, cap=26))
    if _on(prev, st, "shade"):
        x0, y0, x1, y1 = SD["rod"]
        bx0, by0, bx1, by1 = rep_box(cx, cy, "r86", SD_BODY, cap=32, w=SD["cw"])
        s.append(F.poly([(x0, y0 + 60), (x1, y0 + 60), (bx1 + 2, by1 + 2), (bx1 - 150, by1 + 2)], "#000000", None, close=True, op=0.38))
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, "#3a4650", J.LINE_DIM, 3, rx=10))
        s.append(_tline((x0 + x1) / 2, y1 + 42, "止める棒", 26, J.TICK, "middle", 200))      # 机上：上の札（1992年の報告）の縁に触れた＝棒の下へ
        s.append(F.poly([(bx1 - 70, by0 - 2), (bx1 - 50, by0 + 30), (bx1 - 80, by0 + 56), (bx1 - 56, by0 + 84), (bx1 - 76, by1 + 2)], "none", J.ALERT, 5))
        s.append(_tline(cx, by1 + 80, "成り立たないようだ", 34, rep_col("r92"), "middle", 600))
    return s


# ── seesaw（c514）＝1992年の報告の天秤（板と支点＝水平・🔴 c421 の吊る天秤と別の形）：左＝この保護では運転員を責めない（頭から）／2行目＝右＝運転員にも甘くない
SW = dict(cx=960.0, py=640.0, x0=380.0, x1=1540.0, bw=420.0, bh=130.0, fy=760.0)
SW_L = ("この保護の件は", "運転員を責めない")
SW_R = ("ただし", "運転員にも甘くない")


def _sw_y():
    return SW["py"] - 12 - SW["bh"] / 2 - 4


def seesaw_base(st0):
    cx, py = SW["cx"], SW["py"]
    return [_rep(cx, 330.0, "r92", None, cap=28),
            F.poly([(cx, py + 12), (cx - 80, SW["fy"]), (cx + 80, SW["fy"])], J.BG2, J.LINE, 5, close=True),
            F.rect(SW["x0"], py - 12, SW["x1"] - SW["x0"], 24, J.LINE, None, None, rx=6)]


def _sw_block(x, a, b, col):
    y = _sw_y()
    return (_card(x, y, SW["bw"], SW["bh"], col, sw=6) + _tline(x, y - 14, a, 26, J.TICK, "middle", SW["bw"] - 30)
            + _tline(x, y + 36, b, 32, col, "middle", SW["bw"] - 30))


def seesaw_stage(prev, st):
    s = []
    if _on(prev, st, "left"):
        s.append(_sw_block(SW["x0"] + SW["bw"] / 2 + 20, *SW_L, J.OK))
    if _on(prev, st, "right"):
        s.append(_sw_block(SW["x1"] - SW["bw"] / 2 - 20, *SW_R, rep_col("r92")))
    return s


# ── light（c515）＝運転の手順（書類）と運転員の側（制御盤＝人は描かない）：1行目＝どちらにも「保護を外す」の札が軽い（破線・羽）／2行目＝1992年の報告
LT = dict(doc=(300.0, 330.0, 360.0, 400.0), desk=(1260.0, 560.0), rep=(960.0, 790.0))


def _feather(cx, cy, s=1.0, col=None):
    c = col or J.TICK
    a = math.radians(-35)
    pts = []
    for i in range(24):
        t = 2 * math.pi * i / 24
        x, y = 14 * s * math.cos(t), 44 * s * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    tip = (cx - 56 * s * math.sin(a), cy + 56 * s * math.cos(a))
    return F.poly(pts, "none", c, 3, close=True) + F.line(cx + 44 * s * math.sin(a), cy - 44 * s * math.cos(a), tip[0], tip[1], c, 3)


def light_base(st0):
    x, y, w, h = LT["doc"]
    dx, dy = LT["desk"]
    g = [_doc(x, y, w, h, J.DOC, nlines=4, top=110.0, gap=60.0), _tline(x + w / 2, y + 60, "運転の手順", 32, J.DOC, "middle", w - 40),
         F.poly([(dx - 260, dy + 60), (dx + 260, dy + 60), (dx + 200, dy - 40), (dx - 200, dy - 40)], J.BG2, J.LINE, 4, close=True),
         F.rect(dx - 240, dy - 220, 480, 170, J.BG2, J.LINE, 4, rx=8)]
    for i in range(6):
        g.append(F.circ(dx - 180 + i * 72, dy - 170, 14, (J.OK, J.AMBER, J.LINE)[i % 3], None))
    g.append(_tline(dx, dy + 110, "運転員の側", 32, INK, "middle", 300))
    return g


def light_chips():
    x, y, w, h = LT["doc"]
    dx, dy = LT["desk"]
    return ((x + 140, y + h - 50), (dx - 80, dy - 100))


def light_stage(prev, st):
    s = []
    if _on(prev, st, "both"):
        for cx, cy in light_chips():
            s.append(_card(cx, cy, 220, 54, J.TICK, sw=3, dash="8 6"))
            s.append(_tline(cx, cy + 9, "保護を外す", 26, J.TICK, "middle", 200))
            s.append(_feather(cx + 160, cy - 6, 0.9))
    if _on(prev, st, "r92"):
        s.append(_rep(*LT["rep"], "r92", "どちらも軽く見ていた", cap=28))
    return s


# ── test200（c516）＝縦の出力の目盛り（値に比例）：予定 700MW の線 → 1行目＝200MW で止まる・700 に×・その場で変更／2行目＝200MW のまま試験へ（S1 p29）
T2_PLAN, T2_ACT = 700.0, 200.0
T2 = dict(x=520.0, y0=800.0, k=0.62, top=330.0, xa=660.0, xt=1380.0)


def t2_y(v):
    return T2["y0"] - T2["k"] * v


def test200_base(st0):
    x, y0 = T2["x"], T2["y0"]
    yp = t2_y(T2_PLAN)
    return [F.line(x, y0, x, T2["top"], J.TICK, 4), _arrow(x, T2["top"] + 20, x, T2["top"] - 16, J.TICK, 4, 16),
            F.line(x - 12, y0, x + 12, y0, J.TICK, 4), _tline(x - 22, y0 + 10, "0", 28, J.TICK, "end", 60),
            _tline(x + 22, T2["top"] - 6, "出力（熱）", 26, J.TICK, "start", 200),
            F.line(x, yp, 1560.0, yp, J.OK, 4, dash="14 10"), _tline(1560.0, yp - 18, f"予定 {T2_PLAN:,.0f}MW", 30, J.OK, "end", 340)]


def test200_stage(prev, st):
    s = []
    xa, ya, yp = T2["xa"], t2_y(T2_ACT), t2_y(T2_PLAN)
    if _on(prev, st, "stuck"):
        s.append(_arrow(xa, T2["y0"] - 10, xa, ya + 4, J.AMBER, 8, 26))
        s.append(F.line(xa - 40, ya, xa + 40, ya, J.AMBER, 6))
        s.append(F.line(xa, ya - 24, xa, yp + 34, J.AMBER, 3, dash="6 8"))
        s.append(_xmark(xa, yp, 22, J.ALERT, 8))
        s.append(_tline(xa + 50, yp + 60, "戻せない", 30, J.ALERT, "start", 200))
        s.append(_card(1000.0, 520.0, 300, 76, J.ALERT, sw=4))
        s.append(_tline(1000.0, 531.0, "その場で変更", 30, J.ALERT, "middle", 260))
    if _on(prev, st, "go"):
        s.append(_arrow(xa + 50, ya, T2["xt"] - 120, ya, J.AMBER, 7, 26))
        s.append(_card(T2["xt"], ya, 220, 90, J.AMBER, sw=6))
        s.append(_tline(T2["xt"], ya + 12, "試験", 36, J.AMBER, "middle", 200))
        s.append(_tline((xa + T2["xt"]) / 2, ya - 28, f"{T2_ACT:,.0f}MW", 36, J.AMBER, "middle", 260, fam="Dela"))
    return s


# ── printout（c602）＝計算機の印字（送り穴の紙・模式）に「即時停止の水準」→ 1行目＝それでも試験へ（▶）／2行目＝1986年のソ連の報告（S3 p2021）
def _printout(x, y, w, h, col=None, nlines=6, skip=None):
    """計算機の印字の紙（両の端に送り穴）。skip=(y0, y1)＝その高さの行は描かない（真ん中に印を置く紙＝geom_gap は地の下の線も数える）。"""
    c = col or J.LINE
    g = [F.rect(x, y, w, h, J.BG2, c, 4, rx=4)]
    for yy in range(int(y + 24), int(y + h - 10), 36):
        g.append(F.circ(x + 16, yy, 6, J.BG, c, 2))
        g.append(F.circ(x + w - 16, yy, 6, J.BG, c, 2))
    gap = (h - 60) / max(nlines, 1)
    for i in range(nlines):
        yy = y + 40 + i * gap
        if skip and skip[0] <= yy <= skip[1]:
            continue
        g.append(F.line(x + 44, yy, x + w - 44 - 60 * (i % 2), yy, J.LINE_DIM, 6))
    return "".join(g)


PO = dict(paper=(300.0, 300.0, 420.0, 500.0), stamp=(510.0, 600.0))


def printout_base(st0):
    x, y, w, h = PO["paper"]
    sx, sy = PO["stamp"]
    return [_printout(x, y, w, h), F.rect(sx - 160, sy - 42, 320, 84, J.BG2, J.ALERT, 5, rx=6),
            _tline(sx, sy + 11, "即時停止の水準", 30, J.ALERT, "middle", 290)]


def printout_stage(prev, st):
    s = []
    if _on(prev, st, "start"):
        s.append(_arrow(750.0, 550.0, 1080.0, 550.0, J.OK, 8, 30))
        s.append(F.poly([(1140.0, 500.0), (1140.0, 600.0), (1230.0, 550.0)], J.OK, None, close=True))
        s.append(_tline(1185.0, 662.0, "試験へ", 34, J.OK, "middle", 200))
    if _on(prev, st, "s86"):
        s.append(_rep(1380.0, 790.0, "s86", "印字を見ても続行", cap=28))
    return s


# ── rods15（c603）＝棒を1本ずつ（数＝記録）：上の列＝すぐ止める決まり 15本／下の列＝1986年のソ連の報告 6〜8本（6本＋破線2本）＝15本のおよそ半分／
#    2行目＝右上の札⑦。🔴 「事故のあとの計算 8本」は描かない（出典の欄だけ）・「半分以下」と書かない（S3 の比べるもとは30本）
RD_RULE, RD_LO, RD_HI, RD_N = 15, 6, 8, 7
RD = dict(x0=560.0, dx=54.0, ya=410.0, yb=620.0, w=26.0, h=110.0)


def _rodicon(x, y, col, dash=False):
    if dash:
        return F.rect(x - RD["w"] / 2, y - RD["h"] / 2, RD["w"], RD["h"], "none", col, 4, rx=8, dash="8 6")
    return F.rect(x - RD["w"] / 2, y - RD["h"] / 2, RD["w"], RD["h"], col, None, None, rx=8)


def rods15_base(st0):
    return []


def rods15_stage(prev, st):
    s = []
    if _on(prev, st, "rows"):
        for i in range(RD_RULE):
            s.append(_rodicon(RD["x0"] + i * RD["dx"], RD["ya"], J.ALERT))
        for i in range(RD_HI):
            s.append(_rodicon(RD["x0"] + i * RD["dx"], RD["yb"], rep_col("s86"), dash=i >= RD_LO))
        s.append(_tline(RD["x0"] - 44, RD["ya"] + 12, "すぐ止める決まり", 30, J.ALERT, "end", 420))
        s.append(_rep(350.0, RD["yb"], "s86", None, cap=24))
        s.append(_tline(RD["x0"] + (RD_RULE - 1) * RD["dx"] + 50, RD["ya"] + 14, f"{RD_RULE}本", 40, J.ALERT, "start", 200, fam="Dela"))
        xb = RD["x0"] + (RD_HI - 1) * RD["dx"] + 50
        s.append(_tline(xb, RD["yb"] + 14, f"{RD_LO}〜{RD_HI}本", 40, rep_col("s86"), "start", 220, fam="Dela"))
        s.append(_tline(xb + 230, RD["yb"] + 12, f"＝{RD_RULE}本のおよそ半分", 30, J.AMBER, "start", 420))
    if _on(prev, st, "viol"):
        s.append(_badge(RD_N))
    return s


# ── weight（c605）＝1行目（聞き役）：⑦ の札／2行目＝違反は変わらず／3行目＝安全上の重さ＝1986年の報告の小さな重り・1992年の報告の大きな重り（S1 p22）
WT_N = 7
WT = dict(card=(960.0, 350.0, 600.0, 96.0), stamp=(1430.0, 350.0), s=(700.0, 700.0, 0.4), b=(1220.0, 700.0, 1.0))


def _weight(cx, by, s, col):
    """分銅（台形＋つまみ）。by＝底・s＝大きさ（1.0 で高さ 230）。"""
    h, wb, wt = 230 * s, 300 * s, 200 * s
    return (F.poly([(cx - wb / 2, by), (cx + wb / 2, by), (cx + wt / 2, by - h), (cx - wt / 2, by - h)], col, None, close=True, op=0.85)
            + F.circ(cx, by - h - 24 * s, 24 * s, "none", col, max(4, 8 * s)))


def weight_base(st0):
    cx, cy, w, h = WT["card"]
    return [_card(cx, cy, w, h, J.AMBER, sw=6), F.txt(cx - w / 2 + 46, cy + 16, CIRC[WT_N - 1], 44, J.AMBER, "Noto", "middle"),
            _tline(cx + 30, cy + 12, VIOL[WT_N - 1], 34, INK, "middle", w - 130)]


def weight_stage(prev, st):
    s = []
    if _on(prev, st, "same"):
        x, y = WT["stamp"]
        s.append(F.rect(x - 130, y - 40, 260, 80, J.BG2, J.ALERT, 5, rx=8))
        s.append(_tline(x, y + 10, "違反は変わらず", 28, J.ALERT, "middle", 240))
    if _on(prev, st, "big"):
        for key, (cx, by, sc) in (("r86", WT["s"]), ("r92", WT["b"])):
            s.append(_weight(cx, by, sc, rep_col(key)))
            s.append(_rep(cx, by + 60, key, None, cap=24))
        s.append(_tline(CX, 520.0, "安全上の重さ", 28, J.TICK, "middle", 260))
        s.append(_tline(WT["b"][0] + 170, 560.0, "ずっと大きい", 30, rep_col("r92"), "start", 300))   # 🔧 geom_gap：上の⑦の札と印に重なった＝重りの右へ
    return s


# ── skala（c606）＝計算機 SKALA の画面（模式）：1行目＝当てにならない・1回の計算に10〜15分（S1 p16）／2行目＝画面に「？」・1992年の報告：値は知らなかった見込み／
#    3行目＝残す棒が減っていく（下向きの矢印）・おそらく気づいていた
SK_MIN = (10, 15)
SK = dict(scr=(420.0, 330.0, 400.0, 280.0), x=620.0, rep=(1560.0, 400.0))


def skala_base(st0):
    x, y, w, h = SK["scr"]
    g = [F.rect(x, y, w, h, J.BG, J.LINE, 6, rx=14)]
    for i, yy in enumerate((y + 44, y + 74, y + h - 70, y + h - 40)):       # 🔧 geom_gap：真ん中（あとで「？」を置く所）に行を描かない
        g.append(F.line(x + 40, yy, x + w - 60 - 80 * (i % 2), yy, J.LINE_DIM, 8))
    g.append(F.poly([(SK["x"] - 50, y + h), (SK["x"] + 50, y + h), (SK["x"] + 80, y + h + 50), (SK["x"] - 80, y + h + 50)], J.BG2, J.LINE, 4, close=True))
    g.append(_tline(SK["x"], y + h + 100, "SKALA", 34, INK, "middle", 260))
    return g


def skala_stage(prev, st):
    s = []
    if _on(prev, st, "unrel"):
        s.append(F.poly([(920.0, 344.0), (968.0, 424.0), (872.0, 424.0)], "none", J.ALERT, 5, close=True))
        s.append(_tline(996.0, 410.0, "当てにならない", 32, J.ALERT, "start", 320))
        s.append(_tline(880.0, 520.0, f"1回の計算に{SK_MIN[0]}〜{SK_MIN[1]}分", 28, INK, "start", 380))
    if _on(prev, st, "unknown"):
        s.append(F.circ(SK["x"], 470.0, 74, J.BG, None))
        s.append(_qmark(SK["x"], 470.0, 140, J.AMBER))
        s.append(_rep(*SK["rep"], "r92", "値は知らなかった見込み", cap=26))
    if _on(prev, st, "aware"):
        s.append(_arrow(1000.0, 600.0, 1000.0, 730.0, J.ALERT, 7, 26))
        s.append(_tline(1040.0, 680.0, "残す棒が減っていく", 28, J.ALERT, "start", 300))
        s.append(_tline(SK["rep"][0], 520.0, "おそらく気づいていた", 30, rep_col("r92"), "middle", 340))
    return s


# ── twosay（c607）＝左右の2つの言い方（字は少なく・頁の絵は使わない）：1行目＝右＝1991年の委員会「値を知らなかった」（印字に「？」）／
#    2行目＝左＝1986年のソ連の報告「印字で見た」（✓）＋あいだに「逆」
TW = dict(l=(520.0, 470.0), r=(1400.0, 470.0), w=260.0, h=300.0)


def twosay_base(st0):
    return []


def twosay_stage(prev, st):
    s = []
    w, h = TW["w"], TW["h"]
    if _on(prev, st, "right"):
        x, y = TW["r"]
        s.append(_printout(x - w / 2, y - h / 2, w, h, rep_col("c91"), nlines=5, skip=(y - 80, y + 80)))   # 🔧 geom_gap：「？」の下の行
        s.append(F.circ(x, y, 64, J.BG2, None))
        s.append(_qmark(x, y, 110, J.AMBER))
        s.append(_rep(x, y + h / 2 + 90, "c91", "値を知らなかった", cap=28))
    if _on(prev, st, "left"):
        x, y = TW["l"]
        s.append(_printout(x - w / 2, y - h / 2, w, h, rep_col("s86"), nlines=5, skip=(y - 80, y + 80)))
        s.append(F.circ(x, y, 64, J.BG2, None))
        s.append(_check(x, y, 40, J.OK))
        s.append(_rep(x, y + h / 2 + 90, "s86", "印字で見た", cap=28))
        s.append(_arrow(760.0, 470.0, 1160.0, 470.0, J.AMBER, 6, 24))
        s.append(_arrow(1160.0, 470.0, 760.0, 470.0, J.AMBER, 6, 24))
        s.append(_tline(CX, 436.0, "逆", 48, J.AMBER, "middle", 120))
    return s


# ── meaning（c608）＝残す棒の下限の札 → 1行目＝左＝運転員の受け取り「分布を整えるため」（出力の分布の線が平らに）／2行目＝右＝1992年の報告「安全のため」（盾）
MN = dict(card=(960.0, 350.0, 520.0, 84.0), l=(560.0, 640.0), r=(1360.0, 640.0))


def meaning_base(st0):
    cx, cy, w, h = MN["card"]
    return [_card(cx, cy, w, h, STEEL, sw=5), F.rect(cx - w / 2 + 30, cy - 30, 18, 60, STEEL, None, None, rx=4),
            _tline(cx + 20, cy + 11, "残す棒の下限", 32, INK, "middle", w - 100)]


def _shield(cx, cy, w, h, col):
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h * 0.1), (cx, cy + h / 2), (cx - w / 2, cy + h * 0.1)]
    return F.poly(pts, col, None, close=True, op=0.22) + F.poly(pts, "none", col, 6, close=True)


def meaning_stage(prev, st):
    s = []
    cx, cy, w, h = MN["card"]
    if _on(prev, st, "thought"):
        x, y = MN["l"]
        s.append(F.line(cx - 120, cy + h / 2 + 4, x + 40, 436.0, J.TICK, 3, dash="8 8"))     # 机上：字の上 8px＝字から離す
        s.append(_tline(x, 484.0, "分布を整えるため", 30, INK, "middle", 360))
        s.append(_tline(x, 522.0, "運転員の受け取り", 24, J.TICK, "middle", 300))
        s.append(F.rect(x - 180, 700.0, 360, 24, "#2b3a44", GRAPH, 3, rx=6))
        bump = [(x - 170 + 340 * i / 16, 690.0 - 70 * abs(math.sin(math.pi * i / 4))) for i in range(17)]
        s.append(F.poly(bump, "none", J.TICK, 3, dash="6 6"))
        s.append(F.line(x - 170, 630.0, x + 170, 630.0, J.AMBER, 5))
    if _on(prev, st, "real"):
        x, y = MN["r"]
        s.append(F.line(cx + 120, cy + h / 2 + 4, x - 40, 440.0, J.TICK, 3, dash="8 8"))
        s.append(_rep(x, 470.0, "r92", None, cap=26))
        s.append(_shield(x, 620.0, 150, 170, rep_col("r92")))
        s.append(_tline(x, 770.0, "安全のため", 34, rep_col("r92"), "middle", 300))
    return s


# ── go（c609）＝開始の合図の灯（3つ）：1行目（聞き役）＝消えている／2行目＝緑に点く・1:23:04 試験が始まる（S3 p2021）
GO_T = "1:23:04"
GO = dict(x0=680.0, y0=360.0, w=560.0, h=140.0, xs=(790.0, 960.0, 1130.0))


def go_base(st0):
    g = [F.rect(GO["x0"], GO["y0"], GO["w"], GO["h"], J.BG2, J.LINE, 5, rx=24),
         F.line(CX, GO["y0"] + GO["h"], CX, GO["y0"] + GO["h"] + 60, J.LINE, 8)]
    for x in GO["xs"]:
        g.append(F.circ(x, GO["y0"] + GO["h"] / 2, 46, J.BG, J.LINE_DIM, 4))
    return g


def go_stage(prev, st):
    s = []
    if _on(prev, st, "start"):
        for x in GO["xs"]:
            s.append(F.circ(x, GO["y0"] + GO["h"] / 2, 46, J.OK, J.BG, 4))
        s.append(_bigtime(CX, 690.0, GO_T, 110))
        s.append(_tline(CX, 772.0, "試験が始まる", 32, J.OK, "middle", 400))
    return s


# ── valve8（c610）＝横から見た蒸気の管・弁・8号タービン（模式）：1行目＝弁に×・蒸気が消える・回る勢いだけで回る（弧の矢印）／2行目＝話が分かれる（2つの報告）
V8_N = 8
V8 = dict(y=470.0, x0=140.0, valve=560.0, tb=1180.0, s=1.2)


def valve8_base(st0):
    y, vx, tx = V8["y"], V8["valve"], V8["tb"]
    return [F.line(V8["x0"], y, tx - 210, y, "#cfd8dc", 18, op=0.5), _tline(V8["x0"] + 10, y - 30, "蒸気", 28, INK, "start", 120),
            F.poly([(vx - 40, y - 34), (vx + 40, y + 34), (vx + 40, y - 34), (vx - 40, y + 34)], STEEL, J.BG, 4, close=True),
            _tline(vx, y - 60, "弁", 28, STEEL, "middle", 120), _turbine(tx, y, V8["s"]),
            _tline(tx, y + 150, f"{V8_N}号タービン", 32, INK, "middle", 300)]


def valve8_stage(prev, st):
    s = []
    y, vx, tx = V8["y"], V8["valve"], V8["tb"]
    if _on(prev, st, "shut"):
        s.append(F.line(vx + 50, y, tx - 214, y, J.BG, 20, op=0.75))
        s.append(_xmark(vx, y, 50, J.ALERT, 11))
        s.append(_arc_arrow(tx, y, 260, 110, 200, 320, J.AMBER, 6, 22))
        s.append(_arc_arrow(tx, y, 260, 110, 20, 140, J.AMBER, 6, 22))
        s.append(_tline(tx, y - 170, "勢いだけで回る", 30, J.AMBER, "middle", 300))
    if _on(prev, st, "fork"):
        s.append(F.line(CX, 668.0, CX, 700.0, J.LINE, 5))
        s.append(_arrow(CX, 700.0, 680.0, 742.0, rep_col("s86"), 5, 20))
        s.append(_arrow(CX, 700.0, 1240.0, 742.0, rep_col("c91"), 5, 20))
        s.append(_rep(560.0, 792.0, "s86", None, cap=24))
        s.append(_rep(1360.0, 792.0, "c91", None, cap=24))
        s.append(_tline(CX, 648.0, "話が分かれる", 28, J.TICK, "middle", 300))
    return s


# ── flow35（c612）＝試験の35秒（横＝秒）：1行目＝1991年の委員会・出力の線は平ら／2行目＝水の流れの線が下がり、35秒で10〜15%（終わりの帯）＝S1 p75
FW_SEC, FW_DROP = 35, (10, 15)
FW = dict(x0=360.0, x1=1460.0, yb=780.0, yp=430.0, yf=520.0, k=12.0)


def fw_band():
    return tuple(FW["yf"] + FW["k"] * d for d in FW_DROP)


def flow35_base(st0):
    x0, x1, yb = FW["x0"], FW["x1"], FW["yb"]
    g = [F.line(x0, yb, x1 + 40, yb, J.TICK, 4), F.line(x0, yb, x0, 360.0, J.TICK, 4)]
    for x, t in ((x0, "0"), (x1, f"{FW_SEC}秒")):
        g.append(F.line(x, yb - 10, x, yb + 10, J.TICK, 4))
        g.append(_tline(x, yb + 44, t, 28, J.TICK, "middle", 160))
    g.append(_tline(x1 + 70, yb + 10, "試験の始まりから", 24, J.TICK, "start", 240))
    return g


def flow35_stage(prev, st):
    s = []
    x0, x1 = FW["x0"], FW["x1"]
    if _on(prev, st, "power"):
        s.append(_rep(1560.0, 330.0, "c91", None, cap=26))
        s.append(F.line(x0, FW["yp"], x1, FW["yp"], J.AMBER, 7))
        s.append(_tline(x1 + 20, FW["yp"] + 10, "出力：上がらない", 28, J.AMBER, "start", 300))
    if _on(prev, st, "flow"):
        b0, b1 = fw_band()
        ym = (b0 + b1) / 2
        pts = [(x0 + (x1 - x0) * i / 20, FW["yf"] + (ym - FW["yf"]) * (i / 20) ** 1.3) for i in range(21)]
        s.append(F.rect(x1 - 16, b0, 32, b1 - b0, WATER, None, None, op=0.35))
        s.append(F.poly(pts, "none", WATER, 7))
        s.append(_tline(x1 + 30, ym + 10, f"水の流れ {FW_DROP[0]}〜{FW_DROP[1]}%減", 26, WATER, "start", 300))
    return s


# ── digital（c614）＝🔴 c402 の丸い時計と別の形＝数字の時計と AZ-5 のボタン：1行目＝1991年の委員会：押した理由は確かめられず／
#    2行目＝時計 1:23:40・ボタンが光る・すべての棒を下ろす（S1 p65・p76）
DG_T = "1:23:40"
DG = dict(clk=(900.0, 330.0, 600.0, 180.0), btn=(1200.0, 680.0), rep=(480.0, 420.0))


def _az5(bx, by):
    return (F.circ(bx, by, 84, J.BG2, J.LINE, 6) + F.circ(bx, by, 64, J.ALERT, None)
            + _tline(bx, by + 12, "AZ-5", 34, INK, "middle", 120))


def digital_base(st0):
    x, y, w, h = DG["clk"]
    return [F.rect(x, y, w, h, J.BG, J.LINE, 6, rx=16), _az5(*DG["btn"])]


def digital_stage(prev, st):
    s = []
    if _on(prev, st, "why"):
        s.append(_rep(*DG["rep"], "c91", "理由は確かめられず", cap=28))
        s.append(_qmark(DG["rep"][0], 600.0, 120, J.AMBER))
    if _on(prev, st, "press"):
        x, y, w, h = DG["clk"]
        s.append(_tline(x + w / 2, y + h / 2 + 40, DG_T, 110, J.AMBER, "middle", w - 40, fam="Dela"))
        bx, by = DG["btn"]
        # 🔧 門番 layout：字を丸ごと囲む輪は「上から下へ貫く線」と数えられた＝左右の弧に分ける（字の幅の上と下に点を置かない）
        for a0, a1 in ((-60.0, 60.0), (120.0, 240.0)):
            s.append(F.poly(_arcpts(bx, by, 104, 104, a0, a1, 16), "none", J.ALERT, 5))
        s.append(_tline(bx + 130, by + 12, "すべての棒を下ろす", 28, INK, "start", 300))
    return s


# ── spike（c616）＝縦の出力の計器（🔴 c301 の丸い針と別の形）：530MW の目盛り（長さは値に比例）→ 1行目＝急上昇の信号の灯・1:23:43／
#    2行目＝棒が目盛りを超えて上へ（S1 p65「power exceeded 530 MW(th)」）
SP_T, SP_V = "1:23:43", 530
SPK = dict(x=720.0, w=120.0, y0=800.0, top=330.0, k=380.0 / 530.0, lamp=(1320.0, 420.0))


def spk_y(v):
    return SPK["y0"] - SPK["k"] * v


def spike_base(st0):
    x, w, y0, top = SPK["x"], SPK["w"], SPK["y0"], SPK["top"]
    yt = spk_y(SP_V)
    return [F.rect(x, top, w, y0 - top, J.BG2, J.LINE, 5, rx=8), F.line(x - 20, yt, x + w + 20, yt, J.AMBER, 5),
            _tline(x + w + 40, yt + 12, f"{SP_V}MW", 36, J.AMBER, "start", 260, fam="Dela"),
            _tline(x + w / 2, y0 + 44, "出力", 26, J.TICK, "middle", 160)]


def spike_stage(prev, st):
    s = []
    lx, ly = SPK["lamp"]
    if _on(prev, st, "sig"):
        s.append(F.circ(lx, ly, 46, J.ALERT, None))
        for i in range(8):
            a = math.radians(45 * i)
            s.append(F.line(lx + 62 * math.cos(a), ly + 62 * math.sin(a), lx + 84 * math.cos(a), ly + 84 * math.sin(a), J.ALERT, 5))
        s.append(_tline(lx, ly + 150, "急上昇の信号", 32, J.ALERT, "middle", 300))
        s.append(_bigtime(lx, ly + 250, SP_T, 76))
    if _on(prev, st, "over"):
        x, w = SPK["x"], SPK["w"]
        s.append(F.rect(x + 12, SPK["top"] + 10, w - 24, SPK["y0"] - SPK["top"] - 22, J.AMBER, None, None, rx=4, op=0.85))
        s.append(_arrow(x + w / 2, SPK["top"] + 4, x + w / 2, SPK["top"] - 50, J.ALERT, 7, 24))
        s.append(_tline(x + w + 40, spk_y(SP_V) - 48, "超えた", 30, J.ALERT, "start", 200))
    return s


def spike_top():
    return SPK["top"] + 10


# ── rodstop（c617）＝横から見た棒の通り道（模式）：1行目＝棒が下りて途中で止まる（動く部品・下の端に届かない）・1986年のソ連の報告／
#    2行目＝動かす装置の電気を切った（稲妻に×）→ 重さで落とす（S1 p65・S3 p2021）
RS = dict(core=(700.0, 380.0, 1000.0, 800.0), ch=(830.0, 870.0), drive=(850.0, 320.0), lim=790.0, rod=(350.0, 560.0), drop=170.0, rep=(1460.0, 430.0))


def rs_bottom(st=None):
    on = (st or {}).get("stop") == "on"
    return RS["rod"][1] + (RS["drop"] if on else 0.0)


def rodstop_base(st0):
    x0, y0, x1, y1 = RS["core"]
    c0, c1 = RS["ch"]
    dx, dy = RS["drive"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, "#2b3a44", GRAPH, 4, rx=8), F.rect(c0, y0 - 20, c1 - c0, y1 - y0 + 20, J.BG, J.LINE_DIM, 3),
            F.rect((c0 + c1) / 2 - 40, RS["lim"] - 8, 80, 16, J.AMBER, None, None, rx=3),
            _tline(x1 + 30, RS["lim"] + 10, "下の端", 26, J.AMBER, "start", 160),
            F.rect(dx - 90, dy - 28, 180, 56, J.BG2, STEEL, 4, rx=8), _tline(dx + 120, dy + 10, "動かす装置", 26, STEEL, "start", 220),
            _tline(x0 - 24, (y0 + y1) / 2, "炉", 28, J.TICK, "end", 100)]


def rodstop_parts(st):
    c0, c1 = RS["ch"]
    t, b = RS["rod"]
    dy = RS["drop"] if st.get("stop") == "on" else 0.0
    return [_P("rod", "poly", [(c0 + 6, t), (c1 - 6, t), (c1 - 6, b), (c0 + 6, b)], fill=STEEL, stroke=J.BG, w=3, alpha=1.0, dy=dy)]


def rodstop_stage(prev, st):
    s = []
    c0, c1 = RS["ch"]
    x1 = RS["core"][2]
    if _on(prev, st, "stop"):
        yb = rs_bottom(st) + 6
        s.append(F.line(c0 - 30, yb, c1 + 30, yb, J.ALERT, 6))
        s.append(_tline(x1 + 30, yb + 10, "ここで止まる", 28, J.ALERT, "start", 240))
        s.append(_rep(*RS["rep"], "s86", None, cap=26))
    if _on(prev, st, "cut"):
        dx, dy = RS["drive"]
        s.append(_bolt(dx - 150, dy, 26, J.AMBER))
        s.append(_xmark(dx - 150, dy, 22, J.ALERT, 7))
        s.append(_arrow(c1 + 50, 560.0, c1 + 50, 690.0, J.ALERT, 5, 20, dash="10 8"))
        s.append(_tline(x1 + 30, 630.0, "重さで落とす", 28, INK, "start", 240))
        s.append(_tline(RS["rep"][0], RS["rep"][1] + 70, "電気を切った", 30, rep_col("s86"), "middle", 300))
    return s


# ── why8（c620）＝1行目（聞き役）：AZ-5 のボタン → 爆発（星形）と「？」／2行目＝手がかり＝止める棒の形（棒の影）・第8章の札
W8_CH = 8
W8 = dict(btn=(420.0, 520.0), burst=(980.0, 520.0), rod=(1460.0, 360.0, 1520.0, 700.0))


def _burst(cx, cy, r0, r1, n=12):
    return [(cx + (r0 if i % 2 == 0 else r1) * math.cos(math.pi * i / n), cy + (r0 if i % 2 == 0 else r1) * math.sin(math.pi * i / n))
            for i in range(2 * n)]


def why8_base(st0):
    bx, by = W8["btn"]
    cx, cy = W8["burst"]
    return [_az5(bx, by), _arrow(bx + 110, by, cx - 170, cy, J.LINE, 7, 26),
            F.poly(_burst(cx, cy, 150, 90), J.AMBER, J.ALERT, 5, close=True, op=0.9), F.txt(cx, cy + 38, "？", 110, J.BG, "Noto", "middle")]


def why8_stage(prev, st):
    s = []
    if _on(prev, st, "hint"):
        x0, y0, x1, y1 = W8["rod"]
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, "#3a4650", J.LINE_DIM, 3, rx=10))
        s.append(_qmark((x0 + x1) / 2, (y0 + y1) / 2, 56, J.AMBER))
        s.append(_tline(x0 - 40, (y0 + y1) / 2 + 10, "手がかり：棒の形", 28, J.TICK, "end", 300))
        s.append(_card((x0 + x1) / 2, y1 + 72, 200, 64, J.AMBER, sw=5))
        s.append(_tline((x0 + x1) / 2, y1 + 85, f"第{W8_CH}章", 32, J.AMBER, "middle", 170))
    return s


# ── roof（c701）＝上から見た4号機とタービンの建屋（配置は模式）：1行目（聞き役）＝建屋だけ／2行目＝燃える塊と火花が屋根へ（点線の弧）・火の印／
#    3行目＝1986年のソ連の報告（S3 p2021）。🔴 火は赤と黄（燃料の橙・ソ連の報告の橙と分ける）
RF = dict(hall=(200.0, 600.0, 1720.0, 760.0), unit=(1180.0, 330.0, 1520.0, 560.0), fires=((640.0, 680.0), (900.0, 650.0), (1120.0, 700.0)),
          src=(1300.0, 360.0), rep=(560.0, 420.0))


def _flame(cx, cy, s=1.0):
    pts = [(cx, cy - 46 * s), (cx + 22 * s, cy - 10 * s), (cx + 26 * s, cy + 14 * s), (cx, cy + 26 * s), (cx - 26 * s, cy + 14 * s), (cx - 22 * s, cy - 10 * s)]
    inner = [(x * 0.55 + cx * 0.45, y * 0.55 + (cy + 8 * s) * 0.45) for x, y in pts]
    return F.poly(pts, J.ALERT, None, close=True) + F.poly(inner, J.AMBER, None, close=True)


def roof_base(st0):
    hx0, hy0, hx1, hy1 = RF["hall"]
    ux0, uy0, ux1, uy1 = RF["unit"]
    g = [F.rect(hx0, hy0, hx1 - hx0, hy1 - hy0, J.BG2, J.LINE, 5, rx=6)]
    for x in range(int(hx0 + 400), int(hx1), 160):           # 机上：屋根の継ぎ目の線が「タービンの建屋」の字を横切った＝字の右から
        g.append(F.line(x, hy0 + 8, x, hy1 - 8, J.LINE_DIM, 3))
    g += [_tline(hx0 + 40, hy1 - 22, "タービンの建屋", 28, INK, "start", 300),
          F.rect(ux0, uy0, ux1 - ux0, uy1 - uy0, "#2b3a44", J.LINE, 5, rx=6), _tline((ux0 + ux1) / 2, (uy0 + uy1) / 2 + 12, "4号機", 34, INK, "middle", 260)]
    return g


def roof_stage(prev, st):
    s = []
    if _on(prev, st, "fall"):
        x0, y0 = RF["src"]
        for tx, ty in RF["fires"]:
            pts = [(x0 + (tx - x0) * u / 16, y0 + (ty - y0) * u / 16 - 480 * (u / 16) * (1 - u / 16)) for u in range(17)]
            s.append(F.poly(pts, "none", J.AMBER, 4, dash="10 10"))
            s.append(_flame(tx, ty, 1.0))
        for dx, dy in ((-40, -30), (30, -60), (-10, -90)):
            s.append(F.circ(x0 + dx, y0 + dy, 7, J.AMBER, None))
    if _on(prev, st, "s86"):
        s.append(_rep(*RF["rep"], "s86", "屋根に落ち、火事に", cap=28))
    return s


# ── dayband（c706）＝26日の24時間の帯（時刻に比例・空の色＝夜・朝・昼・夕・夜）と27日へ続く破線（🔴 c311 の帯と別の形）：
#    1行目＝朝・窓と戸を閉めた家（S2 p1082）／2行目＝22:00 避難を決める（L2 p3024）。🔴 27日の時刻（正午・14:00〜17:00）は c707・c708 で＝ここは書かない
DB_T = "22:00"
DB = dict(x0=220.0, x1=1520.0, y=470.0, h=70.0, ext=1780.0, house=8.0)
DB_SEG = ((0, 5, "#1c2740"), (5, 7, "#3a4d63"), (7, 18, "#4a6a82"), (18, 20, "#3a4d63"), (20, 24, "#1c2740"))


def db_x(hh):
    return DB["x0"] + (DB["x1"] - DB["x0"]) * hh / 24.0


def db_h(t):
    h, m = (int(v) for v in t.split(":"))
    return h + m / 60.0


def dayband_base(st0):
    y, h = DB["y"], DB["h"]
    g = [F.rect(db_x(a), y, db_x(b) - db_x(a), h, col, None, None) for a, b, col in DB_SEG]
    g += [F.rect(DB["x0"], y, DB["x1"] - DB["x0"], h, "none", J.LINE_DIM, 3),
          F.rect(DB["x1"], y, DB["ext"] - DB["x1"], h, "none", J.LINE_DIM, 3, dash="10 8"),
          _tline(DB["x0"], y + h + 50, "26日", 28, J.TICK, "start", 120), _tline((DB["x1"] + DB["ext"]) / 2, y + h + 50, "27日", 28, J.TICK, "middle", 120),
          F.circ(db_x(12), y - 40, 22, J.AMBER, None), _moon(db_x(2), y - 40, 20)]
    return g


def dayband_stage(prev, st):
    s = []
    y, h = DB["y"], DB["h"]
    if _on(prev, st, "indoor"):
        x = db_x(DB["house"])
        s.append(F.rect(x - 55, 330.0, 110, 80, J.BG2, J.LINE, 4))
        s.append(F.poly([(x - 70, 332.0), (x + 70, 332.0), (x, 280.0)], J.BG2, J.LINE, 4, close=True))
        for wx in (x - 30, x + 10):
            s.append(F.rect(wx, 350.0, 22, 26, J.BG, J.AMBER, 3))
            s.append(F.line(wx, 350.0, wx + 22, 376.0, J.AMBER, 3))
        s.append(_arrow(x, 416.0, x, y - 6, J.LINE, 4, 16))
        s.append(_tline(x, y + h + 50, "窓と戸を閉め家の中に", 26, INK, "middle", 360))
    if _on(prev, st, "decide"):
        x = db_x(db_h(DB_T))
        s.append(F.line(x, y - 30, x, y + h + 20, J.AMBER, 6))
        s.append(_tline(x, y - 50, DB_T, 44, J.AMBER, "middle", 220, fam="Dela"))
        s.append(_tline(x, y + h + 100, "避難を決める", 32, J.AMBER, "middle", 300))
    return s


# ── notice（c714）＝🔴 c206 の7枚の札と別の形＝掲示の紙と絵の札：1行目＝紙「注意」5月4日 早朝・放射能対策本部／2行目＝雨水（しずく）→ 木炭でこす（コップ）／
#    3行目＝水道水・井戸水・牛乳（3つの絵）＝心配ない（国会会議録 1986-05-07・葉もの野菜は次の c715 の頁）
NT_DATE = (5, 4)
NC = dict(paper=(180.0, 300.0, 440.0, 510.0), p1=450.0, p2=680.0)


def notice_base(st0):
    x, y, w, h = NC["paper"]
    g = [F.rect(x, y, w, h, J.BG2, J.DOC, 5, rx=6), F.rect(x, y, w, 70, J.DOC_DIM, None, None, rx=6)]
    for i in range(5):
        g.append(F.line(x + 40, 560.0 + i * 46, x + w - 40 - 80 * (i % 2), 560.0 + i * 46, J.LINE_DIM, 8))
    return g


def notice_stage(prev, st):
    s = []
    x, y, w, h = NC["paper"]
    if _on(prev, st, "head"):
        s.append(_tline(x + w / 2, y + 48, "注意", 36, INK, "middle", w - 40))
        s.append(_tline(x + w / 2, y + 130, f"{NT_DATE[0]}月{NT_DATE[1]}日　早朝", 32, J.AMBER, "middle", w - 40))
        s.append(_tline(x + w / 2, y + 180, "放射能対策本部", 26, J.TICK, "middle", w - 40))
    if _on(prev, st, "rain"):
        cy = NC["p1"]
        s.append(F.circ(780.0, cy + 14, 30, WATER, None))
        s.append(F.poly([(754.0, cy + 2), (806.0, cy + 2), (780.0, cy - 54)], WATER, None, close=True))
        s.append(_arrow(830.0, cy, 880.0, cy, J.LINE, 5, 18))
        s.append(F.poly([(900.0, cy - 50), (1000.0, cy - 50), (986.0, cy + 60), (914.0, cy + 60)], "none", J.LINE, 5, close=True))
        s.append(F.poly([(906.0, cy + 14), (994.0, cy + 14), (986.0, cy + 60), (914.0, cy + 60)], "#3a4650", None, close=True))
        for dx in (-24, 0, 24):
            s.append(F.circ(950.0 + dx, cy + 38, 6, J.BG, None))
        s.append(_tline(1050.0, cy - 12, "雨水をじかに飲むなら", 26, J.TICK, "start", 420))
        s.append(_tline(1050.0, cy + 36, "木炭でこす", 34, INK, "start", 420))
    if _on(prev, st, "tap"):
        cy = NC["p2"]
        # 水道の蛇口・井戸・牛乳びん（模式）
        s.append(F.rect(740.0, cy - 30, 70, 20, J.LINE, None, None, rx=4))
        s.append(F.rect(790.0, cy - 12, 20, 36, J.LINE, None, None, rx=4))
        s.append(F.rect(756.0, cy - 50, 16, 22, J.LINE, None, None, rx=3))
        s.append(F.rect(860.0, cy - 6, 90, 50, J.BG2, J.LINE, 4))
        s.append(F.poly([(850.0, cy - 6), (960.0, cy - 6), (905.0, cy - 50)], "none", J.LINE, 4, close=True))
        s.append(F.rect(1000.0, cy - 30, 48, 74, J.BG2, J.LINE, 4, rx=8))
        s.append(F.rect(1012.0, cy - 54, 24, 26, J.BG2, J.LINE, 4, rx=4))
        for xx, t in ((775.0, "水道水"), (905.0, "井戸水"), (1024.0, "牛乳")):
            s.append(_tline(xx, cy + 90, t, 24, J.TICK, "middle", 120))
        s.append(_check(1120.0, cy, 26, J.OK))
        s.append(_tline(1170.0, cy + 14, "心配ない", 38, J.OK, "start", 300))
    return s


# ── table6（c806）＝1986年のソ連の報告の違反の表（3つの列 × 6つの行・字は省いた）：1行目＝列の名（違反・動機・結果）／
#    2行目＝2行目の動機の欄だけ「運転員の誤り」（0時28分の急落の行＝S3 p2026）
TB6_ROWS, TB6_COLS, TB6_MARK = 6, ("違反", "動機", "結果"), (2, 2)
# 🔧 geom_gap：印の欄の灰の線が「運転員の誤り」の下を通った＝その欄は線を描かない（ほかに2つ空けて、印の欄を先に知らせない）
TB6_BLANK = (TB6_MARK, (4, 3), (6, 1))
T6 = dict(x0=420.0, x1=1560.0, y0=350.0, hh=60.0, rh=64.0)


def t6_cell(r, c):
    cw = (T6["x1"] - T6["x0"]) / len(TB6_COLS)
    y = T6["y0"] + T6["hh"] + (r - 1) * T6["rh"]
    return (T6["x0"] + (c - 1) * cw, y, T6["x0"] + c * cw, y + T6["rh"])


def table6_base(st0):
    x0, x1, y0 = T6["x0"], T6["x1"], T6["y0"]
    y1 = y0 + T6["hh"] + TB6_ROWS * T6["rh"]
    g = [F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.DOC, 5, rx=6), F.line(x0, y0 + T6["hh"], x1, y0 + T6["hh"], J.DOC, 4)]
    for c in range(1, len(TB6_COLS)):
        xx = t6_cell(1, c)[2]
        g.append(F.line(xx, y0, xx, y1, J.DOC_DIM, 3))
    for r in range(1, TB6_ROWS + 1):
        if r > 1:
            g.append(F.line(x0, t6_cell(r, 1)[1], x1, t6_cell(r, 1)[1], J.DOC_DIM, 2))
        for c in range(1, len(TB6_COLS) + 1):
            if (r, c) in TB6_BLANK:
                continue
            a, b, cc, d = t6_cell(r, c)
            g.append(F.line(a + 30, (b + d) / 2, cc - 30 - 70 * ((r + c) % 2), (b + d) / 2, J.LINE_DIM, 8))
    return g


def table6_stage(prev, st):
    s = []
    if _on(prev, st, "cols"):
        for c, t in enumerate(TB6_COLS, 1):
            a, _b, cc, _d = t6_cell(1, c)
            s.append(_tline((a + cc) / 2, T6["y0"] + 42, t, 32, J.DOC, "middle", cc - a - 20))
        s.append(_rep(1300.0, 300.0, "s86", None, cap=24))
    if _on(prev, st, "mark"):
        a, b, cc, d = t6_cell(*TB6_MARK)
        s.append(F.rect(a + 4, b + 4, cc - a - 8, d - b - 8, J.BG2, J.AMBER, 5, rx=6))
        s.append(_tline((a + cc) / 2, (b + d) / 2 + 11, "運転員の誤り", 30, J.AMBER, "middle", cc - a - 30))
        s.append(_tline(T6["x0"] - 20, (b + d) / 2 + 10, "0時28分の急落", 28, J.AMBER, "end", 330))
    return s


# ── pile（c808）＝6つの札（字なし＝表の6つの行）が1か所に重なる（動く部品）：1行目＝1986年のソ連の報告「主な原因：違反の重なり」／2行目＝説明の芯の輪
PL6 = 6
PIL = dict(cx=960.0, cy=540.0, rx=600.0, ry=120.0, w=230.0, h=104.0, rep=(960.0, 320.0))
PIL_COLS = ("LINE", "AMBER", "OK", "ALERT", "ship", "DOC")


def pile_xy(i):
    a = math.radians(360.0 / PL6 * i)
    return PIL["cx"] + PIL["rx"] * math.cos(a), PIL["cy"] + PIL["ry"] * math.sin(a)


def pile_parts(st):
    on = st.get("pile") == "on"
    out = []
    for i in range(PL6):
        x, y = pile_xy(i)
        w, h = PIL["w"], PIL["h"]
        tx, ty = PIL["cx"] + (i - (PL6 - 1) / 2) * 12, PIL["cy"] + (i - (PL6 - 1) / 2) * 8
        out.append(_P(f"card{i}", "poly", [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)],
                      pivot=[x, y], rot=(-10.0 + 4.0 * i) if on else 0.0, fill=J.BG2, stroke=rc(PIL_COLS[i % len(PIL_COLS)]), w=6,
                      alpha=1.0, dx=(tx - x) if on else 0.0, dy=(ty - y) if on else 0.0, lag=0.07 * i))
    return out


def pile_base(st0):
    return []


def pile_stage(prev, st):
    s = []
    if _on(prev, st, "pile"):
        s.append(_rep(*PIL["rep"], "s86", "主な原因：違反の重なり", cap=26))
    if _on(prev, st, "core"):
        s.append(F.poly(_arcpts(PIL["cx"], PIL["cy"], 240.0, 150.0, 0, 360, 48), "none", J.AMBER, 5, dash="14 10"))
        s.append(_tline(PIL["cx"], 790.0, "職員の違反＝説明の芯", 32, J.AMBER, "middle", 600))
    return s


# ── carry（c810）＝炉と「正のボイド係数」の札 → 1行目＝急上昇を大きくする（上向きの矢印）／2行目＝職員の箱から太い矢印・規則の外の状態（破線の枠）＝
#    1986年のソ連の報告「持ち込んだのは職員」（S3 p2027）。🔴 人の形は描かない（箱だけ）
CR = dict(core=(780.0, 440.0, 1140.0, 690.0), staff=(380.0, 565.0), zone=(730.0, 370.0, 1190.0, 730.0), rep=(380.0, 380.0))


def carry_base(st0):
    x0, y0, x1, y1 = CR["core"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, "#2b3a44", GRAPH, 4, rx=8), _tline((x0 + x1) / 2, y1 - 30, "炉", 30, INK, "middle", 120)]


def carry_stage(prev, st):
    s = []
    x0, y0, x1, y1 = CR["core"]
    if _on(prev, st, "void"):
        s.append(_card((x0 + x1) / 2, y0 + 64, 320, 72, J.ALERT, sw=5))
        s.append(_tline((x0 + x1) / 2, y0 + 75, "正のボイド係数", 30, INK, "middle", 290))
        s.append(_arrow(1240.0, 680.0, 1240.0, 420.0, J.ALERT, 8, 28))
        s.append(_tline(1280.0, 560.0, "急上昇を大きく", 28, J.ALERT, "start", 300))
    if _on(prev, st, "staff"):
        zx0, zy0, zx1, zy1 = CR["zone"]
        s.append(F.rect(zx0, zy0, zx1 - zx0, zy1 - zy0, "none", J.ALERT, 4, rx=20, dash="14 10"))
        s.append(_tline((zx0 + zx1) / 2, zy1 + 44, "規則の外の状態", 28, J.ALERT, "middle", 300))
        sx, sy = CR["staff"]
        s.append(_card(sx, sy, 200, 90, J.LINE, sw=5))
        s.append(_tline(sx, sy + 12, "職員", 34, INK, "middle", 160))
        s.append(_arrow(sx + 110, sy, zx0 - 8, sy, J.LINE, 10, 32))
        s.append(_rep(*CR["rep"], "s86", "持ち込んだのは職員", cap=26))
    return s


# ── sizes（c813）＝1986年の報告の原因の文：大きな札「人の誤りと違反」＋小さな札「炉の性質」（1行目＝聞き役）→ 2行目＝根本：人的要素（S2 p1112）
SZ = dict(frame=(260.0, 420.0, 1660.0, 720.0), big=(760.0, 580.0, 620.0, 170.0), small=(1380.0, 580.0, 300.0, 90.0))


def sizes_base(st0):
    fx0, fy0, fx1, fy1 = SZ["frame"]
    bx, by, bw, bh = SZ["big"]
    sx, sy, sw_, sh = SZ["small"]
    col = rep_col("r86")
    return [_rep(CX, 330.0, "r86", None, cap=28), F.rect(fx0, fy0, fx1 - fx0, fy1 - fy0, "none", J.TICK, 3, rx=16, dash="10 10"),
            _tline(fx0 + 30, fy1 - 22, "原因を書いた文", 26, J.TICK, "start", 300),
            F.rect(bx - bw / 2, by - bh / 2, bw, bh, J.BG2, col, 8, rx=12), _tline(bx, by + 16, "人の誤りと違反", 44, INK, "middle", bw - 40),
            _tline((bx + bw / 2 + sx - sw_ / 2) / 2, by + 18, "＋", 56, J.TICK, "middle", 80),
            F.rect(sx - sw_ / 2, sy - sh / 2, sw_, sh, J.BG2, J.LINE, 4, rx=10), _tline(sx, sy + 10, "炉の性質", 28, INK, "middle", sw_ - 30)]


def sizes_stage(prev, st):
    s = []
    if _on(prev, st, "root"):
        bx, by, bw, bh = SZ["big"]
        col = rep_col("r86")
        s.append(F.rect(bx - 150, SZ["frame"][1] + 12, 300, 50, J.BG2, col, 4, rx=25))
        s.append(_tline(bx, SZ["frame"][1] + 46, "根本：人的要素", 28, col, "middle", 270))
    return s


def sz_area(k):
    _x, _y, w, h = SZ[k]
    return w * h


# ── door（c815）＝閉じた扉「ほかの説明」（模式）→ 錠・1986年の報告「探さなかった」（S2 p1047）
DO = dict(x=820.0, y=320.0, w=280.0, h=480.0, rep=(1460.0, 560.0))


def door_base(st0):
    x, y, w, h = DO["x"], DO["y"], DO["w"], DO["h"]
    return [F.rect(x - 20, y - 20, w + 40, h + 20, J.BG2, J.DOC_DIM, 6, rx=6), F.rect(x, y, w, h, "#2b3a44", J.LINE, 4, rx=4),
            F.rect(x + 30, y + 150, w - 60, 130, "none", J.LINE_DIM, 3, rx=4), F.rect(x + 30, y + 310, w - 60, 140, "none", J.LINE_DIM, 3, rx=4),
            F.circ(x + w - 40, y + 290, 12, J.AMBER, None),
            F.rect(x + 40, y + 50, w - 80, 66, J.BG2, J.AMBER, 4, rx=6), _tline(x + w / 2, y + 94, "ほかの説明", 28, INK, "middle", w - 100)]


def door_stage(prev, st):
    s = []
    if _on(prev, st, "shut"):
        lx, ly = DO["x"] + DO["w"] - 40, DO["y"] + 340
        s.append(F.poly(_arcpts(lx, ly - 4, 22, 28, 180, 360, 16), "none", J.AMBER, 7))
        s.append(F.rect(lx - 32, ly - 4, 64, 52, J.AMBER, None, None, rx=6))
        s.append(_rep(*DO["rep"], "r86", "探さなかった", cap=30))
    return s


# ── venn3（c816）＝重なる3つの輪（決まり・人・組織）と真ん中に「安全文化」（1行目）→ 2行目＝育てて保つ（回る矢印）＝1986年の報告（S2 p1018）
# 机上：真ん中の「安全文化」を輪の線が横切った＝輪を寄せて大きく（3つの輪がみな字を囲む・字と線は 11px 以上）
VN = (("決まり", "LINE", 880.0, 480.0), ("人", "OK", 1040.0, 480.0), ("組織", "AMBER", 960.0, 620.0))
VN_R = 170.0
VN_LAB = ((790.0, 440.0), (1130.0, 440.0), (960.0, 740.0))


def venn3_base(st0):
    return []


def venn3_stage(prev, st):
    s = []
    if _on(prev, st, "ring"):
        for (t, r, x, y), (lx, ly) in zip(VN, VN_LAB):
            s.append(F.circ(x, y, VN_R, rc(r), None, op=0.16))
            s.append(F.circ(x, y, VN_R, "none", rc(r), 5))
            s.append(_tline(lx, ly, t, 32, rc(r), "middle", 160))
        s.append(_tline(CX, 548.0, "安全文化", 32, INK, "middle", 200))
        s.append(_rep(1560.0, 330.0, "r86", None, cap=26))
    if _on(prev, st, "keep"):
        s.append(_arc_arrow(1500.0, 610.0, 56, 56, -60, 250, J.OK, 6, 20))
        s.append(_tline(1500.0, 720.0, "育てて保つ", 32, J.OK, "middle", 260))
    return s


# ── shield（c817）＝発電所（模式）に向かう赤い矢印＝運転員の誤り（1行目）→ 2行目＝あいだに盾「誤りに強い作り」・1986年の報告（S2 p1050）
SL = dict(bld=(1080.0, 450.0, 1500.0, 760.0), stack=(1120.0, 330.0, 1180.0, 450.0), sh=(900.0, 600.0), rep=(1560.0, 330.0))


def shield_base(st0):
    x0, y0, x1, y1 = SL["bld"]
    a0, b0, a1, b1 = SL["stack"]
    return [F.rect(a0, b0, a1 - a0, b1 - b0, J.BG2, J.LINE, 4), F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 5, rx=6),
            F.poly(_arcpts((x0 + x1) / 2 + 60, y0, 120, 70, 180, 360, 20), J.BG2, J.LINE, 5),
            _tline((x0 + x1) / 2, y1 + 44, "原子力発電所", 28, INK, "middle", 300)]


def shield_stage(prev, st):
    s = []
    if _on(prev, st, "err"):
        for (ya, yb) in ((480.0, 520.0), (600.0, 600.0), (720.0, 680.0)):
            s.append(_arrow(300.0, ya, 790.0, yb, J.ALERT, 6, 24))
            s.append(_xmark(280.0, ya, 14, J.ALERT, 5))
        s.append(_tline(300.0, 420.0, "運転員の誤り", 30, J.ALERT, "start", 300))
    if _on(prev, st, "r86"):
        s.append(_shield(SL["sh"][0], SL["sh"][1], 140, 220, J.OK))
        s.append(_tline(SL["sh"][0], 770.0, "誤りに強い作り", 32, J.OK, "middle", 300))
        s.append(_rep(*SL["rep"], "r86", "設計にも求めた", cap=26))
    return s


# ── table86（c820）＝1986年の会議の机（上から・模式）：紙3枚と空いた所（破線）→ 1行目＝「止める棒の特徴」が無い・1992年の報告／2行目＝報告は違ったものに（S1 p27）
TA = dict(x0=300.0, x1=1620.0, y0=540.0, y1=680.0, xs=(470.0, 770.0, 1070.0), slot=1380.0)


def table86_base(st0):
    g = [F.rect(TA["x0"], TA["y0"], TA["x1"] - TA["x0"], TA["y1"] - TA["y0"], J.DOC_DIM, J.DOC, 5, rx=40, op=None)]
    ym = (TA["y0"] + TA["y1"]) / 2
    for x in TA["xs"]:
        g.append(F.rect(x - 100, ym - 50, 200, 100, J.BG2, J.LINE, 3, rx=4))
        for i in range(2):
            g.append(F.line(x - 70, ym - 16 + i * 32, x + 70 - 40 * i, ym - 16 + i * 32, J.LINE_DIM, 6))
    g.append(_tline(TA["x0"] + 10, TA["y1"] + 50, "ウィーンの会議の机", 26, J.TICK, "start", 300))
    return g


def table86_stage(prev, st):
    s = []
    ym = (TA["y0"] + TA["y1"]) / 2
    if _on(prev, st, "cards"):
        x = TA["slot"]
        s.append(F.rect(x - 100, ym - 50, 200, 100, "none", J.AMBER, 4, rx=4, dash="10 8"))
        s.append(_qmark(x, ym, 56, J.AMBER))
        s.append(_tline(x, TA["y0"] - 26, "止める棒の特徴", 30, J.AMBER, "middle", 300))
        s.append(_rep(CX, 350.0, "r92", None, cap=26))
    if _on(prev, st, "r92"):
        s.append(_tline(CX, 450.0, "報告は違ったものに", 32, rep_col("r92"), "middle", 400))
    return s


# ── rod12（c822）＝横から見た制御棒（改造の計画＝1986年のソ連の報告）：1行目＝棒がいつも 1.2m 差してある（動く部品・深さは炉の高さ 7m に比例）／
#    2行目＝炉の下の方で反応が強まるのを防ぐ（S3 p2028・S1 p16）。押しのけ棒はまだ描かない（第8章）
RZ_M, RZ_H = 1.2, 7.0
RZ = dict(core=(600.0, 380.0, 1000.0, 800.0), xs=(660.0, 740.0, 860.0, 940.0), len=160.0, rep=(1480.0, 400.0))


def rz_depth():
    return (RZ["core"][3] - RZ["core"][1]) * RZ_M / RZ_H


def rod12_base(st0):
    x0, y0, x1, y1 = RZ["core"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, "#2b3a44", GRAPH, 4, rx=8), F.line(x0 - 20, y0, x1 + 20, y0, J.LINE, 4),
            _tline(x1 + 30, y1 - 10, f"炉（高さ {RZ_H:g}m）", 26, J.TICK, "start", 260)]


def rod12_parts(st):
    y0 = RZ["core"][1]
    dy = rz_depth() if st.get("ins") == "on" else 0.0
    return [_P(f"rod{i}", "poly", [(x - 12, y0 - RZ["len"]), (x + 12, y0 - RZ["len"]), (x + 12, y0), (x - 12, y0)], fill=STEEL, stroke=J.BG, w=3,
               alpha=1.0, dy=dy, lag=0.05 * i) for i, x in enumerate(RZ["xs"])]


def rod12_stage(prev, st):
    s = []
    x0, y0, x1, y1 = RZ["core"]
    if _on(prev, st, "ins"):
        d = rz_depth()
        bx = x1 + 30
        s.append(F.line(bx, y0, bx, y0 + d, J.AMBER, 4))
        s.append(F.line(bx - 12, y0, bx + 12, y0, J.AMBER, 4))
        s.append(F.line(bx - 12, y0 + d, bx + 12, y0 + d, J.AMBER, 4))
        s.append(_tline(bx + 26, y0 + d / 2 + 14, f"{RZ_M:g}m", 36, J.AMBER, "start", 160, fam="Dela"))
        s.append(_tline(bx + 26, y0 + d + 56, "いつも差しておく", 26, INK, "start", 300))
        s.append(_rep(*RZ["rep"], "s86", "改造の計画", cap=28))
    if _on(prev, st, "why"):
        s.append(F.rect(x0 + 6, y1 - 120, x1 - x0 - 12, 114, J.ALERT, None, None, rx=6, op=0.28))
        s.append(_check(x1 + 50, y1 - 66, 18, J.OK))
        s.append(_tline(x1 + 80, y1 - 56, "下の方で強まるのを防ぐ", 28, J.OK, "start", 380))
    return s


# ── rodq（c824）＝止める棒の影（上は塗り・下は破線＝まだ分からない形・「？」）→ 2行目＝第8章の札（事故の山場）
RQ_CH = 8
RQ = dict(x=900.0, w=120.0, y0=300.0, y1=800.0, mid=580.0)


def rodq_base(st0):
    x, w, y0, y1, ym = RQ["x"], RQ["w"], RQ["y0"], RQ["y1"], RQ["mid"]
    return [F.rect(x, y0, w, ym - y0, "#3a4650", J.LINE_DIM, 4, rx=10), F.rect(x + 40, ym, w - 80, 30, "#3a4650", None, None),
            F.rect(x, ym + 30, w, y1 - ym - 30, "none", J.AMBER, 4, rx=10, dash="12 10"), _qmark(x + w / 2, (ym + 30 + y1) / 2, 80, J.AMBER)]


def rodq_stage(prev, st):
    s = []
    if _on(prev, st, "next"):
        x = RQ["x"] + RQ["w"]
        s.append(_arrow(x + 30, 520.0, 1260.0, 520.0, J.AMBER, 5, 20, dash="10 8"))
        s.append(_card(1400.0, 520.0, 240, 90, J.AMBER, sw=5))
        s.append(_tline(1400.0, 535.0, f"第{RQ_CH}章", 40, J.AMBER, "middle", 200))
        s.append(_tline(1400.0, 620.0, "次の章へ", 28, J.TICK, "middle", 260))        # 🔧 門番 dup：見出し「事故の山場へ」を83%覆った
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
    # 🆕 ⑤b-5：第4〜7章
    guard=_v("保護の仕組み", ("two", "auto"), guard_base, guard_stage, guard_parts),
    drum=_v("横から見た蒸気ドラム", ("sep", "loop"), drum_base, drum_stage),
    drumtrip=_v("ドラムの保護", ("r86", "off"), drumtrip_base, drumtrip_stage),
    stage2=_v("ドラムの断面と保護", ("p036", "lv2"), stage2_base, stage2_stage),
    marks5=_v("札と2つの印", ("ok92", "notdone"), marks5_base, marks5_stage),
    tg2=_v("止まる順の流れ", ("flow", "r86"), tg2_base, tg2_stage),
    retry=_v("試験のやり直し", ("s86",), retry_base, retry_stage),
    shift=_v("外した時刻", ("move", "proc"), shift_base, shift_stage, shift_parts),
    shadow=_v("札と止める棒の影", ("card", "shade"), lambda st0: [], shadow_stage),
    seesaw=_v("1992年の報告の天秤", ("left", "right"), seesaw_base, seesaw_stage),
    light=_v("手順書と制御盤", ("both", "r92"), light_base, light_stage),
    test200=_v("試験の出力", ("stuck", "go"), test200_base, test200_stage),
    printout=_v("印字の紙", ("start", "s86"), printout_base, printout_stage),
    rods15=_v("棒の数の比べ", ("rows", "viol"), rods15_base, rods15_stage),
    weight=_v("重さの比べ", ("same", "big"), weight_base, weight_stage),
    skala=_v("計算機の画面", ("unrel", "unknown", "aware"), skala_base, skala_stage),
    twosay=_v("2つの言い方", ("right", "left"), twosay_base, twosay_stage),
    meaning=_v("下限の決まりの受け取り方", ("thought", "real"), meaning_base, meaning_stage),
    go=_v("開始の合図", ("start",), go_base, go_stage),
    valve8=_v("横から見た弁とタービン", ("shut", "fork"), valve8_base, valve8_stage),
    flow35=_v("出力と水の流れ", ("power", "flow"), flow35_base, flow35_stage),
    digital=_v("ボタンと時刻", ("why", "press"), digital_base, digital_stage),
    spike=_v("出力の計器", ("sig", "over"), spike_base, spike_stage),
    rodstop=_v("横から見た棒の通り道", ("stop", "cut"), rodstop_base, rodstop_stage, rodstop_parts),
    why8=_v("ボタンと爆発", ("hint",), why8_base, why8_stage),
    roof=_v("上から見た4号機と建屋", ("fall", "s86"), roof_base, roof_stage),
    dayband=_v("朝から夜への帯", ("indoor", "decide"), dayband_base, dayband_stage),
    notice=_v("注意の紙", ("head", "rain", "tap"), notice_base, notice_stage),
    table6=_v("表の列と行", ("cols", "mark"), table6_base, table6_stage),        # 🔧 門番 dup：見出し「違反の表」を丸ごと含んだ
    pile=_v("重なる札", ("pile", "core"), pile_base, pile_stage, pile_parts),
    carry=_v("炉の状態", ("void", "staff"), carry_base, carry_stage),
    sizes=_v("2つの札の大きさ", ("root",), sizes_base, sizes_stage),
    door=_v("扉と錠", ("shut",), door_base, door_stage),
    venn3=_v("重なる輪", ("ring", "keep"), venn3_base, venn3_stage),
    shield=_v("発電所と盾", ("err", "r86"), shield_base, shield_stage),
    table86=_v("会議の机", ("cards", "r92"), table86_base, table86_stage),
    rod12=_v("横から見た制御棒", ("ins", "why"), rod12_base, rod12_stage, rod12_parts),
    rodq=_v("棒の影", ("next",), rodq_base, rodq_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
# 原文の値・欄・項目の写し（左上に「模式」を付けない）
NOT_SCHEMATIC = ("years", "cards7", "cal", "orm", "off11", "grid3", "ring", "meter", "clock", "hold", "swap", "two91", "say3", "bars",
                 "pillars", "balance",
                 "marks5", "shift", "seesaw", "test200", "rods15", "table6")
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
    # 🆕 ⑤b-5：焼く側（build_jiko._draw_anim）は部品の線の太さ w を必ず数で読む＝None だと Actions の焼きで落ちる（試し焼き 39884985410）。
    #    机上の門番は動く部品を焼かないので素通りした＝型の入口で止める
    for p in per[0]:
        if not isinstance(p.get("w", 4), (int, float)):
            raise ValueError(f"m24：{view} の部品 {p.get('id')} の線の太さ w={p.get('w')!r}（数で書く・線なしでも 2 など）")
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
    # 🆕 ⑤b-5
    elif view == "guard":
        drops = tuple(parts_of("guard", s)[0]["dy"] for s in allst)
        out.update(n=GD_N, viol=tuple(VIOL[n - 1] for n in GD_N), order=(GD["sensor"][0], GD["relay"], GD["core"][0]), drops=drops,
                   rod_bot=GD["rtop"] + GD["rlen"] + drops[-1], core=GD["core"])
    elif view == "drum":
        out.update(per=len(DR["ys"]), left=DR["xl"] + DR["w"], right=DR["xr"], core=DR["core"])
    elif view == "drumtrip":
        out.update(t=DT_T, n=DT_N, viol=VIOL[DT_N - 1], gauges=DT_G)
    elif view == "stage2":
        out.update(t=S2_T, lv=S2D["lv"], wl=S2D["wl"])
    elif view == "marks5":
        out.update(n=MK_N, viol=VIOL[MK_N - 1])
    elif view == "tg2":
        out.update(t=TG_T86, n=TG_N, viol=VIOL[TG_N - 1], ys=TG["ys"], xm=tg_xy()[1])
    elif view == "retry":
        out.update(n=RT_N, span=RT["a"][1] - RT["a"][0])
    elif view == "shift":
        fin = [p["dx"] for p in parts_of("shift", allst[-1])][0]
        out.update(t86=SH_T86, m86=SH_M86, m92=SH_M92, x86=sh_x(SH_M86), x92=sh_x(SH_M86) + fin, x0=SH["x0"], x1=SH["x1"], span=SH["span"],
                   lab92=sh_lab92())
    elif view == "shadow":
        out.update(card=rep_box(SD["card"][0], SD["card"][1], "r86", SD_BODY, cap=32, w=SD["cw"]), body=SD_BODY)
    elif view == "seesaw":
        out.update(left=SW_L, right=SW_R, level=True)
    elif view == "test200":
        out.update(plan=T2_PLAN, act=T2_ACT, yp=t2_y(T2_PLAN), ya=t2_y(T2_ACT), y0=T2["y0"], k=T2["k"])
    elif view == "rods15":
        out.update(rule=RD_RULE, lo=RD_LO, hi=RD_HI, n=RD_N, viol=VIOL[RD_N - 1])
    elif view == "weight":
        out.update(n=WT_N, s86=WT["s"][2], s92=WT["b"][2])
    elif view == "skala":
        out.update(min=SK_MIN)
    elif view == "twosay":
        out.update(l=TW["l"], r=TW["r"])
    elif view == "go":
        out.update(t=GO_T)
    elif view == "valve8":
        out.update(n=V8_N, valve=V8["valve"], tb=V8["tb"])
    elif view == "flow35":
        out.update(sec=FW_SEC, drop=FW_DROP, band=fw_band(), yf=FW["yf"], k=FW["k"])
    elif view == "digital":
        out.update(t=DG_T)
    elif view == "spike":
        out.update(t=SP_T, v=SP_V, yt=spk_y(SP_V), y0=SPK["y0"], k=SPK["k"], top=spike_top())
    elif view == "rodstop":
        out.update(bot=rs_bottom(allst[-1]), lim=RS["lim"], drop=RS["drop"])
    elif view == "why8":
        out.update(ch=W8_CH)
    elif view == "roof":
        out.update(hall=RF["hall"], unit=RF["unit"], fires=RF["fires"])
    elif view == "dayband":
        out.update(t=DB_T, x=db_x(db_h(DB_T)), x0=DB["x0"], x1=DB["x1"], house=DB["house"])
    elif view == "notice":
        out.update(date=NT_DATE)
    elif view == "table6":
        out.update(rows=TB6_ROWS, cols=TB6_COLS, mark=TB6_MARK)
    elif view == "pile":
        fin = parts_of("pile", allst[-1])
        out.update(n=len(fin), spread=max(math.hypot(p["pts"][0][0] + p["pts"][2][0] + 2 * p["dx"] - 2 * PIL["cx"],
                                                     p["pts"][0][1] + p["pts"][2][1] + 2 * p["dy"] - 2 * PIL["cy"]) / 2 for p in fin))
    elif view == "sizes":
        out.update(big=sz_area("big"), small=sz_area("small"))
    elif view == "venn3":
        out.update(items=tuple(t for t, *_r in VN))
    elif view == "rod12":
        fin = parts_of("rod12", allst[-1])[0]["dy"]
        out.update(m=RZ_M, h=RZ_H, depth=fin, core_h=RZ["core"][3] - RZ["core"][1])
    elif view == "rodq":
        out.update(ch=RQ_CH)
    return out
