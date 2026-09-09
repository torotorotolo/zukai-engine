# -*- coding: utf-8 -*-
"""panel の各段で「問い（t・左寄せ）」と「答え（v・右寄せ）」の横の空きを、
   焼いた絵の画素から全数で測る（2026-09-10・⑤c 検品【見る】2周目 2/3）。

⚠️ 設計値ではなく**焼いた絵**を測る（設計に書いた値が絵に届くとは限らない）。
陽性対照：§R-9 で目測「20px 台」とした `c207` が、最小の側に出ること。
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "tools")
from cuts import SPEC  # noqa: E402

D = Path("out/jiko/qa_keybridge-r02")


def main():
    rows = []
    for cid, s in SPEC.items():
        fig = s.get("fig")
        if not fig or fig[0] != "panel":
            continue
        p = D / f"cut_{cid}.jpg"
        if not p.exists():
            continue
        a = np.asarray(Image.open(p).convert("L")).astype(int)
        ink = a > 110
        # 段の帯は、左端の色罫（x=75..95）が立っている y から拾う
        band = ink[:, 70:100].sum(axis=1) > 3
        ys, run = [], None
        for i, v in enumerate(band):
            if v and run is None:
                run = i
            if not v and run is not None:
                if i - run > 60:
                    ys.append((run, i))
                run = None
        blocks = fig[1].get("blocks") or []
        for bi, (y0, y1) in enumerate(ys):
            # ⚠️ 2026-09-10：`v` が無い段は「問いと答えのあいだ」が存在しない。
            #    `t` が右端まで伸びるので下の右端しらべを通ってしまい、
            #    **題の中の字間**を最小の空きとして拾っていた（`c911` `c917`）。
            if bi >= len(blocks) or not blocks[bi].get("v"):
                continue
            cols = ink[y0:y1, 200:1880].sum(axis=0) > 0
            best, run = (0, 0, 0), None
            for i, v in enumerate(cols):
                if not v and run is None:
                    run = i
                if v and run is not None:
                    if i - run > best[0]:
                        best = (i - run, run, i)
                    run = None
            xa, xb = 200 + best[1], 200 + best[2]
            # ⚠️ 「いちばん広い空白」が本当に**問いと答えのあいだ**か確かめる。
            #    答え（v）は右寄せなので、空白の右側の墨が RIGHT(1848) 近くまで届くこと。
            right = np.where(cols)[0]
            if len(right) == 0 or 200 + right[-1] < 1700:
                continue
            if not cols[:best[1]].any():          # 空白の左に墨が無い＝答えだけの段
                continue
            rows.append((best[0], cid, y0, xa, xb))
    rows.sort()
    print(f"panel の段 {len(rows)} 組を測った（{len({r[1] for r in rows})} カット）")
    print("── 空きが小さい順に15組 ──")
    for g, cid, y0, xa, xb in rows[:15]:
        print(f"  {cid}  y={y0:4d}  空き {g:4d}px  （{xa}→{xb}）")
    q = np.percentile([r[0] for r in rows], [10, 50, 90])
    print(f"10%点 {q[0]:.0f}px ／ 中央値 {q[1]:.0f}px ／ 90%点 {q[2]:.0f}px")
    ctrl = [g for g, cid, *_ in rows if cid == "c207"]
    print(f"陽性対照 c207 の段 = {ctrl} px（§R-9 の「目測 20px 台」は測ると 55px）")


if __name__ == "__main__":
    main()
