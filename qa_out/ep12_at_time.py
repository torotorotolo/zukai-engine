# -*- coding: utf-8 -*-
"""試写の時刻 ⇄ 台本の行（12本目⑥・2026-09-24）。回に依存しない（scene_jiko から積む）。

    python qa_out/ep12_at_time.py 0:10 18:07              … 時刻 → その -2〜+4秒に掛かる行
    python qa_out/ep12_at_time.py --lines c101-2,c409-2   … 行 → 本編の時刻（頭出し用）

積み方＝カットの頭 ＋ LEAD ＋ 扉（card_of）＋ 字幕の t（audio_mix が声を置く位置と同じ）。
⚠️ `qa_out/ep7_at.py` は扉（12本目からの章の頭 2秒）を足していない＝章の頭のカットで2秒ずれる。
⚠️ 秒は**いまの scene_jiko.CUTS**（＝焼いた版の設計）で積む。版を替えたら焼いた版と check_final で突き合わせてから使う。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

card = getattr(S, "card_of", lambda _c: 0.0)
rows, t = [], 0.0
for cid, sec in S.CUTS:
    for i, r in enumerate(S.SUBS.get(cid, []), 1):
        a = t + S.LEAD + card(cid) + r["t"]
        rows.append((a, a + r["d"], f"{cid}-{i}", r["text"]))
    t += sec


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


args = sys.argv[1:]
print(f"積んだ尺 {t:.2f}秒 = {mmss(t)}")
if args[:1] == ["--lines"]:
    want = set(args[1].split(","))
    for a, b, lid, txt in rows:
        if lid in want:
            print(f"   {mmss(a)}  {lid:8s} {txt}")
else:
    for s in args:
        m, sec = s.split(":")
        T = int(m) * 60 + float(sec)
        print(f"■ {s}")
        for a, b, lid, txt in rows:
            if b >= T - 2 and a <= T + 4:
                print(f"   {mmss(a)}–{mmss(b)}  {lid:8s} {txt}")
