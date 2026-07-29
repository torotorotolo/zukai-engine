# -*- coding: utf-8 -*-
"""解剖図の部品。「◯◯をやめるとどうなるのか」用。

■ 形は実物で確認してから描く（2026-07-28）
`ref/ref_digest.png`（Wikimedia Commons・PD）を見て、初稿の誤りを直した。

| 部位 | 初稿の誤り | 実際の形 |
|---|---|---|
| 肝臓 | 楕円 | **上辺が凸、下辺が右上がりのくさび**。左（患者の右）が厚く、右へ細く尖る |
| 胃 | 丸い塊 | **J字（バグパイプ）**。上の膨らみ＝穹窿部から下へ、大彎が下に大きく張る |
| 大腸 | 角ばった枠 | 上行→**下に垂れる横行**→下行→S状。角は丸い（肝彎曲・脾彎曲） |
| 小腸 | 平行な波線 | **とぐろを巻いた塊**。線が交差して密集する |

■ 画風は Vault `Resources/参考-アニメ様式-ClaudeCode日本史-20260728.md` に合わせる
和紙の地・低彩度・濃茶の輪郭線・フラット塗り＋影1段・中央スポットライト・四隅減光。
青いSF風ホログラムは目標様式と違うので使わない。
"""
import math
import re

# 和紙と低彩度の配色（目標様式に合わせる）
WASHI = "#efe3cc"
WASHI_LIT = "#faf3e4"
INK = "#4a3b2a"          # 濃茶の輪郭線
INK_SOFT = "#7d6a52"
BODY = "#e6d7bd"
LIVER = "#a8553f"
LIVER_HI = "#c9724f"
STOMACH = "#c08a76"
GUT = "#c9a077"
PANCREAS = "#c7a55c"

CX = 600  # 胴体の中心線

# (y, 半幅) 首→僧帽筋→肩→脇→胸→くびれ→骨盤→切り口
SILHOUETTE = [
    (0, 58), (56, 60), (86, 92), (116, 168), (150, 252), (188, 292),
    (232, 300), (300, 298), (368, 290), (430, 274), (492, 252),
    (548, 236), (600, 234), (656, 250), (716, 272), (782, 286), (852, 288),
]


def smooth(points):
    """点列を二次曲線でつなぐ。中点を通すので必ず滑らかになる。"""
    d = f"M{points[0][0]:.0f} {points[0][1]:.0f}"
    for i in range(1, len(points) - 1):
        x, y = points[i]
        nx, ny = points[i + 1]
        d += f" Q{x:.0f} {y:.0f} {(x + nx) / 2:.0f} {(y + ny) / 2:.0f}"
    d += f" L{points[-1][0]:.0f} {points[-1][1]:.0f}"
    return d


def torso_path():
    left = [(CX - hw, y) for y, hw in SILHOUETTE]
    right = [(CX + hw, y) for y, hw in reversed(SILHOUETTE)]
    return smooth(left) + " " + smooth(right)[1:].replace("M", "L", 1) + " Z"


def ribs(op=0.44):
    """肋骨。胸郭は下に向かって開くので、幅は下ほど広く・垂れを深く。"""
    out = [f'<path d="M{CX} 244 V500" stroke="{INK_SOFT}" stroke-width="3" opacity="{op}"/>']
    for i in range(6):
        y = 262 + i * 44
        hw = 214 + i * 8
        drop = 26 + i * 9
        out.append(f'<path d="M{CX - hw} {y} Q{CX} {y + drop} {CX + hw} {y}" fill="none" '
                   f'stroke="{INK_SOFT}" stroke-width="3" opacity="{op - i * 0.03:.2f}"/>')
    return "".join(out)


def liver(fill=None, hi=False):
    """肝臓。上辺が凸、下辺が右上がり。左（患者の右）が厚く右へ尖る。"""
    f = fill or LIVER
    # 左（患者の右）は厚く縦に長い。右へ行くほど薄くなり尖る。高さ:幅 ≒ 1:2.2
    d = ("M338 412 "
         "C332 356 380 330 444 328 "        # 左上：横隔膜のドーム
         "C524 336 614 356 680 386 "        # 上辺の凸が右へ下る
         "C714 402 718 424 700 436 "        # 右の尖端（左葉の先）
         "C648 468 578 494 502 510 "        # 下辺：右から左へ下る
         "C428 526 362 512 344 476 "
         "C334 448 336 430 338 412 Z")
    notch = ('<path d="M492 342 C486 392 494 434 512 466" fill="none" '
             f'stroke="{_dark(f)}" stroke-width="4.5" opacity="0.5"/>')
    gall = (f'<path d="M470 496 q28 -8 38 14 q10 24 -12 34 q-26 8 -33 -14 q-5 -24 7 -34 z" '
            f'fill="#7f8f4e" stroke="{INK}" stroke-width="3"/>')
    shade = ('<path d="M338 412 C334 364 382 340 444 338 C516 336 596 352 656 376 '
             'C556 386 430 412 372 486 C348 470 336 442 338 412 Z" '
             f'fill="{_light(f)}" opacity="0.40"/>')
    return (f'<g>{"" if not hi else ""}'
            f'<path d="{d}" fill="{f}" stroke="{INK}" stroke-width="4.5"/>'
            f'{shade}{notch}{gall}</g>')


def stomach():
    """胃。J字。左上が穹窿部、大彎が下に張り、幽門は左へ向く。"""
    # J字。左上＝穹窿部、右外側が大彎、下端から幽門が左へ向く
    d = ("M676 348 "
         "C742 316 812 348 820 420 "        # 穹窿部の大きな膨らみ
         "C828 494 802 552 748 566 "        # 大彎が下へ張る
         "C706 578 664 556 652 520 "        # 下端
         "C644 494 660 486 676 500 "        # 幽門へ細く絞る
         "C690 512 706 512 712 494 "        # 小彎（内側のくびれ）
         "C700 452 678 400 676 348 Z")
    fold = ('<path d="M712 386 C760 376 796 410 800 462" fill="none" '
            f'stroke="{_light(STOMACH)}" stroke-width="6" opacity="0.55"/>'
            '<path d="M690 500 C722 522 764 520 786 494" fill="none" '
            f'stroke="{_dark(STOMACH)}" stroke-width="4.5" opacity="0.4"/>')
    return (f'<path d="{d}" fill="{STOMACH}" stroke="{INK}" stroke-width="4"/>{fold}')


def colon():
    """大腸。上行→垂れる横行→下行→S状結腸。角は丸い。"""
    d = ("M424 750 V652 "
         "C424 622 442 610 466 608 "
         "C560 646 646 646 740 608 "
         "C764 610 782 622 782 652 "
         "V726 C782 756 766 768 740 768 "
         "H676 C648 768 638 782 634 802")
    return (f'<path d="{d}" fill="none" stroke="{GUT}" stroke-width="36" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3.2" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="0.5" '
            f'fill-opacity="0" style="stroke-dasharray:none"/>')


def small_intestine():
    """小腸。とぐろ。線を交差させて塊に見せる。"""
    loops = []
    s = 20260728
    for i in range(26):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        x = 486 + (s >> 9) % 196
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        y = 648 + (s >> 9) % 100
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        r = 24 + (s >> 10) % 16
        a = (s >> 4) % 360
        loops.append(f'<path d="M{x - r} {y} a{r} {r * 0.72:.0f} 0 1 1 {r * 2} 0" fill="none" '
                     f'stroke="{GUT}" stroke-width="21" stroke-linecap="round" '
                     f'transform="rotate({a} {x} {y})"/>')
    return "".join(loops)


def pancreas():
    # 胃の裏。左（患者の右）が頭部で厚く、右へ細く尾を引く
    return (f'<path d="M498 528 C540 508 620 512 700 528 C740 536 762 548 758 560 '
            f'C752 574 716 566 676 558 C606 546 540 552 506 566 '
            f'C482 574 476 538 498 528 Z" '
            f'fill="{PANCREAS}" stroke="{INK}" stroke-width="3" opacity="0.55"/>')


# ── 単体プロップ（原点中心・translate で好きな場所に置ける） ────────────
# 上の臓器は胴体の絶対座標に埋まっているが、以下は場面に単体で浮かせる用。
# 「臓器を光らせて宙に浮かべ、キャラが指差す」は参考動画の逃げ方の2番目に多い型
# （Vault `Resources/参考-HSS秒単位分解-20260728.md` の分類2・約20カット）。

KIDNEY = "#a34a3c"
KIDNEY_HI = "#c56b4f"
BRAIN = "#d9a3a8"
BRAIN_HI = "#eec3c4"


def kidney(fill=None, flip=False, ureter=True, vessels=True):
    """腎臓1個。原点＝臓器の中心。素の大きさは 幅約220 × 高さ約340。

    根拠 = `ref/ref_kidney.png`（Gray1120・Wikimedia Commons・PD）。

    | 記憶で描くとこうなる | 実物 |
    |---|---|
    | 丸い、または横長のそら豆 | **縦長**。高さ:幅 ≒ 1.6:1 |
    | 両側がくびれる | くぼみ（腎門）は**内側の1か所だけ**。外側は一様に凸 |
    | 血管が外側から刺さる | 動脈・静脈・尿管は**全部くぼみから出る**。尿管は下へ降りる |
    | 上下が同じ | 上端に副腎が帽子のように乗る（本図では省略可） |

    既定は腎門が右向き（＝体の左側にある腎臓の見え方）。flip=True で左向き。
    """
    f = fill or KIDNEY
    # 時計回り。上端 → 上外側の張り出し → 腎門のくぼみ → 下外側 → 下端 → 外側の凸
    d = ("M0 -170 "
         "C44 -172 76 -150 84 -112 "     # 上極。右へ丸く張り出す
         "C90 -76 62 -40 44 -8 "          # 腎門へ向かって内側へ絞る
         "C40 0 40 0 44 8 "               # くぼみの底（ここに血管が入る）
         "C62 40 90 76 84 112 "           # 再び外へ膨らみながら下極へ
         "C76 150 44 172 0 170 "          # 下極
         "C-64 168 -110 108 -112 12 "     # 外側は一様な凸。くびれを作らない
         "C-114 -84 -66 -168 0 -170 Z")
    # 皮質と髄質の境（Gray1128 の boundary zone）。内側に沿う1本で十分
    inner = (f'<path d="M12 -118 C-48 -104 -70 -40 -70 8 C-70 62 -46 108 8 122" '
             f'fill="none" stroke="{_dark(f)}" stroke-width="5" opacity="0.42"/>')
    hi = (f'<path d="M-4 -158 C-58 -152 -98 -84 -100 6 C-101 44 -92 76 -76 100 '
          f'C-96 62 -98 -6 -80 -56 C-62 -108 -32 -142 -4 -158 Z" '
          f'fill="{_light(f)}" opacity="0.45"/>')
    v = ""
    if vessels:
        # 動脈(赤)は上、静脈(青)は下。実物は静脈が手前＝太く見える
        v = (f'<path d="M44 -14 h74" stroke="#b8483c" stroke-width="17" '
             f'stroke-linecap="round"/>'
             f'<path d="M44 16 h86" stroke="#5c7fa8" stroke-width="21" '
             f'stroke-linecap="round"/>')
    u = ""
    if ureter:
        # 尿管は腎門から下へ。まっすぐでなく体の中心へ寄りながら降りる。
        # 細く長くすると、宙に浮かせたとき2本の「脚」に見えるので、太く短くする
        u = (f'<path d="M46 34 C58 84 62 128 54 166" fill="none" stroke="#e5dcc6" '
             f'stroke-width="21" stroke-linecap="round"/>'
             f'<path d="M46 34 C58 84 62 128 54 166" fill="none" stroke="{INK}" '
             f'stroke-width="21" stroke-linecap="round" opacity="0.2"/>')
    g = (f'{u}{v}<path d="{d}" fill="{f}" stroke="{INK}" stroke-width="6"/>{hi}{inner}')
    return f'<g transform="scale(-1,1)">{g}</g>' if flip else f'<g>{g}</g>'


# 脳回（隆起そのもの）の芯線と太さ。**溝を線で描いてはいけない。**
# 溝を細線で引くと「塗った縞」になる（初稿の失敗2回目）。実物の脳回は太いソーセージで、
# 縁が丸く盛り上がり、その谷間が影になる。だから **管を重ねて描き、谷は隙間として出す**。
#
# 根拠 = `ref/ref_brain_sobotta.png`（Sobotta 1909 Plate 626・PD。脳溝脳回に名前が振ってある
# 実物写生）。向きは家族ごとに決まっていて、乱数で撒くと必ず嘘になる：
#   前頭 … 前後方向にほぼ水平（上前頭回・中前頭回・下前頭回）
#   中心 … **上後方から前下方へ斜めに降り、外側溝へ集まる**（中心前回・中心回・中心後回）。脳の顔
#   頭頂 … 中心後回の後ろから後方へ（縁上回・角回）
#   後頭 … 短く不規則
#   側頭 … 外側溝と平行に前後方向（上・中・下側頭回）
#
# 描き順＝奥（側頭・後頭）から手前（前頭）へ。1本ずつ「濃い縁→中身」の順で置くと、
# 後から置いた管の縁が前の管の上に乗り、境目が谷になる。
# 端は必ず輪郭の外か外側溝まで伸ばす。中途半端に止めると丸い管の先端が面の真ん中に
# 浮いて「棒を並べた」ように見える（初稿の失敗3回目）。はみ出しは clipPath が切る。
# 外側溝の芯線。輪郭・クリップ・溝の線の3つでこれを共有する
_SYLVIAN = "M-190 22 C-140 46 -60 52 16 34 C58 24 86 6 100 -14"
# 外側溝より後ろでは、頭頂・後頭が溝の高さより下まで続く（Sobotta図版）
_SYLVIAN_TAIL = "C128 10 158 40 188 92"

# 太さは必ずばらす。全部同じ幅にすると、等間隔の棒を並べた「バーコード」に見える。
# 芯線も直線に近づけない。実物の脳回は必ずどこかで曲がる。
#
# さらに Sobotta 図版を部分拡大して分かったこと（2026-07-28・3回目の作り直し）：
#   ・脳回は「長い平行な管」ではない。**短くいびつな塊が枝分かれしながら密に詰まっている**
#   ・だから本数を増やし、短い枝（b付き）を主幹の脇に生やす
#   ・溝は細く深い。管の縁取りを細めにして、溝の本数で密度を出す
#
# 溝（谷）の網。**脳回を1本ずつ管として描くのはやめた。**
# 管は縁を全周に付けるので、短い枝が「面の上に転がったマカロニ」に見える（3回目の失敗）。
# 実物の脳回は互いに壁を共有していて、独立した部品ではない。
#   → 溝のほうを **枝分かれしてつながる網** として引き、脳回は残った面として出す。
#   → 平坦に見えないよう、溝1本ごとに「広い薄影 → 深い谷 → 谷の上の稜線ハイライト」の3層で描く。
# 幅もばらす。同じ幅で平行に引くとバーコードになる（2回目の失敗）。
def _bez(p, t):
    """3次ベジエ上の点。p = (P0, C1, C2, P3)。"""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1.0 - t
    a, b, c, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
    return (a * x0 + b * x1 + c * x2 + d * x3, a * y0 + b * y1 + c * y2 + d * y3)


def _family(base, normal, n, spread, wlo, whi, seed, jitter=9.0, links=2, trim=0.24):
    """1つの territory を、流れに沿った溝の族で埋める。

    実物の皮質に平坦な面は無い。手で十数本並べても必ず隙間が残るので、
    **基準の芯線を法線方向へ n 本ずらして敷き、隣どうしを短い枝でつなぐ**。
    これで「向きの揃った密な網」になり、かつ枝分かれして見える。
    """
    nx, ny = normal
    L = math.hypot(nx, ny) or 1.0
    nx, ny = nx / L, ny / L
    s = seed * 2654435761 + 1

    def rnd(a, b):
        nonlocal s
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        return a + (b - a) * ((s >> 9) % 10000) / 10000.0

    curves, out = [], []
    for i in range(n):
        # 等間隔に並べない。間隔まで揃うと縞模様に見える
        k = (i / (n - 1.0) - 0.5) * 2.0 if n > 1 else 0.0   # -1..+1
        off = k * spread + rnd(-spread * 0.10, spread * 0.10)
        pts = []
        for j, (px, py) in enumerate(base):
            j0 = rnd(-jitter, jitter)
            pts.append((px + nx * off + j0, py + ny * off + j0 * 0.6))
        # 長さもばらす。全部が端から端まで走ると平行線の束になる。
        # P0 を P1 側へ、P3 を P2 側へ寄せて縮める。
        # ただし **端を境界（外側溝や後頭極）に届かせたい族では trim を小さくする**。
        # 既定のままだと中心系が外側溝の手前で止まり、そこに平坦な帯が残った（6回目の失敗）
        a, b = rnd(0.0, trim), rnd(0.0, trim)
        p0 = (pts[0][0] + (pts[1][0] - pts[0][0]) * a, pts[0][1] + (pts[1][1] - pts[0][1]) * a)
        p3 = (pts[3][0] + (pts[2][0] - pts[3][0]) * b, pts[3][1] + (pts[2][1] - pts[3][1]) * b)
        pts = [p0, pts[1], pts[2], p3]
        curves.append(pts)
        d = (f"M{pts[0][0]:.1f} {pts[0][1]:.1f} C{pts[1][0]:.1f} {pts[1][1]:.1f} "
             f"{pts[2][0]:.1f} {pts[2][1]:.1f} {pts[3][0]:.1f} {pts[3][1]:.1f}")
        out.append((d, rnd(wlo, whi)))
    # 隣の溝どうしを短い枝でつなぐ。これが無いと平行線の集合にしか見えない
    for i in range(len(curves) - 1):
        for _ in range(links):
            t = rnd(0.18, 0.82)
            ax, ay = _bez(curves[i], t)
            bx, by = _bez(curves[i + 1], t + rnd(-0.10, 0.10))
            mx, my = (ax + bx) / 2 + rnd(-7, 7), (ay + by) / 2 + rnd(-7, 7)
            out.append((f"M{ax:.1f} {ay:.1f} Q{mx:.1f} {my:.1f} {bx:.1f} {by:.1f}",
                        rnd(wlo * 0.55, wlo * 0.85)))
    return out


# territory ごとの流れ。(基準の芯線, 法線, 本数, 広がり, 幅の下限, 幅の上限, 種)
# 向きの根拠は Sobotta 1909 Plate 626：
#   前頭=前後にほぼ水平／中心=上後方から前下方へ斜め／頭頂後頭=後方へ放射／側頭=外側溝と平行
#
# ★基準線は territory の**真ん中**を通し、広がりは territory の実寸から決めること。
#   端を通すと族が片側に寄り、外側溝の上や後頭の下に大きな平坦面が残る（3回目の失敗）。
#   下端は必ず外側溝まで届かせる。
_SULCI_LOWER = _family(
    ((-180, 70), (-108, 100), (-8, 96), (140, 46)), (0, 1), 6, 40, 9, 13, 11,
    links=2, trim=0.07)

# 外側溝の上は3つの縄張りに分かれる。**族ごとにクリップすること。**
# 分けないと、前頭（水平）と中心（垂直）が同じ場所で直交してカゴ編みになる（4回目の失敗）。
# 実物では隣の縄張りの溝は境界で突き当たって終わり、交差しない。
_TERRITORY = [
    # 前頭：中心前溝より前。上段の族と、外側溝のすぐ上を埋める下前頭の帯の2本立て。
    # 上段だけだと外側溝との間に平坦な帯が残る（5回目の失敗）
    ("M-36 -190 C-56 -130 -94 -70 -132 48 L-260 60 L-260 -260 L-36 -260 Z",
     _family(((-206, -48), (-166, -76), (-114, -96), (-54, -96)),
             (0.28, -0.96), 6, 62, 9, 14, 3, jitter=11) +
     _family(((-198, 12), (-152, -8), (-102, -20), (-58, -18)),
             (0.2, -0.98), 3, 26, 8, 12, 23, jitter=8, links=1)),
    # 中心：中心前溝と中心後溝のあいだ。下端は外側溝まで降ろす（trim を小さく）
    ("M-36 -190 C-56 -130 -94 -70 -132 48 L8 60 C26 -66 46 -124 60 -180 Z",
     _family(((-16, -178), (-38, -116), (-60, -56), (-70, 56)),
             (1, 0.15), 7, 66, 9, 15, 7, trim=0.06)),
    # 頭頂・後頭：中心後溝より後ろ。後頭極まで埋める（trim を小さく）
    ("M60 -180 C46 -124 26 -66 8 40 L260 60 L260 -260 L60 -260 Z",
     _family(((14, -98), (74, -78), (132, -48), (192, 4)),
             (0.38, -0.93), 8, 82, 9, 14, 5, trim=0.07)),
]


_BRAIN_N = 0     # clipPath の id を一意にするための連番


def _perp(d):
    """パスの向きに直交する単位ベクトルのうち、左上（＝光源側）を向くほうを返す。

    溝ごとに手で「明るい側」を指定すると必ず取り違えるので、経路から機械的に決める。
    """
    n = [float(v) for v in re.findall(r"-?\d+\.?\d*", d)]
    x0, y0, x1, y1 = n[0], n[1], n[-2], n[-1]
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    px, py = -dy / L, dx / L
    if px * -0.45 + py * -1.0 < 0:      # 左上向きでなければ反転
        px, py = -px, -py
    return px, py


def _sulci(f, group):
    """溝の網を引く。1本につき4層＝広い薄影／稜線ハイライト／反対側の影／深い谷。

    **オフセット量は溝の幅から計算すること。** 稜線ハイライトを溝の幅より内側に置くと、
    あとから描く谷の線に完全に覆われて消える（初稿はこれで真っ黒な棒になった）。
    ずらす向きは `_perp()` が経路から機械的に決める。
    """
    shade, floor = _dark(f, -0.30), _dark(f, -0.60)
    crest, dip = _light(f, 0.55), _dark(f, -0.34)
    out = []
    for d, w in group:      # 1周目：溝が落ち込んでいる範囲の広い薄影
        # 密に並べると薄影どうしが重なって全体が濁る。溝が増えたぶん幅と濃さは抑える
        out.append(f'<path d="{d}" fill="none" stroke="{shade}" stroke-width="{w * 2.1:.0f}" '
                   f'stroke-linecap="round" stroke-linejoin="round" opacity="0.12"/>')
    for d, w in group:      # 2周目：谷の両脇（明るい稜線と、反対側の落ち込み）
        px, py = _perp(d)
        o = w * 0.95
        out.append(f'<g transform="translate({px * o:.1f},{py * o:.1f})">'
                   f'<path d="{d}" fill="none" stroke="{crest}" stroke-width="{w * 0.8:.0f}" '
                   f'stroke-linecap="round" opacity="0.6"/></g>')
        out.append(f'<g transform="translate({-px * o:.1f},{-py * o:.1f})">'
                   f'<path d="{d}" fill="none" stroke="{dip}" stroke-width="{w * 0.7:.0f}" '
                   f'stroke-linecap="round" opacity="0.28"/></g>')
    for d, w in group:      # 3周目：谷そのもの
        out.append(f'<path d="{d}" fill="none" stroke="{floor}" stroke-width="{w}" '
                   f'stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>')
    return "".join(out)


# 輪郭の通過点（時計回り・前頭極から）。**滑らかな卵にしないこと。**
# Sobotta 図版では脳回ひとつひとつが縁で盛り上がり、輪郭が波打っている。
_BRAIN_RIM = [
    (-204, -6), (-200, -40), (-188, -74), (-166, -104), (-138, -128), (-104, -144),
    (-66, -154), (-26, -160), (14, -160), (54, -152), (92, -138), (126, -118),
    (152, -94), (174, -64), (188, -30), (192, 6), (184, 40), (168, 68), (144, 88),
    (114, 98), (76, 112), (34, 122), (-10, 126), (-52, 124), (-90, 116), (-122, 104),
    (-146, 86), (-158, 60), (-166, 38), (-182, 28), (-196, 16),
]


def _scallop(pts, bulge=8.0, cx=-12.0, cy=-16.0):
    """点列を、外へ膨らむ小さな弧でつないで波打つ輪郭にする。膨らみの向きは重心から外向き。"""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        vx, vy = mx - cx, my - cy
        L = math.hypot(vx, vy) or 1.0
        d += (f" Q{mx + vx / L * bulge:.1f} {my + vy / L * bulge:.1f} "
              f"{x1:.1f} {y1:.1f}")
    return d + " Z"


def brain(fill=None, glow=False):
    """脳（左を向いた側面図）。原点＝大脳の中心。素の大きさは 幅約400 × 高さ約290。

    根拠 = `ref/ref_brain_sobotta.png`（Sobotta 1909 Plate 626・PD。**脳溝に名前が振ってある
    実物写生**なので、しわの向きまでこれで決めた）と `ref/ref_brain.png`（Gray728・葉の境界）。

    | 記憶で描くとこうなる | 実物 |
    |---|---|
    | 縦長の卵、または雲のような丸の集合 | **横長**。幅:高さ ≒ 1.45:1 |
    | 側頭葉を別の塊として下に置く | **側頭葉は同じ輪郭の一部**。外側溝という切れ込みで分かれて見えるだけ |
    | 外側溝が全幅にわたる笑った弧 | **前下から入って後上へ浅く昇る裂け目**。後端は少し上に跳ねて終わる |
    | 側頭極が前頭極と同じくらい前に出る | **側頭極は前頭極よりかなり奥**（全幅の2割ほど内側）に引っ込む |
    | 前頭葉が一番高い | 一番高いのは**中央より少し後ろ**。前頭極はむしろ低く前へ突き出す |
    | しわが均一な弧の集合 | 向きの決まった家族に分かれる（`_SULCI` 参照）。太い隆起と深い谷 |

    初稿の失敗2つ：①側頭葉を独立した楕円で描いて脳の下にソーセージが浮いた
    ②しわを乱数で撒いてパンの表面になった。どちらも実物を見ずに描いたのが原因。
    """
    f = fill or BRAIN
    # 大脳＋側頭葉を一筆で。前頭極(左)→頭頂→後頭(右)→側頭葉の下辺→側頭極→前頭極。
    # 通過点は _BRAIN_RIM。滑らかにつながず、脳回ぶんの波を付ける
    outline = _scallop(_BRAIN_RIM)
    # 外側溝（シルビウス裂）。前下から入り、後上へ浅く昇って、後端で少し跳ねる
    sylvian = (f'<path d="{_SYLVIAN}" fill="none" stroke="{INK}" stroke-width="9" '
               f'stroke-linecap="round"/>'
               f'<path d="M-172 34 C-124 56 -50 62 22 44 C58 34 82 18 96 2" fill="none" '
               f'stroke="{_light(f, 0.5)}" stroke-width="5" stroke-linecap="round" '
               f'opacity="0.5"/>')
    # 小脳。後頭極の下に食い込む。細い平行線（小脳回）で質感を出す
    cere = ("M136 60 C186 56 216 84 214 116 C212 150 176 166 138 160 "
            "C104 154 86 128 90 100 C94 76 114 62 136 60 Z")
    lines = "".join(
        f'<path d="M{104 + i * 14} {62 + i * 5} q16 44 2 80" fill="none" '
        f'stroke="{_dark(f, -0.36)}" stroke-width="3.5" opacity="0.45"/>' for i in range(8))
    # しわと小脳の筋は、必ず輪郭で切り落とす。切らないと外へはみ出して毛のように見える
    global _BRAIN_N
    _BRAIN_N += 1
    cid, kid = f"brnC{_BRAIN_N}", f"brnK{_BRAIN_N}"
    uid, lid = f"brnU{_BRAIN_N}", f"brnL{_BRAIN_N}"
    # 外側溝を境に、上（前頭・中心・頭頂・後頭）と下（側頭）の縄張りを分ける。
    # 分けないと中心系の管が溝を越え、丸い先端が側頭葉に3つ並んで浮く
    div = _SYLVIAN + " " + _SYLVIAN_TAIL
    clips = (f'<clipPath id="{cid}"><path d="{outline}"/></clipPath>'
             f'<clipPath id="{kid}"><path d="{cere}"/></clipPath>'
             f'<clipPath id="{uid}"><path d="{div} L260 -260 L-260 -260 L-260 22 Z"/></clipPath>'
             f'<clipPath id="{lid}"><path d="{div} L260 260 L-260 260 L-260 22 Z"/></clipPath>')
    upper = []
    for i, (terr, fam) in enumerate(_TERRITORY):
        tid = f"brnT{_BRAIN_N}_{i}"
        clips += f'<clipPath id="{tid}"><path d="{terr}"/></clipPath>'
        upper.append(f'<g clip-path="url(#{tid})">{_sulci(f, fam)}</g>')
    # 脳幹。小脳の前から下へ。まっすぐ下ろさず前に傾ける
    stem = (f'<path d="M66 92 C74 140 66 178 48 200 C26 224 -2 214 0 190 '
            f'C4 156 24 132 22 88 Z" fill="{_dark(f, -0.16)}" '
            f'stroke="{INK}" stroke-width="6"/>')
    # 立体感はベタ塗りのパッチでなく、上からの光と下の落ち影で出す。
    # 初稿は明るい塊を1枚貼っていて、輪郭のはっきりしたシミに見えた
    gid = f"brnG{_BRAIN_N}"
    grad = (f'<linearGradient id="{gid}" x1="0.15" y1="0" x2="0.6" y2="1">'
            f'<stop offset="0%" stop-color="{_light(f, 0.5)}" stop-opacity="0.55"/>'
            f'<stop offset="45%" stop-color="{f}" stop-opacity="0"/>'
            f'<stop offset="100%" stop-color="{_dark(f, -0.5)}" stop-opacity="0.35"/>'
            f'</linearGradient>')
    body = (f'{clips}{grad}{stem}'
            f'<path d="{cere}" fill="{_dark(f, -0.12)}" stroke="{INK}" stroke-width="6"/>'
            f'<g clip-path="url(#{kid})">{lines}</g>'
            # 下地は脳回と同色にする。暗くすると管の隙間が「穴」に見える（初稿の失敗4回目）。
            # 溝は管の輪郭線だけで表し、立体感はこの上に重ねる光と影の勾配で出す
            f'<path d="{outline}" fill="{f}" stroke="{INK}" stroke-width="7"/>'
            f'<g clip-path="url(#{cid})">'
            f'<g clip-path="url(#{lid})">{_sulci(f, _SULCI_LOWER)}</g>'
            f'<g clip-path="url(#{uid})">{"".join(upper)}</g>'
            f'{sylvian}<path d="{outline}" fill="url(#{gid})"/></g>'
            f'<path d="{outline}" fill="none" stroke="{INK}" stroke-width="7"/>')
    return f'<g filter="url(#glow)">{body}</g>' if glow else f'<g>{body}</g>'


def _dark(c, f=-0.32):
    h = c.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, int(v * (1 + f))) for v in (r, g, b))


def _light(c, f=0.36):
    h = c.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * f) for v in (r, g, b))


def defs():
    """和紙の地・粒子・周辺減光・落ち影。目標様式の4点セット。"""
    return f'''
  <radialGradient id="paper" cx="50%" cy="42%" r="70%">
    <stop offset="0%" stop-color="{WASHI_LIT}"/>
    <stop offset="62%" stop-color="{WASHI}"/>
    <stop offset="100%" stop-color="#d8c8ac"/></radialGradient>
  <filter id="fiber" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.62 0.04" numOctaves="4" seed="7"/>
    <feColorMatrix type="saturate" values="0"/></filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" seed="3"/>
    <feColorMatrix type="saturate" values="0"/></filter>
  <radialGradient id="vig" cx="50%" cy="42%" r="70%">
    <stop offset="46%" stop-color="#3a2c18" stop-opacity="0"/>
    <stop offset="100%" stop-color="#3a2c18" stop-opacity="0.40"/></radialGradient>
  <filter id="soft" x="-25%" y="-25%" width="150%" height="150%">
    <feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#4a3b2a" flood-opacity="0.28"/></filter>
  <filter id="glow" x="-45%" y="-45%" width="190%" height="190%">
    <feGaussianBlur stdDeviation="17" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''


def background(w, h):
    return (f'<rect width="{w}" height="{h}" fill="url(#paper)"/>'
            f'<rect width="{w}" height="{h}" filter="url(#fiber)" opacity="0.10"/>')


def overlay(w, h):
    return (f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity="0.07"/>'
            f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
