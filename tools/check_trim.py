# -*- coding: utf-8 -*-
"""切り出しの縦線が、画像に焼き込まれた**文字を割っていないか**を測る。

■ なぜ要るか（2026-08-04 の r05 拡大目視で出た）
  別添1 付図-3 を左右に割って ep05／ep06 にしていたが、この図は
  「フィレット・シール」「スプライス・プレート」「元と同じリベットと間隔で打鋲せよ」
  といった**引き出し線つきの札が中央をまたいでいる**。
  x=0.53 / x=0.50 で切っていたので、両方の端に
    ep05 …「フィレッ」「スプライス・ブ」「元と同じリベットと」
    ep06 …「ット・シール」「プレート」「と間隔で打鋲せよ」
  と**文字の途中で切れた断片**が並んでいた。ルール §3
  「切ったら切り出した画像を目で見る」の見落とし。机上検査6種はどれも
  **画像の中の文字を見ない**ので全部通っていた。

■ 測り方
  二値化して、黒画素の連結成分を取る。そのうち**文字らしい大きさ**の塊
  （高さ 8〜60px かつ 幅 ≦ 高さ×3）を「文字」と見なし、
  切り出しの左右の x がその塊を**またいでいないか**を見る。

🔴 **効くのは「線画＋印刷された札」の図だけ**（付図・別添の図面）。
   2026-08-04 に作った直後、この道具は c214・c231・c333（写真-43／44）で
   「文字を13個割っている」と鳴った。実物を見ると、それは焼き込みキャプションではなく
   **残骸そのものに手書きされた墨書き（「S-5R」など）**で、写真の中身だった。
   写真では小さな暗い塊が何でも「文字」に見えるので、**スキャン写真の結果は信用しない。**
   （[[feedback-verify-your-own-instrument]]：新しく作った物差しは最初ほぼ必ず間違っている）
   ⚠️ 図の線や矢印も塊になるが、細長いので高さ・縦横比の条件でだいたい落ちる。

    python tools/check_trim.py                    # SPEC の trim を全部見る
    python tools/check_trim.py --img ja123/a1f003.jpg --x 0.53
    python tools/check_trim.py --img ja123/a1f003.jpg --safe   # 割らずに切れる x を出す
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
from PIL import Image

REF = Path(__file__).parent.parent / "ref"
GLYPH_H = (8, 60)      # 文字とみなす高さ（px）
GLYPH_AR = 3.0         # 幅 ≦ 高さ×これ


def components(a):
    """黒画素の連結成分の外接矩形を返す（4近傍・union-find）。"""
    h, w = a.shape
    par = {}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def uni(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            par[ry] = rx

    lab = np.zeros((h, w), dtype=np.int32)
    nxt = 1
    for y in range(h):
        row = a[y]
        for x in np.flatnonzero(row):
            up = lab[y - 1, x] if y else 0
            lf = lab[y, x - 1] if x else 0
            if up and lf:
                lab[y, x] = up
                uni(up, lf)
            elif up or lf:
                lab[y, x] = up or lf
            else:
                lab[y, x] = nxt
                par[nxt] = nxt
                nxt += 1
    boxes = {}
    for y in range(h):
        for x in np.flatnonzero(lab[y]):
            r = find(lab[y, x])
            b = boxes.get(r)
            if b is None:
                boxes[r] = [x, y, x, y]
            else:
                b[0] = min(b[0], x); b[2] = max(b[2], x)
                b[3] = y
    return list(boxes.values())


def glyphs(path):
    im = Image.open(path).convert("L")
    w, h = im.size
    a = np.asarray(im) < 160
    out = []
    for x0, y0, x1, y1 in components(a):
        gh, gw = y1 - y0 + 1, x1 - x0 + 1
        if GLYPH_H[0] <= gh <= GLYPH_H[1] and gw <= gh * GLYPH_AR:
            out.append((x0 / w, y0 / h, x1 / w, y1 / h))
    return out, (w, h)


def cut_hits(gl, x):
    return [g for g in gl if g[0] < x < g[2]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img")
    ap.add_argument("--x", type=float, action="append")
    ap.add_argument("--safe", action="store_true")
    a = ap.parse_args()

    if a.img:
        targets = [(a.img, [(a.x or [])])]
    else:
        import scene_jiko as S
        seen = {}
        for cid, t in S.PHOTO_TRIM.items():
            seen.setdefault(S.SPEC[cid]["photo"], []).append((cid, t))
        targets = [(p, v) for p, v in seen.items()]

    bad = 0
    for img, uses in targets:
        p = REF / img
        if not p.exists():
            print(f"✗ {img} が無い")
            continue
        gl, (w, h) = glyphs(p)
        print(f"── {img}（{w}×{h}）　文字らしい塊 {len(gl)}個")
        if a.img and a.safe:
            xs = []
            for i in range(5, 96):
                x = i / 100
                if not cut_hits(gl, x):
                    xs.append(x)
            runs, s = [], None
            for i, x in enumerate(xs):
                if s is None:
                    s = x
                elif round(x - xs[i - 1], 3) > 0.011:
                    runs.append((s, xs[i - 1])); s = x
            if s is not None:
                runs.append((s, xs[-1]))
            print("  文字を割らずに切れる x：")
            for lo, hi in runs:
                print(f"    {lo:.2f} 〜 {hi:.2f}")
            continue
        if a.img:
            for x in (a.x or []):
                hits = cut_hits(gl, x)
                mark = "🔴" if hits else "✓"
                print(f"  {mark} x={x}：割っている塊 {len(hits)}個")
                for g in hits[:8]:
                    print(f"      x {g[0]:.3f}〜{g[2]:.3f}  y {g[1]:.3f}〜{g[3]:.3f}")
                bad += len(hits)
            continue
        for cid, t in uses:
            for i, x in ((0, t[0]), (2, t[2])):
                if x in (0.0, 1.0):
                    continue
                hits = cut_hits(gl, x)
                if hits:
                    bad += 1
                    side = "左" if i == 0 else "右"
                    print(f"  🔴 {cid} の{side}端 x={x}：文字を {len(hits)}個 割っている")
                    for g in hits[:6]:
                        print(f"      x {g[0]:.3f}〜{g[2]:.3f}  y {g[1]:.3f}〜{g[3]:.3f}")
    print(f"\n{'🔴 文字を割っている切り出しがある' if bad else '✓ 文字を割っている切り出しは無い'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
