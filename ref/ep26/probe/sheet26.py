# 26本目 ②：見本帳（1ます 640×440・2列×3行）を作る。ますの下は番号・撮影日・権利・原寸だけ（題名は入れない＝乗客の名前を絵に焼かない）
# 使い方: python -P ref/ep26/probe/sheet26.py <pick26.json> <縮小版のフォルダ> <出力フォルダ>
import json, os, sys

from PIL import Image, ImageDraw, ImageFont

CW, CH, CAP, GAP = 640, 440, 30, 8


def font(size):
    for f in ("C:/Windows/Fonts/meiryo.ttc", "C:/Windows/Fonts/msgothic.ttc", "C:/Windows/Fonts/arial.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def main():
    picks = json.load(open(sys.argv[1], encoding="utf-8"))
    tdir, out = sys.argv[2], sys.argv[3]
    os.makedirs(out, exist_ok=True)
    files = {os.path.splitext(f)[0]: f for f in os.listdir(tdir) if not f.endswith(".tsv")}
    fnt = font(18)
    rows = []
    for s in range(0, len(picks), 6):
        part = picks[s:s + 6]
        W = 2 * CW + 3 * GAP
        H = 3 * (CH + CAP) + 4 * GAP
        sheet = Image.new("RGB", (W, H), (40, 40, 40))
        d = ImageDraw.Draw(sheet)
        for k, r in enumerate(part):
            x = GAP + (k % 2) * (CW + GAP)
            y = GAP + (k // 2) * (CH + CAP + GAP)
            if r["key"] in files:
                im = Image.open(os.path.join(tdir, files[r["key"]])).convert("RGB")
                im.thumbnail((CW, CH))
                sheet.paste(im, (x + (CW - im.width) // 2, y + (CH - im.height) // 2))
            else:  # まだ取れていない点（見本帳を組み直す）
                d.text((x + 20, y + 20), "未取得", fill=(255, 80, 80), font=fnt)
            cap = f"{r['key']}  {str(r.get('date') or '')[:10]}  {r['w']}x{r['h']}  {str(r.get('lic') or '')[:14]}"
            d.rectangle([x, y + CH, x + CW, y + CH + CAP], fill=(255, 255, 255))
            d.text((x + 6, y + CH + 4), cap, fill=(0, 0, 0), font=fnt)
        n = s // 6 + 1
        p = os.path.join(out, f"sheet{n:02d}.png")
        sheet.save(p)
        rows.append(f"sheet{n:02d}\t" + ",".join(r["key"] for r in part))
    with open(os.path.join(out, "sheets.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("sheet\tkeys\n" + "\n".join(rows) + "\n")
    print("sheets", len(rows), "->", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
