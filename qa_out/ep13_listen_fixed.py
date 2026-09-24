# -*- coding: utf-8 -*-
"""13本目 ⑤a'：**直した行だけ**の短い mp3 と目次を作る（API 不使用・2026-09-24）。

  python qa_out/ep13_listen_fixed.py   → out/ep13_listen/ep13_fixed_t130.mp3 ＋ _index.md

行の音は el_build と同じ切り方（narration.json の subtitles の t・d）＝出荷する音。行と行のあいだは 1.0秒。
直した行と直した理由は下の FIXED（⑤a' のログ audio/el_qa/build_ep13_a2_fix*.log・retake_ep13_a2_head.log から）。
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "ep13_listen"
SR = 24000
GAP = 1.0
NUM = "数の前後の間（数字に戻した）"
HEAD = "行頭の崩れ（取り直し）"
FIXED = {
    **{k: NUM for k in ("c101-1 c101-2 c105-1 c202-2 c209-1 c212-1 c220-1 c401-1 c402-2 c407-1 c411-1 c412-1 c422-3 "
                        "c506-1 c520-3 c605-1 c610-2 c611-2 c613-2 c614-1 c622-3 c701-1 c701-2 c706-2 c718-1 c814-1 "
                        "c715-2 c805-1 c515-2 c220-2").split()},
    **{k: HEAD for k in "c303-1 c821-1 c602-2 c510-1 c713-1 c906-2 c905-2 c403-2 c712-1 c703-1 c418-1 c423-1 c917-2 c101-2 c607-2".split()},
    "c304-2": "側→がわ（網『そば』）", "c305-2": "側→がわ（網『そば』）", "c512-1": "側→がわ", "c609-3": "側→がわ（網『そば』）",
    "c508-1": "交わす→かわす（網『まじわす』）", "c905-1": "床→ゆか（網『とこ』）＋数", "c906-1": "1.86→カタカナ（網『わちろく』）",
    "c709-2": "管制官→かんせいかん（網『かんじぇい』）", "c713-2": "管制→かんせい・便名→びんめい",
    "c103-1": "旅客機→りょかくき（読みをそろえる）", "c109-1": "旅客機→りょかくき", "c501-1": "旅客機→りょかくき",
    "c401-2": "N103AA をカタカナの1語に", "c416-2": "貨物室の「し」抜け（取り直し）",
    "c710-1": "床が崩れ→ゆか（行頭が3回崩れた）", "c712-1": "昇降舵→しょうこうだ（網『しょうこうがじ』）＋行頭",
}
FIXED["c101-1"] = NUM + "＋旅客機"
FIXED["c607-2"] = HEAD + "＋旅客機→りょかくき"
FIXED["c101-2"] = NUM + "＋" + HEAD
FIXED["c412-1"] = NUM + "＋N103AA"
FIXED["c407-1"] = NUM + "＋N103AA"


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def main():
    sys.path.insert(0, str(ROOT / "tools"))
    import el_script as E
    nj = json.loads((ROOT / "audio" / "narration.json").read_text(encoding="utf-8"))
    order = [l.lid for l in E.lines() if l.lid in FIXED]
    missing = set(FIXED) - set(order)
    if missing:
        raise SystemExit(f"🔴 台本に無い行ID: {sorted(missing)}")
    chunks, idx, t = [], [], 0.0
    cache = {}
    for lid in order:
        cid, i = lid.rsplit("-", 1)
        if cid not in cache:
            with wave.open(str(ROOT / "audio" / f"{cid}.wav"), "rb") as w:
                cache[cid] = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        r = nj["subtitles"][cid][int(i) - 1]
        seg = cache[cid][int(round(r["t"] * SR)):int(round((r["t"] + r["d"]) * SR))]
        idx.append(f"- {mmss(t)}　{lid}　{FIXED[lid]}\n  　{r['text']}")
        chunks += [seg, np.zeros(int(GAP * SR), dtype=np.int16)]
        t += len(seg) / SR + GAP
    OUT.mkdir(parents=True, exist_ok=True)
    mp3 = OUT / "ep13_fixed_t130.mp3"
    pcm = np.concatenate(chunks).tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0",
                    "-b:a", "80k", str(mp3)], input=pcm, check=True)
    head = (f"# 13本目 ⑤a' 直した行だけ（{len(order)}行・{mmss(t)}）\n\n"
            "カズヤくんが聞かなくても仕上がっている前提です（音素の網と間の実測で確かめ済み）。気になったら時刻で教えてください。\n"
            "⚠️ 9/25 20:00 を過ぎると音声は直せません。\n\n")
    (OUT / "ep13_fixed_t130_index.md").write_text(head + "\n".join(idx) + "\n", encoding="utf-8")
    print(f"✓ {len(order)}行・{mmss(t)} → {mp3}（{mp3.stat().st_size / 1e6:.1f}MB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
