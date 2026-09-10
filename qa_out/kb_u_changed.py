# -*- coding: utf-8 -*-
"""r02 と r03 を画素で突き合わせ、**変わったカット**を出す。

⚠️ [[feedback-render-is-not-fully-deterministic]]：1画素の差で版ずれを判断しない。
   ここは「差>16 の画素が 0.05% を超えたら変わった」で数える（§Q-6 検証① と同じ物差し）。

  python qa_out/kb_u_changed.py            … 変わった／変わっていないを数える
  python qa_out/kb_u_changed.py --list     … 差の大きい順に全部出す
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent.parent
# 🔴 2026-09-10（⑤c' 3巡目）：巡が増えるたびに書き換えていたので引数で受けるようにした。
#    ⚠️ 既定は**いちばん新しい2つ**ではなく、書いてある2つ（黙って別の巡を比べない）。
#      `python qa_out/kb_u_changed.py r04 r05 --list`
_a = [x for x in sys.argv[1:] if not x.startswith("--")]
A = HERE / f"out/jiko/qa_keybridge-{_a[0] if len(_a) > 0 else 'r03'}"
B = HERE / f"out/jiko/qa_keybridge-{_a[1] if len(_a) > 1 else 'r04'}"
print(f"■ 比べる: {A.name} → {B.name}")


def diff(pa, pb):
    a = np.asarray(Image.open(pa).convert("RGB"), dtype=np.int16)
    b = np.asarray(Image.open(pb).convert("RGB"), dtype=np.int16)
    if a.shape != b.shape:
        return 100.0, 255.0
    d = np.abs(a - b).max(axis=2)
    return float((d > 16).mean() * 100), float(d.mean())


rows = []
missing = []
for pa in sorted(A.glob("cut_*.jpg")):
    pb = B / pa.name
    if not pb.exists():
        missing.append(pa.stem[4:])
        continue
    pct, avg = diff(pa, pb)
    rows.append((pct, avg, pa.stem[4:]))

rows.sort(reverse=True)
changed = [r for r in rows if r[0] > 0.05]
print(f"突き合わせ {len(rows)} カット（r03 対 r04）")
print(f"  絵が変わった（差>16 の画素が 0.05% 超） … {len(changed)}")
print(f"  変わっていない                          … {len(rows) - len(changed)}")
if missing:
    print(f"  🔴 r03 に無い … {len(missing)}: {' '.join(missing[:10])}")

# 🔴 予測との突き合わせ（§Q-6 検証① と同じ形）。予測＝`kb_u_predict.py` の SVG 差
#    ＋ `footage.USE` が NTSB のカット（出典行の直しはローカルの SVG に出ないため）
exp = HERE / "qa_out/kb_u_expect.txt"
if exp.exists():
    want = {l.strip() for l in exp.read_text(encoding="utf-8").split() if l.strip()}
    got = {c for _, _, c in changed}
    miss = sorted(want - got)
    extra = sorted(got - want)
    print(f"\n予測 {len(want)} 対 実測 {len(got)}")
    print(f"  🔴 変わるはずが変わっていない … {len(miss)}"
          + (": " + " ".join(miss) if miss else ""))
    print(f"  🔴 予測になかったのに変わった … {len(extra)}"
          + (": " + " ".join(extra) if extra else ""))

n = len(rows) if "--list" in sys.argv else 30
print("\n差の大きい順")
for pct, avg, cid in rows[:n]:
    print(f"  {cid}  {pct:6.2f}%  平均差 {avg:5.2f}")
