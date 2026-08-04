# -*- coding: utf-8 -*-
"""事故調査報告書のスキャンページから、写真・付図を1枚ずつ切り出して**番号で名前を付ける**。

日航123便（62-2 JA8119）の日本語版分割PDFは 1ページ＝1枚の約400dpiスキャンだが、
**キャプションだけはテキスト層として入っている**。「写真‐１　墜落現場遠景(1)」を読み、
同じページで見つけた矩形に番号を割り当てる。

  p001.png  … 写真‐1        f012.png  … 付図‐12
  a1p01.png … 別添1 写真‐1  a1f03.png … 別添1 付図‐3

■ 🔴 4つの落とし穴（どれも実物を見て分かったこと）
  ① **明暗では分けられない。** 「暗い画素の割合」でも「純白でない画素」でも
     明るい写真を丸ごと取り逃す（スキャンが写真の明部を255に飛ばしている）。
     → 写真は**升目ごとの標準偏差**で探す。紙は平坦・写真は粒状。
  ② **付図（線画）は①では1枚も取れない。** 白地に線なので升目の大半が真っ白で、
     連結成分が砂粒に割れる。→ 図が1枚しかないページは**インクの外接矩形**で取る。
  ③ **ページに /Rotate が付いている。** 横位置の紙を縦に見せているので、
     描画すると本文が横倒しになり、番号の順も上下が逆になる。
     → **`set_rotation(0)` で回転を外してから**描画する。素の向きが本来の読み順で、
       写真も立った状態で出てくる（切ったあとに回す必要がない）。
  ④ **キャプションの中に別の番号が出てくる。**「写真‐９２に示す部位」「写真‐１０７で
     示したように」。行頭に来ているものだけを拾わないと、番号が1つ多くなって全部ずれる。

■ 使い方
    python tools/extract_photos.py <pdf...> --out <dir>

⚠️ **新しく作った物差しは最初ほぼ必ず間違っている。切り出した画像を必ず目で見る。**
"""
import argparse
import re
import sys
from pathlib import Path

import fitz
import numpy as np
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding="utf-8")

ZOOM = 5.05        # 400dpi のスキャンとほぼ等倍になる描画倍率
BLK = 32           # ばらつきを測る升目の大きさ（画素）
STD_MIN = 6.0      # この升目内標準偏差を超えたら「何か写っている」
MIN_W, MIN_H = 700, 500    # これ未満は写真でなく罫・ノンブル
# 矩形の中の埋まり具合。文字の塊は中がスカスカになる。
# 🔴 0.55 だと**平らな面が広い写真を落とす**（写真‐44 は 0.39、写真‐108 は 0.50）。
#    落ちたぶんだけ番号が繰り上がって**別の写真に前の番号が付く**ので、
#    「取れなかった」で済まず、静かに間違ったものが出る。文字は先に白で潰してあるので
#    ここは低くしてよい。
FILL_MIN = 0.32
# 外へ広げる升目の数。🔴 **1でもキャプションが写り込む。**
#    探すときは文字を白で潰しているので矩形は写真にぴったり付くが、そこから32px広げると
#    すぐ上の行の下ぶくらみを拾う（p029 p030 p045 p047 で実際に写り込んだ）。
#    0 にしたうえで、さらに clip_text() で文字の帯を機械的に外す。
PAD = 0
INK = 200                  # これより暗ければインク（付図の外接矩形用）

# 「写真‐１２３」「付図‐４」「別添1 付図‐３」。ハイフンは U+2010、数字は全角。
ZEN = str.maketrans("０１２３４５６７８９", "0123456789")
# ⚠️ 番号のうしろに**空白か行末**を要求する。これが無いと「写真‐９２に示す部位」
#    「写真‐１０７で示したように」という**説明文の中の参照**まで拾い、番号が1つ増えて
#    そのページ以降の割り当てが全部ずれる（④）。
CAP = re.compile(r"^(?:別添\s*([0-9０-９]+)\s*)?(写真|付図)\s*[‐\-－ー―]\s*([0-9０-９]+)"
                 r"(?=[\s　]|$)")


def captions(page):
    """キャプションを [(bbox, 種別, 番号, 別添番号)] で返す。**行頭のものだけ**拾う。

    ⚠️ **行の単位で見る。**「1ブロック＝1キャプション」と決め打つと、
       写真‐1 と 写真‐2 が同じブロックに入っているページ（ja_06 p012 ほか）で
       2枚目を丸ごと取り逃す。逆にブロックの全行を拾うと説明文の中の参照を拾うので、
       それは CAP の「番号のうしろは空白か行末」で切る。
    """
    out = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            text = "".join(s["text"] for s in ln["spans"]).strip()
            m = CAP.match(text)
            if m:
                out.append((tuple(ln["bbox"]), m.group(2),
                            int(m.group(3).translate(ZEN)),
                            int(m.group(1).translate(ZEN)) if m.group(1) else 0))
    out.sort(key=lambda c: (round(c[0][1] / 40), c[0][0]))     # 読み順（上→下、左→右）
    return out


def name_of(kind, num, annex):
    return f"{'a%d' % annex if annex else ''}{'p' if kind == '写真' else 'f'}{num:03d}"


def boxes_from(mask):
    """マスクの連結成分を (x0,y0,x1,y1,升目数) で返す（4近傍・素朴な flood fill）。"""
    H, W = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    for y in range(H):
        for x in range(W):
            if not mask[y, x] or seen[y, x]:
                continue
            stack, n = [(y, x)], 0
            seen[y, x] = True
            y0 = y1 = y
            x0 = x1 = x
            while stack:
                cy, cx = stack.pop()
                n += 1
                y0, y1 = min(y0, cy), max(y1, cy)
                x0, x1 = min(x0, cx), max(x1, cx)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            out.append((x0, y0, x1, y1, n))
    return out


def photo_boxes(a):
    """写真の矩形 (x0,y0,x1,y1) を画素座標で返す。読み順（上→下、左→右）。"""
    h, w = a.shape
    H, W = h // BLK, w // BLK
    b = a[:H * BLK, :W * BLK].reshape(H, BLK, W, BLK).astype(np.float32)
    m = b.mean(axis=(1, 3))
    std = np.sqrt(np.maximum((b * b).mean(axis=(1, 3)) - m * m, 0))
    res = []
    for x0, y0, x1, y1, n in boxes_from(std >= STD_MIN):
        px0, py0 = max((x0 - PAD) * BLK, 0), max((y0 - PAD) * BLK, 0)
        px1, py1 = min((x1 + 1 + PAD) * BLK, w), min((y1 + 1 + PAD) * BLK, h)
        if px1 - px0 < MIN_W or py1 - py0 < MIN_H:
            continue
        if n / max((x1 - x0 + 1) * (y1 - y0 + 1), 1) < FILL_MIN:
            continue
        res.append((px0, py0, px1, py1))
    res.sort(key=lambda r: (round(r[1] / 400), r[0]))
    return res


def ink_box(a, pad=24):
    """インクの外接矩形。付図（線画）はこれで取る。"""
    ys, xs = np.where(a < INK)
    if not len(ys):
        return None
    return (max(int(xs.min()) - pad, 0), max(int(ys.min()) - pad, 0),
            min(int(xs.max()) + pad, a.shape[1]), min(int(ys.max()) + pad, a.shape[0]))


def clip_text(box, tboxes):
    """矩形の上端・下端にかかっている**文字の帯**を外す。

    🔴 報告書のキャプションは写真のすぐ上に組まれていて、切り出しの上端に
       「リベットの破断状況」のような**前の写真の説明の続き**が1行残る。
       焼いたあとの画面では、こちらが付けた注記の真横に報告書の文が並ぶことになる
       （タイタン号で英字が焼き込まれていたのと同じ事故）。
    """
    x0, y0, x1, y1 = box
    for tx0, ty0, tx1, ty1 in tboxes:
        if tx1 <= x0 or tx0 >= x1:              # 横に重なっていない文字は関係ない
            continue
        band = (y1 - y0) * 0.25
        if y0 < ty1 <= y0 + band:
            y0 = min(ty1 + 4, y1 - 1)
        if y1 - band <= ty0 < y1:
            y1 = max(ty0 - 4, y0 + 1)
    return (x0, y0, x1, y1)


def union(boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def assign(caps, boxes):
    """キャプション（写真の**上**にある）に、その下で最も近い矩形を割り当てる。

    🔴 **caps の bbox は画素に直してから渡すこと。**
       `get_text` が返すのはポイント（1/72インチ）で、矩形は画素。単位を混ぜると
       「横に重なっているか」の判定が必ず外れ、**下の行の写真が丸ごと入れ替わる**。
       しかもエラーは出ず、警告も出ない（写真‐3 と 写真‐4 が入れ替わっていた）。
    """
    out, used = [], set()
    for i, (bb, *_rest) in enumerate(caps):
        cx = (bb[0] + bb[2]) / 2
        cands = [j for j, b in enumerate(boxes)
                 if j not in used and b[3] > bb[3] and b[0] - 40 <= cx <= b[2] + 40]
        if not cands:
            cands = [j for j, b in enumerate(boxes) if j not in used and b[3] > bb[3]]
        if not cands:
            out.append(None)
            continue
        j = min(cands, key=lambda j: (boxes[j][1] - bb[3], abs((boxes[j][0] + boxes[j][2]) / 2 - cx)))
        used.add(j)
        out.append(j)
    return out, [j for j in range(len(boxes)) if j not in used]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--out", default="photos")
    ap.add_argument("--zoom", type=float, default=ZOOM)
    # 🔴 **1ビット（2値）のスキャンなので、原寸のまま画面に出してはいけない。**
    #    中間調が1階調も無く、濃淡はすべて誤差拡散ディザ（網点）なので、
    #    1920px に伸ばすと砂目がそのまま出る（2026-08-03 に実写して確認）。
    #    縮小＋わずかなぼかしで**ディザが階調に戻り、写真として読める**。
    #    ⚠️ 縮小版を見て「使える」と判断してはいけない、の裏返しで、
    #      **出すときは必ず縮めてから出す**。額装パネルの幅の上限が 1200px なので
    #      ここで 1200 に落としておく（ファイルも 1/3 になる）。
    ap.add_argument("--cap", type=int, default=0, help="長辺の上限（0で原寸）")
    ap.add_argument("--blur", type=float, default=0.0, help="ディザをほどくぼかし半径")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    got, warn = {}, []

    for pdf in args.pdfs:
        d = fitz.open(pdf)
        for pno in range(len(d)):
            page = d[pno]
            page.set_rotation(0)                    # 🔴 回転を外す（③）
            caps = captions(page)
            if not caps:
                continue
            z = args.zoom
            pm = page.get_pixmap(matrix=fitz.Matrix(z, z), colorspace=fitz.csGRAY)
            im = Image.frombytes("L", (pm.width, pm.height), pm.samples)
            del pm
            a = np.asarray(im).copy()
            # テキスト層（キャプション・ノンブル）は白で塗り潰してから探す
            tboxes = []
            for b in page.get_text("blocks"):
                x0, y0, x1, y1 = (int(v * z) for v in b[:4])
                a[max(y0 - 6, 0):y1 + 6, max(x0 - 6, 0):x1 + 6] = 255
                tboxes.append((x0, y0, x1, y1))
            tag = f"{Path(pdf).stem}p{pno + 1:03d}"
            caps = [(tuple(v * z for v in c[0]),) + tuple(c[1:]) for c in caps]
            boxes = photo_boxes(a)
            if len(caps) == 1:
                # 図が1枚のページ。線画も多パネルの顕微鏡写真もここで1枚にまとめる（②）
                box = union(boxes) if boxes else ink_box(a)
                pairs = [(caps[0], box)] if box else []
                if not box:
                    warn.append(f"{tag}: {name_of(*caps[0][1:])} で何も見つからない")
            else:
                idx, left = assign(caps, boxes)
                pairs = [(c, boxes[j]) for c, j in zip(caps, idx) if j is not None]
                for c, j in zip(caps, idx):
                    if j is None:
                        warn.append(f"{tag}: {name_of(*c[1:])} に当たる矩形が無い")
                for j in left:
                    warn.append(f"{tag}: 余った矩形 {boxes[j]}")
                # ★割り当てそのものの検算。キャプションの中心は、その写真の真上にある。
                #   外れていたら単位か並び順を間違えている（実際に写真‐3/4 が入れ替わった）。
                for c, box in pairs:
                    cx = (c[0][0] + c[0][2]) / 2
                    if not box[0] - 60 <= cx <= box[2] + 60:
                        warn.append(f"{tag}: {name_of(*c[1:])} の札が写真の真上に無い"
                                    f"（札 x={cx:.0f} / 写真 x={box[0]}〜{box[2]}）")
            for cap, box in pairs:
                crop = im.crop(clip_text(box, tboxes))
                if args.cap:
                    crop.thumbnail((args.cap, args.cap), Image.LANCZOS)
                if args.blur:
                    crop = crop.filter(ImageFilter.GaussianBlur(args.blur))
                n = name_of(*cap[1:])
                if args.cap or args.blur:
                    crop.save(out / f"{n}.jpg", quality=88, optimize=True)
                else:
                    crop.save(out / f"{n}.png")
                got[n] = (tag, crop.width, crop.height)
            del a, im
        d.close()

    for n in sorted(got):
        t, w, h = got[n]
        print(f"{n:>8}  {w:>5}x{h:<5}  {t}")
    print(f"\n切り出し {len(got)} 枚 → {out}")
    for m in warn:
        print("⚠️ " + m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
