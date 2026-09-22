# -*- coding: utf-8 -*-
"""12本目④：一次資料3冊を「`=== p<N> ===` で頁を割った1ファイル」にまとめる。

なぜ要るか
  `tools/check_facts.py` は **原文1ファイル・`=== p<N> ===` 区切り** を前提にしている。
  `ref/ep12/src/*.txt`（`extract_pdf.py` の出力）は **改ページ文字 `\\f` で割られていて、
  区切りの行が無い**。そのまま渡すと check_facts は「区切りが無い」で止まる。
  10本目は原文が10文書に割れていて check_facts を使えず、手作業に落ちた
  （Vault `事故検証-三豊百貨店-台本第1版` §7-1）。同じ穴を踏まないため、ここで1本にする。

頁の番号（台本 §2 の「頁」の欄はこの通し番号で書く）
  DNA 6035F『CASTLE SERIES, 1954』   PDF の頁   1〜 538 → p1〜p538       （足す数 0）
  WT-923『Operation Castle Project 4.1』 PDF の頁 1〜  96 → p1001〜p1096  （足す数 1000）
  DASA 1251 Vol.II                   PDF の頁   1〜 351 → p2001〜p2351   （足す数 2000）
  ⚠️ **PDF の頁**であって、報告書に印字された頁ではない（表紙・前付のぶんずれる）。
  ＋ `web_quotes.txt`（p3001〜）＝3冊の外の決め所の原文（DTRA 2013・2024年の論文の要旨）。
    そのファイル自身が `=== p<N> ===` で割ってあり、各頁の頭に出どころと取り方を書いてある。
    ⚠️ 頁の画像では確かめていない（web の文字を写したもの）＝④'は元の URL で確かめる。

    python ref/ep12/make_pages.py            # → ref/ep12/src/castle_pages.txt
    python ref/ep12/make_pages.py --check    # 頁数だけ数えて出す（書かない）
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent / "src"
DOCS = [  # (ファイル, 足す数, 名前)
    ("dna6035f.txt", 0, "DNA 6035F"),
    ("project41_wt923.txt", 1000, "WT-923 Project 4.1"),
    ("dasa1251_v2.txt", 2000, "DASA 1251 Vol.II"),
]
OUT = HERE / "castle_pages.txt"


def pages_of(path):
    """extract_pdf.py は頁を "\\n\\f\\n" でつないでいる。"""
    return path.read_text(encoding="utf-8").split("\f")


def main():
    out = []
    for name, off, label in DOCS:
        ps = pages_of(HERE / name)
        if len(ps) < 10:          # fail closed：割れていない＝前提が崩れた
            raise SystemExit("E %s を頁に割れない（%d頁）" % (name, len(ps)))
        print("%-22s %4d頁 → p%d〜p%d" % (label, len(ps), off + 1, off + len(ps)))
        for i, t in enumerate(ps, 1):
            out.append("=== p%d ===\n%s" % (off + i, t.strip("\n")))
    web = HERE / "web_quotes.txt"
    if web.exists():
        wt = web.read_text(encoding="utf-8").strip("\n")
        n_web = wt.count("=== p")
        print("%-22s %4d頁 → p3001〜（web の原文の写し）" % ("web_quotes.txt", n_web))
        out.append(wt)
    if "--check" in sys.argv:
        return
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("→ %s（%d頁）" % (OUT, len(out)))


if __name__ == "__main__":
    main()
