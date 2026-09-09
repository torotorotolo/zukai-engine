# -*- coding: utf-8 -*-
"""`photo_ann` の補足（`d`）が、自分の値より**下の組のラベル**に近くなっていないかを全数で測る。

■ なぜ（⑤c 2周目の目視・6例）
    `c214` `c215` `c316` `c413` `c422` `c201` で、補足の一行が
    「上の答えの補足」ではなく「**下の見出し**」に見えた。近接の原則が逆に効いている。

■ 測り方
    `scene_jiko.build_layers()` が組んだ SVG の `<text>` を、
    `check_layout.boxes()` で**字面の外接矩形**にして、上から順に並べる。
    連続する2行の縦の空き（下の行の上端 − 上の行の下端）を出し、

        上の空き ＝ 値 `v`（または前の行）と補足 `d` のあいだ
        下の空き ＝ 補足 `d` と次の組のラベル `t` のあいだ

    **下の空き ≤ 上の空き** なら、補足は下の組に寄って見える。

⚠️ 行の役（t / v / d）は SPEC の文字列と突き合わせて決める（座標だけでは分からない）。
⚠️ フォントは先に読む（`check_layout` と同じ理由）。

使い方: python qa_out/kb_look2_gap.py
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))

import fontmetrics as _fm  # noqa: E402
_fm.measured()

import scene_jiko as S              # noqa: E402
from check_layout import boxes      # noqa: E402
from cuts import SPEC               # noqa: E402


def roles(cid):
    """その画面で使われている文字列 → 役（t / v / d）と組番号。"""
    m = {}
    for i, a in enumerate(SPEC.get(cid, {}).get("ann") or []):
        for k in ("t", "v", "d"):
            if a.get(k):
                m[str(a[k])] = (k, i)
    return m


def main():
    jobs, _ = S.build_layers(allow_missing=True)
    per = {}
    for k, svg in jobs.items():
        cid = k.split("_")[0] if "_" in k else k
        per.setdefault(cid, []).append(svg)

    hits = []
    for cid in sorted(per):
        role = roles(cid)
        if not role:
            continue
        rows = []
        for svg in per[cid]:
            for x0, y0, x1, y1, t, *_ in boxes(svg, cid):
                if t in role:
                    r, i = role[t]
                    rows.append((y0, y1, r, i, t))
        rows.sort()
        for j, (y0, y1, r, i, t) in enumerate(rows):
            if r != "d" or j == 0 or j + 1 >= len(rows):
                continue
            up = y0 - rows[j - 1][1]                 # 上の空き
            dn = rows[j + 1][0] - y1                 # 下の空き
            if rows[j + 1][2] != "t" or rows[j + 1][3] == i:
                continue                              # 次が別の組のラベルでなければ見ない
            if dn <= up:
                hits.append((cid, t[:22], round(up), round(dn),
                             rows[j - 1][4][:14], rows[j + 1][4][:14]))

    print(f"🔴 補足が「上の答え」より「下の見出し」に近い: {len(hits)}件 "
          f"/ {len(set(h[0] for h in hits))}カット")
    print("   cid   補足                 上の空き 下の空き  上の行 → 下の行")
    for cid, t, up, dn, prev, nxt in hits:
        print(f"   {cid}  {t:22} {up:5}px {dn:5}px   「{prev}」→「{nxt}」")


if __name__ == "__main__":
    main()
