# -*- coding: utf-8 -*-
"""⑤c 3周目 ── `photo_ann` の「答えの級数がひらく29カット」の**中身**を見る。

`kb_u_meter.py ann` は級数しか印字しないので、「大きい側は数字か」が決められない。
⚠️ 式を写さない。`scene_jiko.photo_ann()` を**本当に回して** `<text>` を読む。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S                                     # noqa: E402
from cuts import SPEC                                      # noqa: E402

T = re.compile(r'<text[^>]*?font-size="([0-9.]+)"[^>]*?>([^<]*)</text>')
NUM = re.compile(r'[0-9０-９]')


def main():
    print(f"■ 読んだファイル: {Path(S.__file__).resolve()}")
    big_num = big_word = 0
    for cid, sp in SPEC.items():
        if not sp.get("ann") or sp.get("panel"):
            continue
        pairs = []
        for a, blk in zip(sp["ann"], S.photo_ann(sp)):
            hits = T.findall(blk)
            ans = str(a.get("v") or a.get("d") or "")
            hit = [float(sz) for sz, tx in hits if tx == ans]
            if hit:
                pairs.append((hit[0], ans))
        if len(pairs) < 2:
            continue
        gap = max(p[0] for p in pairs) - min(p[0] for p in pairs)
        if gap < 24:
            continue
        top = max(pairs)[1]
        kind = "数字" if NUM.search(top) else "🔴語"
        if kind == "数字":
            big_num += 1
        else:
            big_word += 1
        body = "／".join(f"{s:.0f}「{t[:16]}」" for s, t in pairs)
        print(f"  {cid} 開き{gap:3.0f}px  最大＝{kind}  {body}")
    print(f"\n最大が数字 {big_num} カット ／ 🔴 最大が語 {big_word} カット")


if __name__ == "__main__":
    main()
