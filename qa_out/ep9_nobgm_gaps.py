# -*- coding: utf-8 -*-
"""BGMなしで焼いた音の「語りの無い区間」が本当に無音かを測る（9本目⑥・2026-09-17）。

なぜ：`audio_mix.py --bgm=none` はログに「BGM＝なし」と出すが、それは自己申告。
      焼き上がった音そのもので、**声の鳴っていない区間に何も鳴っていない**ことを数字で見る。

区間の決め方＝`audio_mix.main` と同じ積み方。
  カットの声は [カットの頭 + LEAD, カットの頭 + LEAD + audio/<cid>.wav の長さ] に乗る。
  それ以外（カットの頭の LEAD・声の尻からカットの終わりまで）が「語りの無い区間」。
  ⚠️ AAC は音の縁を数ミリ秒にじませ、頭に数十ミリ秒のずれも持ちうるので、
     声の区間の両側に MARGIN 秒の余白を取る（ずれそのものは「声の立ち上がり」で実測して出す）。

使い方：
  python qa_out/ep9_nobgm_gaps.py <wav か mp4> [--head=秒]
陽性対照：
  `python tools/audio_mix.py --head=40 --bgm=drone --out=ep9_head_drone.wav` の wav を当てて
  「鳴っている」と出なければ、この物差しは壊れている。
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

SR = 44100
MARGIN = 0.05          # 声の区間の両側の余白（秒）
SILENT_DB = -60.0      # 語りの無い区間の最大がこれ以下なら「無音」


def load(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
                        "-ar", str(SR), "-f", "s16le", "-"], capture_output=True)
    if r.returncode or not r.stdout:
        raise SystemExit(f"🔴 音を読めない: {path}（fail closed）")
    return np.frombuffer(r.stdout, dtype="<i2")


def db(x):
    return 20 * np.log10(max(float(x), 1e-12))


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        raise SystemExit(__doc__)
    head = next((float(a.split("=")[1]) for a in sys.argv[1:] if a.startswith("--head=")), None)
    a = load(files[0])
    n = len(a)

    spans, t = [], 0.0
    for cid, sec in S.CUTS:
        p = HERE / "audio" / f"{cid}.wav"
        if not p.exists():
            raise SystemExit(f"🔴 {p} が無い＝声の区間が決められない（fail closed）")
        with wave.open(str(p)) as w:
            d = w.getnframes() / w.getframerate()
        spans.append((cid, t, t + S.LEAD, t + S.LEAD + d, t + sec))
        t += sec
        if head and t >= head:
            break
    end = min(n / SR, t)
    if n / SR < t - 0.5:
        print(f"⚠️ 音の長さ {n / SR:.2f}秒 がカットの和 {t:.2f}秒 より短い")

    voice = np.zeros(n, bool)
    for cid, t0, v0, v1, t1 in spans:
        voice[int(max(0.0, v0 - MARGIN) * SR):int(min(end, v1 + MARGIN) * SR)] = True
    gap = ~voice
    gap[int(end * SR):] = False     # カットの和の外（audio_mix の +1秒）は測らない

    # 声の立ち上がりのずれ（最初に -40dBFS を超えた位置 と 1カット目の声の頭）
    loud = np.flatnonzero(np.abs(a[:int(min(end, 30) * SR)]) > 328)
    if len(loud):
        print(f"声の立ち上がり：実測 {loud[0] / SR:.3f}秒 ／ 積み方 {spans[0][2]:.3f}秒 "
              f"（ずれ {1000 * (loud[0] / SR - spans[0][2]):+.0f}ms・余白 {1000 * MARGIN:.0f}ms）")

    rows = []
    for cid, t0, v0, v1, t1 in spans:
        i, j = int(t0 * SR), int(min(end, t1) * SR)
        g = a[i:j][gap[i:j]].astype(np.float64) / 32768.0
        if len(g) == 0:
            continue
        pk = np.abs(g).max()
        rows.append((db(pk), db(np.sqrt((g ** 2).mean())), len(g) / SR, cid, t0))

    allg = a[gap].astype(np.float64) / 32768.0
    allv = a[voice & (np.arange(n) < int(end * SR))].astype(np.float64) / 32768.0
    gpk, grms = db(np.abs(allg).max()), db(np.sqrt((allg ** 2).mean()))
    vrms = db(np.sqrt((allv ** 2).mean()))
    nz = int(np.count_nonzero(allg))
    print(f"対象 {len(spans)}カット・{end:.2f}秒 ／ 語りの無い区間 {len(allg) / SR:.2f}秒"
          f"（うち 0 でない標本 {nz:,}／{len(allg):,}）")
    print(f"  語りの無い区間：最大 {gpk:.1f} dBFS ／ 実効 {grms:.1f} dBFS")
    print(f"  声の区間      ：実効 {vrms:.1f} dBFS（くらべる目安）")
    rows.sort(reverse=True)
    print("  最大の大きい順 5カット：")
    for pk, rms, sec, cid, t0 in rows[:5]:
        print(f"    {cid:6s} {int(t0 // 60):2d}:{t0 % 60:05.2f}  最大 {pk:6.1f} ／ 実効 {rms:6.1f} dBFS"
              f"（区間 {sec:.2f}秒）")
    ok = gpk <= SILENT_DB
    print(("✓ 無音" if ok else "🔴 鳴っている") +
          f"（語りの無い区間の最大 {gpk:.1f} dBFS ／ 基準 {SILENT_DB:.0f} dBFS 以下）")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
