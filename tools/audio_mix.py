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

■ 🔴 2026-07-31：語尾が BGM に埋もれていた（カズヤくんの試写指摘①）
  冒頭の「午前10時47分」が「じゅうじ よんじゅうなな」と聞こえた。
  読みは正しかった（kana_log も YOMI 辞書も `ジュウジヨンジュウナナフン`）。
  `tools/check_mora.py` で実測した原因はこうだった。

  | 80〜400Hz（鼻音「ン」の帯）で測った値 | |
  |---|---|
  | 直前の母音「ナ」 | 母音は BGM の **20dB 上** |
  | 文末の「ン」     | BGM の **1.5dB 上**しかない |

  日本語の「ン」は 80〜400Hz の鼻音 murmur にしか実体が無い。
  ところがドローンは 27.5／55／82.5／110／164.8Hz ＝**まったく同じ帯**を鳴らす。
  → 語尾が丸ごとマスクされる。**辞書を触ってはいけない事案だった。**

  直した2点（どちらもドローンの「低い持続音」という性格は壊さない）
   ① 声とぶつかる倍音（82.5／110／164.8Hz）を削る。
      ⚠️ ドローンのエネルギーは **89.9% が 80Hz 未満**にある。
         声の帯に居るのは 9.8% だけなので、そこを削っても低音の圧は残る。
   ② ナレーションが鳴っている間だけ寝床を下げる（サイドチェイン）。
      カット間の無音では元の高さに戻るので、間で BGM が息を吹き返す。

  検査 … `python tools/check_mask.py`（語尾とドローンの余裕 dB を全417行で測る）
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

# 🔴 サイドチェイン：ナレーションが鳴っている間だけ寝床を下げる（2026-07-31）。
#    深さは実測で決めた。**倍音を削るだけでは語尾の余裕が基準に届かなかった**ので併用する。
#    立ち上がりを速く・戻りを遅くすると、文と文の切れ目で BGM が持ち上がって
#    「うねって」聞こえる。**戻りをゆっくり（1.1秒）**にしてうねりを消す。
DUCK_DB = 7.0            # 話しているあいだ寝床を何dB下げるか
DUCK_ATK = 0.12          # 下がりきるまで（秒）
DUCK_REL = 1.10          # 戻りきるまで（秒）
DUCK_FLOOR = -42.0       # これ以下のナレーションは「鳴っていない」とみなす（dBFS）

# 🔴 2026-07-31：ここはテスト映像（アロハ航空）のカットIDのままだった。
#    `p1` `c2` `c4` `c5` はタイタン号の台本に存在しないので、**心拍も衝撃音も
#    一度も鳴らないまま34分が焼かれるところだった。**
#
# ■ どこに入れるかの判断（人が亡くなる場面には入れない）
#    心拍は「見ている人が危険に気づく」ところに入れる。**人が亡くなる場面には入れない。**
#    c115b（耐圧殻が壊れ、5名が亡くなった）に鼓動を敷くのは、
#    デリケートな事象の利用(exploit)に近づく。規約でもチャンネルの性格でも取らない。
#    → 装置が警告し続けていたと分かる c529〜c534 と、
#      11か月の空白から88回目へ向かう c614〜c617 に入れる。
HEART_CUTS = {"c529", "c530", "c531", "c532", "c533", "c534",
              "c614", "c615", "c616", "c617"}
# 低い衝撃音は**掴みの1回だけ**。爆縮の瞬間には置かない。
# そこに衝撃音を置くと「再現音」になり、実際に鳴っていない音を足すことになる
# （2026-07-29 決定：再現音は入れない）。
IMPACT_AT = {"pr01": 0.15}


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
    """低い持続音。純音を重ねると機械的なので、わずかに離調させてうねらせる。

    🔴 2026-07-31：82.5／110／164.8Hz を削った。
       ここは阿井田茂（男声）の基本周波数と鼻音「ン」の murmur が乗る帯で、
       **語尾がまるごとマスクされていた**（実測 1.5dB 差）。
       ドローンのエネルギーの 89.9% は 80Hz 未満にあるので、
       削っても「低く重い持続音」という性格は残る。
    """
    t = np.arange(n) / SR
    y = np.zeros(n)
    for f, a in ((27.5, 0.55), (55.0, 1.00), (55.31, 0.85), (82.5, 0.20),
                 (110.0, 0.07), (164.8, 0.00)):
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


def duck_gain(narr, n, blk=None):
    """ナレーションが鳴っているあいだ寝床を下げる倍率を、10ms ごとに返す。

    🔴 全長ぶんの倍率を配列で持つと 34 分で 720MB になる。**ブロック単位で持つ**。
       立ち上がり 0.12 秒・戻り 1.10 秒の一極フィルタなので、
       10ms のブロックのまま掛けても段差は聞こえない。
    """
    blk = blk or int(0.010 * SR)
    k = n // blk
    lv = np.zeros(k)
    m = min(k * blk, len(narr))
    lv[:m // blk] = np.abs(narr[:m].reshape(-1, blk)).max(axis=1)
    lv = 20 * np.log10(lv + 1e-12)
    tgt = np.where(lv > DUCK_FLOOR, 10 ** (-DUCK_DB / 20), 1.0)
    # 一極の追従（下がるのは速く、戻るのはゆっくり）
    ka = 1 - np.exp(-blk / SR / max(DUCK_ATK, 1e-6))
    kr = 1 - np.exp(-blk / SR / max(DUCK_REL, 1e-6))
    g = np.empty(k)
    cur = 1.0
    for i, v in enumerate(tgt):
        cur += (v - cur) * (ka if v < cur else kr)
        g[i] = cur
    return g, blk


def main(head=None, out_name="mix.wav", duck=True):
    """head に秒を渡すと**先頭その秒だけ**を混ぜる。

    🔴 34分ぶんを混ぜると float64 の配列だけで数GBになり、**4GBのPCでは開けない**。
       聴き比べのために頭だけ焼きたいときは `--head=14` を使う。
    """
    cuts = S.CUTS
    if head:
        keep, t = [], 0.0
        for cid, sec in cuts:
            keep.append((cid, sec))
            t += sec
            if t >= head:
                break
        cuts = keep
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

    # 🔴 サイドチェイン。**ナレーションだけ**を鍵にして寝床を下げる
    #    （心拍と衝撃音は鍵に入れない。鳴った瞬間に BGM が沈んで不自然になる）。
    if duck:
        dg, blk = duck_gain(mix, n)
        for i, v in enumerate(dg):
            bed[i * blk:(i + 1) * blk] *= v
        print(f"サイドチェイン：話している時間 {100 * (dg < 0.9).mean():.0f}% ／ "
              f"最大 {-20 * np.log10(dg.min()):.1f}dB 下げた")

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
        if cid not in starts:
            continue
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
    p = out / out_name
    with wave.open(str(p), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print(f"wrote {p}  {total:.1f}秒  ピーク {np.abs(mix).max():.2f}")


if __name__ == "__main__":
    import sys as _s
    hd = next((float(a.split("=")[1]) for a in _s.argv[1:] if a.startswith("--head=")), None)
    nm = next((a.split("=")[1] for a in _s.argv[1:] if a.startswith("--out=")), "mix.wav")
    main(head=hd, out_name=nm, duck="--noduck" not in _s.argv[1:])
