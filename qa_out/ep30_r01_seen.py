# -*- coding: utf-8 -*-
"""28本目 ⑥：見た画像の帳（機械で数える）。Read と同じメッセージで SendUserFile に出した物を1行ずつ足す。

    python -P qa_out/ep30_r01_seen.py <画像> [<画像>…] [--note=何を見たか]   → qa_out/ep30_r01/seen.tsv・累計を出す
"""
import hashlib
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
TSV = HERE / "qa_out" / "ep30_r01" / "seen.tsv"


def main():
    note = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--note=")), "")
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    TSV.parent.mkdir(parents=True, exist_ok=True)
    with TSV.open("a", encoding="utf-8", newline="\n") as f:
        for p in paths:
            b = Path(p).read_bytes()
            f.write(f"{time.strftime('%H:%M:%S')}\t{Path(p).as_posix()}\t{hashlib.md5(b).hexdigest()[:8]}\t{note}\n")
    n = sum(1 for _ in TSV.open(encoding="utf-8"))
    print(f"見た画像 累計 {n} 枚／40（{TSV.name}）")


if __name__ == "__main__":
    main()
