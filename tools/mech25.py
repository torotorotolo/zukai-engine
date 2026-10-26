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
  🆕 ⑤b-6（2026-10-26）＝第5〜10章の図解 57カット（各カット1つの見え方＝名は前の42と重ねない）
  第5章  speed_step（c606）・push_out（c608）・hbars6（c609）・strip43（c610）・cog2（c611）・ramp（c612）・ceiling（c614）・sort2（c616）・
         cant（c617）・coupler（c619）・empty_slot（c623）
  第6章  dots_co（c701）・donut（c705）・order3（c708）・tl_plan（c710 年表・横）・spill（c712）・signal_date（c714）・drop2（c717）・
         kk_page（c718）・receipt（c720）・trim3（c722）・scale2（c725）・jr_words（c727）
  第7章  tearoff（c801 暦）・stretch（c803）・flow_fan（c807 流れ）・hourglass（c809）・book_seat（c811）・kengi3（c812）
  第8章  plates4（c901）・duty（c903）・verdict（c904）・word_swap（c906）・bypass（c908）・relay3（c909）・scatter（c911）・stamps4（c914）・
         podium（c915）・stamps2（c916）・bench（c917）・nested（c918）・wall（c922）
  第9章  role_lines（ca03）・ring12（ca04）・links6（ca06）・tl_leak（ca07 年表・縦）・handover（ca08）・bundle（ca09）・jyanken（ca12）・
         meeting（ca15）・waveform（ca16）・open_book（ca20）・five_slips（ca22）
  第10章 answer（cb06）・two_causes（cb08）・stones3（cb09）・batteries（cb10）
  🔴 出どころの色に2つ（⑤b-6）：裁判所（神戸地裁・最高裁）＝LINE（章の線の色）・検証報告書（2011年）＝SUB（章に染まらない白）＝どちらも名の札と一緒に
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
    # 🆕 ⑤b-6（2026-10-26・第8〜9章）：使っている7色と重ねない・新しい色の値は足さない＝名の札と一緒に出す
    ct=("裁判所", "LINE"),            # 神戸地裁の判決（2012年1月・2013年9月）・最高裁の決定（2017年6月）＝章の線の色
    kv=("検証報告書", "SUB"),         # 検証報告書（2011年・運輸安全委員会の検証メンバー・チーム）＝章の色に染まらない白
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
#  🆕 ⑤b-6（2026-10-26）：第5〜10章の図解 57カット（c6 11・c7 12・c8 6・c9 13・ca 11・cb 4）
#  🔴 出どころの色に2つ足した（SRC の ct・kv＝新しい色の値は無し）：裁判所＝LINE（章の線の色）・検証報告書＝SUB（章に染まらない白）。
#     国会（2023年の法務省・鉄道局長・国土交通大臣〈当時〉の答弁も）＝紫 city のまま。国（国土交通省の措置）は出どころの札を出さない（出典の行だけ）
#  🔴 同じ型は全編で2回まで・続けない：棒 c211（縦・秒）↔c609（横・km/h）／暦 c528（3枚の月の暦）↔c801（日めくりと破った頁）／
#     流れ c507（縦）↔c807（横の枝分かれ）／年表 c710（横・月）↔ca07（縦・月）。案C の F4・F5 と ⑤b-5 の42とも別の絵
#  🔴 画面の字は語りの複写にしない（門番 echo＝12字以上で一続きの一致 0.72）＝引用は2つ以上の字に割る（「予見できた」＋「とは認められない」）
# ══════════════════════════════════════════════════════════
def _ym(y, m, d=1):
    """暦の年月日 → 年（小数・月の頭＝m−1）。"""
    return y + (m - 1 + (d - 1) / 31.0) / 12.0


def _ctr(cx, cy, t, cap=28, col=None, mw=700, fam="Noto"):
    """字の真ん中の高さを cy に。"""
    return _tline(cx, cy + cap * 0.36, t, cap, col, "middle", mw, fam)


def _stag(cx, cy, key, t=None, cap=24):
    """出どころの名の札（縁と字は出どころの色）。"""
    return _chip(cx, cy, t or SRC[key][0], sc(key), cap)


def _apts(x0, y0, x1, y1, w=14.0, head=34.0, hw=24.0):
    """矢印の形（7点＝動く部品の pts にも使う）。"""
    a = math.atan2(y1 - y0, x1 - x0)
    c, s = math.cos(a), math.sin(a)
    L = math.hypot(x1 - x0, y1 - y0)

    def p(u, v):
        return (x0 + u * c - v * s, y0 + u * s + v * c)
    return [p(0, -w / 2), p(L - head, -w / 2), p(L - head, -hw), p(L, 0), p(L - head, hw), p(L - head, w / 2), p(0, w / 2)]


def _rot(pts, cx, cy, deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def _bldg(x0, y0, x1, y1, col, nx=3, ny=3):
    """建物の印（名とロゴは描かない）＝外形と窓の升。"""
    g = [F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, col, 5, rx=6)]
    ww, wh = (x1 - x0) / (nx * 2 + 1), (y1 - y0 - 40) / (ny * 2 + 1)
    for i in range(nx):
        for j in range(ny):
            g.append(F.rect(x0 + ww * (2 * i + 1), y0 + 20 + wh * (2 * j + 1), ww, wh, "none", col, 3))
    return "".join(g)


def _doc(x0, y0, w, h, col, lines=3, sw=4):
    """書類の印（紙と字の行の灰の線＝字は書かない）。"""
    g = [F.rect(x0, y0, w, h, J.BG2, col, sw, rx=6)]
    for i in range(lines):
        yy = y0 + h * (i + 1) / (lines + 1)
        g.append(F.line(x0 + 14, yy, x0 + w - 14 - (i % 2) * w * 0.25, yy, J.LINE_DIM, 5))
    return "".join(g)


# ══════════════════════════════════════════════════════════
#  第5章
#  speed_step（c606）＝時の線と最高速度の段（R1 p.96 の会社の説明＝1991年3月 100→120km/h）・付け替え（1996年12月20日）・事故（2005年4月25日）
#  横は時に比例・縦は速さに比例（門番が見る）
# ══════════════════════════════════════════════════════════
SS = dict(x0=240.0, t0=1989.0, k=82.0, v0=90.0, kv=8.0, yb=760.0, ax=800.0, x1=1640.0)
SS_EV = (("1991年3月", (1991, 3, 1)), ("1996年12月20日", (1996, 12, 20)), ("2005年4月25日", (2005, 4, 25)))
SS_V = (100, 120)


def ss_x(t):
    return SS["x0"] + (t - SS["t0"]) * SS["k"]


def ss_y(v):
    return SS["yb"] - (v - SS["v0"]) * SS["kv"]


def _ss_ex(i):
    return ss_x(_ym(*SS_EV[i][1]))


def speed_step_base(st0):
    x96, x05 = _ss_ex(1), _ss_ex(2)
    return [_arrow(SS["x0"], SS["ax"], SS["x1"], SS["ax"], J.LINE, 4, 18),
            F.line(x96, 430.0, x96, SS["ax"], J.LINE, 4, dash="12 10"),
            _ctr(x96, 362.0, "付け替え（今の形に）", 26, INK, 360), _ctr(x96, 400.0, SS_EV[1][0], 24, J.TICK, 300),
            F.line(x05, 430.0, x05, SS["ax"], J.ALERT, 4),
            _ctr(x05, 362.0, "事故", 28, J.ALERT, 200), _ctr(x05, 400.0, SS_EV[2][0], 24, J.TICK, 260)]


def speed_step_stage(prev, st):
    s = []
    x91 = _ss_ex(0)
    if _on(prev, st, "y91"):
        s.append(F.line(x91, 470.0, x91, SS["ax"], J.AMBER, 4))
        s.append(_ctr(x91, 446.0, SS_EV[0][0], 28, J.AMBER, 220))
    if _on(prev, st, "step"):
        y100, y120, x05 = ss_y(SS_V[0]), ss_y(SS_V[1]), _ss_ex(2)
        s.append(F.poly([(SS["x0"], y100), (x91, y100), (x91, y120), (x05, y120)], "none", sc("jr"), 7))
        s.append(_ctr((SS["x0"] + x91) / 2 - 6, y100 - 26, f"{SS_V[0]}km/h", 26, INK, 160))
        s.append(_ctr(1240.0, y120 - 28, f"{SS_V[1]}km/h", 30, INK, 200))
        s.append(_stag(660.0, 600.0, "jr", "会社の説明", 24))
    return s


# ══════════════════════════════════════════════════════════
#  push_out（c608）＝上から見た曲線と外へ押す力（一般の物理の説明・人は描かない）：速さ2倍 → 力4倍（升1つ → 2×2の4つ）
#  矢印は動く部品（聞き役の行で4倍の長さへ）
# ══════════════════════════════════════════════════════════
PO = dict(cx=-180.0, cy=580.0, r=600.0, a=24.0, car=(420.0, 580.0), ax0=458.0, short=130.0, long=520.0)
PO_V, PO_F = 2, 4
PO_SQ = 56.0


def push_out_parts(st):
    L = PO["long"] if st.get("grow") == "on" else PO["short"]
    y = PO["car"][1]
    return [_P("force", "poly", _apts(PO["ax0"], y, PO["ax0"] + L, y, 16.0, 38.0, 28.0), fill=J.ALERT, stroke=J.BG, w=2,
               alpha=1.0 if st.get("force") == "on" else 0.0)]


def push_out_base(st0):
    g = []
    cx, cy, r, a = PO["cx"], PO["cy"], PO["r"], PO["a"]
    for k in range(-int(a), int(a) + 1, 4):
        p0 = (cx + (r - 30) * math.cos(math.radians(k)), cy + (r - 30) * math.sin(math.radians(k)))
        p1 = (cx + (r + 30) * math.cos(math.radians(k)), cy + (r + 30) * math.sin(math.radians(k)))
        g.append(F.line(p0[0], p0[1], p1[0], p1[1], J.LINE_DIM, 5))
    for rr in (r - 15, r + 15):
        g.append(F.poly(_arcpts(cx, cy, rr, rr, -a, a, 24), "none", J.LINE, 5))
    x, y = PO["car"]
    g.append(F.rect(x - 30, y - 100, 60, 200, TRAIN, J.BG, 3, rx=10))
    g.append(_ctr(250.0, 860.0 - 40, "曲線", 26, J.TICK, 160))
    return g


def push_out_stage(prev, st):
    s = []
    if _on(prev, st, "force"):
        s.append(_ctr(600.0, 532.0, "外へ押し出す力", 28, J.ALERT, 260))
    if _on(prev, st, "sq"):
        q, gap = PO_SQ, 8.0
        s.append(_arrow(1110.0, 440.0, 1230.0, 440.0, J.AMBER, 6, 22) + _ctr(1170.0, 486.0, "もとの速さ", 24, J.TICK, 200))
        s.append(_arrow(1262.0, 440.0, 1410.0, 440.0, J.LINE, 4, 16))
        s.append(F.rect(1440.0, 440.0 - q / 2, q, q, J.AMBER, None, None, rx=6) + _ctr(1468.0, 500.0, "もとの力", 24, J.TICK, 200))
        s.append(_arrow(1110.0, 674.0, 1350.0, 674.0, J.AMBER, 6, 22) + _ctr(1230.0, 722.0, f"速さ {PO_V}倍", 28, J.AMBER, 220))
        s.append(_arrow(1370.0, 674.0, 1424.0, 674.0, J.LINE, 4, 16))
        for i in range(2):
            for j in range(2):
                s.append(F.rect(1440.0 + i * (q + gap), 614.0 + j * (q + gap), q, q, J.AMBER, None, None, rx=6))
        s.append(_ctr(1500.0, 774.0, f"力 {PO_F}倍", 30, J.AMBER, 220))
    return s


# ══════════════════════════════════════════════════════════
#  hbars6（c609）＝転覆限界速度の6本の横の棒（0から値どおり＝棒の長さは km/h に比例）。c211（縦の棒・秒）の相方＝向きと物差しを替えた
#  104 報告書（定員150名・揺れあり＝p.230 の物差し）・106／122／123 報告書の表43・108前後 神戸地裁（可能性が高い）・133 会社の公表（事故の日）
# ══════════════════════════════════════════════════════════
HB6 = (("rep", "報告書", "定員150名・揺れあり", 104, "104"), ("rep", "報告書", "93名・揺れあり", 106, "106"),
       ("ct", "神戸地裁", "判決・可能性が高い", 108, "108前後"), ("rep", "報告書", "93名・揺れなし", 122, "122"),
       ("rep", "報告書", "空車・揺れなし", 123, "123"), ("jr", "JR西日本", "事故の日の公表", 133, "133"))
HBX = dict(x0=640.0, k=8.0, y0=388.0, dy=74.0, h=44.0)


def hb_y(i):
    return HBX["y0"] + i * HBX["dy"]


def hb_end(v):
    return HBX["x0"] + v * HBX["k"]


def hbars6_base(st0):
    return [F.line(HBX["x0"], 350.0, HBX["x0"], hb_y(5) + 36, J.LINE, 4)]


def hbars6_stage(prev, st):
    s = []
    h = HBX["h"]
    if _on(prev, st, "bars"):
        s.append(_tline(HBX["x0"] + 12, 336.0, "転覆限界速度（km/h）", 26, J.TICK, "start", 420))
        for i, (_k, _n, _c, v, _l) in enumerate(HB6):
            s.append(F.rect(HBX["x0"], hb_y(i) - h / 2, hb_end(v) - HBX["x0"], h, J.LINE_DIM, None, None, rx=6))
    if _on(prev, st, "cols"):
        for i, (k, name, cond, v, lab) in enumerate(HB6):
            y = hb_y(i)
            s.append(F.rect(HBX["x0"], y - h / 2, hb_end(v) - HBX["x0"], h, sc(k), None, None, rx=6))
            s.append(_tline(130.0, y + 9, name, 24, sc(k), "start", 150))
            s.append(_tline(290.0, y + 8, cond, 22, INK, "start", 330))
            s.append(_tline(hb_end(v) + 14, y + 10, lab, 28, INK, "start", 140))
    return s


# ══════════════════════════════════════════════════════════
#  strip43（c610）＝報告書の表43の最後の行の写し（1両目の列）：93名・揺れあり 106／93名・揺れなし 122／空車・揺れなし 123／
#  会社の公表（空車）133＝表の中の会社の列（R1 p.188・p.194）。表（c227 matrix）とは別の見た目＝1本の帯の切れ端
# ══════════════════════════════════════════════════════════
T43 = (("93名・揺れあり", "106", "rep"), ("93名・揺れなし", "122", "rep"), ("空車・揺れなし", "123", "rep"), ("会社の公表（空車）", "133", "jr"))
T43X = dict(x0=200.0, x1=1720.0, y0=410.0, y1=720.0, cw=380.0)


def t43_cx(i):
    return T43X["x0"] + T43X["cw"] * (i + 0.5)


def strip43_base(st0):
    g = [F.rect(T43X["x0"], T43X["y0"], T43X["x1"] - T43X["x0"], T43X["y1"] - T43X["y0"], J.BG2, J.LINE, 4, rx=4),
         _tline(T43X["x0"] + 6, 388.0, "報告書の表43（1両目の列・最後の行）", 26, J.TICK, "start", 700),
         F.line(T43X["x0"], 500.0, T43X["x1"], 500.0, J.LINE_DIM, 3)]
    for i, (cond, _v, _c) in enumerate(T43):
        if i:
            g.append(F.line(T43X["x0"] + T43X["cw"] * i, T43X["y0"], T43X["x0"] + T43X["cw"] * i, T43X["y1"], J.LINE_DIM, 3))
        g.append(_ctr(t43_cx(i), 456.0, cond, 24, J.TICK, T43X["cw"] - 30))
    return g


def _t43_cell(i, big=True):
    cond, v, c = T43[i]
    x0 = T43X["x0"] + T43X["cw"] * i
    col = rc(c) if c not in SRC else sc(c)
    g = [F.rect(x0 + 10, 512.0, T43X["cw"] - 20, T43X["y1"] - 522.0, "none", col, 6, rx=8)] if big else []
    g.append(_ctr(t43_cx(i), 610.0, v, 84 if big else 54, col if big else J.TICK, 300, "Dela"))
    return "".join(g)


def strip43_stage(prev, st):
    s = []
    if _on(prev, st, "co"):
        s.append(_t43_cell(3))
        s.append(_ctr(t43_cx(3), 760.0, "事故の日に公表", 26, sc("jr"), 340))
    if _on(prev, st, "rep"):
        s += [_t43_cell(0), _t43_cell(1), _t43_cell(2, big=False)]
        s.append(_ctr((t43_cx(0) + t43_cx(1)) / 2, 760.0, "報告書の試算", 26, sc("rep"), 340))
    return s


# ══════════════════════════════════════════════════════════
#  cog2（c611）＝後ろから見た車体と重心の2つの高さ：ばねで傾く分を入れた高さ（報告書の物差し＝表43 の注3）・入れない高さ（会社の 133km/h＝注4）
#  🔴 入れた高さ（青）が上・入れない高さ（茶）が下（門番が見る）。数は 133 だけ（m の値は出さない）
# ══════════════════════════════════════════════════════════
CG = dict(cx=960.0, hi=520.0, lo=606.0, tilt=5.0)
CG_CO = 133
CG_BODY = ((780.0, 700.0), (780.0, 420.0), (820.0, 372.0), (1100.0, 372.0), (1140.0, 420.0), (1140.0, 700.0))


def _spring(x, y0, y1, w=22.0, n=6):
    pts = [(x, y0)] + [(x + (w if i % 2 else -w), y0 + (y1 - y0) * (i + 0.5) / n) for i in range(n)] + [(x, y1)]
    return F.poly(pts, "none", J.LINE, 5)


def cog2_base(st0):
    g = [F.poly(CG_BODY, TRAIN, J.BG, 3, close=True)]
    g += [_spring(860.0, 702.0, 760.0), _spring(1060.0, 702.0, 760.0)]
    g.append(F.rect(800.0, 760.0, 320.0, 30.0, J.BG2, J.LINE, 4, rx=6))
    g += [F.circ(856.0, 812.0, 24.0, J.BG2, J.LINE, 5), F.circ(1064.0, 812.0, 24.0, J.BG2, J.LINE, 5)]
    g.append(F.line(700.0, 842.0, 1220.0, 842.0, J.LINE, 6))
    return g


def cog2_stage(prev, st):
    s = []
    if _on(prev, st, "spring"):
        s.append(F.poly(_rot(CG_BODY, CG["cx"], 700.0, CG["tilt"]), "none", J.AMBER, 4, close=True, dash="12 10"))
        s.append(_tline(1200.0, 470.0, "ばねで車体が傾く分など", 28, J.AMBER, "start", 600))
    if _on(prev, st, "two"):
        s.append(F.line(742.0, CG["hi"], CG["cx"], CG["hi"], sc("rep"), 3) + F.circ(CG["cx"], CG["hi"], 18.0, sc("rep"), J.BG, 4))
        s.append(F.line(742.0, CG["lo"], CG["cx"], CG["lo"], sc("jr"), 3) + F.circ(CG["cx"], CG["lo"], 18.0, sc("jr"), J.BG, 4))
        s.append(_tline(730.0, CG["hi"] + 9, "入れた高さ（報告書の物差し）", 24, sc("rep"), "end", 600))
        s.append(_tline(730.0, CG["lo"] + 9, "入れない高さ", 24, sc("jr"), "end", 400))
        s.append(_tline(730.0, CG["lo"] + 46, f"→ {CG_CO}km/h（会社）", 24, sc("jr"), "end", 400))
        s.append(_stag(1420.0, 640.0, "rep", "表43の注記", 24))
    return s


# ══════════════════════════════════════════════════════════
#  ramp（c612）＝斜めの速さの目盛り（左下 → 右上＝速い）：神戸地裁の幅 105〜110km/h・108前後（可能性が高い）→ 会社の133km/h（相当異なる）
#  位置は速さに比例（門番が見る）。c302（横の速度の目盛り）とは別の見た目＝斜めの坂
# ══════════════════════════════════════════════════════════
RP = dict(ax=300.0, ay=780.0, bx=1600.0, by=380.0, v0=100.0, v1=135.0)
RP_BAND, RP_DOT, RP_CO = (105, 110), 108, 133


def rp_pt(v):
    t = (v - RP["v0"]) / (RP["v1"] - RP["v0"])
    return RP["ax"] + t * (RP["bx"] - RP["ax"]), RP["ay"] + t * (RP["by"] - RP["ay"])


def ramp_base(st0):
    return [_arrow(RP["ax"], RP["ay"], RP["bx"], RP["by"], J.LINE_DIM, 6, 22), _tline(RP["bx"] + 18, RP["by"] + 40, "速さ", 24, J.TICK, "start", 100)]


def ramp_stage(prev, st):
    s = []
    if _on(prev, st, "band"):
        a, b = rp_pt(RP_BAND[0]), rp_pt(RP_BAND[1])
        s.append(F.line(a[0], a[1], b[0], b[1], sc("ct"), 30))
        d = rp_pt(RP_DOT)
        s.append(F.circ(d[0], d[1], 15.0, J.AMBER, J.BG, 4))
        m = rp_pt(sum(RP_BAND) / 2)
        s.append(_ctr(m[0], m[1] - 104, f"{RP_BAND[0]}〜{RP_BAND[1]}km/h", 28, INK, 300))   # 🔧 geom_gap：2段目の弧と 4.7px
        s.append(_ctr(d[0], d[1] + 56, f"{RP_DOT}前後", 26, J.AMBER, 200))
        s.append(_stag(1000.0, 760.0, "ct", "神戸地裁（2012年1月の判決）", 24) + _ctr(1000.0, 812.0, "可能性が高い", 24, J.TICK, 300))
    if _on(prev, st, "co"):
        c = rp_pt(RP_CO)
        s.append(F.circ(c[0], c[1], 18.0, sc("jr"), J.BG, 4))
        # 🔧 geom_gap：札が弧の終わりと坂の矢印の頭に 4.2〜4.6px＝左上へ・弧は帯の上から
        s.append(_ctr(c[0] - 110, c[1] - 72, f"{RP_CO}km/h（会社の公表）", 26, sc("jr"), 380))
        d = rp_pt(RP_DOT)
        p0, p2, cc = (d[0] + 30, d[1] - 40), (c[0] - 10, c[1] - 26), (1000.0, 470.0)
        pts = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * cc[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * cc[1] + u * u * p2[1])
               for u in [i / 20 for i in range(21)]]
        s.append(F.poly(pts, "none", J.ALERT, 4, dash="12 10"))
        s.append(_ctr(960.0, 420.0, "現実の値と相当異なる", 28, J.ALERT, 360))
    return s


# ══════════════════════════════════════════════════════════
#  ceiling（c614）＝天井の線（転覆限界速度 104km/h＝定員150名・報告書の物差し）を、手前の区間の最高速度 120km/h の矢印が突き抜ける（R1 p.230）
#  縦は速さに比例・矢印は動く部品（門番が見る）
# ══════════════════════════════════════════════════════════
CE = dict(x=1000.0, y0=820.0, v0=80.0, k=10.0, x0=520.0, x1=1480.0, start=96)
CE_LIM, CE_MAX = 104, 120


def ce_y(v):
    return CE["y0"] - (v - CE["v0"]) * CE["k"]


def ceiling_parts(st):
    v = CE_MAX if st.get("up") == "on" else CE["start"]
    return [_P("speed", "poly", _apts(CE["x"], CE["y0"], CE["x"], ce_y(v), 30.0, 44.0, 40.0), fill=J.AMBER, stroke=J.BG, w=2, alpha=1.0)]


def ceiling_base(st0):
    y = ce_y(CE_LIM)
    return [F.line(CE["x0"] - 60, CE["y0"], CE["x1"] + 60, CE["y0"], J.LINE, 5),
            F.line(CE["x0"], y, CE["x1"], y, J.ALERT, 6, dash="16 10"),
            _tline(CE["x0"] - 40, y - 20, f"転覆限界速度 {CE_LIM}km/h", 28, INK, "start", 460),
            _tline(CE["x0"] - 40, y + 40, "定員150名・報告書の物差し", 22, J.TICK, "start", 400)]


def ceiling_stage(prev, st):
    s = []
    if _on(prev, st, "up"):
        top = ce_y(CE_MAX)
        s.append(_tline(CE["x"] + 46, top + 12, "手前の区間の最高速度", 26, J.AMBER, "start", 420))
        s.append(_tline(CE["x"] + 46, top + 52, f"{CE_MAX}km/h", 32, J.AMBER, "start", 200))
        s.append(F.poly([(CE["x"] + 330, ce_y(CE_LIM)), (CE["x"] + 344, ce_y(CE_LIM)), (CE["x"] + 344, top + 70), (CE["x"] + 330, top + 70)],
                        "none", J.ALERT, 4))
        s.append(_tline(CE["x"] + 360, (ce_y(CE_LIM) + top + 70) / 2 + 10, "大きく超える", 26, J.ALERT, "start", 220))
    return s


# ══════════════════════════════════════════════════════════
#  sort2（c616）＝曲線の付け替え（1996年12月）の札を2つの箱へ仕分ける：原因の3つの文（出てこない ✕）／「優先」の根拠（R1 p.230）
# ══════════════════════════════════════════════════════════
SO_CARD = "曲線の付け替え（1996年12月）"


def sort2_base(st0):
    return [F.rect(690.0, 330.0, 540.0, 80.0, J.BG2, INK, 4, rx=12), _ctr(CX, 370.0, SO_CARD, 28, INK, 500)]


def sort2_stage(prev, st):
    s = []
    if _on(prev, st, "no"):
        s.append(F.rect(200.0, 520.0, 660.0, 290.0, J.BG2, J.LINE, 4, rx=14) + _ctr(530.0, 566.0, "原因の3つの文", 28, INK, 600))
        for i in range(3):
            x0 = 252.0 + i * 195.0
            s.append(F.rect(x0, 616.0, 170.0, 76.0, J.BG, J.LINE_DIM, 3, rx=8) + _ctr(x0 + 85, 654.0, f"文{i + 1}", 26, J.TICK, 150))
        s.append(_arrow(760.0, 414.0, 640.0, 512.0, J.LINE_DIM, 4, 18, dash="10 8") + _xmark(668.0, 470.0, 22))
        s.append(_ctr(530.0, 756.0, "付け替えは出てこない", 26, J.ALERT, 560))
    if _on(prev, st, "yes"):
        s.append(F.rect(1060.0, 520.0, 660.0, 290.0, J.BG2, sc("rep"), 5, rx=14) + _ctr(1390.0, 566.0, "「優先」の根拠", 28, sc("rep"), 600))
        s.append(_ctr(1390.0, 602.0, "報告書 230頁", 22, J.TICK, 300))
        s.append(F.rect(1110.0, 650.0, 560.0, 80.0, INK, None, None, rx=12) + _ctr(1390.0, 690.0, "曲線の付け替え", 28, J.BG, 500))
        s.append(_arrow(1160.0, 414.0, 1300.0, 642.0, J.AMBER, 5, 20))
    return s


# ══════════════════════════════════════════════════════════
#  cant（c617）＝後ろから見たレールの高さの差（カント＝外側のレールを 97mm 高くして車体を内へ傾ける＝R1 p.73）。
#  高さの差は強めて描いた（模式）。枕木・レール・車体は動く部品＝内側のレールを軸に傾く
# ══════════════════════════════════════════════════════════
CA = dict(px=1220.0, py=700.0, dy=60.0)
CA_MM = 97
CA_ANG = math.degrees(math.asin(CA["dy"] / (CA["px"] - 703.0)))
CA_BODY = ((760.0, 664.0), (760.0, 402.0), (800.0, 362.0), (1140.0, 362.0), (1180.0, 402.0), (1180.0, 664.0))


def cant_parts(st):
    r = CA_ANG if st.get("tilt") == "on" else 0.0
    piv = dict(pivot=[CA["px"], CA["py"]], rot=r)
    # 🔧 試し焼き（40257662340）：傾いた枕木の左の端が札「97mm」と括弧に重なった（動く部品＝geom_gap は測らない）＝左の端を 650 へ
    return [_P("sleeper", "poly", [(650.0, 712.0), (1320.0, 712.0), (1320.0, 736.0), (650.0, 736.0)], fill=J.LINE_DIM, stroke=J.BG, w=2, **piv),
            _P("railL", "poly", [(680.0, 676.0), (726.0, 676.0), (726.0, 712.0), (680.0, 712.0)], fill=J.LINE, stroke=J.BG, w=2, **piv),
            _P("railR", "poly", [(1197.0, 676.0), (1243.0, 676.0), (1243.0, 712.0), (1197.0, 712.0)], fill=J.LINE, stroke=J.BG, w=2, **piv),
            _P("body", "poly", list(CA_BODY), fill=TRAIN, stroke=J.BG, w=3, **piv)]


def cant_base(st0):
    return [_ctr(703.0, 800.0, "外側のレール", 24, J.TICK, 240), _ctr(CA["px"], 800.0, "内側のレール", 24, J.TICK, 240)]


def cant_stage(prev, st):
    s = []
    if _on(prev, st, "tilt"):
        top = CA["py"] - 6 - CA["dy"]
        s.append(F.line(560.0, CA["py"] - 6, 1180.0, CA["py"] - 6, J.LINE_DIM, 3, dash="10 8"))
        s.append(F.poly([(586.0, top), (600.0, top), (600.0, CA["py"] - 6), (586.0, CA["py"] - 6)], "none", J.AMBER, 4))
        s.append(_tline(572.0, top + 40, f"{CA_MM}mm", 34, J.AMBER, "end", 200))
        s.append(_tline(1264.0, 430.0, "車体を内へ傾ける", 26, INK, "start", 360))
    if _on(prev, st, "name"):
        s.append(_ctr(1560.0, 560.0, "カント", 72, J.AMBER, 360))
        s.append(_ctr(1560.0, 624.0, "外側のレールを高く", 24, J.TICK, 360))
    return s


# ══════════════════════════════════════════════════════════
#  coupler（c619）＝上から見た1両目と2両目（右の曲線＝外は左）：2両目は 110km/h でもそれだけでは脱線しない（計算）→
#  外への力に加え、1両目から連結器を通して左向きの力（推定される＝R1 p.226）。脱線の瞬間は描かない
# ══════════════════════════════════════════════════════════
CU = dict(cx=1560.0, cy=900.0, r=820.0, a0=188.0, a1=230.0, c2=198.0, c1=216.0, L=220.0, W=64.0)
CU_V = 110
CU_WORD = "推定される"


def _cu_car(ang):
    cx, cy, r = CU["cx"], CU["cy"], CU["r"]
    a = math.radians(ang)
    c = (cx + r * math.cos(a), cy + r * math.sin(a))
    n = (math.cos(a), math.sin(a))
    t = (-math.sin(a), math.cos(a))
    hl, hw = CU["L"] / 2, CU["W"] / 2
    pts = [(c[0] + u * hl * t[0] + v * hw * n[0], c[1] + u * hl * t[1] + v * hw * n[1]) for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    return c, n, t, pts


def coupler_base(st0):
    g = []
    for rr in (CU["r"] - 15, CU["r"] + 15):
        g.append(F.poly(_arcpts(CU["cx"], CU["cy"], rr, rr, CU["a0"], CU["a1"], 24), "none", J.LINE, 5))
    c2, _n2, t2, p2 = _cu_car(CU["c2"])
    c1, _n1, t1, p1 = _cu_car(CU["c1"])
    g += [F.poly(p2, TRAIN, J.BG, 3, close=True), F.poly(p1, TRAIN, J.BG, 3, close=True)]
    a = (c2[0] + t2[0] * CU["L"] / 2, c2[1] + t2[1] * CU["L"] / 2)
    b = (c1[0] - t1[0] * CU["L"] / 2, c1[1] - t1[1] * CU["L"] / 2)
    g.append(F.line(a[0], a[1], b[0], b[1], INK, 8))
    g.append(_chip(1100.0, 420.0, "1両目", J.TICK, 24))
    g.append(_chip(960.0, 690.0, "2両目", J.TICK, 24))
    return g


def coupler_stage(prev, st):
    s = []
    c2, n2, _t2, p2 = _cu_car(CU["c2"])
    if _on(prev, st, "c2"):
        s.append(F.poly(p2, "none", J.AMBER, 6, close=True))
        s.append(_tline(140.0, 712.0, f"{CU_V}km/h でも", 30, INK, "start", 460))
        s.append(_tline(140.0, 758.0, "それだけでは脱線しない", 26, INK, "start", 460))
        s.append(_tline(140.0, 800.0, "報告書の計算", 22, J.TICK, "start", 300))
    if _on(prev, st, "pull"):
        a = (c2[0] + n2[0] * 44, c2[1] + n2[1] * 44)
        b = (c2[0] + n2[0] * 236, c2[1] + n2[1] * 236)
        s.append(_arrow(a[0], a[1], b[0], b[1], J.ALERT, 7, 26))
        s.append(_tline(b[0] - 10, b[1] - 18, "外への力", 26, J.ALERT, "end", 200))
        c1, n1, t1, _p1 = _cu_car(CU["c1"])
        m = ((c1[0] - t1[0] * CU["L"] / 2 + c2[0] + _t2[0] * CU["L"] / 2) / 2, (c1[1] - t1[1] * CU["L"] / 2 + c2[1] + _t2[1] * CU["L"] / 2) / 2)
        ang = math.radians((CU["c1"] + CU["c2"]) / 2)
        e = (m[0] + math.cos(ang) * 170, m[1] + math.sin(ang) * 170)
        s.append(_arrow(m[0] + math.cos(ang) * 20, m[1] + math.sin(ang) * 20, e[0], e[1], J.AMBER, 7, 26))
        # 🔧 門番 echo：「1両目から連結器を通して」（12字）が語りの丸写し＝3行に割る
        s.append(_tline(e[0] - 18, e[1] - 80, "1両目から", 24, J.AMBER, "end", 300))
        s.append(_tline(e[0] - 18, e[1] - 44, "連結器を通した", 24, J.AMBER, "end", 300))
        s.append(_tline(e[0] - 18, e[1] - 8, "左向きの力", 26, J.AMBER, "end", 300))
        s.append(_tline(1150.0, 770.0, CU_WORD, 30, sc("rep"), "start", 240) + _meter(1320.0, 760.0, CU_WORD))
    return s


# ══════════════════════════════════════════════════════════
#  empty_slot（c623）＝上から見た線路：信号の手前には照らす装置・曲線の手前は何も無い（点線の空の箱）→ 次の章（仕組みと間に合わなかった工事）
# ══════════════════════════════════════════════════════════
def empty_slot_base(st0):
    g = [_rails(140.0, 1180.0, 600.0)]
    for rr in (386.0, 414.0):
        g.append(F.poly(_arcpts(1180.0, 200.0, rr, rr, 90.0, 32.0, 20), "none", J.LINE, 5))
    g.append(F.line(480.0, 560.0, 480.0, 430.0, J.LINE, 8) + F.rect(452.0, 350.0, 56.0, 90.0, J.BG2, J.LINE, 4, rx=8)
             + F.circ(480.0, 374.0, 14.0, J.ALERT, None) + F.circ(480.0, 414.0, 14.0, J.LINE_DIM, None))
    g.append(F.rect(355.0, 589.0, 50.0, 22.0, J.AMBER, None, None, rx=4) + _ctr(380.0, 664.0, "信号の手前：照らす装置", 22, J.TICK, 320))
    g.append(F.rect(1055.0, 589.0, 50.0, 22.0, "none", J.LINE, 3, rx=4, dash="6 5") + _ctr(1080.0, 664.0, "曲線の手前：何も無い", 24, INK, 320))
    return g


def empty_slot_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(1080.0, 520.0, 64))
        s.append(_chip(1560.0, 330.0, "ほかの鉄道は？", J.AMBER, 28))
    if _on(prev, st, "next"):
        x0, y0, w, h = 1000.0, 740.0, 160.0, 40.0
        g = [F.rect(x0, y0, w, h, J.BG, J.AMBER, 3, rx=4)]
        for i in range(6):
            xx = x0 + 10 + i * 28
            g.append(F.poly([(xx, y0 + h), (xx + 14, y0 + h), (xx + 28, y0), (xx + 14, y0)], J.AMBER, None, close=True))
        s.append("".join(g) + F.line(1012.0, 780.0, 1012.0, 808.0, J.AMBER, 5) + F.line(1148.0, 780.0, 1148.0, 808.0, J.AMBER, 5))
        s.append(_ctr(1080.0, 836.0, "間に合わなかった工事", 24, J.AMBER, 320))
        s.append(_chip(1560.0, 760.0, "次の章：仕組みと工事", INK, 26))
    return s


# ══════════════════════════════════════════════════════════
#  第6章
#  dots_co（c701）＝会社の数の点：JR＝3社（JR西日本を含む・JR の全体の数は資料に無い＝点は3つだけ）／私鉄＝113社の点のうち13社（最高裁 S2 p.3）
# ══════════════════════════════════════════════════════════
DC_JR, DC_TOTAL = 3, 113
DC_LIT = (3, 11, 20, 26, 38, 45, 57, 64, 71, 83, 90, 99, 108)
DCX = dict(x0=876.0, y0=450.0, dx=58.0, dy=48.0, cols=15, r=13.0)


def dc_pt(i):
    return DCX["x0"] + (i % DCX["cols"]) * DCX["dx"], DCX["y0"] + (i // DCX["cols"]) * DCX["dy"]


def dots_co_base(st0):
    return [F.rect(140.0, 360.0, 580.0, 460.0, J.BG2, J.LINE_DIM, 3, rx=14), F.rect(800.0, 360.0, 940.0, 460.0, J.BG2, J.LINE_DIM, 3, rx=14),
            _tline(170.0, 408.0, "JR", 34, INK, "start", 120), _tline(830.0, 408.0, "私鉄", 34, INK, "start", 160)]


def dots_co_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_chip(CX, 318.0, "事故の前・自主的に", J.TICK, 26))
        s.append("".join(F.circ(*dc_pt(i), DCX["r"], J.LINE_DIM, None) for i in range(DC_TOTAL)))
    if _on(prev, st, "n"):
        s.append("".join(F.circ(*dc_pt(i), DCX["r"] + 2, J.AMBER, J.BG, 3) for i in DC_LIT))
        s.append(_tline(1716.0, 408.0, f"{DC_TOTAL}社のうち{len(DC_LIT)}社", 30, J.AMBER, "end", 420))
        s.append("".join(F.circ(300.0 + i * 120.0, 590.0, 30.0, J.AMBER, J.BG, 4) for i in range(DC_JR)))
        s.append(_ctr(420.0, 680.0, f"{DC_JR}社（JR西日本を含む）", 28, J.AMBER, 520))
        s.append(_stag(1300.0, 318.0, "ct", "最高裁（2017年の決定）", 22))   # 🔧 試し焼き：JR の枠の中に置くと JR だけの話に見える＝枠の外の上へ
    return s


# ══════════════════════════════════════════════════════════
#  donut（c705）＝曲線の照らしの105か所の内わけ（R1 p.134）：ATS-P だけ 88・ATS-SW だけ 11・両方 6（輪の角度は数に比例＝門番が見る）
#  🔴 輪の真ん中に字を置かない（layout）＝計105か所は輪の上
# ══════════════════════════════════════════════════════════
DN = (("ATS-P だけ", 88, "AMBER"), ("ATS-SW だけ", 11, "LINE"), ("両方", 6, "INK_W"))
DN_TOTAL = 105
DNX = dict(cx=640.0, cy=610.0, ro=210.0, ri=118.0)


def dn_angs():
    out, a = [], -90.0
    for _t, n, _c in DN:
        b = a + 360.0 * n / DN_TOTAL
        out.append((a, b))
        a = b
    return out


def donut_base(st0):
    return []


def donut_stage(prev, st):
    s = []
    if _on(prev, st, "all"):
        for (t, n, c), (a, b) in zip(DN, dn_angs()):
            s.append(_sector(DNX["cx"], DNX["cy"], DNX["ri"], DNX["ro"], a, b, rc(c), J.BG, 4, n=max(4, int((b - a) / 6))))
        s.append(_ctr(DNX["cx"], 340.0, f"計{DN_TOTAL}か所", 34, J.AMBER, 300))   # 🔧 geom_gap：2段目の外の弧と 0.9px
        for i, (t, n, c) in enumerate(DN):
            y = 470.0 + i * 90.0
            s.append(F.rect(1010.0, y - 20, 40.0, 40.0, rc(c), None, None, rx=6))
            s.append(_tline(1070.0, y + 10, t, 28, INK, "start", 300) + _tline(1640.0, y + 12, f"{n}か所", 32, J.AMBER, "end", 200))
    if _on(prev, st, "way"):
        a, b = dn_angs()[0]
        s.append(F.poly(_arcpts(DNX["cx"], DNX["cy"], DNX["ro"] + 22, DNX["ro"] + 22, a, b, 40), "none", sc("jr"), 7))
        s.append(_stag(1180.0, 760.0, "jr", "会社のやり方", 24))
        s.append(_tline(1320.0, 770.0, "ATS-P と一緒に付ける", 28, INK, "start", 420))
    return s


# ══════════════════════════════════════════════════════════
#  order3（c708）＝ATS-P の3つの働きの整備の順（止まれの信号の手前・分岐器が先＝曲線が後＝R1 p.229）と報告書の3つの言い方（強さの升）
# ══════════════════════════════════════════════════════════
OR3 = ("止まれの信号の手前", "分岐器", "曲線")
OR3_ROWS = (("危険の認識", "あった", "可能性が考えられる"), ("急ぐべきと認識", "容易でなかった", "考えられる"), ("曲線の照らし", "後回しに", "考えられる"))
OR3X = dict(xs=(400.0, 960.0, 1520.0), y=450.0, w=380.0, h=110.0, ys=(610.0, 700.0, 790.0))


def order3_base(st0):
    g = [_tline(210.0, 372.0, "ATS-P の働き：整備の順", 26, J.TICK, "start", 520)]
    for i, (x, t) in enumerate(zip(OR3X["xs"], OR3)):
        g.append(F.rect(x - OR3X["w"] / 2, OR3X["y"] - OR3X["h"] / 2, OR3X["w"], OR3X["h"], J.BG2, J.LINE, 4, rx=12))
        g.append(_ctr(x - OR3X["w"] / 2 + 34, OR3X["y"], "①②③"[i], 32, J.AMBER, 60) + _ctr(x + 22, OR3X["y"], t, 28, INK, OR3X["w"] - 90))
        if i:
            g.append(_arrow(OR3X["xs"][i - 1] + OR3X["w"] / 2 + 8, OR3X["y"], x - OR3X["w"] / 2 - 8, OR3X["y"], J.LINE, 4, 16))
    return g


def _or3_row(i):
    a, b, w = OR3_ROWS[i]
    y = OR3X["ys"][i]
    return (_tline(260.0, y + 10, a, 28, INK, "start", 300) + _arrow(580.0, y, 650.0, y, J.LINE_DIM, 4, 14)
            + _tline(670.0, y + 10, b, 28, INK, "start", 300) + _tline(1150.0, y + 9, w, 26, J.AMBER, "start", 260)
            + _meter(1420.0, y, w))


def order3_stage(prev, st):
    s = []
    if _on(prev, st, "r1"):
        s.append(_or3_row(0))
    if _on(prev, st, "r2"):
        s.append(_or3_row(1))
    if _on(prev, st, "r3"):
        s.append(_or3_row(2))
        x = OR3X["xs"][2]
        s.append(F.rect(x - OR3X["w"] / 2 - 10, OR3X["y"] - OR3X["h"] / 2 - 10, OR3X["w"] + 20, OR3X["h"] + 20, "none", J.ALERT, 5, rx=16, dash="14 10"))
        s.append(_ctr(x, OR3X["y"] + 90, "後回し", 28, J.ALERT, 200))
    return s


# ══════════════════════════════════════════════════════════
#  tl_plan（c710）＝年表（横・1か月＝58画素）：2003年9月29日 経営会議（会社）→ 工期 2003年10月〜2005年5月 → 使い始め 2005年2月以降・順に（R1 p.135）
#  事故（2005年4月25日）の線は基図。相方 ca07（縦の年表）とは向きを替えた
# ══════════════════════════════════════════════════════════
TP = dict(x0=180.0, m0=6.0, k=58.0, y=600.0, x1=1660.0)
TP_MEET = (2003, 9, 29)
TP_WORK = ((2003, 10, 1), (2005, 5, 31))
TP_USE = (2005, 2, 1)
TP_ACC = (2005, 4, 25)


def tp_x(y, m, d=1):
    return TP["x0"] + ((y - 2003) * 12 + (m - 1) + (d - 1) / 31.0 - TP["m0"]) * TP["k"]


def tl_plan_base(st0):
    g = [_arrow(TP["x0"], TP["y"], TP["x1"], TP["y"], J.LINE, 4, 18)]
    for mm in range(7, 32):
        x = TP["x0"] + (mm - TP["m0"]) * TP["k"]
        if x <= TP["x1"] - 30:
            g.append(F.line(x, TP["y"] - 8, x, TP["y"] + 8, J.LINE_DIM, 3))
    for yy in (2004, 2005):
        x = tp_x(yy, 1)
        g.append(F.line(x, TP["y"] - 18, x, TP["y"] + 18, J.LINE, 4) + _ctr(x, TP["y"] + 40, f"{yy}年", 26, J.TICK, 140))
    xa = tp_x(*TP_ACC)
    g.append(F.line(xa, 380.0, xa, 820.0, J.ALERT, 4) + _ctr(xa, 350.0, "事故", 28, J.ALERT, 120) + _ctr(xa + 4, 846.0, "2005年4月25日", 24, J.ALERT, 260))
    return g


def tl_plan_stage(prev, st):
    s = []
    if _on(prev, st, "meet"):
        x = tp_x(*TP_MEET)
        s.append(F.poly([(x, TP["y"] - 18), (x + 18, TP["y"]), (x, TP["y"] + 18), (x - 18, TP["y"])], sc("jr"), J.BG, 3, close=True))
        s.append(_ctr(x + 40, 510.0, "経営会議で決める", 28, sc("jr"), 320) + _ctr(x + 40, 550.0, "2003年9月29日", 24, J.TICK, 260))
    if _on(prev, st, "work"):
        a, b = tp_x(*TP_WORK[0]), tp_x(*TP_WORK[1])
        s.append(F.rect(a, 664.0, b - a, 38.0, J.AMBER, None, None, rx=8))
        s.append(_ctr((a + b) / 2 - 80, 742.0, "工期：2003年10月〜2005年5月", 26, INK, 560))
    if _on(prev, st, "use"):
        x = tp_x(*TP_USE)
        for i in range(4):
            xx = x + i * 26
            s.append(F.poly([(xx - 12, TP["y"] - 34), (xx + 12, TP["y"] - 34), (xx, TP["y"] - 12)], J.AMBER, None, close=True))
        s.append(_ctr(x - 50, 470.0, "使い始め", 28, J.AMBER, 200) + _ctr(x - 50, 508.0, "2005年2月以降・順に", 24, J.AMBER, 300))
    return s


# ══════════════════════════════════════════════════════════
#  spill（c712）＝年度の境の壁（2005年4月）を、曲線などの照らしの予定がほんの少し越える（担当者の口述＝R1 p.136）。
#  中長期計画は 2003年度・2004年度・止まれの信号の照らしは 2004年度のうち。1か月＝60画素・事故の線（2005年4月25日）
# ══════════════════════════════════════════════════════════
SPL = dict(wall=1100.0, k=60.0, ys=(470.0, 600.0, 730.0), h=44.0)
SPL_ACC = (2005, 4, 25)
SPL_POKE = 2


def spl_x(y, m, d=1):
    return SPL["wall"] + (_ym(y, m, d) - _ym(2005, 4)) * 12 * SPL["k"]


def spill_base(st0):
    w = SPL["wall"]
    xa = spl_x(*SPL_ACC)
    return [F.line(w, 330.0, w, 800.0, INK, 8), _ctr(740.0, 352.0, "2004年度", 30, J.TICK, 260), _ctr(1460.0, 352.0, "2005年度", 30, J.TICK, 260),
            F.line(xa, 400.0, xa, 800.0, J.ALERT, 4, dash="10 8"), _tline(xa + 12, 832.0, "事故 2005年4月25日", 24, J.ALERT, "start", 300)]


def _spl_bar(y, x0, x1, t, col, ink, tx=None, head=False):
    h = SPL["h"]
    g = F.rect(x0, y - h / 2, x1 - x0 - (18 if head else 0), h, col, None, None, rx=8)
    if head:
        g += F.poly([(x1 - 22, y - h / 2 - 8), (x1, y), (x1 - 22, y + h / 2 + 8)], col, None, close=True)
    return g + _ctr(tx or (x0 + x1) / 2, y, t, 22, ink, x1 - x0 - 30)


def spill_stage(prev, st):
    s = []
    if _on(prev, st, "plan"):
        s.append(_spl_bar(SPL["ys"][0], 140.0, SPL["wall"] - 6, "中長期計画：2003年度・2004年度", J.LINE_DIM, INK))
    if _on(prev, st, "staff"):
        s.append(_chip(380.0, 410.0, "担当者の口述（報告書）", J.TICK, 22))
        s.append(_spl_bar(SPL["ys"][1], 500.0, 1040.0, "止まれの信号の照らし：2004年度のうち", J.LINE, J.BG))
    if _on(prev, st, "poke"):
        x1 = SPL["wall"] + SPL_POKE * SPL["k"]
        s.append(_spl_bar(SPL["ys"][2], 700.0, x1, "分岐・曲線などの照らし", J.AMBER, J.BG, tx=900.0, head=True))
        s.append(_tline(x1 + 18, SPL["ys"][2] + 10, "少し入り込む", 28, J.AMBER, "start", 260))
    return s


# ══════════════════════════════════════════════════════════
#  signal_date（c714）＝止まれの信号の手前の照らしの使い始め：2005年2月 → 2005年6月（工期が短い＝区長〈当時〉の口述・2004年10月ごろ伝えた＝R1 p.138）
#  曲線の照らしの話ではない（曲線の印は沈めて「この話ではない」）
# ══════════════════════════════════════════════════════════
SD_FROM, SD_TO, SD_TOLD = "2005年2月", "2005年6月", "2004年10月ごろ"


def signal_date_base(st0):
    return [_rails(140.0, 760.0, 800.0), F.line(360.0, 780.0, 360.0, 470.0, J.LINE, 8), F.rect(320.0, 360.0, 80.0, 112.0, J.BG2, J.LINE, 4, rx=10),
            F.circ(360.0, 392.0, 18.0, J.ALERT, None), F.circ(360.0, 440.0, 18.0, J.LINE_DIM, None),
            F.rect(232.0, 789.0, 64.0, 22.0, J.AMBER, None, None, rx=4)]


def signal_date_stage(prev, st):
    s = []
    if _on(prev, st, "short"):
        s.append(_stag(1000.0, 340.0, "jr", "区長（当時）の口述", 24))
        s.append(_ctr(1000.0, 414.0, "工期が短い", 30, INK, 300))
        s.append(F.line(950.0, 470.0, 1050.0, 470.0, J.AMBER, 8) + _arrow(860.0, 470.0, 936.0, 470.0, J.TICK, 4, 16)
                 + _arrow(1140.0, 470.0, 1064.0, 470.0, J.TICK, 4, 16))
    if _on(prev, st, "move"):
        s.append(_ctr(690.0, 580.0, SD_FROM, 34, J.TICK, 260) + _ctr(690.0, 530.0, "前の予定", 22, J.TICK, 200))   # 🔧 geom_gap：取り消し線が字を貫く＝線をやめた
        s.append(_arrow(810.0, 580.0, 920.0, 580.0, J.AMBER, 5, 20))
        s.append(_ctr(1060.0, 580.0, SD_TO, 36, J.AMBER, 280))
        s.append(_tline(870.0, 659.0, SD_TOLD, 24, J.TICK, "end", 260) + _tline(886.0, 659.0, "伝えた", 24, INK, "start", 120))   # 🔧 門番 echo＝2つの字に割る
    if _on(prev, st, "which"):
        s.append(F.rect(272.0, 340.0, 176.0, 488.0, "none", J.AMBER, 4, rx=14, dash="12 8"))
        s.append(_ctr(360.0, 316.0, "止まれの信号の手前", 26, J.AMBER, 320))
        s.append(F.poly(_arcpts(1340.0, 860.0, 260.0, 260.0, 230.0, 300.0, 16), "none", J.LINE_DIM, 8))
        s.append(_ctr(1500.0, 690.0, "曲線の照らし", 26, J.TICK, 260) + _ctr(1500.0, 734.0, "この話ではない", 28, J.ALERT, 300))
    return s


# ══════════════════════════════════════════════════════════
#  drop2（c717）＝縦の2つの日付：事故 2005年4月25日 → この区間の ATS-P の使い始め 2005年6月19日（約2か月＝R1 p.140・S2 p.4）。
#  c512（横の時の線と2本のピン）とは別の見た目＝縦の点線と括弧
# ══════════════════════════════════════════════════════════
DR2 = dict(x=700.0, y0=400.0, y1=740.0)
DR2_A, DR2_B, DR2_GAP = "2005年4月25日", "2005年6月19日", "約2か月"


def drop2_base(st0):
    return [F.circ(DR2["x"], DR2["y0"], 22.0, J.ALERT, J.BG, 4), _tline(DR2["x"] + 46, DR2["y0"] - 4, "事故", 30, J.ALERT, "start", 200),
            _tline(DR2["x"] + 46, DR2["y0"] + 34, DR2_A, 26, J.TICK, "start", 300)]


def drop2_stage(prev, st):
    s = []
    if _on(prev, st, "line"):
        s.append(_arrow(DR2["x"], DR2["y0"] + 30, DR2["x"], DR2["y1"] - 30, J.LINE, 5, 20, dash="12 10"))
        s.append(_tline(DR2["x"] + 46, DR2["y1"] + 8, "この区間の ATS-P の使い始め", 28, INK, "start", 560))
    if _on(prev, st, "date"):
        s.append(F.circ(DR2["x"], DR2["y1"], 22.0, J.AMBER, J.BG, 4))
        s.append(_tline(DR2["x"] + 46, DR2["y1"] + 50, DR2_B, 30, J.AMBER, "start", 300))
        s.append(F.poly([(DR2["x"] - 60, DR2["y0"]), (DR2["x"] - 76, DR2["y0"]), (DR2["x"] - 76, DR2["y1"]), (DR2["x"] - 60, DR2["y1"])], "none", J.AMBER, 4))
        s.append(_tline(DR2["x"] - 96, (DR2["y0"] + DR2["y1"]) / 2 + 12, DR2_GAP, 34, J.AMBER, "end", 240))
        s.append(F.rect(1300.0, 700.0, 120.0, 36.0, J.AMBER, None, None, rx=8) + _ctr(1360.0, 780.0, "ATS-P の地上子", 22, J.TICK, 260))
    return s


# ══════════════════════════════════════════════════════════
#  kk_page（c718）＝国会会議録の頁の写し（2005年5月12日・参議院 国土交通委員会・国土交通大臣〈当時〉）：ATS-P の整備の真っ最中・
#  6月にはでき上がる状況で事故（引用は2つの字に割る＝門番 echo）。c915（演台と吹き出し）・c918（答弁の中の答弁）とは別の見た目
# ══════════════════════════════════════════════════════════
KP_DAY = "2005年5月12日"


def kk_page_base(st0):
    return []


def kk_page_stage(prev, st):
    s = []
    if _on(prev, st, "date"):
        s.append(_chip(420.0, 350.0, "事故 2005年4月25日", J.ALERT, 24))
        s.append(_arrow(600.0, 350.0, 760.0, 350.0, J.LINE, 4, 16) + _ctr(680.0, 318.0, "翌月", 22, J.TICK, 100))
        s.append(_stag(960.0, 350.0, "kok", KP_DAY, 24))
    if _on(prev, st, "page"):
        s.append(F.rect(300.0, 430.0, 1320.0, 390.0, J.BG2, sc("kok"), 5, rx=10) + F.line(300.0, 506.0, 1620.0, 506.0, sc("kok"), 3))
        s.append(_tline(336.0, 482.0, "国会会議録・参議院 国土交通委員会", 26, sc("kok"), "start", 760))
        s.append(_tline(1584.0, 482.0, KP_DAY, 26, J.TICK, "end", 300))
        s.append(_tline(336.0, 560.0, "国土交通大臣（当時）", 28, INK, "start", 500))
        s.append(_tline(940.0, 650.0, "ATS-P：", 34, J.AMBER, "end", 260) + _tline(950.0, 650.0, "整備の真っ最中", 34, INK, "start", 500))
    if _on(prev, st, "june"):
        s.append(_tline(940.0, 750.0, "6月にはでき上がる", 34, INK, "end", 460) + _tline(950.0, 750.0, "状況で、事故", 34, INK, "start", 400))
    return s


# ══════════════════════════════════════════════════════════
#  receipt（c720）＝神戸地裁（2012年1月の判決）：ATS-P か ATS-SW の照らしで事故を回避できた → 工事の費用の伝票（この曲線だけ＝S3 p.12）
#  ATS-P 80万円程度・ATS-SW 80万〜120万円程度。値札（c226）とは別の見た目＝下の縁がぎざぎざの伝票
# ══════════════════════════════════════════════════════════
RC_ROWS = (("ATS-P", "80万円程度"), ("ATS-SW", "80万〜120万円程度"))


def receipt_base(st0):
    return []


def receipt_stage(prev, st):
    s = []
    if _on(prev, st, "court"):
        s.append(_stag(520.0, 380.0, "ct", "神戸地裁（2012年1月の判決）", 24))
        # 🔧 門番 echo：「ATS-P か ATS-SW」（12字）が語りの丸写し＝3つの字に割る
        s.append(_tline(470.0, 487.0, "ATS-P", 32, J.AMBER, "end", 200) + _ctr(500.0, 476.0, "か", 26, J.TICK, 60)
                 + _tline(530.0, 487.0, "ATS-SW", 32, J.AMBER, "start", 220) + _ctr(520.0, 524.0, "の照らしで", 28, INK, 300))
        s.append(_arrow(520.0, 560.0, 520.0, 620.0, J.LINE, 5, 18))
        s.append(_ctr(500.0, 668.0, "事故を回避できた", 32, INK, 460) + _check(720.0, 664.0, 20, INK))
    if _on(prev, st, "cost"):
        x0, x1, y0, y1 = 1080.0, 1640.0, 340.0, 800.0
        pts = [(x0, y0), (x1, y0), (x1, y1)]
        n = 10
        for i in range(n):
            xa = x1 - (x1 - x0) * (i + 0.5) / n
            xb = x1 - (x1 - x0) * (i + 1) / n
            pts += [(xa, y1 - 22), (xb, y1)]
        s.append(F.poly(pts, J.BG2, INK, 4, close=True))
        s.append(_ctr(1360.0, 392.0, "工事の費用", 30, INK, 400) + _ctr(1360.0, 434.0, "この曲線だけ", 24, J.TICK, 300))
        s.append(F.line(x0 + 30, 466.0, x1 - 30, 466.0, J.LINE_DIM, 3, dash="8 8"))
        s.append(_tline(1120.0, 548.0, RC_ROWS[0][0], 30, INK, "start", 200) + _tline(1600.0, 550.0, RC_ROWS[0][1], 34, J.AMBER, "end", 300))
        s.append(_tline(1120.0, 640.0, RC_ROWS[1][0], 26, J.TICK, "start", 200) + _tline(1600.0, 640.0, RC_ROWS[1][1], 26, J.TICK, "end", 320))
    return s


# ══════════════════════════════════════════════════════════
#  trim3（c722）＝決まった運転時間の帯の右の端が3回切られて落ちる：2002年3月 20秒・2003年3月 20秒・2004年10月 10秒＝3回で50秒
#  （中山寺駅に止まる延長 45秒は除く＝R1 p.141）。切れ端の幅は秒に比例（1秒＝8画素）・切れ端は動く部品
# ══════════════════════════════════════════════════════════
TR = dict(x0=200.0, main=980.0, k=8.0, y=470.0, h=60.0, drop=250.0)
TR_CUT = (("2002年3月", 20), ("2003年3月", 20), ("2004年10月", 10))
TR_ADD, TR_SUM = 45, 50


def tr_edges():
    xs = [TR["x0"] + TR["main"]]
    for _d, sec in TR_CUT:
        xs.append(xs[-1] + sec * TR["k"])
    return xs


def trim3_parts(st):
    xs = tr_edges()
    y, h = TR["y"], TR["h"]
    dy = TR["drop"] if st.get("cut") == "on" else 0.0
    return [_P(f"cut{i}", "poly", [(xs[i] + 2, y - h / 2), (xs[i + 1] - 2, y - h / 2), (xs[i + 1] - 2, y + h / 2), (xs[i] + 2, y + h / 2)],
               fill=J.AMBER, stroke=J.BG, w=2, dy=dy, lag=0.25 * i, alpha=1.0) for i in range(3)]


def trim3_base(st0):
    y, h = TR["y"], TR["h"]
    return [F.rect(TR["x0"], y - h / 2, TR["main"], h, J.LINE, None, None, rx=8), _ctr(TR["x0"] + TR["main"] / 2, y, "決まった運転時間（宝塚〜尼崎）", 26, J.BG, 800)]


def trim3_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_tline(tr_edges()[-1] + 26, TR["y"] + 12, "余裕は？", 30, J.AMBER, "start", 200))
    if _on(prev, st, "ext"):
        w = TR_ADD * TR["k"]
        s.append(F.rect(TR["x0"], 600.0, w, 60.0, "none", J.TICK, 3, rx=8, dash="10 8") + _ctr(TR["x0"] + w / 2, 630.0, f"中山寺駅に止まる延長 {TR_ADD}秒", 22, J.TICK, w - 20))
        s.append(_tline(TR["x0"] + w + 20, 640.0, "除く", 28, J.ALERT, "start", 120))
    if _on(prev, st, "cut"):
        xs = tr_edges()
        yb = TR["y"] + TR["drop"] + TR["h"] / 2
        for i, (d, sec) in enumerate(TR_CUT):
            cx = (xs[i] + xs[i + 1]) / 2
            s.append(_ctr(cx, yb + 26, d, 20, J.TICK, 150) + _ctr(cx, yb + 58, f"{sec}秒", 24, J.AMBER, 120))
        s.append(_tline(xs[-1] + 30, TR["y"] + TR["drop"] + 12, f"{len(TR_CUT)}回で{TR_SUM}秒", 30, J.AMBER, "start", 220))
    return s


# ══════════════════════════════════════════════════════════
#  scale2（c725）＝2つの扱いの天びん（R1 p.199）：社員の扱いの誤りで1分以上の遅れ → 日勤教育・懲戒／会社の運行計画＝65日の半数以上の日に
#  1分以上遅れて着く（右は前のカット c723・c724 の語り＝基図）。天びんは水平のまま（どちらにも傾けない）
# ══════════════════════════════════════════════════════════
def scale2_base(st0):
    g = [F.line(360.0, 520.0, 1560.0, 520.0, J.LINE, 8), F.line(960.0, 520.0, 960.0, 760.0, J.LINE, 8),
         F.poly([(960.0, 500.0), (930.0, 540.0), (990.0, 540.0)], J.LINE, None, close=True), F.rect(860.0, 760.0, 200.0, 30.0, J.BG2, J.LINE, 4, rx=6)]
    for x in (1240.0, 1640.0):
        g.append(F.line(x, 520.0, x, 580.0, J.LINE_DIM, 3))
    g.append(F.rect(1160.0, 580.0, 560.0, 230.0, J.BG2, sc("jr"), 4, rx=12))
    g.append(_ctr(1440.0, 622.0, "会社の運行計画", 26, sc("jr"), 500) + _ctr(1440.0, 686.0, "65日の半数以上の日に", 26, INK, 500)
             + _ctr(1440.0, 750.0, "1分以上遅れて着く", 28, J.AMBER, 500))
    return g


def scale2_stage(prev, st):
    s = []
    if _on(prev, st, "l"):
        for x in (280.0, 680.0):
            s.append(F.line(x, 520.0, x, 580.0, J.LINE_DIM, 3))
        s.append(F.rect(200.0, 580.0, 560.0, 230.0, J.BG2, INK, 4, rx=12))
        s.append(_ctr(480.0, 622.0, "社員の扱いの誤りで", 26, INK, 500) + _ctr(480.0, 686.0, "1分以上の遅れ", 30, J.AMBER, 500))
    if _on(prev, st, "r"):
        s.append(_ctr(480.0, 752.0, "→ 日勤教育・懲戒", 28, J.ALERT, 500))
        s.append(_stag(CX, 430.0, "rep", "報告書", 24))
    return s


# ══════════════════════════════════════════════════════════
#  jr_words（c727）＝JR西日本の冊子（2021年3月「将来にわたる鉄道の安全の実現に向けて」）の2つの言葉＝冊子の頁の形（折った角）。
#  原文の句を短い字に割る（門番 echo）。c530（2つの口述・大きな括弧）とは別の見た目
# ══════════════════════════════════════════════════════════
JW = (("当該曲線部に対する", "速度照査付きのATSを", "整備できていませんでした"), ("懲罰的と受け止められる", "再教育などを", "行っていました"))


def _jw_page(x0, lines):
    x1, y0, y1 = x0 + 700.0, 420.0, 780.0
    col = sc("jr")
    g = [F.poly([(x0, y0), (x1 - 50, y0), (x1, y0 + 50), (x1, y1), (x0, y1)], J.BG2, col, 5, close=True),
         F.poly([(x1 - 50, y0), (x1 - 50, y0 + 50), (x1, y0 + 50)], "none", col, 4)]
    for i, t in enumerate(lines):
        g.append(_ctr(x0 + 350.0, 520.0 + i * 76.0, t, 30 if i else 28, INK if i else J.TICK, 620))
    return "".join(g)


def jr_words_base(st0):
    return [_stag(CX, 344.0, "jr", "JR西日本の冊子（2021年3月）", 24)]


def jr_words_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_jw_page(200.0, JW[0]))
    if _on(prev, st, "b"):
        s.append(_jw_page(1020.0, JW[1]))
    return s


# ══════════════════════════════════════════════════════════
#  第7章
#  tearoff（c801）＝日めくり（2005年4月25日 事故の日）と、破った頁の2枚（4月28日・5月27日＝国の措置＝R1 p.249）。c528（3枚の月の暦）とは別の見た目
# ══════════════════════════════════════════════════════════
TO_DAYS = (("4月", "28", "3日後", "国 → JR西日本", "安全性向上計画の指示"), ("5月", "27", "", "国 → 関係各社", "曲線の ATS：指導"))


def _torn(x0, y0, w, h, col):
    pts = [(x0, y0 + 10)]
    n = 8
    for i in range(n):
        pts += [(x0 + w * (i + 0.5) / n, y0), (x0 + w * (i + 1) / n, y0 + 10)]
    pts += [(x0 + w, y0 + h), (x0, y0 + h)]
    return F.poly(pts, J.BG2, col, 4, close=True)


def tearoff_base(st0):
    return [F.rect(220.0, 330.0, 380.0, 480.0, J.BG2, J.LINE, 5, rx=12), F.rect(300.0, 316.0, 30.0, 40.0, J.LINE, None, None, rx=6),
            F.rect(490.0, 316.0, 30.0, 40.0, J.LINE, None, None, rx=6), F.line(240.0, 450.0, 580.0, 450.0, J.LINE_DIM, 3),
            _ctr(410.0, 384.0, "2005年", 28, J.TICK, 300), _ctr(410.0, 426.0, "4月", 34, INK, 200), _ctr(410.0, 610.0, "25", 170, INK, 340, "Dela"),
            _ctr(410.0, 762.0, "事故の日", 28, J.ALERT, 300)]


def _to_slip(i):
    mon, day, after, who, what = TO_DAYS[i]
    y0 = 380.0 + i * 220.0
    g = [_torn(700.0, y0, 240.0, 180.0, J.AMBER), _ctr(820.0, y0 + 46, mon, 28, J.TICK, 200), _ctr(820.0, y0 + 122, day, 84, INK, 220, "Dela")]
    if after:
        g.append(_tline(990.0, y0 + 28, after, 28, J.AMBER, "start", 200))
    g.append(_tline(990.0, y0 + 88, who, 28, INK, "start", 500) + _tline(990.0, y0 + 146, what, 32, INK, "start", 700))
    return "".join(g)


def tearoff_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(820.0, 330.0, 56) + _tline(870.0, 346.0, "事故のあと", 28, J.TICK, "start", 300))
    if _on(prev, st, "d1"):
        s.append(_to_slip(0))
    if _on(prev, st, "d2"):
        s.append(_to_slip(1))
    return s


# ══════════════════════════════════════════════════════════
#  stretch（c803）＝決まった運転時間の3本の帯（15分00秒から＝その前は省く・1秒＝16画素）：前 15分35秒 → 運転の再開から 16分20秒（＋45秒）→
#  2006年3月18日から 16分25秒（＋5秒＝R1 p.141・p.249）。帯の右の端は秒に比例（門番が見る）。c722（切られて落ちる帯）とは逆向きの絵
# ══════════════════════════════════════════════════════════
SR = dict(x0=200.0, k=16.0, t0=900, h=56.0, ys=(430.0, 590.0, 750.0))
SR_T = (935, 980, 985)
SR_LAB = ("15分35秒", "16分20秒", "16分25秒")
SR_HEAD = ("事故の前", "運転の再開から（2005年6月19日）", "2006年3月18日から")


def sr_x(t):
    return SR["x0"] + (t - SR["t0"]) * SR["k"]


def _sr_row(i):
    y, h = SR["ys"][i], SR["h"]
    g = [_tline(SR["x0"] + 20, y - h / 2 - 18, SR_HEAD[i], 22, J.TICK, "start", 520),   # 🔧 geom_gap：切れ目の印と 5.8px
         F.rect(SR["x0"], y - h / 2, sr_x(SR_T[0]) - SR["x0"], h, J.LINE_DIM, None, None, rx=6),
         F.line(SR["x0"] - 14, y + h / 2 + 6, SR["x0"] + 4, y - h / 2 - 6, J.LINE, 3) + F.line(SR["x0"] - 4, y + h / 2 + 6, SR["x0"] + 14, y - h / 2 - 6, J.LINE, 3)]
    if i >= 1:
        g.append(F.rect(sr_x(SR_T[0]), y - h / 2, sr_x(SR_T[1]) - sr_x(SR_T[0]), h, J.AMBER, None, None, rx=6))
        g.append(_ctr((sr_x(SR_T[0]) + sr_x(SR_T[1])) / 2, y, f"＋{SR_T[1] - SR_T[0]}秒", 28, J.BG, 300))
    if i >= 2:
        g.append(F.rect(sr_x(SR_T[1]), y - h / 2, sr_x(SR_T[2]) - sr_x(SR_T[1]), h, INK, None, None, rx=4))
        g.append(_ctr((sr_x(SR_T[1]) + sr_x(SR_T[2])) / 2, y - h / 2 - 22, f"＋{SR_T[2] - SR_T[1]}秒", 24, J.AMBER, 120))
    g.append(_tline(sr_x(SR_T[i]) + 18, y + 11, SR_LAB[i], 30, INK, "start", 220))
    return "".join(g)


def stretch_base(st0):
    return [_sr_row(0)]


def stretch_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_sr_row(1))
    if _on(prev, st, "b"):
        s.append(_sr_row(2))
    return s


# ══════════════════════════════════════════════════════════
#  flow_fan（c807）＝横の流れと枝分かれ：省令を改める（2006年3月24日）→ 施行（2006年7月1日）→ 曲線・分岐器・線路の終わり：速度を制限する装置
#  ＋ほかに3つ（中身は次の c808 の語り＝先回りしない）。c507（縦の流れ＋強さの升）の相方
# ══════════════════════════════════════════════════════════
FF_DAYS = ("2006年3月24日", "2006年7月1日")
FF_YS = (340.0, 470.0, 600.0, 730.0)


def flow_fan_base(st0):
    return []


def flow_fan_stage(prev, st):
    s = []
    if _on(prev, st, "ab"):
        s.append(F.rect(140.0, 480.0, 360.0, 140.0, J.BG2, INK, 4, rx=14) + _ctr(320.0, 530.0, "省令を改める", 30, INK, 330)
                 + _ctr(320.0, 584.0, FF_DAYS[0], 24, J.TICK, 330))
        s.append(_arrow(510.0, 550.0, 600.0, 550.0, J.LINE, 5, 18))
        s.append(F.rect(610.0, 480.0, 270.0, 140.0, J.BG2, INK, 4, rx=14) + _ctr(745.0, 530.0, "施行", 30, INK, 240)
                 + _ctr(745.0, 584.0, FF_DAYS[1], 24, J.TICK, 250))
    if _on(prev, st, "fan"):
        for i, y in enumerate(FF_YS):
            s.append(_arrow(890.0, 550.0, 1050.0, y, J.AMBER if i == 0 else J.LINE_DIM, 4, 16))
            if i == 0:
                s.append(F.rect(1060.0, y - 50, 700.0, 100.0, J.BG2, J.AMBER, 5, rx=12) + _ctr(1410.0, y - 18, "曲線・分岐器・線路の終わり", 26, INK, 660)
                         + _ctr(1410.0, y + 24, "速度を制限する装置", 28, J.AMBER, 660))
            else:
                s.append(F.rect(1060.0, y - 46, 700.0, 92.0, "none", J.LINE_DIM, 3, rx=12, dash="12 10"))
        s.append(_ctr(1410.0, 822.0, "ほかに3つ", 24, J.TICK, 300))
        s.append(_chip(745.0, 690.0, "義務になる", J.AMBER, 26))
    return s


# ══════════════════════════════════════════════════════════
#  hourglass（c809）＝砂時計（猶予）：すでにある線（速い線・本数の多い線）は施行から10年か次の改築まで（M1）→ それでも 2006年度末までに
#  47社の曲線 2,254か所（R1 p.250）
# ══════════════════════════════════════════════════════════
HG_YEARS, HG_CO, HG_N, HG_BY = 10, 47, "2,254", "2006年度末"


def hourglass_base(st0):
    return [F.rect(290.0, 362.0, 260.0, 16.0, J.LINE, None, None, rx=4), F.rect(290.0, 782.0, 260.0, 16.0, J.LINE, None, None, rx=4),
            F.poly([(310.0, 380.0), (530.0, 380.0), (440.0, 572.0), (440.0, 588.0), (530.0, 780.0), (310.0, 780.0), (400.0, 588.0), (400.0, 572.0)],
                   "none", J.LINE, 5, close=True)]


def hourglass_stage(prev, st):
    s = []
    if _on(prev, st, "has"):
        s.append(_tline(640.0, 424.0, "すでにある線", 30, INK, "start", 400) + _tline(640.0, 474.0, "猶予があった", 28, J.AMBER, "start", 400))
    if _on(prev, st, "term"):
        s.append(F.poly([(334.0, 420.0), (506.0, 420.0), (430.0, 560.0), (410.0, 560.0)], J.AMBER, None, close=True, op=0.85))
        s.append(F.poly([(410.0, 700.0), (430.0, 700.0), (500.0, 770.0), (340.0, 770.0)], J.AMBER, None, close=True, op=0.85))
        s.append(_tline(640.0, 556.0, "速い線・本数の多い線", 26, J.TICK, "start", 460))
        s.append(_tline(640.0, 616.0, f"施行から{HG_YEARS}年", 32, INK, "start", 400) + _tline(640.0, 668.0, "または次の改築まで", 28, INK, "start", 400))
    if _on(prev, st, "done"):
        s.append(_ctr(1500.0, 430.0, f"{HG_BY}までに", 26, J.TICK, 400))
        s.append(_ctr(1500.0, 560.0, f"{HG_N}か所", 84, J.AMBER, 520, "Dela") + _ctr(1500.0, 664.0, f"{HG_CO}社の曲線", 30, INK, 400))
    return s


# ══════════════════════════════════════════════════════════
#  book_seat（c811）＝会社（建物の印）に、決まりの本（安全管理規程）と責任者の席（安全統括管理者）＝2006年の鉄道事業法の改正（R1 p.250）
# ══════════════════════════════════════════════════════════
BS_YEAR = 2006


def book_seat_base(st0):
    return [_bldg(200.0, 400.0, 660.0, 800.0, J.LINE), _ctr(430.0, 372.0, "会社ごとに", 26, J.TICK, 300)]


def book_seat_stage(prev, st):
    s = []
    if _on(prev, st, "rule"):
        s.append(_chip(1200.0, 340.0, f"{BS_YEAR}年・鉄道事業法の改正", INK, 24))
        s.append(F.poly([(800.0, 540.0), (920.0, 520.0), (1040.0, 540.0), (1040.0, 690.0), (920.0, 670.0), (800.0, 690.0)], J.BG2, J.AMBER, 5, close=True)
                 + F.line(920.0, 520.0, 920.0, 670.0, J.AMBER, 4))
        s.append(_ctr(920.0, 740.0, "安全管理規程", 30, INK, 320) + _ctr(920.0, 784.0, "安全の決まり", 24, J.TICK, 300))
        s.append(_arrow(670.0, 600.0, 786.0, 600.0, J.LINE, 4, 16))
    if _on(prev, st, "seat"):
        # 🔧 試し焼き（40257662340）：細い背もたれの上の丸い印が人の形（頭と体）に見えた＝背もたれを板にし、四角の名札を板の中へ
        s.append(F.rect(1330.0, 430.0, 150.0, 170.0, J.BG2, J.LINE, 6, rx=10) + F.rect(1320.0, 600.0, 190.0, 28.0, J.LINE, None, None, rx=6)
                 + F.line(1340.0, 628.0, 1340.0, 690.0, J.LINE, 6) + F.line(1490.0, 628.0, 1490.0, 690.0, J.LINE, 6)
                 + F.rect(1370.0, 470.0, 70.0, 40.0, J.AMBER, None, None, rx=6))
        s.append(_ctr(1420.0, 740.0, "安全統括管理者", 30, INK, 360) + _ctr(1420.0, 784.0, "安全の責任者", 24, J.TICK, 300))
        s.append(_arrow(1060.0, 600.0, 1310.0, 600.0, J.LINE, 4, 16))
    return s


# ══════════════════════════════════════════════════════════
#  kengi3（c812）＝2007年の建議（2007年6月28日）の書類と3つの印：① 罰しない報告の仕組み ② 走行中の無線のメモは禁止 ③ 機器の作り手まで行き渡らせる
#  （K07 p.1〜2）。c418（3つの箱）とは別の見た目＝印と短い字
# ══════════════════════════════════════════════════════════
KG3 = (("罰しない", "報告の仕組み"), ("走行中の無線", "メモは禁止"), ("機器の作り手", "まで行き渡らせる"))
KG3_XS = (450.0, 960.0, 1470.0)


def _kg_icon(i, x):
    col = sc("ken")
    if i == 0:
        return (_doc(x - 70, 500.0, 120.0, 150.0, J.LINE, 3)
                + F.poly([(x + 60, 520.0), (x + 110, 536.0), (x + 110, 590.0), (x + 60, 630.0), (x + 10, 590.0), (x + 10, 536.0)], J.BG2, col, 5, close=True))
    if i == 1:
        return (_radio(x - 50, 590.0, 1.4, J.LINE) + F.line(x + 30, 640.0, x + 100, 520.0, J.LINE, 8) + _xmark(x + 64, 580.0, 30))
    g = [F.circ(x - 50, 575.0, 50.0, J.BG2, J.LINE, 6)]
    for k in range(8):
        a = math.radians(k * 45)
        g.append(F.line(x - 50 + 50 * math.cos(a), 575 + 50 * math.sin(a), x - 50 + 70 * math.cos(a), 575 + 70 * math.sin(a), J.LINE, 10))
    g.append(_arrow(x + 30, 575.0, x + 110, 575.0, col, 5, 18))
    return "".join(g)


def kengi3_base(st0):
    return [F.rect(160.0, 330.0, 1600.0, 500.0, J.BG2, sc("ken"), 5, rx=14),
            _tline(200.0, 384.0, "建議（2007年6月28日・事故調査委員会）", 26, sc("ken"), "start", 900), F.line(180.0, 410.0, 1740.0, 410.0, sc("ken"), 3)]


def _kg(i):
    x = KG3_XS[i]
    a, b = KG3[i]
    return _ctr(x - 150, 460.0, "①②③"[i], 34, sc("ken"), 60) + _kg_icon(i, x) + _ctr(x, 720.0, a, 30, INK, 420) + _ctr(x, 770.0, b, 28, INK, 420)


def kengi3_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_kg(0))
    if _on(prev, st, "bc"):
        s += [_kg(1), _kg(2)]
    return s


# ══════════════════════════════════════════════════════════
#  第8章
#  plates4（c901）＝裁判所の印（神戸地裁・最高裁＝白黒の章の線の色）と、起訴された4人の机の名札（役職だけ・顔は描かない）：
#  元幹部（のちに社長）1人・歴代の社長 3人（国会 2023年3月8日 の法務省の答弁＝4名）
# ══════════════════════════════════════════════════════════
PL4 = (("元幹部", "のちに社長"), ("歴代の社長", ""), ("歴代の社長", ""), ("歴代の社長", ""))
PL4_XS = (330.0, 830.0, 1160.0, 1490.0)
PL4_N = (4, 1, 3)


def _court(cx, cy, s=1.0, col=None):
    c = col or sc("ct")
    g = [F.poly([(cx - 110 * s, cy - 40 * s), (cx + 110 * s, cy - 40 * s), (cx, cy - 90 * s)], J.BG2, c, 4, close=True),
         F.rect(cx - 104 * s, cy + 70 * s, 208 * s, 18 * s, c, None, None)]
    for k in range(4):
        g.append(F.rect(cx - 86 * s + k * 52 * s, cy - 30 * s, 16 * s, 96 * s, c, None, None))
    return "".join(g)


def _plate(x, t1, t2, col):
    return (F.poly([(x - 120, 640.0), (x + 120, 640.0), (x + 140, 770.0), (x - 140, 770.0)], J.BG2, col, 5, close=True)
            + _ctr(x, 690.0, t1, 30, INK, 240) + (_ctr(x, 738.0, t2, 24, J.TICK, 240) if t2 else ""))


def plates4_base(st0):
    return []


def plates4_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_court(CX, 420.0) + _qmark(1130.0, 410.0, 60) + _ctr(CX, 540.0, "刑事裁判", 26, J.TICK, 300))
    if _on(prev, st, "one"):
        s.append(_chip(560.0, 360.0, f"起訴 {PL4_N[0]}人", J.AMBER, 30))
        s.append(_plate(PL4_XS[0], *PL4[0], sc("jr")) + _ctr(PL4_XS[0], 612.0, f"{PL4_N[1]}人", 26, J.AMBER, 120))
    if _on(prev, st, "three"):
        for x, (a, b) in zip(PL4_XS[1:], PL4[1:]):
            s.append(_plate(x, a, b, sc("jr")))
        s.append(_ctr(PL4_XS[2], 612.0, f"{PL4_N[2]}人", 26, J.AMBER, 120))
    return s


# ══════════════════════════════════════════════════════════
#  duty（c903）＝元幹部の歩み（事故 2005年4月 → 社長に → 起訴のあとに退く＝S3 p.6）と、問われた義務の矢印（指示すべき義務＝S3 p.4）：
#  元幹部（鉄道本部長などのころ）→ 担当の部署 → この曲線に ATS（点線＝付いていない）
# ══════════════════════════════════════════════════════════
def duty_base(st0):
    return []


def duty_stage(prev, st):
    s = []
    if _on(prev, st, "career"):
        s.append(_chip(400.0, 400.0, "事故（2005年4月）", J.ALERT, 26) + _arrow(570.0, 400.0, 720.0, 400.0, J.LINE, 4, 16))
        s.append(_chip(860.0, 400.0, "社長に", sc("jr"), 28) + _arrow(980.0, 400.0, 1130.0, 400.0, J.LINE, 4, 16))
        s.append(_chip(1380.0, 400.0, "起訴のあとに退く", J.TICK, 26))
    if _on(prev, st, "duty"):
        s.append(F.rect(180.0, 590.0, 360.0, 120.0, J.BG2, sc("jr"), 5, rx=14) + _ctr(360.0, 632.0, "元幹部", 30, INK, 300)
                 + _ctr(360.0, 676.0, "鉄道本部長などのころ", 22, J.TICK, 330))
        s.append(_arrow(550.0, 650.0, 760.0, 650.0, J.AMBER, 6, 22) + _ctr(655.0, 610.0, "指示すべき義務", 28, J.AMBER, 300))
        s.append(F.rect(770.0, 600.0, 320.0, 100.0, J.BG2, J.LINE, 4, rx=14) + _ctr(930.0, 650.0, "担当の部署", 28, INK, 280))
        s.append(_arrow(1100.0, 650.0, 1320.0, 650.0, J.LINE, 5, 20))
        s.append(F.rect(1330.0, 590.0, 400.0, 120.0, J.BG2, J.ALERT, 5, rx=14, dash="14 10") + _ctr(1530.0, 650.0, "この曲線に ATS", 30, INK, 360))
    return s


# ══════════════════════════════════════════════════════════
#  verdict（c904）＝判決の表紙の形（神戸地裁・2012年1月）：無罪・検察の求刑 禁錮3年（S3 p.66）。判決の日は2つの日付が割れる＝月まで
# ══════════════════════════════════════════════════════════
VD_DAY, VD_ASK = "2012年1月", "禁錮3年"


def verdict_base(st0):
    return [F.rect(560.0, 320.0, 800.0, 500.0, J.BG2, sc("ct"), 6, rx=12), _ctr(CX, 382.0, "神戸地裁の判決", 30, sc("ct"), 600),
            _ctr(CX, 428.0, VD_DAY, 28, J.TICK, 400), F.line(600.0, 458.0, 1320.0, 458.0, sc("ct"), 3)]


def verdict_stage(prev, st):
    s = []
    if _on(prev, st, "v"):
        s.append(_ctr(CX, 610.0, "無罪", 140, INK, 600))
        s.append(_chip(CX, 750.0, f"検察の求刑：{VD_ASK}", J.TICK, 26))
    return s


# ══════════════════════════════════════════════════════════
#  word_swap（c906）＝言い方の札の入れ替え：「予見でき｜なかった？」（認めたのではない）→「予見できた｜とは認められない」（義務を課すほど）→
#  犯罪の証明がない（判決の結び＝S3 p.66）。引用は2つの札に割る（門番 echo）。c916（判子の ✕ と ○）とは別の見た目
# ══════════════════════════════════════════════════════════
def word_swap_base(st0):
    return []


def word_swap_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(F.rect(560.0, 380.0, 300.0, 84.0, J.BG2, INK, 4, rx=10) + _ctr(710.0, 422.0, "予見でき", 36, INK, 280))
        s.append(F.rect(872.0, 380.0, 280.0, 84.0, J.BG2, J.TICK, 4, rx=10, dash="12 8") + _ctr(1012.0, 422.0, "なかった", 36, J.TICK, 260))
        s.append(_qmark(1200.0, 422.0, 56))
    if _on(prev, st, "swap"):
        # 🔧 geom_gap：取り消し線が字を貫く＝線をやめて札の下に ✕
        s.append(_xmark(1012.0, 500.0, 18) + _ctr(1012.0, 352.0, "と認めたのではない", 22, J.ALERT, 300))
        s.append(_tline(400.0, 548.0, "義務を課すほど", 26, J.TICK, "start", 400))
        s.append(F.rect(400.0, 570.0, 320.0, 84.0, J.BG2, INK, 4, rx=10) + _ctr(560.0, 612.0, "予見できた", 36, INK, 300))
        s.append(F.rect(732.0, 570.0, 500.0, 84.0, J.BG2, sc("ct"), 6, rx=10) + _ctr(982.0, 612.0, "とは認められない", 36, INK, 470))
    if _on(prev, st, "end"):
        s.append(_arrow(816.0, 664.0, 816.0, 724.0, J.LINE, 5, 18))
        s.append(_chip(CX, 772.0, "犯罪の証明がない（判決の結び）", sc("ct"), 30))
    return s


# ══════════════════════════════════════════════════════════
#  bypass（c908）＝強制起訴の回り道：事件 → 検察：起訴しない（遮断）→ 市民の検察審査会の議決（回り道）→ 起訴（指定弁護士＝S2 p.1）
#  （国会 2011年2月21日・2013年11月13日・最高裁）。c807（横の流れの枝分かれ）とは別の見た目＝遮断と回り道
# ══════════════════════════════════════════════════════════
def bypass_base(st0):
    return [F.rect(160.0, 600.0, 170.0, 80.0, J.BG2, J.LINE, 4, rx=14), _ctr(245.0, 640.0, "事件", 30, INK, 150),
            F.rect(1510.0, 596.0, 220.0, 88.0, J.BG2, INK, 5, rx=14), _ctr(1620.0, 640.0, "起訴", 34, INK, 200),
            F.line(340.0, 640.0, 1500.0, 640.0, J.LINE_DIM, 5, dash="14 10")]


def bypass_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(1620.0, 552.0, 56))
    if _on(prev, st, "stop"):
        s.append(F.rect(744.0, 580.0, 32.0, 120.0, J.ALERT, None, None, rx=6) + _xmark(760.0, 640.0, 34))
        s.append(_ctr(760.0, 744.0, "検察：起訴しない", 28, J.ALERT, 360))
        s.append(_chip(1620.0, 744.0, "強制起訴", J.AMBER, 30))
    if _on(prev, st, "detour"):
        # 🔧 geom_gap：回り道の線が箱の字を貫く＝箱の手前と先で線を切る
        s.append(F.poly([(600.0, 630.0), (600.0, 430.0), (826.0, 430.0)], "none", J.AMBER, 7) + F.line(1234.0, 430.0, 1450.0, 430.0, J.AMBER, 7)
                 + _arrow(1450.0, 430.0, 1560.0, 590.0, J.AMBER, 7, 26))
        s.append(F.rect(830.0, 390.0, 400.0, 80.0, J.BG2, J.AMBER, 5, rx=14) + _ctr(1030.0, 430.0, "検察審査会（市民）", 28, INK, 380))
        s.append(_ctr(1030.0, 510.0, "議決", 28, J.AMBER, 200))
        s.append(_ctr(1620.0, 820.0, "指定弁護士が起訴", 24, J.TICK, 300))
    return s


# ══════════════════════════════════════════════════════════
#  relay3（c909）＝3人の社長の時期の階段の帯（横は年に比例＝1年＝100画素）：1992年6月〜1997年3月・1997年4月〜2003年4月・2003年4月〜2006年2月（S2 p.1）
#  → 付け替え（1996年12月）と事故（2005年4月）の線（役職だけ）
# ══════════════════════════════════════════════════════════
RL = dict(x0=200.0, y0=1992.0, k=100.0, ys=(430.0, 530.0, 630.0), h=64.0)
RL_T = (((1992, 6), (1997, 3)), ((1997, 4), (2003, 4)), ((2003, 4), (2006, 2)))
RL_MK = (("付け替え（1996年12月）", (1996, 12, 20), "LINE"), ("事故（2005年4月）", (2005, 4, 25), "ALERT"))


def rl_x(t):
    return RL["x0"] + (t - RL["y0"]) * RL["k"]


def rl_span(i):
    (ya, ma), (yb, mb) = RL_T[i]
    return rl_x(_ym(ya, ma)), rl_x(_ym(yb, mb) + 1 / 12.0)


def relay3_base(st0):
    return [_tline(RL["x0"], 360.0, "歴代の社長（3人）", 26, sc("jr"), "start", 400)]


def relay3_stage(prev, st):
    s = []
    if _on(prev, st, "bars"):
        for i in range(3):
            a, b = rl_span(i)
            y = RL["ys"][i]
            (ya, _ma), (yb, _mb) = RL_T[i]
            s.append(F.rect(a, y - RL["h"] / 2, b - a, RL["h"], J.BG2, sc("jr"), 5, rx=10))
            s.append(_tline(a + 10, y + 9, f"{ya}年〜{yb}年", 23, INK, "start", b - a - 24))   # 🔧 geom_gap：事故の線が3本目の字を貫く＝字を小さく
    if _on(prev, st, "mark"):
        for t, (y_, m_, d_), c in RL_MK:
            x = rl_x(_ym(y_, m_, d_))
            s.append(F.line(x, 386.0, x, 760.0, rc(c), 4, dash="12 8" if c == "LINE" else None))
            s.append(_ctr(x, 798.0, t, 24, rc(c) if c != "LINE" else J.TICK, 340))
    return s


# ══════════════════════════════════════════════════════════
#  scatter（c911）＝管内の同じような曲線（2000か所以上＝点の数は模式・数えない）の中の1つ（この曲線）：特に危ないと認識できた
#  とは認められない（最高裁 2017年＝S2 p.5）。c701（数えた点の升目）とは別の見た目＝散らばった曲線の印
# ══════════════════════════════════════════════════════════
SCT_N = 230
SCT_HI = (980.0, 600.0)
SCT_OUT = ((1260.0, 310.0, 1790.0, 450.0), (820.0, 540.0, 1160.0, 730.0), (150.0, 680.0, 820.0, 830.0), (150.0, 320.0, 520.0, 400.0))


def sct_pts():
    out, x = [], 12345
    while len(out) < SCT_N:
        x = (x * 1103515245 + 12345) % 2147483648
        px = 170.0 + (x % 15900) / 10.0
        x = (x * 1103515245 + 12345) % 2147483648
        py = 340.0 + (x % 4700) / 10.0
        x = (x * 1103515245 + 12345) % 2147483648
        rot = float(x % 360)
        if any(a <= px <= c and b <= py <= d for a, b, c, d in SCT_OUT):
            continue
        if any((px - qx) ** 2 + (py - qy) ** 2 < 34 ** 2 for qx, qy, _r in out):
            continue
        out.append((px, py, rot))
    return out


def scatter_base(st0):
    return ["".join(F.poly(_arcpts(x, y, 13.0, 13.0, r, r + 100.0, 6), "none", J.LINE_DIM, 4) for x, y, r in sct_pts())]


def scatter_stage(prev, st):
    s = []
    if _on(prev, st, "many"):
        s.append(_ctr(1520.0, 352.0, "2000か所以上", 34, J.AMBER, 420) + _ctr(1520.0, 404.0, "同じような曲線", 26, J.TICK, 360))
        s.append(_stag(335.0, 360.0, "ct", "最高裁（2017年）", 24))
    if _on(prev, st, "one"):
        x, y = SCT_HI
        s.append(F.poly(_arcpts(x, y, 30.0, 30.0, 200.0, 340.0, 10), "none", J.AMBER, 10))
        s.append(_ctr(x, y + 74, "この曲線", 30, J.AMBER, 240))
        s.append(_tline(200.0, 730.0, "特に危ないと", 28, INK, "start", 400))
        s.append(_tline(200.0, 782.0, "認識できた", 28, INK, "start", 160) + _tline(350.0, 782.0, "とは認められない", 28, sc("ct"), "start", 300))
    return s


# ══════════════════════════════════════════════════════════
#  stamps4（c914）＝4枚の書類と「無罪」の判（四角＝輪の真ん中に字を置かない）：元幹部 神戸地裁 2012年1月／歴代の社長 神戸地裁 2013年9月・最高裁 2017年6月
#  （国会 2023年3月8日 の法務省の答弁＝いずれも無罪＝高裁の日付は言わない＝台本 §1-5）
# ══════════════════════════════════════════════════════════
SP4 = (("元幹部", ("神戸地裁", "2012年1月")), ("歴代の社長", ("神戸地裁 2013年9月", "最高裁 2017年6月")),
       ("歴代の社長", ("神戸地裁 2013年9月", "最高裁 2017年6月")), ("歴代の社長", ("神戸地裁 2013年9月", "最高裁 2017年6月")))
SP4_XS = (330.0, 760.0, 1190.0, 1620.0)


def stamps4_base(st0):
    return []


def stamps4_stage(prev, st):
    s = []
    if _on(prev, st, "who"):
        s.append(_stag(CX, 332.0, "kok", "2023年の国会：法務省の答弁", 24))
        for x, (t, _c) in zip(SP4_XS, SP4):
            s.append(F.rect(x - 180, 400.0, 360.0, 400.0, J.BG2, J.LINE, 4, rx=10) + _ctr(x, 448.0, t, 28, INK, 320))
    if _on(prev, st, "done"):
        for x, (_t, (a, b)) in zip(SP4_XS, SP4):
            s.append(F.rect(x - 100, 500.0, 200.0, 110.0, "none", INK, 6, rx=14) + _ctr(x, 555.0, "無罪", 60, INK, 180))
            s.append(_ctr(x, 680.0, a, 22, J.TICK, 330) + _ctr(x, 720.0, b, 22, J.TICK, 330))
    return s


# ══════════════════════════════════════════════════════════
#  podium（c915）＝演台と吹き出し（2023年3月8日・参議院 予算委員会・国土交通省 鉄道局長）：事業許可の取り消しなど 行政処分は行っていない
#  （人は描かない＝演台とマイクだけ）
# ══════════════════════════════════════════════════════════
PD_DAY = "2023年3月8日"


def podium_base(st0):
    return []


def podium_stage(prev, st):
    s = []
    col = sc("kok")
    if _on(prev, st, "who"):
        s.append(_stag(CX, 336.0, "kok", f"{PD_DAY}・参議院 予算委員会", 24))
        s.append(F.poly([(340.0, 560.0), (580.0, 560.0), (560.0, 780.0), (360.0, 780.0)], J.BG2, col, 5, close=True)
                 + F.line(500.0, 556.0, 540.0, 470.0, J.LINE, 5) + F.circ(544.0, 460.0, 12.0, J.LINE, None))
        s.append(_ctr(460.0, 818.0, "国土交通省 鉄道局長", 26, col, 400))
    if _on(prev, st, "say"):
        s.append(F.rect(760.0, 430.0, 940.0, 330.0, J.BG2, col, 5, rx=24) + F.poly([(760.0, 590.0), (640.0, 620.0), (760.0, 640.0)], J.BG2, col, 5))
        s.append(_ctr(1230.0, 520.0, "事業許可の取り消しなど", 32, INK, 860) + _ctr(1230.0, 590.0, "行政処分は", 32, INK, 600)
                 + _ctr(1230.0, 672.0, "行っていない", 42, J.AMBER, 600))
    return s


# ══════════════════════════════════════════════════════════
#  stamps2（c916）＝2つの言い方の判：「誰も罪に問われなかった」✕（4人は起訴・裁判で問われた）→「有罪になった人はいない」○（台本 §1-4）
# ══════════════════════════════════════════════════════════
def stamps2_base(st0):
    return []


def stamps2_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(F.rect(400.0, 360.0, 1120.0, 120.0, J.BG2, J.TICK, 4, rx=14) + _ctr(960.0, 420.0, "誰も罪に問われなかった", 40, INK, 1000))
    if _on(prev, st, "no"):
        s.append(_xmark(1610.0, 420.0, 44))
        s.append(_tline(560.0, 562.0, "起訴：4人", 30, J.AMBER, "start", 300) + _tline(900.0, 562.0, "裁判で問われた", 30, INK, "start", 400))
    if _on(prev, st, "yes"):
        s.append(F.rect(400.0, 640.0, 1120.0, 120.0, J.BG2, J.AMBER, 6, rx=14) + _ctr(960.0, 700.0, "有罪になった人はいない", 40, INK, 1000))
        s.append(F.circ(1610.0, 700.0, 40.0, "none", J.AMBER, 9))
    return s


# ══════════════════════════════════════════════════════════
#  bench（c917）＝被告人の席（4つ・空の席）と、席の外の2つ：運転士（事故で亡くなった・被告人ではない）／会社そのもの（この裁判では裁かれていない）
# ══════════════════════════════════════════════════════════
BN_SEATS = 4


def bench_base(st0):
    return []


def bench_stage(prev, st):
    s = []
    if _on(prev, st, "seats"):
        s.append(_ctr(CX, 470.0, f"被告人の席：{BN_SEATS}人", 26, J.TICK, 400) + F.line(520.0, 510.0, 1400.0, 510.0, J.LINE, 6))
        for i in range(BN_SEATS):
            s.append(F.rect(550.0 + i * 220.0, 530.0, 160.0, 90.0, J.BG2, J.LINE, 4, rx=14))
        s.append(F.rect(160.0, 676.0, 580.0, 150.0, J.BG2, J.LINE, 4, rx=14, dash="12 8"))
        s.append(_ctr(450.0, 714.0, "運転士", 28, INK, 300) + _ctr(450.0, 754.0, "事故で亡くなった", 24, J.TICK, 400)
                 + _ctr(450.0, 796.0, "被告人ではない", 26, J.AMBER, 400))
    if _on(prev, st, "co"):
        s.append(_bldg(1100.0, 670.0, 1290.0, 830.0, sc("jr"), 2, 2))
        s.append(_tline(1330.0, 712.0, "会社そのもの", 28, sc("jr"), "start", 400) + _tline(1330.0, 760.0, "この裁判では", 26, INK, "start", 400)
                 + _tline(1330.0, 806.0, "裁かれていない", 28, J.AMBER, "start", 400))
    return s


# ══════════════════════════════════════════════════════════
#  nested（c918）＝答弁の中の答弁（2023年6月13日・参議院 国土交通委員会・国土交通大臣〈当時〉）：法務省が「慎重に検討する必要」と答えてきた
#  ＝紹介の形（外の吹き出しの中に点線の吹き出し）。組織罰＝会社そのものを罰する。c718（会議録の頁）・c915（演台）とは別の見た目
# ══════════════════════════════════════════════════════════
NS_DAY = "2023年6月13日"


def nested_base(st0):
    return []


def nested_stage(prev, st):
    s = []
    col = sc("kok")
    if _on(prev, st, "word"):
        s.append(_ctr(470.0, 450.0, "組織罰", 44, J.AMBER, 300) + _ctr(470.0, 516.0, "会社そのものを罰する", 26, INK, 400)
                 + _ctr(470.0, 566.0, "国会でも問われた", 26, J.TICK, 400))
    if _on(prev, st, "quote"):
        s.append(_stag(1310.0, 340.0, "kok", f"{NS_DAY}・参議院 国土交通委員会", 22))
        s.append(F.rect(860.0, 400.0, 900.0, 420.0, J.BG2, col, 5, rx=28) + F.poly([(860.0, 560.0), (760.0, 590.0), (860.0, 610.0)], J.BG2, col, 5))
        s.append(_tline(900.0, 452.0, "国土交通大臣（当時）", 26, col, "start", 500))
        s.append(F.rect(920.0, 486.0, 780.0, 290.0, J.BG, J.TICK, 3, rx=22, dash="12 8"))
        s.append(_tline(960.0, 540.0, "法務省：", 28, J.TICK, "start", 300) + _tline(960.0, 604.0, "様々な課題があり", 26, INK, "start", 600)
                 + _tline(960.0, 672.0, "慎重に検討する必要", 34, INK, "start", 640) + _tline(1660.0, 744.0, "と答えてきた", 24, J.TICK, "end", 300))
    return s


# ══════════════════════════════════════════════════════════
#  wall（c922）＝調べる側（事故調査委員会・委員〈当時〉＝青）と調べられる側（会社＝茶）のあいだの壁の割れ目を、情報が漏れる（検証報告書＝白）
#  日付は ca03 だけ（映像方針 §4-9）
# ══════════════════════════════════════════════════════════
def wall_base(st0):
    return []


def wall_stage(prev, st):
    s = []
    if _on(prev, st, "two"):
        s.append(_bldg(160.0, 420.0, 700.0, 760.0, sc("rep"), 3, 2) + _ctr(430.0, 470.0, "調べる側", 30, sc("rep"), 400))
        s.append(_ctr(430.0, 400.0, "事故調査委員会・委員（当時）", 22, INK, 520))
        s.append(_bldg(1220.0, 420.0, 1760.0, 760.0, sc("jr"), 3, 2) + _ctr(1490.0, 470.0, "調べられる側", 30, sc("jr"), 400))
        s.append(_ctr(1490.0, 400.0, "会社", 24, INK, 300))
        for r in range(9):
            for c in range(2):
                x = 870.0 + c * 100.0 - (50.0 if r % 2 else 0.0)
                x0, x1 = max(860.0, x), min(1060.0, x + 96.0)
                s.append(F.rect(x0, 380.0 + r * 46.0, x1 - x0, 40.0, J.BG2, J.LINE_DIM, 3, rx=3))
        s.append(_stag(430.0, 808.0, "kv", "検証報告書", 22))
    if _on(prev, st, "leak"):
        s.append(F.poly([(950.0, 520.0), (980.0, 570.0), (940.0, 620.0), (975.0, 670.0), (950.0, 720.0)], "none", J.ALERT, 6))
        s.append(_arrow(710.0, 620.0, 1210.0, 620.0, J.ALERT, 6, 24, dash="14 10"))
        s.append(_doc(760.0, 650.0, 70.0, 90.0, J.ALERT, 2, 3) + _doc(1110.0, 650.0, 70.0, 90.0, J.ALERT, 2, 3))
        s.append(_ctr(CX, 340.0, "情報が漏れた", 30, J.ALERT, 360))
    return s


# ══════════════════════════════════════════════════════════
#  第9章
#  role_lines（ca03）＝日付の札（2009年9月25日 分かった）と役職の線：社長（当時）ら → 求め → 委員（当時）／委員（当時）→ 調べの情報 → 会社（S1 p.1）
# ══════════════════════════════════════════════════════════
RLN_DAY = "2009年9月25日"


def role_lines_base(st0):
    return []


def role_lines_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_ctr(CX, 340.0, RLN_DAY, 32, J.AMBER, 400) + _ctr(CX, 388.0, "分かった", 24, J.TICK, 200))
        s.append(F.rect(300.0, 500.0, 400.0, 130.0, J.BG2, sc("rep"), 5, rx=16) + _ctr(500.0, 540.0, "事故調査委員会", 22, J.TICK, 360)
                 + _ctr(500.0, 590.0, "委員（当時）", 32, INK, 360))
        s.append(_stag(CX, 790.0, "kv", "検証報告書", 22))
    if _on(prev, st, "b"):
        s.append(F.rect(1220.0, 500.0, 400.0, 130.0, J.BG2, sc("jr"), 5, rx=16) + _ctr(1420.0, 540.0, "JR西日本", 22, J.TICK, 360)
                 + _ctr(1420.0, 590.0, "社長（当時）ら", 32, INK, 360))
        s.append(_arrow(1212.0, 530.0, 708.0, 530.0, sc("jr"), 5, 22) + _ctr(CX, 500.0, "求め", 28, sc("jr"), 200))
    if _on(prev, st, "c"):
        s.append(_arrow(708.0, 604.0, 1212.0, 604.0, J.ALERT, 5, 22, dash="14 10") + _ctr(CX, 660.0, "調べの情報", 28, J.ALERT, 300))
    return s


# ══════════════════════════════════════════════════════════
#  ring12（ca04）＝丸い机と12の席（人の形は描かない＝席の数＝検証のチーム12人＝S1 p.2）・2009年11月10日・遺族と負傷者も（家族を含む）
#  🔴 輪の真ん中に字を置かない（layout）＝字は輪の右
# ══════════════════════════════════════════════════════════
RG12 = dict(cx=640.0, cy=580.0, r=160.0, rs=246.0, s=46.0)
RG12_N = 12
RG12_DAY = "2009年11月10日"


def ring12_base(st0):
    return []


def ring12_stage(prev, st):
    s = []
    if _on(prev, st, "team"):
        s.append(F.circ(RG12["cx"], RG12["cy"], RG12["r"], J.BG2, sc("kv"), 5))
        for i in range(RG12_N):
            a = math.radians(-90 + i * 360 / RG12_N)
            x, y = RG12["cx"] + RG12["rs"] * math.cos(a), RG12["cy"] + RG12["rs"] * math.sin(a)
            s.append(F.rect(x - RG12["s"] / 2, y - RG12["s"] / 2, RG12["s"], RG12["s"], J.BG2, sc("kv"), 4, rx=10))
        s.append(_tline(1000.0, 430.0, "検証のチーム", 30, INK, "start", 400))
        s.append(_tline(1000.0, 530.0, f"{RG12_N}人", 76, J.AMBER, "start", 300, "Dela"))
        s.append(_tline(1000.0, 594.0, RG12_DAY, 26, J.TICK, "start", 400) + _tline(1000.0, 636.0, "運輸安全委員会が置いた", 24, J.TICK, "start", 500))
    if _on(prev, st, "also"):
        s.append(F.rect(990.0, 690.0, 640.0, 120.0, J.BG2, J.AMBER, 4, rx=14) + _ctr(1310.0, 732.0, "遺族と負傷者も", 30, INK, 600)
                 + _ctr(1310.0, 778.0, "（家族を含む）", 24, J.TICK, 400))
    return s


# ══════════════════════════════════════════════════════════
#  links6（ca06）＝4人の委員（当時）と会社の人の6本の線（接触の6件＝S1 p.31・名前は出さない＝役職だけ）。1人目から3本・ほかは1本ずつ
# ══════════════════════════════════════════════════════════
LK_YS = (400.0, 520.0, 640.0, 760.0)
LK_TO = ((0, 430.0), (0, 490.0), (0, 550.0), (1, 610.0), (2, 670.0), (3, 740.0))


def links6_base(st0):
    g = [_ctr(460.0, 340.0, "委員（当時）4人", 26, sc("rep"), 400)]
    for y in LK_YS:
        g.append(F.rect(300.0, y - 36, 320.0, 72.0, J.BG2, sc("rep"), 4, rx=14) + _ctr(460.0, y, "委員（当時）", 26, INK, 290))
    g.append(F.rect(1240.0, 380.0, 460.0, 420.0, J.BG2, sc("jr"), 5, rx=16) + _ctr(1490.0, 560.0, "会社の人", 32, sc("jr"), 300)
             + _ctr(1490.0, 606.0, "JR西日本", 24, J.TICK, 300))
    return g


def links6_stage(prev, st):
    s = []
    if _on(prev, st, "all"):
        for k, (i, y) in enumerate(LK_TO):
            s.append(F.line(626.0, LK_YS[i], 1236.0, y, J.AMBER, 4))
            s.append(_tline(1262.0, y + 9, "①②③④⑤⑥"[k], 26, J.AMBER, "start", 40))
        s.append(_ctr(CX, 352.0, f"接触：{len(LK_TO)}件", 34, J.AMBER, 300))
        s.append(_stag(1490.0, 740.0, "kv", "検証報告書", 22))
    return s


# ══════════════════════════════════════════════════════════
#  tl_leak（ca07）＝縦の年表（1か月＝17画素）：事故（2005年4月25日）・建議（2005年9月）→ 意見を聞くための案の公表（2006年12月20日）→
#  公表の2日前（2006年12月18日）→ 全文のコピー → 会社の担当部長（S1 p.24・p.32）。c710（横の年表）の相方
# ══════════════════════════════════════════════════════════
TLK = dict(x=560.0, y0=360.0, k=17.0, y1=820.0)
TLK_EV = (("事故", (2005, 4, 25), "ALERT"), ("建議", (2005, 9, 6), "bldg_a"), ("意見を聞くための案：公表", (2006, 12, 20), "state"))
TLK_LEAK = (2006, 12, 18)


def tlk_y(y, m, d=1):
    return TLK["y0"] + ((y - 2005) * 12 + (m - 4) + (d - 1) / 31.0) * TLK["k"]


def tl_leak_base(st0):
    g = [_arrow(TLK["x"], TLK["y0"] - 20, TLK["x"], TLK["y1"] + 20, J.LINE, 5, 18)]
    for yy in (2006, 2007):
        y = tlk_y(yy, 1)
        g.append(F.line(TLK["x"] - 16, y, TLK["x"] + 16, y, J.LINE, 4) + _tline(TLK["x"] - 30, y + 9, f"{yy}年", 24, J.TICK, "end", 120))
    for t, d, c in TLK_EV[:2]:
        y = tlk_y(*d)
        g.append(F.circ(TLK["x"], y, 12.0, rc(c), J.BG, 3))
        g.append(_tline(TLK["x"] + 34, y + 9, f"{t}（{d[0]}年{d[1]}月" + (f"{d[2]}日）" if c == "ALERT" else "）"), 24, rc(c), "start", 500))
    return g


def tl_leak_stage(prev, st):
    s = []
    if _on(prev, st, "draft"):
        t, d, c = TLK_EV[2]
        y = tlk_y(*d)
        s.append(F.poly([(TLK["x"], y - 16), (TLK["x"] + 16, y), (TLK["x"], y + 16), (TLK["x"] - 16, y)], rc(c), J.BG, 3, close=True))
        s.append(_tline(TLK["x"] + 34, y + 10, t, 28, rc(c), "start", 520) + _tline(TLK["x"] + 34, y + 48, f"{d[0]}年{d[1]}月{d[2]}日", 24, J.TICK, "start", 300))
    if _on(prev, st, "two"):
        y = tlk_y(*TLK_LEAK)
        s.append(F.line(TLK["x"] + 4, y, TLK["x"] + 60, 600.0, J.ALERT, 4))
        s.append(_tline(TLK["x"] + 70, 594.0, f"{TLK_LEAK[0]}年{TLK_LEAK[1]}月{TLK_LEAK[2]}日", 28, J.ALERT, "start", 400)
                 + _tline(TLK["x"] + 70, 630.0, "公表の2日前", 24, J.ALERT, "start", 300))
    if _on(prev, st, "copy"):
        s.append(_doc(1120.0, 520.0, 110.0, 140.0, J.ALERT, 3) + _arrow(980.0, 590.0, 1108.0, 590.0, J.ALERT, 5, 20))
        s.append(_arrow(1242.0, 590.0, 1370.0, 590.0, J.ALERT, 5, 20) + _ctr(1176.0, 700.0, "全文のコピー", 26, J.ALERT, 300))
        s.append(F.rect(1380.0, 540.0, 380.0, 110.0, J.BG2, sc("jr"), 5, rx=14) + _ctr(1570.0, 595.0, "会社の担当部長", 28, INK, 340))
    return s


# ══════════════════════════════════════════════════════════
#  handover（ca08）＝最終の報告書（公表 2007年6月28日）の全文のコピーが、公表の3日前（2007年6月25日）に会社の手へ（コピーは動く部品＝S1 p.32）
# ══════════════════════════════════════════════════════════
HO = dict(x0=560.0, y0=470.0, w=120.0, h=150.0, dx=760.0)
HO_DAY, HO_PUB = "2007年6月25日", "2007年6月28日"


def handover_parts(st):
    a = 1.0 if st.get("date") == "on" else 0.0
    dx = HO["dx"] if st.get("move") == "on" else 0.0
    x0, y0, w, h = HO["x0"], HO["y0"], HO["w"], HO["h"]
    return [_P("copy", "poly", [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], fill=J.BG2, stroke=J.ALERT, w=5, dx=dx, alpha=a)]


def handover_base(st0):
    g = []
    for k in range(3):
        g.append(_doc(220.0 + k * 14, 400.0 + k * 14, 280.0, 320.0, sc("rep"), 4))
    g.append(_ctr(374.0, 778.0, "最終の報告書", 28, sc("rep"), 340) + _ctr(374.0, 820.0, f"公表：{HO_PUB}", 24, J.TICK, 340))
    g.append(F.rect(1260.0, 420.0, 500.0, 290.0, J.BG2, sc("jr"), 5, rx=16) + _ctr(1620.0, 470.0, "会社", 34, sc("jr"), 200))
    return g


def handover_stage(prev, st):
    s = []
    if _on(prev, st, "date"):
        s.append(_ctr(960.0, 360.0, HO_DAY, 32, J.AMBER, 400) + _ctr(960.0, 408.0, "公表の3日前", 26, INK, 300))
    if _on(prev, st, "move"):
        s.append(_ctr(960.0, 690.0, "全文のコピー", 28, J.ALERT, 300))
    if _on(prev, st, "inside"):
        s.append(_ctr(1590.0, 664.0, "そのまま会社の手に", 26, INK, 300))
    return s


# ══════════════════════════════════════════════════════════
#  bundle（ca09）＝頁の束（第3章の一部・第4章以降）→ 社長（当時）（2007年6月17日）→ いちばん役に立った＝意見を聞く会の日程（S1 p.31・p.32）
# ══════════════════════════════════════════════════════════
BU_DAY = "2007年6月17日"


def bundle_base(st0):
    return []


def bundle_stage(prev, st):
    s = []
    if _on(prev, st, "who"):
        s.append(_ctr(520.0, 360.0, BU_DAY, 30, J.AMBER, 400))
        s.append(F.rect(1300.0, 390.0, 400.0, 120.0, J.BG2, sc("jr"), 5, rx=16) + _ctr(1500.0, 450.0, "社長（当時）", 32, INK, 360))
    if _on(prev, st, "pages"):
        for k in range(3):
            s.append(_doc(260.0 + k * 16, 440.0 + k * 16, 340.0, 300.0, J.LINE, 4))
        s.append(F.rect(630.0, 520.0, 200.0, 50.0, J.BG2, J.AMBER, 4, rx=8) + _ctr(730.0, 545.0, "第3章（一部）", 22, INK, 190))
        s.append(F.rect(630.0, 600.0, 200.0, 50.0, J.BG2, J.AMBER, 4, rx=8) + _ctr(730.0, 625.0, "第4章〜", 22, INK, 190))
        s.append(_arrow(850.0, 560.0, 1290.0, 470.0, J.ALERT, 5, 22))
    if _on(prev, st, "sched"):
        s.append(F.rect(1100.0, 600.0, 600.0, 200.0, J.BG2, INK, 4, rx=12) + _ctr(1400.0, 640.0, "意見を聞く会の日程", 26, INK, 560))
        for k in range(3):
            s.append(F.line(1140.0, 690.0 + k * 34, 1560.0 - k * 60, 690.0 + k * 34, J.LINE_DIM, 6))
        c = (1660.0, 600.0)
        star = [(c[0] + (30 if k % 2 == 0 else 13) * math.cos(math.radians(-90 + k * 36)), c[1] + (30 if k % 2 == 0 else 13) * math.sin(math.radians(-90 + k * 36)))
                for k in range(10)]
        s.append(F.poly(star, J.AMBER, J.BG, 2, close=True))
        s.append(_ctr(1400.0, 836.0, "いちばん役に立った", 26, J.AMBER, 400))
    return s


# ══════════════════════════════════════════════════════════
#  jyanken（ca12）＝「優先的に」（報告書の案の字句＝青）→ 社長（当時）の吹き出し「後出しじゃんけん」（茶）＝と話している（検証報告書＝S1 p.14）
#  手は描かない（台本 §1-4）
# ══════════════════════════════════════════════════════════
def jyanken_base(st0):
    return []


def jyanken_stage(prev, st):
    s = []
    if _on(prev, st, "say"):
        s.append(F.rect(300.0, 460.0, 440.0, 120.0, J.BG2, sc("rep"), 5, rx=16) + _ctr(520.0, 520.0, "「優先的に」", 40, sc("rep"), 420))
        s.append(_ctr(520.0, 616.0, "報告書の案の字句", 22, J.TICK, 400))
        s.append(_arrow(760.0, 520.0, 1000.0, 520.0, J.LINE, 5, 20))
        s.append(_tline(1060.0, 420.0, "社長（当時）", 26, sc("jr"), "start", 300))
        s.append(F.rect(1060.0, 450.0, 680.0, 160.0, J.BG2, sc("jr"), 5, rx=28) + _ctr(1400.0, 530.0, "後出しじゃんけん", 44, INK, 640))
    if _on(prev, st, "told"):
        s.append(_stag(1400.0, 700.0, "kv", "検証報告書", 22) + _ctr(1400.0, 760.0, "と話している", 24, J.TICK, 300))
    return s


# ══════════════════════════════════════════════════════════
#  meeting（ca15）＝上から見た机（席の数は描かない）と委員（当時）の席・発言の吹き出し（2007年6月11日の委員懇談会）・審議の録音（S1 p.51）
#  ca04（丸い机と12の席）とは別の見た目＝長い机と録音機
# ══════════════════════════════════════════════════════════
MT_DAY = "2007年6月11日"


def meeting_base(st0):
    return []


def meeting_stage(prev, st):
    s = []
    if _on(prev, st, "seat"):
        s.append(_chip(1060.0, 340.0, f"{MT_DAY}・委員懇談会", J.TICK, 24))
        s.append(F.rect(520.0, 470.0, 780.0, 180.0, J.BG2, J.LINE, 4, rx=14))
        s.append(F.rect(670.0, 412.0, 60.0, 42.0, sc("rep"), None, None, rx=10) + _ctr(700.0, 384.0, "委員（当時）", 26, sc("rep"), 300))
        s.append(F.rect(1080.0, 512.0, 150.0, 84.0, J.BG2, J.LINE, 4, rx=10) + F.circ(1120.0, 552.0, 18.0, "none", J.LINE, 4)
                 + F.circ(1190.0, 552.0, 18.0, "none", J.LINE, 4))
        s.append(_ctr(1155.0, 628.0, "審議の録音", 22, J.TICK, 200))
    if _on(prev, st, "say"):
        # 🔧 geom_gap：吹き出しが席の札「委員（当時）」に 8px 重なる＝幅を詰める
        s.append(F.rect(150.0, 290.0, 450.0, 130.0, J.BG2, sc("rep"), 5, rx=24) + F.poly([(560.0, 418.0), (650.0, 434.0), (520.0, 418.0)], J.BG2, sc("rep"), 4))
        s.append(_ctr(390.0, 330.0, "後出しじゃんけん", 32, INK, 440) + _ctr(390.0, 382.0, "的ですね", 32, INK, 300))
        s.append(_ctr(1155.0, 702.0, "録音に残っている", 24, J.AMBER, 300))
    return s


# ══════════════════════════════════════════════════════════
#  waveform（ca16）＝録音の波形（振れは小さい）と、届かない「強い語勢」の線：削ってほしい、とは、はっきり言っていない（検証報告書＝S1 p.51）
# ══════════════════════════════════════════════════════════
WV = dict(x0=260.0, n=64, dx=22.0, y=560.0, amp=58.0, top=150.0)


def wv_amp(i):
    return WV["amp"] * (0.35 + 0.65 * abs(math.sin(i * 0.61) * math.cos(i * 0.23)))


def waveform_base(st0):
    return ["".join(F.line(WV["x0"] + i * WV["dx"], WV["y"] - wv_amp(i), WV["x0"] + i * WV["dx"], WV["y"] + wv_amp(i), J.LINE, 8) for i in range(WV["n"]))]


def waveform_stage(prev, st):
    s = []
    if _on(prev, st, "words"):
        s.append(_chip(520.0, 360.0, "削ってほしい", INK, 28))
        s.append(_tline(700.0, 370.0, "はっきりとは", 26, J.TICK, "start", 300) + _tline(870.0, 370.0, "言っていない", 28, INK, "start", 300))
    if _on(prev, st, "tone"):
        x1 = WV["x0"] + (WV["n"] - 1) * WV["dx"]
        for d in (-1, 1):
            s.append(F.line(WV["x0"] - 20, WV["y"] + d * WV["top"], x1 + 20, WV["y"] + d * WV["top"], J.ALERT, 4, dash="14 10"))
        s.append(_tline(x1 + 20, WV["y"] - WV["top"] - 16, "強い語勢", 26, J.ALERT, "end", 260))
        s.append(_ctr(CX - 120, 790.0, "感じられなかった", 30, INK, 400) + _stag(1360.0, 790.0, "kv", "検証報告書", 22))
    return s


# ══════════════════════════════════════════════════════════
#  open_book（ca20）＝見開きの本（検証報告書＝白）：左の頁＝最終の報告書の内容への影響はなかった（前の ca19 の語り＝基図）／
#  右の頁＝公正であるべき事故調査を歪めた・到底容認されない（S1 p.53）＝どちらにも寄せない
# ══════════════════════════════════════════════════════════
def open_book_base(st0):
    col = sc("kv")
    return [F.poly([(300.0, 360.0), (950.0, 380.0), (950.0, 800.0), (300.0, 780.0)], J.BG2, col, 5, close=True),
            F.poly([(970.0, 380.0), (1620.0, 360.0), (1620.0, 780.0), (970.0, 800.0)], J.BG2, col, 5, close=True),
            F.line(960.0, 370.0, 960.0, 812.0, col, 4),
            _ctr(625.0, 520.0, "最終の報告書の内容への", 30, INK, 600), _ctr(625.0, 590.0, "影響はなかった", 38, INK, 600),
            _ctr(625.0, 660.0, "と判断", 24, J.TICK, 300)]


def open_book_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_ctr(1295.0, 480.0, "公正であるべき", 30, INK, 560) + _ctr(1295.0, 548.0, "事故調査を歪めた", 36, INK, 600))
    if _on(prev, st, "b"):
        s.append(_ctr(1295.0, 670.0, "到底容認されない", 40, J.ALERT, 600))
    return s


# ══════════════════════════════════════════════════════════
#  five_slips（ca22）＝「優先的に」の一文の5枚の紙（検証報告書の中だけで少なくとも5通り＝字は灰の線で伏せる）→ 1枚を引き出す＝
#  最終の報告書（2007年）の原文（R1 p.230）・考えられる
# ══════════════════════════════════════════════════════════
FS_N = 5
FS_PICK = 2
FS_WORD = "考えられる"


def five_slips_base(st0):
    return []


def five_slips_stage(prev, st):
    s = []
    if _on(prev, st, "five"):
        s.append(_stag(460.0, 340.0, "kv", "検証報告書の中", 24))
        for i in range(FS_N):
            x0, y0 = 220.0 + i * 16, 390.0 + i * 78
            s.append(F.rect(x0, y0, 440.0, 66.0, J.BG2, J.LINE, 3, rx=8) + F.line(x0 + 20, y0 + 24, x0 + 400, y0 + 24, J.LINE_DIM, 6)
                     + F.line(x0 + 20, y0 + 44, x0 + 300, y0 + 44, J.LINE_DIM, 6))
        s.append(_ctr(460.0, 830.0, f"少なくとも{FS_N}通り", 30, J.AMBER, 400))
    if _on(prev, st, "pick"):
        x0, y0 = 220.0 + FS_PICK * 16, 390.0 + FS_PICK * 78
        s.append(F.rect(x0 - 6, y0 - 6, 452.0, 78.0, "none", sc("rep"), 6, rx=10))
        s.append(_arrow(x0 + 460, y0 + 33, 850.0, 560.0, sc("rep"), 5, 20))
        s.append(F.rect(860.0, 420.0, 900.0, 300.0, J.BG2, sc("rep"), 5, rx=16))
        s.append(_tline(900.0, 470.0, "最終の報告書（2007年）", 24, sc("rep"), "start", 500) + _tline(900.0, 540.0, "…曲線速照機能の整備は", 28, J.TICK, "start", 800))
        s.append(_tline(900.0, 612.0, "優先的に行うべきであった", 36, INK, "start", 820))
        s.append(_tline(900.0, 684.0, FS_WORD, 26, J.AMBER, "start", 200) + _meter(1060.0, 676.0, FS_WORD))
    return s


# ══════════════════════════════════════════════════════════
#  第10章
#  answer（cb06）＝この動画の答えの札：問い「急いでいたの？」→ 留めた紙（この曲線を、わざと110km/hほどで通ろうとした可能性＝R1 p.222 の主語）→
#  判「低いものと考えられる」（青・升2つ）。🔴 c510 と同じ主語だけ（門番が主語の語を見る）。c510（5つの見出しの札）とは別の見た目
# ══════════════════════════════════════════════════════════
AN_SUBJ = F5_SUBJ
AN_WORD = F5_WORD


def answer_base(st0):
    return []


def answer_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_chip(CX, 344.0, "急いでいたの？", INK, 32))
    if _on(prev, st, "subj"):
        s.append(F.rect(300.0, 430.0, 1320.0, 116.0, J.BG2, INK, 4, rx=6) + F.circ(330.0, 444.0, 14.0, J.AMBER, J.BG, 3)
                 + F.circ(1590.0, 444.0, 14.0, J.AMBER, J.BG, 3))
        s.append(_ctr(CX, 494.0, AN_SUBJ, 32, INK, 1240))
    if _on(prev, st, "stamp"):
        s.append(F.rect(620.0, 600.0, 680.0, 180.0, J.BG2, sc("rep"), 8, rx=20))
        s.append(_ctr(CX, 666.0, AN_WORD, 46, sc("rep"), 620) + _meter(CX - METER_W / 2, 740.0, AN_WORD))
    return s


# ══════════════════════════════════════════════════════════
#  two_causes（cb08）＝左：会社（建物の印）＝運転士の管理のしかた・関与した・可能性が考えられる（R1 p.243）／右：曲線と空の装置の箱＝
#  速度を照らす仕組み：無し（R1 p.230）
# ══════════════════════════════════════════════════════════
TCZ_WORD = "可能性が考えられる"


def two_causes_base(st0):
    return []


def two_causes_stage(prev, st):
    s = []
    if _on(prev, st, "co"):
        s.append(_bldg(180.0, 430.0, 440.0, 720.0, sc("jr"), 2, 3))
        s.append(_tline(500.0, 500.0, "会社の運転士の管理", 30, sc("jr"), "start", 520) + _tline(500.0, 560.0, "関与した", 28, INK, "start", 300))
        s.append(_tline(500.0, 626.0, TCZ_WORD, 26, J.AMBER, "start", 260) + _meter(770.0, 618.0, TCZ_WORD))
    if _on(prev, st, "curve"):
        for rr in (386.0, 414.0):
            s.append(F.poly(_arcpts(1700.0, 840.0, rr, rr, 180.0, 262.0, 20), "none", J.LINE, 5))
        s.append(F.rect(1180.0, 780.0, 50.0, 22.0, "none", J.LINE, 3, rx=4, dash="6 5") + _qmark(1205.0, 730.0, 44))   # 🔧 geom_gap：「？」がレールの上＝線路の脇へ
        s.append(_ctr(1420.0, 380.0, "速度を照らす仕組み", 28, INK, 500) + _ctr(1420.0, 444.0, "無し", 44, J.ALERT, 200))
    return s


# ══════════════════════════════════════════════════════════
#  stones3（cb09）＝3つの飛び石（左から右へ）：① 報告書＝優先的に付けるべきだった（考えられる）② 社長（当時）＝記述を考え直すよう頼んだ（検証報告書）
#  ③ 有罪になった人はいない（国会 2023年）。字は石の上・出どころの札は石の下（輪の中に字を置かない）
# ══════════════════════════════════════════════════════════
ST3_XS = (380.0, 960.0, 1540.0)
ST3_WORD = "考えられる"


def stones3_base(st0):
    pts = [(160.0 + i * 16, 700.0 + 14 * math.sin(i / 6.0)) for i in range(101)]
    return [F.poly(pts, "none", J.LINE_DIM, 5, dash="14 10")]


def _stone(x, col):
    return F.poly(_arcpts(x, 700.0, 140.0, 44.0, 0, 360, 36), J.BG2, col, 6, close=True)


def stones3_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_stone(ST3_XS[0], sc("rep")) + _ctr(ST3_XS[0], 520.0, "優先的に", 34, INK, 400) + _ctr(ST3_XS[0], 578.0, "付けるべきだった", 30, INK, 460))
        s.append(_tline(ST3_XS[0] - 90, 640.0, ST3_WORD, 24, J.AMBER, "start", 160) + _meter(ST3_XS[0] + 40, 632.0, ST3_WORD))
        s.append(_stag(ST3_XS[0], 790.0, "rep", "報告書", 22))
        s.append(_stone(ST3_XS[1], sc("kv")) + _ctr(ST3_XS[1], 470.0, "社長（当時）", 28, sc("jr"), 300))
    if _on(prev, st, "b"):
        s.append(_ctr(ST3_XS[1], 540.0, "記述を考え直すよう", 30, INK, 460) + _ctr(ST3_XS[1], 600.0, "頼んだ", 30, INK, 300))
        s.append(_stag(ST3_XS[1], 790.0, "kv", "検証報告書", 22))
        s.append(_stone(ST3_XS[2], sc("kok")) + _ctr(ST3_XS[2], 540.0, "有罪になった人は", 30, INK, 460) + _ctr(ST3_XS[2], 600.0, "いない", 34, INK, 300))
        s.append(_stag(ST3_XS[2], 790.0, "kok", "国会（2023年）", 22))
    return s


# ══════════════════════════════════════════════════════════
#  batteries（cb10）＝原因の3つの文の言い方を電池の目盛りで（升の数＝表 LV）：文1 推定される（3）・文2 考えられる（2）・文3 可能性が考えられる（1）
#  （R1 p.243・p.264）。c420（扉）・c502（階段）・c523（縦の目盛り）とは別の見た目
# ══════════════════════════════════════════════════════════
BT3 = ("推定される", "考えられる", "可能性が考えられる")
BT_YS = (430.0, 590.0, 750.0)


def _battery(y, lit):
    g = [F.rect(320.0, y - 46, 280.0, 92.0, J.BG2, INK, 5, rx=10), F.rect(600.0, y - 20, 20.0, 40.0, INK, None, None, rx=4)]
    for k in range(4):
        g.append(F.rect(334.0 + k * 66, y - 34, 56.0, 68.0, J.AMBER if k < lit else J.BG, J.AMBER if k < lit else J.LINE_DIM, 3, rx=6))
    return "".join(g)


def batteries_base(st0):
    return []


def batteries_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_chip(1440.0, 340.0, "強さまで読む", J.AMBER, 28))
        for i, y in enumerate(BT_YS):
            s.append(_tline(200.0, y + 10, f"文{i + 1}", 28, J.TICK, "start", 100) + _battery(y, 0))
    if _on(prev, st, "w"):
        for w, y in zip(BT3, BT_YS):
            s.append(_battery(y, LV[w]) + _tline(680.0, y + 12, w, 36, INK, "start", 560))
    if _on(prev, st, "diff"):
        s.append(F.poly([(1300.0, BT_YS[0] - 40), (1320.0, BT_YS[0] - 40), (1320.0, BT_YS[2] + 40), (1300.0, BT_YS[2] + 40)], "none", J.AMBER, 5))
        s.append(_tline(1350.0, 580.0, "違いで", 34, J.AMBER, "start", 300) + _tline(1350.0, 634.0, "話が変わる", 34, J.AMBER, "start", 360))
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
    # 🆕 ⑤b-6 第5章
    speed_step=_v("時の線と速さの段", ("y91", "step"), speed_step_base, speed_step_stage),
    push_out=_v("上から見た曲線と外への力", ("force", "sq", "grow"), push_out_base, push_out_stage, push_out_parts),
    hbars6=_v("6本の横の棒", ("bars", "cols"), hbars6_base, hbars6_stage),
    strip43=_v("表の最後の行の写し", ("co", "rep"), strip43_base, strip43_stage),
    cog2=_v("後ろから見た車体と重心", ("spring", "two"), cog2_base, cog2_stage),
    ramp=_v("斜めの速さの目盛り", ("band", "co"), ramp_base, ramp_stage),
    ceiling=_v("天井の線と上る矢印", ("up",), ceiling_base, ceiling_stage, ceiling_parts),
    sort2=_v("2つの箱への仕分け", ("no", "yes"), sort2_base, sort2_stage),
    cant=_v("後ろから見たレールの高さの差", ("tilt", "name"), cant_base, cant_stage, cant_parts),
    coupler=_v("上から見た1両目と2両目", ("c2", "pull"), coupler_base, coupler_stage),
    empty_slot=_v("上から見た線路の装置", ("q", "next"), empty_slot_base, empty_slot_stage),
    # 🆕 ⑤b-6 第6章
    dots_co=_v("会社の数の点", ("q", "n"), dots_co_base, dots_co_stage),
    donut=_v("内わけの輪", ("all", "way"), donut_base, donut_stage),
    order3=_v("3つの働きの順と言い方", ("r1", "r2", "r3"), order3_base, order3_stage),
    tl_plan=_v("計画の年表（横）", ("meet", "work", "use"), tl_plan_base, tl_plan_stage),
    spill=_v("年度の境の壁", ("plan", "staff", "poke"), spill_base, spill_stage),
    signal_date=_v("止まれの信号と使い始めの月", ("short", "move", "which"), signal_date_base, signal_date_stage),
    drop2=_v("縦の2つの日付", ("line", "date"), drop2_base, drop2_stage),
    kk_page=_v("会議録の頁の写し", ("date", "page", "june"), kk_page_base, kk_page_stage),
    receipt=_v("工事の費用の伝票", ("court", "cost"), receipt_base, receipt_stage),
    trim3=_v("切られて落ちる帯", ("q", "ext", "cut"), trim3_base, trim3_stage, trim3_parts),
    scale2=_v("2つの扱いの天びん", ("l", "r"), scale2_base, scale2_stage),
    jr_words=_v("冊子の2つの頁", ("a", "b"), jr_words_base, jr_words_stage),
    # 🆕 ⑤b-6 第7章
    tearoff=_v("日めくりと破った頁", ("q", "d1", "d2"), tearoff_base, tearoff_stage),
    stretch=_v("のびた3本の帯", ("a", "b"), stretch_base, stretch_stage),
    flow_fan=_v("横の流れと枝分かれ", ("ab", "fan"), flow_fan_base, flow_fan_stage),
    hourglass=_v("砂時計と数", ("has", "term", "done"), hourglass_base, hourglass_stage),
    book_seat=_v("決まりの本と責任者の席", ("rule", "seat"), book_seat_base, book_seat_stage),
    kengi3=_v("書類と3つの印", ("a", "bc"), kengi3_base, kengi3_stage),
    # 🆕 ⑤b-6 第8章
    plates4=_v("裁判所の印と4つの名札", ("q", "one", "three"), plates4_base, plates4_stage),
    duty=_v("歩みと義務の矢印", ("career", "duty"), duty_base, duty_stage),
    verdict=_v("判決の表紙の形", ("v",), verdict_base, verdict_stage),
    word_swap=_v("言い方の札の入れ替え", ("q", "swap", "end"), word_swap_base, word_swap_stage),
    bypass=_v("遮断と回り道", ("q", "stop", "detour"), bypass_base, bypass_stage),
    relay3=_v("3本の時期の帯", ("bars", "mark"), relay3_base, relay3_stage),
    scatter=_v("散らばった曲線の印", ("many", "one"), scatter_base, scatter_stage),
    stamps4=_v("4枚の書類と判", ("who", "done"), stamps4_base, stamps4_stage),
    podium=_v("演台と吹き出し", ("who", "say"), podium_base, podium_stage),
    stamps2=_v("2つの言い方の判", ("a", "no", "yes"), stamps2_base, stamps2_stage),
    bench=_v("被告人の席と外の2つ", ("seats", "co"), bench_base, bench_stage),
    nested=_v("答弁の中の答弁", ("word", "quote"), nested_base, nested_stage),
    wall=_v("2つの建物と壁", ("two", "leak"), wall_base, wall_stage),
    # 🆕 ⑤b-6 第9章
    role_lines=_v("日付の札と役職の線", ("a", "b", "c"), role_lines_base, role_lines_stage),
    ring12=_v("丸い机と席", ("team", "also"), ring12_base, ring12_stage),
    links6=_v("4つの箱と6本の線", ("all",), links6_base, links6_stage),
    tl_leak=_v("漏えいの年表（縦）", ("draft", "two", "copy"), tl_leak_base, tl_leak_stage),
    handover=_v("コピーの受け渡し", ("date", "move", "inside"), handover_base, handover_stage, handover_parts),
    bundle=_v("頁の束と日程の紙", ("who", "pages", "sched"), bundle_base, bundle_stage),
    jyanken=_v("字句と吹き出し", ("say", "told"), jyanken_base, jyanken_stage),
    meeting=_v("上から見た机と録音機", ("seat", "say"), meeting_base, meeting_stage),
    waveform=_v("録音の波形と線", ("words", "tone"), waveform_base, waveform_stage),
    open_book=_v("見開きの本", ("a", "b"), open_book_base, open_book_stage),
    five_slips=_v("5枚の紙と1枚", ("five", "pick"), five_slips_base, five_slips_stage),
    # 🆕 ⑤b-6 第10章
    answer=_v("留めた紙と判", ("q", "subj", "stamp"), answer_base, answer_stage),
    two_causes=_v("会社の印と曲線の印", ("co", "curve"), two_causes_base, two_causes_stage),
    stones3=_v("3つの飛び石", ("a", "b"), stones3_base, stones3_stage),
    batteries=_v("電池の目盛り", ("q", "w", "diff"), batteries_base, batteries_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
# 原文の値・欄・項目の写し（左上に「模式」を付けない）
NOT_SCHEMATIC = ("tt_col", "delay_bars", "ruler_v", "ring2", "tags4", "matrix", "hscale", "tt_band", "clockfan", "two_ribbons", "tiles",
                 "plaques", "split_box", "stairs4", "fan5", "band25", "cal18", "qcards",
                 # 🆕 ⑤b-6：値に比例・原文の写し
                 "hbars6", "strip43", "donut", "tl_plan", "kk_page", "jr_words", "stretch", "relay3", "tl_leak")
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
                band25=("rep",), two_ribbons=("rep",),
                # 🆕 ⑤b-6
                speed_step=("jr",), hbars6=("rep", "ct", "jr"), strip43=("rep", "jr"), cog2=("rep", "jr"), ramp=("ct", "jr"), sort2=("rep",),
                coupler=("rep",), dots_co=("ct",), donut=("jr",), tl_plan=("jr",), signal_date=("jr",), kk_page=("kok",), receipt=("ct",),
                scale2=("jr", "rep"), jr_words=("jr",), kengi3=("ken",), plates4=("ct", "jr"), duty=("jr",), verdict=("ct",), word_swap=("ct",),
                relay3=("jr",), scatter=("ct",), stamps4=("kok",), podium=("kok",), bench=("jr",), nested=("kok",), wall=("rep", "jr", "kv"),
                role_lines=("rep", "jr", "kv"), ring12=("kv",), links6=("rep", "jr", "kv"), tl_leak=("rep", "ken", "jr"), handover=("rep", "jr"),
                bundle=("jr",), jyanken=("rep", "jr", "kv"), meeting=("rep",), waveform=("kv",), open_book=("kv",), five_slips=("kv", "rep"),
                answer=("rep",), two_causes=("jr",), stones3=("rep", "kv", "kok", "jr"))
VIEW_WORDS = dict(doors3=DR3, stairs4=tuple(w for w, _m in ST4), persp=(PS_WORD,), two_cards=(TW2_WORD,), flow3=tuple(w for *_x, w, _y, _c in FL3),
                  fan5=(F5_WORD,), two_brakes=(BK_WORD,), band25=(B25_WORD,), weaker=WK_RUNGS + (WK_A, WK_B), objects=(OB_WORD,),
                  lens=(LN_WORD,), evidence=(EV_WORD,),
                  # 🆕 ⑤b-6
                  coupler=(CU_WORD,), order3=tuple(w for *_x, w in OR3_ROWS), five_slips=(FS_WORD,), answer=(AN_WORD,), two_causes=(TCZ_WORD,),
                  stones3=(ST3_WORD,), batteries=BT3)


def _geo6(view, allst):
    """🆕 ⑤b-6 の見え方の形（val＝記録と丸ごと比べる値・px と lins＝画素が値に比例するか＝p＝p0＋(v−v0)×k）。"""
    if view == "speed_step":
        return dict(val=(tuple(t for t, _d in SS_EV), SS_V), px=(_ss_ex(0), _ss_ex(1), _ss_ex(2), ss_y(SS_V[0]), ss_y(SS_V[1])),
                    lins=((SS["x0"], SS["k"], SS["t0"]),) * 3 + ((SS["yb"], -SS["kv"], SS["v0"]),) * 2)
    if view == "push_out":
        return dict(val=(PO_V, PO_F), px=(PO["long"],), lins=((0.0, PO["short"], 0.0),))
    if view == "hbars6":
        return dict(val=tuple((k, n, c, v, lab) for k, n, c, v, lab in HB6), px=tuple(hb_end(v) for *_x, v, _l in HB6),
                    lins=((HBX["x0"], HBX["k"], 0.0),) * len(HB6))
    if view == "strip43":
        return dict(val=T43)
    if view == "cog2":
        return dict(val=(CG_CO, CG["hi"] < CG["lo"]))
    if view == "ramp":
        k = (RP["bx"] - RP["ax"]) / (RP["v1"] - RP["v0"])
        return dict(val=(RP_BAND, RP_DOT, RP_CO), px=tuple(rp_pt(v)[0] for v in RP_BAND + (RP_DOT, RP_CO)), lins=((RP["ax"], k, RP["v0"]),) * 4)
    if view == "ceiling":
        tip = parts_of("ceiling", allst[-1])[0]["pts"][3][1]
        return dict(val=(CE_LIM, CE_MAX), px=(ce_y(CE_LIM), tip), lins=((CE["y0"], -CE["k"], CE["v0"]),) * 2)
    if view == "sort2":
        return dict(val=(SO_CARD,))
    if view == "cant":
        return dict(val=(CA_MM,))
    if view == "coupler":
        return dict(val=(CU_V, CU_WORD))
    if view == "dots_co":
        return dict(val=(DC_TOTAL, len(DC_LIT), DC_JR, len(set(DC_LIT)) == len(DC_LIT) and max(DC_LIT) < DC_TOTAL))
    if view == "donut":
        cum, a = [], 0
        for _t, n, _c in DN:
            a += n
            cum.append(a)
        return dict(val=tuple((t, n) for t, n, _c in DN) + (DN_TOTAL,), px=tuple(b for _a, b in dn_angs()),
                    lins=((-90.0, 360.0 / DN_TOTAL, 0.0),) * len(DN))
    if view == "order3":
        return dict(val=(OR3, OR3_ROWS))
    if view == "tl_plan":
        ds = (TP_MEET, TP_WORK[0], TP_WORK[1], TP_USE, TP_ACC)
        return dict(val=ds, px=tuple(tp_x(*d) for d in ds), lins=((TP["x0"] - TP["m0"] * TP["k"], 12 * TP["k"], 2003.0),) * len(ds))
    if view == "spill":
        return dict(val=(SPL_ACC, SPL_POKE), px=(spl_x(*SPL_ACC),), lins=((SPL["wall"], 12 * SPL["k"], _ym(2005, 4)),))
    if view == "signal_date":
        return dict(val=(SD_FROM, SD_TO, SD_TOLD))
    if view == "drop2":
        return dict(val=(DR2_A, DR2_B, DR2_GAP))
    if view == "kk_page":
        return dict(val=(KP_DAY,))
    if view == "receipt":
        return dict(val=RC_ROWS)
    if view == "trim3":
        xs = tr_edges()
        return dict(val=(TR_CUT, TR_ADD, TR_SUM, sum(s for _d, s in TR_CUT)), px=tuple(b - a for a, b in zip(xs, xs[1:])),
                    lins=((0.0, TR["k"], 0.0),) * len(TR_CUT))
    if view == "jr_words":
        return dict(val=JW)
    if view == "tearoff":
        return dict(val=TO_DAYS)
    if view == "stretch":
        return dict(val=(SR_T, SR_LAB, SR_HEAD), px=tuple(sr_x(t) for t in SR_T), lins=((SR["x0"], SR["k"], SR["t0"]),) * len(SR_T))
    if view == "flow_fan":
        return dict(val=FF_DAYS)
    if view == "hourglass":
        return dict(val=(HG_YEARS, HG_CO, HG_N, HG_BY))
    if view == "book_seat":
        return dict(val=(BS_YEAR,))
    if view == "kengi3":
        return dict(val=KG3)
    if view == "plates4":
        return dict(val=(PL4, PL4_N))
    if view == "verdict":
        return dict(val=(VD_DAY, VD_ASK))
    if view == "relay3":
        return dict(val=RL_T, px=tuple(rl_span(i)[0] for i in range(len(RL_T))), lins=((RL["x0"], RL["k"], RL["y0"]),) * len(RL_T))
    if view == "scatter":
        return dict(val=("2000か所以上", len(sct_pts()) < 2000))
    if view == "stamps4":
        return dict(val=SP4)
    if view == "podium":
        return dict(val=(PD_DAY,))
    if view == "bench":
        return dict(val=(BN_SEATS,))
    if view == "nested":
        return dict(val=(NS_DAY,))
    if view == "role_lines":
        return dict(val=(RLN_DAY,))
    if view == "ring12":
        return dict(val=(RG12_N, RG12_DAY))
    if view == "links6":
        return dict(val=(len(LK_YS), len(LK_TO)))
    if view == "tl_leak":
        ds = tuple(d for _t, d, _c in TLK_EV) + (TLK_LEAK,)
        return dict(val=(TLK_EV, TLK_LEAK), px=tuple(tlk_y(*d) for d in ds), lins=((TLK["y0"], 12 * TLK["k"], _ym(2005, 4)),) * len(ds))
    if view == "handover":
        return dict(val=(HO_DAY, HO_PUB))
    if view == "bundle":
        return dict(val=(BU_DAY,))
    if view == "meeting":
        return dict(val=(MT_DAY,))
    if view == "five_slips":
        return dict(val=(FS_N, FS_WORD))
    if view == "answer":
        return dict(subj=AN_SUBJ, word=AN_WORD)
    if view == "two_causes":
        return dict(val=(TCZ_WORD,))
    if view == "stones3":
        return dict(val=(ST3_WORD,))
    if view == "batteries":
        return dict(val=BT3)
    return {}


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
    else:
        out.update(_geo6(view, allst))
    return out
