# -*- coding: utf-8 -*-
"""18本目 ⑤b-8（2026-10-05）：Actions の試し焼き（`out/jiko/qa_ep18_b8/`）を 640px のシート（2列×3行）に並べる。
   python qa_out/ep18_b8/make_sheets.py [qa_ep18_b8] → qa_out/ep18_b8/sheet_<qa の置き場>_<n>.jpg（1280×1080・各コマの左上に名前）
     並び＝c104（頁の印が出そろう 0.30・2枚目の頁の印 0.55・決め所＝qa の静止画 0.92）→ c105（尻の頁の印の途中 0.62・出そろい 0.92）
     → 決め所16（0.92）→ パネル3（0.92）→ 地図2（c402 0.92・ca02 の測る線の途中 0.75 と 0.92）
   python qa_out/ep18_b8/make_sheets.py at → 試し焼きの `at` の引数（Actions の入力にそのまま貼る）
   python qa_out/ep18_b8/make_sheets.py marks [qa_dir] → 頁の上の印（c104 の2枚・c105）を原寸の帯に（額の中の印の行だけ）
   （⑤b-7c の qa_out/ep18_b7c/make_sheets.py を写した）"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
QUOTE = "c210 c317 c406 c417 c505 c521 c619 c625 c715 c810 c815 c913 ca16 ca23 cb13 cb17".split()
PANEL = "c113 c214 c901".split()
MAPS = "c402 ca02".split()
# 本体の尺の割合（c104 12.73秒＝1枚目の印が出そろう 3.42秒・2枚目が着く 5.04秒・2枚目の印 6.51秒・決め所へ 8.0秒／c105 9.65秒＝
#   尻の頁の印 5.38〜8.25秒／ca02 7.52秒＝測る線 4.6〜7.0秒）＝scene_jiko の秒から（⑤b-8 に機械で出した）
AT = [("c104", 0.30), ("c104", 0.55), ("c105", 0.62), ("ca02", 0.75)]
args = [a for a in sys.argv[1:]]
qa_dir = next((a for a in args if a.startswith("qa_")), "qa_ep18_b8")
args = [a for a in args if not a.startswith("qa_")]
if args and args[0] == "at":
    by = {}
    for c, t in AT:
        by.setdefault(c, []).append(f"{t:g}")
    print(",".join(f"{c}:{'/'.join(ts)}" for c, ts in by.items()))
    sys.exit(0)
base = ROOT / "out" / "jiko" / qa_dir
hit = next(iter(base.rglob("at_*.jpg")), None)
SRC = hit.parent if hit else base
CUT = next(iter(base.rglob("cut_c104.jpg")), None)
CSRC = CUT.parent if CUT else base


def frames():
    out = [(f"{c} {t:.2f}", SRC / f"at_{c}_{int(round(t * 100)):03d}.jpg") for c, t in AT[:3]]
    out += [(f"{c} 0.92", CSRC / f"cut_{c}.jpg") for c in ["c104", "c105"] + QUOTE + PANEL]
    out += [(f"{c} {t:.2f}", SRC / f"at_{c}_{int(round(t * 100)):03d}.jpg") for c, t in AT[3:]]
    out += [(f"{c} 0.92", CSRC / f"cut_{c}.jpg") for c in MAPS]
    return out


if args and args[0] == "marks":
    sys.path.insert(0, str(ROOT / "tools"))
    import scene_jiko as S  # noqa: E402  額の箱（本番と同じ式）
    rows = []
    for c, t, key, (y0, y1) in (("c104", 0.30, "c104~i", (0.0, 0.40)), ("c104", 0.55, "c104~o", (0.0, 0.35)),
                                ("c105", 0.92, "c105~t", (0.0, 0.35))):
        p = (CSRC / f"cut_{c}.jpg") if t == 0.92 else (SRC / f"at_{c}_{int(round(t * 100)):03d}.jpg")
        x, y, w, h = S.photo_box(S.ins_specs()[key])
        im = Image.open(p).convert("RGB")
        rows.append(im.crop((x, y + int(h * y0), x + w, y + int(h * y1))))
    W = max(r.width for r in rows)
    sheet = Image.new("RGB", (W, sum(r.height + 6 for r in rows)), (40, 40, 40))
    yy = 0
    for r in rows:
        sheet.paste(r, (0, yy))
        yy += r.height + 6
    f = OUT / f"marks_{qa_dir}.jpg"
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
