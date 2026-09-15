# -*- coding: utf-8 -*-
"""ep8_fixlist.py — 文言の門番3本（echo / dup / wording）の所見を**カットごと**にまとめる。

■ なぜ要るか
    3本とも「同じ画面の文字」を別の向きから見ている（複写・二重表示・言葉づかい）。
    別々に読むと同じカットを3回開くことになるので、1カット1ブロックに畳む。
    ⚠️ **数だけを見て直さない。**各行の本文（何の文字が、何と、どれだけ一致したか）まで残す。

■ 使い方
    python qa_out/ep8_fixlist.py             # 全部
    python qa_out/ep8_fixlist.py c1 c2       # 章の頭文字で絞る（cid の前方一致）
"""
from __future__ import annotations

import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")

CID = re.compile(r"\b((?:pr|ep|c)\d{2,3}[a-z]?)\b")


def run(cmd):
    r = subprocess.run([sys.executable, *cmd], cwd=HERE, capture_output=True)
    return (r.stdout + b"\n" + r.stderr).decode("utf-8", "replace").split("\n")


def main():
    pats = tuple(sys.argv[1:])
    per = defaultdict(list)
    for tag, cmd in (("echo", ["tools/check_echo.py"]),
                     ("dup", ["tools/check_dup.py"]),
                     ("word", ["tools/check_wording.py"])):
        cur = None
        for ln in run(cmd):
            if not ln.strip():
                continue
            m = CID.search(ln)
            if ln.lstrip().startswith(("🔴", "⚠️", "・")) and m:
                cur = m.group(1)
                per[cur].append(f"  [{tag}] {ln.strip()}")
            elif cur and ln.startswith(("      ", "\t")):
                per[cur].append(f"         {ln.strip()}")
            else:
                cur = None
    n = 0
    for cid in sorted(per):
        if pats and not cid.startswith(pats):
            continue
        n += 1
        print(f"■ {cid}")
        for ln in per[cid]:
            print(ln)
    print(f"\n# 所見のあるカット {n} 件")


if __name__ == "__main__":
    main()
