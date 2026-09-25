# -*- coding: utf-8 -*-
"""事故検証チャンネルのサムネイル。**必ず写真を使う**（2026-07-30 カズヤくん指示）。

■ 2026-07-30：競合のサムネを**画素で実測**して型を作り直した
指示は「競合を徹底的に分析して、ヒットしている動画と型をそろえる。その後でオリジナリティを足す」。
`ゆっくり事故検証`（登録7.3万）の全期間人気順から上位12本＋下位8本の maxresdefault を落とし、
彩度と色相で赤い行・黄色い行を検出して寸法を測った。

■ 実測した競合の型（上位12本／下位8本ともまったく同じ＝これは「守って当然の土俵」）

    ┌─────────────────────────────┐  ← 写真は**全面**。上下に黒帯は無い
    │ 赤1行  上端に密着 y=15〜170          │     字面の高さ **約150px**（画面の21%）
    │        全幅 x=16〜1264（画面の97%）  │     色 **#c30a08**（純赤ではなく濃い臙脂）
    │                                     │     **白フチ**（太い）
    │   写真（左右に2枚並べることが多い）   │  ← 事故前／事故後、本体／残骸 の対比
    │                                     │
    │ 黄1行  下端に密着 y=525〜705         │     字面の高さ **約180px**（25%）
    │        全幅                          │     色 **#fbfb0e** ／ **黒フチ**
    └─────────────────────────────┘

    ⚠️ **副題・カテゴリタブ・原因チップ・年代バッジ・出典は competitor には1つも無い。**
       文字は赤1行と黄1行の**2行だけ**。それぞれを画面幅いっぱいまで潰して最大化している。
    ⚠️ 書体は**角張った極太**（Noto Sans JP Black 相当）。Dela Gothic One の丸ゴシックではない。
    ⚠️ 文字数は赤・黄とも **10〜14字**。

■ 第1稿・第2稿が外していた点（全部直した）
    | | 競合 | こちらの旧案 |
    |---|---|---|
    | 赤の字面 | 150px | 96px（1.6倍小さい） |
    | 赤の幅 | 画面の97% | 63% |
    | 赤のフチ | **白** | 黒 |
    | 黄の字面 | 180px | 148px |
    | 余計な要素 | **ゼロ** | 副題・タブ・原因チップ・バッジ・出典の5つ |
    | 書体 | 角張った極太 | Dela（丸い） |
    | 写真 | 2枚並べ | 1枚 |

■ オリジナリティ（型を壊さない範囲でだけ足す）
    型は competitor と同一のまま、**写真の中身だけ**を唯一無二にする。
      左＝タイタニックの船首（NOAA・PD）／右＝**回収された耐圧殻の破断面**（NTSB・PD）
    右は2025年10月公開の報告書の写真で、**競合の96万本（2025-02-16公開）には存在しない**。
    枠は横並び＝競合の型そのもの。中身だけが誰も持っていない。

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

# ── 実測した競合の値。**ここは競合に合わせる。勝手に動かさない** ────
RED = "#c30a08"          # 上の行。純赤ではなく濃い臙脂
YEL = "#fbfb0e"          # 下の行。緑寄りの純黄
MG = 16                  # 左右の余白（実測 13〜26 の中央値）
TXT_W = W - MG * 2       # 1248
# 🔴 すべて競合の maxresdefault を画素で測った値。**推定値は1つも使っていない。**
#    （最初は「字面＝0.72em」と当て推量で置き、赤が上に27px・黄が下に27px はみ出した。
#      さらに文字が競合の1.35倍の大きさになっていた。実測に置き換えて両方直した）
RED_CAP = 150            # 赤のインクの高さ（競合タイタン号96万回の実測値）
YEL_CAP = 186            # 黄のインクの高さ（同上。三豊100万回は170、セウォル74万回は186）
RED_TOP = 15             # 赤のインク上端（競合の実測 12〜18 の中央）
YEL_BOT = 701            # 黄のインク下端（競合の実測 700〜704 の下限側）
STROKE = 24              # フチの太さ

# Noto Sans JP Black のインクの出かた（こちらのクラウド出力を画素で測った）
#   font-size に対して 高さ 0.95em ／ ベースラインより上 0.855em ／ 下 0.091em
INK_H, INK_UP, INK_DN = 0.95, 0.855, 0.091


def _size(cap):
    """インクの高さ cap を出す font-size。**0.72 ではなく実測の 0.95 で割る。**"""
    return cap / INK_H


# ベースラインは「競合のインク位置」から逆算する
RED_BASE = round(RED_TOP + INK_UP * _size(RED_CAP))       # → 150
YEL_BASE = round(YEL_BOT - INK_DN * _size(YEL_CAP))       # → 683

# Noto Sans JP Black の実測字幅（em）。全角はほぼ 1.0、半角数字は 0.56
FULL, HALF = 1.0, 0.56


def face(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:900;font-display:block;}}")


def units(t):
    return sum(HALF if ord(c) < 0x2E80 else FULL for c in t)


def size_for(t, cap):
    """インクの高さ cap になる font-size。

    横は textLength で全幅に潰すので、**級数は高さだけで決める**。
    ⚠️ 文字数が多いと横に潰れすぎて読めなくなる。10〜14字に収めること
       （競合も全部そこに収めている）。
    """
    return _size(cap)


def line(t, base, cap, fill, stroke, sw):
    return (f'<text x="{MG}" y="{base}" font-family="NSB" font-size="{size_for(t, cap):.1f}" '
            f'textLength="{TXT_W}" lengthAdjust="spacingAndGlyphs" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" '
            f'paint-order="stroke fill">{t}</text>')


# ── 文字の演出（2026-08-06 カズヤくん指摘「のっぺりしていてインパクトが弱い」）──
#
# 旧 `line()` は **単色ベタ＋フチ1本**だけだった。競合の寸法（級数・幅・色・フチ）は
# 画素で測って合わせてあるが、**質感までは測っていなかった**。
# 足せるのは3つ。どれも型（赤1行・黄1行・写真だけ）を壊さない。
#   ① 二重フチ … 内側に白（または黒）、その外にもう1本。字が地から完全に浮く
#   ② 縦グラデーション … 上を明るく下を暗く。ベタ塗りの平面感が消える
#   ③ 影 … 右下に硬い影。厚みが出る
# ⚠️ 位置と大きさは動かさない。`textLength` を同じにして重ねるので、
#    何枚重ねても字面の寸法は `RED_CAP` / `YEL_CAP` のまま。

def grad(gid, top, bot):
    """縦のグラデーション。上が明るく下が暗い（光が上から当たっている見え方）。"""
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bot}"/></linearGradient>')


def line_fx(t, base, cap, fill, inner, sw_in, outer=None, sw_out=0, shadow=None):
    """演出つきの1行。

    fill   … 塗り。`url(#gid)` を渡せばグラデーションになる
    inner  … 内側のフチ（競合の実測どおり 赤は白・黄は黒）
    outer  … その外にもう1本。None なら1本だけ
    shadow … (dx, dy, 色, 不透明度)。字の下に硬い影を落とす
    ⚠️ フチは**太い順に描いて重ねる**。SVG の stroke は線の中心に乗るので、
       外側の1本は内側より太くないと隠れる。
    """
    size = size_for(t, cap)
    head = (f'<text x="{MG}" y="{base}" font-family="NSB" font-size="{size:.1f}" '
            f'textLength="{TXT_W}" lengthAdjust="spacingAndGlyphs"')
    g = []
    if shadow:
        dx, dy, col, op = shadow
        g.append(f'{head} transform="translate({dx},{dy})" fill="{col}" stroke="{col}" '
                 f'stroke-width="{max(sw_out, sw_in)}" stroke-linejoin="round" '
                 f'opacity="{op}" paint-order="stroke fill">{t}</text>')
    if outer:
        g.append(f'{head} fill="none" stroke="{outer}" stroke-width="{sw_out}" '
                 f'stroke-linejoin="round">{t}</text>')
    g.append(f'{head} fill="none" stroke="{inner}" stroke-width="{sw_in}" '
             f'stroke-linejoin="round">{t}</text>')
    g.append(f'{head} fill="{fill}">{t}</text>')
    return "".join(g)


def photo(src, cy=0.5, contrast=1.18, color=1.12, bright=0.96, w=W, h=H, zoom=1.0, cx=0.5, trim=None):
    """写真を箱いっぱいに切り出して data URI にする。

    zoom … 1.0 より大きいと**寄る**（2026-08-06 追加）。123便の飛行中の写真は
           機影が画面の35%しかなく、縮めると何の絵か分からなかった。
    cx   … 横方向の寄せ。既定は中央。
    trim … (左, 上, 右, 下) の割合で先に切る（2026-09-17 追加）。9本目の事故現場の写真は
           **焼き付けを器具ごと複写したもの**＝黒い台紙・留め具・縦書きの字が写っている。本編と同じ値を渡す
    """
    im = Image.open(HERE / "ref" / src).convert("RGB")
    if trim:
        im = im.crop((round(im.width * trim[0]), round(im.height * trim[1]),
                      round(im.width * trim[2]), round(im.height * trim[3])))
    z = max(w / im.width, h / im.height) * zoom
    cw, ch = min(im.width, w / z), min(im.height, h / z)
    l, t = (im.width - cw) * cx, (im.height - ch) * cy
    im = im.crop((round(l), round(t), round(l + cw), round(t + ch))).resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(color)
    im = ImageEnhance.Brightness(im).enhance(bright)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def rival_type(hero, red, yellow, split=None, extra=""):
    """競合と同一の型。**赤1行・黄1行・写真だけ。**

    hero  … 全面に敷く写真の data URI
    split … (右半分の data URI, 継ぎ目のx) を渡すと左右2枚並べになる
    extra … オリジナリティを足すときだけ使う。**空が既定**
    """
    g = [f'<image href="{hero}" x="0" y="0" width="{W}" height="{H}" '
         f'preserveAspectRatio="xMidYMid slice"/>']
    if split:
        # ⚠️ 右半分の写真は**その枠の寸法(640×720)で作ったもの**を渡すこと。
        #    1280×720 で作った画像を 640幅の枠に slice で入れると倍に寄って、
        #    耐圧殻が「木の板と黄色いテープ」にしか見えなくなった（t4の失敗）。
        uri, sx = split
        g.append(f'<image href="{uri}" x="{sx}" y="0" width="{W - sx}" height="{H}" '
                 f'preserveAspectRatio="xMidYMid slice"/>')
    # 黄色の行だけ下地に負けやすいので、下端に薄い暗幕を敷く（競合も暗い写真を選んでいる）。
    # 型を変えるものではなく、明るい写真を使ったときの保険。
    g.append(f'<linearGradient id="sb" x1="0" y1="1" x2="0" y2="0">'
             f'<stop offset="0" stop-color="#000" stop-opacity="0.46"/>'
             f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
             f'<rect x="0" y="{H - 260}" width="{W}" height="260" fill="url(#sb)"/>')
    g.append(extra)
    # 赤は白フチ、黄は黒フチ（実測）。フチは太くしないと写真の上で消える。
    # 赤が「濃い臙脂＋白フチ」なのは、明るい下地では文字色が・暗い下地ではフチが効くから。
    # フチの太さも実測に合わせた。17pxでは競合より細く、写真に接した部分が読みにくかった
    g.append(line(red, RED_BASE, RED_CAP, RED, "#ffffff", STROKE))
    g.append(line(yellow, YEL_BASE, YEL_CAP, YEL, "#000000", STROKE))
    return "".join(g)


# ── 演出の段階（2026-08-06）。寸法は `rival_type` と1画素も変えていない ──
FX = {
    # ① 二重フチだけ。赤＝白フチの外に黒、黄＝黒フチの外に白
    "a_edge": dict(rg=None, yg=None, ro="#1a0000", yo="#ffffff", sh=None),
    # ② ①＋縦グラデーション（上が明るく下が暗い）
    "b_grad": dict(rg=("#e8352c", "#8e0402"), yg=("#fffb8a", "#e8b400"),
                   ro="#1a0000", yo="#ffffff", sh=None),
    # ③ ②＋右下に硬い影
    "c_shadow": dict(rg=("#e8352c", "#8e0402"), yg=("#fffb8a", "#e8b400"),
                     ro="#1a0000", yo="#ffffff", sh=(9, 9, "#000000", 0.55)),
    # ④ ③の影をもっと落とす（厚みを最大に）
    "d_deep": dict(rg=("#f04338", "#7d0301"), yg=("#fffcae", "#dfa200"),
                   ro="#140000", yo="#ffffff", sh=(13, 13, "#000000", 0.7)),
    # ⑤ ③に**上の暗幕とビネット**を足す。地がのっぺりした明るい灰色なので、
    #    文字の側だけ濃くしても画面全体の平板さは残る。地のほうを締める。
    "e_veil": dict(rg=("#e8352c", "#8e0402"), yg=("#fffb8a", "#e8b400"),
                   ro="#1a0000", yo="#ffffff", sh=(9, 9, "#000000", 0.55),
                   veil=True),
}


def fx_type(hero, red, yellow, fx, yel_plain=False, ground=True, split=None):
    """`rival_type` と同じ型のまま、**文字の質感だけ**を足す。

    yel_plain … 黄の行だけ**最初のデザイン**（単色ベタ＋黒フチ1本）に戻す
                （2026-08-06 カズヤくん指示「新案の赤字だけ残して黄色は元に戻す」）。
                ⚠️ 黄は下端に密着していて、下の暗幕と黒フチで十分に立つ。
                  二重フチ（外に白）を足すと**縁が主役になって字が読みにくくなる**側だった。
    ground    … 地の演出（上の暗幕・ビネット）を出すか。False で最初の地に戻る
    split     … (右側の data URI, 継ぎ目の x)。`rival_type` と同じ左右2枚並べ
                （2026-09-21 追加）。⚠️ **右側は その枠の寸法(W-x × H)で作ったもの**を渡す。
                1280幅で作った画像を640幅の枠に slice で入れると倍に寄る（1本目 t4 の失敗）
    """
    k = FX[fx]
    g = [f'<image href="{hero}" x="0" y="0" width="{W}" height="{H}" '
         f'preserveAspectRatio="xMidYMid slice"/>']
    if split:
        uri, sx = split
        g.append(f'<image href="{uri}" x="{sx}" y="0" width="{W - sx}" height="{H}" '
                 f'preserveAspectRatio="xMidYMid slice"/>')
    defs = [f'<linearGradient id="sb" x1="0" y1="1" x2="0" y2="0">'
            f'<stop offset="0" stop-color="#000" stop-opacity="0.46"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>']
    rf, yf = RED, YEL
    if k["rg"]:
        defs.append(grad("gr", *k["rg"]))
        rf = "url(#gr)"
    if k["yg"]:
        defs.append(grad("gy", *k["yg"]))
        yf = "url(#gy)"
    g.append("".join(defs))
    if k.get("veil") and ground:
        # 上の暗幕（赤の下地）と四隅のビネット。**型は変えない**（文字も写真も動かさない）。
        defs2 = (f'<linearGradient id="st" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="#000" stop-opacity="0.42"/>'
                 f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
                 f'<radialGradient id="vg" cx="0.5" cy="0.5" r="0.75">'
                 f'<stop offset="0.45" stop-color="#000" stop-opacity="0"/>'
                 f'<stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient>')
        g.append(defs2)
        g.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#vg)"/>')
        g.append(f'<rect x="0" y="0" width="{W}" height="230" fill="url(#st)"/>')
    g.append(f'<rect x="0" y="{H - 260}" width="{W}" height="260" fill="url(#sb)"/>')
    # 外フチは内フチより太くする（stroke は線の中心に乗るので、同じ太さだと隠れる）
    g.append(line_fx(red, RED_BASE, RED_CAP, rf, "#ffffff", STROKE,
                     k["ro"], STROKE + 16, k["sh"]))
    if yel_plain:
        g.append(line(yellow, YEL_BASE, YEL_CAP, YEL, "#000000", STROKE))
    else:
        g.append(line_fx(yellow, YEL_BASE, YEL_CAP, yf, "#000000", STROKE,
                         k["yo"], STROKE + 16, k["sh"]))
    return "".join(g)


def bake(name, body):
    css = face("NSB", "NotoSansJP-Black.woff2")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">{body}</svg>')
    html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
            f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')
    OUT.mkdir(parents=True, exist_ok=True)
    render.png(html, OUT / f"{name}.png", W, H)
    print(name, len(body) // 1024, "KB", flush=True)


# ── 素材（すべてパブリックドメイン。出所は ref/CREDITS.md） ────────
PH_BOW = "titan_titanic_bow.jpg"      # NOAA/IFE/URI 2004年調査：タイタニックの船首
PH_HULL = "titan_hull_edge.jpg"       # NTSB図14下：耐圧殻の中央破断面
PH_PAIR = "titan_hull_pair.jpg"       # NTSB図13：外面と内面の2枚組
PH_ROV = "titan_rov_tailcone.jpg"     # USCG：海底に立つ尾部コーン（深度3,775.9m）
PH_AFT = "titan_rov_aft.jpg"          # USCG：後部ドームと潰れた船体の残骸
PH_CF = "titan_cf_evidence.jpg"       # USCG職員撮影：回収した炭素繊維の破片（**完全にPD**）


def titan():
    """⚠️ 数字は**すべて NTSB/MIR-25-36 の本文で確認したもの**だけ。

    引き継ぎメモの「約0.001秒で爆縮」は報告書に無い（全文検索で `0.001` も
    `millisecond` も出ない）。「8回潜り続けた」も不正確で、潜航記録は
      81 = 3,840m ／ 82 = 3,840m ／ 83 = 2,954m ／ 84〜87 = 10m以下 ／ 88 = 爆縮。

    🔴 「死」「殺」の扱い（2026-07-30 決定）
       競合のタイトル100本を数えたら**素の「死」は0本**、29本が伏せ字「ﾀﾋ」、
       71本が言い換え（犠牲8／最後の瞬間11／末路5／消えた4／最期2／絶命1）。
       サムネの赤字も9本中8本が「ﾀﾋ」で、素の「死傷」は**100万回の1本だけ**。
       → **こちらは伏せ字を使わず、言い換えで書く。**
         規約に「死」を禁じる条文は無く、判定は文脈で行われる。一次資料で検証する
         このチャンネルは「ドキュメンタリーの文脈」＝規約上いちばん有利な位置にいる。
         伏せ字はその立場を自分から捨てる（規約を回避しようとしている見え方になる）。
       ⚠️ 本当に避けるべきは文字ではなく**煽り**。「即ﾀﾋ」「絶命」「地獄絵図」は
         規約の「デリケートな事象の利用（exploit）」判定に近づく。数字と一次資料の
         用語（爆縮・局所座屈・層間剥離）で殴るほうが、規約上も安全で差別化にもなる。

    🔴 黄色の行（2026-07-30 カズヤくん指示）
       競合とまったく同じ「タイタン号事故の真相」は**完全一致でマズい**ので変更。
       競合の黄色にも「事故名だけ」の型が多い（リア放射線事故／東海村JCO臨界事故／
       ソユーズ11号減圧事故…）ので、そちらの型に寄せて
       **「潜水艇タイタン号 爆縮」**にする。「爆縮」は一次資料の用語で、
       このチャンネルの性格（技術で説明する）もそこで出る。
    """
    SX = 620
    RW = W - SX
    bow = photo(PH_BOW, cy=0.46, contrast=1.26, color=1.34, bright=1.12)
    rov = photo(PH_ROV, cy=0.42, contrast=1.24, color=1.30, bright=1.10)
    aft = photo(PH_AFT, cy=0.44, contrast=1.26, color=1.32, bright=1.12)
    cf = photo(PH_CF, cy=0.50, contrast=1.30, color=1.16, bright=1.10)
    pair_r = photo(PH_PAIR, cy=0.50, contrast=1.28, color=1.10, bright=1.02, w=RW, h=H)
    bow_l = photo(PH_BOW, cy=0.46, contrast=1.26, color=1.34, bright=1.12, w=SX, h=H)

    # 🔴 2026-07-31 カズヤくん承認（試写の指摘②）：**新しさを黄に入れる。**
    #    競合の96万回は 2025-02-16 公開＝**2つの最終報告書より前**
    #    （USCG 2025-08-04／NTSB 2025-10-02）。ここが唯一の差別化点なので外から見せる。
    #    ⚠️ 3行目は足さない。**赤は1文字も触らない**（赤が強い一撃を持つ側だから）。
    #    「潜水艇」を落として「最終報告」を入れる＝ 11字 → 12字。基準の10〜14字に収まる。
    # 2026-08-01 カズヤくん指定で「タイタン号 最新報告書」（11字）に変更。
    # 「爆縮」を外して「最新」を入れた＝新しさを前に出す判断。
    YEL_MAIN = "タイタン号 最新報告書"        # 旧: タイタン号爆縮 最終報告／潜水艇タイタン号 爆縮
    RED_MAIN = "乗員5名 生還者なし"          # ← 決定。「死」を伏せ字にせず言い換えで満たす
    YEL_OLD = "潜水艇タイタン号 爆縮"        # 見比べ用に旧案も焼く

    # ★★ 本番決定案。写真＝USCG の ROV が撮った後部ドームと潰れた船体
    bake("titan_FINAL", rival_type(aft, RED_MAIN, YEL_MAIN))
    # 旧黄（新しさを入れる前）。並べて見て、潰れ具合が許せるかを判定する
    bake("titan_yel_old", rival_type(aft, RED_MAIN, YEL_OLD))

    # 以下は比較用に残す（写真だけを差し替えたもの）
    bake("titan_alt_rov", rival_type(rov, RED_MAIN, YEL_MAIN))    # 海底に立つ尾部コーン
    bake("titan_alt_cf", rival_type(cf, RED_MAIN, YEL_MAIN))      # 炭素繊維の破片（留保ゼロ）
    bake("titan_alt_bow", rival_type(bow, RED_MAIN, YEL_MAIN))    # タイタニック船首
    # 赤を切り口側にした版（人的被害ではなく報告書の発見を前に出す）
    bake("titan_alt_red", rival_type(aft, "壊れた船体で3回潜航", YEL_MAIN))


# ── 2本目：日本航空123便 ────────────────────────────────
# ⚠️ 報告書の写真はすべて**白黒のスキャン**なので、1本目のような彩度は乗らない。
#    `color` を上げても効かない。**コントラストと明るさ**で立たせる。
JA_FLIGHT = "ja123/p124.jpg"   # 写真-124：奥多摩町上空を飛行中の事故機（尾翼を失っている）
JA_BULK = "ja123/p024.jpg"     # 写真-24：復元した後部圧力隔壁（破れが白く抜ける）
JA_REAR = "ja123/p005.jpg"     # 写真-5：後部胴体の残骸（2）＝4人が救出された部位


def ja123():
    """🔴 決め語は 2026-08-06 にカズヤくん承認ずみ。

      赤「生存者4人 全員が最後尾」（12字）
        裏付け＝本文2.13.1「いずれも機体後部の座席列番号54から60、左側及び中央部の
        座席に着席していた（付図-5参照）」。
        ⚠️ 実測で効くのは「証言・記録・生存者」（1.94倍）で、
          「噂・隠蔽・周年」は効かない。だからそちら側の語は入れない。
      黄「日航123便 26年後の解説」（13字）
        差別化＝2011年7月の「事故調査報告書についての解説」。
        競合は1987年の報告書までしか扱っていない。

    ⚠️ 写真-4・写真-5 は現場に救助の人が大勢写っていて、**煽りに寄る**うえ
       縮めると灰色の塊にしか見えない。本命では使わない（比較用にだけ焼く）。
    ⚠️ 型は競合と同一。**赤1行・黄1行・写真だけ。**副題もタブも出典も足さない。
       チャンネル名・アイコン・ロゴも入れない。
    """
    SX = 620
    RW = W - SX
    RED_MAIN = "生存者4人 全員が最後尾"
    YEL_MAIN = "日航123便 26年後の解説"

    # 🔴 2026-08-06：1本目と同じ強さ（contrast 1.3前後）を当てたら**両方とも壊れた**。
    #    左は紙の粒子まで持ち上がって機体が黒い塊になり、右は隔壁の白が飛んで
    #    構造が消えた。白黒スキャンは元から階調が狭いので、**弱くかける**のが正しい。
    flight = photo(JA_FLIGHT, cy=0.44, contrast=1.16, color=1.0, bright=1.00)
    flight_l = photo(JA_FLIGHT, cy=0.44, contrast=1.16, color=1.0, bright=1.00, w=SX, h=H)
    bulk = photo(JA_BULK, cy=0.46, contrast=1.04, color=1.0, bright=0.96)
    bulk_r = photo(JA_BULK, cy=0.46, contrast=1.04, color=1.0, bright=0.96, w=RW, h=H)
    rear_r = photo(JA_REAR, cy=0.52, contrast=1.12, color=1.0, bright=1.00, w=RW, h=H)

    # 🔴 2026-08-06：左右2枚並べは**この題材では成立しなかった**。
    #    左（飛行中）は明るい灰色、右（隔壁）は白飛びした白黒で、継ぎ目で調子が反転する。
    #    1本目はどちらもカラーの海底写真だったので並べられた。
    #    → 飛行中の1枚に絞る。**尾翼を失った機影**は、この事故にしか無い絵で、
    #      縮めても何の絵か分かる（隔壁は縮めると「白い塊」になる）。
    # ★★ 本番決定案（2026-08-06）。寄り1.30・明るさ0.85・コントラスト1.30。
    #    ⚠️ 明るさを落とすのは**赤の白フチを地から離すため**。素のままだと
    #      地が明るい灰色で、白フチが溶けて赤い行が沈む（1本目は暗い海底写真だった）。
    #    ⚠️ 寄り1.60 は機体が枠に触れて「飛行機」に見えなくなる。1.30 が上限。
    hero = photo(JA_FLIGHT, cy=0.46, contrast=1.30, color=1.0, bright=0.85, zoom=1.30)

    # 🔴 2026-08-06 カズヤくん指摘「文字がのっぺりしていてインパクトが弱い」。
    #    競合の**寸法**は測って合わせてあったが、**質感**は測っていなかった。
    #    位置も大きさも1画素も変えずに、二重フチ→グラデ→影 と段階で足して見比べる。
    #    → **e_veil を採用**（二重フチ＋縦グラデ＋影＋上の暗幕とビネット）。
    #      ⚠️ いちばん効いたのは文字そのものより**地を締めたこと**だった。
    #        地が一様な明るい灰色だと、文字だけ濃くしても画面の平板さが残る。
    #      ⚠️ d_deep（影を最大）は行き過ぎ。黄の下半分が茶色に寄って「黄色」でなくなる。
    #
    # 🔴 2026-08-06 カズヤくん指示：**赤は新案のまま、黄だけ最初のデザインに戻す。**
    #    赤は上端で明るい地に接するので二重フチとグラデが要る。
    #    黄は下端に密着していて下の暗幕と黒フチだけで十分に立つ側で、
    #    外に白フチを足すと**縁が主役になって字が読みにくくなる**。
    bake("ja123_FINAL", fx_type(hero, RED_MAIN, YEL_MAIN, "e_veil", yel_plain=True))
    # 地の演出（上の暗幕とビネット）を切った版。どちらが良いか見比べる用
    bake("ja123_alt_noveil",
         fx_type(hero, RED_MAIN, YEL_MAIN, "e_veil", yel_plain=True, ground=False))
    bake("ja123_fx0_flat", rival_type(hero, RED_MAIN, YEL_MAIN))   # 最初＝両方とも単色ベタ
    bake("ja123_fx_both_new", fx_type(hero, RED_MAIN, YEL_MAIN, "e_veil"))  # 両方とも新案
    # 比較用に残す
    bake("ja123_alt_bulk", rival_type(bulk, RED_MAIN, YEL_MAIN))       # 隔壁1枚
    bake("ja123_alt_flight", rival_type(flight, RED_MAIN, YEL_MAIN))   # 寄せない版
    bake("ja123_alt_pair", rival_type(flight_l, RED_MAIN, YEL_MAIN, split=(bulk_r, SX)))


TH_TORN = "thresher/thr_t23.jpg"    # 289-T-23：引き裂かれた船体（ぎざぎざの断面）
TH_HULL = "thresher/thr_t33.jpg"    # 289-T-33：外殻（上部構造）の大きな曲面
TH_DRAFT = "thresher/thr_t24.jpg"   # 289-T-24：喫水の目盛（4 5 6 7 8 9 30 …）
TH_CRATER = "thresher/thr_t41.jpg"  # 289-T-41：海底に残った黒い跡
# 🔴 2026-08-10 カズヤくん指摘：**アルバム41点はどれも何の写真か伝わらない。**
#    海底の白黒は縮めると灰色の塊になる。「競合17本中0本」の珍しさを取って
#    肝心の「一目で何か分かる」を捨てていた。→ 艦そのものの写真を候補に足す。
TH_BOW = "thresher/cm_USS_Thresher__SSN-593__bow.jpg"          # 正面から迫る艦首
TH_BOWC = "thresher/cm_USS_Thresher__SSN-593__bow__cropped_.jpg"  # 同・寄り
TH_SEA = "thresher/cm_USS_Thresher__SSN-593_.jpg"              # 航走中。**593が読める**
TH_BOW2 = "thresher/nara_428-N-1057645.jpg"                    # 別カットの艦首
TH_DEBRIS = "thresher/cm_330-PSA-110-63__USN_711302___22171571340_.jpg"  # 海底の残骸（褐色）
# 🔴 2026-08-10 3巡目：**記録映画からコマを抜いた。**
#    静止画はどれも白黒だが、記録映画 `thr_85185`（naId 85185・789秒）は**カラー**。
#    この題材でカラーの艦影は競合にまず無い＝一覧で色が違うだけで目を引く。
#    ⚠️ 元が 720x480 なので 1280x720 へは1.78倍に伸びる。**原寸では甘い**が、
#      一覧の210pxでは分からない。サムネは実寸で判断する。
TH_FILM_A = "thresher/thr_film593_a.jpg"   # 622秒。セイルやや左・白波
TH_FILM_B = "thresher/thr_film593_b.jpg"   # 628秒。**セイル中央・593が大きい・波が左右対称**
TH_FILM_C = "thresher/thr_film593_c.jpg"   # 631秒。セイルやや右


def thresher():
    """🔴 決め語は 2026-08-10 にカズヤくん承認ずみ。

      赤「129名圧壊 海底2600m」（units 10.0）
        ⚠️ **「水深2600m」ではない。** 台本 pr04 は「**沈んだ場所の**水深は、
          およそ8,500フィート」＝2,600mは**海底の深さ**であって圧壊した深さでは
          ない（圧壊はもっと浅い）。「水深」と書くと事実と違うことを言ってしまう。
      黄「機密解除された査問会記録」（units 12.0）
        差別化＝査問会記録が 2020-09-23 と 2021-07-09 に公開された。
        競合17本はどれも扱っていない。

    ⚠️ 型は競合と同一。**赤1行・黄1行・写真だけ。**副題もタブも出典も足さない。
       チャンネル名・アイコン・ロゴも入れない。
    ⚠️ **アルバム41点はどれも打字の説明札が貼り込まれている。**
       そのまま使うと白い札が写って画面に文字が2種類出るので、
       `cx` / `zoom` で札を画面の外へ逃がすこと。
    """
    RED_MAIN = "129名圧壊 海底2600m"
    YEL_MAIN = "機密解除された査問会記録"

    # 札は t23=右上／t33=右／t24=右下／t41=右下。どれも左へ寄せて逃がす。
    # 🔴 1巡目（cx 0.28〜0.34）では **hull・draft・crater の3枚とも札が画面に残った**
    #    （"superst… break ap…" "Draft markers…" "TRIESTE I…" が右端に読めた）。
    #    札はどれも右端に貼ってあるので、cx を 0.1 前後まで左へ振って寄りも強める。
    torn = photo(TH_TORN, cx=0.30, cy=0.52, contrast=1.22, color=1.0,
                 bright=0.92, zoom=1.30)
    hull = photo(TH_HULL, cx=0.08, cy=0.50, contrast=1.20, color=1.0,
                 bright=0.92, zoom=1.50)
    draft = photo(TH_DRAFT, cx=0.10, cy=0.44, contrast=1.30, color=1.0,
                  bright=0.96, zoom=1.50)
    crater = photo(TH_CRATER, cx=0.06, cy=0.50, contrast=1.24, color=1.0,
                   bright=0.94, zoom=1.60)

    # 🔴 2巡目。艦そのものが写っているほう。地が明るい海なので **bright を落として**
    #    赤の白フチを地から離す（123便の飛行中の写真と同じ理屈）。
    # 🔴 2巡目で分かったこと（カズヤくん指摘を受けて艦の写真を試した）
    #    ・**艦首から見た3枚（bow/bowc/bow2）は駄目。** セイルが真上に伸びていて、
    #      上端に密着する赤の帯に**必ず切られる**。艦の形が「黒い柱」にしか見えない。
    #    ・**航走中の1枚（sea）が最も読める。** 艦影が横に寝ているので赤と黄の
    #      あいだにきれいに収まり、しかも**セイルの「593」が読める**。
    #    → sea を3通りの寄りで詰める。
    sea = photo(TH_SEA, cy=0.50, cx=0.45, contrast=1.26, color=1.0,
                bright=0.84, zoom=1.15)
    sea_z = photo(TH_SEA, cy=0.52, cx=0.42, contrast=1.30, color=1.0,
                  bright=0.82, zoom=1.45)
    sea_zz = photo(TH_SEA, cy=0.53, cx=0.40, contrast=1.34, color=1.0,
                   bright=0.80, zoom=1.75)
    debris = photo(TH_DEBRIS, cy=0.50, contrast=1.22, color=1.10,
                   bright=0.94, zoom=1.20)

    # 🔴 3巡目。記録映画のカラー。地が明るい空と海なので bright を落として
    #    赤の白フチを地から離す。**寄りすぎると 720x480 の粗が出る**ので控えめに。
    film_a = photo(TH_FILM_A, cy=0.50, contrast=1.12, color=1.06,
                   bright=0.90, zoom=1.10)
    film_b = photo(TH_FILM_B, cy=0.50, contrast=1.12, color=1.06,
                   bright=0.90, zoom=1.10)
    film_c = photo(TH_FILM_C, cy=0.50, contrast=1.12, color=1.06,
                   bright=0.90, zoom=1.10)
    # 同じコマを濃いめに焼いた版（フィルムは眠いので締めたほうが一覧で立つか試す）
    film_b2 = photo(TH_FILM_B, cy=0.50, contrast=1.26, color=1.20,
                    bright=0.86, zoom=1.10)
    film_b3 = photo(TH_FILM_B, cy=0.52, contrast=1.26, color=1.20,
                    bright=0.86, zoom=1.32)

    # 123便で採った作り（赤＝二重フチ＋グラデ＋影、黄＝単色ベタ）をそのまま当てる。
    for nm, hero in (("film_b", film_b), ("film_b2", film_b2), ("film_b3", film_b3),
                     ("sea_z", sea_z), ("debris", debris)):
        bake(f"thr_{nm}", fx_type(hero, RED_MAIN, YEL_MAIN, "e_veil",
                                  yel_plain=True))


# ── 4本目 サーフサイド（2026-09-06・⑥）─────────────────────
SS_FACE = "surfside/fb_pr01.jpg"    # B-Roll #1 12.5秒：せん断した棟の断面（NIST／PD）
SS_PILE = "surfside/fb_pr02.jpg"    # 同 53.8秒：瓦礫の山と背後に残った棟
SS_WIDE = "surfside/fb_pr03.jpg"    # 同 15.0秒：瓦礫と捜索隊の引き


def surfside():
    """4本目のサムネ。⚠️ **決め語はまだカズヤくんの承認を取っていない**（案を3通り焼く）。

    型は競合と同一＝**赤1行・黄1行・写真だけ**（[[feedback-jiko-thumbnail-rival-format]]）。
    副題・タブ・出典・チャンネル名・ロゴは足さない。

    ■ 決め語の考え方（3本目 thresher の型に合わせた）
      赤＝被害の規模。thresher は「129名圧壊 海底2600m」。
        ⚠️ 「即死」「圧死」は使わない（[[feedback-jiko-death-word-policy]]＝
           報告書の語は本編で原文どおり読むが、**タイトル・サムネは言い換えのまま**）。
      黄＝この動画の差別化。thresher は「機密解除された査問会記録」。
        サーフサイドの差別化は **NIST の技術的知見が 2026年6月22日に出たばかり**であること。
        ⚠️ 実測で効くのは「証言・記録・生存者」＝1.94倍（[[feedback-what-drives-views]]）。
           逆に「隠蔽」0.80／「衝撃」0.83／「闇」0.92 は逆効果なので使わない。

    ■ 地の作り
      fb_pr01 は平均輝度 160.8・彩度 8.0 ＝**明るくて色の無い地**。
      123便・thresher と同じ理屈で **bright を落として**赤の白フチを地から離す。
    """
    # 🔴 2026-09-21 カズヤくん指示：**公開ずみのサムネから「死亡」を外す**（8本目・10本目と同じ扱い）。
    #    この回は「**死亡 → 犠牲** のその場の置き換えだけ」＝画像も他の文言も変えない
    #    （8本目は「7人死亡」→「犠牲7人」と語順まで変えたが、それはこの回の指示ではない）。
    #    ⚠️ 2文字→2文字なので**折返しも字の大きさも変わらない**（210px の読みやすさは据え置き）。
    RED_A = "98名犠牲 12階が数秒で"
    YEL_A = "2026年6月公表 NISTの技術的知見"
    YEL_B = "4本のはずが2本だった鉄筋"
    RED_B = "98名犠牲 崩落は3週間前から"

    face = photo(SS_FACE, cy=0.50, cx=0.50, contrast=1.24, color=1.0,
                 bright=0.82, zoom=1.10)
    pile = photo(SS_PILE, cy=0.50, cx=0.50, contrast=1.22, color=1.05,
                 bright=0.88, zoom=1.10)
    wide = photo(SS_WIDE, cy=0.50, cx=0.50, contrast=1.22, color=1.05,
                 bright=0.86, zoom=1.15)

    # 🔴 210px（YouTube のサイドバーの実寸）で測った結果：
    #    黄は**字数が少ないほど読める**。17字（YEL_A）は詰まって読みにくく、
    #    12字（YEL_B・YEL_C）ははっきり読める（[[feedback-thumbnail-must-read-at-210px]]）。
    YEL_C = "2026年6月 NISTが公表"
    for nm, hero, r, y in (("a_face", face, RED_A, YEL_A),
                           ("b_face_bars", face, RED_A, YEL_B),
                           ("c_pile", pile, RED_A, YEL_A),
                           ("d_face_3weeks", face, RED_B, YEL_A),
                           ("e_wide", wide, RED_A, YEL_A),
                           ("f_face_new", face, RED_A, YEL_C)):
        bake(f"ss_{nm}", fx_type(hero, r, y, "e_veil", yel_plain=True))


SL1_ROD = "sl1/fb_c811.jpg"     # 記録映画 Phase III：防護服の3人が炉の部品を吊り上げる
SL1_CTRL = "sl1/haer_74.jpg"    # HAER ID-33-D-74：SL-1 の制御盤の前（1958年）


def sl1():
    """5本目のサムネ。型は競合と同一＝**赤1行・黄1行・写真だけ**。

    ■ 決め語（本編が実際に読んでいる数字だけを使う）
      赤＝被害の規模。**「3名死亡」**（[[feedback-jiko-death-word-policy]]＝
        「即死」「圧死」はタイトル・サムネに出さない）。
        事故の核心は「中央の制御棒を**手で 20インチ 引き抜いた**」（c712・c719・c721・c727）。
      黄＝この動画の差別化。**208ページの報告書が「原因」を書いていない**こと（pr04・ep01）。
        ⚠️ 実測で効くのは「証言・記録・生存者」＝1.94倍。「隠蔽」「衝撃」「闇」は逆効果
        （[[feedback-what-drives-views]]）。
      ⚠️ 黄は**字数が少ないほど 210px で読める**（[[feedback-thumbnail-must-read-at-210px]]）。

    ■ 地の作り
      `fb_c811` は 1920幅のうち **x240〜1679 だけが絵**（残りは黒帯＝`footage.PILLAR`）。
      `zoom=4/3` でちょうど黒帯が画面の外へ出る（1440×810 を切り出す）。
      ⚠️ ここを 1.0 のままにすると**サムネの左右に黒帯が出る**。
    """
    RED_A = "3名死亡 制御棒を手で引いた"
    RED_B = "当直の3名死亡 棒は20インチ"
    YEL_A = "1961年 SL-1原子炉事故"
    YEL_B = "原因を書かない208ページ"

    rod = photo(SL1_ROD, cy=0.30, cx=0.50, contrast=1.20, color=1.10,
                bright=0.88, zoom=4 / 3)
    rod_lo = photo(SL1_ROD, cy=0.50, cx=0.50, contrast=1.20, color=1.10,
                   bright=0.88, zoom=4 / 3)
    ctrl = photo(SL1_CTRL, cy=0.44, cx=0.42, contrast=1.22, color=1.0,
                 bright=0.86, zoom=1.15)

    for nm, hero, r, y in (("a_rod", rod, RED_A, YEL_A),
                           ("b_rod_208", rod, RED_A, YEL_B),
                           ("c_ctrl", ctrl, RED_A, YEL_A),
                           ("d_rod_inch", rod, RED_B, YEL_A),
                           ("e_rod_lo", rod_lo, RED_A, YEL_A)):
        bake(f"sl1_{nm}", fx_type(hero, r, y, "e_veil", yel_plain=True))


KB_SHIP = "keybridge/fb_ca01.jpg"   # NTSB B-Roll 空撮 369秒：ダリの船首に載った橋桁と、右へ伸びる残りの径間（§105・PD）
KB_BOW = "keybridge/fb_pr08.jpg"    # 240330-A-PA223-1001（陸軍工兵隊）34秒：船首に載った橋桁の寄り（§105・PD）


def keybridge():
    """6本目のサムネ（2026-09-11・⑥）。型は競合と同一＝**赤1行・黄1行・写真だけ**。

    ■ 決め語（本編が実際に読んでいる事実だけを使う）
      赤＝被害の規模＋核心。**「6名死亡」**（pr03）。
        核心は2つ ── 停電の原因が「端子台に奥まで入っていなかった一本の信号線」（pr06・pr07）と、
        衝突まで1分16秒あったのに「橋の上の8人には、誰も伝えなかった」（pr04・pr11・ep06）。
        ⚠️ 警官を責める形にしない。報告書は封鎖を「素早い封鎖が、命を救った」と評価している（ep03）。
      黄＝事故名。日本の報道の呼び名は「ボルチモアの橋崩落」＝検索でも通じる側を採る。
      ⚠️ 「隠蔽」「衝撃」「闇」「結末」は逆効果（[[feedback-what-drives-views]]）。
      ⚠️ 黄は字数が少ないほど 210px で読める（[[feedback-thumbnail-must-read-at-210px]]）。

    ■ 地の作り
      `fb_ca01` は上が明るい空・下が何も無い水面＝**赤と黄の下に絵の主役が来ない**。船と橋桁は画面の中段。
      🔴 人の顔は写っていない（小さな作業艇だけ）＝「実在の顔と N名死亡を並べない」に当たらない。
      `fb_pr08` は寄りで線が細かい＝246px で塊に見えないかを見比べるための対照。
    """
    RED_A = "6名死亡 信号線1本で停電"
    RED_B = "6名死亡 知らせは届かず"
    YEL_A = "2024年 ボルチモア橋崩落"

    ship = photo(KB_SHIP, cy=0.50, cx=0.50, contrast=1.18, color=1.10, bright=0.92)
    bow = photo(KB_BOW, cy=0.50, cx=0.50, contrast=1.16, color=1.08, bright=0.90)

    for nm, hero, r, y in (("a_ship_wire", ship, RED_A, YEL_A),
                           ("b_ship_notice", ship, RED_B, YEL_A),
                           ("c_bow_wire", bow, RED_A, YEL_A)):
        bake(f"kb_{nm}", fx_type(hero, r, y, "e_veil", yel_plain=True))


EP7_SMOKE = "ep7/wtc_smoke_day.jpg"    # Mike Goad（2001年9月11日）：煙の上がるマンハッタンの遠景（PD）
EP7_PRE = "ep7/manhattan_pre.jpg"      # Carol M. Highsmith：事故の前のツインタワー（PD・LCCN2015645969）


def ep7():
    """7本目（9.11）のサムネ（2026-09-14・⑥）。型は競合と同一＝**赤1行・黄1行・写真だけ**。

    ■ 決め語（本編が実際に読んでいる事実だけを使う）
      赤＝この回の差＝**「軍が1機目の乗っ取りを知らされたのは、ぶつかる9分前」**（pr04・ep03）。
        残りの3機は墜ちるまで知らされていない＝**猶予は9分、そのあとは0分**。
        規模は **2,973人**（pr11。乗っ取った側の19人を含まない委員会報告の数）。
        ⚠️ 「隠蔽」「衝撃」「闇」は逆効果（[[feedback-what-drives-views]]）。
        ⚠️ 「即死」などはタイトル・サムネに出さない（[[feedback-jiko-death-word-policy]]）。
      黄＝**「9.11」＋事件名**（2026-09-14 カズヤくん「9.11 という文字のほうが引きがある」）。
      ⚠️ 黄は字数が少ないほど 210px で読める（[[feedback-thumbnail-must-read-at-210px]]）。

    ■ 地の作り
      🔴 **人の顔が1つも写っていない写真だけを地にする**
        （「実在の顔と N名死亡を並べない」＝[[project-jiko-rules-index]] §5）。
        この条件で `artcc_screen_pre`（管制室）は**手前に大きな顔**があるので採らない。
        `pentagon_west_day` は壁の寄りで、246px では瓦礫の塊にしか見えないので採らない。
      `wtc_smoke_day` は煙と稜線が画面の中段＝**赤（上端150px）と黄（下端180px）の下に主役が来ない**。
      `manhattan_pre` は「その朝より前」の側。塔が中段の右寄りなので `cx=0.45` で中央へ寄せる。
    """
    # 🔴 2026-09-14（t2）カズヤくん決定：赤は **B案に確定**／**黄に「9.11」を入れる**
    #    （「9.11 という文字を使ったほうが引きがある」＝タイトルも同じ語に揃えた）。
    #    残る選択は**黄の字数**だけ＝下の3案。⚠️ 黄は字数が少ないほど 210px で読める。
    RED = "2,973人死亡 猶予は9分"
    YEL_A = "9.11 同時多発テロ"          # 11字（型の既定 10〜14字の下寄り）
    YEL_B = "2001年 9.11の真相"          # 13字（競合の「〜の真相」に寄せた形）
    YEL_C = "9.11 アメリカ同時多発テロ"   # 15字（⚠️ 型の上限を1字超える。読めるかを見るための対照）

    smoke = photo(EP7_SMOKE, cy=0.50, cx=0.50, contrast=1.18, color=1.10, bright=0.92)

    for nm, hero, r, y in (("a_toll_911", smoke, RED, YEL_A),
                           ("b_toll_shinso", smoke, RED, YEL_B),
                           ("c_toll_america", smoke, RED, YEL_C)):
        bake(f"ep7_{nm}", fx_type(hero, r, y, "e_veil", yel_plain=True))


EP8_LAUNCH = "ep8/launch_sky.jpg"      # NASA（2003年1月16日）：39-A射点を離れるコロンビア号（PD）
EP8_PAD = "ep8/pad_stack.jpg"          # NASA KSC-03pd0076（2003年）：射点に立つ機体（PD・対照用）


def ep8():
    """8本目（コロンビア号）のサムネ（2026-09-15・⑥）。型は7本目と同一＝**赤1行・黄1行・写真だけ**。

    ■ 決め語（本編が実際に読んでいる事実だけを使う）
      赤＝**7人死亡＋この回だけの核心**（7本目で採用された形＝[[project-jiko-rules-index]] §5）。
        この回だけの核心は3つあり、どれを採るかを t1 の3案で見る：
          a **助ける道はあった** … 第6章の決め所（CAIB p174「challenging but feasible」）
          b **求めは三度退けられた** … 冒頭の引き `pr04`（CAIB p172「Three independent requests」）
          c **原因は16日前** … 時間の順序そのもの（`pr05`・`pr06`）
        ⚠️ 「隠蔽」「衝撃」「闇」「結末」は逆効果（[[feedback-what-drives-views]]）。
        ⚠️ 「即死」などはタイトル・サムネに出さない（[[feedback-jiko-death-word-policy]]）。
      黄＝**通り名「コロンビア号」＋出来事**（11字）。タイトルにも同じ語を入れてある
        （2026-09-14 カズヤくん「世間で通っている短い呼び名は両方で使う」）。
        ⚠️ 黄は字数が少ないほど 210px で読める（[[feedback-thumbnail-must-read-at-210px]]）。

    ■ 地の作り
      🔴 **人の顔が1つも写っていない写真だけを地にする**
        （「実在の顔と N名死亡を並べない」＝[[project-jiko-rules-index]] §5）。
        この条件で `hangar_floor`（残骸を並べた床）と `hangar_grid` は**人が写っている**ので採らない。
        `orb_earth`（窓から見た地球）は暗すぎて 246px では黒い板になるので採らない。
      `launch_sky` は機体が**画面の中段・右寄り**＝赤（上端230px の暗幕）と黄（下端260px）の
      どちらの下にも主役が来ない。`cx=0.56` で機体を中央へ寄せる。
    """
    RED_A = "7人死亡 助ける道はあった"       # 13字
    RED_B = "7人死亡 求めは三度退けられた"    # 15字
    RED_C = "7人死亡 原因は16日前にあった"    # 15字
    YEL = "コロンビア号 空中分解"            # 11字（7本目の採用と同じ字数）

    sky = photo(EP8_LAUNCH, cy=0.46, cx=0.56, contrast=1.16, color=1.08, bright=0.94)

    for nm, hero, r, y in (("a_saved", sky, RED_A, YEL),
                           ("b_thrice", sky, RED_B, YEL),
                           ("c_16days", sky, RED_C, YEL)):
        bake(f"ep8_{nm}", fx_type(hero, r, y, "e_veil", yel_plain=True))


EP9_WRECK = "ep9/wreck_klm_01.jpg"    # Anefo 929-1003（1977年・CC0）：KLM機の尾翼と、焼けて骨組みだけになった胴体
EP9_WRECK_TRIM = (0.198, 0.1986, 0.8286, 0.7652)   # `cuts/ss.py` の本編と同じ値（台紙ごとの複写＝切らないと黒い台紙が出る）


def ep9():
    """9本目（テネリフェ）のサムネ（2026-09-17・⑥）。型は7本目・8本目と同一＝**赤1行・黄1行・写真だけ**。

    ■ 決め語（④' で承認されたタイトル・決め所の語だけを使う。推量を足さない）
      赤＝**583人死亡＋この回の核心**。3案を 210px で比べる：
          a **待ての声は届かず** … タイトルの二つ目の事実（「離陸は待て」の声が別の無線と重なった＝p40）
          b **来るはずのない空港** … 決め所#1＝タイトルのつかみ（16字＝型の上限を1字超える対照）
          c **同じ滑走路に2機** … 冒頭の引き（pr02「その滑走路に、ボーイング747が2機いた」）
        ⚠️ 「583」は報告書の表のマスの足し算（印字されていない）＝タイトルと同じ扱い（④'で承認）
        ⚠️ 「隠蔽」「衝撃」「闇」「結末」は逆効果／「即死」は出さない
      黄＝**通り名「テネリフェ」＋出来事**（12字）。タイトル末尾の事故名と同じ語
    ■ 地の作り
      🔴 **人の顔が1つも写っていない写真だけを地にする**。事故現場6点のうち
        `wreck_both_01`（手前に2人の顔）・`wreck_both_02`（エンジンの中に人）は採らない。
      `wreck_klm_01` は尾翼と胴体の骨組みが**画面の上下の中ほど**＝赤（上）と黄（下）の下に主役が来ない。
    """
    RED_A = "583人死亡 待ての声は届かず"      # 15字
    RED_B = "583人死亡 来るはずのない空港"    # 16字（型の上限を1字超える対照）
    RED_C = "583人死亡 同じ滑走路に2機"      # 15字
    YEL = "テネリフェ 空港衝突事故"          # 12字

    wreck = photo(EP9_WRECK, cy=0.40, cx=0.50, contrast=1.16, color=1.0, bright=0.96, trim=EP9_WRECK_TRIM)

    for nm, r in (("a_matte", RED_A), ("b_kuru", RED_B), ("c_niki", RED_C)):
        bake(f"ep9_{nm}", fx_type(wreck, r, YEL, "e_veil", yel_plain=True))


EP10_BEFORE = "ep10/sampoong_before_01.jpg"   # 서울연구원（1995年6月・公共ヌリ第1類型＋CC BY 4.0）：崩れる前の三豊百貨店
EP10_SITE = "ep10/site_cleanup_01.jpg"        # 서울역사편찬원（1995年・公共ヌリ第1類型）：崩れた跡地と重機


def ep10():
    """10本目（三豊百貨店）のサムネ（2026-09-20・⑥）。型は7〜9本目と同一＝**赤1行・黄1行・写真だけ**。

    ■ 🔴🔴 地に使える写真が**2点しかない**（この回だけの制約）
      この回の写真92点のうち **82点が CC BY-SA 4.0**。BY-SA は
      **切る・色を変える・上に文字を重ねると翻案**になり、継承が掛かる
      （→ 記憶 reference-cc-by-sa-unmodified-in-video・`ref/ep10/materials.md` §1）。
      サムネは**必ず切って文字を重ねる**ので、BY-SA の82点は地にできない。
      手直しが許されているのは公共ヌリ第1類型の10点だけで、そのうち
      **1280×720 に足りる大きさ**なのは `sampoong_before_01/02`（1600×1070）だけ。
      `site_cleanup_01`（809×534）は 1.58倍に伸びるが、人は10〜20pxで顔が立たない。
      ⚠️ `rescue_work_19` は顔が立つので採らない。

    ■ 決め語（④' で承認されたタイトルと、章の名前からだけ取る。推量を足さない）
      赤＝**502人死亡＋この回の核心**（どれも15字＝7〜9本目と同じ長さ）
          a/b **危険はないと診断** … タイトルの二つ目の事実（15時10分の診断）
          c    **床は朝から動いた** … 第1章の名前「その日の朝、床が動きだした」
      黄＝**通り名「三豊百貨店」＋出来事**（10字）。タイトル末尾の事故名と同じ語
      ⚠️ 「隠蔽」「衝撃」「闇」「結末」は逆効果（記憶 project-jiko-rules-index §3）
      ⚠️ 502 は白書の最終値（`c906`）＝タイトルと同じ扱い
    """
    RED_A = "502人死亡 危険はないと診断"    # 15字
    RED_C = "502人死亡 床は朝から動いた"    # 15字
    YEL = "三豊百貨店 崩壊事故"            # 10字

    # 崩れる前：看板「三豊百貨店」と OPEN の垂れ幕が帯の内側に来るよう上に寄せる
    before = photo(EP10_BEFORE, cy=0.35, cx=0.50, contrast=1.14, color=1.08, bright=0.97)
    # 崩れた跡地：重機と掘り下げられた穴が中央に来る
    site = photo(EP10_SITE, cy=0.50, cx=0.50, contrast=1.16, color=1.06, bright=0.97)

    bake("ep10_a_shindan", fx_type(before, RED_A, YEL, "e_veil", yel_plain=True))
    bake("ep10_b_ato", fx_type(site, RED_A, YEL, "e_veil", yel_plain=True))
    bake("ep10_c_yuka", fx_type(before, RED_C, YEL, "e_veil", yel_plain=True))


def ep10_t2():
    """10本目・2巡目（2026-09-21）。🔴 **赤の行から「死亡」を外す**（カズヤくん指示）。

    ■ 根拠：記憶 `feedback-jiko-death-word-policy` の表は
      「**タイトル・サムネの赤字は言い換え**（…犠牲者5名／生還者なし／全員が帰らなかった）」。
      ⚠️ ところが**4本目〜9本目は素の「死亡」で焼いていた**（98名死亡／3名死亡／6名死亡／
      2,973人死亡／7人死亡／583人死亡）。1本目「乗員5名 生還者なし」・2本目
      「生存者4人 全員が最後尾」だけが言い換え。**今回の指示は書いてある決まりのほうへ戻す。**

    ■ 赤の案（どれも14〜15字＝7〜9本目と同じ長さ。数字は必ず残す）
      d 犠牲502人 危険はないと診断 … タイトルの二つ目の事実
      e 犠牲502人 床は朝から動いた … 第1章の名前
      f 生還3人 帰らなかった502人  … **数字2つ**。`c815`（助け出された3人）＋白書の502人
      h 犠牲502人 店は開いたまま   … `ep14`「それでも、店は開いたままだった」
      i 跡地の写真に d と同じ赤
      g 🆕 **左右2枚並べ**（左＝崩れる前／右＝跡地）。`rival_type` の split を `fx_type` にも通した

    ■ 地に使える写真（⚠️ 1巡目の私の説明は絞りすぎだった）
      YouTube のサムネの規格は**推奨 3840×2160・最小幅 640px**（support.google.com/youtube/answer/72431）。
      公共ヌリ第1類型の10点は **809×534 でも規格内**＝`site_cleanup_01` も使える（1.58倍に伸びる）。
      使えないのは CC BY-SA の82点だけ（切る・文字を重ねる＝翻案）。
    """
    RED_D = "犠牲502人 危険はないと診断"   # 15字
    RED_E = "犠牲502人 床は朝から動いた"   # 15字
    RED_F = "生還3人 帰らなかった502人"    # 15字
    RED_H = "犠牲502人 店は開いたまま"     # 14字
    YEL = "三豊百貨店 崩壊事故"           # 10字

    before = photo(EP10_BEFORE, cy=0.35, cx=0.50, contrast=1.14, color=1.08, bright=0.97)
    site = photo(EP10_SITE, cy=0.50, cx=0.50, contrast=1.16, color=1.06, bright=0.97)
    # 右半分は**その枠の寸法で**作る（640×720）。1280幅のものを入れると倍に寄る
    site_r = photo(EP10_SITE, cy=0.50, cx=0.55, contrast=1.16, color=1.06, bright=0.97,
                   w=640, h=H)

    bake("ep10_d_gisei", fx_type(before, RED_D, YEL, "e_veil", yel_plain=True))
    bake("ep10_e_yuka", fx_type(before, RED_E, YEL, "e_veil", yel_plain=True))
    bake("ep10_f_seikan", fx_type(before, RED_F, YEL, "e_veil", yel_plain=True))
    bake("ep10_g_split", fx_type(before, RED_D, YEL, "e_veil", yel_plain=True,
                                 split=(site_r, 640)))
    bake("ep10_h_mise", fx_type(before, RED_H, YEL, "e_veil", yel_plain=True))
    bake("ep10_i_ato", fx_type(site, RED_D, YEL, "e_veil", yel_plain=True))

EP8_WIDE = "ep8/launch_wide.jpg"       # NASA KSC-03pd0134（2003年）：湿地ごしの打ち上げ（PD）


def ep8_t2():
    """8本目（コロンビア号）のサムネ差し替え（2026-09-21・公開ずみ動画の張り替え）。

    🔴 カズヤくん指示「**『死亡』という単語を含まない版**」＋「変更するのは8本目だけ」。
       赤は **A案＝いまの文言のまま「死亡」だけ言い換え**（記憶 feedback-jiko-death-word-policy の
       表がもともと「タイトル・サムネの赤字は言い換え」と書いている。4〜9本目がそこから外れていた）。
       ⚠️ 黄「コロンビア号 空中分解」と型は**変えない**。すでに数字が付いている動画なので直す所は最小に。

    ■ 地の候補（90点から「**顔が1つも写っていない**・1280px以上・横長」で絞った3点。全部 NASA の PD）
       a `launch_sky`  … いま公開中の地
       b `pad_stack`   … 夕方の射点に立つ機体。**機体に "Columbia" の文字が読める**
                          ⚠️ 左下に 30px ほどの人影が1つ（顔は判別できない）
       c 同上を**寄せて人影を画面外に落とした**もの（zoom 1.25・cx 0.62・cy 0.30）
       d `launch_wide` … 湿地ごしの打ち上げ。水面に炎が映る。⚠️ 機体が小さい
       ❌ et_orange（下部に人が3人）／le_fixture2（顔が2つ）／atlantis_nose（別の機体）
    """
    RED = "犠牲7人 求めは三度退けられた"     # 15字（公開中は「7人死亡 求めは三度退けられた」＝同じ15字）
    YEL = "コロンビア号 空中分解"            # 11字（変えない）

    sky = photo(EP8_LAUNCH, cy=0.46, cx=0.56, contrast=1.16, color=1.08, bright=0.94)
    pad = photo(EP8_PAD, cy=0.42, cx=0.56, contrast=1.14, color=1.06, bright=0.97)
    padz = photo(EP8_PAD, cy=0.30, cx=0.62, zoom=1.25,
                 contrast=1.14, color=1.06, bright=0.97)
    wide = photo(EP8_WIDE, cy=0.44, cx=0.50, contrast=1.16, color=1.08, bright=0.96)

    for nm, hero in (("a_sky", sky), ("b_pad", pad), ("c_padzoom", padz), ("d_wide", wide)):
        bake(f"ep8t2_{nm}", fx_type(hero, RED, YEL, "e_veil", yel_plain=True))


def ep10_ai():
    """10本目・A/Bテスト用（2026-09-21）。**地だけ OpenAI 画像APIで作った版**。

    ■ 文字は1字も変えない＝赤「犠牲502人 危険はないと診断」／黄「三豊百貨店 崩壊事故」。
      `ep10_g_split`（現行・採用ずみ）が対照群で、こちらが挑戦側。
    ■ 地の生成＝`tools/gen_thumb_ai.py`（`gpt-image-2.5-flare` high 1792x1008）。
      a＝断面（なぜ落ちたか）／b＝建物1枚（強い1枚）
    ⚠️ **写真用の補正をそのまま当てない。** `photo()` の既定（contrast 1.18・color 1.12）は
      粒状のスキャン写真を締めるための値で、もともと滑らかなクレイ調に当てると
      桃色が飽和して**赤に寄る**（＝上に載る赤 #c30a08 と喧嘩する）。ここは素に近づける。
    """
    RED_D = "犠牲502人 危険はないと診断"   # 15字（現行と同じ）
    YEL = "三豊百貨店 崩壊事故"           # 10字（現行と同じ）

    # a・b＝クレイ調（2026-09-21 に不採用。記録として残す）
    # c・d＝実写（カズヤくん指示「写真に近い質感で悲劇が伝わる」「背景も実写」）
    #   ⚠️ 実写の地は写真なので、`photo()` の既定の補正（contrast 1.18・color 1.12）を当てる。
    #     クレイ調で使った素通し（1.03 / 1.00）は、粒状の写真だと眠い絵になる。
    for nm in ("a", "b"):
        hero = photo(f"ep10/ai/ep10_{nm}.jpg", cy=0.50, cx=0.50,
                     contrast=1.03, color=1.00, bright=1.00)
        bake(f"ep10ai_{nm}", fx_type(hero, RED_D, YEL, "e_veil", yel_plain=True))
    for nm in ("c", "d"):
        hero = photo(f"ep10/ai/ep10_{nm}.jpg", cy=0.50, cx=0.50,
                     contrast=1.14, color=1.08, bright=0.97)
        bake(f"ep10ai_{nm}", fx_type(hero, RED_D, YEL, "e_veil", yel_plain=True))


def ep10_ai2():
    """10本目・**崩落の瞬間**の地（2026-09-22 カズヤくん指示）。

    「百貨店が今まさに崩壊しているような実写画像」「とにかく派手で目を引くように。
      しかし現実感のある、実際の事件を再現するような程度で」
    地＝`tools/gen_thumb_ai.py e`（`ref/ep10/ai/ep10_e.jpg`）。

    ⚠️ **文字は1字も変えない**＝赤「犠牲502人 危険はないと診断」／黄「三豊百貨店 崩壊事故」。
       公開中の `ep10_g_split` と**絵だけが違う**形にして、比べられるようにする。
    ⚠️ 補正は c・d と同じ実写側の値（クレイ調の素通しだと眠い絵になる）。
    🔴 この地は**サムネだけ**に使う。本編の画には1カットも入れない
       （AI で作った絵を、一次資料で検証する本編に混ぜない）。
    """
    RED_D = "犠牲502人 危険はないと診断"   # 15字（公開中と同じ）
    YEL = "三豊百貨店 崩壊事故"           # 10字（公開中と同じ）
    hero = photo("ep10/ai/ep10_e.jpg", cy=0.50, cx=0.50,
                 contrast=1.14, color=1.08, bright=0.97)
    bake("ep10ai_e_kuzure", fx_type(hero, RED_D, YEL, "e_veil", yel_plain=True))


EP11_ICE_PAD = "ep11/ice_pad.jpg"        # NASA GPN-2004-00011（1986-01-28）：発射台に張った氷（PD）
EP11_EGRESS = "ep11/ice_egress.jpg"      # NASA（1986年）：乗員が逃げる通路まで凍った発射塔（PD）
EP11_TEACHER = "ep11/mcauliffe_class.jpg"  # NASA（1985年）：教師として選ばれたマコーリフの公式肖像（PD）
EP11_PAD_AM = "ep11/launch_pad_morning.jpg"  # NASA STS-51-L.jpg（1986年）：その朝の発射台（PD）


def ep11():
    """11本目・チャレンジャー号（2026-09-22・⑥）。

    🔴🔴 **「爆発」はタイトルにもサムネにも使わない**（①で確定）。
       8本目コロンビア号と**同じ「空中分解」の回**なので、
       差し分けは **「氷」と「教師」**（→ 記憶 `project-jiko-ep11-challenger`）。
    🔴 **「犠牲7人」をサムネの核にしない**（8本目の赤が「7人死亡…」で真正面から重なる）。
       数字は **2.2度** と **「7人のうち1人」** で出す。
    ⚠️ 赤の行は**言い換え**（→ 記憶 `feedback-jiko-death-word-policy`）。
       この4案はどれも「死亡」を書いていない。
    ⚠️ 🔴 **`d` の文言を「全員が反対」にしてはいけない。**原文（ch5 L654）は
       ボイジョリー個人の証言で、④' が「賛成する発言は一度も出なかった」→
       **「技術者は、ひとりも賛成しなかった」**に絞り直している。
       「反対した」は報告書が書いていない一歩先（→ [[feedback-dont-state-inferences-as-findings]]）。
    ⚠️ 地に使えるのは **2,000px 以上の写真だけ**。記録映像から抜いた止め絵（640×480）は
       1280幅に伸ばすと粗が出るので使わない（`ice_icicle` 系は不可）。
    """
    RED_A = "発射台につららが下がっていた"   # 14字・氷
    RED_B = "打ち上げの朝 気温は2.2度"       # 14字・氷＋数字（pr08＝摂氏2.2度）
    RED_C = "乗員7人のうち1人は現役教師"     # 14字・教師＋数字（pr05）
    RED_D = "前の夜 技術者は賛成しなかった"   # 14字・決め所 pr04 のまま
    YEL = "チャレンジャー号 空中分解"        # 13字・世間で通っている短い呼び名を使う

    for red in (RED_A, RED_B, RED_C, RED_D):
        for bad in ("死亡", "爆発", "ﾀﾋ"):
            if bad in red:
                raise SystemExit(f"🔴 赤の行に使ってはいけない語「{bad}」がある: {red}")

    ice = photo(EP11_ICE_PAD, cy=0.50, cx=0.50, contrast=1.14, color=1.08, bright=0.97)
    egress = photo(EP11_EGRESS, cy=0.45, cx=0.50, contrast=1.14, color=1.08, bright=0.97)
    teacher = photo(EP11_TEACHER, cy=0.38, cx=0.50, contrast=1.12, color=1.06, bright=0.99)
    pad_am = photo(EP11_PAD_AM, cy=0.50, cx=0.50, contrast=1.14, color=1.08, bright=0.97)
    # 右半分は**その枠の寸法で**作る（640×720）。1280幅のものを入れると倍に寄る
    teacher_r = photo(EP11_TEACHER, cy=0.36, cx=0.50, contrast=1.12, color=1.06,
                      bright=0.99, w=640, h=H)

    bake("ep11_a_tsurara", fx_type(ice, RED_A, YEL, "e_veil", yel_plain=True))
    bake("ep11_b_kion", fx_type(egress, RED_B, YEL, "e_veil", yel_plain=True))
    bake("ep11_c_kyoshi", fx_type(teacher, RED_C, YEL, "e_veil", yel_plain=True))
    bake("ep11_d_zenya", fx_type(pad_am, RED_D, YEL, "e_veil", yel_plain=True))
    # e＝10本目で採用された左右2枚並べ。左＝氷／右＝教師＝この回の差し分けを1枚で見せる
    bake("ep11_e_split", fx_type(ice, RED_A, YEL, "e_veil", yel_plain=True,
                                 split=(teacher_r, 640)))


def ep11_t2():
    """11本目・2巡目（2026-09-22・⑥）。1巡目を**原寸と幅246pxの両方で見て**直した。

    ■ 1巡目で出た粗（`out/thumb/ep11-t1`）
      | 案 | 粗 | 直し |
      |---|---|---|
      | `d_zenya` | 🔴 **絵と文字が食い違う**（文字は「前の夜」／絵は**昼の打ち上げ**） | 絵に合う文字（気温）へ |
      | `b_kion`  | 🔴 つららの列が**下端で切れ**、上半分が正体不明の暗い形 | `cy` 0.45→**0.62**（列を中央へ） |
      | `a_tsurara` | ⚠️ 原寸では氷が見えるが、**小さくすると灰色の塊** | **1.6倍に寄せる** |
      | `e_split` | ⚠️ 左が灰色の塊・右の顔も小さい＝`c` より弱い | 2巡目では作らない |
      | `c_kyoshi` | ⭕ いちばん強い（顔が大きい・色がある・246pxで読める） | 顔の余白だけ少し足す |

    ⚠️ 直したのは**切り位置と文字の当て先だけ**。赤・黄の型と、
       「爆発／死亡を使わない」「犠牲7人を核にしない」は1巡目と同じ。
    """
    RED_A = "発射台につららが下がっていた"   # 14字・氷
    RED_B = "打ち上げの朝 気温は2.2度"       # 14字・氷＋数字（pr08＝摂氏2.2度）
    RED_C = "乗員7人のうち1人は現役教師"     # 14字・教師＋数字（pr05）
    YEL = "チャレンジャー号 空中分解"        # 13字

    for red in (RED_A, RED_B, RED_C):
        for bad in ("死亡", "爆発", "ﾀﾋ"):
            if bad in red:
                raise SystemExit(f"🔴 赤の行に使ってはいけない語「{bad}」がある: {red}")

    # f＝1巡目でいちばん目を引いた絵（打ち上げ）に、**絵と合う文字**を当てた
    launch = photo(EP11_PAD_AM, cy=0.50, cx=0.50, contrast=1.14, color=1.08, bright=0.97)
    # g＝1巡目の c。顔の上に赤がかぶらないよう cy を下げて余白を足す
    teacher = photo(EP11_TEACHER, cy=0.44, cx=0.50, contrast=1.12, color=1.06, bright=0.99)
    # h＝つららの列を中央に置き直した（1巡目は下端で切れていた）
    egress = photo(EP11_EGRESS, cy=0.62, cx=0.50, contrast=1.16, color=1.08, bright=0.99)
    # j＝1巡目の a を 1.6倍に寄せた（小さくしたとき何が写っているか分かるように）
    ice_z = photo(EP11_ICE_PAD, cy=0.45, cx=0.50, zoom=1.6,
                  contrast=1.18, color=1.08, bright=1.00)

    bake("ep11_f_launch_kion", fx_type(launch, RED_B, YEL, "e_veil", yel_plain=True))
    bake("ep11_g_kyoshi2", fx_type(teacher, RED_C, YEL, "e_veil", yel_plain=True))
    bake("ep11_h_tsurara2", fx_type(egress, RED_A, YEL, "e_veil", yel_plain=True))
    bake("ep11_j_tsurara3", fx_type(ice_z, RED_A, YEL, "e_veil", yel_plain=True))


def ep11_t3():
    """11本目・3巡目（2026-09-22・⑥）。**教師の案だけ**を直す。

    🔴🔴 2巡目の `g_kyoshi2` は**悪化した**。`cy` を 0.38→0.44 に上げたのは
       「顔に余白を足す」つもりだったが、`photo()` の `cy` は**切り出す窓の上端の位置**で、
       上げると窓が下へ動く＝**被写体は画面の上へ寄る**。結果、赤い帯が**目を完全に隠した**。
       → **下げる**のが正しい（→ [[feedback-verify-your-own-instrument]]＝物差しの向きをまず疑う）。
    ⚠️ 2巡目で通ったもの（`f_launch_kion`・`h_tsurara2`）は**触らない**。

    ■ この巡で作るもの
      k … 教師 `cy=0.30`（目が帯の下に出るはず）
      m … 教師 `cy=0.22`（さらに下げた控え）
      n … 左＝つらら（2巡目で読めるようになった切り）／右＝教師＝この回の差し分けを1枚で
    """
    RED_A = "発射台につららが下がっていた"
    RED_C = "乗員7人のうち1人は現役教師"
    YEL = "チャレンジャー号 空中分解"

    k = photo(EP11_TEACHER, cy=0.30, cx=0.50, contrast=1.12, color=1.06, bright=0.99)
    m = photo(EP11_TEACHER, cy=0.22, cx=0.50, contrast=1.12, color=1.06, bright=0.99)
    egress = photo(EP11_EGRESS, cy=0.62, cx=0.50, contrast=1.16, color=1.08, bright=0.99)
    # 右半分は**その枠の寸法で**作る（640×720）
    teacher_r = photo(EP11_TEACHER, cy=0.30, cx=0.50, contrast=1.12, color=1.06,
                      bright=0.99, w=640, h=H)

    bake("ep11_k_kyoshi3", fx_type(k, RED_C, YEL, "e_veil", yel_plain=True))
    bake("ep11_m_kyoshi4", fx_type(m, RED_C, YEL, "e_veil", yel_plain=True))
    bake("ep11_n_split2", fx_type(egress, RED_A, YEL, "e_veil", yel_plain=True,
                                  split=(teacher_r, 640)))


def ep11_t4():
    """11本目・4巡目（2026-09-22・⑥）。**写真と切りは `m_kyoshi4` のまま固定**して、
    赤の行だけを差し替える（2026-09-22 カズヤくん指示「Mの写真で他の赤字案を」）。

    ⚠️ 文言はすべて台本第2版で**裏を取った行**からしか作っていない。
      p … `c210` の**決め所**そのもの（報告書がマコーリフの仕事をこう書いている）
      q … `pr01`／`pr09`（発射台の氷）＋ `c208`（教師）を1行に。この回の差し分け2つが同時に出る
      r … `c208`「中学と高校で、いろいろな教科を教えていた」＝採用中の案をより具体にした形
      s … `c209`「乗員に加わったのは1985年の7月。それから半年」
    🔴 どれも「死亡」「爆発」を使わず、「犠牲7人」を核にしていない（8本目と重ねないため）。
    ⚠️ 「高校教師」とだけ書かない＝**中学と高校の両方**を教えていた（`c208`）。
    """
    TEACHER_CY = 0.22          # ✅ m_kyoshi4 で採用された切り（帯と顔が離れる）
    RED = {
        "p_jugyou": "宇宙から授業をするはずだった",   # 14字・c210 の決め所
        "q_kori":   "教師が乗る朝 発射台は凍った",   # 14字・氷＋教師
        "r_chuko":  "7人の1人は中学と高校の教師",    # 14字・c208
        "s_hantoshi": "半年前に選ばれた 現役の教師",  # 14字・c209
    }
    YEL = "チャレンジャー号 空中分解"

    for nm, red in RED.items():
        for bad in ("死亡", "爆発", "ﾀﾋ"):
            if bad in red:
                raise SystemExit(f"🔴 {nm} の赤に使ってはいけない語「{bad}」がある: {red}")
        if not (10 <= len(red) <= 15):
            raise SystemExit(f"🔴 {nm} の赤が {len(red)}字（型は10〜15字）: {red}")

    hero = photo(EP11_TEACHER, cy=TEACHER_CY, cx=0.50,
                 contrast=1.12, color=1.06, bright=0.99)
    for nm, red in RED.items():
        bake(f"ep11_{nm}", fx_type(hero, red, YEL, "e_veil", yel_plain=True))


EP12_CLOSE = "ep12/fb_close_b.jpg"    # ENERGY.GOV HD.10.290（1954-03-01）：ブラボーの火球の寄り（PD・米国の職務著作）
EP12_AERIAL = "ep12/fb_aerial_a.jpg"  # NARA 146763394（RG 678・1954）：空から見たブラボーのキノコ雲（PD・§105）


def ep12():
    """12本目・キャッスル・ブラボー水爆実験（2026-09-24・⑥）1巡目。

    🔴 地は**ブラボーそのものの写真だけ**。ロメオ・ユニオン・ヤンキー（同じ作戦の別の実験）の雲は
       似て見えても使わない（絵が題と食い違う）。
    🔴 赤の行は**決め所（★＝原文に当てた行）**から取る。
       「2.5倍」（計算した数）・「知りながら撃った」（本文で伝説として扱う言葉）・「死亡」は使わない。
    ⚠️ 乗組員は私人＝顔の写る写真を地にしない（築地のマグロ検査 `jp_tuna_check` も外した）。
    ⚠️ 地は 2,000px 以上の写真だけ（映像から抜いた `fb_cNNN` は使わない）。
      a … `c409`★「予報：人の住む島々に、大きな降灰なし」（DNA p208）＋火球の寄り（暗い地で文字が立つ）
      b … a と同じ赤＋空から見たキノコ雲（形がいちばんはっきり・退色で赤紫）
      c … `c618`★「船は、部隊の誰にも気づかれなかった」（DNA p219）＋キノコ雲
      d … `c103`★「爆発の威力は、予想よりはるかに大きかった」（DNA p212）＋火球の寄り
    ⚠️ 赤の「島に」「部隊に」は★の範囲を落とさないための語（外すと言い過ぎになる）。
    """
    RED = {
        "a_yohou_close": "予報は 島に大きな降灰なし",     # 13字・c409
        "b_yohou_aerial": "予報は 島に大きな降灰なし",    # 13字・c409
        "c_gyosen_aerial": "漁船は 部隊に気づかれなかった",  # 15字（型の上限）・c618
        "d_iryoku_close": "威力は 予想をはるかに超えた",   # 14字・c103
    }
    YEL = "ビキニ水爆実験 第五福竜丸"    # 13字・日本で通っている呼び名（台本第2版 §1-1）＋船の名

    for nm, red in RED.items():
        for bad in ("死亡", "ﾀﾋ", "2.5倍", "知りながら"):
            if bad in red:
                raise SystemExit(f"🔴 {nm} の赤に使ってはいけない語「{bad}」がある: {red}")
        if not (10 <= len(red) <= 15):
            raise SystemExit(f"🔴 {nm} の赤が {len(red)}字（型は10〜15字）: {red}")

    close = photo(EP12_CLOSE, cy=0.55, cx=0.50, contrast=1.12, color=1.06, bright=1.00)
    aerial = photo(EP12_AERIAL, cy=0.40, cx=0.50, contrast=1.12, color=1.00, bright=0.98)
    hero = {"close": close, "aerial": aerial}
    for nm, red in RED.items():
        bake(f"ep12_{nm}", fx_type(hero[nm.rsplit('_', 1)[1]], red, YEL, "e_veil", yel_plain=True))


EP13_THY = "ep13/tcjau_fra_1974.jpg"   # RuthAS／CC BY 3.0：姉妹機 TC-JAU（トルコ航空の DC-10・1974-07-28 フランクフルト）
EP13_WRECK = "ep13/wreck_1997.jpg"     # Ian Abbott／CC BY 4.0：現場の森に残っていた 981便の破片（1997年）


def ep13():
    """13本目・トルコ航空981便（2026-09-25・⑥）1巡目。

    🔴 事故機 TC-JAV の写真は4点とも CC BY-SA＝文字を重ねると改変（継承の義務が付く）＝**地に使わない**
       （本編も額装・無改変だけ＝`ss.FRAME_ONLY`）。地は CC BY の2点から：
       thy   … 姉妹機 TC-JAU（同じ航空会社・同じ型・同じ年の色）。⚠️ 事故機そのものではない
       wreck … 現場の森に残っていた破片（981便そのもの・1997年）。⚠️ 210px で何の絵か分かるかを見る
    🔴 赤は §B5-5「犠牲N人＋この回だけの核心」と、★（原文に当てた決め所）そのままの1本。
       「死亡」・通説（ストライキ・ヒースロー・335人）は使わない。
      a … 犠牲346人＋「電話1本の約束」（第5章の章名・タイトルの2文目）＋ thy
      b … 犠牲346人＋「旅客機の半ドア」（c108〜c109 の言い方）＋ thy
      c … a と同じ赤 ＋ wreck
      d … `c103`★「危険は、前の事故ですでに明らかだった」を「危険は すでに明らかだった」に（仏 p105）＋ wreck
    ⚠️ 顔の写る写真は地にしない（§B5-4）。2点とも人は写っていない。
    """
    RED = {
        "a_yakusoku_thy": "犠牲346人 電話1本の約束",      # 14字
        "b_handoa_thy": "犠牲346人 旅客機の半ドア",       # 14字
        "c_yakusoku_wreck": "犠牲346人 電話1本の約束",    # 14字
        "d_kiken_wreck": "危険は すでに明らかだった",      # 13字・c103★
    }
    YEL = "トルコ航空981便の真相"    # 12字・日本で通っている呼び名＋「の真相」（§B5-1）

    for nm, red in RED.items():
        for bad in ("死亡", "ﾀﾋ", "ストライキ", "ヒースロー", "335"):
            if bad in red:
                raise SystemExit(f"🔴 {nm} の赤に使ってはいけない語「{bad}」がある: {red}")
        if not (10 <= len(red) <= 15):
            raise SystemExit(f"🔴 {nm} の赤が {len(red)}字（型は10〜15字）: {red}")

    thy = photo(EP13_THY, cy=0.50, cx=0.50, contrast=1.10, color=1.05, bright=1.00)
    wreck = photo(EP13_WRECK, cy=0.50, cx=0.50, contrast=1.12, color=1.05, bright=1.00)
    hero = {"thy": thy, "wreck": wreck}
    for nm, red in RED.items():
        bake(f"ep13_{nm}", fx_type(hero[nm.rsplit('_', 1)[1]], red, YEL, "e_veil", yel_plain=True))


if __name__ == "__main__":
    import sys
    if "ep13" in sys.argv:
        ep13()
    elif "ep12" in sys.argv:
        ep12()
    elif "ep10-ai2" in sys.argv:
        ep10_ai2()
    elif "ep11-t4" in sys.argv:
        ep11_t4()
    elif "ep11-t3" in sys.argv:
        ep11_t3()
    elif "ep11-t2" in sys.argv:
        ep11_t2()
    elif "ep11" in sys.argv:
        ep11()
    elif "ep8-t2" in sys.argv:
        ep8_t2()
    elif "ep10-ai" in sys.argv:
        ep10_ai()
    elif "ep10-t2" in sys.argv:
        ep10_t2()
    elif "ep10" in sys.argv:
        ep10()
    elif "ep9" in sys.argv:
        ep9()
    elif "ep8" in sys.argv:
        ep8()
    elif "ep7" in sys.argv:
        ep7()
    elif "keybridge" in sys.argv:
        keybridge()
    elif "sl1" in sys.argv:
        sl1()
    elif "surfside" in sys.argv:
        surfside()
    elif "thresher" in sys.argv:
        thresher()
    else:
        ja123()
