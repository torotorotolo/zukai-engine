# -*- coding: utf-8 -*-
"""31本目 ⑤c／⑤c' の見る版のフォルダを組む（mkc30.py を写した・中身は同じ＋前半と後半の数を出す）。
  python -P qa_out/ep31_c/mkc31.py <元> <先>
    例（⑤c）  out/jiko/qa-ep31_b7_full out/jiko/qa_ep31_c
  cut_*.jpg はそのまま・card_*.png はそのまま（qa_sheet が cut_cN00card.jpg に写す）
  at_<cid>_<割合>.jpg → cut_<cid>_<割合>.jpg（qa_sheet・qa_seen は cut_*.jpg しか並べない）
  🔴 扉の名が card_cN01.png でない章は qa_sheet が黙って飛ばす
     ＝ここで cut_<1つ前の番号>card.jpg に写す（31本目は11枚とも cN01＝写す物は無い見込み）
  🔴 前半（⑤c-1）と後半（⑤c-2）は1つのフォルダ・1つの帳にする（qa_seen の帳はフォルダ1つ＝分けると続きを書けない）
     ＝31本目の1通目は「前半だけを qa_ep31_c1 へ」だったが、30本目と同じく1つにした（⑤c-1 は sheet 01〜26）
写したら md5 で元と照らす。🔴 元を qa_sheet に直接わたすと頭のコマ（at_*）が黙って抜ける。
⚠️ Modal の成果物が1段下のフォルダに入っていたら、その1段下を <元> にする。"""
import hashlib
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path("C:/Users/konar/Desktop/zukai-engine")
FIRST_HALF = tuple(f"c{n}" for n in "123456")   # つかみ〜第6章（c101〜c631）


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def odd_card_name(fname):
    """card_c702.png → cut_c701card.jpg。card_cN01.png は None（qa_sheet が写すので、ここでは写さない）。"""
    m = re.fullmatch(r"card_c([0-9a-f])(\d\d)\.png", fname)
    if not m or m.group(2) == "01":
        return None
    return f"cut_c{m.group(1)}{int(m.group(2)) - 1:02d}card.jpg"


def half_counts(dst):
    """前半と後半の コマの数（最後のコマ・頭のコマ・扉）を名前から数える。"""
    out = {}
    for half, test in (("前半", lambda c: c.startswith(FIRST_HALF)),
                       ("後半", lambda c: not c.startswith(FIRST_HALF))):
        last = [f for f in dst.glob("cut_*.jpg") if re.fullmatch(r"cut_[0-9a-z]+\.jpg", f.name)
                and test(f.name[4:])]
        head = [f for f in dst.glob("cut_*_*.jpg") if test(f.name[4:])]
        card = [f for f in dst.glob("card_*.png") if test(f.name[5:])]
        out[half] = (len(last), len(head), len(card))
    return out


def main(src, dst):
    src, dst = REPO / src, REPO / dst
    if not src.is_dir():
        raise SystemExit(f"🔴 元が無い: {src}")
    if dst.exists() and any(dst.iterdir()):
        raise SystemExit(f"🔴 先が空でない: {dst}")
    dst.mkdir(parents=True, exist_ok=True)
    pairs = [(f, dst / f.name) for f in sorted(src.glob("cut_*.jpg"))]
    pairs += [(f, dst / f.name) for f in sorted(src.glob("card_*.png"))]
    pairs += [(f, dst / ("cut_" + f.name[3:])) for f in sorted(src.glob("at_*.jpg"))]
    bad = 0
    for a, b in pairs:
        shutil.copy2(a, b)
        if md5(a) != md5(b):
            bad += 1
            print("🔴 md5 違い", a.name)
    odd = []
    for card in sorted(src.glob("card_*.png")):
        name = odd_card_name(card.name)
        if name:
            with Image.open(card) as im:
                im.convert("RGB").save(dst / name, quality=92)   # qa_sheet.cards_as_cuts と同じ写し方
            odd.append(f"{card.name}→{name}")
    n_cut = len(list(dst.glob("cut_*.jpg")))
    n_card = len(list(dst.glob("card_*.png")))
    print(f"写した {len(pairs)}（cut {n_cut}＝最後のコマと頭のコマ・扉 {n_card}）・md5 違い {bad}")
    if odd:
        print(f"扉の名が cN01 でない {len(odd)}枚を写した（qa_sheet は飛ばす）: {' '.join(odd)}")
    for half, (last, head, card) in half_counts(dst).items():
        print(f"{half}: 最後のコマ {last}・頭のコマ {head}・扉 {card}＝{last + head + card}コマ")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
