# -*- coding: utf-8 -*-
"""31本目 ⑥：30本目の受け取りの道具を写す（ep30 → ep31 の字の置き換えだけ・中身は変えない）。
    python -P qa_out/ep31_r01/mktools.py
🔴 写したあとに手で直す＝`ep31_r02_verify_upload.py` の DURATIONS・DUR_NOTE（本編の尺）・`receive.sh` の `--qa=`（31本目の検品の絵の置き場）
   ほか 30本目の値（カットの番号・数）が残っていないかを grep で見る
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa_out"
NAMES = ["ep30_r01_cutframes", "ep30_r01_ground", "ep30_r01_seen", "ep30_r01_sheet", "ep30_r01_subscan",
         "ep30_r01_voiceq", "ep30_r01_vs_qa", "ep30_r01_where", "ep30_r02_vs_r01", "ep30_r02_verify_upload"]
PAIRS = [(QA / f"{n}.py", QA / f"{n.replace('ep30', 'ep31')}.py") for n in NAMES]
PAIRS += [(QA / "ep30_r01" / n, QA / "ep31_r01" / n) for n in ("receive.sh", "motion.py", "mute_vs_scan.py")]
for src, dst in PAIRS:
    if dst.exists():
        print("skip（もうある）", dst.relative_to(ROOT))
        continue
    t = src.read_text(encoding="utf-8")
    dst.write_text(t.replace("ep30", "ep31").replace("EP30", "EP31"), encoding="utf-8", newline="\n")
    print(dst.relative_to(ROOT), t.count("ep30") + t.count("EP30"))
