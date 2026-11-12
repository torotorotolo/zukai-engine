# -*- coding: utf-8 -*-
"""28本目 ⑥：試写 OK の r01 と、c309 だけ直した r02 を全コマ・全部の音で比べる（直した所のほかが変わっていないか）。

    python -P qa_out/ep32_r02_vs_r01.py [--a=titan_audio-ep32-r01.mp4] [--b=titan_audio-ep32-r02.mp4]
出力＝qa_out/ep32_r01/r02_vs_r01.txt（カットごとの差の最大が大きい順）。
差の平均＝1コマ全体の平均の差（0〜255）・局所＝16×9 に割った升の平均の差の最大。圧縮のにじみは r01 と r02 でも出る＝大きい順に見て、外れるカットを読む。
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
JIKO = HERE / "out" / "jiko"
WIN = HERE / "qa_out" / "ep32_r01" / "windows.json"
OUT = HERE / "qa_out" / "ep32_r01" / "r02_vs_r01.txt"
W, H, BW = 480, 270, 30


def arg(k, d):
    return next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith(f"--{k}=")), d)


def frames(p):
    pr = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(p), "-map", "0:v:0",
                           "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
                          stdout=subprocess.PIPE, bufsize=W * H * 16)
    while True:
        b = pr.stdout.read(W * H)
        if len(b) < W * H:
            break
        yield np.frombuffer(b, np.uint8).astype(np.int16)
    pr.wait()


def pcm(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(p), "-map", "0:a:0", "-ac", "1", "-ar", "48000",
                        "-f", "s16le", "-"], capture_output=True)
    if r.returncode:
        raise SystemExit(f"🔴 音を読めない {p.name}: {r.stderr[:200]}")
    return r.stdout


def main():
    a, b = JIKO / arg("a", "titan_audio-ep32-r01.mp4"), JIKO / arg("b", "titan_audio-ep32-r02.mp4")
    t, cuts = 0.0, []
    for cid, sec, _ in json.loads(WIN.read_text(encoding="utf-8")):
        cuts.append((cid, t, t + sec))
        t += sec
    stat = {c[0]: [0.0, 0.0, -1, 0] for c in cuts}      # 差の平均の最大・局所の最大・その秒・コマ数
    i, k, n = 0, 0, 0
    ga, gb = frames(a), frames(b)
    for fa, fb in zip(ga, gb):
        s = n / 30.0
        while k + 1 < len(cuts) and s >= cuts[k][2]:
            k += 1
        d = np.abs(fa - fb).reshape(H, W)
        m = float(d.mean())
        loc = float(d.reshape(H // BW, BW, W // BW, BW).mean(axis=(1, 3)).max())
        st = stat[cuts[k][0]]
        st[3] += 1
        if m > st[0]:
            st[0], st[2] = m, s - cuts[k][1]
        st[1] = max(st[1], loc)
        n += 1
    left_a, left_b = sum(1 for _ in ga), sum(1 for _ in gb)
    pa, pb = pcm(a), pcm(b)
    x = np.frombuffer(pa, np.int16)
    y = np.frombuffer(pb, np.int16)
    m = min(len(x), len(y))
    dif = (x[:m].astype(np.int32) - y[:m].astype(np.int32))
    rms = float(np.sqrt(np.mean(dif.astype(np.float64) ** 2)))
    first = int(np.argmax(dif != 0)) if dif.any() else -1
    lines = [f"比べた物 {a.name} ／ {b.name}",
             f"コマ {n:,}（余り a {left_a}・b {left_b}）",
             f"音 md5 {hashlib.md5(pa).hexdigest()[:12]} ／ {hashlib.md5(pb).hexdigest()[:12]}・長さ {len(x):,} ／ {len(y):,} 標本・"
             f"差の RMS {rms:.2f}（16bit）・最大 {int(np.abs(dif).max())}・最初の差 {first / 48000 if first >= 0 else 0:.3f} 秒" +
             ("・完全に同じ" if pa == pb else ""),
             "", "カット  差の平均の最大  局所の最大  その位置（カットの頭から・秒）  コマ数"]
    for cid, st in sorted(stat.items(), key=lambda kv: -kv[1][0])[:25]:
        lines.append(f"{cid}  {st[0]:7.2f}  {st[1]:7.2f}  {st[2]:7.2f}  {st[3]}")
    all_m = sorted(st[0] for st in stat.values() if st[3])
    lines.append(f"\nカット数 {len(all_m)}・差の平均の最大の中央値 {all_m[len(all_m) // 2]:.2f}")
    text = "\n".join(lines)
    OUT.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
