# -*- coding: utf-8 -*-
"""束③（§R-4）の直す先を数える。

「答えが `v` の段と `d` の段に割れる」と言うとき、**`d` が答えかどうか**が肝。
  ・段に `v` がある … その段の `d` は**補足**（触らない。⑤c' 1巡目で決めた）
  ・段に `v` が無い … その段の `d` が**答え**（＝これが小さいと割れて見える）

ここで数えるのは「**同じカットの中に、v の答えと d の答えが混じる**」段だけ。
⚠️ 陽性対照 ＝ §R-4 が挙げた `c215` `c112` `c201` が出ること。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import fontmetrics as fm                                   # noqa: E402
from cuts import SPEC                                      # noqa: E402


def maxw_of(spec):
    if spec.get("band"):
        return 1500
    return 700          # panel= の額装は別勘定。ここでは全画面の注記だけ見る


rows_mixed = 0
cuts_mixed = []
for cid, sp in SPEC.items():
    anns = sp.get("ann") or []
    if not anns or sp.get("panel"):
        continue
    mw = maxw_of(sp)
    ans = []            # (段, 種別, 級数, 文字列)
    for i, a in enumerate(anns):
        ts = fm.fit(a["t"], mw, "Noto", cap=a.get("ts", 46), floor=24) if a.get("t") else 0
        if a.get("v"):
            s = fm.fit(a["v"], mw, "Dela", cap=a.get("vs", 96), floor=30)
            ans.append((i, "v", s, a["v"]))
        elif a.get("d"):
            dcap = max(a.get("ds", 34), ts)
            s = fm.fit(a["d"], mw, "Noto", cap=dcap, floor=22)
            ans.append((i, "d", s, a["d"]))
    kinds = {k for _, k, _, _ in ans}
    if kinds == {"v", "d"}:
        vmax = max(s for _, k, s, _ in ans if k == "v")
        dmin = min(s for _, k, s, _ in ans if k == "d")
        if vmax - dmin >= 24:
            cuts_mixed.append((cid, vmax - dmin, ans))
            rows_mixed += sum(1 for _, k, _, _ in ans if k == "d")

cuts_mixed.sort(key=lambda r: -r[1])
print(f"🔴 1枚の中で「v の答え」と「d の答え」が 24px 以上ひらく ＝ "
      f"{len(cuts_mixed)}カット / d の段 {rows_mixed}段")
for cid, gap, ans in cuts_mixed:
    body = " ".join(f"{k}{s}「{t[:12]}」" for _, k, s, t in ans)
    print(f"  {cid}  開き{gap:3.0f}px  {body}")

pos = [c for c, _, _ in cuts_mixed]
print("\n陽性対照 c215 =", "出た" if "c215" in pos else "🔴 落ちた",
      "／ c112 =", "出た" if "c112" in pos else "🔴 落ちた",
      "／ c201 =", "出た" if "c201" in pos else "🔴 落ちた")
