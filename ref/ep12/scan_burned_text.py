# -*- coding: utf-8 -*-
"""12本目②：記録映像に「焼き込まれた英字」が出ている秒を機械で洗い出す。

なぜ要るか
  このchは画面に英字を出さない（→[[reference-report-figures-have-burned-in-english]]）。
  記録映画には**題字・説明字幕**が焼き込まれていることがあり、
  ⑤で当てる秒を決める前に「使えない秒」を先に外しておく必要がある。
  DOE の『Castle Bravo Detonation』は 59秒あたりに
  "CASTLE BRAVO / FEBRUARY 28, 1954 (15 Megatons)" が出る（目で確認ずみ）。

物差し＝**明るく・小さく・横に並ぶ**画素のかたまり。
  1) 明度が上位の画素だけ残す
  2) 縦横の勾配が両方立つ（＝字の縁）画素を数える
  3) 画面を横帯に割り、1本の帯に集中していれば「字の行」とみなす
陽性対照＝同じ絵に自分で白い字を描いて、鳴ることを確かめる。
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")


def textness(a):
    """0..1。字らしさ。"""
    g = a.astype(np.float32)
    gy = np.abs(np.diff(g, axis=0))[:, :-1]
    gx = np.abs(np.diff(g, axis=1))[:-1, :]
    edge = (gx > 28) & (gy > 28)
    bright = g[:-1, :-1] > np.percentile(g, 92)
    m = edge & bright
    rows = m.sum(axis=1).astype(np.float32)
    if rows.sum() == 0:
        return 0.0, -1
    # いちばん濃い行を中心に ±3% の帯へどれだけ集まっているか
    h = len(rows)
    k = max(3, int(h * 0.03))
    best, bi = 0.0, 0
    c = np.convolve(rows, np.ones(k), "same")
    bi = int(np.argmax(c))
    best = float(c[bi] / max(rows.sum(), 1))
    return float(m.sum()) / m.size * best * 100.0, bi


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    step = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    dur = float(sys.argv[4])

    pat = out / "t_%04d.png"
    if not (out / "t_0001.png").exists():
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(src),
                        "-vf", "fps=%.6f,scale=960:-2" % (1.0 / step),
                        "-y", str(pat)], check=True)
    fs = sorted(out.glob("t_*.png"))
    print("コマ %d 枚（%.1f 秒おき）" % (len(fs), step))

    vals = []
    for i, f in enumerate(fs):
        a = np.asarray(Image.open(f).convert("L"))
        v, bi = textness(a)
        vals.append((i * step, v, bi, a.shape[0]))

    base = np.median([v for _, v, _, _ in vals])
    print("字らしさ 中央値 %.4f" % base)

    # 陽性対照＝いちばん字らしくないコマに自分で字を描く
    quiet = min(vals, key=lambda r: r[1])
    im = Image.open(fs[int(quiet[0] / step)]).convert("L")
    d = ImageDraw.Draw(im)
    d.text((120, im.height - 90), "CASTLE BRAVO  FEBRUARY 28, 1954", fill=255)
    d.text((120, im.height - 70), "LARGEST U.S. THERMONUCLEAR DEVICE", fill=255)
    cv, cbi = textness(np.asarray(im))
    print("陽性対照（%.0f秒のコマに自分で字を描いた）: %.4f → %s"
          % (quiet[0], cv, "鳴る" if cv > base * 3 else "🔴 鳴らない＝物差しが役に立たない"))

    thr = max(base * 3, cv * 0.25)
    print("\nしきい値 %.4f を超えた秒（＝英字が出ている当たり）" % thr)
    hit = [(t, v, bi, h) for t, v, bi, h in vals if v > thr]
    for t, v, bi, h in hit:
        print("  %6.1f秒  %.4f  行 y=%d/%d（下から %.0f%%）"
              % (t, v, bi, h, (1 - bi / h) * 100))
    if not hit:
        print("  （無し）")
    print("\n全体の推移（2秒ごと）")
    print("  " + " ".join("%.0f:%.2f" % (t, v) for t, v, _, _ in vals[::2]))


if __name__ == "__main__":
    main()
