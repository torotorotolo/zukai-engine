# -*- coding: utf-8 -*-
"""EEVEE ヘッドレス・スモークテスト（Blender の中で走る側）。

■ このファイルが答えを出す唯一の問い
    「Modal の GPU コンテナで、Blender の EEVEE Next が
      本当に NVIDIA の GPU を掴んで動くのか。1コマ何秒か。」

  ここが決まらないと、費用も所要時間も全部ただの予想のままになる。
  設計上の全数字が「1コマ1.3秒」という未実測値に乗っているため。

■ 🔴 いちばん危ない失敗の仕方
  EEVEE が GPU を掴み損ねると、Mesa の llvmpipe（CPUでGPUを真似るソフト描画）に
  **エラーを出さずに落ちる**。そのまま描き切ってしまうので気づけず、
  1コマ 30〜120秒（想定の25〜90倍）になって無料枠を成果ゼロで焼き切る。
  → だから describe_gpu() で実際のレンダラ名を見て、ソフト描画なら**課金前に死ぬ**。

■ 使い方（Blender の中から）
    blender -b --factory-startup -P b3d/smoke.py -- --out /out --engine eevee
"""
import json
import os
import sys
import time

import bpy

# ── 引数（`--` より後ろが渡ってくる）─────────────────────────────
ARGV = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    key = "--" + name
    if key in ARGV:
        i = ARGV.index(key)
        if i + 1 < len(ARGV):
            return ARGV[i + 1]
    return default


OUT = arg("out", "/out")
ENGINE = arg("engine", "eevee")          # eevee | cycles
RES = int(arg("res", "1920"))
SAMPLES = int(arg("samples", "32"))
DENOISE = arg("denoise", "1") != "0"
FOG = arg("fog", "1") != "0"
# off / oidn_cpu / oidn_gpu / optix
#   🔴 Blender の既定 OpenImageDenoise は **CPU側で動く**。
#      L4 コンテナのCPUは数コアしかないので、そこが律速になる。
#      実測（2026-08-01・L4・1920px・32サンプル）:
#        デノイズ有 4.50秒 / 無 1.95秒 → デノイズだけで 2.55秒＝全体の57%
#      レイトレ本体より重いのは明らかに異常なので、GPU側へ寄せる。
DENOISER = arg("denoiser", "oidn_gpu")

os.makedirs(OUT, exist_ok=True)


# ── 1. GPU を本当に掴めているかを見る ──────────────────────────
SOFTWARE_MARKERS = ("llvmpipe", "lavapipe", "softpipe", "swrast", "SwiftShader")


def describe_gpu():
    """描画に使われている実物の名前を返す。取れなければ None。"""
    try:
        import gpu
        return dict(
            renderer=gpu.platform.renderer_get(),
            vendor=gpu.platform.vendor_get(),
            version=gpu.platform.version_get(),
            backend=gpu.platform.backend_type_get(),
        )
    except Exception as e:                                   # noqa: BLE001
        return dict(error=f"{type(e).__name__}: {e}")


def assert_not_software(info):
    """ソフト描画に落ちていたら、レンダを始める前に死ぬ。"""
    blob = " ".join(str(v) for v in info.values())
    for m in SOFTWARE_MARKERS:
        if m.lower() in blob.lower():
            raise SystemExit(
                f"[FATAL] ソフトウェア描画に落ちています（{m}）。"
                f" GPU を掴めていないので、ここで止めます。 info={info}"
            )


def _apply_denoiser(scene, kind):
    """デノイザをどこで動かすかを決める。

    Blender 4.x の cycles には2種類ある。
      OPENIMAGEDENOISE … 既定。品質は良いが **既定でCPU実行**。
                          denoising_use_gpu = True でGPUへ寄せられる。
      OPTIX             … NVIDIA専用。GPU実行で最速。
    プロパティ名はバージョンで揺れるので、無ければ黙って飛ばして
    実際に適用できた組み合わせを返す（結果のJSONに残る）。
    """
    c = scene.cycles
    got = []

    def try_set(obj, prop, val):
        if hasattr(obj, prop):
            try:
                setattr(obj, prop, val)
                got.append(f"{prop}={val}")
                return True
            except (TypeError, AttributeError):
                pass
        return False

    if kind == "optix":
        try_set(c, "denoiser", "OPTIX")
    elif kind == "oidn_gpu":
        try_set(c, "denoiser", "OPENIMAGEDENOISE")
        # ★ここが本命。これが無いとCPUで回る
        try_set(c, "denoising_use_gpu", True)
    elif kind == "oidn_cpu":
        try_set(c, "denoiser", "OPENIMAGEDENOISE")
        try_set(c, "denoising_use_gpu", False)

    actual = getattr(c, "denoiser", "?")
    on_gpu = getattr(c, "denoising_use_gpu", "n/a")
    print(f"[denoise] 要求={kind} 適用={got} → denoiser={actual} use_gpu={on_gpu}")
    return f"{kind}:{actual}:gpu={on_gpu}"


def setup_cycles_gpu():
    """Cycles で GPU を使うには scene.cycles.device='GPU' だけでは足りない。
    --factory-startup で起動しているので compute_device_type は 'NONE' のまま。
    ここで明示的に構成しないと、黙って 100% CPU レンダになる。"""
    prefs = bpy.context.preferences.addons["cycles"].preferences
    chosen = None
    for kind in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = kind
            chosen = kind
            break
        except TypeError:
            continue
    if chosen is None:
        raise SystemExit("[FATAL] Cycles が OPTIX/CUDA を受け付けません。")

    prefs.get_devices()
    enabled = []
    for d in prefs.devices:
        d.use = d.type in ("OPTIX", "CUDA")
        if d.use:
            enabled.append(f"{d.name}({d.type})")
    if not enabled:
        raise SystemExit(f"[FATAL] {chosen} の有効なデバイスが0本です。")
    print(f"[cycles] compute_device_type={chosen} devices={enabled}")
    return chosen, enabled


# ── 2. 参照chと同じ密度の最小シーンを組む ──────────────────────
def _finish_scene(scene, body):
    """ライトとカメラを置く。

    ⚠️ ライトは「物を作ったあと」に置く。先に置くと TRACK_TO の相手がまだ居らず、
       constraint に target が入らないままスポットが真下を向く。
       エラーは1つも出ないので、暗い映像が焼き上がるまで気づけない
       （設計レビューで指摘された実際の事故のかたち）。
    """
    ldata = bpy.data.lights.new("key", type="SPOT")
    ldata.energy = 3000.0
    ldata.spot_size = 1.05
    ldata.spot_blend = 0.35
    light = bpy.data.objects.new("key", ldata)
    scene.collection.objects.link(light)
    light.location = (4.0, -6.0, 3.0)
    con = light.constraints.new("TRACK_TO")
    con.target = body
    if con.target is None:
        raise SystemExit("[FATAL] ライトの注視先が解決していません。")

    cdata = bpy.data.cameras.new("cam")
    cdata.lens = 45.0
    cam = bpy.data.objects.new("cam", cdata)
    scene.collection.objects.link(cam)
    cam.location = (7.5, -9.0, 2.2)
    ccon = cam.constraints.new("TRACK_TO")
    ccon.target = body
    scene.camera = cam
    return scene


def build_scene():
    """深海プリセットの最小版。
    「体積フォグの箱 + スポット1灯 + 物1つ」が参照chの深海カットの実質すべて。
    ここが焼ければ、本番の深海カットも焼ける。"""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene

    # 世界（暗い青。sRGBの16進をそのまま入れるとリニアとして解釈されるので変換する）
    def srgb_to_linear(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    world = bpy.data.worlds.new("W")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (
        srgb_to_linear(0x0F / 255), srgb_to_linear(0x19 / 255), srgb_to_linear(0x22 / 255), 1.0)
    bg.inputs["Strength"].default_value = 0.25

    # 主役（円筒＋半球＝潜水艇のいちばん粗い代役）
    bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=2.6, vertices=48, location=(0, 0, 0))
    body = bpy.context.object
    body.name = "hull"
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new("hull_mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.82, 0.83, 0.84, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.45
    body.data.materials.append(mat)

    # 体積フォグの箱（深海の霧と光条の正体はこれ1つ）
    # ⚠️ ここが固定費の主犯かどうかを切り分けるため、--fog 0 で外せるようにしてある
    if not FOG:
        return _finish_scene(scene, body)
    bpy.ops.mesh.primitive_cube_add(size=40, location=(0, 0, 0))
    fog = bpy.context.object
    fog.name = "fog"
    fmat = bpy.data.materials.new("fog_mat")
    fmat.use_nodes = True
    nt = fmat.node_tree
    nt.nodes.clear()
    scat = nt.nodes.new("ShaderNodeVolumeScatter")
    scat.inputs["Density"].default_value = 0.02
    scat.inputs["Color"].default_value = (0.10, 0.30, 0.42, 1.0)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(scat.outputs["Volume"], out.inputs["Volume"])
    fog.data.materials.append(fmat)

    return _finish_scene(scene, body)


def setup_render(scene):
    scene.render.resolution_x = RES
    scene.render.resolution_y = int(RES * 9 / 16)
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    # 2D図解と色を合わせる前提なので AgX は使わない（設計レビューの指摘）
    scene.view_settings.view_transform = "Standard"

    info = {}
    if ENGINE == "cycles":
        scene.render.engine = "CYCLES"
        kind, devs = setup_cycles_gpu()
        scene.cycles.device = "GPU"
        scene.cycles.samples = SAMPLES
        scene.cycles.use_denoising = DENOISE and DENOISER != "off"
        applied = "off"
        if scene.cycles.use_denoising:
            applied = _apply_denoiser(scene, DENOISER)
        info = dict(cycles_backend=kind, cycles_devices=devs,
                    denoise=scene.cycles.use_denoising,
                    denoiser=applied, fog=FOG)
    else:
        # 4.2 以降の EEVEE Next。識別子は環境で揺れるので候補を順に試す。
        for ident in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                scene.render.engine = ident
                info["engine_id"] = ident
                break
            except TypeError:
                continue
        else:
            raise SystemExit("[FATAL] EEVEE の識別子が見つかりません。")
        ee = scene.eevee
        for attr, val in (("taa_render_samples", SAMPLES),
                          ("use_raytracing", True),
                          ("volumetric_samples", 32)):
            if hasattr(ee, attr):
                setattr(ee, attr, val)
    return info


# ── 3. 焼いて、1コマ何秒かを測る ───────────────────────────────
def main():
    t_all = time.time()
    gpu_info = describe_gpu()
    print(f"[gpu] {gpu_info}")

    scene = build_scene()
    engine_info = setup_render(scene)

    # 🔴 ここで初めてGPUの実体が見える（描画コンテキストが立ったあと）
    gpu_info2 = describe_gpu()
    print(f"[gpu after ctx] {gpu_info2}")
    assert_not_software(gpu_info2)

    # 1コマ目は初期化を含むので捨て、2〜3コマ目の平均を実測値にする
    times = []
    for i in range(3):
        scene.render.filepath = os.path.join(OUT, f"smoke_{ENGINE}_{i}.png")
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        times.append(time.time() - t0)
        print(f"[render] frame {i}: {times[-1]:.2f}s")

    warm = sum(times[1:]) / max(1, len(times) - 1)
    result = dict(
        engine=ENGINE,
        blender=bpy.app.version_string,
        resolution=[scene.render.resolution_x, scene.render.resolution_y],
        samples=SAMPLES,
        sec_per_frame_first=round(times[0], 3),
        sec_per_frame=round(warm, 3),          # ★これが欲しかった数字
        all_times=[round(t, 3) for t in times],
        gpu=gpu_info2,
        total_sec=round(time.time() - t_all, 2),
        **engine_info,
    )
    dst = os.path.join(OUT, f"bench_{ENGINE}.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[RESULT] {json.dumps(result, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
