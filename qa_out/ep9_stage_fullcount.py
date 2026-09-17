# -*- coding: utf-8 -*-
"""⑤c' 机上で全数へ広げる（c718・c109 の型）。描画はしない。

 A. 検品静止画を撮った秒に、出そろっていない段があるカット（＝シートがその段を見ていない）
 B. 段が出そろってから、カットの終わりまで 1.0 秒未満しか無い段
 C. compare の ref（破線の枠の注記）が、1本目の棒の上端の線に接する・棒の中に入る
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import scene_jiko as S  # noqa: E402
import build_jiko as B  # noqa: E402

idx, jobs = S.layer_index()
meta = B.meta_of(idx)
secs = dict(S.CUTS)


def shot_at(cid, sec, at=0.92):
    rows = S.SUBS.get(cid)
    if not rows:
        return sec * at
    last = rows[-1]
    full_until = last["t"] + last["d"] + S.LEAD + 0.12 - 0.14
    t = max(min(sec * at, full_until), min(sec * 0.70, full_until))
    held = (meta.get(cid) or {}).get("held") or []
    if held:
        times = meta[cid]["times"]
        start = max(times[i][0] for i in held if i < len(times))
        t = max(t, min(start + 0.6, sec - 0.10))
    return t


def texts(svg):
    svg = re.sub(r"<tspan[^>]*>", "", svg or "").replace("</tspan>", "")
    return [re.sub(r"<[^>]+>", "", m) for m in re.findall(r"<text[^>]*>(.*?)</text>", svg)]


A, Bs, C = [], [], []
for cid in [c for c in S.ORDER if c in idx]:
    sec = secs[cid]
    t = shot_at(cid, sec)
    spec = S.SPEC[cid]
    photo_only = bool(spec.get("photo")) and not spec.get("fig")
    for i, (a, b) in enumerate(meta[cid]["times"]):
        span = 0.45 if photo_only else B.draw_span(b - a)
        k = max(0.0, min(1.0, (t - a) / span))
        name = f"{cid}_a{i + 1}"
        tx = " / ".join(texts(jobs.get(name)))[:60]
        if k < 1.0:
            A.append(f"{cid} 段{i + 1}/{len(meta[cid]['times'])} k={k:.2f}（撮った {t:.2f}s・出そろう {a + span:.2f}s・尺 {sec:.2f}s）「{tx}」")
        full = a + span
        if sec - full < 1.0:
            Bs.append(f"{cid} 段{i + 1}/{len(meta[cid]['times'])} 出そろって {sec - full:.2f}s で切り替わる（出はじめ {a:.2f}s・出そろう {full:.2f}s・尺 {sec:.2f}s）「{tx}」")
    fig = spec.get("fig")
    if fig and fig[0] == "compare" and fig[1].get("ref"):
        svg = jobs.get(f"{cid}_a1", "")
        dash = re.search(r'<rect[^>]*y="([\d.]+)"[^>]*stroke-dasharray', svg)
        tm = re.search(r'<text[^>]*y="([\d.]+)"[^>]*font-size="([\d.]+)"', svg)
        bars = [float(v) for v in re.findall(r'<rect[^>]*y="([\d.]+)"[^>]*fill="#[0-9a-f]{6}" opacity', svg)]
        if dash and tm and bars:
            fy, ty, fs = float(dash.group(1)), float(tm.group(1)), float(tm.group(2))
            top = bars[0]
            gap = (top - 2) - (ty - 0.80 * fs)      # 棒の上端の線の上側 − 字の頭（負なら線が字にかかる／字が棒の中）
            C.append(f"{cid} 破線の枠 y{fy:.0f}・注記の字 y{ty - 0.80 * fs:.0f}〜{ty + 0.10 * fs:.0f}・1本目の棒の上端 y{top:.0f}"
                     f"（線 y{top - 2:.0f}〜{top + 2:.0f}）→ {'🔴 字が棒の中／線に接する' if top + 2 > ty - 0.80 * fs - 1 else '・離れている'}"
                     f"  ref「{fig[1]['ref']}」")

print(f"■ A. 撮った秒に出そろっていない段（{len(A)}件）")
print("\n".join("  " + s for s in A) or "  なし")
print(f"\n■ B. 出そろってから 1.0 秒未満で切り替わる段（{len(Bs)}件）")
print("\n".join("  " + s for s in Bs) or "  なし")
print(f"\n■ C. compare の ref（{len(C)}件）")
print("\n".join("  " + s for s in C) or "  なし")
