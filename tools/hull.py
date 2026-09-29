# -*- coding: utf-8 -*-
"""hull.py — 断面F「船の断面の動く模式図」（2026-09-29 新設・14本目 ⑤b-4）。

■ 何か（Vault `Projects/事故検証-14本目-映像方針-案Cと競合の画面-20260926.md` §2-2・追補 §4 の【F】の行）
  セウォル号の断面を、13本目の `section`（胴体の輪切り）と同じ「基図＋段の鍵で動く部品」で描く。
  案C の再現イラスト（絵）ではなく**図解**＝章の色の線と面・左上に見る向き・左下に「模式」と出典（§5b-10）。
  形のもとは海審の要目と構造の文（p1013・p1016〜p1020・p1038・p1042〜p1044）だけ。**写真はなぞらない**。**人は描かない**。
  🔴 数えられる形を描かない（車・箱を1台ずつ描かない）＝積み荷は面、種類は印を1つずつ（数ではない）。数は字幕（§5b-9）

■ 見え方（view）。🔴 見る向きの札を左上に必ず出す（§5b-80「高さは横から・場所は上から」の合図）
  side  … 横から見た断面（船首が右）。全体。改造・積み荷・船員の居場所
  stern … 同じ断面の船尾の寄り（改造の中身＝c402・c403・c414）
  hold  … 同じ断面の船体の下の寄り（底のタンクの水＝c409・c509）
  front … 船首の側から見た断面。傾き heel（度・左舷が下＝画面で時計回り＝案C の A と同じ向き）は段の鍵
  pair  … front を2隻並べる（c405 重心と復原力＝足す前と足したあと）
  port  … 3階と4階の左舷の外側を横から見た図（出入口・手すり・水位＝c817・c914）。傾きは描かない
          （🔴 手すりが水につかった時刻〈判決 p18〉と傾きの角度〈海審 p1057〉を1枚の傾いた断面に重ねると、
            どう描いても片方の記録と食い違う＝傾きを描かない見え方に分けた）

■ SPEC の書き方
  fig=("hull", dict(view="side", start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=… | m=(x, y)), …)],
                    rel=[dict(t="約5.6メートル", src="海審 p1016"), dict(heel=52.2, src="判決 p16")], note="模式…", src="…"))
  状態は前の段から引き継ぐ（書いた欄だけ変わる＝13本目 latch／section と同じ）。欄と値は下の FIELDS。
  段ごとの飾り（引き継がない・その段の層に焼く）：tag（札）・icon（積み荷の種類の印）・dim（長さ・幅・深さの矢印）
  🔴 札に出す数（メートル・度・人・分…）は `rel=` に同じ文字列で宣言（門番 check_mech ③）。傾き heel の0でない値も
     `rel=[dict(heel=値, src=…)]` で宣言（記録に無い傾きは src="模式" と書く＝黙って作らない）

■ 門番 `check_mech`（judge_hull）＝①状態の筋（記録）②本番の関数が置いた部品の画素（`titan_fig.mech_pts`）③札の数
  部品は**全部**この関数が組む（`parts_of`）＝描く側と門番が同じ幾何（[[feedback-gates-must-share-the-production-geometry]]）
"""
from __future__ import annotations

import math

import jiko_style as J
import titan_fig as F

# ══════════════════════════════════════════════════════════
#  形（メートル）。竜骨＝0（上が＋）・船尾＝0（船首が＋）
# ══════════════════════════════════════════════════════════
LOA, BEAM = 145.61, 22.00               # 全長・幅（海審 p1013）
HALF = BEAM / 2
D_Y = 7.67                              # D甲板＝竜骨から約7.67メートル（海審 p1019）
C_Y = D_Y + 6.33                        # ＝14.00＝深さ（p1013）。D甲板の天井 約5.1〜6.33（p1019）
B_Y = C_Y + 4.95                        # 3階（B甲板）の床。C甲板の天井 約4.2〜4.95（p1019）
A_Y = B_Y + 2.7                         # 4階（A甲板）。B甲板の天井 約2.7（p1019）
BR_Y = A_Y + 2.6                        # 5階（船橋甲板）。A甲板の天井 約2.6（p1018）
CMP_Y = BR_Y + 2.5                      # 屋上（コンパス甲板）。船橋甲板の天井 約2.5（p1018）
E_Y = 1.8                               # E甲板＝その下の天井 約1.5〜1.8（p1020）
TW_Y = B_Y - 2.2                        # トゥイーン甲板（天井 約2.2・長さ 約18.6＝p1019）
DRAFT = 6.20                            # 出港のときの喫水（海審 p1038 注14「약 6.20미터」）＝横から見た断面の水面
FR0, FR = 2.0, 0.7                      # 肋骨の番号 → 位置（間隔 0.7＝p1019 Fr.71〜136 が約45.5メートル。Fr.0 の位置は模式）
RAIL_H = 1.1                            # 手すりの高さ（記録に無い＝模式）
WALK = 1.5                              # 左舷の通路の幅（記録に無い＝模式）
# 🔴 記録に無い（模式）：部屋の前後の位置・長さ（下の X_ の多く）・通路の幅・手すりの高さ・船体の線の丸み


def frx(n):
    return FR0 + n * FR


# 🔴 船首の側から見た断面（front・pair）の水面＝**52.2度で3階（B甲板）の左舷の端が水面に届く高さ**（海審 p1057
#    「B갑판 좌현이 수면이 닿을 정도(기울기 약 52.2도)」）＝案C の A（`illu.deck_at`）と同じ考え。出港のときの喫水 6.20 で
#    回すと 52.2度で端が 0.9メートル水の下になり、記録（届くほど）を越えた（⑤b-4 の selftest で見つけた）。
#    ⚠️ そのぶん船は喫水 約4.8メートルに浮く＝形は模式（傾きの記録と「どの甲板が水面に」の記録を食い違わせない方を採った）
DRAFT_F = B_Y - HALF * math.tan(math.radians(52.2))


# 船尾の改造（海審 p1016 2.2.4〜2.2.6・p1017 2.2.9）
A_ROOF0, A_RAISE = 3.5, 1.7             # A甲板の船尾の部屋の天井 約3.5 → 約1.7 上げた
A_EXT, BR_EXT = 5.6, 2.6                # 後ろへ延ばした長さ（A甲板の船尾 約5.6・船橋甲板の船尾 約2.6）
X_COMP = (17.6, 33.6)                   # その部屋の前後の位置と長さ（記録に無い＝模式）
X_AEXT = X_COMP[0] - A_EXT              # 12.0
X_BREXT = X_COMP[0] - BR_EXT            # 15.0
ROOF_HI = A_Y + A_ROOF0 + A_RAISE       # 26.85（上げたあとの天井＝船橋甲板の天井 CMP_Y 26.75 とほぼ同じ高さ）
X_BCAB = (2.0, 12.5)                    # 運転手の客室（長さ 約10.5＝p1016 2.2.5。船尾の端に置いたのは模式）
X_HOLD1 = 100.0                         # 囲われた車の倉の前の端（模式）
X_SUP3 = (X_BCAB[1], X_HOLD1)           # 3階の部屋
X_SUP4 = (X_COMP[1], 98.0)              # 4階の部屋（船尾の背の高い部屋より前）
X_SUP5 = (X_COMP[1], 97.0)              # 5階
X_BRIDGE = (88.0, 97.0)                 # 操舵室（船橋甲板の前の端＝p1018「선수로부터 선교(조타실)」）
X_TWEEN = (X_BCAB[1], X_BCAB[1] + 18.6)  # トゥイーン甲板（C甲板の車の倉の後ろ＝p1019）
X_EHOLD = (frx(71), frx(136))           # E甲板の貨物倉（Fr.71〜136＝p1019）
X_TANK = (8.0, 132.0)                   # 底のタンク（模式の帯。タンクの並びは表7の総量で1本に）
X_BOX = (104.0, 122.0)                  # 船首の甲板の10フィートの箱（2段＝p1042 3.1.4.5・位置は模式）
BOX_TIER = 2.59                         # 箱の高さ 8.6フィート（p1043 注17）
X_DBOX = (108.0, 115.0)                 # D甲板の8フィートの箱（p1042 表6 D갑판 8피트 컨테이너 7・位置は模式）
X_RAMP = (86.0, 97.0)                   # 船首の右側の渡し板（p1016 2.2.6。位置と大きさは模式）
X_MARBLE = (20.2, 24.2)                 # 展示室の大理石（約37トン＝p1024 2.4.8。置き場所は模式）
BW_CAP = 2501.826                       # 平衡水（バラスト）タンクの容量の合計（p1044 表7）
BW_FRAC = dict(none=0.0, before=370.0 / BW_CAP, req=1703.0 / BW_CAP, low=761.272 / BW_CAP)
#   before＝改造の前 370トン・req＝改造のあとに認められた条件 1,703トン（p1018 表1）・low＝出港のとき 約761.2トン（p1043・p1044 表7）
CARGO_LESS = 987.0 / 2437.0              # 積める荷の上限 2,437 → 987 トン（p1018 表1）
PAIR_G = dict(low=9.8, high=13.8)       # c405 の重心の高さ（🔴 模式＝大きく描く。記録は 11.27 → 11.78 メートル＝p1018 表1）

# ══════════════════════════════════════════════════════════
#  見え方（画素）
# ══════════════════════════════════════════════════════════
CLIP = (F.BX0, F.BY0 + 12, F.BX1, F.BY1 - 40)
VIEWS = {
    "side": dict(kind="side", s=10.3, ox=118.0, oy=702.0, lab="横から見た断面（船首が右）"),
    "stern": dict(kind="side", s=30.0, ox=240.0, oy=1220.0, lab="横から見た断面・船尾の寄り（船首が右）"),
    "hold": dict(kind="side", s=22.0, ox=-330.0, oy=700.0, lab="横から見た断面・船体の下の寄り（船首が右）"),
    "front": dict(kind="front", s=13.0, piv=[(700.0, 600.0)], clip=(150.0, CLIP[1], 1130.0, CLIP[3]),
                  lab="船首の側から見た断面（左舷が右）"),
    "pair": dict(kind="pair", s=9.0, piv=[(500.0, 590.0), (1240.0, 590.0)], lab="船首の側から見た断面（左舷が右）"),
    "port": dict(kind="port", s=26.0, x0=150.0, y3=640.0, len=38.0, lab="3階と4階の左舷の外側を横から見た図"),
}


class _SideV:
    def __init__(self, v):
        self.s, self.ox, self.oy = v["s"], v["ox"], v["oy"]

    def p(self, x, y):
        return [self.ox + x * self.s, self.oy - y * self.s]


class _FrontV:
    """船首の側から：x＝左舷が＋（画面の右）・y＝竜骨から上。piv＝水面の中心（傾きの回転の中心）。"""

    def __init__(self, v, k=0):
        self.s = v["s"]
        self.piv = v["piv"][k]

    def p(self, x, y):
        return [self.piv[0] + x * self.s, self.piv[1] - (y - DRAFT_F) * self.s]


class _PortV:
    """左舷の外側：u＝船の長さの向きのメートル（右が船首）・y＝竜骨から上。"""

    def __init__(self, v):
        self.s, self.x0, self.y3 = v["s"], v["x0"], v["y3"]

    def p(self, u, y):
        return [self.x0 + u * self.s, self.y3 - (y - B_Y) * self.s]


def _box(V, x0, y0, x1, y1):
    return [V.p(x0, y0), V.p(x1, y0), V.p(x1, y1), V.p(x0, y1)]


def _ngon(V, x, y, r_px, n=12):
    cx, cy = V.p(x, y)
    return [[cx + r_px * math.cos(2 * math.pi * i / n), cy + r_px * math.sin(2 * math.pi * i / n)] for i in range(n)]


# 船体（横から）。船尾の板 → 3階の床の高さの囲い → 船首の甲板 → 船首の線 → 船底
HULL_SIDE = [(0.0, 4.6), (0.0, B_Y), (X_HOLD1, B_Y), (X_HOLD1, C_Y), (LOA - 1.2, C_Y + 0.8), (LOA, C_Y + 0.8),
             (LOA - 2.5, 7.0), (LOA - 7.5, 1.2), (LOA - 12.0, 0.0), (9.0, 0.0), (3.0, 1.2)]
# 船体（船首の側から）。3階の床の高さまで（車の倉は囲われている）
HULL_FRONT = [(-HALF, B_Y), (-HALF, 3.0), (-HALF + 1.2, 0.8), (-7.0, 0.0), (7.0, 0.0), (HALF - 1.2, 0.8),
              (HALF, 3.0), (HALF, B_Y)]

# ══════════════════════════════════════════════════════════
#  状態（欄と値）
# ══════════════════════════════════════════════════════════
ONOFF = ("off", "on")
FIELDS = {
    "side": dict(aroof=("low", "high"), aext=ONOFF, bcab=ONOFF, ramp=("on", "gone", "off"), marble=ONOFF,
                 cargo=("none", "load", "less"), ballast=("none", "before", "req", "low"), arrows=ONOFF,
                 hl=("none", "new", "de"), crew=("off", "br", "both"), run=ONOFF),
    "front": dict(heel=None, cargo=("off", "mid", "port"), lash=ONOFF, exits=ONOFF, paths=("off", "faint", "on"),
                  angle=ONOFF),
    "pair": dict(heel=None, add=ONOFF, g=("low", "high"), force=ONOFF, up=ONOFF),
    "port": dict(water=("low", "b", "a"), exits=("off", "on", "shut3", "shut"), out=ONOFF),
}
START = {
    "side": dict(aroof="high", aext="on", bcab="on", ramp="off", marble="off", cargo="none", ballast="none",
                 arrows="off", hl="none", crew="off", run="off"),
    "front": dict(heel=0.0, cargo="off", lash="off", exits="off", paths="off", angle="off"),
    "pair": dict(heel=0.0, add="off", g="low", force="off", up="off"),
    "port": dict(water="low", exits="off", out="off"),
}
PORT_LEVEL = dict(low=B_Y - 2.3, b=B_Y + RAIL_H + 0.5, a=A_Y + RAIL_H + 0.5)   # 水の面（模式の高さ・順番は判決 p18）
DOOR_U = dict(b=(8.0, 9.3), a=(22.0, 23.3))                                   # 出入口の位置（記録に無い＝模式）


def kind_of(view):
    return VIEWS[view]["kind"]


def _states(view, start, steps):
    k = kind_of(view)
    fields = FIELDS["side" if k == "side" else k]
    cur = dict(START["side" if k == "side" else k], **(start or {}))
    out = []
    for st in [dict(state={})] + list(steps):
        cur = dict(cur, **(st.get("state") or {}))
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"hull：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if fields[f_] is None:
                cur[f_] = float(v)
            elif v not in fields[f_]:
                raise ValueError(f"hull：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    return out[0], out[1:]


# ══════════════════════════════════════════════════════════
#  部品（状態 → 形）。🔴 門番もこの関数を呼ぶ
# ══════════════════════════════════════════════════════════
def _P(ident, typ, pts=None, **kw):
    d = dict(id=ident, type=typ)
    if pts is not None:
        d["pts"] = [list(map(float, q)) for q in pts]
    d.update(kw)
    return d


def _side_parts(V, st):
    s = V.s
    hlnew = "AMBER" if st["hl"] == "new" else "INK_W"
    on = lambda b: 1.0 if b else 0.0  # noqa: E731
    parts = []
    # 積み荷（面。1台ずつ描かない）＝表6 の甲板（トゥイーン・C・D・E）と船首の甲板の箱
    cg = dict(tw=(X_TWEEN[0] + 0.3, TW_Y, X_TWEEN[1] - 0.3, TW_Y + 1.5),
              c=(12.8, C_Y, 98.5, C_Y + 2.4), d=(8.0, D_Y, 118.0, D_Y + 3.6),
              e=(X_EHOLD[0] + 0.5, E_Y, X_EHOLD[1] - 0.5, E_Y + 2.9),
              box=(X_BOX[0], C_Y, X_BOX[1], C_Y + 2 * BOX_TIER), dbox=(X_DBOX[0], D_Y, X_DBOX[1], D_Y + BOX_TIER - 0.1))
    vis = st["cargo"] != "none"
    for k, (x0, y0, x1, y1) in cg.items():
        if st["cargo"] == "less":
            x1 = x0 + (x1 - x0) * CARGO_LESS
        parts.append(_P(f"cg_{k}_f", "poly", _box(V, x0, y0, x1, y1), fill="AMBER", alpha=0.32 * on(vis)))
        parts.append(_P(f"cg_{k}_o", "poly", _box(V, x0, y0, x1, y1), stroke="AMBER", w=2.5, alpha=on(vis)))
    # 底のタンクの水（帯の高さ×割合＝表1・表7）
    fr = BW_FRAC[st["ballast"]]
    parts.append(_P("bw", "poly", _box(V, X_TANK[0], 0.0, X_TANK[1], max(0.02, fr * E_Y)), fill="LINE",
                    alpha=0.9 * on(fr > 0)))
    # 船尾の改造（p1016）
    roof = A_Y + A_ROOF0 + (A_RAISE if st["aroof"] == "high" else 0.0)
    parts += [_P("comp_f", "poly", _box(V, X_COMP[0], A_Y, X_COMP[1], roof), fill="BG2", alpha=0.85),
              _P("comp_o", "poly", _box(V, X_COMP[0], A_Y, X_COMP[1], roof), stroke=hlnew if st["aroof"] == "high"
                 else "INK_W", w=3)]
    ae = st["aext"] == "on"
    parts += [_P("aext_f", "poly", _box(V, X_AEXT, A_Y, X_COMP[0], BR_Y), fill="BG2", alpha=0.85 * on(ae)),
              _P("aext_o", "poly", _box(V, X_AEXT, A_Y, X_COMP[0], BR_Y), stroke=hlnew, w=3, alpha=on(ae)),
              _P("brext_f", "poly", _box(V, X_BREXT, BR_Y, X_COMP[0], ROOF_HI), fill="BG2", alpha=0.85 * on(ae)),
              _P("brext_o", "poly", _box(V, X_BREXT, BR_Y, X_COMP[0], ROOF_HI), stroke=hlnew, w=3, alpha=on(ae)),
              _P("split", "line", [V.p(X_BREXT, BR_Y), V.p(X_COMP[1], BR_Y)], stroke=hlnew, w=3, alpha=on(ae))]
    bc = st["bcab"] == "on"
    parts += [_P("bcab_f", "poly", _box(V, X_BCAB[0], B_Y, X_BCAB[1], A_Y), fill="BG2", alpha=0.85 * on(bc)),
              _P("bcab_o", "poly", _box(V, X_BCAB[0], B_Y, X_BCAB[1], A_Y), stroke=hlnew, w=3, alpha=on(bc))]
    rp = st["ramp"]
    parts.append(_P("ramp", "poly", _box(V, X_RAMP[0], C_Y + 0.4, X_RAMP[1], B_Y - 0.4), stroke="INK_W", w=3,
                    alpha={"on": 1.0, "gone": 0.3, "off": 0.0}[rp]))
    (xa, ya), (xb, yb) = V.p(X_RAMP[0] + 1.5, C_Y + 0.9), V.p(X_RAMP[1] - 1.5, B_Y - 0.9)
    parts += [_P("rampx1", "line", [[xa, ya], [xb, yb]], stroke="ALERT", w=6, alpha=on(rp == "gone")),
              _P("rampx2", "line", [[xa, yb], [xb, ya]], stroke="ALERT", w=6, alpha=on(rp == "gone"))]
    mb = st["marble"] == "on"
    parts += [_P("marble_f", "poly", _box(V, X_MARBLE[0], BR_Y + 0.15, X_MARBLE[1], BR_Y + 1.25), fill="AMBER",
                 alpha=0.9 * on(mb)),
              _P("marble_o", "poly", _box(V, X_MARBLE[0], BR_Y + 0.15, X_MARBLE[1], BR_Y + 1.25), stroke="INK_W",
                 w=2, alpha=on(mb))]
    # 目立たせる（c514＝D・E甲板）
    de = st["hl"] == "de"
    parts += [_P("hl_d", "poly", _box(V, 4.0, D_Y + 0.12, 124.0, C_Y - 0.12), stroke="ALERT", w=5, alpha=on(de)),
              _P("hl_e", "poly", _box(V, X_EHOLD[0] + 0.1, E_Y + 0.12, X_EHOLD[1] - 0.1, D_Y - 0.12), stroke="ALERT",
                 w=5, alpha=on(de))]
    # 船員の居場所（c712）＝人は描かない・輪だけ（判決 p14〜15）
    cr = st["crew"]
    r_ring = max(16.0, 1.9 * s)
    parts += [_P("crew_br", "circle", c=V.p(92.5, BR_Y + 1.25), r=r_ring, stroke="AMBER", w=5,
                 alpha=on(cr in ("br", "both")), glow=on(cr in ("br", "both")), fill=None),
              _P("crew_en", "circle", c=V.p(22.0, B_Y + 1.35), r=r_ring, stroke="AMBER", w=5,
                 alpha=on(cr == "both"), glow=on(cr == "both"), fill=None)]
    # 矢印（c409：荷 ↓・水 ↑）と進む向き（c509）
    ar = st["arrows"] == "on"
    parts += [_P("arr_cg", "line", [V.p(45.0, B_Y - 0.4), V.p(45.0, C_Y + 2.6)], stroke="AMBER", w=6, head=20,
                 alpha=on(ar)),
              _P("arr_bw", "line", [V.p(45.0, -0.9), V.p(45.0, E_Y + 0.6)], stroke="LINE", w=6, head=20,
                 alpha=on(ar))]
    parts.append(_P("run", "line", [V.p(58.0, -0.55), V.p(86.0, -0.55)], stroke="AMBER", w=6, head=22,
                    alpha=on(st["run"] == "on")))
    return parts


def _front_ship(V, st, heel, pre="", full=True):
    """船首の側から見た船1隻の部品（船の座標の画素・回す前）。rot＝heel・pivot＝水面の中心。"""
    on = lambda b: 1.0 if b else 0.0  # noqa: E731
    piv = list(V.piv)
    R = dict(rot=float(heel), pivot=piv)
    parts = [_P(pre + "hull_f", "poly", [V.p(*q) for q in HULL_FRONT], fill="BG2", alpha=0.7, **R)]
    if full:
        cargo = st.get("cargo", "off")
        sh = dict(d=2.6, c=1.4, e=0.9) if cargo == "port" else dict(d=0.0, c=0.0, e=0.0)
        blocks = dict(e=(-5.2, E_Y, 5.2, E_Y + 2.6), d=(-8.2, D_Y, 8.2, D_Y + 3.0), c=(-9.4, C_Y, 9.4, C_Y + 2.2))
        for k, (x0, y0, x1, y1) in blocks.items():
            q = _box(V, x0 + sh[k], y0, x1 + sh[k], y1)
            parts.append(_P(pre + f"cg_{k}_f", "poly", q, fill="AMBER", alpha=0.35 * on(cargo != "off"), **R))
            parts.append(_P(pre + f"cg_{k}_o", "poly", q, stroke="AMBER", w=2.5, alpha=on(cargo != "off"), **R))
            for j, x in enumerate((x0 + 0.5, x1 - 0.5)):          # 固縛（縛る帯）＝片寄ると外れて消える
                dx_ = -1.1 if j == 0 else 1.1
                parts.append(_P(pre + f"lash_{k}{j}", "line", [V.p(x, y1 - 0.3), V.p(x + dx_, y0)], stroke="INK_W",
                                w=2, alpha=on(cargo != "off" and st.get("lash") == "on"), **R))
    for nm, y in (("E", E_Y), ("D", D_Y), ("C", C_Y)):
        w_ = HALF - (1.4 if nm == "E" else 0.0)
        parts.append(_P(pre + f"dk{nm}", "line", [V.p(-w_, y), V.p(w_, y)], stroke="LINE_DIM", w=2, **R))
    parts.append(_P(pre + "dkB", "line", [V.p(-HALF, B_Y), V.p(HALF, B_Y)], stroke="INK_W", w=3, **R))
    rooms = dict(f3=(-HALF, B_Y, HALF - WALK, A_Y), f4=(-HALF + WALK, A_Y, HALF - WALK, BR_Y),
                 f5=(-8.0, BR_Y, 8.0, CMP_Y))
    for k, (x0, y0, x1, y1) in rooms.items():
        parts.append(_P(pre + k + "_f", "poly", _box(V, x0, y0, x1, y1), fill="BG2", alpha=0.7, **R))
        parts.append(_P(pre + k + "_o", "poly", _box(V, x0, y0, x1, y1), stroke="INK_W", w=3, **R))
    parts.append(_P(pre + "dkA", "line", [V.p(-HALF, A_Y), V.p(HALF, A_Y)], stroke="INK_W", w=3, **R))
    if full:
        # 左舷の通路の手すり（3階・4階＝判決 p16「3층과 4층 좌현갑판에는 난간」）と出入口
        for k, y in (("3", B_Y), ("4", A_Y)):
            parts.append(_P(pre + f"rail{k}", "line", [V.p(HALF, y), V.p(HALF, y + RAIL_H)], stroke="INK_W", w=4,
                            **R))
            ex = st.get("exits") == "on"
            parts.append(_P(pre + f"door{k}", "poly", _box(V, HALF - WALK - 0.35, y + 0.05, HALF - WALK + 0.05,
                                                           y + 2.0), fill="AMBER" if ex else "LINE_DIM", **R))
            pa = st.get("paths", "off")
            parts.append(_P(pre + f"path{k}", "line", [V.p(-3.0, y + 1.0), V.p(HALF - WALK - 0.6, y + 1.0)],
                            stroke="AMBER", w=5, head=18, alpha={"off": 0.0, "faint": 0.35, "on": 1.0}[pa], **R))
    parts.append(_P(pre + "hull_o", "poly", [V.p(*q) for q in HULL_FRONT], stroke="INK_W", w=4, **R))
    return parts


def _front_parts(V, st):
    parts = _front_ship(V, st, st["heel"])
    x0, y0, x1, y1 = VIEWS["front"]["clip"][0], V.piv[1], VIEWS["front"]["clip"][2], CLIP[3]
    parts.append(_P("sea", "poly", [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], fill="LINE", alpha=0.22, top=True))
    parts.append(_P("wl", "line", [[x0, y0], [x1, y0]], stroke="LINE", w=3, top=True))
    r = 250.0
    a0, a1 = -90.0, -90.0 + float(st["heel"])
    arc = [[V.piv[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / 24)),
            V.piv[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / 24))] for i in range(25)]
    parts.append(_P("arc", "line", arc, stroke="AMBER", w=5, alpha=1.0 if st["angle"] == "on" else 0.0, top=True))
    parts.append(_P("up0", "line", [[V.piv[0], V.piv[1]], [V.piv[0], V.piv[1] - r - 20]], stroke="TICK", w=2,
                    alpha=1.0 if st["angle"] == "on" else 0.0, top=True))
    return parts


def _pair_parts(v, st):
    on = lambda b: 1.0 if b else 0.0  # noqa: E731
    parts = []
    for k, pre in enumerate(("L_", "R_")):
        V = _FrontV(v, k)
        R = dict(rot=float(st["heel"]), pivot=list(V.piv))
        parts += _front_ship(V, st, st["heel"], pre=pre, full=False)
        if pre == "R_":
            add = st["add"] == "on"
            parts.append(_P("R_add_f", "poly", _box(V, -5.5, CMP_Y, 5.5, CMP_Y + 2.2), fill="AMBER", alpha=0.85 * on(add),
                            **R))
            parts.append(_P("R_add_o", "poly", _box(V, -5.5, CMP_Y, 5.5, CMP_Y + 2.2), stroke="INK_W", w=2,
                            alpha=on(add), **R))
        gy = PAIR_G["high"] if (pre == "R_" and st["g"] == "high") else PAIR_G["low"]
        parts.append(_P(pre + "g", "poly", _ngon(V, 0.0, gy, 13.0), fill="ALERT", stroke="INK_W", w=2, **R))
        if pre == "R_":
            parts.append(_P("R_up", "line", [V.p(1.6, PAIR_G["low"]), V.p(1.6, PAIR_G["high"] - 0.3)],
                            stroke="ALERT", w=5, head=16, alpha=on(st["up"] == "on"), **R))
        # 元へ戻ろうとする力（回らない矢印・大きさは模式＝重心が高いほど小さく）
        rr = 262.0
        a0, a1 = (-58.0, -122.0) if pre == "L_" else (-70.0, -96.0)
        arc = [[V.piv[0] + rr * math.cos(math.radians(a0 + (a1 - a0) * i / 20)),
                V.piv[1] + rr * math.sin(math.radians(a0 + (a1 - a0) * i / 20))] for i in range(21)]
        parts.append(_P(pre + "force", "line", arc, stroke="AMBER", w=7, head=22, alpha=on(st["force"] == "on"),
                        top=True))
        x0, x1 = V.piv[0] - 300, V.piv[0] + 300
        parts.append(_P(pre + "sea", "poly", [[x0, V.piv[1]], [x1, V.piv[1]], [x1, CLIP[3]], [x0, CLIP[3]]],
                        fill="LINE", alpha=0.22, top=True))
        parts.append(_P(pre + "wl", "line", [[x0, V.piv[1]], [x1, V.piv[1]]], stroke="LINE", w=3, top=True))
    return parts


def _port_parts(V, st):
    on = lambda b: 1.0 if b else 0.0  # noqa: E731
    L = VIEWS["port"]["len"]
    lv = PORT_LEVEL[st["water"]]
    y_bot = B_Y - (CLIP[3] - V.y3) / V.s
    parts = [_P("water", "poly", _box(V, 0.0, y_bot, L, lv), fill="LINE", alpha=0.55)]
    ex = st["exits"]
    for k, fl in (("3", "b"), ("4", "a")):
        u0, u1 = DOOR_U[fl]
        y = B_Y if k == "3" else A_Y
        cx, cy = V.p((u0 + u1) / 2, y + 1.0)
        shut = ex == "shut" or (ex == "shut3" and k == "3")
        a, b = V.p(u0 - 0.3, y - 0.2), V.p(u1 + 0.3, y + 2.3)
        parts += [_P(f"glow{k}", "circle", c=[cx, cy], r=26.0, fill="AMBER", stroke="INK_W", w=3,
                     alpha=0.9 * on(ex == "on"), glow=on(ex == "on")),
                  _P(f"x{k}a", "line", [a, b], stroke="ALERT", w=7, alpha=on(shut)),
                  _P(f"x{k}b", "line", [[a[0], b[1]], [b[0], a[1]]], stroke="ALERT", w=7, alpha=on(shut)),
                  _P(f"out{k}", "line", [V.p((u0 + u1) / 2 + 1.4, y + 1.2), V.p((u0 + u1) / 2 + 3.4, y - 1.4)],
                     stroke="AMBER", w=6, head=20, alpha=on(st["out"] == "on"))]
    return parts


def parts_of(view, st):
    v = VIEWS[view]
    k = v["kind"]
    if k == "side":
        return _side_parts(_SideV(v), st)
    if k == "front":
        return _front_parts(_FrontV(v), st)
    if k == "pair":
        return _pair_parts(v, st)
    return _port_parts(_PortV(v), st)


# ══════════════════════════════════════════════════════════
#  基図（動かない所）
# ══════════════════════════════════════════════════════════
def _clip_open(view, box=None):
    x0, y0, x1, y1 = box or CLIP
    cid = f"hullclip_{view}"
    return (f'<defs><clipPath id="{cid}"><rect x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" '
            f'height="{y1 - y0:.0f}"/></clipPath></defs><g clip-path="url(#{cid})">')


def _side_base(view, V):
    s = V.s
    g = [_clip_open(view)]
    ywl = V.p(0, DRAFT)[1]
    g.append(F.rect(CLIP[0], ywl, CLIP[2] - CLIP[0], CLIP[3] - ywl, J.GRID, op=0.75))
    g.append(F.poly([V.p(*q) for q in HULL_SIDE], J.BG2, None, close=True, op=0.6))
    # 甲板の線（E・D・C・トゥイーン）と倉・帯の枠
    g += [F.line(*V.p(frx(36), E_Y), *V.p(frx(147), E_Y), J.LINE_DIM, 2),
          F.line(*V.p(2.0, D_Y), *V.p(LOA - 4.2, D_Y), J.LINE, 3),
          F.line(*V.p(0.0, C_Y), *V.p(LOA - 1.0, C_Y + 0.02), J.LINE_DIM, 2),
          F.line(*V.p(X_TWEEN[0], TW_Y), *V.p(X_TWEEN[1], TW_Y), J.LINE_DIM, 2),
          F.rect(*V.p(X_EHOLD[0], D_Y), (X_EHOLD[1] - X_EHOLD[0]) * s, (D_Y - E_Y) * s, "none", J.LINE_DIM, 2,
                 dash="8 6"),
          F.rect(*V.p(X_TANK[0], E_Y), (X_TANK[1] - X_TANK[0]) * s, E_Y * s, "none", J.LINE_DIM, 2)]
    # 上の階（3階＝船尾の運転手の客室の所は下の部品・4階・5階は船尾の部屋より前）
    for (x0, x1), (y0, y1) in ((X_SUP3, (B_Y, A_Y)), (X_SUP4, (A_Y, BR_Y)), (X_SUP5, (BR_Y, CMP_Y))):
        q = _box(V, x0, y0, x1, y1)
        g += [F.poly(q, J.BG2, None, close=True, op=0.45), F.poly(q, "none", J.INK_W, 3, close=True)]
    # 運転手の客室にする前の「乗用車の置き場」（B甲板の船尾＝p1016 2.2.5）＝点線の枠
    g.append(F.poly(_box(V, X_BCAB[0], B_Y, X_BCAB[1], A_Y), "none", J.LINE_DIM, 2, close=True, dash="7 6"))
    # 窓の並び（飾り＝中は描かない）
    for (x0, x1), y0 in ((X_SUP3, B_Y + 1.0), (X_SUP4, A_Y + 1.0)):
        x = x0 + 1.5
        while x + 0.9 < x1 - 1.0:
            g.append(F.rect(*V.p(x, y0 + 0.8), 0.9 * s, 0.8 * s, J.LINE_DIM))
            x += 3.0
    # 操舵室の窓の帯・屋上のマスト・船首のマスト
    g += [F.rect(*V.p(X_BRIDGE[0], BR_Y + 1.8), (X_BRIDGE[1] - X_BRIDGE[0]) * s, 0.8 * s, J.LINE),
          F.line(*V.p(92.0, CMP_Y), *V.p(92.0, CMP_Y + 4.2), J.INK_W, 3),
          F.line(*V.p(127.0, C_Y + 0.8), *V.p(127.0, C_Y + 11.0), J.INK_W, 3),
          F.line(*V.p(127.0, C_Y + 8.5), *V.p(119.0, C_Y + 5.4), J.INK_W, 2)]
    g.append(F.poly([V.p(*q) for q in HULL_SIDE], "none", J.INK_W, 4, close=True))
    g.append(F.line(CLIP[0], ywl, CLIP[2], ywl, J.LINE, 2, dash="12 8"))
    g.append("</g>")
    return g


def _deck_labels(view, V):
    names = [("5階（船橋甲板）", BR_Y + 1.25), ("4階（A甲板）", A_Y + 1.3), ("3階（B甲板）", B_Y + 1.35),
             ("C甲板", C_Y + 2.4), ("D甲板", D_Y + 3.0), ("E甲板", E_Y + 2.9), ("底のタンク", E_Y / 2)]
    g = []
    if view == "side":
        for t, y in names:
            yy = V.p(0, y)[1] + 9
            g.append(F.txtfit(1636, yy, t, 200, cap=22, col=J.TICK))
    elif view == "stern":
        for t, y in names[:4]:
            yy = V.p(0, y)[1] + 9
            if CLIP[1] + 20 < yy < CLIP[3] - 10:
                g.append(F.txtfit(CLIP[2] - 12, yy, t.split("（")[0], 150, cap=24, col=J.TICK, anchor="end"))
    else:
        for t, y in names[3:]:
            yy = V.p(0, y)[1] + 9
            if CLIP[1] + 20 < yy < CLIP[3] - 10:
                g.append(F.txtfit(V.p(X_EHOLD[0] + 1.0, 0)[0] if t == "E甲板" else CLIP[0] + 60, yy, t, 200, cap=24,
                                  col=J.TICK))
    return g


def _front_base(view, v):
    g = []
    for k in range(len(v["piv"])):
        V = _FrontV(v, k)
        if view == "pair":
            x0, x1 = V.piv[0] - 300, V.piv[0] + 300
        else:
            x0, x1 = v["clip"][0], v["clip"][2]
        g.append(F.rect(x0, V.piv[1], x1 - x0, CLIP[3] - V.piv[1], J.GRID, op=0.75))
        if k == 0:
            g.append(F.txtfit(x0 + 12, V.piv[1] + 34, "水面", 120, cap=24, col=J.TICK))
    return g


def _port_base(view, V):
    L = VIEWS["port"]["len"]
    s = V.s
    g = [_clip_open(view, (V.x0 - 2, CLIP[1], V.x0 + L * s + 2, CLIP[3]))]
    yb = B_Y - (CLIP[3] - V.y3) / s
    g.append(F.poly(_box(V, 0, yb, L, B_Y), J.BG2, None, close=True, op=0.6))            # 船体の横の壁
    g.append(F.line(*V.p(0, C_Y), *V.p(L, C_Y), J.LINE_DIM, 2, dash="10 8"))            # C甲板の高さ
    for y0, y1 in ((B_Y, A_Y), (A_Y, BR_Y), (BR_Y, CMP_Y)):
        q = _box(V, 0, y0, L, y1)
        g += [F.poly(q, J.BG2, None, close=True, op=0.45), F.poly(q, "none", J.INK_W, 2, close=True)]
        u = 1.2
        while u + 1.0 < L - 0.5:
            if not any(a - 0.6 < u < b + 0.4 for a, b in DOOR_U.values()) or y0 == BR_Y:
                g.append(F.rect(*V.p(u, y0 + 1.9), 1.0 * s, 0.9 * s, J.LINE_DIM))
            u += 2.6
    # 出入口（3階・4階）
    for fl, y in (("b", B_Y), ("a", A_Y)):
        u0, u1 = DOOR_U[fl]
        g.append(F.poly(_box(V, u0, y + 0.05, u1, y + 2.0), J.LINE_DIM, J.INK_W, 3, close=True))
    # 床の縁と手すり（柱）
    for y in (B_Y, A_Y):
        g += [F.line(*V.p(0, y), *V.p(L, y), J.INK_W, 4), F.line(*V.p(0, y + RAIL_H), *V.p(L, y + RAIL_H), J.INK_W, 3)]
        u = 0.4
        while u < L:
            g.append(F.line(*V.p(u, y), *V.p(u, y + RAIL_H), J.INK_W, 2))
            u += 1.9
    # 3階と4階のあいだの階段（判決 p16「난간과 계단」）
    g.append(F.line(*V.p(29.0, B_Y), *V.p(33.0, A_Y), J.INK_W, 4))
    for i in range(1, 6):
        u = 29.0 + 4.0 * i / 6
        y = B_Y + (A_Y - B_Y) * i / 6
        g.append(F.line(*V.p(u - 0.35, y), *V.p(u + 0.35, y), J.INK_W, 2))
    g.append("</g>")
    for t, y in (("3階", B_Y + 0.95), ("4階", A_Y + 0.95), ("5階", BR_Y + 0.95)):
        g.append(F.txtfit(V.x0 + L * s + 14, V.p(0, y)[1] + 9, t, 90, cap=26, col=J.TICK))
    return g


# ══════════════════════════════════════════════════════════
#  段ごとの飾り（札・印・寸法）
# ══════════════════════════════════════════════════════════
TAG_AT = {
    "side": {"t1": (150, 290, "start", 600), "t2": (150, 350, "start", 600), "t3": (760, 290, "start", 560),
             "t4": (760, 350, "start", 560), "t5": (1240, 290, "start", 380), "t6": (1240, 350, "start", 380),
             "b1": (150, 800, "start", 700), "b2": (900, 800, "start", 700)},
    "stern": {"t1": (1500, 330, "start", 330), "t2": (1500, 400, "start", 330)},
    "hold": {"t1": (160, 290, "start", 700), "t2": (160, 350, "start", 700), "t3": (1000, 290, "start", 800),
             "t4": (1000, 350, "start", 800)},
    "front": {f"row{i}": (1170, 330 + 110 * i, "start", 660) for i in range(5)},
    "pair": {"lh": (500, 835, "middle", 520), "rh": (1240, 835, "middle", 520), "top": (870, 290, "middle", 700),
             "gl": (524, 555, "start", 200), "gr": (1268, 518, "start", 300)},
    "port": {f"row{i}": (1250, 330 + 105 * i, "start", 580) for i in range(5)},
}


def _icon(kind, cx, cy, sc=1.0):
    """積み荷の種類の印（数ではない＝1つずつ）。幅 約60画素。"""
    k = sc
    ink, bg = J.INK_W, J.BG2
    P = lambda x, y: (cx + x * k, cy + y * k)  # noqa: E731

    def R(x, y, w, h, fill=bg, sw=2.5):
        return F.rect(cx + x * k, cy + y * k, w * k, h * k, fill, ink, sw)

    def C(x, y, r):
        return F.circ(*P(x, y), r * k, J.BG, ink, 2.5)

    def Ln(x1, y1, x2, y2, sw=3):
        return F.line(*P(x1, y1), *P(x2, y2), ink, sw)
    if kind == "car":
        return "".join([F.poly([P(-28, 4), P(-28, -6), P(-14, -8), P(-6, -18), P(14, -18), P(22, -8), P(28, -6),
                                P(28, 4)], bg, ink, 2.5, close=True), C(-16, 6, 6), C(16, 6, 6)])
    if kind == "van":
        return "".join([F.poly([P(-30, 6), P(-30, -22), P(18, -22), P(30, -8), P(30, 6)], bg, ink, 2.5, close=True),
                        C(-17, 8, 6), C(18, 8, 6)])
    if kind == "truck":
        return "".join([R(-32, -26, 40, 28), F.poly([P(10, 2), P(10, -18), P(24, -18), P(32, -8), P(32, 2)], bg, ink,
                                                      2.5, close=True), C(-22, 6, 6), C(-8, 6, 6), C(22, 6, 6)])
    if kind == "digger":
        return "".join([R(-30, 0, 40, 10, sw=2.5), R(-24, -18, 26, 18), Ln(2, -14, 20, -34, 4), Ln(20, -34, 32, -10, 4),
                        F.poly([P(26, -10), P(38, -10), P(34, 0)], bg, ink, 2.5, close=True)])
    if kind == "forklift":
        return "".join([R(-26, -16, 30, 18), Ln(-18, -16, -18, -30, 3), Ln(-18, -30, 2, -30, 3), Ln(10, 2, 10, -34, 4),
                        Ln(10, 0, 30, 0, 4), C(-18, 4, 6), C(-2, 4, 6)])
    if kind == "steel":
        return "".join([R(-30, -18, 60, 6), R(-30, -10, 60, 6), R(-30, -2, 60, 6)])
    if kind == "box":
        return "".join([R(-26, -24, 52, 26)] + [Ln(-26 + 13 * i, -24, -26 + 13 * i, 2, 2) for i in (1, 2, 3)])
    if kind == "bag":
        return "".join([R(-16, -24, 32, 26), Ln(-8, -24, -4, -32, 2), Ln(8, -24, 4, -32, 2), Ln(-4, -32, 4, -32, 2)])
    raise ValueError(f"hull：知らない印 {kind!r}")


def _dim_svg(view, V, dm):
    """寸法の矢印（数字は書かない＝模式）。kind＝len（長さ）・dep（深さ）・bre（幅＝右上の小さな船首の側の図）。"""
    g = []
    col = J.AMBER
    if dm["kind"] == "len":
        y = V.p(0, -2.6)[1]
        a, b = V.p(0, 0)[0], V.p(LOA, 0)[0]
        m = (a + b) / 2
        g += [F.arrow(m, y, a, y, col, 4, 16), F.arrow(m, y, b, y, col, 4, 16),
              F.txtfit(m, y + 42, dm.get("t", "長さ"), 300, cap=30, col=col, anchor="middle")]
    elif dm["kind"] == "dep":
        x = V.p(60.0, 0)[0]                  # 船の真ん中あたり（右の外は甲板の名の札）
        a, b = V.p(0, 0)[1], V.p(0, C_Y)[1]
        m = (a + b) / 2
        g += [F.arrow(x, m, x, a, col, 4, 16), F.arrow(x, m, x, b, col, 4, 16),
              F.txtfit(x + 16, m + 10, dm.get("t", "深さ"), 120, cap=30, col=col)]
    elif dm["kind"] == "bre":
        cx, cy, k = 1640.0, 330.0, 5.0
        q = [(cx + x * k, cy - (y - C_Y) * k) for x, y in HULL_FRONT]
        g += [F.poly(q, J.BG2, J.INK_W, 3, close=True),
              F.txtfit(cx, cy - 20, "船首の側から", 240, cap=22, col=J.TICK, anchor="middle")]
        y = cy - (C_Y + 1.0 - C_Y) * k + 20
        g += [F.arrow(cx, y, cx - HALF * k, y, col, 4, 14), F.arrow(cx, y, cx + HALF * k, y, col, 4, 14),
              F.txtfit(cx, y + 36, dm.get("t", "幅"), 120, cap=28, col=col, anchor="middle")]
    elif dm["kind"] == "rise":
        # 天井を上げた高さ（c402）＝部屋の左の外に上下の矢印
        x = V.p(X_COMP[1] + 1.2, 0)[0]
        a, b = V.p(0, A_Y + A_ROOF0)[1], V.p(0, ROOF_HI)[1]
        g += [F.arrow(x, a, x, b, col, 4, 14), F.line(x - 10, a, x + 10, a, col, 3),
              F.txtfit(x + 14, (a + b) / 2 + 10, dm.get("t", ""), 300, cap=28, col=col)]
    elif dm["kind"] == "ext":
        # 延ばした長さ（c402）＝下の段 A_EXT・上の段 BR_EXT
        for (x0, y), t in (((X_AEXT, A_Y - 0.8), dm.get("ta", "")), ((X_BREXT, ROOF_HI + 0.8), dm.get("tb", ""))):
            (xa, ya), (xb, _) = V.p(x0, y), V.p(X_COMP[0], y)
            g += [F.arrow(xb, ya, xa, ya, col, 4, 14), F.line(xb, ya - 10, xb, ya + 10, col, 3)]
            if t:
                g.append(F.txtfit(xa - 12, ya + 10, t, 260, cap=26, col=col, anchor="end"))
    else:
        raise ValueError(f"hull：知らない寸法 {dm['kind']!r}")
    return "".join(g)


def _stage_svgs(view, V, steps, cap=34):
    pre = TAG_AT[view]
    stages, texts = [], []
    for st in steps:
        s = []
        for dm in F._many(st.get("dim")):
            s.append(_dim_svg(view, V, dm))
            texts += [t for t in (dm.get("t"), dm.get("ta"), dm.get("tb")) if t]
        for ic in F._many(st.get("icon")):
            s.append(_icon(ic["k"], *V.p(*ic["m"]), sc=ic.get("sc", 1.0)))
        for tg in F._many(st.get("tag")):
            if "m" in tg:
                x, y = V.p(*tg["m"])
                x, y = x + tg.get("dx", 0), y + tg.get("dy", 0)
                anchor, mw = tg.get("anchor", "start"), tg.get("w", 420)
            else:
                at = tg.get("at", next(iter(pre)))
                x, y, anchor, mw = pre[at] if isinstance(at, str) else (tuple(at) if len(at) == 4
                                                                        else (at[0], at[1], "start", 420))
            c = tg.get("cap", cap)
            if tg.get("to"):
                tx, ty = V.p(*tg["to"])
                s.append(F.line(x, y + 8, tx, ty, J.AMBER, 2))
            s.append(F.txtfit(x, y, tg["t"], mw, cap=c, col=tg.get("col", J.AMBER), anchor=anchor))
            texts.append(tg["t"])
            if tg.get("d"):
                s.append(F.txtfit(x, y + round(c * 0.95), tg["d"], mw, cap=round(c * 0.62), col=J.TICK, anchor=anchor))
                texts.append(tg["d"])
        stages.append("".join(s) or " ")
    return stages, texts


# ══════════════════════════════════════════════════════════
#  型の本体
# ══════════════════════════════════════════════════════════
def _svg_of(sh, key):
    """動かない部品を基図の SVG に（鍵0の状態で）。"""
    a = key.get("alpha", sh.get("alpha", 1.0))
    a = 1.0 if a is None else float(a)
    if a <= 0.01:
        return ""
    col = lambda nm: None if not nm else (nm if nm.startswith("#") else getattr(J, nm))  # noqa: E731
    fill, stroke = col(key.get("fill", sh.get("fill"))), col(key.get("stroke", sh.get("stroke")))
    if sh["type"] == "circle":
        cx, cy = sh["c"][0] + float(key.get("dx", 0) or 0), sh["c"][1] + float(key.get("dy", 0) or 0)
        return F.circ(cx, cy, sh["r"], fill or "none", stroke, sh.get("w", 3), op=round(a, 3))
    q = F.mech_pts(sh, key)
    if sh["type"] == "poly":
        return F.poly(q, fill or "none", stroke, sh.get("w", 3), close=True, op=round(a, 3))
    out = F.poly(q, "none", stroke or fill, sh.get("w", 3), op=round(a, 3))
    if sh.get("head") and len(q) >= 2:
        (x1, y1), (x2, y2) = q[-2], q[-1]
        out += F.arrow(x1, y1, x2, y2, stroke or fill, sh.get("w", 3), sh["head"]).replace("/>", f' opacity="{a:.3f}"/>', 1)
    return out


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def hull(view, steps, start=None, rel=(), note="", src=""):
    """断面F。view＝VIEWS の名前。steps＝ナレーションの行ごとの段（上の「SPEC の書き方」）。"""
    if view not in VIEWS:
        raise ValueError(f"hull：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if "模式" not in note:
        raise ValueError("hull：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    v = VIEWS[view]
    k = v["kind"]
    start, states = _states(view, start, steps)
    for st in [start] + states:
        if k in ("front", "pair") and abs(st["heel"]) > 0.01 and not any(
                isinstance(r, dict) and abs(float(r.get("heel", -999)) - st["heel"]) < 0.01 for r in rel):
            raise ValueError(f"hull：傾き {st['heel']} 度を rel に宣言していない（記録の頁か「模式」を src に）")
    V = _SideV(v) if k == "side" else _FrontV(v) if k in ("front", "pair") else _PortV(v)
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
        sh = {f_: p0[f_] for f_ in p0 if f_ not in ("alpha", "top")}
        sh["keys"] = keys
        moving = p0.get("top") or any({f_: kk.get(f_) for f_ in KEY_FIELDS} != {f_: keys[0].get(f_) for f_ in KEY_FIELDS}
                                      for kk in keys[1:])
        sh["anim"] = bool(moving)
        shapes.append(sh)
        if moving:
            anim.append(sh)
    g = []
    if k == "side":
        g += _side_base(view, V)
    elif k in ("front", "pair"):
        g += _front_base(view, v)
    else:
        g += _port_base(view, V)
    static = "".join(_svg_of(sh, sh["keys"][0]) for sh in shapes if not sh["anim"])
    if k == "side":
        g.insert(len(g) - 1, static)            # 基図の切り抜きの中（船体の線の前・水の線の前）
    else:
        g.append(static)
    if k == "side":
        g += _deck_labels(view, V)
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, v["lab"], 1000, cap=28, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, V, steps)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="hull", view=view, start=start, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(st) for st in steps])
    return f
