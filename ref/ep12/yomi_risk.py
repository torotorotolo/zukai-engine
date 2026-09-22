# -*- coding: utf-8 -*-
"""12本目④：台本から「誤読の危ない数」を、行の中の位置つきで拾う（⑤a への申し送り用）。

なぜ位置を出すか
  11本目の試写では40件中13件が数字の誤読で、**同じ語でも行頭・行末だけ崩れた**
  （記憶 feedback-tts-misreads-are-positional）。⑤a は `check_yomi_numbers.py` で
  送信文字列を見るが、**④の時点で「どの行のどこに危ない数があるか」**を渡しておく。

型（`tools/check_yomi_numbers.py` と同じ区分）
  A 西暦4桁（1954年）  B 小数（2.5倍）  C 数＋助数詞（23人・157キロ・6時45分）
  D 読みが2通りある日付・日数（1日・4日・20日・7、8日 など）

    python ref/ep12/yomi_risk.py <台本.md>            # 型ごとの件数と、行頭・行末に来たもの
    python ref/ep12/yomi_risk.py <台本.md> --all      # 全件
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import check_script as cs  # noqa: E402

A = re.compile(r"(1[89]\d\d|20\d\d)年")
B = re.compile(r"\d+\.\d+")
D = re.compile(r"(?<![\d.])(1|2|3|4|5|6|7|8|9|10|14|19|20|24)日(?!本)|[0-9]、[0-9](日|分|時間)")
C = re.compile(r"\d[\d,.]*\s*(万|億)?\s*(人|隻|トン|キロ|メートル|センチ|倍|分|時|秒|日|回|年|か月|階|%|つ|号|度|海里)")


def kinds(t):
    out = []
    for name, rx in (("A", A), ("B", B), ("D", D), ("C", C)):
        for m in rx.finditer(t):
            out.append((name, m.start(), m.end(), m.group(0)))
    return out


def main():
    md = sys.argv[1]
    cuts = cs.parse(open(md, encoding="utf-8").read())
    rows, cnt = [], Counter()
    for cid, _, ls in cuts:
        for i, l in enumerate(ls, 1):
            t = cs.clean(l)
            for k, a, b, s in kinds(t):
                pos = "行頭" if a <= 2 else ("行末" if b >= len(t.rstrip("。、")) - 1 else "")
                rows.append((f"{cid}-{i}", k, s, pos, t))
                cnt[k] += 1
    print("型ごと: " + " / ".join(f"{k} {cnt[k]}" for k in "ABCD"), f"（計 {sum(cnt.values())}）")
    edge = [r for r in rows if r[3]]
    print(f"🔴 行頭・行末に来た数: {len(edge)}件")
    for r in (rows if "--all" in sys.argv else edge):
        print("  %-7s %s %-12s %-3s %s" % (r[0], r[1], r[2], r[3], r[4][:44]))


if __name__ == "__main__":
    main()
