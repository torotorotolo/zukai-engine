# -*- coding: utf-8 -*-
"""13本目④：一次資料10冊と国会の発言を「`=== p<N> ===` で頁を割った1ファイル」にまとめる。

なぜ要るか
  `tools/check_facts.py` は **原文1ファイル・`=== p<N> ===` 区切り（p と数字のあいだに空白なし）** を前提にしている。
  `ref/ep13/src/*.txt` は **`=== p 1 ===`（空白あり）** で、しかも資料ごとに別のファイル。
  そのまま渡すと check_facts は「区切りが無い」で止まる（10本目は多文書で check_facts を使えず手作業に落ちた）。
  12本目の `ref/ep12/make_pages.py` と同じ形で、ここで1本にする。

頁の番号（台本 §2 の「頁」の欄と、見出しの出典の欄はこの通し番号で書く）
  仏 最終報告 原文（S1）          PDF の頁 1〜158 → p1〜p158        （足す数 0）
  英訳 AIB 8/76（S2・OCR）        PDF の頁 1〜55  → p1001〜p1055    （足す数 1000）
  米上院 委員会資料（S6）         PDF の頁 1〜62  → p2001〜p2062    （足す数 2000）
  NTSB AAR-73-02（S5）            PDF の頁 1〜45  → p3001〜p3045    （足す数 3000）
  AD 74-08-04 R4（S7）            → p4001〜 ／ AD 74-12-07（S8）→ p4101〜 ／ AD 75-15-05（S9）→ p4201〜
  官報 1974-04-02（S10）          → p4301〜
  SB 52-37（S13）                 → p5001〜 ／ SB 52-38（S14）→ p5101〜
  国会会議録（S18・S19）          → p6001〜（1発言1頁。日付・URL の順。対応表＝`src/thy_pages_kokkai.tsv`）
  ⚠️ **PDF の頁**であって、報告書に印字された頁ではない（上院資料は 印字＝PDF−12）。

    python ref/ep13/make_pages.py            # → ref/ep13/src/thy_pages.txt と thy_pages_kokkai.tsv
    python ref/ep13/make_pages.py --check    # 頁数だけ数えて出す（書かない）
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent / "src"
DOCS = [  # (ファイル, 足す数, 名前)
    ("faa_FinalAccidentReportinFrench.txt", 0, "仏 最終報告 原文（S1）"),
    ("aib_8-76_TC-JAV.ocr.txt", 1000, "英訳 AIB 8/76（S2）"),
    ("senate_cprt93_dc10.txt", 2000, "米上院 委員会資料（S6）"),
    ("ntsb_AAR73-02_N103AA_erau.txt", 3000, "NTSB AAR-73-02（S5）"),
    ("faa_AD74-08-04.txt", 4000, "AD 74-08-04 R4（S7）"),
    ("faa_AD74-12-07.txt", 4100, "AD 74-12-07（S8）"),
    ("faa_AD75-15-05.txt", 4200, "AD 75-15-05（S9）"),
    ("fr_1974-04-02_11992.txt", 4300, "官報 1974-04-02（S10）"),
    ("faa_SB52-37.txt", 5000, "SB 52-37（S13）"),
    ("faa_SB52-38.txt", 5100, "SB 52-38（S14）"),
]
KOKKAI_OFF = 6000
OUT = HERE / "thy_pages.txt"
OUT_TSV = HERE / "thy_pages_kokkai.tsv"
SPLIT = re.compile(r"=== p ?(\d+) ===")


def pages_of(path):
    parts = SPLIT.split(path.read_text(encoding="utf-8", errors="replace"))
    return [(int(parts[i]), parts[i + 1]) for i in range(1, len(parts), 2)]


def kokkai_speeches():
    """S18（21件）＋S19（cited と relevant_other）を URL で重複除去し、日付・URL の順に並べる。"""
    seen, out = set(), []

    def add(it):
        if isinstance(it, dict) and it.get("speechURL") and it["speechURL"] not in seen:
            seen.add(it["speechURL"])
            out.append(it)

    for it in json.loads((HERE / "kokkai_1974_turkish.json").read_text(encoding="utf-8")):
        add(it)
    ex = json.loads((HERE / "kokkai_extra.json").read_text(encoding="utf-8"))
    for v in ex["cited"].values():
        for it in (v if isinstance(v, list) else []):
            add(it)
    for it in ex["relevant_other"]:
        add(it)
    return sorted(out, key=lambda s: (s["date"], s["speechURL"]))


def main():
    out, n_all = [], 0
    for name, off, label in DOCS:
        ps = pages_of(HERE / name)
        if not ps:            # fail closed：割れていない＝前提が崩れた
            raise SystemExit("E %s を頁に割れない" % name)
        print("%-24s %4d頁 → p%d〜p%d" % (label, len(ps), off + ps[0][0], off + ps[-1][0]))
        for n, t in ps:
            out.append("=== p%d ===\n%s" % (off + n, t.strip("\n")))
        n_all += len(ps)
    sp = kokkai_speeches()
    rows = []
    for i, s in enumerate(sp, 1):
        p = KOKKAI_OFF + i
        out.append("=== p%d ===\n%s" % (p, s["speech"].strip()))
        rows.append("p%d\t%s\t%s\t%s\t%s" % (p, s["date"], s.get("speaker") or "",
                                              s.get("speakerPosition") or "", s["speechURL"]))
    print("%-24s %4d発言 → p%d〜p%d" % ("国会会議録（S18・S19）", len(sp), KOKKAI_OFF + 1, KOKKAI_OFF + len(sp)))
    if "--check" in sys.argv:
        return
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    OUT_TSV.write_text("頁\t日付\t発言者\t肩書\tURL\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print("→ %s（%d頁）／ %s" % (OUT, n_all + len(sp), OUT_TSV.name))


if __name__ == "__main__":
    main()
