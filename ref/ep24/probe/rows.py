# -*- coding: utf-8 -*-
"""24本目②：表の頁を「文字の位置（座標）」から行に組み直す（文字の層の列崩れの対策）。
使い方: rows.py <pdf> <出力.txt> <PDF頁…> [-g 正規表現]   ＝ 全行を出力へ・正規表現に当たる行（と前後1行）だけ画面へ
行＝語の y の中心が 3pt 以内で同じ行。語は x の順。左端の x を [x=…] で添える（列の見当）。"""
import re, sys
import fitz


def page_rows(page, tol=3.0):
    words = page.get_text("words")  # x0, y0, x1, y1, word, block, line, wno
    rows = []
    for w in sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0])):
        yc = (w[1] + w[3]) / 2
        if rows and abs(rows[-1][0] - yc) <= tol:
            rows[-1][1].append(w)
        else:
            rows.append([yc, [w]])
    out = []
    for yc, ws in rows:
        ws.sort(key=lambda w: w[0])
        out.append((yc, ws[0][0], " ".join(w[4] for w in ws)))
    return out


def main():
    args = sys.argv[1:]
    pat = None
    if "-g" in args:
        i = args.index("-g")
        pat = re.compile(args[i + 1], re.I)
        args = args[:i] + args[i + 2:]
    pdf, outp, pages = args[0], args[1], [int(p) for p in args[2:]]
    doc = fitz.open(pdf)
    with open(outp, "w", encoding="utf-8") as f:
        for p in pages:
            rows = page_rows(doc[p - 1])
            f.write(f"=== PDF p.{p}\n")
            for k, (yc, x0, t) in enumerate(rows):
                f.write(f"[y={yc:6.1f} x={x0:5.1f}] {t}\n")
            if pat:
                hit = {k for k, r in enumerate(rows) if pat.search(r[2])}
                show = sorted({j for k in hit for j in (k - 1, k, k + 1) if 0 <= j < len(rows)})
                print(f"=== PDF p.{p}（{len(hit)}行）")
                for j in show:
                    yc, x0, t = rows[j]
                    print(f"[y={yc:6.1f} x={x0:5.1f}] {t}")


if __name__ == "__main__":
    main()
