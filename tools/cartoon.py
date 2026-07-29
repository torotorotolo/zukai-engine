# -*- coding: utf-8 -*-
"""EHL5様式のキャラクター部品。

■ これは何か
`character.py`（棒人間・HSS様式）とは別系統。到達目標に定めた
**Explaining Health Like You're Five**（192万回）の画風を再現するための部品。
分解の正本 → Vault `Resources/参考-EHL5秒単位分解-20260729.md`

■ 比率と色は実測から起こした
参考フレーム `ref/ehl5_body.jpg`（1280x720・全身が写るカット）を画素で計測：

| 項目 | 実測（1280px幅の画面で） | 本モジュールの単位 |
|---|---|---|
| 全高 | 670px | **1000** |
| 頭（髪の頂点〜顎） | 240px | **360** ＝ **2.78頭身** |
| 頭幅（髪込み） | 280px | 420 |
| 肩幅 | 約365px | 350（**頭幅より狭い**） |
| 目の位置 | 髪の生え際から顔の40% | y=-830 |
| 輪郭線 | 9〜10px | **16**（1920pxで約15px相当） |

| 色 | 実測 |
|---|---|
| 肌 | `#f5ac46`（**かなり橙に寄った暖色**。肌色ではない） |
| 髪 | `#502103` |
| シャツ | `#026853` |
| ジーンズ | `#1c3c47` |
| **白目** | `#f8eabd`（**純白ではなくクリーム**） |
| 瞳 | `#060200` |

■ 背景との描き分け（EHL5様式の核心）
参考フレームのソファを走査したところ **暗い線が1本も検出されなかった**。
つまり **前景＝黒の太輪郭＋高彩度／背景＝輪郭線を引かない＋低彩度**。
奥行きは描き込み量ではなくこの差で作る。背景を描くときは `bg_ink()` を使うこと。
"""
import math

# ── 色 ──────────────────────────────────────────────────
INK = "#171210"            # 前景の輪郭。純黒でなくわずかに温かい
SKIN = "#f5ac46"
SKIN_SH = "#dd9130"
HAIR = "#502103"
HAIR_HI = "#6e3a12"
SHIRT = "#026853"
SHIRT_SH = "#014b3c"
PANTS = "#1c3c47"
PANTS_SH = "#132b33"
SHOE = "#8a4f16"
SOLE = "#e8d8c4"
EYE_W = "#f8eabd"          # 白目はクリーム
PUPIL = "#0a0603"
MOUTH_IN = "#7d3326"
TONGUE = "#d4675a"
COAT = "#fbf7ee"
COAT_SH = "#e6dfd0"

LW = 16.0                  # 前景の輪郭線。全高1000に対する太さ

# ── 骨格（原点＝両足の接地点、上が負） ──────────────────────
# すべて参考フレームの画素から換算（1280px幅の値 × 1.493）
FOOT_Y = 0.0
ANKLE_Y = -67.0
KNEE_Y = -179.0            # 初稿は-230にしていて脚が短く見えた
HIP_Y = -343.0
WAIST_Y = -360.0
SHOULDER_Y = -582.0
NECK_Y = -620.0
CHIN_Y = -638.0
FACE_CY = -819.0           # 顔（肌）の中心
HAIR_TOP = -1000.0
HAIRLINE_Y = -873.0

FACE_RX, FACE_RY = 190.0, 181.0     # **横に広い**。丸顔でなく角の取れた四角
SH_HW = 183.0              # 肩の半幅。頭の半幅(209)より狭い
WAIST_HW = 175.0           # 胴はほとんど絞らない
HIP_HW = 168.0
ARM_W = 75.0
LEG_W = 112.0
SLEEVE_Y = -470.0          # 半袖の裾。ここから下は素肌

EYE_Y = -784.0             # 初稿は-830で目が高すぎ、額が無かった
EYE_DX = 58.0
EYE_RX, EYE_RY = 41.0, 45.0
PUPIL_R = 21.0
BROW_Y = -851.0
NOSE_Y = -724.0
MOUTH_Y = -675.0

FACES = ("normal", "smile", "worry", "shock", "tired")
POSES = ("stand", "hips", "point", "hold", "walk")


def _sh(d, fill, lw=LW, op=1.0):
    return (f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{lw:.1f}" '
            f'stroke-linejoin="round" stroke-linecap="round" opacity="{op}"/>')


def _limb(pts, w, col):
    """腕・脚。太い線として描き、両端を丸める。"""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        x, y = pts[i]
        nx, ny = pts[i + 1]
        d += f" Q{x:.1f} {y:.1f} {(x + nx) / 2:.1f} {(y + ny) / 2:.1f}"
    d += f" L{pts[-1][0]:.1f} {pts[-1][1]:.1f}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + LW:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _hand(x, y, ang=0.0, kind="fist"):
    """手。指を描き分けず、ミトン状の塊に親指を1本だけ付ける。"""
    if kind == "point":
        g = (f'<path d="M-34 -6 q-8 -34 18 -38 q22 -4 26 16 l0 10 '
             f'q26 -4 30 10 q4 16 -14 22 q-24 8 -46 2 q-16 -6 -14 -22 Z" '
             f'fill="{SKIN}" stroke="{INK}" stroke-width="{LW:.1f}" stroke-linejoin="round"/>'
             f'<path d="M18 -18 h56" stroke="{INK}" stroke-width="{LW:.1f}" '
             f'stroke-linecap="round"/>'
             f'<path d="M18 -18 h56" stroke="{SKIN}" stroke-width="{LW * 1.6:.1f}" '
             f'stroke-linecap="round"/>')
    else:
        # 手は前腕とほぼ同じ太さにする。小さいと腕の先に玉が付いて見える
        g = (f'<ellipse rx="46" ry="42" fill="{SKIN}" stroke="{INK}" '
             f'stroke-width="{LW:.1f}"/>'
             f'<path d="M-34 -16 q-14 12 -2 24" fill="none" stroke="{INK}" '
             f'stroke-width="{LW * 0.6:.1f}" stroke-linecap="round" opacity="0.75"/>')
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">{g}</g>'


def _shoe(x, y, flip=False):
    """靴（横から見たスニーカー）。甲とソールの幅を必ず揃えること。
    初稿はソールだけ長く、足の下に白い板が飛び出して見えた。"""
    upper = ("M-72 -26 C-78 -60 -60 -84 -30 -84 C-4 -84 6 -66 10 -46 "
             "C44 -42 76 -40 88 -26 Z")
    sole = ("M-76 -26 H92 C104 -26 106 -14 100 -6 C94 0 -70 0 -76 -4 "
            "C-84 -10 -84 -22 -76 -26 Z")
    tr = f'translate({x:.1f},{y:.1f})' + (' scale(-1,1)' if flip else '')
    return (f'<g transform="{tr}">{_sh(upper, SHOE)}'
            f'<path d="{sole}" fill="{SOLE}" stroke="{INK}" stroke-width="{LW * 0.9:.1f}" '
            f'stroke-linejoin="round"/>'
            f'<path d="M-40 -70 q26 14 34 34" fill="none" stroke="{SOLE}" '
            f'stroke-width="{LW * 0.8:.1f}" stroke-linecap="round" opacity="0.9"/></g>')


# ── 顔 ────────────────────────────────────────────────────

def _eye(cx, kind, blink=0.0, look=0.0):
    """目。blink 0=開 1=閉。look は瞳の左右のずれ（-1〜1）。"""
    ry = EYE_RY * (1.0 - blink)
    if ry < 5:
        return (f'<path d="M{cx - EYE_RX:.0f} {EYE_Y:.0f} q{EYE_RX:.0f} 14 '
                f'{EYE_RX * 2:.0f} 0" fill="none" stroke="{INK}" '
                f'stroke-width="{LW * 0.85:.1f}" stroke-linecap="round"/>')
    px = cx + look * 14
    py = EYE_Y + (6 if kind in ("worry", "tired") else 0)
    pr = PUPIL_R * (1.25 if kind == "shock" else 1.0)
    g = (f'<ellipse cx="{cx:.0f}" cy="{EYE_Y:.0f}" rx="{EYE_RX:.0f}" ry="{ry:.0f}" '
         f'fill="{EYE_W}" stroke="{INK}" stroke-width="{LW * 0.9:.1f}"/>'
         f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{pr:.0f}" fill="{PUPIL}"/>'
         f'<circle cx="{px - pr * 0.32:.0f}" cy="{py - pr * 0.38:.0f}" r="{pr * 0.26:.0f}" '
         f'fill="#ffffff" opacity="0.9"/>')
    if kind == "tired":     # 上まぶたを下ろす
        g += (f'<path d="M{cx - EYE_RX - 4:.0f} {EYE_Y - ry * 0.25:.0f} '
              f'q{EYE_RX:.0f} {-ry * 0.9:.0f} {EYE_RX * 2 + 8:.0f} 0 '
              f'l0 {-ry:.0f} l{-EYE_RX * 2 - 8:.0f} 0 Z" fill="{SKIN}" '
              f'stroke="{INK}" stroke-width="{LW * 0.9:.1f}" stroke-linejoin="round"/>')
    return g


def _brow(cx, kind, side):
    """眉。太い短線。左右で角度を変えて表情を作る。"""
    y = BROW_Y
    ang = {"normal": 0, "smile": -4, "worry": 16, "shock": -10, "tired": 10}[kind] * side
    return (f'<g transform="translate({cx:.0f},{y:.0f}) rotate({ang})">'
            f'<path d="M-38 4 q38 -20 76 0" fill="none" stroke="{HAIR}" '
            f'stroke-width="{LW * 1.05:.1f}" stroke-linecap="round"/></g>')


def _mouth(kind, open_amt=0.0):
    """口。open_amt 0=閉 1=大きく開く。口パクはこれを動かす。"""
    y = MOUTH_Y
    if open_amt > 0.08:
        h = 20 + 52 * open_amt
        w = 44 + 22 * open_amt
        return (f'<path d="M{-w:.0f} {y:.0f} q{w:.0f} -16 {w * 2:.0f} 0 '
                f'q{-w * 0.5:.0f} {h:.0f} {-w * 2:.0f} 0 Z" fill="{MOUTH_IN}" '
                f'stroke="{INK}" stroke-width="{LW * 0.85:.1f}" stroke-linejoin="round"/>'
                f'<path d="M{-w * 0.55:.0f} {y + h * 0.45:.0f} q{w * 0.55:.0f} '
                f'{h * 0.5:.0f} {w * 1.1:.0f} 0 Z" fill="{TONGUE}"/>')
    # 二次ベジエの実際の垂れは制御点のyの半分。18では平らな線にしか見えなかった
    bow = {"normal": 38, "smile": 78, "worry": -38, "shock": 24, "tired": -30}[kind]
    w = 58 if kind != "smile" else 74
    return (f'<path d="M{-w:.0f} {y:.0f} q{w:.0f} {bow:.0f} {w * 2:.0f} 0" fill="none" '
            f'stroke="{INK}" stroke-width="{LW * 1.1:.1f}" stroke-linecap="round"/>')


def _hair(style="short"):
    """髪。塊で描き、明るい面を1枚だけ重ねる。原点は顔の中心 FACE_CY。

    参考は**左上へ流れる前髪と、右へ抜ける分け目**。生え際(-873)より下へ
    もみあげが少し降りる。左右対称のヘルメットにしないこと。
    """
    top = HAIR_TOP - FACE_CY          # -181
    hl = HAIRLINE_Y - FACE_CY         # -54
    if style == "bald":
        return ""
    if style == "curly":
        d = (f"M-196 {hl + 40:.0f} q-30 -86 44 -122 q26 -66 108 -54 q70 -34 122 26 "
             f"q74 12 58 84 q-40 -44 -110 -46 q-84 -4 -132 34 q-46 36 -90 78 Z")
        return (f'<g transform="translate(0,{FACE_CY:.0f})">{_sh(d, HAIR)}'
                + "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{HAIR}" '
                          f'stroke="{INK}" stroke-width="{LW:.1f}"/>'
                          for cx, cy, r in [(-150, -96, 44), (-70, -140, 50), (24, -156, 52),
                                            (110, -128, 46), (166, -70, 40)])
                + f'<path d="M-60 -150 q60 -34 122 -6 q-66 -6 -110 24 Z" '
                  f'fill="{HAIR_HI}" opacity="0.75"/></g>')
    # 短髪
    d = (f"M-196 {hl + 22:.0f} "
         f"C-206 {top + 44:.0f} -140 {top - 16:.0f} -40 {top - 22:.0f} "
         f"C68 {top - 28:.0f} 176 {top + 30:.0f} 194 {hl - 34:.0f} "
         f"C200 {hl - 6:.0f} 196 {hl + 26:.0f} 190 {hl + 44:.0f} "
         f"C170 {hl - 24:.0f} 96 {hl - 52:.0f} 20 {hl - 40:.0f} "
         f"C-56 {hl - 28:.0f} -128 {hl + 12:.0f} -172 {hl + 62:.0f} Z")
    hi = (f"M-118 {top + 46:.0f} C-46 {top - 12:.0f} 62 {top - 8:.0f} 132 {top + 52:.0f} "
          f"C58 {top + 8:.0f} -46 {top + 12:.0f} -118 {top + 46:.0f} Z")
    side = (f"M-196 {hl + 22:.0f} C-200 {hl + 62:.0f} -194 {hl + 96:.0f} -182 {hl + 118:.0f} "
            f"C-172 {hl + 78:.0f} -180 {hl + 46:.0f} -172 {hl + 62:.0f} Z")
    return (f'<g transform="translate(0,{FACE_CY:.0f})">'
            f'{_sh(d, HAIR)}{_sh(side, HAIR)}'
            f'<path d="{hi}" fill="{HAIR_HI}" opacity="0.8"/></g>')


def head(face="normal", *, hair="short", blink=0.0, mouth=0.0, look=0.0, tilt=0.0):
    """顔ひとつ。原点はキャラの接地点基準（FACE_CY に顔がある）。"""
    ear = (f'<path d="M{-FACE_RX + 14:.0f} {FACE_CY - 4:.0f} '
           f'q-42 -8 -40 34 q2 42 44 34 Z" fill="{SKIN}" stroke="{INK}" '
           f'stroke-width="{LW:.1f}" stroke-linejoin="round"/>')
    # 顔＝角の取れた四角。丸にすると赤ん坊になる。顎はわずかに細く、下端は平ら
    skin = (f'<path d="M{-FACE_RX:.0f} {FACE_CY - 40:.0f} '
            f'C{-FACE_RX:.0f} {FACE_CY - FACE_RY - 26:.0f} '
            f'{-FACE_RX * 0.55:.0f} {FACE_CY - FACE_RY - 44:.0f} 0 {FACE_CY - FACE_RY - 44:.0f} '
            f'C{FACE_RX * 0.60:.0f} {FACE_CY - FACE_RY - 44:.0f} '
            f'{FACE_RX:.0f} {FACE_CY - FACE_RY + 4:.0f} {FACE_RX:.0f} {FACE_CY - 30:.0f} '
            f'C{FACE_RX:.0f} {FACE_CY + 62:.0f} {FACE_RX * 0.80:.0f} {CHIN_Y - 6:.0f} '
            f'{FACE_RX * 0.34:.0f} {CHIN_Y:.0f} '
            f'C{-FACE_RX * 0.30:.0f} {CHIN_Y + 8:.0f} {-FACE_RX * 0.86:.0f} {CHIN_Y - 30:.0f} '
            f'{-FACE_RX:.0f} {FACE_CY - 40:.0f} Z" fill="{SKIN}" stroke="{INK}" '
            f'stroke-width="{LW:.1f}" stroke-linejoin="round"/>')
    # 鼻は小さく、目の直下に。長い鉤にすると顔の真ん中に釣り針が浮く
    nose = (f'<path d="M26 {NOSE_Y - 22:.0f} q26 20 0 32" fill="none" stroke="{INK}" '
            f'stroke-width="{LW * 0.72:.1f}" stroke-linecap="round"/>')
    cheek = (f'<ellipse cx="{-EYE_DX - 52:.0f}" cy="{EYE_Y + 68:.0f}" rx="30" ry="16" '
             f'fill="{SKIN_SH}" opacity="0.5"/>')
    g = (ear + skin + cheek
         + _eye(-EYE_DX, face, blink, look) + _eye(EYE_DX, face, blink, look)
         + _brow(-EYE_DX, face, 1) + _brow(EYE_DX, face, -1)
         + nose + _mouth(face, mouth) + _hair(hair))
    if abs(tilt) > 0.01:
        g = (f'<g transform="translate(0,{CHIN_Y:.0f}) rotate({tilt:.2f}) '
             f'translate(0,{-CHIN_Y:.0f})">{g}</g>')
    return g


# ── 体 ────────────────────────────────────────────────────

def _torso(costume):
    """胴。参考はTシャツで**肩が丸く、そこがそのまま半袖になっている**。
    胴はほとんど絞らない（初稿は台形にして寸胴に見えた）。"""
    top = SHIRT if costume != "coat" else COAT
    hem = WAIST_Y + (0 if costume != "coat" else 120)
    hw = WAIST_HW if costume != "coat" else WAIST_HW + 14
    d = (f"M{-SH_HW:.0f} {SLEEVE_Y:.0f} "
         f"C{-SH_HW - 6:.0f} {SHOULDER_Y + 24:.0f} {-SH_HW + 22:.0f} {SHOULDER_Y - 26:.0f} "
         f"{-72:.0f} {SHOULDER_Y - 40:.0f} "
         f"C{-24:.0f} {SHOULDER_Y - 50:.0f} {24:.0f} {SHOULDER_Y - 50:.0f} "
         f"{72:.0f} {SHOULDER_Y - 40:.0f} "
         f"C{SH_HW - 22:.0f} {SHOULDER_Y - 26:.0f} {SH_HW + 6:.0f} {SHOULDER_Y + 24:.0f} "
         f"{SH_HW:.0f} {SLEEVE_Y:.0f} "
         f"L{hw:.0f} {hem:.0f} "
         f"q0 26 -30 26 h{-hw * 2 + 60:.0f} q-30 0 -30 -26 Z")
    out = _sh(d, top)
    # 襟ぐり。首の付け根を隠す
    out += (f'<path d="M-70 {SHOULDER_Y - 40:.0f} q70 76 140 0" fill="none" '
            f'stroke="{INK}" stroke-width="{LW * 0.85:.1f}" stroke-linecap="round"/>')
    # 袖口の線。ここから下が素肌になる
    out += "".join(
        f'<path d="M{s * (SH_HW - 4):.0f} {SLEEVE_Y - 6:.0f} q{s * -34:.0f} 26 '
        f'{s * -74:.0f} 10" fill="none" stroke="{INK}" stroke-width="{LW * 0.8:.1f}" '
        f'stroke-linecap="round"/>' for s in (-1, 1))
    if costume == "coat":
        out += (f'<path d="M6 {SHOULDER_Y + 10:.0f} V{hem - 16:.0f}" fill="none" '
                f'stroke="{INK}" stroke-width="{LW * 0.55:.1f}" opacity="0.5"/>'
                f'<rect x="52" y="{hem - 150:.0f}" width="76" height="60" rx="6" '
                f'fill="none" stroke="{INK}" stroke-width="{LW * 0.55:.1f}" opacity="0.5"/>')
    else:
        out += (f'<path d="M{-SH_HW + 56:.0f} {SHOULDER_Y + 100:.0f} q30 26 10 52" '
                f'fill="none" stroke="{SHIRT_SH}" stroke-width="{LW * 0.7:.1f}" '
                f'stroke-linecap="round" opacity="0.85"/>')
    return out


def _legs(pose, step=0.0):
    """脚。step は歩幅（-1〜1）。立ちは0。"""
    # 脚の間隔は脚の太さ(112)に対して十分に開ける。初稿は±62で1本の塊に見えた
    a = step * 66
    back = [(-84, HIP_Y + 16), (-90 - a * 0.4, KNEE_Y), (-92 - a, ANKLE_Y - 26)]
    fore = [(84, HIP_Y + 16), (90 + a * 0.4, KNEE_Y), (92 + a, ANKLE_Y - 26)]
    return (_limb(back, LEG_W, PANTS_SH) + _shoe(back[-1][0], FOOT_Y, flip=True)
            + _limb(fore, LEG_W, PANTS) + _shoe(fore[-1][0], FOOT_Y))


def _arms(pose, costume, swing=0.0, raise_=0.0):
    """腕。**半袖なので肘から先は素肌**。初稿は全部シャツ色で描いて着ぐるみに見えた。"""
    col = SKIN if costume != "coat" else COAT
    sy = SLEEVE_Y - 10
    sx = SH_HW - 18
    if pose == "hips":
        back = [(-sx, sy), (-sx - 62, sy + 74), (-WAIST_HW + 10, sy + 120)]
        fore = [(sx, sy), (sx + 62, sy + 74), (WAIST_HW - 10, sy + 120)]
    elif pose == "point":
        back = [(-sx, sy), (-sx - 22, sy + 92), (-sx - 8, sy + 176)]
        fore = [(sx, sy), (sx + 104, sy - 60 - raise_ * 80),
                (sx + 208, sy - 96 - raise_ * 140)]
    elif pose == "hold":
        back = [(-sx, sy), (-sx - 22, sy + 92), (-sx - 8, sy + 176)]
        fore = [(sx, sy), (sx + 76, sy + 40), (sx + 46, sy - 66 - raise_ * 60)]
    else:
        s = swing * 44
        back = [(-sx, sy), (-sx - 26 + s * 0.4, sy + 116), (-sx - 12 + s, sy + 228)]
        fore = [(sx, sy), (sx + 26 - s * 0.4, sy + 116), (sx + 12 - s, sy + 228)]
    kind = "point" if pose == "point" else "fist"
    return (_limb(back, ARM_W, col) + _hand(*back[-1], 0)
            + _limb(fore, ARM_W, col)
            + _hand(fore[-1][0], fore[-1][1], -18 if kind == "point" else 0, kind))


class Part(str):
    anchors: dict


def character(pose="stand", face="normal", *, costume="shirt", hair="short",
              at=(0.0, 0.0), scale=1.0, flip=False,
              blink=0.0, mouth=0.0, look=0.0, tilt=0.0, breathe=0.0,
              swing=0.0, raise_=0.0, step=0.0, shadow=True):
    """キャラクター1体。

    breathe … 呼吸の上下（-1〜1）。上半身だけを僅かに上下させる
    blink   … 0=開 1=閉／mouth … 0=閉 1=開／look … 瞳の左右／tilt … 首の傾き（度）
    swing   … 腕の振り／raise_ … 指差し・持ち手の高さ／step … 歩幅
    """
    # 首は胴と頭の**裏**に置く。表に出すと襟の上に肌色の箱が乗って見える（初稿の失敗）
    neck = (f'<path d="M-52 {CHIN_Y - 40:.0f} h104 v{SHOULDER_Y - CHIN_Y + 90:.0f} h-104 Z" '
            f'fill="{SKIN_SH}" stroke="{INK}" stroke-width="{LW:.1f}" '
            f'stroke-linejoin="round"/>')
    body = []
    if shadow:
        body.append(f'<ellipse cy="6" rx="150" ry="26" fill="{INK}" opacity="0.16"/>')
    body.append(_legs(pose, step))
    up = [neck, _torso(costume), _arms(pose, costume, swing, raise_)]
    body.append(f'<g transform="translate(0,{-breathe * 9:.1f})">{"".join(up)}</g>')
    body.append(f'<g transform="translate(0,{-breathe * 13:.1f})">'
                f'{head(face, hair=hair, blink=blink, mouth=mouth, look=look, tilt=tilt)}</g>')
    tr = (f'translate({at[0]:.1f},{at[1]:.1f}) '
          f'scale({-scale if flip else scale:.4f},{scale:.4f})')
    out = Part(f'<g transform="{tr}">{"".join(body)}</g>')
    out.anchors = {"head": (at[0], at[1] + FACE_CY * scale),
                   "chin": (at[0], at[1] + CHIN_Y * scale)}
    return out


# ── 擬人化した臓器 ────────────────────────────────────────

KIDNEY = "#c0392b"
KIDNEY_SH = "#9c2c20"
KIDNEY_HI = "#d95b46"


def kidney_char(face="normal", *, at=(0.0, 0.0), scale=1.0, flip=False,
                blink=0.0, mouth=0.0, sweat=0, run=0.0, arms_up=0.0, tilt=0.0):
    """顔と手足のある腎臓。**EHL5様式の核心。** 臓器を解剖図でなく登場人物にする。

    run … 走っている脚の位相（0〜1）／arms_up … 万歳の度合い／sweat … 汗の数
    """
    lw = LW * 0.9
    # そら豆。腎門は右（flip で左）
    d = ("M0 -150 C44 -152 76 -128 84 -92 C90 -60 60 -32 42 -6 "
         "C38 0 38 0 42 6 C60 32 90 60 84 92 C76 128 44 152 0 150 "
         "C-64 148 -108 92 -110 8 C-112 -74 -64 -148 0 -150 Z")
    body = (f'<path d="{d}" fill="{KIDNEY}" stroke="{INK}" stroke-width="{lw:.1f}"/>'
            f'<path d="M-6 -136 C-58 -130 -96 -70 -98 6 C-99 40 -90 68 -76 90 '
            f'C-94 56 -96 -4 -80 -50 C-64 -96 -34 -122 -6 -136 Z" '
            f'fill="{KIDNEY_HI}" opacity="0.5"/>')
    ey = -34
    er = 30
    ry = er * (1.0 - blink)
    if ry < 4:
        eyes = "".join(f'<path d="M{cx - er} {ey} q{er} 12 {er * 2} 0" fill="none" '
                       f'stroke="{INK}" stroke-width="{lw:.1f}" stroke-linecap="round"/>'
                       for cx in (-44, 22))
    else:
        pr = 15 if face != "shock" else 19
        eyes = "".join(
            f'<ellipse cx="{cx}" cy="{ey}" rx="{er}" ry="{ry:.0f}" fill="{EYE_W}" '
            f'stroke="{INK}" stroke-width="{lw:.1f}"/>'
            f'<circle cx="{cx + 3}" cy="{ey + (4 if face in ("worry","tired") else 0)}" '
            f'r="{pr}" fill="{PUPIL}"/>'
            f'<circle cx="{cx - 2}" cy="{ey - 6}" r="{pr * 0.3:.0f}" fill="#fff" opacity="0.9"/>'
            for cx in (-44, 22))
    bd = {"normal": 0, "smile": -6, "worry": 18, "shock": -8, "tired": 12, "angry": 22}[face]
    brows = "".join(
        f'<g transform="translate({cx},{ey - er - 20}) rotate({bd * s})">'
        f'<path d="M-26 0 q26 -12 52 2" fill="none" stroke="{INK}" '
        f'stroke-width="{lw * 1.1:.1f}" stroke-linecap="round"/></g>'
        for cx, s in ((-44, 1), (22, -1)))
    my = 34
    if mouth > 0.1:
        h = 14 + 34 * mouth
        m = (f'<path d="M-30 {my} q30 -12 60 0 q-15 {h} -60 0 Z" fill="{MOUTH_IN}" '
             f'stroke="{INK}" stroke-width="{lw * 0.9:.1f}" stroke-linejoin="round"/>')
    elif face in ("angry", "shock"):     # 食いしばった歯
        m = (f'<path d="M-32 {my - 10} h64 v26 h-64 Z" fill="{EYE_W}" stroke="{INK}" '
             f'stroke-width="{lw * 0.9:.1f}" stroke-linejoin="round"/>'
             + "".join(f'<path d="M{-32 + i * 16} {my - 10} v26" stroke="{INK}" '
                       f'stroke-width="{lw * 0.5:.1f}"/>' for i in range(1, 4)))
    else:
        bow = {"normal": 10, "smile": 24, "worry": -12, "tired": -10}.get(face, 10)
        m = (f'<path d="M-28 {my} q28 {bow} 56 0" fill="none" stroke="{INK}" '
             f'stroke-width="{lw * 0.9:.1f}" stroke-linecap="round"/>')
    # 手足
    ah = -arms_up * 70
    arms = (_limb([(-96, 10), (-140, 30 + ah), (-168, 20 + ah * 1.4)], 26, KIDNEY)
            + f'<circle cx="-168" cy="{20 + ah * 1.4:.0f}" r="24" fill="{KIDNEY}" '
              f'stroke="{INK}" stroke-width="{lw:.1f}"/>'
            + _limb([(86, 10), (130, 30 + ah), (158, 20 + ah * 1.4)], 26, KIDNEY)
            + f'<circle cx="158" cy="{20 + ah * 1.4:.0f}" r="24" fill="{KIDNEY}" '
              f'stroke="{INK}" stroke-width="{lw:.1f}"/>')
    p = math.sin(run * math.tau) * 46
    legs = (_limb([(-46, 138), (-56 - p * 0.4, 196), (-58 - p, 250)], 28, KIDNEY_SH)
            + f'<ellipse cx="{-58 - p:.0f}" cy="258" rx="30" ry="18" fill="{KIDNEY_SH}" '
              f'stroke="{INK}" stroke-width="{lw:.1f}"/>'
            + _limb([(46, 138), (56 + p * 0.4, 196), (58 + p, 250)], 28, KIDNEY)
            + f'<ellipse cx="{58 + p:.0f}" cy="258" rx="30" ry="18" fill="{KIDNEY}" '
              f'stroke="{INK}" stroke-width="{lw:.1f}"/>')
    sw = "".join(
        f'<path d="M{sx} {sy} c-13 17 -13 30 0 30 c13 0 13 -13 0 -30 Z" fill="#7fc7e8" '
        f'stroke="{INK}" stroke-width="{lw * 0.7:.1f}"/>'
        for sx, sy in [(-140, -110), (110, -120), (-160, -40), (132, -50), (-120, -160)][:sweat])
    g = (f'<g transform="rotate({tilt:.1f})">{arms}{legs}{body}{eyes}{brows}{m}</g>{sw}')
    tr = (f'translate({at[0]:.1f},{at[1]:.1f}) '
          f'scale({-scale if flip else scale:.4f},{scale:.4f})')
    return f'<g transform="{tr}">{g}</g>'


# ── 背景を描くときの決まり ────────────────────────────────

def bg_ink(col, f=-0.34):
    """**背景の輪郭線は黒でなく「その色を暗くした色」にする。**

    参考フレームのソファを走査したところ暗線が1本も検出されなかった。
    前景だけが黒い太線を持つことで奥行きが出る。背景に黒を使うと画面が平らになる。
    """
    h = col.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, int(v * (1 + f))) for v in (r, g, b))
