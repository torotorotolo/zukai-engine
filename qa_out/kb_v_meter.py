# -*- coding: utf-8 -*-
"""⑤c 3周目の物差し ── `panel` の**答え（`v`）側**の級数がカットの中で割れていないか。

⚠️ `kb_u_meter.py panel` は**問い（本文）側だけ**を測っている（`k` と `v` を除いて max を取る）。
   ⑤c' で問い側をそろえた結果、**答え側の割れだけが残った**（台帳 §U-5-4-1 の目視）。
   ここはその目視を全数へ広げる（[[feedback-scale-one-visual-finding-to-a-full-count]]）。

⚠️ 式を写さない。`titan_fig.panel()` を**本当に回して** `<text font-size=…>` を読む。
   ⚠️ 読んだファイルを必ず印字する（[[feedback-verify-your-own-instrument]] の2例目）。

  python -u qa_out/kb_v_meter.py        … 実測
  python -u qa_out/kb_v_meter.py --pos  … 陽性対照（v の1つを 2倍にして鳴るか）
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import titan_fig as T                                      # noqa: E402
from cuts import SPEC                                      # noqa: E402

TEXT = re.compile(r'<text[^>]*?font-size="([0-9.]+)"[^>]*?>([^<]*)</text>')
GAP = 8.0
RATIO = []          # (cid, 問い＝本文の級数, 答え＝v の級数, 問いの字面)


def rows(pos=False):
    out = []
    for cid, sp in SPEC.items():
        f = sp.get("fig")
        if not f or f[0] != "panel":
            continue
        kw = dict(f[1])
        bl = [dict(b) for b in kw["blocks"]]
        if pos:
            # 陽性対照：いちばん上の答えだけ、わざと長い語に替えて級数を落とさせる
            for b in bl:
                if str(b.get("v", "")).strip():
                    b["v"] = str(b["v"]) + "永" * 14
                    break
        kw["blocks"] = bl
        fig = T.panel(**kw)
        sizes, texts = [], []
        for st, b in zip(fig.stages, bl):
            v = str(b.get("v", "")).strip()
            if not v:
                continue
            hits = TEXT.findall(st)
            hit = [float(sz) for sz, tx in hits if tx == v]
            body = [float(sz) for sz, tx in hits
                    if tx and tx != v and tx != str(b.get("k", "\0"))]
            if hit:
                sizes.append(hit[0])
                texts.append(v)
                if body:
                    RATIO.append((cid, max(body), hit[0], str(b.get("t", ""))))
        if len(sizes) >= 2:
            out.append((cid, max(sizes) - min(sizes), sizes, texts))
    return out


def main():
    pos = "--pos" in sys.argv
    print(f"■ 読んだファイル: {Path(T.__file__).resolve()}")
    print(f"■ SPEC: {len(SPEC)} カット／モード: {'陽性対照' if pos else '実測'}")
    out = rows(pos)
    bad = sorted([r for r in out if r[1] >= GAP], key=lambda r: -r[1])
    print(f"\n🔴 答え（v）の級数が {GAP:.0f}px 以上割れる ＝ {len(bad)} カット"
          f"（答えが2つ以上ある panel は 全 {len(out)} カット）")
    for cid, g, sz, tx in bad:
        pair = "／".join(f"{s:.0f}「{t[:14]}」" for s, t in zip(sz, tx))
        print(f"  {cid}  開き{g:6.1f}px  {pair}")

    # §S-10 の残り ── 問い（本文）対 答え（v）。⑤c' は極端な2枚だけ直した
    if RATIO:
        low = sorted(RATIO, key=lambda r: r[2] / r[1])
        n = sum(1 for r in RATIO if r[2] < r[1])
        print(f"\n🔴 答え（v）が問い（本文）より小さい段 ＝ {n} 段（全 {len(RATIO)} 段）"
              f"／答え÷問い の中央値 {sorted(r[2] / r[1] for r in RATIO)[len(RATIO) // 2]:.0%}")
        for cid, q, a, t in low[:8]:
            print(f"  {cid}  問い{q:.0f} 対 答え{a:.0f} ＝ {a / q:.0%}  「{t[:18]}」")


if __name__ == "__main__":
    main()
