# -*- coding: utf-8 -*-
"""9本目 ⑥ 試写の「この秒だけ聴く／見る」の**本当の秒**（積み方は `ep7_af_cue.py` と同じ）。

  行の頭 ＝ カットの頭 ＋ `LEAD` ＋ 字幕の `t`（`scene_jiko.CUTS` を順に足す＝`audio_mix.main` と同じ）。
  ⚠️ `audio/el_qa/ep9_youmimi.md` の秒は⑤aの見込み＝試写の一覧にはこちらの秒を載せる。

    python qa_out/ep9_af_cue.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

# 要耳17行（`audio/el_qa/ep9_youmimi.md`）。番号は「そのカットの何行目か」（1始まり）
EAR = [("c115", 1), ("c207", 2), ("c213", 1), ("c307", 1), ("c321", 1), ("c404", 1),
       ("c417", 3), ("c419", 2), ("c511", 1), ("c512", 2), ("c611", 2), ("c712", 1),
       ("c731", 2), ("c909", 3), ("c912", 1), ("c915", 3), ("ep09", 2)]
# 要目視＝⑥で差し替えた ep03 ＋ 直さなかった粗（引き継ぎ 20260917d §3）
EYE = ["ep03", "c510", "c808", "c806", "c903", "ep04", "ep06", "c605", "c624"]


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def main():
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    print(f"カット {len(S.CUTS)} ／ 積んだ尺 {t:.2f}秒 = {mmss(t)}\n")

    print(f"── 要耳{len(EAR)}行（本編の秒）")
    for cid, nth in EAR:
        rows = S.SUBS.get(cid, [])
        if len(rows) < nth:
            raise SystemExit(f"🔴 {cid} に {nth} 行目が無い（{len(rows)}行）。止めた。")
        r = rows[nth - 1]
        print(f"  {mmss(starts[cid] + S.LEAD + r['t']):>8}  {cid}-{nth}  {r['text']}")

    print("\n── 要目視（カットの頭 → 終わり）")
    span = dict(S.CUTS)
    for cid in EYE:
        a = starts[cid]
        print(f"  {mmss(a):>8} 〜 {mmss(a + span[cid]):>8}  {cid}（{span[cid]:.1f}秒）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
