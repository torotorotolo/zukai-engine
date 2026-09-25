# -*- coding: utf-8 -*-
"""15本目④：原文を `=== p<N> ===` 区切りの1ファイルにまとめる（check_facts.py にそのまま渡す）。
    python ref/ep15/v1_build/make_pages.py      → ref/ep15/src/ep15_pages.txt（src/ は無視設定＝コミットしない）

通し番号（台本の出典欄の略号と同じ）：
  AAB（NTSB/AAB-12/01）   p1〜p52      （PDF の頁のまま。印字＝PDF −9）
  #40 材料試験             p1001〜
  #33 生存要因・運航       p2001〜
  #14 データ記録           p3001〜
  #53 性能解析             p4001〜
  CAROL A-12-0NN           p50NN        （JSON の文字の値を全部つないで1件1頁）
  勧告書 A-12-008          p6001〜／A-12-009-012 p6101〜／A-12-013-017 p6201〜
  #17 耐空性               p7001〜
⚠️ 原文の文字は変えない（空白の揺れは check_facts の norm が吸う）。1つでも読めなければ止める（fail closed）。
"""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SRC = Path(__file__).resolve().parents[1] / "src"
PAGE = re.compile(r"=== p(\d+) ===")
PAGED = [("AAB1201.txt", 0),
         ("ntsb_docket_40_materials_lab_12-029.txt", 1000),
         ("ntsb_docket_33_survival_factors_operations_factual.txt", 2000),
         ("ntsb_docket_14_data_recorders_factual.txt", 3000),
         ("ntsb_docket_53_aircraft_performance_study.txt", 4000),
         ("ntsb_recletter_A-12-008.txt", 6000),
         ("ntsb_recletter_A-12-009-012.txt", 6100),
         ("ntsb_recletter_A-12-013-017.txt", 6200),
         ("ntsb_docket_17_airworthiness_factual.txt", 7000)]


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


out, count = [], {}
for name, off in PAGED:
    t = (SRC / name).read_text(encoding="utf-8")
    parts = PAGE.split(t)
    if len(parts) < 3:
        sys.exit(f"E 頁の区切りが無い: {name}")
    n = 0
    for i in range(1, len(parts), 2):
        out.append(f"=== p{int(parts[i]) + off} ===\n{parts[i + 1].strip()}\n")
        n += 1
    count[name] = (off + 1, off + n)
for k in range(8, 18):
    name = f"ntsb_carol_sr_A-12-0{k:02d}.json"
    d = json.loads((SRC / name).read_text(encoding="utf-8"))
    txt = "\n".join(s.replace("\r\n", "\n") for s in strings(d) if s and s.strip())
    out.append(f"=== p{5000 + k} ===\n{txt}\n")
    count[name] = (5000 + k, 5000 + k)
dst = SRC / "ep15_pages.txt"
dst.write_text("\n".join(out), encoding="utf-8")
for name, (a, b) in count.items():
    print(f"  p{a}〜p{b}  {name}")
print(f"→ {dst}  {len(out)}頁")
