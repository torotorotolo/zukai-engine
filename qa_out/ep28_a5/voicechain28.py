# -*- coding: utf-8 -*-
"""28本目 ⑤a-2：声の EQ（`audio_mix.VOICE_EQ`＝3kHz・1オクターブ・−4dB）で 2〜4kHz がどこまで下がるかを測る（焼き直さない・読むだけ）。

なぜ：記憶 feedback-jiko-yukkuri-audio-quality の案＝本編の 2〜4kHz −13.6 → 約 −16.5（競合 −16.8〜−17.6）。A/B は 27本目の本編（BGM こみ）に
     ffmpeg で掛けた音＝28本目の声で本編と同じ関数を通した数を、推測でなく測る。
物差し＝`qa_out/ep27_r01_voiceq.py` の voiced_psd・bands（27本目 `ep27_r02_voicechain.py` と同じ・声の区間・Hann 4096）。
     本編と同じくカットごとに `audio_mix.voice_chain` を通す。⚠️ BGM・リミッタ・AAC を通した本編の数は ⑥ で mp4 を測る（`ep27_r01_voiceq.py <mp4>`）。

    python -P qa_out/ep28_a5/voicechain28.py             → qa_out/ep28_a5/voicechain28.txt
    python -P qa_out/ep28_a5/voicechain28.py --selftest  … 回の出し分け・山の形・ffmpeg との一致（陽性対照つき）
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE / "tools"))
sys.path.insert(0, str(HERE / "qa_out"))
sys.stdout.reconfigure(encoding="utf-8")
import audio_mix as AM            # noqa: E402
import el_script as ES            # noqa: E402
import ep27_r01_voiceq as V       # noqa: E402
import narration as N             # noqa: E402

RIVALS = "競合3本の 2〜4kHz ＝ −16.8〜−17.6（27本目 ⑥'・完成品の声の区間）"


def row(name, x, sr=AM.SR):
    f, p, sec = V.voiced_psd(x, sr)
    m = f < 22050
    b = V.bands(f[m], p[m])
    c = V.crest(x, sr)
    return f"{name:<30}" + "".join(f"{v:7.1f}" for v in b[:6]) + f"   クレスト {c[0]:.1f}dB・声 {sec / 60:.1f}分"


def main():
    cids = [c for c, _ in N.SCRIPT]
    raw, comp, chain = [], [], []
    for c in cids:
        x = AM.read_wav(HERE / "audio" / f"{c}.wav")      # 本編と同じ：24kHz → 44.1kHz（np.interp）
        raw.append(x)
        comp.append(AM.compress(x))
        chain.append(AM.voice_chain(x))
    head = f"{'':<30}" + "".join(f"{s:>7}" for s in ("0-0.5k", "0.5-1k", "1-2k", "2-4k", "4-8k", "8-12k"))
    lines = [f"■ 28本目 声の道すじの段ごとの帯域（声の区間・全体に対する dB）＝本編の関数・カットごと（{ES.SLUG}・{len(cids)}カット）",
             f"VOICE_EQ＝{AM.voice_eq_ep()}", head,
             row("① 合成の声（read_wav 44.1k）", np.concatenate(raw)),
             row("② ①を compress（本編の値）", np.concatenate(comp)),
             row("③ ②に EQ（voice_chain）", np.concatenate(chain)),
             RIVALS]
    out = HERE / "qa_out" / "ep28_a5" / "voicechain28.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"→ {out}")


def ffmpeg_eq(x, af):
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f64le", "-ar", str(AM.SR), "-ac", "1", "-i", "-",
                        "-af", af, "-f", "f64le", "-ar", str(AM.SR), "-ac", "1", "-"],
                       input=x.astype(np.float64).tobytes(), capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float64)


def band_db(x, lo, hi):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / AM.SR)
    return 10 * np.log10(X[(f >= lo) & (f < hi)].sum() + 1e-30)


def selftest():
    bad = []

    def ok(name, cond, note=""):
        print(f"  {'✓' if cond else '✗'} {name} {note}")
        if not cond:
            bad.append(name)

    rng = np.random.default_rng(20261101)
    x = rng.standard_normal(AM.SR * 6) * 0.1
    keep = ES.SLUG
    try:
        # 回の出し分け：27本目までは compress と1標本も違わない・28本目からは違う
        ES.SLUG = "ep27"
        ok("ep27 は EQ なし（compress と同じ）", np.array_equal(AM.voice_chain(x), AM.compress(x)))
        for s in ("ep28", "ep29"):
            ES.SLUG = s
            ok(f"{s} は EQ あり", not np.array_equal(AM.voice_chain(x), AM.compress(x)))
    finally:
        ES.SLUG = keep
    # 山の形（正弦波で測る）
    t = np.arange(AM.SR * 2) / AM.SR
    for f0, lo, hi in ((3000, -4.05, -3.95), (400, -0.1, 0.1), (100, -0.1, 0.1)):
        s = np.sin(2 * np.pi * f0 * t)
        y = AM.peaking(s, *AM.VOICE_EQ)
        g = 20 * np.log10(np.sqrt((y[4410:-4410] ** 2).mean()) / np.sqrt((s[4410:-4410] ** 2).mean()))
        ok(f"{f0}Hz の変化が {lo}〜{hi}dB", lo <= g <= hi, f"（実測 {g:+.3f}dB）")
    # ffmpeg の equalizer（A/B の B と同じ指定）と大きさの形が同じ
    af = "equalizer=f=3000:t=o:w=1:g=-4"
    y0 = ffmpeg_eq(x, af)
    y1 = AM.peaking(x, *AM.VOICE_EQ)
    for lo, hi in ((0, 500), (1000, 2000), (2000, 4000), (4000, 8000)):
        d = band_db(y1, lo, hi) - band_db(y0, lo, hi)
        ok(f"ffmpeg との差 {lo}〜{hi}Hz が 0.1dB 未満", abs(d) < 0.1, f"（{d:+.3f}dB）")
    # 陽性対照：違う山（−5dB・幅1.2）なら上の物差しで差が出る
    y2 = AM.peaking(x, 3000.0, 1.2, -5.0)
    d = band_db(y2, 2000, 4000) - band_db(y0, 2000, 4000)
    ok("陽性対照：別の山（−5dB・幅1.2）は 2〜4kHz で 0.5dB 以上違う", abs(d) >= 0.5, f"（{d:+.3f}dB）")
    if bad:
        raise SystemExit(f"🔴 selftest 不合格 {len(bad)}件: {bad}")
    print("selftest: 全部合格（audio/ には触っていない）")


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        main()
