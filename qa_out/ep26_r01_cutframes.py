# -*- coding: utf-8 -*-
"""26本目 ⑥：本編の mp4 から、カットごとに1コマ（検品の静止画といちばん合う瞬間＝`vs_qa.tsv` の t_mp4）を原寸で抜き出す
（25本目 `ep25_r01_cutframes.py` の写し）。

なぜ：字幕の門番 `qa_out/sub_center.py` は「静止画のフォルダ（cut_<cid>.jpg）」を測る作り＝本編そのものの字幕を測るために、
     本編のコマを同じ名前で置く（記憶の決め「焼いたら毎回 sub_center」）。扉（card_）は字幕が無いので抜かない。
⚠️ いちばん合うコマが字幕の消え際に当たると sub_center が誤報する（17本目 ⑥ の落とし穴・26本目の c204 は字幕の出る途中だった）
   ＝鳴ったら同じ字幕のはっきり出たコマで測り直す。
⚠️ 26本目は C: の空きが多い（10-28 で 24GB）＝抜いたコマ（約100MB）は既定で out/jiko/ep26_r01_frames（--out で替えられる）。

    python qa_out/ep26_r01_cutframes.py   → out/jiko/ep26_r01_frames/cut_<cid>.jpg
    python qa_out/sub_center.py out/jiko/ep26_r01_frames
"""
import csv
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
TSV = HERE / "qa_out" / "ep26_r01" / "vs_qa.tsv"


def main():
    mp4 = HERE / "out" / "jiko" / next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")),
                                       "titan_audio-ep26-r01.mp4")
    out = Path(next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--out=")),
                    str(HERE / "out" / "jiko" / "ep26_r01_frames")))
    if not mp4.exists() or not TSV.exists():
        raise SystemExit(f"🔴 mp4 か vs_qa.tsv が無い（{mp4}・{TSV}）")
    rows = [r for r in csv.DictReader(TSV.open(encoding="utf-8"), delimiter="\t") if not r["cut"].startswith("card_")]
    out.mkdir(parents=True, exist_ok=True)
    bad = []
    for r in rows:
        p = out / f"cut_{r['cut']}.jpg"
        q = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{float(r['t_mp4']):.3f}", "-i", str(mp4),
                            "-frames:v", "1", "-q:v", "2", str(p)], capture_output=True)
        if q.returncode or not p.exists():
            bad.append(r["cut"])
    print(f"抜いたコマ {len(rows) - len(bad)}／{len(rows)}・取れない {len(bad)}：{' '.join(bad) or 'なし'}  → {out}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
