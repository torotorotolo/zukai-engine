# -*- coding: utf-8 -*-
"""31本目 ⑥ サムネ：生成の地（szk_a・szk_b）の2機を空から切り抜き、字の手前に重ねる透明つき PNG を作る
（17本目 `ep17_ai_plane.py` の考え方＝空との違いで機体の型を取る）。

なぜ：11-09 カズヤくん「背景の写真の存在感が薄いので、もっと大きく表示。もしくはもっとインパクトのある画像を生成」。
     H 反転版は字の中が暗い白黒＝大きな「雫石」が真ん中の帯をほぼ全部ふさぎ、2機は字の後ろ（暗い側）に隠れる。
     寄せる（1.35倍など）と、2機が横いっぱいに並んでいるので機首か戦闘機が画面の外へ切れる → 機体だけを字の手前・上下の行の奥に出す。
やること：
  ① 空（青・色の濃い画素）でない画素のつながりのうち、画面の下の端に触れない大きな塊＝機体の種（雲と山は下の端に触れる）
  ② GrabCut（OpenCV）で種のまわりを詰める（確かな空と下の雲の塊＝背景・種の芯＝前景）
  ③ 穴を埋め・小さな塊を捨て・縁を 1.2px ぼかす → ref/ep31/ai/ep31_szk_{a,b}_plane.png（1280×720・透明つき）
  ④ 確かめの並べ（左＝地に赤い輪郭・右＝市松の上の切り抜き）→ out/thumb/ep31/chk31_plane.png
    python -P qa_out/ep31_thumb_plane.py
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
AI = HERE / "ref" / "ep31" / "ai"
OUT = HERE / "out" / "thumb" / "ep31"
MIN_AREA = 1500
# 🔧 1回目（下の端に触れない塊＝種）は A で2機とも取れなかった（機体の下の白いかすみが雲までつながり、下の端の塊に入った）・
#    B は雲のかけら4つが種に混ざった → 機体ごとに囲む枠（x0, y0, x1, y1）を決め、枠の中だけを切り抜く。
#    枠＝並べ（cmp31_hinv2 の生の地）で見た位置と、B の1回目の種（旅客機 x355〜1261・y152〜356／戦闘機 x55〜348・y155〜453）から
RECTS = {
    "a": {"戦闘機": (50, 100, 300, 360), "旅客機": (280, 210, 1279, 432)},
    "b": {"戦闘機": (35, 130, 372, 472), "旅客機": (330, 130, 1279, 382)},
}


def cut(g):
    src = AI / f"ep31_szk_{g}.jpg"
    img = cv2.imread(str(src))
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    sky = (H >= 88) & (H <= 135) & (S >= 70) & (V >= 70)
    keep = np.zeros((h, w), bool)
    for nm, (x0, y0, x1, y1) in RECTS[g].items():
        gc = np.full((h, w), cv2.GC_BGD, np.uint8)
        box = np.zeros((h, w), bool)
        box[y0:y1, x0:x1] = True
        gc[box & ~sky] = cv2.GC_PR_FGD
        gc[box & sky] = cv2.GC_PR_BGD
        bg, fg = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
        cv2.grabCut(img, gc, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
        m = ((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD)) & box
        m = ndimage.binary_fill_holes(m)
        n2, lab2, st2, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
        big = [i for i in range(1, n2) if st2[i][4] >= MIN_AREA]
        part = np.isin(lab2, big)
        ys, xs = np.nonzero(part)
        print(f"  {g} {nm}: 塊 {len(big)}・{int(part.sum())}画素・x{xs.min()}〜{xs.max()}・y{ys.min()}〜{ys.max()}"
              f"（枠 x{x0}〜{x1}・y{y0}〜{y1}＝枠に触れたら枠が狭い）")
        keep |= part
    rgb = Image.open(src).convert("RGB")
    alpha = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = rgb.copy()
    rgba.putalpha(alpha)
    dst = AI / f"ep31_szk_{g}_plane.png"
    rgba.save(dst)
    ys, xs = np.nonzero(keep)
    print(f"  {g}: 切り抜き {int(keep.sum())}画素・x{xs.min()}〜{xs.max()}・y{ys.min()}〜{ys.max()} → {dst.name}")
    return src, keep, rgba


def check(rows):
    sheet = Image.new("RGB", (1280, 360 * len(rows)), (20, 20, 20))
    for r, (src, keep, rgba) in enumerate(rows):
        a = cv2.imread(str(src))
        cs, _ = cv2.findContours(keep.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(a, cs, -1, (0, 0, 255), 3)
        left = Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB)).resize((640, 360), Image.LANCZOS)
        chk = Image.new("RGB", (1280, 720), (255, 255, 255))
        px = np.indices((720, 1280)).sum(0) // 40 % 2
        chk = Image.fromarray(np.where(px[..., None] == 1, 200, 255).astype(np.uint8).repeat(3, -1))
        chk.paste(rgba, (0, 0), rgba)
        sheet.paste(left, (0, 360 * r))
        sheet.paste(chk.resize((640, 360), Image.LANCZOS), (640, 360 * r))
    OUT.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT / "chk31_plane.png")
    print(OUT / "chk31_plane.png")


if __name__ == "__main__":
    check([cut("a"), cut("b")])
