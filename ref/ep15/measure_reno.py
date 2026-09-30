# -*- coding: utf-8 -*-
"""15本目 ⑤b-2（2026-09-30）：案C の置き場 RA（上から見たステッド空港）の位置を、報告書の図の**画素から機械で測る**（目で読まない）。
    python ref/ep15/measure_reno.py        → ref/ep15/illu_reno.json（`tools/illu.py` の R_PYL・R_ACC・R_SHOW_DEG・R_S0・R_LAPS の正本）

■ 何を測るか
  ① 図1（AAB p11・北が上）：パイロンの印（青＝パイロン・黄＝案内・赤＝本部）の色の塊の真ん中・ショーライン（緑の画素を直線で当てる）・
     事故地点（小さな赤い点）。縮尺＝コースの長さ 8.4333マイル（#33 p2009）÷ パイロンを回る順の折れ線の長さ（画素）
  ② #14 図12（p3014・Google Earth の上に 1周目 黄・2周目 橙・3周目 赤）：パイロンの印（暗い赤の三角）→ 図1 へ相似で当てはめる
     （回転・一様な拡大・平行移動の最小二乗）。航跡＝色ごとの画素を、コースの真ん中から見た角度で2度ずつ並べた点
  ③ 確かめ：事故地点がショーラインの南に何メートルか（記録：ボックス席の端は 874フィート＝266メートル＝AAB p19）
■ ⚠️ 図12 の画像そのもの（Google・USDA などの空撮）は写さない＝使うのは NTSB が重ねた航跡の線の位置だけ（映像方針 §1 線1）。
   パイロンの塊の真ん中は、図12 では航跡の赤と色が近い＝下の F12_NAMES の近くの塊だけを採る（名の札の位置は図を見て決めた＝
   カットの中の位置は機械で測った値）
⚠️ 原文の PDF は `ref/ep15/src/`（git の外＝手元だけ）。無ければ止まる（fail closed）
"""
import json
import math
import sys
from collections import deque
from pathlib import Path

import fitz
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = HERE / "illu_reno.json"
ORDER = ["hm", "p1", "p2", "p3", "sg", "p4", "p5", "p6", "gw", "p7", "p8", "p9"]    # 回る順（左回り）
COURSE_M = 8.4333 * 1609.344                                                      # #33 p2009
# 図1 の塊 → パイロンの名（青9・黄2・赤1。並びは北から＝図の名の札で確かめた）
F1_BLUE = dict(p5=(447, 31), p4=(606, 85), p6=(310, 124), p3=(699, 394), p7=(302, 470), p2=(674, 514), p8=(355, 547),
               p1=(584, 578), p9=(422, 580))
F1_YELLOW = dict(sg=(651, 218), gw=(309, 238))
F1_RED = dict(hm=(529, 597))
# 図12 の名の札のそばの塊（図12 は北が右＝相似の当てはめが回転を決める）
F12_NAMES = dict(p7=(415, 76), p8=(324, 143), p9=(293, 231), hm=(279, 365), p1=(295, 435), p2=(383, 532), p3=(536, 562),
                 sg=(760, 488), p4=(913, 428), p5=(968, 232), p6=(843, 68), gw=(705, 71))


def image(pdf, page):
    p = SRC / pdf
    if not p.exists():
        sys.exit(f"E 原文が無い：{p}")
    d = fitz.open(p)
    pix = fitz.Pixmap(d, d[page - 1].get_images(full=True)[0][0])
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3].astype(int)


def blobs(mask, min_px):
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    for y0, x0 in zip(*np.nonzero(mask)):
        if seen[y0, x0]:
            continue
        q, pts = deque([(y0, x0)]), []
        seen[y0, x0] = True
        while q:
            y, x = q.popleft()
            pts.append((x, y))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        q.append((yy, xx))
        if len(pts) >= min_px:
            a = np.array(pts, dtype=float)
            out.append((a[:, 0].mean(), a[:, 1].mean()))
    return out


def near(bl, want, lim=12.0):
    """名の札のそばの塊の真ん中（無ければ止める）。"""
    out = {}
    for k, (x, y) in want.items():
        c = [b for b in bl if math.hypot(b[0] - x, b[1] - y) < lim]
        if not c:
            sys.exit(f"E {k} の塊が見つからない（{x},{y} の近く）")
        c = min(c, key=lambda b: math.hypot(b[0] - x, b[1] - y))
        out[k] = (round(c[0], 1), round(c[1], 1))
    return out


def main():
    im = image("AAB1201.pdf", 11)
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    f1 = {}
    f1.update(near(blobs((B > 120) & (R < 90) & (G < 120) & (B - R > 60), 12), F1_BLUE))
    f1.update(near(blobs((R > 150) & (G > 150) & (B < 70) & (abs(R - G) < 60), 12), F1_YELLOW))
    f1.update(near(blobs((R > 140) & (G < 60) & (B < 60), 4), F1_RED))
    gm = (G > 110) & (R < 70) & (B < 90) & (G - R > 60)
    ys, xs = np.nonzero(gm)
    k, c = np.linalg.lstsq(np.vstack([xs, np.ones_like(xs)]).T, ys, rcond=None)[0]
    sub = np.zeros_like(R, dtype=bool)
    sub[640:700, 480:570] = True
    acc = blobs(sub & (R > 90) & (G < 70) & (B < 70) & (R - G > 50), 3)
    if len(acc) != 1:
        sys.exit(f"E 事故地点の塊が {len(acc)}")
    per = sum(math.dist(f1[a], f1[b]) for a, b in zip(ORDER, ORDER[1:] + ORDER[:1]))
    mpp = COURSE_M / per
    h0 = f1["hm"]

    def w1(p):
        return ((p[0] - h0[0]) * mpp, -(p[1] - h0[1]) * mpp)
    sl = lambda x: k * x + c  # noqa: E731
    s0, s1 = w1((147, sl(147))), w1((735, sl(735)))
    deg = math.degrees(math.atan2(s1[1] - s0[1], s1[0] - s0[0]))
    S0 = w1((h0[0], sl(h0[0])))
    a = math.radians(deg)
    u, v = np.array([math.cos(a), math.sin(a)]), np.array([math.sin(a), -math.cos(a)])
    A = w1(acc[0])
    rel = np.array(A) - np.array(S0)
    print(f"図1：1画素 {mpp:.3f} メートル・ショーラインの向き {deg:.2f}度・事故地点 {[round(x) for x in A]}"
          f"＝ショーラインの南 {rel @ v:.0f}メートル（記録：ボックス席の端 266メートル）")

    im2 = image("ntsb_docket_14_data_recorders_factual.pdf", 14)
    R, G, B = im2[..., 0], im2[..., 1], im2[..., 2]
    f12 = near(blobs((R > 90) & (R < 200) & (G < 45) & (B < 45) & (R - G > 70), 10), F12_NAMES)
    rows, rhs = [], []
    for nm in ORDER:
        (x, y), (p, q) = f12[nm], f1[nm]
        rows += [[x, -y, 1, 0], [y, x, 0, 1]]
        rhs += [p, q]
    aa, bb, tx, ty = np.linalg.lstsq(np.array(rows, float), np.array(rhs, float), rcond=None)[0]

    def w12(q):
        return w1((aa * q[0] - bb * q[1] + tx, bb * q[0] + aa * q[1] + ty))
    res = [math.dist(w12(f12[nm]), w1(f1[nm])) for nm in ORDER]
    print(f"図12→図1：拡大 {math.hypot(aa, bb):.4f}・回転 {math.degrees(math.atan2(bb, aa)):.2f}度・残差 平均 {np.mean(res):.0f}"
          f"・最大 {max(res):.0f} メートル")
    cen = np.array([640.0, 330.0])
    cols = dict(lap1=(R > 200) & (G > 200) & (B < 90), lap2=(R > 200) & (G > 110) & (G < 185) & (B < 70),
                lap3=(R > 200) & (G < 60) & (B < 60))
    wc = np.mean([w1(f1[nm]) for nm in ORDER], axis=0)
    laps = {}
    for nm, m in cols.items():
        m = m.copy()
        m[640:, 400:] = False            # 右下の Google の文字
        m[:12, :] = False
        ys, xs = np.nonzero(m)
        ang = (np.degrees(np.arctan2(ys - cen[1], xs - cen[0])) + 360) % 360
        rad = np.hypot(xs - cen[0], ys - cen[1])
        W = []
        for a0 in range(0, 360, 2):
            sel = (ang >= a0) & (ang < a0 + 2) & (rad > 150)
            if sel.sum() >= 3:
                rr, t = np.median(rad[sel]), math.radians(a0 + 1)
                W.append(w12((cen[0] + rr * math.cos(t), cen[1] + rr * math.sin(t))))
        angs = [(math.degrees(math.atan2(q[1] - wc[1], q[0] - wc[0])) + 360) % 360 for q in W]
        order = sorted(range(len(W)), key=lambda i: angs[i])
        W, A_ = [W[i] for i in order], [angs[i] for i in order]
        segs, cur = [], [0]
        for i in range(1, len(W)):
            if A_[i] - A_[i - 1] > 9:
                segs.append(cur)
                cur = []
            cur.append(i)
        segs.append(cur)
        if len(segs) > 1 and (A_[0] + 360) - A_[-1] <= 9:
            segs[0] = segs[-1] + segs[0]
            segs.pop()
        path = [[round(W[i][0]), round(W[i][1])] for i in max(segs, key=len)]
        q = path[::4] + ([path[-1]] if (len(path) - 1) % 4 else [])
        laps[nm] = q
        print(f"{nm}：{len(q)}点・{sum(math.dist(p, r) for p, r in zip(q, q[1:])):.0f}メートル（記録のコース {COURSE_M:.0f}）")
    out = dict(mpp_fig1=round(mpp, 4), showline_deg=round(deg, 2), S0=[round(x, 1) for x in S0],
               accident=[round(x) for x in A], south_of_showline=round(float(rel @ v), 1),
               pylons={nm: [round(x) for x in w1(f1[nm])] for nm in ORDER}, laps=laps,
               fit12=dict(scale=round(math.hypot(aa, bb), 4), deg=round(math.degrees(math.atan2(bb, aa)), 2),
                          resid_mean_m=round(float(np.mean(res)), 1)))
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
