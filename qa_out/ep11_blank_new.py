# -*- coding: utf-8 -*-
"""⑤c-3 で足した11点だけを `check_blank` の本体に通す。

🔴 なぜ要るか＝この機械はコミットの空きが 0.35GB しかなく、
   `check_blank` が全点（87点）を回すと MemoryError で**門番ごと落ちる**
   （→ [[feedback-a-gate-that-throws-measures-nothing]]）。
⚠️ **判定は書き直さない。**`check_blank.scan` と `report` をそのまま呼ぶ
   （物差しを2か所に書かない → [[feedback-verify-your-own-instrument]]）。
"""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import check_blank as CB                                    # noqa: E402
import cuts.ss as CS_                                       # noqa: E402,F401
from check_blank import CS                                  # noqa: E402

NEW = set(sys.argv[1:]) or {
    "c513", "c517", "c519", "c605", "c606", "c613",
    "c803", "c804", "ep01", "ep02", "ep03", "ep04",
}
sm, po, bo, skip = CS.production_inputs()
sm = {c: v for c, v in sm.items() if c in NEW}
print(f"■ ⑤c-3 で足したカットのうち、写真を持つ {len(sm)} 件だけを測る")
CB.CACHE_MAX = 1                       # 1枚ずつ流す（袋に貯めない）
sys.exit(1 if CB.report(CB.scan(sm, po, bo, skip), True, False) else 0)
