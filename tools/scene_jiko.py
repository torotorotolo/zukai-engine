# -*- coding: utf-8 -*-
"""事故検証×図解様式のテスト映像。10カット・96.3秒。

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
  全画面の実写4カット＝31.2秒 / 全体96.3秒 = **32.4%**。さらに c2 に写真インセット1点。
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
import re
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
# 🔴 字幕は必須（2026-07-30 カズヤくん指示）。1行ずつ音声を合成して尺を取っているので
#    フレーム精度で音と合う。画面下 y=916 以下は字幕帯として空けてある。
# 🔴 大きさは「考えすぎる葦」を実測して合わせた。
#    Vault `analysis/assets/top10/sheet_*.jpg`（1/4縮小の一覧フレーム）から2通りで測定：
#      ① 字面の高さ 5px × 4 = **20px**（201本の中央値。四分位も20〜20で安定）
#      ② 1文字の幅  約5.8px × 4 = **23px**
#    → フォントサイズ **26px**（1080に対して2.4%）。4巡目の46pxは約2倍だった。
#    葦の文字は **細く・小さく・箱なし**、**2行まで**。太字＋帯は使わない。
#    葦は全編ベクター画面だがこちらは実写に重ねるので、箱の代わりにごく弱い影だけ敷く。
# ⚠️ 字幕を3秒以下に細切れにするのは**2026-07-30に不採用**（見にくいと判定された）。
#    静止禁止は図とグラフの動きで満たす。字幕は自然な文の単位で切る。
SUB_Y, SUB_H = 916, 120
SUB_SIZE = 26
# 🔴 2026-07-30：**横長1列のほうがスッキリする**とのカズヤくん判定で 22→34 に。
#    台本の最長は31字なので実質1行に収まる（26px×31字≒806px で1920に余裕）。
SUB_WRAP = 34            # これを超えたときだけ2行に折る
XML = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def esc(t):
    return "".join(XML.get(c, c) for c in t)


def wrap2(text):
    """長い字幕は**2行まで**に折る（葦も2行までしか使っていない）。
    折る位置は読点。無ければ中央付近の文字境界。"""
    if len(text) <= SUB_WRAP:
        return [text]
    mid = len(text) // 2
    cands = [m.end() for m in re.finditer("[、。]", text) if 4 <= m.end() <= len(text) - 3]
    cut = min(cands, key=lambda i: abs(i - mid)) if cands else mid
    return [text[:cut], text[cut:]]


def sub_row(text, w=W, h=SUB_H):
    """字幕1枚。**箱も帯も敷かない**（葦式）。影だけで実写の上の可読性を持たせる。
    1行なら下寄せ、2行なら上下に振り分ける。**最終行の位置を揃える**のが読みやすさの要。"""
    lines = wrap2(text)
    ys = [h * 0.72] if len(lines) == 1 else [h * 0.42, h * 0.80]
    g = []
    for t, y in zip(lines, ys):
        e = esc(t)
        g.append(f'<text x="{w / 2 + 2:.0f}" y="{y + 2:.0f}" font-family="NotoM" '
                 f'font-size="{SUB_SIZE}" fill="{J.BG}" opacity="0.62" '
                 f'text-anchor="middle">{e}</text>'
                 f'<text x="{w / 2:.0f}" y="{y:.0f}" font-family="NotoM" '
                 f'font-size="{SUB_SIZE}" fill="{J.INK_W}" opacity="0.92" '
                 f'text-anchor="middle">{e}</text>')
    return "".join(g)


def sub_strip(lines):
    """1カットぶんの字幕を縦に積んだ帯。合成時に行ごとに切り出す。"""
    return "".join(f'<g transform="translate(0,{i * SUB_H})">{sub_row(t)}</g>'
                   for i, t in enumerate(lines))


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


def p1_lab():
    """写真の枠と出典。図そのものの情報なので**カット頭から出す**。"""
    x, y, w, h = P1_BOX
    return photo_frame(x, y, w, h, CR_NTSB)


def p1_a1():
    """1行目「1988年4月28日。ハワイ上空、高度7300メートル。」に合わせる。"""
    return J.label(1310, 330, "高度 7,300 m を巡航中", J.INK_W, 34)


def p1_a2():
    """2行目「飛行中の旅客機から、屋根が消えた。」に合わせる。"""
    g = [J.leader(560, 430, 1290, 452, J.ALERT),
         J.label(1310, 440, "客室の天井と外板が", J.ALERT, 42),
         J.label(1310, 490, "5.5 m にわたって消失", J.ALERT, 42),
         J.label(1310, 574, "乗客89人・乗員6人", J.INK_W, 32),
         J.label(1310, 620, "客室乗務員1名が機外へ", J.INK_W, 32)]
    return "".join(g)


# ── p2：実写（事故前の N73711 本人） ──────────────────────
P2_BOX = (900, 268, 880, 598)


def p2_bg():
    return J.frame(W, H) + J.title("この機体は、19年間飛んでいた",
                                   "事故を起こした N73711　1969年製")


def p2_lab():
    x, y, w, h = P2_BOX
    return photo_frame(x, y, w, h, CR_NARA, 23)


def p2_a1():
    """ナレーションは1行だけ。**喋っていない情報だけ**を置く。"""
    g = [J.label(150, 380, "N 7 3 7 1 1", J.AMBER, 62),
         J.label(150, 470, "1969年製", J.LINE, 32),
         J.label(150, 560, "離陸と着陸の回数だけが、", J.INK_W, 32),
         J.label(150, 606, "同型機の倍の速さで積み上がった。", J.INK_W, 32)]
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


def c2_lab():
    """寸法と写真枠。図そのものの情報なので頭から出す。"""
    g = [J.dim(ax(120), ax(249.5), 512, "5.5 m"),
         J.dim(ax(0), ax(720), 822, "全長 30.5 m")]
    x, y, w, h = C2_INSET
    g.append(photo_frame(x, y, w, h, CR_NTSB_S, 24))
    return "".join(g)


def c2_a1():
    """1行目「失われたのは、前方の扉のすぐ後ろから、5.5メートル。」"""
    return (J.leader(ax(185), ay(2), 470, 448, J.ALERT)
            + J.label(190, 396, "剥離した範囲", J.ALERT, 42))


def c2_a2():
    """2行目「天井から窓の下までが、一続きに剥ぎ取られていた。」
    ナレーションが触れない情報（与圧）だけを短く置く。"""
    return (J.label(1330, 706, "与圧された客室の内側は", J.LINE, 28)
            + J.label(1330, 744, "外気より 0.5 気圧ぶん高い", J.LINE, 28))


# ── p3：実写（着陸後の機体を見上げる調査員） ──────────────
P3_BOX = (150, 262, 800, 607)


def p3_bg():
    return J.frame(W, H) + J.title("人と並べると、大きさが分かる",
                                   "マウイ島カフルイ空港に緊急着陸した機体")


def p3_lab():
    x, y, w, h = P3_BOX
    return photo_frame(x, y, w, h, CR_FAA)


def p3_a1():
    """1行目「着陸した機体を、調査員が見上げている。」— 喋っているので置かない。"""
    return ""


def p3_a2():
    """2行目「外板が無くなり、客室の骨組みが、そのまま外に出ていた。」"""
    g = [J.leader(560, 400, 1080, 400, J.ALERT),
         J.label(1100, 388, "剥き出しになった", J.ALERT, 40),
         J.label(1100, 438, "胴体のフレームと床梁", J.ALERT, 40),
         J.label(1100, 540, "この状態で、13分間飛んだ。", J.INK_W, 34)]
    return "".join(g)


# ── c3：胴体断面 ──────────────────────────────────────────

# 断面図の置き場所。3巡目までは中心y=620・R=300で、
# 「事故前／剥離後」のラベルが円の底に被り、字幕帯にも近すぎた。
SEC_CY, SEC_R = 596, 1.30            # → R=260、円は y=336〜856 に収まる


def c3_base():
    g = [J.frame(W, H), J.title("失われたのは、上半分だった", "胴体断面（客室1〜4列目）")]
    for cx in (600, 1400):
        g.append(J.b737_section(cx, SEC_CY, SEC_R, floor=True))
        for dx in (-100, -68, 68, 100):
            g.append(f'<rect x="{cx + dx - 13}" y="{SEC_CY + 38}" width="26" height="40" '
                     f'rx="5" fill="none" stroke="{J.LINE_DIM}" stroke-width="4"/>')
    return "".join(g)


def c3_arc():
    """破断の弧だけ。左から広げると「上部が裂けて広がっていく」動きになる。
    装飾のズームではなく、**円周55%という情報を運ぶ動き**にしたい。"""
    return J.b737_section(1400, SEC_CY, SEC_R, upper=(-165, -15), arc_only=True)


def c3_lab():
    R = 200 * SEC_R
    fy = SEC_CY + R * 0.34
    g = [J.label(600, 306, "事故前", J.LINE, 40, "middle"),
         J.label(1400, 306, "剥離後", J.ALERT, 40, "middle"),
         J.label(600, SEC_CY + 58, "客室", J.LINE, 28, "middle"),
         J.label(600, SEC_CY + 168, "貨物室", J.LINE, 28, "middle"),
         J.label(600 + R * 0.62, fy + 34, "床", J.LINE_DIM, 24, "start"),
         J.dim(600 - R, 600 + R, 250, "3.76 m"),
         J.label(1000, SEC_CY + 14, "→", J.INK_W, 72, "middle")]
    return "".join(g)


def c3_call():
    """「ここが消えた」。**弧が右端まで届いてから**出すので独立させる。"""
    R = 200 * SEC_R
    g = [J.leader(1400 + R * 0.7, SEC_CY - R * 0.72, 1620, 404, J.ALERT),
         J.label(1870, 392, "ここが消えた", J.ALERT, 38, "end"),
         J.label(1870, 438, "円周の約 55%", J.LINE, 28, "end")]
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


def c4_lab():
    """図のラベルと寸法。重ね幅は**縦に測る寸法**（横に引くと図が嘘になる）。"""
    g = [J.label(300, 356, "外板（上）", J.INK_W, 32),
         J.label(300, 900, "外板（下）", J.LINE, 32),
         J.vdim(LJ_Y - 62 * LJ_S, LJ_Y + 62 * LJ_S, LJ_X - 480 * LJ_S - 40, "76 mm")]
    cx = LJ_X + 300 * LJ_S
    g.append(f'<path d="M{cx} 300 V842" stroke="{J.AMBER}" stroke-width="3" '
             f'stroke-dasharray="26 14"/>')
    g.append(J.label(cx, 286, "A", J.AMBER, 34, "middle"))
    g.append(J.label(cx, 872, "A", J.AMBER, 34, "middle"))
    return "".join(g)


def c4_a1():
    """1行目「始まりは、リベット1列の、小さな亀裂だった。」"""
    g = [J.leader(LJ_X + 180, LJ_Y - 40 * LJ_S, 1330, 366, J.ALERT),
         J.label(1350, 352, "最上列のリベット穴から", J.ALERT, 36),
         J.label(1350, 396, "疲労亀裂が発生", J.ALERT, 36)]
    return "".join(g)


def c4_a2():
    """2行目「搭乗する乗客の1人が、この亀裂を見ていた。」— 亀裂のアニメが担う。"""
    return ""


def c4_a3():
    """3行目「だが、誰にも言わなかった。」— 次のカットへの繋ぎだけ。"""
    return (J.label(1350, 500, "この面を A-A で切ると、", J.AMBER, 30)
            + J.label(1350, 540, "なぜ折れたのかが見える", J.AMBER, 30))


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
    """**亀裂だけ**を返す。7巡目までは断面図まるごとの複製だったので、
    脈動させると図全体の濃度が揺れていた。"""
    return J.lap_joint_section(SEC_X, SEC_Y, SEC_S, crack_only=True)


def c5_bond():
    """接着層が**剥がれた**状態。緑の上に灰色を左から重ねると「剥離の進行」になる。
    事故の起点そのものなので、ここは必ず動かす。"""
    return (f'<rect x="{SEC_X - SEC_HL}" y="{SEC_Y - 4 * SEC_S:.0f}" '
            f'width="{SEC_HL * 2:.0f}" height="{8 * SEC_S:.0f}" fill="{J.LINE_DIM}"/>')


def c5_lab():
    """図のラベルと寸法だけ。**ナレーションで喋る内容は書かない。**

    🔴 2026-07-30 カズヤくん指摘：ここは文字が多すぎて、ナレーションと図の
       どちらに集中すべきか分からなくなっていた。数えたら3ブロックが
       ナレーションとほぼ同じ内容の重複だった（「設計では〜分け合うはずだった」
       「潮風の中を19年〜剥がれていた」「荷重の行き場は〜縁だけ」）。
       残すのは ①図の部位名 ②寸法 ③ナレーションが触れない情報 だけ。
    """
    top = SEC_Y - 26 * SEC_S
    bot = SEC_Y + 26 * SEC_S
    g = [J.dim(SEC_X - SEC_HL, SEC_X + SEC_HL, 436, "76 mm"),
         J.label(SEC_X - 640, top - 14, "外板（上）", J.INK_W, 28),
         J.label(SEC_X + 660, bot + 40, "外板（下）", J.LINE, 28, "end")]
    return "".join(g)


def c5_a1():
    """1行目「外板は2枚が重なり、接着とリベットで荷重を分け合う設計だった。」"""
    return (J.leader(SEC_X - SEC_HL - 6, SEC_Y + 10, 560, 690, J.OK)
            + J.label(150, 706, "接着層", J.OK, 40))


def c5_a2():
    """2行目「その接着が、潮風の中で剥がれていた。」— 剥離のアニメが担う。"""
    return ""


def c5_a3():
    """3行目「荷重の行き場は、リベット穴の縁だけになった。」
    ナレーションが触れない「皿もみ」と「段差」だけを置く。"""
    top = SEC_Y - 26 * SEC_S
    g = [J.leader(SEC_X - 62 * SEC_S, top + 6, 620, 372, J.ALERT),
         J.label(150, 300, "皿もみの縁は、刃のように薄い", J.ALERT, 34),
         J.leader(SEC_X + SEC_HL, SEC_Y, 1330, 360, J.AMBER),
         J.label(1350, 348, "段差", J.AMBER, 38)]
    return "".join(g)


# ── p4：実写（航路・NASA） ────────────────────────────────
P4_BOX = (1030, 250, 760, 591)


def p4_bg():
    return J.frame(W, H) + J.title("ヒロを出て、ホノルルへ向かっていた",
                                   "アロハ航空243便の航路　ハワイ諸島")


def p4_lab():
    x, y, w, h = P4_BOX
    return photo_frame(x, y, w, h, CR_NASA)


def p4_a1():
    """ナレーションは1行。**喋っていない結論だけ**を置く。"""
    g = [J.label(150, 420, "与圧は、そのたびに", J.INK_W, 34),
         J.label(150, 466, "かかっては、抜ける。", J.INK_W, 34),
         J.label(150, 552, "胴体は、そのたびに", J.ALERT, 34),
         J.label(150, 598, "膨らんでは、縮んでいた。", J.ALERT, 34),
         J.label(150, 700, "19年間で 89,680 回。", J.AMBER, 38)]
    return "".join(g)


# ── c6：高度の時系列 ──────────────────────────────────────

PTS = [(0.00, 0.00), (0.13, 0.86), (0.30, 0.92), (0.36, 0.92),
       (0.41, 0.60), (0.57, 0.28), (0.78, 0.09), (1.00, 0.00)]


def c6_base():
    g = [J.frame(W, H), J.title("剥離から着陸まで、13分", "高度の推移")]
    g.append(J.alt_graph(230, 330, 1460, 520, PTS, part="frame"))
    return "".join(g)


def c6_line():
    """折れ線だけ。**左から描いていく**（最初から全部出ていると動きが無い）。"""
    return J.alt_graph(230, 330, 1460, 520, PTS, part="line")


def c6_mark():
    return J.alt_graph(230, 330, 1460, 520, PTS, mark=3, part="mark")


def c6_lab():
    g = [J.label(210, 350, "7,300 m", J.AMBER, 30, "end"),
         J.label(210, 592, "3,600 m", J.LINE_DIM, 26, "end"),
         J.label(210, 856, "0", J.AMBER, 30, "end"),
         J.label(230, 884, "離陸　ヒロ", J.LINE, 28),
         J.label(1690, 884, "着陸　マウイ島カフルイ", J.LINE, 28, "end")]
    return "".join(g)


def c6_a1():
    """1行目「剥離から着陸まで、13分。」"""
    mx = 230 + 1460 * 0.36
    return J.dim(mx, 1690, 846, "13分") + J.label(660, 640, "緊急降下", J.INK_W, 34)


def c6_a2():
    """2行目「操縦室の扉も吹き飛び、機長は、客室の空を、直接見ていた。」
    喋る内容は書かず、位置を示すラベルだけ置く。"""
    mx = 230 + 1460 * 0.36
    return (J.leader(mx, 330 + 520 * 0.08, 1120, 250, J.ALERT)
            + J.label(1140, 238, "ここで剥離", J.ALERT, 38))


# ── c7：数字 ──────────────────────────────────────────────

def c7_base():
    g = [J.frame(W, H), J.title("設計の想定を、超えて飛んでいた",
                                "離着陸の回数（NTSB報告書 1.17.2 節）")]
    g.append(f'<path d="M960 330 V900" stroke="{J.LINE_DIM}" stroke-width="4"/>')
    g.append(J.label(960, 862, "1969年製・19年間・ハワイ諸島間の短距離を1日十数往復",
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
    jobs = {"p1_bg": p1_bg(), "p1_lab": p1_lab(), "p1_a1": p1_a1(), "p1_a2": p1_a2(),
            "p2_bg": p2_bg(), "p2_lab": p2_lab(), "p2_a1": p2_a1(),
            "c2_base": c2_base(), "c2_hole": c2_hole(), "c2_tearline": c2_tearline(),
            "c2_lab": c2_lab(), "c2_a1": c2_a1(), "c2_a2": c2_a2(),
            "p3_bg": p3_bg(), "p3_lab": p3_lab(), "p3_a2": p3_a2(),
            "c3_base": c3_base(), "c3_arc": c3_arc(), "c3_lab": c3_lab(),
            "c3_call": c3_call(),
            "c4_base": c4_base(), "c4_crack": c4_crack(), "c4_lab": c4_lab(),
            "c4_a1": c4_a1(), "c4_a3": c4_a3(),
            "c5_base": c5_base(), "c5_crack": c5_crack(), "c5_bond": c5_bond(),
            "c5_lab": c5_lab(), "c5_a1": c5_a1(), "c5_a3": c5_a3(),
            "p4_bg": p4_bg(), "p4_lab": p4_lab(), "p4_a1": p4_a1(),
            "c6_base": c6_base(), "c6_line": c6_line(), "c6_mark": c6_mark(),
            "c6_lab": c6_lab(), "c6_a1": c6_a1(), "c6_a2": c6_a2(),
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
               + face_css("Noto", "NotoSansJP-Bold.woff2")
               + face_css("NotoM", "NotoSansJP-Medium.woff2"))


if __name__ == "__main__":
    ensure_css()
    render_all(force="--force" in sys.argv)
