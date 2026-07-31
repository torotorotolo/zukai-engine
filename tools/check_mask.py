# -*- coding: utf-8 -*-
"""★語尾が BGM に埋もれていないかを機械で測る（2026-07-31 追加）。

■ なぜ作ったか
  カズヤくんが冒頭の「10時47分」を「じゅうじ よんじゅうなな」と聞いた。
  ところが `kana_log.txt` は `ヨンジュウナナフン` で正しく、YOMI 辞書にも
  「10時47分→ジュウジヨンジュウナナフン」が既に入っていた。**読みは合っている。**

  `tools/check_mora.py` で実測したところ原因はこうだった：

  | 測ったもの（80〜400Hz・鼻音の帯） | 値 |
  |---|---|
  | 文末の「ン」（ナレーション単体）   | **−4.5 dB** |
  | ドローン（BGM 0.12）だけの無音区間 | **−6.0 dB** |
  | 直前の母音「ナ」                | **+14.0 dB** |

  → **語尾の「ン」は BGM のわずか 1.5dB 上**しかない（母音は 20dB 上）。
  日本語の「ン」は 80〜400Hz の鼻音 murmur にしか実体が無く、
  ドローンは 27.5／55／82.5／110／164.8Hz ＝ **まったく同じ帯**を鳴らしている。
  だから消えて聞こえる。**辞書を触ってはいけない事案だった。**

■ この検査が見るもの
  行ごとに「発話の最後の 0.18 秒」を切り出し、ドローンの寝床（bed）に対する
  余裕（margin, dB）を出す。⚠️ 帯域を分けて測る。全帯域で測ると母音の低音に
  引っ張られて、鼻音が埋もれていても通ってしまう。

    margin = 語尾のエネルギー(80-400Hz) − ドローンのエネルギー(80-400Hz)

■ 基準（実測から決めた）
  10 dB 以上 … 聞こえる
  6〜10 dB   … 弱い（BGMが膨らむ11秒周期の山と重なると消える）
  6 dB 未満  … **消える**（pr01 の「フン」は 1.5 dB だった）

使い方:
    python tools/check_mask.py             … 全カットを測って悪い順に出す
    python tools/check_mask.py --all       … 全行を出す
    python tools/check_mask.py --cut=pr01  … 1カットだけ詳しく
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
AUD = HERE / "audio"
BAND = (80, 400)          # 鼻音「ン」「ム」が鳴る帯（ドローンと正面衝突する）
TAIL = 0.30               # 語尾として見る秒（最後のモーラ1つが入る長さ）
OK, WEAK = 10.0, 6.0      # 余裕の基準（dB）


def read(path):
    with wave.open(str(path)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(axis=1)
    return x.astype(np.float64) / 32768.0, sr


def bandpass(x, sr, f0=BAND[0], f1=BAND[1]):
    """80〜400Hz だけ残す。周波数領域で切って戻すだけ（scipy を入れずに済ませる）。"""
    n = 1 << (len(x) - 1).bit_length()
    X = np.fft.rfft(x, n)
    fr = np.fft.rfftfreq(n, 1 / sr)
    X[(fr < f0) | (fr >= f1)] = 0
    return np.fft.irfft(X, n)[:len(x)]


def envelope(x, sr, win=0.025, hop=0.010):
    """25ms 窓の RMS（dB）を 10ms ごとに。**dBFS なので窓長で値が動かない。**

    🔴 前の版は |rfft|² を len で割っていたので、**窓を長くすると値が上がった**
       （1.0秒窓と0.3秒窓で 5dB ずれた）。パーセバルの関係は
       Σ|x|² = Σ|X|²/N なので、平均パワーにするには **N² で割る**のが正しい。
       時間領域の RMS で測れば、その間違いは起こらない。
    """
    nw, nh = int(win * sr), int(hop * sr)
    k = max(0, (len(x) - nw) // nh + 1)
    if k < 1:
        return np.zeros(0), np.zeros(0)
    idx = np.arange(k) * nh
    seg = np.stack([x[i:i + nw] for i in idx])
    return idx / sr, 20 * np.log10(np.sqrt((seg ** 2).mean(axis=1)) + 1e-12)


def bed_db(mixmod=None):
    """ドローンの寝床（80〜400Hz）。**いちばん膨らむ瞬間**で測る。

    ドローンは 11 秒周期で 0.62〜1.00 に膨らむ。いちばん大きいところで
    聞こえるかどうかが決め手なので、山（t=5.5秒あたり）で測る。
    """
    A = mixmod or __import__("audio_mix")
    d = A.drone(A.SR * 12) * A.V_BGM
    # サイドチェインで下がった状態を見る。**語尾が聞こえるかを決めるのは
    # 話しているあいだの寝床**であって、無音での寝床ではない。
    d = d * 10 ** (-getattr(A, "DUCK_DB", 0.0) / 20)
    _, e = envelope(bandpass(d[int(4.5 * A.SR):int(6.5 * A.SR)], A.SR), A.SR)
    return float(np.percentile(e, 90))


def speech_end(x, sr, a, b, floor=-46.0):
    """区間 [a,b] のうち、実際に音が鳴っている最後の時刻。"""
    seg = x[int(a * sr):int(b * sr)]
    if not len(seg):
        return None
    n = int(0.010 * sr)
    k = len(seg) // n
    if k < 2:
        return None
    e = 20 * np.log10(np.sqrt((seg[:k * n].reshape(k, n) ** 2).mean(axis=1)) + 1e-12)
    on = np.where(e > floor)[0]
    return None if not len(on) else a + (on[-1] + 1) * n / sr


def rows():
    d = json.loads((AUD / "narration.json").read_text(encoding="utf-8"))
    return d["subtitles"], d["durations"]


def scan(only=None, mixmod=None):
    """行ごとに『語尾のモーラのピーク − ドローン』を返す。

    ⚠️ 語尾は**平均でなくピーク**で測る。最後の 0.18 秒には必ず減衰が入るので、
       平均で測ると「全行が埋もれている」という無意味な結果になる（実際に出した）。
       聞こえるかどうかを決めるのは**最後のモーラの山**の高さ。
    """
    subs, _ = rows()
    bed = bed_db(mixmod)
    out = []
    for cid, rs in subs.items():
        if only and cid != only:
            continue
        p = AUD / f"{cid}.wav"
        if not p.exists():
            continue
        x, sr = read(p)
        bp = bandpass(x, sr)
        t, e = envelope(bp, sr)
        for r in rs:
            a, b = r["t"], r["t"] + r["d"]
            end = speech_end(x, sr, a, min(b + 0.15, len(x) / sr))
            if end is None:
                continue
            sel = e[(t >= max(a, end - TAIL)) & (t <= end)]
            if not len(sel):
                continue
            out.append((float(sel.max()) - bed, cid, r["text"], end))
    return sorted(out), bed


def main():
    only = next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--cut=")), None)
    res, bed = scan(only)
    if not res:
        print("🔴 測れる行が無い（audio/*.wav と narration.json を確認）")
        return 1
    dead = [r for r in res if r[0] < WEAK]
    weak = [r for r in res if WEAK <= r[0] < OK]
    print(f"ドローンの寝床（80〜400Hz・いちばん膨らむ瞬間）= {bed:.1f} dB")
    print(f"行 {len(res)} ／ 🔴消える(<{WEAK}dB) {len(dead)} ／ "
          f"⚠️弱い({WEAK}〜{OK}dB) {len(weak)} ／ ✓聞こえる {len(res) - len(dead) - len(weak)}")
    print(f"中央値 {np.median([r[0] for r in res]):.1f} dB")
    show = res if ("--all" in sys.argv or only) else res[:30]
    print(f"\n{'余裕dB':>7}  {'カット':<8}語尾（発話の最後 0.18 秒）")
    for m, cid, text, e in show:
        mark = "🔴" if m < WEAK else ("⚠️" if m < OK else "  ")
        print(f"{m:7.1f} {mark}{cid:<8}…{text[-24:]}")
    if len(show) < len(res):
        print(f"（悪い順に {len(show)} 行だけ表示。全部見るなら --all）")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
