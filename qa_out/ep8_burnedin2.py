# -*- coding: utf-8 -*-
"""ep8 ⑤c' ── §A-7「焼き込みの英字」を**本番と同じ幾何で**測り直す。

🔴🔴 ⑤c の `ep8_burnedin.py` は **`trim`（写真を先に切り落とす割合）を1つも持っていない**
   （`grep trim` が0件）。`CS.crop_rect` を**紙いちめんの原画**に当てていたので、
   `ss.vid` の欄（`fb_*.jpg`）は**切り落とした側にある文字まで「画面に出る」と数えていた**。

   これは `check_slide.py:380` に「2026-09-09（6本目 ⑤c）**切り落としを、この門番も通す**」と
   書いてある、**いちど直したのと同じ穴**を、新しい道具で作り直したもの。
   ＝[[feedback-gates-must-share-the-production-geometry]]
     ／[[feedback-gates-go-stale-when-upstream-changes]]

直し方＝自分で幾何を組まず、本番の `check_slide.cut_geom()` をそのまま呼ぶ。

陽性対照＝`trim` のあるカットと無いカットを並べ、**trim 有りだけが減る**ことを見る。
"""
import json
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import check_slide as CS  # noqa: E402

REF = ROOT / "ref"
MIN_H, MIN_W = 12, 40

ocr = json.loads((REF / "ep8" / "ocr_slides.json").read_text(encoding="utf-8"))
sm, po, bo, skip = CS.production_inputs()

rows, dropped = [], []
for cid in sorted(sm):
    spec = sm[cid]
    g = CS.cut_geom(cid, spec, ocr, po, bo, skip)
    if not g:
        continue
    seen = {}
    for k in (0.0, 1.0):
        r = CS.crop_rect(g["sw"], g["sh"], bo[cid], k,
                         float(spec.get("bias", 0.5)),
                         float(spec.get("xbias", 0.5)),
                         float(spec.get("zoom", 1.0)))
        for ln in g["lines"]:
            b = ln["box"]
            # 窓のなかに半分以上残っているか
            ix0, iy0 = max(b[0], r["left"]), max(b[1], r["top"])
            ix1 = min(b[2], r["left"] + r["cw"])
            iy1 = min(b[3], r["top"] + r["ch"])
            if ix1 <= ix0 or iy1 <= iy0:
                continue
            frac = ((ix1 - ix0) * (iy1 - iy0)) / max(1e-6,
                                                     (b[2] - b[0]) * (b[3] - b[1]))
            if frac < 0.5:
                continue
            s = CS.to_screen(b, r)
            w, h = s[2] - s[0], s[3] - s[1]
            if h < MIN_H or w < MIN_W:
                continue
            key = ln["text"][:24]
            cand = (w, h, (s[0] + s[2]) / 2, (s[1] + s[3]) / 2, frac, ln["text"])
            if key not in seen or w * h > seen[key][0] * seen[key][1]:
                seen[key] = cand
    for key, (w, h, cx, cy, frac, text) in seen.items():
        rows.append((cid, w, h, cx, cy, frac, g["name"], text,
                     bool(g["trim"])))

rows.sort(key=lambda t: -t[1] * t[2])
print("=" * 88)
print("■ 本番と同じ幾何（trim 込み）で数え直した「画面に出る焼き込みの英字」")
print("=" * 88)
print(f"  {'カット':<7}{'大きさ':>12}  {'位置':>13}  {'残り':>5}  素材")
for cid, w, h, cx, cy, frac, name, text, tr in rows:
    band = ""
    if cy > 900:
        band = " 🔴字幕帯"
    elif cy < 200:
        band = " 🔴見出し帯"
    print(f"  {cid:<7}{w:5.0f}x{h:<5.0f}px  ({cx:5.0f},{cy:5.0f})  "
          f"{100 * frac:4.0f}%  {name:<22}{'[trim]' if tr else '      '}"
          f" {text[:34]!r}{band}")
print()
print(f"  ⇒ **{len({r[0] for r in rows})} カット / {len(rows)} 行**")
print()

OLD = ["c901", "c211", "c621", "c705", "c711", "c715", "c717", "c725",
       "c205", "c212", "c302", "c306", "c201", "c820"]
now = {r[0] for r in rows}
print("  ▼ ⑤c が名指しした欄が、trim 込みでも残るか（陽性/陰性の対照）")
for cid in OLD:
    spec = sm.get(cid, {})
    tr = CS.trim_of(spec) if spec else None
    mark = "✅ 残る" if cid in now else "🔴🔴 **消える＝⑤c の見立ては誤り**"
    print(f"    {cid:<7}{'trim あり' if tr else 'trim なし '}  {mark}")
