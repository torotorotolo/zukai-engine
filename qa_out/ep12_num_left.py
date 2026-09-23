# -*- coding: utf-8 -*-
"""12本目 ⑤a：**送信文字列に生の数字が残っていないか**を全行で数える（API 不使用・2026-09-23）。

  python qa_out/ep12_num_left.py            … 残った数字の行だけ出す（0行なら exit 0）
  python qa_out/ep12_num_left.py --sent     … 読み替わった行の「台本 → 送信」を全部出す（目で読む台帳）

🔴 なぜ要るか: EL_YOMI の境界規則は「漢字で終わる鍵は、直後が漢字なら当てない」。
   「2回」の鍵は「2回**行**われて」「2回**聞**こえた」に**黙って当たらない**（エラーも出ない）。
   check_yomi_numbers.py の型（年・小数・数＋決まった助数詞）は「万トン」「歳」「隻」「冊」「割」「ドル」
   「第7」「リチウム6」などを見ない＝この回の数の半分近くが網の外。ここは**どんな数字でも**残れば落とす。
⚠️ 漢数字（十分・一人・二つ など）は字として残るのが正しい語もあるので、ここでは数えない（--sent で目で見る）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as E  # noqa: E402

DIGIT = re.compile(r"[0-9０-９]+(?:[.．][0-9０-９]+)?")


def main():
    bad, changed = [], []
    for l in E.lines():
        sent = E.el_text(l.text)
        if sent != l.text:
            changed.append((l.lid, l.text, sent))
        left = DIGIT.findall(sent)
        if left:
            bad.append((l.lid, left, sent))
    if "--sent" in sys.argv:
        for lid, t, s in changed:
            print(f"{lid}\t{t}\n\t→ {s}")
    print(f"読み替わった行 {len(changed)}／{len(E.lines())}・EL_YOMI {len(E.EL_YOMI)}件")
    if bad:
        print(f"🔴 生の数字が残った行 {len(bad)}")
        for lid, left, s in bad:
            print(f"  {lid}  {left}  {s}")
        return 1
    print("✓ 送信文字列に生の数字は0件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
