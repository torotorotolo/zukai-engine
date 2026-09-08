# -*- coding: utf-8 -*-
"""⚠️ **仮の道具**。`footage.USE` を書き終えたら消すこと（2026-09-08 ⑤b-2 新設）。

■ なぜ要るか（この日に実際に踏んだ）
  実写カットのひかえ静止画 `fb_<cid>.jpg` は、`footage.USE` に欄が無いと
  **出典が出せないので `RuntimeError` で止まる**（`scene_jiko.keybridge_credit`）。
  これは正しい fail closed（出所を偽らない）だが、`build_layers()` は先頭の
  `pr01` でそれを踏むので、

      python tools/check_layout.py   →  pr01 で例外。**1カットも測らずに落ちる**
      python tools/check_dup.py      →  同上

  ＝ ⑤b で書いた27カットは、机上検査を**一度も通っていなかった**。
  当て木を噛ませて回したところ、pr・c1・`titan_fig.truss` に既存の粗が6件あった。

■ 何を差し替えるか（**ここだけ**）
  `keybridge/fb_*.jpg` の**出典の1行だけ**を、実物とほぼ同じ字数の当て字にする。
  ⚠️ 図・注記・見出しの寸法には触れていない。
  ⚠️ 当て字を短くすると「はみ出し」を見逃す側に倒れるので、実物と同じ字数にしてある。

■ 🔴 これは本番の検査ではない
  `footage.USE` を書いたら、**素の `check_layout.py` と `check_dup.py` を
  もう一度通し、このファイルを消す。**

■ 使い方
    python tools/qa_stub_footage.py                  # check_layout（全カット）
    python tools/qa_stub_footage.py --only=c6
    python tools/qa_stub_footage.py --tool=check_dup
"""
import importlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S                                   # noqa: E402

_KB_FB = re.compile(r"^keybridge/fb_([a-z0-9]+)\.jpg$")
_orig = S.keybridge_credit
# 実物の出典（動画の出典＋「（静止画）」）とほぼ同じ字数の当て字。
_STAND_IN = "米国家運輸安全委員会（NTSB）／パブリックドメイン（静止画）"


def _patched(name):
    if _KB_FB.match(name):
        try:
            return _orig(name)                           # USE が書けていれば本物
        except RuntimeError:
            return _STAND_IN
    return _orig(name)


S.keybridge_credit = _patched

only, tool = None, "check_layout"
for a in sys.argv[1:]:
    if a.startswith("--only="):
        only = a.split("=", 1)[1]
    elif a.startswith("--tool="):
        tool = a.split("=", 1)[1]

print(f"⚠️ 当て木つきの {tool}（fb_* の出典だけ差し替え・{len(_STAND_IN)}字）"
      f"／**本番の検査ではない**")
sys.exit(importlib.import_module(tool).main(only))
