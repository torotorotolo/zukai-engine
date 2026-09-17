# -*- coding: utf-8 -*-
"""9本目 ⑤c''：r01 と r02 の検品静止画を突き合わせ、**変わったカットと、変わった場所**を出す。

■ なぜ要るか
  終わりの決まり（台帳 §0）は「直したカットだけ原寸で見る」。**どれが変わったかを手で決めない。**
  md5 で全数を突き合わせ、変わったカットは画素の差の矩形まで出す＝**差の出た所だけ切り出して見る**
  （1920×1080 を丸ごと読まない・鉄則1）。
  ⚠️ レンダは完全には決定的でない（記憶 `feedback-render-is-not-fully-deterministic`）＝
     md5 が変わっても**画素の差がしきい値未満なら「絵は変わっていない」**として数えだけ出す。

■ 判定
  差の画素 … RGB のどれかの差が TH を超える画素
  矩形 … 差の画素を行方向の帯（すき間 GAP_Y 超で割る）→ 帯の中を列方向（すき間 GAP_X 超）に割る

    python qa_out/ep9_r02_diff.py                       → 標準出力（一覧）
    python qa_out/ep9_r02_diff.py --crops <DIR> c109 …  → 指定カットの差の矩形を切り出して積む
"""
import hashlib
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
A = HERE / "out" / "jiko" / "qa_ep9-r01"
B = HERE / "out" / "jiko" / "qa_ep9-r02"
TH = 48
MIN_PX = 40
GAP_Y, GAP_X, PAD = 40, 80, 20


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def runs(idx, gap):
    """整数の並び（昇順）を、すき間 gap を超えるところで割って (始, 終) の列にする。"""
    out = []
    for v in idx:
        if out and v - out[-1][1] <= gap:
            out[-1][1] = v
        else:
            out.append([v, v])
    return out


def boxes(mask):
    ys = np.nonzero(mask.any(axis=1))[0]
    out = []
    for y0, y1 in runs(ys, GAP_Y):
        xs = np.nonzero(mask[y0:y1 + 1].any(axis=0))[0]
        for x0, x1 in runs(xs, GAP_X):
            n = int(mask[y0:y1 + 1, x0:x1 + 1].sum())
            out.append((int(x0), int(y0), int(x1), int(y1), n))
    return out


def diff(name):
    a = np.asarray(Image.open(A / name).convert("RGB"), dtype=np.int16)
    b = np.asarray(Image.open(B / name).convert("RGB"), dtype=np.int16)
    m = np.abs(a - b).max(axis=2) > TH
    return int(m.sum()), boxes(m)


def main():
    if not A.is_dir() or not B.is_dir():
        print(f"🔴 フォルダが無い: {A if not A.is_dir() else B}")
        return 1
    names = sorted(p.name for p in A.glob("cut_*.jpg"))
    if len(names) < 200:
        print(f"🔴 r01 のカットが {len(names)} 枚しか無い（物差しが外れている）")
        return 1
    same = changed = noise = 0
    rows = []
    for nm in names:
        if not (B / nm).exists():
            rows.append((nm[4:-4], "🔴 r02 に無い", 0, []))
            continue
        if md5(A / nm) == md5(B / nm):
            same += 1
            continue
        n, bx = diff(nm)
        if n < MIN_PX:
            noise += 1
            rows.append((nm[4:-4], "・ md5 だけ違う（差 %d px）" % n, n, []))
            continue
        changed += 1
        rows.append((nm[4:-4], "変わった", n, bx))
    extra = sorted(p.name for p in B.glob("cut_*.jpg") if not (A / p.name).exists())
    print(f"■ r01 {len(names)}枚 ／ r02 {len(list(B.glob('cut_*.jpg')))}枚："
          f"同じ md5 {same}・絵が変わった {changed}・md5 だけ違う {noise}・r02 だけ {len(extra)}")
    for cid, kind, n, bx in rows:
        print(f"  {cid:5} {kind}  差 {n} px" if kind == "変わった" else f"  {cid:5} {kind}")
        for x0, y0, x1, y1, k in bx:
            print(f"        x{x0}〜{x1} y{y0}〜{y1}（{x1 - x0 + 1}×{y1 - y0 + 1}・{k} px）")
    return 0


def crops(outdir, cids):
    """指定カットの差の矩形を r02 から切り出し、カットごとに縦に積んで1枚にする（原寸のまま）。"""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for cid in cids:
        nm = f"cut_{cid}.jpg"
        n, bx = diff(nm)
        im = Image.open(B / nm).convert("RGB")
        parts = [im.crop((max(0, x0 - PAD), max(0, y0 - PAD), min(1920, x1 + PAD + 1),
                          min(1080, y1 + PAD + 1))) for x0, y0, x1, y1, _ in bx]
        if not parts:
            print(f"  {cid}: 差の矩形なし（{n} px）")
            continue
        w = max(p.width for p in parts)
        h = sum(p.height for p in parts) + 6 * (len(parts) - 1)
        sheet = Image.new("RGB", (w, h), (255, 0, 255))
        y = 0
        for p in parts:
            sheet.paste(p, (0, y))
            y += p.height + 6
        sheet.save(outdir / f"d_{cid}.png")
        print(f"  {cid}: {len(parts)}か所 → {w}×{h}")


if __name__ == "__main__":
    # ⚠️ 2026-09-17（r02 の実測）：TH=48 では **c713・c729 が「md5 だけ違う（差 0px）」**になった。
    #    直したのは不透明度 0.24 の暗い緑の四角（地との差が1チャンネル 30 前後）＝**しきい値の下に隠れる**。
    #    → 薄い色の直しを見るときは `--th 12` で測り直す（物差しの穴＝[[feedback-verify-your-own-instrument]]）。
    if "--th" in sys.argv:
        TH = int(sys.argv[sys.argv.index("--th") + 1])
        del sys.argv[sys.argv.index("--th"):sys.argv.index("--th") + 2]
    if "--crops" in sys.argv:
        i = sys.argv.index("--crops")
        crops(sys.argv[i + 1], sys.argv[i + 2:])
        sys.exit(0)
    sys.exit(main())
