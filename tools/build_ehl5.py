# -*- coding: utf-8 -*-
"""EHL5テストの合成。背景1枚＋キャラ変種8枚から30fpsのコマを作る。

Chrome を使わず PIL だけで回すので、コマ数を増やしても起動コストが増えない。
参考動画の実測（Vault 参考-EHL5秒単位分解-20260729）に合わせて：
  ・背景は不動。**ズームなし**
  ・カメラのパンは7秒で3〜14px 程度の極小のみ
  ・キャラは呼吸で上下し、口パクとまばたきが常時入る（ほぼフル30fps）
"""
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image

import scene_ehl5 as S

FPS = 30
OUT = S.HERE / "out" / "ehl5"
FR = OUT / "frames"


def variants(name, CW, CH):
    """変種グリッドを8枚に切り出す。"""
    im = Image.open(OUT / f"ch_{name}.png").convert("RGBA")
    cols = 4
    return [im.crop(((i % cols) * CW, (i // cols) * CH,
                     (i % cols) * CW + CW, (i // cols) * CH + CH))
            for i in range(len(S.VARIANTS))]


def mouth_index(t):
    """口パク。母音の切り替わりに見えるよう、等間隔にせず3段でばらす。"""
    k = int(t * 7.5)
    return [0, 2, 1, 3, 1, 2, 0, 3, 2, 1][k % 10]


def blinking(t, phase=0.0):
    """3.4秒に1回、0.12秒だけ閉じる。"""
    u = (t + phase) % 3.4
    return u < 0.12


def build():
    FR.mkdir(parents=True, exist_ok=True)
    n = 0
    for ci, name in enumerate(S.CUTS):
        bg = Image.open(OUT / f"bg_{name}.png").convert("RGBA")
        _, CW, CH, pos, _ = S.cut_layers(name)
        vs = variants(name, CW, CH)
        total = int(S.SEC * FPS)
        # 極小のパン。カットごとに向きを変える（実測では半数のカットに数pxだけ入る）
        pan = [(0, 0), (-10, 0), (7, -3)][ci]
        for f in range(total):
            t = f / FPS
            u = f / (total - 1)
            fr = bg.copy()
            if pan != (0, 0):
                fr = fr.transform(fr.size, Image.AFFINE,
                                  (1, 0, -pan[0] * u, 0, 1, -pan[1] * u),
                                  resample=Image.BILINEAR)
            mi = mouth_index(t)
            bi = 1 if blinking(t) else 0
            cell = vs[bi * len(S.MOUTHS) + mi]
            # 呼吸。上半身が2〜6px上下する程度に留める（大きいと跳ねて見える）
            dy = round(math.sin(t * math.tau / 3.1) * 5)
            dx = round(math.sin(t * math.tau / 4.7) * 2)
            fr.alpha_composite(cell, (pos[0] + dx, pos[1] + dy))
            fr.convert("RGB").save(FR / f"{n:05d}.jpg", quality=93)
            n += 1
        print(f"cut {name}: {total} frames")
    print("total frames", n)
    return n


if __name__ == "__main__":
    n = build()
    mp4 = OUT / "ehl5_test.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-framerate", str(FPS), "-i", str(FR / "%05d.jpg"),
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "19", "-movflags", "+faststart", str(mp4)], check=True)
    print("wrote", mp4, round(n / FPS, 1), "sec")
