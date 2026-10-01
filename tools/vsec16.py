# -*- coding: utf-8 -*-
"""vsec16.py — 16本目「断面の図解」（2026-10-01 新設・⑤b-4）＝ダムの断面と、南の岸の斜面を南北に切った断面の模式図。

■ 何か（Vault `Projects/事故検証-16本目-映像方針-絵コンテ-20261001.md` §6「断面の図解」・§4-2 #4）
  14本目の `hull`・15本目の `tail` と同じ「基図＋段の層（その行から出て残る）＋動く部品」の図解（案C の絵ではない＝
  「再現イラスト」の札は出さない）。左上に見る向き・左下に「模式」と出典（§5b-10）。人は描かない。
  🔴 地形の線は案C の VB（谷を横切る断面）と**同じ線**（`illu.VB_G`・すべり面の模式 `illu.VB_SLIP`）＝向きがそろう（左が南）。
     ダムの断面は VC と同じ形（`illu.vc_dam_um`・谷の底 `illu.vc_bed`）＝左が上流（湖）・右が下流。縦横同じ縮尺

■ 見え方（view）
  dam   … c211 ダムの断面（S9 PDF6＝高さ261.60m・天端725.50m・厚さ 底22.11m・上3.40m）。湖は最も高い水位 722.50m（S1 PDF63）
          まで（数は出さない）。反りは模式。1行目＝底の厚さ・2行目＝上の厚さ・3行目＝水の力（矢印・長さは模式）
  marks … c302 斜面の目印（S1 PDF148＝1960年5月から目印を毎日測った）。目印の数（4）と位置・ずれの大きさは模式
  two   … c403 2人の見立て（大昔に滑り落ちてきた岩の塊・その下のすべり面＝S1 PDF73・PDF174）。形は模式（VB_SLIP）
  pair  … c404 2人の見立て（左）と反対の見方（右＝岩は元の場所にある・上から崩れてきた塊ではない＝S1 PDF74・PDF174）
  probe … c405 人工の揺れで調べた線（調べた線の上では、厚い自前の岩の土台の上に10〜20mの崩れた土＝S1 PDF74・PDF174）と、
          試しの穴（1959〜60年の試し掘り3本・1961年に沢の近くで掘った横穴2本＝すべり面は見つからなかった＝S1 PDF148・PDF174）。
          位置と深さは模式・数は記録
  model … c504 水理模型とは（本物の谷を小さくした谷に水を張る・200分の1＝S1 PDF89）。大きさの比は模式（200分の1 は描けない）
  seep  … c618 湖の水位 702.50m（1963年10月8日・1日1m ずつ下げた＝S1 PDF96）・斜面にしみこんだ水（中の水の高さは模式）・
          急に下げると斜面を押しうる（S1 PDF79）

■ SPEC の書き方（15本目 `tail` と同じ）
  fig=("vsec", dict(view=…, start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…)), …],
                    rel=[dict(t="約22m", src="S9 p2006")], note="…模式…", src="…"))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。札の数（m・本・分の1）は `rel=` に同じ文字列（門番 check_mech）

■ 門番 `check_mech`（judge_vsec）＝①状態の筋 ②本番の関数が置いた形（`f.mech["geo"]` の画素を写しの目盛りで読む＝ダムの寸法・
  水位・土の厚さ・穴の数）③札の数（rel）。🔴 記録の値は門番の側に持つ（§5b-88）
"""
from __future__ import annotations

import math

import jiko_style as J
import titan_fig as F

ONOFF = ("off", "on")
VIEWS = dict(dam=dict(lab="横から見た断面（ダム・谷に沿う）"), marks=dict(lab="横から見た断面（谷を横切る）"),
             two=dict(lab="横から見た断面（谷を横切る）"), pair=dict(lab="横から見た断面（谷を横切る）"),
             probe=dict(lab="横から見た断面（谷を横切る）"),
             # ⚠️ qa_all の dup：見る向きの札「水理模型とは」が c504 の見出しと同じだった＝左の本物の谷の向きを言う
             model=dict(lab="横から見た断面（谷を横切る）と模型"),
             seep=dict(lab="横から見た断面（谷を横切る）"))
FIELDS = dict(dam=dict(base=ONOFF, top=ONOFF, force=ONOFF),
              marks=dict(marks=("off", "on", "moved"), dir=ONOFF),
              two=dict(block=ONOFF, slip=ONOFF, move=ONOFF),
              pair=dict(right=ONOFF),
              probe=dict(survey=ONOFF, holes=ONOFF),
              model=dict(copy=ONOFF, scale=ONOFF),
              seep=dict(inner=ONOFF, push=ONOFF))
START = {v: {k: vs[0] for k, vs in f.items()} for v, f in FIELDS.items()}
ORDER = dict(marks=("off", "on", "moved"))               # 戻さない欄（目印は動いたら戻らない）

# ── 写し（縦横同じ縮尺）。u＝VB の横の距離（南の端 y830 から北へ m）／ダムは VC の w（#100 の x905 から西へ m）──
SLOPE = dict(k=0.692, x0=233.5, u0=0.0, y0=262.0, z0=1300.0)      # u 0〜2,100m・標高 450〜1,300m
PAIR = (dict(k=0.405, x0=86.0, u0=0.0, y0=356.0, z0=1300.0), dict(k=0.405, x0=974.0, u0=0.0, y0=356.0, z0=1300.0))
DAM = dict(k=2.0, x0=100.0, u0=None, y0=240.0, z0=760.0)           # u0＝ダムの上流 480m（_map で決める）・底 y≈832
MODEL = (dict(k=0.40, x0=96.0, u0=0.0, y0=356.0, z0=1300.0), dict(k=0.15, x0=1310.0, u0=0.0, y0=470.0, z0=1300.0))
U1 = 2100.0                        # 斜面の断面の北の端（北の岸の印 930m の先まで）
LAKE = dict(marks=650.0, two=650.0, pair=650.0, probe=650.0, seep=702.5, model=700.0)   # 水位（S1 p72・p96・p89）
DAM_LAKE = 722.5                   # ダムの断面の湖（最も高い水位＝S1 PDF63）
MARKS_U = (380.0, 640.0, 900.0, 1160.0)    # 目印の位置（模式）
MARK_SHIFT = 34.0                  # 目印のずれ（画素・斜面に沿って下へ＝大きく描いた模式）
COVER = 15.0                       # 調べた線の上の崩れた土の厚さ（m・記録 10〜20m の真ん中＝S1 PDF74）
SURVEY_U = (620.0, 1180.0)         # 人工の揺れで調べた線の範囲（模式）
BORINGS = (420.0, 760.0, 1050.0)   # 試し掘り3本（S1 PDF148＝1959〜60年の3本）の位置（模式）
BORING_PAST = 30.0                 # 試し掘りの深さ＝2人の言うすべり面（模式）の 30m 下まで（そこを通っても面が無かった＝模式）
# 横穴2本（1961年・沢の近く＝S1 PDF148）の入口の u（地表）・長さ 150m で斜面の奥へ（模式）。⑤b-4 の下見：1120 は3本目の
#   試し掘り（u1050）と十字に交わって「＋の印」に見えた＝1250（試し掘りと交わらない）
TUNNELS = (1000.0, 1250.0)
TUNNEL_L = 150.0
SEEP_DROP = 40.0                   # 斜面の中の水の高さが湖より高い量（岸の近く・m・模式）
COL_FIX = dict(rock="#56606b", cover="#b9a079", block="#b9a079", slip="#e8b33c", water="#5d92b4", water_ln="#8fc3e4",
               inner="#8fc3e4", mark="#f2c14e")


def _map(view, idx=0):
    if view == "dam":
        import illu as IL
        return dict(DAM, u0=IL.VC_DAM_W - 480.0)
    if view == "pair":
        return PAIR[idx]
    if view == "model":
        return MODEL[idx]
    return SLOPE


def xy(m, u, z):
    """写し m の上の (u, z) → 画面の点（縦横同じ縮尺）。"""
    return (m["x0"] + (u - (m["u0"] or 0.0)) * m["k"], m["y0"] + (m["z0"] - z) * m["k"])


def _lin(P, u):
    import illu as IL
    return IL._lin(P, u)


def ground_um(u0=0.0, u1=U1):
    import illu as IL
    us = [u0] + [q[0] for q in IL.VB_G if u0 < q[0] < u1] + [u1]
    return [(u, _lin(IL.VB_G, u)) for u in us]


def _lake_um(level, u1=U1):
    """湖（谷の底から水位まで）＝南の岸と北の岸のあいだ。"""
    import illu as IL
    G = [q for q in IL.VB_G if q[0] <= u1]
    # 🔴 ⑤b-4 の試し焼き（c504）：水位700m は地形の点（南と北の岸＝ちょうど700m）と同じ値＝「< 0」では端の点を数えず湖が消えた
    #   ＝端に触れる所も数え、同じ u は1つに
    xs = sorted({round(a + (b - a) * (level - za) / (zb - za), 6) for (a, za), (b, zb) in zip(G, G[1:])
                 if (za - level) * (zb - level) <= 0 and za != zb})
    if len(xs) < 2:
        return []
    a, b = xs[0], xs[-1]
    return [(a, level), (b, level)] + [(u, _lin(IL.VB_G, u)) for u in reversed([a] + [q[0] for q in G if a < q[0] < b] + [b])]


def _poly(m, pts, fill, stroke=None, w=0.0, op=None, dash=None):
    return F.poly([xy(m, u, z) for u, z in pts], fill, stroke, w, close=True, op=op, dash=dash)


def _line(m, pts, col, w, dash=None, op=None):
    return F.poly([xy(m, u, z) for u, z in pts], "none", col, w, dash=dash, op=op)


GROUND = "#26343f"                 # 地面の塗り（⑤b-4 の下見：J.BG2 は背景とほぼ同じ色で地面が読めなかった）


def slope_base(m, level, labels=True):
    """斜面の断面の基図（地面・湖・地表の線・南／北）。"""
    g = [_poly(m, ground_um() + [(U1, 440.0), (0.0, 440.0)], GROUND, None),
         _line(m, ground_um(), J.INK_W, 3)]
    lk = _lake_um(level)
    if lk:
        g.append(_poly(m, lk, COL_FIX["water"], None, op=0.9))
        g.append(_line(m, lk[:2], COL_FIX["water_ln"], 3))
    if labels:
        (xa, ya), (xb, yb) = xy(m, 0.0, 440.0), xy(m, U1, 440.0)
        g.append(F.txtfit(xa + 6, ya - 14, "南", 80, cap=30, col=J.TICK))
        g.append(F.txtfit(xb - 6, yb - 14, "北", 80, cap=30, col=J.TICK, anchor="end"))
    return g


def slip_um():
    import illu as IL
    return [tuple(q) for q in IL.VB_SLIP]


def block_um():
    """2人の見立ての古い塊（地表とすべり面のあいだ・模式）。"""
    import illu as IL
    ub, ut = IL.VB_SLIP[0][0], IL.VB_SLIP[-1][0]
    us = [ub + (ut - ub) * j / 40 for j in range(41)]
    return [(u, _lin(IL.VB_G, u)) for u in us] + [(u, _lin(IL.VB_SLIP, u)) for u in reversed(us)]


def dam_um():
    import illu as IL
    return [tuple(q) for q in IL.vc_dam_um()]


def dam_bed_um(m):
    import illu as IL
    w0, w1 = m["u0"] - 20.0, m["u0"] + (F.BX1 - m["x0"]) / m["k"] + 20.0
    ws = [w0] + [q[0] for q in IL.VC_BED if w0 < q[0] < w1] + [w1]
    return [(w, IL.vc_bed(w)) for w in ws]


def dam_lake_um(m):
    import illu as IL
    d = dam_um()
    wu = IL._lin(sorted((z, w) for w, z in d[:25]), DAM_LAKE)
    face = [(w, z) for w, z in d[:25] if z <= DAM_LAKE]
    bed = [q for q in dam_bed_um(m) if q[0] < wu]
    return [(bed[0][0], DAM_LAKE), (wu, DAM_LAKE)] + list(reversed(face)) + list(reversed(bed))


def survey_um():
    """調べた線の上の崩れた土の層（地表から COVER m 下まで）。"""
    a, b = SURVEY_U
    us = [a + (b - a) * j / 24 for j in range(25)]
    top = [(u, _lin_g(u)) for u in us]
    return top + [(u, _lin_g(u) - COVER) for u in reversed(us)]


def _lin_g(u):
    import illu as IL
    return _lin(IL.VB_G, u)


STRATA = (1250.0, 1150.0, 1050.0, 950.0, 850.0, 750.0, 650.0)   # 地層の筋の南の端（u0）の標高（模式）
STRATA_DIP = 0.18                  # 谷（北）へ下がる傾き（m／m・模式）


def strata_um():
    """反対の見方の地層の筋（まっすぐ・谷へ少し傾く）を地面の中だけ切り出した線の並び [[(u, z), …], …]。"""
    out = []
    for z0 in STRATA:
        seg, best = [], []
        for j in range(0, 43):
            u = 50.0 * j
            z = z0 - STRATA_DIP * u
            if 460.0 < z < _lin_g(u) - 12.0:
                seg.append((u, z))
            else:
                best, seg = (seg if len(seg) > len(best) else best), []
        best = seg if len(seg) > len(best) else best
        if len(best) >= 2:
            out.append(best)
    return out


def boring_um(u):
    z = _lin_g(u)
    return [(u, z), (u, _lin(slip_um(), u) - BORING_PAST)]


def tunnel_um(u):
    z = _lin_g(u) - 2.0
    return [(u, z), (u - TUNNEL_L, z)]


def seep_um(level):
    """斜面の中の水の高さ（模式）＝岸の近くで湖より SEEP_DROP m 高く、斜面の奥へ上がる線。"""
    import illu as IL
    shore = next(a + (b - a) * (level - za) / (zb - za) for (a, za), (b, zb) in zip(IL.VB_G, IL.VB_G[1:])
                 if za > level >= zb)
    us = [shore - 900.0 + 900.0 * j / 18 for j in range(19)]
    return [(u, max(level, min(_lin_g(u) - 25.0, level + SEEP_DROP + (shore - u) * 0.22))) for u in us]


def _ring(c, r, n=20):
    return [[c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)] for i in range(n)]


def _P(ident, typ, pts=None, **kw):
    d = dict(id=ident, type=typ)
    if pts is not None:
        d["pts"] = [list(map(float, p)) for p in pts]
    d.update(kw)
    return d


def _slope_dir(u, du=60.0):
    """地表に沿って下る向き（南の斜面＝北へ下る）の単位の向き（画面）。"""
    a, b = xy(SLOPE, u, _lin_g(u)), xy(SLOPE, u + du, _lin_g(u + du))
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)


def parts_of(view, st):
    """状態 → 動く部品（目印の点）。🔴 門番（check_mech.judge_vsec）もこの関数を呼ぶ＝描く側と同じ幾何。"""
    if view != "marks":
        return []
    out = []
    for j, u in enumerate(MARKS_U):
        c = xy(SLOPE, u, _lin_g(u))
        dx, dy = _slope_dir(u)
        mv = st["marks"] == "moved"
        out.append(_P(f"mark{j}", "circle", c=[c[0], c[1] - 9.0], r=10.0, fill=COL_FIX["mark"], stroke="#10161b", w=2.5,
                      dx=MARK_SHIFT * dx if mv else 0.0, dy=MARK_SHIFT * dy if mv else 0.0,
                      alpha=1.0 if st["marks"] != "off" else 0.0))
    return out


def anchors(view, st):
    """札の指し先（段の終わりの状態で）。"""
    if view == "dam":
        m = _map("dam")
        d = dam_um()
        bot = [q for q in d if abs(q[1] - min(z for _w, z in d)) < 0.01]
        top = [q for q in d if abs(q[1] - max(z for _w, z in d)) < 0.01]
        return dict(base=xy(m, sum(w for w, _z in bot) / len(bot), min(z for _w, z in d)),
                    top=xy(m, sum(w for w, _z in top) / len(top), max(z for _w, z in d)),
                    lake=xy(m, m["u0"] + 120.0, DAM_LAKE), face=xy(m, d[12][0], d[12][1]))
    m = SLOPE
    import illu as IL
    a, b = xy(m, 300.0, _lin_g(300.0) + 120.0), xy(m, 1180.0, _lin_g(1180.0) + 90.0)     # 動く向きの矢印（stage_art と同じ）
    return dict(marks=xy(m, MARKS_U[1], _lin_g(MARKS_U[1])), block=xy(m, 520.0, 980.0), dir=((a[0] + b[0]) / 2, (a[1] + b[1]) / 2),
                slip=xy(m, 800.0, _lin(IL.VB_SLIP, 800.0)), top=xy(m, IL.VB_SLIP[0][0], IL.VB_SLIP[0][1]),
                lake=xy(m, 1500.0, LAKE.get(view, 650.0)), survey=xy(m, sum(SURVEY_U) / 2, _lin_g(sum(SURVEY_U) / 2)),
                holes=xy(m, *boring_um(BORINGS[1])[1]), inner=xy(m, 900.0, _lin_g(900.0) - 140.0))


# 札の置き場（x, y, 揃え, 幅）。🔴 段の札は残る（段の層は足し続ける＝ルール §5b-89）＝同じ置き場に2段の札を置かない
TAG_AT = dict(
    dam=dict(base=(1180.0, 812.0, "start", 520.0), top=(1180.0, 312.0, "start", 520.0), force=(110.0, 300.0, "start", 640.0),
             height=(1352.0, 560.0, "start", 300.0)),
    slope=dict(t1=(110.0, 300.0, "start", 760.0), t2=(110.0, 350.0, "start", 760.0), t3=(110.0, 400.0, "start", 760.0),
               r1=(1810.0, 300.0, "end", 640.0), r2=(1810.0, 350.0, "end", 640.0), b1=(1810.0, 836.0, "end", 760.0)),
    pair=dict(left=(86.0, 316.0, "start", 840.0), right=(974.0, 316.0, "start", 840.0), lb=(86.0, 836.0, "start", 840.0),
              rb=(974.0, 836.0, "start", 840.0)),
    model=dict(left=(96.0, 316.0, "start", 760.0), right=(1290.0, 380.0, "start", 520.0), scale=(1290.0, 760.0, "start", 520.0),
               b1=(96.0, 836.0, "start", 1100.0)),
)


def _tag_at(view):
    return TAG_AT["dam"] if view == "dam" else TAG_AT["pair"] if view == "pair" else TAG_AT["model"] \
        if view == "model" else TAG_AT["slope"]


def _states(view, start, steps):
    fields = FIELDS[view]
    cur = dict(START[view], **(start or {}))
    out = []
    for st in [dict(state={})] + list(steps):
        cur = dict(cur, **(st.get("state") or {}))
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"vsec：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"vsec：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    for f_, seq in ORDER.items():
        if f_ in FIELDS[view]:
            idx = [seq.index(s[f_]) for s in out]
            if any(b < a for a, b in zip(idx, idx[1:])):
                raise ValueError(f"vsec：{f_} は戻さない（{' → '.join(seq)}）")
    return out[0], out[1:]


# ── 段の層（その行から出て残る＝動かない絵と札）──
def _arrow(p, q, col, w=5.0, head=18.0):
    return F.arrow(p[0], p[1], q[0], q[1], col, w, head)


def _dim_h(a, b, y, col, tick=10.0):
    """横の寸法の線（a・b の x のあいだ・y）。"""
    return (F.line(a, y, b, y, col, 3) + F.line(a, y - tick, a, y + tick, col, 3) + F.line(b, y - tick, b, y + tick, col, 3))


def _dim_v(x, a, b, col, tick=10.0):
    return (F.line(x, a, x, b, col, 3) + F.line(x - tick, a, x + tick, a, col, 3) + F.line(x - tick, b, x + tick, b, col, 3))


def stage_art(view, prev, st):
    """段で新しく出る動かない絵（前の段との差）。"""
    g = []

    def on(f):
        return st.get(f) == "on" and prev.get(f) != "on"
    if view == "dam":
        m = _map("dam")
        d = dam_um()
        zb, zt = min(z for _w, z in d), max(z for _w, z in d)
        bot = sorted(w for w, z in d if abs(z - zb) < 0.01)
        top = sorted(w for w, z in d if abs(z - zt) < 0.01)
        if on("base"):
            (xa, y), (xb, _y) = xy(m, bot[0], zb), xy(m, bot[-1], zb)
            g.append(_dim_h(xa, xb, y + 20.0, J.AMBER) + F.line(xb + 4.0, y + 20.0, 1170.0, 800.0, J.AMBER, 2))
        if on("top"):
            (xa, y), (xb, _y) = xy(m, top[0], zt), xy(m, top[-1], zt)
            g.append(_dim_h(xa, xb, y - 20.0, J.AMBER, 8.0) + F.line(xb + 4.0, y - 20.0, 1170.0, 300.0, J.AMBER, 2))
        if on("force"):
            # 水の力（湖の側から・深いほど大きい＝長さは模式）。ダムの上流の面へ
            for z in (690.0, 640.0, 590.0, 540.0, 490.0):
                fw = next(w for w, zz in d[:25] if zz >= z)
                L = 40.0 + (DAM_LAKE - z) * 0.9
                p, q = xy(m, fw - L / m["k"] - 4.0, z), xy(m, fw - 3.0, z)
                g.append(_arrow(p, q, COL_FIX["water_ln"], 5.0, 16.0))
        return g
    if view == "marks":
        if st["marks"] == "moved" and prev.get("marks") != "moved":
            for u in MARKS_U:                                     # 前の日の位置（薄い輪）
                c = xy(SLOPE, u, _lin_g(u))
                g.append(F.circ(c[0], c[1] - 9.0, 10.0, "none", J.TICK, 2.5))
        if on("dir"):
            a, b = xy(SLOPE, 300.0, _lin_g(300.0) + 120.0), xy(SLOPE, 1180.0, _lin_g(1180.0) + 90.0)
            g.append(_arrow(a, b, J.AMBER, 7.0, 26.0))
        return g
    if view == "two":
        if on("block"):
            g.append(_poly(SLOPE, block_um(), COL_FIX["block"], "#5e4b33", 2.5, op=0.85))
        if on("slip"):
            g.append(_line(SLOPE, slip_um(), COL_FIX["slip"], 6, dash="16 10"))
        if on("move"):
            a = xy(SLOPE, 330.0, _lin(slip_um(), 330.0) + 110.0)
            b = xy(SLOPE, 1080.0, _lin(slip_um(), 1080.0) + 70.0)
            g.append(_arrow(a, b, J.ALERT, 7.0, 26.0))
        return g
    if view == "pair":
        if on("right"):
            m = PAIR[1]
            g += slope_base(m, LAKE["pair"])
            # 岩は元の場所にある＝地層の筋が山の奥からまっすぐ続く（すべり面も塊も無い＝模式）。⑤b-4 の下見：地表に平行な筋は
            #   「すべりそうな板」に見え、断面の下の端からもはみ出した＝少し谷へ傾いたまっすぐの筋を、地面の中（地表の下・底の上）だけ
            for seg in strata_um():
                g.append(_line(m, seg, J.LINE, 2.5, op=0.8))
        return g
    if view == "probe":
        if on("survey"):
            g.append(_poly(SLOPE, survey_um(), COL_FIX["cover"], "#5e4b33", 2.0))
            a, b = SURVEY_U
            for j in range(7):                                    # 受ける点（三角）
                u = a + (b - a) * j / 6
                x, y = xy(SLOPE, u, _lin_g(u))
                g.append(F.poly([(x, y - 18), (x - 9, y - 4), (x + 9, y - 4)], J.INK_W, "#10161b", 1.5, close=True))
            for j in (2, 4, 6):                                   # 揺れの通り道（土の下の岩の上をたどる）
                u1 = a + (b - a) * j / 6
                pts = [(a, _lin_g(a)), (a + 40.0, _lin_g(a + 40.0) - COVER - 4.0), (u1 - 40.0, _lin_g(u1 - 40.0) - COVER - 4.0),
                       (u1, _lin_g(u1))]
                g.append(_line(SLOPE, pts, J.AMBER, 2.5, op=0.9))
            x, y = xy(SLOPE, a, _lin_g(a))                        # 揺れを起こす所（赤い丸）
            g.append(F.circ(x, y - 12.0, 11.0, J.ALERT, "#10161b", 2.0))
        if on("holes"):
            g.append(_line(SLOPE, slip_um(), COL_FIX["slip"], 4, dash="12 10", op=0.65))     # 2人の言うすべり面（模式）
            for u in BORINGS:
                g.append(_line(SLOPE, boring_um(u), J.INK_W, 5))
            for t in TUNNELS:
                g.append(_line(SLOPE, tunnel_um(t), J.INK_W, 7))
        return g
    if view == "model":
        if on("copy"):
            m = MODEL[1]
            G = ground_um(0.0, 2528.0)
            g.append(F.rect(m["x0"] - 26.0, m["y0"] - 30.0, 2528.0 * m["k"] + 52.0, 850.0 * m["k"] + 60.0, J.BG, J.INK_W, 3))
            g.append(F.poly([xy(m, u, z) for u, z in G] + [xy(m, 2528.0, 440.0), xy(m, 0.0, 440.0)], GROUND, J.INK_W, 2,
                            close=True))
            lk = _lake_um(LAKE["model"], 2528.0)
            if lk:
                g.append(F.poly([xy(m, u, z) for u, z in lk], COL_FIX["water"], COL_FIX["water_ln"], 2, close=True, op=0.9))
            a, b = (MODEL[0]["x0"] + 2528.0 * MODEL[0]["k"] + 20.0, 560.0), (m["x0"] - 40.0, 560.0)
            g.append(_arrow(a, b, J.AMBER, 7.0, 26.0))
        return g
    if view == "seep":
        lv = LAKE["seep"]
        if on("inner"):
            g.append(_line(SLOPE, seep_um(lv), COL_FIX["inner"], 5, dash="14 9"))
        if on("push"):
            for u in (1080.0, 1180.0, 1270.0):
                z = _lin(seep_um(lv), u) - 10.0
                p = xy(SLOPE, u - 50.0, z)
                dx, dy = _slope_dir(u)
                g.append(_arrow(p, (p[0] + dx * 70.0, p[1] + dy * 70.0 - 6.0), J.ALERT, 5.0, 16.0))
            x, y = xy(SLOPE, 1560.0, lv)
            g.append(_arrow((x, y - 70.0), (x, y - 8.0), COL_FIX["water_ln"], 5.0, 16.0))
        return g
    return g


def _stage_svgs(view, steps, start, states, cap=34):
    pre = _tag_at(view)
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


def _base(view, start):
    """動かない基図（頭の状態で出ている絵も＝段の層は差だけ）。"""
    g = []
    if view == "dam":
        m = _map("dam")
        bed = dam_bed_um(m)
        g.append(F.poly([xy(m, w, z) for w, z in bed] + [xy(m, bed[-1][0], 440.0), xy(m, bed[0][0], 440.0)], GROUND, J.INK_W,
                        2.5, close=True))
        g.append(F.poly([xy(m, w, z) for w, z in dam_lake_um(m)], COL_FIX["water"], None, 0, close=True, op=0.9))
        lk = dam_lake_um(m)[:2]
        g.append(F.poly([xy(m, w, z) for w, z in lk], "none", COL_FIX["water_ln"], 3))
        g.append(F.poly([xy(m, w, z) for w, z in dam_um()], "#e6eaed", "#20262d", 2, close=True))
        d = dam_um()
        zb, zt = min(z for _w, z in d), max(z for _w, z in d)
        x = xy(m, max(w for w, _z in d) + 120.0, 0.0)[0]
        g.append(_dim_v(x, xy(m, 0, zt)[1], xy(m, 0, zb)[1], J.TICK))
        # 左右の端の札（上流・下流＝VC と同じ）は湖の上の高さに（下の端は左下の出典の行＝y886 と重なる）
        g.append(F.txtfit(110.0, 420.0, "上流（湖）", 300, cap=30, col=J.INK_W))
        g.append(F.txtfit(1810.0, 420.0, "下流", 200, cap=30, col=J.TICK, anchor="end"))
        st = dict(START["dam"], **start)
        g += stage_art("dam", START["dam"], st)
        return g
    if view == "pair":
        g += slope_base(PAIR[0], LAKE["pair"])
        g.append(_poly(PAIR[0], block_um(), COL_FIX["block"], "#5e4b33", 2.0, op=0.85))
        g.append(_line(PAIR[0], slip_um(), COL_FIX["slip"], 4, dash="12 8"))
        g.append(F.line(F.BX0 + F.BW / 2, F.BY0 + 70, F.BX0 + F.BW / 2, F.BY1 - 60, J.LINE_DIM, 2, dash="8 8"))
        st = dict(START["pair"], **start)
        g += stage_art("pair", START["pair"], st)
        return g
    if view == "model":
        m = MODEL[0]
        G = ground_um(0.0, 2528.0)
        g.append(F.poly([xy(m, u, z) for u, z in G] + [xy(m, 2528.0, 440.0), xy(m, 0.0, 440.0)], GROUND, J.INK_W, 2.5, close=True))
        lk = _lake_um(LAKE["model"], 2528.0)
        if lk:
            g.append(F.poly([xy(m, u, z) for u, z in lk], COL_FIX["water"], COL_FIX["water_ln"], 2.5, close=True, op=0.9))
        st = dict(START["model"], **start)
        g += stage_art("model", START["model"], st)
        return g
    g += slope_base(SLOPE, LAKE[view])
    st = dict(START[view], **start)
    g += stage_art(view, START[view], st)
    return g


def geo_of(view, start, states):
    """門番が測る形（画面の点）と写し（目盛り）。🔴 描く関数と同じ式（§5b-88＝門番は記録を自分の側に持つ）。"""
    m = _map(view)
    out = dict(map=dict(m))
    if view == "dam":
        out["dam"] = [list(xy(m, w, z)) for w, z in dam_um()]
        out["lake_y"] = xy(m, 0.0, DAM_LAKE)[1]
    elif view == "model":
        out["lake_y"] = xy(MODEL[0], 0.0, LAKE["model"])[1]
        out["map"] = dict(MODEL[0])
    else:
        mm = PAIR[0] if view == "pair" else SLOPE
        out["map"] = dict(mm)
        out["lake_y"] = xy(mm, 0.0, LAKE[view])[1]
        out["ground"] = [list(xy(mm, u, z)) for u, z in ground_um()]
    allst = [start] + list(states)
    if view == "probe" and any(s["survey"] == "on" for s in allst):
        out["cover"] = [list(xy(SLOPE, u, z)) for u, z in survey_um()]
    if view == "probe" and any(s["holes"] == "on" for s in allst):
        out["borings"] = [[list(xy(SLOPE, u, z)) for u, z in boring_um(u0)] for u0 in BORINGS]
        out["tunnels"] = [[list(xy(SLOPE, u, z)) for u, z in tunnel_um(t)] for t in TUNNELS]
    if view == "seep":
        out["inner"] = [list(xy(SLOPE, u, z)) for u, z in seep_um(LAKE["seep"])]
    return out


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def vsec(view, steps, start=None, rel=(), note="", src=""):
    """16本目の断面の図解。view＝dam｜marks｜two｜pair｜probe｜model｜seep。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"vsec：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if "模式" not in note:
        raise ValueError("vsec：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
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
        if not sh["anim"] and float(sh["keys"][0].get("alpha", 1.0)) > 0.01:
            g.append(F.circ(sh["c"][0], sh["c"][1], sh["r"], sh["fill"], sh["stroke"], sh["w"]))
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, VIEWS[view]["lab"] + "・模式", 1000, cap=28, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, st0, states)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="vsec", view=view, start=st0, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states))
    return f
