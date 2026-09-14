# -*- coding: utf-8 -*-
"""試写の「この秒」から、**カットと字幕の行**を引く。

    python qa_out/ep7_at.py 0:43 1:38 2:09 25:37 30:05 31:31

積み方は `qa_out/ep7_af_cue.py` と同じ＝カットの頭 ＋ `LEAD` ＋ 字幕の `t`。
⚠️ 秒は**焼いた版**（`scene_jiko.CUTS`）で積む。⑤a の見込みの秒を使わない。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def parse(s):
    m, sec = s.split(":")
    return int(m) * 60 + float(sec)


def main():
    rows, t = [], 0.0
    for cid, dur in S.CUTS:
        for i, r in enumerate(S.SUBS.get(cid, []), 1):
            a = t + S.LEAD + r["t"]
            rows.append((a, a + r["d"], cid, i, r["text"]))
        t += dur

    for arg in sys.argv[1:]:
        want = parse(arg)
        # その秒を含む行。無ければいちばん近い行
        hit = [r for r in rows if r[0] - 1.0 <= want <= r[1] + 1.0]
        if not hit:
            hit = [min(rows, key=lambda r: abs(r[0] - want))]
        print(f"\n■ {arg}")
        for a, b, cid, i, txt in hit:
            print(f"  {mmss(a)}〜{mmss(b)}  {cid}-{i}  {txt}")
        # 前後も1行ずつ出す（読みの直しは前後の語で決まることがある）
        k = rows.index(hit[0])
        for j in (k - 1, k + 1):
            if 0 <= j < len(rows):
                a, b, cid, i, txt = rows[j]
                print(f"    （参考 {mmss(a)}  {cid}-{i}  {txt}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
