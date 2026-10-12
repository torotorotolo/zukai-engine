# -*- coding: utf-8 -*-
"""mech21.py — 21本目（9.11 米国同時多発テロのリメイク）「模式図」（2026-10-12 新設・⑤b-3）。

■ 何か
  18本目 `mech18`・19本目 `mech19`・20本目 `mech20` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。
  再現イラストではない＝「再現」の札は出さない。左上に見る向き・左下に「模式」と出典。🔴 人は描かない（乗っ取った側・乗員・乗客・管制官の
  どの人の形も描かない＝§2 守りの線）。🔴 記録の言葉（無線・電話の逐語）は画面に出さない＝語りと字幕だけ（10-11 カズヤくんの決め）。

■ 見え方（view）＝台本 第2版 §4 の画の欄（第1〜3章）
  us      … 北アメリカの陸（Natural Earth＝国境なし）と出発の3つの空港・行き先の2つの街・4便を結ぶ線（実際の経路ではない）  c202
  ne      … 北東部の陸と NEADS（ローム）・待機の2か所（オーティス・ラングレー）・海の外から来る矢印・オーティスの「？」     c318・c319・c419
  gate    … 保安検査（金属探知機の門2台・手持ちの探知機・通過の矢印）＝人は描かない                              c211
  blade   … 刃渡りの物差し（4インチ＝10.16センチの線）と刃物の影・3つの理由の札                                 c212・c213
  tools   … 機内からの電話が伝えた道具（刃物・スプレー・「爆弾」と「おそらく偽物」）                              c214
  door    … 操縦室の扉（閉めて鍵・金庫の扉の案・鍵が外れて開く・「要求に従う」の矢印）                           c215・c306・c307・c308
  old     … 昔ながらの乗っ取り（要求をのむ→無事に着陸→警察や軍に任せる・要求の中身・暴力が起きたら＝空白）           c303・c304・c305
  chain   … 手順の段（管制官→上司→FAA の本部→国防総省の指揮所→国防長官の許し→NORAD→戦闘機）・ボストンの近道・
            昔の待機の基地・本部の×・後ろの戦闘機の小窓                                       c311・c312・c314・c413・c414・c425
  escort  … 乗っ取られた機と、約8キロ（5マイル）後ろの戦闘機・そばに寄せない                                     c313
  premise … 手順の3つの前提の箱（1つ目に×＝11便）                                                         c315・c316・c426
  cabin   … 上から見た機内（座席の並び 2-3-2・操縦室の扉）・連邦航空保安官の席の印が無い                         c310・c403
  phone   … 機内の電話から地上（航空会社の予約の窓口）への線・約25分・訓練の線（操縦室へ）に×                    c404・c405・c406
  radio   … 管制の無線（ボストン・センターと11便）・機内の放送のつもり・聞き取れない・2つ目の声                    c409・c410・c411
  call    … 電話の線（ボストン・センター→NEADS・8:37:52）・行き来の矢印・演習の予定の札                          c415・c416・c417
  scope   … レーダーの画面（点と便名・高度の札＝札が消える／NEADS の画面＝札の無い点を探す）                    c407・c420・c424

■ SPEC の書き方（mech20 と同じ）
  fig=("m21", dict(view=…, start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…, d=…)), …],
                   rel=[dict(t="8:21", src="委員会報告 p18")], note="…模式…", src=ss.src([…])))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。札の数・時刻は `rel=` に同じ文字列（門番 check_mech の judge_m21）。
  🔴 記録の値（空港・基地の緯度経度・4便の出発と行き先・4インチ・5マイル・手順の段の順・待機の2か所）は門番 check_mech の REC_M21 が
     別に持つ（§5b-88）。⚠️ 動く部品は段の層（札）より上に描かれる＝札は動く部品の通り道に置かない
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import jiko_style as J
import titan_fig as F

HERE = Path(__file__).resolve().parent.parent
ONOFF = ("off", "on")
INK = J.INK_W
L_X, R_X = F.BX0 + 40.0, 1270.0          # 札の左の列・右の列の x
COL = dict(land="#22333f", land_ln="#41606f", sea_ar="#7fb8e6", body="#c9d3da", body_ln="#2a333a", dark="#10161b",
           seat="#41606f", scope="#0b1712", scope_ln="#2f5b45", blip="#7fe3a2", block="#7fe3a2", green="#5fbf8f",
           panel="#3b4a56", door="#55687a", door_ln="#aab9c4", metal="#8a9aa6")


def _P(ident, typ, pts=None, **kw):
    d = dict(id=ident, type=typ)
    if pts is not None:
        d["pts"] = [list(map(float, p)) for p in pts]
    d.update(kw)
    return d


def _on(prev, st, f, v="on"):
    """この段で f が v になった（前の段は v でない）。"""
    return st.get(f) == v and prev.get(f) != v


def _box(cx, cy, w, h, t, col=None, ink=None, cap=30, fill=None, sw=4, dash=None, t2=None):
    """箱と字（1行か2行）。"""
    col = col or J.LINE
    g = [F.rect(cx - w / 2, cy - h / 2, w, h, fill or J.BG2, col, sw, rx=10, dash=dash)]
    if t2:
        g.append(F.txtfit(cx, cy - 6, t, w - 24, cap=cap, col=ink or INK, anchor="middle"))
        g.append(F.txtfit(cx, cy + cap + 2, t2, w - 24, cap=cap, col=ink or INK, anchor="middle"))
    elif t:
        g.append(F.txtfit(cx, cy + cap * 0.36, t, w - 24, cap=cap, col=ink or INK, anchor="middle"))
    return "".join(g)


def _xmark(cx, cy, r=26, col=None, w=9):
    c = col or J.ALERT
    return (F.line(cx - r, cy - r, cx + r, cy + r, J.BG, w + 6) + F.line(cx - r, cy + r, cx + r, cy - r, J.BG, w + 6)
            + F.line(cx - r, cy - r, cx + r, cy + r, c, w) + F.line(cx - r, cy + r, cx + r, cy - r, c, w))


def _qmark(cx, cy, cap=64, col=None):
    return F.txt(cx, cy + cap * 0.36, "？", cap, col or J.AMBER, "Noto", "middle", ol=6)


def _check(cx, cy, s=26, col=None):
    return F.poly([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.8)], "none", col or COL["green"], 9)


def _arrow(x1, y1, x2, y2, col=None, sw=5, head=20, dash=None):
    """矢印（破線も描ける＝線は破線・頭は塗り）。"""
    c = col or J.LINE
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * 0.8 * math.cos(a), y2 - head * 0.8 * math.sin(a)
    p = [(x2, y2), (x2 - head * math.cos(a - 0.42), y2 - head * math.sin(a - 0.42)),
         (x2 - head * math.cos(a + 0.42), y2 - head * math.sin(a + 0.42))]
    return F.line(x1, y1, bx, by, c, sw, dash=dash) + F.poly(p, c, None, close=True)


def _plane_side(x0, y0, L, col=None, ln=None):
    """横から見た旅客機（機首が左・L＝長さの画素）。人は描かない。戻り＝(svg, 操縦室の点, 客室の点, 胴の上の点)"""
    c, k = col or COL["body"], ln or COL["body_ln"]
    h = L * 0.11
    body = [(x0, y0), (x0 + L * 0.03, y0 - h * 0.45), (x0 + L * 0.10, y0 - h * 0.62), (x0 + L * 0.84, y0 - h * 0.62),
            (x0 + L * 0.97, y0 - h * 1.9), (x0 + L, y0 - h * 1.9), (x0 + L * 0.98, y0 - h * 0.40), (x0 + L * 0.90, y0 + h * 0.30),
            (x0 + L * 0.10, y0 + h * 0.42), (x0 + L * 0.03, y0 + h * 0.30)]
    wing = [(x0 + L * 0.40, y0 + h * 0.20), (x0 + L * 0.62, y0 + h * 0.95), (x0 + L * 0.67, y0 + h * 0.95), (x0 + L * 0.55, y0 + h * 0.20)]
    win = "".join(F.circ(x0 + L * (0.14 + 0.024 * i), y0 - h * 0.20, max(2.0, h * 0.06), COL["dark"]) for i in range(28))
    ck = F.poly([(x0 + L * 0.035, y0 - h * 0.28), (x0 + L * 0.075, y0 - h * 0.46), (x0 + L * 0.085, y0 - h * 0.22)], COL["dark"])
    svg = F.poly(body, c, k, 3, close=True) + F.poly(wing, COL["metal"], k, 3, close=True) + win + ck
    return svg, (x0 + L * 0.06, y0 - h * 0.05), (x0 + L * 0.62, y0 - h * 0.05), (x0 + L * 0.50, y0 - h * 0.62)


def _plane_top(cx, cy, L, col=None, ln=None, fighter=False, dash=None, op=None):
    """上から見た機（機首が右・L＝長さの画素）。fighter＝戦闘機（細い胴・後退翼・2枚の尾翼）。"""
    c, k = col or COL["body"], ln or COL["body_ln"]
    if fighter:
        p = [(1.0, 0.0), (0.80, 0.05), (0.55, 0.07), (0.35, 0.46), (0.25, 0.46), (0.28, 0.08), (0.10, 0.08), (0.02, 0.26),
             (-0.04, 0.26), (0.0, 0.0)]
    else:
        p = [(1.0, 0.0), (0.94, 0.05), (0.62, 0.055), (0.42, 0.50), (0.36, 0.50), (0.44, 0.055), (0.12, 0.055), (0.02, 0.20),
             (-0.02, 0.20), (0.0, 0.0)]
    top = [(cx + (u - 0.5) * L, cy - v * L) for u, v in p]
    bot = [(cx + (u - 0.5) * L, cy + v * L) for u, v in reversed(p)]
    return F.poly(top + bot, c if not dash else "none", k if not dash else c, 3 if not dash else 4, close=True, dash=dash, op=op)


def _building(cx, cy, w=200, h=130, col=None):
    """地上の建物（管制のセンター・軍の部署・窓口）＝箱と窓とアンテナ。"""
    c = col or J.LINE
    g = [F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, c, 4, rx=6)]
    for i in range(4):
        for j in range(2):
            g.append(F.rect(cx - w / 2 + 22 + i * (w - 44) / 4, cy - h / 2 + 24 + j * 44, (w - 44) / 4 - 14, 24, COL["panel"]))
    g.append(F.line(cx + w * 0.28, cy - h / 2, cx + w * 0.28, cy - h / 2 - 46, c, 4))
    g.append(F.circ(cx + w * 0.28, cy - h / 2 - 50, 7, c))
    return "".join(g)


def _waves(x, y, ang, n=3, r0=24, col=None):
    """電波の弧（ang＝向き・度＝画面の座標で右が0）。"""
    g = []
    for i in range(n):
        r = r0 + i * 20
        pts = [(x + r * math.cos(math.radians(ang + a)), y + r * math.sin(math.radians(ang + a))) for a in range(-35, 36, 7)]
        g.append(F.poly(pts, "none", col or J.AMBER, 5))
    return "".join(g)


# ══════════════════════════════════════════════════════════
#  地図（us・ne）＝Natural Earth の陸（`ref/ep21/coast_ne50m.json`）＋緯度経度の点。縮尺は東西と南北をそろえる（中心の緯度の正距円筒）
# ══════════════════════════════════════════════════════════
COAST = HERE / "ref" / "ep21" / "coast_ne50m.json"
MAP_VIEW = dict(us=dict(lon=(-127.0, -64.0), lat=(23.5, 50.5)),
                ne=dict(lon=(-88.9, -58.6), lat=(35.9, 44.1)))
MAP_BOX = (F.BX0 + 40.0, 270.0, F.BW - 80.0, 590.0)
# 地点（緯度・経度＝空港・基地・街の一般の座標〈Wikidata の値と同じ桁〉。報告書の値ではない＝図の札に「模式」）
MAP_PTS = dict(bos=(42.3656, -71.0096), ewr=(40.6925, -74.1687), iad=(38.9531, -77.4565), lax=(33.9425, -118.4081),
               sfo=(37.6189, -122.3750), rome=(43.2338, -75.4070), otis=(41.6584, -70.5214), langley=(37.0829, -76.3605),
               nyc=(40.7128, -74.0060), dc=(38.9072, -77.0369), boston=(42.3601, -71.0589))
MAP_NAMES = dict(bos="ボストン", ewr="ニューアーク", iad="ワシントン・ダレス", lax="ロサンゼルス", sfo="サンフランシスコ",
                 rome="ローム（NEADS）", otis="オーティス", langley="ラングレー", nyc="ニューヨーク", dc="ワシントン", boston="ボストン")
# 4便（出発 → 行き先）＝委員会報告 p4・p7・p8・p10
ROUTES = (("11便・175便", "bos", "lax"), ("77便", "iad", "lax"), ("93便", "ewr", "sfo"))
US_LAB = dict(bos=(1470.0, 445.0), ewr=(1470.0, 492.0), iad=(1470.0, 539.0), lax=(430.0, 650.0), sfo=(430.0, 560.0))
US_FLT = dict(bos="11便・175便", ewr="93便", iad="77便")


class Geo:
    def __init__(self, view):
        v = MAP_VIEW[view]
        self.latc, self.lonc = (v["lat"][0] + v["lat"][1]) / 2, (v["lon"][0] + v["lon"][1]) / 2
        self.kx = 111.32 * math.cos(math.radians(self.latc))
        self.ky = 110.57
        x0, y0, w, h = MAP_BOX
        self.s = min(w / ((v["lon"][1] - v["lon"][0]) * self.kx), h / ((v["lat"][1] - v["lat"][0]) * self.ky))
        self.cx, self.cy = x0 + w / 2, y0 + h / 2

    def px(self, lat, lon):
        return (self.cx + (lon - self.lonc) * self.kx * self.s, self.cy - (lat - self.latc) * self.ky * self.s)

    def geo(self, x, y):
        return (self.latc - (y - self.cy) / (self.ky * self.s), self.lonc + (x - self.cx) / (self.kx * self.s))


_COAST = []


def coast():
    if not _COAST:
        _COAST.extend(json.loads(COAST.read_text(encoding="utf-8"))["polys"])
    return _COAST


def map_base(view):
    G = Geo(view)
    x0, y0, w, h = MAP_BOX
    g = [F.rect(x0, y0, w, h, J.BG, J.LINE_DIM, 3)]
    for p in coast():
        q = [G.px(la, lo) for lo, la in p]
        if max(x for x, _ in q) < x0 or min(x for x, _ in q) > x0 + w:
            continue
        g.append(F.poly([(min(max(x, x0), x0 + w), min(max(y, y0), y0 + h)) for x, y in q], COL["land"], COL["land_ln"], 2, close=True))
    return g, G


def _dot(G, k, col=None, r=9):
    x, y = G.px(*MAP_PTS[k])
    return F.circ(x, y, r, col or INK, J.BG, 3)


def us_base(st0):
    g, G = map_base("us")
    return g


def us_stage(prev, st):
    G = Geo("us")
    s = []
    if _on(prev, st, "east"):
        for k in ("bos", "ewr", "iad"):
            x, y = G.px(*MAP_PTS[k])
            lx, ly = US_LAB[k]
            s.append(F.line(x + 10, y, lx - 12, ly - 10, J.LINE, 2))
            s.append(_dot(G, k, J.AMBER))
            s.append(F.txtfit(lx, ly, f"{MAP_NAMES[k]}（{US_FLT[k]}）", MAP_BOX[0] + MAP_BOX[2] - lx - 14, cap=28, col=INK, ol=6))   # ⚠️ geom_gap：枠の外へ出た
    if _on(prev, st, "west"):
        for k in ("lax", "sfo"):
            x, y = G.px(*MAP_PTS[k])
            lx, ly = US_LAB[k]
            s.append(F.line(x - 10, y, lx + 12, ly - 10, J.LINE, 2))
            s.append(_dot(G, k, INK))
            s.append(F.txtfit(lx, ly, MAP_NAMES[k], lx - F.BX0 - 50, cap=28, col=INK, anchor="end", ol=6))
    if _on(prev, st, "routes"):
        for _, a, b in ROUTES:
            (ax, ay), (bx, by) = G.px(*MAP_PTS[a]), G.px(*MAP_PTS[b])
            L_ = math.hypot(bx - ax, by - ay)
            ux, uy = (bx - ax) / L_, (by - ay) / L_
            s.append(_arrow(ax + ux * 14, ay + uy * 14, bx - ux * 14, by - uy * 14, J.AMBER, 4, 22, dash="16 10"))
    return s


NE_LAB = dict(rome=(840.0, 336.0, "end"), otis=(1192.0, 470.0, "start"),     # ⚠️ geom_gap：1172 だと発進の輪（r 34）が字に触れた
              langley=(790.0, 800.0, "end"), nyc=(990.0, 545.0, "start"),
              dc=(750.0, 660.0, "end"), boston=(1140.0, 404.0, "start"))
NE_BASES = ("otis", "langley")                   # すぐ呼べた待機の2か所（委員会報告 p17）
NE_SEA = (((38.2, -63.5), (39.6, -70.6)), ((36.9, -64.0), (37.6, -73.2)), ((40.6, -62.0), (41.0, -68.6)))   # 海の外から来る矢印（向きだけ・模式）
NE_DOM = ((41.3, -84.5), (40.9, -76.6))         # 国内の便の矢印（向きだけ・模式）＝想定の外
NE_Q = ((42.7, -71.6), (42.0, -72.3), (40.7, -69.8))   # オーティスからの「どこへ？」の向き（模式）。⚠️ 門番 layout：南西へ振ると「ニューヨーク」の札に「？」が乗った


def ne_base(st0):
    g, G = map_base("ne")
    for k in ("nyc", "dc", "boston"):
        x, y = G.px(*MAP_PTS[k])
        lx, ly, an = NE_LAB[k]
        g.append(F.circ(x, y, 7, J.LINE, J.BG, 2))
        g.append(F.txtfit(lx, ly, MAP_NAMES[k], 360, cap=26, col=J.TICK, anchor=an, ol=6))
    return g


def _ring_pt(G, k, col, r=20):
    x, y = G.px(*MAP_PTS[k])
    return F.circ(x, y, r, "none", J.BG, 9) + F.circ(x, y, r, "none", col, 5) + F.circ(x, y, 7, col)


def ne_stage(prev, st):
    G = Geo("ne")
    s = []
    if _on(prev, st, "neads"):
        lx, ly, an = NE_LAB["rome"]
        s += [_ring_pt(G, "rome", J.INST, 22), F.txtfit(lx, ly, MAP_NAMES["rome"], 420, cap=30, col=INK, anchor=an, ol=6)]
    if _on(prev, st, "bases"):
        for k in NE_BASES:
            lx, ly, an = NE_LAB[k]
            s += [_ring_pt(G, k, J.AMBER), F.txtfit(lx, ly, MAP_NAMES[k], 360, cap=30, col=INK, anchor=an, ol=6)]
    if _on(prev, st, "sea"):
        for a, b in NE_SEA:
            (ax, ay), (bx, by) = G.px(*a), G.px(*b)
            s.append(_arrow(ax, ay, bx, by, COL["sea_ar"], 6, 24))
    if _on(prev, st, "dom"):
        (ax, ay), (bx, by) = G.px(*NE_DOM[0]), G.px(*NE_DOM[1])
        s.append(_arrow(ax, ay, bx, by, J.TICK, 5, 22, dash="14 10"))
        s.append(_qmark((ax + bx) / 2, (ay + by) / 2 - 40, 52, J.TICK))
    if _on(prev, st, "scr"):
        ox, oy = G.px(*MAP_PTS["otis"])
        s.append(F.circ(ox, oy, 34, "none", J.AMBER, 4))
        for q in NE_Q:
            qx, qy = G.px(*q)
            s.append(_arrow(ox, oy, qx, qy, J.AMBER, 4, 18, dash="10 8"))
            s.append(_qmark(qx + (qx - ox) * 0.25, qy + (qy - oy) * 0.25, 40))
    return s


# ══════════════════════════════════════════════════════════
#  gate（c211）＝保安検査の流れ（人は描かない）
# ══════════════════════════════════════════════════════════
GT = dict(floor=780.0, arch=(560.0, 860.0), aw=170.0, ah=320.0, wand=(1170.0, 640.0), exit=(1470.0, 1720.0))
GT_N = 2                                          # 鳴った探知機の数（委員会報告 p3「the first and second metal detectors」）


def gate_base(st0):
    g = [F.line(F.BX0 + 60, GT["floor"], F.BX1 - 60, GT["floor"], J.LINE_DIM, 4)]
    for i, x in enumerate(GT["arch"]):
        w, h, y1 = GT["aw"], GT["ah"], GT["floor"]
        g.append(F.poly([(x - w / 2, y1), (x - w / 2, y1 - h), (x + w / 2, y1 - h), (x + w / 2, y1)], "none", J.LINE, 14))
        g.append(F.txtfit(x, y1 + 46, f"探知機の門（{i + 1}台目）", 300, cap=28, col=J.TICK, anchor="middle"))
    wx, wy = GT["wand"]
    g.append(F.rect(wx - 18, wy - 90, 36, 120, COL["panel"], J.LINE, 4, rx=14))
    g.append(F.rect(wx - 10, wy + 30, 20, 80, COL["panel"], J.LINE, 4, rx=6))
    g.append(F.txtfit(wx, GT["floor"] + 46, "手持ちの探知機", 300, cap=28, col=J.TICK, anchor="middle"))
    g.append(_arrow(F.BX0 + 90, GT["floor"] - 60, GT["arch"][0] - GT["aw"] / 2 - 20, GT["floor"] - 60, J.LINE_DIM, 5, 20))
    return g


def gate_stage(prev, st):
    s = []
    if _on(prev, st, "ring"):
        for x in GT["arch"]:
            s.append(_waves(x, GT["floor"] - GT["ah"] - 10, -90, 3, 26, J.ALERT))
    if _on(prev, st, "wand"):
        wx, wy = GT["wand"]
        s.append(F.rect(wx - 26, wy - 98, 52, 216, "none", J.AMBER, 5, rx=18))
    if _on(prev, st, "pass_"):        # 🔴 試し焼き ep21_b3：欄の名を "pass" で見ていた＝通過の矢印が出なかった
        y = GT["floor"] - 60
        s.append(_arrow(GT["arch"][-1] + GT["aw"] / 2 + 10, y, GT["exit"][1], y, J.AMBER, 7, 28))
        s.append(F.txtfit((GT["exit"][0] + GT["exit"][1]) / 2, y - 40, "通過", 300, cap=36, col=J.AMBER, anchor="middle"))
    return s


# ══════════════════════════════════════════════════════════
#  blade（c212・c213）＝刃渡りの物差し（4インチ＝10.16センチ）
# ══════════════════════════════════════════════════════════
BL = dict(x0=420.0, cm=78.0, y=700.0, knife_y=560.0, blade_cm=8.5)
BL_LIMIT_IN = 4.0                                  # 委員会報告 p84「knives with blades under 4 inches long」
BL_IN_CM = 2.54


def bl_x(cm):
    return BL["x0"] + BL["cm"] * cm


def blade_base(st0):
    g = [F.rect(bl_x(0) - 20, BL["y"] - 30, bl_x(12) - bl_x(0) + 40, 60, COL["panel"], J.LINE, 3, rx=6)]
    for c in range(13):
        x = bl_x(c)
        g.append(F.line(x, BL["y"] - 30, x, BL["y"] - (6 if c % 5 else -6), INK, 3))
        if c % 5 == 0:
            g.append(F.txt(x, BL["y"] + 66, f"{c}", 30, J.TICK, "Noto", "middle"))
    g.append(F.txt(bl_x(12) + 40, BL["y"] + 66, "センチ", 28, J.TICK, "Noto", "start"))
    # 刃物の影（刃＝0〜blade_cm・柄は左）。人は描かない
    y, L = BL["knife_y"], BL["blade_cm"]
    blade = [(bl_x(0), y - 22), (bl_x(L * 0.85), y - 22), (bl_x(L), y), (bl_x(0), y + 16)]
    g.append(F.poly(blade, COL["metal"], COL["body_ln"], 3, close=True))
    g.append(F.rect(bl_x(0) - 210, y - 26, 200, 48, COL["door"], COL["body_ln"], 3, rx=12))
    g.append(F.line(bl_x(0), y + 44, bl_x(L), y + 44, J.LINE, 3))
    g.append(F.txtfit((bl_x(0) + bl_x(L)) / 2, y + 86, "刃渡り", 260, cap=28, col=J.TICK, anchor="middle"))
    return g


def blade_stage(prev, st):
    s = []
    if _on(prev, st, "limit"):
        x = bl_x(BL_LIMIT_IN * BL_IN_CM)
        s.append(F.line(x, 380, x, BL["y"] + 34, J.AMBER, 6, dash="14 10"))
        s.append(F.txtfit(x, 360, "4インチ（10.16センチ）", 520, cap=34, col=J.AMBER, anchor="middle"))
    if _on(prev, st, "ok"):
        s.append(_check(bl_x(BL["blade_cm"] / 2), BL["knife_y"] - 90, 30))
    for i in (1, 2, 3):
        if _on(prev, st, f"r{i}"):
            s.append(F.circ(L_X + 26, 296 + 62 * (i - 1), 22, "none", J.AMBER, 4))
            s.append(F.txt(L_X + 26, 296 + 62 * (i - 1) + 11, str(i), 30, J.AMBER, "Noto", "middle"))
    return s


# ══════════════════════════════════════════════════════════
#  tools（c214）＝刃物・スプレー・「爆弾」
# ══════════════════════════════════════════════════════════
TL = dict(knife=(470.0, 560.0), spray=(960.0, 560.0), bomb=(1450.0, 560.0))
TL_NAMES = dict(knife="刃物", spray="刺激性のスプレー", bomb="「爆弾がある」")      # ⚠️ 門番 echo：「目や喉を刺激するスプレー」は語りの写し


def tools_base(st0):
    return []


def tools_stage(prev, st):
    s = []
    if _on(prev, st, "knife"):
        x, y = TL["knife"]
        s.append(F.poly([(x - 150, y - 18), (x + 60, y - 18), (x + 120, y + 6), (x - 150, y + 14)], COL["metal"], COL["body_ln"], 3, close=True))
        s.append(F.rect(x - 290, y - 22, 140, 42, COL["door"], COL["body_ln"], 3, rx=12))
        s.append(F.txtfit(x - 80, y + 150, TL_NAMES["knife"], 360, cap=34, col=INK, anchor="middle"))
    if _on(prev, st, "spray"):
        x, y = TL["spray"]
        s.append(F.rect(x - 46, y - 80, 92, 200, COL["panel"], J.LINE, 4, rx=16))
        s.append(F.rect(x - 22, y - 120, 44, 40, COL["metal"], J.LINE, 3, rx=6))
        s.append(F.rect(x - 4, y - 132, 40, 14, COL["metal"], J.LINE, 2, rx=4))
        s.append(F.txtfit(x, y + 150, TL_NAMES["spray"], 440, cap=32, col=INK, anchor="middle"))
    if _on(prev, st, "bomb"):
        x, y = TL["bomb"]
        s.append(F.rect(x - 110, y - 70, 220, 150, COL["panel"], J.LINE, 4, rx=10))
        s.append(F.line(x + 60, y - 70, x + 100, y - 130, J.LINE, 4))
        s.append(_qmark(x, y + 10, 80))
        s.append(F.txtfit(x, y + 150, TL_NAMES["bomb"], 440, cap=32, col=INK, anchor="middle"))
    if _on(prev, st, "fake"):
        x, y = TL["bomb"]
        s.append(F.rect(x - 150, y - 110, 300, 230, "none", J.DOC, 6, rx=12, dash="18 10"))
        s.append(F.txtfit(x, y - 140, "おそらく偽物", 360, cap=40, col=J.DOC, anchor="middle"))
    return s


# ══════════════════════════════════════════════════════════
#  door（c215・c306〜c308）＝操縦室の扉（正面）
# ══════════════════════════════════════════════════════════
DR = dict(wall=(700.0, 300.0, 1220.0, 840.0), door=(830.0, 360.0, 1090.0, 840.0), lock=(1050.0, 610.0))
DR_OPEN = 0.30                                     # 開いた扉の見かけの幅（閉じた幅の割合・模式）


def door_base(st0):
    x0, y0, x1, y1 = DR["wall"]
    g = [F.rect(x0, y0, x1 - x0, y1 - y0, COL["panel"], J.LINE_DIM, 4, rx=6)]
    dx0, dy0, dx1, dy1 = DR["door"]
    g.append(F.rect(dx0, dy0, dx1 - dx0, dy1 - dy0, COL["dark"], None))
    g.append(F.txtfit((x0 + x1) / 2, y0 - 20, "操縦室の扉（客室の側から）", 600, cap=28, col=J.TICK, anchor="middle"))
    return g


def door_parts(st):
    """扉の板と、板に付いた物（金庫の枠・輪・鍵）。開くと板ごと蝶番の側（左）へ縮む＝付いた物も同じ式で縮める
    （⚠️ 試し焼き ep21_b3：輪と鍵を薄めて消す作りだと、開いた所に半ば消えた輪と鍵が浮いて残った＝c307 の最後のコマ）"""
    dx0, dy0, dx1, dy1 = DR["door"]
    k = DR_OPEN if st["door"] == "open" else 1.0
    sk = 26.0 if st["door"] == "open" else 0.0
    w0 = dx1 - dx0

    def P(x, y):
        u = (x - dx0) / w0                                  # 蝶番からの割合（0＝蝶番・1＝取っ手の側）
        return (dx0 + (x - dx0) * k, y + sk * u * (1 if y < (dy0 + dy1) / 2 else -1))
    panel = [P(dx0, dy0), P(dx1, dy0), P(dx1, dy1), P(dx0, dy1)]
    vault = [P(dx0 + 10, dy0 + 10), P(dx1 - 10, dy0 + 10), P(dx1 - 10, dy1 - 10), P(dx0 + 10, dy1 - 10)]
    cx, cy = (dx0 + dx1) / 2, (dy0 + dy1) / 2
    wheel = [P(cx + 54 * math.cos(2 * math.pi * i / 24), cy + 54 * math.sin(2 * math.pi * i / 24)) for i in range(24)]
    lx, ly = DR["lock"]
    up = -18.0 if st["lock"] == "open" else 0.0
    lk_a = 1.0 if st["lock"] in ("on", "open") else 0.0
    va = 1.0 if st["vault"] == "on" else 0.0
    return [_P("panel", "poly", panel, fill=COL["door"], stroke=COL["door_ln"], w=4),
            _P("vault", "poly", vault, fill=None, stroke=J.LINE, w=14, alpha=va),
            _P("wheel", "poly", wheel, fill=None, stroke=J.LINE, w=10, alpha=va),
            _P("lk_body", "poly", [P(lx - 30, ly), P(lx + 30, ly), P(lx + 30, ly + 50), P(lx - 30, ly + 50)], fill=J.AMBER,
               stroke=COL["dark"], w=3, alpha=lk_a),
            _P("lk_shk", "line", [P(lx - 18, ly + up), P(lx - 18, ly - 26 + up), P(lx + 18, ly - 26 + up), P(lx + 18, ly - 8 + up)],
               stroke=J.AMBER, w=8, alpha=lk_a)]


def door_stage(prev, st):
    s = []
    if _on(prev, st, "loose"):
        lx, ly = DR["lock"]
        s.append(_qmark(lx + 110, ly + 20, 64))
    if _on(prev, st, "comply"):
        s.append(_box(370.0, 600.0, 330, 90, "要求に従う", J.DOC, cap=34))
        s.append(_arrow(540.0, 600.0, DR["door"][0] - 16, 600.0, J.DOC, 7, 28))
    return s


# ══════════════════════════════════════════════════════════
#  old（c303〜c305）＝昔ながらの乗っ取り（3つの箱）
# ══════════════════════════════════════════════════════════
OL = dict(y=430.0, w=470.0, h=96.0, xs=(340.0, 960.0, 1580.0), y4=790.0)   # y4＝「暴力が起きたら」の段（「長引くほど」の字 y 690 の下）
OL_T = ("犯人の要求をのむ", "機を無事に着陸させる", "警察や軍に任せる")


def old_base(st0):
    return []


def old_stage(prev, st):
    s = []
    for i, f in enumerate(("b1", "b2", "b3")):
        if _on(prev, st, f):
            s.append(_box(OL["xs"][i], OL["y"], OL["w"], OL["h"], OL_T[i], J.LINE, cap=36))
            if i > 0:
                s.append(_arrow(OL["xs"][i - 1] + OL["w"] / 2 + 8, OL["y"], OL["xs"][i] - OL["w"] / 2 - 8, OL["y"], J.LINE, 6, 24))
    if _on(prev, st, "chips"):
        for j, t in enumerate(("亡命", "仲間の釈放")):
            x = OL["xs"][0] - 110 + 220 * j
            s.append(_box(x, OL["y"] + 120, 190, 60, t, J.INST, cap=28))
    if _on(prev, st, "long"):
        y = OL["y"] + 210
        s.append(_arrow(OL["xs"][0] - OL["w"] / 2, y, OL["xs"][2] + OL["w"] / 2, y, J.TICK, 5, 24))
        s.append(F.txtfit(960.0, y + 50, "長いほど穏やかに終わる（とされた）", 1100, cap=32, col=J.TICK, anchor="middle"))   # ⚠️ 門番 echo
    if _on(prev, st, "b4"):
        y = OL["y4"]
        s.append(_box(560.0, y, 520, 96, "暴力が起きたら", J.ALERT, cap=36))
        s.append(_arrow(830.0, y, 950.0, y, J.TICK, 5, 22))
        s.append(F.rect(970.0, y - 48, 560, 96, "none", J.TICK, 4, rx=10, dash="16 12"))
    return s


# ══════════════════════════════════════════════════════════
#  chain（c311・c312・c314・c413・c414・c425）＝手順の段（委員会報告 p17・p18 の順）
# ══════════════════════════════════════════════════════════
CH_ORDER = ("ctl", "sup", "hq", "nmcc", "osd", "norad", "ftr")
CH_XY = dict(ctl=(230.0, 700.0), sup=(470.0, 605.0), hq=(710.0, 510.0), nmcc=(950.0, 415.0), osd=(1190.0, 320.0),
             norad=(1430.0, 430.0), ftr=(1650.0, 540.0))
CH_W, CH_H = 300.0, 64.0
CH_NAMES = dict(ctl=dict(gen="管制官", bos="ボストン・センター"), sup="上司", hq="FAA の本部", nmcc="国防総省の指揮所",
                osd="国防長官の許し", norad="NORAD", ftr="戦闘機")
CH_SIDE = dict(cape=(560.0, 815.0), mil=(960.0, 815.0), ac=(330.0, 410.0))
CH_SIDE_W = dict(cape=360.0, mil=300.0, ac=420.0)
CH_SIDE_T = dict(cape="ケープコッドの FAA の施設", mil="軍", ac=("アトランティックシティ", "（昔の待機の基地）"))   # ⚠️ 門番 echo：1行だと語りの写し
CH_ESC = (1300.0, 650.0, 1840.0, 852.0)            # 後ろの戦闘機の小窓（c314）
LIT = tuple(str(i) for i in range(8))


def ch_name(k, who):
    n = CH_NAMES[k]
    return n[who] if isinstance(n, dict) else n


def _edge(a, b):
    (ax, ay), (bx, by) = CH_XY[a], CH_XY[b]
    up = by < ay
    x1, y1 = ax + CH_W / 2 - 40, (ay - CH_H / 2 if up else ay + CH_H / 2)
    x2, y2 = bx - CH_W / 2 + 40, (by + CH_H / 2 if up else by - CH_H / 2)
    return x1, y1, x2, y2


def chain_base(st0):
    g = []
    for a, b in zip(CH_ORDER, CH_ORDER[1:]):
        x1, y1, x2, y2 = _edge(a, b)
        g.append(_arrow(x1, y1, x2, y2, J.LINE_DIM, 5, 20))
    for k in CH_ORDER:
        x, y = CH_XY[k]
        col = J.INST if k in ("nmcc", "osd", "norad", "ftr") else J.LINE
        g.append(_box(x, y, CH_W, CH_H, ch_name(k, st0["who"]), col, cap=30))
    return g


def chain_parts(st):
    n = int(st["lit"])
    out = []
    for i, k in enumerate(CH_ORDER):
        x, y = CH_XY[k]
        on = i < n or (k == "norad" and st["norad"] == "on")
        out.append(_P(f"hl_{k}", "poly", [(x - CH_W / 2 - 8, y - CH_H / 2 - 8), (x + CH_W / 2 + 8, y - CH_H / 2 - 8),
                                          (x + CH_W / 2 + 8, y + CH_H / 2 + 8), (x - CH_W / 2 - 8, y + CH_H / 2 + 8)],
                      fill=None, stroke=J.AMBER, w=6, alpha=(1.0 if on else 0.0)))
    for i, (a, b) in enumerate(zip(CH_ORDER, CH_ORDER[1:])):
        x1, y1, x2, y2 = _edge(a, b)
        out.append(_P(f"ar_{a}", "line", [(x1, y1), (x2, y2)], stroke=J.AMBER, w=6, head=20, alpha=(1.0 if i + 1 < n else 0.0)))
    return out


def chain_stage(prev, st):
    s = []
    cx, cy = CH_XY["ctl"]
    if _on(prev, st, "short"):
        mx, my = CH_SIDE["mil"]
        s.append(F.poly([(cx, cy + CH_H / 2), (cx, my), (mx - CH_SIDE_W["mil"] / 2 - 26, my)], "none", J.AMBER, 6, dash="16 10"))
        s.append(F.poly([(mx - CH_SIDE_W["mil"] / 2 - 2, my), (mx - CH_SIDE_W["mil"] / 2 - 30, my - 14), (mx - CH_SIDE_W["mil"] / 2 - 30, my + 14)],
                        J.AMBER, close=True))
        s.append(_box(mx, my, CH_SIDE_W["mil"], CH_H, CH_SIDE_T["mil"], J.INST, cap=30))
    if _on(prev, st, "cape"):
        x, y = CH_SIDE["cape"]
        s.append(_box(x, y, CH_SIDE_W["cape"], CH_H, CH_SIDE_T["cape"], J.AMBER, cap=28))
    if _on(prev, st, "ac"):
        x, y = CH_SIDE["ac"]
        s.append(_arrow(cx - 20, cy - CH_H / 2, x - 40, y + (CH_H + 40) / 2 + 6, J.LINE, 5, 20, dash="12 10"))
        s.append(_box(x, y, CH_SIDE_W["ac"], CH_H + 40, CH_SIDE_T["ac"][0], J.LINE, cap=26, t2=CH_SIDE_T["ac"][1]))
    if _on(prev, st, "ac", "x"):
        x, y = CH_SIDE["ac"]
        s.append(_xmark(x + CH_SIDE_W["ac"] / 2 - 10, y - (CH_H + 40) / 2 + 4, 24))
    if _on(prev, st, "hqx"):
        x1, y1, x2, y2 = _edge("hq", "nmcc")
        s.append(_xmark((x1 + x2) / 2, (y1 + y2) / 2, 28))
    if _on(prev, st, "esc"):
        x0, y0, x1, y1 = CH_ESC
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG, J.LINE_DIM, 3, rx=8))
        s.append(_plane_top(x1 - 120, (y0 + y1) / 2, 150))
        s.append(_plane_top(x0 + 90, (y0 + y1) / 2, 70, col=COL["metal"], fighter=True))
        s.append(F.line(x0 + 135, y1 - 34, x1 - 205, y1 - 34, J.AMBER, 3, dash="10 8"))
        s.append(F.txtfit((x0 + x1) / 2, y0 + 34, "後ろから見守る", x1 - x0 - 30, cap=26, col=J.TICK, anchor="middle"))
    return s


# ══════════════════════════════════════════════════════════
#  escort（c313）＝乗っ取られた機と後ろの戦闘機（上から・進む向きが右）
# ══════════════════════════════════════════════════════════
ES = dict(plane=(1330.0, 560.0), fighter=(470.0, 560.0), near=(1500.0, 420.0), Lp=420.0, Lf=150.0)   # ⚠️ 試し焼き：near (1330, 380) は主翼に重なった
ES_MILES = 5                                       # 委員会報告 p18「five miles directly behind the hijacked aircraft」
ES_KM = round(ES_MILES * 1.609344)                  # ＝8（台本 §9）


def escort_base(st0):
    x, y = ES["plane"]
    return [_plane_top(x, y, ES["Lp"]), F.txtfit(x, y + 250, "乗っ取られた機", 400, cap=30, col=J.TICK, anchor="middle"),   # ⚠️ y+210 は翼の先に触れた
            _arrow(x + ES["Lp"] / 2 + 30, y, x + ES["Lp"] / 2 + 120, y, J.LINE_DIM, 6, 24)]


def escort_stage(prev, st):
    s = []
    if _on(prev, st, "fighter"):
        x, y = ES["fighter"]
        s.append(_plane_top(x, y, ES["Lf"], col=COL["metal"], fighter=True))
        s.append(F.txtfit(x, y + 130, "戦闘機", 300, cap=30, col=J.TICK, anchor="middle"))
    if _on(prev, st, "dim"):
        y = 760.0
        xa, xb = ES["fighter"][0] + ES["Lf"] / 2 + 10, ES["plane"][0] - ES["Lp"] / 2 - 10
        s += [F.line(xa, y, xb, y, J.AMBER, 4), F.line(xa, y - 16, xa, y + 16, J.AMBER, 4), F.line(xb, y - 16, xb, y + 16, J.AMBER, 4)]
    if _on(prev, st, "near"):
        x, y = ES["near"]
        s.append(_plane_top(x, y, ES["Lf"], col=J.TICK, fighter=True, dash="10 8"))
        s.append(_xmark(x, y, 34))
    return s


# ══════════════════════════════════════════════════════════
#  premise（c315・c316・c426）＝手順の3つの前提（委員会報告 p18）
# ══════════════════════════════════════════════════════════
PM = dict(y=540.0, w=500.0, h=250.0, xs=(340.0, 960.0, 1580.0))
PM_T = (("すぐに見分けがつき、", "姿を消そうとしない"), ("指揮の段を順に", "上がる時間がある"), ("昔ながらの乗っ取り", "（ミサイルにしない）"))


def premise_base(st0):
    g = []
    for i, _ in enumerate(PM_T):
        x, y = PM["xs"][i], PM["y"]
        g.append(F.rect(x - PM["w"] / 2, y - PM["h"] / 2, PM["w"], PM["h"], J.BG2, J.LINE, 4, rx=12))
        g.append(F.circ(x, y - PM["h"] / 2 - 56, 34, J.BG2, J.LINE, 4))          # ⚠️ geom_gap：枠に乗せると番号の字が枠の線に触れた＝上へ
        g.append(F.txt(x, y - PM["h"] / 2 - 42, str(i + 1), 40, J.INK_W, "Noto", "middle"))
        g.append(F.txtfit(x, y + 4, PM_T[i][0], PM["w"] - 50, cap=36, col=INK, anchor="middle"))
        g.append(F.txtfit(x, y + 56, PM_T[i][1], PM["w"] - 50, cap=36, col=INK, anchor="middle"))
    return g


def premise_parts(st):
    out = []
    for i, _ in enumerate(PM_T):
        x, y = PM["xs"][i], PM["y"]
        on = st[f"p{i + 1}"] == "on"
        out.append(_P(f"hl{i + 1}", "poly", [(x - PM["w"] / 2 - 10, y - PM["h"] / 2 - 10), (x + PM["w"] / 2 + 10, y - PM["h"] / 2 - 10),
                                           (x + PM["w"] / 2 + 10, y + PM["h"] / 2 + 10), (x - PM["w"] / 2 - 10, y + PM["h"] / 2 + 10)],
                      fill=None, stroke=J.AMBER, w=7, alpha=1.0 if on else 0.0))
    return out


def premise_stage(prev, st):
    s = []
    if _on(prev, st, "x1"):
        # ⚠️ geom_gap：大きな×を字に重ねると読めない＝枠を赤く・右上の角に×（字には重ねない）
        x, y = PM["xs"][0], PM["y"]
        s.append(F.rect(x - PM["w"] / 2 - 4, y - PM["h"] / 2 - 4, PM["w"] + 8, PM["h"] + 8, "none", J.ALERT, 9, rx=14))
        s.append(_xmark(x + PM["w"] / 2 - 6, y - PM["h"] / 2 + 6, 30, J.ALERT, 11))
    return s


# ══════════════════════════════════════════════════════════
#  cabin（c310・c403）＝上から見た機内（機首が左）。座席の並び 2-3-2・操縦室の扉（形は模式）
# ══════════════════════════════════════════════════════════
CB = dict(all=dict(K=29.0, X0=250.0), front=dict(K=60.0, X0=180.0))   # front＝前の部分に寄る（胴の幅 300px＝上に札の段が残る）
CB_Y = 560.0
CB_LEN, CB_W = 48.0, 5.0                      # 機の長さ・胴の幅（m・模式）
CB_DOOR = 4.2                                  # 操縦室の扉（機首から m・模式）
CB_ROWS = (6.0, 44.0, 0.86)                    # 座席の列の始め・終わり・間隔（m・模式）
CB_SEATS = (2, 3, 2)                           # 横の並び（ボーイング767 の普通席の形＝模式）


def cb_x(zoom, m):
    return CB[zoom]["X0"] + CB[zoom]["K"] * m


def cabin_base(st0):
    z = st0["zoom"]
    K = CB[z]["K"]
    hw = CB_W / 2 * K
    x0, x1 = cb_x(z, 0), cb_x(z, CB_LEN)
    xr = min(x1, F.BX1 - 20)
    body = [(x0, CB_Y), (x0 + 3.5 * K, CB_Y - hw), (xr, CB_Y - hw), (xr, CB_Y + hw), (x0 + 3.5 * K, CB_Y + hw)]
    g = [F.poly(body, J.BG2, J.LINE, 4, close=True)]
    dx = cb_x(z, CB_DOOR)
    g.append(F.line(dx, CB_Y - hw, dx, CB_Y + hw, J.AMBER if z == "front" else J.LINE, 6))
    g.append(F.txtfit((x0 + dx) / 2 + 10, CB_Y - hw - 22, "操縦室", 300, cap=28, col=J.TICK, anchor="middle"))
    a, b, p = CB_ROWS
    n = int((b - a) / p) + 1
    seat = 0.42 * p
    col_w = CB_W / (sum(CB_SEATS) + 2)
    for r in range(n):
        m = a + r * p
        x = cb_x(z, m)
        if x > F.BX1 - 40:
            break
        yy = -CB_W / 2 + col_w * 0.5
        for gi, k in enumerate(CB_SEATS):
            for _ in range(k):
                g.append(F.rect(x, CB_Y + yy * K, seat * K, col_w * 0.8 * K, COL["seat"]))
                yy += col_w
            yy += col_w * 0.5 if gi < len(CB_SEATS) - 1 else 0
    g.append(F.txtfit(cb_x(z, (a + min(b, (F.BX1 - CB[z]["X0"]) / K)) / 2), CB_Y + hw + 44, "客室（座席）", 400, cap=28, col=J.TICK,
                      anchor="middle"))
    return g


def cabin_stage(prev, st):
    s = []
    z = st["zoom"]
    K = CB[z]["K"]
    hw = CB_W / 2 * K
    if _on(prev, st, "legend"):
        x, y = 1180.0, 330.0
        s.append(F.rect(x, y - 24, 36, 36, "none", J.AMBER, 5, rx=6, dash="8 6"))
        s.append(F.txtfit(x + 56, y + 6, "連邦航空保安官の席", 520, cap=30, col=INK))
        s.append(F.txtfit(x + 56, y + 50, "（この並びに印は無い）", 520, cap=26, col=J.TICK))
    if _on(prev, st, "doorq"):
        dx = cb_x(z, CB_DOOR)
        s.append(_qmark(dx, CB_Y - hw - 70, 72))
    return s


# ══════════════════════════════════════════════════════════
#  phone（c404〜c406）＝機内の電話から地上の窓口へ（人は描かない）
# ══════════════════════════════════════════════════════════
PH = dict(x0=520.0, y0=470.0, L=980.0, office=(1500.0, 770.0))   # ⚠️ y0 420 だと尾翼の先が y 215＝上の帯に近い


def ph_geo():
    svg, ck, cab, _ = _plane_side(PH["x0"], PH["y0"], PH["L"])
    return svg, ck, cab


def phone_base(st0):
    svg, ck, cab = ph_geo()
    ox, oy = PH["office"]
    return [svg, F.line(F.BX0 + 40, 850, F.BX1 - 40, 850, J.LINE_DIM, 3), _building(ox, oy, 240, 140, J.INST),
            F.txtfit(ox - 140, oy + 6, "航空会社の予約の窓口", 380, cap=28, col=J.TICK, anchor="end")]


def phone_stage(prev, st):
    s = []
    _, ck, cab = ph_geo()
    ox, oy = PH["office"]
    if _on(prev, st, "call"):
        s.append(F.poly([cab, (cab[0], 640.0), (ox - 60, 640.0), (ox - 60, oy - 70)], "none", J.AMBER, 6, dash="16 10"))
        s.append(F.circ(cab[0], cab[1], 12, J.AMBER))
    if _on(prev, st, "ckq"):
        s.append(_qmark(ck[0], ck[1] - 96, 64))
    if _on(prev, st, "dur"):
        y = 640.0
        s += [F.line(cab[0] + 40, y + 34, ox - 100, y + 34, J.AMBER, 4), F.line(cab[0] + 40, y + 20, cab[0] + 40, y + 48, J.AMBER, 4),
              F.line(ox - 100, y + 20, ox - 100, y + 48, J.AMBER, 4)]
    if _on(prev, st, "train"):
        s.append(F.line(cab[0] - 20, cab[1] + 34, ck[0] + 30, ck[1] + 34, J.DOC, 5, dash="12 10"))
    if _on(prev, st, "train", "x"):
        s.append(_xmark((cab[0] + ck[0]) / 2, cab[1] + 34, 26))
    return s


# ══════════════════════════════════════════════════════════
#  radio（c409〜c411）＝管制の無線（ボストン・センター ↔ 11便）
# ══════════════════════════════════════════════════════════
RD = dict(x0=980.0, y0=420.0, L=760.0, ctr=(420.0, 740.0))


def rd_geo():
    svg, ck, cab, top = _plane_side(RD["x0"], RD["y0"], RD["L"])
    return svg, ck, cab, top


def radio_base(st0):
    svg, ck, cab, top = rd_geo()
    cx, cy = RD["ctr"]
    return [svg, F.line(F.BX0 + 40, cy + 70, F.BX1 - 40, cy + 70, J.LINE_DIM, 3), _building(cx, cy, 240, 140, J.LINE),   # ⚠️ 地面の線 y 850 が札に触れた
            F.txtfit(cx, cy + 108, "ボストン・センター（管制）", 460, cap=28, col=J.TICK, anchor="middle"),
            F.line(ck[0], ck[1] - 50, cx + 67, cy - 120, J.LINE_DIM, 3, dash="6 10")]


def radio_stage(prev, st):
    s = []
    _, ck, cab, top = rd_geo()
    cx, cy = RD["ctr"]
    ax, ay = ck[0], ck[1] - 50
    ang = math.degrees(math.atan2((cy - 120) - ay, (cx + 67) - ax))
    if _on(prev, st, "v1"):
        s.append(F.line(ax, ay, cx + 67, cy - 120, J.AMBER, 5))
        s.append(_waves(ax - 30, ay + 20, ang, 3, 30))
    if _on(prev, st, "pa"):
        px, py = cab[0] + 60, cab[1] + 100
        s.append(F.rect(px - 22, py - 22, 44, 44, COL["panel"], J.DOC, 4, rx=6))
        s.append(F.poly([(px + 22, py - 12), (px + 44, py - 30), (px + 44, py + 30), (px + 22, py + 12)], J.DOC, close=True))
        s.append(_arrow(ck[0] + 40, ck[1] + 40, px - 30, py, J.DOC, 4, 18, dash="10 8"))
    if _on(prev, st, "garble"):
        s.append(_qmark(cx - 150, cy - 110, 72))
    if _on(prev, st, "v2"):
        s.append(_waves(ax - 30, ay + 20, ang, 3, 110))
    if _on(prev, st, "know"):
        s.append(F.rect(cx - 140, cy - 95, 280, 150, "none", J.AMBER, 6, rx=12))      # ⚠️ 試し焼き：下の辺が建物の札に重なった
    return s


# ══════════════════════════════════════════════════════════
#  call（c415〜c417）＝電話の線（ボストン・センター → NEADS）
# ══════════════════════════════════════════════════════════
CA = dict(left=(420.0, 640.0), right=(1500.0, 640.0), y=560.0)


def call_base(st0):
    (lx, ly), (rx, ry) = CA["left"], CA["right"]
    return [F.line(F.BX0 + 40, 850, F.BX1 - 40, 850, J.LINE_DIM, 3), _building(lx, ly, 260, 150, J.LINE), _building(rx, ry, 260, 150, J.INST),
            F.txtfit(lx, ly + 120, "ボストン・センター（FAA）", 480, cap=28, col=J.TICK, anchor="middle"),
            F.txtfit(rx, ry + 120, "NEADS（軍の北東部の防空）", 480, cap=28, col=J.TICK, anchor="middle")]


def call_stage(prev, st):
    s = []
    (lx, _), (rx, _) = CA["left"], CA["right"]
    y = CA["y"]
    xa, xb = lx + 150, rx - 150
    if _on(prev, st, "link"):
        s.append(F.line(xa, y, xb, y, J.AMBER, 6))
        s += [F.circ(xa, y, 10, J.AMBER), F.circ(xb, y, 10, J.AMBER)]
    if _on(prev, st, "talk", "ask"):
        s.append(_arrow(xa + 120, y - 40, xb - 220, y - 40, J.AMBER, 6, 26))
    if _on(prev, st, "talk", "back"):
        s.append(_arrow(xb - 120, y + 40, xa + 220, y + 40, J.INST, 6, 26))
        s.append(_qmark(xb - 70, y + 50, 52, J.INST))
    if _on(prev, st, "drill"):
        x, yy = rx, 300.0
        s.append(F.rect(x - 230, yy - 50, 460, 120, J.BG2, J.DOC, 4, rx=8))
        s.append(F.txtfit(x, yy - 4, "演習の予定", 420, cap=32, col=J.DOC, anchor="middle"))
        s.append(F.txtfit(x, yy + 44, "旧ソ連の爆撃機の想定", 420, cap=28, col=INK, anchor="middle"))
    return s


# ══════════════════════════════════════════════════════════
#  scope（c407・c420・c424）＝レーダーの画面（点と、便名・高度の札）
# ══════════════════════════════════════════════════════════
SC = dict(c=(760.0, 560.0), r=280.0, blip=(850.0, 480.0), block=(905.0, 395.0, 1075.0, 455.0))
SC_LAB = dict(faa="管制のレーダーの画面", neads="NEADS のレーダーの画面")
SC_DOTS = ((640, 440), (700, 690), (580, 600), (830, 640), (900, 520), (760, 380), (620, 740), (950, 700), (540, 470),
           (880, 360), (690, 520), (980, 600), (600, 360), (820, 770), (720, 300), (500, 560), (940, 440), (1010, 520))
SC_SEARCH = ((650, 470), (820, 650), (930, 470), (700, 560))       # 探す輪の通り道（段ごと・模式）


def scope_base(st0):
    (cx, cy), r = SC["c"], SC["r"]
    g = [F.circ(cx, cy, r, COL["scope"], COL["scope_ln"], 6)]
    for k in (1, 2):
        g.append(F.circ(cx, cy, r * k / 3, "none", COL["scope_ln"], 2))
    g += [F.line(cx - r, cy, cx + r, cy, COL["scope_ln"], 2), F.line(cx, cy - r, cx, cy + r, COL["scope_ln"], 2),
          F.line(cx, cy, cx + r * 0.71, cy - r * 0.71, COL["blip"], 3, op=0.6)]
    if st0["who"] == "faa":
        bx, by = SC["blip"]
        for i in range(1, 5):
            g.append(F.circ(bx - 22 * i, by + 14 * i, 4, COL["blip"], op=round(0.75 - 0.15 * i, 2)))
        g.append(F.circ(bx, by, 9, COL["blip"]))
        g.append(F.line(bx + 8, by - 8, SC["block"][0] - 4, SC["block"][3] - 6, COL["blip"], 2))
    return g


def scope_parts(st):
    x0, y0, x1, y1 = SC["block"]
    a = 1.0 if st["block"] == "on" else 0.0
    out = [_P("blk", "poly", [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill=COL["dark"], stroke=COL["block"], w=3, alpha=a),
           _P("blk_l1", "line", [(x0 + 14, y0 + 18), (x1 - 40, y0 + 18)], stroke=COL["block"], w=7, alpha=a),
           _P("blk_l2", "line", [(x0 + 14, y0 + 42), (x0 + 90, y0 + 42)], stroke=COL["block"], w=7, alpha=a),
           _P("blk_ld", "line", [(SC["blip"][0] + 8, SC["blip"][1] - 8), (x0 - 4, y1 - 6)], stroke=COL["blip"], w=2, alpha=a)]
    i = SC_STEP.index(st["search"])
    if i > 0:
        sx, sy = SC_SEARCH[i - 1]
    else:
        sx, sy = SC_SEARCH[0]
    out.append(_P("search", "circle", c=SC_SEARCH[0], r=48, fill=None, stroke=J.AMBER, w=6, alpha=(1.0 if i > 0 else 0.0),
                  dx=sx - SC_SEARCH[0][0], dy=sy - SC_SEARCH[0][1]))
    return out


SC_STEP = ("off", "s1", "s2", "s3", "s4")


def scope_stage(prev, st):
    s = []
    if _on(prev, st, "dots"):
        for x, y in SC_DOTS:
            s.append(F.circ(x, y, 7, COL["blip"]))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表・札の置き場・線の先
# ══════════════════════════════════════════════════════════
VIEWS = dict(
    us=dict(lab="北アメリカの地図（北が上）", fields=dict(east=ONOFF, west=ONOFF, routes=ONOFF), base=us_base, stage=us_stage),
    ne=dict(lab="アメリカ北東部の地図（北が上）", fields=dict(neads=ONOFF, bases=ONOFF, sea=ONOFF, dom=ONOFF, scr=ONOFF), base=ne_base,
            stage=ne_stage),
    gate=dict(lab="保安検査の流れ（横から）", fields=dict(ring=ONOFF, wand=ONOFF, pass_=ONOFF), base=gate_base, stage=gate_stage),
    blade=dict(lab="刃渡りの物差し", fields=dict(limit=ONOFF, ok=ONOFF, r1=ONOFF, r2=ONOFF, r3=ONOFF), base=blade_base, stage=blade_stage),
    tools=dict(lab="機内からの電話が伝えた道具", fields=dict(knife=ONOFF, spray=ONOFF, bomb=ONOFF, fake=ONOFF), base=tools_base,
               stage=tools_stage),
    door=dict(lab="操縦室の扉（正面）", fields=dict(lock=("off", "on", "open"), vault=ONOFF, door=("closed", "open"), loose=ONOFF,
                                                comply=ONOFF), base=door_base, stage=door_stage, parts=door_parts),
    old=dict(lab="昔ながらの乗っ取り（手引きの想定）", fields=dict(b1=ONOFF, b2=ONOFF, b3=ONOFF, chips=ONOFF, long=ONOFF, b4=ONOFF),
             base=old_base, stage=old_stage),
    chain=dict(lab="乗っ取りが分かったときの手順の段", fields=dict(who=("gen", "bos"), lit=LIT, norad=ONOFF, short=ONOFF, cape=ONOFF,
                                                         ac=("off", "on", "x"), hqx=ONOFF, esc=ONOFF),
               base=chain_base, stage=chain_stage, parts=chain_parts),
    escort=dict(lab="上から見た2機（進む向きが右）", fields=dict(fighter=ONOFF, dim=ONOFF, near=ONOFF), base=escort_base, stage=escort_stage),
    premise=dict(lab="手順の3つの前提", fields=dict(p1=ONOFF, p2=ONOFF, p3=ONOFF, x1=ONOFF), base=premise_base, stage=premise_stage,
                 parts=premise_parts),
    cabin=dict(lab="上から見た機内（機首が左）", fields=dict(zoom=("all", "front"), legend=ONOFF, doorq=ONOFF), base=cabin_base,
               stage=cabin_stage),
    phone=dict(lab="機内の電話と地上（横から）", fields=dict(call=ONOFF, ckq=ONOFF, dur=ONOFF, train=("off", "on", "x")), base=phone_base,
               stage=phone_stage),
    radio=dict(lab="管制の無線（横から）", fields=dict(v1=ONOFF, pa=ONOFF, garble=ONOFF, v2=ONOFF, know=ONOFF), base=radio_base,
               stage=radio_stage),
    call=dict(lab="電話の線", fields=dict(link=ONOFF, talk=("off", "ask", "back"), drill=ONOFF), base=call_base, stage=call_stage),
    scope=dict(lab="レーダーの画面", fields=dict(who=("faa", "neads"), block=ONOFF, dots=ONOFF, search=SC_STEP), base=scope_base,
               stage=scope_stage, parts=scope_parts),
)
START = dict(us=dict(east="off", west="off", routes="off"),
             ne=dict(neads="off", bases="off", sea="off", dom="off", scr="off"),
             gate=dict(ring="off", wand="off", pass_="off"),
             blade=dict(limit="off", ok="off", r1="off", r2="off", r3="off"),
             tools=dict(knife="off", spray="off", bomb="off", fake="off"),
             door=dict(lock="off", vault="off", door="closed", loose="off", comply="off"),
             old=dict(b1="off", b2="off", b3="off", chips="off", long="off", b4="off"),
             chain=dict(who="gen", lit="0", norad="off", short="off", cape="off", ac="off", hqx="off", esc="off"),
             escort=dict(fighter="off", dim="off", near="off"),
             premise=dict(p1="off", p2="off", p3="off", x1="off"),
             cabin=dict(zoom="all", legend="off", doorq="off"),
             phone=dict(call="off", ckq="off", dur="off", train="off"),
             radio=dict(v1="off", pa="off", garble="off", v2="off", know="off"),
             call=dict(link="off", talk="off", drill="off"),
             scope=dict(who="faa", block="off", dots="off", search="off"))
HEAD_ONLY = dict(chain=("who",), cabin=("zoom",), scope=("who",))
# 戻さない欄（消えた札は戻らない・×は戻らない・開いた扉は閉じない・灯した段は消えない）
ORDER = dict(door=dict(lock=("off", "on", "open"), door=("closed", "open")), chain=dict(lit=LIT, ac=("off", "on", "x")),
             phone=dict(train=("off", "on", "x")), call=dict(talk=("off", "ask", "back")), scope=dict(search=SC_STEP))
NOT_SCHEMATIC = ()

TAG_AT = dict(
    us=dict(east=(1470.0, 330.0, "start", 360.0), west=(L_X, 330.0, "start", 420.0)),
    ne=dict(neads=(L_X, 330.0, "start", 560.0), bases=(L_X, 430.0, "start", 560.0), sea=(1300.0, 330.0, "start", 520.0),
            dom=(L_X, 330.0, "start", 560.0), scr=(1300.0, 330.0, "start", 520.0), info=(L_X, 430.0, "start", 560.0)),
    # ⚠️ sea を (1300, 800) に置くと海の外から来る2本目の矢印の始まり（x 1506・y 797）に字が乗る＝上へ
    gate=dict(ring=(L_X, 330.0, "start", 520.0), pass_=(1300.0, 330.0, "start", 520.0)),
    blade=dict(r1=(L_X + 64, 307.0, "start", 640.0), r2=(L_X + 64, 369.0, "start", 640.0), r3=(L_X + 64, 431.0, "start", 640.0),
               ok=(1300.0, 470.0, "start", 520.0), rule=(1300.0, 560.0, "start", 520.0)),
    tools=dict(fake=(1220.0, 330.0, "end", 520.0)),
    door=dict(rule=(1290.0, 470.0, "start", 520.0), loose=(1290.0, 600.0, "start", 520.0), vault=(1290.0, 380.0, "start", 520.0),
              who=(L_X, 330.0, "start", 560.0), comply=(1290.0, 470.0, "start", 520.0)),
    old=dict(chips=(L_X, 330.0, "start", 640.0), why=(1240.0, 560.0, "start", 560.0), none=(1560.0, 798.0, "start", 280.0)),
    chain=dict(tl=(L_X, 300.0, "start", 520.0), br=(1300.0, 780.0, "start", 520.0), cape=(L_X, 830.0, "start", 110.0),
               hqx=(L_X, 330.0, "start", 520.0), ac=(620.0, 330.0, "start", 400.0)),     # ⚠️ ac の幅 520 だと国防長官の箱（x 1040〜）にかかる
    escort=dict(dim=(830.0, 820.0, "middle", 520.0), near=(1250.0, 300.0, "end", 520.0)),     # ⚠️ geom_gap：x 1400 の注の行が主翼の先に触れた
    premise=dict(x1=(L_X, 760.0, "start", 760.0)),
    cabin=dict(n33=(L_X, 330.0, "start", 640.0), none=(1240.0, 430.0, "start", 560.0), start=(1180.0, 300.0, "start", 620.0),
               how=(620.0, 300.0, "start", 520.0)),          # front の胴は y 410〜710＝札は上の段（y 300）
    phone=dict(time=(L_X, 330.0, "start", 520.0), dur=(1284.0, 724.0, "middle", 300.0), train=(L_X, 330.0, "start", 640.0),
               out=(1300.0, 600.0, "start", 520.0)),
    radio=dict(time=(L_X, 330.0, "start", 520.0), pa=(1330.0, 640.0, "start", 500.0), garble=(L_X, 330.0, "start", 520.0),
               v2=(L_X, 430.0, "start", 520.0), know=(L_X, 330.0, "start", 520.0)),
    call=dict(time=(960.0, 500.0, "middle", 520.0), first=(960.0, 760.0, "middle", 560.0), fast=(L_X, 330.0, "start", 760.0)),
    scope=dict(time=(1270.0, 330.0, "start", 520.0), block=(1270.0, 430.0, "start", 560.0), dot=(1270.0, 560.0, "start", 560.0),
               search=(1270.0, 430.0, "start", 560.0), news=(1270.0, 560.0, "start", 560.0)),
)


def anchors(view, st):
    """札から線を引く先（画面の点）。"""
    if view == "scope":
        x0, y0, x1, y1 = SC["block"]
        return dict(block=(x1 + 6, (y0 + y1) / 2), blip=(SC["blip"][0] + 12, SC["blip"][1]))
    if view == "ne":
        G = Geo("ne")
        return {k: G.px(*MAP_PTS[k]) for k in MAP_PTS}
    if view == "door":
        return dict(lock=(DR["lock"][0] + 34, DR["lock"][1] + 20), door=(DR["door"][2], 480.0))
    if view == "cabin":
        z = st["zoom"]
        return dict(door=(cb_x(z, CB_DOOR), CB_Y - CB_W / 2 * CB[z]["K"] - 10))
    if view == "chain":
        return {k: (CH_XY[k][0], CH_XY[k][1] - CH_H / 2) for k in CH_ORDER}
    return {}


def parts_of(view, st):
    fn = VIEWS[view].get("parts")
    return fn(st) if fn else []


def _states(view, start, steps):
    fields = VIEWS[view]["fields"]
    cur = dict(START[view], **(start or {}))
    out = []
    for i, st in enumerate([dict(state={})] + list(steps)):
        new = st.get("state") or {}
        for f_ in HEAD_ONLY.get(view, ()):
            if i > 0 and f_ in new:
                raise ValueError(f"m21：{f_} は頭（start）だけで決める")
        cur = dict(cur, **new)
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m21：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m21：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    for f_, seq in ORDER.get(view, {}).items():
        if f_ in fields:
            idx = [seq.index(s[f_]) for s in out]
            if any(b < a for a, b in zip(idx, idx[1:])):
                raise ValueError(f"m21：{f_} は戻さない（{' → '.join(seq)}）")
    return out[0], out[1:]


def stage_art(view, prev, st):
    return VIEWS[view]["stage"](prev, st)


def _base(view, st0):
    """基図＋頭の状態の層（頭で on にした欄は基図に描く＝前のカットの続き）"""
    pre = dict(START[view], **{k: st0[k] for k in HEAD_ONLY.get(view, ())})
    return VIEWS[view]["base"](st0) + stage_art(view, pre, st0)


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
                below_d = tg.get("d") and ty > y + round(c * 0.95)
                sy = y - round(c * 0.9) if ty < y - c else y + 8 + (round(c * 0.95) if below_d else 0)
                sx = x if anchor == "start" else (x - mw / 2 if anchor == "middle" else x)
                s.append(F.line(sx, sy, tx, ty, J.AMBER, 2))
            ol = 6 if view in ("us", "ne") else 0        # 地図の上の札は縁取り（陸の線を字の下で消す）
            s.append(F.txtfit(x, y, tg["t"], mw, cap=c, col=tg.get("col", J.AMBER), anchor=anchor, ol=ol))
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
    k0 = sh["keys"][0]
    if sh["type"] == "circle":
        return F.circ(sh["c"][0] + float(k0.get("dx", 0) or 0), sh["c"][1] + float(k0.get("dy", 0) or 0), sh["r"],
                      k0.get("fill", sh.get("fill")) or "none", k0.get("stroke", sh.get("stroke")), sh.get("w"))
    pts = F.mech_pts(sh, k0)
    if sh["type"] == "poly":
        return F.poly(pts, k0.get("fill", sh.get("fill")) or "none", k0.get("stroke", sh.get("stroke")), sh.get("w") or None, close=True,
                      op=(round(a, 2) if a < 0.99 else None))
    return F.poly(pts, "none", k0.get("stroke", sh.get("stroke")), sh.get("w"), op=(round(a, 2) if a < 0.99 else None))


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def m21(view, steps, start=None, rel=(), note="", src=""):
    """21本目の模式図。view は VIEWS の15種。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m21：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if "模式" not in note:
        raise ValueError("m21：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    seq = [st0] + states
    per = [parts_of(view, s) for s in seq]
    shapes, anim = [], []
    for j, p0 in enumerate(per[0]):
        keys = []
        for i, ps in enumerate(per):
            pj = ps[j]
            kk = {f_: pj[f_] for f_ in KEY_FIELDS if f_ in pj and pj[f_] is not None}
            kk.setdefault("alpha", 1.0)
            dl = 0.0 if i == 0 else float(steps[i - 1].get("delay", 1.0 if i == 1 else F.MECH_DELAY)) + float(p0.get("lag", 0.0))
            keys.append(dict(stage=max(0, i - 1), delay=dl, **kk))
        sh = {f_: p0[f_] for f_ in p0 if f_ not in ("alpha", "dx", "dy", "rot", "lag")}
        sh["keys"] = keys
        moving = any({f_: kk.get(f_) for f_ in KEY_FIELDS} != {f_: keys[0].get(f_) for f_ in KEY_FIELDS} for kk in keys[1:])
        sh["anim"] = bool(moving)
        shapes.append(sh)
        if moving:
            anim.append(sh)
    g = _base(view, st0)
    for sh in shapes:
        if not sh["anim"]:
            g.append(_static_part(sh))
    lab = SC_LAB[st0["who"]] if view == "scope" else VIEWS[view]["lab"]
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, lab + ("" if view in NOT_SCHEMATIC else "・模式"), 1000, cap=28, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, st0, states)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="m21", view=view, start=st0, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M21）
# ══════════════════════════════════════════════════════════
def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst])
    if view in ("us", "ne"):
        G = Geo(view)
        out["pts"] = {k: G.px(*v) for k, v in MAP_PTS.items()}
        out["back"] = {k: G.geo(*G.px(*v)) for k, v in MAP_PTS.items()}
        out["coast"] = len(coast())
        out["k"] = (G.kx * G.s, G.ky * G.s, G.latc)      # 経度1度・緯度1度の画素と中心の緯度（門番は自分の式で km あたりに直す）
        if view == "us":
            out["routes"] = [(a, b) for _, a, b in ROUTES]
            out["flights"] = {k: US_FLT[k] for k in US_FLT}
        else:
            out["bases"] = list(NE_BASES)
            out["neads"] = "rome"
    elif view == "gate":
        out["arches"] = len(GT["arch"])
    elif view == "blade":
        out["px_cm"] = BL["cm"]
        out["limit_x"] = bl_x(BL_LIMIT_IN * BL_IN_CM)
        out["zero_x"] = bl_x(0)
        out["blade_end_x"] = bl_x(BL["blade_cm"])
    elif view == "chain":
        out["order"] = [CH_NAMES[k] if not isinstance(CH_NAMES[k], dict) else CH_NAMES[k]["gen"] for k in CH_ORDER]
        out["xy"] = [CH_XY[k] for k in CH_ORDER]
    elif view == "escort":
        out["miles"] = ES_MILES
        out["km"] = ES_KM
        out["fighter_x"] = ES["fighter"][0]
        out["plane_x"] = ES["plane"][0]
    elif view == "premise":
        out["boxes"] = [" ".join(t) for t in PM_T]
    elif view == "cabin":
        out["seats"] = list(CB_SEATS)
    return out
