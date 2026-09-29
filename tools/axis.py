# -*- coding: utf-8 -*-
"""axis.py — 軸の型「年表・時間の帯」（2026-09-29 新設・14本目 ⑤b-5）。

■ 何か（Vault `Projects/事故検証-14本目-映像方針-追補-文字の画面-20260926.md` §3 の【年表】【帯】）
  横に1本の軸を引き、記録にある年月日・時刻を**位置**で見せる図解。数字の読み上げは字幕に任せ、図は位置・順・長さを持つ（§5b-9）。
  13本目までの `titan_fig.timeline`（旗が段ごとに立つだけ）に足りなかった3つを持つ：
    ① **進むカーソル**（段の鍵で動く部品＝`kind="anim"`・線と三角だけ＝半透明の面を持たない §5b-91）
    ② **前のカットからの続き**（`past=` は基図に沈んだ色で描く＝c803→c804→c809→c818 の交信の帯）
    ③ **割れる時刻の印**（`split`＝出典の名だけを添えた同じ形の目盛り。**どれが正しいとは描かない**＝色・大きさを変えない）
  15本目も使い回す（出典の名の表示は `cuts/ss.AXIS_DOCS`＝§0b）。

■ 見え方（view）
  date  … 年表。値は "1994" ／ "2012-10" ／ "2013-01-24"（書いた細かさが、門番の許す幅になる）
  clock … 時刻の帯。値は "8:52" ／ "翌9:10"（翌日）
  lanes … 交信の帯＝clock に「話し手の段」を足す。段の名は `lanes=("管制", "近くの船", "セウォル号")`
          🔴 私人の言葉を帯に書かない（§2 守りの線）＝交信 `link` は**文字を持てない**（門番が止める）

■ SPEC の書き方
  fig=("axis", dict(view="clock", span=("18:00", "翌10:00"), ticks=("18:00", "20:00", …),
                    past=[…], steps=[dict(add=[…], cur="21:05"), dict()], note="…", src=ss.src([…])))
  部品（add と past に書く・段に1つずつでなく何個でも）：
    dict(k="pt", at="21:05", t="出港", rec="海審 p1038")          … 点（アンバー）。t は項目名だけ（語りの文を書かない）
    dict(k="split", at="9:46", rec="判決 p18")                     … 割れる時刻の印（出典の名は rec から組む）
    dict(k="span", a="18:30", b="21:05", t="遅れ", rec=[…], c="ALERT") … 区間（軸の上の太い帯）
    dict(k="br", a="1994-04-01", b="2012-10-08", rec=[…])           … 長さの括弧（軸の上・数字は書かない）
    dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13", both=False) … 交信（lanes だけ）
    dict(k="chips", at="2026-01-28", chips=["舵の使い方", "装置の故障"], rec=…)  … 前の段の点の下に項目の札だけ足す
    ⚠️ 年だけの値（"2015"）は年の真ん中に置く（目盛りは年の頭）。同じ時刻の2本目の交信は lab=False（時刻の札を重ねない）
    欄：by=True＝点にも出典の名を添える（🔴 割れる時刻〈ss.ILLU_SPLIT_TIMES〉の点は必須＝門番）／
        chips=["内側の原因", …]＝点の下に並べる項目の札（原因は「並べるだけ」）／c="INST" など色の名
  cur … その段でカーソルを置く値（書かなければ前の段のまま）。`start=dict(cur=…)` で頭の位置（既定は軸の左端）
  🔴 rec（記録の頁）は**全部の値に要る**。門番 `check_axis` が自分の側の記録の表 `REC_AXIS` と照らす（§5b-88）

■ 門番 `check_axis`＝①値が記録の表にあって頁が合う ②**描いた画素の x を目盛りの画素から逆算**して値と合う
  ③割れる時刻は2つ以上・同じ形 ④交信に文字が無い・段の名が決まった名だけ
  x は全部この関数が組む（`f.mech`）＝描く側と門番が同じ幾何（[[feedback-gates-must-share-the-production-geometry]]）
"""
from __future__ import annotations

import datetime
import re

import jiko_style as J
import titan_fig as F

VIEWS = ("date", "clock", "lanes")
# 軸の左右（画素）。lanes は左に段の名を置くので左を空ける
X0, X1 = F.BX0 + 110, F.BX1 - 110
X0_LANES = F.BX0 + 250
AY = F.BY0 + 0.64 * F.BH                 # date・clock の軸の高さ（上に札の段・下に目盛りと項目の札）
ROW_UP = (90, 244, 398)                  # 札の段（軸からの高さ。字の下端）
CAP_TOP, CAP_T, CAP_D = 56, 40, 30       # 札の字の大きさ（時刻・項目名・出典の名）。13本目の timeline は 40／32
#   ⚠️ 44／34／28 では項目が2〜4個のカットで軸の上が広く空いた（⑤b-5 の下見）
OFF = 8                                  # 左右に寄せた札（anchor start／end）の文字の端と縦の線の間（20 だと近い2点が同じ段に並べなかった）
LANE_Y0, LANE_GAP = F.BY0 + 190, 130     # lanes の段（上から）
MONTH0 = 1                               # 月の数え始め（🔴 門番の陽性対照がここを壊す）
NEXT_DAY = 24 * 60                       # 「翌」の足し分（分）（同上）
COL = dict(pt="AMBER", split="DOC", span="LINE", br="LINE", link="LINE", chips="LINE")


# ══════════════════════════════════════════════════════════
#  値（文字 → 軸の上の数）。🔴 門番は別に自分の読み方を持つ
# ══════════════════════════════════════════════════════════
def _yr(d):
    """日付 → 年（小数）。その年の日数で割る。"""
    j = datetime.date(d.year, 1, 1)
    return d.year + (d - j).days / (datetime.date(d.year + 1, 1, 1) - j).days


def val(view, s):
    """(数, 細かさ)。date＝年（小数）・細かさ year|month|day／clock・lanes＝分・細かさ min。"""
    s = str(s).strip()
    if view == "date":
        m = re.fullmatch(r"(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?", s)
        if not m:
            raise ValueError(f"axis：年月日の書き方が違う {s!r}（1994／2012-10／2013-01-24）")
        y = int(m[1])
        if not m[2]:
            return float(y), "year"
        # 月は暦の日数で置く（12等分にすると月の目盛りが一直線に並ばない＝門番が捕まえた）
        if m[3]:
            return _yr(datetime.date(y, int(m[2]), int(m[3]))), "day"
        mo = int(m[2]) + 1 - MONTH0
        y, mo = y + (mo - 1) // 12, (mo - 1) % 12 + 1
        return _yr(datetime.date(y, mo, 1)), "month"
    m = re.fullmatch(r"(翌)?(\d{1,2}):(\d{2})", s)
    if not m:
        raise ValueError(f"axis：時刻の書き方が違う {s!r}（8:52／翌9:10）")
    return (NEXT_DAY if m[1] else 0) + int(m[2]) * 60 + int(m[3]), "min"


def label(view, s, fmt=""):
    """画面に出す値の文字（date＝「1994年4月1日」・clock＝「8:52」）。fmt="ym"＝年月まで・"y"＝年だけ（語りの細かさに合わせる）。"""
    s = str(s).strip()
    if view == "date":
        p = s.split("-")[:{"ym": 2, "y": 1}.get(fmt, 3)]
        return p[0] + "年" + (f"{int(p[1])}月" if len(p) > 1 else "") + (f"{int(p[2])}日" if len(p) > 2 else "")
    return s.replace("翌", "")


def doc_names(rec):
    """rec（「判決 p18」か list）→ 画面に出す出典の名（`cuts/ss.AXIS_DOCS`）。"""
    try:
        from cuts import ss
        names = getattr(ss, "AXIS_DOCS", {})
    except Exception:  # noqa: BLE001
        names = {}
    out = []
    for r in (rec if isinstance(rec, (list, tuple)) else [rec]):
        d = str(r).split(" p")[0].strip()
        nm = names.get(d, d)
        if nm not in out:
            out.append(nm)
    return "・".join(out)


def _c(name, dflt):
    nm = name or dflt
    return nm if nm.startswith("#") else getattr(J, nm)


# ══════════════════════════════════════════════════════════
#  型の本体
# ══════════════════════════════════════════════════════════
class _Ax:
    def __init__(self, view, span, lanes):
        self.view = view
        self.a, _ = val(view, span[0])
        self.b, _ = val(view, span[1])
        if self.b <= self.a:
            raise ValueError(f"axis：span が逆 {span}")
        self.x0 = X0_LANES if view == "lanes" else X0
        self.x1 = X1
        self.lanes = list(lanes or [])
        if view == "lanes":
            if len(self.lanes) < 2:
                raise ValueError("axis：lanes には段の名を2つ以上")
            self.ly = {nm: LANE_Y0 + LANE_GAP * i for i, nm in enumerate(self.lanes)}
            self.ay = LANE_Y0 + LANE_GAP * (len(self.lanes) - 1) + 70    # 目盛りの軸は段の下
            self.top = LANE_Y0 - 40
        else:
            self.ly = {}
            self.ay = AY
            self.top = AY - 20

    def x(self, s, item=False):
        v, pr = val(self.view, s)
        if item and pr == "year":
            v += 0.5          # 年だけの記録は年の真ん中に置く（目盛りはその年の頭＝1月に置くと「1月」と読める）
        if not (self.a - 1e-9 <= v <= self.b + 1e-9):
            raise ValueError(f"axis：{s} が軸の範囲 {self.a}〜{self.b} の外")
        return self.x0 + (self.x1 - self.x0) * (v - self.a) / (self.b - self.a)


def _tick_lab(view, s):
    if view == "date":
        p = s.split("-")
        return (f"{int(p[1])}月", p[0] + "年") if len(p) > 1 else (p[0], "")
    return (s.replace("翌", ""), "翌日" if s.startswith("翌") and s.replace("翌", "") in ("0:00", "00:00") else "")


def _base(A, ticks, note, src):
    g = []
    ay = A.ay
    if A.view == "lanes":
        for nm, y in A.ly.items():
            g.append(F.line(A.x0, y, A.x1, y, J.LINE_DIM, 3, dash="10 10"))
            g.append(F.txtfit(F.BX0 + 8, y + 11, nm, A.x0 - F.BX0 - 30, cap=32, col=J.INK_W))
    g.append(F.line(A.x0, ay, A.x1, ay, J.LINE, 5))
    g.append(F.arrow(A.x1 - 4, ay, A.x1 + 34, ay, J.LINE, 5))
    tk = []
    for i, s in enumerate(ticks):
        x = A.x(s)
        lb, sub = _tick_lab(A.view, s)
        if A.view == "date" and sub and not (i == 0 or lb == "1月"):
            sub = ""          # 月の目盛りの年は、最初と1月にだけ添える
        g.append(F.line(x, ay - 12, x, ay + 12, J.LINE_DIM, 3))
        g.append(F.txt(x, ay + 48, lb, 30, J.TICK, "Noto", "middle", ol=6))
        if sub:
            g.append(F.txt(x, ay + 80, sub, 24, J.TICK, "Noto", "middle", ol=6))
        tk.append(dict(at=s, x=round(x, 2), lab=lb, sub=sub))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    return g, tk


def _rows(items, A):
    """札を上の段に振る（左から順に・前の札と重なれば1段上へ）。戻り＝{id(item): 段}。"""
    out, ends = {}, [-1e9] * len(ROW_UP)
    for it in sorted(items, key=lambda d: A.x(d["at"], True)):
        x = A.x(it["at"], True)
        w = it["_w"]
        lo = x - OFF if it["_anch"] == "start" else (x - w + OFF if it["_anch"] == "end" else x - w / 2)
        for r in range(len(ROW_UP)):
            if lo > ends[r] + 24:
                out[id(it)] = r
                ends[r] = lo + w
                break
        else:
            raise ValueError(f"axis：札が {len(ROW_UP)} 段に収まらない（{it['at']}）＝軸の範囲か札を減らす")
    return out


def _anch(A, x, w):
    if x - w / 2 < F.BX0 + 10:
        return "start"
    if x + w / 2 > F.BX1 - 10:
        return "end"
    return "middle"


def _prep(A, it):
    """札の文字と幅を決める（段の振り分けの前）。"""
    k = it["k"]
    if k not in COL:
        raise ValueError(f"axis：知らない部品 {k!r}（{tuple(COL)}）")
    top = label(A.view, it["at"], it.get("fmt", "")) if k in ("pt", "split", "link") and it.get("lab", True) else ""
    t = it.get("t", "")
    d = doc_names(it["rec"]) if (k == "split" or it.get("by")) else ""
    w = max(F.fm.width(top, CAP_TOP, "Dela") if top else 0, F.fm.width(t, CAP_T, "Noto") if t else 0,
            F.fm.width(d, CAP_D, "Noto") if d else 0) + 16
    it = dict(it, _top=top, _t=t, _d=d, _w=min(w, 460), _row=bool(top or t or d) and k != "link")
    # anchor＝近い2点の札を左右に振る（左の点は "end"・右の点は "start"＝縦の線が隣の札を貫かない）
    it["_anch"] = (it.get("anchor") or _anch(A, A.x(it["at"], True), it["_w"])) if "at" in it else "middle"
    return it


def _draw(A, it, row, dim):
    """1つの部品の SVG と、門番が読む画素の記録。"""
    k = it["k"]
    g = []
    col = J.LINE_DIM if dim else _c(it.get("c"), COL[k])
    ink = J.TICK if dim else J.INK_W
    rec = dict(k=k, rec=it.get("rec"), dim=dim, t=it.get("t", ""))
    if k in ("span", "br"):
        xa, xb = A.x(it["a"], True), A.x(it["b"], True)
        rec.update(a=it["a"], b=it["b"], xa=round(xa, 2), xb=round(xb, 2))
        if k == "span":
            y = A.ay
            g.append(F.rect(xa, y - 11, xb - xa, 22, col, op=0.45 if dim else 0.85))
            if it.get("t"):
                g.append(F.txtfit((xa + xb) / 2, y + 118, it["t"], max(160, xb - xa + 120), cap=30, col=ink if dim else col,
                                  anchor="middle"))
        else:
            y = A.ay - 40
            g += [F.line(xa, y, xb, y, col, 4), F.line(xa, y - 14, xa, y + 14, col, 4), F.line(xb, y - 14, xb, y + 14, col, 4)]
        return "".join(g), rec
    x = A.x(it["at"], True)
    rec.update(at=it["at"], x=round(x, 2), top=it["_top"], d=it["_d"], row=row, c=it.get("c") or COL[k],
               big=bool(it.get("big")), by=bool(it.get("by")), chips=[] if dim else list(it.get("chips") or []))
    if k == "chips":          # 項目の札だけを後の段で出す（点は前の段で描いた）
        return _chips(A, x, it.get("chips") or [], col, ink), rec
    anch = it["_anch"]
    tx = x - OFF if anch == "start" else (x + OFF if anch == "end" else x)
    if k == "link":
        y0, y1 = A.ly[it["fr"]], A.ly[it["to"]]
        rec.update(fr=it["fr"], to=it["to"], both=bool(it.get("both")))
        g.append(F.circ(x, y0, 9, col))
        g.append(F.arrow(x, y0, x, y1 + (-14 if y1 > y0 else 14), col, 4, 16))
        if it.get("both"):
            g.append(F.arrow(x, y1, x, y0 + (-14 if y0 > y1 else 14), col, 4, 16))
        # 時刻の札は話し手の点の左・段の線の上（段を積むと上の札へ伸びる点線が下の札を貫いた＝⑤b-5 の layout）
        if it["_top"]:
            g.append(F.txtfit(x - 16, y0 - 14, it["_top"], it["_w"], cap=40, col=ink, anchor="end", fam="Dela"))
        return "".join(g), rec
    ay = A.ay
    ty = ay - ROW_UP[row]
    lines = [(it["_top"], CAP_TOP, "Dela", ink)] if it["_top"] else []
    if it["_t"]:
        lines.append((it["_t"], CAP_T, "Noto", col if k == "pt" else ink))
    if it["_d"]:
        lines.append((it["_d"], CAP_D, "Noto", J.TICK if dim else _c("DOC", "DOC")))
    # 札は下から積む（一番下の行の下端＝ty）
    yy = ty
    for s, cap, fam, c in reversed(lines):
        g.append(F.txtfit(tx, yy, s, it["_w"], cap=cap, col=c, anchor=anch, fam=fam))
        yy -= cap + 6
    g.append(F.line(x, ay - 10, x, ty + 10, col, 3 if k == "split" else 4))
    if k == "pt":
        g.append(F.circ(x, ay, 12 if it.get("big") else 9, col))
    else:
        g.append(F.line(x, ay - 22, x, ay + 22, col, 6))
    if not dim:               # 前のカットの点（past）は項目の札を出さない（隣の点の札と重なる）
        g.append(_chips(A, x, it.get("chips") or [], col, ink))
    return "".join(g), rec


def _chips(A, x, chips, col, ink):
    """点の下（目盛りの札のさらに下）に項目の札を縦に並べる。原因は「並べるだけ」＝場面にしない。"""
    g = []
    ay = A.ay
    for i, ch in enumerate(chips):
        cy = ay + 108 + 58 * i
        w = F.fm.width(ch, 28, "Noto") + 36
        cx = min(max(x, F.BX0 + w / 2 + 4), F.BX1 - w / 2 - 4)
        g.append(F.line(x, ay + 60, x, cy - 22, J.LINE_DIM, 2, dash="4 6") if i == 0 else "")
        g.append(F.rect(cx - w / 2, cy - 22, w, 44, "none", col, 3, rx=8))
        g.append(F.txtfit(cx, cy + 10, ch, w - 16, cap=28, col=ink, anchor="middle"))
    return "".join(g)


def _cursor(A, xs):
    """進むカーソル＝縦の線と上の三角（段の鍵で x が動く）。🔴 面は不透明の三角だけ（§5b-91）。"""
    y0 = A.top - 6 if A.view == "lanes" else A.ay - 30
    y1 = A.ay + 16            # 目盛りの字（軸の下 +24 から）にかけない＝動く部品は札の層の上に描かれる（§5b-89）
    keys = [dict(stage=max(0, i - 1), delay=(0.0 if i == 0 else F.MECH_DELAY), dx=round(x - xs[0], 2), alpha=1.0)
            for i, x in enumerate(xs)]
    ln = dict(id="cur_line", type="line", pts=[[xs[0], y0], [xs[0], y1]], stroke="ALERT", w=4, keys=keys, anim=True)
    tri = dict(id="cur_head", type="poly", pts=[[xs[0] - 13, y0 - 22], [xs[0] + 13, y0 - 22], [xs[0], y0]],
               fill="ALERT", keys=[dict(k) for k in keys], anim=True)
    return [ln, tri]


def axis(view, steps, span, ticks=(), past=(), lanes=(), start=None, note="", src="", cur_on=True):
    """軸の型。steps＝ナレーションの行ごとの段（上の「SPEC の書き方」）。"""
    if view not in VIEWS:
        raise ValueError(f"axis：知らない見え方 {view!r}（{VIEWS}）")
    if not src:
        raise ValueError("axis：src（出典）を書くこと（図解は出典必須）")
    A = _Ax(view, span, lanes)
    for it in list(past) + [x for st in steps for x in F._many(st.get("add"))]:
        if not it.get("rec"):
            raise ValueError(f"axis：rec（記録の頁）が無い部品 {it}")
        if it["k"] == "link" and (it.get("t") or it.get("chips")):
            raise ValueError("axis：交信 link に文字を書かない（私人の言葉を帯に書かない＝守りの線）")
        if it["k"] == "link" and view != "lanes":
            raise ValueError("axis：交信 link は lanes だけ")
    base, tk = _base(A, ticks, note, src)
    # 札の段は、past と全部の段の点をまとめて振る（段をまたいで重ならない）
    raw = list(past) + [x for st in steps for x in F._many(st.get("add"))]
    prep = {id(it): _prep(A, it) for it in raw}
    rows = _rows([p for p in prep.values() if "at" in p and p["_row"]], A)
    parts = []
    g = list(base)
    for it in past:
        p = prep[id(it)]
        s, r = _draw(A, p, rows.get(id(p), 0), dim=not it.get("keep"))
        g.append(s)
        parts.append(dict(r, stage=-1))
    stages = []
    xs = [A.x0 if not (start or {}).get("cur") else A.x(start["cur"], True)]
    for j, st in enumerate(steps):
        s = []
        for it in F._many(st.get("add")):
            p = prep[id(it)]
            sv, r = _draw(A, p, rows.get(id(p), 0), dim=False)
            s.append(sv)
            parts.append(dict(r, stage=j))
        stages.append("".join(s) or " ")
        xs.append(A.x(st["cur"], True) if st.get("cur") else xs[-1])
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, "年表" if view == "date" else ("交信の帯" if view == "lanes" else "時刻の帯"),
                      400, cap=28, col=J.TICK))
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    anim = _cursor(A, xs) if cur_on else []
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="axis", view=view, span=list(span), ticks=tk, parts=parts, lanes=dict(A.ly),
                  cur=[round(x, 2) for x in xs], cur_on=cur_on, x0=A.x0, x1=A.x1)
    return f
