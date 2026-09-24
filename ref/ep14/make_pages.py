# -*- coding: utf-8 -*-
"""14本目④：一次資料（判決・海審の報告・後年の資料）を「`=== p<N> ===` で頁を割った1ファイル」にまとめる。

なぜ要るか
  `tools/check_facts.py` は **原文1ファイル・`=== p<N> ===` 区切り** を前提にしている。
  `ref/ep14/src/` の本文は資料ごとに別ファイルで、区切りも `=====P1=====`（判決・海審）／`=== p1 ===`（後年の PDF）／
  区切りなし（casenote の転載の判決）の3通り。13本目の `ref/ep13/make_pages.py` と同じ形で、ここで1本にする。
  🔴 韓国語は PDF の文字の層で分かち書きの空白が落ちたり増えたりする＝**空白を全部取り除いて**書き出す
  （台本 §2 の原文の欄も空白なしで書く。ルール 4-2「多文書の回は原文を空白除去して当てる」）。

頁の番号（台本の出典の欄・§2 の「頁」の欄・画の欄の `図 pN` はこの通し番号で書く）
  判決   大法院 2015도6809（S1）                  PDF の頁 1〜81   → p1〜p81        （足す数 0。印字の頁と同じ）
  海審   海洋安全審判院 特別調査報告（S2）        PDF の頁 1〜138  → p1001〜p1138  （足す数 1000。kousei.md の「P47」＝p1047）
  裁決   中央海審 제2026-001호（A）               PDF の頁 1〜174  → p2001〜p2174  （足す数 2000）
  特調委 本巻Ⅱ（D）                              PDF の頁 1〜330  → p3001〜p3330  （足す数 3000）
  特調委 小委員会の報告（E）                      PDF の頁 1〜486  → p4001〜p4486  （足す数 4000）
  頁の無い判決（casenote の転載＝1件を1頁に）     G p5001 ／ H p5002 ／ I p5003 ／ J p5004 ／ K p5005 ／ L p5006 ／ M p5007

    python ref/ep14/make_pages.py            # → ref/ep14/src/sewol_pages.txt
    python ref/ep14/make_pages.py --check    # 頁数だけ数えて出す（書かない）
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent / "src"
DOCS = [  # (ファイル, 足す数, 名前)
    ("sewol_scourt.txt", 0, "判決 大法院 2015도6809（S1）"),
    ("kmst_sewol.txt", 1000, "海審 特別調査報告（S2）"),
    ("later/kmst_2026_001_central_verdict.txt", 2000, "裁決 中央海審 2026（A）"),
    ("later/sdc2022_sewol_main_report.txt", 3000, "特調委 本巻Ⅱ（D）"),
    ("later/sdc2022_sewol_subcommittee_report.txt", 4000, "特調委 小委員会（E）"),
]
SINGLE = [  # (ファイル, 頁, 名前)＝頁の区切りが無い判決
    ("later/court_scourt_2015do11610_123captain.txt", 5001, "G 123艇の艇長 大法院 2015도11610"),
    ("later/court_gwangju_high_2015no177_123captain.txt", 5002, "H 123艇の艇長 光州高裁 2015노177"),
    ("later/court_seoul_high_2021no453_kcg_chiefs.txt", 5003, "I 海洋警察の幹部 ソウル高裁 2021노453"),
    ("later/court_scourt_2023do2364_kcg_chiefs.txt", 5004, "J 海洋警察の幹部 大法院 2023도2364"),
    ("later/court_scourt_2015do7703_company.txt", 5005, "K 清海鎮海運 大法院 2015도7703"),
    ("later/court_gwangju_dist_2014gohap180_crew1.txt", 5006, "L 船員1審 光州地裁 2014고합180"),
    ("later/court_gwangju_high_2014no490_crew2.txt", 5007, "M 船員2審 光州高裁 2014노490"),
]
OUT = HERE / "sewol_pages.txt"
SPLIT = re.compile(r"=====P(\d+)=====|=== ?p ?(\d+) ===")
WS = re.compile(r"\s+")


def pages_of(path):
    parts = SPLIT.split(path.read_text(encoding="utf-8", errors="replace"))
    # split は (本文, P番号, p番号, 本文, …) を返す
    out = []
    for i in range(1, len(parts), 3):
        n = parts[i] or parts[i + 1]
        out.append((int(n), parts[i + 2]))
    return out


def main():
    out, total = [], 0
    for name, off, label in DOCS:
        ps = pages_of(HERE / name)
        if not ps:  # fail closed：割れていない＝前提が崩れた
            raise SystemExit("E %s を頁に割れない" % name)
        nums = [n for n, _ in ps]
        if nums != list(range(1, len(ps) + 1)):
            raise SystemExit("E %s の頁が1から連番でない（%s…）" % (name, nums[:5]))
        print("%-34s %4d頁 → p%d〜p%d" % (label, len(ps), off + 1, off + len(ps)))
        for n, body in ps:
            out.append("=== p%d ===\n%s\n" % (off + n, WS.sub("", body)))
        total += len(ps)
    for name, pg, label in SINGLE:
        body = (HERE / name).read_text(encoding="utf-8", errors="replace")
        if len(body) < 1000:
            raise SystemExit("E %s が短すぎる（%d字）" % (name, len(body)))
        print("%-34s    1頁 → p%d（%d字）" % (label, pg, len(WS.sub("", body))))
        out.append("=== p%d ===\n%s\n" % (pg, WS.sub("", body)))
        total += 1
    print("計 %d頁" % total)
    if "--check" in sys.argv:
        return
    OUT.write_text("".join(out), encoding="utf-8")
    print("→ %s（%d字）" % (OUT, sum(len(x) for x in out)))


if __name__ == "__main__":
    main()
