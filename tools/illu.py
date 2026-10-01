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
  A … 船を外から（船首の側から見た形）。傾き heel・船首の波 wake・船首の甲板のコンテナ boxes・操舵室の印 bridge・カメラ cam
  D … 123艇のまわり。view で見え方を選ぶ（⑤b-3 で広げた）：
      ship＝A の船＋123艇・人の影（船員）・客室の窓の印 mark・窓の奥の群れ crowd（c103・c911）／
      sea＝海を進む123艇（横から・bx＝艇首の位置・run＝進む波・far＝遠くのセウォル号・spk＝放送の設備）／
      far＝123艇から見た遠くの船（mark・binoc＝双眼鏡の丸い視野が甲板→海をなぞる）／
      heli＝船の上のヘリ1機と吊り下げの線／rail＝3階の左舷の手すりとゴムボート（rboat・cg＝立った乗組員・board＝乗り移る人）
  B … 船内（3階）。view＝corridor（閉じた客室の扉が並ぶ廊下とスピーカー）／cabin（客室で待つ群れとスピーカー）／
      desk（3階の案内デスクのマイク）。傾きは場面ごとに1つ（SVG で回して焼く＝段のあいだに変えない）
  C … 操舵室（5階）の中（⑤b-3）。view＝helm（舵の前の当直）／console（無線機と船内放送の機器の寄り＝人は枠の外）／
      room（操舵室の中の人の影）。傾きは B と同じく場面ごとに1つ。出来事＝rings（無線機から外へ）・rings_in（外から
      無線機へ）・glow（放送の機器の電源の灯）・asks（問いかけの印）・walkie（3階からの無線機）
  E … 管制センターの中（⑤b-3）。管制の画面（レーダー）と船の点・交信の装備。人は描かない（管制官の人数が記録に無い）。
      sel＝画面の船の点に印・出来事 rings（交信の装備から外へ）
  ── 15本目（リノ・エアレース2011・⑤b-2）＝頭に R を付けた別の鍵（A〜E は14本目の船＝selftest の見本が使う）──
  RA … 上から見たステッド空港（北が上）。view＝wide（コース全体）／near（パイロン7・8と駐機場）／ramp（駐機場の寄り）。
       事故機の印 gg（off／p7／p8／gone＝道に沿って進み 0秒で消える）・点線 path（模式）・琥珀の線 trace・× x・ボックス席 box・
       3周の航跡 laps・パイロン6〜7 seg67・パイロン8の輪 ring8・一片が見つかった所 piece・燃料車の輪 fuel・コースの破線 course
  RB … 空の中の事故機。view＝side（横から・機首が右）／rear（後ろから）＝段で入れ替えてよい。ground（on＝丘と砂漠）・
       pitch（機首の上げ・度）・roll（左への傾き・度）・ail（補助翼 off／right）・出来事 rings（テレメトリー）・pylon（1本流れる）
  RD … ピットの事故機（⑤b-2 は c109 の小さな絵の尾翼の寄り tail だけ・mark＝尾翼の輪）＝⑤b-3 で本格的に
  動きの部品（build_jiko）：draw（線を道の頭から見せる）・mover（印が道を進み向きを変える）・akeys（濃さだけの鍵）
  ── 16本目（バイオントダム災害・⑤b-2）＝頭に V の別の鍵 ──
  VA … 上から見た谷（北が上）。view＝wide（谷の全体）／near（ダムと崩れた斜面）／west（峡谷の出口とピアーヴェ川の谷）。
       tod（day／night・段で night→dawn）・block（崩れたあとの塊）・slide（崩れた範囲）・towns／shore（建物の面 on／gone／mud）・
       tunnel・split（会社の説明の想定＝off／on／flow）・road（off／on／low＝730m未満）・gates・marks（北の岸の930m）・
       wave_w（西へダムを越える水）・flood（ピアーヴェ川の谷へ広がる水）・wave_e（東へ向かった波）・
       見る向きの合図＝prev（頭だけ：B／C／D の切り口の線と目の印）・nxt（次の断面の線）・switch（頭だけ：「上から見ると」）。
       形のもと＝#100（1934年の地形図）を目で読んだ点（正本 ref/ep16/map16.json）＝上の「16本目」の節

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
    lamp_on="#9fe07e",                        # ⑤b-3：操舵室の船内放送の機器の電源の灯（色は記録に無い＝点いていることだけ）
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
# 123艇（横から・艇首が左）。🔴 ⑤b-3：全長は記録にある＝**32.2 メートル**（艇長の判決 p5002「100톤급 경비정으로 총톤수
#   121톤, 전장 32.2m, 폭 6m」）＝⑤b-2 の仮の 24.2 メートルを直した（艇首の側＝乗り移る所・札の指し先は変えていない）。
#   高さ・上部の形は記録に無い＝仮（123艇の映像はなぞらない）
BOAT_L = 32.2
BOAT = dict(x0=1116.0, x1=1116.0 + BOAT_L * SHIP_S, deck=612.0)
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


def front_sea_svg(y=WATER, x0=0.0, x1=float(W)):
    """手前の海（沈んだ部分を覆う）。y＝水面（既定は A・D の WATER）。"""
    return ('<defs><linearGradient id="seaf" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{C["seaf0"]}" stop-opacity="0.80"/>'
            f'<stop offset="1" stop-color="{C["seaf1"]}" stop-opacity="0.97"/></linearGradient></defs>'
            f'<rect x="{x0:.0f}" y="{y + 1:.0f}" width="{x1 - x0:.0f}" height="{H - y - 1:.0f}" fill="url(#seaf)"/>'
            f'<path d="M {x0:.0f} {y + 1:.0f} H {x1:.0f}" stroke="#dbe7ee" stroke-opacity="0.35" stroke-width="2"/>')


# 123艇の横の形（艇首＝0・艇尾＝全長。メートル・水面から上が＋）。⑤b-2 の画素の形をメートルに直した（20画素＝1メートル）。
#   記録は全長・幅・100トン級だけ（艇長の判決 p5002）＝高さ・上部の形・放送の設備の位置は仮
BOAT_M = dict(deck=1.5, keel=-0.8, cab=((7.5, 1.5), (8.2, 3.7), (18.0, 3.7), (18.5, 1.5)), mast=13.1, mast_top=6.4,
              spk=(8.6, 3.7))


def boat123_svg(x0, water, s, spk=False):
    """123艇（横から見た形・艇首が左）。x0＝艇首の画面の x・water＝水面の y・s＝1メートルの画素。"""
    L, M = BOAT_L, BOAT_M
    P = lambda x, y: (x0 + x * s, water - y * s)  # noqa: E731
    k = s / SHIP_S
    hull = [P(0, M["deck"]), P(L, M["deck"]), P(L - 0.4, M["keel"]), P(3.5, M["keel"]), P(1.2, 0.0)]
    (sx0, sy0), (sx1, sy1) = P(2.0, 0.7), P(L - 0.4, 0.3)
    g = [f'<path d="{_d(hull)}" fill="{C["boat"]}" stroke="{C["boat_edge"]}" stroke-width="{2 * k:.1f}"/>',
         _rect(sx0, sy0, sx1 - sx0, sy1 - sy0, C["boat_navy"]),
         f'<path d="{_d([P(*q) for q in M["cab"]])}" fill="#f2f4f5" stroke="{C["boat_edge"]}" stroke-width="{2 * k:.1f}"/>']
    for j in range(5):
        (wx, wy) = P(9.0 + 1.7 * j, 3.3)
        g.append(_rect(wx, wy, 1.2 * s, 0.75 * s, C["win"]))
    (mx, my), (bx, by) = P(M["mast"], M["mast_top"]), P(12.1, 5.7)
    g += [_rect(mx, my, 0.25 * s, 2.7 * s, "#aeb8bf"), _rect(bx, by, 2.25 * s, 0.2 * s, "#aeb8bf")]
    if spk:
        # 外へ呼びかける放送の設備（艇長の判決 p5002「I방송장비」）。位置と形は記録に無い＝屋根の上の小さなラッパの形
        (hx, hy) = P(*M["spk"])
        u = s * 1.5                                    # 下見：0.9 では小さくて見えなかった
        g.append(f'<path d="M {hx + 0.3 * u:.1f} {hy:.1f} V {hy - 0.35 * u:.1f}" stroke="#7f8d97" stroke-width="{0.12 * u:.1f}"/>'
                 f'<path d="M {hx + 0.55 * u:.1f} {hy - 0.62 * u:.1f} L {hx + 0.10 * u:.1f} {hy - 0.52 * u:.1f} '
                 f'L {hx - 0.45 * u:.1f} {hy - 0.80 * u:.1f} L {hx - 0.45 * u:.1f} {hy - 0.18 * u:.1f} '
                 f'L {hx + 0.10 * u:.1f} {hy - 0.40 * u:.1f} L {hx + 0.55 * u:.1f} {hy - 0.30 * u:.1f} Z" '
                 f'fill="#dfe5e9" stroke="{C["ol"]}" stroke-width="{0.08 * u:.1f}" stroke-linejoin="round"/>')
    return "".join(g)


def boat_svg():
    """123艇（c103 の置き場 D・ship）。操舵室の前＝艇首が左＝セウォル号の側。"""
    return boat123_svg(BOAT["x0"], WATER, SHIP_S)


def fig_svg(h=None, deg=0.0, foot=None, col=None):
    """人の影の型紙（顔も服の細部も無い・足もとが foot）。h＝背の高さの画素・deg＝足もとのまわりに傾ける（船内の傾き）。"""
    h = float(h or FIG_H)
    x, y = foot or FIG_FOOT
    r = h * 0.17
    col = col or C["fig"]
    g = (f'<circle cx="{x:.1f}" cy="{y - h + r:.1f}" r="{r:.1f}" fill="{col}"/>'
         f'<path d="M {x - h * 0.22:.1f} {y - h * 0.64:.1f} Q {x:.1f} {y - h * 0.73:.1f} {x + h * 0.22:.1f} '
         f'{y - h * 0.64:.1f} L {x + h * 0.27:.1f} {y:.1f} L {x - h * 0.27:.1f} {y:.1f} Z" fill="{col}"/>')
    return f'<g transform="rotate({deg:.2f} {x:.1f} {y:.1f})">{g}</g>' if deg else g


def big_foot(h):
    """大きな型紙の足もと（層の中）。62.6度まで傾けても層の外に出ない位置。"""
    return (h * 1.05, h * 1.35)


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
        # ⑤b-2 の試し焼き：暗い窓（#3a4f60）に暗い影（#1b2631）では群れが見えなかった＝窓の奥を明るく敷いてから影を置く
        lit = "".join(_mrect(x, y, x + w, y + h, piv, "#9fb3c2") for (x, y, w, h) in row)
        g.append(f'{lit}<g clip-path="url(#wc{k})">{crowd_svg(lay)}</g>')
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
# ⑤b-2 の試し焼き：左上に置くと客室の群れの帯（画面の左上から右下へ）と重なった＝左下（出典の上）へ
INSET = dict(x=72.0, y=600.0, w=250.0, h=176.0, s=3.6)


def inset_svg(deg, part="cabin"):
    """位置の図。part＝cabin（客室の階＝3・4階に色）／bridge（操舵室＝5階の船橋に色・⑤b-3 の置き場 C）。"""
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
    cab, brg = (C["mark"], C["deck"]) if part == "cabin" else (C["deck"], C["mark"])
    ship = (f'<path d="{_d([P(*q) for q in hull])}" fill="{C["hull"]}" stroke="{C["edge"]}" stroke-width="1.2"/>'
            + mr(-hw, HULL_TOP, hw, B_DECK, C["deck"], C["edge"]) + mr(-hw, B_DECK, hw, BR_DECK, cab, C["edge"])
            + mr(-7.2, BR_DECK, 7.2, ROOF, brg, C["edge"]) + mr(-0.2, ROOF, 0.2, MAST_TOP, C["mast"]))
    return (f'<defs><clipPath id="inset"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/></clipPath></defs>'
            f'<g clip-path="url(#inset)">{_rect(x, y, w, py - y, "#d4dfe5")}'
            f'<g transform="rotate({deg:.2f} {px:.1f} {py:.1f})">{ship}</g>'
            f'{_rect(x, py, w, y + h - py, C["seaf0"], op=0.88)}</g>'
            f'{_rect(x, y, w, h, "none", "#e3eaee", 2, rx=6)}'
            + tag_svg(x + 10, y + h + 34, "客室の階（色）" if part == "cabin" else "操舵室（色）", cap=22, col=C["mark"]))


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


def ask_svg(c):
    """問いかけの印（吹き出しの「？」）。c＝吹き出しの真ん中。字は立てたまま（読めるように）。"""
    x, y = c
    return (f'<path d="M {x - 40:.0f} {y - 34:.0f} H {x + 40:.0f} Q {x + 52:.0f} {y - 34:.0f} {x + 52:.0f} {y - 22:.0f} '
            f'V {y + 16:.0f} Q {x + 52:.0f} {y + 28:.0f} {x + 40:.0f} {y + 28:.0f} H {x - 6:.0f} L {x - 30:.0f} {y + 50:.0f} '
            f'L {x - 24:.0f} {y + 28:.0f} H {x - 40:.0f} Q {x - 52:.0f} {y + 28:.0f} {x - 52:.0f} {y + 16:.0f} V {y - 22:.0f} '
            f'Q {x - 52:.0f} {y - 34:.0f} {x - 40:.0f} {y - 34:.0f} Z" fill="{C["tag"]}" stroke="{C["ol"]}" stroke-width="4"/>'
            f'<text x="{x:.0f}" y="{y + 15:.0f}" font-family="Noto" font-size="44" fill="{C["ol"]}" '
            f'text-anchor="middle">？</text>')


def glow_svg(c, r=24):
    """電源の灯のまわりの光の輪（広げて薄める）。"""
    return (f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r}" fill="none" stroke="{C["lamp_on"]}" stroke-width="7"/>'
            f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r + 7}" fill="none" stroke="{C["ol"]}" stroke-opacity="0.4" stroke-width="3"/>')


def seascape_svg(horizon, x0=0.0, x1=float(W), lines=True):
    """窓・双眼鏡の奥の空と海（水平のまま）。晴れて波が穏やか（判決 p16）。"""
    g = ['<defs><linearGradient id="csky" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{C["sky0"]}"/><stop offset="1" stop-color="{C["sky1"]}"/></linearGradient>'
         '<linearGradient id="csea" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{C["sea0"]}"/><stop offset="1" stop-color="{C["sea1"]}"/></linearGradient></defs>',
         f'<rect x="{x0:.0f}" y="-1400" width="{x1 - x0:.0f}" height="{horizon + 1402:.0f}" fill="url(#csky)"/>',
         f'<rect x="{x0:.0f}" y="{horizon:.0f}" width="{x1 - x0:.0f}" height="{H + 1400 - horizon:.0f}" fill="url(#csea)"/>']
    if lines:
        g.append(f'<g stroke="{C["wave"]}" stroke-opacity="0.3" stroke-width="2">')
        for j, dy in enumerate((22, 48, 80, 118, 164)):
            for xa in range(int(x0) + (j * 97) % 240, int(x1), 380):
                g.append(f'<path d="M {xa} {horizon + dy:.0f} h {110 + (j * 37) % 90}"/>')
        g.append("</g>")
    return "".join(g)


def wave_band_svg(ys, seed="illu-cwaves", op=0.35):
    """波の筋（横に流す drift・画面の幅で巻き戻す）。ys＝筋の y の並び。"""
    import random
    rnd = random.Random(seed)
    g = [f'<g stroke="{C["wave"]}" stroke-opacity="{op}" stroke-width="2" fill="none">']
    for y in ys:
        x, segs = rnd.uniform(0, 200), []
        while x < W:
            ln = rnd.uniform(70, 200)
            segs.append(f"M {x:.0f} {y:.0f} h {min(ln, W - x):.0f}")
            x += ln + rnd.uniform(80, 200)
        g.append(f'<path d="{" ".join(segs)}"/>')
    g.append("</g>")
    return "".join(g)


# ══════════════════════════════════════════════════════════
#  C　操舵室（5階・船橋）の中 ── 14本目 ⑤b-3（2026-09-29）
# ══════════════════════════════════════════════════════════
# 🔴 記録にあるもの：操舵室の放送の機器・非常ベル・船内電話・無線機（判決 p16・p17・p49「조타실 내의 비상벨의 이용,
#    방송장비 또는 선내전화기를 통한 안내방송, 무전기를 통한 사무부에의 지시 등 조타실에서 손쉽게 할 수 있었다」）／
#    VHF の交信（判決 p11・海審 p1058）／操舵手が舵を回す（海審 p1047）／非常電源が来ていた（海審 p1060 注30）。
#    形・並び・色・計器は記録に無い＝抽象（平らな塗り・細部なし）。
# 絵は B と同じく**場面ごとに傾き1つ**を SVG で回して焼く（画面の右が下＝左舷）。**窓の外の海は回さない**（水平＝傾いたのは船）。
# 人の影は1人ずつ数えられる型紙（sprite）＝門番 ③。🔴 **影は立てたまま（重力の向き）**・足もとだけ傾いた床に置く
#   （⑤b-3 の下見：部屋と一緒に 45度傾けると、8人が斜めに寝そべった帯に見えて数えにくく、重力まで傾いた絵になった）。
# 🔴 人数（⑤b-3 で原文に当てた）：8時30分〜8時50分は当直2人＋機関長の3人（海審 p1047・p1048）／8時52分〜9時00分ごろは
#    判決 p11 の8人＋機関長の9人（機関長は9時00〜05分に出た＝海審 p1055・船員の2審 p5007）／9時25分ごろは8人（判決 p14）。
#    ＝helm は**舵の前だけの寄り**（当直の2人）・部屋の全体に人を置くのは 9時05分より後の room だけ
CCEN = dict(helm=(960.0, 540.0), console=(960.0, 450.0), room=(960.0, 480.0))    # 回す中心
HELM = dict(k=176.0, feet=830.0, wall=760.0, horizon=452.0)   # k＝1メートルの画素（背 1.7メートル＝300画素）
CONS = dict(wtop=110.0, wbot=520.0, top=560.0, face=600.0, horizon=380.0)
# room：背 1.7メートル＝160画素・床に沿って 116画素ずつ＝45度の床で画面の縦に 82画素ずつずれる（背の半分 80 より大きい＝
#   門番 ③ の「重ならない」）。8人の並びが 45度でも画面の上下に収まる長さ（812画素）
ROOMC = dict(k=94.0, feet=600.0, wall=560.0, horizon=380.0)
HELM_FIG = ((1075.0, 830.0), (1345.0, 830.0))       # 操舵手（舵の右）・3等航海士の足もと（回す前）
ROOM_FIG = tuple((494.0 + 116.0 * j, 600.0) for j in range(8))
ROOM_ASKER, ROOM_CAPTAIN = 2, 5                     # 問いかける2等航海士・船長（並びの中のどの影かは記録に無い＝仮）
HELM_WHEEL = (945.0, 612.0)
CONS_RADIO = (700.0, 400.0)                         # VHF の表示窓（輪の中心）
CONS_PA = (1300.0, 478.0)                           # 船内放送の機器
CONS_LAMP = (1460.0, 420.0)                         # 船内放送の機器の電源の灯
ROOM_WALKIE = (1400.0, 440.0)                       # 3階と話す無線機（手に持つ形・机の上）


def _c_frame(view):
    """見え方ごとの 天井・窓の上・窓の下・机の上・机の前（回す前の y）と窓の枠の間隔・幅。"""
    if view == "helm":
        k, wall = HELM["k"], HELM["wall"]
        return dict(wt=wall - 2.4 * k, wb=wall - 1.12 * k, top=wall - 1.0 * k, face=wall - 0.94 * k, floor=wall,
                    pitch=300.0, mw=22.0)
    if view == "room":
        k, wall = ROOMC["k"], ROOMC["wall"]
        return dict(wt=wall - 2.3 * k, wb=wall - 1.1 * k, top=wall - 0.95 * k, face=wall - 0.88 * k, floor=wall,
                    pitch=230.0, mw=16.0)
    return dict(wt=CONS["wtop"], wb=CONS["wbot"], top=CONS["top"], face=CONS["face"], floor=None, pitch=460.0, mw=28.0)


def c_room_svg(view):
    """操舵室の壁・窓の枠・天井・机・床（回す前の画面の座標）。窓は抜いてある＝下の層の海が見える。"""
    X0, X1, Y0, Y1 = -1100.0, 3020.0, -1100.0, 2000.0
    f = _c_frame(view)
    g = [_rect(X0, Y0, X1 - X0, f["wt"] - Y0, C["ceil"]),
         _rect(X0, f["wt"] - 26, X1 - X0, 26, C["wall_r"]),
         _rect(X0, f["wb"], X1 - X0, f["top"] - f["wb"], C["wall_l"])]
    x = X0
    while x < X1:                                        # 窓の枠（縦）
        g.append(_rect(x, f["wt"], f["mw"], f["wb"] - f["wt"], C["door_edge"]))
        x += f["pitch"]
    g += [f'<path d="M {X0:.0f} {f["wt"]:.1f} H {X1:.0f} M {X0:.0f} {f["wb"]:.1f} H {X1:.0f}" stroke="{C["door_edge"]}" '
          f'stroke-width="8"/>',
          _rect(X0, f["top"], X1 - X0, f["face"] - f["top"], C["desk_top"]),                    # 机の上
          _rect(X0, f["face"], X1 - X0, (f["floor"] or Y1) - f["face"], C["desk"])]             # 机の前
    if f["floor"] is not None:
        g.append(_rect(X0, f["floor"], X1 - X0, Y1 - f["floor"], C["floor"]))
        g.append(f'<path d="M {X0:.0f} {f["floor"]:.1f} H {X1:.0f}" stroke="{C["door_edge"]}" stroke-width="4"/>')
    if view == "helm":
        # 舵（操舵台）＝台と小さな輪（形は記録に無い＝抽象）。当直の操舵手が回す（海審 p1047）
        wx, wy = HELM_WHEEL
        g += [_rect(wx - 42, wy + 24, 84, HELM["feet"] - wy - 24, "#56626b", C["ol"], 3, rx=8),
              f'<circle cx="{wx:.0f}" cy="{wy:.0f}" r="58" fill="none" stroke="{C["mic"]}" stroke-width="12"/>',
              f'<circle cx="{wx:.0f}" cy="{wy:.0f}" r="12" fill="{C["mic"]}"/>']
        for a in (0, 60, 120):
            r = math.radians(a)
            g.append(f'<path d="M {wx - 56 * math.cos(r):.1f} {wy - 56 * math.sin(r):.1f} L {wx + 56 * math.cos(r):.1f} '
                     f'{wy + 56 * math.sin(r):.1f}" stroke="{C["mic"]}" stroke-width="7"/>')
    elif view == "console":
        # VHF の無線機（左）：箱・表示窓・スピーカーの格子・つまみ。形は抽象（機種は記録に無い）
        rx, ry = CONS_RADIO
        g += [_rect(rx - 150, ry - 70, 440, 240, "#3a464f", C["ol"], 4, rx=10),
              _rect(rx - 120, ry - 38, 230, 76, "#15242d", "#0c1418", 3, rx=6),
              f'<path d="M {rx - 104:.0f} {ry:.0f} H {rx + 90:.0f}" stroke="#6fa38a" stroke-width="5" opacity="0.8"/>']
        for j in range(6):
            g.append(f'<path d="M {rx + 140:.0f} {ry - 40 + 16 * j:.0f} H {rx + 262:.0f}" stroke="#1f2a31" stroke-width="7"/>')
        g += [f'<circle cx="{rx - 70:.0f}" cy="{ry + 110:.0f}" r="18" fill="#1f2a31"/>',
              f'<circle cx="{rx + 20:.0f}" cy="{ry + 110:.0f}" r="18" fill="#1f2a31"/>']
        # 船内放送の機器（右）：箱・スイッチの列・電源の灯（灯は点いている＝非常電源が来ていた＝海審 p1060 注30）
        px, py = CONS_PA
        lx, ly = CONS_LAMP
        g.append(_rect(px - 230, py - 100, 460, 200, "#3f4a52", C["ol"], 4, rx=10))
        for j in range(6):
            g.append(_rect(px - 196 + 62 * j, py - 6, 36, 60, "#1f2a31", "#0c1418", 2, rx=5))
        g += [f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="21" fill="#1a2328"/>',
              f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="15" fill="{C["lamp_on"]}"/>',
              f'<circle cx="{lx - 5:.0f}" cy="{ly - 5:.0f}" r="5" fill="#f4fff0" opacity="0.9"/>']
        # 放送のマイク（首の長いもの）
        g += [f'<ellipse cx="{px + 330:.0f}" cy="{CONS["top"] + 8:.0f}" rx="46" ry="12" fill="{C["mic"]}"/>',
              f'<path d="M {px + 330:.0f} {CONS["top"] + 4:.0f} Q {px + 330:.0f} {py - 90:.0f} {px + 280:.0f} {py - 140:.0f}" '
              f'stroke="{C["mic"]}" stroke-width="9" fill="none" stroke-linecap="round"/>',
              f'<rect x="{px + 252:.0f}" y="{py - 170:.0f}" width="46" height="34" rx="12" fill="{C["mic"]}" '
              f'transform="rotate(-35 {px + 275:.0f} {py - 153:.0f})"/>']
    elif view == "room":
        # 3階の案内デスクと話す無線機（判決 p14「조타실에 있는 무전기」）＝机の上の手に持つ形（形は抽象）
        wx, wy = ROOM_WALKIE
        g += [_rect(wx - 16, wy - 30, 32, 62, "#2c353b", C["ol"], 3, rx=6),
              _rect(wx + 4, wy - 64, 6, 36, "#2c353b"),
              _rect(wx - 9, wy - 20, 18, 14, "#3d5563")]
    return "".join(g)


def _rot_at(inner, deg, cen):
    return f'<g transform="rotate({deg:.2f} {cen[0]:.0f} {cen[1]:.0f})">{inner}</g>' if deg else inner


# ══════════════════════════════════════════════════════════
#  E　管制センター（チンド）の中 ── 14本目 ⑤b-3
# ══════════════════════════════════════════════════════════
# 記録：管制センター＝**レーダーと交信の装備で、行き交う船の動きを見守り、情報を知らせる所**（特調委 p3096）／
#   管制の画面（特調委小 p4180「관제화면」）・진도VTS のレーダーの航跡（海審 p1010）／9時6分に VHF 67番でセウォル号を呼んだ
#   （海審 p1059）・9時6分〜9時36分の交信（特調委小 p4180）。🔴 人は描かない（管制官の人数が記録に無い）・椅子も置かない
#   （空の椅子＝人がいなかったように見える）。画面には**セウォル号の点だけ**（ほかの船の数と位置は記録に無い＝点を足さない）
ESCR = (170.0, 110.0, 1350.0, 700.0)
ERAD = (760.0, 405.0)                  # 画面の同心円の中心
EDOT = (905.0, 350.0)                  # セウォル号の点
EMIC = (1330.0, 640.0)                 # 交信のマイクの頭
EDIR = math.degrees(math.atan2(EDOT[1] - EMIC[1], EDOT[0] - EMIC[0]))


def e_room_svg():
    x0, y0, x1, y1 = ESCR
    cx, cy = ERAD
    g = ['<defs><linearGradient id="ewall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d3942"/>'
         '<stop offset="1" stop-color="#1e262d"/></linearGradient>'
         f'<clipPath id="escr"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath></defs>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#ewall)"/>',
         _rect(x0 - 22, y0 - 22, x1 - x0 + 44, y1 - y0 + 44, "#0b1014", "#3b4852", 3, rx=10),
         _rect(x0, y0, x1 - x0, y1 - y0, "#0e2433"),
         '<g clip-path="url(#escr)">']
    x = x0
    while x < x1:
        g.append(f'<path d="M {x:.0f} {y0:.0f} V {y1:.0f}" stroke="#173a4c" stroke-width="1.5"/>')
        x += 90
    y = y0
    while y < y1:
        g.append(f'<path d="M {x0:.0f} {y:.0f} H {x1:.0f}" stroke="#173a4c" stroke-width="1.5"/>')
        y += 90
    for r in (95, 190, 285, 380, 475):
        g.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="none" stroke="#1f5066" stroke-width="2.5"/>')
    g.append(f'<path d="M {cx:.0f} {cy:.0f} L {cx + 460 * math.cos(math.radians(-38)):.0f} '
             f'{cy + 460 * math.sin(math.radians(-38)):.0f}" stroke="#2b6f86" stroke-width="3"/></g>')
    # 机と交信の装備（形は抽象）
    g += [_rect(0, 760, W, 34, "#3a4650"), _rect(0, 794, W, H - 794, "#252e35"),
          _rect(1470, 590, 340, 172, "#303b44", "#141b20", 3, rx=8),
          _rect(1500, 622, 150, 56, "#10202a", "#0b1014", 2, rx=4),
          f'<path d="M 1512 650 H 1636" stroke="#6fa38a" stroke-width="4" opacity="0.8"/>']
    for j in range(6):
        g.append(f'<path d="M 1672 {620 + 20 * j} H 1790" stroke="#1a2328" stroke-width="8"/>')
    mx, my = EMIC
    g += [f'<ellipse cx="{mx + 90:.0f}" cy="768" rx="50" ry="12" fill="{C["mic"]}"/>',
          f'<path d="M {mx + 90:.0f} 764 Q {mx + 96:.0f} {my + 40:.0f} {mx + 18:.0f} {my + 8:.0f}" stroke="{C["mic"]}" '
          f'stroke-width="9" fill="none" stroke-linecap="round"/>',
          f'<rect x="{mx - 24:.0f}" y="{my - 16:.0f}" width="48" height="32" rx="12" fill="{C["mic"]}" '
          f'transform="rotate(30 {mx:.0f} {my:.0f})"/>']
    return "".join(g)


def e_dot_svg():
    x, y = EDOT
    return (f'<circle cx="{x}" cy="{y}" r="17" fill="{C["mark"]}" opacity="0.25"/>'
            f'<circle cx="{x}" cy="{y}" r="10" fill="{C["mark"]}" stroke="#0b1014" stroke-width="2"/>')


def e_sel_svg():
    x, y = EDOT
    return (f'<circle cx="{x}" cy="{y}" r="36" fill="none" stroke="{C["mark"]}" stroke-width="4"/>'
            f'<path d="M {x - 52} {y} H {x - 40} M {x + 40} {y} H {x + 52} M {x} {y - 52} V {y - 40} M {x} {y + 40} V {y + 52}" '
            f'stroke="{C["mark"]}" stroke-width="4"/>')


# ══════════════════════════════════════════════════════════
#  D の見え方（⑤b-3）：sea（海を進む123艇）・far（123艇から見た遠くの船・双眼鏡）・heli（ヘリ）・rail（3階の左舷とゴムボート）
# ══════════════════════════════════════════════════════════
SEA = dict(x0=540.0, water=700.0, s=26.0)          # 海を進む123艇：艇首の x の既定・水面・1メートルの画素
FAR = dict(piv=(1210.0, 612.0), s=0.42)            # 123艇から見た遠くのセウォル号（水面の中心・縮尺）
FAR_SEA = dict(piv=(330.0, 609.0), s=0.30)         # sea の奥の遠くのセウォル号（c919）
NEAR = (960.0, 640.0)                              # 双眼鏡の中の船（水面の中心・20画素＝1メートル）
BINOC = ((745.0, 470.0), (1175.0, 470.0), 330.0)   # 双眼鏡の2つの丸（中心・半径）
HELI = (850.0, 168.0)                              # ヘリの胴の真ん中（形は記録に無い＝影の形）。下見：上端に寄りすぎた＝下げた
HELI_LINE = (835.0, 202.0, 318.0)                  # 吊り下げの線（x・上・下）＝傾いた船の上の側（右舷）の近くまで
RAIL = dict(water=730.0, k=60.0)                   # 3階の左舷（横から）。1メートル＝60画素（背 1.7メートル＝102画素）
RAIL_TOP = RAIL["water"] - 2.1 * RAIL["k"]         # 手すりの上＝ボートで立った人の頭（ボートの床 0.4＋背 1.7 メートル）
RAIL_EDGE = RAIL_TOP + 1.0 * RAIL["k"]             # 甲板のふち（手すりの下）
RAIL_FLOOR = RAIL["water"] - 0.4 * RAIL["k"]       # ゴムボートの床
# 下見：出入り口がボートから遠いと、乗り移る影が手すりの高さを横切って「手すりの上を歩く」絵になった
#   ＝出入り口をボートの右端の上へ・立った乗組員はボートの左端へ（位置は記録に無い＝仮）
RAIL_CG = (525.0, RAIL_FLOOR)                      # 立った乗組員の足もと
RAIL_DOOR = (1010.0, 470.0)                        # 3階の通路につながる左舷の出入り口の下（判決 p17）
RAIL_SPOTS = tuple((600.0 + 58.0 * j, RAIL_FLOOR) for j in range(7))


def marks_far_svg(piv, sw):
    g = []
    for row in win_rects():
        x0, y0 = row[0][0] - 0.25, row[0][1] - 0.25
        x1, y1 = row[-1][0] + row[-1][2] + 0.25, row[0][1] + row[0][3] + 0.25
        g.append(_mrect(x0, y0, x1, y1, piv, "none", C["mark"], sw, rx=4))
    return "".join(g)


def far_ship_svg(piv, deg, s, marks=False):
    """遠くの船（傾き deg を焼き込む・縮尺 s・水面から下は切る）。marks＝客室の窓の列の印だけ。"""
    px, py = piv
    inner = marks_far_svg(piv, 3.5 / s) if marks else ship_svg(piv)
    return (f'<defs><clipPath id="farc"><rect x="-10" y="-10" width="{W + 20}" height="{py + 10:.1f}"/></clipPath></defs>'
            f'<g clip-path="url(#farc)"><g transform="rotate({deg:.2f} {px:.1f} {py:.1f})">'
            f'<g transform="translate({px:.1f} {py:.1f}) scale({s:.3f}) translate({-px:.1f} {-py:.1f})">{inner}</g></g></g>')


def far_center(piv, deg, s):
    """遠くの船の真ん中あたり（札とカメラの指し先）。"""
    p = ship_pt(0.0, A_DECK, deg, piv)
    return (piv[0] + (p[0] - piv[0]) * s, piv[1] + (p[1] - piv[1]) * s)


def wake123_svg(x0, water, s):
    """進む123艇の艇首の波と艇尾の白い筋（run の間だけ）。"""
    sx = x0 + BOAT_L * s
    g = [f'<path d="M {x0 - 34:.0f} {water + 2:.0f} Q {x0 + 40:.0f} {water - 12:.0f} {x0 + 150:.0f} {water + 4:.0f} '
         f'Q {x0 + 40:.0f} {water + 16:.0f} {x0 - 34:.0f} {water + 2:.0f} Z" fill="{C["foam"]}" opacity="0.9"/>',
         f'<path d="M {sx - 20:.0f} {water + 4:.0f} H {sx + 460:.0f}" stroke="{C["foam"]}" stroke-width="12" opacity="0.45" '
         f'stroke-linecap="round"/>']
    for k in range(5):
        xa = sx + 30 + 92 * k
        g.append(f'<path d="M {xa:.0f} {water + 8 + 6 * k:.0f} q 60 -4 124 3" stroke="{C["foam"]}" stroke-width="4" '
                 f'fill="none" opacity="{0.8 - 0.14 * k:.2f}"/>')
    return "".join(g)


def binoc_svg():
    """双眼鏡の丸い視野（2つの丸の外を暗く）。"""
    (c1, c2, r) = BINOC
    return (f'<defs><mask id="bm"><rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>'
            f'<circle cx="{c1[0]:.0f}" cy="{c1[1]:.0f}" r="{r:.0f}" fill="#000"/>'
            f'<circle cx="{c2[0]:.0f}" cy="{c2[1]:.0f}" r="{r:.0f}" fill="#000"/></mask></defs>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#06090b" mask="url(#bm)"/>')


def near_ship_svg(deg, base=(0.0, 0.0)):
    """双眼鏡の中の船（傾きを焼き込む）と、その奥の空と海・手前の海。base＝先に置く位置（ずらしの真ん中）。"""
    return (f'<g transform="translate({base[0]:.1f} {base[1]:.1f})">'
            + seascape_svg(HORIZON, -2600.0, 4500.0)
            + f'<g transform="rotate({deg:.2f} {NEAR[0]:.0f} {NEAR[1]:.0f})">{ship_svg(NEAR)}</g>'
            + front_sea_svg(WATER, -2600.0, 4500.0) + "</g>")


def heli_svg():
    """海洋警察のヘリ1機（影の形・形と色は記録に無い）と吊り下げの線（人は描かない＝救助された人を描かない）。"""
    x, y = HELI
    lx, ly0, ly1 = HELI_LINE
    return (f'<path d="M {lx:.0f} {ly0:.0f} V {ly1:.0f}" stroke="{C["ol"]}" stroke-width="5"/>'
            f'<path d="M {lx:.0f} {ly0:.0f} V {ly1:.0f}" stroke="#e3eaee" stroke-width="2"/>'
            f'<path d="M {x + 40:.0f} {y + 2:.0f} L {x + 170:.0f} {y - 8:.0f} L {x + 172:.0f} {y + 6:.0f} L {x + 40:.0f} {y + 22:.0f} Z" '
            f'fill="#e3e8eb" stroke="{C["ol"]}" stroke-width="3"/>'
            f'<path d="M {x + 158:.0f} {y - 8:.0f} L {x + 176:.0f} {y - 40:.0f} L {x + 186:.0f} {y - 38:.0f} L {x + 180:.0f} {y + 4:.0f} Z" '
            f'fill="#e3e8eb" stroke="{C["ol"]}" stroke-width="3"/>'
            f'<path d="M {x - 78:.0f} {y + 6:.0f} Q {x - 80:.0f} {y - 30:.0f} {x - 30:.0f} {y - 34:.0f} L {x + 44:.0f} {y - 30:.0f} '
            f'Q {x + 64:.0f} {y - 10:.0f} {x + 56:.0f} {y + 24:.0f} Q {x - 10:.0f} {y + 40:.0f} {x - 60:.0f} {y + 30:.0f} Z" '
            f'fill="#eef1f3" stroke="{C["ol"]}" stroke-width="3"/>'
            f'<path d="M {x - 70:.0f} {y + 8:.0f} Q {x - 66:.0f} {y - 22:.0f} {x - 34:.0f} {y - 24:.0f} L {x - 30:.0f} {y + 6:.0f} Z" '
            f'fill="{C["win"]}"/>'
            f'<path d="M {x - 66:.0f} {y + 16:.0f} H {x + 54:.0f}" stroke="{C["boat_navy"]}" stroke-width="6"/>'
            f'<path d="M {x - 44:.0f} {y + 40:.0f} V {y + 52:.0f} M {x + 30:.0f} {y + 38:.0f} V {y + 52:.0f} '
            f'M {x - 66:.0f} {y + 52:.0f} H {x + 50:.0f}" stroke="{C["ol"]}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M {x - 6:.0f} {y - 34:.0f} V {y - 46:.0f}" stroke="{C["ol"]}" stroke-width="6"/>'
            f'<path d="M {x - 150:.0f} {y - 48:.0f} H {x + 140:.0f}" stroke="{C["ol"]}" stroke-width="6" stroke-linecap="round"/>')


def rail_ship_svg():
    """3階の左舷を横から（海の上のゴムボートの高さから）。客室の壁・窓（中は描かない）・左舷の出入り口・甲板・手すり・海。
    傾きの角度は描かない（9時38分の角度は記録に無い＝海審 p1057 は 9時34分 52.2度・9時46分 61.2度）"""
    wy = RAIL["water"]
    top, edge = RAIL_TOP, RAIL_EDGE
    dx, dy = RAIL_DOOR
    g = ['<defs><linearGradient id="rsky" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{C["sky0"]}"/><stop offset="1" stop-color="{C["sky1"]}"/></linearGradient>'
         '<linearGradient id="rsea" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{C["sea0"]}"/><stop offset="1" stop-color="{C["sea1"]}"/></linearGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="180" fill="url(#rsky)"/>',
         _rect(0, 150, W, 330, C["hull"]),
         f'<path d="M 0 150 H {W}" stroke="{C["edge"]}" stroke-width="4"/>']
    for x in range(40, W, 150):
        if not (dx - 150 < x < dx + 80):
            g.append(_rect(x, 250, 88, 80, C["win"], rx=4))
    g += [_rect(dx - 66, dy - 180, 132, 180, C["edge"], rx=4), _rect(dx - 56, dy - 170, 112, 170, "#2f3a42"),
          _rect(0, 470, W, edge - 470, C["deck"]),
          f'<path d="M 0 470 H {W}" stroke="{C["edge"]}" stroke-width="3"/>',
          _rect(0, edge, W, wy - edge + 40, "#dfe5e9"),
          _rect(0, wy - 18, W, 12, C["navy"])]
    for x in range(0, W + 70, 70):
        g.append(_rect(x, top, 7, edge - top, "#8d9aa3"))
    g += [_rect(0, top - 5, W, 10, "#8d9aa3", C["ol"], 1.5),
          _rect(0, top + 0.5 * RAIL["k"] - 3, W, 6, "#8d9aa3"),
          f'<rect x="0" y="{wy:.0f}" width="{W}" height="{H - wy:.0f}" fill="url(#rsea)"/>',
          f'<path d="M 0 {wy + 1:.0f} H {W}" stroke="#dbe7ee" stroke-opacity="0.4" stroke-width="2"/>']
    return "".join(g)


def rboat_svg(part):
    """123艇のゴムボート（1隻だけ＝特調委小 p4194）。形・色・大きさは記録に無い＝仮。back＝奥の浮き・床／front＝手前の浮き。"""
    fy = RAIL_FLOOR
    if part == "back":
        return (_rect(470, fy - 20, 560, 24, "#4c575e", C["ol"], 2, rx=12) + _rect(480, fy - 2, 540, 16, "#2c3439"))
    return (f'<path d="M 440 {fy - 14:.0f} Q 440 {fy + 40:.0f} 500 {fy + 42:.0f} H 1010 Q 1052 {fy + 40:.0f} 1052 {fy + 14:.0f} '
            f'Q 1052 {fy - 14:.0f} 1010 {fy - 16:.0f} H 500 Q 450 {fy - 18:.0f} 440 {fy - 14:.0f} Z" fill="#5f6b73" '
            f'stroke="{C["ol"]}" stroke-width="3"/>'
            f'<path d="M 470 {fy + 12:.0f} H 1030" stroke="#76838b" stroke-width="5" opacity="0.8"/>')


def rail_guide_svg():
    """頭の高さ＝手すりの上（艇長の判決 p5002）を見せる点線。"""
    x0, x1 = RAIL_CG[0] - 34, RAIL_CG[0] + 340
    return (f'<path d="M {x0:.0f} {RAIL_TOP:.0f} H {x1:.0f}" stroke="{C["ol"]}" stroke-width="7" stroke-dasharray="16 10"/>'
            f'<path d="M {x0:.0f} {RAIL_TOP:.0f} H {x1:.0f}" stroke="{C["mark"]}" stroke-width="3.5" stroke-dasharray="16 10"/>')


def rail_board_path(j):
    """j 人目の道：3階の通路の出入り口 → すぐ下の手すりを越える → ゴムボート（判決 p17）。"""
    return [RAIL_DOOR, (RAIL_DOOR[0] - 25.0, RAIL_TOP + 2.0), RAIL_SPOTS[j]]


# ══════════════════════════════════════════════════════════
#  15本目（リノ・エアレース2011）── ⑤b-2（2026-09-30）：RA・RB・RD
# ══════════════════════════════════════════════════════════
# 置き場：RA＝上から見たステッド空港（北が上）／RB＝空の中の事故機（横から side・後ろから rear）／
#         RD＝ピットの事故機（⑤b-2 は c109 の小さな絵の「尾翼の寄り」tail だけ＝本格は ⑤b-3）
# 🔴 鍵 A〜E は14本目（セウォル号）の置き場＝触らない（14本目の selftest の見本 fixture_ep14 が使う）。15本目は頭に R。
# 🔴 守りの線（Vault 映像方針 15本目 §1・§10）：パイロットは人の形で描かない（操縦席の覆いは光る面＝中を描かない）／
#    落ちたことは RA の×と札だけ（機体の印は0秒で消し、そこから先は点線＝模式）／形のもとは PD の図だけ
#    （AAB 図1 p11・図2 p14・図3 p20・#33 図7 p2009・#14 図12 p3014）＝写真（BY-SA・CC BY・courtesy）はなぞらない／
#    RA の縮尺は1画素あたり1.5メートル以上（人を描けない縮尺＝門番 ⑧）／横転のきっかけは場面にしない（渦も板も描かない）／
#    時刻・秒の札は AAB p28 の経過の表の値だけ（`cuts.ss.ILLU_SEC_OK`＝門番 ⑤）／数（機体1・燃料車1・スタンド3・パイロン12）
#    は部品の obj で名乗る（`cuts.ss.ILLU_COUNTS`＝門番 ③）
# 位置（メートル・東 E・北 N・原点＝本部のパイロン）＝`ref/ep15/measure_reno.py` が図の画素から機械で測った（目で読んでいない。
#   結果の正本＝`ref/ep15/illu_reno.json`）：
#   ・図1（AAB p11・北が上）：パイロン12本（青・黄・赤の三角の色の塊）・ショーライン（緑の画素を直線で当てた）・事故地点（赤い点）。
#     縮尺＝コースの長さ 8.4333マイル（#33 p2009）÷ パイロンを回る順の折れ線＝1画素 8.644メートル。
#     確かめ＝事故地点はショーラインの南 約280メートル（記録：ボックス席の端は 874フィート＝266メートル＝AAB p19 の内側）
#   ・#14 図12（p3014・1周目 黄・2周目 橙・3周目 赤）：パイロン12本で図1 へ相似に当てた（残差 平均28メートル）。
#     航跡＝色ごとの画素を角度で並べた点（4つおき）。3周目の終わり＝最後の GPS（16:24:29＝#14 p3008）の近く
#   ・滑走路：14/32＝9,000フィート・8/26＝7,608フィート（AAB p16）。8/26 の南の縁＝ショーライン（p17）。14/32 の向きは図12 の
#     暗い帯・南の端は 8/26 の中心線と交わる所。
#   ⚠️ 8/26 の東西の端・駐機場・ピット・ボックス席・スタンドの東西の広がりは図3（p20・斜めの空撮）から読んだ概略（記録の数は
#      ショーラインから 266・228メートルと「燃料車はピットの近く」だけ）＝左下の出典に「配置は概略」。幅（滑走路 46メートル・
#      ボックス席 24メートル・スタンド 30メートル）も記録に無い＝抽象
R_PYL = dict(hm=(0.0, 0.0), p1=(468.0, 163.0), p2=(1251.0, 717.0), p3=(1470.0, 1755.0), sg=(1054.0, 3276.0),
             p4=(660.0, 4426.0), p5=(-709.0, 4889.0), p6=(-1899.0, 4085.0), gw=(-1902.0, 3107.0),
             p7=(-1962.0, 1093.0), p8=(-1511.0, 430.0), p9=(-924.0, 147.0))
R_ORDER = ("hm", "p1", "p2", "p3", "sg", "p4", "p5", "p6", "gw", "p7", "p8", "p9")    # 回る順（左回り＝図1 の向きの矢印）
R_SHOW_DEG = -6.13                 # ショーラインの向き（東から・北が＋）
R_S0 = (0.0, -320.2)               # ショーラインの上で本部のパイロンの真南の点
R_ACC = (-46.0, -598.0)            # 事故地点（図1 の赤い点）
R_LAPS = dict(
    lap1=((1658, 1084), (1683, 1446), (1691, 1764), (1692, 2049), (1694, 2313), (1691, 2567), (1676, 2819), (1657, 3075),
          (1631, 3345), (1588, 3633), (1530, 3950), (1423, 4280), (1259, 4613), (1039, 4946), (746, 5241), (377, 5403),
          (-21, 5551), (-435, 5506), (-831, 5393), (-1216, 5261), (-1527, 4987), (-1766, 4659), (-1972, 4221),
          (-2062, 3864), (-2109, 3524), (-2130, 3207), (-2136, 2910), (-2133, 2624), (-2124, 2342), (-2112, 2055),
          (-2097, 1751), (-2054, 1431), (-1942, 1122), (-1810, 793), (-1594, 508), (-1320, 273), (-999, 103),
          (-652, -16), (-290, -83), (-12, -102)),
    lap2=((2051, 2796), (1944, 3082), (1827, 3353), (1705, 3620), (1489, 3822), (1267, 4002), (1056, 4184), (661, 4498),
          (411, 4700), (125, 4919), (-212, 5094), (-647, 5024), (-1188, 4948), (-1472, 4716), (-1714, 4454), (-1920, 4175),
          (-2053, 3858), (-2084, 3513), (-2113, 3202), (-2155, 2768), (-2148, 2482), (-2135, 2123), (-2124, 1821),
          (-2090, 1501), (-2021, 1060), (-1913, 685), (-1628, 462), (-1373, 174), (-1045, -26), (-671, -107),
          (-296, -180), (89, -209), (448, -41), (817, 29), (1160, 184), (1476, 388), (1771, 621), (1938, 969), (1978, 1051)),
    lap3=((188, -220), (572, -152), (942, -28), (1273, 177), (1531, 469), (1739, 783), (1810, 1172), (1866, 1517),
          (1914, 1830), (1911, 2137), (1859, 2429), (1777, 2699), (1698, 2952), (1580, 3252), (1464, 3479), (1346, 3709),
          (1222, 3954), (993, 4215), (790, 4431), (563, 4672), (288, 4890), (-38, 5002), (-386, 5058), (-740, 5032),
          (-1077, 4919), (-1384, 4742), (-1690, 4563), (-1991, 4124), (-2138, 3719), (-2189, 3390), (-2210, 3075),
          (-2210, 2773), (-2200, 2480), (-2185, 2188), (-2160, 1888), (-2124, 1571), (-2052, 1243), (-1912, 930),
          (-1730, 621), (-1480, 357), (-1404, 309)))
R_LAP_COL = dict(lap1="#f2d24a", lap2="#ef9b3a", lap3="#e0533c")     # 図12 と同じ 黄・橙・赤（何周目かの色）
R_GG = ((-1912.0, 930.0), (-1730.0, 621.0), (-1480.0, 357.0), (-1404.0, 309.0))   # 3周目：パイロン7のすぐ後 → 航跡の終わり
R_SEG67 = ((-1991.0, 4124.0), (-2138.0, 3719.0), (-2189.0, 3390.0), (-2210.0, 3075.0), (-2210.0, 2773.0), (-2200.0, 2480.0),
           (-2185.0, 2188.0), (-2160.0, 1888.0), (-2124.0, 1571.0), (-2052.0, 1243.0))   # 3周目のパイロン6〜7の区間（AAB p29）
# 崩れ始め（航跡の終わり）→ 事故地点＝🔴 模式（地面の上の道は記録に無い＝AAB p11「らせん状に降下」だけ）＝点線で描く
R_FALL = ((-1404.0, 309.0), (-1060.0, 205.0), (-720.0, 60.0), (-440.0, -150.0), (-220.0, -370.0), (-46.0, -598.0))
R_RW = 46.0                        # 滑走路の幅（記録に無い＝抽象）
R_RW826 = (-1390.0, 929.0)         # 8/26：ショーラインに沿った範囲（長さ 2,319メートル＝7,608フィート・東の端＝14/32 と交わる所）
R_RW1432 = dict(s_end=(926.0, -396.5), deg=116.3, len=2743.0)    # 14/32：南の端・向き（東から・北が＋）・長さ（9,000フィート）
R_RAMP = dict(s=(-760.0, 929.0), d=(0.0, 266.0))      # 駐機場（ランプ）＝ボックス席の端まで（266メートル＝AAB p19）
R_PITS = dict(s=(-730.0, -170.0), d=(228.0, 330.0))   # ピット（端はショーラインの南 228メートル＝748フィート＝AAB p19）
R_BOX = dict(s=(-150.0, 450.0), d=(266.0, 290.0))     # ボックス席
R_STANDS = ((-140.0, 60.0), (90.0, 250.0), (280.0, 440.0))   # スタンド3つ（図3 の矢印）の s の範囲
R_STAND_D = (296.0, 326.0)
R_BUILT = dict(s=(-900.0, 1000.0), d=(330.0, 560.0))  # スタンドの奥（テント・建物＝数が記録に無い＝塗りだけ）
R_FUEL = (-650.0, 185.0)           # 燃料車（ピットの近くの駐機場＝AAB p19・図3）の s, d
R_FUEL_M = (12.0, 3.0)             # 燃料車の長さと幅（記録に無い＝抽象）
R_PIECE_R = 120.0                  # 一片が見つかった所＝本部のパイロンの「近く」（AAB p18）の輪の半径（点にしない）
R_RING8 = 330.0                    # パイロン8を回る所（3周の航跡が重なる所）の輪の半径
RA_VIEW = dict(wide=dict(c=(-300.0, 2650.0), mpp=7.8, lab="上から見た図（コース全体）"),
               near=dict(c=(-800.0, 150.0), mpp=2.5, lab="上から見た図"),
               ramp=dict(c=(-150.0, -420.0), mpp=1.5, lab="上から見た図（駐機場の寄り）"))
RA_Y0 = 485.0                      # 画面の真ん中の y（左上の札の下〜左下の出典の上）
RA_T = dict(move=0.95, fade=0.22, path=0.75, x=0.3, box=0.45, trace=1.8, lap=1.9, lap_gap=0.35, glow=1.1, show=0.4)
RA_MK = (960.0, 540.0)             # 事故機の印の層の中の真ん中（mover が道の上へ動かして向きを変える）
RA_MK_K = 6.2                      # 印の1メートル＝画素（翼の幅 8.8メートル＝55画素＝実物の約15倍・出典に「機体は拡大」）


def r_sd(s, d):
    """ショーラインに沿って s メートル（東が＋）・南へ d メートルの点（E, N）。"""
    a = math.radians(R_SHOW_DEG)
    u, v = (math.cos(a), math.sin(a)), (math.sin(a), -math.cos(a))
    return (R_S0[0] + s * u[0] + d * v[0], R_S0[1] + s * u[1] + d * v[1])


def r_px(p, view):
    """世界の点（メートル）→ RA の見え方 view の画面の点。"""
    v = RA_VIEW[view]
    return (960.0 + (p[0] - v["c"][0]) / v["mpp"], RA_Y0 - (p[1] - v["c"][1]) / v["mpp"])


def _pl(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def _poly(pts, fill, stroke=None, sw=0.0, op=None):
    s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<path d="{_d(pts)}" fill="{fill}"{s}{o}/>'


def _smooth(pts, closed=False, per=8):
    """Catmull-Rom で滑らかにした点の並び。"""
    n = len(pts)
    P = (lambda i: pts[i % n]) if closed else (lambda i: pts[max(0, min(n - 1, i))])
    out = []
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = P(i - 1), P(i), P(i + 1), P(i + 2)
        for k in range(per):
            t = k / per
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(tuple(pts[0] if closed else pts[-1]))
    return out


def ra_path(view, pts, per=8, closed=False):
    """世界の点の並び（メートル）→ 画面の滑らかな点の並び（画素）。"""
    return _smooth([r_px(p, view) for p in pts], closed=closed, per=per)


def _sd_poly(s0, s1, d0, d1, view):
    return [r_px(r_sd(s, d), view) for s, d in ((s0, d0), (s1, d0), (s1, d1), (s0, d1))]


def ra_ground_svg(view):
    """地面：砂漠・スタンドの奥の塗り・駐機場・滑走路2本・ピット・ボックス席（と前の幕）・スタンド3つ・燃料車1台。
    人・テント・駐機の機体・建物の1つずつは描かない（数が記録に無い）。"""
    import random
    mpp = RA_VIEW[view]["mpp"]
    g = [f'<rect x="-10" y="-10" width="{W + 20}" height="{H + 20}" fill="#cbb792"/>']
    rnd = random.Random("reno-desert")
    for _ in range(160):                      # 地面の濃淡（世界に固定＝見え方が変わっても同じ所に同じ濃淡）
        e, n = rnd.uniform(-7000, 6500), rnd.uniform(-4000, 9000)
        rx, ry = rnd.uniform(120, 900) / mpp, rnd.uniform(80, 520) / mpp
        col = ("#bfa982", "#d6c7a5", "#c4ae87")[rnd.randrange(3)]
        op = rnd.uniform(0.22, 0.48)
        x, y = r_px((e, n), view)
        if -rx - 60 < x < W + rx + 60 and -ry - 60 < y < H + ry + 60:
            g.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{col}" opacity="{op:.2f}"/>')
    b, r, p, bx = R_BUILT, R_RAMP, R_PITS, R_BOX
    g.append(_poly(_sd_poly(b["s"][0], b["s"][1], b["d"][0], b["d"][1], view), "#b5b0a4"))
    g.append(_poly(_sd_poly(r["s"][0], r["s"][1], r["d"][0], r["d"][1], view), "#aeb2b4"))
    g.append(_poly(_sd_poly(R_RW826[0], R_RW826[1], -R_RW, 0.0, view), "#5d6266"))
    a = math.radians(R_RW1432["deg"])
    u, nrm = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    s_ = R_RW1432["s_end"]
    n_ = (s_[0] + u[0] * R_RW1432["len"], s_[1] + u[1] * R_RW1432["len"])
    hw = R_RW / 2
    g.append(_poly([r_px(q, view) for q in ((s_[0] + nrm[0] * hw, s_[1] + nrm[1] * hw), (n_[0] + nrm[0] * hw, n_[1] + nrm[1] * hw),
                                            (n_[0] - nrm[0] * hw, n_[1] - nrm[1] * hw), (s_[0] - nrm[0] * hw, s_[1] - nrm[1] * hw))],
                   "#5d6266"))
    g.append(_poly(_sd_poly(p["s"][0], p["s"][1], p["d"][0], p["d"][1], view), "#9a9ea2"))
    g.append(_poly(_sd_poly(bx["s"][0], bx["s"][1], bx["d"][0], bx["d"][1], view), "#dcd3bb"))
    for s0, s1 in R_STANDS:
        g.append(_poly(_sd_poly(s0, s1, R_STAND_D[0], R_STAND_D[1], view), "#e8eaec", "#8f989e", 1.2))
    if mpp <= 3.0:     # 寄りの絵だけ：柵と幕（全体の絵では 1画素に満たない）
        (x0, y0), (x1, y1) = r_px(r_sd(p["s"][0], p["d"][0]), view), r_px(r_sd(p["s"][1], p["d"][0]), view)
        g.append(f'<path d="M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}" stroke="#6d7378" stroke-width="1.6"/>')   # ピットの端の低い柵（p20）
        (x0, y0), (x1, y1) = r_px(r_sd(bx["s"][0], bx["d"][0]), view), r_px(r_sd(bx["s"][1], bx["d"][0]), view)
        for col, off in (("#3d6ea6", 0), ("#b0443a", 7)):     # ボックス席の前の幕を付けたパイプ（p20・幕は青と赤＝p21 注26）
            g.append(f'<path d="M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}" stroke="{col}" stroke-width="3" '
                     f'stroke-dasharray="7 7" stroke-dashoffset="{off}"/>')
    fl, fw = R_FUEL_M
    fs, fd = R_FUEL
    g.append(_poly(_sd_poly(fs - fl / 2, fs + fl / 2, fd - fw / 2, fd + fw / 2, view), "#f4f5f6", "#3f464c", 1.2))
    return "".join(g)


def ra_course_pts():
    """コース（パイロンの外側を回る線）＝パイロンを真ん中から 90メートル外へ押した点。道の細部は記録に無い＝模式の破線。"""
    c = (sum(p[0] for p in R_PYL.values()) / len(R_PYL), sum(p[1] for p in R_PYL.values()) / len(R_PYL))
    out = []
    for k in R_ORDER:
        x, y = R_PYL[k]
        L = math.hypot(x - c[0], y - c[1]) or 1.0
        out.append((x + (x - c[0]) / L * 90.0, y + (y - c[1]) / L * 90.0))
    return out


def ra_course_svg(view):
    return (f'<path d="{_pl(ra_path(view, ra_course_pts(), per=10, closed=True))} Z" fill="none" stroke="#f4f1ea" '
            f'stroke-width="2.6" stroke-dasharray="9 10" opacity="0.55"/>')


def ra_pylons_svg(view):
    """パイロン10本＋案内2本（AAB p17）。どれも同じ印（記号の大きさは見え方で変えない）。"""
    g = []
    for k in R_ORDER:
        x, y = r_px(R_PYL[k], view)
        g.append(f'<circle cx="{x + 1.5:.1f}" cy="{y + 1.5:.1f}" r="7" fill="#1a2530" opacity="0.35"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#f4f1ea" stroke="#2b2f33" stroke-width="1.8"/>')
    return "".join(g)


def ra_marker_svg():
    """上から見た事故機の印（機首が +x）。形は AAB 図2（p14）の上から見た図の概形（翼を短くした形・翼端の板）。
    操縦席の覆いは光る面（中を描かない）。大きさは拡大（RA_MK_K）"""
    cx, cy = RA_MK
    k = RA_MK_K

    def P(x, y):
        return (cx + x * k, cy - y * k)
    hw = 4.395
    body = [(4.8, 0.0), (4.3, 0.42), (2.0, 0.55), (-3.9, 0.30), (-5.0, 0.18), (-5.0, -0.18), (-3.9, -0.30), (2.0, -0.55),
            (4.3, -0.42)]
    wing = [(1.6, 0.5), (0.7, hw), (-0.5, hw), (-1.2, 0.5), (-1.2, -0.5), (-0.5, -hw), (0.7, -hw), (1.6, -0.5)]
    stab = [(-4.0, 0.25), (-4.5, 1.84), (-5.0, 1.84), (-5.0, -1.84), (-4.5, -1.84), (-4.0, -0.25)]
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{5.6 * k:.1f}" fill="#f7f4ee" opacity="0.30"/>'
            + _poly([P(*q) for q in wing], "#cfd6db", "#3a454e", 1.6) + _poly([P(*q) for q in stab], "#cfd6db", "#3a454e", 1.4)
            + _poly([P(*q) for q in body], "#dde3e7", "#3a454e", 1.6)
            + f'<ellipse cx="{cx + 0.5 * k:.1f}" cy="{cy:.1f}" rx="{0.8 * k:.1f}" ry="{0.3 * k:.1f}" fill="#9cc0d6" '
            f'stroke="#3a454e" stroke-width="1"/>')


def ra_line_svg(pts, col, w, dash=None, op=1.0, glow=False):
    """道の線（draw の部品＝build_jiko が頭から順に見せる）。"""
    d = _pl(pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    g = ""
    if glow:
        g += (f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="0.35" stroke-width="{w * 3.2:.1f}" '
              f'stroke-linecap="round" stroke-linejoin="round"/>')
    return g + (f'<path d="{d}" fill="none" stroke="#1a2530" stroke-opacity="{0.5 * op:.2f}" stroke-width="{w + 3:.1f}" '
                f'stroke-linecap="round" stroke-linejoin="round"{da}/>'
                f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round" '
                f'stroke-linejoin="round"{da}/>')


def ra_x_svg(view):
    x, y = r_px(R_ACC, view)
    d = f"M {x - 13:.1f} {y - 13:.1f} L {x + 13:.1f} {y + 13:.1f} M {x + 13:.1f} {y - 13:.1f} L {x - 13:.1f} {y + 13:.1f}"
    return (f'<path d="{d}" stroke="#1a2530" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{C["mark"]}" stroke-width="5" stroke-linecap="round"/>')


def ra_box_svg(view):
    bx = R_BOX
    return _poly(_sd_poly(bx["s"][0], bx["s"][1], bx["d"][0] - 3, bx["d"][1] + 3, view), "none", C["mark"], 3.0)


def ra_ring_svg(center, rad_m, view, dash=None):
    x, y = r_px(center, view)
    r = max(16.0, rad_m / RA_VIEW[view]["mpp"])
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="#1a2530" stroke-opacity="0.5" stroke-width="7"{da}/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{C["mark"]}" stroke-width="3.5"{da}/>')


def _ra_timeline(start, states, steps):
    """RA の鍵（段の中の順番つき）＝事故機の印が進む → 消える（0秒）→ 点線が伸びる → ×・ボックス席 の順（見本 §8）。"""
    T = RA_T
    on = (lambda st, f: st[f] == "on")
    gg0 = start["gg"]
    K = dict(gg_u=[dict(stage=0, delay=0.0, u=1.0 if gg0 in ("p8", "gone") else 0.0)],
             gg_a=[dict(stage=0, delay=0.0, a=1.0 if gg0 in ("p7", "p8") else 0.0)])
    for f in ("path", "trace", "laps", "seg67"):
        K[f] = [dict(stage=0, delay=0.0, u=1.0 if on(start, f) else 0.0)]
    for f in ("x", "box", "ring8", "piece", "fuel", "course"):
        K[f] = [dict(stage=0, delay=0.0, a=1.0 if on(start, f) else 0.0)]
    K["lap"] = {n: [dict(stage=0, delay=0.0, u=1.0 if on(start, "laps") else 0.0)] for n in R_LAPS}
    prev = start
    for i, (st, sp) in enumerate(zip(states, steps)):
        dl = float(sp.get("delay", KEY_DELAY))
        t = dl
        g0, g1 = prev["gg"], st["gg"]
        if g0 != g1:
            if g1 == "off":
                K["gg_a"].append(dict(stage=i, delay=t, dur=T["fade"], a=0.0))
            elif g1 == "p7":
                K["gg_u"].append(dict(stage=i, delay=t, dur=0.02, u=0.0))
                K["gg_a"].append(dict(stage=i, delay=t, dur=0.3, a=1.0))
            else:                                   # p8／gone：まだ動いていなければ動いてから
                if g0 in ("off", "p7"):
                    if g0 == "off":
                        K["gg_a"].append(dict(stage=i, delay=t, dur=0.25, a=1.0))
                    K["gg_u"].append(dict(stage=i, delay=t, dur=T["move"], u=1.0))
                    t += T["move"]
                if g1 == "gone":
                    K["gg_a"].append(dict(stage=i, delay=t, dur=T["fade"], a=0.0))
                    t += T["fade"]
        if prev["path"] != st["path"]:
            K["path"].append(dict(stage=i, delay=t, dur=T["path"], u=1.0 if on(st, "path") else 0.0))
            t += T["path"] if on(st, "path") else 0.0
        if prev["x"] != st["x"]:
            K["x"].append(dict(stage=i, delay=t, dur=T["x"], a=1.0 if on(st, "x") else 0.0))
        if prev["box"] != st["box"]:
            K["box"].append(dict(stage=i, delay=t + 0.1, dur=T["box"], a=1.0 if on(st, "box") else 0.0))
        if prev["trace"] != st["trace"]:
            K["trace"].append(dict(stage=i, delay=dl, dur=float(sp.get("dur", T["trace"])), u=1.0 if on(st, "trace") else 0.0))
        if prev["laps"] != st["laps"]:
            for j, n in enumerate(R_LAPS):
                K["lap"][n].append(dict(stage=i, delay=dl + j * T["lap_gap"], dur=T["lap"], u=1.0 if on(st, "laps") else 0.0))
        if prev["seg67"] != st["seg67"]:
            K["seg67"].append(dict(stage=i, delay=dl, dur=T["glow"], u=1.0 if on(st, "seg67") else 0.0))
        for f in ("ring8", "piece", "fuel", "course"):
            if prev[f] != st[f]:
                late = T["lap"] + 2 * T["lap_gap"] if (f == "ring8" and prev["laps"] != st["laps"]) else 0.0
                K[f].append(dict(stage=i, delay=dl + late, dur=T["show"], a=1.0 if on(st, f) else 0.0))
        prev = st
    return K


def _scene_RA(start, states, steps):
    """RA＝上から見たステッド空港（北が上）。見え方 view＝wide（コース全体）／near（パイロン7・8と駐機場）／ramp（駐機場の寄り）。"""
    view = start["view"]
    if any(st["view"] != view for st in states):
        raise ValueError("illu RA：見え方 view は場面の頭（start）で1つだけ（地面の縮尺を焼き込む）")
    allst = [start] + states

    def used(f):
        return any(st[f] != "off" for st in allst)
    K = _ra_timeline(start, states, steps)
    A1 = [dict(stage=0, delay=0.0, a=1.0)]
    parts = [dict(_part("ground", ra_ground_svg(view),
                        "AAB p11（図1）・p16（滑走路2本の長さ）・p17（ショーライン）・p19（ボックス席・ピット・燃料車）・p20（図3・柵と幕）・p21（幕は青と赤）"),
                  obj=dict(fuel_truck=1, stands=3)),
             _part("course", ra_course_svg(view), "#33 p2009（コース＝パイロン10本と案内2本）", keys=K["course"])]
    if used("laps"):
        for n in R_LAPS:
            pts = ra_path(view, R_LAPS[n], per=4)
            parts.append(dict(_part(n, ra_line_svg(pts, R_LAP_COL[n], 3.5, op=0.95), "#14 p3014（図12＝1〜3周目の航跡）・p3008"),
                              kind="draw", path=[list(q) for q in pts], go=K["lap"][n], keys=A1, reveal=18))
    if used("seg67"):
        pts = ra_path(view, R_SEG67, per=6)
        parts.append(dict(_part("seg67", ra_line_svg(pts, C["mark"], 5.0, glow=True),
                                "AAB p29（パイロン6と7のあいだで一番速かった）・#14 p3014（図12＝3周目の航跡）"),
                          kind="draw", path=[list(q) for q in pts], go=K["seg67"], keys=A1, reveal=40))
    if used("ring8"):
        parts.append(_part("ring8", ra_ring_svg(R_PYL["p8"], R_RING8, view),
                           "AAB p29（パイロン8を回る速さとGは前の2周とほぼ同じ）・#14 p3014（図12）", keys=K["ring8"]))
    parts.append(dict(_part("pylons", ra_pylons_svg(view), "AAB p17（パイロン10本と案内のパイロン2本）・p11（図1）"),
                      obj=dict(pylons=len(R_ORDER))))
    gp = ra_path(view, R_GG, per=10)
    if used("gg"):
        parts.append(dict(_part("trail", ra_line_svg(gp, "#f7f4ee", 3.0, op=0.7), "#14 p3014（図12＝3周目の航跡）・p3008"),
                          kind="draw", path=[list(q) for q in gp], go=K["gg_u"], keys=A1, reveal=14))
    fp = ra_path(view, R_FALL, per=10)
    if used("path"):
        parts.append(dict(_part("fall", ra_line_svg(fp, "#f7f4ee", 3.4, dash="3 9", op=0.95),
                                "AAB p11（右へ転がりながら上昇し、らせん状に降下して地面へ）・p19（ボックス席）"),
                          kind="draw", path=[list(q) for q in fp], go=K["path"], keys=A1, reveal=16))
    if used("trace"):
        parts.append(dict(_part("trace", ra_line_svg(fp, C["mark"], 6.0), "AAB p28（崩れ始めてから約9.1秒で地面）"),
                          kind="draw", path=[list(q) for q in fp], go=K["trace"], keys=A1, reveal=18))
    if used("piece"):
        parts.append(_part("piece", ra_ring_svg(R_PYL["hm"], R_PIECE_R, view, dash="10 7"),
                           "AAB p18（左の板の内側の一片は本部のパイロンの近くで見つかった）", keys=K["piece"]))
    if used("fuel"):
        parts.append(_part("fuel", ra_ring_svg(r_sd(*R_FUEL), 18.0, view), "AAB p19（燃料車がピットの近くの駐機場に）",
                           keys=K["fuel"]))
    if used("box"):
        parts.append(_part("box", ra_box_svg(view), "AAB p19（観客のボックス席に落ちた）", keys=K["box"]))
    if used("x"):
        parts.append(_part("x", ra_x_svg(view), "AAB p11（図1＝事故地点）・p19", keys=K["x"]))
    if used("gg"):
        parts.append(dict(_part("gg", ra_marker_svg(), "AAB p14（図2＝機体の形）・p28（パイロン8を回って崩れ始めた）"),
                          kind="mover", path=[list(q) for q in gp], go=K["gg_u"], keys=K["gg_a"], anchor=list(RA_MK),
                          obj=dict(aircraft=1)))
    return parts


def _ra_anchors(view):
    P = lambda p: r_px(p, view)  # noqa: E731
    a = {k: P(v) for k, v in R_PYL.items()}
    fp = ra_path(view, R_FALL, per=10)
    a.update(x=P(R_ACC), gg0=P(R_GG[0]), gg1=P(R_GG[-1]), fall0=fp[0], fall_mid=fp[len(fp) // 2],
             box=P(r_sd(150.0, 278.0)), ramp=P(r_sd(-330.0, 120.0)), fuel=P(r_sd(*R_FUEL)), pits=P(r_sd(-450.0, 280.0)),
             stands=P(r_sd(160.0, 311.0)), seg67=P(R_SEG67[len(R_SEG67) // 2]), center=(960.0, RA_Y0))
    return a


# ── RB：空の中の事故機（横から side・後ろから rear）。形＝AAB 図2（p14）の横から見た図と上から見た図の寸法（翼の幅 約8.8メートル・
#    水平尾翼 約3.7メートル＝p13）。色（銀）と「177」＝事故の週の写真で確かめただけ（写真はなぞらない）。胴体の下の取り入れ口は無い（p13）
RB_K = 58.0                        # 横から：1メートル＝58画素（機体の長さ 9.83メートル＝570画素）
RB_KR = 50.0                       # 後ろから：1メートル＝50画素（翼の幅 8.79メートル＝440画素）
RB_C = (960.0, 430.0)              # 機体の真ん中＝回す中心（横から）
# 後ろから：⑤b-2 の下見で、90度前後に傾いた翼の下の先が地平線より下（砂漠の上）に出て「翼が地面に触れた」ように見えた
#   ＝回す中心を上へ（翼の半分 237画素＋余白 → 下の先が地平線より上）
# 🔴 ⑤b-3（2026-09-30）：試し焼き 36657377530 の c307（93度）で、下の翼の先 y≈596 が**地平線 612 の 16画素上**＝手前の丘と
#    砂漠の境にちょうど乗り、やはり「地面に触れた」絵に見えた（門番 ⑨ の余白 8画素では通っていた）。
#    ＝中心をさらに上へ（360→330）・少し小さく（54→50）＝93度で翼の先 y≈549（地平線の63画素上＝手前の丘より上）。
#    門番 ⑨ の余白も RB_GAP（50画素）に広げた（翼の厚み約10画素を引いても40画素のすき間が見える）
RB_CR = (960.0, 330.0)
RB_HZ = 612.0                      # 地平線
RB_GAP = 50.0                      # 後ろから見た翼の下の先と地平線のすき間の下限（門番 ⑨）
RB_T = dict(view=0.35, pitch=0.55, roll=2.6, ail=0.4, pylon=2.4)
RB_VIEW = dict(side="横から見た図", rear="後ろから見た図")
# 横から見た形（メートル・x＝前・y＝上・原点＝翼の付け根のあたり）。図2 の横の図から概形を読んだ（線の数は減らした＝抽象）
RB_SIDE = dict(
    body=((4.80, -0.02), (4.45, 0.22), (4.20, 0.30), (3.30, 0.36), (1.45, 0.50), (1.05, 0.78), (0.55, 0.84), (-0.20, 0.68),
          (-1.50, 0.62), (-2.85, 0.55), (-4.35, 1.62), (-4.85, 1.66), (-5.05, 1.50), (-5.05, 0.15), (-4.75, -0.05),
          (-3.00, -0.42), (-1.00, -0.62), (0.80, -0.62), (2.60, -0.52), (3.60, -0.42), (4.45, -0.24)),
    glass=((1.45, 0.50), (1.05, 0.78), (0.55, 0.84), (-0.20, 0.68), (-0.05, 0.54)),
    wing=((2.20, -0.40), (1.20, -0.30), (-0.80, -0.34), (-1.90, -0.42), (-0.80, -0.56), (1.20, -0.58)),
    stab=((-3.55, 0.31), (-5.00, 0.37), (-5.00, 0.27), (-3.55, 0.24)),
    glare=((1.45, 0.50), (3.30, 0.36), (4.05, 0.31), (4.05, 0.25), (3.30, 0.29), (1.45, 0.43)),
    prop=(4.25, 0.0, 0.07, 1.70), num=(-1.75, -0.24, 0.62), tail=(-4.95, 0.30))
RB_SPAN = 4.395                    # 翼の半分（28フィート10インチ÷2＝AAB p13）
RB_STAB = 1.84                     # 水平尾翼の半分（12フィート1インチ÷2＝p13）
RB_AIL = (3.30, 4.20)              # 補助翼（約3フィートに短くした＝p13）の外側の範囲
RB_AIL_D = 0.14                    # 補助翼の切れの見せ方（メートル・記録の角度は無い＝向きだけ）


def rb_side_svg(c, k):
    """横から見た事故機（機首が右）。操縦席の覆いは光る面（中を描かない）。回る翼は薄い円。"""
    S = RB_SIDE

    def P(x, y):
        return (c[0] + x * k, c[1] - y * k)
    g = ['<defs><linearGradient id="rbb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef2f4"/>'
         '<stop offset="0.55" stop-color="#c3cbd1"/><stop offset="1" stop-color="#9aa5ad"/></linearGradient>'
         '<linearGradient id="rbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8f4fb"/>'
         '<stop offset="0.45" stop-color="#9dbfd4"/><stop offset="1" stop-color="#557489"/></linearGradient></defs>']
    px, py, rx, ry = S["prop"]
    cx, cy = P(px, py)
    g.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx * k:.1f}" ry="{ry * k:.1f}" fill="#d8dee2" opacity="0.35" '
             f'stroke="#8a969e" stroke-width="1.5" stroke-opacity="0.5"/>')
    g.append(_poly([P(*q) for q in S["stab"]], "#b9c2c8", "#44505a", 2))
    g.append(_poly([P(*q) for q in S["body"]], "url(#rbb)", "#44505a", 2.4))
    g.append(_poly([P(*q) for q in S["wing"]], "#aeb8bf", "#44505a", 2))
    g.append(_poly([P(*q) for q in S["glare"]], "#2b3036"))
    g.append(_poly([P(*q) for q in S["glass"]], "url(#rbg)", "#44505a", 2))
    (a1, b1), (a2, b2) = P(1.10, 0.70), P(0.30, 0.78)
    g.append(f'<path d="M {a1:.1f} {b1:.1f} Q {(a1 + a2) / 2:.1f} {min(b1, b2) - 0.08 * k:.1f} {a2:.1f} {b2:.1f}" stroke="#ffffff" '
             f'stroke-opacity="0.85" stroke-width="{0.05 * k:.1f}" fill="none" stroke-linecap="round"/>')
    nx, ny, nh = S["num"]
    tx, ty = P(nx, ny)
    g.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-family="Noto" font-size="{nh * k:.1f}" fill="#15181b" text-anchor="middle" '
             f'stroke="#f3f5f6" stroke-width="{0.035 * k:.1f}" paint-order="stroke fill">177</text>')
    return "".join(g)


def rb_rear_svg(c, k, ail=0.0):
    """後ろから見た事故機（機体の左が画面の左）。奥から：回る翼の円 → 翼と補助翼と翼端の板 → 胴 → 覆い（光る面）→ 水平尾翼 → 垂直尾翼。
    ail＝補助翼の切れ（メートル）。正＝右の翼を下げる向き（右の補助翼が上・左が下＝AAB p28 の 0.27秒）"""
    def P(x, y):
        return (c[0] + x * k, c[1] - y * k)
    hw = RB_SPAN
    g = ['<defs><radialGradient id="rbr" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#e8f4fb"/>'
         '<stop offset="0.6" stop-color="#9dbfd4"/><stop offset="1" stop-color="#557489"/></radialGradient></defs>']
    cx, cy = P(0.0, 0.02)
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{1.70 * k:.1f}" fill="#d8dee2" opacity="0.22" stroke="#8a969e" '
             f'stroke-opacity="0.4" stroke-width="1.5"/>')
    g.append(_poly([P(*q) for q in ((-hw, -0.26), (-0.5, -0.22), (0.5, -0.22), (hw, -0.26), (hw, -0.36), (0.5, -0.48),
                                    (-0.5, -0.48), (-hw, -0.36))], "#c3cbd1", "#44505a", 2))
    for sgn in (1, -1):
        x0, x1 = sgn * RB_AIL[0], sgn * RB_AIL[1]
        dy = ail * sgn
        g.append(_poly([P(x0, -0.30 + dy), P(x1, -0.29 + dy), P(x1, -0.37 + dy), P(x0, -0.38 + dy)], "#9aa5ad", "#44505a", 1.6))
        g.append(_poly([P(sgn * hw - 0.03, -0.52), P(sgn * hw + 0.03, -0.52), P(sgn * hw + 0.03, -0.12), P(sgn * hw - 0.03, -0.12)],
                       "#aeb8bf", "#44505a", 1.4))
    fx, fy = P(0.0, 0.0)
    g.append(f'<ellipse cx="{fx:.1f}" cy="{fy:.1f}" rx="{0.55 * k:.1f}" ry="{0.72 * k:.1f}" fill="#c9d1d7" stroke="#44505a" stroke-width="2.2"/>')
    ox, oy = P(0.0, 0.74)
    g.append(f'<ellipse cx="{ox:.1f}" cy="{oy:.1f}" rx="{0.30 * k:.1f}" ry="{0.22 * k:.1f}" fill="url(#rbr)" stroke="#44505a" stroke-width="1.8"/>')
    g.append(_poly([P(-RB_STAB, 0.34), P(RB_STAB, 0.34), P(RB_STAB, 0.26), P(-RB_STAB, 0.26)], "#b9c2c8", "#44505a", 1.8))
    g.append(_poly([P(-0.06, 0.40), P(0.06, 0.40), P(0.035, 1.72), P(-0.035, 1.72)], "#b9c2c8", "#44505a", 1.6))
    return "".join(g)


def rb_sky_svg(hz=RB_HZ):
    """快晴の空（AAB p16）。🔴 画面いっぱいに塗る（地平線より下は地平線の色のまま）＝空だけの見え方（ground=off）や、
    後ろから→横から（空だけ）へ入れ替えるときに下が黒く抜けない（⑤b-2 の下見で c104 の下半分が黒かった）"""
    return (f'<defs><linearGradient id="rbs" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{hz:.0f}">'
            '<stop offset="0" stop-color="#4f84b3"/><stop offset="1" stop-color="#cfe0ea"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="{H + 10}" fill="url(#rbs)"/>')


def rb_hills_svg(far=True, hz=RB_HZ):
    """遠い山並み／手前の丘（図3 の奥の山並みの概形）。🔴 横に流す（drift）ので 1920 の周期で継ぎ目なし（整数回の正弦の和）。"""
    import random
    rnd = random.Random("reno-hills-far" if far else "reno-hills-near")
    base = hz - (46.0 if far else 8.0)
    amp = 30.0 if far else 14.0
    comps = [(n, rnd.uniform(0.35, 1.0) * amp / (1 + j * 0.6), rnd.uniform(0, math.tau)) for j, n in enumerate((2, 3, 5, 7, 11))]
    pts = [(float(i), base - sum(a * math.sin(2 * math.pi * n * i / W + ph) for n, a, ph in comps)) for i in range(0, W + 1, 8)]
    d = f"M 0 {hz + 20:.1f} " + " ".join(f"L {x:.1f} {y:.1f}" for x, y in pts) + f" L {W} {hz + 20:.1f} Z"
    return f'<path d="{d}" fill="{"#a4b4bf" if far else "#b9a887"}"/>'


def rb_ground_svg(hz=RB_HZ, seed="reno-ground"):
    """砂漠の地面と筋（流れる＝速さ）。筋は画面の幅で折り返す（drift で継ぎ目なし）。"""
    import random
    rnd = random.Random(seed)
    g = [f'<rect x="0" y="{hz:.0f}" width="{W}" height="{H - hz + 10:.0f}" fill="#cbb792"/>']
    for j in range(20):
        y = hz + 12 + j * 15 + (j % 3) * 3
        x = rnd.uniform(0, W)
        for _ in range(4):
            ln = rnd.uniform(60, 190)
            for xa, xb in ((x, min(x + ln, W)), (0.0, max(0.0, x + ln - W))):
                if xb > xa:
                    g.append(f'<path d="M {xa:.0f} {y:.0f} H {xb:.0f}" stroke="#bda57f" stroke-width="3" opacity="0.7"/>')
            x = (x + ln + rnd.uniform(180, 420)) % W
    return "".join(g)


def rb_air_svg():
    """空だけの見え方（ground=off）の流れる筋（進む向き＝左へ流れる）。雲ではない（快晴＝AAB p16）＝細く薄い線だけ。"""
    import random
    rnd = random.Random("reno-air")
    g = []
    for j in range(14):
        y = 90 + j * 52 + rnd.uniform(-10, 10)
        x = rnd.uniform(0, W)
        ln = rnd.uniform(120, 320)
        for xa, xb in ((x, min(x + ln, W)), (0.0, max(0.0, x + ln - W))):
            if xb > xa:
                g.append(f'<path d="M {xa:.0f} {y:.0f} H {xb:.0f}" stroke="#ffffff" stroke-opacity="0.28" stroke-width="3"/>')
    return "".join(g)


def rb_pylon_svg(x, foot, h):
    """パイロン＝電柱の上の樽（#33 p2009「a barrel mounted at the top of a telephone pole … about 50-feet」）。色は記録に無い＝抽象。"""
    w, bw, bh = max(4.0, h * 0.035), h * 0.10, h * 0.12
    return (f'<rect x="{x - w / 2:.1f}" y="{foot - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#e7e2d6" stroke="#6f6a60" stroke-width="1.5"/>'
            f'<rect x="{x - bw / 2:.1f}" y="{foot - h - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" fill="#d9d2c3" '
            f'stroke="#6f6a60" stroke-width="1.5"/>')


def _rb_timeline(start, states, steps):
    """RB の鍵：見え方の入れ替え（0.35秒）→ そのあと 機首の上げ（0.55秒＝一気に）・傾き（ゆっくり）・補助翼。"""
    T = RB_T
    K = dict(side=[dict(stage=0, delay=0.0, a=1.0 if start["view"] == "side" else 0.0)],
             rear=[dict(stage=0, delay=0.0, a=1.0 if start["view"] == "rear" else 0.0)],
             pitch=[dict(stage=0, delay=0.0, rot=-float(start["pitch"]))],
             roll=[dict(stage=0, delay=0.0, rot=-float(start["roll"]))],
             ail=[dict(stage=0, delay=0.0, a=1.0 if start["ail"] == "right" else 0.0)],
             pylon=[dict(stage=0, delay=0.0, dx=1350.0)])
    prev = start
    for i, (st, sp) in enumerate(zip(states, steps)):
        dl = float(sp.get("delay", KEY_DELAY))
        t = dl
        if st["view"] != prev["view"]:
            for v in ("side", "rear"):
                K[v].append(dict(stage=i, delay=t, dur=T["view"], a=1.0 if st["view"] == v else 0.0))
            t += T["view"] + 0.25
        if float(st["pitch"]) != float(prev["pitch"]):
            K["pitch"].append(dict(stage=i, delay=t, dur=float(sp.get("dur", T["pitch"])), rot=-float(st["pitch"])))
        if float(st["roll"]) != float(prev["roll"]):
            K["roll"].append(dict(stage=i, delay=t, dur=float(sp.get("dur", T["roll"])), rot=-float(st["roll"])))
        if st["ail"] != prev["ail"]:
            K["ail"].append(dict(stage=i, delay=t + 0.2, dur=T["ail"], a=1.0 if st["ail"] == "right" else 0.0))
        if sp.get("pylon"):
            K["pylon"].append(dict(stage=i, delay=dl, dur=T["pylon"], dx=-1400.0))
        prev = st
    return K


def _scene_RB(start, states, steps):
    """RB＝空の中の事故機。view＝side（横から・機首が右）／rear（後ろから）＝段で入れ替えてよい（0.35秒で重ねて）。
    ground＝on（丘と砂漠と筋・パイロンが流れる＝c101・c215）／off（空と流れる筋だけ＝機首の上げを機体の向きだけで見せる）。
    🔴 上った高さ・降下は描かない（線2＝1.3秒の最大Gで止める）。板（トリムタブ）は描き分けない・渦も描かない（線3）"""
    allst = [start] + states
    if any(st["ground"] != start["ground"] for st in states):
        raise ValueError("illu RB：ground は場面の頭（start）で1つだけ")
    views = {st["view"] for st in allst}
    K = _rb_timeline(start, states, steps)
    rear_on = "rear" in views
    side_g = "side" in views and start["ground"] == "on"
    side_a = "side" in views and start["ground"] == "off"
    if side_g and rear_on:
        raise ValueError("illu RB：地面ありの横から（ground=on）と後ろからは同じ場面にしない（地面の流れる向きが逆）")
    grnd_keys = [dict(stage=0, delay=0.0, a=1.0)] if side_g else K["rear"]     # 地面は 横から（ground=on）か 後ろから のときだけ
    parts = [_part("sky", rb_sky_svg(), "AAB p16（快晴＝clear sky）")]
    if side_g or rear_on:
        parts += [dict(_part("hills_far", rb_hills_svg(True), "AAB p20（図3 の奥の山並み）", keys=grnd_keys),
                       drift=-14.0 if side_g else 6.0),
                  dict(_part("hills_near", rb_hills_svg(False), "AAB p20（図3）・p16（リノ＝ネバダの砂漠の空港）", keys=grnd_keys),
                       drift=-60.0 if side_g else 18.0),
                  dict(_part("ground", rb_ground_svg(), "AAB p16（砂漠の空港）", keys=grnd_keys), drift=-900.0 if side_g else 40.0)]
    if side_a:
        parts.append(dict(_part("air", rb_air_svg(), "AAB p16（快晴）", keys=K["side"]), drift=-1100.0))
    if side_g and any(sp.get("pylon") for sp in steps):
        parts.append(_part("pylon", rb_pylon_svg(960.0, RB_HZ + 40.0, 300.0), "#33 p2009（パイロン＝電柱の上の樽）",
                           keys=K["pylon"]))
    if rear_on:
        parts.append(_part("pylon8", rb_pylon_svg(300.0, RB_HZ + 10.0, 150.0), "AAB p28（パイロン8を回って崩れ始めた）・#33 p2009",
                           keys=K["rear"]))
    # 🔴 回す鍵（keys＝rot）と濃さの鍵（akeys＝a）は別の並び（build_jiko._il_scene）。1本にまとめると、長い回転（2.6秒）の途中に
    #    短い濃さの鍵（0.35秒）が入ったとき、回転が次の鍵の値へ飛ぶ（_il_state は「次の鍵の前に前の鍵が終わる」作り）
    first = True
    if "side" in views:
        parts.append(dict(_part("side", rb_side_svg(RB_C, RB_K), "AAB p14（図2＝機体の形）・p13（翼と尾翼を短くした）", RB_C,
                                K["pitch"]), akeys=K["side"], obj=dict(aircraft=1)))
        first = False
    if rear_on:
        for nm, ail, want in (("rear_n", 0.0, 0.0), ("rear_d", RB_AIL_D, 1.0)):
            if nm == "rear_d" and not any(st["ail"] == "right" for st in allst):
                continue
            vis = [dict(k, a=k["a"] * (1.0 - abs(want - a["a"]))) for k, a in _pair_keys(K["rear"], K["ail"])]
            p = dict(_part(nm, rb_rear_svg(RB_CR, RB_KR, ail), "AAB p14（図2 の寸法）・p13（翼端の板・補助翼を短くした）" +
                           ("・p28（0.27秒に補助翼が右の翼を下げる向きに）" if ail else ""), RB_CR, K["roll"]), akeys=vis)
            if first:
                p["obj"] = dict(aircraft=1)
                first = False
            parts.append(p)
    at = next((st for st, sp in zip(states, steps) if sp.get("rings")), None)
    if at is not None:
        c = (RB_C[0] - 0.4 * RB_K, RB_C[1] + 0.45 * RB_K)
        parts += _pulse_part("ring", ring_svg(c, 90.0, r=64), "AAB p17・p18（テレメトリー＝機体の状態を地上へ送る）", c, states, steps,
                             "rings", "out")
    return parts


def _rb_motion_end(start, states, steps):
    """段ごとの「大きく動く鍵」（見え方の入れ替え・機首の上げ）が終わる時刻（行頭からの秒）。札の既定の出る時刻に使う。
    傾き（roll）はゆっくり小さく動く＝札を待たせない（c305 の「0.27秒」が行の後ろへずれる）"""
    K = _rb_timeline(start, states, steps)
    out = {}
    for nm in ("side", "rear", "pitch"):
        for k in K[nm][1:]:
            out[k["stage"]] = max(out.get(k["stage"], 0.0), float(k.get("delay", 0.0)) + float(k.get("dur", 0.0)))
    return out


def _key_time(k):
    return (int(k["stage"]), float(k.get("delay", 0.0)))


def _pair_keys(ka, kb):
    """2つの並び（どちらも a の欄）を時刻でそろえ、[(その時刻の ka の鍵, kb の鍵)…]（前の値を引き継ぐ）。"""
    evs = sorted({_key_time(k) for k in ka + kb})
    out, a, b = [], dict(ka[0]), dict(kb[0])
    for tm in evs:
        for k in ka:
            if _key_time(k) == tm:
                a = dict(k)
        for k in kb:
            if _key_time(k) == tm:
                b = dict(k)
        dur = max(float(a.get("dur", 0.0)) if _key_time(a) == tm else 0.0, float(b.get("dur", 0.0)) if _key_time(b) == tm else 0.0)
        out.append((dict(stage=tm[0], delay=tm[1], dur=dur or 0.3, a=float(a["a"])), dict(b)))
    return out


def _rb_anchors(st):
    if st["view"] == "rear":
        d = -float(st["roll"])
        R = lambda x, y: rot_pt((RB_CR[0] + x * RB_KR, RB_CR[1] - y * RB_KR), d, RB_CR)  # noqa: E731
        return dict(plane=RB_CR, lwing=R(-RB_SPAN, -0.3), rwing=R(RB_SPAN, -0.3), lail=R(-3.75, -0.34), rail=R(3.75, -0.34),
                    top=R(0.0, 1.2))
    d = -float(st["pitch"])
    R = lambda x, y: rot_pt((RB_C[0] + x * RB_K, RB_C[1] - y * RB_K), d, RB_C)  # noqa: E731
    # 🆕 ⑤b-3：canopy（操縦席の覆い＝光る面の上）・engine（機首の覆い）・prop（回る翼の円の上の方）＝c107・c414 の札
    return dict(plane=R(0.0, 0.0), nose=R(4.5, 0.0), tail=R(*RB_SIDE["tail"]), mid=R(-0.4, -0.45), top=R(0.0, 0.9),
                ring=(RB_C[0] - 0.4 * RB_K, RB_C[1] + 0.45 * RB_K + 110.0), canopy=R(0.55, 0.80), engine=R(3.0, 0.10),
                prop=R(4.25, 1.15))


# ── RD：ピットの事故機（⑤b-2 は c109 の小さな絵＝尾翼の寄り tail だけ）。地面に置いた姿勢・脚は描かない（記録の図に無い）＝
#    尾翼へ寄って、胴の前と脚は枠の外。🔴 人（整備の仲間・検査員）は描かない（映像方針 §1 線2）
RD_K = 300.0                       # 1メートル＝300画素（尾翼の寄り）
RD_TAIL = (560.0, 560.0)           # 水平尾翼の後ろの縁の真ん中が来る画面の位置
RD_HZ = 330.0                      # 地平線（少し上から見下ろす＝尾翼の奥が駐機場の舗装）


def rd_ramp_svg():
    return (f'<rect x="0" y="{RD_HZ:.0f}" width="{W}" height="{H - RD_HZ + 10:.0f}" fill="#a9adb0"/>'
            + "".join(f'<path d="M 0 {RD_HZ + 40 + 70 * j:.0f} H {W}" stroke="#9ca0a3" stroke-width="3" opacity="0.6"/>'
                      for j in range(10)))


def rd_mark_svg():
    x, y = RD_TAIL
    return (f'<ellipse cx="{x + 40:.0f}" cy="{y:.0f}" rx="170" ry="90" fill="none" stroke="#1a2530" stroke-opacity="0.5" stroke-width="12"/>'
            f'<ellipse cx="{x + 40:.0f}" cy="{y:.0f}" rx="170" ry="90" fill="none" stroke="{C["mark"]}" stroke-width="6"/>')


def _scene_RD(start, states, steps):
    """RD＝ピットの事故機（尾翼の寄り）。mark＝尾翼（昇降舵とトリムタブのあたり）の輪。"""
    tx, ty = RB_SIDE["tail"]
    c = (RD_TAIL[0] - tx * RD_K, RD_TAIL[1] + ty * RD_K)
    return [_part("sky", rb_sky_svg(RD_HZ), "AAB p16（快晴）"),
            _part("hills", rb_hills_svg(True, RD_HZ), "AAB p20（図3 の奥の山並み）"),
            _part("ramp", rd_ramp_svg(), "AAB p37（9月12日の技術検査）・p19（ピット）"),
            dict(_part("plane", rb_side_svg(c, RD_K), "AAB p14（図2＝機体の形・水平尾翼と昇降舵とトリムタブ）"), obj=dict(aircraft=1)),
            _part("mark", rd_mark_svg(), "AAB p14（水平尾翼・昇降舵・トリムタブ）",
                  keys=_keys(start, states, steps, lambda st: _vis(st["mark"] == "on")))]


# ── RC：ボックス席とピット（地上から）── 15本目 ⑤b-3（2026-09-30）
# 記録（AAB）：p19「the edge of the pit area (where many other spectators were located) was 748 feet south of the showline,
#   and a fuel truck was parked on the ramp near the pits」／p20「Low-level metal fencing was installed at the edge of the pit
#   area between the crew pits and the ramp …」「Metal piping fitted with curtains was installed at the edge of the box seating
#   area between the box seats and the ramp」／p21 注26「the curtains used by spectators were blue and red」／p16（快晴）・
#   p20 図3（スタンド・奥の山並み）。
# 🔴 形・高さ・間隔・幕の色の並びは記録に無い＝抽象（平らな塗り・左下に「模式」）。人は顔の無い群れだけ（`crowd_layout`＝
#    重なって数えられない形・枠の外まで続く）＝役割 spectators・場面の時刻 at は落ちる瞬間（`cuts.ss.ILLU_CROWD_UNTIL`）より前
#    （門番 ②）。燃料車は1台（obj）。ピットの機体・テント・ほかの車は描かない（数が記録に無い）。スタンドは枠で切れる1続きの帯
#    （数を名乗らない＝図の「3つ」は A の上から見た絵で）
# 見え方：pits＝駐機場からピットの端（低い金属の柵）・その奥の観客・駐機場の燃料車（c212）／box＝駐機場からボックス席の前の幕と
#   その奥の観客・スタンド（c726）／fences＝2つの柵の寄りを低い位置から（左＝ピットの前の低い金属の柵・右＝ボックス席の前の
#   幕を付けたパイプ＝c816。落ちたあとの章＝人を描かない。柵の奥は**ぼかした面**＝人も物も描かない）
# 地上から見る絵＝ピンホールの透視（焦点 RC_F 画素・目の高さ E メートル・地平線 hz）：地面の点（横 x・奥行き D メートル）は
#   (cx＋F·x／D, hz＋F·E／D)、高さ h の点は (…, hz＋F·(E−h)／D)
RC_F = 1150.0
RC_CAM = dict(pits=dict(E=1.6, hz=470.0), box=dict(E=1.6, hz=470.0), fences=dict(E=0.6, hz=400.0))
RC_PIT_D, RC_BOX_D = 24.0, 18.0          # カメラから柵までの奥行き（記録に無い＝模式）
RC_FENCE_H, RC_PIPE_H = 1.05, 1.2        # 低い金属の柵・幕を付けたパイプの高さ（記録に無い＝「low-level」の模式）
RC_TRUCK = dict(D=19.0, x0=-9.0, x1=-1.0, h=3.0)    # 燃料車（奥行き・横の範囲・高さ＝記録に無い＝抽象・運転台が右）
RC_BLUE, RC_RED = "#2f5c9c", "#b23f36"   # 幕の青と赤（注26。色味と並びは記録に無い＝交互の模式）
RC_FEN = dict(D=4.0, split=960.0)        # fences：柵までの奥行き・左右の境
RC_VIEW = dict(pits="駐機場から見たピット", box="駐機場から見たボックス席", fences="駐機場から見た2つの柵（低い位置から）")


def rc_p(view, x, D, h=0.0, cx=960.0):
    c = RC_CAM[view]
    return (cx + RC_F * x / D, c["hz"] + RC_F * (c["E"] - h) / D)


def rc_ground_svg(view, y0, col="#8e9295", line="#7f8386", x0=0.0, x1=float(W), cx=960.0):
    """手前の舗装（駐機場）。奥行きごとの継ぎ目と、消える点へ向かう線（平らな地面の手がかり）。"""
    c = RC_CAM[view]
    g = [f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" height="{H - y0 + 10:.0f}" fill="{col}"/>']
    for D in (3.0, 4.2, 5.8, 8.0, 11.0, 15.0):
        y = c["hz"] + RC_F * c["E"] / D
        if y0 + 6 < y < H:
            g.append(f'<path d="M {x0:.0f} {y:.1f} H {x1:.0f}" stroke="{line}" stroke-width="2.5" opacity="0.8"/>')
    d0, d1 = RC_F * c["E"] / max(1.0, y0 - c["hz"]), RC_F * c["E"] / (H - c["hz"])
    for xm in range(-30, 31, 6):
        a, b = cx + RC_F * xm / d0, cx + RC_F * xm / d1
        g.append(f'<path d="M {a:.1f} {y0:.1f} L {b:.1f} {H}" stroke="{line}" stroke-width="2" opacity="0.55"/>')
    return (f'<clipPath id="rcg{int(x0)}"><rect x="{x0:.0f}" y="0" width="{x1 - x0:.0f}" height="{H}"/></clipPath>'
            f'<g clip-path="url(#rcg{int(x0)})">' + "".join(g) + "</g>")


def rc_fence_svg(view, D, h=RC_FENCE_H, step=2.5, cx=960.0, x0=0.0, x1=float(W)):
    """低い金属の柵（柱と2本の横棒＝形は記録に無い＝抽象）。x0〜x1 の画面の範囲に描く。"""
    k = RC_F / D
    xm0, xm1 = (x0 - cx) / k - step, (x1 - cx) / k + step
    g = []
    for yh in (h, h * 0.5):
        (_, y) = rc_p(view, 0.0, D, yh)
        g.append(f'<path d="M {x0:.0f} {y:.1f} H {x1:.0f}" stroke="#4d565c" stroke-width="{0.075 * k:.1f}"/>'
                 f'<path d="M {x0:.0f} {y:.1f} H {x1:.0f}" stroke="#aab2b7" stroke-width="{0.045 * k:.1f}"/>')
    xm = math.floor(xm0 / step) * step
    while xm <= xm1:
        (px, ytop), (_, ybot) = rc_p(view, xm, D, h + 0.04, cx), rc_p(view, xm, D, 0.0, cx)
        if x0 - 20 < px < x1 + 20:
            g.append(f'<rect x="{px - 0.03 * k:.1f}" y="{ytop:.1f}" width="{0.06 * k:.1f}" height="{ybot - ytop:.1f}" '
                     f'fill="#aab2b7" stroke="#4d565c" stroke-width="{max(1.5, 0.012 * k):.1f}"/>')
        xm += step
    return "".join(g)


def rc_curtain_svg(view, D, h=RC_PIPE_H, step=3.0, cx=960.0, x0=0.0, x1=float(W)):
    """幕を付けた金属のパイプ（柱・上のパイプ・柱のあいだに幕＝青と赤の交互は模式）。"""
    k = RC_F / D
    xm0, xm1 = (x0 - cx) / k - step, (x1 - cx) / k + step
    g = []
    xm = math.floor(xm0 / step) * step
    j = int(round(xm / step))
    while xm <= xm1:
        (a, yt), (b, _) = rc_p(view, xm, D, h - 0.04, cx), rc_p(view, xm + step, D, h - 0.04, cx)
        (_, yb) = rc_p(view, xm, D, 0.15, cx)
        col = RC_BLUE if j % 2 == 0 else RC_RED
        g.append(f'<path d="M {a:.1f} {yt:.1f} L {b:.1f} {yt:.1f} L {b:.1f} {yb:.1f} L {a:.1f} {yb:.1f} Z" fill="{col}" '
                 f'stroke="#1f262b" stroke-width="{max(1.5, 0.01 * k):.1f}"/>')
        for q in range(1, 4):                      # 布のたるみ（縦の筋）
            xx = a + (b - a) * q / 4
            g.append(f'<path d="M {xx:.1f} {yt + 4:.1f} V {yb - 3:.1f}" stroke="#000" stroke-opacity="0.13" '
                     f'stroke-width="{max(2.0, 0.02 * k):.1f}"/>')
        xm += step
        j += 1
    (_, yp) = rc_p(view, 0.0, D, h)
    g.append(f'<path d="M {x0:.0f} {yp:.1f} H {x1:.0f}" stroke="#4d565c" stroke-width="{0.07 * k:.1f}"/>'
             f'<path d="M {x0:.0f} {yp:.1f} H {x1:.0f}" stroke="#c3cacf" stroke-width="{0.04 * k:.1f}"/>')
    xm = math.floor(xm0 / step) * step
    while xm <= xm1:
        (px, ytop), (_, ybot) = rc_p(view, xm, D, h + 0.03, cx), rc_p(view, xm, D, 0.0, cx)
        g.append(f'<rect x="{px - 0.025 * k:.1f}" y="{ytop:.1f}" width="{0.05 * k:.1f}" height="{ybot - ytop:.1f}" '
                 f'fill="#c3cacf" stroke="#4d565c" stroke-width="{max(1.5, 0.012 * k):.1f}"/>')
        xm += step
    return "".join(g)


def rc_truck_svg(view):
    """燃料車（1台＝AAB p19）。横から見た形（運転台・タンク・車輪）＝形と色は記録に無い＝抽象。"""
    t = RC_TRUCK
    D, x0, x1 = t["D"], t["x0"], t["x1"]
    k = RC_F / D

    def P(x, h):
        return rc_p(view, x, D, h)
    (sx0, gy), (sx1, _) = P(x0 - 0.3, 0.0), P(x1 + 0.3, 0.0)
    g = [f'<ellipse cx="{(sx0 + sx1) / 2:.1f}" cy="{gy:.1f}" rx="{(sx1 - sx0) / 2:.1f}" ry="{0.22 * k:.1f}" fill="#000" '
         f'opacity="0.22"/>']
    (a, b), (c_, d) = P(x0 + 0.2, 1.0), P(x1 - 0.2, 0.55)
    g.append(f'<rect x="{a:.1f}" y="{b:.1f}" width="{c_ - a:.1f}" height="{d - b:.1f}" fill="#3a4147"/>')
    (a, b), (c_, d) = P(x0, 3.0), P(x1 - 2.5, 1.0)
    g.append(f'<rect x="{a:.1f}" y="{b:.1f}" width="{c_ - a:.1f}" height="{d - b:.1f}" rx="{0.9 * k:.1f}" fill="#e2e5e3" '
             f'stroke="#4b545a" stroke-width="2.5"/>')
    g.append(f'<path d="M {a + 0.4 * k:.1f} {(b + d) / 2:.1f} H {c_ - 0.4 * k:.1f}" stroke="#9aa3a8" stroke-width="{0.12 * k:.1f}"/>')
    cab = [P(x1 - 2.3, 1.0), P(x1 - 2.3, 2.75), P(x1 - 0.9, 2.75), P(x1, 1.8), P(x1, 1.0)]
    g.append(_poly(cab, "#c9ced1", "#4b545a", 2.5))
    g.append(_poly([P(x1 - 2.0, 2.55), P(x1 - 1.0, 2.55), P(x1 - 0.35, 1.9), P(x1 - 2.0, 1.9)], "#6f8796", "#4b545a", 2))
    for xw in (x0 + 1.2, x0 + 2.6, x1 - 1.2):
        (wx, wy) = P(xw, 0.5)
        g.append(f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="{0.5 * k:.1f}" fill="#23282c"/>'
                 f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="{0.2 * k:.1f}" fill="#8a9297"/>')
    return "".join(g)


def rc_stands_svg(view):
    """スタンド（box の奥・枠で切れる1続きの帯＝数を名乗らない）と、段ごとの小さな群れ。返り値＝(SVG, 群れの並び)。"""
    c = RC_CAM[view]
    tiers = [(40.0 + 3.0 * i, 1.0 + 1.25 * i) for i in range(7)]     # (奥行き, 段の高さ)＝記録に無い＝模式
    (_, yf), (_, yb) = rc_p(view, 0.0, tiers[0][0], 0.0), rc_p(view, 0.0, tiers[-1][0], tiers[-1][1] + 1.2)
    g = [f'<rect x="0" y="{yb:.1f}" width="{W}" height="{yf - yb:.1f}" fill="#8796a1"/>',
         f'<path d="M 0 {yb:.1f} H {W}" stroke="#56626b" stroke-width="5"/>']
    rows = []
    for D, h in tiers:
        (_, y) = rc_p(view, 0.0, D, h)
        g.append(f'<path d="M 0 {y:.1f} H {W}" stroke="#6b7a85" stroke-width="3"/>')
        lay = crowd_layout(0.0, float(W), y, RC_F * 0.95 / D, rows=1)
        rows.append((lay, 0.0, float(W)))
        g.append(crowd_svg(lay, cols=("#34414b", "#34414b", "#34414b")))
    return "".join(g), rows


def rc_haze_svg(view, y1, x0=0.0, x1=float(W)):
    """柵の奥のぼかした面（fences）＝人も物も描かない（落ちたあとの章・線2）。地平線より上の遠い所を平らな霞に。"""
    c = RC_CAM[view]
    return (f'<rect x="{x0:.0f}" y="{y1:.0f}" width="{x1 - x0:.0f}" height="{c["hz"] - y1 + 2:.0f}" fill="#d7dbd6"/>'
            f'<rect x="{x0:.0f}" y="{c["hz"]:.0f}" width="{x1 - x0:.0f}" height="{H - c["hz"]:.0f}" fill="#b8b2a3"/>')


def _rc_clip(svg, x0, x1, ident):
    """左右に分けた絵（fences）の片側を枠で切る。"""
    return (f'<defs><clipPath id="{ident}"><rect x="{x0:.0f}" y="0" width="{x1 - x0:.0f}" height="{H}"/></clipPath></defs>'
            f'<g clip-path="url(#{ident})">{svg}</g>')


def _rc_anchors(view):
    if view == "pits":
        t = RC_TRUCK
        return dict(fence=rc_p(view, 3.0, RC_PIT_D, RC_FENCE_H), truck=rc_p(view, (t["x0"] + t["x1"] - 2.5) / 2, t["D"], 3.0),
                    crowd=rc_p(view, 6.0, RC_PIT_D + 3.0, 1.6))
    if view == "box":
        return dict(box=rc_p(view, 2.0, RC_BOX_D + 4.0, 1.7), curtain=rc_p(view, -2.5, RC_BOX_D, 0.7))
    s = RC_FEN["split"]
    return dict(fence=rc_p(view, 0.0, RC_FEN["D"], RC_FENCE_H, cx=s / 2),
                curtain=rc_p(view, 0.0, RC_FEN["D"], RC_PIPE_H * 0.6, cx=s + (W - s) / 2))


def _scene_RC(start, states, steps):
    """RC＝ボックス席とピット（地上から）。view＝pits／box／fences（場面の頭で1つ）。crowd＝観客の群れ・fuel＝燃料車。"""
    v = start["view"]
    if any(st["view"] != v for st in states):
        raise ValueError("illu RC：view は場面の頭で1つだけ")
    c = RC_CAM[v]
    parts = [_part("sky", rb_sky_svg(c["hz"]), "AAB p16（快晴）")]
    ck = _keys(start, states, steps, lambda st: _vis(st["crowd"] == "on"))
    if v == "pits":
        (_, yf) = rc_p(v, 0.0, RC_PIT_D, 0.0)
        parts += [_part("hills", rb_hills_svg(True, c["hz"]), "AAB p20（図3 の奥の山並み）"),
                  _part("pitground", f'<rect x="0" y="{c["hz"]:.0f}" width="{W}" height="{yf - c["hz"] + 2:.0f}" fill="#b9ad96"/>',
                        "AAB p19（ピット）・p20（図3）")]
        (_, base) = rc_p(v, 0.0, RC_PIT_D + 2.0, 0.0)
        lay = crowd_layout(0.0, float(W), base, RC_F * 1.7 / (RC_PIT_D + 2.0), rows=3)
        parts.append(_part("crowd", crowd_svg(lay), "AAB p19（ピットのあたりにも多くの観客＝many other spectators）",
                           keys=ck, role="spectators", crowd=[dict(layout=lay, x0=0.0, x1=float(W))]))
        parts += [_part("fence", rc_fence_svg(v, RC_PIT_D), "AAB p20（ピットと駐機場のあいだの低い金属の柵）"),
                  _part("ramp", rc_ground_svg(v, yf), "AAB p19（駐機場＝ramp）"),
                  dict(_part("truck", rc_truck_svg(v), "AAB p19（燃料車がピットの近くの駐機場に止まっていた）",
                             keys=_keys(start, states, steps, lambda st: _vis(st["fuel"] == "on"))), obj=dict(fuel_truck=1))]
    elif v == "box":
        (_, yf) = rc_p(v, 0.0, RC_BOX_D, 0.0)
        svg, rows = rc_stands_svg(v)
        parts += [_part("hills", rb_hills_svg(True, c["hz"]), "AAB p20（図3 の奥の山並み）"),
                  _part("stands", svg, "AAB p19（スタンド＝grandstands）・p20（図3）", keys=ck, role="spectators",
                        crowd=[dict(layout=lay, x0=x0, x1=x1) for lay, x0, x1 in rows])]
        (_, base) = rc_p(v, 0.0, RC_BOX_D + 2.0, 0.0)
        lay = crowd_layout(0.0, float(W), base, RC_F * 1.7 / (RC_BOX_D + 2.0), rows=4)
        parts += [_part("crowd", crowd_svg(lay), "AAB p19（観客のボックス席）", keys=ck, role="spectators",
                        crowd=[dict(layout=lay, x0=0.0, x1=float(W))]),
                  _part("curtain", rc_curtain_svg(v, RC_BOX_D),
                        "AAB p20（ボックス席と駐機場のあいだの幕を付けた金属のパイプ）・p21（注26＝幕は青と赤）"),
                  _part("ramp", rc_ground_svg(v, yf), "AAB p19（駐機場＝ramp）")]
    else:
        s, D = RC_FEN["split"], RC_FEN["D"]
        (_, yf) = rc_p(v, 0.0, D, 0.0)
        (_, yh) = rc_p(v, 0.0, D, 2.4)
        parts += [_part("haze", rc_haze_svg(v, max(0.0, yh)), "AAB p20（柵の場所）"),
                  _part("ramp", rc_ground_svg(v, yf, x0=0.0, x1=s, cx=s / 2) + rc_ground_svg(v, yf, x0=s, x1=float(W), cx=s + (W - s) / 2),
                        "AAB p19（駐機場＝ramp）"),
                  # 🔴 ⑤b-3 の下見：幕の板は範囲の外まで描く作り＝右半分の幕が左半分へはみ出して低い金属の柵を覆った
                  #    ＝左右それぞれを枠で切る（clip）。寄りの絵では柱の間隔を詰める（2.5→1.2・3.0→1.6 メートル＝模式）
                  _part("fence", _rc_clip(rc_fence_svg(v, D, step=1.2, cx=s / 2, x0=0.0, x1=s - 6.0), 0.0, s - 6.0, "rcf"),
                        "AAB p20（ピットと駐機場のあいだの低い金属の柵）"),
                  _part("curtain", _rc_clip(rc_curtain_svg(v, D, step=1.6, cx=s + (W - s) / 2, x0=s + 6.0, x1=float(W)),
                                            s + 6.0, float(W), "rcc"),
                        "AAB p20（ボックス席と駐機場のあいだの幕を付けた金属のパイプ）・p21（注26＝幕は青と赤）"),
                  _part("split", f'<rect x="{s - 6:.0f}" y="0" width="12" height="{H}" fill="#10161b"/>', "AAB p20（柵の場所）")]
    return parts


# ══════════════════════════════════════════════════════════
#  札（段ごとの `_a<番号>`）と、左上の「再現イラスト」・左下の出典
# ══════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════
#  16本目（バイオントダム災害）⑤b-2（2026-10-01）：VA 上から見た谷（北が上）
# ══════════════════════════════════════════════════════════
# 🔴 鍵は頭に V（14本目 A〜E・15本目 RA〜RD は selftest の見本が使う＝触らない）。VB・VC（⑤b-3）・VD（⑤b-4）も V の頭で足す
# 🔴 守りの線（Vault 映像方針 16本目 §2・§7・§9＝ルール §5b-111）：
#    ・形のもと＝#100 イタリア軍地理院 1934年の地形図（PD）を**目で読んだ点**（正本＝`ref/ep16/map16.json`・道具＝
#      `ref/ep16/measure_map16.py check`＝記録の距離〈トンネル2.5km・北の岸の印1.1km・崩れた幅1.7km〉・面積〈1.9km²〉・
#      Wikidata の4点で縮尺と向きを照らす）。座標は #100 の画素（x 東・y 南）＝1画素 5.379メートル（1 km 方眼＝185.9画素）。
#      茶と灰の単色刷りで等高線は1本ずつ追えない＝湖の700mの線は標高の点から内挿した**概略**・標高の帯は谷からの距離の**模式**
#      （左下の出典の行で断る）。S8 の図・BY-SA・CC BY・Google Earth はなぞらない
#    ・人は置かない（22時39分に町の人がどこにいたかの記録が無い＝S1・S8・S9）。町と集落は建物の面だけ（数えない形＝斜めの縞）。
#      消えるのは S1 PDF98 が挙げた所だけ＝ロンガローネ・ピラーゴ・フォルナーチェ（ピアーヴェ川の谷）・ピネダとサン・マルティーノ
#      （湖の岸）。ファエとカステッラヴァッツォ（の一部）は #100 の外＝描かない。記録に無い町（リヴァルタ・ヴィッラノーヴァ・
#      コディッサーゴ）は建物の面を描かない（残った／消えたのどちらも名乗らない）
#    ・記録の最高を越えない（北の岸の印は 930m の2か所＝S1 PDF146）。上からの絵は高さを描かない＝谷の真ん中で盛り上がる水も無い
#    ・夜の色（月・星・明かりは描かない）。動く水・塊・ダムは明るい固定の色（夜の地と ΔE 25 以上）
#    ・縮尺は1画素あたり1.5m 以上（門番 ⑧）＝人が1画素に満たない
VA_MPX = 5.379                     # #100 の1画素＝メートル（1 km 方眼＝185.9画素・measure_map16.py grid）
VA_PTS = dict(                     # 目で読んだ点（#100 の画素）＝map16.json の points と同じ（selftest が照合）
    dam=(535.0, 536.0), casso=(577.0, 437.0), erto=(1148.0, 424.0), longarone=(140.0, 520.0), pirago=(105.0, 634.0),
    fornace=(118.0, 697.0), smartino=(1323.0, 352.0), pineda=(1058.0, 585.0), gorge_exit=(330.0, 545.0),
    tunnel_in=(1000.0, 507.0), tunnel_out=(525.0, 527.0), north_dam=(535.0, 445.0), north_1100=(740.0, 448.0),
    slide_w=(553.0, 551.0), slide_e=(869.0, 610.0), road_up=(560.0, 508.0), road_down=(345.0, 532.0), toc=(715.0, 700.0))
VA_LINES = dict(                   # map16.json の lines と同じ
    vajont=((1480, 394), (1440, 392), (1380, 392), (1320, 398), (1270, 418), (1240, 438), (1200, 468), (1150, 503),
            (1100, 515), (1045, 528), (1000, 552), (945, 574), (900, 578), (850, 575), (800, 565), (750, 550), (700, 539),
            (650, 547), (600, 546), (560, 535), (535, 536), (500, 540), (450, 545), (400, 547), (360, 543), (330, 545),
            (300, 552), (270, 562)),
    piave=((205, 250), (215, 320), (222, 385), (214, 450), (206, 515), (214, 580), (226, 645), (232, 705), (242, 780),
           (248, 845)),
    tunnel=((525, 527), (560, 519), (640, 521), (720, 514), (800, 526), (880, 527), (950, 516), (1000, 507)),
    road=((1140, 436), (1060, 468), (990, 488), (900, 500), (800, 508), (700, 503), (620, 500), (560, 508), (500, 520),
          (440, 528), (385, 532), (345, 532), (300, 532), (250, 530), (200, 525), (165, 522)),
    road_casso=((620, 500), (600, 470), (577, 445)))
# 湖の700mの線の概略＝[x, 川の y, 北の岸までの画素, 南の岸までの画素]（map16.json の lake_stations の rows と同じ）
VA_LAKE = ((535, 536, 15, 15), (560, 535, 15, 16), (600, 546, 18, 18), (650, 547, 20, 22), (700, 539, 22, 28),
           (750, 550, 24, 32), (800, 565, 22, 30), (850, 575, 32, 34), (900, 578, 46, 32), (945, 574, 52, 28),
           (1000, 552, 44, 28), (1045, 528, 36, 40), (1100, 515, 46, 30), (1150, 503, 44, 48), (1200, 468, 40, 30),
           (1240, 438, 48, 24), (1270, 418, 40, 22), (1320, 398, 18, 16), (1380, 392, 14, 12), (1440, 392, 10, 9),
           (1480, 394, 0, 0))
VA_POLY = dict(                    # map16.json の polys と同じ
    piave_floor=((185, 250), (170, 330), (160, 390), (165, 440), (168, 500), (172, 560), (150, 600), (145, 650), (152, 700),
                 (160, 760), (165, 845), (170, 1000), (330, 1000), (318, 845), (306, 760), (304, 690), (304, 620),
                 (310, 575), (330, 555), (305, 520), (300, 470), (290, 420), (262, 380), (240, 330), (228, 250)),
    longarone=((128, 428), (152, 428), (160, 470), (166, 520), (170, 565), (165, 605), (140, 615), (122, 590), (115, 545),
               (118, 490), (122, 455)),
    pirago=((86, 622), (122, 618), (128, 640), (110, 652), (88, 648)),
    fornace=((108, 690), (124, 688), (128, 702), (110, 706)),
    casso=((563, 431), (588, 428), (594, 440), (580, 448), (565, 445)),
    erto=((1128, 414), (1150, 408), (1172, 416), (1168, 434), (1140, 436)),
    smartino=((1306, 346), (1330, 342), (1340, 352), (1322, 361), (1305, 357)),
    pineda=((1040, 578), (1062, 575), (1076, 583), (1064, 594), (1042, 592)),
    slide_back=((869, 610), (884, 675), (866, 742), (828, 790), (765, 814), (690, 814), (625, 790), (580, 742), (558, 675),
                (553, 600)))
# ダムの弧（上から見たアーチ＝上流〈東〉へ張り出す・天端の長さ190m＝S9 PDF6 の寸法の範囲。弧の形は模式）
VA_DAM_N, VA_DAM_S, VA_DAM_C = (533.0, 520.0), (533.0, 552.0), (540.0, 536.0)
VA_SHIFT = 65.0                    # 塊が北へ動いた量（画素）＝約350m（S8 p.46「水平に300〜400m」）
VA_GORGE_W = 8.0                   # 峡谷の暗い筋の幅（画素＝約43m・模式）。⑤b-2 の下見：13（70m）は近い見え方で37画素の黒い帯＝道路に見えた
VA_GORGE_PX = (6.0, 16.0)          # 画面の上の峡谷の筋の太さの下限と上限（画素）
# ピアーヴェ川の谷へ広がる水の範囲（谷底＋町の段丘＝ロンガローネ・ピラーゴ・フォルナーチェを覆う・南北は画面の外へ続く＝模式）
VA_FLOOD = ((185, 250), (160, 330), (140, 390), (112, 425), (103, 470), (100, 530), (104, 590), (74, 614), (72, 655),
            (94, 690), (97, 722), (118, 780), (138, 845), (150, 1000), (330, 1000), (318, 845), (306, 760), (304, 690),
            (304, 620), (312, 575), (345, 560), (372, 546), (345, 528), (305, 520), (300, 470), (290, 420), (262, 380),
            (240, 330), (228, 250))
VA_FLOOD_SPLIT = 548.0             # 北へ広がる水／南へ広がる水の境（画素の y）
VA_FLOOD_GO = dict(n=((345, 545), (290, 530), (230, 500), (190, 440), (185, 380), (200, 300), (205, 200)),
                   s=((345, 545), (290, 560), (230, 590), (180, 640), (175, 720), (195, 820), (215, 1000)))
VA_WAVE_W = ((578, 528), (548, 534), (533, 536), (500, 540), (450, 545), (400, 547), (360, 543), (330, 545))
VA_WAVE_W_W = 34.0                 # ダムを越えた水の帯の幅（画素＝約180m・模式。高さは描かない）
VA_EAST_X0 = 880.0                 # 東へ向かった波が走る湖（塊の東の端から上流の端まで）
VA_SPLIT_X = (665.0, 800.0)        # c316 会社の説明（想定）の土砂の帯（模式）
# 見る向きの合図（Vault 映像方針 16本目 §4）：B＝谷を横切る断面（約1.1km上流の点を通る南北の線・西を向いて見る）／
#   C＝谷に沿う断面（ダムを通る東西の線・南を向いて見る）／D＝正面から見た斜面（北の岸の目の印・南を向いて見る）
VA_CUT = dict(B=dict(a=(740.0, 360.0), b=(740.0, 830.0), col="#3fb8a8", eye=(778.0, 470.0), look=180.0),
              C=dict(a=(390.0, 536.0), b=(905.0, 536.0), col="#e2a83c", eye=(640.0, 470.0), look=90.0),
              D=dict(a=None, b=None, col="#f3f6f8", eye=(700.0, 472.0), look=90.0))
VA_SWITCH = "上から見ると"         # 切り替えの字（画面の上の真ん中・約1.2秒で消える）。語りが同じ言葉を言うカットは出さない
VA_LAB = "上から見た図（北が上）"
VA_VIEW = dict(wide=dict(c=(770.0, 560.0), mpp=4.1),       # 谷の全体（ロンガローネ〜湖の上流の端）
               near=dict(c=(720.0, 545.0), mpp=1.9),       # ダムと崩れた斜面（トンネルの入口まで）
               west=dict(c=(392.0, 565.0), mpp=2.2))       # 峡谷の出口とピアーヴェ川の谷（ロンガローネ・ピラーゴ・フォルナーチェ）
VA_Y0 = 500.0                      # 画面の真ん中の y（左上の札の下〜左下の出典の上）
VA_BANDS = (1500.0, 950.0, 520.0, 220.0)    # 標高の帯（模式）＝谷底・湖からの距離（メートル）
VA_PAL = dict(
    day=dict(b0="#7c8b69", b1="#899a75", b2="#97a881", b3="#a6b68e", b4="#b5c49c", floor="#d5d0b8", floor_ln="#c3bda2",
             gorge="#66735e", lake="#5d92b4", shore="#3f7193", river="#4c86ab", house="#c49a84", house_ln="#9c725e",
             road="#f1e9d3", road_ln="#7d735e", scar="#a39a8a"),
    # 夜（⑤b-2 の下見のあと check_color.de で測った）：湖と谷の帯の差 7.2 → 22.2（湖 #1b3653 → #2a5f8f）・
    #   建物の面と地の差 17.4 → 27.2（#625e68 → #807886＝消える前の町が夜でも見える・泥の色とも 25.7）
    night=dict(b0="#151b27", b1="#1a2130", b2="#1f2738", b3="#252e41", b4="#2b3549", floor="#333d52", floor_ln="#3b465b",
               gorge="#0e131b", lake="#2a5f8f", shore="#5584ad", river="#3c6c97", house="#807886", house_ln="#5e5866",
               road="#858d9f", road_ln="#3c4352", scar="#77726a"),
    dawn=dict(b0="#4f5868", b1="#566070", b2="#5e6878", b3="#667082", b4="#6f798b", floor="#8a8e94", floor_ln="#7c8188",
              gorge="#454c58", lake="#5a7690", shore="#46637d", river="#46637d", house="#8c8584", house_ln="#6e6766",
              road="#a2a6af", road_ln="#5d616b", scar="#86807a"))
# 動く物・大事な物は時刻で変えない明るい色（夜の地と ΔE 25 以上＝門番 ⑬〈⑤b-3〉の値）
VA_FIX = dict(dam="#e6eaed", dam_ln="#20262d", block="#b9a079", block_ln="#5e4b33", flood="#a8d9ec", foam="#dff1f9",
              mud="#8c7357", mud_ln="#5f4c38", split="#a8916f", flow="#f2c14e")
VA_T = dict(wave=0.9, flood=1.3, flood_lag=0.7, towns_lag=0.55, towns=0.55, recede=0.8, mud=0.8, slide=0.9, block=0.6,
            tunnel=1.6, ends=0.4, road=1.4, low=0.6, gates=0.45, split=0.8, flow=1.6, marks=0.45, wave_e=2.6, shore=0.8,
            dawn=1.8, line=0.45, prev_hold=1.5, prev_fade=0.5, prev_thin=0.55, switch_hold=1.2, switch_fade=0.35)
# 部品の出典（rec）。頁は ss.REC_DOCS の通し番号（S1＝PDF の頁・S8＝p1041〜・S9＝p2001〜・#100＝画像＝p1）
VA_REC = dict(
    ground="#100 p1（1934年の地形図＝谷・川・村の位置・湖の700mの線の概略）",
    dawn="S1 p98（10月10日の夜明けには…もう存在しなかった）",
    towns="S1 p98（ロンガローネ・ピラーゴ・フォルナーチェ＝夜明けにはもう存在しなかった）・#100 p1（位置）",
    shore="S1 p98（湖の岸のピネダとサン・マルティーノ）・#100 p1（位置）",
    dam="S1 p171（ダムは耐えた）",
    block="S1 p147（1つの塊のまま）・S8 p1046（水平に300〜400m）・S1 p146（北の岸に乗り上げた）",
    slide="S1 p144（崩れた斜面＝幅およそ1.7キロ・面積およそ1.9平方キロ）",
    tunnel="S1 p85（右岸の岩の中の迂回トンネル・出口はダムの近く・入口は約2,500m上流）",
    split="S9 p2007（崩れても2つの湖をつなぐ迂回トンネル）・S1 p78（洪水を流せる）",
    road="S1 p98（エルト・カッソからロンガローネへの道・730m未満）",
    gates="S1 p98（上の入口＝作業員2人・下の入口＝憲兵隊がふさいだか、ふさごうとしていた）",
    marks="S1 p146（北の岸のダムの真横と約1.1km上流で930m）",
    wave_w="S1 p146（西へダムを越えた）・S1 p98（ダムを越えてピアーヴェ川の谷へ）",
    flood="S1 p98（ダムを越えてピアーヴェ川の谷へ）",
    wave_e="S1 p146（東へ・湖の上流の岸へ）")


def va_px(p, view):
    """#100 の画素の点 → VA の見え方 view の画面の点。"""
    v = VA_VIEW[view]
    k = VA_MPX / v["mpp"]
    return (960.0 + (p[0] - v["c"][0]) * k, VA_Y0 + (p[1] - v["c"][1]) * k)


def va_path(view, pts, per=8, closed=False):
    return _smooth([va_px(p, view) for p in pts], closed=closed, per=per)


def va_shore(x, side):
    """湖の700mの線の概略の、x での岸の y（side＝"n" 北／"s" 南）。行のあいだは直線（measure_map16.shore と同じ式）。"""
    for (x0, y0, n0, s0), (x1, y1, n1, s1) in zip(VA_LAKE, VA_LAKE[1:]):
        if x0 <= x <= x1:
            f = (x - x0) / (x1 - x0) if x1 > x0 else 0.0
            y, n, s = y0 + (y1 - y0) * f, n0 + (n1 - n0) * f, s0 + (s1 - s0) * f
            return y - n if side == "n" else y + s
    raise ValueError(f"illu VA：x={x} は湖の範囲の外")


def va_dam_arc(n=10):
    """ダムの弧（南のたもと → 冠 → 北のたもと）。2次のベジエを冠を通るように置いた。"""
    (nx, ny), (sx, sy), (cx, cy) = VA_DAM_N, VA_DAM_S, VA_DAM_C
    kx, ky = 2 * cx - (nx + sx) / 2, 2 * cy - (ny + sy) / 2
    return [((1 - t) ** 2 * sx + 2 * (1 - t) * t * kx + t * t * nx, (1 - t) ** 2 * sy + 2 * (1 - t) * t * ky + t * t * ny)
            for t in (i / n for i in range(n + 1))]


def va_lake_px(view):
    """湖の輪郭（画面の点）＝北の岸（ダム→上流の端）＋南の岸（上流の端→ダム）＋ダムの弧。"""
    x0 = VA_PTS["dam"][0] + 10.0
    north = [VA_DAM_N] + [(float(x), float(y - n)) for x, y, n, _s in VA_LAKE if x > x0]
    south = [(float(x), float(y + s)) for x, y, _n, s in reversed(VA_LAKE) if x > x0] + [VA_DAM_S]
    N, S = va_path(view, north, per=6), va_path(view, south, per=6)
    arc = [va_px(p, view) for p in va_dam_arc()]
    return N + S[1:] + arc[1:-1]


def va_slide_pts():
    """崩れた範囲（形は模式）＝前のふち（湖の南の岸・slide_w〜slide_e）＋後ろのふち（VA_POLY slide_back）。#100 の画素。"""
    x0, x1 = VA_PTS["slide_w"][0], VA_PTS["slide_e"][0]
    front = [(float(x), va_shore(x, "s")) for x in range(int(x0), int(x1) + 1, 8)] + [(x1, va_shore(x1, "s"))]
    return front + [tuple(map(float, q)) for q in VA_POLY["slide_back"]]


def _va_hatch(pid, bg, ln, step=7, w=3):
    """建物の面の斜めの縞（数えない形＝1軒ずつ描かない）。"""
    return (f'<defs><pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate(45)"><rect width="{step}" height="{step}" fill="{bg}"/>'
            f'<rect width="{w}" height="{step}" fill="{ln}"/></pattern></defs>')


def _va_poly(view, pts, fill, stroke=None, sw=0.0, op=None, per=4):
    return _poly(va_path(view, pts, per=per, closed=True), fill, stroke, sw, op)


def va_ground_svg(view, tod):
    """地面：標高の帯（模式＝谷底と湖からの距離）・ピアーヴェ川の河原と川・峡谷と川・湖・残る村（エルト・カッソ）。"""
    P = VA_PAL[tod]
    mpp = VA_VIEW[view]["mpp"]
    k = VA_MPX / mpp
    g = [f'<rect x="-10" y="-10" width="{W + 20}" height="{H + 20}" fill="{P["b0"]}"/>',
         _va_hatch("vaH", P["house"], P["house_ln"])]
    lake = va_lake_px(view)
    floor = va_path(view, VA_POLY["piave_floor"], per=6, closed=True)
    i = VA_LINES["vajont"].index((535, 536))
    gorge = va_path(view, VA_LINES["vajont"][i:], per=6)
    for d_m, col in zip(VA_BANDS, ("b1", "b2", "b3", "b4")):
        w = 2.0 * d_m / mpp
        for s in (floor, lake):
            g.append(f'<path d="{_pl(s)} Z" fill="{P[col]}" stroke="{P[col]}" stroke-width="{w:.1f}" stroke-linejoin="round"/>')
        g.append(f'<path d="{_pl(gorge)}" fill="none" stroke="{P[col]}" stroke-width="{w + VA_GORGE_W * k:.1f}" '
                 'stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<path d="{_pl(floor)} Z" fill="{P["floor"]}"/>')
    pv = va_path(view, VA_LINES["piave"], per=6)
    for dx, op in ((-9.0, 0.55), (8.0, 0.45)):            # 河原の筋（模式）
        g.append(f'<path d="{_pl([(x + dx * k / 2.4, y) for x, y in pv])}" fill="none" stroke="{P["floor_ln"]}" '
                 f'stroke-width="{max(1.5, 1.2 * k):.1f}" opacity="{op}"/>')
    g.append(f'<path d="{_pl(pv)}" fill="none" stroke="{P["river"]}" stroke-width="{max(2.5, 2.2 * k):.1f}" '
             'stroke-linecap="round" stroke-linejoin="round"/>')
    gw = min(VA_GORGE_PX[1], max(VA_GORGE_PX[0], VA_GORGE_W * k))
    g.append(f'<path d="{_pl(gorge)}" fill="none" stroke="{P["gorge"]}" stroke-width="{gw:.1f}" '
             'stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<path d="{_pl(gorge)}" fill="none" stroke="{P["river"]}" stroke-width="{max(1.8, min(3.5, 0.9 * k)):.1f}" '
             'stroke-linecap="round" stroke-linejoin="round"/>')
    # 湖の上流の端から先の川（#100 の東の端まで）
    g.append(f'<path d="{_pl(va_path(view, ((1480, 394), (1540, 392), (1610, 388)), per=4))}" fill="none" '
             f'stroke="{P["river"]}" stroke-width="{max(1.8, 0.9 * k):.1f}"/>')
    g.append(f'<path d="{_pl(lake)} Z" fill="{P["lake"]}" stroke="{P["shore"]}" stroke-width="{max(2.0, 0.8 * k):.1f}" '
             'stroke-linejoin="round"/>')
    for name in ("erto", "casso"):
        g.append(_va_poly(view, VA_POLY[name], "url(#vaH)", P["house_ln"], 1.5))
    return "".join(g)


def va_towns_svg(view, tod, names, mud=False):
    """建物の面（数えない形）か、消えたあとの泥の色の跡（mud）。"""
    P = VA_PAL[tod]
    if mud:
        return "".join(_va_poly(view, VA_POLY[n], VA_FIX["mud"], VA_FIX["mud_ln"], 2.0) for n in names)
    pid = "vaT" + names[0][:3]
    return _va_hatch(pid, P["house"], P["house_ln"]) + "".join(
        _va_poly(view, VA_POLY[n], f"url(#{pid})", P["house_ln"], 1.5) for n in names)


def va_block_svg(view):
    """崩れたあと：崩れた範囲（むき出しの滑った面＝明るい灰）と、北へ動いて湖を埋めた1つの塊（明るい茶）。形は模式。"""
    sl = va_slide_pts()
    blk = [(x, y - VA_SHIFT) for x, y in sl]
    k = VA_MPX / VA_VIEW[view]["mpp"]
    g = [f'<defs><pattern id="vaB" width="14" height="14" patternUnits="userSpaceOnUse">'
         f'<rect width="14" height="14" fill="{VA_FIX["block"]}"/><circle cx="4" cy="5" r="1.6" fill="{VA_FIX["block_ln"]}" '
         f'opacity="0.45"/><circle cx="11" cy="11" r="1.3" fill="{VA_FIX["block_ln"]}" opacity="0.35"/></pattern></defs>',
         _poly(va_path(view, sl, per=4, closed=True), VA_PAL["night"]["scar"], "#4b4740", max(1.5, 0.5 * k)),
         _poly(va_path(view, blk, per=4, closed=True), "url(#vaB)", VA_FIX["block_ln"], max(2.0, 0.7 * k))]
    return "".join(g)


def va_slide_svg(view):
    """崩れた範囲（崩れる前の斜面の上・形は模式）＝薄い琥珀の面と太い縁。"""
    k = VA_MPX / VA_VIEW[view]["mpp"]
    pts = va_path(view, va_slide_pts(), per=4, closed=True)
    return (_poly(pts, C["mark"], None, 0.0, 0.30) + _poly(pts, "none", "#10161b", max(6.0, 1.6 * k), 0.55)
            + _poly(pts, "none", C["mark"], max(3.0, 0.9 * k)))


def va_dam_svg(view):
    """ダムの弧（明るい固定の色＝夜の地と ΔE 25 以上。太さは天端の厚さより太い＝見える太さの模式）。"""
    arc = [va_px(p, view) for p in va_dam_arc(16)]
    w = max(5.0, 30.0 / VA_VIEW[view]["mpp"])
    return (f'<path d="{_pl(arc)}" fill="none" stroke="{VA_FIX["dam_ln"]}" stroke-width="{w + 4:.1f}" stroke-linecap="round"/>'
            f'<path d="{_pl(arc)}" fill="none" stroke="{VA_FIX["dam"]}" stroke-width="{w:.1f}" stroke-linecap="round"/>')


def _va_band(pts, w, col, op, edge=None):
    e = (f'<path d="{_pl(pts)}" fill="none" stroke="{edge}" stroke-width="{w + 5:.1f}" stroke-opacity="{op * 0.8:.2f}" '
         'stroke-linecap="round" stroke-linejoin="round"/>') if edge else ""
    return e + (f'<path d="{_pl(pts)}" fill="none" stroke="{col}" stroke-width="{w:.1f}" stroke-opacity="{op}" '
                'stroke-linecap="round" stroke-linejoin="round"/>')


def va_wave_w_svg(view):
    """西へダムを越えて峡谷を下る水（帯・高さは描かない）。"""
    k = VA_MPX / VA_VIEW[view]["mpp"]
    pts = va_path(view, VA_WAVE_W, per=6)
    return _va_band(pts, VA_WAVE_W_W * k, VA_FIX["flood"], 0.88, edge=VA_FIX["foam"])


def va_flood_svg(view, half):
    """ピアーヴェ川の谷へ広がる水（north＝境より北・south＝南）。平らな面＝盛り上がりは描かない。"""
    pts = va_path(view, VA_FLOOD, per=4, closed=True)
    ys = va_px((0.0, VA_FLOOD_SPLIT), view)[1]
    cid = f"vaF{half}"
    clip = (f'<defs><clipPath id="{cid}"><rect x="-10" y="{"-10" if half == "n" else f"{ys:.1f}"}" width="{W + 20}" '
            f'height="{(ys + 10) if half == "n" else (H + 10 - ys):.1f}"/></clipPath></defs>')
    return clip + f'<g clip-path="url(#{cid})">' + _poly(pts, VA_FIX["flood"], VA_FIX["foam"], 3.0, 0.86) + "</g>"


def va_wave_e_svg(view):
    """東へ向かった波（崩れた塊の東の端から湖の上流の端まで）＝湖の面を泡の色で覆う。岸を少し越える（上流の岸で25〜90m）。"""
    lake = va_lake_px(view)
    xs = va_px((VA_EAST_X0, 0.0), view)[0]
    k = VA_MPX / VA_VIEW[view]["mpp"]
    return (f'<defs><clipPath id="vaE"><rect x="{xs:.1f}" y="-10" width="{W + 20 - xs:.1f}" height="{H + 20}"/></clipPath></defs>'
            f'<g clip-path="url(#vaE)"><path d="{_pl(lake)} Z" fill="{VA_FIX["foam"]}" fill-opacity="0.82" '
            f'stroke="{VA_FIX["foam"]}" stroke-width="{max(4.0, 3.0 * k):.1f}" stroke-opacity="0.82" stroke-linejoin="round"/></g>')


def va_wave_e_path(view):
    pts = [(VA_EAST_X0 + 4.0, va_shore(VA_EAST_X0 + 4.0, "n") / 2 + va_shore(VA_EAST_X0 + 4.0, "s") / 2)]
    pts += [(float(x), y + (s - n) / 2.0) for x, y, n, s in VA_LAKE if x > VA_EAST_X0 + 10]
    return va_path(view, pts, per=6)


def va_tunnel_svg(view):
    """迂回トンネル（北の岸の岩の中＝点線）。"""
    pts = va_path(view, VA_LINES["tunnel"], per=6)
    return (f'<path d="{_pl(pts)}" fill="none" stroke="#10161b" stroke-opacity="0.55" stroke-width="9" stroke-linecap="round" '
            'stroke-linejoin="round"/>'
            f'<path d="{_pl(pts)}" fill="none" stroke="{C["mark"]}" stroke-width="5" stroke-dasharray="3 11" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def va_tunnel_ends_svg(view):
    g = []
    for p in (VA_PTS["tunnel_in"], VA_PTS["tunnel_out"]):
        x, y = va_px(p, view)
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#10161b" fill-opacity="0.55" stroke="{C["mark"]}" '
                 'stroke-width="4"/>')
    return "".join(g)


def va_split_svg(view):
    """会社の説明（想定）：崩れた土砂で湖が2つに分かれる（湖を横切る帯＝模式）。"""
    x0, x1 = VA_SPLIT_X
    top = [(float(x), va_shore(x, "n") - 6.0) for x in range(int(x0), int(x1) + 1, 15)]
    bot = [(float(x), va_shore(x, "s") + 6.0) for x in range(int(x1), int(x0) - 1, -15)]
    pts = va_path(view, top + bot, per=3, closed=True)
    return (_poly(pts, VA_FIX["split"], None, 0.0, 0.92)
            + f'<path d="{_pl(pts)} Z" fill="none" stroke="#2b2117" stroke-width="2.5" stroke-dasharray="10 7"/>')


def va_flow_path(view):
    """想定の水の通り道＝分かれた上流の湖 → トンネルの入口 → トンネル → 出口（ダムのそば）。"""
    lead = ((905.0, va_shore(905.0, "n") / 2 + va_shore(905.0, "s") / 2), (965.0, 528.0))
    return va_path(view, lead + VA_LINES["tunnel"][::-1], per=6)


def va_flow_svg(view):
    pts = va_flow_path(view)
    g = [_va_band(pts, 7.0, VA_FIX["flow"], 0.95, edge="#10161b")]
    n = len(pts)
    for j in range(3, n - 1, max(4, n // 7)):                # 流れる向きの山形（模式）
        (x0, y0), (x1, y1) = pts[j - 1], pts[j + 1]
        a = math.atan2(y1 - y0, x1 - x0)
        x, y = pts[j]
        L = 14.0
        p1 = (x - L * math.cos(a) + 0.7 * L * math.sin(a), y - L * math.sin(a) - 0.7 * L * math.cos(a))
        p2 = (x - L * math.cos(a) - 0.7 * L * math.sin(a), y - L * math.sin(a) + 0.7 * L * math.cos(a))
        g.append(f'<path d="M {p1[0]:.1f} {p1[1]:.1f} L {x:.1f} {y:.1f} L {p2[0]:.1f} {p2[1]:.1f}" fill="none" '
                 f'stroke="#10161b" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(g)


def va_road_px(view):
    return va_path(view, VA_LINES["road"], per=6)


def va_road_svg(view):
    """道（形は模式）＝エルトから北の岸ぞい・ダムの北のたもと・峡谷ぞいにロンガローネへ。カッソへの枝も。"""
    g = []
    for pts in (va_road_px(view), va_path(view, VA_LINES["road_casso"], per=6)):
        g.append(f'<path d="{_pl(pts)}" fill="none" stroke="{VA_PAL["night"]["road_ln"]}" stroke-width="7" '
                 'stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<path d="{_pl(pts)}" fill="none" stroke="{VA_PAL["night"]["road"]}" stroke-width="3.5" '
                 'stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(g)


def va_road_low_svg(view):
    """道の標高730mより低い区間（上の入口〜下の入口）。"""
    r = VA_LINES["road"]
    i, j = r.index((560, 508)), r.index((345, 532))
    pts = va_path(view, r[i:j + 1], per=6)
    return _va_band(pts, 7.0, C["mark"], 1.0, edge="#10161b")


def va_gates_svg(view):
    """道の入口2か所の印（上＝実線の輪〈作業員2人がふさいだ〉・下＝点線の輪〈ふさいだか、ふさごうとしていた〉）。人は描かない。"""
    g = []
    for p, dash in ((VA_PTS["road_up"], None), (VA_PTS["road_down"], "5 5")):
        x, y = va_px(p, view)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#10161b" fill-opacity="0.45" stroke="#10161b" '
                 f'stroke-width="8"{da}/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="none" stroke="#f3f6f8" stroke-width="4"{da}/>'
                 f'<path d="M {x - 8:.1f} {y:.1f} L {x + 8:.1f} {y:.1f}" stroke="#f3f6f8" stroke-width="4"{da}/>')
    return "".join(g)


def va_marks_svg(view):
    """北の岸の印2か所（930m＝波が最も高く届いた所）。"""
    g = []
    for p in (VA_PTS["north_dam"], VA_PTS["north_1100"]):
        x, y = va_px(p, view)
        g.append(f'<path d="M {x:.1f} {y - 15:.1f} L {x + 13:.1f} {y + 9:.1f} L {x - 13:.1f} {y + 9:.1f} Z" fill="{C["mark"]}" '
                 'stroke="#10161b" stroke-width="3.5" stroke-linejoin="round"/>')
    return "".join(g)


def va_eye_svg(x, y, look, col):
    """目の印（見ている向きの矢印つき）。look＝画面の向き（度・東が0・南が90・西が180）。"""
    r = math.radians(look)
    ux, uy = math.cos(r), math.sin(r)
    t0, t1 = (x + ux * 26, y + uy * 26), (x + ux * 66, y + uy * 66)
    hx, hy = t1[0] - ux * 14, t1[1] - uy * 14
    h1, h2 = (hx - uy * 9, hy + ux * 9), (hx + uy * 9, hy - ux * 9)
    return (f'<path d="M {t0[0]:.1f} {t0[1]:.1f} L {t1[0]:.1f} {t1[1]:.1f}" stroke="#10161b" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M {t0[0]:.1f} {t0[1]:.1f} L {hx:.1f} {hy:.1f}" stroke="{col}" stroke-width="4"/>'
            f'<path d="M {t1[0]:.1f} {t1[1]:.1f} L {h1[0]:.1f} {h1[1]:.1f} L {h2[0]:.1f} {h2[1]:.1f} Z" fill="{col}" '
            'stroke="#10161b" stroke-width="2"/>'
            f'<path d="M {x - 21:.1f} {y:.1f} Q {x:.1f} {y - 17:.1f} {x + 21:.1f} {y:.1f} Q {x:.1f} {y + 17:.1f} {x - 21:.1f} {y:.1f} Z" '
            'fill="#f3f6f8" stroke="#10161b" stroke-width="3"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{col}" stroke="#10161b" stroke-width="2"/>')


def _va_text(x, y, t, col="#f3f6f8", size=28, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Noto" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'stroke="#10161b" stroke-width="6" stroke-linejoin="round" paint-order="stroke fill">{F.esc(t)}</text>')


def va_cut_svg(view, which, strong=True, label=None):
    """断面の切り口の線（B＝青緑・C＝琥珀の破線）と目の印。D は目の印だけ（正面から見た斜面＝北の岸から南を向いて）。"""
    c = VA_CUT[which]
    g = []
    if c["a"]:
        (x0, y0), (x1, y1) = va_px(c["a"], view), va_px(c["b"], view)
        w = 6.0 if strong else 3.0
        g.append(f'<path d="M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}" stroke="#10161b" stroke-opacity="0.55" '
                 f'stroke-width="{w + 5:.1f}" stroke-linecap="round"/>'
                 f'<path d="M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}" stroke="{c["col"]}" stroke-width="{w:.1f}" '
                 'stroke-dasharray="16 11" stroke-linecap="round"/>')
    if strong or not c["a"]:
        ex, ey = va_px(c["eye"], view)
        g.append(va_eye_svg(ex, ey, c["look"], c["col"]))
        if label:
            g.append(_va_text(ex + 30, ey - 30, label, col=c["col"] if c["a"] else "#f3f6f8"))
    return "".join(g)


def va_switch_svg(text=VA_SWITCH):
    w = 70 + 46 * len(text)
    x = 960 - w / 2
    return (f'<rect x="{x:.0f}" y="40" width="{w:.0f}" height="66" rx="10" fill="{CHIP_BG}" fill-opacity="0.72" '
            f'stroke="{CHIP_FG}" stroke-width="2.5"/>'
            f'<text x="960" y="87" font-family="Noto" font-size="44" fill="{CHIP_FG}" text-anchor="middle">{F.esc(text)}</text>')


def _va_timeline(start, states, steps):
    """VA の鍵（段の中の順番つき）。水がダムを越える → 谷へ広がる → 建物の面が消える、の順（冒頭 c102・c823）。"""
    T = VA_T

    def k0(**kw):
        return [dict(stage=0, delay=0.0, **kw)]
    s0 = start
    K = dict(dawn=k0(a=float(s0["tod"] == "dawn")), slide=k0(a=float(s0["slide"] == "on")),
             block=k0(a=float(s0["block"] == "on")), towns=k0(a=float(s0["towns"] == "on")),
             mud=k0(a=float(s0["towns"] == "mud")), shore=k0(a=float(s0["shore"] == "on")),
             shore_mud=k0(a=float(s0["shore"] == "mud")), tunnel_go=k0(u=float(s0["tunnel"] == "on")),
             tunnel_a=k0(a=1.0), ends=k0(a=float(s0["tunnel"] == "on")), split=k0(a=float(s0["split"] != "off")),
             flow_go=k0(u=float(s0["split"] == "flow")), flow_a=k0(a=1.0), road_go=k0(u=float(s0["road"] != "off")),
             road_a=k0(a=1.0), low=k0(a=float(s0["road"] == "low")), gates=k0(a=float(s0["gates"] == "on")),
             marks=k0(a=float(s0["marks"] == "on")),
             wave_e_go=k0(u=float(s0["wave_e"] != "off")), wave_e_a=k0(a=float(s0["wave_e"] == "on")),
             wave_w_go=k0(u=float(s0["wave_w"] != "off")), wave_w_a=k0(a=float(s0["wave_w"] == "on")),
             flood_go=k0(u=float(s0["flood"] != "off")), flood_a=k0(a=float(s0["flood"] == "on")),
             nxtB=k0(a=float(s0["nxt"] == "B")), nxtC=k0(a=float(s0["nxt"] == "C")))
    # 頭だけの合図：前の図の切り口の線（はじめ太く・1.5秒で細く）と切り替えの字（1.2秒で消える）
    K["prev"] = [dict(stage=0, delay=0.0, a=1.0), dict(stage=0, delay=T["prev_hold"], dur=T["prev_fade"], a=0.0)]
    K["prev_thin"] = [dict(stage=0, delay=0.0, a=0.0), dict(stage=0, delay=T["prev_hold"], dur=T["prev_fade"], a=T["prev_thin"])]
    K["switch"] = [dict(stage=0, delay=0.0, a=1.0), dict(stage=0, delay=T["switch_hold"], dur=T["switch_fade"], a=0.0)]
    prev = start
    for i, (st, sp) in enumerate(zip(states, steps)):
        dl = float(sp.get("delay", KEY_DELAY))

        def ch(f):
            return prev[f] != st[f]
        ww = ch("wave_w") and st["wave_w"] == "on"
        wdur = float(sp.get("dur", T["wave"])) if ww and not ch("flood") else T["wave"]   # 谷へ広がらない段（c815）は dur で
        if ch("wave_w"):
            if st["wave_w"] == "on":
                K["wave_w_go"].append(dict(stage=i, delay=dl, dur=wdur, u=1.0))
                K["wave_w_a"].append(dict(stage=i, delay=dl, dur=0.12, a=1.0))
            elif st["wave_w"] == "recede":
                K["wave_w_a"].append(dict(stage=i, delay=dl, dur=T["recede"], a=0.0))
        fl0 = dl + (T["flood_lag"] / T["wave"] * wdur if ww else 0.0)     # 水が峡谷の出口に着いてから谷へ広がる
        fl_on = ch("flood") and st["flood"] == "on"
        if ch("flood"):
            if st["flood"] == "on":
                K["flood_go"].append(dict(stage=i, delay=fl0, dur=T["flood"], u=1.0))
                K["flood_a"].append(dict(stage=i, delay=fl0, dur=0.12, a=1.0))
            elif st["flood"] == "recede":
                K["flood_a"].append(dict(stage=i, delay=dl, dur=T["recede"], a=0.0))
        if ch("towns"):
            t_t = fl0 + T["towns_lag"] if fl_on else dl
            if prev["towns"] == "on" and st["towns"] in ("gone", "mud"):
                K["towns"].append(dict(stage=i, delay=t_t, dur=T["towns"], a=0.0))
            if st["towns"] == "mud":
                K["mud"].append(dict(stage=i, delay=dl, dur=T["mud"], a=1.0))
            if st["towns"] == "on":
                K["towns"].append(dict(stage=i, delay=dl, dur=T["towns"], a=1.0))
                K["mud"].append(dict(stage=i, delay=dl, dur=T["mud"], a=0.0))
        if ch("wave_e"):
            if st["wave_e"] == "on":
                K["wave_e_go"].append(dict(stage=i, delay=dl, dur=float(sp.get("dur", T["wave_e"])), u=1.0))
                K["wave_e_a"].append(dict(stage=i, delay=dl, dur=0.12, a=1.0))
            elif st["wave_e"] == "recede":
                K["wave_e_a"].append(dict(stage=i, delay=dl, dur=T["recede"], a=0.0))
        if ch("shore"):
            if prev["shore"] == "on" and st["shore"] in ("gone", "mud"):
                K["shore"].append(dict(stage=i, delay=dl, dur=T["shore"], a=0.0))
            if st["shore"] == "mud":
                K["shore_mud"].append(dict(stage=i, delay=dl + 0.3, dur=T["mud"], a=1.0))
        for f in ("slide", "block", "gates", "marks"):
            if ch(f):
                K[f].append(dict(stage=i, delay=dl, dur=T[f], a=float(st[f] == "on")))
        if ch("tunnel") and st["tunnel"] == "on":
            K["tunnel_go"].append(dict(stage=i, delay=dl, dur=float(sp.get("dur", T["tunnel"])), u=1.0))
            K["ends"].append(dict(stage=i, delay=dl + float(sp.get("dur", T["tunnel"])), dur=T["ends"], a=1.0))
        if ch("split"):
            late = 0.0
            if prev["split"] == "off":
                K["split"].append(dict(stage=i, delay=dl, dur=T["split"], a=1.0))
                late = T["split"]
            if st["split"] == "flow":
                K["flow_go"].append(dict(stage=i, delay=dl + late, dur=T["flow"], u=1.0))
        if ch("road"):
            late = 0.0
            if prev["road"] == "off":
                K["road_go"].append(dict(stage=i, delay=dl, dur=T["road"], u=1.0))
                late = T["road"]
            if st["road"] == "low":
                K["low"].append(dict(stage=i, delay=dl + late, dur=T["low"], a=1.0))
        if ch("tod") and st["tod"] == "dawn":
            K["dawn"].append(dict(stage=i, delay=dl, dur=float(sp.get("dur", T["dawn"])), a=1.0))
        if ch("nxt"):
            for w in ("B", "C"):
                K["nxt" + w].append(dict(stage=i, delay=dl, dur=T["line"], a=float(st["nxt"] == w)))
        prev = st
    return K


def _scene_VA(start, states, steps):
    """VA＝上から見た谷（北が上）。見え方 view＝wide（谷の全体）／near（ダムと崩れた斜面）／west（峡谷の出口とピアーヴェ川の谷）。"""
    view = start["view"]
    allst = [start] + states
    if any(st["view"] != view for st in states):
        raise ValueError("illu VA：見え方 view は場面の頭（start）で1つだけ（地面の縮尺を焼き込む）")
    t0 = start["tod"]
    if t0 == "dawn" or any(st["tod"] not in (t0, "dawn") or (t0 == "day" and st["tod"] != "day") for st in states):
        raise ValueError("illu VA：tod は頭で day か night・段で変えてよいのは night → dawn（夜明け＝c823 の2行目）だけ")
    if any(st["prev"] != start["prev"] or st["switch"] != start["switch"] for st in states):
        raise ValueError("illu VA：prev（前の図の切り口の線）と switch（切り替えの字）は頭（start）だけ＝合図")
    if start["prev"] == start["nxt"] != "off":
        raise ValueError("illu VA：前の図の線と次の図の線が同じ")

    def used(f, v=None):
        return any((st[f] != "off") if v is None else (st[f] == v) for st in allst)
    K = _va_timeline(start, states, steps)
    A1 = [dict(stage=0, delay=0.0, a=1.0)]
    k = VA_MPX / VA_VIEW[view]["mpp"]
    R = VA_REC
    parts = [_part("ground", va_ground_svg(view, t0), R["ground"])]
    if used("tod", "dawn"):
        parts.append(_part("dawn", va_ground_svg(view, "dawn"), R["dawn"], keys=K["dawn"]))
    if used("slide"):
        parts.append(_part("slide", va_slide_svg(view), R["slide"], keys=K["slide"]))
    if used("block"):
        parts.append(dict(_part("block", va_block_svg(view), R["block"], keys=K["block"]), obj=dict(block=1)))
    tn = ("longarone", "pirago", "fornace")
    parts.append(_part("towns", va_towns_svg(view, t0, tn), R["towns"], keys=K["towns"]))
    if used("towns", "mud"):
        parts.append(_part("mud", va_towns_svg(view, t0, tn, mud=True), R["towns"], keys=K["mud"]))
    sn = ("pineda", "smartino")
    parts.append(_part("shore", va_towns_svg(view, t0, sn), R["shore"], keys=K["shore"]))
    if used("shore", "mud"):
        parts.append(_part("shore_mud", va_towns_svg(view, t0, sn, mud=True), R["shore"], keys=K["shore_mud"]))
    if used("road"):
        rp = va_road_px(view)
        parts.append(dict(_part("road", va_road_svg(view), R["road"], keys=K["road_a"]), kind="draw",
                          path=[list(q) for q in rp], go=K["road_go"], reveal=60))
        if used("road", "low"):
            parts.append(_part("road_low", va_road_low_svg(view), R["road"], keys=K["low"]))
    if used("gates"):
        parts.append(dict(_part("gates", va_gates_svg(view), R["gates"], keys=K["gates"]), obj=dict(road_gates=2)))
    if used("tunnel"):
        tp = va_path(view, VA_LINES["tunnel"], per=6)
        parts.append(dict(_part("tunnel", va_tunnel_svg(view), R["tunnel"], keys=K["tunnel_a"]), kind="draw",
                          path=[list(q) for q in tp], go=K["tunnel_go"], reveal=40, obj=dict(tunnel=1)))
        parts.append(_part("tunnel_ends", va_tunnel_ends_svg(view), R["tunnel"], keys=K["ends"]))
    if used("split"):
        parts.append(_part("split", va_split_svg(view), R["split"], keys=K["split"]))
        if used("split", "flow"):
            fp = va_flow_path(view)
            parts.append(dict(_part("flow", va_flow_svg(view), R["split"], keys=K["flow_a"]), kind="draw",
                              path=[list(q) for q in fp], go=K["flow_go"], reveal=44))
    if used("marks"):
        parts.append(dict(_part("marks", va_marks_svg(view), R["marks"], keys=K["marks"]), obj=dict(north_marks=2)))
    if used("wave_e"):
        ep = va_wave_e_path(view)
        parts.append(dict(_part("wave_e", va_wave_e_svg(view), R["wave_e"], keys=K["wave_e_a"]), kind="draw",
                          path=[list(q) for q in ep], go=K["wave_e_go"], reveal=int(150 * k)))
    if used("wave_w"):
        wp = va_path(view, VA_WAVE_W, per=6)
        parts.append(dict(_part("wave_w", va_wave_w_svg(view), R["wave_w"], keys=K["wave_w_a"]), kind="draw",
                          path=[list(q) for q in wp], go=K["wave_w_go"], reveal=int(VA_WAVE_W_W * k + 30)))
    if used("flood"):
        for half in ("n", "s"):
            gp = va_path(view, VA_FLOOD_GO[half], per=6)
            parts.append(dict(_part("flood_" + half, va_flood_svg(view, half), R["flood"], keys=K["flood_a"]),
                              kind="draw", path=[list(q) for q in gp], go=K["flood_go"], reveal=int(300 * k)))
    parts.append(dict(_part("dam", va_dam_svg(view), R["dam"]), obj=dict(dam=1)))
    # 合図の部品（切り口の線・目の印・切り替えの字＝見る向きの合図・ルール §5b-80）は記録の物でない＝出典を持たない
    #   ＝`signal=True`（門番 ① は rec を求めない・③ の数にも入らない＝obj を持たない）
    for w in ("B", "C"):
        if used("nxt", w):
            parts.append(dict(_part("nxt" + w, va_cut_svg(view, w, strong=True), "", keys=K["nxt" + w]), signal=True))
    if start["prev"] != "off":
        lab = "さっきの断面" if VA_CUT[start["prev"]]["a"] else "さっきの見る位置"
        parts.append(dict(_part("prev", va_cut_svg(view, start["prev"], strong=True, label=lab), "", keys=K["prev"]),
                          signal=True))
        if VA_CUT[start["prev"]]["a"]:
            parts.append(dict(_part("prev_thin", va_cut_svg(view, start["prev"], strong=False), "", keys=K["prev_thin"]),
                              signal=True))
    if start["switch"] == "on":
        parts.append(dict(_part("switch", va_switch_svg(), "", keys=K["switch"]), signal=True))
    return parts


def _va_anchors(view):
    P = lambda p: va_px(p, view)  # noqa: E731
    a = {k: P(v) for k, v in VA_PTS.items()}
    a.update(lake=P((900.0, 560.0)), gorge=P((440.0, 545.0)), piave=P((228.0, 690.0)), piave_n=P((214.0, 455.0)),
             mark1=P(VA_PTS["north_dam"]),
             mark2=P(VA_PTS["north_1100"]), slide=P((715.0, 690.0)), road_low=P((450.0, 528.0)),
             upstream=P((1400.0, 381.0)), split=P((735.0, 560.0)), block=P((710.0, 540.0)), center=(960.0, VA_Y0))
    return a


def _va_note(st0, states):
    """左下の出典のあとに添える断り（16本目 VA）。"""
    allst = [st0] + list(states)

    def u(f):
        return any(st[f] != "off" for st in allst)
    note = ["谷の形は1934年の地形図から・湖の形は概略"]
    if u("wave_w") or u("flood") or u("wave_e"):
        note.append("動きは縮めてある")
    if u("road"):
        note.append("道は模式")
    if u("slide") or u("block"):
        note.append("崩れた範囲は模式")
    if u("split"):
        note.append("土砂の帯は模式")
    return "・".join(note)


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


ASSUME_FG = "#f2c14e"


def overlay_svg(view, src, assume=""):
    """左上の「再現イラスト」の札（と見る向き）・左下の出典（ルール §5b-74③・§5b-80）。check_illu ④ が同じ関数で見る。
    🆕 16本目 ⑤b-2：assume＝想定の札（「会社の説明（想定）」「模型の想定」＝起きた事ではない絵・映像方針 16本目 §2③）を
       見る向きの下に（琥珀の枠）"""
    x, y, w, h = CHIP
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{CHIP_BG}" fill-opacity="0.62" '
         f'stroke="{CHIP_FG}" stroke-width="2"/>',
         f'<text x="{x + w / 2:.0f}" y="{y + 35}" font-family="Noto" font-size="28" fill="{CHIP_FG}" '
         f'text-anchor="middle">再現イラスト</text>']
    if view:
        g.append(f'<text x="{x + 4}" y="{y + h + 34}" font-family="Noto" font-size="24" fill="#e3eaee" '
                 f'stroke="#10161b" stroke-width="5" stroke-linejoin="round" paint-order="stroke fill">{F.esc(view)}</text>')
    if assume:
        ay = y + h + (54 if view else 14)
        aw = 40 + 28 * len(assume)
        g.append(f'<rect x="{x}" y="{ay}" width="{aw}" height="46" rx="6" fill="{CHIP_BG}" fill-opacity="0.72" '
                 f'stroke="{ASSUME_FG}" stroke-width="2.5"/>'
                 f'<text x="{x + aw / 2:.0f}" y="{ay + 33}" font-family="Noto" font-size="27" fill="{ASSUME_FG}" '
                 f'text-anchor="middle">{F.esc(assume)}</text>')
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
    "A": dict(heel=0.0, wake="on", boxes="off", bridge="off", cam=1.0),
    "D": dict(view="ship", heel=61.2, mark="off", crowd="off", cam=1.0, bx=SEA["x0"], run="off", far="off", spk="off",
              binoc="off", rboat="off", cg="off"),
    "B": dict(view="corridor", heel=0.0, crowd="off", cam=1.0),
    "C": dict(view="console", heel=0.0, crew=0, cam=1.0),
    "E": dict(sel="off", cam=1.0),
    # 15本目 ⑤b-2：RA 上から見たステッド空港／RB 空の中の事故機／RD ピットの事故機（上の「15本目」の節）
    "RA": dict(view="near", gg="off", path="off", trace="off", x="off", box="off", laps="off", seg67="off", ring8="off",
               piece="off", fuel="off", course="on", cam=1.0),
    "RB": dict(view="side", ground="on", pitch=0.0, roll=0.0, ail="off", cam=1.0),
    "RD": dict(view="tail", mark="off", cam=1.0),
    # 15本目 ⑤b-3：RC ボックス席とピット（地上から）。pan＝カメラの中心を横へ（画素・cam の寄りのまま首を振る）
    "RC": dict(view="pits", crowd="off", fuel="off", cam=1.0, pan=0.0),
    # 16本目 ⑤b-2：VA 上から見た谷（上の「16本目」の節）。tod＝day／night（段で night→dawn だけ）・block＝崩れたあとの塊・
    #   slide＝崩れた範囲・towns／shore＝建物の面（on／gone／mud）・tunnel・split（off／on／flow）・road（off／on／low）・gates・
    #   marks・wave_w／flood／wave_e（off／on／recede）・prev（頭だけ：B／C／D）・nxt（B／C）・switch（頭だけ）
    "VA": dict(view="wide", tod="night", block="off", slide="off", towns="on", shore="on", tunnel="off", split="off",
               road="off", gates="off", marks="off", wave_w="off", flood="off", wave_e="off", prev="off", nxt="off",
               switch="off", cam=1.0),
}
ONOFF = ("off", "on")
CHOICES = dict(wake=("on", "off"), boxes=("off", "on", "fall", "fell"), mark=ONOFF, crowd=ONOFF, bridge=ONOFF, run=ONOFF,
               far=ONOFF, spk=ONOFF, binoc=ONOFF, rboat=ONOFF, cg=ONOFF, sel=ONOFF,
               gg=("off", "p7", "p8", "gone"), path=ONOFF, trace=ONOFF, x=ONOFF, box=ONOFF, laps=ONOFF, seg67=ONOFF,
               ring8=ONOFF, piece=ONOFF, fuel=ONOFF, course=ONOFF, ground=ONOFF, ail=("off", "right"),
               # 16本目 ⑤b-2：VA
               tod=("day", "night", "dawn"), block=ONOFF, slide=ONOFF, towns=("on", "gone", "mud"),
               shore=("on", "gone", "mud"), tunnel=ONOFF, split=("off", "on", "flow"), road=("off", "on", "low"),
               gates=ONOFF, marks=ONOFF, wave_w=("off", "on", "recede"), flood=("off", "on", "recede"),
               wave_e=("off", "on", "recede"), prev=("off", "B", "C", "D"), nxt=("off", "B", "C"), switch=ONOFF)
VIEWS = dict(B=("corridor", "cabin", "desk"), C=("helm", "console", "room"), D=("ship", "sea", "far", "heli", "rail"),
             RA=tuple(RA_VIEW), RB=("side", "rear"), RD=("tail",), RC=tuple(RC_VIEW), VA=tuple(VA_VIEW))
# 変える段には rec が要る（記録の事実を描く欄）。⑤b-3 で置き場 C・D・E の欄を足した（位置 bx とカメラ cam は要らない）
#   15本目 ⑤b-2：RA の印・線・×・輪、RB の機首の上げ・傾き・補助翼（コースの破線 course と地面 ground は要らない）
#   16本目 ⑤b-2：VA の時刻（夜明け）・塊・崩れた範囲・建物の面・トンネル・想定の帯・道・入口・印・水（合図の prev・nxt・switch は要らない）
REC_FIELDS = ("heel", "wake", "boxes", "crowd", "mark", "bridge", "run", "far", "binoc", "rboat", "cg", "crew", "sel",
              "gg", "path", "trace", "x", "box", "laps", "seg67", "ring8", "piece", "fuel", "pitch", "roll", "ail",
              "tod", "block", "slide", "towns", "shore", "tunnel", "split", "road", "gates", "marks", "wave_w", "flood",
              "wave_e")
# 段ごとの出来事（引き継がない・数で書く＝画面の文字の門番が文字として読まない）。pylon＝RB でパイロンが1本流れる
EVENTS = ("rings", "board", "rings_in", "asks", "walkie", "glow", "pylon")
VIEW = dict(A="船首の側から見た図", D="船首の側から見た図", B="船の中", C="操舵室の中", E="管制センターの中",
            RD="ピットの事故機（横から）")
# 左下の出典のあとに添える断り（15本目）。16本目 VA は場面の中身で変わる（関数＝_va_note）
NOTE = dict(RA="配置は概略・機体は拡大・点線は模式", RC="柵・幕・車の形と並びは模式・配置は概略", VA=_va_note)
D_VIEW = dict(ship="船首の側から見た図", heli="船首の側から見た図", sea="123艇を横から見た図", far="123艇から見た図",
              rail="3階の左舷を横から見た図")
ROLES = ("crew", "coast_guard", "control")                # 型紙（数えられる影）で置ける役割
CAM_C = dict(A=(820.0, 420.0), D=(990.0, 560.0), B=CB, E=(905.0, 420.0))
# 音の輪の種類：out＝広がって外へ／inn＝外から集まる（大→小）／ask＝問いかけの印が出る／glow＝灯のまわりの光
RING_KIND = dict(out=dict(s0=0.5, s1=2.2, gap=0.8, dur=1.4), inn=dict(s0=2.4, s1=0.55, gap=0.8, dur=1.3),
                 ask=dict(s0=0.72, s1=1.12, gap=1.15, dur=1.05), glow=dict(s0=0.8, s1=2.0, gap=0.75, dur=1.2))


def _check_state(place, st):
    for k, v in st.items():
        if k not in FIELDS[place]:
            raise ValueError(f"illu {place}：知らない欄 {k!r}（使えるのは {tuple(FIELDS[place])}）")
        if k == "view":
            if v not in VIEWS.get(place, ()):
                raise ValueError(f"illu {place}：view={v!r} は知らない見え方（{VIEWS.get(place)}）")
        elif k in CHOICES and v not in CHOICES[k]:
            raise ValueError(f"illu {place}：{k}={v!r} は知らない状態（{CHOICES[k]}）")
        if k == "cam" and float(v) < 1.0:
            raise ValueError("illu：cam（寄り）は 1.0 以上（引きすぎると画面の端が空く）")
        if k == "pan" and not -880.0 <= float(v) <= 880.0:
            raise ValueError("illu：pan（カメラの中心の横のずれ）は ±880 画素まで（中心が画面の外へ出ると端が空く）")


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


def _pulse_part(pid, svg, rec, c, states, steps, key, kind):
    """段ごとの出来事 key（数＝何回）を、音の輪の型（RING_KIND）の部品に。起きない場面は部品を作らない。"""
    pulse = [dict(stage=i, delay=float(sp.get("ring_delay", 0.3)), n=int(sp[key]), **RING_KIND[kind])
             for i, (st, sp) in enumerate(zip(states, steps)) if sp.get(key)]
    return [dict(_part(pid, svg, rec, c), kind="ring", pulse=pulse)] if pulse else []


def bridge_mark_svg(piv):
    """操舵室（5階・船橋の真ん中）の印（A・c702）。窓の中の人は描かない（外から見えない）。"""
    return _mrect(-7.7, BR_DECK - 0.35, 7.7, ROOF + 0.55, piv, "none", C["mark"], 5, rx=6)


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
    if any(st["bridge"] == "on" for st in [start] + states):
        # ⑤b-3（c702）：操舵室に集まった＝場所だけを外から示す（中の人数は 8時52〜55分に9人＝判決 p11 の8人＋機関長
        #   〈海審 p1053・p1055〉。外からは中が見えない＝人を描かない）
        parts.append(_part("bridge", bridge_mark_svg(piv), "判決 p11（8時52分ごろ 船長と甲板部が操舵室に集まった）", piv,
                           _keys(start, states, steps, lambda st: dict(rot=float(st["heel"]), **_vis(st["bridge"] == "on")))))
    parts += [_part("front_sea", front_sea_svg(), "判決 p16"),
              _part("wake", wake_svg(piv), "判決 p11（8時52分に止まる）", piv,
                    _keys(start, states, steps, lambda st: _vis(st["wake"] == "on")))]
    return parts


def _scene_D(start, states, steps):
    """置き場 D は見え方 view で分ける（⑤b-3）。見え方は場面の頭で1つ。乗客の群れは ship だけ（窓の奥＝門番 ②）。"""
    view = start["view"]
    if any(st["view"] != view for st in states):
        raise ValueError("illu D：見え方 view は場面の頭（start）で1つだけ")
    if view != "ship" and any(st["crowd"] == "on" for st in [start] + states):
        raise ValueError(f"illu D：乗客の群れ（crowd）は view=ship の窓の奥だけ（{view} には描かない）")
    return {"ship": _scene_D_ship, "sea": _scene_D_sea, "far": _scene_D_far, "heli": _scene_D_heli,
            "rail": _scene_D_rail}[view](start, states, steps)


def _fixed_heel(start, states, what):
    deg = float(start["heel"])
    if any(float(st["heel"]) != deg for st in states):
        raise ValueError(f"illu {what}：傾きは場面の頭（start）で1つだけ（SVG で焼き込む）")
    return deg


def _scene_D_sea(start, states, steps):
    """海を進む123艇（c901・c902）・遠くのセウォル号と123艇の放送の設備（c919）。横から見た図。"""
    x0, wy, s = SEA["x0"], SEA["water"], SEA["s"]
    allst = [start] + states
    run = any(st["run"] == "on" for st in allst)
    parts = [_part("sky", sky_svg(), "判決 p16（晴れ・波が穏やか）・海審 p1065（ピョンプンドの北東）"),
             dict(_part("waves", waves_svg(), "判決 p16（波が穏やか）"), drift=150.0 if run else -9.0)]
    if any(st["far"] == "on" for st in allst):
        deg = _fixed_heel(start, states, "D sea（遠くの船）")
        parts.append(_part("far", far_ship_svg(FAR_SEA["piv"], deg, FAR_SEA["s"]), "海審 p1013（要目）・p1015（〔그림1〕の写真）",
                           FAR_SEA["piv"], _keys(start, states, steps, lambda st: _vis(st["far"] == "on"))))
    mv = lambda st: dict(dx=float(st["bx"]) - x0)  # noqa: E731
    parts.append(_part("boat", boat123_svg(x0, wy, s, spk=any(st["spk"] == "on" for st in allst)),
                       "艇長の判決 p5002（100トン級・全長32.2・幅6メートル・放送の設備）", (x0, wy),
                       _keys(start, states, steps, mv)))
    parts.append(_part("front_sea", front_sea_svg(wy), "判決 p16"))
    if run:
        parts.append(_part("wake", wake123_svg(x0, wy, s), "特調委 p3099（8時57分に指示を受けて現場へ向かった）", (x0, wy),
                           _keys(start, states, steps, lambda st: dict(mv(st), **_vis(st["run"] == "on")))))
    # 外からの無線（c902：9時18分 TRS で約450人と知らされた＝艇長の判決 p5002）＝マストの先へ集まる輪
    at = next((st for st, sp in zip(states, steps) if sp.get("rings_in")), None)
    if at is not None:
        m = (float(at["bx"]) + (BOAT_M["mast"] + 0.1) * s, wy - BOAT_M["mast_top"] * s)
        parts += _pulse_part("ring_in", ring_svg(m, -135.0, r=74), "艇長の判決 p5002（無線で知らされた）", m, states, steps,
                             "rings_in", "inn")
    return parts


def _scene_D_far(start, states, steps):
    """123艇から見た遠くのセウォル号（c903・c904）。双眼鏡の丸い視野は甲板→海をなぞる（艇長の判決 p5002「쌍안경으로 …
    J갑판뿐만 아니라 바다 위 등 어디에도 보이지 않아」）＝誰もいない甲板と海（人は描かない）"""
    deg = _fixed_heel(start, states, "D far")
    piv, s = FAR["piv"], FAR["s"]
    parts = [_part("sky", sky_svg(), "判決 p16（晴れ・波が穏やか）・海審 p1065（ピョンプンドの北東）"),
             dict(_part("waves", waves_svg(), "判決 p16（波が穏やか）"), drift=-9.0),
             _part("far", far_ship_svg(piv, deg, s), "海審 p1013（要目）・p1015（〔그림1〕の写真）")]
    if any(st["mark"] == "on" for st in [start] + states):      # 使わない場面に部品（と出典）を載せない
        parts.append(_part("mark", far_ship_svg(piv, deg, s, marks=True), "判決 p18（乗客は船内で待っていた）", piv,
                           _keys(start, states, steps, lambda st: _vis(st["mark"] == "on"))))
    if any(st["binoc"] == "on" for st in [start] + states):
        (c1, c2, r) = BINOC
        cx, cy = (c1[0] + c2[0]) / 2, c1[1]
        td = ship_pt(-6.0, A_DECK, deg, NEAR)                         # 甲板（上になった右舷の側）
        dk = (cx - td[0], cy - td[1])
        se = (cx - (NEAR[0] + 560.0), cy - (WATER + 20.0))             # 左舷の側の海の面
        # 🔴 本番は層を 1920×1080 に焼いてから PIL でずらす＝画面の外に描いた所は消える（下見の SVG では消えない）。
        #   ずらしで空く帯が双眼鏡の黒い枠に隠れるよう、先に置く位置（base）を決める：横は2つの真ん中・縦は甲板で
        #   下へ枠の上の余白（丸の上＝cy−r）ぶんだけ
        base = ((dk[0] + se[0]) / 2, dk[1] - (cy - r) + 2.0)
        deck = dict(dx=dk[0] - base[0], dy=dk[1] - base[1])
        sea = dict(dx=se[0] - base[0], dy=se[1] - base[1])
        if max(abs(deck["dx"]), abs(sea["dx"])) > c1[0] - r or min(deck["dy"], sea["dy"]) < -(H - cy - r):
            raise ValueError("illu D far：双眼鏡のずらしが黒い枠の余白を越える（本番で絵の無い所が見える）")
        on = start["binoc"] == "on"
        ks = [dict(stage=0, delay=0.0, a=1.0 if on else 0.0, **deck)]
        for i, (st, sp) in enumerate(zip(states, steps)):
            dl = float(sp.get("delay", KEY_DELAY))
            if st["binoc"] == "on" and not on:
                ks.append(dict(stage=i, delay=dl, dur=0.5, a=1.0, **deck))           # 双眼鏡を上げる＝まず甲板
                ks.append(dict(stage=i, delay=dl + 2.1, dur=1.9, a=1.0, **sea))      # 海の面へなぞる
                on = True
            else:
                ks.append(dict(stage=i, delay=dl, dur=0.5, a=1.0 if st["binoc"] == "on" else 0.0,
                               dx=ks[-1]["dx"], dy=ks[-1]["dy"]))
                on = st["binoc"] == "on"
        rec = "艇長の判決 p5002（双眼鏡で甲板にも海にも乗客が見えなかった）"
        mk = [dict(stage=q["stage"], delay=q["delay"], dur=q.get("dur", 0.5), a=q["a"]) for q in ks]   # 暗い枠は濃さだけ
        parts += [_part("near", near_ship_svg(deg, base), rec, (0.0, 0.0), ks),
                  _part("binoc", binoc_svg(), rec, (0.0, 0.0), mk)]
    return parts


def _scene_D_heli(start, states, steps):
    """船の上のヘリ1機と吊り下げの線（c905）。救助された人は描かない（線の先に人を付けない）。"""
    piv = PIVOT["A"]
    parts = _ship_parts("D", start, states, steps, piv)
    parts.append(_part("front_sea", front_sea_svg(), "判決 p16"))
    ks = [dict(stage=0, delay=0.0, dy=0.0)]
    for i, sp in enumerate(steps):                                     # 空中で止まる（上下にわずかに揺れる）
        ks.append(dict(stage=i, delay=0.2, dur=2.4, dy=-7.0 if i % 2 == 0 else 3.0))
    parts.append(_part("heli", heli_svg(), "判決 p70（最初に着いた海洋警察のヘリが 9時30分ごろから救助）", HELI, ks))
    return parts


def _scene_D_rail(start, states, steps):
    """3階の左舷の手すりとゴムボート（c908〜c910）。艇長の判決 p5002「고무단정이 J에 처음 접안한 09:38경 내지 09:39경 촬영된
    동영상에 의하면, 고무단정에서 일어선 승조원의 머리 높이가 J 3층 좌현 갑판 난간 윗부분과 일치」＝立った1人の頭＝手すりの上。
    🔴 ボートに乗っていた海洋警察の人数は記録に無い＝**立った1人だけ**を描く（ほかの人を足さない）。
    機関部の船員は3階の通路につながる左舷の出入り口から出てボートへ（判決 p17）＝board（人数は判決の7人）"""
    k = RAIL["k"]
    h = 1.7 * k
    foot = big_foot(h)
    bk = lambda st: dict(dx=0.0 if st["rboat"] == "on" else -980.0, a=1.0 if st["rboat"] == "on" else 0.0)  # noqa: E731
    rb = "艇長の判決 p5002（ゴムボートが 9時38〜39分に初めて横づけ）・特調委小 p4194（ゴムボートは1隻だけ）"
    parts = [_part("rail_ship", rail_ship_svg(),
                   "艇長の判決 p5002（3階の左舷の甲板の手すり）・判決 p17（3階の通路につながる左舷の出入り口）"),
             dict(_part("waves", wave_band_svg((748, 772, 802, 838, 874), seed="illu-rail"), "判決 p16（波が穏やか）"),
                  drift=-12.0),
             _part("rboat_back", rboat_svg("back"), rb, (0.0, 0.0), _keys(start, states, steps, bk))]
    cg = None
    if start["cg"] == "on":
        cg = (0, -1.0)
    else:
        for i, (st, sp) in enumerate(zip(states, steps)):
            if st["cg"] == "on":
                cg = (i, float(sp.get("delay", 0.3)))
                break
    if cg:
        parts.append(dict(_part("cg", fig_svg(h, foot=foot), "艇長の判決 p5002（ボートで立った乗組員）"),
                          kind="sprite", foot=list(foot), inst=[dict(stage=cg[0], delay=cg[1], path=[list(RAIL_CG)])],
                          role="coast_guard", fig_h=h))
    inst, n = [], 0
    for i, (st, sp) in enumerate(zip(states, steps)):
        for j in range(int(sp.get("board") or 0)):
            if n >= len(RAIL_SPOTS):
                raise ValueError(f"illu D rail：ボートに置ける影は {len(RAIL_SPOTS)} まで")
            inst.append(dict(stage=i, delay=float(sp.get("delay", 0.3)) + float(sp.get("gap", 0.45)) * j,
                             path=[list(p) for p in rail_board_path(n)]))
            n += 1
    if inst:
        parts.append(dict(_part("crew", fig_svg(h, foot=foot), "判決 p17（9時39分に機関部の船員が海洋警察のボートへ）・海審 p1061"),
                          kind="sprite", foot=list(foot), inst=inst, role="crew", fig_h=h))
    parts += [_part("rboat_front", rboat_svg("front"), rb, (0.0, 0.0), _keys(start, states, steps, bk)),
              _part("guide", rail_guide_svg(), "艇長の判決 p5002（立った乗組員の頭の高さが手すりの上と同じ）", (0.0, 0.0),
                    _keys(start, states, steps, lambda st: _vis(st["cg"] == "on")))]
    return parts


def _c_points(view, deg):
    """置き場 C の札・輪の指し先（回した後の画面）。"""
    cen = CCEN[view]
    R = lambda p: rot_pt(p, deg, cen)  # noqa: E731
    hr, hh = 1.7 * ROOMC["k"], 1.7 * HELM["k"]
    up = lambda p, h: (R(p)[0], R(p)[1] - h)  # noqa: E731   影は立てたまま＝頭は足もとの真上
    a, c = ROOM_FIG[ROOM_ASKER], ROOM_FIG[ROOM_CAPTAIN]
    ha = up(a, hr)
    return dict(radio=R(CONS_RADIO), lamp=R(CONS_LAMP), pa=R(CONS_PA), walkie=R(ROOM_WALKIE), wheel=R(HELM_WHEEL),
                helmsman=up(HELM_FIG[0], hh), officer3=up(HELM_FIG[1], hh),
                asker=ha, captain=up(c, hr), ask=(ha[0] + 78.0, ha[1] - 46.0))


def _scene_C(start, states, steps):
    view, deg, crew = start["view"], float(start["heel"]), int(start["crew"])
    if any(st["view"] != view or float(st["heel"]) != deg or int(st["crew"]) != crew for st in states):
        raise ValueError("illu C：操舵室の見え方・傾き・人の影の数は場面の頭（start）で1つだけ（SVG で傾けて焼く）")
    cen = CCEN[view]
    L = dict(helm=HELM, console=CONS, room=ROOMC)[view]
    rec_room = dict(helm="海審 p1045（当直は3等航海士と操舵手）・p1047（操舵手が舵を回す）",
                    console="判決 p49（操舵室の放送の機器・無線機）・海審 p1058（VHF の交信）",
                    room="判決 p14（操舵室の無線機）・p49（操舵室の放送の機器・非常ベル・無線機）")[view]
    parts = [_part("c_sea", seascape_svg(L["horizon"]), "判決 p16（晴れ・波が穏やか）")]
    if view == "helm":
        parts.append(dict(_part("c_waves", wave_band_svg((472, 490, 510, 532, 553)),
                                "海審 p1048（8時46分ごろ 約18ノットで進んでいた）"), drift=150.0))
    parts.append(_part("c_room", _rot_at(c_room_svg(view), deg, cen), rec_room, cen))
    if crew:
        spots = dict(helm=HELM_FIG, room=ROOM_FIG).get(view, ())
        if crew > len(spots):
            raise ValueError(f"illu C：view={view} に置ける人の影は {len(spots)} まで（console は寄り＝人は枠の外）")
        h = 1.7 * dict(helm=HELM, room=ROOMC)[view]["k"]
        foot = big_foot(h)
        inst = [dict(stage=0, delay=-1.0, path=[list(rot_pt(p, deg, cen))]) for p in spots[:crew]]
        who = dict(helm="海審 p1045（当直は3等航海士と操舵手の2人）", room="判決 p11（操舵室に集まった甲板部）・p14（まだ操舵室に）")[view]
        parts.append(dict(_part("crew", fig_svg(h, 0.0, foot), who),
                          kind="sprite", foot=list(foot), inst=inst, role="crew", fig_h=h, fig_deg=0.0))
    pts = _c_points(view, deg)
    if view == "console":
        parts += _pulse_part("ring_out", ring_svg(pts["radio"], -55.0 + deg), "判決 p11・海審 p1058（VHF の交信）",
                             pts["radio"], states, steps, "rings", "out")
        parts += _pulse_part("ring_in", ring_svg(pts["radio"], -55.0 + deg, r=70), "判決 p13〜14（管制センターからの交信）",
                             pts["radio"], states, steps, "rings_in", "inn")
        parts += _pulse_part("glow", glow_svg(pts["lamp"]), "海審 p1060（注30：非常電源が来ていた）", pts["lamp"],
                             states, steps, "glow", "glow")
    if view == "room":
        parts += _pulse_part("walkie", ring_svg(pts["walkie"], 125.0 + deg, r=56), "判決 p14（3階の乗務員から無線機で）",
                             pts["walkie"], states, steps, "walkie", "inn")
        parts += _pulse_part("asks", ask_svg(pts["ask"]), "判決 p14（2等航海士から何度も「どうしましょうか」）", pts["ask"],
                             states, steps, "asks", "ask")
    parts.append(_part("inset", inset_svg(deg, "bridge"), "海審 p1013（要目）・p1015（〔그림1〕の写真）"))
    return parts


def _scene_E(start, states, steps):
    parts = [_part("e_room", e_room_svg(),
                   "特調委 p3096（管制センター＝レーダーと交信の装備で船の動きを見守る所）・特調委小 p4180（管制の画面）"),
             _part("e_dot", e_dot_svg(), "海審 p1010（진도VTS のレーダーの航跡）・p1059（セウォル号を呼んだ）"),
             _part("e_sel", e_sel_svg(), "海審 p1059（9時6分に VHF でセウォル号を呼んだ）", EDOT,
                   _keys(start, states, steps, lambda st: _vis(st["sel"] == "on")))]
    parts += _pulse_part("ring_out", ring_svg(EMIC, EDIR, r=70), "特調委小 p4180（9時6分〜9時36分の交信）", EMIC, states, steps,
                         "rings", "out")
    return parts


def _scene_D_ship(start, states, steps):
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
    v = st.get("view")
    if place == "RA":
        return _ra_anchors(v)
    if place == "VA":
        return _va_anchors(v)
    if place == "RB":
        return _rb_anchors(st)
    if place == "RD":
        return dict(tail=RD_TAIL)
    if place == "RC":
        return _rc_anchors(v)
    if place == "A" or (place == "D" and v in ("ship", "heli")):
        piv = PIVOT["D"] if (place == "D" and v == "ship") else PIVOT["A"]
        h = float(st["heel"])
        a = {"b_port": ship_pt(SHIP_HALF, B_DECK, h, piv), "br_port": ship_pt(SHIP_HALF, BR_DECK, h, piv),
             "boxes_sea": box_fall_pt(h, piv), "win": ship_pt(3.0, A_DECK + 1.35, h, piv),
             "boxes": ship_pt(-2.0, HULL_TOP + BOX["tier"] * 1.5, h, piv),
             "boat": (BOAT["x0"] + 264.0, BOAT["deck"] - 100.0), "ship": ship_pt(0.0, ROOF, h, piv),
             "bridge": ship_pt(0.0, ROOF + 0.55, h, piv), "heli": (HELI[0] + 10.0, HELI[1] - 50.0),
             "line": (HELI_LINE[0], HELI_LINE[2])}
        return a
    if place == "D":
        h = float(st["heel"])
        if v == "sea":
            x0, s, wy = float(st["bx"]), SEA["s"], SEA["water"]
            return {"boat": (x0 + 13.2 * s, wy - 6.4 * s), "cabin": (x0 + 13.0 * s, wy - 3.7 * s),
                    "spk": (x0 + BOAT_M["spk"][0] * s, wy - (BOAT_M["spk"][1] + 0.62) * s),
                    "far": far_center(FAR_SEA["piv"], h, FAR_SEA["s"])}
        if v == "far":
            fp, fs = FAR["piv"], FAR["s"]
            w = ship_pt(3.0, A_DECK + 1.35, h, fp)
            return {"far": far_center(fp, h, fs), "win_far": (fp[0] + (w[0] - fp[0]) * fs, fp[1] + (w[1] - fp[1]) * fs)}
        return {"rail": (RAIL_CG[0] + 330.0, RAIL_TOP), "head": (RAIL_CG[0], RAIL_TOP), "door": (RAIL_DOOR[0], RAIL_DOOR[1] - 150.0),
                "rboat": (760.0, RAIL_FLOOR + 26.0)}
    if place == "C":
        return _c_points(v, float(st["heel"]))
    if place == "E":
        return {"dot": EDOT, "mic": EMIC, "screen": (ERAD[0], ESCR[1] + 60.0)}
    deg = float(st["heel"])
    return {"desk": rot_pt((960.0, 560.0), deg, CB), "spk": rot_pt(CABIN_SPK, deg, CB),
            "corr_spk": rot_pt(corridor_spk(), deg, CB), "crowd": rot_pt((900.0, ROOM["floor"] + 60), deg, CB)}


def _camc(place, st0, states):
    """カメラ（cam）で寄る中心の既定。見え方ごとに主役の所へ。"""
    last = states[-1] if states else st0
    if place == "RA":
        return (960.0, RA_Y0)
    if place == "VA":
        return (960.0, VA_Y0)
    if place == "RB":
        return RB_CR if st0["view"] == "rear" else RB_C
    if place == "RD":
        return RD_TAIL
    if place == "RC":
        return (960.0, RC_CAM[st0["view"]]["hz"])
    if place == "C":
        return CCEN[st0["view"]]
    if place == "A" and any(st["bridge"] == "on" for st in [st0] + states):
        return ship_pt(0.0, (BR_DECK + ROOF) / 2, float(last["heel"]), PIVOT["A"])
    if place == "D":
        v = st0["view"]
        if v == "sea":
            return (float(last["bx"]) + BOAT_L * SEA["s"] * 0.42, SEA["water"] - 90.0)
        if v == "far":
            return far_center(FAR["piv"], float(st0["heel"]), FAR["s"])
        if v == "heli":
            return (900.0, 380.0)
        if v == "rail":
            return (960.0, 560.0)
    return CAM_C[place]


def scene(place, steps, start=None, at=None, people=None, src=None, view=None, rec=None, scale=None, camc=None, assume=None):
    """再現イラストの場面1つ（型 `illu`・冒頭の絵 `intro=dict(illu=…)`・小さく戻す `illu_pair` が使う）。

    place  … 置き場 "A"／"B"／"C"／"D"／"E"（上の説明）
    start  … 頭の状態（既定は FIELDS）。steps … 台本の行ごとの段 dict(state=dict(…), rec="資料 p頁", tag=…,
             rings=数〈音の輪〉, rings_in=数〈外から集まる輪〉, glow=数〈灯〉, asks=数〈問いかけの印〉, walkie=数〈3階から〉,
             board=数〈乗り移る人〉, delay=秒, dur=秒, touch="3階（B甲板）の左舷")
    at     … 場面の時刻（宣言・画面には出さない）。人を描く場面は必須（門番 ②）
    people … 描いた人の数の宣言 dict(crew=(8, "判決 p11"))（門番 ③）
    src    … 左下の出典（省略時は部品と段の rec から組む＋置き場の断り NOTE）
    view   … 左上の見る向き（省略時は置き場の既定）。scale … 上から見た絵の縮尺（メートル／画素）
             🔴 15本目 RA は描く側が組む（見え方の縮尺 ÷ カメラの寄りの最大＝門番 ⑧ が見る値）
    camc   … カメラで寄る中心（画素か、札の指し先の名＝RA の "fall_mid" など）
    15本目（⑤b-2）の置き場：RA＝上から見たステッド空港（view＝wide／near／ramp・gg＝事故機の印 off／p7／p8／gone・
             path＝点線（模式）・trace＝琥珀の線・x・box・laps＝3周の航跡・seg67・ring8・piece・fuel・course）／
             RB＝空の中の事故機（view＝side／rear・ground・pitch＝機首の上げ（度）・roll＝左への傾き（度）・ail＝補助翼 off／right・
             出来事 rings＝テレメトリーの輪・pylon＝パイロンが1本流れる）／RD＝ピットの事故機（view＝tail・mark）
    16本目（⑤b-2）の置き場：VA＝上から見た谷（view＝wide／near／west・欄は FIELDS["VA"] の注）
    assume … 想定の札（「会社の説明（想定）」など＝起きた事ではない絵・左上の見る向きの下）
    """
    if place not in FIELDS:
        raise ValueError(f"illu：知らない置き場 {place!r}（{tuple(FIELDS)}）")
    steps = [dict(s) for s in steps]
    for sp in steps:
        bad = set(sp) - {"state", "rec", "tag", "gap", "delay", "dur", "ring_delay", "touch"} - set(EVENTS)
        if bad:
            raise ValueError(f"illu：段に知らない鍵 {sorted(bad)}")
    st0, states = _states(place, start, steps)
    parts = {"A": _scene_A, "B": _scene_B, "C": _scene_C, "D": _scene_D, "E": _scene_E,
             "RA": _scene_RA, "RB": _scene_RB, "RD": _scene_RD, "RC": _scene_RC,
             "VA": _scene_VA}[place](st0, states, steps)
    if isinstance(camc, str):
        camc = _anchors(place, states[-1] if states else st0)[camc]
    if "pan" in FIELDS[place]:
        # 15本目 ⑤b-3：首振り（pan）＝カメラの中心 cx を段の鍵で動かす（build_jiko._il_cam・下見が cx を読む）。
        #   層は画面の大きさで焼くので、層を横にずらすと端が空く＝寄り（cam）の中で中心だけ動かす
        c0 = camc if isinstance(camc, (list, tuple)) else _camc(place, st0, states)
        cam = _keys(st0, states, steps, lambda st: dict(z=float(st["cam"]), cx=float(c0[0]) + float(st["pan"])))
    else:
        cam = _keys(st0, states, steps, lambda st: dict(z=float(st["cam"])))
    if place in ("RA", "VA"):
        # 🔴 上から見た絵の縮尺は描く側が組む（見え方の縮尺 ÷ カメラの寄りの最大＝門番 ⑧ が見る値）。16本目 VA も同じ
        auto = (RA_VIEW if place == "RA" else VA_VIEW)[st0["view"]]["mpp"] / max(float(k.get("z", 1.0)) for k in cam)
        scale = min(float(scale), auto) if scale else auto
    objects = {}
    for p in parts:
        for k, n in (p.get("obj") or {}).items():
            objects[k] = objects.get(k, 0) + int(n)
    tags = []
    mend = _rb_motion_end(st0, states, steps) if place == "RB" else {}
    for i, (st, sp) in enumerate(zip(states, steps)):
        # 🔴 ⑤b-3：札の指し先は「段の終わりの状態」＝見え方の入れ替えや機首の上げ（一気に大きく動く）の段で札を 0.35秒に出すと、
        #    動く前の空を指す（試し焼き 36657377530 の c307：「17.3G」が水平の機体の先の空を指した）＝既定は動きが終わってから
        g, texts, keep, dl = [], [], False, max(0.35, mend.get(i, 0.0))
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
    label = view or _label(place, st0, states)
    if not src:
        src = rec_line(recs)
        note = NOTE.get(place)
        note = note(st0, states) if callable(note) else note
        if note:
            src = (src + "／" if src else "") + note
    return dict(place=place, view=label, at=at, people=dict(people or {}), scale=scale, rec=rec, objects=objects,
                parts=parts, cam=cam, camc=list(camc or _camc(place, st0, states)), tags=tags, nstage=len(steps),
                start=st0, states=states, steps=steps, recs=recs, src=src, assume=assume or "")


def _label(place, st0, states):
    """左上の見る向き。RB で見え方が段で入れ替わる場面は、出てくる順に「後ろから→横から見た図」（§5b-80 の合図）。
    ⚠️ ⑤b-2 の下見のあと：見え方の名を絵の層で2つ入れ替える形は、同じ位置の文字が重なる（check_layout）＝上の層の1行にした"""
    if place == "D":
        return D_VIEW[st0["view"]]
    if place == "RA":
        return RA_VIEW[st0["view"]]["lab"]
    if place == "RC":
        return RC_VIEW[st0["view"]]
    if place == "VA":
        return VA_LAB
    if place == "RB":
        seq = []
        for st in [st0] + list(states):
            if st["view"] not in seq:
                seq.append(st["view"])
        return "→".join(RB_VIEW[v].replace("見た図", "") for v in seq[:-1]) + ("→" if len(seq) > 1 else "") + RB_VIEW[seq[-1]]
    return VIEW[place]


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
    f.illu = dict(full=True, scenes=[dict(sc, role="main", box=None)], view=sc["view"], src=sc["src"], assume=sc["assume"])
    return f


PAIR_BOX = ((96, 262, 840, 473), (984, 262, 840, 473))
TRIO_BOX = ((96, 262, 560, 315), (680, 262, 560, 315), (1264, 262, 560, 315))     # 15本目 ⑤b-2：3つの問い（c109）


def illu_pair(blocks, lead=""):
    """2つ（または3つ）の問いのパネルの中に、再現イラストを小さく戻す（画面の種類「混ざり」・14本目 c105・c108・15本目 c109）。

    blocks … [dict(k="問い1", t="なぜ傾いたか", v="…", stage=段, scene=dict(place="A", steps=[…], …)), 2つか3つ]
             段の数は台本の行の数（`stages=`・行より多ければ行のあいだに挟まる）。絵は block の stage の行頭から見せる。
    """
    if len(blocks) not in (2, 3):
        raise ValueError("illu_pair：問いは2つか3つ")
    n = max(int(b.get("stages", 1)) for b in blocks)
    stages = [[] for _ in range(n)]
    lab, scenes, recs = [], [], []
    for b, (x, y, w, h) in zip(blocks, PAIR_BOX if len(blocks) == 2 else TRIO_BOX):
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
