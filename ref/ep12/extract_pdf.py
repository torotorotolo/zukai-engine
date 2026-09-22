# -*- coding: utf-8 -*-
"""12本目②：一次資料の PDF から本文を出し、**文字層の質**を測る。

なぜ質を測るか
  ④と④' は決め所を**原文で照合**する（→[[feedback-verify-every-onscreen-quote]]）。
  文字層が OCR で崩れていると、
    - 語句検索が当たらず「原文に無い」と誤って結論する（→[[feedback-absence-of-a-word-is-not-absence]]）
    - 崩れた綴りをそのまま引用してしまう
  DNA 6035F の先頭は "CASTLE SERI s" "Executiv Agency" と崩れていた。

測るもの
  - 頁ごとの文字数（0 なら画像だけの頁＝OCR も無い）
  - **英単語らしさ**＝辞書を使わずに測る近似。よくある語が何％当たるか
  - 埋め込み画像の点数と実寸（図を絵として使えるか）
"""
import re
import sys
from collections import Counter
from pathlib import Path

import fitz

sys.stdout.reconfigure(encoding="utf-8")

# 英文なら必ず出る語。OCR が崩れると当たらなくなる
COMMON = ["the", "and", "of", "was", "were", "test", "radiation", "island",
          "personnel", "atoll", "fallout", "shot", "were", "from", "that"]


def main():
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    d = fitz.open(src)
    pages = []
    for i in range(d.page_count):
        pages.append(d[i].get_text())
    text = "\n\f\n".join(pages)
    out.write_text(text, encoding="utf-8")

    n_empty = sum(1 for p in pages if len(p.strip()) < 40)
    lens = sorted(len(p) for p in pages)
    words = re.findall(r"[a-zA-Z]{2,}", text.lower())
    c = Counter(words)
    hit = sum(c[w] for w in COMMON)
    print("== %s ==" % src.name)
    print("頁 %d / 文字 %d / 出力 %s" % (d.page_count, len(text), out))
    print("文字がほぼ無い頁 %d（%.1f%%）＝画像だけ＝原文照合に使えない"
          % (n_empty, n_empty / d.page_count * 100))
    print("1頁あたり文字数 中央値 %d（最小 %d / 最大 %d）"
          % (lens[len(lens) // 2], lens[0], lens[-1]))
    print("語 %d 個。よくある語の当たり %d 回（全語の %.1f%%）"
          % (len(words), hit, hit / max(len(words), 1) * 100))
    print("  内訳: " + " ".join("%s:%d" % (w, c[w]) for w in COMMON[:10]))
    # 1文字だけの断片が多い＝OCR が割れている合図
    frag = sum(1 for w in re.findall(r"\b[a-zA-Z]\b", text))
    print("1文字だけの断片 %d 個（多いほど OCR が割れている）" % frag)

    n_img = 0
    big = 0
    for i in range(d.page_count):
        for im in d[i].get_images(full=True):
            n_img += 1
            if (im[2] or 0) >= 1280:
                big += 1
    print("埋め込み画像 %d 点（幅1280以上 %d 点）" % (n_img, big))


if __name__ == "__main__":
    main()
