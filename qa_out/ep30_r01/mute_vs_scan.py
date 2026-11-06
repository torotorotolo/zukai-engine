# -*- coding: utf-8 -*-
"""30本目 ⑥：本編の字幕の全段の走査（subscan.tsv）で「出た 0 行」の段を、消す設計（SUB_MUTE の元＝SPEC の mute・m30 の図の mute）と照らす。
scene_jiko.build_layers は層の仕事を全部組むので重い＝SUB_MUTE を作る3つの道のうち SPEC から読める2つ（図の mute・写真の mute）をここで同じ式で読む。
3つ目の決め所（with_last）は台本の決め所が無い回（30本目＝決め所の画面なし）＝ここでは数えない（図の holds を読む道具が要る）。

    python -P qa_out/ep30_r01/mute_vs_scan.py   → 一致なら exit 0
"""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import cuts  # noqa: E402
import el_script as ES  # noqa: E402

subs = {cid: rows for cid, rows in ES.subtitle_rows()} if hasattr(ES, "subtitle_rows") else None
mute = {}
for c, sp in cuts.SPEC.items():
    fig = sp.get("fig")
    if fig and fig[0] in ("m27", "m28", "m29", "m30") and fig[1].get("mute"):
        mute.setdefault(c, set()).update(int(i) for i in fig[1]["mute"])
    if sp.get("mute"):
        mute.setdefault(c, set()).update(int(i) for i in sp["mute"])
design = {(c, i + 1) for c, s in mute.items() for i in s}      # subscan の row は 1 から

rows = list(csv.DictReader((ROOT / "qa_out" / "ep30_r01" / "subscan.tsv").open(encoding="utf-8"), delimiter="\t"))
zero = {(r["cut"], int(r["row"])) for r in rows if r["got"] == "0"}
part = [(r["cut"], r["row"], r["want"], r["got"]) for r in rows if r["got"] != "0" and r["got"] != r["want"]]
print(f"消す設計 {len(design)} 段（{len(mute)} カット）・本編で出なかった段 {len(zero)}・行の数が欠けた段（0 でない）{len(part)}")
only_scan = sorted(zero - design)
only_design = sorted(design - zero)
print("  設計に無いのに出なかった:", only_scan or "なし")
print("  設計で消すのに出た　　　:", only_design or "なし")
print("  欠けた段（2行のはずが1行など）:", part or "なし")
print("  消すカット:", " ".join(f"{c}{sorted(s)}" for c, s in sorted(mute.items())))
sys.exit(0 if not only_scan and not only_design and not part else 1)
