# -*- coding: utf-8 -*-
"""⑥ 試写の「この秒だけ聴く／見る」の**本当の秒**を、焼いた版の積み方で取り直す。

🔴 なぜ取り直すか
  `audio/el_qa/ep7_youmimi.md` の秒は **⑤a が narration.json だけから積んだ見込み**で、
  ⑤b の章マーカー・間・静止の伸ばしが入ると動く。4本目では **2分12秒**ずれていた
  （`qa_out/surfside_open.md`）。**試写の一覧に見込みの秒を載せない。**

  積み方は `audio_mix.main` / `build_jiko.build_full` と同じ＝`scene_jiko.CUTS` を順に足し、
  行の頭 ＝ カットの頭 ＋ `LEAD` ＋ 字幕の `t`。

    python qa_out/ep7_af_cue.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

# 要耳10行（`audio/el_qa/ep7_youmimi.md`）。番号は「そのカットの何行目か」（1始まり）
EAR = [("c113", 1), ("c120", 2), ("c209", 2), ("c210", 1), ("c214", 1),
       ("c313", 1), ("c417", 1), ("c623", 3), ("c811", 2), ("c904", 1)]
# 要目視（`qa_out/ep7_qa_fix.md` §H-4 と 引き継ぎ §6）
EYE = ["c412", "c201", "c320", "c809", "c804", "c813", "c716", "c711"]


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def main():
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    print(f"カット {len(S.CUTS)} ／ 積んだ尺 {t:.2f}秒 = {mmss(t)}\n")

    print("── 要耳10行（本編の秒・取り直し）")
    for cid, nth in EAR:
        rows = S.SUBS.get(cid, [])
        if len(rows) < nth:
            raise SystemExit(f"🔴 {cid} に {nth} 行目が無い（{len(rows)}行）。止めた。")
        r = rows[nth - 1]
        a = starts[cid] + S.LEAD + r["t"]
        print(f"  {mmss(a):>8}  {cid}-{nth}  {r['text']}")

    print("\n── 要目視（カットの頭 → 終わり）")
    span = dict(S.CUTS)
    for cid in EYE:
        a = starts[cid]
        print(f"  {mmss(a):>8} 〜 {mmss(a + span[cid]):>8}  {cid}（{span[cid]:.1f}秒）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
