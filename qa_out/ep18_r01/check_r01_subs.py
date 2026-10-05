# -*- coding: utf-8 -*-
"""18本目 r01 の字幕を全603行、正解の絵と比べる（2026-10-05 ⑥・14本目 `qa_out/ep14_r02/check_r02_subs.py` を写した）。

なぜ：★全体の指紋が検品の焼き（Actions `37269429916`・bf89fcfe…）と本番 r01（Modal・7cbfc052…）で合わなかった
     （同じ版 f8f92f2・層 1,327 枚・代表 28 層は一致）。検品の静止画 243 枚と本番のコマの照合（`qa_out/ep18_r01_vs_qa.py`）では
     242 カットが圧縮の揺れの内・**c809 だけ検品の静止画の字幕が1行目しか写っていなかった（本番は2行＝文の全部）**
     ＝違いは字幕の層にある疑い → ルール 6-62①：字幕の全行を本番と同じ関数で焼いた正解と比べる。
正解の絵＝本番と同じ関数（sub_strip → J.remap → page(css=sub_css) → render.png）で字幕の層を焼く（scratchpad に）。
r01 の側＝各行の表示の真ん中（カットの頭＋扉の秒＋LEAD＋t＋d/2）のコマの帯（y900〜1080）。
画面に出さない行（SUB_MUTE）は「帯に字が無い」ことを確かめる。
使い方: python qa_out/ep18_r01/check_r01_subs.py [--render]   （--render で正解の絵を焼き直す）
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
# 正解の絵（243枚）はリポに入れない＝scratchpad（このチャットの一時置き場）
REF = Path(r"C:/Users/konar/AppData/Local/Temp/claude/C--Users-konar-Documents-Obsidian-Vault/"
           r"c14422b0-06d2-4ae4-ad0c-eb32aac5b9d9/scratchpad/r01ref")
REF.mkdir(exist_ok=True)
MP4 = str(REPO / "out" / "jiko" / "titan_audio-ep18-r01.mp4")

S.build_layers()                       # SUB_MUTE（決め所と同じ行の字幕を消す）を埋める
starts = {}
for line in (REPO / "qa_out" / "ep18_af_timeline.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    c, _, st, sec, *_ = line.split("\t")
    starts[c] = float(st)

if "--render" in sys.argv or not any(REF.glob("sub_*.png")):
    def one(cid):
        rows = S.SUBS[cid]
        h = S.SUB_H * len(rows)
        html = S.page(J.remap(S.sub_strip(rows), S.pal_of_layer(f"sub_{cid}")), S.W, h, css=S.sub_css())
        render.png(html, REF / f"sub_{cid}.png", S.W, h)
    with ThreadPoolExecutor(max_workers=2) as ex:     # ⚠️ 手元の Chrome は並べすぎると黙って固まる（ルール 6-4）
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
    print(f"  {o[0]}-{o[1]} {o[2]:8.2f}s 平均 {o[3]:5.2f}・差>64 {o[4]:5.2f}%・明るい画素 r01 {o[5]}／正解 {o[6]}"
          f"{'・出さない行' if o[7] else ''}・{'れいむ' if o[8] == 'q' else 'まりさ'}「{o[9][:20]}」")
(SP / "r01_subs.tsv").write_text("\n".join("\t".join(map(str, o)) for o in out), encoding="utf-8")
