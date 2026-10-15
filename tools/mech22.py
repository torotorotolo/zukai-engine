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
  🆕 ⑤b-4（2026-10-15）：第4〜7章（台本 第2版 §4 の画の欄と映像方針の一覧＝了承②）
  send    … 母船が送り続けた文（印の間隔は模式＝1分に2.5回）と、返事の無い潜水艇の段                                         c501
  proto   … 会社の手順の流れ（途絶→待つ→海面を探す→外へ）と「海の上のならい」の段                                         c502・c507
  none    … 欄が空（×）＝救助の備え2つ／亀裂を知らせた先3つ                                                                c521・c816
  layers  … 筒の壁の断面（5枚の層・1＝いちばん内側）・剥離の面（1と2・3と4）・空隙・こすれ                                    c610・c615・c619
  buckle  … 厚い1枚が薄い2枚に分かれ、外から押されて内へ曲がる（動く部品）                                                  c617
  tc      … 引っ張り（旅客機の胴体＝中から外へ）と押しつぶし（深い海の殻＝外から中へ）                                       c702
  shell   … ふつうの深海の潜水艇（鋼かチタンの球）とタイタン（炭素繊維の筒）の並べ図                                         c703・c704
  say     … 人の言葉＝輪郭（顔は描かない）＋吹き出しの英字（報告書が引くまま・訳は字幕）                                     c705・c712・c718・c806
  ruler   … 深さの物差し（縦・縮尺どおり）＝会社の望み・壊れる深さの計算・運航の目標・タイタニック                           c706・c709・c713
  sf      … 安全率のしくみ（潜ってよい深さと壊れる深さの棒・長さは模式）                                                     c707
  model   … 3分の1の模型（炭素繊維の筒とドーム）・外からの圧・壊れたドーム                                                 c711
  klass   … 船級のしくみ（持ち主→船級協会が確かめる→証明書）                                                               c714
  wind    … 筒の作り方（糸が樹脂の槽をくぐって回る芯に巻きつく）                                                           c801
  meet    … 2018年1月19日の会合の席（CEO・運航部長・社員3人）と録音の印                                                     c805
  side（🆕 crack＝前の左舷の内側の亀裂3つ）c520・c701・c815／paper（🆕 書類6枚）c710・c716・c717・c719・c802・c804・c810・c811
  🆕 ⑤b-5（2026-10-15）：第8〜9章（台本 第2版 §4 の画の欄と映像方針の一覧＝了承②）
  cards   … 要点の箱の並び（row＝横・flow＝矢印でつなぐ）＝材料・模型2つ・作り方・疲れの寿命・2つの道・3つの見方・警告の基準
                                                                        c901・c902・c903・c905・c907・c920・c922・ca21・ca22・ca25
  groove  … チタンの輪の溝（5インチ）と思ったより厚い筒の端（5.166インチ）・外側を削る（縮尺どおりの幅）                         c912
  coupons … 端材を18の試料に切る（長さの向き9・周りの向き9）                                                                   c915
  shelf   … 安全率を棚にたとえる（いつも100キロ＝基準 125キロ・この筒 111キロ）                                                c918
  d80     … 80回目の深さの線（NTSB 図19 を原寸で読んだ点だけ）と、浮上の終わりの大きな音・聞いた人                               ca05
  rtm     … 筒の外から見た監視装置（音のセンサー8・ひずみ計16）・押されて縮む・2022年に拾わなかった3つ                           ca06・ca24
  ae      … 80回目の終わりの音とひずみ（15時17分ごろから増える・15時26分45秒の山とひずみの跳び・米運輸安全委の幅）             ca07・ca08
  ctrl    … コントローラーの向き（そのまま＝倒す向きと動く向きが逆・逆さに持つ）                                               ca15
  stime   … 時刻に沿って横に並べたひずみ（潜航どうしを比べにくい）                                                             ca16
  nonlin  … 浅い所だけ曲がる線（層のはがれ）と筒の前の端のひずみ計                                                               ca19
  screen  … 監視装置の画面の決まり（30で黄・50で赤・警報の音なし・潜航ごとに0へ）                                               ca23
  dives（🆕 y22＝2022年だけ）ca01／bow（🆕 hit＝左舷の船首にぶつかる）ca02／ruler（🆕 mid＝0〜4,500m・試験の最も深い所・窓の等級2つ）c921・c923／
  layers（🆕 grind＝層ごとの削ったしわの数）c910／paper（🆕 書類5枚）c919・ca04・ca09・ca12・ca13／say（🆕 again）ca11／none（🆕 insp）ca10
  🆕 ⑤b-6（2026-10-15）：第10〜11章・終章（台本 第2版 §4 の画の欄と映像方針の一覧＝了承②）
  temp    … 冬の気温の平均（最高 −0.5°・最低 −5.5°＝カナダの報告書の書き方のまま「°」）と天気                               cb04
  risk    … 危険度の点数の目盛り（この日の35・48を超えると「ストライク」・3つで その日は中止）                                 cb17
  cols    … 3つの報告書の答えを3列に（上の段＝主な原因・下の段＝その次・7つ目に下線・下の段の「監督の穴」の枠）       cc02・cc03・cc05・cc06・cc11
  cmp     … 3つの答えの並べ（重なる所＝3列に✓・分かれる所＝列ごとの言葉と破線の帯）                                          cc09・cc10
  cards（🆕 tow・rec6・q3）cb13・cc08・cd02〜cd04／paper（🆕 書類6枚）cb02・cb06・cb18・cc07・cc13・cd05・cd06／layers（🆕 ice＝凍ってふくらむ）cb05／
  org（🆕 vac＝空いた席の枠・線の先 eng）cb08

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
from mech21 import _P, _arrow, _box, _check, _on, _qmark, _xmark

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
SD_CRACK = 3                      # 🆕 ⑤b-4：1つ目の船体の筒の内側の亀裂（TSB §1.12.1「3 interior cracks on the forward port side of the cylinder」）


def sd_geo():
    return titan_geo(SD["cx"], SD["cy"], SD["L"])


def sd_cracks(G):
    """🆕 ⑤b-4（c815）：筒の前寄りの亀裂の位置（機首が左＝見えているのは左舷）。位置と形は模式・数は記録"""
    return [(G["xc0"] + (G["xc1"] - G["xc0"]) * (0.12 + 0.10 * k), G["cy"] - G["R"] * (0.42 - 0.38 * k)) for k in range(SD_CRACK)]


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
    if _on(prev, st, "crack"):
        for x, y in sd_cracks(G):
            s.append(F.poly([(x - 34, y - 4), (x - 16, y + 10), (x, y - 10), (x + 16, y + 8), (x + 34, y - 6)], "none", J.ALERT, 6))
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
    if _on(prev, st, "vac"):          # 🆕 ⑤b-6（cb08）：空いた席（技術部長）を太い点線で＝字は基図の「（空席）」のまま
        i = next(k for k, (_nm, s_) in enumerate(ORG) if s_ == "vacant")
        x, y = ORG_XY[i]
        s.append(F.rect(x - ORG_W / 2 - 8, y - ORG_H / 2 - 8, ORG_W + 16, ORG_H + 16, "none", J.AMBER, 7, rx=14, dash="16 10"))
    return s


def org_vacant_xy():
    i = next(k for k, (_nm, s_) in enumerate(ORG) if s_ == "vacant")
    return ORG_XY[i]


# ══════════════════════════════════════════════════════════
#  paper（c209・c211）＝書類の要点（英字の句はそのまま・訳は字幕）
# ══════════════════════════════════════════════════════════
PP = dict(x0=250.0, x1=1180.0, y0=290.0, y1=850.0)
PP_DOC = dict(
    waiver=dict(head="参加の同意書（要点）", lines=("experimental submersible vessel", "not been certified by any regulatory body")),
    plan=dict(head="2023年の計画書（一節）", lines=("guests who help fund OceanGate expeditions",)),
    # 🆕 ⑤b-4（2026-10-15）：第6〜7章の6枚（句は報告書の英字のまま・頁は門番 check_mech の REC_M22 が持つ）。w＝紙の幅（既定 930）
    model=dict(head="米運輸安全委員会の見方（一節）", lines=("theoretical models of composite structures", "that assumed perfect geometry and fiber orientation",
                                                       "should have validated them through physical testing"), w=1060.0),
    blog=dict(head="会社のブログ（2019年2月）", lines=("Why Isn’t Titan Classed?", "by itself, classing is not sufficient to ensure safety"), w=1060.0),
    fn17=dict(head="米運輸安全委員会の注（一節）", lines=("a path for owners to prove seaworthiness of new technology", "no “experimental” design endorsement",
                                                   "for vessels carrying passengers or cargo"), w=1060.0),
    emp=dict(head="社員の言葉（米運輸安全委員会の報告書が引く）", lines=("paying clients as “mission specialists.”", "you can’t just change the title of a person",
                                                          "when you’re receiving compensation."), w=1060.0),
    qa18=dict(head="品質点検の報告（2018年1月18日・要点）", lines=("visible voids and delaminations", "end segments that had been cut off",
                                                         "a full inspection of the cylinder and the bond lines", "before any dives were conducted with people on board"),
              w=1060.0),
    mts=dict(head="業界の委員会の手紙の案（要点）", lines=("unanimous concern regarding the development of ‘TITAN’", "the current “experimental” approach adopted by OceanGate",
                                                 "could result in negative outcomes (from minor to catastrophic)", "a prototype testing program that was reviewed",
                                                 "and witnessed by a classification society"), w=1060.0),
    # 🆕 ⑤b-5（2026-10-15）：第8〜9章の5枚（句は報告書の英字のまま・行の切れ目だけ入れた・頁は門番 check_mech の REC_M22 が持つ）
    tsb115=dict(head="カナダの調べの一節", lines=("Assuming that the test results from the samples", "are representative of the properties of the carbon fibre cylinder",
                                             "it was unsafe for the Titan to have been repeatedly exposed",
                                             "to pressures equivalent to the depth of the Titanic or deeper"), w=1060.0),
    #   ⚠️ ca04：語りは ca02（7月3日の船首）の続きに聞こえるが、米沿岸警備隊の報告書ではこの「動けず」は80回目（7月15日）の階段の吹き抜け＝見出しで日を出す
    u80=dict(head="80回目（2022年7月15日）の記録（要点）", lines=("the TITAN became entangled in the TITANIC’s stairwell", "For a moment, the TITAN remained trapped",
                                                       "no incident report was filed for this event."), w=1060.0),
    shift=dict(head="会社の説明（報告書の要点）", lines=("a shift in the TITAN’s position within its frame", "told the hull had shifted in its metal cradle"), w=1060.0),
    u290a=dict(head="CEO の指示（米沿岸警備隊の報告書）", lines=("directed that no further investigation or assessments",
                                                    "were necessary ahead of the next scheduled 2022 dive", "or during the TITAN’s extended layup period"),
               w=1060.0),
    u290b=dict(head="米沿岸警備隊の見方（要点）", lines=("neither the Director of Engineering", "nor anyone else onboard with the authority",
                                                "to assess the submersible’s safety", "possessed the necessary engineering expertise",
                                                "to interpret the strain gauge data"), w=1060.0),
    # 🆕 ⑤b-6（2026-10-15）：第10〜11章・終章の6枚（句は報告書の英字のまま・行の切れ目だけ入れた・頁は門番 check_mech の REC_M22 が持つ）
    tarp=dict(head="基地からのメール（2022年9月28日・要点）", lines=("a quote for a tarp for the submersible had been provided",
                                                         "they had not received approval to proceed", "so the tarp was not purchased."), w=1060.0),
    u8=dict(head="米沿岸警備隊の結論と主な要因（要点）", lines=("unprotected in inclement weather", "compromised the TITAN’s hull integrity.",
                                                     "failure to conduct preventative maintenance on the TITAN’s hull", "or protect it from the elements"),
            w=1060.0),
    n73=dict(head="米運輸安全委員会の所見（一節）", lines=("After dive 82, the Titan sustained additional damage", "—of unknown origin—that further deteriorated",
                                                 "and weakened the pressure vessel to a point", "where it could not survive a dive to the depth of the Titanic."),
             w=1060.0),
    tc=dict(head="カナダの調べの一節", lines=("TC was unaware that the Titan was not registered", "with any flag state.",
                                         "both DFO and the CBSA had information about the Titan", "that TC was not aware of."), w=1060.0),
    u307=dict(head="米沿岸警備隊の報告書の一節", lines=("Encouraging employees to voice concerns", "without fear of retaliation",
                                                "and prioritizing safety over expediency", "could have prevented the sequence of events",
                                                "that led to the disaster."), w=1060.0),
    drift=dict(head="カナダの調べの一節", lines=("past success is not a guarantee of future success,", "because this drift occurs gradually,",
                                            "it is not easily identifiable", "and may go unnoticed as risk levels grow over time."), w=1060.0))
PP_DEATH = 9                      # 同意書の「death」（USCG p71「The liability waiver mentions death 9 times」）


def _pp_line_y(i, n=2):
    """句の行の y。2行までは ⑤b-3b の並び（c209・c211）のまま・3行からは行の間を詰める（紙の下の端 850 の内）。"""
    if n <= 2:
        return PP["y0"] + 230 + i * 150
    return PP["y0"] + 160 + i * min(110.0, (PP["y1"] - PP["y0"] - 220.0) / (n - 1))


def _pp_x1(d):
    return PP["x0"] + d.get("w", PP["x1"] - PP["x0"])


def paper_base(st0):
    d = PP_DOC[st0["doc"]]
    n, x1 = len(d["lines"]), _pp_x1(d)
    g = [F.rect(PP["x0"], PP["y0"], x1 - PP["x0"], PP["y1"] - PP["y0"], J.BG2, J.LINE, 4, rx=6),
         _tline(PP["x0"] + 40, PP["y0"] + 66, d["head"], 38, INK, "start", x1 - PP["x0"] - 80)]
    for k in range(9):
        y = PP["y0"] + 130 + k * 72
        if any(abs(y - _pp_line_y(i, n) + 10) < 40 for i in range(n)) or (n > 2 and y < _pp_line_y(n - 1, n) + 40):
            continue   # 🆕 ⑤b-4：3行からは句のあいだに飾りの線を引かない（字に触れる）
        if y > PP["y1"] - 30:
            continue
        g.append(F.line(PP["x0"] + 40, y, x1 - 40 - (k % 3) * 90, y, J.LINE_DIM, 6))
    for i, t in enumerate(d["lines"]):
        g.append(_tline(PP["x0"] + 40, _pp_line_y(i, n), t, 34, INK, "start", x1 - PP["x0"] - 80))
    return g


def paper_stage(prev, st):
    d = PP_DOC[st["doc"]]
    n, x1 = len(d["lines"]), _pp_x1(d)
    s = []
    for i, t in enumerate(d["lines"]):
        if _on(prev, st, f"hl{i + 1}"):
            # ⚠️ 門番 layout：字を描き直さない＝句の下に黄の線を引くだけ
            y = _pp_line_y(i, n)
            w = min(F.fm.width(t, 34), x1 - PP["x0"] - 80)
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
DV_YEAR = "2022"                  # 🆕 ⑤b-5（ca01）：残す年（USCG p235「While 7 of the 13 dives reached the TITANIC depth of 3840 m」）


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
    if _on(prev, st, "y22"):          # 🆕 ⑤b-5（ca01）：2022年の段だけを残し、ほかの年を地の色で薄める（字を描き直さない）
        for k, yr in enumerate(sorted(_yr_rows())):
            if yr != DV_YEAR:
                # ⚠️ geom_gap：上下 60px だと 2021年の帯が右上の札（y 302〜333）に 3px かかった＝点（半径 26）と年の札の高さ ±45px に
                s.append(F.rect(F.BX0 + 40, DV["ys"][k] - 45, F.BX1 - F.BX0 - 80, 90, J.BG, op=0.72))
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
    if _on(prev, st, "hit"):          # 🆕 ⑤b-5（ca02）：左舷の船首（船首が北＝上なら左の舷）に潜水艇の印がぶつかる（TSB 付録B「collided with the port bow」）
        x, y = bw_hit()
        pts = [(x + (30 if k % 2 == 0 else 12) * math.cos(math.pi * k / 6), y + (30 if k % 2 == 0 else 12) * math.sin(math.pi * k / 6)) for k in range(12)]
        s.append(F.circ(x - 64, y + 6, 26, SUBC) + F.poly(pts, J.ALERT, None, close=True))
    return s


def bw_hit():
    """🆕 ⑤b-5：左舷の船首の縁の点（船首の先から少し後ろ・左の縁）。"""
    tx, ty = BW_["tip"]
    return tx - BW_["w"] - 4, ty + 170.0


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
#  🆕 ⑤b-4（2026-10-15）：第4〜7章の見え方（記録の値は門番 check_mech の REC_M22 が別に持つ）
# ══════════════════════════════════════════════════════════
def _rc(r):
    """役の名（jiko_style.ROLE の名）か意味の色の名（"LINE" ほか）→ 色の値。"""
    return J.ROLE[r] if r in J.ROLE else getattr(J, r)


def _n_of(prev, st):
    return int(prev.get("n", "0")), int(st["n"])


#  send（c501）＝母船の画面から送り続けた文の印（帯の幅を10分とした模式の間隔）と、返事の無い潜水艇の段
SE = dict(x0=430.0, x1=1760.0, ys=(450.0, 690.0), min=10.0)
SE_N = 25                          # 帯の幅10分に25通＝1分に2.5回（NTSB p.17「sent two to three messages every minute」の間・模式）


def se_xs():
    dx = (SE["x1"] - SE["x0"] - 60.0) / (SE_N - 1)
    return [SE["x0"] + 30.0 + i * dx for i in range(SE_N)]


def send_base(st0):
    g = []
    for (nm, col), y in zip((("母船", SHIPC), ("潜水艇", SUBC)), SE["ys"]):
        g.append(F.line(SE["x0"], y, SE["x1"], y, J.LINE_DIM, 4))
        g.append(_tline(SE["x0"] - 30, y + 12, nm, 36, col, "end", 280))
    g.append(_arrow(SE["x0"], 800.0, SE["x1"], 800.0, J.LINE_DIM, 3, 16))
    g.append(_tline(SE["x1"] - 30, 782.0, "時間", 26, J.TICK, "end", 200))
    return g


def send_stage(prev, st):
    s = []
    if _on(prev, st, "send"):
        y = SE["ys"][0]
        for x in se_xs():
            s.append(F.rect(x - 15, y - 46, 30, 24, SHIPC, rx=4) + F.line(x, y - 16, x, y + 44, SHIPC, 2, dash="5 6"))
    if _on(prev, st, "none"):
        y = SE["ys"][1]
        s.append(_tline((SE["x0"] + SE["x1"]) / 2, y - 26, "返事なし", 38, J.TICK, "middle", 400))
    return s


#  proto（c502・c507）＝会社の手順の流れ（連絡が途絶える→浮き上がるのを待つ→近くの海面を探す→外に知らせる）と「海の上のならい」の段
PR = dict(xs=(300.0, 740.0, 1180.0, 1620.0), y=450.0, w=390.0, h=120.0, by=720.0, bx=1080.0, bw=760.0)
PR_T = (("連絡が途絶える", "LINE"), ("浮き上がるのを待つ", "company"), ("近くの海面を探す", "company"), ("外に知らせる", "company"))
PR_BEST = ("海の上のならい", "すぐ救難の当局へ")   # TSB §2.6「the maritime best practice of notifying SAR authorities as soon as possible」
#   ⚠️ 門番 echo：「できるだけ早く救難の当局へ」は語り「できるだけ早く救難の当局に知らせる」の写し＝12字未満に
PR_FIELD = (None, "wait", "search", "out")


def _pr_box(i):
    t, r = PR_T[i]
    return _box(PR["xs"][i], PR["y"], PR["w"], PR["h"], t, _rc(r), cap=32, sw=5)


def proto_base(st0):
    return [_tline(F.BX0 + 40.0, 300.0, "会社の手順（連絡が途絶えたとき）", 30, COC, "start", 800), _pr_box(0)]


def proto_stage(prev, st):
    s = []
    for i in (1, 2, 3):
        if _on(prev, st, PR_FIELD[i]):
            x0 = PR["xs"][i - 1] + PR["w"] / 2 + 4
            s.append(_arrow(x0, PR["y"], PR["xs"][i] - PR["w"] / 2 - 4, PR["y"], J.LINE, 5, 18) + _pr_box(i))
    if _on(prev, st, "best"):
        x, y = PR["xs"][0], PR["y"] + PR["h"] / 2 + 4
        bl = PR["bx"] - PR["bw"] / 2
        s.append(F.line(x, y, x, PR["by"], J.LINE, 5) + _arrow(x, PR["by"], bl - 6, PR["by"], J.LINE, 5, 18))
        s.append(_box(PR["bx"], PR["by"], PR["bw"], 120.0, PR_BEST[1], J.LINE, cap=34, sw=5))
        s.append(_tline(bl, PR["by"] - 78, PR_BEST[0], 30, INK, "start", 500))
    return s


#  none（c521・c816）＝欄が空（×）。rescue＝救助の備え（TSB §2.5）・told＝亀裂を知らせた先（USCG p162・p164）
NO = dict(rescue=dict(head="救助の備え", items=("水の中の位置を知る手段", "ROV の会社との救助の契約"), lay="col"),
          told=dict(head="亀裂のことを知らせた先", items=("客", "当局", "船級協会"), lay="row"),
          # 🆕 ⑤b-5：ca10（USCG p290「no effort was made to remove the TITAN’s insert or take the submersible temporarily out of service」）
          insp=dict(head="音のあとの調べ", items=("内張りを外して見る", "休ませて詳しく調べる"), lay="col"))


def no_xy(key, i):
    if NO[key]["lay"] == "col":
        return 1040.0, 450.0 + i * 200.0, 1000.0, 130.0
    return 480.0 + i * 480.0, 520.0, 380.0, 150.0


def none_base(st0):
    k = st0["set"]
    g = [_tline(F.BX0 + 40.0, 320.0, NO[k]["head"], 34, INK, "start", 800)]
    for i, t in enumerate(NO[k]["items"]):
        x, y, w, h = no_xy(k, i)
        g.append(_box(x, y, w, h, t, J.LINE, cap=36 if NO[k]["lay"] == "col" else 42, sw=4))
        if NO[k]["lay"] == "col":
            g.append(F.rect(x - w / 2 - 140, y - 40, 80, 80, J.BG, J.LINE, 4, rx=8))
    return g


def none_stage(prev, st):
    k = st["set"]
    s = []
    n0, n1 = _n_of(prev, st)
    for i in range(n0, n1):
        x, y, w, h = no_xy(k, i)
        s.append(_xmark(x - w / 2 - 100, y, 26, J.ALERT) if NO[k]["lay"] == "col" else _xmark(x, y + h / 2 + 64, 30, J.ALERT))
    return s


#  say（c705・c712・c718・c806）＝人の言葉。輪郭（顔は描かない）＋吹き出しの英字（報告書が引くまま・訳は字幕）。色＝話した人の役
SY = dict(px=360.0, ptop=330.0, ph=420.0, bx0=700.0, bx1=1790.0, by0=320.0)
SAY = dict(
    comp=dict(who="元運航部長の話", sub="CEO の考えとして", role="LINE", bubbles=(("“better in compression than tension”",),)),
    letter=dict(who="CEO", sub="会社の関係者への手紙", role="company",
                bubbles=(("there was no damage to the main cylindrical section,", "which is the critical part and a shape",
                          "that is far better understood"),)),
    tv=dict(who="CEO", sub="テレビの取材", role="company",
            bubbles=(("I’d like to be remembered as an innovator.",), ("I’ve broken some rules to make this.",))),
    rec=dict(who="CEO", sub="会合の録音", role="company",
             bubbles=(("there is not a lot of confidence on your part", "in the engineering that went into this vessel"),)),
    # 🆕 ⑤b-5：ca11（NTSB p1036「told the director of engineering, "Let's dive again and see what happens"」）
    again=dict(who="CEO", sub="データを見たあと", role="company", bubbles=(("“Let’s dive again and see what happens”",),)),
)
SY_CAP, SY_LH = 42.0, 60.0


def sy_box(key, i):
    """吹き出し i の枠（x0, y0, x1, y1）＝上から順に積む。"""
    y = SY["by0"]
    for j, lines in enumerate(SAY[key]["bubbles"]):
        h = 50.0 + SY_LH * len(lines)
        if j == i:
            return SY["bx0"], y, SY["bx1"], y + h
        y += h + 50.0
    raise ValueError(f"m22 say：吹き出し {i} は {key} に無い")


def say_base(st0):
    d = SAY[st0["set"]]
    col = _rc(d["role"])
    return [_person(SY["px"], SY["ptop"], SY["ph"], col),
            _tline(SY["px"], SY["ptop"] + SY["ph"] + 52, d["who"], 36, col, "middle", 480),
            _tline(SY["px"], SY["ptop"] + SY["ph"] + 90, d["sub"], 28, J.TICK, "middle", 520)]


def say_stage(prev, st):
    d = SAY[st["set"]]
    s = []
    n0, n1 = _n_of(prev, st)
    hx, hy = SY["px"] + SY["ph"] * 0.17 + 50, SY["ptop"] + SY["ph"] * 0.17
    for i in range(n0, n1):
        x0, y0, x1, y1 = sy_box(st["set"], i)
        ty = min(max(hy, y0 + 36), y1 - 36)
        s.append(F.poly([(x0 + 2, ty - 24), (hx, hy), (x0 + 2, ty + 24)], J.BG2, J.LINE, 4, close=True))
        s.append(F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 4, rx=24) + F.rect(x0 - 3, ty - 21, 9, 42, J.BG2))
        for k, t in enumerate(d["bubbles"][i]):
            s.append(_tline(x0 + 40, y0 + 13 + SY_LH * (k + 1), t, SY_CAP, INK, "start", x1 - x0 - 80))
    return s


#  layers（c610・c615・c619）＝筒の壁の断面（5枚の層・1＝いちばん内側＝NTSB p.41「layer 1, the innermost co-bonded layer」）
LY = dict(x0=600.0, x1=1440.0, y_in=780.0, th=84.0, icon=(330.0, 560.0, 140.0))
LY_N = 5
LY_IN_CM = 2.54                    # 1枚の厚さ＝1インチ（NTSB p.59「the five 1-inch-thick layers」）
LY_SEP = ((1, 2), (3, 4))          # 剥離した面（NTSB p.40「One delamination was between layers 1 and 2 and the other was between layers 3 and 4」）
LY_VOID = ((1, 2), (3, 4))         # 長い空隙が並んでいた面（NTSB p.59「these adhesive interfaces contained long extended voids」）
LY_GRIND = {1: 1, 2: 8, 3: 14, 4: 24}   # 🆕 ⑤b-5（c910）：削ったしわの数（USCG 図143＝p180 の表「Ground wrinkles」・5枚目は N/A）＝原寸で読んだ
LY_ICE = dict(x=1020.0, depth=150.0)     # 🆕 ⑤b-6（cb05）：凍る水のすき間（外側の面から・場所と深さは模式＝水が入った所は報告書に無い）


def ly_top(i):
    """層 i（1＝いちばん内側）の外側の縁の y（層 i と i+1 の境）。"""
    return LY["y_in"] - i * LY["th"]


def ice_top():
    """🆕 ⑤b-6（cb05）：凍る水のすき間の口の y（外側＝海の側の面）。"""
    return ly_top(LY_N)


def layers_base(st0):
    cx, cy, r = LY["icon"]
    g = [F.circ(cx, cy, r, "none", J.LINE_DIM, 26), F.rect(cx - 16, cy - r - 22, 32, 44, "none", J.AMBER, 4),
         F.line(cx + 16, cy - r - 22, LY["x0"] - 6, ly_top(LY_N), J.LINE_DIM, 2, dash="8 6"),
         F.line(cx + 16, cy - r + 22, LY["x0"] - 6, LY["y_in"], J.LINE_DIM, 2, dash="8 6"),
         _tline(cx, cy + r + 62, "筒の輪切り", 28, J.TICK, "middle", 260)]
    for i in range(1, LY_N + 1):
        # 🔧 ⑤b-4 の試し焼き：偶数の層を紺の固定色（#1c2c38）にしたら章の色（赤銅）に置き換わらず、別の材料に見えた＝章の色の LINE_DIM を薄く重ねる
        g.append(F.rect(LY["x0"], ly_top(i), LY["x1"] - LY["x0"], LY["th"], J.BG2, J.LINE_DIM, 3))
        if i % 2 == 0:
            g.append(F.rect(LY["x0"] + 2, ly_top(i) + 2, LY["x1"] - LY["x0"] - 4, LY["th"] - 4, J.LINE_DIM, op=0.30))
        g.append(_tline(LY["x1"] + 30, ly_top(i) + LY["th"] / 2 + 12, str(i), 34, INK, "start", 60))
    for i in range(1, LY_N):
        g.append(F.line(LY["x0"], ly_top(i), LY["x1"], ly_top(i), J.DOC, 3))
    x = LY["x1"] + 70     # 1枚の厚さの括弧（層の番号の右）。⚠️ 左に置くと輪切りから伸ばす破線が札を貫く
    g.append(F.line(x, ly_top(LY_N), x, ly_top(LY_N - 1), J.AMBER, 4) + F.line(x - 10, ly_top(LY_N), x + 10, ly_top(LY_N), J.AMBER, 4)
             + F.line(x - 10, ly_top(LY_N - 1), x + 10, ly_top(LY_N - 1), J.AMBER, 4))
    g.append(_tline(LY["x0"], ly_top(LY_N) - 24, "外側（海の水）", 28, J.TICK, "start", 300))
    g.append(_tline(LY["x0"], LY["y_in"] + 40, "内側（人が乗る側）", 28, J.TICK, "start", 360))
    g.append(_tline(LY["x1"] + 30, ly_top(LY_N) - 24, "層", 28, J.TICK, "start", 80))
    return g


def layers_stage(prev, st):
    s = []
    if _on(prev, st, "sep"):
        for a, _b in LY_SEP:
            y = ly_top(a)
            s.append(F.line(LY["x0"], y, LY["x1"], y, J.ALERT, 8) + _tline(LY["x1"] + 100, y + 11, "剥離", 32, J.ALERT, "start", 160))
    if _on(prev, st, "void"):
        for a, _b in LY_VOID:
            y = ly_top(a)
            for k in range(6):
                x = LY["x0"] + 90 + k * 140
                s.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{48 if k % 2 else 34}" ry="9" fill="{J.BG}" stroke="{J.INK_W}" stroke-width="2"/>')
        s.append(_tline(LY["x0"] + 24, ly_top(1) - 22, "長い空隙", 28, INK, "start", 200))
    if _on(prev, st, "grind"):        # 🆕 ⑤b-5（c910）：層ごとの「削ったしわ」の数（層の外側の面＝次の層を巻く前に削った面）。5枚目は数えていない
        s.append(_tline(LY["x1"] + 150, ly_top(LY_N) - 24, "削ったしわ", 28, J.AMBER, "start", 220))
        for i in range(1, LY_N + 1):
            n = LY_GRIND.get(i)
            y = ly_top(i)
            s.append(_tline(LY["x1"] + 190, y + LY["th"] / 2 + 12, "—" if n is None else str(n), 34, J.AMBER, "middle", 90))
            for k in range(n or 0):
                x = LY["x0"] + 20 + (k + 0.5) * (LY["x1"] - LY["x0"] - 40) / n
                s.append(F.poly([(x - 9, y + 2), (x, y + 13), (x + 9, y + 2)], "none", J.AMBER, 4))
    if _on(prev, st, "rub"):
        cx = (LY["x0"] + LY["x1"]) / 2
        s.append(_arrow(cx + 170, ly_top(1) - LY["th"] / 2 + 4, cx - 170, ly_top(1) - LY["th"] / 2 + 4, J.AMBER, 7, 26))
        s.append(_arrow(cx - 170, ly_top(1) + LY["th"] / 2 - 4, cx + 170, ly_top(1) + LY["th"] / 2 - 4, J.AMBER, 7, 26))
        for k in range(9):
            x = LY["x0"] + 80 + k * 85
            s.append(F.line(x, ly_top(1) - 5, x + 34, ly_top(1) + 5, J.AMBER, 3))
    if _on(prev, st, "ice"):          # 🆕 ⑤b-6（cb05）：外側（海の側）のすき間に入った水が凍ってふくらむ（NTSB p1060「If water had penetrated … and frozen」）
        x, y0, d = LY_ICE["x"], ice_top(), LY_ICE["depth"]
        s.append(F.poly([(x - 46, y0), (x + 46, y0), (x, y0 + d)], J.INK_W, J.INK_W, 3, close=True, op=0.55))
        for k in (-1, 1):
            s.append(_arrow(x + k * 30, y0 + d * 0.36, x + k * 120, y0 + d * 0.36, J.ALERT, 7, 24))
            s.append(F.line(x + k * 8, y0 + 10, x + k * 20, y0 + d * 0.5, J.BG, 3))
    return s


#  buckle（c617）＝厚い1枚が薄い2枚に分かれ（剥離）、外から押されて内へ曲がる（座屈）。動く部品＝2枚の板。曲がり方は模式
BK = dict(x0=560.0, x1=1360.0, top=470.0, th=120.0, gap=24.0, bow=66.0, n=24)


def bk_plate(y0, h, bow):
    xs = [BK["x0"] + (BK["x1"] - BK["x0"]) * i / BK["n"] for i in range(BK["n"] + 1)]
    u = [math.sin(math.pi * (x - BK["x0"]) / (BK["x1"] - BK["x0"])) for x in xs]
    top = [(x, y0 + bow * v) for x, v in zip(xs, u)]
    bot = [(x, y0 + h + bow * v) for x, v in reversed(list(zip(xs, u)))]
    return top + bot


def buckle_parts(st):
    sp, pr = st["split"] == "on", st["press"] == "on"
    h, g = BK["th"] / 2, (BK["gap"] if sp else 0.0)
    b = BK["bow"] if pr else 0.0
    return [_P("outer", "poly", bk_plate(BK["top"] - g / 2, h, b), fill=J.BG2, stroke=J.LINE, w=5),
            _P("inner", "poly", bk_plate(BK["top"] + h + g / 2, h, b), fill=J.BG2, stroke=J.LINE, w=5)]


BK_LAB = dict(out=470.0, inner=620.0)   # 外側・内側の札の y（板の左＝外側が上・内側が下＝内へ曲がる＝下へ）。⚠️ 板の上に置くと押す矢印が札を貫く


def buckle_base(st0):
    return [_tline(BK["x0"] - 30, BK_LAB["out"], "外側（海の水）", 28, J.TICK, "end", 260),
            _tline(BK["x0"] - 30, BK_LAB["inner"], "内側", 28, J.TICK, "end", 200)]


def buckle_stage(prev, st):
    s = []
    if _on(prev, st, "split"):
        s.append(_tline(BK["x0"] - 30, BK["top"] + BK["th"] / 2 + 10, "剥離", 30, J.ALERT, "end", 140))
    if _on(prev, st, "press"):
        for k in range(5):
            x = BK["x0"] + 120 + k * 140
            s.append(_arrow(x, 330.0, x, 420.0, J.LINE, 6, 22))
    return s


#  tc（c702）＝引っ張り（旅客機の胴体＝中の空気が外へ押す）と押しつぶし（深い海の殻＝外から押す）。USCG p.274
TC = dict(l=(470.0, 580.0), r=(1150.0, 580.0), R=140.0)
TC_SIDE = (("l", "air", "旅客機の胴体", "引っ張られる", True), ("r", "sea", "深い海の殻", "押しつぶされる", False))


def tc_arrows(cx, cy, R, outward):
    out = []
    for k in range(8):
        a = math.pi * 2 * k / 8 + math.pi / 8
        r0, r1 = (R * 0.30, R * 0.82) if outward else (R * 1.42, R * 1.12)
        out.append((cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)))
    return out


def tc_base(st0):
    return [F.circ(TC[k][0], TC[k][1], TC["R"], "none", J.LINE_DIM, 10) for k in ("l", "r")]


def tc_stage(prev, st):
    s = []
    for side, fld, head, word, outward in TC_SIDE:
        if _on(prev, st, fld):
            cx, cy = TC[side]
            s.append(F.circ(cx, cy, TC["R"], "none", J.LINE, 12))
            s += [_arrow(*a, J.LINE, 5, 18) for a in tc_arrows(cx, cy, TC["R"], outward)]
            s.append(_tline(cx, 344.0, head, 34, INK, "middle", 460))
            s.append(_tline(cx, 830.0, word, 36, J.AMBER, "middle", 460))
    return s


#  shell（c703・c704）＝ふつうの深海の潜水艇の殻（鋼かチタンの球）とタイタンの殻（炭素繊維の筒・両端はチタン）。TSB §1.13
SH = dict(l=(420.0, 570.0), rs=150.0, r=(1080.0, 570.0), cw=500.0, ch=210.0)
SH_L = ("ふつうの深海の潜水艇", "鋼かチタンの球")
SH_R = ("タイタン", "炭素繊維の筒")


def _hull_path(cx, cy, w, h):
    r, dm = h / 2, h * 0.30
    xa, xb = cx - w / 2 + dm, cx + w / 2 - dm
    return (f'M{xa:.1f} {cy - r:.1f} H{xb:.1f} A{dm:.1f} {r:.1f} 0 0 1 {xb:.1f} {cy + r:.1f} '
            f'H{xa:.1f} A{dm:.1f} {r:.1f} 0 0 1 {xa:.1f} {cy - r:.1f} Z'), xa, xb


def shell_base(st0):
    d, _, _ = _hull_path(SH["r"][0], SH["r"][1], SH["cw"], SH["ch"])
    return [F.circ(SH["l"][0], SH["l"][1], SH["rs"], "none", J.LINE_DIM, 4), f'<path d="{d}" fill="none" stroke="{J.LINE_DIM}" stroke-width="4"/>']


def shell_stage(prev, st):
    s = []
    if _on(prev, st, "left"):
        cx, cy = SH["l"]
        s.append(F.circ(cx, cy, SH["rs"], "#22323e", J.LINE, 10) + F.circ(cx - 46, cy - 50, 34, "#2e4352"))
        s.append(_tline(cx, 344.0, SH_L[0], 30, J.TICK, "middle", 460) + _tline(cx, 800.0, SH_L[1], 36, INK, "middle", 460))
    if _on(prev, st, "right"):
        cx, cy = SH["r"]
        d, xa, xb = _hull_path(cx, cy, SH["cw"], SH["ch"])
        s.append(f'<path d="{d}" fill="#262b30" stroke="{J.LINE}" stroke-width="10"/>')
        for x in (xa, xb):
            s.append(F.rect(x - 9, cy - SH["ch"] / 2 - 8, 18, SH["ch"] + 16, J.BG2, J.LINE, 3))
        s.append(_tline(cx, 344.0, SH_R[0], 30, J.TICK, "middle", 460) + _tline(cx, 800.0, SH_R[1], 36, INK, "middle", 460))
    return s


#  ruler（c706・c709・c713）＝深さの物差し（縦・縮尺どおり）。near＝0〜7,000m・far＝0〜14,000m。タイタニック（約3,800m）は基図
RL = dict(x=600.0, y0=330.0, y1=830.0, xr=1330.0, lx=1360.0)
RL_Z = dict(near=7000.0, far=14000.0, mid=4500.0)          # 🆕 ⑤b-5：mid＝0〜4,500m（650m と 1,000m の札が重ならない尺）
RL_TK = dict(near=tuple(range(0, 7001, 1000)), far=tuple(range(0, 14001, 2000)), mid=tuple(range(0, 4001, 1000)))
RL_M = dict(goal=(6000.0, "会社の望み", "company"),          # TSB §1.12.1「rated up to 6000 m」
            op=(4500.0, "運航の目標", "company"),              # USCG p.114「the 4,500 m … target max pressure depth for TITAN’s operations」
            fail=(13200.0, "壊れる深さの計算", "company"),     # NTSB p.25「an implosion depth about 13,200 meters」
            # 🆕 ⑤b-5（c921・c923）：NTSB p.30「to a simulated maximum depth of 4,200 meters」・USCG p.278「a depth of only 650 m」・
            #   NTSB p.30「an acrylic window certified to 1,000 meters」（色＝その値を書いた調べ）
            #   🔧 試し焼き：数を札（右の列）に別に出すと、縮尺どおりの物差しの別の深さの高さに数が並んだ＝数は線の札そのものに書く（門番が記録と照らす）
            test=(4200.0, "試験で最も深い 4,200メートル", "company"),      # ⚠️ 門番 dup：「加圧の試験」は c921 の見出し
            w650=(650.0, "最初の窓の等級 約650メートル", "uscg"),
            w1k=(1000.0, "別の記述 1,000メートル", "ntsb"))
RL_RATIO = dict(x=1060.0, w=70.0, bx=1150.0, bw=60.0)


def rl_y(z, m):
    return RL["y0"] + (RL["y1"] - RL["y0"]) * m / RL_Z[z]


def ruler_base(st0):
    z = st0["z"]
    g = [F.line(RL["x"] - 20, RL["y0"], RL["xr"], RL["y0"], SEA_LN, 5), _tline(RL["lx"], RL["y0"] + 10, "海面", 28, J.TICK, "start", 200),
         F.line(RL["x"], RL["y0"], RL["x"], RL["y1"], J.LINE_DIM, 4), _tline(RL["x"] - 16, RL["y0"] - 26, "深さ（メートル）", 26, J.TICK, "end", 360)]
    for m in RL_TK[z][1:]:
        y = rl_y(z, m)
        g.append(F.line(RL["x"] - 12, y, RL["x"], y, J.LINE_DIM, 3) + _tline(RL["x"] - 20, y + 9, f"{m:,}", 26, J.TICK, "end", 160))
    y = rl_y(z, TITANIC_M)
    g.append(F.line(RL["x"], y, RL["xr"], y, J.TICK, 4, dash="14 10") + _tline(RL["lx"], y + 10, "タイタニック", 30, J.TICK, "start", 300))
    return g


def ruler_stage(prev, st):
    z, s = st["z"], []
    for k, (m, t, r) in RL_M.items():
        if _on(prev, st, k):
            y, c = rl_y(z, m), _rc(r)
            s.append(F.line(RL["x"], y, RL["xr"], y, c, 7) + _tline(RL["lx"], y + 11, t, 32, c, "start", 440))
    if _on(prev, st, "ratio"):
        h = rl_y(z, TITANIC_M) - RL["y0"]
        for k in range(3):
            s.append(F.rect(RL_RATIO["x"], RL["y0"] + k * h, RL_RATIO["w"], h, "none", J.TICK, 3, dash="8 6"))
        s.append(F.rect(RL_RATIO["bx"], RL["y0"], RL_RATIO["bw"], rl_y(z, RL_M["fail"][0]) - RL["y0"], COC, op=0.55))
    return s   # ⚠️ 模型の試験の深さは3冊で割れる＝箱や棒で描かない（札「模型の試験は届かず」だけ＝映像方針 c713）


#  sf（c707）＝安全率のしくみ（潜ってよい深さと壊れる深さの棒・その比）。🔴 長さは模式（値ではない）＝NTSB p.24 の定義だけ
SF = dict(x0=560.0, ys=(470.0, 650.0), h=74.0, op=380.0, k=2.0)


def sf_base(st0):
    g = []
    for y, t in zip(SF["ys"], ("潜ってよい深さ", "壊れる深さ")):
        g.append(_tline(SF["x0"] - 24, y + 12, t, 34, INK, "end", 460))
        g.append(F.rect(SF["x0"], y - SF["h"] / 2, SF["op"] * SF["k"] + 40, SF["h"], "none", J.LINE_DIM, 3, rx=6, dash="10 8"))
    return g


def sf_stage(prev, st):
    s = []
    x0, (y0, y1), h = SF["x0"], SF["ys"], SF["h"]
    if _on(prev, st, "bars"):
        s.append(F.rect(x0, y0 - h / 2, SF["op"], h, J.LINE, rx=6) + F.rect(x0, y1 - h / 2, SF["op"] * SF["k"], h, J.ALERT, rx=6, op=0.85))
    if _on(prev, st, "ratio"):
        for i in range(int(SF["k"])):
            a, b = x0 + SF["op"] * i, x0 + SF["op"] * (i + 1)
            yb = y1 - h / 2 - 16
            s.append(F.line(a + 4, yb, b - 4, yb, J.AMBER, 4) + F.line(a + 4, yb, a + 4, yb + 12, J.AMBER, 4) + F.line(b - 4, yb, b - 4, yb + 12, J.AMBER, 4))
    if _on(prev, st, "spare"):
        s.append(F.rect(x0 + SF["op"], y1 - h / 2 - 6, SF["op"] * (SF["k"] - 1), h + 12, "none", J.AMBER, 6, rx=6, dash="12 8"))
    return s


#  model（c711）＝3分の1の模型（炭素繊維の筒と炭素繊維のドーム）・外からの圧・ドームの1つが壊れた（どちらのドームかは模式）。TSB §1.12.1
MD = dict(cx=880.0, cy=570.0, w=560.0, h=200.0)
MD_DOME_M = 3000.0                 # ドームが壊れた圧の深さ（TSB §1.12.1「failed at pressures equivalent to depths of around 3000 m」）


def model_base(st0):
    d, xa, xb = _hull_path(MD["cx"], MD["cy"], MD["w"], MD["h"])
    return [f'<path d="{d}" fill="#262b30" stroke="{J.LINE}" stroke-width="6"/>',
            F.line(xa, MD["cy"] - MD["h"] / 2, xa, MD["cy"] + MD["h"] / 2, J.LINE_DIM, 3),
            F.line(xb, MD["cy"] - MD["h"] / 2, xb, MD["cy"] + MD["h"] / 2, J.LINE_DIM, 3),
            _tline(MD["cx"], MD["cy"] + 12, "炭素繊維の筒", 32, INK, "middle", 300),
            _tline(MD["cx"], 800.0, "両端のドームも炭素繊維", 30, J.TICK, "middle", 600)]


def model_stage(prev, st):
    s = []
    cx, cy, w, h = MD["cx"], MD["cy"], MD["w"], MD["h"]
    if _on(prev, st, "press"):
        for k in range(4):
            x = cx - w / 2 + 110 + k * (w - 220) / 3
            s.append(_arrow(x, cy - h / 2 - 90, x, cy - h / 2 - 14, J.LINE, 5, 18) + _arrow(x, cy + h / 2 + 90, x, cy + h / 2 + 14, J.LINE, 5, 18))
        s.append(_arrow(cx - w / 2 - 110, cy, cx - w / 2 - 14, cy, J.LINE, 5, 18) + _arrow(cx + w / 2 + 110, cy, cx + w / 2 + 14, cy, J.LINE, 5, 18))
    if _on(prev, st, "fail"):
        _, _, xb = _hull_path(cx, cy, w, h)
        dm = h * 0.30
        s.append(f'<path d="M{xb:.1f} {cy - h / 2:.1f} A{dm:.1f} {h / 2:.1f} 0 0 1 {xb:.1f} {cy + h / 2:.1f} Z" fill="{J.ALERT}" fill-opacity="0.55" '
                 f'stroke="{J.ALERT}" stroke-width="6"/>')
        s.append(F.poly([(xb + 6, cy - 60), (xb + 30, cy - 20), (xb + 12, cy + 10), (xb + 40, cy + 50)], "none", J.INK_W, 4))
    return s


#  klass（c714）＝船級のしくみ（船の持ち主→船級協会〈民間の団体〉が設計・工事を確かめ、試験に立ち会う→証明書）。NTSB p.22
KL = dict(own=(280.0, 430.0), soc=(900.0, 430.0), cert=(1560.0, 430.0), w=400.0, h=130.0, cy=660.0, cxs=(560.0, 900.0, 1240.0))
KL_CHK = ("設計を確かめる", "工事を確かめる", "試験に立ち会う")
KL_SOC = ("船級協会", "民間の団体")
KL_CERT = "証明書"


def _kl_chk(i):
    x, y = KL["cxs"][i], KL["cy"]
    return (F.line(KL["soc"][0], KL["soc"][1] + KL["h"] / 2 + 4, x, y - 54, J.LINE_DIM, 3)
            + _box(x, y, 300.0, 100.0, KL_CHK[i], J.AMBER, cap=30, sw=4))


def klass_base(st0):
    return [_box(KL["own"][0], KL["own"][1], 340.0, KL["h"], "船の持ち主", J.LINE, cap=34, sw=5)]


def klass_stage(prev, st):
    s = []
    if _on(prev, st, "soc"):
        s.append(_arrow(KL["own"][0] + 176, KL["own"][1], KL["soc"][0] - KL["w"] / 2 - 6, KL["soc"][1], J.LINE, 5, 18))
        s.append(_box(KL["soc"][0], KL["soc"][1], KL["w"], KL["h"], KL_SOC[0], J.LINE, cap=36, sw=6, t2=KL_SOC[1]))
    if _on(prev, st, "design"):
        s += [_kl_chk(0), _kl_chk(1)]
    if _on(prev, st, "test"):
        s.append(_kl_chk(2))
    if _on(prev, st, "cert"):
        s.append(_arrow(KL["soc"][0] + KL["w"] / 2 + 6, KL["soc"][1], KL["cert"][0] - 150 - 6, KL["cert"][1], J.LINE, 5, 18))
        s.append(_box(KL["cert"][0], KL["cert"][1], 300.0, KL["h"], KL_CERT, J.DOC, ink=J.DOC, cap=38, sw=6))
    return s


#  wind（c801）＝筒の作り方（炭素繊維の糸が樹脂の槽をくぐり、回る芯に巻きつく＝フィラメント・ワインディング）。TSB §1.12.1
WD = dict(sp=(300.0, 430.0, 70.0), bath=(720.0, 660.0, 320.0, 120.0), man=(1330.0, 470.0, 760.0, 190.0))


def wind_base(st0):
    sx, sy, sr = WD["sp"]
    bx, by, bw, bh = WD["bath"]
    mx, my, mw, mh = WD["man"]
    return [F.circ(sx, sy, sr, J.BG2, J.LINE, 6), F.circ(sx, sy, 16, J.LINE), _tline(sx, sy + sr + 56, "炭素繊維の糸", 30, INK, "middle", 300),
            F.rect(bx - bw / 2, by - bh / 2, bw, bh, "none", J.LINE, 5, rx=8), F.rect(bx - bw / 2 + 6, by - bh / 2 + 34, bw - 12, bh - 40, "#5a4a2a"),
            _tline(bx, by + bh / 2 + 50, "樹脂の槽", 30, INK, "middle", 300),
            F.line(mx - mw / 2 - 50, my, mx + mw / 2 + 40, my, J.LINE_DIM, 6), F.rect(mx - mw / 2, my - mh / 2, mw, mh, J.BG2, J.LINE_DIM, 4, rx=10),
            _tline(mx, my + mh / 2 + 56, "回る芯", 30, INK, "middle", 300)]


def wind_stage(prev, st):
    s = []
    if _on(prev, st, "run"):
        sx, sy, sr = WD["sp"]
        bx, by, bw, bh = WD["bath"]
        mx, my, mw, mh = WD["man"]
        s.append(F.poly([(sx + sr * 0.7, sy + sr * 0.7), (bx - 60, by + 20), (bx + 60, by + 20), (mx - mw / 2 + 20, my - mh / 2 + 10)], "none", J.INK_W, 4))
        for k in range(14):
            x = mx - mw / 2 + 30 + k * 50
            s.append(F.line(x, my - mh / 2 + 6, min(x + 70, mx + mw / 2 - 6), my + mh / 2 - 6, "#6d7a84", 5))
        r = 110.0
        a0, a1 = math.radians(-50), math.radians(50)
        xr = mx + mw / 2 - 30
        s.append(f'<path d="M{xr + r * math.cos(a0) * 0.5:.1f} {my + r * math.sin(a0):.1f} A{r * 0.5:.1f} {r:.1f} 0 0 1 '
                 f'{xr + r * math.cos(a1) * 0.5:.1f} {my + r * math.sin(a1):.1f}" fill="none" stroke="{J.AMBER}" stroke-width="6"/>')
        tx, ty = xr + r * math.cos(a1) * 0.5, my + r * math.sin(a1)
        s.append(F.poly([(tx - 18, ty - 6), (tx + 8, ty + 14), (tx - 22, ty + 22)], J.AMBER, None, close=True))
    return s


#  meet（c805）＝2018年1月19日の会合の席（CEO・運航部長・社員3人＝TSB §1.12.1）と、CEO の録音（USCG p.149）。人は札だけ（顔を描かない）
MT = dict(tb=(960.0, 600.0, 620.0, 170.0), w=180.0, h=74.0, rec=(520.0, 750.0))
MT_SEATS = (("CEO", 520.0, 600.0), ("運航部長", 1400.0, 600.0), ("社員", 760.0, 440.0), ("社員", 960.0, 440.0), ("社員", 1160.0, 440.0))


def meet_base(st0):
    cx, cy, w, h = MT["tb"]
    g = [F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, J.LINE_DIM, 4, rx=40)]
    for i, (t, x, y) in enumerate(MT_SEATS):
        g.append(_box(x, y, MT["w"], MT["h"], t, COC, cap=30, sw=8 if i == 0 else 4))
    return g


def meet_stage(prev, st):
    s = []
    if _on(prev, st, "rec"):
        x, y = MT["rec"]
        s.append(F.line(x, MT_SEATS[0][2] + MT["h"] / 2 + 4, x, y - 30, J.LINE_DIM, 3) + F.rect(x - 60, y - 30, 120, 60, J.BG2, J.AMBER, 4, rx=8)
                 + F.circ(x - 32, y, 13, J.AMBER) + _tline(x + 18, y + 10, "録音", 26, INK, "middle", 70))
    return s


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-10-15）：第8〜9章の見え方（記録の値は門番 check_mech の REC_M22 が別に持つ）
# ══════════════════════════════════════════════════════════
#  cards（c901・c902・c903・c905・c907・c920・c922・ca21・ca22・ca25）＝札の箱の並び（row＝横に並べる・flow＝矢印でつなぐ）。
#    箱＝(題, 中身, 役の色, 絵, 印)。題は基図に1回だけ・明るくする段は枠・中身・絵・印（n＝左から明るくした箱の数＝戻さない）。
#    ⚠️ 門番 echo：字は12字未満（語りの写しにしない）。原文＝USCG p118・p174（材料）・NTSB p1027〜p1028・p1062（2020年の模型2つ＝1つ目は壊れ、
#    2つ目は約2,500mで「壊れると分かって」止めた）・TSB §1.12.2（1層ずつ固める）・TSB §1.16（疲れの寿命）・TSB §1.12.2／§2.1（2つの道）・
#    USCG p289／NTSB p1059／TSB §1.10.10.1（3つの見方）・NTSB p1031／p1064／p1065（警告の基準）
CD = dict(
    wind2=dict(lay="row", cards=(("1つ目の筒", "樹脂の槽をくぐる糸", "LINE", "bath", None),
                                 ("2つ目の筒", "樹脂を含ませたテープ", "sub", "tape", None))),
    mat=dict(lay="row", cards=(("1つ目の筒の糸", "三菱ケミカル系", "LINE", "spool", None),
                               ("2つ目の筒のテープ", "東レの米国の会社", "sub", "tape", None),
                               ("期限切れの安い材料", "3つの報告書に無い", "ALERT", None, "x"))),
    m20=dict(lay="row", cards=(("1つ目の模型", "壊れた", "ALERT", "hull_x", None),
                               ("2つ目の模型", "寸前で試験を止めた", "ALERT", "hull_crack", None))),
    #   ⚠️ 門番 box：中身の無い箱（題だけ）は内側の空きが33%＝TSB §1.12.2 の手順の中身を足した（wound onto a … mandrel・vacuum bagged and cured・
    #      a layer of adhesive was applied・the next layer was added）
    cure=dict(lay="flow", cards=(("1層を巻く", "テープを巻く", "INK_W", None, None), ("固める", "真空の袋で", "INK_W", None, None),
                                 ("接着剤の膜", "表面に塗る", "INK_W", None, None), ("次の層へ", "上に重ねる", "INK_W", None, None)), loop="5回くり返す"),
    life=dict(lay="row", cards=(("いちばん強い試料", "耐えた見込み", "tsb", "check", None),
                                ("いちばん弱い試料", "82%超を使った可能性", "ALERT", "gauge", None))),
    path=dict(lay="row", cards=(("壊れるまでの回数", "", "LINE", None, "q"), ("音の監視", "その場で分かる", "company", None, None))),
    views=dict(lay="row", cards=(("米沿岸警備隊", "強く示す", "uscg", None, None), ("米運輸安全委員会", "可能性が高い", "ntsb", None, None),
                                 ("カナダの調べ", "決められない", "tsb", None, None))),
    base=dict(lay="flow", cards=(("1つ目の船体と模型", "その音を使う", "company", None, None), ("警告の基準", "30回で黄・50回で赤", "company", None, None),
                                 ("2つ目の船体", "警告にならず", "sub", None, "x"))),
    # 🆕 ⑤b-6（2026-10-15）：cb13＝引かれたことの影響（USCG p295「further weakened」・TSB §2.1.3「may have exacerbated existing damage」＝米運輸安全委員会の
    #   「their actual effects are unknown」（NTSB p1060）は語りに無い＝note で）／cc08＝カナダの調べの勧告6つ（TSB §4.2.1〜§4.2.4＝6つとも「the Department of
    #   Transport」）／cd02〜cd04＝c107 の3つの問い（語りの言葉のまま）と答え（NTSB p1074・TSB §2.1／USCG p290／USCG p307・NTSB p1074・TSB §3.1）
    tow=dict(lay="row", cards=(("米沿岸警備隊", "さらに弱った", "uscg", None, None), ("カナダの調べ", "傷を広げたかも", "tsb", None, None))),
    rec6=dict(lay="row", cards=tuple((f"M26-0{k}", "運輸省へ", "tsb", None, None) for k in range(2, 8))),
    q3=dict(lay="row", cards=(("何が壊れたのか", "窓でなく炭素繊維の側", "sub", None, None), ("なぜ潜り続けたのか", "調べずに続けた", "company", None, None),
                              ("誰なら止められたのか", "まず会社自身", "company", None, None))),
)
CD_LIFE = 0.82                    # いちばん弱い試料で使った疲れの寿命（TSB §1.16「more than 82% of its fatigue life」＝ゲージの塗り）
CD_ROW = dict(y=560.0, h_ic=430.0, h=220.0, x0=170.0, x1=1750.0, gap=60.0, wmax=460.0, wmax_t=380.0)   # 絵の無い組＝幅380・高さ220（門番 box）
CD_FLOW = dict(y=520.0, h=170.0, x0=150.0, x1=1770.0, gap=110.0, wmax=380.0, loop=150.0)


def _cd_has(key, j):
    return any(c[j] for c in CD[key]["cards"])


def cd_xy(key, i):
    """箱 i の (cx, cy, w, h)。"""
    d = CD[key]
    k = len(d["cards"])
    G = CD_ROW if d["lay"] == "row" else CD_FLOW
    wmax = G["wmax_t"] if d["lay"] == "row" and not _cd_has(key, 3) else G["wmax"]
    w = min(wmax, (G["x1"] - G["x0"] - G["gap"] * (k - 1)) / k)
    span = w * k + G["gap"] * (k - 1)
    cx = (G["x0"] + G["x1"]) / 2 - span / 2 + w / 2 + i * (w + G["gap"])
    h = G["h"] if d["lay"] == "flow" or not _cd_has(key, 3) else G["h_ic"]
    return cx, G["y"], w, h


def _cd_ty(key, i):
    cx, cy, w, h = cd_xy(key, i)
    if CD[key]["lay"] == "flow":
        return cy - 14 if _cd_has(key, 1) else cy + 12
    return cy - h / 2 + 58 if _cd_has(key, 3) else cy - 40


def _cd_by(key, i):
    cx, cy, w, h = cd_xy(key, i)
    if CD[key]["lay"] == "flow":
        return cy + 46
    return cy + h / 2 - 36 if _cd_has(key, 3) else cy + 50


def _cd_icon(ic, cx, cy, c):
    """箱の中の絵（模式）。"""
    if ic in ("bath", "spool"):
        g = [F.circ(cx - 130, cy - 40, 44, J.BG2, c, 5), F.circ(cx - 130, cy - 40, 14, c)]
        if ic == "bath":
            g.append(F.poly([(cx - 60, cy - 10), (cx - 60, cy + 60), (cx + 60, cy + 60), (cx + 60, cy - 10)], "none", c, 5))
            g.append(F.rect(cx - 56, cy + 14, 112, 42, c, op=0.35))
            g.append(F.poly([(cx - 96, cy - 62), (cx - 20, cy + 40), (cx + 20, cy + 40), (cx + 110, cy - 40)], "none", c, 3))
            g.append(F.rect(cx + 100, cy - 80, 60, 80, J.BG2, c, 4, rx=6))
        else:
            for k in range(3):
                g.append(F.line(cx - 86, cy - 64 + k * 24, cx + 140, cy - 40 + k * 30, c, 3))
        return "".join(g)
    if ic == "tape":
        return (F.circ(cx - 110, cy - 30, 62, J.BG2, c, 5) + F.circ(cx - 110, cy - 30, 22, "none", c, 4)
                + F.poly([(cx - 110, cy + 32), (cx + 120, cy + 32), (cx + 120, cy + 4), (cx - 60, cy + 4)], c, None, close=True, op=0.75)
                + F.rect(cx + 104, cy - 80, 60, 116, J.BG2, c, 4, rx=6))
    if ic in ("hull_x", "hull_crack"):
        d, xa, xb = _hull_path(cx, cy - 10, 280, 112)
        g = [f'<path d="{d}" fill="{J.BG2}" stroke="{J.LINE}" stroke-width="5"/>']
        if ic == "hull_x":
            g.append(f'<path d="{d}" fill="{c}" fill-opacity="0.35" stroke="none"/>')
            g.append(F.poly([(cx - 70, cy - 66), (cx - 30, cy - 20), (cx - 50, cy + 10), (cx - 10, cy + 46)], "none", c, 7))
            g.append(F.poly([(cx + 40, cy - 60), (cx + 70, cy - 24), (cx + 46, cy + 4)], "none", c, 7))
        else:
            g.append(F.poly([(cx - 40, cy - 66), (cx - 16, cy - 36), (cx - 30, cy - 12)], "none", c, 5))
        return "".join(g)
    if ic == "check":
        return _check(cx, cy - 10, 54, c)
    if ic == "gauge":
        x0, w, y = cx - 170, 340.0, cy - 30
        return (_tline(x0, y - 22, "疲れの寿命", 26, J.TICK, "start", 200) + F.rect(x0, y, w, 50, J.BG2, J.LINE, 4, rx=6)
                + F.rect(x0 + 3, y + 3, (w - 6) * CD_LIFE, 44, c, op=0.85) + _arrow(x0 + w * CD_LIFE, y + 80, x0 + w * CD_LIFE + 70, y + 80, c, 5, 18))
    raise ValueError(f"m22 cards：知らない絵 {ic!r}")


def cards_base(st0):
    key = st0["set"]
    d = CD[key]
    g = []
    for i, (t, _b, _r, _ic, _mk) in enumerate(d["cards"]):
        cx, cy, w, h = cd_xy(key, i)
        g.append(F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, J.LINE_DIM, 4, rx=14))
        g.append(_tline(cx, _cd_ty(key, i), t, 34, INK, "middle", w - 40))
        if d["lay"] == "flow" and i + 1 < len(d["cards"]):
            nx, _, nw, _ = cd_xy(key, i + 1)
            g.append(_arrow(cx + w / 2 + 12, cy, nx - nw / 2 - 12, cy, J.LINE, 5, 20))
    return g


def cards_stage(prev, st):
    key = st["set"]
    d = CD[key]
    s = []
    n0, n1 = _n_of(prev, st)
    for i in range(n0, n1):
        _t, b, r, ic, mk = d["cards"][i]
        cx, cy, w, h = cd_xy(key, i)
        c = _rc(r)
        s.append(F.rect(cx - w / 2, cy - h / 2, w, h, "none", c, 7, rx=14))
        if ic:
            s.append(_cd_icon(ic, cx, cy - 10, c))
        if mk == "x":
            s.append(_xmark(cx, cy + 10, 50, J.ALERT, 12) if d["lay"] == "row" else _xmark(cx + w / 2 - 34, cy - h / 2 + 34, 16, J.ALERT, 7))
        if mk == "q":
            s.append(_qmark(cx, cy + 40, 90, INK) if not _cd_has(key, 3) else _qmark(cx, cy + 20, 120, INK))
        if b:
            s.append(_tline(cx, _cd_by(key, i), b, 36 if d["lay"] == "row" else 30, INK if r == "LINE" else c, "middle", w - 40))
    if _on(prev, st, "loop") and d.get("loop"):
        k = len(d["cards"])
        (xa, cy, _, h), (xb, _, _, _) = cd_xy(key, 0), cd_xy(key, k - 1)
        yb, yl = cy + h / 2 + 8, cy + h / 2 + CD_FLOW["loop"]
        s.append(F.poly([(xb, yb), (xb, yl), (xa, yl)], "none", J.AMBER, 5) + _arrow(xa, yl, xa, yb + 4, J.AMBER, 5, 20))
        s.append(_tline((xa + xb) / 2, yl + 44, d["loop"], 32, J.AMBER, "middle", 400))
    return s


#  groove（c912）＝チタンの輪の溝（断面）と、思ったより厚い筒の端。幅は縮尺どおり（1センチ＝40画素）。
#    原文 NTSB p1043「could only accommodate a 5-inch-thick cylinder」「the two trimmed cylinder ends were 5.166 inches and 5.175 inches thick」
#    「The excess thickness necessitated trimming the outer diameter of the cylinder」＝内側が左・外側（海の側）が右
GV = dict(x0=620.0, y_ch=600.0, px_cm=40.0, wall=44.0, depth=110.0, top=360.0)   # depth 110＝下の寸法の札を出典の行（y 886）から離す
GV_IN = 5.0                       # 溝が受け入れる厚さ（インチ）
GV_END_IN = 5.166                 # 切り落とした端の厚さ（インチ・薄い方）


def gv_px(inch):
    return inch * 2.54 * GV["px_cm"]


def groove_base(st0):
    x0, y, d, wl = GV["x0"], GV["y_ch"], GV["depth"], GV["wall"]
    x1 = x0 + gv_px(GV_IN)
    g = [F.rect(x0 - wl, y, wl, d + wl, J.LINE_DIM, J.LINE, 3), F.rect(x1, y, wl, d + wl, J.LINE_DIM, J.LINE, 3),
         F.rect(x0 - wl, y + d, x1 - x0 + 2 * wl, wl, J.LINE_DIM, J.LINE, 3)]
    yd = y + d + wl + 40
    g.append(F.line(x0, yd, x1, yd, J.AMBER, 3) + F.line(x0, yd - 12, x0, yd + 12, J.AMBER, 3) + F.line(x1, yd - 12, x1, yd + 12, J.AMBER, 3))
    g.append(_tline((x0 + x1) / 2, yd + 42, f"溝の幅 約{GV_IN * 2.54:.1f}センチ（{GV_IN:g}インチ）", 30, J.AMBER, "middle", 640))
    g.append(_tline(x0 - wl - 30, y + d / 2 + 10, "チタンの輪", 30, J.TICK, "end", 300))
    g.append(_tline(x0 - wl - 30, GV["top"] + 60, "内側", 30, J.TICK, "end", 160) + _tline(x1 + wl + 30, GV["top"] + 60, "外側（海）", 30, J.TICK, "start", 260))
    return g


def groove_stage(prev, st):
    s = []
    x0, y = GV["x0"], GV["y_ch"]
    xe = x0 + gv_px(GV_END_IN)
    if _on(prev, st, "thick"):
        s.append(F.rect(x0, GV["top"], xe - x0, y - GV["top"], J.BG2, INK, 4))
        for k in range(1, 5):
            x = x0 + (xe - x0) * k / 5
            s.append(F.line(x, GV["top"] + 4, x, y - 4, J.LINE_DIM, 2))
        for k in range(14):
            s.append(F.circ(x0 + 30 + (k * 37) % (xe - x0 - 60), GV["top"] + 30 + (k * 53) % (y - GV["top"] - 60), 4, J.TICK))
        s.append(F.line(x0, GV["top"] - 20, xe, GV["top"] - 20, INK, 3) + F.line(x0, GV["top"] - 32, x0, GV["top"] - 8, INK, 3)
                 + F.line(xe, GV["top"] - 32, xe, GV["top"] - 8, INK, 3))
    if _on(prev, st, "cut"):
        x1 = x0 + gv_px(GV_IN)
        s.append(F.rect(x1, GV["top"], xe - x1, y - GV["top"], J.ALERT, op=0.85))
        s.append(_arrow(xe + 150, GV["top"] + 140, xe + 14, GV["top"] + 140, J.ALERT, 6, 22))
    return s


#  coupons（c915）＝2つ目の筒の端材を18の試料に切る（長さの向き9・周りの向き9）。TSB §1.15「18 samples, 9 in the axial direction and 9 in the
#    circumferential direction」。形と並びは模式（数は記録）。色＝カナダの研究所
CPN = dict(x0=440.0, x1=1480.0, y0=400.0, y1=760.0)
CP_N = (9, 9)                     # (長さの向き, 周りの向き)


def cp_rects():
    """[(向き, x, y, w, h)]＝左半分に縦長9（長さの向き）・右半分に横長9（周りの向き）。"""
    x0, x1, y0, y1 = CPN["x0"], CPN["x1"], CPN["y0"], CPN["y1"]
    xm = (x0 + x1) / 2
    out = []
    na, nc = CP_N
    for k in range(na):
        out.append(("axial", x0 + 30 + k * (xm - x0 - 60) / na, y0 + 30, (xm - x0 - 60) / na - 14, y1 - y0 - 60))
    for k in range(nc):
        out.append(("circ", xm + 30, y0 + 24 + k * (y1 - y0 - 48) / nc, x1 - xm - 60, (y1 - y0 - 48) / nc - 10))
    return out


def coupons_base(st0):
    x0, x1, y0, y1 = CPN["x0"], CPN["x1"], CPN["y0"], CPN["y1"]
    return [F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, J.LINE, 4, rx=8), F.line((x0 + x1) / 2, y0 + 10, (x0 + x1) / 2, y1 - 10, J.LINE_DIM, 3, dash="10 8"),
            _arrow(x0 - 60, y1, x0 - 60, y1 - 160, J.LINE, 4, 18), _tline(x0 - 80, y1 - 60, "筒の長さ", 26, J.TICK, "end", 200),
            _arrow(x0, y1 + 46, x0 + 180, y1 + 46, J.LINE, 4, 18), _tline(x0 + 200, y1 + 56, "筒の周り", 26, J.TICK, "start", 200)]


def coupons_stage(prev, st):
    s = []
    if _on(prev, st, "cut"):
        for _k, x, y, w, h in cp_rects():
            s.append(F.rect(x, y, w, h, TSC, TSC, 3, op=0.85))
    return s


#  shelf（c918）＝棚のたとえ（いつも100キロを載せる棚＝基準の安全率 1.25 なら125キロまで／この筒の周りの向き 1.11＝111キロまで）。
#    たとえの数は安全率の比で計算する（記録の値＝TSB §1.12.2「changed its safety factor to 1.25」・§1.15「the calculated safety factor was 1.11」）
SV = dict(sx0=250.0, sx1=780.0, sy=640.0, gx=1150.0, gy0=800.0, gy1=330.0, kmax=130.0, lx=1530.0)   # lx＝線の右の札（右の端 1848 の内）
SV_LOAD = 100.0                   # たとえの棚にいつも載せる重さ（キロ）
SV_REQ = 1.25
SV_CIRC = 1.11


def sv_y(k):
    return SV["gy0"] - (SV["gy0"] - SV["gy1"]) * k / SV["kmax"]


def sv_lab(sf):
    return f"{round(SV_LOAD * sf):d}キロまで"


def shelf_base(st0):
    g = [F.line(SV["sx0"] - 20, 330.0, SV["sx0"] - 20, SV["sy"] + 120, J.LINE, 6),
         F.rect(SV["sx0"], SV["sy"], SV["sx1"] - SV["sx0"], 26, J.BG2, J.LINE, 4),
         F.poly([(SV["sx0"] - 20, SV["sy"] + 26), (SV["sx0"] + 90, SV["sy"] + 26), (SV["sx0"] - 20, SV["sy"] + 110)], "none", J.LINE, 4),
         _tline((SV["sx0"] + SV["sx1"]) / 2, SV["sy"] + 80, "たとえの棚", 30, J.TICK, "middle", 400),
         F.line(SV["gx"], SV["gy0"], SV["gx"], SV["gy1"], J.LINE_DIM, 4), _tline(SV["gx"], SV["gy1"] - 20, "重さ（キロ）", 26, J.TICK, "middle", 240)]
    for k in (0, 50, 100):
        g.append(F.line(SV["gx"] - 12, sv_y(k), SV["gx"], sv_y(k), J.LINE_DIM, 3) + _tline(SV["gx"] - 20, sv_y(k) + 9, str(k), 26, J.TICK, "end", 100))
    return g


def shelf_stage(prev, st):
    s = []
    if _on(prev, st, "load"):
        bx = (SV["sx0"] + SV["sx1"]) / 2
        s.append(F.rect(bx - 110, SV["sy"] - 170, 220, 170, J.BG2, INK, 5, rx=6) + _tline(bx, SV["sy"] - 72, f"{SV_LOAD:g}キロ", 40, INK, "middle", 200))
        s.append(F.line(SV["gx"], sv_y(SV_LOAD), SV["gx"] + 360, sv_y(SV_LOAD), INK, 5) + _tline(SV["lx"], sv_y(SV_LOAD) + 10, "いつもの重さ", 28, INK, "start", 290))
    if _on(prev, st, "std"):
        y = sv_y(SV_LOAD * SV_REQ)
        s.append(F.line(SV["gx"], y, SV["gx"] + 360, y, INK, 5, dash="16 10") + _tline(SV["lx"], y + 10, "基準＝" + sv_lab(SV_REQ), 28, INK, "start", 300))
    if _on(prev, st, "tube"):
        y = sv_y(SV_LOAD * SV_CIRC)
        s.append(F.line(SV["gx"], y, SV["gx"] + 360, y, J.ALERT, 7) + _tline(SV["lx"], y + 10, "この筒＝" + sv_lab(SV_CIRC), 28, J.ALERT, "start", 300))
    if _on(prev, st, "spare"):
        for xx, sf, c in ((SV["gx"] + 60, SV_REQ, INK), (SV["gx"] + 130, SV_CIRC, J.ALERT)):
            ya, yb = sv_y(SV_LOAD), sv_y(SV_LOAD * sf)
            s.append(F.line(xx, ya, xx, yb, c, 6) + F.line(xx - 12, yb, xx + 12, yb, c, 6))
        s.append(_tline(SV["gx"] + 100, sv_y(SV_LOAD) + 50, "余裕", 28, J.TICK, "middle", 140))
    return s


#  d80（ca05）＝80回目（2022年7月15日）の深さの線。NTSB 図19 を原寸で読んだ点だけ（±2分＝映像方針・あいだは直線＝模式）。
#    大きな音の山 15:26:45（USCG p283）は海面の線に置く（浮上の終わり＝USCG p234「still submerged but nearing the surface」）
D80 = dict(t0=7 * 60.0, t1=16 * 60.0, d1=4000.0, x0=330.0, x1=1480.0, y0=400.0, y1=800.0)
D80_PTS = (("7:35", 0.0), ("10:05", 3840.0), ("13:35", 3840.0), ("15:16", 0.0))
D80_BANG = "15:26:45"


def d80_xy(t, m):
    p = [float(x) for x in t.split(":")]
    mi = p[0] * 60 + p[1] + (p[2] / 60 if len(p) > 2 else 0)
    return (D80["x0"] + (mi - D80["t0"]) / (D80["t1"] - D80["t0"]) * (D80["x1"] - D80["x0"]),
            D80["y0"] + m / D80["d1"] * (D80["y1"] - D80["y0"]))


def d80_base(st0):
    x0, x1, y0, y1 = D80["x0"], D80["x1"], D80["y0"], D80["y1"]
    g = [F.line(x0 - 20, y0, x1 + 30, y0, SEA_LN, 5), _tline(x0 - 30, y0 + 10, "海面", 28, J.TICK, "end", 160),
         F.line(x0, y0, x0, y1, J.LINE_DIM, 3), _tline(x0 - 30, y1 + 50, "深さ", 26, J.TICK, "end", 160)]
    for m in (1000, 2000, 3000, 4000):
        y = d80_xy("7:00", m)[1]
        g.append(F.line(x0 - 10, y, x1, y, J.GRID, 2) + _tline(x0 - 20, y + 9, f"{m:,}m", 24, J.TICK, "end", 140))
    for h in range(8, 17, 2):
        x = d80_xy(f"{h}:00", 0)[0]
        g.append(F.line(x, y1, x, y1 + 12, J.LINE_DIM, 3) + _tline(x, y1 + 46, f"{h}時", 26, J.TICK, "middle", 100))
    return g


def d80_stage(prev, st):
    s = []
    if _on(prev, st, "line"):
        s.append(F.poly([d80_xy(t, m) for t, m in D80_PTS], "none", SUBC, 7))
    if _on(prev, st, "bang"):
        x, y = d80_xy(D80_BANG, 0)
        pts = [(x + (34 if k % 2 == 0 else 14) * math.cos(math.pi * k / 6), y + (34 if k % 2 == 0 else 14) * math.sin(math.pi * k / 6)) for k in range(12)]
        s.append(F.poly(pts, J.ALERT, None, close=True))
    if _on(prev, st, "who"):
        x, y = d80_xy(D80_BANG, 0)
        s.append(_person(x + 150, y - 110, 70, SHIPC) + _person(x + 150, y + 30, 70, SUBC))   # 海面の上＝小舟（母船の側）・下＝艇の中
    return s


#  rtm（ca06・ca24）＝筒の外から見た監視装置（音のセンサー8・ひずみ計の場所8＝輪の向きと長さの向きの2つずつ＝16）。NTSB p1031・USCG 図105（p139）。
#    位置は図105 をもとにした模式（番号は描かない＝図105 に番号が無い）。dead＝2022年に一度も音を拾わなかった3つ（NTSB p1051・USCG p283）
RT = dict(x0=560.0, x1=1360.0, cy=580.0, R=170.0, ring=46.0)
RT_AE = ((0.08, 0.50, True), (0.05, -0.55, False), (0.46, -0.05, True), (0.52, -0.92, False), (0.80, 0.58, True), (1.03, -0.60, False),
         (0.93, -0.92, False), (0.93, 0.22, False))    # (前の端0〜後ろの端1, -1上〜1下, 拾わなかったか)
# 🔧 試し焼き：(0.84, 0.62) が拾わなかったセンサー（0.80, 0.58）に重なった＝後ろの2つを (0.90, ±0.66) へ
RT_SG = ((0.18, -0.62), (0.18, 0.62), (0.30, -0.30), (0.30, 0.30), (0.66, -0.30), (0.66, 0.30), (0.90, -0.66), (0.90, 0.66))


def rt_xy(fx, fy):
    if fx > 1.0:
        return RT["x1"] + RT["ring"] / 2, RT["cy"] + fy * RT["R"]
    return RT["x0"] + fx * (RT["x1"] - RT["x0"]), RT["cy"] + fy * RT["R"] * 0.9


def rtm_base(st0):
    x0, x1, cy, R, rg = RT["x0"], RT["x1"], RT["cy"], RT["R"], RT["ring"]
    return [F.rect(x0, cy - R, x1 - x0, 2 * R, J.BG2, J.LINE, 5), F.rect(x0 - rg, cy - R - 12, rg, 2 * R + 24, J.LINE_DIM, J.LINE, 3),
            F.rect(x1, cy - R - 12, rg, 2 * R + 24, J.LINE_DIM, J.LINE, 3),
            f'<path d="M{x0 - rg:.1f} {cy - R:.1f} A{R * 0.55:.1f} {R:.1f} 0 0 0 {x0 - rg:.1f} {cy + R:.1f}" fill="none" stroke="{J.LINE_DIM}" stroke-width="4" stroke-dasharray="10 8"/>',
            f'<path d="M{x1 + rg:.1f} {cy - R:.1f} A{R * 0.55:.1f} {R:.1f} 0 0 1 {x1 + rg:.1f} {cy + R:.1f}" fill="none" stroke="{J.LINE_DIM}" stroke-width="4" stroke-dasharray="10 8"/>',
            _arrow(x0 - 170, cy + R + 70, x0 - 300, cy + R + 70, J.LINE, 4, 18), _tline(x0 - 150, cy + R + 80, "前", 28, J.TICK, "start", 80)]


def rtm_stage(prev, st):
    s = []
    if _on(prev, st, "ae"):
        for fx, fy, _d in RT_AE:
            x, y = rt_xy(fx, fy)
            s.append(F.circ(x, y, 17, SUBC, J.BG, 3))
    if _on(prev, st, "sg"):
        for fx, fy in RT_SG:
            x, y = rt_xy(fx, fy)
            s.append(F.rect(x - 8, y - 20, 16, 40, "none", J.AMBER, 4) + F.rect(x - 20, y - 8, 40, 16, "none", J.AMBER, 4))
    if _on(prev, st, "squeeze"):
        x0, x1, cy, R = RT["x0"], RT["x1"], RT["cy"], RT["R"]
        for k in range(4):
            x = x0 + 100 + k * (x1 - x0 - 200) / 3
            s.append(_arrow(x, cy - R - 110, x, cy - R - 16, J.LINE, 5, 18) + _arrow(x, cy + R + 110 - 60, x, cy + R + 16, J.LINE, 5, 18))
        s.append(F.rect(x0 + 10, cy - R + 14, x1 - x0 - 20, 2 * R - 28, "none", INK, 3, dash="12 8"))
    if _on(prev, st, "dead"):
        for fx, fy, dead in RT_AE:
            if dead:
                x, y = rt_xy(fx, fy)
                s.append(F.circ(x, y, 19, J.BG2, J.TICK, 4) + F.line(x - 12, y - 12, x + 12, y + 12, J.TICK, 4) + F.line(x - 12, y + 12, x + 12, y - 12, J.TICK, 4))
    return s


#  ae（ca07・ca08）＝80回目の終わりの音とひずみ（上＝音・下＝ひずみ）。記録の時刻の点だけ（USCG p283「beginning at approximately 3:17 p.m.」
#    「a significant escalation beginning at 3:25:56 p.m.」「At 3:26:45 p.m. … a major acoustic emission event」・p286「coincided」・
#    NTSB p1052「between about 1515 and 1530」）。線の高さと形は模式（値を描かない）
AE = dict(t0=15 * 60 + 10.0, t1=15 * 60 + 35.0, x0=390.0, x1=1560.0, ya=(330.0, 560.0), ys=(610.0, 800.0))
AE_UP = "15:17"
AE_ESC = "15:25:56"
AE_PEAK = "15:26:45"
AE_BAND = ("15:15", "15:30")
AE_SHAPE = ((910.0, 0.05), (917.0, 0.06), (921.0, 0.16), (925.93, 0.30), (926.5, 0.55), (926.75, 1.0), (927.1, 0.25), (929.0, 0.10), (935.0, 0.06))


def _ae_min(t):
    p = [float(x) for x in t.split(":")]
    return p[0] * 60 + p[1] + (p[2] / 60 if len(p) > 2 else 0)


def ae_x(mi):
    return AE["x0"] + (mi - AE["t0"]) / (AE["t1"] - AE["t0"]) * (AE["x1"] - AE["x0"])


def _ae_pts(lo, hi):
    pts = [(m, v) for m, v in AE_SHAPE if lo <= m <= hi]
    return [(ae_x(m), AE["ya"][1] - v * (AE["ya"][1] - AE["ya"][0] - 20)) for m, v in pts]


def _ae_strain(after):
    y_lo, y_hi = AE["ys"][1] - 50, AE["ys"][1] - 120
    pk = ae_x(_ae_min(AE_PEAK))
    return [(pk, y_lo), (pk, y_hi), (AE["x1"], y_hi)] if after else [(AE["x0"], y_lo), (pk, y_lo)]


def ae_base(st0):
    g = []
    for (ya, yb), t in ((AE["ya"], "音の大きさ"), (AE["ys"], "ひずみ")):
        g.append(F.line(AE["x0"], ya, AE["x0"], yb, J.LINE_DIM, 3) + F.line(AE["x0"], yb, AE["x1"], yb, J.LINE_DIM, 3))
        g.append(_tline(AE["x0"] - 24, (ya + yb) / 2 + 10, t, 28, J.TICK, "end", 260))
    for k in range(6):
        mi = AE["t0"] + k * 5
        x = ae_x(mi)
        g.append(F.line(x, AE["ys"][1], x, AE["ys"][1] + 12, J.LINE_DIM, 3) + _tline(x, AE["ys"][1] + 44, f"{int(mi // 60)}:{int(mi % 60):02d}", 26, J.TICK, "middle", 120))
    g.append(F.poly(_ae_pts(AE["t0"], AE["t1"]), "none", J.LINE_DIM, 4))
    g.append(F.poly(_ae_strain(False) + _ae_strain(True)[1:], "none", J.LINE_DIM, 4))
    return g


def ae_stage(prev, st):
    s = []
    if _on(prev, st, "band"):
        xa, xb = ae_x(_ae_min(AE_BAND[0])), ae_x(_ae_min(AE_BAND[1]))
        s.append(F.rect(xa, AE["ya"][0] - 10, xb - xa, AE["ys"][1] - AE["ya"][0] + 10, NTC, NTC, 3, op=0.22))
    if _on(prev, st, "up"):
        s.append(F.poly(_ae_pts(_ae_min(AE_UP), _ae_min(AE_ESC)), "none", INK, 7))
        x = ae_x(_ae_min(AE_UP))
        s.append(F.line(x, AE["ya"][0], x, AE["ya"][1], INK, 3, dash="10 8"))
    if _on(prev, st, "peak"):
        s.append(F.poly(_ae_pts(_ae_min(AE_ESC), 927.1), "none", J.ALERT, 7))
    if _on(prev, st, "jump"):
        s.append(F.poly(_ae_strain(True), "none", J.ALERT, 7))
    return s


#  ctrl（ca15）＝コントローラーの向き（81回目＝推進器の操作が逆→操縦士は逆さに持って続けた＝USCG p235「turning the controller around and operating
#    the controls in reverse」）。左＝そのまま持つ（倒す向きと動く向きが逆）・右＝逆さに持つ（そろう）。形は模式
CT = dict(l=(560.0, 600.0), r=(1360.0, 600.0), w=380.0, h=190.0)


def _pad(cx, cy, flip):
    w, h = CT["w"], CT["h"]
    sg = -1 if flip else 1
    return (F.rect(cx - w / 2, cy - h / 2, w, h, J.BG2, J.LINE, 5, rx=80) + F.circ(cx - 80 * sg, cy + 10 * sg, 34, J.LINE_DIM, J.LINE, 4)
            + F.circ(cx + 80 * sg, cy - 18 * sg, 15, J.LINE) + F.circ(cx + 120 * sg, cy + 16 * sg, 15, J.LINE))


def ctrl_dirs(flip):
    """(倒す向き, 動く向き)＝画面の上が +1。そのまま＝逆（故障）・逆さに持つ＝そろう。"""
    return (1, 1) if flip else (1, -1)


def ctrl_base(st0):
    cx, cy = CT["l"]
    op, mv = ctrl_dirs(False)
    return [_pad(cx, cy, False), _arrow(cx - 80, cy - 40, cx - 80, cy - 40 - 120 * op, INK, 7, 26),
            _tline(cx - 80, cy - 190, "倒す", 28, INK, "middle", 120),
            _arrow(cx + 230, cy - 110 + 60 * mv, cx + 230, cy - 110 - 60 * mv, J.ALERT, 7, 26), _tline(cx + 230, cy - 210, "艇の動き", 28, J.ALERT, "middle", 160),
            _tline(cx, cy + CT["h"] / 2 + 60, "そのまま持つ", 30, J.TICK, "middle", 300)]


def ctrl_stage(prev, st):
    s = []
    if _on(prev, st, "flip"):
        cx, cy = CT["r"]
        op, mv = ctrl_dirs(True)
        s.append(_pad(cx, cy, True) + _arrow(cx + 80, cy - 40, cx + 80, cy - 40 - 120 * op, INK, 7, 26)
                 + _arrow(cx + 260, cy - 110 + 60 * mv, cx + 260, cy - 110 - 60 * mv, SUBC, 7, 26))
        s.append(_arrow(CT["l"][0] + CT["w"] / 2 + 60, cy, cx - CT["w"] / 2 - 40, cy, J.LINE, 5, 22))
    return s


#  stime（ca16）＝会社のひずみの見方＝時刻に沿って潜航ごとの線を横に並べる（NTSB p1051「plotting it side-by-side with dive depth as a function of time」）。
#    形は模式（値を描かない）。比べにくい＝NTSB p1064「it was difficult for OceanGate to compare data between dives」
STM = dict(x0=300.0, x1=1740.0, y0=380.0, y1=760.0)
STM_DIVES = ((330.0, 620.0), (700.0, 1040.0), (1110.0, 1330.0), (1400.0, 1720.0))   # 潜航ごとの時刻の幅（画素・模式）


def _stm_hump(xa, xb, depth):
    dy = (STM["y1"] - STM["y0"]) * (0.92 if depth else 0.55)
    return [(xa, STM["y0"]), (xa + (xb - xa) * 0.28, STM["y0"] + dy), (xa + (xb - xa) * 0.62, STM["y0"] + dy), (xb, STM["y0"])]


def stime_base(st0):
    return [F.line(STM["x0"], STM["y0"], STM["x1"], STM["y0"], J.LINE_DIM, 3), _arrow(STM["x1"] - 120, STM["y1"] + 60, STM["x1"], STM["y1"] + 60, J.LINE, 4, 18),
            _tline(STM["x1"] - 140, STM["y1"] + 70, "時刻", 28, J.TICK, "end", 120)]


def stime_stage(prev, st):
    s = []
    if _on(prev, st, "on"):
        for xa, xb in STM_DIVES:
            s.append(F.poly(_stm_hump(xa, xb, True), "none", J.TICK, 4, dash="12 8") + F.poly(_stm_hump(xa, xb, False), "none", INK, 6))
        s.append(F.line(380.0, 820.0, 440.0, 820.0, INK, 6) + _tline(452.0, 830.0, "ひずみ", 26, J.TICK, "start", 160)
                 + F.line(640.0, 820.0, 700.0, 820.0, J.TICK, 4, dash="12 8") + _tline(712.0, 830.0, "深さ", 26, J.TICK, "start", 120))
    if _on(prev, st, "hard"):
        for (_, xb), (xa, _) in zip(STM_DIVES, STM_DIVES[1:]):
            s.append(_qmark((xb + xa) / 2, STM["y0"] + 150, 70, J.ALERT))
    return s


#  nonlin（ca19）＝浅い所だけ線が曲がるしくみ（左＝深さとひずみの線の模式・右＝筒の前の端のひずみ計と層のはがれ）。
#    原文 NTSB p1059「This change in strain response is more consistent with a delamination between layers」「The sensor … was located at the forward
#    end of the composite cylinder」「the separated layers to initially respond differently … at shallow depths, but, at greater depths, … similar」
NL = dict(gx0=330.0, gx1=900.0, gy0=360.0, gy1=800.0, sh=150.0, cx0=1180.0, cx1=1700.0, cy=560.0, R=120.0)


def nl_lines():
    """(まっすぐな線, 曲がった線)＝(x, y) の点。曲がった線は浅い所（gy0〜gy0+sh）だけずれ、深い所はまっすぐな線と平行。"""
    x0, x1, y0, y1, sh = NL["gx0"], NL["gx1"], NL["gy0"], NL["gy1"], NL["sh"]
    k = (x1 - x0 - 60) / (y1 - y0)
    straight = [(x0, y0), (x0 + k * (y1 - y0), y1)]
    off = 70.0
    bent = [(x0, y0), (x0 + off * 0.55, y0 + sh * 0.25), (x0 + off * 0.85, y0 + sh * 0.6), (x0 + off + k * sh, y0 + sh), (x0 + off + k * (y1 - y0), y1)]
    return straight, bent


def nonlin_base(st0):
    x0, x1, y0, y1 = NL["gx0"], NL["gx1"], NL["gy0"], NL["gy1"]
    st, _ = nl_lines()
    cx0, cx1, cy, R = NL["cx0"], NL["cx1"], NL["cy"], NL["R"]
    return [F.line(x0, y0, x0, y1, J.LINE_DIM, 3) + F.line(x0, y0, x1, y0, J.LINE_DIM, 3),
            _tline(x0 - 20, y0 + 10, "浅い", 26, J.TICK, "end", 100) + _tline(x0 - 20, y1, "深い", 26, J.TICK, "end", 100),
            _tline(x1, y0 - 18, "ひずみ →", 26, J.TICK, "end", 200),
            F.poly(st, "none", J.TICK, 5, dash="14 10"),
            F.rect(cx0, cy - R, cx1 - cx0, 2 * R, J.BG2, J.LINE, 5), F.rect(cx0 - 36, cy - R - 10, 36, 2 * R + 20, J.LINE_DIM, J.LINE, 3),
            _tline(cx0 - 50, cy + R + 60, "前", 28, J.TICK, "middle", 80)]


def nonlin_stage(prev, st):
    s = []
    if _on(prev, st, "bend"):
        _, bent = nl_lines()
        s.append(F.poly(bent, "none", J.ALERT, 7))
    if _on(prev, st, "zones"):
        y0, sh = NL["gy0"], NL["sh"]
        s.append(F.rect(NL["gx0"] + 4, y0 + 4, NL["gx1"] - NL["gx0"] - 4, sh - 4, J.ALERT, op=0.12))
    if _on(prev, st, "fwd"):
        cx0, cx1, cy, R = NL["cx0"], NL["cx1"], NL["cy"], NL["R"]
        s.append(F.line(cx0, cy - R + 34, cx0 + (cx1 - cx0) * 0.7, cy - R + 34, J.ALERT, 6, dash="16 8"))
        x, y = cx0 + 26, cy - R + 70
        s.append(F.rect(x - 8, y - 20, 16, 40, "none", J.AMBER, 4) + F.rect(x - 20, y - 8, 40, 16, "none", J.AMBER, 4))
    return s


#  screen（ca23）＝監視装置の画面の決まり（音の数が30で黄・50で赤・警報の音なし・潜航ごとにゼロへ）。NTSB p1031「if the system detected 30 hits during a
#    dive, the system issued a yellow display warning. If 50 hits were detected, a red warning was issued」「Hit counts did not accumulate between successive
#    dives」・TSB §1.10.9「The system did not have audible alarms」。画面の形は模式
SC = dict(x0=360.0, x1=1260.0, y0=330.0, y1=790.0, bx0=460.0, bx1=1160.0, by=520.0, bh=80.0, nmax=60.0, spk=(1520.0, 500.0))
SC_Y, SC_R = 30, 50


def sc_x(n):
    return SC["bx0"] + (SC["bx1"] - SC["bx0"]) * n / SC["nmax"]


def screen_base(st0):
    g = [F.rect(SC["x0"], SC["y0"], SC["x1"] - SC["x0"], SC["y1"] - SC["y0"], J.BG2, J.LINE, 5, rx=22),
         _tline(SC["bx0"], SC["by"] - 40, "1回の潜航の音の数", 30, J.TICK, "start", 500),
         F.rect(SC["bx0"], SC["by"], SC["bx1"] - SC["bx0"], SC["bh"], "none", J.LINE, 4)]
    for n in (0, SC_Y, SC_R):
        g.append(F.line(sc_x(n), SC["by"] + SC["bh"], sc_x(n), SC["by"] + SC["bh"] + 16, J.LINE, 3)
                 + _tline(sc_x(n), SC["by"] + SC["bh"] + 52, str(n), 30, INK, "middle", 80))
    x, y = SC["spk"]
    g.append(F.poly([(x - 60, y - 26), (x - 30, y - 26), (x + 10, y - 66), (x + 10, y + 66), (x - 30, y + 26), (x - 60, y + 26)], J.BG2, J.LINE, 4, close=True))
    return g


def screen_stage(prev, st):
    s = []
    by, bh = SC["by"], SC["bh"]
    if _on(prev, st, "lv"):
        s.append(F.rect(sc_x(SC_Y), by + 4, sc_x(SC_R) - sc_x(SC_Y), bh - 8, J.AMBER, op=0.9)
                 + F.rect(sc_x(SC_R), by + 4, sc_x(SC["nmax"]) - sc_x(SC_R) - 4, bh - 8, J.ALERT, op=0.9))
    if _on(prev, st, "mute"):
        x, y = SC["spk"]
        s.append(_xmark(x + 80, y, 34, J.ALERT, 10))
    if _on(prev, st, "reset"):
        y = by + bh + 110
        s.append(F.poly([(sc_x(40), by + bh + 70), (sc_x(40), y), (sc_x(0), y)], "none", J.AMBER, 5) + _arrow(sc_x(0), y, sc_x(0), by + bh + 76, J.AMBER, 5, 20))
    return s


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-15）：第10〜11章・終章
# ══════════════════════════════════════════════════════════
#  temp（cb04）＝セントジョンズの冬（2022年12月〜2023年2月）の気温の平均。TSB §1.22「The average high temperature in St. John’s between December 2022
#    and February 2023 was -0.5° and the average low was -5.5°」「experiences snow, strong winds, freezing rain, and hail」。
#    🔴 単位はカナダの報告書の書き方のまま「°」（℃ と書かない＝摂氏は推測・映像方針 §0-3）。⚠️ 棒（qty）は 0 より大きい値しか描けない＝目盛りの点で
TP = dict(x=760.0, y0=360.0, y1=800.0, vmax=5.0, vmin=-10.0)
TP_HI, TP_LO = -0.5, -5.5
TP_TICKS = (5, 0, -5, -10)


def tp_y(v):
    return TP["y0"] + (TP["vmax"] - v) / (TP["vmax"] - TP["vmin"]) * (TP["y1"] - TP["y0"])


def _deg(v):
    return ("−" if v < 0 else "") + f"{abs(v):g}°"


def temp_base(st0):
    x = TP["x"]
    g = [F.line(x, TP["y0"], x, TP["y1"], J.LINE, 5), _tline(x, TP["y0"] - 30, "気温", 28, J.TICK, "middle", 200)]
    for v in TP_TICKS:
        y = tp_y(v)
        g.append(F.line(x - 14, y, x + 14, y, J.LINE, 3) + _tline(x - 30, y + 10, _deg(v), 28, J.TICK, "end", 120))
    # ⚠️ geom_gap：0° の線を目盛りの字「0°」（x−58〜x−30）にかけた＝字の左で止める（右は気温の札の場所）
    g.append(F.line(x - 340, tp_y(0), x - 72, tp_y(0), J.LINE_DIM, 3, dash="12 9"))
    g.append(_tline(x - 340, tp_y(0) - 14, "水が凍る", 26, J.TICK, "start", 200))
    return g


def temp_stage(prev, st):
    s = []
    x = TP["x"]
    if _on(prev, st, "avg"):
        for v in (TP_HI, TP_LO):
            y = tp_y(v)
            s.append(F.line(x - 44, y, x + 44, y, J.AMBER, 9) + F.circ(x, y, 14, J.AMBER))
    return s


#  risk（cb17）＝危険度の点数（事故の潜航の計画＝35）と会社の決まり（48を超えると「ストライク」・3つで その日の潜航を中止）。TSB §1.17.12.1「a risk index
#    of greater than 48 was considered to be a strike」「had a risk index of 35」・USCG p78「three or more “strikes” … cancel the day’s dive operation」。
#    目盛りの右の端（60）は模式（点数の上限は報告書に無い）
RK = dict(x0=360.0, x1=1320.0, y=560.0, vmax=60.0, bx=(1480.0, 1600.0, 1720.0), by=560.0, br=40.0)
RK_DAY, RK_STRIKE, RK_N = 35, 48, 3


def rk_x(v):
    return RK["x0"] + (RK["x1"] - RK["x0"]) * v / RK["vmax"]


def risk_base(st0):
    y = RK["y"]
    g = [F.line(RK["x0"], y, RK["x1"], y, J.LINE, 5), _tline(RK["x0"], y - 150, "危険度の点数", 30, J.TICK, "start", 400)]
    for v in range(0, int(RK["vmax"]) + 1, 10):
        g.append(F.line(rk_x(v), y - 12, rk_x(v), y + 12, J.LINE, 3) + _tline(rk_x(v), y + 50, str(v), 28, J.TICK, "middle", 80))
    for bx in RK["bx"]:
        g.append(F.circ(bx, RK["by"], RK["br"], "none", J.LINE_DIM, 4))
    return g


def risk_stage(prev, st):
    s = []
    y = RK["y"]
    if _on(prev, st, "day"):
        s.append(F.line(rk_x(RK_DAY), y, rk_x(RK_DAY), y + 64, J.AMBER, 3) + F.circ(rk_x(RK_DAY), y, 18, J.AMBER))
    if _on(prev, st, "line"):
        x = rk_x(RK_STRIKE)
        # ⚠️ 門番 layout：帯を y+40 まで塗ると目盛りの字「50」「60」（y+50）を覆った＝軸の線の少し下まで
        s.append(F.rect(x, y - 40, RK["x1"] - x, 54, J.ALERT, op=0.25) + F.line(x, y - 60, x, y + 14, J.ALERT, 5, dash="12 8"))
    if _on(prev, st, "three"):
        for bx in RK["bx"]:
            s.append(F.circ(bx, RK["by"], RK["br"], "none", J.ALERT, 6) + _xmark(bx, RK["by"], 18, J.ALERT, 7))
    return s


#  cols（cc02・cc03・cc05・cc06・cc11）＝3つの報告書の答えを3列に（列の色＝調べの役の色・札の色＝主語の役の色＝会社 橙・船体 白・規則 灰）。
#    上の段＝主な原因・下の段＝その次（米沿岸警備隊＝その他の要因・米運輸安全委員会＝寄与・カナダ＝危険の所見）。字は札が出る段に1回だけ（明るくするのは下線と枠）。
#    原文＝USCG p5（primary causal factor）・p7（primary causal factors 1〜8）・p8（other contributing causal factors の4つ目）・NTSB p1074（probable cause・
#    Contributing ×2）・TSB §3.1（never validated・fail progressively with damage accumulating）・§3.2（without any independent verification）
#    🔧 ⑤b-6 の門番 box：列を 296〜852 の同じ高さにし、字を左に寄せたら、札の少ない列（米運輸安全委員会・カナダ）の空きが 45〜50% ＝
#       列の高さは中身まで・下の段は上の段のすぐ下・字は列の真ん中に。札は報告書の文の部分を足した（NTSB p1074 の推定原因の3つの部分・TSB §3.1 の2つ目）
CL = dict(xs=(400.0, 960.0, 1520.0), w=520.0, y0=296.0, hy=342.0, t1y=390.0, r0=432.0, dr=32.0, gap=40.0, dr2=42.0, pad=34.0)
CL_COL = (("米沿岸警備隊", "uscg"), ("米運輸安全委員会", "ntsb"), ("カナダの調べ", "tsb"))
CL_TIER = (("主な要因", "その他の要因"), ("推定原因", "寄与"), ("原因と寄与", "危険の所見"))
CL_ITEM = dict(
    u0=(0, 1, (("確立した手順に従わず", "company"),)),
    u8=(0, 1, (("設計と試験が不十分", "company"), ("寿命を調べず", "company"), ("監視の装置に頼りすぎ", "company"), ("傷のあとも使い続けた", "company"),
               ("船体の作りの欠陥", "sub"), ("不具合を詳しく調べず", "company"), ("懸念を言えない職場", "company"), ("整備せず外に置いた", "company"))),
    ux=(0, 2, (("規則の足りなさ", "LINE"),)),
    n1=(1, 1, (("強さと寿命を確かめず", "company"), ("層のはがれと別の傷", "sub"), ("局所の座屈で壊れた", "sub"))),
    n2=(1, 2, (("規則と指針の足りなさ", "LINE"),)),
    n3=(1, 2, (("監視の記録の読み違い", "company"),)),
    t1=(2, 1, (("強さを確かめず", "company"), ("作りと試験が標準外", "company"))),
    t2=(2, 1, (("傷が積もって壊れた", "sub"),)),
    tx=(2, 2, (("独立した確認なし", "LINE"),)),
)
CL_GAP = ("ux", "n2", "tx")        # 外から監督する仕組みの穴＝3列それぞれの下の段（cc11）
CL_U7 = ("u8", 6)                  # 7つ目＝職場の文化（cc03）


def cl_layout():
    """札ごとの (欄, 列, 段, 字, 役, y) と、列ごとの下の段の名の y・列の下の端。上の段は u0→u8／n1／t1→t2・下の段は ux／n2→n3／tx。"""
    rows, t2y, bot = [], [], []
    for c in range(len(CL_COL)):
        y = CL["r0"]
        mine = [(f_, v) for f_, v in CL_ITEM.items() if v[0] == c]
        for f_, (_c, tier, items) in mine:
            if tier != 1:
                continue
            for t, r in items:
                rows.append((f_, c, 1, t, r, y))
                y += CL["dr"] + (10 if f_ == "u0" else 0)
        ly = y - CL["dr"] + CL["gap"] + 30
        t2y.append(ly)
        y = ly + CL["dr2"]
        for f_, (_c, tier, items) in mine:
            if tier != 2:
                continue
            for t, r in items:
                rows.append((f_, c, 2, t, r, y))
                y += CL["dr2"]
        bot.append(y - CL["dr2"] + CL["pad"])
    return rows, t2y, bot


def cl_rows():
    return cl_layout()[0]


def _cl_cap(f_):
    return 30 if f_ == "u0" else 27


def _cl_w(t, f_):
    return min(F.fm.width(t, _cl_cap(f_)), CL["w"] - 48)


def cols_base(st0):
    g = []
    _rows, t2y, bot = cl_layout()
    for c, (nm, r) in enumerate(CL_COL):
        x, w = CL["xs"][c], CL["w"]
        g.append(F.rect(x - w / 2, CL["y0"], w, bot[c] - CL["y0"], J.BG2, J.LINE_DIM, 4, rx=14))
        g.append(_tline(x, CL["hy"], nm, 32, _rc(r), "middle", w - 40))
        g.append(_tline(x, CL["t1y"], CL_TIER[c][0], 24, J.TICK, "middle", 300))
        g.append(_tline(x, t2y[c], CL_TIER[c][1], 24, J.TICK, "middle", 300))
        g.append(F.line(x - w / 2 + 20, t2y[c] - 30, x + w / 2 - 20, t2y[c] - 30, J.LINE_DIM, 2, dash="8 6"))
    return g


def cols_stage(prev, st):
    s = []
    rows, _t2y, bot = cl_layout()
    fresh = {f_ for f_ in CL_ITEM if _on(prev, st, f_)}
    for c, (_nm, r) in enumerate(CL_COL):
        before = any(prev.get(f_) == "on" for f_, v in CL_ITEM.items() if v[0] == c)
        if not before and any(CL_ITEM[f_][0] == c for f_ in fresh):
            x, w = CL["xs"][c], CL["w"]
            s.append(F.rect(x - w / 2, CL["y0"], w, bot[c] - CL["y0"], "none", _rc(r), 7, rx=14))
    for f_, c, tier, t, r, y in rows:
        if f_ in fresh:
            s.append(_tline(CL["xs"][c], y, t, _cl_cap(f_), _rc(r) if r != "LINE" else INK, "middle", CL["w"] - 48))
    if _on(prev, st, "u7"):
        # ⚠️ geom_gap：下線は次の行の字（行の間 32px）に触れた＝行の左右の端に黄の印（字は列の真ん中）
        f_, i = CL_U7
        _f, c, _tier, t, _r, y = [rw for rw in rows if rw[0] == f_][i]
        x, w = CL["xs"][c], CL["w"]
        s.append(F.rect(x - w / 2 + 14, y - 22, 10, 26, J.AMBER, rx=3) + F.rect(x + w / 2 - 24, y - 22, 10, 26, J.AMBER, rx=3))
    if _on(prev, st, "gap"):
        for f_ in CL_GAP:
            for _f, c, _tier, t, _r, y in [rw for rw in rows if rw[0] == f_]:
                w = _cl_w(t, f_)
                s.append(F.rect(CL["xs"][c] - w / 2 - 14, y - 28, w + 28, 38, "none", J.AMBER, 4, rx=8))
    return s


#  cmp（cc09・cc10）＝3つの答えの並べ（左＝重なる所・分かれる所／右の3列＝調べ）。重なる所＝3列に✓（調べの色）・分かれる所＝列ごとの言葉か破線の帯。
#    原文＝USCG p7（the loss of structural integrity of the TITAN’s carbon fiber hull）・NTSB p1074（local buckling failure of the pressure vessel）・TSB §2.1
#    （the pressure hull’s carbon fibre cylinder was the likeliest point of failure）／USCG p7 の 1)2)3)・NTSB p1073「unaware of its actual strength and durability」・
#    p1074「flawed analysis of their pressure vessel monitoring system data」・TSB §3.1／USCG p289・NTSB p1059・TSB §1.10.10.1（2022年の音＝ca21・ca22 と同じ言葉）
VS = dict(lx=150.0, xs=(950.0, 1270.0, 1590.0), cw=300.0, hy=338.0, ys=(452.0, 522.0, 592.0, 722.0, 794.0), sec=(400.0, 668.0))
VS_COL = (("米沿岸警備隊", "uscg"), ("米運輸安全委員会", "ntsb"), ("カナダの調べ", "tsb"))
VS_ROWS = (("same", "窓でなく炭素繊維の側", None), ("same", "強さと寿命を確かめず", None), ("same", "監視の記録を生かせず", None),
           ("cells", "2022年の音の重み", ("強く示す", "可能性が高い", "決められない")), ("band", "最後の数秒の順番", "書き方が違う"))


def cmp_base(st0):
    g = []
    for c, (nm, r) in enumerate(VS_COL):
        g.append(_tline(VS["xs"][c], VS["hy"], nm, 28, _rc(r), "middle", VS["cw"] - 10))
    g.append(F.line(VS["lx"], VS["hy"] + 24, VS["xs"][2] + VS["cw"] / 2, VS["hy"] + 24, J.LINE_DIM, 3))
    g.append(_tline(VS["lx"], VS["sec"][0], "重なる所", 26, J.TICK, "start", 300))
    g.append(_tline(VS["lx"], VS["sec"][1], "分かれる所", 26, J.TICK, "start", 300))
    g.append(F.line(VS["lx"], VS["sec"][1] - 34, VS["xs"][2] + VS["cw"] / 2, VS["sec"][1] - 34, J.LINE_DIM, 2, dash="8 6"))
    return g


def cmp_stage(prev, st):
    s = []
    n0, n1 = _n_of(prev, st)
    for i in range(n0, n1):
        kind, lab, val = VS_ROWS[i]
        y = VS["ys"][i]
        s.append(_tline(VS["lx"], y + 11, lab, 32, INK, "start", VS["xs"][0] - VS["cw"] / 2 - VS["lx"] - 30))
        if kind == "same":
            for c, (_nm, r) in enumerate(VS_COL):
                s.append(_check(VS["xs"][c], y - 2, 20, _rc(r)))
        elif kind == "cells":
            for c, (_nm, r) in enumerate(VS_COL):
                s.append(_tline(VS["xs"][c], y + 10, val[c], 28, _rc(r), "middle", VS["cw"] - 20))
        else:
            xa, xb = VS["xs"][0] - VS["cw"] / 2 + 10, VS["xs"][2] + VS["cw"] / 2 - 10
            s.append(F.rect(xa, y - 28, xb - xa, 50, "none", J.TICK, 3, rx=10, dash="12 9") + _tline((xa + xb) / 2, y + 9, val, 28, J.TICK, "middle", 600))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表・札の置き場・線の先
# ══════════════════════════════════════════════════════════
VIEWS = dict(
    fuji=dict(lab="深さの比べ（横から）", fields=dict(press=ONOFF, coin=ONOFF), base=fuji_base, stage=fuji_stage),
    reports=dict(lab="報告書の表紙", fields=dict(r1=ONOFF, r2=ONOFF, r3=ONOFF), base=reports_base, stage=reports_stage),
    side=dict(lab="横から見たタイタン（機首が左）", fields=dict(dim=ONOFF, hull=ONOFF, mat=ONOFF, bolts=ONOFF, only=ONOFF, crack=ONOFF), base=side_base,
              stage=side_stage),
    org=dict(lab="上級の職の席（カナダの報告書の表4）", fields=dict(seats=ONOFF, ceo=ONOFF, all=ONOFF, staff=ONOFF), base=org_base,
             stage=org_stage),
    paper=dict(lab="書類の要点（英字は原文のまま）", fields=dict(doc=tuple(PP_DOC), hl1=ONOFF, hl2=ONOFF, hl3=ONOFF, hl4=ONOFF, hl5=ONOFF,
                                                         n9=ONOFF, name=ONOFF, uscg=ONOFF),
               base=paper_base, stage=paper_stage),
    table=dict(lab="カナダの報告書 付録Bの表（英字は原文のまま）", fields=dict(yr=ONOFF), base=table_base, stage=table_stage),
    dives=dict(lab="付録Bの潜航（1回＝1点）", fields=dict(reach=ONOFF, dome=ONOFF, batt=ONOFF, thr=ONOFF, wt=ONOFF, com=ONOFF, y22=ONOFF),
               base=dives_base, stage=dives_stage),
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
    bow=dict(lab="上から見た船首のまわり（北が上）", fields=dict(ese=ONOFF, ene=ONOFF, plan=ONOFF, jump=ONOFF, hit=ONOFF), base=bow_base, stage=bow_stage),
    two=dict(lab="調べごとの見方", fields=dict(us=ONOFF, ca=ONOFF, why=ONOFF), base=two_base, stage=two_stage),
    # 🆕 ⑤b-4（2026-10-15）
    send=dict(lab="母船と潜水艇の文", fields=dict(send=ONOFF, none=ONOFF), base=send_base, stage=send_stage),
    proto=dict(lab="会社の手順の流れ", fields=dict(wait=ONOFF, search=ONOFF, out=ONOFF, best=ONOFF), base=proto_base, stage=proto_stage),
    none=dict(lab="欄の中身", fields=dict(set=tuple(NO), n=("0", "1", "2", "3")), base=none_base, stage=none_stage),
    say=dict(lab="人の言葉（顔は描かない）", fields=dict(set=tuple(SAY), n=("0", "1", "2")), base=say_base, stage=say_stage),
    layers=dict(lab="筒の壁の断面（5枚の層）", fields=dict(sep=ONOFF, void=ONOFF, rub=ONOFF, grind=ONOFF), base=layers_base, stage=layers_stage),
    buckle=dict(lab="層の板の断面", fields=dict(split=ONOFF, press=ONOFF), base=buckle_base, stage=buckle_stage, parts=buckle_parts),
    tc=dict(lab="輪切りで見た力の向き", fields=dict(air=ONOFF, sea=ONOFF), base=tc_base, stage=tc_stage),
    shell=dict(lab="人が乗る殻の形と材料", fields=dict(left=ONOFF, right=ONOFF), base=shell_base, stage=shell_stage),
    ruler=dict(lab="深さの物差し（縮尺どおり）", fields=dict(z=("near", "far", "mid"), goal=ONOFF, op=ONOFF, fail=ONOFF, ratio=ONOFF,
                                                     test=ONOFF, w650=ONOFF, w1k=ONOFF),
               base=ruler_base, stage=ruler_stage),
    sf=dict(lab="安全率のしくみ", fields=dict(bars=ONOFF, ratio=ONOFF, spare=ONOFF), base=sf_base, stage=sf_stage),
    model=dict(lab="3分の1の大きさの模型（横から）", fields=dict(press=ONOFF, fail=ONOFF), base=model_base, stage=model_stage),
    klass=dict(lab="船級のしくみ", fields=dict(soc=ONOFF, design=ONOFF, test=ONOFF, cert=ONOFF), base=klass_base, stage=klass_stage),
    wind=dict(lab="筒の作り方（横から）", fields=dict(run=ONOFF), base=wind_base, stage=wind_stage),
    meet=dict(lab="会合の席", fields=dict(rec=ONOFF), base=meet_base, stage=meet_stage),
    # 🆕 ⑤b-5（2026-10-15）
    cards=dict(lab="要点の並び", fields=dict(set=tuple(CD), n=("0", "1", "2", "3", "4"), loop=ONOFF), base=cards_base, stage=cards_stage),
    groove=dict(lab="筒の端とチタンの輪の溝（断面）", fields=dict(thick=ONOFF, cut=ONOFF), base=groove_base, stage=groove_stage),
    coupons=dict(lab="端材から切り出した試料", fields=dict(cut=ONOFF), base=coupons_base, stage=coupons_stage),
    shelf=dict(lab="安全率を棚にたとえると", fields=dict(load=ONOFF, std=ONOFF, tube=ONOFF, spare=ONOFF), base=shelf_base, stage=shelf_stage),
    d80=dict(lab="80回目の深さ（記録の点）", fields=dict(line=ONOFF, bang=ONOFF, who=ONOFF), base=d80_base, stage=d80_stage),
    rtm=dict(lab="船体の監視装置", fields=dict(ae=ONOFF, sg=ONOFF, squeeze=ONOFF, dead=ONOFF), base=rtm_base, stage=rtm_stage),
    ae=dict(lab="80回目の終わりの記録（15時台）", fields=dict(up=ONOFF, peak=ONOFF, jump=ONOFF, band=ONOFF), base=ae_base, stage=ae_stage),
    ctrl=dict(lab="コントローラーの向き", fields=dict(flip=ONOFF), base=ctrl_base, stage=ctrl_stage),
    stime=dict(lab="会社のひずみの見方", fields=dict(on=ONOFF, hard=ONOFF), base=stime_base, stage=stime_stage),
    nonlin=dict(lab="浅い所で曲がる線", fields=dict(bend=ONOFF, zones=ONOFF, fwd=ONOFF), base=nonlin_base, stage=nonlin_stage),
    screen=dict(lab="監視装置の画面", fields=dict(lv=ONOFF, mute=ONOFF, reset=ONOFF), base=screen_base, stage=screen_stage),
    # 🆕 ⑤b-6（2026-10-15）
    temp=dict(lab="冬の気温の平均（12月〜2月）", fields=dict(avg=ONOFF, wx=ONOFF), base=temp_base, stage=temp_stage),
    risk=dict(lab="潜航の計画の危険度", fields=dict(day=ONOFF, line=ONOFF, three=ONOFF), base=risk_base, stage=risk_stage),
    cols=dict(lab="調べごとの答え（3列）", fields={f_: ONOFF for f_ in tuple(CL_ITEM) + ("u7", "gap")}, base=cols_base, stage=cols_stage),
    cmp=dict(lab="3つの答えの並べ", fields=dict(n=tuple(str(i) for i in range(len(VS_ROWS) + 1))), base=cmp_base, stage=cmp_stage),
)
VIEWS["cards"]["fields"]["n"] = tuple(str(i) for i in range(7))             # 🆕 ⑤b-6：勧告6つ（rec6）
VIEWS["layers"]["fields"]["ice"] = ONOFF                                      # 🆕 ⑤b-6（cb05）
VIEWS["org"]["fields"]["vac"] = ONOFF                                         # 🆕 ⑤b-6（cb08）
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
START["lars_side"]["lvl"] = "up"
HEAD_ONLY = dict(paper=("doc",), chat=("set",), depth=("z",), none=("set",), say=("set",), ruler=("z",), cards=("set",))
# 戻さない欄（増えた吹き出しは減らない・描いた深さの点は消えない・沈んだ台は浮かない）
ORDER = dict(chat=dict(n=tuple(str(i) for i in range(9))), depth=dict(upto=DP_ORDER), lars_side=dict(lvl=("up", "under")),
             none=dict(n=("0", "1", "2", "3")), say=dict(n=("0", "1", "2")), cards=dict(n=tuple(str(i) for i in range(7))),
             cmp=dict(n=tuple(str(i) for i in range(len(VS_ROWS) + 1))))
NOT_SCHEMATIC = ("table", "chat", "ruler")   # 原文の表と文の写し・🆕 ⑤b-4 縮尺どおりの深さの物差し（左上に「模式」を付けない）

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
    # 🆕 ⑤b-4（2026-10-15）
    send=dict(doubt=(SE["x0"], 352.0, "start", 1000.0)),
    proto=dict(look=(PR["xs"][0], 372.0, "middle", 400.0), t3=(PR["xs"][2], 372.0, "middle", 380.0), cut=(1400.0, 300.0, "middle", 640.0),
               bad=(1500.0, 732.0, "start", 340.0)),
    none=dict(t=(F.BX1 - 40.0, 320.0, "end", 760.0), low=(960.0, 800.0, "middle", 900.0)),
    say=dict(r=(SY["bx0"], 760.0, "start", 1000.0)),
    layers=dict(th=(LY["x1"] + 94.0, ly_top(LY_N) + 54.0, "start", 300.0), t=(1000.0, 330.0, "start", 440.0)),
    buckle=dict(r1=(1420.0, 470.0, "start", 420.0), r2=(1420.0, 640.0, "start", 420.0)),
    tc=dict(r1=(1420.0, 540.0, "start", 420.0), r2=(1420.0, 690.0, "start", 420.0)),
    shell=dict(r1=(1400.0, 450.0, "start", 440.0), r2=(1400.0, 580.0, "start", 440.0), r3=(1400.0, 710.0, "start", 440.0)),
    ruler=dict(doc=(700.0, 400.0, "start", 560.0), sf=(700.0, 480.0, "start", 560.0), dl=(1240.0, 680.0, "start", 380.0),
               low=(700.0, 770.0, "start", 600.0), low2=(RL["lx"], 730.0, "start", 470.0)),
    sf=dict(r1=(1420.0, 560.0, "start", 420.0), r2=(1420.0, 700.0, "start", 420.0)),
    model=dict(r1=(1300.0, 410.0, "start", 540.0), r2=(1300.0, 700.0, "start", 540.0)),
    klass=dict(q=(KL["own"][0], 330.0, "middle", 320.0)),
    wind=dict(low=(L_X, 800.0, "start", 400.0)),
    meet=dict(ask=(1400.0, 748.0, "middle", 440.0), rec=(620.0, 762.0, "start", 360.0)),   # ⚠️ geom_gap：y 712 だと札が机の右下の角に触れた
)
TAG_AT["paper"].update(r2=(1360.0, 560.0, "start", 460.0), r3=(1360.0, 740.0, "start", 460.0))   # 🆕 ⑤b-4：幅の広い紙（w 1060＝右の端 1310）の右
# 🆕 ⑤b-5（2026-10-15）：第8〜9章。⚠️ 出典の行（y 886）の上に 20px 以上あける（d は札の下 0.95 字）
TAG_AT["bow"].update(hit=(600.0, 470.0, "end", 480.0), hit2=(600.0, 600.0, "end", 480.0))
TAG_AT["ruler"].update(r1=(RL["lx"], 530.0, "start", 460.0), r2=(RL["lx"], 620.0, "start", 460.0), r3=(RL["lx"], 700.0, "start", 460.0))
TAG_AT.update(
    cards=dict(t=(F.BX1 - 40.0, 330.0, "end", 760.0), tl=(F.BX0 + 40.0, 330.0, "start", 760.0), low=(960.0, 800.0, "middle", 1300.0),
               low3=(1480.0, 800.0, "middle", 440.0), a12=(715.0, 400.0, "middle", 300.0), a23=(1205.0, 400.0, "middle", 300.0)),
    groove=dict(w=(GV["x0"] + gv_px(GV_END_IN) / 2, GV["top"] - 44, "middle", 600.0), cut=(1310.0, 512.0, "start", 500.0)),
    coupons=dict(a=((CPN["x0"] * 3 + CPN["x1"]) / 4, CPN["y0"] - 28, "middle", 500.0), c=((CPN["x0"] + CPN["x1"] * 3) / 4, CPN["y0"] - 28, "middle", 500.0)),
    shelf=dict(t=(F.BX1 - 40.0, 330.0, "end", 600.0)),
    d80=dict(bang=(1360.0, 360.0, "end", 400.0), boat=(1600.0, 330.0, "start", 240.0), inner=(1600.0, 470.0, "start", 240.0)),   # ⚠️ 門番 wording：「p1」は頁の形
    rtm=dict(t1=(120.0, 330.0, "start", 520.0), t2=(F.BX1 - 40.0, 330.0, "end", 520.0), l2=(120.0, 420.0, "start", 380.0)),
    # ⚠️ 門番 layout：up を x 700 に置くと次の段の幅の帯（15:15〜＝x 626〜）が札を覆った＝15:15 の左へ
    ae=dict(peak=(1200.0, 372.0, "start", 360.0), jump=(1200.0, 650.0, "start", 360.0), up=(612.0, 360.0, "end", 220.0),
            band=(1580.0, 590.0, "start", 260.0)),
    ctrl=dict(flip=(CT["r"][0], 380.0, "middle", 400.0)),
    stime=dict(hard=(960.0, 330.0, "middle", 900.0)),
    nonlin=dict(sh=(890.0, 420.0, "end", 360.0), deep=(350.0, 770.0, "start", 330.0), fwd=(1440.0, 760.0, "middle", 520.0)),
    screen=dict(mute=(SC["spk"][0], 640.0, "middle", 400.0), reset=(sc_x(20), 770.0, "middle", 400.0)),
    # 🆕 ⑤b-6（2026-10-15）
    temp=dict(hi=(TP["x"] + 80.0, tp_y(TP_HI) + 12.0, "start", 360.0), lo=(TP["x"] + 80.0, tp_y(TP_LO) + 12.0, "start", 360.0),
              wx=(1320.0, 420.0, "start", 500.0)),
    risk=dict(day=(rk_x(RK_DAY), RK["y"] + 120.0, "middle", 320.0), line=(rk_x(RK_STRIKE), RK["y"] - 124.0, "middle", 360.0),
              three=(RK["bx"][1], RK["by"] + 120.0, "middle", 400.0)),
    cols=dict(), cmp=dict(),
)
TAG_AT["cards"].update(b1=(520.0, 760.0, "middle", 420.0), b2=(960.0, 760.0, "middle", 420.0), b3=(1400.0, 760.0, "middle", 420.0))   # 🆕 ⑤b-6：3つの箱の下
TAG_AT["layers"].update(r2=(120.0, 340.0, "start", 440.0))      # 🆕 ⑤b-6（cb05）：左上＝輪切りの絵（y 398〜）と破線の上
TAG_AT["org"].update(eng=(750.0, 770.0, "middle", 520.0))       # 🆕 ⑤b-6（cb08）：空いた席（x 560〜940）の下＝2段目の席のすき間を線が通る


def anchors(view, st):
    """札から線を引く先（画面の点）。"""
    if view == "side":
        G = sd_geo()
        return dict(hull=((G["xc0"] + G["xc1"]) / 2, G["cy"] - G["R"]), dome=(G["xh0"] + 10, G["cy"] - G["R"] * 0.7),
                    cyl=((G["xc0"] + G["xc1"]) / 2, G["cy"]), crack=sd_cracks(G)[0])
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
    if view == "org":                 # 🆕 ⑤b-6（cb08）：空いた席の下の縁（線は2段目の席のすき間 x 730〜770 を通る）
        x, y = org_vacant_xy()
        return dict(eng=(x, y + ORG_H / 2 + 10))
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
    if view in ("none", "say", "cards"):     # 🆕 ⑤b-4・⑤b-5（cards）
        key = out[0]["set"]
        lim = len(NO[key]["items"]) if view == "none" else len(SAY[key]["bubbles"]) if view == "say" else len(CD[key]["cards"])
        if any(int(s["n"]) > lim for s in out):
            raise ValueError(f"m22：{view} の数が {key} の数（{lim}）を超える")
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
                   dome_x=G["xh0"], cyl=(G["xc0"], G["xc1"]), cracks=sd_cracks(G))
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
    # 🆕 ⑤b-4（2026-10-15）
    elif view == "send":
        out.update(n=SE_N, minutes=SE["min"], xs=se_xs())
    elif view == "proto":
        out.update(boxes=[(t, _rc(r)) for t, r in PR_T], best=PR_BEST)
    elif view == "none":
        out.update(set=start["set"], items=list(NO[start["set"]]["items"]))
    elif view == "say":
        d = SAY[start["set"]]
        out.update(set=start["set"], who=d["who"], col=_rc(d["role"]), bubbles=[tuple(b) for b in d["bubbles"]])
    elif view == "layers":
        out.update(n=LY_N, inch_cm=LY_IN_CM, sep=[tuple(p) for p in LY_SEP], void=[tuple(p) for p in LY_VOID],
                   inner_y=ly_top(1) + LY["th"] / 2, outer_y=ly_top(LY_N) + LY["th"] / 2)
    elif view == "buckle":
        rows = []
        for s in allst:
            o, i = buckle_parts(s)
            po, pi = o["pts"], i["pts"]
            mid = BK["n"] // 2
            rows.append(dict(split=s["split"], press=s["press"], th_out=po[-1][1] - po[0][1], gap=pi[0][1] - po[-1][1],
                             bow=po[mid][1] - po[0][1]))
        out.update(rows=rows, th=BK["th"], inner_down=BK_LAB["inner"] > BK_LAB["out"])
    elif view == "tc":
        out.update(sides={side: (head, outward, TC[side], tc_arrows(TC[side][0], TC[side][1], TC["R"], outward)) for side, _, head, _, outward in TC_SIDE})
    elif view == "shell":
        out.update(left=SH_L, right=SH_R)
    elif view == "ruler":
        z = start["z"]
        out.update(z=z, y0=RL["y0"], y1=RL["y1"], dmax=RL_Z[z], titanic=(TITANIC_M, rl_y(z, TITANIC_M)),
                   marks={k: (m, rl_y(z, m)) for k, (m, _, _) in RL_M.items()}, cols={k: _rc(r) for k, (_, _, r) in RL_M.items()}, ratio_n=3,
                   labs={k: t for k, (_, t, _) in RL_M.items()})
    elif view == "sf":
        out.update(op=SF["op"], k=SF["k"])
    elif view == "model":
        out.update(dome_m=MD_DOME_M)
    elif view == "klass":
        out.update(chk=list(KL_CHK), soc=KL_SOC, cert=KL_CERT)
    elif view == "meet":
        out.update(seats=[t for t, _, _ in MT_SEATS])
    # 🆕 ⑤b-5（2026-10-15）
    elif view == "cards":
        d = CD[start["set"]]
        out.update(set=start["set"], cards=[tuple(c[:3]) for c in d["cards"]], cols=[_rc(c[2]) for c in d["cards"]], life=CD_LIFE, loop=d.get("loop"))
    elif view == "groove":
        out.update(px_cm=GV["px_cm"], groove_px=gv_px(GV_IN), end_px=gv_px(GV_END_IN), groove_in=GV_IN, end_in=GV_END_IN)
    elif view == "coupons":
        out.update(rects=[(k, w, h) for k, _x, _y, w, h in cp_rects()])
    elif view == "shelf":
        out.update(load=SV_LOAD, req=SV_REQ, circ=SV_CIRC, labs=(sv_lab(SV_REQ), sv_lab(SV_CIRC)), gy0=SV["gy0"],
                   px_kg=(SV["gy0"] - SV["gy1"]) / SV["kmax"], y_req=sv_y(SV_LOAD * SV_REQ), y_circ=sv_y(SV_LOAD * SV_CIRC))
    elif view == "d80":
        out.update(pts=[(t, m, d80_xy(t, m)) for t, m in D80_PTS], bang=(D80_BANG, d80_xy(D80_BANG, 0)), D=dict(D80))
    elif view == "rtm":
        out.update(ae=[dd for _, _, dd in RT_AE], sg=len(RT_SG))
    elif view == "ae":
        out.update(up=AE_UP, esc=AE_ESC, peak=AE_PEAK, band=AE_BAND, jump_x=_ae_strain(True)[0][0], peak_x=ae_x(_ae_min(AE_PEAK)),
                   x_of={t: ae_x(_ae_min(t)) for t in (AE_UP, AE_ESC, AE_PEAK) + AE_BAND}, D=dict(AE))
    elif view == "ctrl":
        out.update(plain=ctrl_dirs(False), flip=ctrl_dirs(True))
    elif view == "stime":
        out.update(dives=list(STM_DIVES))
    elif view == "nonlin":
        st_, bent = nl_lines()
        out.update(straight=st_, bent=bent, sh=NL["sh"], gy0=NL["gy0"], gauge_x=NL["cx0"] + 26, cyl=(NL["cx0"], NL["cx1"]))
    elif view == "screen":
        out.update(y=SC_Y, r=SC_R, nmax=SC["nmax"])
    if view == "layers":
        out.update(grind=dict(LY_GRIND))
    if view == "dives":
        out.update(year=DV_YEAR)
    if view == "bow":
        out.update(hit=bw_hit(), w=BW_["w"])
    # 🆕 ⑤b-6（2026-10-15）
    if view == "temp":
        out.update(hi=TP_HI, lo=TP_LO, y_hi=tp_y(TP_HI), y_lo=tp_y(TP_LO), y0=tp_y(0), px_deg=(TP["y1"] - TP["y0"]) / (TP["vmax"] - TP["vmin"]))
    elif view == "risk":
        out.update(day=RK_DAY, strike=RK_STRIKE, n=len(RK["bx"]), x_day=rk_x(RK_DAY), x_line=rk_x(RK_STRIKE), x0=RK["x0"],
                   px=(RK["x1"] - RK["x0"]) / RK["vmax"])
    elif view == "cols":
        out.update(heads=[(nm, _rc(r)) for nm, r in CL_COL], tiers=[tuple(t) for t in CL_TIER],
                   items={f_: (c, tier, tuple(items)) for f_, (c, tier, items) in CL_ITEM.items()},
                   cols={f_: [_rc(r) for _t, r in items] for f_, (_c, _tier, items) in CL_ITEM.items()}, gap=CL_GAP, u7=CL_U7)
    elif view == "cmp":
        out.update(heads=[(nm, _rc(r)) for nm, r in VS_COL], rows=[tuple(r) for r in VS_ROWS])
    if view == "layers":
        out.update(ice=dict(x=LY_ICE["x"], top=ice_top(), outer=LY["y_in"] - LY_N * LY["th"], inner=LY["y_in"]))
    if view == "org":
        out.update(vac_xy=org_vacant_xy(), eng=anchors("org", start)["eng"])
    return out
