# -*- coding: utf-8 -*-
"""19本目 ⑥：同じ版（0dcaa9c）の Actions の検品画像 × 見終わった焼き ep19_c7（4ced951）を1枚ずつ照らす。
md5 が違う物は、原寸の灰色の差 48 超の画素の数（チャット7 の物差し＝陰性対照10すべて0）で「本当に変わった」かを分ける。"""
import hashlib
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(r"C:\Users\konar\Desktop\zukai-engine")
new_root = REPO / "out" / "jiko" / "qa_ep19_r01chk_dl"
old = REPO / "out" / "jiko" / "qa_ep19_c7"
cands = [p for p in new_root.rglob("*.jpg")]
newd = {p.name: p for p in cands}
oldd = {p.name: p for p in old.glob("*.jpg")}
md5 = lambda p: hashlib.md5(p.read_bytes()).hexdigest()
both = sorted(set(newd) & set(oldd))
only_new, only_old = sorted(set(newd) - set(oldd)), sorted(set(oldd) - set(newd))
same, diff = 0, []
for n in both:
    if md5(newd[n]) == md5(oldd[n]):
        same += 1
        continue
    a = np.asarray(Image.open(newd[n]).convert("L"), dtype=np.int16)
    b = np.asarray(Image.open(oldd[n]).convert("L"), dtype=np.int16)
    if a.shape != b.shape:
        diff.append((n, -1, "大きさが違う"))
        continue
    d = np.abs(a - b)
    big = int((d > 48).sum())
    ys, xs = np.where(d > 48)
    box = f"x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}" if big else ""
    diff.append((n, big, box))
print(f"新 {len(newd)} 枚・旧 {len(oldd)} 枚・共通 {len(both)}・md5 一致 {same}・違う {len(diff)}")
print("新だけ:", only_new[:20], "…" if len(only_new) > 20 else "")
print("旧だけ:", only_old[:20], "…" if len(only_old) > 20 else "")
real = [x for x in diff if x[1] != 0]
print(f"■ 差48超の画素がある（本当に変わった）{len(real)} 枚")
for n, big, box in sorted(real, key=lambda x: -x[1]):
    print(f"  {n}\t{big}\t{box}")
print(f"■ md5 は違うが差48超は 0（焼きの揺れ）{len(diff) - len(real)} 枚")
