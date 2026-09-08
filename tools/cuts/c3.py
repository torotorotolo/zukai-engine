# -*- coding: utf-8 -*-
"""第3章。6本目（キー橋）の割り当ては未着手。

🔴 **2026-09-08（6本目②）に空にした。**
   カットIDは題材をまたいで必ずぶつかる（`pr01` `c101` … は5本すべてで重複する）。
   5本目（SL-1）の中身は git の **`58cd823`** に在る:
       git show 58cd823:tools/cuts/c3.py

   ④の台本が通ってから、台本 §4 の画の欄と**1対1**で書く。
   検算＝`python -c "import cuts; print(len(cuts.SPEC))"` が台本のカット数と合うこと。
   書き方＝`tools/cuts/README.md`。
"""

SPEC = {}
