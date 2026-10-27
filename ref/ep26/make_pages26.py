# -*- coding: utf-8 -*-
"""make_pages26.py — 26本目 ⑤b-4：出典の頁の原文を1ファイル（`=== p<N> ===` で頁を割る）にする＝`cuts.ss.REC_PAGES`。

■ なぜ（25本目 `ref/ep25/make_pages25.py` と同じ）
  ② の写し（git の外 `ref/ep26/src/`＝資料ごとの頁のファイル）を、案C の部品の `rec=` が「資料 p頁」で原文に在るかを
  門番 check_illu ① が照らす1つの形へ並べ直す。
■ 頁の番号（通し＝`cuts/ss.py` の REC_DOCS の注と同じ）
  G1＝英国の審問の報告の米国上院の刷り直し S. Doc. 933（88頁）＝**印刷の頁**（PDF＝印刷＝`src/sd933_pages/p057.txt` の頭が「57」）＝
      台本の「G1 p.57」がそのまま p57
  G2＝MAIB 1992（30頁）＝**2000＋PDF の頁**（印刷＝PDF−4＝本文 p.1 が PDF 5）＝`src/txt/maib_bypage.txt` の「=== PDF p.NN」
  G7＝米国上院の公聴会 S. Doc. 726（1,170頁）＝**20000＋PDF の頁**（印刷の頁とは数頁ずれる＝画面は PDF の頁）＝`src/sd726_pages/p0719.txt`
  T1＝英国の審問の証言（書き起こし・有志のサイト）＝**保存していない**＝この原文に入れない（REC_DOCS で `text=False`・番号は問の番号 Q）
■ 使い方
    python ref/ep26/make_pages26.py      → ref/ep26/src/ep26_pages.txt（git の外＝手元だけ。Actions では門番を回さない）
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = SRC / "ep26_pages.txt"


def _norm(s):
    return "".join(unicodedata.normalize("NFKC", s or "").split())


def _g1():
    out = {}
    for f in sorted((SRC / "sd933_pages").glob("p[0-9][0-9][0-9].txt")):
        n = int(f.stem[1:])
        out[n] = _norm(f.read_text(encoding="utf-8"))
    if len(out) != 88:
        raise SystemExit(f"🔴 G1 の頁が 88 でない（{len(out)}）")
    # 印刷の頁＝ファイルの番号（頭の行に頁の数が出る頁で照らす＝p5 は本文の頭の頁で数が刷られていない）
    for n in (38, 54, 55, 56, 57, 58, 59, 60):
        if str(n) not in out[n][:60]:
            raise SystemExit(f"🔴 G1 p{n} の頭に印刷の頁の数が無い（PDF＝印刷 の前提が崩れた）")
    return out


def _g2():
    t = (SRC / "txt" / "maib_bypage.txt").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^=== PDF p\.(\d+)\n(.*?)(?=^=== PDF p\.|\Z)", t, re.M | re.S):
        out[2000 + int(m.group(1))] = _norm(m.group(2))
    if len(out) != 30:
        raise SystemExit(f"🔴 G2 の頁が 30 でない（{len(out)}）")
    return out


def _g7():
    out = {}
    for f in sorted((SRC / "sd726_pages").glob("p[0-9][0-9][0-9][0-9].txt")):
        out[20000 + int(f.stem[1:])] = _norm(f.read_text(encoding="utf-8"))
    if len(out) != 1170:
        raise SystemExit(f"🔴 G7 の頁が 1,170 でない（{len(out)}）")
    return out


def main():
    pages, n_of = {}, {}
    for name, fn in (("G1", _g1), ("G2", _g2), ("G7", _g7)):
        for n, text in fn().items():
            if n in pages:
                raise SystemExit(f"🔴 頁の番号がぶつかった：{name} → p{n}")
            pages[n] = text
            n_of[name] = n_of.get(name, 0) + 1
    with OUT.open("w", encoding="utf-8", newline="\n") as fo:
        for n in sorted(pages):
            fo.write(f"=== p{n} ===\n{pages[n]}\n")
    print("✓", OUT.name, "＝", "・".join(f"{k} {v}頁" for k, v in n_of.items()), f"（計 {len(pages)}頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
