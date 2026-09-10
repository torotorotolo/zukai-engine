# -*- coding: utf-8 -*-
"""ラベル（問い）の墨と、答えの墨の**縦のすき間**を、本番の SVG から測る。

■ なぜ（台帳 §Y-2）
  `pr08`（`vs=112`）で「接触から崩落まで」の白墨と「13秒」の赤墨が **3px 重なっていた**。
  目視で1件見つけたので、その場で全数へ広げる（[[feedback-scale-one-visual-finding-to-a-full-count]]）。

■ 測り方
  `scene_jiko.build_layers()` の `{cid}_aN` レイヤー＝**注記1段ぶん**。その中の `<text>` を
  順に (ラベル, 答え, 補足) として読み、`fontmetrics.ink()` で字面の上端・下端を出す。
  すき間 ＝ 答えの字面の上端 − ラベルの字面の下端（負なら**重なっている**）。
  ⚠️ 縁取り（`stroke-width`）は墨の外へ半分ひろがるので、その半分ずつも引く。

■ 陽性対照 `--pos` … 全部の答えの級数を +40px にする。**すき間が縮まなければ測れていない**。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import fontmetrics as fm                                     # noqa: E402
import scene_jiko as S                                       # noqa: E402

LINE = 10          # 墨のすき間の下限（台帳 §Y-2 の実測から）
TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')
A = {k: re.compile(k + r'="([^"]*)"') for k in
     ("x", "y", "font-size", "font-family", "stroke-width", "text-anchor")}


def rows(svg):
    """(字面, ベースライン, 級数, 書体, 縁の太さ, 左, 右)。

    ⚠️ **横の位置まで出す。** 最初これを出さずに測ったら、`panel` の段ラベル「1」と
       同じ行の問いを「上下に積まれた組」として数え、**-119px の重なり**が202組も出た。
       同じ行に横並びしているものは、上下のすき間を測る相手ではない。
    """
    out = []
    for m in TEXT.finditer(svg):
        a, t = m.group(1), m.group(2)
        if not t.strip():
            continue
        g = {k: (r.search(a).group(1) if r.search(a) else "") for k, r in A.items()}
        size = float(g["font-size"])
        w = sum(fm.adv(c, g["font-family"]) for c in t) * size
        x, anc = float(g["x"]), (g["text-anchor"] or "start")
        x0 = x - w if anc == "end" else (x - w / 2 if anc == "middle" else x)
        out.append((t, float(g["y"]), size, g["font-family"],
                    float(g["stroke-width"] or 0), x0, x0 + w))
    return out


def stacked(a, b):
    """横の範囲が重なっているか（＝上下に積まれた組か）。"""
    lo, hi = max(a[5], b[5]), min(a[6], b[6])
    return (hi - lo) > 0.2 * min(a[6] - a[5], b[6] - b[5])


def main(pos=False):
    print(f"■ 画は本番と同じ経路: {Path(S.__file__).resolve()} の build_layers()")
    print(f"■ 字幅・字面: {Path(fm.__file__).resolve()}／モード: "
          f"{'陽性対照（答えを+40px）' if pos else '実測'}")
    jobs, _ = S.build_layers(allow_missing=True)
    hits = []
    for k in sorted(jobs):
        if "_a" not in k:
            continue
        cid = k.split("_")[0]
        rs = rows(jobs[k])
        for i in range(len(rs) - 1):
            r1, r2 = rs[i], rs[i + 1]
            (t1, y1, s1, f1, w1, _l1, _r1) = r1
            (t2, y2, s2, f2, w2, _l2, _r2) = r2
            if y2 <= y1 or not stacked(r1, r2):
                continue
            if pos:
                s2 += 40
            bot = y1 + fm.ink(t1, s1, f1)[1]
            top = y2 - fm.ink(t2, s2, f2)[0]
            hits.append((top - bot, cid, s2, t1, t2, (w1 + w2) / 2))
    hits.sort()
    # ⚠️ 台帳 §Y-2 が絵から測った値は**墨どうし**（色で分けて測った）。
    #    ここも墨どうしを主にして、縁取りぶんは別の欄に出す。
    #    突き合わせ：`pr08`＝ここ -3.3px／台帳 **-3px**、`pr02`(104)＝2.1px／台帳 **2px**。
    print(f"\n{'墨のすき間':>9}{'縁込み':>8}{'級数':>6}  カット  ラベル ／ 答え")
    for gap, cid, s2, t1, t2, halo in hits:
        mark = "🔴" if gap < 0 else ("⚠️" if gap < LINE else "  ")
        print(f"{mark}{gap:>7.1f}px{gap - halo:>7.1f}px{s2:>6.0f}  "
              f"{cid:6} 「{t1[:18]}」／「{t2[:16]}」")
    bad = [h for h in hits if h[0] < LINE]
    print(f"\n{'🔴' if bad else '✓'} 墨のすき間が {LINE}px 未満 ＝ {len(bad)} 組"
          f"／うち重なり（負）＝ {len([h for h in hits if h[0] < 0])} 組"
          f"／測った {len(hits)} 組")
    print("  ⚠️ 線は台帳 §Y-2 の実測から取った：`vs=88` は 10〜15px で読めていて、"
          "`vs=96` の 6px は「縁取りが食い込む」。**境目は 96 と 104 のあいだ**。")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main("--pos" in sys.argv[1:]))
