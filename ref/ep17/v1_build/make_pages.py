# -*- coding: utf-8 -*-
"""17本目の原文を1ファイルにまとめる（check_facts.py に渡す `=== p<N> ===` の形）。

    python ref/ep17/v1_build/make_pages.py      → ref/ep17/src/ep17_pages.txt（git の管理外）

通し頁（台本の §2 の頁の欄と、画の欄の `図 pN` はこの番号）:
  p1〜p105     S1 報告書96-5 の本文の**印刷頁**（ja_norm.txt＝NFKC＋空白を全部潰した文字層。probe/grepja.py と同じ対応）
  p184〜p186   S1 別添3（画像だけの頁）＝ v1_build/ocr_betten3.txt があれば入れる（Windows OCR の読み＝決め所は頁の画像で当てた）
  p2001〜      S2 名古屋地裁 2003-12-26 判決の PDF の頁＋2000（NFKC＋空白を全部潰す）
  p3001〜      L1 FAA Human Factors Team 1996 の PDF の頁＋3000（NFKC＋空白を1つに）
  p4001〜      S6 NTSB 勧告書 A-94-164〜166 の PDF の頁＋4000（文字層は OCR＝崩れあり）
  p5001        S7 連邦官報 1994-10-18 AD 94-21-07 の全文（1頁として）
⚠️ 日本語は空白を全部潰す（行をまたぐ語をつなぐため）＝台本 §2 の原文も空白なし・半角英数字で書く。
"""
import os
import re
import sys
import unicodedata

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'src'))
OUT = os.path.join(SRC, 'ep17_pages.txt')
OFF = {"ja_01": -17, "ja_02": 31, "ja_03": 63, "ja_04": 77}


def ja(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', s))


def en(s):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', s)).strip()


def main():
    pages = {}
    # S1 本文（印刷頁）
    with open(os.path.join(SRC, 'ja_norm.txt'), encoding='utf-8') as f:
        for line in f:
            fn, pdf, _p, text = line.rstrip('\n').split('\t', 3)
            if fn in OFF:
                pages[int(pdf[3:]) + OFF[fn]] = text
    n1 = len(pages)
    # S1 別添3 の OCR（あれば）
    ocr = os.path.join(HERE, 'ocr_betten3.txt')
    if os.path.exists(ocr):
        t = open(ocr, encoding='utf-8').read()
        parts = re.split(r'=== p(\d+) ===', t)
        for i in range(1, len(parts), 2):
            pages[int(parts[i])] = ja(parts[i + 1])
    # S2 判決
    t = open(os.path.join(SRC, 'court_2003-12-26_H7wa4179.txt'), encoding='utf-8').read()
    parts = re.split(r'=== court_2003-12-26_H7wa4179\.pdf pdf(\d+) ===', t)
    for i in range(1, len(parts), 2):
        pages[2000 + int(parts[i])] = ja(parts[i + 1])
    # L1・S6（PDF の文字層）
    for base, fn in ((3000, 'faa_hf_team_1996.pdf'), (4000, 'ntsb_A94-164-166.pdf')):
        d = fitz.open(os.path.join(SRC, fn))
        for i, pg in enumerate(d, 1):
            pages[base + i] = en(pg.get_text())
    # S7
    pages[5001] = en(open(os.path.join(SRC, 'fr_1994-10-18_94-25581_AD94-21-07.txt'), encoding='utf-8', errors='replace').read())
    with open(OUT, 'w', encoding='utf-8') as f:
        for p in sorted(pages):
            f.write('=== p%d ===\n%s\n' % (p, pages[p]))
    print('S1本文 %d頁 / 全 %d頁 → %s' % (n1, len(pages), OUT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
