# -*- coding: utf-8 -*-
"""32本目 ⑥：c101 のしぶき（⑤c' で区間の頭を 7.0→5.0 にした＝しぶきの最大はカットの途中）を本編の動きとして数える。
本編の c101（0〜カットの尻）を 480×270 の灰色で1コマずつ読み、白い跳ね（明るさ 225 以上）の画素を数える。
数える所＝縦 15〜80%（上の見出しと下の字幕の帯を外す）・横 0〜65%（左の水面）。0.1秒ごとの最大を出し、山の秒を語りと照らす。
語りの秒＝`qa_out/ep32_r01/shisha_times.tsv` の c101-2（「沿岸警備隊のカメラの映像だ。白いしぶきは、…」）の頭と字の割合。
    python -P qa_out/ep32_r01/splash.py   → 山の秒と、山・山の前・山の後ろのコマ（out は qa_out/ep32_r01/_frames）
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
MP4 = ROOT / "out" / "jiko" / "titan_audio-ep32-r01.mp4"
W, H, FPS = 480, 270, 30
win = json.loads((ROOT / "qa_out" / "ep32_r01" / "windows.json").read_text(encoding="utf-8"))
dur = win[0][1]
assert win[0][0] == "c101"
p = subprocess.run(["ffmpeg", "-v", "error", "-t", f"{dur:.3f}", "-i", str(MP4), "-vf", f"scale={W}:{H}",
                    "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
a = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W)
roi = a[:, int(H * 0.15):int(H * 0.80), :int(W * 0.65)].astype(np.int16)
# 🔧 11-12：明るさ 225 の決め打ちは全コマ 4〜6画素＝測れていなかった（VTS は灰色寄り）→ そのコマの中央値より 35 以上明るい画素に替えた
med = np.median(roi.reshape(len(roi), -1), axis=1).astype(np.int16)
cnt = (roi >= (med[:, None, None] + 35)).sum(axis=(1, 2))
print(f"c101 尺 {dur}秒・コマ {len(a)}")
per = {}
for i, c in enumerate(cnt):
    k = round(int(i / FPS * 10) / 10, 1)
    per[k] = max(per.get(k, 0), int(c))
pk = max(per, key=per.get)
print(f"白い跳ねの画素（0.1秒ごとの最大）：山 {pk:.1f}秒＝{per[pk]}・中央値 {int(np.median(list(per.values())))}")
print("  " + " ".join(f"{k:.1f}:{v}" for k, v in sorted(per.items()) if abs(k * 10 % 5) < 1e-6))
# 語り（c101-2 の頭と、「白いしぶきは」までの字の割合で見込む＝目安）
import csv
rows = list(csv.DictReader((ROOT / "qa_out" / "ep32_r01" / "shisha_times.tsv").open(encoding="utf-8"), delimiter="\t"))
r2 = next(r for r in rows if r["行ID"] == "c101-2")
r3 = next(r for r in rows if r["行ID"] == "c102-1")
t2, t3 = float(r2["新しい秒"]), float(r3["新しい秒"])
txt = r2["文"]
i0 = txt.index("白いしぶき")
print(f"語り c101-2 の頭 {t2:.2f}秒（次の行 c102-1 は {t3:.2f}秒）・「白いしぶき」は字の {i0}/{len(txt)} ＝ 見込み 約{t2 + (t3 - 0.35 - t2) * i0 / len(txt):.1f}秒")
for tag, s in (("前", max(0.0, pk - 1.5)), ("山", pk), ("後", min(dur - 0.1, pk + 1.5))):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{s:.2f}", "-i", str(MP4), "-frames:v", "1",
                    str(ROOT / "qa_out" / "ep32_r01" / "_frames" / f"splash_{tag}.png")], check=True)
    print(f"  コマ {tag} {s:.2f}秒 → _frames/splash_{tag}.png")
