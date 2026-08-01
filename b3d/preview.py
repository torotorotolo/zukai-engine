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
# 🔴 distance は書かない。対象の大きさから自動で決める（L.camera の fill）。
#    2巡目は distance=3.6 を手で置いて対象を突き抜けた。
#    fill … 対象が画面の短辺に占める割合。0.78 なら余白2割強。
SHOTS = [
    dict(
        name="1_exterior",
        note="深海のヒーローショット。参照chの冒頭と同じ位置づけ",
        mode="exterior", world="deep_sea",
        cam=dict(azimuth=34, elevation=7, lens=85, fill=0.80),
        light=dict(energy=14000, loc=(7.0, -9.0, 5.0), spot=True, size=1.30),
        fill_light=420.0,
    ),
    dict(
        name="2_hull_layers",
        note="炭素繊維5層＋接着面4つの模式図。3層目が剥離（c414/c416/c428）",
        mode="hull_layers", highlight=(3,), world="studio",
        cam=dict(azimuth=76, elevation=13, lens=75, fill=0.84),
        light=dict(energy=1600, loc=(3.0, 5.0, 4.5), spot=False, size=6.0),
        fill_light=700.0,
    ),
    dict(
        name="3_cutaway",
        note="耐圧殻の半割り。5人が座る狭さと壁の厚みを同時に（c107/c204/c308）",
        mode="cutaway", highlight=(3,), world="studio",
        cam=dict(azimuth=18, elevation=17, lens=68, fill=0.84),
        light=dict(energy=1800, loc=(6.0, -4.0, 5.0), spot=False, size=8.0),
        fill_light=300.0, inside=150.0, inside_at=(0.45, 0.0, 0.52),
    ),
    dict(
        name="4_hull",
        note="耐圧殻の外観。継ぎ目リングとボルト18本（c204/c205/c417）",
        mode="hull", world="studio",
        cam=dict(azimuth=52, elevation=11, lens=80, fill=0.80),
        light=dict(energy=1700, loc=(5.0, -6.0, 4.5), spot=False, size=8.0),
        fill_light=600.0,
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
    L.fill_light(root, energy=shot.get("fill_light", 200.0))
    if shot.get("inside"):
        L.inside_light(root, energy=shot["inside"],
                       offset=shot.get("inside_at", (0.0, 0.0, 0.5)))
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
