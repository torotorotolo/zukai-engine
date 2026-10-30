# -*- coding: utf-8 -*-
"""27本目 ⑥：ゆっくり音声の音質を測る（記憶 feedback-jiko-yukkuri-audio-quality＝視聴者「耳が痛い」・28本目の ⑤a から直す）。

なぜ：推測を実測の口調で言わない。声の道すじ＝AquesTalk1（アプリの出力 8kHz）→ `aq_tts.to_sr`（×0.8・resample_poly で 24kHz）→
     audio/<cid>.wav → `audio_mix.read_wav`（**np.interp の直線補間**で 44.1kHz）→ compress（-24dBFS・3:1）→ BGM・リミッタ（天井 0.97）→
     -15.0 LUFS → AAC 192k モノラル。どの段で何が足されたかを、同じ物差しで測る。
測るもの（声の区間＝50ms の枠で実効値が -35dBFS より大きい所）：
  ① 帯域ごとの強さ（全体に対する dB）＝0〜0.5／0.5〜1／1〜2／2〜4／4〜8／8〜12／12〜16／16〜22kHz。耳に刺さりやすいのは 2〜5kHz
  ② 4kHz より上＝8kHz の合成には本来ない帯（あれば変換の鏡像か、割れの倍音）
  ③ 上限に届いた標本（wav＝|x|≥26000＝GAIN 0.8 の上限 26214 の近く・本編＝|x|≥0.96）
  ④ クレストファクタ（山÷実効値・dB）＝圧縮の強さ
  ⑤ 本編の 12〜22kHz の山が 24kHz の鏡像（直線補間の影）かを、24kHz−f と f の対応で見る

    python -P qa_out/ep27_r01_voiceq.py [<mp4>] [--ref=<比べる音のファイル>,…]   → qa_out/ep27_r01/voiceq.txt
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
BANDS = [(0, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 12000), (12000, 16000), (16000, 22050)]
NFFT = 4096


def decode(path, sr):
    """ffmpeg で f32 モノラルに（1本の配列＝声の帯の測りには十分小さい：15分で 164MB）"""
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype="<f4").astype(np.float64)


def voiced_psd(x, sr, gate_db=-35.0):
    """声の枠（50ms の実効値 > gate）の上で Hann 窓の FFT の平均の強さ。(周波数, 強さ, 声の秒)"""
    hop = int(sr * 0.05)
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-20)
    on = 20 * np.log10(rms) > gate_db
    win = np.hanning(NFFT)
    acc = np.zeros(NFFT // 2 + 1)
    k = 0
    for i in range(0, len(x) - NFFT, NFFT // 2):
        if not on[min(n - 1, (i + NFFT // 2) // hop)]:
            continue
        acc += np.abs(np.fft.rfft(x[i:i + NFFT] * win)) ** 2
        k += 1
    f = np.fft.rfftfreq(NFFT, 1 / sr)
    return f, acc / max(k, 1), on.sum() * 0.05


def bands(f, p):
    tot = p.sum()
    out = []
    for lo, hi in BANDS:
        m = (f >= lo) & (f < hi)
        out.append(10 * np.log10(p[m].sum() / tot + 1e-30) if m.any() else float("nan"))
    return out


def crest(x, sr, gate_db=-35.0):
    hop = int(sr * 0.05)
    n = len(x) // hop
    fr = x[: n * hop].reshape(n, hop)
    rms = np.sqrt(np.mean(fr ** 2, axis=1) + 1e-20)
    on = 20 * np.log10(rms) > gate_db
    v = fr[on].ravel()
    return 20 * np.log10(np.abs(v).max() / np.sqrt(np.mean(v ** 2))), 20 * np.log10(np.percentile(np.abs(v), 99.9) / np.sqrt(np.mean(v ** 2)))


def line(name, b, extra=""):
    return f"{name:<22}" + "".join(f"{v:7.1f}" for v in b) + f"  {extra}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mp4 = Path(args[0]) if args else HERE / "out" / "jiko" / "titan_audio-ep27-r01.mp4"
    refs = []
    for a in sys.argv[1:]:
        if a.startswith("--ref="):
            refs = [Path(r) for r in a.split("=", 1)[1].split(",") if r]
    lines = []
    head = f"{'':<22}" + "".join(f"{f'{lo//1000 if lo>=1000 else lo/1000:g}-{hi/1000:g}k':>7}" for lo, hi in BANDS)
    lines.append("■ ① 帯域ごとの強さ（声の区間・全体に対する dB）")
    lines.append(head)
    # 合成した声（audio/*.wav・24kHz）
    wavs = sorted((HERE / "audio").glob("c*.wav")) + sorted((HERE / "audio").glob("ed*.wav"))
    xs, near = [], 0
    for w in wavs:
        with wave.open(str(w)) as h:
            sr_w = h.getframerate()
            a = np.frombuffer(h.readframes(h.getnframes()), dtype="<i2").astype(np.float64)
        near += int((np.abs(a) >= 26000).sum())
        xs.append(a / 32768.0)
    xw = np.concatenate(xs)
    f, p, sec = voiced_psd(xw, sr_w)
    bw = bands(f, p)
    cw = crest(xw, sr_w)
    lines.append(line(f"合成の声 wav {sr_w // 1000}kHz", bw, f"声 {sec / 60:.1f}分"))
    # 本編
    x = decode(mp4, 44100)
    f2, p2, sec2 = voiced_psd(x, 44100)
    b2 = bands(f2, p2)
    c2 = crest(x, 44100)
    lines.append(line("本編 mp4 44.1kHz", b2, f"声 {sec2 / 60:.1f}分"))
    for r in refs:
        xr = decode(r, 44100)
        fr_, pr, sr_ = voiced_psd(xr, 44100)
        lines.append(line(f"比べる {r.stem[:14]}", bands(fr_, pr), f"声 {sr_ / 60:.1f}分・クレスト {crest(xr, 44100)[0]:.1f}dB"))
    lines.append("")
    lines.append("■ ③ 上限に届いた標本")
    lines.append(f"  合成の声 wav：|x|≥26000（GAIN 0.8 の上限 26214 の近く）＝{near} 標本（{len(wavs)} 本）")
    lines.append(f"  本編 mp4：|x|≥0.96＝{int((np.abs(x) >= 0.96).sum())} 標本・最大 {np.abs(x).max():.3f}")
    lines.append("■ ④ クレストファクタ（声の区間・山÷実効値）")
    lines.append(f"  合成の声 wav：最大 {cw[0]:.1f}dB・99.9% 点 {cw[1]:.1f}dB")
    lines.append(f"  本編 mp4    ：最大 {c2[0]:.1f}dB・99.9% 点 {c2[1]:.1f}dB")
    # ⑤ 鏡像：本編の 16〜22kHz の強さの形が、24kHz を軸に折り返した 2〜8kHz の形と似ているか
    def db(pp, ff, lo, hi):
        m = (ff >= lo) & (ff < hi)
        return 10 * np.log10(pp[m].mean() + 1e-30)
    lines.append("■ ⑤ 本編の高い帯（直線補間 24→44.1kHz の鏡像は 24kHz±f に出て 22.05kHz で折り返す）")
    for lo, hi in ((1000, 2000), (2000, 3000), (3000, 4000)):
        img_lo, img_hi = 24000 - hi, 24000 - lo                     # 24k−f（20〜23kHz）
        al_lo, al_hi = 44100 - (24000 + hi), 44100 - (24000 + lo)   # 24k+f が 44.1k で折り返す先（16〜19kHz）
        lines.append(f"  声 {lo/1000:g}〜{hi/1000:g}kHz {db(p2, f2, lo, hi):6.1f}dB → 24k−f（{img_lo/1000:.0f}〜{img_hi/1000:.0f}kHz）"
                     f"{db(p2, f2, img_lo, min(img_hi, 22050)):6.1f}dB・24k+f の折り返し（{al_lo/1000:.1f}〜{al_hi/1000:.1f}kHz）{db(p2, f2, al_lo, al_hi):6.1f}dB")
    lines.append(f"  比べ：本編の 8〜12kHz {db(p2, f2, 8000, 12000):6.1f}dB・12〜16kHz {db(p2, f2, 12000, 16000):6.1f}dB（BGM も入る）")
    out = HERE / "qa_out" / "ep27_r01" / "voiceq.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"→ {out}")


if __name__ == "__main__":
    main()
