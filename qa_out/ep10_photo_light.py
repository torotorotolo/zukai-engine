# -*- coding: utf-8 -*-
"""⑤c-2 写真90カットの明るさ・コントラストを**全数**測る。焼けた絵を読む。

■ なぜ書き直すか
  ⑤c では「写真の枠を機械で切り出す物差しが作れず」測れなかった（引き継ぎ §6）。
  枠を**絵から探そうとした**のが間違いで、枠は**本番の幾何がすでに持っている**。
  `scene_jiko.photo_box(spec)` が (x, y, w, h) を返す。
  → 記憶 `feedback-gates-must-share-the-production-geometry`（本番と同じ幾何で測る）

■ どこを測るか（暗幕と文字を外す）
  全画面 … 上の暗幕 y<SCRIM_TOP(300) と、側の暗幕（右 x>1150／左 x<770）を外す。
           出典の帯（y>836）も外す
  額装   … 枠の内側を 8px 入る（縁 3px と JPEG のにじみを避ける）
  帯     … 帯の中で、見出し（y<210）と出典（y>836）を外す

■ 何を出すか
  中央値・5%点・95%点・コントラスト（95%−5%）・つぶれ（<32 の割合）・とび（>224 の割合）。
  ⚠️ 写真はデュオトーン（BG2〜#e6eef2）なので**素の 0〜255 には広がらない**。
     しきい値は**この回の90欄の分布**から取る（記憶 feedback-gate-threshold-from-ledger-split）。
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import jiko_style as J  # noqa: E402
import scene_jiko as S  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
SHOT = HERE / "out" / "jiko" / "qa_ep10-r01"


def clean_box(spec):
    """測ってよい矩形 (x0, y0, x1, y1)。暗幕・見出し・出典を外したあと。"""
    x, y, w, h = S.photo_box(spec)
    x0, y0, x1, y1 = x, y, x + w, y + h
    if spec.get("panel"):
        return (x0 + 8, y0 + 8, x1 - 8, y1 - 8)
    if spec.get("band"):
        return (x0, max(y0, 210), x1, min(y1, 836))
    # 全画面
    y0, y1 = max(y0, S.SCRIM_TOP), min(y1, 836)
    if spec.get("side", "right") == "right":
        x1 = min(x1, 1150)
    else:
        x0 = max(x0, 770)
    return (x0, y0, x1, y1)


def main():
    rows = []
    for cid in S.ORDER:
        spec = S.SPEC.get(cid) or {}
        if not spec.get("photo") or spec.get("fig"):
            continue
        p = SHOT / f"cut_{cid}.jpg"
        if not p.exists():
            print(f"🔴 {cid}: 焼けた絵が無い（{p.name}）。0で埋めずに止める")
            return 2
        x0, y0, x1, y1 = [int(round(v)) for v in clean_box(spec)]
        with Image.open(p) as im:
            g = np.asarray(im.convert("L"), dtype=np.uint8)
        if x1 - x0 < 40 or y1 - y0 < 40:
            print(f"🔴 {cid}: 測る窓が小さすぎる {x1 - x0}×{y1 - y0}")
            return 2
        a = g[y0:y1, x0:x1].astype(np.float32)
        p5, p50, p95 = np.percentile(a, [5, 50, 95])
        rows.append(dict(cid=cid, kind=("額装" if spec.get("panel")
                                        else "帯" if spec.get("band") else "全画面"),
                         photo=spec.get("photo", "").split("/")[-1],
                         w=x1 - x0, h=y1 - y0, med=p50, p5=p5, p95=p95,
                         con=p95 - p5, dark=float((a < 32).mean()) * 100,
                         blow=float((a > 224).mean()) * 100,
                         sub=str(spec.get("s", ""))[:22]))
    if not rows:
        print("🔴 写真カットが1つも取れていない（fail closed）")
        return 2
    med = np.array([r["med"] for r in rows])
    con = np.array([r["con"] for r in rows])
    print(f"■ 写真カット {len(rows)} 欄を、本番の幾何（photo_box）で切って測った")
    print(f"  中央値の分布 … 下から 5%={np.percentile(med, 5):.1f} "
          f"25%={np.percentile(med, 25):.1f} 中央={np.median(med):.1f} "
          f"75%={np.percentile(med, 75):.1f} 95%={np.percentile(med, 95):.1f}")
    print(f"  コントラスト … 5%={np.percentile(con, 5):.1f} 中央={np.median(con):.1f} "
          f"95%={np.percentile(con, 95):.1f}")
    print()
    print("  暗いほうから10欄（中央値）")
    for r in sorted(rows, key=lambda r: r["med"])[:10]:
        print(f"   {r['cid']} {r['kind']:4s} 中央 {r['med']:5.1f}  5%{r['p5']:5.1f} 95%{r['p95']:5.1f}"
              f"  コントラスト {r['con']:5.1f}  つぶれ {r['dark']:4.1f}%  {r['photo'][:26]}")
    print("\n  明るいほうから10欄（中央値）")
    for r in sorted(rows, key=lambda r: -r["med"])[:10]:
        print(f"   {r['cid']} {r['kind']:4s} 中央 {r['med']:5.1f}  5%{r['p5']:5.1f} 95%{r['p95']:5.1f}"
              f"  コントラスト {r['con']:5.1f}  とび {r['blow']:4.1f}%  {r['photo'][:26]}")
    print("\n  コントラストが低いほうから10欄")
    for r in sorted(rows, key=lambda r: r["con"])[:10]:
        print(f"   {r['cid']} {r['kind']:4s} コントラスト {r['con']:5.1f}  中央 {r['med']:5.1f}"
              f"  つぶれ {r['dark']:4.1f}%  とび {r['blow']:4.1f}%  {r['photo'][:26]}")
    print("\n  ⑤c が疑いに積んだ8欄（分布のどこに居るか）")
    order_med = {r["cid"]: i for i, r in enumerate(sorted(rows, key=lambda r: r["med"]))}
    order_con = {r["cid"]: i for i, r in enumerate(sorted(rows, key=lambda r: r["con"]))}
    by = {r["cid"]: r for r in rows}
    for cid in ["c105", "c416", "c519", "c520", "c703", "c715", "c808", "c109"]:
        r = by.get(cid)
        if not r:
            print(f"   {cid} … 写真カットではない（図を持つ）ので、この物差しには載らない")
            continue
        print(f"   {cid} {r['kind']:4s} 中央 {r['med']:5.1f}（暗い順 {order_med[cid] + 1}/{len(rows)}）"
              f"  コントラスト {r['con']:5.1f}（低い順 {order_con[cid] + 1}/{len(rows)}）"
              f"  つぶれ {r['dark']:4.1f}%  とび {r['blow']:4.1f}%")
    import json
    (HERE / "qa_out" / "ep10_photo_light.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n（全 {len(rows)} 欄の値は qa_out/ep10_photo_light.json）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
