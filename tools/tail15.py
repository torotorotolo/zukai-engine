# -*- coding: utf-8 -*-
"""tail15.py — 15本目「尾翼の板（トリムタブ）の動く模式図」（2026-09-30 新設・15本目 ⑤b-3）。

■ 何か（Vault `Projects/事故検証-15本目-映像方針-絵コンテ-20260926.md` §4 の【尾翼】・§11-2 の使い回し）
  13本目の `latch`／`section`・14本目の `hull` と同じ「基図＋段の鍵で動く部品」の図解（案C の絵ではない）。
  章の色の線と面・左上に見る向き・左下に「模式」と出典（§5b-10）。人は描かない。形と角度は**模式**（板の角度だけ記録の値）。

■ 見え方（view）。🔴 見る向きの札を左上に必ず出す（§5b-80）
  side … 横から見た断面（機首が右＝案C の B・D と同じ向き）：水平尾翼（固定）→ ちょうつがい → 昇降舵 → ちょうつがい → 板。
         板の下の出っ張り（ホーン）と昇降舵を細い棒「リンク」がつなぐ。空気の流れは右から左。
         c302（2行目から）・c514・c321・c322
  plan … 上から見た水平尾翼の左右（機首が上＝画面の左が機体の左）。板は昇降舵の内側の後ろの縁。板ごとに3か所のちょうつがい。
         左の板のリンクは水平尾翼の中の作動器（改造後＝電気）へ・右の板のリンクは**鉄の棒で昇降舵の後ろの桁に固定**（改造後）。
         c303・c512・c513・c719

■ 記録（AAB＝NTSB AAB-12/01。頁は PDF の頁）
  p14「The right elevator trim tab was modified such that it was fixed in place and faired with the right elevator by means of a
       steel rod installed between the elevator rear spar and the link assembly; the stock trim actuator had been removed」
  p15 電気の昇降舵トリム・整備の仲間は「neutral elevator trim (0° left tab deflection)」と思っていた
  p22 3日前のレースの写真で左の板は後ろの縁が上へ 5度・8度（予選とレースも同じ向き＝p40）／p23 限りは後ろの縁が上へ約13度
  p28 0.56秒に左の板は後ろの縁が上へ21度以上（＝リンクが切れている）／p31 板は3か所のちょうつがい・1か所にねじ1本
  p32 左のリンクは曲がって折れた・右のリンクも曲がって折れた（圧縮）／p39 左のリンクは崩れの早い段階で折れていた
  p40「The flutter and failure of the left tab link assembly excited the flutter of the right tab, increasing the dynamic
       compressive loads in the right tab fixed link assembly beyond its buckling strength」
  p42 右の板を固定し、トリムの力は全部左の板へ＝「removing the system's redundancy」／機首下げの大きな調整
  🔴 後ろの縁が上の板＝空気が板を下へ押す＝昇降舵の後ろの縁が下がる＝機首下げ（トリム）。板の力が消えると昇降舵がはね上がり機首が上がる
     （c322 の語り＝AAB p41〜p42 の筋）

■ SPEC の書き方（14本目 `hull` と同じ）
  fig=("tail", dict(view="side"|"plan", start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=… , to=…)), …],
                    rel=[dict(t="8度", src="AAB p22")], note="模式…", src="…"))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。欄と値は FIELDS。札の数（度）は `rel=` に同じ文字列（門番 check_mech ③）

■ 門番 `check_mech`（judge_tail）＝①状態の筋（記録）②本番の関数が置いた部品の画素（`titan_fig.mech_pts`）③札の数
"""
from __future__ import annotations

import math

import jiko_style as J
import titan_fig as F

VIEWS = dict(side=dict(lab="横から見た断面（左の板・模式）"), plan=dict(lab="上から見た水平尾翼（左右・模式）"))
ONOFF = ("off", "on")
FIELDS = dict(
    side=dict(elev=("trim", "down", "up"), tab=("zero", "up", "free"), link=("ok", "broken"), force=ONOFF, nose=ONOFF,
              ghost=ONOFF, hinge=ONOFF),
    plan=dict(mode=("stock", "mod"), lmark=ONOFF, rmark=ONOFF, hinge=ONOFF, llink=("ok", "broken"), rlink=("ok", "broken"),
              shake=("none", "left", "both"), spread=ONOFF, rod=ONOFF, act=ONOFF),
)
START = dict(side=dict(elev="trim", tab="zero", link="ok", force="off", nose="off", ghost="off", hinge="off"),
             plan=dict(mode="mod", lmark="off", rmark="off", hinge="off", llink="ok", rlink="ok", shake="none", spread="off",
                       rod="off", act="off"))

# ── side の置き場（画素・模式）。機首が右＝空気は右から左。角度は画面で時計回りが正（titan_fig.mech_pts と同じ）＝
#    左へ伸びる部品は正で後ろの縁が上がる ──
# 🔴 ⑤b-3 の下見：最初の大きさ（全長 1205画素・厚み ±38画素）は板が細い線にしか見えず、8度と0度の違いも読めなかった
#    ＝横に 1.35倍・縦（厚み）に 2.2倍（模式＝厚みを強めた）・板はさらに太く。点は下の表（ちょうつがいの位置も同じ変換）
Y0 = 540.0
E_H = (1014.0, Y0)                       # 昇降舵のちょうつがい（水平尾翼の後ろ）
T_H = (393.0, Y0)                        # 板のちょうつがい（昇降舵の後ろの縁）
ELEV_DEG = dict(trim=0.0, down=-6.0, up=10.0)     # 昇降舵（模式の角度＝記録に無い）。down＝後ろの縁が下（板の力で押さえる）
#   ⚠️ 下見：up＝14度では限りを越えた板（24度）の先が左上の見え方の名に触れた＝10度（板の先 y≈296）
TAB_DEG = dict(zero=0.0, up=8.0, free=24.0)       # 板（昇降舵に対して）。up＝後ろの縁が上へ 8度（AAB p22 の写真）・
#                                                   free＝限り 約13度（p23）を越える（0.56秒に21度以上＝p28）＝リンクが切れた印
STAB = [(1776.8, 540.0), (1759.2, 502.6), (1716.0, 474.0), (1554.0, 456.4), (1338.0, 467.4), (1135.5, 485.0), (1043.7, 493.8),
        (1043.7, 586.2), (1135.5, 595.0), (1338.0, 612.6), (1554.0, 623.6), (1716.0, 606.0), (1759.2, 577.4)]
ELEV = [(1032.9, 540.0), (1022.1, 507.0), (997.8, 496.0), (798.0, 507.0), (595.5, 520.2), (398.4, 531.2), (398.4, 548.8),
        (595.5, 559.8), (798.0, 573.0), (997.8, 584.0), (1022.1, 573.0)]
E_TE = (5, 6)                            # ELEV の後ろの縁の上と下（門番が角度を測る）
TAB = [(401.0, 528.0), (285.0, 532.0), (150.0, 537.0), (150.0, 543.0), (285.0, 548.0), (401.0, 552.0), (410.0, 606.0),
       (393.0, 610.0)]
T_TE = (2, 3)
HORN = (401.0, 608.0)                    # 板のホーンの先（リンクの後ろの端）＝板と一緒に回る
LINK_E = (609.0, 588.0)                  # リンクの前の端（昇降舵の下＝作動器の棒の先）＝昇降舵と一緒に回る
GAP = 16.0                               # 折れたリンクのすき間（片側）


def _rot(p, c, deg):
    r = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return [c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r)]


def _elev_pt(p, st):
    return _rot(p, E_H, ELEV_DEG[st["elev"]])


def _tab_pt(p, st):
    """板の点：板のちょうつがいのまわりに板の角度 → 昇降舵と一緒に回す。"""
    return _elev_pt(_rot(p, T_H, TAB_DEG[st["tab"]]), st)


def side_points(st):
    """side の部品の点（門番も同じ関数）。"""
    tab = [_tab_pt(p, st) for p in TAB]
    ghost = [_elev_pt(p, st) for p in TAB[:6]]
    a, b = _tab_pt(HORN, st), _elev_pt(LINK_E, st)
    mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    if st["link"] == "broken":
        la = [a, [mid[0] - ux * GAP, mid[1] - uy * GAP + 9.0]]
        lb = [[mid[0] + ux * GAP, mid[1] + uy * GAP - 9.0], b]
    else:
        la, lb = [a, mid], [mid, b]
    tm = _tab_pt((280.0, 540.0), st)
    return dict(elev=[_elev_pt(p, st) for p in ELEV], tab=tab, ghost=ghost, link_a=la, link_b=lb,
                force=[[tm[0], tm[1] - 170.0], [tm[0], tm[1] - 18.0]], th=_elev_pt(T_H, st), tm=tm)


# ── plan の置き場（左の側の画素・右は x→1920−x の鏡）──
CX = 960.0
PSTAB = [(905.0, 330.0), (330.0, 372.0), (300.0, 392.0), (292.0, 560.0), (905.0, 560.0)]
PELEV = [(905.0, 560.0), (292.0, 560.0), (300.0, 640.0), (640.0, 700.0), (905.0, 700.0)]
PTAB = [(640.0, 700.0), (880.0, 700.0), (880.0, 752.0), (646.0, 752.0)]
PHINGE = (668.0, 760.0, 852.0)            # 3か所のちょうつがい（AAB p31）の x（板の前の縁 y=700）
PLINK = ((760.0, 726.0), (760.0, 506.0))  # 板の中ほど → 水平尾翼の中の作動器（左）
PACT = (722.0, 470.0, 76.0, 44.0)         # 作動器の箱（x, y, 幅, 高さ）
PROD = ((760.0, 644.0), (760.0, 604.0))   # 右：鉄の棒（リンクの前の端と昇降舵の後ろの桁をつなぐ）＝鏡で右へ。
#   リンク（板→y644）と重ねない＝折れたリンクのすき間（y669〜701）が棒に隠れない
PSPAR = 604.0                            # 昇降舵の後ろの桁（右の鉄の棒の付け根）＝模式
PSHAKE = [(700.0, 780.0), (730.0, 766.0), (760.0, 780.0), (790.0, 766.0), (820.0, 780.0)]


def _mx(pts):
    return [[2 * CX - x, y] for x, y in pts]


def plan_link(side, broken):
    """リンクの2つの半分（折れたらすき間と少しの曲がり）。side＝"l"／"r"。右は鉄の棒の付け根まで（作動器は外した）。"""
    (x0, y0), (x1, y1) = PLINK
    if side == "r":
        y1 = PROD[0][1]
    mid = (y0 + y1) / 2
    if broken:
        a, b = [[x0, y0], [x0 - 8.0, mid + GAP]], [[x0 + 8.0, mid - GAP], [x1, y1]]
    else:
        a, b = [[x0, y0], [x0, mid]], [[x0, mid], [x1, y1]]
    return (a, b) if side == "l" else (_mx(a), _mx(b))


def _P(ident, typ, pts=None, **kw):
    d = dict(id=ident, type=typ)
    if pts is not None:
        d["pts"] = [list(map(float, p)) for p in pts]
    d.update(kw)
    return d


def _on(v):
    return 1.0 if v else 0.0


def parts_of(view, st):
    """状態 → 部品（id・形・色・濃さ）。🔴 門番（check_mech.judge_tail）もこの関数を呼ぶ＝描く側と同じ幾何。"""
    if view == "side":
        q = side_points(st)
        red = "ALERT" if st["link"] == "broken" else "AMBER"
        return [
            _P("elev", "poly", q["elev"], fill="BG2", stroke="INK_W", w=3),
            # ⚠️ ⑤b-3 の試し焼き：細い線は本番の動く部品で点線にならず（描き手に dash が無い）、札の「点線」と食い違った
            #    ＝灰色の板（塗り）にした（札は「＝灰色の板」）
            _P("ghost", "poly", q["ghost"], fill="TICK", stroke="INK_W", w=1.5, alpha=0.85 if st["ghost"] == "on" else 0.0),
            _P("tab", "poly", q["tab"], fill="AMBER" if st["tab"] != "free" else "ALERT", stroke="INK_W", w=2.5),
            _P("link_a", "line", q["link_a"], stroke=red, w=5),
            _P("link_b", "line", q["link_b"], stroke=red, w=5),
            _P("thinge", "poly", _ring(q["th"], 9.0), fill="BG", stroke="INK_W", w=3),
            _P("hglow", "poly", _ring(q["th"], 22.0), fill=None, stroke="AMBER", w=4, alpha=_on(st["hinge"] == "on")),
            _P("force", "line", q["force"], stroke="AMBER", w=6, head=18, alpha=_on(st["force"] == "on")),
            _P("nose", "line", [[1826.0, 700.0], [1826.0, 420.0]], stroke="ALERT", w=7, head=22, alpha=_on(st["nose"] == "on")),
        ]
    mod = st["mode"] == "mod"
    la, lb = plan_link("l", st["llink"] == "broken")
    ra, rb = plan_link("r", st["rlink"] == "broken")
    x, y, w, h = PACT
    box = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    bolt = [(760.0, 476.0), (748.0, 494.0), (758.0, 494.0), (752.0, 509.0), (770.0, 488.0), (760.0, 488.0), (766.0, 476.0)]
    out = [
        _P("link_la", "line", la, stroke="ALERT" if st["llink"] == "broken" else "INK_W", w=5),
        _P("link_lb", "line", lb, stroke="ALERT" if st["llink"] == "broken" else "INK_W", w=5),
        _P("link_ra", "line", ra, stroke="ALERT" if st["rlink"] == "broken" else "INK_W", w=5),
        _P("link_rb", "line", rb, stroke="ALERT" if st["rlink"] == "broken" else "INK_W", w=5,
           alpha=1.0),
        # 右の板：改造後はリンクの先が鉄の棒で後ろの桁に固定（作動器は外した＝p14）／ふつうの P-51D は作動器まで
        _P("link_rs", "line", _mx([PROD[0], PLINK[1]]), stroke="INK_W", w=5, alpha=_on(not mod)),
        _P("act_l", "poly", box, fill="BG2", stroke="INK_W", w=3),
        _P("act_r", "poly", _mx(box), fill="BG2", stroke="INK_W", w=3, alpha=_on(not mod)),
        _P("bolt", "poly", bolt, fill="AMBER", stroke="AMBER", w=1, alpha=_on(mod)),
        # ⚠️ 下見：章の色の LINE だと第3章（赤銅）で桃色＝折れた印の赤と紛らわしい＝鋼の灰色（章の色に置き換わらない固定の色）
        _P("rod", "line", _mx([PROD[0], PROD[1]]), stroke="#b9c3c9", w=16, alpha=_on(mod)),
        _P("rodhl", "poly", _mx(_ring((PROD[0][0], (PROD[0][1] + PROD[1][1]) / 2), 58.0)), fill=None, stroke="AMBER", w=4,
           alpha=_on(mod and st["rod"] == "on")),
        _P("acthl", "poly", _ring((x + w / 2, y + h / 2), 62.0), fill=None, stroke="AMBER", w=4, alpha=_on(st["act"] == "on")),
        _P("ring_l", "poly", _ellipse(((PTAB[0][0] + PTAB[1][0]) / 2, 726.0), 150.0, 52.0), fill=None, stroke="AMBER", w=4,
           alpha=_on(st["lmark"] == "on")),
        _P("ring_r", "poly", _mx(_ellipse(((PTAB[0][0] + PTAB[1][0]) / 2, 726.0), 150.0, 52.0)), fill=None, stroke="AMBER", w=4,
           alpha=_on(st["rmark"] == "on")),
        _P("shake_l", "line", PSHAKE, stroke="ALERT", w=5, alpha=_on(st["shake"] in ("left", "both"))),
        _P("shake_r", "line", _mx(PSHAKE), stroke="ALERT", w=5, alpha=_on(st["shake"] == "both")),
        _P("spread", "line", [[830.0, 830.0], [1090.0, 830.0]], stroke="ALERT", w=6, head=20, alpha=_on(st["spread"] == "on")),
    ]
    for j, hx in enumerate(PHINGE):
        out.append(_P(f"hg{j}", "poly", _ring((hx, 700.0), 15.0), fill=None, stroke="AMBER", w=4, alpha=_on(st["hinge"] == "on")))
    return out


def _ring(c, r, n=24):
    return [[c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)] for i in range(n)]


def _ellipse(c, rx, ry, n=32):
    return [[c[0] + rx * math.cos(2 * math.pi * i / n), c[1] + ry * math.sin(2 * math.pi * i / n)] for i in range(n)]


def anchors(view, st):
    """札の指し先（段の終わりの状態で）。"""
    if view == "side":
        q = side_points(st)
        te = [(q["tab"][T_TE[0]][0] + q["tab"][T_TE[1]][0]) / 2, (q["tab"][T_TE[0]][1] + q["tab"][T_TE[1]][1]) / 2]
        lm = q["link_a"][1]
        return dict(tab=q["tm"], tab_te=te, elev=_elev_pt((700.0, 512.0), st), stab=(1400.0, 462.0), link=lm, hinge=q["th"],
                    ehinge=E_H, force=q["force"][0], nose=(1826.0, 420.0))
    return dict(ltab=(760.0, 752.0), rtab=(1160.0, 752.0), act=(PACT[0] + PACT[2] / 2, PACT[1]),
                rod=(2 * CX - PROD[0][0], PROD[1][1]), lhinge=(PHINGE[0], 700.0), llink=(760.0, 616.0),
                rlink=(1160.0, 640.0), spread=(1090.0, 830.0))


# 札の置き場（x, y, 揃え, 幅）。動く部品の通り道を避けた（下見で確かめる）。
# 🔴 段の札は**残る**（段の層は足し続ける＝ルール §5b-89）＝1つのカットで同じ置き場に2段の札を置かない・あとで嘘になる札を付けない。
#   side：上の段 top（板がはね上がる道＝x520〜720・y330〜470 より上）・下の3段 b1〜b3（昇降舵の下の空き）・elev・stab・nose
#   plan：上の左右 lt・lt2・rt・rt2（水平尾翼の前の縁より上）・下の左右 l1・r1（左右の板の震えより下・出典の行より上）・act（左の作動器の左）
TAG_AT = dict(
    side=dict(top=(100.0, 300.0, "start", 640.0), b1=(100.0, 744.0, "start", 760.0), b2=(100.0, 794.0, "start", 760.0),
              b3=(100.0, 844.0, "start", 760.0), elev=(780.0, 300.0, "start", 520.0), stab=(1320.0, 300.0, "start", 500.0),
              nose=(1800.0, 844.0, "end", 480.0)),
    plan=dict(lt=(100.0, 290.0, "start", 470.0), lt2=(100.0, 336.0, "start", 470.0), rt=(1820.0, 290.0, "end", 470.0),
              rt2=(1820.0, 336.0, "end", 470.0), l1=(100.0, 822.0, "start", 640.0), r1=(1820.0, 822.0, "end", 640.0),
              act=(700.0, 452.0, "end", 380.0)),
)


def _states(view, start, steps):
    fields = FIELDS[view]
    cur = dict(START[view], **(start or {}))
    out = []
    for st in [dict(state={})] + list(steps):
        cur = dict(cur, **(st.get("state") or {}))
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"tail：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"tail：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    return out[0], out[1:]


def _stage_svgs(view, steps, states, cap=34):
    pre = TAG_AT[view]
    stages, texts = [], []
    for st, stt in zip(steps, states):
        s = []
        an = anchors(view, stt)
        for tg in F._many(st.get("tag")):
            at = tg.get("at", "top")
            x, y, anchor, mw = pre[at] if isinstance(at, str) else (tuple(at) if len(at) == 4 else (at[0], at[1], "start", 420))
            c = tg.get("cap", cap)
            if tg.get("to"):
                tx, ty = an[tg["to"]] if isinstance(tg["to"], str) else tg["to"]
                sy = y - round(c * 0.9) if ty < y - c else y + 8
                sx = x if anchor == "start" else x - (0 if anchor == "end" else 0)
                s.append(F.line(sx, sy, tx, ty, J.AMBER, 2))
            s.append(F.txtfit(x, y, tg["t"], mw, cap=c, col=tg.get("col", J.AMBER), anchor=anchor))
            texts.append(tg["t"])
            if tg.get("d"):
                s.append(F.txtfit(x, y + round(c * 0.95), tg["d"], mw, cap=round(c * 0.62), col=J.TICK, anchor=anchor))
                texts.append(tg["d"])
        stages.append("".join(s) or " ")
    return stages, texts


def _svg_of(sh, key):
    a = key.get("alpha", sh.get("alpha", 1.0))
    a = 1.0 if a is None else float(a)
    if a <= 0.01:
        return ""
    col = lambda nm: None if not nm else (nm if nm.startswith("#") else getattr(J, nm))  # noqa: E731
    fill, stroke = col(key.get("fill", sh.get("fill"))), col(key.get("stroke", sh.get("stroke")))
    q = F.mech_pts(sh, key)
    if sh["type"] == "poly":
        return F.poly(q, fill or "none", stroke, sh.get("w", 3), close=True, op=round(a, 3))
    out = F.poly(q, "none", stroke or fill, sh.get("w", 3), op=round(a, 3))
    if sh.get("head") and len(q) >= 2:
        (x1, y1), (x2, y2) = q[-2], q[-1]
        out += F.arrow(x1, y1, x2, y2, stroke or fill, sh.get("w", 3), sh["head"]).replace("/>", f' opacity="{a:.3f}"/>', 1)
    return out


def _base(view):
    """動かない基図（部品の外の線と名前）。"""
    g = []
    if view == "side":
        g.append(F.poly(STAB, J.BG2, J.INK_W, 3, close=True))
        for yy in (345.0, 760.0):
            g.append(F.arrow(1830.0, yy, 1560.0, yy, J.LINE_DIM, 3, 16))
        g.append(F.txtfit(1830.0, 330.0, "空気の流れ", 260, cap=24, col=J.TICK, anchor="end"))
        g.append(F.circ(E_H[0], E_H[1], 9, J.BG, J.INK_W, 3))
        g.append(F.txtfit(1400.0, 670.0, "水平尾翼（動かない）", 380, cap=28, col=J.TICK, anchor="middle"))
        g.append(F.txtfit(800.0, 660.0, "昇降舵", 240, cap=28, col=J.TICK, anchor="middle"))
    else:
        body = [(912.0, 250.0), (1008.0, 250.0), (996.0, 560.0), (985.0, 880.0), (935.0, 880.0), (924.0, 560.0)]
        g.append(F.poly(body, J.BG2, J.LINE_DIM, 3, close=True))
        for pts in (PSTAB, _mx(PSTAB)):
            g.append(F.poly(pts, J.BG2, J.INK_W, 3, close=True))
        for pts in (PELEV, _mx(PELEV)):
            g.append(F.poly(pts, J.BG, J.INK_W, 3, close=True))
        for pts in (PTAB, _mx(PTAB)):
            g.append(F.poly(pts, J.AMBER, J.INK_W, 2.5, close=True))
        for sgn in (1, -1):
            for hx in PHINGE:
                x = hx if sgn == 1 else 2 * CX - hx
                g.append(F.rect(x - 7, 693, 14, 14, J.INK_W, J.BG, 2))
            xs = (300.0, 905.0) if sgn == 1 else (2 * CX - 905.0, 2 * CX - 300.0)
            g.append(F.line(xs[0] + 20, PSPAR, xs[1] - 20, PSPAR, J.LINE_DIM, 2, dash="8 6"))
        g.append(F.arrow(CX, 318.0, CX, 262.0, J.TICK, 4, 16))
        g.append(F.txtfit(CX + 70, 290.0, "機首の向き", 220, cap=24, col=J.TICK))
        # 左右の名は札に書く（上の左右の札の置き場と重ねない）。部品の名は形の中へ
        for sgn, anc in ((1, "start"), (-1, "end")):
            g.append(F.txtfit(CX - sgn * 630.0, 522.0, "水平尾翼（左）" if sgn == 1 else "水平尾翼（右）", 260, cap=26, col=J.TICK,
                              anchor=anc))
            g.append(F.txtfit(CX - sgn * 630.0, 640.0, "昇降舵", 200, cap=26, col=J.TICK, anchor=anc))
    return g


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def tail(view, steps, start=None, rel=(), note="", src=""):
    """尾翼の板の模式図。view＝"side"｜"plan"。steps＝ナレーションの行ごとの段（上の「SPEC の書き方」）。"""
    if view not in VIEWS:
        raise ValueError(f"tail：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if "模式" not in note:
        raise ValueError("tail：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    start, states = _states(view, start, steps)
    seq = [start] + states
    per = [parts_of(view, st) for st in seq]
    shapes, anim = [], []
    for j, p0 in enumerate(per[0]):
        keys = []
        for i, ps in enumerate(per):
            pj = ps[j]
            kk = {f_: pj[f_] for f_ in KEY_FIELDS if f_ in pj}
            kk.setdefault("alpha", 1.0)
            keys.append(dict(stage=max(0, i - 1), delay=(0.0 if i == 0 else (1.0 if i == 1 else F.MECH_DELAY)), **kk))
        sh = {f_: p0[f_] for f_ in p0 if f_ not in ("alpha",)}
        sh["keys"] = keys
        moving = any({f_: kk.get(f_) for f_ in KEY_FIELDS} != {f_: keys[0].get(f_) for f_ in KEY_FIELDS} for kk in keys[1:])
        sh["anim"] = bool(moving)
        shapes.append(sh)
        if moving:
            anim.append(sh)
    g = _base(view)
    g.append("".join(_svg_of(sh, sh["keys"][0]) for sh in shapes if not sh["anim"]))
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, VIEWS[view]["lab"], 1000, cap=28, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, states)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="tail", view=view, start=start, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(st) for st in steps])
    return f
