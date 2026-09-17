# -*- coding: utf-8 -*-
"""9本目 ⑥ True peak の直し方を、**全長の音を手元で混ぜて**測り比べる（2026-09-17）。

なぜ：r03 は 0dBFS を超えた 0.1秒枠が 24個・最大 +1.0 dBFS（8本目 14・+0.6）。
      `audio_mix.limit()` は 1ms ブロックで利得を出し、立ち上がり 2ms で追いかけて、
      **追いつけなかった山を最後に `np.clip` で切り落とす**。切った波形は AAC にすると標本の間で山が立つ。
測るもの：`audio_mix.main(bgm="none")` → AAC 192k（本番の mux と同じ）→ ebur128 の FTPK（0.1秒枠の真のピーク）
      ＋ 切り落とした標本の数（天井に張り付いた標本）

    python qa_out/ep9_af_tp.py base la97 la89 la84

  base … いまの作り（CEILING 0.97・先読みなし）＝**陽性対照**（Modal の r03 と同じ 24枠・+1.0 が出なければ物差しが違う）
  laNN … 先読み 5ms ＋ CEILING 0.NN
⚠️ ローカルで回すのは**音の混ぜだけ**（映像は焼かない）。1通り 約3分・一時ファイル 約200MB（終わったら消す）
"""
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import audio_mix as A  # noqa: E402

ORIG_LIMIT = A.limit
LOOK = 5          # 先読み（ブロック＝1ms）


def limit_la(x, ceiling=None, atk=0.002, rel=0.05):
    """`audio_mix.limit` に**先読み**を足したもの（山の LOOK ms 前から利得を下げ始める）。"""
    ceiling = A.CEILING if ceiling is None else ceiling
    if A.peak_abs(x) <= ceiling:
        return x
    blk = max(1, int(0.001 * A.SR))
    k = len(x) // blk
    view = x[:k * blk].reshape(k, blk)
    lv = np.empty(k, dtype=np.float64)
    step = max(1, 4_000_000 // blk)
    for i in range(0, k, step):
        lv[i:i + step] = np.abs(view[i:i + step]).max(axis=1)
    need = np.minimum(1.0, ceiling / np.maximum(lv, 1e-12))
    pad = np.concatenate([need, np.ones(LOOK)])
    need = np.lib.stride_tricks.sliding_window_view(pad, LOOK + 1).min(axis=1)
    ka = 1 - np.exp(-blk / A.SR / max(atk, 1e-6))
    kr = 1 - np.exp(-blk / A.SR / max(rel, 1e-6))
    g = np.empty(k)
    cur = 1.0
    for i in range(k):
        tgt = need[i]
        cur += (tgt - cur) * (ka if tgt < cur else kr)
        g[i] = cur
    view *= g[:, None].astype(x.dtype)
    x[k * blk:] *= x.dtype.type(g[-1])
    np.clip(x, -ceiling, ceiling, out=x)
    return x


def ftpk(m4a):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-v", "verbose", "-i", str(m4a), "-vn",
                        "-af", "ebur128=framelog=verbose:peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    txt = r.stderr
    fr = re.findall(r"t:\s*([\d.]+)\s+TARGET:\S+ LUFS\s+M:\s*(?:-?[\d.]+|-inf).*?FTPK:\s*(-?[\d.]+|-inf)", txt)
    tail = txt[txt.rfind("Summary:"):]
    I = re.search(r"I:\s*(-?[\d.]+) LUFS", tail)
    PK = re.search(r"Peak:\s*(-?[\d.]+|-inf) dBFS", tail)
    if not fr or not I:
        raise SystemExit(f"🔴 ebur128 が読めない（fail closed）: {m4a}")
    pks = [float(p) for _, p in fr if p != "-inf"]
    return (len(fr), sum(p > 0.0 for p in pks), sum(p > -1.0 for p in pks),
            max(pks), float(I.group(1)), PK.group(1) if PK else "?")


def main():
    names = [a for a in sys.argv[1:] if not a.startswith("--")] or ["base"]
    out = ROOT / "out" / "jiko"
    for nm in names:
        m = re.fullmatch(r"la(\d+)(?:a(\d+))?", nm)
        A.LOOKAHEAD_MS = 0                  # ⚠️ 09-17 に本番の limit() が先読み 5ms を持った＝ここで外して「元の作り」を再現する
        if nm == "base":
            A.CEILING, A.limit = 0.97, ORIG_LIMIT
        elif m:
            atk = int(m.group(2)) / 1000.0 if m.group(2) else 0.002      # laNNaK＝立ち上がり K ms
            A.CEILING = int(m.group(1)) / 100.0
            A.limit = (lambda x, ceiling=None, _a=atk: limit_la(x, ceiling, atk=_a))
        else:
            raise SystemExit(f"🔴 知らない名前: {nm}")
        wav, m4a = out / f"tp_{nm}.wav", out / f"tp_{nm}.m4a"
        print(f"\n===== {nm}: CEILING {A.CEILING} ／ {'先読みなし' if A.limit is ORIG_LIMIT else '先読み ' + str(LOOK) + 'ms'}",
              flush=True)
        A.main(out_name=wav.name, bgm="none")
        with open(wav, "rb") as f:
            f.seek(44)
            a = np.frombuffer(f.read(), dtype="<i2")
        # ⚠️ 天井 0.97 は `* 32767` のあと int16 へ切り捨てで 31783＝round の 31784 に届かない
        #    （1回目は全部 0 と出た）→ 切り捨てた値から 1 段下までを「張り付いた」と数える
        cap = int(A.CEILING * 32767) - 1
        clipped = int(np.count_nonzero(np.abs(a.astype(np.int32)) >= cap))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "192k", str(m4a)],
                       check=True)
        n, over0, over1, mx, I, tp = ftpk(m4a)
        print(f"★ {nm}: 天井に張り付いた標本 {clipped:,} ／ 0.1秒枠 {n:,} のうち 0dBFS 超 {over0}・−1dBFS 超 {over1} "
              f"／ 枠の最大 {mx:+.1f} dBFS ／ 全体 {I:.1f} LUFS ／ True peak {tp} dBFS", flush=True)
        wav.unlink(missing_ok=True)
        m4a.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
