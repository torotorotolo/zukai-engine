# -*- coding: utf-8 -*-
"""27本目 ⑥'：このチャットで読んだ画像を機械で帳に足す（手で数えると間違える＝CLAUDE.md 鉄則1b・26本目 `ep26_r01_seen.py` の写し）。
⑥（チャット15）の帳 `qa_out/ep27_r01/seen.tsv`（13枚）とは分ける＝チャットごとに40枚の上限を数えるため。
    python qa_out/ep27_r02_seen.py <画像のパス> [<画像のパス> …] [--note=何のために見たか]   → qa_out/ep27_r02/seen.tsv に md5 つきで1行ずつ足し、合計を出す
    python qa_out/ep27_r02_seen.py --count                                                     … 合計だけ
"""
import hashlib
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
SEEN = HERE / "qa_out" / "ep27_r02" / "seen.tsv"


def main():
    SEEN.parent.mkdir(parents=True, exist_ok=True)
    note = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--note=")), "")
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    with SEEN.open("a", encoding="utf-8") as f:
        for p in paths:
            if p.startswith(("http://", "https://")):  # ブラウザで見た画（手元にファイルが無い）＝URL をそのまま帳へ
                f.write(f"{datetime.now():%H:%M}\t{p}\t-\t{note}\n")
                continue
            q = Path(p)
            if not q.is_absolute():
                q = HERE / q
            md5 = hashlib.md5(q.read_bytes()).hexdigest()
            f.write(f"{datetime.now():%H:%M}\t{q.name}\t{md5}\t{note}\n")
    rows = [r for r in SEEN.read_text(encoding="utf-8").splitlines() if r.strip()] if SEEN.exists() else []
    print(f"帳 {len(rows)} 行（このチャットで読んだ画像）")


if __name__ == "__main__":
    main()
