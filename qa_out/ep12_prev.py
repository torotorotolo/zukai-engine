# -*- coding: utf-8 -*-
"""12本目 ⑤b-4（2026-09-23）：試し焼き。カットの層だけ焼いて、指定の時刻の1コマを**本番と同じ compose()** で合成する。

なぜ要るか：机上の門番（check_layout ほか）は**動く部品（drift の線・降る灰・光）と札の重なり**を見ない
（⑤b-3・⑤b-4 の試し焼きで「線が島の名札を貫く」「降る灰の柱が札を貫く」を見つけた）。

使い方:
    python qa_out/ep12_prev.py c605,c611 [0.95] [名前]
    → out/jiko/prev/<名前>.jpg（2コマを縦に並べた1枚。各コマは本体の帯 y 60〜1000 を切り出し）
⚠️ 手元の Chrome は1本ずつ（`render_all(jobs_workers=1)`）。門番と同時に回さない。重い処理の前にコミットの空きを測る。
⚠️ 検品（⑤c）の代わりではない。見るのは「線と札の重なり」「切り口」だけ。
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.chdir(REPO)
sys.path.insert(0, str(REPO / "tools"))
import scene_jiko as S          # noqa: E402
import build_jiko as B          # noqa: E402
from PIL import Image           # noqa: E402

cids = sys.argv[1].split(",")
frac = float(sys.argv[2]) if len(sys.argv) > 2 else 0.95
name = sys.argv[3] if len(sys.argv) > 3 else "prev_" + "_".join(cids)
for c in cids:
    S.render_all(only=c, jobs_workers=1)
idx, _ = S.layer_index(allow_missing=True)
meta = B.meta_of(idx)
lay = B._load_layers(cids, idx)
subs = {c: B.L(f"sub_{c}") for c in cids if (B.OUT / f"sub_{c}.png").exists()}
band = B.load_band()
photos = {c: B.load_photo(S.PHOTO_CUTS[c][1], S.PHOTO_CUTS[c][0],
                          S.PHOTO_TRIM.get(c), S.PHOTO_LEVELS.get(c))
          for c in cids if idx[c]["photo"]}
secs = dict(S.CUTS)
frames = []
for c in cids:
    sec = secs[c]
    off = S.card_of(c)
    t = off + (sec - off) * frac
    im = B.compose(c, t, sec, lay, photos, meta, subs, band).convert("RGB")
    frames.append(im.crop((0, 60, 1920, 1000)))
    print(f"{c}: {sec:.2f}秒のうち {t:.2f}秒", flush=True)
out = Image.new("RGB", (1920, 940 * len(frames) + 8 * (len(frames) - 1)), (255, 0, 255))
for i, f in enumerate(frames):
    out.paste(f, (0, i * 948))
dst = REPO / "out" / "jiko" / "prev" / f"{name}.jpg"
dst.parent.mkdir(parents=True, exist_ok=True)
out.save(dst, quality=90)
print(dst)
