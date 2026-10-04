# -*- coding: utf-8 -*-
"""18本目 ⑤b-7b（2026-10-05）：Actions の試し焼き（`out/jiko/qa_ep18_b7b/`）の `at` のコマを 640px のシート（2列×3行）に並べる。
   python qa_out/ep18_b7b/make_sheets.py [qa_ep18_b7b] → qa_out/ep18_b7b/sheet_<qa の置き場>_<n>.jpg（1280×1080・各コマの左上に名前）
   python qa_out/ep18_b7b/make_sheets.py strips [qa_ep18_b7b] → 頁の額の**上の端と下の端**を原寸のまま帯に切り出し、4カットずつ縦に重ねる
     （strips_<qa の置き場>_<n>.jpg＝幅は額の幅＋20px・帯の高さ 70px）＝頁の端の行が欠けていないかを原寸で見る（§5b-115③）
   ＋ crop <名> <x0> <y0> <x1> <y1> [qa_dir] で原寸の切り出し
   （⑤b-7a の qa_out/ep18_b7a/make_sheets.py を写した。⚠️ 前のは置き場の名が fix で終わらないと sheet_N を上書きした＝名に置き場を入れた）"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CUTS = ("c105 c109 c303 c307 c316 c414 c508 c516 c623 c712 c721 c814 c903 c905 c909 c910 ca15 cb12 cb21 cb22").split()
args = [a for a in sys.argv[1:]]
qa_dir = next((a for a in args if a.startswith("qa_")), "qa_ep18_b7b")
args = [a for a in args if not a.startswith("qa_")]
base = ROOT / "out" / "jiko" / qa_dir
hit = next(iter(base.rglob("at_*_095.jpg")), None)
SRC = hit.parent if hit else base
if args and args[0] == "crop":
    name, box = args[1], tuple(int(v) for v in args[2:6])
    Image.open(SRC / f"at_{name}.jpg").convert("RGB").crop(box).save(OUT / f"crop_{name}_{box[0]}_{box[1]}.jpg", quality=92)
    print("crop", name, box)
    sys.exit(0)
if args and args[0] == "strips":
    sys.path.insert(0, str(ROOT / "tools"))
    import scene_jiko as S  # noqa: E402  額の箱（本番と同じ式）
    BAND = 70
    rows = []
    for c in CUTS:
        p = SRC / f"at_{c}_095.jpg"
        if not p.exists():
            print("無い", p.name)
            continue
        x, y, w, h = S.PHOTO_CUTS[c][0]
        im = Image.open(p).convert("RGB")
        top = im.crop((x - 10, y - 10, x + w + 10, y - 10 + BAND))
        bot = im.crop((x - 10, y + h + 10 - BAND, x + w + 10, y + h + 10))
        rows.append((c, top, bot))
    for n in range(0, len(rows), 4):
        part = rows[n:n + 4]
        W = max(max(t.width, b.width) for _, t, b in part) + 90
        sheet = Image.new("RGB", (W, len(part) * (2 * BAND + 12)), (40, 40, 40))
        d = ImageDraw.Draw(sheet)
        for j, (c, t, b) in enumerate(part):
            y0 = j * (2 * BAND + 12)
            sheet.paste(t, (90, y0))
            sheet.paste(b, (90, y0 + BAND + 4))
            d.text((4, y0 + 4), f"{c} top", fill=(255, 230, 0))       # PIL の既定の書体は日本語を描けない
            d.text((4, y0 + BAND + 8), f"{c} bottom", fill=(255, 230, 0))
        fn = OUT / f"strips_{qa_dir}_{n // 4 + 1}.jpg"
        sheet.save(fn, quality=92)
        print("strips", fn.name, [c for c, _, _ in part], sheet.size)
    sys.exit(0)
order = [n for n in args] or [f"{c}_095" for c in CUTS]
for n in range(0, len(order), 6):
    sheet = Image.new("RGB", (1280, 1080), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for j, name in enumerate(order[n:n + 6]):
        p = SRC / f"at_{name}.jpg"
        if not p.exists():
            print("無い", p.name)
            continue
        im = Image.open(p).convert("RGB").resize((640, 360), Image.LANCZOS)
        x, y = (j % 2) * 640, (j // 2) * 360
        sheet.paste(im, (x, y))
        d.rectangle((x, y, x + 120, y + 16), fill=(0, 0, 0))
        d.text((x + 4, y + 2), name, fill=(255, 230, 0))
    fn = OUT / f"sheet_{qa_dir}_{n // 6 + 1}.jpg"
    sheet.save(fn, quality=90)
    print("sheet", fn.name, order[n:n + 6])
