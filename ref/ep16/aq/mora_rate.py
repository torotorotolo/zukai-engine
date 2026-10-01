# -*- coding: utf-8 -*-
"""mora_rate.py — 同じ話速なのに字/分が回で違うわけを数える（16本目 ⑤a-2・2026-10-01）。読むだけ（audio/ に触らない）。

  python ref/ep16/aq/mora_rate.py <narration.json> <yomi_sheet.tsv> [名前]

行ごとに 拍（モーラ）・読点の数・声の秒（narration.json の subtitles の d）を突き合わせ、
d ≈ a×拍 ＋ b×読点 ＋ c を最小二乗で当てる（a＝1拍の秒・b＝読点1つの間）。
16本目の実測（話速147・行間0.49）＝15本目 r02 と比べて 1字あたりの拍 +2.3%（1.315／1.286）・読点 +15%（100字あたり
6.57／5.69）・1拍の秒 93.1ms／91.6ms＝声そのものの速さはほぼ同じで、台本の中身のぶん字/分が下がる（354.1 と 364.3）。
前の回と比べるときは `git show <版>:audio/narration.json` と `git show <版>:ref/epN/aq/yomi_sheet.tsv` を一時ファイルへ。"""
import csv
import json
import re
import sys

import numpy as np

SMALL = set("ゃゅょぁぃぅぇぉゎ")
PUNCT = re.compile(r"[、。？！「」（）・]")


def mora(yomi):
    return sum(1 for ch in yomi if "\u3041" <= ch <= "\u309f" and ch not in SMALL or ch in "ーっ" and ch not in SMALL)


def main(nar, sheet, name):
    js = json.load(open(nar, encoding="utf-8"))
    rows = {r["行ID"]: r for r in csv.DictReader(open(sheet, encoding="utf-8"), delimiter="\t")}
    X, y, chars, moras, commas, secs = [], [], 0, 0, 0, 0.0
    miss = 0
    for cid, subs in js["subtitles"].items():
        for i, s in enumerate(subs, 1):
            r = rows.get(f"{cid}-{i}")
            if r is None:
                miss += 1
                continue
            yo = r["読み"]
            m = mora(yo)
            c = yo.count("、")
            body = re.sub(r"^Q:\s", "", r["文"])
            chars += len(PUNCT.sub("", body))
            moras += m
            commas += c
            secs += s["d"]
            X.append([m, c, 1.0])
            y.append(s["d"])
    a, b, c0 = np.linalg.lstsq(np.array(X), np.array(y), rcond=None)[0]
    pred = np.array(X) @ np.array([a, b, c0])
    resid = np.array(y) - pred
    print(f"[{name}] 話速 {js['speed']}・行間 {js['gap']}／行 {len(y)}（表に無い行 {miss}）")
    print(f"  句読点なし {chars:,}字・拍 {moras:,}（1字あたり {moras / chars:.3f}拍）・読点 {commas}（100字あたり {100 * commas / chars:.2f}）")
    print(f"  声 {secs:.1f}秒 → 拍/秒 {moras / secs:.3f}・声だけの字/分 {chars / (secs / 60):.1f}")
    print(f"  当てはめ d ≈ {a * 1000:.1f}ms×拍 ＋ {b * 1000:.0f}ms×読点 ＋ {c0 * 1000:.0f}ms"
          f"（残差の標準偏差 {resid.std() * 1000:.0f}ms）→ 読点の間を除いた拍/秒 {1 / a:.3f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
