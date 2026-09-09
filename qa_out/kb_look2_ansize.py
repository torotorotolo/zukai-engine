# -*- coding: utf-8 -*-
"""写真カットの注記（ann）で「答え」が「問い（ラベル）」より小さくないかを全数で測る。
（2026-09-10・⑤c 検品【見る】2周目 2/3）

§R-4「答えが `v` の組と `d` の組に割れる」を、**組ごとの実際の級数**まで降ろしたもの。
級数は `scene_jiko.photo_ann()` と同じ `fm.fit()` で求める（＝描画に渡る値そのもの）。

陽性対照：`c516` の段2（ラベル 46 に対して答え `d`）が「答え≦ラベル」に出ること。
        （焼いた絵の墨の高さでも ラベル43px 対 答え40px と確かめてある）
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "tools")

import scene_jiko as S  # noqa: E402
from cuts import SPEC  # noqa: E402

fm = S.fm
PANEL_GAP = S.PANEL_GAP


def maxw_of(spec):
    side = spec.get("side", "right")
    if spec.get("panel"):
        px, _py, pw, _ph = S.photo_box(spec)
        return (S.J.RIGHT - (px + pw + PANEL_GAP)) if side == "right" \
            else ((px - PANEL_GAP) - S.J.MG)
    return 1500 if spec.get("band") else 700


def main():
    bad, allrows, spread = [], 0, []
    for cid, spec in SPEC.items():
        ann = spec.get("ann")
        if not ann or not spec.get("photo"):
            continue
        mw = maxw_of(spec)
        sizes = []
        for a in ann:
            if not a.get("t"):
                continue
            ts = fm.fit(a["t"], mw, "Noto", cap=a.get("ts", 46), floor=24)
            if a.get("v"):
                asz = fm.fit(a["v"], mw, "Dela", cap=a.get("vs", 96), floor=30)
                kind = "v"
            elif a.get("d"):
                dcap = max(a.get("ds", 34), ts)
                asz = fm.fit(a["d"], mw, "Noto", cap=dcap, floor=22)
                kind = "d"
            else:
                continue
            allrows += 1
            sizes.append(asz)
            if asz <= ts:
                bad.append((asz - ts, cid, a["t"], a.get("v") or a.get("d"),
                            ts, asz, kind))
        if len(sizes) >= 2 and max(sizes) - min(sizes) >= 24:
            spread.append((max(sizes) - min(sizes), cid, sizes))
    bad.sort()
    print(f"写真カットの注記 {allrows} 組を測った")
    print(f"🔴 答えがラベル以下 ＝ {len(bad)} 組 / {len({b[1] for b in bad})} カット")
    for d, cid, t, v, ts, asz, kind in bad:
        print(f"  {cid}  ラベル{ts:.0f} 対 答え{asz:.0f}（{kind}）  「{t}」→「{v}」")
    spread.sort(reverse=True)
    print(f"\n🔴 1枚の中で答えの級数が 24 以上ひらく ＝ {len(spread)} カット")
    for d, cid, sizes in spread[:15]:
        print(f"  {cid}  {'/'.join(f'{s:.0f}' for s in sizes)}  （差 {d:.0f}）")
    ctrl = [b for b in bad if b[1] == "c516"]
    print(f"\n陽性対照 c516 = {'出た' if ctrl else '🔴出ない＝測れていない'}")


if __name__ == "__main__":
    main()
