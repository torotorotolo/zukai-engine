# -*- coding: utf-8 -*-
"""640px のシート（1コマ 640×360・2列×3行＝1枚に6コマ）を作る（16本目 ⑤b-6b で書いた・⑤b-7 以降も使う）。
試し焼き（Actions の成果物）を**全数**見るための縮小シート。⚠️ シートで決めてはいけない3型（図の比例・小さな点・札の切れ）と
私人の顔・名前は原寸で見る（記憶 feedback-sheet-cannot-judge-three-types・ルール §5b-97）。

    python qa_out/at_sheet.py <成果物のフォルダ> <出力のフォルダ> <名前1> <名前2> ...
      名前は「qa_c705」「at_c813_30」のようなファイル名の頭（.jpg／.png を探す・下のフォルダも探す）。
      左上に名前を焼く（どのコマか取り違えない）。無いコマは赤字で「無い：名前」。
    python qa_out/at_sheet.py --seen <台帳.tsv> <見た画像のパス> [何として見たか]
      見た画像を台帳に1行足して、何枚目かを出す（画像は1チャット40枚まで＝手で数えない）。
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, COLS, ROWS, GAP = 640, 360, 2, 3, 8


def find(src, name):
    for ext in (".jpg", ".png", ".jpeg"):
        hits = sorted(Path(src).rglob(name + ext))
        if hits:
            return hits[0]
    return None


def sheets(src, out, names):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    except OSError:
        font = ImageFont.load_default()
    per = COLS * ROWS
    made, missing = [], []
    for si in range(0, len(names), per):
        sheet = Image.new("RGB", (COLS * W + (COLS + 1) * GAP, ROWS * H + (ROWS + 1) * GAP), (40, 40, 40))
        d = ImageDraw.Draw(sheet)
        for i, nm in enumerate(names[si:si + per]):
            p = find(src, nm)
            x, y = GAP + (i % COLS) * (W + GAP), GAP + (i // COLS) * (H + GAP)
            if not p:
                missing.append(nm)
                d.text((x + 10, y + 10), f"無い：{nm}", fill=(255, 80, 80), font=font)
                continue
            im = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)
            sheet.paste(im, (x, y))
            d.rectangle((x, y, x + 12 + d.textlength(nm, font=font), y + 30), fill=(0, 0, 0))
            d.text((x + 6, y + 3), nm, fill=(255, 255, 0), font=font)
        fn = out / f"sheet_{si // per + 1:02d}.jpg"
        sheet.save(fn, quality=90)
        made.append((fn, names[si:si + per]))
    for fn, nms in made:
        print(fn, " ".join(nms))
    if missing:
        print("無いコマ:", " ".join(missing))
    return made, missing


def seen(ledger, path, what=""):
    with open(ledger, "a", encoding="utf-8") as f:
        f.write(f"{path}\t{what}\n")
    n = sum(1 for _ in open(ledger, encoding="utf-8"))
    print(f"台帳 {Path(ledger).name}：{n} 枚目")
    return n


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--seen":
        seen(a[1], a[2], a[3] if len(a) > 3 else "")
    elif len(a) >= 3:
        sheets(a[0], a[1], a[2:])
    else:
        print(__doc__)
        sys.exit(2)
