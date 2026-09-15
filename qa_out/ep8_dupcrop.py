# -*- coding: utf-8 -*-
"""8本目 ⑤c §A-1：同じ写真を敷いた欄の切り出し窓が、本当に別の絵になっているか。

🔴 根拠＝記憶 [[feedback-video-qa-index]] §4「切り出しの遊びを先に測る」。
   キー橋 `kb_pre_deck05.jpg` は縦の遊びが 336px しか無く、bias を動かしても
   **視聴者には同じ絵**で、画素の物差しだけが動いた。

幾何は本番の `check_slide.crop_rect` / `production_inputs()` をそのまま呼ぶ
（[[feedback-gates-must-share-the-production-geometry]]）。

測るもの（1組ずつ）
  遊び      … その写真が bias/xbias で動かせる最大の画素数（sw-cw, sh-ch）
  IoU       … 2つの切り出し窓の重なり率（1.00 = 完全に同じ窓）
  中心の差  … 切り出し窓の中心が何 px ずれているか／それは画面上の何 px か
  面積比    … 寄りの違い（zoom）が効いているか
"""
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(r"C:/Users/konar/Desktop/zukai-engine") / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image  # noqa: E402
import check_slide as CS  # noqa: E402

REF = Path(r"C:/Users/konar/Desktop/zukai-engine") / "ref"

sm, po, bo, skip = CS.production_inputs()

# 素材名 -> [(cid, rect, spec)]
by_photo = {}
for cid in sorted(sm):
    name = po.get(cid)
    if not name:
        continue
    spec = sm[cid]
    with Image.open(REF / name) as im:
        sw, sh = im.size
    r = CS.crop_rect(sw, sh, bo[cid], 0.0, float(spec.get("bias", 0.5)),
                     float(spec.get("xbias", 0.5)), float(spec.get("zoom", 1.0)))
    by_photo.setdefault(Path(name).name, []).append((cid, r, spec, sw, sh))

print(f"■ 写真が映るカット {sum(len(v) for v in by_photo.values())} 件／"
      f"素材 {len(by_photo)} 点。2回以上使った素材だけを見る")
print()

dup = {k: v for k, v in by_photo.items() if len(v) >= 2}
print(f"2回以上使った素材＝{len(dup)}点")
worst = []
for name, uses in sorted(dup.items(), key=lambda kv: -len(kv[1])):
    sw, sh = uses[0][3], uses[0][4]
    print(f"\n── {name}  原画 {sw}×{sh}  使った欄 {len(uses)}："
          f"{' '.join(c for c, *_ in uses)}")
    for cid, r, spec, _, _ in uses:
        playx, playy = sw - r["cw"], sh - r["ch"]
        print(f"   {cid}  bias={spec.get('bias', .5)} xbias={spec.get('xbias', .5)} "
              f"zoom={spec.get('zoom', 1.0)}  窓 {r['cw']:.0f}×{r['ch']:.0f} @"
              f"({r['left']:.0f},{r['top']:.0f})  遊び 横{playx:.0f} 縦{playy:.0f}px")
    for (ca, ra, _, _, _), (cb, rb, _, _, _) in combinations(uses, 2):
        ax0, ay0 = ra["left"], ra["top"]
        ax1, ay1 = ax0 + ra["cw"], ay0 + ra["ch"]
        bx0, by0 = rb["left"], rb["top"]
        bx1, by1 = bx0 + rb["cw"], by0 + rb["ch"]
        ix = max(0.0, min(ax1, bx1) - max(ax0, bx0))
        iy = max(0.0, min(ay1, by1) - max(ay0, by0))
        inter = ix * iy
        ua = ra["cw"] * ra["ch"]
        ub = rb["cw"] * rb["ch"]
        iou = inter / (ua + ub - inter) if (ua + ub - inter) else 0.0
        # 小さいほうの窓のうち何割が相手に含まれるか（＝「片方がもう片方の一部」）
        cover = inter / min(ua, ub) if min(ua, ub) else 0.0
        dcx = abs((ax0 + ax1) / 2 - (bx0 + bx1) / 2)
        dcy = abs((ay0 + ay1) / 2 - (by0 + by1) / 2)
        # 画面に出たときの中心のずれ（画面幅 1920 に換算・小さいほうの窓を基準）
        scr = 1920.0 / min(ra["cw"], rb["cw"])
        area = max(ua, ub) / min(ua, ub)
        flag = ""
        if iou >= 0.80 and area < 1.25:
            flag = "🔴 ほぼ同じ窓"
        elif iou >= 0.60 and area < 1.40:
            flag = "⚠️ 重なりが大きい"
        print(f"   {ca}×{cb}  IoU {iou:.2f}  包含 {cover:.2f}  面積比 {area:.2f}  "
              f"中心差 {dcx:.0f},{dcy:.0f}px（画面換算 {dcx * scr:.0f},{dcy * scr:.0f}px） {flag}")
        if flag:
            worst.append((iou, name, ca, cb, area, flag))

print("\n■ まとめ")
if worst:
    for iou, name, ca, cb, area, flag in sorted(worst, reverse=True):
        print(f"  {flag}  {ca}×{cb}  IoU {iou:.2f} 面積比 {area:.2f}  {name}")
else:
    print("  ✓ 2回以上使った素材のどの組も IoU 0.60 未満（＝別の窓）")
