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
from mech21 import _P, _arrow, _check, _on, _qmark, _xmark

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
    # 柱（上と下）＋柱の頭の板の芯（押し抜きで柱に残る部分＝動かない）
    g.append(F.rect(cx - cw / 2, SLC["up"], cw, SLC["top"] - SLC["up"], J.BG2, J.LINE, 4))
    g.append(F.rect(cx - cw / 2, SLC["top"] + SLC["th"], cw, SLC["low"] - SLC["top"] - SLC["th"], J.BG2, J.LINE, 4))
    th = SLC["th"]
    plug = [(cx - cw / 2 - th - 2, SLC["top"]), (cx + cw / 2 + th + 2, SLC["top"]), (cx + cw / 2 + 2, SLC["top"] + th), (cx - cw / 2 - 2, SLC["top"] + th)]
    g.append(F.poly(plug, J.BG2, None, close=True))
    if st0["fl"] != "none":
        n = int(st0["fl"])
        g.append(_tline(SLC["x0"] + 10, SLC["top"] - 18, f"{n}階の床", 28, INK, "start", 300))
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
    return ps


def tower_stage(prev, st):
    if st.get("set") == "three":
        return tower3_stage(prev, st)
    s = []
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


def cards_base(st0):
    t, r = CARDS["head"]
    return [_tline(CD["x0"], 380.0, t, 34, rc(r), "start", 800), F.line(CD["x0"], 400.0, CD["x1"], 400.0, rc(r), 3)]


def _cd_row(i):
    t, v = CARDS["rows"][i]
    y = CD["ys"][i]
    return (F.rect(CD["x0"], y - CD["h"] / 2, CD["x1"] - CD["x0"], CD["h"], J.BG2, J.LINE_DIM, 3, rx=10)
            + _tline(CD["x0"] + 30, y + 12, t, 36, INK, "start", 640)
            + _tline(CD["x1"] - 30, y + 16, v, 46, J.AMBER, "end", 400, fam="Dela"))


def cards_stage(prev, st):
    return [_cd_row(i) for i in range(3) if _on(prev, st, f"r{i}")]


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
#  見え方の表
# ══════════════════════════════════════════════════════════
def _lab_plan(st0):
    if st0["floor"] == "area":
        return "上から見た床（全部の階を足した広さ）"
    if st0["floor"] == "ct":
        return "上から見た屋上（冷却塔の置き場）"
    return "上から見た" + PL_FLOOR.get(st0["floor"], "5階の床") if st0["floor"] != "grid" else "上から見た5階の柱の並び（一部）"


def _lab_tower(st0):
    return "斜めから見た屋上の3基の冷却塔" if st0["set"] == "three" else "斜めから見た冷却塔"


def _lab_crack(st0):
    return "横から見た屋上の床（寄り）" if st0["fl"] == "roof" else "横から見た5階の床（寄り）"


def _lab_cal(st0):
    return "暦（1995年6月〜7月）" if st0["set"] == "rescue" else "暦（1989年7月〜12月）"


def _lab_load(st0):
    return "柱が支える重さ" if st0["set"] == "col" else "横から見た屋上と5階の重さ"


def _lab_vs(st0):
    return "記録ごとの数の比べ" if st0["set"] == "count" else "よく語られる話と記録"


def _bldg_base2(st0):
    return bldg_base(st0) + bldg_extra_base(st0)


def _bldg_stage2(prev, st):
    return bldg_stage(prev, st) + bldg_extra_stage(prev, st)


def _bldg_parts2(st):
    return bldg_parts(st) + bldg_extra_parts(st)


def _plan_stage2(prev, st):
    return plan_stage(prev, st) + plan_extra_stage(prev, st)


def _plan_parts2(st):
    return plan_parts(st) + plan_extra_parts(st)


def _slab_stage2(prev, st):
    return slab_stage(prev, st) + slab_extra_stage(prev, st)


def _slab_parts2(st):
    return slab_parts(st) + slab_extra_parts(st)


def _lab_slab(st0):
    return "横から見た床（断面）" if st0["z"] == "span" else "横から見た柱のまわりの床（断面）"


VIEWS = dict(
    section=dict(lab="横から見た建物（断面）", fields=dict(a=ONOFF, b=ONOFF, under=ONOFF, look=ONOFF, keep=ONOFF, fall=("none", "top", "all"), load=ONOFF),
                 base=section_base, stage=section_stage, parts=sc_parts),
    bldg=dict(lab="斜めから見た建物", fields=dict(hi=tuple(HI), cell=ONOFF, bulge=ONOFF, roof=ONOFF, closed=ONOFF, open=ONOFF, spk=ONOFF, exit=ONOFF,
                                              x=ONOFF, use5=("off", "permit", "both"), q5=ONOFF, chk=ONOFF, weak=ONOFF, qroof=ONOFF, under=ONOFF),
              base=_bldg_base2, stage=_bldg_stage2, parts=_bldg_parts2),
    plan=dict(lab=_lab_plan, fields=dict(floor=tuple(PL_FLOOR) + ("grid", "area", "ct"), scale=ONOFF, sag=ONOFF, north=ONOFF, crack=ONOFF, start=ONOFF,
                                         sink=ONOFF, goods=("off", "on", "fixed"), chk=ONOFF, nums=ONOFF, hit=ONOFF, walls=ONOFF, rubble=ONOFF,
                                         aplan=ONOFF, add=ONOFF, dp=("off", "thin", "miss"), miss_lit=ONOFF, ct=("off", "back", "moved")),
              base=plan_base, stage=_plan_stage2, parts=_plan_parts2),
    slab=dict(lab=_lab_slab, fields=dict(z=("span", "col"), fl=("none", "5", "4", "roof"), sag=ONOFF, same=ONOFF, beam=("off", "plan"), night=ONOFF,
                                         crack=ONOFF, sink=ONOFF, punch=ONOFF, bar=("off", "ok", "sunk"), box=ONOFF),
              base=slab_base, stage=_slab_stage2, parts=_slab_parts2),
    tower=dict(lab=_lab_tower, fields=dict(set=("one", "three"), run=ONOFF, drain=ONOFF, load=ONOFF, roof=ONOFF), base=tower_base, stage=tower_stage,
               parts=tower_parts),
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
    cards=dict(lab="記録の数（ソウル市の報告）", fields=dict(r0=ONOFF, r1=ONOFF, r2=ONOFF), base=cards_base, stage=cards_stage),
    nums=dict(lab="持ち物を返すセンターの数", fields=dict(place=ONOFF, n=ONOFF), base=nums_base, stage=nums_stage),
    redo=dict(lab="使い道が変わったときの手順", fields=dict(loop=ONOFF, x=ONOFF), base=redo_base, stage=redo_stage),
    sheets=dict(lab="継ぎ足された計算", fields=dict(add=ONOFF), base=sheets_base, stage=sheets_stage, parts=sheets_parts),
    rank=dict(lab="全国の百貨店の順位（店の形は順位だけ）", fields=dict(r0=ONOFF, r1=ONOFF), base=rank_base, stage=rank_stage),
    beam=dict(lab="斜めから見た柱と梁と床", fields=dict(r=ONOFF, l=ONOFF, lit=ONOFF, q=ONOFF), base=beam_base, stage=beam_stage),
    drop=dict(lab="横から見た柱の頭（断面）", fields=dict(dp=ONOFF, up=ONOFF), base=drop_base, stage=drop_stage),
    spans=dict(lab="横から見た床と柱（断面）", fields=dict(sag=ONOFF, joint=ONOFF), base=spans_base, stage=spans_stage, parts=spans_parts),
    colx=dict(lab="柱の断面の比べ（同じ縮尺）", fields=dict(both=ONOFF), base=colx_base, stage=colx_stage),
    load=dict(lab=_lab_load, fields=dict(set=("col", "sum"), cap=("same", "less"), brit=ONOFF, roofw=ONOFF, q5=ONOFF), base=load_base, stage=load_stage,
              parts=load_parts),
    hoop=dict(lab="斜めから見た柱の中の鉄筋", fields=dict(l=ONOFF, r=ONOFF, cut=ONOFF), base=hoop_base, stage=hoop_stage),
    persq=dict(lab="1平方メートルにかかる重さの目安", fields=dict(l=ONOFF, r=ONOFF), base=persq_base, stage=persq_stage),
    calc=dict(lab="構造の計算書の欄", fields=dict(miss=ONOFF, plan=ONOFF), base=calc_base, stage=calc_stage),
    vs=dict(lab=_lab_vs, fields=dict(set=tuple(VS_SET), c0=ONOFF, c1=ONOFF, lit=ONOFF), base=vs_base, stage=vs_stage),
    drag=dict(lab="横から見た屋上の床（断面）", fields=dict(split=ONOFF, pos=("start", "moved")), base=drag_base, stage=drag_stage, parts=drag_parts),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
HEAD_ONLY = dict(plan=("floor",), slab=("z", "fl"), clocks=("set",), bldg=("under",), tower=("set",), crack=("fl",), cal=("set",), load=("set",),
                 vs=("set",))
ORDER = dict(section=dict(fall=("none", "top", "all")), plan=dict(goods=("off", "on", "fixed"), dp=("off", "thin", "miss"), ct=("off", "back", "moved")),
             road=dict(amb=("off", "on", "blocked")), wall=dict(rubble=("on", "clear")), slab=dict(bar=("off", "ok", "sunk")),
             crack=dict(crack=("off", "on", "long")), load=dict(cap=("same", "less")), drag=dict(pos=("start", "moved")),
             bldg=dict(use5=("off", "permit", "both")))
NOT_SCHEMATIC = ("form", "cal", "cards", "vs")          # 原文の欄・記録の日付と数の写し（左上に「模式」を付けない）
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
              lowl=(272.0, 640.0, "start", 400.0)),     # 🔧 試し焼き（10-18）：「同じ板の上と下」を左下（y 830）に置くと板から遠かった   # ⚠️ geom_gap：br を x 1180 に置くと右の柱が字を覆った
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
)


def anchors(view, st):
    """札から線を引く先（画面の点）。"""
    if view == "section":
        return dict(a5=(SC["xb"][1] + 10, sc_top(5) + SC["fh"] / 2), roof=(SC["xb"][1] + 10, SC["roof"] - 10))
    if view == "bldg":
        p = bl_band("a", 5, *CELL["a5"])
        return dict(cell=(p[1][0], (p[1][1] + p[2][1]) / 2), roof=(bl_x("a")[1], bl_y(BL_N)), x=(1380.0, 600.0))
    if view == "plan":
        x0, y0, x1, y1 = pl_rect("a")
        return dict(nw=(x0 + 10, y0 + 30), sw=(x1 - 10, y0 + 30), hit=grid_xy("5", "E"), sag=pl_pt(0.62, 0.55))
    if view == "slab" and st["z"] == "col":
        return dict(col=(SLC["cx"] + SLC["cw"] / 2 + SLC["th"], SLC["top"]))
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
    return out
