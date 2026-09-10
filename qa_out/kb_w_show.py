# -*- coding: utf-8 -*-
"""⑤c'【直す】3巡目の道具 ── **必要なカットの設計だけ**を原文のまま出す。

なぜ要るか：直す対象は 11本の章ファイルに散っている 42カット。
ファイルを丸ごと読むと 3,800行を読むことになるが、実際に触るのは 1/4 以下。
[[feedback-context-economy]]（読むのは必要な範囲だけ）。

    python -u qa_out/kb_w_show.py c601 c603 ...
    python -u qa_out/kb_w_show.py --file tools/cuts/c6.py   # その章の全カット名

⚠️ 出すのは**ファイルの原文**（`cuts.SPEC` を import した後の値ではない）。
   Edit で書き換える相手は原文なので、原文でないと差し替え文字列が作れない。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
CUTS = HERE / "tools" / "cuts"

# 1カットの始まり：行頭4スペース + "cid": dict(
HEAD = re.compile(r'^    "([a-z]{1,2}\d{2,3})": dict\(')


def blocks(path):
    """{cid: (開始行, 終了行, 本文)}。**直前の連続するコメント行も含める**。"""
    src = path.read_text(encoding="utf-8").splitlines()
    out, i = {}, 0
    while i < len(src):
        m = HEAD.match(src[i])
        if not m:
            i += 1
            continue
        # 直前の「    # …」の連なりを頭に足す
        s = i
        while s > 0 and src[s - 1].lstrip().startswith("#"):
            s -= 1
        # 終わり＝括弧の釣り合いが取れる行
        depth, j = 0, i
        while j < len(src):
            depth += src[j].count("(") - src[j].count(")")
            if depth <= 0 and j > i:
                break
            j += 1
        out[m.group(1)] = (s + 1, j + 1, "\n".join(src[s:j + 1]))
        i = j + 1
    return out


def main(argv):
    if argv and argv[0] == "--file":
        p = HERE / argv[1]
        print(f"■ {p}")
        for cid, (a, b, _) in blocks(p).items():
            print(f"  {cid}  行{a}〜{b}")
        return 0
    want = list(argv)
    seen = {}
    for p in sorted(CUTS.glob("*.py")):
        for cid, v in blocks(p).items():
            seen[cid] = (p, v)
    miss = [c for c in want if c not in seen]
    for cid in want:
        if cid not in seen:
            continue
        p, (a, b, txt) = seen[cid]
        print(f"\n{'=' * 62}\n■ {cid}  {p.relative_to(HERE)}  行{a}〜{b}\n{'=' * 62}")
        print(txt)
    print(f"\n■ 出した {len(want) - len(miss)} カット／SPEC 全 {len(seen)}")
    if miss:
        print(f"🔴 見つからない: {miss}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
