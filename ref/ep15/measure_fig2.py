# -*- coding: utf-8 -*-
"""15本目 ⑤b-4（2026-09-30）：改造の比べの模式図（`tools/mod15.py`）の形のもと＝AAB 図2（PDF 14頁）を**画素から機械で測る**（目で読まない）。
    python ref/ep15/measure_fig2.py        → ref/ep15/fig2_shapes.json（`tools/mod15.py` の機体の形の正本）

■ 図2 とは（AAB p14「Illustration of the accident airplane with stock P-51D dimensions shown in red.」）
  NTSB の図（PD）。左＝上から見た事故機（機首が右）・右＝横から見た事故機。**赤い面＝ふつうの P-51D にだけある部分**
  （翼の外側・水平尾翼の端・胴の下の空気の取り入れ口）。赤い点線＝ふつうの操縦席の覆い（使わない）
■ 何を測るか
  ① 背景を除く：背景は白〜灰色のなめらかな濃淡＝隣との差が 3 以下の画素だけを外側から塗りつぶす（機体の縁で値が跳ぶ）
  ② 塊：上から見た図（左）・横から見た図（右）。細い物（プロペラの羽根・ピトー管・尾の細い針）は丸い型で開いて落とす
  ③ 赤の面（R が高く G・B が低い画素）＝ふつうの P-51D だけの部分。事故機＝塊から赤を引いた残り
  ④ 縮尺＝上から見た図の赤い翼端から赤い翼端まで＝ふつうの翼の幅 37フィート5/16インチ（11.286メートル＝AAB p13）
     確かめ：事故機の翼の幅 28フィート10インチ（8.788メートル）・水平尾翼 12フィート1インチ（3.683）／13フィート2 1/8インチ（4.016）
     ・横から見た図の長さ＝上から見た図の長さ（同じ縮尺の図か）
■ 出力（メートル・x＝前が正・原点＝プロペラの軸の先・y＝上から見た図は機体の左が正（画面の上）／横から見た図は上が正）
⚠️ 原文の PDF は `ref/ep15/src/`（git の外＝手元だけ）。無ければ止まる（fail closed）
"""
import json
import sys
from pathlib import Path

import cv2
import fitz
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PDF = HERE / "src" / "AAB1201.pdf"
OUT = HERE / "fig2_shapes.json"
XREF = 38                                   # 14頁の画像（1321×881・DCT）
FT = 0.3048
SPAN_STOCK = (37 + (5 / 16) / 12) * FT      # 11.286（AAB p13）
SPAN_MOD = (28 + 10 / 12) * FT              # 8.788
STAB_STOCK = (13 + (2 + 1 / 8) / 12) * FT   # 4.016
STAB_MOD = (12 + 1 / 12) * FT               # 3.683


def load():
    if not PDF.exists():
        sys.exit(f"🔴 原文の PDF が無い：{PDF}（fail closed）")
    d = fitz.open(str(PDF))
    pix = fitz.Pixmap(d, XREF)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()
    return a                                                   # RGB


def foreground(a):
    """背景（なめらかな濃淡）を外から塗りつぶして除く。"""
    h, w = a.shape[:2]
    img = cv2.cvtColor(a, cv2.COLOR_RGB2BGR)
    mask = np.zeros((h + 2, w + 2), np.uint8)
    seeds = [(3, 3), (w - 4, 3), (3, h - 4), (w - 4, h - 4), (660, 60), (660, 840), (1000, 200), (1000, 700), (200, 800),
             (300, 60), (20, 440), (w - 20, 440)]
    for s in seeds:
        cv2.floodFill(img, mask, s, (0, 255, 0), loDiff=(3, 3, 3), upDiff=(3, 3, 3),
                      flags=4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8))
    return (mask[1:-1, 1:-1] == 0).astype(np.uint8)


def biggest(m, xlo, xhi):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    best, area = None, 0
    for i in range(1, n):
        x, y, w, h, ar = st[i]
        if x >= xlo and x + w <= xhi and ar > area:
            best, area = i, ar
    if best is None:
        sys.exit("🔴 図2 の塊が見つからない（fail closed）")
    return (lab == best).astype(np.uint8)


def opened(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, k)


def red_of(a, m):
    """赤の面。⚠️ 最初の判定（R>120・R−G>60）は赤の縁の暗い赤（輪郭の線・例 (95,50,45)）を取りこぼし、事故機の水平尾翼が
    記録より 7.4% 長く測れた＝暗い赤も採る（R>80・R が G と B より 35 以上大きい）。"""
    R, G, B = (a[:, :, i].astype(int) for i in range(3))
    red = ((R > 80) & (R - G > 35) & (R - B > 35)).astype(np.uint8) & m
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    return cv2.morphologyEx(red, cv2.MORPH_CLOSE, k) & m     # 赤の中の白い点線（継ぎ目）を埋める


def minus_red(m, red, r=1):
    """事故機＝塊から赤を引く。赤と銀の境の輪郭の線は、線の真ん中で分ける（r＝赤を広げる画素）。
    ⚠️ r＝2（5×5）では水平尾翼が記録より 3.0% 短く、r＝0 では 7.4% 長く測れた（線の太さ 2〜3画素 ≒ 尾翼の幅の 1%ずつ）"""
    if r <= 0:
        return m & (1 - red)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return m & (1 - cv2.dilate(red, k))


def glass_of(a, m):
    R, G, B = (a[:, :, i].astype(int) for i in range(3))
    g = ((B - R > 28) & (G - R > 18) & (B > 150)).astype(np.uint8) & m
    g = opened(g, 2)
    return biggest_any(g)


def biggest_any(m):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n <= 1:
        sys.exit("🔴 覆いの塊が無い（fail closed）")
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return (lab == i).astype(np.uint8)


def polys(m, eps=0.9, min_area=60):
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        if cv2.contourArea(c) < min_area:
            continue
        ap = cv2.approxPolyDP(c, eps, True)[:, 0, :]
        out.append(ap.astype(float))
    out.sort(key=lambda p: -abs(cv2.contourArea(p.astype(np.float32))))
    return out


def main():
    a = load()
    fg = foreground(a)
    top = opened(biggest(fg, 0, 690), 5)                       # 細い物（羽根・ピトー管・尾の針）を落とす
    side = opened(biggest(fg, 680, a.shape[1]), 5)
    top = biggest_any(top)
    side = biggest_any(side)
    rtop, rside = red_of(a, top), red_of(a, side)
    mod_top = biggest_any(opened(minus_red(top, rtop), 2))
    mod_side = biggest_any(opened(minus_red(side, rside), 2))

    # ── 縮尺：上から見た図の赤い翼端の外の縁（上と下）＝ふつうの翼の幅 ──
    ys, xs = np.nonzero(top)
    ry, rx = np.nonzero(rtop)
    y0, y1 = ry.min(), ry.max()                                # 赤い翼端の外の縁（上・下）
    k = (y1 - y0 + 1) / SPAN_STOCK                             # 画素／メートル
    my, mx = np.nonzero(mod_top)
    span_mod = (my.max() - my.min() + 1) / k
    cy = (y0 + y1) / 2.0                                       # 胴の真ん中の線（y）
    # プロペラの軸の先＝上から見た図の右端（開いたあとの塊）
    nose_x = xs.max()
    # 水平尾翼：胴の後ろ（塊の左 18%）の上下の広がり
    tail_zone = top[:, xs.min(): xs.min() + int(0.18 * (xs.max() - xs.min()))]
    ty = np.nonzero(tail_zone.any(axis=1))[0]
    stab_stock = (ty.max() - ty.min() + 1) / k
    mtail = mod_top[:, xs.min(): xs.min() + int(0.18 * (xs.max() - xs.min()))]
    mty = np.nonzero(mtail.any(axis=1))[0]
    stab_mod = (mty.max() - mty.min() + 1) / k
    len_top = (xs.max() - xs.min() + 1) / k
    sy, sx = np.nonzero(side)
    len_side = (sx.max() - sx.min() + 1) / k
    side_nose, side_axis = sx.max(), None
    # 横から見た図のプロペラの軸の高さ＝機首の右端の列の塊の真ん中
    col = np.nonzero(side[:, sx.max() - 2])[0]
    side_axis = float(col.mean())

    def T(p):   # 上から見た図 → メートル（x 前が正・y 機体の左が正＝画面の上）
        return [[round((float(x) - nose_x) / k, 4), round((cy - float(y)) / k, 4)] for x, y in p]

    def S(p):   # 横から見た図 → メートル（y 上が正）
        return [[round((float(x) - side_nose) / k, 4), round((side_axis - float(y)) / k, 4)] for x, y in p]

    out = dict(
        src="AAB p14 図2（NTSB・PD）＝xref 38 の画像の画素から機械で測った（ref/ep15/measure_fig2.py）",
        k_px_per_m=round(k, 4),
        check=dict(span_stock_m=round(SPAN_STOCK, 3), span_mod_m=round(span_mod, 3), span_mod_rec=round(SPAN_MOD, 3),
                   stab_stock_m=round(stab_stock, 3), stab_stock_rec=round(STAB_STOCK, 3),
                   stab_mod_m=round(stab_mod, 3), stab_mod_rec=round(STAB_MOD, 3),
                   len_top_m=round(len_top, 3), len_side_m=round(len_side, 3)),
        top=dict(stock=T(polys(top)[0]), mod=T(polys(mod_top)[0]), red=[T(p) for p in polys(rtop, min_area=150)],
                 glass=T(polys(glass_of(a, mod_top))[0])),
        side=dict(stock=S(polys(side)[0]), mod=S(polys(mod_side)[0]), red=[S(p) for p in polys(rside, min_area=150)],
                  glass=S(polys(glass_of(a, mod_side))[0])),
    )
    c = out["check"]
    bad = []
    if abs(c["span_mod_m"] / SPAN_MOD - 1) > 0.015:
        bad.append(f"事故機の翼の幅 {c['span_mod_m']} ≠ 記録 {SPAN_MOD:.3f}（±1.5%）")
    for nm, rec in (("stab_stock_m", STAB_STOCK), ("stab_mod_m", STAB_MOD)):
        if abs(c[nm] / rec - 1) > 0.03:
            bad.append(f"{nm} {c[nm]} ≠ 記録 {rec:.3f}（±3%）")
    if abs(c["len_side_m"] / c["len_top_m"] - 1) > 0.03:
        bad.append(f"横の図の長さ {c['len_side_m']} ≠ 上の図の長さ {c['len_top_m']}（同じ縮尺でない？）")
    print(json.dumps(c, ensure_ascii=False))
    print("点の数：", {v: {kk: (len(vv) if kk != "red" else [len(p) for p in vv]) for kk, vv in out[v].items()} for v in ("top", "side")})
    if bad:
        for b in bad:
            print("🔴", b)
        return 1
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ 書いた：{OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
