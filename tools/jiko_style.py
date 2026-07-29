# -*- coding: utf-8 -*-
"""事故検証チャンネルの図解様式。**平面であることが正しい様式**として設計する。

■ なぜこの様式か
人物カートゥーンは崩れると「下手な絵」に見える＝失敗が目立つ。
図解・断面図・経路図・時系列は**平面が正しい**ので、同じ画力でも成立する。
判断基準は「その平面さが意図に見えるか、失敗に見えるか」。

■ 競合との差（Vault `Projects/新チャンネル-事故検証ジャンル再測定-20260729.md`）
最大手「ゆっくり事故検証」（登録7.3万）は**AI/ストックの実写風静止画＋黄色字幕だけで
図解が1枚も無い**。航空・海難・列車・建築の事故はいちばん図解が効く題材なので、ここが空いている。

■ 資料
NTSB / USCG / NASA / NOAA はすべてパブリックドメイン。一次資料をそのまま根拠にできる。
このテストの題材＝アロハ航空243便（1988-04-28）。`ref/ref_aloha_*.png|jpg` は NTSB 撮影のPD。
"""
import math

# ── 配色（暗い技術図。事故という題材に合わせる） ──────────
BG = "#0f1922"
BG2 = "#16232e"
GRID = "#22333f"
LINE = "#8fb6c9"          # 技術線
LINE_DIM = "#41606f"
INK_W = "#eaf2f6"         # 主図形
ALERT = "#e0503c"         # 破壊・欠陥
ALERT_DIM = "#8e3225"
AMBER = "#e8b33c"         # 数値
OK = "#5fbf8f"
LW = 5.0                  # 技術線の基本太さ（1920px幅）


def frame(w, h):
    """地。方眼を薄く敷いて『技術図』の文脈を作る。"""
    g = [f'<rect width="{w}" height="{h}" fill="{BG}"/>']
    for x in range(0, w + 1, 60):
        g.append(f'<path d="M{x} 0 V{h}" stroke="{GRID}" stroke-width="1.6"/>')
    for y in range(0, h + 1, 60):
        g.append(f'<path d="M0 {y} H{w}" stroke="{GRID}" stroke-width="1.6"/>')
    for x in range(0, w + 1, 300):
        g.append(f'<path d="M{x} 0 V{h}" stroke="{GRID}" stroke-width="3.4"/>')
    for y in range(0, h + 1, 300):
        g.append(f'<path d="M0 {y} H{w}" stroke="{GRID}" stroke-width="3.4"/>')
    return "".join(g)


def title(t, sub="", x=90, y=118):
    """見出し。左上に置き、下に細い罫を1本。中央寄せの飾り帯にはしない。"""
    g = (f'<text x="{x}" y="{y}" font-family="Dela" font-size="62" fill="{INK_W}">{t}</text>'
         f'<path d="M{x} {y + 30} h{min(1740, 40 + len(t) * 62)}" stroke="{ALERT}" '
         f'stroke-width="5"/>')
    if sub:
        g += (f'<text x="{x}" y="{y + 78}" font-family="Noto" font-size="32" '
              f'fill="{LINE}">{sub}</text>')
    return g


def label(x, y, t, col=None, size=30, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="Noto" font-size="{size}" '
            f'fill="{col or LINE}" text-anchor="{anchor}">{t}</text>')


def leader(x1, y1, x2, y2, col=None):
    """引き出し線。端に小さな丸を打つ。"""
    c = col or LINE
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c}" stroke-width="{LW * 0.7:.1f}"/>'
            f'<circle cx="{x1}" cy="{y1}" r="8" fill="{c}"/>')


def dim(x1, x2, y, t, col=None):
    """寸法線。両端に矢羽根を付けて『図面』に見せる。"""
    c = col or AMBER
    return (f'<path d="M{x1} {y} H{x2}" stroke="{c}" stroke-width="{LW * 0.7:.1f}"/>'
            f'<path d="M{x1} {y - 12} v24 M{x2} {y - 12} v24" stroke="{c}" '
            f'stroke-width="{LW * 0.7:.1f}"/>'
            f'<path d="M{x1 + 8} {y - 8} l-12 8 l12 8" fill="none" stroke="{c}" '
            f'stroke-width="{LW * 0.6:.1f}"/>'
            f'<path d="M{x2 - 8} {y - 8} l12 8 l-12 8" fill="none" stroke="{c}" '
            f'stroke-width="{LW * 0.6:.1f}"/>'
            f'<rect x="{(x1 + x2) / 2 - 96:.0f}" y="{y - 26}" width="192" height="52" '
            f'fill="{BG}"/>'
            f'<text x="{(x1 + x2) / 2:.0f}" y="{y + 12}" font-family="Dela" font-size="34" '
            f'fill="{c}" text-anchor="middle">{t}</text>')


def vdim(y1, y2, x, t, col=None):
    """縦の寸法線。重ね幅のように**縦に測る寸法**を横に引くと図が嘘になる。"""
    c = col or AMBER
    return (f'<path d="M{x} {y1} V{y2}" stroke="{c}" stroke-width="{LW * 0.7:.1f}"/>'
            f'<path d="M{x - 12} {y1} h24 M{x - 12} {y2} h24" stroke="{c}" '
            f'stroke-width="{LW * 0.7:.1f}"/>'
            f'<path d="M{x - 8} {y1 + 8} l8 -12 l8 12" fill="none" stroke="{c}" '
            f'stroke-width="{LW * 0.6:.1f}"/>'
            f'<path d="M{x - 8} {y2 - 8} l8 12 l8 -12" fill="none" stroke="{c}" '
            f'stroke-width="{LW * 0.6:.1f}"/>'
            f'<text x="{x - 22}" y="{(y1 + y2) / 2 + 12:.0f}" font-family="Dela" '
            f'font-size="34" fill="{c}" text-anchor="end">{t}</text>')


# ── 機体（ボーイング737-200 の側面） ──────────────────────
# 🔴 形は **NTSB 事故調査資料に添付された 737-200 三面図を画素で実測**して起こした。
#    （`ref/b737_3view.png`。初稿は記憶で描いたので主翼が三角・エンジンが楕円になっていた）
#
# 座標系： (0,0) = 機首先端x ／ 胴体上面線y。機首は左。
#          全長 720 単位 = 30.53 m （= 23.58 単位/m）
#
# 実測値（すべて上の三面図から）：
#   胴体下面      y = 92.5        → 胴体径 3.76 m と一致
#   垂直尾翼頂点  y = -141.1
#   主脚下端      y = 117.7 ／ 前脚下端 y = 112.3
#   窓列          y = 31〜40・ピッチ 13.0・幅 7.8
#   前方扉        x = 100〜120 ／ 後方扉 x = 544〜564
#   ナセル        x = 277〜450・y = 67〜103
#     → JT8D の「長く薄いナセルを主翼下面に密着させる」-200 特有の形。
#       全長 7.2 m・直径 1.5 m。**胴体下面線より上に食い込み、下に少しだけ出る**
#   主翼          翼根 x=248（前縁）〜416（後縁）・後退角25度・上反角6度
#     → 側面図では奥の翼が上反角ぶん持ち上がり、後退角ぶん後ろへずれて見える

# 外形。三面図の側面図を塗り面に変換 → 上下の包絡線を追跡 → Douglas-Peucker で簡約。
# 途中の細かい凹凸（x=318 のアンテナ、x=238 の張り出し、前脚・主脚）も実測どおり。
_SIL = (
    "M0.0 52.8 L4.2 47.4 L11.4 43.2 L33.6 34.8 L45.6 22.8 L56.4 16.2 L87.7 7.2 "
    "L127.3 1.8 L305.7 -0.6 L315.9 -10.8 L320.7 -10.2 L321.3 -0.6 L324.9 0.0 "
    "L527.2 -3.0 L556.7 -15.0 L574.1 -27.0 L611.9 -68.5 L665.4 -131.5 "
    "L672.6 -138.7 L679.8 -141.1 L711.6 -139.9 L712.2 1.8 L720.0 3.0 L720.0 4.2 "
    "L699.0 13.8 L696.0 26.4 L690.0 34.8 L652.7 49.2 L602.3 63.7 L560.3 73.3 "
    "L482.2 88.3 L452.8 91.3 L451.0 91.9 L449.2 97.3 L440.8 99.7 L380.1 105.1 "
    "L373.5 117.7 L354.3 117.1 L349.5 106.9 L321.9 106.9 L300.3 104.5 "
    "L279.2 99.1 L273.2 93.1 L262.4 92.5 L244.4 93.1 L243.8 101.5 L238.4 102.1 "
    "L232.4 93.7 L228.8 92.5 L99.1 91.3 L98.5 110.5 L96.7 112.3 L85.3 111.7 "
    "L83.5 109.9 L82.9 97.3 L57.0 94.3 L54.6 84.7 L18.6 72.1 L4.8 63.7 "
    "L0.0 57.6 Z")

# 主翼（奥側）。後退角25度・上反角6度ぶんずらした位置に見える。
# 2巡目は翼根から翼端までの面を丸ごと描いたので、**ナセルと重なって図が濁った**。
# 側面図で実際に見えるのはナセルの上に出る細い帯だけなので、そこだけ描く。
_WING = "M296 84 L450 46 L462 58 L336 92 Z"
# ナセル。前方に張り出した吸気口 → 円筒部 → 細くなる排気管、の3段
_NAC = ("M277 85 C277 73 286 67 301 67 L409 67 C425 67 434 72 437 80 "
        "L449 90 C452 95 449 100 442 101 L306 103 C288 103 277 96 277 85 Z")
# 窓列。実測ピッチ13.0。扉の位置は空ける
_WIN_X = [140.5 + 12.99 * i for i in range(9)] + [466.6 + 13.3 * i for i in range(6)] + \
         [258.0 + 12.99 * i for i in range(16)]


def b737_side(x, y, s=1.0, skin=INK_W, lw=LW, detail=True):
    """ボーイング737-200 の側面図。(x, y) は**機首先端・胴体上面線**に置く。

    塗り分けは1段だけ（地の色を薄く重ねる）。平面のまま「図」として成立させる。
    """
    ink = BG
    g = [f'<g transform="translate({x},{y}) scale({s})">',
         f'<path d="{_SIL}" fill="{skin}"/>']
    if not detail:
        return "".join(g) + "</g>"
    # 主翼・ナセル。地の色を薄く重ねて面を分ける（線を足すと図が濁る）
    g.append(f'<path d="{_WING}" fill="{ink}" opacity="0.16"/>')
    g.append(f'<path d="{_WING}" fill="none" stroke="{ink}" stroke-width="2.6" '
             f'opacity="0.36"/>')
    # ナセルは主翼より手前。**塗りを濃くして翼の線を隠さないと図が濁る**（2巡目の粗）
    g.append(f'<path d="{_NAC}" fill="{BG2}" opacity="0.62"/>')
    g.append(f'<path d="{_NAC}" fill="none" stroke="{ink}" stroke-width="3.2" '
             f'opacity="0.60"/>')
    # 吸気口のリップと排気管の口。ここが無いと「ただの楕円」に戻る
    g.append(f'<path d="M291 69 C283 76 283 94 292 101" fill="none" stroke="{ink}" '
             f'stroke-width="2.6" opacity="0.5"/>')
    g.append(f'<path d="M424 70 L430 99" fill="none" stroke="{ink}" '
             f'stroke-width="2.6" opacity="0.4"/>')
    # 尾翼まわり。**この3本が無いと尾部が「ただの大きな楔」に見える**（1巡目の粗）
    #   ① 胴体の背中の続き（尾錐）… 垂直尾翼と胴体の境目
    #   ② 水平尾翼の前縁      … 垂直尾翼と水平尾翼の境目
    #   ③ 方向舵のヒンジ線
    # 2巡目は水平尾翼の線を胴体の中から引き始めたので、尾錐の線と**X字に交差**した。
    # 水平尾翼は尾錐から生えているので、交点(662, 16.5)より後ろだけを引く。
    g.append(f'<path d="M527 -3 C596 6 646 14 704 24" fill="none" stroke="{ink}" '
             f'stroke-width="3.4" opacity="0.55"/>')
    g.append(f'<path d="M662 16.5 L718 3.6" fill="none" stroke="{ink}" '
             f'stroke-width="3.4" opacity="0.62"/>')
    g.append(f'<path d="M686 -134 L674 12" fill="none" stroke="{ink}" '
             f'stroke-width="2.6" opacity="0.42"/>')
    # 窓列
    g.append("".join(f'<rect x="{wx:.1f}" y="30.6" width="7.8" height="9.0" rx="2.6" '
                     f'fill="{ink}" opacity="0.80"/>' for wx in _WIN_X))
    # 扉（前方・後方）と貨物扉
    for dx, dy, dw, dh in ((100.0, 10.0, 20.0, 47.0), (544.1, 13.8, 19.8, 42.6)):
        g.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="5" '
                 f'fill="none" stroke="{ink}" stroke-width="3.0" opacity="0.55"/>')
    g.append(f'<rect x="150" y="62" width="34" height="20" rx="4" fill="none" '
             f'stroke="{ink}" stroke-width="2.4" opacity="0.35"/>')
    # 操縦室の窓（737は前面2枚＋側面。ここが無いと機首が「棒」に見える）
    g.append(f'<path d="M41 30 L60 20 L60 32 L43 36 Z" fill="{ink}" opacity="0.72"/>')
    g.append(f'<path d="M64 19 L79 16 L79 29 L64 31 Z" fill="{ink}" opacity="0.72"/>')
    g.append('</g>')
    return "".join(g)


def b737_tear(x, y, s=1.0, col=None, part="hole"):
    """胴体上部の剥離範囲。

    1巡目は**赤い長方形を貼った**ように見えた。外板が「無くなった」のだから、
    塗りは客室の暗がりにして、縁だけを赤で示すほうが事実にも近いし怖い。
    内側に胴体フレーム（輪状の骨組み）を数本入れる。実際の写真でも、
    外板が飛んだあとはフレームと床梁が剥き出しになっている。

    実測との対応：
      前方扉のすぐ後ろ（x=120）から 18 ft = 5.49 m = 129.5 単位ぶん後ろまで。
      下端は円周の55%に対応する y≈53（＝窓列の下）。窓ごと持って行かれている。
    """
    c = col or ALERT
    x0, x1 = 120.0, 249.5
    rnd = [0.62, 0.31, 0.88, 0.14, 0.70, 0.45, 0.95, 0.22, 0.58, 0.80, 0.36, 0.72, 0.48]
    pts = [f"M{x0} 1.0"]
    # 上端も少しだけ荒らす（胴体上面線に沿うが、切り口はまっすぐではない）
    for i in range(1, 9):
        t = i / 8
        pts.append(f"L{x0 + (x1 - x0) * t:.1f} {0.4 + 2.2 * rnd[i % len(rnd)]:.1f}")
    # 後端の裂け目
    pts.append(f"L{x1 + 3.0:.1f} 19.0 L{x1 - 3.0:.1f} 33.0 L{x1 + 2.0:.1f} 47.0")
    # 下端のぎざぎざ（後→前）。2巡目は振幅13・8コマ間隔で棘に見えたので、
    # 振幅を9に落として山の数を減らす（裂け目であって鋸ではない）
    for i in range(9):
        t = i / 8
        pts.append(f"L{x1 - (x1 - x0) * t:.1f} {47 + 9 * rnd[i % len(rnd)]:.1f}")
    # 前端の裂け目
    pts.append(f"L{x0 - 3.0:.1f} 32.0 L{x0 + 4.0:.1f} 16.0")
    d = " ".join(pts) + " Z"
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    if part == "line":
        # 縁だけ。これを脈打たせる。**穴そのものを明滅させると嘘に見える**
        g.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="5" '
                 f'stroke-linejoin="round"/>')
    else:
        g.append(f'<clipPath id="tearclip"><path d="{d}"/></clipPath>')
        g.append(f'<path d="{d}" fill="{BG}"/>')
        g.append(f'<path d="{d}" fill="{BG2}" opacity="0.85"/>')
        # 剥き出しになった胴体フレームと床梁
        g.append('<g clip-path="url(#tearclip)">' + "".join(
            f'<path d="M{x0 + 9 + i * 13.0:.1f} -2 V60" stroke="{LINE_DIM}" '
            f'stroke-width="3.2" opacity="0.75"/>' for i in range(10)) +
            f'<path d="M{x0 - 4} 40 H{x1 + 4}" stroke="{LINE_DIM}" stroke-width="4" '
            f'opacity="0.6"/></g>')
    g.append('</g>')
    return "".join(g)


def b737_section(x, y, r=1.0, upper=None, floor=True, arc_only=False):
    """胴体断面。直径3.76m。床から上が客室、下が貨物室。
    upper に (開始角, 終了角) を渡すと、その範囲を破断色で描く。
    arc_only=True で破断の弧だけを返す（**弧を左から広げて「裂けていく」動きにする**ため）。"""
    R = 200 * r
    if arc_only:
        g = []
    else:
        g = [f'<circle cx="{x}" cy="{y}" r="{R:.0f}" fill="none" stroke="{INK_W}" '
             f'stroke-width="{LW * 1.6:.1f}"/>',
             f'<circle cx="{x}" cy="{y}" r="{R - 14 * r:.0f}" fill="none" '
             f'stroke="{LINE_DIM}" stroke-width="{LW * 0.8:.1f}"/>']
    if floor and not arc_only:
        fy = y + R * 0.34
        hw = (R ** 2 - (fy - y) ** 2) ** 0.5
        g.append(f'<path d="M{x - hw:.0f} {fy:.0f} H{x + hw:.0f}" stroke="{LINE}" '
                 f'stroke-width="{LW * 1.2:.1f}"/>')
        for sx in (-0.52, 0.52):
            g.append(f'<path d="M{x + R * sx:.0f} {fy:.0f} v{-R * 0.34:.0f} '
                     f'h{28 * r * (1 if sx > 0 else -1):.0f}" fill="none" stroke="{LINE}" '
                     f'stroke-width="{LW:.1f}" stroke-linejoin="round"/>')
    if upper:
        a0, a1 = [math.radians(a) for a in upper]
        x0, y0 = x + R * math.cos(a0), y + R * math.sin(a0)
        x1, y1 = x + R * math.cos(a1), y + R * math.sin(a1)
        large = 1 if (upper[1] - upper[0]) % 360 > 180 else 0
        g.append(f'<path d="M{x0:.0f} {y0:.0f} A{R:.0f} {R:.0f} 0 {large} 1 '
                 f'{x1:.0f} {y1:.0f}" fill="none" stroke="{ALERT}" '
                 f'stroke-width="{LW * 2.4:.1f}" stroke-linecap="round"/>')
    return "".join(g)


# 疲労亀裂。2巡目は1本の長さがリベット間隔とほぼ同じで、**つながって赤い波線**に見えた。
# 実際は「穴ごとに短い亀裂が出て、まだつながっていない」状態なので、短く・不揃いにする。
_CRACK_SHAPES = ["l12 -6 l10 5 l8 -4", "l10 -5 l8 6 l11 -5",
                 "l14 -7 l9 6", "l9 -4 l11 5 l6 -5"]


def _cracks(n):
    """6巡目は全リベットに起点の赤点を打ったので、**赤い点線**に見えた。
    実際に亀裂が入っていたのは一部の穴なので、点は打たず、亀裂の本数も間引く。
    「まだつながっていない」ことが伝わればよい。"""
    g = []
    for i in range(min(n, 15)):
        if i % 3 == 2:            # 3穴に1つは無傷にする（連続して見えないように）
            continue
        cx = -448 + i * 62
        g.append(f'<path d="M{cx + 15} -40 {_CRACK_SHAPES[i % 4]}" fill="none" '
                 f'stroke="{ALERT}" stroke-width="{LW * 1.3:.1f}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(g)


def lap_joint(x, y, s=1.0, cracks=0, only_cracks=False):
    """ラップジョイント（外板の重ね継手）。**外から skin を見た平面図**として描く。

    初稿は板を細い帯で描いたのでリベットしか見えなかった。
    重ね継手は「2枚の大きな面が帯状に重なり、その帯にリベットが3列走る」形。
    面をきちんと描かないと何の図か分からない。疲労亀裂は**最上列に沿って**進む。
    """
    LAPT = 62          # 重なり帯の半分の高さ
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    if only_cracks:
        g.append(f'<path d="M-470 -40 H470" stroke="{ALERT}" stroke-width="{LW * 1.1:.1f}" '
                 f'opacity="0.28" stroke-dasharray="20 16"/>')
        g.append(_cracks(cracks))
        g.append('</g>')
        return "".join(g)
    # 下の外板（奥）。上端が重なり帯の上まで入り込む
    g.append(f'<path d="M-480 {-LAPT} H480 V250 H-480 Z" fill="{LINE}" opacity="0.50" '
             f'stroke="{LINE}" stroke-width="{LW * 1.2:.1f}" stroke-linejoin="round"/>')
    # 上の外板（手前）。下の板の上に乗る
    g.append(f'<path d="M-480 -250 H480 V{LAPT} H-480 Z" fill="{INK_W}" opacity="0.80" '
             f'stroke="{INK_W}" stroke-width="{LW * 1.5:.1f}" stroke-linejoin="round"/>')
    # ── 段差 ──
    # 初稿は「暗い線を1本」だけ引いていたので、重なりが平らに見えていた。
    # 実物の段差は ①板の切り口（板厚ぶんの帯）②その下の落ち影 の2つで見える。
    # 平面図に落ち影を入れるのは図解として正しい（陰影ではなく段差の表現）。
    # 1巡目は影が長く柔らかすぎて「ぼかし」に見えた。段差は 0.9mm しかないので、
    # **短く硬い落ち影**にする。影が長いと段差が高く見えて、図として嘘になる。
    g.append(f'<linearGradient id="lapsh" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG}" stop-opacity="0.92"/>'
             f'<stop offset="0.55" stop-color="{BG}" stop-opacity="0.34"/>'
             f'<stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>')
    g.append(f'<rect x="-480" y="{LAPT}" width="960" height="20" fill="url(#lapsh)"/>')
    # 板の切り口。ここだけ明るくすると「厚みのある板の端」として立ち上がる
    g.append(f'<rect x="-480" y="{LAPT - 11}" width="960" height="11" fill="{INK_W}"/>')
    g.append(f'<path d="M-480 {LAPT - 11} H480" stroke="{LINE_DIM}" '
             f'stroke-width="{LW * 0.6:.1f}" opacity="0.7"/>')
    g.append(f'<path d="M-480 {LAPT} H480" stroke="{BG}" '
             f'stroke-width="{LW * 1.2:.1f}"/>')
    # 重なり帯の斜線
    g.append(f'<clipPath id="lapband"><rect x="-480" y="{-LAPT}" width="960" '
             f'height="{LAPT * 2}"/></clipPath>')
    g.append(f'<g clip-path="url(#lapband)">' + "".join(
        f'<path d="M{-600 + i * 29} {LAPT} l{LAPT * 2} {-LAPT * 2}" '
        f'stroke="{AMBER}" stroke-width="3" opacity="0.30"/>' for i in range(42)) + '</g>')
    # リベット3列。重なり帯の中を走る
    for ry in (-40, 0, 40):
        for i in range(16):
            cx = -448 + i * 62
            g.append(f'<circle cx="{cx}" cy="{ry}" r="15" fill="{BG2}" stroke="{INK_W}" '
                     f'stroke-width="{LW * 0.9:.1f}"/>')
            g.append(f'<circle cx="{cx}" cy="{ry}" r="6" fill="{LINE_DIM}"/>')
    if cracks:
        g.append(_cracks(cracks))
    g.append('</g>')
    return "".join(g)


def lap_joint_section(x, y, s=1.0, crack=True, crack_only=False):
    """重ね継手の **A-A 断面**。段差は平面図では原理的に見えないので、断面で示す。

    ここまで描いて初めて事故の因果が図になる：
      外板は2枚が76mm重なり、**接着（コールドボンド）とリベット3列**で荷重を分け合う設計。
      その接着が湿気と腐食で剥がれると、荷重はリベット穴の縁だけに集中する。
      穴は皿もみ（カウンターシンク）なので縁が刃のように薄い。そこから疲労亀裂が出る。

    横方向は平面図の縦方向に対応させる（平面図に A-A の切断線を引く）。
      左 = 下の外板の自由端側 ／ 右 = 上の外板の自由端＝段差
    """
    T = 26                  # 板厚（誇張。実機は0.9mm＝この図では見えない）
    LAP = 190               # 重ね幅 76mm ぶん
    hl = LAP / 2
    if crack_only:
        # 🔴 7巡目まで c5_crack は**断面図まるごとの複製**だった。
        #    それを脈動させていたので、図全体の濃度が揺れていた。亀裂だけ返す。
        return (f'<g transform="translate({x},{y}) scale({s})">'
                f'<path d="M-70 {-T + 12} l-16 -3 l-12 4 l-14 -3 l-10 2" fill="none" '
                f'stroke="{ALERT}" stroke-width="6" stroke-linecap="round" '
                f'stroke-linejoin="round"/>'
                f'<circle cx="-70" cy="{-T + 12}" r="13" fill="none" stroke="{ALERT}" '
                f'stroke-width="4" opacity="0.8"/></g>')
    EXT = 300               # 継手の外側へ伸ばす長さ
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    # 下（内側）の外板：左端が自由端
    g.append(f'<path d="M{-hl} 0 H{hl + EXT} V{T} H{-hl} Z" fill="{LINE}" '
             f'opacity="0.55" stroke="{LINE}" stroke-width="3"/>')
    # 上（外側）の外板：右端が自由端＝ここが段差
    g.append(f'<path d="M{-hl - EXT} {-T} H{hl} V0 H{-hl - EXT} Z" fill="{INK_W}" '
             f'opacity="0.85" stroke="{INK_W}" stroke-width="3"/>')
    # 接着層。**ここが剥がれたのが事故の起点**なので独立した層として描く
    g.append(f'<rect x="{-hl}" y="-4" width="{LAP}" height="8" fill="{OK}" '
             f'opacity="0.85"/>')
    # 段差の落ち影
    g.append(f'<path d="M{hl} 0 h{EXT}" stroke="{BG}" stroke-width="9" opacity="0.5"/>')
    # リベット3列。皿もみなので頭は外面と面一、縁が薄い。
    # 2巡目は頭が幅40で間隔62だったため、板の残りが細い楔になって「歯」に見えた。
    # 頭を幅28に絞って、板の面を残す。
    for rx in (-62, 0, 62):
        g.append(f'<path d="M{rx - 14} {-T} L{rx + 14} {-T} L{rx + 8} {-T + 13} '
                 f'L{rx - 8} {-T + 13} Z" fill="{BG2}" stroke="{BG}" stroke-width="3"/>')
        g.append(f'<rect x="{rx - 8}" y="{-T + 13}" width="16" height="{T * 2 - 13}" '
                 f'fill="{BG2}" stroke="{BG}" stroke-width="3"/>')
        g.append(f'<rect x="{rx - 13}" y="{T}" width="26" height="11" rx="4" '
                 f'fill="{BG2}" stroke="{BG}" stroke-width="3"/>')
    if crack:
        # 皿もみの刃のような縁から、**板厚の中を**横に進む。
        # 2巡目は斜めに立ち上げすぎて板の外に出ていた。
        g.append(f'<path d="M-70 {-T + 12} l-16 -3 l-12 4 l-14 -3 l-10 2" fill="none" '
                 f'stroke="{ALERT}" stroke-width="6" stroke-linecap="round" '
                 f'stroke-linejoin="round"/>')
        g.append(f'<circle cx="-70" cy="{-T + 12}" r="13" fill="none" stroke="{ALERT}" '
                 f'stroke-width="4" opacity="0.8"/>')
    g.append('</g>')
    return "".join(g)


def alt_graph(x, y, w, h, pts, mark=None, part="all"):
    """高度の時系列。pts = [(t0-1の位置, 高度0-1), ...]

    part="frame" 枠と方眼だけ ／ part="line" 折れ線だけ ／ part="mark" 剥離点だけ。
    **折れ線を左から描いていく**ために分ける（グラフが最初から全部出ていると動きが無い）。
    """
    g = []
    if part in ("all", "frame"):
        g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BG2}" '
                 f'stroke="{LINE_DIM}" stroke-width="{LW * 0.8:.1f}"/>')
        for i in range(1, 5):
            gy = y + h * i / 5
            g.append(f'<path d="M{x} {gy:.0f} H{x + w}" stroke="{GRID}" '
                     f'stroke-width="2.4"/>')
    if part in ("all", "line"):
        d = "M" + " L".join(f"{x + w * a:.0f} {y + h * (1 - b):.0f}" for a, b in pts)
        g.append(f'<path d="{d}" fill="none" stroke="{AMBER}" '
                 f'stroke-width="{LW * 1.8:.1f}" stroke-linejoin="round" '
                 f'stroke-linecap="round"/>')
    if mark is not None and part in ("all", "mark"):
        mx, my = x + w * pts[mark][0], y + h * (1 - pts[mark][1])
        g.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="16" fill="{ALERT}"/>'
                 f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="30" fill="none" stroke="{ALERT}" '
                 f'stroke-width="{LW:.1f}" opacity="0.6"/>')
    return "".join(g)


def bignum(x, y, num, unit="", cap="", col=None):
    """大きな数字。事故検証は数字が主役になる場面が多い。"""
    c = col or AMBER
    g = (f'<text x="{x}" y="{y}" font-family="Dela" font-size="168" fill="{c}" '
         f'text-anchor="middle">{num}</text>')
    if unit:
        g += (f'<text x="{x}" y="{y + 56}" font-family="Dela" font-size="44" fill="{c}" '
              f'text-anchor="middle" opacity="0.9">{unit}</text>')
    if cap:
        g += (f'<text x="{x}" y="{y - 150}" font-family="Noto" font-size="34" '
              f'fill="{LINE}" text-anchor="middle">{cap}</text>')
    return g
