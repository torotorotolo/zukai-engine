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
FU["c607"] = _f(2, "見え方の図", "委員長の説明", [
    _c(0, K, head="図の前提", lines="まっすぐ前を見た場合", sub="基準点", icon="eye", cell=(0, 0)),
    _c(1, K, head="頭の振り方", lines="分からない", cell=(1, 0)),
], src=kk("106914889X00219720823"))
FU["c608"] = _f(2, "図の言葉", "委員長の説明", [
    _c(0, K, head="報告書の図で", lines="注視野", sub="航空医学の用語", cap=80, cell=(0, 0)),
], src=kk("106914889X00219720823"))
FU["c614"] = _f(3, "証拠の届かない所", "委員長と最高裁", [
    _c(0, K, head="30秒前から数秒前", lines="訓練機を見たか", sub="事実が分からない", cell=(0, 0)),
    _c(1, K, head="元委員長", lines="最終的な結論", q=True, sub="出なかった", cell=(1, 0)),
    _c(2, T, head="最高裁（避けられた可能性）", lines="実は極めて限られたもの", q=True, cell=(0, 1), span=(2, 1)),
], src=kk("106904889X00319720817") + "・" + S_J, mute=(1,))
FU["c616"] = _f(2, "7秒の手がかり", "委員長の説明", [
    _c(0, K, head="録音", big="接触の約7秒前", lines="「雑音」", cell=(0, 0)),
    _c(1, K, head="雑音の解釈から", lines="確かに見つけていた", cell=(1, 0)),
], [_x(1, "a", "b")], src=kk("106914889X00219720823"))
FU["c617"] = _f(3, "報告書の想定", "雑音の時点の機長", [
    _c(0, K, head="機長", lines=("間近の訓練機を見た", "または急な接近"), cell=(0, 0)),
    _c(1, K, head="報告書", lines="操縦輪を強く保持", sub="と考えられる", cell=(1, 0)),
    _c(2, K, head="委員長", lines="断定ではない", cell=(0, 1), span=(2, 1)),
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
FU["c933"] = _f(2, "防衛庁の受けとめ", "官房長の答弁", [
    _c(0, K, head="刑事の裁判", big="1985年", lines="結審", cell=(0, 0)),
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
