# -*- coding: utf-8 -*-
"""32本目 ⑤c／⑤c' の見る版のフォルダを組む（qa_out/ep31_c/mkc31.py を写した・写し方は同じ）。
  python -P qa_out/ep32_c/mkc32.py <元> <先> [期待のコマ数]
    例（⑤c）  out/jiko/qa-ep32_b7_full out/jiko/qa_ep32_c 328
  cut_*.jpg はそのまま・card_*.png はそのまま（qa_sheet が cut_cN00card.jpg に写す）
  at_<cid>_<割合>.jpg → cut_<cid>_<割合>.jpg（qa_sheet・qa_seen は cut_*.jpg しか並べない）
  🔴 扉の名が card_cN01.png でない章は qa_sheet が黙って飛ばす
     ＝ここで cut_<1つ前の番号>card.jpg に写す（32本目は11枚とも cN01＝写す物は無い見込み）
  🔴 ⑤c と ⑤c' は1つのフォルダ・1つの帳（qa_seen の帳はフォルダ1つ＝分けると続きを書けない）
     ＝案B（2026-11-11）：⑤c は sheet 01〜40・⑤c' の頭で sheet 41
  🆕 期待のコマ数を渡すと、写した数（最後のコマ＋頭のコマ＋扉）と照らし、違えば exit 1
     ／頭のコマの元のカット（at_<cid>）が無ければ exit 1（黙って余分なコマを並べない）
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


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def odd_card_name(fname):
    """card_c702.png → cut_c701card.jpg。card_cN01.png は None（qa_sheet が写すので、ここでは写さない）。"""
    m = re.fullmatch(r"card_c([0-9a-f])(\d\d)\.png", fname)
    if not m or m.group(2) == "01":
        return None
    return f"cut_c{m.group(1)}{int(m.group(2)) - 1:02d}card.jpg"


def main(src, dst, expect=None):
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
    last = sorted(f.name for f in dst.glob("cut_*.jpg") if re.fullmatch(r"cut_[0-9a-z]+\.jpg", f.name))
    head = sorted(f.name for f in dst.glob("cut_*_*.jpg"))
    card = sorted(f.name for f in dst.glob("card_*.png"))
    last_ids = {n[4:-4] for n in last}
    orphan = [n for n in head if n[4:].split("_")[0] not in last_ids]
    total = len(last) + len(head) + len(card)
    print(f"写した {len(pairs)}・md5 違い {bad}")
    print(f"最後のコマ {len(last)}・頭のコマ {len(head)}・扉 {len(card)}＝{total}コマ")
    if odd:
        print(f"扉の名が cN01 でない {len(odd)}枚を写した（qa_sheet は飛ばす）: {' '.join(odd)}")
    if orphan:
        print(f"🔴 元のカットが無い頭のコマ {len(orphan)}: {' '.join(orphan)}")
    ng = bool(bad or orphan)
    if expect is not None:
        ok = total == expect
        print(f"{'✓' if ok else '🔴'} 期待 {expect}コマ ／ 写した {total}コマ")
        ng = ng or not ok
    return 1 if ng else 0


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        raise SystemExit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) == 4 else None))
