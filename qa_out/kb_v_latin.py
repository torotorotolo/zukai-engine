# -*- coding: utf-8 -*-
"""⑤c 3周目 ── 画面に**私たちが書いた**ラテン文字を数える。

⚠️ 型⑯（写真・図版に**焼き込まれた**英字 21カット）とは別。あちらは素材の制約で直せない。
   こちらは台本・設計に自分で書いた英字なので、直せる（#381 `c724`／§R-16 の系）。
   出典行の「MIR-25-40」「NTSB」は様式なので除く。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

from cuts import SPEC                                      # noqa: E402

LAT = re.compile(r"[A-Za-z][A-Za-z0-9 .\-]*")


def scan(v):
    if not isinstance(v, str):
        return []
    return [m.strip() for m in LAT.findall(v) if len(m.strip()) >= 2]


def main():
    hits = {}
    for cid, sp in SPEC.items():
        found = []
        # ⚠️ 副題は "s"。1版目は "sub" と書いて `c111`「NSTM」と `c724` を取りこぼした
        for key in ("t", "s", "note", "lead", "src"):
            found += [(key, m) for m in scan(sp.get(key))]
        for a in sp.get("ann") or []:
            for key in ("t", "v", "d"):
                found += [("注記." + key, m) for m in scan(a.get(key))]
        f = sp.get("fig")
        if f and isinstance(f[1], dict):
            for b in f[1].get("blocks") or []:
                for key in ("t", "v"):
                    found += [("panel." + key, m) for m in scan(b.get(key))]
            for n in f[1].get("nodes") or []:
                for key in ("t", "d"):
                    found += [("people." + key, m) for m in scan(n.get(key))]
        if found:
            hits[cid] = found
    print(f"■ 画面に書いたラテン文字がある ＝ {len(hits)} カット／全 {len(SPEC)}")
    for cid, f in hits.items():
        print(f"  {cid}  " + "／".join(f"{k}「{t}」" for k, t in f))


if __name__ == "__main__":
    main()
