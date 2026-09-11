# -*- coding: utf-8 -*-
"""前の版と今の版の同じカットを**画素で比べ**、変わった所の外接矩形を出す（台帳 §AE）。

    python -u qa_out/kb_ae_diffbox.py c101 c108 ...
    python -u qa_out/kb_ae_diffbox.py --a out/jiko/qa_keybridge-r08 --b out/jiko/qa_keybridge-r09 c101

■ 何のためか
  ⑤c【見る】6周目は「直しが絵を悪くしたか（r08 より悪いか）」を見る。前の版を原寸でもう一度読むと
  画像が倍になる（[[feedback-subagents-must-not-read-images]]）。そこで**どこが動いたか**を先に機械で出し、
  前の版は要る所だけ切り出して見る。
  ⚠️ 矩形は「動いた場所」であって「粗」ではない。判定は原寸の目視で決める。
■ 測り方
  灰色にして画素ごとの差 > 40 を「変わった」とし、8px のブロックへ畳んで2回ふくらませ、連結成分を取る。
  30画素未満の成分は JPEG の揺れとして捨てる。面積の大きい順に6つまで出す。
  対照（2026-09-11）：副題だけ直した `c201` は矩形が副題の帯 [48,128-656,208] の1つだけ／
  図を替えた `c307` は 27.02%。
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent


def main(argv):
    a_dir, b_dir = "out/jiko/qa_keybridge-r08", "out/jiko/qa_keybridge-r09"
    cuts = []
    it = iter(argv)
    for x in it:
        if x == "--a":
            a_dir = next(it)
        elif x == "--b":
            b_dir = next(it)
        else:
            cuts.append(x)
    A, B = HERE / a_dir, HERE / b_dir
    for d in (A, B):
        if not d.is_dir():
            # fail closed：比べる相手が無いのに「変化なし」と答えない
            raise SystemExit(f"🔴 フォルダが無い: {d}")
    print(f"■ {a_dir} → {b_dir}")
    for cid in cuts:
        pa, pb = A / f"cut_{cid}.jpg", B / f"cut_{cid}.jpg"
        if not (pa.exists() and pb.exists()):
            print(f"{cid} 🔴 画像が無い（{pa.exists()}/{pb.exists()}）")
            continue
        a = np.asarray(Image.open(pa).convert("L"), dtype=np.int16)
        b = np.asarray(Image.open(pb).convert("L"), dtype=np.int16)
        if a.shape != b.shape:
            print(f"{cid} 🔴 大きさが違う {a.shape} {b.shape}")
            continue
        m = np.abs(a - b) > 40
        h, w = m.shape
        bh, bw = h // 8, w // 8
        blk = m[:bh * 8, :bw * 8].reshape(bh, 8, bw, 8).any(axis=(1, 3))
        blk = ndimage.binary_dilation(blk, iterations=2)
        lab, _ = ndimage.label(blk)
        boxes = []
        for sl in ndimage.find_objects(lab):
            y0, y1 = sl[0].start * 8, sl[0].stop * 8
            x0, x1 = sl[1].start * 8, sl[1].stop * 8
            area = int(m[y0:y1, x0:x1].sum())
            if area >= 30:
                boxes.append((area, x0, y0, x1, y1))
        boxes.sort(reverse=True)
        s = "  ".join(f"[{x0},{y0}-{x1},{y1}]" for _, x0, y0, x1, y1 in boxes[:6])
        print(f"{cid} {w}x{h} changed={m.mean() * 100:.2f}% n={len(boxes)}  {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
