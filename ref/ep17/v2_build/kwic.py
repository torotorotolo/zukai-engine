# -*- coding: utf-8 -*-
"""17本目④'：原文 ref/ep17/src/ep17_pages.txt の指定頁から、語句の前後だけを抜き出す（引き直し用・読むだけ）。
15本目 ref/ep15/v2_build/kwic.py を写し、日本語の頁（S1・S2）は空白を全部潰して当てる形にした。
    python ref/ep17/v2_build/kwic.py 頁 語句 [前字数 後字数]
    python ref/ep17/v2_build/kwic.py -f QUERIES.txt     ← 1行1件「頁<TAB>語句[<TAB>前<TAB>後]」
  頁＝「57」「53-57」「2081,2088-2098」「S1」（p1〜105・p184〜186）「S2」（p2001〜）「L1」（p3001〜）「S6」（p4001〜）「S7」（p5001）「all」
    S1＝報告書96-5 の**印刷頁**（p1〜p105＝文字層・p106〜p163＝画像の頁で文字は題だけ・p184〜p186＝別添3 の OCR）
    S2＝名古屋地裁 2003-12-26 判決の PDF 頁＋2000／L1＝FAA HF Team 1996 の PDF 頁＋3000／S6＝NTSB 勧告書の PDF 頁＋4000（OCR）／S7＝連邦官報
    🔴 報告書の本文の時刻は UTC（台本は日本時間＝+9時間。「11時14分05秒」＝20時14分5秒）
  語句は正規表現。NFKC に揃えてから当てる（全角の数字・英字は半角になる）。
    日本語の頁（p<3000）＝原文も語句も空白を全部潰して当てる（原文は空白潰し済み）。
    英語の頁（p>=3000）＝語句の中の空白は「空白の1つ以上」に読み替え・大文字小文字を区別しない。
  1件につき最大6か所まで出す。0件なら「0件」と出す（🔴 無いことの証明ではない＝言い換え・表記ゆれ・頁の境目で当て直す）。
"""
import re, sys, unicodedata
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
T = open(Path(__file__).resolve().parents[1] / "src/ep17_pages.txt", encoding="utf-8").read()
parts = re.split(r"=== p ?(\d+) ===", T)
P = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
NAMED = {"S1": list(range(1, 106)) + [184, 185, 186], "S2": [p for p in P if 2000 < p < 3000],
         "L1": [p for p in P if 3000 < p < 4000], "S6": [p for p in P if 4000 < p < 5000],
         "S7": [p for p in P if p > 5000]}


def pages(spec):
    if spec == "all":
        return sorted(P)
    out = []
    for r in spec.split(","):
        r = r.strip().lstrip("p")
        if r in NAMED:
            out += sorted(NAMED[r]); continue
        if "-" in r:
            x, y = map(int, r.split("-")); out += range(x, y + 1)
        else:
            out.append(int(r))
    return out


def run(pg, pat, b=200, a=300):
    pat = unicodedata.normalize("NFKC", pat.strip())
    rx_ja = re.compile(re.sub(r"\s+", "", pat))
    rx_en = re.compile(re.sub(r"\s+", r"\\s+", pat), re.I)
    hit = 0
    for p in pages(pg):
        s = P.get(p, "")
        if p < 3000:
            s = re.sub(r"\s+", "", s); rx = rx_ja
        else:
            rx = rx_en
        for m in rx.finditer(s):
            hit += 1
            snip = re.sub(r"\s+", " ", s[max(0, m.start() - b):m.end() + a])
            head = "（頁の頭）" if m.start() - b <= 0 else ""
            tail = "（頁の終わり）" if m.end() + a >= len(s) else ""
            print(f"--- p{p} /{pat}/ :: {head}…{snip}…{tail}")
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
