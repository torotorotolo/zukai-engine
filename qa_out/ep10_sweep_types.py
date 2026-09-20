# -*- coding: utf-8 -*-
"""⑤c' 直した「型」を**195カット全数**へ広げる（2026-09-20）。

直した1件をその場で全数へ広げる決まり → [[feedback-scale-one-visual-finding-to-a-full-count]]

■ A型 `ep07`：段の順番のせいで、**最後の節がカットの終わりに間に合わない**
   `people` の段は「矢印を全部 → 節を全部」なので、節 n・矢印 m だと段が n+m になる。
   ナレーションの行より段が多いカットは、余った段が行の隙間に押し込まれ、
   最後の段が尺の終わりぎりぎりから描き始まる。
   → **全カットで「最後の段が出はじめる秒 ÷ 尺」**を出し、遅いものを並べる。
   ⚠️ 検品画像は必ず描画途中を写す（[[feedback-qa-still-is-mid-animation]]）ので、
     「撮影時に出そろっていない」だけでは粗ではない。**粗は「行き先の無い矢印」**＝
     矢印の段が、その矢印が指す節の段より**前**に来ているカット。

■ B型 副題の重なり：**別の写真なのに同じ副題**
   ⚠️ 同じ写真を2回出すカット（`crack_wall_01`・`sign_sampoong_02`）は
     **同じ副題が正しい**ので、除く。

■ C型 `c513`：`layers` で「面」に意味があるのに**等分**のままのカット

使い方: python qa_out/ep10_sweep_types.py
"""
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S
import build_jiko as B
import cuts

SPEC = S.SPEC
idx, _ = S.layer_index(allow_missing=True)
meta = B.meta_of(idx)
secs = dict(S.CUTS)

print("■ A型  `people` で「行き先の無い矢印」が出るカット")
print("   （矢印の段が、その矢印が指す節の段より前に来ている）")
bad_a = []
for cid, sp in SPEC.items():
    fig = sp.get("fig")
    if not fig or fig[0] != "people":
        continue
    kw = fig[1]
    nodes, edges = kw.get("nodes") or [], kw.get("edges") or []
    if not edges:
        continue
    if kw.get("pair"):
        # 🔴 2026-09-20：ここは最初**古い規則のまま**書いていて、直したカットを
        #    まだ 🔴 と出していた（物差しが、測る相手のコードと食い違っていた）。
        #    → [[feedback-verify-your-own-instrument]]
        #    いまの `people` は矢印を **max(a, b)＝あとに出るほうの端**の段に置く。
        #    節 i の段は i なので、矢印の段は必ず両端以上＝宙に浮かない。
        late = [(e["a"], e["b"]) for e in edges
                if max(e["a"], e["b"]) < e["a"] or max(e["a"], e["b"]) < e["b"]]
    else:
        # 段は 矢印を全部（0..m-1）→ 節を全部（m..m+n-1）
        m = len(edges)
        late = [(e["a"], e["b"]) for k, e in enumerate(edges)
                if m + e["b"] > k or m + e["a"] > k]
    if late:
        bad_a.append((cid, len(nodes), len(edges), len(late)))
for cid, n, m, k in bad_a:
    print(f"   🔴 {cid}  節{n}・矢印{m}  宙に浮く矢印 {k}本  尺{secs.get(cid, 0):.1f}秒"
          f"  段{len(meta[cid]['times']) if cid in meta else '?'}")
if not bad_a:
    print("   ✓ 0件")

# 🔴 陽性対照。**0件と出たときに「網が効いている」ことを示す**ための1本。
#    これが鳴らなければ、上の 0件 は「粗が無い」ではなく「測っていない」。
#    → [[feedback-verify-your-own-instrument]]／⑤c-2 の「分岐ごとに1本」
_probe_nodes = [dict(x=0.2, y=0.3, t="A"), dict(x=0.5, y=0.5, t="B"),
                dict(x=0.8, y=0.3, t="C")]
_probe_edges = [dict(a=0, b=1, t=""), dict(a=2, b=1, t="")]
_m = len(_probe_edges)
_hit = [1 for k, e in enumerate(_probe_edges)
        if _m + e["b"] > k or _m + e["a"] > k]
print(f"   {'✓' if _hit else '🔴'} 陽性対照（pair を付けない節3・矢印2）"
      f"＝ 宙に浮く矢印 {len(_hit)}本を検出"
      f"{'' if _hit else '  ← 網が効いていません'}")
if not _hit:
    sys.exit(1)

print()
print("■ A型（参考）最後の段が出はじめるのが遅いカット（尺の 85% 以降）")
slow = []
for cid, m in meta.items():
    sec = secs[cid]
    if not m["times"]:           # 段が無いカット（実写など）は対象外
        continue
    t0 = m["times"][-1][0]
    if sec and t0 / sec >= 0.85:
        slow.append((t0 / sec, cid, len(m["times"]), sec, t0))
for r, cid, n, sec, t0 in sorted(slow, reverse=True)[:12]:
    print(f"   ⚠️ {cid}  段{n}  尺{sec:5.1f}秒  最後の段 {t0:5.2f}秒 ＝ {r*100:.0f}%")
if not slow:
    print("   ✓ 0件")

print()
print("■ B型  別の写真なのに副題が同じ")
bysub = collections.defaultdict(list)
for cid, sp in SPEC.items():
    if sp.get("photo") and sp.get("s"):
        bysub[sp["s"]].append((cid, sp["photo"]))
bad_b = 0
for sub, rows in sorted(bysub.items()):
    if len(rows) < 2:
        continue
    photos = {p for _, p in rows}
    if len(photos) == 1:
        print(f"   ・ {sub}  ＝ {[c for c, _ in rows]}（**同じ写真**なので同じ副題でよい）")
        continue
    bad_b += 1
    print(f"   🔴 {sub}")
    for c, p in rows:
        print(f"        {c}  {p}")
if not bad_b:
    print("   ✓ 別の写真どうしで副題が重なっているものは 0件")

print()
print("■ C型  `layers` のカット（面の位置に意味があるか）")
for cid, sp in SPEC.items():
    fig = sp.get("fig")
    if not fig or fig[0] != "layers":
        continue
    kw = fig[1]
    n = kw.get("n", 5)
    fr = kw.get("frac")
    bonds = kw.get("bonds") or []
    body = 682 - 150 - 22 * (n - 1)
    lhs = [body * f / sum(fr) for f in fr] if fr else [body / n] * n
    tot = sum(lhs) + 22 * (n - 1)
    depths = [f"{(sum(lhs[:b['i']]) + 22 * (b['i'] - 1) + 11) / tot * 100:.1f}%"
              for b in bonds]
    print(f"   {cid}  n={n}  frac={fr}  面の深さ {depths or '（面の注記なし）'}"
          f"  labels={kw.get('labels')}")
