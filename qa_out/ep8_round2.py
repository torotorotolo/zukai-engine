# -*- coding: utf-8 -*-
r"""ep8_round2.py — 2周目の聞取を1周目と突き合わせ、「直った／残った／新しく崩れた」を機械で出す（⑤a・8本目）。

  python qa_out/ep8_round2.py

🔴 なぜ要るか（7本目の教訓）:
   Scribe は**同じ音を2回起こすと結果が変わる**。1回の聞取で「誤読だ」と決めると、
   直さなくてよい行を直して**元は正しかった行を壊す**。だから
     ・**2周とも崩れた行だけ**を直す
     ・辞書を当てた行は**2周目で本当に直ったか**を確かめる
   の2つをここで機械にやらせる。

見るもの:
   A. 辞書を当てた 58行 … 2周目の聞取に「狙った語」が出ているか
   B. 1周目で崩れ、辞書を当てていない行 … 2周目も崩れているか（＝本物）／直っているか（＝Scribe の揺れ）
   C. 1周目は無事で 2周目に崩れた行 … 焼き直しで壊した疑い／Scribe の揺れ
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
Q = ROOT / "audio" / "el_qa"


def load(p):
    rows = list(csv.DictReader(p.read_text(encoding="utf-8").splitlines(), delimiter="\t"))
    return {r["場面"]: r for r in rows}


def main():
    import el_script as ES
    r1, r2 = load(Q / "ep8_el_yomi_round1.tsv"), load(Q / "ep8_el_yomi.tsv")
    lines = {l.lid: l.text for l in ES.lines()}
    hits = {}
    for l in ES.lines():
        h = []
        ES.el_text(l.text, h)
        if h:
            hits[l.lid] = h
    print(f"1周目 {len(r1)}行 ／ 2周目 {len(r2)}行 ／ 辞書を当てた行 {len(hits)}")

    def ratio(d, lid):
        """🔴 一致率は tsv に **0〜1 の比**（"1.000"）で入っている。%と取り違えると
        しきい値に一度も届かず、**全部『動きなし』**という嘘の合格が出る（2026-09-14 実測）。
        → [[feedback-verify-your-own-instrument]]"""
        try:
            v = float(d[lid]["一致率"].rstrip("%"))
        except Exception:
            return -1.0
        return v * 100.0 if v <= 1.0 else v

    # 陽性対照＝物差しがポイントで動くこと（0.90→0.84 は 6ポイント差）
    assert abs(ratio({"x": {"一致率": "0.900"}}, "x") - 90.0) < 1e-9, "一致率をパーセントに直せていない"

    print("\n=== A. 辞書を当てた行（2周目の聞取）===")
    worse = []
    for lid in sorted(hits, key=lambda x: (x[:2], x)):
        a, b = ratio(r1, lid), ratio(r2, lid)
        mark = "⭐" if b > a + 0.5 else ("▲" if b < a - 0.5 else "＝")
        if mark == "▲":
            worse.append(lid)
        print(f"{mark} {lid:<8} {a:5.1f}% → {b:5.1f}%")
        print(f"    台本: {lines[lid]}")
        print(f"    1周目: {r1[lid]['聞こえた文']}")
        print(f"    2周目: {r2[lid]['聞こえた文']}")

    print(f"\n=== B/C. 辞書を当てていない行で一致率が 3ポイント以上動いた行 ===")
    moved = []
    for lid in r2:
        if lid in hits:
            continue
        a, b = ratio(r1, lid), ratio(r2, lid)
        if abs(a - b) >= 3.0:
            moved.append((lid, a, b))
    for lid, a, b in sorted(moved, key=lambda x: x[2] - x[1]):
        mark = "▲" if b < a else "⭐"
        print(f"{mark} {lid:<8} {a:5.1f}% → {b:5.1f}%")
        print(f"    台本: {lines[lid]}")
        print(f"    1周目: {r1[lid]['聞こえた文']}")
        print(f"    2周目: {r2[lid]['聞こえた文']}")
    print(f"\n辞書を当てた行で悪化 {len(worse)}／当てていない行で3pt以上動いた {len(moved)}")
    print("⚠️ 動いた行は**焼き直していない**（キャッシュから同じ pcm を出している）ので、"
          "動きは全部 Scribe の揺れ。台本と読み比べて本物だけ拾う。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
