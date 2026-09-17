# -*- coding: utf-8 -*-
"""9本目 ⑤c：シート4枚ごとに「語り・見出し・副題・写真・注記」を並べた手元の一覧を書く（この回だけの道具）。

シートの絵だけでは「絵が語りと合っているか」「副題が写っているものと合っているか」を決められないので、
同じ並び（`qa_sheet.cuts_of` と同じ＝ファイル名の昇順）で文字の側を並べる。
⚠️ 読むだけ。台本・`audio/narration.json`・`cuts.SPEC` は書き換えない。

    python qa_out/ep9_sheetnotes.py   → qa_out/ep9_notes_b1.txt 〜 b9.txt（1ファイル＝シート4枚＝24カット）
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import cuts  # noqa: E402
import qa_sheet  # noqa: E402

SRC = HERE / "out" / "jiko" / "qa_ep9-r01"
SHEETS = HERE / "out" / "jiko" / "sheet_ep9-r01"
PER_SHEET = 6
PER_BATCH = 4


def strings_in(x, out):
    """fig の中の文字だけを拾う（色コードなど # で始まるものは捨てる）。"""
    if isinstance(x, str):
        if x and not x.startswith("#"):
            out.append(x)
    elif isinstance(x, dict):
        for v in x.values():
            strings_in(v, out)
    elif isinstance(x, (list, tuple)):
        for v in x:
            strings_in(v, out)
    return out


def main():
    nar = json.loads((HERE / "audio" / "narration.json").read_text(encoding="utf-8"))
    subs, durs = nar["subtitles"], nar["durations"]
    names = qa_sheet.cuts_of(SRC)
    sheets = sorted(SHEETS.glob("sheet_*.jpg"))
    assert len(sheets) * PER_SHEET >= len(names), "シートの枚数が足りない"

    for b in range(0, len(sheets), PER_BATCH):
        lines = []
        for si in range(b, min(b + PER_BATCH, len(sheets))):
            chunk = names[si * PER_SHEET:(si + 1) * PER_SHEET]
            lines.append(f"== {sheets[si].name}")
            for pos, cid in enumerate(chunk):
                sp = cuts.SPEC.get(cid, {})
                where = f"{'左右'[pos % 2]}{pos // 2 + 1}段"
                photo = sp.get("photo", "")
                fig = sp.get("fig")
                kind = f"photo={Path(photo).stem}" if photo else ""
                if sp.get("panel"):
                    kind += "(額装)"
                if fig:
                    kind += f" fig={fig[0]}"
                narr = "".join(s["text"] for s in subs.get(cid, []))
                lines.append(f"[{cid}] {where} {durs.get(cid, 0):.1f}秒 {kind}")
                lines.append(f"   見出し「{sp.get('t', '')}」 副題「{sp.get('s', '')}」")
                extra = []
                if sp.get("ann"):
                    extra += strings_in(sp["ann"], [])
                if fig:
                    extra += strings_in(fig[1], [])
                if extra:
                    lines.append("   画の文字：" + "／".join(extra)[:260])
                lines.append(f"   語り：{narr[:300]}")
        out = HERE / "qa_out" / f"ep9_notes_b{b // PER_BATCH + 1}.txt"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(out.name, len(lines), "行")


if __name__ == "__main__":
    main()
