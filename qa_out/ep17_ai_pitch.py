# -*- coding: utf-8 -*-
"""17本目 ⑥ サムネ：生成 AI の地（案A）の機体の機首の角度を、実際の約52.6度（報告書・台本 第7章「52.6度」）に合わせる。

なぜ：案A は「機首上げ 約50度」と指示したのに、描かれた機体は約25度（ふつうの離陸の上昇に近い）＝10-21 カズヤくん
     「実際の 52.6度の異様さを出してほしい」。生成のやり直し（課金）の前に、絵を回して合わせる（無料・角度を数で決められる）。
⚠️ 角度の物差し：明るい白の点の主成分は 18.6度と出た＝胴体の前半の光った所に偏る（翼・エンジンの照り）。
   → **機首の先と胴体の後ろの端（尾の円すい）の2点**で測る（1280×720 の絵で目で取った点＝NOSE・TAIL・原寸は ×1.4）。
やること：
  ① 地平線より下（街と滑走路の灯り）を、その列の空の色で塗る（回すと地面が斜めになって嘘の絵になるため）
  ② 機体の真ん中（2点の中点）を軸に、52.6度との差だけ反時計回りに回す（角は空の色）
  ③ 回した機体が画面の縦に収まるように縮め、まわりを空の色で埋める（空は一様な紺＝継ぎ目が出にくい）
⚠️ 生成の絵＝再現のイメージ（概要欄に断る）。回したのは角度を記録に合わせるため（事実へ寄せる直し）

    python qa_out/ep17_ai_pitch.py   → ref/ep17/ai/ep17_cal_a_p526_orig.png・ep17_cal_a_p526.jpg（1280×720）
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
SRC = HERE / "ref" / "ep17" / "ai" / "ep17_cal_a_orig.png"
OUT = HERE / "ref" / "ep17" / "ai"
TARGET = 52.6          # 報告書の最大の機首の角度（台本 第7章）
HORIZON = 0.78         # 地平線（街の灯りの始まり）＝高さの割合
NOSE, TAIL = (1118, 112), (258, 515)     # 1280×720 の絵で取った機首の先・胴体の後ろの端
FIT = 0.86             # 回した機体の縦の長さを、画面の高さのこの割合に収める
CENTER = (0.52, 0.50)  # 縮めたあとの機体の真ん中の置き場所（幅・高さの割合）


def main():
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    k = W / 1280
    nx, ny = NOSE[0] * k, NOSE[1] * k
    tx, ty = TAIL[0] * k, TAIL[1] * k
    ang0 = math.degrees(math.atan2(ty - ny, nx - tx))
    L = math.hypot(nx - tx, ny - ty)
    cx, cy = (nx + tx) / 2, (ny + ty) / 2
    print(f"元の絵 {W}×{H}：機首の先と後ろの端の2点で測った軸 {ang0:.1f}度・長さ {L:.0f}px・真ん中 ({cx:.0f}, {cy:.0f})")
    a = np.asarray(im).astype(np.int16)
    yh = int(H * HORIZON)
    sky_row = a[yh - 30:yh - 10].mean(axis=0)
    b = a.copy()
    b[yh:, :, :] = sky_row[None, :, :]
    fill = tuple(int(x) for x in np.median(a[: int(H * 0.15)].reshape(-1, 3), axis=0))
    rot = TARGET - ang0
    out = Image.fromarray(b.astype(np.uint8)).rotate(rot, resample=Image.BICUBIC, center=(cx, cy), fillcolor=fill)
    # ③ 回した機体の縦の長さ＝L·sin(52.6)（翼の張り出しは別）→ 画面の FIT に縮める
    s = min(1.0, FIT * H / (L * math.sin(math.radians(TARGET))))
    small = out.resize((round(W * s), round(H * s)), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), fill)
    ox, oy = round(CENTER[0] * W - cx * s), round(CENTER[1] * H - cy * s)
    canvas.paste(small, (ox, oy))
    # 縮めた絵の外の縁（空の色の継ぎ目）が出ないよう、元の空の色で埋めてあることを数で見る
    edge = np.asarray(canvas).astype(np.int16)
    print(f"回した角度 {rot:+.1f}度（反時計回り）→ 機体の軸 {TARGET}度・縮め {s:.2f}倍・置き場所 ({ox}, {oy})・空の色 {fill}・"
          f"四隅の色 {[tuple(edge[y, x]) for y, x in ((5, 5), (5, W - 6), (H - 6, 5), (H - 6, W - 6))]}")
    canvas.save(OUT / "ep17_cal_a_p526_orig.png")
    canvas.resize((1280, 720), Image.LANCZOS).save(OUT / "ep17_cal_a_p526.jpg", "JPEG", quality=94)
    nose2 = (CENTER[0] * W + (nx - cx) * s * math.cos(math.radians(rot)) + (ny - cy) * s * math.sin(math.radians(rot)),
             CENTER[1] * H - (nx - cx) * s * math.sin(math.radians(rot)) + (ny - cy) * s * math.cos(math.radians(rot)))
    print(f"機首の先の置き場所（原寸）≈ ({nose2[0]:.0f}, {nose2[1]:.0f})")
    print("→ ref/ep17/ai/ep17_cal_a_p526_orig.png・ep17_cal_a_p526.jpg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
