# -*- coding: utf-8 -*-
"""boxes.py — 箱の型「流れ図・書類の再現図・並べ図」（2026-09-29 新設・14本目 ⑤b-6）。

■ 何か（Vault `Projects/事故検証-14本目-映像方針-追補-文字の画面-20260926.md` §3 の【流れ】【書類】【並べ】）
  flow … 箱と矢印。裁判の流れ（1審→2審→大法院の列に、役職の箱・罪名の箱・結果の箱）と、仕組みの模式（操舵台→弁→舵）
         🔴 第11章の約束（追補 §7-8・§2 守りの線）＝**役職名だけ**（名前を出さない）・人の影と顔を使わない・
            罪名と刑は箱の中の文字で・赤を使わない（責める形にしない）＝門番 check_boxes が画面の文字を全部照らす
  form … 書類の再現図。🔴 **欄の名は報告書の文にあるものだけ**（無い欄を描かない）・「再現」の札・出典
  row  … 並べ図。🔴 決まっていない原因を**同じ形で横に並べるだけ**（場面にしない・どれかを目立たせない）

■ SPEC の書き方
  fig=("boxes", dict(view="flow", layout=ss.CT, past=[…], steps=[dict(add=[ss.ct("r_captain"), …]), …], note=…, src=…))
    layout … 列（cols）・見出しの箱（heads＝1審・2審・大法院／模式の部品）・席（seats）・列の境の破線（bounds）・行（rows）
    部品：dict(k="role"|"crime"|"res", id=…, t="船長", col="who", row="船長"|rows=(…)|y=…, rec=…)  … 箱（t＝役職・罪名・結果）
          dict(k="edge", fr=id|[ids], to=id|[ids], style="arrow"|"leader", lab="")  … 矢印（複数から1つ＝寄せる・1つから複数＝分ける）
          dict(k="bracket", id=…, over=[ids])・dict(k="grp", t="甲板部", x=…, y=…)・dict(k="seats_on", n=13, rec=…)
          dict(k="mark", at=id, t="？")・dict(k="chip", at=id, t="…", dy=…, rec=…)・dict(k="rule", y=…)
  fig=("boxes", dict(view="form", form=ss.FORM_PRE, steps=[dict(add=[dict(k="end", id="ship"), dict(k="paper"), …])], …))
  🆕 18本目 ⑤b-6a：紙を2〜3枚並べる＝form=[ss.FORM_A, ss.FORM_B]・steps=[dict(add=dict(k="paper", i=0)), dict(add=dict(k="paper", i=1))]
  fig=("boxes", dict(view="row", slots=3, past=[…], steps=[dict(add=[dict(k="item", t="舵の使い方？", rec=…)])], …))
  🔴 rec（記録の頁）は全部の箱に要る。門番 `check_boxes` が自分の側の記録の表と照らす（§5b-88）

■ 門番 `check_boxes`（焼く直前の SVG の `data-q` と、部品のつながり）
  ① 画面の文字が全部、記録の表の言葉（役職・罪名・結果・欄の名・原因の項目）か＝名前が紛れ込まない
  ② 役職→罪名→結果のつながりが記録どおり（刑は役職と組で）③ 席の数＝裁判官の数・全員一致なら全部が灯る
  ④ 書類の欄＝報告書の文にある名だけ・「再現」の札 ⑤ 並べ図の箱は全部同じ大きさと色 ⑥ 赤・人の形を使わない
"""
from __future__ import annotations

import jiko_style as J
import titan_fig as F
from qty import dq, _foot

VIEWS = ("flow", "form", "row")
# 箱の種類 →（枠の色, 字の大きさ, 高さ）
KSTY = dict(head=("INST", 34, 60), role=("LINE", 28, 40), crime=("DOC", 28, 40), res=("INST", 28, 40),
            node=("LINE", 38, 100), chip=("INST", 28, 48))
SEAT, SEAT_GAP = 22, 5         # 13席で 346 画素（大法院の列 360 の内）。18 では「全員一致」の灯りが小さかった（下見）
REPRO = "再現"                # 書類の再現図の札（🔴 門番の陽性対照がここを壊す）
# 🆕 2026-09-30（15本目 ⑤c'）：上の箱から**真下の箱**（x の範囲が重なる）へは縦の矢印。
#    それまでの矢印は「左の箱の右端 → 右の箱の左端」の流れしか描けず、c918 の問い（上）→答え（下）では横の線が
#    問いの字と答えの字の**真ん中を通り**、打ち消し線に見えた（原寸）。門番＝check_boxes ⑨（線分 `segs` と箱）。
#    🔴 門番の陽性対照がここを False にする（縦の矢印を切ると、線が箱の中を通って鳴る）
VERT = True


def _c(name):
    return name if name.startswith("#") else getattr(J, name)


def _box(x0, x1, cy, h, t, kind, dim, q, size=None):
    st, sz, _ = KSTY[kind]
    sz = size or sz
    col = J.LINE_DIM if dim else _c(st)
    ink = J.TICK if dim else J.INK_W
    return (dq(F.rect(x0, cy - h / 2, x1 - x0, h, J.BG2, col, 4, rx=8), f"node|{kind}|{q}")
            + dq(F.txtfit((x0 + x1) / 2, cy + sz * 0.36, t, x1 - x0 - 20, cap=sz, col=ink, anchor="middle"), f"ntext|{kind}|{q}"))


class _Flow:
    def __init__(self, layout):
        self.L = layout
        self.cols = dict(layout.get("cols") or {})
        self.rows = dict(layout.get("rows") or {})
        self.nodes = {}
        for h in layout.get("heads") or []:
            x0, x1 = h.get("x") or self.cols[h["col"]]
            y0, y1 = h.get("y") or layout["head_y"]
            self.nodes[h["id"]] = dict(h, k="head", x0=x0, x1=x1, cy=(y0 + y1) / 2, h=y1 - y0)

    def place(self, p):
        """部品の箱の位置（x0, x1, cy, h）。"""
        if p["k"] not in ("role", "crime", "res"):
            raise ValueError(f"boxes：箱でない部品 {p['k']}")
        col = p.get("col") or {"role": "who", "crime": "crime"}.get(p["k"])
        if p.get("pos"):
            x0, x1 = p["pos"]
        else:
            x0, x1 = self.cols[col]
        if "y" in p:
            cy = p["y"]
        elif "rows" in p:
            ys = [self.rows[r] for r in p["rows"]]
            cy = sum(ys) / len(ys)
        else:
            cy = self.rows[p["row"]]
        return dict(p, col=col, x0=x0, x1=x1, cy=cy, h=KSTY[p["k"]][2])


def _above(a, b):
    """a が b の真上（a の下の辺が b の上の辺より上で、x の範囲が重なる）。"""
    return (a["k"] != "bracket" and b["k"] != "bracket" and a["cy"] + a["h"] / 2 < b["cy"] - b["h"] / 2
            and max(a["x0"], b["x0"]) < min(a["x1"], b["x1"]))


def _edge(fl, p, dim, segs=None):
    """矢印。描いた線分（x1, y1, x2, y2）を `segs` に足す（門番 check_boxes ⑨ が箱と照らす）。"""
    segs = [] if segs is None else segs
    fr = [fl.nodes[i] for i in F._many(p["fr"])] if isinstance(p["fr"], list) else [fl.nodes[p["fr"]]]
    to = [fl.nodes[i] for i in F._many(p["to"])] if isinstance(p["to"], list) else [fl.nodes[p["to"]]]
    col = J.LINE_DIM if dim else J.LINE
    lead = p.get("style") == "leader"
    dash = "4 10" if lead else None
    sw = 3 if lead else 4
    g = []

    def right(n):
        return (n["x1"], n["cy"]) if n["k"] != "bracket" else (n["x"], n["cy"])

    if len(fr) == 1 and len(to) == 1 and to[0]["k"] == "head" and to[0]["cy"] < fr[0]["cy"]:
        (xa, ya), t = right(fr[0]), to[0]
        tx = (t["x0"] + t["x1"]) / 2
        g.append(F.poly([(xa + 4, ya), (tx, ya), (tx, t["cy"] + t["h"] / 2 + 26)], "none", col, sw))
        g.append(F.arrow(tx, t["cy"] + t["h"] / 2 + 30, tx, t["cy"] + t["h"] / 2 + 6, col, sw, 18))
        segs += [(xa + 4, ya, tx, ya), (tx, ya, tx, t["cy"] + t["h"] / 2 + 6)]
    elif VERT and len(fr) == 1 and len(to) == 1 and _above(fr[0], to[0]):
        # 🆕 ⑤c'：真下の箱へは、重なる x の範囲の真ん中に縦の矢印（箱の辺から 6 画素あける）
        a, b = fr[0], to[0]
        x = (max(a["x0"], b["x0"]) + min(a["x1"], b["x1"])) / 2
        y0, y1 = a["cy"] + a["h"] / 2 + 6, b["cy"] - b["h"] / 2 - 6
        g.append(F.line(x, y0, x, y1, col, sw, dash=dash) if lead else F.arrow(x, y0, x, y1, col, sw, 18))
        segs.append((x, y0, x, y1))
    else:
        xa = max(right(n)[0] for n in fr) + 4
        xb = min(n["x0"] for n in to) - 4
        ys = [n["cy"] for n in fr + to]
        if len(fr) == 1 and len(to) == 1 and abs(fr[0]["cy"] - to[0]["cy"]) < 1:
            y = fr[0]["cy"]
            g.append(F.line(xa, y, xb, y, col, sw, dash=dash) if lead else F.arrow(xa, y, xb, y, col, sw, 18))
            segs.append((xa, y, xb, y))
        else:
            xm = p.get("xm") or (xa + xb) / 2
            for n in fr:
                g.append(F.line(right(n)[0] + 4, n["cy"], xm, n["cy"], col, sw, dash=dash))
                segs.append((right(n)[0] + 4, n["cy"], xm, n["cy"]))
            g.append(F.line(xm, min(ys), xm, max(ys), col, sw, dash=dash))
            segs.append((xm, min(ys), xm, max(ys)))
            for n in to:
                g.append(F.line(xm, n["cy"], n["x0"] - 4, n["cy"], col, sw, dash=dash) if lead
                         else F.arrow(xm, n["cy"], n["x0"] - 4, n["cy"], col, sw, 18))
                segs.append((xm, n["cy"], n["x0"] - 4, n["cy"]))
        if p.get("lab"):
            y = fr[0]["cy"] - 26
            g.append(dq(F.txtfit((xa + xb) / 2, y, p["lab"], xb - xa - 16, cap=30, col=J.TICK if dim else J.INK_W,
                                 anchor="middle"), f"elab|{p['lab']}"))
    ids = "・".join(n["id"] for n in fr) + ">" + "・".join(n["id"] for n in to)
    return f'<g data-q="edge|{F.esc(ids)}">' + "".join(g) + "</g>"


def _flow(layout, past, steps, note, src):
    fl = _Flow(layout)
    lab = []
    if layout.get("kind"):
        lab.append(dq(F.txt(F.BX0 + 8, F.BY0 + 34, layout["kind"], 28, J.TICK), "kind"))
    for x in layout.get("bounds") or ():
        y0, y1 = layout["guide_y"]
        lab.append(F.line(x, y0, x, y1, J.LINE_DIM, 2, dash="6 12"))
    heads = layout.get("heads") or []
    for h in heads:
        n = fl.nodes[h["id"]]
        lab.append(_box(n["x0"], n["x1"], n["cy"], n["h"], h["t"], h.get("kind", "head"), False, h["id"]))
    if layout.get("chain"):
        for a, b in zip(heads, heads[1:]):
            na, nb = fl.nodes[a["id"]], fl.nodes[b["id"]]
            lab.append(F.arrow(na["x1"] + 6, na["cy"], nb["x0"] - 6, nb["cy"], J.INST, 4, 18))
    seats = layout.get("seats")
    sx = []
    if seats:
        c0, c1 = fl.cols[seats["col"]]
        wtot = seats["n"] * SEAT + (seats["n"] - 1) * SEAT_GAP
        s0 = (c0 + c1) / 2 - wtot / 2
        sx = [s0 + i * (SEAT + SEAT_GAP) for i in range(seats["n"])]
        for x in sx:
            lab.append(dq(F.rect(x, seats["y"], SEAT, SEAT, "none", J.LINE_DIM, 3, rx=3), "seat"))
        if seats.get("t"):
            lab.append(dq(F.txt(s0 - 14, seats["y"] + SEAT - 1, seats["t"], 26, J.TICK, "Noto", "end"), "seatlab"))
    rec = []

    def draw(p, dim):
        k = p["k"]
        if not p.get("rec") and k in ("role", "crime", "res", "seats_on", "chip"):
            raise ValueError(f"boxes：rec（記録の頁）が無い部品 {p}")
        if k in ("role", "crime", "res"):
            n = fl.place(p)
            fl.nodes[p["id"]] = n
            rec.append(dict(n, dim=dim))
            return _box(n["x0"], n["x1"], n["cy"], n["h"], p["t"], k, dim, p["id"])
        if k == "bracket":
            ns = [fl.nodes[i] for i in p["over"]]
            x = max(n["x1"] for n in ns) + 16
            y0 = min(n["cy"] - n["h"] / 2 for n in ns)
            y1 = max(n["cy"] + n["h"] / 2 for n in ns)
            fl.nodes[p["id"]] = dict(p, k="bracket", x=x, x0=x, x1=x, cy=(y0 + y1) / 2, h=y1 - y0)
            col = J.LINE_DIM if dim else J.LINE
            return F.poly([(x - 12, y0), (x, y0), (x, y1), (x - 12, y1)], "none", col, 4)
        if k == "edge":
            segs = []
            svg = _edge(fl, p, dim, segs)
            rec.append(dict(p, dim=dim, segs=segs))
            return svg
        if k == "grp":
            return dq(F.txt(p["x"], p["y"], p["t"], 30, J.TICK if dim else J.INK_W), f"grp|{p['t']}")
        if k == "seats_on":
            if not seats or p["n"] > len(sx):
                raise ValueError(f"boxes：灯す席 {p['n']} が席の数 {len(sx)} を超える")
            rec.append(dict(p, dim=dim))
            return "".join(dq(F.rect(x, seats["y"], SEAT, SEAT, J.LINE_DIM if dim else J.INST, rx=3), "seat_on")
                           for x in sx[:p["n"]])
        if k == "mark":
            n = fl.nodes[p["at"]]
            return dq(F.txt((n["x0"] + n["x1"]) / 2, n["cy"] - n["h"] / 2 - 18, p["t"], 64, J.TICK if dim else J.AMBER,
                            "Noto", "middle"), f"mark|{p['t']}")
        if k == "chip":
            n = fl.nodes[p["at"]]
            cy = n["cy"] + n["h"] / 2 + p.get("dy", 60)
            w = F.fm.width(p["t"], 28, "Noto") + 40
            cx = (n["x0"] + n["x1"]) / 2
            rec.append(dict(p, dim=dim))
            return (F.line(cx, n["cy"] + n["h"] / 2 + 4, cx, cy - 24, J.LINE_DIM if dim else J.LINE, 3, dash="6 8")
                    + _box(cx - w / 2, cx + w / 2, cy, 48, p["t"], "chip", dim, p.get("id", p["t"])))
        if k == "rule":
            return F.line(F.BX0 + 12, p["y"], F.BX1 - 12, p["y"], J.LINE_DIM, 2, dash="10 10")
        raise ValueError(f"boxes：流れ図に知らない部品 {k!r}")

    for p in past:
        lab.append(draw(p, dim=not p.get("keep")))
    stages = ["".join(draw(p, False) for p in F._many(st.get("add"))) or " " for st in steps]
    lab.append(_foot(note, src))
    f = F.Fig("".join(lab), stages, "", (F.BX0, F.BX1))
    # heads＝見出しの箱の位置（門番 ⑨ が矢印の線分と照らす。部品の箱は parts の role・crime・res）
    f.mech = dict(kind="boxes", view="flow", parts=rec, seats=len(sx),
                  heads=[{k: fl.nodes[h["id"]][k] for k in ("id", "k", "t", "x0", "x1", "cy", "h")} for h in heads])
    return f


# ══════════════════════════════════════════════════════════
#  書類の再現図
# ══════════════════════════════════════════════════════════
FORM_BOX = dict(ship=(110, 430), office=(1430, 1790))
PAPER = (690, 1170, 360, 760)     # x0, x1, y0, y1
FORM_CY = 560
# 🆕 2026-10-04（18本目 ⑤b-6a）：**紙を2〜3枚横に並べる**（`form=[書類1, 書類2, …]`）。c605＝査問会の認定111「氷の下」と、大西洋艦隊の
#    司令官の意見書「開けた海」＝**別の2つの書類**を1枚の紙に混ぜると、無い書類を作ることになる／c112＝認定・意見・勧告の3つの部分。
#    紙は FORM_SPAN の内を FORM_GAP あけて等分（書類ごとに `paper=` を書けばそれを使う）。門番の印は紙ごとに `@番号`
#    （"ftitle@0"・"field@1|場所"…）。段の部品は `dict(k="paper", i=1)`・`dict(k="fill", i=0, f="場所")`（i を省くと 0）。
#    🔴 門番 check_boxes ⑩ が紙どうしの重なり・紙の左右の外れを測る（陽性対照＝FORM_GAP を負にする）
FORM_SPAN = (100, 1820)
FORM_GAP = 60
FORM_Y = (330, 690)               # 並べる紙の上下の既定（欄2つまで。3〜4つは書類ごとに paper=）
# 🆕 2026-09-30（15本目 ⑤b-5）：書類の値（記録の文にある値だけ＝門番 REC_FORM の values）を読める大きさで出すため、
#    form に `paper=(x0, x1, y0, y1)`（紙の大きさ）・`lw=`（欄の名の幅）を持てるようにした（既定は14本目の寸法のまま）。
#    欄に `late=True` を書くと紙には値を出さず、段の部品 `dict(k="fill", f="欄の名")` でその段に値を書き込む
#    （c617＝「はい」に丸が付いていた、を語りと同じ時に出す）。🔴 行き来の箱（ship／office）と紙を重ねない（紙は 470〜1390 の内）


def _form(form, steps, note, src):
    multi = isinstance(form, (list, tuple))      # 🆕 18本目 ⑤b-6a：紙を2〜3枚並べる
    forms = list(form) if multi else [form]
    if multi and not 2 <= len(forms) <= 3:
        raise ValueError(f"boxes：並べる紙は2〜3枚（{len(forms)}枚）")
    for fm in forms:
        if not fm.get("rec") or any(not fd.get("rec") for fd in fm["fields"]):
            raise ValueError("boxes：書類の再現図の title と欄には rec（報告書の頁）が要る")
    if multi:
        if any(fm.get("ends") for fm in forms):
            raise ValueError("boxes：行き来の箱（ends）は紙1枚の書類だけ")
        w = (FORM_SPAN[1] - FORM_SPAN[0] - FORM_GAP * (len(forms) - 1)) / len(forms)
        boxes_ = [fm.get("paper") or (FORM_SPAN[0] + i * (w + FORM_GAP), FORM_SPAN[0] + i * (w + FORM_GAP) + w) + FORM_Y
                  for i, fm in enumerate(forms)]
    else:
        boxes_ = [form.get("paper") or PAPER]
    nodes = {k: dict(id=k, k="end", x0=a, x1=b, cy=FORM_CY, h=96) for k, (a, b) in FORM_BOX.items()}
    x0, x1, y0, y1 = boxes_[0]
    nodes["paper"] = dict(id="paper", k="paper", x0=x0, x1=x1, cy=FORM_CY, h=y1 - y0)
    if not multi and form.get("ends") and (x0 < FORM_BOX["ship"][1] + 40 or x1 > FORM_BOX["office"][0] - 40):
        raise ValueError(f"boxes：紙 {x0}〜{x1} が行き来の箱と重なる（行き来の箱を使う書類の紙は 470〜1390 の内）")
    fyss = []
    for fm, (_, _, b0, b1) in zip(forms, boxes_):
        fys = {fd["t"]: b0 + 180 + 110 * i for i, fd in enumerate(fm["fields"])}
        if fys and max(fys.values()) + 30 > b1:
            raise ValueError(f"boxes：欄 {len(fys)} 個が紙の高さ {b1 - b0} に収まらない")
        fyss.append(fys)
    lab = []
    rec = []

    def tg(q, i):
        """門番の印（紙1枚なら今までどおり・並べるなら紙の番号 @i を名の後ろに）。"""
        if not multi:
            return q
        head, sep, rest = q.partition("|")
        return f"{head}@{i}{sep}{rest}"

    def val(fd, i):
        a0, a1, _, _ = boxes_[i]
        lw = forms[i].get("lw", 190)
        return dq(F.txtfit(a0 + lw + 70, fyss[i][fd["t"]] - 4, fd["v"], a1 - a0 - lw - 110, cap=34, col=J.AMBER),
                  tg(f"fval|{fd['t']}", i))

    def paper(i):
        fm = forms[i]
        a0, a1, b0, b1 = boxes_[i]
        lw = fm.get("lw", 190)                   # 欄の名の幅（値はその右）
        g = [dq(F.rect(a0, b0, a1 - a0, b1 - b0, J.BG2, J.DOC, 4, rx=4), tg("paper", i)),
             dq(F.txtfit((a0 + a1) / 2, b0 + 70, fm["title"], a1 - a0 - 60, cap=38, col=J.INK_W, anchor="middle"),
                tg("ftitle", i)),
             F.line(a0 + 30, b0 + 100, a1 - 30, b0 + 100, J.DOC, 3)]
        for fd in fm["fields"]:
            fy = fyss[i][fd["t"]]
            g.append(dq(F.txtfit(a0 + 40, fy, fd["t"], lw, cap=34, col=J.INK_W), tg(f"field|{fd['t']}", i)))
            g.append(F.line(a0 + lw + 60, fy + 8, a1 - 40, fy + 8, J.DOC, 3))
            if fd.get("v") and not fd.get("late"):
                g.append(val(fd, i))
        # 札「再現」（紙の左上の外）
        w = F.fm.width(REPRO, 28, "Noto") + 32
        g.append(dq(F.rect(a0, b0 - 56, w, 44, J.BG2, J.DOC, 3, rx=6), tg("repro", i)))
        g.append(dq(F.txt(a0 + 16, b0 - 24, REPRO, 28, J.DOC), tg("reprot", i)))
        rec.append(dict(k="paper", i=i, title=fm["title"], rec=fm["rec"], fields=[dict(fd) for fd in fm["fields"]]))
        return "".join(g)

    def draw(p):
        k = p["k"]
        i = p.get("i", 0)
        if k in ("paper", "fill") and not 0 <= i < len(forms):
            raise ValueError(f"boxes：紙の番号 {i} が無い（紙は {len(forms)} 枚）")
        if k == "paper":
            return paper(i)
        if k == "end":
            e = form["ends"][p["id"]]
            if not e.get("rec"):
                raise ValueError(f"boxes：書類の行き来の箱 {p['id']} に rec が要る")
            n = nodes[p["id"]]
            rec.append(dict(k="end", id=p["id"], t=e["t"], rec=e["rec"]))
            return _box(n["x0"], n["x1"], n["cy"], n["h"], e["t"], "role", False, p["id"], size=36)
        if k == "edge":
            a, b = nodes[p["fr"]], nodes[p["to"]]
            return (f'<g data-q="edge|{p["fr"]}>{p["to"]}">'
                    + F.arrow(a["x1"] + 10, FORM_CY, b["x0"] - 10, FORM_CY, J.LINE, 5, 20) + "</g>")
        if k == "fill":          # 🆕 ⑤b-5：late の欄に値を書き込む
            fd = next((f for f in forms[i]["fields"] if f["t"] == p["f"]), None)
            if not fd or not fd.get("v") or not fd.get("late"):
                raise ValueError(f"boxes：fill の欄 {p['f']!r} が late=True の値のある欄でない")
            rec.append(dict(k="fill", i=i, f=fd["t"], rec=fd["rec"]))
            return val(fd, i)
        raise ValueError(f"boxes：書類の再現図に知らない部品 {k!r}")

    stages = ["".join(draw(p) for p in F._many(st.get("add"))) or " " for st in steps]
    lab.append(_foot(note, src))
    f = F.Fig("".join(lab), stages, "", (F.BX0, F.BX1))
    f.mech = dict(kind="boxes", view="form", parts=rec, papers=len(forms))
    return f


# ══════════════════════════════════════════════════════════
#  並べ図
# ══════════════════════════════════════════════════════════
ROW_W, ROW_H, ROW_GAP, ROW_CY = 480, 140, 100, 540


def _row(slots, past, steps, note, src):
    xs = [F.BCX + (i - (slots - 1) / 2) * (ROW_W + ROW_GAP) for i in range(slots)]
    items = list(past) + [p for st in steps for p in F._many(st.get("add"))]
    if len(items) > slots:
        raise ValueError(f"boxes：並べる項目 {len(items)} が枠 {slots} を超える")
    for p in items:
        if p["k"] != "item":
            raise ValueError(f"boxes：並べ図に知らない部品 {p['k']!r}（item だけ＝場面にしない）")
        if not p.get("rec"):
            raise ValueError(f"boxes：rec（記録の頁）が無い項目 {p}")
        if set(p) - {"k", "t", "rec", "keep"}:
            raise ValueError(f"boxes：並べ図の項目は形を変えられない（{sorted(set(p) - {'k', 't', 'rec', 'keep'})}）＝どれかを目立たせない")
    slot = {id(p): i for i, p in enumerate(items)}
    rec = []

    def draw(p, dim):
        x = xs[slot[id(p)]]
        rec.append(dict(p, dim=dim))
        return (dq(F.rect(x - ROW_W / 2, ROW_CY - ROW_H / 2, ROW_W, ROW_H, J.BG2, J.LINE_DIM if dim else J.LINE, 4, rx=12),
                   f"item|{p['t']}")
                + dq(F.txtfit(x, ROW_CY + 17, p["t"], ROW_W - 40, cap=48, col=J.TICK if dim else J.INK_W, anchor="middle"),
                     f"itext|{p['t']}"))

    lab = [draw(p, dim=not p.get("keep")) for p in past]
    stages = ["".join(draw(p, False) for p in F._many(st.get("add"))) or " " for st in steps]
    lab.append(_foot(note, src))
    f = F.Fig("".join(lab), stages, "", (F.BX0, F.BX1))
    f.mech = dict(kind="boxes", view="row", parts=rec, slots=slots)
    return f


def boxes(view, steps, layout=None, past=(), form=None, slots=3, note="", src=""):
    """箱の型。steps＝ナレーションの行ごとの段（上の「SPEC の書き方」）。"""
    if view not in VIEWS:
        raise ValueError(f"boxes：知らない見え方 {view!r}（{VIEWS}）")
    if not src:
        raise ValueError("boxes：src（出典）を書くこと（図解は出典必須）")
    if view == "flow":
        return _flow(layout or {}, past, steps, note, src)
    if view == "form":
        return _form(form, steps, note, src)
    return _row(slots, past, steps, note, src)
