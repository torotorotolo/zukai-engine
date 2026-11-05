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
"""
from __future__ import annotations

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


def _cid(view):
    return "c" + view[3:] if view.startswith("fu_") else view


def _ids(fu):
    return [c["id"] for c in fu["cards"]] + [a["id"] for a in fu["arrows"]]


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


def stage_art(view, prev, st):
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
    d = FU.get(_cid(view))
    if not d or not d["mute"]:
        return []
    return [ln for c in d["cards"] if c["q"] for ln in _qwrap(c["lines"])]


def m30(view, steps, start=None, rel=(), note="", src="", mute=()):
    """30本目 札の型。view は `fu()` の「fu_205」の形（表 FU の鍵はカットの番号）。steps＝語りの行ごとの段。"""
    view = _cid(view)
    if view not in FU:
        raise ValueError(f"m30：表 FU に無い {view!r}")
    d = FU[view]
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
    _boxes, bb, _k = layout(d)
    if bb[2] > AREA_W or bb[3] > AREA_H:
        raise ValueError(f"m30：{view} の札が広すぎる（幅 {bb[2]:.0f}／{AREA_W:.0f}・高さ {bb[3]:.0f}／{AREA_H:.0f}）")
    g = [F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK, ol=OL)]
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
    d = FU[view]
    boxes, bb, k = layout(d)
    return dict(view=view, src={key: tuple(v) for key, v in SRC.items()}, vsrc=tuple(sorted({c["who"] for c in d["cards"] if c["who"]})),
                quotes=tuple("".join(c["lines"]) for c in d["cards"] if c["q"]), mute=d["mute"], n=d["n"],
                cards=tuple(dict(id=c["id"], who=c["who"], q=c["q"], dim=c["dim"], rows=tuple(_rows(c, k))) for c in d["cards"]),
                narrows=len(d["arrows"]), bbox=bb, boxes=boxes, k=k)
