# -*- coding: utf-8 -*-
"""29本目 ⑥：28本目の受け取りの道具を写す（ep28 → ep29 の字の置き換えだけ・中身は変えない）。
    python -P qa_out/ep29_r01/mktools.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa_out"
NAMES = ["ep28_r01_cutframes", "ep28_r01_ground", "ep28_r01_seen", "ep28_r01_sheet", "ep28_r01_subscan",
         "ep28_r01_voiceq", "ep28_r01_vs_qa", "ep28_r01_where", "ep28_r02_vs_r01", "ep28_r02_verify_upload"]
for n in NAMES:
    src = QA / f"{n}.py"
    dst = QA / f"{n.replace('ep28', 'ep29')}.py"
    t = src.read_text(encoding="utf-8")
    dst.write_text(t.replace("ep28", "ep29").replace("EP28", "EP29"), encoding="utf-8", newline="\n")
    print(dst.name, t.count("ep28"))
