# -*- coding: utf-8 -*-
"""⑤b-2b の作業用（この回だけ）。**c320 の注記の置き場所を総当たりで測る。**

■ なぜ要るか
  `check_slide` の G-14（こちらの文字が焼き込みの文字に載る）が c320 で鳴る。
  素材（空港の出発案内板）は**画面じゅうが文字**なので、置き場所を勘で動かすと
  往復が増える（[[feedback-context-economy]]）。SPEC を差し替えて1回の起動で全部測る。

使い方: python qa_out/ep7_c320_probe.py
"""
import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S
import check_slide as CS
import footage as _F        # ⚠️ 先に読む。redirect 中だと sys.stdout.reconfigure で落ちる
import check_layout as _CL  # 同じ理由（`my_boxes` が中で読む）

CANDS = [("left", 0.50, 240), ("left", 0.50, 440), ("left", 0.50, 560),
         ("right", 0.50, 560), ("left", 0.30, 344), ("right", 0.30, 240)]

base = dict(S.SPEC["c320"])
for side, bias, ann_y in CANDS:
    S.SPEC["c320"] = dict(base, side=side, bias=bias, ann_y=ann_y)
    buf = io.StringIO()
    with redirect_stdout(buf):
        CS.main()
    hits = [ln for ln in buf.getvalue().splitlines()
            if "c320" in ln or re.search(r"^\s+「", ln)]
    bad = [ln for ln in buf.getvalue().splitlines() if "🔴 c320" in ln]
    print(f"── side={side} bias={bias} ann_y={ann_y} → 🔴 {len(bad)}件")
    for ln in hits[:4]:
        print("   ", ln.strip())
S.SPEC["c320"] = base
