# -*- coding: utf-8 -*-
"""sub_center.py — 焼いたコマ（試し焼きの `cut_<cid>.jpg`）の**字幕が中央にそろっているか**を機械で測る（2026-10-02 16本目⑤b-7 新設）。

■ なぜ要るか：試し焼き 36943709915 で cb04 の字幕の2行目が「…水を抜く工」で欠けていた（後半が描かれていない）。
  字幕は SVG の中央そろえ（`scene_jiko.sub_row`＝text-anchor="middle"）＝欠けた行は字の範囲の真ん中が画面の中央（960）から
  ずれる。門番 subwrap は字幕の**文**の折り方を測るだけ＝焼いた絵の欠けは見ない（机上検査は絵を見ない）。
  全218コマのうち1行だけ＝640px のシートでは「2行目が短い」くらいにしか見えない。
■ 測るもの：字幕の帯（y 900〜1080）の黄色い字（語り）と水色の字（聞き役）を行ごとに分け、字の範囲の真ん中が
  中央から TOL px より離れた行を挙げる。

    python qa_out/sub_center.py <試し焼きの成果物のフォルダ>      # 例 out/jiko/qa_ep16_b7

■ 🆕 2026-10-08（20本目 ⑤b-2）：**字の下半分が欠けた行**も測る（試し焼き 37739768739 の c107「1つ目。あの日、操｜縦室と客室で…」＝
  x≈768（Chrome の描画の区画の境目）から右の字の下半分が水平に切れていた・同じ字幕の層を使う2コマとも＝層の書き出しの欠け）。
  行の字の範囲を 48px ごとの区画に分け、区画ごとの字の下の端が行の下の端（区画の上位10%）より行の高さの 30% 以上上にある区画が
  **3つ以上続けば**欠け（1区画だけなら「「」「ー」など上だけの字）。中央からのずれでは拾えない（行の左右の端は残る）。
  聞き役の赤（#ff3030 の近く＝14本目から）の行と、途中のコマ `at_*.jpg` も測る（それまでは黄と水色・`cut_*` だけ）。
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
TOL = 30          # 中央からのずれの許し（px）。字のフチと句読点の偏りは 10px 未満（⑤b-7 に217コマで測った）


def lines_of(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    band = a[900:1080]
    r, g, b = band[..., 0], band[..., 1], band[..., 2]
    ink = ((r > 170) & (g > 150) & (b < 110)) | ((b > 160) & (g > 140) & (r < 170))   # 黄（語り）・水色（聞き役）
    ink |= (r > 200) & (g < 110) & (b < 110)                                           # 🆕 20本目：赤（聞き役・14本目から）
    rows = ink.sum(axis=1)
    out, y = [], 0
    while y < len(rows):
        if rows[y] > 3:
            y0 = y
            while y < len(rows) and rows[y] > 3:
                y += 1
            if y - y0 >= 12:
                cols = np.where(ink[y0:y].sum(axis=0) > 0)[0]
                out.append((y0 + 900, y + 900, int(cols[0]), int(cols[-1]), _cut_bins(ink[y0:y], int(cols[0]), int(cols[-1]))))
        y += 1
    return out


BIN, CUT_K, CUT_RUN = 48, 0.30, 3


def _cut_bins(m, x0, x1):
    """🆕 20本目 ⑤b-2：行の中で、字の下半分が欠けた区画の続き（始めの x, 終わりの x）の並び。m＝その行の字の有無（高さ×幅）"""
    h = m.shape[0]
    bots = []
    for xa in range(x0, x1 + 1, BIN):
        part = m[:, xa:min(x1 + 1, xa + BIN)]
        ys = np.where(part.any(axis=1))[0]
        bots.append((xa, int(ys[-1]) if len(ys) else None))
    inked = [b for _, b in bots if b is not None]
    if not inked:
        return []
    # ⚠️ 基準は中央値でなく上位10%（90パーセンタイル）＝欠けた区画が行の半分を超えると中央値が欠けた側に寄る（c107 は17区画中10が欠け＝
    #    中央値では鳴らなかった・⑤b-2 の陽性対照）
    ref = float(np.percentile(inked, 90))
    runs, cur = [], []
    for xa, b in bots:
        if b is not None and b < ref - CUT_K * h:
            cur.append(xa)
        else:
            if len(cur) >= CUT_RUN:
                runs.append((cur[0], cur[-1] + BIN))
            cur = []
    if len(cur) >= CUT_RUN:
        runs.append((cur[0], cur[-1] + BIN))
    return runs


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    root = Path(sys.argv[1])
    files = sorted(root.rglob("cut_*.jpg")) + sorted(root.rglob("at_*.jpg"))    # 🆕 20本目：途中のコマも
    if not files:
        raise SystemExit(f"🔴 {root} に cut_*.jpg が無い（0件を合格にしない）")
    bad, cut, n = [], [], 0
    for p in files:
        for y0, y1, x0, x1, runs in lines_of(p):
            n += 1
            c = (x0 + x1) / 2
            if abs(c - 960) > TOL:
                bad.append((p.stem, y0, x0, x1, round(c)))
            for a, b in runs:
                cut.append((p.stem, y0, y1, a, b))
    print(f"■ 焼いたコマ {len(files)} 枚・字幕の行 {n} 行を測った（中央 960 からのずれの許し {TOL}px・下半分の欠け＝{BIN}px の区画が"
          f"{CUT_RUN}つ以上続けて行の高さの {int(CUT_K * 100)}% 以上短い）")
    if n == 0:
        print("🔴 字幕の行を1行も拾えなかった（色の網が外れた＝0件を合格にしない）")
        return 2
    for s, y0, x0, x1, c in bad:
        print(f"  🔴 {s}  y{y0}  字の範囲 x {x0}〜{x1}（真ん中 {c}）＝行の一部が描かれていない疑い")
    for s, y0, y1, a, b in cut:
        print(f"  🔴 {s}  y{y0}〜{y1}  x {a}〜{b} の字の下半分が欠けている（字幕の層の書き出しの欠け＝焼き直す）")
    print("✓ どの字幕の行も中央にそろい、欠けも無い" if not bad and not cut else f"🔴 ずれ {len(bad)} 行・欠け {len(cut)} か所")
    return 1 if bad or cut else 0


if __name__ == "__main__":
    sys.exit(main())
