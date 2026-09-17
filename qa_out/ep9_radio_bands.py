# -*- coding: utf-8 -*-
"""⑤c' 机上：radio の帯（bands）が、その時間に送信の無い段へ四角を出すカットを全数で数える。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import scene_jiko as S  # noqa: E402

n_cut = n_band = 0
for cid in S.ORDER:
    fig = (S.SPEC.get(cid) or {}).get("fig")
    if not fig or fig[0] != "radio":
        continue
    kw = fig[1]
    bands = kw.get("bands") or []
    if not bands:
        continue
    n_cut += 1
    lanes = kw["lanes"]
    for b in bands:
        n_band += 1
        empty = []
        for i, name in enumerate(lanes):
            hit = [e for e in kw["events"] if e.get("lane", 0) == i and
                   (e["a"] <= b["b"] and (e.get("b") if e.get("b") is not None else e["a"]) >= b["a"])]
            if not hit:
                empty.append(name)
        print(f"{cid} 帯「{b.get('t', '')}」{b['a']}〜{b['b']}  段 {len(lanes)}"
              f"  送信の無い段に四角: {'／'.join(empty) if empty else 'なし'}")
print(f"帯のある radio カット {n_cut}・帯 {n_band}")
