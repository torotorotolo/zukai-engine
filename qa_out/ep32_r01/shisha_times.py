# -*- coding: utf-8 -*-
"""32本目 ⑥：⑤a-2 の「行ごとの時刻」（`qa_out/ep32_a5/32本目_行ごとの時刻.tsv`＝原音 c416 の 1.85秒を足す前）を、
いまの設計（scene_jiko.CUTS＝本編と同じ表）の秒に引き直す。試写の手引きの「聞いてほしい所」の秒はこちらを使う。
式＝新しい秒＝そのカットの頭（CUTS の積み上げ）＋LEAD＋扉の秒＋（その行の秒 − そのカットの最初の行の秒）
    python -P qa_out/ep32_r01/shisha_times.py   → qa_out/ep32_r01/shisha_times.tsv・ずれの要約
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

rows = list(csv.DictReader((ROOT / "qa_out" / "ep32_a5" / "32本目_行ごとの時刻.tsv").open(encoding="utf-8"), delimiter="\t"))
start, t = {}, 0.0
for cid, sec in S.CUTS:
    start[cid] = t
    t += sec
first = {}
for r in rows:
    cid = r["行ID"].rsplit("-", 1)[0]
    first.setdefault(cid, float(r["秒"]))
out = ROOT / "qa_out" / "ep32_r01" / "shisha_times.tsv"
diffs = []
with out.open("w", encoding="utf-8", newline="\n") as f:
    f.write("新しい時刻\t新しい秒\t前の秒\t差\t行ID\t文\n")
    for r in rows:
        cid = r["行ID"].rsplit("-", 1)[0]
        if cid not in start:
            print("🔴 CUTS に無いカット", cid)
            continue
        new = start[cid] + S.LEAD + S.card_of(cid) + (float(r["秒"]) - first[cid])
        d = new - float(r["秒"])
        diffs.append((r["行ID"], d))
        f.write(f"{int(new // 60)}:{new % 60:04.1f}\t{new:.3f}\t{r['秒']}\t{d:+.3f}\t{r['行ID']}\t{r['文']}\n")
# ずれの段（c416 より前は 0・後ろは +1.85 の見込み）
prev = None
for lid, d in diffs:
    k = round(d, 2)
    if k != prev:
        print(f"  {lid} から 差 {k:+.2f}秒")
        prev = k
print(f"→ {out}（{len(diffs)} 行）・設計の尺 {t:.2f}秒")
