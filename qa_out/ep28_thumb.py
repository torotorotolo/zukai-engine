# -*- coding: utf-8 -*-
"""28本目 ⑥：サムネ（11-03 カズヤくん「八田與一の動画と同様のデザインに変更」「CM044の看板をアップにした写真」「全体的にもっと華やかに。写真は看板のみ切り抜きではなく、背景も込み」）。

型＝27本目の k5（`qa_out/ep27_thumb.py`）の並び＝字なしのトラテープ・左に赤い名前（Noto Serif JP Black）・その下に白の1行・右下に黄の1句。
顔の代わりに CM044（CC BY 3.0・`ref/ep28/cm044.jpg`）の看板を背景ごと全面に敷く。d3＝いまの本線。a〜b2＝切り抜きの版・c1 c2 d1 d2＝全面の途中（比べるために残す）。
⚠️ ルール §B2-11 ③「ロゴ単体は使わない」とぶつかる＝選択肢にその旨を書いて聞いた上でのカズヤくんの選び（この回の決め）。CC BY＝概要欄に作者・ライセンス・改変（切り出し・左の一部を反転してつなぐ・明るさ・彩度・文字）を書く。

    python -P qa_out/ep28_thumb.py --recut           … 看板を切り抜き直す（out/thumb/ep28/cm044_sign.png＝git の外）
    python -P qa_out/ep28_thumb.py --kinds=c1,d1     … 焼いて out/thumb/ep28/ep28_T_<kind>.png・並べ cmp_<kinds>.jpg（640px と 210px）
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter, ImageOps

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "qa_out"))
import ep27_thumb as E  # noqa: E402

T = E.T
W, H = E.W, E.H
SRC = HERE / "ref" / "ep28" / "cm044.jpg"
OUTD = HERE / "out" / "thumb" / "ep28"
CUT = OUTD / "cm044_sign.png"
# 看板の外周（800px に縮めた見取りで読んだ点＝元の写真は ×2.4）。GrabCut の種にする＝内は前景・外は背景
POLY = [(206, 398), (262, 262), (606, 151), (624, 150), (634, 164), (625, 200), (562, 345), (520, 378), (232, 422), (210, 415)]
FONT = "NotoSerifJP-Black.woff2"
RED = "#f60404"

# 焼く案： (看板の倍率, 看板の左上 x, y, 名前, 名前の枠〈上・下・左・右〉, 白の行, 黄の1句, 黄の字の大きさ)
KINDS = {
    "a": dict(s=0.66, x=620, y=66, name="タイムズカー", band=(196, 424, 40, 800), white="情報漏洩662万件", yellow="なぜ免許証を7年も？", ys=108),
    "b": dict(s=0.66, x=620, y=66, name="タイムズカー", band=(196, 424, 40, 800), white="免許証の画像146万件", yellow="なぜ退会後も7年？", ys=112),
    # 2版＝看板を右下へ（字が T に掛かる所を減らす）・字を上へ・看板を明るく（SIGN_ADJ）
    "a2": dict(s=0.66, x=668, y=92, name="タイムズカー", band=(172, 396, 40, 780), white="情報漏洩662万件", yellow="なぜ免許証を7年も？", ys=108),
    "b2": dict(s=0.66, x=668, y=92, name="タイムズカー", band=(172, 396, 40, 780), white="免許証の画像146万件", yellow="なぜ退会後も7年？", ys=112),
}
SIGN_ADJ = {"a2": (1.18, 1.15), "b2": (1.18, 1.15)}      # 看板の明るさ・彩度（1版の看板は暗く見えた＝写真の日陰）
# 🆕 3版（11-03 カズヤくん「全体的にもっと華やかに。写真は看板のみ切り抜きではなく、背景も込み」）＝写真を全面に敷く（切り抜かない）・色を鮮やかに。
#    photo＝(倍率, 写真の左上 x, y, 明るさ, コントラスト, 彩度)。x>0 のとき足りない左は写真を裏返してつなぐ（元の写真の左は壁と配管）
#    c1＝k5 と同じ並び（左に名前・右に看板）／c2＝名前を横いっぱいに大きく・白の行は左に2段
KINDS.update({
    "c1": dict(photo=(0.70, 221, -120, 1.12, 1.12, 1.45), name="タイムズカー", band=(172, 396, 40, 780),
               white=[("情報漏洩662万件", 40, 546, 76)], yellow="なぜ免許証を7年も？", ys=108),
    "c2": dict(photo=(0.78, 0, -115, 1.12, 1.12, 1.45), name="タイムズカー", band=(156, 346, 40, 1240),
               white=[("情報漏洩", 40, 462, 84), ("662万件", 40, 556, 84)], yellow="なぜ免許証を7年も？", ys=112),
})
# 🆕 4版（11-03 カズヤくん「c1で、看板をもう少し上に。写真をもっと明るく。『タイムズカー』の縁は黒で」）
#    photo の7番目＝ガンマ（1 未満で中間の明るさを持ち上げる＝白い看板を飛ばさずに暗い所が明るくなる）。rim＝名前の縁（色・半径・ぼかし）。fade＝下の黒ぼかし（始まりの y・中ほど・下端の濃さ）
KINDS["d1"] = dict(photo=(0.70, 221, -190, 1.18, 1.10, 1.40, 0.72), name="タイムズカー", band=(172, 396, 40, 780),
                   white=[("情報漏洩662万件", 40, 546, 76)], yellow="なぜ免許証を7年も？", ys=108,
                   rim=("#000000", 14.0, 1.0), fade=(590, 0.60, 0.88, 0.45))
# d2＝d1 で出た粗の直し：① 看板を上げたら下の小さな看板（駐車場の名前の赤い字）が黄の1句のすぐ上に出た＝黒ぼかしを 525 から・568 で濃く
#    ② 名前の「カー」の黒い縁が看板の「T」に掛かった＝名前を 22px・白の行を 20px 上へ ③ 明るくして薄れた黄色＝彩度 1.50
KINDS["d2"] = dict(KINDS["d1"], photo=(0.70, 221, -190, 1.18, 1.10, 1.50, 0.72), band=(150, 374, 40, 780),
                   white=[("情報漏洩662万件", 40, 526, 76)], fade=(525, 0.78, 0.92, 0.22))
# d3＝11-03 カズヤくん「d2で黄色字を左詰め」＝黄の1句を名前・白の行と同じ x=40 から始める
KINDS["d3"] = dict(KINDS["d2"], yleft=40)
RIM_K5 = ("#ffffff", 18.6, 5.4)      # k5 の等倍の白いぼかし
FADE_C = (560, 0.72, 0.92, 0.45)


def ground_full(c):
    """写真を全面に敷く（切り抜かない）。足りない左は裏返した写真でつなぐ。色は全体に鮮やかに（サムネだけ＝本編の写真の色は原本のまま）"""
    import numpy as np
    s, px, py, br, ct, co, *gm = c["photo"]
    im = Image.open(SRC).convert("RGB")
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    if py + im.height < H or px + im.width < W:
        raise SystemExit(f"🔴 写真が画面を覆わない：{im.size}・左上 ({px}, {py})")
    if gm:
        im = im.point([round(255 * (v / 255) ** gm[0]) for v in range(256)] * 3)
    im = ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(br)).enhance(ct)).enhance(co)
    base = Image.new("RGB", (W, H), "#050505")
    if px > 0:
        base.paste(ImageOps.mirror(im), (px - im.width, py))
    base.paste(im, (px, py))
    a = np.asarray(base.convert("L"))
    print(f"写真：{im.size}・明るさの平均 {a.mean():.0f}／255・白飛び（250 以上）{(a >= 250).mean():.1%}")
    return base


def cut_sign():
    """看板だけを切り抜く（透明つき PNG）。多角形を内へ縮めた所＝前景・外へ広げた所より外＝背景で GrabCut → 開いて閉じて縁をならす → 1.6px ぼかす"""
    if CUT.exists() and "--recut" not in sys.argv:
        return Image.open(CUT).convert("RGBA")
    import cv2
    import numpy as np
    from scipy import ndimage as nd
    rgb = np.asarray(Image.open(SRC).convert("RGB"))
    h, w = rgb.shape[:2]
    k = w / 800
    m0 = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m0).polygon([(x * k, y * k) for x, y in POLY], fill=255)
    poly = np.asarray(m0) > 0
    inner = nd.binary_erosion(poly, iterations=26)
    outer = nd.binary_dilation(poly, iterations=30)
    m = np.full((h, w), cv2.GC_BGD, np.uint8)
    m[outer] = cv2.GC_PR_BGD
    m[poly] = cv2.GC_PR_FGD
    m[inner] = cv2.GC_FGD
    cv2.grabCut(rgb[:, :, ::-1].copy(), m, None, np.zeros((1, 65)), np.zeros((1, 65)), 6, cv2.GC_INIT_WITH_MASK)
    fg = (m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD)
    lb, n = nd.label(fg)
    fg = nd.binary_fill_holes(lb == 1 + int(np.argmax(nd.sum(fg, lb, range(1, n + 1)))))
    st = nd.generate_binary_structure(2, 1)
    fg = nd.binary_fill_holes(nd.binary_closing(nd.binary_opening(fg, st, iterations=5), st, iterations=5))
    fg = nd.binary_erosion(fg, iterations=1)
    im = Image.fromarray(rgb).convert("RGBA")
    im.putalpha(Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)))
    ys, xs = np.nonzero(fg)
    box = (max(0, xs.min() - 6), max(0, ys.min() - 6), min(w, xs.max() + 7), min(h, ys.max() + 7))
    im = im.crop(box)
    OUTD.mkdir(parents=True, exist_ok=True)
    im.save(CUT)
    print(f"切り抜き 箱 {box}・{im.size}・面積 {int(fg.sum())}（多角形 {int(poly.sum())}）")
    return im


def name_svg(hx, text, band, rim):
    """27本目 k5 の名前と同じ作り＝字の形を座標で描く・ぼかしの縁（rim＝色・半径・ぼかし）・赤い字。枠いっぱいに字を並べる（hx.lay）"""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    top, bot, left, right = band
    gl, fs, sx = hx.lay(text, top, bot, left=left, right=right, rim=0, gap=2, font=FONT)
    hx.ink(text[0], FONT)
    gs, cmap, upm = hx._FT[FONT]
    ds = []
    for c, x, b, f, s, _, _ in gl:
        sp = SVGPathPen(gs)
        gs[cmap[ord(c)]].draw(TransformPen(sp, (f * s / upm, 0, 0, -f / upm, x, b)))
        ds.append(f'<path d="{sp.getCommands()}"/>')
    p = "".join(ds)
    col, r, sig = rim
    svg = (f'<defs><filter id="kg" x="0" y="0" width="{W}" height="{H}" filterUnits="userSpaceOnUse">'
           f'<feGaussianBlur stdDeviation="{sig:.2f}"/></filter></defs>'
           f'<g fill="{col}" stroke="{col}" stroke-width="{2 * r:.2f}" stroke-linejoin="round" filter="url(#kg)">{p}</g>'
           f'<g fill="{RED}" stroke="{RED}" stroke-width="3" stroke-linejoin="round">{p}</g>')
    return svg, fs, sx


def body(k):
    hx, _ = E._hx()
    c = KINDS[k]
    if "photo" in c:
        base = ground_full(c)
    else:
        sign = cut_sign()
        sg = sign.resize((round(sign.width * c["s"]), round(sign.height * c["s"])), Image.LANCZOS)
        rgb = sg.convert("RGB")
        if k in SIGN_ADJ:
            rgb = ImageEnhance.Color(ImageEnhance.Brightness(rgb).enhance(SIGN_ADJ[k][0])).enhance(SIGN_ADJ[k][1])
        base = Image.new("RGB", (W, H), "#050505")
        base.paste(rgb, (c["x"], c["y"]), sg.getchannel("A"))
    tape = ('<defs><pattern id="tiger" patternUnits="userSpaceOnUse" width="64" height="64" patternTransform="rotate(45)">'
            '<rect width="32" height="64" fill="#ffd60a"/><rect x="32" width="32" height="64" fill="#111111"/></pattern></defs>'
            '<g transform="rotate(-7 380 64)"><rect x="-80" y="30" width="1600" height="72" fill="url(#tiger)"/></g>')
    name, fs, sx = name_svg(hx, c["name"], c["band"], c.get("rim", RIM_K5))
    rows = c["white"] if isinstance(c["white"], list) else [(c["white"], 40, 546, 76)]
    yx, ya = (c["yleft"], "start") if "yleft" in c else (1240, "end")
    post = ("".join(f'<text x="{x}" y="{y}" font-family="NSJ" font-size="{fz}" fill="#ffffff" stroke="#000" stroke-width="14" '
                    f'stroke-linejoin="round" paint-order="stroke fill">{t}</text>' for t, x, y, fz in rows) +
            f'<text x="{yx}" y="692" text-anchor="{ya}" font-family="NSJ" font-size="{c["ys"]}" fill="#fbfb0e" stroke="#000" '
            f'stroke-width="16" stroke-linejoin="round" paint-order="stroke fill">{c["yellow"]}</text>')
    # 全面の写真では黄の1句の後ろの黄色い板と看板に字が溶ける＝下だけ黒へぼかす（上は写真の明るさのまま）
    fy, fm, fe, fo = c.get("fade", FADE_C)
    fade = ('<defs><linearGradient id="bt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="{fo}" stop-color="#000" stop-opacity="{fm}"/><stop offset="1" stop-color="#000" stop-opacity="{fe}"/></linearGradient></defs>'
            f'<rect x="0" y="{fy}" width="{W}" height="{H - fy}" fill="url(#bt)"/>') if "photo" in c else ""
    return f'<image href="{E._uri(base)}" x="0" y="0" width="{W}" height="{H}"/>' + fade + tape + name + post, fs, sx


def main():
    OUTD.mkdir(parents=True, exist_ok=True)
    kinds = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--kinds=")), "a").split(",")
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
    sh = Image.new("RGB", (640 + 20 + 210 + 10, len(kinds) * (360 + 30)), (60, 60, 60))
    d = ImageDraw.Draw(sh)
    for i, k in enumerate(kinds):
        b, fs, sx = body(k)
        n = f"ep28_T_{k}"
        E.bake2(f"ep28/{n}", b)
        print(f"{n}：名前 大きさ {fs:.1f}px・長体 {sx:.3f}")
        im = Image.open(OUTD / f"{n}.png").convert("RGB")
        y = i * 390
        d.text((4, y + 2), n, fill=(255, 255, 0), font=font)
        sh.paste(im.resize((640, 360), Image.LANCZOS), (0, y + 28))
        sh.paste(im.resize((210, 118), Image.LANCZOS), (660, y + 28))
    p = OUTD / f"cmp_{'_'.join(kinds)}.jpg"
    sh.save(p, quality=90)
    print(p)


if __name__ == "__main__":
    main()
