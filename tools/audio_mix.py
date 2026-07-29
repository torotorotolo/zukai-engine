# -*- coding: utf-8 -*-
"""ナレーション・BGM・効果音を1本のトラックに混ぜる。

■ なぜ BGM を自作の合成音にしたか（2026-07-29）
  DOVA-SYNDROME や 甘茶の音楽工房 は商用可・クレジット不要で規約上は使える。
  ただし **DOVA は「音源ファイルの配布」を禁じている**。
  このリポジトリは Actions の課金制限を避けるため **public** にしてあるので、
  mp3 を置くと再配布に当たる恐れがある（実際に規約へ明記されている）。
  そこで、事故検証の音づくりに必要な要素だけを自前で合成する。
  権利問題がゼロになり、尺にも完全に合わせられる。
  → 専用アカウントで private リポジトリを用意できたら、既製BGMに差し替えてよい。

■ 音の設計（シリアス・恐怖感）
  ドローン   … 低い持続音。55Hz を軸に少しだけ離調させてうねりを作る
  下支え     … 27.5Hz の超低音。鳴っていると気づかないが、抜くと軽くなる
  空気       … ごく小さいノイズ。無音の「死んだ感じ」を消す
  心拍       … 48拍/分。**原因が判明していく c4 / c5 だけ**に入れる
  低い衝撃音 … 掴み(p1)と、剥離の瞬間(c2)の2回だけ

  ⚠️ 金属の軋みや警報の「再現音」は入れない。
     実際の事故で鳴っていない音を足すと、検証番組としての信用が落ちる。
     （2026-07-29 カズヤくん決定：効果音は控えめ＝低い衝撃音と心拍だけ）

■ 音量（深読みフクロウの実績値 BGM 0.12 に合わせる）
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S

SR = 44100
HERE = S.HERE
V_NARR = 1.00
V_BGM = 0.12
V_HEART = 0.10
V_IMPACT = 0.30

HEART_CUTS = {"c4", "c5"}          # 原因に踏み込むところだけ鼓動を入れる
IMPACT_AT = {"p1": 0.15, "c2": 0.40}   # 掴みと、剥離の瞬間


def read_wav(p):
    with wave.open(str(p)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        if w.getnchannels() == 2:
            a = a.reshape(-1, 2).mean(axis=1)
        if w.getframerate() != SR:
            n = int(len(a) * SR / w.getframerate())
            a = np.interp(np.linspace(0, len(a), n, endpoint=False),
                          np.arange(len(a)), a)
    return a.astype(np.float64) / 32768.0


def drone(n):
    """低い持続音。純音を重ねると機械的なので、わずかに離調させてうねらせる。"""
    t = np.arange(n) / SR
    y = np.zeros(n)
    for f, a in ((27.5, 0.55), (55.0, 1.00), (55.31, 0.85), (82.5, 0.42),
                 (110.0, 0.20), (164.8, 0.07)):
        y += a * np.sin(2 * np.pi * f * t + a * 3.1)
    y /= 3.1
    # 11秒周期のゆっくりした膨らみ
    y *= 0.62 + 0.38 * (0.5 - 0.5 * np.cos(2 * np.pi * t / 11.0))
    # 空気（ごく小さいノイズ。移動平均で高域を落とす）
    rng = np.random.default_rng(20260729)
    air = rng.standard_normal(n)
    k = 24
    air = np.convolve(air, np.ones(k) / k, mode="same")
    y += 0.10 * air / (np.abs(air).max() + 1e-9)
    return y


def heartbeat(n, bpm=48.0):
    """48拍/分。lub-dub の2打で1拍。低い正弦に速い減衰をかける。"""
    y = np.zeros(n)
    period = 60.0 / bpm
    for beat in np.arange(0, n / SR, period):
        for off, amp in ((0.0, 1.0), (0.30, 0.62)):
            i = int((beat + off) * SR)
            ln = int(0.34 * SR)
            if i + ln > n:
                break
            t = np.arange(ln) / SR
            env = np.exp(-t * 17.0)
            y[i:i + ln] += amp * env * np.sin(2 * np.pi * 46.0 * t)
    return y


def impact(dur=2.4):
    """低い衝撃音。60Hz から 28Hz へ落ちる掃引＋ごく短いノイズの立ち上がり。"""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 60.0 * np.exp(-t * 1.5) + 26.0
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t * 2.1)
    rng = np.random.default_rng(4321)
    nz = rng.standard_normal(n) * np.exp(-t * 26.0)
    k = 40
    nz = np.convolve(nz, np.ones(k) / k, mode="same")
    y += 0.9 * nz / (np.abs(nz).max() + 1e-9)
    return y / (np.abs(y).max() + 1e-9)


def main():
    cuts = S.CUTS
    total = sum(s for _, s in cuts)
    n = int(total * SR) + SR
    bed = drone(n) * V_BGM
    mix = np.zeros(n)

    starts, t = {}, 0.0
    for cid, sec in cuts:
        starts[cid] = t
        t += sec

    # ナレーション
    audio = HERE / "audio"
    for cid, _ in cuts:
        p = audio / f"{cid}.wav"
        if not p.exists():
            print(f"! {cid}.wav が無い")
            continue
        a = read_wav(p) * V_NARR
        i = int((starts[cid] + S.LEAD) * SR)
        mix[i:i + len(a)] += a[:max(0, n - i)]

    # 心拍（該当カットだけ。頭で 0.8 秒かけて立ち上げ、尻で落とす）
    hb = heartbeat(n) * V_HEART
    gate = np.zeros(n)
    for cid, sec in cuts:
        if cid not in HEART_CUTS:
            continue
        i, j = int(starts[cid] * SR), int((starts[cid] + sec) * SR)
        ramp = int(0.8 * SR)
        g = np.ones(j - i)
        g[:ramp] = np.linspace(0, 1, ramp)
        g[-ramp:] = np.linspace(1, 0, ramp)
        gate[i:j] = np.maximum(gate[i:j], g)
    mix += hb * gate

    # 低い衝撃音
    imp = impact()
    for cid, off in IMPACT_AT.items():
        i = int((starts[cid] + off) * SR)
        e = min(n, i + len(imp))
        mix[i:e] += imp[:e - i] * V_IMPACT

    mix += bed
    peak = np.abs(mix).max()
    if peak > 0.97:
        mix *= 0.97 / peak
        print(f"ピークが {peak:.2f} だったので {0.97 / peak:.3f} 倍に下げた")

    out = HERE / "out" / "jiko"
    out.mkdir(parents=True, exist_ok=True)
    p = out / "mix.wav"
    with wave.open(str(p), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print(f"wrote {p}  {total:.1f}秒  ピーク {np.abs(mix).max():.2f}")


if __name__ == "__main__":
    main()
