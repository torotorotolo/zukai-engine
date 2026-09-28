# -*- coding: utf-8 -*-
"""報告書96-5 を NFKC＋空白潰しで探す。印刷頁＝PDF頁＋ずれ（目次78項目で確認：ja_01 −17・ja_02 +31・ja_03 +63・ja_04 +77）。
使い方: grepja.py [-c 前後の字数] 正規表現 [正規表現 ...]
出力: 印刷頁・ファイル・PDF頁・前後の文"""
import re, sys
SRC = r"C:\Users\konar\Desktop\zukai-engine\ref\ep17\src\ja_norm.txt"
OFF = {"ja_01": -17, "ja_02": 31, "ja_03": 63, "ja_04": 77}
args = sys.argv[1:]
ctx = 60
if args and args[0] == "-c":
    ctx = int(args[1]); args = args[2:]
rows = []
with open(SRC, encoding="utf-8") as f:
    for line in f:
        fn, pdf, _p, text = line.rstrip("\n").split("\t", 3)
        rows.append((fn, int(pdf[3:]), text))
for pat in args:
    rx = re.compile(pat)
    n = 0
    print(f"### {pat}")
    for fn, pdf, text in rows:
        for m in rx.finditer(text):
            n += 1
            pr = pdf + OFF[fn] if fn in OFF else "?"
            a, b = max(0, m.start() - ctx), min(len(text), m.end() + ctx)
            print(f"  p.{pr} ({fn} pdf{pdf}) …{text[a:m.start()]}【{m.group(0)}】{text[m.end():b]}…")
    print(f"  ({n} hits)")
