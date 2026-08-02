# -*- coding: utf-8 -*-
"""配色の物差し。**色を足す前に、地との比と色どうしの離れ方を実測する。**

🔴 なぜ要るか（2026-08-02 カズヤくん指摘「色が増えていない」）
   r13 の試写で「色使いが少なく似た演出が続いて飽きる」と言われ、
   前の巡では `TICK` を1色足しただけで終わっていた。**答えになっていない。**
   色を足すなら、足す前に

     ① 地（BG）との比        … 文字なら 4.5 以上、線・面なら 3.0 以上
     ② すでにある色との離れ方 … 近すぎる色を足しても「増えた」ことにならない

   の2つを測る。⚠️ 「暗い技術図」という様式は壊さない。派手な色は足さない。

■ 自分の物差しをまず疑う（[[feedback-verify-your-own-instrument]]）
   この道具は最初から `jiko_style.py` に**すでに書き込まれている実測値**で検算する。
     GRID 1.36 ／ LINE_DIM 2.64 ／ ALERT 4.55 ／ TICK 6.39 ／
     LINE 8.21 ／ AMBER 9.26 ／ OK 7.89 ／ INK_W 15.67
   ここが再現できないうちは、新しい色の数字も信じない。

■ 色どうしの離れ方
   CIE2000 ではなく **CIE76（Lab のユークリッド距離）** で足りる。
   ここで見たいのは「隣に置いたとき別の色に見えるか」であって、
   微差の知覚一致ではない。**ΔE 25 以上**を「別の意味の色」の下限とする。
   ⚠️ `TICK` は LINE を暗くした**同系の派生色**（実測 ΔE 8.2）で、
      別の意味を持たせるための色ではない。判定からは外す（下の DERIVED）。
      🔴 最初この道具の説明に「LINE と TICK は ΔE 22.4」と**測らずに書いた**。
         実測は 8.2 だった。説明文であっても数字を推定で置かない。

使い方:
    python tools/check_color.py            … 全色の地との比と、色どうしの距離
    python tools/check_color.py --check    … 記録済みの実測値と突き合わせる（★先にこれ）
"""
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J

# jiko_style.py に**すでに書いてある**実測値。道具の検算に使う（推定ではない）
RECORDED = {"GRID": 1.36, "LINE_DIM": 2.64, "ALERT": 4.55, "TICK": 6.39,
            "LINE": 8.21, "AMBER": 9.26, "OK": 7.89, "INK_W": 15.67}

TEXT_MIN = 4.5      # 小さい文字に要る比（WCAG AA）
GRAPHIC_MIN = 3.0   # 線・面に要る比（WCAG AA 非文字）
DE_MIN = 25.0       # 図の中で取り違えないための色どうしの最小距離
# 「別の意味の色」ではないもの。地に沈める色と、既存色の派生（明るさ違い）。
DERIVED = {"GRID", "BG2", "LINE_DIM", "ALERT_DIM", "INST_DIM", "DOC_DIM", "TICK"}


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(h):
    r, g, b = (lin(c) for c in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def lab(h):
    """sRGB → CIELAB（D65）。色どうしの離れ方を測るために要る。"""
    r, g, b = (lin(c) for c in rgb(h))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.00000
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def de(a, b):
    la, lb = lab(a), lab(b)
    return sum((x - y) ** 2 for x, y in zip(la, lb)) ** 0.5


def palette():
    """jiko_style から色だけを拾う（新しく足した色も自動で入る）。"""
    skip = {"BG"}
    out = {}
    for k in dir(J):
        if k.startswith("_") or k in skip or not k.isupper():
            continue
        v = getattr(J, k)
        if isinstance(v, str) and v.startswith("#") and len(v) == 7:
            out[k] = v
    return out


def verify():
    """★まず道具を疑う。記録済みの実測値を再現できるか。"""
    print("■ 物差しの検算（jiko_style.py に記録済みの実測値と突き合わせる）")
    ok = True
    for name, want in RECORDED.items():
        got = ratio(getattr(J, name), J.BG)
        d = abs(got - want)
        mark = "✓" if d <= 0.02 else "🔴"
        if d > 0.02:
            ok = False
        print(f"  {mark} {name:<10}{getattr(J, name)}  記録 {want:5.2f} / 実測 {got:5.2f}"
              + ("" if d <= 0.02 else f"  ← ずれ {d:.2f}"))
    print("  " + ("✓ 記録と一致した。この物差しは信用してよい"
                  if ok else "🔴 一致しない。**新しい色の数字を信じてはいけない**"))
    return ok


def main():
    if "--check" in sys.argv:
        return 0 if verify() else 1
    verify()
    pal = palette()
    print(f"\n■ 地（BG {J.BG}）との比  ── 文字 {TEXT_MIN} 以上／線・面 {GRAPHIC_MIN} 以上")
    for k, v in sorted(pal.items(), key=lambda kv: ratio(kv[1], J.BG)):
        r = ratio(v, J.BG)
        use = ("文字にも使える" if r >= TEXT_MIN else
               ("線・面だけ" if r >= GRAPHIC_MIN else "沈める用（文字に使わない）"))
        L, a, b = lab(v)
        print(f"  {k:<10}{v}  比 {r:5.2f}  L*{L:5.1f}  {use}")

    print(f"\n■ 色どうしの離れ方（ΔE76・{DE_MIN} 未満は図の中で取り違える）")
    # 地に沈める色と、同系の派生色は「区別させる」対象ではないので外す
    live = {k: v for k, v in pal.items() if k not in DERIVED}
    near = []
    for (ka, va), (kb, vb) in itertools.combinations(sorted(live.items()), 2):
        d = de(va, vb)
        if d < DE_MIN:
            near.append((d, ka, kb))
    for d, ka, kb in sorted(near):
        print(f"  🔴 {ka} と {kb} が近い（ΔE {d:.1f}）")
    if not near:
        print(f"  ✓ 生きている色 {len(live)}つは、どれも ΔE {DE_MIN} 以上離れている")

    print("\n■ 対で並べたときの比（隣に置く色は 3.0 以上ないと境目が見えない）")
    for ka, kb in (("LINE", "TICK"), ("LINE", "INK_W"), ("AMBER", "OK"),
                   ("ALERT", "AMBER"), ("INST", "LINE"), ("DOC", "AMBER"),
                   ("INST", "ALERT"), ("DOC", "INK_W")):
        if not (hasattr(J, ka) and hasattr(J, kb)):
            continue
        print(f"  {ka:<8}× {kb:<8} 比 {ratio(getattr(J, ka), getattr(J, kb)):5.2f}"
              f"  ΔE {de(getattr(J, ka), getattr(J, kb)):5.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
