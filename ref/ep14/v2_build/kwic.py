# -*- coding: utf-8 -*-
"""原文 sewol_pages.txt（空白なし）の指定頁から、語句の前後だけを抜き出す（④' の引き直し用・読むだけ）。
    python ref/ep14/v2_build/kwic.py 頁 語句 [前字数 後字数]
    python ref/ep14/v2_build/kwic.py -f QUERIES.txt     ← 1行1件「頁<TAB>語句[<TAB>前<TAB>後]」
  頁＝「14」「1059-1061」「12,14,16」「all」。語句は正規表現（空白は自動で取り除く＝原文に空白が無いため）。
  1件につき最大5か所まで出す。0件なら「0件」と出す（無いことの証明ではない＝言い換えで当て直す）。
"""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
# ⑤a：本線の直書きをやめた（別の作業ツリーから回すため）
T = open(Path(__file__).resolve().parents[1] / "src" / "sewol_pages.txt", encoding="utf-8").read()
parts = re.split(r"=== p ?(\d+) ===", T)
P = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def pages(spec):
    if spec == "all":
        return sorted(P)
    out = []
    for r in spec.split(","):
        if "-" in r:
            x, y = map(int, r.split("-")); out += range(x, y + 1)
        else:
            out.append(int(r))
    return out


def run(pg, pat, b=150, a=250):
    pat = re.sub(r"\s+", "", pat)
    hit = 0
    for p in pages(pg):
        s = P.get(p, "")
        for m in re.finditer(pat, s):
            hit += 1
            print(f"--- p{p} /{pat}/ :: …{s[max(0, m.start() - b):m.end() + a]}…")
            if hit >= 5:
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
