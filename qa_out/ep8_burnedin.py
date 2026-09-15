# -*- coding: utf-8 -*-
"""⑤c §A-7：**焼き込みの英字が画面に出ているカット**を全数で当てる。

きっかけ＝シート sheet_04 の `c205` に "Debris forward of LH wing" が読めた。
門番 `check_slide` は G-13（字幕帯の中）と G-14（**こちらの文字が上に載る**）しか見ないので、
「絵の中に英字がただ見えている」には構造上鳴らない
（記憶 [[feedback-gates-dont-see-text-burned-into-the-picture]]／
　[[feedback-gates-blind-spot-is-the-scan-direction]]）。

→ 目で見えた1件を式にして全数へ（記憶 [[feedback-scale-one-visual-finding-to-a-full-count]]）。

やり方＝OCR が拾った行の箱を、本番の `crop_rect` / `to_screen` で**画面座標**へ写し、
切り出し窓の中に残っている行を、画面上の大きさ（px）つきで並べる。
k=0 と k=1 の両端を見る（寄りが進むと入ってくる／出ていく行があるため）。
"""
import json
import sys
from pathlib import Path

REPO = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(REPO / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image  # noqa: E402
import check_slide as CS  # noqa: E402

REF = REPO / "ref"
MIN_H = 12      # 画面上の高さがこれ未満なら「読めない」とみなす（1080p で 12px）
MIN_W = 40

ocr = json.loads((REF / "ep8" / "ocr_slides.json").read_text(encoding="utf-8"))
sm, po, bo, skip = CS.production_inputs()

rows = []
for cid in sorted(sm):
    name = po.get(cid)
    if not name:
        continue
    o = ocr.get(Path(name).name)
    if not o:
        continue
    with Image.open(REF / name) as im:
        sw, sh = im.size
    spec = sm[cid]
    for k in (0.0, 1.0):
        r = CS.crop_rect(sw, sh, bo[cid], k, float(spec.get("bias", .5)),
                         float(spec.get("xbias", .5)), float(spec.get("zoom", 1.0)))
        for L in o["lines"]:
            bx = L["box"]
            # 切り出し窓と重なっている割合（1.0＝行が丸ごと画面に出る）
            ix = max(0.0, min(bx[2], r["left"] + r["cw"]) - max(bx[0], r["left"]))
            iy = max(0.0, min(bx[3], r["top"] + r["ch"]) - max(bx[1], r["top"]))
            area = (bx[2] - bx[0]) * (bx[3] - bx[1])
            if not area or ix * iy / area < 0.5:
                continue
            s = CS.to_screen(bx, r)
            w, h = s[2] - s[0], s[3] - s[1]
            if h < MIN_H or w < MIN_W:
                continue
            rows.append((cid, k, Path(name).name, round(w), round(h),
                         round(s[0]), round(s[1]), ix * iy / area, L["text"]))

# カットごとに「いちばん大きい行」だけを代表にする
best = {}
for r in rows:
    key = r[0]
    if key not in best or r[4] > best[key][4]:
        best[key] = r

print(f"■ 写真のあるカット {sum(1 for c in sm if po.get(c))} 件を、OCR の行 "
      f"{sum(len(v['lines']) for v in ocr.values())} 行と突き合わせた")
print(f"■ 画面に**読める大きさ**（高さ {MIN_H}px 以上・幅 {MIN_W}px 以上・行の半分以上が窓の中）"
      f"で焼き込みが出るカット＝**{len(best)}件**\n")
print("カット  画面での大きさ  位置(x,y)   入り具合  素材                  読めた文字")
for cid, k, nm, w, h, x, y, cov, txt in sorted(best.values(), key=lambda r: -r[4]):
    band = "🔴字幕帯" if y > 900 else ("見出し帯" if y < 200 else "")
    print(f"{cid:6} {w:5}x{h:<4}px  ({x:4},{y:4})  {cov:5.0%}  {nm:<22} {txt[:34]!r} {band}")

print("\n■ 素材ごとの件数（同じ写真を何度も敷いた欄がそのまま効く）")
per = {}
for cid, k, nm, *_ in best.values():
    per[nm] = per.get(nm, 0) + 1
for nm, n in sorted(per.items(), key=lambda kv: -kv[1]):
    print(f"   {nm:<24} {n}カット")
