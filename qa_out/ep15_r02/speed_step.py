# -*- coding: utf-8 -*-
"""話速の段を確かめる：数行を話速ごとに合成し、アプリの出力（キャッシュの wav）の md5 と長さを比べる。audio/*.wav は触らない。
   使い方: python speed_step.py 153,150,149,148,147,146,145"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(ROOT / "tools"))
import aq_build as B      # noqa: E402
import aq_tts as T        # noqa: E402
import el_script as ES    # noqa: E402
import narration          # noqa: E402
import speaker            # noqa: E402

assert ES.SLUG == "ep15", ES.SLUG
speeds = [int(x) for x in sys.argv[1].split(",")]
yomi = B.yomi_table()
# 語り3行・聞き役3行（章の違うところから）
want_n, want_q = [], []
for cid, lines in narration.SCRIPT:
    for i, x in enumerate(lines, 1):
        who, _ = speaker.split(x)
        lid = f"{cid}-{i}"
        if who and len(want_q) < 3 and cid[:2] in ("c1", "c4", "c8"):
            if not any(l.startswith(cid[:2]) for l in want_q):
                want_q.append(lid)
        if not who and len(want_n) < 3 and cid[:2] in ("c1", "c5", "c9"):
            if not any(l.startswith(cid[:2]) for l in want_n):
                want_n.append(lid)
lids = want_n + want_q
who_of = {}
for cid, lines in narration.SCRIPT:
    for i, x in enumerate(lines, 1):
        who_of[f"{cid}-{i}"] = speaker.split(x)[0]
print("行:", lids)
res = {}
for sp in speeds:
    defs = B.voice_defs(speed=sp)
    presets = B.setup(defs)
    row = []
    for lid in lids:
        pr = presets[who_of[lid]]
        T.synth(yomi[lid], pr, lid)
        key = T.cache_key(T.sent_text(yomi[lid]), T.preset_row(pr))
        p = T.CACHE / ES.SLUG / f"{key}.wav"
        x, fs = T.read_wav(p)
        row.append((hashlib.md5(x.tobytes()).hexdigest()[:8], len(x) / fs))
    res[sp] = row
    tot = sum(s for _, s in row)
    print(f"話速 {sp}: " + " ".join(f"{h}/{s:.3f}" for h, s in row) + f"  合計 {tot:.3f}秒")
base = res[speeds[0]]
print()
for sp in speeds[1:]:
    same = sum(a[0] == b[0] for a, b in zip(res[sp], base))
    r = sum(s for _, s in res[sp]) / sum(s for _, s in base)
    print(f"話速 {sp} と {speeds[0]}: md5 一致 {same}/{len(lids)}・長さの比 {r:.4f}")
print("stats", T.stats())
