# -*- coding: utf-8 -*-
"""mech23.py — 23本目（三豊百貨店崩壊事故のリメイク）「模式図」（2026-10-18 新設・⑤b-3）。

■ 何か
  22本目 `mech22` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。再現イラストではない＝「再現」の札は出さない。
  🔴 **左上の札＝見る向きの合図**（「横から見た…」「上から見た…」「斜めから見た…」＝映像方針の一覧の「見る向き」と同じ頭の語。門番 check_mech が
     PLAN の「見る向き：」と照らす）。左下に「模式」と出典。🔴 人の形・顔・私人の名前は描かない（会議は机と役職の札だけ）。
  🔴 **色は役の色**（`jiko_style.ROLE`＝会社 company 橙・区 ward 緑・市 city 紫・国〈国会・検察・裁判所〉state 青・構造技術者 engineer 水色・
     **A棟 bldg_a ピンク**・B棟＝主図形の白 INK_W）。赤＝崩れる・欠陥／黄＝数（据え置き）。門番 check_mech の judge_m23 が記録の表（REC_M23）で照らす（§5b-88）

■ 章をまたぐ型（⑤b-3 で立てた・⑤b-4〜6 で欄を足して使い回す＝22本目の時間の帯と同じ）
  section … 横から見た建物の断面（ソウル市の報告 p.34 の断面図の描き起こし＝A棟〈北・左〉・つなぎの通路・B棟〈南・右〉・地上5階・地下4階・
            各階の使い道）。部品＝A棟の床の板8枚と階の帯（崩れる順＝屋上と5階の床が先・下の階が次々に＝国会の報告 p.28）   c202・c209・c407（c917）
  bldg    … 斜めから見た建物（A棟・つなぎの通路・B棟・地上5階）。階の帯を明るく・閉めた所・札・印                     c204・c218・c317（c609 ほか）
  plan    … 上から見た床（ソウル市の報告 p.34 の平面図の描き起こし＝A棟〈左＝北〉・つなぎの通路・B棟）。屋上のうろこ・沈んだ点・北側の食堂のひび・
            地下1階の通路・柱の並びの一部（判決の列と行の番号）・A棟の跡（北と南の壁）                      c206・c210・c304・c316・c403・c413（c611 ほか）
  slab    … 横から見た床と柱（断面）＝z="span"（柱2本のあいだの床）／z="col"（柱1本のまわり）。沈み・ひび・鉄の梁の補強の予定・押し抜きのせん断
                                                                                                         c207・c212・c310・c404（c715 ほか）
■ 第1〜3章だけの見え方
  tower（c215 冷却塔）・bunko（c213 15センチと文庫本）・crack（c303 床の寄り）・meeting（c301 机と札）・doc（c306 構造技術者の仕事）・
  form（c307 別紙2 の欄＝原文の韓国語のまま・名前と職の欄は出さない）・flow（c312 国会の報告の判断）・table（c315 区の安全点検）・
  clocks（c402・c418 記録ごとの時刻）・night（c420 夜の現場）

■ SPEC の書き方（mech22 と同じ）
  fig=("m23", dict(view=…, start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…, d=…, col=…)), …],
                   rel=[dict(t="8:00", src="K6-R p30")], note="…模式…", src=ss.src([…])))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。札の数・時刻は `rel=` に同じ文字列（門番 check_mech の judge_m23）。
  🔴 記録の値（階の数・使い道・閉めた所・沈んだ点の数・柱の番号・時刻・点検の日付・別紙2 の原文）は門番 check_mech の REC_M23 が別に持つ（§5b-88）。
     描く側の表（SC_USE・CLOSED・SINK_PTS・GRID・CK_SET・FORM・TB_ROWS ほか）を書き換えると鳴る。⚠️ 動く部品は段の層（札）より上に描かれる＝札は動く部品の通り道に置かない
  ⚠️ 札の色の既定は主図形の白（22本目の mech22 は黄）＝黄は数の札だけ（呼ぶ側が col=J.AMBER）
"""
from __future__ import annotations

import math

import fontmetrics as fm
import jiko_style as J
import titan_fig as F
from mech21 import _P, _arrow, _box, _check, _on, _qmark, _xmark

ONOFF = ("off", "on")
INK = J.INK_W
L_X = F.BX0 + 40.0
A_C = J.ROLE["bldg_a"]            # A棟（北・崩れた棟）＝ピンク
B_C = J.INK_W                     # B棟（南・残った棟）＝主図形の白


def rc(r):
    """役の名（ROLE）か意味の色の名（ALERT・LINE…）か #色 → 色の値。"""
    if not r:
        return INK
    if str(r).startswith("#"):
        return r
    return J.ROLE.get(r) or getattr(J, r)


def _tline(x, y, t, cap=30, col=None, anchor="start", mw=600, fam="Noto"):
    return F.txtfit(x, y, t, mw, cap=cap, col=col or INK, anchor=anchor, fam=fam)


def _hatch(x0, y0, x1, y1, step=18.0, col=None, sw=2, op=0.55):
    """斜線の網（左下→右上）。四角の中だけ。"""
    c = col or J.LINE_DIM
    g = []
    w, h = x1 - x0, y1 - y0
    k = -h
    while k < w:
        ax, ay = x0 + max(k, 0.0), y1 - max(-k, 0.0)
        bx = x0 + min(k + h, w)
        by = y1 - (bx - x0 - k)
        g.append(F.line(ax, ay, bx, by, c, sw, op=op))
        k += step
    return "".join(g)


def _zig(x0, y0, x1, y1, n=6, amp=8.0, col=None, sw=4):
    """ひびの線（ジグザグ）。"""
    pts = []
    for i in range(n + 1):
        u = i / n
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        L = math.hypot(x1 - x0, y1 - y0) or 1.0
        nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        s = 0.0 if i in (0, n) else (amp if i % 2 else -amp)
        pts.append((x + nx * s, y + ny * s))
    return F.poly(pts, "none", col or J.ALERT, sw)


def _loop(cx, cy, w, h, col, sw=4):
    """見てまわった印（破線の輪＋矢じり）。"""
    pts = [(cx + w / 2 * math.cos(math.radians(a)), cy + h / 2 * math.sin(math.radians(a))) for a in range(20, 341, 10)]
    g = [F.poly(pts, "none", col, sw, dash="10 8")]
    (ax, ay), (bx, by) = pts[-2], pts[-1]
    g.append(_arrow(ax, ay, bx + (bx - ax) * 0.6, by + (by - ay) * 0.6, col, sw, 16))
    return "".join(g)


def _speaker(cx, cy, s=22.0, col=None, dash=None):
    c = col or INK
    body = [(cx - s, cy - s * 0.45), (cx - s * 0.4, cy - s * 0.45), (cx + s * 0.4, cy - s), (cx + s * 0.4, cy + s), (cx - s * 0.4, cy + s * 0.45),
            (cx - s, cy + s * 0.45)]
    g = [F.poly(body, "none", c, 3, close=True, dash=dash)]
    for r in (0.8, 1.3):
        g.append(F.poly([(cx + s * 0.4 + s * r * math.cos(math.radians(a)), cy + s * r * math.sin(math.radians(a))) for a in range(-40, 41, 10)],
                        "none", c, 3, dash=dash))
    return "".join(g)


def _moon(cx, cy, r=26.0, col=None):
    c = col or INK
    return (F.circ(cx, cy, r, c, None) + F.circ(cx + r * 0.45, cy - r * 0.25, r * 0.9, J.BG, None))


# ══════════════════════════════════════════════════════════
#  section（横から見た建物の断面）＝ソウル市の報告 p.34 の断面図の描き起こし（A棟が左＝北・B棟が右＝南）
# ══════════════════════════════════════════════════════════
#   幅の比は断面図の描き方のまま（A 475：通路 120：B 385 を 1070 画素に）・階の高さは模式（そろえた）。地下1〜3階は全体の下・地下4階は真ん中だけ（図のまま）。
#   右の x 1360〜 は札の列（建物の上と左は棟の名と階の名で埋まる）
SC = dict(xa=(240.0, 760.0), xc=(760.0, 890.0), xb=(890.0, 1310.0), roof=330.0, fh=52.0, core=26.0, b4=(541.0, 1043.0))
SC_ABOVE, SC_BELOW = 5, 4          # 地上5階・地下4階（ソウル市の報告 p.34「지하4층 지상5층」・検察の報告 p.45）
SC_CORE = dict(a=((240.0, 327.0), (677.0, 760.0)), b=((890.0, 961.0), (1245.0, 1310.0)))   # 屋上の両端の高い所（断面図の形＝割合のまま）
# 各階の使い道（断面図の札＝A棟 5階「식당가」・1〜4階「매장」／B棟 4〜5階「운동시설 동」・1〜3階「판매시설」／地下1階「식품」「수퍼마켓」／
#   地下2〜3階「주차장」／地下4階「기계실」）。語りは「食品の売り場」＝地下1階は1つの札
SC_USE = dict(a=(((5, 5), "食堂街"), ((1, 4), "売り場")), b=(((4, 5), "運動の施設"), ((1, 3), "売り場")),
              under=(((-1, -1), "食品の売り場"), ((-2, -2), "駐車場"), ((-3, -3), "駐車場"), ((-4, -4), "機械室")))


def sc_top(L):
    """階 L（5〜1・地下は −1〜−4）の上の端の y。"""
    return SC["roof"] + (SC_ABOVE - L) * SC["fh"] if L > 0 else sc_ground() + (-L - 1) * SC["fh"]


def sc_ground():
    return SC["roof"] + SC_ABOVE * SC["fh"]


def sc_mid(L0, L1):
    return (sc_top(max(L0, L1)) + sc_top(min(L0, L1)) + SC["fh"]) / 2


SC_SLABS = (5, 4, 3, 2, 1, -1, -2)   # A棟の床の板（屋上＝5階の上の端・5〜1階の床・地下1・2階の床）＝崩れて地下3階の床へ
SC_PILE_Y = None                     # 下で計算（地下3階の床の上）


def _sc_slab_y(i):
    """i 番目の床の板の上の端（0＝屋上の板）。"""
    return SC["roof"] if i == 0 else sc_top(SC_SLABS[i - 1]) + SC["fh"]


SC_NSLAB = len(SC_SLABS) + 1        # 屋上＋7枚＝8枚


def sc_parts(st):
    """A棟の階の帯（薄いピンク）・床の板・つなぎの通路（動く部品）。fall＝none→top（屋上と5階の床が落ちる）→all（地下3階の床まで）"""
    x0, x1 = SC["xa"]
    fall = st["fall"]
    ps = []
    lit = 0.24 if st["a"] == "on" else 0.10
    for L in (5, 4, 3, 2, 1):
        gone = fall == "all" or (fall == "top" and L == 5)
        y = sc_top(L)
        ps.append(_P(f"band{L}", "poly", [(x0, y), (x1, y), (x1, y + SC["fh"]), (x0, y + SC["fh"])], fill=A_C, stroke=None,
                     alpha=0.0 if gone else lit))
    for (c0, c1) in SC_CORE["a"]:
        ps.append(_P(f"core{int(c0)}", "poly", [(c0, SC["roof"] - SC["core"]), (c1, SC["roof"] - SC["core"]), (c1, SC["roof"]), (c0, SC["roof"])],
                     fill=A_C, stroke=A_C, w=3, alpha=0.0 if fall != "none" else (0.5 if st["a"] == "on" else 0.25)))
    th = 8.0
    bottom = sc_top(-3) + SC["fh"]           # 地下3階の床（の上の端）
    for i in range(SC_NSLAB):
        y = _sc_slab_y(i) - th / 2
        if fall == "all":
            k = SC_NSLAB - 1 - i                 # 下の板から積む（屋上の板がいちばん上）
            yy = bottom - th - k * (th + 5)
            tl = (-1) ** i * 5.0
            pts = [(x0 + 10, yy - tl), (x1 - 10, yy + tl), (x1 - 10, yy + th + tl), (x0 + 10, yy + th - tl)]
        elif fall == "top" and i in (0, 1):
            base = sc_top(4) - th            # 4階の床の上の端の上に重なる
            yy = base - (1 - i) * (th + 5)
            tl = 7.0 if i == 0 else -5.0
            pts = [(x0 + 6, yy - tl), (x1 - 6, yy + tl), (x1 - 6, yy + th + tl), (x0 + 6, yy + th - tl)]
        else:
            pts = [(x0, y), (x1, y), (x1, y + th), (x0, y + th)]
        # 🔧 試し焼き（10-18）：落ちる前の板まで赤にすると全部の階が先に崩れたように見えた＝落ちた板だけ赤
        col = J.ALERT if (fall == "all" or (fall == "top" and i in (0, 1))) else A_C
        ps.append(_P(f"slab{i}", "poly", pts, fill=col, stroke=None, alpha=1.0 if fall != "none" or st["a"] == "on" else 0.55))
    c0, c1 = SC["xc"]
    ps.append(_P("conn", "poly", [(c0, SC["roof"]), (c1, SC["roof"]), (c1, sc_ground()), (c0, sc_ground())], fill=J.LINE, stroke=J.LINE, w=3,
                 alpha=0.0 if fall == "all" else 0.16))
    return ps


def section_base(st0):
    g = []
    x0, x1 = SC["xa"][0], SC["xb"][1]
    gy = sc_ground()
    # 地下1〜3階（全体）・地下4階（真ん中）
    for L in (-1, -2, -3):
        g.append(F.rect(x0, sc_top(L), x1 - x0, SC["fh"], J.BG2, J.LINE, 3))
    b40, b41 = SC["b4"]
    g.append(F.rect(b40, sc_top(-4), b41 - b40, SC["fh"], J.BG2, J.LINE, 3))
    # A棟・通路の外形（崩れたあとも見える薄い破線）
    a0, a1 = SC["xa"]
    (ac0, ac1), (ad0, ad1) = SC_CORE["a"]
    ga = [(a0, gy), (a0, SC["roof"] - SC["core"]), (ac1, SC["roof"] - SC["core"]), (ac1, SC["roof"]), (ad0, SC["roof"]),
          (ad0, SC["roof"] - SC["core"]), (a1, SC["roof"] - SC["core"]), (a1, gy)]
    g.append(F.poly(ga, "none", A_C, 4))
    c0, c1 = SC["xc"]
    g.append(F.poly([(c0, SC["roof"]), (c1, SC["roof"]), (c1, gy)], "none", J.LINE, 3))
    # B棟（白）
    b0, b1 = SC["xb"]
    (bc0, bc1), (bd0, bd1) = SC_CORE["b"]
    gb = [(b0, gy), (b0, SC["roof"] - SC["core"]), (bc1, SC["roof"] - SC["core"]), (bc1, SC["roof"]), (bd0, SC["roof"]),
          (bd0, SC["roof"] - SC["core"]), (b1, SC["roof"] - SC["core"]), (b1, gy)]
    g.append(F.poly(gb + [(b0, gy)], J.BG2, B_C, 4, close=True))
    for L in (4, 3, 2, 1):
        g.append(F.line(b0, sc_top(L), b1, sc_top(L), J.LINE_DIM, 2))
    for L in (4, 3, 2):
        g.append(F.line(a0, sc_top(L), a1, sc_top(L), J.LINE_DIM, 2, dash="6 6"))
    g.append(F.line(a0 - 60, gy, b1 + 30, gy, J.LINE, 4))
    # 階の名（左）・屋上・棟の名
    xl = a0 - 14
    g.append(_tline(xl, SC["roof"] - 4, "屋上", 22, J.TICK, "end", 120))
    for L in (5, 4, 3, 2, 1):
        g.append(_tline(xl, sc_top(L) + SC["fh"] / 2 + 8, f"{L}階", 22, J.TICK, "end", 120))
    for L in (-1, -2, -3, -4):
        g.append(_tline(xl if L > -4 else b40 - 12, sc_top(L) + SC["fh"] / 2 + 8, f"地下{-L}階", 22, J.TICK, "end", 160))
    g.append(_tline((a0 + a1) / 2, SC["roof"] - SC["core"] - 14, "A棟（北）", 30, A_C, "middle", 300))
    g.append(_tline((b0 + b1) / 2, SC["roof"] - SC["core"] - 14, "B棟（南）", 30, B_C, "middle", 300))
    g.append(_tline((c0 + c1) / 2, SC["roof"] + 34, "通路", 22, J.TICK, "middle", 150))
    return g


def _sc_use(wing):
    xs = dict(a=SC["xa"], b=SC["xb"], under=(SC["xa"][0], SC["xb"][1]))[wing]
    out = []
    for (l0, l1), t in SC_USE[wing]:
        x0, x1 = xs if not (wing == "under" and l0 == -4) else SC["b4"]
        # ⚠️ geom_gap：幾つかの階にまたがる札を真ん中の高さに置くと階の線が字を貫いた＝1つの階の帯の真ん中へ（偶数の階は上の帯・奇数は真ん中の帯）
        k = l1 - l0 + 1
        L = l1 if k % 2 == 0 else l0 + k // 2
        # 🔧 試し焼き（10-18）：1〜4階の「売り場」を4階の帯に置くと4階だけの札に読めた＝幾つかの階の札には階の幅を添える
        rng = "" if k == 1 else (f"（{l0}・{l1}階）" if k == 2 else f"（{l0}〜{l1}階）")
        out.append((t + rng, ((x0 + x1) / 2, sc_top(L) + SC["fh"] / 2 + 9), (l0, l1)))
    return out


def section_stage(prev, st):
    s = []
    for wing, f_ in (("a", "a"), ("b", "b"), ("under", "under")):
        if _on(prev, st, f_):
            col = A_C if wing == "a" else INK
            if wing == "b":
                b0, b1 = SC["xb"]
                s.append(F.rect(b0, SC["roof"], b1 - b0, sc_ground() - SC["roof"], INK, None, op=0.10))
            for t, (x, y), (l0, l1) in _sc_use(wing):
                s.append(_tline(x, y, t, 28 if wing != "under" else 24, col, "middle", 330))
    x0, x1 = SC["xa"]
    # ⚠️ 門番 layout：輪を A棟の真ん中に置くと「食堂街」の札を線が貫いた＝右寄せ（札は真ん中）・止めた所は左
    if _on(prev, st, "look"):            # 見てまわった（会社の人＝橙）：5階と屋上
        s.append(_loop(x1 - 100, sc_top(5) + SC["fh"] / 2, 170.0, 34.0, J.COMPANY))
        s.append(_loop(x1 - 100, SC["roof"] - 2, 170.0, 22.0, J.COMPANY))
    if _on(prev, st, "keep"):            # 一部の食堂に人を入れない（場所は模式）
        y = sc_top(5)
        s.append(F.rect(x0 + 20, y + 6, 100.0, SC["fh"] - 12, "none", J.COMPANY, 4, dash="8 6"))
    if _on(prev, st, "load"):            # 重さが増えた階（屋上と5階）＝崩れたあとの元の場所に赤の破線
        s.append(F.rect(x0 + 4, SC["roof"] - SC["core"], x1 - x0 - 8, SC["core"] + 8, "none", J.ALERT, 4, dash="10 8"))
        s.append(F.rect(x0 + 4, sc_top(5) + 4, x1 - x0 - 8, SC["fh"] - 4, "none", J.ALERT, 4, dash="10 8"))
    return s


# ══════════════════════════════════════════════════════════
#  bldg（斜めから見た建物）＝A棟（ピンク）・つなぎの通路・B棟（白）・地上5階（幅の比は平面図の描き方・高さと奥行きは模式）
# ══════════════════════════════════════════════════════════
BL = dict(g=810.0, fh=78.0, xa=(330.0, 800.0), xc=(800.0, 910.0), xb=(910.0, 1280.0), d=(140.0, -96.0))
BL_N = 5
# 閉めた所（検察の報告 p.47「5층 식당 대부분, 신용판매부, 4층 귀금속 코너 영업 중단」）＝帯の中の割合（場所と広さは模式）
CLOSED = dict(a5=(0.10, 0.90), a4=(0.55, 0.72))
CELL = dict(a5=(0.22, 0.40))       # 5階の食堂の1つ（c204＝場所は模式）
HI = dict(none=(), a5=(("a", 5),), low=(("a", 1), ("a", 2), ("a", 3), ("b", 1), ("b", 2), ("b", 3)))


def bl_y(L):
    """階 L の上の端の y（前の面）。"""
    return BL["g"] - L * BL["fh"]


def bl_x(w):
    return BL["x" + w]


def bl_band(w, L, f0=0.0, f1=1.0):
    x0, x1 = bl_x(w)
    a, b = x0 + (x1 - x0) * f0, x0 + (x1 - x0) * f1
    y0 = bl_y(L)
    return [(a, y0), (b, y0), (b, y0 + BL["fh"]), (a, y0 + BL["fh"])]


def bldg_base(st0):
    g = []
    dx, dy = BL["d"]
    top = bl_y(BL_N)
    gy = BL["g"]
    bx0, bx1 = bl_x("b")
    # B棟の右の面・3つの上の面
    g.append(F.poly([(bx1, top), (bx1 + dx, top + dy), (bx1 + dx, gy + dy), (bx1, gy)], J.BG2, B_C, 3, close=True, op=None))
    for w, c in (("a", A_C), ("c", J.LINE), ("b", B_C)):
        x0, x1 = bl_x(w)
        g.append(F.poly([(x0, top), (x1, top), (x1 + dx, top + dy), (x0 + dx, top + dy)], J.BG2, c, 3, close=True))
    for w, c in (("a", A_C), ("c", J.LINE), ("b", B_C)):
        x0, x1 = bl_x(w)
        g.append(F.rect(x0, top, x1 - x0, gy - top, J.BG2, c, 4 if w != "c" else 3))
        for L in range(1, BL_N):
            g.append(F.line(x0, bl_y(L), x1, bl_y(L), J.LINE_DIM, 2))
    for L in range(1, BL_N):
        g.append(F.line(bx1, bl_y(L), bx1 + dx, bl_y(L) + dy, J.LINE_DIM, 2))
    g.append(F.line(BL["xa"][0] - 60, gy, bx1 + dx + 60, gy, J.LINE, 4))
    for L in range(1, BL_N + 1):
        g.append(_tline(BL["xa"][0] - 16, bl_y(L) + BL["fh"] / 2 + 9, f"{L}階", 24, J.TICK, "end", 120))
    a0, a1 = bl_x("a")
    g.append(_tline((a0 + a1) / 2 + dx / 2, top + dy - 14, "A棟（北）", 30, A_C, "middle", 300))
    g.append(_tline((bx0 + bx1) / 2 + dx / 2, top + dy - 14, "B棟（南）", 30, B_C, "middle", 300))
    return g


def bldg_parts(st):
    """階の帯（明るくする所）＝動く部品（薄れて出る）。"""
    ps = []
    lit = set(HI[st["hi"]])
    for w in ("a", "b"):
        for L in range(1, BL_N + 1):
            on = (w, L) in lit
            ps.append(_P(f"hi_{w}{L}", "poly", bl_band(w, L), fill=A_C if w == "a" else INK, stroke=None, alpha=0.30 if on else 0.0))
    return ps


def bldg_stage(prev, st):
    s = []
    if _on(prev, st, "cell"):
        p = bl_band("a", 5, *CELL["a5"])
        s.append(F.poly(p, "none", J.ALERT, 5, close=True))
    if _on(prev, st, "bulge"):         # 床が盛り上がる（下から上へ）・天井が沈む（上から下へ）＝赤
        p = bl_band("a", 5, *CELL["a5"])
        x0, x1 = p[0][0], p[1][0]
        y0, y1 = p[0][1], p[2][1]
        s.append(_arrow(x0 + (x1 - x0) * 0.32, y1 - 6, x0 + (x1 - x0) * 0.32, y1 - 34, J.ALERT, 6, 18))
        s.append(_arrow(x0 + (x1 - x0) * 0.68, y0 + 6, x0 + (x1 - x0) * 0.68, y0 + 34, J.ALERT, 6, 18))
    if _on(prev, st, "roof"):          # 5階の天井＝屋上の床の裏（A棟の屋上の板を明るく）
        a0, a1 = bl_x("a")
        y = bl_y(BL_N)
        s.append(F.rect(a0, y - 5, a1 - a0, 10, A_C, None))
    if _on(prev, st, "closed"):        # 閉めた所（網）・開いていた所（ほかの帯）
        for key, (f0, f1) in CLOSED.items():
            w, L = key[0], int(key[1])
            p = bl_band(w, L, f0, f1)
            s.append(F.poly(p, J.BG, J.TICK, 3, close=True))
            s.append(_hatch(p[0][0], p[0][1], p[1][0], p[2][1], 16.0, J.TICK, 2, 0.8))
    if _on(prev, st, "open"):
        for w in ("a", "b"):
            for L in range(1, BL_N + 1):
                if w == "a" and L in (4, 5):
                    continue
                s.append(F.poly(bl_band(w, L), INK, None, op=0.14, close=True))
    if _on(prev, st, "spk"):           # 案内の放送（スピーカー）＝使われなかった＝破線
        for w in ("a", "b"):
            x0, x1 = bl_x(w)
            for L in range(1, BL_N + 1):
                s.append(_speaker(x0 + 34, bl_y(L) + BL["fh"] / 2, 16.0, INK, dash="5 4"))
    if _on(prev, st, "exit"):          # 外へ出る矢印（破線＝出さなかった）
        for x in (bl_x("a")[0] + 120, bl_x("c")[0] + 55, bl_x("b")[1] - 120):
            s.append(_arrow(x, BL["g"] - 30, x, BL["g"] + 46, INK, 5, 18, dash="8 6"))
    if _on(prev, st, "x"):
        s.append(_xmark(1380.0, 600.0, 34.0, J.ALERT, 10))
    return s


# ══════════════════════════════════════════════════════════
#  plan（上から見た床）＝ソウル市の報告 p.34 の平面図の描き起こし（A棟が左＝北・B棟が右＝南・幅の比は図のまま）
# ══════════════════════════════════════════════════════════
#   幅の比は平面図の描き方のまま（A 610：通路 165：B 425 を 1100 画素に・縦はその比）。右の x 1390〜 は札の列
PL = dict(xa=(240.0, 799.0), xc=(799.0, 950.0), xb=(950.0, 1340.0), y=(410.0, 758.0), yc=(438.0, 730.0))
PL_FLOOR = dict(roof="屋上", f5="5階の床", b1="地下1階の床", site="崩れたあとの現場")
SINK_PTS = ((0.24, 0.30), (0.46, 0.66), (0.70, 0.36), (0.84, 0.74))   # 屋上の4か所（検察の報告 p.47「옥상 바닥 4곳」）＝場所は模式（A棟の中の割合）
NORTH_SIDE = (0.0, 0.5)            # 5階の北側（A棟の左半分）＝割合（模式）
GOODS = ((0.30, 0.50), (0.42, 0.50), (0.58, 0.50))   # 地下1階の通路の商品（区の報告 p.45「지하1층 통로상에 상품 적치」）＝場所は模式（全体の割合）
B1_CHK = ("消防の受け持ち", "電気の受け持ち", "昇降機の受け持ち")    # 区の報告 p.45「소방, 전기 및 승강기 안전관리자 상근」
# 柱の並びの一部（判決 大96 理由1「5열 E행, 5열 F행」・同じ理由の「4열 E행」「4열 G행」）＝番号は判決の書き方・間隔と向きは模式
GRID = dict(cols=("4", "5"), rows=("E", "F", "G"), x=(640.0, 800.0), y=(480.0, 600.0, 720.0), win=(400.0, 1040.0, 410.0, 790.0),
            dash=(480.0, 960.0))
GRID_HIT = (("5", "E"), ("5", "F"))


def pl_rect(w):
    x0, x1 = PL["x" + w]
    y0, y1 = PL["yc"] if w == "c" else PL["y"]
    return x0, y0, x1, y1


def pl_pt(fx, fy, w="a"):
    x0, y0, x1, y1 = pl_rect(w)
    return x0 + (x1 - x0) * fx, y0 + (y1 - y0) * fy


def grid_xy(c, r):
    return GRID["x"][GRID["cols"].index(c)], GRID["y"][GRID["rows"].index(r)]


def plan_base(st0):
    g = []
    fl = st0["floor"]
    if fl in ("area", "ct"):        # 🆕 ⑤b-4：全部の階を足した広さ・屋上の置き場（向きは模式＝北の印を描かない）
        return plan_extra_base(st0)
    if fl in ("two", "three"):      # 🆕 ⑤b-5：床を並べる（棟と向きは描かない）
        return plan_b5_base(st0)
    # 北の向き（A棟の側＝左）＝左下
    g.append(_arrow(230.0, 810.0, 130.0, 810.0, J.TICK, 4, 16))
    g.append(_tline(242.0, 820.0, "北", 28, J.TICK, "start", 60))
    if fl == "grid":
        x0, x1, y0, y1 = GRID["win"]
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, A_C, 3, dash="12 8"))
        for x in GRID["dash"]:
            g.append(F.line(x, y0, x, y1, J.LINE_DIM, 2, dash="6 6"))
        for x in GRID["x"]:
            g.append(F.line(x, y0, x, y1, J.LINE, 2))
        for y in GRID["y"]:
            g.append(F.line(x0, y, x1, y, J.LINE, 2))
        for x in GRID["dash"]:
            for y in GRID["y"]:
                g.append(F.rect(x - 10, y - 10, 20, 20, J.LINE_DIM, None))
        for x in GRID["x"]:
            for y in GRID["y"]:
                g.append(F.rect(x - 14, y - 14, 28, 28, INK, None))
        return g
    if fl == "b1":                  # 地下1階＝全体が1つの床（上の棟の境は破線）
        x0, y0, _, y1 = pl_rect("a")
        x1 = PL["xb"][1]
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 4))
        for x in (PL["xa"][1], PL["xb"][0]):
            g.append(F.line(x, y0, x, y1, J.LINE_DIM, 2, dash="8 8"))
        g.append(_tline((PL["xa"][0] + PL["xa"][1]) / 2, y0 + 34, "A棟の下", 24, A_C, "middle", 300))
        g.append(_tline((PL["xb"][0] + PL["xb"][1]) / 2, y0 + 34, "B棟の下", 24, J.TICK, "middle", 300))
        return g
    for w, c in (("c", J.LINE), ("b", B_C)):
        x0, y0, x1, y1 = pl_rect(w)
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, c, 4 if w == "b" else 3, dash="10 8" if (w == "c" and fl == "site") else None))
    x0, y0, x1, y1 = pl_rect("a")
    g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, A_C, 4, dash="12 8" if fl == "site" else None))
    # ⚠️ geom_gap：棟の名を床の中の左上に置くと、うろこ・仕切り・壁の線が字を貫いた＝床の外の上の真ん中へ
    g.append(_tline((x0 + x1) / 2, y0 - 14, "A棟", 26, A_C, "middle", 120))
    bx0, by0, bx1, _ = pl_rect("b")
    g.append(_tline((bx0 + bx1) / 2, by0 - 14, "B棟", 26, B_C, "middle", 120))
    cx0, cy0, cx1, _ = pl_rect("c")
    g.append(_tline((cx0 + cx1) / 2, cy0 + 34, "通路", 22, J.TICK, "middle", 150))
    if fl == "site":
        g.append(_hatch(x0 + 30, y0 + 8, x1 - 30, y1 - 8, 22.0, J.TICK, 2, 0.6))
    return g


def plan_stage(prev, st):
    s = []
    x0, y0, x1, y1 = pl_rect("a")
    if _on(prev, st, "scale"):         # 魚のうろこのように浮き上がる（国会の報告 p.30 の言葉の絵）＝A棟の屋上に弧の並び
        r = 30.0
        for j, y in enumerate(range(int(y0 + 40), int(y1 - 20), 34)):
            off = (j % 2) * r
            x = x0 + 30 + off
            while x < x1 - 30:
                s.append(F.poly([(x - r + 2 * r * k / 8, y - math.sin(math.pi * k / 8) * 16) for k in range(9)], "none", A_C, 3))
                x += 2 * r
    if _on(prev, st, "sag"):           # 一部がたわむ（場所は模式）
        cx, cy = pl_pt(0.62, 0.55)
        s.append(F.poly([(cx + 90 * math.cos(math.radians(a)), cy + 56 * math.sin(math.radians(a))) for a in range(0, 361, 12)],
                        J.BG, J.ALERT, 5, dash="10 8"))
        s.append(_arrow(cx, cy - 22, cx, cy + 26, J.ALERT, 6, 18))
    if _on(prev, st, "north"):         # 5階の北側の食堂（A棟の左半分）
        f0, f1 = NORTH_SIDE
        s.append(F.rect(x0 + (x1 - x0) * f0, y0, (x1 - x0) * (f1 - f0), y1 - y0, A_C, None, op=0.22))
        for k in range(1, 4):                       # 食堂の仕切りの壁（模式）
            yy = y0 + (y1 - y0) * k / 4
            s.append(F.line(x0, yy, x0 + (x1 - x0) * f1, yy, INK, 3))
        s.append(F.line(x0 + (x1 - x0) * f1, y0, x0 + (x1 - x0) * f1, y1, INK, 3))
    if _on(prev, st, "crack"):         # 壁と床のひび（北側・場所は模式）
        f1 = NORTH_SIDE[1]
        for k in range(4):
            yy = y0 + (y1 - y0) * (k + 0.5) / 4
            s.append(_zig(x0 + 40, yy - 14, x0 + (x1 - x0) * f1 - 50, yy + 12, 7, 7.0, J.ALERT, 4))
        for k in range(1, 4):
            yy = y0 + (y1 - y0) * k / 4
            s.append(_zig(x0 + 70 + 60 * k, yy - 9, x0 + 120 + 60 * k, yy + 9, 3, 5.0, J.ALERT, 4))
    if _on(prev, st, "start"):         # のちに崩れはじめる側（赤の破線）
        f0, f1 = NORTH_SIDE
        s.append(F.rect(x0 + (x1 - x0) * f0 + 6, y0 + 6, (x1 - x0) * (f1 - f0) - 12, y1 - y0 - 12, "none", J.ALERT, 5, dash="12 8"))
    if _on(prev, st, "sink"):          # 屋上の4か所の沈み（場所は模式）
        for fx, fy in SINK_PTS:
            cx, cy = pl_pt(fx, fy)
            s.append(F.circ(cx, cy, 22, "none", J.ALERT, 6))
            s.append(F.circ(cx, cy, 7, J.ALERT, None))
    if _on(prev, st, "goods", "on"):   # 地下1階の通路の商品（区の指摘）
        bx0, by0 = PL["xa"][0], PL["y"][0]
        bx1, by1 = PL["xb"][1], PL["y"][1]
        yc = by0 + (by1 - by0) * 0.5
        s.append(F.rect(bx0 + 40, yc - 34, bx1 - bx0 - 80, 68, "none", J.LINE, 3, dash="10 8"))
        s.append(_tline(bx0 + 56, yc - 46, "通路", 22, J.TICK, "start", 120))
    if _on(prev, st, "goods", "fixed"):   # その場で直させた（区＝緑）
        bx0, by0 = PL["xa"][0], PL["y"][0]
        bx1, by1 = PL["xb"][1], PL["y"][1]
        x = bx0 + (bx1 - bx0) * GOODS[1][0]
        s.append(_check(x, by0 + (by1 - by0) * 0.5, 30, J.OK))
    if _on(prev, st, "chk"):            # 区が確かめた受け持ち（右の札の列）
        for i, t in enumerate(B1_CHK):
            y = 640.0 + i * 70.0                 # ⚠️ 門番 layout：560 からだと r2 の札に 7px 重なった
            s.append(_check(1410.0, y - 10, 18, J.OK))
            s.append(_tline(1442.0, y, t, 28, J.OK, "start", 400))
    if _on(prev, st, "nums"):          # 列と行の番号（判決の書き方）
        for c, x in zip(GRID["cols"], GRID["x"]):
            s.append(_tline(x, GRID["win"][2] - 16, f"{c}列", 28, INK, "middle", 120))
        for r_, y in zip(GRID["rows"], GRID["y"]):
            s.append(_tline(GRID["win"][0] - 18, y + 10, f"{r_}行", 28, INK, "end", 120))
    if _on(prev, st, "hit"):
        for c, r_ in GRID_HIT:
            x, y = grid_xy(c, r_)
            s.append(F.circ(x, y, 40, "none", J.ALERT, 7))
    if _on(prev, st, "walls"):         # A棟の跡に残った北側と南側の壁（ソウル市の報告 p.37・p.39）
        s.append(F.rect(x0 - 8, y0 - 6, 22, y1 - y0 + 12, A_C, None))
        s.append(F.rect(x1 - 14, y0 - 6, 22, y1 - y0 + 12, A_C, None))
    if _on(prev, st, "rubble"):        # 壁から離れて落ちた床（瓦礫）
        s.append(F.rect(x0 + 40, y0 + 16, x1 - x0 - 80, y1 - y0 - 32, J.ALERT, None, op=0.22))
        for xx in (x0 + 40, x1 - 40):
            s.append(F.line(xx, y0 + 16, xx, y1 - 16, J.ALERT, 4, dash="8 6"))
    return s


def plan_parts(st):
    """地下1階の通路の商品（直させた＝消える）。"""
    if st["floor"] != "b1":
        return []
    bx0, by0 = PL["xa"][0], PL["y"][0]
    bx1, by1 = PL["xb"][1], PL["y"][1]
    yc = by0 + (by1 - by0) * 0.5
    ps = []
    a = 0.0 if st["goods"] in ("off", "fixed") else 1.0
    for i, (fx, _fy) in enumerate(GOODS):
        x = bx0 + (bx1 - bx0) * fx
        ps.append(_P(f"goods{i}", "poly", [(x - 46, yc - 24), (x + 46, yc - 24), (x + 46, yc + 24), (x - 46, yc + 24)], fill=J.DOC, stroke=INK, w=3,
                     alpha=a))
    return ps


# ══════════════════════════════════════════════════════════
#  slab（横から見た床と柱）＝z="span"（柱2本のあいだ）／z="col"（柱1本のまわり）。厚さ・沈みの大きさは誇張（模式）
# ══════════════════════════════════════════════════════════
SLS = dict(x0=260.0, x1=1660.0, top=480.0, th=44.0, cols=(560.0, 1360.0), cw=64.0, up=300.0, low=840.0, sag=34.0, n=40)
SLC = dict(x0=300.0, x1=1620.0, top=470.0, th=56.0, cx=960.0, cw=96.0, up=290.0, low=840.0, sink=18.0, drop=150.0)


def _sls_edge(y, sag):
    c0, c1 = SLS["cols"]
    pts = []
    for i in range(SLS["n"] + 1):
        x = SLS["x0"] + (SLS["x1"] - SLS["x0"]) * i / SLS["n"]
        d = sag * math.sin(math.pi * (x - c0) / (c1 - c0)) if c0 < x < c1 else 0.0
        pts.append((x, y + d))
    return pts


def slab_parts(st):
    if st["z"] == "span":
        sag = SLS["sag"] if st["sag"] == "on" else 0.0
        top = _sls_edge(SLS["top"], sag)
        bot = _sls_edge(SLS["top"] + SLS["th"], sag)
        return [_P("slab", "poly", top + list(reversed(bot)), fill=J.BG2, stroke=J.LINE, w=4)]
    cx, cw, th, top = SLC["cx"], SLC["cw"], SLC["th"], SLC["top"]
    x0, x1 = SLC["x0"], SLC["x1"]
    s_ = SLC["sink"] if st["sink"] == "on" else 0.0
    dr = SLC["drop"] if st["punch"] == "on" else 0.0
    L = [(x0, top), (cx - cw / 2 - th, top + s_), (cx - cw / 2, top + th + s_), (x0, top + th)]
    R = [(cx + cw / 2 + th, top + s_), (x1, top), (x1, top + th), (cx + cw / 2, top + th + s_)]
    if dr:
        L = [(x + 0.0, y + dr + (x - x0) * 0.05) for x, y in L]
        R = [(x + 0.0, y + dr + (x1 - x) * 0.05) for x, y in R]
    return [_P("slabL", "poly", L, fill=J.BG2, stroke=J.LINE, w=4), _P("slabR", "poly", R, fill=J.BG2, stroke=J.LINE, w=4)]


def slab_base(st0):
    g = []
    if st0["z"] == "span":
        for c in SLS["cols"]:
            g.append(F.rect(c - SLS["cw"] / 2, SLS["up"], SLS["cw"], SLS["top"] - SLS["up"], J.BG2, J.LINE, 4))
            g.append(F.rect(c - SLS["cw"] / 2, SLS["top"] + SLS["th"], SLS["cw"], SLS["low"] - SLS["top"] - SLS["th"], J.BG2, J.LINE, 4))
        if st0["fl"] != "none":
            up, dn = (("屋上の床", "5階の天井") if st0["fl"] == "roof" else (f"{int(st0['fl'])}階の床", f"{int(st0['fl']) - 1}階の天井"))
            g.append(_tline(SLS["x0"] + 10, SLS["top"] - 18, up, 28, INK, "start", 300))
            g.append(_tline(SLS["x0"] + 10, SLS["top"] + SLS["th"] + 46, dn, 28, INK, "start", 300))
        return g
    cx, cw = SLC["cx"], SLC["cw"]
    # 柱（上と下）＋柱の頭の板の芯（押し抜きで柱に残る部分＝動かない）。🆕 ⑤b-5：屋上の床（ca03）は上に柱が無い
    if st0["fl"] != "roof":
        g.append(F.rect(cx - cw / 2, SLC["up"], cw, SLC["top"] - SLC["up"], J.BG2, J.LINE, 4))
    g.append(F.rect(cx - cw / 2, SLC["top"] + SLC["th"], cw, SLC["low"] - SLC["top"] - SLC["th"], J.BG2, J.LINE, 4))
    th = SLC["th"]
    plug = [(cx - cw / 2 - th - 2, SLC["top"]), (cx + cw / 2 + th + 2, SLC["top"]), (cx + cw / 2 + 2, SLC["top"] + th), (cx - cw / 2 - 2, SLC["top"] + th)]
    g.append(F.poly(plug, J.BG2, None, close=True))
    if st0["fl"] != "none":
        lab = "屋上の床（5階の天井）" if st0["fl"] == "roof" else f"{int(st0['fl'])}階の床"
        g.append(_tline(SLC["x0"] + 10, SLC["top"] - 18, lab, 28, INK, "start", 400))
    return g


def slab_stage(prev, st):
    s = []
    if st["z"] == "span":
        c0, c1 = SLS["cols"]
        mx = (c0 + c1) / 2
        if _on(prev, st, "sag"):        # 元の下の面（破線）と沈み（括弧）
            yb = SLS["top"] + SLS["th"]
            s.append(F.line(c0 + 40, yb, c1 - 40, yb, J.TICK, 3, dash="8 6"))
            s.append(F.line(mx + 150, yb, mx + 150, yb + SLS["sag"] * 0.98, J.ALERT, 4))
            s.append(_arrow(mx, yb + 4, mx, yb + SLS["sag"] - 4, J.ALERT, 5, 14))
        if _on(prev, st, "same"):       # 1枚の板の上と下（5階の床＝4階の天井）
            s.append(F.line(SLS["x0"] + 6, SLS["top"] - 4, c0 - 40, SLS["top"] - 4, A_C, 6))
            s.append(F.line(SLS["x0"] + 6, SLS["top"] + SLS["th"] + 4, c0 - 40, SLS["top"] + SLS["th"] + 4, A_C, 6))
        if st["beam"] == "plan" and prev.get("beam") != "plan":   # 鉄の梁を下から入れる（予定＝破線）・支え
            yb = SLS["top"] + SLS["th"] + SLS["sag"] * (1 if st["sag"] == "on" else 0) + 4
            s.append(F.rect(c0 + 60, yb, c1 - c0 - 120, 34, "none", J.SHIP, 5, dash="12 8"))
            s.append(F.line(c0 + 60, yb + 17, c1 - 60, yb + 17, J.SHIP, 3, dash="12 8"))
            for x in (mx - 200, mx + 200):
                s.append(F.line(x, yb + 34, x, SLS["low"], J.SHIP, 4, dash="12 8"))
        if _on(prev, st, "night"):           # ⚠️ 門番 layout：(1540, 340) だと右の札「技術者の提案」を覆った
            s.append(_moon(1760.0, 420.0, 30.0, INK))
        return s
    cx, cw, th, top = SLC["cx"], SLC["cw"], SLC["th"], SLC["top"]
    if _on(prev, st, "crack"):          # 柱の近くのひび（柱の頭の縁から斜めに＝模式）
        for sg in (-1, 1):
            s.append(_zig(cx + sg * (cw / 2 + th), top + 2, cx + sg * (cw / 2 + 4), top + th - 2, 4, 5.0, J.ALERT, 5))
    if _on(prev, st, "punch"):          # 🔧 試し焼き（10-18）：柱に残る芯（円すいの形）の輪郭＝線が無いと黒い影に見えた
        s.append(F.poly([(cx - cw / 2 - th, top), (cx + cw / 2 + th, top), (cx + cw / 2, top + th), (cx - cw / 2, top + th)], "none", J.ALERT, 4,
                        close=True))
    return s


# ══════════════════════════════════════════════════════════
#  tower（c215・斜めから見た冷却塔）＝冷房の水を外の空気で冷やす装置（形は模式・数と重さは第7章）
# ══════════════════════════════════════════════════════════
TWR = dict(x0=760.0, x1=1100.0, y0=470.0, y1=770.0, d=(110.0, -70.0), roof=800.0)


def tower_base(st0):
    if st0.get("set") == "three":     # 🆕 ⑤b-4：屋上の3基（c803）
        return tower3_base(st0)
    g = []
    x0, x1, y0, y1 = TWR["x0"], TWR["x1"], TWR["y0"], TWR["y1"]
    dx, dy = TWR["d"]
    g.append(F.line(380.0, TWR["roof"], 1560.0, TWR["roof"], J.LINE, 5))
    g.append(_tline(390.0, TWR["roof"] + 34, "屋上の床", 24, J.TICK, "start", 200))
    for x in (x0 + 40, x1 - 40):
        g.append(F.rect(x - 10, y1, 20, TWR["roof"] - y1, J.LINE_DIM, None))
    g.append(F.poly([(x1, y0), (x1 + dx, y0 + dy), (x1 + dx, y1 + dy), (x1, y1)], J.BG2, J.LINE, 3, close=True))
    g.append(F.poly([(x0, y0), (x1, y0), (x1 + dx, y0 + dy), (x0 + dx, y0 + dy)], J.BG2, J.LINE, 3, close=True))
    g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 4))
    for k in range(1, 7):                       # 空気の入るすき間（模式）
        y = y0 + 60 + k * 30
        g.append(F.line(x0 + 30, y, x1 - 30, y, J.LINE_DIM, 3))
    fx, fy = (x0 + x1) / 2 + dx / 2, y0 + dy / 2
    g.append(F.poly([(fx + 110 * math.cos(math.radians(a)), fy + 30 * math.sin(math.radians(a))) for a in range(0, 361, 15)], J.BG2, J.LINE, 4))
    g.append(F.rect(fx - 110, fy - 64, 220, 64, J.BG2, None))
    g.append(F.line(fx - 110, fy - 64, fx - 110, fy, J.LINE, 4))
    g.append(F.line(fx + 110, fy - 64, fx + 110, fy, J.LINE, 4))
    g.append(F.poly([(fx + 110 * math.cos(math.radians(a)), fy - 64 + 30 * math.sin(math.radians(a))) for a in range(0, 361, 15)], J.BG2, J.LINE, 4))
    g.append(_tline((x0 + x1) / 2, y0 + 56, "冷却塔", 30, INK, "middle", 300))   # ⚠️ geom_gap：下に置くと水を抜く受け皿の枠が字を覆った
    # 冷房の水の管（建物の中から来て、冷えて戻る）
    g.append(F.poly([(x1 + 30, y0 + 90), (1340.0, y0 + 90), (1340.0, TWR["roof"])], "none", J.LINE, 6))
    g.append(F.poly([(x0 - 30, y1 - 40), (600.0, y1 - 40), (600.0, TWR["roof"])], "none", J.LINE, 6))
    return g


def tower_parts(st):
    """外の空気の矢印（止めると消える）。"""
    if st.get("set") == "three":
        return []
    a = 0.85 if st["run"] == "on" else 0.0
    fx, fy = (TWR["x0"] + TWR["x1"]) / 2 + TWR["d"][0] / 2, TWR["y0"] + TWR["d"][1] / 2 - 64
    ps = []
    for i, (x, y, ang) in enumerate(((TWR["x0"] - 150, 620.0, 0.0), (fx - 40, fy - 30, -90.0), (fx + 40, fy - 30, -90.0))):
        L, w = 90.0, 10.0
        c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        pts = [(x - s_ * w, y + c * w), (x + c * L - s_ * w, y + s_ * L + c * w), (x + c * (L + 24), y + s_ * (L + 24)),
               (x + c * L + s_ * w, y + s_ * L - c * w), (x + s_ * w, y - c * w)]
        ps.append(_P(f"air{i}", "poly", pts, fill=J.LINE, stroke=None, alpha=a))
    return ps + tower_gauge_parts(st)          # 🆕 ⑤b-5：水位の目盛りの水（ca09）


def tower_stage(prev, st):
    if st.get("set") == "three":
        return tower3_stage(prev, st)
    s = tower_gauge_stage(prev, st)
    fx, fy = (TWR["x0"] + TWR["x1"]) / 2 + TWR["d"][0] / 2, TWR["y0"] + TWR["d"][1] / 2 - 64
    if _on(prev, st, "run", "off"):
        s.append(_xmark(fx, fy - 6, 26.0, J.COMPANY, 9))
    if _on(prev, st, "drain"):          # 水を抜く（下の受け皿から外へ）
        s.append(_arrow(TWR["x0"] + 60, TWR["y1"] - 6, TWR["x0"] + 60, TWR["roof"] - 6, J.COMPANY, 6, 20))
        s.append(F.rect(TWR["x0"] + 10, TWR["y1"] - 46, TWR["x1"] - TWR["x0"] - 20, 34, "none", J.COMPANY, 4, dash="10 6"))
    return s


# ══════════════════════════════════════════════════════════
#  bunko（c213・比べ）＝床の沈み 15センチと文庫本の縦（A6判 105×148ミリ）を同じ縮尺で
# ══════════════════════════════════════════════════════════
BK_PX_CM = 30.0                    # 1センチ＝30画素（模式の縮尺・同じ縮尺で並べる）
BK_SINK_CM = 15.0                  # 5階の柱の近くの床の沈み（国会の報告 p.30「15㎝ 정도」・検察の報告 p.47「15㎝」）
BK_BOOK_MM = (105.0, 148.0)        # 文庫本（A6判）の幅と縦
BK = dict(base=820.0, bx=1040.0, rx=820.0, colx=430.0)


def bunko_base(st0):
    g = []
    w, h = (v / 10 * BK_PX_CM for v in BK_BOOK_MM)
    x, y = BK["bx"], BK["base"] - h
    g.append(F.rect(x, y, w, h, J.BG2, J.DOC, 5, rx=6))
    g.append(F.rect(x + 12, y, 18, h, J.DOC, None, op=0.5))
    g.append(_tline(x + w / 2, y + h / 2, "文庫本", 34, J.DOC, "middle", w - 40))
    return g


def bunko_stage(prev, st):
    s = []
    h = BK_SINK_CM * BK_PX_CM
    if _on(prev, st, "br"):
        x, y1 = BK["rx"], BK["base"]
        y0 = y1 - h
        s.append(F.line(x, y0, x, y1, J.ALERT, 5))
        for y in (y0, y1):
            s.append(F.line(x - 22, y, x + 22, y, J.ALERT, 5))
        bh = BK_BOOK_MM[1] / 10 * BK_PX_CM
        s.append(F.line(BK["bx"] - 24, BK["base"] - bh, BK["bx"] + BK_BOOK_MM[0] / 10 * BK_PX_CM + 24, BK["base"] - bh, J.TICK, 2, dash="6 6"))
    if _on(prev, st, "col"):           # 柱のすぐそばの床（元の高さ＝破線・沈んだ高さ＝赤）
        cx = BK["colx"]
        y1 = BK["base"]
        y0 = y1 - h
        s.append(F.rect(cx - 40, 300.0, 80, 540.0, J.BG2, J.LINE, 4))      # ⚠️ geom_gap：下の端 860 は下の注の行に 3.6px
        s.append(F.line(cx + 40, y0, BK["rx"] - 40, y0, J.TICK, 3, dash="8 6"))
        s.append(F.line(cx + 40, y1, BK["rx"] - 40, y1, J.ALERT, 6))
    return s


# ══════════════════════════════════════════════════════════
#  crack（c303・横から見た5階の床の寄り）＝床のコンクリートのひびが伸びる（ひびの形と深さは模式）
# ══════════════════════════════════════════════════════════
CR = dict(x0=300.0, x1=1620.0, top=480.0, bot=700.0)
CR_PATH = ((960.0, 480.0), (948.0, 520.0), (972.0, 556.0), (954.0, 596.0), (980.0, 636.0), (966.0, 676.0))   # ひびの通り道（模式）


def crack_base(st0):
    g = [F.rect(CR["x0"], CR["top"], CR["x1"] - CR["x0"], CR["bot"] - CR["top"], J.BG2, J.LINE, 4)]
    for k in range(1, 4):
        g.append(F.line(CR["x0"] + 10, CR["top"] + 12 * k, CR["x1"] - 10, CR["top"] + 12 * k, J.LINE_DIM, 1, op=0.5))
    g.append(_tline(CR["x0"] + 10, CR["top"] - 18, ("屋上の床" if st0.get("fl") == "roof" else "5階の床") + "（コンクリート）", 28, INK, "start", 500))
    return g


def _crack_pts(u):
    """ひびの線を u（0〜1）まで伸ばした太い線の多角形（点の数は一定）。"""
    n = len(CR_PATH) - 1
    pts = [CR_PATH[0]]
    for i in range(1, n + 1):
        k = min(1.0, max(0.0, u * n - (i - 1)))          # この区間をどこまで伸ばすか（0〜1）
        (xa, ya), (xb, yb) = CR_PATH[i - 1], CR_PATH[i]
        pts.append((xa + (xb - xa) * k, ya + (yb - ya) * k) if k > 0 else pts[-1])
    left = [(x - 3, y) for x, y in pts]
    right = [(x + 3, y) for x, y in reversed(pts)]
    return left + right


def crack_parts(st):
    u = dict(off=0.0, on=1.0, long=1.0)[st["crack"]]
    return [_P("crack", "poly", _crack_pts(u), fill=J.ALERT, stroke=None, alpha=1.0 if u > 0 else 0.0)] + crack_extra_parts(st)


def crack_stage(prev, st):
    return crack_extra_stage(prev, st)


# ══════════════════════════════════════════════════════════
#  meeting（c301・会議の机と役職の札）＝人は描かない（記録＝14時の対策の会議・社長が会長らに5階のひびを説明）
# ══════════════════════════════════════════════════════════
MT = dict(near=(560.0, 1360.0, 720.0), far=(700.0, 1220.0, 500.0))
#   ⚠️ geom_gap：奥の札を y 512 に置くと机の奥の縁（y 500）が字を貫いた＝机の上（y 566）へ
MT_CARDS = (("社長", 960.0, 668.0), ("会長", 820.0, 566.0), ("役員たち", 1110.0, 566.0))   # 検察の報告 p.47「사장 … 회장 … 등 임원들에게」


def _card_w(t):
    return max(120.0, fm.width(t, 30) + 36)


def meeting_base(st0):
    """机と札（字は基図に1回だけ＝明るくする段は枠だけ＝門番 layout の「同じ字の重ね描き」を避ける）。"""
    (nx0, nx1, ny), (fx0, fx1, fy) = MT["near"], MT["far"]
    g = [F.poly([(fx0, fy), (fx1, fy), (nx1, ny), (nx0, ny)], J.BG2, J.LINE, 4, close=True)]
    for t, x, y in MT_CARDS:
        w = _card_w(t)
        g.append(F.rect(x - w / 2, y - 30, w, 52, J.BG2, J.LINE_DIM, 3, rx=6))
        g.append(_tline(x, y + 6, t, 30, J.COMPANY, "middle", w - 16))
    return g


def meeting_stage(prev, st):
    s = []
    if _on(prev, st, "lit"):
        for t, x, y in MT_CARDS:
            w = _card_w(t)
            s.append(F.rect(x - w / 2, y - 30, w, 52, "none", J.COMPANY, 5, rx=6))
    if _on(prev, st, "tell"):
        sx, sy = MT_CARDS[0][1], MT_CARDS[0][2]
        for _t, x, y in MT_CARDS[1:]:
            s.append(_arrow(sx + (x - sx) * 0.18, sy - 40, x + (sx - x) * 0.18, y + 34, J.COMPANY, 5, 18))
        px, py = 1450.0, 640.0                  # 5階のひびの紙（説明の中身＝赤のひび）
        s.append(F.rect(px, py - 110, 200, 150, J.BG2, J.DOC, 4, rx=6))
        s.append(_zig(px + 30, py - 70, px + 170, py - 20, 6, 8.0, J.ALERT, 4))
        s.append(_tline(px + 100, py + 24, "5階のひび", 26, J.DOC, "middle", 180))
    return s


# ══════════════════════════════════════════════════════════
#  doc（c306・構造技術者の仕事）＝計算書と建物の絵（人の形は描かない）
# ══════════════════════════════════════════════════════════
DC = dict(paper=(380.0, 330.0, 360.0, 470.0), bx=(1080.0, 1520.0), by=(470.0, 800.0))   # ⚠️ geom_gap：建物を下げて重さの矢印（y 390〜）を右上の札から離した


def doc_base(st0):
    g = []
    x0, x1 = DC["bx"]
    y0, y1 = DC["by"]
    g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE_DIM, 3))
    for k in range(1, 5):
        g.append(F.line(x0, y0 + (y1 - y0) * k / 5, x1, y0 + (y1 - y0) * k / 5, J.LINE_DIM, 2))
    for k in range(1, 4):
        g.append(F.line(x0 + (x1 - x0) * k / 4, y0, x0 + (x1 - x0) * k / 4, y1, J.LINE_DIM, 2))
    g.append(F.line(x0 - 60, y1, x1 + 60, y1, J.LINE, 4))
    return g


def doc_stage(prev, st):
    s = []
    if _on(prev, st, "paper"):
        x, y, w, h = DC["paper"]
        s.append(F.rect(x, y, w, h, J.BG2, J.SHIP, 5, rx=6))
        for k in range(7):
            yy = y + 60 + k * 52
            s.append(F.line(x + 40, yy, x + w - 40 - (k % 3) * 40, yy, J.TICK, 3))
        s.append(_tline(x + w / 2, y - 18, "計算書", 30, J.SHIP, "middle", w))
    if _on(prev, st, "load"):
        x0, x1 = DC["bx"]
        y0 = DC["by"][0]
        for k in range(5):
            xx = x0 + (x1 - x0) * k / 4
            s.append(_arrow(xx, y0 - 80, xx, y0 - 8, J.LINE, 5, 18))
        s.append(_qmark(x1 + 90, (y0 + DC["by"][1]) / 2, 70, J.SHIP))
    return s


# ══════════════════════════════════════════════════════════
#  form（c307・検察の報告の別紙2 の欄）＝欄の値は原文の韓国語のまま（訳は字幕）・名前と職の欄は出さない（灰の帯）
# ══════════════════════════════════════════════════════════
#   原文＝国会の会議録 p.52「별지 2」「유지·관리 관련 피의자 및 범죄사항 요지」・欄「성명」「직책」「범죄사항」・構造技術者の行の頭の句。
#   🔴 句の後ろ（2回の診断・15時10分・16時40分の報告）は次のカット（c308・c311）の語り＝出さない（「…」）
FORM = dict(title="별지 2", head="유지·관리 관련 피의자 및 범죄사항 요지", cols=("성명", "직책", "범죄사항"),
            cell=("삼풍백화점의 ‘무량판공법’으로", "계산 설계한 건축구조기술사로서 …"),
            hl=(("‘무량판공법’으로", 0), ("계산 설계한", 1), ("건축구조기술사", 1)))
FM = dict(x0=240.0, x1=1680.0, y0=330.0, cw=(240.0, 300.0), hy=470.0, ry0=500.0, ry1=760.0, cap=40)


def _fm_x():
    a = FM["x0"] + FM["cw"][0]
    b = a + FM["cw"][1]
    return FM["x0"], a, b, FM["x1"]


def form_base(st0):
    x0, a, b, x1 = _fm_x()
    g = [_tline(x0, FM["y0"], FORM["title"], 30, J.DOC, "start", 200),
         _tline((x0 + x1) / 2, FM["y0"] + 60, FORM["head"], 34, INK, "middle", x1 - x0 - 200),
         F.rect(x0, FM["hy"] - 50, x1 - x0, FM["ry1"] - FM["hy"] + 50, J.BG2, J.DOC, 4),
         F.line(x0, FM["ry0"] - 8, x1, FM["ry0"] - 8, J.DOC, 3)]
    for x in (a, b):
        g.append(F.line(x, FM["hy"] - 50, x, FM["ry1"], J.DOC, 3))
    for t, (l, r) in zip(FORM["cols"], ((x0, a), (a, b), (b, x1))):
        g.append(_tline((l + r) / 2, FM["hy"] - 12, t, 30, J.DOC, "middle", r - l - 20))
    for l, r in ((x0, a), (a, b)):              # 名前と職の欄は出さない（灰の帯）
        g.append(F.rect(l + 30, FM["ry0"] + 40, r - l - 60, 40, J.LINE_DIM, None))
    for i, t in enumerate(FORM["cell"]):
        g.append(F.txt(b + 30, _fm_line_y(i), t, FM["cap"], INK, "Noto", "start"))
    return g


def _fm_line_y(i):
    return FM["ry0"] + 70 + i * 74


def fm_phrase_box(t, i):
    """句 t（行 i の中）の箱（x0, y0, x1, y1）＝字幅は fontmetrics（本番の物差し）。"""
    _x0, _a, b, _x1 = _fm_x()
    line = FORM["cell"][i]
    if t not in line:                  # 句が行に無い＝印を置けない（門番 check_mech が「印の句が欄の行に無い」で止める）
        return None
    k = line.index(t)
    xa = b + 30 + fm.width(line[:k], FM["cap"])
    xb = xa + fm.width(t, FM["cap"])
    y = _fm_line_y(i)
    return xa - 6, y - FM["cap"] * 0.92, xb + 6, y + FM["cap"] * 0.22


def form_stage(prev, st):
    s = []
    for j, (t, i) in enumerate(FORM["hl"]):
        bx = fm_phrase_box(t, i)
        if _on(prev, st, f"h{j}") and bx:
            xa, ya, xb, yb = bx
            s.append(F.line(xa, yb + 6, xb, yb + 6, J.DOC, 7))      # 下線だけ（塗りの箱は字の上に重なる＝段の層は基図の字より上）
    return s


# ══════════════════════════════════════════════════════════
#  flow（c312・国会の報告の判断＝札と線）。🔴「大きな惨事」は次のカット（c313）の語り＝描かない
# ══════════════════════════════════════════════════════════
FLOW = dict(head=("国会の報告の判断", "state"),
            boxes=(("崩れるのを甘く見た", "company", (520.0, 470.0)), ("経営の事情も考えた", "company", (520.0, 670.0)),
                   ("営業のあとに直すだけと決めた", "company", (1330.0, 570.0))))
FW = dict(w=(460.0, 460.0, 600.0), h=110.0)


def _fw_box(i, lit):
    t, r, (cx, cy) = FLOW["boxes"][i]
    w, h = FW["w"][i], FW["h"]
    c = rc(r) if lit else J.LINE_DIM
    return F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, c, 5, rx=12) + _tline(cx, cy + 11, t, 32, rc(r) if lit else J.TICK, "middle", w - 40)


def flow_base(st0):
    t, r = FLOW["head"]
    return [_tline(L_X + 160, 330.0, t, 32, rc(r), "start", 600)]


def flow_stage(prev, st):
    s = []
    if _on(prev, st, "b1"):
        s += [_fw_box(0, True), _fw_box(1, True)]
    if _on(prev, st, "b2"):
        (_, _, (x3, y3)) = FLOW["boxes"][2]
        for i in (0, 1):
            _, _, (cx, cy) = FLOW["boxes"][i]
            s.append(_arrow(cx + FW["w"][i] / 2 + 10, cy, x3 - FW["w"][2] / 2 - 12, y3 + (cy - y3) * 0.25, J.COMPANY, 5, 20))
        s.append(_fw_box(2, True))
    return s


# ══════════════════════════════════════════════════════════
#  table（c315・区の安全点検＝札の表）。区の報告 p.45「1차(해빙기 안전대비) : 95.3.13.～3.30.」「2차(테러, 가스폭발 대비) : 95.6.12.～6.30.」
# ══════════════════════════════════════════════════════════
TB_ROWS = (("1回目", (3, 13), (3, 30), ""), ("2回目", (6, 12), (6, 30), "テロとガス爆発への備え"))
TB_DAY = (6, 29)                   # 事故の日
TB = dict(x=380.0, bar=(700.0, 1500.0), ys=(450.0, 610.0), h=56.0)


def tb_x(m, d, row):
    (_, (m0, d0), (m1, d1), _) = TB_ROWS[row]
    a, b = TB["bar"]
    n0, n1, n = m0 * 31 + d0, m1 * 31 + d1, m * 31 + d
    return a + (b - a) * (n - n0) / (n1 - n0)


def table_base(st0):
    return [_tline(L_X + 160, 330.0, "区の安全点検（2回）", 32, J.OK, "start", 600)]


def _tb_row(i):
    t, (m0, d0), (m1, d1), why = TB_ROWS[i]
    y = TB["ys"][i]
    a, b = TB["bar"]
    g = [_tline(TB["x"], y + 12, t, 34, J.OK, "start", 220),
         F.rect(a, y - TB["h"] / 2, b - a, TB["h"], J.BG2, J.OK, 4, rx=10),
         _tline(a + 20, y + 12, f"{m0}月{d0}日〜{d1}日", 30, J.AMBER, "start", b - a - 40)]
    return g


def table_stage(prev, st):
    s = []
    if _on(prev, st, "r2"):
        s += _tb_row(1)
        x = tb_x(*TB_DAY, 1)
        y = TB["ys"][1]
        s.append(F.line(x, y - TB["h"] / 2 - 10, x, y + TB["h"] / 2 + 10, J.ALERT, 6))
        s.append(_tline(x, y - TB["h"] / 2 - 20, "6月29日", 28, J.ALERT, "middle", 200))
    if _on(prev, st, "why"):
        y = TB["ys"][1] + 84
        s.append(_tline(TB["bar"][0], y, TB_ROWS[1][3], 32, INK, "start", 800))
        s.append(F.rect(TB["bar"][0] - 10, y + 34, 640, 64, J.BG, J.ALERT, 4, rx=8))
        s.append(_tline(TB["bar"][0] + 10, y + 78, "骨組みの強さの点検ではない", 32, J.ALERT, "start", 620))
    if _on(prev, st, "r1"):
        s += _tb_row(0)
    return s


# ══════════════════════════════════════════════════════════
#  clocks（c402・c418・記録ごとの時刻の時計）。針の角度は時刻から（門番が針の角度を照らす）
# ══════════════════════════════════════════════════════════
#   fall＝崩れはじめの時刻（国会の報告 p.30「17:52」・ソウル市 p.34／瑞草区 p.42「17:55경」・検察 p.45「17:57경」）
#   after＝崩れたあと（17:55ごろ・市の事故対策本部 18:00・市長が着く 18:50ごろ＝ソウル市 p.35）
CK_SET = dict(fall=(("17:52", "", "国会の報告", "state"), ("17:55", "ごろ", "市と区の報告", "city"), ("17:57", "ごろ", "検察の報告", "state")),
              after=(("17:55", "ごろ", "崩れはじめ", "ALERT"), ("18:00", "", "市の事故対策本部", "city"), ("18:50", "ごろ", "市長が着く", "city")))
CK = dict(xs=(520.0, 960.0, 1400.0), y=520.0, r=120.0, ty=720.0, sy=774.0)


def ck_angles(t):
    """時刻 → (短針の角度, 長針の角度)（度・12時から時計回り）。"""
    h, m = (int(x) for x in t.split(":"))
    return ((h % 12) * 30.0 + m * 0.5, m * 6.0)


def _hand(cx, cy, ang, L, w, col):
    a = math.radians(ang)
    return F.line(cx, cy, cx + L * math.sin(a), cy - L * math.cos(a), col, w)


def _clock(i, item, lit, dim=False):
    t, apx, who, r = item
    cx, cy, R = CK["xs"][i], CK["y"], CK["r"]
    c = rc(r) if not dim else J.LINE_DIM
    g = [F.circ(cx, cy, R, J.BG2, c, 7 if lit else 5)]
    for k in range(12):
        a = math.radians(k * 30)
        g.append(F.line(cx + R * 0.80 * math.sin(a), cy - R * 0.80 * math.cos(a), cx + R * 0.92 * math.sin(a), cy - R * 0.92 * math.cos(a),
                        J.TICK, 4 if k % 3 == 0 else 2))
    ha, ma = ck_angles(t)
    hc = INK if not dim else J.TICK
    g.append(_hand(cx, cy, ha, R * 0.52, 10, hc))
    g.append(_hand(cx, cy, ma, R * 0.80, 6, hc))
    g.append(F.circ(cx, cy, 9, hc, None))
    g.append(_tline(cx, CK["ty"], t + apx, 44, J.AMBER if not dim else J.TICK, "middle", 300, fam="Dela"))
    g.append(_tline(cx, CK["sy"], who, 28, rc(r) if not dim else J.TICK, "middle", 380))
    if lit:
        g.append(F.circ(cx, cy, R + 16, "none", c, 4))
    return "".join(g)


def clocks_base(st0):
    return []


def clocks_stage(prev, st):
    s = []
    items = CK_SET[st["set"]]
    for i in range(3):
        f_ = f"k{i}"
        if st[f_] != prev.get(f_):
            if st[f_] == "lit" and prev.get(f_) == "on":      # 明るくするのは輪だけ（字を重ね描きしない）
                _t, _a, _w, r = items[i]
                s.append(F.circ(CK["xs"][i], CK["y"], CK["r"] + 16, "none", rc(r), 6))
            elif st[f_] in ("on", "lit", "dim"):
                s.append(_clock(i, items[i], st[f_] == "lit", st[f_] == "dim"))
    if _on(prev, st, "br"):            # 17:55ごろ〜18:50ごろ の括弧（1時間たらず）
        a, b = CK["xs"][0], CK["xs"][2]
        y = CK["y"] - CK["r"] - 40
        s.append(F.poly([(a, y + 20), (a, y), (b, y), (b, y + 20)], "none", J.TICK, 4))
    return s


# ══════════════════════════════════════════════════════════
#  night（c420・夜の現場）＝灯り・車・クレーンの影（人は描かない）。A棟の跡に北と南の壁・B棟は残る
# ══════════════════════════════════════════════════════════
NT = dict(g=780.0, a=(330.0, 900.0), b=(1080.0, 1470.0), top=430.0)


def night_base(st0):
    g = []
    gy = NT["g"]
    a0, a1 = NT["a"]
    b0, b1 = NT["b"]
    g.append(F.line(140.0, gy, 1780.0, gy, J.LINE, 4))
    g.append(F.rect(b0, NT["top"], b1 - b0, gy - NT["top"], J.BG2, B_C, 4))
    for k in range(1, 5):
        g.append(F.line(b0, NT["top"] + (gy - NT["top"]) * k / 5, b1, NT["top"] + (gy - NT["top"]) * k / 5, J.LINE_DIM, 2))
    for x in (a0, a1 - 26):                      # 残った北と南の壁
        g.append(F.rect(x, NT["top"] + 10, 26, gy - NT["top"] - 10, A_C, None, op=0.85))
    mound = [(a0 + 26, gy), (a0 + 70, 700.0), (a0 + 160, 664.0), (a0 + 300, 684.0), (a0 + 420, 650.0), (a1 - 60, 690.0), (a1 - 26, gy)]
    g.append(F.poly(mound, J.BG2, J.LINE, 3, close=True))
    g.append(_hatch(a0 + 40, 668.0, a1 - 40, gy - 4, 20.0, J.LINE_DIM, 2, 0.7))
    # クレーンの影（2台）
    for (bx, tx, ty) in ((560.0, 700.0, 340.0), (1000.0, 900.0, 380.0)):     # 🔧 試し焼き（10-18）：2台の腕が交わって「A」の字に見えた
        g.append(F.line(bx, gy - 40, tx, ty, J.LINE, 8))
        g.append(F.line(tx, ty, tx + (40 if tx > bx else -40), ty + 120, J.LINE_DIM, 3))
        g.append(F.rect(bx - 50, gy - 46, 100, 46, J.LINE_DIM, None))
    # 投光器の灯り（3つ）
    for x in (250.0, 1010.0, 1620.0):
        g.append(F.line(x, gy, x, 520.0, J.LINE_DIM, 5))
        g.append(F.poly([(x - 14, 520.0), (x + 14, 520.0), (x + 150, gy), (x - 150, gy)], INK, None, op=0.10, close=True))
        g.append(F.circ(x, 516.0, 12, INK, None))
    # 車の影（2台）
    for x in (1530.0, 1690.0):
        g.append(F.rect(x - 60, gy - 58, 120, 42, J.LINE_DIM, None, rx=6))
        for wx in (x - 34, x + 34):
            g.append(F.circ(wx, gy - 14, 13, J.BG, J.LINE_DIM, 4))
    return g


def night_stage(prev, st):
    s = []
    if _on(prev, st, "q"):                 # ⚠️ geom_gap：瓦礫の真ん中だとクレーンの腕が「？」を貫いた
        s.append(_qmark(440.0, 600.0, 84, J.USCG))
    return s


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-18）：第4〜7章の見え方（c5〜c8）
# ══════════════════════════════════════════════════════════
import datetime as _dt  # noqa: E402

# ── road（c502・上から見た現場のまわりの道路と車）＝道と車の形と数は模式・人は描かない（国会の報告 p.32「교통통제와 … 출입통제가 신속히 이루어지지 아니하여
#    구조차량의 현장접근과 응급환자의 후송이 방해받는」）
RD = dict(site=(700.0, 300.0, 1120.0, 470.0), h=(520.0, 610.0), v=(1290.0, 1380.0), x0=110.0, vy1=860.0, amb=((210.0, 545.0, 0.0), (1335.0, 820.0, -90.0)))


def _car(x, y, w=56.0, h=28.0, deg=0.0, col=None, fill=None):
    c = col or J.LINE_DIM
    if deg:
        w, h = h, w
    return F.rect(x - w / 2, y - h / 2, w, h, fill or c, None, rx=5)


def _amb(x, y, deg, col=None):
    """救急車の上から見た形（白い箱と赤の十字）。deg＝0 右向き・−90 上向き。"""
    w, h = (92.0, 44.0) if deg == 0 else (44.0, 92.0)
    g = [F.rect(x - w / 2, y - h / 2, w, h, INK, J.BG, 3, rx=7)]
    g.append(F.rect(x - 6, y - 16, 12, 32, J.ALERT, None))
    g.append(F.rect(x - 16, y - 6, 32, 12, J.ALERT, None))
    return "".join(g)


def road_base(st0):
    g = []
    x0, y0, x1, y1 = RD["site"]
    h0, h1 = RD["h"]
    v0, v1 = RD["v"]
    g.append(F.rect(RD["x0"], h0, 1740.0 - RD["x0"], h1 - h0, J.BG2, J.LINE_DIM, 3))
    g.append(F.rect(v0, 300.0, v1 - v0, RD["vy1"] - 300.0, J.BG2, J.LINE_DIM, 3))
    g.append(F.line(RD["x0"], (h0 + h1) / 2, 1740.0, (h0 + h1) / 2, J.LINE_DIM, 2, dash="14 12"))
    g.append(F.line((v0 + v1) / 2, 300.0, (v0 + v1) / 2, RD["vy1"], J.LINE_DIM, 2, dash="14 12"))
    g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, A_C, 4))
    g.append(_hatch(x0 + 10, y0 + 10, x1 - 10, y1 - 10, 22.0, J.TICK, 2, 0.6))
    g.append(_tline((x0 + x1) / 2, y0 - 16, "崩れた百貨店", 30, A_C, "middle", 250))     # ⚠️ geom_gap：箱の中だと網の線が字を貫く（地の板を敷いても数える）＝箱の上
    return g


def _rd_cars():
    h0, h1 = RD["h"]
    v0, v1 = RD["v"]
    pts = []
    for lane, y in enumerate((h0 + 24, h1 - 24)):
        x = RD["x0"] + 70 + lane * 30
        while x < v0 - 40:
            pts.append((x, y, 0.0))
            x += 78
        x = v1 + 60
        while x < 1720:
            pts.append((x, y, 0.0))
            x += 78
    for lane, x in enumerate((v0 + 22, v1 - 22)):
        y = h1 + 60 + lane * 26
        while y < RD["vy1"] - 30:
            pts.append((x, y, 90.0))
            y += 74
    # 救急車の置き場は空ける
    return [(x, y, d) for x, y, d in pts if all(math.hypot(x - ax, y - ay) > 80 for ax, ay, _ in RD["amb"])]


RD_CARS = _rd_cars()


def road_stage(prev, st):
    s = []
    if _on(prev, st, "jam"):
        for x, y, d in RD_CARS:
            s.append(_car(x, y, deg=d))
    if _on(prev, st, "amb"):
        for x, y, d in RD["amb"]:
            s.append(_amb(x, y, d))
            if d == 0:
                s.append(_arrow(x + 60, y - 50, x + 300, y - 50, INK, 4, 16, dash="10 8"))
            else:
                s.append(_arrow(x + 50, y - 60, x + 50, y - 230, INK, 4, 16, dash="10 8"))
    if _on(prev, st, "amb", "blocked"):
        for x, y, d in RD["amb"]:
            s.append(_xmark(x + (190 if d == 0 else 50), y - (50 if d == 0 else 150), 22.0, J.ALERT, 8))
    return s


# ── wall（c504・横から見た北側の壁）＝ソウル市の報告 p.37「북측 잔여벽체 와이어로프 10개」「북측벽체 추가보강(H-BEAM 2개소 및 와이어로프 8개)」
#    ＝H形鋼は2か所（記録）・ワイヤーの本数と壁・瓦礫の形は模式。壁の左＝北（外）・右＝崩れた A棟の跡（瓦礫）
WL = dict(x=(900.0, 944.0), top=340.0, g=820.0, hb=((900.0, 600.0, 620.0), (900.0, 700.0, 760.0)), wires=6)   # ⚠️ geom_gap：札の場所を空けた（ワイヤーは高く・左へ）
WL_RUBBLE = (((960.0, 820.0), (1010.0, 700.0), (1100.0, 690.0), (1150.0, 820.0)), ((1120.0, 820.0), (1200.0, 650.0), (1320.0, 680.0), (1360.0, 820.0)),
             ((1330.0, 820.0), (1400.0, 720.0), (1500.0, 730.0), (1540.0, 820.0)), ((1010.0, 700.0), (1080.0, 620.0), (1180.0, 640.0), (1100.0, 690.0)),
             ((1210.0, 650.0), (1280.0, 590.0), (1360.0, 620.0), (1320.0, 680.0)), ((1500.0, 820.0), (1560.0, 760.0), (1640.0, 780.0), (1660.0, 820.0)))


def wall_base(st0):
    g = []
    x0, x1 = WL["x"]
    g.append(F.line(160.0, WL["g"], 1760.0, WL["g"], J.LINE, 4))
    g.append(F.rect(x0, WL["top"], x1 - x0, WL["g"] - WL["top"], A_C, None, op=0.85))
    for k in range(1, 5):                      # 階の跡（模式）
        y = WL["top"] + (WL["g"] - WL["top"]) * k / 5
        g.append(F.line(x1, y, x1 + 22, y, A_C, 3))
    for i in range(WL["wires"]):               # ワイヤー（本数は模式）
        y = WL["top"] + i * 22
        g.append(F.line(x0, y, 150.0 + i * 44, WL["g"], J.LINE, 2))
    for (x, y, gx) in WL["hb"]:                # H形鋼（2か所＝記録）
        g.append(F.line(x, y, gx, WL["g"], J.DOC, 14))
        for u in (0.3, 0.6, 0.9):
            px, py = x + (gx - x) * u, y + (WL["g"] - y) * u
            g.append(F.line(px - 10, py - 12, px + 10, py + 12, J.BG, 3))
    g.append(_tline((x0 + x1) / 2, WL["top"] - 18, "北側の壁（A棟）", 28, A_C, "middle", 300))
    g.append(_tline(300.0, 640.0, "ワイヤー", 28, J.LINE, "start", 200))
    g.append(_tline(470.0, 795.0, "H形鋼", 28, J.DOC, "start", 120))          # 「2か所」は下の注（ソウル市の報告）
    g.append(_tline(1260.0, 560.0, "瓦礫", 28, J.TICK, "middle", 120))
    return g


def wall_parts(st):
    a = 0.12 if st["rubble"] == "clear" else 1.0      # ⚠️ c504 は尺 2.6秒＝間隔 0.12秒（0.25 だと最後の瓦礫が 3.35秒まで動き、尺の外へ）
    return [_P(f"rb{i}", "poly", pts, fill=J.LINE_DIM, stroke=J.LINE, w=3, alpha=a, lag=0.12 * i) for i, pts in enumerate(WL_RUBBLE)]


def wall_stage(prev, st):
    return []


# ── cal（c513・c810 暦）＝日付は記録（曜日は暦＝datetime で計算・門番が実際の曜日と照らす）。原文の日付の写し＝「模式」を付けない
CAL_SET = dict(rescue=dict(first=(1995, 6, 25), last=(1995, 7, 15), fall=(1995, 6, 29), mark=(1995, 7, 9)),
               move89=dict(months=((1989, 7), (1989, 8), (1989, 9), (1989, 10), (1989, 11), (1989, 12)), band=((1989, 7), (1989, 12)),
                           open=(1989, 12, 1)))
CL = dict(x0=435.0, cw=150.0, y0=380.0, ch=112.0, mx0=300.0, mw=200.0, mg=16.0, my=(430.0, 610.0))
CAL_WD = ("日", "月", "火", "水", "木", "金", "土")


def cal_cells():
    """rescue の日の升目：[(日付, 列, 行)]（列＝曜日〈日曜 0〉・行＝週）。"""
    c = CAL_SET["rescue"]
    d = _dt.date(*c["first"])
    end = _dt.date(*c["last"])
    out = []
    row = 0
    while d <= end:
        col = (d.weekday() + 1) % 7
        out.append((d, col, row))
        if col == 6:
            row += 1
        d += _dt.timedelta(days=1)
    return out


def _cal_xy(col, row):
    return CL["x0"] + col * CL["cw"], CL["y0"] + row * CL["ch"]


def _cal_cell_of(ymd):
    for d, col, row in cal_cells():
        if (d.year, d.month, d.day) == tuple(ymd):
            return col, row
    return None


def _mo_x(i):
    return CL["mx0"] + i * (CL["mw"] + CL["mg"])


def cal_base(st0):
    g = []
    if st0["set"] == "rescue":
        g.append(_tline(CL["x0"] - 20, CL["y0"] - 54, "1995年", 28, J.TICK, "end", 200))
        for i, w in enumerate(CAL_WD):
            g.append(_tline(CL["x0"] + i * CL["cw"] + CL["cw"] / 2, CL["y0"] - 16, w, 26, J.TICK, "middle", 100))
        for d, col, row in cal_cells():
            x, y = _cal_xy(col, row)
            g.append(F.rect(x + 3, y + 3, CL["cw"] - 6, CL["ch"] - 6, J.BG2, J.LINE_DIM, 2, rx=6))
            lab = f"{d.month}月{d.day}日" if d.day == 1 or (row == 0 and col == 0) else f"{d.day}"
            g.append(_tline(x + 14, y + 38, lab, 26 if len(lab) > 2 else 30, J.TICK, "start", CL["cw"] - 20))
        return g
    g.append(_tline(CL["mx0"] - 20, CL["my"][0] + 40, "1989年", 28, J.TICK, "end", 200))
    for i, (y_, m_) in enumerate(CAL_SET["move89"]["months"]):
        x = _mo_x(i)
        g.append(F.rect(x, CL["my"][0], CL["mw"], CL["my"][1] - CL["my"][0], J.BG2, J.LINE_DIM, 3, rx=8))
        g.append(_tline(x + CL["mw"] / 2, CL["my"][0] + 50, f"{m_}月", 34, J.TICK, "middle", CL["mw"] - 20))
        for r in range(4):                         # 週の線（飾り）
            yy = CL["my"][0] + 80 + r * 26
            g.append(F.line(x + 20, yy, x + CL["mw"] - 20, yy, J.LINE_DIM, 2))
    return g


def cal_stage(prev, st):
    s = []
    if st["set"] == "rescue":
        c = CAL_SET["rescue"]
        if _on(prev, st, "d0"):
            col, row = _cal_cell_of(c["fall"])
            x, y = _cal_xy(col, row)
            s.append(F.rect(x + 6, y + 6, CL["cw"] - 12, CL["ch"] - 12, "none", J.ALERT, 6, rx=8))
            s.append(_tline(x + CL["cw"] / 2, y + CL["ch"] - 16, "崩れた日", 24, J.ALERT, "middle", CL["cw"] - 16))
        if _on(prev, st, "d1"):
            a = _cal_cell_of(c["fall"])
            b = _cal_cell_of(c["mark"])
            for d, col, row in cal_cells():
                k = (row, col)
                if (a[1], a[0]) < k < (b[1], b[0]):
                    x, y = _cal_xy(col, row)
                    s.append(F.rect(x + 6, y + 6, CL["cw"] - 12, CL["ch"] - 12, J.AMBER, None, op=0.14, rx=8))
            x, y = _cal_xy(*b)
            s.append(F.rect(x + 6, y + 6, CL["cw"] - 12, CL["ch"] - 12, "none", J.AMBER, 7, rx=8))
        return s
    c = CAL_SET["move89"]
    if _on(prev, st, "band"):
        (y0_, m0), (y1_, m1) = c["band"]
        ms = [m for _y, m in c["months"]]
        xa, xb = _mo_x(ms.index(m0)), _mo_x(ms.index(m1)) + CL["mw"]
        s.append(F.rect(xa, CL["my"][1] + 24, xb - xa, 40, J.COMPANY, None, op=0.75, rx=8))
    if _on(prev, st, "open"):
        y_, m_, d_ = c["open"]
        i = [m for _y, m in c["months"]].index(m_)
        x = _mo_x(i) + 6 + (CL["mw"] - 12) * (d_ - 1) / 31
        s.append(F.line(x, CL["my"][0] - 10, x, CL["my"][1] + 10, J.COMPANY, 6))     # 🔧 試し焼き（10-18）：赤（＝壊れる・欠陥）だった＝開店は会社の橙
        s.append(_tline(x, CL["my"][0] - 22, "開店（12月1日）", 28, J.COMPANY, "middle", 300))
    return s


# ── cards（c518 札）＝記録の数の板（ソウル市の報告 p.37・p.39＝7月19日の時点）。原文の数の写し＝「模式」を付けない
CARDS = dict(head=("7月19日の時点", "city"),
             rows=(("救助された人", "932人"), ("入院（76の病院）", "380人"), ("見つかった遺体", "459人")))
CD = dict(x0=380.0, x1=1540.0, ys=(470.0, 590.0, 710.0), h=96.0)


def _cset(set_):
    """札の組（🔧 ⑤b-6：rescue は毎回 CARDS を引く＝門番の陽性対照が CARDS を壊したとき絵に届くように。組の表に写すと届かない）"""
    return CARDS if set_ == "rescue" else CARD_SETS[set_]


def cards_base(st0):
    t, r = _cset(st0.get("set", "rescue"))["head"]
    return [_tline(CD["x0"], 380.0, t, 34, rc(r), "start", 800), F.line(CD["x0"], 400.0, CD["x1"], 400.0, rc(r), 3)]


def _cd_row(i, set_="rescue"):
    t, v = _cset(set_)["rows"][i]
    y = CD["ys"][i]
    wide = set_ != "rescue"             # 🆕 ⑤b-6：額の幅の札（cc12）・字の札（cd07）は値の字が長い＝値の幅を広げ、名の幅を狭める
    return (F.rect(CD["x0"], y - CD["h"] / 2, CD["x1"] - CD["x0"], CD["h"], J.BG2, J.LINE_DIM, 3, rx=10)
            + _tline(CD["x0"] + 30, y + 12, t, 36, INK, "start", 400 if wide else 640)
            + _tline(CD["x1"] - 30, y + 16, v, 46, J.AMBER, "end", 660 if wide else 400, fam="Dela"))


def cards_stage(prev, st):
    set_ = st.get("set", "rescue")
    n = len(_cset(set_)["rows"])
    return [_cd_row(i, set_) for i in range(n) if _on(prev, st, f"r{i}")]


# ── nums（c519 数の並び）＝場所の札と、数の箱と矢印（ソウル市の報告 p.39「사법연수원에 … 유실물관리센터」「1,087건을 접수하여 301건을 확인후 인계」）
NUMS = dict(place=("司法研修院", "state"), sub="持ち物を返すセンター", boxes=(("受け付け", "1,087件"), ("確かめて引き渡し", "301件")))
NB = dict(card=(960.0, 350.0, 520.0, 84.0), xs=(560.0, 1360.0), y=640.0, w=520.0, h=170.0)


def nums_base(st0):
    return []


def nums_stage(prev, st):
    s = []
    if _on(prev, st, "place"):
        cx, cy, w, h = NB["card"]
        t, r = NUMS["place"]
        s.append(F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, rc(r), 5, rx=12))
        s.append(_tline(cx, cy + 13, t, 38, rc(r), "middle", w - 40))
        s.append(_tline(cx, cy + h / 2 + 46, NUMS["sub"], 30, INK, "middle", 600))
    if _on(prev, st, "n"):
        for (t, v), x in zip(NUMS["boxes"], NB["xs"]):
            y = NB["y"]
            s.append(F.rect(x - NB["w"] / 2, y - NB["h"] / 2, NB["w"], NB["h"], J.BG2, J.LINE, 4, rx=12))
            s.append(_tline(x, y - 22, t, 32, INK, "middle", NB["w"] - 40))
            s.append(_tline(x, y + 50, v, 52, J.AMBER, "middle", NB["w"] - 40, fam="Dela"))
        s.append(_arrow(NB["xs"][0] + NB["w"] / 2 + 16, NB["y"], NB["xs"][1] - NB["w"] / 2 - 16, NB["y"], J.LINE, 6, 24))
    return s


# ── redo（c606 札と線）＝ショッピングセンター → 百貨店（c605 の語り）・計画と計算をまとめてやり直す（判決 大96 理由2.가）・怠った
RDO = dict(a=(530.0, 380.0, 440.0), b=(1390.0, 380.0, 440.0), h=96.0, docs=((730.0, 620.0), (1190.0, 620.0)), dw=340.0, dh=120.0)


def redo_base(st0):
    (ax, ay, aw), (bx, by, bw), h = RDO["a"], RDO["b"], RDO["h"]
    g = [F.rect(ax - aw / 2, ay - h / 2, aw, h, J.BG2, J.LINE_DIM, 4, rx=12), _tline(ax, ay + 11, "ショッピングセンター", 32, J.TICK, "middle", aw - 30),
         F.rect(bx - bw / 2, by - h / 2, bw, h, J.BG2, J.COMPANY, 5, rx=12), _tline(bx, by + 11, "百貨店", 36, J.COMPANY, "middle", bw - 30),
         _arrow(ax + aw / 2 + 14, ay, bx - bw / 2 - 14, by, J.COMPANY, 6, 24)]
    return g


def redo_stage(prev, st):
    s = []
    if _on(prev, st, "loop"):
        for (x, y), t in zip(RDO["docs"], ("建物の計画", "構造の計算")):
            s.append(F.rect(x - RDO["dw"] / 2, y - RDO["dh"] / 2, RDO["dw"], RDO["dh"], J.BG2, J.DOC, 4, rx=10))
            s.append(_tline(x, y + 11, t, 32, J.DOC, "middle", RDO["dw"] - 30))
        (x0, y0), (x1, _y1) = RDO["docs"]
        s.append(_loop((x0 + x1) / 2, y0, x1 - x0 + RDO["dw"] + 80, RDO["dh"] + 90, INK, 4))
        s.append(_tline((x0 + x1) / 2, y0 + RDO["dh"] / 2 + 100, "まとめてやり直す", 30, INK, "middle", 500))
    if _on(prev, st, "x"):
        (x0, y0), (x1, _y1) = RDO["docs"]
        s.append(_xmark((x0 + x1) / 2, y0, 46.0, J.ALERT, 11))
    return s


# ── sheets（c607 書類）＝構造の計算書に紙を20回あまり継ぎ足す（判決 大96 理由1「20여회에 걸쳐서 수시로 구조계산을 추가」）＝枚数は模式（20 より多く 30 より少ない）
SH = dict(x=380.0, y=380.0, w=300.0, h=380.0, n=22, dx=34.0, dy=6.0)


def sheets_base(st0):
    x, y, w, h = SH["x"], SH["y"], SH["w"], SH["h"]
    g = [F.rect(x, y, w, h, J.BG2, J.SHIP, 5, rx=6)]
    for k in range(7):
        yy = y + 60 + k * 44
        g.append(F.line(x + 30, yy, x + w - 30 - (k % 3) * 40, yy, J.TICK, 3))
    g.append(_tline(x + w / 2, y - 18, "構造の計算書", 30, J.SHIP, "middle", 400))
    return g


def sheets_parts(st):
    a = 1.0 if st["add"] == "on" else 0.0
    ps = []
    for i in range(SH["n"]):
        x = SH["x"] + SH["w"] * 0.6 + (i + 1) * SH["dx"]
        y = SH["y"] + 20 + (i % 2) * SH["dy"]
        ps.append(_P(f"sh{i}", "poly", [(x, y), (x + SH["w"] * 0.55, y), (x + SH["w"] * 0.55, y + SH["h"] - 40), (x, y + SH["h"] - 40)],
                     fill=J.BG2, stroke=J.SHIP, w=3, alpha=a, lag=0.04 * i))
    return ps


def sheets_stage(prev, st):
    return []


# ── rank（c618 店の大きさ）＝全国の百貨店の順位（白書 p.69＝新聞を引いた節「랭킹 7위」「2위」）。🔧 一覧の「店の形の大きさで」→ ほかの店の売り上げと広さは
#    記録に無い＝**同じ大きさの店の形を順位の数だけ並べ、三豊を灯す**（大きさに数の意味を持たせない）
RANK = dict(rows=(("売り上げ", 7), ("売り場の大きさ", 2)), ys=(500.0, 720.0), x0=600.0, dx=150.0)


def _shop(cx, by, col, lit):
    w, h = 96.0, 64.0
    g = [F.rect(cx - w / 2, by - h, w, h, J.BG2 if not lit else col, col, 4, op=None if not lit else 0.9)]
    g.append(F.poly([(cx - w / 2 - 10, by - h), (cx, by - h - 40), (cx + w / 2 + 10, by - h)], J.BG2 if not lit else col, col, 4, close=True))
    return "".join(g)


def rank_base(st0):
    return []


def rank_stage(prev, st):
    s = []
    for i, ((t, n), y) in enumerate(zip(RANK["rows"], RANK["ys"])):
        if _on(prev, st, f"r{i}"):
            s.append(_tline(RANK["x0"] - 70, y - 20, t, 32, INK, "end", 360))
            for k in range(n):
                cx = RANK["x0"] + k * RANK["dx"]
                lit = k == n - 1
                s.append(_shop(cx, y, J.COMPANY if lit else J.LINE_DIM, lit))
                s.append(_tline(cx, y + 44, f"{k + 1}位", 28 if not lit else 32, J.AMBER if lit else J.TICK, "middle", 120))
    return s


# ── beam（c701 斜めから見た柱と梁と床）＝梁のある作り（ふつう）／梁の無い作り（この建物＝柱の頭の厚い板・国会の報告 p.28・判決）。形は模式
BM = dict(x=(420.0, 1220.0), w=360.0, d=(120.0, -80.0), top=500.0, g=800.0, cw=36.0)


def _bm_beams_lit(x0):
    """梁だけを明るくする（⚠️ 枠を丸ごと描き直すと札の字が2回描かれ、門番 layout が「重なり」で鳴る）。"""
    w, (dx, dy), top = BM["w"], BM["d"], BM["top"]
    s = []
    for (xa, ya), (xb, yb) in (((x0 + dx, top + dy), (x0 + w + dx, top + dy)), ((x0, top), (x0 + dx, top + dy)), ((x0 + w, top), (x0 + w + dx, top + dy)),
                               ((x0, top), (x0 + w, top))):
        s.append(F.poly([(xa, ya), (xb, yb), (xb, yb + 30), (xa, ya + 30)], "none", J.AMBER, 6, close=True))
    return "".join(s)


def _bm_frame(x0, kind, lit=False, show=True):
    if not show:
        return ""
    w, (dx, dy), top, g_, cw = BM["w"], BM["d"], BM["top"], BM["g"], BM["cw"]
    cols_back = [(x0 + dx, top + dy), (x0 + w + dx, top + dy)]
    cols_front = [(x0, top), (x0 + w, top)]
    s = []
    for (x, y) in cols_back:
        s.append(F.rect(x - cw / 2, y, cw, g_ - top, J.BG2, J.LINE_DIM, 3))
    th = 18.0 if kind == "beam" else 34.0
    if kind == "beam":
        bc = J.AMBER if lit else J.LINE
        for (xa, ya), (xb, yb) in (((x0 + dx, top + dy), (x0 + w + dx, top + dy)), ((x0, top), (x0 + dx, top + dy)), ((x0 + w, top), (x0 + w + dx, top + dy))):
            s.append(F.poly([(xa, ya), (xb, yb), (xb, yb + 30), (xa, ya + 30)], J.BG2, bc, 4, close=True))
    else:
        for (x, y) in cols_back + cols_front:
            s.append(F.poly([(x - 46, y), (x + 46, y), (x + 46 + dx * 0.25, y + dy * 0.25), (x - 46 + dx * 0.25, y + dy * 0.25)], J.BG2, INK, 3, close=True))
            s.append(F.rect(x - 46, y, 92, 22, J.BG2, INK, 3))
    for (x, y) in cols_front:
        s.append(F.rect(x - cw / 2, y + (30 if kind == "beam" else 22), cw, g_ - top - (30 if kind == "beam" else 22), J.BG2, J.LINE, 4))
    if kind == "beam":
        bc = J.AMBER if lit else J.LINE
        s.append(F.poly([(x0, top), (x0 + w, top), (x0 + w, top + 30), (x0, top + 30)], J.BG2, bc, 4, close=True))
    sx0, sx1 = x0 - 70, x0 + w + 70
    slab = [(sx0, top - th), (sx1, top - th), (sx1 + dx, top - th + dy), (sx0 + dx, top - th + dy)]
    s.append(F.poly(slab, J.BG2, INK, 4, close=True))
    s.append(F.poly([(sx0, top - th), (sx1, top - th), (sx1, top), (sx0, top)], J.BG2, INK, 4, close=True))
    s.append(F.poly([(sx1, top - th), (sx1 + dx, top - th + dy), (sx1 + dx, top + dy), (sx1, top)], J.BG2, INK, 3, close=True))
    lab = "梁のある作り（ふつう）" if kind == "beam" else "梁の無い作り（この建物）"
    s.append(_tline(x0 + w / 2 + dx / 2, g_ + 46, lab, 30, INK if kind == "beam" else A_C, "middle", 520))
    return "".join(s)


def beam_base(st0):
    return [F.line(200.0, BM["g"], 1720.0, BM["g"], J.LINE, 4)]


def beam_stage(prev, st):
    s = []
    if _on(prev, st, "r"):
        s.append(_bm_frame(BM["x"][1], "flat"))
    if _on(prev, st, "l"):
        s.append(_bm_frame(BM["x"][0], "beam"))
    if _on(prev, st, "lit"):
        s.append(_bm_beams_lit(BM["x"][0]))
    if _on(prev, st, "q"):                      # ⚠️ geom_gap：右の枠の床の右の端（x 1770）に重ねない＝床の上
        s.append(_qmark(BM["x"][1] + BM["w"] / 2 + 60, 330.0, 84, J.AMBER))
    return s


# ── drop（c703 横から見た柱の頭の断面）＝ドロップパネル（柱の頭の厚い板＝床が柱のまわりから抜け落ちないよう下から支える＝国会の報告 p.29・判決）。厚さの比は模式
DP = dict(cx=960.0, cw=120.0, s0=400.0, s1=490.0, p1=540.0, pw=420.0, x0=260.0, x1=1660.0, g=848.0)   # ⚠️ geom_gap：柱の下 860 は下の注の行に 3.6px


def drop_base(st0):
    cx, cw = DP["cx"], DP["cw"]
    g = [F.rect(cx - cw / 2, DP["p1"], cw, DP["g"] - DP["p1"], J.BG2, J.LINE, 4),
         F.rect(cx - cw / 2, 300.0, cw, DP["s0"] - 300.0, J.BG2, J.LINE, 4),
         F.rect(DP["x0"], DP["s0"], DP["x1"] - DP["x0"], DP["s1"] - DP["s0"], J.BG2, J.LINE, 4),
         F.rect(cx - DP["pw"] / 2, DP["s1"], DP["pw"], DP["p1"] - DP["s1"], J.BG2, INK, 4)]
    g.append(_tline(DP["x0"] + 10, DP["s0"] - 18, "床", 28, INK, "start", 200))
    g.append(_tline(cx + cw / 2 + 20, 720.0, "柱", 28, INK, "start", 200))
    return g


def drop_stage(prev, st):
    s = []
    cx = DP["cx"]
    if _on(prev, st, "dp"):
        s.append(F.rect(cx - DP["pw"] / 2, DP["s1"], DP["pw"], DP["p1"] - DP["s1"], J.AMBER, J.AMBER, 4, op=0.45))
    if _on(prev, st, "up"):
        for x in (cx - 160, cx + 160):
            s.append(_arrow(x, DP["p1"] + 70, x, DP["s1"] + 8, INK, 6, 20))
    return s


# ── spans（c706 横から見た床と柱）＝柱のあいだが長いほど床は垂れやすく、つなぎ目に大きな力（一般の説明・10.8メートル＝判決）。たわみは誇張（模式）
SP2 = dict(short=(640.0, 1060.0, 400.0, 10.0), long=(360.0, 1560.0, 640.0, 46.0), th=30.0, cw=44.0, n=40)
SP_LONG_M = 10.8


def _sp_edge(c0, c1, y, sag, x0, x1):
    pts = []
    for i in range(SP2["n"] + 1):
        x = x0 + (x1 - x0) * i / SP2["n"]
        d = sag * math.sin(math.pi * (x - c0) / (c1 - c0)) if c0 < x < c1 else 0.0
        pts.append((x, y + d))
    return pts


def spans_parts(st):
    ps = []
    for k in ("short", "long"):
        c0, c1, y, sag = SP2[k]
        s_ = sag if st["sag"] == "on" else 0.0
        x0, x1 = c0 - 110, c1 + 110
        top = _sp_edge(c0, c1, y, s_, x0, x1)
        bot = _sp_edge(c0, c1, y + SP2["th"], s_, x0, x1)
        ps.append(_P(f"sl_{k}", "poly", top + list(reversed(bot)), fill=J.BG2, stroke=J.LINE, w=4))
    return ps


def spans_base(st0):
    g = []
    for k in ("short", "long"):
        c0, c1, y, _sag = SP2[k]
        for c in (c0, c1):
            low = 120.0 if k == "short" else 150.0      # ⚠️ geom_gap：短い段の柱の下が「10.8メートル」の札に触れた
            g.append(F.rect(c - SP2["cw"] / 2, y + SP2["th"], SP2["cw"], low, J.BG2, J.LINE, 4))
            g.append(F.rect(c - SP2["cw"] / 2, y - 110.0, SP2["cw"], 110.0, J.BG2, J.LINE, 4))
    c0, c1, y, _s = SP2["short"]
    g.append(_tline(c1 + 160, y + 24, "柱のあいだが短い", 28, J.TICK, "start", 400))
    c0, c1, y, _s = SP2["long"]
    yy = y - 28                                 # ⚠️ 床の下に置くと下の注の行に近い＝床の上（柱のあいだ）・札は線の上（線が字を貫かない）
    g.append(F.line(c0, yy, c1, yy, J.TICK, 3))
    for c in (c0, c1):
        g.append(F.line(c, yy - 14, c, yy + 14, J.TICK, 3))
    g.append(_tline((c0 + c1) / 2, yy - 16, f"{SP_LONG_M:g}メートル", 30, J.AMBER, "middle", 280))
    return g


def spans_stage(prev, st):
    s = []
    if _on(prev, st, "joint"):
        for k in ("long",):
            c0, c1, y, _s = SP2[k]
            for c in (c0, c1):
                s.append(F.circ(c, y + SP2["th"] / 2, 44, "none", J.ALERT, 6))
    return s


# ── colx（c708 柱の断面の比べ）＝国会の報告 p.29「구조계산서에는 800㎜에 16개로 되어있으나 설계도면상에는 600㎜에 8개」。同じ縮尺（1センチ＝4画素）・
#    鉄筋は表面から5センチの輪（p.29「주철근이 정상위치(표면에서 50㎜임)」）
CX_PX_CM = 4.0
CX_COLS = (("計算書", 80.0, 16, "engineer"), ("図面", 60.0, 8, "ALERT"))
CX = dict(xs=(620.0, 1300.0), y=600.0, cover_cm=5.0)


def colx_base(st0):
    return []


def colx_stage(prev, st):
    s = []
    if _on(prev, st, "both"):
        for (t, dcm, n, r), x in zip(CX_COLS, CX["xs"]):
            R = dcm / 2 * CX_PX_CM
            col = rc(r)
            s.append(F.circ(x, CX["y"], R, J.BG2, col, 6))
            rr = R - CX["cover_cm"] * CX_PX_CM
            for k in range(n):
                a = 2 * math.pi * k / n
                s.append(F.circ(x + rr * math.cos(a), CX["y"] + rr * math.sin(a), 9, INK, None))
            s.append(_tline(x, CX["y"] - R - 24, t, 34, col, "middle", 300))
            s.append(_tline(x, CX["y"] + 196, f"直径{dcm:g}センチ", 32, J.AMBER, "middle", 380))
            s.append(_tline(x, CX["y"] + 240, f"鉄筋{n}本", 32, J.AMBER, "middle", 380))
    return s


# ── load（c710 重さ・c818 重さの足し算）。col＝太い柱と細い柱（支えられる重さ＝矢印の長さは模式）／sum＝屋上の冷却塔と5階の「？」
LD = dict(cols=((620.0, 160.0, "太い柱"), (1300.0, 120.0, "細い柱")), top=520.0, g=840.0,
          roof=(430.0, 460.0), f5=(650.0, 680.0), x=(360.0, 1560.0), towers=(640.0, 960.0, 1280.0), tw=170.0, th=110.0)


def load_base(st0):
    g = []
    if st0["set"] == "use":            # 🆕 ⑤b-5（c902）
        return load_use_base(st0)
    if st0["set"] == "col":
        g.append(F.line(260.0, LD["g"], 1660.0, LD["g"], J.LINE, 4))
        for x, w, t in LD["cols"]:
            g.append(F.rect(x - w / 2, LD["top"], w, LD["g"] - LD["top"], J.BG2, J.LINE, 4))
            g.append(_tline(x + w / 2 + 24, 760.0, t, 30, INK, "start", 260))
        return g
    x0, x1 = LD["x"]
    for (a, b), t in ((LD["roof"], "屋上"), (LD["f5"], "5階の床")):
        g.append(F.rect(x0, a, x1 - x0, b - a, J.BG2, J.LINE, 4))
        g.append(_tline(x0 - 16, b, t, 28, J.TICK, "end", 200))
    for x in (x0 + 60, (x0 + x1) / 2, x1 - 60):
        g.append(F.rect(x - 22, LD["roof"][1], 44, LD["f5"][0] - LD["roof"][1], J.BG2, J.LINE, 3))
        g.append(F.rect(x - 22, LD["f5"][1], 44, 848.0 - LD["f5"][1], J.BG2, J.LINE, 3))     # ⚠️ geom_gap：860 は下の注の行に 3.6px
    for x in LD["towers"]:
        g.append(F.rect(x - LD["tw"] / 2, LD["roof"][0] - LD["th"], LD["tw"], LD["th"], J.BG2, J.LINE, 4, rx=6))
    return g


def load_parts(st):
    if st["set"] != "col":
        return []
    ps = []
    for i, (x, w, _t) in enumerate(LD["cols"]):
        L = 150.0 if (i == 0 or st["cap"] == "same") else 70.0
        y1 = LD["top"] - 12
        y0 = y1 - L
        hw, sw = 34.0, 16.0
        ps.append(_P(f"arw{i}", "poly", [(x - sw, y0), (x + sw, y0), (x + sw, y1 - 30), (x + hw, y1 - 30), (x, y1), (x - hw, y1 - 30), (x - sw, y1 - 30)],
                     fill=J.AMBER if i == 0 else J.ALERT, stroke=None))
    return ps


def load_stage(prev, st):
    s = []
    if st["set"] == "use":
        return load_use_stage(prev, st)
    if st["set"] == "col":
        if _on(prev, st, "brit"):
            x, w, _t = LD["cols"][1]
            s.append(_zig(x - w / 2 + 6, 600.0, x + w / 2 - 6, 650.0, 5, 8.0, J.ALERT, 5))
            s.append(_zig(x - w / 2 + 6, 700.0, x + w / 2 - 6, 740.0, 5, 8.0, J.ALERT, 5))
        return s
    if _on(prev, st, "roofw"):
        for x in LD["towers"]:
            s.append(F.rect(x - LD["tw"] / 2, LD["roof"][0] - LD["th"], LD["tw"], LD["th"], J.ALERT, J.ALERT, 4, rx=6, op=0.35))
            s.append(_arrow(x, LD["roof"][0] + 6, x, LD["roof"][1] + 70, J.ALERT, 7, 22))
    if _on(prev, st, "q5"):
        x = (LD["x"][0] + LD["x"][1]) / 2 + 300
        s.append(F.rect(x - 110, LD["f5"][0] - 120, 220, 120, "none", J.AMBER, 5, rx=8, dash="12 8"))
        s.append(_qmark(x, LD["f5"][0] - 60, 72, J.AMBER))
        s.append(_arrow(x, LD["f5"][1] + 6, x, LD["f5"][1] + 90, J.AMBER, 7, 22))
    return s


# ── hoop（c717 斜めから見た柱の中の鉄筋）＝帯筋は主な鉄筋の外から束ねる（正しい）／内側に入っていた（国会の報告 p.29「띠철근은 주철근의 안쪽」・白書 p.89）・
#    消防の設備のために柱を削り、円い帯筋を切った（p.29「소방시설 설치를 위하여 … 원형 띠철근을 절단」）。本数と形は模式
HP = dict(xs=(520.0, 1180.0), top=360.0, g=760.0, rx=120.0, ry=42.0, bar_r=92.0, n=8, hy=(430.0, 520.0, 610.0, 700.0), out_r=106.0, in_r=72.0)


def _ell(cx, cy, rx, ry, a0=0, a1=360, step=8):
    return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in range(a0, a1 + 1, step)]


def _hp_col(cx, inside, cut=False):
    s = []
    rx, ry, top, g_ = HP["rx"], HP["ry"], HP["top"], HP["g"]
    s.append(F.poly(_ell(cx, g_, rx, ry, 0, 180) + [(cx - rx, top), (cx + rx, top)][::-1], J.BG2, None, close=True))
    s.append(F.rect(cx - rx, top, 2 * rx, g_ - top, J.BG2, None))
    for k in range(HP["n"]):                    # 奥の鉄筋（薄く）
        a = 2 * math.pi * k / HP["n"]
        if math.sin(a) < 0:
            x = cx + HP["bar_r"] * math.cos(a)
            s.append(F.line(x, top + HP["ry"] * 0.8 * math.sin(a), x, g_ + HP["ry"] * 0.8 * math.sin(a), J.LINE_DIM, 5))
    hr = HP["in_r"] if inside else HP["out_r"]
    hc = J.ALERT if inside else J.AMBER
    for j, y in enumerate(HP["hy"]):
        if cut and j == 1:
            s.append(F.poly(_ell(cx, y, hr, hr * ry / rx, 200, 340), "none", hc, 5))
            s.append(F.poly(_ell(cx, y, hr, hr * ry / rx, 20, 160), "none", hc, 5))
        else:
            s.append(F.poly(_ell(cx, y, hr, hr * ry / rx), "none", hc, 5, close=True))
    for k in range(HP["n"]):                    # 手前の鉄筋
        a = 2 * math.pi * k / HP["n"]
        if math.sin(a) >= 0:
            x = cx + HP["bar_r"] * math.cos(a)
            s.append(F.line(x, top + HP["ry"] * 0.8 * math.sin(a), x, g_ + HP["ry"] * 0.8 * math.sin(a), INK, 5))
    s.append(F.poly(_ell(cx, top, rx, ry), "none", J.LINE, 4, close=True))
    s.append(F.line(cx - rx, top, cx - rx, g_, J.LINE, 4))
    s.append(F.line(cx + rx, top, cx + rx, g_, J.LINE, 4))
    s.append(F.poly(_ell(cx, g_, rx, ry, 0, 180), "none", J.LINE, 4))
    if cut:                                      # 削った所（破線の欠け）
        y = HP["hy"][1]
        s.append(F.poly([(cx + rx, y - 60), (cx + rx - 46, y - 20), (cx + rx - 46, y + 30), (cx + rx, y + 64)], J.BG, J.ALERT, 4, dash="8 6"))
    lab = "正しい：帯筋が外" if not inside else "実際：帯筋が内側"
    s.append(_tline(cx, g_ + 80, lab, 30, hc, "middle", 420))
    return "".join(s)


def hoop_base(st0):
    return []


def hoop_stage(prev, st):
    s = []
    if _on(prev, st, "l"):
        s.append(_hp_col(HP["xs"][0], False))
    if _on(prev, st, "r"):
        s.append(_hp_col(HP["xs"][1], True))
    if _on(prev, st, "cut"):                    # ⚠️ 柱を丸ごと描き直すと札の字が2回＝切れ目と削った所だけを重ねる
        cx, rx, y = HP["xs"][1], HP["rx"], HP["hy"][1]
        hr = HP["in_r"]
        s.append(F.rect(cx + hr - 3, y - 10, 10, 20, J.BG2, None))                    # 帯筋の切れ目（右の端・⚠️ 幅を広げると手前の鉄筋〈cx+65〉も切れて見える）
        s.append(_xmark(cx + hr + 2, y - 34, 10.0, J.ALERT, 5))
        s.append(F.poly([(cx + rx, y - 60), (cx + rx - 46, y - 20), (cx + rx - 46, y + 30), (cx + rx, y + 64)], J.BG, J.ALERT, 4, dash="8 6"))
    return s


# ── persq（c806 比べ）＝1平方メートルのます目に大人（1人65キロとして＝400キロ→およそ6人・240キロ→4人ほど＝計算・台本 §9）。人の形は重さの目安（顔は描かない）
PQ_KG = 65.0
PQ = dict(sq=((300.0, 790.0), (1060.0, 790.0)), w=480.0, d=(200.0, -130.0), n=(6, 4), kg=(400.0, 240.0))


def _person(cx, by, col):
    g = [F.circ(cx, by - 118, 17, col, None), F.rect(cx - 20, by - 96, 40, 66, col, None, rx=14), F.rect(cx - 16, by - 34, 13, 34, col, None, rx=5),
         F.rect(cx + 3, by - 34, 13, 34, col, None, rx=5)]
    return "".join(g)


def _pq_pos(i, n):
    """i 番目の人の、ます目の中の割合 (u 横, v 奥)。"""
    cols = 3 if n == 6 else 2
    r, c = divmod(i, cols)
    return (0.2 + 0.6 * c / (cols - 1), 0.72 - 0.5 * r)


def persq_base(st0):
    return []


def _pq_sq(k, col):
    (x0, y0), w, (dx, dy) = PQ["sq"][k], PQ["w"], PQ["d"]
    s = [F.poly([(x0, y0), (x0 + w, y0), (x0 + w + dx, y0 + dy), (x0 + dx, y0 + dy)], J.BG2, col, 4, close=True)]
    n = PQ["n"][k]
    order = sorted(range(n), key=lambda i: -_pq_pos(i, n)[1])
    for i in order:
        u, v = _pq_pos(i, n)
        s.append(_person(x0 + w * u + dx * (1 - v), y0 + dy * (1 - v) - 6, INK))
    lab = "1平方メートル（冷却塔の下の床）" if k == 0 else "1平方メートル（屋上の床の前提）"
    s.append(_tline(x0 + w / 2 + dx / 2, y0 + 50, lab, 28, col, "middle", w + 160))
    return "".join(s)


def persq_stage(prev, st):
    s = []
    if _on(prev, st, "l"):
        s.append(_pq_sq(0, J.ALERT))
    if _on(prev, st, "r"):
        s.append(_pq_sq(1, J.LINE))
    return s


# ── calc（c807 書類）＝構造の計算書に冷却塔3基の計算が無い（判決 大96 理由1「옥상에 설치하기로 예정된 냉각탑 3개에 대한 구조계산을 누락」）。中身は模式
CC = dict(x=380.0, y=330.0, w=560.0, h=500.0, rows=7, miss=3)


def calc_base(st0):
    x, y, w, h = CC["x"], CC["y"], CC["w"], CC["h"]
    g = [F.rect(x, y, w, h, J.BG2, J.SHIP, 5, rx=6), _tline(x + w / 2, y + 50, "構造の計算書", 32, J.SHIP, "middle", w - 40)]
    for k in range(CC["rows"]):
        yy = y + 110 + k * 52
        if k == CC["miss"]:
            continue
        g.append(F.rect(x + 40, yy - 14, w - 80 - (k % 3) * 60, 22, J.LINE_DIM, None, rx=4))
    return g


def calc_stage(prev, st):
    s = []
    x, y, w = CC["x"], CC["y"], CC["w"]
    if _on(prev, st, "miss"):
        yy = y + 110 + CC["miss"] * 52
        s.append(F.rect(x + 30, yy - 30, w - 60, 46, "none", J.ALERT, 4, rx=6, dash="10 8"))
        s.append(_tline(x + 50, yy + 4, "冷却塔3基", 28, J.ALERT, "start", 300))
        s.append(_xmark(x + w - 70, yy - 7, 18.0, J.ALERT, 7))
    if _on(prev, st, "plan"):                  # 基本計画の建物（屋上に3基の破線＝置く予定）＝札は段の tag で
        bx0, bx1, by0, by1 = 1160.0, 1620.0, 580.0, 820.0
        s.append(F.rect(bx0, by0, bx1 - bx0, by1 - by0, J.BG2, J.LINE, 4))
        for k in range(1, 5):
            s.append(F.line(bx0, by0 + (by1 - by0) * k / 5, bx1, by0 + (by1 - by0) * k / 5, J.LINE_DIM, 2))
        for i in range(3):
            tx = bx0 + 60 + i * 140
            s.append(F.rect(tx, by0 - 70, 100, 70, "none", J.COMPANY, 4, rx=6, dash="10 6"))
    return s


# ── vs（c809・c813 札の比べ）＝記録ごとの値の札（原文の数の写し＝「模式」を付けない）。rumor の左の札は見た目を分ける（破線・灰・かぎかっこ）
VS_SET = dict(count=((("判決", "3基", "state"),), (("白書", "4台", "city"),)),
              rumor=((("よく語られる話", "「1台12トン」", "TICK"), ("", "「1993年に騒音で移した」", "TICK")),
                     (("判決", "1基28.7トン", "state"), ("検察の記録", "移したのは1989年", "state"))))
VSB = dict(xs=(560.0, 1360.0), y=560.0, w=620.0)


def vs_base(st0):
    return []


def _vs_card(i, set_, lit=False):
    rows = VS_SET[set_][i]
    x, w = VSB["xs"][i], VSB["w"]
    rumor = set_ == "rumor" and i == 0
    n = len(rows)
    h = 150.0 * n + 40
    y0 = VSB["y"] - h / 2
    col = J.TICK if rumor else rc(rows[0][2])
    s = [F.rect(x - w / 2, y0, w, h, J.BG2, col, 7 if lit else 4, rx=14, dash="14 10" if rumor else None)]
    for k, (head, val, r) in enumerate(rows):
        yy = y0 + 40 + 150 * k
        if head:
            s.append(_tline(x, yy + 30, head, 32, rc(r), "middle", w - 40))
        s.append(_tline(x, yy + 100, val, 44 if not rumor else 38, J.AMBER if not rumor else J.TICK, "middle", w - 40, fam="Noto"))
    return "".join(s)


def vs_stage(prev, st):
    s = []
    for i in range(2):
        if _on(prev, st, f"c{i}"):
            s.append(_vs_card(i, st["set"]))
    if _on(prev, st, "lit"):
        x, w = VSB["xs"][0], VSB["w"]
        n = len(VS_SET[st["set"]][0])
        h = 150.0 * n + 40
        s.append(F.rect(x - w / 2 - 12, VSB["y"] - h / 2 - 12, w + 24, h + 24, "none", rc(VS_SET[st["set"]][0][0][2]), 5, rx=18))
    return s


# ── drag（c812 横から見た屋上の床と重い箱）＝引きずると重さは床の狭い所に集まったまま動く（重い箱の下だけたわむ・誇張＝模式）／小分けにして移すべきだった（判決 大96 理由2.가）
DG = dict(x0=200.0, x1=1720.0, top=600.0, th=40.0, cols=(330.0, 960.0, 1590.0), cw=44.0, box=(170.0, 120.0), xs=(560.0, 1260.0), sag=30.0, n=60)


def _dg_edge(y, bx):
    pts = []
    for i in range(DG["n"] + 1):
        x = DG["x0"] + (DG["x1"] - DG["x0"]) * i / DG["n"]
        d = DG["sag"] * math.exp(-((x - bx) / 150.0) ** 2)
        pts.append((x, y + d))
    return pts


def drag_parts(st):
    bx = DG["xs"][1] if st["pos"] == "moved" else DG["xs"][0]
    w, h = DG["box"]
    top = _dg_edge(DG["top"], bx)
    bot = _dg_edge(DG["top"] + DG["th"], bx)
    by = DG["top"] + DG["sag"] - 4
    return [_P("slab", "poly", top + list(reversed(bot)), fill=J.BG2, stroke=J.LINE, w=4),
            _P("box", "poly", [(bx - w / 2, by - h), (bx + w / 2, by - h), (bx + w / 2, by), (bx - w / 2, by)], fill=J.BG2, stroke=J.COMPANY, w=5),
            _P("aw", "poly", [(bx - 12, by + 54), (bx + 12, by + 54), (bx + 12, by + 96), (bx + 28, by + 96), (bx, by + 128), (bx - 28, by + 96), (bx - 12, by + 96)],
               fill=J.ALERT, stroke=None)]


def drag_base(st0):
    g = []
    for c in DG["cols"]:
        g.append(F.rect(c - DG["cw"] / 2, DG["top"] + DG["th"] + 20, DG["cw"], 848.0 - DG["top"] - DG["th"] - 20, J.BG2, J.LINE, 3))   # ⚠️ 860 は注に 3.6px
    g.append(_tline(DG["x0"] + 10, DG["top"] - 160, "屋上の床", 28, INK, "start", 300))
    return g


def drag_stage(prev, st):
    s = []
    if _on(prev, st, "split"):
        for i in range(4):
            x = 1260.0 + i * 120
            s.append(F.rect(x, 360.0, 80, 56, "none", J.USCG, 4, rx=6, dash="8 6"))
        s.append(_tline(1260.0, 344.0, "小分けにして移す", 28, J.USCG, "start", 460))
    if _on(prev, st, "pos", "moved"):
        a, b = DG["xs"]
        y = DG["top"] - DG["box"][1] - 40
        s.append(_arrow(a, y, b - 40, y, J.COMPANY, 5, 20, dash="12 8"))
    return s


# ── 既存の見え方に足す欄（⑤b-4）：bldg の5階の使い道（許可＝運動の施設／実際＝食堂街・判決 大96 理由2.가・国会の報告 p.29）・地下1階の帯と仮の使用
#    （区の報告 p.43「73,205㎡중 55,257㎡(지하1～지상3층)」）・弱い柱の印・屋上の「？」
USE5 = dict(permit="運動の施設", actual="食堂街")
TEMP_FLOORS = (("a", 1), ("a", 2), ("a", 3), ("b", 1), ("b", 2), ("b", 3), ("u", -1))
HI["temp"] = TEMP_FLOORS
BL_U = dict(y=(812.0, 856.0))


def _bl_use5_xy():
    a0, a1 = bl_x("a")
    y = bl_y(5) + BL["fh"] / 2 + 10
    return a0 + 18, (a0 + a1) / 2 + 48, y


def bldg_extra_base(st0):
    g = []
    if st0.get("under") == "on":
        x0, x1 = BL["xa"][0], BL["xb"][1]
        y0, y1 = BL_U["y"]
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE_DIM, 3, dash="10 8"))
        g.append(_tline(x0 - 16, y1 - 8, "地下1階", 24, J.TICK, "end", 140))
    return g


def bldg_extra_stage(prev, st):
    s = []
    xl, xr, y = _bl_use5_xy()
    if _on(prev, st, "use5", "permit"):
        s.append(_tline(xl, y, "許可：" + USE5["permit"], 26, INK, "start", 200))
    if _on(prev, st, "use5", "both"):
        if prev.get("use5") != "permit":
            s.append(_tline(xl, y, "許可：" + USE5["permit"], 26, INK, "start", 200))
        s.append(_tline(xr, y, "実際：" + USE5["actual"], 26, A_C, "start", 170))
        s.append(_arrow(xr - 40, y - 9, xr - 8, y - 9, A_C, 4, 12))
    if _on(prev, st, "q5"):                 # ⚠️ 帯の中・右は実際の札の場所／右の外は B棟の前の面＝A棟の屋上の面の上
        s.append(_qmark(640.0, 385.0, 60, J.AMBER))
    if _on(prev, st, "chk"):
        s.append(_xmark(1420.0, 550.0, 28.0, J.ALERT, 9))
    if _on(prev, st, "weak"):               # 細い柱（A棟の前の面に赤の破線＝場所と本数は模式）
        x0, x1 = bl_x("a")
        for k in range(1, 5):
            x = x0 + (x1 - x0) * k / 5
            s.append(F.line(x, bl_y(5), x, BL["g"], J.ALERT, 3, dash="8 6"))
    if _on(prev, st, "qroof"):              # 屋上の「？」の箱（⚠️「A棟（北）」の札〈x 560〜710〉の右）
        cx, cy = 820.0, 318.0                   # ⚠️ geom_gap：屋上の面（y 324〜420）に重ねると面の縁が「？」を貫く＝面の上
        s.append(F.rect(cx - 70, cy - 96, 140, 96, "none", J.AMBER, 5, rx=8, dash="12 8"))
        s.append(_qmark(cx, cy - 48, 60, J.AMBER))
    return s


def bldg_extra_parts(st):
    if st.get("under") != "on":
        return []
    on = ("u", -1) in set(HI[st["hi"]])
    x0, x1 = BL["xa"][0], BL["xb"][1]
    y0, y1 = BL_U["y"]
    return [_P("hi_u1", "poly", [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill=INK, stroke=None, alpha=0.30 if on else 0.0)]


# ── plan に足す床（⑤b-4）：area＝全部の階を足した広さ（許可 7万1,136・工事の図面 7万3,205＝増えた 2,069 の割合だけ＝国会の報告 p.29・区の報告 p.43）／
#    grid のドロップパネル（薄い所＝多く・判決／無い所＝5階 4列E行の柱の上＝判決 大96 理由1「5층 4열E행 부위에 해당하는 기둥상부에 … 15㎝ 두께의 지판시공이 누락」）／
#    ct＝屋上の冷却塔の置き場と引きずった道すじ（後ろの側 → 前の側＝白書 p.90 の図の言い方・場所と向きは模式）
AREA = dict(permit=71136, plan=73205, add=2069, x=(380.0, 1280.0), y=(420.0, 760.0))
DP_MISS = (("4", "E"),)
CT = dict(x=(380.0, 1360.0), y=(400.0, 780.0), back=((520.0, 470.0), (770.0, 470.0), (1020.0, 470.0)), front=((620.0, 690.0), (870.0, 690.0), (1120.0, 690.0)), s=110.0)


def _area_split():
    x0, x1 = AREA["x"]
    return x0 + (x1 - x0) * AREA["permit"] / AREA["plan"]


def plan_extra_base(st0):
    fl = st0["floor"]
    g = []
    if fl == "area":
        x0, x1 = AREA["x"]
        y0, y1 = AREA["y"]
        xs = _area_split()
        g.append(F.rect(x0, y0, xs - x0, y1 - y0, J.BG2, J.LINE, 4))
        g.append(_tline(x0 + 30, y0 + 60, "許可の床", 32, INK, "start", 500))     # ⚠️ 数の札は字幕の写し（門番 echo）＝数は語りに任せる
    if fl == "ct":
        x0, x1 = CT["x"]
        y0, y1 = CT["y"]
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 4))
        g.append(_tline(x0 + 20, y0 - 16, "後ろの側", 26, J.TICK, "start", 300))
        g.append(_tline(x0 + 20, y1 + 40, "前の側", 26, J.TICK, "start", 300))
    return g


def plan_extra_stage(prev, st):
    s = []
    fl = st["floor"]
    if fl == "area":
        x0, x1 = AREA["x"]
        y0, y1 = AREA["y"]
        xs = _area_split()
        if _on(prev, st, "aplan"):
            s.append(F.rect(x0 - 10, y0 - 10, x1 - x0 + 20, y1 - y0 + 20, "none", J.COMPANY, 5, dash="14 8"))
        if _on(prev, st, "add"):
            s.append(F.rect(xs, y0, x1 - xs, y1 - y0, J.ALERT, J.ALERT, 3, op=0.85))
            s.append(_arrow(x1 + 120, (y0 + y1) / 2, x1 + 14, (y0 + y1) / 2, J.ALERT, 5, 18))
    if fl == "grid":
        if _on(prev, st, "dp", "thin"):
            for c in GRID["cols"]:
                for r_ in GRID["rows"]:
                    x, y = grid_xy(c, r_)
                    s.append(F.rect(x - 40, y - 40, 80, 80, "none", J.LINE, 3, dash="6 5"))
        if _on(prev, st, "dp", "miss"):
            for c, r_ in DP_MISS:
                x, y = grid_xy(c, r_)
                s.append(F.rect(x - 44, y - 44, 88, 88, J.BG, J.ALERT, 5, dash="8 6"))
                s.append(F.rect(x - 14, y - 14, 28, 28, INK, None))
                s.append(_xmark(x + 44, y - 44, 16.0, J.ALERT, 6))
        if _on(prev, st, "miss_lit"):
            for c, r_ in DP_MISS:
                x, y = grid_xy(c, r_)
                s.append(F.circ(x, y, 74, "none", J.ALERT, 6))
    if fl == "ct" and _on(prev, st, "ct", "moved"):
        for (ax, ay), (bx, by) in zip(CT["back"], CT["front"]):
            s.append(_arrow(ax, ay + CT["s"] / 2 + 6, bx, by - CT["s"] / 2 - 6, J.ALERT, 5, 18, dash="12 8"))
    return s


def plan_extra_parts(st):
    if st["floor"] != "ct":
        return []
    ps = []
    for i, ((ax, ay), (bx, by)) in enumerate(zip(CT["back"], CT["front"])):
        x, y = (bx, by) if st["ct"] == "moved" else (ax, ay)
        h = CT["s"] / 2
        ps.append(_P(f"ct{i}", "poly", [(x - h, y - h), (x + h, y - h), (x + h, y + h), (x - h, y + h)], fill=J.BG2, stroke=J.COMPANY, w=5,
                     alpha=0.0 if st["ct"] == "off" else 1.0, lag=0.15 * i))
    return ps


# ── slab に足す欄（⑤b-4）：上の鉄筋（正しい位置＝表面から近い・沈んだ位置＝判決 4〜6センチ・国会 6〜8センチ・白書 5〜7センチ＝深さは誇張）・屋上の床・重い箱
SLB = dict(ok=10.0, sunk=28.0, bw=5.0)


def slab_extra_parts(st):
    """上の鉄筋（span だけ・off のときは透明＝段で部品の数を変えない）。"""
    if st["z"] != "span":
        return []
    sag = SLS["sag"] if st["sag"] == "on" else 0.0
    off = SLB["sunk"] if st["bar"] == "sunk" else SLB["ok"]
    a = _sls_edge(SLS["top"] + off, sag)
    b = _sls_edge(SLS["top"] + off + SLB["bw"], sag)
    # 🔧 試し焼き（10-18）：正しい位置を破線（段の層＝動かない）で描くと、床が垂れたときに破線だけまっすぐ残り、垂れた床の上へはみ出した
    #    ＝正しい位置の細い線も部品にして床と一緒に垂らす（沈んだときだけ見せる）
    ka = _sls_edge(SLS["top"] + SLB["ok"] + SLB["bw"] / 2 - 1.5, sag)
    kb = _sls_edge(SLS["top"] + SLB["ok"] + SLB["bw"] / 2 + 1.5, sag)
    return [_P("bar", "poly", a + list(reversed(b)), fill=J.ALERT if st["bar"] == "sunk" else INK, stroke=None,
               alpha=0.0 if st["bar"] == "off" else 1.0),
            _P("barok", "poly", ka + list(reversed(kb)), fill=INK, stroke=None, alpha=0.75 if st["bar"] == "sunk" else 0.0)]


def slab_extra_stage(prev, st):
    s = []
    if st["z"] == "span":
        if _on(prev, st, "box"):                    # 🔧 試し焼き（10-18）：箱の底を垂れる前の高さにすると、垂れた床から浮いて見えた＝垂れた床の上に置く
            c0, c1 = SLS["cols"]
            mx = (c0 + c1) / 2
            yb = SLS["top"] + (SLS["sag"] if st["sag"] == "on" else 0.0) - 2
            s.append(F.rect(mx - 100, yb - 120, 200, 120, J.BG2, J.COMPANY, 5, rx=6))
            s.append(_arrow(mx - 420, yb - 60, mx - 120, yb - 60, J.COMPANY, 5, 20, dash="12 8"))
    return s


# ── tower に足す欄（⑤b-4）：屋上の3基（判決 大96 理由1「자체하중이 각 28.7t(물의 하중까지 포함하면 45.5t)인 냉각탑 3개」）・重さの矢印・屋上の床を明るく
TW3 = dict(n=3, xs=(560.0, 900.0, 1240.0), w=230.0, h=190.0, d=(80.0, -50.0), roof=700.0, slab=(700.0, 740.0), x=(330.0, 1640.0))


def tower3_base(st0):
    g = []
    x0, x1 = TW3["x"]
    a, b = TW3["slab"]
    g.append(F.rect(x0, a, x1 - x0, b - a, J.BG2, J.LINE, 4))
    g.append(_tline(x0 - 16, b - 8, "屋上の床", 24, J.TICK, "end", 200))
    dx, dy = TW3["d"]
    for x in TW3["xs"]:
        y1 = TW3["roof"]
        y0 = y1 - TW3["h"]
        w = TW3["w"]
        g.append(F.poly([(x + w, y0), (x + w + dx, y0 + dy), (x + w + dx, y1 + dy), (x + w, y1)], J.BG2, J.LINE, 3, close=True))
        g.append(F.poly([(x, y0), (x + w, y0), (x + w + dx, y0 + dy), (x + dx, y0 + dy)], J.BG2, J.LINE, 3, close=True))
        g.append(F.rect(x, y0, w, y1 - y0, J.BG2, J.LINE, 4))
        for k in range(1, 4):
            g.append(F.line(x + 20, y0 + 40 + k * 34, x + w - 20, y0 + 40 + k * 34, J.LINE_DIM, 3))
        cx, cy = x + w / 2 + dx / 2, y0 + dy / 2
        g.append(F.poly([(cx + 70 * math.cos(math.radians(t)), cy + 18 * math.sin(math.radians(t))) for t in range(0, 361, 15)], J.BG2, J.LINE, 3))
    return g


def tower3_stage(prev, st):
    s = []
    if _on(prev, st, "load"):                  # 床の下へ重さの矢印（⚠️ 塔の前の面の上に引くと、すき間の線と重なる）
        for x in TW3["xs"]:
            cx = x + TW3["w"] / 2
            s.append(_arrow(cx, TW3["slab"][1] + 8, cx, TW3["slab"][1] + 100, J.ALERT, 8, 24))
    if _on(prev, st, "roof"):                  # ⚠️ どの棟の屋上かは描かない＝白で明るく（A棟のピンクにしない）
        x0, x1 = TW3["x"]
        a, b = TW3["slab"]
        s.append(F.rect(x0, a, x1 - x0, b - a, INK, INK, 4, op=0.40))
    return s


# ── crack に足す欄（⑤b-4）：屋上の床（c816）・ひびが育つ（判決 大96 理由1「휨변형에 의한 균열이 장기간 지속적으로 성장」）・長くかかる重さ
CR_BRANCH = (((954.0, 596.0), (900.0, 640.0), (860.0, 690.0)), ((980.0, 636.0), (1040.0, 668.0), (1100.0, 696.0)), ((948.0, 520.0), (890.0, 548.0)))


def crack_extra_parts(st):
    a = 1.0 if st.get("crack") == "long" else 0.0
    ps = []
    for i, path in enumerate(CR_BRANCH):
        left = [(x - 3, y) for x, y in path]
        right = [(x + 3, y) for x, y in reversed(path)]
        ps.append(_P(f"br{i}", "poly", left + right, fill=J.ALERT, stroke=None, alpha=a, lag=0.2 * i))
    return ps


def crack_extra_stage(prev, st):
    s = []
    if _on(prev, st, "load"):                  # ⚠️ 左の床の名の札（x 310〜620）の上を避ける
        for x in (720.0, 960.0, 1200.0, 1440.0):
            s.append(_arrow(x, CR["top"] - 110, x, CR["top"] - 12, J.AMBER, 6, 18))
    return s


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（第8〜9章・2026-10-19）：新しい見え方11（lists・over・cover・duct・opening・joint・hook・stack・insp・rule・items）と、
#     既存の見え方に足す欄（load の use・section の walls／joints・bldg の4階・plan の two／three・slab の屋上の柱のまわり・tower の水位）
# ══════════════════════════════════════════════════════════
def _drop(cx, cy, r=9.0, col=None):
    """水のしずく（模式）。"""
    return F.poly([(cx, cy - r * 2.2)] + [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(-30, 211, 20)],
                  col or J.USCG, None, close=True)


def _lamp(cx, cy, col=None):
    """吊り下げの照明（模式）。"""
    c = col or INK
    return (F.line(cx, cy - 44, cx, cy - 16, c, 3)
            + F.poly([(cx - 20, cy - 16), (cx + 20, cy - 16), (cx + 30, cy + 8), (cx - 30, cy + 8)], J.BG2, c, 4, close=True)
            + F.circ(cx, cy + 16, 7, J.AMBER, None))


def _eye(cx, cy, col=None):
    c = col or INK
    top = [(cx + 46 * math.cos(math.radians(a)), cy - 26 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    bot = [(cx - 46 * math.cos(math.radians(a)), cy + 26 * math.sin(math.radians(a))) for a in range(0, 181, 15)]
    return F.poly(top + bot, "none", c, 4, close=True) + F.circ(cx, cy, 11, c, None)


# ── load に足す組 use（c902 重さ）＝スケート場の床と食堂街の床（判決 大96 理由2.가「고정하중(Dead Load) 및 적재하중(Live Load)의 차이가 크므로」）。
#    物の名は語り・形と置き場と矢印の長さは模式
LU = dict(l=(240.0, 860.0), r=(1060.0, 1680.0), top=600.0, th=40.0, g=848.0, ly=790.0)
LU_ITEMS = (("厨房", 1090.0, 160.0, 90.0), ("冷蔵庫", 1280.0, 100.0, 150.0), ("間仕切り", 1440.0, 26.0, 140.0), ("客席", 1510.0, 160.0, 60.0))
LU_AW = (1200.0, 1330.0, 1453.0, 1560.0)


def _lu_slab(x0, x1):
    g = [F.rect(x0, LU["top"], x1 - x0, LU["th"], J.BG2, J.LINE, 4)]
    for x in (x0 + 60, x1 - 60):
        g.append(F.rect(x - 20, LU["top"] + LU["th"], 40, LU["g"] - LU["top"] - LU["th"], J.BG2, J.LINE, 3))
    return g


def load_use_base(st0):
    g = _lu_slab(*LU["l"]) + _lu_slab(*LU["r"])
    g.append(_tline(sum(LU["l"]) / 2, LU["ly"], "スケート場の床", 28, INK, "middle", 400))
    g.append(_tline(sum(LU["r"]) / 2, LU["ly"], "食堂街の床", 28, INK, "middle", 400))
    return g


def load_use_stage(prev, st):
    s = []
    if _on(prev, st, "sk"):
        x0, x1 = LU["l"]
        s.append(F.rect(x0, LU["top"], x1 - x0, LU["th"], INK, None, op=0.16))
        for x in (440.0, 660.0):                   # 軽い物の小さな矢印（模式）
            s.append(_arrow(x, LU["top"] - 34, x, LU["top"] - 6, J.LINE_DIM, 4, 12))
    if _on(prev, st, "food"):
        y = LU["top"]
        for t, x, w, h in LU_ITEMS:
            if t == "客席":                          # 机と椅子2つ
                s.append(F.rect(x + 40, y - h, 80, 14, J.BG2, INK, 3))
                s.append(F.line(x + 80, y - h + 14, x + 80, y, INK, 3))
                for cx in (x + 14, x + w - 14):
                    s.append(F.rect(cx - 14, y - 34, 28, 34, J.BG2, INK, 3))
            else:
                s.append(F.rect(x, y - h, w, h, J.BG2, INK, 3, rx=4))
            s.append(_tline(x + w / 2, y - h - 14, t, 24, INK, "middle", 160))
        x0, x1 = LU["r"]
        s.append(F.rect(x0, LU["top"], x1 - x0, LU["th"], J.ALERT, None, op=0.22))
        for x in LU_AW:
            s.append(_arrow(x, LU["top"] + LU["th"] + 4, x, LU["top"] + LU["th"] + 80, J.ALERT, 6, 18))
    return s


# ── lists（c904 箱）＝記録が挙げる5階の物を、記録ごとの箱に（国会の報告 p.29「칸막이 및 대형냉장고·주방기기와 공용부분에 화단 및 분수대 등」・
#    白書 p.89「대형냉장고・조적벽・돌정원」＝検察の資料と新聞を引いた節・頁の画像）。🔧 一覧の「国会・白書・判決の3つの箱」→ **2つの箱**
#    （判決の挙げる物は次の c905 の語り＝描かない）。原文の写し＝「模式」を付けない
LISTS = (("国会の報告", "state", ("間仕切り", "大きな冷蔵庫", "厨房の機器", "花壇と噴水")),
         ("白書", "city", ("大きな冷蔵庫", "れんがの壁", "石の庭")))
LSB = dict(xs=(560.0, 1360.0), w=620.0, top=340.0, head=64.0, row=78.0, n=4)


def _ls_y(j):
    return LSB["top"] + LSB["head"] + 56 + j * LSB["row"]


def _ls_box(i):
    h_, r_, items = LISTS[i]
    x, w = LSB["xs"][i], LSB["w"]
    hh = LSB["head"] + 40 + LSB["n"] * LSB["row"]
    g = [F.rect(x - w / 2, LSB["top"], w, hh, J.BG2, rc(r_), 4, rx=12),
         F.line(x - w / 2, LSB["top"] + LSB["head"], x + w / 2, LSB["top"] + LSB["head"], rc(r_), 3),
         _tline(x, LSB["top"] + 46, h_, 34, rc(r_), "middle", w - 40)]
    for j, t in enumerate(items):
        g.append(_tline(x - w / 2 + 64, _ls_y(j) + 12, t, 32, INK, "start", w - 100))
    return "".join(g)


def lists_base(st0):
    return []


def lists_stage(prev, st):
    s = []
    for i, f_ in enumerate(("k", "w")):
        if _on(prev, st, f_):
            s.append(_ls_box(i))
    if _on(prev, st, "diff"):                       # 片方だけの物＝黄の点・両方にある物＝破線でつなぐ
        a, b = LISTS[0][2], LISTS[1][2]
        for i, (own, other) in enumerate(((a, b), (b, a))):
            x = LSB["xs"][i] - LSB["w"] / 2 + 34
            for j, t in enumerate(own):
                if t not in other:
                    s.append(F.circ(x, _ls_y(j), 9, J.AMBER, None))
        for t in a:
            if t in b:
                s.append(F.line(LSB["xs"][0] + LSB["w"] / 2 + 6, _ls_y(a.index(t)), LSB["xs"][1] - LSB["w"] / 2 - 6, _ls_y(b.index(t)), J.LINE, 3,
                                dash="8 6"))
    return s


# ── over（c906 重さの矢印）＝5階の床に、前提の重さの上へ足された重さ（判決 大96 理由1「예정된 하중보다 360㎏/㎡ 이상의 과하중이 5층 기둥과 바닥 슬래브에」）。
#    矢印の長さは模式（値は札＝判決）
OV = dict(x0=200.0, x1=1720.0, top=660.0, th=40.0, cols=(420.0, 960.0, 1500.0), cw=44.0, up=470.0, pre=64.0, add=110.0,
          xs=(510.0, 600.0, 690.0, 780.0, 870.0, 1050.0, 1140.0, 1230.0, 1320.0, 1410.0))
OVER_KG = 360.0


def over_base(st0):
    g = [F.rect(OV["x0"], OV["top"], OV["x1"] - OV["x0"], OV["th"], J.BG2, J.LINE, 4)]
    for c in OV["cols"]:
        g.append(F.rect(c - OV["cw"] / 2, OV["up"], OV["cw"], OV["top"] - OV["up"], J.BG2, J.LINE, 3))
        g.append(F.rect(c - OV["cw"] / 2, OV["top"] + OV["th"], OV["cw"], 848.0 - OV["top"] - OV["th"], J.BG2, J.LINE, 3))
    g.append(_tline(OV["x0"] + 10, OV["top"] + OV["th"] + 40, "5階の床", 26, INK, "start", 150))
    return g


def _ov_y():
    """（前提の矢印の上と下, 足された矢印の上と下）の y。"""
    y1 = OV["top"] - 6
    return (y1 - OV["pre"], y1), (y1 - OV["pre"] - 8 - OV["add"], y1 - OV["pre"] - 8)


def over_stage(prev, st):
    s = []
    (p0, p1), (a0, a1) = _ov_y()
    if _on(prev, st, "pre"):
        for x in OV["xs"]:
            s.append(_arrow(x, p0, x, p1, J.LINE, 5, 16))
    if _on(prev, st, "add"):
        for x in OV["xs"]:
            s.append(_arrow(x, a0, x, a1, J.ALERT, 6, 18))
    return s


# ── cover（c908 床の断面）＝屋上の床の上の防水の層と押えコンクリート（国会の報告 p.29「옥상슬래브 위에 덧씌운 콘크리트(누름콘크리트)」）。
#    🔴 厚さの数（3〜6センチ／15センチ）は次の c909 の語り＝描かない・厚さは模式
CV = dict(x0=260.0, x1=1660.0, top=600.0, th=56.0, cols=(560.0, 1360.0), cw=64.0, wp=10.0, cc=64.0)


def cover_base(st0):
    g = [F.rect(CV["x0"], CV["top"], CV["x1"] - CV["x0"], CV["th"], J.BG2, J.LINE, 4)]
    for c in CV["cols"]:
        g.append(F.rect(c - CV["cw"] / 2, CV["top"] + CV["th"], CV["cw"], 848.0 - CV["top"] - CV["th"], J.BG2, J.LINE, 4))
    g.append(_tline(CV["x0"] + 10, CV["top"] + CV["th"] + 44, "屋上の床", 28, INK, "start", 220))
    return g


def _cv_y():
    y_wp = CV["top"] - CV["wp"]
    return y_wp, y_wp - CV["cc"]


def cover_stage(prev, st):
    s = []
    y_wp, y_cc = _cv_y()
    x0, x1 = CV["x0"], CV["x1"]
    if _on(prev, st, "q"):                          # 重さを増やす物（まだ名を言わない）＝黄の破線と「？」
        s.append(F.rect(x0, y_cc, x1 - x0, CV["top"] - y_cc, "none", J.AMBER, 4, dash="12 8"))
        s.append(_qmark(960.0, (y_cc + y_wp) / 2, 44, J.AMBER))
    if _on(prev, st, "cover"):                      # ⚠️ 網の線を引かない（下の段の「？」を線が通ると geom_gap が鳴る）＝塗りで覆う
        s.append(F.rect(x0, y_wp, x1 - x0, CV["wp"], J.USCG, None, op=0.9))
        s.append(F.rect(x0, y_cc, x1 - x0, CV["cc"], J.BG2, None))
        s.append(F.rect(x0, y_cc, x1 - x0, CV["cc"], J.LINE_DIM, INK, 4, op=0.9))
    return s


# ── duct（c910 部材の立体）＝屋上を支える北側のコアの耐力壁を、5階の厨房の排気のダクトのために横に切った（国会の報告 p.29「배기닥트의 설치를 위하여
#    옥상바닥을 받치는 북측 코아 내력벽을 수평방향으로 절단(벽체길이 160㎝ 중 98㎝ 절단)」・判決 大96 理由1「5층 식당 주방의 배기덕트 설치를 위하여」）。
#    🔴 穴の長さの比＝壁の長さ 160 のうち 98（国会の報告）＝門番が照らす。数（40×98・160）は次の c911 の語り＝描かない。壁の高さ・厚さ・穴の高さと場所は模式
DU = dict(x0=520.0, x1=1240.0, top=430.0, bot=800.0, d=(90.0, -60.0), f0=0.18, sy=(466.0, 536.0), sl=(300.0, 1460.0, 400.0), sd=1.5)
DU_CUT = (98.0, 160.0)


def du_slot():
    x0, x1 = DU["x0"], DU["x1"]
    a = x0 + (x1 - x0) * DU["f0"]
    return a, a + (x1 - x0) * DU_CUT[0] / DU_CUT[1]


def duct_base(st0):
    g = []
    x0, x1, top, bot = DU["x0"], DU["x1"], DU["top"], DU["bot"]
    dx, dy = DU["d"]
    g.append(F.poly([(x1, top), (x1 + dx, top + dy), (x1 + dx, bot + dy), (x1, bot)], J.BG2, J.LINE, 3, close=True))
    g.append(F.rect(x0, top, x1 - x0, bot - top, J.BG2, INK, 4))
    sx0, sx1, sy = DU["sl"]                        # 屋上の床（壁の上に載る板＝前の面は壁の前の面にそろえる）
    th = top - sy
    ex, ey = dx * DU["sd"], dy * DU["sd"]
    g.append(F.poly([(sx0, sy), (sx1, sy), (sx1 + ex, sy + ey), (sx0 + ex, sy + ey)], J.BG2, J.LINE, 3, close=True))
    g.append(F.poly([(sx1, sy), (sx1 + ex, sy + ey), (sx1 + ex, sy + ey + th), (sx1, top)], J.BG2, J.LINE, 3, close=True))
    g.append(F.rect(sx0, sy, sx1 - sx0, th, J.BG2, J.LINE, 3))
    g.append(F.line(260.0, bot, 1500.0, bot, J.LINE, 4))
    g.append(_tline(sx0 - 10, top - 6, "屋上の床", 26, J.TICK, "end", 200))
    g.append(_tline(x0, bot + 40, "北側の耐力壁（コア）", 28, INK, "start", 500))
    return g


def duct_stage(prev, st):
    s = []
    a, b = du_slot()
    y0, y1 = DU["sy"]
    ym = (y0 + y1) / 2
    r = (y1 - y0) / 2 - 8
    if _on(prev, st, "duct"):                      # 厨房の排気のダクト（会社の工事＝橙）＝穴の左の端まで
        s.append(F.rect(130.0, ym - r, a - 130.0, 2 * r, J.BG2, J.COMPANY, 4))
        s.append(F.poly([(130.0 + 12 * math.cos(math.radians(t)), ym + r * math.sin(math.radians(t))) for t in range(90, 271, 15)], "none",
                        J.COMPANY, 4))
    if _on(prev, st, "cut"):
        s.append(F.rect(a, y0, b - a, y1 - y0, J.BG, J.ALERT, 5))
        s.append(F.line(a + 6, ym, b - 20, ym, J.COMPANY, 3, dash="10 8"))     # ダクトは穴を通る（破線）
    if _on(prev, st, "load"):                       # 建物の重さを受け持つ（穴より下の壁へ）
        for x in ((a + b) / 2 - 120, (a + b) / 2 + 120, DU["x1"] - 50):
            s.append(_arrow(x, y1 + 40 if a < x < b else DU["top"] + 30, x, DU["bot"] - 30, J.AMBER, 6, 18))
    return s


# ── opening（c912 部材の寄り）＝切った穴のまわり（判決 大96 理由1「아무런 보강조치를 취하지 아니함으로써 벽체의 내력을 저하」）。
#    壁の中の鉄筋は穴の縁で切れる（赤の点）・穴のまわりに入れるはずの補強の鉄（黄の破線）が無い。鉄筋の間隔と本数・穴の形は模式
OP = dict(x0=260.0, x1=1300.0, y0=330.0, y1=820.0, sx=(560.0, 1060.0), sy=(530.0, 620.0), vx=80.0, hy=70.0)


def opening_base(st0):
    x0, x1, y0, y1 = OP["x0"], OP["x1"], OP["y0"], OP["y1"]
    (a, b), (c, d) = OP["sx"], OP["sy"]
    g = [F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, INK, 4)]
    x = x0 + OP["vx"] / 2
    while x < x1:
        if a < x < b:
            g.append(F.line(x, y0 + 10, x, c, J.LINE_DIM, 3) + F.line(x, d, x, y1 - 10, J.LINE_DIM, 3))
            g.append(F.circ(x, c, 5, J.ALERT, None) + F.circ(x, d, 5, J.ALERT, None))
        else:
            g.append(F.line(x, y0 + 10, x, y1 - 10, J.LINE_DIM, 3))
        x += OP["vx"]
    y = y0 + OP["hy"] / 2
    while y < y1:
        if c < y < d:
            g.append(F.line(x0 + 10, y, a, y, J.LINE_DIM, 3) + F.line(b, y, x1 - 10, y, J.LINE_DIM, 3))
            g.append(F.circ(a, y, 5, J.ALERT, None) + F.circ(b, y, 5, J.ALERT, None))
        else:
            g.append(F.line(x0 + 10, y, x1 - 10, y, J.LINE_DIM, 3))
        y += OP["hy"]
    g.append(F.rect(a, c, b - a, d - c, J.BG, J.ALERT, 5))
    return g


def opening_stage(prev, st):
    s = []
    (a, b), (c, d) = OP["sx"], OP["sy"]
    if _on(prev, st, "none"):                       # 入れるはずの補強の鉄（破線＝無い）
        for y in (c - 26, d + 26):
            s.append(F.line(a - 90, y, b + 90, y, J.AMBER, 5, dash="12 8"))
        for x in (a - 26, b + 26):
            s.append(F.line(x, c - 80, x, d + 80, J.AMBER, 5, dash="12 8"))
        s.append(_xmark(b + 110, c - 90, 24.0, J.ALERT, 8))
    if _on(prev, st, "weak"):
        s.append(_arrow(1380.0, 580.0, 1380.0, 700.0, J.ALERT, 8, 24))
    return s


# ── joint（c913・c916 床の断面）＝床と壁のつなぎ目（壁は右）。c913＝5階の床の上の鉄筋（判決 大96 理由1「5층 슬래브 상부철근과 벽체의 정착길이는 철근지름의
#    40배인 64㎝를 확보하여야 함에도 15-18㎝ 정도로 짧게 정착」）＝長さは下の物差し（同じ縮尺＝門番が照らす）。c916＝壁は立ったまま床だけ落ちる（国会の報告 p.29
#    「붕괴 시 벽체는 그대로 있고 슬래브만 무너져 내리는 현상」）。つなぎ目の形・壁の厚さ・鉄筋が壁に入る長さの絵は模式
JT = dict(wx=(1180.0, 1300.0), top=300.0, bot=848.0, sx0=300.0, sy=(500.0, 580.0), bar=518.0, enter=40.0, fall=200.0, tilt=30.0,
          px_cm=7.0, rx=300.0, ry=(690.0, 760.0), rh=22.0)
JT_CM = dict(need=64.0, got=(15.0, 18.0))


def _jt_shift(pts, st):
    if st["fall"] != "on":
        return pts
    x0, x1 = JT["sx0"], JT["wx"][0]
    return [(x, y + JT["fall"] + JT["tilt"] * (x1 - x) / (x1 - x0)) for x, y in pts]


def joint_parts(st):
    x0, x1 = JT["sx0"], JT["wx"][0]
    y0, y1 = JT["sy"]
    slab = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    yb = JT["bar"]
    bar = [(x0 + 20, yb - 3), (x1 + JT["enter"], yb - 3), (x1 + JT["enter"], yb + 3), (x0 + 20, yb + 3)]
    return [_P("slab", "poly", _jt_shift(slab, st), fill=J.BG2, stroke=J.LINE, w=4),
            _P("bar", "poly", _jt_shift(bar, st), fill=INK if st["bar"] == "lit" else J.LINE, stroke=None)]


def joint_base(st0):
    x0, x1 = JT["wx"]
    g = [F.rect(x0, JT["top"], x1 - x0, JT["bot"] - JT["top"], J.BG2, INK, 4),
         _tline((x0 + x1) / 2, JT["top"] + 44, "壁", 30, INK, "middle", 100)]
    if st0["fl"] == "5":
        g.append(_tline(JT["sx0"] + 10, JT["sy"][0] - 18, "5階の床", 28, INK, "start", 220))
    return g


def jt_ruler():
    """物差し（同じ縮尺）の右の端の x＝（入れるべき長さ,（実際の短い方, 長い方））。"""
    x = JT["rx"]
    return x + JT_CM["need"] * JT["px_cm"], (x + JT_CM["got"][0] * JT["px_cm"], x + JT_CM["got"][1] * JT["px_cm"])


def joint_stage(prev, st):
    s = []
    x0, x1 = JT["wx"]
    if _on(prev, st, "bar", "lit"):                 # つなぎ目の輪
        s.append(F.circ(x0, JT["bar"] + 20, 74, "none", J.AMBER, 4))
    if _on(prev, st, "ruler"):
        need, (g0, g1) = jt_ruler()
        (ya, yb), h = JT["ry"], JT["rh"]
        x = JT["rx"]
        s.append(F.line(x, ya - h, x, yb + h, INK, 3))
        s.append(F.rect(x, ya - h / 2, need - x, h, "none", INK, 4, dash="10 6"))
        s.append(F.rect(x, yb - h / 2, g0 - x, h, J.ALERT, None))
        s.append(F.rect(g0, yb - h / 2, g1 - g0, h, J.ALERT, None, op=0.45))
    if _on(prev, st, "wall"):                       # 立ったままの壁
        s.append(F.rect(x0, JT["top"], x1 - x0, JT["bot"] - JT["top"], INK, None, op=0.16))
        s.append(F.rect(x0, JT["top"], x1 - x0, JT["bot"] - JT["top"], "none", INK, 8))
    return s


# ── hook（c915 部材の比べ）＝床の鉄筋を壁に入れる形（国会の報告 p.29「슬래브 속의 두 가닥 철근을 내력벽 속으로 각각 64㎝·40㎝씩 ‘ㄱ’자 형태로 꺾어 넣고
#    끝부분은 갈고리 모양으로 처리(HOOK장치)하여야 하는데도 ‘ㅣ’자형으로 갈고리장치 없이 짧게 시공」）。左＝先を曲げて引っかける形（2本・壁の中の長さの比 64：40＝
#    門番が照らす）／右＝まっすぐ短い形。数は語りに無い＝描かない・壁と床の厚さは模式
HK = dict(cx=(560.0, 1360.0), w=560.0, wall=90.0, top=400.0, bot=760.0, sy=(520.0, 590.0), bars=(536.0, 574.0), hz=(54.0, 32.0), unit=3.0,
          short=30.0)
HK_CM = (64.0, 40.0)
HK_LAB = ("先を曲げて引っかける", "まっすぐ短く")


def hk_wall_x(i):
    return HK["cx"][i] + HK["w"] / 2 - HK["wall"]


def hk_bars(i, kind):
    """パネル i の2本の鉄筋の折れ線（kind＝bent／straight）。"""
    xl, wx0 = HK["cx"][i] - HK["w"] / 2, hk_wall_x(i)
    out = []
    for y, hz, cm in zip(HK["bars"], HK["hz"], HK_CM):
        if kind == "bent":
            down = cm * HK["unit"] - hz
            x = wx0 + hz
            out.append([(xl + 20, y), (x, y), (x, y + down), (x - 6, y + down + 14), (x - 20, y + down + 16)])
        else:
            out.append([(xl + 20, y), (wx0 + HK["short"], y)])
    return out


def hook_base(st0):
    g = []
    for i, cx in enumerate(HK["cx"]):
        xl = cx - HK["w"] / 2
        wx0 = hk_wall_x(i)
        g.append(F.rect(xl, HK["sy"][0], wx0 - xl, HK["sy"][1] - HK["sy"][0], J.BG2, J.LINE, 4))
        g.append(F.rect(wx0, HK["top"], HK["wall"], HK["bot"] - HK["top"], J.BG2, J.LINE, 4))
        g.append(_tline(wx0 + HK["wall"] / 2, HK["top"] + 40, "壁", 28, J.TICK, "middle", 80))
        g.append(_tline(xl - 10, HK["sy"][1] - 22, "床", 26, J.TICK, "end", 60))
    return g


def hook_stage(prev, st):
    s = []
    for i, (f_, kind) in enumerate((("l", "bent"), ("r", "straight"))):
        if _on(prev, st, f_):
            col = INK if i == 0 else J.ALERT
            for pts in hk_bars(i, kind):
                s.append(F.poly(pts, "none", col, 6))
            s.append(_tline(HK["cx"][i], HK["bot"] + 40, HK_LAB[i], 30, col, "middle", 520))
    return s


# ── section に足す欄（c917）：A棟の北と南に残った壁（ソウル市の報告 p.37「A동 북측 잔여벽체」「A동 남측 벽체」）・床の板が外れたつなぎ目（赤の印）。
#    壁の高さと厚さは模式（A棟の両端＝屋上の両端の高い所の位置）
SC_WALL_W = 22.0


def sc_walls():
    a0, a1 = SC["xa"]
    return ((a0, a0 + SC_WALL_W), (a1 - SC_WALL_W, a1))


def section_extra_stage(prev, st):
    s = []
    top, gy = SC["roof"] - SC["core"], sc_ground()
    if _on(prev, st, "walls"):
        for x0, x1 in sc_walls():
            s.append(F.rect(x0, top, x1 - x0, gy - top, A_C, None))
    if _on(prev, st, "joints"):
        (n0, n1), (s0, s1) = sc_walls()
        for i in range(6):                          # 屋上と5〜1階の床の板の高さ
            y = _sc_slab_y(i)
            s.append(F.line(n1, y, n1 + 18, y, J.ALERT, 6) + F.line(s0 - 18, y, s0, y, J.ALERT, 6))
    return s


# ── stack（c918 積み木）＝5階に積み重なった重さ（国会の報告 p.29「대형냉장고」・白書 p.89「조적벽・돌정원」・判決 大96 理由1「대리석 및 화강석의 마감재공사,
#    15㎝ 두께의 주방 바닥콘크리트공사, 벽돌을 사용한 칸막이 벽체공사, 온돌공사, 대형냉장고 등 시설물 적치를 고려한 보강공사를 하지 아니함」）。
#    その下の柱＝図面で細くなった（国会の報告 p.29「구조계산서에는 800㎜ … 설계도면상에는 600㎜」＝太さの比 600：800＝c708 と同じ記録）。積み木の大きさは模式（重さの比ではない）
SK = dict(slab=(520.0, 1200.0, 640.0, 684.0), cx=860.0, cw=40.0, g=848.0)
SK_ITEMS = (("厨房の床", 540.0, 1180.0, 590.0, 640.0), ("大理石", 560.0, 850.0, 536.0, 590.0), ("オンドル", 870.0, 1160.0, 536.0, 590.0),
            ("冷蔵庫", 580.0, 730.0, 340.0, 536.0), ("れんがの壁", 750.0, 980.0, 400.0, 536.0), ("石の庭", 1000.0, 1160.0, 460.0, 536.0))
SK_COL_MM = (600.0, 800.0)          # 図面・計算書の柱の太さ


def stack_base(st0):
    x0, x1, y0, y1 = SK["slab"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 4),
            F.rect(SK["cx"] - SK["cw"] / 2, y1, SK["cw"], SK["g"] - y1, J.BG2, J.LINE, 4),
            _tline(x0 - 14, y1 - 10, "5階の床", 26, J.TICK, "end", 200)]


def stack_stage(prev, st):
    s = []
    if _on(prev, st, "items"):
        for t, x0, x1, y0, y1 in SK_ITEMS:
            s.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.DOC, 4, rx=4))
            cap = 30 if y1 - y0 > 80 else 26
            s.append(_tline((x0 + x1) / 2, (y0 + y1) / 2 + cap * 0.36, t, cap, INK, "middle", x1 - x0 - 16))
    if _on(prev, st, "col"):                        # 計算書の太さ（破線）と図面の太さ（赤）
        y1, g = SK["slab"][3], SK["g"]
        w_calc = SK["cw"] * SK_COL_MM[1] / SK_COL_MM[0]
        s.append(F.rect(SK["cx"] - w_calc / 2, y1 + 4, w_calc, g - y1 - 4, "none", INK, 3, dash="8 6"))
        s.append(F.rect(SK["cx"] - SK["cw"] / 2, y1, SK["cw"], g - y1, J.ALERT, J.ALERT, 3, op=0.85))
    if _on(prev, st, "noreinf"):
        s.append(_xmark(1228.0, 456.0, 18.0, J.ALERT, 7))
    return s


# ── bldg に足す欄（ca08）：4階の帯＝照明の売り場（国会の報告 p.30「4층 조명코너에서 건물 진동으로 조명등이 추락」）。🔴 **どの棟かは記録に無い＝両方の棟の4階**・
#    照明（右の札の列に形と落ちる矢印）・揺れ（左の外の矢印）
HI["f4"] = (("a", 4), ("b", 4))
HI["f4a5"] = (("a", 4), ("b", 4), ("a", 5))


def bldg_b5_stage(prev, st):
    s = []
    if _on(prev, st, "lamp"):
        s.append(_lamp(1490.0, 452.0))
        s.append(_arrow(1490.0, 484.0, 1490.0, 530.0, J.ALERT, 5, 16))
    if _on(prev, st, "shake"):
        y = bl_y(4) + BL["fh"] / 2
        s.append(_arrow(190.0, y, 130.0, y, INK, 5, 16) + _arrow(190.0, y, 250.0, y, INK, 5, 16))
    if _on(prev, st, "hi", "f4a5"):         # 🔧 試し焼き（10-19）：A棟の4階と5階が同じピンクで1つの塊に見えた＝食堂街（5階）に太い枠
        s.append(F.poly(bl_band("a", 5), "none", A_C, 6, close=True))
    return s


# ── plan に足す床（ca05・ca17）：two＝5階と屋上を並べる（判決 大96 理由1「5층 식당주방 내 기둥 주변과 최초 냉각탑이 설치되었다가 이동한 경로를 중심으로
#    슬래브에 발생한 휨변형에 의한 균열이 장기간 지속적으로 성장」）／three＝4階・5階・屋上の3枚（前触れの場所＝国会の報告 p.30・白書 p.88・判決）。
#    🔴 棟と向きは描かない（どの棟の屋上か・4階の売り場の棟は記録に無い＝床は四角だけ）・柱の並び・厨房と道すじの場所は模式
P2 = dict(r=((240.0, 420.0, 860.0, 780.0), (1000.0, 420.0, 1620.0, 780.0)), lab=("5階", "屋上"))
P3 = dict(r=((150.0, 460.0, 650.0, 740.0), (710.0, 460.0, 1210.0, 740.0), (1270.0, 460.0, 1770.0, 740.0)), lab=("4階", "5階", "屋上"),
          marks=("照明が落ちた", "水漏れ・ひび", "たわみ・ひび"))


def _p_cols(r, nx=4, ny=3):
    x0, y0, x1, y1 = r
    return [(x0 + (x1 - x0) * (i + 0.5) / nx, y0 + (y1 - y0) * (j + 0.5) / ny) for j in range(ny) for i in range(nx)]


def _p2_kitchen():
    x0, y0, x1, y1 = P2["r"][0]
    return x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 3, x1, y1


def plan_b5_base(st0):
    fl = st0["floor"]
    P = P2 if fl == "two" else P3
    g = []
    for r, t in zip(P["r"], P["lab"]):
        x0, y0, x1, y1 = r
        g.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 4))
        g.append(_tline((x0 + x1) / 2, y0 - 20, t, 30, INK, "middle", 200))
        if fl == "two":
            for x, y in _p_cols(r):
                g.append(F.rect(x - 9, y - 9, 18, 18, J.LINE_DIM, None))
    return g


def plan_b5_stage(prev, st):
    s = []
    fl = st["floor"]
    if fl == "two":
        if _on(prev, st, "kit"):                    # 5階の厨房（会社の店＝橙の面）と柱のまわりのたわみ（赤の破線の輪）
            kx0, ky0, kx1, ky1 = _p2_kitchen()
            s.append(F.rect(kx0, ky0, kx1 - kx0, ky1 - ky0, J.COMPANY, None, op=0.14))
            for x, y in _p_cols(P2["r"][0]):
                if x > kx0 and y > ky0:
                    s.append(F.poly([(x + 44 * math.cos(math.radians(a)), y + 34 * math.sin(math.radians(a))) for a in range(0, 361, 12)], "none",
                                    J.ALERT, 4, dash="8 6"))
        if _on(prev, st, "path"):                   # 屋上の冷却塔を引きずった道すじ（後ろの側→前の側＝c811 と同じ向き）とたわみ・ひび
            x0, y0, x1, y1 = P2["r"][1]
            for k in range(3):
                x = x0 + (x1 - x0) * (k + 1) / 4
                s.append(F.rect(x - 34, y0 + 40, 68, y1 - y0 - 80, J.ALERT, None, op=0.20))
                s.append(_arrow(x, y0 + 50, x, y1 - 50, J.ALERT, 5, 18, dash="12 8"))
                s.append(_zig(x + 40, y0 + 120, x + 60, y0 + 200, 3, 5.0, J.ALERT, 3))
    if fl == "three":
        if _on(prev, st, "marks"):
            r4, r5, rr = P3["r"]
            cx, cy = (r4[0] + r4[2]) / 2, (r4[1] + r4[3]) / 2
            s.append(_lamp(cx, cy - 10) + _arrow(cx, cy + 34, cx, cy + 90, J.ALERT, 5, 16))
            cx, cy = (r5[0] + r5[2]) / 2, (r5[1] + r5[3]) / 2
            for dx_, dy_ in ((-60, 30), (0, 60), (60, 30)):
                s.append(_drop(cx + dx_, cy + dy_))
            s.append(_zig(cx - 120, cy - 80, cx + 120, cy - 40, 6, 7.0, J.ALERT, 4))
            x0, y0, x1, y1 = rr
            for k in range(3):
                x = x0 + (x1 - x0) * (k + 1) / 4
                s.append(_arrow(x, y0 + 40, x, y1 - 40, J.ALERT, 5, 16, dash="10 8"))
            for r, t in zip(P3["r"], P3["marks"]):
                s.append(_tline((r[0] + r[2]) / 2, r[3] + 50, t, 28, J.ALERT, "middle", 460))
        if _on(prev, st, "up"):                     # 上の階（3枚とも）＝括弧（⚠️ 門番 layout：y 400 だと床の名の字の箱を横に貫いた）
            xa, xb = P3["r"][0][0], P3["r"][2][2]
            s.append(F.poly([(xa, 390.0), (xa, 372.0), (xb, 372.0), (xb, 390.0)], "none", J.AMBER, 4))
    return s


# ── slab に足す欄（ca03）：屋上の床の柱のまわり（z="col"・fl="roof"＝上に柱が無い）・入れるはずのドロップパネルが無い所（赤の破線）・水漏れ（しずく）。
#    白書 p.88「5층 ○○식당 … 이곳 지판이 미설치된 부분은 준공후 얼마 되지 않은 때부터 누수 및 균열현상등」（店の名は書かない）。板の大きさとしずくの場所は模式
def slab_b5_stage(prev, st):
    s = []
    if st["z"] != "col":
        return s
    cx, cw, th, top = SLC["cx"], SLC["cw"], SLC["th"], SLC["top"]
    yb = top + th
    if _on(prev, st, "dpm"):
        for a, b in ((cx - cw / 2 - 150, cx - cw / 2), (cx + cw / 2, cx + cw / 2 + 150)):
            s.append(F.rect(a, yb, b - a, 40, "none", J.ALERT, 4, dash="8 6"))
    if _on(prev, st, "leak"):
        for x, y in ((700.0, 610.0), (790.0, 650.0), (1130.0, 620.0), (1230.0, 660.0)):
            s.append(_drop(x, y))
    return s


# ── tower に足す欄（ca09）：水位の目盛り（国会の報告 p.30「냉각탑의 수위를 조절」・目盛りの数と水の高さは模式）
TG = dict(x=(640.0, 676.0), y=(470.0, 690.0), lv=dict(off=690.0, on=530.0, low=610.0))


def tower_gauge_parts(st):
    g_ = st.get("gauge", "off")
    lv = TG["lv"][g_]
    x0, x1 = TG["x"]
    return [_P("water", "poly", [(x0 + 4, lv), (x1 - 4, lv), (x1 - 4, TG["y"][1] - 4), (x0 + 4, TG["y"][1] - 4)], fill=J.USCG, stroke=None,
               alpha=0.0 if g_ == "off" else 0.75)]


def tower_gauge_stage(prev, st):
    s = []
    if prev.get("gauge", "off") == "off" and st.get("gauge", "off") != "off":
        x0, x1 = TG["x"]
        y0, y1 = TG["y"]
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, "none", INK, 4, rx=6))
        for y in range(int(y0) + 30, int(y1), 40):
            s.append(F.line(x0 - 22, y, x0 - 4, y, J.TICK, 3))
    return s


# ── insp（ca11 床の寄り）＝仕上げのある床の寄り（白書 p.85「民間の工事の竣工の検査は、図面と工事が合っているかを見るだけ」＝検察の資料と新聞を引いた節）。
#    🔴 「仕上げの下は見えない」は次の ca12 の語り＝札に書かない。厚さ・鉄筋の間隔・図面の中身は模式
IN = dict(x0=300.0, x1=1240.0, fin=(470.0, 506.0), slab=(506.0, 700.0), bars=(540.0, 666.0), tile=94.0, eye=(770.0, 372.0),
          doc=(1420.0, 380.0, 220.0, 280.0))


def insp_base(st0):
    x0, x1 = IN["x0"], IN["x1"]
    (f0, f1), (s0, s1) = IN["fin"], IN["slab"]
    g = [F.rect(x0, s0, x1 - x0, s1 - s0, J.BG2, J.LINE, 4)]
    for y in IN["bars"]:
        x = x0 + 40
        while x < x1 - 20:
            g.append(F.circ(x, y, 7, J.LINE_DIM, None))
            x += 70
    g.append(F.rect(x0, f0, x1 - x0, f1 - f0, J.DOC, J.DOC, 3, op=0.45))
    x = x0 + IN["tile"]
    while x < x1:
        g.append(F.line(x, f0, x, f1, J.BG, 3))
        x += IN["tile"]
    g.append(_tline(x0, f0 - 16, "仕上げ", 26, J.DOC, "start", 200))
    g.append(_tline(x0 + 10, s1 + 40, "床のコンクリート", 26, J.TICK, "start", 400))
    return g


def insp_stage(prev, st):
    s = []
    f0 = IN["fin"][0]
    if _on(prev, st, "eye"):                        # 外からの検査（目の印）
        ex, ey = IN["eye"]
        s.append(_eye(ex, ey))
        for x in (ex - 80, ex + 80):
            s.append(F.line(ex, ey + 30, x, f0 - 8, INK, 2, dash="6 6"))
        s.append(_qmark(ex + 90, ey - 10, 52, J.AMBER))
    if _on(prev, st, "doc"):                        # 図面と仕上げの面を見比べる（黄の破線の両矢印）
        x, y, w, h = IN["doc"]
        s.append(F.rect(x, y, w, h, J.BG2, J.DOC, 4, rx=6))
        for k in range(1, 5):
            s.append(F.line(x + 24, y + 40 + k * 44, x + w - 24, y + 40 + k * 44, J.LINE_DIM, 3))
        s.append(_tline(x + w / 2, y - 16, "図面", 28, J.DOC, "middle", 160))
        yy = (IN["fin"][0] + IN["fin"][1]) / 2
        s.append(_arrow(x - 14, yy, IN["x1"] + 16, yy, J.AMBER, 5, 18, dash="10 6") + _arrow(IN["x1"] + 16, yy, x - 14, yy, J.AMBER, 5, 18, dash="10 6"))
    return s


# ── rule（ca13・ca15 札の線）＝構造の技術者が計算で安全を確かめる決まりの線（検察の報告 p.50「층수가 16층 이상이거나 기둥과 기둥 사이 거리가 30m 이상인
#    건축물로 한정」＝どちらか一方で線の内）。ca15＝三豊（地上5階＝検察の報告 p.45・柱のあいだ 10.8m＝判決）を同じ軸に。軸は縮尺どおり（門番が照らす）
RL = dict(x0=420.0, x1=1500.0, y0=760.0, y1=330.0, mx=40.0, my=25.0)
RL_LINE = dict(floors=16, span=30.0)
RL_PT = (10.8, 5)


def rl_x(m):
    return RL["x0"] + m / RL["mx"] * (RL["x1"] - RL["x0"])


def rl_y(f):
    return RL["y0"] - f / RL["my"] * (RL["y0"] - RL["y1"])


def rl_zone():
    xs, yf = rl_x(RL_LINE["span"]), rl_y(RL_LINE["floors"])
    x0, x1, y0, y1 = RL["x0"], RL["x1"], RL["y0"], RL["y1"]
    return [(xs, y0), (xs, yf), (x0, yf), (x0, y1), (x1, y1), (x1, y0)]


def rule_base(st0):
    x0, x1, y0, y1 = RL["x0"], RL["x1"], RL["y0"], RL["y1"]
    g = [F.line(x0, y0, x1 + 20, y0, INK, 4), F.line(x0, y0, x0, y1 - 10, INK, 4)]
    for m in range(0, int(RL["mx"]) + 1, 10):
        g.append(F.line(rl_x(m), y0, rl_x(m), y0 + 12, INK, 3))
        g.append(_tline(rl_x(m), y0 + 40, str(m), 24, J.TICK, "middle", 80))
    for f in range(0, int(RL["my"]) + 1, 5):
        g.append(F.line(x0 - 12, rl_y(f), x0, rl_y(f), INK, 3))
        g.append(_tline(x0 - 20, rl_y(f) + 8, str(f), 24, J.TICK, "end", 80))
    g.append(_tline(x1 + 20, y0 + 80, "柱と柱のあいだ（メートル）", 26, J.TICK, "end", 600))
    g.append(_tline(x0 + 16, y1 - 14, "階の数", 26, J.TICK, "start", 200))
    return g


def rule_stage(prev, st):
    s = []
    if _on(prev, st, "zone"):
        c = J.ROLE["state"]
        s.append(F.poly(rl_zone(), c, None, close=True, op=0.18))
        xs, yf = rl_x(RL_LINE["span"]), rl_y(RL_LINE["floors"])
        s.append(F.poly([(RL["x0"], yf), (xs, yf), (xs, RL["y0"])], "none", c, 5))
        s.append(_tline(rl_x(1), yf - 14, f"{RL_LINE['floors']}階以上", 28, c, "start", 300))
        s.append(_tline(xs + 14, rl_y(1.2), f"{RL_LINE['span']:g}メートル以上", 28, c, "start", 260))
        s.append(_tline(rl_x(20), rl_y(21.5), "確かめる決まりがある", 30, INK, "middle", 520))
    if _on(prev, st, "pt"):
        px, py = rl_x(RL_PT[0]), rl_y(RL_PT[1])
        c = J.COMPANY
        s.append(F.line(RL["x0"], py, px - 14, py, c, 3, dash="8 6") + F.line(px, py + 14, px, RL["y0"], c, 3, dash="8 6"))
        s.append(F.circ(px, py, 13, c, None))
        s.append(_tline(px, py - 30, "三豊", 30, c, "middle", 160))
        s.append(_tline(px + 30, py + 22, f"地上{RL_PT[1]}階", 26, c, "start", 300))
        s.append(_tline(px + 30, py + 60, f"{RL_PT[0]:g}メートル", 26, c, "start", 300))
    return s


# ── items（ca16 札の並び）＝区の安全の点検で見る項目（瑞草区の報告 p.45「점검사항 - 5개분야 11개사항」の「소방안전관리 … 전기안전관리 … 가스안전관리 …
#    건축물안전관리 : 승강기, 축대·난간 관리, 노후건물·간판 관리상태」＝1回目・2回目の点検）。🔴 骨組みや床の強さの項目は無い（語り）＝破線の札に×。
#    原文の項目の写し＝「模式」を付けない
ITEMS = dict(head=("区の安全の点検（6月）", "ward"), cards=("消防", "電気", "ガス", "エレベーター", "看板"), no="建物の骨組みや床の強さ")
IB = dict(y=520.0, h=96.0, w=250.0, gap=30.0, ny=700.0, nw=560.0)


def _it_x(i):
    n = len(ITEMS["cards"])
    tot = n * IB["w"] + (n - 1) * IB["gap"]
    return 960.0 - tot / 2 + i * (IB["w"] + IB["gap"]) + IB["w"] / 2


def items_base(st0):
    t, r = ITEMS["head"]
    return [_tline(960.0, 390.0, t, 36, rc(r), "middle", 900), F.line(560.0, 412.0, 1360.0, 412.0, rc(r), 3)]


def _it_card(i):
    x = _it_x(i)
    return (F.rect(x - IB["w"] / 2, IB["y"] - IB["h"] / 2, IB["w"], IB["h"], J.BG2, rc(ITEMS["head"][1]), 4, rx=10)
            + _tline(x, IB["y"] + 12, ITEMS["cards"][i], 34, INK, "middle", IB["w"] - 24))


def items_stage(prev, st):
    s = []
    n = len(ITEMS["cards"])
    if _on(prev, st, "c0"):
        s += [_it_card(i) for i in range(min(3, n))]
    if _on(prev, st, "c1"):
        s += [_it_card(i) for i in range(3, n)]
        s.append(_tline(_it_x(n - 1) + IB["w"] / 2, IB["y"] + IB["h"] / 2 + 40, "など", 26, J.TICK, "end", 120))
    if _on(prev, st, "no"):
        x, w = 960.0, IB["nw"]
        s.append(F.rect(x - w / 2, IB["ny"] - 45, w, 90, "none", J.TICK, 4, rx=10, dash="12 8"))
        s.append(_tline(x, IB["ny"] + 12, ITEMS["no"], 32, J.TICK, "middle", w - 40))
        s.append(_xmark(x + w / 2 + 50, IB["ny"], 26.0, J.ALERT, 9))
    return s


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-19）：第10〜11章・終章の見え方（cb・cc・cd）
# ══════════════════════════════════════════════════════════
#   🔴 次のカットの語りにある数・言葉は描かない（cb05 に「6人」〈cb06〉・cb08 に「書かれていない」〈cb09〉と1,439人〈cb10〉・cc03 に表ごとの人数〈cc04・cc06・cc08〉・
#      cc11 に1人あたりの額〈cc12〉・cc16 に大法院の日付〈cc17〉・災難管理法〈cc22〉・5つの法律〈cc23〉）。🔴 名前は描かない（役職と金額だけ＝原文の名前の欄は灰の帯）
def _paper_icon(cx, cy, col, w=44.0, h=56.0):
    """紙の印（届け・書類）。"""
    g = [F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, col, 3, rx=4)]
    for k, cut in ((16, 9), (28, 9), (40, 15)):
        g.append(F.line(cx - w / 2 + 9, cy - h / 2 + k, cx + w / 2 - cut, cy - h / 2 + k, col, 2))
    return "".join(g)


# ── desk（cb02 札と線）＝行方の分からない人の届けの窓口（国会の報告 p.32「실종자신고의 접수를 서울특별시사고대책본부와 서초구청 실종신고가족안내소로
#    이분화하였다가 이후 이를 서울특별시사고대책본부로 통합관리하는 과정에서 실종자 수를 하루 만에 207명에서 410명으로 수정 발표」）。窓口の形と置き場は模式
DESK = dict(two=(("市の事故対策本部", "city"), ("区の家族の案内所", "ward")), fix=(207, 410))
DK = dict(xs=(560.0, 1360.0), y=420.0, w=560.0, h=110.0, fy=810.0)


def desk_base(st0):
    return []


def desk_stage(prev, st):
    s = []
    if _on(prev, st, "two"):
        for (t, r), x in zip(DESK["two"], DK["xs"]):
            s.append(_box(x, DK["y"], DK["w"], DK["h"], t, rc(r), rc(r), 36))
            for k in (-1, 0, 1):
                s.append(_paper_icon(x + k * 90, DK["y"] + 190, rc(r)))
            s.append(_arrow(x, DK["y"] + 152, x, DK["y"] + DK["h"] / 2 + 12, rc(r), 4, 16))
            s.append(_tline(x, DK["y"] + 266, "届け", 28, J.TICK, "middle", 200))
    if _on(prev, st, "one"):
        (xl, xr), y = DK["xs"], DK["y"]
        c = rc(DESK["two"][0][1])
        s.append(_arrow(xr - DK["w"] / 2 - 12, y + 14, xl + DK["w"] / 2 + 16, y + 14, c, 6, 24))
        s.append(_tline((xl + xr) / 2, y - 18, "まとめる", 30, c, "middle", 220))
        s.append(F.rect(xl - DK["w"] / 2 - 10, y - DK["h"] / 2 - 10, DK["w"] + 20, DK["h"] + 20, "none", c, 6, rx=14))
    if _on(prev, st, "fix"):
        a, b = DESK["fix"]
        y = DK["fy"]
        s.append(_tline(930.0, y, f"{a}人", 52, J.AMBER, "end", 300, fam="Dela"))
        s.append(_arrow(950.0, y - 18, 1110.0, y - 18, J.AMBER, 6, 24))
        s.append(_tline(1130.0, y, f"{b}人", 52, J.AMBER, "start", 300, fam="Dela"))
        s.append(_tline(1030.0, y - 76, "1日のうちに直した", 28, INK, "middle", 500))
    return s


# ── tally（cb04 数の並び）＝届けと確かめの数（ソウル市の報告 95.8.9＝国会の会議録 p.53「(95.8.8. 24:00 현재) … 신고 1,566 … 계 1,485 … 관리대상 81」）。
#    棒の長さは件数の比（確かめが済んだ＋残り＝届け）＝原文の数の写し（「模式」を付けない）
TALLY = dict(head=("8月8日の時点", "city"), total=("届け", 1566), done=("確かめが済んだ", 1485), left=("行方の分からない人", 81))
TL = dict(x0=300.0, x1=1620.0, y=560.0, h=90.0)


def tl_x(v):
    return TL["x0"] + (TL["x1"] - TL["x0"]) * v / TALLY["total"][1]


def tally_base(st0):
    t, r = TALLY["head"]
    return [_tline(TL["x0"], 400.0, t, 36, rc(r), "start", 600), F.line(TL["x0"], 420.0, TL["x1"], 420.0, rc(r), 3)]


def tally_stage(prev, st):
    s = []
    y, h = TL["y"], TL["h"]
    if _on(prev, st, "total"):
        t, v = TALLY["total"]
        s.append(F.rect(TL["x0"], y - h / 2, TL["x1"] - TL["x0"], h, "none", INK, 4))
        s.append(_tline(TL["x0"], y - h / 2 - 22, t, 30, INK, "start", 300))
        s.append(_tline(TL["x1"], y - h / 2 - 22, f"{v:,}件", 40, J.AMBER, "end", 400, fam="Dela"))
    if _on(prev, st, "done"):
        t, v = TALLY["done"]
        xd = tl_x(v)
        s.append(F.rect(TL["x0"], y - h / 2, xd - TL["x0"], h, J.LINE_DIM, None))
        s.append(_tline((TL["x0"] + xd) / 2, y + 12, t, 32, INK, "middle", xd - TL["x0"] - 40))
        s.append(_tline((TL["x0"] + xd) / 2, y + h / 2 + 64, f"{v:,}件", 40, J.AMBER, "middle", 400, fam="Dela"))
    if _on(prev, st, "left"):
        t, v = TALLY["left"]
        xd = tl_x(TALLY["done"][1])
        xm = (xd + TL["x1"]) / 2
        s.append(F.rect(xd, y - h / 2, TL["x1"] - xd, h, J.AMBER, None))
        s.append(F.line(xm, y + h / 2 + 8, xm, 718.0, J.AMBER, 3))
        s.append(_tline(xm, 776.0, f"{v}人", 48, J.AMBER, "middle", 300, fam="Dela"))
        s.append(_tline(xm, 826.0, t, 28, INK, "middle", 320))
    return s


# ── toll（cb05 箱の2回目）＝1995年10月の数（国政監査〈内務委〉のソウル市の報告 p.24「사망자 501명(사망확인 471명, 사망인정 30명)」）。原文の数の写し
#    🔴 同じ報告の「届けが出たまま確かめられない人 6人」は次の cb06 の語り＝描かない
TOLL = dict(head=("市の報告（1995年10月）", "city"), total=("亡くなった人", 501), parts=(("遺体で確かめた", 471), ("亡くなったと認めた", 30)))
TB5 = dict(x0=420.0, x1=1500.0, top=330.0, head=70.0, bot=830.0, ty=510.0, py=700.0)


def toll_base(st0):
    t, r = TOLL["head"]
    x0, x1 = TB5["x0"], TB5["x1"]
    return [F.rect(x0, TB5["top"], x1 - x0, TB5["bot"] - TB5["top"], J.BG2, rc(r), 4, rx=12),
            F.line(x0, TB5["top"] + TB5["head"], x1, TB5["top"] + TB5["head"], rc(r), 3),
            _tline((x0 + x1) / 2, TB5["top"] + 48, t, 34, rc(r), "middle", x1 - x0 - 40)]


def toll_stage(prev, st):
    s = []
    cx = (TB5["x0"] + TB5["x1"]) / 2
    if _on(prev, st, "total"):
        t, v = TOLL["total"]
        s.append(_tline(cx - 30, TB5["ty"], t, 40, INK, "end", 420))
        s.append(_tline(cx, TB5["ty"] + 8, f"{v}人", 64, J.AMBER, "start", 360, fam="Dela"))
    if _on(prev, st, "parts"):
        for (t, v), x in zip(TOLL["parts"], (cx - 260.0, cx + 260.0)):
            s.append(F.rect(x - 230, TB5["py"] - 80, 460, 160, J.BG, J.LINE, 4, rx=10))
            s.append(_tline(x, TB5["py"] - 22, t, 32, INK, "middle", 420))
            s.append(_tline(x, TB5["py"] + 52, f"{v}人", 50, J.AMBER, "middle", 420, fam="Dela"))
        s.append(_tline(cx, TB5["py"] + 18, "＋", 48, INK, "middle", 56))
    return s


# ── koseki（cb07 書類）＝戸籍の整理（白書 p.92「'95년 11월 29일을 기해 관리대상자중 30명에 대해서 호적법 제90조에 의한 호적정리」＝頁の画像）。人の形は描かない・書類の形は模式
KOSEKI = dict(n=30, day=(11, 29))
KS = dict(x=560.0, y=330.0, w=520.0, h=500.0)


def koseki_base(st0):
    x, y, w, h = KS["x"], KS["y"], KS["w"], KS["h"]
    g = [F.rect(x + 18, y + 18, w, h, J.BG2, J.LINE_DIM, 3, rx=6), F.rect(x, y, w, h, J.BG2, J.DOC, 5, rx=6),
         _tline(x + w / 2, y + 64, "戸籍", 40, J.DOC, "middle", w - 60), F.line(x + 40, y + 96, x + w - 40, y + 96, J.DOC, 3)]
    for k in (0, 1, 4):
        yy = y + 160 + k * 72
        g.append(F.line(x + 50, yy, x + w - 50 - (k % 2) * 80, yy, J.TICK, 3))
    return g


def koseki_stage(prev, st):
    s = []
    x, y, w, h = KS["x"], KS["y"], KS["w"], KS["h"]
    if _on(prev, st, "n"):
        s.append(F.rect(x + 40, y + 250, w - 80, 120, J.BG, J.AMBER, 4, rx=8))
        s.append(_tline(x + w / 2, y + 290, "遺体の見つからない", 28, INK, "middle", w - 120))
        s.append(_tline(x + w / 2, y + 352, f"{KOSEKI['n']}人", 52, J.AMBER, "middle", w - 120, fam="Dela"))
        m, d = KOSEKI["day"]          # 🔧 geom_gap：書類の角に重ねた印は字が書類の枠線を横切った（−32px）＝書類の外へ
        s.append(F.circ(x + w + 130, y + h - 90, 96, J.BG, J.AMBER, 6))
        s.append(_tline(x + w + 130, y + h - 78, f"{m}月{d}日", 36, J.AMBER, "middle", 170))
    if _on(prev, st, "done"):
        s.append(_check(1270.0, 470.0, 26, J.OK))
    return s


# ── final（cb08 数の並び）＝白書の最終の数（白書 p.92「사망자 502명, 부상자 937명」「최종 사망자 수가 502명으로 확정」・戸籍の30人＝p.92・10月の471人＝国政監査 p.24）。
#    🔴 「その1人が誰で、いつ加わったのかは書かれていない」は次の cb09・1,439人は cb10 の語り＝描かない
FINAL = dict(head=("白書の最終の数", "city"), cards=(("亡くなった人", 502), ("けがをした人", 937)), koseki=30, oct=471)
FN = dict(xs=(600.0, 1320.0), y=450.0, w=560.0, h=150.0, ey=730.0)


def final_base(st0):
    t, r = FINAL["head"]
    return [_tline(L_X + 160, 330.0, t, 34, rc(r), "start", 600)]


def final_stage(prev, st):
    s = []
    if _on(prev, st, "cards"):
        for (t, v), x in zip(FINAL["cards"], FN["xs"]):
            s.append(F.rect(x - FN["w"] / 2, FN["y"] - FN["h"] / 2, FN["w"], FN["h"], J.BG2, rc(FINAL["head"][1]), 4, rx=12))
            s.append(_tline(x, FN["y"] - 22, t, 32, INK, "middle", FN["w"] - 40))
            s.append(_tline(x, FN["y"] + 52, f"{v}人", 54, J.AMBER, "middle", FN["w"] - 40, fam="Dela"))
    if _on(prev, st, "calc"):
        y = FN["ey"]
        dead = FINAL["cards"][0][1]
        k, o = FINAL["koseki"], FINAL["oct"]
        got = dead - k
        for t, x, c in ((f"{dead}", 380.0, J.AMBER), ("−", 500.0, INK), (f"{k}", 600.0, J.AMBER), ("＝", 700.0, INK), (f"{got}", 820.0, J.AMBER)):
            s.append(_tline(x, y + 18, t, 52, c, "middle", 160, fam="Dela"))
        s.append(_tline(600.0, y + 76, "戸籍で整理", 26, J.TICK, "middle", 200))
        s.append(F.rect(1240.0, y - 52, 300.0, 104.0, J.BG2, J.LINE_DIM, 4, rx=10))
        s.append(_tline(1290.0, y + 12, "10月", 30, J.TICK, "middle", 100))
        s.append(_tline(1440.0, y + 18, f"{o}", 48, J.TICK, "middle", 160, fam="Dela"))
        s.append(_arrow(900.0, y, 1226.0, y, J.AMBER, 4, 18) + _arrow(1226.0, y, 900.0, y, J.AMBER, 4, 18))
        s.append(_tline(1063.0, y - 22, f"{got - o}人多い", 30, J.AMBER, "middle", 260))
    return s


# ── ages（cb11 棒の2回目）＝亡くなった人の年代（白書 p.93 の表「0세 부터 10세 14명 … 21세 부터 30세 258명 … 60세 이상 6명 · 총계 502명」＝頁の画像を
#    10-19 に原寸で読んだ）。棒の高さは人数の比（数は字幕・いちばん多い年代の札だけ）。🔴 割合の欄は出さない（501人で割った値＝白書の中で合わない）・
#    男女の数は次の cb12 の語り＝描かない。⚠️ 棒の型 qty は行の名に数字を許さない（年代の名が数字）＝模式図の型で描く
AGES = (("0〜10歳", 14), ("11〜20歳", 71), ("21〜30歳", 258), ("31〜40歳", 80), ("41〜50歳", 52), ("51〜60歳", 21), ("60歳以上", 6))
AG = dict(x0=300.0, x1=1620.0, base=780.0, top=400.0, bw=120.0)


def ag_x(i):
    step = (AG["x1"] - AG["x0"]) / len(AGES)
    return AG["x0"] + step * (i + 0.5)


def ag_h(v):
    return (AG["base"] - AG["top"]) * v / max(v_ for _t, v_ in AGES)


def ages_base(st0):
    g = [F.line(AG["x0"] - 20, AG["base"], AG["x1"] + 20, AG["base"], INK, 4)]
    for i, (t, _v) in enumerate(AGES):
        g.append(_tline(ag_x(i), AG["base"] + 44, t, 28, J.TICK, "middle", 176))
    return g


def ages_stage(prev, st):
    s = []
    if _on(prev, st, "bars"):
        for i, (_t, v) in enumerate(AGES):
            h = ag_h(v)
            s.append(F.rect(ag_x(i) - AG["bw"] / 2, AG["base"] - h, AG["bw"], h, J.LINE_DIM, J.LINE, 3))
    if _on(prev, st, "top"):
        i = max(range(len(AGES)), key=lambda k: AGES[k][1])
        h = ag_h(AGES[i][1])
        s.append(F.rect(ag_x(i) - AG["bw"] / 2, AG["base"] - h, AG["bw"], h, J.AMBER, J.AMBER, 3))
    return s


# ── most（cb15 数の比べ）＝それまでの最多（白書 p.92「지난 48년 건국이래 … 가장 많은 희생자를 낸 사고로 기록될 것」「천재지변을 제외하고」1970年の南営号の沈没 326人＝
#    頁の画像）。棒の長さは人数の比（同じ縮尺）。人の形は描かない・船の名は語りに無い＝出さない
MOST = dict(rows=(("三豊百貨店", "1995年", 502, "ALERT"), ("船の沈没", "1970年", 326, "LINE")))
MS = dict(x0=540.0, x1=1540.0, ys=(470.0, 680.0), h=90.0, vmax=560.0)


def ms_x(v):
    return MS["x0"] + (MS["x1"] - MS["x0"]) * v / MS["vmax"]


def most_base(st0):
    return [F.line(MS["x0"], 380.0, MS["x0"], 780.0, INK, 4)]


def _ms_row(i):
    t, yr, v, r = MOST["rows"][i]
    y, h = MS["ys"][i], MS["h"]
    return (F.rect(MS["x0"], y - h / 2, ms_x(v) - MS["x0"], h, rc(r), None, op=0.9)
            + _tline(MS["x0"] - 24, y - 2, t, 34, INK, "end", 400) + _tline(MS["x0"] - 24, y + 38, yr, 28, J.TICK, "end", 300)
            + _tline(ms_x(v) + 22, y + 18, f"{v}人", 48, J.AMBER, "start", 260, fam="Dela"))


def most_stage(prev, st):
    s = []
    for i in range(2):
        if _on(prev, st, f"r{i}"):
            s.append(_ms_row(i))
    return s


# ── pen（cc13・cc23 数の比べ）＝罰の重さ（検察の報告 p.50「준공후 일정기간내에 손괴가 발생한 경우 5년이하의 징역으로 처벌」（건축업법 제59조2호）／
#    1995年12月30日の5つの法律〈法律第5137〜5141号〉「무기 또는 3년이상의 징역」＝確かめの係 F107）。横の軸＝年（同じ縮尺）・無期は右の端の外（矢じり）
PEN = dict(rows=(("事故の前", "手抜き工事で壊れたとき", 0.0, 5.0, "LINE", "5年以下の懲役"),
                 ("1995年12月30日から", "わざと手を抜いた工事で", 3.0, None, "state", "無期か3年以上の懲役")), ymax=15)
#   🔧 門番 echo：「無期または3年以上の懲役」（12字）は語りの写し＝「無期か…」（原文「무기 또는 3년이상의 징역」と同じ意味）
PN = dict(x0=600.0, x1=1520.0, ys=(470.0, 680.0), h=70.0, ax=790.0, inf=1640.0)


def pn_x(y):
    return PN["x0"] + (PN["x1"] - PN["x0"]) * y / PEN["ymax"]


def pen_base(st0):
    g = [F.line(PN["x0"], PN["ax"], PN["inf"], PN["ax"], INK, 4)]
    for y in range(0, PEN["ymax"] + 1, 5):
        g.append(F.line(pn_x(y), PN["ax"], pn_x(y), PN["ax"] + 12, INK, 3))
        g.append(_tline(pn_x(y), PN["ax"] + 44, f"{y}年", 26, J.TICK, "middle", 100))
    g.append(_tline(PN["inf"], PN["ax"] + 44, "無期", 26, J.TICK, "middle", 100))
    return g


def _pn_label(i):
    t, d, *_ = PEN["rows"][i]
    y = PN["ys"][i]
    return _tline(PN["x0"] - 30, y - 4, t, 32, INK, "end", 480) + _tline(PN["x0"] - 30, y + 36, d, 26, J.TICK, "end", 480)


def _pn_bar(i):
    _t, _d, a, b, r, lab = PEN["rows"][i]
    y, h = PN["ys"][i], PN["h"]
    x0 = pn_x(a)
    x1 = pn_x(b) if b is not None else PN["inf"] - 26
    g = [F.rect(x0, y - h / 2, x1 - x0, h, rc(r), None, op=0.9)]
    if b is None:                       # 上は無期＝右の端の外へ矢じり
        g.append(F.poly([(x1, y - h / 2 - 12), (PN["inf"] + 10, y), (x1, y + h / 2 + 12)], rc(r), None, close=True))
        g.append(_tline(x0, y - h / 2 - 18, lab, 32, rc(r), "start", 900))
    else:
        g.append(_tline(x1 + 22, y + 12, lab, 32, J.AMBER, "start", 600))
    return "".join(g)


def pen_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_pn_label(0))
    if _on(prev, st, "b0"):
        s.append(_pn_bar(0))
    if _on(prev, st, "law"):
        s.append(_pn_label(1))
    if _on(prev, st, "b1"):
        s.append(_pn_bar(1))
    return s


# ── haul（cb16 道路と車の2回目・上から）＝瓦礫を運ぶ車の線（国会の報告 p.32「유골과 유품의 일부가 건물잔해와 함께 … 집하장 등으로 실려감」・
#    国政監査〈内務委〉p.24「잔재검색은 8.14 최종완료 … 골편 등 142점과 유품 3,419점을 발견」）。🔴 場所の名は出さない（集める場所）・遺骨は描かない・
#    道と車の形・数・置き場は模式
HAUL = dict(found=(("骨片など", 142), ("遺品", 3419)), day=(8, 14), labels=("崩れた百貨店の跡", "瓦礫を集める場所"))
HL = dict(site=(150.0, 400.0, 560.0, 700.0), yard=(1360.0, 400.0, 1770.0, 700.0), road=(560.0, 1360.0, 515.0, 585.0), trucks=(700.0, 930.0, 1160.0))


def _truck(x, y, col=None):
    """上から見たトラック（右向き）＝運転台と荷台（瓦礫の網）。"""
    c = col or J.LINE
    g = [F.rect(x - 70, y - 24, 104, 48, J.BG2, c, 3, rx=4), _hatch(x - 64, y - 18, x + 28, y + 18, 14.0, J.TICK, 2, 0.8),
         F.rect(x + 40, y - 20, 30, 40, c, None, rx=5)]
    return "".join(g)


def haul_base(st0):
    x0, y0, x1, y1 = HL["site"]
    a0, b0, a1, b1 = HL["yard"]
    r0, r1, ry0, ry1 = HL["road"]
    return [F.rect(r0, ry0, r1 - r0, ry1 - ry0, J.BG2, J.LINE_DIM, 3),
            F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, A_C, 4), _hatch(x0 + 10, y0 + 10, x1 - 10, y1 - 10, 22.0, J.TICK, 2, 0.6),
            _tline((x0 + x1) / 2, y0 - 16, HAUL["labels"][0], 28, A_C, "middle", 400),
            F.rect(a0, b0, a1 - a0, b1 - b0, J.BG2, J.LINE, 4), _tline((a0 + a1) / 2, b0 - 16, HAUL["labels"][1], 28, INK, "middle", 400)]


def haul_stage(prev, st):
    s = []
    y = (HL["road"][2] + HL["road"][3]) / 2
    if _on(prev, st, "truck"):
        for x in HL["trucks"]:
            s.append(_truck(x, y))
        s.append(_arrow(HL["trucks"][-1] + 90, y, HL["yard"][0] - 14, y, INK, 4, 18, dash="10 8"))
        a0, b0, a1, b1 = HL["yard"]
        for k in range(3):
            px = a0 + 70 + k * 130
            s.append(F.poly([(px - 60, b1 - 20), (px, b1 - 110 - 20 * (k % 2)), (px + 60, b1 - 20)], J.BG2, J.TICK, 3, close=True))
    if _on(prev, st, "found"):
        a0, b0, a1, b1 = HL["yard"]
        cx = (a0 + a1) / 2
        s.append(F.circ(cx - 120, b0 + 100, 40, "none", J.ROLE["city"], 6))
        s.append(F.line(cx - 92, b0 + 128, cx - 52, b0 + 168, J.ROLE["city"], 8))
        for k, (t, v) in enumerate(HAUL["found"]):
            s.append(_tline(a0, b1 + 60 + k * 54, f"{t}{v:,}点", 34, J.AMBER, "start", a1 - a0 + 40))
    return s


# ── pay（cb18 数の並び）＝補償の支払い（白書 p.93「1996-06-14 時点で502人中464人に1,758億ウォン（平均3億8千万）」「709人に1,003億ウォン」＝頁の画像）。
#    円＝台本の目安（当時のレート）。原文の数の写し
# 🔧 門番 echo：見出しの「…の時点」「支払い（…）」は語りの写し（77%）＝日付だけ（12字未満）
PAY = dict(head="1996年6月14日", rows=(("亡くなった人", "464人分", "1,758億ウォン"), ("けがをした人", "709人", "1,003億ウォン")),
           yen="およそ240億円", avg="3億8千万ウォン")
PY = dict(x0=300.0, x1=1620.0, ys=(470.0, 760.0), h=120.0, sy=596.0)


def pay_base(st0):
    return [_tline(PY["x0"], 370.0, PAY["head"], 34, INK, "start", 700), F.line(PY["x0"], 390.0, PY["x1"], 390.0, J.LINE, 3)]


def _py_row(i):
    t, n, v = PAY["rows"][i]
    y = PY["ys"][i]
    return (F.rect(PY["x0"], y - PY["h"] / 2, PY["x1"] - PY["x0"], PY["h"], J.BG2, J.LINE_DIM, 3, rx=10)
            + _tline(PY["x0"] + 30, y + 12, t, 36, INK, "start", 320) + _tline(PY["x0"] + 400, y + 14, n, 40, J.AMBER, "start", 300, fam="Dela")
            + _tline(PY["x1"] - 30, y + 18, v, 48, J.AMBER, "end", 560, fam="Dela"))


def pay_stage(prev, st):
    s = []
    if _on(prev, st, "r0"):
        s.append(_py_row(0))
    if _on(prev, st, "sub"):            # 🔧 門番 echo：「当時のレートでおよそ240億円」は語りの写し＝名と値を別の字に（どちらも12字未満）
        y = PY["sy"]
        s.append(_tline(PY["x1"] - 30, y + 14, PAY["yen"], 32, INK, "end", 400))
        s.append(_tline(PY["x1"] - 300, y + 14, "当時のレートで", 26, J.TICK, "end", 300))
        s.append(_tline(PY["x0"] + 30, y + 14, "1人あたりの平均", 26, J.TICK, "start", 300))
        s.append(_tline(PY["x0"] + 280, y + 14, PAY["avg"], 32, INK, "start", 400))
    if _on(prev, st, "r1"):
        s.append(_py_row(1))
    return s


# ── q3（cb19 問い）＝この回の3つの問い（冒頭 c107 の語り）。3つ目を明るく（字は基図に1回だけ＝明るくする段は枠だけ）。問いの写し＝「模式」を付けない
Q3 = ("なぜ店は開いたままだったのか", "なぜ建物は崩れたのか", "誰なら止められたのか")
QB3 = dict(x0=420.0, x1=1500.0, ys=(400.0, 560.0, 720.0), h=110.0)


def q3_base(st0):
    g = []
    for i, t in enumerate(Q3):
        y = QB3["ys"][i]
        last = i == len(Q3) - 1
        g.append(F.rect(QB3["x0"], y - QB3["h"] / 2, QB3["x1"] - QB3["x0"], QB3["h"], J.BG2, J.LINE_DIM, 4, rx=14))
        g.append(F.circ(QB3["x0"] + 70, y, 34, J.LINE if last else J.LINE_DIM, None))
        g.append(_tline(QB3["x0"] + 70, y + 14, str(i + 1), 38, J.BG, "middle", 60, fam="Dela"))
        g.append(_tline(QB3["x0"] + 140, y + 14, t, 40, INK if last else J.TICK, "start", 900))
    return g


def q3_stage(prev, st):
    s = []
    if _on(prev, st, "lit"):
        y = QB3["ys"][-1]
        s.append(F.rect(QB3["x0"] - 10, y - QB3["h"] / 2 - 10, QB3["x1"] - QB3["x0"] + 20, QB3["h"] + 20, "none", J.AMBER, 7, rx=20))
    return s


# ── forms3（cc03 書類の再現の2回目）＝検察の報告の追加の罪名と別紙1〜3（国会の会議録 p.48「※추가죄명 - 뇌물공여 : 회장 … 사장 …」・p.51「별지 1 설계·시공 및
#    감리 관련 피의자 및 영장범죄사실 요지」・p.52「별지 2 유지·관리 관련 피의자 및 범죄사항 요지」・p.53「별지 3 수뢰 공무원 범죄사실 요지」）。欄の値は原文の韓国語のまま・
#    🔴 名前は灰の帯・表の行（人数と中身）は次の cc04〜cc08 の語り＝紙の頭だけ（行は灰の帯と「…」）
FORMS3 = dict(add="※추가죄명 - 뇌물공여 :", roles=("회장", "사장"),
              sheets=(("별지 1", ("설계·시공 및 감리 관련", "피의자 및 영장범죄사실 요지")),
                      ("별지 2", ("유지·관리 관련", "피의자 및 범죄사항 요지")),
                      ("별지 3", ("수뢰 공무원", "범죄사실 요지"))))
F3 = dict(ay=360.0, ax0=440.0, ax1=1400.0, xs=(380.0, 960.0, 1540.0), w=500.0, top=470.0, h=380.0)


def forms3_base(st0):
    return []


def forms3_stage(prev, st):
    s = []
    if _on(prev, st, "add"):
        y = F3["ay"]
        s.append(F.rect(F3["ax0"], y - 40, F3["ax1"] - F3["ax0"], 80, J.BG2, J.DOC, 4))
        s.append(F.txt(F3["ax0"] + 30, y + 11, FORMS3["add"], 30, INK, "Noto", "start"))
        x = F3["ax0"] + 30 + fm.width(FORMS3["add"], 30) + 30
        for r in FORMS3["roles"]:
            s.append(F.txt(x, y + 11, r, 30, J.COMPANY, "Noto", "start"))
            x += fm.width(r, 30) + 14
            s.append(F.rect(x, y - 14, 90, 30, J.LINE_DIM, None))
            x += 120
    if _on(prev, st, "sheets"):
        for (no, (h0, h1)), cx in zip(FORMS3["sheets"], F3["xs"]):
            x0, y0, w, h = cx - F3["w"] / 2, F3["top"], F3["w"], F3["h"]
            s.append(F.rect(x0, y0, w, h, J.BG2, J.DOC, 4))
            s.append(F.txt(x0 + 24, y0 + 44, no, 26, J.DOC, "Noto", "start"))
            s.append(F.txtfit(cx, y0 + 96, h0, w - 40, cap=26, col=INK, anchor="middle"))
            s.append(F.txtfit(cx, y0 + 134, h1, w - 40, cap=26, col=INK, anchor="middle"))
            s.append(F.line(x0 + 20, y0 + 162, x0 + w - 20, y0 + 162, J.DOC, 3))
            for k, cut in enumerate((60, 140, 90, 180)):
                s.append(F.rect(x0 + 34, y0 + 196 + k * 40, w - 68 - cut, 16, J.LINE_DIM, None))
            s.append(_tline(cx, y0 + h - 18, "…", 30, J.TICK, "middle", 100))
    return s


# ── acts（cc05 札の並び）＝1つ目の表（別紙1）が並べること（国会の会議録 p.51「슬래브 지판부를 얇게 시공, 슬래브 상부철근을 내려앉게」「구조계산에 반영치 않은
#    냉각탑 설치, 이동으로 슬래브 손상」「내력벽 절단 손상」）＝語りの4つ（絵の札）。どの章で見たか＝第6章（c703・c713・c715）・第7章（c803〜c815）・第8章（c910）
ACTS = dict(head=("1つ目の表が並べること", "state"), cards=("ドロップパネルを薄く", "上の鉄筋を沈めた", "冷却塔を計算に入れず", "耐力壁を切った"),
            ch=("第6章", "第6章", "第7章", "第8章"))
AC = dict(y=580.0, w=350.0, h=300.0, gap=40.0, iy=520.0)


def ac_x(i):
    n = len(ACTS["cards"])
    tot = n * AC["w"] + (n - 1) * AC["gap"]
    return 960.0 - tot / 2 + i * (AC["w"] + AC["gap"]) + AC["w"] / 2


def _ac_icon(i, cx, cy):
    if i == 0:                          # 柱の頭の板（薄い・赤）
        return (F.rect(cx - 120, cy - 50, 240, 26, J.BG2, J.LINE, 3) + F.rect(cx - 60, cy - 24, 120, 10, J.ALERT, None)
                + F.rect(cx - 20, cy - 14, 40, 74, J.BG2, J.LINE, 3))
    if i == 1:                          # 床の中の上の鉄筋（正しい位置＝破線・沈んだ＝赤）
        return (F.rect(cx - 130, cy - 40, 260, 70, J.BG2, J.LINE, 3) + F.line(cx - 116, cy - 26, cx + 116, cy - 26, J.LINE, 3, dash="8 6")
                + F.line(cx - 116, cy + 2, cx + 116, cy + 2, J.ALERT, 5))
    if i == 2:                          # 屋上の冷却塔と動かす矢印
        return (F.line(cx - 130, cy + 40, cx + 130, cy + 40, J.LINE, 4) + F.rect(cx - 90, cy - 40, 90, 80, J.BG2, J.LINE, 3)
                + F.circ(cx - 45, cy - 40, 22, "none", J.LINE, 3) + _arrow(cx + 10, cy, cx + 110, cy, J.ALERT, 4, 16))
    return (F.rect(cx - 50, cy - 60, 100, 130, J.BG2, J.LINE, 3) + F.rect(cx - 50, cy - 10, 70, 34, J.BG, J.ALERT, 4))   # 耐力壁と切った穴


def acts_base(st0):
    t, r = ACTS["head"]
    return [_tline(960.0, 370.0, t, 34, rc(r), "middle", 900), F.line(560.0, 392.0, 1360.0, 392.0, rc(r), 3)]


def _ac_card(i):
    x = ac_x(i)
    return (F.rect(x - AC["w"] / 2, AC["y"] - AC["h"] / 2, AC["w"], AC["h"], J.BG2, rc(ACTS["head"][1]), 4, rx=12)
            + _ac_icon(i, x, AC["iy"]) + _tline(x, AC["y"] + 104, ACTS["cards"][i], 30, INK, "middle", AC["w"] - 24))


def acts_stage(prev, st):
    s = []
    if _on(prev, st, "c0"):
        s += [_ac_card(0), _ac_card(1)]
    if _on(prev, st, "c1"):
        s += [_ac_card(2), _ac_card(3)]
    if _on(prev, st, "seen"):
        for i, ch in enumerate(ACTS["ch"]):
            x = ac_x(i)
            s.append(F.rect(x - AC["w"] / 2 - 8, AC["y"] - AC["h"] / 2 - 8, AC["w"] + 16, AC["h"] + 16, "none", J.AMBER, 5, rx=16))
            s.append(_tline(x, AC["y"] + AC["h"] / 2 + 52, ch, 30, J.AMBER, "middle", 200))
    return s


# ── chair（cc07 札と線）＝2つ目の表（別紙2）の会長の欄（国会の会議録 p.52「‘무량판공법’으로 건축된 사실을 잘 알고 있고 … 균열이 발생한 사실을 보고 받아
#    건축붕괴의 이상징후를 알고 있음에도 사람들을 대피시키지 아니한 채 방치한 과실」）。🔴 時刻（14:30）は語りに無い＝描かない・c307 の書類の再現と別の絵（札だけ）
CHAIR = dict(head=("2つ目の表・会長の欄", "company"), cards=("梁の無い作りと知っていた", "ひびの報告を受けた", "逃がさず放っておいた"), fault="過失")
CH = dict(x=960.0, ys=(430.0, 590.0, 750.0), w=760.0, h=96.0)


def chair_base(st0):
    t, r = CHAIR["head"]
    return [_tline(L_X + 40, 330.0, t, 34, rc(r), "start", 700)]


def _ch_card(i, col):
    y = CH["ys"][i]
    return _box(CH["x"], y, CH["w"], CH["h"], CHAIR["cards"][i], col, INK, 34)


def chair_stage(prev, st):
    s = []
    c = rc(CHAIR["head"][1])
    if _on(prev, st, "c12"):
        s += [_ch_card(0, c), _arrow(CH["x"], CH["ys"][0] + CH["h"] / 2 + 8, CH["x"], CH["ys"][1] - CH["h"] / 2 - 10, c, 5, 18), _ch_card(1, c)]
    if _on(prev, st, "c3"):
        s += [_arrow(CH["x"], CH["ys"][1] + CH["h"] / 2 + 8, CH["x"], CH["ys"][2] - CH["h"] / 2 - 10, c, 5, 18), _ch_card(2, c)]
        x = CH["x"] + CH["w"] / 2 + 110
        s.append(F.circ(x, CH["ys"][2], 62, J.BG, J.ALERT, 6))
        s.append(_tline(x, CH["ys"][2] + 14, CHAIR["fault"], 38, J.ALERT, "middle", 110))
    return s


# ── fake（cc09 書類）＝現場を見ずに書いた報告の書類（判決 大96 判示事項[5]「허위의 복명서를 작성한 후 대규모소매점개설신고서를 수리한 행위가 … '직무상 부정한 행위'」・
#    国会の会議録 p.53〈別紙3〉「백화점 개설승인 관련, 허위복명서 작성」＝市の職員）。書類と店の形は模式・人は描かない
FAKE = dict(head=("市の職員（店を開く承認の手続き）", "city"), row="現場を見た")
FK = dict(doc=(300.0, 380.0, 420.0, 440.0), shop=(1220.0, 440.0, 1640.0, 760.0), eye=(980.0, 600.0))


def fake_base(st0):
    t, r = FAKE["head"]
    return [_tline(L_X + 40, 330.0, t, 32, rc(r), "start", 800)]


def fake_stage(prev, st):
    s = []
    c = rc(FAKE["head"][1])
    if _on(prev, st, "site"):
        x0, y0, x1, y1 = FK["shop"]
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 4))
        s.append(F.poly([(x0 - 20, y0), ((x0 + x1) / 2, y0 - 70), (x1 + 20, y0)], "none", J.LINE, 4))
        s.append(F.rect((x0 + x1) / 2 - 50, y1 - 120, 100, 120, J.BG, J.LINE, 3))
        s.append(_tline((x0 + x1) / 2, y0 + 70, "百貨店", 32, INK, "middle", 300))
        ex, ey = FK["eye"]
        s.append(_eye(ex, ey, c))
        s.append(F.line(ex + 60, ey, x0 - 20, ey, c, 3, dash="10 8"))
        s.append(_xmark(ex, ey, 34.0, J.ALERT, 8))
    if _on(prev, st, "doc"):
        x, y, w, h = FK["doc"]
        s.append(F.rect(x, y, w, h, J.BG2, c, 5, rx=6))
        s.append(_tline(x + w / 2, y + 56, "報告の書類", 34, c, "middle", w - 40))
        s.append(F.line(x + 30, y + 84, x + w - 30, y + 84, c, 3))
        for k in range(3):
            s.append(F.line(x + 40, y + 140 + k * 50, x + w - 60 - (k % 2) * 60, y + 140 + k * 50, J.TICK, 3))
        yy = y + h - 80
        s.append(F.rect(x + 40, yy - 26, 52, 52, J.BG, J.AMBER, 4))
        s.append(_check(x + 66, yy, 20, J.AMBER))
        s.append(_tline(x + 112, yy + 12, FAKE["row"], 32, J.AMBER, "start", w - 130))
    return s


# ── bribe（cc11 札の比べ）＝よく語られる話と検察の表（国会の会議録 p.53〈別紙3〉の15人の額＝区の12人 8,180万ウォン・市の3人 900万ウォン・計 9,080万ウォン／
#    「1,300万」は2審で刑を改めた3人の追徴の合計＝高96 主文＝総額ではない）。棒の長さは額の比（同じ縮尺）。🔴 1人あたりの額は次の cc12 の語り＝描かない
BRIBE = dict(rumor=1300, ward=(12, 8180), city=(3, 900))
BR = dict(x0=760.0, x1=1760.0, vmax=11000.0, ys=(460.0, 660.0), h=70.0, lx=420.0)


def br_x(v):
    return BR["x0"] + (BR["x1"] - BR["x0"]) * v / BR["vmax"]


def bribe_base(st0):
    return [F.line(BR["x0"], 380.0, BR["x0"], 760.0, INK, 4)]


def bribe_stage(prev, st):
    s = []
    if _on(prev, st, "rumor"):
        y = BR["ys"][0]
        s.append(F.rect(BR["lx"] - 260, y - 80, 520, 160, J.BG2, J.TICK, 4, rx=14, dash="14 10"))
        s.append(_tline(BR["lx"], y - 30, "よく語られる話", 30, J.TICK, "middle", 480))
        s.append(_tline(BR["lx"], y + 22, "区への総額", 32, J.TICK, "middle", 480))
        s.append(_tline(BR["lx"], y + 66, "1,300万ウォン", 34, J.TICK, "middle", 480))
        s.append(F.rect(BR["x0"], y - BR["h"] / 2, br_x(BRIBE["rumor"]) - BR["x0"], BR["h"], "none", J.TICK, 4, dash="10 8"))
    if _on(prev, st, "ward"):
        y = BR["ys"][1]
        n, v = BRIBE["ward"]
        c = rc("state")
        s.append(F.rect(BR["lx"] - 260, y - 60, 520, 120, J.BG2, c, 4, rx=14))
        s.append(_tline(BR["lx"], y + 12, "検察の表", 34, c, "middle", 480))
        xe = br_x(v)
        s.append(F.rect(BR["x0"], y - BR["h"] / 2, xe - BR["x0"], BR["h"], J.ROLE["ward"], None))
        s.append(_tline((BR["x0"] + xe) / 2, y + 12, f"区の{n}人", 32, J.BG, "middle", 300))
        s.append(_tline((BR["x0"] + xe) / 2, y + BR["h"] / 2 + 52, f"{v:,}万ウォン", 38, J.AMBER, "middle", 400, fam="Dela"))
    if _on(prev, st, "city"):
        y = BR["ys"][1]
        n, v = BRIBE["city"]
        xa = br_x(BRIBE["ward"][1])
        xe = br_x(BRIBE["ward"][1] + v)
        s.append(F.rect(xa, y - BR["h"] / 2, xe - xa, BR["h"], J.ROLE["city"], None))
        s.append(_tline((xa + xe) / 2, y + BR["h"] / 2 + 52, f"市の{n}人", 30, J.ROLE["city"], "middle", 200))
        tot = BRIBE["ward"][1] + v
        s.append(F.poly([(BR["x0"], y - BR["h"] / 2 - 18), (BR["x0"], y - BR["h"] / 2 - 34), (xe, y - BR["h"] / 2 - 34), (xe, y - BR["h"] / 2 - 18)],
                        "none", J.AMBER, 3))
        s.append(_tline((BR["x0"] + xe) / 2, y - BR["h"] / 2 - 50, f"計{tot:,}万ウォン", 38, J.AMBER, "middle", 500, fam="Dela"))
    return s


# ── shelf（cc15 書類）＝図面を残す決まりは5年だけ（国会の会議録 p.49「대형건축물에 대한 설계도면 등의 보존연한이 5년에 불과 … 본건의 경우에는 구청에서만
#    설계도면 보존」＝cc14 の語りの絵）。棚と図面の形は模式
SHELF = dict(years=5, l=("設計と工事の会社", "LINE"), r=("区", "ward"))
SF = dict(xs=(560.0, 1360.0), y0=440.0, y1=800.0, w=440.0)


def shelf_base(st0):
    g = []
    for (t, r), cx in zip((SHELF["l"], SHELF["r"]), SF["xs"]):
        x0 = cx - SF["w"] / 2
        g.append(F.rect(x0, SF["y0"], SF["w"], SF["y1"] - SF["y0"], J.BG2, rc(r), 4))
        for k in (1, 2):
            yy = SF["y0"] + (SF["y1"] - SF["y0"]) * k / 3
            g.append(F.line(x0, yy, x0 + SF["w"], yy, rc(r), 3))
        g.append(_tline(cx, SF["y0"] - 22, f"{t}の棚", 32, rc(r), "middle", 520))
    cx = SF["xs"][1]
    for k in range(3):                  # 区の棚＝図面（紙の筒）
        yy = SF["y0"] + (SF["y1"] - SF["y0"]) * (k + 1) / 3 - 14
        for j in range(5):
            x = cx - SF["w"] / 2 + 50 + j * 76
            g.append(F.rect(x - 26, yy - 66, 52, 66, J.BG, J.DOC, 3, rx=6))
    g.append(_tline(SF["xs"][0], (SF["y0"] + SF["y1"]) / 2 + 12, "空", 44, J.TICK, "middle", 100))
    return g


def shelf_stage(prev, st):
    s = []
    if _on(prev, st, "rule"):
        s.append(_tline(960.0, 360.0, f"残す決まりは{SHELF['years']}年だけ", 36, J.AMBER, "middle", 700))
    return s


# ── stages（cc18 札と線）＝判決の言葉（判決 大96 判決要旨[1]「건축계획의 수립, 건축설계, 건축공사공정, 건물 완공 후의 유지관리 등에 있어서의 과실이 복합적으로 작용」）。
#    段階は時の向き（左→右の矢羽根）・過失は段階ごとの赤い札が下の「崩れた」へ集まる＝cd04 の札の並びと別の絵
STAGES = dict(head=("大法院の判決", "state"), cards=("計画", "設計", "工事", "建ったあとの管理"))
SG = dict(x0=200.0, x1=1720.0, y=500.0, h=110.0, fy=640.0, by=800.0)


def _sg_seg(i):
    n = len(STAGES["cards"])
    w = (SG["x1"] - SG["x0"]) / n
    return SG["x0"] + i * w, SG["x0"] + (i + 1) * w


def stages_base(st0):
    t, r = STAGES["head"]
    return [_tline(L_X + 40, 330.0, t, 34, rc(r), "start", 600)]


def stages_stage(prev, st):
    s = []
    y, h = SG["y"], SG["h"]
    if _on(prev, st, "cards"):
        for i, t in enumerate(STAGES["cards"]):
            a, b = _sg_seg(i)
            k = 34.0
            pts = [(a + (k if i else 0), y - h / 2), (b - 6, y - h / 2), (b - 6 + k, y), (b - 6, y + h / 2), (a + (k if i else 0), y + h / 2)]
            if i:
                pts.append((a + 2 * k, y))
            s.append(F.poly(pts, J.BG2, J.LINE, 4, close=True))
            s.append(_tline((a + b) / 2 + 20, y + 12, t, 34, INK, "middle", b - a - 70))
    if _on(prev, st, "fault"):
        for i in range(len(STAGES["cards"])):
            a, b = _sg_seg(i)
            cx = (a + b) / 2 + 20
            s.append(_tline(cx, SG["fy"], "過失", 30, J.ALERT, "middle", 120))
            s.append(_arrow(cx, SG["fy"] + 14, 960.0 + (cx - 960.0) * 0.18, SG["by"] - 46, J.ALERT, 4, 16))
        s.append(_box(960.0, SG["by"], 360.0, 84.0, "重なって崩れた", J.ALERT, J.ALERT, 32))
    return s


# ── chain（cc19 鎖）＝段階ごとの人を、まとめて罪に問う（判決 大96 判示事項[1]「각 단계별 관련자들을 업무상과실치사상죄의 공동정범으로 처단한 사례」）。
#    4つの段階の札が1本の鎖でつながる＝cc18 の矢羽根と別の絵。人の形は描かない
CHAIN = dict(cards=("計画", "設計", "工事", "建ったあとの管理"), pos=((380.0, 560.0), (760.0, 450.0), (1160.0, 450.0), (1540.0, 560.0)))
CN = dict(w=300.0, h=96.0, ring=16.0, oy=790.0)


def chain_base(st0):
    return []


def chain_stage(prev, st):
    s = []
    if _on(prev, st, "link"):
        P = CHAIN["pos"]
        for (ax, ay), (bx, by) in zip(P, P[1:]):
            L = math.hypot(bx - ax, by - ay)
            n = int((L - CN["w"]) / (CN["ring"] * 1.6))
            for k in range(n):
                u = 0.5 + (k - (n - 1) / 2) * (CN["ring"] * 1.6) / L
                s.append(F.circ(ax + (bx - ax) * u, ay + (by - ay) * u, CN["ring"], "none", J.ROLE["state"], 5))
        for t, (x, y) in zip(CHAIN["cards"], P):
            s.append(_box(x, y, CN["w"], CN["h"], t, J.LINE, INK, 32))
    if _on(prev, st, "one"):
        s.append(_box(960.0, CN["oy"], 360.0, 84.0, "1か所だけ", J.TICK, J.TICK, 32, dash="12 8"))
        s.append(_xmark(960.0 + 230.0, CN["oy"], 26.0, J.ALERT, 8))
    return s


# ── gap（cc20 切れた線）＝区の職員の違反と崩壊（判決 大99「위 공무원들의 직무의무위반행위와 이 사건 붕괴사고 사이에 상당인과관계가 있다고 인정할 수는 없다」
#    「서울고등법원에 환송」）。線の長さと置き場は模式
GAP = dict(l=("区の職員の違反", "ward"), r=("崩壊", "ALERT"))
GP = dict(xl=460.0, xr=1460.0, y=560.0, wl=440.0, wr=300.0, h=120.0, cut=(880.0, 1040.0))


def gap_base(st0):
    return []


def gap_stage(prev, st):
    s = []
    y = GP["y"]
    a, b = GP["xl"] + GP["wl"] / 2 + 12, GP["xr"] - GP["wr"] / 2 - 12
    if _on(prev, st, "line"):
        (tl, rl), (tr, rr) = GAP["l"], GAP["r"]
        s.append(_box(GP["xl"], y, GP["wl"], GP["h"], tl, rc(rl), rc(rl), 36))
        s.append(_box(GP["xr"], y, GP["wr"], GP["h"], tr, rc(rr), rc(rr), 40))
        s.append(F.line(a, y, b, y, J.LINE, 5, dash="14 10"))
    if _on(prev, st, "cut"):
        c0, c1 = GP["cut"]
        s.append(F.rect(c0, y - 20, c1 - c0, 40, J.BG, None))
        s.append(_zig(c0, y - 34, c0, y + 34, 4, 8.0, J.ALERT, 5) + _zig(c1, y - 34, c1, y + 34, 4, 8.0, J.ALERT, 5))
        s.append(_tline(960.0, y - 70, "原因と結果の関係", 32, rc("state"), "middle", 600))
        s.append(_tline(960.0, y + 92, "あるとまでは認めない", 32, rc("state"), "middle", 600))
        s.append(_arrow(1380.0, 760.0, 1100.0, 800.0, rc("state"), 4, 18))
        s.append(_tline(1080.0, 812.0, "裁判のやり直し", 30, rc("state"), "end", 500))
    return s


# ── causes（cc21 札と線＝流れ図の2回目）＝国会の報告が挙げる原因（国会の報告 p.28「설계·시공·감리 및 유지·관리상의 결함과 행정관청의 감독부실 등이 복합적
#    요인으로 작용」）。4つの欠陥の札（左の列）と役所の監督の不備（下）が「重なった」へ＝c312 の流れと別の形
CAUSES = dict(head=("国会の報告が挙げる原因", "state"), cards=("設計", "工事", "監理", "建ったあとの管理"), gov="役所の監督", marks=("欠陥", "不備"))
CS = dict(x=500.0, ys=(430.0, 515.0, 600.0, 685.0), w=380.0, h=70.0, gy=810.0, bx=780.0, mx=1340.0, my=620.0)


def causes_base(st0):
    t, r = CAUSES["head"]
    return [_tline(L_X + 40, 330.0, t, 34, rc(r), "start", 700)]


def causes_stage(prev, st):
    s = []
    if _on(prev, st, "four"):
        for t, y in zip(CAUSES["cards"], CS["ys"]):
            s.append(_box(CS["x"], y, CS["w"], CS["h"], t, J.LINE, INK, 30))
        y0, y1 = CS["ys"][0] - CS["h"] / 2, CS["ys"][-1] + CS["h"] / 2
        s.append(F.poly([(CS["bx"] - 30, y0), (CS["bx"], y0), (CS["bx"], y1), (CS["bx"] - 30, y1)], "none", J.ALERT, 4))
        s.append(_tline(CS["bx"] + 30, (y0 + y1) / 2 + 12, CAUSES["marks"][0], 34, J.ALERT, "start", 120))
    if _on(prev, st, "gov"):
        s.append(_box(CS["x"], CS["gy"], CS["w"], CS["h"], CAUSES["gov"], J.LINE, INK, 30))
        s.append(_tline(CS["bx"] + 30, CS["gy"] + 12, CAUSES["marks"][1], 34, J.ALERT, "start", 120))
        y0, y1 = CS["ys"][0] - CS["h"] / 2, CS["ys"][-1] + CS["h"] / 2
        s.append(_arrow(CS["bx"] + 150, (y0 + y1) / 2, CS["mx"] - 200, CS["my"] - 20, J.ALERT, 5, 20))
        s.append(_arrow(CS["bx"] + 150, CS["gy"], CS["mx"] - 200, CS["my"] + 30, J.ALERT, 5, 20))
        s.append(_box(CS["mx"], CS["my"], 380.0, 120.0, "重なった", J.ALERT, J.ALERT, 40))
    return s


# ── open（cd02 札と線）＝開いたままの店（国会の報告 p.32「붕괴에 대한 안이한 판단과 백화점의 경영적 측면 등을 고려하여 고객과 직원을 긴급대피시키지 아니하고
#    영업종료 후 보수·보강공사만 하기로 결정」・検察の報告 p.48「고객·직원들을 대피시키지 아니함」）。合図 → 掛けた札 → 出口（人は描かない）＝c312 の札の流れと別の絵
OPEN = dict(sign="営業のあとに直す", who="客と従業員")
OPN = dict(sig=(360.0, 580.0), sign=(960.0, 600.0), door=(1520.0, 600.0))   # ⚠️ OP は opening（c912）の表＝名前を分けた


def open_base(st0):
    return []


def open_stage(prev, st):
    s = []
    if _on(prev, st, "sig"):
        x, y = OPN["sig"]
        s.append(F.rect(x - 170, y - 90, 340, 180, J.BG2, J.AMBER, 4, rx=12))
        s.append(_zig(x - 120, y - 40, x + 120, y - 20, 6, 10.0, J.ALERT, 5))
        s.append(_tline(x, y + 56, "朝からの合図", 32, J.AMBER, "middle", 300))
    if _on(prev, st, "sign"):
        x, y = OPN["sign"]
        c = J.COMPANY
        s.append(_arrow(OPN["sig"][0] + 184, OPN["sig"][1], x - 200, y, J.LINE, 5, 20))
        s.append(F.poly([(x - 120, y - 50), (x, y - 140), (x + 120, y - 50)], "none", J.TICK, 3))
        s.append(F.circ(x, y - 140, 8, J.TICK, None))
        s.append(F.rect(x - 180, y - 50, 360, 110, J.BG2, c, 5, rx=10))
        s.append(_tline(x, y + 16, OPEN["sign"], 34, c, "middle", 330))
        dx, dy = OPN["door"]
        s.append(_arrow(x + 196, y, dx - 130, dy, J.LINE, 5, 20))
        s.append(F.rect(dx - 100, dy - 150, 200, 260, J.BG2, J.LINE, 4))
        s.append(F.circ(dx + 60, dy - 10, 9, J.LINE, None))
        s.append(_arrow(dx + 100, dy + 60, dx + 230, dy + 60, INK, 4, 16, dash="10 8"))
        s.append(_xmark(dx + 170, dy + 60, 22.0, J.ALERT, 7))
        s.append(_tline(dx, dy + 160, OPEN["who"], 30, INK, "middle", 300))
    return s


# ── blocks（cd03 積み木の2回目）＝重なったもの（判決 大96 判決要旨[1]「과실이 복합적으로 작용」・中身は第6〜8章の記録）＝下の段＝弱い作り（細い柱・薄い板・沈んだ鉄筋）・
#    上の段＝載った重さ（冷却塔・食堂街）・右＝切られた壁。c918（5階の物の積み木）と別の絵。積み木の大きさは模式（重さの比ではない）
BLOCKS = dict(low=("細い柱", "薄い板", "沈んだ鉄筋"), up=("冷却塔の重さ", "食堂街の重さ"), wall="重さを支える壁")
BLK = dict(g=820.0, low=((300.0, 600.0), (620.0, 920.0), (940.0, 1240.0)), ly=640.0, up=((340.0, 740.0), (780.0, 1200.0)), uy=470.0,
           wall=(1360.0, 1480.0, 380.0), cut=(560.0, 620.0))      # ⚠️ BK は bunko（c213）の表＝名前を分けた


def blocks_base(st0):
    return [F.line(220.0, BLK["g"], 1600.0, BLK["g"], J.LINE, 4)]


def blocks_stage(prev, st):
    s = []
    if _on(prev, st, "low"):
        for t, (a, b) in zip(BLOCKS["low"], BLK["low"]):
            s.append(F.rect(a, BLK["ly"], b - a, BLK["g"] - BLK["ly"], J.BG2, J.ALERT, 4, rx=4))
            s.append(_tline((a + b) / 2, (BLK["ly"] + BLK["g"]) / 2 + 12, t, 34, INK, "middle", b - a - 30))
    if _on(prev, st, "up"):
        for t, (a, b) in zip(BLOCKS["up"], BLK["up"]):
            s.append(F.rect(a, BLK["uy"], b - a, BLK["ly"] - BLK["uy"] - 8, J.BG2, J.DOC, 4, rx=4))
            s.append(_tline((a + b) / 2, (BLK["uy"] + BLK["ly"]) / 2 + 8, t, 34, INK, "middle", b - a - 30))
            for k in (0.3, 0.7):
                x = a + (b - a) * k
                s.append(_arrow(x, BLK["uy"] - 70, x, BLK["uy"] - 12, J.DOC, 4, 16))
        w0, w1, wt = BLK["wall"]
        c0, c1 = BLK["cut"]
        s.append(F.rect(w0, wt, w1 - w0, BLK["g"] - wt, J.BG2, J.LINE, 4))
        s.append(F.rect(w0 - 4, c0, w1 - w0 + 8, c1 - c0, J.BG, J.ALERT, 5))
        s.append(_tline(w1 + 24, wt + 40, BLOCKS["wall"], 30, INK, "start", 330))
        s.append(_tline(w1 + 24, (c0 + c1) / 2 + 12, "切られた", 30, J.ALERT, "start", 200))
    return s


# ── stop（cd04 札の並び）＝止められた所（国会の報告 p.28「설계·시공·감리 및 유지·관리상의 결함과 행정관청의 감독부실」）。5つの札の下に欠陥と不備・
#    上に「1人ではない」の括弧＝cc21 の流れ図と別の絵（並べるだけ）
STOP = dict(head=("国会の報告が挙げる所", "state"), cards=("設計", "工事", "監理", "建ったあとの管理", "役所の監督"), marks=("欠陥", "欠陥", "欠陥", "欠陥", "不備"))
SP5 = dict(y=560.0, w=300.0, h=110.0, gap=30.0, my=680.0, by=440.0)


def sp5_x(i):
    n = len(STOP["cards"])
    tot = n * SP5["w"] + (n - 1) * SP5["gap"]
    return 960.0 - tot / 2 + i * (SP5["w"] + SP5["gap"]) + SP5["w"] / 2


def stop_base(st0):
    t, r = STOP["head"]
    return [_tline(960.0, 340.0, t, 32, rc(r), "middle", 800)]


def stop_stage(prev, st):
    s = []
    if _on(prev, st, "cards"):
        for i, t in enumerate(STOP["cards"]):
            s.append(_box(sp5_x(i), SP5["y"], SP5["w"], SP5["h"], t, J.LINE, INK, 32))
    if _on(prev, st, "mk"):
        for i, t in enumerate(STOP["marks"]):
            x = sp5_x(i)
            s.append(F.line(x, SP5["y"] + SP5["h"] / 2 + 8, x, SP5["my"] - 34, J.ALERT, 4))
            s.append(_tline(x, SP5["my"] + 8, t, 34, J.ALERT, "middle", 200))
    if _on(prev, st, "one"):
        xa, xb = sp5_x(0) - SP5["w"] / 2, sp5_x(len(STOP["cards"]) - 1) + SP5["w"] / 2
        y = SP5["by"]
        s.append(F.poly([(xa, y + 30), (xa, y), (xb, y), (xb, y + 30)], "none", J.AMBER, 4))
    return s


# ── cards の組（cc12＝札の2回目・cd07）。c518 の「rescue」は上の CARDS のまま
CARD_SETS = dict(
    # rescue（c518）＝上の CARDS（`_cset` が毎回引く＝ここに写さない）
    # cc12＝検察の表（国会の会議録 p.53〈別紙3〉「금 100만 원 수뢰」〜「금 1,400만 원 수뢰」・15人の計 9,080万ウォン）・円は台本の目安（1995年のレート）
    bribe=dict(head=("受け取ったとされる額（検察の表）", "state"),
               rows=(("1人あたり", "100万〜1,400万ウォン"), ("15人の合計", "9,080万ウォン"), ("1995年のレートで", "およそ1,100万円"))),
    # cd07＝ソウル市の公告（2026-06＝事故を悼む新しい造形の作品の公募の最終の結果）。置く場所の名は語らない
    art=dict(head=("2026年6月", "city"), rows=(("ソウル市が選んだ", "新しい造形の作品"),)),
)


# ══════════════════════════════════════════════════════════
#  見え方の表
# ══════════════════════════════════════════════════════════
def _lab_plan(st0):
    if st0["floor"] == "area":
        return "上から見た床（全部の階を足した広さ）"
    if st0["floor"] == "ct":
        return "上から見た屋上（冷却塔の置き場）"
    if st0["floor"] == "two":
        return "上から見た5階と屋上の床"
    if st0["floor"] == "three":
        return "上から見た4階・5階・屋上の床"
    return "上から見た" + PL_FLOOR.get(st0["floor"], "5階の床") if st0["floor"] != "grid" else "上から見た5階の柱の並び（一部）"


def _lab_tower(st0):
    return "斜めから見た屋上の3基の冷却塔" if st0["set"] == "three" else "斜めから見た冷却塔"


def _lab_crack(st0):
    return "横から見た屋上の床（寄り）" if st0["fl"] == "roof" else "横から見た5階の床（寄り）"


def _lab_cal(st0):
    return "暦（1995年6月〜7月）" if st0["set"] == "rescue" else "暦（1989年7月〜12月）"


def _lab_load(st0):
    if st0["set"] == "use":
        return "横から見た2つの床に載る重さ"
    return "柱が支える重さ" if st0["set"] == "col" else "横から見た屋上と5階の重さ"


def _lab_vs(st0):
    return "記録ごとの数の比べ" if st0["set"] == "count" else "よく語られる話と記録"


def _lab_cards(st0):
    return dict(rescue="記録の数（ソウル市の報告）", bribe="記録の額（検察の報告）", art="ソウル市の計画")[st0.get("set", "rescue")]


def _bldg_base2(st0):
    return bldg_base(st0) + bldg_extra_base(st0)


def _bldg_stage2(prev, st):
    return bldg_stage(prev, st) + bldg_extra_stage(prev, st) + bldg_b5_stage(prev, st)


def _bldg_parts2(st):
    return bldg_parts(st) + bldg_extra_parts(st)


def _plan_stage2(prev, st):
    return plan_stage(prev, st) + plan_extra_stage(prev, st) + plan_b5_stage(prev, st)


def _plan_parts2(st):
    return plan_parts(st) + plan_extra_parts(st)


def _slab_stage2(prev, st):
    return slab_stage(prev, st) + slab_extra_stage(prev, st) + slab_b5_stage(prev, st)


def _section_stage2(prev, st):
    return section_stage(prev, st) + section_extra_stage(prev, st)


def _slab_parts2(st):
    return slab_parts(st) + slab_extra_parts(st)


def _lab_slab(st0):
    return "横から見た床（断面）" if st0["z"] == "span" else "横から見た柱のまわりの床（断面）"


VIEWS = dict(
    section=dict(lab="横から見た建物（断面）", fields=dict(a=ONOFF, b=ONOFF, under=ONOFF, look=ONOFF, keep=ONOFF, fall=("none", "top", "all"), load=ONOFF,
                                                    walls=ONOFF, joints=ONOFF),
                 base=section_base, stage=_section_stage2, parts=sc_parts),
    bldg=dict(lab="斜めから見た建物", fields=dict(hi=tuple(HI), cell=ONOFF, bulge=ONOFF, roof=ONOFF, closed=ONOFF, open=ONOFF, spk=ONOFF, exit=ONOFF,
                                              x=ONOFF, use5=("off", "permit", "both"), q5=ONOFF, chk=ONOFF, weak=ONOFF, qroof=ONOFF, under=ONOFF,
                                              lamp=ONOFF, shake=ONOFF),
              base=_bldg_base2, stage=_bldg_stage2, parts=_bldg_parts2),
    plan=dict(lab=_lab_plan, fields=dict(floor=tuple(PL_FLOOR) + ("grid", "area", "ct", "two", "three"), scale=ONOFF, sag=ONOFF, north=ONOFF, crack=ONOFF,
                                         start=ONOFF, sink=ONOFF, goods=("off", "on", "fixed"), chk=ONOFF, nums=ONOFF, hit=ONOFF, walls=ONOFF, rubble=ONOFF,
                                         aplan=ONOFF, add=ONOFF, dp=("off", "thin", "miss"), miss_lit=ONOFF, ct=("off", "back", "moved"),
                                         kit=ONOFF, path=ONOFF, marks=ONOFF, up=ONOFF),
              base=plan_base, stage=_plan_stage2, parts=_plan_parts2),
    slab=dict(lab=_lab_slab, fields=dict(z=("span", "col"), fl=("none", "5", "4", "roof"), sag=ONOFF, same=ONOFF, beam=("off", "plan"), night=ONOFF,
                                         crack=ONOFF, sink=ONOFF, punch=ONOFF, bar=("off", "ok", "sunk"), box=ONOFF, dpm=ONOFF, leak=ONOFF),
              base=slab_base, stage=_slab_stage2, parts=_slab_parts2),
    tower=dict(lab=_lab_tower, fields=dict(set=("one", "three"), run=ONOFF, drain=ONOFF, load=ONOFF, roof=ONOFF, gauge=("off", "on", "low")),
               base=tower_base, stage=tower_stage, parts=tower_parts),
    bunko=dict(lab="大きさの比べ（同じ縮尺）", fields=dict(br=ONOFF, col=ONOFF), base=bunko_base, stage=bunko_stage),
    crack=dict(lab=_lab_crack, fields=dict(fl=("5", "roof"), crack=("off", "on", "long"), load=ONOFF), base=crack_base, stage=crack_stage, parts=crack_parts),
    meeting=dict(lab="会議の机と役職の札（人は描かない）", fields=dict(lit=ONOFF, tell=ONOFF), base=meeting_base, stage=meeting_stage),
    doc=dict(lab="計算書と建物（人は描かない）", fields=dict(paper=ONOFF, load=ONOFF), base=doc_base, stage=doc_stage),
    form=dict(lab="検察の報告の別紙2（原文のまま）", fields=dict(h0=ONOFF, h1=ONOFF, h2=ONOFF), base=form_base, stage=form_stage),
    flow=dict(lab="報告の判断の流れ", fields=dict(b1=ONOFF, b2=ONOFF), base=flow_base, stage=flow_stage),
    table=dict(lab="点検の期間", fields=dict(r1=ONOFF, r2=ONOFF, why=ONOFF), base=table_base, stage=table_stage),
    clocks=dict(lab="記録ごとの時刻", fields=dict(set=tuple(CK_SET), k0=("off", "on", "lit", "dim"), k1=("off", "on", "lit", "dim"),
                                                k2=("off", "on", "lit", "dim"), br=ONOFF),
                base=clocks_base, stage=clocks_stage),
    night=dict(lab="夜の現場（人は描かない）", fields=dict(q=ONOFF), base=night_base, stage=night_stage),
    # 🆕 ⑤b-4（第4〜7章）
    road=dict(lab="上から見た現場のまわりの道路と車", fields=dict(jam=ONOFF, amb=("off", "on", "blocked")), base=road_base, stage=road_stage),
    wall=dict(lab="横から見た北側の壁（断面）", fields=dict(rubble=("on", "clear")), base=wall_base, stage=wall_stage, parts=wall_parts),
    cal=dict(lab=_lab_cal, fields=dict(set=tuple(CAL_SET), d0=ONOFF, d1=ONOFF, band=ONOFF, open=ONOFF), base=cal_base, stage=cal_stage),
    cards=dict(lab=_lab_cards, fields=dict(set=("rescue", "bribe", "art"), r0=ONOFF, r1=ONOFF, r2=ONOFF), base=cards_base, stage=cards_stage),
    nums=dict(lab="持ち物を返すセンターの数", fields=dict(place=ONOFF, n=ONOFF), base=nums_base, stage=nums_stage),
    redo=dict(lab="使い道が変わったときの手順", fields=dict(loop=ONOFF, x=ONOFF), base=redo_base, stage=redo_stage),
    sheets=dict(lab="継ぎ足された計算", fields=dict(add=ONOFF), base=sheets_base, stage=sheets_stage, parts=sheets_parts),
    rank=dict(lab="全国の百貨店の順位（店の形は順位だけ）", fields=dict(r0=ONOFF, r1=ONOFF), base=rank_base, stage=rank_stage),
    beam=dict(lab="斜めから見た柱と梁と床", fields=dict(r=ONOFF, l=ONOFF, lit=ONOFF, q=ONOFF), base=beam_base, stage=beam_stage),
    drop=dict(lab="横から見た柱の頭（断面）", fields=dict(dp=ONOFF, up=ONOFF), base=drop_base, stage=drop_stage),
    spans=dict(lab="横から見た床と柱（断面）", fields=dict(sag=ONOFF, joint=ONOFF), base=spans_base, stage=spans_stage, parts=spans_parts),
    colx=dict(lab="柱の断面の比べ（同じ縮尺）", fields=dict(both=ONOFF), base=colx_base, stage=colx_stage),
    load=dict(lab=_lab_load, fields=dict(set=("col", "sum", "use"), cap=("same", "less"), brit=ONOFF, roofw=ONOFF, q5=ONOFF, sk=ONOFF, food=ONOFF),
              base=load_base, stage=load_stage, parts=load_parts),
    hoop=dict(lab="斜めから見た柱の中の鉄筋", fields=dict(l=ONOFF, r=ONOFF, cut=ONOFF), base=hoop_base, stage=hoop_stage),
    persq=dict(lab="1平方メートルにかかる重さの目安", fields=dict(l=ONOFF, r=ONOFF), base=persq_base, stage=persq_stage),
    calc=dict(lab="構造の計算書の欄", fields=dict(miss=ONOFF, plan=ONOFF), base=calc_base, stage=calc_stage),
    vs=dict(lab=_lab_vs, fields=dict(set=tuple(VS_SET), c0=ONOFF, c1=ONOFF, lit=ONOFF), base=vs_base, stage=vs_stage),
    drag=dict(lab="横から見た屋上の床（断面）", fields=dict(split=ONOFF, pos=("start", "moved")), base=drag_base, stage=drag_stage, parts=drag_parts),
    # 🆕 ⑤b-5（第8〜9章）
    lists=dict(lab="記録が挙げる5階の物", fields=dict(k=ONOFF, w=ONOFF, diff=ONOFF), base=lists_base, stage=lists_stage),
    over=dict(lab="横から見た5階の床にかかる重さ", fields=dict(pre=ONOFF, add=ONOFF), base=over_base, stage=over_stage),
    cover=dict(lab="横から見た屋上の床（断面）", fields=dict(q=ONOFF, cover=ONOFF), base=cover_base, stage=cover_stage),
    duct=dict(lab="斜めから見た北側の耐力壁", fields=dict(duct=ONOFF, cut=ONOFF, load=ONOFF), base=duct_base, stage=duct_stage),
    opening=dict(lab="切った穴のまわり（寄り）", fields=dict(none=ONOFF, weak=ONOFF), base=opening_base, stage=opening_stage),
    joint=dict(lab="横から見た床と壁のつなぎ目（断面）", fields=dict(fl=("none", "5"), bar=("off", "lit"), ruler=ONOFF, fall=ONOFF, wall=ONOFF),
               base=joint_base, stage=joint_stage, parts=joint_parts),
    hook=dict(lab="床の鉄筋を壁に入れる形の比べ（断面）", fields=dict(l=ONOFF, r=ONOFF), base=hook_base, stage=hook_stage),
    stack=dict(lab="5階に積み重なった重さ", fields=dict(items=ONOFF, col=ONOFF, noreinf=ONOFF), base=stack_base, stage=stack_stage),
    insp=dict(lab="横から見た仕上げのある床（寄り）", fields=dict(eye=ONOFF, doc=ONOFF), base=insp_base, stage=insp_stage),
    rule=dict(lab="計算を確かめる決まりの線（階の数と柱のあいだ）", fields=dict(zone=ONOFF, pt=ONOFF), base=rule_base, stage=rule_stage),
    items=dict(lab="区の安全の点検の項目", fields=dict(c0=ONOFF, c1=ONOFF, no=ONOFF), base=items_base, stage=items_stage),
    # 🆕 ⑤b-6（第10〜11章・終章）
    desk=dict(lab="行方の分からない人の届けの窓口", fields=dict(two=ONOFF, one=ONOFF, fix=ONOFF), base=desk_base, stage=desk_stage),
    tally=dict(lab="届けと確かめの数（ソウル市の報告）", fields=dict(total=ONOFF, done=ONOFF, left=ONOFF), base=tally_base, stage=tally_stage),
    toll=dict(lab="国会に出した数（市の報告）", fields=dict(total=ONOFF, parts=ONOFF), base=toll_base, stage=toll_stage),
    koseki=dict(lab="戸籍の整理（人の形は描かない）", fields=dict(n=ONOFF, done=ONOFF), base=koseki_base, stage=koseki_stage),
    final=dict(lab="白書の数と10月の数", fields=dict(cards=ONOFF, calc=ONOFF), base=final_base, stage=final_stage),
    ages=dict(lab="亡くなった人の年代（白書の表）", fields=dict(bars=ONOFF, top=ONOFF), base=ages_base, stage=ages_stage),
    most=dict(lab="亡くなった人の数の比べ（同じ縮尺）", fields=dict(r0=ONOFF, r1=ONOFF), base=most_base, stage=most_stage),
    pen=dict(lab="罰の重さの比べ（懲役の年）", fields=dict(q=ONOFF, b0=ONOFF, law=ONOFF, b1=ONOFF), base=pen_base, stage=pen_stage),
    haul=dict(lab="上から見た瓦礫を運ぶ道", fields=dict(truck=ONOFF, found=ONOFF), base=haul_base, stage=haul_stage),
    pay=dict(lab="補償の支払い（白書）", fields=dict(r0=ONOFF, sub=ONOFF, r1=ONOFF), base=pay_base, stage=pay_stage),
    q3=dict(lab="3つの問い", fields=dict(lit=ONOFF), base=q3_base, stage=q3_stage),
    forms3=dict(lab="検察の報告の罪名と別紙（原文のまま）", fields=dict(add=ONOFF, sheets=ONOFF), base=forms3_base, stage=forms3_stage),
    acts=dict(lab="1つ目の表の中身（検察の報告）", fields=dict(c0=ONOFF, c1=ONOFF, seen=ONOFF), base=acts_base, stage=acts_stage),
    chair=dict(lab="2つ目の表の会長の欄（札だけ）", fields=dict(c12=ONOFF, c3=ONOFF), base=chair_base, stage=chair_stage),
    fake=dict(lab="現場を見ずに書いた書類（人は描かない）", fields=dict(site=ONOFF, doc=ONOFF), base=fake_base, stage=fake_stage),
    bribe=dict(lab="よく語られる話と検察の表（同じ縮尺）", fields=dict(rumor=ONOFF, ward=ONOFF, city=ONOFF), base=bribe_base, stage=bribe_stage),
    shelf=dict(lab="図面を残す棚", fields=dict(rule=ONOFF), base=shelf_base, stage=shelf_stage),
    stages=dict(lab="判決が挙げる段階", fields=dict(cards=ONOFF, fault=ONOFF), base=stages_base, stage=stages_stage),
    chain=dict(lab="段階ごとの人をつなぐ鎖", fields=dict(link=ONOFF, one=ONOFF), base=chain_base, stage=chain_stage),
    gap=dict(lab="違反と崩壊のつながり", fields=dict(line=ONOFF, cut=ONOFF), base=gap_base, stage=gap_stage),
    causes=dict(lab="国会の報告の原因の流れ", fields=dict(four=ONOFF, gov=ONOFF), base=causes_base, stage=causes_stage),
    open=dict(lab="開いたままの店（人は描かない）", fields=dict(sig=ONOFF, sign=ONOFF), base=open_base, stage=open_stage),
    blocks=dict(lab="重なったもの（積み木）", fields=dict(low=ONOFF, up=ONOFF), base=blocks_base, stage=blocks_stage),
    stop=dict(lab="止められた所（国会の報告）", fields=dict(cards=ONOFF, mk=ONOFF, one=ONOFF), base=stop_base, stage=stop_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
HEAD_ONLY = dict(plan=("floor",), slab=("z", "fl"), clocks=("set",), bldg=("under",), tower=("set",), crack=("fl",), cal=("set",), load=("set",),
                 vs=("set",), joint=("fl",), cards=("set",))
ORDER = dict(section=dict(fall=("none", "top", "all")), plan=dict(goods=("off", "on", "fixed"), dp=("off", "thin", "miss"), ct=("off", "back", "moved")),
             road=dict(amb=("off", "on", "blocked")), wall=dict(rubble=("on", "clear")), slab=dict(bar=("off", "ok", "sunk")),
             crack=dict(crack=("off", "on", "long")), load=dict(cap=("same", "less")), drag=dict(pos=("start", "moved")),
             bldg=dict(use5=("off", "permit", "both")), tower=dict(gauge=("off", "on", "low")))
NOT_SCHEMATIC = ("form", "cal", "cards", "vs", "lists", "items",   # 原文の欄・記録の日付と数・項目の写し（左上に「模式」を付けない）
                 "tally", "toll", "final", "ages", "most", "pen", "pay", "q3", "forms3", "acts", "bribe", "stop")   # 🆕 ⑤b-6（数と長さは記録の比・原文の写し）
VIEW_DIR = ("横から", "上から", "斜めから")


def lab_of(view, st0):
    lab = VIEWS[view]["lab"]
    return lab(st0) if callable(lab) else lab


TAG_AT = dict(
    section=dict(r1=(1360.0, 360.0, "start", 470.0), r2=(1360.0, 470.0, "start", 470.0), r3=(1360.0, 580.0, "start", 470.0),
                 r4=(1360.0, 690.0, "start", 470.0)),
    bldg=dict(t=(L_X, 330.0, "start", 560.0), t2=(L_X, 380.0, "start", 560.0), r1=(1460.0, 430.0, "start", 380.0), r2=(1460.0, 560.0, "start", 380.0),
              r3=(1460.0, 690.0, "start", 380.0), low=(L_X, 860.0, "start", 1000.0)),
    plan=dict(r1=(1390.0, 440.0, "start", 450.0), r2=(1390.0, 540.0, "start", 450.0), r3=(1390.0, 640.0, "start", 450.0),
              r4=(1390.0, 740.0, "start", 450.0), g=(1090.0, 540.0, "start", 440.0), nwt=(240.0, 388.0, "start", 400.0),
              swt=(799.0, 388.0, "end", 400.0)),
    slab=dict(t=(L_X, 330.0, "start", 520.0), r=(1460.0, 380.0, "start", 380.0), low=(L_X, 830.0, "start", 1000.0), mid=(960.0, 640.0, "middle", 600.0),
              br=(1124.0, 610.0, "start", 190.0), r2=(1440.0, 650.0, "start", 400.0),
              lowl=(272.0, 640.0, "start", 400.0),      # 🔧 試し焼き（10-18）：「同じ板の上と下」を左下（y 830）に置くと板から遠かった   # ⚠️ geom_gap：br を x 1180 に置くと右の柱が字を覆った
              lowe=(440.0, 640.0, "end", 400.0)),       # 🆕 ⑤b-5（ca03）：⚠️ geom_gap：lowl（左寄せ）だと右上への引き出し線が字の左上の角から浅く出て 1.8px＝右寄せで線を字から離す
    tower=dict(t=(L_X, 330.0, "start", 560.0), r1=(1300.0, 380.0, "start", 520.0), r2=(1300.0, 470.0, "start", 520.0),
               dr=(744.0, 784.0, "end", 128.0)),       # 🔧 試し焼き（10-18）：x 380 だと水を抜く矢印（x 820）から遠かった・806 は脚に触れた（geom_gap）
    bunko=dict(br=(790.0, 600.0, "end", 300.0), col=(492.0, 330.0, "start", 340.0), r=(1460.0, 500.0, "start", 380.0)),   # ⚠️ 門番 layout：br を x 470 に置くと柱が札を覆った
    crack=dict(t=(L_X, 330.0, "start", 560.0), r=(1040.0, 600.0, "start", 520.0)),
    meeting=dict(t=(L_X, 330.0, "start", 560.0), t2=(L_X, 390.0, "start", 560.0)),
    doc=dict(t=(L_X, 330.0, "start", 560.0), t2=(L_X, 390.0, "start", 560.0), r=(1080.0, 360.0, "start", 520.0), low=(380.0, 850.0, "start", 520.0)),
    form=dict(low=(960.0, 840.0, "middle", 1300.0)),
    flow=dict(),
    table=dict(r=(1540.0, 610.0, "start", 300.0)),
    clocks=dict(top=(960.0, 340.0, "middle", 900.0), br=(960.0, 336.0, "middle", 600.0)),   # ⚠️ geom_gap：br を y 360 にすると括弧の線が字を貫いた
    night=dict(t=(L_X, 330.0, "start", 640.0), t2=(L_X, 390.0, "start", 640.0)),
    # 🆕 ⑤b-4
    road=dict(r1=(1440.0, 400.0, "start", 400.0), r3=(1440.0, 700.0, "start", 400.0), low=(L_X + 40, 760.0, "start", 900.0)),
    wall=dict(r=(1200.0, 440.0, "start", 560.0)),
    cal=dict(low=(435.0, 790.0, "start", 1050.0), r=(1505.0, 650.0, "start", 330.0), low1=(300.0, 760.0, "start", 1300.0), t=(L_X, 330.0, "start", 800.0)),
    cards=dict(),
    nums=dict(low=(960.0, 800.0, "middle", 1200.0)),
    redo=dict(r=(1440.0, 720.0, "start", 400.0)),      # 🔧 試し焼き（10-18）：y 640 だと輪の矢じりが「判決」を指して見えた
    sheets=dict(top=(1100.0, 340.0, "start", 700.0), low=(380.0, 810.0, "start", 1300.0)),
    rank=dict(t=(L_X, 330.0, "start", 700.0)),
    beam=dict(t=(L_X, 330.0, "start", 700.0)),
    drop=dict(r1=(1240.0, 600.0, "start", 560.0), r2=(1240.0, 720.0, "start", 560.0)),
    spans=dict(t=(L_X, 330.0, "start", 900.0)),
    colx=dict(t=(L_X, 330.0, "start", 900.0)),
    load=dict(t=(L_X, 330.0, "start", 520.0), r=(1460.0, 420.0, "start", 380.0), r2=(1460.0, 560.0, "start", 380.0)),
    hoop=dict(t=(L_X, 296.0, "start", 560.0), r=(1350.0, 470.0, "start", 490.0), r2=(1350.0, 600.0, "start", 490.0)),   # ⚠️ t を y 330 にすると左の柱の上の楕円（y 318〜）に字が触れる
    persq=dict(t=(L_X, 330.0, "start", 800.0), t2=(L_X, 390.0, "start", 800.0), r=(1100.0, 420.0, "start", 700.0)),
    calc=dict(r1=(1000.0, 360.0, "start", 820.0), r2=(1160.0, 460.0, "start", 660.0)),
    vs=dict(low=(560.0, 760.0, "middle", 700.0)),
    drag=dict(t=(L_X, 330.0, "start", 700.0), l=(L_X, 500.0, "start", 340.0)),
    # 🆕 ⑤b-5
    lists=dict(low=(960.0, 820.0, "middle", 900.0)),
    over=dict(l1=(L_X, 640.0, "start", 230.0), l2=(L_X, 520.0, "start", 270.0)),
    cover=dict(l=(270.0, 500.0, "start", 520.0), r=(1470.0, 450.0, "start", 360.0)),
    duct=dict(dl=(120.0, 580.0, "start", 380.0), r1=(1380.0, 480.0, "start", 440.0), r2=(1380.0, 640.0, "start", 440.0)),
    opening=dict(r1=(1340.0, 430.0, "start", 480.0), r2=(1420.0, 660.0, "start", 400.0)),
    joint=dict(t=(L_X, 330.0, "start", 600.0), r=(1340.0, 430.0, "start", 480.0),
               rn=(jt_ruler()[0] + 22.0, JT["ry"][0] + 10.0, "start", 600.0), rg=(jt_ruler()[1][1] + 24.0, JT["ry"][1] + 10.0, "start", 600.0)),
    hook=dict(t=(L_X, 330.0, "start", 600.0), hl=(HK["cx"][0], 370.0, "middle", 400.0), hr=(HK["cx"][1], 370.0, "middle", 400.0)),
    stack=dict(t=(L_X, 330.0, "start", 420.0), cl=(920.0, 790.0, "start", 600.0), r=(1260.0, 470.0, "start", 500.0)),
    insp=dict(r=(1290.0, 760.0, "start", 520.0)),
    rule=dict(t=(L_X, 330.0, "start", 300.0), pt=(690.0, 560.0, "end", 300.0)),
    items=dict(),
    # 🆕 ⑤b-6
    desk=dict(), tally=dict(), toll=dict(), final=dict(), pay=dict(), q3=dict(r3=(1540.0, 734.0, "start", 290.0)), shelf=dict(r=(1360.0, 860.0, "middle", 700.0)),
    koseki=dict(r=(1320.0, 480.0, "start", 500.0)),
    ages=dict(top=(ag_x(2) + 84.0, 440.0, "start", 520.0)),
    most=dict(r0=(1060.0, 380.0, "start", 700.0), r1=(MS["x0"] + 30.0, 786.0, "start", 700.0)),
    pen=dict(b0=(L_X, 360.0, "start", 520.0), law=(L_X, 360.0, "start", 760.0)),
    haul=dict(low=(L_X + 40, 800.0, "start", 700.0), road=(960.0, 660.0, "middle", 560.0),
              yard=(1510.0, 470.0, "start", 250.0)),      # 🔧 門番 layout：集める場所の下（y 846）だと「市の報告」が下の注に触れた＝場所の中の上へ
    forms3=dict(add=(1430.0, 372.0, "start", 400.0)),
    acts=dict(seen=(960.0, 842.0, "middle", 600.0)),     # 🔧 geom_gap：札の上（y 438）だと札の枠に重なった＝章の印の下へ
    chair=dict(), fake=dict(gl=(900.0, 520.0, "middle", 420.0), r=(780.0, 760.0, "start", 360.0)),
    bribe=dict(), stages=dict(), chain=dict(c=(960.0, 660.0, "middle", 600.0)), gap=dict(t=(L_X + 40, 330.0, "start", 520.0)),
    causes=dict(), open=dict(q=(L_X + 40, 330.0, "start", 900.0), mid=(660.0, 700.0, "middle", 340.0), sg=(960.0, 730.0, "middle", 420.0)),
    blocks=dict(q=(L_X + 40, 330.0, "start", 700.0)),
    stop=dict(q=(L_X + 40, 330.0, "start", 700.0), one=(960.0, 412.0, "middle", 600.0)),
)
TAG_AT["load"].update(ul=(300.0, 540.0, "start", 520.0), ur=(1060.0, 360.0, "start", 620.0))
TAG_AT["bldg"].update(lr=(1530.0, 470.0, "start", 300.0), sh=(120.0, 500.0, "start", 140.0))
TAG_AT["plan"].update(b5=(550.0, 830.0, "start", 400.0), bR=(1000.0, 830.0, "start", 600.0), top=(960.0, 340.0, "middle", 800.0))
TAG_AT["tower"].update(gl=(600.0, 470.0, "end", 440.0))


def anchors(view, st):
    """札から線を引く先（画面の点）。"""
    if view == "section":
        return dict(a5=(SC["xb"][1] + 10, sc_top(5) + SC["fh"] / 2), roof=(SC["xb"][1] + 10, SC["roof"] - 10))
    if view == "bldg":
        p = bl_band("a", 5, *CELL["a5"])
        return dict(cell=(p[1][0], (p[1][1] + p[2][1]) / 2), roof=(bl_x("a")[1], bl_y(BL_N)), x=(1380.0, 600.0),
                    a5=(bl_x("a")[0] + 30.0, bl_y(5) + 20.0))     # 🆕 ⑤b-5（ca08）：⚠️ 左の外の札から引くので「5階」の札の上を通す（線と字 23px）
    if view == "plan":
        x0, y0, x1, y1 = pl_rect("a")
        return dict(nw=(x0 + 10, y0 + 30), sw=(x1 - 10, y0 + 30), hit=grid_xy("5", "E"), sag=pl_pt(0.62, 0.55))
    if view == "slab" and st["z"] == "col":
        return dict(col=(SLC["cx"] + SLC["cw"] / 2 + SLC["th"], SLC["top"]), dpm=(SLC["cx"] - SLC["cw"] / 2 - 150.0, SLC["top"] + SLC["th"] + 20.0))
    if view == "cover":
        return dict(wp=(1440.0, CV["top"] - CV["wp"] / 2))
    if view == "duct":
        return dict(slot=(du_slot()[1] + 4.0, (DU["sy"][0] + DU["sy"][1]) / 2))
    if view == "joint":
        return dict(bar=(760.0, JT["bar"]))
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
                raise ValueError(f"m23：{f_} は頭（start）だけで決める")
        cur = dict(cur, **new)
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m23：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m23：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    for f_, seq in ORDER.get(view, {}).items():
        idx = [seq.index(s[f_]) for s in out]
        if any(b < a for a, b in zip(idx, idx[1:])):
            raise ValueError(f"m23：{f_} は戻さない（{' → '.join(seq)}）")
    return out[0], out[1:]


def stage_art(view, prev, st):
    return VIEWS[view]["stage"](prev, st)


def _base(view, st0):
    """基図＋頭の状態の層（頭で on にした欄は基図に描く＝前のカットの続き）"""
    pre = dict(START[view], **{k: st0[k] for k in HEAD_ONLY.get(view, ())})
    return VIEWS[view]["base"](st0) + stage_art(view, pre, st0)


def _stage_svgs(view, steps, start, states, cap=32):
    pre = TAG_AT[view]
    stages, texts = [], []
    prev = start
    for st, stt in zip(steps, states):
        s = stage_art(view, prev, stt)
        an = anchors(view, stt)
        for tg in F._many(st.get("tag")):
            at = tg.get("at", next(iter(pre)) if pre else (L_X, 330.0))
            x, y, anchor, mw = pre[at] if isinstance(at, str) else (tuple(at) if len(at) == 4 else (at[0], at[1], "start", 420))
            c = tg.get("cap", cap)
            col = tg.get("col", INK)
            if tg.get("to"):
                tx, ty = an[tg["to"]] if isinstance(tg["to"], str) else tg["to"]
                below_d = tg.get("d") and ty > y + round(c * 0.95)
                sy = y - round(c * 0.9) if ty < y - c else y + 8 + (round(c * 0.95) if below_d else 0)
                s.append(F.line(x, sy, tx, ty, col, 2))
            s.append(F.txtfit(x, y, tg["t"], mw, cap=c, col=col, anchor=anchor))
            texts.append(tg["t"])
            if tg.get("d"):
                s.append(F.txtfit(x, y + round(c * 0.95), tg["d"], mw, cap=round(c * 0.66), col=J.TICK, anchor=anchor))
                texts.append(tg["d"])
        stages.append("".join(s) or " ")
        prev = stt
    return stages, texts


def _static_part(sh):
    a = float(sh["keys"][0].get("alpha", 1.0))
    if a <= 0.01:
        return ""
    k0 = sh["keys"][0]
    pts = F.mech_pts(sh, k0)
    return F.poly(pts, k0.get("fill", sh.get("fill")) or "none", k0.get("stroke", sh.get("stroke")), sh.get("w") or None, close=True,
                  op=(round(a, 2) if a < 0.99 else None))


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def m23(view, steps, start=None, rel=(), note="", src=""):
    """23本目の模式図。view は VIEWS の見え方。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m23：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view not in NOT_SCHEMATIC and "模式" not in note:
        raise ValueError("m23：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
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
    lab = lab_of(view, st0)
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, lab + ("" if view in NOT_SCHEMATIC else "・模式"), 1000, cap=30, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, st0, states)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="m23", view=view, start=st0, states=states, rel=list(rel), tags=texts, shapes=shapes, lab=lab,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M23）
# ══════════════════════════════════════════════════════════
def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst])
    if view == "section":
        rows = []
        for s in allst:
            ps = {p["id"]: p for p in sc_parts(s)}
            rows.append(dict(fall=s["fall"], slab_y=[min(y for _x, y in ps[f"slab{i}"]["pts"]) for i in range(SC_NSLAB)],
                             band_a={L: ps[f"band{L}"]["alpha"] for L in (5, 4, 3, 2, 1)}, conn=ps["conn"]["alpha"]))
        out.update(above=SC_ABOVE, below=SC_BELOW, use={w: [(tuple(r), t) for r, t in SC_USE[w]] for w in SC_USE},
                   a_left=SC["xa"][1] <= SC["xb"][0], a_col=A_C, b_col=B_C, rows=rows, ground=sc_ground(),
                   b3_floor=sc_top(-3) + SC["fh"], roof=SC["roof"], fh=SC["fh"])
    elif view == "bldg":
        out.update(n=BL_N, closed={k: tuple(v) for k, v in CLOSED.items()}, hi={k: tuple(v) for k, v in HI.items()}, a_col=A_C, b_col=B_C,
                   a_left=bl_x("a")[1] <= bl_x("b")[0])
    elif view == "plan":
        out.update(floor=start["floor"], sink=len(SINK_PTS), north=NORTH_SIDE, a_left=PL["xa"][1] <= PL["xb"][0], chk=tuple(B1_CHK),
                   cols=GRID["cols"], rows=GRID["rows"], hit=tuple(GRID_HIT), goods=len(GOODS), a_col=A_C,
                   grid_px={(c, r): grid_xy(c, r) for c in GRID["cols"] for r in GRID["rows"]})
    elif view == "slab":
        rows = []
        for s in allst:
            ps = {p["id"]: p for p in slab_parts(s)}
            rows.append({k: [tuple(p) for p in v["pts"]] for k, v in ps.items()})
        out.update(z=start["z"], rows=rows, top=SLS["top"] if start["z"] == "span" else SLC["top"],
                   cols=SLS["cols"] if start["z"] == "span" else (SLC["cx"],))
    elif view == "bunko":
        out.update(px_cm=BK_PX_CM, sink_cm=BK_SINK_CM, book_mm=BK_BOOK_MM, sink_px=BK_SINK_CM * BK_PX_CM,
                   book_px=tuple(v / 10 * BK_PX_CM for v in BK_BOOK_MM))
    elif view == "meeting":
        out.update(cards=tuple(t for t, _x, _y in MT_CARDS), col=J.COMPANY)
    elif view == "form":
        out.update(form=dict(title=FORM["title"], head=FORM["head"], cols=FORM["cols"], cell=FORM["cell"]), hl=tuple(FORM["hl"]),
                   boxes=[fm_phrase_box(t, i) for t, i in FORM["hl"]])
    elif view == "flow":
        out.update(head=FLOW["head"], boxes=tuple((t, r) for t, r, _p in FLOW["boxes"]))
    elif view == "table":
        out.update(rows=tuple(TB_ROWS), day=TB_DAY, day_x=tb_x(*TB_DAY, 1), bar=TB["bar"])
    elif view == "clocks":
        items = CK_SET[start["set"]]
        out.update(set=start["set"], items=tuple(items), angles=[ck_angles(t) for t, _a, _w, _r in items])
    # 🆕 ⑤b-4
    if view == "bldg":
        out.update(use5=dict(USE5), temp=tuple(HI["temp"]), under=start.get("under"))
    if view == "plan" and start["floor"] == "area":
        out.update(area=dict(AREA), split_px=_area_split())
    if view == "plan" and start["floor"] == "grid":
        out.update(dp_miss=tuple(DP_MISS))
    if view == "plan" and start["floor"] == "ct":
        rows = []
        for s in allst:
            ps = {p["id"]: p for p in plan_extra_parts(s)}
            rows.append([(sum(x for x, _y in ps[f"ct{i}"]["pts"]) / 4, sum(y for _x, y in ps[f"ct{i}"]["pts"]) / 4) for i in range(len(CT["back"]))])
        out.update(ct_n=len(CT["back"]), ct_rows=rows)
    if view == "slab" and start["z"] == "span":
        bars = []
        for s in allst:
            b = slab_extra_parts(s)[0]
            bars.append((s["bar"], min(y for _x, y in b["pts"][:SLS["n"] + 1]) - SLS["top"]))
        out.update(bars=bars, bar_off=dict(SLB))
    if view == "tower":
        out.update(set=start["set"], n=TW3["n"] if start["set"] == "three" else 1)
    if view == "crack":
        out.update(branch=len(CR_BRANCH), fl=start["fl"])
    if view == "wall":
        out.update(hbeam=len(WL["hb"]))
    if view == "cal":
        if start["set"] == "rescue":
            c = CAL_SET["rescue"]
            out.update(set="rescue", cells=[((d.year, d.month, d.day), col, row) for d, col, row in cal_cells()], fall=c["fall"], mark=c["mark"],
                       fall_cell=_cal_cell_of(c["fall"]), mark_cell=_cal_cell_of(c["mark"]))
        else:
            c = CAL_SET["move89"]
            out.update(set="move89", months=tuple(c["months"]), band=tuple(c["band"]), open=c["open"])
    if view == "cards":
        out.update(cards=dict(head=CARDS["head"], rows=tuple(CARDS["rows"])))
    if view == "nums":
        out.update(nums=dict(place=NUMS["place"], boxes=tuple(NUMS["boxes"])))
    if view == "sheets":
        out.update(sheets=SH["n"])
    if view == "rank":
        out.update(rank=tuple(RANK["rows"]))
    if view == "colx":
        out.update(colx=tuple((t, d, n, r) for t, d, n, r in CX_COLS), px_cm=CX_PX_CM, cover_cm=CX["cover_cm"])
    if view == "spans":
        out.update(long_m=SP_LONG_M, sag=(SP2["short"][3], SP2["long"][3]))
    if view == "load":
        out.update(set=start["set"], towers=len(LD["towers"]))
    if view == "persq":
        out.update(n=tuple(PQ["n"]), kg=tuple(PQ["kg"]), per=PQ_KG)
    if view == "vs":
        out.update(set=start["set"], cards=VS_SET[start["set"]])
    if view == "drag":
        rows = []
        for s in allst:
            ps = {p["id"]: p for p in drag_parts(s)}
            bx = sum(x for x, _y in ps["box"]["pts"]) / 4
            low = max(ps["slab"]["pts"][:DG["n"] + 1], key=lambda p: p[1])
            rows.append(dict(pos=s["pos"], box_x=bx, sag_x=low[0]))
        out.update(drag=rows)
    # 🆕 ⑤b-5
    if view == "section" and any(s.get("walls") == "on" for s in allst):
        out.update(walls=[tuple(w) for w in sc_walls()], a_x=tuple(SC["xa"]), b_x=tuple(SC["xb"]))
    if view == "bldg":
        out.update(f4=tuple(HI["f4"]), f4a5=tuple(HI["f4a5"]))
    if view == "plan" and start["floor"] in ("two", "three"):
        P = P2 if start["floor"] == "two" else P3
        out.update(labs=tuple(P["lab"]), marks=tuple(P.get("marks", ())))
    if view == "tower" and start["set"] == "one":
        out.update(gauge=[(s.get("gauge", "off"), TG["lv"][s.get("gauge", "off")]) for s in allst])
    if view == "load" and start["set"] == "use":
        out.update(use_items=tuple(t for t, *_ in LU_ITEMS))
    if view == "lists":
        out.update(lists=tuple((h_, r_, tuple(items)) for h_, r_, items in LISTS))
    if view == "over":
        (p0, p1), (a0, a1) = _ov_y()
        out.update(over_kg=OVER_KG, pre=(p0, p1), add=(a0, a1), top=OV["top"])
    if view == "cover":
        y_wp, y_cc = _cv_y()
        out.update(cover=dict(cc=y_cc, wp=y_wp, top=CV["top"]))
    if view == "duct":
        a, b = du_slot()
        out.update(duct=dict(frac=(b - a) / (DU["x1"] - DU["x0"]), cut=tuple(DU_CUT), slot=(a, b), wall=(DU["x0"], DU["x1"])))
    if view == "joint":
        need, (g0, g1) = jt_ruler()
        rows = []
        for s in allst:
            ps = {p["id"]: p for p in joint_parts(s)}
            rows.append(dict(fall=s["fall"], slab_y=min(y for _x, y in ps["slab"]["pts"])))
        out.update(joint=dict(need_cm=(need - JT["rx"]) / JT["px_cm"], got_cm=((g0 - JT["rx"]) / JT["px_cm"], (g1 - JT["rx"]) / JT["px_cm"]),
                              rows=rows, top=JT["sy"][0], wall=tuple(JT["wx"])))
    if view == "hook":
        def inwall(i, pts):                         # 壁の中の長さ（横＋縦＝先の引っかけは数えない）
            wx0 = hk_wall_x(i)
            seg = pts[:3] if len(pts) > 2 else pts
            L_ = 0.0
            for (xa, ya), (xb, yb) in zip(seg, seg[1:]):
                L_ += math.hypot(max(xb, wx0) - max(xa, wx0), yb - ya) if (xb > wx0 or xa > wx0) else 0.0
            return L_
        bent, straight = hk_bars(0, "bent"), hk_bars(1, "straight")
        out.update(hook=dict(bent=[inwall(0, p) for p in bent], straight=[inwall(1, p) for p in straight], hooks=[len(p) > 3 for p in bent],
                             straight_hooks=[len(p) > 3 for p in straight]))
    if view == "stack":
        out.update(stack=tuple(t for t, *_ in SK_ITEMS), col_w=(SK["cw"], SK["cw"] * SK_COL_MM[1] / SK_COL_MM[0]))
    if view == "rule":
        out.update(rule=dict(line=dict(RL_LINE), pt=tuple(RL_PT), zone=rl_zone(), pt_px=(rl_x(RL_PT[0]), rl_y(RL_PT[1])),
                             ax=dict(x0=RL["x0"], x1=RL["x1"], y0=RL["y0"], y1=RL["y1"], mx=RL["mx"], my=RL["my"])))
    if view == "items":
        out.update(items=dict(head=tuple(ITEMS["head"]), cards=tuple(ITEMS["cards"])))
    # 🆕 ⑤b-6
    if view == "cards":
        cs = _cset(start.get("set", "rescue"))
        out.update(set=start.get("set", "rescue"), cards=dict(head=tuple(cs["head"]), rows=tuple(cs["rows"])))
    if view == "desk":
        out.update(desk=dict(two=tuple(DESK["two"]), fix=tuple(DESK["fix"])))
    if view == "tally":
        out.update(tally=dict(head=tuple(TALLY["head"]), total=TALLY["total"][1], done=TALLY["done"][1], left=TALLY["left"][1],
                              x=(TL["x0"], TL["x1"]), done_x=tl_x(TALLY["done"][1])))
    if view == "toll":
        out.update(toll=dict(head=tuple(TOLL["head"]), total=TOLL["total"][1], parts=tuple(v for _t, v in TOLL["parts"])))
    if view == "koseki":
        out.update(koseki=dict(KOSEKI))
    if view == "final":
        out.update(final=dict(cards=tuple(v for _t, v in FINAL["cards"]), koseki=FINAL["koseki"], oct=FINAL["oct"]))
    if view == "ages":
        out.update(ages=dict(rows=tuple(AGES), h=tuple(ag_h(v) for _t, v in AGES), top=max(range(len(AGES)), key=lambda k: AGES[k][1])))
    if view == "most":
        out.update(most=dict(rows=tuple((t, yr, v) for t, yr, v, _r in MOST["rows"]), x0=MS["x0"], x1=tuple(ms_x(v) for _t, _y, v, _r in MOST["rows"]),
                             unit=(MS["x1"] - MS["x0"]) / MS["vmax"]))
    if view == "pen":
        out.update(pen=dict(rows=tuple((t, a, b, lab) for t, _d, a, b, _r, lab in PEN["rows"]), x=tuple((pn_x(a), pn_x(b) if b is not None else None)
                                                                                                       for _t, _d, a, b, _r, _l in PEN["rows"]),
                            x0=PN["x0"], x1=PN["x1"], ymax=PEN["ymax"], inf=PN["inf"]))
    if view == "haul":
        out.update(haul=dict(found=tuple(HAUL["found"]), day=tuple(HAUL["day"]), texts=tuple(HAUL["labels"])))
    if view == "pay":
        out.update(pay=dict(head=PAY["head"], rows=tuple(PAY["rows"]), yen=PAY["yen"], avg=PAY["avg"]))
    if view == "q3":
        out.update(q3=tuple(Q3))
    if view == "forms3":
        out.update(forms3=dict(add=FORMS3["add"], roles=tuple(FORMS3["roles"]), sheets=tuple((n, tuple(h)) for n, h in FORMS3["sheets"])))
    if view == "acts":
        out.update(acts=dict(head=tuple(ACTS["head"]), cards=tuple(ACTS["cards"]), ch=tuple(ACTS["ch"])))
    if view == "chair":
        out.update(chair=dict(head=tuple(CHAIR["head"]), cards=tuple(CHAIR["cards"])))
    if view == "fake":
        out.update(fake=dict(head=tuple(FAKE["head"])))
    if view == "bribe":
        out.update(bribe=dict(rumor=BRIBE["rumor"], ward=tuple(BRIBE["ward"]), city=tuple(BRIBE["city"]), x0=BR["x0"],
                              unit=(BR["x1"] - BR["x0"]) / BR["vmax"], xs=(br_x(BRIBE["rumor"]), br_x(BRIBE["ward"][1]),
                                                                          br_x(BRIBE["ward"][1] + BRIBE["city"][1]))))
    if view == "shelf":
        out.update(shelf=dict(years=SHELF["years"], l=tuple(SHELF["l"]), r=tuple(SHELF["r"])))
    if view == "stages":
        out.update(stages=dict(head=tuple(STAGES["head"]), cards=tuple(STAGES["cards"])))
    if view == "chain":
        out.update(chain=dict(cards=tuple(CHAIN["cards"])))
    if view == "gap":
        out.update(gap=dict(l=tuple(GAP["l"]), r=tuple(GAP["r"])))
    if view == "causes":
        out.update(causes=dict(head=tuple(CAUSES["head"]), cards=tuple(CAUSES["cards"]), gov=CAUSES["gov"], marks=tuple(CAUSES["marks"])))
    if view == "blocks":
        out.update(blocks=dict(low=tuple(BLOCKS["low"]), up=tuple(BLOCKS["up"]), wall=BLOCKS["wall"]))
    if view == "stop":
        out.update(stop=dict(head=tuple(STOP["head"]), cards=tuple(STOP["cards"]), marks=tuple(STOP["marks"])))
    if view == "open":
        out.update(open=dict(OPEN))
    return out
