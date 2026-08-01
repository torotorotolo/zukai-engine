# -*- coding: utf-8 -*-
"""潜水艇タイタン。**この1モデルで約35カットを撮る。**

■ 形の出どころ
  NTSB / USCG の公開報告に出てくる**寸法（数値）だけ**から組み立てている。
  数値そのものは事実なので著作権が及ばない。
  ⚠️ ドケットの図版をトレースしないこと。ドケットの大半は当事者提出資料で、
     連邦職員の職務著作ではない＝パブリックドメインではない（権利レビューの指摘）。

■ 寸法（台本の facts と一致させること）
  全長           22 ft   = 6.71 m
  耐圧殻 内径    56 in   = 1.42 m
  耐圧殻 板厚     5 in   = 0.127 m  → 外半径 0.837 m
  耐圧殻 長さ    96 in   = 2.44 m
  のぞき窓 径    15 in   = 0.38 m
  ドームのボルト  18本（c205）
  炭素繊維の層    5層（1インチ×5 ＝ 5インチ）

■ 作りの方針（参照chの実測に合わせる）
  - 主役はフラット。テクスチャを貼らない（拡大しても粒子が見えないのが参照chの絵）
  - 金属は metal を上げすぎない。映り込む環境が無いと**真っ黒に落ちる**（1巡目の失敗）
  - Boolean を使わない。bmesh で切る（Boolean はワールド空間評価なので、
    あとから動かすと胴体だけ動いて口が開く）
  - 全部を root の Empty にぶら下げる。root を動かせば全部が一緒に動く

■ 1巡目（2026-08-01）で潰した欠陥
  1 円錐が逆向き（radius1 は −Z 側。Y軸へ回すと +Y 側に来る）→ L.taper() に集約
  2 受け台が本体から外れて浮く → 位置を胴体半径から算出
  3 層が1枚も見えない → **入れ子の筒は外から見えない。切って断面を出す**
  4 剥離の朱赤が出ない → 同上
  5 断面が切れない → 法線をローカル空間へ変換していなかった → L.cut()
  6 チタンが真っ黒 → metal を 1.0 から 0.35 へ
  7 ハイライトが白飛び → 光を面光源にして弱める
  8 太短い → 望遠寄りで見る（参照chも望遠で平たく見せている）
  9 黒いドームが小さい → 参照chで最も目を引く要素。大きく取る
"""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lib as L                                                    # noqa: E402

# ── 寸法（メートル）──────────────────────────────────────────
LOA = 6.71            # 全長
R_IN = 0.710          # 耐圧殻 内半径
WALL = 0.127          # 板厚（5インチ）
R_OUT = R_IN + WALL   # 0.837
CYL_LEN = 2.44        # 円筒部の長さ
VIEWPORT_R = 0.190    # のぞき窓の半径（径380mm）
N_LAYERS = 5          # 炭素繊維の層数
N_BOLTS = 18          # ドームを留めるボルト（c205）

R_FAIR = 0.98         # 外装の半径
DOME_R = 0.62         # 前面の黒いドーム半径（参照chで最も目を引く要素）

# ── 色（2D図解と揃える。参照chに合わせてフラット寄り）──────────
C_WHITE = "#dde3e7"
C_CARBON = "#39424b"
C_CARBON2 = "#4d5862"   # 層を1枚おきに変えて「5枚ある」ことを読ませる
C_TITAN = "#8f99a2"
C_DOME = "#111a21"
C_FRAME = "#39414a"


def _mats():
    return dict(
        white=L.material("m_white", C_WHITE, rough=0.55, metal=0.0),
        carbon=L.material("m_carbon", C_CARBON, rough=0.62, metal=0.0),
        carbon2=L.material("m_carbon2", C_CARBON2, rough=0.62, metal=0.0),
        # 🔴 metal=1.0 にすると、映り込む環境が無い深海では真っ黒になる（1巡目の失敗）
        titan=L.material("m_titan", C_TITAN, rough=0.42, metal=0.35),
        dome=L.material("m_dome", C_DOME, rough=0.22, metal=0.0),
        frame=L.material("m_frame", C_FRAME, rough=0.65, metal=0.20),
        alert=L.material("m_alert", L.ALERT, rough=0.50, metal=0.0),
        # 接着面（c416「接着剤の面が4つできる」）。層より明るくして境目を読ませる
        glue=L.material("m_glue", "#cdd6dc", rough=0.45, metal=0.0),
        # 断面の切り口。内側が真っ黒に沈まないよう、地の色を少し明るく
        inner=L.material("m_inner", "#8a949d", rough=0.75, metal=0.0),
        # 人。顔も指も作らない（参照chも顔なしマネキン）
        figure=L.material("m_figure", "#161c23", rough=0.80, metal=0.0),
    )


# ── 耐圧殻 ──────────────────────────────────────────────────────
def carbon_layers(m, n=N_LAYERS, highlight=(), length=CYL_LEN):
    """炭素繊維の層を n 枚の同心の筒として作る。

    🔴 層の表現は「変形」ではなく「板を重ねる」。
       設計レビューで、頂点を一様に縮める実装では layers=[2,3] の指定が
       絵に出ない（＝企画の中核カットが成立しない）と指摘された点。

    🔴 そして**入れ子の筒は外からは1枚しか見えない**（1巡目の失敗）。
       このカットは必ず L.cut() で切って、断面の帯として見せること。

    highlight … 剥離した層の番号（1始まり）。朱赤にして外へ逃がす。
    """
    step = (R_OUT - R_IN) / n
    out = []
    for i in range(n):
        idx = i + 1
        r = R_IN + step * (i + 0.5)
        gap = 0.020 if idx in highlight else 0.0      # 剥離＝板がずれて浮く
        c = L.cylinder(f"cf_layer_{idx}", r + gap, length, verts=128)
        s = c.modifiers.new("thick", "SOLIDIFY")
        s.thickness = step * 0.80
        s.offset = 0
        mat = m["alert"] if idx in highlight else (m["carbon"] if i % 2 == 0
                                                   else m["carbon2"])
        L.assign(c, mat)
        out.append(c)
    return out


def wall_sample(m, highlight=(), n=N_LAYERS, arc_deg=70.0, length=1.6,
                r_in=2.20, wall=0.75, adhesive=True):
    """🔴 炭素繊維の壁を「切り出して大きく見せる」模式図。

    ■ なぜ実寸で作ってはいけないか（2巡目の失敗）
      耐圧殻は直径1,674mmに対して壁が127mm＝**直径の7.6%**しかない。
      5層に割ると1層1.5%。1920pxで焼いても数ピクセルにしかならず、
      どんなカメラワークでも層は読めない。
      → 壁の一部だけを取り出し、比率を誇張して見せるのが正しい。
        正確な寸法は2D側のテロップが持つ（b3d/README.md 絶対ルール5）。

    ■ 何を見せるか
      ・層が5枚あること（c414「5回で厚さ5インチ」）
      ・層と層のあいだに接着面が4つできること（c416）
      ・剥離した層が浮くこと（c308 / c428 / c625）
    """
    # 🔴 切らない。solid_arc で「欲しい帯だけ」を中実に作る（5巡目の方針転換）。
    #    切って穴を塞ぐやり方は、ゴミ面が出るうえ実寸だと細すぎて読めなかった。
    a0 = 90.0 - arc_deg / 2.0
    a1 = 90.0 + arc_deg / 2.0

    t_layer = wall * 0.155 / 0.175      # 層の厚み
    t_glue = wall * 0.020 / 0.175       # 接着面の厚み
    unit = t_layer + t_glue

    out = []
    r = r_in
    for i in range(n):
        idx = i + 1
        # 剥離した層は、そこから外側をまとめて外へ逃がす（板がずれて浮く）
        lift = 0.13 if (highlight and idx >= min(highlight)) else 0.0
        mat = m["alert"] if idx in highlight else (m["carbon"] if i % 2 == 0
                                                   else m["carbon2"])
        out.append(L.assign(
            L.solid_arc(f"wall_{idx}", r + lift, r + lift + t_layer, length,
                        a0, a1), mat))
        r += t_layer
        # 接着面（層と層のあいだ。5層なら4面）— c416「接着剤の面が4つできる」
        if adhesive and i < n - 1:
            out.append(L.assign(
                L.solid_arc(f"glue_{idx}", r + lift, r + lift + t_glue, length,
                            a0, a1), m["glue"]))
            r += t_glue
    return out


def dome_bolts(m, y, r, n=N_BOLTS):
    """ドームを留めるボルト18本（c205「ドームは18本のボルトで」）。"""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        b = L.cylinder(f"bolt_{i}", 0.028, 0.075,
                       loc=(r * math.cos(a), y, r * math.sin(a)), verts=12)
        out.append(L.assign(b, m["titan"]))
    return out


def pressure_hull(m, layers=True, highlight=(), bolts=True):
    """耐圧殻：炭素繊維の円筒＋前後のチタン半球ドーム＋継ぎ目リング＋のぞき窓。"""
    parts = []
    half = CYL_LEN / 2

    if layers:
        parts += carbon_layers(m, highlight=highlight)
    else:
        c = L.cylinder("cf_shell", (R_IN + R_OUT) / 2, CYL_LEN, verts=128)
        s = c.modifiers.new("thick", "SOLIDIFY")
        s.thickness = WALL
        parts.append(L.assign(c, m["carbon"]))

    # 前後のチタン半球ドーム
    for name, y, facing in (("dome_fore", half, (0, 1, 0)),
                            ("dome_aft", -half, (0, -1, 0))):
        d = L.hemisphere(name, R_OUT, loc=(0, y, 0), facing=facing)
        s = d.modifiers.new("thick", "SOLIDIFY")
        s.thickness = 0.055
        parts.append(L.assign(d, m["titan"]))

    # 継ぎ目のリング
    for name, y in (("ring_fore", half), ("ring_aft", -half)):
        r = L.ring(name, R_OUT + 0.014, 0.040, loc=(0, y, 0))
        parts.append(L.assign(r, m["titan"]))
        if bolts:
            parts += dome_bolts(m, y, R_OUT + 0.014)

    # のぞき窓（外へ向かって広がる円錐台＝水圧で押し込まれる向き）
    vy = half + R_OUT - 0.06
    parts.append(L.assign(
        L.taper("viewport", VIEWPORT_R * 1.45, VIEWPORT_R, 0.20, vy, toward=+1),
        m["dome"]))
    parts.append(L.assign(
        L.ring("viewport_ring", VIEWPORT_R * 1.5, 0.030, loc=(0, vy, 0)),
        m["titan"]))
    return parts


# ── 外装 ────────────────────────────────────────────────────────
def exterior(m):
    """白い外装（フェアリング）と受け台。ヒーローショット用。"""
    parts = []
    body_len = 3.30
    nose_len = 1.55
    tail_len = LOA - body_len - nose_len       # 1.86

    b = L.cylinder("fair_body", R_FAIR, body_len, verts=128)
    L.bevel(b, 0.04, 3)
    parts.append(L.assign(b, m["white"]))

    # 船首：胴体から前方（+Y）へすぼまり、先端にドームが載る
    parts.append(L.assign(
        L.taper("fair_nose", R_FAIR, DOME_R * 0.92, nose_len,
                body_len / 2, toward=+1), m["white"]))
    # 船尾：胴体から後方（−Y）へすぼまる
    parts.append(L.assign(
        L.taper("fair_tail", R_FAIR, 0.40, tail_len,
                -body_len / 2, toward=-1), m["white"]))

    # 🔴 前面の黒いドーム。参照chで最も目を引く要素なので大きく取る
    ny = body_len / 2 + nose_len
    parts.append(L.assign(
        L.hemisphere("fair_dome", DOME_R, loc=(0, ny, 0), facing=(0, 1, 0)),
        m["dome"]))
    parts.append(L.assign(
        L.ring("dome_ring", DOME_R * 0.99, 0.032, loc=(0, ny, 0)), m["titan"]))

    # 胴体の帯。🔴 2巡目は太くて黒く「輪ゴム」に見えたので、細く明るく
    for y in (-0.55, 0.55):
        parts.append(L.assign(
            L.ring(f"band_{y}", R_FAIR + 0.006, 0.013, loc=(0, y, 0)),
            m["titan"]))

    # 受け台（そり）。🔴 2巡目は脚が短くて胴体に届かず「はしご」に見えた。
    #    脚の長さを胴体まで届く値から逆算する。
    z_rail = -(R_FAIR + 0.42)
    for sx in (-0.86, 0.86):
        parts.append(L.assign(
            L.box("skid", (0.14, LOA * 0.70, 0.14), loc=(sx, -0.30, z_rail)),
            m["frame"]))
        for sy in (-1.85, -0.30, 1.15):
            # 胴体表面（その位置での半径）まで届く高さにする
            z_hull = -math.sqrt(max(0.01, R_FAIR ** 2 - sx ** 2)) if abs(sx) < R_FAIR \
                else -0.20
            h = abs(z_hull - z_rail)
            parts.append(L.assign(
                L.box("leg", (0.11, 0.11, h), loc=(sx, sy, z_rail + h / 2)),
                m["frame"]))
    # 前後の横つなぎ
    for sy in (-1.85, 1.15):
        parts.append(L.assign(
            L.box("cross", (1.86, 0.12, 0.12), loc=(0, sy, z_rail)), m["frame"]))

    # スラスター4基。🔴 2巡目は胴体に埋まって「半分の球」に見えたので、
    #    胴体の外へ完全に出し、支柱を付けて筒として読ませる
    for sx, sy in ((-1.0, -0.95), (1.0, -0.95), (-1.0, 0.75), (1.0, 0.75)):
        out = 1.0 if sx > 0 else -1.0
        parts.append(L.assign(
            L.cylinder("thruster", 0.175, 0.40,
                       loc=(sx + out * 0.52, sy, -0.26), axis="X", verts=32),
            m["frame"]))
        parts.append(L.assign(
            L.ring("thruster_lip", 0.175, 0.022,
                   loc=(sx + out * 0.72, sy, -0.26), axis="X"), m["titan"]))
        parts.append(L.assign(
            L.box("pylon", (0.40, 0.045, 0.045), loc=(sx + out * 0.22, sy, -0.26)),
            m["frame"]))
    return parts


# ── 断面の出し方 ────────────────────────────────────────────────
def seated_figures(m, n=5, x=-0.30, z_floor=-R_IN * 0.62):
    """座っている人を n 体。**「狭さ」はこれが無いと絶対に伝わらない。**

    ⚠️ 表情・指・口パクは作らない。参照chも顔なしのマネキンで通している。
    ⚠️ 圧壊カット（anim=implode）には人を出さないこと。
       YouTubeの広告適性で「教育目的の枠外での死の描写」に寄るため
       （権利レビューの指摘）。ここは「乗り込む／狭さ」のカットなので置いてよい。
    """
    out = []
    span = CYL_LEN * 0.78
    for i in range(n):
        y = -span / 2 + span * i / max(1, n - 1)
        # 🔴 8巡目もまだ「立ち気味」だった。座って見える決め手は **腰**。
        #    腰の塊から「胴が上へ」「太ももが前へ」同じ高さで分岐すると、
        #    L字のシルエットができて一目で座位に読める。
        #    胴だけ長い縦箱だと、足を付けても立ち姿に見える。
        hip_z = z_floor + 0.17
        out.append(L.assign(                      # 腰
            L.box(f"fig_hip_{i}", (0.34, 0.22, 0.30), loc=(x, y, hip_z)),
            m["figure"]))
        out.append(L.assign(                      # 太もも（腰と同じ高さで前へ）
            L.box(f"fig_thigh_{i}", (0.46, 0.20, 0.19),
                  loc=(x + 0.38, y, hip_z - 0.03)), m["figure"]))
        shin = L.box(f"fig_shin_{i}", (0.36, 0.18, 0.16),      # すね（前下がり）
                     loc=(x + 0.70, y, z_floor + 0.11))
        shin.rotation_euler = (0, math.radians(28), 0)
        out.append(L.assign(shin, m["figure"]))

        torso = L.box(f"fig_torso_{i}", (0.28, 0.23, 0.46),    # 胴（腰の上）
                      loc=(x - 0.02, y, hip_z + 0.30))
        torso.rotation_euler = (0, math.radians(-13), 0)       # 背をもたれさせる
        out.append(L.assign(torso, m["figure"]))

        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.098, segments=24, ring_count=16,
                                             location=(x - 0.12, y, hip_z + 0.62))
        h = bpy.context.object
        h.name = f"fig_head_{i}"
        bpy.ops.object.shade_smooth()
        out.append(L.assign(h, m["figure"]))
    return out


def half_hull(m, highlight=(), figures=True):
    """耐圧殻の半割り。**切らずに、最初から半分だけ作る。**

    円筒は solid_arc（中実の半円筒）なので、両端に必ず正しい断面が出る。
    ドームは半球を半分にするので cut を使うが、穴埋めをしない（fill=False）ので
    ゴミ面は出ない。切り口は壁の厚みぶんしか開かず、ほぼ見えない。
    """
    parts = []
    half = CYL_LEN / 2

    # 壁を5層に割って、断面に帯として出す（実寸。細いが「厚みがある」ことは読める）
    step = (R_OUT - R_IN) / N_LAYERS
    for i in range(N_LAYERS):
        idx = i + 1
        # 🔴 実寸だと壁は直径の7.6%しかなく、朱赤が「細い赤線」にしか見えない。
        #    剥離した層から外側を 30mm 浮かせて、隙間そのものを見せる。
        #    厚みは実寸のまま（誇張しない）。浮かせるのは剥離の表現なので嘘にならない。
        lift = 0.030 if (highlight and idx >= min(highlight)) else 0.0
        mat = m["alert"] if idx in highlight else (m["carbon"] if i % 2 == 0
                                                   else m["carbon2"])
        # 90..270 度＝x<0 側だけを残す。カメラは +X から見るので、
        # 手前が開いて中がのぞける（断面図の作法）。
        parts.append(L.assign(
            L.solid_arc(f"hull_layer_{idx}", R_IN + step * i + lift,
                        R_IN + step * (i + 1) + lift, CYL_LEN, 90.0, 270.0), mat))

    # 半球ドーム（半分だけ残す）
    for name, y, facing in (("dome_fore", half, (0, 1, 0)),
                            ("dome_aft", -half, (0, -1, 0))):
        d = L.hemisphere(name, R_OUT, loc=(0, y, 0), facing=facing)
        s = d.modifiers.new("thick", "SOLIDIFY")
        s.thickness = 0.055
        L.cut(d, plane_no=(1, 0, 0), clear="outer", fill=False)
        parts.append(L.assign(d, m["titan"]))

    # 継ぎ目リング（半分）
    for name, y in (("ring_fore", half), ("ring_aft", -half)):
        r = L.ring(name, R_OUT + 0.014, 0.040, loc=(0, y, 0))
        L.cut(r, plane_no=(1, 0, 0), clear="outer", fill=False)
        parts.append(L.assign(r, m["titan"]))

    # 中の床。人が座る面を置くと「狭さ」が一気に読める（c204）
    parts.append(L.assign(
        L.box("floor", (R_IN * 0.86, CYL_LEN * 0.92, 0.03),
              loc=(-R_IN * 0.43, 0, -R_IN * 0.62)), m["inner"]))
    if figures:
        parts += seated_figures(m)
    return parts


# ── 入口 ────────────────────────────────────────────────────────
MODES = ("exterior", "hull", "hull_layers", "cutaway")


def build(mode="exterior", highlight=(), at=(0, 0, 0), rot_z=0.0, scale=1.0):
    """mode: exterior / hull / hull_layers / cutaway

    ⚠️ 位置・回転・拡大は **root の Empty にだけ**かける。
       部品ごとに動かすと必ずどこかがずれる。
    """
    m = _mats()
    if mode == "exterior":
        parts = exterior(m)
    elif mode == "hull":
        parts = pressure_hull(m, layers=False)
    elif mode == "hull_layers":
        # 🔴 実寸の円筒断面では壁が細すぎて読めない（2巡目の失敗）。
        #    壁の一部だけを取り出して比率を誇張した模式図にする。
        parts = wall_sample(m, highlight=highlight)
    elif mode == "cutaway":
        parts = half_hull(m, highlight=highlight)
    else:
        raise SystemExit(f"[titan] 知らない mode: {mode}（{MODES}）")

    root = L.new_empty("titan_root")
    L.parent_to(parts, root)
    root.location = at
    root.rotation_euler = (0, 0, math.radians(rot_z))
    root.scale = (scale, scale, scale)
    print(f"[titan] mode={mode} parts={len(parts)} highlight={highlight}")
    return root
