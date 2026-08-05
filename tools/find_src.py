# -*- coding: utf-8 -*-
"""原文照合の検索器。改行と空白を潰した本文から、前後の文脈つきで探す。

報告書・解説書のテキストは PDF から起こしたもので、**1文が途中で改行されている**。
行単位の grep では「後部圧力隔壁の」で切れて当たらない。ここでは空白を全部潰した
1本の文字列を持って、当たった位置の前後を出す。

    python tools/find_src.py 即死
    python tools/find_src.py 18h46 --src cvr        # 資料を絞る
    python tools/find_src.py 0.203 --w 200          # 前後の文字数
    python tools/find_src.py "隔壁" --count         # 件数だけ

資料の名前：report（報告書本文）／kaisetsu（解説書）／cvr（別添1時系列表）
　　　　　　alpa（ALPA文書）／huroku（別添2）
"""
import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SRC = Path(r"C:\Users\konar\Desktop\ja123_src")
NAMES = {"report": "report_text", "kaisetsu": "kaisetsu", "cvr": "cvr_rows",
         "alpa": "alpa_fix", "huroku": "huroku_text"}

_cache = {}


def flat(key):
    if key not in _cache:
        t = (SRC / (NAMES[key] + ".txt")).read_text(encoding="utf-8", errors="replace")
        _cache[key] = re.sub(r"[\s\u3000]+", "", t)
    return _cache[key]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("word")
    ap.add_argument("--src", default="all")
    ap.add_argument("--w", type=int, default=90, help="前後に出す文字数")
    ap.add_argument("--max", type=int, default=12, help="出す件数の上限")
    ap.add_argument("--count", action="store_true")
    a = ap.parse_args()

    keys = list(NAMES) if a.src == "all" else [a.src]
    total = 0
    for k in keys:
        t = flat(k)
        hits = [m.start() for m in re.finditer(re.escape(a.word), t)]
        total += len(hits)
        if not hits:
            continue
        print(f"── {k}（{NAMES[k]}.txt）  {len(hits)}件")
        if a.count:
            continue
        for i, p in enumerate(hits[:a.max], 1):
            s, e = max(0, p - a.w), min(len(t), p + len(a.word) + a.w)
            print(f"  [{i}] …{t[s:p]}【{a.word}】{t[p + len(a.word):e]}…")
        if len(hits) > a.max:
            print(f"  （ほか {len(hits) - a.max}件）")
        print()
    if total == 0:
        print(f"✗ 「{a.word}」はどの資料にも無い")
    else:
        print(f"合計 {total}件")


if __name__ == "__main__":
    main()
