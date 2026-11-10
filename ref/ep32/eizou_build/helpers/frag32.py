# -*- coding: utf-8 -*-
"""32本目 ⑤b-3b：地図の札の数を照らす原文（門番 check_sat の REC_SAT_PAGES＝`ref/ep32/src/news_frag_v2.txt`・git の外）を作る。

  python -P ref/ep32/eizou_build/helpers/frag32.py [--find <句> …]

報告書 `ref/ep32/src/ntsb/AAR1003.pdf`（md5 14290858…＝① と同じ）の頁ごとの字の層を「=== pN ===」で並べる（N＝PDF の頁＝付録B の p189〜202 と同じ数え方）。
札の出典は「抜き書き pN」（check_sat._rec_page が NFKC・空白なしで句を探す）。--find は句の入った頁を出す（空白を無くして探す）。
"""
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parents[4]
PDF = REPO / "ref" / "ep32" / "src" / "ntsb" / "AAR1003.pdf"
OUT = REPO / "ref" / "ep32" / "src" / "news_frag_v2.txt"


def norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


def main():
    import fitz
    doc = fitz.open(PDF)
    pages = [(i + 1, pg.get_text("text")) for i, pg in enumerate(doc)]
    if "--find" in sys.argv:
        for q in sys.argv[sys.argv.index("--find") + 1:]:
            hit = [n for n, t in pages if norm(q).lower() in norm(t).lower()]
            print(f"「{q}」→ 頁 {hit}")
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        for n, t in pages:
            f.write(f"=== p{n} ===\n{t.strip()}\n")
    print(f"→ {OUT}（{len(pages)} 頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
