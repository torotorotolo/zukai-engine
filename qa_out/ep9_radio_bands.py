# -*- coding: utf-8 -*-
"""⑤c' 机上：radio の帯（bands）が、その時間に送信の無い段へ四角を出すカットを全数で数える。

2026-09-17（⑤c''）：**焼く前の SVG の四角を数える形に書き直した。**
前の版は SPEC の events と bands だけを見ていたので、型（`band_svg`）が塗る段を変えても
同じ答えを出し続けた（＝型の直しを見ていない物差し）。
帯の四角＝`rect` の高さ 52（送信の帯は 44）。四角の y から段を逆算し、その段に帯の時間と
重なる送信があるかを SPEC で照らす。

    python qa_out/ep9_radio_bands.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402
import titan_fig as T  # noqa: E402

jobs, _ = S.build_layers()
n_cut = n_band = n_bad = n_rect = 0
for cid in S.ORDER:
    fig = (S.SPEC.get(cid) or {}).get("fig")
    if not fig or fig[0] != "radio":
        continue
    kw = fig[1]
    bands = kw.get("bands") or []
    if not bands:
        continue
    n_cut += 1
    lanes = kw["lanes"]
    n = max(1, len(lanes))
    top, bot = T.BY0 + 76, T.BY1 - 150
    lh = (bot - top) / n
    svg = "".join(v for k, v in jobs.items() if k.startswith(cid + "_"))
    got = []
    for m in re.finditer(r"<rect ([^>]*)>", svg):
        at = m.group(1)
        h = re.search(r'height="([\d.]+)"', at)
        if not h or abs(float(h.group(1)) - 52) > 0.01:
            continue
        y = float(re.search(r'\by="([\d.-]+)"', at).group(1))
        got.append(round((y + 26 - top) / lh - 0.5))
    n_rect += len(got)
    for b in bands:
        n_band += 1
        busy = {e.get("lane", 0) for e in kw["events"]
                if e["a"] <= b["b"] and (e["b"] if e.get("b") is not None else e["a"]) >= b["a"]}
        painted = sorted(set(got))
        bad = [lanes[i] for i in painted if i not in busy]
        n_bad += len(bad)
        print(f"{cid} 帯「{b.get('t', '')}」{b['a']}〜{b['b']}  段 {n}  四角のある段 "
              f"{'／'.join(lanes[i] for i in painted)}  送信の無い段に四角: "
              f"{'／'.join(bad) if bad else 'なし'}")
print(f"帯のある radio カット {n_cut}・帯 {n_band}・帯の四角 {n_rect}・送信の無い段の四角 {n_bad}")
# fail closed：帯があるのに四角を1つも拾えなければ、物差しが外れている
if n_band and not n_rect:
    print("🔴 帯の四角を1つも拾えなかった（rect の書き方が変わったか）")
    sys.exit(1)
sys.exit(1 if n_bad else 0)
