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

import math
import re

import jiko_style as J
import titan_fig as F
from mech21 import _arrow, _on, _qmark, _xmark
from mech24 import _w, rc
from mech27 import CX, INK, OL, ONOFF, _panel, _t, svg_texts
from mech30 import ICONS as _ICONS30
# 🆕 ⑤b-5：時間の線と棒の式（30本目と同じ式＝回をまたいで同じ・門番 judge ⑤ は同じ決めを自分で計算する＝描く側を引かない）
from mech30 import _axis, _bar, _ev, _lin, _mix, _y0, _yd  # noqa: F401

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
S_MLIT = "国土交通省 記者発表（2002年9月4日）"
S_LAW = "衆議院「法律第五十八号（昭和50年7月10日）」"
S_TOWN = "雫石町の頁"
S_ANA = "全日本空輸の頁（2026年11月）"
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
FU["c202"] = _f(2, "旅客機の道", "2つの点を結ぶ", [
    _c(0, T, head="函館", lines="NDB", icon="ndb", cap=60, cell=(0, 0)),
    _c(0, T, head="松島", lines="NDB", icon="ndb", cap=60, cell=(1, 0)),
    _c(1, T, big="J11L", lines="高い空の直行の道", cell=(0, 1), span=(2, 1)),
], [_x(1, "a", "b", head=False)], src=S_J)
FU["c203"] = _f(2, "NDB とは", "電波で道を示す", [
    _c(0, None, head="地上の局", lines="電波を出し続ける", icon="ndb", cell=(0, 0)),
    _c(1, None, head="旅客機", lines="点から点へ", icon="plane", cell=(1, 0)),
], [_x(1, "b", "a", t="その方角へ")], src=kk("106613843X00119710805"))
FU["c209"] = _f(3, "乗っていた2人", "階級の記録", [
    _c(1, K, head="編隊長機の教官", lines="一等空尉", icon="plane", cap=60, cell=(0, 0)),
    _c(1, K, head="訓練機の訓練生", lines="二等空曹", icon="plane", cap=60, cell=(1, 0)),
], src=kk("106614889X00119710802"))
FU["c213"] = _f(2, "空の使い分け", "はずだった形", [
    _c(0, None, head="旅客機", lines="管制の道", sub="J11L", icon="plane", cell=(0, 0)),
    _c(1, None, head="戦闘機", lines="訓練空域", icon="plane", cell=(1, 0)),
    _c(1, K, head="総理大臣の答弁", lines="航空路とは別の地域", cell=(0, 1), span=(2, 1)),
], src=kk("106603843X00119710804"))
FU["c214"] = _f(2, "1つ目の問い", "その朝の訓練空域", [
    _c(1, None, lines=("訓練の空は", "どう決まったのか"), cap=72, cell=(0, 0)),
], src=kk("106603843X00119710804"))
# ── 第2章
FU["c303"] = _f(2, "訓練空域の決め方", "松島の場合", [
    _c(0, K, head="防衛局長の説明", lines="方面航空司令官", sub="方面隊の空域を定める", cell=(0, 0)),
    _c(1, K, lines="第四航空団の司令", sub="自分の空域を定める", cell=(1, 0)),
    _c(1, K, big="5つ", lines="名のついた空域", cell=(2, 0)),
], [_x(1, "a", "b"), _x(1, "b", "c")], src=kk("106613843X00119710805"), gx=120)
FU["c305"] = _f(3, "臨時の空域", "立案した人", [
    _c(1, T, head="飛行班長補佐", lines="三等空佐", cap=60, cell=(0, 0)),
    _c(2, T, head="急いで思い立つ", big="1か所", lines="臨時の訓練空域", sub="訓練計画を消化するため", cell=(1, 0)),
], [_x(2, "a", "b")], src=S_J)
FU["c310"] = _f(2, "伝えられた先", "戦闘機の課程", [
    _c(0, T, head="補佐", lines="同じやり方で伝達", cell=(0, 0)),
    _c(1, T, head="主任教官", lines=("位置と範囲を", "まったく確かめず"), cell=(1, 0)),
], [_x(0, "a", "b")], src=S_J)
FU["c314"] = _f(2, "ほかの幹部", "最高裁の見方", [
    _c(0, T, head="幹部ら", lines="説明を聞くのみ", sub="安易に了承", cell=(0, 0)),
    _c(1, T, head="立案した補佐", lines="明確な空域を観念せず", q=True, cell=(1, 0)),
], src=S_J)
FU["c316"] = _f(2, "教官の受け取り方", "空域の名から", [
    _c(0, T, head="臨時の空域", lines="盛岡", cap=64, cell=(0, 0)),
    _c(0, T, head="教官の考え", lines="盛岡のあたり", cell=(1, 0)),
    _c(1, T, head="教官が思っていた J11L", lines=("盛岡市街の上空", "ほぼ南北"), sub="判決「誤った認識」", cell=(0, 1), span=(2, 1)),
], [_x(0, "a", "b")], src=S_J)
FU["c317"] = _f(2, "法廷での話", "一審の公判", [
    _c(0, T, head="教官の話", lines="漠然と考えていた", cell=(0, 0)),
    _c(1, T, head="最高裁", lines="信用できる", cell=(1, 0)),
], [_x(1, "a", "b")], src=S_J)
FU["c321"] = _f(1, "その朝の1回目", "判決の認定", [
    _c(0, T, head="空域「盛岡」で", lines=("午前中の訓練の際は", "無事帰投"), q=True, cap=58, cell=(0, 0)),
], src=S_J)
FU["c324"] = _f(2, "1年あまりのち", "防衛庁の答弁", [
    _c(1, K, head="防衛庁の参事官", lines="臨時に横手の空域を指定", q=True, cell=(0, 0)),
    _c(1, K, head="設定の点では", lines="間違いなかった", sub="と考えている", cell=(1, 0)),
], src=kk("106904889X00319720817"), mute=(1,))
FU["c327"] = _f(2, "判決の言葉", "幹部たちについて", [
    _c(0, T, head="最高裁の判決", lines="まったく配慮していなかった", q=True, sub="J11L との位置関係", cap=60, cell=(0, 0)),
], src=S_J, mute=(1,))
FU["c328"] = _f(3, "1つ目の答え", "前半", [
    _c(2, T, head="空域の示し方", lines="地図の上で", sub="J11L は載っていない", icon="map", cell=(0, 0)),
    _c(2, T, head="飛行班長", lines="検討なしに承認", cell=(1, 0)),
], [_x(2, "a", "b")], src=S_J)
# ── 第3章
FU["c412"] = _f(2, "位置を見失ったわけ", "報告書の推定原因", [
    _c(0, H, head="地文航法だけで訓練", lines=("地上の景色を", "目で見て位置を知る"), sub="狭い空域・高い所で", cell=(0, 0)),
    _c(1, H, lines="位置を確かめられず", cell=(1, 0)),
], [_x(1, "a", "b")], src=S_W)
FU["c414"] = _f(2, "常設の訓練空域", "防衛庁の参事官", [
    _c(0, K, head="常設の空域", big="5か所", cell=(0, 0)),
    _c(1, K, head="ルートの中心線から", big="約9キロ", lines="離れた範囲で訓練", sub="5海里", cell=(1, 0)),
], src=kk("106904889X00319720817"))
FU["c415"] = _f(3, "パイロットへの指導", "防衛庁の説明", [
    _c(0, K, head="指導", lines=("まず自分の位置を確認", "ルートは直角に横切る"), cell=(0, 0)),
    _c(1, K, head="参事官", lines=("教官機の行動に", "適当でないものがあった"), q=True, cell=(1, 0)),
], src=kk("106904889X00319720817"), mute=(1,))
FU["c416"] = _f(3, "教官の義務", "最高裁の判断", [
    _c(0, T, lines="見張りの義務", cap=58, cell=(0, 0)),
    _c(1, T, head="もう一つの義務", big="両側5海里の内", lines=("J11L の近くで", "編隊の訓練を避ける"), cell=(1, 0)),
], src=S_J)
FU["c417"] = _f(2, "1つ目の答え", "まとめ", [
    _c(0, T, head="幹部", lines="地図の上で示す", sub="J11L は載っていない", icon="map", cell=(0, 0)),
    _c(1, T, head="教官", lines="J11L の位置の思い違い", cell=(1, 0)),
    _c(1, K, head="編隊", lines="自衛隊の決まりの幅の中へ", cell=(0, 1), span=(2, 1)),
], src=S_J + "・" + kk("106904889X00319720817"))
# ── 第4章
FU["c502"] = _f(2, "その日の午後", "訓練の予定", [
    _c(0, T, head="午後", lines="1回目の訓練", cell=(0, 0)),
    _c(1, K, head="飛ぶ予定の時間", big="1時間35分", cell=(1, 0)),
], src=S_J + "・" + kk("106614889X00419711007"))
FU["c504"] = _f(2, "2機の速さ", "長官の報告", [
    _c(0, K, head="教官機と訓練機", big="マッハ0.72", cell=(0, 0)),
    _c(1, None, head="この高さの標準の気温で", big="時速 約800キロ", sub="計算した値", cell=(1, 0)),
], [_x(1, "a", "b")], src=kk("106614889X00119710802"))
FU["c505"] = _f(3, "旅客機の飛び方", "高さと速さ", [
    _c(0, K, head="高さ", big="約8,500メートル", lines="松島へまっすぐ", icon="plane", bcap=70, cell=(0, 0)),
    _c(1, K, head="速さ", big="マッハ約0.79", sub="時速 約870キロ（計算）", bcap=70, cell=(1, 0)),
    _c(2, K, lines="管制の承認を受けた定期便", cell=(0, 1), span=(2, 1)),
], src=kk("106614889X00419711007") + "・" + S_J)
FU["c507"] = _f(2, "接触のときの姿勢", "ぶつかった機", [
    _c(0, K, head="議員のまとめ（F-86F）", lines="深いバンク角の左旋回", q=True, sub="接触のとき", cell=(0, 0)),
], src=kk("106614889X00419711007"))
FU["c508"] = _f(2, "教官機の向き", "長官の報告", [
    _c(0, K, head="場所", lines="雫石町の付近", cell=(0, 0)),
    _c(1, K, head="教官機", lines=("太平洋側へ出るため", "左旋回中"), q=True, cell=(1, 0)),
], [_x(1, "a", "b", head=False)], src=kk("106614889X00119710802"))
FU["c513"] = _f(2, "限られた可能性", "最高裁の判断", [
    _c(0, T, head="気づいて指示し、避ける", lines="実は極めて限られたもの", q=True, cell=(0, 0)),
], src=S_J, mute=(1,))
FU["c515"] = _f(3, "気づいた時", "元委員長の説明", [
    _c(1, K, head="教官が気づく", lines="衝突のおそれ", cell=(0, 0)),
    _c(2, K, big="接触の約2〜3秒前", lines="回避の命令", sub="推定", cell=(1, 0)),
], [_x(2, "a", "b")], src=kk("106904889X00319720817"))
FU["c516"] = _f(2, "気づく前", "委員会の答弁", [
    _c(0, K, head="教官の話", lines="それより前は見ていない", cell=(0, 0)),
    _c(1, K, head="元委員長", lines="反証は見出せず", cell=(1, 0)),
], src=kk("106904889X00319720817"))
FU["c519"] = _f(2, "接触の時刻", "3つの言い方", [
    _c(0, K, head="長官（事故の3日後）", big="14時3分ごろ", bcap=72, cell=(0, 0)),
    _c(1, K, head="報告書の推定", big="14:02:39", bcap=72, cell=(1, 0)),
    _c(1, K, head="防衛庁の主張", big="14:02:32", bcap=72, cell=(2, 0)),
], src=kk("106614889X00119710802", "107114103X00719730509"))
FU["c521"] = _f(2, "推定原因", "教官について", [
    _c(0, H, head="教官の指示", lines="回避に間に合わず", cell=(0, 0)),
    _c(1, H, head="理由", lines="見つけるのが遅れた", cell=(1, 0)),
], [_x(1, "b", "a")], src=S_W)
FU["c522"] = _f(3, "推定原因", "訓練生について", [
    _c(1, H, head="訓練生", big="接触の約2秒前", lines="右のやや下に旅客機", cell=(0, 0)),
    _c(2, H, lines="すぐ回避操作", sub="間に合わず", cell=(1, 0)),
], [_x(2, "a", "b")], src=S_W)
FU["c523"] = _f(2, "遅れた理由", "報告書の考え", [
    _c(0, H, head="訓練生", lines=("機動隊形の旋回", "経験が浅い"), cell=(0, 0)),
    _c(1, H, lines=("教官機との関係位置を", "維持することに専心"), q=True, cell=(1, 0)),
], src=S_W)
# ── 第5章
FU["c602"] = _f(2, "旅客機の記録", "よける操作の跡", [
    _c(0, H, head="接触の前", lines="機体の反応なし", cell=(0, 0)),
    _c(1, H, lines="回避の操作は直前まで無し", cell=(1, 0)),
], [_x(1, "a", "b")], src=S_W)
FU["c603"] = _f(2, "そのわけ", "報告書の考え", [
    _c(0, H, head="全日空機の操縦者", lines=("訓練機と接触すると", "予測しなかったため"), q=True, cell=(0, 0)),
], src=S_W, mute=(1,))
# 🔧 2026-11-09（⑤c'）：画面の字の呼び名を「元委員長」に揃えた（c605・c610・c515 の札と同じ。1972年8月の答弁は報告書のあと＝元）。語りは変えない
FU["c607"] = _f(2, "見え方の図", "元委員長の説明", [
    _c(0, K, head="図の前提", lines="まっすぐ前を見た場合", sub="基準点", icon="eye", cell=(0, 0)),
    _c(1, K, head="頭の振り方", lines="分からない", cell=(1, 0)),
], src=kk("106914889X00219720823"))
FU["c608"] = _f(2, "図の言葉", "元委員長の説明", [
    _c(0, K, head="報告書の図で", lines="注視野", sub="航空医学の用語", cap=80, cell=(0, 0)),
], src=kk("106914889X00219720823"))
FU["c614"] = _f(3, "証拠の届かない所", "調べた側と裁いた側", [   # 🔧 ⑤c'：「委員長と最高裁」→ 札の「元委員長」と二度にならない字（門番 dup）
    _c(0, K, head="30秒前から数秒前", lines="訓練機を見たか", sub="事実が分からない", cell=(0, 0)),
    _c(1, K, head="元委員長", lines="最終的な結論", q=True, sub="出なかった", cell=(1, 0)),
    _c(2, T, head="最高裁（避けられた可能性）", lines="実は極めて限られたもの", q=True, cell=(0, 1), span=(2, 1)),
], src=kk("106904889X00319720817") + "・" + S_J, mute=(1,))
FU["c616"] = _f(2, "7秒の手がかり", "元委員長の説明", [
    _c(0, K, head="録音", big="接触の約7秒前", lines="「雑音」", cell=(0, 0)),
    _c(1, K, head="雑音の解釈から", lines="確かに見つけていた", cell=(1, 0)),
], [_x(1, "a", "b")], src=kk("106914889X00219720823"))
FU["c617"] = _f(3, "報告書の想定", "雑音の時点の機長", [
    _c(0, K, head="機長", lines=("間近の訓練機を見た", "または急な接近"), cell=(0, 0)),
    _c(1, K, head="報告書", lines="操縦輪を強く保持", sub="と考えられる", cell=(1, 0)),
    _c(2, K, head="元委員長", lines="断定ではない", cell=(0, 1), span=(2, 1)),
], [_x(1, "a", "b")], src=kk("106914889X00219720823"))
FU["c618"] = _f(3, "書き分け", "証拠のある所まで", [
    _c(0, K, head="7秒より前", lines="証拠が無い", cell=(0, 0)),
    _c(1, K, head="報告書", lines=("「7秒前」", "「それ以前から」"), cell=(1, 0)),
    _c(2, K, head="7秒の間の動き", lines="決定的な証拠は無い", cell=(0, 1), span=(2, 1)),
], src=kk("106914889X00219720823"))
FU["c619"] = _f(2, "見張りの扱い", "元委員長の答弁", [
    _c(0, K, head="報告書の見張りの記述", lines="ほとんど書いてございません", q=True, cell=(0, 0)),
    _c(1, K, head="推定原因の中身から", lines=("見張りを直接の問題と", "考えられなかった"), cell=(1, 0)),
], src=kk("106904889X00319720817"), mute=(0,))
FU["c621"] = _f(2, "防衛庁の質問書", "参事官の説明", [
    _c(0, K, head="問うたこと", lines="見張りの義務の考え方", cell=(0, 0)),
    _c(1, K, lines="発見と衝突の時刻", sub="の推定", cell=(1, 0)),
], src=kk("107105266X00619730308"))
FU["c623"] = _f(2, "防衛庁の疑問", "見張りの論じ方", [
    _c(0, K, head="防衛庁の参事官", lines="注視野という新しい概念", q=True, cell=(0, 0)),
    _c(1, K, lines="納得できなかった", q=True, cell=(1, 0)),
], [_x(1, "a", "b", head=False)], src=kk("107105266X00619730308"), mute=(0, 1))
FU["c624"] = _f(2, "7秒前という推論", "防衛庁の見方", [
    _c(0, K, head="報告書", big="14:02:39", lines="その7秒前に見た", bcap=72, cell=(0, 0)),
    _c(0, K, head="防衛庁の参事官", lines="一つの推定", q=True, sub="本当にそうか疑問", cell=(1, 0)),
], src=kk("107105266X00619730308"), mute=(0,))
FU["c626"] = _f(3, "見張れた時間", "航空局の答弁", [
    _c(0, K, head="防衛庁の言う時刻", big="14:02:32", bcap=72, cell=(0, 0)),
    _c(0, K, head="報告書の時刻", big="14:02:39", bcap=72, cell=(1, 0)),
    _c(1, K, head="航空局の技術部長", lines="見張れる時間の余裕", sub="32秒なら、より少ない", cell=(0, 1), span=(2, 1)),
], src=kk("107114103X00719730509"))
FU["c627"] = _f(2, "最高裁の書き方", "旅客機の操縦者", [
    _c(0, T, head="見張りの違反の", lines="有無にかかわらず", q=True, sub="判断を示さない", cap=60, cell=(0, 0)),
], src=S_J, mute=(1,))
FU["c628"] = _f(2, "民事の裁判", "東京高裁", [
    _c(0, K, head="過失の割合", big="国 2：全日空 1", cell=(0, 0)),
    _c(1, None, lines="理由の文は読めていない", sub="この動画", cell=(1, 0)),
], src=kk("112214103X00219911217"))
# ── 第6章
FU["c704"] = _f(2, "政府の動き", "事故の日に", [
    _c(0, K, head="総理府", big="7月30日", lines="全日空機事故対策本部", cell=(0, 0)),
    _c(1, K, head="本部長", lines="運輸大臣", sub="現地で指揮", cell=(1, 0)),
], [_x(1, "a", "b", head=False)], src=kk("106613830X00219710802"))
FU["c705"] = _f(2, "運輸大臣の言葉", "国会で", [
    _c(0, K, head="運輸大臣", big="8月2日", sub="162人の命について", cell=(0, 0)),
    _c(1, K, lines=("つつしんで心より深く", "おわびを申し上げる"), q=True, cell=(1, 0)),
], src=kk("106613830X00219710802"), mute=(1,))
FU["c708"] = _f(2, "遺族への連絡", "長官の報告", [
    _c(0, K, head="防衛庁", lines="遺族各戸を弔問", cell=(0, 0)),
    _c(1, K, head="ほとんどの家に", big="各1名", lines="連絡員が常駐", cell=(1, 0)),
], src=kk("106614889X00119710802"))
FU["c712"] = _f(2, "同じ月の事故", "運輸白書の記録", [
    _c(0, H, head="1971年7月", big="3日", lines="ばんだい号", sub="北海道 七飯町の山", cell=(0, 0)),
    _c(0, H, big="30日", lines="この事故", cell=(1, 0)),
], src=S_W)
FU["c714"] = _f(2, "事故の翌日に", "総理府に", [
    _c(0, K, head="全日空機接触事故", big="7月31日", lines="調査委員会", cell=(0, 0)),
    _c(1, K, lines="第1回の委員会", sub="同じ日に", cell=(1, 0)),
], src=kk("106814103X01219720524"))
FU["c715"] = _f(2, "調査の重ね方", "副長官の報告", [
    _c(0, K, head="委員会", big="10回", cell=(0, 0)),
    _c(0, K, head="懇談会", big="9回", cell=(1, 0)),
    _c(0, K, head="現地の調査", big="3回", cell=(2, 0)),
], src=kk("106814103X01219720524"), note="1972年5月までの数")
FU["c716"] = _f(2, "総理府に置いたわけ", "副長官の説明", [
    _c(0, K, head="自衛隊法", lines="運輸大臣の調査権限", sub="外していた", cell=(0, 0)),
    _c(1, K, head="総理が直接委嘱", lines="関係者は委員にしない", sub="全日空・自衛隊", cell=(1, 0)),
], [_x(1, "a", "b")], src=kk("106604889X00519710816"))
FU["c717"] = _f(1, "委員と報告", "まとめた時期", [
    _c(0, K, head="委員", big="5人", cell=(0, 0)),
    _c(0, H, head="報告書の発表", big="1972年7月27日", bcap=72, cell=(1, 0)),
], src=kk("106613830X00219710802") + "・" + S_W)
# ── 第7章（目撃談＝噂の札は灰色の地・こちらの言葉で言い切らない・落ちてくる人を描かない）
FU["c802"] = _f(2, "1つの目撃談", "国会で紹介された話", [
    _c(0, None, head="新聞に載った目撃談", lines=("黒いものが飛び出す", "白いものが開く", "数秒後に爆発"), sub="地元の子の話", gray=True, cell=(0, 0)),
], src=kk("106614889X00119710802"))
FU["c803"] = _f(2, "防衛局長の答え", "音の速さ", [
    _c(1, K, head="防衛局長", big="1秒に340メートル", lines="音の進む速さ", sub="計算すれば分かる", bcap=72, cell=(0, 0)),
], src=kk("106614889X00119710802"))
FU["c804"] = _f(2, "光と音", "届く時間の差", [
    _c(0, None, head="遠くの出来事", lines="光が先に届く", cell=(0, 0)),
    _c(0, None, lines="音はあとから", cell=(1, 0)),
    _c(1, None, lines="見聞きした順 ≠ 起きた順", cell=(0, 1), span=(2, 1)),
], [_x(0, "a", "b")], note="答弁の理屈の説明", src=kk("106614889X00119710802"))
FU["c805"] = _f(2, "防衛局長の答え", "事故の直後に", [
    _c(0, K, head="防衛局長", lines=("いま即断することは", "適当ではなかろう"), q=True, cell=(0, 0)),
    _c(1, K, head="事故の翌日の段階", lines="新聞に出た本人の証言", sub="それ以外の情報は無い", cell=(1, 0)),
], src=kk("106614889X00119710802"), mute=(0,))
FU["c808"] = _f(2, "警察の見方", "刑事局長の答弁", [
    _c(0, K, head="警察庁の刑事局長", lines=("一応、衝突後の", "脱出であろう"), q=True, cell=(0, 0)),
    _c(1, K, head="脱出のしかた", lines="もう少し調べを詰める", cell=(1, 0)),
], src=kk("106613843X00119710805"), mute=(0,))
FU["c810"] = _f(2, "報告書の推定", "訓練生の回避", [
    _c(0, H, head="訓練生", big="接触の約2秒前", lines="旅客機を見る", cell=(0, 0)),
    _c(1, H, lines="すぐ回避操作", cell=(1, 0)),
], [_x(1, "a", "b")], src=S_W)
FU["c812"] = _f(2, "どちらをとるか", "目撃談について", [
    _c(0, None, head="新聞に載った目撃談", lines="見た人の話", gray=True, cell=(0, 0)),
    _c(1, None, head="この動画がとる側", lines=("報告書の推定", "警察の答弁"), cell=(1, 0)),
], src=kk("106614889X00119710802", "106613843X00119710805") + "・" + S_W)
# ── 第8章（判決の言葉＝原文どおりの札は「」・判決の記号の字は出さない・「被告人」は教官のこと）
FU["c901"] = _f(3, "逮捕と送致", "刑事局長の答弁", [
    _c(1, K, head="業務上過失致死の疑い", big="7月31日", lines="逮捕", cell=(0, 0)),
    _c(2, K, big="8月2日", lines="盛岡地方検察庁へ送致", cell=(1, 0)),
], [_x(2, "a", "b")], src=kk("106604720X00219710810"))
FU["c902"] = _f(2, "翌日になったわけ", "刑事局長の説明", [
    _c(1, K, head="その時点では", lines=("衝突した地点が", "航空路の中か外か"), sub="分からなかった", cell=(0, 0)),
], src=kk("106603843X00119710804"))
FU["c903"] = _f(2, "警察の調べ", "派遣隊にも", [
    _c(0, K, head="松島派遣隊の幹部", big="十数名", lines="事情の聴取", bcap=72, cell=(0, 0)),
    _c(1, K, lines="目撃者の調べ", sub="あわせて", cell=(1, 0)),
], src=kk("106604720X00219710810"))
FU["c904"] = _f(2, "報告書と裁判", "最高裁の説明", [
    _c(0, T, head="事故の報告書", lines="再発防止のための調べ", sub="刑事責任の追及は目的外", cell=(0, 0)),
    _c(1, T, head="裁判では", lines="同意のうえで証拠に", cell=(1, 0)),
], [_x(1, "a", "b")], src=S_J)
FU["c906"] = _f(1, "一審のあと", "国会議員の発言", [
    _c(0, K, head="教官", lines="同日中に控訴", cap=60, cell=(0, 0)),
], src=kk("107503830X00919750318"))
FU["c908"] = _f(3, "扱わないこと", "読んだ範囲", [
    _c(1, None, head="訓練生の一審・二審", lines="原文を読めていない", cell=(0, 0)),
    _c(2, None, lines="結果はここで言わない", cell=(1, 0)),
], [_x(2, "a", "b")], src=S_J)   # 最高裁で争われたのは教官の分だけ（主文「被告人に関する部分」）＝訓練生の判決の原文は手元に無い
FU["c911"] = _f(3, "教官の責任", "最高裁の判断", [
    _c(1, T, head="見張り義務違反の過失責任", lines="やむをえない", q=True, cap=72, cell=(0, 0)),
], src=S_J, mute=(2,))
FU["c912"] = _f(2, "量刑の見方", "最高裁のはじめの書き方", [
    _c(0, T, head="二審の立場", lines="見張りの怠りを重視", cell=(0, 0)),
    _c(1, T, head="結果の重さ", big="162人", sub="乗員・乗客の全員", cell=(0, 1)),
    _c(0, T, head="禁錮4年について", lines="首肯しえないわけではない", q=True, cell=(1, 0), span=(1, 2)),
], src=S_J)
FU["c913"] = _f(2, "しかし", "最高裁の続き", [
    _c(0, T, head="直接の原因", lines="見張りの怠り", sub="責任は免れない", cell=(0, 0)),
    _c(1, T, lines=("余りに重視することは", "相当とはいい難い"), q=True, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_J)
FU["c914"] = _f(2, "見張りの難しさ", "機動隊形の教官", [
    _c(0, T, head="十分に見張ること", lines="すこぶる難度の高い作業", q=True, cell=(0, 0)),
    _c(1, T, head="避けられた可能性", lines="実は極めて限られたもの", q=True, cell=(1, 0)),
], src=S_J, mute=(0,))
FU["c915"] = _f(3, "もう一つの義務", "最高裁の判断", [
    _c(1, T, head="教官", lines=("違背したことは", "明らか"), q=True, cell=(0, 0)),
    _c(2, T, head="その背景", lines="幹部の訓練計画", cell=(1, 0)),
], [_x(2, "b", "a")], src=S_J, mute=(1,))
FU["c916"] = _f(2, "計画に従った訓練", "最高裁の書き方", [
    _c(0, T, head="訓練", lines="計画どおりに実施", cell=(0, 0)),
    _c(1, T, head="判決の「被告人」＝教官", lines=("被告人のみに", "その責任を負わせることも", "相当とはいえない"), q=True, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_J)
FU["c918"] = _f(2, "計画と実行", "最高裁の言葉", [
    _c(0, T, lines="杜撰な計画", q=True, sub="ずさん", cap=54, cell=(0, 0)),
    _c(0, T, lines="幹部らの怠慢", q=True, cap=54, cell=(1, 0)),
    _c(1, T, lines="抜きには考えられない", cap=46, cell=(2, 0)),
], src=S_J, mute=(0,), gx=60)   # 🔧 横一列（2段にすると上の札が地 L1 の壁の模様＝OCR の行 y 344〜392 に載る＝門番 slide G-14）
FU["c919"] = _f(2, "事故のあとの対策", "最高裁が挙げる", [
    _c(0, T, head="訓練空域", lines="民間機の経路から隔離", cell=(0, 0)),
    _c(1, T, head="編隊の訓練", lines="見張り用の教官機を別に", cell=(1, 0)),
], src=S_J)
FU["c922"] = _f(1, "違う結論", "刑について", [
    _c(0, T, head="反対意見の裁判官", big="2人", cell=(0, 0)),
    _c(0, T, head="教官は", big="禁錮2年", lines="実刑に", cell=(1, 0)),
], src=S_J)
FU["c923"] = _f(2, "反対意見の一人", "空の衝突", [
    _c(0, T, head="空中衝突", lines=("瞬時にして", "多数の人命を奪う"), q=True, cell=(0, 0)),
    _c(1, T, head="操縦者の責任", lines="極めて重大", q=True, cap=64, cell=(1, 0)),
], src=S_J, mute=(1,))
FU["c924"] = _f(2, "反対意見のもう一人", "教官にとって", [
    _c(0, T, head="J11L の位置の確認", lines="極めて容易", q=True, sub="近くの訓練の回避も", cap=64, cell=(0, 0)),
], src=S_J, mute=(0,))
FU["c925"] = _f(2, "反対意見の2人", "認めたことと加えたこと", [
    _c(0, T, head="派遣隊の幹部ら", lines="安全配慮の欠如", sub="認める", cell=(0, 0)),
    _c(1, T, head="教官自身の過失も", lines="軽視できない", cell=(1, 0)),
], src=S_J)
FU["c926"] = _f(2, "分かれた点", "多数意見と反対意見", [
    _c(0, T, head="禁錮4年", lines="重すぎる", sub="どちらも同じ", cell=(0, 0)),
    _c(1, T, head="違いは", lines=("実刑か", "執行猶予か"), cell=(1, 0)),
], src=S_J)
FU["c927"] = _f(2, "つながりの見方", "反対意見の一人", [
    _c(0, T, head="見張りの違反と衝突のつながり", lines="かなり微妙な点がある", q=True, cell=(0, 0)),
], src=S_J, mute=(1,))
FU["c928"] = _f(3, "実刑を求めたわけ", "反対意見の一人", [
    _c(0, T, head="執行猶予では", lines="操縦者・教官として", cell=(0, 0)),
    _c(1, T, lines=("責任の重大性を明確にする", "うえにおいて十分でない"), q=True, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_J)
FU["c929"] = _f(3, "幹部の裁判", "読んだ資料の範囲", [
    _c(1, None, head="幹部の刑事の裁判", lines="資料に出てこない", cell=(0, 0)),
], src=S_J + "・国会会議録（読んだ会議の範囲）")
FU["c930"] = _f(3, "3つ目の答え", "刑事の責任", [
    _c(0, None, head="3つ目の問い", lines="なぜ教官に", cell=(0, 0)),
    _c(1, T, head="刑事の裁判", lines="操縦の2人が被告", cell=(1, 0)),
    _c(2, T, head="最高裁で争われたのは", lines="教官の分だけ", cell=(2, 0)),
], [_x(2, "b", "c")], src=S_J)
FU["c931"] = _f(3, "3つ目の答え", "続き", [
    _c(0, T, head="最高裁", lines="2つの義務の違反を認めた", cell=(0, 0)),
    _c(1, T, head="ひとりに禁錮4年の実刑は", lines="酷に過ぎる", q=True, cell=(1, 0)),
    _c(2, T, lines="幹部の責任こそ重大", q=True, cell=(0, 1), span=(2, 1)),
], src=S_J, mute=(1, 2))
# 🔧 2026-11-09（⑤c'）：札0＝「刑事の裁判／1985年（大きな数）／結審」は「1985年に裁判が終わった」と読めた（終わったのは1983年の最高裁＝c909・c910）。
#    1985年は官房長が答えた年＝頭の小さな字へ移し、大きな数の欄を外した（数は出典の日付の年のまま＝門番 m31 の③④）
FU["c933"] = _f(2, "防衛庁の受けとめ", "官房長の答弁", [
    _c(0, K, head="1985年の時点", lines=("刑事の裁判は", "結審ずみ"), cell=(0, 0)),
    _c(1, K, lines="厳粛に受けとめて", q=True, sub="判決の結果について", cell=(1, 0)),
], src=kk("110304889X00619851210"), mute=(1,))
# ── 第9章
FU["ca01"] = _f(3, "遺族への補償", "防衛庁の答弁", [
    _c(1, K, head="窓口", lines="防衛庁", cap=60, cell=(0, 0)),
    _c(1, K, head="支払った時期", big="1971年末〜72年冬", bcap=64, cell=(1, 0)),
    _c(2, K, head="乗客155人のうち", big="152人分", cell=(0, 1), span=(2, 1)),
], src=kk("107503830X00819750314"))
FU["ca02"] = _f(1, "補償の額", "防衛庁の答弁", [
    _c(0, K, head="ひとまず防衛庁が支払い", big="16億5,200万円", bcap=80, cell=(0, 0)),
], src=kk("107503830X00819750314"))
FU["ca04"] = _f(1, "もう一つの裁判", "民事", [
    _c(0, K, head="機体と営業の損害", lines="全日空の側 と 国", cap=60, cell=(0, 0)),
], src=kk("107503830X00819750314", "112214103X00219911217"))
FU["ca07"] = _f(3, "判決の理由", "読んだ範囲", [
    _c(1, None, head="民事の判決", lines="理由の文は読めていない", cell=(0, 0)),
    _c(2, None, head="全日空の側の過失の中身", lines="ここでは言えない", cell=(1, 0)),
], [_x(2, "a", "b")], src=kk("112214103X00219911217"))
FU["ca11"] = _f(2, "賠償の分け方", "防衛庁の答弁", [
    _c(0, K, head="乗客と乗員の遺族へ", big="約20億円", cell=(0, 0)),
    _c(1, K, head="そのうち国の側", big="約14億円", cell=(1, 0)),
], src=kk("112214103X00219911217"))
# ── 第10章
FU["cb01"] = _f(3, "空の決まり", "事故のあとに", [
    _c(1, K, head="政府の連絡協議会", big="8月", lines=("航空交通安全", "緊急対策要綱"), bcap=72, cell=(0, 0)),
    _c(2, K, head="中身の一つ（運輸大臣の報告）", lines=("訓練空域を", "空港と航空路から分ける"), cell=(1, 0)),
], [_x(2, "a", "b")], src=kk("106613843X00119710805"))
FU["cb03"] = _f(2, "これまでの訓練空域", "防衛政務次官の説明", [
    _c(0, K, head="できるだけ", lines="航空路・管制圏を避ける", cell=(0, 0)),
    _c(1, K, lines="交通量の少ない空域", cell=(1, 0)),
], [_x(1, "a", "b")], src=kk("106613830X00319710816"))
FU["cb04"] = _f(2, "新しい訓練空域", "防衛政務次官の説明", [
    _c(0, K, head="低い高さの訓練空域", big="8か所", sub="8月11日", cell=(0, 0)),
    _c(1, K, head="高い空の訓練空域", lines="運輸省と協議中", cell=(1, 0)),
], src=kk("106613830X00319710816"))
FU["cb05"] = _f(2, "これからの決め方", "防衛政務次官の説明", [
    _c(0, K, lines="運輸省と十分協議", cell=(0, 0)),
    _c(1, K, lines="公示して決定", cell=(1, 0)),
], [_x(1, "a", "b")], src=kk("106613830X00319710816"))
FU["cb06"] = _f(1, "縮まる見込み", "防衛政務次官の説明", [
    _c(0, K, head="前の訓練空域と比べて", big="ほぼ50%", sub="くらいになる見込み", cell=(0, 0)),
], src=kk("106613830X00319710816"))
FU["cb07"] = _f(2, "報告書の発表", "総理府の委員会", [
    _c(0, H, head="調査委員会", big="1972年7月27日", lines="報告書を発表", bcap=72, cell=(0, 0)),
], src=S_W)
FU["cb08"] = _f(3, "報告書の勧告", "元委員長の読み上げ", [
    _c(1, K, head="勧告の一つ", lines=("他の航空機等と衝突しないように", "見張りをしなければならないよう", "法的に明確化する"), q=True, cap=46, cell=(0, 0)),
], src=kk("106904889X00319720817"))
FU["cb09"] = _f(2, "防衛庁の受けとめ", "長官の答弁", [
    _c(0, K, head="防衛庁長官", lines="謙虚に受けとめ", q=True, sub="報告書全体を", cell=(0, 0)),
    _c(1, K, head="勧告の事項", lines="すみやかに沿う措置", cell=(1, 0)),
], src=kk("106904889X00319720817"), mute=(0,))
FU["cb13"] = _f(3, "新しい報告の決まり", "航空法の改正", [
    _c(0, L, head="航空法", big="第76条の2", bcap=72, cell=(0, 0)),
    _c(1, L, head="飛行中に", lines="衝突・接触のおそれ", cell=(1, 0)),
    _c(2, L, head="機長", lines="運輸大臣に報告", cell=(2, 0)),
], [_x(2, "b", "c")], src=S_LAW, gx=110)
FU["cb15"] = _f(3, "空の分け方の続き", "国土交通省の記者発表", [
    _c(1, KU, head="「雫石事故」を契機に", lines="民間の訓練試験空域", cell=(0, 0)),
    _c(2, KU, lines=("民間航空の安全と発展に", "大きく寄与"), q=True, cell=(1, 0)),
], [_x(2, "a", "b")], src=S_MLIT)
FU["cb16"] = _f(3, "別の空中衝突", "国土交通省の記者発表", [
    _c(0, KU, head="管理していたのは", lines="近くの空港事務所", cell=(0, 0)),
    _c(1, KU, head="訓練空域の中で", big="2001年5月", lines="三重県桑名市の上空", sub="訓練機どうしの衝突", bcap=72, cell=(1, 0)),
], src=S_MLIT)
FU["cb18"] = _f(2, "空域の使い方", "国土交通省の記者発表", [
    _c(0, KU, head="民間の訓練空域", lines=("使用されていない場合", "安全が確認された場合"), cell=(0, 0)),
    _c(1, KU, lines="定期便の通過が可能に", cell=(1, 0)),
], [_x(1, "a", "b", t="に限り")], src=S_MLIT)
# ── 第11章
FU["cc03"] = _f(2, "森の名前", "町の頁から", [
    _c(0, M, head="もとの名", lines="慰霊の森", cell=(0, 0)),
    _c(0, M, big="令和元年", lines="森のしずく公園", sub="改称", bcap=72, cell=(1, 0)),
    _c(1, M, head="式を主催する法人", lines="理事長は町長", sub="2020年の町の記事", cell=(0, 1), span=(2, 1)),
], [_x(0, "a", "b")], src=S_TOWN)
FU["cc05"] = _f(2, "会社の展示", "全日空の頁", [
    _c(0, KS, head="全日空", lines="安全教育センター", cell=(0, 0)),
    _c(1, KS, lines="事故機の一部を展示", sub="2026年11月の時点", cell=(1, 0)),
], [_x(1, "a", "b", head=False)], src=S_ANA)
FU["cc07"] = _f(2, "1つ目の答え", "空域の決まり方", [
    _c(0, T, head="幹部", lines="地図の上で指で示す", sub="J11L は載っていない", icon="map", cell=(0, 0)),
    _c(1, T, head="上役", lines="検討なしに承認", cell=(1, 0)),
], [_x(1, "a", "b")], src=S_J)
FU["cc08"] = _f(2, "1つ目の答え", "続き", [
    _c(0, T, head="教官", lines="J11L の位置の思い違い", cell=(0, 0)),
    _c(1, T, head="編隊", big="西側5海里の内", sub="自衛隊が訓練を制限した幅", bcap=72, cell=(1, 0)),
], [_x(1, "a", "b")], src=S_J)
FU["cc09"] = _f(2, "2つ目の答え", "旅客機からの見え方", [
    _c(0, None, head="2つ目の問い", lines="旅客機から見えていたか", cell=(0, 0)),
    _c(1, K, head="報告書の推定", big="少なくとも約7秒前", lines="から見ていた", bcap=64, cell=(1, 0)),
], src=kk("106914889X00219720823"))
FU["cc10"] = _f(2, "2つ目の答え", "続き", [
    _c(0, K, head="防衛庁", lines="時刻に異論", cell=(0, 0)),
    _c(0, K, head="運輸省", lines="報告書の時刻を是認", cell=(1, 0)),
    _c(1, T, head="最高裁", lines="旅客機の操縦者の見張り", sub="判断を示さず", cell=(0, 1)),
    _c(1, None, lines="機長と副操縦士", sub="確かめるすべはない", cell=(1, 1)),
], src=kk("107105266X00619730308", "107114103X00719730509") + "・" + S_J)
FU["cc11"] = _f(2, "3つ目の答え", "刑事の責任", [
    _c(0, None, head="3つ目の問い", lines="なぜ教官に", cell=(0, 0)),
    _c(1, T, head="刑事の裁判", lines="操縦の2人が被告", cell=(1, 0)),
    _c(1, T, head="最高裁", lines="教官の分だけ", cell=(2, 0)),
], [_x(1, "b", "c")], src=S_J)
FU["cc12"] = _f(2, "3つ目の答え", "続き", [
    _c(0, T, head="ひとりに4年の実刑は", lines="酷に過ぎる", q=True, cell=(0, 0)),
    _c(0, T, head="航空自衛隊、特に", lines="幹部の責任こそ重大", q=True, cell=(1, 0)),
    _c(1, T, head="反対意見の2人", big="禁錮2年", lines="の実刑を", bcap=72, cell=(0, 1), span=(2, 1)),
], src=S_J, mute=(0, 1))
FU["cc14"] = _f(2, "事故のあと", "変わったこと", [
    _c(0, None, lines="空を分けた", cell=(0, 0)),
    _c(0, L, lines="見張りの義務を法律に", cell=(1, 0)),
    _c(1, KU, head="民間の訓練空域", big="2002年10月", lines="センター中心の管理", bcap=72, cell=(0, 1), span=(2, 1)),
], src=S_LAW + "・" + S_MLIT)


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


# ── 🆕 ⑤b-5（2026-11-08）：見え方の表の部品（30本目 mech30 の ⑤b-5・⑤b-6 の形を写した＝札の大きさは mech31 の _zbox で測る）
def _lead(c, x, y):
    """札の上か下の辺から、線の上の点へ（細い線と点）。"""
    bx, by, bw, bh = _zbox(c)
    x0 = min(max(x, bx + 24), bx + bw - 24)
    y0 = by + bh + 8 if y > by + bh else by - 8
    return F.line(x0, y0, x, y, J.TICK, 4) + F.circ(x, y, 12, INK)


def _rowmid(c):
    """札の中の行の真ん中の高さ（_draw_card と同じ割り付け）＝[(種類, 字, y)]。"""
    _x0, y, _w2, h = _zbox(c)
    rows = _rows(c)
    yy = y + (h - sum(cap * LH[kd] for kd, _t2, cap in rows)) / 2
    out = []
    for kd, t, cap in rows:
        out.append((kd, t, yy + cap * LH[kd] / 2))
        yy += cap * LH[kd]
    return out


def _ring(c, col=None, pad=14.0):
    """札を囲む明るい枠（その段で話している札）。"""
    x, y, w, h = _zbox(c)
    return F.rect(x - pad, y - pad, w + 2 * pad, h + 2 * pad, "none", col or J.AMBER, 7, rx=22)


def _plane(cx, cy, col, k=1.0, ang=0.0, fill=None):
    """飛行機を上から見た形（_i_plane と同じ点・拡大率 k・向き ang 度＝時計回り・人を乗せない）。"""
    pts = [(0, -62), (8, -52), (9, -12), (66, 14), (66, 26), (9, 14), (7, 40), (26, 52), (26, 60), (0, 56), (-26, 60), (-26, 52), (-7, 40), (-9, 14),
           (-66, 26), (-66, 14), (-9, -12), (-8, -52)]
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return F.poly([(cx + k * (x * ca - y * sa), cy + k * (x * sa + y * ca)) for x, y in pts], fill or J.BG2, col, 5, close=True)


def _blip(x, y, col, r=16.0, dim=False):
    """機影の印（向きを描かない＝丸と外の輪）。"""
    if dim:
        return F.circ(x, y, r * 0.6, "none", J.TICK, 4)
    return F.circ(x, y, r * 1.9, "none", col, 4, op=0.55) + F.circ(x, y, r, col)


def _s(h, m, s=0):
    """時刻を秒に（門番 ⑤ hms は「14:02:39」「14:03」の字を自分で秒に読む）。"""
    return h * 3600.0 + m * 60.0 + s


# ── c509・c510・c511 方位の図（教官機を真ん中・機首が上・右へ時計回りの角度＝札「正面から測ったと見た場合」＝数え方は判決に無い）。
#    距離は札の数の比例（1キロ＝PK px）・上下の角は描かない（札の字だけ）・機影の向きは描かない。門番 ⑤ pol が角度と距離を点の座標から測る
CP, PK, PR = (720.0, 590.0), 150.0, 180.0
PLANE = J.AMBER              # 機影の印の色（札の黄の数と結ぶ）
N_POL = "模式・角度は機首から右回り（数え方の見立て）・距離は比例・上下の角は描かない"


def _pol(deg, km):
    a = math.radians(deg)
    return CP[0] + km * PK * math.sin(a), CP[1] - km * PK * math.cos(a)


def _rose():
    """方位の輪（0度・90度・180度の字）と真ん中の教官機。"""
    cx, cy = CP
    g = F.circ(cx, cy, PR, "none", J.TICK, 4, op=0.8)
    for a in (0, 90, 180, 270):
        x1, y1 = cx + PR * math.sin(math.radians(a)), cy - PR * math.cos(math.radians(a))
        x2, y2 = cx + (PR + 26) * math.sin(math.radians(a)), cy - (PR + 26) * math.cos(math.radians(a))
        g += F.line(x1, y1, x2, y2, J.TICK, 5)
    g += F.line(cx, cy - 70, cx, cy - PR, J.TICK, 3, dash="12 10")
    g += _t(cx, cy - PR - 44, "0度", 40, J.TICK, "middle", 160) + _t(cx + PR + 40, cy + 14, "90度", 40, J.TICK, "start", 160)
    g += _t(cx, cy + PR + 56, "180度", 40, J.TICK, "middle", 200)
    return g + _plane(cx, cy, INK, k=0.95) + _t(cx - 96, cy + 14, "教官機", 40, INK, "end", 220)


def _ray(deg, km, col, lab="", dim=False, side="end", dy=-40.0):
    """真ん中からその点への破線と機影の印・名の字。"""
    x, y = _pol(deg, km)
    a = math.radians(deg)
    x0, y0 = CP[0] + 78 * math.sin(a), CP[1] - 78 * math.cos(a)
    if dim:
        return F.line(x0, y0, x, y, J.TICK, 3, dash="8 12", op=0.6) + _blip(x, y, col, dim=True)
    g = F.line(x0, y0, x, y, col, 5, dash="14 10") + _blip(x, y, col)
    if lab:
        g += _t(x + (-40 if side == "end" else 40), y + dy, lab, 42, col, side, 260)
    return g


def _tie(c, x, y):
    """札の左か右の辺の真ん中から、その点へ（細い線と点）。"""
    bx, by, bw, bh = _zbox(c)
    x0 = bx - 8 if x < bx else bx + bw + 8
    return F.line(x0, by + bh / 2, x, y, J.TICK, 4) + F.circ(x, y, 12, INK)


def _dbl(x1, y1, x2, y2, col, sw=6):
    """両向きの矢印（真ん中から両端へ）。"""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return _arrow(mx, my, x2, y2, col, sw, 22) + _arrow(mx, my, x1, y1, col, sw, 22)


def _arc(cx, cy, r, a0, a1, col, sw=6):
    """円弧の矢印（角度は上から右回り・a0 から a1 へ・先に矢じり）。"""
    n = max(4, int(abs(a1 - a0) / 5))
    pts = [(cx + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), cy - r * math.cos(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return F.poly(pts[:-1], "none", col, sw) + _arrow(pts[-3][0], pts[-3][1], pts[-1][0], pts[-1][1], col, sw, 22)


C509 = [
    _at(_c(0, None, lines=("角度は教官機の", "正面から測ったと", "見た場合"), cap=44), 300, 360),
    _at(_c(1, T, head="最高裁が引く二審の認定", big="約30秒前", bcap=72), 1480, 760),
    _at(_c(2, T, head="旅客機", big="右78度", lines="約4.3キロ", sub="上10度", bcap=64, cap=50), 1580, 440),
]
VIEWS["c509"] = _z(3, "方位の図", "角度と距離", C509, [
    _p(0, _rose),
    _p(2, lambda: _ray(78, 4.3, PLANE)),
], src=S_J, note=N_POL, schem=True,
    tl=dict(kind="pol", c=CP, k=PK, pts=(("右78度", "約4.3キロ") + _pol(78, 4.3),)))

# ── c518 接触の時刻の帯（秒の比例＝門番 ⑤ hms）。報告書の推定と防衛庁の主張のあいだ＝7秒の棒。長官の「14:03ごろ」は影（語りに出ない）
YT = dict(x0=300.0, x1=1620.0, y=560.0, v0=_s(14, 2, 20), v1=_s(14, 3, 10))
VT = (_s(14, 2, 39), _s(14, 2, 32), _s(14, 3))
C518 = [
    _at(_c(1, K, head="報告書の推定", big="14:02:39", bcap=72), 990, 350),
    _at(_c(2, K, head="防衛庁の主張", big="14:02:32", bcap=72), 520, 770),
    _at(_c(2, K, head="長官の報告", big="14:03ごろ", bcap=56, dim=True), 1500, 350),
]


def _t518_axis():
    return _axis(YT, [_s(14, 2, 20) + 10 * i for i in range(6)])


def _t518_gap():
    x0, x1 = _lin(YT, VT[1]), _lin(YT, VT[0])
    return (F.rect(x0, YT["y"] - 16, x1 - x0, 32, J.AMBER, None, None, rx=8, op=0.85)
            + _t((x0 + x1) / 2, YT["y"] - 44, "7秒", 52, J.AMBER, "middle", 200))


VIEWS["c518"] = _z(3, "時刻の帯", "秒の目盛りで", C518, [
    _p(0, _t518_axis),
    _p(1, lambda: _lead(C518[0], _lin(YT, VT[0]), YT["y"])),
    _p(2, lambda: _lead(C518[1], _lin(YT, VT[1]), YT["y"]) + _lead(C518[2], _lin(YT, VT[2]), YT["y"]) + _t518_gap()),
], src=kk("107114103X00719730509", "106614889X00119710802"), note="目盛りは10秒ごと",
    tl=dict(kind="hms", ax=((YT["v0"], YT["x0"]), (YT["v1"], YT["x1"])),
            pts=(("14:02:39", _lin(YT, VT[0])), ("14:02:32", _lin(YT, VT[1])), ("14:03", _lin(YT, VT[2])))))

# ── c702 派遣の数の表（日付・人・車両・航空機＝数の棒にしない・人の形は使わない）
TX702 = (300.0, 760.0, 1160.0, 1560.0)          # 列の真ん中（日付・人・車両・航空機）
TY702 = (460.0, 600.0, 740.0)                   # 行の真ん中（見出し・30日・31日）
R702 = (("7月30日", "3,660人", "470両", "80機"), ("7月31日", "5,320人", "480両", "80機"))


def _t702_grid():
    g = "".join(F.line(120.0, y, 1760.0, y, J.TICK, 3) for y in (520.0, 670.0))
    g += "".join(F.line(x, 400.0, x, 810.0, J.TICK, 3) for x in (520.0, 960.0, 1360.0))
    return g + "".join(_t(x, TY702[0] + 14, s, 40, J.TICK, "middle", 300) for x, s in zip(TX702, ("日付", "人", "車両", "航空機")))


def _t702_row(i):
    y = TY702[i + 1]
    d, p, v, a = R702[i]
    return (_t(TX702[0], y + 18, d, 52, INK, "middle", 400) + _t(TX702[1], y + 24, p, 72, J.AMBER, "middle", 400)
            + _t(TX702[2], y + 20, v, 56, J.AMBER, "middle", 360) + _t(TX702[3], y + 20, a, 56, J.AMBER, "middle", 360))


C702 = [_at(_c(0, K, head="防衛庁長官の報告", lines="陸・海・空の各自衛隊", cap=48), 960, 305)]
VIEWS["c702"] = _z(2, "派遣の数", "最初の2日", C702, [_p(1, _t702_grid), _p(1, lambda: _t702_row(0) + _t702_row(1))],
                   src=kk("106614889X00119710802"))

# ══════════════════════════════════════════════════════════
#  ⑤b-5 の残り（章の順）。🔴 言い切らない線＝台本の画の欄と出典の欄の字の範囲だけ（位置と広さは模式＝左下の注で断る）
# ══════════════════════════════════════════════════════════
# ── 第1章 c205 旅客機の時刻の帯（分の比例＝門番 ⑤ hm）・国会議員のまとめ
Y205 = dict(x0=240.0, x1=1680.0, y=560.0, v0=13 * 60.0 + 30, v1=14 * 60.0 + 15)
V205 = (13 * 60.0 + 33, 13 * 60.0 + 46, 13 * 60.0 + 50, 14 * 60.0 + 11)
C205 = [
    _at(_c(0, K, head="千歳を離陸", big="13:33", bcap=64), 360, 770),
    _at(_c(0, K, head="函館の上", big="13:46", lines="約6,700メートル", bcap=64, cap=46), 700, 350),
    _at(_c(1, K, head="管制に報告", big="13:50", lines="約8,500メートル", bcap=64, cap=46), 1010, 720),
    _at(_c(2, K, head="松島の上", big="14:11", lines="の予定", bcap=64, cap=46), 1450, 360),
]
VIEWS["c205"] = _z(3, "旅客機の時刻", "千歳から松島へ", C205, [
    _p(0, lambda: _axis(Y205, [Y205["v0"] + 5 * i for i in range(10)])),
    _p(0, lambda: _lead(C205[0], _lin(Y205, V205[0]), Y205["y"]) + _lead(C205[1], _lin(Y205, V205[1]), Y205["y"])),
    _p(1, lambda: _lead(C205[2], _lin(Y205, V205[2]), Y205["y"])),
    _p(2, lambda: _lead(C205[3], _lin(Y205, V205[3]), Y205["y"])),
], src=kk("106614889X00419711007"), note="目盛りは5分ごと",
    tl=dict(kind="hm", ax=((Y205["v0"], Y205["x0"]), (Y205["v1"], Y205["x1"])),
            pts=tuple((f"{int(v // 60)}:{int(v % 60):02d}", _lin(Y205, v)) for v in V205)))

# ── c210 機動隊形（前の教官機が左右に旋回・うしろの訓練機が決まった位置）＝c503 と同じ並び（訓練機は右のうしろ）
C210 = [
    _at(_c(0, T, head="機動隊形", lines="編隊の訓練", cap=56), 380, 400),
    _at(_c(1, T, lines="所定の位置", q=True, sub="について行く", cap=56), 1480, 760),
]
VIEWS["c210"] = _z(2, "2機の役目", "前と後ろ", C210, [
    _p(0, lambda: _plane(860.0, 420.0, INK) + _t(860.0, 540.0, "教官機", 40, INK, "middle", 200)
       + _plane(1060.0, 650.0, INK) + _t(1060.0, 770.0, "訓練機", 40, INK, "middle", 200)),
    _p(1, lambda: _arc(860.0, 420.0, 150.0, -55.0, -125.0, J.AMBER) + _arc(860.0, 420.0, 150.0, 55.0, 125.0, J.AMBER), arrow=True),
    _p(1, lambda: F.line(900.0, 470.0, 1020.0, 600.0, J.TICK, 4, dash="10 10")),
], src=S_J, note="模式・2機の間の距離と旋回の大きさは描いた形でない", schem=True)


# ── c212 2つの飛び方（旅客機＝計器飛行方式で決まった道・2機＝有視界飛行で訓練の空域）
def _c212_free():
    g = F.rect(1080.0, 470.0, 680.0, 340.0, "none", J.TICK, 5, rx=24, dash="16 12") + _t(1100.0, 456.0, "訓練の空域", 38, J.TICK, "start", 300)
    # 🔧 重ね絵：交差する線は「×」（禁止の印）に見えた＝交差しない丸い道に
    pts = [(1300.0 + 170.0 * math.cos(math.radians(t)) + 24.0 * math.cos(math.radians(3 * t)), 600.0 + 70.0 * math.sin(math.radians(t)))
           for t in range(0, 361, 10)]
    return g + F.poly(pts, "none", J.AMBER, 5, close=True, dash="12 8") + _plane(1560.0, 600.0, INK, k=0.6, ang=30.0)


def _c212_route():
    g = F.circ(240.0, 780.0, 14, J.BG2, INK, 5) + F.circ(760.0, 470.0, 14, J.BG2, INK, 5)
    g += _arrow(252.0, 772.0, 746.0, 478.0, INK, 7, 26)
    return g + _plane(500.0, 625.0, INK, k=0.6, ang=59.0) + _t(560.0, 720.0, "決まった道", 40, INK, "start", 300)


C212 = [
    _at(_c(1, K, head="旅客機", lines="計器飛行方式", cap=52), 430, 330),
    _at(_c(0, K, head="2機", lines="有視界飛行", q=True, cap=56), 1420, 330),
    _at(_c(1, None, lines="目で見て確かめる", cap=48), 1420, 745),
]
VIEWS["c212"] = _z(2, "2つの飛び方", "管制と目", C212, [_p(0, _c212_free), _p(1, _c212_route, arrow=True)],
                   src=kk("106614889X00419711007"), note="模式・道と空域の形は描いた形でない", schem=True)

# ── c216 その日の時刻（分の比例＝門番 ⑤ hm）・離陸は長官の報告と議員のまとめ・接触の「14:02ごろ」は語りのまとめ
Y216 = dict(x0=240.0, x1=1680.0, y=560.0, v0=13 * 60.0 + 20, v1=14 * 60.0 + 10)
V216 = (13 * 60.0 + 28, 13 * 60.0 + 33, 14 * 60.0 + 2)
C216 = [
    _at(_c(0, K, head="2機が松島を離陸", big="13:28", bcap=64), 420, 350),
    _at(_c(0, K, head="旅客機が千歳を離陸", big="13:33", bcap=64), 660, 770),
    _at(_c(1, None, head="雫石町の上空", big="14:02ごろ", lines="接触", bcap=64, cap=50), 1450, 350),
]
VIEWS["c216"] = _z(2, "その日の時刻", "離陸から接触まで", C216, [
    _p(0, lambda: _axis(Y216, [Y216["v0"] + 10 * i for i in range(6)])),
    _p(0, lambda: _lead(C216[0], _lin(Y216, V216[0]), Y216["y"]) + _lead(C216[1], _lin(Y216, V216[1]), Y216["y"])),
    _p(1, lambda: _lead(C216[2], _lin(Y216, V216[2]), Y216["y"])),
], src=kk("106614889X00119710802", "106614889X00419711007"), note="目盛りは10分ごと",
    tl=dict(kind="hm", ax=((Y216["v0"], Y216["x0"]), (Y216["v1"], Y216["x1"])),
            pts=(("13:28", _lin(Y216, V216[0])), ("13:33", _lin(Y216, V216[1])), ("14:02", _lin(Y216, V216[2])))))

# ── 第2章 c302 5つの空域の名（判決の書いた順・位置は描かない＝資料に図が無い）。名は絵の部品（札の枚数に数えない）
NAMES302 = ("横手", "月山", "米沢", "気仙沼", "相馬")


def _c302_names():
    g = ""
    for i, nm in enumerate(NAMES302):
        x = 300.0 + 330.0 * i
        g += _panel(x - 130, 370.0, 260, 130, sc(T), op=0.84, sw=5) + _t(x, 457.0, nm, 64, INK, "middle", 240)
    return g


C302 = [_at(_c(0, T, head="飛行訓練準則の原則", lines="1回の飛行に1つ", cap=56), 960, 690)]
VIEWS["c302"] = _z(1, "空域の名", "準則が定めた5つ", C302, [_p(0, _c302_names)], src=S_J, note="名は判決の書いた順・位置は描かない（資料に図が無い）")

# ── c309 伝わった順（補佐 → 班長 → 隊長＝3人の幹部・主任教官への伝達は影＝次のカット）。役職だけ
C309 = [
    _at(_c(0, T, head="飛行班長補佐", lines="空域を進言", cap=52), 330, 420),
    _at(_c(0, T, head="飛行班長", lines="そのまま承認", cap=52), 960, 420),
    _at(_c(0, T, head="飛行隊長", lines="そのまま承認", cap=52), 1590, 420),
    _at(_c(1, None, head="空域「盛岡」", big="3人", lines="の幹部", bcap=72, cap=52), 1290, 720),
]


def _c309_arrows():
    a, b, c = (_zbox(x) for x in C309[:3])
    g = _arrow(a[0] + a[2] + 12, 420, b[0] - 12, 420, sc(T), 7, 26) + _t((a[0] + a[2] + b[0]) / 2, 392, "進言", 36, sc(T), "middle", 200)
    return g + _arrow(b[0] + b[2] + 12, 420, c[0] - 12, 420, sc(T), 7, 26) + _t((b[0] + b[2] + c[0]) / 2, 392, "報告", 36, sc(T), "middle", 200)


def _c309_branch():
    a = _zbox(C309[0])
    g = _arrow(330.0, a[1] + a[3] + 10, 330.0, 640.0, J.TICK, 4, 20, "12 10") + _t(350.0, 590.0, "伝達", 34, J.TICK, "start", 120)
    g += _panel(170.0, 652.0, 320, 150, J.TICK, op=0.55, sw=3)
    return (g + _t(330.0, 702.0, "主任教官", 34, J.TICK, "middle", 300) + _t(330.0, 750.0, "確かめず", 40, J.TICK, "middle", 300)
            + _t(330.0, 790.0, "注意も与えず", 30, J.TICK, "middle", 300))


def _c309_ring():
    a, c = _zbox(C309[0]), _zbox(C309[2])
    return F.rect(a[0] - 18, a[1] - 18, c[0] + c[2] - a[0] + 36, max(a[3], c[3]) + 36, "none", J.AMBER, 6, rx=24)


VIEWS["c309"] = _z(3, "伝わった順", "松島派遣隊の中で", C309, [
    _p(0, _c309_arrows, arrow=True), _p(0, _c309_branch, arrow=True), _p(1, _c309_ring)], src=S_J)

# ── c312 部屋のスケジュール・ボード（「盛岡」の2字だけ・位置と範囲の欄は空白＝模式）
BD = (360.0, 290.0, 1200.0, 400.0)
BX312 = (560.0, 960.0, 1360.0)


def _c312_board():
    x, y, w, h = BD
    g = F.rect(x, y, w, h, INK, None, None, rx=14, op=0.10) + F.rect(x, y, w, h, "none", INK, 6, rx=14)
    g += F.line(x, y + 90, x + w, y + 90, J.TICK, 3) + "".join(F.line(xx, y + 18, xx, y + h - 18, J.TICK, 3) for xx in (760.0, 1160.0))
    g += "".join(_t(xx, y + 60, s, 40, J.TICK, "middle", 300) for xx, s in zip(BX312, ("空域", "位置", "範囲")))
    return g + _t(x + 8, y - 22, "スケジュール・ボード", 40, INK, "start", 600)


def _c312_blank():
    y = BD[1]
    return "".join(F.rect(xx - 170, y + 120, 340, 240, "none", J.AMBER, 6, rx=12, dash="16 12") for xx in BX312[1:])


C312 = [_at(_c(2, T, head="最高裁の判決", lines="何ら指示、説明されなかった", q=True, cap=48), 960, 780)]
VIEWS["c312"] = _z(3, "部屋の板", "伝え方", C312, [
    _p(0, _c312_board), _p(1, lambda: _t(BX312[0], BD[1] + 280, "盛岡", 110, INK, "middle", 360)), _p(2, _c312_blank)],
    src=S_J, note="模式・板の形と欄は描いた形でない", schem=True)


# ── c319 教官の見当（盛岡の市街に近づかず西側・横手の空域の北側付近＝判決の認定）。位置と大きさは模式
def _c319_city():
    return (F.circ(1350.0, 470.0, 110.0, INK, None, None, op=0.12) + F.circ(1350.0, 470.0, 110.0, "none", INK, 5)
            + _t(1350.0, 634.0, "盛岡の市街", 44, INK, "middle", 300))


def _c319_area():
    pts = [(820.0 + 230.0 * math.cos(math.radians(a)), 430.0 + 140.0 * math.sin(math.radians(a))) for a in range(0, 361, 10)]
    return (F.poly(pts, J.AMBER, None, close=True, op=0.14) + F.poly(pts, "none", J.AMBER, 6, close=True, dash="18 12")
            + _t(820.0, 444.0, "教官の見当", 44, J.AMBER, "middle", 300))


def _c319_away():
    return _arrow(1060.0, 440.0, 1225.0, 462.0, J.TICK, 5, 22, "12 10") + _xmark(1142.0, 451.0, 24, J.ALERT, 8)


def _c319_yokote():
    return (F.rect(560.0, 700.0, 420.0, 120.0, "none", J.TICK, 5, rx=14, dash="14 10") + _t(770.0, 776.0, "横手の空域", 44, J.TICK, "middle", 380)
            + _arrow(770.0, 690.0, 770.0, 585.0, J.TICK, 4, 20))


C319 = [
    _at(_c(0, T, head="教官の考え", lines="市街に近づかず", sub="その西側で", cap=50), 300, 430),
    _at(_c(1, T, head="判決の認定", lines="北側付近の空域で", cap=48), 1450, 780),
]
VIEWS["c319"] = _z(2, "訓練の場所", "見当のつけ方", C319, [
    _p(0, _c319_city), _p(0, _c319_area), _p(0, _c319_away, arrow=True),
    _p(0, lambda: _arrow(1720.0, 840.0, 1720.0, 730.0, J.TICK, 5, 22) + _t(1756.0, 800.0, "北", 40, J.TICK, "start", 80)),
    _p(1, _c319_yokote, arrow=True)],
    src=S_J, note="模式・教官の考え（判決の認定）・位置と大きさは描いた形でない", schem=True)

# ── c325 3つの言い方（1971 防衛局長＝伝聞・1972 参事官・1983 最高裁）。語りは最高裁の認定＝最高裁の札を囲む
# 🔧 check_fuda F3（毎秒 9.2字）＝1971年の答弁の原文の札と小さい字を外した（「教官の話」＝伝聞・どの教官かは答弁に無い）
C325 = [
    _at(_c(0, K, head="1971年 防衛庁", lines="教官の話", cap=56), 330, 470),
    _at(_c(0, K, head="1972年 参事官", lines="臨時に横手", cap=56), 960, 470),
    _at(_c(0, T, head="1983年 最高裁", lines="盛岡", q=True, cap=72), 1590, 470),
    _at(_c(1, T, lines="進言と承認", cap=56), 1590, 750),
]
VIEWS["c325"] = _z(2, "3つの言い方", "空域の名と決め手", C325, [
    _p(0, lambda: _ring(C325[2], sc(T))),
    _p(1, lambda: _arrow(1590.0, _zbox(C325[2])[1] + _zbox(C325[2])[3] + 24, 1590.0, _zbox(C325[3])[1] - 12, sc(T), 6, 22), arrow=True),
], src=kk("106613843X00119710805", "106904889X00319720817") + "・" + S_J)

# ── 第3章 c402〜c404・c410 J11L の線（縦・模式）と守る幅。c403・c404・c410 の帯は同じ物差し（1キロ＝KM px）＝門番 ⑤ num が幅の字と位置を照らす
JX, JY0, JY1 = 960.0, 300.0, 820.0
KM = 36.0
AX_KM = ((0.0, JX), (10.0, JX + 10 * KM))


def _j11l(lab=True):
    g = F.line(JX, JY0, JX, JY1, J.AMBER, 8)
    for y in (JY0, JY1):
        g += F.circ(JX, y, 16, J.BG2, J.AMBER, 6) + _t(JX + 30, y + 14, "NDB", 34, J.TICK, "start", 140)
    return g + (_t(JX - 30, JY0 + 100, "J11L", 44, J.AMBER, "end", 200) if lab else "")      # 🔧 layout：帯の上の辺（JB0）より下に


# 🔧 layout：帯の上下の辺が線の両端の「NDB」の字を横切った＝帯は線の端から 30px 内側まで（JB0・JB1）
JB0, JB1 = JY0 + 30, JY1 - 30


def _c402_band():
    return (F.rect(JX - 200, JB0, 400, JB1 - JB0, J.TICK, None, None, op=0.22) + F.line(JX - 200, JB0, JX - 200, JB1, J.TICK, 3, dash="12 10")
            + F.line(JX + 200, JB0, JX + 200, JB1, J.TICK, 3, dash="12 10") + _t(JX + 214, JB1 - 20, "守る幅", 40, J.TICK, "start", 240))


C402 = [
    _at(_c(0, K, head="防衛局長の説明", lines=("点と点を結ぶところを", "最短距離で"), q=True, cap=46), 420, 430),
    _at(_c(1, K, lines=("航空局長の通達で", "内部規程として"), q=True, cap=46), 1500, 640),
]
VIEWS["c402"] = _z(2, "ジェット・ルート", "守る幅の決まり", C402, [_p(1, _c402_band), _p(0, _j11l)],
                   src=kk("106613843X00119710805"), note="模式・線の向きと幅は描いた形でない", schem=True)


def _kmband(km, col, op, lab=None, ly=760.0, dim=False, lx=None):
    """J11L の両側の帯（片側 km キロ）。lx＝幅の字の左端（無ければ矢印の真ん中）＝ほかの帯の辺が字を横切らない所へ。"""
    w = km * KM
    g = F.rect(JX - w, JB0, 2 * w, JB1 - JB0, col, None, None, op=op)
    g += F.line(JX - w, JB0, JX - w, JB1, col, 3, dash="12 10") + F.line(JX + w, JB0, JX + w, JB1, col, 3, dash="12 10")
    if lab:
        c2 = J.TICK if dim else J.AMBER
        g += _arrow(JX + 10, ly, JX + w - 6, ly, c2, 4, 18)
        g += (_t(lx, ly - 22, lab, 40 if dim else 48, c2, "start", w) if lx is not None
              else _t(JX + w / 2, ly - 22, lab, 40 if dim else 48, c2, "middle", w + 200))
    return g


C403 = [_at(_c(1, K, head="運輸省の航空局長", lines="1973年の答弁", cap=46), 1660, 420)]
VIEWS["c403"] = _z(2, "守る幅の数", "J11L の両側", C403, [_p(0, lambda: _kmband(16, sc(K), 0.20, "片側約16キロ")), _p(0, _j11l)],
                   src=kk("107113830X00919730424"), note="模式・線の向きは描いた形でない・幅は比例", schem=True,
                   tl=dict(kind="num", ax=AX_KM, pts=(("約16キロ", JX + 16 * KM),)))

C404 = [
    _at(_c(0, T, head="松島派遣隊", lines="飛行訓練準則", cap=52), 290, 400),
    _at(_c(1, T, lines="編隊の訓練を制限", sub="5海里", cap=50), 1600, 640),
]
VIEWS["c404"] = _z(3, "自衛隊の準則", "準則の幅", C404, [
    # 🔧 layout：薄い帯の幅の字は9キロの帯の右の辺の外（辺が字を横切らない）
    _p(0, lambda: _kmband(16, J.TICK, 0.08, "約16キロ", ly=372.0, dim=True, lx=JX + 9 * KM + 24)),
    _p(1, lambda: _kmband(9, sc(T), 0.26, "約9キロ")),
    _p(0, _j11l),
    _p(2, lambda: _ring(C404[1], sc(T))),
], src=S_J + "・" + kk("107113830X00919730424"), note="模式・幅は比例・薄い帯は運輸省の言う幅", schem=True,
    tl=dict(kind="num", ax=AX_KM, pts=(("約9キロ", JX + 9 * KM), ("約16キロ", JX + 16 * KM))))

# ── c405 高さの断面（縦の比例＝門番 ⑤ num・y の座標）。帯＝準則の高さ（判決）・印＝旅客機（判決）と2機（長官の報告）
H405 = dict(x=760.0, y0=820.0, y1=300.0, v0=7400.0, v1=9600.0)
M405 = (("旅客機", 8500.0, 820.0, T), ("訓練機", 8600.0, 1260.0, K), ("教官機", 7700.0, 820.0, K))


def _h405(v):
    return H405["y0"] + (v - H405["v0"]) * (H405["y1"] - H405["y0"]) / (H405["v1"] - H405["v0"])


def _c405_band():
    x, ya, yb = H405["x"], _h405(9400), _h405(7600)
    g = F.line(x, H405["y1"], x, H405["y0"], J.TICK, 4)
    g += F.rect(x, ya, 960.0, yb - ya, sc(T), None, None, op=0.20) + F.line(x, ya, x + 960, ya, sc(T), 4) + F.line(x, yb, x + 960, yb, sc(T), 4)
    return g + _t(x + 950, ya - 16, "約9,400メートル", 40, J.AMBER, "end", 420) + _t(x + 950, yb + 48, "約7,600メートル", 40, J.AMBER, "end", 420)


def _c405_mark(i):
    name, v, x, who = M405[i]
    y = _h405(v)
    return (F.line(x, y, x + 100, y, sc(who), 10) + _t(x + 116, y + 14, name, 40, INK, "start", 140)
            + _t(x + 246, y + 14, f"約{int(v):,}", 40, J.AMBER, "start", 200))


C405 = [
    _at(_c(0, T, head="判決が引く準則", lines="訓練を制限する高さ", cap=44), 400, 440),
    _at(_c(1, K, head="防衛庁長官の報告", lines="2機の高さ", cap=48), 400, 680),
]
VIEWS["c405"] = _z(2, "高さの断面", "帯の中の3機", C405, [_p(0, _c405_band), _p(1, lambda: _c405_mark(0) + _c405_mark(1) + _c405_mark(2))],
                   src=S_J + "・" + kk("106614889X00119710802"), note="模式・高さは比例・横の位置は描いた形でない", schem=True,
                   tl=dict(kind="num", ax=((H405["v0"], H405["y0"]), (H405["v1"], H405["y1"])),
                           pts=(("約9,400", _h405(9400)), ("約7,600", _h405(7600))) + tuple((f"約{int(v):,}", _h405(v)) for _n, v, _x, _w in M405)))

# ── c407 通告の年（月の比例＝門番 ⑤ ym）
Y407 = dict(x0=260.0, x1=1660.0, y=560.0, v0=1961.0, v1=1973.0)
V407 = (1961 + 11.5 / 12, 1971 + 6.5 / 12)
C407 = [
    _at(_c(0, K, head="運輸省の航空局長", big="1961年12月", bcap=58), 420, 360),
    _at(_c(0, None, big="1971年7月", lines="事故", bcap=58, cap=50), 1490, 360),
    _at(_c(1, K, lines="ジェット・ルートの幅", sub="防衛庁へ通告", cap=50), 420, 760),
]
VIEWS["c407"] = _z(2, "通告の時期", "事故までの年月", C407, [
    _p(0, lambda: _axis(Y407, range(1961, 1974))),
    _p(0, lambda: _bar(Y407, *V407, J.TICK, h=40) + _t((_lin(Y407, V407[0]) + _lin(Y407, V407[1])) / 2, Y407["y"] - 44, "約10年", 48, J.AMBER, "middle", 300)),
    _p(0, lambda: _lead(C407[0], _lin(Y407, V407[0]), Y407["y"]) + _lead(C407[1], _lin(Y407, V407[1]), Y407["y"])),
    _p(1, lambda: _lead(C407[2], _lin(Y407, V407[0]), Y407["y"])),
], src=kk("107114103X00719730509"),
    tl=dict(kind="ym", ax=((Y407["v0"], Y407["x0"]), (Y407["v1"], Y407["x1"])), pts=(("1961年12月", _lin(Y407, V407[0])), ("1971年7月", _lin(Y407, V407[1])))))


# ── c410 場所の2つの言い方（報告書＝線の上・最高裁＝西側5海里の内側）。帯の幅は c404 と同じ物差し（約9キロ）
def _c410_art():
    w = 9 * KM
    return (F.rect(JX - w, JY0, w, JY1 - JY0, sc(T), None, None, op=0.22) + F.line(JX - w, JY0, JX - w, JY1, sc(T), 3, dash="12 10") + _j11l())


C410 = [
    _at(_c(1, H, head="報告書", lines="J11Lの中", cap=56), 1420, 420),
    _at(_c(1, T, head="最高裁", lines="西側5海里の内側", cap=52), 400, 690),
    _at(_c(2, None, head="どちらも", lines="編隊の訓練を避ける空", cap=50), 1400, 730),
]
VIEWS["c410"] = _z(3, "2つの書き方", "線の上と西側", C410, [
    _p(0, _c410_art), _p(1, lambda: _tie(C410[0], JX, 470.0) + _tie(C410[1], 800.0, 600.0))],
    src=S_W + "・" + S_J, note="模式・位置は描いた形でない・帯は5海里", schem=True)


# ── c411 機動隊形の旋回に要る空間（上下・左右・前後に大きな箱＝模式）
def _c411_box():
    fx0, fy0, fx1, fy1 = 820.0, 430.0, 1300.0, 740.0
    dx, dy = 150.0, -110.0
    g = F.rect(fx0, fy0, fx1 - fx0, fy1 - fy0, J.BG2, None, None, op=0.25)
    for x1, y1, x2, y2 in ((fx0, fy0, fx1, fy0), (fx1, fy0, fx1, fy1), (fx1, fy1, fx0, fy1), (fx0, fy1, fx0, fy0),
                           (fx0 + dx, fy0 + dy, fx1 + dx, fy0 + dy), (fx1 + dx, fy0 + dy, fx1 + dx, fy1 + dy),
                           (fx0, fy0, fx0 + dx, fy0 + dy), (fx1, fy0, fx1 + dx, fy0 + dy), (fx1, fy1, fx1 + dx, fy1 + dy)):
        g += F.line(x1, y1, x2, y2, J.TICK, 4)
    g += _dbl(1560.0, 330.0, 1560.0, 700.0, J.AMBER) + _t(1600.0, 530.0, "上下", 44, J.AMBER, "start", 120)
    g += _dbl(820.0, 790.0, 1300.0, 790.0, J.AMBER) + _t(1060.0, 846.0, "左右", 44, J.AMBER, "middle", 120)
    return g + _dbl(1330.0, 770.0, 1490.0, 655.0, J.AMBER) + _t(1520.0, 760.0, "前後", 44, J.AMBER, "start", 120)


C411 = [
    _at(_c(0, H, head="報告書の推定", lines="機動隊形の旋回", cap=52), 380, 420),
    _at(_c(1, H, lines=("非常に大きな", "飛行空間"), q=True, cap=52), 380, 690),
]
VIEWS["c411"] = _z(2, "旋回に要る広さ", "訓練の型と空域", C411, [_p(1, _c411_box, arrow=True), _p(0, lambda: _plane(1060.0, 585.0, INK, k=0.8))],
                   src=S_W, note="模式・箱の大きさは描いた形でない", schem=True)

# ── 第4章 c503 2機の並び（長官の報告＝教官機 左の前・訓練機 右のうしろ）。上が進む向き
C503 = [
    _at(_c(0, K, head="教官機", big="約7,700メートル", lines="左の前", bcap=58, cap=48), 380, 560),
    _at(_c(1, K, head="訓練機", big="約8,600メートル", lines="右のうしろ", bcap=58, cap=48), 1540, 690),
]
VIEWS["c503"] = _z(2, "2機の並び", "南へ下るとき", C503, [
    _p(0, lambda: _arrow(960.0, 380.0, 960.0, 262.0, J.TICK, 5, 22) + _t(990.0, 330.0, "進む向き（南）", 38, J.TICK, "start", 360), arrow=True),
    _p(0, lambda: _plane(760.0, 430.0, INK)), _p(1, lambda: _plane(1160.0, 690.0, INK))],
    src=kk("106614889X00119710802"), note="模式・上が進む向き・2機の間の距離は描いた形でない", schem=True)

# ── c510・c511 方位の図の続き（c509 と同じ輪・同じ物差し）
C510 = [
    _at(_c(0, T, head="旅客機", big="右78度", lines="約4.3キロ", sub="上10度", bcap=64, cap=50, dim=True), 1580, 440),
    _at(_c(0, T, big="右116度", lines="約1.9キロ", sub="上29度", bcap=64, cap=50), 1360, 740),
]
VIEWS["c510"] = _z(2, "訓練機の方位", "同じ30秒前", C510, [
    # 🔧 layout：面の左の辺が「0度」「180度」の字を横切った＝面は真ん中の線から 60px 右から
    _p(1, lambda: F.rect(CP[0] + 60, 250.0, 1840.0 - CP[0] - 60, 600.0, J.AMBER, None, None, rx=18, op=0.07)
       + _t(1200.0, 300.0, "右の側", 48, J.AMBER, "middle", 300)),
    _p(0, _rose), _p(0, lambda: _ray(78, 4.3, PLANE, dim=True)), _p(0, lambda: _ray(116, 1.9, PLANE, "訓練機", side="start"))],
    src=S_J, note=N_POL, schem=True,
    tl=dict(kind="pol", c=CP, k=PK, pts=(("右116度", "約1.9キロ") + _pol(116, 1.9), ("右78度", "約4.3キロ") + _pol(78, 4.3))))

C511 = [
    # 🔧 重ね絵：札が約30秒前の旅客機の薄い印（右78度）を隠していた＝右へ
    _at(_c(0, T, head="約20秒前の旅客機", big="右106度", lines="約2.5キロ", sub=("上11度", "二審の「下方」は誤記"), bcap=64, cap=50), 1590, 440),
    _at(_c(1, T, big="右132度", lines="約1.7キロ", sub="上10度", bcap=64, cap=50), 1590, 735),
]
VIEWS["c511"] = _z(2, "方位の変わり方", "10秒のちの位置", C511, [
    _p(0, _rose), _p(0, lambda: _ray(78, 4.3, PLANE, dim=True) + _ray(116, 1.9, PLANE, dim=True)),
    _p(0, lambda: _ray(106, 2.5, PLANE, "旅客機", side="start")), _p(1, lambda: _ray(132, 1.7, PLANE, "訓練機", side="start", dy=60.0))],
    src=S_J, note=N_POL + "・薄い印は約30秒前", schem=True,
    tl=dict(kind="pol", c=CP, k=PK, pts=(("右106度", "約2.5キロ") + _pol(106, 2.5), ("右132度", "約1.7キロ") + _pol(132, 1.7))))


# ── 第5章 c605 図の作り方（3機の航跡 → 操縦席ごとの見え方の図＝視界図）。線の形は模式
def _c605_tracks():
    g = ""
    for i, (name, col, dash) in enumerate((("旅客機", INK, None), ("教官機", J.TICK, "16 10"), ("訓練機", J.LINE, "4 10"))):
        y0 = 450.0 + 110.0 * i
        pts = [(160.0 + 12.0 * k, y0 + 40.0 * math.sin(k / 7.0 + i)) for k in range(56)]
        g += F.poly(pts, "none", col, 7, dash=dash) + _t(pts[-1][0] + 20, pts[-1][1] + 14, name, 40, col, "start", 200)
    return g


C605 = [
    _at(_c(0, K, head="元委員長の説明", lines="3機の航跡", cap=52), 530, 305),
    _at(_c(1, K, lines="視界図", q=True, sub="操縦席ごとの見え方", cap=64), 1420, 545),
]
VIEWS["c605"] = _z(2, "図の作り方", "航跡から見え方へ", C605, [
    _p(0, _c605_tracks), _p(1, lambda: _arrow(990.0, 560.0, 1110.0, 560.0, J.AMBER, 7, 26), arrow=True),
    _p(1, lambda: F.rect(1130.0, 330.0, 580.0, 440.0, J.BG2, INK, 6, rx=40, op=0.55) + F.line(1150.0, 690.0, 1690.0, 690.0, J.TICK, 3, dash="12 10"))],
    src=kk("106914889X00219720823"), note="模式・線の形は実際の航跡でない", schem=True)

# ── c606 跡の描き方（旅客機＝記録の装置・2機＝教官と訓練生の記憶）
C606 = [
    _at(_c(0, K, head="旅客機", lines=("フライト・データ・", "レコーダ"), q=True, sub="跡ははっきり", icon="plane", cap=48), 520, 450),
    _at(_c(0, K, head="教官機と訓練機", lines="記録の装置なし", icon="plane", cap=48), 1400, 450),
    _at(_c(1, K, lines="記憶によって", q=True, sub="教官と訓練生の", cap=56), 1400, 720),
]
VIEWS["c606"] = _z(2, "跡の描き方", "記録と記憶", C606, [
    _p(1, lambda: _arrow(1400.0, _zbox(C606[1])[1] + _zbox(C606[1])[3] + 10, 1400.0, _zbox(C606[2])[1] - 12, sc(K), 6, 22), arrow=True)],
    src=kk("106914889X00219720823"))

# ── c610 第13図の考え（まっすぐ前の基準点・左へ約60度で訓練機）。どの機の席の図かは答弁に無い＝「見る位置」とだけ書く。角度は門番 ⑤ pol
VP, VR = (560.0, 640.0), 360.0


def _c610_pt():
    a = math.radians(-60.0)
    return VP[0] + VR * math.sin(a), VP[1] - VR * math.cos(a)


def _c610_base():
    x, y = VP
    g = F.circ(x, y, 14, INK) + _t(x, y + 58, "見る位置", 40, INK, "middle", 240)
    g += F.line(x, y - 24, x, y - VR, J.TICK, 5, dash="14 10") + F.circ(x, y - VR, 18, "none", INK, 5) + F.line(x - 26, y - VR, x + 26, y - VR, INK, 4)
    return g + _t(x + 34, y - VR + 14, "基準点", 40, INK, "start", 200)


def _c610_turn():
    x, y = VP
    px, py = _c610_pt()
    arc = [(x + 140 * math.sin(math.radians(t)), y - 140 * math.cos(math.radians(t))) for t in range(0, -61, -5)]
    g = F.line(x, y, px, py, J.AMBER, 5, dash="14 10") + F.poly(arc, "none", J.AMBER, 5)
    return g + _t(x + 230 * math.sin(math.radians(-30)), y - 230 * math.cos(math.radians(-30)) + 14, "左へ約60度", 40, J.AMBER, "middle", 260)


C610 = [
    _at(_c(0, K, head="元委員長の説明", lines="第13図", cap=60), 1300, 380),
    _at(_c(1, K, lines="左のほう六十度", q=True, sub="訓練機が見える", cap=56), 1300, 680),
]
VIEWS["c610"] = _z(2, "図の上の見え方", "まっすぐ前から左へ", C610, [
    _p(0, _c610_base), _p(0, _c610_turn),
    _p(1, lambda: _blip(*_c610_pt(), PLANE) + _t(_c610_pt()[0], _c610_pt()[1] + 74, "訓練機", 40, PLANE, "middle", 200))],
    src=kk("106914889X00219720823"), note="模式・どの機の席の図かは答弁に無い・角度だけ", schem=True,
    tl=dict(kind="pol", c=VP, k=1.0, pts=(("左へ約60度", None) + _c610_pt(),)))


# ── c612・c613 注視野の考え（委員長の説明の範囲＝円は模式・広さと向きは描いた形でない）。字幕は札の原文を読む行で消す
def _vz(cx, cy, r, lab, col=None):
    col = col or J.LINE
    return (F.circ(cx, cy, r, col, None, None, op=0.14) + F.circ(cx, cy, r, "none", col, 5, op=0.9)
            + _t(cx, cy + r + 50, lab, 40, col, "middle", 2 * r + 120))


C612 = [
    _at(_c(0, K, head="報告書の解析", lines="訓練生にとって", cap=46), 400, 300),
    _at(_c(1, K, lines="注視野の外にあった", q=True, cap=56), 1480, 640),
]
VIEWS["c612"] = _z(2, "訓練生の見え方", "解析の考え", C612, [
    _p(0, lambda: _vz(520.0, 590.0, 180.0, "前を見るとき") + _vz(900.0, 590.0, 180.0, "教官機を見るとき") + _plane(900.0, 590.0, INK, k=0.6)),
    _p(1, lambda: _blip(1480.0, 430.0, PLANE) + _t(1440.0, 444.0, "旅客機", 42, PLANE, "end", 200))],
    src=kk("106914889X00219720823"), note="模式・注視野の広さと向きは描いた形でない", mute=(1,), schem=True)

C613 = [
    _at(_c(0, K, head="元委員長が読んだ報告書", lines="教官にとって", cap=46), 400, 300),
    # 🔧 echo：見出しの字が語りの行の字面と同じ＝数を黄の大きな字に分けた
    _at(_c(1, K, head="少なくとも", big="30秒前から", lines="注視野内", q=True, bcap=64, cap=64), 1450, 600),
]
VIEWS["c613"] = _z(2, "教官の見え方", "報告書の考え", C613, [
    _p(0, lambda: _vz(780.0, 580.0, 200.0, "訓練機の方を見るとき") + _plane(720.0, 620.0, INK, k=0.6)),
    _p(1, lambda: _blip(880.0, 480.0, PLANE) + _t(840.0, 494.0, "旅客機", 42, PLANE, "end", 200))],
    src=kk("106904889X00319720817"), note="模式・注視野の広さと向きは描いた形でない", mute=(1,), schem=True)

# ── c620 防衛庁の質問書（c518 と同じ秒の帯＝門番 ⑤ hms）
C620 = [
    _at(_c(0, K, head="報告書の推定", big="14:02:39", bcap=72), 990, 350),
    _at(_c(1, K, head="防衛庁の質問書", big="1972年12月25日", bcap=58), 1500, 350),
    _at(_c(2, K, big="14:02:32", lines="接触したと思われる", q=True, bcap=72, cap=46), 520, 760),
]
VIEWS["c620"] = _z(3, "反対の時刻", "質問書に書いた秒", C620, [
    _p(0, _t518_axis), _p(0, lambda: _lead(C620[0], _lin(YT, VT[0]), YT["y"])),
    _p(2, lambda: _lead(C620[2], _lin(YT, VT[1]), YT["y"]) + _t518_gap())],
    src=kk("107114103X00719730509"), note="目盛りは10秒ごと",
    tl=dict(kind="hms", ax=((YT["v0"], YT["x0"]), (YT["v1"], YT["x1"])), pts=(("14:02:39", _lin(YT, VT[0])), ("14:02:32", _lin(YT, VT[1])))))


# ── 第9章 ca03 補償の残り（3人の分＝四角3つ・人の形は使わない・名前は出さない）
def _ca03_boxes(hi=False):
    g = ""
    for i in range(3):
        on = hi and i == 0
        g += F.rect(760.0 + 140.0 * i - 45, 385.0, 90, 90, J.AMBER if on else J.BG2, sc(K), 6, rx=16, op=0.9 if on else 0.6)
    return g


CA03 = [
    _at(_c(0, K, head="防衛庁の答弁", big="3人", lines="話し合いがまとまらず", bcap=80, cap=48), 400, 450),
    _at(_c(0, K, lines="裁判に", cap=64), 1450, 430),
    _at(_c(1, K, head="そのうち", big="1人の分", lines="判決を受けて賠償", sub="1975年の時点", bcap=72, cap=48), 1300, 715),
]
VIEWS["ca03"] = _z(2, "補償の残り", "話し合いと裁判", CA03, [
    _p(0, _ca03_boxes), _p(0, lambda: _arrow(1100.0, 430.0, 1306.0, 430.0, sc(K), 6, 22), arrow=True), _p(1, lambda: _ca03_boxes(True))],
    src=kk("107503830X00819750314"))


# ── 第10章 cb02 要綱の柱（訓練空域を空港と航空路から分ける・特別管制空域を広げる）＋1975年の改正法の条文
def _cb02_sep():
    g = F.line(130.0, 420.0, 900.0, 420.0, INK, 7) + _t(140.0, 396.0, "航空路", 40, INK, "start", 200)
    g += F.circ(260.0, 650.0, 56.0, J.BG2, INK, 6) + F.line(222.0, 650.0, 298.0, 650.0, INK, 8) + _t(260.0, 750.0, "空港", 40, INK, "middle", 200)
    g += F.rect(540.0, 600.0, 300.0, 160.0, J.AMBER, None, None, rx=14, op=0.16) + F.rect(540.0, 600.0, 300.0, 160.0, "none", J.AMBER, 6, rx=14, dash="16 10")
    g += _t(690.0, 694.0, "訓練空域", 42, J.AMBER, "middle", 280)
    return g + _dbl(690.0, 440.0, 690.0, 588.0, J.AMBER) + _dbl(326.0, 680.0, 528.0, 680.0, J.AMBER)


def _cb02_ctl():
    return (F.rect(130.0, 395.0, 770.0, 50.0, sc(K), None, None, op=0.30) + F.rect(120.0, 350.0, 790.0, 140.0, "none", sc(K), 5, rx=18, dash="16 10")
            + _t(515.0, 338.0, "特別管制空域", 40, sc(K), "middle", 400))


CB02 = [
    _at(_c(0, K, head="緊急対策要綱", lines=("空港及び航空路", "からの分離"), q=True, cap=48), 1420, 330),
    _at(_c(1, K, lines="特別管制空域の拡大", q=True, cap=48), 1420, 545),
    _at(_c(2, L, head="1975年の改正法", lines=("計器飛行方式に", "よらなければ"), q=True, cap=48), 1420, 740),
]
VIEWS["cb02"] = _z(3, "対策の柱", "2つの決め", CB02, [_p(0, _cb02_sep, arrow=True), _p(1, _cb02_ctl)],
                   src=kk("106613843X00119710805") + "・" + S_LAW, note="模式・空域の形は描いた形でない", schem=True)

# ── cb12 航空法 第71条の2（e-Gov の今の版＝ref/ep31/src/web/egov_koukuho_71-2_20261108.xml・⑥ の頭で当て直す）。
#    🔴 衆議院の頁の誤字（「運輪」「衡突」）は出さない＝画面の片は今の版の字。1975年の版との違いは「運輸大臣」→「国土交通大臣」・「行なつて」→「行つて」（どちらも画面に出さない所）だけ
#    🔧 check_fuda F3（毎秒 9.5字）＝札は2つの片だけ（「外が見えない天気を除く」は語りだけ）
CB12 = [
    _at(_c(0, L, head="航空法 第71条の2", lines=("指示に従つている航行で", "あるとないとにかかわらず"), q=True, cap=56), 960, 420),
    _at(_c(1, L, lines="見張りをしなければならない", q=True, cap=60), 960, 700),
]
VIEWS["cb12"] = _z(2, "操縦する人の義務", "いまの条文", CB12, [], src="e-Gov 法令検索の航空法（2026年11月に取り込み）")


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
