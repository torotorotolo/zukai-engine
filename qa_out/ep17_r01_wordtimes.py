# -*- coding: utf-8 -*-
"""17本目 ⑥：試写の要耳＝語を含む行の本編の時刻を全部出す（`ep17_r01_times.py` と同じ積み方＝扉こみ）。

    python qa_out/ep17_r01_wordtimes.py 操縦輪 昇降舵 水平安定板 下り道
"""
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import narration as N  # noqa: E402
import scene_jiko as S  # noqa: E402


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def main():
    card = getattr(S, "card_of", lambda _c: 0.0)
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    for w in sys.argv[1:]:
        hits = []
        for cid, rows in N.SCRIPT:
            for i, r in enumerate(rows):
                if unicodedata.normalize("NFKC", w) in unicodedata.normalize("NFKC", r):
                    sub = S.SUBS.get(cid, [])
                    if i < len(sub):
                        hits.append(f"{cid}-{i + 1} {mmss(starts[cid] + S.LEAD + card(cid) + sub[i]['t'])}")
        print(f"{w}（{len(hits)}行）: " + "・".join(hits))


if __name__ == "__main__":
    main()
