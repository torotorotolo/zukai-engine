# -*- coding: utf-8 -*-
"""32本目 ⑥：`qa_out/kb_af_loud.py` の「声なし」に c416 の原音（SPEC の orig＝管制の録音 1.55秒）が入っていないかを確かめる。
kb_af_loud は心拍と衝撃音の区間だけを声なしから外す（原音は 32本目 ⑤b-7 の新しい仕組み＝道具が知らない）。
同じ ebur128 の記録（qa_out/titan_audio-ep32-r01_ebur128.txt）を同じ式で分け、原音の区間を外した値と、
声なしの窓のうち大きい窓（−30 LUFS より上）の時刻を出す。
    python -P qa_out/ep32_r01/loud_orig.py
"""
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "qa_out"))
sys.stdout.reconfigure(encoding="utf-8")
import kb_af_loud as K  # noqa: E402
import scene_jiko as S  # noqa: E402

starts, spans, total = K.timeline()
txt = (ROOT / "qa_out" / "titan_audio-ep32-r01_ebur128.txt").read_text(encoding="utf-8", errors="replace")
fr = re.findall(r"t:\s*([\d.]+)\s+TARGET:\S+ LUFS\s+M:\s*(-?[\d.]+|-inf)", txt)
# 原音の区間＝c416 の語りの終わり＋pre から len 秒（audio_mix の記録＝591.36秒から 1.55秒）
o = S.SPEC["c416"]["orig"]
st = dict(S.CUTS)
t = 0.0
cut0 = {}
for cid, sec in S.CUTS:
    cut0[cid] = t
    t += sec
o0 = 591.36
o1 = o0 + float(o["len"])
sa = np.array([s[0] for s in spans])
sb = np.array([s[1] for s in spans])
res = {"含める": {}, "外す": {}}
loud_q = []
for ts, ms in fr:
    t1 = float(ts)
    t0 = t1 - K.WIN
    m = -120.0 if ms == "-inf" else float(ms)
    if t0 < 0 or t1 > total:
        continue
    if np.any((sa <= t0) & (sb >= t1)) or np.any((sa < t1) & (sb > t0)):
        continue
    ended = sb[sb <= t0]
    since = t0 - ended.max() if len(ended) else 99.0
    k = "0.0-0.5" if since < 0.5 else "0.5-1.0" if since < 1.0 else "1.0-2.0" if since < 2.0 else "2.0+"
    res["含める"].setdefault(k, []).append(m)
    in_orig = t0 < o1 and t1 > o0
    if not in_orig:
        res["外す"].setdefault(k, []).append(m)
    if m > -30.0:
        loud_q.append((t1, m, k, in_orig))
for name, d in res.items():
    allv = []
    for k in ("0.0-0.5", "0.5-1.0", "1.0-2.0", "2.0+"):
        v, n = K.emean(d.get(k, []))
        allv += d.get(k, [])
        print(f"原音を{name}  声なし {k:>7}秒 {v:6.1f} LUFS（窓 {n}）")
    q, _ = K.emean(allv)
    print(f"原音を{name}  声なし（全部） {q:6.1f} LUFS")
print(f"原音の区間 {o0:.2f}〜{o1:.2f}秒・声なしで −30 LUFS より大きい窓 {len(loud_q)} 個（うち原音の区間 {sum(1 for x in loud_q if x[3])} 個）")
for t1, m, k, io in loud_q[:20]:
    cid = next((c for c in reversed(list(cut0)) if cut0[c] <= t1), "?")
    print(f"  {K.mmss(t1)}（{t1:.1f}秒・{cid}）M {m:6.1f}・{k}・{'原音' if io else '原音の外'}")
