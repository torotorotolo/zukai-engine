# -*- coding: utf-8 -*-
"""25本目②：付図24（運行の経過・事故現場付近・時刻軸）の帯（発言・操作の長さ）を、PDF の図形（ベクタ）から秒に直す。
文字の層は化けている＝読める字は Windows OCR（tools/ocr_win.ps1 の出力）から取り、時刻の目盛り（「9:17:40」など）の画素の位置で x→秒の式を頁ごとに決める。
帯＝塗りのある四角（get_drawings の rect / 'f' or 'fs'）。座標は描画した PNG（dpi）と同じ画素に直す（page.rotation_matrix を掛ける）。
使い方: python fuzu24.py <pdf> <dpi> <出力> <PDF頁>:<そのOCRの出力> ..."""
import re, sys

import fitz

TICK = re.compile(r"^\[(\d+),(\d+)-(\d+),(\d+)\]\s+(.*)$")


def ticks(ocr_path):
    """OCR の行から時刻の目盛りを拾う（9:17:40 → 秒）。"""
    out = []
    raw = open(ocr_path, "rb").read()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        txt = raw.decode("cp932", "replace")
    for line in txt.splitlines():
        m = TICK.match(line.strip())
        if not m:
            continue
        x0, y0, x1, y1, t = int(m[1]), int(m[2]), int(m[3]), int(m[4]), m[5]
        d = re.sub(r"\D", "", t)
        if len(d) == 5 and d[0] == "9" and t.strip().startswith("9"):
            h, mi, s = int(d[0]), int(d[1:3]), int(d[3:5])
            if 0 <= mi < 60 and 0 <= s < 60 and s % 10 == 0:
                out.append(((x0 + x1) / 2, h * 3600 + mi * 60 + s, y0))
    return out


def fit(tk):
    n = len(tk)
    mx = sum(x for x, _, _ in tk) / n
    mt = sum(t for _, t, _ in tk) / n
    sxx = sum((x - mx) ** 2 for x, _, _ in tk)
    sxt = sum((x - mx) * (t - mt) for x, t, _ in tk)
    a = sxt / sxx
    b = mt - a * mx
    res = max(abs(a * x + b - t) for x, t, _ in tk)
    return a, b, res


def hms(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec - h * 3600 - m * 60
    return f"{h}:{m:02d}:{s:04.1f}"


def main():
    pdf, dpi, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    doc = fitz.open(pdf)
    lines = []
    for spec in sys.argv[4:]:
        pno, ocr = spec.split(":", 1)
        pno = int(pno)
        pg = doc[pno - 1]
        tk = ticks(ocr)
        lines.append(f"===== PDF{pno} 目盛り={[(round(x), hms(t)) for x, t, _ in tk]}")
        if len(tk) < 2:
            lines.append("  !! 目盛りが2つ未満＝式が立たない")
            continue
        a, b, res = fit(tk)
        lines.append(f"  式: 秒 = {a:.5f} * x + {b:.1f}（1秒={1 / a:.1f}画素・目盛りへの当てはまりの最大ずれ {res:.2f}秒）")
        M = pg.rotation_matrix * fitz.Matrix(dpi / 72, dpi / 72)
        rects = []
        for dr in pg.get_drawings():
            if dr.get("fill") is None:
                continue
            for it in dr["items"]:
                if it[0] != "re":
                    continue
                r = fitz.Rect(it[1]) * M
                w, h = r.width, r.height
                if w < 3 or h < 3:
                    continue
                if w > 0.6 * pg.rect.height * dpi / 72:  # 頁の幅いっぱいの地は帯ではない
                    continue
                rects.append((round(r.y0), round(r.y1), round(r.x0), round(r.x1), tuple(round(c, 2) for c in dr["fill"])))
        rects.sort()
        lines.append(f"  塗りの四角 {len(rects)} 個（y0-y1 / x0-x1 / 色 / 始まり〜終わりの時刻 / 長さ）")
        for y0, y1, x0, x1, col in rects:
            t0, t1 = a * x0 + b, a * x1 + b
            lines.append(f"   y{y0}-{y1} x{x0}-{x1} {col} {hms(t0)}〜{hms(t1)} ({t1 - t0:.1f}秒)")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("done")


if __name__ == "__main__":
    main()
