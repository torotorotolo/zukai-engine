# -*- coding: utf-8 -*-
"""音素の網（再発防止策1の試作）── 人が判定する一覧を出す（API 不使用・2026-09-24）。

  python qa_out/phon_review.py ep13 [--ids c101,c203-2] [--gop -8]

phon_check.analyse の結果から、①読みの食い違い（雑音の型は除く）②GOP が低いのに食い違いの出ない語
③句読点の無い所の間、を1行1件で出す。**合否は人が読んで決める**（網は聞く所を絞るだけ）。
雑音の型（12本目 r04 の陰性 425行で数えた・2026-09-24）＝自然な発音と pyopenjtalk の表記の差:
  「いう」の i→yu（15件）／e の後の i↔e（ei＝ee・6件）／o の後の u↔o（ou＝oo）／「所」の sh↔j（しょ・じょ 6件）
陽性対照の実測（12本目 r04）: 誤読 9行中 8行を①で捕まえた（逃したのは 漁船＝ぎょせん→ぎょうせん の長音だけ）。
  語頭語尾の欠け 4行は 1行だけ（実験の j 抜け）＝「いきなり始まる」聞こえ方は音素が欠けないので網にかからない。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phon_check as P  # noqa: E402


def benign(h, r):
    e, x, s = h["exp"], h["rec"], P.surf(r, h["tok"])
    prev = r["El"][h["e0"] - 1] if h["e0"] > 0 else ""
    if (e, x) == ("i", "yu") and ("いう" in s or "言う" in s or "いっ" in s):
        return True
    if (e, x) in (("i", "e"), ("e", "i")) and prev == "e":
        return True
    if (e, x) in (("u", "o"), ("o", "u")) and prev == "o":
        return True
    if (e, x) in (("sh", "j"), ("j", "sh")) and "所" in s:
        return True
    return False


def ctx(r, k):
    t = r["tok"]
    a = r["toks"][t[k - 1]][0] if 0 < k <= len(t) else "（頭）"
    b = r["toks"][t[k]][0] if k < len(t) else "（尾）"
    return f"{a}｜{b}"


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "ep13"
    gthr = float(P.arg("--gop", "-8"))
    ids = [x for x in (P.arg("--ids", "") or "").split(",") if x]
    rows = P.analyse(tag)
    if ids:
        rows = [r for r in rows if any(r["lid"] == i or r["lid"].startswith(i + "-") for i in ids)]
    nb = 0
    print("## ① 読みの食い違い（雑音の型を除く）: 行 | 語 | 読み→音 | 位置 | 語の GOP")
    for r in rows:
        for h in r["bad"]:
            if benign(h, r):
                nb += 1
                continue
            g = min((r["tg"].get(i, 0.0) for i in h["tok"]), default=0.0)
            print(f"{r['lid']} | {P.surf(r, h['tok'])} | {h['exp'] or '∅'}→{h['rec'] or '∅'} | {h['pos']} | {g:.1f}")
    print(f"（雑音の型として除いた {nb}件）")
    print(f"\n## ② GOP が {gthr} 未満なのに ① に出ない語: 行 | 語 | GOP")
    for r in rows:
        shown = {i for h in r["bad"] for i in h["tok"]}
        for i, v in sorted(r["tg"].items()):
            if v < gthr and i not in shown:
                print(f"{r['lid']} | {r['toks'][i][0]} | {v:.1f}")
    print("\n## ③ 句読点の無い所の間: 行 | 秒 | 長さ | 印 | 前｜後")
    for r in rows:
        for p in r["pauses"]:
            if p[3] != "句読点":
                print(f"{r['lid']} | {p[0]:.2f} | {p[1]:.2f} | {p[3] or '無印'} | {ctx(r, p[2])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
