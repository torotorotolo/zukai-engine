# -*- coding: utf-8 -*-
"""ep7_c716_probe.py — c716 の「End of Recording」が**何秒から**始まるかを実測する（2026-09-14 ⑤c'）。

■ なぜ要るか
    ⑤c-2 §B＝`c716` は 10秒まるごと終幕カード「End of Recording」だけだった
    （額の中の平均 42.3・明るい画素 4.0%）。
    ⚠️ 1通目の当たり「s1（12〜30秒）へ振り替える」は**誤り**。s1 はほぼ一色の黄色
    （ばらつき 8.9）で、使うと `c417` と同じ粗になる。
    → **30〜42秒を 0.5秒刻みで当たって、カードの始まりを実測してから秒を決める。**

■ 🔴 守っていること
    本番と同じ経路で1コマだけ抜く（`footage.urls_of` ＋ ffmpeg）。
    判定は**値**で見る（[[feedback-verify-your-own-instrument]]）＝
    「明るさの平均」と「ばらつき」。陽性対照＝真っ黒と真っ白を同じ関数に通す。

■ 使い方
    python qa_out/ep7_c716_probe.py
    python qa_out/ep7_c716_probe.py --selftest
"""
from __future__ import annotations

import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import footage as FO                                            # noqa: E402

CLIP = "1-AWA-714-Pentagon_more2.mp4"


def stats(im: Image.Image):
    px = list(im.convert("L").getdata())
    return statistics.mean(px), statistics.pstdev(px), 100.0 * sum(1 for v in px if v > 160) / len(px)


def frame_at(t: float, out: Path):
    last = None
    for url in FO.urls_of(CLIP):
        cmd = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
               "-user_agent", FO.UA, "-ss", f"{t:.2f}", "-i", url,
               "-an", "-frames:v", "1", "-q:v", "3", str(out)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if r.returncode == 0 and out.exists() and out.stat().st_size > 0:
            return True
        last = (r.returncode, (r.stderr or "")[:200])
    print(f"  🔴 {t:.1f}s のコマが取れない: {last}")
    return False


def selftest():
    ok = True

    def chk(what, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  🔴 ") + what)
        ok = ok and bool(cond)

    a = stats(Image.new("RGB", (64, 64), (0, 0, 0)))
    b = stats(Image.new("RGB", (64, 64), (255, 255, 255)))
    chk(f"真っ黒＝平均0・ばらつき0・明るい画素0%（実測 {a[0]:.1f}/{a[1]:.1f}/{a[2]:.1f}）",
        a == (0.0, 0.0, 0.0))
    chk(f"真っ白＝平均255・ばらつき0・明るい画素100%（実測 {b[0]:.1f}/{b[1]:.1f}/{b[2]:.1f}）",
        b[0] == 255.0 and b[1] == 0.0 and b[2] == 100.0)
    half = Image.new("RGB", (64, 64), (0, 0, 0))
    half.paste(Image.new("RGB", (64, 32), (255, 255, 255)), (0, 0))
    h = stats(half)
    chk(f"半分ずつ＝平均127.5・明るい画素50%（実測 {h[0]:.1f}/{h[2]:.1f}）",
        abs(h[0] - 127.5) < 0.6 and abs(h[2] - 50.0) < 0.6)
    chk("クリップの URL が引ける", bool(FO.urls_of(CLIP)))
    print("  " + ("✓ selftest 通過" if ok else "🔴 selftest 失敗"))
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    print(f"■ {CLIP}  30.0〜42.0秒を 0.5秒刻み（平均／ばらつき／明るい画素%）")
    tmp = Path(tempfile.mkdtemp(prefix="c716_"))
    rows = []
    t = 30.0
    while t <= 42.01:
        p = tmp / f"{t:.1f}.jpg"
        if frame_at(t, p):
            with Image.open(p) as im:
                m, sd, br = stats(im)
            rows.append((t, m, sd, br))
            # カードは「暗くて平ら」。絵は「明るいかばらつく」
            tag = "🔴 カードらしい" if (m < 70 and sd < 40) else "・絵がある"
            print(f"   {t:5.1f}s  平均 {m:6.1f}  ばらつき {sd:5.1f}  明るい {br:5.1f}%   {tag}")
        t += 0.5
    card = [r for r in rows if r[1] < 70 and r[2] < 40]
    pic = [r for r in rows if not (r[1] < 70 and r[2] < 40)]
    if card:
        print(f"\n⭐ カードらしいコマ＝{card[0][0]:.1f}s 以降（いちばん早いもの）")
    if pic:
        print(f"⭐ 絵があるコマ＝{pic[0][0]:.1f}s 〜 {pic[-1][0]:.1f}s（{len(pic)}コマ）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
