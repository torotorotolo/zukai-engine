# -*- coding: utf-8 -*-
"""15本目④'：原文 ep15_pages.txt の指定頁から、語句の前後だけを抜き出す（引き直し用・読むだけ）。
14本目 ref/ep14/v2_build/kwic.py を英語の原文に合わせた（空白は残す・大文字小文字を区別しない）。
    python ref/ep15/v2_build/kwic.py 頁 語句 [前字数 後字数]
    python ref/ep15/v2_build/kwic.py -f QUERIES.txt     ← 1行1件「頁<TAB>語句[<TAB>前<TAB>後]」
  頁＝「28」「1-52」「12,14,16」「all」（AAB p1〜52・#40 p1001〜・#33 p2001〜・#14 p3001〜・#53 p4001〜
      ・CAROL p5008〜5017・勧告書 p6001〜/p6101〜/p6201〜・#17 p7001〜）。
  語句は正規表現。語句の中の空白は「空白・改行の1つ以上」に読み替える（原文は PDF の改行が残るため）。
  アポストロフィは原文が ’ のことがある＝「.」で当てる（例 pilot.s）。
  1件につき最大6か所まで出す。0件なら「0件」と出す（無いことの証明ではない＝言い換え・頁の境目で当て直す）。
"""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
T = open("C:/Users/konar/Desktop/zukai-engine/ref/ep15/src/ep15_pages.txt", encoding="utf-8").read()
parts = re.split(r"=== p ?(\d+) ===", T)
P = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def pages(spec):
    if spec == "all":
        return sorted(P)
    out = []
    for r in spec.split(","):
        r = r.strip().lstrip("p")
        if "-" in r:
            x, y = map(int, r.split("-")); out += range(x, y + 1)
        else:
            out.append(int(r))
    return out


def run(pg, pat, b=200, a=300):
    rx = re.compile(re.sub(r"\s+", r"\\s+", pat.strip()), re.I)
    hit = 0
    for p in pages(pg):
        s = P.get(p, "")
        for m in rx.finditer(s):
            hit += 1
            snip = re.sub(r"\s+", " ", s[max(0, m.start() - b):m.end() + a])
            print(f"--- p{p} /{pat}/ :: …{snip}…")
            if hit >= 6:
                return
    if not hit:
        print(f"--- p{pg} /{pat}/ :: 0件")


if sys.argv[1] == "-f":
    for line in open(sys.argv[2], encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        bits = line.split("\t")
        run(bits[0], bits[1], *(int(x) for x in bits[2:4]))
else:
    run(sys.argv[1], sys.argv[2], *(int(x) for x in sys.argv[3:5]))
