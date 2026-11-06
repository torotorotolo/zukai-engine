# -*- coding: utf-8 -*-
"""mech30.py — 30本目（地下鉄サリン事件・1995-03-20・事件の回の4本目）「札の型」（2026-11-05 新設・⑤b-4＝札 76＋言葉のカード 11＝87カット）。

■ 何か
  映像方針 §5-4 の「札の型」＝**見出し＋札1〜4枚＋矢印0〜2本＋誰の記録かの色＝描き手1つ**。カットごとの関数は書かない＝表 `FU` の1行が1カット。
  mech29 までと同じ「段の層（その行から出て残る）＋動く部品は使わない」。再現イラストではない＝「再現」の札は出さない。
  🔴 **地は写真**（`cuts.ss.gr`＝暗くするだけ・方眼と章の色なし・静止）＝字は暗い縁取り（OL）・札の地は半ば透ける紺（`_panel`）。8:1 は check_ground。
  🔴 この回の線（ルール §B2-12）に当たることは札に書かない＝物質の名・まいた場所の直前の駅ほか（語の一覧は git の外の網）。語りは「猛毒の神経ガス」「症状と治療」まで。
  🔴 名前＝札に出すのは教祖だけ（本名は c210 だけ）・ほかは立場だけ・団体名は「アレフ」だけ。**人の形・家・顔を描かない**（印の服は平らに置いた形・頭なし）。
  🔴 「分かっていたのに放置」も「防ぎようがなかった」も言い切らない／「警察が犯人扱いした」と言い切らない＝札の並べ方でも組み上げない（c409・c410 は第一通報者へ矢印を引かない）。
  🔴 **色は「誰の記録か」**（SRC＝新しい色の値は足していない）：白書＝青／判決＝紫／国会＝緑／手記＝桃／公安調査庁＝水色／無線＝橙／ほかの国の資料と聞き取り＝茶。
     意味の色＝黄 AMBER（数・日付・時刻）。誰のものでもない札は線の色。噂の札（ca09）だけ灰色＝事実の図と違う見た目。
  🔴 札の中の数字と原文どおりの字（`q=True`＝「」が付く）は門番の側 `check_mech.REC_M30` が別に持つ（§5b-88）＝描く側の表を書き換えると鳴る。
     原文との照合は `ref/ep30/eizou_build/rec30_src.py`（git の外の資料を読む＝手元だけ・抜き書きのファイルは作らない）。字数と字の大きさは `tools/check_fuda.py`。

■ 表の書き方
  `FU["c305"] = _f(2, "見出し", "副題", [_c(at=0, who=H, head="…", big="…", lines=("…",), cell=(0, 0)), …], [_x(1, "a", "b", t="…")], src="…")`
    先頭の数 … 段の数＝語りの行の数（行より多いと行の間に等間隔で挟む＝scene_jiko.stage_times）
    at    … その札が出る段（語りの行の番号）。札の id は書いた順に a・b・c…／矢印は x・y
    cell  … 格子の場所（列, 行）・span＝（列の数, 行の数）。列の幅と行の高さは中身の字で決まる（枠の中を空けない＝門番 box）
    mute  … 札の原文を読む行（字幕を消す＝feedback-no-subtitle-when-onscreen）。mute があるカットの `q=True` の字だけ門番 echo の例外
  SPEC は `"c305": fu_spec("c305", ss.gr("stock/ga1"))`。

■ 🆕 ⑤b-5（2026-11-06）：見え方の表 `VIEWS`（札の型の表に無いカット＝無線帯 8・模式の前半 11）
  1行が1カット＝札（`_c` のまま・置き場は格子でなく真ん中の座標 `_at`）＋絵の部品（`_p`＝その段から出て残る）。描く部品も門番が測る形も札の型と同じ。
  無線帯（c714〜c734）は描き手1つ（`_rb_view`）＝同じ帯が段ごとに伸びる・前の段は時刻と短い語で残る・その段の時刻から右の札へ線。
  模式（`schem=True`）は左上に「模式」・note にも「模式」。時間の線（c307・c407・c514）は比例＝門番 judge_m30 の ⑤ が位置と字の値を測る。
  SPEC は `"c714": zu_spec("c714", ss.gr("ks1"))`。
"""
from __future__ import annotations

import math
import re

import jiko_style as J
import titan_fig as F
from mech21 import _arrow, _on, _qmark, _xmark
from mech24 import _w, rc
from mech27 import CX, INK, OL, ONOFF, _panel, _phone, _t, svg_texts

# 誰の記録か（名・ROLE か J の名）。同じ色の鍵は同じ画面に出さない（門番が見る）
SRC = dict(
    hakusho=("白書", "uscg"),
    hanketsu=("判決", "tsb"),
    kokkai=("国会", "ntsb"),
    shuki=("手記", "bldg_a"),
    kouan=("公安調査庁", "ship"),
    musen=("無線", "company"),
    doc=("ほかの国の資料", "DOC"),
)
GRAY_FILL = "#34383c"       # 噂の札の地（事実の図と違う見た目）
GRAY_LINE = "#9aa1a6"
GRAY_INK = "#d2d6d9"

HEAD_CAP, BODY_CAP, BIG_CAP, SUB_CAP = 32.0, 50.0, 92.0, 32.0
LH = dict(head=1.42, body=1.36, big=1.12, sub=1.40)
PX, PY = 34.0, 20.0
ICON_W, ICON_H = 150.0, 136.0
YC = 534.0                  # 札のまとまりの真ん中の高さ（左下の注の行と左上の見出しの間）
AREA_W, AREA_H = F.BW, 610.0
FIT_W, FIT_H, KMAX = 1620.0, 560.0, 1.5


def sc(key):
    return rc(SRC[key][1]) if key else J.LINE


def _f(n, t, s, cards, arrows=(), src="", note="", mute=(), gx=None, gy=None):
    """1カット。t・s＝見出しと副題（札の字と重ねない＝門番 dup）・src＝左下の出典の行。"""
    cs = []
    for i, c in enumerate(cards):
        cs.append(dict(c, id="abcdefgh"[i]))
    xs = []
    for i, a in enumerate(arrows):
        xs.append(dict(a, id="xyzw"[i]))
    return dict(n=n, t=t, s=s, cards=tuple(cs), arrows=tuple(xs), src=src, note=note, mute=tuple(mute), gx=gx, gy=gy)


def _c(at=0, who=None, lines=(), head=None, big=None, sub=(), q=False, icon=None, cell=(0, 0), span=(1, 1), dim=False, gray=False, cap=BODY_CAP, bcap=BIG_CAP, cross=False):
    """札1枚。head＝誰の記録か（色の字）・big＝数と日付（黄）・lines＝本文・sub＝小さい字・q＝原文どおり（「」を付ける）・icon＝左の印。"""
    if isinstance(lines, str):
        lines = (lines,)
    if isinstance(sub, str):
        sub = (sub,)
    return dict(at=at, who=who, lines=tuple(lines), head=head, big=big, sub=tuple(sub), q=q, icon=icon, cell=cell, span=span, dim=dim, gray=gray,
                cap=cap, bcap=bcap, cross=cross)


def _x(at=0, a="a", b="b", t=None, q=False, ng=False, dash=False, who=None, head=True):
    """矢印1本（札 a から札 b へ）。t＝矢印の上の字・q＝？・ng＝×・head=False は線だけ。"""
    return dict(at=at, a=a, b=b, t=t, q=q, ng=ng, dash=dash, who=who, head=head)


def _qwrap(lines):
    if not lines:
        return ()
    ls = list(lines)
    ls[0] = "「" + ls[0]
    ls[-1] = ls[-1] + "」"
    return tuple(ls)


def _rows(c, k=1.0):
    out = []
    if c["head"]:
        out.append(("head", c["head"], HEAD_CAP * k))
    if c["big"]:
        out.append(("big", c["big"], c["bcap"] * k))
    for ln in (_qwrap(c["lines"]) if c["q"] else c["lines"]):
        out.append(("body", ln, c["cap"] * k))
    for ln in c["sub"]:
        out.append(("sub", ln, SUB_CAP * k))
    return out


def _size(c, k=1.0):
    rows = _rows(c, k)
    cw = max((_w(t, cap) for _k, t, cap in rows), default=0.0)
    ch = sum(cap * LH[kd] for kd, _t2, cap in rows)
    if c["icon"]:
        cw += (ICON_W + 22) * k
        ch = max(ch, ICON_H * k)
    return cw + 2 * PX * k, ch + 2 * PY * k


def _card_of(fu, cid):
    return next(c for c in fu["cards"] if c["id"] == cid)


def _same_row(fu, a):
    ca, cb = _card_of(fu, a["a"]), _card_of(fu, a["b"])
    r0a, r1a = ca["cell"][1], ca["cell"][1] + ca["span"][1]
    r0b, r1b = cb["cell"][1], cb["cell"][1] + cb["span"][1]
    return r0a < r1b and r0b < r1a


def _grid(fu, k):
    cards = fu["cards"]
    ncol = max(c["cell"][0] + c["span"][0] for c in cards)
    nrow = max(c["cell"][1] + c["span"][1] for c in cards)
    harrow = any(_same_row(fu, a) for a in fu["arrows"])
    varrow = any(not _same_row(fu, a) for a in fu["arrows"])
    gx = (fu["gx"] if fu["gx"] is not None else (170.0 if harrow else 56.0)) * k
    gy = (fu["gy"] if fu["gy"] is not None else (84.0 if varrow else 30.0)) * k
    colw, rowh = [0.0] * ncol, [0.0] * nrow
    for c in cards:
        w, h = _size(c, k)
        if c["span"][0] == 1:
            colw[c["cell"][0]] = max(colw[c["cell"][0]], w)
        if c["span"][1] == 1:
            rowh[c["cell"][1]] = max(rowh[c["cell"][1]], h)
    for c in cards:
        w, h = _size(c, k)
        if c["span"][0] > 1:
            have = sum(colw[c["cell"][0]:c["cell"][0] + c["span"][0]]) + gx * (c["span"][0] - 1)
            if w > have:
                add = (w - have) / c["span"][0]
                for i in range(c["cell"][0], c["cell"][0] + c["span"][0]):
                    colw[i] += add
        if c["span"][1] > 1:
            have = sum(rowh[c["cell"][1]:c["cell"][1] + c["span"][1]]) + gy * (c["span"][1] - 1)
            if h > have:
                add = (h - have) / c["span"][1]
                for i in range(c["cell"][1], c["cell"][1] + c["span"][1]):
                    rowh[i] += add
    tw = sum(colw) + gx * (ncol - 1)
    th = sum(rowh) + gy * (nrow - 1)
    x0, y0 = CX - tw / 2, YC - th / 2
    boxes = {}
    for c in cards:
        cc, rr = c["cell"]
        cs, rs = c["span"]
        x = x0 + sum(colw[:cc]) + gx * cc
        y = y0 + sum(rowh[:rr]) + gy * rr
        cw, rh = sum(colw[cc:cc + cs]) + gx * (cs - 1), sum(rowh[rr:rr + rs]) + gy * (rs - 1)
        w, h = _size(c, k)
        # 🔴 枠の高さは中身の高さ（行の真ん中に置く）・列をまたぐ札の幅も中身の幅＝枠の中を空けない（門番 box）
        if cs > 1:
            x, cw = x + (cw - w) / 2, w
        boxes[c["id"]] = (x, y + (rh - h) / 2, cw, h)
    return boxes, (x0, y0, tw, th)


def layout(fu):
    """札ごとの箱 {id: (x, y, w, h)}・まとまりの箱・拡大率。列の幅と行の高さは中身の字で決まる＝同じ列の札は幅が揃う。
    🔴 拡大率 k＝札のまとまりが画面の FIT_W×FIT_H に収まるいちばん大きい倍率（KMAX まで）＝札が少ないカットほど字が大きい。"""
    _b, (_x0, _y0, tw, th) = _grid(fu, 1.0)
    k = min(FIT_W / tw, FIT_H / th, KMAX)
    boxes, bb = _grid(fu, k)
    return boxes, bb, k


# ══════════════════════════════════════════════════════════
#  印（人の形・顔・家は描かない＝線と四角だけ。ICON_W×ICON_H に収まる）
# ══════════════════════════════════════════════════════════
def _i_phone(cx, cy, col):
    return _phone(cx, cy, 1.05, col)


def _i_book(cx, cy, col):
    return (F.poly([(cx, cy - 34), (cx - 62, cy - 50), (cx - 62, cy + 42), (cx, cy + 58)], J.BG2, col, 6, close=True)
            + F.poly([(cx, cy - 34), (cx + 62, cy - 50), (cx + 62, cy + 42), (cx, cy + 58)], J.BG2, col, 6, close=True)
            + "".join(F.line(cx + 14, cy - 22 + i * 26, cx + 48, cy - 30 + i * 26, col, 4) for i in range(3)))


def _i_glass(cx, cy, col):
    return F.circ(cx - 14, cy - 14, 42, J.BG2, col, 8) + F.line(cx + 16, cy + 16, cx + 56, cy + 56, col, 11)


def _i_globe(cx, cy, col):
    r = 58
    g = F.circ(cx, cy, r, J.BG2, col, 6) + F.line(cx - r, cy, cx + r, cy, col, 4) + F.line(cx, cy - r, cx, cy + r, col, 4)
    g += F.poly([(cx - 24, cy - 53), (cx - 34, cy - 24), (cx - 36, cy), (cx - 34, cy + 24), (cx - 24, cy + 53)], "none", col, 4)
    g += F.poly([(cx + 24, cy - 53), (cx + 34, cy - 24), (cx + 36, cy), (cx + 34, cy + 24), (cx + 24, cy + 53)], "none", col, 4)
    return g + F.line(cx - 48, cy - 30, cx + 48, cy - 30, col, 4) + F.line(cx - 48, cy + 30, cx + 48, cy + 30, col, 4)


def _i_radio(cx, cy, col):
    return (F.rect(cx - 36, cy - 30, 72, 88, J.BG2, col, 6, rx=8) + F.line(cx + 20, cy - 30, cx + 20, cy - 66, col, 7)
            + F.circ(cx, cy - 6, 12, "none", col, 4) + "".join(F.line(cx - 22, cy + 18 + i * 14, cx + 22, cy + 18 + i * 14, col, 4) for i in range(3)))


def _i_payphone(cx, cy, col):
    return (F.rect(cx - 44, cy - 62, 88, 124, J.BG2, col, 6, rx=8) + F.rect(cx - 12, cy - 46, 42, 26, "none", col, 4, rx=3)
            + F.line(cx - 28, cy - 46, cx - 28, cy + 8, col, 8)
            + "".join(F.circ(cx - 4 + (i % 3) * 14, cy - 6 + (i // 3) * 16, 3.5, col) for i in range(9)))


def _i_suit(cx, cy, col):
    """防護服の形（平らに置いた形・頭と顔なし）。"""
    return F.poly([(cx - 20, cy - 62), (cx + 20, cy - 62), (cx + 66, cy - 40), (cx + 66, cy + 6), (cx + 42, cy + 6), (cx + 42, cy - 16), (cx + 34, cy - 16),
                   (cx + 34, cy + 62), (cx + 6, cy + 62), (cx, cy + 14), (cx - 6, cy + 62), (cx - 34, cy + 62), (cx - 34, cy - 16), (cx - 42, cy - 16),
                   (cx - 42, cy + 6), (cx - 66, cy + 6), (cx - 66, cy - 40)], J.BG2, col, 6, close=True)


def _i_car(cx, cy, col):
    """車の形（車種を描かない）。"""
    return (F.poly([(cx - 70, cy + 24), (cx - 70, cy - 6), (cx - 42, cy - 8), (cx - 22, cy - 40), (cx + 34, cy - 40), (cx + 54, cy - 8), (cx + 70, cy - 2), (cx + 70, cy + 24)],
                   J.BG2, col, 6, close=True)
            + F.circ(cx - 38, cy + 28, 15, J.BG2, col, 6) + F.circ(cx + 38, cy + 28, 15, J.BG2, col, 6))


def _i_mask(cx, cy, col):
    """防毒マスクの形（中に顔を描かない）。"""
    return (F.poly([(cx - 36, cy - 58), (cx + 36, cy - 58), (cx + 56, cy - 26), (cx + 44, cy + 24), (cx - 44, cy + 24), (cx - 56, cy - 26)], J.BG2, col, 6, close=True)
            + F.circ(cx - 24, cy - 22, 15, "none", col, 5) + F.circ(cx + 24, cy - 22, 15, "none", col, 5)
            + F.circ(cx, cy + 44, 22, J.BG2, col, 6) + F.line(cx - 10, cy + 44, cx + 10, cy + 44, col, 4))


def _i_speaker(cx, cy, col):
    g = F.poly([(cx - 52, cy - 20), (cx - 22, cy - 20), (cx + 6, cy - 46), (cx + 6, cy + 46), (cx - 22, cy + 20), (cx - 52, cy + 20)], J.BG2, col, 6, close=True)
    for r in (26, 48):
        g += F.poly([(cx + 10 + r * 0.72, cy - r * 0.72), (cx + 10 + r, cy), (cx + 10 + r * 0.72, cy + r * 0.72)], "none", col, 5)
    return g


def _i_eye(cx, cy, col):
    """目の模式（瞳だけ小さい・顔は描かない）。"""
    return (F.poly([(cx - 70, cy), (cx - 40, cy - 30), (cx, cy - 42), (cx + 40, cy - 30), (cx + 70, cy), (cx + 40, cy + 30), (cx, cy + 42), (cx - 40, cy + 30)], J.BG2, col, 6, close=True)
            + F.circ(cx, cy, 30, "none", col, 4) + F.circ(cx, cy, 7, col))


def _i_bottle(cx, cy, col):
    return (F.rect(cx - 14, cy - 62, 28, 22, J.BG2, col, 6, rx=3) + F.poly([(cx - 14, cy - 40), (cx - 36, cy - 18), (cx - 36, cy + 62), (cx + 36, cy + 62), (cx + 36, cy - 18), (cx + 14, cy - 40)], J.BG2, col, 6, close=True)
            + F.rect(cx - 24, cy + 2, 48, 36, "none", col, 4, rx=3))


def _i_news(cx, cy, col):
    return (F.rect(cx - 62, cy - 52, 124, 104, J.BG2, col, 6, rx=6) + F.rect(cx - 48, cy - 38, 44, 34, "none", col, 4)
            + "".join(F.line(cx + 6, cy - 34 + i * 15, cx + 48, cy - 34 + i * 15, col, 4) for i in range(3))
            + "".join(F.line(cx - 48, cy + 10 + i * 15, cx + 48, cy + 10 + i * 15, col, 4) for i in range(3)))


def _i_cal(cx, cy, col):
    return (F.rect(cx - 56, cy - 48, 112, 104, J.BG2, col, 6, rx=8) + F.line(cx - 56, cy - 20, cx + 56, cy - 20, col, 5)
            + F.line(cx - 28, cy - 62, cx - 28, cy - 36, col, 7) + F.line(cx + 28, cy - 62, cx + 28, cy - 36, col, 7)
            + "".join(F.circ(cx - 32 + (i % 3) * 32, cy + 2 + (i // 3) * 26, 5, col) for i in range(6)))


def _i_stairs(cx, cy, col):
    """駅の出入口の形（階段だけ）。"""
    return (F.poly([(cx - 66, cy + 56), (cx - 66, cy + 26), (cx - 34, cy + 26), (cx - 34, cy - 4), (cx - 2, cy - 4), (cx - 2, cy - 34), (cx + 30, cy - 34), (cx + 30, cy - 60), (cx + 66, cy - 60)],
                   "none", col, 8) + F.line(cx + 66, cy - 60, cx + 66, cy + 56, col, 6) + F.line(cx - 66, cy + 56, cx + 66, cy + 56, col, 6))


def _i_window(cx, cy, col):
    """窓の形に×（窓がない部屋）。"""
    return (F.rect(cx - 52, cy - 52, 104, 104, J.BG2, col, 6, rx=4) + F.line(cx, cy - 52, cx, cy + 52, col, 5) + F.line(cx - 52, cy, cx + 52, cy, col, 5)
            + _xmark(cx, cy, 44, J.ALERT, 9))


def _i_desk(cx, cy, col):
    """指令の部屋の形（並んだ机と画面）。"""
    return (F.rect(cx - 66, cy - 54, 132, 58, J.BG2, col, 6, rx=6) + F.line(cx - 22, cy - 54, cx - 22, cy + 4, col, 4) + F.line(cx + 22, cy - 54, cx + 22, cy + 4, col, 4)
            + F.line(cx - 70, cy + 30, cx + 70, cy + 30, col, 8) + F.line(cx - 50, cy + 30, cx - 50, cy + 58, col, 6) + F.line(cx + 50, cy + 30, cx + 50, cy + 58, col, 6))


ICONS = dict(phone=_i_phone, book=_i_book, glass=_i_glass, globe=_i_globe, radio=_i_radio, payphone=_i_payphone, suit=_i_suit, car=_i_car, mask=_i_mask,
             speaker=_i_speaker, eye=_i_eye, bottle=_i_bottle, news=_i_news, cal=_i_cal, stairs=_i_stairs, window=_i_window, desk=_i_desk)


# ══════════════════════════════════════════════════════════
#  描き手（札の型はこの1つだけ）
# ══════════════════════════════════════════════════════════
def _icon(c, cx, cy, col, k):
    """印の座標は等倍で書いた＝拡大率を座標の値に掛ける（SVG の変換にしない＝門番 box が座標を読むので、変換だと印が小さく測られる）。"""
    g = ICONS[c["icon"]](cx, cy, col)
    if c["cross"]:
        g += _xmark(cx, cy, 50, J.ALERT, 10)

    def xv(v):
        return cx + (float(v) - cx) * k

    def yv(v):
        return cy + (float(v) - cy) * k

    g = re.sub(r'(?<![-\w])(x|x1|x2|cx)="([-\d.]+)"', lambda m: f'{m[1]}="{xv(m[2]):.1f}"', g)
    g = re.sub(r'(?<![-\w])(y|y1|y2|cy)="([-\d.]+)"', lambda m: f'{m[1]}="{yv(m[2]):.1f}"', g)
    g = re.sub(r'(?<![-\w])(width|height|r|rx|stroke-width)="([-\d.]+)"', lambda m: f'{m[1]}="{float(m[2]) * k:.1f}"', g)
    return re.sub(r' d="M([^"]+)"', lambda m: ' d="M' + re.sub(r"([-\d.]+) ([-\d.]+)", lambda p: f"{xv(p[1]):.1f} {yv(p[2]):.1f}", m[1]) + '"', g)


def _draw_card(c, box, k=1.0):
    x, y, w, h = box
    col = sc(c["who"])
    ink, big = INK, J.AMBER
    head = col
    fill = None
    op = None
    if c["gray"]:
        col, ink, big, head, fill = GRAY_LINE, GRAY_INK, GRAY_INK, GRAY_INK, GRAY_FILL
    if c["dim"]:
        ink, big, head = J.TICK, J.TICK, J.TICK
        col = J.TICK
        op = 0.55
    g = _panel(x, y, w, h, col, op=op if op is not None else 0.84, sw=3 if c["dim"] else 5, fill=fill)
    rows = _rows(c, k)
    ch = sum(cap * LH[kd] for kd, _t2, cap in rows)
    tx0, tw = x, w
    if c["icon"]:
        g += _icon(c, x + (PX + ICON_W / 2) * k, y + h / 2, col, k)
        tx0, tw = x + (ICON_W + 22) * k, w - (ICON_W + 22) * k
    tx = tx0 + tw / 2
    yy = y + (h - ch) / 2
    for kd, t, cap in rows:
        lh = cap * LH[kd]
        base = yy + lh / 2 + cap * 0.36
        colr = head if kd == "head" else big if kd == "big" else (J.TICK if c["dim"] else ink)
        g += _t(tx, base, t, cap, colr, "middle", tw - 2 * PX * k + 8)
        yy += lh
    return g


def _arrow_xy(A, B):
    ax, ay, aw, ah = A
    bx, by, bw, bh = B
    if ax + aw <= bx or bx + bw <= ax:
        lo, hi = max(ay, by), min(ay + ah, by + bh)
        ya = yb = (lo + hi) / 2 if hi > lo else None
        if ya is None:
            ya, yb = ay + ah / 2, by + bh / 2
        if ax + aw <= bx:
            return ax + aw + 12, ya, bx - 12, yb
        return ax - 12, ya, bx + bw + 12, yb
    lo, hi = max(ax, bx), min(ax + aw, bx + bw)
    xm = (lo + hi) / 2
    if ay + ah <= by:
        return xm, ay + ah + 10, xm, by - 10
    return xm, ay - 10, xm, by + bh + 10


def _draw_arrow(a, boxes, k=1.0):
    x1, y1, x2, y2 = _arrow_xy(boxes[a["a"]], boxes[a["b"]])
    col = sc(a["who"])
    g = _arrow(x1, y1, x2, y2, col, 8, 30, "16 12" if a["dash"] else None) if a["head"] else F.line(x1, y1, x2, y2, col, 7, dash="16 12" if a["dash"] else None)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if a["q"]:
        g += _qmark(mx, my - 8 * k, 76 * k, J.AMBER)
    if a["ng"]:
        g += _xmark(mx, my, 26 * k, J.ALERT, 9)
    if a["t"]:
        if abs(y1 - y2) < 2:
            g += _t(mx, my - 26 * k, a["t"], 34 * k, col, "middle", max(abs(x2 - x1), 130.0))
        else:
            g += _t(mx + 26 * k, my + 12 * k, a["t"], 34 * k, col, "start", 420.0)
    return g


# ══════════════════════════════════════════════════════════
#  表（1行が1カット）。カットの順＝一覧 `ref/ep30/eizou_list30.md`。字は語りと同じ字面を避ける（門番 echo）・見出しと重ねない（門番 dup）
# ══════════════════════════════════════════════════════════
H, T, K, S, U, R, D = "hakusho", "hanketsu", "kokkai", "shuki", "kouan", "musen", "doc"
S_H = "警察白書 平成8年"
S_U = "公安調査庁 オウム真理教問題デジタルアーカイブ"
S_S = "公安調査庁 デジタルアーカイブの手記"
S_T = "東京地裁 平成16年2月27日判決"
S_O = "厚生労働省 オーラルヒストリー"
S_R = "警視庁の無線の記録"


def _strip(lit):
    """反省の3つの箱（cb02 と同じ3つ）＝いま話している箱だけ明るく。"""
    return [_c(0, H if i == lit else None, lines=t, cap=40, dim=i != lit, cell=(i, 0)) for i, t in enumerate(("知識不足", "情報不足", "権限の制限"))]


FU = {}
# ── つかみ・第1章
FU["c205"] = _f(2, "サリンとは", "毒の種類と、体に出たこと", [
    _c(0, K, lines="猛毒の神経ガス", sub="化学兵器として開発", cap=58, cell=(0, 0)),
    _c(1, S, head="院長の手記", lines=("目の痛み", "視界の暗さ", "息苦しさ"), sub="人によっては吐き気", cap=50, cell=(1, 0)),
], [_x(1, "a", "b", t="吸うと")], src="国会会議録 平成7年4月19日・" + S_S)
FU["c207"] = _f(2, "亡くなった方の数", "資料ごとの数え方", [
    _c(0, K, head="国会 4月19日", big="12人", cell=(0, 0)),
    _c(0, T, head="刑事裁判の判決", big="12人", cell=(1, 0)),
    _c(1, U, head="公安調査庁", big="13人", sub="2020年3月に、さらに1人", cell=(2, 0)),
], src="国会会議録 平成7年4月19日・" + S_T + "・" + S_U)
FU["c209"] = _f(2, "けがの数", "国の給付金の認定", [
    _c(0, U, big="5,800人以上", bcap=100, cell=(0, 0)),
    _c(1, U, lines="認められた数", sub="2010年3月まで", cap=50, cell=(0, 1)),
], src=S_U)
FU["c210"] = _f(3, "だれが", "事件を起こした側", [
    _c(1, U, head="教団", lines="オウム真理教", cap=62, cell=(0, 0)),
    _c(1, None, head="教祖", lines="麻原彰晃", sub="本名 松本智津夫", cap=62, cell=(1, 0)),
    _c(2, T, head="裁判の結論", lines="教祖の指示の下、幹部らが実行", cap=50, cell=(0, 1), span=(2, 1)),
], src=S_U + "・" + S_T)
# ── 第2章
FU["c305"] = _f(2, "弁護士の一家の事件", "神奈川県警の動き", [
    _c(0, H, head="1989年", big="11月7日", bcap=64, lines="届け出", cap=46, cell=(0, 0)),
    _c(0, H, head="1989年", big="11月17日", bcap=64, lines="捜査本部", cap=46, cell=(1, 0)),
    _c(1, H, head="部屋に残っていた物", lines="教団のバッジ", sub="早くから関与を視野に", cap=60, cell=(0, 1), span=(2, 1)),
], [_x(0, "a", "b")], src=S_H)
FU["c306"] = _f(2, "白書の続き", "弁護士の事件の捜査", [
    _c(0, H, lines="事件現場において物証が乏しかったこと", q=True, cap=54, cell=(0, 0)),
    _c(1, H, lines=("教団の閉鎖性が強く", "内部情報がほとんど得られなかった"), q=True, cap=54, cell=(0, 1)),
], src=S_H, mute=(0, 1))
FU["c308"] = _f(2, "選挙の結果", "教祖の次の言葉", [
    _c(0, U, head="1990年2月 衆議院選挙", big="25人全員が落選", bcap=72, cell=(0, 0)),
    _c(1, U, head="このあとの教祖", lines="選挙では救済できない", cap=56, cell=(0, 1)),
], src=S_U)
FU["c310"] = _f(3, "2つの事件", "局長の答弁", [
    _c(1, K, lines="弁護士の事件", cap=54, cell=(0, 0)),
    _c(1, K, lines="熊本の事件", cap=54, cell=(1, 0)),
    _c(2, K, head="その時点で", lines="関連を解明するには至らなかった", q=True, cap=50, cell=(0, 1), span=(2, 1)),
], [_x(1, "a", "b", q=True, dash=True, head=False)], src="国会会議録 平成8年5月23日", gy=30.0)
FU["c312"] = _f(2, "年表の続き", "教祖の言葉の記録", [
    _c(0, U, big="1993年4月", bcap=64, lines="サリンに初めて言及", cap=46, cell=(0, 0)),
    _c(1, U, big="1994年3月", bcap=64, lines="国家に対する戦闘宣言", cap=46, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_U, gx=110.0)
FU["c313"] = _f(2, "白書の反省", "反省の中身", [
    _c(0, H, head="教団は", lines="過去にテロなし", cap=58, cell=(0, 0)),
    _c(1, H, head="情報収集・分析体制", lines="十分とはいえず", cap=58, cell=(1, 0)),
], src=S_H)
# ── 第3章
FU["c402"] = _f(2, "指示の先", "土地の争いの裁判", [
    _c(0, None, head="1994年6月20日ごろ", lines="教団", cap=64, cell=(0, 0)),
    _c(1, U, lines="裁判所", cap=64, cell=(1, 0)),
    _c(0, None, lines="地主と住民", cap=50, dim=True, cell=(2, 0)),
], [_x(1, "a", "b", t="教祖の指示", who=U), _x(1, "c", "b", head=False, dash=True, t="裁判")], src=S_U, gx=230.0)
FU["c405"] = _f(3, "松本の被害", "資料ごとの数", [
    _c(1, T, head="亡くなった方：判決の時点", big="7人", bcap=80, cell=(0, 0)),
    _c(1, U, head="亡くなった方：のちに", big="8人", bcap=80, cell=(1, 0)),
    _c(2, H, head="負傷：白書", big="144人", bcap=80, cell=(0, 1)),
    _c(2, U, head="負傷：公安調査庁", big="約140人", bcap=80, cell=(1, 1)),
], src=S_T + "・" + S_H + "・" + S_U)
FU["c406"] = _f(2, "初めての事件", "白書と救急の現場", [
    _c(0, H, icon="globe", lines=("世界で初めて", "犯罪の手段として"), q=True, cap=52, cell=(0, 0)),
    _c(1, D, head="救急の指導医", lines="聞いたことがなかった", cap=44, cell=(0, 1)),
], src=S_H + "・" + S_O)
FU["c408"] = _f(2, "毒の判断", "事件の数日後", [
    _c(0, H, icon="glass", lines=("サリンである可能性が", "極めて高い"), q=True, cap=54, cell=(0, 0)),
    _c(1, K, lines="その前に、現場の捜索", cap=44, cell=(0, 1)),
], src=S_H + "・国会会議録 平成7年12月1日")
FU["c409"] = _f(2, "通報した人", "2つの立場", [
    _c(0, H, lines="第一通報者", cap=70, cell=(0, 0)),
    _c(1, K, lines="被害者", cap=70, cell=(1, 0)),
], [_x(1, "a", "b", head=False, t="同じ人")], src=S_H + "・国会会議録 平成7年10月12日")
FU["c410"] = _f(3, "警察がしたこと", "捜索までの手順", [
    _c(0, H, lines="令状", cap=62, cell=(0, 0)),
    _c(0, H, lines="被疑者不詳", cap=62, cell=(1, 0)),
    _c(1, H, lines="捜索と検証", cap=62, cell=(2, 0)),
    _c(2, H, lines="第一通報者から事情を聴取", cap=46, cell=(0, 1), span=(3, 1)),
], [_x(0, "a", "b"), _x(1, "b", "c")], src=S_H + "・国会会議録 平成8年5月23日", gx=110.0)
FU["c412"] = _f(2, "国会の批判", "議員の言葉", [
    _c(0, K, head="1995年6月", lines="終始一貫被疑者扱いにした", q=True, cap=60, cell=(0, 0)),
    _c(1, K, head="1996年5月", lines="第一通報者に対する見込み捜査", q=True, cap=56, cell=(0, 1)),
], src="国会会議録 平成7年6月7日・平成8年5月14日", mute=(0,))
FU["c413"] = _f(2, "警察庁の答弁", "局長の言葉", [
    _c(0, K, head="議員 1995年6月", lines=("終始一貫", "被疑者扱いにした"), q=True, dim=True, cap=38, cell=(0, 0), span=(1, 2)),
    _c(0, K, head="局長 1995年10月", lines=("容疑者として", "取り扱ったものではありません"), q=True, cap=46, cell=(1, 0)),
    _c(1, K, lines=("あくまでも第一通報者、", "かつ被害者として"), q=True, cap=46, cell=(1, 1)),
], src="国会会議録 平成7年6月7日・平成7年10月12日", mute=(0,))
FU["c414"] = _f(2, "国家公安委員長の答弁", "局長に続く言葉", [
    _c(0, K, head="1995年11月", lines="会見でその言葉は使っていない", cap=46, cell=(0, 0)),
    _c(1, K, lines=("疑惑というのが", "ひとり歩きをしてしまった"), q=True, cap=56, cell=(0, 1)),
], src="国会会議録 平成7年11月28日")
FU["c416"] = _f(2, "白書の書き方", "捜索と聴取について", [
    _c(0, H, lines="適正な捜査であった", q=True, cap=64, cell=(0, 0)),
    _c(1, H, lines="多大な心労と迷惑", q=True, cap=60, cell=(0, 1)),
], src=S_H)
FU["c417"] = _f(2, "謝罪の時期", "警察庁の答弁", [
    _c(0, None, head="1995年", big="3月20日", bcap=58, lines="地下鉄の事件", cap=42, dim=True, cell=(0, 0)),
    _c(0, K, big="6月11日", bcap=58, lines="署長が遺憾の意", cap=42, cell=(1, 0)),
    _c(1, K, big="6月27日", bcap=58, lines="本部長が県議会で", cap=42, cell=(2, 0)),
], [_x(0, "a", "b"), _x(1, "b", "c")], src="国会会議録 平成8年5月23日", gx=90.0)
FU["c418"] = _f(3, "訂正の時期", "局長の答弁", [
    _c(1, K, head="放送局の訂正まで", big="約1年", bcap=110, sub="松本の事件から", cell=(0, 0)),
], src="国会会議録 平成9年5月13日")
FU["c420"] = _f(2, "白書の続き", "知識が十分でも", [
    _c(0, H, lines="即座に解決したとは断言できない", q=True, cap=60, cell=(0, 0)),
    _c(1, H, lines="一層効率的に推進し得たのではないか", q=True, cap=60, cell=(0, 1)),
], src=S_H, mute=(0,))
FU["c421"] = _f(3, "勉強したこと", "救急の現場", [
    _c(0, D, lines="知らなかった毒", cap=56, cell=(0, 0)),
    _c(1, D, icon="book", head="救急の指導医", lines=("松本のあとで", "みんなが勉強"), cap=46, cell=(1, 0)),
    _c(2, None, lines="あの朝の東京へ", cap=46, cell=(0, 1), span=(2, 1)),
], [_x(1, "a", "b")], src=S_O, gy=30.0)
# ── 第4章
FU["c504"] = _f(1, "国会の追及", "議員の批判", [
    _c(0, K, head="議員の言葉", big="2か月あまり", bcap=90, sub="調べなかったのでは", cell=(0, 0)),
], src="国会会議録 平成7年6月7日")
FU["c507"] = _f(3, "白書の言葉", "土の鑑定のあと", [
    _c(1, H, lines=("松本サリン事件は", "教団による犯行ではないか"), q=True, cap=56, cell=(0, 0)),
    _c(2, H, lines="捜査資料の入手には至らなかった", q=True, cap=56, cell=(0, 1)),
], src=S_H, mute=(2,))
FU["c510"] = _f(2, "防護服", "警部補の手記", [
    _c(0, S, icon="suit", lines=("自衛隊と", "全く同質"), cap=60, cell=(0, 0)),
], src=S_S)
FU["c511"] = _f(2, "続いた襲撃", "別の猛毒の事件", [
    _c(0, T, head="1994年12月〜1995年1月", lines="3人が襲われ、1人が亡くなった", cap=52, cell=(0, 0)),
    _c(1, T, lines="教祖の判決が認めた事件", cap=48, cell=(0, 1)),
], src=S_T)
# ── 第5章
FU["c602"] = _f(2, "前日のメモ", "息子の手記から", [
    _c(0, U, lines="狙いは妹の居場所", cap=48, cell=(0, 0)),
    _c(1, S, lines=("万が一のことがあったら警察に連絡しろ。", "オウムに間違いない"), q=True, cap=48, cell=(0, 1)),
], src=S_U + "・手記")
FU["c604"] = _f(3, "捜査の手がかり", "白書の書き方", [
    _c(1, H, icon="car", lines="目撃されたレンタカー", cap=44, cell=(0, 0)),
    _c(1, H, lines="信者を割り出す", cap=50, cell=(1, 0)),
    _c(2, H, lines="組織的な犯行と判断", cap=50, cell=(0, 1), span=(2, 1)),
], [_x(1, "a", "b")], src=S_H, gy=30.0)
FU["c605"] = _f(2, "東京の事件", "捜査が進む節目", [
    _c(0, None, head="東京", lines="警視庁の管内", cap=60, cell=(0, 0)),
    _c(1, H, lines=("特に進展をみることとなる", "契機"), q=True, cap=50, cell=(1, 0)),
], src=S_H)
FU["c606"] = _f(2, "大きな報道", "事務長の事件のあと", [
    _c(0, H, icon="news", lines=("教団が絡んでいる", "かのような報道"), cap=48, cell=(0, 0)),
    _c(1, H, head="教祖の危機感", lines="大規模な強制捜査", q=True, cap=54, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_H)
FU["c608"] = _f(2, "迫る捜査", "教祖らの動き", [
    _c(0, U, icon="news", head="3月16日の読売新聞", lines=("ワゴン車の押収", "指紋の検出"), cap=44, cell=(0, 0)),
    _c(1, T, head="判決", lines=("自動小銃の部品を", "隠す"), cap=48, cell=(1, 0)),
], src=S_U + "・" + S_T)
FU["c612"] = _f(2, "車の中の話", "教祖の判決", [
    _c(0, T, lines=("共謀が成立していたことは", "明らかである"), q=True, cap=60, cell=(0, 0)),
    _c(1, T, lines="地下鉄の案は、ほかの判決にも", cap=40, cell=(0, 1)),
], src=S_T + "・東京高裁 平成15年5月19日判決", mute=(0,))
FU["c615"] = _f(2, "別の判決", "目的についての見方", [
    _c(0, T, lines="強制捜査を一時しのぎ的に回避", q=True, cap=46, cell=(0, 0)),
    _c(1, T, head="内乱罪の主張に対して", lines=("統治の基本秩序を壊乱することを", "目的とするものとはいえない"), q=True, cap=46, cell=(0, 1)),
], src="東京地裁 平成14年6月26日判決")
FU["c616"] = _f(2, "呼び方の違い", "法律と最高裁", [
    _c(0, D, head="給付金の法律", lines="国の統治機構を破壊する等の主義", q=True, cap=50, cell=(0, 0)),
    _c(1, T, head="最高裁", lines="阻止，かく乱する目的", q=True, cap=50, cell=(0, 1)),
], src="給付金の法律・最高裁 平成23年11月18日判決", mute=(0,))
FU["c617"] = _f(2, "届いた防護服", "事件の2日前", [
    _c(0, S, icon="cal", head="警部補の手記", big="3月18日", bcap=62, cell=(0, 0)),
    _c(0, S, icon="suit", big="64着", bcap=84, cell=(1, 0)),
    _c(1, S, lines="開発は松本のあと", cap=44, cell=(0, 1), span=(2, 1)),
], src=S_S)
FU["c619"] = _f(2, "判決の見方", "前の夜の2件", [
    _c(0, None, lines="爆発物", cap=50, dim=True, cell=(0, 0)),
    _c(0, None, lines="火炎びん", cap=50, dim=True, cell=(1, 0)),
    _c(1, T, head="教祖の判決", lines=("「世間の同情を買う」", "「自作自演」"), cap=54, cell=(0, 1), span=(2, 1)),
], src=S_T)
# ── 第6章
FU["c701"] = _f(3, "3つの記録", "あの朝を知る手がかり", [
    _c(1, R, icon="radio", lines="警視庁の無線", cap=46, cell=(0, 0)),
    _c(1, S, icon="book", lines="現場の手記", cap=46, cell=(1, 0)),
    _c(1, K, icon="news", lines="国会の答弁", cap=46, cell=(2, 0)),
    _c(2, S, lines="手記の時刻は本人の記憶", cap=46, cell=(0, 1), span=(3, 1)),
], src=S_U)
FU["c709"] = _f(2, "助役の手記", "自責の念", [
    _c(0, S, lines=("サリンの対処法を", "勉強していれば"), q=True, cap=64, cell=(0, 0)),
], src=S_S, mute=(0,))
FU["c711"] = _f(2, "小伝馬町駅", "運転士の手記", [
    _c(0, S, lines="ホームは人でいっぱい", cap=44, cell=(0, 0)),
    _c(1, S, lines="これ何ですかね。", q=True, cap=66, cell=(0, 1)),
], src=S_S)
FU["c712"] = _f(2, "警察官の言葉", "運転士の手記", [
    _c(0, S, icon="stairs", lines=("警察官と消防を", "ホームへ"), cap=44, cell=(0, 0)),
    _c(1, S, lines="サリンかな", q=True, sub="時刻なし・本人の記憶", cap=64, cell=(1, 0)),
], src=S_S)
FU["c722"] = _f(3, "爆発という語", "2つの記録", [
    _c(1, R, head="無線の記録", lines="理由は分からない", cap=46, cell=(0, 0)),
    _c(2, S, icon="phone", head="警部補の手記・110番", lines="地下鉄で爆発が起きた", q=True, cap=46, cell=(0, 1)),
], src=S_R + "・" + S_S)
FU["c724"] = _f(2, "現場からの連絡", "隊員の手記", [
    _c(0, S, lines="指揮隊から応援の要請", cap=46, cell=(0, 0), span=(2, 1)),
    _c(1, S, lines="火煙もなく", q=True, cap=62, cell=(0, 1)),
    _c(1, S, lines="多くの傷者", q=True, cap=62, cell=(1, 1)),
], src=S_S)
FU["c725"] = _f(2, "何が起きているのか", "隊員の不安", [
    _c(0, S, lines="火事ではない", cap=56, cell=(0, 0)),
    _c(0, S, lines="けが人が多い", cap=56, cell=(1, 0)),
], [_x(0, "a", "b", q=True, dash=True, head=False)], src=S_S)
FU["c727"] = _f(2, "消防の無線", "隊員の手記", [
    _c(0, S, icon="radio", cross=True, lines=("無線機は", "通じない"), cap=50, cell=(0, 0)),
    _c(1, S, icon="payphone", lines=("公衆電話で", "報告"), cap=50, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_S)
FU["c732"] = _f(2, "ほかへの連絡", "記録を探した結果", [
    _c(0, R, lines="警察の無線", cap=50, cell=(0, 0), span=(1, 2)),
    _c(0, None, lines="消防", cap=50, cell=(1, 0)),
    _c(0, None, lines="病院", cap=50, cell=(1, 1)),
    _c(1, None, lines="届いた時刻の記録は見つからず", cap=42, cell=(0, 2), span=(2, 1)),
], [_x(1, "a", "b", q=True, dash=True), _x(1, "a", "c", q=True, dash=True)], src=S_R, gx=220.0)
FU["c735"] = _f(1, "警察庁の動き", "白書の書き方", [
    _c(0, H, big="9:00", bcap=96, lines="警察庁に対策室", cap=54, cell=(0, 0)),
], src=S_H)
# ── 第7章
FU["c802"] = _f(2, "最初の電話", "院長の手記", [
    _c(0, S, icon="phone", big="8:16", bcap=54, lines=("地下鉄日比谷線の茅場町駅で", "爆発火災が発生したらしい"), q=True, cap=46, cell=(0, 0)),
    _c(1, S, lines="4、5人は大丈夫", q=True, cap=56, cell=(0, 1)),
], src=S_S, mute=(0,))
FU["c804"] = _f(3, "最初の患者", "院長の手記", [
    _c(1, S, big="8:25ごろ", bcap=60, lines="歩いて来た3人", cap=46, cell=(0, 0)),
    _c(1, S, lines="皆、目が痛い", cap=50, cell=(1, 0)),
    _c(2, S, lines="歩けるなら重症ではない", cap=46, cell=(0, 1), span=(2, 1)),
], src=S_S)
FU["c805"] = _f(2, "のちに分かること", "院長の手記", [
    _c(0, S, lines="この病院で最初の被害者", cap=48, cell=(0, 0)),
    _c(1, S, head="2024年", lines=("疑問をもって対応しなかったことを", "後悔"), q=True, cap=52, cell=(0, 1)),
], src=S_S, mute=(1,))
FU["c807"] = _f(2, "情報への疑い", "副医長の心の中", [
    _c(0, S, lines="爆発火災？", cap=76, cell=(0, 0), span=(2, 1)),
    _c(0, S, lines="焦げ臭さなし", cap=44, cell=(0, 1)),
    _c(0, S, lines="外傷なし", cap=44, cell=(1, 1)),
], src=S_S)
FU["c808"] = _f(2, "救急隊の答え", "院長の手記", [
    _c(0, S, lines=("我々も駅の中に入っていないので", "分かりません"), q=True, cap=54, cell=(0, 0)),
    _c(1, S, lines="これからもっと多くの人が来る", q=True, cap=46, cell=(0, 1)),
], src=S_S, mute=(0,))
FU["c810"] = _f(2, "病院の判断", "院長の手記", [
    _c(0, S, lines="3人目も同じ状態", cap=44, cell=(0, 0)),
    _c(1, S, icon="speaker", head="全館放送", lines="非常招集", cap=66, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_S)
FU["c811"] = _f(1, "診療の中止", "院長の手記", [
    _c(0, S, big="9:30ごろ", bcap=80, lines="通常の診療を全部中止", cap=50, cell=(0, 0)),
], src=S_S)
FU["c814"] = _f(3, "何の毒か", "院長の手記", [
    _c(1, S, head="消防庁からの情報", lines="別の物質らしい", cap=54, cell=(0, 0)),
    _c(2, S, lines=("これまで診てきた", "症状と違う"), cap=54, cell=(1, 0)),
], [_x(2, "a", "b", ng=True, head=False)], src=S_S)
FU["c815"] = _f(2, "似ている症状", "院長の手記", [
    _c(0, S, lines=("農薬の中毒に", "似ている"), cap=58, cell=(0, 0)),
    _c(1, S, lines=("でも特有の匂いが", "しない"), cap=58, cell=(1, 0)),
], [_x(1, "a", "b", q=True, dash=True, head=False)], src=S_S)
FU["c818"] = _f(2, "指令の部屋", "救急の指導医", [
    _c(0, D, icon="desk", head="最初に聞いた話", lines="爆発事故", cap=56, cell=(0, 0)),
    _c(1, D, icon="eye", head="病院からの知らせ", lines="瞳が小さい", cap=56, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_O, gx=120.0)
FU["c823"] = _f(3, "二次被害の訴え", "院長の手記", [
    _c(1, S, lines=("スタッフの半数が", "二次被害を訴えた"), cap=46, cell=(0, 0)),
    _c(2, S, icon="window", head="ホール", lines=("窓がなく", "換気が不十分"), cap=46, cell=(1, 0)),
], src=S_S)
FU["c824"] = _f(2, "のちの教訓", "院長の手記", [
    _c(0, S, lines="衣服を袋に", cap=60, cell=(0, 0)),
    _c(1, S, lines="自分の身は自分で守る", q=True, cap=54, cell=(1, 0)),
], src=S_S)
# ── 第8章
FU["c901"] = _f(2, "松本からの電話", "院長の手記", [
    _c(0, S, icon="phone", lines="松本", cap=60, cell=(0, 0)),
    _c(0, S, lines="東京の病院", cap=54, cell=(1, 0)),
    _c(0, S, lines="症状が松本と同じ", cap=44, cell=(0, 1)),
    _c(1, S, lines="治療の経過をFAXで", cap=44, cell=(1, 1)),
], [_x(0, "a", "b")], src=S_S, gy=30.0)
FU["c904"] = _f(3, "解毒剤", "院長の手記", [
    _c(1, S, icon="bottle", head="効くと教わった", lines="パム", cap=72, cell=(0, 0)),
    _c(2, S, big="7本", bcap=100, lines="残りはこれだけ", cap=42, cell=(1, 0)),
], src=S_S)
FU["c910"] = _f(2, "暗い照明", "警部補の手記", [
    _c(0, S, big="12:00ごろ", bcap=58, lines="警視庁に戻る", cap=44, cell=(0, 0)),
    _c(1, S, lines="節電してるの？", q=True, cap=54, cell=(1, 0)),
    _c(1, S, icon="eye", lines=("5人とも", "瞳が小さい"), cap=46, cell=(0, 1), span=(2, 1)),
], src=S_S)
# ── 第9章
FU["ca02"] = _f(3, "捜索までの道筋", "局長の答弁", [
    _c(1, K, lines=("2月末の事件の", "捜査"), cap=46, cell=(0, 0)),
    _c(2, K, lines="諸準備", cap=60, cell=(1, 0)),
    _c(2, K, big="3月22日", bcap=58, lines="捜索", cap=42, cell=(2, 0)),
], [_x(2, "a", "b"), _x(2, "b", "c")], src="国会会議録 平成7年4月19日", gx=110.0)
FU["ca03"] = _f(3, "別の局長の言葉", "準備の長さ", [
    _c(0, K, head="1996年4月", lines=("通常必要とされる時間よりも", "長時間を要した"), q=True, cap=46, cell=(0, 0)),
    _c(1, K, lines="警察の動きなどが察知された", q=True, cap=52, cell=(0, 1)),
    _c(2, K, lines="証拠の散逸", q=True, cap=52, cell=(0, 2)),
], src="国会会議録 平成8年4月9日")
FU["ca04"] = _f(2, "備えの話", "土の鑑定から", [
    _c(0, K, head="1995年の答弁", lines=("サリンの存在等も", "あるかもわからない"), q=True, cap=48, cell=(0, 0)),
    _c(1, K, icon="mask", head="1996年の答弁", lines=("防毒マスク等の調達", "使用訓練"), cap=44, cell=(1, 0)),
], src="国会会議録 平成7年4月19日・平成8年4月9日")
FU["ca06"] = _f(2, "裁判の数", "起訴と判決", [
    _c(0, D, big="17件", bcap=76, lines="教祖の起訴", cap=42, cell=(0, 0)),
    _c(0, D, big="13件", bcap=76, lines="判決の対象", cap=42, cell=(1, 0)),
    _c(1, D, big="約190人", bcap=76, lines="ほかの関係者", cap=42, cell=(2, 0)),
], src="犯罪白書 令和元年版")
FU["ca07"] = _f(2, "教祖の判決", "死刑の確定まで", [
    _c(0, T, big="2004年2月", bcap=56, lines="死刑を言い渡し", cap=44, cell=(0, 0)),
    _c(0, T, big="2006年9月", bcap=56, lines="確定", cap=44, cell=(1, 0)),
    _c(1, T, lines=("救済の名の下に日本国を支配して", "自らその王となることを空想し"), q=True, cap=52, cell=(0, 1), span=(2, 1)),
], [_x(0, "a", "b")], src=S_T + "・" + S_U, gx=110.0, gy=30.0)
FU["ca08"] = _f(2, "判決の数", "刑の執行まで", [
    _c(0, T, head="地下鉄の事件の判決", big="12人", sub="亡くなった方", cell=(0, 0)),
    _c(1, U, head="一連の事件で死刑確定", big="13人", sub="2018年7月に執行", cell=(1, 0)),
], src=S_T + "・" + S_U)
FU["ca09"] = _f(3, "聞こえてくる話", "公安調査庁の説明", [
    _c(0, None, gray=True, big="噂", bcap=110, cell=(0, 0), span=(1, 2)),
    _c(1, U, lines=("使われる場：", "後継の団体の勧誘"), cap=44, cell=(1, 0)),
    _c(2, None, gray=True, lines="「陰謀」", cap=56, cell=(1, 1)),
], src=S_U)
FU["ca10"] = _f(2, "裁判の結論", "3つの判断", [
    _c(0, T, lines="教祖の判決", cap=40, cell=(0, 0)),
    _c(0, T, lines="幹部たちの判決", cap=40, cell=(1, 0)),
    _c(0, T, lines="最高裁の判断", cap=40, cell=(2, 0)),
    _c(1, T, lines=("地下鉄3路線5方面の電車内等に", "サリンを発散させて"), q=True, cap=52, cell=(0, 1), span=(3, 1)),
], src=S_T + "・最高裁 平成23年11月18日判決")
FU["ca12"] = _f(2, "別の事件", "ここでは別の話", [
    _c(0, K, big="1995年3月30日", bcap=54, lines="警察庁の長官の事件", cap=42, cell=(0, 0)),
    _c(1, K, big="2010年", bcap=54, lines="時効", sub="だれも裁かれていない", cap=42, cell=(1, 0)),
], [_x(1, "a", "b")], src="国会会議録 平成22年4月6日", gx=110.0)
FU["ca15"] = _f(2, "給付金", "対象の事件全体", [
    _c(0, D, head="2008年6月", lines="法律が成立", cap=46, cell=(0, 0), span=(2, 1)),
    _c(1, D, big="約6千人", bcap=76, cell=(0, 1)),
    _c(1, D, big="約30億3千万円", bcap=66, cell=(1, 1)),
], src="犯罪被害者白書 平成24年版・" + S_U)
# ── 第10章
FU["cb03"] = _f(2, "1つ目の反省", "松本の事件で", _strip(0) + [
    _c(0, H, lines="戸惑いがあった", q=True, cap=48, cell=(0, 1), span=(3, 1)),
    _c(1, H, lines="即座に解決したとは断言できない", q=True, cap=44, cell=(0, 2), span=(3, 1)),
    _c(1, H, lines="一層効率的に推進し得たのではないか", q=True, cap=44, cell=(0, 3), span=(3, 1)),
], src=S_H, mute=(1,))
FU["cb04"] = _f(2, "2つ目の反省", "弁護士の事件で", _strip(1) + [
    _c(0, H, lines="内部情報がほとんど得られず", q=True, cap=52, cell=(0, 1), span=(3, 1)),
    _c(1, H, head="情報収集の体制", lines="十分とはいえず", cap=50, cell=(0, 2), span=(3, 1)),
], src=S_H)
FU["cb06"] = _f(2, "3つ目の反省", "当時の法律", _strip(2) + [
    _c(0, H, lines="捜査を行うことは困難であった", q=True, cap=52, cell=(0, 1), span=(3, 1)),
    _c(1, H, lines=("管轄区域内の公安の維持等に関連することを", "明確に認定"), q=True, cap=42, cell=(0, 2), span=(3, 1)),
], src=S_H)
FU["cb10"] = _f(2, "議員の言葉", "批判の中身", [
    _c(0, K, head="1996年5月", lines="初動捜査のつまずき", q=True, cap=52, cell=(0, 0)),
    _c(0, K, head="1996年5月", lines="見込み捜査", q=True, cap=52, cell=(1, 0)),
    _c(1, K, lines="やりきれない思い", q=True, cap=58, cell=(0, 1), span=(2, 1)),
], src="国会会議録 平成8年5月14日")
FU["cb13"] = _f(2, "白書が書くこと", "地下鉄の前に", [
    _c(0, H, head="疑い", lines=("松本の事件は", "教団か"), cap=50, cell=(0, 0)),
    _c(1, H, head="足りなかった", lines=("強制捜査に", "入る資料"), cap=50, cell=(1, 0)),
    _c(1, H, head="契機", lines=("事務長の", "事件"), cap=50, cell=(2, 0)),
], src=S_H)
FU["cb15"] = _f(2, "国の検討会", "当時の現場", [
    _c(0, D, lines=("検知や防護、除染といった概念が", "十分に普及しておらず"), q=True, cap=56, cell=(0, 0)),
], src="消防庁 通知 令和元年12月")
FU["cb18"] = _f(2, "院長の書いたこと", "事件のあと", [
    _c(0, S, head="第一報", lines="爆発火災", sub="最初の3人は関係ないと判断", cap=56, cell=(0, 0)),
    _c(1, S, lines="先入観をもたないこと", q=True, cap=50, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_S)
# ── 第11章
FU["cc03"] = _f(3, "心の後遺症", "院長の手記", [
    _c(0, S, head="事件の1か月後", lines="病院の調査", cap=46, cell=(0, 0)),
    _c(1, S, big="2、3割", bcap=84, lines="眠れないなど", cap=42, cell=(1, 0)),
    _c(2, S, head="手記の時点", lines="数人が通院", cap=46, cell=(2, 0)),
], src=S_S)
FU["cc05"] = _f(2, "遺族の手記", "代表の言葉", [
    _c(0, S, lines="2021年11月の手記", cap=42, cell=(0, 0)),
    _c(1, S, head="最高裁で確定", lines="約10億円の支払命令", cap=46, cell=(0, 1)),
    _c(1, S, lines="まだ事件は終わっていない", q=True, cap=58, cell=(0, 2)),
], src=S_S, mute=(1,))
# 🔴 cc10 の時点は ⑥ の頭と公開の直前に当て直す（台本 §0-5）
FU["cc10"] = _f(2, "いまの処分", "公安審査委員会の決定", [
    _c(0, U, big="2026年11月4日", bcap=50, lines=("請求は出た", "決定はまだ"), cap=44, cell=(0, 0)),
    _c(1, U, big="2026年9月4日", bcap=50, lines=("再発防止処分", "の決定"), cap=44, cell=(1, 0)),
], src=S_U)
FU["cc11"] = _f(3, "いまの勧誘", "公安調査庁の説明", [
    _c(1, U, head="主に30歳以下", lines=("名前を隠した", "サークル"), cap=46, cell=(0, 0)),
    _c(1, U, lines=("人間関係を", "深める"), cap=46, cell=(1, 0)),
    _c(1, U, lines=("団体へ", "入会"), cap=46, cell=(2, 0)),
    _c(2, U, lines="ヨーガ、心理学、メンタルヘルス等が学べる", q=True, cap=42, cell=(0, 1), span=(3, 1)),
], [_x(1, "a", "b"), _x(1, "b", "c")], src=S_U, gx=110.0, gy=30.0)
FU["cc12"] = _f(2, "断ると", "勧誘のあと", [
    _c(0, None, lines=("名前を隠した", "サークル"), cap=46, dim=True, cell=(0, 0)),
    _c(0, U, lines=("人間関係を", "深める"), cap=46, cell=(1, 0)),
    _c(0, U, lines=("団体へ", "入会"), cap=46, cell=(2, 0)),
    _c(1, U, lines="今まで学んできたことが無駄になる", q=True, cap=46, cell=(0, 1), span=(3, 1)),
], [_x(0, "a", "b"), _x(0, "b", "c")], src=S_U, mute=(1,), gx=110.0, gy=30.0)
FU["cc14"] = _f(1, "情報の窓口", "情報を受ける所", [
    _c(0, U, lines="公安調査庁の窓口", cap=54, cell=(0, 0)),
    _c(0, None, lines="説明欄へ", cap=54, cell=(1, 0)),
], [_x(0, "a", "b")], src=S_U)
FU["cc15"] = _f(3, "ここまでの答え", "毒と資料と反省", [
    _c(1, None, lines="同じ毒は、前の年に", cap=52, cell=(0, 0), span=(3, 1)),
    _c(2, H, lines="疑いはあった、資料は足りず", cap=44, cell=(0, 1), span=(3, 1)),
    _c(2, H, lines="知識不足", cap=40, cell=(0, 2)),
    _c(2, H, lines="情報不足", cap=40, cell=(1, 2)),
    _c(2, H, lines="権限の制限", cap=40, cell=(2, 2)),
], src=S_H)


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-11-06）：見え方の表 VIEWS＝札の型の表 FU に無いカット（無線帯 8・模式の前半 11＝映像方針 §5-4）
#    札は札の型と同じ部品（`_draw_card`・`_rows`・`_size`）＝門番が測る形（`geo_of`）も同じ＝judge_m30・check_fuda・check_echo がそのまま測る。
#    🔴 人の形・家・顔は描かない（車は外の形だけ・話す人は立場の字だけ）・この回の線の語は札にも絵にも出さない（c202 は駅の点を描かない・c506 は化学式なし）。
# ══════════════════════════════════════════════════════════
def _at(c, x, y):
    """札をその座標（札の真ん中）に置く。"""
    return dict(c, pos=(float(x), float(y)))


def _p(at, fn, arrow=False):
    """絵の部品（段 at から出て残る）。fn() が SVG の字を返す。arrow＝矢印（門番 check_fuda の本数に数える）。"""
    return dict(at=at, fn=fn, arrow=arrow)


def _z(n, t, s, cards=(), parts=(), src="", note="", mute=(), schem=False, band=(), tl=None):
    """1カット。band＝無線帯の行（時刻, 語, 字の大きさ）・tl＝時間の線（門番 ⑤＝dict(kind, ax, pts)）。"""
    cs = tuple(dict(c, id="abcdefgh"[i]) for i, c in enumerate(cards))
    ps = tuple(dict(p, id=f"p{i}") for i, p in enumerate(parts))
    return dict(n=n, t=t, s=s, cards=cs, parts=ps, src=src, note=note, mute=tuple(mute), schem=schem, band=tuple(band), tl=tl)


def _zbox(c):
    w, h = _size(c)
    x, y = c["pos"]
    return (x - w / 2, y - h / 2, w, h)


def _lead(c, x, y):
    """札の上か下の辺から、線の上の点へ（細い線と点）。"""
    bx, by, bw, bh = _zbox(c)
    x0 = min(max(x, bx + 24), bx + bw - 24)
    y0 = by + bh + 8 if y > by + bh else by - 8
    return F.line(x0, y0, x, y, J.TICK, 4) + F.circ(x, y, 12, INK)


def _rot(pts, cx, cy, a):
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def _mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def _wavy(xb, y0, y1, amp=22.0, per=190.0):
    """県境の線（模式＝ゆるい波・実際の形ではない）。"""
    n = int((y1 - y0) / 10)
    return [(xb + amp * math.sin(i * 10.0 / per * 2 * math.pi), y0 + i * 10.0) for i in range(n + 1)]


def _border(xb, y0, y1, hi=False):
    pts = _wavy(xb, y0, y1)
    if hi:
        return F.poly(pts, "none", J.AMBER, 18, op=0.45) + F.poly(pts, "none", J.AMBER, 7)
    return F.poly(pts, "none", J.BG, 14) + F.poly(pts, "none", INK, 6)


# ── 無線帯（c714・c715・c716・c718・c721・c730・c733・c734）＝描き手1つ。同じ帯が段ごとに伸びる・前の段は時刻と短い語で残る・
#    その段の時刻は明るく、右の札へ線でつなぐ（語は右の札だけ＝同じ画面に同じ語を2度出さない）。
#    時刻は音声の時報から（±数十秒＝ref/ep30/sources.md §2）・語は公開の音声を機械で書き起こしたもの（耳で未確認＝了承②）＝「」の札と note で断る
RB = (("8:21", "病人2名"), ("8:23", "同じ件かも"), ("8:24", "ガソリンの匂い"), ("8:31", "目が見えない"), ("8:39", "爆発物"),
      ("8:44", "同時多発"), ("8:53", "防毒マスク"), ("8:58", "また爆発物"), ("9:04", "毒ガス"))
RBX = dict(x=152.0, head=272.0, y0=342.0, dy=58.0, tx=184.0, kx=300.0, kx1=660.0, cap=38.0, ccap=46.0)
S_RB = "公安調査庁 オウム真理教問題デジタルアーカイブの無線指令音声記録"
N_RB = "語は公開の音声を機械で書き起こしたもの・時刻は音声の時報から"


def _rb_y(i):
    return RBX["y0"] + RBX["dy"] * i


def _rb_head():
    col = sc(R)
    return (_icon(dict(icon="radio", cross=False), RBX["x"] + 4, RBX["head"] - 6, col, 0.42)
            + _t(RBX["x"] + 44, RBX["head"] + 13, "警視庁の無線", 36, col, "start", 460))


def _rb_row(i, cur, frm):
    """帯の1段。cur＝このカットで出た段（時刻だけ明るく）。frm＝縦の線をどの段からつなぐか（-1＝見出し・None＝つながない）。"""
    x, y, col = RBX["x"], _rb_y(i), sc(R)
    g = ""
    if frm is not None:
        g += F.line(x, (_rb_y(frm) if frm >= 0 else RBX["head"] + 30) + 14, x, y - 14, col, 6)
    if cur:
        return g + F.circ(x, y, 14, J.AMBER) + _t(RBX["tx"], y + RBX["ccap"] * 0.36, RB[i][0], RBX["ccap"], J.AMBER, "start", 130)
    return (g + F.circ(x, y, 9, col) + _t(RBX["tx"], y + RBX["cap"] * 0.36, RB[i][0], RBX["cap"], J.TICK, "start", 110)
            + _t(RBX["kx"], y + RBX["cap"] * 0.36, RB[i][1], RBX["cap"], INK, "start", 340))


def _rb_link(i, c):
    """その段の時刻から右の札の左の辺へ（帯の語の列の右までは横に引く）。"""
    y = _rb_y(i)
    bx, by, bw, bh = _zbox(c)
    x0, x1, y1 = RBX["tx"] + 120, bx - 14, by + bh / 2
    mid = min(RBX["kx1"], x1)
    return F.poly([(x0, y), (mid, y), (x1, y1)], "none", sc(R), 4) + F.circ(x1, y1, 7, sc(R))


def _rb_view(n, t, s, past, new, cards, mute=(), head_at=0):
    """無線帯の1カット。past＝前のカットまでの段（頭から出る）・new＝((段, 出る段, 札の番号, 縦の線をつなぐ段), …)。"""
    parts = [_p(head_at, _rb_head)]
    last = -1
    for i in past:
        parts.append(_p(0, lambda i=i, f=last: _rb_row(i, False, f)))
        last = i
    for i, at, ci, frm in new:
        parts.append(_p(at, lambda i=i, f=frm: _rb_row(i, True, f)))
        parts.append(_p(at, lambda i=i, c=cards[ci]: _rb_link(i, c)))
    band = tuple((RB[i][0], RB[i][1], RBX["cap"]) for i in past) + tuple((RB[i][0], "", RBX["ccap"]) for i, _a, _c2, _f in new)
    return _z(n, t, s, cards, parts, src=S_RB, note=N_RB, mute=mute, band=band)


_X = 1250.0                 # 無線帯の札の真ん中（右の区画）
VIEWS = {}
VIEWS["c714"] = _rb_view(3, "無線の記録", "あの朝の順番", (), ((0, 2, 1, -1),), [
    _at(_c(1, R, icon="radio", lines=("音声に", "時報が入る"), cap=48), _X, 372),
    _at(_c(2, R, head="八丁堀駅へ", lines="病人2名", q=True, sub=("事件事故かも", "詳細は不明"), cap=64), _X, 640),
], head_at=1)
VIEWS["c715"] = _rb_view(2, "2つ目の駅", "同じ線の別の駅", (0,), ((1, 0, 0, 0),), [
    _at(_c(0, R, head="小伝馬町駅", lines="八丁堀の件と同じかも", cap=56), _X, 430),
    _at(_c(1, R, lines="病人は4人ぐらい", cap=54), _X, 640),
])
VIEWS["c716"] = _rb_view(2, "匂いの知らせ", "3つ目の駅", (0, 1), ((2, 0, 0, 1),), [
    _at(_c(0, R, head="築地駅", lines="ガソリンの匂い", q=True, sub="電車が止まっている", cap=62), _X, 450),
    _at(_c(1, R, lines="最優先で調査せよ", q=True, cap=58), _X, 680),
])
VIEWS["c718"] = _rb_view(2, "苦しむ人", "ホームの様子", (0, 1, 2), ((3, 0, 0, 2),), [
    _at(_c(0, R, lines="小伝馬町駅の駅員から", cap=50), _X, 400),
    _at(_c(1, R, lines="目が見えない", q=True, cap=60), _X, 560),
    _at(_c(1, R, lines="苦しがってる人がいる", q=True, cap=60), _X, 710),
], mute=(1,))
VIEWS["c721"] = _rb_view(2, "爆発物の語", "8時40分の手前", (0, 1, 2, 3), ((4, 0, 0, 3),), [
    _at(_c(0, R, head="本部から各局へ", lines="爆発物を使用した…事件", q=True, cap=70), 1230, 470),
    _at(_c(1, R, icon="speaker", lines="全部の局へ", cap=56), 1230, 700),
])
VIEWS["c730"] = _rb_view(2, "知らせが重なる", "同じ線の駅で", (0, 1, 2, 3, 4), ((5, 0, 0, 4),), [
    _at(_c(0, R, head="日比谷線の各駅で", lines="同時多発", q=True, cap=76), _X, 480),
    _at(_c(1, R, lines="各駅を調べる指示", cap=52), _X, 700),
])
VIEWS["c733"] = _rb_view(2, "2つの指示", "ほぼ同じころに", (0, 1, 2, 3, 4, 5), ((7, 0, 0, 5), (6, 1, 2, None)), [
    _at(_c(0, R, head="本部から各局へ", lines=("爆発物使用の", "…事件"), q=True, cap=52), 1500, 470),
    _at(_c(1, R, lines=("23区内に", "全体の配備"), cap=46), 1500, 720),
    _at(_c(1, R, head="本部の指示", lines="防毒マスク", q=True, sub="むやみに中へ入らない", cap=56), 950, 380),
])
VIEWS["c734"] = _rb_view(2, "毒ガスの語", "9時をすぎて", (0, 1, 2, 3, 4, 5, 6, 7), ((8, 0, 0, 7),), [
    _at(_c(0, R, head="本部の指示", lines="毒ガス事案", q=True, cap=76), _X, 450),
    _at(_c(1, R, lines="手で触ることなく", q=True, sub="マスクは完全に着ける", cap=56), _X, 690),
])


# ── c202 路線の模式＝3つの線が霞ケ関で交わる（角度と長さは模式・駅の点は描かない＝どの駅でまいたかを描かない）・電車の印5つ
MET = (("日比谷線", "#b5b5ac", 62.0, -1), ("丸ノ内線", "#f62e36", -14.0, 1), ("千代田線", "#00bb85", -58.0, 1))   # 名・線の色（いまの東京メトロの色）・角度・名を書く端
MC, MR = (1250.0, 540.0), 330.0


def _met_lines():
    g = ""
    for _n, col, a, _e in MET:
        dx, dy = MR * math.cos(math.radians(a)), MR * math.sin(math.radians(a))
        g += F.line(MC[0] - dx, MC[1] - dy, MC[0] + dx, MC[1] + dy, J.BG, 32) + F.line(MC[0] - dx, MC[1] - dy, MC[0] + dx, MC[1] + dy, col, 18)
    return (g + F.circ(MC[0], MC[1], 30, J.BG2, INK, 8)
            + _t(MC[0] + 141, MC[1] + 51 + 17, "霞ケ関", 48, INK, "middle", 200))


def _met_names():
    g = ""
    for name, col, a, e in MET:
        x, y = MC[0] + e * MR * math.cos(math.radians(a)), MC[1] + e * MR * math.sin(math.radians(a))
        g += _t(x + 22 * e, y + 15, name, 42, col, "start" if e > 0 else "end", 220)
    return g


def _train(cx, cy, col):
    """電車の印（横から見た四角と窓3つ）。"""
    return F.rect(cx - 34, cy - 20, 68, 40, J.BG2, col, 5, rx=9) + "".join(F.rect(cx - 25 + i * 18, cy - 11, 12, 12, col, None, None, rx=2) for i in range(3))


VIEWS["c202"] = _z(2, "3つの路線", "当時の地下鉄", [
    _at(_c(0, None, lines="営団地下鉄", sub="いまの東京メトロ", cap=60), 480, 380),
    _at(_c(1, None, head="電車", big="5本", bcap=96), 480, 620),
], [_p(0, _met_lines), _p(1, _met_names), _p(1, lambda: "".join(_train(480 + (i - 2) * 86.0, 790.0, INK) for i in range(5)))],
    src=S_U, note="模式・路線の形と長さは実際と違う", schem=True)


# ── 時間の線（比例）＝c307 年・c407 時刻・c514 月。位置は値の式（門番 judge_m30 ⑤ が字の値と位置を照らす）
def _lin(d, v):
    return d["x0"] + (v - d["v0"]) * (d["x1"] - d["x0"]) / (d["v1"] - d["v0"])


def _axis(d, ticks, col=None):
    g = F.line(d["x0"], d["y"], d["x1"], d["y"], col or J.TICK, 4)
    return g + "".join(F.line(_lin(d, v), d["y"] - 14, _lin(d, v), d["y"] + 14, col or J.TICK, 4) for v in ticks)


def _bar(d, v0, v1, col, h=52.0):
    x0, x1 = _lin(d, v0), _lin(d, v1)
    return F.rect(x0, d["y"] - h / 2, x1 - x0, h, col, None, None, rx=10, op=0.88)


Y307 = dict(x0=300.0, x1=1620.0, y=560.0, v0=1989.0, v1=1996.0)            # 年（1989年の頭 → 1996年の頭）
V307 = (1989 + 10.5 / 12, 1995.5)                                           # 1989年11月（月の真ん中）・1995年（年の真ん中＝月は書かない）
C307 = [
    _at(_c(0, None, big="1989年11月", lines="弁護士の一家の事件", cap=44, bcap=58), 480, 380),
    _at(_c(1, K, head="局長の答弁", big="5年あまり", bcap=84), 900, 720),
    _at(_c(1, None, big="1995年", lines="検挙", cap=44, bcap=58), 1510, 380),
    # 判決の札は線の下（上の段に置くと 1989年と1995年のあいだの出来事に見えた＝手元の重ね絵）
    _at(_c(2, T, head="判決", lines="一家3人は殺害されていた", cap=44), 1480, 720),
]
VIEWS["c307"] = _z(3, "検挙まで", "長くかかった捜査", C307, [
    _p(0, lambda: _axis(Y307, range(1989, 1997))),
    _p(0, lambda: _lead(C307[0], _lin(Y307, V307[0]), Y307["y"])),
    _p(1, lambda: _bar(Y307, *V307, rc(SRC[K][1])) + _lead(C307[2], _lin(Y307, V307[1]), Y307["y"])),
], src="国会会議録 平成7年10月12日・" + S_T,
    tl=dict(kind="ym", ax=((Y307["v0"], Y307["x0"]), (Y307["v1"], Y307["x1"])), pts=(("1989年11月", _lin(Y307, V307[0])), ("1995年", _lin(Y307, V307[1])))))

Y407 = dict(x0=250.0, x1=1670.0, y=600.0, v0=23 * 60.0, v1=31 * 60.0 + 30)   # 分（6月27日 23:00 → 28日 7:30）
V407 = (23 * 60.0 + 30, 31 * 60.0)                                          # 23:30・翌朝 7:00
C407 = [
    _at(_c(0, K, big="23:30ごろ", lines="消防から松本署へ", cap=46, bcap=66), 430, 400),
    _at(_c(1, K, head="翌朝", big="7:00", lines="310人の体制", cap=52, bcap=76), 1480, 400),
]


def _night():
    d, n = Y407, 40
    w = (d["x1"] - d["x0"]) / n
    g = "".join(F.rect(d["x0"] + i * w, d["y"] - 30, w + 1, 60, _mix("#2c3e6b", "#f2d48a", i / (n - 1)), None, None, op=0.92) for i in range(n))
    g += "".join(F.line(_lin(d, v), d["y"] - 44, _lin(d, v), d["y"] + 44, J.TICK, 6 if v == 24 * 60 else 3) for v in range(24 * 60, 32 * 60, 60))
    mx, my, r = d["x0"] + 30, d["y"] + 110, 30
    moon = [(mx + r * math.cos(math.radians(a)), my + r * math.sin(math.radians(a))) for a in range(40, 321, 10)]
    moon += [(mx + 0.42 * r + 0.78 * r * math.cos(math.radians(a)), my + 0.78 * r * math.sin(math.radians(a))) for a in range(-40, 41, 10)][::-1]
    sx, sy = d["x1"] - 30, d["y"] + 110
    sun = F.circ(sx, sy, 22, "#f2d48a") + "".join(F.line(sx + 32 * math.cos(math.radians(a)), sy + 32 * math.sin(math.radians(a)),
                                                         sx + 46 * math.cos(math.radians(a)), sy + 46 * math.sin(math.radians(a)), "#f2d48a", 6) for a in range(0, 360, 45))
    return g + F.poly(moon, "#cfd8e3", None, close=True) + sun


VIEWS["c407"] = _z(2, "その夜の動き", "翌朝までの体制", C407, [
    _p(0, _night),
    _p(0, lambda: _lead(C407[0], _lin(Y407, V407[0]), Y407["y"])),
    _p(1, lambda: _lead(C407[1], _lin(Y407, V407[1]), Y407["y"])),
], src="国会会議録 平成7年12月1日",
    tl=dict(kind="hm", ax=((Y407["v0"], Y407["x0"]), (Y407["v1"], Y407["x1"])), pts=(("23:30", _lin(Y407, V407[0])), ("7:00", _lin(Y407, V407[1])))))

Y514 = dict(x0=300.0, x1=1620.0, y=520.0, v0=1994 + 5 / 12, v1=1995 + 3 / 12)   # 月（1994年6月の頭 → 1995年4月の頭）
V514 = (1994 + 5.5 / 12, 1995 + 2.5 / 12)                                       # 1994年6月・1995年3月（月の真ん中）
C514 = [
    _at(_c(0, None, big="1994年6月", lines="松本", cap=44, bcap=58), 400, 700),
    _at(_c(0, S, head="母親の手記", lines="捜査の進展はなく", q=True, cap=60), 960, 330),
    _at(_c(1, None, big="1995年3月", lines="地下鉄", cap=44, bcap=58), 1530, 700),
]
VIEWS["c514"] = _z(2, "手記の言葉", "その後の月日", C514, [
    _p(0, lambda: _axis(Y514, [Y514["v0"] + i / 12 for i in range(11)])),
    _p(0, lambda: _bar(Y514, *V514, rc(SRC[S][1]), h=44) + _lead(C514[0], _lin(Y514, V514[0]), Y514["y"])),
    _p(1, lambda: _lead(C514[2], _lin(Y514, V514[1]), Y514["y"])),
], src="公安調査庁 デジタルアーカイブの遺族の手記",
    tl=dict(kind="ym", ax=((Y514["v0"], Y514["x0"]), (Y514["v1"], Y514["x1"])), pts=(("1994年6月", _lin(Y514, V514[0])), ("1995年3月", _lin(Y514, V514[1])))))


# ── 県境の模式＝c315・c316（どこの県とも書かない）・c519（山梨と東京＝札は地名だけ）。県境の形は模式
def _c315_art(hi=False):
    g = _border(1000.0, 262.0, 840.0)
    g += _t(500, 314, "自分の県", 42, J.TICK, "middle", 300) + _t(1500, 314, "ほかの県", 42, J.TICK, "middle", 300)
    return g


def _c315_arrow(hi=False):
    """県の外への矢印と「？」。hi＝c316 で上に重ねる明るい線だけ（「？」は足さない＝2つ重なると門番 layout が鳴る）。"""
    if hi:
        return _arrow(640.0, 640.0, 1400.0, 640.0, J.AMBER, 10, 34)
    return _arrow(640.0, 640.0, 1400.0, 640.0, INK, 8, 34, "22 14") + _qmark(1000.0, 586.0, 76, J.AMBER)


C315 = [
    _at(_c(0, H, lines="県の警察は県の中", cap=56), 500, 440),
    _at(_c(1, H, head="当時の法律", lines="外で動くには理由が要る", cap=48), 1000, 760),
]
VIEWS["c315"] = _z(2, "県ごとの警察", "動ける範囲", C315, [_p(0, _c315_art), _p(1, _c315_arrow, arrow=True)], src=S_H,
                   note="模式・県境の形は実際と違う", schem=True)
VIEWS["c316"] = _z(1, "あとで効く決まり", "県の外へ出るとき", [dict(c, at=0, dim=True) for c in C315], [
    _p(0, _c315_art), _p(0, _c315_arrow, arrow=True),
    _p(0, lambda: _border(1000.0, 262.0, 840.0, hi=True) + _c315_arrow(hi=True), arrow=False),
], src=S_H, note="模式・県境の形は実際と違う", schem=True)

C519 = [_at(_c(0, None, lines="山梨", cap=72), 480, 430), _at(_c(0, None, lines="東京", cap=72), 1440, 430)]


def _c519_stop():
    return (_arrow(1290.0, 610.0, 1000.0, 610.0, INK, 9, 34) + F.line(976.0, 548.0, 976.0, 672.0, J.BG, 22) + F.line(976.0, 548.0, 976.0, 672.0, J.ALERT, 12))


VIEWS["c519"] = _z(2, "県の外へ出るには", "白書の書き方", C519, [
    _p(0, lambda: _border(960.0, 262.0, 840.0)), _p(0, _c519_stop, arrow=True),
    _p(1, lambda: F.circ(1440.0, 690.0, 104, "none", J.AMBER, 8) + _qmark(1440.0, 690.0, 110, J.AMBER)),
], src=S_H, note="模式・県境の形は実際と違う", schem=True)


# ── 土の模式＝c505（土を取る＝道具の形だけ・手は描かない）・c506（土の断面と虫めがね＝化学式を書かない）
SOIL = ("#6b4b30", "#584029", "#46331f")
LEAF = ("#b07a3a", "#8f5f2c", "#c4934a")


def _leaf(cx, cy, a, col):
    """枯れた葉の形（とがった楕円と葉脈）。"""
    pts = [(-46, 0), (-30, -15), (0, -21), (30, -15), (46, 0), (30, 15), (0, 21), (-30, 15)]
    p1, p2 = _rot([(-40, 0), (40, 0)], cx, cy, a)
    return F.poly(_rot(pts, cx, cy, a), col, J.BG, 3, close=True) + F.line(*p1, *p2, J.BG, 3)


def _trowel(cx, cy, a, col):
    """土を取る道具の形（刃と柄だけ・手は描かない）。"""
    p1, p2 = _rot([(52, 0), (160, 0)], cx, cy, a)
    return F.line(*p1, *p2, col, 18) + F.poly(_rot([(-70, 0), (-20, -34), (40, -24), (52, 0), (40, 24), (-20, 34)], cx, cy, a), J.BG2, col, 6, close=True)


def _c505_soil():
    y = 640.0
    top = [(860.0 + i * 20, y + 8 * math.sin(i * 0.7)) for i in range(41)]
    g = F.poly(top + [(1660.0, 790.0), (860.0, 790.0)], SOIL[1], None, close=True, op=0.92) + F.poly(top, "none", SOIL[0], 6)
    for i, (lx, la) in enumerate(((930, 12), (1010, -20), (1100, 34), (1420, -8), (1500, 26), (1590, -30), (1190, -14))):
        g += _leaf(lx, y - 12, la, LEAF[i % 3])
    g += _trowel(1300.0, 590.0, -32.0, INK) + "".join(F.circ(1290 + dx, 590 + dy, 8, SOIL[0]) for dx, dy in ((-20, -6), (6, 4), (-2, -18), (22, -10)))
    return g


C505 = [
    _at(_c(0, K, lines="長野県警", sub="松本の捜査の経験", cap=60), 520, 350),
    _at(_c(0, K, lines="山梨", cap=60), 1400, 350),
    _at(_c(1, K, lines=("枯れた葉の辺り", "その土を採取"), cap=50), 520, 650),
]
VIEWS["c505"] = _z(2, "山梨の土", "県をまたいだ捜査", C505, [
    _p(0, lambda: F.poly(_wavy(1000.0, 262.0, 440.0), "none", J.TICK, 5, dash="14 10")),
    _p(0, lambda: _arrow(_zbox(C505[0])[0] + _zbox(C505[0])[2] + 14, 350.0, _zbox(C505[1])[0] - 14, 350.0, INK, 8, 30), arrow=True),
    _p(1, _c505_soil),
], src="国会会議録 平成7年10月12日", note="模式", schem=True)


def _c506_layers():
    g = ""
    for i, (y0, y1) in enumerate(((470.0, 560.0), (560.0, 660.0), (660.0, 790.0))):
        g += F.rect(880.0, y0, 820.0, y1 - y0, SOIL[i], None, None, op=0.92)
    for lx, la in ((940, 10), (1080, -24), (1560, 18), (1650, -12)):
        g += _leaf(lx, 458.0, la, LEAF[lx % 3])
    return g


def _c506_glass():
    cx, cy, r = 1270.0, 610.0, 105.0
    dots = "".join(F.circ(cx + dx, cy + dy, 5, J.AMBER) for dx, dy in ((-30, -12), (18, 22), (34, -28), (-8, 36), (-40, 30)))
    return (F.circ(cx, cy, r, J.BG2, None, None, op=0.55) + dots + F.circ(cx, cy, r, "none", INK, 10)
            + F.line(cx + r * 0.72, cy + r * 0.72, cx + r * 1.55, cy + r * 1.55, INK, 18))


C506 = [
    _at(_c(0, H, big="1994年11月", lines="科学警察研究所の鑑定", cap=44, bcap=64), 520, 360),
    _at(_c(1, H, lines=("サリンが分解した際にも", "できる化学物質"), q=True, cap=44), 520, 640),
    _at(_c(1, K, lines="まことに微量", q=True, cap=50), 1560, 330),
]
VIEWS["c506"] = _z(2, "土の鑑定", "地下鉄の4か月前", C506, [_p(0, _c506_layers), _p(1, _c506_glass)],
                   src=S_H + "・国会会議録 平成7年10月12日", note="模式", schem=True)


# ── 車の中の話の模式＝c610・c611（車は外の形だけ・顔と名前なし・話す人は立場の字だけ・吹き出しは判決と公安調査庁のまとめの要旨と原文）
CAR = (820.0, 540.0)


def _car():
    cx, cy = CAR
    pts = [(cx - 600, cy + 205), (cx - 600, cy - 30), (cx - 470, cy - 60), (cx - 330, cy - 230), (cx + 330, cy - 230), (cx + 470, cy - 60),
           (cx + 600, cy - 30), (cx + 600, cy + 205)]
    g = F.poly(pts, "none", J.BG, 16, close=True) + F.poly(pts, "none", INK, 7, close=True)
    g += F.circ(cx - 380, cy + 215, 52, J.BG2, INK, 7) + F.circ(cx + 380, cy + 215, 52, J.BG2, INK, 7)
    return g + _t(300.0, 716.0, "教祖", 44, INK, "middle", 200) + _t(1330.0, 716.0, "幹部", 44, INK, "middle", 200)


def _tail(c, x, y, col, n=64.0):
    """吹き出しの尾（札の下の角から、話す人の字の向きへ短く＝長い三角は光の筋に見えた＝手元の重ね絵）。"""
    bx, by, bw, bh = _zbox(c)
    ax, ay = (bx + 30 if x < bx else bx + bw - 30), by + bh - 6
    d = math.hypot(x - ax, y - ay) or 1.0
    return F.poly([(ax - 18, ay), (ax + 18, ay), (ax + (x - ax) / d * n, ay + (y - ay) / d * n)], J.BG2, col, 4, close=True, op=0.9)


C610 = [
    _at(_c(0, T, lines=("強制捜査に", "どうするか"), cap=44), 640, 410),
    _at(_c(1, T, lines="地下鉄に…", cap=52), 1060, 500),
]
VIEWS["c610"] = _z(2, "車の中で", "教祖と幹部", C610, [
    _p(0, _car), _p(0, lambda: _tail(C610[0], 312.0, 672.0, rc(SRC[T][1]))), _p(1, lambda: _tail(C610[1], 1316.0, 672.0, rc(SRC[T][1]))),
], src=S_T, note="模式・吹き出しは判決の要旨", schem=True)
C611 = [dict(c, at=0, dim=True) for c in C610] + [
    _at(_c(0, U, lines=("それはパニックに", "なるかもしれないなあ"), q=True, cap=44), 610, 585),
    _at(_c(1, U, head="提案した幹部", big="1995年4月", lines=("亡くなり", "裁判なし"), cap=44, bcap=58), 1650, 520),
]
VIEWS["c611"] = _z(2, "教祖の答え", "提案のその後", C611, [
    _p(0, _car), _p(0, lambda: _tail(C611[2], 300.0, 676.0, rc(SRC[U][1]))),
], src=S_U, note="模式", mute=(0,), schem=True)


def _cid(view):
    return "c" + view[3:] if view.startswith(("fu_", "zu_")) else view


def _ids(fu):
    return [c["id"] for c in fu["cards"]] + [a["id"] for a in fu.get("arrows", ())] + [p["id"] for p in fu.get("parts", ())]


def fu(cid):
    """SPEC の fig＝("m30", …)。段は札の at から組む。"""
    d = FU[cid]
    steps = []
    for i in range(d["n"]):
        on = {c["id"]: "on" for c in d["cards"] if c["at"] == i}
        on.update({a["id"]: "on" for a in d["arrows"] if a["at"] == i})
        steps.append(dict(state=on))
    # view は「fu_205」の形（門番 wording が kw の字からカット番号を拾う＝画面に出ない字でも鳴る）
    return ("m30", dict(view="fu_" + cid[1:], steps=steps, note=d["note"], src=d["src"], mute=list(d["mute"])))


def fu_spec(cid, ground, **kw):
    """章ファイルの SPEC の1行＝`"c305": fu_spec("c305", ss.gr("stock/ga1"))`。kw＝`bias=` など。"""
    d = FU[cid]
    return dict(ground, t=d["t"], s=d["s"], fig=fu(cid), **kw)


def zu(cid):
    """🆕 ⑤b-5：見え方の表 VIEWS のカットの fig＝("m30", …)。段は札と部品の at から組む。view は「zu_714」の形（fu_ と同じ理由）。"""
    d = VIEWS[cid]
    steps = [dict(state={x["id"]: "on" for x in d["cards"] + d["parts"] if x["at"] == i}) for i in range(d["n"])]
    return ("m30", dict(view="zu_" + cid[1:], steps=steps, note=d["note"], src=d["src"], mute=list(d["mute"])))


def zu_spec(cid, ground, **kw):
    """章ファイルの SPEC の1行＝`"c714": zu_spec("c714", ss.gr("ks1"))`。"""
    d = VIEWS[cid]
    return dict(ground, t=d["t"], s=d["s"], fig=zu(cid), **kw)


def stage_art(view, prev, st):
    if view in VIEWS:
        # 部品（線・帯・印）が先・札が上
        d = VIEWS[view]
        s = [p["fn"]() for p in d["parts"] if _on(prev, st, p["id"])]
        return s + [_draw_card(c, _zbox(c)) for c in d["cards"] if _on(prev, st, c["id"])]
    d = FU[view]
    boxes, _bb, k = layout(d)
    s = []
    for c in d["cards"]:
        if _on(prev, st, c["id"]):
            s.append(_draw_card(c, boxes[c["id"]], k))
    for a in d["arrows"]:
        if _on(prev, st, a["id"]):
            s.append(_draw_arrow(a, boxes, k))
    return s


def quote_lines(view):
    """原文どおりに出す字（門番 echo の例外＝mute のあるカットだけ＝その行の字幕は消える）。"""
    d = FU.get(_cid(view)) or VIEWS.get(_cid(view))
    if not d or not d["mute"]:
        return []
    return [ln for c in d["cards"] if c["q"] for ln in _qwrap(c["lines"])]


def m30(view, steps, start=None, rel=(), note="", src="", mute=()):
    """30本目 札の型と見え方の表。view は `fu()` の「fu_205」か `zu()` の「zu_714」の形（表の鍵はカットの番号）。steps＝語りの行ごとの段。"""
    view = _cid(view)
    if view not in FU and view not in VIEWS:
        raise ValueError(f"m30：表 FU にも見え方の表 VIEWS にも無い {view!r}")
    d = FU.get(view) or VIEWS[view]
    zv = view in VIEWS
    if zv and d["schem"] and "模式" not in note:
        raise ValueError(f"m30：{view} は模式＝note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    ids = _ids(d)
    cur = {k: "off" for k in ids}
    st0 = dict(cur, **(start or {}))
    states, c2 = [], dict(st0)
    for st in steps:
        c2 = dict(c2, **(st.get("state") or {}))
        for k, v in c2.items():
            if k not in ids or v not in ONOFF:
                raise ValueError(f"m30：{view} の欄 {k}={v!r} は知らない")
        states.append(dict(c2))
    g = []
    if zv:
        for c in d["cards"]:
            x, y, w, h = _zbox(c)
            if x < F.BX0 or x + w > F.BX1 or y < F.BY0 or y + h > F.BY1 - 34:
                raise ValueError(f"m30：{view} の札 {c['id']} が本体の外（{x:.0f},{y:.0f}〜{x + w:.0f},{y + h:.0f}）")
        if d["schem"]:
            g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, "模式", 1000, cap=30, col=J.TICK, ol=OL))
    else:
        _boxes, bb, _k = layout(d)
        if bb[2] > AREA_W or bb[3] > AREA_H:
            raise ValueError(f"m30：{view} の札が広すぎる（幅 {bb[2]:.0f}／{AREA_W:.0f}・高さ {bb[3]:.0f}／{AREA_H:.0f}）")
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK, ol=OL))
    stages, prev = [], st0
    for stt in states:
        stages.append("".join(stage_art(view, prev, stt)) or " ")
        prev = stt
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = []
    f.mech = dict(kind="m30", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=[], lab="", note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view), texts_all=svg_texts("".join(stages)), sns=False)
    return f


def geo_of(view):
    if view in VIEWS:
        # 🆕 ⑤b-5：札の型と同じ形＋無線帯の行（band）・時間の線（tl）。拡大率は 1（札の字の大きさは表に書いた値のまま）
        d = VIEWS[view]
        boxes = {c["id"]: _zbox(c) for c in d["cards"]}
        x0 = min(b[0] for b in boxes.values())
        y0 = min(b[1] for b in boxes.values())
        bb = (x0, y0, max(b[0] + b[2] for b in boxes.values()) - x0, max(b[1] + b[3] for b in boxes.values()) - y0)
        return dict(view=view, src={key: tuple(v) for key, v in SRC.items()}, vsrc=tuple(sorted({c["who"] for c in d["cards"] if c["who"]})),
                    quotes=tuple("".join(c["lines"]) for c in d["cards"] if c["q"]), mute=d["mute"], n=d["n"],
                    cards=tuple(dict(id=c["id"], who=c["who"], q=c["q"], dim=c["dim"], rows=tuple(_rows(c))) for c in d["cards"]),
                    narrows=sum(1 for p in d["parts"] if p["arrow"]), bbox=bb, boxes=boxes, k=1.0, band=d["band"], tl=d["tl"], schem=d["schem"])
    d = FU[view]
    boxes, bb, k = layout(d)
    return dict(view=view, src={key: tuple(v) for key, v in SRC.items()}, vsrc=tuple(sorted({c["who"] for c in d["cards"] if c["who"]})),
                quotes=tuple("".join(c["lines"]) for c in d["cards"] if c["q"]), mute=d["mute"], n=d["n"],
                cards=tuple(dict(id=c["id"], who=c["who"], q=c["q"], dim=c["dim"], rows=tuple(_rows(c, k))) for c in d["cards"]),
                narrows=len(d["arrows"]), bbox=bb, boxes=boxes, k=k)
