# -*- coding: utf-8 -*-
"""16本目④'：原文 ep16_pages.txt の指定頁から、語句の前後だけを抜き出す（引き直し用・読むだけ）。
15本目 ref/ep15/v2_build/kwic.py を16本目の原文（伊語・英語）に合わせた（空白は1つにならす・大文字小文字を区別しない）。
    python ref/ep16/v2_build/kwic.py 頁 語句 [前字数 後字数]
    python ref/ep16/v2_build/kwic.py -f QUERIES.txt     ← 1行1件「頁<TAB>語句[<TAB>前<TAB>後]」
  頁＝「98」「90-99」「72,89,96」「S1」「S8」「S9」「S10」「all」
      S1＝議会の最終報告 Doc.76-bis の PDF の頁 p1〜p248（🔴 PDF146＝印刷147・PDF147＝印刷146）
      S8＝Genevois & Ghirotti 2005 の冊子の頁 p1041〜p1052（冊子41頁＝p1041）
      S9＝ヴァイオント財団の年表の PDF の頁 p2001〜p2019（PDF5＝p2005）
      S10＝Reberschak ほか『Vajont. La prima sentenza』試し読みの PDF の頁 p3001〜p3025（PDF20＝p3020＝印刷21）
  語句は正規表現。語句の中の空白は「空白・改行の1つ以上」に読み替える（原文は PDF の改行が残るため）。
  伊語のアクセント（à è é ì ò ù）は原文どおり。当たらなければ「.」で当てる（例 salv.）。
  1件につき最大6か所まで出す。0件なら「0件」と出す（無いことの証明ではない＝言い換え・頁の境目・OCR の崩れ〈movimneti〉で当て直す）。
"""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
T = open(Path(__file__).resolve().parents[1] / "src/ep16_pages.txt", encoding="utf-8").read()
parts = re.split(r"=== p ?(\d+) ===", T)
P = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
DOC = {"S1": (1, 248), "S8": (1041, 1052), "S9": (2001, 2019), "S10": (3001, 3025)}


def pages(spec):
    spec = spec.strip()
    if spec == "all":
        return sorted(P)
    out = []
    for r in spec.split(","):
        r = r.strip()
        if r.upper() in DOC:
            a, b = DOC[r.upper()]
            out += [p for p in sorted(P) if a <= p <= b]
            continue
        r = r.lstrip("p")
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


if __name__ == "__main__":
    if sys.argv[1] == "-f":
        for line in open(sys.argv[2], encoding="utf-8"):
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            bits = line.split("\t")
            run(bits[0], bits[1], *(int(x) for x in bits[2:4]))
    else:
        run(sys.argv[1], sys.argv[2], *(int(x) for x in sys.argv[3:5]))
