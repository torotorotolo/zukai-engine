# -*- coding: utf-8 -*-
"""焼いた絵から**答えの語**を切り出して1枚に並べ、**語の墨の高さ**も測る（台帳 §AC）。

  python -u qa_out/kb_ac_word.py 出力.jpg c723:線1本ずつ c212:第18・第20径間 ...
  python -u qa_out/kb_ac_word.py 出力.jpg --src out/jiko/qa_keybridge-r09 c517:落ちた

■ 何のためか
  Dela に入る漢字の「つぶれ」は機械では決まらない（§Z-1-3）。判定は**3倍の切り出しを目で見て**決める。
  この道具は、その切り出しを**本番と同じ座標**で作り、比べるための数（墨の高さ）を添えるだけ。
  ⚠️ 墨の高さで 🔴／✅ を決めない。§AC の規則は「同じ字に台帳の判定があれば、✅ の最小の
     墨の高さを床にする」「無ければ3倍で、文脈なしに字が決まるか」。

■ 測り方
  座標は `scene_jiko.build_layers()` が作る**本番の SVG** の `<text>`（x・y・font-size・text-anchor）から取る
  （[[feedback-gates-must-share-the-production-geometry]]）。語の幅は「級数×字数×1.02」の見積もり。
  墨の高さ＝ベースラインから 0.4×級数 上の行を基点に、**語の色（その行でいちばん明るい画素）±70** の
  点が3つ以上ある行が上下に続く所まで。
  ⚠️ **明るい写真の上の語は測れない**（`c905` で 851px と出た＝写真と縁取りを語に数えた）。
     そのときは数を捨てて絵で決める。
  ⚠️ 同じ語が SVG に2つ以上あると最初の1つを取る。

  対照（2026-09-11・r08）：`c723`「線1本ずつ」76px → 62px（🔴）／`c108`「3径間」88px → 68px（✅）／
  `c212`「第18・第20径間」66px → 50px（台帳で「読める」の最小）
"""
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')
ATTR = re.compile(r'([\w:-]+)="([^"]*)"')


def ink_height(arr, box, y, fs):
    yc = int(y - 0.4 * fs)
    band = arr[yc, box[0]:box[2]]
    ref = band[band.sum(1).argmax()]

    def ink(yy):
        return int((np.abs(arr[yy, box[0]:box[2]] - ref).max(1) < 70).sum())

    top = bot = yc
    while top > 0 and ink(top - 1) >= 3:
        top -= 1
    while bot < arr.shape[0] - 1 and ink(bot + 1) >= 3:
        bot += 1
    return bot - top + 1


def main(argv):
    out = Path(argv[0])
    rest = argv[1:]
    src = ROOT / "out/jiko/qa_keybridge-r08"
    if "--src" in rest:
        i = rest.index("--src")
        src = ROOT / rest[i + 1]
        rest = rest[:i] + rest[i + 2:]
    targets = [a.split(":", 1) for a in rest]
    if not targets:
        raise SystemExit("🔴 対象が無い（カット:語 を1つ以上）")
    jobs, _ = S.build_layers(allow_missing=True)
    crops, missing = [], 0
    for cid, word in targets:
        hits = [(dict(ATTR.findall(m.group(1))), m.group(2))
                for k, svg in jobs.items() if k.split("_")[0] == cid
                for m in TEXT.finditer(svg) if word in m.group(2)]
        if not hits:
            print(f"🔴 {cid}「{word}」が本番の SVG に無い（0件と数えない）")
            missing += 1
            continue
        a, txt = hits[0]
        fs, x, y = float(a["font-size"]), float(a["x"]), float(a["y"])
        w = fs * len(txt) * 1.02
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[a.get("text-anchor", "start")]
        im = Image.open(src / f"cut_{cid}.jpg").convert("RGB")
        box = (int(max(0, x0 - 24)), int(max(0, y - fs * 1.05 - 16)),
               int(min(im.width, x0 + w + 24)), int(min(im.height, y + fs * 0.25 + 16)))
        h = ink_height(np.asarray(im).astype(int), box, y, fs)
        c = im.crop(box)
        sc = min(3.0, 1500 / c.width)
        c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
        lab = (f"{cid}「{txt}」 {fs:.0f}px {a.get('font-family')} 墨{h}px"
               f"{'（明るい地＝測れていない）' if h > fs * 1.5 else ''} ×{sc:.1f} box={box}")
        print(lab)
        crops.append((lab, c))
    if not crops:
        raise SystemExit(3)
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 26)
    except OSError:
        f = ImageFont.load_default()
    W = max(c.width for _, c in crops) + 20
    H = sum(c.height + 44 for _, c in crops) + 10
    sh = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(sh)
    yy = 6
    for t, c in crops:
        d.text((10, yy), t, fill=(200, 0, 0), font=f)
        yy += 36
        sh.paste(c, (10, yy))
        yy += c.height + 8
    sh.save(out, quality=95)
    print(f"■ {out} {sh.size}  ⚠️ 1枚の画像として数える")
    return 3 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
