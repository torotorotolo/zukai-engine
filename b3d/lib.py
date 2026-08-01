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


def solid_arc(name, r_in, r_out, length, a0=0.0, a1=180.0, seg=96,
              loc=(0, 0, 0)):
    """環状扇形（ちくわを縦に割った形）を、中実の立体として最初から作る。

    🔴 4巡目までの失敗の総括：
       「丸ごと作ってから bmesh で切る」やり方は2つの問題を同時に抱えていた。
         ① 切ったあとの穴埋め（holes_fill）が不正な面を作り、
            ドームの断面に三角形のゴミが出た
         ② 実寸の壁（直径1,674mmに対し127mm）は切っても細すぎて読めない
       → **切らない。最初から欲しい形だけを作る。**
          断面は「切った跡」ではなく、最初から在る面になるので必ず正しく出る。

    r_in..r_out … 壁の内半径・外半径（この幅が断面の帯になる）
    a0..a1      … 角度（度）。0..180 なら半割り、55..125 なら細い扇形
    length      … Y方向の長さ
    """
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)

    bm = bmesh.new()
    y0 = -length / 2.0
    ts = [math.radians(a0 + (a1 - a0) * i / seg) for i in range(seg + 1)]
    outer = [bm.verts.new((r_out * math.cos(t), y0, r_out * math.sin(t))) for t in ts]
    inner = [bm.verts.new((r_in * math.cos(t), y0, r_in * math.sin(t)))
             for t in reversed(ts)]
    cap = bm.faces.new(outer + inner)

    ret = bmesh.ops.extrude_face_region(bm, geom=[cap])
    moved = [v for v in ret["geom"] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=moved, vec=(0, length, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])

    bm.to_mesh(me)
    bm.free()
    me.update()
    ob.location = loc
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


def cut(ob, plane_co=(0, 0, 0), plane_no=(1, 0, 0), clear="outer", fill=False):
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

    # 🔴 穴埋めは既定で **切**。
    #    4巡目に holes_fill が不正な面を作り、ドームの断面に三角形のゴミが出た。
    #    厚みのある殻（Solidify済み）なら、切り口は壁の厚みぶんしか開かないので
    #    塞がなくてもほぼ見えない。断面をきちんと見せたい形は
    #    solid_arc() で「最初から中実に作る」こと。
    cut_edges = [e for e in res.get("geom_cut", [])
                 if isinstance(e, bmesh.types.BMEdge)] if fill else []
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


def deep_sea(sc, density=0.040, color="#12384a", bg_strength=0.16):
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
    marine_snow()
    return fog


def marine_snow(count=170, seed=7, span=(6.5, 9.0, 4.0), r=(0.006, 0.016)):
    """マリンスノー（深海に舞う白い粒）。

    🔴 9巡目の失敗：粒を自己発光させ、大きく、広く均一に撒いたら
       **「星空」になった**。深海ではなく宇宙空間に見える。
       深海に見せる条件は粒ではなく **水の濁り（体積フォグ）** のほうが主。
       粒は「濁りの中に少しだけ」が正しい。

       ・発光させない（周りの光で照らされるだけにする）
       ・小さく（6〜16mm）
       ・被写体の周りに寄せる（遠くまで撒くと星になる）
       ・数を抑える

    🔴 seed を固定する。同じ発注書から同じ絵が出ないと5巡のQCが成立しない。
    """
    import random
    rnd = random.Random(seed)

    base = bpy.data.materials.get("m_snow")
    if base is None:
        base = bpy.data.materials.new("m_snow")
        base.use_nodes = True
        b = base.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.58, 0.66, 0.72, 1.0)
        b.inputs["Roughness"].default_value = 0.95
        # 🔴 発光させない。光らせると星になる。

    # 1個だけ作って残りは複製（メッシュを共有するので軽い）
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0,
                                          location=(0, 0, 0))
    src = bpy.context.object
    src.name = "snow_src"
    src.data.materials.append(base)

    for i in range(count):
        ob = src.copy()                     # メッシュは共有
        ob.location = (rnd.uniform(-span[0], span[0]),
                       rnd.uniform(-span[1], span[1]),
                       rnd.uniform(-span[2], span[2]))
        k = rnd.uniform(r[0], r[1])
        ob.scale = (k, k, k)
        bpy.context.scene.collection.objects.link(ob)
    bpy.data.objects.remove(src, do_unlink=True)
    return None


def studio(sc, top="#6f8798", bottom="#18242e", strength=1.8):
    """図解用の地。上が明るく下が暗い縦グラデ。

    🔴 2巡目は単色 #16232e（暗い）1枚で、耐圧殻も断面も真っ黒に沈んだ。
       参照chの図解パートは**明るいグラデ背景**で、物がはっきり見えている。
       グラデにすると、映り込む「空」ができるので金属も黒く落ちない。
    """
    w = bpy.data.worlds.new("W")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()

    tex = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    # 🔴 ワールドの Generated は **−1〜+1** を返す（3巡目はこれを 0〜1 と思い込み、
    #    画面のほぼ全域が暗いほうの色一色になった）。まず 0〜1 に写し直す。
    rng = nt.nodes.new("ShaderNodeMapRange")
    rng.inputs["From Min"].default_value = -0.55
    rng.inputs["From Max"].default_value = 0.75
    rng.inputs["To Min"].default_value = 0.0
    rng.inputs["To Max"].default_value = 1.0
    rng.clamp = True

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = hexcol(bottom)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = hexcol(top)
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = strength
    out = nt.nodes.new("ShaderNodeOutputWorld")

    nt.links.new(tex.outputs["Generated"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Z"], rng.inputs["Value"])
    nt.links.new(rng.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    return None


def inside_light(target, energy=120.0, offset=(0.0, 0.0, 0.0)):
    """断面カットの「中」を照らす。

    🔴 半割りにしても、内側に光が入らないと真っ黒な板にしかならない
       （2巡目で実際にそうなった）。層を読ませたいなら中を照らす。

    🔴 offset を必ず指定すること。既定の「重心」に置くと、
       中に人を置いたカットでは**光が人の胴体の中に入ってしまい**、
       その人だけ黒い点が出る（7巡目で実際に出た）。
    """
    d = bpy.data.lights.new("inside", type="POINT")
    d.energy = energy
    d.shadow_soft_size = 0.5
    lt = bpy.data.objects.new("inside", d)
    bpy.context.scene.collection.objects.link(lt)
    center, _, _ = bounds(target)
    lt.location = (center.x + offset[0], center.y + offset[1], center.z + offset[2])
    return lt


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
        d.spot_blend = 0.5
    else:
        # 🔴 面光源は「大きくする」ほど影と反射がやわらぐ。
        #    1巡目は小さい強いスポットで白飛びした。参照chの絵は平坦で
        #    ハイライトがほぼ無いので、大きく・弱くが正解。
        d.size = size
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


def bounds(root):
    """root にぶら下がる全メッシュの、ワールド座標での中心と半径を返す。

    🔴 カメラ距離を手で置かないための土台。
       2巡目は distance=3.6 を手書きして**対象を突き抜けた**。
       「レイアウトは測ってから直す。目視で置かない」を3Dでも守る。
    """
    from mathutils import Vector

    dg = bpy.context.evaluated_depsgraph_get()
    pts = []

    def walk(ob):
        if ob.type == "MESH":
            ev = ob.evaluated_get(dg)
            mw = ev.matrix_world
            for c in ev.bound_box:
                pts.append(mw @ Vector(c))
        for ch in ob.children:
            walk(ch)

    walk(root)
    if not pts:
        return Vector((0, 0, 0)), 1.0, []
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    center = (lo + hi) / 2.0
    radius = max((p - center).length for p in pts)
    return center, radius, pts


def camera(sc, target, azimuth=45.0, elevation=12.0, lens=50.0,
           fill=0.80, distance=None):
    """対象を必ず画面に収めるカメラ。

    fill … 対象が画面の短辺に占める割合（0.80 なら余白2割）。
           distance を明示すればそちらが優先されるが、**原則 fill で決める**。
    """
    from mathutils import Vector

    bpy.context.view_layer.update()
    center, radius, pts = bounds(target)

    a, e = math.radians(azimuth), math.radians(elevation)
    d = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))

    if distance is None:
        # 🔴 外接球で決めてはいけない（3巡目の失敗）。
        #    全長6.7mの細長い物体は外接球の半径が3.5mになり、それを画面の短辺に
        #    収めようとすると左右に巨大な余白ができて、対象が画面の1/3になる。
        #    正しくは「カメラから見たときの、横と縦の広がり」を別々に測る。
        sensor = 36.0
        aspect = sc.render.resolution_x / max(1, sc.render.resolution_y)
        half_fov_x = math.atan(sensor / 2.0 / lens)
        half_fov_y = math.atan(math.tan(half_fov_x) / aspect)

        fwd = -d                                   # カメラから対象へ向く向き
        up_w = Vector((0, 0, 1))
        right = fwd.cross(up_w)
        right = right.normalized() if right.length > 1e-6 else Vector((1, 0, 0))
        up = right.cross(fwd).normalized()

        mx = my = mz = 0.0
        for p in pts:
            v = p - center
            mx = max(mx, abs(v.dot(right)))
            my = max(my, abs(v.dot(up)))
            mz = max(mz, v.dot(-fwd))              # カメラ側へどれだけ出っ張るか
        dx = mx / math.tan(half_fov_x)
        dy = my / math.tan(half_fov_y)
        distance = max(dx, dy) / max(0.05, fill) + mz
        print(f"[cam] 投影 幅±{mx:.2f}m 高±{my:.2f}m → dx={dx:.1f} dy={dy:.1f}")

    offset = d * distance

    # 注視点は「原点」ではなく「対象の重心」。ここを外すと画面の端に寄る
    aim = new_empty("cam_aim", loc=tuple(center))
    aim.parent = target

    d = bpy.data.cameras.new("cam")
    d.lens = lens
    cam = bpy.data.objects.new("cam", d)
    sc.collection.objects.link(cam)
    cam.location = tuple(center + offset)
    c = cam.constraints.new("TRACK_TO")
    c.target = aim
    sc.camera = cam
    print(f"[cam] r={radius:.2f}m dist={distance:.2f}m lens={lens}mm "
          f"center=({center.x:.2f},{center.y:.2f},{center.z:.2f})")
    return cam


def Vector_(t):
    from mathutils import Vector
    return Vector(t)
