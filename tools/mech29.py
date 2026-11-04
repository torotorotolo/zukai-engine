# -*- coding: utf-8 -*-
"""mech29.py — 29本目（GMO不正アクセス問題・2026-10-20 に異変を確認・GMOインターネットへの不正アクセス）「図解」（2026-11-04 新設・⑤b-4＝図38カット）。

■ 何か
  28本目 `mech28` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品は使わない」。再現イラストではない＝「再現」の札は出さない。
  🔴 **地は写真**（`cuts.ss.gr`＝CC BY・CC0・PD を暗くするだけ・方眼と章の色なし・静止）＝字はどれも暗い縁取り（OL）・札の地は半ば透ける紺（`_panel`）。
     字と図の線の周りの地は門番 check_ground が 8:1 で測る。
  左上に見え方の名（模式の見え方は末尾に「・模式」）・左下に注（模式の見え方は「模式」）と出典。
  🔴 会社の事件の決まり（ルール §B2-11・§B2-11b）：顧客・公開された人・SNS の投稿者・役員・記者の名前は描かない（役職だけ）・攻撃した者は「第三者」「攻撃した者」・
     会社を犯人と言わない・公開された情報は一切出さない・特定の国や集団を書かない。**人は描かない**。手口の推測の絵は描かない（説明会で会社が言った順番だけ）。
     「犯人」の字は SNS の原文の札と会社の言葉の引用（c703）だけ。
  🔴 **色は「誰か・何か」**（役の色＝SRC・新しい色の値は足していない）：会社＝青 uscg／攻撃した者＝橙 company／警察＝紫 tsb／利用者＝桃 bldg_a／記者＝水色 ship／
     セキュリティの会社＝緑 ntsb／SNS の声＝白い札。同じ色の鍵は同じ画面に出さない（門番 judge_m29 が VIEW_SRC で見る）。意味の色＝赤 ALERT（侵入・止まった）・黄 AMBER（数・日付）。
  🔴 画面の数は全部 `rel=` に同じ文字列で宣言する（門番が基図と段の層の全部の字から数を拾って照らす）。
  🔴 記録の値（色・数・比例・会社の言葉・SNS の原文）は門番の側 REC_M29 が別に持つ（§5b-88）。描く側の表を書き換えると鳴る。

■ 見え方（view）＝映像方針の一覧 `ref/ep29/eizou_list29.md` の「種類」（図38）
  つかみ  gap76（c105 帯）
  第1章  vps（c202 模式）・cal3（c205 暦）・num26739（c208 札）・two_reports（c218 比べ）
  第2章  ransom（c305 模式）・clock_noon（c306 時計）・sns307（c307）・bounty（c315 札）・tips（c319 棒）
  第3章  order4（c402 年表）・in1〜in4（c403〜c406 模式）・gap2（c407 帯）・qa_why（c409 問答）・drive（c412 模式）・two_says（c415 比べ）・know（c417 並べ）・qa_route（c419 問答）
  第4章  hist（c502 年表）・cal24（c503 暦）・deep_fast（c505 言葉）・sort5（c507 箱）・report_flow（c511 流れ）・two_ans（c513 並べ）・resil（c519 模式）
  第5章  scope（c603 箱）・sns618（c618）・sum3（c606 式）・paycut（c609 割合）・ai_say（c615 言葉）・sns616（c616）・sns617（c617）・sns619（c619）
  第6章  contact（c701 窓口）・tipline（c703 窓口）
  🔴 同じ型でも絵を分ける：c105（1本の帯）↔c407（2本の帯）・c205（3枚の暦）↔c503（1カ月の暦）・c402（2カ月の線）↔c502（3年の線）・c409（上下の問答）↔c419（左右の問答）・
     c417（左右の枠）↔c513（上下の枠）・c507（入れ子の箱）↔c603（左右の枠）・c505（1枚の言葉）↔c615（問い・言葉・3つの札）・c701（電話）↔c703（サイトとメール）。

■ SPEC の書き方（mech28 と同じ）
  `**ss.gr("cm004"), fig=("m29", dict(view=…, steps=[dict(state=dict(…)), …], rel=[dict(t="76日", src="計算")], note="…", src="…"))`
  原文どおりの字を読む行は `mute=[行の番号]`（字幕を消す＝scene_jiko.SUB_MUTE・門番 echo の例外は `quote_lines`）。
"""
from __future__ import annotations

import calendar as _cal
import datetime as _dt

import jiko_style as J
import titan_fig as F
from mech21 import _arrow, _on
from mech24 import rc
from mech27 import CARD, CARD_INK, CARD_SUB, CX, INK, OL, ONOFF, _panel, _phone, _sns_note, _t, _tag, svg_texts
from mech28 import _clock, _lines, _quote_card, ck_angles

# 誰か・何か（名・ROLE か J の名）。同じ色の鍵は同じ画面に出さない（門番が VIEW_SRC で見る）
SRC = dict(
    company=("会社", "uscg"),
    attacker=("攻撃した者", "company"),
    police=("警察", "tsb"),
    user=("利用者", "bldg_a"),
    press=("記者", "ship"),
    sec=("セキュリティの会社", "ntsb"),
    sns=("SNS の声", "SUB"),
)


def sc(key):
    return rc(SRC[key][1])


def _d(y, m, d):
    return _dt.date(y, m, d)


# ══════════════════════════════════════════════════════════
#  部品（人は描かない＝線と四角だけ・特定の製品の画面は描かない）
# ══════════════════════════════════════════════════════════
def _pc(cx, cy, s, col):
    """手元のパソコン（画面と台）。"""
    w, h = 220 * s, 140 * s
    return (F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 6, rx=10)
            + F.rect(cx - w / 2 + 14 * s, cy - h / 2 + 14 * s, w - 28 * s, h - 28 * s, "none", col, 3, rx=4)
            + F.line(cx, cy + h / 2, cx, cy + h / 2 + 28 * s, col, 7)
            + F.line(cx - 56 * s, cy + h / 2 + 30 * s, cx + 56 * s, cy + h / 2 + 30 * s, col, 7))


def _server(cx, cy, s, col):
    """サーバー（棚と灯り）。"""
    w, h = 170 * s, 190 * s
    g = F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 6, rx=10)
    for i in range(3):
        y = cy - h / 2 + (32 + 58 * i) * s
        g += F.line(cx - w / 2 + 16 * s, y, cx + w / 2 - 44 * s, y, col, 6)
        g += F.circ(cx + w / 2 - 26 * s, y, 7 * s, col)
    return g


def _key(cx, cy, s, col):
    """鍵（アカウントの印）。"""
    r = 42 * s
    return (F.circ(cx - 66 * s, cy, r, J.BG2, col, 7)
            + F.line(cx - 66 * s + r, cy, cx + 86 * s, cy, col, 9)
            + F.line(cx + 40 * s, cy, cx + 40 * s, cy + 32 * s, col, 9)
            + F.line(cx + 76 * s, cy, cx + 76 * s, cy + 32 * s, col, 9))


def _lock(cx, cy, s, col):
    """錠前（データを使えなくした印）。"""
    w, h = 110 * s, 84 * s
    return (F.poly([(cx - 34 * s, cy - h / 2), (cx - 34 * s, cy - h / 2 - 34 * s), (cx - 20 * s, cy - h / 2 - 52 * s), (cx + 20 * s, cy - h / 2 - 52 * s),
                    (cx + 34 * s, cy - h / 2 - 34 * s), (cx + 34 * s, cy - h / 2)], "none", col, 9)
            + F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 7, rx=10)
            + F.circ(cx, cy - 6 * s, 10 * s, col) + F.line(cx, cy - 6 * s, cx, cy + 22 * s, col, 7))


def _docs(cx, cy, s, col):
    """データの束（重なった紙）。"""
    w, h = 200 * s, 150 * s
    g = ""
    for k in (2, 1, 0):
        x, y = cx - w / 2 + k * 20 * s, cy - h / 2 - k * 20 * s
        g += F.rect(x, y, w, h, J.BG2, col, 5, rx=10)
    for i in range(3):
        y = cy - h / 2 + (40 + 34 * i) * s
        g += F.line(cx - w / 2 + 24 * s, y, cx + w / 2 - 24 * s, y, col, 5)
    return g


def _folder(cx, cy, s, col):
    """手元のフォルダ。"""
    w, h = 130 * s, 86 * s
    return (F.poly([(cx - w / 2, cy - h / 2), (cx - w / 2 + 44 * s, cy - h / 2), (cx - w / 2 + 58 * s, cy - h / 2 + 16 * s), (cx + w / 2, cy - h / 2 + 16 * s),
                    (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], J.BG2, col, 5, close=True))


def _switch_on(cx, cy, s, col):
    """切り替えの印（オン）。"""
    w, h = 110 * s, 54 * s
    return F.rect(cx - w / 2, cy - h / 2, w, h, col, None, None, rx=h / 2) + F.circ(cx + w / 2 - h / 2, cy, h / 2 - 7 * s, INK)


def _no_tag(cx, cy, t, w):
    """「〜ではない」の札（赤い × つき）。"""
    x0 = cx - w / 2 + 44
    return (_tag(cx, cy, t, J.ALERT, 38, INK, w=w, h=84)
            + F.line(x0 - 14, cy - 14, x0 + 14, cy + 14, J.ALERT, 7) + F.line(x0 - 14, cy + 14, x0 + 14, cy - 14, J.ALERT, 7))


# ══════════════════════════════════════════════════════════
#  つかみ  gap76（c105）＝帯：8月5日 → 10月20日（76日・位置は日に比例）。🔴 芯の引き
# ══════════════════════════════════════════════════════════
GP = dict(x0=170.0, x1=1750.0, y=470.0, h=124.0, d0=_d(2026, 8, 5), d1=_d(2026, 10, 20))
GP_M = ((_d(2026, 9, 1), "9月"), (_d(2026, 10, 1), "10月"))


def gp_x(d):
    return GP["x0"] + (d - GP["d0"]).days * (GP["x1"] - GP["x0"]) / (GP["d1"] - GP["d0"]).days


def gp_days():
    return (GP["d1"] - GP["d0"]).days


def gap76_base(st0):
    return []


def gap76_stage(prev, st):
    s = []
    x0, x1, y, h = GP["x0"], GP["x1"], GP["y"], GP["h"]
    if _on(prev, st, "band"):
        s.append(F.rect(x0, y - h / 2, x1 - x0, h, J.ALERT, None, None, rx=10))
        for d, t in GP_M:
            s.append(F.line(gp_x(d), y - h / 2 - 16, gp_x(d), y - h / 2 + 2, J.LINE, 4))
            s.append(_t(gp_x(d), y - h / 2 - 28, t, 28, J.TICK, "middle", 140))
        s.append(_t(x0, y - h / 2 - 96, "8月5日", 54, J.AMBER, "start", 400))
        s.append(_t(x0, y - h / 2 - 40, "最初の侵入", 34, INK, "start", 420))
        s.append(_t(x1, y - h / 2 - 96, "10月20日", 54, J.AMBER, "end", 400))
        s.append(_t(x1, y - h / 2 - 40, "会社が確かめた", 34, INK, "end", 420))
        s.append(_t(CX, y + 36, f"{gp_days()}日", 100, INK, "middle", 420))
        s.append(_t(CX, y + h / 2 + 76, "およそ2カ月半", 56, J.AMBER, "middle", 700))
    if _on(prev, st, "blind"):
        s.append(_tag(560.0, y + h / 2 + 190, "そのあいだ、気づけず", J.ALERT, 40, INK))
    if _on(prev, st, "ask"):
        s.append(_arrow(1470.0, y + h / 2 + 150, 1660.0, y + h / 2 + 8, sc("user"), 7, 26))
        s.append(_tag(1360.0, y + h / 2 + 190, "きっかけは問い合わせ", sc("user"), 40, INK))
    return s


# ══════════════════════════════════════════════════════════
#  第1章  vps（c202）＝手元のパソコン → ネットの向こうの1台。特定の製品の画面は描かない
# ══════════════════════════════════════════════════════════
def vps_base(st0):
    return []


def vps_stage(prev, st):
    s = []
    if _on(prev, st, "vps"):
        s.append(_panel(1150.0, 290.0, 620.0, 520.0, sc("company"), sw=4, dash="14 10"))
        s.append(_t(1460.0, 346.0, "ネットの向こう", 36, sc("company"), "middle", 560))
        s.append(_server(1460.0, 530.0, 1.15, sc("company")))
        s.append(_tag(1460.0, 730.0, "VPS（1台ぶんを借りる）", sc("company"), 36, INK))
    if _on(prev, st, "rd"):
        s.append(_pc(380.0, 500.0, 1.5, sc("user")))
        s.append(_t(380.0, 700.0, "手元のパソコン", 40, sc("user"), "middle", 480))
        s.append(_arrow(600.0, 520.0, 1130.0, 520.0, J.AMBER, 9, 34))
        s.append(_t(865.0, 470.0, "リモートデスクトップ", 44, J.AMBER, "middle", 510))
        s.append(_t(865.0, 590.0, "画面だけが手元に来る", 32, INK, "middle", 510))
    return s


# ══════════════════════════════════════════════════════════
#  cal3（c205）＝暦3枚（10月19日・20日・21日）。曜日は日付の式。第3報の経緯の順
# ══════════════════════════════════════════════════════════
C3 = dict(xs=(350.0, 960.0, 1570.0), y=540.0, w=540.0, h=520.0)
C3_V = ((_d(2026, 10, 19), ("問い合わせを受ける", "調査の開始")),
        (_d(2026, 10, 20), ("不正なプログラムを", "確認")),
        (_d(2026, 10, 21), ("午前4時", "全プランを順に停止", "第1報")))
_WD = "月火水木金土日"


def _cal_page(i):
    x, y, w, h = C3["xs"][i], C3["y"], C3["w"], C3["h"]
    d, lines = C3_V[i]
    top = y - h / 2
    g = (_panel(x - w / 2, top, w, h, sc("company"), sw=5)
         + F.line(x - w / 2, top + 76, x + w / 2, top + 76, sc("company"), 4)
         + _t(x, top + 54, f"{d.month}月", 38, sc("company"), "middle", w - 40)
         + _t(x, top + 186, str(d.day), 100, J.AMBER, "middle", w - 40)
         + _t(x, top + 242, f"{_WD[d.weekday()]}曜日", 32, J.TICK, "middle", w - 40))
    return g + _lines(x, top + 322, lines, 38, INK, "middle", w - 40, 58.0)


def cal3_base(st0):
    return []


def cal3_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_cal_page(0))
    if _on(prev, st, "b"):
        s += [_arrow(C3["xs"][0] + C3["w"] / 2 + 4, C3["y"], C3["xs"][1] - C3["w"] / 2 - 4, C3["y"], J.LINE, 7, 22), _cal_page(1),
              _arrow(C3["xs"][1] + C3["w"] / 2 + 4, C3["y"], C3["xs"][2] - C3["w"] / 2 - 4, C3["y"], J.LINE, 7, 22), _cal_page(2)]
    return s


# ══════════════════════════════════════════════════════════
#  num26739（c208）＝札：26,739件は「対象となり得る」数（語りと図が同じ字＝字幕を重ねない）
# ══════════════════════════════════════════════════════════
N2_V = "26,739件"
N2_A = "対象となり得るサーバー数"
N2_B = "「不正アクセスまたは情報取得が確認された件数ではありません」"


def num26739_base(st0):
    return []


def num26739_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_panel(320.0, 290.0, 1280.0, 280.0, sc("company"), sw=5))
        s.append(_t(CX, 420.0, N2_V, 120, J.AMBER, "middle", 1200))
        s.append(_t(CX, 520.0, N2_A, 52, INK, "middle", 1200))
    if _on(prev, st, "b"):
        s.append(_quote_card(CX, 690.0, 1680.0, 170.0, (N2_B,), sc("company"), 46, None, "第3報（2026年10月23日）"))
    return s


# ══════════════════════════════════════════════════════════
#  two_reports（c218）＝比べ：第1報 ↔ 第4報（3日で書くことが変わった）。字は頁のまま・第1報は途中を「…」で縮めた
# ══════════════════════════════════════════════════════════
TR_A = ("「個人情報の漏えいや、", "…悪用された事実は", "確認されておりません」")
TR_B = ("「外部に持ち出された", "事実を確認」")


def _tr_card(x, head, lines, col):
    # 2行の札は字を大きく（枠の中が空かない＝門番 box）
    three = len(lines) == 3
    return (_panel(x, 300.0, 700.0, 440.0, col, sw=6) + _t(x + 350, 372.0, head, 42, col, "middle", 640)
            + _lines(x + 350, 462.0 if three else 500.0, lines, 48 if three else 62, INK, "middle", 640, 72.0 if three else 92.0))


def two_reports_base(st0):
    return []


def two_reports_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_tr_card(130.0, "第1報〈10月21日〉", TR_A, sc("company")))
    if _on(prev, st, "b"):
        s.append(_arrow(850.0, 520.0, 1070.0, 520.0, J.AMBER, 10, 36))
        s.append(_t(960.0, 480.0, "3日", 60, J.AMBER, "middle", 200))
        s.append(_tr_card(1090.0, "第4報〈10月24日〉", TR_B, J.ALERT))
    return s


# ══════════════════════════════════════════════════════════
#  第2章  ransom（c305）＝データの束に鍵 → 金を求める札。特定の製品や別の事件の絵は使わない
# ══════════════════════════════════════════════════════════
def ransom_base(st0):
    return []


def ransom_stage(prev, st):
    s = []
    if _on(prev, st, "lock"):
        s.append(_docs(520.0, 520.0, 1.7, J.LINE))
        s.append(_lock(520.0, 510.0, 1.25, J.ALERT))
        s.append(_t(520.0, 760.0, "データが使えない", 44, J.ALERT, "middle", 640))
    if _on(prev, st, "ask"):
        s.append(_arrow(860.0, 500.0, 1080.0, 500.0, sc("attacker"), 9, 34))
        s.append(_panel(1100.0, 340.0, 660.0, 320.0, sc("attacker"), sw=6))
        s.append(_t(1430.0, 470.0, "戻してほしければ", 50, INK, "middle", 600))
        s.append(_t(1430.0, 570.0, "金を", 70, sc("attacker"), "middle", 600))
    return s


# ══════════════════════════════════════════════════════════
#  clock_noon（c306）＝時計2つ：10月27日 9:58 第8報 → 12:00 予告の時刻（針は時刻の式）・図は12:00まで
# ══════════════════════════════════════════════════════════
CN = dict(a=(470.0, 362.0), b=(1450.0, 362.0), r=108.0)      # y＝時刻の字を地 CM027 の焼き込みの字の上に載せない（門番 slide G-14）
CN_T = (("10月27日", 9, 58), ("10月27日", 12, 0))
CN_W = ("バックアップ", "ネットワーク", "電源", "コード")


def _cn_labels(x, y, r, day, h, m, what, col):
    return (_t(x, y + r + 46, day, 34, INK, "middle", 420)
            + _t(x, y + r + 112, f"{h}:{m:02d}", 66, J.AMBER, "middle", 420)
            + _t(x, y + r + 166, what, 36, col, "middle", 520))


def clock_noon_base(st0):
    return []


def clock_noon_stage(prev, st):
    s = []
    (xa, ya), (xb, yb), r = CN["a"], CN["b"], CN["r"]
    if _on(prev, st, "both"):
        d, h, m = CN_T[0]
        s += [_clock(xa, ya, r, h, m, sc("company")), _cn_labels(xa, ya, r, d, h, m, "第8報", sc("company"))]
        d, h, m = CN_T[1]
        s += [_arrow(xa + r + 30, ya, xb - r - 30, yb, J.AMBER, 8, 30), _clock(xb, yb, r, h, m, sc("attacker")),
              _cn_labels(xb, yb, r, d, h, m, "予告の時刻", sc("attacker"))]
    if _on(prev, st, "ask"):
        for i, t in enumerate(CN_W):
            s.append(_tag(330.0 + i * 420.0, 780.0, t, sc("company"), 38, INK, w=360.0, h=72))
    return s


# ══════════════════════════════════════════════════════════
#  SNS の声（c307・c618・c616・c617・c619）＝原文どおりの字をこちらの札に組み直す（アイコン・X の画面の作り・アカウント名は出さない）
# ══════════════════════════════════════════════════════════
#   🔴 札の字は原文どおり（門番の側 REC_M29 の sns に原文）・注釈は同じ置き場（cuts.ss.SNS_NOTE・SNS_NOTE_BOX＝門番 check_ground）
#   🔴 字は検索の控え（`ref/ep29/src/sns/`＝git の外）と一覧の字に合わせた＝x.com の頁は開かない。c307・c616・c618 の札は 11-03 にカズヤくんが確かめた・c617・c619 は札なしを ② で確かめた
#      c617＝前に文が続く＝頭に「…」／c619＝前に文が続く＝頭に「…」・2文は投稿の中で続いている／c616＝2文は投稿の中で続いている
SNS_CARDS = dict(
    k307=(("GMOの正午になる前にPCの電源切ってとかいう呼びかけ今知った。", "こんなん気づかなかった人が殆どなのでは……。"), "X の投稿（2026年10月27日）"),
    k618=(("9月末で解約した人間だけど、", "GMOから今日まで1度もメールで案内ないんだけど。"), "X の投稿（2026年11月3日）"),
    k616=(("AIと事件の問題の本質は直接的に関係ないような。", "AIの脅威に問題点をすり替えているように聞こえた。"), "X の投稿（2026年11月3日）"),
    k617=(("…今年の8月に侵入されていたのに", "10月まで気づかなかった理由だ。"), "X の投稿（2026年11月2日）"),
    k619=(("…侵入に2カ月半気づけなかった会社の責任も重い。", "それでも、叩く順番はまず犯人じゃない？"), "X の投稿（2026年11月3日）"),
)


def _sns_h(key, cap):
    return 40 + cap * 1.55 * len(SNS_CARDS[key][0]) + 56


def _sns_frame(cx, cy, w, key, cap):
    """札の地と出どころの行（字は別に出す＝行ごとに出せる）。"""
    src = SNS_CARDS[key][1]
    h = _sns_h(key, cap)
    return F.rect(cx - w / 2, cy - h / 2, w, h, CARD, None, None, rx=22) + F.txtfit(cx - w / 2 + 48, cy + h / 2 - 22, src, w - 96, cap=26, col=CARD_SUB)


def _sns_line(cx, cy, w, key, i, cap):
    h = _sns_h(key, cap)
    return F.txtfit(cx - w / 2 + 48, cy - h / 2 + 28 + cap + i * cap * 1.55, SNS_CARDS[key][0][i], w - 96, cap=cap, col=CARD_INK)


def sns_base(st0):
    return [_sns_note()]


def sns307_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s += [_sns_frame(CX, 500.0, 1640.0, "k307", 48), _sns_line(CX, 500.0, 1640.0, "k307", 0, 48)]
    if _on(prev, st, "b"):
        s.append(_sns_line(CX, 500.0, 1640.0, "k307", 1, 48))
    return s


def sns618_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s += [_sns_frame(CX, 440.0, 1500.0, "k618", 50), _sns_line(CX, 440.0, 1500.0, "k618", 0, 50), _sns_line(CX, 440.0, 1500.0, "k618", 1, 50)]
    if _on(prev, st, "b"):
        s.append(_tag(CX, 640.0, "個人の申告", J.AMBER, 44, INK))
        s.append(_t(CX, 744.0, "解約した人の扱い＝発表に見当たらず（11月3日の時点）", 38, INK, "middle", 1500))
    return s


def sns616_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s += [_sns_frame(CX, 490.0, 1500.0, "k616", 46), _sns_line(CX, 490.0, 1500.0, "k616", 0, 46)]
    if _on(prev, st, "b"):
        s.append(_sns_line(CX, 490.0, 1500.0, "k616", 1, 46))
    return s


def sns617_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s += [_sns_frame(CX, 500.0, 1280.0, "k617", 58), _sns_line(CX, 500.0, 1280.0, "k617", 0, 58), _sns_line(CX, 500.0, 1280.0, "k617", 1, 58)]
    return s


def sns619_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s += [_sns_frame(CX, 500.0, 1500.0, "k619", 50), _sns_line(CX, 500.0, 1500.0, "k619", 0, 50)]
    if _on(prev, st, "b"):
        s.append(_sns_line(CX, 500.0, 1500.0, "k619", 1, 50))
    return s


# ══════════════════════════════════════════════════════════
#  bounty（c315）＝札：懸賞金＝総額の上限 100万米ドル・10月28日 12:00 から受付（第12報）・身代金でも買い取りでもない。専用サイトの画面は出さない
# ══════════════════════════════════════════════════════════
BT_V = ("100万米ドル", "10月28日 12:00 から受付")


def bounty_base(st0):
    return []


def bounty_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_panel(360.0, 280.0, 1200.0, 340.0, sc("company"), sw=6))
        s.append(_t(CX, 346.0, "懸賞金：総額の上限", 40, sc("company"), "middle", 1100))
        s.append(_t(CX, 470.0, BT_V[0], 110, J.AMBER, "middle", 1100))
        s.append(_t(CX, 566.0, BT_V[1], 40, INK, "middle", 1100))
    if _on(prev, st, "b"):
        s.append(_no_tag(560.0, 720.0, "身代金", 620.0))
        s.append(_no_tag(1360.0, 720.0, "情報の買い取り", 620.0))
        s.append(_t(CX, 826.0, "要求の額とは別", 36, INK, "middle", 900))
    return s


# ══════════════════════════════════════════════════════════
#  tips（c319）＝棒：懸賞金への情報提供の累計（高さは数に比例・0から・🔴 日付の間隔どおりに置く＝10月31日と11月1日は空き）。語るのは 735 の1本だけ
# ══════════════════════════════════════════════════════════
TP = dict(x0=470.0, dx=216.0, y0=770.0, k=0.46, w=150.0, d0=_d(2026, 10, 28))
TP_V = ((_d(2026, 10, 28), 113, "10月28日"), (_d(2026, 10, 29), 321, "29日"), (_d(2026, 10, 30), 428, "30日"), (_d(2026, 11, 2), 735, "11月2日"))


def tp_x(d):
    return TP["x0"] + (d - TP["d0"]).days * TP["dx"]


def tp_y(v):
    return TP["y0"] - v * TP["k"]


def tips_base(st0):
    return []


def tips_stage(prev, st):
    s = []
    y0 = TP["y0"]
    if _on(prev, st, "police"):
        s.append(_tag(530.0, 310.0, "捜査本部 約70人（報道・10月29日）", sc("police"), 34, INK))
    if _on(prev, st, "bars"):
        s.append(F.line(320.0, y0, 1680.0, y0, J.LINE, 5))
        for d, v, lab in TP_V:
            x = tp_x(d)
            last = v == TP_V[-1][1]
            s.append(F.rect(x - TP["w"] / 2, tp_y(v), TP["w"], y0 - tp_y(v), J.AMBER if last else J.LINE_DIM, None, None, rx=6))
            s.append(_t(x, tp_y(v) - 16, f"{v}件" if last else str(v), 64 if last else 36, J.AMBER if last else J.TICK, "middle", 300))
            s.append(_t(x, y0 + 46, lab, 34, INK if last else J.TICK, "middle", 210))
        s.append(_t(tp_x(_d(2026, 10, 31)) + TP["dx"] / 2, y0 + 46, "土日は更新なし", 28, J.TICK, "middle", 400))
    if _on(prev, st, "none"):
        s.append(_tag(1300.0, 310.0, "さらなる公開の報道は見つからず（11月3日の時点）", J.AMBER, 32, INK))
    return s


# ══════════════════════════════════════════════════════════
#  第3章  order4（c402）＝年表：会社が示した順番の4点だけ（位置は日に比例）・説明会の説明をもとにこちらで組んだ
# ══════════════════════════════════════════════════════════
O4 = dict(x0=210.0, x1=1710.0, y=540.0, d0=_d(2026, 8, 5), d1=_d(2026, 10, 20))
O4_D = (_d(2026, 8, 5), _d(2026, 8, 17), _d(2026, 9, 20), _d(2026, 10, 14), _d(2026, 10, 20))


def o4_x(d):
    return O4["x0"] + (d - O4["d0"]).days * (O4["x1"] - O4["x0"]) / (O4["d1"] - O4["d0"]).days


def order4_base(st0):
    y = O4["y"]
    g = [F.line(O4["x0"], y, O4["x1"], y, J.LINE, 6)]
    for d in (O4_D[0], O4_D[1], O4_D[4]):
        g.append(F.circ(o4_x(d), y, 15, J.AMBER))
    g.append(F.rect(o4_x(O4_D[2]), y - 11, o4_x(O4_D[3]) - o4_x(O4_D[2]), 22, J.AMBER, None, None, rx=8))
    return g


def order4_stage(prev, st):
    s = []
    y = O4["y"]
    if _on(prev, st, "lab"):
        s.append(_t(o4_x(O4_D[0]), y - 90, "8月5日", 48, J.AMBER, "start", 420))
        s.append(_t(o4_x(O4_D[0]), y - 38, "最初の侵入", 34, INK, "start", 420))
        s.append(_t(o4_x(O4_D[1]), y + 72, "8月17日", 48, J.AMBER, "start", 420))
        s.append(_t(o4_x(O4_D[1]), y + 124, "管理サーバーへ", 34, INK, "start", 420))
        xm = (o4_x(O4_D[2]) + o4_x(O4_D[3])) / 2
        s.append(_t(o4_x(O4_D[2]), y - 90, "9月20日", 44, J.AMBER, "middle", 300))
        s.append(_t(o4_x(O4_D[3]), y - 90, "10月14日", 44, J.AMBER, "middle", 300))
        s.append(_t(xm, y - 38, "マルウェアを配る", 34, INK, "middle", 640))
        s.append(_t(o4_x(O4_D[4]), y + 72, "10月20日", 48, J.AMBER, "end", 420))
        s.append(_t(o4_x(O4_D[4]), y + 124, "会社が確かめた", 34, INK, "end", 420))
        s.append(_tag(CX, 340.0, "説明会の説明をもとにこちらで組んだ", J.LINE, 34, INK))
    return s


# ══════════════════════════════════════════════════════════
#  in1〜in4（c403〜c406）＝模式の4枚（同じ暗い地 T229・絵は別）。手口の絵は描かない＝会社の言葉の順番だけ
# ══════════════════════════════════════════════════════════
def in1_base(st0):
    return []


def in1_stage(prev, st):
    s = []
    if _on(prev, st, "who"):
        s.append(_tag(CX, 320.0, "8月5日", J.AMBER, 52, J.AMBER))
        s.append(_tag(330.0, 540.0, "攻撃した者", sc("attacker"), 48, INK, w=400.0, h=120))
        s.append(_panel(960.0, 370.0, 760.0, 440.0, sc("user"), sw=5, dash="14 10"))
        s.append(_t(1340.0, 428.0, "「お客様環境」", 44, sc("user"), "middle", 700))
        s.append(_server(1340.0, 575.0, 0.96, sc("user")))
        s.append(_tag(1340.0, 745.0, "VPS〈利用者が借りる1台〉", sc("user"), 34, INK))
    if _on(prev, st, "in"):
        s.append(_arrow(540.0, 540.0, 1200.0, 560.0, J.ALERT, 11, 40))
        s.append(_t(800.0, 500.0, "入った", 50, J.ALERT, "middle", 300))
    return s


def in2_base(st0):
    return []


def in2_stage(prev, st):
    s = []
    if _on(prev, st, "key"):
        s.append(_server(330.0, 530.0, 1.05, sc("user")))
        s.append(_t(330.0, 696.0, "VPS", 42, sc("user"), "middle", 300))
        s.append(_panel(620.0, 340.0, 680.0, 370.0, J.ALERT, sw=6))
        s.append(_key(960.0, 470.0, 1.4, J.AMBER))
        s.append(_t(960.0, 625.0, "管理者のアカウント", 54, INK, "middle", 620))
        s.append(_arrow(1320.0, 525.0, 1500.0, 525.0, J.ALERT, 10, 36))
        s.append(_t(1410.0, 482.0, "盗まれた", 40, J.ALERT, "middle", 240))
        s.append(_tag(1640.0, 525.0, "攻撃した者", sc("attacker"), 36, INK, w=250.0, h=100))
    if _on(prev, st, "power"):
        s.append(_tag(960.0, 780.0, "広く動かせる権限", J.AMBER, 44, INK))
    return s


def in3_base(st0):
    return []


def in3_stage(prev, st):
    s = []
    if _on(prev, st, "go"):
        s.append(_panel(130.0, 320.0, 560.0, 440.0, sc("user"), sw=5, dash="14 10"))
        s.append(_t(410.0, 380.0, "「お客様環境」", 40, sc("user"), "middle", 500))
        s.append(_server(410.0, 540.0, 0.96, sc("user")))
        s.append(_t(410.0, 716.0, "VPS", 40, sc("user"), "middle", 300))
        s.append(_arrow(530.0, 540.0, 1150.0, 540.0, J.ALERT, 11, 40))
        s.append(_tag(900.0, 460.0, "8月17日", J.AMBER, 50, J.AMBER))
        s.append(_panel(1160.0, 320.0, 630.0, 440.0, sc("company"), sw=6))
        s.append(_server(1475.0, 520.0, 1.05, sc("company")))
        s.append(_t(1475.0, 690.0, "管理サーバー", 50, INK, "middle", 560))
    if _on(prev, st, "side"):
        s.append(_tag(1475.0, 810.0, "会社の側", sc("company"), 42, INK))
    return s


IN4 = dict(xs=(1120.0, 1270.0, 1420.0, 1570.0, 1720.0), ys=(350.0, 470.0, 590.0), s=0.46)


def in4_base(st0):
    return []


def in4_stage(prev, st):
    s = []
    if _on(prev, st, "fan"):
        s.append(_panel(120.0, 330.0, 480.0, 390.0, sc("company"), sw=6))
        s.append(_server(360.0, 500.0, 1.05, sc("company")))
        s.append(_t(360.0, 668.0, "管理サーバー", 46, INK, "middle", 440))
        s.append(_tag(610.0, 300.0, "9月20日", J.AMBER, 40, J.AMBER))
        s.append(_arrow(730.0, 300.0, 830.0, 300.0, J.AMBER, 6, 24))
        s.append(_tag(960.0, 300.0, "10月14日", J.AMBER, 40, J.AMBER))
        for y in IN4["ys"]:
            s.append(_arrow(610.0, 525.0, 1040.0, y, J.ALERT, 6, 26))
        for y in IN4["ys"]:
            for x in IN4["xs"]:
                s.append(_server(x, y, IN4["s"], sc("user")))
    if _on(prev, st, "mal"):
        s.append(_tag(745.0, 378.0, "マルウェア", J.ALERT, 38, INK))
    if _on(prev, st, "max"):
        s.append(_t(1420.0, 742.0, "対象となり得た数", 34, INK, "middle", 620))
        s.append(_t(1420.0, 816.0, "最大 26,739台", 64, J.AMBER, "middle", 700))
    return s


# ══════════════════════════════════════════════════════════
#  gap2（c407）＝帯2本：8月5日から76日・8月17日から64日（位置は日に比例・10月20日で止まる）・c105 と別の絵
# ══════════════════════════════════════════════════════════
G2 = dict(x0=170.0, x1=1610.0, ya=430.0, yb=640.0, h=104.0, d0=_d(2026, 8, 5), d1=_d(2026, 10, 20), d2=_d(2026, 8, 17))


def g2_x(d):
    return G2["x0"] + (d - G2["d0"]).days * (G2["x1"] - G2["x0"]) / (G2["d1"] - G2["d0"]).days


def g2_days():
    return (G2["d1"] - G2["d0"]).days, (G2["d1"] - G2["d2"]).days


def gap2_base(st0):
    return []


def gap2_stage(prev, st):
    s = []
    x1, h = g2_x(G2["d1"]), G2["h"]
    a, b = g2_days()
    if _on(prev, st, "a"):
        y = G2["ya"]
        s.append(F.line(x1, 300.0, x1, 730.0, J.AMBER, 6))
        s.append(_t(x1 + 18, 340.0, "10月20日", 42, J.AMBER, "start", 300))
        s.append(_t(x1 + 18, 392.0, "止まる", 34, INK, "start", 300))
        s.append(_t(G2["x0"], y - h / 2 - 22, "8月5日から", 42, INK, "start", 500))
        s.append(F.rect(G2["x0"], y - h / 2, x1 - G2["x0"], h, J.ALERT, None, None, rx=10))
        s.append(_t((G2["x0"] + x1) / 2, y + 30, f"{a}日", 84, INK, "middle", 400))
    if _on(prev, st, "b"):
        y = G2["yb"]
        x = g2_x(G2["d2"])
        s.append(_t(x, y - h / 2 - 22, "8月17日から（管理サーバー）", 42, INK, "start", 800))
        s.append(F.rect(x, y - h / 2, x1 - x, h, sc("attacker"), None, None, rx=10))
        s.append(_t((x + x1) / 2, y + 30, f"{b}日", 84, INK, "middle", 400))
    return s


# ══════════════════════════════════════════════════════════
#  qa_why（c409）＝問答（上下）：問いは要旨・答えは字幕の字のまま（11-04 カズヤくんが耳で確かめた）
# ══════════════════════════════════════════════════════════
QW_Q = "「なぜ10月20日まで気づけなかったのか」"
QW_A = "「その回答は今持ってございません」"


def qa_why_base(st0):
    return []


def qa_why_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_quote_card(CX, 390.0, 1400.0, 180.0, (QW_Q,), sc("press"), 48, "記者の問い〈要旨〉"))
    if _on(prev, st, "a"):
        s.append(_quote_card(CX, 610.0, 1500.0, 220.0, (QW_A,), sc("company"), 66, "運営会社の副社長の答え"))
    if _on(prev, st, "next"):
        s.append(_tag(CX, 790.0, "今後の検証", J.AMBER, 40, INK))
    return s


# ══════════════════════════════════════════════════════════
#  drive（c412）＝手元のパソコンのフォルダ ↔ VPS の共有の線。札「ドライブ共有」「利用者の便利のためオン」
# ══════════════════════════════════════════════════════════
def drive_base(st0):
    return [_pc(380.0, 470.0, 1.45, sc("user")), _folder(380.0, 462.0, 0.9, sc("user")), _t(380.0, 660.0, "手元のパソコンのフォルダ", 36, sc("user"), "middle", 560),
            _server(1540.0, 490.0, 1.2, sc("company")), _t(1540.0, 660.0, "VPS", 40, sc("company"), "middle", 400)]


def drive_stage(prev, st):
    s = []
    if _on(prev, st, "line"):
        s.append(_arrow(760.0, 490.0, 600.0, 490.0, J.AMBER, 8, 30))
        s.append(_arrow(1160.0, 490.0, 1420.0, 490.0, J.AMBER, 8, 30))
        s.append(F.line(760.0, 490.0, 1160.0, 490.0, J.AMBER, 8))
        s.append(_t(960.0, 442.0, "ドライブ共有", 56, J.AMBER, "middle", 560))
    if _on(prev, st, "on"):
        s.append(_switch_on(760.0, 760.0, 1.1, J.AMBER))
        s.append(_t(850.0, 776.0, "利用者の便利のためオン", 44, INK, "start", 800))
    return s


# ══════════════════════════════════════════════════════════
#  two_says（c415）＝比べ：質疑の前の説明「可能性」↔ 質疑「確認」（どれも要旨）＝運営会社の副社長
# ══════════════════════════════════════════════════════════
TS_V = ("「可能性」", "「確認」")


def two_says_base(st0):
    return []


def two_says_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_panel(130.0, 300.0, 700.0, 340.0, J.LINE, sw=5))
        s.append(_t(480.0, 366.0, "質疑の前の説明", 40, J.LINE, "middle", 640))
        s.append(_t(480.0, 450.0, "手元のファイルを盗み取った", 36, INK, "middle", 640))
        s.append(_t(480.0, 560.0, TS_V[0], 78, J.AMBER, "middle", 640))
        s.append(_arrow(850.0, 470.0, 1070.0, 470.0, J.AMBER, 10, 36))
        s.append(_panel(1090.0, 300.0, 700.0, 340.0, J.ALERT, sw=6))
        s.append(_t(1440.0, 366.0, "質疑", 40, J.ALERT, "middle", 640))
        s.append(_t(1440.0, 450.0, "取られたことは", 36, INK, "middle", 640))
        s.append(_t(1440.0, 560.0, TS_V[1], 78, J.AMBER, "middle", 640))
    if _on(prev, st, "b"):
        s.append(_tag(CX, 730.0, "確かめたのは全部の端末ではない", J.AMBER, 44, INK))
        s.append(_t(CX, 826.0, "運営会社の副社長", 34, J.TICK, "middle", 900))
    return s


# ══════════════════════════════════════════════════════════
#  know（c417）＝並べ（左右の枠）：分かる／明らかでない・時点の札
# ══════════════════════════════════════════════════════════
KN_A = ("順番と日付", "76日")
KN_B = ("どう入ったのか", "なぜ気づけなかったのか", "攻撃した者が誰か")


def know_base(st0):
    return []


def know_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_panel(130.0, 290.0, 760.0, 450.0, sc("company"), sw=6))
        s.append(_t(510.0, 362.0, "会社の説明で分かる", 42, sc("company"), "middle", 700))
        s.append(_t(510.0, 480.0, KN_A[0], 52, INK, "middle", 700))
        s.append(_t(510.0, 590.0, KN_A[1], 72, J.AMBER, "middle", 700))
        s.append(_t(510.0, 660.0, "日数はこちらの計算", 30, J.TICK, "middle", 700))
    if _on(prev, st, "b"):
        s.append(_panel(1030.0, 290.0, 760.0, 450.0, J.AMBER, sw=5, dash="14 10"))
        s.append(_t(1410.0, 362.0, "明らかでない", 42, J.AMBER, "middle", 700))
        for i, t in enumerate(KN_B):
            s.append(_t(1410.0, 470.0 + i * 92.0, t, 46, INK, "middle", 700))
    if _on(prev, st, "when"):
        s.append(_tag(CX, 810.0, "2026年11月3日の時点", J.AMBER, 42, INK))
    return s


# ══════════════════════════════════════════════════════════
#  qa_route（c419）＝問答（左右）：記者の問い → 代表の答え（要旨）。🔴 2年前の指摘と今回の侵入を結びつけない
# ══════════════════════════════════════════════════════════
QR_Q = ("「今回攻撃された箇所は、", "2年前に指摘された", "箇所なのか」")
QR_A = ("「侵入の経路は", "まだ正確に", "把握できていない」")


def qa_route_base(st0):
    return []


def qa_route_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_panel(130.0, 290.0, 760.0, 410.0, sc("press"), sw=5))
        s.append(_t(510.0, 358.0, "記者の問い〈要旨〉", 38, sc("press"), "middle", 700))
        s.append(_lines(510.0, 462.0, QR_Q, 50, INK, "middle", 700, 76.0))
    if _on(prev, st, "a"):
        s.append(_arrow(910.0, 495.0, 1010.0, 495.0, J.AMBER, 9, 32))
        s.append(_panel(1030.0, 290.0, 760.0, 410.0, sc("company"), sw=6))
        s.append(_t(1410.0, 358.0, "グループの代表の答え〈要旨〉", 38, sc("company"), "middle", 700))
        s.append(_lines(1410.0, 462.0, QR_A, 50, INK, "middle", 700, 76.0))
    if _on(prev, st, "unk"):
        s.append(_tag(CX, 790.0, "2つの関係は不明（11月3日の時点）", J.AMBER, 44, INK))
    return s


# ══════════════════════════════════════════════════════════
#  第4章  hist（c502）＝年表（位置は日に比例・3年の線）。🔴 今回の侵入は同じ線に乗せない＝関係が分かっていない
# ══════════════════════════════════════════════════════════
HS = dict(x0=210.0, x1=1720.0, y=560.0, d0=_d(2022, 2, 1), d1=_d(2025, 2, 1))
HS_D = (_d(2022, 2, 1), _d(2024, 4, 24), _d(2024, 4, 26), _d(2024, 5, 20), _d(2025, 2, 1))
HS_Q = "「ネットのセキュリティもGMO」"


def hs_x(d):
    return HS["x0"] + (d - HS["d0"]).days * (HS["x1"] - HS["x0"]) / (HS["d1"] - HS["d0"]).days


def hist_base(st0):
    y = HS["y"]
    return [F.line(HS["x0"], y, HS["x1"], y, J.LINE, 6), F.circ(hs_x(HS_D[1]), y, 12, J.LINE),
            F.rect(hs_x(HS_D[2]), y - 8, hs_x(HS_D[3]) - hs_x(HS_D[2]), 16, J.LINE, None, None, rx=4), F.circ(hs_x(HS_D[4]), y, 12, J.LINE)]


def hist_stage(prev, st):
    s = []
    y = HS["y"]
    if _on(prev, st, "a"):
        s.append(F.circ(hs_x(HS_D[0]), y, 18, sc("sec")))
        s.append(_t(HS["x0"] - 20, y - 104, "2022年2月", 54, J.AMBER, "start", 500))
        s.append(_t(HS["x0"] - 20, y - 46, "グループ入り：セキュリティの会社", 36, INK, "start", 640))
        x = hs_x(HS_D[1])
        s.append(_t(x - 24, y - 104, "2024年4月24日", 38, J.TICK, "end", 460))
        s.append(_t(x - 24, y - 52, "報告会", 34, J.TICK, "end", 460))
        xm = (hs_x(HS_D[2]) + hs_x(HS_D[3])) / 2
        s.append(F.line(xm, y - 14, xm, 400.0, J.LINE_DIM, 3))
        s.append(_t(xm + 14, 356.0, "4月26日から5月20日", 34, J.TICK, "start", 440))
        s.append(_t(xm + 14, 404.0, "緊急メンテナンス 4回", 32, J.TICK, "start", 440))
        s.append(_t(HS["x1"] + 20, y + 72, "2025年2月", 38, J.TICK, "end", 600))
        s.append(_t(HS["x1"] + 20, y + 124, HS_Q, 34, J.TICK, "end", 620))
    if _on(prev, st, "word"):
        s.append(_tag(530.0, 690.0, "ホワイトハッカー＝守る側の腕", sc("sec"), 38, INK))
    return s


# ══════════════════════════════════════════════════════════
#  cal24（c503）＝1カ月の暦（2024年4月・曜日は日付の式）・24日に印・札2つ。c205 と別の絵
# ══════════════════════════════════════════════════════════
C24 = dict(x0=130.0, y0=340.0, w=118.0, h=86.0, y=2024, m=4, day=24)
C24_V = ("「診断結果の報告会」", "「エンジニア同士の詳細説明会」")


def c24_rc(day):
    """日 → (行, 列)。列は日曜 0。"""
    first = (_dt.date(C24["y"], C24["m"], 1).weekday() + 1) % 7
    n = first + day - 1
    return n // 7, n % 7


def c24_xy(day):
    r, c = c24_rc(day)
    return C24["x0"] + c * C24["w"], C24["y0"] + r * C24["h"]


def cal24_base(st0):
    x0, y0, w, h = C24["x0"], C24["y0"], C24["w"], C24["h"]
    g = [_t(x0, y0 - 54, "2024年4月", 40, J.TICK, "start", 500)]
    g += [_t(x0 + (i + 0.5) * w, y0 - 12, t, 26, J.TICK, "middle", w) for i, t in enumerate("日月火水木金土")]
    for r in range(5):
        for c in range(7):
            g.append(F.rect(x0 + c * w, y0 + r * h, w, h, J.BG2, J.LINE_DIM, 2, op=0.6))
    for day in range(1, _cal.monthrange(C24["y"], C24["m"])[1] + 1):
        x, y = c24_xy(day)
        if day != C24["day"]:
            g.append(_t(x + w / 2, y + h / 2 + 12, str(day), 32, J.TICK, "middle", w - 12))
    return g


def cal24_stage(prev, st):
    s = []
    if _on(prev, st, "day"):
        x, y = c24_xy(C24["day"])
        w, h = C24["w"], C24["h"]
        s.append(F.rect(x + 2, y + 2, w - 4, h - 4, J.BG2, J.AMBER, 7, rx=8))
        s.append(_t(x + w / 2, y + h / 2 + 16, str(C24["day"]), 44, J.AMBER, "middle", w - 12))
        s.append(_t(1420.0, 390.0, "2024年4月24日", 58, J.AMBER, "middle", 720))
        for i, t in enumerate(C24_V):
            yy = 500.0 + i * 130.0
            s.append(_panel(1000.0, yy - 50, 800.0, 100.0, sc("sec"), sw=5))
            s.append(_t(1400.0, yy + 15, t, 40, INK, "middle", 760))
    return s


# ══════════════════════════════════════════════════════════
#  deep_fast（c505）＝言葉：「深さと速さの両面で不足しておりました」＝運営会社の副社長（語りと図が同じ字＝字幕を重ねない）
# ══════════════════════════════════════════════════════════
DF_Q = "「深さと速さの両面で不足しておりました」"


def deep_fast_base(st0):
    return []


def deep_fast_stage(prev, st):
    s = []
    if _on(prev, st, "m4"):
        s.append(_tag(620.0, 340.0, "4月26日", J.AMBER, 44, J.AMBER))
        s.append(_arrow(800.0, 340.0, 1090.0, 340.0, J.AMBER, 7, 26))
        s.append(_tag(1280.0, 340.0, "5月20日", J.AMBER, 44, J.AMBER))
        s.append(_t(CX, 450.0, "緊急メンテナンス 4回", 54, INK, "middle", 1000))
    if _on(prev, st, "say"):
        s.append(_quote_card(CX, 640.0, 1600.0, 270.0, (DF_Q,), sc("company"), 68, "運営会社の副社長", "説明会（2026年11月2日）"))
    return s


# ══════════════════════════════════════════════════════════
#  sort5（c507）＝入れ子の箱：並べて順番を決めていたもの＝副社長の説明の語だけ
# ══════════════════════════════════════════════════════════
S5_A = "セキュリティの修正の影響"
S5_B = ("グループ全体の脆弱性の対応", "機能の開発", "性能の向上", "使いやすさ")


def sort5_base(st0):
    return [_panel(150.0, 290.0, 1620.0, 530.0, sc("company"), sw=5), _t(CX, 356.0, "同じ箱で順番を決める", 40, sc("company"), "middle", 1400)]


def sort5_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_tag(CX, 450.0, S5_A, J.ALERT, 50, INK, w=980.0, h=110))
    if _on(prev, st, "b"):
        for i, t in enumerate(S5_B):
            x, y = (560.0, 1360.0)[i % 2], (600.0, 720.0)[i // 2]
            s.append(_tag(x, y, t, J.LINE, 42, INK, w=740.0, h=96))
    return s


# ══════════════════════════════════════════════════════════
#  report_flow（c511）＝流れ：セキュリティの会社 → 事業の側／システムの側（役職だけ）・札「社長の説明はここまで」
# ══════════════════════════════════════════════════════════
def report_flow_base(st0):
    return []


def report_flow_stage(prev, st):
    s = []
    if _on(prev, st, "from"):
        s.append(_tag(320.0, 500.0, "セキュリティの会社", sc("sec"), 44, INK, w=450.0, h=110))
        s.append(_t(320.0, 600.0, "指摘の報告", 34, J.TICK, "middle", 420))
    if _on(prev, st, "two"):
        s.append(_arrow(550.0, 460.0, 760.0, 400.0, J.LINE, 8, 30))
        s.append(_arrow(550.0, 540.0, 760.0, 640.0, J.LINE, 8, 30))
        s.append(_panel(780.0, 290.0, 1000.0, 220.0, sc("company"), sw=6))
        s.append(_t(1280.0, 352.0, "事業の側", 40, sc("company"), "middle", 900))
        s.append(_t(1280.0, 418.0, "運営会社の社長", 46, INK, "middle", 900))
        s.append(_t(1280.0, 482.0, "事業の責任者", 40, INK, "middle", 900))
        s.append(_panel(780.0, 560.0, 1000.0, 110.0, sc("company"), sw=6))
        s.append(_t(1060.0, 630.0, "システムの側", 40, sc("company"), "middle", 480))
        s.append(_t(1500.0, 632.0, "副社長", 46, INK, "middle", 480))
    if _on(prev, st, "then"):
        s.append(_tag(320.0, 700.0, "社長は当時 グループの取締役", J.AMBER, 30, INK, w=460.0, h=80))
        s.append(_tag(1280.0, 790.0, "社長の説明はここまで", J.AMBER, 44, INK))
    return s


# ══════════════════════════════════════════════════════════
#  two_ans（c513）＝並べ（上下の枠）：報告の基準の答えが2つ（要旨）。役職だけ・c417 と別の絵
# ══════════════════════════════════════════════════════════
TA_A = "基準はある"
TA_B = ("どんな脆弱性なら取締役に上げるかの", "基準は当時は無かった")


def two_ans_base(st0):
    return [_panel(150.0, 300.0, 1620.0, 210.0, sc("company"), sw=5), _t(430.0, 420.0, "グループの代表", 46, sc("company"), "middle", 500),
            _panel(150.0, 550.0, 1620.0, 260.0, sc("user"), sw=5), _t(430.0, 695.0, "グループの法務部長", 44, sc("user"), "middle", 500)]


def two_ans_stage(prev, st):
    s = []
    if _on(prev, st, "say"):
        s.append(_t(1190.0, 424.0, TA_A, 74, J.AMBER, "middle", 1040))
        s.append(_t(1190.0, 656.0, TA_B[0], 42, INK, "middle", 1040))
        s.append(_t(1190.0, 730.0, TA_B[1], 58, J.AMBER, "middle", 1040))
    return s


# ══════════════════════════════════════════════════════════
#  resil（c519）＝模式：入られないだけの守り ↔ 早く食い止めて回復する の2つの線・札「レジリエンス」（数ではない）
# ══════════════════════════════════════════════════════════
RS = dict(x0=260.0, x1=1660.0, top=400.0, low=730.0, t0=700.0)


def resil_base(st0):
    return [F.line(RS["x0"], RS["low"] + 30, RS["x1"], RS["low"] + 30, J.LINE, 4), _t(RS["x1"], RS["low"] + 72, "時間", 30, J.TICK, "end", 200),
            _t(RS["x0"] - 16, RS["top"] - 36, "サービスの動き", 30, J.TICK, "start", 400)]


def resil_stage(prev, st):
    s = []
    x0, x1, top, low, t0 = RS["x0"], RS["x1"], RS["top"], RS["low"], RS["t0"]
    if _on(prev, st, "a"):
        s.append(_tag(CX, 310.0, "レジリエンス", J.AMBER, 50, INK))
        s.append(F.poly([(x0, top), (t0, top), (t0 + 120, low - 10), (x1, low - 10)], "none", J.LINE_DIM, 8))
        s.append(_t(x1, low - 34, "入られないだけの守り", 36, J.TICK, "end", 620))
        s.append(_t(t0, top - 24, "入られる", 34, J.ALERT, "middle", 240))
        s.append(F.line(t0, top - 10, t0, low + 30, J.ALERT, 4, dash="10 8"))
    if _on(prev, st, "b"):
        s.append(F.poly([(x0, top), (t0, top), (t0 + 70, top + 150), (t0 + 200, top + 150), (t0 + 360, top + 8), (x1, top + 8)], "none", J.AMBER, 10))
        s.append(_t(x1, top + 66, "早く食い止めて回復する", 40, J.AMBER, "end", 620))
    if _on(prev, st, "late"):
        s.append(_tag(470.0, 620.0, "この変化が遅れた", J.ALERT, 42, INK))
    return s


# ══════════════════════════════════════════════════════════
#  第5章  scope（c603）＝左右の枠：補償の対象／対象の外（開示 2026-10-24）。c507 と別の絵
# ══════════════════════════════════════════════════════════
SC_A = ("不正と認めた取引", "実現損失（取引の差損と手数料など）")
SC_B = ("市場の変動による損失", "得られたはずの利益", "間接的な損害")


def scope_base(st0):
    return []


def scope_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_panel(130.0, 300.0, 800.0, 470.0, sc("company"), sw=6))
        s.append(_t(530.0, 376.0, "補償の対象", 48, sc("company"), "middle", 740))
        s.append(_t(530.0, 510.0, SC_A[0], 50, INK, "middle", 740))
        s.append(_t(530.0, 610.0, SC_A[1], 36, J.AMBER, "middle", 740))
    if _on(prev, st, "b"):
        s.append(_panel(990.0, 300.0, 800.0, 470.0, J.LINE_DIM, sw=5, dash="14 10"))
        s.append(_t(1390.0, 376.0, "対象の外", 48, J.ALERT, "middle", 740))
        for i, t in enumerate(SC_B):
            s.append(_t(1390.0, 486.0 + i * 92.0, t, 44, INK, "middle", 740))
    return s


# ══════════════════════════════════════════════════════════
#  sum3（c606）＝式：3つの区分の額（第12報の表）。公開された情報の中身には触れない・🔴 合計は図に出さない（c607 の語り）
# ══════════════════════════════════════════════════════════
S3 = dict(xs=(350.0, 960.0, 1570.0), y=560.0, w=520.0, h=270.0)
S3_V = (("基本的な情報", "10,000円"), ("金融・認証の情報", "15,000円"), ("プライバシー性の", "高い情報", "25,000円"))


def sum3_base(st0):
    return []


def sum3_stage(prev, st):
    s = []
    if _on(prev, st, "who"):
        s.append(_tag(CX, 340.0, "公開された情報の区分ごと", sc("company"), 40, INK))
    if _on(prev, st, "cards"):
        for i, v in enumerate(S3_V):
            x, y, w, h = S3["xs"][i], S3["y"], S3["w"], S3["h"]
            s.append(_panel(x - w / 2, y - h / 2, w, h, sc("company"), sw=5))
            s.append(_lines(x, y - 66 if len(v) == 3 else y - 40, v[:-1], 38, INK, "middle", w - 40, 50.0))
            s.append(_t(x, y + 90, v[-1], 72, J.AMBER, "middle", w - 40))
        for x in (655.0, 1265.0):
            s.append(_t(x, S3["y"] + 26, "＋", 72, INK, "middle", 80))
    return s


# ══════════════════════════════════════════════════════════
#  paycut（c609）＝割合：代表の月額 30%（帯の長さは割合に比例）・3カ月・12月支給分から・「役員4名」だけ。🔴 開示の表は名前があるので出さない＝こちらで組む
# ══════════════════════════════════════════════════════════
PC = dict(x0=300.0, k=13.2, y=470.0, h=110.0)
PC_V = (30.0, 100.0)


def pc_x(v):
    return PC["x0"] + v * PC["k"]


def paycut_base(st0):
    return []


def paycut_stage(prev, st):
    s = []
    y, h = PC["y"], PC["h"]
    if _on(prev, st, "cut"):
        s.append(_t(pc_x(PC_V[1]), y - h / 2 - 22, "代表の月額", 42, INK, "end", 500))
        s.append(F.rect(PC["x0"], y - h / 2, pc_x(PC_V[1]) - PC["x0"], h, J.LINE_DIM, None, None, rx=8))
        s.append(F.rect(PC["x0"], y - h / 2, pc_x(PC_V[0]) - PC["x0"], h, J.ALERT, None, None, rx=8))
        s.append(_t((PC["x0"] + pc_x(PC_V[0])) / 2, y + 28, "30%", 78, INK, "middle", 380))
        s.append(_t(PC["x0"], y - h / 2 - 22, "減らす分", 42, J.ALERT, "start", 400))
        for i, t in enumerate(("3カ月", "12月支給分から", "役員4名")):
            s.append(_tag(480.0 + i * 480.0, 640.0, t, J.AMBER, 44, INK, w=420.0, h=96))
    if _on(prev, st, "next"):
        s.append(_t(CX, 790.0, "経営責任は検証のあとに", 44, INK, "middle", 1200))
    return s


# ══════════════════════════════════════════════════════════
#  ai_say（c615）＝問い → 言葉（要旨）→ 3つの札。c505 と別の絵
# ══════════════════════════════════════════════════════════
AI_Q = "「基本的に、AIが使われた証拠は無い」"
AI_T = ("使われたかは不明", "事件とAIは別の話", "AIのせいにはしない")


def ai_say_base(st0):
    return []


def ai_say_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_tag(CX, 330.0, "問い：AIが使われた証拠は？", sc("press"), 40, INK))
    if _on(prev, st, "a"):
        s.append(_quote_card(CX, 510.0, 1560.0, 230.0, (AI_Q,), sc("company"), 62, "グループの代表の答え〈要旨〉"))
    if _on(prev, st, "b"):
        for i, t in enumerate(AI_T):
            s.append(_tag(390.0 + i * 570.0, 730.0, t, J.LINE, 38, INK, w=530.0, h=96))
    return s


# ══════════════════════════════════════════════════════════
#  第6章  contact（c701）＝窓口（ルール §B2-11 ④・🔴 番号は ⑥ の直前に頁で当て直す）・tipline（c703）＝情報の提供の窓口（字だけ・リンクと画面なし）
# ══════════════════════════════════════════════════════════
CT_TEL = "03-5456-2560"
CT_URL = "help.onamae.com/contact/"
TL_SITE = "cybercrimebounty.gmo"
TL_MAIL = "info@cybercrimebounty.gmo"
TL_Q = "「ご自身での犯人の特定や接触、確証のない情報の投稿はお控えいただき」"
TL_SRC = ("出典：GMOインターネットグループ『【重要】「お名前.com デスクトップクラウド」への不正アクセスに関する",
          "現在の対応について（第16報）』2026-10-29 20:50時点 group.gmo/info/alert/2026102902/")


def contact_base(st0):
    return [_panel(220.0, 300.0, 1480.0, 500.0, sc("company"), sw=5)]


def contact_stage(prev, st):
    s = []
    if _on(prev, st, "tel"):
        s.append(_phone(340.0, 440.0, 0.9, sc("company")))
        s.append(_t(420.0, 396.0, "電話（土日・祝日を含め24時間）", 38, sc("company"), "start", 1200))
        s.append(_t(420.0, 500.0, CT_TEL, 84, INK, "start", 1200))
    if _on(prev, st, "form"):
        s.append(F.line(280.0, 570.0, 1640.0, 570.0, J.LINE_DIM, 3))
        s.append(_t(420.0, 650.0, "問い合わせフォーム", 38, sc("company"), "start", 1200))
        s.append(_t(420.0, 730.0, CT_URL, 58, INK, "start", 1200))
    return s


def tipline_base(st0):
    return []


def tipline_stage(prev, st):
    s = []
    if _on(prev, st, "where"):
        for i, (a, b) in enumerate((("専用サイト", TL_SITE), ("メール", TL_MAIL))):
            x = 530.0 + i * 860.0
            s.append(_panel(x - 410.0, 330.0, 820.0, 190.0, sc("company"), sw=5))
            s.append(_t(x, 396.0, a, 36, sc("company"), "middle", 760))
            s.append(_t(x, 476.0, b, 50, INK, "middle", 770))
    if _on(prev, st, "ask"):
        s.append(_quote_card(CX, 680.0, 1680.0, 120.0, (TL_Q,), J.AMBER, 44))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表（mech28 と同じ作り）
# ══════════════════════════════════════════════════════════
def _v(lab, fields, base, stage):
    return dict(lab=lab, fields={f_: ONOFF for f_ in fields}, base=base, stage=stage)


_SNS_LAB = "SNS の投稿（原文どおりの字を札に）"
#   左上の札は形の名前だけ（話題は見出しと副題＝同じ画面で同じ言葉を二度出さない・門番 dup）
VIEWS = dict(
    gap76=_v("時間の帯", ("band", "blind", "ask"), gap76_base, gap76_stage),
    vps=_v("正面から見た図", ("vps", "rd"), vps_base, vps_stage),
    cal3=_v("正面から見た暦", ("a", "b"), cal3_base, cal3_stage),
    num26739=_v("正面から見た札", ("a", "b"), num26739_base, num26739_stage),
    two_reports=_v("正面から見た2つの札", ("a", "b"), two_reports_base, two_reports_stage),
    ransom=_v("正面から見た図", ("lock", "ask"), ransom_base, ransom_stage),
    clock_noon=_v("正面から見た時計", ("both", "ask"), clock_noon_base, clock_noon_stage),
    sns307=_v(_SNS_LAB, ("a", "b"), sns_base, sns307_stage),
    bounty=_v("正面から見た札", ("a", "b"), bounty_base, bounty_stage),
    tips=_v("縦の棒", ("police", "bars", "none"), tips_base, tips_stage),
    order4=_v("時間の線", ("lab",), order4_base, order4_stage),
    in1=_v("正面から見た図", ("who", "in"), in1_base, in1_stage),
    in2=_v("正面から見た図", ("key", "power"), in2_base, in2_stage),
    in3=_v("正面から見た図", ("go", "side"), in3_base, in3_stage),
    in4=_v("正面から見た図", ("fan", "mal", "max"), in4_base, in4_stage),
    gap2=_v("時間の帯", ("a", "b"), gap2_base, gap2_stage),
    qa_why=_v("正面から見た札", ("q", "a", "next"), qa_why_base, qa_why_stage),
    drive=_v("正面から見た図", ("line", "on"), drive_base, drive_stage),
    two_says=_v("正面から見た2つの札", ("a", "b"), two_says_base, two_says_stage),
    know=_v("正面から見た2つの枠", ("a", "b", "when"), know_base, know_stage),
    qa_route=_v("正面から見た2つの札", ("q", "a", "unk"), qa_route_base, qa_route_stage),
    hist=_v("時間の線", ("a", "word"), hist_base, hist_stage),
    cal24=_v("正面から見た暦", ("day",), cal24_base, cal24_stage),
    deep_fast=_v("正面から見た札", ("m4", "say"), deep_fast_base, deep_fast_stage),
    sort5=_v("正面から見た箱", ("a", "b"), sort5_base, sort5_stage),
    report_flow=_v("左から右へ：報告の流れ", ("from", "two", "then"), report_flow_base, report_flow_stage),
    two_ans=_v("正面から見た2つの枠", ("say",), two_ans_base, two_ans_stage),
    resil=_v("2つの線", ("a", "b", "late"), resil_base, resil_stage),
    scope=_v("正面から見た2つの枠", ("a", "b"), scope_base, scope_stage),
    sns618=_v(_SNS_LAB, ("a", "b"), sns_base, sns618_stage),
    sum3=_v("正面から見た式", ("who", "cards"), sum3_base, sum3_stage),
    paycut=_v("割合の帯", ("cut", "next"), paycut_base, paycut_stage),
    ai_say=_v("正面から見た札", ("q", "a", "b"), ai_say_base, ai_say_stage),
    sns616=_v(_SNS_LAB, ("a", "b"), sns_base, sns616_stage),
    sns617=_v(_SNS_LAB, ("a",), sns_base, sns617_stage),
    sns619=_v(_SNS_LAB, ("a", "b"), sns_base, sns619_stage),
    contact=_v("正面から見た札", ("tel", "form"), contact_base, contact_stage),
    tipline=_v("正面から見た札", ("where", "ask"), tipline_base, tipline_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
# 模式（比例でも原文の字でもない関係の絵）＝左上に「模式」を付ける・note に「模式」を書く
SCHEMATIC = ("vps", "ransom", "in1", "in2", "in3", "in4", "drive", "sort5", "report_flow", "resil")
SNS_VIEWS = ("sns307", "sns618", "sns616", "sns617", "sns619")
QUOTE_VIEWS = dict(sns307=("k307",), sns618=("k618",), sns616=("k616",), sns617=("k617",), sns619=("k619",))
# 見え方ごとの注の字幅（出典の行が2行になる c703 は段の中で描く＝注は空）
SRC_IN_STAGE = ("tipline",)


def lab_of(view, st0):
    # ⑤c'（28本目）：抽象の図に「正面から見た○○」は中学生に通じない・見る向きの門番は PLAN に「見る向き：」が無ければ見ない＝左上に出さない
    lab = VIEWS[view]["lab"]
    return "" if lab.startswith("正面から見た") else lab


def _states(view, start, steps):
    fields = VIEWS[view]["fields"]
    cur = dict(START[view], **(start or {}))
    out = []
    for st in [dict(state={})] + list(steps):
        cur = dict(cur, **(st.get("state") or {}))
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m29：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m29：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    return out[0], out[1:]


def stage_art(view, prev, st):
    return VIEWS[view]["stage"](prev, st)


def _base(view, st0):
    """基図＋頭の状態の層（頭で on にした欄は基図に描く）"""
    return VIEWS[view]["base"](st0) + stage_art(view, dict(START[view]), st0)


def _stage_svgs(view, steps, start, states):
    stages = []
    prev = start
    for _st, stt in zip(steps, states):
        s = stage_art(view, prev, stt)
        stages.append("".join(s) or " ")
        prev = stt
    return stages


def quote_lines(view):
    """原文どおりに大きく出す字（門番 echo の例外＝その行の字幕は SPEC の mute で消す）。"""
    if view in QUOTE_VIEWS:
        return [ln for k in QUOTE_VIEWS[view] for ln in SNS_CARDS[k][0]]
    return {"num26739": [N2_A, N2_B], "qa_why": [QW_Q, QW_A], "qa_route": list(QR_Q) + list(QR_A), "deep_fast": [DF_Q],
            "ai_say": [AI_Q], "tipline": [TL_Q]}.get(view, [])


def m29(view, steps, start=None, rel=(), note="", src="", mute=()):
    """29本目の図解。view は VIEWS の見え方。steps＝ナレーションの行ごとの段。
    mute＝原文どおりの字を大きく出す札の字を読む行（字幕を消す＝scene_jiko.SUB_MUTE）。"""
    if quote_lines(view) and not mute:
        raise ValueError(f"m29：{view} は原文どおりの字を大きく出す＝その字を読む行を mute に書く（字幕と二重に出さない）")
    if view not in VIEWS:
        raise ValueError(f"m29：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view in SCHEMATIC and "模式" not in note:
        raise ValueError("m29：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    g = _base(view, st0)
    lab = lab_of(view, st0)
    lab_t = "・".join(x for x in (lab, "模式" if view in SCHEMATIC else "") if x)
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, lab_t, 1000, cap=30, col=J.TICK, ol=OL) if lab_t else "")
    if view in SRC_IN_STAGE:
        g.append(F.txtfit(F.BX0, F.BY1 - 40, TL_SRC[0], F.BW, cap=26, col=J.TICK, ol=OL) + F.txtfit(F.BX0, F.BY1 - 6, TL_SRC[1], F.BW, cap=26, col=J.TICK, ol=OL))
    else:
        g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW * 0.60 if view in SNS_VIEWS else F.BW,
                          cap=26, col=J.TICK, ol=OL))
    stages = _stage_svgs(view, steps, st0, states)
    base_svg = "".join(g)
    f = F.Fig(base_svg, stages, "", (F.BX0, F.BX1))
    f.moves = []
    body = "".join(g[:-2]) + "".join(stages)
    f.mech = dict(kind="m29", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=[], lab=lab, note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states), texts_all=svg_texts(body),
                  sns=bool(view in SNS_VIEWS))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M29）
# ══════════════════════════════════════════════════════════
VIEW_SRC = dict(gap76=("user",), vps=("company", "user"), cal3=("company",), num26739=("company",), two_reports=("company",), ransom=("attacker",), clock_noon=("company", "attacker"),
                bounty=("company",), tips=("police",), in1=("attacker", "user"), in2=("attacker", "user"), in3=("company", "user"), in4=("company", "user"), gap2=("attacker",),
                qa_why=("press", "company"), drive=("company", "user"), know=("company",), qa_route=("press", "company"), hist=("sec",), cal24=("sec",), deep_fast=("company",), sort5=("company",),
                report_flow=("sec", "company"), two_ans=("company", "user"), scope=("company",), sum3=("company",), ai_say=("press", "company"), contact=("company",), tipline=("company",))


def _geo(view):
    if view == "gap76":
        return dict(val=(GP["d0"].isoformat(), GP["d1"].isoformat(), gp_days()), pxx=(gp_x(GP["d0"]), gp_x(GP["d1"])) + tuple(gp_x(d) for d, _t2 in GP_M),
                    linx=((GP["x0"], (GP["x1"] - GP["x0"]) / gp_days(), 0.0),) * 4)
    if view == "cal3":
        return dict(val=tuple((d.isoformat(), _WD[d.weekday()], lines) for d, lines in C3_V))
    if view == "num26739":
        return dict(val=(N2_V, N2_A, N2_B))
    if view == "two_reports":
        return dict(val=("".join(TR_A), "".join(TR_B)))
    if view == "clock_noon":
        return dict(val=tuple((d, h, m) for d, h, m in CN_T), hands=tuple(ck_angles(h, m) for _d, h, m in CN_T))
    if view == "bounty":
        return dict(val=BT_V)
    if view == "tips":
        k = TP["dx"]
        return dict(val=tuple((d.isoformat(), v) for d, v, _l in TP_V), px=tuple(tp_y(v) for _d, v, _l in TP_V), lins=((TP["y0"], -TP["k"], 0.0),) * 4,
                    pxx=tuple(tp_x(d) for d, _v, _l in TP_V), linx=((TP["x0"], k, 0.0),) * 4)
    if view == "order4":
        k = (O4["x1"] - O4["x0"]) / (O4["d1"] - O4["d0"]).days
        return dict(val=tuple(d.isoformat() for d in O4_D), pxx=tuple(o4_x(d) for d in O4_D), linx=((O4["x0"], k, 0.0),) * 5)
    if view == "gap2":
        k = (G2["x1"] - G2["x0"]) / (G2["d1"] - G2["d0"]).days
        return dict(val=g2_days(), pxx=(g2_x(G2["d0"]), g2_x(G2["d2"]), g2_x(G2["d1"])), linx=((G2["x0"], k, 0.0),) * 3)
    if view == "qa_why":
        return dict(val=(QW_Q, QW_A))
    if view == "two_says":
        return dict(val=TS_V)
    if view == "know":
        return dict(val=(KN_A, KN_B))
    if view == "qa_route":
        return dict(val=("".join(QR_Q), "".join(QR_A)))
    if view == "hist":
        k = (HS["x1"] - HS["x0"]) / (HS["d1"] - HS["d0"]).days
        return dict(val=(tuple(d.isoformat() for d in HS_D), HS_Q), pxx=tuple(hs_x(d) for d in HS_D), linx=((HS["x0"], k, 0.0),) * 5)
    if view == "cal24":
        return dict(val=(_dt.date(C24["y"], C24["m"], C24["day"]).isoformat(), c24_rc(C24["day"]), C24_V))
    if view == "deep_fast":
        return dict(val=(DF_Q,))
    if view == "sort5":
        return dict(val=(S5_A,) + S5_B)
    if view == "two_ans":
        return dict(val=(TA_A, "".join(TA_B)))
    if view == "scope":
        return dict(val=(SC_A, SC_B))
    if view == "sum3":
        return dict(val=tuple(("".join(v[:-1]), v[-1]) for v in S3_V))
    if view == "paycut":
        return dict(val=PC_V, px=tuple(pc_x(v) for v in PC_V), lins=((PC["x0"], PC["k"], 0.0),) * 2)
    if view == "ai_say":
        return dict(val=(AI_Q,))
    if view in SNS_VIEWS:
        return dict(val=tuple((k, SNS_CARDS[k][0], SNS_CARDS[k][1]) for k in sorted(SNS_CARDS)))
    if view == "contact":
        return dict(val=(CT_TEL, CT_URL))
    if view == "tipline":
        return dict(val=(TL_SITE, TL_MAIL, TL_Q, "".join(TL_SRC)))
    return {}


def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst], src={k: tuple(v) for k, v in SRC.items()}, vsrc=tuple(VIEW_SRC.get(view, ())))
    out.update(_geo(view))
    return out
