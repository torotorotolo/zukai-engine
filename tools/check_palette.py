# -*- coding: utf-8 -*-
"""章ごとの色（12本目から・2026-09-23 カズヤくん決定）の門番。

測るもの（どれか外れたら exit 1）
  1. `scene_jiko.CHAPTER_PALETTE` の章名が、いまの `scene_jiko.CHAPTERS` の章名に**全部当たる**か。
     🔴 次の回で CHAPTERS だけ差し替えて色の表を直し忘れると、前の回の章名が1つも当たらない＝ここで止まる
     （章番号で引く作りだと、前の回の色が新しい回の同じ番号の章へ**黙って**出る。§0b）。
  2. 色の名前が `jiko_style.PALETTES` に在るか。
  3. 各色の地（BG）に対して、文字に使う色が **4.5:1 以上**か（WCAG の小さい文字の下限・§5b-6d）。
     地・線の色（INK_W・LINE・TICK）は章の色、意味の色（AMBER・ALERT・DOC・INST・OK）は替えない。
  4. **隣り合う章の色が見分けられるか**＝写真の中間の明るさ（デュオトーンの中点）の色の差 ΔE（CIE76）が
     DE_MIN 以上か。同じ色が隣り合うのは可（区切りは章の扉が運ぶ）。

🔴 しきい値 DE_MIN は**見本の目視で決めた**（2026-09-23・`ref/ep12/mock_palettes.py` の3×3）：
   - 目で「近すぎる」と判じた2組＝見本の赤銅とセピア **5.6**／見本の夜の藍と紺 **11.9** → 必ず鳴ること（陽性対照）
   - 目ではっきり違って見えた組＝見本のセピアと青緑 **14.7**
   → その間の **13**。陽性対照が鳴らなければ物差しが壊れている＝exit 1（[[feedback-verify-your-own-instrument]]）。
   ⚠️ 最初は 20 と置いたが、根拠が無く（見本で明らかに違うセピアと青緑まで落ちた）、上の3点で決め直した。
   測るのは写真の中点だけ（図の線の色の差は参考に出す）。
  5. 🆕 2026-10-14（22本目 ⑤b-1）：**役の色**（`jiko_style.ROLE`＝米沿岸警備隊・会社・母船ほか＝「図に色を多く」）。
     ①使う章の色の地（BG・BG2）すべての上で文字の比 4.5 以上 ②紺の7色（PAL_TOKENS）と同じ値でない（同じ値は remap で章の色に
     置き換わる＝役の色が消える）③意味の色（ALERT・AMBER・DOC と別名でない OK・INST）・ほかの役・使う章の線と目盛りと主図形
     （LINE・TICK・INK_W）から ΔE（CIE76・色そのもの）ROLE_DE_MIN 以上 ④別名（ROLE_ALIAS）は値が本当に同じか。
     ROLE_DE_MIN 25＝check_color の「別の意味の色」の下限（同じ物差し）。陽性対照＝見本の母船 #7fc8e8 と紺の LINE（12.0）・
     見本の会社 #f0903c と AMBER（24.0）が鳴ること。⚠️ 潜水艇の白 sub と INK_W は同じ白の扱い（照合から外す）
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J

TEXT_MIN = 4.5
DE_MIN = 13.0
TEXT_TOKENS = ("INK_W", "LINE", "TICK")
MEANING = ("AMBER", "ALERT", "DOC", "INST", "OK")
# 陽性対照（見本の値そのまま。目で「近すぎる」と判じた）
CONTROLS = [("見本の赤銅", ("#2a1511", "#fbe3cf"), "見本のセピア", ("#241a10", "#f3e7cf")),
            ("見本の夜の藍", ("#0e1330", "#dfe4fb"), "紺（11本目まで）", ("#16232e", "#e6eef2"))]


def rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def ratio(a, b):
    def L(h):
        r, g, bb = (lin(c) for c in rgb(h))
        return 0.2126 * r + 0.7152 * g + 0.0722 * bb
    la, lb = L(a), L(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def lab(c):
    r, g, b = (lin(x) for x in c)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.0
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = [v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116 for v in (x, y, z)]
    return 116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])


def mid(duo):
    d, l = rgb(duo[0]), rgb(duo[1])
    return tuple((p + q) / 2 for p, q in zip(d, l))


def de(duo_a, duo_b):
    a, b = lab(mid(duo_a)), lab(mid(duo_b))
    return sum((p - q) ** 2 for p, q in zip(a, b)) ** 0.5


ROLE_DE_MIN = 25.0        # 役の色どうし・意味の色・章の線との差の下限（check_color.DE_MIN と同じ物差し）
ROLE_CONTROLS = [("見本の母船", "#7fc8e8", J.PALETTES["navy"]["LINE"], "紺の章の線 LINE と 12.0"),
                 ("見本の会社", "#f0903c", J.AMBER, "黄 AMBER と 24.0")]


def de1(a, b):
    """色そのものの差（CIE76）。章の色の差（de＝写真の中点）とは別"""
    la, lb = lab(rgb(a)), lab(rgb(b))
    return sum((p - q) ** 2 for p, q in zip(la, lb)) ** 0.5


def duo_of(name):
    p = J.palette(name)
    return p["BG2"], p["DUO_L"]


def main():
    import scene_jiko as S
    bad = []

    def say(ok, msg):
        print(("✓ " if ok else "🔴 ") + msg)
        if not ok:
            bad.append(msg)

    # 0. 物差しの陽性対照
    for na, a, nb, b in CONTROLS:
        v = de(a, b)
        say(v < DE_MIN, f"陽性対照：{na} と {nb} の差 ΔE {v:.1f} は DE_MIN {DE_MIN} 未満で鳴る")

    names = {nm for _, nm in S.CHAPTERS.values()}
    # 1. 章名の当たり
    stale = [k for k in S.CHAPTER_PALETTE if k not in names]
    say(not stale, f"色の表の章名がいまの章名に全部当たる（当たらない {len(stale)}件 {stale[:3]}）")
    # 2. 色の名前
    unknown = sorted({v for v in S.CHAPTER_PALETTE.values() if v not in J.PALETTES})
    say(not unknown, f"色の名前が jiko_style.PALETTES に在る（無い {unknown}）")
    # 3. 文字の比
    used = sorted(set(S.CHAPTER_PALETTE.values()) | {"navy"} - set(unknown))
    print(f"\n■ 地との比（文字 {TEXT_MIN} 以上）")
    print("色       " + " ".join(f"{k:>6s}" for k in TEXT_TOKENS + MEANING))
    for pn in used:
        p = J.palette(pn)
        row, low = [], []
        for k in TEXT_TOKENS + MEANING:
            c = p[k] if k in p else getattr(J, k)
            r = ratio(c, p["BG"])
            row.append(f"{r:6.2f}")
            if r < TEXT_MIN:
                low.append(f"{k} {r:.2f}")
        print(f"{pn:8s} " + " ".join(row))
        say(not low, f"{pn}：文字の色が全部 {TEXT_MIN} 以上（足りない {low}）")
    # 4. 隣り合う章の色の差
    print(f"\n■ 隣り合う章の色の差（写真の中点の ΔE・{DE_MIN} 以上。同じ色の隣は可）")
    chs = sorted(S.CHAPTERS.values())
    pal = [(n, nm, S.CHAPTER_PALETTE.get(nm, "navy")) for n, nm in chs]
    for (n1, _, p1), (n2, _, p2) in zip(pal, pal[1:]):
        if p1 == p2:
            print(f"  {n1}章 {p1} → {n2}章 {p2}：同じ色（可）")
            continue
        v = de(duo_of(p1), duo_of(p2))
        say(v >= DE_MIN, f"{n1}章 {p1} → {n2}章 {p2}：ΔE {v:.1f}")
    # 5. 役の色（22本目から）
    role = getattr(J, "ROLE", {})
    if role:
        print(f"\n■ 役の色（文字 {TEXT_MIN} 以上・ΔE {ROLE_DE_MIN} 以上・紺の7色と別の値）")
        for nm, c, ref, want in ROLE_CONTROLS:
            v = de1(c, ref)
            say(v < ROLE_DE_MIN, f"陽性対照：{nm}（{c}）と {ref} の差 ΔE {v:.1f} は ROLE_DE_MIN {ROLE_DE_MIN} 未満で鳴る（{want}）")
        alias = getattr(J, "ROLE_ALIAS", {})
        tok = {J.PALETTES["navy"][k].lower(): k for k in J.PAL_TOKENS}
        for k, c in role.items():
            if k in alias:
                say(c.lower() == getattr(J, alias[k]).lower(), f"役 {k}＝{alias[k]} の別名（値が同じ {c}）")
                continue
            low = [f"{pn} {min(ratio(c, J.palette(pn)['BG']), ratio(c, J.palette(pn)['BG2'])):.2f}"
                   for pn in used if min(ratio(c, J.palette(pn)["BG"]), ratio(c, J.palette(pn)["BG2"])) < TEXT_MIN]
            say(not low, f"役 {k} {c}：どの章の地でも文字の比 {TEXT_MIN} 以上（足りない {low}）")
            say(c.lower() not in tok, f"役 {k} {c}：紺の7色と別の値（同じ＝{tok.get(c.lower())}）")
            ref = {n: getattr(J, n) for n in ("ALERT", "AMBER", "DOC", "OK", "INST")}
            ref.update({f"役 {o}": v for o, v in role.items() if o != k and o not in alias})
            # ⚠️ 潜水艇の白 sub は主図形の白 INK_W と同じ役＝章の線・目盛り・INK_W とは照らさない（INK_W と章の線の差は
            #    白黒 18.3・セピア 21.4 で、公開した回もこの組で描いてきた＝同じ白を別の基準で止めない。2026-10-14 実測）
            for pn in ([] if k == "sub" else used):
                for t in ("LINE", "TICK", "INK_W"):
                    ref[f"{pn}.{t}"] = J.palette(pn)[t]
            near = sorted((de1(c, v), n) for n, v in ref.items())[:1]
            say(near[0][0] >= ROLE_DE_MIN, f"役 {k} {c}：いちばん近い色 {near[0][1]} と ΔE {near[0][0]:.1f}")
    print(f"\n{'🔴 ' + str(len(bad)) + '件' if bad else '✓ 章の色 すべて合格'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
