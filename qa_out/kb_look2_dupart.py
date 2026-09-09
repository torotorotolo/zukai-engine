# -*- coding: utf-8 -*-
"""同じ絵が2度出ていないかを **画素で** 数える（2026-09-10・2版目）。

⚠️ 1版目は「焼けた画面どうし」を比べたので、**同じ図でも左右の置き場所が違うと
   落ちた**（陽性対照の pr06 ─ ca02 が挙がらなかった）。
   → 置き場所に左右されない **資産のファイルどうし**を比べる形に直した。
⚠️ ファイル名や資産IDで数えてはいけない（別名の同じ図に鳴らない）
   ＝ [[feedback-duplicate-art-needs-pixel-comparison]]。

判定 … 共通の大きさに落として、差>16 の画素が 10%未満なら「視聴者には同じ絵」。
陽性対照 … pr06 と ca02（どちらも kb_p125_fig60.png）が 0% で挙がること。
使い方 … python qa_out/kb_look2_dupart.py
"""
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "tools")
from cuts import SPEC  # noqa: E402

REF = Path("ref")
用 = defaultdict(list)
for cid, spec in SPEC.items():
    if spec.get("photo"):
        用[spec["photo"]].append(cid)

names, arr = [], []
missing = []
for name in sorted(用):
    p = REF / name
    if not p.exists():
        missing.append(name)
        continue
    im = Image.open(p).convert("L").resize((256, 256), Image.BILINEAR)
    names.append(name)
    arr.append(np.asarray(im, np.float32))
if missing:
    print(f"⚠️ 手元に無い資産 {len(missing)}件（ひかえの静止画）: "
          f"{' '.join(Path(m).name for m in missing[:6])} …")
print(f"比べた資産: {len(names)}件／使っているカット "
      f"{sum(len(用[n]) for n in names)}")

hit = []
for i, j in combinations(range(len(names)), 2):
    d = (np.abs(arr[i] - arr[j]) > 16).mean() * 100
    if d < 10.0:
        hit.append((d, names[i], names[j]))
hit.sort()
print(f"\n🔴 別名なのに同じ絵（差>16 が 10%未満）: {len(hit)}組")
for d, a, b in hit:
    print(f"   {d:5.2f}%  {Path(a).name} ─ {Path(b).name}")
    print(f"           {' '.join(用[a])}  ／  {' '.join(用[b])}")

print("\n🔴 同じ資産を2カット以上で使っている:")
for name, ids in sorted(用.items(), key=lambda kv: -len(kv[1])):
    if len(ids) > 1:
        print(f"   {len(ids)}カット  {Path(name).name}  ← {' '.join(sorted(ids))}")
