# -*- coding: utf-8 -*-
"""**構図がそっくりなカット**を探す。文字は違うのに絵が同じ、を見つける。

■ なぜ要るか（2026-08-04 の r05 目視で出た）
  `mapfig` の6カットが**全部おなじ対角の折れ線**だった。
  c101（東京→大阪）と c127（大月→山中）は、点の位置まで
  0.74/0.26 対 0.70/0.24 とほぼ一致していて、**同じ章の中で同じ絵が2回**出ていた。
  机上検査6種はどれも文字しか見ないので、**絵の使い回しは全部通る**。

■ 測り方
  1コマ画像を「地」と「文字」に分けられないので、**文字が乗らない構造だけを見る**。
  → 灰色にして 32×18 に潰し、平均で二値化した指紋（dHash に近い）を取る。
    小さな文字は潰れて消え、**枠・板・線・点の配置だけが残る**。
  → 指紋のハミング距離が近いカットの組を出す。

  ⚠️ **同じ型を使えば似るのは当たり前。** 出るのは候補であって、罪ではない。
     見るのは「**隣り合っている／同じ章の中にある**」組。離れていれば実害は小さい。

    python tools/check_twin.py                 # 距離 12 以下の組
    python tools/check_twin.py --d 8           # きびしく
    python tools/check_twin.py --dir out/jiko/qa_r05
"""
import argparse
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image

HERE = Path(__file__).parent.parent
W, H = 32, 18


def fp(path):
    im = Image.open(path).convert("L")
    # 見出し帯（上 18%）と字幕帯（下 17%）は毎カット同じ形なので落とす。
    # ここを入れたままだと全カットが似て出る。
    w, h = im.size
    im = im.crop((0, int(h * 0.18), w, int(h * 0.83))).resize((W, H), Image.BILINEAR)
    px = list(im.getdata())
    avg = sum(px) / len(px)
    return [1 if v > avg else 0 for v in px]


def dist(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def chap(cid):
    return cid[:2] if cid[0] == "c" else cid[:2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="out/jiko/qa_r05")
    ap.add_argument("--d", type=int, default=12, help="この距離以下を出す")
    a = ap.parse_args()

    d = HERE / a.dir
    files = sorted(d.glob("cut_*.jpg"))
    if not files:
        print(f"✗ {d} に cut_*.jpg が無い")
        return 1
    print(f"{len(files)}カットの指紋を取る…")
    fps = {}
    for f in files:
        fps[f.stem[4:]] = fp(f)

    ids = sorted(fps)
    order = {c: i for i, c in enumerate(ids)}
    hits = []
    for i, x in enumerate(ids):
        for y in ids[i + 1:]:
            dd = dist(fps[x], fps[y])
            if dd <= a.d:
                hits.append((dd, x, y))
    hits.sort()

    near = [h for h in hits if abs(order[h[1]] - order[h[2]]) <= 6]
    same = [h for h in hits if h not in near and chap(h[1]) == chap(h[2])]
    far = [h for h in hits if h not in near and h not in same]

    def show(title, rows, why):
        print(f"\n── {title}（{len(rows)}組）　{why}")
        for dd, x, y in rows[:40]:
            gap = abs(order[x] - order[y])
            print(f"   距離{dd:3d}  {x} ⇔ {y}   （{gap}カット離れ）")
        if len(rows) > 40:
            print(f"   （ほか {len(rows) - 40}組）")

    show("🔴 近いところに同じ絵", near, "6カット以内。**視聴者が続けて見るので実害が大きい**")
    show("⚠️ 同じ章の中に同じ絵", same, "章をまたがない。退屈さの原因になりうる")
    show("・章をまたぐ相似", far, "離れているので実害は小さい。型が同じなら当たり前")

    print(f"\n合計 {len(hits)}組（距離 {a.d} 以下）")
    return 1 if near else 0


if __name__ == "__main__":
    sys.exit(main())
