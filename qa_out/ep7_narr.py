# -*- coding: utf-8 -*-
"""⑤b-2b の作業用。**カット id を渡すと、そのカットのナレーションと画面の文字を並べて出す。**

■ なぜ要るか
  `check_echo` の 95件を直すには「そのカットが何を喋っているか」が要る。
  台本（Vault）を grep で1件ずつ引くと往復が増える（[[feedback-context-economy]]）。
  `scene_jiko.SUBS` が同じものを持っているので、ここから引く。

使い方:
  python qa_out/ep7_narr.py c112 c113 c114
  python qa_out/ep7_narr.py --ch c1          # 章まるごと
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S


def show(cid):
    sp = S.SPEC.get(cid)
    if sp is None:
        print(f"── {cid} ── 🔴 SPEC に無い")
        return
    rows = [r["text"] for r in S.SUBS.get(cid, [])]
    print(f"── {cid} ──")
    print(f"  t  : {sp.get('t', '')}")
    print(f"  s  : {sp.get('s', '')}")
    for r in rows:
        print(f"  ナレ: {r}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--ch" in sys.argv:
        pre = args[0]
        ids = [c for c in S.SPEC if c.startswith(pre)]
    else:
        ids = args
    for cid in ids:
        show(cid)
