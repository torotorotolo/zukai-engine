# -*- coding: utf-8 -*-
"""27本目 ⑥'：声の 2〜4kHz の強さが、声の道すじのどの段で決まるかを切り分ける（焼き直さない・読むだけ）。

なぜ：⑥'（10-30）競合3本（ゆっくり事故検証・ゆっくり暗闇の事件簿・おしえて!オカルト先生）と同じ物差しで比べると、
     うちの本編は 2〜4kHz（全体に対する dB）だけが 3.4〜4.2dB 強い（ほかの帯は ±0.5dB）。
     その強さが ①合成の声そのものか ②混ぜる段（`audio_mix.compress`）で足されたものかを、本編と同じ関数で測る。
物差し＝`qa_out/ep27_r01_voiceq.py` の voiced_psd・bands（声の区間＝50ms の実効値が -35dBFS より大きい所・Hann 4096）。

    python -P qa_out/ep27_r02_voicechain.py      → qa_out/ep27_r02/voicechain.txt
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.path.insert(0, str(HERE / "qa_out"))
sys.stdout.reconfigure(encoding="utf-8")
import audio_mix as AM            # noqa: E402
import ep27_r01_voiceq as V       # noqa: E402
import narration as N             # noqa: E402


def row(name, x, sr=AM.SR):
    f, p, sec = V.voiced_psd(x, sr)
    m = f < 22050
    b = V.bands(f[m], p[m])
    c = V.crest(x, sr)
    return f"{name:<28}" + "".join(f"{v:7.1f}" for v in b[:6]) + f"   クレスト {c[0]:.1f}dB・声 {sec / 60:.1f}分"


def main():
    cids = [c for c, _ in N.SCRIPT]
    x = np.concatenate([AM.read_wav(HERE / "audio" / f"{c}.wav") for c in cids])   # 本編と同じ：24kHz → 44.1kHz（np.interp）
    head = f"{'':<28}" + "".join(f"{s:>7}" for s in ("0-0.5k", "0.5-1k", "1-2k", "2-4k", "4-8k", "8-12k"))
    lines = ["■ 声の道すじの段ごとの帯域（声の区間・全体に対する dB）＝本編の関数（audio_mix.read_wav・compress）", head,
             row("① 合成の声（read_wav 44.1k）", x),
             row("② ①を compress（本編の値）", AM.compress(x))]
    out = HERE / "qa_out" / "ep27_r02" / "voicechain.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"→ {out}")


if __name__ == "__main__":
    main()
