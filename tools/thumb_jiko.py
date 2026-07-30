# -*- coding: utf-8 -*-
"""事故検証チャンネルのサムネイル。**必ず写真を使う**（2026-07-30 カズヤくん指示）。

■ なぜ作り直したか
`tools/thumb_photo.py`（v4）は動くが、2つ都合が悪かった。
  ① ローカルの Edge で焼いていた（レンダリングはクラウドのみ、が本チャンネルの規則）
  ② フォントを別リポジトリ（zankoku-sekkeizu）から読んでいた＝クラウドで落ちる
このファイルは `tools/render.py` を通してクラウドの Chrome で焼き、
フォントはこのリポジトリの `fonts/` を base64 で埋め込む。

■ 3つの型を並べて焼く（どれを採用するかはカズヤくんが決める）
  A 証拠写真型 … 競合と同じ「全幅の黄色い事故名」。写真は全面。競合の棚に馴染む
  B 左パネル型 … 写真を右半分に無傷で見せ、文字は左の暗いパネルに積む
  C 数字型     … 図解チャンネルらしく巨大な数字を主役にする（競合との差が一番はっきり）

■ どの型にも必ず入るもの（チャンネルの顔）
  1 左端の検証タブ（縦書きのカテゴリ）… 競合に無い。視聴者が系統を覚える
  2 原因チップ「原因：〇〇」          … 「なぜ壊れたかを図解する」という約束の先出し
  3 出典の明記                        … 一次資料で作っていることをサムネで示す
     ⚠️ 引用の要件（出典明記）をサムネでも満たしておく。実務上の危険は訴訟ではなく
        YouTube の権利申し立てなので、**PDが手に入る素材はPDを優先**する。

使い方： python tools/thumb_jiko.py
"""
import base64
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageEnhance

import render

HERE = Path(__file__).parent.parent
FONTS = HERE / "fonts"
OUT = HERE / "out" / "thumb"
W, H = 1280, 720

TAB_W = 66
INK = "#eef1f4"
DARK = "#0d1015"
YEL = "#ffd21c"
RED = "#f0250f"

# Dela Gothic One の実測字幅（em）。**推定 0.72 で c7 の数字を接触させた失敗があるので
# サムネでも同じ値を使う**。半角＝0.84 ／ 全角＝1.016
DELA_FULL, DELA_HALF = 1.016, 0.84


def face(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


def units(t):
    return sum(DELA_HALF if ord(c) < 0x2E80 else DELA_FULL for c in t)


def fit(t, box_w, want, lo=0.72, hi=1.06):
    """高さ want を狙い、横は box_w に収める級数を返す。

    横圧縮は textLength に任せる（文字数が増えても縦が縮まないようにするため）。
    圧縮率が lo を下回る＝潰れすぎるときだけ級数を落とす。
    """
    natural = units(t) * want
    ratio = box_w / natural
    if ratio < lo:
        return box_w / (units(t) * lo)
    if ratio > hi:
        return box_w / (units(t) * hi)
    return want


def photo(src, cy=0.5, contrast=1.18, color=1.12, bright=0.94, w=W, h=H):
    """写真を箱いっぱいに切り出して data URI にする。"""
    im = Image.open(HERE / "ref" / src).convert("RGB")
    z = max(w / im.width, h / im.height)
    cw, ch = min(im.width, w / z), min(im.height, h / z)
    l, t = (im.width - cw) / 2, (im.height - ch) * cy
    im = im.crop((round(l), round(t), round(l + cw), round(t + ch)))
    im = im.resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(color)
    im = ImageEnhance.Brightness(im).enhance(bright)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


DEFS = f'''<defs>
  <linearGradient id="sT" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#03060a" stop-opacity="0.90"/>
    <stop offset="100%" stop-color="#03060a" stop-opacity="0"/></linearGradient>
  <linearGradient id="sB" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0%" stop-color="#03060a" stop-opacity="0.96"/>
    <stop offset="100%" stop-color="#03060a" stop-opacity="0"/></linearGradient>
  <linearGradient id="sL" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#03060a" stop-opacity="0.96"/>
    <stop offset="72%" stop-color="#03060a" stop-opacity="0.88"/>
    <stop offset="100%" stop-color="#03060a" stop-opacity="0"/></linearGradient>
  <radialGradient id="vig" cx="52%" cy="46%" r="74%">
    <stop offset="46%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity="0.58"/></radialGradient>
  <linearGradient id="red" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ff7a52"/><stop offset="44%" stop-color="{RED}"/>
    <stop offset="100%" stop-color="#960c03"/></linearGradient>
  <linearGradient id="ylw" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#fff8c2"/><stop offset="44%" stop-color="{YEL}"/>
    <stop offset="100%" stop-color="#cf8203"/></linearGradient>
  <linearGradient id="wht" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#c5cdd6"/>
  </linearGradient>
  <pattern id="hz" width="30" height="30" patternUnits="userSpaceOnUse"
           patternTransform="rotate(45)">
    <rect width="30" height="30" fill="#14161a"/><rect width="15" height="30" fill="{YEL}"/>
  </pattern>
  <filter id="sh" x="-14%" y="-14%" width="132%" height="132%">
    <feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#000" flood-opacity="0.74"/>
  </filter>
</defs>'''


def tab(category):
    """左端の検証タブ。どの型にも必ず入るチャンネルの顔。"""
    return f'''
<rect x="0" y="0" width="{TAB_W}" height="{H}" fill="#101317" opacity="0.95"/>
<rect x="{TAB_W - 7}" y="0" width="7" height="{H}" fill="{YEL}"/>
<rect x="14" y="26" width="38" height="38" rx="6" fill="{RED}"/>
<text x="33" y="55" font-family="Dela" font-size="26" fill="#fff"
      text-anchor="middle">検</text>
<text x="33" y="112" font-family="Noto" font-size="40" font-weight="700" fill="{INK}"
      letter-spacing="10" text-anchor="middle"
      style="writing-mode:vertical-rl;text-orientation:upright">{category}</text>'''


def cause_chip(x, y, cause):
    """原因チップ。「なぜ壊れたかを図解する」というこのチャンネルの約束を先出しする。"""
    return f'''<g filter="url(#sh)">
  <rect x="{x}" y="{y}" width="{22 + len(cause) * 28 + 96}" height="54" rx="6"
        fill="#101317" opacity="0.93"/>
  <rect x="{x}" y="{y}" width="7" height="54" fill="{YEL}"/>
  <text x="{x + 20}" y="{y + 38}" font-family="Noto" font-size="29" font-weight="700"
        fill="{INK}">原因：{cause}</text></g>'''


def credit(t, y=H - 14):
    """出典。**サムネでも出す**（引用の要件を満たしておく）。"""
    return (f'<text x="{TAB_W + 16}" y="{y}" font-family="Noto" font-size="19" '
            f'fill="#9fb0bd" opacity="0.95">{t}</text>')


def big(x, y, t, box_w, want, fill, anchor="start", stroke=0.19):
    s = fit(t, box_w, want)
    return (f'<text x="{x}" y="{y}" font-family="Dela" font-size="{s:.1f}" '
            f'text-anchor="{anchor}" textLength="{box_w}" '
            f'lengthAdjust="spacingAndGlyphs" fill="{fill}" stroke="#07090c" '
            f'stroke-width="{s * stroke:.1f}" stroke-linejoin="round" '
            f'paint-order="stroke fill" filter="url(#sh)">{t}</text>')


# ── 型A：証拠写真型（競合と同じ「全幅の黄色い事故名」） ────────
def type_a(uri, hook_r, hook_w, sub, title, cause, category, badge, src):
    inner = W - TAB_W - 48
    return f'''{DEFS}
<image href="{uri}" x="0" y="0" width="{W}" height="{H}"
       preserveAspectRatio="xMidYMid slice"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/>
<rect x="0" y="0" width="{W}" height="286" fill="url(#sT)"/>
<rect x="0" y="{H - 300}" width="{W}" height="300" fill="url(#sB)"/>
{tab(category)}
<rect x="{TAB_W}" y="520" width="{W - TAB_W}" height="11" fill="url(#hz)" opacity="0.92"/>
<text x="{TAB_W + 24}" y="118" font-family="Dela" font-size="{fit(hook_r + hook_w, 812, 96):.1f}"
      textLength="812" lengthAdjust="spacingAndGlyphs" stroke="#07090c"
      stroke-width="{fit(hook_r + hook_w, 812, 96) * 0.20:.1f}" stroke-linejoin="round"
      paint-order="stroke fill" filter="url(#sh)"><tspan fill="url(#red)">{hook_r}</tspan
      ><tspan fill="url(#wht)">{hook_w}</tspan></text>
<text x="{TAB_W + 28}" y="180" font-family="Noto" font-size="42" font-weight="700"
      letter-spacing="-1" fill="url(#wht)" stroke="#07090c" stroke-width="11"
      stroke-linejoin="round" paint-order="stroke fill" filter="url(#sh)">{sub}</text>
{cause_chip(TAB_W + 24, 440, cause)}
{big(TAB_W + inner // 2 + 24, 674, title, inner, 148, "url(#ylw)", "middle")}
<g filter="url(#sh)">
  <rect x="964" y="26" width="286" height="56" rx="8" fill="#101317" opacity="0.93"/>
  <rect x="964" y="26" width="7" height="56" fill="{RED}"/>
  <text x="1112" y="66" font-family="Noto" font-size="31" font-weight="700" fill="{INK}"
        text-anchor="middle">{badge}</text></g>
{credit(src, 706)}'''


# ── 型B：左パネル型（写真を右半分に無傷で見せる） ─────────────
def type_b(uri, hook_r, hook_w, sub, title, cause, category, badge, src):
    px = TAB_W + 24
    pw = 566
    return f'''{DEFS}
<image href="{uri}" x="0" y="0" width="{W}" height="{H}"
       preserveAspectRatio="xMidYMid slice"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/>
<rect x="0" y="0" width="700" height="{H}" fill="url(#sL)"/>
{tab(category)}
<rect x="{px}" y="176" width="{pw}" height="9" fill="url(#hz)" opacity="0.92"/>
{big(px, 148, hook_r + hook_w, pw, 104, "url(#red)")}
<text x="{px}" y="236" font-family="Noto" font-size="34" font-weight="700"
      fill="url(#wht)" stroke="#07090c" stroke-width="9" stroke-linejoin="round"
      paint-order="stroke fill" filter="url(#sh)">{sub}</text>
{big(px, 384, title, pw, 116, "url(#ylw)")}
{cause_chip(px, 430, cause)}
<g filter="url(#sh)">
  <rect x="{px}" y="530" width="286" height="56" rx="8" fill="#101317" opacity="0.93"/>
  <rect x="{px}" y="530" width="7" height="56" fill="{RED}"/>
  <text x="{px + 148}" y="570" font-family="Noto" font-size="31" font-weight="700"
        fill="{INK}" text-anchor="middle">{badge}</text></g>
{credit(src)}'''


# ── 型C：数字型（図解チャンネルらしく数字を主役にする） ───────
def type_c(uri, num, num_unit, num_cap, hook, title, cause, category, badge, src):
    px = TAB_W + 26
    pw = 560
    return f'''{DEFS}
<image href="{uri}" x="0" y="0" width="{W}" height="{H}"
       preserveAspectRatio="xMidYMid slice"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/>
<rect x="0" y="0" width="720" height="{H}" fill="url(#sL)"/>
<rect x="0" y="{H - 250}" width="{W}" height="250" fill="url(#sB)"/>
{tab(category)}
<text x="{px}" y="132" font-family="Noto" font-size="32" font-weight="700"
      fill="#9fb0bd">{num_cap}</text>
{big(px, 292, num, pw, 190, "url(#ylw)")}
<text x="{px}" y="348" font-family="Noto" font-size="40" font-weight="700"
      fill="url(#wht)" stroke="#07090c" stroke-width="10" stroke-linejoin="round"
      paint-order="stroke fill" filter="url(#sh)">{num_unit}</text>
<rect x="{px}" y="386" width="{pw}" height="9" fill="url(#hz)" opacity="0.92"/>
{big(px, 470, hook, pw, 78, "url(#red)")}
{cause_chip(px, 508, cause)}
{big(TAB_W + (W - TAB_W) // 2, 676, title, W - TAB_W - 48, 128, "url(#wht)", "middle")}
<g filter="url(#sh)">
  <rect x="964" y="26" width="286" height="56" rx="8" fill="#101317" opacity="0.93"/>
  <rect x="964" y="26" width="7" height="56" fill="{RED}"/>
  <text x="1112" y="66" font-family="Noto" font-size="31" font-weight="700" fill="{INK}"
        text-anchor="middle">{badge}</text></g>
{credit(src, 706)}'''


def bake(name, body):
    css = face("Dela", "DelaGothicOne.woff2") + face("Noto", "NotoSansJP-Bold.woff2")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">{body}</svg>')
    html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
            f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')
    OUT.mkdir(parents=True, exist_ok=True)
    render.png(html, OUT / f"{name}.png", W, H)
    print(name, flush=True)


# ── タイタン号（本番1本目）の案 ───────────────────────────
# 🔴 2026-07-30 第1稿の敗因：地に**壊れた耐圧殻の実物写真**（NTSB図14）を使ったところ、
#    スマホ相当（幅246px）では**流木か岩にしか見えなかった**。証拠としては最強でも、
#    スクロール中に「潜水艇の話」だと認識されない。カズヤくん判断で
#    **タイタニック船首のPD写真に差し替え**（深い海の話だと一目で伝わる）。
# 壊れた耐圧殻はインセット案（A2i）に残す。動画本編では主役のまま使う。
CR_BOW = "写真：NOAA／IFE／ロードアイランド大学（パブリックドメイン）"
CR_NTSB = "写真：NTSB／MIR-25-36（パブリックドメイン）"
PH_BOW = "titan_titanic_bow.jpg"    # NOAA 2004年調査：タイタニックの船首（水深3,840m）
PH_HULL = "titan_hull_edge.jpg"     # NTSB図14下：中央破断面。層が刃のように裂けている


def inset(uri, x, y, w, h, cap):
    """壊れた耐圧殻の実物写真を小さく差し込む枠。**証拠は捨てずに残す**ため。"""
    return f'''<g filter="url(#sh)">
  <image href="{uri}" x="{x}" y="{y}" width="{w}" height="{h}"
         preserveAspectRatio="xMidYMid slice"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{YEL}"
        stroke-width="5"/>
  <rect x="{x}" y="{y + h - 34}" width="{w}" height="34" fill="#101317" opacity="0.90"/>
  <text x="{x + 10}" y="{y + h - 10}" font-family="Noto" font-size="22"
        font-weight="700" fill="{INK}">{cap}</text></g>'''


def titan():
    """⚠️ ここに書く数字は**すべて NTSB/MIR-25-36 の本文で確認したもの**だけ。

    引き継ぎメモにあった「約0.001秒で爆縮」は報告書を全文検索しても
    "0.001" も "millisecond" も出てこなかったので**使わない**。
    「8回潜り続けた」も不正確だった。報告書の表6・付録の潜航記録では、
    ダイブ80（2022-07-15・3,840m）の直後は
      81 = 3,840m ／ 82 = 3,840m ／ 83 = 2,954m ／ 84〜87 = 10m以下 ／ 88 = 爆縮
    なので「そのあと3回、タイタニックの深さへ人を運んだ」が正確で、しかも強い。

    決まったタイトル（2026-07-30 カズヤくん）：
    「船体が壊れる音を全員が聞いていた。それでも3回タイタニックへ客を運び、
      5名が爆縮したタイタン号事故の真相【ゆっくり解説】」
    ⚠️ サムネの決め語は**タイトルの丸写しにしない**。短く殴る側に振る。
    """
    bow = photo(PH_BOW, cy=0.46, contrast=1.20, color=1.16, bright=0.96)
    hull = photo(PH_HULL, cy=0.52, contrast=1.26, color=1.04, bright=0.94, w=380, h=214)

    # A2：証拠写真型（第1稿でいちばん読めた型）。地をタイタニック船首に差し替え
    bake("titan_A2", type_a(
        bow, "壊れる音", "を全員が聞いた",
        "5名死亡・そのあと3回、同じ船でタイタニックへ",
        "タイタン号 爆縮", "炭素繊維の層間剥離", "潜水", "2023・北大西洋", CR_BOW))

    # A2i：A2 に「実際に壊れた耐圧殻」をインセットで差し込む。
    #      深海だと一目で分かる地＋唯一の武器（実物写真）の両取りを狙う
    bake("titan_A2i", type_a(
        bow, "壊れる音", "を全員が聞いた",
        "5名死亡・そのあと3回、同じ船でタイタニックへ",
        "タイタン号 爆縮", "炭素繊維の層間剥離", "潜水", "2023・北大西洋",
        CR_BOW + "　／　インセット：" + CR_NTSB)
        + inset(hull, 866, 240, 380, 214, "回収された耐圧殻"))

    # C2：数字型（図解chらしく数字を主役に）
    bake("titan_C2", type_c(
        bow, "3,363", "メートルの深さで爆縮", "5名が死亡した水深",
        "壊れたあと3回潜った", "潜水艇タイタン号 5名死亡",
        "炭素繊維の層間剥離", "潜水", "2023・北大西洋", CR_BOW))


if __name__ == "__main__":
    titan()
