# -*- coding: utf-8 -*-
"""ep8 ⑤c' ── 「同じ絵」3組を、⑤c とは別の道具で確かめ直す。

⚠️ ⑤c は「写真の枠だけを切り出して平均の画素差」で 0.0 と出した。
   引き写さずに自分で確かめる（[[feedback-verify-inherited-claims]]）。
   ここでは**素材のファイルと切り出し窓**を本番の幾何から出す
   （[[feedback-gates-must-share-the-production-geometry]]）。
   素材が同じで窓も同じなら、絵は必ず同じ＝画素を見るまでもなく決まる。

陽性対照＝わざと別の組（c305 × c707）も並べる。
"""
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image  # noqa: E402
import check_slide as CS  # noqa: E402

REF = ROOT / "ref"
sm, po, bo, skip = CS.production_inputs()

PAIRS = [("c305", "pr07"), ("c707", "c817"), ("ep01", "ep02"),
         ("c309", "c315"), ("c705", "c711"), ("c715", "c717"),
         ("c305", "c707")]   # ← 陽性対照（別の組）


def info(cid):
    name = po.get(cid)
    if not name:
        return None
    spec = sm[cid]
    with Image.open(REF / name) as im:
        sw, sh = im.size
    r = CS.crop_rect(sw, sh, bo[cid], 0.0, float(spec.get("bias", 0.5)),
                     float(spec.get("xbias", 0.5)), float(spec.get("zoom", 1.0)))
    return name, (sw, sh), r, spec


print("=" * 78)
print("■ 素材のファイルと切り出し窓を突き合わせる")
print("=" * 78)
for a_, b_ in PAIRS:
    ia, ib = info(a_), info(b_)
    print(f"  ── {a_} × {b_} " + "─" * 46)
    if ia is None or ib is None:
        print(f"      写真が無い（{a_}={ia is not None} {b_}={ib is not None}）")
        print()
        continue
    na, _, ra, sa = ia
    nb, _, rb, sb = ib
    KEYS = ("left", "top", "cw", "ch")          # 切り出し窓そのもの

    def win(r):
        return tuple(round(float(r[k]), 2) for k in KEYS)

    same_src = Path(na).name == Path(nb).name
    same_win = win(ra) == win(rb)
    print(f"      素材 {a_}: {Path(na).name}")
    print(f"      素材 {b_}: {Path(nb).name}")
    print(f"      窓 {a_}: left,top,cw,ch = {win(ra)}   貼り箱 {ra['box']}")
    print(f"      窓 {b_}: left,top,cw,ch = {win(rb)}   貼り箱 {rb['box']}")
    print(f"      veil {a_}={sa.get('veil')} / {b_}={sb.get('veil')}   "
          f"zoom {sa.get('zoom', 1.0)} / {sb.get('zoom', 1.0)}")
    if same_src and same_win:
        print(f"      ⇒ 🔴🔴 **素材も窓も同じ＝まったく同じ絵**")
    elif same_src:
        print(f"      ⇒ ⚠️ 素材は同じだが窓が違う")
    else:
        print(f"      ⇒ ・ 別の素材")
    print()
