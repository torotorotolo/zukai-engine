# -*- coding: utf-8 -*-
"""レンダリング前に、文字の位置だけを机上で検算する。

なぜ要るか：
  レンダリングはクラウドだけなので、1巡すると3分半＋ダウンロードがかかる。
  「文字が画面外で切れる」「詰めたら注記どうしが重なった」は**字幅の計算で分かる**ので、
  クラウドに投げる前にここで落とす。余白を詰めた15巡目からは特に効く。

やること：
  1 scene_jiko の各レイヤーの SVG から <text> を全部拾う
  2 字幅を推定して外接矩形を出す
  3 画面（MG〜RIGHT・上60〜下906）から出ているものを名指しする
  4 **同じカットで同時に出ているレイヤー**どうしの重なりを名指しする

⚠️ 字幅は推定。フォントの実測ではないので、境界の1〜2文字ぶんは信用しない。
   ここを通っても**必ずクラウドで焼いて拡大目視する**（この道具は目視の代わりではない）。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J
import scene_jiko as S

TOP, BOT = 52, 906           # 字幕帯(916)より上。見出し(Dela 62px)の字面上端が 59
TEXT = re.compile(r'<text\s([^>]*)>([^<]*)</text>')
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
# ベースラインより下に出る字。深さは3段階で見る（読点と数字のコンマを同じ扱いにすると
# 「89,680」の下端を 43px も低く見積もって、単位の「回」と重なった判定になる）
DESC_DEEP = set("gjpqy、。")          # 0.22em
DESC_SHALLOW = set(",()（）")          # 0.10em


def adv(ch, family):
    """1文字の送り幅（em）。Noto/Dela の実測ではなく素朴な推定。"""
    o = ord(ch)
    if o >= 0x2E80:                      # 漢字・かな・全角記号
        return 1.0
    if ch == " ":
        return 0.30
    if ch in ".,":
        return 0.28
    if ch in "()（）":
        return 0.45
    return 0.72 if family == "Dela" else 0.56


def width(t, size, family):
    return sum(adv(c, family) for c in t) * size


def boxes(svg, layer):
    """(x0, y0, x1, y1, 文字, レイヤー名) を返す。y は字面の上下で近似。"""
    out = []
    for m in TEXT.finditer(svg):
        a = dict(ATTR.findall(m.group(1)))
        t = m.group(2)
        if not t.strip():
            continue
        x, y = float(a["x"]), float(a["y"])
        size, fam = float(a["font-size"]), a.get("font-family", "Noto")
        w = width(t, size, fam)
        anchor = a.get("text-anchor", "start")
        x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        # 字面：ベースラインより上に 0.74em。下は下に出る字の深さで3段階
        if any(c in DESC_DEEP or ord(c) >= 0x2E80 for c in t):
            below = size * 0.22
        elif any(c in DESC_SHALLOW for c in t):
            below = size * 0.10
        else:
            below = size * 0.03
        out.append((x0, y - size * 0.74, x0 + w, y + below, t, layer))
    return out


# カットごとに「同時に画面に出ているレイヤー」。_aN は途中から出るが、
# カットの終盤には全部出ているので、終盤の状態で重なりを見る。
def layers_of(cut, jobs):
    pre = f"{cut}_"
    return {k: v for k, v in jobs.items() if k.startswith(pre)}


def main():
    jobs = {}
    for name in dir(S):
        fn = getattr(S, name)
        if callable(fn) and re.fullmatch(r"[cp]\d_(base|bg|lab|a\d|call)", name):
            jobs[name] = fn()
    jobs["c7_num"] = S.c7_num(1.0)
    bad = 0

    print("── 画面から出ている文字 ──")
    for k, svg in sorted(jobs.items()):
        for x0, y0, x1, y1, t, _ in boxes(svg, k):
            why = []
            if x0 < J.MG - 4:
                why.append(f"左が {x0:.0f}（下限 {J.MG}）")
            if x1 > J.RIGHT + 4:
                why.append(f"右が {x1:.0f}（上限 {J.RIGHT}）")
            if y0 < TOP:
                why.append(f"上が {y0:.0f}")
            if y1 > BOT:
                why.append(f"下が {y1:.0f}")
            if why:
                bad += 1
                print(f"  🔴 {k}「{t[:22]}」… " + "／".join(why))
    if not bad:
        print("  ✓ 全部おさまっている")

    print("\n── 同じカットで重なっている文字 ──")
    cuts = sorted({k.split("_")[0] for k in jobs})
    ov = 0
    for cut in cuts:
        bs = []
        for k, svg in layers_of(cut, jobs).items():
            bs += boxes(svg, k)
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                a, b = bs[i], bs[j]
                ix = min(a[2], b[2]) - max(a[0], b[0])
                iy = min(a[3], b[3]) - max(a[1], b[1])
                if ix > 6 and iy > 6:
                    ov += 1
                    print(f"  🔴 {cut}: 「{a[4][:16]}」({a[5]}) と "
                          f"「{b[4][:16]}」({b[5]}) が {ix:.0f}×{iy:.0f}px 重なる")
    if not ov:
        print("  ✓ 重なりなし")

    print(f"\n{'🔴 直すところあり' if bad or ov else '✓ 机上の検算はすべて通った'}"
          f"（画面外 {bad}件・重なり {ov}件）")
    return 1 if bad or ov else 0


if __name__ == "__main__":
    sys.exit(main())
