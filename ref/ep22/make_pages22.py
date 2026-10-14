# -*- coding: utf-8 -*-
"""make_pages22.py — 22本目 ⑤b-3b：出典の頁の原文を1ファイル（`=== p<N> ===` で頁を割る）にする＝`cuts.ss.REC_PAGES`。

■ なぜ（21本目 `ref/ep21/make_pages21.py` と同じ）
  ① の写し（git の外 `ref/ep22/src/`）は資料ごとに形が違う（PDF の頁の文字・ウェブの頁）＝門番と出典の行が読む1つの形へ並べ直す。
■ 頁の番号（通し＝`cuts/ss.py` の REC_DOCS の注と同じ）
  USCG＝米沿岸警備隊 海難調査委員会の報告書（2025年8月）の **PDF の頁**（台本の「USCG p.71〈63〉」の 71）
  NTSB＝米運輸安全委員会の報告書 MIR-25-36（2025年10月）＝**1000＋PDF の頁**（台本の「NTSB p.36〈28〉」→ p1036）
  TSB ＝カナダ運輸安全委員会の報告書 M23A0169（2026年6月・ウェブの頁＝頁なし）＝**節**（`illu.sec_num`：1.3.1＝103010000・
        付録B＝902000000・脚注13＝800000013）。節の見出しの行（「1.3.1 Voyage to …」）から次の見出しまで・付録 A〜C・脚注は1つずつ
  ⚠️ TSB の「1.21.1」は原文で2回出る（First mission・Second mission）＝同じ番号に続けて入れる
■ 使い方
    python ref/ep22/make_pages22.py      → ref/ep22/src/ep22_pages.txt（git の外＝手元だけ。Actions では門番を回さない）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = HERE / "src"
OUT = SRC / "ep22_pages.txt"
sys.path.insert(0, str(ROOT / "tools"))
from illu import sec_num  # noqa: E402

PDF_HEAD = re.compile(r"^=== PDF p\.(\d+) ｜ 印字 p\.[^ ]* ===$", re.M)
SEC_HEAD = re.compile(r"^(\d+(?:\.\d+)+) [A-Z]")
APP_HEAD = re.compile(r"^Appendix\s([A-Z])\s[–-]\s")     # ⚠️ 原文の「Appendix」のあとは改行しない空白（U+00A0）


def _pdf(path):
    txt = path.read_text(encoding="utf-8")
    heads = list(PDF_HEAD.finditer(txt))
    return {int(m[1]): txt[m.end(): heads[k + 1].start() if k + 1 < len(heads) else len(txt)].strip("\n")
            for k, m in enumerate(heads)}


def _tsb(path):
    """節・付録・脚注ごとの原文（番号 → 文字）。節の前（表題・要旨）は 1.0 の前＝入れない（要旨は節でない）。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    out, cur, buf = {}, None, []

    def flush():
        if cur is not None:
            out[cur] = (out.get(cur, "") + "\n" + "\n".join(buf)).strip("\n")

    i_fn = next(i for i, ln in enumerate(lines) if ln.strip() == "Footnotes")
    for ln in lines[:i_fn]:
        m, a = SEC_HEAD.match(ln), APP_HEAD.match(ln)
        if m or a or re.match(r"^\d\.0 [A-Z]", ln):
            flush()
            cur = sec_num("付録" + a[1]) if a else sec_num(ln.split(" ")[0])
            buf = []
        buf.append(ln)
    flush()
    # 脚注＝「番号」の行・本文・「Return to footnote」の組
    body = "\n".join(lines[i_fn + 1:])
    for m in re.finditer(r"(?m)^(\d+)\n\n(.*?)\n\nReturn to footnote\n\1\n", body, re.S):
        out[sec_num(f"脚注{int(m[1])}")] = m[2].strip()
    return out


def main():
    pages, n_of = {}, {}

    def put(n, text, what):
        pages[n] = (pages.get(n, "") + "\n" + text).strip("\n")
        n_of[what] = n_of.get(what, 0) + 1

    for p, t in _pdf(SRC / "uscg_mbi_pages.txt").items():
        put(p, t, "USCG")
    for p, t in _pdf(SRC / "ntsb_mir2536_pages.txt").items():
        put(1000 + p, t, "NTSB")
    for p, t in _tsb(SRC / "tsb_m23a0169_html.txt").items():
        put(p, t, "TSB")
    with OUT.open("w", encoding="utf-8") as fo:
        for n in sorted(pages):
            fo.write(f"=== p{n} ===\n{pages[n].rstrip()}\n")
    print(f"{OUT.name}: {len(pages)} 頁＝" + "・".join(f"{k} {v}" for k, v in n_of.items()))


if __name__ == "__main__":
    main()
