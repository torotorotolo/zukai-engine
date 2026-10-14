# -*- coding: utf-8 -*-
"""mech22.py — 22本目（タイタン号のリメイク）「模式図」（2026-10-14 新設・⑤b-3b）。

■ 何か
  21本目 `mech21` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。再現イラストではない＝「再現」の札は出さない。
  左上に見る向き・左下に「模式」と出典。🔴 人の顔・私人の名前は描かない（社員の数は顔の無い印）。🔴 交信の文（付録A）は**打ち間違いのまま**・訳は字幕だけ。
  🔴 **色は役の色**（`jiko_style.ROLE`＝米沿岸警備隊 USCG 青・米運輸安全委員会 OK 緑・カナダ INST 紫・会社 COMPANY 橙・母船 SHIP 水色・潜水艇 SUB 白）。
     赤＝壊れた・不具合／黄＝数（据え置き）。門番 check_mech の judge_m22 が記録の表（REC_M22）で値・数・色を照らす（§5b-88）

■ 見え方（view）＝台本 第2版 §4 の画の欄（第1〜3章）と映像方針の一覧（了承②）
  fuji    … 深さの物差し・逆さの富士山（3,776m）とタイタニックの深さ（約3,800m）・水の重さの矢印・1円玉と乗用車（約1.2トン）     c202
  reports … 3つの報告書の表紙（題と年月だけ＝米沿岸警備隊 2025年8月・米運輸安全委員会 2025年10月・カナダ 2026年6月）          c203
  side    … 横から見たタイタン（NTSB 図3 の比＝`titan_fig.TT_*`・機首が左）・全長の寸法・5人まで・耐圧殻（筒とドーム）・前のドームのボルト18本
                                                                                       c205・c206・c311
  org     … 2023年の上級の8つの職の席（埋まった席＝会社の橙・空いた席＝灰の点線）・CEO の席・社員の印15（数は黄）・「実験的」     c207・c208
  paper   … 書類の要点（同意書＝英字の句2つと「死」の数え／計画書の一節＝英字の句・呼び名・米沿岸警備隊の見立て）              c209・c211
  table   … カナダの報告書 付録B の表（27行・欄は英字のまま）・年のまとまり・「27回」                                       c212
  dives   … 付録B の潜航を1回1点で年ごとに並べた点（届いた13回＝潜水艇の白）・不具合の赤の輪と札                     c213〜c216
  lars_top… 上から見た台と艇（NTSB 図4 の上の線画をなぞる・機首は左）・前のドームを閉めてボルトで締める                         c310
  lars_side… 横から見た台が沈む3段（水を入れる→台ごと水面の下→艇を切り離す）                                               c314
  sink    … 重りで沈む潜水艇（下向きの矢印だけ）・この年の初めて                                                           c315
  drop    … 重りの仕組み（降りる→重りを落として緩める→浮く・重りの数と場所は描かない）                                     c409
  sonar   … 母船の下の送受信機と艇のあいだの音の波・電波は水を通りにくい・声の装置は無い                                     c316
  comms   … 2つの通信の箱（1つ目＝文字を送る・動く／2つ目＝予備の通信と追跡・動いていない）                                  c318
  chat    … 付録A の文の吹き出し（潜水艇＝左の白・母船＝右の水色・打ち間違いのまま）・米沿岸警備隊の青の札                 c317・c401・c406・c408
  depth   … 深さの線（記録の点だけ＝あいだは直線＝模式）・返事の無い間・海の底・止まった点・寄り                       c319・c402・c418・c419
  bow     … 上から見たタイタニックの船首と、潜水艇の知らせ（東南東）・母船の画面（東北東）・跳ぶ位置                          c403・c404
  two     … 2段の札（上＝米国の2つの調べ／下＝カナダの調べ）                                                               c410

■ SPEC の書き方（mech21 と同じ）
  fig=("m22", dict(view=…, start=dict(…), steps=[dict(state=dict(…), tag=dict(t=…, at=…, to=…, d=…)), …],
                   rel=[dict(t="6.7", src="NTSB p1010")], note="…模式…", src=ss.src([…])))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。札の数・時刻は `rel=` に同じ文字列（門番 check_mech の judge_m22）。
  🔴 記録の値（深さ・時刻・表の行・職の席・ボルトの数・方角）は門番 check_mech の REC_M22 が別に持つ（§5b-88）。描く側の表（APPA・APPB・ORG・
     DEPTH・FUJI_M ほか）を書き換えると鳴る。⚠️ 動く部品は段の層（札）より上に描かれる＝札は動く部品の通り道に置かない
"""
from __future__ import annotations

import math

import jiko_style as J
import titan_fig as F
from mech21 import _P, _arrow, _box, _check, _on, _xmark

ONOFF = ("off", "on")
INK = J.INK_W
L_X = F.BX0 + 40.0
SUBC, SHIPC, COC, USC, NTC, TSC = J.SUB, J.SHIP, J.COMPANY, J.USCG, J.OK, J.INST
SEA_LN = "#2a4a5e"                        # 海面・海の底の線（面に使わない・紺の7色と別の値＝章の色に染まらない）


def _tline(x, y, t, cap=30, col=None, anchor="start", mw=600, fam="Noto"):
    return F.txtfit(x, y, t, mw, cap=cap, col=col or INK, anchor=anchor, fam=fam)


# ══════════════════════════════════════════════════════════
#  横から見たタイタン（NTSB 図3 の比＝titan_fig の TT_*・機首が左）
# ══════════════════════════════════════════════════════════
def titan_geo(cx, cy, L):
    """タイタンの横の形の要所（画素）。全長 L＝のぞき窓の外面〜尾部の先。"""
    R = L * F.TT_R
    dm = R * F.TT_DOME
    x0 = cx - L / 2
    xc0 = x0 + L * F.TT_NOSE + dm
    xc1 = xc0 + L * F.TT_CYL
    return dict(L=L, R=R, dm=dm, x0=x0, xc0=xc0, xc1=xc1, xh0=xc0 - dm, xh1=xc1 + dm, xt=x0 + L, cx=cx, cy=cy)


def titan_svg(G, col=None, hull=None, dim=False, frame=True, win=True):
    """横から見たタイタンの線画。hull＝耐圧殻（筒と両端のドーム）を塗る色（None＝塗らない）。"""
    c = J.LINE_DIM if dim else (col or SUBC)
    L, R, dm, cy = G["L"], G["R"], G["dm"], G["cy"]
    xc0, xc1, xt = G["xc0"], G["xc1"], G["xt"]
    g = [f'<path d="M{xc1:.1f} {cy - R:.1f} L{xt:.1f} {cy - R * 0.96:.1f} C{xt - L * 0.11:.1f} {cy + R * 0.12:.1f} '
         f'{xc1 + L * 0.16:.1f} {cy + R:.1f} {xc1 + L * 0.02:.1f} {cy + R:.1f}" fill="{J.BG2}" stroke="{J.LINE_DIM if dim else J.LINE}" '
         f'stroke-width="4" stroke-linejoin="round"/>']
    body = (f'M{xc0:.1f} {cy - R:.1f} H{xc1:.1f} A{dm:.1f} {R:.1f} 0 0 1 {xc1:.1f} {cy + R:.1f} '
            f'H{xc0:.1f} A{dm:.1f} {R:.1f} 0 0 1 {xc0:.1f} {cy - R:.1f} Z')
    g.append(f'<path d="{body}" fill="{hull or J.BG2}"{" fill-opacity=\"0.30\"" if hull else ""} stroke="{c}" stroke-width="5"/>')
    for x in (xc0, xc1):
        g.append(F.rect(x - L * 0.010, cy - R * 1.04, L * 0.020, R * 2.08, J.BG2, c, 3))
    g.append(F.rect(xc0 + L * F.TT_CYL * 0.62 - L * 0.016, cy - R - L * 0.030, L * 0.032, L * 0.030, J.BG2, J.LINE, 3))
    g.append(F.rect(G["xh1"] - L * 0.004, cy - L * 0.016, L * 0.030, L * 0.032, J.BG2, J.LINE, 3))
    if frame:
        fy = cy + R + L * 0.055
        for px_ in (xc0, xc1):
            g.append(F.rect(px_ - L * 0.006, cy + R, L * 0.012, fy - cy - R, J.LINE_DIM))
        g.append(F.rect(xc0 - L * 0.05, fy, (xc1 - xc0) + L * 0.10, L * 0.014, J.LINE_DIM))
    if win:
        g.append(F.circ(G["x0"] + L * 0.026, cy, R * 0.20, J.BG, c, 4))
    return "".join(g)


def titan_poly(G):
    """動く部品の外形＝(耐圧殻〈筒と両端のドーム〉, 尾部)の2つの多角形（lars_side）。
    🔧 ⑤b-3b の試し焼き：1つの多角形で尾部の下の縁を直線にしたら靴の形に見えた＝線画（titan_svg）と同じ曲線を点で取る"""
    L, R, dm, cy = G["L"], G["R"], G["dm"], G["cy"]
    xc0, xc1, xt = G["xc0"], G["xc1"], G["xt"]
    fore = [(xc0 - dm * math.sin(math.pi * k / 16), cy - R * math.cos(math.pi * k / 16)) for k in range(17)]     # 上→前→下
    aft = [(xc1 + dm * math.sin(math.pi * k / 16), cy + R * math.cos(math.pi * k / 16)) for k in range(17)]      # 下→後ろ→上
    hull = fore + aft
    p0, c1, c2, p3 = (xt, cy - R * 0.96), (xt - L * 0.11, cy + R * 0.12), (xc1 + L * 0.16, cy + R), (xc1 + L * 0.02, cy + R)
    bez = [tuple((1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * b + 3 * (1 - u) * u ** 2 * c + u ** 3 * d for a, b, c, d in zip(p0, c1, c2, p3))
           for u in [k / 12 for k in range(13)]]
    tail = [(xc1, cy - R)] + bez
    return hull, tail


# ══════════════════════════════════════════════════════════
#  fuji（c202）＝深さの物差し（海面 0m〜4,000m）・逆さの富士山・タイタニックの深さ・水の重さ・1円玉と乗用車
# ══════════════════════════════════════════════════════════
FJ = dict(x=300.0, y0=330.0, y1=830.0, mx=4000.0, fx=640.0, fw=640.0, wx=1060.0, coin=(1320.0, 470.0), car=(1600.0, 470.0))
FUJI_M = 3776.0                   # 富士山の高さ（国土地理院）
TITANIC_M = 3800.0                # タイタニックの深さ（TSB §1.3「approximately 3800 m」）
FJ_TICKS = (0, 1000, 2000, 3000, 4000)


def fj_y(m):
    return FJ["y0"] + (FJ["y1"] - FJ["y0"]) * m / FJ["mx"]


def fuji_base(st0):
    g = [F.line(FJ["x"] - 20, FJ["y0"], F.BX1 - 40, FJ["y0"], SEA_LN, 4),
         _tline(F.BX1 - 40, FJ["y0"] - 14, "海面", 28, J.TICK, "end", 200),
         F.line(FJ["x"], FJ["y0"], FJ["x"], FJ["y1"], J.LINE, 4)]
    for m in FJ_TICKS:
        y = fj_y(m)
        g.append(F.line(FJ["x"] - 14, y, FJ["x"], y, J.LINE, 4))
        g.append(_tline(FJ["x"] - 24, y + 10, f"{m:,}", 28, J.TICK, "end", 160))
    # ⚠️ 門番 layout：物差しの名を下（y 878）に置くと左下の注の行に重なった＝上へ
    g.append(_tline(FJ["x"] - 20, FJ["y0"] - 30, "深さ（メートル）", 24, J.TICK, "end", 200))
    # 逆さの富士山（底辺＝海面・頂＝3,776m）
    fx, fw, fy = FJ["fx"], FJ["fw"], fj_y(FUJI_M)
    g.append(F.poly([(fx - fw / 2, FJ["y0"]), (fx + fw / 2, FJ["y0"]), (fx + fw * 0.09, fy - 30), (fx, fy), (fx - fw * 0.09, fy - 30)],
                    J.BG2, J.LINE, 4, close=True))
    g.append(_tline(fx, FJ["y0"] + 150, "富士山（逆さ）", 34, INK, "middle", 400))
    g.append(_tline(fx, FJ["y0"] + 196, "3,776メートル", 34, J.AMBER, "middle", 400, "Dela"))
    # タイタニックの深さ（線と船の印）
    ty = fj_y(TITANIC_M)
    g.append(F.line(FJ["x"], ty, F.BX1 - 40, ty, SEA_LN, 4, dash="14 10"))
    g.append(F.poly([(FJ["wx"] - 110, ty - 6), (FJ["wx"] + 110, ty - 6), (FJ["wx"] + 80, ty - 40), (FJ["wx"] - 90, ty - 40)], J.BG2, J.LINE, 4,
                    close=True))
    g.append(_tline(FJ["wx"] + 150, ty - 52, "タイタニック", 32, INK, "start", 300))
    g.append(_tline(FJ["wx"] + 150, ty - 12, "約3,800メートル", 32, J.AMBER, "start", 330, "Dela"))
    return g


def fuji_stage(prev, st):
    s = []
    if _on(prev, st, "press"):
        for i in range(5):
            x = FJ["wx"] - 140 + i * 70
            s.append(_arrow(x, FJ["y0"] + 40, x, fj_y(TITANIC_M) - 70, J.LINE, 4, 18))
        s.append(_tline(FJ["wx"] + 170, FJ["y0"] + 60, "水の重さ", 32, INK, "start", 300))   # ⚠️ geom_gap：矢印の上に置くと線が字を貫いた
    if _on(prev, st, "coin"):
        (cx, cy), (kx, ky) = FJ["coin"], FJ["car"]
        s.append(F.circ(cx, cy, 34, J.BG2, J.LINE, 4))
        s.append(_tline(cx, cy + 82, "1円玉の広さ", 30, INK, "middle", 260))
        s.append(F.rect(kx - 110, ky - 46, 220, 70, J.BG2, J.LINE, 4, rx=18))
        s.append(F.rect(kx - 60, ky - 86, 120, 44, J.BG2, J.LINE, 4, rx=12))
        for wx in (kx - 62, kx + 62):
            s.append(F.circ(wx, ky + 28, 20, J.BG, J.LINE, 4))
        s.append(_tline(kx, ky + 100, "乗用車1台ぶん", 30, INK, "middle", 300))
        s.append(_arrow(kx - 120, ky - 10, cx + 48, cy - 10, J.AMBER, 5, 20))
    return s


# ══════════════════════════════════════════════════════════
#  reports（c203）＝3つの報告書の表紙（題と年月だけ）
# ══════════════════════════════════════════════════════════
RP = dict(xs=(420.0, 960.0, 1500.0), y=560.0, w=400.0, h=470.0)
RP_T = (("米沿岸警備隊", "海難調査委員会の報告書", "2025年8月", "uscg"),
        ("米国の運輸安全委員会", "調査の報告書", "2025年10月", "ntsb"),
        ("カナダの運輸安全委員会", "調査の報告書", "2026年6月", "tsb"))


def reports_base(st0):
    # ⚠️ 門番 layout：暗い字の上に明るい字を描き直すと「重なり」＝題と年月は基図に1回だけ（明るくする段は枠と帯と名だけ）
    g = []
    for i, (who, ttl, ym, _) in enumerate(RP_T):
        x, y, w, h = RP["xs"][i], RP["y"], RP["w"], RP["h"]
        g.append(F.rect(x - w / 2, y - h / 2, w, h, J.BG2, J.LINE_DIM, 4, rx=8))
        g.append(_tline(x, y - h / 2 + 150, ttl, 32, INK, "middle", w - 50))
        # ⚠️ 門番 box：題と年月のあいだが空き矩形 33%＝表紙の本文の行（灰の線・模式）を3本
        for k in range(3):
            yy = y - h / 2 + 200 + k * 34
            g.append(F.line(x - w / 2 + 50, yy, x + w / 2 - 50 - (k % 2) * 70, yy, J.LINE_DIM, 6))
        g.append(_tline(x, y + 120, ym, 44, J.AMBER, "middle", w - 50, "Dela"))
    return g


def _rp_lit(i):
    who, ttl, ym, role = RP_T[i]
    x, y, w, h = RP["xs"][i], RP["y"], RP["w"], RP["h"]
    c = J.ROLE[role]
    return "".join([F.rect(x - w / 2, y - h / 2, w, h, "none", c, 6, rx=8), F.rect(x - w / 2, y - h / 2, w, 96, c, op=0.9),
                    _tline(x, y - h / 2 + 62, who, 34, J.BG, "middle", w - 40)])


def reports_stage(prev, st):
    return [_rp_lit(i) for i in range(3) if _on(prev, st, f"r{i + 1}")]


# ══════════════════════════════════════════════════════════
#  side（c205・c206・c311）＝横から見たタイタン
# ══════════════════════════════════════════════════════════
SD = dict(cx=930.0, cy=520.0, L=1260.0)
SD_LEN_M = 6.7                    # 全長（NTSB p.10「22-foot-long」＝6.7m）
SD_SEATS = 5                      # 乗れる人の数（TSB §1.2.1「up to 5 people」）
SD_BOLTS = 18                     # 前のドームを留めるボルト（TSB 脚注39「OceanGate began using 18 securing bolts」）


def sd_geo():
    return titan_geo(SD["cx"], SD["cy"], SD["L"])


def _bolts(G, n):
    """前のドームの縁（前のリング）のボルト＝横から見て縦1列。"""
    R, cy, x = G["R"], G["cy"], G["xc0"]
    r_b = max(3.0, min(7.0, R * 1.84 / n * 0.42))
    out = []
    for i in range(n):
        a = math.pi * (i / (n - 1.0)) - math.pi / 2
        out.append((x - 2 + math.cos(a) * 4, cy + math.sin(a) * R * 0.92, r_b))
    return out


def side_base(st0):
    return [titan_svg(sd_geo())]


def side_stage(prev, st):
    G = sd_geo()
    s = []
    if _on(prev, st, "dim"):
        y = G["cy"] + G["R"] + G["L"] * 0.055 + 80
        s.append(F.line(G["x0"], y - 22, G["x0"], y + 22, J.AMBER, 4) + F.line(G["xt"], y - 22, G["xt"], y + 22, J.AMBER, 4))
        s.append(_arrow(G["cx"] - 140, y, G["x0"] + 4, y, J.AMBER, 4, 18) + _arrow(G["cx"] + 140, y, G["xt"] - 4, y, J.AMBER, 4, 18))
        s.append(_tline(G["cx"], y + 14, "全長6.7メートル", 40, J.AMBER, "middle", 270, "Dela"))
    if _on(prev, st, "hull"):
        L, R, dm, cy = G["L"], G["R"], G["dm"], G["cy"]
        body = (f'M{G["xc0"]:.1f} {cy - R:.1f} H{G["xc1"]:.1f} A{dm:.1f} {R:.1f} 0 0 1 {G["xc1"]:.1f} {cy + R:.1f} '
                f'H{G["xc0"]:.1f} A{dm:.1f} {R:.1f} 0 0 1 {G["xc0"]:.1f} {cy - R:.1f} Z')
        s.append(f'<path d="{body}" fill="{SUBC}" fill-opacity="0.22" stroke="{SUBC}" stroke-width="9"/>')
    if _on(prev, st, "mat"):
        cy, R = G["cy"], G["R"]
        xm = (G["xc0"] + G["xc1"]) / 2
        s.append(F.line(xm, cy - R - 6, xm, cy - R - 70, J.LINE, 3) + _tline(xm, cy - R - 82, "炭素繊維の筒", 36, INK, "middle", 400))
        for x, anc in ((G["xh0"] + G["dm"] * 0.3, "end"), (G["xh1"] - G["dm"] * 0.3, "start")):
            s.append(F.line(x, cy + R * 0.7, x, cy + R + 140, J.LINE, 3))
        s.append(_tline(G["xh0"] + G["dm"] * 0.3, cy + R + 180, "チタンのドーム", 34, INK, "middle", 320))
        s.append(_tline(G["xh1"] - G["dm"] * 0.3, cy + R + 180, "チタンのドーム", 34, INK, "middle", 320))
    if _on(prev, st, "bolts"):
        for (x, y, r) in _bolts(G, SD_BOLTS):
            s.append(F.circ(x, y, r, J.AMBER))
    if _on(prev, st, "only"):
        x, cy = G["xh0"], G["cy"]
        s.append(_arrow(x - 230, cy, x - 24, cy, COC, 7, 26) + _arrow(x - 40, cy + 34, x - 230, cy + 34, COC, 7, 26))
    return s


# ══════════════════════════════════════════════════════════
#  org（c207・c208）＝2023年の上級の8つの職の席（TSB 表4）＋社員の印15
# ══════════════════════════════════════════════════════════
ORG = (("CEO", "filled"), ("最高執行責任者", "filled"), ("技術部長", "vacant"), ("広報部長", "filled"), ("運航の管理者", "filled"),
       ("物流と品質保証の部長", "filled"), ("遠征の管理者", "filled"), ("総務部長", "filled"))
ORG_XY = [(960.0, 330.0)] + [(330.0 + 420.0 * i, 480.0) for i in range(4)] + [(540.0 + 420.0 * i, 610.0) for i in range(3)]
ORG_W, ORG_H = 380.0, 86.0
ORG_STAFF = 15                    # 2023年の季節の初めの社員（TSB §1.23「15 employees」）
ORG_PY = 760.0


def _seat(i, lit, ceo=False):
    """席の枠（lit＝明るくする段は枠だけ＝字は基図に1回＝門番 layout の重なり）。lit=None＝基図（暗い枠と字）"""
    nm, stt = ORG[i]
    x, y = ORG_XY[i]
    if stt == "vacant":
        fr = F.rect(x - ORG_W / 2, y - ORG_H / 2, ORG_W, ORG_H, "none" if lit else J.BG, J.TICK if lit else J.LINE_DIM, 4, rx=10, dash="12 9")
        return fr if lit else (fr + _tline(x, y - 4, nm, 30, J.TICK, "middle", ORG_W - 30) + _tline(x, y + 30, "（空席）", 24, J.TICK, "middle", 200))
    if lit:
        return F.rect(x - ORG_W / 2, y - ORG_H / 2, ORG_W, ORG_H, "none", COC, 9 if ceo else 5, rx=10)
    return (F.rect(x - ORG_W / 2, y - ORG_H / 2, ORG_W, ORG_H, J.BG2, J.LINE_DIM, 4, rx=10)
            + _tline(x, y + 11, nm, 34 if i == 0 else 32, INK, "middle", ORG_W - 30))


def _org_tree(col, sw):
    """席をつなぐ線（CEO→1段目・真ん中の縦の線→2段目）。真ん中の縦の線 x 960 は1段目の席のすき間（x 940〜980）を通る"""
    x0, y0 = ORG_XY[0]
    g = [F.line(x0, y0 + ORG_H / 2, x0, 410, col, sw), F.line(ORG_XY[1][0], 410, ORG_XY[4][0], 410, col, sw)]
    for i in range(1, 5):
        g.append(F.line(ORG_XY[i][0], 410, ORG_XY[i][0], ORG_XY[i][1] - ORG_H / 2, col, sw))
    g += [F.line(ORG_XY[5][0], 545, ORG_XY[7][0], 545, col, sw), F.line(x0, 410, x0, 545, col, sw)]
    for i in range(5, 8):
        g.append(F.line(ORG_XY[i][0], 545, ORG_XY[i][0], ORG_XY[i][1] - ORG_H / 2, col, sw))
    return g


def org_base(st0):
    g = _org_tree(J.LINE_DIM, 3)
    g += [_seat(i, False) for i in range(len(ORG))]
    return g


def _person(cx, top, h, col):
    r = h * 0.17
    return (F.circ(cx, top + r, r, col) + F.poly([(cx - h * 0.25, top + h), (cx - h * 0.25, top + h * 0.52), (cx - h * 0.12, top + h * 0.40),
                                                  (cx + h * 0.12, top + h * 0.40), (cx + h * 0.25, top + h * 0.52), (cx + h * 0.25, top + h)],
                                                 col, None, close=True))


def org_stage(prev, st):
    s = []
    if _on(prev, st, "seats"):
        s += [_seat(i, True) for i in range(len(ORG))]
    if _on(prev, st, "ceo"):
        s.append(_seat(0, True, ceo=True))
    if _on(prev, st, "all"):
        # ⚠️ geom_gap：CEO から斜めの線を引くと1段目の席の字を貫いた＝席をつなぐ線（基図の木の形）を会社の色で太く
        s += _org_tree(COC, 5)
    if _on(prev, st, "staff"):
        for i in range(ORG_STAFF):
            s.append(_person(400.0 + i * 74.0, ORG_PY, 64.0, J.AMBER))
        s.append(_tline(400.0 + ORG_STAFF * 74.0 + 10, ORG_PY + 52, "社員", 32, INK, "start", 200))
    return s


# ══════════════════════════════════════════════════════════
#  paper（c209・c211）＝書類の要点（英字の句はそのまま・訳は字幕）
# ══════════════════════════════════════════════════════════
PP = dict(x0=250.0, x1=1180.0, y0=290.0, y1=850.0)
PP_DOC = dict(
    waiver=dict(head="参加の同意書（要点）", lines=("experimental submersible vessel", "not been certified by any regulatory body")),
    plan=dict(head="2023年の計画書（一節）", lines=("guests who help fund OceanGate expeditions",)))
PP_DEATH = 9                      # 同意書の「death」（USCG p71「The liability waiver mentions death 9 times」）


def _pp_line_y(i):
    return PP["y0"] + 230 + i * 150


def paper_base(st0):
    d = PP_DOC[st0["doc"]]
    g = [F.rect(PP["x0"], PP["y0"], PP["x1"] - PP["x0"], PP["y1"] - PP["y0"], J.BG2, J.LINE, 4, rx=6),
         _tline(PP["x0"] + 40, PP["y0"] + 66, d["head"], 38, INK, "start", 820)]
    for k in range(9):
        y = PP["y0"] + 130 + k * 72
        if any(abs(y - _pp_line_y(i) + 10) < 40 for i in range(len(d["lines"]))):
            continue
        g.append(F.line(PP["x0"] + 40, y, PP["x1"] - 40 - (k % 3) * 90, y, J.LINE_DIM, 6))
    for i, t in enumerate(d["lines"]):
        g.append(_tline(PP["x0"] + 40, _pp_line_y(i), t, 34, INK, "start", PP["x1"] - PP["x0"] - 80))
    return g


def paper_stage(prev, st):
    d = PP_DOC[st["doc"]]
    s = []
    for i, t in enumerate(d["lines"]):
        if _on(prev, st, f"hl{i + 1}"):
            # ⚠️ 門番 layout：字を描き直さない＝句の下に黄の線を引くだけ
            y = _pp_line_y(i)
            w = min(F.fm.width(t, 34), PP["x1"] - PP["x0"] - 80)
            s.append(F.rect(PP["x0"] + 36, y + 12, w + 8, 8, J.AMBER, rx=3))
    if _on(prev, st, "n9"):
        x0, y0 = 1320.0, 420.0
        s.append(_tline(x0, y0, "「death」の数", 34, INK, "start", 460))
        for k in range(PP_DEATH):
            x = x0 + 20 + (k % 5) * 80
            y = y0 + 70 + (k // 5) * 100
            s.append(F.rect(x, y, 56, 76, "none", J.AMBER, 4, rx=6) + F.line(x + 12, y + 24, x + 44, y + 24, J.AMBER, 4)
                     + F.line(x + 12, y + 44, x + 44, y + 44, J.AMBER, 4))
    if _on(prev, st, "name"):
        s.append(_box(1510.0, 470.0, 560.0, 100.0, "ミッション・スペシャリスト", COC, cap=34))
        s.append(_arrow(1230.0, 470.0, 1196.0, 470.0, COC, 5, 18))
    if _on(prev, st, "uscg"):
        s.append(_box(1510.0, 680.0, 560.0, 130.0, "料金を払う乗客を", USC, cap=34, t2="隠す呼び方"))
        s.append(_tline(1510.0, 780.0, "米沿岸警備隊の見立て", 28, USC, "middle", 520))
    return s


# ══════════════════════════════════════════════════════════
#  table（c212）＝カナダの報告書 付録B の表（27行・欄は英字のまま）
# ══════════════════════════════════════════════════════════
#   原文 TSB 付録B 表B1（Date／Depth reached (m)／Dive time (h)／People on board／Support vessel／Goal of dive／Notes）
APPB = (
    ("2021-06-30", "7", "2.6", "5", "Horizon Arctic", "Test", "Forward dome fell off the submersible during recovery"),
    ("2021-07-03", "1700", "5.8", "4", "Horizon Arctic", "Test", "Starboard thrusters failed"),
    ("2021-07-09", "3840", "16", "3", "Horizon Arctic", "Test", "Incident with drop weight"),
    ("2021-07-13", "89", "4.9", "5", "Horizon Arctic", "Test", ""),
    ("2021-07-19", "3500", "11.3", "5", "Horizon Arctic", "Titanic", "Incident with drop weight"),
    ("2021-07-24", "3840", "10.7", "5", "Horizon Arctic", "Titanic", "Incident with drop weight"),
    ("2021-07-27", "3840", "9.5", "5", "Horizon Arctic", "Titanic", "Titan too light, had to thrust to bottom and then starboard battery failed"),
    ("2021-07-28", "3840", "11.1", "5", "Horizon Arctic", "Titanic", ""),
    ("2021-08-04", "3840", "10.7", "5", "Horizon Arctic", "Titanic", ""),
    ("2021-08-05", "3840", "10.8", "5", "Horizon Arctic", "Titanic", ""),
    ("2022-06-16", "7", "3.5", "5", "Horizon Arctic", "Test", ""),
    ("2022-06-18", "1380", "6.3", "5", "Horizon Arctic", "Titanic", ""),
    ("2022-06-20", "3840", "27", "5", "Horizon Arctic", "Titanic", "Batteries died on approach to LARS"),
    ("2022-07-01", "25", "5", "4", "Horizon Arctic", "Test", ""),
    ("2022-07-03", "3840", "13", "5", "Horizon Arctic", "Titanic",
     "Battery and control problems; Titan collided with the port bow of the Titanic and was disabled on recovery"),
    ("2022-07-06", "3840", "12", "5", "Horizon Arctic", "Titanic", ""),
    ("2022-07-08", "30", "4.2", "5", "Horizon Arctic", "Test", ""),
    ("2022-07-11", "10", "3.5", "5", "Horizon Arctic", "Cameron Canyon", ""),
    ("2022-07-14", "3840", "11.9", "5", "Horizon Arctic", "Titanic", "Issues with tracking and communications"),
    ("2022-07-15", "3840", "10.9", "5", "Horizon Arctic", "Titanic",
     "Power failure on the bottom. There was also a loud bang heard by those inside the submersible on surfacing"),
    ("2022-07-19", "3840", "12.75", "5", "Horizon Arctic", "Titanic", "Thruster control mapping failure, electrical problems"),
    ("2022-07-22", "3840", "11.1", "5", "Horizon Arctic", "Titanic", "Port horizontal thruster flooded"),
    ("2022-07-23", "2954", "12.1", "5", "Horizon Arctic", "Hydrographic feature", ""),
    ("2023-05-31", "10", "2", "5", "Polar Prince", "Test", "Software and camera issues"),
    ("2023-06-05", "10", "2", "5", "Polar Prince", "Southeast of Cape Race", "Poor visibility on the surface"),
    ("2023-06-13", "10", "2", "5", "Polar Prince", "Northeast of the Gully", "Ballast system issue"),
    ("2023-06-18", "3346", "2.05", "5", "Polar Prince", "Titanic", "Occurrence dive"),
)
APPB_HEAD = ("Date", "Depth reached (m)", "Dive time (h)", "People on board", "Support vessel", "Goal of dive", "Notes")
# ⚠️ 門番 layout：左の年の札（x 116 の右寄せ）が枠の外へ出た・欄の名が隣の欄に重なった＝表を右へ寄せ、欄の名と備考は 12px まで縮めてよい
TB = dict(x0=210.0, y0=300.0, rh=19.6, cols=(210.0, 340.0, 455.0, 545.0, 635.0, 790.0, 980.0, 1810.0), cap=16)


def table_base(st0):
    g = []
    xs, y0, rh = TB["cols"], TB["y0"], TB["rh"]
    g.append(F.rect(xs[0] - 6, y0 - rh + 2, xs[-1] - xs[0] + 6, rh * (len(APPB) + 1) + 6, J.BG2, J.LINE_DIM, 2))
    for j, h in enumerate(APPB_HEAD):
        g.append(F.txtfit(xs[j], y0 - 2, h, xs[j + 1] - xs[j] - 10, cap=TB["cap"], col=INK, floor=11))
    for i, row in enumerate(APPB):
        y = y0 + rh * (i + 1)
        if i % 2 == 0:
            g.append(F.rect(xs[0] - 6, y - rh + 4, xs[-1] - xs[0] + 6, rh, J.GRID, op=0.6))
        for j, v in enumerate(row):
            g.append(F.txtfit(xs[j], y, v, xs[j + 1] - xs[j] - 10, cap=TB["cap"], col=J.TICK, floor=11))
    return g


def _yr_rows():
    out = {}
    for i, r in enumerate(APPB):
        out.setdefault(r[0][:4], []).append(i)
    return out


def table_stage(prev, st):
    s = []
    if _on(prev, st, "yr"):
        rh, y0 = TB["rh"], TB["y0"]
        for yr, idx in _yr_rows().items():
            ya, yb = y0 + rh * idx[0] + 2, y0 + rh * (idx[-1] + 1) + 2
            s.append(F.line(186, ya, 186, yb, J.AMBER, 5) + F.line(186, ya, 200, ya, J.AMBER, 5) + F.line(186, yb, 200, yb, J.AMBER, 5))
            s.append(_tline(176, (ya + yb) / 2 + 9, f"{yr}年", 22, J.AMBER, "end", 100))
    return s


# ══════════════════════════════════════════════════════════
#  dives（c213〜c216）＝付録B の潜航を1回1点で年ごとに並べる
# ══════════════════════════════════════════════════════════
DV = dict(x0=360.0, dx=104.0, ys=(390.0, 560.0, 730.0), r=26.0)
DV_DEEP = "3840"                  # タイタニックの深さまで届いた行の「Depth reached」の値（付録B）
DV_MARK = dict(dome=("Forward dome fell off",), batt=("Batteries died",), thr=("thruster",), wt=("drop weight",),
               com=("communications",))
DV_WORD = dict(dome="前のドーム", batt="電池", thr="推進器", wt="重り", com="通信")


def dv_pts():
    """(行の番号, 年, x, y)。年ごとに左から。"""
    out = []
    for k, (yr, idx) in enumerate(sorted(_yr_rows().items())):
        for j, i in enumerate(idx):
            out.append((i, yr, DV["x0"] + j * DV["dx"], DV["ys"][k]))
    return out


def dv_marked(kind):
    keys = DV_MARK[kind]
    return [i for i, r in enumerate(APPB) if any(k.lower() in r[6].lower() for k in keys)]


def dives_base(st0):
    g = []
    for k, yr in enumerate(sorted(_yr_rows())):
        g.append(_tline(F.BX0 + 70, DV["ys"][k] + 12, f"{yr}年", 34, J.TICK, "start", 200))
    for i, yr, x, y in dv_pts():
        g.append(F.circ(x, y, DV["r"], J.BG2, J.LINE_DIM, 4))
    return g


def dives_stage(prev, st):
    s = []
    pts = {i: (x, y) for i, _, x, y in dv_pts()}
    if _on(prev, st, "reach"):
        for i, r in enumerate(APPB):
            if r[1] == DV_DEEP:
                x, y = pts[i]
                s.append(F.circ(x, y, DV["r"], SUBC, SUBC, 4))
        # ⚠️ 門番 echo：「タイタニックの深さまで届いた」は語りの写し
        s.append(F.circ(1360.0, 862.0 - 30, 14, SUBC) + _tline(1384.0, 842.0, "沈んだ船の深さまで潜った回", 28, INK, "start", 420))
    for kind in DV_MARK:
        if _on(prev, st, kind):
            for i in dv_marked(kind):
                x, y = pts[i]
                s.append(F.circ(x, y, DV["r"] + 12, "none", J.ALERT, 6))
                s.append(_tline(x, y + DV["r"] + 44, DV_WORD[kind], 24, J.ALERT, "middle", DV["dx"] - 4))
    return s


# ══════════════════════════════════════════════════════════
#  lars_top（c310）＝上から見た台と艇（NTSB 図4 の上の線画をなぞる・機首は左）
# ══════════════════════════════════════════════════════════
LT = dict(x0=300.0, x1=1560.0, y0=360.0, y1=760.0, cx=930.0, cy=560.0, L=820.0)


def lars_top_base(st0):
    x0, x1, y0, y1 = LT["x0"], LT["x1"], LT["y0"], LT["y1"]
    cy = LT["cy"]
    g = [F.poly([(x0 + 150, y0), (x1, y0), (x1, cy - 24), (x1 - 120, cy - 24), (x1 - 120, cy + 24), (x1, cy + 24), (x1, y1),
                 (x0 + 150, y1), (x0, y1 - 150), (x0, cy + 18), (x0 + 40, cy + 18), (x0 + 40, cy - 18), (x0, cy - 18), (x0, y0 + 150)],
                J.BG2, COC, 4, close=True)]
    for tx, ty in ((x0 + 110, y0 + 60), (x1 - 330, y0 + 60), (x0 + 110, y1 - 60), (x1 - 330, y1 - 60)):
        g.append(F.rect(tx - 10, ty - 44, 240, 88, J.BG, J.LINE_DIM, 3, rx=44) + F.rect(tx + 20, ty - 18, 180, 36, J.LINE_DIM, rx=18))
    # 潜水艇（機首＝左）
    L, cx = LT["L"], LT["cx"]
    R = L * 0.14
    xn, xc0, xc1, xt = cx - L / 2, cx - L * 0.30, cx + L * 0.08, cx + L / 2
    g.append(F.poly([(xc1, cy - R), (xt, cy), (xc1, cy + R)], J.BG, SUBC, 4, close=True))
    g.append(F.rect(xc0, cy - R, xc1 - xc0, 2 * R, J.BG, SUBC, 4))
    g.append(f'<path d="M{xc0:.1f} {cy - R:.1f} A{xc0 - xn:.1f} {R:.1f} 0 0 0 {xc0:.1f} {cy + R:.1f}" fill="{J.BG}" stroke="{SUBC}" '
             f'stroke-width="4"/>')
    g.append(F.rect(cx - L * 0.12, cy - R * 1.45, L * 0.20, R * 2.9, J.BG, SUBC, 4, rx=40))
    for yy in (cy - R * 0.95, cy + R * 0.95):
        g.append(F.circ(cx - L * 0.02, yy, R * 0.32, J.LINE_DIM))
    return g


def lars_top_stage(prev, st):
    s = []
    if _on(prev, st, "close"):
        L, cx, cy = LT["L"], LT["cx"], LT["cy"]
        R = L * 0.14
        xn, xc0 = cx - L / 2, cx - L * 0.30
        s.append(f'<path d="M{xc0:.1f} {cy - R:.1f} A{xc0 - xn:.1f} {R:.1f} 0 0 0 {xc0:.1f} {cy + R:.1f} Z" fill="{SUBC}" fill-opacity="0.30" '
                 f'stroke="{COC}" stroke-width="8"/>')
        for k in range(9):
            y = cy - R + 2 * R * k / 8
            s.append(F.circ(xc0 - 3, y, 6, J.AMBER))
    return s


# ══════════════════════════════════════════════════════════
#  lars_side（c314）＝横から見た台が沈む3段
# ══════════════════════════════════════════════════════════
LS = dict(sea=400.0, x0=540.0, x1=1380.0, top=360.0, h=70.0, sub_cy=300.0, sub_L=520.0, under=230.0, det=200.0)


def lars_side_base(st0):
    return [F.rect(F.BX0 + 10, LS["sea"], F.BW - 20, 450.0, "#16303f", op=0.55),     # ⚠️ geom_gap：下の端 y 870 は注の行に触れた＝850
            F.line(F.BX0 + 10, LS["sea"], F.BX1 - 10, LS["sea"], SEA_LN, 5),
            _tline(F.BX1 - 30, LS["sea"] - 14, "海面", 28, J.TICK, "end", 200)]


def lars_side_parts(st):
    dy_l = LS["under"] if st["lvl"] == "under" else 0.0
    dy_s = dy_l + (LS["det"] if st["det"] == "on" else 0.0)
    x0, x1, t, h = LS["x0"], LS["x1"], LS["top"], LS["h"]
    G = titan_geo((x0 + x1) / 2, LS["sub_cy"], LS["sub_L"])
    out = [_P("pontoon", "poly", [(x0, t), (x1, t), (x1 + 40, t + h / 2), (x1, t + h), (x0, t + h)], fill=J.BG2, stroke=COC, w=5, dy=dy_l),
           _P("water", "poly", [(x0 + 30, t + h * 0.5), (x1 - 30, t + h * 0.5), (x1 - 30, t + h - 10), (x0 + 30, t + h - 10)],
              fill="#2c6f9a", stroke=None, w=0, dy=dy_l, alpha=0.85 if st["fill"] == "on" else 0.0),
           ]
    hull, tail = titan_poly(G)
    out += [_P("sub_tail", "poly", tail, fill=J.BG2, stroke=J.LINE, w=4, dy=dy_s), _P("sub", "poly", hull, fill=J.BG, stroke=SUBC, w=5, dy=dy_s)]
    return out


def lars_side_stage(prev, st):
    return []


# ══════════════════════════════════════════════════════════
#  sink（c315）・drop（c409）＝重りで沈む・重りを落として緩める／浮く（重りの数と場所は描かない）
# ══════════════════════════════════════════════════════════
SK = dict(cx=760.0, cy=430.0, L=600.0)
DR3 = dict(xs=(420.0, 960.0, 1500.0), cy=470.0, L=420.0)


def sink_base(st0):
    G = titan_geo(SK["cx"], SK["cy"], SK["L"])
    return [F.rect(F.BX0 + 10, 280.0, F.BW - 20, 570.0, "#16303f", op=0.45), titan_svg(G, frame=True)]


def _weight(cx, top, w=110.0, h=46.0, col=None):
    c = col or J.LINE
    return F.rect(cx - w / 2, top, w, h, J.LINE_DIM, c, 4, rx=6) + _tline(cx, top + h - 12, "重り", 26, INK, "middle", w - 10)


def sink_stage(prev, st):
    s = []
    G = titan_geo(SK["cx"], SK["cy"], SK["L"])
    if _on(prev, st, "fall"):
        y = G["cy"] + G["R"] + G["L"] * 0.07
        s.append(_weight(G["cx"] - 40, y, 140.0))
        s.append(_arrow(G["cx"], y + 70, G["cx"], 840.0, J.LINE, 9, 34))
    return s


def drop_base(st0):
    g = [F.rect(F.BX0 + 10, 280.0, F.BW - 20, 570.0, "#16303f", op=0.45),
         F.line(F.BX0 + 10, 830.0, F.BX1 - 10, 830.0, SEA_LN, 5, dash="14 10"), _tline(F.BX1 - 30, 814.0, "海の底", 26, J.TICK, "end", 200)]
    G = titan_geo(DR3["xs"][0], DR3["cy"], DR3["L"])
    g.append(titan_svg(G, frame=False))
    g.append(_weight(G["cx"], G["cy"] + G["R"] + 8))
    g.append(_arrow(G["cx"], G["cy"] + G["R"] + 70, G["cx"], 790.0, J.LINE, 8, 30))
    g.append(_tline(G["cx"], 330.0, "降りる", 34, INK, "middle", 300))
    return g


def drop_stage(prev, st):
    s = []
    if _on(prev, st, "slow"):
        G = titan_geo(DR3["xs"][1], DR3["cy"], DR3["L"])
        s.append(titan_svg(G, frame=False))
        s.append(_weight(G["cx"] - 40, G["cy"] + G["R"] + 120))
        s.append(_arrow(G["cx"] - 40, G["cy"] + G["R"] + 170, G["cx"] - 40, 790.0, J.LINE_DIM, 5, 22))
        s.append(_arrow(G["cx"] + 120, G["cy"] + G["R"] + 20, G["cx"] + 120, G["cy"] + G["R"] + 110, J.LINE, 8, 30))
        s.append(_tline(G["cx"], 330.0, "落として緩める", 34, INK, "middle", 400))
    if _on(prev, st, "rise"):
        G = titan_geo(DR3["xs"][2], DR3["cy"] + 60, DR3["L"])
        s.append(titan_svg(G, frame=False))
        s.append(_weight(G["cx"], 760.0))
        s.append(_arrow(G["cx"], G["cy"] - G["R"] - 20, G["cx"], 380.0, J.LINE, 8, 30))
        s.append(_tline(G["cx"], 330.0, "落として浮く", 34, INK, "middle", 400))
    return s


# ══════════════════════════════════════════════════════════
#  sonar（c316）＝母船の下の送受信機と艇のあいだの音の波
# ══════════════════════════════════════════════════════════
SN = dict(sea=380.0, ship=(760.0, 380.0), tr=(800.0, 470.0), sub=(1280.0, 760.0))   # ⚠️ geom_gap：船を x 560 に置くと船橋が左上の札に触れた


def _ship_side(cx, sea, L=520.0, col=None):
    c = col or SHIPC
    h = L * 0.12
    hull = [(cx - L / 2, sea - h), (cx + L / 2 + 30, sea - h), (cx + L / 2, sea + h * 0.55), (cx - L / 2 + 30, sea + h * 0.55)]
    br = [(cx - L * 0.30, sea - h), (cx - L * 0.30, sea - h * 2.4), (cx - L * 0.05, sea - h * 2.4), (cx - L * 0.05, sea - h)]
    return F.poly(hull, J.BG2, c, 5, close=True) + F.poly(br, J.BG2, c, 4, close=True)


def sonar_base(st0):
    g = [F.rect(F.BX0 + 10, SN["sea"], F.BW - 20, 470.0, "#16303f", op=0.55),
         F.line(F.BX0 + 10, SN["sea"], F.BX1 - 10, SN["sea"], SEA_LN, 5), _ship_side(SN["ship"][0], SN["sea"])]
    (tx, ty), (sx, sy) = SN["tr"], SN["sub"]
    g.append(F.line(tx, SN["sea"] + 30, tx, ty - 16, SHIPC, 3) + F.rect(tx - 16, ty - 16, 32, 32, J.BG2, SHIPC, 4, rx=6))
    g.append(titan_svg(titan_geo(sx, sy, 420.0), frame=False))
    # ⚠️ geom_gap：船の上は左上の見え方の札と船橋に触れた／🔧 試し焼き：船の右（x 1080）は「電波は水の中を通りにくい」の札の真下で1つの札に読めた＝船首の左
    g.append(_tline(480.0, SN["sea"] - 24, "母船", 32, SHIPC, "end", 200))
    g.append(_tline(sx, sy - 90, "潜水艇", 32, SUBC, "middle", 200))
    return g


def _arcs(x, y, ang, rs, col, sw=5):
    g = []
    for r in rs:
        pts = [(x + r * math.cos(math.radians(ang + a)), y + r * math.sin(math.radians(ang + a))) for a in range(-30, 31, 6)]
        g.append(F.poly(pts, "none", col, sw))
    return "".join(g)


def sonar_stage(prev, st):
    s = []
    (tx, ty), (sx, sy) = SN["tr"], SN["sub"]
    ang = math.degrees(math.atan2(sy - ty, sx - tx))
    if _on(prev, st, "sound"):
        s.append(_arcs(tx, ty, ang, (60, 110, 160), J.LINE))
        s.append(_arcs(sx - 220, sy - 30, ang + 180, (60, 110, 160), J.LINE))
    if _on(prev, st, "radio"):
        x, y = 1460.0, 330.0
        s.append(_arcs(x - 90, y, 0, (30, 60), J.LINE_DIM, 4) + _xmark(x, y + 100, 30, J.ALERT, 8))
        s.append(F.line(x, y + 60, x, y + 140, J.LINE_DIM, 4, dash="8 8"))
    if _on(prev, st, "voice"):
        x, y = 1720.0, 560.0
        s.append(F.rect(x - 34, y - 60, 68, 100, J.BG2, J.LINE_DIM, 4, rx=30) + F.line(x, y + 40, x, y + 80, J.LINE_DIM, 4)
                 + _xmark(x, y - 10, 46, J.ALERT, 9))
    return s


# ══════════════════════════════════════════════════════════
#  comms（c318）＝2つの通信の箱
# ══════════════════════════════════════════════════════════
CM = dict(xs=(560.0, 1360.0), y=520.0, w=640.0, h=260.0)
CM_T = (("1つ目の装置", "文字を送る・位置を追う"), ("2つ目の装置", "予備の通信と追跡"))


def comms_base(st0):
    g = []
    for i, (a, b) in enumerate(CM_T):
        x, y, w, h = CM["xs"][i], CM["y"], CM["w"], CM["h"]
        c = SHIPC if i == 0 else J.LINE_DIM
        g.append(F.rect(x - w / 2, y - h / 2, w, h, J.BG2, c, 6 if i == 0 else 4, rx=14))
        g.append(_tline(x, y - 22, a, 40, INK if i == 0 else J.TICK, "middle", w - 60))
        g.append(_tline(x, y + 40, b, 32, INK if i == 0 else J.TICK, "middle", w - 60))
    g.append(_check(CM["xs"][0] + CM["w"] / 2 - 60, CM["y"] - CM["h"] / 2 + 52, 22, SHIPC))
    return g


def comms_stage(prev, st):
    s = []
    if _on(prev, st, "dead"):
        x, y, w, h = CM["xs"][1], CM["y"], CM["w"], CM["h"]
        s.append(F.rect(x - w / 2, y - h / 2, w, h, "none", J.ALERT, 6, rx=14))
        s.append(_box(x, y + h / 2 + 50, 360, 76, "動いていない", J.ALERT, ink=J.ALERT, cap=36))
    return s


# ══════════════════════════════════════════════════════════
#  chat（c317・c401・c406・c408）＝付録A の文の吹き出し（打ち間違いのまま）
# ══════════════════════════════════════════════════════════
#   原文 TSB 付録A（時刻・送り手〈T＝潜水艇・SST＝母船の支援の班〉・文）。画面の時刻は秒まで（小数を落とす＝門番の表と同じ書き方）
APPA = {
    # ⚠️ 門番 wording：組の名にカット番号（"c317"）を使うと「画面にカット番号」と鳴る（SPEC の文字列は画面の言葉として測られる）
    "descent": (("9:19:36", "SST", "I hsvr trscking"), ("9:19:43", "T", "descendingb thru 235"), ("9:19:49", "SST", "i have tracking"),
             ("9:20:02", "T", "yeah")),
    "restore": (("10:11:55", "T", "lost system oand chat settings"), ("10:14:17", "T", "yes"), ("10:14:35", "T", "all good here"),
             ("10:15:39", "SST", "ack all good")),
    "niskin": (("10:36:50", "SST", "remember to write down the location and time of niskin deployment"), ("10:38:06", "T", "n?"),
             ("10:38:30", "SST", "remember to write down the location and time when you deploy the niskin bottle"),
             ("10:39:36", "T", "when? messages truncated"), ("10:39:57", "SST", "when you deploy niskin"), ("10:40:01", "SST", "write down time"),
             ("10:40:04", "SST", "andn location"), ("10:40:56", "T", "no niskin. never cleaned and string baf")),
    "last": (("10:47:26", "T", "dropped two wts"),),
}
CH = dict(xl=300.0, xr=1640.0, mw=1080.0)


def _ch_rows(key):
    rows = APPA[key]
    n = len(rows)
    step = 116.0 if n <= 4 else 66.0
    cap = 34 if n <= 4 else 26
    y0 = 390.0 if n <= 4 else 330.0
    return rows, [y0 + i * step for i in range(n)], cap


def chat_base(st0):
    # 🔧 試し焼き：c408 だけ「潜水艇」の下に用の無い線を引いていた＝外した
    return [_tline(CH["xl"] - 160, 300.0, "潜水艇", 30, SUBC, "start", 200), _tline(CH["xr"] + 150, 300.0, "母船", 30, SHIPC, "end", 200)]


def _bubble(row, y, cap):
    t, who, txt = row
    w = min(F.fm.width(txt, cap) + 56, CH["mw"])
    h = cap + 34
    if who == "T":
        x0, c, tx = CH["xl"], SUBC, CH["xl"] - 20
        tail = [(x0 + 10, y + h / 2 - 16), (x0 - 18, y + h / 2 + 4), (x0 + 30, y + h / 2 - 2)]
        lab = (tx, "end")
    else:
        x0, c, tx = CH["xr"] - w, SHIPC, CH["xr"] + 20
        tail = [(CH["xr"] - 10, y + h / 2 - 16), (CH["xr"] + 18, y + h / 2 + 4), (CH["xr"] - 30, y + h / 2 - 2)]
        lab = (tx, "start")
    return (F.rect(x0, y - h / 2, w, h, J.BG2, c, 4, rx=h / 2) + F.poly(tail, J.BG2, c, 4, close=True)
            + _tline(x0 + 28, y + cap * 0.36, txt, cap, INK, "start", w - 50)
            + _tline(lab[0], y + 9, t, 24, J.TICK, lab[1], 150, "Dela"))


def chat_stage(prev, st):
    s = []
    rows, ys, cap = _ch_rows(st["set"])
    a, b = int(prev["n"]), int(st["n"])
    for i in range(a, b):
        s.append(_bubble(rows[i], ys[i], cap))
    if _on(prev, st, "uscg"):
        s.append(_box(CH["xl"] + 200, 640.0, 560.0, 120.0, "10:47:02ごろ 送った", USC, cap=36, t2="米沿岸警備隊の記録"))
    return s


# ══════════════════════════════════════════════════════════
#  depth（c319・c402・c418・c419）＝深さの線（記録の点だけ・あいだは直線＝模式）
# ══════════════════════════════════════════════════════════
#   (時刻, 深さ m, 段)。原文：TSB §1.3.2「descending through 235 m」（9:19）・「Titan at 680 m」（9:31）・USCG p32「At 9:23:04 … 436 m」・
#   p34「from 2,203 m … to 2,289 m」（10:11:18〜10:15）・「Four minutes later［10:36:50 の4分後］… 3,149 m」・p35「approximately 10:47:02 … 3,341 m」
#   「approximately 10:47:08 … 3,346.28 m」
DEPTH = (("9:19", 235.0, "a"), ("9:23", 436.0, "a"), ("9:31", 680.0, "a"), ("10:11", 2203.0, "b"), ("10:15", 2289.0, "b"),
         ("10:40:50", 3149.0, "c"), ("10:47:02", 3341.0, "c"), ("10:47:08", 3346.28, "c"))
SEABED_M = 3800.0
DP = dict(all=dict(t0=9 * 60 + 10, t1=10 * 60 + 55, d0=0.0, d1=4000.0, x0=300.0, x1=1720.0, y0=320.0, y1=830.0,
                   tt=("9:15", "9:30", "9:45", "10:00", "10:15", "10:30", "10:45"), dt=(0, 1000, 2000, 3000, 4000)),
          end=dict(t0=10 * 60 + 30, t1=10 * 60 + 52, d0=2700.0, d1=3900.0, x0=300.0, x1=1720.0, y0=320.0, y1=830.0,
                   tt=("10:35", "10:40", "10:45", "10:50"), dt=(3000, 3200, 3400, 3600, 3800)))   # ⚠️ geom_gap：10:30 の目盛りの字が物差しの名に触れた
DP_GAP = ("9:53", "10:10")        # 母船の問いに返事が来ない（TSB §1.3.2「At 0953 … kept sending this message until 1010」）
DP_ORDER = ("0", "a", "b", "c")


def _min(t):
    p = [float(x) for x in t.split(":")]
    return p[0] * 60 + p[1] + (p[2] / 60 if len(p) > 2 else 0)


def dp_xy(z, t, m):
    D = DP[z]
    x = D["x0"] + (D["x1"] - D["x0"]) * (_min(t) - D["t0"]) / (D["t1"] - D["t0"])
    y = D["y0"] + (D["y1"] - D["y0"]) * (m - D["d0"]) / (D["d1"] - D["d0"])
    return x, y


def depth_base(st0):
    z = st0["z"]
    D = DP[z]
    g = [F.line(D["x0"], D["y0"], D["x1"], D["y0"], J.LINE, 3), F.line(D["x0"], D["y0"], D["x0"], D["y1"], J.LINE, 3)]
    for t in D["tt"]:
        x, _ = dp_xy(z, t, D["d0"])
        g.append(F.line(x, D["y0"] - 10, x, D["y0"], J.LINE, 3) + _tline(x, D["y0"] - 20, t, 26, J.TICK, "middle", 120, "Dela"))
    for m in D["dt"]:
        _, y = dp_xy(z, f"{D['t0'] // 60}:{D['t0'] % 60:02d}", m)
        g.append(F.line(D["x0"], y, D["x1"], y, J.GRID, 2) + _tline(D["x0"] - 14, y + 9, f"{m:,}", 26, J.TICK, "end", 120))
    g.append(_tline(D["x0"] - 14, D["y0"] - 40, "深さ（メートル）", 24, J.TICK, "end", 200))   # ⚠️ 門番 layout：下だと注の行に重なった
    if z == "end":
        g += _dp_upto(z, "0", st0["upto"]) + _dp_sea(z)
    return g


def _in_win(z, t, m):
    D = DP[z]
    return D["t0"] <= _min(t) <= D["t1"] and D["d0"] <= m <= D["d1"]


def _dp_upto(z, a, b):
    """段 a の次から段 b までの点と線（前の段の最後の点からつなぐ）。寄り（z=end）は窓の外の点を描かず、窓に入る線は左の端で切る。"""
    s = []
    ia, ib = DP_ORDER.index(a), DP_ORDER.index(b)
    if ib <= ia:
        return s
    want = set(DP_ORDER[ia + 1: ib + 1])
    prev = None
    D = DP[z]
    for t, m, k in DEPTH:
        x, y = dp_xy(z, t, m)
        if k in want and _in_win(z, t, m):
            if prev is not None:
                (px, py), (pt_, pm) = prev
                if not _in_win(z, pt_, pm):          # 窓の左の端（t0）で線を切る
                    f = (D["t0"] - _min(pt_)) / (_min(t) - _min(pt_))
                    px, py = dp_xy(z, f"{D['t0'] // 60}:{D['t0'] % 60:02d}", pm + (m - pm) * f)
                s.append(F.line(px, py, x, y, SUBC, 5))
            s.append(F.circ(x, y, 10, SUBC))
        prev = ((x, y), (t, m))
    return s


def _dp_sea(z):
    D = DP[z]
    _, y = dp_xy(z, "10:00", SEABED_M)
    # ⚠️ geom_gap：線の下（y 844）は 4,000メートルの目盛りの線に乗った＝線の上・左の端から
    return [F.line(D["x0"], y, D["x1"], y, SEA_LN, 5, dash="16 10"), _tline(D["x0"] + 20, y - 14, "海の底（約3,800メートル）", 28, J.TICK, "start", 520)]


def depth_stage(prev, st):
    z = st["z"]
    s = _dp_upto(z, prev["upto"], st["upto"])
    if _on(prev, st, "gap") and z == "all":      # 寄り（z=end）の窓の外＝描かない
        (xa, _), (xb, _) = dp_xy(z, DP_GAP[0], 0), dp_xy(z, DP_GAP[1], 0)
        D = DP[z]
        s.append(F.rect(xa, D["y0"] + 4, xb - xa, D["y1"] - D["y0"] - 8, J.LINE_DIM, op=0.35))
    if _on(prev, st, "sea"):
        s += _dp_sea(z)
    if _on(prev, st, "left"):
        x, y = dp_xy(z, "10:15", 2289.0)
        _, ys = dp_xy(z, "10:15", SEABED_M)
        s.append(F.line(x + 40, y + 6, x + 40, ys - 6, J.AMBER, 5) + F.line(x + 26, y + 6, x + 54, y + 6, J.AMBER, 5)
                 + F.line(x + 26, ys - 6, x + 54, ys - 6, J.AMBER, 5))
    if _on(prev, st, "stop"):
        x, y = dp_xy(z, DEPTH[-1][0], DEPTH[-1][1])
        s.append(F.circ(x, y, 18, "none", J.ALERT, 6))
    return s


# ══════════════════════════════════════════════════════════
#  bow（c403・c404）＝上から見たタイタニックの船首（模式・北が上）と、潜水艇の位置の知らせ
# ══════════════════════════════════════════════════════════
BW_ = dict(tip=(820.0, 340.0), L=400.0, w=110.0, r=200.0)
BW_DIR = dict(ese=112.5, ene=67.5)        # 方位（度・北から時計回り）＝付録A「east south east of the nbow」「east north east of the bow」
BW_JUMP = ((0.0, 0.0), (60.0, -70.0), (-40.0, 50.0), (90.0, 30.0), (-20.0, -90.0), (40.0, 80.0))


def bw_pt(kind, r=None):
    a = math.radians(BW_DIR[kind])
    r = BW_["r"] if r is None else r
    tx, ty = BW_["tip"]
    return tx + r * math.sin(a), ty - r * math.cos(a)


def bow_base(st0):
    tx, ty = BW_["tip"]
    L, w = BW_["L"], BW_["w"]
    g = [F.poly([(tx, ty), (tx + w, ty + 120), (tx + w, ty + L), (tx - w, ty + L), (tx - w, ty + 120)], J.BG2, J.LINE, 4, close=True),
         F.line(tx - w, ty + L, tx + w, ty + L, J.LINE_DIM, 4, dash="10 8"),
         _tline(tx, ty + L + 50, "タイタニックの船首", 32, INK, "middle", 400),
         F.circ(tx, ty, 9, J.LINE)]
    nx, ny = 1760.0, 660.0          # ⚠️ geom_gap：右上（1700, 330）は「母船が船首の真上へ」の札に触れた＝右下へ
    g.append(_arrow(nx, ny + 70, nx, ny - 20, J.LINE, 5, 20) + _tline(nx, ny + 108, "北", 30, J.TICK, "middle", 80))
    return g


def bow_stage(prev, st):
    s = []
    tx, ty = BW_["tip"]
    if _on(prev, st, "ese"):
        x, y = bw_pt("ese")
        s.append(F.line(tx, ty, x, y, SUBC, 3, dash="8 8") + F.circ(x, y, 16, SUBC))
    if _on(prev, st, "ene"):
        x, y = bw_pt("ene")
        s.append(F.line(tx, ty, x, y, SHIPC, 3, dash="8 8") + F.circ(x, y, 16, "none", SHIPC, 5))
    if _on(prev, st, "plan"):
        s.append(_arrow(1460.0, ty + 40, tx + 40, ty, SHIPC, 6, 24))
        s.append(F.rect(1460.0 - 40, ty + 20, 80, 40, J.BG2, SHIPC, 4, rx=10))
    if _on(prev, st, "jump"):
        x0, y0 = bw_pt("ese")
        pts = [(x0 + dx, y0 + dy) for dx, dy in BW_JUMP]
        for (a, b), (c, d) in zip(pts, pts[1:]):
            s.append(F.line(a, b, c, d, SUBC, 3, dash="6 8"))
        for x, y in pts[1:]:
            s.append(F.circ(x, y, 12, "none", SUBC, 4))
    return s


# ══════════════════════════════════════════════════════════
#  two（c410）＝2段の札（上＝米国の2つの調べ／下＝カナダの調べ）
# ══════════════════════════════════════════════════════════
TW = dict(x=960.0, ys=(400.0, 680.0), w=1500.0, h=190.0)
TW_US = "この深さなら通常の手順"          # ⚠️ 門番 echo：「この深さでのふつうのやり方」は語りの写し
TW_CA = ("海の底まで約500メートル", "いつもより早い", "理由は分からない")
TW_SEABED = 500                   # 海の底までの残り（TSB §1.3.2「approximately 500 m from the seabed」）


def two_base(st0):
    g = []
    for i, y in enumerate(TW["ys"]):
        g.append(F.rect(TW["x"] - TW["w"] / 2, y - TW["h"] / 2, TW["w"], TW["h"], J.BG2, J.LINE_DIM, 4, rx=14))
    return g


def two_stage(prev, st):
    s = []
    x0 = TW["x"] - TW["w"] / 2
    if _on(prev, st, "us"):
        y = TW["ys"][0]
        s.append(F.rect(x0, y - TW["h"] / 2, TW["w"], TW["h"], J.BG2, USC, 6, rx=14))
        s.append(F.rect(x0 + 30, y - 70, 250, 56, USC, rx=10) + _tline(x0 + 155, y - 31, "米沿岸警備隊", 28, J.BG, "middle", 230))
        s.append(F.rect(x0 + 300, y - 70, 300, 56, NTC, rx=10) + _tline(x0 + 450, y - 31, "米運輸安全委員会", 28, J.BG, "middle", 280))
        s.append(_tline(x0 + 40, y + 56, TW_US, 44, INK, "start", TW["w"] - 80))
    if _on(prev, st, "ca"):
        y = TW["ys"][1]
        s.append(F.rect(x0, y - TW["h"] / 2, TW["w"], TW["h"], J.BG2, TSC, 6, rx=14))
        s.append(F.rect(x0 + 30, y - 70, 340, 56, TSC, rx=10) + _tline(x0 + 200, y - 31, "カナダの運輸安全委員会", 28, J.BG, "middle", 320))
        s.append(_tline(x0 + 40, y + 56, TW_CA[0] + "・" + TW_CA[1], 42, INK, "start", TW["w"] - 80))
    if _on(prev, st, "why"):
        y = TW["ys"][1]
        s.append(_box(x0 + TW["w"] - 280, y - 42, 460, 76, TW_CA[2], J.AMBER, ink=J.AMBER, cap=34))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表・札の置き場・線の先
# ══════════════════════════════════════════════════════════
VIEWS = dict(
    fuji=dict(lab="深さの比べ（横から）", fields=dict(press=ONOFF, coin=ONOFF), base=fuji_base, stage=fuji_stage),
    reports=dict(lab="報告書の表紙", fields=dict(r1=ONOFF, r2=ONOFF, r3=ONOFF), base=reports_base, stage=reports_stage),
    side=dict(lab="横から見たタイタン（機首が左）", fields=dict(dim=ONOFF, hull=ONOFF, mat=ONOFF, bolts=ONOFF, only=ONOFF), base=side_base,
              stage=side_stage),
    org=dict(lab="上級の職の席（カナダの報告書の表4）", fields=dict(seats=ONOFF, ceo=ONOFF, all=ONOFF, staff=ONOFF), base=org_base,
             stage=org_stage),
    paper=dict(lab="書類の要点（英字は原文のまま）", fields=dict(doc=("waiver", "plan"), hl1=ONOFF, hl2=ONOFF, n9=ONOFF, name=ONOFF, uscg=ONOFF),
               base=paper_base, stage=paper_stage),
    table=dict(lab="カナダの報告書 付録Bの表（英字は原文のまま）", fields=dict(yr=ONOFF), base=table_base, stage=table_stage),
    dives=dict(lab="付録Bの潜航（1回＝1点）", fields=dict(reach=ONOFF, dome=ONOFF, batt=ONOFF, thr=ONOFF, wt=ONOFF, com=ONOFF), base=dives_base,
               stage=dives_stage),
    lars_top=dict(lab="上から見た台と潜水艇（機首が左）", fields=dict(close=ONOFF), base=lars_top_base, stage=lars_top_stage),
    lars_side=dict(lab="横から見た台と潜水艇", fields=dict(fill=ONOFF, lvl=("up", "under"), det=ONOFF), base=lars_side_base,
                   stage=lars_side_stage, parts=lars_side_parts),
    sink=dict(lab="横から見た潜水艇", fields=dict(fall=ONOFF), base=sink_base, stage=sink_stage),
    drop=dict(lab="重りの使い方（横から）", fields=dict(slow=ONOFF, rise=ONOFF), base=drop_base, stage=drop_stage),
    sonar=dict(lab="母船と潜水艇の通信（横から）", fields=dict(sound=ONOFF, radio=ONOFF, voice=ONOFF), base=sonar_base, stage=sonar_stage),
    comms=dict(lab="潜水艇の2つの通信の装置", fields=dict(dead=ONOFF), base=comms_base, stage=comms_stage),
    chat=dict(lab="母船と潜水艇の文", fields=dict(set=tuple(APPA), n=tuple(str(i) for i in range(9)), uscg=ONOFF),
              base=chat_base, stage=chat_stage),
    depth=dict(lab="潜水艇の深さ（記録の点）", fields=dict(z=("all", "end"), upto=DP_ORDER, gap=ONOFF, sea=ONOFF, left=ONOFF, stop=ONOFF),
               base=depth_base, stage=depth_stage),
    bow=dict(lab="上から見た船首のまわり（北が上）", fields=dict(ese=ONOFF, ene=ONOFF, plan=ONOFF, jump=ONOFF), base=bow_base, stage=bow_stage),
    two=dict(lab="調べごとの見方", fields=dict(us=ONOFF, ca=ONOFF, why=ONOFF), base=two_base, stage=two_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
START["lars_side"]["lvl"] = "up"
HEAD_ONLY = dict(paper=("doc",), chat=("set",), depth=("z",))
# 戻さない欄（増えた吹き出しは減らない・描いた深さの点は消えない・沈んだ台は浮かない）
ORDER = dict(chat=dict(n=tuple(str(i) for i in range(9))), depth=dict(upto=DP_ORDER), lars_side=dict(lvl=("up", "under")))
NOT_SCHEMATIC = ("table", "chat")       # 原文の表と文の写し（左上に「模式」を付けない）

TAG_AT = dict(
    fuji=dict(t=(1250.0, 620.0, "start", 560.0), top=(1250.0, 330.0, "start", 560.0)),
    reports=dict(),
    side=dict(cap=(L_X, 320.0, "start", 520.0), tag=(1290.0, 330.0, "start", 520.0), low=(L_X, 330.0, "start", 640.0),
              only=(L_X, 820.0, "start", 560.0)),
    org=dict(ra=(1250.0, 296.0, "start", 560.0), rb=(1250.0, 352.0, "start", 560.0)),   # CEO の席（x 770〜1150・y 287〜373）の右＝線（y 373〜）より上
    paper=dict(r=(1320.0, 330.0, "start", 480.0)),
    table=dict(n27=(176.0, 290.0, "end", 100.0)),          # ⚠️ geom_gap：表の右上（x 1500）は表の枠の中＝年の括弧の上の左の空き
    # 2021年の行は x 1296・2023年の行は x 672 まで＝右の空き（2023年の行の右・凡例 y 842 の上）
    dives=dict(t=(1380.0, 330.0, "start", 440.0), low=(800.0, 720.0, "start", 1000.0), low2=(800.0, 790.0, "start", 1000.0)),
    lars_top=dict(t1=(L_X, 320.0, "start", 640.0), t2=(1000.0, 320.0, "start", 760.0), low=(L_X, 830.0, "start", 1100.0)),
    lars_side=dict(t1=(L_X, 320.0, "start", 560.0), t2=(L_X, 470.0, "start", 520.0), t3=(L_X, 770.0, "start", 520.0)),
    sink=dict(r=(1150.0, 600.0, "start", 640.0), r2=(1150.0, 700.0, "start", 640.0), r3=(1150.0, 800.0, "start", 640.0)),
    drop=dict(),
    sonar=dict(sound=(L_X, 600.0, "start", 520.0), radio=(1320.0, 300.0, "end", 480.0), voice=(1640.0, 640.0, "end", 560.0)),
    comms=dict(t=(L_X, 330.0, "start", 520.0), why=(1040.0, 800.0, "start", 760.0)),
    chat=dict(dep=(CH["xl"] + 520.0, 470.0, "start", 520.0)),
    # ⚠️ geom_gap：札は目盛りの横の線（全体＝y 447・575・702・830／寄り＝y 447・532・617・702・787）のあいだに置く
    depth=dict(rate=(330.0, 520.0, "start", 520.0), gap=(1125.0, 390.0, "start", 540.0), d23=(1200.0, 560.0, "start", 300.0),
               left=(1260.0, 675.0, "start", 440.0), d33=(1700.0, 420.0, "end", 600.0), force=(1700.0, 490.0, "end", 700.0),
               none=(340.0, 600.0, "start", 760.0), rec=(340.0, 680.0, "start", 760.0)),   # 海の底の札（寄りで y 745〜774）の上
    bow=dict(ese=(1100.0, 470.0, "start", 520.0), ene=(1100.0, 270.0, "start", 520.0), plan=(1520.0, 330.0, "start", 320.0),
             jump=(L_X, 330.0, "start", 520.0), sig=(L_X, 780.0, "start", 560.0)),
    two=dict(),
)


def anchors(view, st):
    """札から線を引く先（画面の点）。"""
    if view == "side":
        G = sd_geo()
        return dict(hull=((G["xc0"] + G["xc1"]) / 2, G["cy"] - G["R"]), dome=(G["xh0"] + 10, G["cy"] - G["R"] * 0.7),
                    cyl=((G["xc0"] + G["xc1"]) / 2, G["cy"]))
    if view == "dives":
        pts = {i: (x, y) for i, _, x, y in dv_pts()}
        return {f"d{i}": v for i, v in pts.items()}
    if view == "depth":
        z = st["z"]
        return {t: dp_xy(z, t, m) for t, m, _ in DEPTH}
    if view == "bow":
        return dict(ese=bw_pt("ese"), ene=bw_pt("ene"), tip=BW_["tip"])
    if view == "lars_top":
        return dict(dome=(LT["cx"] - LT["L"] * 0.42, LT["cy"] - LT["L"] * 0.14))
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
                raise ValueError(f"m22：{f_} は頭（start）だけで決める")
        cur = dict(cur, **new)
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m22：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m22：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    for f_, seq in ORDER.get(view, {}).items():
        idx = [seq.index(s[f_]) for s in out]
        if any(b < a for a, b in zip(idx, idx[1:])):
            raise ValueError(f"m22：{f_} は戻さない（{' → '.join(seq)}）")
    if view == "chat":
        n_rows = len(APPA[out[0]["set"]])
        if any(int(s["n"]) > n_rows for s in out):
            raise ValueError(f"m22：吹き出しの数が付録Aの行（{n_rows}）を超える")
    return out[0], out[1:]


def stage_art(view, prev, st):
    return VIEWS[view]["stage"](prev, st)


def _base(view, st0):
    """基図＋頭の状態の層（頭で on にした欄は基図に描く＝前のカットの続き）。depth の寄り（z=end）は基図が頭の点まで描く"""
    pre = dict(START[view], **{k: st0[k] for k in HEAD_ONLY.get(view, ())})
    if view == "depth" and st0["z"] == "end":
        pre = dict(pre, upto=st0["upto"], sea="on")
    return VIEWS[view]["base"](st0) + stage_art(view, pre, st0)


def _stage_svgs(view, steps, start, states, cap=34):
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
            if tg.get("to"):
                tx, ty = an[tg["to"]] if isinstance(tg["to"], str) else tg["to"]
                below_d = tg.get("d") and ty > y + round(c * 0.95)
                sy = y - round(c * 0.9) if ty < y - c else y + 8 + (round(c * 0.95) if below_d else 0)
                s.append(F.line(x, sy, tx, ty, tg.get("col", J.AMBER), 2))
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
    k0 = sh["keys"][0]
    pts = F.mech_pts(sh, k0)
    return F.poly(pts, k0.get("fill", sh.get("fill")) or "none", k0.get("stroke", sh.get("stroke")), sh.get("w") or None, close=True,
                  op=(round(a, 2) if a < 0.99 else None))


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")


def m22(view, steps, start=None, rel=(), note="", src=""):
    """22本目の模式図。view は VIEWS の17種。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m22：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view not in NOT_SCHEMATIC and "模式" not in note:
        raise ValueError("m22：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
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
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 34, VIEWS[view]["lab"] + ("" if view in NOT_SCHEMATIC else "・模式"), 1000, cap=28, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, st0, states)
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    f.mech = dict(kind="m22", view=view, start=st0, states=states, rel=list(rel), tags=texts, shapes=shapes,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M22）
# ══════════════════════════════════════════════════════════
def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst])
    if view == "fuji":
        out.update(px_m=(FJ["y1"] - FJ["y0"]) / FJ["mx"], y0=FJ["y0"], fuji_y=fj_y(FUJI_M), titanic_y=fj_y(TITANIC_M),
                   ticks={m: fj_y(m) for m in FJ_TICKS})
    elif view == "reports":
        out.update(order=[(w, ym, J.ROLE[r]) for w, _, ym, r in RP_T])
    elif view == "side":
        G = sd_geo()
        out.update(L=G["L"], x0=G["x0"], xt=G["xt"], len_m=SD_LEN_M, seats=SD_SEATS, bolts=len(_bolts(G, SD_BOLTS)),
                   dome_x=G["xh0"], cyl=(G["xc0"], G["xc1"]))
    elif view == "org":
        out.update(seats=list(ORG), staff=ORG_STAFF, col=COC)
    elif view == "paper":
        out.update(doc=start["doc"], lines=list(PP_DOC[start["doc"]]["lines"]), death=PP_DEATH)
    elif view == "table":
        out.update(rows=[tuple(r) for r in APPB], head=APPB_HEAD)
    elif view == "dives":
        out.update(rows=[(r[0], r[1], r[6]) for r in APPB], pts=dv_pts(), deep=[i for i, r in enumerate(APPB) if r[1] == DV_DEEP],
                   marks={k: dv_marked(k) for k in DV_MARK}, lit=SUBC)
    elif view == "chat":
        out.update(rows=list(APPA[start["set"]]), set=start["set"], cols=dict(T=SUBC, SST=SHIPC))
    elif view == "depth":
        z = start["z"]
        out.update(pts=[(t, m, dp_xy(z, t, m)) for t, m, _ in DEPTH], z=z, D=dict(DP[z]), gap=DP_GAP, seabed=SEABED_M)
    elif view == "bow":
        out.update(tip=BW_["tip"], ese=bw_pt("ese"), ene=bw_pt("ene"))
    elif view == "two":
        out.update(us=TW_US, ca=list(TW_CA), seabed=TW_SEABED)
    elif view == "lars_side":
        out.update(sea=LS["sea"], top=LS["top"], under=LS["under"], det=LS["det"], sub_cy=LS["sub_cy"])
    elif view == "comms":
        out.update(boxes=[a for a, _ in CM_T])
    return out
