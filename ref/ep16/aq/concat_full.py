# -*- coding: utf-8 -*-
"""concat_full.py — 尺の3つ目の測り方（ルール 5a-32）：出荷する audio/<cid>.wav を本編と同じ並び
（章の扉・LEAD・声・TAIL・決め所の余白）でつないだ wav を書く（16本目 ⑤a-2・2026-10-01）。測るだけ・送らない。

  python ref/ep16/aq/concat_full.py <リポ> <出力.wav>   → ffprobe -v error -show_entries format=duration <出力.wav>

声の部分は narration.json の秒でなく wav の標本数そのもの＝aq_build --rate・check_script ③ とは別の道で長さが決まる。
⚠️ `aq_build --listen all` はキャッシュから組み直す＝出荷する wav を測っていない（別の道にならない）。
16本目の実測＝2,288.471秒（aq_build --rate 38分08.5秒・check_script ③ 38分08秒）・wav と narration.json の秒の差 0.6ms 超は0。
出力は約110MB（38分）＝scratchpad に書いて、測ったら消す。"""
import json
import sys
import wave
from pathlib import Path

repo = Path(sys.argv[1])
out = Path(sys.argv[2])
sys.path.insert(0, str(repo / "tools"))
import aq_build as B          # noqa: E402
import check_script as CSC    # noqa: E402
import narration              # noqa: E402

SR = B.SR
quotes = B.quotes_and_md()
js = json.loads((repo / "audio" / "narration.json").read_text(encoding="utf-8"))
sil = lambda s: b"\x00\x00" * int(round(s * SR))
n_samples, prev, mism = 0, None, []
with wave.open(str(out), "w") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    for cid, _ in narration.SCRIPT:
        key = cid[:2] if CSC.CHAPTER_CUT_RE.match(cid) else None
        if key is not None:
            if prev is not None and key != prev:
                b = sil(CSC.CARD_SEC)
                w.writeframes(b)
                n_samples += len(b) // 2
            prev = key
        with wave.open(str(repo / "audio" / f"{cid}.wav")) as r:
            assert (r.getframerate(), r.getnchannels(), r.getsampwidth()) == (SR, 1, 2), cid
            pcm = r.readframes(r.getnframes())
        sec = len(pcm) / 2 / SR
        if abs(sec - js["durations"][cid]) > 0.0006:
            mism.append((cid, sec, js["durations"][cid]))
        tail = CSC.TAIL + (CSC.TAIL_EXTRA_QUOTE if cid in quotes else 0.0)
        for b in (sil(CSC.LEAD), pcm, sil(tail)):
            w.writeframes(b)
            n_samples += len(b) // 2
print(f"{out.name}: {len(narration.SCRIPT)}カット・{n_samples}標本 = {n_samples / SR:.3f}秒"
      f"／wav の秒と narration.json の秒が 0.6ms 超ずれたカット {len(mism)} {mism[:3]}")
