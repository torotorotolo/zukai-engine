# -*- coding: utf-8 -*-
"""26本目 ⑥：このチャットで読んだ画像を機械で帳に足す（手で数えると間違える＝CLAUDE.md 鉄則1b・25本目 `ep25_r01_seen.py` の写し）。
    python qa_out/ep26_r01_seen.py <画像のパス> [<画像のパス> …] [--note=何のために見たか]   → qa_out/ep26_r01/seen.tsv に md5 つきで1行ずつ足し、合計を出す
    python qa_out/ep26_r01_seen.py --count                                                     … 合計だけ
"""
import hashlib
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
SEEN = HERE / "qa_out" / "ep26_r01" / "seen.tsv"


def main():
    SEEN.parent.mkdir(parents=True, exist_ok=True)
    note = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--note=")), "")
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    with SEEN.open("a", encoding="utf-8") as f:
        for p in paths:
            q = Path(p)
            if not q.is_absolute():
                q = HERE / q
            md5 = hashlib.md5(q.read_bytes()).hexdigest()
            f.write(f"{datetime.now():%H:%M}\t{q.name}\t{md5}\t{note}\n")
    rows = [r for r in SEEN.read_text(encoding="utf-8").splitlines() if r.strip()]
    print(f"帳 {len(rows)} 行（このチャットで読んだ画像）")


if __name__ == "__main__":
    main()
