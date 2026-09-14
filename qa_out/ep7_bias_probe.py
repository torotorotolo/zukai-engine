# -*- coding: utf-8 -*-
"""ep7_bias_probe.py — 出典の帯の**下地の明るさ**を bias ごとに測る（2026-09-14 ⑤c'）。

■ なぜ要るか
    ⑤c-2 §E-5＝`c214` の出典は下地の中央値 **90.7**（c114 39.0／c809 46.0 の2倍以上）で、
    白いビルの外壁に重なって沈んでいた。直しは「寄せを変えて出典の下を暗い所にする」。
    ⚠️ **どの寄せが暗いかは当てずっぽうで決めない**（[[feedback-verify-the-ledgers-suggested-fix]]）。

■ 🔴 本番と同じ幾何で測る（[[feedback-gates-must-share-the-production-geometry]]）
    `scene_jiko.photo_box()` と `build_jiko.fit()` をそのまま呼ぶ。

■ 使い方
    python qa_out/ep7_bias_probe.py c214
    python qa_out/ep7_bias_probe.py --selftest
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import build_jiko as B                                          # noqa: E402
import cuts                                                     # noqa: E402
import scene_jiko as S                                          # noqa: E402

# 出典の帯（⑤c-2 で実測した画面座標）
CRED = (72, 838, 900, 880)


def band_median(cid, bias):
    spec = dict(cuts.SPEC[cid])
    spec["bias"] = bias
    box = S.photo_box(spec)
    with Image.open(HERE / "ref" / spec["photo"]) as im:
        src = im.convert("RGB")
        got = B.fit(src, box, bias=bias,
                    xbias=spec.get("xbias", 0.5), zoom=spec.get("zoom", 1.0))
    bx, by, _, _ = box
    x0, y0, x1, y1 = CRED
    # 箱の中の座標へ直す（箱の外に出る欄はここで落とす＝fail closed）
    cx0, cy0, cx1, cy1 = x0 - bx, y0 - by, x1 - bx, y1 - by
    if cx0 < 0 or cy0 < 0 or cx1 > got.width or cy1 > got.height:
        return None
    px = got.crop((cx0, cy0, cx1, cy1)).convert("L").getdata()
    return statistics.median(px)


def selftest():
    ok = True

    def chk(what, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  🔴 ") + what)
        ok = ok and bool(cond)

    # 陽性対照＝**値**で見る（件数でなく。[[feedback-verify-your-own-instrument]]）
    w, b = Image.new("RGB", (2400, 1600), (255, 255, 255)), Image.new("RGB", (2400, 1600), (0, 0, 0))
    box = (72, 210, 810, 648)
    mw = statistics.median(B.fit(w, box, bias=0.5).convert("L").getdata())
    mb = statistics.median(B.fit(b, box, bias=0.5).convert("L").getdata())
    chk(f"真っ白は 255（実測 {mw}）", mw == 255)
    chk(f"真っ黒は 0（実測 {mb}）", mb == 0)
    v = band_median("c214", 0.40)
    chk(f"c214 bias=0.40 が ⑤c-2 の実測 90.7 と合う（いま {v}）", v is not None and abs(v - 90.7) < 12)
    print("  " + ("✓ selftest 通過" if ok else "🔴 selftest 失敗"))
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    cid = sys.argv[1] if len(sys.argv) > 1 else "c214"
    print(f"■ {cid}  出典の帯 {CRED} の下地の中央値（低いほど字が読める）")
    best = None
    for i in range(5, 20):
        bias = i / 20
        v = band_median(cid, bias)
        mark = ""
        if v is not None and (best is None or v < best[1]):
            best, mark = (bias, v), ""
        print(f"   bias={bias:.2f}  中央値 {('---' if v is None else f'{v:6.1f}')}{mark}")
    if best:
        print(f"\n⭐ いちばん暗いのは bias={best[0]:.2f}（中央値 {best[1]:.1f}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
