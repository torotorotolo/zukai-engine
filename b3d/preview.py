# -*- coding: utf-8 -*-
"""潜水艇タイタンを3カットだけ本焼きして、拡大目視にかける。

■ なぜ3カットで止めるのか
  設計レビューで「ビルダーの形状バグは、28本焼いたあとにまとめて発覚する」と
  指摘された。66カット焼いてから形の狂いに気づくと全部やり直しになる。
  **1モデル＝約35カットぶん**を背負っているので、ここで形を固める。

  カズヤくんの作法「直したら5回以上精査する」に合わせ、
  この3枚を拡大して直す→また焼く、を繰り返す想定。1巡あたり約¥5。

■ 焼く3枚
  1 exterior     … 深海のヒーローショット（c107 / pr01 相当）
  2 hull_layers  … 炭素繊維5層。剥離した層を朱赤で（c416 / c431 相当）
  3 cutaway      … 断面。中の空間と層の重なり（c308 / c625 相当）

    blender -b --factory-startup -P b3d/preview.py -- --out /out --res 1920
"""
import os
import sys
import time
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib as L                                                    # noqa: E402
from builders import sub_titan                                     # noqa: E402

ARGV = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    k = "--" + name
    return ARGV[ARGV.index(k) + 1] if (k in ARGV and ARGV.index(k) + 1 < len(ARGV)) else default


OUT = arg("out", "/out")
RES = int(arg("res", "1920"))
SAMPLES = int(arg("samples", "32"))
os.makedirs(OUT, exist_ok=True)


# ── 3つの見え方 ────────────────────────────────────────────────
SHOTS = [
    dict(
        name="1_exterior",
        note="深海のヒーローショット。参照chの冒頭と同じ位置づけ",
        mode="exterior", world="deep_sea",
        cam=dict(azimuth=38, elevation=8, distance=13.5, lens=52),
        light=dict(energy=9000, loc=(6.5, -8.5, 4.5), spot=True, size=1.25),
    ),
    dict(
        name="2_hull_layers",
        note="炭素繊維5層。3層目を剥離させて朱赤で見せる",
        mode="hull_layers", highlight=(3,), world="studio",
        cam=dict(azimuth=62, elevation=16, distance=7.4, lens=60),
        light=dict(energy=1200, loc=(4, -5, 5), spot=False),
    ),
    dict(
        name="3_cutaway",
        note="断面。中の空間の狭さと、層の重なりを同時に見せる",
        mode="cutaway", highlight=(3,), world="studio",
        cam=dict(azimuth=118, elevation=14, distance=7.0, lens=58),
        light=dict(energy=1500, loc=(-4, -5, 5), spot=False),
    ),
]


def render_one(shot):
    sc = L.setup_scene(RES, int(RES * 9 / 16), samples=SAMPLES, denoise=True)

    # 🔴 順番が命：世界 → 物 → 光 → カメラ。
    #    光を物より先に置くと TRACK_TO の相手が居らず、真下を向いたまま気づけない。
    if shot["world"] == "deep_sea":
        L.deep_sea(sc)
    else:
        L.studio(sc)

    root = sub_titan.build(mode=shot["mode"], highlight=shot.get("highlight", ()))

    L.key_light(root, **shot["light"])
    L.fill_light(root, energy=180.0)
    L.camera(sc, root, **shot["cam"])

    sc.render.filepath = os.path.join(OUT, f"titan_{shot['name']}.png")
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t0
    print(f"[preview] {shot['name']}: {dt:.2f}s  ({shot['note']})")
    return dt


def main():
    total = 0.0
    for s in SHOTS:
        total += render_one(s)
    print(f"[preview] 3枚 合計 {total:.2f}秒  平均 {total / len(SHOTS):.2f}秒/コマ")
    print(f"[RESULT] {{\"frames\": {len(SHOTS)}, \"total_sec\": {total:.2f}}}")


if __name__ == "__main__":
    main()
