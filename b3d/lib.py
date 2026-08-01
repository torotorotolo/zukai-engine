# -*- coding: utf-8 -*-
"""Blender の中で使う共通の道具（マテリアル・形・カメラ・光・レンダ設定）。

⚠️ このファイルは Blender の中でしか動かない（bpy を import する）。
   ローカルの4GB機からは絶対に読み込まない。tools/ 側から import しないこと。
"""
import math

import bmesh
import bpy
from mathutils import Vector


# ── 色 ─────────────────────────────────────────────────────────
def srgb_to_linear(c):
    """🔴 Blender のマテリアルはリニア値を受け取る。

    sRGBの16進をそのまま /255 して入れると、2D図解と色が合わない。
    設計レビューで「継ぎ目対策のコードが継ぎ目を作る側に働く」と
    指摘されたのがこれ。必ずこの関数を通す。
    """
    c = c / 255.0 if c > 1.0 else c
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hexcol(h, a=1.0):
    """'#0f1922' → リニアRGBA"""
    h = h.lstrip("#")
    return (srgb_to_linear(int(h[0:2], 16)),
            srgb_to_linear(int(h[2:4], 16)),
            srgb_to_linear(int(h[4:6], 16)), a)


# 2D図解（jiko_style.py）と揃えた色
INK_W = "#e8eef2"      # 白に近い字
DEEP_BG = "#0f1922"    # 深海の地
ALERT = "#c8402e"      # 朱赤（強調）
AMBER = "#d9a441"      # 山吹（数値）


# ── マテリアル ──────────────────────────────────────────────────
def material(name, color, rough=0.5, metal=0.0, emit=None, alpha=1.0):
    """参照chに合わせて「フラット寄り」に作る。

    参照chの潜水艇は拡大してもテクスチャの粒子が見えない。
    主役はシンプル、環境だけテクスチャ頼り、という割り切りをそのまま採る。
    """
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes.get("Principled BSDF")
    if b is None:
        return m
    b.inputs["Base Color"].default_value = hexcol(color) if isinstance(color, str) else color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if "Alpha" in b.inputs:
        b.inputs["Alpha"].default_value = alpha
        if alpha < 1.0:
            m.blend_method = "BLEND" if hasattr(m, "blend_method") else m.blend_method
    if emit is not None and "Emission Color" in b.inputs:
        b.inputs["Emission Color"].default_value = hexcol(emit) if isinstance(emit, str) else emit
        b.inputs["Emission Strength"].default_value = 1.0
    return m


def assign(ob, mat):
    ob.data.materials.clear()
    ob.data.materials.append(mat)
    return ob


# ── 形をつくる ──────────────────────────────────────────────────
def new_empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "PLAIN_AXES"
    e.location = loc
    bpy.context.scene.collection.objects.link(e)
    return e


def cylinder(name, radius, depth, loc=(0, 0, 0), axis="Y", verts=64):
    """円筒。既定は Y 軸方向（潜水艇の長手方向）に寝かせる。"""
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=verts,
                                        location=loc)
    ob = bpy.context.object
    ob.name = name
    if axis == "Y":
        ob.rotation_euler = (math.radians(90), 0, 0)
    elif axis == "X":
        ob.rotation_euler = (0, math.radians(90), 0)
    bpy.ops.object.shade_smooth()
    return ob


def hemisphere(name, radius, loc=(0, 0, 0), facing=(0, 1, 0), segments=64, rings=32):
    """半球。facing の向きに膨らむ。

    ⚠️ Boolean は使わない。bmesh で切って半分を消す。
       Boolean のオペランドはワールド空間で評価されるので、
       あとから location/scale を変えると胴体だけ動いて口が開く
       （設計レビューで指摘された事故のかたち）。
    """
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=segments,
                                         ring_count=rings, location=(0, 0, 0))
    ob = bpy.context.object
    ob.name = name

    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    n = Vector(facing).normalized()
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                           plane_co=(0, 0, 0), plane_no=n, clear_inner=True)
    bm.to_mesh(me)
    bm.free()

    ob.location = loc
    bpy.ops.object.shade_smooth()
    return ob


def ring(name, radius, thickness, loc=(0, 0, 0), axis="Y", verts=64):
    """継ぎ目のリング（チタンの結合部）。"""
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=thickness,
                                     major_segments=verts, minor_segments=16,
                                     location=loc)
    ob = bpy.context.object
    ob.name = name
    if axis == "Y":
        ob.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.shade_smooth()
    return ob


def taper(name, r_root, r_tip, depth, root_y, toward=+1, verts=64):
    """すぼまり（船首・船尾・のぞき窓）。

    🔴 `primitive_cone_add` は radius1 が −Z 側、radius2 が +Z 側にできる。
       これを X軸まわりに +90° 回すと −Z→+Y に写るので、
       「radius1 が +Y 側」になる。ここを取り違えると円錐が逆向きに開く
       （1巡目で実際に船首と船尾の両方が外へラッパ状に開いた）。

    root_y  … 太いほうの端の Y座標
    toward  … +1 なら +Y 方向へすぼまる／−1 なら −Y 方向へ
    """
    # 太い側を root_y に、細い側を root_y + toward*depth に置く
    cy = root_y + toward * depth / 2.0
    if toward > 0:
        # 太い側を +Y に置きたい → radius1（−Z側→+Y側）を太くする
        r1, r2, rot = r_root, r_tip, math.radians(-90)
    else:
        r1, r2, rot = r_tip, r_root, math.radians(-90)
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=depth,
                                    vertices=verts, location=(0, cy, 0))
    ob = bpy.context.object
    ob.name = name
    ob.rotation_euler = (rot, 0, 0)
    bpy.ops.object.shade_smooth()
    return ob


def apply_modifiers(ob):
    """モディファイアを確定させる。切る前に必ず通す。

    Solidify で付けた厚みは、適用しないと切断面に出てこない。
    """
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    for mod in list(ob.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except RuntimeError:
            pass
    return ob


def cut(ob, plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear="outer"):
    """平面で切って片側を捨てる。

    🔴 法線は必ずローカル空間へ変換してから渡すこと。
       1巡目はワールド空間の法線をそのまま渡したせいで、
       90°回転している物体の切断面が明後日を向き、**何も切れていなかった**。
    """
    import bmesh
    from mathutils import Vector

    if ob.type != "MESH":
        return ob
    apply_modifiers(ob)
    inv = ob.matrix_world.inverted()
    co_l = inv @ Vector(plane_co)
    no_l = (inv.to_3x3() @ Vector(plane_no)).normalized()

    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    res = bmesh.ops.bisect_plane(
        bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
        plane_co=co_l, plane_no=no_l,
        clear_outer=(clear == "outer"), clear_inner=(clear == "inner"))

    # 🔴 切っただけでは断面が「空いたまま」になる。
    #    穴を塞がないと、炭素繊維の層が帯として読めず、向こう側が透けて見える。
    #    層の枚数を見せるのがこのカットの目的なので、ここは必須。
    cut_edges = [e for e in res.get("geom_cut", [])
                 if isinstance(e, bmesh.types.BMEdge)]
    if cut_edges:
        try:
            bmesh.ops.holes_fill(bm, edges=cut_edges, sides=0)
        except (TypeError, RuntimeError):
            try:
                bmesh.ops.edgenet_fill(bm, edges=cut_edges)
            except (TypeError, RuntimeError):
                pass
    bm.to_mesh(me)
    bm.free()
    me.update()
    return ob


def box(name, size, loc=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = size
    return ob


def parent_to(children, root):
    """root の Empty にぶら下げる。

    これで root を動かす／回す／拡大するだけで全部が一緒に動く。
    部品ごとに location を書き換えると必ずどこかがずれる。
    """
    for c in children:
        c.parent = root
        c.matrix_parent_inverse = root.matrix_world.inverted()
    return root


def bevel(ob, width=0.01, segments=2):
    m = ob.modifiers.new("bevel", "BEVEL")
    m.width = width
    m.segments = segments
    m.limit_method = "ANGLE"
    return ob


# ── シーン・カメラ・光 ─────────────────────────────────────────
def setup_scene(res_x=1920, res_y=1080, samples=32, denoise=True, fps=15):
    """🔴 実測で確定した設定（2026-08-01 / b3d/README.md 参照）。

    - Cycles + OptiX（Modal では EEVEE が動かない）
    - デノイズは必ず GPU。CPUのままだと 4.85秒 → GPUで 1.89秒（2.6倍）
    - view_transform は Standard。AgX だと2D図解と色が合わない
    """
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.render.resolution_x = res_x
    sc.render.resolution_y = res_y
    sc.render.resolution_percentage = 100
    sc.render.fps = fps
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "Standard"

    prefs = bpy.context.preferences.addons["cycles"].preferences
    kind = None
    for k in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = k
            kind = k
            break
        except TypeError:
            continue
    if kind is None:
        raise SystemExit("[FATAL] Cycles が OPTIX/CUDA を受け付けません。")
    prefs.get_devices()
    on = [d.name for d in prefs.devices if d.type in ("OPTIX", "CUDA")]
    for d in prefs.devices:
        d.use = d.type in ("OPTIX", "CUDA")
    if not on:
        raise SystemExit("[FATAL] GPUデバイスが0本です。CPUレンダになるので止めます。")
    sc.cycles.device = "GPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = denoise
    if denoise and hasattr(sc.cycles, "denoising_use_gpu"):
        sc.cycles.denoising_use_gpu = True          # ★これを忘れると2.6倍遅い
    print(f"[scene] {kind} devices={on} samples={samples} "
          f"denoise_gpu={getattr(sc.cycles, 'denoising_use_gpu', 'n/a')}")
    return sc


def deep_sea(sc, density=0.012, color="#12384a", bg_strength=0.18):
    """深海の空間。参照chの実装は「体積フォグの箱1つ＋スポット1灯」以上のことをしていない。"""
    w = bpy.data.worlds.new("W")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = hexcol(DEEP_BG)
    bg.inputs["Strength"].default_value = bg_strength

    bpy.ops.mesh.primitive_cube_add(size=60, location=(0, 0, 0))
    fog = bpy.context.object
    fog.name = "fog"
    m = bpy.data.materials.new("fog_mat")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    s = nt.nodes.new("ShaderNodeVolumeScatter")
    s.inputs["Density"].default_value = density
    s.inputs["Color"].default_value = hexcol(color)
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(s.outputs["Volume"], o.inputs["Volume"])
    fog.data.materials.append(m)
    return fog


def studio(sc, bg="#16232e", strength=0.35):
    """図解用の平坦な地。単色グラデ＋やわらかい上方光＋接地影だけ。"""
    w = bpy.data.worlds.new("W")
    sc.world = w
    w.use_nodes = True
    b = w.node_tree.nodes["Background"]
    b.inputs["Color"].default_value = hexcol(bg)
    b.inputs["Strength"].default_value = strength
    return None


def key_light(target, energy=4000.0, loc=(5, -7, 4), spot=True, size=1.1):
    """🔴 必ず「物を作ったあと」に呼ぶこと。

    先に作ると TRACK_TO の相手がまだ居らず、constraint に target が入らないまま
    スポットが真下を向く。エラーは1つも出ないので、暗い映像が焼き上がるまで
    気づけない（設計レビューで指摘された実際の事故のかたち）。
    """
    if target is None:
        raise SystemExit("[FATAL] key_light の注視先がありません。物を先に作ってください。")
    d = bpy.data.lights.new("key", type="SPOT" if spot else "AREA")
    d.energy = energy
    if spot:
        d.spot_size = size
        d.spot_blend = 0.4
    else:
        d.size = 6.0
    lt = bpy.data.objects.new("key", d)
    bpy.context.scene.collection.objects.link(lt)
    lt.location = loc
    c = lt.constraints.new("TRACK_TO")
    c.target = target
    if c.target is None:
        raise SystemExit("[FATAL] ライトの注視先が解決しませんでした。")
    return lt


def fill_light(target, energy=300.0, loc=(-6, 4, 2)):
    d = bpy.data.lights.new("fill", type="AREA")
    d.energy = energy
    d.size = 8.0
    lt = bpy.data.objects.new("fill", d)
    bpy.context.scene.collection.objects.link(lt)
    lt.location = loc
    c = lt.constraints.new("TRACK_TO")
    c.target = target
    return lt


def camera(sc, target, azimuth=45.0, elevation=12.0, distance=12.0, lens=50.0):
    """注視点まわりの球面座標でカメラを置く。カット表からはこの3つの数字だけ渡す。"""
    a, e = math.radians(azimuth), math.radians(elevation)
    loc = (distance * math.cos(e) * math.cos(a),
           distance * math.cos(e) * math.sin(a),
           distance * math.sin(e))
    d = bpy.data.cameras.new("cam")
    d.lens = lens
    cam = bpy.data.objects.new("cam", d)
    sc.collection.objects.link(cam)
    cam.location = loc
    c = cam.constraints.new("TRACK_TO")
    c.target = target
    sc.camera = cam
    return cam
