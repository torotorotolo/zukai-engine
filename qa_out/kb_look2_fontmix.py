# -*- coding: utf-8 -*-
"""同じ列の中で `v` の書体が Dela と Noto に割れるカットを全数で数える（2026-09-09・⑤c 2周目）。

⚠️ §P-3 #2 は「`v` は Dela 固定」と結論していたが、**`txt()` が自分でもう一度
   `numfam()` を通す**（`titan_fig.py:145`）ので、呼び出し側の "Dela" は最終ではない。
   → 実際に描かれる書体は `numfam(v, "Dela")` の戻り。ここではそれを数える。

陽性対照：`c103`（「持ち主・管理者」＝ Dela ／ 他2段 ＝ Noto）で mixed が出ること。
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))

import titan_fig as T  # noqa: E402
from cuts import SPEC as CUTS  # noqa: E402  ⚠️ cuts が持つ名前は SPEC


def main():
    mixed, alldela, allnoto = [], [], []
    for cid, spec in CUTS.items():
        fig = spec.get("fig")
        if not fig or fig[0] != "panel":
            continue
        blocks = fig[1].get("blocks") or []
        fams = []
        for b in blocks:
            v = b.get("v")
            if v in (None, ""):
                continue
            fams.append((str(v), T.numfam(str(v), "Dela")))
        if len(fams) < 2:
            continue
        kinds = {f for _, f in fams}
        row = (cid, fams)
        if len(kinds) > 1:
            mixed.append(row)
        elif kinds == {"Dela"}:
            alldela.append(row)
        else:
            allnoto.append(row)

    print(f"panel で v が2欄以上あるカット: {len(mixed)+len(alldela)+len(allnoto)}")
    print(f"  🔴 1枚の中で書体が割れる: {len(mixed)}カット")
    print(f"     全部 Dela: {len(alldela)} ／ 全部 Noto: {len(allnoto)}")
    print()
    for cid, fams in mixed:
        print(cid)
        for v, f in fams:
            print(f"    {f:5} {v}")


if __name__ == "__main__":
    main()
