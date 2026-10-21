# -*- coding: utf-8 -*-
"""17本目 ⑥：試写の手引きの時刻を、本編の組み立て（扉こみ）から出す。

なぜ：⑤a-2 の要耳一覧の秒（`qa_out/ep17_a5/17本目_行ごとの時刻.tsv`）は扉（章の頭の札）を入れる前の秒＝本編とずれる。
     本編の行の頭＝カットの頭＋LEAD＋扉（S.card_of）＋字幕の t（`qa_out/kb_af_loud.timeline` と同じ積み方＝audio_mix と同じ）。

    python qa_out/ep17_r01_times.py c103-2,c105-1 c807,c115     … 行（カット-行番号）の頭と、カットの頭〜終わり
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def main():
    card = getattr(S, "card_of", lambda _c: 0.0)
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = (t, sec)
        t += sec
    print(f"積んだ尺 {t:.2f}秒 = {mmss(t)}")
    for arg in sys.argv[1:]:
        for k in [x for x in arg.split(",") if x]:
            if "-" in k:
                cid, n = k.rsplit("-", 1)
                rows = S.SUBS.get(cid, [])
                i = int(n) - 1
                if cid not in starts or not (0 <= i < len(rows)):
                    print(f"  🔴 {k} が無い")
                    continue
                a = starts[cid][0] + S.LEAD + card(cid) + rows[i]["t"]
                print(f"  {k:10s} {mmss(a)}")
            else:
                if k not in starts:
                    print(f"  🔴 {k} が無い")
                    continue
                s, sec = starts[k]
                print(f"  {k:10s} {mmss(s + card(k))}〜{mmss(s + sec)}")


if __name__ == "__main__":
    main()
