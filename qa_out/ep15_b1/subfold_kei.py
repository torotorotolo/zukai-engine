# -*- coding: utf-8 -*-
"""15本目 ⑤b-1（2026-09-30）：字幕の書体を Noto → けいふぉんと にしたことで**折りが変わった行**を全数書き出す（ルール §6-58）。

  python qa_out/ep15_b1/subfold_kei.py      → qa_out/ep15_b1/15本目_字幕の折り_Noto→けいふぉんと.tsv

折り方は本番と同じ `scene_jiko.wrap2`（書体は `scene_jiko.SUB_FONT` を切り替える＝描く書体の字幅で測る）。
秒は narration.json の実測（カットの頭＋字幕の t）＝`aq_build.timeline` と同じ並び。⑤c の検品は、この行を原寸で見る。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import check_listener as L       # noqa: E402  決め所（md の★）の読み方
import check_script as CS        # noqa: E402
import el_script                 # noqa: E402
import narration                 # noqa: E402
import scene_jiko as S           # noqa: E402

js = json.loads((ROOT / "audio" / "narration.json").read_text(encoding="utf-8"))
subs = js["subtitles"]
quotes = L.quote_cuts(CS, [c for c, _ in narration.SCRIPT])
rows, _ = L.timeline(list(narration.SCRIPT), CS, quotes, subs, ())      # ed01 も行に出す（字幕がある）

want = S.SUB_FONT
out, n2 = [], {"Noto": 0, "Kei": 0}
for cid, i, who, text, t in rows:
    folds = {}
    for font in ("Noto", "Kei"):
        S.SUB_FONT = font
        folds[font] = S.wrap2(text)
        n2[font] += len(folds[font]) == 2
    if folds["Noto"] != folds["Kei"]:
        kind = (f"{len(folds['Noto'])}行→{len(folds['Kei'])}行" if len(folds["Noto"]) != len(folds["Kei"])
                else "折り目が動いた")
        out.append((t, f"{cid}-{i}", "聞き役" if who == "q" else "語り", kind,
                    "／".join(folds["Noto"]), "／".join(folds["Kei"])))
S.SUB_FONT = want
p = Path(__file__).with_name("15本目_字幕の折り_Noto→けいふぉんと.tsv")
with p.open("w", encoding="utf-8", newline="\n") as f:
    f.write("時刻\t秒\t行ID\t話者\t変わり方\tNoto の折り\tけいふぉんと の折り\n")
    for t, lid, who, kind, a, b in out:
        f.write(f"{int(t // 60)}:{t % 60:04.1f}\t{t:.2f}\t{lid}\t{who}\t{kind}\t{a}\t{b}\n")
kinds = {}
for r in out:
    kinds[r[3]] = kinds.get(r[3], 0) + 1
print(f"字幕 {len(rows)}枚・2行に折れる Noto {n2['Noto']}／けいふぉんと {n2['Kei']}・折りが変わった {len(out)}行 {kinds}")
print(f"→ {p.relative_to(ROOT)}")
