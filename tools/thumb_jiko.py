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


def photo(src, cy=0.5, contrast=1.18, color=1.12, bright=0.96, w=W, h=H, zoom=1.0, cx=0.5):
    """写真を箱いっぱいに切り出して data URI にする。

    zoom … 1.0 より大きいと**寄る**（2026-08-06 追加）。123便の飛行中の写真は
           機影が画面の35%しかなく、縮めると何の絵か分からなかった。
    cx   … 横方向の寄せ。既定は中央。
    """
    im = Image.open(HERE / "ref" / src).convert("RGB")
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


def fx_type(hero, red, yellow, fx, yel_plain=False, ground=True):
    """`rival_type` と同じ型のまま、**文字の質感だけ**を足す。

    yel_plain … 黄の行だけ**最初のデザイン**（単色ベタ＋黒フチ1本）に戻す
                （2026-08-06 カズヤくん指示「新案の赤字だけ残して黄色は元に戻す」）。
                ⚠️ 黄は下端に密着していて、下の暗幕と黒フチで十分に立つ。
                  二重フチ（外に白）を足すと**縁が主役になって字が読みにくくなる**側だった。
    ground    … 地の演出（上の暗幕・ビネット）を出すか。False で最初の地に戻る
    """
    k = FX[fx]
    g = [f'<image href="{hero}" x="0" y="0" width="{W}" height="{H}" '
         f'preserveAspectRatio="xMidYMid slice"/>']
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


if __name__ == "__main__":
    ja123()
