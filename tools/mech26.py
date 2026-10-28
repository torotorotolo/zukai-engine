# -*- coding: utf-8 -*-
"""mech26.py — 26本目（タイタニック号沈没事故・1912-04-14〜15）「図解」（2026-10-28 新設・⑤b-5＝第1〜5章の37カット）。

■ 何か
  25本目 `mech25` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。再現イラストではない＝「再現」の札は出さない。
  左上に見え方の名（頭は PLAN の見る向き＝横から・上から・正面・時間の線／模式の見え方は末尾に「・模式」）・左下に注（模式の見え方は「模式」）と出典。
  🔴 人は役職だけ（名前は画面に出さない＝台本 §1-4・名前の網）。人の形は「顔の無い影」だけ（c302・c313）。事故の瞬間・亡くなる場面は描かない。
  🔴 **色は「どの船か・誰の話か」**（役の色＝ROLE と J の名で引く・新しい色の値は足していない・船の色は ⑤b-3 の地図 c306 と同じ）：
     タイタニック号＝水色 ship／カリフォルニアン号＝緑 ntsb／カルパチア号＝青 uscg／ケープ・レース（陸の無線局）＝紫 tsb／
     アメリカ号＝橙 company／アンティリアン号＝紫 city／オリンピック号（姉妹船）＝桃 bldg_a／
     報告書（1912年の英国の報告）＝白 SUB／1992年の調べ直し＝茶 DOC／証言の人＝船長 桃 bldg_a・航海士と見習い 紫 city。
     同じ色の鍵は同じ画面に出さない（門番 check_mech の judge_m26 が VIEW_SRC で見る）。
     灯の色（舷灯の緑と赤・信号弾の白）は物の色＝LIGHT（門番が c607 の左右を見る）。意味の色＝赤 ALERT（届かない・取り違え）・黄 AMBER（数・時刻）。
  🔴 画面の時刻は `ref/ep26/sources.md` §6 の時計の表の値と G1 の時刻だけ＝**どの船の時計かを同じ画面に書く**（「…の時計」）。
     割れる時刻（1:10／1:15・2:00／2:05）は誰の話かを書く（「…の話」「…の記憶」）。船が違う時刻を1本の時間の線に並べない（c416＝タイタニック号・c637＝カリフォルニアン号）。
  🔴 案B の守りの線：見えた船をタイタニック号と名乗らない・心の中は描かない・1992年の調べ直しは言い切らない（c626 は「論点」まで）。

■ 見え方（view）＝映像方針の一覧 `ref/ep26/eizou_list26.md` の「見た目の型」（第1〜5章の図解 37カット・案C 18 と地図は別）
  第1章  tons2（c202 総トン数の2本の棒）・people4（c206 乗っていた人の縦の棒）・boats20（c209 上から見たボート20隻）・
         track3（c210 1本の帯の3つの印）・table1894（c211 1894年の表の段）
  第2章  radio3（c302 海の上の船と電波）・clocks2（c303 2隻の正午）・aside（c311 脇に置いた知らせ）・busy（c313 乗客の電報）・
         cf_side（c317 カリフォルニアン号の横の姿）・relay3（c319 3隻と電波）・drown（c322 強い電波と弱い電波）
  第3章  watch（c403 船橋と見張り台）・helm（c406 号令と船首）・olympic（c408 37秒の見積もり）・damage（c411 傷の範囲と区画）・
         tray（c413 壁で仕切った区画）・ttband（c416 タイタニック号の時計の横の帯）
  第4章  cqd（c501 モールスの CQD）・carp（c505 カルパチア号の向かい方）・rockets_n（c510 信号弾の数の2つの札）・colors（c516 信号の色）
  第5章  field（c602 氷原の手前で止まる）・drift（c604 推測の位置と流れ）・sidelights（c607 舷灯の色）・masts2（c609 マストの灯）・
         morse（c611 モールス灯）・views2（c612 2人の見立て）・watches（c613 3つの当直と鐘）・bearing（c617 方位）・flicker（c619 瞬き）・
         section（c620 前の断面と伝声管）・company（c623 会社の夜の合図）・height（c626 信号弾の高さ）・memory2（c634 2人の記憶）・
         cfband（c637 カリフォルニアン号の時計の縦の帯）・swap（c639 取り違え）
  🔴 同じ型は近くで続けない：棒 c202（横の棒と物差し）↔c206（縦の棒）↔c210（1本の帯）・時刻の帯 c416（横・青）↔c637（縦・橙）・
     灯 c607（上から見た舷灯）↔c609（2隻のマストの灯）↔c611（灯の点と線）↔c619（2本の光の帯）・2つの札 c510↔c612↔c634（形を替える）。
     案C の絵（K1〜K6）とも別の絵（c620 の断面は船橋と海図室の「つながり」だけ＝人の影は描かない）。

■ SPEC の書き方（mech25 と同じ）
  fig=("m26", dict(view=…, start=dict(…), steps=[dict(state=dict(…)), …], rel=[dict(t="46,328トン", src="G1 p11")], note="…", src=ss.src([…])))
  🔴 画面の字の数（時刻・数・年）は全部 `rel=` に同じ文字列で宣言する（門番 judge_m26 が基図と段の層の全部の字から数を拾って照らす）。
  🔴 記録の値（色・数・時刻・比例・モールスの符号・舷灯の左右）は門番の側 REC_M26 が別に持つ（§5b-88）。描く側の表を書き換えると鳴る。
"""
from __future__ import annotations

import math
import re

import jiko_style as J
import titan_fig as F
from mech21 import _P, _arrow, _check, _on, _qmark, _xmark
from mech24 import _arcpts, _tline, _w, rc
from mech25 import _bell, _chip, _waves

ONOFF = ("off", "on")
INK = J.INK_W
CX = 960.0

# どの船か・誰の話か（名・ROLE か J の名）。同じ色の鍵は同じ画面に出さない（門番が VIEW_SRC で見る）
#   🔴 船の色は ⑤b-3 の地図 c306（タイタニック号の航路＝水色 ship・カリフォルニアン号＝緑 ntsb・アメリカ号＝橙 company）と同じ＝動画の中で同じ船は同じ色
SRC = dict(
    tt=("タイタニック号", "ship"),
    cf=("カリフォルニアン号", "ntsb"),
    cp=("カルパチア号", "uscg"),
    cr=("ケープ・レース", "tsb"),           # 陸の無線局（ニューファンドランド）
    an=("アンティリアン号", "city"),
    am=("アメリカ号", "company"),
    ol=("オリンピック号", "bldg_a"),        # 姉妹船（試験の見積もり）
    rep=("報告書", "SUB"),                  # 1912年の英国の審問の報告（G1）
    maib=("1992年の調べ直し", "DOC"),       # 英国 海難調査局の再評価（G2）
    cap=("船長", "bldg_a"),                 # 証言の人（船長）
    mate=("航海士", "city"),                # 証言の人（航海士・見習い）
)
# 灯の色（物の色）
LIGHT = dict(green=J.OK, red=J.ALERT, white=J.SUB)


def sc(key):
    return rc(SRC[key][1])


def _clk(x, y, t, ship, cap=30, anchor="middle", mw=620):
    """時刻とどの船の時計か（1つの札）。"""
    return _tline(x, y, f"{t}（{SRC[ship][0]}の時計）", cap, sc(ship), anchor, mw)


def _cpts(cx, cy, r, n=14):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _rot(pts, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def _hull_side(x0, x1, yw, h, bow_right=True):
    """横から見た船体（船首＝右）。"""
    L = x1 - x0
    if bow_right:
        return [(x0, yw - h), (x1, yw - h - 8), (x1 - L * 0.07, yw), (x0 + L * 0.03, yw)]
    return [(x0, yw - h - 8), (x1, yw - h), (x1 - L * 0.03, yw), (x0 + L * 0.07, yw)]


def _ship_side(x0, x1, yw, col, h=None, funnels=1, masts=True, fill=None, dash=None, sw=4, op=None):
    """横から見た汽船の影（船首＝右）。上の構造・煙突・2本のマスト。"""
    L = x1 - x0
    h = h or max(26.0, L * 0.09)
    fill = fill or J.BG2
    g = [F.poly(_hull_side(x0, x1, yw, h), fill, col, sw, close=True, dash=dash, op=op)]
    sx0, sx1, sh = x0 + L * 0.30, x0 + L * 0.70, h * 0.55
    g.append(F.rect(sx0, yw - h - sh, sx1 - sx0, sh, fill, col, max(2, sw - 1), op=op, dash=dash))
    for i in range(funnels):
        fx = x0 + L * (0.42 + 0.12 * i) if funnels > 1 else x0 + L * 0.52
        g.append(F.rect(fx, yw - h - sh - h * 0.9, L * 0.035, h * 0.9, fill, col, max(2, sw - 1), op=op, dash=dash))
    if masts:
        for mx in (x0 + L * 0.14, x0 + L * 0.88):
            g.append(F.line(mx, yw - h, mx, yw - h - h * 2.6, col, 3, dash=dash, op=op))
    return "".join(g)


def _mast_tops(x0, x1, yw, h=None):
    L = x1 - x0
    h = h or max(26.0, L * 0.09)
    return [(x0 + L * 0.14, yw - h - h * 2.6), (x0 + L * 0.88, yw - h - h * 2.6)]


def _top_pts(cx, cy, L, W):
    """上から見た船（船首＝上）の頂点。"""
    return [(cx, cy - L / 2), (cx + W / 2, cy - L / 2 + W * 1.1), (cx + W / 2, cy + L / 2 - 6), (cx + W / 2 - 6, cy + L / 2),
            (cx - W / 2 + 6, cy + L / 2), (cx - W / 2, cy + L / 2 - 6), (cx - W / 2, cy - L / 2 + W * 1.1)]


def _ship_top(cx, cy, L, W, deg, col, fill=None, sw=4, dash=None, op=None):
    return F.poly(_rot(_top_pts(cx, cy, L, W), cx, cy, deg), fill or J.BG2, col, sw, close=True, dash=dash, op=op)


def _tower(cx, yb, hgt, col):
    """陸の無線局（小屋と鉄塔）。"""
    top = yb - hgt
    return (F.rect(cx - 44, yb - 46, 88, 46, J.BG2, col, 4, rx=4)
            + F.poly([(cx - 30, yb - 46), (cx, top), (cx + 30, yb - 46)], "none", col, 4)
            + F.line(cx - 18, yb - 100, cx + 18, yb - 100, col, 3) + F.line(cx - 10, yb - 160, cx + 10, yb - 160, col, 3)
            + F.circ(cx, top, 7, col))


def _lamp(cx, cy, col, r=10.0, glow=2.6):
    return F.circ(cx, cy, r * glow, col, None, op=0.22) + F.circ(cx, cy, r, col)


def _burst(cx, cy, col, r=26.0, sw=4):
    """信号弾の星（真ん中の点と放射の線）。"""
    g = [F.circ(cx, cy, r * 0.32, col)]
    for i in range(8):
        a = 2 * math.pi * i / 8
        g.append(F.line(cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a), col, sw))
    return "".join(g)


def _ice(cx, cy, s=1.0):
    p = [(cx - 30 * s, cy + 14 * s), (cx - 18 * s, cy - 10 * s), (cx - 4 * s, cy - 20 * s), (cx + 12 * s, cy - 8 * s), (cx + 28 * s, cy + 14 * s)]
    return F.poly(p, J.SUB, J.TICK, 2, close=True, op=0.85)


def _north(cx, cy, s=1.0):
    return (F.poly([(cx, cy - 46 * s), (cx + 14 * s, cy), (cx - 14 * s, cy)], J.TICK, None, close=True)
            + _tline(cx, cy + 34 * s, "北", 26, J.TICK, "middle", 80))


def _slip(cx, cy, col, w=74.0, h=50.0, sw=4):
    g = [F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, sw, rx=4)]
    for i in range(3):
        y = cy - h / 2 + 13 + i * 12
        g.append(F.line(cx - w / 2 + 10, y, cx + w / 2 - 10 - (16 if i == 2 else 0), y, col, 3))
    return "".join(g)


def _figure(cx, yb, s, col):
    """顔の無い影（座る・頭と肩）。"""
    return (F.circ(cx, yb - 118 * s, 22 * s, col)
            + F.poly([(cx - 40 * s, yb), (cx - 34 * s, yb - 70 * s), (cx - 14 * s, yb - 92 * s), (cx + 14 * s, yb - 92 * s),
                      (cx + 34 * s, yb - 70 * s), (cx + 40 * s, yb)], col, None, close=True))


def _lying(cx, cy, s, col):
    """横になった顔の無い影（頭と体）。"""
    return F.circ(cx - 70 * s, cy, 18 * s, col) + F.rect(cx - 48 * s, cy - 15 * s, 120 * s, 30 * s, col, None, None, rx=14 * s)


def _eye(cx, cy, col, s=1.0):
    top = _arcpts(cx, cy + 22 * s, 46 * s, 34 * s, 200, 340, 10)
    bot = _arcpts(cx, cy - 22 * s, 46 * s, 34 * s, 20, 160, 10)
    return F.poly(top + bot, J.BG2, col, 4, close=True) + F.circ(cx, cy, 11 * s, col)


def _clock(cx, cy, r, col, ticks=True):
    g = [F.circ(cx, cy, r, J.BG2, col, 5)]
    if ticks:
        for i in range(12):
            a = 2 * math.pi * i / 12
            g.append(F.line(cx + r * 0.80 * math.cos(a), cy + r * 0.80 * math.sin(a), cx + r * 0.94 * math.cos(a), cy + r * 0.94 * math.sin(a), col, 4))
    return "".join(g)


def _hand_pts(cx, cy, ln, w=7.0):
    """時計の針（12時を指す向き）の頂点。"""
    return [(cx - w / 2, cy + 10), (cx + w / 2, cy + 10), (cx + w / 2, cy - ln + 8), (cx, cy - ln), (cx - w / 2, cy - ln + 8)]


def _say(cx, cy, who, t, cap=30, w=None):
    """誰の話か（色）と言葉の札（上の小さな名・下の言葉）。"""
    c = sc(who) if who in SRC else rc(who)
    ww = w or max(_w(t, cap), _w(SRC.get(who, (who,))[0], 24)) + 60
    return (F.rect(cx - ww / 2, cy - 44, ww, 88, J.BG2, c, 4, rx=14)
            + _tline(cx, cy - 14, SRC[who][0] if who in SRC else who, 24, c, "middle", ww - 24)
            + _tline(cx, cy + 28, t, cap, INK, "middle", ww - 24))


def _neq(cx, cy, col=None, s=1.0):
    c = col or J.ALERT
    return (F.line(cx - 34 * s, cy - 12 * s, cx + 34 * s, cy - 12 * s, c, 8) + F.line(cx - 34 * s, cy + 12 * s, cx + 34 * s, cy + 12 * s, c, 8)
            + F.line(cx + 18 * s, cy - 34 * s, cx - 18 * s, cy + 34 * s, c, 8))


# ══════════════════════════════════════════════════════════
#  第1章
#  tons2（c202）＝横の2本の棒（長さは総トン数に比例＝G1 p.11 の 46,328・p.56 の 6,223）。
#  2行目でカリフォルニアン号の棒の長さの目盛りをタイタニック号の棒に刻む（7つ）＝「約7倍」
# ══════════════════════════════════════════════════════════
TN = dict(x0=470.0, k=1240.0 / 46328.0, ya=430.0, yb=650.0, h=88.0)
TN_V = (("tt", 46328, "46,328トン"), ("cf", 6223, "6,223トン"))
TN_TIMES = "約7倍"


def tn_end(v):
    return TN["x0"] + v * TN["k"]


def tons2_base(st0):
    x0 = TN["x0"]
    g = [F.line(x0, TN["ya"] - 80, x0, TN["yb"] + 70, J.LINE, 5)]
    for (key, _v, _l), y in zip(TN_V, (TN["ya"], TN["yb"])):
        g.append(_tline(x0 - 26, y + 11, SRC[key][0], 30, sc(key), "end", 330))
    return g


def tons2_stage(prev, st):
    s = []
    x0, h = TN["x0"], TN["h"]
    if _on(prev, st, "tt"):
        _k, v, lab = TN_V[0]
        s.append(F.rect(x0, TN["ya"] - h / 2, tn_end(v) - x0, h, sc("tt"), None, None, rx=6))
        s.append(_tline(tn_end(v), TN["ya"] - h / 2 - 20, lab, 36, INK, "end", 420))
    if _on(prev, st, "cf"):
        _k, v, lab = TN_V[1]
        s.append(F.rect(x0, TN["yb"] - h / 2, tn_end(v) - x0, h, sc("cf"), None, None, rx=6))
        s.append(_tline(tn_end(v) + 22, TN["yb"] + 12, lab, 36, INK, "start", 420))
        n = int(TN_V[0][1] // v)
        for i in range(1, n + 1):
            x = x0 + i * v * TN["k"]
            s.append(F.line(x, TN["ya"] - h / 2 + 6, x, TN["ya"] + h / 2 - 6, J.BG, 5))
            s.append(F.line(x, TN["ya"] + h / 2 + 8, x, TN["ya"] + h / 2 + 30, sc("cf"), 4))
        s.append(_chip(CX + 160, (TN["ya"] + TN["yb"]) / 2 + 4, TN_TIMES, J.AMBER, 36))
    return s


# ══════════════════════════════════════════════════════════
#  people4（c206）＝縦の棒（高さは人数に比例＝G1 p.32）：一等 325・二等 285・三等 706（乗客 1,316）・乗員 885・あわせて 2,201・子ども 109
# ══════════════════════════════════════════════════════════
PP = dict(y0=800.0, k=0.48, w=136.0, xs=(470.0, 650.0, 830.0, 1090.0, 1330.0))
PP_ROWS = (("一等", 325, "bldg_a"), ("二等", 285, "city"), ("三等", 706, "company"), ("乗員", 885, "SUB"))
PP_KIDS = (109, (6, 24, 79))
PP_PASS, PP_ALL = 1316, 2201


def pp_top(v):
    return PP["y0"] - v * PP["k"]


def people4_base(st0):
    g = [F.line(380.0, PP["y0"], 1430.0, PP["y0"], J.LINE, 5)]
    for i, (n, _v, _c) in enumerate(PP_ROWS):
        g.append(_tline(PP["xs"][i], PP["y0"] + 42, n, 30, INK, "middle", 200))
    g.append(_tline(PP["xs"][4], PP["y0"] + 42, "子ども", 30, J.AMBER, "middle", 200))
    return g


def people4_stage(prev, st):
    s = []
    w = PP["w"]
    if _on(prev, st, "q"):
        s.append(_qmark(1660.0, 400.0, 72))
    if _on(prev, st, "bars"):
        for i, (_n, v, c) in enumerate(PP_ROWS):
            x, top = PP["xs"][i], pp_top(v)
            s.append(F.rect(x - w / 2, top, w, PP["y0"] - top, rc(c), None, None, rx=6))
            s.append(_tline(x, top - 16, f"{v:,}人", 30, INK, "middle", 200))
        xa, xb = PP["xs"][0] - w / 2, PP["xs"][2] + w / 2
        yb = pp_top(PP_ROWS[2][1]) - 70
        s.append(F.poly([(xa, yb + 18), (xa, yb), (xb, yb), (xb, yb + 18)], "none", J.LINE, 4))
        s.append(_tline((xa + xb) / 2, yb - 16, f"乗客 {PP_PASS:,}人", 32, INK, "middle", 400))
        s.append(_chip(1640.0, 600.0, f"あわせて {PP_ALL:,}人", J.AMBER, 34))
    if _on(prev, st, "kids"):
        x, top = PP["xs"][4], pp_top(PP_KIDS[0])
        s.append(F.rect(x - w / 2, top, w, PP["y0"] - top, J.AMBER, None, None, rx=6))
        s.append(_tline(x, top - 16, f"{PP_KIDS[0]}人", 30, J.AMBER, "middle", 200))
    return s


# ══════════════════════════════════════════════════════════
#  boats20（c209）＝上から見たボート20隻（長さは定員に比例・並びは模式＝G1 p.25）
#  語りの呼び方（台本 §0-5）：大きなボート（65人乗り）14隻・小さめのボート（40人乗り）2隻・折りたたみ式のボート（47人乗り）4隻
# ══════════════════════════════════════════════════════════
BT = dict(k=2.2, h=46.0, gap=18.0, x0=230.0)
BT_ROWS = (("大きなボート", 65, 14, "LINE"), ("小さめのボート", 40, 2, "AMBER"), ("折りたたみ式のボート", 47, 4, "bldg_a"))
BT_SEATS = 1178
BT_Y = ((380.0, 446.0), (568.0,), (692.0,))


def bt_len(cap):
    return cap * BT["k"]


def _boat(x, y, cap, col, fold=False):
    L, h = bt_len(cap), BT["h"]
    return F.rect(x, y - h / 2, L, h, J.BG2 if fold else col, col if fold else J.BG, 4 if fold else 2, rx=h / 2, dash="12 8" if fold else None)


def boats20_base(st0):
    return [F.rect(190.0, 318.0, 1610.0, 450.0, "none", J.LINE_DIM, 3, rx=40, dash="10 10")]


def _bt_row(i):
    name, cap, n, c = BT_ROWS[i]
    col = rc(c)
    g = []
    ys = BT_Y[i]
    per = 7 if i == 0 else n
    for j in range(n):
        y = ys[j // per] if i == 0 else ys[0]
        x = BT["x0"] + (j % per) * (bt_len(cap) + BT["gap"])
        g.append(_boat(x, y, cap, col, fold=(i == 2)))
    xr = BT["x0"] + per * (bt_len(cap) + BT["gap"]) + 30
    yl = sum(ys) / len(ys)
    g.append(_tline(xr, yl - 6, name, 32, col, "start", 520))
    g.append(_tline(xr, yl + 36, f"{cap}人乗り・{n}隻", 30, INK, "start", 420))
    return "".join(g)


def boats20_stage(prev, st):
    s = []
    if _on(prev, st, "big"):
        s += [_bt_row(0), _bt_row(1)]
    if _on(prev, st, "fold"):
        s.append(_bt_row(2))
    return s


# ══════════════════════════════════════════════════════════
#  track3（c210）＝1本の帯（長さは人数に比例）：乗っていた人 2,201・ボートの席 1,178・英国の規則が求めた量 962（G1 p.62）
# ══════════════════════════════════════════════════════════
TK = dict(x0=230.0, x1=1690.0, y=560.0, h=78.0)
TK_V = (2201, 1178, 962)


def tk_x(v):
    return TK["x0"] + v * (TK["x1"] - TK["x0"]) / TK_V[0]


def track3_base(st0):
    y, h = TK["y"], TK["h"]
    xs = tk_x(TK_V[1])
    return [F.rect(TK["x0"], y - h / 2, TK["x1"] - TK["x0"], h, J.BG2, J.LINE, 4, rx=8),
            F.rect(TK["x0"], y - h / 2, xs - TK["x0"], h, sc("tt"), None, None, rx=8),
            _tline(TK["x0"] + 22, y + 12, f"ボートの席 {TK_V[1]:,}人ぶん", 32, INK, "start", 600),
            _tline(TK["x1"], y - h / 2 - 22, f"乗っていた人 {TK_V[0]:,}人", 32, INK, "end", 600)]


def track3_stage(prev, st):
    s = []
    y, h = TK["y"], TK["h"]
    xr, xs = tk_x(TK_V[2]), tk_x(TK_V[1])
    if _on(prev, st, "rule"):
        s.append(F.line(xr, y - h / 2 - 64, xr, y + h / 2 + 20, J.AMBER, 6))
        s.append(_tline(xr, y - h / 2 - 80, "英国の規則が求めた量", 30, J.AMBER, "middle", 420))
        yb = y + h / 2 + 32
        s.append(F.poly([(xr, yb - 14), (xr, yb), (xs, yb), (xs, yb - 14)], "none", INK, 4))
        s.append(_tline((xr + xs) / 2 + 16, yb + 42, "規則より多い", 28, INK, "start", 300))
    if _on(prev, st, "num"):
        s.append(_tline(xr - 18, y + h / 2 + 50, f"{TK_V[2]}人ぶん", 38, J.AMBER, "end", 300))
    return s


# ══════════════════════════════════════════════════════════
#  table1894（c211）＝1894年の表の段（段の数と高さは模式・横は総トン数に比例＝G1 p.63〜64）。
#  表は「1万トン以上」で終わる＝4万6,328トンの船も1万トンの船と同じ量（段の外へ伸びる平らな線と印）
# ══════════════════════════════════════════════════════════
TB = dict(x0=260.0, k=1300.0 / 50000.0, yb=760.0, top=520.0)
TB_V = (1894, 10000, 46328)
TB_STEPS = ((0.0, 700.0), (0.25, 650.0), (0.5, 600.0), (0.75, 556.0))   # (1万トンまでの割合, 段の高さ)＝模式


def tb_x(v):
    return TB["x0"] + v * TB["k"]


def table1894_base(st0):
    return [F.line(TB["x0"], TB["yb"], 1760.0, TB["yb"], J.LINE, 5), F.line(TB["x0"], TB["yb"], TB["x0"], 470.0, J.LINE, 5),
            _tline(1760.0, TB["yb"] + 44, "総トン数", 28, J.TICK, "end", 300),
            _tline(TB["x0"] + 16, 488.0, "求められたボートの量", 26, J.TICK, "start", 420)]


def table1894_stage(prev, st):
    s = []
    x10 = tb_x(TB_V[1])
    if _on(prev, st, "q"):
        s.append(_qmark(1660.0, 420.0, 72))
    if _on(prev, st, "t94"):
        pts = [(TB["x0"], TB["yb"])]
        for i, (f, y) in enumerate(TB_STEPS):
            xa = TB["x0"] + f * (x10 - TB["x0"])
            pts += [(xa, y), (TB["x0"] + (TB_STEPS[i + 1][0] if i + 1 < len(TB_STEPS) else 1.0) * (x10 - TB["x0"]), y)]
        pts += [(x10, TB["top"]), (x10 + 40, TB["top"])]
        s.append(F.poly(pts + [(x10 + 40, TB["yb"])], rc("DOC"), None, close=True, op=0.32))
        s.append(F.poly(pts, "none", rc("DOC"), 6))
        s.append(F.line(x10, TB["yb"] - 10, x10, TB["yb"] + 10, J.LINE, 5))
        s.append(_tline(x10, TB["yb"] + 44, "1万トン", 28, INK, "middle", 200))
        s.append(_chip(560.0, 390.0, f"{TB_V[0]}年の表（見直されないまま）", rc("DOC"), 30))
    if _on(prev, st, "flat"):
        xt = tb_x(TB_V[2])
        s.append(F.line(x10 + 40, TB["top"], 1720.0, TB["top"], rc("DOC"), 6, dash="18 12"))
        s.append(_tline((x10 + xt) / 2, TB["top"] - 22, "1万トン以上は同じ量", 30, INK, "middle", 520))
        s.append(F.line(xt, TB["yb"], xt, TB["top"] + 24, sc("tt"), 6))
        s.append(F.circ(xt, TB["top"], 16, sc("tt")))
        s.append(_tline(xt, TB["yb"] + 44, f"{TB_V[2]:,}トン", 30, sc("tt"), "middle", 260))
        s.append(_tline(xt + 18, TB["yb"] - 40, "タイタニック号", 28, sc("tt"), "start", 300))
    return s


# ══════════════════════════════════════════════════════════
#  第2章
#  radio3（c302）＝横から見た海：陸の無線局の電波・無線の無い船・無線のある船の無線室で眠る影（G2 p.1）
# ══════════════════════════════════════════════════════════
RD = dict(yw=640.0, land=(110.0, 330.0), tw=230.0, a=(640.0, 940.0), b=(1180.0, 1560.0), call=(1700.0, 380.0, 86.0))


def radio3_base(st0):
    yw = RD["yw"]
    g = [F.line(RD["land"][1], yw, 1800.0, yw, J.LINE_DIM, 3),
         F.poly([(RD["land"][0], yw - 20), (RD["land"][1] - 30, yw - 26), (RD["land"][1], yw + 30), (RD["land"][0], yw + 30)], J.BG2, J.LINE, 3, close=True),
         _tower(RD["tw"], yw - 22, 230.0, sc("cr")), _tline(RD["tw"], yw + 70, "陸の無線局", 28, sc("cr"), "middle", 260)]
    for r, a in ((150.0, 34.0), (380.0, 15.0), (640.0, 9.0), (930.0, 6.0)):
        g.append(F.poly(_arcpts(RD["tw"], yw - 252, r, r, -a, a, 8), "none", sc("cr"), 4))
    a0, a1 = RD["a"]
    g.append(_ship_side(a0, a1, yw, J.LINE, masts=False))
    b0, b1 = RD["b"]
    g.append(_ship_side(b0, b1, yw, J.LINE))
    return g


def radio3_stage(prev, st):
    s = []
    if _on(prev, st, "none"):
        a0, a1 = RD["a"]
        s.append(_chip((a0 + a1) / 2, 470.0, "無線なし", J.TICK, 28))
    if _on(prev, st, "deaf"):
        b0, b1 = RD["b"]
        (m0x, m0y), (m1x, m1y) = _mast_tops(b0, b1, RD["yw"])
        s.append(F.line(m0x, m0y + 6, m1x, m1y + 6, J.LINE, 3))
        cx, cy, r = RD["call"]
        rx = b0 + (b1 - b0) * 0.62
        s.append(F.line(rx, RD["yw"] - 60, cx - r * 0.7, cy + r * 0.7, J.LINE_DIM, 3))
        s.append(F.circ(cx, cy, r, J.BG, J.LINE, 4))
        s.append(F.rect(cx - 62, cy + 18, 124, 14, J.LINE_DIM, None, None, rx=4) + _lying(cx + 6, cy + 2, 0.52, J.LINE))
        s.append(_xmark(cx + 52, cy - 46, 18, J.ALERT, 7))
        s.append(_tline(cx, cy + r + 40, "誰も聞いていない", 28, J.ALERT, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  clocks2（c303）＝西の船と東の船の時計（針の数字なし）。2行目で、それぞれの船の真上（真南）に太陽が来たとき針が12へ回る（G2 p.6）
# ══════════════════════════════════════════════════════════
CK = dict(yw=780.0, xs=(560.0, 1360.0), cy=610.0, r=78.0, arc=(300.0, 1620.0, 360.0))
CK_START = (-130.0, 70.0)          # 頭の針の角度（度・12時からの時計回り）＝1行目のあいだは船ごとにばらばら


def ck_sun(x):
    x0, x1, ytop = CK["arc"]
    t = (x - x0) / (x1 - x0)
    return ytop + (1 - math.sin(math.pi * t)) * 260.0


def clocks2_parts(st):
    g = []
    for i, x in enumerate(CK["xs"]):
        rot = 0.0 if st.get("noon") == "on" else CK_START[i]
        g.append(_P(f"hand{i}", "poly", _hand_pts(x, CK["cy"], CK["r"] * 0.80), fill=INK, stroke=None, w=2, pivot=[x, CK["cy"]], rot=rot,
                    alpha=1.0 if st.get("clk") == "on" else 0.0))
    return g


def clocks2_base(st0):
    yw = CK["yw"]
    x0, x1, _y = CK["arc"]
    g = [F.line(200.0, yw, 1720.0, yw, J.LINE_DIM, 3),
         F.poly([(x0 + (x1 - x0) * i / 40, ck_sun(x0 + (x1 - x0) * i / 40)) for i in range(41)], "none", J.LINE_DIM, 3, dash="10 10")]
    for x, lab in zip(CK["xs"], ("西の船", "東の船")):
        g.append(_ship_side(x - 150, x + 150, yw, J.LINE, h=28.0))
        g.append(_tline(x, yw + 46, lab, 30, INK, "middle", 220))
    g.append(_arrow(1640.0, 860.0 - 40, 1780.0, 860.0 - 40, J.TICK, 4, 16) + _tline(1620.0, 830.0, "東", 26, J.TICK, "end", 60))
    return g


def clocks2_stage(prev, st):
    s = []
    if _on(prev, st, "clk"):
        for x in CK["xs"]:
            s.append(_clock(x, CK["cy"], CK["r"], J.LINE))
    if _on(prev, st, "noon"):
        for x in CK["xs"]:
            y = ck_sun(x)
            s.append(F.line(x, y + 40, x, CK["cy"] - CK["r"] - 14, J.AMBER, 4, dash="8 8"))
            s.append(F.circ(x, y, 30, J.AMBER))
            s.append(_tline(x + 46, y + 10, "真南", 28, J.AMBER, "start", 120))
            s.append(_tline(x + CK["r"] + 20, CK["cy"] + 10, "正午", 28, J.AMBER, "start", 120))
    return s


# ══════════════════════════════════════════════════════════
#  aside（c311）＝横から見たタイタニック号：アメリカ号の知らせ → 無線室で脇に置く（ケープ・レースと話せる所まで待つ）→ 航海士へ渡らない（G1 p.36）
# ══════════════════════════════════════════════════════════
AS = dict(hull=(560.0, 1760.0, 780.0, 70.0), radio=(960.0, 600.0, 240.0, 110.0), bridge=(1480.0, 540.0, 200.0, 100.0),
          am=(150.0, 420.0, 780.0), cr=(220.0, 470.0))


def _room(cx, cy, w, h, t, col):
    return F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 4, rx=8) + _tline(cx, cy + 10, t, 28, col, "middle", w - 20)


def aside_base(st0):
    x0, x1, yw, h = AS["hull"]
    a0, a1, ya = AS["am"]
    g = [F.poly(_hull_side(x0, x1, yw, h), J.BG2, sc("tt"), 4, close=True),
         _room(*AS["radio"], "無線室", sc("tt")), _room(*AS["bridge"], "船橋", sc("tt")),
         _ship_side(a0, a1, ya, sc("am"), h=26.0), _tline((a0 + a1) / 2, ya + 44, "アメリカ号", 28, sc("am"), "middle", 260),
         _tower(AS["cr"][0], AS["cr"][1], 150.0, sc("cr")), _tline(AS["cr"][0] + 60, AS["cr"][1] - 70, "ケープ・レース（陸の無線局）", 28, sc("cr"), "start", 480)]
    return g


def aside_stage(prev, st):
    s = []
    rx, ry, rw, rh = AS["radio"]
    bx, by, bw, bh = AS["bridge"]
    if _on(prev, st, "aside"):
        a0, a1, ya = AS["am"]
        s.append(_arrow(a1 - 20, ya - 70, rx - rw / 2 - 10, ry + 10, sc("am"), 5, 22))
        s.append(_slip(rx - 20, 748.0, J.AMBER, 60.0, 40.0, 3) + _tline(rx + 26, 758.0, "脇に置く", 28, J.AMBER, "start", 200))
        s.append(F.poly([(rx - rw / 2 + 20, ry - rh / 2), (AS["cr"][0] + 60, AS["cr"][1] - 40)], "none", sc("cr"), 4, dash="8 10"))
        s.append(_tline(AS["cr"][0] + 360, AS["cr"][1] + 4, "話せる所まで待つ", 28, sc("cr"), "start", 300))
    if _on(prev, st, "nope"):
        x0, y0, x1, y1 = rx + rw / 2 + 10, ry - 10, bx - bw / 2 - 10, by + 10
        s.append(F.line(x0, y0, x1, y1, J.ALERT, 5, dash="12 10"))
        s.append(_xmark((x0 + x1) / 2, (y0 + y1) / 2, 22, J.ALERT, 8))
        s.append(_tline((x0 + x1) / 2, by - bh / 2 - 66, "航海士へ渡らない", 30, J.ALERT, "middle", 340))
        s.append(_chip(bx, by - bh / 2 - 130, "報告書の見方", sc("rep"), 26))
    return s


# ══════════════════════════════════════════════════════════
#  busy（c313）＝横から見た無線室：乗客の電報（20:00から＝G1 p.37「from 8 o'clock onward」）→ ケープ・レースへ・氷の知らせは届かない
# ══════════════════════════════════════════════════════════
BS = dict(room=(460.0, 360.0, 1320.0, 800.0), desk=(560.0, 1200.0, 680.0), fig=(760.0, 680.0), cr=(250.0, 600.0), bridge=(1640.0, 420.0, 230.0, 96.0))
BS_T = "20:00"


def busy_base(st0):
    x0, y0, x1, y1 = BS["room"]
    d0, d1, dy = BS["desk"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, sc("tt"), 4, rx=10), _tline(x1 - 20, y0 + 40, "無線室（タイタニック号）", 26, sc("tt"), "end", 400),
            F.rect(d0, dy, d1 - d0, 18, J.LINE_DIM, None, None, rx=4), F.line(d0 + 40, dy + 18, d0 + 40, y1, J.LINE_DIM, 6),
            F.line(d1 - 40, dy + 18, d1 - 40, y1, J.LINE_DIM, 6), _figure(BS["fig"][0], BS["fig"][1] + 4, 0.9, J.LINE),
            _tower(BS["cr"][0], BS["cr"][1], 190.0, sc("cr")), _tline(BS["cr"][0], BS["cr"][1] + 40, "ケープ・レース", 28, sc("cr"), "middle", 260),
            _room(*BS["bridge"], "船長・航海士", sc("tt"))]


def busy_stage(prev, st):
    s = []
    bx, by, bw, bh = BS["bridge"]
    if _on(prev, st, "ice"):
        s.append(_slip(1080.0, 650.0, J.ALERT))
        s.append(_tline(1080.0, 612.0, "氷の知らせ", 26, J.ALERT, "middle", 200))
        s.append(F.line(1130.0, 630.0, bx - bw / 2 - 10, by + 30, J.ALERT, 5, dash="12 10"))
        s.append(_xmark((1130.0 + bx - bw / 2) / 2 + 30, (630.0 + by + 30) / 2, 22, J.ALERT, 8))
        s.append(_chip(1640.0, 560.0, "届いていない（報告書）", sc("rep"), 26))
    if _on(prev, st, "busy"):
        for i, (x, y) in enumerate(((620.0, 640.0), (520.0, 580.0), (420.0, 540.0), (330.0, 520.0))):
            s.append(_slip(x, y - i * 6, INK, 60.0, 40.0, 3))
        s.append(_arrow(600.0, 600.0, 320.0, 470.0, sc("cr"), 5, 22))
        s.append(_tline(900.0, 430.0, "乗客の電報", 30, INK, "middle", 300))
        s.append(_clk(900.0, 480.0, f"{BS_T}から", "tt", 26, mw=520))
    return s


# ══════════════════════════════════════════════════════════
#  cf_side（c317）＝横から見たカリフォルニアン号（形は模式＝記録に長さが無い）・レイランド社・ロンドンからボストンへ・乗客 0人（G1 p.56）
# ══════════════════════════════════════════════════════════
CS = dict(x0=380.0, x1=1520.0, yw=640.0, h=84.0)
CS_V = ("レイランド社", "ロンドン", "ボストン", 0)


def cf_side_base(st0):
    return [F.line(200.0, CS["yw"], 1760.0, CS["yw"], J.LINE_DIM, 3), _ship_side(CS["x0"], CS["x1"], CS["yw"], sc("cf"), h=CS["h"])]


def cf_side_stage(prev, st):
    s = []
    if _on(prev, st, "co"):
        s.append(_chip(1060.0, 330.0, f"{CS_V[0]}の船", sc("cf"), 32))
        y = 750.0
        s.append(_arrow(560.0, y, 1340.0, y, J.LINE, 6, 26))
        s.append(_tline(540.0, y + 11, CS_V[1], 32, INK, "end", 260) + _tline(1370.0, y + 11, f"{CS_V[2]}（アメリカ）", 32, INK, "start", 400))
    if _on(prev, st, "empty"):
        x0, x1, yw, h = CS["x0"], CS["x1"], CS["yw"], CS["h"]
        for i in range(12):
            x = x0 + 120 + i * (x1 - x0 - 280) / 11
            s.append(F.circ(x, yw - h * 0.62, 11, J.BG, J.TICK, 3))
        s.append(_chip(1700.0, 520.0, f"乗客 {CS_V[3]}人", J.AMBER, 32))
    return s


# ══════════════════════════════════════════════════════════
#  relay3（c319）＝上から見た3隻：カリフォルニアン号 → アンティリアン号への電波・タイタニック号も横で聞く → 「受け取った」と返す（G1 p.56）
# ══════════════════════════════════════════════════════════
RL = dict(an=(330.0, 540.0), cf=(920.0, 470.0), tt=(1520.0, 650.0))


def relay3_base(st0):
    g = [_north(1760.0, 340.0)]
    for k, (x, y) in RL.items():
        g.append(_ship_top(x, y, 120.0, 34.0, -90.0, sc(k)))
        g.append(_tline(x, y + 70, SRC[k][0], 28, sc(k), "middle", 300))
    return g


def relay3_stage(prev, st):
    s = []
    cx, cy = RL["cf"]
    if _on(prev, st, "hear"):
        for r in (90.0, 200.0, 320.0, 440.0):
            s.append(F.poly(_arcpts(cx, cy, r, r, 160, 200, 8), "none", sc("cf"), 5))
        s.append(_tline(720.0, cy - 120, "アンティリアン号へ送る", 28, sc("cf"), "middle", 400))
        for r in (200.0, 360.0, 520.0):
            s.append(F.poly(_arcpts(cx, cy, r, r, 5, 35, 6), "none", sc("cf"), 4, dash="10 8"))
        s.append(_tline(RL["tt"][0], RL["tt"][1] - 80, "横で聞く", 30, sc("tt"), "middle", 260))
    if _on(prev, st, "reply"):
        tx, ty = RL["tt"]
        s.append(_arrow(tx - 80, ty - 120, cx + 90, cy - 30, sc("tt"), 6, 24))
        s.append(_chip(1300.0, 380.0, "受け取った", sc("tt"), 32))
    return s


# ══════════════════════════════════════════════════════════
#  drown（c322）＝横から：タイタニック号と陸のケープ・レースの交信（弱い電波）→ 近くのカリフォルニアン号の強い電波がかき消す（G1 p.57）
# ══════════════════════════════════════════════════════════
DR = dict(yw=700.0, cr=230.0, tt=(760.0, 1160.0), cf=(1400.0, 1640.0), meter=(1000.0, 340.0))


def drown_base(st0):
    yw = DR["yw"]
    t0, t1 = DR["tt"]
    f0, f1 = DR["cf"]
    return [F.line(330.0, yw, 1800.0, yw, J.LINE_DIM, 3),
            F.poly([(110.0, yw - 20), (300.0, yw - 26), (330.0, yw + 30), (110.0, yw + 30)], J.BG2, J.LINE, 3, close=True),
            _tower(DR["cr"], yw - 22, 240.0, sc("cr")), _tline(DR["cr"], yw + 70, "ケープ・レース（陸）", 28, sc("cr"), "middle", 320),
            _ship_side(t0, t1, yw, sc("tt")), _tline((t0 + t1) / 2, yw + 50, "タイタニック号", 28, sc("tt"), "middle", 300),
            _ship_side(f0, f1, yw, sc("cf"), h=26.0), _tline((f0 + f1) / 2, yw + 50, "カリフォルニアン号", 28, sc("cf"), "middle", 320)]


def drown_stage(prev, st):
    s = []
    yw = DR["yw"]
    mx, my = DR["meter"]
    if _on(prev, st, "talk"):
        for r in (140.0, 280.0, 420.0):
            s.append(F.poly(_arcpts(DR["cr"], yw - 262, r, r, -12, 12, 6), "none", sc("cr"), 3, dash="8 10"))
        s.append(_tline(mx - 40, my + 8, "陸の電波", 28, sc("cr"), "end", 200) + F.rect(mx, my - 14, 110.0, 24, sc("cr"), None, None, rx=6))
    if _on(prev, st, "loud"):
        fx = DR["cf"][0] + 40
        for r in (60.0, 130.0, 200.0, 270.0):
            s.append(F.poly(_arcpts(fx, yw - 90, r, r, 160, 200, 6), "none", sc("cf"), 9))
        s.append(_tline(mx - 40, my + 78, "近くの船の電波", 28, sc("cf"), "end", 300) + F.rect(mx, my + 56, 520.0, 30, sc("cf"), None, None, rx=6))
        s.append(_xmark(mx + 160, my, 22, J.ALERT, 8))
        s.append(_chip(1600.0, 820.0 - 20, "報告書の見方", sc("rep"), 26))
    return s


# ══════════════════════════════════════════════════════════
#  第3章
#  watch（c403）＝横から見たタイタニック号の前（船首＝右）：船橋の一等航海士と操舵手・見張り台の見張り・鐘と電話の線（G1 p.39）
# ══════════════════════════════════════════════════════════
WT = dict(hull=(220.0, 1760.0, 790.0, 96.0), bridge=(1080.0, 560.0, 1260.0, 680.0), mast=1480.0, nest=(1446.0, 420.0, 68.0, 44.0))
WT_T = "22:00"


def watch_base(st0):
    x0, x1, yw, h = WT["hull"]
    b0, by0, b1, by1 = WT["bridge"]
    nx, ny, nw, nh = WT["nest"]
    m = WT["mast"]
    return [F.poly(_hull_side(x0, x1, yw, h), J.BG2, sc("tt"), 4, close=True),
            F.rect(b0, by0, b1 - b0, by1 - by0, J.BG2, sc("tt"), 4, rx=6),
            F.line(m, yw - h, m, 330.0, sc("tt"), 5), F.rect(nx, ny, nw, nh, J.BG2, sc("tt"), 4, rx=6),
            _tline(nx + nw + 20, ny + 32, "見張り台（見張り 2人）", 28, INK, "start", 380),
            _tline((b0 + b1) / 2, by0 - 18, "一等航海士", 28, INK, "middle", 220),
            _tline((b0 + b1) / 2, by1 - 36, "操舵手", 28, INK, "middle", 200),
            _tline((b0 + b1) / 2, by0 + 40, "船橋", 24, J.TICK, "middle", 160)]


def watch_stage(prev, st):
    s = []
    if _on(prev, st, "hand"):
        s.append(_clk(560.0, 400.0, WT_T, "tt", 30, mw=600))
        s.append(_chip(560.0, 480.0, "二等航海士 → 一等航海士", J.LINE, 30))
    if _on(prev, st, "ice"):
        nx, ny, nw, nh = WT["nest"]
        s.append(_bell(nx + nw / 2, ny - 50, 0.8, J.AMBER))
        s.append(F.poly([(nx + nw / 2, ny + nh), (nx + nw / 2 - 40, 520.0), (WT["bridge"][2] + 10, 600.0)], "none", J.AMBER, 4, dash="10 8"))
        s.append(_tline(1330.0, 520.0, "電話", 26, J.AMBER, "end", 120))
        s.append(_chip(560.0, 600.0, "氷が近い（二等航海士）", J.AMBER, 30))
    return s


# ══════════════════════════════════════════════════════════
#  helm（c406）＝上から見たタイタニック号：号令「ハード・ア・スターボード」→ 船首が左へ回る（当時の号令の決まり＝G2 p.4・G1 p.41「about two points to port」）
# ══════════════════════════════════════════════════════════
HM = dict(cx=1000.0, cy=570.0, L=430.0, W=96.0, pivot=(1000.0, 620.0))
HM_DEG = -22.5          # 約2点＝22.5度（左へ）＝G1 p.41


def helm_parts(st):
    rot = HM_DEG if st.get("turn") == "on" else 0.0
    return [_P("ship", "poly", _top_pts(HM["cx"], HM["cy"], HM["L"], HM["W"]), fill=J.BG2, stroke=sc("tt"), w=5, pivot=list(HM["pivot"]), rot=rot)]


def helm_base(st0):
    return [_tline(HM["cx"], HM["cy"] + HM["L"] / 2 + 40, "タイタニック号", 28, sc("tt"), "middle", 300)]


def helm_stage(prev, st):
    s = []
    if _on(prev, st, "order"):
        s.append(_chip(480.0, 470.0, "号令", sc("tt"), 32) + _tline(480.0, 540.0, "Hard-a-starboard（原文）", 28, INK, "middle", 420))
        s.append(_bell(380.0, 610.0, 0.8, J.AMBER) + _tline(420.0, 622.0, "見張りの鐘とほぼ同時", 26, J.AMBER, "start", 400))
    if _on(prev, st, "turn"):
        cx, cy = HM["pivot"]
        r = HM["L"] / 2 + 90
        pts = _arcpts(cx, cy, r, r, -90, -90 + HM_DEG, 8)
        s.append(F.poly(pts[:-1], "none", J.AMBER, 6) + _arrow(pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], J.AMBER, 6, 26))
        s.append(_tline(pts[-1][0] - 30, pts[-1][1] - 10, "船首は左へ", 34, J.AMBER, "end", 300))
        s.append(_chip(1480.0, 380.0, "当時の号令の決まり", rc("DOC"), 28))
    return s


# ══════════════════════════════════════════════════════════
#  olympic（c408）＝上から見た37秒の見積もり（オリンピック号の試験＝G1 p.41）：号令から約2点（約22度）回るまで約37秒・約466ヤード（約430メートル）。
#  船の長さ（登録の 852.5フィート＝G1 p.11）と進む道のりは同じ縮尺（1m＝0.9画素）
# ══════════════════════════════════════════════════════════
OL = dict(k=0.9, sx=1150.0, sy=820.0, W=34.0)
OL_V = (37, 466, 430, 22)              # 秒・ヤード・メートル（語りの丸め）・度（語り）
OL_SHIP_FT, OL_YD_M, OL_FT_M = 852.5, 0.9144, 0.3048
OL_TURN = 22.5                          # 2点＝22.5度（G1 p.41 の「two points」）＝絵の回り


def ol_path():
    L = OL_V[1] * OL_YD_M * OL["k"]
    th = math.radians(OL_TURN)
    R = L / th
    cx, cy = OL["sx"] - R, OL["sy"]
    return [(cx + R * math.cos(-th * i / 20), cy + R * math.sin(-th * i / 20)) for i in range(21)], L


def ol_ship_len():
    return OL_SHIP_FT * OL_FT_M * OL["k"]


def olympic_base(st0):
    return [F.circ(OL["sx"], OL["sy"], 12, J.LINE), _tline(OL["sx"] + 28, OL["sy"] + 10, "号令のとき", 26, J.TICK, "start", 240)]


def olympic_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(1600.0, 420.0, 72))
    if _on(prev, st, "test"):
        s.append(_chip(600.0, 350.0, "オリンピック号の試験からの見積もり", sc("ol"), 30))
    if _on(prev, st, "path"):
        pts, _L = ol_path()
        s.append(F.poly(pts, "none", J.AMBER, 6, dash="14 10"))
        bx, by = pts[-1]
        th = math.radians(OL_TURN)
        Ls = ol_ship_len()
        cxs, cys = bx + Ls / 2 * math.sin(th), by + Ls / 2 * math.cos(th)
        s.append(_ship_top(cxs, cys, Ls, OL["W"], -OL_TURN, sc("tt")))
        s.append(F.line(bx, by, bx, by - 130, J.TICK, 3, dash="8 8"))
        s.append(F.poly(_arcpts(bx, by, 100, 100, -90, -90 - OL_TURN, 6), "none", J.AMBER, 4))
        s.append(_tline(bx + 26, by - 96, f"約{OL_V[3]}度", 32, J.AMBER, "start", 200))
        mx, my = pts[10]
        s.append(_tline(mx - 48, my - 8, f"約{OL_V[2]}メートル", 34, INK, "end", 360) + _tline(mx - 48, my + 32, f"（{OL_V[1]}ヤード）", 26, J.TICK, "end", 300))
        s.append(_clock(500.0, 560.0, 40.0, J.AMBER) + _tline(560.0, 574.0, f"約{OL_V[0]}秒", 44, J.AMBER, "start", 240))
    return s


# ══════════════════════════════════════════════════════════
#  damage（c411）＝横から見たタイタニック号（船首＝右）：傷は船首から約300フィート（約90メートル）・前から6つの区画・10秒たらず（G1 p.42）。
#  傷の長さは船の長さ（登録の 852.5フィート＝G1 p.11）に比例・区画の境は模式
# ══════════════════════════════════════════════════════════
DM = dict(x0=200.0, x1=1760.0, deck=530.0, keel=720.0)
DM_V = (300, 90, 10, 20)               # フィート・メートル（語り）・秒・ノット（より速い）
DM_COMP = ("前", "1", "2", "3", "6", "5")
DM_F = (0.05, 0.12, 0.19, 0.27, 0.33, 0.40)    # 船首からの境の位置（船の長さの割合）＝模式


def dm_k():
    return (DM["x1"] - DM["x0"]) / OL_SHIP_FT


def dm_xd():
    return DM["x1"] - DM_V[0] * dm_k()


def damage_base(st0):
    x0, x1, d, kl = DM["x0"], DM["x1"], DM["deck"], DM["keel"]
    L = x1 - x0
    g = [F.poly([(x0, d), (x1, d - 14), (x1 - 80, kl), (x0 + 40, kl)], J.BG2, sc("tt"), 5, close=True)]
    prev = x1
    for i, f in enumerate(DM_F):
        x = x1 - f * L
        g.append(F.line(x, d + 6, x, kl - 4, J.LINE, 3))
        g.append(_tline((prev + x) / 2, kl + 40, DM_COMP[i], 30, INK, "middle", 80))
        prev = x
    g.append(_tline(1440.0, kl + 86, "前＝船首の区画　1〜3＝船倉　6と5＝ボイラー室", 26, J.TICK, "middle", 700))
    return g


def damage_stage(prev, st):
    s = []
    xd, x1 = dm_xd(), DM["x1"]
    if _on(prev, st, "dmg"):
        pts, x, up = [], xd, True
        while x < x1 - 96:
            pts.append((x, DM["keel"] - (30 if up else 16)))
            x += 26
            up = not up
        s.append(F.poly(pts, "none", J.ALERT, 7))
        y = DM["deck"] - 50
        s.append(F.poly([(xd, y + 16), (xd, y), (x1, y - 14), (x1, y + 2)], "none", J.ALERT, 5))
        s.append(_tline((xd + x1) / 2 - 70, y - 22, f"約{DM_V[1]}メートル", 34, J.ALERT, "end", 300)
                 + _tline((xd + x1) / 2 - 50, y - 22, f"（{DM_V[0]}フィート）", 26, J.TICK, "start", 260))
    if _on(prev, st, "sec"):
        s.append(_clock(470.0, 400.0, 40.0, J.AMBER) + _tline(530.0, 416.0, f"{DM_V[2]}秒たらず", 44, J.AMBER, "start", 300))
        s.append(_arrow(420.0, 470.0, 780.0, 470.0, J.LINE, 5, 22) + _tline(810.0, 480.0, f"{DM_V[3]}ノットより速く進む", 28, INK, "start", 360))
    return s


# ══════════════════════════════════════════════════════════
#  tray（c413）＝横から見た壁で仕切った区画の並び（船首＝右・模式）：1つに水 → ほかは守られる／前の5つに水 → 壁を越えて順に後ろへ（G1 p.45）
# ══════════════════════════════════════════════════════════
TR = dict(x0=240.0, x1=1680.0, top=430.0, wall=500.0, bot=720.0, n=9)
TR_FRONT = 5


def tr_box(i):
    w = (TR["x1"] - TR["x0"]) / TR["n"]
    return TR["x0"] + i * w, TR["x0"] + (i + 1) * w


def _tr_level(st, i):
    n = TR["n"]
    if st.get("five") == "on":
        if i >= n - TR_FRONT:
            return TR["wall"]
        if i == n - TR_FRONT - 1:
            return 640.0
        return None
    if st.get("one") == "on" and i == n - 1:
        return 600.0
    return None


def tray_parts(st):
    g = []
    for i in range(TR["n"]):
        a, b = tr_box(i)
        lv = _tr_level(st, i)
        y = lv if lv is not None else TR["bot"] - 2
        g.append(_P(f"w{i}", "poly", [(a + 6, y), (b - 6, y), (b - 6, TR["bot"] - 4), (a + 6, TR["bot"] - 4)], fill=sc("tt"), stroke=None, w=2,
                    alpha=0.85 if lv is not None else 0.0))
    return g


def tray_base(st0):
    g = [F.poly([(TR["x0"], TR["top"]), (TR["x0"], TR["bot"]), (TR["x1"], TR["bot"]), (TR["x1"] + 50, TR["top"])], "none", J.LINE, 5)]
    for i in range(1, TR["n"]):
        x = tr_box(i)[0]
        g.append(F.line(x, TR["wall"], x, TR["bot"], INK, 6))
    g.append(_tline(TR["x1"] + 40, TR["bot"] + 44, "船首", 26, J.TICK, "end", 120))
    return g


def tray_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(1700.0, 360.0, 72))
    if _on(prev, st, "one"):
        a, b = tr_box(1)
        s.append(_tline((a + b) / 2, TR["top"] - 30, "区画", 30, INK, "middle", 160) + F.line((a + b) / 2, TR["top"] - 18, (a + b) / 2, TR["wall"] + 40, J.TICK, 3))
        xw = tr_box(3)[0]
        s.append(_tline(xw, TR["top"] - 30, "壁", 30, INK, "middle", 80) + F.line(xw, TR["top"] - 18, xw, TR["wall"] - 8, J.TICK, 3))
        for i in range(TR["n"] - 1):
            a, b = tr_box(i)
            s.append(_check((a + b) / 2, 660.0, 18, J.OK))
        a, b = tr_box(TR["n"] - 1)
        s.append(_tline((a + b) / 2, TR["bot"] + 44, "1つに水", 28, sc("tt"), "middle", 160))
        s.append(_tline(700.0, TR["bot"] + 44, "ほかの区画は無事", 28, J.OK, "middle", 400))
    if _on(prev, st, "five"):
        a = tr_box(TR["n"] - TR_FRONT)[0]
        b = tr_box(TR["n"] - 1)[1]
        s.append(F.poly([(a, TR["top"] - 6), (a, TR["top"] - 22), (b, TR["top"] - 22), (b, TR["top"] - 6)], "none", J.ALERT, 5))
        s.append(_tline((a + b) / 2, TR["top"] - 40, f"前の{TR_FRONT}つ", 32, J.ALERT, "middle", 240))
        s.append(_arrow(a + 40, TR["wall"] - 20, a - 80, TR["wall"] - 20, J.ALERT, 6, 24))
        s.append(_tline(a - 8, 600.0, "順に後ろへ", 28, J.ALERT, "end", 260))
    return s


# ══════════════════════════════════════════════════════════
#  ttband（c416）＝時間の線（横・青）＝タイタニック号の時計だけ（G1 p.42・49・54・85）：23:40 衝突・0:05ごろ ボートの用意・0:15 CQD・0:45ごろ 信号弾・2:20 沈没
#  横は時刻に比例（1分＝9.25画素）。ほかの船の時刻は並べない（c637 はカリフォルニアン号の時計の縦の帯＝色と並びを替えた）
# ══════════════════════════════════════════════════════════
TT = dict(x0=220.0, x1=1700.0, y=590.0, h=46.0, t0=23 * 60 + 40, t1=26 * 60 + 20)
TT_EV = (("23:40", "衝突", "dn", "start"), ("0:05ごろ", "ボートの用意", "up", "boat"), ("0:15", "CQD", "dn", "radio"),
         ("0:45ごろ", "信号弾", "up", "radio"), ("2:20", "沈没", "dn", "start"))


def _min(t):
    h, m = [int(x) for x in re.findall(r"\d+", t)[:2]]
    return (h + (24 if h < 12 else 0)) * 60 + m


def tt_x(t):
    return TT["x0"] + (_min(t) - TT["t0"]) * (TT["x1"] - TT["x0"]) / (TT["t1"] - TT["t0"])


def _tt_ev(i):
    t, lab, side, _k = TT_EV[i]
    x, y, h = tt_x(t), TT["y"], TT["h"]
    if side == "up":
        return (F.line(x, y - h / 2, x, y - h / 2 - 20, sc("tt"), 4) + _tline(x, y - h / 2 - 32, t, 30, J.AMBER, "middle", 220)
                + _tline(x, y - h / 2 - 74, lab, 30, INK, "middle", 260))
    return (F.line(x, y + h / 2, x, y + h / 2 + 16, sc("tt"), 4) + _tline(x, y + h / 2 + 50, t, 30, J.AMBER, "middle", 220)
            + _tline(x, y + h / 2 + 92, lab, 30, INK, "middle", 260))


def ttband_base(st0):
    g = [F.rect(TT["x0"], TT["y"] - TT["h"] / 2, TT["x1"] - TT["x0"], TT["h"], sc("tt"), None, None, rx=10, op=0.55),
         _tline(TT["x0"], 400.0, "タイタニック号の時計", 32, sc("tt"), "start", 520)]
    for i, ev in enumerate(TT_EV):
        if ev[3] == "start":
            g.append(_tt_ev(i))
    return g


def ttband_stage(prev, st):
    s = []
    for key in ("boat", "radio"):
        if _on(prev, st, key):
            s += [_tt_ev(i) for i, ev in enumerate(TT_EV) if ev[3] == key]
    return s


# ══════════════════════════════════════════════════════════
#  第4章
#  cqd（c501）＝正面：CQD のモールス（C −·−·・Q −−·−・D −··＝国際の符号）と電鍵 → 四方への電波の線（いくつもの船・ケープ・レース＝G1 p.54）
# ══════════════════════════════════════════════════════════
CQ = dict(x0=360.0, ys=(470.0, 580.0, 690.0), dash=78.0, dot=13.0, gap=24.0, key=(1120.0, 760.0), ant=(1330.0, 600.0))
CQ_CODE = (("C", "−·−·"), ("Q", "−−·−"), ("D", "−··"))
CQ_T = "0:15"


def _morse(x, y, code, col):
    g = []
    for ch in code:
        if ch == "−":
            g.append(F.rect(x, y - 13, CQ["dash"], 26, col, None, None, rx=13))
            x += CQ["dash"] + CQ["gap"]
        else:
            g.append(F.circ(x + CQ["dot"], y, CQ["dot"], col))
            x += 2 * CQ["dot"] + CQ["gap"]
    return "".join(g)


def cqd_base(st0):
    kx, ky = CQ["key"]
    return [F.rect(kx - 110, ky, 220, 30, J.BG2, J.LINE, 4, rx=6), F.line(kx - 90, ky - 6, kx + 70, ky - 28, J.LINE, 8),
            F.circ(kx + 78, ky - 34, 18, J.LINE), _tline(kx, ky + 74, "電鍵", 26, J.TICK, "middle", 120),
            F.line(kx + 110, ky + 10, CQ["ant"][0], ky + 10, J.LINE_DIM, 3), F.line(CQ["ant"][0], ky + 10, CQ["ant"][0], CQ["ant"][1], J.LINE, 4)]


def cqd_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(1730.0, 330.0, 72))
    if _on(prev, st, "code"):
        for (L, code), y in zip(CQ_CODE, CQ["ys"]):
            s.append(F.txt(300.0, y + 20, L, 56, J.AMBER, "Dela", "middle") + _morse(CQ["x0"], y, code, INK))
        s.append(_chip(520.0, 360.0, "遭難の合図", J.ALERT, 30))
        s.append(_clk(1000.0, 370.0, CQ_T, "tt", 30))
    if _on(prev, st, "out"):
        ax, ay = CQ["ant"]
        for ex, ey in ((1560.0, 470.0), (1640.0, 600.0), (1560.0, 730.0)):
            s.append(_arrow(ax + 20, ay, ex - 40, ey, J.LINE, 5, 22))
        s.append(_ship_side(1580.0, 1700.0, 610.0, J.LINE, h=18.0) + _ship_side(1500.0, 1620.0, 744.0, J.LINE, h=18.0))
        s.append(_tline(1640.0, 820.0, "いくつもの船", 28, INK, "middle", 260))
        s.append(_tower(1560.0, 470.0, 110.0, sc("cr")) + _tline(1620.0, 440.0, "ケープ・レース", 28, sc("cr"), "start", 240))
    return s


# ══════════════════════════════════════════════════════════
#  carp（c505）＝上から：カルパチア号が 0:35（カルパチア号の時計）に受ける → 回す → 北52度西へ約107キロ（58マイル）・途中の氷山の印（G7 PDF 23〜24頁）
# ══════════════════════════════════════════════════════════
CP = dict(cx=1360.0, cy=740.0, L=120.0, W=34.0, len=560.0)
CP_V = ("0:35", 52, 107)
CP_ROT0 = 90.0                           # 受けたときの向き（東＝地中海へ向かう途中＝絵の頭の向き）


def carp_parts(st):
    rot = -float(CP_V[1]) if st.get("turn") == "on" else CP_ROT0
    return [_P("ship", "poly", _top_pts(CP["cx"], CP["cy"], CP["L"], CP["W"]), fill=J.BG2, stroke=sc("cp"), w=5, pivot=[CP["cx"], CP["cy"]], rot=rot)]


def cp_bow():
    a = math.radians(-CP_V[1])
    return CP["cx"] + CP["L"] / 2 * math.sin(a), CP["cy"] - CP["L"] / 2 * math.cos(a)


def cp_end():
    a = math.radians(-CP_V[1])
    bx, by = cp_bow()
    return bx + CP["len"] * math.sin(a), by - CP["len"] * math.cos(a)


def carp_base(st0):
    return [_north(1740.0, 380.0), _tline(CP["cx"] + 90, CP["cy"] + 10, "カルパチア号", 28, sc("cp"), "start", 300)]


def carp_stage(prev, st):
    s = []
    if _on(prev, st, "get"):
        s.append(_waves(CP["cx"] - 30, CP["cy"] - 60, 30, 2, sc("cp"), -150, -30, 18, 4))
        s.append(_clk(1460.0, 840.0 - 10, CP_V[0], "cp", 28, mw=560))
    if _on(prev, st, "turn"):
        bx, by = cp_bow()
        ex, ey = cp_end()
        s.append(_arrow(bx, by, ex, ey, sc("cp"), 6, 26))
        s.append(_xmark(ex - 24, ey - 20, 18, sc("tt"), 6) + _tline(ex - 56, ey - 14, "知らせの位置", 28, sc("tt"), "end", 300))
        s.append(F.line(bx, by, bx, by - 150, J.TICK, 3, dash="8 8"))
        s.append(F.poly(_arcpts(bx, by, 110, 110, -90, -90 - CP_V[1], 8), "none", J.AMBER, 4))
        s.append(_tline(bx + 24, by - 120, f"北から西へ{CP_V[1]}度", 28, J.AMBER, "start", 300))
        mx, my = (bx + ex) / 2, (by + ey) / 2
        s.append(_tline(mx + 50, my - 50, f"約{CP_V[2]}キロ", 34, INK, "start", 260))
        s.append(_ice(980.0, 470.0, 0.9) + _ice(1150.0, 600.0, 0.7) + _ice(900.0, 560.0, 0.6))
        s.append(_tline(900.0, 610.0, "氷山", 24, J.TICK, "middle", 100))
    return s


# ══════════════════════════════════════════════════════════
#  rockets_n（c510）＝正面の2つの札：報告書「約8発」（G1 p.54）／四等航海士の証言「6発から12発」・間隔「たぶん5分」（T1 Q15395・Q15399＝書き起こし）
# ══════════════════════════════════════════════════════════
RN = dict(l=(220.0, 900.0), r=(1020.0, 1700.0), y0=440.0, y1=830.0)
RN_V = (8, (6, 12), 5)


def rockets_n_base(st0):
    return []


def rockets_n_stage(prev, st):
    s = []
    y0, y1 = RN["y0"], RN["y1"]
    if _on(prev, st, "q"):
        s.append(_qmark(960.0, 380.0, 72))
    if _on(prev, st, "rep"):
        a, b = RN["l"]
        c = sc("rep")
        s.append(F.rect(a, y0, b - a, y1 - y0, J.BG2, c, 4, rx=16) + _tline((a + b) / 2, y0 + 52, "報告書", 30, c, "middle", 300))
        s.append(_tline((a + b) / 2, 620.0, f"約{RN_V[0]}発", 76, INK, "middle", 400))
        for i in range(RN_V[0]):
            s.append(_burst(a + 70 + i * 78, 730.0, J.SUB, 26))
    if _on(prev, st, "say"):
        a, b = RN["r"]
        c = sc("mate")
        lo, hi = RN_V[1]
        s.append(F.rect(a, y0, b - a, y1 - y0, J.BG2, c, 4, rx=16) + _tline((a + b) / 2, y0 + 52, "四等航海士の証言", 30, c, "middle", 400))
        s.append(_tline((a + b) / 2, 590.0, f"{lo}発から{hi}発", 56, INK, "middle", 560))
        for i in range(hi):
            x, y = a + 90 + (i % 6) * 100, 660.0 + (i // 6) * 70
            s.append(_burst(x, y, J.SUB, 24) if i < lo else F.circ(x, y, 22, "none", J.TICK, 3))
        xa, xb = a + 90, a + 190
        s.append(F.poly([(xa, 768.0), (xa, 782.0), (xb, 782.0), (xb, 768.0)], "none", J.AMBER, 4))
        s.append(_tline(xb + 24, 794.0, f"間隔は たぶん{RN_V[2]}分", 28, J.AMBER, "start", 360))
    return s


# ══════════════════════════════════════════════════════════
#  colors（c516）＝正面の夜空：当時の遭難の信号は何色でもよい（G2 p.18）→ タイタニック号のは白＝ほかの信号と色では見分けがつかない
# ══════════════════════════════════════════════════════════
CL_ROW = ("SUB", "ALERT", "OK", "USCG", "AMBER")
CL_TT = "SUB"


def colors_base(st0):
    return [F.rect(200.0, 320.0, 1520.0, 490.0, J.BG, J.LINE_DIM, 3, rx=20)]


def colors_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(960.0, 400.0, 72))
    if _on(prev, st, "any"):
        for i, c in enumerate(CL_ROW):
            s.append(_burst(330.0 + i * 170, 540.0, rc(c), 42, 6))
        s.append(_tline(670.0, 680.0, "当時の決まり：何色でもよい", 32, INK, "middle", 700))
    if _on(prev, st, "white"):
        s.append(_burst(1340.0, 540.0, rc(CL_TT), 52, 7) + _burst(1590.0, 540.0, J.SUB, 44, 6))
        s.append(_tline(1340.0, 650.0, "タイタニック号＝白", 30, sc("tt"), "middle", 300))
        s.append(_tline(1590.0, 650.0, "ほかの信号", 30, INK, "middle", 220))
        s.append(_tline(1465.0, 740.0, "見分けがつかない", 32, J.AMBER, "middle", 400))
    return s


# ══════════════════════════════════════════════════════════
#  第5章
#  field（c602）＝上から：カリフォルニアン号が 22:20ごろ（カリフォルニアン号の時計）氷原の手前で機関を逆に回して止まる → 氷原は北にも南にも（G1 p.56）
# ══════════════════════════════════════════════════════════
FD = dict(cy=560.0, x_from=1500.0, x_stop=720.0, L=130.0, W=36.0)
FD_T = "22:20ごろ"


def field_parts(st):
    dx = FD["x_stop"] - FD["x_from"] if st.get("stop") == "on" else 0.0
    return [_P("ship", "poly", _top_pts(FD["x_from"], FD["cy"], FD["L"], FD["W"]), fill=J.BG2, stroke=sc("cf"), w=5,
               pivot=[FD["x_from"], FD["cy"]], rot=-90.0, dx=dx)]


def field_base(st0):
    pts = [(300.0, 300.0), (560.0, 310.0), (590.0, 420.0), (540.0, 560.0), (600.0, 700.0), (560.0, 840.0), (280.0, 840.0), (320.0, 640.0), (260.0, 480.0)]
    g = [F.poly(pts, J.SUB, J.TICK, 3, close=True, op=0.75)]
    for (a, b) in (((340.0, 400.0), (480.0, 380.0)), ((360.0, 600.0), (520.0, 640.0)), ((330.0, 760.0), (500.0, 730.0))):
        g.append(F.line(a[0], a[1], b[0], b[1], J.TICK, 3))
    g.append(_tline(720.0, 420.0, "氷原", 30, J.SUB, "start", 160))
    g.append(_north(1760.0, 370.0))
    return g


def field_stage(prev, st):
    s = []
    if _on(prev, st, "stop"):
        s.append(F.line(FD["x_stop"] + 90, FD["cy"], FD["x_from"] + 60, FD["cy"], sc("cf"), 3, dash="10 12"))
        s.append(_arrow(FD["x_stop"] + 80, FD["cy"] + 70, FD["x_stop"] + 230, FD["cy"] + 70, J.AMBER, 6, 24))
        s.append(_tline(FD["x_stop"] + 250, FD["cy"] + 80, "機関を逆に回して止まる", 30, J.AMBER, "start", 440))
        s.append(_clk(1250.0, 420.0, FD_T, "cf", 30))
    if _on(prev, st, "ice"):
        s.append(_arrow(640.0, 470.0, 640.0, 300.0, J.SUB, 5, 22) + _tline(670.0, 320.0, "北へ続く", 28, J.SUB, "start", 200))
        s.append(_arrow(640.0, 680.0, 640.0, 840.0, J.SUB, 5, 22) + _tline(670.0, 830.0, "南へ続く", 28, J.SUB, "start", 200))
        s.append(_tline(860.0, 760.0, "見える限り", 30, J.SUB, "start", 260))
    return s


# ══════════════════════════════════════════════════════════
#  drift（c604）＝上から：当時タイタニック号が沈んだとされた位置と、カリフォルニアン号の推測の位置（その北・北微東 約19マイル＝約35キロ＝G1 p.56）→
#  推測の位置は海の流れなどでずれる（右の小さな枠＝流れは南微西＝G2 p.9・値は描かない）
# ══════════════════════════════════════════════════════════
DF = dict(a=(860.0, 720.0), len=380.0, box=(1290.0, 470.0, 1780.0, 800.0))
DF_V = (19, 35)
DF_BRG = 11.25            # 北微東（N. by E.）＝11.25度
DF_CUR = 191.25           # 南微西（south by west）


def df_b():
    a = math.radians(DF_BRG)
    return DF["a"][0] + DF["len"] * math.sin(a), DF["a"][1] - DF["len"] * math.cos(a)


def drift_base(st0):
    ax, ay = DF["a"]
    return [_north(1740.0, 370.0), _xmark(ax, ay, 20, sc("tt"), 7),
            _tline(ax, ay + 60, "タイタニック号", 26, sc("tt"), "middle", 300) + _tline(ax, ay + 96, "当時の報告の沈没位置", 26, sc("tt"), "middle", 400)]


def drift_stage(prev, st):
    s = []
    bx, by = df_b()
    ax, ay = DF["a"]
    if _on(prev, st, "pts"):
        s.append(F.circ(bx, by, 16, sc("cf")) + _tline(bx + 34, by + 10, "カリフォルニアン号（推測の位置）", 28, sc("cf"), "start", 560))
    if _on(prev, st, "dist"):
        s.append(F.line(ax, ay - 24, bx, by + 20, J.AMBER, 4, dash="12 10"))
        t = 0.48
        s.append(_tline(ax + (bx - ax) * t + 40, ay + (by - ay) * t + 10, f"約{DF_V[1]}キロ（{DF_V[0]}マイル）", 32, J.AMBER, "start", 400))
    if _on(prev, st, "cur"):
        x0, y0, x1, y1 = DF["box"]
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE_DIM, 3, rx=14))
        a = math.radians(DF_CUR)
        ux, uy = math.sin(a), -math.cos(a)
        px, py = x0 + 140, y0 + 90
        s.append(F.circ(px, py, 14, sc("cf")) + _tline(px + 30, py + 10, "推測の位置", 26, sc("cf"), "start", 220))
        qx, qy = px + 170 * ux, py + 170 * uy
        s.append(_arrow(px, py + 20, qx, qy - 20, sc("cr"), 5, 22) + F.circ(qx, qy, 14, "none", sc("cf"), 3))
        s.append(_tline(qx + 30, qy + 10, "ずれる", 26, INK, "start", 160))
        for i in range(3):
            xx = x0 + 380 + i * 40
            s.append(_arrow(xx, y0 + 60, xx + 90 * ux, y0 + 60 + 90 * uy, sc("cr"), 3, 14))
        s.append(_tline(x0 + 340, y1 - 26, "海の流れ", 26, sc("cr"), "start", 200))
    return s


# ══════════════════════════════════════════════════════════
#  sidelights（c607）＝上から見た船（船首＝上・模式）：右に緑・左に赤・マストに白の灯 → 見える色で向きが分かる →
#  船長の話＝23:00〜23:30（カリフォルニアン号の時計）に約5マイル（約9キロ）先に緑（G1 p.57）
# ══════════════════════════════════════════════════════════
SL = dict(cx=960.0, cy=600.0, L=340.0, W=96.0, ly=540.0, r=270.0, eye=(1700.0, 640.0))
SL_SIDE = dict(right="green", left="red", mast="white")
SL_V = (5, 9)


def sl_lamp(side):
    if side == "mast":
        return SL["cx"], SL["ly"] - 70
    d = SL["W"] / 2 + 10
    return (SL["cx"] + d if side == "right" else SL["cx"] - d), SL["ly"]


def sidelights_base(st0):
    return [_ship_top(SL["cx"], SL["cy"], SL["L"], SL["W"], 0.0, J.LINE),
            _tline(SL["cx"] + SL["W"] / 2 + 20, SL["cy"] + SL["L"] / 2 - 10, "船首は上", 24, J.TICK, "start", 160)]


def sidelights_stage(prev, st):
    s = []
    if _on(prev, st, "green"):
        for i in range(5):
            s.append(F.circ(SL["cx"], SL["cy"] - 60 + i * 40, 7, J.AMBER))
        x, y = sl_lamp("right")
        s.append(_lamp(x, y, LIGHT[SL_SIDE["right"]], 12))
        s.append(_say(1540.0, 370.0, "cap", "緑の舷灯を見た"))
    if _on(prev, st, "two"):
        xr, yr = sl_lamp("right")
        xl, yl = sl_lamp("left")
        xm, ym = sl_lamp("mast")
        s.append(F.poly([(xr, yr)] + _arcpts(xr, yr, SL["r"], SL["r"], -90, 22.5, 10), LIGHT["green"], None, close=True, op=0.16))
        s.append(F.poly([(xl, yl)] + _arcpts(xl, yl, SL["r"], SL["r"], -202.5, -90, 10), LIGHT["red"], None, close=True, op=0.16))
        s.append(_lamp(xl, yl, LIGHT[SL_SIDE["left"]], 12) + _lamp(xm, ym, LIGHT[SL_SIDE["mast"]], 12))
        s.append(_tline(xr + SL["r"] + 30, yr - 30, "右側は緑", 32, LIGHT["green"], "start", 240))
        s.append(_tline(xl - SL["r"] - 30, yl - 30, "左側は赤", 32, LIGHT["red"], "end", 240))
        s.append(_tline(SL["cx"], 840.0, "色＝船の向きの手がかり", 30, INK, "middle", 600))
    if _on(prev, st, "seen"):
        ex, ey = SL["eye"]
        xr, yr = sl_lamp("right")
        s.append(_eye(ex, ey, sc("cap")) + F.line(ex - 56, ey - 4, xr + 30, yr + 6, sc("cap"), 3, dash="10 10"))
        s.append(_tline(1440.0, 690.0, f"約{SL_V[1]}キロ（{SL_V[0]}マイル）", 30, INK, "middle", 360))
        s.append(_clk(1450.0, 770.0, "23:00〜23:30", "cf", 26, mw=620))
    return s


# ══════════════════════════════════════════════════════════
#  masts2（c609）＝正面の2隻（横の姿・模式）：マストの灯1つの船と2つの船 → 三等航海士の見方＝2つ見えた・明らかに客船 → 船長に伝えた（G1 p.57）
# ══════════════════════════════════════════════════════════
MS = dict(a=(240.0, 820.0), b=(1080.0, 1700.0), yw=700.0)
MS_V = (1, 2)


def masts2_base(st0):
    yw = MS["yw"]
    a0, a1 = MS["a"]
    b0, b1 = MS["b"]
    g = [F.line(200.0, yw, 1760.0, yw, J.LINE_DIM, 3), _ship_side(a0, a1, yw, J.LINE), _ship_side(b0, b1, yw, J.LINE)]
    x, y = _mast_tops(a0, a1, yw)[1]
    g.append(_lamp(x, y, LIGHT["white"], 11))
    g.append(_tline((a0 + a1) / 2, yw + 60, f"マストの灯 {MS_V[0]}つ", 30, INK, "middle", 300))
    return g


def ms_lights_b():
    b0, b1 = MS["b"]
    (x0, y0), (x1, y1) = _mast_tops(b0, b1, MS["yw"])
    return [(x0, y0), (x1, y1 + 40)]           # 後ろの灯は高く・前の灯は低く（模式）


def masts2_stage(prev, st):
    s = []
    b0, b1 = MS["b"]
    if _on(prev, st, "who"):
        s.append(_chip((b0 + b1) / 2, 360.0, "三等航海士の見方", sc("mate"), 30))
    if _on(prev, st, "two"):
        for x, y in ms_lights_b():
            s.append(_lamp(x, y, LIGHT["white"], 11))
        s.append(_tline((b0 + b1) / 2, MS["yw"] + 60, f"マストの灯 {MS_V[1]}つ", 30, INK, "middle", 300))
        s.append(_chip((b0 + b1) / 2, 440.0, "明らかに客船", sc("mate"), 32))
        s.append(_arrow(b0 + 60, 440.0, 900.0, 440.0, sc("mate"), 5, 22) + _chip(760.0, 440.0, "船長へ", sc("cap"), 30))
    return s


# ══════════════════════════════════════════════════════════
#  morse（c611）＝正面：モールス灯の短い光と長い光（灯の点と線）→ 遠くの灯「答えは？」＝船長の指示（G1 p.57）
# ══════════════════════════════════════════════════════════
MO = dict(lamp=(400.0, 600.0), x0=560.0, y=600.0, far=(1620.0, 600.0))
MO_SEQ = "··−·−−"


def morse_base(st0):
    lx, ly = MO["lamp"]
    fx, fy = MO["far"]
    return [F.line(lx, ly + 40, lx, 820.0, J.LINE, 6), F.rect(lx - 50, ly - 40, 100, 80, J.BG2, J.LINE, 5, rx=10),
            F.line(lx - 30, ly - 14, lx + 30, ly - 14, J.LINE_DIM, 4) + F.line(lx - 30, ly + 14, lx + 30, ly + 14, J.LINE_DIM, 4),
            _tline(lx - 26, ly + 90, "モールス灯", 26, J.TICK, "end", 200), F.circ(fx, fy, 9, J.TICK)]


def morse_stage(prev, st):
    s = []
    if _on(prev, st, "call"):
        s.append(_say(MO["lamp"][0], 400.0, "cap", "モールス灯で呼べ"))
        x, y = MO["x0"], MO["y"]
        first = {}
        for ch in MO_SEQ:
            if ch == "·":
                s.append(F.circ(x + 18, y, 38, J.AMBER, None, op=0.20) + F.circ(x + 18, y, 18, J.AMBER))
                first.setdefault("short", x + 18)
                x += 36 + 46
            else:
                s.append(F.rect(x - 10, y - 32, 130, 64, J.AMBER, None, None, rx=32, op=0.20) + F.rect(x, y - 18, 110, 36, J.AMBER, None, None, rx=18))
                first.setdefault("long", x + 55)
                x += 110 + 46
        s.append(_tline(first["short"], y + 80, "短い光", 28, J.AMBER, "middle", 160))
        s.append(_tline(first["long"], y + 80, "長い光", 28, J.AMBER, "middle", 160))
        fx, fy = MO["far"]
        s.append(_qmark(fx, fy - 100, 64) + _tline(fx, fy + 70, "答えは？", 30, INK, "middle", 200))
    return s


# ══════════════════════════════════════════════════════════
#  views2（c612）＝横から：2人の見立て（三等航海士の話＝船長「客船には見えない」／三等航海士「客船です」）と、止まったとき消えたように見えた灯りの列（G1 p.57）
# ══════════════════════════════════════════════════════════
VW = dict(x0=700.0, x1=1220.0, yw=740.0, n=8)
VW_SAY = ("客船には見えない", "客船です")


def vw_lights():
    x0, x1, yw = VW["x0"], VW["x1"], VW["yw"]
    h = (x1 - x0) * 0.09
    return [(x0 + (x1 - x0) * (0.22 + 0.56 * i / (VW["n"] - 1)), yw - h - 14) for i in range(VW["n"])]


def views2_parts(st):
    a = 0.18 if st.get("b") == "on" else 1.0
    return [_P(f"l{i}", "poly", _cpts(x, y, 9), fill=J.AMBER, stroke=None, w=2, alpha=a) for i, (x, y) in enumerate(vw_lights())]


def views2_base(st0):
    return [F.line(200.0, VW["yw"], 1760.0, VW["yw"], J.LINE_DIM, 3), _ship_side(VW["x0"], VW["x1"], VW["yw"], J.LINE)]


def views2_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_say(390.0, 430.0, "cap", VW_SAY[0]) + _tline(390.0, 506.0, "（三等航海士の話）", 24, J.TICK, "middle", 300))
    if _on(prev, st, "b"):
        s.append(_say(1530.0, 430.0, "mate", VW_SAY[1]))
        s.append(_tline(960.0, 810.0, "止まったとき → 灯りが消えて見えた", 28, INK, "middle", 620))
    if _on(prev, st, "diff"):
        s.append(_neq(960.0, 420.0) + _tline(960.0, 510.0, "見立てが違う", 32, J.ALERT, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  watches（c613）＝時間の線（横）：カリフォルニアン号の3つの当直（夜・真夜中から・朝＝G1 p.57〜59）と、23:40 の1つの鐘（真夜中からの当直を起こす）
#  横は時刻に比例（外の端の時刻は記録に無い＝出さない）
# ══════════════════════════════════════════════════════════
WW = dict(x0=200.0, x1=1720.0, t0=20 * 60, t1=32 * 60, y=580.0, h=84.0)
WW_BLK = (("夜の当直", "三等航海士", "20:00", "0:00"), ("真夜中からの当直", "二等航海士", "0:00", "4:00"), ("朝の当直", "一等航海士", "4:00", "8:00"))
WW_EV = "23:40"


def ww_x(t):
    m = _min(t)
    if m < WW["t0"]:
        m += 24 * 60
    return WW["x0"] + (m - WW["t0"]) * (WW["x1"] - WW["x0"]) / (WW["t1"] - WW["t0"])


def watches_base(st0):
    y, h = WW["y"], WW["h"]
    g = [_tline(1720.0, 400.0, "カリフォルニアン号の時計", 30, sc("cf"), "end", 520)]
    for i, (name, who, a, b) in enumerate(WW_BLK):
        xa, xb = ww_x(a) if i else WW["x0"], ww_x(b) if i < 2 else WW["x1"]
        g.append(F.rect(xa + 3, y - h / 2, xb - xa - 6, h, sc("mate"), None, None, rx=8, op=(0.30, 0.48, 0.30)[i]))
        g.append(_tline((xa + xb) / 2, y + 11, who, 30, INK, "middle", xb - xa - 30))
        g.append(_tline((xa + xb) / 2, y - h / 2 - 22, name, 28, INK, "middle", xb - xa - 30))
    for t in ("0:00", "4:00"):
        x = ww_x(t)
        g.append(F.line(x, y + h / 2, x, y + h / 2 + 18, J.LINE, 4) + _tline(x, y + h / 2 + 52, t, 30, J.AMBER, "middle", 140))
    return g


def watches_stage(prev, st):
    s = []
    x, y, h = ww_x(WW_EV), WW["y"], WW["h"]
    if _on(prev, st, "out"):
        s.append(F.line(x, y - h / 2 - 96, x, y + h / 2 + 6, J.ALERT, 5))
        s.append(_tline(x, y - h / 2 - 108, WW_EV, 32, J.AMBER, "middle", 160))
        s.append(_tline(x - 20, y - h / 2 - 150, "灯が消えた（三等航海士の話）", 28, J.ALERT, "end", 520))
    if _on(prev, st, "bell"):
        s.append(_bell(x - 40, y + h / 2 + 110, 0.9, J.AMBER))
        s.append(_tline(x - 4, y + h / 2 + 130, "鐘1つ＝次の当直を起こす", 28, J.AMBER, "start", 520))
    return s


# ══════════════════════════════════════════════════════════
#  bearing（c617）＝上から：羅針盤の目盛りとカリフォルニアン号（真ん中）→ 相手の船への線（方位）→ 変わるか・近づくか＝船長の指示（G1 p.58）
# ══════════════════════════════════════════════════════════
BR = dict(cx=720.0, cy=580.0, r=220.0, brg=105.0, d=430.0)


def br_pt(brg, d):
    a = math.radians(brg)
    return BR["cx"] + d * math.sin(a), BR["cy"] - d * math.cos(a)


def bearing_base(st0):
    cx, cy, r = BR["cx"], BR["cy"], BR["r"]
    g = [F.circ(cx, cy, r, "none", J.LINE, 4)]
    for i in range(36):
        a = math.radians(i * 10)
        r0 = r - (26 if i % 9 == 0 else 14)
        g.append(F.line(cx + r0 * math.sin(a), cy - r0 * math.cos(a), cx + r * math.sin(a), cy - r * math.cos(a), J.LINE, 3 if i % 9 else 5))
    g.append(_tline(cx, cy - r - 22, "北", 28, J.TICK, "middle", 80))
    g.append(_ship_top(cx, cy, 90.0, 26.0, -90.0, sc("cf")) + _tline(cx, cy + 60, "カリフォルニアン号", 24, sc("cf"), "middle", 260))
    x, y = br_pt(BR["brg"], BR["d"])
    g.append(_ship_top(x, y, 90.0, 26.0, -60.0, J.TICK) + _tline(x, y + 74, "相手の船", 24, J.TICK, "middle", 160))
    return g


def bearing_stage(prev, st):
    s = []
    cx, cy = BR["cx"], BR["cy"]
    x, y = br_pt(BR["brg"], BR["d"])
    if _on(prev, st, "watch"):
        s.append(F.line(cx, cy, x - 40, y - 10, J.AMBER, 4))
        x2, y2 = br_pt(BR["brg"] - 22, BR["d"])
        s.append(_ship_top(x2, y2, 90.0, 26.0, -60.0, J.TICK, dash="8 8", op=0.7))
        pts = _arcpts(cx, cy, BR["d"] + 70, BR["d"] + 70, BR["brg"] - 90 - 4, BR["brg"] - 90 - 18, 6)
        s.append(F.poly(pts[:-1], "none", J.LINE, 4) + _arrow(pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], J.LINE, 4, 18))
        s.append(_tline(pts[-1][0] + 20, pts[-1][1] + 40, "方位が変わる？", 26, INK, "start", 260))
        x3, y3 = br_pt(BR["brg"], BR["d"] - 150)
        s.append(_arrow(x - 60, y - 14, x3, y3, J.LINE, 4, 18) + _tline(1000.0, 636.0, "近づく？", 26, INK, "start", 160))
        s.append(_say(1520.0, 780.0, "cap", "変わったら知らせよ"))
    if _on(prev, st, "mean"):
        s.append(F.line(cx, cy, cx, cy - BR["r"] + 30, J.AMBER, 3, dash="8 8"))
        pts = _arcpts(cx, cy, 120, 120, -90, BR["brg"] - 90, 10)
        s.append(F.poly(pts, "none", J.AMBER, 6))
        s.append(F.line(pts[4][0], pts[4][1], 1060.0, 372.0, J.AMBER, 3))
        s.append(_tline(1080.0, 386.0, "方位＝相手の向き", 36, J.AMBER, "start", 420))
    return s


# ══════════════════════════════════════════════════════════
#  flicker（c619）＝正面の2本の光の帯：モールスの光（決まった長さの点と線）とただの瞬き（ばらばらに揺れる）→ 見習いは一度モールスと思って答え、考え直した（G1 p.58）
# ══════════════════════════════════════════════════════════
FK = dict(ya=440.0, yb=690.0, x0=420.0)
FK_MORSE = "−·−··−·"
FK_FLICK = ((0, 12, 1.0), (60, 7, 0.5), (140, 15, 0.9), (190, 6, 0.4), (300, 10, 0.8), (360, 5, 0.35), (420, 13, 0.85), (560, 8, 0.6),
            (610, 14, 1.0), (700, 6, 0.4), (820, 11, 0.7), (900, 7, 0.5))


def flicker_base(st0):
    g = []
    for y, t in ((FK["ya"], "モールスの光（決まった長さの点と線）"), (FK["yb"], "ただの瞬き（ばらばら）")):
        g.append(F.line(FK["x0"] - 20, y, 1440.0, y, J.LINE_DIM, 2) + _lamp(300.0, y, J.SUB, 12) + _tline(FK["x0"], y - 56, t, 28, INK, "start", 640))
    x = FK["x0"]
    for ch in FK_MORSE:
        if ch == "·":
            g.append(F.circ(x + 14, FK["ya"], 14, J.AMBER))
            x += 28 + 30
        else:
            g.append(F.rect(x, FK["ya"] - 14, 84, 28, J.AMBER, None, None, rx=14))
            x += 84 + 30
    for dx, r, op in FK_FLICK:
        g.append(F.circ(FK["x0"] + 20 + dx, FK["yb"], r, J.AMBER, None, op=op))
    return g


def flicker_stage(prev, st):
    s = []
    if _on(prev, st, "think"):
        s.append(_say(1640.0, FK["ya"], "mate", "モールス？", w=240) + _tline(1640.0, FK["ya"] + 76, "見習いが答えた", 26, sc("mate"), "middle", 260))
    if _on(prev, st, "fix"):
        s.append(_check(1560.0, FK["yb"], 26, J.OK) + _tline(1600.0, FK["yb"] + 12, "考え直した", 30, J.OK, "start", 220))
        s.append(_xmark(1760.0, FK["ya"] - 36, 18, J.ALERT, 7))
    return s


# ══════════════════════════════════════════════════════════
#  section（c620）＝横から見たカリフォルニアン号の前の断面（船首＝右・模式）：船橋とその下の海図室・伝声管 →
#  0:30すぎ 機関室の乗組員が信号弾2発を見た → 1:10ごろ（二等航海士の話）伝声管で船長へ「白い信号弾 5発」（G1 p.58）
# ══════════════════════════════════════════════════════════
SE = dict(hull=(300.0, 1500.0, 800.0, 160.0), bridge=(820.0, 1260.0, 440.0), chart=(860.0, 470.0, 1220.0, 620.0), pipe=1170.0, sky=(1680.0, 560.0))
SE_V = ("0:30すぎ", 2, "1:10ごろ", 5)


def section_base(st0):
    x0, x1, yw, h = SE["hull"]
    b0, b1, by = SE["bridge"]
    c0, cy0, c1, cy1 = SE["chart"]
    p = SE["pipe"]
    g = [F.poly(_hull_side(x0, x1, yw, h), J.BG2, sc("cf"), 5, close=True), F.rect(b0, by, b1 - b0, yw - h - by, J.BG2, sc("cf"), 4, rx=4),
         F.line(b0 - 30, by, b1 + 30, by, sc("cf"), 6), F.line(b0 - 30, by - 40, b1 + 30, by - 40, sc("cf"), 3),
         F.rect(c0, cy0, c1 - c0, cy1 - cy0, J.BG, sc("cf"), 3, rx=6), _tline((c0 + c1) / 2 - 50, cy1 - 24, "海図室", 26, J.TICK, "middle", 200),
         F.line(p - 8, by - 30, p - 8, cy0 + 70, INK, 4) + F.line(p + 8, by - 30, p + 8, cy0 + 70, INK, 4),
         F.circ(p, by - 34, 14, "none", INK, 4) + F.circ(p, cy0 + 74, 14, "none", INK, 4),
         _tline(p + 30, by - 50, "伝声管", 26, INK, "start", 160), _tline(c0 + 60, by - 56, "船橋", 26, J.TICK, "start", 120),
         _tline(c0 + 100, cy0 + 70, "船長", 28, sc("cap"), "middle", 120),
         _tline(400.0, 300.0, "カリフォルニアン号の時計", 28, sc("cf"), "start", 420),
         F.circ(SE["sky"][0], SE["sky"][1], 9, J.TICK)]
    return g


def section_stage(prev, st):
    s = []
    sx, sy = SE["sky"]
    if _on(prev, st, "two"):
        s.append(_burst(sx - 50, sy - 110, J.SUB, 26) + _burst(sx + 40, sy - 160, J.SUB, 26))
        s.append(_tline(sx, sy - 220, SE_V[0], 30, J.AMBER, "middle", 200))
        s.append(_tline(sx, sy + 56, f"機関室の乗組員が {SE_V[1]}発", 26, INK, "middle", 300))
    if _on(prev, st, "pipe"):
        p, by = SE["pipe"], SE["bridge"][2]
        s.append(_tline(SE["bridge"][1] + 40, by - 60, "二等航海士", 28, sc("mate"), "start", 260))
        s.append(_arrow(p + 34, by - 10, p + 34, SE["chart"][1] + 60, J.AMBER, 5, 20))
        s.append(_chip(p + 210, SE["chart"][1] + 100, f"白い信号弾 {SE_V[3]}発", J.AMBER, 28))
        s.append(_tline(400.0, 345.0, f"{SE_V[2]}（二等航海士の話）", 30, J.AMBER, "start", 460))
    return s


# ══════════════════════════════════════════════════════════
#  company（c623）＝正面の夜空：会社ごとの夜の合図の光（ホワイト・スター・ライン＝緑＝カルパチア号の船長の話＝T1 Q25394・書き起こし）と遭難の信号（白い星＝G1 p.54）
#  ほかの会社の合図の色は描かない（記録に無い＝「？」）
# ══════════════════════════════════════════════════════════
CO = dict(xs=(400.0, 740.0, 1080.0), y0=400.0, y1=680.0, w=280.0, dist=(1470.0, 400.0, 1730.0, 680.0))
CO_WS = ("ホワイト・スター・ライン", "OK")


def company_base(st0):
    return [F.rect(200.0, 320.0, 1560.0, 500.0, J.BG, J.LINE_DIM, 3, rx=20)]


def company_stage(prev, st):
    s = []
    if _on(prev, st, "what"):
        for x in CO["xs"]:
            s.append(F.rect(x - CO["w"] / 2, CO["y0"], CO["w"], CO["y1"] - CO["y0"], J.BG2, J.LINE, 3, rx=14))
        for x in CO["xs"][1:]:
            s.append(_qmark(x, (CO["y0"] + CO["y1"]) / 2, 56) + _tline(x, CO["y1"] - 24, "ほかの会社", 26, J.TICK, "middle", 220))
        s.append(_tline(740.0, 370.0, "会社ごとの夜の合図", 30, INK, "middle", 520))
    if _on(prev, st, "ws"):
        x = CO["xs"][0]
        s.append(_burst(x, 520.0, rc(CO_WS[1]), 50, 7))
        s.append(_tline(x, CO["y1"] - 52, CO_WS[0], 26, rc(CO_WS[1]), "middle", 260) + _tline(x, CO["y1"] - 20, "緑", 28, rc(CO_WS[1]), "middle", 80))
        s.append(_tline(x, CO["y1"] + 52, "（カルパチア号の船長の話）", 24, sc("cap"), "middle", 360))
    if _on(prev, st, "vs"):
        a, y0, b, y1 = CO["dist"]
        s.append(F.rect(a, y0, b - a, y1 - y0, J.BG2, J.ALERT, 4, rx=14) + _tline((a + b) / 2, y0 + 44, "遭難の信号", 28, J.ALERT, "middle", 240))
        s.append(_burst((a + b) / 2 - 40, 540.0, J.SUB, 34) + _burst((a + b) / 2 + 50, 600.0, J.SUB, 30))
        s.append(_tline((a + b) / 2, y1 - 24, "白い星", 26, INK, "middle", 160))
        s.append(F.rect(250.0, CO["y0"] - 16, 980.0, CO["y1"] - CO["y0"] + 32, "none", J.AMBER, 4, rx=18, dash="14 10"))
    return s


# ══════════════════════════════════════════════════════════
#  height（c626）＝横から：その船のマストの灯の高さと、信号弾の高さ＝その半分くらい（二等航海士の話＝T1 Q7921・書き起こし）→
#  「低い光」は1992年の調べ直しで論点になった（G2 p.13＝結論は言い切らない）
# ══════════════════════════════════════════════════════════
HT = dict(x0=720.0, x1=1240.0, yw=740.0, h=40.0, mast=170.0)
HT_RATIO = 0.5


def ht_mast():
    return HT["x0"] + (HT["x1"] - HT["x0"]) * 0.88, HT["yw"] - HT["h"] - HT["mast"]


def ht_burst_y():
    return HT["yw"] - (HT["yw"] - ht_mast()[1]) * HT_RATIO


def height_base(st0):
    x0, x1, yw, h = HT["x0"], HT["x1"], HT["yw"], HT["h"]
    mx, my = ht_mast()
    g = [F.line(200.0, yw, 1760.0, yw, J.LINE_DIM, 3), F.poly(_hull_side(x0, x1, yw, h), J.BG2, J.LINE, 4, close=True),
         F.rect(x0 + 160, yw - h - 26, 220, 26, J.BG2, J.LINE, 3), F.line(mx, yw - h, mx, my, J.LINE, 3), _lamp(mx, my, J.SUB, 10),
         _tline((x0 + x1) / 2, yw + 46, "その船（遠く）", 26, J.TICK, "middle", 260)]
    xb = x0 - 70
    g.append(F.poly([(xb + 14, yw), (xb, yw), (xb, my), (xb + 14, my)], "none", J.SUB, 4))
    g.append(_tline(xb - 18, (yw + my) / 2 + 10, "マストの灯の高さ", 28, INK, "end", 360))
    return g


def height_stage(prev, st):
    s = []
    yb = ht_burst_y()
    if _on(prev, st, "half"):
        cx = (HT["x0"] + HT["x1"]) / 2 + 20
        s.append(_burst(cx, yb, J.SUB, 30))
        xb = HT["x1"] + 70
        s.append(F.poly([(xb - 14, HT["yw"]), (xb, HT["yw"]), (xb, yb), (xb - 14, yb)], "none", J.AMBER, 4))
        s.append(_tline(xb + 20, (HT["yw"] + yb) / 2 - 2, "その半分くらい", 30, J.AMBER, "start", 300))
        s.append(_tline(xb + 20, (HT["yw"] + yb) / 2 + 36, "（二等航海士の話）", 24, sc("mate"), "start", 300))
    if _on(prev, st, "topic"):
        s.append(_chip(960.0, 420.0, "低い光", J.AMBER, 34))
        s.append(_chip(1440.0, 380.0, "1992年の調べ直しの論点", sc("maib"), 28))
    return s


# ══════════════════════════════════════════════════════════
#  memory2（c634）＝正面の2列：二等航海士の話（1:10ごろ・白い信号弾 5発）／船長の記憶（1:15ごろ・白い信号弾 1発だけ）＝カリフォルニアン号の時計（G1 p.58〜59）
# ══════════════════════════════════════════════════════════
MM = dict(l=(260.0, 860.0), r=(1060.0, 1660.0), y0=390.0, y1=800.0)
MM_V = (("mate", "二等航海士の話", "1:10ごろ", 5), ("cap", "船長の記憶", "1:15ごろ", 1))


def _mm_col(i, part):
    key, head, t, n = MM_V[i]
    a, b = MM["l"] if i == 0 else MM["r"]
    cx, c = (a + b) / 2, sc(key)
    if part == "head":
        return (F.rect(a, MM["y0"], b - a, MM["y1"] - MM["y0"], J.BG2, c, 4, rx=16) + _tline(cx, MM["y0"] + 50, head, 30, c, "middle", 400)
                + _tline(cx, 560.0, t, 60, INK, "middle", 420))
    g = [_burst(cx + (k - (n - 1) / 2) * 92, 660.0, J.SUB, 30) for k in range(n)]
    g.append(_tline(cx, 760.0, f"白い信号弾 {n}発" + ("だけ" if n == 1 else ""), 30, INK, "middle", 400))
    return "".join(g)


def memory2_base(st0):
    return [_tline(960.0, 350.0, "カリフォルニアン号の時計", 28, sc("cf"), "middle", 420)]


def memory2_stage(prev, st):
    s = []
    if _on(prev, st, "l"):
        s += [_mm_col(0, "head"), _mm_col(0, "n")]
    if _on(prev, st, "r"):
        s.append(_mm_col(1, "head") + _neq(960.0, 590.0))
    if _on(prev, st, "one"):
        s.append(_mm_col(1, "n"))
    return s


# ══════════════════════════════════════════════════════════
#  cfband（c637）＝時間の線（縦・橙）＝カリフォルニアン号の時計だけ（G1 p.56〜59）：22:20ごろ 止まる・23:40 灯が消える（三等航海士）・
#  1:10ごろ 白い信号弾5つ（二等航海士）・2:05 全部で8つ（見習い）・2:40ごろ 見えなくなる（二等航海士）→ 23:30 から朝まで眠る通信士の帯（G1 p.57・p.59）
#  縦は時刻に比例（1分＝1.733画素）。タイタニック号の時刻は並べない（c416 の横の青い帯と色と並びを替えた）
# ══════════════════════════════════════════════════════════
CB = dict(x=620.0, w=40.0, y0=300.0, y1=820.0, t0=22 * 60, t1=27 * 60, sleep=1300.0)
CB_EV = (("22:20ごろ", "止まる（氷原の手前）"), ("23:40", "灯が消える（三等航海士の話）"), ("1:10ごろ", "白い信号弾5つ（二等航海士の話）"),
         ("2:05", "全部で8つ（見習いの話）"), ("2:40ごろ", "見えなくなる（二等航海士の話）"))
CB_SLEEP = "23:30"


def cb_y(t):
    return CB["y0"] + (_min(t) - CB["t0"]) * (CB["y1"] - CB["y0"]) / (CB["t1"] - CB["t0"])


def cfband_base(st0):
    x, w = CB["x"], CB["w"]
    return [F.rect(x - w / 2, CB["y0"], w, CB["y1"] - CB["y0"], sc("cf"), None, None, rx=10, op=0.55),
            _tline(1740.0, 360.0, "カリフォルニアン号の船内の時計", 30, sc("cf"), "end", 560)]


def cfband_stage(prev, st):
    s = []
    x, w = CB["x"], CB["w"]
    if _on(prev, st, "ev"):
        for t, lab in CB_EV:
            y = cb_y(t)
            s.append(F.line(x - w / 2 - 14, y, x + w / 2 + 14, y, INK, 4) + _tline(x - w / 2 - 26, y + 11, t, 30, J.AMBER, "end", 220)
                     + _tline(x + w / 2 + 30, y + 11, lab, 28, INK, "start", 560))
    if _on(prev, st, "sleep"):
        xs, ya = CB["sleep"], cb_y(CB_SLEEP)
        s.append(F.rect(xs - 18, ya, 36, CB["y1"] - ya, J.LINE_DIM, None, None, rx=8) + _arrow(xs, CB["y1"] - 10, xs, CB["y1"] + 40, J.LINE, 5, 20))
        s.append(_tline(xs - 32, ya + 11, CB_SLEEP, 28, J.AMBER, "end", 120))
        s.append(_tline(xs + 40, ya + 140, "通信士は眠っていた", 30, INK, "start", 420))
        s.append(_tline(xs + 40, CB["y1"] + 20, "朝、起こされる", 28, INK, "start", 300))
    return s


# ══════════════════════════════════════════════════════════
#  swap（c639）＝横から：前に見えていた船（点線）と、4:00ごろ新しく見えた船（マストの白い灯2つ）→ 船長は信号弾の船と見たらしい・
#  「大丈夫そうだ」→ 取り違えは正されないまま（G1 p.59）
# ══════════════════════════════════════════════════════════
SW = dict(old=(260.0, 700.0), new=(1080.0, 1600.0), yw=720.0)
SW_V = ("4:00ごろ", 2)


def swap_base(st0):
    yw = SW["yw"]
    o0, o1 = SW["old"]
    n0, n1 = SW["new"]
    g = [F.rect(200.0, 320.0, 1560.0, yw - 320.0, J.BG2, None, None, rx=16, op=0.5), F.line(200.0, yw, 1760.0, yw, J.LINE_DIM, 3),
         _ship_side(o0, o1, yw, J.TICK, dash="10 8"), _tline((o0 + o1) / 2, yw + 50, "前に見えていた船", 28, J.TICK, "middle", 300),
         _ship_side(n0, n1, yw, J.LINE)]
    for x, y in _mast_tops(n0, n1, yw):
        g.append(_lamp(x, y, J.SUB, 11))
    g.append(_tline((n0 + n1) / 2, yw + 50, "新しく見えた船（マストの白い灯 2つ）", 28, INK, "middle", 560))
    g.append(_clk((n0 + n1) / 2, yw + 92, SW_V[0], "cf", 26, mw=560))
    return g


def swap_stage(prev, st):
    s = []
    if _on(prev, st, "think"):
        pts = _arcpts(890.0, 620.0, 300.0, 120.0, -20, -160, 12)
        s.append(F.poly(pts[:-1], "none", J.AMBER, 5) + _arrow(pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], J.AMBER, 5, 22))
        s.append(_tline(890.0, 470.0, "信号弾の船と見たらしい", 30, J.AMBER, "middle", 420))
    if _on(prev, st, "said"):
        s.append(_say(1340.0, 400.0, "cap", "大丈夫そうだ"))
        s.append(_xmark(890.0, 540.0, 22, J.ALERT, 8) + _tline(890.0, 600.0, "正されないまま", 28, J.ALERT, "middle", 300))
    if _on(prev, st, "q"):
        s.append(_qmark(560.0, 420.0, 80))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表（mech25 と同じ作り）
# ══════════════════════════════════════════════════════════
def _v(lab, fields, base, stage, parts=None):
    d = dict(lab=lab, fields={f_: ONOFF for f_ in fields}, base=base, stage=stage)
    if parts:
        d["parts"] = parts
    return d


VIEWS = dict(
    tons2=_v("横から見た2本の棒（総トン数）", ("tt", "cf"), tons2_base, tons2_stage),
    people4=_v("横から見た縦の棒（人数）", ("q", "bars", "kids"), people4_base, people4_stage),
    boats20=_v("上から見たボートの並び", ("big", "fold"), boats20_base, boats20_stage),
    track3=_v("横から見た1本の帯（人数）", ("rule", "num"), track3_base, track3_stage),
    table1894=_v("正面から見た規則の表の段", ("q", "t94", "flat"), table1894_base, table1894_stage),
    radio3=_v("横から見た海の上の船と電波", ("none", "deaf"), radio3_base, radio3_stage),
    clocks2=_v("正面から見た2隻の時計", ("clk", "noon"), clocks2_base, clocks2_stage, clocks2_parts),
    aside=_v("横から見た知らせの道すじ", ("aside", "nope"), aside_base, aside_stage),
    busy=_v("横から見た無線室", ("ice", "busy"), busy_base, busy_stage),
    cf_side=_v("横から見た船の形", ("co", "empty"), cf_side_base, cf_side_stage),
    relay3=_v("上から見た3隻と電波", ("hear", "reply"), relay3_base, relay3_stage),
    drown=_v("横から見た強い電波と弱い電波", ("talk", "loud"), drown_base, drown_stage),
    watch=_v("横から見た船橋と見張り台", ("hand", "ice"), watch_base, watch_stage),
    helm=_v("上から見た船首の向き", ("order", "turn"), helm_base, helm_stage, helm_parts),
    olympic=_v("上から見た回る道のり", ("q", "test", "path"), olympic_base, olympic_stage),
    damage=_v("横から見た傷の範囲と区画", ("dmg", "sec"), damage_base, damage_stage),
    tray=_v("横から見た仕切りの並び", ("q", "one", "five"), tray_base, tray_stage, tray_parts),
    ttband=_v("時間の線（横）", ("boat", "radio"), ttband_base, ttband_stage),
    cqd=_v("正面から見たモールスの点と線", ("q", "code", "out"), cqd_base, cqd_stage),
    carp=_v("上から見た向かい方", ("get", "turn"), carp_base, carp_stage, carp_parts),
    rockets_n=_v("正面から見た2つの数の札", ("q", "rep", "say"), rockets_n_base, rockets_n_stage),
    colors=_v("正面から見た夜空の光", ("q", "any", "white"), colors_base, colors_stage),
    field=_v("上から見た氷原の手前", ("stop", "ice"), field_base, field_stage, field_parts),
    drift=_v("上から見た2つの位置", ("pts", "dist", "cur"), drift_base, drift_stage),
    sidelights=_v("上から見た船の灯", ("green", "two", "seen"), sidelights_base, sidelights_stage),
    masts2=_v("正面から見た2隻の灯", ("who", "two"), masts2_base, masts2_stage),
    morse=_v("正面から見た灯の点と線", ("call",), morse_base, morse_stage),
    views2=_v("横から見た灯りの列と2つの札", ("a", "b", "diff"), views2_base, views2_stage, views2_parts),
    watches=_v("時間の線（当直）", ("out", "bell"), watches_base, watches_stage),
    bearing=_v("上から見た羅針盤の目盛り", ("watch", "mean"), bearing_base, bearing_stage),
    flicker=_v("正面から見た2本の光の帯", ("think", "fix"), flicker_base, flicker_stage),
    section=_v("横から見た前の断面", ("two", "pipe"), section_base, section_stage),
    company=_v("正面から見た夜の合図の光", ("what", "ws", "vs"), company_base, company_stage),
    height=_v("横から見た光の高さ", ("half", "topic"), height_base, height_stage),
    memory2=_v("正面から見た2つの記憶", ("l", "r", "one"), memory2_base, memory2_stage),
    cfband=_v("時間の線（縦）", ("ev", "sleep"), cfband_base, cfband_stage),
    swap=_v("横から見た2隻の船", ("think", "said", "q"), swap_base, swap_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
# 値に比例・原文の値の写し（左上に「模式」を付けない）
NOT_SCHEMATIC = ("tons2", "people4", "track3", "ttband", "rockets_n", "watches", "memory2", "cfband")


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
                raise ValueError(f"m26：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m26：{f_}={v!r} は知らない値（{fields[f_]}）")
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
    for _st, stt in zip(steps, states):
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


def m26(view, steps, start=None, rel=(), note="", src=""):
    """26本目の図解。view は VIEWS の見え方。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m26：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view not in NOT_SCHEMATIC and "模式" not in note:
        raise ValueError("m26：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    seq = [st0] + states
    per = [parts_of(view, s) for s in seq]
    for p in per[0]:
        if not isinstance(p.get("w", 4), (int, float)):
            raise ValueError(f"m26：{view} の部品 {p.get('id')} の線の太さ w={p.get('w')!r}（数で書く・線なしでも 2 など）")
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
    body = "".join(g[:-2]) + "".join(stages)
    f.mech = dict(kind="m26", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=shapes, lab=lab, note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states), texts_all=svg_texts(body))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M26）
# ══════════════════════════════════════════════════════════
# 見え方ごとに、画面に出る「どの船か・誰の話か」の鍵（同じ画面で色が重ならないか＝門番）
VIEW_SRC = dict(tons2=("tt", "cf"), track3=("tt",), table1894=("tt",), radio3=("cr",), aside=("tt", "am", "cr", "rep"), busy=("tt", "cr", "rep"),
                cf_side=("cf",), relay3=("cf", "an", "tt"), drown=("cr", "tt", "cf", "rep"), watch=("tt",), helm=("tt",), olympic=("tt", "ol"),
                damage=("tt",), tray=("tt",), ttband=("tt",), cqd=("tt", "cr"), carp=("cp", "tt"), rockets_n=("rep", "mate"), colors=("tt",),
                field=("cf",), drift=("tt", "cf", "cr"), sidelights=("cap", "cf"), masts2=("mate", "cap"), morse=("cap",), views2=("cap", "mate"),
                watches=("cf", "mate"), bearing=("cf", "cap"), flicker=("mate",), section=("cf", "cap", "mate"), company=("cap",),
                height=("mate", "maib"), memory2=("mate", "cap", "cf"), cfband=("cf",), swap=("cf", "cap"))


def _lit(view, st):
    return [p for p in parts_of(view, st) if p.get("alpha", 1.0) > 0.5]


def _geo(view, allst):
    last = allst[-1]
    if view == "tons2":
        return dict(val=(tuple((k, v) for k, v, _l in TN_V), TN_TIMES, int(TN_V[0][1] // TN_V[1][1])),
                    px=tuple(tn_end(v) for _k, v, _l in TN_V), lins=((TN["x0"], TN["k"], 0.0),) * 2)
    if view == "people4":
        vs = tuple(v for _n, v, _c in PP_ROWS) + (PP_KIDS[0],)
        return dict(val=(tuple((n, v) for n, v, _c in PP_ROWS), PP_PASS, PP_ALL, PP_KIDS,
                         sum(v for _n, v, _c in PP_ROWS[:3]) == PP_PASS, PP_PASS + PP_ROWS[3][1] == PP_ALL, sum(PP_KIDS[1]) == PP_KIDS[0]),
                    px=tuple(pp_top(v) for v in vs), lins=((PP["y0"], -PP["k"], 0.0),) * len(vs))
    if view == "boats20":
        return dict(val=(tuple((n, cap, k) for n, cap, k, _c in BT_ROWS), BT_SEATS, sum(cap * k for _n, cap, k, _c in BT_ROWS) == BT_SEATS),
                    px=tuple(bt_len(cap) for _n, cap, _k, _c in BT_ROWS), lins=((0.0, BT["k"], 0.0),) * 3)
    if view == "track3":
        k = (TK["x1"] - TK["x0"]) / TK_V[0]
        return dict(val=TK_V, px=tuple(tk_x(v) for v in TK_V), lins=((TK["x0"], k, 0.0),) * 3)
    if view == "table1894":
        return dict(val=TB_V, px=(tb_x(TB_V[1]), tb_x(TB_V[2])), lins=((TB["x0"], TB["k"], 0.0),) * 2)
    if view == "clocks2":
        return dict(val=tuple(round(float(p.get("rot", 0.0)), 3) for p in parts_of("clocks2", last)))
    if view == "busy":
        return dict(val=(BS_T,))
    if view == "cf_side":
        return dict(val=CS_V)
    if view == "drown":
        return dict(val=(520.0 > 110.0,))
    if view == "watch":
        return dict(val=(WT_T,))
    if view == "helm":
        return dict(val=(round(float(parts_of("helm", last)[0]["rot"]), 3),))
    if view == "olympic":
        _p, L = ol_path()
        return dict(val=(OL_V, OL_TURN), px=(L, ol_ship_len()), lins=((0.0, OL["k"], 0.0),) * 2)
    if view == "damage":
        return dict(val=(DM_V, DM_COMP), px=(DM["x1"] - dm_xd(), DM["x1"] - DM["x0"]), lins=((0.0, dm_k(), 0.0),) * 2)
    if view == "tray":
        lit = [int(p["id"][1:]) for p in _lit("tray", last) if p["pts"][0][1] <= TR["wall"] + 0.5]
        return dict(val=(len(lit), lit == list(range(TR["n"] - len(lit), TR["n"]))))
    if view == "ttband":
        return dict(val=tuple((t, lab) for t, lab, _s, _k in TT_EV), px=tuple(tt_x(t) for t, *_r in TT_EV),
                    lins=((TT["x0"], (TT["x1"] - TT["x0"]) / (TT["t1"] - TT["t0"]), TT["t0"]),) * len(TT_EV), mins=tuple(_min(t) for t, *_r in TT_EV))
    if view == "cqd":
        return dict(val=(CQ_CODE, CQ_T))
    if view == "carp":
        return dict(val=(CP_V, round(float(parts_of("carp", last)[0]["rot"]), 3)))
    if view == "rockets_n":
        return dict(val=RN_V)
    if view == "colors":
        return dict(val=(rc(CL_TT).lower(), len(set(rc(c).lower() for c in CL_ROW)) == len(CL_ROW)))
    if view == "field":
        return dict(val=(FD_T, FD["x_stop"] < FD["x_from"]))
    if view == "drift":
        bx, by = df_b()
        ax, ay = DF["a"]
        return dict(val=(DF_V, round(math.degrees(math.atan2(bx - ax, ay - by)), 2), DF_CUR))
    if view == "sidelights":
        return dict(val=(SL_SIDE, sl_lamp("right")[0] > SL["cx"], sl_lamp("left")[0] < SL["cx"], SL_V,
                         tuple(LIGHT[SL_SIDE[k]].lower() for k in ("right", "left", "mast"))))
    if view == "masts2":
        return dict(val=(MS_V, len(ms_lights_b()), ms_lights_b()[0][1] < ms_lights_b()[1][1]))
    if view == "views2":
        return dict(val=(VW_SAY, all(p.get("alpha", 1.0) < 0.5 for p in parts_of("views2", last))))
    if view == "watches":
        ts = (WW_BLK[0][3], WW_BLK[1][3], WW_EV)
        return dict(val=(tuple((n, w) for n, w, _a, _b in WW_BLK), WW_EV), px=tuple(ww_x(t) for t in ts),
                    lins=((WW["x0"], (WW["x1"] - WW["x0"]) / (WW["t1"] - WW["t0"]), WW["t0"]),) * len(ts), mins=tuple(_min(t) + (24 * 60 if _min(t) < WW["t0"] else 0) for t in ts))
    if view == "section":
        return dict(val=SE_V)
    if view == "company":
        return dict(val=(CO_WS[0], rc(CO_WS[1]).lower()))
    if view == "height":
        mx, my = ht_mast()
        return dict(val=(round((HT["yw"] - ht_burst_y()) / (HT["yw"] - my), 3),))
    if view == "memory2":
        return dict(val=tuple((k, t, n) for k, _h, t, n in MM_V))
    if view == "cfband":
        ts = tuple(t for t, _l in CB_EV) + (CB_SLEEP,)
        return dict(val=CB_EV + (CB_SLEEP,), px=tuple(cb_y(t) for t in ts),
                    lins=((CB["y0"], (CB["y1"] - CB["y0"]) / (CB["t1"] - CB["t0"]), CB["t0"]),) * len(ts), mins=tuple(_min(t) for t in ts))
    if view == "swap":
        return dict(val=SW_V)
    return {}


def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst], src={k: tuple(v) for k, v in SRC.items()}, vsrc=tuple(VIEW_SRC.get(view, ())),
               light={k: v.lower() for k, v in LIGHT.items()})
    out.update(_geo(view, allst))
    return out
