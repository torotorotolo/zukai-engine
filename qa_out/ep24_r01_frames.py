# -*- coding: utf-8 -*-
"""24本目 ⑥：本編の mp4 から、カットごとに1コマ（検品の静止画といちばん合う瞬間＝`vs_qa.tsv` の t_mp4）を原寸で抜き出す
（23本目 `ep23_r01_frames.py` の写し）。

なぜ：字幕の門番 `qa_out/sub_center.py` は「静止画のフォルダ（cut_<cid>.jpg）」を測る作り＝本編そのものの字幕を測るために、
     本編のコマを同じ名前で置く（記憶の決め「焼いたら毎回 sub_center」）。扉（card_）は字幕が無いので抜かない。
⚠️ いちばん合うコマが字幕の消え際に当たると sub_center が誤報する（17本目 ⑥ の落とし穴）＝鳴ったら同じ字幕のはっきり出たコマで測り直す。

    python qa_out/ep24_r01_frames.py [--mp4=titan_audio-ep24-r01.mp4]   → out/jiko/r01_frames_ep24/cut_<cid>.jpg
    python qa_out/sub_center.py out/jiko/r01_frames_ep24
"""
import csv
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
TSV = HERE / "qa_out" / "ep24_r01" / "vs_qa.tsv"
OUT = HERE / "out" / "jiko" / "r01_frames_ep24"


def main():
    mp4 = HERE / "out" / "jiko" / next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")),
                                       "titan_audio-ep24-r01.mp4")
    if not mp4.exists() or not TSV.exists():
        raise SystemExit(f"🔴 mp4 か vs_qa.tsv が無い（{mp4}・{TSV}）")
    rows = [r for r in csv.DictReader(TSV.open(encoding="utf-8"), delimiter="\t") if not r["cut"].startswith("card_")]
    OUT.mkdir(parents=True, exist_ok=True)
    bad = []
    for r in rows:
        p = OUT / f"cut_{r['cut']}.jpg"
        q = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{float(r['t_mp4']):.3f}", "-i", str(mp4),
                            "-frames:v", "1", "-q:v", "2", str(p)], capture_output=True)
        if q.returncode or not p.exists():
            bad.append(r["cut"])
    print(f"抜いたコマ {len(rows) - len(bad)}／{len(rows)}・取れない {len(bad)}：{' '.join(bad) or 'なし'}  → {OUT.relative_to(HERE)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
