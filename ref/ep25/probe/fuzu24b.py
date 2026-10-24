# -*- coding: utf-8 -*-
"""25本目②：付図24 の発言の帯（太さ2.88の水平線・濃い緑＝輸送指令員／橙＝本件車掌／青＝録音開始の印）を秒にする。
目盛りの式は fuzu24.py と同じ（OCR の「9:17:40」などの画素の位置から頁ごとに）。帯の真上の OCR の字を添える。
頁は10秒ずつ重なる＝同じ帯が2頁に出る（頁の端で切れることもある）→ 始まり・終わりが0.3秒以内なら1つにまとめ、長いほうを残す。
使い方: python fuzu24b.py <pdf> <dpi> <出力> <PDF頁>:<そのOCRの出力> ..."""
import re, sys

import fitz

sys.path.insert(0, ".")
from fuzu24 import ticks, fit, hms  # noqa: E402

SPK = {(0.0, 0.51, 0.0): "輸送指令員A", (1.0, 0.4, 0.0): "本件車掌", (1.0, 0.41, 0.0): "本件車掌", (0.0, 0.0, 1.0): "録音開始の印"}
OCRL = re.compile(r"^\[(\d+),(\d+)-(\d+),(\d+)\]\s+(.*)$")


def ocr_lines(path):
    raw = open(path, "rb").read()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        txt = raw.decode("cp932", "replace")
    out = []
    for line in txt.splitlines():
        m = OCRL.match(line.strip())
        if m:
            out.append((int(m[1]), int(m[2]), int(m[3]), int(m[4]), m[5].replace(" ", "")))
    return out


def main():
    pdf, dpi, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    doc = fitz.open(pdf)
    segs = []
    for spec in sys.argv[4:]:
        pno, ocr = spec.split(":", 1)
        pno = int(pno)
        pg = doc[pno - 1]
        a, b, _ = fit(ticks(ocr))
        ol = ocr_lines(ocr)
        M = pg.rotation_matrix * fitz.Matrix(dpi / 72, dpi / 72)
        for dr in pg.get_drawings():
            col = tuple(round(c, 2) for c in (dr.get("color") or ()))
            if round(dr.get("width") or 0, 2) != 2.88 or col not in SPK:
                continue
            for it in dr["items"]:
                if it[0] != "l":
                    continue
                p1, p2 = it[1] * M, it[2] * M
                if abs(p1.y - p2.y) > 1:
                    continue
                y = round(p1.y)
                if y > 1000 or (2200 < min(p1.x, p2.x) < 2330 and 790 < y < 890):  # 凡例の見本の線は除く
                    continue
                x0, x1 = sorted((p1.x, p2.x))
                # 帯の真上（y-45〜y-2）で x が重なる OCR の字
                lab = [t for (ox0, oy0, ox1, oy1, t) in ol if y - 50 <= oy1 <= y + 2 and ox1 > x0 - 40 and ox0 < x1 + 40]
                segs.append((a * x0 + b, a * x1 + b, SPK[col], pno, y, round(x0), round(x1), " / ".join(lab)))
    segs.sort()
    merged = []
    for s in segs:
        if merged and s[2] == merged[-1][2] and abs(s[0] - merged[-1][0]) < 0.3:
            if (s[1] - s[0]) > (merged[-1][1] - merged[-1][0]):
                merged[-1] = s
            continue
        if merged and s[2] == merged[-1][2] and abs(s[1] - merged[-1][1]) < 0.3:
            if (s[1] - s[0]) > (merged[-1][1] - merged[-1][0]):
                merged[-1] = s
            continue
        merged.append(s)
    lines = ["始まり\t終わり\t長さ\t話し手\t頁\ty\tx0-x1\t帯の上の OCR の字（崩れあり・確定は本文 p.77-78 の書き起こしで）"]
    for t0, t1, who, pno, y, x0, x1, lab in merged:
        lines.append(f"{hms(t0)}\t{hms(t1)}\t{t1 - t0:.1f}\t{who}\tPDF{pno}\t{y}\t{x0}-{x1}\t{lab}")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("segments", len(segs), "merged", len(merged))


if __name__ == "__main__":
    main()
