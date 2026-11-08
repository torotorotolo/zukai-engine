# -*- coding: utf-8 -*-
"""mech31.py — 31本目（全日空機雫石衝突事故・1971-07-30・岩手県雫石町の上空）「札の型」（2026-11-08 新設・⑤b-4＝札113）。
30本目 `tools/mech30.py` の型を写した（描き手・拡大率・格子・矢印は同じ式）。30本目の表（FU・VIEWS・SRC）は mech30 に残したまま＝31本目の章ファイルは m31 だけを引く。

■ 何か
  映像方針 §5-4 の「札の型」＝**見出し＋札1〜4枚＋矢印0〜2本＋誰の記録かの色＝描き手1つ**。カットごとの関数は書かない＝表 `FU` の1行が1カット。
  段の層（その行から出て残る）・動く部品は使わない。再現イラストではない＝「再現」の札は出さない。
  🔴 **地は写真**（`cuts.ss.gr`＝暗くするだけ・方眼と章の色なし・静止）＝字は暗い縁取り（OL）・札の地は半ば透ける紺（`_panel`）。8:1 は check_ground。
  🔴🔴 **この回の線＝人の名前を出さない**（亡くなった方・遺族・操縦者・乗員・役人・裁判官・弁護人は立場だけ）。判決の記号の字（Ｃ三佐ほか）も出さない。
     **人の形・顔・家を描かない**（印は物の形だけ＝飛行機は上から見た形・人は乗せない）。名前の網＝`ref/ep31/v2_build/namecheck31.py`。
  🔴 言い切らない線（台本 第2版のとおり）：訓練生の一審・二審の結果は出さない（c908）・旅客機の操縦者の見張りの違反は最高裁が判断していない（c627）・
     「7秒」は報告書の推定（元委員長の説明）・防衛庁は時刻に異論（c621〜c626）・目撃談（c802・c812）は噂の札＝灰色の地（事実の図と違う見た目）。
  🔴 **色は「誰の記録か」**（SRC＝新しい色の値は足していない）：最高裁の判決＝紫／国会＝緑／運輸白書＝青／国交省＝水色／法律＝茶／町の頁＝桃／会社の頁＝橙。
     意味の色＝黄 AMBER（数・日付・時刻）。誰のものでもない札は線の色。噂の札だけ灰色。
  🔴 札の中の数字と原文どおりの字（`q=True`＝「」が付く）は門番の側 `check_mech.REC_M31` が別に持つ＝描く側の表を書き換えると鳴る。
     原文との照合は `ref/ep31/eizou_build/rec31_src.py`（git の外の資料を読む＝手元だけ）。字数と字の大きさは `tools/check_fuda.py`。

■ 表の書き方（30本目と同じ）
  `FU["c305"] = _f(2, "見出し", "副題", [_c(at=0, who=T, head="…", big="…", lines=("…",), cell=(0, 0)), …], [_x(1, "a", "b", t="…")], src="…")`
    先頭の数 … 段の数＝語りの行の数（行より多いと行の間に等間隔で挟む＝scene_jiko.stage_times）
    at    … その札が出る段（語りの行の番号）。札の id は書いた順に a・b・c…／矢印は x・y
    cell  … 格子の場所（列, 行）・span＝（列の数, 行の数）。列の幅と行の高さは中身の字で決まる（枠の中を空けない＝門番 box）
    mute  … 札の原文を読む行（字幕を消す＝feedback-no-subtitle-when-onscreen）。mute があるカットの `q=True` の字だけ門番 echo の例外
  SPEC は `"c305": fu_spec("c305", ss.gr("a1"))`。
"""
from __future__ import annotations

import re

import jiko_style as J
import titan_fig as F
from mech21 import _arrow, _on, _qmark, _xmark
from mech24 import _w, rc
from mech27 import CX, INK, OL, ONOFF, _panel, _t, svg_texts
from mech30 import ICONS as _ICONS30

# 誰の記録か（名・ROLE か J の名）。同じ色の鍵は同じ画面に出さない（門番が見る）
SRC = dict(
    hanketsu=("最高裁の判決", "tsb"),
    kokkai=("国会", "ntsb"),
    hakusho=("運輸白書", "uscg"),
    kuni=("国交省", "ship"),
    houki=("法律", "DOC"),
    machi=("町の頁", "bldg_a"),
    kaisha=("会社の頁", "company"),
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
    cs = tuple(dict(c, id="abcdefgh"[i]) for i, c in enumerate(cards))
    xs = tuple(dict(a, id="xyzw"[i]) for i, a in enumerate(arrows))
    return dict(n=n, t=t, s=s, cards=cs, arrows=xs, src=src, note=note, mute=tuple(mute), gx=gx, gy=gy)


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
#  印（人の形・顔・家は描かない＝線と四角だけ。ICON_W×ICON_H に収まる）。30本目の形（物の形だけ＝回をまたぐ）＋31本目の形
# ══════════════════════════════════════════════════════════
def _i_plane(cx, cy, col):
    """飛行機を上から見た形（機種を描き分けない・人を乗せない）。機首が上。"""
    pts = [(0, -62), (8, -52), (9, -12), (66, 14), (66, 26), (9, 14), (7, 40), (26, 52), (26, 60), (0, 56), (-26, 60), (-26, 52), (-7, 40), (-9, 14),
           (-66, 26), (-66, 14), (-9, -12), (-8, -52)]
    return F.poly([(cx + x, cy + y) for x, y in pts], J.BG2, col, 6, close=True)


def _i_ndb(cx, cy, col):
    """地上の無線の局（塔と、外へ広がる電波の弧）。"""
    g = F.poly([(cx - 26, cy + 60), (cx, cy - 34), (cx + 26, cy + 60)], "none", col, 7) + F.line(cx - 15, cy + 22, cx + 15, cy + 22, col, 5)
    g += F.circ(cx, cy - 40, 9, col)
    for r in (30, 52):
        g += F.poly([(cx - r * 0.85, cy - 40 - r * 0.53), (cx - r, cy - 40), (cx - r * 0.85, cy - 40 + r * 0.53)], "none", col, 5)
        g += F.poly([(cx + r * 0.85, cy - 40 - r * 0.53), (cx + r, cy - 40), (cx + r * 0.85, cy - 40 + r * 0.53)], "none", col, 5)
    return g


def _i_map(cx, cy, col):
    """折った地図（線は描かない＝J11L の載らない地図）。"""
    return (F.poly([(cx - 64, cy - 44), (cx - 22, cy - 56), (cx + 22, cy - 44), (cx + 64, cy - 56), (cx + 64, cy + 44), (cx + 22, cy + 56), (cx - 22, cy + 44),
                    (cx - 64, cy + 56)], J.BG2, col, 6, close=True)
            + F.line(cx - 22, cy - 56, cx - 22, cy + 44, col, 4) + F.line(cx + 22, cy - 44, cx + 22, cy + 56, col, 4))


ICONS = dict(_ICONS30, plane=_i_plane, ndb=_i_ndb, map=_i_map)


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
#  表（1行が1カット）。カットの順＝一覧 `ref/ep31/eizou_list31.md`。字は語りと同じ字面を避ける（門番 echo）・見出しと重ねない（門番 dup）
#  出典の行は束の書き方（`ref/ep31/assets.json` の credit）と同じ形＝西暦・院と委員会（`ref/ep31/sources.md §7`）
# ══════════════════════════════════════════════════════════
T, K, H, KU, L, M, KS = "hanketsu", "kokkai", "hakusho", "kuni", "houki", "machi", "kaisha"
S_J = "最高裁判所 第一小法廷 判決（1983年9月22日）"
S_W = "運輸省『昭和47年度 運輸白書』"
S_MLIT = "国土交通省の頁（民間訓練試験空域）"
S_LAW = "航空法 第76条の2"
# 国会会議録の会議（記号＝issueID → 出典の行）。院と委員会は sources.md §7・束の出典の行と同じ書き方
KKM = {
    "106614889X00119710802": "1971年8月2日 参議院 内閣委員会",
    "106613830X00219710802": "1971年8月2日 参議院 運輸委員会",
    "106603843X00119710804": "1971年8月4日 衆議院 連合審査会",
    "106613843X00119710805": "1971年8月5日 参議院 連合審査会",
    "106604720X00219710810": "1971年8月10日 衆議院 地方行政委員会",
    "106604889X00519710816": "1971年8月16日 衆議院 内閣委員会",
    "106613830X00319710816": "1971年8月16日 参議院 運輸委員会",
    "106614889X00419711007": "1971年10月7日 参議院 内閣委員会",
    "106814103X01219720524": "1972年5月24日 参議院 決算委員会",
    "106904889X00319720817": "1972年8月17日 衆議院 内閣委員会",
    "106914889X00219720823": "1972年8月23日 参議院 内閣委員会",
    "107105266X00619730308": "1973年3月8日 衆議院 予算委員会第一分科会",
    "107113830X00919730424": "1973年4月24日 参議院 運輸委員会",
    "107114103X00719730509": "1973年5月9日 参議院 決算委員会",
    "107503830X00819750314": "1975年3月14日 衆議院 運輸委員会",
    "107503830X00919750318": "1975年3月18日 衆議院 運輸委員会",
    "110304889X00619851210": "1985年12月10日 衆議院 内閣委員会",
    "112214103X00219911217": "1991年12月17日 参議院 決算委員会",
}


def kk(*ids):
    """国会会議録の出典の行（会議が2つなら「・」でつなぐ）。"""
    return "国会会議録（" + "・".join(KKM[i] for i in ids) + "）"


FU = {}
# ── 第1章
FU["c209"] = _f(3, "乗っていた2人", "階級の記録", [
    _c(1, K, head="編隊長機の教官", lines="一等空尉", icon="plane", cap=60, cell=(0, 0)),
    _c(1, K, head="訓練機の訓練生", lines="二等空曹", icon="plane", cap=60, cell=(1, 0)),
], src=kk("106614889X00119710802"))
# ── 第2章
FU["c303"] = _f(2, "訓練空域の決め方", "松島の場合", [
    _c(0, K, head="防衛局長の説明", lines="方面航空司令官", sub="方面隊の空域を定める", cell=(0, 0)),
    _c(1, K, lines="第四航空団の司令", sub="自分の空域を定める", cell=(1, 0)),
    _c(1, K, big="5つ", lines="名のついた空域", cell=(2, 0)),
], [_x(1, "a", "b"), _x(1, "b", "c")], src=kk("106613843X00119710805"), gx=120)
FU["c316"] = _f(2, "教官の受け取り方", "空域の名から", [
    _c(0, T, head="臨時の空域", lines="盛岡", cap=64, cell=(0, 0)),
    _c(0, T, head="教官の考え", lines="盛岡のあたり", cell=(1, 0)),
    _c(1, T, head="教官が思っていた J11L", lines=("盛岡市街の上空", "ほぼ南北"), sub="判決「誤った認識」", cell=(0, 1), span=(2, 1)),
], [_x(0, "a", "b")], src=S_J)
FU["c327"] = _f(2, "判決の言葉", "幹部たちについて", [
    _c(0, T, head="最高裁の判決", lines="まったく配慮していなかった", q=True, sub="J11L との位置関係", cap=60, cell=(0, 0)),
], src=S_J, mute=(1,))


# ══════════════════════════════════════════════════════════
#  見え方の表 VIEWS（札の型の表に無いカット＝⑤b-5 の模式と型の図で足す）。札は札の型と同じ部品＝門番が測る形も同じ
# ══════════════════════════════════════════════════════════
VIEWS = {}


def _at(c, x, y):
    """札をその座標（札の真ん中）に置く。"""
    return dict(c, pos=(float(x), float(y)))


def _p(at, fn, arrow=False):
    """絵の部品（段 at から出て残る）。fn() が SVG の字を返す。arrow＝矢印（門番 check_fuda の本数に数える）。"""
    return dict(at=at, fn=fn, arrow=arrow)


def _z(n, t, s, cards=(), parts=(), src="", note="", mute=(), schem=False, band=(), tl=None):
    """1カット。band＝帯の行（時刻, 語, 字の大きさ）・tl＝時間の線（門番 ⑤＝dict(kind, ax, pts)）。"""
    cs = tuple(dict(c, id="abcdefgh"[i]) for i, c in enumerate(cards))
    ps = tuple(dict(p, id=f"p{i}") for i, p in enumerate(parts))
    return dict(n=n, t=t, s=s, cards=cs, parts=ps, src=src, note=note, mute=tuple(mute), schem=schem, band=tuple(band), tl=tl)


def _zbox(c):
    w, h = _size(c)
    x, y = c["pos"]
    return (x - w / 2, y - h / 2, w, h)


# ══════════════════════════════════════════════════════════
#  配線（SPEC の fig・段・門番が測る形）
# ══════════════════════════════════════════════════════════
def _cid(view):
    return "c" + view[3:] if view.startswith(("fu_", "zu_")) else view


def _ids(fu):
    return [c["id"] for c in fu["cards"]] + [a["id"] for a in fu.get("arrows", ())] + [p["id"] for p in fu.get("parts", ())]


def fu(cid):
    """SPEC の fig＝("m31", …)。段は札の at から組む。"""
    d = FU[cid]
    steps = []
    for i in range(d["n"]):
        on = {c["id"]: "on" for c in d["cards"] if c["at"] == i}
        on.update({a["id"]: "on" for a in d["arrows"] if a["at"] == i})
        steps.append(dict(state=on))
    # view は「fu_205」の形（門番 wording が kw の字からカット番号を拾う＝画面に出ない字でも鳴る）
    return ("m31", dict(view="fu_" + cid[1:], steps=steps, note=d["note"], src=d["src"], mute=list(d["mute"])))


def fu_spec(cid, ground, **kw):
    """章ファイルの SPEC の1行＝`"c305": fu_spec("c305", ss.gr("a1"))`。kw＝`bias=` など。"""
    d = FU[cid]
    return dict(ground, t=d["t"], s=d["s"], fig=fu(cid), **kw)


def zu(cid):
    """見え方の表 VIEWS のカットの fig＝("m31", …)。段は札と部品の at から組む。view は「zu_714」の形（fu_ と同じ理由）。"""
    d = VIEWS[cid]
    steps = [dict(state={x["id"]: "on" for x in d["cards"] + d["parts"] if x["at"] == i}) for i in range(d["n"])]
    return ("m31", dict(view="zu_" + cid[1:], steps=steps, note=d["note"], src=d["src"], mute=list(d["mute"])))


def zu_spec(cid, ground, **kw):
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


def m31(view, steps, start=None, rel=(), note="", src="", mute=()):
    """31本目 札の型と見え方の表。view は `fu()` の「fu_205」か `zu()` の「zu_714」の形（表の鍵はカットの番号）。steps＝語りの行ごとの段。"""
    view = _cid(view)
    if view not in FU and view not in VIEWS:
        raise ValueError(f"m31：表 FU にも見え方の表 VIEWS にも無い {view!r}")
    d = FU.get(view) or VIEWS[view]
    zv = view in VIEWS
    if zv and d["schem"] and "模式" not in note:
        raise ValueError(f"m31：{view} は模式＝note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    ids = _ids(d)
    cur = {k: "off" for k in ids}
    st0 = dict(cur, **(start or {}))
    states, c2 = [], dict(st0)
    for st in steps:
        c2 = dict(c2, **(st.get("state") or {}))
        for k, v in c2.items():
            if k not in ids or v not in ONOFF:
                raise ValueError(f"m31：{view} の欄 {k}={v!r} は知らない")
        states.append(dict(c2))
    g = []
    if zv:
        for c in d["cards"]:
            x, y, w, h = _zbox(c)
            if x < F.BX0 or x + w > F.BX1 or y < F.BY0 or y + h > F.BY1 - 34:
                raise ValueError(f"m31：{view} の札 {c['id']} が本体の外（{x:.0f},{y:.0f}〜{x + w:.0f},{y + h:.0f}）")
        if d["schem"]:
            g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, "模式", 1000, cap=30, col=J.TICK, ol=OL))
    else:
        _boxes, bb, _k = layout(d)
        if bb[2] > AREA_W or bb[3] > AREA_H:
            raise ValueError(f"m31：{view} の札が広すぎる（幅 {bb[2]:.0f}／{AREA_W:.0f}・高さ {bb[3]:.0f}／{AREA_H:.0f}）")
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK, ol=OL))
    stages, prev = [], st0
    for stt in states:
        stages.append("".join(stage_art(view, prev, stt)) or " ")
        prev = stt
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = []
    f.mech = dict(kind="m31", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=[], lab="", note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view), texts_all=svg_texts("".join(stages)), sns=False)
    return f


def geo_of(view):
    if view in VIEWS:
        # 札の型と同じ形＋帯の行（band）・時間の線（tl）。拡大率は 1（札の字の大きさは表に書いた値のまま）
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
