# -*- coding: utf-8 -*-
"""18本目 ⑤b-7c（2026-10-05）：Actions の試し焼き（`out/jiko/qa_ep18_b7c/`）を 640px のシート（2列×3行）に並べる。
   python qa_out/ep18_b7c/make_sheets.py [qa_ep18_b7c] → qa_out/ep18_b7c/sheet_<qa の置き場>_<n>.jpg（1280×1080・各コマの左上に名前）
     並び＝記録映画21カット（左＝頭寄り at 0.15・右＝尻寄り qa の静止画 0.92＝ショットの中で絵が変わらないか）→ 頭の差し込み12（at 0.10）
     → 尻の差し込み3（at 0.95）・c102／c103 の本の側（qa の静止画）
   python qa_out/ep18_b7c/make_sheets.py at → 試し焼きの `at` の引数（Actions の入力にそのまま貼る）
   python qa_out/ep18_b7c/make_sheets.py strips [qa_dir] → 尻の差し込みの頁（c105・cb21）の額の上の端と下の端を原寸の帯に
   （⑤b-7b の qa_out/ep18_b7b/make_sheets.py を写した）"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FILM = "c117 c202 c212 c301 c506 c514 c515 c601 c607 c621 c701 ca01 ca03 ca07 ca08 ca09 ca12 cb01 cb07 cb14 cb19".split()
HEAD = "c102 c109 c114 c215 c220 c511 c805 c812 c903 c906 ca05 ca06".split()
TAIL = "c103 c105 cb21".split()
args = [a for a in sys.argv[1:]]
qa_dir = next((a for a in args if a.startswith("qa_")), "qa_ep18_b7c")
args = [a for a in args if not a.startswith("qa_")]
if args and args[0] == "at":
    print(",".join([f"{c}:0.15" for c in FILM] + [f"{c}:0.1" for c in HEAD] + [f"{c}:0.95" for c in TAIL]))
    sys.exit(0)
# 焼き直し（差分だけ）＝記録映画21カットの額装（0.5）＋頭の直した3カット（0.1）
FIX = [(c, 0.5) for c in FILM] + [(c, 0.1) for c in ("c102", "c903", "c906")]
if args and args[0] == "fixat":
    print(",".join(f"{c}:{t}" for c, t in FIX))
    sys.exit(0)
base = ROOT / "out" / "jiko" / qa_dir
hit = next(iter(base.rglob("at_*.jpg")), None)
SRC = hit.parent if hit else base
CUT = next(iter(base.rglob("cut_c117.jpg")), None)
CSRC = CUT.parent if CUT else base


def frames():
    if args and args[0] == "fix":
        return [(f"{c} {t:.2f}", SRC / f"at_{c}_{int(round(t * 100)):03d}.jpg") for c, t in FIX]
    out = []
    for c in FILM:
        out += [(f"{c} 0.15", SRC / f"at_{c}_015.jpg"), (f"{c} 0.92", CSRC / f"cut_{c}.jpg")]
    out += [(f"{c} 0.10", SRC / f"at_{c}_010.jpg") for c in HEAD]
    out += [(f"{c} 0.95", SRC / f"at_{c}_095.jpg") for c in TAIL]
    out += [(f"{c} 0.92", CSRC / f"cut_{c}.jpg") for c in ("c102", "c103")]
    return out


if args and args[0] == "strips":
    sys.path.insert(0, str(ROOT / "tools"))
    import scene_jiko as S  # noqa: E402  額の箱（本番と同じ式）
    BAND = 70
    rows = []
    for c in ("c105", "cb21"):
        p = SRC / f"at_{c}_095.jpg"
        x, y, w, h = S.photo_box(S.tail_spec(c))
        im = Image.open(p).convert("RGB")
        rows += [im.crop((x - 10, y - 10, x + w + 10, y - 10 + BAND)), im.crop((x - 10, y + h + 10 - BAND, x + w + 10, y + h + 10))]
    W = max(r.width for r in rows)
    sheet = Image.new("RGB", (W, sum(r.height + 6 for r in rows)), (40, 40, 40))
    yy = 0
    for r in rows:
        sheet.paste(r, (0, yy))
        yy += r.height + 6
    f = OUT / f"strips_{qa_dir}.jpg"
    sheet.save(f, quality=92)
    print(f.name, sheet.size)
    sys.exit(0)
fs = frames()
miss = [n for n, p in fs if not p.exists()]
if miss:
    print("🔴 無いコマ:", " ".join(miss))
fs = [(n, p) for n, p in fs if p.exists()]
for k in range(0, len(fs), 6):
    sheet = Image.new("RGB", (1280, 1080), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    for j, (n, p) in enumerate(fs[k:k + 6]):
        im = Image.open(p).convert("RGB").resize((640, 360), Image.LANCZOS)
        x0, y0 = (j % 2) * 640, (j // 2) * 360
        sheet.paste(im, (x0, y0))
        d.rectangle((x0, y0, x0 + 150, y0 + 22), fill=(0, 0, 0))
        d.text((x0 + 4, y0 + 4), n, fill=(255, 230, 120))
    f = OUT / f"sheet_{qa_dir}_{k // 6 + 1}.jpg"
    sheet.save(f, quality=90)
    print(f.name, len(fs[k:k + 6]))
print("コマ", len(fs), "／", len(frames()))
