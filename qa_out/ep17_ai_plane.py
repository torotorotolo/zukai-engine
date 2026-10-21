# -*- coding: utf-8 -*-
"""17本目 ⑥ サムネ：生成 AI の地（案A）の機体を空から切り抜いて 52.6度に回し、①継ぎ目の無い夜空の地 と ②字の手前に重ねる機体（透明つき PNG）を作る。

なぜ：`ep17_ai_pitch.py` は絵ぜんたいを回した＝空の縦の階調が斜めになり、回した四角の縁に色の継ぎ目が出た。さらに H 型の反転版
     （字の外だけカラー）では機体が字の後ろに隠れ、210px で飛行機と分からない（10-21 カズヤくん「実際の 52.6度の異様さを出してほしい」）。
やること：
  ① 空の色を行ごとに左右の端（機体の無い所）から取り、空との色の距離で機体の型（マスク）を作る（中の窓の穴は埋める・小さな点は捨てる）
  ② 機首の先と胴体の後ろの端の2点（`ep17_ai_pitch.NOSE/TAIL`）の軸 25.1度 → 52.6度へ回し、画面の縦に収まるよう縮める
  ③ 地＝なめらかな縦の階調の夜空＋回した機体（継ぎ目なし）／重ね＝回した機体だけの透明つき PNG（1280×720 の座標）
⚠️ 生成の絵＝再現のイメージ（概要欄に断る）。回したのは角度を記録（約52.6度）に合わせるため

    python qa_out/ep17_ai_plane.py  → ref/ep17/ai/ep17_cal_a_p526c.jpg（地）・ep17_cal_a_p526_plane.png（重ね）
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "qa_out"))
sys.stdout.reconfigure(encoding="utf-8")
import ep17_ai_pitch as P  # noqa: E402

SRC = P.SRC
OUT = P.OUT
TH = 30.0              # 空との色の距離（RGB）がこれを超えたら機体


def main():
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    a = np.asarray(im).astype(np.float32)
    yh = int(H * P.HORIZON)
    # ① 行ごとの空の色＝左右の端 70px の中央値（機体は端に届かない）
    edge = np.concatenate([a[:, :70], a[:, -70:]], axis=1)
    sky = np.median(edge, axis=1)                              # H×3
    d = np.sqrt(((a - sky[:, None, :]) ** 2).sum(axis=2))
    m = (d > TH)
    m[yh:, :] = False
    # 穴を埋める（窓・エンジンの口）＝外から塗って届かない所が穴
    mi = Image.fromarray((m * 255).astype(np.uint8))
    ff = mi.copy()
    ImageDraw.floodfill(ff, (0, 0), 128)
    holes = np.asarray(ff) == 0
    m = m | holes
    # 小さな点（星・灯り）を捨てる＝機体の外接の箱の外は捨てる
    k = W / 1280
    nx, ny, tx, ty = P.NOSE[0] * k, P.NOSE[1] * k, P.TAIL[0] * k, P.TAIL[1] * k
    x0, x1 = int(min(nx, tx) - 200 * k), int(max(nx, tx) + 120 * k)
    y0, y1 = int(min(ny, ty) - 120 * k), int(max(ny, ty) + 120 * k)
    box = np.zeros_like(m)
    box[max(0, y0):y1, max(0, x0):x1] = True
    m = m & box
    print(f"機体の型の点 {int(m.sum())}（画面の {m.mean() * 100:.1f}%）・穴を埋めた {int(holes.sum())}")
    alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)
    # ② 回す・縮める（ep17_ai_pitch と同じ値）
    ang0 = math.degrees(math.atan2(ty - ny, nx - tx))
    L = math.hypot(nx - tx, ny - ty)
    cx, cy = (nx + tx) / 2, (ny + ty) / 2
    rot = P.TARGET - ang0
    s = min(1.0, P.FIT * H / (L * math.sin(math.radians(P.TARGET))))
    r = rgba.rotate(rot, resample=Image.BICUBIC, center=(cx, cy))
    r = r.resize((round(W * s), round(H * s)), Image.LANCZOS)
    plane = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ox, oy = round(P.CENTER[0] * W - cx * s), round(P.CENTER[1] * H - cy * s)
    plane.alpha_composite(r, (ox, oy))
    # ③ 地＝なめらかな縦の階調（上＝元の空の上の端の色・下＝地平線の少し上の色）
    top, bot = sky[: int(H * 0.08)].mean(axis=0), sky[yh - 40: yh - 10].mean(axis=0)
    t = np.linspace(0, 1, H)[:, None, None]
    grad = (top[None, None, :] * (1 - t) + bot[None, None, :] * t).repeat(W, axis=1)
    ground = Image.fromarray(grad.astype(np.uint8), "RGB").convert("RGBA")
    ground.alpha_composite(plane)
    g = ground.convert("RGB").resize((1280, 720), Image.LANCZOS)
    g.save(OUT / "ep17_cal_a_p526c.jpg", "JPEG", quality=94)
    plane.resize((1280, 720), Image.LANCZOS).save(OUT / "ep17_cal_a_p526_plane.png")
    print(f"回した角度 {rot:+.1f}度・縮め {s:.2f}倍・空の上 {tuple(int(x) for x in top)}・下 {tuple(int(x) for x in bot)}")
    print("→ ref/ep17/ai/ep17_cal_a_p526c.jpg（地）・ep17_cal_a_p526_plane.png（重ね）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
