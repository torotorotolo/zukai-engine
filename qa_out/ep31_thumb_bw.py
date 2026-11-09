# -*- coding: utf-8 -*-
"""31本目 ⑥ サムネ：生成の地 A（szk_a）を「1971年の白黒の写真」の質感に加工する（費用 0・生成し直す前の段）。
11-09 カズヤくん「サムネの写真変更」「当時の写真の質感を再現するように、白黒で作成」「色だけでなく質感も」。
地の切り出しは決めの「① 1.15倍」（`ep31_thumb_hx.py zooms` の z115）と同じ式を、生成の原寸（1792×1008）から先に当てて 1280×720 にし、
その大きさで質感を足す（粒の大きさを出来上がりの画素で決める＝あとで拡大して粒がぼけない）。

質感の部品（色を抜くだけでは当時の写真にならない）
  ① 白黒フィルムの感じ方＝赤 0.24・緑 0.58・青 0.18（目の明るさより青をやや明るく＝パンクロのフィルムの寄り）
  ② レンズの甘さ（ぼかし）と、明るい所のにじみ（ハレーション＝明るい所をぼかして重ねる）
  ③ 焼き付けの階調＝コントラストを上げ、黒は浮かせ・白は沈める（紙の写真の黒と白）
  ④ 周辺の暗さ（レンズの周辺光量の落ち）
  ⑤ フィルムの粒＝中間の明るさで強い（粒の径は一覧の 640px で潰れない大きさ）／強めの段は、ほこりの点と細い傷
    python -P qa_out/ep31_thumb_bw.py   → ref/ep31/ai/ep31_szk_a_bw1.jpg（控えめ）・ep31_szk_a_bw2.jpg（強め）
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
AI = HERE / "ref" / "ep31" / "ai"
W, H = 1280, 720
Z115 = dict(zoom=1.15, cx=round(152 / (W - W / 1.15), 3), cy=0.0)     # 決めの寄せ（ep31_thumb_hx.py の final と同じ値）

STEPS = {
    "bw1": dict(grain=9.0, gsig=1.3, contrast=1.20, black=22, white=232, soft=0.9, halo=0.15, vig=0.15, dust=0, scratch=0),
    "bw2": dict(grain=14.0, gsig=1.7, contrast=1.35, black=30, white=226, soft=1.2, halo=0.25, vig=0.25, dust=30, scratch=2),
}
# 🔧 1回目（bw1・bw2）は粒が強すぎた＝空が砂嵐のような雑音（式の ×2 が効きすぎ）→ 粒を半分以下・塊をやや大きく・
#    空を明るく（青の重み）・紙の写真の S 字の階調・白い機体のにじみ。2段＝自然な写真／当時の新聞の写真寄り（コントラスト強め）
STEPS2 = {
    "bw3": dict(grain=4.0, gsig=1.5, contrast=1.30, black=16, white=238, soft=1.1, halo=0.22, vig=0.20, dust=0, scratch=0,
                mix=(0.20, 0.50, 0.30), scurve=0.35),
    "bw4": dict(grain=5.5, gsig=1.8, contrast=1.45, black=12, white=232, soft=1.3, halo=0.28, vig=0.26, dust=12, scratch=1,
                mix=(0.20, 0.50, 0.30), scurve=0.55),
}


def crop_like_photo(im, zoom, cx, cy):
    """thumb_jiko.photo と同じ式（箱いっぱい・寄せ・横と縦の寄せ）"""
    z = max(W / im.width, H / im.height) * zoom
    cw, ch = min(im.width, W / z), min(im.height, H / z)
    l, t = (im.width - cw) * cx, (im.height - ch) * cy
    return im.crop((round(l), round(t), round(l + cw), round(t + ch))).resize((W, H), Image.LANCZOS)


def film(im, grain, gsig, contrast, black, white, soft, halo, vig, dust, scratch, seed=31,
         mix=(0.24, 0.58, 0.18), scurve=0.0, gmul=2.0):
    a = np.asarray(im.convert("RGB")).astype(float) / 255
    g = a[..., 0] * mix[0] + a[..., 1] * mix[1] + a[..., 2] * mix[2]               # ①
    g = ndimage.gaussian_filter(g, soft)                                              # ② 甘さ
    hl = np.clip((g - 0.70) / 0.30, 0, 1)
    g = 1 - (1 - g) * (1 - halo * ndimage.gaussian_filter(hl, 6 if not scurve else 8))   # ② にじみ
    g = np.clip(0.5 + (g - 0.5) * contrast, 0, 1)                                     # ③ コントラスト
    if scurve:
        g = g + scurve * (g * g * (3 - 2 * g) - g)                                    # ③ 紙の写真の S 字（肩と足）
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / np.sqrt(2)
    g = g * (1 - vig * r ** 2)                                                        # ④
    rng = np.random.default_rng(seed)
    n = ndimage.gaussian_filter(rng.normal(0, 1, (H, W)), gsig)
    n /= n.std()
    g = g + n * (grain / 255) * (0.6 + 1.6 * g * (1 - g)) * gmul                      # ⑤ 粒（中間で強い）
    if dust:
        for _ in range(dust):
            y, x = rng.integers(0, H), rng.integers(0, W)
            rr = rng.uniform(0.8, 2.2)
            m = (yy - y) ** 2 + (xx - x) ** 2 <= rr * rr
            g[m] = g[m] * 0.3 + (0.95 if rng.random() < 0.6 else 0.05) * 0.7       # 白い点（焼き付けのほこり）と黒い点
    for _ in range(scratch):
        x0 = int(rng.integers(80, W - 80))
        xs = (x0 + np.cumsum(rng.normal(0, 0.15, H))).astype(int).clip(0, W - 1)
        g[np.arange(H), xs] = np.clip(g[np.arange(H), xs] + 0.18, 0, 1)             # 縦の細い傷（薄く）
    g = black / 255 + np.clip(g, 0, 1) * (white - black) / 255                         # ③ 焼き付けの黒と白
    out = (np.clip(g, 0, 1) * 255).round().astype(np.uint8)
    return Image.fromarray(out, "L").convert("RGB")


# 🆕 11-09 カズヤくん（白黒で生成し直した2案を見て）「案①をもっと荒い質感に編集」＝生成 案①（szk_c・もう白黒）に粒・ほこり・傷・階調を足す3段。
#    粒は「塊」で（gsig を大きく）＝1回目の bw1・bw2 の失敗（細かい雑音を強くしただけ＝砂嵐）を繰り返さない。切り出しは案①のまま（zoom 1.0）
STEPS_C = {
    "r1": dict(grain=6.0, gsig=1.6, contrast=1.10, black=14, white=240, soft=0.4, halo=0.10, vig=0.10, dust=15, scratch=1, scurve=0.25),
    "r2": dict(grain=9.0, gsig=1.9, contrast=1.18, black=18, white=236, soft=0.6, halo=0.14, vig=0.16, dust=30, scratch=2, scurve=0.35),
    "r3": dict(grain=13.0, gsig=2.3, contrast=1.28, black=24, white=230, soft=0.8, halo=0.18, vig=0.22, dust=50, scratch=3, scurve=0.45),
}


def main_c():
    src = Image.open(AI / "ep31_szk_c_orig.png").convert("RGB")
    base = crop_like_photo(src, zoom=1.0, cx=0.5, cy=0.5)
    for k, kw in STEPS_C.items():
        dst = AI / f"ep31_szk_c_{k}.jpg"
        film(base, gmul=1.0, **kw).save(dst, "JPEG", quality=95)
        print(f"  {dst.name}: {kw}")


def main():
    if "c" in sys.argv[1:]:
        return main_c()
    src = Image.open(AI / "ep31_szk_a_orig.png").convert("RGB")
    base = crop_like_photo(src, **Z115)
    for k, kw in list(STEPS.items()) + [(k, dict(v, gmul=1.0)) for k, v in STEPS2.items()]:
        dst = AI / f"ep31_szk_a_{k}.jpg"
        film(base, **kw).save(dst, "JPEG", quality=95)
        print(f"  {dst.name}: {kw}")


if __name__ == "__main__":
    main()
