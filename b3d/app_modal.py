# -*- coding: utf-8 -*-
"""Modal（秒課金のクラウド）で Blender をヘッドレス実行する入口。

■ 実行のしかた
    pip install modal
    modal setup                      # ブラウザが開いてアカウントと紐づく（初回だけ）
    modal run b3d/app_modal.py       # スモークテスト（EEVEE と Cycles を1回ずつ）

■ 見積もり
    T4 = $0.000164/秒（$0.59/時）。スモークテストは EEVEE/Cycles 合わせて
    コンテナ起動込みで5分未満なので **$0.05 未満**。

■ 🔴 GPUを掴めているかが全て
    コンテナの中から NVIDIA の OpenGL/EGL が見えないと、EEVEE は
    ソフトウェア描画（llvmpipe）に**黙って落ちる**。それを防ぐ手当てが2つ入っている。
      1) NVIDIA_DRIVER_CAPABILITIES に graphics を入れる
         （これが無いと、コンテナランタイムは CUDA のライブラリしか渡さない）
      2) Mesa のソフト描画ドライバ（libgl1-mesa-dri / mesa-vulkan-drivers / libosmesa6）を
         **わざと入れない**。落ちる先を物理的に無くしておく。
    そのうえで smoke.py が実物のレンダラ名を見て、ソフト描画なら課金前に死ぬ。
"""
import json
import pathlib

import modal

# ── Blender 本体（2026-08-01 に実在と sha256 を確認済み）────────────
BLENDER_VER = "4.5.12"                       # LTS（2028年までサポート）
BLENDER_SHA256 = "95e3a2dfedba3bd32ca54fc355eac6b15a11986954ccb02815a07535d0120a25"
BLENDER_URL = (
    f"https://download.blender.org/release/Blender4.5/"
    f"blender-{BLENDER_VER}-linux-x64.tar.xz"
)

# ⚠️ pip install bpy は使わない。Python 3.13 専用なうえ、
#    -f 1..100 のようなコマンドライン引数が一切使えなくなる。

APT = [
    # X / 入力まわり（background でも Blender がリンクを要求する）
    "libx11-6", "libxi6", "libxxf86vm1", "libxfixes3", "libxrender1", "libxext6",
    "libxkbcommon0", "libsm6", "libice6", "libxrandr2", "libxcursor1", "libxinerama1",
    # GL / EGL の「ローダ」。実体のドライバは NVIDIA 側から渡ってくる
    "libgl1", "libegl1", "libglu1-mesa",
    # 一般
    "libglib2.0-0", "libgomp1", "curl", "xz-utils", "ca-certificates", "ffmpeg",
    # 🔴 ここに libgl1-mesa-dri / mesa-vulkan-drivers / libosmesa6 を足さないこと。
    #    足した瞬間に「静かにソフト描画へ落ちる」経路が開く。
]

image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.4.1-base-ubuntu22.04", add_python="3.11"
    )
    .env({
        # graphics を入れないと OpenGL/EGL が渡らず EEVEE が動かない
        "NVIDIA_DRIVER_CAPABILITIES": "compute,utility,graphics",
        "NVIDIA_VISIBLE_DEVICES": "all",
        "PYTHONUNBUFFERED": "1",
    })
    .apt_install(*APT)
    .run_commands(
        # -f を付ける（付けないと404のHTMLをtarに流し込み、原因の分からない失敗になる）
        f"curl -fsSL --retry 3 -o /tmp/b.tar.xz {BLENDER_URL}",
        f'echo "{BLENDER_SHA256}  /tmp/b.tar.xz" | sha256sum -c -',
        "mkdir -p /opt/blender && tar -xJf /tmp/b.tar.xz -C /opt/blender --strip-components=1",
        "rm /tmp/b.tar.xz",
        "/opt/blender/blender --version",
    )
    .add_local_dir(str(pathlib.Path(__file__).parent), remote_path="/b3d")
)

app = modal.App("jiko-b3d")
vol = modal.Volume.from_name("jiko-b3d-out", create_if_missing=True)


@app.function(image=image, gpu="L4", volumes={"/out": vol}, timeout=900)
def smoke(engine: str = "eevee", res: int = 1920, samples: int = 32):
    """スモークテスト1回ぶん。1コマ何秒かを測って返す。"""
    import subprocess

    cmd = [
        "/opt/blender/blender", "-b", "--factory-startup",
        "-P", "/b3d/smoke.py", "--",
        "--out", "/out", "--engine", engine,
        "--res", str(res), "--samples", str(samples),
    ]
    print(" ".join(cmd))
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(p.stdout[-8000:])
    if p.stderr:
        print("--- stderr ---")
        print(p.stderr[-4000:])
    vol.commit()

    bench = pathlib.Path(f"/out/bench_{engine}.json")
    if p.returncode != 0 or not bench.exists():
        return dict(engine=engine, ok=False, returncode=p.returncode,
                    stderr=p.stderr[-2000:], stdout=p.stdout[-2000:])
    # ⚠️ bench.json 側にも "engine" が入っているので、先に読んでから上書きする
    #    （dict(engine=..., **{"engine": ...}) は TypeError になる）
    data = json.loads(bench.read_text(encoding="utf-8"))
    data.update(engine=engine, ok=True, egl_errors=p.stderr.count("EGL Error"))
    return data


@app.function(image=image, gpu="L4", volumes={"/out": vol}, timeout=600)
def preview(res: int = 1920, samples: int = 32):
    """潜水艇を3カットだけ本焼きして拡大目視にかける。"""
    import subprocess
    import time as _t

    cmd = ["/opt/blender/blender", "-b", "--factory-startup",
           "-P", "/b3d/preview.py", "--",
           "--out", "/out", "--res", str(res), "--samples", str(samples)]
    t0 = _t.time()
    p = subprocess.run(cmd, capture_output=True, text=True)
    wall = _t.time() - t0
    print(p.stdout[-6000:])
    if p.stderr:
        print("--- stderr ---")
        print(p.stderr[-3000:])
    vol.commit()
    made = sorted(x.name for x in pathlib.Path("/out").glob("titan_*.png"))
    return dict(ok=p.returncode == 0, wall_sec=round(wall, 1), files=made,
                egl_errors=p.stderr.count("EGL Error"),
                stderr=p.stderr[-1500:] if p.returncode else "")


@app.function(image=image, volumes={"/out": vol}, timeout=300)
def fetch(names: list):
    """焼けたPNGを持ち帰る。GPUを使わないCPUコンテナなので、ほぼ無料。"""
    out = {}
    for n in names:
        f = pathlib.Path("/out") / n
        if f.exists():
            out[n] = f.read_bytes()
    return out


@app.function(image=image, gpu="T4", volumes={"/out": vol}, timeout=300)
def probe():
    """🔴 レンダする前に「GPUが本当に使える形で渡っているか」を確かめる。

    EEVEE は OpenGL/EGL 経由でGPUを使う。Modal のようなコンテナ基盤では
    CUDA のライブラリだけが渡り、**描画用の NVIDIA EGL/GLX が渡らない**ことがある。
    そうなると EEVEE は EGL_BAD_MATCH を出しつつソフト描画に落ち、
    絵は出るのに桁違いに遅い、という一番たちの悪い壊れ方をする。
    """
    import glob
    import subprocess

    def sh(cmd):
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return (r.stdout + r.stderr).strip()

    info = dict(
        nvidia_smi=sh("nvidia-smi --query-gpu=name,driver_version,memory.total "
                      "--format=csv,noheader") or "(nvidia-smi なし)",
        # NVIDIA の EGL/GLX 実体があるか。無ければ EEVEE はGPUを使えない
        egl_nvidia=sorted(glob.glob("/usr/lib/x86_64-linux-gnu/libEGL_nvidia.so*")),
        glx_nvidia=sorted(glob.glob("/usr/lib/x86_64-linux-gnu/libGLX_nvidia.so*")),
        egl_vendor_icd=sorted(glob.glob("/usr/share/glvnd/egl_vendor.d/*")),
        # ソフト描画ドライバが紛れ込んでいないか
        mesa_dri=sorted(glob.glob("/usr/lib/x86_64-linux-gnu/dri/*.so"))[:8],
        libcuda=sorted(glob.glob("/usr/lib/x86_64-linux-gnu/libcuda.so*")),
        driver_caps=sh("echo $NVIDIA_DRIVER_CAPABILITIES"),
        blender=sh("/opt/blender/blender --version | head -1"),
    )
    # Cycles から見えるデバイス（CUDA/OptiX。EGLとは別系統なのでここは通る見込み）
    info["cycles_devices"] = sh(
        "/opt/blender/blender -b --factory-startup --python-expr "
        "\"import bpy;p=bpy.context.preferences.addons['cycles'].preferences;"
        "p.compute_device_type='OPTIX';p.get_devices();"
        "print('DEVICES:',[(d.name,d.type) for d in p.devices])\" 2>&1 | grep DEVICES"
    )
    for k, v in info.items():
        print(f"  {k}: {v}")
    return info


@app.function(image=image, gpu="T4", volumes={"/out": vol}, timeout=1800)
def bench_all(sample_list: list, res: int = 1920,
              denoise: bool = True, fog: bool = True,
              denoiser: str = "oidn_gpu"):
    """🔴 サンプル数の比較は「1つのコンテナの中で」やること。

    smoke.remote() を回数ぶん呼ぶと、そのたびに別のコンテナ＝別の物理T4が立つ。
    機体の当たり外れや同居ワークロードの影響がサンプル数の差より大きく出て、
    「8サンプルが32サンプルより遅い」という筋の通らない表が出る（2026-08-01に実際に出た）。
    同じGPUで連続して測れば比較になる。
    """
    import subprocess

    out = []
    for s in sample_list:
        cmd = [
            "/opt/blender/blender", "-b", "--factory-startup",
            "-P", "/b3d/smoke.py", "--",
            "--out", "/out", "--engine", "cycles",
            "--res", str(res), "--samples", str(s),
            "--denoise", "1" if denoise else "0",
            "--fog", "1" if fog else "0",
            "--denoiser", denoiser,
        ]
        p = subprocess.run(cmd, capture_output=True, text=True)
        bench = pathlib.Path("/out/bench_cycles.json")
        if p.returncode != 0 or not bench.exists():
            out.append(dict(samples=s, ok=False, stderr=p.stderr[-800:]))
            continue
        d = json.loads(bench.read_text(encoding="utf-8"))
        out.append(dict(samples=s, ok=True, spf=d["sec_per_frame"],
                        times=d["all_times"], devices=d.get("cycles_devices")))
        print(f"  samples={s:>4} -> {d['sec_per_frame']:.2f} 秒/コマ  {d['all_times']}")
    vol.commit()
    return out


@app.local_entrypoint()
def look(res: int = 1920, samples: int = 32, out: str = "out/jiko/b3d"):
    """潜水艇を3カット焼いて手元に持ち帰る（拡大目視用）。

    🔴 Modal を呼ぶ前に必ず budget.check() を通す。
       上限を超える見込みなら、1バイトも課金せずにここで止まる。
    """
    import budget

    FRAMES = 4
    SPF = 1.89                      # L4 / 1920px / 32サンプルの実測値
    est = budget.check("L4", FRAMES, SPF, f"潜水艇プレビュー4枚 {res}px")

    r = preview.remote(res=res, samples=samples)
    budget.record("L4", r.get("wall_sec", 0.0), f"潜水艇プレビュー4枚 {res}px", est)

    if not r.get("ok"):
        print("❌ 失敗しました")
        print(r.get("stderr", "")[-1500:])
        return
    if r.get("egl_errors"):
        print(f"⚠️ EGLエラー {r['egl_errors']}件（GPUを掴めていない疑い）")

    dst = pathlib.Path(out)
    dst.mkdir(parents=True, exist_ok=True)
    for name, data in fetch.remote(r["files"]).items():
        (dst / name).write_bytes(data)
        print(f"  取得 {dst / name}  ({len(data) / 1024:.0f} KB)")
    print(f"\n✅ {len(r['files'])}枚。{dst} を拡大して見てください。")


@app.local_entrypoint()
def gpus(kinds: str = "T4,L4,A10G", samples: int = 32, res: int = 1920):
    """🔴 どのGPUが「1コマあたり」いちばん安いかを実測で決める。

    時間単価が安いGPUが得とはかぎらない。T4 は 2018年の世代で
    レイトレ専用回路が弱く、単価は安いが遅い。L4（2023年）は単価が1.4倍でも
    3倍速ければ、1コマあたりでは 2倍以上安くなる。ここは実測でしか決まらない。
    """
    FRAMES_3D = 8742
    PRICE = {"T4": 0.59, "L4": 0.80, "A10G": 1.10, "A100": 2.10, "L40S": 1.95}

    rows = []
    for g in [k.strip() for k in kinds.split(",") if k.strip()]:
        print(f"\n=== {g} ===")
        try:
            r = bench_all.with_options(gpu=g).remote([samples], res)
        except Exception as e:                                   # noqa: BLE001
            print(f"  {g}: 起動できず {type(e).__name__}: {e}")
            continue
        if r and r[0].get("ok"):
            rows.append((g, r[0]["spf"], r[0].get("devices")))

    print("\n" + "=" * 78)
    print(f"  GPU別の1コマ単価（Cycles/OptiX {samples}サンプル / {res}px / "
          f"本編3D {FRAMES_3D:,}コマ）")
    print("=" * 78)
    print(f"  {'GPU':>6} | {'$/時':>6} | {'秒/コマ':>8} | {'GPU時間':>8} | "
          f"{'費用':>8} | {'円':>8}")
    print("  " + "-" * 74)
    best = None
    for g, spf, dev in rows:
        ph = PRICE.get(g, 0.0)
        h = FRAMES_3D * spf / 3600
        usd = h * ph
        if best is None or usd < best[1]:
            best = (g, usd, spf)
        print(f"  {g:>6} | {ph:>6.2f} | {spf:>8.2f} | {h:>8.2f} | "
              f"{'$' + format(usd, '.2f'):>8} | {'¥' + format(usd * 160, ',.0f'):>8}")
    if best:
        print("  " + "-" * 74)
        print(f"  → 最安は {best[0]}：{best[2]:.2f}秒/コマ・"
              f"${best[1]:.2f}（約¥{best[1] * 160:,.0f}）")
    print("=" * 78)


@app.local_entrypoint()
def floor(gpu: str = "L4"):
    """固定費（サンプル数に関係なくかかる時間）の正体を切り分ける。

    ⚠️ 全ケースを**1つのコンテナ**で連続実行する。別コンテナに分けると
       機体差（実測で±20%）が効果の差より大きく出て、比較にならない。
    """
    FRAMES_3D = 8742
    PRICE = {"T4": 0.59, "L4": 0.80, "A10G": 1.10}
    price = PRICE.get(gpu, 0.80)
    fn = bench_all.with_options(gpu=gpu)

    cases = [
        ("デノイズCPU 1920px", dict(res=1920, denoiser="oidn_cpu")),
        ("★デノイズGPU 1920px", dict(res=1920, denoiser="oidn_gpu")),
        ("★OptiXデノイザ 1920px", dict(res=1920, denoiser="optix")),
        ("デノイズ無し 1920px", dict(res=1920, denoise=False)),
        ("★デノイズGPU 1280px", dict(res=1280, denoiser="oidn_gpu")),
        ("★デノイズGPU 960px", dict(res=960, denoiser="oidn_gpu")),
        ("★デノイズGPU 640px", dict(res=640, denoiser="oidn_gpu")),
    ]
    rows = []
    for label, kw in cases:
        res = kw.pop("res")
        r = fn.remote([32], res, **kw)
        rows.append((label, r[0]["spf"] if (r and r[0].get("ok")) else None))

    print("\n" + "=" * 74)
    print(f"  固定費の切り分け（Cycles/OptiX 32サンプル / {gpu} / 本編3D {FRAMES_3D:,}コマ）")
    print("=" * 74)
    base = rows[0][1]
    for label, spf in rows:
        if spf is None:
            print(f"  {label:<22} 失敗")
            continue
        usd = FRAMES_3D * spf / 3600 * price
        delta = f"（既定比 {spf / base * 100:>5.0f}%）" if base else ""
        print(f"  {label:<22} {spf:>6.2f} 秒/コマ  "
              f"${usd:>6.2f}（約¥{usd * 160:>6,.0f}）{delta}")
    print("=" * 74)


@app.local_entrypoint()
def bench(samples: str = "1,8,16,32,64,128", res: int = 1920):
    """同一コンテナでサンプル数を振り、画質と費用の折れ目を出す。"""
    FRAMES_3D = 8742
    USD_PER_HOUR = 0.59
    rows = bench_all.remote([int(x) for x in samples.split(",") if x.strip()], res)

    print("\n" + "=" * 70)
    print(f"  Cycles サンプル数と費用（同一T4 / {res}px / 本編3D {FRAMES_3D:,}コマ）")
    print("=" * 70)
    print(f"  {'samples':>8} | {'秒/コマ':>8} | {'GPU時間':>8} | {'費用':>9} | {'円':>9}")
    print("  " + "-" * 66)
    ok = [r for r in rows if r.get("ok")]
    for r in ok:
        h = FRAMES_3D * r["spf"] / 3600
        usd = h * USD_PER_HOUR
        print(f"  {r['samples']:>8} | {r['spf']:>8.2f} | {h:>8.2f} | "
              f"{'$' + format(usd, '.2f'):>9} | {'¥' + format(usd * 160, ',.0f'):>9}")
    for r in rows:
        if not r.get("ok"):
            print(f"  {r['samples']:>8} | 失敗 {str(r.get('stderr'))[-200:]}")
    if ok:
        floor = min(r["spf"] for r in ok)
        top = max(r["spf"] for r in ok)
        print("  " + "-" * 66)
        print(f"  最速 {floor:.2f}秒 / 最遅 {top:.2f}秒 → 差は {top - floor:.2f}秒。")
        print("  差が小さいなら、時間を決めているのはサンプル数ではなく")
        print("  デノイズと起動の固定費。その場合はサンプルを上げても費用はほぼ増えない。")
    print("=" * 70)


@app.local_entrypoint()
def sweep(samples: str = "8,16,32,64", res: int = 1920):
    """Cycles のサンプル数を振って、画質と費用の折れ目を探す。

    Cycles は「サンプル数」＝光を何本飛ばすかで時間が決まる。
    デノイズ（ノイズ取り）を効かせれば少ないサンプルでも見られる絵になるので、
    どこまで落とせるかを実測で決める。参照chの絵はフラットで陰影が単純なため、
    低サンプルでも破綻しにくいはず。
    """
    FRAMES_3D = 8742          # 本編の3D差し替えぶん（582.8秒 × 15fps）
    USD_PER_HOUR = 0.59       # T4
    rows = []
    for s in [int(x) for x in samples.split(",") if x.strip()]:
        r = smoke.remote(engine="cycles", res=res, samples=s)
        if r.get("ok"):
            rows.append((s, r["sec_per_frame"]))
            print(f"  samples={s:3d} -> {r['sec_per_frame']:.2f} 秒/コマ")
        else:
            print(f"  samples={s:3d} -> 失敗 {str(r.get('stderr'))[-300:]}")

    print("\n" + "=" * 66)
    print(f"  Cycles サンプル数と費用（{res}px / 本編3D {FRAMES_3D:,}コマ）")
    print("=" * 66)
    print(f"  {'samples':>8} | {'秒/コマ':>8} | {'GPU時間':>8} | {'費用':>9} | {'円':>8}")
    print("  " + "-" * 62)
    for s, spf in rows:
        h = FRAMES_3D * spf / 3600
        usd = h * USD_PER_HOUR
        print(f"  {s:>8} | {spf:>8.2f} | {h:>8.2f} | {'$' + format(usd, '.2f'):>9} "
              f"| {'¥' + format(usd * 160, ',.0f'):>8}")
    print("=" * 66)


@app.local_entrypoint()
def main(engines: str = "eevee,cycles", diagnose: bool = True):
    """EEVEE と Cycles を1回ずつ焼いて、1コマ何秒かを表で出す。"""
    if diagnose:
        print("=== GPUがどう渡っているかを先に確かめます ===")
        probe.remote()
        print()

    results = []
    for e in [x.strip() for x in engines.split(",") if x.strip()]:
        print(f"\n=== {e} を試します ===")
        results.append(smoke.remote(engine=e))

    print("\n" + "=" * 62)
    print("  スモークテスト結果")
    print("=" * 62)
    for r in results:
        if not r.get("ok"):
            print(f"  {r['engine']:8s} : ❌ 失敗（returncode={r.get('returncode')}）")
            print(f"             {str(r.get('stderr', ''))[-600:]}")
            continue
        spf = r["sec_per_frame"]
        gpu = r.get("gpu", {})
        egl = r.get("egl_errors", 0)
        mark = "⚠️ 要注意" if egl else "✅"
        print(f"  {r['engine']:8s} : {mark} {spf:.2f} 秒/コマ   "
              f"（初回 {r['sec_per_frame_first']:.2f}秒 / Blender {r['blender']}）")
        print(f"             GPU: {gpu.get('renderer')} / {gpu.get('backend')}")
        if egl:
            print(f"             🔴 EGLエラー {egl}件。GPUを掴めずソフト描画に"
                  f"落ちている可能性が高い（絵は出るが桁違いに遅い）")
        # 本編の3D差し替えぶん（582.8秒 × 15fps = 8,742コマ）に当てはめる
        hours = 8742 * spf / 3600
        usd = hours * 0.59
        print(f"             → 本編3D 8,742コマ = {hours:.2f} GPU時間 "
              f"= ${usd:.2f}（約¥{usd * 160:.0f}）")
    print("=" * 62)
