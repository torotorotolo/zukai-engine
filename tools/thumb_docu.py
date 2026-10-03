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
    if "ep16" in sys.argv:
        if "b1" in keep:
            ep16_b1()
        if "b2" in keep:
            ep16_b2()
