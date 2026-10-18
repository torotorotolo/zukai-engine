# -*- coding: utf-8 -*-
"""Noto Sans KR（可変・OFL）→ 太さ 700 に固定 → ハングルの音節すべて（U+AC00〜D7A3・11,172字）＋空白だけの woff2 を fonts/ に作る。

  python fonts/notosanskr-license/make_subset.py <NotoSansKR[wght].ttf の道>

2026-10-18（事故検証 23本目 ⑤b-2）。画面の出典の行のハングル（ソウル研究院の「서울연구데이터서비스」・Commons の個人の作者欄の名前）が
NotoSansJP に無い字＝豆腐になる（門番 check_layout）→ 書体を足した（カズヤくん了承）。
🔴 使う字だけに縮めない＝作者の名前の字だけの書体にすると公開リポから名前の字が読める（「名前0」）。音節すべてを入れる。
描き手は `tools/scene_jiko.ensure_css` が書体名「Noto」の @font-face をもう1つ unicode-range つきで足す（図の SVG は直さない）・
物差しは `tools/fontmetrics.FALLBACK`（字幅・字面・無い字の判定）。出どころと md5 は同じ置き場の SOURCE.md
"""
import hashlib
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

DST = Path(__file__).resolve().parents[1] / "NotoSansKR-Hangul-Bold.woff2"


def main(src):
    f = instancer.instantiateVariableFont(TTFont(src), {"wght": 700})
    opt = subset.Options()
    opt.flavor = "woff2"
    opt.layout_features = ["kern", "liga", "ccmp", "locl"]
    opt.hinting = False
    opt.name_IDs = ["*"]
    opt.name_languages = ["*"]
    opt.notdef_outline = True
    sub = subset.Subsetter(opt)
    sub.populate(unicodes=list(range(0xAC00, 0xD7A4)) + [0x20])
    sub.subset(f)
    f.flavor = "woff2"
    f.save(DST)
    cm = TTFont(DST).getBestCmap()
    print(f"{DST.name} {DST.stat().st_size} bytes・字 {len(cm)}・md5 {hashlib.md5(DST.read_bytes()).hexdigest()}")
    return 0 if all(cp in cm for cp in range(0xAC00, 0xD7A4)) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
