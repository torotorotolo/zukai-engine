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
# 🔴 2026-07-30：1.5倍だと全長1080pxで右に670pxの余白が残っていた。
#    インセット写真の手前（x=1242）まで使い切る 1.62倍にする。
#    縦は 垂直尾翼の頂点 y=367 ／ 主脚の下端 y=787 で、本体の枠(210〜892)に収まる。
AC_X, AC_Y, AC_S = 76, 596, 1.62

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
    """写真の枠と出典。**出典は必ず画面に出す。**

    🔴 2026-07-30：出典を写真の**下40px**に置いていたので、写真の下に必ず
       高さ60pxほどの帯状の余白ができていた（10カット全部）。
       写真の**内側の下端**に暗い帯を敷いて載せる。テレビのクレジットと同じ置き方で、
       どの写真の出典かも曖昧にならない。写真の箱はそのぶん下まで伸ばせる。
    """
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" '
         f'stroke="{J.LINE}" stroke-width="6"/>']
    for cx, cy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        g.append(f'<path d="M{cx - 26} {cy} h52 M{cx} {cy - 26} v52" stroke="{J.INK_W}" '
                 f'stroke-width="6"/>')
    ch = size + 22
    g.append(f'<rect x="{x + 3}" y="{y + h - ch - 3}" width="{w - 6}" height="{ch}" '
             f'fill="{J.BG}" opacity="0.72"/>')
    g.append(J.label(x + 16, y + h - 16, credit, J.LINE, size))
    return "".join(g)


# ── 実写カットの型（2026-07-30 に作り直した） ─────────────
# 写真は **本体の高さ 682px を必ず使い切る**。反対側に幅632pxの「情報柱」を立て、
# 柱の中も y=270〜880 を使い切るようにブロックを配置する。
# 文字は 14巡目の 32〜42px から **大注記 52〜56px・事実 42px・数値 Dela 92〜104px** に上げた。
PH_L = (J.MG, J.BAND_T, J.PHOTO_W, J.PHOTO_H)                 # 写真を左に置く型
PH_R = (J.RIGHT - J.PHOTO_W, J.BAND_T, J.PHOTO_W, J.PHOTO_H)  # 写真を右に置く型
CR, CL = J.COL_R[0], J.COL_L[0]        # 情報柱の左端（右柱=1216 ／ 左柱=72）


# ── p1：実写（事故機の左側面）＋右の情報柱 ────────────────
P1_BOX = PH_L


def p1_bg():
    """写真の下に敷く地。**注記は別レイヤーにする**（初稿は注記側にも背景を塗って写真が消えた）。"""
    return (J.frame(W, H) + J.title("飛行中に、屋根が消えた",
                                   "アロハ航空243便　1988年4月28日　ボーイング737-200")
            + J.chapter(1, 6, "何が起きたか"))


def p1_lab():
    """写真の枠と出典。図そのものの情報なので**カット頭から出す**。"""
    x, y, w, h = P1_BOX
    return photo_frame(x, y, w, h, CR_NTSB)


def p1_a1():
    """1行目「1988年4月28日。ハワイ上空、高度7300メートル。」に合わせる。"""
    return (J.label(CR, 272, "巡航高度", J.LINE, 32)
            + J.big(CR, 376, "7,300 m", J.AMBER, 96)
            + J.rule(CR, J.RIGHT, 424, J.ALERT))


def p1_a2():
    """2行目「飛行中の旅客機から、屋根が消えた。」に合わせる。

    赤字は 42→56px。柱の幅632pxに対して「5.5 m にわたって消失」でちょうど埋まる。
    """
    g = [J.leader(502, 408, 1206, 478, J.ALERT),
         J.label(CR, 498, "客室の天井と外板が", J.ALERT, 56),
         J.label(CR, 566, "5.5 m にわたって消失", J.ALERT, 56),
         J.label(CR, 672, "乗客89人・乗員6人", J.INK_W, 42),
         J.label(CR, 726, "客室乗務員1名が機外へ", J.INK_W, 42),
         J.rule(CR, J.RIGHT, 780, J.LINE_DIM, 3),
         J.label(CR, 846, "乗員乗客95人のうち", J.ALERT, 40),
         J.label(CR, 890, "94人が生き延びた", J.ALERT, 40)]
    return "".join(g)


# ── p2：実写（事故前の N73711 本人）＋左の情報柱 ──────────
P2_BOX = PH_R


def p2_bg():
    return (J.frame(W, H) + J.title("この機体は、19年間飛んでいた",
                                   "事故を起こした N73711　1969年製")
            + J.chapter(2, 6, "どの機体だったか"))


def p2_lab():
    x, y, w, h = P2_BOX
    return photo_frame(x, y, w, h, CR_NARA, 23)


def p2_a1():
    """ナレーションは1行だけ。**喋っていない情報だけ**を置く。

    「N 7 3 7 1 1」を字間で伸ばしていたのを Dela 100px の1語に変えた。
    登録記号は機体の身元そのものなので、ここがこのカットの主役でよい。
    """
    g = [J.label(CL, 272, "機体記号", J.LINE, 32),
         J.big(CL, 366, "N73711", J.AMBER, 100),
         J.label(CL, 416, "1969年製　ボーイング737-200", J.LINE, 32),
         J.rule(CL, J.COL_L[1], 456, J.ALERT),
         J.label(CL, 530, "離陸と着陸の回数だけが、", J.ALERT, 48),
         J.label(CL, 588, "同型機の倍の速さで", J.ALERT, 48),
         J.label(CL, 646, "積み上がっていた。", J.ALERT, 48),
         J.rule(CL, J.COL_L[1], 700, J.LINE_DIM, 3),
         J.label(CL, 762, "世界の737のなかで", J.INK_W, 38),
         J.label(CL, 810, "離着陸の回数は2番目に多い", J.INK_W, 38),
         J.label(CL, 878, "ヒロ発ホノルル行き 243便", J.LINE, 32)]
    return "".join(g)


# ── c2：機体側面図（＋写真インセット） ────────────────────
# 1巡目の粗を全部直した：
#   引き出し線が機体を横断していた → 注記は機体の上下に置き、線を短くする
#   5.5m 寸法が図から離れて浮いていた → 剥離範囲の真上に降ろす
#   目盛線が胴体の上を通っていた → 機体より先に描いて下に潜らせる
#   胴体直径の注記が機体を跨いでいた → **断面図(c3)に任せて c2 からは外す**
C2_INSET = (1288, 236, 560, 430)


def c2_base():
    g = [J.frame(W, H), J.title("消えたのは、前方扉のすぐ後ろから",
                                "ボーイング737-200　側面図（NTSB調査資料の三面図から作図）")
            + J.chapter(3, 6, "どこが失われたか")]
    # 機首からの距離。**実在しない station 番号を振ると図が嘘になる**ので、
    # 実測できる「機首からの m」で目盛る（全長30.53m = 720単位）。
    for m in range(0, 31, 5):
        u = m * 720 / 30.53
        g.append(f'<path d="M{ax(u):.0f} 356 V800" stroke="{J.GRID}" stroke-width="2.4"/>')
        # 0m の目盛だけ中央寄せにすると左端が画面の余白(72)より外に出る
        g.append(J.label(ax(u), 836, f"{m} m", J.LINE_DIM, 24,
                         "start" if m == 0 else "middle"))
    g.append(J.b737_side(AC_X, AC_Y, AC_S))
    return "".join(g)


def c2_hole():
    return J.b737_tear(AC_X, AC_Y, AC_S, part="hole")


def c2_tearline():
    return J.b737_tear(AC_X, AC_Y, AC_S, part="line")


def c2_lab():
    """寸法と写真枠。図そのものの情報なので頭から出す。"""
    # ⚠️ 18巡目：5.5m を y=330 に置いたら測っている剥離部（y=596）から267px離れて浮き、
    #    19巡目に y=552 まで降ろしたら**上の帯 1240×160px が空いた**。
    #    → 製図の作法どおり、寸法線は上に置いて**寸法補助線で剥離部まで繋ぐ**。
    #      これで「何を測っているか分かる」と「帯が埋まる」を両立できる。
    g = [J.dim(ax(120), ax(249.5), 330, "5.5 m", ext=254),
         J.dim(ax(0), ax(720), 878, "全長 30.5 m")]
    x, y, w, h = C2_INSET
    g.append(photo_frame(x, y, w, h, CR_NTSB_S, 24))
    return "".join(g)


def c2_a1():
    """1行目「失われたのは、前方の扉のすぐ後ろから、5.5メートル。」

    剥離範囲は寸法線の上に注記を置く（14巡目は機体の左の空きに置いて線が長かった）。
    ⚠️ 引き出し線は**やめた**。15巡目は「5.5 m」寸法線の白抜きを横切り、16巡目に
       左へ逃がしても隙間が7pxしか無く、寸法線を剥離部の近くに降ろすと必ずぶつかる。
       **寸法線そのものが指し棒**（矢羽根が剥離部の x 範囲を正確に挟んでいる）なので、
       注記を寸法線の真上に積めば引き出し線は要らない。交差の危険も永久に無くなる。
    """
    return J.label((ax(120) + ax(249.5)) / 2, 288, "剥離した範囲", J.ALERT, 52, "middle")


def c2_a2():
    """2行目「天井から窓の下までが、一続きに剥ぎ取られていた。」
    ナレーションが触れない情報（与圧）だけを置く。インセット写真の下の空きを使う。

    ⚠️ 15巡目の「この差が、外板を内側から押す」は c5 の「内側から外へ押す力」と
       同じことを言っていた。報告書の原記述（約18 ft）に差し替える。
    """
    g = [J.label(1288, 716, "客室と外気の圧力差", J.LINE, 30),
         J.big(1288, 800, "0.5 気圧", J.AMBER, 78),
         J.label(1288, 858, "報告書の記録は 約18 フィート", J.LINE, 32)]
    return "".join(g)


# ── p3：実写（着陸後の機体を見上げる調査員）＋右の情報柱 ──
P3_BOX = PH_L


def p3_bg():
    return (J.frame(W, H) + J.title("人と並べると、大きさが分かる",
                                   "マウイ島カフルイ空港に緊急着陸した機体")
            + J.chapter(3, 6, "どこが失われたか"))


def p3_lab():
    x, y, w, h = P3_BOX
    return photo_frame(x, y, w, h, CR_FAA)


def p3_a1():
    """1行目「着陸した機体を、調査員が見上げている。」

    14巡目は空だった。このカットの主題は**大きさ**なので、
    喋っていない胴体径をここで出すと、写真の人と数字が噛み合う。
    """
    return (J.label(CR, 272, "胴体の直径", J.LINE, 32)
            + J.big(CR, 376, "3.76 m", J.AMBER, 96)
            + J.label(CR, 424, "人の背丈の2倍を超える", J.LINE, 32)
            + J.rule(CR, J.RIGHT, 464, J.ALERT))


def p3_a2():
    """2行目「外板が無くなり、客室の骨組みが、そのまま外に出ていた。」"""
    g = [J.leader(700, 424, 1206, 528, J.ALERT),
         J.label(CR, 546, "剥き出しになった", J.ALERT, 54),
         J.label(CR, 608, "胴体のフレームと床梁", J.ALERT, 54),
         J.rule(CR, J.RIGHT, 666, J.LINE_DIM, 3),
         J.label(CR, 732, "この状態で、13分間飛んだ。", J.INK_W, 44),
         # NTSB報告書の「客室床面より上」という記述をそのまま図の言葉にする。
         # どのナレーションも触れていないのに、機体が折れなかった理由に直結する。
         J.label(CR, 830, "破断は客室の床面で止まり、", J.LINE, 34),
         J.label(CR, 874, "床より下の外板は残った。", J.LINE, 34)]
    return "".join(g)


# ── c3：胴体断面 ──────────────────────────────────────────

# 断面図の置き場所。
# 🔴 2026-07-30：円が中空で内側の 580px 角が余白に見えていた。
#    ① `b737_section(inside=True)` で客室と貨物室を面として塗り分け、座席を 3-3 で入れた
#    ② 円を R=290→296 に上げ、中心を左右に開いて（520 / 1360）左右の余白を減らした
#    本体の枠 210〜892 に対して円は y=290〜882。
SEC_CY, SEC_R = 586, 1.48            # → R=296
# 16巡目は 520 / 1360 で左に 224px の帯が空いていた（最大の空き 8.5%）。左へ寄せる
SEC_L, SEC_RT = 460, 1330            # 左（事故前）と右（剥離後）の中心x


def c3_base():
    g = [J.frame(W, H), J.title("失われたのは、上半分だった", "胴体断面（客室1〜4列目）")
            + J.chapter(3, 6, "どこが失われたか")]
    for cx in (SEC_L, SEC_RT):
        g.append(J.b737_section(cx, SEC_CY, SEC_R, floor=True))
    return "".join(g)


def c3_arc():
    """破断の弧だけ。左から広げると「上部が裂けて広がっていく」動きになる。
    装飾のズームではなく、**円周55%という情報を運ぶ動き**にしたい。"""
    return J.b737_section(SEC_RT, SEC_CY, SEC_R, upper=(-165, -15), arc_only=True)


def c3_lab():
    R = 200 * SEC_R
    fy = SEC_CY + R * 0.34
    g = [J.label(SEC_L, 262, "事故前", J.LINE, 46, "middle"),
         J.label(SEC_RT, 262, "剥離後", J.ALERT, 46, "middle"),
         J.label(SEC_L, SEC_CY - R * 0.60, "客室", J.INK_W, 34, "middle"),
         J.label(SEC_L, fy + R * 0.36, "貨物室", J.LINE, 34, "middle"),
         # 🔴 0.90R では円周の線に被り、0.72R では**座席の上に乗った**（18巡目）。
         #    座席は床の上に並ぶので、床のラベルは**床の線の下（貨物室側）**に置くしかない。
         J.label(SEC_L - R * 0.86, fy + 36, "床", J.LINE, 28),
         J.dim(SEC_L - R, SEC_L + R, 316, "3.76 m"),
         J.label((SEC_L + SEC_RT) // 2, SEC_CY + 14, "→", J.INK_W, 76, "middle")]
    return "".join(g)


def c3_call():
    """「ここが消えた」。**弧が右端まで届いてから**出すので独立させる。

    ⚠️ 14巡目は「円周の約 55%」と書いていたが、これはナレーションが
       「円周の、およそ55パーセント」とそのまま喋っている＝ルール違反だった。削除。
       代わりに、どのナレーションも触れていない「座席が外気に出た」を置く。
    """
    R = 200 * SEC_R
    g = [J.leader(SEC_RT + R * 0.70, SEC_CY - R * 0.70, 1650, 330, J.ALERT),
         J.label(J.RIGHT, 318, "ここが消えた", J.ALERT, 46, "end"),
         J.label(J.RIGHT, 848, "1〜4列目の座席が、", J.LINE, 32, "end"),
         J.label(J.RIGHT, 888, "そのまま外気に出た。", J.LINE, 32, "end")]
    return "".join(g)


# ── c4：重ね継手の平面図 ──────────────────────────────────

# 🔴 2026-07-30：0.95倍だと板が 912×475px で、右に 720×520px の穴が空いていた。
#    `lap_joint` の伸びを 250→290 単位にして板の縦を 302〜858 まで伸ばし、
#    右に幅602pxの情報柱を立てた。
# ⚠️ 左端をこれ以上詰められない理由：76mm の縦寸法線は文字を線の**左**に出すので、
#    板の左端から 150px ほどの逃げが要る（詰めすぎると「76 mm」が画面外に切れる）。
#    その逃げに「外板（上）（下）」のラベルを入れて、空きにしないでおく。
LJ_X, LJ_Y, LJ_S = 740, 580, 0.96
C4_COL = 1246


def c4_base():
    g = [J.frame(W, H), J.title("始まりは、リベット1列の亀裂",
                                "外板の重ね継手（ラップジョイント）を外から見た図")
            + J.chapter(4, 6, "なぜ壊れたのか")]
    g.append(J.lap_joint(LJ_X, LJ_Y, LJ_S, cracks=0))
    return "".join(g)


def c4_crack():
    return J.lap_joint(LJ_X, LJ_Y, LJ_S, cracks=15, only_cracks=True)


def c4_lab():
    """図のラベルと寸法。重ね幅は**縦に測る寸法**（横に引くと図が嘘になる）。"""
    g = [J.label(J.MG + 18, 344, "外板（上）", J.INK_W, 36),
         J.label(J.MG + 18, 830, "外板（下）", J.LINE, 36),
         J.vdim(LJ_Y - 62 * LJ_S, LJ_Y + 62 * LJ_S, LJ_X - 480 * LJ_S - 44, "76 mm")]
    cx = LJ_X + 300 * LJ_S
    g.append(f'<path d="M{cx} 286 V874" stroke="{J.AMBER}" stroke-width="3" '
             f'stroke-dasharray="26 14"/>')
    g.append(J.label(cx, 272, "A", J.AMBER, 38, "middle"))
    g.append(J.label(cx, 902, "A", J.AMBER, 38, "middle"))
    return "".join(g)


def c4_a1():
    """1行目「始まりは、リベット1列の、小さな亀裂だった。」"""
    g = [J.leader(LJ_X + 200, LJ_Y - 40 * LJ_S, C4_COL - 10, 388, J.ALERT),
         J.label(C4_COL, 368, "最上列のリベット穴から", J.ALERT, 46),
         J.label(C4_COL, 424, "疲労亀裂が発生", J.ALERT, 46),
         J.rule(C4_COL, J.RIGHT, 470, J.ALERT)]
    return "".join(g)


def c4_a2():
    """2行目「搭乗する乗客の1人が、この亀裂を見ていた。」

    14巡目は空だった。亀裂のアニメだけでは柱の中段が空くので、
    **喋っていない継手そのものの作り**をここで出す。
    """
    g = [J.label(C4_COL, 556, "重ね幅 76 mm に", J.INK_W, 40),
         J.label(C4_COL, 608, "リベットが3列", J.INK_W, 40),
         J.label(C4_COL, 684, "外板の厚さは 0.91 mm", J.LINE, 34),
         J.rule(C4_COL, J.RIGHT, 730, J.LINE_DIM, 3)]
    return "".join(g)


def c4_a3():
    """3行目「だが、誰にも言わなかった。」— 次のカットへの繋ぎだけ。"""
    return (J.label(C4_COL, 800, "この面を A-A で切ると、", J.AMBER, 38)
            + J.label(C4_COL, 856, "なぜ折れたのかが見える", J.AMBER, 38))


# ── c5：重ね継手の A-A 断面 ───────────────────────────────
# 1巡目は図が小さく、引き出し線が図を横断し、下1/3が空いていた。
# 図を大きくして中央に据え、注記は**図の上下の空きに置いて線を短くする**。
# 🔴 2026-07-30：それでも図は高さ120pxの細い帯で、上下に合わせて400pxの余白が残っていた
#    （最大の空き矩形 16.7%＝全カット中で最悪）。2つ直した：
#      ① 板厚の誇張を 26→44 単位に上げ、横の伸びを 300→260 に詰めて図を「厚い」形にした
#      ② 図の上下を**「外気側」と「客室側」の面**にした。空きを塗りで埋めたのではなく、
#         どちらが外でどちらが客室かは断面図で必ず要る情報。
#         客室側から外へ向かう矢印＝与圧が外板を押す力そのもので、事故の因果に直結する。
SEC_X, SEC_Y, SEC_S = 960, 560, 2.25
SEC_HL = 95 * SEC_S          # 重ね幅の半分（画面px）
SEC_T = 44 * SEC_S           # 板厚（誇張）1枚ぶん = 99px
C5_OUT = (J.BAND_T, SEC_Y - SEC_T - 8)        # 外気側の帯 210〜453
C5_IN = (SEC_Y + SEC_T + 8, J.BAND_B)         # 客室側の帯 667〜892


def c5_base():
    g = [J.frame(W, H), J.title("荷重を分け合う相手が、いなくなった",
                                "重ね継手 A-A 断面（板厚 0.91 mm。図では誇張している）")
            + J.chapter(4, 6, "なぜ壊れたのか")]
    # 外気側／客室側の面。断面図では「どちらが外か」が必ず要る
    # 15巡目は 0.07 / 0.08 で外気側の帯がほとんど見えなかった（面として読めない）
    g.append(J.tone(J.MG, C5_OUT[0], J.RIGHT - J.MG, C5_OUT[1] - C5_OUT[0], J.LINE, 0.11))
    g.append(J.tone(J.MG, C5_IN[0], J.RIGHT - J.MG, C5_IN[1] - C5_IN[0], J.AMBER, 0.13))
    # 与圧が客室側から外板を押す力。矢印を等間隔に立てる（実際に働いている力）
    for i in range(5):
        px = 450 + i * 225
        g.append(f'<path d="M{px} 884 V744 m-14 20 l14 -20 l14 20" fill="none" '
                 f'stroke="{J.AMBER}" stroke-width="4" opacity="0.55" '
                 f'stroke-linejoin="round"/>')
    g.append(J.lap_joint_section(SEC_X, SEC_Y, SEC_S, crack=False))
    return "".join(g)


def c5_crack():
    """**亀裂だけ**を返す。7巡目までは断面図まるごとの複製だったので、
    脈動させると図全体の濃度が揺れていた。"""
    return J.lap_joint_section(SEC_X, SEC_Y, SEC_S, crack_only=True)


def c5_bond():
    """接着層が**剥がれた**状態。緑の上に灰色を左から重ねると「剥離の進行」になる。
    事故の起点そのものなので、ここは必ず動かす。"""
    # ⚠️ 接着層の厚みを 12→18 単位にしたとき、ここを直し忘れて
    #    剥がれた灰色の上下に緑が縁として残っていた（17巡目の拡大で発覚）。
    #    **jiko_style の接着層と必ず同じ高さにする。**
    return (f'<rect x="{SEC_X - SEC_HL}" y="{SEC_Y - 9 * SEC_S:.0f}" '
            f'width="{SEC_HL * 2:.0f}" height="{18 * SEC_S:.0f}" fill="{J.LINE_DIM}"/>')


def c5_lab():
    """図のラベルと寸法だけ。**ナレーションで喋る内容は書かない。**

    🔴 2026-07-30 カズヤくん指摘：ここは文字が多すぎて、ナレーションと図の
       どちらに集中すべきか分からなくなっていた。数えたら3ブロックが
       ナレーションとほぼ同じ内容の重複だった（「設計では〜分け合うはずだった」
       「潮風の中を19年〜剥がれていた」「荷重の行き場は〜縁だけ」）。
       残すのは ①図の部位名 ②寸法 ③ナレーションが触れない情報 だけ。
    """
    # ⚠️ 部位名は**帯の中（地の上）に置く**。板の上に載せると
    #    上の外板は INK_W の明るい塗りなので INK_W の文字が消える。
    # 76mm の寸法線は 406→380 に上げた。15巡目は「皿もみ」の引き出し線が
    # 寸法線の左の矢羽根(x=746)を2pxだけ避けて通っていて、拡大すると触っていた。
    g = [J.dim(SEC_X - SEC_HL, SEC_X + SEC_HL, 380, "76 mm"),
         J.label(J.MG + 18, 252, "機体の外側（外気）", J.LINE, 38),
         J.label(176, 445, "外板（上）", J.INK_W, 34),
         J.label(J.MG + 18, 706, "客室の内側（与圧）", J.AMBER, 38),
         J.label(1500, 706, "外板（下）", J.LINE, 34),
         J.label(J.RIGHT, 800, "内側から外へ押す力", J.AMBER, 32, "end")]
    return "".join(g)


def c5_a1():
    """1行目「外板は2枚が重なり、接着とリベットで荷重を分け合う設計だった。」

    引き出し線は**ラベルの文字の端まで引く**。13巡目は線の終点とラベルが
    280px 離れていて、線が浮いて見えた。
    """
    return (J.leader(SEC_X - SEC_HL + 20, SEC_Y, 250, 786, J.OK)
            + J.label(J.MG + 18, 800, "接着層", J.OK, 48))


def c5_a2():
    """2行目「その接着が、潮風の中で剥がれていた。」— 剥離のアニメが担う。"""
    return ""


def c5_a3():
    """3行目「荷重の行き場は、リベット穴の縁だけになった。」
    ナレーションが触れない「皿もみ」と「段差」だけを置く。"""
    g = [J.leader(SEC_X - 62 * SEC_S, SEC_Y - SEC_T + 10, 640, 286, J.ALERT),
         J.label(J.MG + 18, 300, "皿もみの縁は、刃のように薄い", J.ALERT, 42),
         # 段差の起点は接着層の右端ではなく**上の外板の切り口の面**を指す。
         # 16巡目は y=SEC_Y に打っていたので、緑の接着層の右端に丸が乗っていた。
         J.leader(SEC_X + SEC_HL, SEC_Y - SEC_T * 0.5, 1490, 328, J.AMBER),
         J.label(1500, 342, "段差", J.AMBER, 46)]
    return "".join(g)


# ── p4：実写（航路・NASA）＋左の情報柱 ───────────────────
P4_BOX = PH_R


def p4_bg():
    return (J.frame(W, H) + J.title("ヒロを出て、ホノルルへ向かっていた",
                                   "アロハ航空243便の航路　ハワイ諸島")
            + J.chapter(5, 6, "19年で積み上がったもの"))


def p4_lab():
    x, y, w, h = P4_BOX
    return photo_frame(x, y, w, h, CR_NASA)


def p4_a1():
    """ナレーションは1行。**喋っていない結論だけ**を置く。

    14巡目は 34px で柱の下半分が空いていた。44px に上げ、
    回数は Dela の大きな数字にして柱の底まで使う。
    """
    g = [J.label(CL, 290, "与圧は、そのたびに", J.INK_W, 44),
         J.label(CL, 346, "かかっては、抜ける。", J.INK_W, 44),
         J.label(CL, 442, "胴体は、そのたびに", J.ALERT, 44),
         J.label(CL, 498, "膨らんでは、縮んでいた。", J.ALERT, 44),
         J.rule(CL, J.COL_L[1], 556, J.ALERT),
         J.label(CL, 626, "19年間の離着陸", J.LINE, 34),
         J.big(CL, 736, "89,680 回", J.AMBER, 100),
         J.label(CL, 812, "1回ごとに、亀裂は", J.LINE, 34),
         J.label(CL, 856, "わずかに伸びていく。", J.LINE, 34)]
    return "".join(g)


# ── c6：高度の時系列 ──────────────────────────────────────

PTS = [(0.00, 0.00), (0.13, 0.86), (0.30, 0.92), (0.36, 0.92),
       (0.41, 0.60), (0.57, 0.28), (0.78, 0.09), (1.00, 0.00)]


# グラフの枠。🔴 2026-07-30：1460×520 で右に 230px・下に 160px 余っていた。
# 目盛ラベルの逃げ（左140px）だけ残して、残りは全部グラフにする。
# 16巡目は上端が 288 で、副題(y=182)との間に 1920×120px の帯が空いていた
GX, GY, GW, GH = 246, 248, 1544, 596       # → x 246〜1790, y 248〜844


def c6_base():
    g = [J.frame(W, H),
         J.title("剥離から着陸まで、13分",
                 "高度の推移（NTSB報告書の飛行記録から作図）")
         + J.chapter(5, 6, "19年で積み上がったもの")]
    g.append(J.alt_graph(GX, GY, GW, GH, PTS, part="frame"))
    return "".join(g)


def c6_line():
    """折れ線だけ。**左から描いていく**（最初から全部出ていると動きが無い）。"""
    return J.alt_graph(GX, GY, GW, GH, PTS, part="line")


def c6_mark():
    return J.alt_graph(GX, GY, GW, GH, PTS, mark=3, part="mark")


def c6_lab():
    g = [J.label(GX - 20, GY + 22, "7,300 m", J.AMBER, 32, "end"),
         J.label(GX - 20, GY + GH * 0.507, "3,600 m", J.LINE_DIM, 28, "end"),
         J.label(GX - 20, GY + GH + 8, "0", J.AMBER, 32, "end"),
         J.label(GX, GY + GH + 46, "離陸　ヒロ", J.LINE, 30),
         J.label(GX + GW, GY + GH + 46, "着陸　マウイ島カフルイ", J.LINE, 30, "end")]
    return "".join(g)


def c6_a1():
    """1行目「剥離から着陸まで、13分。」"""
    mx = GX + GW * 0.36
    # グラフの左上（折れ線が上がりきる前）が空いていたので巡航区間を名付ける
    return (J.dim(mx, GX + GW, GY + GH - 22, "13分")
            + J.label(700, 660, "緊急降下", J.INK_W, 40)
            + J.label(560, 292, "巡航", J.INK_W, 36))


def c6_a2():
    """2行目「操縦室の扉も吹き飛び、機長は、客室の空を、直接見ていた。」
    喋る内容は書かず、位置を示すラベルだけ置く。"""
    mx = GX + GW * 0.36
    return (J.leader(mx, GY + GH * 0.08, 1160, 372, J.ALERT)
            + J.label(1180, 358, "ここで剥離", J.ALERT, 46)
            + J.label(1180, 418, "与圧を失ったまま降下した", J.LINE, 30))


# ── c7：数字 ──────────────────────────────────────────────

# 🔴 2026-07-30：数字2つが画面の中央に浮いていて、上に 840×440px の穴が空いていた。
#    横棒を足して 1.20 倍という差を面で見せる（字で「1.20倍」と書くしかなかったのが弱点）。
# 🔴 15巡目の事故：数字を 196px に上げたら**左右がくっついて「75,00089,680」に読めた**。
#    Dela の数字は 1文字 0.84em（0.72 と見積もっていた）。「75,000 回」は 196px なら
#    幅 1,100px になり、仕切り線(x=960)の左に収まらない。
#    → 140px に下げ、単位を数字と同じ文字列に入れて（豆腐に見える小さな「回」を廃止）、
#      中心を 500 / 1420 に開いた。左は 108〜892、右は 1028〜1812 で仕切り線を跨がない。
C7_LX, C7_RX = 490, 1430         # 左右の列の中心x
C7_NUM = 168                     # 数字の大きさ（これ以上上げると仕切り線を越える）
C7_BAR = (112, 534, 776, 112)    # 棒の (左端, 上端, 最大長, 高さ)


def c7_base():
    g = [J.frame(W, H), J.title("設計の想定を、超えて飛んでいた",
                                "離着陸の回数（NTSB報告書 1.17.2 節）"),
         J.chapter(6, 6, "設計の想定と実際")]
    g.append(f'<path d="M960 236 V846" stroke="{J.LINE_DIM}" stroke-width="4"/>')
    g.append(J.label(960, 886, "1969年製・19年間・ハワイ諸島間の短距離を1日十数往復",
                     J.LINE, 32, "middle"))
    return "".join(g)


def c7_num(k):
    n = int(89680 * k)
    bx, by, bw, bh = C7_BAR
    g = [J.bignum(C7_LX, 430, "75,000", "", "経済設計寿命（20年）の離着陸回数", J.LINE, C7_NUM),
         J.bignum(C7_RX, 430, f"{n:,}", "", "実際に飛んだ離着陸回数", J.ALERT, C7_NUM),
         J.bar(bx, by, bw, bh, 75000 / 89680, J.LINE, "設計の想定"),
         J.bar(bx + 920, by, bw, bh, n / 89680, J.ALERT, "実績")]
    # 柱の下（y=760〜890）が空いていたので、就航と事故の年を左右の足元に置いた
    g.append(J.label(C7_LX, 832, "1969年　就航", J.LINE, 34, "middle"))
    g.append(J.label(C7_RX, 832, "1988年　事故", J.ALERT, 34, "middle"))
    if k >= 0.999:
        g.append(J.label(C7_RX, 726, "想定の 1.20 倍", J.ALERT, 48, "middle"))
        g.append(J.label(C7_LX, 726, "この回数で使い切る前提だった", J.LINE, 32, "middle"))
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
    jobs = {"_empty": J.frame(W, H),          # 余白測定の基準（check_space.py が使う）
            "p1_bg": p1_bg(), "p1_lab": p1_lab(), "p1_a1": p1_a1(), "p1_a2": p1_a2(),
            "p2_bg": p2_bg(), "p2_lab": p2_lab(), "p2_a1": p2_a1(),
            "c2_base": c2_base(), "c2_hole": c2_hole(), "c2_tearline": c2_tearline(),
            "c2_lab": c2_lab(), "c2_a1": c2_a1(), "c2_a2": c2_a2(),
            "p3_bg": p3_bg(), "p3_lab": p3_lab(), "p3_a1": p3_a1(), "p3_a2": p3_a2(),
            "c3_base": c3_base(), "c3_arc": c3_arc(), "c3_lab": c3_lab(),
            "c3_call": c3_call(),
            "c4_base": c4_base(), "c4_crack": c4_crack(), "c4_lab": c4_lab(),
            "c4_a1": c4_a1(), "c4_a2": c4_a2(), "c4_a3": c4_a3(),
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
