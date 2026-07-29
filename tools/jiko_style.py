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

# 主翼（奥側）。後退角25度・上反角6度ぶんずらした位置に見える
_WING = "M248 91 L416 91 L452 50 L406 47 Z"
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
    g.append(f'<path d="{_WING}" fill="{ink}" opacity="0.20"/>')
    g.append(f'<path d="{_WING}" fill="none" stroke="{ink}" stroke-width="2.6" '
             f'opacity="0.45"/>')
    g.append(f'<path d="{_NAC}" fill="{ink}" opacity="0.28"/>')
    g.append(f'<path d="{_NAC}" fill="none" stroke="{ink}" stroke-width="3.2" '
             f'opacity="0.60"/>')
    # 吸気口のリップと排気管の口。ここが無いと「ただの楕円」に戻る
    g.append(f'<path d="M291 69 C283 76 283 94 292 101" fill="none" stroke="{ink}" '
             f'stroke-width="2.6" opacity="0.5"/>')
    g.append(f'<path d="M424 70 L430 99" fill="none" stroke="{ink}" '
             f'stroke-width="2.6" opacity="0.4"/>')
    # 尾翼まわり。方向舵のヒンジ線と水平尾翼の前縁
    g.append(f'<path d="M684 -134 L668 -2" fill="none" stroke="{ink}" '
             f'stroke-width="2.6" opacity="0.42"/>')
    g.append(f'<path d="M651 11 L719 3.4" fill="none" stroke="{ink}" '
             f'stroke-width="3.0" opacity="0.42"/>')
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


def b737_tear(x, y, s=1.0, col=None, seed=0):
    """胴体上部の剥離範囲。**まっすぐ切ったのではなく裂けた**ので、下端をぎざぎざにする。

    実測との対応：
      前方扉のすぐ後ろ（x=120）から 18 ft = 5.49 m = 129.5 単位ぶん後ろまで。
      下端は円周の55%に対応する y≈53（＝窓列の下）。窓ごと持って行かれている。
    """
    c = col or ALERT
    x0, x1 = 120.0, 249.5
    # 上端は胴体上面線に沿う（実測でこの区間の上面は y=0 でほぼ平ら）
    top = f"M{x0} 0.6 L{x1} -0.2"
    jag, n = [], 13
    rnd = [0.62, 0.31, 0.88, 0.14, 0.70, 0.45, 0.95, 0.22, 0.58, 0.80, 0.36, 0.72, 0.48]
    for i in range(n + 1):
        t = i / n
        px = x1 - (x1 - x0) * t
        py = 46 + 13 * rnd[(i + seed) % len(rnd)]
        jag.append(f"L{px:.1f} {py:.1f}")
    d = top + " " + " ".join(jag) + " Z"
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="{d}" fill="{c}"/>'
            f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2" '
            f'stroke-linejoin="round"/></g>')


def b737_section(x, y, r=1.0, upper=None, floor=True):
    """胴体断面。直径3.76m。床から上が客室、下が貨物室。
    upper に (開始角, 終了角) を渡すと、その範囲を破断色で描く。"""
    R = 200 * r
    g = [f'<circle cx="{x}" cy="{y}" r="{R:.0f}" fill="none" stroke="{INK_W}" '
         f'stroke-width="{LW * 1.6:.1f}"/>',
         f'<circle cx="{x}" cy="{y}" r="{R - 14 * r:.0f}" fill="none" stroke="{LINE_DIM}" '
         f'stroke-width="{LW * 0.8:.1f}"/>']
    if floor:
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


def lap_joint(x, y, s=1.0, cracks=0, only_cracks=False):
    """ラップジョイント（外板の重ね継手）。**外から skin を見た平面図**として描く。

    初稿は板を細い帯で描いたのでリベットしか見えなかった。
    重ね継手は「2枚の大きな面が帯状に重なり、その帯にリベットが3列走る」形。
    面をきちんと描かないと何の図か分からない。疲労亀裂は**最上列に沿って**進む。
    """
    LAPT = 62          # 重なり帯の半分の高さ
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    if only_cracks:
        for i in range(min(cracks, 15)):
            cx = -448 + i * 62
            g.append(f'<path d="M{cx + 16} -40 l18 -11 l16 12 l16 -11" fill="none" '
                     f'stroke="{ALERT}" stroke-width="{LW * 2.0:.1f}" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>')
        g.append(f'<path d="M-470 -40 H470" stroke="{ALERT}" stroke-width="{LW * 1.1:.1f}" '
                 f'opacity="0.5" stroke-dasharray="20 16"/>')
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
    g.append(f'<linearGradient id="lapsh" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG}" stop-opacity="0.75"/>'
             f'<stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>')
    g.append(f'<rect x="-480" y="{LAPT}" width="960" height="46" fill="url(#lapsh)"/>')
    # 板の切り口。上面より一段暗くすることで「厚みのある板の端」に見える
    g.append(f'<rect x="-480" y="{LAPT - 9}" width="960" height="9" fill="{LINE}" '
             f'opacity="0.85"/>')
    g.append(f'<path d="M-480 {LAPT - 9} H480" stroke="{INK_W}" '
             f'stroke-width="{LW * 0.8:.1f}"/>')
    g.append(f'<path d="M-480 {LAPT} H480" stroke="{BG}" '
             f'stroke-width="{LW * 1.0:.1f}"/>')
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
        for i in range(min(cracks, 15)):
            cx = -448 + i * 62
            g.append(f'<path d="M{cx + 16} -40 l18 -11 l16 12 l16 -11" fill="none" '
                     f'stroke="{ALERT}" stroke-width="{LW * 2.0:.1f}" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>')
    g.append('</g>')
    return "".join(g)


def lap_joint_section(x, y, s=1.0, crack=True):
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
    EXT = 300               # 継手の外側へ伸ばす長さ
    hl = LAP / 2
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
    # リベット3列。皿もみなので頭は外面と面一、縁が薄い
    for rx in (-62, 0, 62):
        g.append(f'<path d="M{rx - 20} {-T} L{rx + 20} {-T} L{rx + 11} {-T + 13} '
                 f'L{rx - 11} {-T + 13} Z" fill="{BG2}" stroke="{BG}" stroke-width="3"/>')
        g.append(f'<rect x="{rx - 11}" y="{-T + 13}" width="22" height="{T * 2 - 13}" '
                 f'fill="{BG2}" stroke="{BG}" stroke-width="3"/>')
        g.append(f'<rect x="{rx - 17}" y="{T}" width="34" height="11" rx="4" '
                 f'fill="{BG2}" stroke="{BG}" stroke-width="3"/>')
    if crack:
        # 皿もみの刃のような縁から、板厚の中を斜めに進む
        g.append(f'<path d="M-73 {-T + 13} l-13 -9 l-9 6 l-11 -7" fill="none" '
                 f'stroke="{ALERT}" stroke-width="7" stroke-linecap="round" '
                 f'stroke-linejoin="round"/>')
        g.append(f'<circle cx="-62" cy="{-T + 13}" r="15" fill="none" stroke="{ALERT}" '
                 f'stroke-width="4" opacity="0.75"/>')
    g.append('</g>')
    return "".join(g)


def alt_graph(x, y, w, h, pts, mark=None):
    """高度の時系列。pts = [(t0-1の位置, 高度0-1), ...]"""
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BG2}" '
         f'stroke="{LINE_DIM}" stroke-width="{LW * 0.8:.1f}"/>']
    for i in range(1, 5):
        gy = y + h * i / 5
        g.append(f'<path d="M{x} {gy:.0f} H{x + w}" stroke="{GRID}" stroke-width="2.4"/>')
    d = "M" + " L".join(f"{x + w * a:.0f} {y + h * (1 - b):.0f}" for a, b in pts)
    g.append(f'<path d="{d}" fill="none" stroke="{AMBER}" stroke-width="{LW * 1.8:.1f}" '
             f'stroke-linejoin="round" stroke-linecap="round"/>')
    if mark is not None:
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
