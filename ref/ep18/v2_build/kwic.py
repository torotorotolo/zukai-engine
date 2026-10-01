# -*- coding: utf-8 -*-
"""18本目④'：原文 ref/ep18/src/ep18_pages.txt の指定頁から、語句の前後だけを抜き出す（引き直し用・読むだけ）。
17本目 ref/ep17/v2_build/kwic.py を写し、18本目の通し頁（全部英語）に合わせた。
    python ref/ep18/v2_build/kwic.py 頁 語句 [前字数 後字数]
    python ref/ep18/v2_build/kwic.py -f QUERIES.txt     ← 1行1件「頁<TAB>語句[<TAB>前<TAB>後]」
  頁＝「57」「53-57」「34-73,4181-4220」または名前：
    V1   第1回（査問会の記録 第1巻＝索引・認定・意見・勧告・最初の証言）PDF p.n → p1〜p300（文字の層）
         ＝記録の頁は 認定・意見・勧告が PDF＋1645／証言が PDF−73
    FOR  認定・意見・勧告＝V1 p34〜73 と、その再録 R08 p181〜220（＝p4181〜4220）を両方（V1 p.n ＝ R08 p.n＋147）
    X    第9・10回（証拠）PDF p.n → p1001〜p1600
    IR18 第18回（上級の意見書・措置のまとめ）→ p2001〜p2203（海軍長官の第7 endorsement＝p2001〜2006）
    IR20 第20回 → p3001〜p3102
    R08  第8回（最後の証言＋認定・意見・勧告の再録 p.181〜220）→ p4001〜p4300
    R03  第3回（OCR・崩れあり）→ p5001〜p5322
    R17  第17回（OCR・崩れあり）→ p6001〜p6319
    R13  第13回（OCR・崩れあり）→ p7001〜p7899
    J    JCAE 公聴会記録（1965）の**印刷頁** p.n → p8001〜p8192（前付＝p7901〜7914）
    D    Stierman 1964（修士論文・二次）→ p9001（1頁に全部）
    T    書き起こし＝p9801 国防総省 No.710-64（1964-10-01）／p9802 第17回 p.97 の要旨（どちらも②で原寸で読んだ文）
    AP   AP 2021-08-02（Military Times 掲載）→ p9901
    NAVSEA 2023-04-06 → p9951
    all  全部
  語句は正規表現。NFKC に揃え、語句の中の空白は「空白の1つ以上」に読み替え・大文字小文字を区別しない。
  1件につき最大6か所まで出す。0件なら「0件」と出す（🔴 無いことの証明ではない＝言い換え・表記ゆれ・頁の境目・OCR の崩れで当て直す）。
  🔴 V1 の43頁は「見た目の字が描けていない頁」（文字の層＝OCR の見えない字だけ）＝当たった行に ⚠️見えない頁 と出す。
     認定・意見・勧告なら FOR で R08 の再録にも当てる。証言の頁（p102・128・136・145・197〜199・211）は再録が無い＝文字の層の OCR だけ。
"""
import re, sys, unicodedata
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
T = open(Path(__file__).resolve().parents[1] / "src/ep18_pages.txt", encoding="utf-8").read()
parts = re.split(r"=== p ?(\d+) ===", T)
P = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
rng = lambda a, b: [p for p in P if a <= p <= b]
NAMED = {"V1": rng(1, 300), "X": rng(1001, 1600), "IR18": rng(2001, 2203), "IR20": rng(3001, 3102),
         "R08": rng(4001, 4300), "R03": rng(5001, 5322), "R17": rng(6001, 6319), "R13": rng(7001, 7899),
         "J": rng(8001, 8192), "JF": rng(7901, 7914), "D": [9001], "T": [9801, 9802], "AP": [9901], "NAVSEA": [9951],
         "FOR": rng(34, 73) + rng(4181, 4220)}
BLANK_V1 = {1, 4, 5, 6, 7, 8, 9, 10, 11, 27, 28, 29, 30, 34, 36, 37, 42, 43, 44, 45, 46, 47, 49, 55, 56, 58, 59, 60,
            63, 64, 65, 67, 68, 71, 73, 102, 128, 136, 145, 197, 198, 199, 211}


def label(p):
    if p <= 300:
        return f"V1 p.{p}" + ("（⚠️見えない頁" + (f"＝画像は R08 p.{p + 147}" if 34 <= p <= 73 else "＝再録なし") + "）" if p in BLANK_V1 else "")
    for a, b, nm, off in [(1001, 1600, "X", 1000), (2001, 2203, "IR18", 2000), (3001, 3102, "IR20", 3000),
                          (4001, 4300, "R08", 4000), (5001, 5322, "R03(OCR)", 5000), (6001, 6319, "R17(OCR)", 6000),
                          (7001, 7899, "R13(OCR)", 7000), (7901, 7914, "J前付", 7900), (8001, 8192, "J", 8000)]:
        if a <= p <= b:
            return f"{nm} p.{p - off}"
    return {9001: "D", 9801: "T No.710-64", 9802: "T R17 p.97", 9901: "AP", 9951: "NAVSEA"}.get(p, "?")


def pages(spec):
    if spec == "all":
        return sorted(P)
    out = []
    for r in spec.split(","):
        r = r.strip().lstrip("p")
        if r in NAMED:
            out += sorted(NAMED[r]); continue
        if "-" in r:
            x, y = map(int, r.split("-")); out += [p for p in range(x, y + 1) if p in P]
        else:
            out.append(int(r))
    return out


def run(pg, pat, b=200, a=300):
    pat = unicodedata.normalize("NFKC", pat.strip())
    rx = re.compile(re.sub(r"\s+", r"\\s+", pat), re.I)
    hit = 0
    for p in pages(pg):
        s = unicodedata.normalize("NFKC", P.get(p, ""))
        for m in rx.finditer(s):
            hit += 1
            snip = re.sub(r"\s+", " ", s[max(0, m.start() - b):m.end() + a])
            head = "（頁の頭）" if m.start() - b <= 0 else ""
            tail = "（頁の終わり）" if m.end() + a >= len(s) else ""
            print(f"--- p{p}〔{label(p)}〕 /{pat}/ :: {head}…{snip}…{tail}")
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
