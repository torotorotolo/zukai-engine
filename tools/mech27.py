# -*- coding: utf-8 -*-
"""mech27.py — 27本目（八田與一容疑者の事件・2022-06-29・大分県別府市）「図解」（2026-10-30 新設・⑤b-4＝図34カット）。

■ 何か
  26本目 `mech26` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品は使わない」。再現イラストではない＝「再現」の札は出さない。
  🔴 27本目から**地は写真**（`cuts.ss.gr`＝CC BY・CC0 を暗くするだけ・方眼と章の色なし・静止＝了承② 決め1）＝字はどれも暗い縁取り（OL）・
     札の地は半ば透ける紺（`_panel`）。字と図の線の周りの地は門番 check_ground が 8:1 で測る。
  左上に見え方の名（頭は見る向き＝横から・上から・正面・時間の線／模式の見え方は末尾に「・模式」）・左下に注（模式の見え方は「模式」）と出典。
  🔴 事件の回の決まり（ルール §B2-10）：被害者・遺族・けがをした人・目撃者・SNS の投稿者の名前は描かない・容疑者は必ず「八田與一容疑者」
     （SNS の投稿の原文どおりのカードだけ例外＝原文の字）・「犯人」と書かない・**人は描かない**（顔の無い影も描かない）・事故の瞬間の人は描かない。
  🔴 **色は「誰か・何か」**（役の色＝ROLE と J の名で引く・新しい色の値は足していない）：
     警察（大分県警察）＝青 uscg／警察庁・国＝紫 tsb／遺族ら＝桃 bldg_a／報道・専門家の言葉＝茶 DOC／容疑者の車＝橙 company／
     ミニバイク＝水色 ship・オートバイ＝緑 ntsb／裁判（裁判官・刑事）＝紫 INST／民事＝緑 ntsb／目撃の情報＝橙 company／SNS の声＝白い札。
     同じ色の鍵は同じ画面に出さない（門番 check_mech の judge_m27 が VIEW_SRC で見る）。意味の色＝赤 ALERT（無い・違う・危ない）・黄 AMBER（数・日付）。
  🔴 画面の数（年・月・日・件・円・キロ・秒）は全部 `rel=` に同じ文字列で宣言する（門番が基図と段の層の全部の字から数を拾って照らす）。
  🔴 記録の値（色・数・比例・SNS の原文）は門番の側 REC_M27 が別に持つ（§5b-88）。描く側の表を書き換えると鳴る。

■ 見え方（view）＝映像方針の一覧 `ref/ep27/eizou_list27.md` の「見た目の型」（図34）
  つかみ  bignum（c103 大きな数）
  第2章  bikes2（c201 2台）・crash（c203 坂と交差点）・flee（c205 点線）・talk（c208 やり取りの帯）・speed（c210 速さの棒）・trail（c218 途切れる線）
  第3章  hitrun3（c302 3つの記号）・items4（c306 公表された物の札）・wanted（c310 全国の警察）・reward（c312 報奨金の積み棒）・steps5（c318 手配の歩み）
  第4章  charge2（c401 罪の名前の縦の年表）・complaint（c403 告訴）・charges2（c405 2つの疑い）・warrant（c406 逮捕状）・basis6（c407 6つの箱）・
         limit（c410 時効の棒）・courts2（c416 2つの部屋）
  第5章  cumline（c501 累計の線）・monthly（c502 月ごとの縦の棒）・share（c503 100マス）・verify（c508 確かめ）・mistaken（c513 人違い）・
         fake（c515 うその動画）・sns1（c517）・sns13（c518）・detective（c519 元刑事の札）
  第6章  road500（c605 手前の道）・one_min（c606 約1分）・calendar（c607 めくりの暦）・sns4（c612）・post（c615 県警の投稿の札）
  第7章  contact（c701 窓口）
  🔴 同じ型は近くで続けない：c405（2つの柱）↔c406（左から右の流れ）↔c407（3×2 の箱）・c501（線）↔c502（縦の棒）↔c503（100マス）・
     c605（上から見た道）↔c606（時間の線の2つの印）↔c607（めくりの暦）・棒は c210（横・比べ）↔c312（横・積み）↔c410（横・壁と矢印）↔c502（縦）。
     SNS の札は c517（1枚・大）↔c518（2枚・左右）↔c612（1枚・上と「？」）。

■ SPEC の書き方（mech26 と同じ）
  `**ss.gr("cm044"), fig=("m27", dict(view=…, steps=[dict(state=dict(…)), …], rel=[dict(t="1万3978件", src="T261005-03")], note="…", src="…"))`
"""
from __future__ import annotations

import datetime as _dt
import math
import re

import jiko_style as J
import titan_fig as F
from mech21 import _arrow, _on, _qmark, _xmark
from mech24 import _w, rc

ONOFF = ("off", "on")
INK = J.INK_W
CX = 960.0
OL = 7                      # 字の暗い縁取り（写真の地の上でも読める＝F.txt の ol）
PANEL_OP = 0.84             # 札の地（紺）の透けぐあい
CARD = "#f5f6f7"            # SNS の札の地（白に近い）
CARD_INK = "#14181c"
CARD_SUB = "#5c6770"

# 誰か・何か（名・ROLE か J の名）。同じ色の鍵は同じ画面に出さない（門番が VIEW_SRC で見る）
SRC = dict(
    police=("警察", "uscg"),
    npa=("警察庁", "tsb"),
    kuni=("国", "tsb"),
    family=("遺族ら", "bldg_a"),
    news=("報道", "DOC"),
    expert=("専門家", "DOC"),
    car=("容疑者の車", "company"),
    mini=("ミニバイク", "ship"),
    moto=("オートバイ", "ntsb"),
    court=("裁判", "INST"),
    civil=("民事", "ntsb"),
    seen=("目撃の情報", "company"),
    sns=("SNS の声", "SUB"),
)


def sc(key):
    return rc(SRC[key][1])


def _t(x, y, t, cap=30, col=None, anchor="start", mw=600):
    """字（暗い縁取りつき）。"""
    return F.txtfit(x, y, t, mw, cap=cap, col=col or INK, anchor=anchor, ol=OL)


def _panel(x, y, w, h, col=None, op=PANEL_OP, sw=4, rx=14, dash=None, fill=None):
    """札の地（半ば透ける紺）と縁。"""
    g = F.rect(x, y, w, h, fill or J.BG2, None, None, rx=rx, op=op)
    if col:
        g += F.rect(x, y, w, h, "none", col, sw, rx=rx, dash=dash)
    return g


def _tag(cx, cy, t, col=None, cap=30, ink=None, w=None, h=None, sw=4, dash=None):
    col = col or J.LINE
    w = w or _w(t, cap) + 52
    h = h or cap + 28
    return _panel(cx - w / 2, cy - h / 2, w, h, col, sw=sw, rx=min(h / 2, 14), dash=dash) + _t(cx, cy + cap * 0.36, t, cap, ink or col, "middle", w - 26)


def _box2(cx, cy, w, h, head, body, col, cap=34, cap2=30, ink2=None):
    """見出しと中身の2行の札。"""
    return (_panel(cx - w / 2, cy - h / 2, w, h, col)
            + _t(cx, cy - h / 2 + cap + 18, head, cap, col, "middle", w - 30)
            + _t(cx, cy + h / 2 - 24, body, cap2, ink2 or INK, "middle", w - 30))


def _dash_line(x1, y1, x2, y2, col, sw=6, dash="4 16"):
    return F.line(x1, y1, x2, y2, col, sw, dash=dash)


def _brace_h(x0, x1, y, col, up=True, t="", cap=30):
    d = -1 if up else 1
    g = F.poly([(x0, y - d * 18), (x0, y), (x1, y), (x1, y - d * 18)], "none", col, 4)
    if t:
        g += _t((x0 + x1) / 2, y + d * 22 + (cap * 0.7 if not up else -4), t, cap, col, "middle", max(200.0, x1 - x0 + 200))
    return g


# ── 小さな絵（人は描かない） ─────────────────────────────
def _bike(cx, cy, s, col, big=False):
    """横から見た二輪（前は右）。big=False＝ミニバイク（スクーターの形：後ろの覆い・足を置く床・前の覆い）・
    big=True＝オートバイ（エンジン・燃料タンク・座席・排気管）。どちらも前照灯つき。
    🔧 ⑤c'（2026-10-30）：前の形（細いひし形の枠と車輪だけ）は本番 1:1 で**ペダルの自転車**に見えた（c201・c203・c606）＝
       エンジンや覆いの塊で描き直した。車輪の位置と半径・いちばん上の高さ（ハンドル）は前と同じ＝札との位置は変えない。"""
    r = (58.0 if big else 40.0) * s
    gap = (210.0 if big else 150.0) * s
    xa, xb = cx - gap / 2, cx + gap / 2
    k = min(1.0, 0.45 + 0.55 * s)                   # 線の太さ（小さく描くときは細く＝車輪がつぶれない）
    tire, hub = 10.0 * k, (8.0 if big else 6.0) * s
    g = [F.circ(xa, cy, r, "none", col, tire), F.circ(xb, cy, r, "none", col, tire),
         F.circ(xa, cy, hub, col), F.circ(xb, cy, hub, col)]
    if big:
        # ⚠️ 座席から後ろの車輪への細い線・車輪を横切る排気管は、手元の層の焼き（qa_out/ep27_c2/r6.png）で自転車の枠に見えた＝外して太い泥よけに
        g += [F.line(cx - 40 * s, cy - 40 * s, xa, cy, col, 10 * k),                                   # 後ろの腕
              F.line(cx - 92 * s, cy - 92 * s, xa - 40 * s, cy - 66 * s, col, 12 * k),                 # 後ろの泥よけ
              F.rect(cx - 42 * s, cy - 72 * s, 84 * s, 56 * s, col, None, None, rx=8 * s),              # エンジン
              F.poly([(cx - 20 * s, cy - 104 * s), (cx + 50 * s, cy - 114 * s),
                      (cx + 64 * s, cy - 84 * s), (cx - 12 * s, cy - 76 * s)], col, None, None, close=True),  # 燃料タンク
              F.line(cx - 96 * s, cy - 96 * s, cx - 20 * s, cy - 96 * s, col, 13 * k),                 # 座席
              F.line(cx + 60 * s, cy - 110 * s, xb, cy, col, 9 * k),                                    # 前の足
              F.line(cx + 60 * s, cy - 110 * s, cx + 66 * s, cy - 134 * s, col, 7 * k),
              F.line(cx + 44 * s, cy - 134 * s, cx + 92 * s, cy - 134 * s, col, 8 * k),                 # ハンドル
              F.circ(cx + 86 * s, cy - 106 * s, 11 * s, col)]                                           # 前照灯
    else:
        g += [F.poly([(xa - 44 * s, cy - 26 * s), (xa - 36 * s, cy - 58 * s), (cx + 4 * s, cy - 62 * s),
                      (cx + 14 * s, cy - 34 * s), (cx + 14 * s, cy - 14 * s), (xa + 18 * s, cy - 14 * s)],
                     col, None, None, close=True),                                                      # 後ろの覆い
              F.line(xa - 34 * s, cy - 72 * s, cx + 2 * s, cy - 72 * s, col, 12 * k),                  # 座席
              F.line(cx + 14 * s, cy - 14 * s, xb - 34 * s, cy - 14 * s, col, 9 * k),                  # 足を置く床
              F.poly([(xb - 34 * s, cy - 14 * s), (xb - 24 * s, cy - 92 * s), (xb - 8 * s, cy - 92 * s),
                      (xb - 16 * s, cy - 14 * s)], col, None, None, close=True),                        # 前の覆い
              F.line(xb - 12 * s, cy - 88 * s, xb, cy, col, 7 * k),                                     # 前の足
              F.line(xb - 14 * s, cy - 92 * s, xb - 12 * s, cy - 100 * s, col, 7 * k),
              F.line(xb - 32 * s, cy - 100 * s, xb + 8 * s, cy - 100 * s, col, 8 * k),                  # ハンドル
              F.circ(xb + 2 * s, cy - 86 * s, 8 * s, col)]                                              # 前照灯
    return "".join(g)


def _car_side(cx, cy, w, col, op=None, dash=None):
    """横から見た軽乗用車（箱の形・車輪2つ）。cy＝地面。"""
    h = w * 0.42
    body = [(cx - w / 2, cy - 18), (cx - w / 2, cy - h * 0.62), (cx - w * 0.30, cy - h), (cx + w * 0.30, cy - h),
            (cx + w / 2, cy - h * 0.50), (cx + w / 2, cy - 18)]
    return (F.poly(body, J.BG2, col, 6, close=True, dash=dash, op=op)
            + F.circ(cx - w * 0.30, cy - 14, w * 0.11, J.BG, col, 6, op=op) + F.circ(cx + w * 0.30, cy - 14, w * 0.11, J.BG, col, 6, op=op))


def _car_top(cx, cy, L, W, col):
    """上から見た車（前＝右）。"""
    return (F.rect(cx - L / 2, cy - W / 2, L, W, J.BG2, col, 6, rx=18)
            + F.rect(cx + L * 0.08, cy - W / 2 + 12, L * 0.20, W - 24, "none", col, 4, rx=6))


def _burst(cx, cy, col, r=34.0):
    g = [F.circ(cx, cy, r * 0.30, col)]
    for i in range(10):
        a = 2 * math.pi * i / 10
        g.append(F.line(cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a), col, 6))
    return "".join(g)


def _doc(cx, cy, s, col):
    """書類（逮捕状）。"""
    w, h = 120 * s, 156 * s
    g = [F.poly([(cx - w / 2, cy - h / 2), (cx + w / 2 - 30 * s, cy - h / 2), (cx + w / 2, cy - h / 2 + 30 * s), (cx + w / 2, cy + h / 2),
                 (cx - w / 2, cy + h / 2)], J.BG2, col, 6, close=True)]
    for i in range(4):
        y = cy - h / 2 + 50 * s + i * 24 * s
        g.append(F.line(cx - w / 2 + 18 * s, y, cx + w / 2 - 18 * s - (30 * s if i == 3 else 0), y, col, 5))
    return "".join(g)


def _phone(cx, cy, s, col):
    return (F.rect(cx - 30 * s, cy - 52 * s, 60 * s, 104 * s, J.BG2, col, 6, rx=12) + F.line(cx - 12 * s, cy + 38 * s, cx + 12 * s, cy + 38 * s, col, 5))


def _cross(cx, cy, s, col):
    a = 18 * s
    return F.poly([(cx - a, cy - 3 * a), (cx + a, cy - 3 * a), (cx + a, cy - a), (cx + 3 * a, cy - a), (cx + 3 * a, cy + a), (cx + a, cy + a),
                   (cx + a, cy + 3 * a), (cx - a, cy + 3 * a), (cx - a, cy + a), (cx - 3 * a, cy + a), (cx - 3 * a, cy - a), (cx - a, cy - a)],
                  "none", col, 6, close=True)


def _cam(cx, cy, s, col):
    """防犯カメラ（箱と首）。"""
    return (F.poly([(cx - 46 * s, cy - 22 * s), (cx + 36 * s, cy - 34 * s), (cx + 40 * s, cy + 2 * s), (cx - 42 * s, cy + 14 * s)], J.BG2, col, 6, close=True)
            + F.line(cx - 10 * s, cy + 10 * s, cx - 10 * s, cy + 50 * s, col, 6) + F.line(cx - 36 * s, cy + 50 * s, cx + 16 * s, cy + 50 * s, col, 6))


def _glass(cx, cy, s, col):
    """虫めがね。"""
    return F.circ(cx, cy, 40 * s, "none", col, 8) + F.line(cx + 28 * s, cy + 28 * s, cx + 70 * s, cy + 70 * s, col, 12)


def _bubble(cx, cy, w, h, col, t, cap=30, ink=None):
    """吹き出し（しっぽは下）。"""
    g = _panel(cx - w / 2, cy - h / 2, w, h, col, rx=h / 2)
    g += F.poly([(cx - 18, cy + h / 2 - 2), (cx - 34, cy + h / 2 + 30), (cx + 8, cy + h / 2 - 2)], J.BG2, col, 4, op=PANEL_OP)
    return g + _t(cx, cy + cap * 0.36, t, cap, ink or col, "middle", w - 30)


def _page(cx, cy, w, h, top, big, col, cap=34, bigcap=76):
    """めくりの暦の1枚（綴じの帯・上の年月・大きな日）。"""
    return (_panel(cx - w / 2, cy - h / 2, w, h, col, op=0.9)
            + F.rect(cx - w / 2, cy - h / 2, w, 44, col, None, None, rx=10, op=0.9)
            + F.circ(cx - w * 0.25, cy - h / 2, 9, J.BG, col, 4) + F.circ(cx + w * 0.25, cy - h / 2, 9, J.BG, col, 4)
            + F.txtfit(cx, cy - h / 2 + 33, top, w - 24, cap=cap - 6, col=J.BG, anchor="middle")
            + _t(cx, cy + bigcap * 0.40 + 16, big, bigcap, col, "middle", w - 30))


# ══════════════════════════════════════════════════════════
#  つかみ  bignum（c103）＝大きな数（寄せられた情報の数）と「有力な手がかりは、まだ」
# ══════════════════════════════════════════════════════════
BN_V = ("1万3978件", "2026年9月末まで")


def bignum_base(st0):
    return []


def bignum_stage(prev, st):
    s = []
    if _on(prev, st, "num"):
        s.append(_t(CX, 392.0, "警察に寄せられた情報", 44, sc("police"), "middle", 1200))
        s.append(_t(CX, 600.0, BN_V[0], 176, J.AMBER, "middle", 1500))
        s.append(_t(CX, 676.0, "〈2026年の9月末までの合計〉", 36, J.LINE, "middle", 900))
    if _on(prev, st, "clue"):
        # 🔧 ⑤c'：「まだ無い」は語り（「まだ得られていないという」＝報道の伝聞）より強い言い切り＝語りの言葉に揃える
        s.append(_tag(CX, 790.0, "有力な手がかり：まだ得られていない", J.ALERT, 40, INK))
    return s


# ══════════════════════════════════════════════════════════
#  第2章  bikes2（c201）＝横から見た2台（人は描かない・並びの前後は描かない＝離して並べる）
# ══════════════════════════════════════════════════════════
BK = dict(mini=(600.0, 640.0), moto=(1320.0, 640.0))


def bikes2_base(st0):
    return [F.line(220.0, 720.0, 1700.0, 720.0, J.LINE_DIM, 4, dash="14 12")]


def bikes2_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(CX, 470.0, 96))
    if _on(prev, st, "pair"):
        s.append(_tag(CX, 360.0, "友人どうしの大学生2人", J.LINE, 36, INK))
    if _on(prev, st, "mini"):
        x, y = BK["mini"]
        s.append(_bike(x, y, 1.0, sc("mini")))
        s.append(_tag(x, 790.0, SRC["mini"][0], sc("mini"), 36))
    if _on(prev, st, "moto"):
        x, y = BK["moto"]
        s.append(_bike(x, y, 1.0, sc("moto"), big=True))
        s.append(_tag(x, 790.0, SRC["moto"][0], sc("moto"), 36))
    return s


# ══════════════════════════════════════════════════════════
#  crash（c203）＝横から見た坂と交差点：坂を下る軽乗用車 → 止まっていた2台に追突 → 信号機の柱で止まる（人は描かない）
# ══════════════════════════════════════════════════════════
CR = dict(road=((170.0, 400.0), (980.0, 720.0), (1780.0, 720.0)), car=(420.0, 500.0), pair=(1120.0, 720.0), pole=1560.0)


def crash_base(st0):
    (x0, y0), (x1, y1), (x2, y2) = CR["road"]
    p = CR["pole"]
    g = [F.poly([(x0, y0), (x1, y1), (x2, y2)], "none", J.LINE, 8),
         F.line(p, 720.0, p, 420.0, J.LINE, 8),
         F.rect(p - 34, 380.0, 68.0, 120.0, J.BG2, J.LINE, 5, rx=10),
         F.circ(p, 412.0, 14, J.ALERT), F.circ(p, 468.0, 14, "none", J.LINE_DIM, 4),
         _t(p + 60, 470.0, "信号機の柱", 32, J.LINE, "start", 300)]
    # 止まっていた2台（並びの前後は描かない＝札の中に2つの印）
    cx, cy = CR["pair"]
    g.append(_panel(cx - 130, cy - 150, 260, 130, J.LINE))
    # 🔧 ⑤c'：0.42・±58 では描き直した2台の車輪が重なって1つの塊に見えた（手元の層の焼き）＝0.38・±60（車輪のすき間 約14px・額の中）
    g.append(_bike(cx - 60, cy - 62, 0.38, sc("mini")) + _bike(cx + 60, cy - 62, 0.38, sc("moto"), big=True))
    g.append(_t(cx, cy + 50, "止まっていた2台", 32, INK, "middle", 380))
    return g


def crash_stage(prev, st):
    s = []
    cx, cy = CR["pair"]
    if _on(prev, st, "hit"):
        x, y = CR["car"]
        s.append(_car_side(x, y, 170.0, sc("car")))
        s.append(_t(x - 20, y - 110, "坂を下ってきた軽乗用車", 32, sc("car"), "start", 520))
        s.append(_arrow(x + 110, y + 12, cx - 160, cy - 64, sc("car"), 8, 30))
        s.append(_burst(cx - 148, cy - 88, J.ALERT, 40))
        s.append(_t(cx - 150, cy - 156, "後ろから追突", 32, J.ALERT, "middle", 300))
    if _on(prev, st, "pole"):
        p = CR["pole"]
        s.append(_arrow(cx + 140, cy - 40, p - 110, cy - 40, sc("car"), 8, 30))
        s.append(_car_side(p - 100, cy, 150.0, sc("car")))
        s.append(_burst(p - 18, cy - 70, J.ALERT, 34))
    return s


# ══════════════════════════════════════════════════════════
#  flee（c205）＝上から見た、止まった車と、そこから離れていく点線（人は描かない）
# ══════════════════════════════════════════════════════════
FL = dict(car=(520.0, 560.0), pts=((640.0, 560.0), (900.0, 520.0), (1180.0, 600.0), (1460.0, 520.0), (1720.0, 470.0)))


def flee_base(st0):
    x, y = FL["car"]
    return [F.rect(180.0, 470.0, 1640.0, 180.0, "none", J.LINE_DIM, 3, rx=30, dash="18 12"),
            _car_top(x, y, 240.0, 120.0, sc("car")),
            _t(x, y + 128, "車をその場に残した", 32, sc("car"), "middle", 420)]


def flee_stage(prev, st):
    s = []
    if _on(prev, st, "run"):
        pts = FL["pts"]
        s.append(F.poly(list(pts), "none", INK, 7, dash="4 18"))
        s.append(_arrow(pts[-2][0], pts[-2][1], pts[-1][0] + 40, pts[-1][1] - 8, INK, 7, 30))
        s.append(_t(1180.0, 420.0, "走って逃げた", 36, INK, "middle", 400))
    if _on(prev, st, "bare"):
        s.append(_tag(1180.0, 760.0, "靴をはかず、裸足だったとみられる", J.AMBER, 36, INK))
        s.append(_t(1180.0, 826.0, "（防犯カメラなどの映像による）", 28, J.LINE, "middle", 600))
    return s


# ══════════════════════════════════════════════════════════
#  talk（c208）＝時間の線：15秒か30秒ぐらいのやり取り → そのあと交差点（時刻は描かない・長さは秒に比例）
# ══════════════════════════════════════════════════════════
TK = dict(x0=360.0, k=24.0, y=600.0, h=70.0)
TK_S = (15, 30)


def tk_x(sec):
    return TK["x0"] + sec * TK["k"]


def talk_base(st0):
    y = TK["y"]
    g = [F.line(TK["x0"] - 60, y, 1720.0, y, J.LINE_DIM, 4)]
    for sec in range(0, 31, 5):
        x = tk_x(sec)
        g.append(F.line(x, y + TK["h"] / 2 + 6, x, y + TK["h"] / 2 + 22, J.TICK, 3))
    g.append(_t(tk_x(0), y + TK["h"] / 2 + 56, "0秒", 26, J.TICK, "middle", 120))
    return g


def talk_stage(prev, st):
    s = []
    y, h = TK["y"], TK["h"]
    if _on(prev, st, "say"):
        s.append(_bubble(720.0, 400.0, 560.0, 90.0, J.LINE, "言いがかりをつけてきた", 34, INK))
        s.append(_t(1060.0, 412.0, "（けがをした友人の話）", 28, J.LINE, "start", 400))
    if _on(prev, st, "band"):
        a, b = TK_S
        s.append(F.rect(tk_x(0), y - h / 2, tk_x(a) - tk_x(0), h, J.AMBER, None, None, rx=8, op=0.9))
        s.append(F.rect(tk_x(a), y - h / 2, tk_x(b) - tk_x(a), h, "none", J.AMBER, 5, rx=8, dash="12 8"))
        s.append(_t(tk_x(a), y + h / 2 + 56, f"{a}秒", 28, J.AMBER, "middle", 120))
        s.append(_t(tk_x(b), y + h / 2 + 56, f"{b}秒", 28, J.AMBER, "middle", 120))
        s.append(_t((tk_x(0) + tk_x(b)) / 2, y - h / 2 - 20, "やり取り（友人の話）", 32, INK, "middle", 500))
        s.append(_arrow(tk_x(b) + 30, y, 1500.0, y, J.LINE, 7, 28))
        s.append(_tag(1640.0, y, "そのあと交差点", J.LINE, 32, INK))
    return s


# ══════════════════════════════════════════════════════════
#  speed（c210）＝横の棒（長さは時速に比例）：制限 40・報道の数 70以上〈2022年〉・100近く〈2023年〉
# ══════════════════════════════════════════════════════════
SP = dict(x0=520.0, k=11.0, ys=(430.0, 580.0, 700.0), h=72.0)
SP_V = (40, 70)          # 🔧 ⑤c'：100（2023年の報道）は c211 の語り＝この図から外した


def sp_x(v):
    return SP["x0"] + v * SP["k"]


def speed_base(st0):
    x0 = SP["x0"]
    g = [F.line(x0, 360.0, x0, 760.0, J.LINE, 5)]
    # 🔧 ⑤c'：「2023年の報道 100キロ近く」の行を外した＝100キロは次の c211 の語り（c210 の語りは 70キロ以上まで＝図が先回りしていた）
    for lab, y in zip(("制限", "2022年の報道"), SP["ys"]):
        g.append(_t(x0 - 26, y + 11, lab, 30, INK, "end", 340))
    return g


def speed_stage(prev, st):
    s = []
    x0, h = SP["x0"], SP["h"]
    if _on(prev, st, "lim"):
        y = SP["ys"][0]
        s.append(F.rect(x0, y - h / 2, sp_x(SP_V[0]) - x0, h, J.LINE, None, None, rx=6))
        s.append(_t(sp_x(SP_V[0]) + 20, y + 12, "時速40キロ", 36, J.LINE, "start", 400))
    if _on(prev, st, "fast"):
        y = SP["ys"][1]
        s.append(F.rect(x0, y - h / 2, sp_x(SP_V[1]) - x0, h, J.ALERT, None, None, rx=6))
        s.append(_arrow(sp_x(SP_V[1]), y, sp_x(SP_V[1]) + 90, y, J.ALERT, 8, 28))
        s.append(_t(sp_x(SP_V[1]) + 110, y + 12, "70キロ以上", 36, J.ALERT, "start", 360))
        # 🔧 ⑤c'：y800 では札の周りの地の升が 8.0:1 を下回った（check_ground）＝外した3行目の空き y700 へ
        s.append(_tag(1460.0, 700.0, "ブレーキの跡は無かった", J.AMBER, 32, INK))
    return s


# ══════════════════════════════════════════════════════════
#  trail（c218）＝上から見た、交差点から港まで続く点線が港で途切れる（「6月29日」「2日後」だけ）
# ══════════════════════════════════════════════════════════
TR = dict(a=(300.0, 640.0), pts=((300.0, 640.0), (620.0, 560.0), (960.0, 600.0), (1260.0, 500.0), (1430.0, 470.0)), sea=1520.0)


def trail_base(st0):
    ax, ay = TR["a"]
    g = [F.circ(ax, ay, 16, J.ALERT), _t(ax, ay + 60, "交差点", 30, INK, "middle", 200), _t(ax, ay + 100, "6月29日", 30, J.AMBER, "middle", 240)]
    x = TR["sea"]
    for i in range(5):
        y = 360.0 + i * 100
        g.append(F.poly([(x + 20, y), (x + 80, y - 18), (x + 140, y), (x + 200, y - 18), (x + 260, y)], "none", J.TICK, 4))
    g.append(_t(x + 140, 860.0, "港（海）", 30, J.TICK, "middle", 260))
    return g


def trail_stage(prev, st):
    s = []
    if _on(prev, st, "dna"):
        pts = TR["pts"]
        s.append(F.poly(list(pts), "none", INK, 7, dash="4 18"))
        ex, ey = pts[-1]
        s.append(F.line(ex + 20, ey - 26, ex + 20, ey + 26, J.ALERT, 8))
        s.append(_t(ex - 10, ey - 52, "ここで途切れる", 30, J.ALERT, "middle", 300))
        s.append(_tag(ex - 60, 690.0, "2日後 Tシャツ", J.AMBER, 32, INK))
        s.append(_tag(ex - 60, 790.0, "DNAの型が容疑者と一致したとされる（報道）", sc("news"), 30, INK))
    return s


# ══════════════════════════════════════════════════════════
#  第3章  hitrun3（c302）＝正面から見た3つの記号（ひき逃げ＝けが人を助けない・警察に知らせない・立ち去る）
# ══════════════════════════════════════════════════════════
HR_XS = (520.0, 960.0, 1400.0)


def hitrun3_base(st0):
    return [_tag(CX, 340.0, "ひき逃げ（道路交通法違反）", J.AMBER, 40, INK)]


def hitrun3_stage(prev, st):
    s = []
    if _on(prev, st, "three"):
        labs = ("けが人を助けない", "警察に知らせない", "その場を立ち去る")
        for x, lab in zip(HR_XS, labs):
            s.append(_panel(x - 160, 450.0, 320.0, 250.0, J.LINE))
            s.append(_t(x, 674.0, lab, 32, INK, "middle", 300))
        s.append(_cross(HR_XS[0], 545.0, 1.3, J.ALERT) + _xmark(HR_XS[0] + 76, 600.0, 26))
        s.append(_phone(HR_XS[1], 545.0, 1.1, sc("police")) + _xmark(HR_XS[1] + 76, 600.0, 26))
        s.append(F.rect(HR_XS[2] - 120, 490.0, 110.0, 110.0, "none", J.LINE, 6, rx=8) + _arrow(HR_XS[2] - 40, 545.0, HR_XS[2] + 130, 545.0, J.ALERT, 9, 32))
    return s


# ══════════════════════════════════════════════════════════
#  items4（c306）＝正面から見た、公表された物の札（文字の札だけ・物の写真は使わない）
# ══════════════════════════════════════════════════════════
IT = (("黒いTシャツ", 520.0, 470.0), ("スリッパ（車の中）", 1300.0, 470.0), ("リュックサック", 520.0, 640.0))
IT_AREA = ("土地勘がありそうな地域", 1300.0, 640.0)


def _hang(cx, cy, t, col):
    w = max(_w(t, 34) + 110, 420)
    return (_panel(cx - w / 2, cy - 48, w, 96, col, rx=12) + F.circ(cx - w / 2 + 34, cy, 12, J.BG, col, 4)
            + _t(cx + 18, cy + 12, t, 34, INK, "middle", w - 90))


def items4_base(st0):
    return [_t(CX, 360.0, "警察が公表した手がかり（2023年5月）", 34, sc("police"), "middle", 900)]


def items4_stage(prev, st):
    s = []
    if _on(prev, st, "items"):
        for t, x, y in IT:
            s.append(_hang(x, y, t, J.LINE))
    if _on(prev, st, "area"):
        t, x, y = IT_AREA
        s.append(_hang(x, y, t, J.AMBER))
    return s


# ══════════════════════════════════════════════════════════
#  wanted（c310）＝正面から見た、警察庁の指定 → 全国の警察（「道路交通法違反で全国初」の札）
# ══════════════════════════════════════════════════════════
WD = dict(npa=(470.0, 560.0), grid=(1100.0, 420.0), n=(6, 4), cell=88.0)


def wanted_base(st0):
    x, y = WD["npa"]
    return [_box2(x, y, 340.0, 140.0, "警察庁が指定", "重要指名手配", sc("npa"), 34, 40)]


def wanted_stage(prev, st):
    s = []
    if _on(prev, st, "fan"):
        gx, gy = WD["grid"]
        nx, ny = WD["n"]
        c = WD["cell"]
        for j in range(ny):
            for i in range(nx):
                s.append(F.rect(gx + i * c, gy + j * c, c - 18, c - 18, "none", sc("police"), 5, rx=8))
        x, y = WD["npa"]
        for j in range(ny):
            s.append(_arrow(x + 180, y, gx - 24, gy + j * c + (c - 18) / 2, sc("npa"), 5, 22))
        s.append(_t(gx + nx * c / 2 - 9, gy + ny * c + 50, "全国の警察で重点的に捜す", 32, sc("police"), "middle", 640))
    if _on(prev, st, "first"):
        s.append(_tag(470.0, 760.0, "道路交通法違反で初めての指定（全国）", J.AMBER, 32, INK))
    return s


# ══════════════════════════════════════════════════════════
#  reward（c312）＝横の積み棒（長さは金額に比例）：国 上限300万円〈2023年9月15日から〉＋遺族らの懸賞金 上限500万円＝最大800万円
# ══════════════════════════════════════════════════════════
RW = dict(x0=260.0, k=1.70, y=560.0, h=96.0)
RW_V = (300, 500, 800)


def rw_x(v):
    return RW["x0"] + v * RW["k"]


def reward_base(st0):
    return [F.line(RW["x0"], RW["y"] - 90, RW["x0"], RW["y"] + 90, J.LINE, 5)]


def reward_stage(prev, st):
    s = []
    y, h = RW["y"], RW["h"]
    if _on(prev, st, "kuni"):
        s.append(F.rect(RW["x0"], y - h / 2, rw_x(RW_V[0]) - RW["x0"], h, sc("kuni"), None, None, rx=6))
        s.append(_t((RW["x0"] + rw_x(RW_V[0])) / 2, y - h / 2 - 54, "国の捜査特別報奨金", 32, sc("kuni"), "middle", 520))
        s.append(_t((RW["x0"] + rw_x(RW_V[0])) / 2, y - h / 2 - 16, "上限300万円（2023年9月15日から）", 28, INK, "middle", 560))
    if _on(prev, st, "who"):
        s.append(_tag((RW["x0"] + rw_x(RW_V[0])) / 2, 380.0 - 60, "対象＝逮捕に役立つ情報を寄せた人", sc("kuni"), 30, INK))
    if _on(prev, st, "family"):
        x1 = rw_x(RW_V[0])
        s.append(F.rect(x1, y - h / 2, rw_x(RW_V[2]) - x1, h, sc("family"), None, None, rx=6))
        s.append(_t((x1 + rw_x(RW_V[2])) / 2, y + h / 2 + 46, "遺族らの懸賞金 上限500万円", 30, sc("family"), "middle", 700))
        s.append(_brace_h(RW["x0"], rw_x(RW_V[2]), y + h / 2 + 90, J.AMBER, up=False, t="最大800万円", cap=40))
        s.append(_tag(1640.0, 380.0 - 60, "大分県で初めて", J.AMBER, 30, INK))
    return s


# ══════════════════════════════════════════════════════════
#  steps5（c318）＝時間の線（横・月に比例）：2022年7月 → 2023年5月 → 2023年9月 → 2024年6月 → 2024年8月（頭は事件の2022年6月）
# ══════════════════════════════════════════════════════════
ST = dict(x0=230.0, x1=1690.0, m0=(2022, 6), m1=(2024, 8), y=600.0)
ST_EV = (((2022, 7), "名前と顔写真"), ((2023, 5), "動画10本"), ((2023, 9), "重要指名手配・報奨金"), ((2024, 6), "似顔絵"), ((2024, 8), "手配の動画"))


def _mi(ym):
    return ym[0] * 12 + ym[1] - 1


def st_x(ym):
    return ST["x0"] + (_mi(ym) - _mi(ST["m0"])) * (ST["x1"] - ST["x0"]) / (_mi(ST["m1"]) - _mi(ST["m0"]))


def steps5_base(st0):
    y = ST["y"]
    g = [F.line(ST["x0"], y, ST["x1"] + 60, y, J.LINE, 6)]
    for yr in (2023, 2024):
        x = st_x((yr, 1))
        g.append(F.line(x, y - 14, x, y + 14, J.TICK, 4) + _t(x, y + 50, f"{yr}年", 26, J.TICK, "middle", 140))
    g.append(F.circ(ST["x0"], y, 12, J.ALERT) + _t(ST["x0"], y + 50, "事件", 26, J.ALERT, "middle", 140))
    return g


def steps5_stage(prev, st):
    s = []
    y = ST["y"]
    if _on(prev, st, "pts"):
        for i, (ym, lab) in enumerate(ST_EV):
            x = st_x(ym)
            up = i % 2 == 0
            yy = y - 110 if up else y + 130
            s.append(F.circ(x, y, 16, sc("police")))
            s.append(F.line(x, y + (-18 if up else 18), x, yy + (34 if up else -40), sc("police"), 3))
            s.append(_t(x, yy - 6, f"{ym[0]}年{ym[1]}月", 26, J.AMBER, "middle", 260))
            s.append(_t(x, yy + 30, lab, 30, INK, "middle", 300))
    if _on(prev, st, "span"):
        # 🔧 ⑤b-4 の目視：下に置くと左下の注の行と約5px（geom_gap の 6px 未満）＝時間の線の上側へ
        s.append(_brace_h(ST["x0"], st_x(ST["m1"]), 400.0, J.AMBER, up=True, t="事件から2年あまり", cap=32))
    return s


# ══════════════════════════════════════════════════════════
#  第4章  charge2（c401）＝時間の線（縦）：2022年「道路交通法違反〈ひき逃げ〉」→ 2025年6月から「殺人・殺人未遂・道路交通法違反」
# ══════════════════════════════════════════════════════════
CG = dict(x=420.0, ya=420.0, yb=700.0)


def charge2_base(st0):
    x = CG["x"]
    return [F.line(x, 340.0, x, 800.0, J.LINE, 6),
            F.circ(x, CG["ya"], 14, J.AMBER) + _t(x - 30, CG["ya"] + 10, "2022年", 32, J.AMBER, "end", 240),
            F.circ(x, CG["yb"], 14, J.AMBER) + _t(x - 30, CG["yb"] + 10, "2025年6月", 32, J.AMBER, "end", 280)]


def charge2_stage(prev, st):
    s = []
    x = CG["x"]
    if _on(prev, st, "q"):
        s.append(_qmark(1500.0, 560.0, 90))
    if _on(prev, st, "old"):
        s.append(_panel(x + 50, CG["ya"] - 60, 760.0, 120.0, sc("police")))
        s.append(_t(x + 430, CG["ya"] + 14, "道路交通法違反（ひき逃げ）", 38, INK, "middle", 700))
        s.append(_t(x + 430, CG["ya"] - 76, "はじめの手配の疑い", 28, sc("police"), "middle", 500))
    if _on(prev, st, "one"):
        s.append(_tag(x + 1000, CG["ya"], "罪の名前は ひとつだけ", J.AMBER, 32, INK))
        s.append(_panel(x + 50, CG["yb"] - 60, 980.0, 120.0, J.ALERT, dash="14 10"))
        s.append(_t(x + 540, CG["yb"] + 14, "殺人・殺人未遂・道路交通法違反", 38, INK, "middle", 920))
        s.append(_t(x + 540, CG["yb"] - 76, "このあと（2025年6月から）", 28, J.ALERT, "middle", 500))
    return s


# ══════════════════════════════════════════════════════════
#  complaint（c403）＝横から見た流れ：告訴＝遺族らの会 → 警察へ「罪を調べて、罰して」・5万人以上の署名
#   🔧 ⑤c'：「被害を受けた側」は語り（c402「亡くなった大学生の父親ら、…遺族らの会が」）よりあいまい＝語りの言葉に揃えた（名前は出さない）
# ══════════════════════════════════════════════════════════
def complaint_base(st0):
    return [_box2(430.0, 540.0, 340.0, 130.0, "遺族らの会", "告訴状を出す", sc("family"), 34, 30),
            _box2(1490.0, 540.0, 340.0, 130.0, "別府警察署", "受け付けた", sc("police"), 34, 30)]


def complaint_stage(prev, st):
    s = []
    if _on(prev, st, "file"):
        s.append(_arrow(620.0, 540.0, 1300.0, 540.0, sc("family"), 9, 34))
        s.append(_t(CX, 500.0, "告訴", 40, sc("family"), "middle", 300))
        s.append(_t(CX, 600.0, "「罪を調べて、罰して」", 32, INK, "middle", 520))
        s.append(_tag(CX, 760.0, "5万人以上の署名", J.AMBER, 38, INK))
    return s


# ══════════════════════════════════════════════════════════
#  charges2（c405）＝正面から見た2つの柱：2025年6月2日 逮捕状（手配からおよそ3年後）・殺人＝亡くなった大学生／殺人未遂＝けがをした友人
# ══════════════════════════════════════════════════════════
CH = dict(l=520.0, r=1400.0, top=560.0)


def charges2_base(st0):
    return []


def charges2_stage(prev, st):
    s = []
    if _on(prev, st, "date"):
        s.append(_tag(CX, 340.0, "2025年6月2日", J.AMBER, 40, INK))
    if _on(prev, st, "warrant"):
        s.append(_doc(CX, 520.0, 0.9, sc("court")) + _t(CX, 640.0, "逮捕状", 34, sc("court"), "middle", 300))
        s.append(_t(CX, 690.0, "手配から およそ3年後", 28, J.LINE, "middle", 400))
    if _on(prev, st, "two"):
        for x, head, body, col in ((CH["l"], "殺人の疑い", "亡くなった大学生", J.ALERT), (CH["r"], "殺人未遂の疑い", "けがをした友人", J.LINE)):
            s.append(_panel(x - 230, 440.0, 460.0, 340.0, col, sw=6))
            s.append(_t(x, 510.0, head, 44, col, "middle", 420))
            s.append(F.line(x - 180, 548.0, x + 180, 548.0, col, 3))
            s.append(_arrow(x, 570.0, x, 640.0, col, 6, 22))
            s.append(_t(x, 720.0, body, 38, INK, "middle", 420))
    return s


# ══════════════════════════════════════════════════════════
#  warrant（c406）＝横から見た流れ：裁判官が出す → 逮捕状 → 警察が逮捕できる・「罪が決まったのではない」・推定無罪
# ══════════════════════════════════════════════════════════
def warrant_base(st0):
    return [_tag(330.0, 400.0, "裁判官", sc("court"), 34), _arrow(450.0, 400.0, 840.0, 400.0, sc("court"), 6, 24),
            _doc(CX, 400.0, 0.62, sc("court")), _arrow(1080.0, 400.0, 1440.0, 400.0, sc("police"), 6, 24),
            _tag(1600.0, 400.0, "警察が逮捕できる", sc("police"), 32)]


def warrant_stage(prev, st):
    s = []
    if _on(prev, st, "notyet"):
        s.append(_tag(CX, 560.0, "有罪が決まったのではない", J.ALERT, 38, INK))
    if _on(prev, st, "court"):
        s.append(_arrow(360.0, 670.0, 1480.0, 670.0, J.LINE, 6, 26))
        s.append(F.line(1540.0, 610.0, 1540.0, 730.0, sc("court"), 10))
        s.append(_t(920.0, 640.0, "裁判で決まるまで", 32, J.LINE, "middle", 600))
        s.append(_t(920.0, 716.0, "罪を犯した人とは見なさない", 32, INK, "middle", 700))
        s.append(_t(1600.0, 680.0, "裁判", 32, sc("court"), "start", 200))
    if _on(prev, st, "pres"):
        s.append(_tag(CX, 810.0, "推定無罪", J.AMBER, 48, INK))
    return s


# ══════════════════════════════════════════════════════════
#  basis6（c407）＝正面から見た6つの箱（報道の根拠）：速さ・ブレーキの跡・何度もの走行実験・防犯カメラの解析・現場の検証・残された車の計器
# ══════════════════════════════════════════════════════════
BS = (("速さ", "制限（40キロ）を大きく超える"), ("ブレーキの跡", "無かった"), ("何度もの走行実験", ""), ("防犯カメラの解析", ""),
      ("現場の検証", ""), ("残された車の計器", ""))


def bs_box(i):
    """6つの札の真ん中（3列×2段）。"""
    col, row = i % 3, i // 3
    return 460.0 + col * 500.0, 470.0 + row * 230.0


def basis6_base(st0):
    return [_t(CX, 336.0, "報道が伝えた根拠", 32, sc("news"), "middle", 800)]


def basis6_stage(prev, st):
    s = []
    if _on(prev, st, "all"):
        for i, (head, _b) in enumerate(BS):
            if i >= 2:
                x, y = bs_box(i)
                s.append(_tag(x, y, head, J.LINE_DIM, 34, J.TICK))
    if _on(prev, st, "speed"):
        x, y = bs_box(0)
        s.append(_tag(x, y, BS[0][0], J.AMBER, 40, INK, sw=7) + _t(x, y + 74, BS[0][1], 28, J.AMBER, "middle", 440))
    if _on(prev, st, "brake"):
        x, y = bs_box(1)
        s.append(_tag(x, y, BS[1][0], J.AMBER, 40, INK, sw=7) + _t(x, y + 74, BS[1][1], 30, J.AMBER, "middle", 440))
    return s


# ══════════════════════════════════════════════════════════
#  limit（c410）＝横の棒（長さは年に比例）：ひき逃げの罪のまま＝時効7年（壁）・殺人＝時効なし（矢印が画面の外へ）
# ══════════════════════════════════════════════════════════
LM = dict(x0=480.0, k=110.0, ya=470.0, yb=650.0, h=70.0)
LM_V = 7


def limit_base(st0):
    x0 = LM["x0"]
    return [F.line(x0, 380.0, x0, 740.0, J.LINE, 5),
            _t(x0 - 26, LM["ya"] + 11, "ひき逃げの罪のまま", 30, INK, "end", 380),
            _t(x0 - 26, LM["yb"] + 11, "殺人", 34, INK, "end", 380)]


def limit_stage(prev, st):
    s = []
    x0, h = LM["x0"], LM["h"]
    if _on(prev, st, "bars"):
        xe = x0 + LM_V * LM["k"]
        s.append(F.rect(x0, LM["ya"] - h / 2, xe - x0, h, J.LINE, None, None, rx=6))
        s.append(F.line(xe + 10, LM["ya"] - 70, xe + 10, LM["ya"] + 70, J.ALERT, 12))
        s.append(_t(xe + 40, LM["ya"] + 12, "時効 7年", 36, J.LINE, "start", 300))
        s.append(F.rect(x0, LM["yb"] - h / 2, 1280.0, h, J.ALERT, None, None, rx=6, op=0.9))
        s.append(_arrow(x0 + 1280, LM["yb"], x0 + 1330, LM["yb"], J.ALERT, 12, 40))
    if _on(prev, st, "none"):
        s.append(_tag(x0 + 1000, LM["yb"] + 110, "時効なし", J.AMBER, 40, INK))
    return s


# ══════════════════════════════════════════════════════════
#  courts2（c416）＝正面から見た2つの部屋：民事（損害をお金で償うよう求める）・刑事（罪があるかを決める）
# ══════════════════════════════════════════════════════════
def _room(cx, cy, w, h, col, head, body, lit):
    op = None if lit else 0.55
    roof = F.poly([(cx - w / 2 - 20, cy - h / 2), (cx, cy - h / 2 - 90), (cx + w / 2 + 20, cy - h / 2)], "none", col, 6, op=op)
    return (roof + _panel(cx - w / 2, cy - h / 2, w, h, col, op=PANEL_OP if lit else 0.5, sw=6 if lit else 3)
            + _t(cx, cy - 30, head, 44, col if lit else J.TICK, "middle", w - 40) + _t(cx, cy + 60, body, 30, INK if lit else J.TICK, "middle", w - 40))


def courts2_base(st0):
    return [_room(1380.0, 610.0, 560.0, 300.0, sc("court"), "刑事の裁判", "罪があるかを決める", False)]


def courts2_stage(prev, st):
    s = []
    if _on(prev, st, "civil"):
        s.append(_room(540.0, 610.0, 560.0, 300.0, sc("civil"), "民事の裁判", "損害をお金で償うよう求める", True))
        s.append(_t(CX, 610.0, "≠", 80, J.AMBER, "middle", 120))
    return s


# ══════════════════════════════════════════════════════════
#  第5章  cumline（c501）＝時間の線と累計（横は日に比例・縦は件数に比例）
# ══════════════════════════════════════════════════════════
CL = dict(x0=300.0, x1=1640.0, d0=(2022, 6, 29), d1=(2026, 9, 30), y0=790.0, k=440.0 / 14000.0)
CL_PTS = (((2022, 7, 28), 36, "36件", "2022年7月28日"), ((2023, 6, 29), 854, "854件", "2023年6月29日"),
          ((2023, 12, 31), 4052, "4052件", "2023年12月末"),
          ((2024, 8, 31), 6937, "6937件", "2024年8月末"),    # 🔧 ⑤c'：語り「2年あまりで6937件」の点が無かった（① §2 の累計）
          ((2025, 4, 30), 9430, "9430件", "2025年4月末"),
          ((2025, 12, 31), 12029, "1万2029件", "2025年12月末"), ((2026, 9, 30), 13978, "1万3978件", "2026年9月末"))


def _days(d):
    return (_dt.date(*d) - _dt.date(*CL["d0"])).days


def cl_x(d):
    return CL["x0"] + _days(d) * (CL["x1"] - CL["x0"]) / _days(CL["d1"])


def cl_y(v):
    return CL["y0"] - v * CL["k"]


def cumline_base(st0):
    g = [F.line(CL["x0"], CL["y0"], CL["x1"] + 60, CL["y0"], J.LINE, 5), F.line(CL["x0"], CL["y0"], CL["x0"], 320.0, J.LINE_DIM, 3)]
    for yr in (2023, 2024, 2025, 2026):
        x = cl_x((yr, 1, 1))
        g.append(F.line(x, CL["y0"], x, CL["y0"] + 14, J.TICK, 4) + _t(x, CL["y0"] + 46, f"{yr}年", 26, J.TICK, "middle", 140))
    return g


def _cl_dot(i, lab_dy=-30, anchor="middle"):
    d, v, lab, when = CL_PTS[i]
    x, y = cl_x(d), cl_y(v)
    return F.circ(x, y, 12, J.AMBER) + _t(x, y + lab_dy, lab, 30, J.AMBER, anchor, 300) + _t(x, y + lab_dy + 34, f"〈{when}〉", 22, J.LINE, anchor, 300)


def cumline_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_qmark(960.0, 520.0, 80))
    if _on(prev, st, "ends"):
        s.append(_cl_dot(0, -60, "start"))
        s.append(_cl_dot(6, -60, "end"))
    if _on(prev, st, "line"):
        pts = [(cl_x(d), cl_y(v)) for d, v, _l, _w in CL_PTS]
        s.append(F.poly(pts, "none", J.AMBER, 7))
        s.append(_cl_dot(1, -100, "middle"))
        s.append(_cl_dot(2, -96, "end"))          # 🔧 layout：-50 では 854件の札と重なった
        s.append(_cl_dot(3, -60, "end"))          # 🆕 ⑤c'：6937件（2024年8月末）＝点の左上（4052件の札より右・線より上）
        s.append(_cl_dot(4, 52, "start"))         # 🔧 check_slide G-14：上に置くと地の写真の焼き込みの字（駅の札）に載った＝点の右下へ
        s.append(_cl_dot(5, -50, "end"))
    return s


# ══════════════════════════════════════════════════════════
#  monthly（c502）＝縦の棒（高さは件数に比例）：月ごとの山（2023年9月の後半 884・10月 915・2024年7月 約660・2025年6月 706・2026年6月 401）
# ══════════════════════════════════════════════════════════
MO = dict(y0=790.0, k=0.40, w=150.0, xs=(330.0, 560.0, 900.0, 1240.0, 1580.0))
MO_V = (("2023年9月15〜30日", 884, "884件", "報奨金の対象に"), ("2023年10月", 915, "915件", ""), ("2024年7月", 660, "約660件", "似顔絵"),
        ("2025年6月", 706, "706件", "殺人の逮捕状"), ("2026年6月", 401, "401件", ""))


def mo_top(v):
    return MO["y0"] - v * MO["k"]


def monthly_base(st0):
    g = [F.line(220.0, MO["y0"], 1720.0, MO["y0"], J.LINE, 5)]
    for (lab, _v, _n, _t2), x in zip(MO_V, MO["xs"]):
        g.append(_t(x, MO["y0"] + 40, lab, 24, J.TICK, "middle", 220))
    return g


def _mo_bar(i, col):
    lab, v, num, tag = MO_V[i]
    x, top = MO["xs"][i], mo_top(v)
    g = F.rect(x - MO["w"] / 2, top, MO["w"], MO["y0"] - top, col, None, None, rx=6) + _t(x, top - 16, num, 30, INK, "middle", 220)
    if tag:
        g += _t(x, top - 56, tag, 26, col, "middle", 240)
    return g


def monthly_stage(prev, st):
    s = []
    if _on(prev, st, "y23"):
        s.append(_mo_bar(0, sc("kuni")) + _mo_bar(1, sc("kuni")))
    if _on(prev, st, "later"):
        s.append(_mo_bar(2, J.LINE) + _mo_bar(3, J.ALERT) + _mo_bar(4, J.LINE_DIM))
    if _on(prev, st, "share"):
        s.append(_tag(1240.0, 300.0, "殺人の疑いが加わってから 4378件（全体の約3割）", J.AMBER, 30, INK))
    return s


# ══════════════════════════════════════════════════════════
#  share（c503）＝正面から見た100マス（1マス＝全体の1%）：情報1万3978件のうち「似た人を見た」約1万3240件＝9割をこえる
# ══════════════════════════════════════════════════════════
SH = dict(x0=300.0, y0=330.0, c=48.0, gap=6.0)
SH_V = (13978, 13240)


def sh_n():
    return int(round(SH_V[1] * 100 / SH_V[0]))


def _sh_cell(i):
    r, c = i // 10, i % 10
    return SH["x0"] + c * (SH["c"] + SH["gap"]), SH["y0"] + r * (SH["c"] + SH["gap"])


def share_base(st0):
    g = []
    for i in range(100):
        x, y = _sh_cell(i)
        g.append(F.rect(x, y, SH["c"], SH["c"], "none", J.LINE_DIM, 3, rx=4))
    g.append(_t(1260.0, 400.0, "寄せられた情報 1万3978件", 34, J.LINE, "middle", 760))
    return g


def share_stage(prev, st):
    s = []
    if _on(prev, st, "fill"):
        for i in range(sh_n()):
            x, y = _sh_cell(i)
            s.append(F.rect(x, y, SH["c"], SH["c"], sc("seen"), None, None, rx=4))
        s.append(_t(1260.0, 640.0, "9割をこえる", 72, sc("seen"), "middle", 700))   # 🔧 G-14：y560 は焼き込みの字（駅の案内）に載った
    if _on(prev, st, "seen"):
        s.append(_tag(1260.0, 760.0, "「似た人を見た」約1万3240件", sc("seen"), 36, INK))
    return s


# ══════════════════════════════════════════════════════════
#  verify（c508）＝横から見た流れ：目撃の情報の山 → 本人と確かめられたという報道＝調べた範囲では見当たらない・警察はすべて調べている
# ══════════════════════════════════════════════════════════
def verify_base(st0):
    g = []
    for i in range(6):
        g.append(_panel(260.0 + i * 16, 420.0 + i * 26, 300.0, 120.0, sc("seen"), sw=3))
    g.append(_t(410.0 + 80, 680.0, "似た人を見たという目撃", 30, sc("seen"), "middle", 460))
    g.append(_arrow(700.0, 540.0, 1040.0, 540.0, J.LINE, 7, 28))
    g.append(F.rect(1100.0, 420.0, 540.0, 240.0, "none", sc("news"), 5, rx=16, dash="16 12"))
    g.append(_t(1370.0, 400.0, "本人と確認された、という報道", 30, sc("news"), "middle", 600))
    return g


def verify_stage(prev, st):
    s = []
    if _on(prev, st, "none"):
        s.append(_t(1370.0, 540.0, "調べた範囲では", 34, INK, "middle", 480) + _t(1370.0, 600.0, "見当たらない", 40, J.ALERT, "middle", 480))
    if _on(prev, st, "all"):
        s.append(_glass(520.0, 790.0, 0.8, sc("police")))
        s.append(_tag(980.0, 800.0, "警察：寄せられた情報は全部調べる", sc("police"), 32, INK))
    return s


# ══════════════════════════════════════════════════════════
#  mistaken（c513）＝正面から見た人違い：「似ている」の吹き出しが広がる → のちに「別の人」と報道（顔や店の名前は出さない）
# ══════════════════════════════════════════════════════════
MS_B = ((420.0, 420.0), (300.0, 640.0), (640.0, 560.0))


def mistaken_base(st0):
    return [F.circ(1340.0, 560.0, 120, "none", J.LINE, 6, ) + _t(1340.0, 740.0, "関係の無い人", 32, J.LINE, "middle", 400)]


def mistaken_stage(prev, st):
    s = []
    if _on(prev, st, "talk"):
        for x, y in MS_B:
            s.append(_bubble(x, y, 260.0, 80.0, sc("seen"), "似ている", 32, INK))
        for x, y in MS_B:
            s.append(_dash_line(x + 130, y, 1210.0, 560.0, sc("seen"), 5, "6 14"))
        s.append(_tag(1340.0, 360.0, "のちに 別の人と報道", sc("news"), 32, INK))
    if _on(prev, st, "doubt"):
        s.append(_xmark(1340.0, 560.0, 70, J.ALERT, 14))
    return s


# ══════════════════════════════════════════════════════════
#  fake（c515）＝横から見た流れ：「捕まえた」のうその動画 → 関係の無い人が疑われる → 名誉毀損にあたる〈元検事の指摘〉（顔は描かない）
# ══════════════════════════════════════════════════════════
def fake_base(st0):
    return [_panel(250.0, 400.0, 460.0, 290.0, J.LINE), F.poly([(430.0, 480.0), (430.0, 610.0), (540.0, 545.0)], J.LINE, None, close=True),
            _t(480.0, 740.0, "「捕まえた」のうその動画", 32, J.ALERT, "middle", 520)]


def fake_stage(prev, st):
    s = []
    if _on(prev, st, "who"):
        s.append(_arrow(740.0, 545.0, 1120.0, 545.0, J.ALERT, 8, 30))
        s.append(F.circ(1300.0, 545.0, 110, "none", J.LINE, 6) + _t(1300.0, 712.0, "関係の無い人が疑われる", 32, INK, "middle", 520))
    if _on(prev, st, "law"):
        s.append(_tag(1300.0, 820.0, "名誉毀損にあたる（元検事の指摘）", sc("expert"), 32, INK))
    return s


# ══════════════════════════════════════════════════════════
#  SNS の声（c517・c518・c612）＝原文どおりの字をこちらの札に組み直す（アイコン・X の画面の作り・アカウント名は出さない）
# ══════════════════════════════════════════════════════════
#   🔴 札の字は原文どおり（門番の側 REC_M27 の sns に原文）・注釈は3画面とも同じ置き場（cuts.ss.SNS_NOTE・SNS_NOTE_BOX＝門番 check_ground）
SNS_CARDS = dict(
    k1=(("なんか八田與一にめっちゃ似てる人と", "すれ違ったんだけどたぶん違う"), "X の投稿（2026年10月29日）"),
    k3=(("関東で目撃情報が寄せられているから、", "重点的に調べるべきではないか"), "X の投稿（2026年10月25日）"),
    k4=(("八田與一容疑者、警察が海を捜索してるけど", "死んだ説が濃厚だと思う。"), "X の投稿（2026年10月22日）"),
)


def _sns_card(cx, cy, w, key, cap=42, op=None):
    lines, src = SNS_CARDS[key]
    lh = cap * 1.55
    h = 56 + lh * len(lines) + 60
    g = [F.rect(cx - w / 2, cy - h / 2, w, h, CARD, None, None, rx=22, op=op)]
    for i, ln in enumerate(lines):
        g.append(F.txtfit(cx - w / 2 + 48, cy - h / 2 + 36 + cap + i * lh, ln, w - 96, cap=cap, col=CARD_INK))
    g.append(F.txtfit(cx - w / 2 + 48, cy + h / 2 - 30, src, w - 96, cap=26, col=CARD_SUB))
    return "".join(g)


def _sns_note():
    import cuts.ss as ss
    y0, x1, y1 = ss.SNS_NOTE_BOX
    t = ss.SNS_NOTE
    cap = 30
    w = _w(t, cap) + 28
    return (F.rect(x1 - w, y0, w, y1 - y0, "#000000", None, None, rx=10)
            + F.txtfit(x1 - w + 14, y1 - 14, t, w - 20, cap=cap, col=ss.SNS_NOTE_INK))


def _sns_head(t):
    return _t(CX, 330.0, t, 32, J.LINE, "middle", 900)


def sns1_base(st0):
    return [_sns_note()]


def sns1_stage(prev, st):
    s = []
    if _on(prev, st, "head"):
        s.append(_sns_head("SNS の声（原文どおり）"))
    if _on(prev, st, "k1"):
        s.append(_sns_card(CX, 560.0, 1300.0, "k1", 50))
    return s


def sns13_base(st0):
    return [_sns_note(), _sns_head("SNS の声（原文どおり）"), _sns_card(560.0, 480.0, 820.0, "k1", 32, op=0.82)]


def sns13_stage(prev, st):
    s = []
    if _on(prev, st, "kanto"):
        s.append(_tag(1370.0, 410.0, "関東での目撃について", J.LINE, 30, INK))
    if _on(prev, st, "k3"):
        s.append(_sns_card(1370.0, 620.0, 820.0, "k3", 34))
    return s


def sns4_base(st0):
    return [_sns_note()]


def sns4_stage(prev, st):
    s = []
    if _on(prev, st, "k4"):
        s.append(_sns_head("SNS の声（原文どおり）"))
        s.append(_sns_card(CX, 470.0, 1360.0, "k4", 46))
    if _on(prev, st, "q"):
        s.append(_qmark(CX, 740.0, 96))
    return s


# ══════════════════════════════════════════════════════════
#  detective（c519）＝正面から見た元刑事の札：声をかけない・追い詰めない・すぐに110番／「違っていたからといって怒られるわけじゃない」
# ══════════════════════════════════════════════════════════
DT = ("声をかけない", "追い詰めない", "すぐに110番")
DT_Q = "違っていたからといって怒られるわけじゃない"
DT_X = (520.0, 960.0, 1400.0)


def detective_base(st0):
    return []


def detective_stage(prev, st):
    s = []
    if _on(prev, st, "three"):
        for x, t in zip(DT_X, DT):
            s.append(_tag(x, 380.0, t, sc("police") if "110" in t else J.LINE, 36, INK))
    if _on(prev, st, "quote"):
        s.append(_panel(400.0, 510.0, 1120.0, 132.0, sc("expert"), sw=5))
        s.append(_t(424.0, 590.0, "“", 70, sc("expert"), "start", 60))
        s.append(_t(CX, 578.0, DT_Q, 44, INK, "middle", 1000))
        s.append(_t(1500.0, 626.0, "元刑事（NEWSポストセブン 2026年10月25日）", 24, sc("expert"), "end", 800))
    if _on(prev, st, "call"):
        s.append(F.rect(DT_X[2] - 170, 340.0, 340.0, 80.0, "none", J.AMBER, 7, rx=14))
        s.append(_arrow(DT_X[2], 430.0, DT_X[2], 470.0, J.AMBER, 6, 20))
        s.append(_tag(CX, 790.0, "自分で捕まえず、警察へ", sc("police"), 34, INK))
    return s


# ══════════════════════════════════════════════════════════
#  第6章  road500（c605）＝上から見た手前の道：店の防犯カメラ → 約500m → 交差点（店の位置は描かない＝道のりだけ）
# ══════════════════════════════════════════════════════════
RD = dict(y=600.0, cam=440.0, cross=1460.0)


def road500_base(st0):
    y = RD["y"]
    return [F.rect(200.0, y - 50, 1520.0, 100.0, J.BG2, J.LINE, 4, op=0.7),
            F.line(220.0, y, 1700.0, y, J.LINE_DIM, 4, dash="30 22"),
            F.rect(RD["cross"] - 50, y - 210, 100.0, 420.0, J.BG2, J.LINE, 4, op=0.7),
            _t(RD["cross"] + 70, y - 150, "現場の交差点", 30, INK, "start", 300)]


def road500_stage(prev, st):
    s = []
    y = RD["y"]
    if _on(prev, st, "cam"):
        s.append(_cam(RD["cam"], y - 140, 1.0, sc("police")))
        s.append(_t(RD["cam"], y - 222, "店の防犯カメラ", 30, sc("police"), "middle", 320))
        s.append(_tag(RD["cam"] + 60, 340.0 - 40, "2026年6月29日 映像を公開", J.AMBER, 30, INK))
    if _on(prev, st, "dist"):
        a, b = RD["cam"], RD["cross"] - 60
        s.append(F.line(a, y + 110, b, y + 110, J.AMBER, 5) + F.line(a, y + 90, a, y + 130, J.AMBER, 5) + F.line(b, y + 90, b, y + 130, J.AMBER, 5))
        s.append(_t((a + b) / 2, y + 170, "約500メートル（道のり）", 34, J.AMBER, "middle", 700))
    if _on(prev, st, "flyer"):
        # 🔧 ⑤c'：中心 x1240 では札の右の端が交差点の縦の道（x1410〜1510）に 4.5px 重なった（geom_gap）＝左へ 60px
        s.append(_tag(1180.0, 820.0, "チラシ配り：11の都道府県", sc("police"), 30, INK))
    return s


# ══════════════════════════════════════════════════════════
#  one_min（c606）＝時間の線（2つの印）：友人のバイクが通る → 約1分後に容疑者の車が通る（時刻は描かない）
# ══════════════════════════════════════════════════════════
OM = dict(y=560.0, a=600.0, b=1320.0)


def one_min_base(st0):
    return [_arrow(240.0, OM["y"], 1720.0, OM["y"], J.LINE, 6, 28), _t(1700.0, OM["y"] + 50, "時間", 26, J.TICK, "end", 140)]


def one_min_stage(prev, st):
    s = []
    y = OM["y"]
    if _on(prev, st, "two"):
        s.append(F.line(OM["a"], y - 80, OM["a"], y + 80, sc("moto"), 8) + _bike(OM["a"], y - 150, 0.5, sc("moto"), big=True))
        s.append(_t(OM["a"], y + 130, "友人のバイクが通る", 32, sc("moto"), "middle", 420))
        s.append(F.line(OM["b"], y - 80, OM["b"], y + 80, sc("car"), 8) + _car_side(OM["b"], y - 96, 140.0, sc("car")))
        s.append(_t(OM["b"], y + 130, "容疑者の車が写っていた", 32, sc("car"), "middle", 460))
        s.append(_brace_h(OM["a"], OM["b"], y - 230, J.AMBER, up=True, t="約1分後", cap=38))
    if _on(prev, st, "first"):
        s.append(_tag(CX, 790.0, "車が走る映像の公開は 初めて", J.AMBER, 32, INK))
    return s


# ══════════════════════════════════════════════════════════
#  calendar（c607）＝正面から見た、めくりの暦：2026年9月 延長／国の報奨金の受付 2026年11月1日〜2027年10月31日（上限300万円）／遺族らの懸賞金 〜2026年11月30日
# ══════════════════════════════════════════════════════════
CA = dict(y=560.0, w=260.0, h=250.0)


def calendar_base(st0):
    return []


def calendar_stage(prev, st):
    s = []
    y, w, h = CA["y"], CA["w"], CA["h"]
    if _on(prev, st, "sep"):
        s.append(_page(330.0, y, w, h, "2026年", "9月", J.LINE))
        s.append(_t(330.0, y + h / 2 + 46, "重要指名手配が続く", 28, INK, "middle", 320))
        s.append(_t(330.0, y + h / 2 + 84, "報奨金も1年延長", 28, INK, "middle", 320))
    if _on(prev, st, "kuni"):
        s.append(_page(860.0, y, w, h, "2026年11月", "1日", sc("kuni")))
        s.append(_page(1560.0, y, w, h, "2027年10月", "31日", sc("kuni")))
        s.append(_arrow(1000.0, y, 1420.0, y, sc("kuni"), 8, 30))
        s.append(_t(1210.0, y - 40, "国の報奨金の受付", 30, sc("kuni"), "middle", 400))
        s.append(_t(1210.0, y + 54, "上限300万円", 30, INK, "middle", 400))
    if _on(prev, st, "family"):
        s.append(_tag(1210.0, 830.0, "遺族らの懸賞金 いまの決まりでは2026年11月30日まで", sc("family"), 28, INK))
    return s


# ══════════════════════════════════════════════════════════
#  post（c615）＝正面から見た、県警の X の固定の投稿の文の札（投稿の画面は使わない）
# ══════════════════════════════════════════════════════════
PS_Q = "あなたのそばに潜んでいるかも。"


def post_base(st0):
    return []


def post_stage(prev, st):
    s = []
    if _on(prev, st, "near"):
        s.append(_tag(CX, 360.0, "警察は「そばにいる可能性」をくり返し呼びかけ", sc("police"), 32, INK))
    if _on(prev, st, "quote"):
        s.append(_panel(440.0, 480.0, 1040.0, 140.0, sc("police"), sw=6, rx=40))
        s.append(F.poly([(600.0, 618.0), (560.0, 690.0), (680.0, 618.0)], J.BG2, sc("police"), 5, op=PANEL_OP))
        s.append(_t(CX, 560.0, PS_Q, 56, INK, "middle", 960))
        s.append(_t(1440.0, 604.0, "大分県警察 公式X（2026年6月29日）", 24, sc("police"), "end", 700))
    return s


# ══════════════════════════════════════════════════════════
#  第7章  contact（c701）＝正面から見た窓口の札：別府警察署（代表 0977-21-2131）・ホームページの匿名の窓口・緊急は110番・秘密は守られる・匿名は報奨金の対象外
# ══════════════════════════════════════════════════════════
CT_TEL = "0977-21-2131"


def contact_base(st0):
    return [_panel(220.0, 300.0, 1480.0, 520.0, sc("police"), sw=5)]


def contact_stage(prev, st):
    s = []
    if _on(prev, st, "where"):
        s.append(_phone(320.0, 400.0, 0.7, sc("police")) + _t(380.0, 396.0, "別府警察署（代表）", 32, sc("police"), "start", 500)
                 + _t(380.0, 446.0, CT_TEL, 44, INK, "start", 500))
        s.append(_glass(1000.0, 398.0, 0.5, sc("police")) + _t(1060.0, 396.0, "ホームページ（大分県警察）", 32, sc("police"), "start", 600)
                 + _t(1060.0, 446.0, "匿名の窓口", 36, INK, "start", 600))
    if _on(prev, st, "rules"):
        s.append(F.line(260.0, 520.0, 1660.0, 520.0, J.LINE_DIM, 3))
        s.append(_t(300.0, 590.0, "緊急（目の前で似た人を見たなど）は", 30, INK, "start", 700) + _t(1020.0, 594.0, "110番", 44, J.AMBER, "start", 300))
        s.append(_t(300.0, 660.0, "情報を寄せた人の秘密は守られる", 30, INK, "start", 800))
        s.append(_t(300.0, 720.0, "匿名の情報は報奨金の対象外", 30, J.TICK, "start", 800))
    if _on(prev, st, "small"):
        s.append(_tag(1320.0, 700.0, "小さな情報でも", J.AMBER, 34, INK))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表（mech26 と同じ作り）
# ══════════════════════════════════════════════════════════
def _v(lab, fields, base, stage):
    return dict(lab=lab, fields={f_: ONOFF for f_ in fields}, base=base, stage=stage)


VIEWS = dict(
    bignum=_v("正面から見た大きな数", ("num", "clue"), bignum_base, bignum_stage),
    bikes2=_v("横から見た2台", ("q", "pair", "mini", "moto"), bikes2_base, bikes2_stage),
    crash=_v("横から見た坂と交差点", ("hit", "pole"), crash_base, crash_stage),
    flee=_v("上から見た、止まった車と点線", ("run", "bare"), flee_base, flee_stage),
    talk=_v("時間の線（やり取り）", ("say", "band"), talk_base, talk_stage),
    speed=_v("横の棒（時速）", ("lim", "fast"), speed_base, speed_stage),
    trail=_v("上から見た、途切れる点線", ("dna",), trail_base, trail_stage),
    hitrun3=_v("正面から見た3つの記号", ("three",), hitrun3_base, hitrun3_stage),
    items4=_v("正面から見た公表の札", ("items", "area"), items4_base, items4_stage),
    wanted=_v("正面から見た全国の警察", ("fan", "first"), wanted_base, wanted_stage),
    reward=_v("横の積み棒（金額）", ("kuni", "who", "family"), reward_base, reward_stage),
    steps5=_v("時間の線（手配の歩み）", ("pts", "span"), steps5_base, steps5_stage),
    charge2=_v("時間の線（縦・罪の名前）", ("q", "old", "one"), charge2_base, charge2_stage),
    complaint=_v("横から見た告訴の流れ", ("file",), complaint_base, complaint_stage),
    charges2=_v("正面から見た2つの疑い", ("date", "warrant", "two"), charges2_base, charges2_stage),
    warrant=_v("横から見た逮捕状の流れ", ("notyet", "court", "pres"), warrant_base, warrant_stage),
    basis6=_v("正面から見た6つの箱", ("all", "speed", "brake"), basis6_base, basis6_stage),
    limit=_v("横の棒（時効の年）", ("bars", "none"), limit_base, limit_stage),
    courts2=_v("正面から見た2つの部屋", ("civil",), courts2_base, courts2_stage),
    cumline=_v("時間の線（情報の累計）", ("q", "ends", "line"), cumline_base, cumline_stage),
    monthly=_v("縦の棒（月ごとの件数）", ("y23", "later", "share"), monthly_base, monthly_stage),
    share=_v("正面から見た100マス（1マス＝1%）", ("fill", "seen"), share_base, share_stage),
    verify=_v("横から見た確かめの流れ", ("none", "all"), verify_base, verify_stage),
    mistaken=_v("正面から見た人違い", ("talk", "doubt"), mistaken_base, mistaken_stage),
    fake=_v("横から見たうその動画の流れ", ("who", "law"), fake_base, fake_stage),
    sns1=_v("SNS の投稿（原文どおりの字を札に）", ("head", "k1"), sns1_base, sns1_stage),
    sns13=_v("SNS の投稿（原文どおりの字を札に）", ("kanto", "k3"), sns13_base, sns13_stage),
    detective=_v("正面から見た元刑事の言葉の札", ("three", "quote", "call"), detective_base, detective_stage),
    road500=_v("上から見た現場の手前の道", ("cam", "dist", "flyer"), road500_base, road500_stage),
    one_min=_v("時間の線（約1分）", ("two", "first"), one_min_base, one_min_stage),
    calendar=_v("正面から見た、めくりの暦", ("sep", "kuni", "family"), calendar_base, calendar_stage),
    sns4=_v("SNS の投稿（原文どおりの字を札に）", ("k4", "q"), sns4_base, sns4_stage),
    post=_v("正面から見た県警の投稿の文の札", ("near", "quote"), post_base, post_stage),
    contact=_v("正面から見た情報提供の窓口", ("where", "rules", "small"), contact_base, contact_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
# 値に比例・原文の字の写し・窓口の札（左上に「模式」を付けない）
NOT_SCHEMATIC = ("bignum", "talk", "speed", "reward", "steps5", "charge2", "limit", "cumline", "monthly", "share",
                 "items4", "basis6", "sns1", "sns13", "sns4", "detective", "calendar", "post", "contact", "one_min")
SNS_VIEWS = ("sns1", "sns13", "sns4")


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
                raise ValueError(f"m27：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m27：{f_}={v!r} は知らない値（{fields[f_]}）")
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


_TEXT = re.compile(r"<text\s[^>]*>([^<]*)</text>")


def svg_texts(svg):
    """SVG の <text> の中身（門番が全部の字から数を拾う）。"""
    return [t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">") for t in _TEXT.findall(svg)]


QUOTE_VIEWS = dict(sns1=("k1",), sns13=("k1", "k3"), sns4=("k4",))


def quote_lines(view):
    """原文どおりに大きく出す字（門番 echo の例外＝その行の字幕は SPEC の mute で消す）。"""
    if view in QUOTE_VIEWS:
        return [ln for k in QUOTE_VIEWS[view] for ln in SNS_CARDS[k][0]]
    return {"detective": [DT_Q], "post": [PS_Q]}.get(view, [])


def m27(view, steps, start=None, rel=(), note="", src="", mute=()):
    """27本目の図解。view は VIEWS の見え方。steps＝ナレーションの行ごとの段。
    mute＝原文どおりの字を大きく出す札の字を読む行（字幕を消す＝scene_jiko.SUB_MUTE）。"""
    if quote_lines(view) and not mute:
        raise ValueError(f"m27：{view} は原文どおりの字を大きく出す＝その字を読む行を mute に書く（字幕と二重に出さない）")
    if view not in VIEWS:
        raise ValueError(f"m27：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view not in NOT_SCHEMATIC and "模式" not in note:
        raise ValueError("m27：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    g = _base(view, st0)
    lab = lab_of(view, st0)
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, lab + ("" if view in NOT_SCHEMATIC else "・模式"), 1000, cap=30, col=J.TICK, ol=OL))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW * 0.86 if view in SNS_VIEWS else F.BW,
                      cap=26, col=J.TICK, ol=OL))
    stages = _stage_svgs(view, steps, st0, states)
    base_svg = "".join(g)
    f = F.Fig(base_svg, stages, "", (F.BX0, F.BX1))
    f.moves = []
    body = "".join(g[:-2]) + "".join(stages)
    f.mech = dict(kind="m27", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=[], lab=lab, note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states), texts_all=svg_texts(body),
                  sns=bool(view in SNS_VIEWS))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M27）
# ══════════════════════════════════════════════════════════
VIEW_SRC = dict(bignum=("police",), bikes2=("mini", "moto"), crash=("mini", "moto", "car"), flee=("car",), speed=(), trail=("news",),
                hitrun3=("police",), items4=("police",), wanted=("npa", "police"), reward=("kuni", "family"), steps5=("police",),
                charge2=("police",), complaint=("family", "police"), charges2=("court",), warrant=("court", "police"), basis6=("news",),
                courts2=("court", "civil"), monthly=("kuni",), share=("seen",), verify=("seen", "news", "police"), mistaken=("seen", "news"),
                fake=("expert",), detective=("police", "expert"), road500=("police",), one_min=("moto", "car"), calendar=("kuni", "family"),
                post=("police",), contact=("police",))


def _geo(view, allst):
    if view == "bignum":
        return dict(val=BN_V)
    if view == "talk":
        return dict(val=TK_S, px=tuple(tk_x(v) for v in TK_S), lins=((TK["x0"], TK["k"], 0.0),) * 2)
    if view == "speed":
        return dict(val=SP_V, px=tuple(sp_x(v) for v in SP_V), lins=((SP["x0"], SP["k"], 0.0),) * len(SP_V))
    if view == "reward":
        return dict(val=(RW_V, RW_V[0] + RW_V[1] == RW_V[2]), px=tuple(rw_x(v) for v in RW_V), lins=((RW["x0"], RW["k"], 0.0),) * 3)
    if view == "steps5":
        k = (ST["x1"] - ST["x0"]) / (_mi(ST["m1"]) - _mi(ST["m0"]))
        return dict(val=tuple((f"{ym[0]}年{ym[1]}月", lab) for ym, lab in ST_EV), px=tuple(st_x(ym) for ym, _l in ST_EV),
                    lins=((ST["x0"], k, float(_mi(ST["m0"]))),) * len(ST_EV), mons=tuple(float(_mi(ym)) for ym, _l in ST_EV))
    if view == "limit":
        return dict(val=(LM_V,), px=(LM["x0"] + LM_V * LM["k"],), lins=((LM["x0"], LM["k"], 0.0),))
    if view == "cumline":
        kx = (CL["x1"] - CL["x0"]) / _days(CL["d1"])
        return dict(val=tuple((when, v) for _d, v, _l, when in CL_PTS),
                    px=tuple(cl_y(v) for _d, v, _l, _w in CL_PTS), lins=((CL["y0"], -CL["k"], 0.0),) * len(CL_PTS),
                    pxx=tuple(cl_x(d) for d, *_r in CL_PTS), linx=((CL["x0"], kx, 0.0),) * len(CL_PTS),
                    days=tuple(float(_days(d)) for d, *_r in CL_PTS))
    if view == "monthly":
        return dict(val=tuple((lab, v) for lab, v, _n, _t2 in MO_V), px=tuple(mo_top(v) for _l, v, _n, _t2 in MO_V),
                    lins=((MO["y0"], -MO["k"], 0.0),) * len(MO_V))
    if view == "share":
        return dict(val=(SH_V, sh_n()))
    if view in SNS_VIEWS:
        return dict(val=tuple((k, SNS_CARDS[k][0], SNS_CARDS[k][1]) for k in sorted(SNS_CARDS)))
    if view == "detective":
        return dict(val=(DT, DT_Q))
    if view == "post":
        return dict(val=(PS_Q,))
    if view == "contact":
        return dict(val=(CT_TEL,))
    return {}


def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst], src={k: tuple(v) for k, v in SRC.items()}, vsrc=tuple(VIEW_SRC.get(view, ())))
    out.update(_geo(view, allst))
    return out
