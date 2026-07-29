# -*- coding: utf-8 -*-
"""キャラクター部品。シニア向け健康解説チャンネル用。

参考2本（Vault `Resources/参考-健康解説アニメ2本-分析-20260728.md`）の共通原則
「キャラクターが登場して演じる」を満たすための、1体ぶんの部品一式。

■ 形の根拠（記憶で描かず、必ず実測・実物から起こした）────────────────

【1】画風と比率 … 参考B（砂糖・手描きキャラ型）のフレームを画素で実測した。
`ref/_grid_bl.png` `ref/_grid_br.png` に方眼を焼いてある。実測値：

| 項目 | 実測 | 頭径D=200 換算 |
|---|---|---|
| 頭 | 224 x 224 px | **200 x 200（ほぼ真円）** |
| 輪郭線 | 11 px（径の4.9%） | **10** |
| 全高 | 602 px | **530（＝2.65頭身）** |
| 首 | 無い。頭が肩に直接載る | 0 |
| 肩幅 | 頭径の約0.58 | 116 |
| 胴（肩〜股） | 頭径の約0.72 | 145 |
| 脚（股〜足） | 頭径の約0.91 | 185 |
| 目 | 幅33/38・高57、頭の縦44%の位置 | rx14/17・ry25・y=-12 |
| 目の左右間隔 | 中心間50（頭中心より右に片寄る＝3/4向き） | far +2 / near +46 |
| 口 | 幅80、頭の縦71%の位置 | 幅70・y=+42 |
| 眉 | 頭の縦27%の位置 | y=-46 |

※ 目が「頭の縦44%」＝ほぼ中央なのが要点。記憶で描くと必ず上に寄せてしまう。

【2】表情 … ダーウィン『人及び動物の表情について』(1872) の図版（PD）で確認した。
`ref/face_darwin_2.png`（悲嘆）／`ref/face_darwin_7.png`（驚愕）

- **つらい**＝眉の「内端が上がり外端が下がる」ハの字。図版II-3の額のしわがその証拠。
  怒りの ＼／ と取り違えるのが最頻の誤り。口角は下がる（図版II-5, II-7）。
- **驚き**＝眉を高く強く弧に上げ、上まぶたを大きく開いて**虹彩の上に白目が出る**。
  口は横に広げず**縦長のO（顎が落ちる）**。図版VII-1,2。
- 参考Bの実物でも一致を確認（`ref/_sugar_tl.png` の困り顔がまさにハの字眉）。

【3】ポーズ … マイブリッジ『Animal Locomotion』(1887) の連続写真（PD）で確認した。
`ref/pose_sit_muybridge.jpg`（Plate 241・着衣で椅子に座る）
`ref/pose_lie_muybridge.jpg`（Plate 263・寝台に横になる）

- **座る**＝座面の高さは脛の長さと等しい。腰は座面の奥に置き、
  **膝は腰より腿1本ぶん前へ出る**（腿を短く描くのが最頻の誤り）。
  脛はほぼ垂直に落ちる。上体は10度ほど前へ傾く。
- **寝る**＝頭は枕のぶん床から浮く。肩が最も高く、腰へ向かってなだらかに下がる。
  横向きで膝を軽く抱えるのが実際の寝姿。

【4】シニアであることの記号 … 参考Bは白い無地の丸顔（年齢不詳）。
本チャンネルは視聴者が自分に重ねられることが要なので、年齢の記号を2つだけ足す。
  a) **グレーの髪と後退した生え際** … 60代を一目で示す最も安い記号
  b) **わずかな背中の丸み（`stoop`）** … 脊椎後彎。既定は控えめ。
     `stoop=0` で背筋が伸びる＝**姿勢そのもので before/after を語れる**ようにした。

■ 使い方 ────────────────────────────────────────────
    import character as C
    svg = f'<svg ...><defs>{C.defs()}</defs>{C.character("point", "smile", at=(700, 980))}</svg>'
    C.character(...).anchors["hand"]   # 小道具を持たせる座標

    python tools/character.py          # 検証用の一覧シートを out/ に3枚出す
"""
import math

# ── 実測から起こした基準寸法（頭径 D=200 を単位とする）─────────────────
D = 200.0          # 頭の直径
R = D / 2          # 頭の半径
LW = 10.0          # 主線の太さ（実測 径の4.9%）
TOTAL_H = 530.0    # 全高（2.65頭身）

SHOULDER_Y = -330.0        # 肩の高さ（＝頭の下端。首は無い）
HIP_Y = -185.0             # 股の高さ
SHOULDER_HW = 58.0         # 肩の半幅
HIP_HW = 46.0              # 腰の半幅
ARM_W = 26.0               # 腕の太さ
LEG_W = 34.0               # 脚の太さ
HAND_R = 17.0              # 手の大きさ

# ── 色 ────────────────────────────────────────────────────
# 線は黒でなく濃茶。ただし anatomy.INK(#4a3b2a) より締める。
# 人体図は「見るもの」だがキャラは「演じるもの」で、テレビ距離での輪郭の強さが要る。
INK = "#33291f"
INK_SOFT = "#6b5c4b"
SKIN = "#fdfaf3"           # 顔と手。純白でなく紙一枚ぶん温かい（クリーム背景から浮かせない）
SKIN_SH = "#eadfcd"
HAIR = "#a9a29a"           # 白髪まじりのグレー
HAIR_SH = "#877f76"
MOUTH_IN = "#7e332b"
TONGUE = "#c8604f"
TOOTH = "#fffdf7"
BLUSH = "#e2a08e"

# 衣装。純色を避け、少し濁らせる（参考2本の共通原則7）
COSTUMES = {
    "casual": dict(top="#6f96a1", inner="#f2ead9", pants="#857a6b",
                   shoe="#4f463c", dots=False, skirt=False),
    "coat":   dict(top="#fbf7ee", inner="#b9c6cc", pants="#857a6b",
                   shoe="#4f463c", dots=False, skirt=True),
    "pajama": dict(top="#a3c1d6", inner="#a3c1d6", pants="#a3c1d6",
                   shoe="#efe9dc", dots=True, skirt=False),
}

FACES = ("normal", "pain", "surprise", "convinced", "smile")
POSES = ("stand", "sit", "lie", "point", "hold")
FACE_JA = {"normal": "普通", "pain": "つらい", "surprise": "驚き",
           "convinced": "納得", "smile": "笑顔"}
POSE_JA = {"stand": "立つ", "sit": "座る", "lie": "寝る",
           "point": "指差し", "hold": "持つ"}


def _d(pts):
    """点列を折れ線のパスにする（線は round 継ぎで丸める）。"""
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def _limb(pts, w, col):
    """手足。太い濃茶を敷いてから細い本体色を重ねる＝輪郭つきのチューブ。

    stroke を重ねる方式にするのは、太さが一定に保たれ、
    関節で線が破綻しないため。参考Bの手足もこの見え方をしている。
    """
    d = _d(pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + LW * 2:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _shape(d, fill, lw=LW):
    return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{lw:.1f}" stroke-linejoin="round"/>'


# ── 手 ──────────────────────────────────────────────────
def _hand(x, y, kind="plain", ang=0.0):
    """手。ミトン。参考Bも指は割らず、指1本を出すときだけ描き足している。"""
    g = [f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">']
    if kind == "point":
        # 人差し指だけ出す。指は手の塊から前へ伸びる1本のチューブ。
        g.append(_limb([(0, 2), (26, -6), (48, -12)], 13, SKIN))
    g.append(f'<circle cx="0" cy="0" r="{HAND_R}" fill="{SKIN}" '
             f'stroke="{INK}" stroke-width="{LW:.1f}"/>')
    if kind == "grip":
        # 握り。指の割れを2本入れるだけで「掴んでいる」に見える。
        g.append(f'<path d="M-6 -11 q10 11 0 22 M6 -12 q10 12 0 24" fill="none" '
                 f'stroke="{INK}" stroke-width="3.4" opacity="0.75"/>')
    elif kind == "plain":
        g.append(f'<path d="M-2 -12 q9 12 0 24" fill="none" '
                 f'stroke="{INK}" stroke-width="3.2" opacity="0.6"/>')
    g.append("</g>")
    return "".join(g)


# ── 顔 ────────────────────────────────────────────────────
EYE_Y = -12.0        # 実測：頭の縦44%
EYE_FAR_X = 2.0      # 3/4向き（右向き）。奥の目は頭の中心近くまで寄る
EYE_NEAR_X = 46.0
EYE_FAR_RX, EYE_NEAR_RX, EYE_RY = 14.0, 17.0, 25.0
BROW_Y = -46.0       # 実測：頭の縦27%
MOUTH_X, MOUTH_Y = 22.0, 42.0   # 実測：頭の縦71%


def _brow(xo, yo, xi, yi, th=13.0, bow=8.0):
    """眉。外端が尖り内端が太い三日月。(xo,yo)=外端（こめかみ側）、(xi,yi)=内端（鼻側）。

    ■ 一定太さの線で描いてはいけない
    参考B実物（`ref/_z_ref_sad.png`）の眉は、先が細く根もとが太い三日月である。
    一定太さのストロークにすると一気にクリップアート臭くなる。

    ■ 山を作ってはいけない
    初稿は中間に制御点を置いて弧の頂点を眉の中央に作ってしまい、
    「つらい」が「怒り」に見えた。ダーウィンの言う悲嘆の眉は
    **内端が最高点で、そこから外端へ単調に下る**。頂点を中央に作った時点で別の表情になる。
    bow は反りの量で、山ではない。
    """
    # 上下2本の二次曲線が同じ2点で出会う＝両端が自然に尖る（初稿は内端を L で切ったので角ばった）。
    # 制御点を 0.6 の位置に置き、太い部分を内端寄りに片寄せる（実際の眉もそうなっている）。
    t = 0.6
    px, py = xo + (xi - xo) * t, yo + (yi - yo) * t
    return (f'<path d="M{xo:.1f} {yo:.1f} '
            f'Q{px:.1f} {py - bow - th:.1f} {xi:.1f} {yi:.1f} '
            f'Q{px:.1f} {py - bow + th * 0.35:.1f} {xo:.1f} {yo:.1f} Z" '
            f'fill="{INK}"/>')


def _eye_solid(cx, rx, ry=EYE_RY, y=EYE_Y, tilt=0.0):
    """黒ベタの目。落ち着き・肯定の状態。参考Bの通常時はこれ。

    外側の上に小さな尖り（まつ毛）を足す。参考Bの目にも同じ尖りがある。
    """
    return (f'<g transform="rotate({tilt:.1f} {cx:.1f} {y:.1f})">'
            f'<ellipse cx="{cx:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{INK}"/>'
            f'<path d="M{cx - rx:.1f} {y - ry * 0.45:.1f} '
            f'Q{cx - rx * 1.35:.1f} {y - ry * 1.15:.1f} {cx - rx * 0.35:.1f} {y - ry * 0.98:.1f} Z" '
            f'fill="{INK}"/></g>')


def _eye_lens(cx, rx, y=EYE_Y, tilt=0.0):
    """細めた目。上まぶたが下りて下辺が弧になる＝納得・得心。

    黒ベタを縦に潰すだけでは「小さい目」に見えてしまう。
    上を直線、下を弧にした木の葉形にすると「細めている」になる。
    """
    return (f'<g transform="rotate({tilt:.1f} {cx:.1f} {y:.1f})">'
            f'<path d="M{cx - rx:.1f} {y - 4:.1f} L{cx + rx:.1f} {y - 4:.1f} '
            f'Q{cx:.1f} {y + 20:.1f} {cx - rx:.1f} {y - 4:.1f} Z" fill="{INK}"/>'
            f'<path d="M{cx - rx:.1f} {y - 4:.1f} L{cx + rx:.1f} {y - 4:.1f}" '
            f'stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>')


def _eye_open(cx, rx, ry, px, py, pr, y=EYE_Y):
    """白目＋瞳の目。視線を向けられるので、困り・驚きに使う。

    ry を大きくすると「虹彩の上下に白目が出る」＝驚愕（ダーウィン図版VII）。
    """
    return (f'<ellipse cx="{cx:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="#ffffff" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="{cx + px:.1f}" cy="{y + py:.1f}" r="{pr:.1f}" fill="{INK}"/>'
            f'<circle cx="{cx + px - pr * 0.34:.1f}" cy="{y + py - pr * 0.4:.1f}" '
            f'r="{pr * 0.3:.1f}" fill="#ffffff"/>')


def _eye_arc(cx, rx):
    """上に凸の弧（＾＾）。笑いで目が細くなる形。"""
    return (f'<path d="M{cx - rx:.1f} {EYE_Y + 10:.1f} Q{cx:.1f} {EYE_Y - 22:.1f} '
            f'{cx + rx:.1f} {EYE_Y + 10:.1f}" fill="none" stroke="{INK}" '
            f'stroke-width="8" stroke-linecap="round"/>')


def _mouth_open(w, h, tongue=True):
    """開いた口。輪郭の中に舌と歯列を入れる（参考Bの笑顔がこの構造）。"""
    x, y = MOUTH_X, MOUTH_Y
    out = (f'<path d="M{x - w / 2:.1f} {y - h * 0.35:.1f} Q{x:.1f} {y - h * 0.62:.1f} '
           f'{x + w / 2:.1f} {y - h * 0.35:.1f} Q{x + w * 0.42:.1f} {y + h * 0.62:.1f} '
           f'{x:.1f} {y + h * 0.62:.1f} Q{x - w * 0.42:.1f} {y + h * 0.62:.1f} '
           f'{x - w / 2:.1f} {y - h * 0.35:.1f} Z" fill="{MOUTH_IN}" '
           f'stroke="{INK}" stroke-width="{LW * 0.7:.1f}" stroke-linejoin="round"/>')
    out += (f'<path d="M{x - w * 0.44:.1f} {y - h * 0.3:.1f} L{x + w * 0.44:.1f} {y - h * 0.3:.1f} '
            f'L{x + w * 0.4:.1f} {y - h * 0.12:.1f} L{x - w * 0.4:.1f} {y - h * 0.12:.1f} Z" '
            f'fill="{TOOTH}"/>')
    if tongue:
        out += (f'<ellipse cx="{x:.1f}" cy="{y + h * 0.34:.1f}" rx="{w * 0.27:.1f}" '
                f'ry="{h * 0.24:.1f}" fill="{TONGUE}"/>')
    return out


def _mouth_curve(w, dip, th=7.0):
    """閉じた口。dip>0 で口角が上がり、dip<0 で下がる。"""
    x, y = MOUTH_X, MOUTH_Y
    return (f'<path d="M{x - w / 2:.1f} {y - dip * 0.5:.1f} Q{x:.1f} {y + dip:.1f} '
            f'{x + w / 2:.1f} {y - dip * 0.5:.1f}" fill="none" stroke="{INK}" '
            f'stroke-width="{th}" stroke-linecap="round"/>')


# 眉の端点。(外端x, 内端x) は固定で、y だけを表情ごとに動かす。
# 右向き3/4なので、奥の眉も手前の眉も「内端＝右（鼻側）」になる。
# 手前の眉のほうが少し高い位置に見えるのは、顔の丸みによる遠近（実物でも同じ）。
# 眉の中心は目の中心（far +2 / near +46）の真上に来るよう置く。
# 初稿は左右の眉が近すぎて1本の太い帯に見えたので、あいだを20あける。
BROW_FAR_XO, BROW_FAR_XI = -28.0, 10.0
BROW_NEAR_XO, BROW_NEAR_XI = 30.0, 74.0


def face(kind="normal"):
    """表情5種。右向き3/4を前提に、奥（far＝左）と手前（near＝右）で寸法を変える。

    ■ 5種が一目で区別できることが要件（テレビ距離のシニア視聴者）。
    そのため各表情に「他の4つが持たない手がかり」を必ず1つ以上入れてある。
      普通  … 手がかり無し（基準）
      つらい… 眉が内側上がり＋白目に瞳（視線をそらす）＋波打つ口
      驚き  … 眉が最も高い＋目が最大＋縦長のO
      納得  … 目が木の葉形（細める）＋片眉だけ大きく上げる＋非対称の口＋首を傾ける
      笑顔  … 目が上凸の弧＋開いた口に舌
    """
    f, n = EYE_FAR_X, EYE_NEAR_X
    fo, fi, no, ni = BROW_FAR_XO, BROW_FAR_XI, BROW_NEAR_XO, BROW_NEAR_XI

    if kind == "normal":
        # 普通：眉はゆるい弧でほぼ水平。目は黒ベタ、口はごく浅い弧。
        return "".join([
            _brow(fo, -42, fi, -46, 9, 5), _brow(no, -47, ni, -51, 10, 5),
            _eye_solid(f, EYE_FAR_RX), _eye_solid(n, EYE_NEAR_RX),
            _mouth_curve(46, 7)])

    if kind == "pain":
        # つらい：内端が高く外端が低い（ダーウィン図版II の悲嘆の眉）。
        # 山を作らないよう bow は 1 まで落とす。視線は上へそらし、口角は下げる。
        m = (f'<path d="M{MOUTH_X - 26:.1f} {MOUTH_Y + 3:.1f} '
             f'Q{MOUTH_X - 9:.1f} {MOUTH_Y - 14:.1f} {MOUTH_X + 5:.1f} {MOUTH_Y - 2:.1f} '
             f'Q{MOUTH_X + 17:.1f} {MOUTH_Y + 9:.1f} {MOUTH_X + 28:.1f} {MOUTH_Y - 5:.1f}" '
             f'fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
        return "".join([
            _brow(fo, -33, fi, -55, 9, 0), _brow(no, -38, ni, -60, 10, 0),
            _eye_open(f, 15, 21, -3, -5, 10), _eye_open(n, 18, 23, -4, -6, 11),
            m])

    if kind == "surprise":
        # 驚き：眉を最も高く強い弧に。目は大きく開き虹彩の上下に白目が出る。
        # 口は横に広げず縦長のO（顎が落ちる）。ダーウィン図版VII。
        return "".join([
            _brow(fo, -52, fi, -54, 8, 10), _brow(no, -55, ni, -57, 9, 10),
            _eye_open(f, 17, 27, 0, 0, 8.5), _eye_open(n, 20, 30, 0, 0, 9.5),
            f'<ellipse cx="{MOUTH_X:.1f}" cy="{MOUTH_Y + 4:.1f}" rx="17" ry="25" '
            f'fill="{MOUTH_IN}" stroke="{INK}" stroke-width="{LW * 0.7:.1f}"/>'
            f'<ellipse cx="{MOUTH_X:.1f}" cy="{MOUTH_Y + 16:.1f}" rx="10" ry="8" fill="{TONGUE}"/>'])

    if kind == "convinced":
        # 納得：手前の眉だけ大きく上げ、目を木の葉形に細め、口角を片側だけ上げる。
        # 「うんうん、なるほど」は左右非対称であることが本体（首も傾く＝character() が付ける）。
        return "".join([
            _brow(fo, -42, fi, -45, 9, 5), _brow(no, -56, ni, -61, 10, 8),
            _eye_lens(f, EYE_FAR_RX + 1, tilt=-4), _eye_lens(n, EYE_NEAR_RX + 1, tilt=-4),
            f'<path d="M{MOUTH_X - 24:.1f} {MOUTH_Y + 3:.1f} Q{MOUTH_X + 2:.1f} {MOUTH_Y + 13:.1f} '
            f'{MOUTH_X + 26:.1f} {MOUTH_Y - 9:.1f}" fill="none" stroke="{INK}" '
            f'stroke-width="7" stroke-linecap="round"/>'])

    if kind == "smile":
        # 笑顔：目は上に凸の弧、口は大きく開いて舌が見える。
        # 頬の赤みは参考A（コーヒー・フラットベクター型）から採った。
        return "".join([
            _brow(fo, -48, fi, -51, 8, 7), _brow(no, -52, ni, -55, 9, 7),
            _eye_arc(f, EYE_FAR_RX + 3), _eye_arc(n, EYE_NEAR_RX + 3),
            f'<ellipse cx="{n + 32:.1f}" cy="{EYE_Y + 32:.1f}" rx="15" ry="9" '
            f'fill="{BLUSH}" opacity="0.5"/>',
            _mouth_open(72, 44)])

    raise ValueError(f"未知の表情: {kind}（{FACES} のいずれか）")


# 髪。外側は頭の円弧そのものを A コマンドでなぞる＝輪郭から絶対にはみ出さない。
# 内側（生え際）だけを自由曲線で描く。
#   始点 = 頭の左下（もみあげ） θ=170°  → (-98.5, 17.4)
#   終点 = 頭の右上（前頭部）   θ=-38°  → ( 78.8,-61.6)
# 生え際は右（顔の前）で高く、左へ下る＝**前頭部が後退している**＝60代の記号。
# ■ 生え際の高さは「頭の円弧から何px下か」で決める
# 初稿は生え際を円弧の近くに置いたため、髪が幅5〜15pxの薄い三日月になり
# 髪でなく影に見えた。円が相手なので、x=±60より外では上端そのものが低く、
# 生え際を少し上げただけで髪が消える。前髪の帯は常に 25〜35px 確保する。
# 後頭部からもみあげへ向けて帯を厚くしていくと、丸刈りでない「量のある髪」になる。
HAIR_PATH = ("M-95 31 A100 100 0 1 1 76 -65 "     # 輪郭：もみあげ下端→後頭部→頭頂→前頭部
             "C68 -70 60 -70 54 -66 "              # 生え際。ここで軽く段をつける＝前頭部の後退
             "C44 -60 38 -62 30 -64 "
             "C14 -68 -2 -68 -18 -64 "             # 額の上をほぼ水平に横切る
             "C-42 -58 -62 -46 -74 -26 "           # こめかみへ下る
             "C-82 -12 -88 4 -92 18 "              # もみあげ（耳の前）。ここが最も厚い
             "C-93 23 -94 28 -95 31 Z")

# 毛流れ。3本だけ入れる。髪は塊で塗ると帽子に見え、線を数本入れると髪になる。
# 後ろから前へ撫でつけた向き＝きちんとした60代の整え方。
HAIR_STRANDS = ("M-84 -6 C-66 -34 -38 -52 -6 -56 "
                "M-76 -30 C-54 -52 -24 -64 10 -64 "
                "M-56 -54 C-34 -70 -6 -78 26 -76")


def head(kind="normal", tilt=0.0):
    """頭。実測どおり半径100のほぼ真円＋グレーの髪。原点は頭の中心。

    tilt は首を傾ける角度（頭の下端を軸に回す）。納得のうなずきに使う。

    ■ 描き順：地の肌 → （クリップ内で）影と髪 → 顔 → 最後に輪郭線
    輪郭線を最後に独立して描くのは、髪の塗りが頭からはみ出す事故を
    構造的に起こせなくするため（初稿では髪のハイライトが頭の外に矩形で飛び出した）。
    """
    g = [f'<g transform="rotate({tilt:.1f} 0 {R:.0f})">' if tilt else "<g>",
         f'<circle cx="0" cy="0" r="{R:.0f}" fill="{SKIN}"/>',
         '<g clip-path="url(#ch_head)">',
         # 光源は左上。内側に沿う影を1枚だけ入れる（平塗りを避ける・shading.py 原則1）
         f'<path d="M96 -28 A100 100 0 0 1 -34 96 A132 132 0 0 0 96 -28 Z" '
         f'fill="{SKIN_SH}" opacity="0.42"/>',
         f'<path d="{HAIR_PATH}" fill="{HAIR}" stroke="{INK}" stroke-width="{LW:.1f}" '
         f'stroke-linejoin="round"/>',
         # 髪の艶。頭頂の左寄りに1本だけ（shading.gloss と同じ考え方）
         f'<path d="M-64 -60 C-42 -84 -8 -95 20 -90 C-6 -80 -34 -66 -52 -44 Z" '
         f'fill="#ffffff" opacity="0.20"/>',
         f'<path d="{HAIR_STRANDS}" fill="none" stroke="{HAIR_SH}" stroke-width="4" '
         f'stroke-linecap="round" opacity="0.55"/>',
         "</g>",
         face(kind),
         f'<circle cx="0" cy="0" r="{R:.0f}" fill="none" stroke="{INK}" stroke-width="{LW:.1f}"/>',
         "</g>"]
    return "".join(g)


# ── 骨組み（ポーズごとの関節座標）─────────────────────────────────
# 原点は両足のあいだの接地点。y は上が負。
def _skeleton(pose, stoop):
    """関節の座標を返す。stoop は背中の丸み（1.0 が既定のシニア）。

    fore/back は視点から見た手前と奥。右向き3/4なので手前＝キャラの左半身。
    """
    lean = stoop * 14.0            # 肩が前（右）へ出る量
    # 頭の前傾は「横へずらす」のではなく「肩に沈める」で表す。
    # 初稿は hlean=20 で頭の中心を肩の中心から +34 も横へ出していた。首が無い絵なので、
    # 横へずらすと猫背ではなく「頭が胴に付いていない」としか見えない（2026-07-28指摘）。
    hlean = stoop * 6.0            # 頭が前へ出る量。ごく僅かに留める
    hsink = stoop * 11.0           # 頭が肩へ沈む量。猫背はこちらで見せる
    # 腕は肩の外側から出す。SHOULDER_HW=58 より内側に置くと、手前の腕が胴に重なって
    # 「胸に貼った縞」に、奥の腕は胴に隠れて消え、左右非対称に見える（同指摘）。
    #
    # さらに、**腕の半径ぶんまで外に出す**こと。手前の腕は胴の上に描くので全幅が出るが、
    # 奥の腕は胴の後ろに描くので、胴に少しでも掛かるとその分だけ細く見える。
    # ax=62 では奥の腕が3割方隠れ、太さが左右で違って見えた。
    # 必要量 = SHOULDER_HW(58) + ARM_W/2(13) + lean(14) = 85 … 手前側で余裕を見て 72 とする
    ax = 72.0

    if pose in ("stand", "point", "hold"):
        sy, hipy = SHOULDER_Y, HIP_Y
        sk = dict(
            hip=(0, hipy), sh=(lean, sy),
            head=(lean + hlean, sy - R + hsink),
            # 脚は腰で離してから、ほぼ垂直に落とす。腰で重ねると1本の塊に見え、
            # そこから下だけ開くので「Λ」になって不自然（初稿）。
            # 間隔は脚の太さ(34)より広く取る。±26 では輪郭線どうしが接して
            # ズボン1本の真ん中に線が入っただけに見え、靴も中央でくっついた（2稿）
            leg_back=[(-34, hipy), (-38, -96), (-42, -16)],
            leg_fore=[(34, hipy), (38, -96), (42, -16)],
            foot_back=(-42, -16), foot_fore=(42, -16), foot_back_out=True,
        )
        # 腕は肩幅(58)のすぐ内側から出し、肘で外へ振る。
        # 初稿は肩を ±34 に置いたため、腕が胴の輪郭の内側に完全に隠れて片腕に見えた。
        if pose == "point":
            # 指差し：肩→肘→手が一直線にならないよう肘を少し上げる。
            sk["arm_fore"] = [(lean + ax, sy + 12), (lean + 112, sy + 34), (lean + 180, sy + 52)]
            sk["hand_fore"] = ((lean + 180, sy + 52), "point", -12)
            sk["arm_back"] = [(lean - ax, sy + 14), (lean - ax - 14, sy + 78),
                              (lean - ax - 8, sy + 142)]
            sk["hand_back"] = ((lean - ax - 8, sy + 142), "plain", 0)
        elif pose == "hold":
            # 持つ：手前の腕だけ胸の高さへ上げる（参考Bの肥料の袋がこの形）。
            # 手は顔から十分離す。近すぎると持たせた小道具が頭に重なる。
            sk["arm_fore"] = [(lean + ax, sy + 12), (lean + 96, sy + 60), (lean + 152, sy + 36)]
            sk["hand_fore"] = ((lean + 152, sy + 36), "grip", 12)
            sk["arm_back"] = [(lean - ax, sy + 14), (lean - ax - 14, sy + 76),
                              (lean - ax - 8, sy + 140)]
            sk["hand_back"] = ((lean - ax - 8, sy + 140), "plain", 0)
        else:
            # 立つ：左右を鏡像にする。肩→肘で外へ14開き、肘→手でわずかに戻す
            sk["arm_fore"] = [(lean + ax, sy + 12), (lean + ax + 14, sy + 76),
                              (lean + ax + 8, sy + 142)]
            sk["hand_fore"] = ((lean + ax + 8, sy + 142), "plain", 0)
            sk["arm_back"] = [(lean - ax, sy + 12), (lean - ax - 14, sy + 76),
                              (lean - ax - 8, sy + 142)]
            sk["hand_back"] = ((lean - ax - 8, sy + 142), "plain", 0)
        return sk

    if pose == "sit":
        # マイブリッジ Plate 241 の実測より：
        #   座面 = 脛の長さ（-92）／腰は座面の奥／膝は腰より腿1本ぶん前
        #   脛はほぼ垂直に落ちる／上体は約10度前傾
        seat = -92.0
        hipx, hipy = -26.0, seat - 4      # 尻は座面のすぐ上に載る（初稿は浮いていた）
        lean2 = lean + 22.0
        sy = hipy - 145.0
        return dict(
            hip=(hipx, hipy), sh=(hipx + lean2, sy), seat_y=seat, hem=seat + 2,
            head=(hipx + lean2 + hlean * 0.8, sy - R + hsink * 0.8),
            # 腿はほぼ水平、膝が前へ出て、脛が垂直に落ちる
            leg_back=[(hipx - 6, hipy - 8), (hipx + 106, hipy - 6), (hipx + 96, -16)],
            leg_fore=[(hipx + 8, hipy + 2), (hipx + 120, hipy + 4), (hipx + 110, -16)],
            foot_back=(hipx + 96, -16), foot_fore=(hipx + 110, -16),
            # 手は腿の上に置く
            arm_fore=[(hipx + lean2 + ax, sy + 12), (hipx + lean2 + 76, sy + 64),
                      (hipx + lean2 + 104, sy + 100)],
            hand_fore=((hipx + lean2 + 104, sy + 100), "plain", 20),
            arm_back=[(hipx + lean2 - ax, sy + 14), (hipx + lean2 - 52, sy + 66),
                      (hipx + lean2 + 8, sy + 102)],
            hand_back=((hipx + lean2 + 8, sy + 102), "plain", 20),
        )

    if pose == "lie":
        # マイブリッジ Plate 263 の実測より：
        #   頭は枕のぶんだけ寝床から浮く／肩が最も高く腰へなだらかに下がる／膝は軽く曲げる
        # 横から見た寝姿。頭は左、原点は寝床の面の中央。
        #
        # ■ 胴の厚みは肩幅ではなく「体の奥行き」
        #   初稿は胴を肩幅と同じ太さで描いたため、青い腸詰めに見えた。
        #   横たわった体を横から見たときの高さ＝奥行き＝肩幅の約2/3（76）。
        # ■ 頭は枕の上なので胴よりはっきり高い。ここを揃えると死体に見える。
        return dict(
            head=(-198, -146), sh=(-92, -92), hip=(58, -80), lying=True,
            head_tilt=-14.0, pillow=True, blanket=True, torso_w=76.0,
            leg_back=[(50, -74), (184, -62), (232, -28)],
            leg_fore=[(62, -88), (198, -70), (248, -34)],
            foot_back=(232, -28), foot_fore=(248, -34),
            arm_fore=[(-78, -76), (-12, -48), (54, -44)],
            hand_fore=((54, -44), "plain", 60),
            arm_back=[(-86, -108), (-24, -84), (34, -76)],
            hand_back=((34, -76), "plain", 60),
        )

    raise ValueError(f"未知のポーズ: {pose}（{POSES} のいずれか）")


def _shoe(x, y, col, lying=False, out=False):
    """靴。横から見た形＝かかとが丸く、つま先が前へ出る。

    out=True でつま先を逆向き（外向き）にする。**立ち姿では必ず奥足に付けること。**
    両足を同じ向きにすると、奥の足のつま先が体の中心を跨いで内股に見える（2026-07-28指摘）。
    """
    if lying:   # 寝ているときは足裏が横を向く
        return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="24" ry="18" fill="{col}" '
                f'stroke="{INK}" stroke-width="{LW:.1f}"/>')
    d = (f'M{-20:.1f} {-14:.1f} q0 -8 10 -8 q12 0 13 8 '
         f'q16 3 22 10 q4 6 -3 8 h-38 q-6 0 -6 -8 z')
    tr = f'translate({x:.1f},{y:.1f})' + (' scale(-1,1)' if out else '')
    return (f'<g transform="{tr}"><path d="{d}" fill="{col}" '
            f'stroke="{INK}" stroke-width="{LW:.1f}" stroke-linejoin="round"/></g>')


def _seat(sk, show=True):
    """腰かけ。座るポーズは支えが無いと空中でしゃがんでいるようにしか見えない。

    座面の高さは骨組みが持っている座面値をそのまま使う（＝脛の長さと一致する）。
    場面側でソファや椅子を描くときは character(..., seat=False) で消す。
    """
    if not show or "seat_y" not in sk:
        return ""
    sy = sk["seat_y"]
    x0, x1 = sk["hip"][0] - 86, sk["hip"][0] + 66
    legs = "".join(
        f'<rect x="{x:.0f}" y="{sy + 12:.0f}" width="15" height="{-sy - 12:.0f}" rx="6" '
        f'fill="#b08a5e" stroke="{INK}" stroke-width="{LW * 0.8:.1f}"/>'
        for x in (x0 + 14, x1 - 30))
    return (legs + f'<rect x="{x0:.0f}" y="{sy:.0f}" width="{x1 - x0:.0f}" height="22" rx="8" '
            f'fill="#c79a68" stroke="{INK}" stroke-width="{LW:.1f}"/>')


def _bedding(sk, cos, part):
    """枕と掛け布団。寝るポーズの一部として持たせる。

    枕は「頭が寝床から浮いている根拠」そのものなので省略できない。
    掛け布団は胸から下を覆う。実際にそう見えるうえに、
    横たわった脚という最も破綻しやすい形をまとめて隠せる。
    """
    if part == "pillow":
        # ふっくらした枕。角を張らせると敷布団に見えてしまう。
        return (f'<path d="M-308 -2 C-320 -54 -294 -70 -258 -68 '
                f'C-222 -66 -180 -70 -150 -64 C-116 -58 -106 -32 -112 -2 Z" '
                f'fill="#f4ecdc" stroke="{INK}" stroke-width="{LW:.1f}" stroke-linejoin="round"/>'
                f'<path d="M-290 -18 C-268 -44 -216 -52 -172 -46" fill="none" '
                f'stroke="{INK}" stroke-width="4" opacity="0.3"/>')
    # 掛け布団。胸から下を覆う。左端を胸より先まで伸ばして、腕や手がはみ出さないようにする。
    blanket = ("M-104 -2 C-112 -98 -48 -128 20 -122 "
               "C112 -114 208 -100 264 -70 C304 -50 324 -26 322 -2 Z")
    return (f'<path d="{blanket}" fill="#c3d5dd" stroke="{INK}" stroke-width="{LW:.1f}" '
            f'stroke-linejoin="round"/>'
            # 縁の折り返し。帯で塗ると縞に見えたので、輪郭に沿う線1本で厚みを出す。
            f'<path d="M-84 -2 C-92 -96 -38 -120 24 -114 C114 -106 206 -92 262 -64" '
            f'fill="none" stroke="{INK}" stroke-width="4.5" opacity="0.34"/>')


def _torso(sk, cos, pose):
    """胴。肩から腰へゆるく絞る。参考Bの胴は頭の0.58倍しかない。"""
    (sx, sy), (hx, hy) = sk["sh"], sk["hip"]
    if sk.get("lying"):
        # 横たわった体を横から見た高さ＝体の奥行き。肩幅で描くと腸詰めになる。
        return _limb([(sx, sy), (hx, hy)], sk.get("torso_w", 76.0), cos["top"])
    top, bot = SHOULDER_HW, HIP_HW
    hem = sk.get("hem", hy) + (40 if cos["skirt"] else 0)   # 白衣は腰より下まで伸びる
    d = (f"M{sx - top:.1f} {sy + 16:.1f} "
         f"Q{sx - top - 4:.1f} {sy - 6:.1f} {sx - top + 20:.1f} {sy - 10:.1f} "   # 肩の丸み（奥）
         f"L{sx + top - 20:.1f} {sy - 10:.1f} "
         f"Q{sx + top + 4:.1f} {sy - 6:.1f} {sx + top:.1f} {sy + 16:.1f} "        # 肩の丸み（手前）
         f"L{hx + bot:.1f} {hem - 14:.1f} "
         f"Q{hx + bot:.1f} {hem:.1f} {hx + bot - 16:.1f} {hem:.1f} "              # 裾の丸み
         f"L{hx - bot + 16:.1f} {hem:.1f} "
         f"Q{hx - bot:.1f} {hem:.1f} {hx - bot:.1f} {hem - 14:.1f} Z")
    out = _shape(d, cos["top"])
    # 襟もと：首が無いので、V字を入れて「服を着ている」ことだけ示す
    out += (f'<path d="M{sx - 22:.1f} {sy - 8:.1f} L{sx + 2:.1f} {sy + 30:.1f} '
            f'L{sx + 26:.1f} {sy - 8:.1f}" fill="{cos["inner"]}" stroke="{INK}" '
            f'stroke-width="{LW * 0.7:.1f}" stroke-linejoin="round"/>')
    if cos["skirt"]:      # 白衣の前立てとポケット
        out += (f'<path d="M{sx + 2:.1f} {sy + 30:.1f} L{hx + 6:.1f} {hem:.1f}" fill="none" '
                f'stroke="{INK}" stroke-width="4" opacity="0.55"/>'
                f'<rect x="{hx + 12:.1f}" y="{hy - 26:.1f}" width="34" height="28" rx="4" '
                f'fill="none" stroke="{INK}" stroke-width="4" opacity="0.55"/>')
    else:
        out += (f'<circle cx="{sx + 4:.1f}" cy="{sy + 62:.1f}" r="4.5" fill="{INK}" opacity="0.5"/>'
                f'<circle cx="{sx + 6:.1f}" cy="{sy + 100:.1f}" r="4.5" fill="{INK}" opacity="0.5"/>')
    return out


def _dots(sk, cos):
    """パジャマの水玉。決定論的に散らす（palette.spread と同じ線形合同法）。

    横たわった姿勢では散らさない。立ち姿の胴の範囲で座標を作っているため、
    寝かせると枕の上まで水玉が飛び散る（実際にそうなった）。
    どのみち掛け布団で胴は隠れるので、描く意味も無い。
    """
    if not cos["dots"] or sk.get("lying"):
        return ""
    (sx, sy), (hx, hy) = sk["sh"], sk["hip"]
    out, s = [], 20260728
    for _ in range(26):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        x = sx - 46 + (s >> 9) % 92
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        y = sy + 16 + (s >> 9) % max(1, int(hy - sy + 110))
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#ffffff" opacity="0.85"/>')
    return "".join(out)


class Character(str):
    """SVG文字列。f-string にそのまま差し込めるが、`.anchors` で手の座標も取れる。"""
    anchors: dict


def character(pose="stand", face_kind="normal", *, costume="casual", flip=False,
              scale=1.0, at=(0.0, 0.0), stoop=1.0, shadow=True, tilt=None,
              seat=True, blanket=True):
    """キャラクター1体を返す。

    pose     … stand / sit / lie / point / hold
    face_kind… normal / pain / surprise / convinced / smile
    costume  … casual（カーディガン）/ coat（白衣）/ pajama
    at       … 接地点の座標。寝る場合は寝床の面の左右中央。
    stoop    … 背中の丸み。1.0=既定のシニア、0=背筋が伸びた状態（やめた後）
    tilt     … 首の傾き。既定では納得のときだけ自動で少し傾く。
    seat     … 座るポーズに腰かけを付けるか（場面が椅子を持つなら False）
    blanket  … 寝るポーズに掛け布団を掛けるか（枕は常に付く）

    覚え書き：**寝る × 笑顔** は目が上凸の弧になるので「安らかに眠っている」に見える。
    睡眠の回で「よく眠れた朝」を出したいときはこの組み合わせを使う。
    """
    if pose not in POSES:
        raise ValueError(f"未知のポーズ: {pose}（{POSES} のいずれか）")
    if face_kind not in FACES:
        raise ValueError(f"未知の表情: {face_kind}（{FACES} のいずれか）")
    cos = COSTUMES[costume]
    sk = _skeleton(pose, stoop)
    if tilt is None:
        tilt = sk.get("head_tilt", -7.0 if face_kind == "convinced" else 0.0)

    body = []
    if shadow and not sk.get("lying"):
        body.append(f'<ellipse cx="{sk["hip"][0]:.0f}" cy="6" rx="96" ry="17" '
                    f'fill="{INK}" opacity="0.16"/>')
    if sk.get("pillow"):
        body.append(_bedding(sk, cos, "pillow"))
    if pose == "sit":
        body.append(_seat(sk, seat))

    # 奥→手前の順に描く。奥側は暗く落として前後を分ける。
    body.append(f'<g opacity="0.82">'
                f'{_limb(sk["leg_back"], LEG_W, cos["pants"])}'
                f'{_shoe(*sk["foot_back"], cos["shoe"], sk.get("lying", False), sk.get("foot_back_out", False))}'
                f'{_limb(sk["arm_back"], ARM_W, cos["top"])}'
                f'{_hand(sk["hand_back"][0][0], sk["hand_back"][0][1], *sk["hand_back"][1:])}</g>')
    body.append(_limb(sk["leg_fore"], LEG_W, cos["pants"]))
    body.append(_shoe(*sk["foot_fore"], cos["shoe"], sk.get("lying", False)))
    body.append(_torso(sk, cos, pose))
    body.append(_dots(sk, cos))
    body.append(_limb(sk["arm_fore"], ARM_W, cos["top"]))
    body.append(_hand(sk["hand_fore"][0][0], sk["hand_fore"][0][1], *sk["hand_fore"][1:]))
    hx, hy = sk["head"]
    body.append(f'<g transform="translate({hx:.1f},{hy:.1f})">{head(face_kind, tilt)}</g>')
    if sk.get("blanket") and blanket:
        # 布団は体の上に掛かる＝頭より後に描く
        body.append(_bedding(sk, cos, "blanket"))

    tr = f'translate({at[0]:.1f},{at[1]:.1f}) scale({-scale if flip else scale:.4f},{scale:.4f})'
    out = Character(f'<g transform="{tr}">{"".join(body)}</g>')

    def _world(p):
        x, y = p
        return (at[0] + (-x if flip else x) * scale, at[1] + y * scale)

    out.anchors = {
        "hand": _world(sk["hand_fore"][0]),   # 小道具を持たせる位置
        "head": _world(sk["head"]),           # 吹き出しの根もと
        "top": _world((sk["head"][0], sk["head"][1] - R)),
        "hip": _world(sk["hip"]),
    }
    return out


def defs():
    """このモジュールが使う定義。id は ch_ で始めて anatomy.defs() と衝突させない。

    ch_head … 頭の内側だけを描くためのクリップ。髪や影が輪郭からはみ出す事故を防ぐ。
              頭ローカル座標（中心が原点・半径100）で定義してあるので、
              character() がどこに何倍で置いても正しく効く。
    """
    return (f'<clipPath id="ch_head"><circle cx="0" cy="0" r="{R:.0f}"/></clipPath>'
            '<filter id="ch_soft" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="{INK}" '
            'flood-opacity="0.22"/></filter>')


# ── 検証用：一覧シート ────────────────────────────────────────
def _page(inner, w, h, bg="#f6efe2"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><defs>{defs()}</defs>'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{inner}</svg>')


def _cap(x, y, t, size=42):
    return (f'<text x="{x}" y="{y}" font-family="Noto" font-size="{size}" '
            f'fill="{INK}" text-anchor="middle">{t}</text>')


def sheet_faces():
    """表情5種を顔だけで並べる。"""
    W, H = 1900, 620
    g = [_cap(W // 2, 78, "表情5種（頭径200・右向き3/4）", 48)]
    for i, k in enumerate(FACES):
        cx = 190 + i * 380
        g.append(f'<g transform="translate({cx},330) scale(1.35)">{head(k)}</g>')
        g.append(_cap(cx, 560, FACE_JA[k]))
    return _page("".join(g), W, H)


def sheet_poses():
    """ポーズ5種を全身で並べる。寝るは横に長いので別の段に置く。"""
    W, H = 1900, 1420
    g = [_cap(W // 2, 70, "ポーズ5種（2.65頭身・接地点そろえ）", 48)]
    for i, k in enumerate(["stand", "sit", "point", "hold"]):
        cx = 250 + i * 470
        g.append(f'<g transform="translate({cx},700) scale(1.0)">'
                 f'{character(k, "normal", at=(0, 0))}</g>')
        g.append(_cap(cx, 776, POSE_JA[k]))
    g.append(f'<g transform="translate({W // 2 - 60},1290) scale(1.0)">'
             f'{character("lie", "convinced", costume="pajama", at=(0, 0))}</g>')
    g.append(_cap(W // 2, 1370, "寝る（枕・掛け布団つき。表情を替えれば不眠・熟睡を描き分けられる）", 36))
    return _page("".join(g), W, H)


def sheet_grid():
    """5表情 × 5ポーズ の総当たり。"""
    cw, chh = 360, 400
    W, H = cw * 5 + 190, chh * 5 + 170
    g = [_cap(W // 2, 68, "表情5種 × ポーズ5種", 46)]
    for r, fk in enumerate(FACES):
        y = 150 + r * chh
        g.append(f'<text x="94" y="{y + chh // 2}" font-family="Noto" font-size="34" '
                 f'fill="{INK}" text-anchor="middle">{FACE_JA[fk]}</text>')
        for c, pk in enumerate(POSES):
            x = 190 + c * cw + cw // 2
            if r == 0:
                g.append(_cap(x, 128, POSE_JA[pk], 36))
            g.append(f'<g transform="translate({x},{y + chh - 40}) scale(0.62)">'
                     f'{character(pk, fk, at=(0, 0))}</g>')
    return _page("".join(g), W, H)


if __name__ == "__main__":
    import base64
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    sys.stdout.reconfigure(encoding="utf-8")
    import render

    FONTS = Path(r"C:\Users\konar\Desktop\zankoku-sekkeizu\public\fonts")
    b = base64.b64encode((FONTS / "NotoSansJP-Bold.woff2").read_bytes()).decode()
    css = ("@font-face{font-family:'Noto';src:url(data:font/woff2;base64,"
           + b + ") format('woff2');font-weight:400;font-display:block;}")
    out = Path(__file__).parent.parent / "out"
    # メモリ4GBのため直列で焼く
    for name, svg, w, h in [("char_faces", sheet_faces(), 1900, 620),
                            ("char_poses", sheet_poses(), 1900, 1420),
                            ("char_grid", sheet_grid(), 360 * 5 + 190, 400 * 5 + 170)]:
        html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
                f'body{{width:{w}px;height:{h}px;overflow:hidden}}</style></head>'
                f'<body>{svg}</body></html>')
        render.png(html, out / f"{name}.png", w, h)
        print("wrote", out / f"{name}.png")
