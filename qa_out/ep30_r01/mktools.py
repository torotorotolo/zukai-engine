# -*- coding: utf-8 -*-
"""30本目 ⑥：29本目の受け取りの道具を写す（ep29 → ep30 の字の置き換えだけ・中身は変えない）。
    python -P qa_out/ep30_r01/mktools.py
🔴 写したあとに手で直す＝`ep30_r02_verify_upload.py` の DURATIONS・DUR_NOTE（本編の尺）・`receive.sh` の `--qa=`（30本目の検品の絵の置き場）
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa_out"
NAMES = ["ep29_r01_cutframes", "ep29_r01_ground", "ep29_r01_seen", "ep29_r01_sheet", "ep29_r01_subscan",
         "ep29_r01_voiceq", "ep29_r01_vs_qa", "ep29_r01_where", "ep29_r02_vs_r01", "ep29_r02_verify_upload"]
PAIRS = [(QA / f"{n}.py", QA / f"{n.replace('ep29', 'ep30')}.py") for n in NAMES]
PAIRS += [(QA / "ep29_r01" / n, QA / "ep30_r01" / n) for n in ("receive.sh", "motion.py")]
for src, dst in PAIRS:
    t = src.read_text(encoding="utf-8")
    dst.write_text(t.replace("ep29", "ep30").replace("EP29", "EP30"), encoding="utf-8", newline="\n")
    print(dst.relative_to(ROOT), t.count("ep29"))
