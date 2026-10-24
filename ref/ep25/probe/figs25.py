# -*- coding: utf-8 -*-
"""25本目②：報告書の別冊の付図から写真を切り出す（頁を描画して、写真の置かれた矩形で切る＝頁の回転を正しく反映）。
埋め込みの実寸（px）も記録する＝全画面に耐えるかの当たり。出力は src/fig_img/（git の外）と index.tsv。
使い方: python figs25.py <src/jtsb> <出力フォルダ> <名前>:<PDF頁>:<付図の名>[:<最大の点数>] ...
  例: RA07-3-1-3:8:付図12  RA07-3-1-3:9:付図13-1:3"""
import os, sys
from io import BytesIO

import fitz
from PIL import Image

DPI = 200
MIN_PT = 60  # 頁の上でこれより小さい画像（印・矢印）は飛ばす


def main():
    base, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for spec in sys.argv[3:]:
        parts = spec.split(":")
        name, pno, label = parts[0], int(parts[1]), parts[2]
        top = int(parts[3]) if len(parts) > 3 else 99
        doc = fitz.open(os.path.join(base, name + ".pdf"))
        pg = doc[pno - 1]
        pix = pg.get_pixmap(dpi=DPI)
        M = pg.rotation_matrix * fitz.Matrix(DPI / 72, DPI / 72)
        cands = []
        for im in pg.get_images(full=True):
            xref = im[0]
            try:
                info = doc.extract_image(xref)
                nat = (info["width"], info["height"])
            except Exception:
                nat = (0, 0)
            for r in pg.get_image_rects(xref):
                if min(r.width, r.height) < MIN_PT:
                    continue
                cands.append((nat[0] * nat[1], nat, r))
        cands.sort(key=lambda c: -c[0])
        for k, (_, nat, r) in enumerate(cands[:top], 1):
            rr = (r * M) & fitz.IRect(0, 0, pix.width, pix.height)
            rows.append((label, name, pno, k, nat, rr))
        # 頁の PNG から PIL で切る
        img = Image.open(BytesIO(pix.tobytes("png"))).convert("RGB")
        for label_, name_, pno_, k, nat, rr in [x for x in rows if x[1] == name and x[2] == pno and x[0] == label]:
            box = (int(rr.x0), int(rr.y0), int(rr.x1), int(rr.y1))
            crop = img.crop(box)
            fn = f"{label_}_{name_}_p{pno_:02d}_{k}_nat{nat[0]}x{nat[1]}.jpg"
            crop.save(os.path.join(outdir, fn), quality=92)
            print(fn, crop.size, flush=True)
    with open(os.path.join(outdir, "index.tsv"), "a", encoding="utf-8") as f:
        for label, name, pno, k, nat, rr in rows:
            f.write(f"{label}\t{name}\tPDF{pno}\t{k}\t{nat[0]}x{nat[1]}\t{int(rr.width)}x{int(rr.height)}@{DPI}dpi\n")


if __name__ == "__main__":
    main()
