# -*- coding: utf-8 -*-
"""ep8 ⑤c' ── 「焼けた絵」と「素材＋本番の幾何」が一致するかを数字で決める。

⚠️ きっかけ＝c705 の時刻の焼き込み。道具（`ep8_burnedin.py`）は画面 (263,283) に
   206x22px で出ると言うのに、**焼けた絵はそこが空の夜空**だった。
   → [[feedback-local-render-path-differs-from-the-baden-one]]「絵が正本」。
     どちらの物差しが絵を測っているのかを決める。

やり方＝素材を本番の切り出し窓で切り、貼り箱の大きさへ縮めて、
       焼けた絵の同じ場所と**画素で**突き合わせる。
       一致すれば幾何は正しい＝OCR の箱の側がおかしい。
       一致しなければ**素材が入れ替わっている**（OCR の台帳が古い）。
"""
import json
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import check_slide as CS  # noqa: E402

REF = ROOT / "ref"
QA = ROOT / "out/jiko/qa_ep8-r01"
ocr = json.loads((REF / "ep8" / "ocr_slides.json").read_text(encoding="utf-8"))
sm, po, bo, skip = CS.production_inputs()

TARGETS = ["c705", "c711", "c715", "c717", "c725", "c901", "c302"]

for cid in TARGETS:
    name = po.get(cid)
    spec = sm[cid]
    box = bo[cid]
    with Image.open(REF / name) as im:
        src = im.convert("RGB")
        sw, sh = src.size
    rec = ocr.get(Path(name).name)
    print("─" * 74)
    print(f"■ {cid}   素材 {Path(name).name}  実寸 {sw}x{sh}")
    if rec:
        print(f"   OCR 台帳が覚えている大きさ = {tuple(rec['size'])}"
              f"   {'✅ 一致' if tuple(rec['size']) == (sw, sh) else '🔴🔴 食い違う＝台帳が古い'}")
    with Image.open(QA / f"cut_{cid}.jpg") as im:
        baked = np.asarray(im.convert("RGB")).astype(np.float64)

    best = None
    for k in (0.0, 0.5, 1.0):
        r = CS.crop_rect(sw, sh, box, k, float(spec.get("bias", 0.5)),
                         float(spec.get("xbias", 0.5)), float(spec.get("zoom", 1.0)))
        cut = src.crop((int(r["left"]), int(r["top"]),
                        int(r["left"] + r["cw"]), int(r["top"] + r["ch"])))
        cut = cut.resize((int(r["w"]), int(r["h"])), Image.LANCZOS)
        ca = np.asarray(cut).astype(np.float64)
        bx, by = int(box[0]), int(box[1])
        sub = baked[by:by + ca.shape[0], bx:bx + ca.shape[1]]
        if sub.shape != ca.shape:
            print(f"   k={k}: 形が合わない {sub.shape} 対 {ca.shape}")
            continue
        # 暗幕ぶんの明るさの違いは割り引いて、**模様**が合うかを見る
        a1 = ca.mean(axis=2)
        a2 = sub.mean(axis=2)
        if a1.std() < 1e-6 or a2.std() < 1e-6:
            corr = float("nan")
        else:
            corr = float(np.corrcoef(a1.ravel(), a2.ravel())[0, 1])
        scale = a2.mean() / max(a1.mean(), 1e-6)
        print(f"   k={k}: 模様の相関 {corr:+.3f}   明るさ比 {scale:.3f}"
              f"（暗幕 veil={spec.get('veil')}）")
        if best is None or (corr == corr and corr > best[1]):
            best = (k, corr)
    if best and best[1] == best[1]:
        v = "✅ 素材と焼けた絵は同じもの" if best[1] > 0.8 else \
            ("⚠️ 部分的にしか合わない" if best[1] > 0.4 else
             "🔴🔴 **別の絵が焼かれている**")
        print(f"   ⇒ いちばん合う k={best[0]} 相関 {best[1]:+.3f}  {v}")
    print()
