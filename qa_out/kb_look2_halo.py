# -*- coding: utf-8 -*-
"""こちらが載せた文字が「明るい地」の上に乗っていないかを全216カットで測る（2026-09-09・⑤c 2周目）。

■ なぜ要るか（⑤c 2周目 c110・c113 の目視から）
    写真は NTSB 報告書のページを丸ごとラスタで取っているので、**白い注記箱と英字が
    絵に焼き込まれたまま**入ってくる（型⑯）。門番は SVG しか見ないので、
    こちらの文字がその白箱に乗っても**1件も鳴らない**（[[feedback-gates-dont-see-text-burned-into-the-picture]]）。

■ 測り方（グリフを避けて「まわり」を測る）
    文字の外接矩形そのものは自分のグリフで明るくなるので使えない。
    → 矩形の**外側 PAD px の縁（ハロー）**だけを測る。ここに自分の字は無い。
      ハローの輝度の**中央値**が高ければ、その文字は明るい地の上にある。

    地は暗幕を敷いた紺（J.BG 系＝輝度 30 前後）。**中央値 150 以上**なら明らかに白箱。

    🔴 ただし**中央値だけでは部分的な重なりを落とす**（c113「コンクリートと木材」は
       白箱に半分だけ乗っていて中央値は暗いまま＝実測で確認）。
       → ハローのうち**輝度 200 以上の画素の割合**も一緒に出し、15% 以上も拾う。

⚠️ これは目視の代わりではない。**当たりを付けるだけ**（0件でも全数目視はやめない）。
⚠️ フォントを先に読む（`check_layout` と同じ理由＝あとだと MemoryError で粗い値に落ちる）。

使い方: python qa_out/kb_look2_halo.py [--th=150] [--only=c1]
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))

import fontmetrics as _fm  # noqa: E402
_fm.measured()                      # 🔴 先に読む

import scene_jiko as S              # noqa: E402
import brand_jiko as J              # noqa: E402
from check_layout import boxes      # noqa: E402
from PIL import Image               # noqa: E402

SRC = HERE / "out" / "jiko" / "qa_keybridge-r02"
PAD = 10          # ハローの太さ
TH = 150          # 中央値がこれ以上なら「明るい地の上」
MINW = 40         # これより小さい文字は飾り


def median(vals):
    v = sorted(vals)
    return v[len(v) // 2] if v else 0


def halo(lum, box):
    x0, y0, x1, y1 = box
    W, H = lum.size
    px = lum.load()
    out = []
    for x in range(max(0, int(x0) - PAD), min(W, int(x1) + PAD), 3):
        for y in (int(y0) - PAD, int(y1) + PAD - 1):
            if 0 <= y < H:
                out.append(px[x, y])
    for y in range(max(0, int(y0) - PAD), min(H, int(y1) + PAD), 3):
        for x in (int(x0) - PAD, int(x1) + PAD - 1):
            if 0 <= x < W:
                out.append(px[x, y])
    if not out:
        return 0, 0.0
    return median(out), sum(1 for v in out if v >= 200) / len(out)


def main():
    th = TH
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--th="):
            th = int(a.split("=")[1])
        if a.startswith("--only="):
            only = a.split("=")[1]

    jobs, _ = S.build_layers(allow_missing=True)
    per_cut = {}
    for k, svg in jobs.items():
        cid = k.split("/")[0].split(":")[0].split("_")[0] if "_" in k else k
        per_cut.setdefault(cid, []).append((k, svg))

    n_hit = 0
    hits = {}
    for cid in sorted(per_cut):
        if only and not cid.startswith(only):
            continue
        p = SRC / f"cut_{cid}.jpg"
        if not p.exists():
            continue
        lum = Image.open(p).convert("L")
        rows = []
        for k, svg in per_cut[cid]:
            for x0, y0, x1, y1, t, _, _, ol in boxes(svg, k):
                if x1 - x0 < MINW:
                    continue
                m, br = halo(lum, (x0, y0, x1, y1))
                if m >= th or br >= 0.15:
                    rows.append((m, br, t[:26], ol, int(x0), int(y0)))
        if rows:
            hits[cid] = sorted(rows, reverse=True)
            n_hit += len(rows)

    print(f"■ 明るい地の上に乗っている文字: {n_hit}件 ／ {len(hits)}カット"
          f"（中央値 {th} 以上、または 200以上の画素が 15% 以上。ハロー {PAD}px）")
    for cid, rows in hits.items():
        print(f"  {cid}")
        for m, br, t, ol, x, y in rows[:6]:
            print(f"     中央値 {m:3}  白{br*100:4.0f}%  {'フチ有' if ol else '🔴フチ無'}"
                  f"  ({x},{y})  「{t}」")


if __name__ == "__main__":
    main()
