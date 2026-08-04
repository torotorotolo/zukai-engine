# -*- coding: utf-8 -*-
"""解説書（`jtsb_kaisetsu.pdf`）から図と表を切り出す（2026-08-04）。

■ なぜ `extract_photos.py` が使えないか
  あちらは**スキャンPDFに埋め込まれたビットマップ**を取り出す道具で、
  キャプションのテキスト層から番号を読んで名前を付けている。
  解説書は**テキストPDF**で、**表は罫線と文字で描かれていて画像が1枚も無い**
  （`page.get_images()` は表のページで0枚を返す）。
  → ページを**描画してから矩形で切る**。切る場所は下の CROP に置く。

■ 🔴 推定で切らない
  矩形は 110dpi で描いたページを見て測った。**切ったら必ず目で見る**
  （制作ルール §3「切ったら切り出した画像を目で見る」）。
  `--contact` で 12 枚を1枚に並べた確認用シートを作る。

■ 権利
  報告書と同じ **PDL1.0**（運輸安全委員会 公共データ利用規約）。
  出典は「解説書 表1」のように**図表の番号まで**画面に出す（`scene_jiko.CREDIT`）。
  加工した旨は `ref/ja123/INDEX.md` と `ref/CREDITS.md` に書く。

使い方:
    python tools/extract_kaisetsu.py            # ref/ja123/ へ書き出す
    python tools/extract_kaisetsu.py --contact  # 確認用の並べたシートも作る
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import fitz
from PIL import Image

HERE = Path(__file__).parent.parent
OUT = HERE / "ref" / "ja123"
# 元PDFは一時領域だと消えるので、Desktop の控えを先に見る。
SRC = [Path(r"C:\Users\konar\Desktop\ja123_src\pdf\jtsb_kaisetsu.pdf"),
       HERE / "ref" / "src" / "jtsb_kaisetsu.pdf"]

DPI = 300
LONG_MAX = 1800          # 長辺の上限（1ビットのスキャンではないので縮小は控えめ）

# (出力名, ページ, 切り出し矩形 pt(x0,y0,x1,y1), 画面に出す出典, 何の図か)
CROP = [
    # 🔴 矩形は `page.get_drawings()` の外接で実測してから詰めた（推定で置かない）。
    #    ただし外接には**すぐ下の本文ブロック**まで入るので、上限は目視で切っている。
    # ⚠️ 名前は `scene_jiko.kaisetsu_credit()` が読む。`kz009` → 図9／`kh001` → 表1。
    #    番号を持たない2枚だけ `KAI_EXTRA` に登録してある。**名前を変えたら向こうも直す。**
    ("kh001.png",  7, (68, 55, 545, 232),
     "解説書 表1", "急減圧時の機内現象についての実際の体験と事故前の認識（推定）"),
    ("kh002.png",  7, (68, 448, 545, 690),
     "解説書 表2", "急減圧後、客室内の高度が10,000ftに上昇するまでの時間（概算）"),
    ("kz001.png",  8, (68, 112, 545, 494),
     "解説書 図1", "急減圧後、客室（与圧室）内の圧力の推移"),
    ("kz002.png",  9, (68, 272, 545, 472),
     "解説書 図2", "川の例（流れの断面積と速さ）"),
    ("kz009.png", 14, (95, 212, 530, 542),
     "解説書 図9", "温度回復のシミュレーション"),
    ("k_keiki.png", 23, (105, 70, 548, 245),
     "解説書 図11・図12", "当時の計器（距離表示と方位表示）"),
    ("kh003.png", 23, (68, 326, 548, 664),
     "解説書 表3", "各航空機の測位結果（日没 12日18:40／日出 13日04:55）"),
    ("kz013.png", 24, (68, 56, 545, 418),
     "解説書 図13", "航空機による墜落場所の特定図"),
    ("kh004.png", 28, (105, 378, 508, 508),
     "解説書 表4", "サイド・スキャン・ソナーの性能"),
    ("kz018.png", 28, (332, 536, 545, 732),
     "解説書 図18", "えい航式深海カメラの航跡"),
    ("kh005.png", 29, (68, 310, 545, 568),
     "解説書 表5", "推定される落下物"),
    ("k_camera.png", 29, (100, 50, 262, 132),
     "解説書 10.(3)", "えい航式深海カメラの諸元（速度・高度・撮影幅）"),
]


def src_pdf():
    for p in SRC:
        if p.exists():
            return p
    raise SystemExit(
        "🔴 jtsb_kaisetsu.pdf が見つからない。\n"
        "   jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html から取り直して\n"
        f"   {SRC[0]} に置く。")


def main(contact=False):
    pdf = src_pdf()
    print(f"元PDF: {pdf}")
    doc = fitz.open(str(pdf))
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for name, page_no, rect, credit, what in CROP:
        page = doc[page_no - 1]
        clip = fitz.Rect(*rect)
        if not clip.intersects(page.rect):
            print(f"  ✗ {name}: 矩形がページの外 {rect}")
            continue
        pix = page.get_pixmap(dpi=DPI, clip=clip)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if max(im.size) > LONG_MAX:
            z = LONG_MAX / max(im.size)
            im = im.resize((int(im.width * z), int(im.height * z)),
                           Image.LANCZOS)
        im.save(OUT / name)
        made.append((name, im, credit, what))
        print(f"  ✓ {name:14s} p{page_no:<3d} {im.width:4d}x{im.height:<4d}  {what}")

    if contact and made:
        cols, cw = 3, 620
        rows = (len(made) + cols - 1) // cols
        thumbs = []
        for _n, im, _c, _w in made:
            z = cw / im.width
            thumbs.append(im.resize((cw, max(1, int(im.height * z))),
                                    Image.LANCZOS))
        rh = [max(t.height for t in thumbs[r * cols:(r + 1) * cols])
              for r in range(rows)]
        sheet = Image.new("RGB", (cols * cw, sum(rh)), "white")
        y = 0
        for r in range(rows):
            x = 0
            for t in thumbs[r * cols:(r + 1) * cols]:
                sheet.paste(t, (x, y))
                x += cw
            y += rh[r]
        # 確認用シートは成果物なので out/ へ（ref/ は .gitignore の許可制）
        (HERE / "out").mkdir(exist_ok=True)
        cpath = HERE / "out" / "kaisetsu_contact.png"
        sheet.save(cpath)
        print(f"\n  確認用シート: {cpath}  {sheet.width}x{sheet.height}")
        print("  🔴 これを目で見てから当てる（推定で通さない）")
    print(f"\n✓ {len(made)} 枚を {OUT} へ書き出した")
    return 0


if __name__ == "__main__":
    sys.exit(main("--contact" in sys.argv))
