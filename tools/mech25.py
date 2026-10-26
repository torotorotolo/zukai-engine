# -*- coding: utf-8 -*-
"""mech25.py — 25本目（JR福知山線脱線事故・2005-04-25）「図解」（2026-10-26 新設・⑤b-5＝第1〜4章の42カット）。

■ 何か
  24本目 `mech24` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。再現イラストではない＝「再現」の札は出さない。
  左上に見え方の名（模式の見え方は末尾に「・模式」）・左下に注（模式の見え方は「模式」）と出典。
  🔴 人の形・顔・手は描かない（運転士・車掌・指令員・社長〈当時〉は役職だけ＝台本 §1-4）。事故の瞬間（脱線・転覆）は描かない。
  🔴 **色は出どころの色**（誰の言葉・どの資料の数か＝台本の帰属の呼び分け）：
     報告書（2007年）＝青 state／建議（2005年）＝桃 bldg_a／車掌（口述・無線）＝橙 company（付図24 の車掌の帯と同じ系統）／
     指令員（総合指令所の輸送指令員）＝緑 ward（付図24 の指令員の帯と同じ系統）／国会（社長〈当時〉）＝紫 city／
     消防庁・兵庫県＝水色 ship（同じ画面に2つを出さない）／JR西日本（会社）＝茶 DOC。
     意味の色＝赤 ALERT（行き過ぎ・遅れ・危ない）・黄 AMBER（数・時刻・言い方の強さの目盛り）。新しい色の値は足していない（ROLE と J の名で引く）。
  🔴 **言い方の強さの目盛り**（4つの升＝R1 p.264 の言葉の決まり）：認められる 4・推定される 3・考えられる 2・可能性が考えられる 1
     （「可能性も考えられる」も 1・「低いものと考えられる」は「考えられる」の 2）。表 LV＝門番 check_mech の REC_M25 が別に持つ。
  🔴 割れる時刻と数は台本 §1-5 の値だけ（猪名寺 9:17:38 は報告書・行き過ぎは出どころの名つき・伊丹の遅れ 着 約1分08秒／発 約1分20秒／「1分半」）。
     R1 p.222 の「低いものと考えられる」は「この曲線を、わざと110km/hほどで通ろうとした可能性」だけに当てる（「わざと速度を出した」全体に広げない）。
     日勤教育の3件は日数と年月だけ（理由の中身は台本 §1-4・§5 で言わない＝画面にも出さない）。

■ 見え方（view）＝映像方針の一覧 `ref/ep25/eizou_list25.md` の「見た目の型」（第1〜4章の図解 42カット＝案C 7・地図 c517 は別）
  第1章  route（c201 路線）・tt_col（c205 縦の時刻表）・delay_bars（c211 縦の棒）・speedo（c212 弧の速度計と記録の札）・overrun（c215 72m と 3m）・
         two_cabs（c218 7両と合図）・glass（c220 受話器とガラス）・ruler_v（c223 縦の物差し）・ring2（c225 2つの弧の時計）・
         tags4（c226 4つの値札）・matrix（c227 出どころの表）
  第2章  hscale（c302 横の速度の目盛り）・tt_band（c308 交信の横の帯）・zone（c311 区間の帯と復唱）・clockfan（c312 秒針の扇）・
         crossing（c316 無い踏切）・two_ribbons（c325 右でそろう2本の帯）・tiles（c326 1マス1秒）・clues（c329 2つの手がかり）
  第3章  section（c407 後ろから見た断面）・plaques（c412 2つの数の板）・split_box（c415 分けた箱）・chapters3（c418 3つの箱）・doors3（c420 3つの入口）
  第4章  stairs4（c502 4段の階段）・persp（c503 運転席の高さから見た曲線）・two_cards（c505 2つの「こと」）・flow3（c507 縦の流れ）・
         fan5（c510 5つの見出しの札）・two_brakes（c511 2本のはしご）・band25（c512 2本のピンと約25秒）・survey（c514 アンケートの板）・
         cab_note（c516 運転台の線画と付箋）・two_signals（c518 2つの合図）・two_scenes（c521 2つのコマ）・weaker（c523 強さの縦の目盛り）・
         objects（c525 赤鉛筆と手袋）・cycle（c527 輪の流れ）・cal18（c528 3枚の暦）・lens（c529 虫めがね）・qcards（c530 2つの口述）・
         evidence（c531 根拠の線）
  🔴 同じ型は全編で2回まで・続けない（台本 §7）：時刻表 c205（縦の列）↔c308（横の帯）・時計 c225（2つの弧）↔c312（秒針の扇）・
     札 c226（紐の値札）↔c510（見出しの札）・比べ c227（表）↔c530（2つの口述）・並べ c325（右でそろう帯）↔c412（2つの板）・
     箱 c415（分けた箱）↔c502（階段）。相方が ⑤b-6 の型（棒 c211↔c609・流れ c507↔c807・暦 c528↔c801）は ⑤b-6 で別の絵に。
     案C の絵（F1 線路の略図・F2 取っ手と秒の帯・F3 交信の欄と吹き出し・F4 速さと距離・F5 曲線の重ね・F6 宝塚の略図）とも別の絵

■ SPEC の書き方（mech24 と同じ）
  fig=("m25", dict(view=…, start=dict(…), steps=[dict(state=dict(…)), …], rel=[dict(t="5418M", src="R1 p5")], note="…", src=ss.src([…])))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。🔴 画面の字の数（時刻・数・年）は全部 `rel=` に同じ文字列で宣言する
  （門番 check_mech の judge_m25 が基図と段の層の全部の字から数を拾って照らす）。
  🔴 記録の値（出どころの名と色・駅の順・時刻・値・強さの言葉と段・札の言葉）は門番の側 REC_M25 が別に持つ（§5b-88）。描く側の表を書き換えると鳴る。
"""
from __future__ import annotations

import math
import re

import jiko_style as J
import titan_fig as F
from mech21 import _P, _arrow, _check, _on, _qmark, _xmark
from mech24 import _arcpts, _tline, _w, rc

ONOFF = ("off", "on")
INK = J.INK_W
CX = 960.0
TRAIN = "#dfe6ea"                 # 列車の印（白に近い灰＝案C の train と同じ明るさ）

# 出どころの色（名・ROLE か J の名）。fd と hy は同じ色＝同じ画面に出さない（門番が見る）
SRC = dict(
    rep=("報告書", "state"),          # 鉄道事故調査報告書 RA2007-3（2007年6月・航空・鉄道事故調査委員会）
    ken=("建議", "bldg_a"),           # 建議（2005年9月・同じ委員会）
    sha=("車掌", "company"),          # 7両目の車掌（口述・列車無線）
    shi=("指令員", "ward"),           # 総合指令所の輸送指令員
    kok=("国会", "city"),             # 国会会議録（社長〈当時〉の答弁）
    fd=("消防庁", "ship"),            # 消防庁 第32報（2005年5月24日）
    hy=("兵庫県", "ship"),            # 兵庫県 福知山線列車事故検証報告書（2006年1月）
    jr=("JR西日本", "DOC"),           # JR西日本（同社の頁・会社の説明）
)

# 言い方の強さ（R1 p.264 の言葉の決まり＝4つの升の数）
LV = {"認められる": 4, "推定される": 3, "考えられる": 2, "可能性が考えられる": 1, "可能性も考えられる": 1, "低いものと考えられる": 2}
METER_W = 4 * 24.0 + 3 * 6.0


def sc(key):
    return rc(SRC[key][1])


def _meter(x, y, word, s=24.0, gap=6.0):
    """言い方の強さの目盛り（左の端 x・真ん中の高さ y）。升の数は表 LV の word の段。"""
    lv = LV[word]
    g = []
    for i in range(4):
        on = i < lv
        g.append(F.rect(x + i * (s + gap), y - s / 2, s, s, J.AMBER if on else J.BG2, J.AMBER if on else J.LINE_DIM, 3, rx=4))
    return "".join(g)


def _chip(cx, cy, t, col=None, cap=28, ink=None, w=None, h=None, sw=4, dash=None):
    col = col or J.LINE
    w = w or _w(t, cap) + 48
    h = h or cap + 26
    return (F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, sw, rx=min(h / 2, 14), dash=dash)
            + _tline(cx, cy + cap * 0.36, t, cap, ink or col, "middle", w - 24))


def _big(x, y, t, cap=80, col=None, anchor="middle"):
    return F.txt(x, y, t, cap, col or INK, "Dela", anchor)


def _bracket(x0, x1, y, col, sw=4, up=True, tick=14):
    d = -tick if up else tick
    return F.poly([(x0, y + d), (x0, y), (x1, y), (x1, y + d)], "none", col, sw)


def _phone(cx, cy, s=1.0, col=None):
    """受話器の印（耳と口の丸と柄）。"""
    c = col or INK
    return (F.line(cx - 30 * s, cy + 20 * s, cx + 30 * s, cy - 20 * s, c, 14 * s) + F.circ(cx - 36 * s, cy + 24 * s, 15 * s, c, None)
            + F.circ(cx + 36 * s, cy - 24 * s, 15 * s, c, None))


def _waves(cx, cy, r0, n, col, a0=-40.0, a1=40.0, step=18.0, sw=5):
    """音・電波の弧（右向き＝a0〜a1 度）。"""
    return "".join(F.poly(_arcpts(cx, cy, r0 + i * step, r0 + i * step, a0, a1, 10), "none", col, sw) for i in range(n))


def _radio(cx, cy, s=1.0, col=None):
    c = col or INK
    return (F.rect(cx - 26 * s, cy - 18 * s, 52 * s, 54 * s, J.BG2, c, 5, rx=8) + F.line(cx + 14 * s, cy - 18 * s, cx + 26 * s, cy - 60 * s, c, 5)
            + F.circ(cx, cy + 10 * s, 9 * s, c, None) + _waves(cx + 26 * s, cy - 60 * s, 14 * s, 2, c, -60, 20, 14 * s, 4))


def _speaker(cx, cy, s=1.0, col=None):
    c = col or INK
    p = [(cx - 30 * s, cy - 14 * s), (cx - 12 * s, cy - 14 * s), (cx + 10 * s, cy - 32 * s), (cx + 10 * s, cy + 32 * s),
         (cx - 12 * s, cy + 14 * s), (cx - 30 * s, cy + 14 * s)]
    return F.poly(p, c, None, close=True) + _waves(cx + 14 * s, cy, 18 * s, 2, c, -45, 45, 16 * s, 5)


def _bell(cx, cy, s=1.0, col=None):
    c = col or J.AMBER
    p = [(cx - 26 * s, cy + 18 * s), (cx - 20 * s, cy - 10 * s), (cx - 10 * s, cy - 24 * s), (cx, cy - 28 * s), (cx + 10 * s, cy - 24 * s),
         (cx + 20 * s, cy - 10 * s), (cx + 26 * s, cy + 18 * s)]
    return F.poly(p, c, None, close=True) + F.circ(cx, cy + 24 * s, 7 * s, c, None)


def _buzzer(cx, cy, s=1.0, col=None):
    c = col or J.AMBER
    return (F.circ(cx, cy, 24 * s, J.BG2, c, 6) + F.circ(cx, cy, 9 * s, c, None) + _waves(cx, cy, 34 * s, 2, c, -40, 40, 14 * s, 4)
            + _waves(cx, cy, 34 * s, 2, c, 140, 220, 14 * s, 4))


def _train_block(x0, x1, y, h, col=None, nose=True):
    """横から（上から）見た列車の印（先頭が右）。人は描かない。"""
    c = col or TRAIN
    p = [(x0, y - h / 2), (x1 - (26 if nose else 0), y - h / 2), (x1, y - h / 2 + (14 if nose else 0)), (x1, y + h / 2), (x0, y + h / 2)]
    return F.poly(p, c, J.BG, 3, close=True)


def _rails(x0, x1, y, gap=28.0, sleeper=46.0):
    g = []
    x = x0 + 10
    while x < x1:
        g.append(F.line(x, y - gap / 2 - 8, x, y + gap / 2 + 8, J.LINE_DIM, 6))
        x += sleeper
    return "".join(g) + F.line(x0, y - gap / 2, x1, y - gap / 2, J.LINE, 5) + F.line(x0, y + gap / 2, x1, y + gap / 2, J.LINE, 5)


def _sector(cx, cy, r0, r1, a0, a1, fill, stroke=None, sw=None, op=None, n=12):
    p = _arcpts(cx, cy, r1, r1, a0, a1, n) + list(reversed(_arcpts(cx, cy, r0, r0, a0, a1, n)))
    return F.poly(p, fill, stroke, sw, close=True, op=op)


# ══════════════════════════════════════════════════════════
#  第1章
#  route（c201）＝宝塚から尼崎・JR東西線へ（駅の並び＝R1 p.5・付図27。駅の間隔は等しく描いた模式）
#  事故の曲線の印＝塚口と尼崎のあいだ（キロ程：塚口 2k872m・曲線の入口 1k949m・曲線の終わり 約1k6〈付図73〉＝塚口から尼崎へ およそ4割の所）
# ══════════════════════════════════════════════════════════
RT_ST = ("宝塚", "中山寺", "川西池田", "北伊丹", "伊丹", "猪名寺", "塚口", "尼崎")
RT = dict(y=540.0, x0=210.0, dx=185.0, tozai=1730.0, curve=0.37)
RT_NO = "5418M"


def rt_x(i):
    return RT["x0"] + RT["dx"] * i


def rt_curve_x():
    return rt_x(6) + RT["dx"] * RT["curve"]


def route_base(st0):
    y = RT["y"]
    g = [F.line(rt_x(0), y, rt_x(7), y, J.AMBER, 14), _tline(rt_x(2), y - 46, "JR福知山線", 26, J.AMBER, "middle", 260)]
    for i, n in enumerate(RT_ST):
        big = i in (0, 7)
        g.append(F.circ(rt_x(i), y, 20 if big else 13, J.BG, J.AMBER if big else INK, 6 if big else 5))
        g.append(_tline(rt_x(i), y + 66, n, 30 if big else 28, INK, "middle", 170))
    cx = rt_curve_x()
    g.append(F.poly(_arcpts(cx, y, 34, 20, 180, 360, 12), "none", J.ALERT, 10))
    g.append(F.line(cx, y - 32, cx, y - 64, J.ALERT, 4))
    g.append(_tline(cx, y - 76, "事故の曲線", 28, J.ALERT, "middle", 200))
    return g


def route_stage(prev, st):
    s = []
    y = RT["y"]
    pink = J.ROLE["bldg_a"]
    if _on(prev, st, "dir"):
        s.append(F.line(rt_x(7), y, RT["tozai"] - 30, y, pink, 14))
        s.append(_arrow(RT["tozai"] - 40, y, RT["tozai"] + 30, y, pink, 14, 40))
        s.append(_tline((rt_x(7) + RT["tozai"]) / 2 + 20, y - 46, "JR東西線へ", 26, pink, "middle", 220))
        s.append(_arrow(rt_x(0), y + 130, RT["tozai"], y + 130, J.ROLE["ship"], 7, 28))
        s.append(_tline(CX, y + 188, "上りの快速", 32, J.ROLE["ship"], "middle", 400))
    if _on(prev, st, "num"):
        s.append(F.rect(CX - 230, 290, 460, 110, J.BG2, J.AMBER, 5, rx=14))
        s.append(_tline(CX - 200, 358, "列車番号", 26, J.TICK, "start", 140))
        s.append(_big(CX + 70, 372, RT_NO, 62, INK))
    return s


# ══════════════════════════════════════════════════════════
#  tt_col（c205）＝その朝の動きの縦の時刻表（報告書の「ごろ」「前後」のまま・R1 p.10〜13）→ 3行目で宝塚の着に赤い枠
# ══════════════════════════════════════════════════════════
TT_ROWS = (("宝塚", "着", "8:56:14ごろ"), ("宝塚", "発", "9:04:00前後"), ("北伊丹", "通過", "9:13:39ごろ"), ("伊丹", "着", "9:15:43ごろ"),
           ("伊丹", "発", "9:16:10ごろ"), ("猪名寺", "通過", "9:17:38ごろ"), ("塚口", "通過", "9:18:22ごろ"), ("脱線", "", "9:18:54ごろ"))
TT = dict(y0=384.0, dy=62.0, xl=250.0, xs=430.0, xk=640.0, xt=820.0, xn=1300.0, x1=1660.0)


def tt_y(i):
    return TT["y0"] + TT["dy"] * i


def tt_col_base(st0):
    return [_tline(TT["xs"], 306, "駅", 26, J.TICK, "middle", 200), _tline(TT["xk"], 306, "着・発", 26, J.TICK, "middle", 200),
            _tline(TT["xt"], 306, "時刻（報告書）", 26, J.TICK, "start", 300),
            F.line(TT["xl"] + 30, 324, TT["x1"], 324, J.LINE_DIM, 3),
            F.line(TT["xl"], 344, TT["xl"], tt_y(7) - 4, J.LINE, 6)]


def tt_col_stage(prev, st):
    s = []
    if _on(prev, st, "rows"):
        for i, (n, k, t) in enumerate(TT_ROWS):
            y = tt_y(i)
            last = n == "脱線"
            dot = J.ALERT if last else (J.AMBER if n == "宝塚" else (J.ROLE["company"] if n == "伊丹" else J.LINE))
            s.append(F.circ(TT["xl"], y - 10, 12, J.BG, dot, 5))
            s.append(_tline(TT["xs"], y, n, 30, J.ALERT if last else INK, "middle", 220))
            if k:
                s.append(_tline(TT["xk"], y, k, 28, J.ROLE["ship"] if k == "通過" else J.TICK, "middle", 160))
            s.append(_tline(TT["xt"], y, t, 32, J.ALERT if last else J.AMBER, "start", 360))
    if _on(prev, st, "late"):
        y = tt_y(0)
        s.append(F.rect(TT["xl"] + 30, y - 44, TT["x1"] - TT["xl"] - 30, 60, "none", J.ALERT, 5, rx=12))
        s.append(_tline(TT["xn"], y, "ここで、もう遅れ", 30, J.ALERT, "start", 330))
    return s


# ══════════════════════════════════════════════════════════
#  delay_bars（c211）＝駅ごとの遅れの縦の棒（高さは秒に比例・R1 p.11 の「程度」「約」のまま）。北伊丹は通過＝横縞
# ══════════════════════════════════════════════════════════
DB_ROWS = (("宝塚", "発", 15, "15秒程度", "AMBER"), ("中山寺", "発", 25, "25秒程度", "company"), ("川西池田", "発", 35, "35秒程度", "ALERT"),
           ("北伊丹", "通過", 34, "約34秒", "ship"))
DB = dict(y0=760.0, k=11.0, xs=(420.0, 760.0, 1100.0, 1440.0), w=180.0)
DB_T = "9:13:39ごろ"


def db_top(v):
    return DB["y0"] - v * DB["k"]


def delay_bars_base(st0):
    g = [F.line(260.0, DB["y0"], 1640.0, DB["y0"], J.LINE, 5), _tline(260.0, 322.0, "定刻からの遅れ", 26, J.TICK, "start", 300)]
    for i, (n, k, _v, _l, _c) in enumerate(DB_ROWS):
        g.append(_tline(DB["xs"][i], DB["y0"] + 44, f"{n} {k}", 28, INK, "middle", 300))
    return g


def _db_bar(i):
    _n, k, v, lab, c = DB_ROWS[i]
    x, col, top = DB["xs"][i], rc(c), db_top(v)
    x0, w = x - DB["w"] / 2, DB["w"]
    if k == "通過":
        g = [F.rect(x0, top, w, DB["y0"] - top, J.BG2, col, 5, rx=6)]
        yy = top + 16
        while yy < DB["y0"] - 8:
            g.append(F.line(x0 + 8, yy, x0 + w - 8, yy, col, 6))
            yy += 20
    else:
        g = [F.rect(x0, top, w, DB["y0"] - top, col, None, None, rx=6)]
    g.append(_tline(x, top - 18, lab, 30, col, "middle", 260))
    return "".join(g)


def delay_bars_stage(prev, st):
    s = []
    if _on(prev, st, "b0"):
        s.append(_db_bar(0))
    if _on(prev, st, "b12"):
        s += [_db_bar(1), _db_bar(2)]
    if _on(prev, st, "b3"):
        s.append(_db_bar(3))
        s.append(_tline(DB["xs"][3], db_top(DB_ROWS[3][2]) - 64, DB_T, 30, J.AMBER, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  speedo（c212）＝1両目の速度計（弧の帯＋数字＝R1 p.86「円弧型バーグラフによるアナログ表示、数字によるデジタル表示」・最大150km/h）と
#  記録の札（報告書）。3行目で表示「120」（R1 p.11＝約122km/h のとき「120」が表示されていたものと見られる）
# ══════════════════════════════════════════════════════════
SP = dict(cx=600.0, cy=600.0, r=280.0, a0=150.0, a1=390.0, vmax=150.0, n=30, band=50.0)
SP_SHOW = 120
SP_REC = (("北伊丹駅を 約120km/h", "加速しながら通る"), ("約122km/h", "ここで加速をやめ、惰性へ"))
SP_CARD = dict(x0=1080.0, x1=1700.0, ys=(330.0, 500.0), h=130.0)


def sp_ang(v):
    return SP["a0"] + (SP["a1"] - SP["a0"]) * v / SP["vmax"]


def sp_lit():
    """表示の値まで点く升の数（升＝5km/h）。"""
    return int(round(SP_SHOW / SP["vmax"] * SP["n"]))


def _sp_segs(k, col):
    cx, cy, r = SP["cx"], SP["cy"], SP["r"]
    g = []
    for i in range(k):
        a0 = SP["a0"] + (SP["a1"] - SP["a0"]) * i / SP["n"] + 1.4
        a1 = SP["a0"] + (SP["a1"] - SP["a0"]) * (i + 1) / SP["n"] - 1.4
        g.append(_sector(cx, cy, r - SP["band"], r, a0, a1, col, None, None, n=3))
    return "".join(g)


def speedo_base(st0):
    cx, cy, r = SP["cx"], SP["cy"], SP["r"]
    g = [_sp_segs(SP["n"], "#22333f"), F.rect(cx - 130, cy - 64, 260, 128, J.BG2, J.LINE, 4, rx=12),
         _tline(cx, cy + 100, "km/h", 26, J.TICK, "middle", 120)]
    for v, lab in ((0, "0"), (150, "150")):
        a = math.radians(sp_ang(v))
        g.append(_tline(cx + (r + 36) * math.cos(a), cy + (r + 36) * math.sin(a) + 10, lab, 26, J.TICK, "middle", 100))
    g.append(_tline(cx, 818.0, "1両目の速度計（表示）", 26, J.TICK, "middle", 400))
    return g


def _sp_card(i):
    big, sub = SP_REC[i]
    x0, x1, y0, h = SP_CARD["x0"], SP_CARD["x1"], SP_CARD["ys"][i], SP_CARD["h"]
    col = sc("rep")
    return (F.rect(x0, y0, x1 - x0, h, J.BG2, col, 5, rx=12) + _tline(x0 + 24, y0 + 34, "記録（報告書）", 22, col, "start", 300)
            + _tline(x0 + 24, y0 + 80, big, 36, INK, "start", x1 - x0 - 48) + _tline(x0 + 24, y0 + 116, sub, 24, J.TICK, "start", x1 - x0 - 48))


def speedo_stage(prev, st):
    s = []
    if _on(prev, st, "rec1"):
        s.append(_sp_card(0))
    if _on(prev, st, "rec2"):
        s.append(_sp_card(1))
    if _on(prev, st, "show"):
        cx, cy = SP["cx"], SP["cy"]
        s.append(_sp_segs(sp_lit(), J.ROLE["ship"]))
        s.append(_big(cx, cy + 26, str(SP_SHOW), 72, J.ROLE["ship"]))
        y1 = SP_CARD["ys"][1] + SP_CARD["h"] / 2
        s.append(_arrow(cx + 134, cy, SP_CARD["x0"] - 14, y1, J.AMBER, 4, 18, dash="10 8"))
        s.append(_tline(1390.0, 712.0, "表示は、実際より少し低い", 30, J.AMBER, "middle", 560))
    return s


# ══════════════════════════════════════════════════════════
#  overrun（c215）＝伊丹駅の行き過ぎ（上から見た線路・止まるべき位置から約72m＝R1 p.12）→ 後ろへ戻して約3m 戻り過ぎ・9:15:43ごろ着。
#  長さは比例（1m＝10.5画素）・列車の印は1両目の前の部分だけ（模式）
# ══════════════════════════════════════════════════════════
OV = dict(y=600.0, stop=820.0, k=10.5, x_in=700.0, car=300.0, plat=(160.0, 900.0))
OV_OVER, OV_BACK = 72.0, 3.0
OV_T = "9:15:43ごろ"


def ov_xover():
    return OV["stop"] + OV_OVER * OV["k"]


def ov_xback():
    return OV["stop"] - OV_BACK * OV["k"]


def overrun_parts(st):
    y, x0 = OV["y"], OV["x_in"]
    dx = 0.0
    if st.get("back") == "on":
        dx = ov_xback() - x0
    elif st.get("over") == "on":
        dx = ov_xover() - x0
    pts = [(x0 - OV["car"], y - 26), (x0 - 28, y - 26), (x0, y - 10), (x0, y + 26), (x0 - OV["car"], y + 26)]
    return [_P("train", "poly", pts, fill=TRAIN, stroke=J.BG, w=3, dx=dx, alpha=1.0)]


def overrun_base(st0):
    y = OV["y"]
    p0, p1 = OV["plat"]
    return [_rails(120.0, 1760.0, y), F.rect(p0, 500.0, p1 - p0, 66.0, J.BG2, J.LINE, 4, rx=6),
            _tline((p0 + p1) / 2 - 60, 543.0, "伊丹駅のホーム", 26, J.TICK, "middle", 400),
            F.poly([(OV["stop"] - 14, 566.0), (OV["stop"] + 14, 566.0), (OV["stop"], 584.0)], J.AMBER, None, close=True),
            F.line(OV["stop"], 500.0, OV["stop"], 566.0, J.AMBER, 5),
            _tline(OV["stop"], 488.0, "止まるべき位置", 26, J.AMBER, "middle", 240)]


def overrun_stage(prev, st):
    s = []
    if _on(prev, st, "over"):
        xa, xb, yy = OV["stop"], ov_xover(), 690.0
        s.append(F.line(xa, yy - 30, xa, yy + 30, J.ALERT, 4) + F.line(xb, yy - 30, xb, yy + 30, J.ALERT, 4))
        s.append(_arrow(xa + 60, yy, xb, yy, J.ALERT, 5, 22) + _arrow(xb - 60, yy, xa, yy, J.ALERT, 5, 22))
        s.append(_tline((xa + xb) / 2, 748.0, "約72m 行き過ぎ", 34, J.ALERT, "middle", 420))
    if _on(prev, st, "back"):
        s.append(_arrow(ov_xover() - 16, 440.0, OV["stop"] + 30, 440.0, J.ROLE["ship"], 6, 24))
        s.append(_tline(1200.0, 422.0, "後ろへ戻す", 26, J.ROLE["ship"], "middle", 260))
        xa, xb, yy = ov_xback(), OV["stop"], 660.0
        s.append(F.poly([(xa, yy - 12), (xa, yy), (xb, yy), (xb, yy - 12)], "none", J.AMBER, 4))
        s.append(_tline(xa - 14, 668.0, "約3m 戻り過ぎ", 26, J.AMBER, "end", 260))
        s.append(_tline(1180.0, 822.0, OV_T, 30, J.AMBER, "end", 260))
        s.append(_tline(1200.0, 822.0, "伊丹駅に着く（約1分08秒遅れ）", 28, INK, "start", 520))
    return s


# ══════════════════════════════════════════════════════════
#  two_cabs（c218）＝7両の列車（横から・先頭＝1両目が右）。7両目の車掌の放送 → 1両目の運転士からのブザーの合図（R1 p.17・p.220）
# ══════════════════════════════════════════════════════════
TC = dict(x0=180.0, x1=1740.0, y=560.0, h=80.0, n=7, gap=12.0)


def tc_car(i):
    """i＝0 → 7両目（左の端）… 6 → 1両目（右の端）"""
    w = (TC["x1"] - TC["x0"] - TC["gap"] * 6) / 7
    x = TC["x0"] + i * (w + TC["gap"])
    return x, x + w


def two_cabs_base(st0):
    y, h = TC["y"], TC["h"]
    g = []
    for i in range(7):
        a, b = tc_car(i)
        g.append(_train_block(a, b, y + h / 2, h, J.BG2 if 0 < i < 6 else "#2a3946", nose=(i == 6)))
        for k in range(3):
            wx = a + 22 + k * ((b - a - 60) / 3)
            g.append(F.rect(wx, y + 16, (b - a - 90) / 3, 22, "#41606f", None, None, rx=4))
    a7, b7 = tc_car(0)
    a1, b1 = tc_car(6)
    g.append(_tline((a7 + b7) / 2, y + h + 46, "7両目", 28, INK, "middle", 160))
    g.append(_tline((a7 + b7) / 2, y + h + 90, "車掌", 30, sc("sha"), "middle", 160))
    g.append(_tline((a1 + b1) / 2, y + h + 46, "1両目", 28, INK, "middle", 160))
    g.append(_tline((a1 + b1) / 2, y + h + 90, "運転士", 30, INK, "middle", 160))
    g.append(_arrow(1610.0, 780.0, 1740.0, 780.0, J.TICK, 4, 18))
    g.append(_tline(1600.0, 788.0, "進む向き", 24, J.TICK, "end", 160))
    return g


def two_cabs_stage(prev, st):
    s = []
    a7, b7 = tc_car(0)
    a1, b1 = tc_car(6)
    if _on(prev, st, "call"):
        s.append(_speaker((a7 + b7) / 2 - 20, 470.0, 1.0, sc("sha")))
        s.append(_tline(a7 + 40, 410.0, "放送「次は尼崎」", 28, sc("sha"), "start", 320))
    if _on(prev, st, "buzz"):
        s.append(_arrow((a1 + b1) / 2, 500.0, a7 + 240, 500.0, J.AMBER, 5, 22, dash="16 10"))
        s.append(_buzzer((a1 + b1) / 2 + 40, 470.0, 0.8, J.AMBER))
        s.append(_tline(1000.0, 476.0, "ブザーの合図「電話機にかかれ」", 28, J.AMBER, "middle", 560))
    return s


# ══════════════════════════════════════════════════════════
#  glass（c220）＝7両目の運転室を横から（客室とのあいだにガラスの仕切り・壁の車内電話）。受話器が戻る＝動く部品。人は描かない
# ══════════════════════════════════════════════════════════
GL = dict(floor=780.0, ceil=330.0, x0=200.0, gx=870.0, gw=28.0, x1=1720.0, hook=(1330.0, 470.0))


def glass_parts(st):
    hx, hy = GL["hook"]
    pts = [(hx - 12, hy - 66), (hx + 12, hy - 66), (hx + 12, hy - 40), (hx + 6, hy - 30), (hx + 6, hy + 30), (hx + 12, hy + 40),
           (hx + 12, hy + 66), (hx - 12, hy + 66), (hx - 12, hy + 40), (hx - 6, hy + 30), (hx - 6, hy - 30), (hx - 12, hy - 40)]
    hang = st.get("hang") == "on"
    return [_P("handset", "poly", pts, pivot=[hx, hy], rot=0.0 if hang else -40.0, fill=INK, stroke=J.BG, w=3,
               dx=0.0 if hang else -170.0, dy=0.0 if hang else 70.0, alpha=1.0)]


def glass_base(st0):
    hx, hy = GL["hook"]
    g = [F.line(GL["x0"], GL["floor"], GL["x1"], GL["floor"], J.LINE, 5), F.line(GL["x0"], GL["ceil"], GL["x1"], GL["ceil"], J.LINE_DIM, 4),
         F.rect(GL["gx"], GL["ceil"], GL["gw"], GL["floor"] - GL["ceil"], "#2a3946", J.LINE, 3),
         F.rect(GL["gx"] + 3, 400.0, GL["gw"] - 6, 250.0, J.ROLE["ship"], None, None, op=0.45),
         _tline(GL["gx"] + GL["gw"] + 16, 690.0, "ガラスの仕切り", 22, J.ROLE["ship"], "start", 200),   # 🔧 geom_gap：ガラスの上に字が乗った
         F.rect(hx - 34, hy - 80, 68, 190, J.BG2, J.LINE, 4, rx=10), F.circ(hx, hy + 80, 8, J.LINE, None),
         _tline(520.0, 740.0, "客室", 30, J.TICK, "middle", 200),
         _tline(1300.0, 740.0, "7両目の運転室", 30, INK, "middle", 360),
         _tline(1520.0, 740.0, "車掌", 30, sc("sha"), "start", 120)]
    return g


def glass_stage(prev, st):
    s = []
    if _on(prev, st, "say"):
        s.append(F.rect(880.0, 348.0, 380.0, 72.0, J.BG2, sc("sha"), 5, rx=36))      # 🔧 geom_gap：電話機の箱に 8.8px 重なった
        s.append(_tline(1070.0, 396.0, "「だいぶと行ってるよ」", 28, sc("sha"), "middle", 350))
    if _on(prev, st, "hang"):
        s.append(_waves(GL["gx"] - 6, 520.0, 26.0, 3, J.AMBER, 150, 210, 22.0, 5))
        s.append(_tline(520.0, 470.0, "客室の側から叩く", 28, J.AMBER, "middle", 300))
        s.append(_tline(1400.0, 640.0, "受話器を戻す", 28, INK, "start", 260))
    return s


# ══════════════════════════════════════════════════════════
#  ruler_v（c223）＝縦の物差し（止まるべき位置から上へ・1m＝11.5画素）：無線で報告した 8m・車掌の見立て 30〜40m（R1 p.18）→ 5m の線（聞いた話）
# ══════════════════════════════════════════════════════════
RV = dict(x=760.0, w=70.0, y0=800.0, k=11.5, top=45.0, x1=1180.0)
RV_SAY, RV_THINK, RV_HEARD = 8.0, (30.0, 40.0), 5.0


def rv_y(m):
    return RV["y0"] - m * RV["k"]


def ruler_v_base(st0):
    x, w = RV["x"], RV["w"]
    g = [F.rect(x - w / 2, rv_y(RV["top"]), w, RV["y0"] - rv_y(RV["top"]), J.BG2, J.LINE, 4, rx=6)]
    for m in range(0, 46):
        L = 34 if m % 10 == 0 else (22 if m % 5 == 0 else 10)
        g.append(F.line(x - w / 2, rv_y(m), x - w / 2 + L, rv_y(m), J.TICK, 3 if m % 5 else 4))
    for m in (0, 10, 20, 30, 40):
        g.append(_tline(x - w / 2 - 14, rv_y(m) + 9, f"{m}m", 24, J.TICK, "end", 100))
    g.append(_tline(x + w / 2 + 16, rv_y(0) + 9, "止まるべき位置", 26, J.AMBER, "start", 260))
    g.append(_tline(x, rv_y(RV["top"]) - 20, "行き過ぎた長さ", 26, J.TICK, "middle", 260))
    return g


def ruler_v_stage(prev, st):
    s = []
    x1, xr = RV["x1"], RV["x"] + RV["w"] / 2
    org = sc("sha")
    if _on(prev, st, "say"):
        a, b = RV_THINK
        s.append(F.rect(xr, rv_y(b), x1 - xr, rv_y(a) - rv_y(b), org, org, 4, op=0.35))
        s.append(_tline(x1 + 20, (rv_y(a) + rv_y(b)) / 2 + 12, "車掌の見立て：30〜40m", 32, org, "start", 560))
        s.append(F.line(xr, rv_y(RV_SAY), x1, rv_y(RV_SAY), org, 9))
        s.append(_tline(x1 + 20, rv_y(RV_SAY) + 12, "無線で報告：8m", 32, org, "start", 500))
    if _on(prev, st, "heard"):
        s.append(F.line(xr - 120, rv_y(RV_HEARD), x1, rv_y(RV_HEARD), J.AMBER, 4, dash="14 10"))
        s.append(_tline(x1 + 20, 776.0, "5mほどなら", 28, J.AMBER, "start", 400))
        s.append(_tline(x1 + 20, 814.0, "処罰の軽い線（車掌が聞いた話）", 26, J.AMBER, "start", 520))   # 🔧 門番 echo
    return s


# ══════════════════════════════════════════════════════════
#  ring2（c225）＝2つの遅れの弧の時計（ひと回り＝2分・弧の角度は秒に比例）：外の橙＝「1分半」（車掌・時計を見ずに＝R1 p.18）／内の青＝約1分20秒（記録＝R1 p.12）
# ══════════════════════════════════════════════════════════
RG = dict(cx=640.0, cy=540.0, ro=210.0, ri=162.0, full=120.0, bw=32.0)
RG_SAY, RG_REC = 90, 80


def rg_ang(sec):
    return -90.0 + 360.0 * sec / RG["full"]


def ring2_base(st0):
    cx, cy, ro = RG["cx"], RG["cy"], RG["ro"]
    g = [F.circ(cx, cy, ro + 26, "none", J.LINE_DIM, 3), F.circ(cx, cy, RG["ri"] - 26, J.BG2, J.LINE_DIM, 3)]
    for k in range(12):
        a = math.radians(rg_ang(k * 10))
        L = 18 if k % 3 == 0 else 9
        g.append(F.line(cx + (ro + 26) * math.cos(a), cy + (ro + 26) * math.sin(a), cx + (ro + 26 + L) * math.cos(a),
                        cy + (ro + 26 + L) * math.sin(a), J.TICK, 4))
    g.append(_tline(cx, cy - ro - 58, "0", 26, J.TICK, "middle", 60))
    g.append(_tline(cx + ro + 60, cy + 9, "30秒", 24, J.TICK, "start", 100))
    g.append(_tline(cx, cy + ro + 78, "1分", 24, J.TICK, "middle", 100))
    g.append(_tline(cx - ro - 60, cy + 9, "1分30秒", 24, J.TICK, "end", 140))
    # 🔧 門番 layout：輪の真ん中の字は、輪の上と下の点が「上下に貫く」と数えられる＝札は右の2枚に任せる
    return g


def _rg_card(y, big, sub, col):
    return (F.rect(1060.0, y - 96, 640.0, 170.0, J.BG2, col, 5, rx=14) + _big(1380.0, y, big, 54, col)
            + _tline(1380.0, y + 50, sub, 26, J.TICK, "middle", 600))


def ring2_stage(prev, st):
    s = []
    cx, cy = RG["cx"], RG["cy"]
    if _on(prev, st, "say"):
        s.append(F.poly(_arcpts(cx, cy, RG["ro"], RG["ro"], rg_ang(0), rg_ang(RG_SAY), 60), "none", sc("sha"), RG["bw"]))
        s.append(_rg_card(440.0, "「1分半」", "車掌の報告（時計を見ずに）", sc("sha")))
    if _on(prev, st, "rec"):
        s.append(F.poly(_arcpts(cx, cy, RG["ri"], RG["ri"], rg_ang(0), rg_ang(RG_REC), 60), "none", sc("rep"), RG["bw"]))
        s.append(_rg_card(700.0, "約1分20秒", "記録（報告書）：伊丹駅を出たとき", sc("rep")))
    return s


# ══════════════════════════════════════════════════════════
#  tags4（c226）＝紐に下がる4つの値札（時の順・出どころの色）：8m 車掌の無線／約40m 国会の社長〈当時〉「車掌の申告によりますと」（2005年5月17日）／
#  約70m 建議（2005年9月6日・K05 p.2）／約72m 報告書（2007年6月・R1 p.12）
# ══════════════════════════════════════════════════════════
TG4 = (("sha", "8m", ("事故の朝の無線",)), ("kok", "約40m", ("2005年5月", "車掌の申告として")), ("ken", "約70m", ("2005年9月",)),
       ("rep", "約72m", ("2007年6月",)))
TG4_HEAD = dict(sha="車掌の無線", kok="国会：社長（当時）", ken="建議：事故調査委員会", rep="報告書：事故調査委員会")
TGX = dict(xs=(370.0, 773.0, 1176.0, 1579.0), y=330.0, top=380.0, w=340.0, h=410.0)


def tags4_base(st0):
    return [F.line(170.0, TGX["y"], 1770.0, TGX["y"], J.LINE, 4)]


def _tag(i):
    key, num, foot = TG4[i]
    x, col = TGX["xs"][i], sc(key)
    top, w, h = TGX["top"], TGX["w"], TGX["h"]
    g = [F.line(x, TGX["y"], x, top + 14, J.LINE, 3), F.rect(x - w / 2, top, w, h, J.BG2, col, 5, rx=16), F.circ(x, top + 24, 9, J.BG, J.LINE, 3),
         _tline(x, top + 76, TG4_HEAD[key], 26, col, "middle", w - 28), _big(x, top + 220, num, 80, INK)]
    for k, t in enumerate(foot):
        g.append(_tline(x, top + 312 + 40 * k, t, 26, J.TICK, "middle", w - 28))
    return "".join(g)


def tags4_stage(prev, st):
    s = []
    for i, f_ in enumerate(("t1", "t2", "t3", "t4")):
        if _on(prev, st, f_):
            s.append(_tag(i))
    return s


# ══════════════════════════════════════════════════════════
#  matrix（c227）＝出どころの表（列＝車掌・国会・建議・報告書／行＝行き過ぎ・遅れ）→ 2行目で見出しの列に黄の枠
# ══════════════════════════════════════════════════════════
MX_COLS = ("sha", "kok", "ken", "rep")
MX_ROWS = (("行き過ぎ", ("8m", "約40m", "約70m", "約72m")), ("遅れ", ("「1分半」", "—", "—", ("約1分08秒（着）", "約1分20秒（発）"))))
MX = dict(xl=330.0, xs=(640.0, 940.0, 1240.0, 1560.0), yh=360.0, ys=(500.0, 660.0), lines=(410.0, 580.0, 740.0), seps=(790.0, 1090.0, 1390.0))


def matrix_base(st0):
    g = [F.line(220.0, y, 1720.0, y, J.LINE_DIM, 3) for y in MX["lines"]]
    g += [F.line(x, MX["lines"][0] + 10, x, MX["lines"][2] - 10, J.LINE_DIM, 3) for x in MX["seps"]]
    for k, x in zip(MX_COLS, MX["xs"]):
        g.append(_chip(x, MX["yh"], SRC[k][0], sc(k), 28))
    return g


def _mx_row(i):
    name, cells = MX_ROWS[i]
    y = MX["ys"][i]
    g = [_tline(MX["xl"], y + 12, name, 30, INK, "middle", 200)]
    for k, x, c in zip(MX_COLS, MX["xs"], cells):
        if isinstance(c, tuple):
            g.append(_tline(x, y - 12, c[0], 28, sc(k), "middle", 290))
            g.append(_tline(x, y + 38, c[1], 28, sc(k), "middle", 290))
        else:
            g.append(_tline(x, y + 14, c, 36, J.LINE_DIM if c == "—" else sc(k), "middle", 280))
    return "".join(g)


def matrix_stage(prev, st):
    s = []
    if _on(prev, st, "r1"):
        s.append(_mx_row(0))
    if _on(prev, st, "r2"):
        s.append(_mx_row(1))
    if _on(prev, st, "head"):
        s.append(F.rect(470.0, MX["yh"] - 40, 1260.0, 80.0, "none", J.AMBER, 5, rx=16))
        s.append(_tline(CX, 812.0, "数には、どの記録かを添える", 30, J.AMBER, "middle", 700))
    return s


# ══════════════════════════════════════════════════════════
#  第2章
#  hscale（c302）＝横の速度の目盛り（100〜130km/h・比例）：1両目の記録 124〜125km/h・9:18:09ごろ（R1 p.13・p.91）・
#  速度計の表示「121」か「122」（見られる＝R1 p.13）→ 2行目で最高速度 120km/h の線と超えた所
# ══════════════════════════════════════════════════════════
HS = dict(x0=220.0, v0=100.0, k=48.0, y=600.0)
HS_MAX = 120
HS_REC = (124, 125)
HS_SHOW = (121, 122)
HS_T = "9:18:09ごろ"


def hs_x(v):
    return HS["x0"] + (v - HS["v0"]) * HS["k"]


def hscale_base(st0):
    y = HS["y"]
    g = [F.line(hs_x(100), y, hs_x(130), y, J.LINE, 5)]
    for v in range(100, 131):
        L = 26 if v % 10 == 0 else (16 if v % 5 == 0 else 8)
        g.append(F.line(hs_x(v), y, hs_x(v), y + L, J.TICK, 3))
    for v in (100, 110, 120, 130):
        g.append(_tline(hs_x(v), y + 58, str(v), 26, J.TICK, "middle", 80))
    g.append(_tline(hs_x(130) + 40, y + 58, "km/h", 24, J.TICK, "start", 100))
    return g


def hscale_stage(prev, st):
    s = []
    y = HS["y"]
    if _on(prev, st, "rec"):
        a, b = (hs_x(v) for v in HS_REC)
        s.append(F.rect(a, y - 80, b - a, 70, sc("rep"), None, None, rx=4))
        s.append(_tline(b + 24, y - 54, "1両目の記録", 28, sc("rep"), "start", 260))
        s.append(_tline(b + 24, y - 16, "124〜125km/h", 28, sc("rep"), "start", 260))
        s.append(_tline((a + b) / 2, y - 112, HS_T, 30, J.AMBER, "middle", 260))
        for v in HS_SHOW:
            x = hs_x(v)
            s.append(F.poly([(x - 12, y + 40), (x + 12, y + 40), (x, y + 18)], INK, None, close=True))
        s.append(_tline((hs_x(HS_SHOW[0]) + hs_x(HS_SHOW[1])) / 2, 726.0, "速度計の表示は「121」か「122」（見られる）", 26, INK, "middle", 640))
    if _on(prev, st, "limit"):
        x = hs_x(HS_MAX)
        # 🔧 試し焼き 40246394718：赤い面が青い記録の帯に重なって紫に見えた＝帯の手前（124）まで
        s.append(F.rect(x, y - 80, hs_x(HS_REC[0]) - x, 70, J.ALERT, None, None, op=0.28))
        s.append(F.line(x, 400.0, x, y + 30, J.ALERT, 6))
        s.append(_tline(x - 14, 392.0, "最高速度 120km/h", 30, J.ALERT, "end", 360))
        s.append(_tline((x + hs_x(HS_REC[0])) / 2, y - 32, "超えていた", 26, J.ALERT, "middle", 180))
    return s


# ══════════════════════════════════════════════════════════
#  tt_band（c308）＝交信の横の帯（9時18分からの秒・1秒＝105画素）：呼出音 0.9〜1.9・指令員 5.9〜6.8・車掌 7.6〜10.7
#  （付図24 の帯を図形の座標で読んだ値＝sources.md §4。秒の字は目盛りだけ＝§1-5 に無い秒を札にしない）
# ══════════════════════════════════════════════════════════
TB = dict(x0=360.0, k=105.0, x1=1640.0, ys=dict(shi=470.0, sha=610.0), h=46.0, ax=720.0, bell=380.0)
TB_EV = (("bell", "呼び出しの音", 0.9, 1.9), ("shi", "応答", 5.9, 6.8), ("sha", "名乗る", 7.6, 10.7))


def tb_x(sec):
    return TB["x0"] + sec * TB["k"]


def tt_band_base(st0):
    g = [F.line(TB["x0"], TB["ax"], TB["x1"], TB["ax"], J.LINE, 5)]
    for k in range(0, 13):
        L = 22 if k % 5 == 0 else 10
        g.append(F.line(tb_x(k), TB["ax"], tb_x(k), TB["ax"] + L, J.TICK, 3))
    g.append(_tline(tb_x(0), TB["ax"] + 56, "9:18", 28, J.AMBER, "middle", 120))
    g.append(_tline(tb_x(5), TB["ax"] + 56, "＋5秒", 26, J.TICK, "middle", 120))
    g.append(_tline(tb_x(10), TB["ax"] + 56, "＋10秒", 26, J.TICK, "middle", 140))
    for key in ("shi", "sha"):
        y = TB["ys"][key]
        g.append(F.line(TB["x0"], y, TB["x1"], y, J.LINE_DIM, 2, dash="8 10"))
        g.append(_tline(TB["x0"] - 24, y + 11, SRC[key][0], 30, sc(key), "end", 220))
    return g


def _tb_ev(i):
    key, lab, a, b = TB_EV[i]
    if key == "bell":
        x = (tb_x(a) + tb_x(b)) / 2
        return _bell(x, TB["bell"], 1.0, J.AMBER) + _tline(x + 40, TB["bell"] + 10, lab, 26, J.TICK, "start", 260)
    y, col = TB["ys"][key], sc(key)
    return (F.rect(tb_x(a), y - TB["h"] / 2, tb_x(b) - tb_x(a), TB["h"], col, None, None, rx=6)
            + _tline((tb_x(a) + tb_x(b)) / 2, y - TB["h"] / 2 - 14, lab, 28, col, "middle", 200))


def tt_band_stage(prev, st):
    s = []
    if _on(prev, st, "e1"):
        s += [_tb_ev(0), _tb_ev(1)]
    if _on(prev, st, "e2"):
        s.append(_tb_ev(2))
    return s


# ══════════════════════════════════════════════════════════
#  zone（c311）＝線路の区間の帯（塚口駅の先 → 曲線）に「ブレーキを始める位置」の区間 → 上に指令員の復唱の帯と「5秒ほど後まで」（R1 p.13）。
#  時間（上）と場所（下）を点線でつないだ模式
# ══════════════════════════════════════════════════════════
ZN = dict(y=660.0, h=40.0, x0=220.0, xc=1500.0, x1=1700.0, zone=(900.0, 1260.0), ty=440.0, rep=(760.0, 980.0), br=(760.0, 1260.0))
ZN_SEC = 5


def zone_base(st0):
    y, h = ZN["y"], ZN["h"]
    g = [F.rect(ZN["x0"], y - h / 2, ZN["xc"] - ZN["x0"], h, "#2a3946", J.LINE, 3),
         F.rect(ZN["xc"], y - h / 2, ZN["x1"] - ZN["xc"], h, J.ALERT, None, None, op=0.7),
         F.rect(240.0, y - 66, 140.0, 30.0, J.BG2, J.LINE, 3, rx=4), _tline(310.0, y + 70, "塚口駅", 28, INK, "middle", 160),
         _tline((ZN["xc"] + ZN["x1"]) / 2, y + 70, "曲線", 28, J.ALERT, "middle", 160),
         _train_block(520.0, 700.0, y, 28.0)]
    return g


def zone_stage(prev, st):
    s = []
    y = ZN["y"]
    a, b = ZN["zone"]
    if _on(prev, st, "zone"):
        s.append(F.rect(a, y - 24, b - a, 48, J.AMBER, J.AMBER, 4, op=0.4))
        s.append(_tline((a + b) / 2, y + 70, "ブレーキを始める位置", 28, J.AMBER, "middle", 380))
        s.append(_tline((a + b) / 2, y + 108, "（このあたり）", 24, J.TICK, "middle", 260))
    if _on(prev, st, "time"):
        ty = ZN["ty"]
        r0, r1 = ZN["rep"]
        b0, b1 = ZN["br"]
        s.append(F.line(700.0, ty, 1500.0, ty, J.TICK, 3))
        s.append(F.rect(r0, ty - 20, r1 - r0, 40, sc("shi"), None, None, rx=6))
        s.append(_tline((r0 + r1) / 2, ty - 34, "指令員の復唱", 28, sc("shi"), "middle", 300))
        s.append(_bracket(b0, b1, ty + 50, J.AMBER, 4, up=True, tick=14))
        s.append(_tline((b0 + b1) / 2 + 30, ty + 94, "復唱のころ 〜 5秒ほど後", 28, J.AMBER, "middle", 420))
        s.append(F.line(b0, ty + 56, a, y - 30, J.LINE, 3, dash="8 8") + F.line(b1, ty + 56, b, y - 30, J.LINE, 3, dash="8 8"))
    return s


# ══════════════════════════════════════════════════════════
#  clockfan（c312）＝秒の時計（9時18分）に指令員の復唱の扇（27秒〜31秒＝付図24 の帯 9:18:27.4〜30.6・§1-5 の「9:18:27〜31」）→ 秒針が27秒から31秒へ
# ══════════════════════════════════════════════════════════
CF = dict(cx=640.0, cy=550.0, r=250.0)
CF_A, CF_B = 27, 31
CF_HM = (9, 18)


def cf_ang(sec):
    return -90.0 + 6.0 * sec


def clockfan_parts(st):
    cx, cy, r = CF["cx"], CF["cy"], CF["r"]
    sec = CF_B if st.get("sweep") == "on" else CF_A
    pts = [(cx - 4, cy + 34), (cx + 4, cy + 34), (cx + 2, cy - r + 26), (cx - 2, cy - r + 26)]
    return [_P("sec", "poly", pts, pivot=[cx, cy], rot=6.0 * sec, fill=J.ALERT, stroke=J.ALERT, w=2, alpha=1.0)]


def clockfan_base(st0):
    cx, cy, r = CF["cx"], CF["cy"], CF["r"]
    g = [F.circ(cx, cy, r, J.BG2, J.LINE, 6)]
    for k in range(60):
        a = math.radians(cf_ang(k))
        L = 26 if k % 5 == 0 else 12
        g.append(F.line(cx + (r - 10) * math.cos(a), cy + (r - 10) * math.sin(a), cx + (r - 10 - L) * math.cos(a),
                        cy + (r - 10 - L) * math.sin(a), J.TICK, 4 if k % 5 == 0 else 2))
    h, m = CF_HM
    for ang, L, wd in ((-90.0 + (h + m / 60.0) * 30.0, 130.0, 14), (-90.0 + m * 6.0, 196.0, 9)):
        a = math.radians(ang)
        g.append(F.line(cx, cy, cx + L * math.cos(a), cy + L * math.sin(a), INK, wd))
    g.append(_tline(cx, cy - 92, "9時18分", 30, J.AMBER, "middle", 200))
    return g


def clockfan_stage(prev, st):
    s = []
    cx, cy, r = CF["cx"], CF["cy"], CF["r"]
    if _on(prev, st, "fan"):
        s.append(_sector(cx, cy, 0.0, r - 16, cf_ang(CF_A), cf_ang(CF_B), sc("shi"), None, None, op=0.6, n=8))
        s.append(_chip(1320.0, 420.0, "指令員の復唱", sc("shi"), 30))
        s.append(_tline(1320.0, 494.0, "付図24 の帯", 26, J.TICK, "middle", 300))
    if _on(prev, st, "sweep"):
        s.append(_tline(1320.0, 640.0, "9:18:27〜31ごろ", 44, J.AMBER, "middle", 600))
    return s + [F.circ(cx, cy, 12, INK, None)] if _on(prev, st, "fan") else s


# ══════════════════════════════════════════════════════════
#  crossing（c316）＝伊丹駅の先の線路（上から）：指令員が「踏切があるのでは」と心配した → 運転士に位置を聞こうとした → 実際には踏切は無い（R1 p.241）
# ══════════════════════════════════════════════════════════
CR = dict(y=600.0, road=(1020.0, 1100.0), card=(1450.0, 380.0))


def crossing_base(st0):
    y = CR["y"]
    return [_rails(160.0, 1760.0, y), F.rect(160.0, 500.0, 360.0, 66.0, J.BG2, J.LINE, 4, rx=6),
            _tline(340.0, 543.0, "伊丹駅", 28, INK, "middle", 200), _train_block(640.0, 860.0, y, 52.0)]


def crossing_stage(prev, st):
    s = []
    y = CR["y"]
    r0, r1 = CR["road"]
    cx, cy = CR["card"]
    if _on(prev, st, "doubt"):
        s.append(F.line(r0, 440.0, r0, 720.0, J.LINE, 4, dash="14 10") + F.line(r1, 440.0, r1, 720.0, J.LINE, 4, dash="14 10"))
        s.append(_qmark((r0 + r1) / 2, 380.0, 80, J.AMBER))
        s.append(F.rect(cx - 200, cy - 50, 400, 100, J.BG2, sc("shi"), 5, rx=14))
        s.append(_tline(cx, cy - 12, "総合指令所の指令員", 24, sc("shi"), "middle", 370))
        s.append(_tline(cx, cy + 30, "踏切があるのでは？", 28, INK, "middle", 370))
    if _on(prev, st, "ask"):
        s.append(_arrow(cx - 210, cy + 30, 880.0, y - 40, sc("shi"), 5, 22, dash="14 8"))
        s.append(_tline(cx, cy + 96, "運転士に、位置を聞こうとした", 26, sc("shi"), "middle", 420))
        s.append(_xmark((r0 + r1) / 2, y, 46, J.ALERT))
        s.append(_tline((r0 + r1) / 2, 790.0, "実際は、伊丹駅の先に踏切は無い", 30, J.ALERT, "middle", 600))
    return s


# ══════════════════════════════════════════════════════════
#  two_ribbons（c325）＝右の端（実際にブレーキを使い始めた所）でそろう2本の帯（長さは秒に比例）：約16秒（毎秒2.8km/h）・約22秒（毎秒2.0km/h）＝R1 p.221
# ══════════════════════════════════════════════════════════
TRB = dict(xe=1560.0, k=52.0, ya=420.0, yb=600.0, h=60.0)
TRB_A, TRB_B = (16, "2.8"), (22, "2.0")


def trb_x0(sec):
    return TRB["xe"] - sec * TRB["k"]


def two_ribbons_base(st0):
    xe = TRB["xe"]
    return [F.line(xe, 372.0, xe, 700.0, INK, 4, dash="12 8"), _tline(xe, 352.0, "実際にブレーキを使い始めた", 26, INK, "middle", 380),
            F.circ(220.0, 540.0, 52.0, J.BG2, J.LINE, 6), F.rect(206.0, 474.0, 28.0, 14.0, J.LINE, None, None),
            F.line(220.0, 540.0, 220.0, 506.0, J.AMBER, 5), F.line(220.0, 540.0, 246.0, 556.0, J.AMBER, 5)]


def _trb(y, sec, rate, sub, col):
    x0 = trb_x0(sec)
    return (F.rect(x0, y, TRB["xe"] - x0, TRB["h"], col, None, None, rx=8) + _big((x0 + TRB["xe"]) / 2, y - 16, f"約{sec}秒", 40, J.AMBER)
            + _tline((x0 + TRB["xe"]) / 2, y + TRB["h"] + 40, sub, 24, J.TICK, "middle", 520)
            + F.line(x0, y - 10, x0, y + TRB["h"] + 10, INK, 3) + _tline(x0, y + TRB["h"] + 80, "始めるべき位置", 22, J.TICK, "middle", 200))


def two_ribbons_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_trb(TRB["ya"], TRB_A[0], TRB_A[1], f"減速を毎秒{TRB_A[1]}km/hとした計算", sc("rep")))
    if _on(prev, st, "b"):
        s.append(_trb(TRB["yb"], TRB_B[0], TRB_B[1], f"効きを弱く：毎秒{TRB_B[1]}km/h", J.ROLE["ship"]))
    return s


# ══════════════════════════════════════════════════════════
#  tiles（c326）＝1マス＝約1秒の升（B1 約2秒＝黄・惰性 約39秒＝灰＝R1 p.221）・列車の印が升の上を進む（動く部品）
# ══════════════════════════════════════════════════════════
TL = dict(x0=180.0, s=34.0, gap=4.0, y=560.0, ty=448.0)
TL_B1, TL_COAST = 2, 39


def tl_x(i):
    return TL["x0"] + i * (TL["s"] + TL["gap"])


def tiles_parts(st):
    x1 = tl_x(TL_B1 + TL_COAST - 1) + TL["s"]
    dx = (x1 - 260.0) if st.get("fill") == "on" else 0.0
    y = TL["ty"]
    pts = [(180.0, y - 18), (240.0, y - 18), (260.0, y), (240.0, y + 18), (180.0, y + 18)]
    return [_P("train", "poly", pts, fill=TRAIN, stroke=J.BG, w=3, dx=dx, alpha=1.0)]


def tiles_base(st0):
    return [F.rect(tl_x(i), TL["y"], TL["s"], TL["s"], J.BG2, J.LINE_DIM, 3, rx=4) for i in range(TL_B1 + TL_COAST)]


def tiles_stage(prev, st):
    s = []
    if _on(prev, st, "fill"):
        for i in range(TL_B1 + TL_COAST):
            b1 = i < TL_B1
            s.append(F.rect(tl_x(i), TL["y"], TL["s"], TL["s"], J.AMBER if b1 else "#5d7584", None, None, rx=4))
        s.append(_tline(tl_x(0), TL["y"] - 54, "B1 約2秒", 28, J.AMBER, "start", 200))
        x0, x1 = tl_x(TL_B1), tl_x(TL_B1 + TL_COAST - 1) + TL["s"]
        s.append(_bracket(x0, x1, TL["y"] - 22, INK, 4, up=False, tick=12))
        s.append(_tline((x0 + x1) / 2, TL["y"] - 54, "惰性 約39秒", 32, INK, "middle", 400))
        s.append(_tline(x1, TL["y"] + TL["s"] + 52, "1マス＝約1秒", 24, J.TICK, "end", 300))
    return s


# ══════════════════════════════════════════════════════════
#  clues（c329）＝真ん中の「？」（曲線の手前の運転士の注意）と、ブレーキの遅れ 約16〜22秒（推算）→ 2つの手がかり（無線のやり取り・車内電話＝R1 p.221）
# ══════════════════════════════════════════════════════════
CL = dict(cx=960.0, cy=540.0, r=96.0, l=(440.0, 560.0), rr=(1480.0, 560.0), w=440.0, h=190.0)


def clues_base(st0):
    return []


def clues_stage(prev, st):
    s = []
    cx, cy = CL["cx"], CL["cy"]
    if _on(prev, st, "q"):
        s.append(F.circ(cx, cy, CL["r"], J.BG2, J.LINE, 5) + _qmark(cx, cy - 6, 110, J.AMBER))
        s.append(_tline(cx, cy + CL["r"] + 54, "曲線の手前の、運転士の注意", 28, INK, "middle", 500))
        s.append(_chip(cx, 330.0, "ブレーキの遅れ：約16〜22秒（推算）", J.LINE, 26, ink=INK))
    if _on(prev, st, "two"):
        for (x, y), icon, t1, t2 in ((CL["l"], "radio", "無線のやり取り", "車掌と指令員"), (CL["rr"], "phone", "車内電話", "運転士と車掌")):
            s.append(F.rect(x - CL["w"] / 2, y - CL["h"] / 2, CL["w"], CL["h"], J.BG2, J.AMBER, 4, rx=14))
            ix = x - CL["w"] / 2 + 70
            s.append(_radio(ix, y + 10, 1.0, J.AMBER) if icon == "radio" else _phone(ix, y, 0.9, J.AMBER))
            s.append(_tline(ix + 70, y - 4, t1, 32, INK, "start", CL["w"] - 160))
            s.append(_tline(ix + 70, y + 44, t2, 24, J.TICK, "start", CL["w"] - 160))
        s.append(F.line(CL["l"][0] + CL["w"] / 2, CL["l"][1], cx - CL["r"] - 6, cy, J.AMBER, 3, dash="10 8"))
        s.append(F.line(CL["rr"][0] - CL["w"] / 2, CL["rr"][1], cx + CL["r"] + 6, cy, J.AMBER, 3, dash="10 8"))
        s.append(_tline(cx, 800.0, "報告書が見る手がかり", 28, sc("rep"), "middle", 400))
    return s


# ══════════════════════════════════════════════════════════
#  第3章
#  section（c407）＝後ろから見た2両目の断面：四角 → ひし形（動く部品）・客室の空間がほぼ無くなる（R1 p.233）。右に横から見た2両目と乗降口（位置は模式）
# ══════════════════════════════════════════════════════════
SC_OUT0 = ((490.0, 380.0), (790.0, 380.0), (790.0, 760.0), (490.0, 760.0))
# 🔧 試し焼き 40246394718：傾けた四角に見えた＝上下につぶれた菱形（高さ 380 → 280・幅 300 → 460）
SC_OUT1 = ((650.0, 470.0), (880.0, 610.0), (650.0, 750.0), (420.0, 610.0))
SC_IN0 = ((520.0, 410.0), (760.0, 410.0), (760.0, 730.0), (520.0, 730.0))
SC_K1, SC_K2 = 0.78, 0.12      # 内の空間の縮み（ひし形の外形からの比）


def _shrink(pts, k):
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return tuple((cx + k * (x - cx), cy + k * (y - cy)) for x, y in pts)


def section_parts(st):
    crush = st.get("crush") == "on"
    gone = st.get("gone") == "on"
    out = SC_OUT1 if crush else SC_OUT0
    inn = _shrink(SC_OUT1, SC_K2) if gone else (_shrink(SC_OUT1, SC_K1) if crush else SC_IN0)
    return [_P("body", "poly", out, fill=J.BG2, stroke=INK, w=6, alpha=1.0),
            _P("room", "poly", inn, fill=J.ROLE["ship"], stroke=J.ROLE["ship"], w=2, alpha=0.45)]


def section_base(st0):
    g = [F.rect(1180.0, 420.0, 540.0, 100.0, J.BG2, J.LINE, 4, rx=10), _tline(1450.0, 398.0, "2両目を横から", 24, J.TICK, "middle", 260)]
    for x in (1240.0, 1370.0, 1500.0, 1630.0):
        g.append(F.rect(x - 22, 436.0, 44.0, 76.0, "#2a3946", J.LINE_DIM, 3, rx=4))
    return g


def section_stage(prev, st):
    s = []
    if _on(prev, st, "crush"):
        for x in (1240.0, 1370.0, 1500.0):
            s.append(F.rect(x - 26, 432.0, 52.0, 84.0, "none", J.ALERT, 5, rx=6))
        s.append(_tline(1370.0, 570.0, "1つ目〜3つ目の乗降口", 26, J.ALERT, "middle", 360))
        s.append(_tline(640.0, 840.0, "断面がひし形に", 28, INK, "middle", 300))
    if _on(prev, st, "gone"):
        s.append(_tline(1450.0, 700.0, "客室の空間：ほぼ無し", 32, J.ROLE["ship"], "middle", 460))
    return s


# ══════════════════════════════════════════════════════════
#  plaques（c412）＝2つの数の板（並べ）：562人（報告書・警察の情報＝R1 p.1）／549人（消防庁・2005年5月24日の時点＝F1 p.1）。
#  起訴の 493人は次の c413 の語り＝先回りしない
# ══════════════════════════════════════════════════════════
PQ = (("rep", "562人", ("報告書（2007年）", "警察の情報による")), ("fd", "549人", ("消防庁", "第32報（2005年5月24日）")))   # 🔧 門番 echo
PQX = dict(xs=(600.0, 1320.0), y0=340.0, w=520.0, h=420.0)


def plaques_base(st0):
    return []


def _pq(i):
    key, num, (head, foot) = PQ[i]
    x, col = PQX["xs"][i], sc(key)
    y0, w, h = PQX["y0"], PQX["w"], PQX["h"]
    return (F.rect(x - w / 2, y0, w, h, J.BG2, col, 5, rx=18) + F.line(x - w / 2 + 20, y0 + 84, x + w / 2 - 20, y0 + 84, col, 3)
            + F.rect(x - w / 2 + 38, y0 + 30, 26, 8, col, None, None) + F.rect(x - w / 2 + 47, y0 + 21, 8, 26, col, None, None)
            + _tline(x, y0 + 56, head, 30, col, "middle", w - 120) + _big(x, y0 + 262, num, 110, INK)
            + _tline(x, y0 + 360, foot, 28, J.TICK, "middle", w - 40))


def plaques_stage(prev, st):
    s = []
    if _on(prev, st, "p1"):
        s.append(_pq(0))
    if _on(prev, st, "p2"):
        s.append(_pq(1))
    return s


# ══════════════════════════════════════════════════════════
#  split_box（c415）＝JR西日本の書き方（同社の頁）：亡くなった人＝お客様 106人｜運転士 1人／けがをした人＝お客様 562人｜付近を通行中の方 1人（分けて書く）
# ══════════════════════════════════════════════════════════
SB_ROWS = (("亡くなった人", ("お客様", "106人"), ("運転士", "1人")), ("けがをした人", ("お客様", "562人"), ("付近を通行中の方", "1人")))
SB = dict(x0=200.0, x1=1720.0, y0=330.0, ys=(360.0, 590.0), rh=200.0, xl=370.0, ca=(540.0, 1110.0), cb=(1150.0, 1700.0))


def split_box_base(st0):
    col = sc("jr")
    return [F.rect(SB["x0"], SB["y0"], SB["x1"] - SB["x0"], 470.0, "none", col, 5, rx=18),
            _tline(CX, SB["y0"] - 18, "JR西日本の書き方（同社の頁）", 28, col, "middle", 600)]


def _sb_row(i):
    name, a, b = SB_ROWS[i]
    y = SB["ys"][i]
    col = sc("jr")
    g = [_tline(SB["xl"], y + SB["rh"] / 2 + 10, name, 30, INK, "middle", 300)]
    for (x0, x1), (lab, num) in ((SB["ca"], a), (SB["cb"], b)):
        g.append(F.rect(x0, y + 10, x1 - x0, SB["rh"] - 20, J.BG2, J.LINE, 3, rx=12))
        g.append(_tline((x0 + x1) / 2, y + 64, lab, 28, J.TICK, "middle", x1 - x0 - 30))
        g.append(_big((x0 + x1) / 2, y + 156, num, 72, INK))
    g.append(F.line(1130.0, y + 4, 1130.0, y + SB["rh"] - 4, col, 8))
    return "".join(g)


def split_box_stage(prev, st):
    s = []
    if _on(prev, st, "r1"):
        s.append(_sb_row(0))
    if _on(prev, st, "r2"):
        s.append(_sb_row(1))
        s.append(_chip(1130.0, 830.0, "分けて書く", sc("jr"), 26))
    return s


# ══════════════════════════════════════════════════════════
#  chapters3（c418）＝兵庫県の検証報告書（2006年1月）の表紙と3つの箱（救助・医療・地域の動き＝語りの3つ）→ 原因の調べは外（HY1 p.2）
# ══════════════════════════════════════════════════════════
CH3 = (("救助", "ALERT"), ("医療", "OK"), ("地域の動き", "AMBER"))
CH3X = dict(xs=(780.0, 1130.0, 1480.0), y0=380.0, w=300.0, h=160.0, out=(1130.0, 700.0))


def chapters3_base(st0):
    col = sc("hy")
    g = [F.rect(200.0, 340.0, 300.0, 420.0, J.BG2, col, 5, rx=10), _tline(350.0, 412.0, "兵庫県", 30, col, "middle", 260),
         _tline(350.0, 462.0, "検証報告書", 30, INK, "middle", 260), _tline(350.0, 508.0, "2006年1月", 24, J.TICK, "middle", 260)]
    for k in range(4):
        g.append(F.line(236.0, 580.0 + k * 40, 464.0 - (40 if k == 3 else 0), 580.0 + k * 40, J.LINE_DIM, 8))
    return g


def chapters3_stage(prev, st):
    s = []
    y0, w, h = CH3X["y0"], CH3X["w"], CH3X["h"]
    if _on(prev, st, "three"):
        # 🔧 geom_gap：表紙から箱の左の縁へ引いた線が、手前の箱の字を貫いた＝上に横の線を通して箱の上へ下ろす
        s.append(F.poly([(500.0, 400.0), (540.0, 400.0), (540.0, y0 - 30), (CH3X["xs"][-1], y0 - 30)], "none", J.LINE_DIM, 3))
        for (t, c), x in zip(CH3, CH3X["xs"]):
            s.append(F.line(x, y0 - 30, x, y0, J.LINE_DIM, 3))
            s.append(F.rect(x - w / 2, y0, w, h, J.BG2, rc(c), 5, rx=14))
            s.append(_tline(x, y0 + h / 2 + 12, t, 34, rc(c), "middle", w - 30))
    if _on(prev, st, "out"):
        x, y = CH3X["out"]
        s.append(F.rect(x - 190, y - 56, 380, 112, J.BG2, J.LINE, 4, rx=14, dash="14 10"))
        s.append(_tline(x - 30, y + 12, "原因の調べ", 32, J.TICK, "middle", 300))
        s.append(_xmark(x + 140, y, 26, J.ALERT))
        s.append(_tline(x, y + 104, "この報告書の外", 26, J.ALERT, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  doors3（c420）＝3つの入口（原因の3つの文）→ 扉の札に言い方の強さ（推定される・考えられる・可能性が考えられる＝R1 p.243）と目盛り
# ══════════════════════════════════════════════════════════
DR3 = ("推定される", "考えられる", "可能性が考えられる")
DR3X = dict(xs=(520.0, 960.0, 1400.0), w=280.0, top=520.0, bot=800.0)


def doors3_base(st0):
    return []


def doors3_stage(prev, st):
    s = []
    w, top, bot = DR3X["w"], DR3X["top"], DR3X["bot"]
    if _on(prev, st, "q"):
        s.append(_chip(CX, 330.0, "ブレーキは、なぜ遅れた？", J.AMBER, 30, ink=INK))
        for k, x in enumerate(DR3X["xs"]):
            arch = _arcpts(x, top, w / 2, w / 2, 180, 360, 16)
            s.append(F.poly([(x - w / 2, bot)] + arch + [(x + w / 2, bot)], J.BG2, J.LINE, 5, close=True))
            s.append(_tline(x, top + 40, f"文{k + 1}", 30, J.TICK, "middle", 120))
    if _on(prev, st, "words"):
        for x, word in zip(DR3X["xs"], DR3):
            s.append(F.rect(x - 130, top + 86, 260, 130, J.BG2, J.AMBER, 4, rx=12))
            s.append(_tline(x, top + 140, word, 26, INK, "middle", 240))
            s.append(_meter(x - METER_W / 2, top + 184, word))
    return s


# ══════════════════════════════════════════════════════════
#  第4章
#  stairs4（c502）＝言い方の4段の階段（強い → 弱い＝R1 p.264）：認められる（言い切れる）・推定される（ほぼ間違いない）・考えられる（可能性が高い）・
#  可能性が考えられる（可能性がある）。頭は前の頁 c501 の2段（認められる・推定される）
# ══════════════════════════════════════════════════════════
ST4 = (("認められる", "言い切れる"), ("推定される", "ほぼ間違いない"), ("考えられる", "可能性が高い"), ("可能性が考えられる", "可能性がある"))
ST4X = dict(x0=200.0, dx=380.0, w=360.0, top=330.0, dy=95.0, bot=800.0)
ST4_COL = ("INK_W", "state", "ship", "LINE")


def st4_box(i):
    x0 = ST4X["x0"] + i * ST4X["dx"]
    return x0, ST4X["top"] + i * ST4X["dy"], x0 + ST4X["w"], ST4X["bot"]


def stairs4_base(st0):
    return []


def _st4(i):
    word, mean = ST4[i]
    x0, y0, x1, y1 = st4_box(i)
    col = rc(ST4_COL[i])
    cx = (x0 + x1) / 2
    return (F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, col, 5, rx=12) + _tline(cx, y0 + 50, word, 30, INK, "middle", x1 - x0 - 24)
            + _tline(cx, y0 + 92, mean, 24, J.TICK, "middle", x1 - x0 - 24) + _meter(cx - METER_W / 2, y0 + 130, word))


def stairs4_stage(prev, st):
    s = []
    if _on(prev, st, "s12"):
        s += [_st4(0), _st4(1)]
    if _on(prev, st, "s3"):
        s.append(_st4(2))
    if _on(prev, st, "s4"):
        s.append(_st4(3))
        s.append(_arrow(330.0, 834.0, 1600.0, 834.0, J.TICK, 4, 18))
        s.append(_tline(300.0, 842.0, "強い", 24, J.TICK, "end", 100))
        s.append(_tline(1630.0, 842.0, "弱い", 24, J.TICK, "start", 100))
    return s


# ══════════════════════════════════════════════════════════
#  persp（c503）＝運転席の高さから見た曲線の入口（遠近の模式）：原因の文1＝ブレーキの遅れ → 制限70km/h の曲線に約116km/h（R1 p.243）・「推定される」
# ══════════════════════════════════════════════════════════
PS_PATH = ((952.0, 820.0), (958.0, 720.0), (972.0, 610.0), (995.0, 520.0), (1030.0, 455.0), (1080.0, 410.0), (1150.0, 382.0),
           (1240.0, 366.0), (1340.0, 360.0))
PS_W = (300.0, 250.0, 185.0, 135.0, 98.0, 70.0, 50.0, 36.0, 26.0)
PS_CURVE = 4                   # この点から先が曲線（赤）
PS_LIMIT, PS_V = 70, 116
PS_WORD = "推定される"


def _ps_rails():
    L, R = [], []
    n = len(PS_PATH)
    for i, (x, y) in enumerate(PS_PATH):
        ax, ay = PS_PATH[max(0, i - 1)]
        bx, by = PS_PATH[min(n - 1, i + 1)]
        dx, dy = bx - ax, by - ay
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        w = PS_W[i]
        L.append((x - w * nx, y - w * ny))
        R.append((x + w * nx, y + w * ny))
    return L, R


def persp_base(st0):
    L, R = _ps_rails()
    g = []
    for a, b in zip(L, R):
        g.append(F.line(a[0], a[1], b[0], b[1], J.LINE_DIM, 5))
    c = PS_CURVE
    g.append(F.poly(L[:c + 1], "none", J.LINE, 6) + F.poly(R[:c + 1], "none", J.LINE, 6))
    g.append(F.poly(L[c:], "none", J.ALERT, 6) + F.poly(R[c:], "none", J.ALERT, 6))
    return g


def persp_stage(prev, st):
    s = []
    L, _R = _ps_rails()
    if _on(prev, st, "brake"):
        s.append(F.rect(140.0, 300.0, 480.0, 130.0, J.BG2, J.LINE, 4, rx=12))
        s.append(_tline(380.0, 342.0, "原因の文1", 26, J.TICK, "middle", 400))
        s.append(_tline(380.0, 394.0, "運転士のブレーキが遅れ", 30, INK, "middle", 440))
    if _on(prev, st, "curve"):
        # 🔧 geom_gap：札「制限 70km/h」がレールと枕木に重なった＝標識を左へ → 左上の「原因の文1」の箱に重なった＝下げる
        sx, sy = L[3][0] - 270, L[3][1] + 40
        s.append(F.line(sx, sy + 30, sx, sy + 110, J.LINE, 5))
        s.append(F.rect(sx - 46, sy - 34, 92, 64, J.BG2, INK, 4, rx=6) + _big(sx, sy + 14, str(PS_LIMIT), 40, INK))
        s.append(_tline(sx, sy + 150, "制限 70km/h", 28, INK, "middle", 220))
        cx, cy = PS_PATH[PS_CURVE + 1]
        s.append(_tline(1160.0, 316.0, "ここから曲線", 26, J.ALERT, "start", 260))
        s.append(_arrow(1400.0, 520.0, cx + 40, cy + 36, J.AMBER, 4, 18))
        s.append(_tline(1420.0, 532.0, "約116km/h で入る", 32, J.AMBER, "start", 360))
        s.append(F.rect(1260.0, 640.0, 440.0, 140.0, J.BG2, sc("rep"), 6, rx=14) + F.rect(1272.0, 652.0, 416.0, 116.0, "none", sc("rep"), 2, rx=10))
        s.append(_tline(1480.0, 714.0, PS_WORD, 42, sc("rep"), "middle", 400))
        s.append(_meter(1480.0 - METER_W / 2, 748.0, PS_WORD))
    return s


# ══════════════════════════════════════════════════════════
#  two_cards（c505）＝注意がそれた理由の2つの札（「など」つき＝R1 p.243）：1つ目＝電話を切られたと思う・車掌と指令の交信に注意／2つ目は次のカットの語り
# ══════════════════════════════════════════════════════════
TW2_WORD = "考えられる"


def two_cards_base(st0):
    return []


def two_cards_stage(prev, st):
    s = []
    if _on(prev, st, "frame"):
        s.append(_tline(800.0, 340.0, "理由の札（文2）", 30, INK, "end", 560))
        s.append(_tline(830.0, 340.0, TW2_WORD, 26, J.AMBER, "start", 200) + _meter(980.0, 330.0, TW2_WORD))
        s.append(F.rect(220.0, 390.0, 840.0, 380.0, J.BG2, INK, 4, rx=16) + _tline(260.0, 436.0, "1つ目", 28, J.AMBER, "start", 120))
        s.append(F.rect(1110.0, 390.0, 590.0, 380.0, J.BG2, J.LINE_DIM, 4, rx=16, dash="14 10")
                 + _tline(1150.0, 436.0, "2つ目", 28, J.AMBER, "start", 120) + _qmark(1405.0, 600.0, 90, J.LINE_DIM))
        s.append(_chip(1610.0, 820.0, "など", J.TICK, 26))
    if _on(prev, st, "a"):
        s.append(_phone(330.0, 524.0, 0.9, sc("sha")) + F.line(366.0, 488.0, 300.0, 560.0, J.ALERT, 5))
        s.append(_tline(400.0, 538.0, "電話を切られたと思う", 32, INK, "start", 620))
    if _on(prev, st, "b"):
        s.append(_radio(330.0, 690.0, 1.0, sc("shi")))
        s.append(_tline(400.0, 700.0, "車掌と指令の交信に注意", 32, INK, "start", 620))
    return s


# ══════════════════════════════════════════════════════════
#  flow3（c507）＝原因の3つの文の縦の流れ（上の背景から）：会社の運転士の管理〈可能性が考えられる〉→ 電話・注意のそれ〈考えられる〉→
#  ブレーキの遅れ・脱線〈推定される〉（R1 p.243）
# ══════════════════════════════════════════════════════════
FL3 = (("A", "会社の運転士の管理", "可能性が考えられる", (300.0, 430.0), "jr"), ("B", "電話・注意のそれ", "考えられる", (500.0, 600.0), "INK_W"),
       ("C", "ブレーキの遅れ・脱線", "推定される", (670.0, 770.0), "ALERT"))
FL3X = dict(x0=420.0, x1=1220.0, xw=1260.0)


def _fl3_col(c):
    return sc(c) if c in SRC else rc(c)


def flow3_base(st0):
    return []


def _fl3_box(i, body=True, dash=None):
    _k, t, word, (y0, y1), c = FL3[i]
    col = _fl3_col(c)
    g = [F.rect(FL3X["x0"], y0, FL3X["x1"] - FL3X["x0"], y1 - y0, J.BG2, col, 5, rx=14, dash=dash)]
    if body:
        ty = y0 + 52 if i == 0 else (y0 + y1) / 2 + 11
        g.append(_tline((FL3X["x0"] + FL3X["x1"]) / 2, ty, t, 32, col, "middle", 760))
    return "".join(g)


def _fl3_word(i):
    _k, _t, word, (y0, y1), _c = FL3[i]
    return _tline(FL3X["xw"], (y0 + y1) / 2 - 4, word, 26, J.AMBER, "start", 400) + _meter(FL3X["xw"], (y0 + y1) / 2 + 30, word)


def flow3_stage(prev, st):
    s = []
    xm = (FL3X["x0"] + FL3X["x1"]) / 2
    if _on(prev, st, "bc"):
        s += [_fl3_box(1), _fl3_box(2), _fl3_word(1), _fl3_word(2)]
        s.append(_arrow(xm, FL3[1][3][1] + 4, xm, FL3[2][3][0] - 4, J.LINE, 5, 20))
    if _on(prev, st, "slot"):
        s.append(_fl3_box(0, body=False, dash="14 10"))
        s.append(_tline(FL3X["x0"] - 20, 372.0, "3つ目：背景", 26, J.TICK, "end", 260))
    if _on(prev, st, "body"):
        s.append(_tline(xm, FL3[0][3][0] + 52, FL3[0][1], 32, _fl3_col(FL3[0][4]), "middle", 760))
        s.append(_tline(xm - 70, 408.0, "報告を怠る・偽ると", 24, INK, "end", 320))
        s.append(_arrow(xm - 56, 400.0, xm - 16, 400.0, J.AMBER, 4, 14))
        s.append(_tline(xm - 4, 408.0, "日勤教育・処分を重く", 24, INK, "start", 380))
    if _on(prev, st, "link"):
        s.append(_fl3_word(0))
        s.append(_arrow(xm, FL3[0][3][1] + 4, xm, FL3[1][3][0] - 4, _fl3_col("jr"), 5, 20))
        s.append(_tline(xm + 26, 474.0, "関与", 26, _fl3_col("jr"), "start", 120))
    return s


# ══════════════════════════════════════════════════════════
#  fan5（c510）＝この曲線を、わざと110km/hほどで通ろうとした可能性（R1 p.222）→「低いものと考えられる」→ 5つの理由の見出しの札（字を少なく）
# ══════════════════════════════════════════════════════════
F5_SUBJ = "この曲線を、わざと110km/hほどで通ろうとした可能性"
F5_WORD = "低いものと考えられる"
F5_TABS = ("ブレーキの使い方", "最高速度を守る", "危なさを知っていた", "アンケート", "目の高さ")
F5X = dict(xs=(300.0, 630.0, 960.0, 1290.0, 1620.0), w=300.0, y0=620.0, h=160.0)


def fan5_base(st0):
    return [F.rect(360.0, 310.0, 1200.0, 110.0, J.BG2, INK, 4, rx=14), _tline(CX, 378.0, F5_SUBJ, 32, INK, "middle", 1150)]


def fan5_stage(prev, st):
    s = []
    if _on(prev, st, "low"):
        s.append(F.rect(690.0, 450.0, 540.0, 100.0, J.BG2, sc("rep"), 6, rx=14))
        s.append(_tline(CX, 512.0, F5_WORD, 34, sc("rep"), "middle", 500))
        s.append(_meter(1250.0, 500.0, F5_WORD))
    if _on(prev, st, "tabs"):
        y0, w, h = F5X["y0"], F5X["w"], F5X["h"]
        for k, (x, t) in enumerate(zip(F5X["xs"], F5_TABS)):
            s.append(F.rect(x - w / 2 + 6, y0, w - 12, h, J.BG2, J.AMBER, 4, rx=12) + F.rect(x - 50, y0 - 20, 100, 24, J.AMBER, None, None, rx=6))
            s.append(_tline(x, y0 + 56, "①②③④⑤"[k], 34, J.AMBER, "middle", 80))
            s.append(_tline(x, y0 + 116, t, 24, INK, "middle", w - 36))
    return s


# ══════════════════════════════════════════════════════════
#  two_brakes（c511）＝2本のはしご（下から B1〜B8・非常＝国交省のハンドル位置図の並び・模式）：わざとなら＝直ちに強いブレーキ／実際＝B5 を約0.8秒（R1 p.222）
# ══════════════════════════════════════════════════════════
BK_STEPS = ("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "非常")
BK = dict(xs=(560.0, 1160.0), w=220.0, h=44.0, gap=6.0, y0=810.0)
BK_REAL = "B5"
BK_SEC = "約0.8秒"
BK_WORD = "考えられる"


def bk_cell(i):
    """i 段目の箱（下から）＝(上の y, 下の y)"""
    y1 = BK["y0"] - i * (BK["h"] + BK["gap"])
    return y1 - BK["h"], y1


def two_brakes_base(st0):
    g = []
    for x, title in zip(BK["xs"], ("わざとなら", "実際")):
        g.append(_tline(x, 300.0, title, 30, INK, "middle", 300))
        for i, t in enumerate(BK_STEPS):
            a, b = bk_cell(i)
            g.append(F.rect(x - BK["w"] / 2, a, BK["w"], BK["h"], J.BG2, J.LINE_DIM, 3, rx=6))
            g.append(_tline(x, b - 12, t, 22, J.TICK, "middle", 160))
    return g


def two_brakes_stage(prev, st):
    s = []
    xl, xr = BK["xs"]
    if _on(prev, st, "care"):
        s.append(_tline(xl, 340.0, "注意は運転に向いているはず", 22, J.TICK, "middle", 380))   # 🔧 門番 echo
    if _on(prev, st, "strong"):
        # 🔧 門番 layout：段の字を上から描き直すと字どうしが重なる＝枠だけ（字は基図のまま）
        a, _b = bk_cell(8)
        _a7, b7 = bk_cell(7)
        s.append(F.rect(xl - BK["w"] / 2 - 8, a - 8, BK["w"] + 16, b7 - a + 16, "none", J.ALERT, 6, rx=10))
        s.append(_tline(xl - BK["w"] / 2 - 20, a + 32, "直ちに強い", 26, J.ALERT, "end", 200))
        s.append(_tline(xl - BK["w"] / 2 - 20, a + 70, "ブレーキ", 26, J.ALERT, "end", 200))
    if _on(prev, st, "real"):
        i = BK_STEPS.index(BK_REAL)
        a, b = bk_cell(i)
        s.append(F.rect(xr - BK["w"] / 2 - 8, a - 8, BK["w"] + 16, BK["h"] + 16, "none", J.AMBER, 6, rx=10))
        s.append(_tline(xr + BK["w"] / 2 + 24, b - 8, BK_SEC, 34, J.AMBER, "start", 260))
        s.append(_tline(xr + BK["w"] / 2 + 24, 720.0, "この使い方の可能性は低い", 26, INK, "start", 400))
        s.append(_tline(xr + BK["w"] / 2 + 24, 768.0, BK_WORD, 24, J.AMBER, "start", 160) + _meter(xr + BK["w"] / 2 + 160, 760.0, BK_WORD))
    return s


# ══════════════════════════════════════════════════════════
#  band25（c512）＝時の線（9:18:05〜9:18:40・1秒＝40画素）の2本のピン：9:18:09ごろ B1（最高速度をある程度厳しく守ろうとした）／
#  9:18:35ごろ ブレーキを始めるべき位置（R1 p.222・p.221）→「約25秒前まで」
# ══════════════════════════════════════════════════════════
B25 = dict(x0=260.0, t0=5.0, k=40.0, y=560.0, x1=1660.0)
B25_A, B25_B, B25_GAP = 9, 35, 25
B25_WORD = "考えられる"


def b25_x(sec):
    return B25["x0"] + (sec - B25["t0"]) * B25["k"]


def band25_base(st0):
    g = [F.line(B25["x0"], B25["y"], B25["x1"], B25["y"], J.LINE, 5)]
    for k in range(5, 41, 5):
        g.append(F.line(b25_x(k), B25["y"] - 8, b25_x(k), B25["y"] + 8, J.TICK, 3))
    return g


def _pin(x, col, t, lab):
    y = B25["y"]
    return (F.line(x, y - 14, x, y - 82, col, 4) + F.circ(x, y, 14, col, J.BG, 3) + _tline(x, y - 104, t, 30, J.AMBER, "middle", 260)
            + _tline(x, y - 146, lab, 26, col, "middle", 300))


def band25_stage(prev, st):
    s = []
    y = B25["y"]
    if _on(prev, st, "a"):
        s.append(_pin(b25_x(B25_A), sc("rep"), "9:18:09ごろ", "B1 を使う"))
    if _on(prev, st, "keep"):
        s.append(F.rect(b25_x(B25_A), y + 24, b25_x(B25_B) - b25_x(B25_A), 30, J.ROLE["ship"], None, None, op=0.5, rx=6))
        s.append(_chip(820.0, 690.0, "最高速度 120km/h", J.ROLE["ship"], 28))
        s.append(_tline(1010.0, 700.0, "ある程度、厳しく守る", 28, INK, "start", 330))
        s.append(_tline(1010.0, 752.0, B25_WORD, 24, J.AMBER, "start", 160) + _meter(1150.0, 744.0, B25_WORD))
    if _on(prev, st, "b"):
        s.append(_pin(b25_x(B25_B), J.ALERT, "9:18:35ごろ", "始めるべき位置"))
        s.append(_bracket(b25_x(B25_A + 1), b25_x(B25_B), y - 34, J.AMBER, 4, up=False, tick=12))
        s.append(_tline((b25_x(B25_A + 1) + b25_x(B25_B)) / 2, y - 50, "約25秒前までは", 30, J.AMBER, "middle", 320))
    return s


# ══════════════════════════════════════════════════════════
#  survey（c514）＝アンケートの板（チェックの欄）→ 多くの運転士の答え：わざと制限より数十km/h高く？＝あり得ない（R1 p.222）
# ══════════════════════════════════════════════════════════
SV = dict(x0=260.0, x1=760.0, y0=330.0, y1=800.0, rows=(470.0, 540.0, 610.0, 680.0, 750.0))


def survey_base(st0):
    g = [F.rect(SV["x0"], SV["y0"], SV["x1"] - SV["x0"], SV["y1"] - SV["y0"], J.BG2, J.LINE, 4, rx=14),
         F.rect(430.0, 312.0, 160.0, 40.0, J.AMBER, None, None, rx=10), _tline(510.0, 412.0, "アンケート", 30, INK, "middle", 300)]
    for y in SV["rows"]:
        g.append(F.rect(300.0, y - 34, 32, 32, J.BG, J.LINE, 3, rx=4) + F.line(356.0, y - 18, 720.0, y - 18, J.LINE_DIM, 8))
    return g


def survey_stage(prev, st):
    s = []
    if _on(prev, st, "many"):
        for y in SV["rows"]:
            s.append(_check(316.0, y - 20, 14, J.AMBER))
        s.append(_tline(1250.0, 400.0, "多くの運転士の答え", 28, J.TICK, "middle", 400))
    if _on(prev, st, "ans"):
        s.append(F.rect(900.0, 450.0, 700.0, 300.0, J.BG2, INK, 4, rx=16))
        s.append(_tline(1250.0, 520.0, "わざと制限より数十km/h高く？", 28, INK, "middle", 640))
        s.append(_tline(1250.0, 670.0, "あり得ない", 72, J.ALERT, "middle", 600))
    return s


# ══════════════════════════════════════════════════════════
#  cab_note（c516）＝運転台の線画（窓・計器・2本の取っ手の棒＝手は描かない）と付箋：どのように急いでいても／わざとは、あり得ない／添えた運転士：多数（R1 p.194）
# ══════════════════════════════════════════════════════════
def cab_note_base(st0):
    g = [F.poly([(240.0, 340.0), (1040.0, 340.0), (1000.0, 560.0), (280.0, 560.0)], J.BG2, J.LINE, 5, close=True),
         F.line(640.0, 344.0, 640.0, 556.0, J.LINE, 6), F.rect(220.0, 590.0, 840.0, 200.0, J.BG2, J.LINE, 5, rx=12),
         F.circ(640.0, 690.0, 62.0, J.BG, J.LINE, 4), F.line(640.0, 690.0, 680.0, 650.0, J.AMBER, 5)]
    for x in (380.0, 900.0):
        g.append(F.line(x, 730.0, x, 640.0, J.LINE, 14) + F.circ(x, 630.0, 20.0, J.LINE, None))
    return g


def cab_note_stage(prev, st):
    s = []
    if _on(prev, st, "note"):
        s.append(F.poly([(1180.0, 360.0), (1720.0, 360.0), (1720.0, 720.0), (1680.0, 760.0), (1180.0, 760.0)], J.BG2, J.AMBER, 5, close=True))
        s.append(_tline(1450.0, 414.0, "アンケートに添えた一文", 24, J.TICK, "middle", 480))
    if _on(prev, st, "text"):
        s.append(_tline(1450.0, 504.0, "どのように急いでいても", 30, INK, "middle", 500))
        s.append(_tline(1450.0, 584.0, "わざとは、あり得ない", 34, J.AMBER, "middle", 500))
        s.append(_tline(1450.0, 690.0, "添えた運転士：多数", 26, J.TICK, "middle", 480))
    return s


# ══════════════════════════════════════════════════════════
#  two_signals（c518）＝「焦っていた」の場面（R1 p.220）：伊丹駅を出た直後 → 車掌が放送をしかける → すぐ運転士がブザーの合図
# ══════════════════════════════════════════════════════════
SG = dict(y=600.0, x0=300.0, x1=1620.0, a=760.0, b=1160.0)


def two_signals_base(st0):
    return []


def two_signals_stage(prev, st):
    s = []
    y = SG["y"]
    if _on(prev, st, "q"):
        s.append(_chip(CX, 340.0, "「焦っていた」？", J.AMBER, 32, ink=INK))
    if _on(prev, st, "line"):
        s.append(F.line(SG["x0"], y, SG["x1"], y, J.LINE, 5) + F.line(SG["x0"], y - 20, SG["x0"], y + 20, J.LINE, 5))
        s.append(_tline(SG["x0"], y + 60, "伊丹駅を出た直後", 28, INK, "start", 300))
    if _on(prev, st, "two"):
        s.append(F.circ(SG["a"], y, 10, sc("sha"), None) + F.circ(SG["b"], y, 10, J.AMBER, None))
        s.append(_speaker(SG["a"], y - 74, 1.0, sc("sha")) + _tline(SG["a"], y - 140, "車掌が放送をしかける", 28, sc("sha"), "middle", 320))
        s.append(_buzzer(SG["b"], y - 74, 1.0, J.AMBER) + _tline(SG["b"], y - 140, "運転士がブザーの合図", 28, J.AMBER, "middle", 320))
        s.append(_arrow(SG["a"] + 60, y - 74, SG["b"] - 70, y - 74, J.TICK, 4, 18))
        s.append(_tline((SG["a"] + SG["b"]) / 2, y + 56, "すぐに", 26, J.TICK, "middle", 120))
    return s


# ══════════════════════════════════════════════════════════
#  two_scenes（c521）＝2つのコマ（R1 p.220〜221 は分けて見る）：伊丹駅を出てからの加速／曲線の手前のブレーキの遅れ
# ══════════════════════════════════════════════════════════
def two_scenes_base(st0):
    return []


def two_scenes_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_chip(CX, 330.0, "注意は、いつ それた？", J.AMBER, 30, ink=INK))
    if _on(prev, st, "a"):
        s.append(F.rect(200.0, 400.0, 700.0, 380.0, J.BG2, J.ROLE["ship"], 5, rx=16))
        s.append(_tline(550.0, 452.0, "伊丹駅を出てからの加速", 28, INK, "middle", 640))
        s.append(F.poly([(260.0, 730.0), (420.0, 690.0), (580.0, 620.0), (760.0, 540.0)], "none", J.ROLE["ship"], 7))
        s.append(_arrow(740.0, 549.0, 840.0, 505.0, J.ROLE["ship"], 7, 26) + _train_block(280.0, 400.0, 740.0, 30.0))
    if _on(prev, st, "b"):
        s.append(F.rect(1020.0, 400.0, 700.0, 380.0, J.BG2, J.ROLE["company"], 5, rx=16))
        s.append(_tline(1370.0, 452.0, "曲線の手前：ブレーキが遅い", 28, INK, "middle", 640))   # 🔧 門番 echo
        s.append(F.line(1080.0, 640.0, 1660.0, 640.0, J.LINE, 4))
        s.append(F.line(1200.0, 600.0, 1200.0, 680.0, INK, 4) + F.line(1520.0, 600.0, 1520.0, 680.0, J.ALERT, 6))
        s.append(F.rect(1200.0, 626.0, 320.0, 28.0, J.ALERT, None, None, op=0.4))
        s.append(_tline(1360.0, 718.0, "遅れ", 28, J.ALERT, "middle", 120))
        s.append(_chip(CX, 830.0, "分けて見る", J.TICK, 26, ink=INK))
    return s


# ══════════════════════════════════════════════════════════
#  weaker（c523）＝言い方の強さの縦の目盛り（4段）：注意がそれた＝考えられる → その理由（日勤教育を心配・言い訳などを考えていた）＝可能性も考えられる（R1 p.220）
# ══════════════════════════════════════════════════════════
WK_RUNGS = ("認められる", "推定される", "考えられる", "可能性が考えられる")
WK = dict(x=380.0, ys=(380.0, 500.0, 620.0, 740.0), card=620.0)
WK_A, WK_B = "考えられる", "可能性も考えられる"


def weaker_base(st0):
    g = [F.line(WK["x"], WK["ys"][0] - 30, WK["x"], WK["ys"][-1] + 30, J.LINE, 6)]
    for y, w in zip(WK["ys"], WK_RUNGS):
        g.append(F.line(WK["x"] - 16, y, WK["x"] + 16, y, J.LINE, 5))
        g.append(_tline(WK["x"] - 30, y + 9, w, 22, J.TICK, "end", 280))
        g.append(_meter(WK["x"] + 34, y, w, 18.0, 5.0))
    return g


def weaker_stage(prev, st):
    s = []
    x = WK["card"]
    ya, yb = WK["ys"][WK_RUNGS.index(WK_A)], WK["ys"][3]
    if _on(prev, st, "a"):
        s.append(_arrow(x - 24, ya, x - 70, ya, INK, 4, 16))
        s.append(F.rect(x, ya - 40, 560.0, 80.0, J.BG2, INK, 4, rx=12) + _tline(x + 280, ya + 11, "注意が運転からそれた", 30, INK, "middle", 520))
        s.append(_arrow(x + 600, ya + 10, x + 600, yb - 34, J.AMBER, 5, 20))
        s.append(_tline(x + 630, (ya + yb) / 2 + 10, "さらに弱い", 28, J.AMBER, "start", 200))
    if _on(prev, st, "b"):
        s.append(_arrow(x - 24, yb, x - 70, yb, J.AMBER, 4, 16))
        s.append(F.rect(x, yb - 54, 560.0, 108.0, J.BG2, J.AMBER, 4, rx=12))
        s.append(_tline(x + 280, yb - 14, "日勤教育を心配", 26, INK, "middle", 520))
        s.append(_tline(x + 280, yb + 30, "言い訳などを考えていた", 28, INK, "middle", 520))
        s.append(_tline(x + 600, yb + 10, WK_B, 28, J.AMBER, "start", 330))
    return s


# ══════════════════════════════════════════════════════════
#  objects（c525）＝物の線画：運転室の床の赤鉛筆／右手の手袋（着けていない＝見られる）→ 交信をメモしようとした？＝可能性も考えられる（R1 p.221〜222）。手は描かない
# ══════════════════════════════════════════════════════════
OB_WORD = "可能性も考えられる"


def _pencil():
    x0, y0 = 380.0, 700.0
    ux, uy = 340.0 / 345.2, -60.0 / 345.2
    nx, ny = -uy, ux
    hw = 13.0

    def p(s_, k):
        return (x0 + ux * s_ + nx * hw * k, y0 + uy * s_ + ny * hw * k)
    body = [p(0, 1), p(290, 1), p(290, -1), p(0, -1)]
    tip = [p(290, 1), p(340, 0), p(290, -1)]
    lead = [p(326, 0.28), p(340, 0), p(326, -0.28)]
    return F.poly(body, J.ALERT, J.BG, 3, close=True) + F.poly(tip, J.DOC, J.BG, 3, close=True) + F.poly(lead, "#2a2f33", None, close=True)


def _glove():
    g = [F.rect(1170.0, 560.0, 160.0, 160.0, J.BG2, INK, 5, rx=34)]
    for x, h in ((1176.0, 104.0), (1214.0, 124.0), (1252.0, 118.0), (1290.0, 96.0)):
        g.append(F.rect(x, 560.0 - h + 20, 34.0, h, J.BG2, INK, 5, rx=17))
    g.append(F.poly([(1172.0, 684.0), (1114.0, 618.0), (1096.0, 630.0), (1098.0, 650.0), (1158.0, 722.0)], J.BG2, INK, 5, close=True))
    g.append(F.rect(1180.0, 716.0, 140.0, 44.0, J.BG2, INK, 5, rx=8))
    # 🔧 試し焼き 40246394718：手の形に見えた＝甲の縫い目と袖口の筋（手袋の印）
    for x in (1214.0, 1252.0, 1290.0):
        g.append(F.line(x, 596.0, x, 664.0, J.LINE, 3, dash="6 6"))
    for x in range(1196, 1320, 16):
        g.append(F.line(float(x), 724.0, float(x), 752.0, J.LINE_DIM, 3))
    return "".join(g)


def objects_base(st0):
    return [F.line(200.0, 730.0, 900.0, 730.0, J.LINE, 4)]


def objects_stage(prev, st):
    s = []
    if _on(prev, st, "things"):
        s.append(_pencil() + _tline(550.0, 792.0, "赤鉛筆：運転室に落ちていた", 26, INK, "middle", 560))
        s.append(_glove() + _tline(1250.0, 818.0, "右手の手袋：着けていない（見られる）", 26, INK, "middle", 600))
    if _on(prev, st, "memo"):
        s.append(_chip(CX, 350.0, "メモを取ろうとした？", J.AMBER, 30, ink=INK))   # 🔧 門番 echo
        s.append(_tline(CX - 20, 436.0, OB_WORD, 26, J.AMBER, "end", 330) + _meter(CX + 10, 428.0, OB_WORD))
    return s


# ══════════════════════════════════════════════════════════
#  cycle（c527）＝日数・中身を決めた規定は無し（✕）→ 輪の流れ（乗務から外す → 書く → 乗務へ戻る）・期間と中身は職場の長が決める（会社の説明＝R1 p.63）
# ══════════════════════════════════════════════════════════
CY = dict(cx=1240.0, cy=560.0, r=210.0)
CY_NODES = ((-90.0, "乗務から外す"), (30.0, "書く"), (150.0, "乗務へ戻る"))


def cycle_base(st0):
    return []


def cycle_stage(prev, st):
    s = []
    cx, cy, r = CY["cx"], CY["cy"], CY["r"]
    if _on(prev, st, "rule"):
        s.append(F.rect(200.0, 360.0, 320.0, 360.0, J.BG2, J.LINE, 4, rx=10, dash="14 10"))
        for k in range(4):
            s.append(F.line(240.0, 420.0 + 50 * k, 480.0, 420.0 + 50 * k, J.LINE_DIM, 8))
        s.append(_xmark(360.0, 520.0, 70, J.ALERT))
        s.append(_tline(360.0, 664.0, "無し", 40, J.ALERT, "middle", 200))
        s.append(_tline(360.0, 770.0, "日数・中身を決めた規定", 26, J.TICK, "middle", 400))
    if _on(prev, st, "loop"):
        for a0, a1 in ((-60.0, 0.0), (60.0, 120.0), (180.0, 240.0)):
            p = _arcpts(cx, cy, r, r, a0, a1, 12)
            s.append(F.poly(p[:-1], "none", J.AMBER, 5) + _arrow(p[-3][0], p[-3][1], p[-1][0], p[-1][1], J.AMBER, 5, 20))
        for a, t in CY_NODES:
            x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            s.append(_chip(x, y, t, INK, 26))
        s.append(_tline(cx, cy - 6, "期間と中身は", 26, INK, "middle", 300))
        s.append(_tline(cx, cy + 40, "職場の長が決める", 28, sc("jr"), "middle", 320))
        s.append(_chip(cx, 830.0, "会社の説明", sc("jr"), 26))
    return s


# ══════════════════════════════════════════════════════════
#  cal18（c528）＝3枚の暦（この運転士の日勤教育＝3件・あわせて18日＝R1 p.49・p.220）：2002年5月 4日間・2003年8月 1日間・2004年6月 13日間。
#  理由の中身は書かない（台本 §1-4・§5）・升は日数だけ（日付の位置は模式）
# ══════════════════════════════════════════════════════════
C18 = (((2002, 5), 4, "AMBER"), ((2003, 8), 1, "ship"), ((2004, 6), 13, "company"))
C18X = dict(xs=(420.0, 960.0, 1500.0), w=440.0, y0=350.0, y1=740.0, s=50.0, gap=10.0, per=6)
C18_TOTAL, C18_N = 18, 3


def cal18_base(st0):
    return []


def cal18_stage(prev, st):
    s = []
    if _on(prev, st, "all"):
        for ((y_, m_), n, c), x in zip(C18, C18X["xs"]):
            col = rc(c)
            w = C18X["w"]
            s.append(F.rect(x - w / 2, C18X["y0"], w, C18X["y1"] - C18X["y0"], J.BG2, col, 5, rx=14))
            s.append(F.line(x - w / 2 + 16, C18X["y0"] + 78, x + w / 2 - 16, C18X["y0"] + 78, col, 3))
            s.append(F.circ(x - 90, C18X["y0"], 10, J.BG, J.LINE, 4) + F.circ(x + 90, C18X["y0"], 10, J.BG, J.LINE, 4))
            s.append(_tline(x, C18X["y0"] + 56, f"{y_}年{m_}月", 32, col, "middle", w - 40))
            for k in range(n):
                r, q = divmod(k, C18X["per"])
                bx = x - (C18X["per"] * C18X["s"] + (C18X["per"] - 1) * C18X["gap"]) / 2 + q * (C18X["s"] + C18X["gap"])
                by = C18X["y0"] + 104 + r * (C18X["s"] + C18X["gap"])
                s.append(F.rect(bx, by, C18X["s"], C18X["s"], col, None, None, rx=6))
            s.append(_tline(x, C18X["y1"] - 40, f"{n}日間", 34, INK, "middle", w - 40))
        s.append(_tline(CX, 816.0, f"{C18_N}回・あわせて{C18_TOTAL}日間", 34, J.AMBER, "middle", 600))
    return s


# ══════════════════════════════════════════════════════════
#  lens（c529）＝日勤教育 → 虫めがね（受け取り方）→「効果のないペナルティ」（技術の向上に／一部の運転士にとって＝R1 p.204）・考えられる
# ══════════════════════════════════════════════════════════
LN_WORD = "考えられる"


def lens_base(st0):
    return []


def lens_stage(prev, st):
    s = []
    if _on(prev, st, "box"):
        s.append(F.rect(220.0, 450.0, 380.0, 200.0, J.BG2, sc("jr"), 5, rx=14) + _tline(410.0, 562.0, "日勤教育", 36, sc("jr"), "middle", 340))
        s.append(_tline(410.0, 410.0, "一部の運転士にとって", 26, J.TICK, "middle", 380))
    if _on(prev, st, "seen"):
        s.append(_arrow(610.0, 550.0, 720.0, 550.0, J.LINE, 4, 16))
        s.append(F.circ(820.0, 540.0, 80.0, J.BG2, J.ROLE["ship"], 8) + F.line(876.0, 596.0, 936.0, 656.0, J.ROLE["ship"], 14))
        s.append(_tline(820.0, 680.0 + 40, "受け取り方", 24, J.ROLE["ship"], "middle", 200))
        s.append(_arrow(910.0, 540.0, 1066.0, 540.0, J.LINE, 4, 16))
        s.append(F.rect(1080.0, 420.0, 620.0, 240.0, J.BG2, J.ALERT, 5, rx=16))
        s.append(_tline(1390.0, 478.0, "技術の向上に", 26, J.TICK, "middle", 560))
        s.append(_tline(1390.0, 556.0, "効果のないペナルティ", 40, INK, "middle", 580))
        s.append(_tline(1390.0, 618.0, "と受け取られた", 26, J.TICK, "middle", 560))
        s.append(_tline(1300.0, 720.0, LN_WORD, 26, J.AMBER, "start", 160) + _meter(1450.0, 712.0, LN_WORD))
    return s


# ══════════════════════════════════════════════════════════
#  qcards（c530）＝別の運転士たちの2つの口述（R1 p.68）：「見せしめのようだった」／「自分のためになった」
# ══════════════════════════════════════════════════════════
QC = (("見せしめのようだった", "ALERT", (220.0, 900.0)), ("自分のためになった", "OK", (1020.0, 1700.0)))


def qcards_base(st0):
    return [_tline(CX, 336.0, "報告書に載る口述", 28, J.TICK, "middle", 800)]


def _qc(i):
    t, c, (x0, x1) = QC[i]
    col = rc(c)
    return (F.rect(x0, 420.0, x1 - x0, 300.0, J.BG2, col, 5, rx=18) + F.txt(x0 + 34, 500.0, "「", 70, col, "Noto", "start")
            + _tline((x0 + x1) / 2 + 10, 592.0, t, 40, INK, "middle", x1 - x0 - 120) + F.txt(x1 - 34, 690.0, "」", 70, col, "Noto", "end"))


def qcards_stage(prev, st):
    s = []
    if _on(prev, st, "l"):
        s.append(_qc(0))
    if _on(prev, st, "r"):
        s.append(_qc(1))
    return s


# ══════════════════════════════════════════════════════════
#  evidence（c531）＝根拠の線：運転士本人の言葉＝無い／ほかの運転士たちの話（言い訳を考えながら運転した＝R1 p.69・p.178）→ 推し量る →
#  言い訳などを考えていた（可能性も考えられる）
# ══════════════════════════════════════════════════════════
EV_WORD = "可能性も考えられる"


def evidence_base(st0):
    return []


def evidence_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(F.rect(200.0, 390.0, 440.0, 220.0, J.BG2, J.LINE, 4, rx=18, dash="14 10"))
        s.append(_tline(420.0, 366.0, "運転士本人の言葉", 26, J.TICK, "middle", 400))
        s.append(F.rect(660.0, 660.0, 600.0, 140.0, J.BG2, INK, 4, rx=14))
        s.append(_tline(960.0, 718.0, "言い訳などを考えていた", 32, INK, "middle", 560))
        s.append(_tline(940.0, 770.0, EV_WORD, 24, J.AMBER, "end", 280) + _meter(960.0, 762.0, EV_WORD))
    if _on(prev, st, "none"):
        s.append(_tline(420.0, 528.0, "無い", 64, J.ALERT, "middle", 300))
    if _on(prev, st, "others"):
        s.append(F.rect(1200.0, 380.0, 480.0, 150.0, J.BG2, J.AMBER, 4, rx=14))   # 🔧 geom_gap：後ろに重ねた札の縁が字にかかった＝1枚に
        s.append(_tline(1440.0, 424.0, "ほかの運転士たちの話", 24, J.TICK, "middle", 440))
        s.append(_tline(1440.0, 480.0, "言い訳を考えながら運転した", 28, INK, "middle", 440))
        s.append(_arrow(1330.0, 580.0, 1210.0, 650.0, J.AMBER, 5, 20))
        s.append(_tline(1360.0, 630.0, "ここから推し量る", 26, J.AMBER, "start", 300))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表（mech24 と同じ作り）
# ══════════════════════════════════════════════════════════
def _v(lab, fields, base, stage, parts=None):
    d = dict(lab=lab, fields={f_: ONOFF for f_ in fields}, base=base, stage=stage)
    if parts:
        d["parts"] = parts
    return d


VIEWS = dict(
    route=_v("路線（駅の並び）", ("dir", "num"), route_base, route_stage),
    tt_col=_v("その朝の時刻表", ("rows", "late"), tt_col_base, tt_col_stage),
    delay_bars=_v("駅ごとの遅れ", ("b0", "b12", "b3"), delay_bars_base, delay_bars_stage),
    speedo=_v("速度計の表示と記録", ("rec1", "rec2", "show"), speedo_base, speedo_stage),
    overrun=_v("上から見た伊丹駅の行き過ぎ", ("over", "back"), overrun_base, overrun_stage, overrun_parts),
    two_cabs=_v("横から見た7両の列車", ("call", "buzz"), two_cabs_base, two_cabs_stage),
    glass=_v("横から見た7両目の運転室", ("say", "hang"), glass_base, glass_stage, glass_parts),
    ruler_v=_v("行き過ぎの物差し", ("say", "heard"), ruler_v_base, ruler_v_stage),
    ring2=_v("2つの遅れ", ("say", "rec"), ring2_base, ring2_stage),
    tags4=_v("数と出どころの札", ("t1", "t2", "t3", "t4"), tags4_base, tags4_stage),
    matrix=_v("出どころで並べる", ("r1", "r2", "head"), matrix_base, matrix_stage),
    hscale=_v("速度の目盛り", ("rec", "limit"), hscale_base, hscale_stage),
    tt_band=_v("交信の秒（付図24 の帯）", ("e1", "e2"), tt_band_base, tt_band_stage),
    zone=_v("区間と復唱", ("zone", "time"), zone_base, zone_stage),
    clockfan=_v("復唱の秒", ("fan", "sweep"), clockfan_base, clockfan_stage, clockfan_parts),
    crossing=_v("上から見た伊丹駅の先", ("doubt", "ask"), crossing_base, crossing_stage),
    two_ribbons=_v("ブレーキの遅れの2つの推算", ("a", "b"), two_ribbons_base, two_ribbons_stage),
    tiles=_v("惰性の長さ（1マス＝約1秒）", ("fill",), tiles_base, tiles_stage, tiles_parts),
    clues=_v("手がかりの札", ("q", "two"), clues_base, clues_stage),
    section=_v("後ろから見た2両目の断面", ("crush", "gone"), section_base, section_stage, section_parts),
    plaques=_v("2つの数の板", ("p1", "p2"), plaques_base, plaques_stage),
    split_box=_v("会社の書き方", ("r1", "r2"), split_box_base, split_box_stage),
    chapters3=_v("兵庫県の検証", ("three", "out"), chapters3_base, chapters3_stage),
    doors3=_v("3つの入口", ("q", "words"), doors3_base, doors3_stage),
    stairs4=_v("言い方の4段", ("s12", "s3", "s4"), stairs4_base, stairs4_stage),
    persp=_v("運転席の高さから見た曲線の入口", ("brake", "curve"), persp_base, persp_stage),
    two_cards=_v("それた理由の2つの札", ("frame", "a", "b"), two_cards_base, two_cards_stage),
    flow3=_v("3つの文のつながり", ("bc", "slot", "body", "link"), flow3_base, flow3_stage),
    fan5=_v("5つの理由", ("low", "tabs"), fan5_base, fan5_stage),
    two_brakes=_v("理由1：ブレーキの使い方", ("care", "strong", "real"), two_brakes_base, two_brakes_stage),
    band25=_v("理由2：最高速度を守る", ("a", "keep", "b"), band25_base, band25_stage),
    survey=_v("理由4：運転士へのアンケート", ("many", "ans"), survey_base, survey_stage),
    cab_note=_v("アンケートに添えた一文", ("note", "text"), cab_note_base, cab_note_stage),
    two_signals=_v("「焦っていた」の場面", ("q", "line", "two"), two_signals_base, two_signals_stage),
    two_scenes=_v("2つの場面", ("q", "a", "b"), two_scenes_base, two_scenes_stage),
    weaker=_v("言い方の強さの目盛り", ("a", "b"), weaker_base, weaker_stage),
    objects=_v("運転室の物", ("things", "memo"), objects_base, objects_stage),
    cycle=_v("日勤教育の流れ", ("rule", "loop"), cycle_base, cycle_stage),
    cal18=_v("この運転士の日勤教育", ("all",), cal18_base, cal18_stage),
    lens=_v("日勤教育の受け取られ方", ("box", "seen"), lens_base, lens_stage),
    qcards=_v("2つの口述", ("l", "r"), qcards_base, qcards_stage),
    evidence=_v("根拠の線", ("q", "none", "others"), evidence_base, evidence_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
# 原文の値・欄・項目の写し（左上に「模式」を付けない）
NOT_SCHEMATIC = ("tt_col", "delay_bars", "ruler_v", "ring2", "tags4", "matrix", "hscale", "tt_band", "clockfan", "two_ribbons", "tiles",
                 "plaques", "split_box", "stairs4", "fan5", "band25", "cal18", "qcards")
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
                raise ValueError(f"m25：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m25：{f_}={v!r} は知らない値（{fields[f_]}）")
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


def m25(view, steps, start=None, rel=(), note="", src=""):
    """25本目の図解。view は VIEWS の見え方。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m25：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view not in NOT_SCHEMATIC and "模式" not in note:
        raise ValueError("m25：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    seq = [st0] + states
    per = [parts_of(view, s) for s in seq]
    # 焼く側（build_jiko._draw_anim）は部品の線の太さ w を必ず数で読む（24本目 ⑤b-5 の試し焼き 39884985410）＝型の入口で止める
    for p in per[0]:
        if not isinstance(p.get("w", 4), (int, float)):
            raise ValueError(f"m25：{view} の部品 {p.get('id')} の線の太さ w={p.get('w')!r}（数で書く・線なしでも 2 など）")
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
    f.mech = dict(kind="m25", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=shapes, lab=lab, note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states), texts_all=svg_texts(body))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M25）
# ══════════════════════════════════════════════════════════
def _on_any(allst, f_):
    return any(s.get(f_) == "on" for s in allst)


# 見え方ごとに、画面に出る出どころの鍵（同じ画面で色が重ならないか＝門番）と強さの言葉
VIEW_SRC = dict(tags4=tuple(k for k, *_r in TG4), matrix=MX_COLS, plaques=tuple(k for k, *_r in PQ), ring2=("sha", "rep"),
                tt_band=("shi", "sha"), zone=("shi",), clockfan=("shi",), crossing=("shi",), speedo=("rep",), hscale=("rep",),
                split_box=("jr",), chapters3=("hy",), two_cabs=("sha",), glass=("sha",), ruler_v=("sha",), two_cards=("sha", "shi"),
                two_signals=("sha",), flow3=("jr",), cycle=("jr",), lens=("jr",), clues=("rep",), persp=("rep",), fan5=("rep",),
                band25=("rep",), two_ribbons=("rep",))
VIEW_WORDS = dict(doors3=DR3, stairs4=tuple(w for w, _m in ST4), persp=(PS_WORD,), two_cards=(TW2_WORD,), flow3=tuple(w for *_x, w, _y, _c in FL3),
                  fan5=(F5_WORD,), two_brakes=(BK_WORD,), band25=(B25_WORD,), weaker=WK_RUNGS + (WK_A, WK_B), objects=(OB_WORD,),
                  lens=(LN_WORD,), evidence=(EV_WORD,))


def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst], src={k: tuple(v) for k, v in SRC.items()}, lv=dict(LV),
               vsrc=tuple(VIEW_SRC.get(view, ())), words=tuple(VIEW_WORDS.get(view, ())))
    if view == "route":
        out.update(st=RT_ST, xs=tuple(rt_x(i) for i in range(8)), curve=rt_curve_x(), no=RT_NO)
    elif view == "tt_col":
        out.update(rows=TT_ROWS, ys=tuple(tt_y(i) for i in range(len(TT_ROWS))))
    elif view == "delay_bars":
        out.update(rows=tuple((n, k, v, lab) for n, k, v, lab, _c in DB_ROWS), tops=tuple(db_top(r[2]) for r in DB_ROWS), y0=DB["y0"], k=DB["k"],
                   t=DB_T, cols=tuple(rc(r[4]).lower() for r in DB_ROWS))
    elif view == "speedo":
        out.update(show=SP_SHOW, rec=SP_REC, lit=sp_lit(), n=SP["n"], vmax=SP["vmax"])
    elif view == "overrun":
        fin = [p["dx"] for p in parts_of("overrun", allst[-1])][0]
        mid = parts_of("overrun", allst[1])[0]["dx"] if len(allst) > 1 else 0.0
        out.update(over=OV_OVER, back=OV_BACK, k=OV["k"], stop=OV["stop"], x_in=OV["x_in"], dx_over=mid, dx_back=fin, t=OV_T)
    elif view == "ruler_v":
        out.update(say=RV_SAY, think=RV_THINK, heard=RV_HEARD, y0=RV["y0"], k=RV["k"], ys=(rv_y(RV_SAY), rv_y(RV_THINK[0]), rv_y(RV_THINK[1]), rv_y(RV_HEARD)))
    elif view == "ring2":
        out.update(say=RG_SAY, rec=RG_REC, full=RG["full"], angs=(rg_ang(RG_SAY) - rg_ang(0), rg_ang(RG_REC) - rg_ang(0)))
    elif view == "tags4":
        out.update(tags=tuple((k, n, tuple(f)) for k, n, f in TG4), xs=TGX["xs"])
    elif view == "matrix":
        out.update(cols=MX_COLS, rows=MX_ROWS)
    elif view == "hscale":
        out.update(mx=HS_MAX, rec=HS_REC, show=HS_SHOW, t=HS_T, x0=HS["x0"], v0=HS["v0"], k=HS["k"], xmax=hs_x(HS_MAX),
                   xrec=tuple(hs_x(v) for v in HS_REC))
    elif view == "tt_band":
        out.update(ev=tuple((k, a, b) for k, _l, a, b in TB_EV), xs=tuple((tb_x(a), tb_x(b)) for _k, _l, a, b in TB_EV), x0=TB["x0"], k=TB["k"])
    elif view == "zone":
        out.update(sec=ZN_SEC, zone=ZN["zone"], curve=ZN["xc"])
    elif view == "clockfan":
        rots = tuple(p["rot"] for s in allst for p in parts_of("clockfan", s))
        out.update(a=CF_A, b=CF_B, hm=CF_HM, rots=rots)
    elif view == "two_ribbons":
        out.update(a=TRB_A, b=TRB_B, xa=trb_x0(TRB_A[0]), xb=trb_x0(TRB_B[0]), xe=TRB["xe"], k=TRB["k"])
    elif view == "tiles":
        out.update(b1=TL_B1, coast=TL_COAST)
    elif view == "section":
        outer = [p["pts"] for p in parts_of("section", allst[-1]) if p["id"] == "body"][0]
        inner0 = [p["pts"] for p in parts_of("section", allst[0]) if p["id"] == "room"][0]
        inner1 = [p["pts"] for p in parts_of("section", allst[-1]) if p["id"] == "room"][0]

        def area(p):
            return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2.0
        out.update(outer=outer, ratio=area(inner1) / area(inner0))
    elif view == "plaques":
        out.update(items=tuple((k, n) for k, n, _f in PQ))
    elif view == "split_box":
        out.update(rows=SB_ROWS)
    elif view == "chapters3":
        out.update(boxes=tuple(t for t, _c in CH3))
    elif view == "doors3":
        out.update(doors=DR3)
    elif view == "stairs4":
        out.update(steps=ST4, tops=tuple(st4_box(i)[1] for i in range(4)))
    elif view == "persp":
        out.update(limit=PS_LIMIT, v=PS_V, word=PS_WORD)
    elif view == "fan5":
        out.update(subj=F5_SUBJ, word=F5_WORD, tabs=F5_TABS)
    elif view == "flow3":
        out.update(flow=tuple((t, w) for _k, t, w, _y, _c in FL3), ys=tuple(y for *_x, y, _c in FL3))
    elif view == "two_brakes":
        out.update(steps=BK_STEPS, real=BK_REAL, sec=BK_SEC)
    elif view == "band25":
        out.update(a=B25_A, b=B25_B, gap=B25_GAP, xa=b25_x(B25_A), xb=b25_x(B25_B))
    elif view == "weaker":
        out.update(rungs=WK_RUNGS, a=WK_A, b=WK_B)
    elif view == "cal18":
        out.update(items=C18, total=C18_TOTAL, n=C18_N)
    elif view == "qcards":
        out.update(items=tuple(t for t, _c, _x in QC))
    return out
