# -*- coding: utf-8 -*-
"""illu.py — 案C の型「再現イラスト」（2026-09-28 新設・14本目 ⑤b-2）。

■ 何か（ルール §5b-73〜76・Vault `Projects/事故検証-14本目-映像方針-案Cと競合の画面-20260926.md` §3〜§5・§7）
  文の出来事を、**記録どおりに**、描いた場面の上で起こす全面の絵（葦の ◎1 事実の再現・動）。
  平らな塗り・人は顔も服の細部も無い影。13本目までの紺の図とは見た目で別物（写真とも見分けられる）。
  見本＝Vault `Resources/事故検証ch-案C見本/mock_c103.html`（09-26 カズヤくん「このまま進める」）。

■ 仕組み（描く側＝`scene_jiko.build_layers`／`build_jiko.illu_frame`）
  1. 絵の部品（空と海・島・船・艇・人の影・音の輪・群れ）を**1つずつ SVG の層**にして PNG に1回だけ焼く。
     🔴 層の名前は `<cid>_il<番号>`＝`scene_jiko.KEEP_COLOR` が**章の色に置き換えない**（絵の色は全章で固定）。
        札（段ごとの `<cid>_a<番号>`）・左上の「再現イラスト」・右上の章・左下の出典は章の色の層のままでよい。
  2. 動きは PIL（Chrome をコマごとに呼ばない）。部品ごとの**段の鍵**（keys）＝位置 dx・dy／回転 rot（pivot のまわり・
     画面で時計回りが正＝`titan_fig.mech_pts` と同じ向き）／拡大 sc（pivot のまわり）／濃さ a。鍵のあいだは余弦の半周で移る
     （13本目 anim と同じ）。ほかに：人の影＝1枚の型紙（sprite）を道（inst の path）に沿って置く／音の輪＝輪の層を広げて
     薄める（pulse）／波＝横に流す（drift・1920 の周期で継ぎ目なし）／カメラ＝cam（z≧1＝寄りと引き）。
  3. 段＝台本の行。部品の状態は**段ごとに宣言**（`state=`）し、前の段から引き継ぐ（13本目 latch／section と同じ）。
     行より段が多いと、行のあいだに段が挟まる（`scene_jiko.stage_times`）。段ごとの出来事（`rings=`・`board=`）は引き継がない。

■ 置き場（使い回す絵）＝place
  A … 船を外から（船首の側から見た形）。傾き heel・船首の波 wake・船首の甲板のコンテナ boxes・カメラ cam
  D … A の船＋123艇・人の影（船員）・客室の窓の印 mark・窓の奥の群れ crowd（⑤b-3 で C・E と一緒に増やす）
  B … 船内（3階）。view＝corridor（閉じた客室の扉が並ぶ廊下とスピーカー）／cabin（客室で待つ群れとスピーカー）／
      desk（3階の案内デスクのマイク）。傾きは場面ごとに1つ（SVG で回して焼く＝段のあいだに変えない）

■ 守りの線（ルール §5b-74）と門番 `check_illu`（§5b-75）
  ① 描く物・人・動作・数・時刻は1つずつ出典（資料と頁＝`rec=`）。部品は置き場が既定の rec を持つ。記録の欄（傾き・波・
     コンテナ・群れ）を変える段と、段ごとの出来事（board・rings）は `rec=` を書く。頭の状態を既定から変えたら場面の `rec=`
  ② 人の影の役割＝船員・海洋警察・管制（型紙を道に沿って置く＝数えられる形）／乗客は**群れの型だけ**（`crowd_layout`＝
     重なって数えられない形・画面や窓の端で切れる）。群れを出す場面の時刻 `at` は `cuts.ss.ILLU_CROWD_UNTIL` より前
  ③ 描いた人の数（描く側が持つ inst の数）＝宣言（`people=dict(crew=(8, "判決 p11"))`）＝記録（宣言の rec）
  ④ 「再現イラスト」の札と出典（`overlay_svg`＝左上と左下）
  ⑤ 画面に出す時刻（札の文字）は、資料で割れる時刻（`cuts.ss.ILLU_SPLIT_TIMES`）でない
  ⑦ 写真・頁・決め所のカットに絵を置かない（混ざりは「冒頭の絵」`intro=dict(illu=…)`か「小さく戻す」`illu_pair` だけ）
  ⑧ 上から見た絵（view に「上から」）は、人が1画素に満たない縮尺（`scale`＝1画素あたりのメートルが 1.5 以上）
  ほかに `touch=`（記録の「どの甲板が水面に届いたか」）を、描く側と同じ幾何（`contact_y`）で確かめる

■ ほかの門番との約束（⑤b-2 で足した）
  ・全面の絵のカットは**見出し t・副題 s を書かない**（画面に出ない＝echo・dup・wording が画面に無い文字を測って鳴った）
  ・rec・people・state・start・place・touch は画面に出ない欄＝check_echo・check_wording は歩かない
  ・`_il` の層は絵＝地（写真と同じ）＝check_layout の「図形が文字を横切る」に数えない。冒頭の絵の層は決め所と別の画面
  ・小さく戻す絵の枠は中身が合成で入る＝check_box が外す
  ・下見＝`tools/illu_preview.py`（ブラウザで段の鍵を再生・§5b-76）。本番の確認は Actions
"""
from __future__ import annotations

import math
import re

import fontmetrics as fm
import titan_fig as F

W, H = 1920, 1080

# ── 絵の色（全章で固定）。🔴 章の色の置き換え（J.remap）が拾う値（J.PAL_TOKENS）を使わない＝check_illu が見る ──
C = dict(
    sky0="#7f9fb6", sky1="#d4dfe5", sea0="#5e8196", sea1="#23465a", seaf0="#4f7488", seaf1="#1f4155",
    isle="#8fa4b1", isle2="#9aadb9", wave="#9fbccb", foam="#e8f0f4",
    hull="#e9edf0", navy="#27405f", red="#94402f", deck="#eef1f3", edge="#93a2ac", win="#3a4f60",
    mast="#b9c3ca", box="#6f808b", box2="#56646e",
    boat="#e6ebee", boat_edge="#7f8d97", boat_navy="#2d4a73",
    fig="#1b2631", crowd0="#1b2631", crowd1="#2b3946", crowd2="#3b4a57",
    mark="#f2c14e", tag="#f3f6f8", ol="#1a2530",
    # 船内（色の記録は無い＝落ち着いた灰で抽象に）
    ceil="#c9d0d4", wall_l="#b7bfc4", wall_r="#a9b2b8", floor="#59636a", endw="#8e9aa2",
    door="#6c7c88", door_edge="#46535c", lamp="#f1f5f7", spk="#2f3a42", ring="#f2c14e",
    room="#b9c0c4", room_floor="#737d83", room_ceil="#c9cfd2", desk="#8a7a66", desk_top="#a4927b", mic="#2c343a",
)
CHIP_FG, CHIP_BG = "#f0d9a0", "#0d1115"

# 段の鍵の既定（秒）。行頭から動き出すまで・動ききるまで
KEY_DELAY, KEY_DUR = 0.25, 1.1


# ══════════════════════════════════════════════════════════
#  A・D　船（船首の側から見た形）
# ══════════════════════════════════════════════════════════
# 単位はメートル。x＝左舷が＋（船首の側から見るので画面の右）・y＝水面から上が＋。
# 幅 22.00 メートル・深さ 14.00 メートル（海審 p1013 の要目）。
# 🔴 甲板の高さは**記録の角度で、その甲板の左舷が水面に届く**ように決めた（海審 p1057：9時34分ごろ「B甲板の左舷が
#    水面に届くほど（約52.2度）」・9時46分ごろ「船橋甲板が水面に届くほど（約61.2度）」）。水面の中心で回すと、左舷の端
#    （x＝11）の高さ y が水面に届く角度は tan θ＝y／11 ＝ B甲板 14.18・船橋甲板 20.01 メートル（差 5.83＝甲板2つぶん
#    約2.9 メートルずつと合う）。＝絵の角度と記録の「どの甲板が水面に」が食い違わない（門番 check_illu の touch）。
#    ⚠️ そのぶん船体は実物より水面から高く出る（形は抽象＝§5b-74①「記録に無い細部は描かない」）
SHIP_HALF = 11.0


def deck_at(deg):
    """左舷の端（x＝11）が、傾き deg 度で水面に届く高さ（メートル）。"""
    return SHIP_HALF * math.tan(math.radians(deg))


B_DECK = deck_at(52.2)                        # 3階（B甲板）の床
BR_DECK = deck_at(61.2)                       # 5階（船橋甲板）の床
A_DECK = (B_DECK + BR_DECK) / 2               # 4階（A甲板）の床
HULL_TOP = B_DECK - (BR_DECK - B_DECK) / 2    # 船首の甲板（C甲板）
KEEL = HULL_TOP - 14.00                       # 船底（深さ 14.00 メートル）
ROOF = BR_DECK + 2.9
MAST_TOP = ROOF + 4.2
CONTACTS = {"3階（B甲板）の左舷": (SHIP_HALF, B_DECK), "船橋甲板の左舷": (SHIP_HALF, BR_DECK)}
DOOR_M = (7.2, BR_DECK + 0.05)                # 操舵室の左（左舷）の出入り口（判決 p18「조타실 좌측에 있는 출입문」）
TIP_M = (10.8, BR_DECK + 0.05)                # 船橋の張り出し（ウイング）の先

SHIP_S = 20.0                                 # 1メートル＝20画素（人の影 1.7 メートル＝34画素）
WATER = 640.0                                 # 水面＝回転の中心の高さ
HORIZON = 604.0
PIVOT = dict(A=(820.0, WATER), D=(640.0, WATER))
BOAT = dict(x0=1116.0, x1=1600.0, deck=612.0)  # 123艇（横から・艇首が左）。形は記録に無い＝仮（123艇の映像はなぞらない）
FIG_FOOT = (60.0, 120.0)                      # 人の影の型紙の足もと（層の中の位置）
FIG_H = 1.7 * SHIP_S


def to_px(x, y, piv):
    return (piv[0] + x * SHIP_S, piv[1] - y * SHIP_S)


def rot_pt(p, deg, piv):
    """画面の点 p を piv のまわりに deg 度回す（画面で時計回りが正）＝`titan_fig.mech_pts`・`build_jiko._il_paste` と同じ式。"""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    x, y = p[0] - piv[0], p[1] - piv[1]
    return (piv[0] + x * c - y * s, piv[1] + x * s + y * c)


def ship_pt(x, y, deg, piv):
    """船の点（メートル）が、傾き deg 度のとき画面のどこに来るか。"""
    return rot_pt(to_px(x, y, piv), deg, piv)


def contact_y(name, deg):
    """CONTACTS の点の、傾き deg 度での水面からの高さ（メートル・＋が上）。0 なら水面に届いている。"""
    piv = (0.0, 0.0)
    return -ship_pt(*CONTACTS[name], deg, piv)[1] / SHIP_S


def win_rects():
    """客室の窓の列（B・A の2列）＝[(x, y, 幅, 高さ)…]（メートル）。印（mark）と群れ（crowd）も同じ窓で切る。"""
    rows = []
    n, step, w, h = 15, 1.36, 0.8, 0.9
    for y0 in (B_DECK + 0.9, A_DECK + 0.9):
        x0 = -step * (n - 1) / 2 - w / 2
        rows.append([(x0 + i * step, y0, w, h) for i in range(n)])
    return rows


def _d(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def _rect(x, y, w, h, fill, stroke=None, sw=0, rx=0, op=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{s}{r}{o}/>'


def _mrect(x0, y0, x1, y1, piv, fill, stroke=None, sw=0, rx=0):
    """メートルの矩形（左下 x0,y0・右上 x1,y1）を画面の矩形に。"""
    (xa, ya), (xb, yb) = to_px(x0, y1, piv), to_px(x1, y0, piv)
    return _rect(xa, ya, xb - xa, yb - ya, fill, stroke, sw, rx)


def sky_svg(isles=True):
    """空・島影・奥の海（動かない地）。晴れて波の穏やかな朝（判決 p16「날씨가 맑고 파도가 잔잔」）。"""
    g = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{C["sky0"]}"/><stop offset="1" stop-color="{C["sky1"]}"/></linearGradient>'
         '<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{C["sea0"]}"/><stop offset="1" stop-color="{C["sea1"]}"/></linearGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="{HORIZON + 10:.0f}" fill="url(#sky)"/>']
    if isles:
        # 島影（事故の海はピョンプンド〈병풍도〉の北東 1.3 マイル＝海審 p1065）。島の形は記録に無い＝低い影だけ
        hz = HORIZON
        g.append(f'<path d="M 0 {hz + 2:.0f} L 0 {hz - 22:.0f} Q 120 {hz - 52:.0f} 250 {hz - 36:.0f} '
                 f'Q 330 {hz - 58:.0f} 430 {hz - 30:.0f} Q 500 {hz - 18:.0f} 560 {hz + 2:.0f} Z" fill="{C["isle"]}"/>')
        g.append(f'<path d="M 1540 {hz + 2:.0f} Q 1630 {hz - 24:.0f} 1720 {hz - 18:.0f} Q 1800 {hz - 30:.0f} '
                 f'1920 {hz - 12:.0f} L 1920 {hz + 2:.0f} Z" fill="{C["isle2"]}"/>')
    g.append(f'<rect x="0" y="{HORIZON:.0f}" width="{W}" height="{H - HORIZON:.0f}" fill="url(#sea)"/>')
    return "".join(g)


def waves_svg():
    """波の筋（横に流す＝drift）。🔴 1920 の周期で継ぎ目なし（build_jiko が画面の幅で巻き戻す）。"""
    import random
    rnd = random.Random("illu-waves")
    g = [f'<g stroke="{C["wave"]}" stroke-opacity="0.35" stroke-width="2" fill="none">']
    for y in (652, 676, 704, 738, 776, 820, 868):
        x, segs = rnd.uniform(0, 200), []
        while x < W:
            ln = rnd.uniform(90, 240) * (0.6 + 0.4 * (y - 640) / 240)
            segs.append(f"M {x:.0f} {y} h {min(ln, W - x):.0f}")
            x += ln + rnd.uniform(90, 210)
        g.append(f'<path d="{" ".join(segs)}"/>')
    g.append("</g>")
    return "".join(g)


def ship_svg(piv):
    """船（傾き0度で描く＝build_jiko が水面の中心 piv のまわりに回す）。色と姿は写真（海審 p1015〔그림1〕）から抽象に。"""
    P = lambda x, y: to_px(x, y, piv)  # noqa: E731
    hw = SHIP_HALF
    hull = [(-hw, HULL_TOP), (hw, HULL_TOP), (hw - 0.3, 6.5), (hw - 2.2, 1.8), (4.6, -1.0), (1.8, KEEL),
            (-1.8, KEEL), (-4.6, -1.0), (-hw + 2.2, 1.8), (-hw + 0.3, 6.5)]
    d = _d([P(*q) for q in hull])
    x0 = P(-hw - 1, 0)[0]
    x1 = P(hw + 1, 0)[0]

    def band(y_top, y_bot, col):
        ya, yb = P(0, y_top)[1], P(0, y_bot)[1]
        return _rect(x0, ya, x1 - x0, yb - ya, col)
    g = [f'<defs><clipPath id="hull"><path d="{d}"/></clipPath></defs><g clip-path="url(#hull)">',
         band(HULL_TOP + 1, 1.7, C["hull"]), band(1.7, 0.7, C["navy"]), band(0.7, KEEL - 1, C["red"]), '</g>',
         f'<path d="{d}" fill="none" stroke="{C["edge"]}" stroke-width="2" stroke-linejoin="round"/>']
    for y0, y1 in ((HULL_TOP, B_DECK), (B_DECK, A_DECK), (A_DECK, BR_DECK)):
        g.append(_mrect(-hw, y0, hw, y1, piv, C["deck"], C["edge"], 2))
    for row in win_rects():
        for (x, y, w, h) in row:
            g.append(_mrect(x, y, x + w, y + h, piv, C["win"]))
    # 船橋（5階）：張り出し（ウイング）の床は全幅・操舵室は真ん中（窓の帯）
    g += [_mrect(-hw, BR_DECK, hw, BR_DECK + 0.35, piv, C["deck"], C["edge"], 1.5),
          _mrect(-7.2, BR_DECK, 7.2, ROOF, piv, C["deck"], C["edge"], 2),
          _mrect(-6.6, BR_DECK + 1.2, 6.6, BR_DECK + 2.1, piv, C["navy"]),
          _mrect(-7.6, ROOF, 7.6, ROOF + 0.3, piv, "#d9dfe3", C["edge"], 1.5),
          _mrect(-0.15, ROOF + 0.3, 0.15, MAST_TOP, piv, C["mast"]),
          _mrect(-1.7, MAST_TOP - 0.8, 1.7, MAST_TOP - 0.55, piv, C["mast"])]
    return "".join(g)


# 船首の甲板（C甲板の前）のコンテナ＝2段（海審 p1097「선수갑판 2단에 적재된 컨테이너」・p1022「10피트 컨테이너」）。
# 🔴 箱の数は記録に無い＝**1つずつ数えられる継ぎ目を描かない**（段の線と筋だけ）。左舷の側の一部が海へ落ちる（海審 p1009）
BOX = dict(x0=-7.5, x1=7.5, split=2.5, tier=2.59)


def boxes_svg(piv, part):
    x0, x1 = (BOX["x0"], BOX["split"]) if part == "stay" else (BOX["split"] + 0.1, BOX["x1"])
    t = BOX["tier"]
    g = [_mrect(x0, HULL_TOP, x1, HULL_TOP + 2 * t, piv, C["box"], C["box2"], 2)]
    for k in (1, 2):
        y = HULL_TOP + k * t - (0.0 if k == 1 else 0.05)
        (xa, ya), (xb, _) = to_px(x0, y, piv), to_px(x1, y, piv)
        g.append(f'<path d="M {xa:.1f} {ya:.1f} H {xb:.1f}" stroke="{C["box2"]}" stroke-width="3"/>')
    for k in range(1, 6):                     # 板の筋（横だけ）
        y = HULL_TOP + k * t * 2 / 6
        (xa, ya), (xb, _) = to_px(x0 + 0.2, y, piv), to_px(x1 - 0.2, y, piv)
        g.append(f'<path d="M {xa:.1f} {ya:.1f} H {xb:.1f}" stroke="{C["box2"]}" stroke-width="1.2" opacity="0.6"/>')
    return "".join(g)


def box_fall_pt(heel, piv):
    """落ちるコンテナ（左舷の側）の真ん中が、傾き heel で滑り出したあと海へ届く点（画面）。"""
    cx = (BOX["split"] + BOX["x1"]) / 2
    p = ship_pt(cx + 7.0, HULL_TOP + BOX["tier"], heel, piv)
    return (p[0] + 40.0, WATER + 30.0)


def wake_svg(piv):
    """船首の波（進んでいる間だけ）。8時52分に止まる（判決 p11）と消える。"""
    x, y = piv
    g = [f'<path d="M {x - 250:.0f} {y + 3:.0f} Q {x - 130:.0f} {y - 11:.0f} {x:.0f} {y - 7:.0f} '
         f'Q {x + 130:.0f} {y - 11:.0f} {x + 250:.0f} {y + 3:.0f} Q {x + 130:.0f} {y + 12:.0f} {x:.0f} {y + 7:.0f} '
         f'Q {x - 130:.0f} {y + 12:.0f} {x - 250:.0f} {y + 3:.0f} Z" fill="{C["foam"]}" opacity="0.85"/>']
    for sgn in (-1, 1):
        for k in range(4):
            xa = x + sgn * (260 + 70 * k)
            g.append(f'<path d="M {xa:.0f} {y + 6 + 5 * k:.0f} q {sgn * 40} 4 {sgn * 80} 2" stroke="{C["foam"]}" '
                     f'stroke-width="3" fill="none" opacity="{0.7 - 0.13 * k:.2f}"/>')
    return "".join(g)


def front_sea_svg():
    """手前の海（沈んだ部分を覆う）。"""
    return ('<defs><linearGradient id="seaf" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{C["seaf0"]}" stop-opacity="0.80"/>'
            f'<stop offset="1" stop-color="{C["seaf1"]}" stop-opacity="0.97"/></linearGradient></defs>'
            f'<rect x="0" y="{WATER + 1:.0f}" width="{W}" height="{H - WATER - 1:.0f}" fill="url(#seaf)"/>'
            f'<path d="M 0 {WATER + 1:.0f} H {W}" stroke="#dbe7ee" stroke-opacity="0.35" stroke-width="2"/>')


def boat_svg():
    """123艇（横から見た形・艇首が左＝セウォル号の側）。100トン級の小型の警備艇（艇長の判決 p5002）。形は仮。"""
    x0, x1, dk = BOAT["x0"], BOAT["x1"], BOAT["deck"]
    hull = [(x0, dk - 2), (x1, dk - 2), (x1 - 8, WATER + 16), (x0 + 70, WATER + 16), (x0 + 24, WATER)]
    g = [f'<path d="{_d(hull)}" fill="{C["boat"]}" stroke="{C["boat_edge"]}" stroke-width="2"/>',
         _rect(x0 + 40, dk + 14, x1 - x0 - 48, 8, C["boat_navy"]),
         f'<path d="{_d([(x0 + 150, dk - 2), (x0 + 164, dk - 46), (x0 + 360, dk - 46), (x0 + 370, dk - 2)])}" '
         f'fill="#f2f4f5" stroke="{C["boat_edge"]}" stroke-width="2"/>']
    for k in range(5):
        g.append(_rect(x0 + 180 + 34 * k, dk - 38, 24, 15, C["win"]))
    g += [_rect(x0 + 262, dk - 100, 5, 54, "#aeb8bf"), _rect(x0 + 242, dk - 86, 45, 4, "#aeb8bf")]
    return "".join(g)


def fig_svg():
    """人の影の型紙（顔も服の細部も無い・足もとが FIG_FOOT）。"""
    x, y = FIG_FOOT
    h = FIG_H
    r = h * 0.17
    return (f'<circle cx="{x:.1f}" cy="{y - h + r:.1f}" r="{r:.1f}" fill="{C["fig"]}"/>'
            f'<path d="M {x - h * 0.22:.1f} {y - h * 0.64:.1f} Q {x:.1f} {y - h * 0.73:.1f} {x + h * 0.22:.1f} '
            f'{y - h * 0.64:.1f} L {x + h * 0.27:.1f} {y:.1f} L {x - h * 0.27:.1f} {y:.1f} Z" fill="{C["fig"]}"/>')


def board_spots(n):
    """123艇の甲板の、乗り移った人の立つ所（画面）。🔴 影どうし重ならない間隔＝1人ずつ数えられる（門番 ③）。"""
    return [(BOAT["x0"] + 70 + 26 * j, BOAT["deck"]) for j in range(n)]


def board_path(j, heel, piv):
    """j 人目の道：操舵室の左の出入り口 → 張り出しの先 → 123艇の甲板（判決 p18）。"""
    return [ship_pt(*DOOR_M, heel, piv), ship_pt(*TIP_M, heel, piv), board_spots(j + 1)[j]]


def marks_svg(piv):
    """客室の窓の列の印（見本 c103 の黄色い枠）。"""
    g = []
    for row in win_rects():
        x0, y0 = row[0][0] - 0.25, row[0][1] - 0.25
        x1, y1 = row[-1][0] + row[-1][2] + 0.25, row[0][1] + row[0][3] + 0.25
        g.append(_mrect(x0, y0, x1, y1, piv, "none", C["mark"], 3.5, rx=4))
    return "".join(g)


# ══════════════════════════════════════════════════════════
#  乗客の群れ（顔の無い群れ＝重なって数えられない形・端で切れる）
# ══════════════════════════════════════════════════════════
# 🔴 門番 check_illu ② が同じ関数で測る：隣の影と2割以上重なる・並びが切る枠の外まで続く（端で切れる）
CROWD_STEP = 0.62          # 隣の影との間隔（影の幅に対する割合）


def crowd_layout(x0, x1, base, w, rows=3, row_dy=None):
    """群れの影の並び [(左端 x, 足もとの y, 幅, 列)…]。x0〜x1 は切る枠＝その外まで並べる。列0 が手前。"""
    out = []
    row_dy = row_dy or w * 0.42
    for r in range(rows):
        ww = w * (1 - 0.06 * r)
        step = ww * CROWD_STEP
        x = x0 - ww * 0.9 + (r % 2) * step * 0.5
        while x <= x1 + ww * 0.1:
            out.append((x, base - r * row_dy, ww, r))
            x += step
    return out


def crowd_uncountable(layout, x0, x1):
    """群れが「数えられない形」か（門番 ②）。返り値＝理由の一覧（空なら合格）。"""
    bad = []
    for r in sorted({q[3] for q in layout}):
        row = sorted([q for q in layout if q[3] == r])
        if not row:
            continue
        if row[0][0] >= x0 or row[-1][0] + row[-1][2] <= x1:
            bad.append(f"群れの列{r}が枠の端で切れていない（左 {row[0][0]:.0f}／右 {row[-1][0] + row[-1][2]:.0f}・枠 {x0:.0f}〜{x1:.0f}）")
        for a, b in zip(row, row[1:]):
            ov = (a[0] + a[2] - b[0]) / a[2]
            if ov < 0.2:
                bad.append(f"群れの列{r}で隣の影の重なりが {ov:.0%}（2割未満＝1人ずつ数えられる）")
                break
    return bad


def crowd_svg(layout, cols=None):
    cols = cols or (C["crowd0"], C["crowd1"], C["crowd2"])
    g = []
    for x, by, w, r in sorted(layout, key=lambda q: -q[3]):     # 奥の列から
        col = cols[min(r, len(cols) - 1)]
        cx = x + w / 2
        g.append(f'<circle cx="{cx:.1f}" cy="{by - w * 0.80:.1f}" r="{w * 0.21:.1f}" fill="{col}"/>'
                 f'<path d="M {x:.1f} {by:.1f} L {x + w * 0.08:.1f} {by - w * 0.40:.1f} Q {cx:.1f} {by - w * 0.66:.1f} '
                 f'{x + w * 0.92:.1f} {by - w * 0.40:.1f} L {x + w:.1f} {by:.1f} Z" fill="{col}"/>')
    return "".join(g)


def win_crowd(piv):
    """窓の奥の群れ（D・9時46分より前だけ）。窓の列ごとに並べて、窓の矩形で切る。返り値＝(SVG, 列ごとの並び・枠)。"""
    rows = []
    clips, g = [], []
    for k, row in enumerate(win_rects()):
        x0 = to_px(row[0][0], 0, piv)[0]
        x1 = to_px(row[-1][0] + row[-1][2], 0, piv)[0]
        base = to_px(0, row[0][1] + 0.35, piv)[1]
        lay = crowd_layout(x0, x1, base, 0.78 * SHIP_S, rows=2)
        rows.append((lay, x0, x1))
        cp = "".join(_mrect(x, y, x + w, y + h, piv, "#000") for (x, y, w, h) in row)
        clips.append(f'<clipPath id="wc{k}">{cp}</clipPath>')
        g.append(f'<g clip-path="url(#wc{k})">{crowd_svg(lay)}</g>')
    return "<defs>" + "".join(clips) + "</defs>" + "".join(g), rows


# ══════════════════════════════════════════════════════════
#  B　船内（3階）
# ══════════════════════════════════════════════════════════
# 絵は SVG で傾けて焼く（場面ごとに傾きは1つ）。傾ける向きは A と同じ＝**画面の右が下**（左舷へ傾く・A と見た向きを揃えた）
CB = (960.0, 450.0)            # 船内の絵を回す中心
# 部屋（回す前の画面の座標）。画面より広く描く＝62.6度まで回しても端が空かない。
# ⑤b-2 の下見：①先を見通す遠近の廊下は 62.6度で何の絵か読めなかった ②客室の群れが小さく端の細い帯になった
#   → 廊下は**扉の並ぶ壁を正面から**（向かいの壁を見る＝回すと画面の中で傾く）・客室は群れに寄って大きく
ROOM = dict(x0=-900.0, x1=2820.0, y0=-900.0, y1=1800.0, ceil=170.0, floor=600.0)
CORR = dict(ceil=200.0, floor=760.0, door_w=176.0, door_h=410.0, pitch=440.0, x0=-760.0)
CORR_SPK = (1275.0, 290.0)
CABIN_SPK = (1430.0, 290.0)
DESK_MIC = (1052.0, 352.0)


def _rot_g(inner, deg):
    return f'<g transform="rotate({deg:.2f} {CB[0]:.0f} {CB[1]:.0f})">{inner}</g>'


def corridor_spk():
    """廊下の壁のスピーカーの真ん中（回す前の画面）。"""
    return CORR_SPK


def corridor_svg(deg):
    """閉じた客室の扉が並ぶ廊下の壁（正面から）。人は描かない。画面の右が下へ傾く（A と同じ向き）。"""
    r, c = ROOM, CORR
    g = [_rect(r["x0"], r["y0"], r["x1"] - r["x0"], c["ceil"] - r["y0"], C["ceil"]),
         _rect(r["x0"], c["ceil"], r["x1"] - r["x0"], c["floor"] - c["ceil"], C["wall_l"]),
         _rect(r["x0"], c["floor"], r["x1"] - r["x0"], r["y1"] - c["floor"], C["floor"]),
         f'<path d="M {r["x0"]:.0f} {c["ceil"]:.0f} H {r["x1"]:.0f}" stroke="{C["door_edge"]}" stroke-width="4"/>',
         f'<path d="M {r["x0"]:.0f} {c["floor"]:.0f} H {r["x1"]:.0f}" stroke="{C["door_edge"]}" stroke-width="5"/>',
         _rect(r["x0"], c["floor"] - 22, r["x1"] - r["x0"], 22, C["wall_r"])]          # 幅木
    for k in range(10):
        x = c["x0"] + k * c["pitch"]
        g.append(_rect(x - 12, c["floor"] - c["door_h"] - 12, c["door_w"] + 24, c["door_h"] + 12, C["door_edge"]))
        g.append(_rect(x, c["floor"] - c["door_h"], c["door_w"], c["door_h"], C["door"]))
        g.append(_rect(x + c["door_w"] - 30, c["floor"] - c["door_h"] * 0.5, 12, 34, C["door_edge"], rx=4))
        g.append(_rect(x + c["pitch"] / 2 + 40, c["ceil"] + 4, 90, 14, C["lamp"], rx=4))   # 天井の灯り
    sx, sy = CORR_SPK
    g.append(_rect(sx - 44, sy - 28, 88, 56, C["spk"], C["ol"], 3, rx=6))
    for k in range(4):
        g.append(f'<path d="M {sx - 30:.0f} {sy - 15 + 10 * k:.0f} H {sx + 30:.0f}" stroke="#56646e" stroke-width="4"/>')
    return _rot_g("".join(g), deg)


# 小さな位置の図（B の左上・ルール §5b-80「見る向きを替えるときは合図」）：A と同じ船首の側から見た船を、
# その場面の傾きで小さく描き、客室の階（B・A＝3階・4階＝海審 p1019・p1023）に色を付ける＝「この船の中の、この傾き」
INSET = dict(x=72.0, y=150.0, w=250.0, h=176.0, s=3.6)


def inset_svg(deg):
    x, y, w, h, s = INSET["x"], INSET["y"], INSET["w"], INSET["h"], INSET["s"]
    px, py = x + w * 0.42, y + h * 0.66

    def P(mx, my):
        return (px + mx * s, py - my * s)

    def mr(x0, y0, x1, y1, fill, stroke=None):
        (xa, ya), (xb, yb) = P(x0, y1), P(x1, y0)
        return _rect(xa, ya, xb - xa, yb - ya, fill, stroke, 1.2 if stroke else 0)
    hw = SHIP_HALF
    hull = [(-hw, HULL_TOP), (hw, HULL_TOP), (hw - 0.3, 6.5), (hw - 2.2, 1.8), (4.6, -1.0), (1.8, KEEL),
            (-1.8, KEEL), (-4.6, -1.0), (-hw + 2.2, 1.8), (-hw + 0.3, 6.5)]
    ship = (f'<path d="{_d([P(*q) for q in hull])}" fill="{C["hull"]}" stroke="{C["edge"]}" stroke-width="1.2"/>'
            + mr(-hw, HULL_TOP, hw, B_DECK, C["deck"], C["edge"]) + mr(-hw, B_DECK, hw, BR_DECK, C["mark"], C["edge"])
            + mr(-7.2, BR_DECK, 7.2, ROOF, C["deck"], C["edge"]) + mr(-0.2, ROOF, 0.2, MAST_TOP, C["mast"]))
    return (f'<defs><clipPath id="inset"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/></clipPath></defs>'
            f'<g clip-path="url(#inset)">{_rect(x, y, w, py - y, "#d4dfe5")}'
            f'<g transform="rotate({deg:.2f} {px:.1f} {py:.1f})">{ship}</g>'
            f'{_rect(x, py, w, y + h - py, C["seaf0"], op=0.88)}</g>'
            f'{_rect(x, y, w, h, "none", "#e3eaee", 2, rx=6)}'
            + tag_svg(x + 10, y + h + 34, "客室の階（色）", cap=22, col=C["mark"]))


def room_svg(deg, desk=False):
    """客室（または3階の案内デスクのある所）の奥の壁・床・天井。記録に無い並び・物は描かない。"""
    r = ROOM
    g = [_rect(r["x0"], r["y0"], r["x1"] - r["x0"], r["ceil"] - r["y0"], C["room_ceil"]),
         _rect(r["x0"], r["ceil"], r["x1"] - r["x0"], r["floor"] - r["ceil"], C["room"]),
         _rect(r["x0"], r["floor"], r["x1"] - r["x0"], r["y1"] - r["floor"], C["room_floor"]),
         f'<path d="M {r["x0"]:.0f} {r["ceil"]:.0f} H {r["x1"]:.0f} M {r["x0"]:.0f} {r["floor"]:.0f} H {r["x1"]:.0f}" '
         f'stroke="{C["door_edge"]}" stroke-width="3"/>']
    if desk:
        mx, my = DESK_MIC
        g += [_rect(500, 470, 900, 28, C["desk_top"], C["door_edge"], 2),
              _rect(520, 498, 860, 210, C["desk"], C["door_edge"], 2),
              f'<ellipse cx="{mx - 56:.0f}" cy="468" rx="34" ry="9" fill="{C["mic"]}"/>',
              f'<path d="M {mx - 56:.0f} 466 L {mx - 56:.0f} {my + 64:.0f} Q {mx - 54:.0f} {my + 16:.0f} {mx - 12:.0f} {my + 6:.0f}" '
              f'stroke="{C["mic"]}" stroke-width="8" fill="none" stroke-linecap="round"/>',
              f'<rect x="{mx - 18:.0f}" y="{my - 14:.0f}" width="40" height="28" rx="12" fill="{C["mic"]}"/>']
    else:
        sx, sy = CABIN_SPK
        g.append(_rect(sx - 44, sy - 28, 88, 56, C["spk"], C["ol"], 3, rx=6))
        for k in range(4):
            g.append(f'<path d="M {sx - 30:.0f} {sy - 15 + 10 * k:.0f} H {sx + 30:.0f}" stroke="#56646e" stroke-width="4"/>')
    return _rot_g("".join(g), deg)


def cabin_crowd(deg):
    """客室で待つ乗客の群れ（判決 p18「선내에 대기」）。返り値＝(SVG, 並び, 枠 x0, x1)。
    ⚠️ 大きさは画面で読める大きさ（影の幅 118画素）＝人数は名乗らない（重なって数えられない・端で切れる）"""
    lay = crowd_layout(ROOM["x0"], ROOM["x1"], ROOM["floor"] + 190, 128, rows=3)   # 下見：高いと左上の位置の図に掛かった
    return _rot_g(crowd_svg(lay), deg), lay, ROOM["x0"], ROOM["x1"]


def ring_svg(c, dir_deg, r=64):
    """音の輪（1本の弧）。c を中心に dir_deg の向きへ開く 110 度の弧（build_jiko が c のまわりに広げて薄める）。"""
    pts = F._arc(c[0], c[1], r, dir_deg - 55, dir_deg + 55, 24)
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{C["ol"]}" stroke-opacity="0.55" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{C["ring"]}" stroke-width="6" stroke-linecap="round"/>')


# ══════════════════════════════════════════════════════════
#  札（段ごとの `_a<番号>`）と、左上の「再現イラスト」・左下の出典
# ══════════════════════════════════════════════════════════
def tag_svg(x, y, t, to=None, anchor="start", col=None, cap=30):
    col = col or C["tag"]
    s = fm.fit(t, 620, "Noto", cap=cap, floor=20)
    g = []
    if to:
        g.append(f'<path d="M {to[0]:.1f} {to[1]:.1f} L {x:.1f} {y - s * 0.35:.1f}" stroke="{C["ol"]}" '
                 f'stroke-width="6" fill="none" stroke-linecap="round"/>'
                 f'<path d="M {to[0]:.1f} {to[1]:.1f} L {x:.1f} {y - s * 0.35:.1f}" stroke="{col}" stroke-width="2.5" fill="none"/>'
                 f'<circle cx="{to[0]:.1f}" cy="{to[1]:.1f}" r="5" fill="{col}" stroke="{C["ol"]}" stroke-width="2"/>')
    tx = x + (10 if anchor == "start" else -10 if anchor == "end" else 0)
    g.append(f'<text x="{tx:.1f}" y="{y:.1f}" font-family="Noto" font-size="{s}" fill="{col}" text-anchor="{anchor}" '
             f'stroke="{C["ol"]}" stroke-width="6" stroke-linejoin="round" paint-order="stroke fill">{F.esc(t)}</text>')
    return "".join(g)


CHIP = (72, 32, 208, 50)       # 見本は x 36＝画面の余白（J.MG＝72）の外だった＝check_layout に合わせて寄せた
SRC_Y = 884


def overlay_svg(view, src):
    """左上の「再現イラスト」の札（と見る向き）・左下の出典（ルール §5b-74③・§5b-80）。check_illu ④ が同じ関数で見る。"""
    x, y, w, h = CHIP
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{CHIP_BG}" fill-opacity="0.62" '
         f'stroke="{CHIP_FG}" stroke-width="2"/>',
         f'<text x="{x + w / 2:.0f}" y="{y + 35}" font-family="Noto" font-size="28" fill="{CHIP_FG}" '
         f'text-anchor="middle">再現イラスト</text>']
    if view:
        g.append(f'<text x="{x + 4}" y="{y + h + 34}" font-family="Noto" font-size="24" fill="#e3eaee" '
                 f'stroke="#10161b" stroke-width="5" stroke-linejoin="round" paint-order="stroke fill">{F.esc(view)}</text>')
    if src:
        s = fm.fit(src, 1500, "Noto", cap=22, floor=15)
        g.append(f'<text x="{x}" y="{SRC_Y}" font-family="Noto" font-size="{s}" fill="#e3eaee" stroke="#10161b" '
                 f'stroke-width="4" stroke-linejoin="round" paint-order="stroke fill">{F.esc(src)}</text>')
    return "".join(g)


def _docs():
    try:
        import cuts.ss as ss
        return getattr(ss, "REC_DOCS", {}) or {}
    except Exception:                                   # noqa: BLE001
        return {}


def parse_rec(r, docs=None):
    """「判決 p11・p18（…）／海審 p1057」→ [("判決", [11, 18]), ("海審", [1057])]。資料名は長い名前から当てる。"""
    docs = docs if docs is not None else _docs()
    names = sorted(docs, key=len, reverse=True) or ["判決", "海審"]
    s = str(r or "")
    hits = list(re.finditer("(" + "|".join(map(re.escape, names)) + r")\s*p\d", s))
    out = []
    for k, m in enumerate(hits):
        # その資料名から次の資料名までの「p頁」を全部（括弧の注釈をまたいで「・p18」と続く書き方も拾う）
        seg = s[m.start(1) + len(m.group(1)): hits[k + 1].start() if k + 1 < len(hits) else len(s)]
        out.append((m.group(1), [int(x) for x in re.findall(r"(?<![0-9A-Za-z])p(\d+)", seg)]))
    return out


def rec_line(recs, docs=None):
    """出典の行（左下）。資料ごとに頁をまとめる。"""
    docs = docs if docs is not None else _docs()
    by, order = {}, []
    for r in recs:
        for doc, pages in parse_rec(r, docs):
            if doc not in by:
                by[doc] = []
                order.append(doc)
            by[doc] += [p for p in pages if p not in by[doc]]
    parts = []
    for doc in order:
        d = docs.get(doc, {})
        ps = sorted(by[doc])
        if d.get("page") == "pdf":
            pg = "PDF " + "・".join(str(p - d.get("base", 0)) for p in ps) + "頁"
        elif d.get("page") == "print":
            pg = "・".join(str(p - d.get("base", 0)) for p in ps) + "頁"
        else:
            pg = ""
        parts.append(f"{d.get('name', doc)} {pg}".strip())
    return ("出典：" + "／".join(parts)) if parts else ""


# ══════════════════════════════════════════════════════════
#  場面（scene）＝部品と鍵
# ══════════════════════════════════════════════════════════
FIELDS = {
    "A": dict(heel=0.0, wake="on", boxes="off", cam=1.0),
    "D": dict(heel=61.2, mark="off", crowd="off", cam=1.0),
    "B": dict(view="corridor", heel=0.0, crowd="off", cam=1.0),
}
CHOICES = dict(wake=("on", "off"), boxes=("off", "on", "fall", "fell"), mark=("off", "on"), crowd=("off", "on"),
               view=("corridor", "cabin", "desk"))
REC_FIELDS = ("heel", "wake", "boxes", "crowd")          # 変える段には rec が要る（記録の事実を描く欄）
EVENTS = ("rings", "board")                              # 段ごとの出来事（引き継がない）
VIEW = dict(A="船首の側から見た図", D="船首の側から見た図", B="船の中")
ROLES = ("crew", "coast_guard", "control")                # 型紙（数えられる影）で置ける役割
CAM_C = dict(A=(820.0, 420.0), D=(990.0, 560.0), B=CB)


def _check_state(place, st):
    for k, v in st.items():
        if k not in FIELDS[place]:
            raise ValueError(f"illu {place}：知らない欄 {k!r}（使えるのは {tuple(FIELDS[place])}）")
        if k in CHOICES and v not in CHOICES[k]:
            raise ValueError(f"illu {place}：{k}={v!r} は知らない状態（{CHOICES[k]}）")
        if k == "cam" and float(v) < 1.0:
            raise ValueError("illu：cam（寄り）は 1.0 以上（引きすぎると画面の端が空く）")


def _states(place, start, steps):
    base = dict(FIELDS[place], **(start or {}))
    _check_state(place, base)
    cur, out = dict(base), []
    for sp in steps:
        cur = dict(cur, **(sp.get("state") or {}))
        _check_state(place, cur)
        out.append(dict(cur))
    return base, out


def _keys(start, states, steps, fn):
    """部品の鍵。鍵0＝カットの頭・鍵 i+1＝段 i（行頭＋delay から dur 秒で移る）。fn は状態 → dict(rot, dx, dy, sc, a)。"""
    ks = [dict(stage=0, delay=0.0, dur=KEY_DUR, **fn(start))]
    for i, (st, sp) in enumerate(zip(states, steps)):
        ks.append(dict(stage=i, delay=float(sp.get("delay", KEY_DELAY)), dur=float(sp.get("dur", KEY_DUR)), **fn(st)))
    return ks


def _part(pid, svg, rec, pivot=(0.0, 0.0), keys=None, **kw):
    return dict(id=pid, svg=svg, rec=rec, pivot=list(pivot), keys=keys or [dict(stage=0, delay=0.0)], kind="layer", **kw)


def _vis(on):
    return dict(a=1.0 if on else 0.0)


def _ship_parts(place, start, states, steps, piv):
    """A と D の共通：空・波・船（傾き）。"""
    rot = lambda st: dict(rot=float(st["heel"]))  # noqa: E731
    return [_part("sky", sky_svg(), "判決 p16（晴れ・波が穏やか）・海審 p1065（ピョンプンドの北東）"),
            dict(_part("waves", waves_svg(), "判決 p16（波が穏やか）"), drift=-9.0),
            _part("ship", ship_svg(piv), "海審 p1013（幅 22.00・深さ 14.00 メートル）・p1015（〔그림1〕の写真）", piv,
                  _keys(start, states, steps, rot))]


def _scene_A(start, states, steps):
    piv = PIVOT["A"]
    parts = _ship_parts("A", start, states, steps, piv)
    if any(st["boxes"] != "off" for st in [start] + states):
        heel_of = lambda st: float(st["heel"])  # noqa: E731
        parts.append(_part("boxes_stay", boxes_svg(piv, "stay"), "海審 p1097（船首の甲板に2段）・p1022（10フィートのコンテナ）",
                           piv, _keys(start, states, steps,
                                      lambda st: dict(rot=heel_of(st), **_vis(st["boxes"] != "off")))))
        # 落ちる一部：段の鍵のほかに「滑り出す→海へ」の2つの鍵を足す（その段の中で）
        # boxes：off＝描かない／on＝全部／fall＝この段で左舷の側の一部が落ちる／fell＝落ちたあと（残った側だけ）
        ks = [dict(stage=0, delay=0.0, dur=KEY_DUR, rot=heel_of(start), dx=0.0, dy=0.0,
                   **_vis(start["boxes"] == "on"))]
        fallen = start["boxes"] in ("fall", "fell")
        for i, (st, sp) in enumerate(zip(states, steps)):
            dl, du = float(sp.get("delay", KEY_DELAY)), float(sp.get("dur", KEY_DUR))
            if st["boxes"] == "fall" and not fallen:
                h = heel_of(st)
                slide = 8.0 * SHIP_S                                   # 甲板に沿って左舷へ 8 メートル
                sx, sy = slide * math.cos(math.radians(h)), slide * math.sin(math.radians(h))
                ks.append(dict(stage=i, delay=dl, dur=0.7, rot=h, dx=sx, dy=sy, a=1.0))
                ks.append(dict(stage=i, delay=dl + 0.7, dur=0.9, rot=h + 25.0, dx=sx + 60.0, dy=sy + 260.0, a=0.0))
                fallen = True
            else:
                ks.append(dict(stage=i, delay=dl, dur=du, rot=ks[-1]["rot"] if fallen else heel_of(st),
                               dx=ks[-1]["dx"], dy=ks[-1]["dy"],
                               a=0.0 if (fallen or st["boxes"] != "on") else 1.0))
        parts.append(_part("boxes_fall", boxes_svg(piv, "fall"), "海審 p1009（船首の甲板のコンテナが傾きで海へ）", piv, ks))
    parts += [_part("front_sea", front_sea_svg(), "判決 p16"),
              _part("wake", wake_svg(piv), "判決 p11（8時52分に止まる）", piv,
                    _keys(start, states, steps, lambda st: _vis(st["wake"] == "on")))]
    return parts


def _scene_D(start, states, steps):
    piv = PIVOT["D"]
    parts = _ship_parts("D", start, states, steps, piv)
    rot = lambda st: float(st["heel"])  # noqa: E731
    parts.append(_part("mark", marks_svg(piv), "判決 p18（乗客は船内で待っていた）", piv,
                       _keys(start, states, steps, lambda st: dict(rot=rot(st), **_vis(st["mark"] == "on")))))
    if any(st["crowd"] == "on" for st in [start] + states):
        svg, rows = win_crowd(piv)
        parts.append(_part("crowd", svg, "判決 p18（乗客は船内で待っていた）", piv,
                           _keys(start, states, steps, lambda st: dict(rot=rot(st), **_vis(st["crowd"] == "on"))),
                           role="passengers", crowd=[dict(layout=lay, x0=x0, x1=x1) for lay, x0, x1 in rows]))
    parts.append(_part("boat", boat_svg(), "判決 p18（操舵室の前に着いた123艇）・艇長の判決 p5002（100トン級）"))
    inst, n = [], 0
    for i, (st, sp) in enumerate(zip(states, steps)):
        for j in range(int(sp.get("board") or 0)):
            # 「차례로（順に）」（判決 p18）＝1人ずつ間を置いて（見本は 0.62秒。行の尺に収めるため既定 0.45秒）
            inst.append(dict(stage=i, delay=float(sp.get("delay", 0.3)) + float(sp.get("gap", 0.45)) * j,
                             path=[list(p) for p in board_path(n, rot(st), piv)]))
            n += 1
    if inst:
        parts.append(dict(_part("crew", fig_svg(), "判決 p11（操舵室に8人）・p18（9時46分に123艇へ）"),
                          kind="sprite", foot=list(FIG_FOOT), inst=inst, role="crew"))
    parts.append(_part("front_sea", front_sea_svg(), "判決 p16"))
    return parts


def _scene_B(start, states, steps):
    deg = float(start["heel"])
    if any(float(st["heel"]) != deg for st in states):
        raise ValueError("illu B：船内の傾きは場面の頭（start）で1つだけ（段で変えない＝SVG で傾けて焼く）")
    views = {start["view"]} | {st["view"] for st in states}
    parts = []
    vis = lambda name: (lambda st: _vis(st["view"] == name))  # noqa: E731
    rings = {}
    if "corridor" in views:
        parts.append(_part("corridor", corridor_svg(deg), "海審 p1019（3階＝B甲板に客室が並ぶ）", CB,
                           _keys(start, states, steps, vis("corridor"))))
        rings["corridor"] = (rot_pt(corridor_spk(), deg, CB), 90.0 + deg)       # 壁から廊下へ（回す前は真下）
    if "cabin" in views:
        parts.append(_part("cabin", room_svg(deg), "判決 p18（乗客は客室で待っていた）", CB,
                           _keys(start, states, steps, vis("cabin"))))
        svg, lay, x0, x1 = cabin_crowd(deg)
        parts.append(_part("crowd", svg, "判決 p18（乗客は船内で待っていた）", CB,
                           _keys(start, states, steps, lambda st: _vis(st["view"] == "cabin" and st["crowd"] == "on")),
                           role="passengers", crowd=[dict(layout=lay, x0=x0, x1=x1)]))
        rings["cabin"] = (rot_pt(CABIN_SPK, deg, CB), 125.0 + deg)       # 左下の群れの側へ
    if "desk" in views:
        parts.append(_part("desk", room_svg(deg, desk=True), "判決 p13（3階の案内デスクの乗務員が放送した）", CB,
                           _keys(start, states, steps, vis("desk"))))
        rings["desk"] = (rot_pt(DESK_MIC, deg, CB), -40.0 + deg)         # マイクから外へ
    parts.append(_part("inset", inset_svg(deg), "海審 p1013（要目）・p1019・p1023（客室の階＝B・A甲板）"))
    for name, (c, dirn) in rings.items():
        pulse = []
        for i, (st, sp) in enumerate(zip(states, steps)):
            if st["view"] == name and sp.get("rings"):
                pulse.append(dict(stage=i, delay=float(sp.get("ring_delay", 0.3)), n=int(sp["rings"]), gap=0.8,
                                  dur=1.4, s0=0.5, s1=2.2))
        if pulse:
            parts.append(dict(_part(f"ring_{name}", ring_svg(c, dirn), "海審 p1053〜p1055（船内の放送）", c),
                              kind="ring", pulse=pulse))
    return parts


def _anchors(place, st):
    """札の指し先（その段の終わりの状態で）。"""
    if place in ("A", "D"):
        piv, h = PIVOT[place], float(st["heel"])
        a = {"b_port": ship_pt(SHIP_HALF, B_DECK, h, piv), "br_port": ship_pt(SHIP_HALF, BR_DECK, h, piv),
             "boxes_sea": box_fall_pt(h, piv), "win": ship_pt(3.0, A_DECK + 1.35, h, piv),
             "boxes": ship_pt(-2.0, HULL_TOP + BOX["tier"] * 1.5, h, piv),
             "boat": (BOAT["x0"] + 264.0, BOAT["deck"] - 100.0), "ship": ship_pt(0.0, ROOF, h, piv)}
        return a
    deg = float(st["heel"])
    return {"desk": rot_pt((960.0, 560.0), deg, CB), "spk": rot_pt(CABIN_SPK, deg, CB),
            "corr_spk": rot_pt(corridor_spk(), deg, CB), "crowd": rot_pt((900.0, ROOM["floor"] + 60), deg, CB)}


def scene(place, steps, start=None, at=None, people=None, src=None, view=None, rec=None, scale=None, camc=None):
    """再現イラストの場面1つ（型 `illu`・冒頭の絵 `intro=dict(illu=…)`・小さく戻す `illu_pair` が使う）。

    place  … 置き場 "A"／"B"／"D"（上の説明）
    start  … 頭の状態（既定は FIELDS）。steps … 台本の行ごとの段 dict(state=dict(…), rec="資料 p頁", tag=…,
             rings=数〈B の音の輪〉, board=数〈D の乗り移る人〉, delay=秒, dur=秒, touch="3階（B甲板）の左舷")
    at     … 場面の時刻（宣言・画面には出さない）。人を描く場面は必須（門番 ②）
    people … 描いた人の数の宣言 dict(crew=(8, "判決 p11"))（門番 ③）
    src    … 左下の出典（省略時は部品と段の rec から組む）
    view   … 左上の見る向き（省略時は置き場の既定）。scale … 上から見た絵の縮尺（メートル／画素）
    """
    if place not in FIELDS:
        raise ValueError(f"illu：知らない置き場 {place!r}（{tuple(FIELDS)}）")
    steps = [dict(s) for s in steps]
    for sp in steps:
        bad = set(sp) - {"state", "rec", "tag", "rings", "board", "gap", "delay", "dur", "ring_delay", "touch"}
        if bad:
            raise ValueError(f"illu：段に知らない鍵 {sorted(bad)}")
    st0, states = _states(place, start, steps)
    parts = {"A": _scene_A, "B": _scene_B, "D": _scene_D}[place](st0, states, steps)
    cam = _keys(st0, states, steps, lambda st: dict(z=float(st["cam"])))
    tags = []
    for i, (st, sp) in enumerate(zip(states, steps)):
        g, texts, keep, dl = [], [], False, 0.35
        an = _anchors(place, st)
        for tg in F._many(sp.get("tag")):
            to = an[tg["at"]] if isinstance(tg.get("at"), str) else tg.get("at")
            ox, oy = tg.get("off", (60, -70))
            x, y = (to[0] + ox, to[1] + oy) if to else tuple(tg["xy"])
            g.append(tag_svg(x, y, tg["t"], to=to, anchor=tg.get("anchor", "start"), col=tg.get("col")))
            texts.append(tg["t"])
            keep = keep or bool(tg.get("keep"))
            dl = float(tg.get("delay", dl))
        tags.append(dict(svg="".join(g) or " ", texts=texts, keep=keep, delay=dl))
    recs = [p["rec"] for p in parts] + [sp.get("rec") for sp in steps if sp.get("rec")] + ([rec] if rec else [])
    recs += [v[1] for v in (people or {}).values() if isinstance(v, (tuple, list)) and len(v) > 1]
    return dict(place=place, view=view or VIEW[place], at=at, people=dict(people or {}), scale=scale, rec=rec,
                parts=parts, cam=cam, camc=list(camc or CAM_C[place]), tags=tags, nstage=len(steps),
                start=st0, states=states, steps=steps, recs=recs, src=src or rec_line(recs))


def strip(sc):
    """描く側（meta）へ渡す形＝部品の SVG を落とす（子プロセスへ運ぶ量を減らす）。"""
    out = dict(sc, parts=[{k: v for k, v in p.items() if k != "svg"} for p in sc["parts"]],
               tags=[{k: v for k, v in t.items() if k != "svg"} for t in sc["tags"]])
    for k in ("steps", "states", "start"):
        out.pop(k, None)
    return out


# ══════════════════════════════════════════════════════════
#  型（titan_fig から `fig=("illu", …)`・`fig=("illu_pair", …)` で呼ぶ）
# ══════════════════════════════════════════════════════════
def illu(place, steps, **kw):
    """全面の再現イラスト（画面の種類「再現イラスト」）。段＝台本の行（札は段の層 `_a<番号>`）。"""
    sc = scene(place, steps, **kw)
    f = F.Fig("", [t["svg"] for t in sc["tags"]], "", (0, W))
    f.illu = dict(full=True, scenes=[dict(sc, role="main", box=None)], view=sc["view"], src=sc["src"])
    return f


PAIR_BOX = ((96, 262, 840, 473), (984, 262, 840, 473))


def illu_pair(blocks, lead=""):
    """2つの問いのパネルの中に、再現イラストを小さく戻す（画面の種類「混ざり」・14本目 c105・c108）。

    blocks … [dict(k="問い1", t="なぜ傾いたか", v="…", stage=段, scene=dict(place="A", steps=[…], …)), 2つ]
             段の数は台本の行の数（`stages=`）。絵は block の stage の行頭から見せる（それまでは枠だけ）。
    """
    if len(blocks) != 2:
        raise ValueError("illu_pair：問いは2つ")
    n = max(int(b.get("stages", 1)) for b in blocks)
    stages = [[] for _ in range(n)]
    lab, scenes, recs = [], [], []
    for b, (x, y, w, h) in zip(blocks, PAIR_BOX):
        sc = scene(**b["scene"])
        if sc["nstage"] != n:
            raise ValueError(f"illu_pair：{b['k']} の絵の段 {sc['nstage']} が行の数 {n} と違う")
        if any(t["texts"] for t in sc["tags"]):
            raise ValueError("illu_pair：小さく戻す絵に札（tag）は付けない（小さくて読めない）")
        scenes.append(dict(sc, role="mini", box=[x, y, w, h], show=int(b.get("stage", 0))))
        recs += sc["recs"]
        lab.append(_rect(x - 3, y - 3, w + 6, h + 6, "none", "#e3eaee", 3, rx=6))
        # 🔴 「再現イラスト」の札は段の層へ（build_jiko は 骨格→小さな絵→段 の順に重ねる＝札が絵の上に来る）
        i = int(b.get("stage", 0))
        cx, cy, cw, ch = x + 12, y + 12, 170, 40
        stages[i].append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="5" fill="{CHIP_BG}" fill-opacity="0.66" '
                         f'stroke="{CHIP_FG}" stroke-width="2"/>'
                         f'<text x="{cx + cw / 2:.0f}" y="{cy + 29}" font-family="Noto" font-size="23" fill="{CHIP_FG}" '
                         f'text-anchor="middle">再現イラスト</text>')
        stages[i].append(F.txtfit(x, y + h + 58, b["k"], 200, cap=34, col=F.J.AMBER))
        stages[i].append(F.txtfit(x + 150, y + h + 58, b["t"], w - 150, cap=44, col=F.J.INK_W))
        if b.get("v"):
            stages[i].append(F.txtfit(x + 150, y + h + 104, b["v"], w - 150, cap=30, col=F.J.TICK))
    src = rec_line(recs)
    lab.append(F.txtfit(F.BX0, F.BY1 - 6, (lead + "　" if lead else "") + src, F.BW, cap=24, col=F.J.TICK))
    f = F.Fig("".join(lab), ["".join(s) or " " for s in stages], "", (0, W))
    f.illu = dict(full=False, scenes=scenes, view="", src=src)
    return f
