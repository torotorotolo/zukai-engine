# -*- coding: utf-8 -*-
"""9本目 ⑤c：`quote` の決め所の折り返しを全件並べる（この回だけの道具・直さない）。

シートの目視で「その資格を出したの／は、」「降りて、すき／間を測った」など同じ型が6件出た
（台帳 B-01・B-09・B-31・B-39 ほか）。目視の1件は式にして全数へ広げる
（記憶 `feedback-scale-one-visual-finding-to-a-full-count`）。
幾何は本番の `titan_fig.quote()` と同じ `balance(phrase, 10)` をそのまま呼ぶ
（記憶 `feedback-gates-must-share-the-production-geometry`）。

判定（機械は候補を出すだけ。決めるのは台帳）
  行頭の字 … 2行目以降の頭がひらがなの助詞・助動詞（は が を に で と の も へ や ず）
  語の途中 … 1行目の尻と2行目の頭が、ひらがなどうし／カタカナどうし／漢字どうしでつながる

    python qa_out/ep9_quote_wrap.py   → 標準出力
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import cuts  # noqa: E402
import titan_fig as TF  # noqa: E402

HEAD_BAD = set("はがをにでとのもへやず")


def kind(ch):
    o = ord(ch)
    if 0x3041 <= o <= 0x309F:
        return "hira"
    if 0x30A0 <= o <= 0x30FF:
        return "kata"
    if 0x4E00 <= o <= 0x9FFF:
        return "kan"
    return "other"


def main():
    rows = []
    for cid in sorted(cuts.SPEC):
        fig = cuts.SPEC[cid].get("fig")
        if not fig or fig[0] != "quote":
            continue
        phrase = fig[1].get("phrase", "")
        # 2026-09-17（⑤c''）：本番の `quote()` は `quote_lines()` で折る（幾何を本番とそろえる）
        lines = TF.quote_lines(phrase, 10) if isinstance(phrase, str) else list(phrase)
        old = TF.balance(phrase, 10) if isinstance(phrase, str) else list(phrase)
        if old != lines:
            print(f"  （旧 balance）{cid:5} {' ／ '.join(old)}")
        marks = []
        for a, b in zip(lines, lines[1:]):
            if b and b[0] in HEAD_BAD:
                marks.append(f"行頭「{b[0]}」")
            if a and b and kind(a[-1]) == kind(b[0]) and kind(b[0]) != "other":
                marks.append(f"語の途中？「{a[-1]}／{b[0]}」")
        rows.append((cid, lines, marks))
    for cid, lines, marks in rows:
        flag = "🔴候補" if marks else "  ・  "
        print(f"{flag} {cid:5} {' ／ '.join(lines)}   {'　'.join(marks)}")
    n = sum(1 for _, _, m in rows if m)
    print(f"\n■ quote {len(rows)}件 ／ 候補 {n}件（機械の候補。決めるのは台帳）")


if __name__ == "__main__":
    main()
