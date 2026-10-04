# -*- coding: utf-8 -*-
"""事故検証チャンネルのサムネ **B 様式**＝「ドキュメントストーリー844」の型（2026-10-03・18本目）。

■ なぜ別のファイルか
    A 様式（いまの型＝競合「ゆっくり事故検証」の赤1行＋黄1行＋全面の写真）は `thumb_jiko.py`。
    🔴 2026-10-03 カズヤくん：A と B の2つの様式で YouTube の「テストと比較」（サムネの A/B）をかけ、
    数値の良いほうを以後の標準にする。B は A と何もかも違うので、A の道具に混ぜず、ここに分ける
    （A の寸法を1画素も動かさないため）。
    ✅ 同日、B の型（B1＝断面図・B2＝実写）を**承認**。ただし予定を変えた：
       **18本目は A（旧版と同じ）だけで出し、テストはしない。A/B テストは17本目（18本目の次に出す回）から。**
       判定＝Studio が B を「ベスト」と出したときだけ B を標準に（「ほぼ同じ」「有意な結果なし」は A のまま）。
       18本目の B1・B2 は**承認ずみの型の見本**として残す（17本目はこの値で、17本目の言葉と絵で作る）。

■ 実測（2026-10-03・@docustory844 の全22本＝長尺だけ・maxresdefault 1280×720）
    正本＝Vault `Projects/事故検証-サムネ新様式-ドキュメントストーリー844の実測仕様-20261003.md`
    上位10本を原寸で見て、色の網（赤・黄・白）で拾った画素の外接枠で測った値：

    | 項目 | 実測 | ここでの値 |
    |---|---|---|
    | 書体 | **極太の明朝体**（線の端にウロコ）。一部に「かすれ」（斑点の欠け） | Noto Serif JP Black |
    | いちばん大きい語の字の高さ | 94〜195px・中央値 約137px（10本） | 赤 約140px |
    | 二番手の語 | 58〜95px | 白 約85px |
    | 赤 | `#f60805`（かすれ無しの7語の中央値）／かすれ有りは `#cb090a` 前後 | `RED` |
    | 黄 | `#fbfc0e`（純）と `#f5d610`（金寄り）の2系統 | `YEL`＝金寄り |
    | 白 | `#fefefe` | `WHT` |
    | フチ | **白・黄・赤とも黒**。インクの外 1〜10px が明るさ 2〜15＝黒いフチ約10px、その外 11〜18px に暗い影 | `EDGE`・`SHADOW` |
    | 色の分け方 | 1つの句の中で語ごとに白／黄／赤を替える（「地球で**最も深い**洞窟で」） | `seg()` |
    | 字の置き場 | 帯ではなく**絵の空いている所**。左の余白 20〜60px・上の行の上端 y=16〜68 | — |
    | 地 | 平均の明るさ 78/255・暗部（明るさ 0.2 未満）が約45%＝暗い | — |
    | 絵 | **断面図**（写真の質感の岩・白い輪郭線で切った空洞や水）12/22・**平らな色の人影**（赤が主）16/22・**赤い矢印** 16/22・**赤枠の実写の差し込み**（顔）7/22 | `ep18_b1()` |
    | 赤枠 | 太さ 約8px・`#de260c` | `FRAME` |

■ 再現するのは「型」だけ（🔴 外さない）
    配置・字の大きさ・色・書体の系統・絵の作り方。**DS844 の画像・ロゴ・チャンネル名・
    決まり文句・キャラクターは使わない。** 絵はここで描き、写真は手元の PD の記録だけ。

使い方： python tools/thumb_docu.py ep18 [--only=a,b1]
         出力＝out/thumb/ep18-ab/
"""
import base64
import io
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

import render
import thumb_jiko as TJ

HERE = Path(__file__).parent.parent
FONTS = HERE / "fonts"
OUT = HERE / "out" / "thumb" / "ep18-ab"
W, H = 1280, 720

# ── 実測した DS844 の値（2026-10-03）。**勝手に動かさない** ─────────────
RED = "#f60805"
RED_K = "#cb090a"        # かすれの赤（暗め）
YEL = "#f5d610"
WHT = "#fefefe"
EDGE = 20                # stroke の太さ。線の中心に乗るので外へ出るのは半分＝10px（実測の黒いフチ）
FRAME = "#de260c"        # 差し込み写真の赤枠
FRAME_W = 8
SIL = "#e3140c"          # 平らな人影（ここでは艦）の赤


def face_css():
    b = base64.b64encode((FONTS / "NotoSerifJP-Black.woff2").read_bytes()).decode()
    return (f"@font-face{{font-family:'NSJ';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:900;font-display:block;}}")


def uri(im, fmt="JPEG", q=92):
    buf = io.BytesIO()
    im.save(buf, fmt, quality=q) if fmt == "JPEG" else im.save(buf, fmt)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


# ── 質感（ノイズ）。DS844 の断面図は「写真の質感の岩」＋「暗い水」 ────────────
def fractal(w, h, seed, octaves=((8, 1.0), (24, 0.55), (80, 0.3), (240, 0.18))):
    """いくつかの細かさの乱数を足した 0〜1 の面。"""
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), float)
    for n, amp in octaves:
        g = rng.random((max(2, round(n * h / w)), n))
        acc += amp * np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), float) / 255
    acc -= acc.min()
    return acc / acc.max()


def colorize(f, dark, light):
    d, l = np.array(dark, float), np.array(light, float)
    return Image.fromarray((d + (l - d) * f[..., None]).clip(0, 255).astype(np.uint8))


def water(seed=3):
    """暗い海。上が少し明るい青緑・下ほど黒。光の筋をうすく。"""
    f = fractal(W, H, seed, ((6, 1.0), (20, 0.5), (70, 0.25)))
    y = np.linspace(0, 1, H)[:, None]
    one = np.ones((H, W))
    base = np.stack([(12 + 22 * (1 - y)) * one, (34 + 50 * (1 - y)) * one, (46 + 58 * (1 - y)) * one], -1)
    base = base * (0.66 + 0.30 * f[..., None])
    # 光の筋（左上から斜めに）
    xx = np.linspace(0, 1, W)[None, :]
    ray = np.clip(np.sin((xx * 5.5 - y * 2.2) * np.pi) ** 8, 0, 1) * np.clip(1 - y * 1.6, 0, 1) * 26
    base += ray[..., None] * np.array([0.6, 1.0, 1.0])
    return Image.fromarray(base.clip(0, 255).astype(np.uint8))


def rock(seed=7, dark=(38, 32, 28), light=(150, 132, 112)):
    """岩の断面（灰色がかった茶）。細かい凹凸の陰影で写真らしく。dark／light で濃淡の幅を変える。"""
    f = fractal(W, H, seed, ((10, 1.0), (40, 0.6), (140, 0.45), (420, 0.35)))
    im = colorize(f, dark, light)
    em = im.filter(ImageFilter.EMBOSS).convert("L")
    a = np.asarray(im, float) * (0.55 + 0.6 * np.asarray(em, float)[..., None] / 255)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def speckle(w, h, seed=11, frac=0.10):
    """かすれ用の斑点（白＝見える・黒＝欠け）。"""
    f = fractal(w, h, seed, ((40, 1.0), (160, 0.7), (480, 0.5)))
    m = (f < np.quantile(f, frac)).astype(np.uint8) * 255
    return Image.fromarray(255 - m).convert("L")


# ── 文字 ───────────────────────────────────────────────
def seg(parts, x, base, anchor="start", kasure=None):
    """1行を語ごとの色で組む。parts = [(語, 色, font-size), ...]（同じベースライン）。

    描く順＝影（ぼかし）→ 黒いフチ → 黒い塗り → 色の塗り（かすれは色の塗りだけ欠く＝欠けから黒が見える）
    """
    parts = [p if len(p) == 4 else (*p, 0) for p in parts]     # (語, 色, font-size, 前の語との間 dx)
    spans = "".join(f'<tspan font-size="{fs}" dx="{dx}" fill="{c}">{t}</tspan>' for t, c, fs, dx in parts)
    blk = "".join(f'<tspan font-size="{fs}" dx="{dx}">{t}</tspan>' for t, c, fs, dx in parts)
    head = f'x="{x}" y="{base}" font-family="NSJ" font-weight="900" text-anchor="{anchor}"'
    g = [f'<text {head} fill="#000" stroke="#000" stroke-width="{EDGE + 10}" stroke-linejoin="round" '
         f'filter="url(#sh)" opacity="0.85">{blk}</text>',
         f'<text {head} fill="#000" stroke="#000" stroke-width="{EDGE}" stroke-linejoin="round">{blk}</text>']
    mk = f' mask="url(#{kasure})"' if kasure else ""
    g.append(f'<text {head}{mk}>{spans}</text>')
    return "".join(g)


def defs(extra=""):
    return ('<defs><filter id="sh" x="-20%" y="-30%" width="140%" height="160%">'
            '<feGaussianBlur stdDeviation="9"/></filter>'
            '<filter id="glow" x="-30%" y="-60%" width="160%" height="220%">'
            '<feGaussianBlur stdDeviation="14"/></filter>' + extra + '</defs>')


def bake(name, body, extra_defs="", out=None):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">{defs(extra_defs)}{body}</svg>')
    html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{face_css()}'
            f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{svg}</body></html>')
    out = out or OUT
    out.mkdir(parents=True, exist_ok=True)
    render.png(html, out / f"{name}.png", W, H)
    print(name, "->", out / f"{name}.png", flush=True)


# ── 艦の横からの形（平らな赤の影）。長さ 1000・中心線 y=0・胴の半径 56 ──────
#    スレッシャー級＝涙滴形の胴・前寄りの小さなセイル（潜舵つき）・十字の尾翼・推進器
SUB = ("M0,0 C0,-38 42,-56 115,-56 L600,-56 C765,-56 905,-30 988,-7 L1000,-7 L1000,7 L988,7 "
       "C905,30 765,56 600,56 L115,56 C42,56 0,38 0,0 Z "
       "M232,-54 L240,-140 Q244,-152 260,-152 L322,-152 Q334,-150 336,-138 L346,-54 Z "
       "M206,-114 L372,-114 L372,-103 L206,-103 Z "
       "M872,-30 L912,-104 L952,-104 L958,-16 Z M872,30 L912,104 L952,104 L958,16 Z "
       "M1000,-46 L1013,-46 L1013,46 L1000,46 Z")


def sub(x, y, s, deg, tex_id, bow_right=True):
    """艦の影を置く。(x, y)＝艦首の先。tex_id＝赤の質感のパターン（DS844 の人影はベタ塗りに暗い斑）。

    bow_right … 艦首を右に（形は艦首が x=0 なので左右を裏返す）。deg が負なら艦首が上がる。
    ⚠️ 1巡目は裏返し忘れで「艦首が下・艦尾が上」になっていた（記録は up angle＝艦首が上）。
    ⚠️ 縁の黒い線は付けない（DS844 の人影は縁なし＋赤い光のにじみ）。
    """
    sx = -s if bow_right else s
    tr = f'translate({x},{y}) rotate({deg}) scale({sx},{s})'
    return (f'<g transform="{tr}"><path d="{SUB}" fill="{SIL}" filter="url(#glow)" opacity="0.6"/>'
            f'<path d="{SUB}" fill="url(#{tex_id})"/></g>')


def block_arrow(x0, y0, x1, y1, shaft=34, head=92, headlen=96):
    """太い直線の矢印（DS844 で多い形）。(x0,y0)→(x1,y1) の先が矢じり。"""
    import math
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    bx, by = x1 - ux * headlen, y1 - uy * headlen
    pts = [(x0 + px * shaft / 2, y0 + py * shaft / 2), (bx + px * shaft / 2, by + py * shaft / 2),
           (bx + px * head / 2, by + py * head / 2), (x1, y1),
           (bx - px * head / 2, by - py * head / 2), (bx - px * shaft / 2, by - py * shaft / 2),
           (x0 - px * shaft / 2, y0 - py * shaft / 2)]
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + " Z"
    return (f'<path d="{d}" fill="#000" filter="url(#sh)" opacity="0.8"/>'
            f'<path d="{d}" fill="{RED}" stroke="#1a0000" stroke-width="5" stroke-linejoin="round"/>')


def inset(src, x, y, w, h, **kw):
    """赤枠の実写の差し込み（DS844 は実在の人の顔。ここでは艦の本物の写真）。"""
    u = TJ.photo(src, w=w, h=h, **kw)
    return (f'<rect x="{x - 4}" y="{y - 4}" width="{w + 8}" height="{h + 8}" fill="#000" filter="url(#sh)" opacity="0.9"/>'
            f'<image href="{u}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{FRAME}" stroke-width="{FRAME_W}"/>')


def seabed_path(seed=5, top=600):
    rng = np.random.default_rng(seed)
    xs = np.linspace(-20, W + 20, 42)
    ys = top + np.cumsum(rng.normal(0, 7, len(xs)))
    ys = ys - (ys.mean() - top)
    pts = " L".join(f"{x:.0f},{y:.0f}" for x, y in zip(xs, ys))
    return f"M-20,{H + 20} L{pts} L{W + 20},{H + 20} Z", f"M{pts}"


# ── 18本目 スレッシャー号 ─────────────────────────────────────
#    決め語は A と同じ（09-30 カズヤくん＝旧版と同じ・「圧壊」はこの回の決め）。
#    🔴 様式の比べっこなので **言葉は A と1字も変えない**：赤「129名圧壊」「海底2600m」・黄「機密解除された査問会記録」
TOP_W, TOP_Y = "機密解除された", "査問会記録"
RED_MAIN, SUB_LBL = "129名圧壊", "海底2600m"


def ep18_a():
    """A＝いまの様式＝旧版 3本目と同じ物（`thumb_jiko.thresher()` の `thr_film_b2` と同じ値）。"""
    hero = TJ.photo(TJ.TH_FILM_B, cy=0.50, contrast=1.26, color=1.20, bright=0.86, zoom=1.10)
    body = TJ.fx_type(hero, "129名圧壊 海底2600m", "機密解除された査問会記録", "e_veil", yel_plain=True)
    TJ.OUT = OUT
    TJ.bake("ep18_A_rival", body)


def ep18_b1():
    """B1＝DS844 の型でいちばん多い組み合わせ＝断面図＋平らな赤の主役＋赤い矢印＋赤枠の実写＋極太明朝。

    🔴 18本目だけの線（映像方針 §15）＝**深さの数を幾何で漏らさない**：目盛り・海面は描かない
       （艦と海底の距離から深さが読めないように）。艦は壊さない（圧壊の起き方は推定＝描かない）。
    """
    wat = uri(water())
    rk = uri(rock())
    sb_fill, sb_line = seabed_path()
    # 赤の質感（暗い斑）
    f = fractal(512, 160, 21, ((12, 1.0), (40, 0.6), (120, 0.4)))
    red_tex = colorize(f, (150, 6, 4), (236, 26, 16))
    sp = speckle(W, H, seed=13, frac=0.09)
    ex = (f'<pattern id="rt" patternUnits="userSpaceOnUse" width="1000" height="320" x="0" y="-160">'
          f'<image href="{uri(red_tex)}" width="1000" height="320" preserveAspectRatio="none"/></pattern>'
          f'<clipPath id="sbc"><path d="{sb_fill}"/></clipPath>'
          f'<mask id="ks" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
          f'<image href="{uri(sp, "PNG")}" width="{W}" height="{H}"/></mask>')
    g = [f'<image href="{wat}" width="{W}" height="{H}"/>',
         f'<image href="{rk}" width="{W}" height="{H}" clip-path="url(#sbc)"/>',
         f'<path d="{sb_line}" fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round"/>',
         # 艦（艦首が右・艦首が上＝記録の「up angle」の向き。角度の数は言わない）
         sub(800, 300, 0.70, -9, "rt"),
         block_arrow(330, 168, 520, 268),
         inset(TJ.TH_SEA, 905, 172, 330, 330, cx=0.42, cy=0.52, zoom=2.4, contrast=1.2, color=1.0, bright=0.95),
         # ビネット
         '<radialGradient id="vg" cx="0.5" cy="0.48" r="0.78"><stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.6"/></radialGradient>'
         f'<rect width="{W}" height="{H}" fill="url(#vg)"/>',
         # 字の大きさは書体の字幅から計算した（Noto Serif JP Black＝漢字の字の高さ 0.95em・上 0.856em）。
         #   上の行 12字＝12.0em → 100px 級で幅 1,200px・字の高さ 約95px（DS844 の二番手〜主の間）
         #   下の行 赤 4.69em×148＋白 5.475em×89＋間 24＝1,205px・赤の字の高さ 約141px（DS844 の主の中央値 137）
         seg([(TOP_W, WHT, 100), (TOP_Y, YEL, 100)], 40, 108, kasure="ks"),
         seg([(RED_MAIN, RED, 148), (SUB_LBL, WHT, 89, 24)], 38, 686)]
    bake("ep18_B1_docu", "".join(g), ex)


def ep18_b2():
    """B2＝DS844 のもう1つの型＝**実写の地**＋赤い矢印＋極太明朝（字は B1 と同じ置き方・同じ語）。

    🔴 DS844 は全期間の再生数では断面図が多いが、**直近の3本（公開3〜25日）はどれも実写の地**
       （日割りの再生数で1〜3位）。どちらが勝つ型かは公開日の古さで決められない＝両方を試せるようにする。
    地＝航走中の本物の写真（`TH_SEA`・セイルの「593」）。B1 の差し込みで見たセイルの位置から、
       1.3倍・cx 0.42・cy 0.52 でセイルが x≈605〜835・y≈196〜401 に来る（計算）→ 矢印はセイルへ。
    """
    hero = TJ.photo(TJ.TH_SEA, cx=0.42, cy=0.52, zoom=1.3, contrast=1.25, color=1.0, bright=0.80)
    sp = speckle(W, H, seed=13, frac=0.09)
    ex = (f'<mask id="ks" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
          f'<image href="{uri(sp, "PNG")}" width="{W}" height="{H}"/></mask>')
    g = [f'<image href="{hero}" width="{W}" height="{H}"/>',
         '<radialGradient id="vg" cx="0.55" cy="0.5" r="0.75"><stop offset="0.45" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.75"/></radialGradient>'
         f'<rect width="{W}" height="{H}" fill="url(#vg)"/>',
         # 上下の字の下をうすく締める（DS844 の実写の回も字の下は暗い）
         '<linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.55"/>'
         '<stop offset="0.25" stop-color="#000" stop-opacity="0"/><stop offset="0.72" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.65"/></linearGradient>'
         f'<rect width="{W}" height="{H}" fill="url(#tb)"/>',
         block_arrow(400, 205, 600, 300),
         seg([(TOP_W, WHT, 100), (TOP_Y, YEL, 100)], 40, 108, kasure="ks"),
         seg([(RED_MAIN, RED, 148), (SUB_LBL, WHT, 89, 24)], 38, 686)]
    bake("ep18_B2_docu_photo", "".join(g), ex)


# ── 16本目 バイオントダム（2026-10-04・公開ずみ `y3v7q6YKBpk` で B の型を試す）──────────────
#    🔴 カズヤくん（10-04）「16本目のサムネを B1・B2 の型で作成。実際に差し替えてテストしてみる。差し替えは手動」
#       （記憶の「公開ずみの動画は直さない」は動画ファイルだけの決まり＝サムネはその外）
#    言葉は公開中の A（`thumb_jiko.ep16()` の `k_tsunami_AI`）と1字も変えない：
#       赤「津波1910人 予兆は3年前」→ 白「津波1910人」＋赤「予兆は3年前」（主＝この回の決め語）
#       黄「バイオントダムの真相」→ 黄「バイオントダム」＋白「の真相」
#    字幅（Noto Serif JP Black）：上の行 10.0em×116＝1,160px・字の高さ 約110px／
#       下の行 白 5.152em×82＋赤 5.612em×136＋間 24＝1,209px・赤の字の高さ 約129px
OUT16 = HERE / "out" / "thumb" / "ep16-ab"
TOP16 = [("バイオントダム", YEL, 116), ("の真相", WHT, 116)]
BOT16 = [("津波1910人", WHT, 82), ("予兆は3年前", RED, 136, 24)]

# 地形の線（左＝南のトック山・右＝北の岸＝本編 VB の向き：#100 の x=740 で西を向いた断面）
GROUND16 = [(-20, 175), (90, 170), (180, 215), (260, 275), (340, 345), (410, 420), (460, 475), (500, 505),
            (600, 505), (650, 470), (740, 410), (830, 350), (930, 300), (1040, 262), (1150, 240), (1300, 225)]


def _pts(ps):
    return " L".join(f"{x},{y}" for x, y in ps)


def ep16_b1():
    """B1＝断面図（本編の VB と同じ向き）＋平らな赤の主役（崩れた斜面の塊）＋赤い矢印＋赤枠の実写（#023）。

    🔴 本編に忠実に：塊は**1つのまま**左（南）の斜面から湖へ滑り、水は右（北）の岸を駆け上がる
       （本編の冒頭 c101 と同じ）。**ダムは壊さない**（この断面にダムは出ない＝差し込みの写真で見せる）。
       高さ・水位・深さの数は絵に入れない（目盛りなし）。
    赤い矢印は塊を指す＝決め語「予兆は3年前」（斜面は事故の3年以上前から動いていた）と組。
    差し込み＝#023 U.S. Army／PD（ダムが立ったまま・奥に谷を埋めた崩れた山と残った湖）。
    """
    sky = np.zeros((H, W, 3), float)
    y = np.linspace(0, 1, H)[:, None]
    f = fractal(W, H, 31, ((6, 1.0), (24, 0.4)))
    sky[..., 0] = 10 + 10 * (1 - y) + 8 * f
    sky[..., 1] = 14 + 16 * (1 - y) + 8 * f
    sky[..., 2] = 26 + 30 * (1 - y) + 10 * f
    sky_u = uri(Image.fromarray(sky.clip(0, 255).astype(np.uint8)))
    rk = uri(rock(seed=17, dark=(24, 20, 17), light=(178, 156, 128)))
    line = _pts(GROUND16)
    ground = f"M-20,{H + 20} L{line} L1300,{H + 20} Z"
    lake = "M442,455 L672,455 L650,470 L600,505 L500,505 L460,475 Z"
    # 🔴 1巡目は厚さ約45px の帯＝「塊が滑った」と読めなかった → 厚さ約110px・先端を湖へ（2巡目）
    mass = ("M128,189 L180,215 L260,275 L340,345 L410,420 L452,466 L535,468 L552,500 "
            "L472,542 L400,522 L330,472 L250,412 L170,347 L95,283 L62,232 Z")
    surge = "M590,452 Q690,424 755,398 L838,347 L905,312 L920,329 L852,369 L770,421 Q700,459 640,470 Z"
    f2 = fractal(512, 256, 23, ((12, 1.0), (40, 0.6), (120, 0.4)))
    red_tex = colorize(f2, (150, 6, 4), (236, 26, 16))
    sp = speckle(W, H, seed=13, frac=0.09)
    ex = (f'<pattern id="rt16" patternUnits="userSpaceOnUse" width="{W}" height="{H}">'
          f'<image href="{uri(red_tex)}" width="{W}" height="{H}" preserveAspectRatio="none"/></pattern>'
          f'<clipPath id="gc"><path d="{ground}"/></clipPath>'
          '<linearGradient id="lk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2aa7d6"/>'
          '<stop offset="1" stop-color="#0d4f78"/></linearGradient>'
          '<linearGradient id="sg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#bfefff"/>'
          '<stop offset="1" stop-color="#ffffff"/></linearGradient>'
          f'<mask id="ks" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
          f'<image href="{uri(sp, "PNG")}" width="{W}" height="{H}"/></mask>')
    g = [f'<image href="{sky_u}" width="{W}" height="{H}"/>',
         f'<image href="{rk}" width="{W}" height="{H}" clip-path="url(#gc)"/>',
         f'<path d="{lake}" fill="url(#lk)"/>',
         f'<path d="M{line}" fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round"/>',
         # 塊（赤い光のにじみ＋質感）
         f'<path d="{mass}" fill="{SIL}" filter="url(#glow)" opacity="0.6"/>',
         f'<path d="{mass}" fill="url(#rt16)"/>',
         # 北の岸を駆け上がる水
         f'<path d="{surge}" fill="#dff6ff" filter="url(#glow)" opacity="0.7"/>',
         f'<path d="{surge}" fill="url(#sg)"/>',
         # 駆け上がった水の先のしぶき
         "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" filter="url(#sh)" opacity="{o}"/>'
                 for cx, cy, r, o in ((900, 300, 30, 0.85), (930, 318, 22, 0.75), (870, 318, 20, 0.7),
                                      (820, 345, 16, 0.6), (915, 282, 16, 0.6))),
         block_arrow(545, 182, 330, 330),
         inset(EP16_A, 950, 168, 300, 280, cx=0.79, cy=1.0, zoom=1.2, contrast=1.15, color=1.0, bright=0.98),
         '<radialGradient id="vg" cx="0.5" cy="0.48" r="0.8"><stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient>'
         f'<rect width="{W}" height="{H}" fill="url(#vg)"/>',
         seg(TOP16, 40, 121, kasure="ks"),
         seg(BOT16, 36, 687)]
    bake("ep16_B1_docu", "".join(g), ex, out=OUT16)


def ep16_b2():
    """B2＝全面の絵＋赤い矢印＋極太明朝。🔴 地は**公開中の A と同じ生成の地**（`ref/ep16/ai/ep16_vaj_a_orig.png`）
    ＝絵を同じにして「字と矢印の様式」だけを比べる（18本目の B2 は実写の地だったが、16本目の A は生成の地）。
    矢印はダムの天端を越える水へ（地の天端は 1280 幅で y≈300・水の壁は x≈180〜970）。
    """
    hero = TJ.photo("ep16/ai/ep16_vaj_a_orig.png", cy=0.50, cx=0.50, contrast=1.06, color=1.02, bright=0.92)
    sp = speckle(W, H, seed=13, frac=0.09)
    ex = (f'<mask id="ks" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
          f'<image href="{uri(sp, "PNG")}" width="{W}" height="{H}"/></mask>')
    g = [f'<image href="{hero}" width="{W}" height="{H}"/>',
         '<linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.5"/>'
         '<stop offset="0.22" stop-color="#000" stop-opacity="0"/><stop offset="0.7" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.7"/></linearGradient>'
         f'<rect width="{W}" height="{H}" fill="url(#tb)"/>',
         block_arrow(95, 420, 330, 300),
         seg(TOP16, 40, 121, kasure="ks"),
         seg(BOT16, 36, 687)]
    bake("ep16_B2_docu_ai", "".join(g), ex, out=OUT16)


EP16_A = "ep16/dam_slide_1963.jpg"   # #023 U.S. Army／PD（`thumb_jiko.EP16_A` と同じ）


def night_sky(seed=31):
    """暗い夜空（上がわずかに明るい紺）。16本目の B1 と同じ作り。"""
    sky = np.zeros((H, W, 3), float)
    y = np.linspace(0, 1, H)[:, None]
    f = fractal(W, H, seed, ((6, 1.0), (24, 0.4)))
    sky[..., 0] = 10 + 10 * (1 - y) + 8 * f
    sky[..., 1] = 14 + 16 * (1 - y) + 8 * f
    sky[..., 2] = 26 + 30 * (1 - y) + 10 * f
    return uri(Image.fromarray(sky.clip(0, 255).astype(np.uint8)))


def day_gray(seed=43):
    """暗い灰色の地（図の背景）。🔴 昼の事故（14本目＝朝・15本目＝夕方前）に夜空を使うと「夜」と読める＝事実と合わない。
    16本目（22時39分）は夜空のまま。"""
    g = np.zeros((H, W, 3), float)
    y = np.linspace(0, 1, H)[:, None]
    f = fractal(W, H, seed, ((6, 1.0), (24, 0.4)))
    for k, (top, bot) in enumerate(((58, 30), (62, 33), (68, 37))):
        g[..., k] = bot + (top - bot) * (1 - y) + 10 * f
    return uri(Image.fromarray(g.clip(0, 255).astype(np.uint8)))


def red_pattern(pid, seed=23):
    f2 = fractal(512, 256, seed, ((12, 1.0), (40, 0.6), (120, 0.4)))
    tex = colorize(f2, (150, 6, 4), (236, 26, 16))
    return (f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{W}" height="{H}">'
            f'<image href="{uri(tex)}" width="{W}" height="{H}" preserveAspectRatio="none"/></pattern>')


def kasure_mask():
    sp = speckle(W, H, seed=13, frac=0.09)
    return (f'<mask id="ks" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<image href="{uri(sp, "PNG")}" width="{W}" height="{H}"/></mask>')


def darken_photo():
    """B2（全面の絵）の締め＝上下の暗幕＋周りを落とす（DS844 の実写の回は暗い）。"""
    return ('<linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.55"/>'
            '<stop offset="0.22" stop-color="#000" stop-opacity="0"/><stop offset="0.68" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.72"/></linearGradient>'
            f'<rect width="{W}" height="{H}" fill="url(#tb)"/>'
            '<radialGradient id="vg" cx="0.5" cy="0.5" r="0.78"><stop offset="0.5" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.6"/></radialGradient>'
            f'<rect width="{W}" height="{H}" fill="url(#vg)"/>')


# ── 14本目 セウォル号（2026-10-04・公開ずみ `WqhSTqWvqAc` で B の型を試す）──────────────
#    🔴 カズヤくん（10-04）「セウォル号、リノ・エアレースの動画も B タイプのサムネを作成。16本目同様にテスト」
#    言葉は公開中の A（`thumb_jiko.ep14_ai_zoom()` の z2）と1字も変えない：
#       赤「犠牲304人 退船命令は出ず」→ 白「犠牲304人」＋赤「退船命令は出ず」（主）／黄「セウォル号沈没の真相」→ 黄「セウォル号」＋白「沈没の真相」
#    字幅：上の行 10.0em×116＝1,160px／下の行 白×71＋赤×119＋間 24＝約1,200px（赤の字の高さ 約113px）
OUT14 = HERE / "out" / "thumb" / "ep14-ab"
TOP14 = [("セウォル号", YEL, 116), ("沈没の真相", WHT, 116)]
BOT14 = [("犠牲304人", WHT, 71), ("退船命令は出ず", RED, 119, 24)]
EP14_SHIP = "ep14/sewol_incheon.jpg"   # jinjoo2713／PD：沈む20日前、仁川港のセウォル号（`thumb_jiko.EP14_SHIP` と同じ）

# 船の寸法（メートル）＝本編の `tools/hull.py` の値（海審 p1013・p1018〜1019）
#    全長 145.61・幅 22（HALF 11）・C甲板 14.00・3階（B甲板）18.95・4階（A甲板）21.65・5階（船橋甲板）24.25・操舵室の前の端 97
#    🔴 煙突の位置と大きさ・船首と船尾の線・船底の丸みは模式（hull.py と同じく記録に無い）
HEEL14 = 52.2                        # 🔴 海審 p1057「B甲板の左舷が水面に届くほど（傾き約52.2度）」＝本編 hull の front と同じ考え


def sewol_side(heel=HEEL14):
    """左舷へ heel 度傾いた船を**右舷の側から**見た横の形（船尾 x=0 → 船首 x=145.61・高さ z' は傾けたあとの上下）。

    🔴 1巡目は本編 hull の front（船首の側から見た断面）をそのまま傾けた＝**赤い箱にしか見えず船と読めなかった**
       → 横の形に替えた。傾きは「右舷の側から見た高さ」の計算に入れる：z' ＝ z・cos θ ＋ y・sin θ（y＝右舷が＋）。
       水面＝3階の左舷の端（y −11・z 18.95）の z'＝本編と同じ記録（52.2度で3階の左舷の端が水面に届く）。
       ＝水面の上に**船底の帯**（右舷の湾曲部 z' 8.69 から下）が出る＝いまのサムネの生成の地と同じ見え方。
    """
    th = math.radians(heel)
    c, sn = math.cos(th), math.sin(th)
    zp = lambda z, y: z * c + y * sn
    v = dict(water=zp(18.95, -11), bilge=zp(0, 11), pbilge=zp(0, -11), cdeck=zp(14.0, 11),
             bdeck=zp(18.95, 11), adeck=zp(21.65, 11), brdeck=zp(24.25, 10))
    L, top, fun = 145.61, v["brdeck"], v["brdeck"] + 2.5
    outline = [(0, 3.5), (0, v["adeck"]), (2, v["adeck"]), (2, top), (30, top), (31, fun), (39, fun), (40, top),
               (97, top), (98, v["adeck"] - 1), (100, v["cdeck"]), (138, v["cdeck"] + 1.2), (L, v["cdeck"] + 2.5),
               (L, 12), (142, -2), (128, v["pbilge"]), (14, v["pbilge"]), (2, -1)]
    bottom = [(6, v["bilge"]), (135, v["bilge"]), (141, 2), (128, v["pbilge"]), (14, v["pbilge"]), (3, 0)]
    return outline, bottom, v


def ep14_b1():
    """B1＝横から見た図（海の断面）＋平らな赤の主役（傾いた船）＋赤い矢印＋赤枠の実写（沈む20日前の船・PD）。

    🔴 本編に忠実に：傾き＝左舷へ 52.2度（海審 p1057）・水面＝3階の左舷の端が水面に届く高さ（本編 hull の front と同じ記録）。
       右舷の側から見る＝船首が右。人は描かない（本編も亡くなった方の数に人の形を使っていない＝§C-1 #59）。角度の数は絵に入れない。
    矢印は3階・4階（客室）へ。
    """
    # 🔴 2巡目（640px で見た）：赤一色だと「まっすぐ浮いた船」に見えた＝傾きが伝わらない
    #    → 船底の帯を暗い色にして白い線（喫水の上の塗り分けの線）で分け、客室の窓の列を足し、船を大きく（3巡目）
    s, x0, water = 6.0, 30.0, 440.0       # 船首の先＝x 904（6.2 では差し込みの下にもぐった）
    outline, bottom, v = sewol_side()
    tr = lambda pts: [(round(x0 + s * x, 1), round(water - s * (z - v["water"]), 1)) for x, z in pts]
    ship = "M" + _pts(tr(outline)) + " Z"
    band = "M" + _pts(tr(bottom)) + " Z"
    decks = "".join(f'<path d="M{_pts(tr([(0, v[k]), (x1, v[k])]))}" stroke="#6e0000" stroke-width="3" fill="none"/>'
                    for k, x1 in (("cdeck", 100), ("bdeck", 97)))
    ex = (red_pattern("rt14") + kasure_mask() +
          '<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a9fd4"/>'
          '<stop offset="1" stop-color="#062a45"/></linearGradient>')
    # 客室の窓（3階・4階の帯に2列・間隔 2.4m・灯りではない＝暗い赤）
    wins = []
    for z0, z1 in ((v["bdeck"], v["adeck"]), (v["adeck"], v["brdeck"])):
        zc, hh = (z0 + z1) / 2, max(0.35, (z1 - z0) * 0.45)
        for xm in np.arange(5.0, 95.0, 2.4):
            (ax, ay), (bx, by) = tr([(xm, zc + hh / 2), (xm + 1.3, zc - hh / 2)])
            wins.append(f'<rect x="{ax}" y="{ay}" width="{bx - ax:.1f}" height="{by - ay:.1f}" fill="#5c0000"/>')
    bilge_line = f'<path d="M{_pts(tr([(6, v["bilge"]), (135, v["bilge"])]))}" stroke="#ffffff" stroke-width="3"/>'
    g = [f'<image href="{day_gray(41)}" width="{W}" height="{H}"/>',
         f'<path d="{ship}" fill="{SIL}" filter="url(#glow)" opacity="0.6"/>',
         f'<path d="{ship}" fill="url(#rt14)"/>',
         f'<path d="{band}" fill="#3a0a0a"/>', bilge_line, decks, "".join(wins),
         # 海（船の沈んだ所は海の色が重なって見える）
         f'<rect x="0" y="{water}" width="{W}" height="{H - water}" fill="url(#sea)" opacity="0.8"/>',
         f'<path d="M0,{water} L{W},{water}" stroke="#ffffff" stroke-width="5"/>',
         block_arrow(250, 185, 400, 316),
         inset(EP14_SHIP, 950, 168, 300, 280, cx=0.682, cy=1.0, zoom=1.397, contrast=1.12, color=1.05, bright=0.98),
         '<radialGradient id="vg" cx="0.5" cy="0.48" r="0.8"><stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient>'
         f'<rect width="{W}" height="{H}" fill="url(#vg)"/>',
         seg(TOP14, 40, 121, kasure="ks"),
         seg(BOT14, 38, 689)]
    bake("ep14_B1_docu", "".join(g), ex, out=OUT14)


def ep14_b2():
    """B2＝公開中の A と同じ生成の地（z2 の寄り）＋赤い矢印＋極太明朝＝字と矢印の様式だけを比べる。
    地の船＝横いっぱい（y≈240〜450）。矢印は上の甲板へ。"""
    import thumb_jiko as T
    hero = T.photo("ep14/ai/ep14_sewol_a.jpg", contrast=1.14, color=1.08, bright=0.90, **T.EP14AI_ZOOM["z2"])
    g = [f'<image href="{hero}" width="{W}" height="{H}"/>', darken_photo(),
         block_arrow(450, 160, 620, 252),
         seg(TOP14, 40, 121, kasure="ks"),
         seg(BOT14, 38, 689)]
    bake("ep14_B2_docu_ai", "".join(g), kasure_mask(), out=OUT14)


# ── 15本目 リノ・エアレース2011（2026-10-04・公開ずみ `hsDtzoHIvE0`）──────────────
#    言葉は公開中の A（`thumb_jiko.ep15()` の `c_kaizou_pit`）と1字も変えない：
#       赤「犠牲11人 改造機が観客席へ」→ 白「犠牲11人」（上）＋赤「改造機が観客席へ」（下・主）の2行
#       （1行だと赤が 120px 級でも 1,267px で入らない＝DS844 の「実際の映像／※閲覧注意」の2行の組み方）
#       黄「リノ・エアレース墜落の真相」→ 黄「リノ・エアレース」＋白「墜落の真相」（13.0em×92＝1,196px）
OUT15 = HERE / "out" / "thumb" / "ep15-ab"
TOP15 = [("リノ・エアレース", YEL, 92), ("墜落の真相", WHT, 92)]
EP15_PIT = "ep15/gg_pit_2010.jpg"   # jeggernot／CC BY 2.0：2010年のピットの事故機（「177」）。顔は元画像でモザイク済み

# P-51 の横の形（機首＝x 0・長さ 1000・上が −）。改造機の細部（切り詰めた翼など）は模式
P51 = ("M0,0 Q15,-38 70,-48 L330,-58 Q380,-118 470,-104 Q520,-90 545,-62 L840,-36 L905,-190 Q930,-205 960,-190 "
       "L985,-30 L1000,-10 L1000,10 L960,14 L700,40 L620,42 Q560,95 470,90 L440,58 L300,58 Q120,58 50,40 Q10,30 0,0 Z "
       "M250,28 L540,20 L540,40 L250,48 Z M830,-6 L992,-14 L992,2 L830,8 Z M-8,-150 L6,-150 L6,150 L-8,150 Z")


def ep15_b1():
    """B1＝横から見た図（地面の断面＋観客席）＋平らな赤の主役（機体）＋白い航跡＋赤い矢印＋赤枠の実写（T3「177」）。

    🔴 本編に忠実に：機首上げ → 上昇 → 降下して観客席へ（AAB-12/01）。**「最後に観客席を避けた」は描かない**
       （支えられない＝⑤の決め）。降下は「操縦なしに」＝機体は**動きの線だけ**で、操縦の向きを示す物を足さない。
       背面になった（横転）の向きは描かない（きっかけが未確定）。高さ・G・秒の数は絵に入れない。人（観客）は描かない。
    """
    ground_y = 530
    # 🔴 1巡目は機体が 300px で小さく、差し込みの上にモザイクの顔が入った → 機体 450px・航跡の下りを機体の向き（40度）に・
    #    差し込みは「177」と翼まで下げた（2巡目）
    traj = "M40,430 C300,430 420,200 560,190 C650,185 720,225 1050,500"
    seats = ("M1000,530 L1000,505 L1050,505 L1050,486 L1100,486 L1100,467 L1150,467 L1150,448 L1200,448 "
             "L1200,430 L1290,430 L1290,530 Z")
    ex = red_pattern("rt15") + kasure_mask()
    g = [f'<image href="{day_gray(51)}" width="{W}" height="{H}"/>',
         f'<image href="{uri(rock(seed=19, dark=(30, 24, 18), light=(170, 140, 104)))}" width="{W}" height="{H}" '
         f'clip-path="url(#gc15)"/>',
         f'<clipPath id="gc15"><rect x="-10" y="{ground_y}" width="{W + 20}" height="{H}"/></clipPath>',
         f'<path d="{seats}" fill="#8f969e" stroke="#ffffff" stroke-width="4" stroke-linejoin="round"/>',
         f'<path d="M-10,{ground_y} L{W + 10},{ground_y}" stroke="#ffffff" stroke-width="5"/>',
         # 航跡（白・うすい光）
         f'<path d="{traj}" fill="none" stroke="#ffffff" stroke-width="16" opacity="0.25" filter="url(#sh)"/>',
         f'<path d="{traj}" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="0.9"/>',
         # 機体（機首が右下＝航跡の向き。上下は裏返さない）
         f'<g transform="translate(1042,505) rotate(40) scale(-0.45,0.45)">'
         f'<path d="{P51}" fill="{SIL}" filter="url(#glow)" opacity="0.6"/><path d="{P51}" fill="url(#rt15)"/></g>',
         block_arrow(1195, 172, 985, 330),
         inset(EP15_PIT, 40, 160, 300, 260, cx=0.651, cy=0.879, zoom=2.343, contrast=1.10, color=1.05, bright=1.0),
         '<radialGradient id="vg" cx="0.5" cy="0.48" r="0.8"><stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient>'
         f'<rect width="{W}" height="{H}" fill="url(#vg)"/>',
         seg(TOP15, 40, 101, kasure="ks"),
         seg([("犠牲11人", WHT, 84)], 40, 548),
         seg([("改造機が観客席へ", RED, 140)], 40, 687)]
    bake("ep15_B1_docu", "".join(g), ex, out=OUT15)


def ep15_b2():
    """B2＝公開中の A と同じ写真の地（T3・全体）＋赤い矢印（「177」へ）＋極太明朝＝字と矢印の様式だけを比べる。"""
    hero = TJ.photo(EP15_PIT, cy=0.50, cx=0.50, contrast=1.10, color=1.05, bright=0.86)
    g = [f'<image href="{hero}" width="{W}" height="{H}"/>', darken_photo(),
         block_arrow(1010, 165, 895, 385),
         seg(TOP15, 40, 101, kasure="ks"),
         seg([("犠牲11人", WHT, 84)], 40, 548),
         seg([("改造機が観客席へ", RED, 140)], 40, 687)]
    bake("ep15_B2_docu_photo", "".join(g), kasure_mask(), out=OUT15)


if __name__ == "__main__":
    only = [a for a in sys.argv if a.startswith("--only=")]
    keep = only[0].split("=", 1)[1].split(",") if only else ["a", "b1", "b2"]
    if "ep18" in sys.argv:
        if "a" in keep:
            ep18_a()
        if "b1" in keep:
            ep18_b1()
        if "b2" in keep:
            ep18_b2()
    for ep, b1, b2 in (("ep16", ep16_b1, ep16_b2), ("ep14", ep14_b1, ep14_b2), ("ep15", ep15_b1, ep15_b2)):
        if ep in sys.argv:
            if "b1" in keep:
                b1()
            if "b2" in keep:
                b2()
