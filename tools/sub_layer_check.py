# -*- coding: utf-8 -*-
"""sub_layer_check.py — 字幕の層（`out/jiko/sub_<cid>.png`）の**書き出しの欠け**を、書き出した直後に測る（2026-10-13 新設・21本目 ⑤b-7）。

■ なぜ要るか
  Chrome の書き出しは、まれに描画の区画の境目（x≈763〜768）から右の字を描かずに PNG を返す（20本目 ⑤b-2 の c107・21本目 ⑤b-2 の c108
  ＝同じ層を使うコマは全部欠ける・焼くたびに起こりうる）。それまでは焼いたあとの絵を `qa_out/sub_center.py` で拾うだけ＝
  ⑥（Modal の本編）では見る人がいない。→ `scene_jiko.render_all` が字幕の層を書き出した直後にここで測り、欠けた層だけを描き直す
  （最大 `scene_jiko.SUB_RETRY` 回・それでも欠ければ止める＝黙って欠けた字幕で焼かない）。

■ 測るもの（字の有無＝アルファ 128 以上＝字とフチ・字幕の1行＝SUB_H の帯ごとに、その中の字の行ごと）＝`qa_out/sub_center.py` と同じ2つ
  1. 行の字の範囲の真ん中が画面の中央 960 から TOL px より離れる（行の後ろが描かれていない）
  2. 48px の区画の字の下の端が、行の上位10%の区画より行の高さの 30% 以上上にある区画が3つ以上続く（字の下半分の欠け）
  ⚠️ 見ないもの：字の形そのもの（別の字に化けた・フチの色）＝門番 subwrap と目視の担当。字幕の層の外（図の層）の欠け。

    python tools/sub_layer_check.py out/jiko                # その場の字幕の層を全部測る
    python tools/sub_layer_check.py --selftest              # 陽性対照（右の下半分を消す・右半分を消す）・陰性対照（そのまま）
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

W, SUB_H = 1920, 180
TOL = 30            # 中央からのずれの許し（px）＝sub_center.py と同じ
BIN, CUT_K, CUT_RUN = 48, 0.30, 3


def _cut_runs(m, x0, x1):
    """行の中で、字の下半分が欠けた区画の続き [(始めの x, 終わりの x)]（sub_center._cut_bins と同じ式）"""
    h = m.shape[0]
    bots = []
    for xa in range(x0, x1 + 1, BIN):
        ys = np.where(m[:, xa:min(x1 + 1, xa + BIN)].any(axis=1))[0]
        bots.append((xa, int(ys[-1]) if len(ys) else None))
    inked = [b for _, b in bots if b is not None]
    if not inked:
        return []
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


def defects_of(alpha, sub_h=SUB_H):
    """アルファ（高さ×幅・0〜255）→ 欠けの一覧（文）。空なら合格。sub_h＝字幕の1行の帯の高さ（本番は scene_jiko.SUB_H を渡す）"""
    ink = alpha > 128
    out = []
    for band in range(ink.shape[0] // sub_h):
        m = ink[band * sub_h:(band + 1) * sub_h]
        rows = m.sum(axis=1)
        y = 0
        while y < len(rows):
            if rows[y] > 3:
                y0 = y
                while y < len(rows) and rows[y] > 3:
                    y += 1
                if y - y0 >= 12:
                    cols = np.where(m[y0:y].any(axis=0))[0]
                    x0, x1 = int(cols[0]), int(cols[-1])
                    c = (x0 + x1) / 2
                    if abs(c - W / 2) > TOL:
                        out.append(f"{band + 1}行目 y{y0}: 字の範囲 x {x0}〜{x1}（真ん中 {c:.0f}）＝行の一部が描かれていない")
                    for a, b in _cut_runs(m[y0:y], x0, x1):
                        out.append(f"{band + 1}行目 y{y0}: x {a}〜{b} の字の下半分が欠けている")
            y += 1
    return out


def defects(path, sub_h=SUB_H):
    """字幕の層の PNG → 欠けの一覧。読めなければ例外（fail closed）"""
    with Image.open(path) as im:
        return defects_of(np.asarray(im.convert("RGBA"))[..., 3], sub_h)


def _fake_layer(n_rows=2):
    """陽性対照の見本＝四角い「字」を真ん中そろえで並べた字幕の層（書体に頼らない＝Actions でも同じ）"""
    a = np.zeros((SUB_H * n_rows, W), dtype=np.uint8)
    for r in range(n_rows):
        n = 22 - 4 * r
        w = n * 52 - 8
        x = (W - w) // 2
        for i in range(n):
            top = 60 + r * SUB_H + (8 if i % 5 == 2 else 0)     # 字の高さを少しばらつかせる
            a[top:r * SUB_H + 116, x + i * 52:x + i * 52 + 44] = 255
    return a


def selftest():
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(f"{'✓' if cond else '🔴'} {label}")
        ok &= bool(cond)
    base = _fake_layer()
    chk("陰性対照：欠けの無い層は鳴らない", not defects_of(base))
    cut = base.copy()
    cut[88:116, 768:] = 0                                       # 1行目の x 768 から右の字の下半分を消す（20本目 c107 の型）
    got = defects_of(cut)
    chk(f"陽性対照：x 768 から右の字の下半分を消すと鳴る（{len(got)}件）", any("下半分" in g for g in got))
    half = base.copy()
    half[SUB_H:, 1000:] = 0                                     # 2行目の後ろを消す
    got = defects_of(half)
    chk(f"陽性対照：2行目の後ろを消すと真ん中のずれで鳴る（{len(got)}件）", any("2行目" in g and "真ん中" in g for g in got))
    return 0 if ok else 2


def main():
    if "--selftest" in sys.argv:
        return selftest()
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "out" / "jiko"
    files = sorted(root.glob("sub_*.png"))
    if not files:
        print(f"🔴 {root} に字幕の層（sub_*.png）が無い（0件を合格にしない）")
        return 2
    bad = 0
    for p in files:
        d = defects(p)
        if d:
            bad += 1
            print(f"🔴 {p.name}: " + "／".join(d))
    print(f"{'✓' if not bad else '🔴'} 字幕の層 {len(files)} 枚・欠け {bad} 枚")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
