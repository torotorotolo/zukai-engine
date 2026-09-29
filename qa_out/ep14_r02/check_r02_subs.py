# -*- coding: utf-8 -*-
"""r02 の字幕を全442行、正解の絵と比べる（14本目 ⑥-2・★指紋が kei1 と合わなかったので本番の mp4 を直接測る）。

正解の絵＝本番と同じ関数（sub_strip → J.remap → page(css=sub_css) → render.png）で字幕の層を焼く（scratchpad に）。
r02 の側＝各行の表示の真ん中（カットの頭＋扉の秒＋LEAD＋t＋d/2）のコマの帯（y900〜1080）。
画面に出さない行（SUB_MUTE）は「帯に字が無い」ことを確かめる。
使い方: python check_r02_subs.py [--render]   （--render で正解の絵を焼き直す）
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(REPO / "tools"))
import jiko_style as J        # noqa: E402
import render                 # noqa: E402
import scene_jiko as S        # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(__file__).resolve().parent
REF = SP / "r02ref"
REF.mkdir(exist_ok=True)
MP4 = str(REPO / "out" / "jiko" / "titan_audio-ep14-r02.mp4")

S.build_layers()                       # SUB_MUTE（決め所と同じ行の字幕を消す）を埋める
starts = {}
for line in (REPO / "qa_out" / "ep14_af_timeline.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    c, _, st, sec, *_ = line.split("\t")
    starts[c] = float(st)

if "--render" in sys.argv or not any(REF.glob("sub_*.png")):
    def one(cid):
        rows = S.SUBS[cid]
        h = S.SUB_H * len(rows)
        html = S.page(J.remap(S.sub_strip(rows), S.pal_of_layer(f"sub_{cid}")), S.W, h, css=S.sub_css())
        render.png(html, REF / f"sub_{cid}.png", S.W, h)
    with ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(one, list(S.SUBS)))
    print(f"正解の絵 {len(list(REF.glob('sub_*.png')))}枚")


def band_at(t):
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", MP4,
                          "-frames:v", "1", "-vf", "crop=1920:180:0:900", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(180, 1920, 3).astype(np.int16)


out = []
for cid, rows in S.SUBS.items():
    strip = Image.open(REF / f"sub_{cid}.png").convert("RGBA")
    off = S.card_of(cid)
    mute = S.SUB_MUTE.get(cid, set())
    for i, r in enumerate(rows):
        T = starts[cid] + off + S.LEAD + r["t"] + r["d"] / 2
        v = band_at(T)
        if i in mute:
            want = np.zeros((180, 1920, 3), np.int16)
        else:
            row = strip.crop((0, i * S.SUB_H, S.W, (i + 1) * S.SUB_H))
            bg = Image.new("RGBA", row.size, (0, 0, 0, 255))
            want = np.asarray(Image.alpha_composite(bg, row).convert("RGB")).astype(np.int16)
        d = np.abs(v - want).max(axis=2)
        lit_v = int((v.max(axis=2) > 80).sum())
        lit_w = int((want.max(axis=2) > 80).sum())
        out.append((cid, i + 1, T, float(d.mean()), float((d > 64).mean() * 100), lit_v, lit_w,
                    i in mute, r.get("who"), r["text"]))

pct = sorted(o[4] for o in out)
print(f"行 {len(out)}（画面に出さない行 {sum(o[7] for o in out)}）")
print(f"差>64 の画素の割合：中央 {pct[len(pct) // 2]:.2f}%・90% 点 {pct[int(len(pct) * 0.9)]:.2f}%・最大 {pct[-1]:.2f}%")
bad = [o for o in out if o[4] > 1.0 or (o[6] and abs(o[5] - o[6]) > 0.15 * o[6]) or (not o[6] and o[5] > 200)]
print(f"疑い（差>64 が 1% 超・明るい画素の数が 15% 以上ずれる・出さない行に字）＝{len(bad)}行")
for o in sorted(bad, key=lambda o: -o[4])[:40]:
    print(f"  {o[0]}-{o[1]} {o[2]:8.2f}s 平均 {o[3]:5.2f}・差>64 {o[4]:5.2f}%・明るい画素 r02 {o[5]}／正解 {o[6]}"
          f"{'・出さない行' if o[7] else ''}・{'れいむ' if o[8] == 'q' else 'まりさ'}「{o[9][:20]}」")
(SP / "r02_subs.tsv").write_text("\n".join("\t".join(map(str, o)) for o in out), encoding="utf-8")
