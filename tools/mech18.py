# -*- coding: utf-8 -*-
"""mech18.py — 18本目（スレッシャー号）「仕組みの模式図」（2026-10-04 新設・⑤b-4）。

■ 何か（Vault `Projects/事故検証-18本目-映像方針-絵コンテ-20261001.md` §18）
  16本目の `vsec16` と同じ「基図＋段の層（その行から出て残る）＋動く部品」の図解（案C の絵ではない＝
  「再現イラスト」の札は出さない）。左上に見る向き・左下に「模式」と出典（§5b-10）。人は描かない。
  14〜16本目の型（船の断面・尾翼・地形の断面）では、管・弁・原子炉の回り道が描けない＝新しい型（ルール §5b-113）

■ 見え方（view）と記録（rec。🔴 門番 check_mech の judge_m18 は記録の値を自分の側〈REC_M18〉に持つ＝§5b-88）
  shock  … c206 衝撃試験を**上から**（1962年7月17〜29日・キーウェストの海域・1万ポンドの爆薬を距離を変えて＝認定79・80
            R08 p4194）。🔴 記録に「艦が潜っていたか」が無い＝横から描くと潜航か浮上かを決めてしまう→上から。距離の数は
            次の c207（数の比べ）で出す＝この絵は数を出さない。艦と爆薬の大きさ・距離は模式
  loop   … c404・c719 原子炉と熱を運ぶ水の回り道と主冷却材ポンプ。9:11 に「FAST mode」での働きが止んだ（認定18 R08 p4185）・
            止まったか SLOW に落ちたかは決められない／止まったなら原子炉は自動で止まる（意見45 R08 p4212）＝止まった場合は
            仮定の札。⚠️ 7.1分・非常用の電動機（意見45）は次の c720（時間の帯）の語り＝描かない
  braze  … c602 銀ろう付け＝受け口の溝に**あらかじめ入れた合金の輪**が溶けて、すき間を**左右の2つの面**へ流れる
            （X p1185「preinserted rings of silver brazing alloy」・X p1171「each land」・認定43 R08 p4189）
  ut     … c608 超音波の検査＝継手の**外から**音を当て、付いている所・付いていない所を見る（認定74・103 R08 p4194・p4197）
  crit   … c612 合格の基準＝付いている面の割合 平均40%以上・どちらの面も25%以上（認定103 R08 p4197・X p1171）
  blow   … c702 吹き出しの仕組み＝空気のボンベ4つ（認定51 R08 p4191＝air banks 1〜4）→ 減圧弁（円すい形の網のこし器
            ＝認定49 R08 p4190）→ 主タンク（海水を押し出す）。弁と管とタンクの数・形・位置は模式
  cold   … c707 空気が冷える＝高い圧力の空気が弁を抜けて一気に広がる → 温度が氷点よりずっと下（J p32 ブロケット少将）→
            空気の中の水分がこし器に氷（意見8c R08 p4205）／水分を取る装置は無い（認定48 R08 p4190「Dehydrators were not installed」）
  tinosa … c714 ティノサ（同じ型・造船所で仕上げ中）の岸壁での空気の系統の試験（J p32 の注・認定50 R08 p4191）
  ice    … c716 網の形のこし器に氷 → タンクへの空気が止まる（J p32 の注「ice formed on the screen-type wire strainers …
            cutting off air flow」）。⚠️「網が破れる」（認定50）は c716 の語りに無い＝c715 の決め所で出る＝描かない

■ SPEC の書き方（16本目 `vsec` と同じ）
  fig=("m18", dict(view=…, start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…)), …],
                   rel=[dict(t="40%", src="R08 p4197")], note="…模式…", src="…"))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。札の数・時刻は `rel=` に同じ文字列（門番 check_mech）
"""
from __future__ import annotations

import math

import jiko_style as J
import titan_fig as F

ONOFF = ("off", "on")
VIEWS = dict(shock=dict(lab="上から見た海"), loop=dict(lab="原子炉の水の回り道"),
             braze=dict(lab="継手を縦に切った断面"), ut=dict(lab="継手を縦に切った断面"),
             crit=dict(lab="継手を縦に切った断面（上の半分）"), blow=dict(lab="空気の通り道"),
             # ⚠️ qa_all の dup：「こし器の中」が c716 の見出し「こし器の氷」を8割覆った
             cold=dict(lab="減圧弁の中"), tinosa=dict(lab="横から見た岸壁"), ice=dict(lab="管の中のこし器"))
FIELDS = dict(shock=dict(sub=ONOFF, blast=ONOFF),
              loop=dict(pump=("fast", "quit", "ask", "stop"), reactor=("on", "scram")),
              braze=dict(alloy=("ring", "flow"), heat=ONOFF),
              ut=dict(probe=ONOFF, sound=ONOFF),
              crit=dict(avg=ONOFF, land=ONOFF),
              blow=dict(flow=ONOFF, strainer=ONOFF),
              cold=dict(expand=ONOFF, ice=ONOFF, dry=("none",)),
              tinosa=dict(sys=ONOFF),
              ice=dict(ice=ONOFF, flow=("on", "stop")))
START = {v: {k: vs[0] for k, vs in f.items()} for v, f in FIELDS.items()}
ORDER = dict(alloy=("ring", "flow"), flow=None)      # 戻さない欄（溶けた合金は輪に戻らない）

# ── 意味の色（章の色に置き換わらない直書き＝jiko_style.remap は地と線の7色だけ）──
COL = dict(sea="#1d4660", sea_ln="#5d92b4", water="#5d92b4", water_dk="#2b5f80", water_ln="#8fc3e4",
           hull="#2f3a43", hull_ln="#a9bcc9", metal="#7d8a94", metal2="#a3afb8", edge="#20262d",
           alloy="#eef1f3", hot="#f3a03c", void="#151b20", air="#8fd3e6", ice="#e4f7ff", ice_ln="#9fdcf5",
           core="#e8b33c", core_off="#4b545c", steel="#5c6873", quay="#55606a", ok="#5fbf8f", heat="#f07a3c")

# ══ 型の値（🔴 門番 check_mech は記録の値 REC_M18 を別に持つ＝ここを壊すと門番が鳴る＝陽性対照）══
CRIT_AVG, CRIT_LAND = 0.40, 0.25     # 合格の線（平均・どちらの面も）＝認定103
BANKS_N = 4                          # 空気のボンベの数＝認定51（air banks 1〜4）
FLOW_BOTH = True                     # 溶けた合金が溝の左右の両方の面へ流れる（輪の溝は受け口の真ん中）
ALLOY_PAD = 0.0                      # 合金の帯をすき間より太く描く量（画素・0＝すき間の内だけ）
CONE_APEX = 0.0                      # こし器の先の高さ（底の高さに対する割合・0＝円すいの先は点）
PROBE_GAP = 0.0                      # 超音波の道具の下の端と継手の外の面のすき間（画素・負＝金属の中）

# ── 写し（画素・模式）──
SHOCK = dict(sea=(110.0, 285.0, 1810.0, 850.0), sub=(700.0, 640.0, 600.0), charge=(1400.0, 380.0),
             rings=(60.0, 150.0, 260.0, 390.0, 530.0))
LOOP = dict(v=(250.0, 350.0, 480.0, 800.0), core=(300.0, 470.0, 430.0, 690.0), hot_y=440.0, cold_y=730.0, xr=1440.0,
            pump=(1000.0, 730.0), pr=46.0, chip=(1000.0, 598.0))
JT = dict(ax=600.0, ri=78.0, ro=106.0, rs=122.0, rf=170.0, fx0=230.0, sh=640.0, mo=1250.0, px1=1760.0,
          gx=945.0, gw=40.0, gd=18.0)
JT_HALF = dict(JT, ax=480.0)                       # crit は上の半分だけ（下に割合の棒）
VOIDS = {(0, -1): ((0.22, 0.42),), (1, -1): ((0.30, 0.62),), (0, 1): ((0.66, 0.84),), (1, 1): ((0.72, 0.95),)}
BAR = dict(avg=(160.0, 1760.0, 566.0, 44.0), land=((160.0, 900.0, 726.0, 44.0), (1020.0, 1760.0, 726.0, 44.0)))
BLOW = dict(bx=150.0, bw=64.0, bg=22.0, by0=430.0, by1=770.0, man_y=360.0, vx0=830.0, vx1=970.0, vy=500.0, vh=50.0,
            tank=(1330.0, 420.0, 1740.0, 800.0), w0=452.0, w1=650.0, inset=(900.0, 712.0, 112.0))
TANK_WALL = ((0.0, 0.25), (0.40, 0.66), (0.80, 1.0))       # 主タンクの底の壁（あいだ＝海とつながる口・模式）
TANK_OPEN = (0.325, 0.73)                                   # 口の真ん中（押し出す海水の矢印）
COLD = dict(y=600.0, ih=95.0, wall=20.0, x0=140.0, x1=1780.0, cb=760.0, ca=960.0, th=1010.0, tg=30.0,
            therm=(1660.0, 300.0, 440.0), dry=(300.0, 296.0, 560.0, 392.0))
TIN = dict(water_y=560.0, cx=820.0, cy=585.0, s=1.55, quay=(1560.0, 500.0, 1848.0, 850.0),
           inset=(230.0, 276.0, 790.0, 420.0))
ICEV = dict(y=600.0, ih=110.0, wall=20.0, x0=120.0, x1=1780.0, cb=640.0, ca=1080.0)


def _P(ident, typ, pts=None, **kw):
    d = dict(id=ident, type=typ)
    if pts is not None:
        d["pts"] = [list(map(float, p)) for p in pts]
    d.update(kw)
    return d


def _rect_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _arc_box(c, r, box, a0=0.0, a1=360.0, n=120):
    """円 c・r の弧のうち、箱 box（x0, y0, x1, y1）の中の部分（折れ線のリスト）。"""
    out, cur = [], []
    for j in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * j / n)
        p = (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
        if box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]:
            cur.append(p)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [s for s in out if len(s) > 1]


# ══ shock（c206）＝上から見た海 ══
def sub_top(cx, cy, L):
    """スレッシャー級を上から（艦首が右）。船体の幅の形は横から見た絵（illu._sa_half）と同じ式＝形のもとは同じ写真（模式）。"""
    import illu as IL
    R = L * 0.114 / 2.0
    x0 = cx - L / 2.0
    us = [L * j / 64 for j in range(65)]
    top = [(x0 + u, cy - IL._sa_half(u, L, R)) for u in us]
    bot = [(x0 + u, cy + IL._sa_half(u, L, R)) for u in reversed(us)]
    return top + bot, R


def _shock_sub_svg():
    cx, cy, L = SHOCK["sub"]
    hull, R = sub_top(cx, cy, L)
    x0 = cx - L / 2.0
    g = []
    for sg in (-1.0, 1.0):          # 艦尾の横舵（上から見える十字の舵の横の2枚）
        g.append(F.poly([(x0 + 0.02 * L, cy + sg * 0.2 * R), (x0 + 0.03 * L, cy + sg * 2.0 * R),
                         (x0 + 0.075 * L, cy + sg * 2.0 * R), (x0 + 0.085 * L, cy + sg * 0.4 * R)],
                        COL["hull"], COL["hull_ln"], 2, close=True))
    g.append(F.poly(hull, COL["hull"], COL["hull_ln"], 2.6, close=True))
    sx = x0 + 0.70 * L
    g.append(F.rect(sx - 0.014 * L, cy - 1.45 * R, 0.028 * L, 2.9 * R, COL["hull"], COL["hull_ln"], 2, rx=3))
    g.append(f'<ellipse cx="{sx:.1f}" cy="{cy:.1f}" rx="{0.045 * L:.1f}" ry="{0.38 * R:.1f}" fill="{COL["hull"]}" '
             f'stroke="{COL["hull_ln"]}" stroke-width="2"/>')
    return "".join(g)


def _shock_blast_svg():
    c = SHOCK["charge"]
    box = SHOCK["sea"]
    g = []
    for j, r in enumerate(SHOCK["rings"]):
        op = 0.95 - 0.15 * j
        for seg in _arc_box(c, r, box):
            g.append(F.poly(seg, "none", J.AMBER, 4, op=round(op, 2)))
    for k in range(8):                                   # 爆発の印（光・炎の絵ではなく記号）
        a = math.radians(22.5 + 45 * k)
        g.append(F.line(c[0] + 18 * math.cos(a), c[1] + 18 * math.sin(a), c[0] + 34 * math.cos(a), c[1] + 34 * math.sin(a),
                        J.ALERT, 4))
    g.append(F.circ(c[0], c[1], 13, J.ALERT, "#10161b", 2))
    cx, cy, L = SHOCK["sub"]
    _hull, R = sub_top(cx, cy, L)
    x0 = cx - L / 2.0
    for u in (0.40, 0.56, 0.72):                          # 揺れの印（船体の両わきの短い線）
        x = x0 + u * L
        for sg in (-1.0, 1.0):
            for off in (12.0, 23.0):
                y = cy + sg * (R + off)
                g.append(F.line(x - 18, y, x + 18, y, J.AMBER, 3))
    return "".join(g)


def _shock_base(st):
    x0, y0, x1, y1 = SHOCK["sea"]
    g = [F.rect(x0, y0, x1 - x0, y1 - y0, COL["sea"], None, 0, rx=10, op=0.55)]
    for j in range(9):                                    # 波の印（静かな海＝模式）
        x = x0 + 120 + (j * 197) % (x1 - x0 - 240)
        y = y0 + 60 + (j * 131) % (y1 - y0 - 120)
        g.append(F.poly([(x, y), (x + 14, y - 6), (x + 28, y), (x + 42, y - 6)], "none", COL["sea_ln"], 2, op=0.6))
    if st["sub"] == "on":
        g.append(_shock_sub_svg())
    if st["blast"] == "on":
        g.append(_shock_blast_svg())
    return g


# ══ loop（c404・c719）＝原子炉と熱を運ぶ水の回り道 ══
def loop_path():
    v, xr = LOOP["v"], LOOP["xr"]
    return [(v[2], LOOP["hot_y"]), (xr, LOOP["hot_y"]), (xr, LOOP["cold_y"]), (v[2], LOOP["cold_y"])]


def _chev(p, d, col, s=13.0):
    a = math.atan2(d[1], d[0])
    pts = [(p[0] + s * math.cos(a), p[1] + s * math.sin(a)),
           (p[0] + s * math.cos(a + 2.5), p[1] + s * math.sin(a + 2.5)),
           (p[0] + s * math.cos(a - 2.5), p[1] + s * math.sin(a - 2.5))]
    return F.poly(pts, col, None, 0, close=True)


def _loop_base():
    v = LOOP["v"]
    g = []
    path = loop_path()
    g.append(F.poly(path, "none", COL["water_dk"], 30))
    g.append(F.poly(path, "none", COL["water"], 20))
    for p, d in (((700.0, LOOP["hot_y"]), (1, 0)), ((1180.0, LOOP["hot_y"]), (1, 0)), ((LOOP["xr"], 585.0), (0, 1)),
                 ((1230.0, LOOP["cold_y"]), (-1, 0)), ((700.0, LOOP["cold_y"]), (-1, 0))):
        g.append(_chev(p, d, COL["ice"]))
    g.append(F.rect(v[0], v[1], v[2] - v[0], v[3] - v[1], COL["steel"], COL["hull_ln"], 3, rx=60))
    px, py = LOOP["pump"]
    g.append(F.rect(px - 26, py - 92, 52, 46, COL["metal"], COL["edge"], 2, rx=4))     # 電動機（ポンプの上）
    g.append(F.line(px, py - 46, px, py - 30, COL["edge"], 6))
    g.append(F.txtfit((v[0] + v[2]) / 2, v[1] - 16, "原子炉", 260, cap=32, col=J.INK_W, anchor="middle"))
    g.append(F.txtfit((v[2] + LOOP["xr"]) / 2, LOOP["hot_y"] - 28, "熱を運ぶ水", 360, cap=30, col=J.INK_W,
                      anchor="middle"))
    g.append(F.txtfit(px + LOOP["pr"] + 16, py + LOOP["pr"] + 24, "ポンプ", 200, cap=30, col=J.INK_W))
    return g


def _loop_chip():
    cx, cy = LOOP["chip"]
    return [F.rect(cx - 52, cy - 24, 104, 46, "#24313a", J.AMBER, 2.5, rx=10),
            F.txtfit(cx, cy + 11, "速い", 90, cap=30, col=J.AMBER, anchor="middle")]


def _loop_parts(st):
    """動く部品：炉心（止まると暗く）・ポンプの胴（止まった場合は暗く）・ポンプの回る印（速い回し方のあいだだけ）。"""
    c = LOOP["core"]
    px, py = LOOP["pump"]
    pr = LOOP["pr"]
    out = [_P("core", "poly", _rect_pts(*c), fill=COL["core"] if st["reactor"] == "on" else COL["core_off"],
              stroke=COL["edge"], w=2, alpha=1.0),
           _P("pump", "circle", c=[px, py], r=pr, fill=COL["metal"] if st["pump"] != "stop" else COL["core_off"],
              stroke=COL["edge"], w=3, alpha=1.0),
           # ⚠️ Actions 37185142461（at_c719_095）：止まった印（赤い■）を段の層に描いたら、動く部品のポンプの円が上に描かれて隠れた
           #   ＝印も動く部品（ポンプより後＝上に描く）
           _P("stopmark", "poly", _rect_pts(px - 15, py - 15, px + 15, py + 15), fill=J.ALERT, w=0,
              alpha=1.0 if st["pump"] == "stop" else 0.0)]
    on = 1.0 if st["pump"] == "fast" else 0.0
    for j, sg in enumerate((-1.0, 1.0)):
        a0, a1 = (200.0, 250.0) if sg < 0 else (290.0, 340.0)
        pts = [(px + (pr + 16) * math.cos(math.radians(a0 + (a1 - a0) * k / 8)),
                py + (pr + 16) * math.sin(math.radians(a0 + (a1 - a0) * k / 8))) for k in range(9)]
        out.append(_P(f"spin{j}", "line", pts, stroke=J.AMBER, w=4, head=12, alpha=on))
    return out


def _loop_quit():
    """速い回し方が止んだ印＝札の赤い枠と角の×（⚠️ qa_all の layout：札を描き直すと字が重なり、取り消しの線は字を貫いた）。"""
    cx, cy = LOOP["chip"]
    return [F.rect(cx - 60, cy - 32, 120, 62, "none", J.ALERT, 3.5, rx=13),
            F.circ(cx + 60, cy - 32, 15, J.ALERT, None, 0),
            F.line(cx + 53, cy - 39, cx + 67, cy - 25, "#ffffff", 3.5), F.line(cx + 53, cy - 25, cx + 67, cy - 39, "#ffffff", 3.5)]


def _loop_stage(prev, st):
    g = []
    if prev.get("pump") == "fast" and st["pump"] != "fast":
        g += _loop_quit()
    return g


# ══ braze・ut・crit（c602・c608・c612）＝継手を縦に切った断面 ══
def _jt(view):
    return JT_HALF if view == "crit" else JT


def jt_lands(j=None):
    """2つの面（溝の左と右）の x の範囲＝型の値から。🔴 門番は数（2）と溝との並びを記録（REC_M18）で照らす。"""
    j = j or JT
    return [(j["sh"], j["gx"] - j["gw"] / 2.0), (j["gx"] + j["gw"] / 2.0, j["mo"])]


def _y(j, r, sg):
    return j["ax"] + sg * r


def jt_fit_poly(j, sg):
    """継手（受け口）の壁＝sg −1 上・＋1 下。溝（輪の入る所）は受け口の真ん中。"""
    ax, ri, rs, rf = j["ax"], j["ri"], j["rs"], j["rf"]
    g0, g1 = j["gx"] - j["gw"] / 2.0, j["gx"] + j["gw"] / 2.0
    pts = [(j["fx0"], rf), (j["mo"], rf), (j["mo"], rs), (g1, rs), (g1, rs + j["gd"]), (g0, rs + j["gd"]), (g0, rs),
           (j["sh"], rs), (j["sh"], ri), (j["fx0"], ri)]
    return [(x, ax + sg * r) for x, r in pts]


def jt_pipe_poly(j, sg):
    return [(j["sh"], _y(j, j["ro"], sg)), (j["px1"], _y(j, j["ro"], sg)), (j["px1"], _y(j, j["ri"], sg)),
            (j["sh"], _y(j, j["ri"], sg))]


def jt_ring_poly(j, sg):
    g0, g1 = j["gx"] - j["gw"] / 2.0 + 3.0, j["gx"] + j["gw"] / 2.0 - 3.0
    return [(g0, _y(j, j["rs"], sg)), (g0, _y(j, j["rs"] + j["gd"] - 3.0, sg)), (g1, _y(j, j["rs"] + j["gd"] - 3.0, sg)),
            (g1, _y(j, j["rs"], sg))]


def jt_alloy(j, k, sg, frac):
    """面 k（0 左・1 右）の合金の帯（溝の縁から外へ frac）。y はすき間（受け口の内〜管の外）＋ALLOY_PAD。"""
    (a0, a1) = jt_lands(j)[k]
    L = a1 - a0
    if k == 0:
        x0, x1 = a1 - frac * L, a1
    else:
        x0, x1 = a0, a0 + frac * L
    ya, yb = _y(j, j["rs"] + ALLOY_PAD, sg), _y(j, j["ro"] - ALLOY_PAD, sg)
    return _rect_pts(x0, min(ya, yb), x1, max(ya, yb))


def _jt_icon():
    """右上の小さな外形（継手に管が差しこまれた形）と、縦に切る線＝何の断面かを先に見せる（c602 だけ・模式）。"""
    x0, y0 = 1470.0, 262.0
    g = [F.rect(x0, y0, 170, 96, COL["metal"], COL["edge"], 2, rx=12),
         F.rect(x0 + 170, y0 + 22, 170, 52, COL["metal2"], COL["edge"], 2, rx=6),
         F.line(x0 - 16, y0 + 48, x0 + 356, y0 + 48, J.AMBER, 3, dash="10 7")]
    return g


def _jt_base(view, j, halves=(-1.0, 1.0), part=False):
    g = []
    if len(halves) == 2:                                  # 管の中（空いている所）をうすく塗る＝2本の帯が1本の管に見えるように
        g.append(F.rect(j["fx0"], j["ax"] - j["ri"], j["px1"] - j["fx0"], 2 * j["ri"], "#16303f", None, 0, op=0.7))
    g.append(F.line(j["fx0"] - 20, j["ax"], j["px1"] + 20, j["ax"], J.LINE_DIM, 2, dash="18 10"))   # 中心の線
    for sg in halves:
        g.append(F.poly(jt_pipe_poly(j, sg), COL["metal2"], COL["edge"], 2, close=True))
        g.append(F.poly(jt_fit_poly(j, sg), COL["metal"], COL["edge"], 2, close=True))
        g.append(F.poly(jt_ring_poly(j, sg), COL["alloy"], COL["edge"], 1.5, close=True))
        if part:                                          # 付いている所と付いていない所（並びと長さは模式）
            for k, (a0, a1) in enumerate(jt_lands(j)):
                g.append(F.poly(jt_alloy(j, k, sg, 1.0), COL["alloy"], None, 0, close=True))
                for f0, f1 in VOIDS[(k, int(sg))]:
                    ya, yb = _y(j, j["rs"], sg), _y(j, j["ro"], sg)
                    x0, x1 = a0 + f0 * (a1 - a0), a0 + f1 * (a1 - a0)
                    g.append(F.rect(x0, min(ya, yb), x1 - x0, abs(yb - ya), COL["void"], None, 0))
    top = j["ax"] - j["rf"]
    g.append(F.txtfit((j["fx0"] + j["sh"]) / 2.0, top - 16, "継手", 240, cap=30, col=J.INK_W, anchor="middle"))
    g.append(F.txtfit((j["mo"] + j["px1"]) / 2.0 + 60, j["ax"] - j["ro"] - 18, "管", 120, cap=30, col=J.INK_W,
                      anchor="middle"))
    return g


def jt_probe(j):
    """超音波の道具（外の面の上・型の値 PROBE_GAP）。"""
    x0, x1 = 1040.0, 1120.0
    yb = j["ax"] - j["rf"] - PROBE_GAP
    return (x0, yb - 66.0, x1, yb)


def _ut_stage(prev, st, j):
    g = []
    if st["probe"] == "on" and prev.get("probe") != "on":
        x0, y0, x1, y1 = jt_probe(j)
        g.append(F.line((x0 + x1) / 2, y0, (x0 + x1) / 2, 268.0, COL["metal2"], 4))
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, "#3b4650", COL["hull_ln"], 2.5, rx=6))
    if st["sound"] == "on" and prev.get("sound") != "on":
        x0, y0, x1, y1 = jt_probe(j)
        c = ((x0 + x1) / 2, y1)
        for r in (16.0, 30.0, 44.0, 58.0):
            pts = [(c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a))) for a in range(35, 146, 5)]
            g.append(F.poly(pts, "none", COL["air"], 3))
        for k, (a0, a1) in enumerate(jt_lands(j)):        # 付いている所（緑の縁）・付いていない所（赤い点線）
            for sg in (-1.0, 1.0):
                ya, yb = _y(j, j["rs"], sg), _y(j, j["ro"], sg)
                g.append(F.rect(a0, min(ya, yb) - 3, a1 - a0, abs(yb - ya) + 6, "none", COL["ok"], 2.5))
                for f0, f1 in VOIDS[(k, int(sg))]:
                    x0_, x1_ = a0 + f0 * (a1 - a0), a0 + f1 * (a1 - a0)
                    g.append(F.rect(x0_, min(ya, yb) - 3, x1_ - x0_, abs(yb - ya) + 6, "none", J.ALERT, 3, dash="8 5"))
    return g


def _braze_parts(st, j=None):
    j = j or JT
    fr = {0: (1.0 if FLOW_BOTH else 0.0), 1: 1.0} if st["alloy"] == "flow" else {0: 0.0, 1: 0.0}
    out = []
    for sg in (-1.0, 1.0):
        for k in (0, 1):
            out.append(_P(f"alloy{k}{'t' if sg < 0 else 'b'}", "poly", jt_alloy(j, k, sg, fr[k]),
                          fill=COL["alloy"] if st["alloy"] == "flow" else COL["hot"], w=0, alpha=1.0))
    return out


def _braze_stage(prev, st, j):
    g = []
    if st["heat"] == "on" and prev.get("heat") != "on":
        for sg in (-1.0, 1.0):                            # 熱の印（波の線・炎や道具は描かない）
            y = j["ax"] + sg * (j["rf"] + 26)
            for dx in (-120.0, -40.0, 40.0, 120.0):
                x = j["gx"] + dx
                pts = [(x + 8 * math.sin(k * 0.9), y + sg * 4 * k) for k in range(9)]
                g.append(F.poly(pts, "none", COL["heat"], 4))
    return g


def crit_bars():
    """割合の棒（平均・左の面・右の面）＝(x0, x1, y, h, 合格の線の割合)。"""
    a = BAR["avg"]
    return dict(avg=(a[0], a[1], a[2], a[3], CRIT_AVG),
                lands=[(b[0], b[1], b[2], b[3], CRIT_LAND) for b in BAR["land"]])


def _bar_svg(x0, x1, y, h, frac, lab, col_lab=None):
    g = [F.rect(x0, y, x1 - x0, h, "#1a2229", J.LINE, 2.5, rx=4)]
    xm = x0 + frac * (x1 - x0)
    g.append(F.rect(xm, y, x1 - xm, h, COL["ok"], None, 0, rx=2, op=0.38))
    for k in range(1, 10):
        x = x0 + (x1 - x0) * k / 10.0
        g.append(F.line(x, y + h - 10, x, y + h, J.LINE, 2))
    g.append(F.line(xm, y - 12, xm, y + h + 12, J.AMBER, 6))
    g.append(F.txtfit(x0, y - 14, lab, 520, cap=28, col=col_lab or J.INK_W))
    g.append(F.txtfit(x1, y + h + 34, "合格の範囲", 220, cap=24, col=COL["ok"], anchor="end"))
    return g


def _crit_stage(prev, st, j):
    g = []
    B = crit_bars()
    if st["avg"] == "on" and prev.get("avg") != "on":
        x0, x1, y, h, fr = B["avg"]
        g += _bar_svg(x0, x1, y, h, fr, "付いている面の割合（2つの面の平均）")
    if st["land"] == "on" and prev.get("land") != "on":
        for (x0, x1, y, h, fr), lab in zip(B["lands"], ("左の面", "右の面")):
            g += _bar_svg(x0, x1, y, h, fr, lab)
    return g


def _crit_base(j):
    g = _jt_base("crit", j, halves=(-1.0,), part=True)
    for (a0, a1), lab in zip(jt_lands(j), ("左の面", "右の面")):
        y = j["ax"] - j["ro"]
        g.append(F.line(a0, y + 10, a1, y + 10, J.TICK, 2))
        g.append(F.line(a0, y + 2, a0, y + 18, J.TICK, 2))
        g.append(F.line(a1, y + 2, a1, y + 18, J.TICK, 2))
        g.append(F.txtfit((a0 + a1) / 2.0, y + 58, lab, 220, cap=28, col=J.TICK, anchor="middle"))
    return g


# ══ blow・cold・tinosa・ice（c702・c707・c714・c716）＝空気の系統 ══
def blow_banks():
    B = BLOW
    return [(B["bx"] + k * (B["bw"] + B["bg"]), B["by0"], B["bx"] + k * (B["bw"] + B["bg"]) + B["bw"], B["by1"])
            for k in range(BANKS_N)]


def cone_pts(bx, ax_, cy, h):
    """円すい形の網のこし器（横から）＝底 bx（高さ ±h）→ 先 ax_（高さ ±CONE_APEX·h）。"""
    a = CONE_APEX * h
    return [(bx, cy - h), (ax_, cy - a), (ax_, cy + a), (bx, cy + h)]


def _cone_svg(pts, lw=4.0):
    (bx, y0), (ax_, ya), (_ax2, yb), (_bx2, y1) = pts
    g = [F.poly(pts, "#1f2a31", COL["metal2"], lw, close=True, op=0.9)]
    n = 7
    for k in range(1, n):                                 # 網の目（斜めの線）
        t = k / n
        xa = bx + (ax_ - bx) * t
        ya_ = y0 + (ya - y0) * t
        yb_ = y1 + (yb - y1) * t
        g.append(F.line(xa, ya_, xa, yb_, COL["metal2"], 1.6, op=0.85))
    for k in range(1, 6):
        t = k / 6
        g.append(F.line(bx, y0 + (y1 - y0) * t, ax_, ya + (yb - ya) * t, COL["metal2"], 1.4, op=0.7))
    return g


def _bottle(x0, y0, x1, y1, col=None, ln=None):
    w = x1 - x0
    return (F.rect(x0, y0 + w * 0.35, w, y1 - y0 - w * 0.35, col or COL["steel"], ln or COL["hull_ln"], 2.5, rx=8)
            + f'<ellipse cx="{(x0 + x1) / 2:.1f}" cy="{y0 + w * 0.38:.1f}" rx="{w / 2:.1f}" ry="{w * 0.38:.1f}" '
              f'fill="{col or COL["steel"]}" stroke="{ln or COL["hull_ln"]}" stroke-width="2.5"/>'
            + F.rect((x0 + x1) / 2 - 6, y0 - 4, 12, 10, ln or COL["hull_ln"], None, 0))


def blow_valve():
    B = BLOW
    return (B["vx0"], B["vy"] - B["vh"], B["vx1"], B["vy"] + B["vh"])


def blow_tank():
    return BLOW["tank"]


def _blow_base():
    B = BLOW
    g = []
    for x0, y0, x1, y1 in blow_banks():
        g.append(_bottle(x0, y0, x1, y1))
        g.append(F.line((x0 + x1) / 2, y0 - 4, (x0 + x1) / 2, B["man_y"], COL["metal2"], 6))
    bk = blow_banks()
    xm = 760.0
    g.append(F.poly([((bk[0][0] + bk[0][2]) / 2, B["man_y"]), (xm, B["man_y"]), (xm, B["vy"]), (B["vx0"], B["vy"])],
                    "none", COL["metal2"], 10))
    t = blow_tank()
    g.append(F.line(B["vx1"], B["vy"], t[0], B["vy"], COL["metal2"], 10))
    vx0, vy0, vx1, vy1 = blow_valve()
    g.append(F.rect((vx0 + vx1) / 2 - 22, vy0 - 46, 44, 48, COL["metal"], COL["edge"], 2, rx=4))
    g.append(F.rect(vx0, vy0, vx1 - vx0, vy1 - vy0, COL["metal"], COL["edge"], 2.5, rx=22))
    # 主タンク（下に海とつながる口＝海水を押し出す）。口の数と幅は模式
    g.append(F.poly([(t[0], t[3]), (t[0], t[1]), (t[2], t[1]), (t[2], t[3])], "none", COL["hull_ln"], 4))
    for a, b in TANK_WALL:
        g.append(F.line(t[0] + a * (t[2] - t[0]), t[3], t[0] + b * (t[2] - t[0]), t[3], COL["hull_ln"], 4))
    return g


def _blow_parts(st):
    t = blow_tank()
    lv = BLOW["w1"] if st["flow"] == "on" else BLOW["w0"]
    return [_P("water", "poly", _rect_pts(t[0] + 3, lv, t[2] - 3, t[3] - 3), fill=COL["water"], w=0, alpha=0.85)]


def blow_inset_cone():
    cx, cy, r = BLOW["inset"]
    return cone_pts(cx - 62.0, cx + 62.0, cy, 40.0)


def _blow_stage(prev, st):
    B = BLOW
    g = []
    t = blow_tank()
    if st["flow"] == "on" and prev.get("flow") != "on":
        for p, d in (((560.0, B["man_y"]), (1, 0)), ((760.0, 430.0), (0, 1)), ((1150.0, B["vy"]), (1, 0))):
            g.append(_chev(p, d, COL["air"], 16.0))
        for xf in TANK_OPEN:                               # 押し出される海水（下の口から）
            x = t[0] + xf * (t[2] - t[0])
            g.append(F.arrow(x, t[3] - 6, x, t[3] + 50, COL["water_ln"], 5, 16))
    if st["strainer"] == "on" and prev.get("strainer") != "on":
        cx, cy, r = B["inset"]
        vx0, vy0, vx1, vy1 = blow_valve()
        g.append(F.line(cx, vy1, cx, cy - r, J.TICK, 2.5, dash="6 6"))
        g.append(F.circ(cx, cy, r, "#141c22", J.TICK, 3))
        g.append(F.rect(cx - r + 8, cy - 46, 2 * r - 16, 92, "#0f151a", None, 0))
        g.append(F.line(cx - r + 8, cy - 46, cx + r - 8, cy - 46, COL["metal2"], 5))
        g.append(F.line(cx - r + 8, cy + 46, cx + r - 8, cy + 46, COL["metal2"], 5))
        g += _cone_svg(blow_inset_cone(), 3.0)
        g.append(F.arrow(cx - r + 18, cy, cx - 70, cy, COL["air"], 4, 14))
    return g


def cold_cone():
    C = COLD
    return cone_pts(C["cb"], C["ca"], C["y"], C["ih"])


def _cold_base():
    C = COLD
    y, ih, w = C["y"], C["ih"], C["wall"]
    g = [F.rect(C["x0"], y - ih - w, C["x1"] - C["x0"], w, COL["metal"], COL["edge"], 2),
         F.rect(C["x0"], y + ih, C["x1"] - C["x0"], w, COL["metal"], COL["edge"], 2)]
    th, tg = C["th"], C["tg"]
    for sg in (-1.0, 1.0):                                 # 弁の座（細くなる所）
        g.append(F.poly([(th - 70, y + sg * ih), (th, y + sg * tg), (th + 24, y + sg * tg), (th + 70, y + sg * ih)],
                        COL["metal"], COL["edge"], 2, close=True))
    g += _cone_svg(cold_cone())
    for k in range(13):                                     # 弁の前＝圧力の高い空気（詰まった点）
        for r_ in range(7):
            x = C["x0"] + 40 + k * 46 + (r_ % 2) * 23
            yy = y - ih + 16 + r_ * 26
            if x < C["cb"] - 14:
                g.append(F.circ(x, yy, 4, COL["air"], None, 0))
    g.append(F.txtfit(C["x0"] + 20, y - ih - w - 18, "圧力の高い空気", 340, cap=28, col=COL["air"]))
    return g


def _cold_parts(st):
    x, y0, y1 = COLD["therm"]
    lv = y0 + 22 if st["expand"] == "off" else y1 - 18
    return [_P("merc", "poly", _rect_pts(x - 5, lv, x + 5, y1 + 4),
               fill=J.ALERT if st["expand"] == "off" else "#6fb6ff", w=0, alpha=1.0)]


def cold_ice():
    """氷（こし器の網の上の縁と下の縁に沿う帯の点）＝型の位置。門番は網の形の上にあるかを測る。"""
    (bx, y0), (ax_, ya), (_a2, yb), (_b2, y1) = cold_cone()
    out = []
    for k in range(1, 9):
        t = k / 9
        out.append((bx + (ax_ - bx) * t, y0 + (ya - y0) * t))
        out.append((bx + (ax_ - bx) * t, y1 + (yb - y1) * t))
    return out


def _diamond(x, y, s, col, ln):
    return F.poly([(x, y - s), (x + s * 0.8, y), (x, y + s), (x - s * 0.8, y)], col, ln, 1.5, close=True)


def _cold_stage(prev, st):
    C = COLD
    y, ih = C["y"], C["ih"]
    g = []
    if st["expand"] == "on" and prev.get("expand") != "on":
        for k in range(8):                                  # 弁のあと＝一気に広がった空気（まばらな点）
            for r_ in range(3):
                x = C["th"] + 120 + k * 80 + (r_ % 2) * 40
                yy = y - ih + 30 + r_ * 66
                g.append(F.circ(x, yy, 4, "#6fb6ff", None, 0))
        for a in (-0.32, 0.0, 0.32):                        # 広がる向き
            g.append(F.arrow(C["th"] + 40, y, C["th"] + 40 + 220 * math.cos(a), y + 220 * math.sin(a) * 0.9, "#6fb6ff", 5,
                             16))
        x, y0, y1 = C["therm"]
        g.append(F.rect(x - 11, y0, 22, y1 - y0 + 6, "#1a2229", J.INK_W, 2.5, rx=11))
        g.append(F.circ(x, y1 + 14, 18, "#6fb6ff", J.INK_W, 2.5))
    if st["ice"] == "on" and prev.get("ice") != "on":
        for k in range(10):                                 # 空気の中の水分（小さな粒）
            x = C["x0"] + 70 + k * 58
            yy = y - 50 + (k * 37) % 100
            g.append(F.circ(x, yy, 3, "#bfe6ff", None, 0))
        for x, yy in cold_ice():
            g.append(_diamond(x, yy, 9, COL["ice"], COL["ice_ln"]))
        x0, y0, x1, y1 = C["dry"]
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, "none", J.TICK, 3, rx=8, dash="10 8"))
        g.append(F.txtfit((x0 + x1) / 2, y0 + 58, "水分を取る装置", x1 - x0 - 30, cap=28, col=J.TICK, anchor="middle"))
        g.append(F.line(x0 + 10, y0 + 10, x1 - 10, y1 - 10, J.ALERT, 5))
        g.append(F.line(x0 + 10, y1 - 10, x1 - 10, y0 + 10, J.ALERT, 5))
        g.append(F.line((x0 + x1) / 2, y1, (x0 + x1) / 2, y - ih - COLD["wall"], J.TICK, 2, dash="6 6"))
    return g


def tin_hull():
    """ティノサ（同じ型）の船体の上と下の y（illu の潜水艦の形を TIN["s"] 倍）。"""
    import illu as IL
    R = IL.SA_SUB_R * TIN["s"]
    return (TIN["cy"] - R, TIN["cy"] + R, TIN["cx"] - IL.SA_SUB["L"] * TIN["s"] / 2, TIN["cx"] + IL.SA_SUB["L"] * TIN["s"] / 2)


def _tin_base():
    import illu as IL
    wy = TIN["water_y"]
    qx0, qy0, qx1, qy1 = TIN["quay"]
    g = [F.rect(F.BX0, wy, qx0 - F.BX0, qy1 - wy, COL["sea"], None, 0, op=0.6),
         F.line(F.BX0, wy, qx0, wy, COL["sea_ln"], 3)]
    g.append(f'<g transform="translate({TIN["cx"]:.1f} {TIN["cy"]:.1f}) scale({TIN["s"]:.3f})">'
             f'{IL.sa_sub_svg(0.0, 0.0)}</g>')
    g.append(F.rect(F.BX0, wy, qx0 - F.BX0, 0.55 * (qy1 - wy), COL["sea"], None, 0, op=0.35))   # 水面の下の船体を薄く
    g.append(F.rect(qx0, qy0, qx1 - qx0, qy1 - qy0, COL["quay"], COL["hull_ln"], 2.5))
    top, bot, xl, xr = tin_hull()
    for xs in (xr - 40.0, (xl + xr) / 2 + 80.0):            # 舫い綱（岸壁の杭へ）
        g.append(F.line(xs, top + 4, qx0 + 16, qy0 + 2, J.TICK, 2.5))
    g.append(F.rect(qx0 + 8, qy0 - 14, 16, 16, J.TICK, None, 0))
    return g


def _tin_stage(prev, st):
    g = []
    if st["sys"] == "on" and prev.get("sys") != "on":
        x0, y0, x1, y1 = TIN["inset"]
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, "#141c22", J.TICK, 3, rx=10))
        for k in range(BANKS_N):                             # 小さな空気の系統（ボンベ → 弁 → タンク）
            bx = x0 + 30 + k * 34
            g.append(_bottle(bx, y0 + 64, bx + 24, y1 - 22))
        g.append(F.line(x0 + 42, y0 + 56, x0 + 250, y0 + 56, COL["metal2"], 5))
        g.append(F.line(x0 + 250, y0 + 56, x0 + 250, y0 + 92, COL["metal2"], 5))
        g.append(F.rect(x0 + 226, y0 + 82, 48, 30, COL["metal"], COL["edge"], 2, rx=8))
        g.append(F.line(x0 + 274, y0 + 97, x0 + 380, y0 + 97, COL["metal2"], 5))
        g.append(F.rect(x0 + 380, y0 + 60, 150, y1 - y0 - 82, "none", COL["hull_ln"], 3))
        g.append(F.rect(x0 + 383, y0 + 92, 144, y1 - y0 - 117, COL["water"], None, 0, op=0.85))
        top, bot, xl, xr = tin_hull()
        g.append(F.line((x0 + x1) / 2, y1, (xl + xr) / 2 - 140, top + 6, J.TICK, 2.5, dash="6 6"))
    return g


def ice_cone():
    I = ICEV
    return cone_pts(I["cb"], I["ca"], I["y"], I["ih"])


def _ice_base():
    I = ICEV
    y, ih, w = I["y"], I["ih"], I["wall"]
    g = [F.rect(I["x0"], y - ih - w, I["x1"] - I["x0"], w, COL["metal"], COL["edge"], 2),
         F.rect(I["x0"], y + ih, I["x1"] - I["x0"], w, COL["metal"], COL["edge"], 2),
         F.rect(I["cb"] - 8, y - ih - w - 10, 16, 2 * (ih + w) + 20, COL["metal"], COL["edge"], 2)]
    g += _cone_svg(ice_cone(), 5.0)
    for x in (230.0, 420.0):                                 # 弁の前の空気（流れ込む）
        g.append(F.arrow(x, y, x + 120, y, COL["air"], 6, 20))
    # ⚠️ 下見（10-04）：管の上の右端に置いたら札「空気が止まる」と並んで「空気が止まる主タンクへ」と読めた＝管の下の右端へ
    g.append(F.txtfit(I["x1"] - 10, y + ih + w + 46, "主タンクへ", 260, cap=28, col=J.INK_W, anchor="end"))
    return g


def ice_crust(on):
    """氷の帯（網の上の縁・下の縁・先）＝動く部品の点。"""
    (bx, y0), (ax_, ya), (_a2, yb), (_b2, y1) = ice_cone()
    th = 16.0
    up = [(bx + 30, y0 + 12), (ax_ - 10, ya - 4), (ax_ - 10, ya + th), (bx + 30, y0 + 12 + th * 2.2)]
    dn = [(bx + 30, y1 - 12), (ax_ - 10, yb + 4), (ax_ - 10, yb - th), (bx + 30, y1 - 12 - th * 2.2)]
    # ⚠️ Actions 37185142461（at_c716_095）：先の氷を台形にしたら網と合わせて右向きの白い矢印に見えた（空気が流れると読める）
    #   ＝先は丸い塊（先から右へはみ出さない）
    cx, cy = ax_ - 18.0, (ya + yb) / 2.0
    tip = [(cx + 22.0 * math.cos(2 * math.pi * k / 10), cy + 22.0 * math.sin(2 * math.pi * k / 10)) for k in range(10)]
    return dict(up=up, dn=dn, tip=tip)


def _ice_parts(st):
    I = ICEV
    a = 1.0 if st["ice"] == "on" else 0.0
    out = [_P(f"ice_{k}", "poly", pts, fill=COL["ice"], stroke=COL["ice_ln"], w=2, alpha=a)
           for k, pts in ice_crust(st["ice"] == "on").items()]
    fa = 1.0 if st["flow"] == "on" else 0.0
    for j, x in enumerate((1160.0, 1350.0, 1540.0)):         # 網のあとの空気（止まると消える）
        out.append(_P(f"dn{j}", "line", [(x, I["y"]), (x + 120, I["y"])], stroke=COL["air"], w=6, head=20, alpha=fa))
    return out


def _ice_stage(prev, st):
    g = []
    if st["flow"] == "stop" and prev.get("flow") != "stop":
        x, y = 1560.0, ICEV["y"]
        g.append(F.line(x - 34, y - 34, x + 34, y + 34, J.ALERT, 8))
        g.append(F.line(x - 34, y + 34, x + 34, y - 34, J.ALERT, 8))
    return g


# ══ 共通 ══
def parts_of(view, st):
    """状態 → 動く部品。🔴 門番（check_mech.judge_m18）もこの関数を呼ぶ＝描く側と同じ幾何。"""
    if view == "loop":
        return _loop_parts(st)
    if view == "braze":
        return _braze_parts(st)
    if view == "blow":
        return _blow_parts(st)
    if view == "cold":
        return _cold_parts(st)
    if view == "ice":
        return _ice_parts(st)
    return []


def anchors(view, st):
    """札の指し先（段の終わりの状態で）。"""
    if view == "shock":
        cx, cy, L = SHOCK["sub"]
        return dict(charge=SHOCK["charge"], sub=(cx, cy))
    if view == "loop":
        v, c = LOOP["v"], LOOP["core"]
        px, py = LOOP["pump"]
        cx, cy = LOOP["chip"]
        return dict(pump=(px, py - LOOP["pr"] - 50), pumpr=(px + LOOP["pr"], py - 18), core=((c[0] + c[2]) / 2, (c[1] + c[3]) / 2),
                    chip=LOOP["chip"], chipl=(cx - 54, cy), chipr=(cx + 54, cy))
    if view in ("braze", "ut", "crit"):
        j = _jt(view)
        (l0, l1), (r0, r1) = jt_lands(j)
        ym = j["ax"] - (j["rs"] + j["ro"]) / 2.0
        yb = j["ax"] + (j["rs"] + j["ro"]) / 2.0            # 下の半分のすき間（札は下に置く＝線が継手の金属を横切らない）
        vx0, vx1 = VOIDS[(1, 1)][0]
        return dict(ring=(j["gx"], j["ax"] - j["rs"] - j["gd"] / 2.0), land=((r0 + r1) / 2.0, yb),
                    lland=((l0 + l1) / 2.0, yb), bond=(l0 + 0.30 * (l1 - l0), yb),
                    void=(r0 + 0.5 * (vx0 + vx1) * (r1 - r0), yb), top=((r0 + r1) / 2.0, ym),
                    probe=((jt_probe(j)[0] + jt_probe(j)[2]) / 2, jt_probe(j)[1]))
    if view == "blow":
        bk = blow_banks()
        v = blow_valve()
        t = blow_tank()
        cx, cy, r = BLOW["inset"]
        return dict(banks=((bk[0][0] + bk[-1][2]) / 2, bk[0][1]), valve=((v[0] + v[2]) / 2, v[1] - 50), tank=((t[0] + t[2]) / 2, t[1]),
                    inset=(cx - r, cy))
    if view == "cold":
        x, y0, y1 = COLD["therm"]
        (bx, ya), (ax_, _y) = cold_cone()[:2]
        return dict(therm=(x - 14, (y0 + y1) / 2), ice=((bx + ax_) / 2, ya + (_y - ya) / 2 - 6),
                    out=(COLD["th"] + 160, COLD["y"] - 40), dry=((COLD["dry"][0] + COLD["dry"][2]) / 2, COLD["dry"][1]))
    if view == "tinosa":
        top, bot, xl, xr = tin_hull()
        return dict(sub=((xl + xr) / 2, top - 90), quay=((TIN["quay"][0] + TIN["quay"][2]) / 2, TIN["quay"][1]))
    if view == "ice":
        (bx, y0), (ax_, ya) = ice_cone()[:2]
        (_a2, yb), (_b2, y1) = ice_cone()[2:]
        return dict(ice=((bx + ax_) / 2, y0 + (ya - y0) / 2 + 8), mesh=((bx + ax_) / 2 + 40, y1 + (yb - y1) * 0.55),
                    stop=(1560.0, ICEV["y"] - 40))
    return {}


# 札の置き場（x, y, 揃え, 幅）。🔴 段の札は残る（段の層は足し続ける＝ルール §5b-89）＝同じ置き場に2段の札を置かない
#   🔴 18本目 ⑤c'（字と線の重なり＝check_layout は字より前に描いた線を見ない）：
#     shock.charge (1440, 336) は爆発の輪（半径60）が「爆薬」の字の箱を通った（c206）→ 輪60と150のあいだ・爆薬の右（すき間 約10px）
#     braze.ring (1010, 364) は熱の印（く）の上端と字の下端が 4.9px（c602）→ 輪の真上（引き出し線は熱の印 985 と 905 のあいだを真下へ）
TAG_AT = dict(
    shock=dict(sub=(700.0, 760.0, "middle", 420.0), shake=(700.0, 820.0, "middle", 520.0), charge=(1470.0, 393.0, "start", 330.0)),
    loop=dict(clock=(1800.0, 304.0, "end", 260.0), fast=(965.0, 528.0, "middle", 380.0), q1=(700.0, 612.0, "middle", 280.0),
              q2=(1250.0, 612.0, "middle", 300.0), q3=(700.0, 806.0, "middle", 400.0), r1=(1800.0, 380.0, "end", 330.0),
              core=(560.0, 650.0, "start", 300.0)),
    braze=dict(ring=(945.0, 340.0, "middle", 420.0), flow=(1300.0, 820.0, "start", 460.0)),
    # ⚠️ 下見（10-04）：2つの札を右下に並べたら「付いている所 付いていない所」と1つの言葉に読めた＝左の面と右の面に分ける
    ut=dict(probe=(1160.0, 330.0, "start", 360.0), bond=(700.0, 822.0, "middle", 300.0), void=(1500.0, 822.0, "middle", 320.0)),
    crit=dict(avg=(800.0, 540.0, "middle", 260.0), l1=(345.0, 700.0, "middle", 200.0), l2=(1205.0, 700.0, "middle", 200.0)),
    blow=dict(banks=(150.0, 320.0, "start", 420.0), valve=(900.0, 386.0, "middle", 220.0), tank=(1535.0, 400.0, "middle", 300.0),
              strainer=(775.0, 702.0, "end", 290.0)),
    cold=dict(out=(1300.0, 452.0, "middle", 300.0), therm=(1620.0, 330.0, "end", 360.0), ice=(860.0, 452.0, "middle", 120.0),
              dry=(580.0, 352.0, "start", 140.0)),
    tinosa=dict(when=(1800.0, 304.0, "end", 300.0), sub=(1060.0, 450.0, "start", 300.0), quay=(1704.0, 470.0, "middle", 276.0),
                sys=(250.0, 316.0, "start", 300.0)),
    ice=dict(ice=(860.0, 446.0, "middle", 120.0), stop=(1560.0, 452.0, "middle", 300.0), doc=(120.0, 330.0, "start", 420.0),
             mesh=(860.0, 790.0, "middle", 160.0)),
)


def _states(view, start, steps):
    fields = FIELDS[view]
    cur = dict(START[view], **(start or {}))
    out = []
    for st in [dict(state={})] + list(steps):
        cur = dict(cur, **(st.get("state") or {}))
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m18：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m18：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    for f_, seq in ORDER.items():
        if seq and f_ in FIELDS[view]:
            idx = [seq.index(s[f_]) for s in out]
            if any(b < a for a, b in zip(idx, idx[1:])):
                raise ValueError(f"m18：{f_} は戻さない（{' → '.join(seq)}）")
    return out[0], out[1:]


def stage_art(view, prev, st):
    """段で新しく出る動かない絵（前の段との差）。"""
    if view == "shock":
        g = []
        if st["sub"] == "on" and prev.get("sub") != "on":
            g.append(_shock_sub_svg())
        if st["blast"] == "on" and prev.get("blast") != "on":
            g.append(_shock_blast_svg())
        return g
    if view == "loop":
        return _loop_stage(prev, st)
    if view == "braze":
        return _braze_stage(prev, st, JT)
    if view == "ut":
        return _ut_stage(prev, st, JT)
    if view == "crit":
        return _crit_stage(prev, st, JT_HALF)
    if view == "blow":
        return _blow_stage(prev, st)
    if view == "cold":
        return _cold_stage(prev, st)
    if view == "tinosa":
        return _tin_stage(prev, st)
    if view == "ice":
        return _ice_stage(prev, st)
    return []


def _base(view, start):
    """動かない基図（頭の状態で出ている絵も＝段の層は差だけ）。"""
    st = dict(START[view], **(start or {}))
    if view == "shock":
        g = _shock_base(START["shock"])
    elif view == "loop":
        g = _loop_base() + _loop_chip()
    elif view == "braze":
        g = _jt_base(view, JT) + _jt_icon()
    elif view == "ut":
        g = _jt_base(view, JT, part=True)
    elif view == "crit":
        g = _crit_base(JT_HALF)
    elif view == "blow":
        g = _blow_base()
    elif view == "cold":
        g = _cold_base()
    elif view == "tinosa":
        g = _tin_base()
    else:
        g = _ice_base()
    g += stage_art(view, START[view], st)
    return g


def geo_of(view, start, states):
    """門番が測る形（画面の点）。🔴 描く関数と同じ式（§5b-88＝門番は記録を自分の側に持つ）。"""
    allst = [start] + list(states)
    out = dict(view=view)
    if view == "shock":
        cx, cy, L = SHOCK["sub"]
        hull, R = sub_top(cx, cy, L)
        out.update(hull=[list(p) for p in hull], charge=list(SHOCK["charge"]),
                   obj=dict(sub=1 if any(s["sub"] == "on" for s in allst) else 0,
                            charge=1 if any(s["blast"] == "on" for s in allst) else 0))
    elif view == "loop":
        out.update(path=[list(p) for p in loop_path()], pump=list(LOOP["pump"]), pr=LOOP["pr"], vessel=list(LOOP["v"]))
    elif view in ("braze", "ut", "crit"):
        j = _jt(view)
        out.update(lands=[list(l_) for l_ in jt_lands(j)], groove=[j["gx"] - j["gw"] / 2.0, j["gx"] + j["gw"] / 2.0],
                   socket=[j["sh"], j["mo"]], gap=[j["ax"] - j["rs"], j["ax"] - j["ro"]], ax=j["ax"],
                   outer=j["ax"] - j["rf"])
        if view == "braze":
            last = parts_of("braze", allst[-1])
            out["alloy"] = [p["pts"] for p in last]
        if view == "ut" and any(s["probe"] == "on" for s in allst):
            out["probe"] = list(jt_probe(j))
        if view == "crit":
            B = crit_bars()
            out["bars"] = dict(avg=list(B["avg"]) if any(s["avg"] == "on" for s in allst) else None,
                               lands=[list(b) for b in B["lands"]] if any(s["land"] == "on" for s in allst) else [])
    elif view == "blow":
        out.update(banks=[list(b) for b in blow_banks()], valve=list(blow_valve()), tank=list(blow_tank()),
                   water=[parts_of("blow", s)[0]["pts"][0][1] for s in allst])
        if any(s["strainer"] == "on" for s in allst):
            out["cone"] = [list(p) for p in blow_inset_cone()]
    elif view == "cold":
        out.update(cone=[list(p) for p in cold_cone()], dry=[s["dry"] for s in allst],
                   merc=[parts_of("cold", s)[0]["pts"][0][1] for s in allst])
        if any(s["ice"] == "on" for s in allst):
            out["ice"] = [list(p) for p in cold_ice()]
    elif view == "tinosa":
        top, bot, xl, xr = tin_hull()
        out.update(hull=[top, bot, xl, xr], water_y=TIN["water_y"], quay=list(TIN["quay"]))
    elif view == "ice":
        out.update(cone=[list(p) for p in ice_cone()])
        last = parts_of("ice", allst[-1])
        out["ice"] = [p["pts"] for p in last if p["id"].startswith("ice_") and p["alpha"] > 0.5]
        out["down"] = [p["alpha"] for p in last if p["id"].startswith("dn")]
    return out


def _stage_svgs(view, steps, start, states, cap=34):
    pre = TAG_AT[view]
    stages, texts = [], []
    prev = start
    for st, stt in zip(steps, states):
        s = stage_art(view, prev, stt)
        an = anchors(view, stt)
        for tg in F._many(st.get("tag")):
            at = tg.get("at", next(iter(pre)))
            x, y, anchor, mw = pre[at] if isinstance(at, str) else (tuple(at) if len(at) == 4 else (at[0], at[1], "start", 420))
            c = tg.get("cap", cap)
            if tg.get("to"):
                tx, ty = an[tg["to"]] if isinstance(tg["to"], str) else tg["to"]
                sy = y - round(c * 0.9) if ty < y - c else y + 8
                s.append(F.line(x, sy, tx, ty, J.AMBER, 2))
            s.append(F.txtfit(x, y, tg["t"], mw, cap=c, col=tg.get("col", J.AMBER), anchor=anchor))
            texts.append(tg["t"])
            if tg.get("d"):
                s.append(F.txtfit(x, y + round(c * 0.95), tg["d"], mw, cap=round(c * 0.62), col=J.TICK, anchor=anchor))
                texts.append(tg["d"])
        stages.append("".join(s) or " ")
        prev = stt
    return stages, texts


def _static_part(sh):
    a = float(sh["keys"][0].get("alpha", 1.0))
    if a <= 0.01:
        return ""
    if sh["type"] == "circle":
        return F.circ(sh["c"][0], sh["c"][1], sh["r"], sh.get("fill", "none"), sh.get("stroke"), sh.get("w"))
    pts = F.mech_pts(sh, sh["keys"][0])
    if sh["type"] == "poly":
        return F.poly(pts, sh.get("fill", "none"), sh.get("stroke"), sh.get("w") or None, close=True,
                      op=(round(a, 2) if a < 0.99 else None))
    out = F.poly(pts, "none", sh.get("stroke"), sh.get("w"), op=(round(a, 2) if a < 0.99 else None))
    if sh.get("head"):
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        out += F.arrow(x1, y1, x2, y2, sh.get("stroke"), sh.get("w"), sh["head"])
    return out


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def m18(view, steps, start=None, rel=(), note="", src=""):
    """18本目の仕組みの模式図。view＝shock｜loop｜braze｜ut｜crit｜blow｜cold｜tinosa｜ice。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m18：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if "模式" not in note:
        raise ValueError("m18：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    seq = [st0] + states
    per = [parts_of(view, s) for s in seq]
    shapes, anim = [], []
    for j, p0 in enumerate(per[0]):
        keys = []
        for i, ps in enumerate(per):
            pj = ps[j]
            kk = {f_: pj[f_] for f_ in KEY_FIELDS if f_ in pj}
            kk.setdefault("alpha", 1.0)
            dl = 0.0 if i == 0 else float(steps[i - 1].get("delay", 1.0 if i == 1 else F.MECH_DELAY))
            keys.append(dict(stage=max(0, i - 1), delay=dl, **kk))
        sh = {f_: p0[f_] for f_ in p0 if f_ not in ("alpha", "dx", "dy")}
        sh["keys"] = keys
        moving = any({f_: kk.get(f_) for f_ in KEY_FIELDS} != {f_: keys[0].get(f_) for f_ in KEY_FIELDS} for kk in keys[1:])
        sh["anim"] = bool(moving)
        shapes.append(sh)
        if moving:
            anim.append(sh)
    g = _base(view, start or {})
    for sh in shapes:
        if not sh["anim"]:
            g.append(_static_part(sh))
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, VIEWS[view]["lab"] + "・模式", 1000, cap=28, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, st0, states)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="m18", view=view, start=st0, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states))
    return f
