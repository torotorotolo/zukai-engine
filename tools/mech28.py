# -*- coding: utf-8 -*-
"""mech28.py — 28本目（タイムズカー情報漏えい・2026-09-25 検知・タイムズモビリティへの不正アクセス）「図解」（2026-11-02 新設・⑤b-4＝図34カット）。

■ 何か
  27本目 `mech27` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品は使わない」。再現イラストではない＝「再現」の札は出さない。
  🔴 **地は写真**（`cuts.ss.gr`＝CC BY・CC0・PD を暗くするだけ・方眼と章の色なし・静止）＝字はどれも暗い縁取り（OL）・札の地は半ば透ける紺（`_panel`）。
     字と図の線の周りの地は門番 check_ground が 8:1 で測る。
  左上に見え方の名（模式の見え方は末尾に「・模式」）・左下に注（模式の見え方は「模式」）と出典。
  🔴 会社の事件の決まり（ルール §B2-11）：会員・SNS の投稿者・役員・弁護士の名前は描かない（役職だけ）・攻撃した者は「第三者」「攻撃した者」・
     会社を「犯人」「加害者」と言わない（SNS の原文の札だけ原文のまま）・「漏えい」で揃える（「流出」は SNS の原文の札だけ）・
     c614 の「ローンを組まれた」は相談として会社の言葉と並べる。**人は描かない**。手口の推測の絵は描かない（会社の説明の3段だけ）。
  🔴 **色は「誰か・何か」**（役の色＝SRC・新しい色の値は足していない）：会社（タイムズモビリティ・パーク24）＝青 uscg／攻撃した者＝橙 company／
     弁護士＝茶 DOC／国（委員会・金融庁・法令）＝紫 tsb／銀行＝水色 ship／信用情報機関＝緑 ntsb／会員＝桃 bldg_a／SNS の声＝白い札。
     同じ色の鍵は同じ画面に出さない（門番 judge_m28 が VIEW_SRC で見る）。意味の色＝赤 ALERT（漏えい・止まった）・黄 AMBER（数・日付）。
  🔴 画面の数は全部 `rel=` に同じ文字列で宣言する（門番が基図と段の層の全部の字から数を拾って照らす）。
  🔴 記録の値（色・数・比例・会社と法令の言葉・SNS の原文）は門番の側 REC_M28 が別に持つ（§5b-88）。描く側の表を書き換えると鳴る。

■ 見え方（view）＝映像方針の一覧 `ref/ep28/eizou_list28.md` の「種類」（図34）
  つかみ  three（c105 3つの数）
  第1章  flow8（c202 9月25日の8項目）・clock2（c203 2つの時計）・reports（c207 知らせの階段）・route3（c209 説明の3段）・cal4w（c215 4週間の暦）
  第2章  six（c302 6つの情報）・bars2（c305 縦の棒2本）・words2（c308 2つの言葉）・club（c311 もう1つのシステム）・ccard（c312 カードの絵）・fixn（c314 直された数）
  第3章  unit2（c402 横の棒2本）・inside（c403 4つの箱）・purpose4（c405 4つの目的）・qa7（c407 問答）・law22（c409 条文）・rule_oct（c414 年表と表）・bank2（c420 銀行2つ）
  第4章  risk4（c501 4つのおそれ）・law_kyc（c504 法と規則）・fsa_check（c507 注意喚起）・jicc5（c512 5日の帯）・qa12（c513 問答2つ）
  第5章  cutoff（c603 対象の外）・formula（c604 式）・profit（c607 縦の棒）・damages（c610 横の棒3本）・quote3000（c612 言葉）・two_claims（c614 2つを並べる）・
         sns2（c616）・sns1b（c617）・sns3（c618）
  第6章  contact（c701 窓口）
  🔴 同じ型は近くで続けない：c202（縦の列）↔c203（時計）↔c207（階段）↔c209（横の3箱）↔c215（暦）・c305（縦の棒）↔c308（左右の札）↔c311（箱の表）↔c312（カードの絵）↔c314（左→右）・
     c402（横の棒）↔c403（2×2）↔c405（真ん中から4方向）・c607（縦の棒）↔c610（横の棒）・SNS は c616（1枚）↔c617（2枚が順に）↔c618（2枚・大きさ違い）。

■ SPEC の書き方（mech27 と同じ）
  `**ss.gr("cm063"), fig=("m28", dict(view=…, steps=[dict(state=dict(…)), …], rel=[dict(t="146万4800件", src="第5報")], note="…", src="…"))`
  原文どおりの字を読む行は `mute=[行の番号]`（字幕を消す＝scene_jiko.SUB_MUTE・門番 echo の例外は `quote_lines`）。
"""
from __future__ import annotations

import datetime as _dt
import math

import jiko_style as J
import titan_fig as F
from mech21 import _arrow, _on
from mech24 import rc
from mech27 import CARD, CARD_INK, CARD_SUB, CX, INK, OL, ONOFF, _panel, _phone, _sns_note, _t, _tag, svg_texts

# 誰か・何か（名・ROLE か J の名）。同じ色の鍵は同じ画面に出さない（門番が VIEW_SRC で見る）
SRC = dict(
    company=("会社", "uscg"),
    attacker=("攻撃した者", "company"),
    lawyer=("弁護士", "DOC"),
    kuni=("国", "tsb"),
    bank=("銀行", "ship"),
    jicc=("信用情報機関", "ntsb"),
    member=("会員", "bldg_a"),
    sns=("SNS の声", "SUB"),
)


def sc(key):
    return rc(SRC[key][1])


def _lines(x, y, lines, cap, col=None, anchor="middle", mw=900.0, lh=None):
    """複数行の字（y＝1行目のベースライン）。"""
    lh = lh or cap * 1.42
    return "".join(_t(x, y + i * lh, ln, cap, col, anchor, mw) for i, ln in enumerate(lines))


def _quote_card(cx, cy, w, h, lines, col, cap=46, head=None, foot=None, op=None, dash=None):
    """言葉の札：上に誰の言葉か・真ん中に原文の行・下に出どころ。"""
    g = _panel(cx - w / 2, cy - h / 2, w, h, col, op=op if op is not None else 0.84, sw=5, dash=dash)
    if head:
        g += _t(cx, cy - h / 2 + 52, head, 32, col, "middle", w - 40)
    lh = cap * 1.42
    n = len(lines)
    top = cy - (n - 1) * lh / 2 + cap * 0.36 + (18 if head else 0) - (14 if foot else 0)
    g += _lines(cx, top, lines, cap, INK, "middle", w - 60, lh)
    if foot:
        g += _t(cx, cy + h / 2 - 20, foot, 26, J.TICK, "middle", w - 40)
    return g


def _idcard(cx, cy, s, col):
    """本人確認書類の絵（顔は描かない＝線と四角だけ）。"""
    w, h = 190 * s, 120 * s
    return (F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 6, rx=12)
            + F.rect(cx - w / 2 + 16 * s, cy - h / 2 + 22 * s, 48 * s, 62 * s, "none", col, 4, rx=4)
            + "".join(F.line(cx - w / 2 + 84 * s, cy - h / 2 + (30 + 26 * i) * s, cx + w / 2 - 16 * s, cy - h / 2 + (30 + 26 * i) * s, col, 5) for i in range(3)))


def _mail(cx, cy, s, col):
    w, h = 96 * s, 66 * s
    return (F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 5, rx=6)
            + F.poly([(cx - w / 2, cy - h / 2), (cx, cy + 4 * s), (cx + w / 2, cy - h / 2)], "none", col, 5))


def _warn(cx, cy, s, col):
    r = 46 * s
    return (F.poly([(cx, cy - r), (cx + r, cy + r * 0.8), (cx - r, cy + r * 0.8)], J.BG2, col, 6, close=True)
            + F.line(cx, cy - r * 0.35, cx, cy + r * 0.25, col, 7) + F.circ(cx, cy + r * 0.52, 5 * s, col))


def _bubble_icon(cx, cy, s, col):
    w, h = 96 * s, 60 * s
    return (F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 5, rx=16)
            + F.poly([(cx - 22 * s, cy + h / 2 - 2), (cx - 34 * s, cy + h / 2 + 22 * s), (cx - 2 * s, cy + h / 2 - 2)], J.BG2, col, 5))


# ══════════════════════════════════════════════════════════
#  つかみ  three（c105）＝3つの数の札（札は全編2回まで＝c105・c312）・数ごとに出どころの行
# ══════════════════════════════════════════════════════════
TH = dict(cx=(350.0, 960.0, 1570.0), y=560.0, w=540.0, h=340.0)
TH_V = (("画像：外へ送られた跡あり", "146万4800件", "第5報（2026年10月23日）", "company"),
        ("見舞金", "3000円分", "第5報（2026年10月23日）", "company"),
        ("訴えに加わりたい人", "10万人超", "弁護士側（2026年10月26日の報道）", "lawyer"))


def _three_card(i):
    lab, v, src, who = TH_V[i]
    x, y, w, h = TH["cx"][i], TH["y"], TH["w"], TH["h"]
    return (_panel(x - w / 2, y - h / 2, w, h, sc(who), sw=5)
            + _t(x, y - 92, lab, 34, sc(who), "middle", w - 40)
            + _t(x, y + 34, v, 84, J.AMBER, "middle", w - 40)
            + _t(x, y + 128, src, 26, J.TICK, "middle", w - 40))


def three_base(st0):
    return []


def three_stage(prev, st):
    s = []
    if _on(prev, st, "ab"):
        s += [_three_card(0), _three_card(1)]
    if _on(prev, st, "c"):
        s.append(_three_card(2))
    return s


# ══════════════════════════════════════════════════════════
#  第1章  flow8（c202）＝9月25日の8項目（第5報の経緯の表の並び・表に時刻は無い＝矢印を引かない）。語りが言う3つだけ灯す
# ══════════════════════════════════════════════════════════
FW = dict(x=500.0, y0=300.0, dy=74.0, lit=(3, 4, 6))
FW_V = ("不正アクセスを検知", "問い合わせ窓口開設", "調査開始", "対象サーバーを隔離", "不正アクセス経路を遮断",
        "外部専門機関によるフォレンジック調査を開始", "個人情報保護委員会へ報告", "第1報を公表")


def fw_y(i):
    return FW["y0"] + i * FW["dy"]


def flow8_base(st0):
    x = FW["x"]
    g = [_t(280.0, 566.0, "9月25日", 60, J.AMBER, "middle", 340), F.line(x, fw_y(0), x, fw_y(7), J.LINE_DIM, 4)]
    for i, t in enumerate(FW_V):
        y = fw_y(i)
        g.append(F.circ(x, y, 8, J.LINE_DIM))
        if i not in FW["lit"]:      # 語りが言う3つは、その行で初めて出す（薄い字の上に重ねない＝門番 layout）
            g.append(_t(x + 34, y + 10, t, 28, J.TICK, "start", 1160))
    return g


def _flow_lit(i, key):
    x, y = FW["x"], fw_y(i)
    col = sc(key)
    return (F.rect(x + 14, y - 34, 1000, 68, J.BG2, col, 5, rx=12, op=1.0) + F.circ(x, y, 12, col)
            + _t(x + 40, y + 14, FW_V[i], 38, INK, "start", 950))


def flow8_stage(prev, st):
    s = []
    if _on(prev, st, "cut"):
        s.append(_flow_lit(FW["lit"][0], "company"))
    if _on(prev, st, "block"):
        s.append(_flow_lit(FW["lit"][1], "company"))
    if _on(prev, st, "report"):
        s.append(_flow_lit(FW["lit"][2], "kuni"))
    return s


# ══════════════════════════════════════════════════════════
#  clock2（c203）＝2つの時計：9月25日 9:07 検知 → 9月26日 7:25「までに」（針の向きは時刻の式）
# ══════════════════════════════════════════════════════════
CK = dict(a=(420.0, 470.0), b=(1500.0, 470.0), r=118.0)
CK_T = (("9月25日", 9, 7), ("9月26日", 7, 25))


def ck_angles(h, m):
    """(時針, 分針) の角度（度・12時が 0・時計回り）"""
    return (h % 12 + m / 60.0) * 30.0, m * 6.0


def _clock(cx, cy, r, h, m, col):
    g = [F.circ(cx, cy, r, J.BG2, col, 6, op=0.9)]
    for i in range(12):
        a = math.radians(i * 30.0)
        g.append(F.line(cx + (r - 18) * math.sin(a), cy - (r - 18) * math.cos(a), cx + (r - 6) * math.sin(a), cy - (r - 6) * math.cos(a), col, 4))
    ah, am = ck_angles(h, m)
    g.append(F.line(cx, cy, cx + r * 0.52 * math.sin(math.radians(ah)), cy - r * 0.52 * math.cos(math.radians(ah)), INK, 9))
    g.append(F.line(cx, cy, cx + r * 0.80 * math.sin(math.radians(am)), cy - r * 0.80 * math.cos(math.radians(am)), INK, 6))
    g.append(F.circ(cx, cy, 8, INK))
    return "".join(g)


def _clock_labels(cx, cy, r, day, h, m, what, col, what_cap=32):
    return (_t(cx, cy + r + 58, day, 36, INK, "middle", 400)
            + _t(cx, cy + r + 130, f"{h}:{m:02d}", 70, J.AMBER, "middle", 400)
            + _t(cx, cy + r + 188, what, what_cap, col, "middle", 620))


def clock2_base(st0):
    (x, y), r = CK["a"], CK["r"]
    d, h, m = CK_T[0]
    return [_clock(x, y, r, h, m, sc("company")), _clock_labels(x, y, r, d, h, m, "不正アクセスを検知", sc("company"))]


def clock2_stage(prev, st):
    s = []
    (xa, ya), (xb, yb), r = CK["a"], CK["b"], CK["r"]
    if _on(prev, st, "cut"):
        s.append(_arrow(xa + r + 30, ya, xb - r - 30, yb, sc("company"), 8, 30))
        s.append(_t(CX, ya - 34, "攻撃元との通信を遮断", 36, INK, "middle", 620))
        s.append(_t(CX, ya + 66, "入れないことの確認も完了", 36, INK, "middle", 620))
    if _on(prev, st, "done"):
        d, h, m = CK_T[1]
        s.append(_clock(xb, yb, r, h, m, sc("company")))
        s.append(_clock_labels(xb, yb, r, d, h, m, "この時刻「までに」", sc("company")))
        s.append(_tag(xb, yb - r - 44, "遅くとも", J.AMBER, 36, INK))
    return s


# ══════════════════════════════════════════════════════════
#  reports（c207）＝知らせの階段（左下から右上へ）：第1報「可能性」→ 第2報 約660万件 → 第3報 約160万件 → 第5報 調査の結果
# ══════════════════════════════════════════════════════════
RP = dict(xs=(290.0, 730.0, 1170.0, 1610.0), ys=(730.0, 610.0, 490.0, 370.0), w=400.0, h=170.0)
RP_V = (("第1報〈9月25日〉", (), "「可能性」"), ("第2報〈9月28日〉", (), "約660万件"),
        ("第3報〈9月29日〉", ("画像が漏えいしたアカウント",), "約160万件"), ("第5報〈10月23日〉", (), "調査の結果"))


def _rp_card(i):
    x, y, w, h = RP["xs"][i], RP["ys"][i], RP["w"], RP["h"]
    head, sub, big = RP_V[i]
    g = _panel(x - w / 2, y - h / 2, w, h, sc("company"), sw=5) + _t(x, y - h / 2 + 44, head, 30, sc("company"), "middle", w - 30)
    if sub:
        g += _t(x, y + 6, sub[0], 26, INK, "middle", w - 30) + _t(x, y + 62, big, 46, J.AMBER, "middle", w - 30)
    else:
        g += _t(x, y + 42, big, 54, J.AMBER, "middle", w - 30)
    return g


def _rp_arrow(i):
    return _arrow(RP["xs"][i] + RP["w"] / 2 - 40, RP["ys"][i] - RP["h"] / 2 - 8, RP["xs"][i + 1] - RP["w"] / 2 - 10, RP["ys"][i + 1] - 20, J.LINE, 6, 24)


def reports_base(st0):
    return []


def reports_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s += [_rp_card(0), _rp_arrow(0), _rp_card(1)]
    if _on(prev, st, "b"):
        s += [_rp_arrow(1), _rp_card(2), _rp_arrow(2), _rp_card(3)]
    return s


# ══════════════════════════════════════════════════════════
#  route3（c209）＝会社の説明の3段だけ（矢印だけ・手口の推測の絵は描かない）。②③は c210 の語り＝薄く置く
# ══════════════════════════════════════════════════════════
RT = dict(xs=(350.0, 960.0, 1570.0), y=480.0, w=500.0, h=230.0)
RT_V = (("①", "Webシステムの", "弱いところを突かれる"), ("②", "中の情報を", "探し回る"), ("③", "手に入れた情報で、", "データベースとファイルの置き場へ"))


def _rt_box(i, lit):
    x, y, w, h = RT["xs"][i], RT["y"], RT["w"], RT["h"]
    n, a, b = RT_V[i]
    if lit:
        return (_panel(x - w / 2, y - h / 2, w, h, sc("attacker"), sw=6, op=1.0) + _t(x, y - 40, n, 44, sc("attacker"), "middle", 100)
                + _t(x, y + 26, a, 36, INK, "middle", w - 40) + _t(x, y + 78, b, 36, INK, "middle", w - 40))
    return (_panel(x - w / 2, y - h / 2, w, h, J.LINE_DIM, sw=4, dash="14 10") + _t(x, y - 40, n, 40, J.TICK, "middle", 100)
            + _t(x, y + 26, a, 30, J.TICK, "middle", w - 40) + _t(x, y + 76, b, 30, J.TICK, "middle", w - 40))


def route3_base(st0):
    g = [_rt_box(i, False) for i in (1, 2)]     # ①は語りの頭で出す（薄い字の上に重ねない＝門番 layout）
    for i in range(2):
        g.append(_arrow(RT["xs"][i] + RT["w"] / 2 + 8, RT["y"], RT["xs"][i + 1] - RT["w"] / 2 - 8, RT["y"], J.LINE, 6, 24))
    return g


def route3_stage(prev, st):
    s = []
    if _on(prev, st, "one"):
        s.append(_rt_box(0, True))
    if _on(prev, st, "word"):
        s.append(_tag(CX, 730.0, "脆弱性（ぜいじゃくせい）＝攻撃に使える弱いところ", J.AMBER, 36, INK))
    return s


# ══════════════════════════════════════════════════════════
#  cal4w（c215）＝暦（日曜はじまり・5週）：9月25日〜10月23日＝28日。知らせ5回の日に印（曜日は日付の式）
# ══════════════════════════════════════════════════════════
CW = dict(x0=400.0, y0=338.0, w=150.0, h=96.0, d0=_dt.date(2026, 9, 20))
CW_S = (_dt.date(2026, 9, 25), _dt.date(2026, 10, 23))
CW_R = (("第1報", _dt.date(2026, 9, 25)), ("第2報", _dt.date(2026, 9, 28)), ("第3報", _dt.date(2026, 9, 29)),
        ("第4報", _dt.date(2026, 10, 16)), ("第5報", _dt.date(2026, 10, 23)))


def cw_rc(d):
    """日付 → (行, 列)。列は日曜 0。"""
    n = (d - CW["d0"]).days
    return n // 7, n % 7


def cw_xy(d):
    r, c = cw_rc(d)
    return CW["x0"] + c * CW["w"], CW["y0"] + r * CW["h"]


def _cw_label(d):
    return f"{d.month}月{d.day}日"


def cal4w_base(st0):
    x0, y0, w, h = CW["x0"], CW["y0"], CW["w"], CW["h"]
    g = [_t(x0 + (i + 0.5) * w, y0 - 14, t, 26, J.TICK, "middle", w) for i, t in enumerate("日月火水木金土")]
    for r in range(5):
        for c in range(7):
            g.append(F.rect(x0 + c * w, y0 + r * h, w, h, J.BG2, J.LINE_DIM, 2, op=0.55))
    for name, d in CW_R:
        x, y = cw_xy(d)
        g.append(F.rect(x + 4, y + 4, w - 8, h - 8, J.BG2, sc("company"), 4, rx=8))
        g.append(_t(x + w / 2, y + 40, _cw_label(d), 26, INK, "middle", w - 14))
        g.append(_t(x + w / 2, y + 76, name, 24, sc("company"), "middle", w - 14))
    g.append(_t(220.0, 590.0, "□＝知らせの日", 28, sc("company"), "middle", 330))
    return g


def cal4w_stage(prev, st):
    s = []
    w, h = CW["w"], CW["h"]
    a, b = CW_S
    if _on(prev, st, "start"):
        x, y = cw_xy(a)
        s.append(F.rect(x + 2, y + 2, w - 4, h - 4, "none", J.AMBER, 7, rx=8))
        s.append(_tag(220.0, 430.0, "気づいた日", J.AMBER, 34, INK))
    if _on(prev, st, "span"):
        x, y = cw_xy(b)
        s.append(F.rect(x + 2, y + 2, w - 4, h - 4, "none", J.AMBER, 7, rx=8))
        xr = CW["x0"] + 7 * w + 26
        ya, yb = cw_xy(a)[1] + h / 2, y + h / 2
        s.append(F.poly([(xr - 16, ya), (xr, ya), (xr, yb), (xr - 16, yb)], "none", J.AMBER, 6))
        s.append(_t(xr + 30, (ya + yb) / 2 - 8, "4週間", 56, J.AMBER, "start", 280))
        s.append(_t(xr + 30, (ya + yb) / 2 + 40, "（28日）", 32, J.AMBER, "start", 280))
    return s


# ══════════════════════════════════════════════════════════
#  第2章  six（c302）＝外へ送られた跡がある6つ（第5報 ① の言葉）
# ══════════════════════════════════════════════════════════
SX = dict(xs=(400.0, 960.0, 1520.0), ys=(345.0, 480.0), w=500.0, h=110.0)      # 2行目は地 CM051 の看板の字（y526〜552）の上に載せない＝門番 slide G-14
SX_V = ("氏名", "住所", "生年月日", "電話番号", "メールアドレス", "運転免許情報")


def six_base(st0):
    return []


def six_stage(prev, st):
    s = []
    if _on(prev, st, "all"):
        for i, t in enumerate(SX_V):
            x, y = SX["xs"][i % 3], SX["ys"][i // 3]
            s.append(_panel(x - SX["w"] / 2, y - SX["h"] / 2, SX["w"], SX["h"], J.ALERT if i == 5 else sc("member"), sw=5))
            s.append(_t(x, y + 16, t, 44, INK, "middle", SX["w"] - 40))
    if _on(prev, st, "out"):
        s.append(_arrow(CX, 546.0, CX, 650.0, J.ALERT, 8, 30))
        s.append(_tag(CX, 700.0, "アクセス＋外へ送られた跡", J.ALERT, 40, INK))
    return s


# ══════════════════════════════════════════════════════════
#  bars2（c305）＝縦の棒2本（高さは数に比例・0から）：9月 約160万〈アカウント〉／10月 146万4800＋89万1602〈画像〉。「減った」と読ませない札
# ══════════════════════════════════════════════════════════
BR = dict(y0=790.0, k=0.00019, xl=360.0, xr=1120.0, w=240.0)
BR_V = (1600000, 1464800, 891602)


def br_y(v):
    return BR["y0"] - v * BR["k"]


def bars2_base(st0):
    return [F.line(240.0, BR["y0"], 1500.0, BR["y0"], J.LINE, 5)]


def bars2_stage(prev, st):
    s = []
    y0 = BR["y0"]
    a, b, c = BR_V
    if _on(prev, st, "left"):
        x, w = BR["xl"], BR["w"]
        s.append(F.rect(x, br_y(a), w, y0 - br_y(a), J.LINE, None, None, rx=6))
        s.append(_t(x + w / 2, br_y(a) - 22, "約160万件", 56, J.AMBER, "middle", 460))
        s.append(_t(x + w / 2, y0 + 48, "9月の第3報：アカウントの数", 28, INK, "middle", 520))
    if _on(prev, st, "right"):
        x, w = BR["xr"], BR["w"]
        s.append(F.rect(x, br_y(b), w, y0 - br_y(b), J.ALERT, None, None, rx=6))
        s.append(F.rect(x, br_y(b + c), w, br_y(b) - br_y(b + c), J.ALERT, J.ALERT, 3, rx=6, op=0.28, dash="10 8"))
        s.append(_t(x + w + 30, (y0 + br_y(b)) / 2 - 20, "外へ送られた跡", 30, INK, "start", 400))
        s.append(_t(x + w + 30, (y0 + br_y(b)) / 2 + 40, "146万4800件", 54, J.AMBER, "start", 400))
        s.append(_t(x + w + 30, (br_y(b) + br_y(b + c)) / 2 - 12, "アクセスだけ", 28, J.TICK, "start", 400))
        s.append(_t(x + w + 30, (br_y(b) + br_y(b + c)) / 2 + 32, "89万1602件", 36, J.TICK, "start", 400))
        s.append(_t(x + w / 2, y0 + 48, "10月の第5報：画像の数", 28, INK, "middle", 520))
        s.append(_panel(650.0, 400.0, 420.0, 130.0, J.AMBER, sw=5))
        s.append(_t(860.0, 452.0, "数えたものが違う", 36, J.AMBER, "middle", 390))
        s.append(_t(860.0, 504.0, "アカウント／画像", 30, INK, "middle", 390))
    return s


# ══════════════════════════════════════════════════════════
#  words2（c308）＝会社の言葉を2つ並べる（第5報 ※3＝いま／この先）
# ══════════════════════════════════════════════════════════
WD_A = ("直ちに画像内容が閲覧可能な", "状態になったことを意味する", "ものではありません")
WD_B = ("将来的な復号の可能性を", "完全に否定できる", "ものではありません")
WD = dict(xs=(490.0, 1430.0), y=560.0, w=830.0, h=400.0)


def _wd_card(i, head, lines):
    return _quote_card(WD["xs"][i], WD["y"], WD["w"], WD["h"], lines, sc("company"), 44, head, "会社の言葉（第5報 ※3）")


def words2_base(st0):
    return []


def words2_stage(prev, st):
    s = []
    if _on(prev, st, "now"):
        s.append(_wd_card(0, "いま", WD_A))
    if _on(prev, st, "next"):
        s.append(_wd_card(1, "この先", WD_B))
    return s


# ══════════════════════════════════════════════════════════
#  club（c311）＝もう1つのシステム（第5報 ⑥・※4 の主な3項目）
# ══════════════════════════════════════════════════════════
CB = dict(x=640.0, y=300.0, w=1180.0, h=520.0, ys=(470.0, 590.0, 710.0))
CB_V = (("氏名・住所・生年月日・運転免許情報", "5件"), ("タイムズクラブカードの番号", "1万9510件"), ("ほかの会社のサービスとつなぐ番号", "13万5436件"))


def club_base(st0):
    return []


def club_stage(prev, st):
    s = []
    x, y, w, h = CB["x"], CB["y"], CB["w"], CB["h"]
    if _on(prev, st, "box"):
        s.append(_panel(x, y, w, h, sc("company"), sw=6))
        s.append(_t(x + w / 2, y + 52, "タイムズクラブWebシステム", 42, sc("company"), "middle", w - 60))
        s.append(_t(x + w / 2, y + 94, "送られた跡の数", 28, J.TICK, "middle", w - 60))
    if _on(prev, st, "hit"):
        s.append(_arrow(170.0, 560.0, x - 16, 560.0, sc("attacker"), 8, 30))
        s.append(_t(370.0, 530.0, "不正アクセス", 34, sc("attacker"), "middle", 420))
    if _on(prev, st, "rows"):
        for (lab, v), yy in zip(CB_V, CB["ys"]):
            s.append(F.line(x + 40, yy - 58, x + w - 40, yy - 58, J.LINE_DIM, 3))
            s.append(_t(x + 50, yy + 14, lab, 32, INK, "start", 700))
            s.append(_t(x + w - 50, yy + 20, v, 56, J.AMBER, "end", 380))
    return s


# ══════════════════════════════════════════════════════════
#  ccard（c312）＝札：カードの絵（桁は描かない＝●）・「一切保持していない」・下4桁 28件〈タイムズクラブ側〉
# ══════════════════════════════════════════════════════════
CC = dict(x=120.0, y=340.0, w=680.0, h=410.0, gx=(200.0, 345.0, 490.0, 635.0))
CC_Q = "一切保持していない"
CC_N = "28件"


def ccard_base(st0):
    x, y, w, h = CC["x"], CC["y"], CC["w"], CC["h"]
    g = [F.rect(x, y, w, h, J.BG2, J.LINE, 6, rx=26, op=0.92), F.rect(x, y + 56, w, 62, J.LINE_DIM, None, None),
         F.rect(x + 50, y + 156, 96, 66, "none", J.LINE, 4, rx=10)]
    for gx in CC["gx"]:
        g.append(_t(gx, y + 300, "●●●●", 34, J.LINE, "start", 130))
    g.append(_t(x + 50, y + 370, "カードの番号（絵）", 28, J.TICK, "start", 500))
    return g


def ccard_stage(prev, st):
    s = []
    if _on(prev, st, "keep"):
        s.append(_panel(880.0, 340.0, 920.0, 200.0, sc("company"), sw=5))
        s.append(_t(1340.0, 398.0, "番号の全部の桁・セキュリティコード", 34, INK, "middle", 860))
        s.append(_t(1340.0, 482.0, CC_Q, 60, sc("company"), "middle", 860))
    if _on(prev, st, "leak"):
        gx = CC["gx"][3]
        y = CC["y"]
        s.append(F.rect(gx - 12, y + 262, 142, 56, "none", J.AMBER, 6, rx=8))
        s.append(_arrow(gx + 136, y + 262, 880.0, 660.0, J.AMBER, 6, 24))
        s.append(_panel(880.0, 570.0, 920.0, 200.0, J.AMBER, sw=5))
        s.append(_t(1340.0, 628.0, "番号の下4桁（タイムズクラブ側）", 34, INK, "middle", 860))
        s.append(_t(1340.0, 716.0, CC_N, 72, J.AMBER, "middle", 860))
    return s


# ══════════════════════════════════════════════════════════
#  fixn（c314）＝直された数：第2報 WESTER ID 等（計9件）→ 第5報 タイムズカー側のつなぐ番号 4件・WESTER ID は 0件
# ══════════════════════════════════════════════════════════
FX_V = dict(old="計9件", new="4件", wester="0件")


def fixn_base(st0):
    return []


def fixn_stage(prev, st):
    s = []
    if _on(prev, st, "old"):
        s.append(_panel(100.0, 320.0, 700.0, 460.0, sc("company"), sw=5))
        s.append(_t(450.0, 386.0, "9月の第2報", 36, sc("company"), "middle", 640))
    if _on(prev, st, "wester"):
        s.append(_t(450.0, 480.0, "WESTER ID など", 44, INK, "middle", 640))
        s.append(_t(450.0, 548.0, "（JR西日本のID）", 28, J.TICK, "middle", 640))
        s.append(_t(450.0, 684.0, FX_V["old"], 84, J.AMBER, "middle", 640))
    if _on(prev, st, "new"):
        s.append(_arrow(816.0, 550.0, 952.0, 550.0, J.LINE, 8, 30))
        s.append(_panel(970.0, 320.0, 850.0, 460.0, sc("company"), sw=5))
        s.append(_t(1395.0, 386.0, "10月の第5報", 36, sc("company"), "middle", 790))
        s.append(_t(1010.0, 500.0, "WESTER ID", 40, INK, "start", 480))
        s.append(_t(1780.0, 516.0, FX_V["wester"], 96, J.ALERT, "end", 280))
        s.append(F.line(1010.0, 572.0, 1780.0, 572.0, J.LINE_DIM, 3))
        s.append(_t(1010.0, 660.0, "タイムズカー側のつなぐ番号", 36, INK, "start", 520))
        s.append(_t(1780.0, 676.0, FX_V["new"], 72, J.AMBER, "end", 240))
    return s


# ══════════════════════════════════════════════════════════
#  第3章  unit2（c402）＝横の棒2本（長さは数に比例・0から）：会員 400万人あまり／漏えいの件数 662万件あまり。単位が違う札（差を「会員でない人」と描かない）
# ══════════════════════════════════════════════════════════
UT = dict(x0=470.0, k=1.75, ys=(420.0, 620.0), h=84.0)
UT_V = (400.0, 662.8007)


def ut_x(v):
    return UT["x0"] + v * UT["k"]


def unit2_base(st0):
    x0, h = UT["x0"], UT["h"]
    g = [F.line(x0, 330.0, x0, 700.0, J.LINE, 5)]
    for (lab, sub, col, v, t), y in zip((("会員", "8月の発表", sc("member"), UT_V[0], "400万人あまり"), ("漏えいの件数", "最終の件数", J.ALERT, UT_V[1], "662万件あまり")), UT["ys"]):
        g.append(_t(x0 - 26, y + 2, lab, 38, INK, "end", 380))
        g.append(_t(x0 - 26, y + 44, sub, 26, J.TICK, "end", 380))
        g.append(F.rect(x0, y - h / 2, ut_x(v) - x0, h, col, None, None, rx=6))
        g.append(_t(x0 + 6, y - h / 2 - 16, t, 44, J.AMBER, "start", 700))
    return g


def unit2_stage(prev, st):
    s = []
    if _on(prev, st, "unit"):
        s.append(_tag(640.0, 780.0, "人の数 ≠ アカウントの数", J.AMBER, 36, INK))
    if _on(prev, st, "former"):
        s.append(_tag(1340.0, 780.0, "いまは会員でない人の分も", sc("member"), 36, INK))
    return s


# ══════════════════════════════════════════════════════════
#  inside（c403）＝662万件の中の4つの箱（割合は公表なし＝同じ大きさに描いて札で断る）
# ══════════════════════════════════════════════════════════
IN = dict(x=300.0, y=290.0, w=1320.0, h=540.0, xs=(650.0, 1270.0), ys=(490.0, 690.0), bw=520.0, bh=120.0)


def _in_box(i, a, b=None):
    x, y = IN["xs"][i % 2], IN["ys"][i // 2]
    g = _panel(x - IN["bw"] / 2, y - IN["bh"] / 2, IN["bw"], IN["bh"], sc("member"), sw=5)
    if b:
        return g + _t(x, y - 6, a, 46, INK, "middle", IN["bw"] - 40) + _t(x, y + 42, b, 28, J.TICK, "middle", IN["bw"] - 40)
    return g + _t(x, y + 19, a, 54, INK, "middle", IN["bw"] - 30)


def inside_base(st0):
    x, y, w, h = IN["x"], IN["y"], IN["w"], IN["h"]
    return [_panel(x, y, w, h, J.LINE, sw=4, op=0.55),
            _t(x + w / 2, y + 66, "662万件の中（割合は公表されていない）", 38, J.AMBER, "middle", w - 60),
            _in_box(0, "今の会員")]


def inside_stage(prev, st):
    s = []
    if _on(prev, st, "two"):
        s += [_in_box(1, "退会した人"), _in_box(2, "入会が済まなかった人")]
    if _on(prev, st, "park"):
        s.append(_in_box(3, "駐車場だけの契約", "（会社向けの入会）"))
    return s


# ══════════════════════════════════════════════════════════
#  purpose4（c405）＝真ん中の画像から4方向（第4報の言葉＝会員ご登録時の本人確認・不正利用が疑われる事案・お問い合わせ対応・各種ご本人確認業務）
# ══════════════════════════════════════════════════════════
PU = dict(c=(960.0, 540.0), xs=(420.0, 1500.0), ys=(390.0, 690.0), w=720.0, h=130.0)
PU_V = ("会員登録時の本人確認手続き", "不正利用が疑われる事案への対応", "お問い合わせ対応", "各種の本人確認業務")


def _pu_box(i):
    x, y = PU["xs"][i % 2], PU["ys"][i // 2]
    cx, cy = PU["c"]
    ex = x + PU["w"] / 2 + 10 if x < cx else x - PU["w"] / 2 - 10
    return (_arrow(cx + (-110 if x < cx else 110), cy + (-50 if y < cy else 50), ex, y, sc("company"), 6, 24)
            + _panel(x - PU["w"] / 2, y - PU["h"] / 2, PU["w"], PU["h"], sc("company"), sw=5)
            + _t(x, y + 14, PU_V[i], 38, INK, "middle", PU["w"] - 40))


def purpose4_base(st0):
    cx, cy = PU["c"]
    return [_idcard(cx, cy - 16, 1.0, J.AMBER), _t(cx, cy + 90, "画像", 34, J.AMBER, "middle", 200)]


def purpose4_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_pu_box(0))
    if _on(prev, st, "b"):
        s.append(_pu_box(1))
    if _on(prev, st, "c"):
        s += [_pu_box(2), _pu_box(3)]
    return s


# ══════════════════════════════════════════════════════════
#  qa7（c407）＝問答：Q7 の答えを組み直した札（会社の字のまま）
# ══════════════════════════════════════════════════════════
Q7_A = ("運転免許情報および画像は、", "なりすまし対策やお問い合わせ対応のため、", "7年間保管していました")


def qa7_base(st0):
    return []


def qa7_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_tag(CX, 320.0, "Q 退会後も保管していた理由", sc("member"), 36, INK))
    if _on(prev, st, "a"):
        s.append(_quote_card(CX, 560.0, 1500.0, 360.0, Q7_A, sc("company"), 50, "ご質問と回答 Q7"))
    if _on(prev, st, "yr"):
        s.append(F.line(640.0, 684.0, 1280.0, 684.0, J.AMBER, 6))
        s.append(_tag(CX, 790.0, "退会してから7年間", J.AMBER, 34, INK))
    return s


# ══════════════════════════════════════════════════════════
#  law22（c409）＝条文：個人情報の保護に関する法律 第22条の後半（e-Gov の字のまま）
# ══════════════════════════════════════════════════════════
L22 = ("利用する必要がなくなったときは、", "当該個人データを遅滞なく消去するよう", "努めなければならない。")


def law22_base(st0):
    return []


def law22_stage(prev, st):
    s = []
    if _on(prev, st, "head"):
        s.append(_panel(220.0, 300.0, 1480.0, 480.0, sc("kuni"), sw=5))
        s.append(_t(CX, 376.0, "個人情報の保護に関する法律 第22条（後半）", 38, sc("kuni"), "middle", 1400))
        s.append(F.line(280.0, 412.0, 1640.0, 412.0, J.LINE_DIM, 3))
    if _on(prev, st, "text"):
        # 地 CM051 の看板の字（y526〜552）の高さに行を載せない＝門番 slide G-14
        s.append(_lines(CX, 510.0, L22[:2], 50, INK, "middle", 1400, 98.0))
        s.append(_t(CX, 700.0, L22[2], 64, J.AMBER, "middle", 1400))
        s.append(F.line(600.0, 722.0, 1320.0, 722.0, J.AMBER, 6))
    return s


# ══════════════════════════════════════════════════════════
#  rule_oct（c414）＝年表（位置は日に比例）＋ 第5報の「現行→変更後」の表
# ══════════════════════════════════════════════════════════
RO = dict(x0=230.0, x1=1630.0, y=370.0, d0=_dt.date(2026, 9, 25), d1=_dt.date(2026, 10, 31))
RO_D = ((_dt.date(2026, 9, 25), "9月25日", "検知"), (_dt.date(2026, 10, 16), "10月16日", "決まりを改める"), (_dt.date(2026, 10, 31), "10月末", "今ある画像を消す〈予定〉"))
RO_R = (("今の会員", "会員の間は保有", "登録確認完了後、即時削除"), ("退会した人", "退会後7年間保有", "保有しない"))


def ro_x(d):
    return RO["x0"] + (d - RO["d0"]).days * (RO["x1"] - RO["x0"]) / (RO["d1"] - RO["d0"]).days


def rule_oct_base(st0):
    y = RO["y"]
    g = [F.line(RO["x0"], y, RO["x1"], y, J.LINE, 6)]
    for i, (d, day, what) in enumerate(RO_D):
        x = ro_x(d)
        col = sc("company") if i == 1 else J.LINE
        g.append(F.circ(x, y, 14, col))
        anc = "end" if i == 2 else ("start" if i == 0 else "middle")
        ax = x + 60 if i == 2 else (x - 60 if i == 0 else x)
        g.append(_t(ax, y - 34, day, 40, J.AMBER, anc, 460))
        g.append(_t(ax, y + 60, what, 32, INK if i == 1 else J.TICK, anc, 560))
    for x, t in ((720.0, "いままで"), (1320.0, "変えたあと")):
        g.append(_t(x, 520.0, t, 30, J.TICK, "middle", 500))
    return g


def _ro_row(i, y):
    who, a, b = RO_R[i]
    return (_panel(180.0, y - 50, 1560.0, 100.0, sc("member"), sw=4)
            + _t(310.0, y + 14, who, 36, sc("member"), "middle", 240)
            + _t(720.0, y + 14, a, 34, J.TICK, "middle", 500)
            + _arrow(990.0, y, 1040.0, y, J.LINE, 6, 22)
            + _t(1370.0, y + 14, b, 38, INK, "middle", 620))


def rule_oct_stage(prev, st):
    s = []
    if _on(prev, st, "now"):
        s.append(_ro_row(0, 590.0))
    if _on(prev, st, "left"):
        s.append(_ro_row(1, 710.0))
        s.append(_t(CX, 812.0, "消し終えたという知らせは見当たらない（10月31日の時点）", 28, J.AMBER, "middle", 1300))
    return s


# ══════════════════════════════════════════════════════════
#  bank2（c420）＝スマホで口座を開くときの確認：画像 → みずほ銀行 ICチップ／三井住友銀行 画像の受付を停止
# ══════════════════════════════════════════════════════════
BK = dict(ys=(420.0, 680.0))


def bank2_base(st0):
    return [_phone(290.0, 500.0, 1.1, J.LINE), _idcard(290.0, 500.0, 0.26, J.LINE),
            _t(290.0, 625.0, "画像を送って", 34, INK, "middle", 400), _t(290.0, 672.0, "確かめる方法", 34, INK, "middle", 400)]


def _bank_tag(y, name):
    return _arrow(470.0, 550.0 if y > 550 else 450.0, 560.0, y, J.LINE, 6, 22) + _tag(740.0, y, name, sc("bank"), 40, INK, w=340.0)


def bank2_stage(prev, st):
    s = []
    y1, y2 = BK["ys"]
    if _on(prev, st, "mz"):
        s.append(_bank_tag(y1, "みずほ銀行"))
    if _on(prev, st, "ic"):
        s.append(_arrow(922.0, y1, 1010.0, y1, sc("bank"), 8, 28))
        s.append(_panel(1030.0, y1 - 90, 790.0, 180.0, sc("bank"), sw=5))
        s.append(_t(1425.0, y1 - 12, "マイナンバーカード", 44, INK, "middle", 740))
        s.append(_t(1425.0, y1 + 48, "ICチップの読み取りへ", 38, sc("bank"), "middle", 740))
    if _on(prev, st, "smbc"):
        s.append(_bank_tag(y2, "三井住友銀行"))
        s.append(_arrow(922.0, y2, 1010.0, y2, sc("bank"), 8, 28))
        s.append(_panel(1030.0, y2 - 90, 790.0, 180.0, J.ALERT, sw=5))
        s.append(_t(1425.0, y2 - 12, "10月23日から", 40, J.AMBER, "middle", 740))
        s.append(_t(1425.0, y2 + 48, "画像の受付を停止", 42, INK, "middle", 740))
    return s


# ══════════════════════════════════════════════════════════
#  第4章  risk4（c501）＝会社が挙げた4つのおそれ（第5報の字のまま・人は描かない）
# ══════════════════════════════════════════════════════════
RK = dict(xs=(530.0, 1390.0), ys=(450.0, 660.0), w=780.0, h=160.0)
RK_V = (("フィッシングメールや", "フィッシングサイトによる詐欺"), ("なりすましによる", "各種申込みや問い合わせ"), ("不正勧誘",), ("個人情報の悪用",))


def _rk_card(i):
    x, y, w, h = RK["xs"][i % 2], RK["ys"][i // 2], RK["w"], RK["h"]
    ic = (_mail, _idcard, _bubble_icon, _warn)[i]
    tx = x - w / 2 + 170
    g = _panel(x - w / 2, y - h / 2, w, h, J.ALERT, sw=5) + ic(x - w / 2 + 88, y, 0.72 if i == 1 else 1.0, J.ALERT)
    lines = RK_V[i]
    if len(lines) == 2:
        return g + _t(tx, y - 10, lines[0], 38, INK, "start", w - 190) + _t(tx, y + 48, lines[1], 38, INK, "start", w - 190)
    return g + _t(x + 70, y + 26, lines[0], 72, INK, "middle", w - 190)     # 短い言葉は大きく（札の余白＝門番 box）


def risk4_base(st0):
    return []


def risk4_stage(prev, st):
    s = []
    if _on(prev, st, "head"):
        s.append(_tag(CX, 300.0, "想定されるリスク（会社の言葉）", sc("company"), 36, INK))
    if _on(prev, st, "a"):
        s += [_rk_card(0), _rk_card(1)]
    if _on(prev, st, "b"):
        s += [_rk_card(2), _rk_card(3)]
    return s


# ══════════════════════════════════════════════════════════
#  law_kyc（c504）＝条文：犯罪収益移転防止法の施行規則の改正・附則（e-Gov の字のまま）
# ══════════════════════════════════════════════════════════
KY_Q = "この命令は、令和九年四月一日から施行する。"


def law_kyc_base(st0):
    return []


def law_kyc_stage(prev, st):
    s = []
    if _on(prev, st, "kuni"):
        s.append(_tag(320.0, 320.0, "国の決まり", sc("kuni"), 36, INK))
    if _on(prev, st, "law"):
        s.append(_panel(120.0, 400.0, 720.0, 220.0, sc("kuni"), sw=5))
        s.append(_t(480.0, 490.0, "犯罪収益移転防止法", 50, INK, "middle", 680))
        s.append(_t(480.0, 560.0, "本人確認を定める法律", 32, J.TICK, "middle", 680))
    if _on(prev, st, "rule"):
        s.append(_arrow(856.0, 510.0, 980.0, 510.0, sc("kuni"), 8, 30))
        s.append(_panel(1000.0, 400.0, 820.0, 220.0, J.AMBER, sw=5))
        s.append(_t(1410.0, 478.0, "施行規則の改正", 44, J.AMBER, "middle", 780))
        s.append(_t(1410.0, 556.0, "画像を送る確認をやめる", 42, INK, "middle", 780))
        s.append(_quote_card(CX, 740.0, 1500.0, 160.0, (KY_Q,), sc("kuni"), 40, None, "附則（令和九年＝2027年）"))
    return s


# ══════════════════════════════════════════════════════════
#  fsa_check（c507）＝金融庁の注意喚起（記の1）：金融機関などへ → 対策の点検（タイムズカーの名は無い）
# ══════════════════════════════════════════════════════════
FS_Q = ("「サードパーティリスク管理やインシデントが", "起きた場合の対応態勢も含めた」")


def fsa_check_base(st0):
    return [_tag(390.0, 400.0, "金融庁", sc("kuni"), 46, INK, w=320.0, h=110.0),
            _arrow(570.0, 400.0, 1180.0, 400.0, sc("kuni"), 8, 30),
            _t(860.0, 372.0, "2026年10月9日の注意喚起", 32, sc("kuni"), "middle", 580),
            _tag(1430.0, 400.0, "金融機関など", sc("bank"), 46, INK, w=460.0, h=110.0)]


def fsa_check_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_quote_card(CX, 610.0, 1500.0, 210.0, FS_Q, sc("kuni"), 42))
        s.append(_t(CX, 762.0, "対策の点検を促す", 44, J.AMBER, "middle", 900))
        s.append(_t(CX, 826.0, "サードパーティ＝外部の取引先など", 28, J.TICK, "middle", 900))
    return s


# ══════════════════════════════════════════════════════════
#  jicc5（c512）＝5日の帯：JICC のアプリの受付（10月1日 一時休止「お申込みの集中」→ 2日 再開 → 夜から4日まで止める〈サーバーのメンテナンス〉→ 5日 再開）
# ══════════════════════════════════════════════════════════
JC = dict(x0=270.0, w=280.0, y=500.0, h=86.0)
JC_D = ("10月1日", "2日", "3日", "4日", "5日")
# (始めの日・終わりの日・止まっているか)。日の中の時刻は描かない＝2日の境は「夜から」の目安
JC_S = ((0.0, 1.0, True), (1.0, 1.72, False), (1.72, 4.0, True), (4.0, 5.0, False))
JC_R = "「お申込みの集中」"


def jc_x(d):
    return JC["x0"] + d * JC["w"]


def jicc5_base(st0):
    y = JC["y"]
    g = []
    for i, t in enumerate(JC_D):
        g.append(_t(jc_x(i) + JC["w"] / 2, y - 66, t, 36, J.AMBER, "middle", JC["w"] - 10))
        g.append(F.line(jc_x(i), y - 50, jc_x(i), y + JC["h"] / 2 + 12, J.LINE_DIM, 3))
    g.append(F.line(jc_x(5), y - 50, jc_x(5), y + JC["h"] / 2 + 12, J.LINE_DIM, 3))
    return g


def jicc5_stage(prev, st):
    s = []
    y, h = JC["y"], JC["h"]
    if _on(prev, st, "who"):
        s.append(_tag(620.0, 320.0, "JICC（信用情報機関）のアプリの受付", sc("jicc"), 36, INK))
    if _on(prev, st, "bar"):
        for a, b, stop in JC_S:
            col = J.ALERT if stop else sc("jicc")
            s.append(F.rect(jc_x(a) + 2, y - h / 2, jc_x(b) - jc_x(a) - 4, h, col, None, None, rx=8))
        s.append(_t((jc_x(0) + jc_x(1)) / 2, y + 12, "一時休止", 34, INK, "middle", 260))
        s.append(_t((jc_x(1) + jc_x(1.72)) / 2, y + 12, "再開", 34, INK, "middle", 190))
        s.append(_t((jc_x(1.72) + jc_x(4)) / 2, y + 12, "止める", 34, INK, "middle", 400))
        s.append(_t((jc_x(4) + jc_x(5)) / 2, y + 12, "再開", 34, INK, "middle", 260))
        s.append(_t((jc_x(0) + jc_x(1)) / 2, y + 112, JC_R, 34, J.AMBER, "middle", 320))
        s.append(_t((jc_x(0) + jc_x(1)) / 2, y + 158, "この日の理由", 26, J.TICK, "middle", 280))
        s.append(_t((jc_x(1.72) + jc_x(4)) / 2, y + 112, "サーバーのメンテナンス", 34, INK, "middle", 620))
        s.append(_t(CX, 802.0, "告知にタイムズカーの名は無い", 30, J.TICK, "middle", 900))
    return s


# ══════════════════════════════════════════════════════════
#  qa12（c513）＝問答：Q12 の2つの答え（会社の字のまま）
# ══════════════════════════════════════════════════════════
Q12_A = ("信用情報機関が悪用の防止効果を", "保証するものではありません")
Q12_B = ("預金口座の開設時には", "利用されません")


def qa12_base(st0):
    return []


def qa12_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_tag(CX, 320.0, "Q 信用情報機関への届け出（本人申告）", sc("jicc"), 36, INK))
    if _on(prev, st, "a"):
        s.append(_quote_card(CX, 500.0, 1200.0, 210.0, Q12_A, sc("company"), 54))
        s.append(_t(290.0, 522.0, "A", 64, sc("company"), "middle", 90))
    if _on(prev, st, "b"):
        s.append(_quote_card(CX, 730.0, 1200.0, 210.0, Q12_B, sc("company"), 54))
        s.append(_t(290.0, 752.0, "A", 64, sc("company"), "middle", 90))
    return s


# ══════════════════════════════════════════════════════════
#  第5章  cutoff（c603）＝見舞金の対象の線引き（線の外の人を「切り捨て」と言う弁護士の言葉＝出どころつき）
# ══════════════════════════════════════════════════════════
CO_Q = "完全に切り捨てられている"


def cutoff_base(st0):
    return []


def cutoff_stage(prev, st):
    s = []
    if _on(prev, st, "line"):
        s.append(_panel(140.0, 300.0, 760.0, 300.0, sc("company"), sw=6))
        s.append(_t(520.0, 374.0, "見舞金の対象", 44, sc("company"), "middle", 700))
        s.append(_t(520.0, 464.0, "画像：外へ送られた跡あり", 38, INK, "middle", 700))
        s.append(_t(520.0, 546.0, "（第5報）", 28, J.TICK, "middle", 700))
        s.append(_panel(1020.0, 300.0, 760.0, 300.0, J.LINE_DIM, sw=4, dash="14 10"))
        s.append(_t(1400.0, 374.0, "対象の外", 44, J.ALERT, "middle", 700))
        s.append(_t(1400.0, 464.0, "名前などだけ", 38, INK, "middle", 700))
        s.append(_t(1400.0, 532.0, "画像はアクセスだけ", 38, INK, "middle", 700))
    if _on(prev, st, "say"):
        s.append(_quote_card(CX, 730.0, 1300.0, 190.0, (f"「{CO_Q}」",), sc("lawyer"), 60, None, "弁護士（2026年10月26日の報道）"))
    return s


# ══════════════════════════════════════════════════════════
#  formula（c604）＝式：146万4800件 × 3000円 ＝ 約44億円（計算＝会社は総額を言っていない・積は式で）
# ══════════════════════════════════════════════════════════
FM_A, FM_B = 1464800, 3000
FM = dict(y=570.0)


def fm_oku():
    """積（億円）の丸め。"""
    return round(FM_A * FM_B / 1e8)


def formula_base(st0):
    return []


def formula_stage(prev, st):
    s = []
    y = FM["y"]
    if _on(prev, st, "none"):
        s.append(_tag(CX, 340.0, "会社の総額：示されていない（10月31日の時点）", sc("company"), 36, INK))
    if _on(prev, st, "calc"):
        s.append(_t(470.0, y, "146万4800件", 88, J.AMBER, "middle", 720))
        s.append(_t(470.0, y + 66, "画像の件数", 32, J.TICK, "middle", 700))
        s.append(_t(888.0, y, "×", 76, INK, "middle", 80))
        s.append(_t(1100.0, y, "3000円", 88, J.AMBER, "middle", 330))
        s.append(_t(1100.0, y + 66, "見舞金", 32, J.TICK, "middle", 330))
        s.append(_t(1310.0, y, "＝", 76, INK, "middle", 80))
        s.append(_t(1600.0, y, f"約{fm_oku()}億円", 96, J.ALERT, "middle", 460))
        s.append(_tag(1600.0, y + 96, "計算", J.ALERT, 32, INK))
    return s


# ══════════════════════════════════════════════════════════
#  profit（c607）＝縦の棒2本（高さは億円に比例・0から）：最終的なもうけの予想 440億円 → 385億円〈12.5%減〉・売上高の予想 4110億円は据え置き
# ══════════════════════════════════════════════════════════
PF = dict(y0=800.0, k=1.0, xs=(560.0, 980.0), w=220.0)
PF_V = (440, 385)
PF_M = (44000, 38500, 411000)


def pf_y(v):
    return PF["y0"] - v * PF["k"]


def profit_base(st0):
    return [F.line(460.0, PF["y0"], 1300.0, PF["y0"], J.LINE, 5),
            _lines(250.0, 400.0, ("2026年10月期", "最終的なもうけの", "予想"), 32, INK, "middle", 340, 48.0)]


def profit_stage(prev, st):
    s = []
    if _on(prev, st, "bars"):
        for x, v, cap, col, under in zip(PF["xs"], PF_V, ("440億円", "385億円"), (J.LINE, J.ALERT), ("前の予想", "10月23日の予想")):
            s.append(F.rect(x, pf_y(v), PF["w"], PF["y0"] - pf_y(v), col, None, None, rx=6))
            s.append(_t(x + PF["w"] / 2, pf_y(v) - 20, cap, 52, J.AMBER, "middle", 400))
            s.append(_t(x + PF["w"] / 2, PF["y0"] + 44, under, 28, INK, "middle", 400))
        s.append(_arrow(PF["xs"][0] + PF["w"] + 20, 500.0, PF["xs"][1] - 20, 500.0, J.LINE, 8, 28))
    if _on(prev, st, "pct"):
        s.append(_t(1500.0, 500.0, "12.5%減", 84, J.ALERT, "middle", 560))
        s.append(_t(1500.0, 690.0, "売上高の予想", 30, J.TICK, "middle", 560))
        s.append(_t(1500.0, 738.0, "4110億円は据え置き", 34, J.TICK, "middle", 560))
    return s


# ══════════════════════════════════════════════════════════
#  damages（c610）＝横の棒3本（長さは円に比例・0から）：慰謝料 3万円・画像 5万円・見舞金 3000円
# ══════════════════════════════════════════════════════════
DM = dict(x0=610.0, k=0.021, h=84.0, ys=(360.0, 500.0, 640.0))
DM_V = ((30000, "3万円", "求める慰謝料（1人）", "lawyer"), (50000, "5万円", "画像が漏えいした人", "lawyer"), (3000, "3000円", "見舞金（会社）", "company"))


def dm_x(v):
    return DM["x0"] + v * DM["k"]


def damages_base(st0):
    return [F.line(DM["x0"], 310.0, DM["x0"], 690.0, J.LINE, 5)]


def _dm_row(i):
    v, cap, lab, who = DM_V[i]
    y, h = DM["ys"][i], DM["h"]
    return (F.rect(DM["x0"], y - h / 2, dm_x(v) - DM["x0"], h, sc(who), None, None, rx=6)
            + _t(DM["x0"] - 24, y + 14, lab, 36, INK, "end", 500)
            + _t(dm_x(v) + 24, y + 22, cap, 64, J.AMBER, "start", 280))


def damages_stage(prev, st):
    s = []
    if _on(prev, st, "two"):
        s += [_dm_row(0), _dm_row(1)]
        # 地 CM047 の看板の字（y799〜812）の上に載せない＝門番 slide G-14
        s.append(_t(CX, 744.0, "目安：過去の漏えいの裁判の約3万円", 30, J.TICK, "middle", 1100))
        s.append(_t(CX, 790.0, "ほかに信用情報機関への申告や再交付の手数料も", 28, J.TICK, "middle", 1100))
    if _on(prev, st, "gift"):
        s.append(_dm_row(2))
    return s


# ══════════════════════════════════════════════════════════
#  quote3000（c612）＝弁護士の言葉の札（記事の字のまま）
# ══════════════════════════════════════════════════════════
LW_Q = ("「3000円という金額を見たとき、", "非常に低すぎるのではないか」")


def quote3000_base(st0):
    return []


def quote3000_stage(prev, st):
    s = []
    if _on(prev, st, "who"):
        s.append(_tag(CX, 315.0, "弁護士（2026年10月26日の会見）", sc("lawyer"), 36, INK))
    if _on(prev, st, "say"):
        # 地 CM053 の看板の字（y613〜648）の高さに行を載せない＝門番 slide G-14
        s.append(_quote_card(CX, 525.0, 1500.0, 320.0, LW_Q, sc("lawyer"), 62))
        s.append(F.poly([(760.0, 685.0), (720.0, 755.0), (860.0, 685.0)], J.BG2, sc("lawyer"), 5, op=0.84))
    return s


# ══════════════════════════════════════════════════════════
#  two_claims（c614）＝並べて置く2つ（§B2-11 ⑦＝言い切らない）：左 弁護士に寄せられた相談／右 会社の言葉
# ══════════════════════════════════════════════════════════
TC_A = "「勝手にローンを組まれた」"
TC_B = ("「売買・公開されたことを", "示す事実は確認されて", "おりません」")


def two_claims_base(st0):
    return []


def two_claims_stage(prev, st):
    s = []
    if _on(prev, st, "a"):
        s.append(_panel(90.0, 300.0, 840.0, 500.0, sc("lawyer"), sw=5))
        s.append(_t(510.0, 366.0, "弁護士に寄せられた相談", 36, sc("lawyer"), "middle", 780))
        s.append(_t(510.0, 500.0, TC_A, 52, INK, "middle", 780))
        s.append(_t(510.0, 770.0, "ABEMA TIMES（2026年10月26日）", 26, J.TICK, "middle", 780))
    if _on(prev, st, "unk"):
        s.append(_tag(510.0, 640.0, "関係は未確認（10月31日の時点）", J.ALERT, 34, INK))
    if _on(prev, st, "b"):
        s.append(_panel(990.0, 300.0, 840.0, 500.0, sc("company"), sw=5))
        s.append(_t(1410.0, 366.0, "会社の言葉", 36, sc("company"), "middle", 780))
        s.append(_lines(1410.0, 480.0, TC_B, 50, INK, "middle", 780, 72.0))
        s.append(_t(1410.0, 770.0, "第5報（2026年10月23日）", 26, J.TICK, "middle", 780))
    return s


# ══════════════════════════════════════════════════════════
#  SNS の声（c616・c617・c618）＝原文どおりの字をこちらの札に組み直す（アイコン・X の画面の作り・アカウント名は出さない）
# ══════════════════════════════════════════════════════════
#   🔴 札の字は原文どおり（門番の側 REC_M28 の sns に原文）・注釈は3画面とも同じ置き場（cuts.ss.SNS_NOTE・SNS_NOTE_BOX＝門番 check_ground）
#   🔴 11-02 に投稿の頁と並べて確かめた：c616＝前に文が続く＝頭に「…」・2文は投稿の中で続いている／c617＝「…多いが、」の続き＝頭に「…」・2文は続いている／
#      c618＝k3a は返信の全文（宛先だけ外す）・k3b は引用の投稿の2段落目の全文
SNS_CARDS = dict(
    k2=(("…退会後どれくらいで必ず削除するというのも", "追加されればいいのにね。", "タイムズカーの免許証の画像７年保管してたのも、", "本当おかしいし。"), "X の投稿（2026年10月31日）"),
    k1a=(("…ここはしっかり対応してるのでそこは素晴らしい。",), "X の投稿（2026年10月29日）"),
    k1b=(("個人的には3000円貰ってそれでOK派なんだけど、", "あえて集団訴訟のサイトにも申し込んでおいた。"), "X の投稿（2026年10月29日）"),
    k3a=(("タイムズカーじゃなくて、ハッカーたちが犯人だよね？",), "X の投稿（2026年10月27日）"),
    k3b=(("保管する必要のない画像を保管し続け、脆弱性のあるシステムで", "流出させたことは非難されても仕方ないですが、", "その後の犯罪の責任まで負わせる必要はあるのでしょうか？"), "X の投稿（2026年10月17日）"),
)


def _sns_card(cx, cy, w, key, cap=42):
    lines, src = SNS_CARDS[key]
    lh = cap * 1.55
    h = 40 + lh * len(lines) + 56
    g = [F.rect(cx - w / 2, cy - h / 2, w, h, CARD, None, None, rx=22)]
    for i, ln in enumerate(lines):
        g.append(F.txtfit(cx - w / 2 + 48, cy - h / 2 + 28 + cap + i * lh, ln, w - 96, cap=cap, col=CARD_INK))
    g.append(F.txtfit(cx - w / 2 + 48, cy + h / 2 - 22, src, w - 96, cap=26, col=CARD_SUB))
    return "".join(g)


def sns2_base(st0):
    return [_sns_note()]


def sns2_stage(prev, st):
    s = []
    if _on(prev, st, "k2"):
        s.append(_sns_card(CX, 530.0, 1500.0, "k2", 44))
    return s


def sns1b_base(st0):
    return [_sns_note()]


def sns1b_stage(prev, st):
    s = []
    if _on(prev, st, "k1a"):
        s.append(_sns_card(CX, 400.0, 1500.0, "k1a", 44))
    if _on(prev, st, "k1b"):
        s.append(_sns_card(CX, 620.0, 1500.0, "k1b", 44))
    return s


def sns3_base(st0):
    return [_sns_note()]


def sns3_stage(prev, st):
    s = []
    if _on(prev, st, "k3a"):
        s.append(_sns_card(CX, 370.0, 1500.0, "k3a", 40))
    if _on(prev, st, "k3b"):
        s.append(_sns_card(CX, 620.0, 1500.0, "k3b", 38))
    return s


# ══════════════════════════════════════════════════════════
#  第6章  contact（c701）＝窓口（ルール §B2-11 ④）：専用窓口・問い合わせフォーム・退会した人の専用フォーム・マイページ
# ══════════════════════════════════════════════════════════
CT_TEL = "0120-25-8924"
CT_URL = "share.timescar.jp/inquiry.html"


def contact_base(st0):
    return [_panel(220.0, 300.0, 1480.0, 520.0, sc("company"), sw=5)]


def contact_stage(prev, st):
    s = []
    if _on(prev, st, "tel"):
        s.append(_phone(330.0, 410.0, 0.8, sc("company")))
        s.append(_t(400.0, 386.0, "専用窓口（24時間）", 34, sc("company"), "start", 700))
        s.append(_t(400.0, 462.0, CT_TEL, 70, INK, "start", 800))
    if _on(prev, st, "form"):
        s.append(F.line(280.0, 510.0, 1640.0, 510.0, J.LINE_DIM, 3))
        s.append(_t(300.0, 578.0, "問い合わせフォーム", 34, sc("company"), "start", 480))
        s.append(_t(800.0, 578.0, CT_URL, 40, INK, "start", 860))
        s.append(_t(300.0, 660.0, "退会した人", 34, sc("company"), "start", 480))
        s.append(_t(800.0, 660.0, "専用の問い合わせフォーム", 36, INK, "start", 860))
        s.append(_t(300.0, 742.0, "会員", 34, sc("company"), "start", 480))
        s.append(_t(800.0, 742.0, "マイページで確認", 36, INK, "start", 860))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表（mech27 と同じ作り）
# ══════════════════════════════════════════════════════════
def _v(lab, fields, base, stage):
    return dict(lab=lab, fields={f_: ONOFF for f_ in fields}, base=base, stage=stage)


#   左上の札は形の名前だけ（話題は見出しと副題＝同じ画面で同じ言葉を二度出さない・門番 dup）
VIEWS = dict(
    three=_v("正面から見た札", ("ab", "c"), three_base, three_stage),
    flow8=_v("正面から見た表", ("cut", "block", "report"), flow8_base, flow8_stage),
    clock2=_v("正面から見た時計", ("cut", "done"), clock2_base, clock2_stage),
    reports=_v("正面から見た階段", ("a", "b"), reports_base, reports_stage),
    route3=_v("正面から見た3つの箱", ("one", "word"), route3_base, route3_stage),
    cal4w=_v("正面から見た暦", ("start", "span"), cal4w_base, cal4w_stage),
    six=_v("正面から見た札", ("all", "out"), six_base, six_stage),
    bars2=_v("縦の棒", ("left", "right"), bars2_base, bars2_stage),
    words2=_v("正面から見た札", ("now", "next"), words2_base, words2_stage),
    club=_v("正面から見た表", ("box", "hit", "rows"), club_base, club_stage),
    ccard=_v("正面から見たカードの絵", ("keep", "leak"), ccard_base, ccard_stage),
    fixn=_v("左から右へ：2つの知らせ", ("old", "wester", "new"), fixn_base, fixn_stage),
    unit2=_v("横の棒", ("unit", "former"), unit2_base, unit2_stage),
    inside=_v("正面から見た箱", ("two", "park"), inside_base, inside_stage),
    purpose4=_v("正面から見た図", ("a", "b", "c"), purpose4_base, purpose4_stage),
    qa7=_v("正面から見た札", ("q", "a", "yr"), qa7_base, qa7_stage),
    law22=_v("正面から見た札", ("head", "text"), law22_base, law22_stage),
    rule_oct=_v("時間の線と表", ("now", "left"), rule_oct_base, rule_oct_stage),
    bank2=_v("左から右へ：切り替え", ("mz", "ic", "smbc"), bank2_base, bank2_stage),
    risk4=_v("正面から見た札", ("head", "a", "b"), risk4_base, risk4_stage),
    law_kyc=_v("左から右へ：法と規則", ("kuni", "law", "rule"), law_kyc_base, law_kyc_stage),
    fsa_check=_v("左から右へ：文書の流れ", ("q",), fsa_check_base, fsa_check_stage),
    jicc5=_v("時間の線", ("who", "bar"), jicc5_base, jicc5_stage),
    qa12=_v("正面から見た札", ("q", "a", "b"), qa12_base, qa12_stage),
    cutoff=_v("正面から見た2つの枠", ("line", "say"), cutoff_base, cutoff_stage),
    formula=_v("正面から見た式", ("none", "calc"), formula_base, formula_stage),
    profit=_v("縦の棒", ("bars", "pct"), profit_base, profit_stage),
    damages=_v("横の棒", ("two", "gift"), damages_base, damages_stage),
    quote3000=_v("正面から見た札", ("who", "say"), quote3000_base, quote3000_stage),
    two_claims=_v("正面から見た2つの札", ("a", "unk", "b"), two_claims_base, two_claims_stage),
    sns2=_v("SNS の投稿（原文どおりの字を札に）", ("k2",), sns2_base, sns2_stage),
    sns1b=_v("SNS の投稿（原文どおりの字を札に）", ("k1a", "k1b"), sns1b_base, sns1b_stage),
    sns3=_v("SNS の投稿（原文どおりの字を札に）", ("k3a", "k3b"), sns3_base, sns3_stage),
    contact=_v("正面から見た札", ("tel", "form"), contact_base, contact_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
# 模式（比例でも原文の字でもない関係の絵）＝左上に「模式」を付ける・note に「模式」を書く
SCHEMATIC = ("route3", "fixn", "inside", "purpose4", "bank2", "risk4", "fsa_check", "cutoff", "two_claims")
SNS_VIEWS = ("sns2", "sns1b", "sns3")
QUOTE_VIEWS = dict(sns2=("k2",), sns1b=("k1a", "k1b"), sns3=("k3a", "k3b"))


def lab_of(view, st0):
    return VIEWS[view]["lab"]


def _states(view, start, steps):
    fields = VIEWS[view]["fields"]
    cur = dict(START[view], **(start or {}))
    out = []
    for st in [dict(state={})] + list(steps):
        cur = dict(cur, **(st.get("state") or {}))
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m28：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m28：{f_}={v!r} は知らない値（{fields[f_]}）")
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
    return {"cutoff": [CO_Q], "quote3000": list(LW_Q)}.get(view, [])


def table_lines(view):
    """会社の表の項目の字（門番 echo の例外）。語りは表の8項目のうち3つを言い換えて言う＝図が語りを写したのではなく、語りが表から語っている。
    字幕は消さない（語りは表の字を読んでいない＝mute は要らない）。字は門番の側 REC_M28 の flow8 が原文と照らす"""
    return list(FW_V) if view == "flow8" else []


def m28(view, steps, start=None, rel=(), note="", src="", mute=()):
    """28本目の図解。view は VIEWS の見え方。steps＝ナレーションの行ごとの段。
    mute＝原文どおりの字を大きく出す札の字を読む行（字幕を消す＝scene_jiko.SUB_MUTE）。"""
    if quote_lines(view) and not mute:
        raise ValueError(f"m28：{view} は原文どおりの字を大きく出す＝その字を読む行を mute に書く（字幕と二重に出さない）")
    if view not in VIEWS:
        raise ValueError(f"m28：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view in SCHEMATIC and "模式" not in note:
        raise ValueError("m28：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    g = _base(view, st0)
    lab = lab_of(view, st0)
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, lab + ("・模式" if view in SCHEMATIC else ""), 1000, cap=30, col=J.TICK, ol=OL))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW * 0.60 if view in SNS_VIEWS else F.BW,
                      cap=26, col=J.TICK, ol=OL))
    stages = _stage_svgs(view, steps, st0, states)
    base_svg = "".join(g)
    f = F.Fig(base_svg, stages, "", (F.BX0, F.BX1))
    f.moves = []
    body = "".join(g[:-2]) + "".join(stages)
    f.mech = dict(kind="m28", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=[], lab=lab, note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states), texts_all=svg_texts(body),
                  sns=bool(view in SNS_VIEWS))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M28）
# ══════════════════════════════════════════════════════════
VIEW_SRC = dict(three=("company", "lawyer"), flow8=("company", "kuni"), clock2=("company",), reports=("company",), route3=("attacker",), cal4w=("company",),
                six=("member",), words2=("company",), club=("company", "attacker"), ccard=("company",), fixn=("company",), unit2=("member",), inside=("member",),
                purpose4=("company",), qa7=("company", "member"), law22=("kuni",), rule_oct=("company", "member"), bank2=("bank",), risk4=("company",), law_kyc=("kuni",),
                fsa_check=("kuni", "bank"), jicc5=("jicc",), qa12=("company", "jicc"), cutoff=("company", "lawyer"), damages=("lawyer", "company"),
                quote3000=("lawyer",), two_claims=("lawyer", "company"), contact=("company",))


def _geo(view, allst):
    if view == "three":
        return dict(val=tuple(v for _l, v, _s, _w2 in TH_V))
    if view == "flow8":
        return dict(val=(FW_V, FW["lit"]))
    if view == "clock2":
        return dict(val=tuple((d, h, m) for d, h, m in CK_T), hands=tuple(ck_angles(h, m) for _d, h, m in CK_T))
    if view == "reports":
        return dict(val=tuple((h, s, b) for h, s, b in RP_V))
    if view == "route3":
        return dict(val=RT_V)
    if view == "cal4w":
        return dict(val=(tuple((n, d.isoformat(), _cw_label(d), cw_rc(d)) for n, d in CW_R), (CW_S[1] - CW_S[0]).days))
    if view == "six":
        return dict(val=SX_V)
    if view == "bars2":
        a, b, c = BR_V
        return dict(val=(a, b, c, b + c), px=(br_y(a), br_y(b), br_y(b + c)), lins=((BR["y0"], -BR["k"], 0.0),) * 3)
    if view == "words2":
        return dict(val=("".join(WD_A), "".join(WD_B)))
    if view == "club":
        return dict(val=CB_V)
    if view == "ccard":
        return dict(val=(CC_Q, CC_N))
    if view == "fixn":
        return dict(val=(FX_V["old"], FX_V["new"], FX_V["wester"]))
    if view == "unit2":
        return dict(val=UT_V, px=tuple(ut_x(v) for v in UT_V), lins=((UT["x0"], UT["k"], 0.0),) * 2)
    if view == "inside":
        return dict(val=(IN["bw"], IN["bh"]))
    if view == "purpose4":
        return dict(val=PU_V)
    if view == "qa7":
        return dict(val=("".join(Q7_A),))
    if view == "law22":
        return dict(val=("".join(L22),))
    if view == "rule_oct":
        k = (RO["x1"] - RO["x0"]) / (RO["d1"] - RO["d0"]).days
        return dict(val=(tuple((day, what) for _d, day, what in RO_D), RO_R), pxx=tuple(ro_x(d) for d, _a, _b in RO_D), linx=((RO["x0"], k, 0.0),) * 3)
    if view == "risk4":
        return dict(val=tuple("".join(x) for x in RK_V))
    if view == "law_kyc":
        return dict(val=(KY_Q,))
    if view == "fsa_check":
        return dict(val=("".join(FS_Q),))
    if view == "jicc5":
        return dict(val=(JC_D, JC_S, JC_R))
    if view == "qa12":
        return dict(val=("".join(Q12_A), "".join(Q12_B)))
    if view == "cutoff":
        return dict(val=(CO_Q,))
    if view == "formula":
        return dict(val=(FM_A, FM_B, fm_oku()))
    if view == "profit":
        return dict(val=(PF_V, PF_M, round((PF_M[0] - PF_M[1]) / PF_M[0] * 100, 1)), px=tuple(pf_y(v) for v in PF_V), lins=((PF["y0"], -PF["k"], 0.0),) * 2)
    if view == "damages":
        return dict(val=tuple((v, c) for v, c, _l, _w2 in DM_V), px=tuple(dm_x(v) for v, _c, _l, _w2 in DM_V), lins=((DM["x0"], DM["k"], 0.0),) * 3)
    if view == "quote3000":
        return dict(val=("".join(LW_Q),))
    if view == "two_claims":
        return dict(val=(TC_A, "".join(TC_B)))
    if view in SNS_VIEWS:
        return dict(val=tuple((k, SNS_CARDS[k][0], SNS_CARDS[k][1]) for k in sorted(SNS_CARDS)))
    if view == "contact":
        return dict(val=(CT_TEL, CT_URL))
    return {}


def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst], src={k: tuple(v) for k, v in SRC.items()}, vsrc=tuple(VIEW_SRC.get(view, ())))
    out.update(_geo(view, allst))
    return out
