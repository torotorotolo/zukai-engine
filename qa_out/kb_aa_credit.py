# -*- coding: utf-8 -*-
"""注記のいちばん下の墨と、出典の行の墨の**縦のすき間**を、本番の SVG から全数で測る（台帳 §AA-1）。

■ なぜ（⑤c 5周目 1/3・c908）
  ⑤c' 4巡目の `BLOCK_GAP=34` で段を広げたぶん、3段目の補足「約65メートル」が出典の行へ
  押し出された。絵で 29px → 6px（r06 → r08）。目視1件を全数へ広げる
  （[[feedback-scale-one-visual-finding-to-a-full-count]]）。
■ 測り方
  `kb_y_gap.rows()`（字面・ベースライン・級数・書体・横の範囲）をそのまま使う。
  `{cid}_aN` の注記のうち、出典の行と**横に重なって上にある**もののいちばん下の墨 → 出典の墨の上端。
■ 対照
  `c908` の絵の実測（明るい行 822-845 と 852-873）＝ **6px**。ここが 6px 前後を出さなければ測れていない。
  （2026-09-11 実測：4.5px）
  ⚠️ 出典の行が見つからないカットは件数とカット番号を出す（0 で埋めない）。
     2026-09-11 は 113件＝写真を使わない図・表のカット（行は「報告書 p.」）と見られるが**全件は確かめていない**。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "qa_out"))
sys.stdout.reconfigure(encoding="utf-8")

import fontmetrics as fm   # noqa: E402
import scene_jiko as S     # noqa: E402
import kb_y_gap as G       # noqa: E402  rows() と stacked() をそのまま使う

AKEY = re.compile(r"^(\w+?)_a(\d+)$")
RED, WARN = 10, 20


def main():
    jobs, _ = S.build_layers(allow_missing=True)
    by = {}
    for k, svg in jobs.items():
        by.setdefault(k.split("_")[0], []).append((k, svg))
    out, nocredit = [], []
    for cid in sorted(by):
        ann = [r for k, svg in by[cid] if AKEY.match(k) for r in G.rows(svg)]
        if not ann:
            continue
        cred = [r for k, svg in by[cid] for r in G.rows(svg) if r[0].lstrip().startswith("出典")]
        if not cred:
            nocredit.append(cid)
            continue
        c = cred[0]
        above = [r for r in ann if r[1] < c[1] and G.stacked(r, c)]
        if not above:
            out.append((999, cid, "（注記と出典が横に重ならない）", c[0][:20]))
            continue
        low = max(above, key=lambda r: r[1] + fm.ink(r[0], r[2], r[3])[1])
        bot = low[1] + fm.ink(low[0], low[2], low[3])[1]
        top = c[1] - fm.ink(c[0], c[2], c[3])[0]
        out.append((top - bot, cid, f"{low[0][:16]}（{low[2]:.0f}px）", c[0][:20]))
    out.sort()
    print(f"{'すき間':>8}  カット  いちばん下の注記 ／ 出典")
    for g, cid, lo, cr in out:
        mark = "🔴" if g < RED else ("⚠️" if g < WARN else "  ")
        print(f"{mark}{g:>7.1f}px  {cid:6} {lo} ／ {cr}")
    print(f"\n注記レイヤーのあるカット {len(out) + len(nocredit)}件／測れた {len(out)}件／"
          f"出典の行が無い {len(nocredit)}件 {' '.join(nocredit)}")
    print(f"{WARN}px 未満 {len([o for o in out if o[0] < WARN])}件"
          f"（{RED}px 未満 {len([o for o in out if o[0] < RED])}件）")
    c908 = [o for o in out if o[1] == "c908"]
    print(f"対照 c908 = {c908[0][0]:.1f}px（絵の実測 6px）" if c908 else "🔴 対照 c908 が出ない")
    return 1 if not c908 else 0


if __name__ == "__main__":
    raise SystemExit(main())
