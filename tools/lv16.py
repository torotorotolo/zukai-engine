# -*- coding: utf-8 -*-
"""lv16.py — 16本目「水位と斜面の速さの線」（2026-10-01 新設・⑤b-5）＝上下2段の線の図（場面1・20カット）。

■ 何か（Vault `Projects/事故検証-16本目-映像方針-絵コンテ-20261001.md` §6「場面1 水位と斜面の速さの線」）
  上の段＝湖の水位（m）・下の段＝斜面の目印が1日に動く距離（ミリ）・横軸は年月で共通（`axis` の暦の読み方＝月は暦の日数）。
  🔴 **記録の点だけを結ぶ**（点と点のあいだは直線でつないだ模式＝S8 の図6 はなぞらない）。線は最初の点の前・最後の点の先へ
     延ばさない。数の記録が無い区間（例＝1963年3月〜9月2日の速さ＝「目立った速まりは無かった」だけ）は線を結ばない（`brk`）。
  台本の画の欄の「再現イラスト 場面1」は**図解として作る**（「再現イラスト」の札は出さない）。人は描かない。

■ SPEC の書き方（14本目 `axis` と同じ「基図＋段の層」。段はナレーションの行ごと＝その行から出て残る）
  fig=("lv", dict(span=("1960-01-01", "1963-11-01"), ticks=("1960", "1961", …), zr=(560, 740), zt=(600, 650, 700),
                  vr=(0, 50), vt=(0, 10, …), rows="zv"|"z", past=[…], steps=[dict(add=[…]), …], rel=[…],
                  note="…模式…", src="…"))
  部品（add と past に書く・前のカットまでに出した物は past＝基図に同じ色で描く）：
    dict(k="pt", s="z"|"v", at="1960-11-04", v=650, rec="S1 p72", t="", off=(dx, dy), anchor="middle")
         … 記録の点。線は同じ段（s）の点を日付の順に隣どうしだけ結ぶ（段の層は、結ぶ2点のうち遅く出た点の段）
    dict(k="brk", s="v", a="1963-03-15", b="1963-09-02", rec="S1 p93")   … この2点のあいだを結ばない（数の記録が無い区間）
    dict(k="ref", s="z", v=700, a=None, b=None, t="700m（模型）", rec="S1 p89", c="DOC", lab="r")
         … 横の線（記録の値）。a／b＝線の始まり・終わりの日（無ければ軸の端まで）
    dict(k="ev", s="both"|"z"|"v", at="1960-11-04", t="崩落", rec="S1 p72", c="ALERT")    … 縦の線（出来事の日）
    dict(k="band", s="both"|"z"|"v", a=…, b=…, t="…", rec=[…], c="TICK")                 … 区間の帯（記録の期間）
    dict(k="ring", s=…, at=…)            … 既に描いた点を囲む（その段までに出た点だけ）
    dict(k="hl", s=…, a=…, b=…)          … 既に描いた線の a〜b を太く重ねる（a・b は点の日）
    dict(k="gap", s="z", at=…, a=580, b=725.5, rec=[…], t="", dx=0)  … 縦の寸法の線（2つの記録の値のあいだ）
  🔴 rec（記録の頁）は pt・brk・ref・ev・band・gap に要る。門番 `check_mech` judge_lv が自分の側の記録の表 `REC_LV*` と照らす
     （§5b-88）。数の札（m・ミリ・センチ）は rel=[dict(t="725.5m", src="S9 p2006")] に同じ文字列（§5b-99）

■ 門番 `check_mech`（judge_lv）＝①点の画素を目盛りの画素で日付と値へ戻し、記録の表の行（日付の窓・値の幅・頁）に入る
  ②線は同じ段の点を日付の順に隣どうしだけ結ぶ（飛ばさない・延ばさない・切ってよいのは表の区間だけ）③横の線・縦の線・帯の値と
  日付も記録の表（715m の許可の線は1963年5月4日より前に引かない）④札の日付は点の日付と合う・札の数は rel
  x・y は全部この関数が組む（`f.mech`）＝描く側と門番が同じ幾何（[[feedback-gates-must-share-the-production-geometry]]）

■ 🔴 2026-10-04（18本目 ⑤b-1・§0b）：16本目の型の道具＝**ファイルとして残す**（この道具は `cuts.ss` を読まない＝ss から16本目の値を
  移しても import で落ちない）。16本目の点の表（`cuts.ss` の LVP・LV_*・VR_* と関数 `lv_fig()`）と、門番 check_mech の記録の表
  （REC_LV・REC_LV_REF・REC_LV_DATE・REC_LV_BRK）は selftest の見本 `tools/fixture_ep16.py` へ移した（値は1つも変えていない＝
  git の `b044b56`）。18本目で線の図を使うときは、点の表を ss に、記録の値を REC_LV＊に回の値で足す
"""
from __future__ import annotations

import axis as A
import jiko_style as J
import titan_fig as F

# 色＝水の線は断面の図（vsec16 の water_ln）と同じ・速さは赤（ALERT＝崩れへ向かう動き）。意味の色は章の色で替わらない
COL = dict(z="#8fc3e4", v=J.ALERT)
NAME = dict(z="湖の水位（m）", v="斜面の目印が1日に動く距離（ミリ）")
X0, X1 = F.BX0 + 150, F.BX1 - 40                       # 横軸（222〜1808）
PANEL = dict(zv=dict(z=(F.BY0 + 58, F.BY0 + 296), v=(F.BY0 + 362, F.BY0 + 576)),
             z=dict(z=(F.BY0 + 58, F.BY0 + 576)))
TICK_Y = F.BY0 + 614          # 目盛りの字（824）
TICK_Y2 = TICK_Y + 30         # 年の段（854）＝左下の出典の行（886）の上
R_PT, W_LN = 9, 5             # 点の半径・線の太さ
KINDS = ("pt", "brk", "ref", "ev", "band", "ring", "hl", "gap")


def _d(s):
    """日付 → 年（小数）。型の読み方＝`axis.val`（月は暦の日数）。🔴 門番は別に自分の読み方を持つ（check_mech._lv_date）。"""
    return A.val("date", s)[0]


def _c(name, dflt):
    nm = name or dflt
    return nm if str(nm).startswith("#") else getattr(J, nm)


class _V:
    """1つのカットの軸（横＝日付・縦＝段ごとの値）。範囲の外の値は描かずに止める（線を枠の外へ延ばさない）。"""

    def __init__(self, span, zr, vr, rows):
        if rows not in PANEL:
            raise ValueError(f"lv：rows は {tuple(PANEL)}（{rows!r}）")
        self.a, self.b = _d(span[0]), _d(span[1])
        if self.b <= self.a:
            raise ValueError(f"lv：span が逆 {span}")
        self.rows = rows
        self.pan = PANEL[rows]
        self.rng = dict(z=tuple(zr), v=tuple(vr or (0, 1)))

    def x(self, s):
        v = _d(s)
        if not (self.a - 1e-9 <= v <= self.b + 1e-9):
            raise ValueError(f"lv：日付 {s} が軸の範囲の外")
        return X0 + (X1 - X0) * (v - self.a) / (self.b - self.a)

    def y(self, s, v):
        if s not in self.pan:
            raise ValueError(f"lv：段 {s!r} はこのカットに無い（rows={self.rows}）")
        top, bot = self.pan[s]
        lo, hi = self.rng[s]
        if not (lo - 1e-9 <= float(v) <= hi + 1e-9):
            raise ValueError(f"lv：値 {v}（{s}）が縦の範囲 {lo}〜{hi} の外＝範囲を広げるか点を外す")
        return bot - (bot - top) * (float(v) - lo) / (hi - lo)

    def panels(self, s):
        return list(self.pan) if s in (None, "both") else [s]


def _tick_lab(s, first):
    """目盛りの字。年（"1960"）＝「1960年」／月（"1963-03"）＝「3月」＋最初と1月だけ年の段。"""
    p = str(s).split("-")
    if len(p) == 1:
        return p[0] + "年", ""
    return f"{int(p[1])}月", (p[0] + "年" if (first or int(p[1]) == 1) else "")


def _base(V, ticks, zt, vt, note, src):
    g, xt, yt = [], [], {s: [] for s in V.pan}
    for s in V.pan:
        top, bot = V.pan[s]
        g.append(F.rect(X0, top, X1 - X0, bot - top, J.BG2, op=0.55))
        for v in (zt if s == "z" else vt):
            y = V.y(s, v)
            g.append(F.line(X0, y, X1, y, J.GRID, 2))
            g.append(F.txt(X0 - 14, y + 9, f"{v:g}", 26, J.TICK, "Noto", "end"))
            yt[s].append(dict(v=float(v), y=round(y, 2)))
        g.append(F.rect(X0, top, X1 - X0, bot - top, "none", J.LINE, 3))
        g.append(F.txtfit(X0, top - 14, NAME[s], 900, cap=28, col=COL[s]))
    ybot = max(b for _t, b in V.pan.values())
    ytop = min(t for t, _b in V.pan.values())
    for i, s in enumerate(ticks):
        x = V.x(s)
        lb, sub = _tick_lab(s, i == 0)
        g.append(F.line(x, ytop, x, ybot, J.GRID, 2, dash="6 8"))
        g.append(F.line(x, ybot, x, ybot + 12, J.LINE, 3))
        g.append(F.txt(x, TICK_Y, lb, 26, J.TICK, "Noto", "middle"))
        if sub:
            g.append(F.txt(x, TICK_Y2, sub, 24, J.TICK, "Noto", "middle"))
        xt.append(dict(at=str(s), x=round(x, 2), lab=lb, sub=sub))
    # 注（模式の断り）は図の右上・左下の行は出典だけ（⚠️ qa_all の layout：cb19 で注＋出典が枠の右の端を16画素越えた）
    g.append(F.txtfit(X1, F.BY0 + 30, note, 760, cap=24, col=J.TICK, anchor="end"))
    if src:
        g.append(F.txtfit(F.BX0, F.BY1 - 6, f"出典：{src}", F.BW, cap=26, col=J.TICK))
    return g, xt, yt


def _label(x, y, t, col, anchor="middle", cap=28):
    return F.txtfit(x, y, t, 520, cap=cap, col=col, anchor=anchor)


def _segs_of(pts, brks):
    """同じ段の点を日付の順に隣どうしだけ結ぶ（brk の区間は結ばない）。pts＝{s: [(段, 部品), …]}（日付の順に並べ替える）。
    🔴 門番の陽性対照がここを壊す（最後の点の先へ延ばす型）＝門番は型の線ではなく点と記録の表で測る"""
    segs = []
    for s, lst in pts.items():
        lst.sort(key=lambda p: _d(p[1]["at"]))
        for (ja, a), (jb, b) in zip(lst, lst[1:]):
            if _d(a["at"]) == _d(b["at"]):
                raise ValueError(f"lv：同じ日に2つの点（{s} {a['at']}）")
            if (s, a["at"], b["at"]) in brks:
                continue
            segs.append(dict(s=s, a=a["at"], b=b["at"], stage=max(ja, jb), pa=a, pb=b))
    return segs


def _ref_span(V, it):
    """横の線の左右の端（a／b＝始まり・終わりの日。無ければ軸の端）。🔴 門番の陽性対照がここを壊す（715m の許可を左の端から引く型）"""
    return (V.x(it["a"]) if it.get("a") else X0), (V.x(it["b"]) if it.get("b") else X1)


def lv(steps, span, zr, vr=None, ticks=(), zt=(), vt=(), rows="zv", past=(), rel=(), note="", src=""):
    """16本目の水位と斜面の速さの線。steps＝ナレーションの行ごとの段（上の「SPEC の書き方」）。"""
    if "模式" not in note:
        raise ValueError("lv：note に「模式」を書くこと（点と点のあいだは直線でつないだ模式＝§5b-10）")
    if not src:
        raise ValueError("lv：src（出典）を書くこと（図解は出典必須）")
    V = _V(span, zr, vr, rows)
    items = [(-1, it) for it in past] + [(j, it) for j, st in enumerate(steps) for it in F._many(st.get("add"))]
    for _j, it in items:
        if it.get("k") not in KINDS:
            raise ValueError(f"lv：知らない部品 {it.get('k')!r}（{KINDS}）")
        if it["k"] in ("pt", "brk", "ref", "ev", "band", "gap") and not it.get("rec"):
            raise ValueError(f"lv：rec（記録の頁）が無い部品 {it}")
    # ── 点と線（同じ段の点を日付の順に隣どうしだけ結ぶ・brk の区間は結ばない）──
    pts = {s: [] for s in ("z", "v")}
    for j, it in items:
        if it["k"] == "pt":
            pts[it["s"]].append((j, it))
    brks = {(it["s"], it["a"], it["b"]) for _j, it in items if it["k"] == "brk"}
    segs = _segs_of(pts, brks)
    seen = {(s, it["at"]): (j, it) for s, lst in pts.items() for j, it in lst}
    for s, a, b in brks:
        if (s, a) not in seen or (s, b) not in seen:
            raise ValueError(f"lv：brk の両端 {a}・{b} が点に無い（{s}）")
    mech = dict(kind="lv", rows=rows, span=list(span), xt=[], yt={}, pts=[], segs=[], refs=[], evs=[], bands=[], rings=[],
                hls=[], gaps=[], brks=[dict(s=s, a=a, b=b) for s, a, b in sorted(brks)], texts=[], rel=list(rel), note=note)
    base, mech["xt"], mech["yt"] = _base(V, ticks, zt, vt, note, src)
    layer = {j: [] for j in range(-1, len(steps))}
    # 線（点の下に描く）。⚠️ 前の段の点へつなぐ線は後の段の層＝前の点の上を通る → 端の点をその層に描き直す
    for sg in segs:
        xa, ya = V.x(sg["a"]), V.y(sg["s"], sg["pa"]["v"])
        xb, yb = V.x(sg["b"]), V.y(sg["s"], sg["pb"]["v"])
        layer[sg["stage"]].append(F.line(xa, ya, xb, yb, COL[sg["s"]], W_LN))
        for (px, py), p in (((xa, ya), sg["pa"]), ((xb, yb), sg["pb"])):
            if (sg["s"], p["at"]) in seen and seen[(sg["s"], p["at"])][0] < sg["stage"]:
                layer[sg["stage"]].append(F.circ(px, py, R_PT, COL[sg["s"]], J.BG, 3))
        mech["segs"].append(dict(s=sg["s"], a=sg["a"], b=sg["b"], xa=round(xa, 2), ya=round(ya, 2), xb=round(xb, 2),
                                 yb=round(yb, 2), stage=sg["stage"]))
    for j, it in items:
        k = it["k"]
        g = layer[j]
        if k == "pt":
            s = it["s"]
            x, y = V.x(it["at"]), V.y(s, it["v"])
            g.append(F.circ(x, y, R_PT, COL[s], J.BG, 3))
            rec = dict(s=s, at=it["at"], v=float(it["v"]), x=round(x, 2), y=round(y, 2), rec=it["rec"], stage=j,
                       t=it.get("t", ""))
            if it.get("t"):
                dx, dy = it.get("off", (0, -22))
                g.append(_label(x + dx, y + dy, it["t"], COL[s], it.get("anchor", "middle")))
                mech["texts"].append(dict(t=it["t"], at=it["at"], k="pt"))
            mech["pts"].append(rec)
        elif k == "ref":
            s = it["s"]
            y = V.y(s, it["v"])
            xa, xb = _ref_span(V, it)
            col = _c(it.get("c"), "DOC")
            g.append(F.line(xa, y, xb, y, col, 3, dash="14 10"))
            if it.get("t"):
                if it.get("lab", "r") == "r":
                    g.append(_label(xb - 8, y - 12, it["t"], col, "end", cap=26))
                else:
                    g.append(_label(xa + 8, y - 12, it["t"], col, "start", cap=26))
                mech["texts"].append(dict(t=it["t"], k="ref"))
            mech["refs"].append(dict(s=s, v=float(it["v"]), y=round(y, 2), xa=round(xa, 2), xb=round(xb, 2), a=it.get("a"),
                                     b=it.get("b"), rec=it["rec"], stage=j, t=it.get("t", "")))
        elif k == "ev":
            x = V.x(it["at"])
            col = _c(it.get("c"), "LINE")
            ps = V.panels(it.get("s"))
            y0 = min(V.pan[p][0] for p in ps)
            y1 = max(V.pan[p][1] for p in ps)
            g.append(F.line(x, y0, x, y1, col, 3, dash="8 8"))
            if it.get("t"):
                right = x > X1 - 260
                # pos＝札を線の上の端（top）か下の端（bot）に。近い2本の縦の線は上下に分ける（c619 の9月26日と10月8日）
                ly = (y1 - 12 if it.get("pos") == "bot" else y0 + 32) + float(it.get("dy", 0))
                g.append(_label(x + (-10 if right else 10), ly, it["t"], col, "end" if right else "start", cap=26))
                mech["texts"].append(dict(t=it["t"], at=it["at"], k="ev"))
            mech["evs"].append(dict(at=it["at"], x=round(x, 2), s=it.get("s", "both"), rec=it["rec"], stage=j, t=it.get("t", "")))
        elif k == "band":
            xa, xb = V.x(it["a"]), V.x(it["b"])
            col = _c(it.get("c"), "TICK")
            for p in V.panels(it.get("s")):
                top, bot = V.pan[p]
                g.append(F.rect(xa, top + 2, xb - xa, bot - top - 4, col, op=0.16))
            if it.get("t"):
                p = V.panels(it.get("s"))[0]
                g.append(F.txtfit((xa + xb) / 2, V.pan[p][0] + 32, it["t"], max(220, xb - xa + 160), cap=26, col=col,
                                  anchor="middle"))
                mech["texts"].append(dict(t=it["t"], k="band"))
            mech["bands"].append(dict(a=it["a"], b=it["b"], xa=round(xa, 2), xb=round(xb, 2), s=it.get("s", "both"),
                                      rec=it["rec"], stage=j, t=it.get("t", "")))
        elif k == "ring":
            key = (it["s"], it["at"])
            if key not in seen or seen[key][0] > j:
                raise ValueError(f"lv：ring {key} は、その段までに描いた点に無い")
            p = seen[key][1]
            x, y = V.x(p["at"]), V.y(p["s"], p["v"])
            g.append(F.circ(x, y, 22, "none", J.AMBER, 4))
            if it.get("t"):
                dx, dy = it.get("off", (0, -36))
                g.append(_label(x + dx, y + dy, it["t"], J.AMBER, it.get("anchor", "middle")))
                mech["texts"].append(dict(t=it["t"], at=p["at"], k="ring"))
            mech["rings"].append(dict(s=p["s"], at=p["at"], x=round(x, 2), y=round(y, 2), stage=j))
        elif k == "hl":
            s = it["s"]
            ks = sorted((sg for sg in segs if sg["s"] == s and _d(it["a"]) <= _d(sg["a"]) and _d(sg["b"]) <= _d(it["b"])),
                        key=lambda q: _d(q["a"]))
            if not ks or ks[0]["a"] != it["a"] or ks[-1]["b"] != it["b"] or any(sg["stage"] > j for sg in ks):
                raise ValueError(f"lv：hl {s} {it['a']}〜{it['b']} は、その段までに描いた線の点の日でない")
            # 線を切った区間（brk）をまたぐときは、つながった区間ごとに重ねる（切れ目を結ばない）
            runs, cur = [], [ks[0]]
            for sg in ks[1:]:
                if sg["a"] == cur[-1]["b"]:
                    cur.append(sg)
                else:
                    runs.append(cur)
                    cur = [sg]
            runs.append(cur)
            for run in runs:
                pl = [(V.x(run[0]["a"]), V.y(s, run[0]["pa"]["v"]))] + [(V.x(sg["b"]), V.y(s, sg["pb"]["v"])) for sg in run]
                g.append(F.poly(pl, "none", J.AMBER, 12, op=0.5))
            mech["hls"].append(dict(s=s, a=it["a"], b=it["b"], stage=j))
        elif k == "gap":
            s = it["s"]
            x = V.x(it["at"]) + float(it.get("dx", 0))
            ya, yb = V.y(s, it["a"]), V.y(s, it["b"])
            g.append(F.line(x, ya, x, yb, J.AMBER, 3))
            g.append(F.arrow(x, (ya + yb) / 2, x, ya, J.AMBER, 3, 14))
            g.append(F.arrow(x, (ya + yb) / 2, x, yb, J.AMBER, 3, 14))
            if it.get("t"):
                g.append(_label(x + 14, (ya + yb) / 2 + 10, it["t"], J.AMBER, "start"))
                mech["texts"].append(dict(t=it["t"], k="gap"))
            mech["gaps"].append(dict(s=s, at=it["at"], x=round(x, 2), ya=round(ya, 2), yb=round(yb, 2), a=float(it["a"]),
                                     b=float(it["b"]), rec=it["rec"], stage=j))
    stages = ["".join(layer[j]) or " " for j in range(len(steps))]
    g = base + layer[-1]
    f = F.Fig("".join(g), stages, "", (X0 - 20, X1 + 20))
    f.moves = []
    f.mech = mech
    return f
