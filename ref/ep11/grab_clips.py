#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""必要な帯だけを 720x480 の原版から抜く（全部は落とさない）。

🔴 C: の空きが 2.7GB しかないので、丸ごと落とす選択肢は無い。
   どちらの原版も Accept-Ranges: bytes なので区間だけ取れる。
   実測（2026-09-21 ⑤c）＝58秒＝27MB・23秒。**2.5倍速**で落ちる。

⚠️ `-c copy` で `.mpg` に書くと buffer underflow が大量に出るが、絵は正しい。
⚠️ 拡張子が違う＝NASA記録映画は `.mpg`／NARA/USIA 57分は `.mpeg`。
"""
import subprocess
import sys
import time
from pathlib import Path

DOC = "https://archive.org/download/ChallengerAccidentandInvestigation/Challenger_Disaster_and_Investigation.mpg"
USIA = "https://archive.org/download/gov.archives.arc.59811/gov.archives.arc.59811.mpeg"

OUT = Path("ref/ep11/vid/clips")

# (名前, 出どころ, 始まり秒, 長さ秒, 何に使うか)
BANDS = [
    ("crew",      DOC,   18,  86, "乗員のバス・射点の機体（1:34）・白い部屋の頭"),
    ("white",     DOC,  380,  92, "白い部屋＝乗り込み（長い連続ショットの中ほど）"),
    ("launch",    DOC,  598,  64, "点火・上昇（きれいな語りの版）"),
    ("accident",  DOC,  662, 106, "破壊・火球・SRBの飛行・落ちる残骸"),
    ("srb",       DOC,  993,  68, "🔴 輪切りの筒を貨車で運ぶ・吊る・積む・ETの到着"),
    ("rollout",   DOC, 1061,  46, "クローラ・射点へ運ぶ・空撮（焼き込み 163）"),
    # ice は先に抜いてある＝t_ice.mpg（1105 +58）
    ("pad",       DOC, 1144,  58, "機首 Challenger・射点の機体・作業"),
    ("smoke",     DOC, 1448,  24, "🔴🔴 黒い煙（24:15〜24:25 が本体）"),
    ("joint",     DOC, 1538,  88, "継ぎ目・Oリングの溝・金具の接写"),
    ("burn",      DOC, 2494, 132, "焼けた継ぎ目・黄色い丸（43:35 は穴を指す）"),
    ("commission", USIA, 55,  22, "🔴 公聴会の記録映像はここだけ（4ショット・約14秒）"),
]


def main():
    only = set(sys.argv[1:])
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for name, url, ss, dur, why in BANDS:
        if only and name not in only:
            continue
        ext = ".mpeg" if url is USIA else ".mpg"
        dst = OUT / f"{name}{ext}"
        if dst.exists() and dst.stat().st_size > 1_000_000:
            print(f"  = {name:11s} 既にある {dst.stat().st_size / 1e6:.0f}MB")
            total += dst.stat().st_size
            continue
        t0 = time.time()
        r = subprocess.run(
            ["ffmpeg", "-nostdin", "-v", "error", "-ss", str(ss), "-i", url,
             "-t", str(dur), "-c", "copy", "-y", str(dst)],
            capture_output=True, text=True)
        el = time.time() - t0
        sz = dst.stat().st_size if dst.exists() else 0
        total += sz
        ok = "✅" if (r.returncode == 0 and sz > 1_000_000) else "🔴"
        print(f"  {ok} {name:11s} {ss:5d}s +{dur:3d}s  {sz / 1e6:6.1f}MB  {el:5.1f}秒  {why}")
        if ok == "🔴":
            print(f"     stderr(末尾): {r.stderr[-300:]}")
    print(f"\n合計 {total / 1e6:.0f}MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
