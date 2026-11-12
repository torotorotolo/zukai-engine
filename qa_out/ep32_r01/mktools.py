# -*- coding: utf-8 -*-
"""32本目 ⑥：31本目の受け取りの道具を写す（ep31 → ep32 の字の置き換えだけ・中身は変えない）。
    python -P qa_out/ep32_r01/mktools.py
🔴 写したあとに手で直す＝`ep32_r02_verify_upload.py` の DURATIONS・DUR_NOTE（本編の尺）・`receive.sh` の `--qa=`（32本目の検品の絵の置き場）
   ・`mute_vs_scan.py` の図の種類の並び（m32 を足す＝31本目 §7-1）
   ほか 31本目の値（カットの番号・数）が残っていないかを grep で見る
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa_out"
NAMES = ["ep31_r01_cutframes", "ep31_r01_ground", "ep31_r01_seen", "ep31_r01_sheet", "ep31_r01_subscan",
         "ep31_r01_voiceq", "ep31_r01_vs_qa", "ep31_r01_where", "ep31_r02_vs_r01", "ep31_r02_verify_upload"]
PAIRS = [(QA / f"{n}.py", QA / f"{n.replace('ep31', 'ep32')}.py") for n in NAMES]
PAIRS += [(QA / "ep31_r01" / n, QA / "ep32_r01" / n) for n in ("receive.sh", "motion.py", "mute_vs_scan.py")]
for src, dst in PAIRS:
    if dst.exists():
        print("skip（もうある）", dst.relative_to(ROOT))
        continue
    t = src.read_text(encoding="utf-8")
    dst.write_text(t.replace("ep31", "ep32").replace("EP31", "EP32"), encoding="utf-8", newline="\n")
    print(dst.relative_to(ROOT), t.count("ep31") + t.count("EP31"))
