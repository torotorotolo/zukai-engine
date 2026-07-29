# -*- coding: utf-8 -*-
"""事故検証×図解様式のテスト映像。10カット・90.7秒。

題材＝**アロハ航空243便**（1988-04-28・ボーイング737-200・N73711）。
巡航中に胴体上部の外板が飛行中に剥離した。原因は重ね継手の接着剥離と疲労亀裂。

■ 数字はすべて NTSB/AAR-89/03 本文で裏を取った（`ref/ntsb_aar8903.pdf` を検索）
    高度 24,000 ft（7,300 m）／乗客89人・乗員6人＝95人／死者1・重傷8
    剥離範囲「客室扉より後方・客室床面より上を約18 ft（5.5 m）」
    N73711 の実績 35,496 飛行時間・**89,680 サイクル**（世界の737で2番目）
    737 の経済設計寿命「20年・51,000時間・**75,000サイクル**」
    外板の板厚 0.036 インチ（0.91 mm）
    亀裂は S-10L 重ね継手の**最上列のリベット**に沿って発生

■ 素材はすべてパブリックドメイン（`ref/CREDITS.md` に出典と作者を記録）
  米連邦機関（NTSB / FAA / NASA）と米国国立公文書館（NARA）の著作物。

■ 実写の割合（2026-07-29 カズヤくん指示で方針変更）
  当初は競合と同水準の18%に合わせていたが、**「使える限り最大限写真を使う」**に変更。
  全画面の実写4カット＝32.0秒 / 全体90.7秒 = **35.3%**。さらに c2 に写真インセット1点。
  図解は骨格として残す（競合の図解比率は約7%なので、密度の差は保てている）。

■ 尺はナレーションから逆算する
  音声を先に作り、`audio/narration.json` の実測秒に前後の間を足したものをカット尺にする。
  映像に合わせて喋らせると必ず早口になる。

■ カット構成
  p1 実写   事故機の左側面（屋根が消えている）      … 掴み
  p2 実写   事故前の N73711 本人                    … 同じ機体だと示す
  c2 図解   機体側面図と剥離範囲（＋写真インセット） … どこが
  p3 実写   着陸後の機体を見上げる調査員            … 人と並べて大きさを出す
  c3 図解   胴体断面（事故前／剥離後）              … どれだけ
  c4 図解   重ね継手の平面図・疲労亀裂              … どこから
  c5 図解   重ね継手の A-A 断面・接着剥離            … なぜ
  p4 実写   ヒロ発ホノルル行きの航路（NASA）        … 舞台
  c6 図解   高度の時系列                            … 何が起きたか
  c7 図解   経済設計寿命と実際の回数                … 背景
"""
import base64
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J
import render

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
FONTS = Path(os.environ.get("ZUKAI_FONTS", HERE / "fonts"))
CSS = ""

# 機体側面図の置き場所。(x, y) は**機首先端・胴体上面線**（jiko_style の座標系）
AC_X, AC_Y, AC_S = 170, 560, 1.5

CR_NTSB = "出典：NTSB（米国運輸安全委員会）／パブリックドメイン"
CR_NTSB_S = "出典：NTSB／パブリックドメイン"
CR_FAA = "出典：FAA（米国連邦航空局）／パブリックドメイン"
CR_NARA = "出典：米国国立公文書館（NARA）／撮影 Charles O'Rear／パブリックドメイン"
CR_NASA = "出典：NASA／パブリックドメイン"


def ax(u):
    """機体座標の x（単位）→ 画面 x"""
    return AC_X + u * AC_S


def ay(u):
    return AC_Y + u * AC_S


def face_css(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


def page(inner, w=W, h=H):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}">{inner}</svg>')
    return (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{CSS}'
            f'body{{width:{w}px;height:{h}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')


# ── 字幕 ─────────────────────────────────────────────────
# 🔴 2026-07-30 カズヤくん指示で必須になった。あわせて**3秒以上の静止を禁止**。
#    字幕は 1行ずつ音声を合成して尺を取っているので、フレーム精度で音と合う。
#    画面下 y=950 以下は字幕帯として空けてある（他の注記を置かない）。
SUB_Y, SUB_H = 950, 130
XML = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def esc(t):
    return "".join(XML.get(c, c) for c in t)


def sub_row(text, w=W, h=SUB_H):
    """字幕1行。写真の上でも読めるよう、下へ向かって濃くなる地を敷いてから白で置く。
    帯を四角く塗ると「テロップ板」に見えて図解様式から浮くので、必ずグラデーションにする。"""
    return (f'<rect width="{w}" height="{h}" fill="url(#subg)"/>'
            f'<text x="{w / 2:.0f}" y="{h * 0.63:.0f}" font-family="Noto" font-size="46" '
            f'fill="{J.INK_W}" text-anchor="middle" stroke="{J.BG}" stroke-width="7" '
            f'paint-order="stroke">{esc(text)}</text>')


def sub_strip(lines):
    """1カットぶんの字幕を縦に積んだ帯。合成時に行ごとに切り出す。"""
    g = [f'<linearGradient id="subg" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{J.BG}" stop-opacity="0"/>'
         f'<stop offset="0.45" stop-color="{J.BG}" stop-opacity="0.72"/>'
         f'<stop offset="1" stop-color="{J.BG}" stop-opacity="0.86"/></linearGradient>']
    for i, t in enumerate(lines):
        g.append(f'<g transform="translate(0,{i * SUB_H})">{sub_row(t)}</g>')
    return "".join(g)


def photo_frame(x, y, w, h, credit, size=25):
    """写真の枠と出典。**出典は必ず画面に出す。**"""
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" '
         f'stroke="{J.LINE}" stroke-width="6"/>']
    for cx, cy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        g.append(f'<path d="M{cx - 26} {cy} h52 M{cx} {cy - 26} v52" stroke="{J.INK_W}" '
                 f'stroke-width="6"/>')
    g.append(J.label(x, y + h + 40, credit, J.LINE_DIM, size))
    return "".join(g)


# ── p1：実写（事故機の左側面） ────────────────────────────
P1_BOX = (140, 258, 1080, 592)


def p1_bg():
    """写真の下に敷く地。**注記は別レイヤーにする**（初稿は注記側にも背景を塗って写真が消えた）。"""
    return J.frame(W, H) + J.title("飛行中に、屋根が消えた",
                                   "アロハ航空243便　1988年4月28日　ボーイング737-200")


def p1_over():
    x, y, w, h = P1_BOX
    g = [photo_frame(x, y, w, h, CR_NTSB)]
    g.append(J.leader(560, 430, 1290, 322, J.ALERT))
    g.append(J.label(1310, 308, "客室の天井と外板が", J.ALERT, 44))
    g.append(J.label(1310, 362, "5.5 m にわたって消失", J.ALERT, 44))
    g.append(J.label(1310, 462, "高度 7,300 m を巡航中に発生", J.INK_W, 32))
    g.append(J.label(1310, 508, "乗客89人・乗員6人", J.INK_W, 32))
    g.append(J.label(1310, 554, "客室乗務員1名が機外へ", J.INK_W, 32))
    g.append(J.label(1310, 700, "▼ この機体に何が起きたのか", J.AMBER, 34))
    return "".join(g)


# ── p2：実写（事故前の N73711 本人） ──────────────────────
P2_BOX = (900, 268, 880, 598)


def p2_bg():
    return J.frame(W, H) + J.title("この機体は、19年間飛んでいた",
                                   "事故を起こした N73711　1969年製")


def p2_over():
    x, y, w, h = P2_BOX
    g = [photo_frame(x, y, w, h, CR_NARA, 23)]
    g.append(J.label(150, 360, "N 7 3 7 1 1", J.AMBER, 62))
    g.append(J.label(150, 428, "ハワイ諸島を結ぶ短距離路線を", J.LINE, 32))
    g.append(J.label(150, 474, "1日に十数往復していた", J.LINE, 32))
    g.append(J.label(150, 560, "1回の飛行は短い。だが", J.LINE, 30))
    g.append(J.label(150, 604, "離陸と着陸の回数だけが、", J.INK_W, 32))
    g.append(J.label(150, 648, "同型機の倍の速さで積み上がっていた。", J.INK_W, 32))
    return "".join(g)


# ── c2：機体側面図（＋写真インセット） ────────────────────
# 1巡目の粗を全部直した：
#   引き出し線が機体を横断していた → 注記は機体の上下に置き、線を短くする
#   5.5m 寸法が図から離れて浮いていた → 剥離範囲の真上に降ろす
#   目盛線が胴体の上を通っていた → 機体より先に描いて下に潜らせる
#   胴体直径の注記が機体を跨いでいた → **断面図(c3)に任せて c2 からは外す**
C2_INSET = (1330, 300, 500, 324)


def c2_base():
    g = [J.frame(W, H), J.title("消えたのは、前方扉のすぐ後ろから",
                                "ボーイング737-200　側面図（NTSB調査資料の三面図から作図）")]
    # 機首からの距離。**実在しない station 番号を振ると図が嘘になる**ので、
    # 実測できる「機首からの m」で目盛る（全長30.53m = 720単位）。
    for m in range(0, 31, 5):
        u = m * 720 / 30.53
        g.append(f'<path d="M{ax(u):.0f} 380 V760" stroke="{J.GRID}" stroke-width="2.4"/>')
        g.append(J.label(ax(u), 796, f"{m} m", J.LINE_DIM, 22, "middle"))
    g.append(J.b737_side(AC_X, AC_Y, AC_S))
    return "".join(g)


def c2_hole():
    return J.b737_tear(AC_X, AC_Y, AC_S, part="hole")


def c2_tearline():
    return J.b737_tear(AC_X, AC_Y, AC_S, part="line")


def c2_anno():
    g = [J.dim(ax(120), ax(249.5), 512, "5.5 m")]
    g.append(J.leader(ax(185), ay(2), 470, 448, J.ALERT))
    g.append(J.label(190, 316, "剥離した範囲", J.ALERT, 42))
    g.append(J.label(190, 366, "客室の扉より後ろ、床より上。", J.LINE, 28))
    g.append(J.label(190, 404, "外板が一続きに裂けて飛散した", J.LINE, 28))
    g.append(J.dim(ax(0), ax(720), 850, "全長 30.5 m"))
    x, y, w, h = C2_INSET
    g.append(photo_frame(x, y, w, h, CR_NTSB_S, 24))
    g.append(J.label(1330, 700, "与圧された客室の内側は", J.LINE, 28))
    g.append(J.label(1330, 738, "外気より 0.5 気圧ぶん高い。", J.LINE, 28))
    g.append(J.label(1330, 776, "その圧力が、裂け目を", J.INK_W, 28))
    g.append(J.label(1330, 814, "一気に押し広げた。", J.INK_W, 28))
    return "".join(g)


# ── p3：実写（着陸後の機体を見上げる調査員） ──────────────
P3_BOX = (150, 262, 800, 607)


def p3_bg():
    return J.frame(W, H) + J.title("人と並べると、大きさが分かる",
                                   "マウイ島カフルイ空港に緊急着陸した機体")


def p3_over():
    x, y, w, h = P3_BOX
    g = [photo_frame(x, y, w, h, CR_FAA)]
    g.append(J.leader(560, 400, 1080, 350, J.ALERT))
    g.append(J.label(1100, 336, "剥き出しになった", J.ALERT, 40))
    g.append(J.label(1100, 386, "胴体のフレームと床梁", J.ALERT, 40))
    g.append(J.label(1100, 480, "外板が無くなると、", J.LINE, 30))
    g.append(J.label(1100, 522, "客室を形づくっていた骨組みが", J.LINE, 30))
    g.append(J.label(1100, 564, "そのまま外に出る。", J.LINE, 30))
    g.append(J.label(1100, 650, "この状態で、13分間飛んだ。", J.INK_W, 34))
    return "".join(g)


# ── c3：胴体断面 ──────────────────────────────────────────

def c3_base():
    g = [J.frame(W, H), J.title("失われたのは、上半分だった", "胴体断面（客室1〜4列目）")]
    g.append(J.b737_section(600, 620, 1.5, floor=True))
    g.append(J.b737_section(1400, 620, 1.5, upper=(-165, -15), floor=True))
    for cx in (600, 1400):
        for dx in (-116, -78, 78, 116):
            g.append(f'<rect x="{cx + dx - 15}" y="{620 + 44}" width="30" height="46" rx="5" '
                     f'fill="none" stroke="{J.LINE_DIM}" stroke-width="4"/>')
    return "".join(g)


def c3_anno():
    g = [J.label(600, 960, "事故前", J.LINE, 40, "middle"),
         J.label(1400, 960, "剥離後", J.ALERT, 40, "middle"),
         J.label(600, 690, "客室", J.LINE, 28, "middle"),
         J.label(600, 806, "貨物室", J.LINE, 28, "middle"),
         J.label(742, 762, "床", J.LINE_DIM, 24, "start")]
    g.append(J.dim(600 - 300, 600 + 300, 380, "3.76 m"))
    g.append(J.leader(1400, 320, 1660, 250, J.ALERT))
    g.append(J.label(1680, 236, "ここが消えた", J.ALERT, 38))
    g.append(J.label(1680, 282, "円周の約 55%", J.LINE, 28))
    g.append(J.label(1000, 620, "→", J.INK_W, 72, "middle"))
    return "".join(g)


# ── c4：重ね継手の平面図 ──────────────────────────────────

LJ_X, LJ_Y, LJ_S = 720, 610, 0.95


def c4_base():
    g = [J.frame(W, H), J.title("始まりは、リベット1列の亀裂",
                                "外板の重ね継手（ラップジョイント）を外から見た図")]
    g.append(J.lap_joint(LJ_X, LJ_Y, LJ_S, cracks=0))
    return "".join(g)


def c4_crack():
    return J.lap_joint(LJ_X, LJ_Y, LJ_S, cracks=15, only_cracks=True)


def c4_anno():
    """注記は必ず図の外へ。図の上に載せると読めない（初稿の失敗）。"""
    g = [J.label(300, 356, "外板（上）", J.INK_W, 32),
         J.label(300, 900, "外板（下）", J.LINE, 32)]
    # 重ね幅は**縦に測る寸法**。横に引くと図が嘘になる
    g.append(J.vdim(LJ_Y - 62 * LJ_S, LJ_Y + 62 * LJ_S, LJ_X - 480 * LJ_S - 40, "76 mm"))
    g.append(J.leader(LJ_X + 180, LJ_Y - 40 * LJ_S, 1330, 330, J.ALERT))
    g.append(J.label(1350, 316, "最上列のリベット穴から", J.ALERT, 36))
    g.append(J.label(1350, 360, "疲労亀裂が発生", J.ALERT, 36))
    g.append(J.label(1350, 430, "1本ずつは短い。", J.LINE, 28))
    g.append(J.label(1350, 468, "だが隣とつながると", J.LINE, 28))
    g.append(J.label(1350, 506, "一続きの裂け目になる", J.LINE, 28))
    g.append(J.label(1350, 590, "搭乗中の乗客が、この亀裂を", J.INK_W, 30))
    g.append(J.label(1350, 628, "見ていた。誰にも言わなかった。", J.INK_W, 30))
    # A-A の切断線。次のカットの断面がどこを切ったものか示す
    cx = LJ_X + 300 * LJ_S
    g.append(f'<path d="M{cx} 300 V880" stroke="{J.AMBER}" stroke-width="3" '
             f'stroke-dasharray="26 14"/>')
    g.append(J.label(cx, 286, "A", J.AMBER, 34, "middle"))
    g.append(J.label(cx, 916, "A", J.AMBER, 34, "middle"))
    return "".join(g)


# ── c5：重ね継手の A-A 断面 ───────────────────────────────
# 1巡目は図が小さく、引き出し線が図を横断し、下1/3が空いていた。
# 図を大きくして中央に据え、注記は**図の上下の空きに置いて線を短くする**。
SEC_X, SEC_Y, SEC_S = 860, 560, 2.0
SEC_HL = 95 * SEC_S          # 重ね幅の半分（画面px）


def c5_base():
    g = [J.frame(W, H), J.title("荷重を分け合う相手が、いなくなった",
                                "重ね継手 A-A 断面（板厚 0.91 mm。図では誇張している）")]
    g.append(J.lap_joint_section(SEC_X, SEC_Y, SEC_S, crack=False))
    return "".join(g)


def c5_crack():
    return J.lap_joint_section(SEC_X, SEC_Y, SEC_S, crack=True)


def c5_anno():
    top = SEC_Y - 26 * SEC_S          # 上の外板の上面
    bot = SEC_Y + 26 * SEC_S          # 下の外板の下面
    g = [J.dim(SEC_X - SEC_HL, SEC_X + SEC_HL, 436, "76 mm")]
    # 皿もみの縁 → 図の左上へ（上の外板の上は空いている）
    g.append(J.leader(SEC_X - 62 * SEC_S, top + 6, 620, 372, J.ALERT))
    g.append(J.label(150, 288, "皿もみの縁は、刃のように薄い", J.ALERT, 36))
    g.append(J.label(150, 336, "リベット穴は円錐形に沈めてある。", J.LINE, 27))
    g.append(J.label(150, 372, "その縁がいちばん薄い。", J.LINE, 27))
    # 段差 → 図の右上へ
    g.append(J.leader(SEC_X + SEC_HL, SEC_Y, 1330, 360, J.AMBER))
    g.append(J.label(1350, 300, "段差", J.AMBER, 38))
    g.append(J.label(1350, 348, "外から見えるのは、", J.LINE, 27))
    g.append(J.label(1350, 384, "この一段だけ。", J.LINE, 27))
    # 接着層 → 図の左下（上の外板の下・下の外板の左は空いている）
    g.append(J.leader(SEC_X - SEC_HL - 6, SEC_Y + 10, 560, 690, J.OK))
    g.append(J.label(150, 706, "接着層", J.OK, 40))
    g.append(J.label(150, 754, "設計では、この接着面とリベットで", J.LINE, 27))
    g.append(J.label(150, 790, "荷重を分け合うはずだった。", J.LINE, 27))
    g.append(J.label(150, 838, "潮風の中を19年。接着面には湿気が入り、", J.INK_W, 27))
    g.append(J.label(150, 874, "腐食が進んで剥がれていた。", J.INK_W, 27))
    g.append(J.label(1350, 706, "荷重の行き場は", J.ALERT, 32))
    g.append(J.label(1350, 748, "リベット穴の縁だけ", J.ALERT, 32))
    g.append(J.label(SEC_X - 640, top - 14, "外板（上）", J.INK_W, 28))
    g.append(J.label(SEC_X + 660, bot + 40, "外板（下）", J.LINE, 28, "end"))
    return "".join(g)


# ── p4：実写（航路・NASA） ────────────────────────────────
P4_BOX = (1030, 250, 760, 591)


def p4_bg():
    return J.frame(W, H) + J.title("ヒロを出て、ホノルルへ向かっていた",
                                   "アロハ航空243便の航路　ハワイ諸島")


def p4_over():
    x, y, w, h = P4_BOX
    g = [photo_frame(x, y, w, h, CR_NASA)]
    g.append(J.label(150, 340, "島から島へ、20〜30分の飛行。", J.LINE, 32))
    g.append(J.label(150, 386, "1日に十数回、上がっては降りる。", J.LINE, 32))
    g.append(J.label(150, 470, "与圧は、そのたびに", J.INK_W, 34))
    g.append(J.label(150, 516, "かかっては、抜ける。", J.INK_W, 34))
    g.append(J.label(150, 604, "胴体は、そのたびに", J.ALERT, 34))
    g.append(J.label(150, 650, "膨らんでは、縮んでいた。", J.ALERT, 34))
    g.append(J.label(150, 750, "19年間で 89,680 回。", J.AMBER, 38))
    return "".join(g)


# ── c6：高度の時系列 ──────────────────────────────────────

PTS = [(0.00, 0.00), (0.13, 0.86), (0.30, 0.92), (0.36, 0.92),
       (0.41, 0.60), (0.57, 0.28), (0.78, 0.09), (1.00, 0.00)]


def c6_base():
    g = [J.frame(W, H), J.title("剥離から着陸まで、13分", "高度の推移")]
    g.append(J.alt_graph(230, 330, 1460, 520, PTS, mark=3))
    return "".join(g)


def c6_anno():
    g = [J.label(210, 350, "7,300 m", J.AMBER, 30, "end"),
         J.label(210, 592, "3,600 m", J.LINE_DIM, 26, "end"),
         J.label(210, 856, "0", J.AMBER, 30, "end"),
         J.label(230, 890, "離陸　ヒロ", J.LINE, 28),
         J.label(1690, 890, "着陸　マウイ島カフルイ", J.LINE, 28, "end")]
    mx = 230 + 1460 * 0.36
    g.append(J.leader(mx, 330 + 520 * 0.08, 1120, 236, J.ALERT))
    g.append(J.label(1140, 222, "ここで剥離", J.ALERT, 38))
    g.append(J.label(1140, 268, "操縦室の扉も吹き飛び、", J.LINE, 26))
    g.append(J.label(1140, 302, "機長は客室の空を直接見ていた", J.LINE, 26))
    g.append(J.label(660, 640, "緊急降下", J.INK_W, 34))
    g.append(J.dim(mx, 1690, 930, "13分"))
    return "".join(g)


# ── c7：数字 ──────────────────────────────────────────────

def c7_base():
    g = [J.frame(W, H), J.title("設計の想定を、超えて飛んでいた",
                                "離着陸の回数（NTSB報告書 1.17.2 節）")]
    g.append(f'<path d="M960 330 V900" stroke="{J.LINE_DIM}" stroke-width="4"/>')
    g.append(J.label(960, 916, "1969年製・19年間・ハワイ諸島間の短距離を1日十数往復",
                     J.LINE, 30, "middle"))
    return "".join(g)


def c7_num(k):
    n = int(89680 * k)
    g = [J.bignum(520, 640, "75,000", "回", "経済設計寿命（20年）", J.LINE),
         J.bignum(1400, 640, f"{n:,}", "回", "実際に飛んだ回数", J.ALERT)]
    if k >= 0.999:
        g.append(J.label(1400, 760, "想定の 1.20 倍", J.ALERT, 40, "middle"))
        g.append(J.label(520, 760, "この回数で使い切る前提だった", J.LINE, 28, "middle"))
    return "".join(g)


# ── カットの並びと尺 ──────────────────────────────────────
# 🔴 尺は**ナレーションから逆算する**。映像に合わせて喋らせると必ず早口になる。
#    `audio/narration.json` があればそれを使い、無ければ下の暫定値で焼く。
LEAD, TAIL = 0.35, 0.50      # 台詞の前後に置く間
_DEFAULT = [("p1", 5.0), ("p2", 3.6), ("c2", 6.2), ("p3", 3.6), ("c3", 5.4),
            ("c4", 6.0), ("c5", 6.4), ("p4", 3.4), ("c6", 5.4), ("c7", 5.4)]


def _narration():
    import json
    p = HERE / "audio" / "narration.json"
    if not p.exists():
        return _DEFAULT, {}
    d = json.loads(p.read_text(encoding="utf-8"))
    dur = d["durations"]
    cuts = [(c, round(dur[c] + LEAD + TAIL, 2)) if c in dur else (c, s)
            for c, s in _DEFAULT]
    return cuts, d.get("subtitles", {})


CUTS, SUBS = _narration()

# 全画面の実写カット。ゆっくり寄る。(枠, ファイル名, 縦方向の寄せ 0=上 0.5=中央 1=下)
PHOTO_CUTS = {
    "p1": (P1_BOX, "aloha_left.jpg", 0.5),
    "p2": (P2_BOX, "aloha_normal.jpg", 0.34),   # 機体と N73711 の登録記号は上寄り
    "p3": (P3_BOX, "ref_aloha_after.jpg", 0.5),
    "p4": (P4_BOX, "ref_aloha_route.jpg", 0.5),
}
# 図解カットに差し込む写真。こちらは動かさない
INSETS = {"c2": (C2_INSET, "ref_aloha_fuselage.png")}


def render_all(force=False):
    out = HERE / "out" / "jiko"
    out.mkdir(parents=True, exist_ok=True)
    jobs = {"p1_bg": p1_bg(), "p1_over": p1_over(),
            "p2_bg": p2_bg(), "p2_over": p2_over(),
            "c2_base": c2_base(), "c2_hole": c2_hole(), "c2_tearline": c2_tearline(),
            "c2_anno": c2_anno(),
            "p3_bg": p3_bg(), "p3_over": p3_over(),
            "c3_base": c3_base(), "c3_anno": c3_anno(),
            "c4_base": c4_base(), "c4_crack": c4_crack(), "c4_anno": c4_anno(),
            "c5_base": c5_base(), "c5_crack": c5_crack(), "c5_anno": c5_anno(),
            "p4_bg": p4_bg(), "p4_over": p4_over(),
            "c6_base": c6_base(), "c6_anno": c6_anno(),
            "c7_base": c7_base()}
    for k, svg in jobs.items():
        p = out / f"{k}.png"
        if p.exists() and not force:
            continue
        render.png(page(svg), p, W, H)
        print(k, flush=True)
    # 字幕帯。1カットぶんを縦に積んで1枚にする（Chrome起動を増やさないため）
    for cid, rows in SUBS.items():
        p = out / f"sub_{cid}.png"
        if p.exists() and not force:
            continue
        h = SUB_H * len(rows)
        render.png(page(sub_strip([r["text"] for r in rows]), W, h), p, W, h)
        print(f"sub_{cid} ({len(rows)}行)", flush=True)
    p = out / "c7_num.png"
    if force or not p.exists():
        cols, rows, cw, ch = 4, 3, W // 2, H // 2
        cells = "".join(
            f'<g transform="translate({(i % cols) * cw},{(i // cols) * ch}) scale(0.5)">'
            f'{c7_num(min(1.0, (i / 11) ** 0.55))}</g>' for i in range(12))
        render.png(page(cells, cw * cols, ch * rows), p, cw * cols, ch * rows)
        print("c7_num", flush=True)
    print("done")


def ensure_css():
    """フォントの base64 は 4MB 超になる。合成側（build_jiko）では不要なので遅延で読む。"""
    global CSS
    if not CSS:
        CSS = (face_css("Dela", "DelaGothicOne.woff2")
               + face_css("Noto", "NotoSansJP-Bold.woff2"))


if __name__ == "__main__":
    ensure_css()
    render_all(force="--force" in sys.argv)
