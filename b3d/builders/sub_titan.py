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
  炭素繊維の層    5層（1インチ×5 ＝ 5インチ）

■ 作りの方針（参照chの実測に合わせる）
  - 主役はフラット。テクスチャを貼らない（拡大しても粒子が見えないのが参照chの絵）
  - Boolean を使わない。bmesh で切る（Boolean はワールド空間評価なので、
    あとから動かすと胴体だけ動いて口が開く）
  - 全部を root の Empty にぶら下げる。root を動かせば全部が一緒に動く
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

# ── 色（2D図解と揃える）──────────────────────────────────────
C_WHITE = "#dfe4e7"   # 外装の白
C_CARBON = "#2b3138"  # 炭素繊維（濃い墨）
C_TITAN = "#9aa4ac"   # チタン
C_GLASS = "#1b2b36"   # のぞき窓（暗いアクリル）
C_FRAME = "#3a4249"   # 台とフレーム


def _mats():
    return dict(
        white=L.material("m_white", C_WHITE, rough=0.42, metal=0.0),
        carbon=L.material("m_carbon", C_CARBON, rough=0.55, metal=0.0),
        titan=L.material("m_titan", C_TITAN, rough=0.30, metal=1.0),
        glass=L.material("m_glass", C_GLASS, rough=0.08, metal=0.0),
        frame=L.material("m_frame", C_FRAME, rough=0.60, metal=0.8),
        alert=L.material("m_alert", L.ALERT, rough=0.45, metal=0.0),
    )


def carbon_layers(m, n=N_LAYERS, highlight=()):
    """炭素繊維の層を n 枚の同心の筒として作る。

    🔴 層の表現は「変形」ではなく「板を重ねる」。
       設計レビューで、頂点を一様に縮める実装では layers=[2,3] の指定が
       絵に出ない（＝企画の中核カットが成立しない）と指摘された点。
       剥離は、指定した層を法線方向へずらすことで見せる。

    highlight … 朱赤で強調する層の番号（1始まり）。剥離した層を指す。
    """
    step = (R_OUT - R_IN) / n
    out = []
    for i in range(n):
        r = R_IN + step * (i + 0.5)
        # 剥離した層はわずかに外へ逃がす（参照chも変形ではなく板をずらしている）
        gap = 0.018 if (i + 1) in highlight else 0.0
        c = L.cylinder(f"cf_layer_{i + 1}", r + gap, CYL_LEN, verts=96)
        sol = c.modifiers.new("thick", "SOLIDIFY")
        sol.thickness = step * 0.82
        sol.offset = 0
        L.assign(c, m["alert"] if (i + 1) in highlight else m["carbon"])
        out.append(c)
    return out


def pressure_hull(m, layers=True, highlight=()):
    """耐圧殻：炭素繊維の円筒＋前後のチタン半球ドーム＋継ぎ目リング＋のぞき窓。"""
    parts = []
    half = CYL_LEN / 2

    if layers:
        parts += carbon_layers(m, highlight=highlight)
    else:
        c = L.cylinder("cf_shell", (R_IN + R_OUT) / 2, CYL_LEN, verts=96)
        s = c.modifiers.new("thick", "SOLIDIFY")
        s.thickness = WALL
        L.assign(c, m["carbon"])
        parts.append(c)

    # 前後のチタン半球ドーム
    for name, y, facing in (("dome_fore", half, (0, 1, 0)),
                            ("dome_aft", -half, (0, -1, 0))):
        d = L.hemisphere(name, R_OUT, loc=(0, y, 0), facing=facing)
        s = d.modifiers.new("thick", "SOLIDIFY")
        s.thickness = 0.06
        parts.append(L.assign(d, m["titan"]))

    # 継ぎ目のリング（ここでボルトで締める）
    for name, y in (("ring_fore", half), ("ring_aft", -half)):
        r = L.ring(name, R_OUT + 0.012, 0.045, loc=(0, y, 0))
        parts.append(L.assign(r, m["titan"]))

    # のぞき窓（円錐台。外に向かって広がる＝水圧で押し込まれる向き）
    vy = half + R_OUT - 0.05
    vp = L.cone("viewport", VIEWPORT_R * 1.35, VIEWPORT_R, 0.22, loc=(0, vy, 0))
    parts.append(L.assign(vp, m["glass"]))
    vr = L.ring("viewport_ring", VIEWPORT_R * 1.4, 0.035, loc=(0, vy - 0.10, 0))
    parts.append(L.assign(vr, m["titan"]))

    return parts


def exterior(m):
    """白い外装（フェアリング）と、載せる台。ヒーローショット用。"""
    parts = []
    body_len = 4.05
    r_body = 1.02

    b = L.cylinder("fair_body", r_body, body_len, verts=96)
    L.bevel(b, 0.03, 3)
    parts.append(L.assign(b, m["white"]))

    # 船首のすぼまり（のぞき窓に向かって細くなる）
    nose_len = 1.35
    n = L.cone("fair_nose", r_body, VIEWPORT_R * 1.6,
               nose_len, loc=(0, body_len / 2 + nose_len / 2, 0))
    parts.append(L.assign(n, m["white"]))

    # 船尾のすぼまり
    tail_len = LOA - body_len - nose_len
    t = L.cone("fair_tail", r_body, 0.42, tail_len,
               loc=(0, -(body_len / 2 + tail_len / 2), 0))
    t.rotation_euler = (math.radians(-90), 0, 0)
    parts.append(L.assign(t, m["white"]))

    # 黒いドーム（前面）＝参照chで最も目を引く要素
    dome = L.hemisphere("fair_dome", VIEWPORT_R * 1.7,
                        loc=(0, body_len / 2 + nose_len, 0), facing=(0, 1, 0))
    parts.append(L.assign(dome, m["glass"]))

    # 受け台（そり）
    for sx in (-0.72, 0.72):
        sk = L.box("skid", (0.11, LOA * 0.72, 0.11), loc=(sx, -0.2, -r_body - 0.28))
        parts.append(L.assign(sk, m["frame"]))
        for sy in (-1.6, 0.0, 1.6):
            leg = L.box("leg", (0.09, 0.09, 0.34), loc=(sx, sy, -r_body - 0.12))
            parts.append(L.assign(leg, m["frame"]))
    return parts


def cutaway(parts, keep="+x"):
    """断面図。片側を bmesh で切り落として中を見せる。

    ⚠️ Boolean ではなく bmesh。かつ「モディファイアを適用してから」切る。
       Solidify で付けた厚みは、適用しないと切断面に出てこない。
    """
    import bmesh
    from mathutils import Vector

    normal = Vector((1, 0, 0)) if keep == "+x" else Vector((-1, 0, 0))
    for ob in parts:
        if ob.type != "MESH":
            continue
        # モディファイアを先に確定させる（これを忘れると厚みが切断面に出ない）
        bpy.context.view_layer.objects.active = ob
        for mod in list(ob.modifiers):
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except RuntimeError:
                pass
        me = ob.data
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.bisect_plane(
            bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
            plane_co=ob.matrix_world.inverted() @ Vector((0, 0, 0)),
            plane_no=normal, clear_outer=True)
        bm.to_mesh(me)
        bm.free()
    return parts


# ── 入口 ────────────────────────────────────────────────────────
def build(mode="exterior", highlight=(), at=(0, 0, 0), rot_z=0.0, scale=1.0):
    """mode: exterior / hull / hull_layers / cutaway

    ⚠️ 位置・回転・拡大は **root の Empty にだけ**かける。
       部品ごとに動かすと必ずどこかがずれる。
    """
    m = _mats()
    if mode == "exterior":
        parts = exterior(m) + pressure_hull(m, layers=False)
    elif mode == "hull":
        parts = pressure_hull(m, layers=False)
    elif mode == "hull_layers":
        parts = pressure_hull(m, layers=True, highlight=highlight)
    elif mode == "cutaway":
        parts = cutaway(pressure_hull(m, layers=True, highlight=highlight))
    else:
        raise SystemExit(f"[titan] 知らない mode: {mode}")

    root = L.new_empty("titan_root")
    L.parent_to(parts, root)
    root.location = at
    root.rotation_euler = (0, 0, math.radians(rot_z))
    root.scale = (scale, scale, scale)
    return root
