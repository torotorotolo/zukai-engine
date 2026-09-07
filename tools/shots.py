# -*- coding: utf-8 -*-
"""記録映像の**ショットの境目**を1秒刻みで採る（工程の新設計 §6 の②）。

■ なぜ要るか（4本目サーフサイドで3件踏んだ）
    `footage.USE` の注記「128〜133.9秒 レプリカの全景」の**範囲の中で絵が別物**だった
    （c322＝壁の文字／c325＝男性2人の顔／c328＝ひびが無く人物4人）。
    秒を **3秒刻みの見取り図**で選んでいたので、ショットの中の変化と人が入る瞬間を見ていなかった。
    → [[feedback-measure-the-source-before-choosing-the-crop]]

■ 🔴 なぜ `ffmpeg` の scene 検出だけでは足りないか（2026-09-07・SL-1 で実測）
    `select=gt(scene,0.18)` は**ハットな切り替えしか見ない**。1961年の AEC の記録映画は
    **ディゾルブ（重ね消し＝前の絵が薄れながら次の絵が出る）**を多用しており、
    そこでは1コマあたりの変化が小さいので境目として出ない。
    実測：Phase I&II で「1本のショットが **333秒**」と出た（5分半も同じ絵のはずがない）。
    → **1秒ごとの見た目の署名を採って、離れたところを境目にする**（ディゾルブも坂として出る）。

■ 何をしているか
    1. `ffmpeg` で **1秒に1コマ**・64x36 に縮めて全部取り出す（55分で約3,300コマ・1分ほど）
    2. 各コマを署名（64x36 の明度）にして、**隣どうしの距離**を出す
    3. 距離が `CUT` を超えたところを境目にする。ハードな切り替えは1点の山、
       ディゾルブは数秒続く高原になるので、**続いた区間はまとめて1つの境目**として畳む
    4. ショットごとに「中の動きの大きさ」（`motion`＝区間内の隣接距離の中央値）も出す。
       **`motion` が小さい＝静止画に近い**＝`still=True` にすべきショット

■ ⚠️ fail closed
    25分の記録映画で境目が `MIN_CUTS` 本未満なら**止める**（exit 2）。
    ffmpeg の項目名は版で変わる（8.x で `pkt_pts_time` が廃止され `pts_time` になった）。
    黙って0本を返すと「ショットが1本」という**間違った合格**になる。
    → [[feedback-parsers-fail-closed]] / [[feedback-verify-your-own-instrument]]

■ 使い方
    python tools/shots.py probe <mp4> --key sl1_ph12 --out analytics/materials/sl1_shots.json
    python tools/shots.py show analytics/materials/sl1_shots.json --key sl1_ph12
    python tools/shots.py selftest        # 陽性対照（切り替えとディゾルブを作って必ず当てる）
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

W, H = 64, 36           # 署名の大きさ
FPS = 1                 # 🔴 1秒刻み（指示）
CUT = 14.0              # 隣どうしの距離（0〜255 の平均絶対差）がこれを超えたら境目
JOIN = 1                # 境目が連続したら畳む（ディゾルブは数秒続く）
MIN_SHOT = 2.0          # これより短い区間は前のショットに戻す
MIN_CUTS = 20           # 🔴 20分超の記録映像でこれ未満なら「読めていない」とみなす（fail closed）


def signatures(path: Path) -> np.ndarray:
    """1秒に1コマ、64x36 のグレースケールを縦に積んだ配列を返す。"""
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
           "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg が落ちた: {p.stderr.decode('utf-8', 'replace')[:400]}")
    buf = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(buf) // (W * H)
    if n == 0:
        raise RuntimeError("コマが1枚も取れなかった（ffmpeg の出力が空）")
    return buf[:n * W * H].reshape(n, H, W).astype(np.int16)


def boundaries(sig: np.ndarray):
    """隣どうしの距離から境目の秒を出す。ディゾルブ（続く高原）は1つに畳む。"""
    d = np.abs(np.diff(sig, axis=0)).mean(axis=(1, 2))       # 秒 i と i+1 の距離
    hot = np.flatnonzero(d > CUT) + 1                        # 境目は「後ろ側」の秒
    cuts, run = [], []
    for s in hot:
        if run and s - run[-1] <= JOIN:
            run.append(s)
        else:
            if run:
                cuts.append(int(round(np.mean(run))))
            run = [s]
    if run:
        cuts.append(int(round(np.mean(run))))
    return cuts, d


def shots_of(path: Path):
    sig = signatures(path)
    dur = len(sig) / FPS
    cuts, d = boundaries(sig)
    if dur > 1200 and len(cuts) < MIN_CUTS:
        raise SystemExit(f"🔴 {path.name}: {dur:.0f}秒で境目が {len(cuts)} 本しか出ていない。"
                         f"読めていない疑い（ffmpeg の版・項目名を確かめる）")
    edges = [0] + cuts + [int(dur)]
    out = []
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        if b - a < MIN_SHOT and out:                          # 短すぎる区間は前に戻す
            out[-1]["until"] = float(b)
            continue
        seg = d[a:max(b - 1, a + 1)]
        out.append(dict(start=float(a), until=float(b),
                        motion=round(float(np.median(seg)) if len(seg) else 0.0, 2)))
    return out, dur


def show(shots, dur, key):
    L = sorted(s["until"] - s["start"] for s in shots)
    n = len(L)
    still = [s for s in shots if s["motion"] < 2.0]
    print(f"== {key} ==  {dur:.0f}秒／ショット {n} 本")
    print(f"  長さ 中央値 {L[n // 2]:.0f}s・平均 {sum(L) / n:.1f}s・最短 {L[0]:.0f}s・最長 {L[-1]:.0f}s")
    for thr in (4, 6, 8, 10, 15):
        k = [x for x in L if x >= thr]
        print(f"   {thr:>2}秒以上: {len(k):>3} 本（合計 {sum(k) / 60:.1f}分）")
    print(f"  ほぼ静止（motion<2.0）: {len(still)} 本 ＝ still=True 向き")


def selftest():
    """陽性対照＝切り替えとディゾルブを作った映像で、境目を必ず当てる。"""
    rng = np.random.default_rng(0)
    A = rng.integers(0, 60, (H, W)).astype(np.int16)          # 暗い絵
    B = rng.integers(190, 255, (H, W)).astype(np.int16)       # 明るい絵
    C = rng.integers(0, 60, (H, W)).astype(np.int16)
    frames = [A] * 10                                          # 0-9秒  A
    frames += [B] * 10                                         # 10秒で ハードな切り替え
    for i in range(1, 5):                                      # 20-23秒 ディゾルブ B→C
        frames.append((B * (1 - i / 5) + C * (i / 5)).astype(np.int16))
    frames += [C] * 10                                         # 24-33秒 C
    sig = np.stack(frames)
    cuts, d = boundaries(sig)
    ok = True
    want = [(10, 10), (21, 23)]                                # ハード＝10秒ちょうど／ディゾルブ＝21〜23秒
    print(f"  出た境目: {cuts}")
    for lo, hi in want:
        hit = [c for c in cuts if lo <= c <= hi]
        flag = "OK" if hit else "🔴 NG"
        ok &= bool(hit)
        print(f"  {flag} {lo}〜{hi}秒に境目（出た: {hit}）")
    flag = "OK" if len(cuts) == 2 else "🔴 NG"
    ok &= len(cuts) == 2
    print(f"  {flag} 境目は2本（ディゾルブを何本にも割らない）＝ {len(cuts)} 本")
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["probe", "show", "selftest"])
    ap.add_argument("target", nargs="?")
    ap.add_argument("--key", default="clip")
    ap.add_argument("--out")
    a = ap.parse_args()

    if a.cmd == "selftest":
        return selftest()

    if a.cmd == "show":
        d = json.load(open(a.target, encoding="utf-8"))
        e = d[a.key]
        return show(e["shots"], e["dur"], a.key) or 0

    shots, dur = shots_of(Path(a.target))
    show(shots, dur, a.key)
    if a.out:
        p = Path(a.out)
        d = json.load(open(p, encoding="utf-8")) if p.exists() else {}
        d[a.key] = dict(src=Path(a.target).name, dur=round(dur, 2), shots=shots)
        p.parent.mkdir(parents=True, exist_ok=True)
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"→ {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
