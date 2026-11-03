# -*- coding: utf-8 -*-
"""27本目 公開のあとのサムネ作り直し（11-03 カズヤくん「八田與一の動画のサムネイルも、今回分析したデザインを基に作り直してください」
「サムネの顔写真は添付のものを使って」）。

型と数値の正本＝Vault Resources/サムネの型-SAMUNE分析6型-20261103・字と箱の部品＝qa_out/ep28_thumb2.py。
    L＝A の写真全面版（28本目で選ばれた L2 の作り）／A＝暗闇に1つ＋一文／B＝言葉の壁／C＝報道の見出し／D＝字だけ／E＝巨大な題字／F＝赤い板の縦書き
    ⭐ A を公開中の動画に貼った（11-03・カズヤくんの選び）。⚠️ 粒（GRAIN）は再圧縮で消えて鮮明さの比を下げる＝A からは外した（B・D は見比べ用のまま）。
写真＝カズヤくんの添付（ref/ep27/police/thumb_face_20261103.webp＝git の外・680x382 の中身 350x382）。⚠️ 小さい＝拡大はふつうの補間だけ（顔を生成しない）。
守る線＝顔（目・鼻・口）に字をかけない・「犯人」「真相」と書かない・反転しない。「容疑者」は 10-31 のカズヤくんの決めのまま省く（題と概要欄にはある）。
左上の店の看板はぼかす（27本目の「地元の店だけ隠す」）。

    python -P qa_out/ep27_thumb2.py --kinds=L,A,B,C,D,E,F   … out/thumb/ep27/ep27_N_<kind>.png と並べ cmp_<kinds>.jpg・210px の cmp210_<kinds>.jpg
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "qa_out"))
import ep28_thumb2 as P  # noqa: E402

E = P.E
W, H = P.W, P.H
OUTD = HERE / "out" / "thumb" / "ep27"
SRC = HERE / "ref" / "ep27" / "police" / "thumb_face_20261103.webp"
IN = (169, 0, 519, 382)             # 添付の左右の黒い帯の内側（列の平均で測った x167〜520 の1px 内）
IW, IH = IN[2] - IN[0], IN[3] - IN[1]
FACE = (93, 40, 231, 200)           # 中身の座標の顔（額〜あご・耳まで）＝ここに字を置かない
SIGN = (0, 0, 78, 112)              # 中身の座標の店の看板の字（頭の左の端 x≈93 より左＝広げると顔までぼける）
BADGE = (1036, 598, 1256, 696)      # 右下の再生時間の札（1280 に換算した目安）
YEL, WHT, BLK = "#ffe600", "#ffffff", "#0a0a0a"
BOX, FB = [], [None]                # 字の外接の記録・顔の外接（下の check が見る）


def inner():
    im = Image.open(SRC).convert("RGB").crop(IN)
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rectangle(SIGN, fill=255)
    return Image.composite(im.filter(ImageFilter.GaussianBlur(7)), im, m.filter(ImageFilter.GaussianBlur(4)))


def sized(s, bright=1.0, tone=(1, 1, 1)):
    """拡大はふつうの補間＋軽いシャープだけ"""
    im = inner().resize((round(IW * s), round(IH * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6 * s, percent=70, threshold=2))
    if bright != 1.0 or tone != (1, 1, 1):
        a = np.asarray(im, np.float32) * bright * np.array(tone, np.float32)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return im


def place(s, xo, yo, l=0, r=0, t=0, b=0, bright=1.0):
    """写真を s 倍で (xo, yo) に置く。l r t b＝その辺から px で透明へ溶かす。顔の外接を記録する"""
    im = sized(s, bright).convert("RGBA")
    w, h = im.size
    al = np.ones((h, w), np.float32)
    xx, yy = np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32)
    if l:
        al *= np.clip(xx / l, 0, 1)[None, :]
    if r:
        al *= np.clip((w - 1 - xx) / r, 0, 1)[None, :]
    if t:
        al *= np.clip(yy / t, 0, 1)[:, None]
    if b:
        al *= np.clip((h - 1 - yy) / b, 0, 1)[:, None]
    im.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
    FB[0] = (xo + FACE[0] * s, yo + FACE[1] * s, xo + FACE[2] * s, yo + FACE[3] * s)
    return f'<image href="{P.uri(im)}" x="{xo}" y="{yo}" width="{w}" height="{h}"/>'


def framed(s, x, y, rot, border=10):
    """写真を白い額に入れて少し傾ける（B・C の「物」）。回す分は check の余白で見る"""
    im = sized(s)
    f = Image.new("RGB", (im.width + 2 * border, im.height + 2 * border), (255, 255, 255))
    f.paste(im, (border, border))
    FB[0] = (x + border + FACE[0] * s, y + border + FACE[1] * s, x + border + FACE[2] * s, y + border + FACE[3] * s)
    return f'<g filter="url(#sh)">{P.img(f, x, y, rot=rot, fmt="JPEG")}</g>'


def bg(bright=0.42, tone=(1, 1, 1), blur=30):
    """同じ写真を全面に広げてぼかした地"""
    k = W / IW
    im = inner().resize((W, round(IH * k)), Image.LANCZOS).crop((0, 120, W, 120 + H)).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im, np.float32) * bright * np.array(tone, np.float32)
    return f'<image href="{P.uri(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), "JPEG")}" width="{W}" height="{H}"/>'


def run(parts, x, y, anchor="start", fam="NSJ", sw=0, sc="#000"):
    """1行の字。parts＝[(字, 大きさ, 色)]。字の外接を BOX に残す"""
    w = sum(P.adv(t, fs, fam) for t, fs, _ in parts)
    x0 = x if anchor == "start" else x - w if anchor == "end" else x - w / 2
    fsm = max(fs for _, fs, _ in parts)
    BOX.append(("".join(t for t, _, _ in parts), x0, y - fsm * 0.9, x0 + w, y + fsm * 0.14, fsm))
    st = f'stroke="{sc}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke fill"' if sw else ""
    spans = "".join(f'<tspan font-size="{fs}" fill="{c}">{t}</tspan>' for t, fs, c in parts)
    return f'<text x="{x0:.1f}" y="{y}" font-family="{fam}" {st}>{spans}</text>'


def glitch(t, x, y, fs, anchor="start"):
    """最後の語＝白＋赤と水色のずれ（1294 の見せ方）"""
    g = "".join(f'<g opacity="0.85">{P.txt(t, x + dx, y, fs, c, "NSJ", anchor)}</g>' for dx, c in ((-5, "#ff2a2a"), (5, "#22e0ff")))
    return g + run([(t, fs, WHT)], x, y, anchor)


def boxed(t, x, y, fs, bg_, fg, fam="NSB", pad=16, rich=None):
    b, r, bot = P.boxed(t, x, y, fs, bg_, fg, fam, pad, rich)
    BOX.append((t, x, y, r, bot, fs))
    return b, r, bot


def vcol(t, x, y0, fs, fill, sw=0):
    """縦書きの列"""
    BOX.append((t, x - fs / 2, y0 - fs * 0.9, x + fs / 2, y0 + (len(t) - 1) * fs + fs * 0.14, fs))
    return P.vert(t, x, y0, fs, fill, "NSB", sw)


def k_L():
    """A の写真全面版（28本目の L2 の作り）。上に写真を大きく・下を黒へ溶かして一文＋最後に名前"""
    fade = ('<linearGradient id="fb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="0.36" stop-color="#000" stop-opacity="0.94"/><stop offset="1" stop-color="#000" stop-opacity="1"/></linearGradient>')
    s = [f"<defs>{fade}</defs>", bg(0.42), place(2.1, 348, -40, l=130, r=130), f'<rect y="404" width="{W}" height="316" fill="url(#fb)"/>']
    s.append(run([("情報", 60, WHT), ("1万3978件", 108, YEL), ("でも、", 60, WHT), ("見つからない", 60, WHT)], 34, 520))
    s.append(glitch("八田與一", 34, 692, 186))
    s.append(boxed("重要指名手配", 806, 640, 34, "#fbe30e", BLK, pad=10)[0])
    return "".join(s)


def k_A():
    """1294 の作り方＝暗闇の左に写真。右に白い明朝の一文。最後の語がいちばん大きい"""
    s = [f'<rect width="{W}" height="{H}" fill="#050505"/>', place(1.885, -140, 0, r=170, bright=0.92)]
    x = 470
    s.append(run([("別府ひき逃げ殺傷事件", 46, YEL)], x, 66, fam="NSB"))
    s.append(run([("寄せられた情報は", 70, WHT)], x, 160))
    s.append(run([("1万3978件", 150, WHT)], x, 318))
    s.append(glitch("八田與一", x, 560, 190))
    s.append(run([("なぜ見つからない？", 62, YEL)], x, 682))
    # 粒（GRAIN）は入れない＝YouTube の再圧縮で消えて鮮明さの比が 0.87 に落ちた（11-03・thumbcheck）
    s.append(run([("写真：大分県警察", 20, WHT)], 14, 706, fam="NSB", sw=4))     # 出どころ＝カズヤくんの答え（11-03「大分県警の公式」）
    return "".join(s)


def k_B():
    """12860 の作り方＝黒地に言葉の壁（この事件の事実の語）・白と黄の箱の字・右に額の写真"""
    words = ["重要指名手配", "目撃情報", "似顔絵", "防犯カメラ", "捜査特別報奨金", "懸賞金"]
    s = [f"<defs>{P.SHADOW}{P.GRAIN}</defs>", f'<rect width="{W}" height="{H}" fill="#0a0a0a"/>']
    fs, seq, i = 124, words * 4, 0
    for row in range(6):
        x, y = -40 - row * 70, 112 + row * 122
        while x < W:
            t = seq[i % len(seq)]
            i += 1
            s.append(P.txt(t, x, y, fs, WHT, "NSB", extra='opacity="0.13"'))
            x += P.adv(t, fs, "NSB") + 46
    s.append(framed(1.25, 806, 34, 5))
    b1, _, b = boxed("八田與一", 30, 52, 142, WHT, BLK)
    b2, _, b = boxed("情報1万3978件", 30, b + 14, 112, "#fbe30e", BLK)
    s += [b1, b2]
    s.append(run([("それでも、見つからない", 66, WHT)], 36, b + 92, fam="NSB", sw=12))
    s.append(run([("なぜ？", 150, "#fbe30e")], 36, b + 262, fam="NSB", sw=16))
    s.append(f'<rect width="{W}" height="{H}" filter="url(#gn)"/>')
    return "".join(s)


def k_C():
    """279 の作り方＝暗い赤の地に箱の字を積む。上に黄の札・下に赤い帯・右上に額の写真"""
    s = [f"<defs>{P.SHADOW}</defs>", bg(0.55, (0.95, 0.32, 0.30), 24), framed(1.30, 792, 24, 4)]
    b0, _, b = boxed("別府ひき逃げ殺傷事件", 30, 30, 50, "#fbe30e", BLK, pad=14)
    b1, _, b = boxed("八田與一", 30, b + 18, 150, WHT, BLK)
    b2, _, b = boxed("情報1万3978件", 30, b + 16, 112, WHT, BLK, rich=[("情報", BLK), ("1万3978件", "#d40000")])
    b3, _, b = boxed("事件から4年", 30, b + 14, 90, WHT, BLK)
    s += [b0, b1, b2, b3]
    s.append(f'<rect x="0" y="{H - 158}" width="{W}" height="158" fill="#c40606"/>')
    s.append(run([("なぜ見つからない？", 110, WHT)], 30, H - 40))
    return "".join(s)


def k_D():
    """678 の作り方＝黒地にかすれた赤の巨大な字。写真は字の手前に黒から浮かべる"""
    grad = ('<linearGradient id="rd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff1d12"/>'
            '<stop offset="1" stop-color="#9a0000"/></linearGradient>')
    s = [f"<defs>{P.GRUNGE}{grad}{P.GRAIN}</defs>", f'<rect width="{W}" height="{H}" fill="#060606"/>']
    P.adv("4年", 520, "NSJ")
    s.append(f'<text x="24" y="550" font-family="NSJ" font-size="520" fill="url(#rd)" filter="url(#gr)">4年</text>')
    s.append(place(1.885, 677, 0, l=130, b=120))
    s.append(run([("情報", 58, WHT), ("1万3978件", 84, YEL), ("でも", 58, WHT)], 40, 86))
    s.append(run([("八田與一", 122, WHT)], 40, 696, sw=10, sc="#060606"))
    s.append(run([("なぜ見つからない？", 54, YEL)], 540, 696, sw=8, sc="#060606"))
    s.append(f'<rect width="{W}" height="{H}" filter="url(#gn)"/>')
    return "".join(s)


def k_E():
    """12798 の作り方＝暗い写真に赤い巨大な題字（白い縁）。上の左右に白い明朝"""
    grad = ('<linearGradient id="rg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a3c"/>'
            '<stop offset="0.55" stop-color="#e50c0c"/><stop offset="1" stop-color="#8f0000"/></linearGradient>'
            '<linearGradient id="dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.35"/>'
            '<stop offset="0.45" stop-color="#000" stop-opacity="0.05"/><stop offset="0.72" stop-color="#000" stop-opacity="0.55"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.85"/></linearGradient>')
    s = [f"<defs>{grad}</defs>", bg(0.40), place(2.0, 314, -30, l=110, r=110), f'<rect width="{W}" height="{H}" fill="url(#dk)"/>']
    s.append(run([("情報", 76, WHT)], 250, 110, "middle", sw=12))
    s.append(run([("1万3978件", 88, YEL)], 250, 214, "middle", sw=12))
    s.append(run([("なぜ", 76, WHT)], 1020, 110, "middle", sw=12))
    s.append(run([("見つからない？", 62, YEL)], 1020, 214, "middle", sw=12))
    fs, t = 292, "八田與一"
    P.adv(t, fs, "NSB")
    head = f'x="{W / 2}" y="644" font-family="NSB" font-size="{fs}" text-anchor="middle" stroke-linejoin="round"'
    s.append(f'<text {head} fill="#000" stroke="#000" stroke-width="34" opacity="0.8">{t}</text>')
    s.append(f'<text {head} fill="#fff" stroke="#fff" stroke-width="14">{t}</text>')
    s.append(f'<text {head} fill="url(#rg)">{t}</text>')
    BOX.append((t, 56, 644 - fs * 0.88, 1224, 644 + fs * 0.1, 0))    # 札（x≥1036・y≥598）に掛かるのは「一」の下の余白だけ＝大きさ 0 で札の見張りから外す
    return "".join(s)


def k_F():
    """12950 の作り方＝明るい写真の右に赤い板。縦書きの黄と白の大きな字"""
    grad = ('<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e30d0d"/>'
            '<stop offset="1" stop-color="#a80000"/></linearGradient>')
    s = [f"<defs>{P.SHADOW}{grad}</defs>", bg(0.55), place(2.0, -10, -30, r=60, bright=1.08)]
    s.append(f'<polygon points="730,0 {W},0 {W},{H} 650,{H}" fill="url(#pn)"/>')
    s.append(boxed("情報1万3978件", 26, 606, 72, "#fbe30e", BLK, pad=14)[0])
    s.append(vcol("見つからない", 900, 118, 106, WHT, 12))
    s.append(vcol("八田與一", 1120, 164, 150, YEL, 14))
    return "".join(s)


KINDS = {"L": k_L, "A": k_A, "B": k_B, "C": k_C, "D": k_D, "E": k_E, "F": k_F}


def check(kind):
    """字が顔に掛かっていないか・札に要の字が掛かっていないか・端から出ていないかを、字の外接で見る（絵を見る前の網）"""
    bad = 0
    fx0, fy0, fx1, fy1 = FB[0]
    m = 14 if kind in "BC" else 2      # 傾けた額は回る分の余白
    for t, x0, y0, x1, y1, fs in BOX:
        if x0 < fx1 + m and x1 > fx0 - m and y0 < fy1 + m and y1 > fy0 - m:
            print(f"  🔴 {kind} 顔に字：{t}（{x0:.0f},{y0:.0f}〜{x1:.0f},{y1:.0f}・顔 {fx0:.0f},{fy0:.0f}〜{fx1:.0f},{fy1:.0f}）")
            bad += 1
        if fs >= 30 and x0 < BADGE[2] and x1 > BADGE[0] and y0 < BADGE[3] and y1 > BADGE[1]:
            print(f"  ⚠️ {kind} 札に字：{t}（x{x0:.0f}〜{x1:.0f}・y{y0:.0f}〜{y1:.0f}）")
            bad += 1
        if x0 < 6 or x1 > W - 6 or y0 < -2 or y1 > H + 2:
            print(f"  ⚠️ {kind} 端から出る：{t}（x{x0:.0f}〜{x1:.0f}・y{y0:.0f}〜{y1:.0f}）")
            bad += 1
    print(f"  {kind}：字 {len(BOX)} 行・顔 ({fx0:.0f},{fy0:.0f})〜({fx1:.0f},{fy1:.0f})・粗 {bad}")
    return bad


def main():
    OUTD.mkdir(parents=True, exist_ok=True)
    kinds = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--kinds=")), "L,A,B,C,D,E,F").split(",")
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 20)
    cols, cw, ch = 2, 640, 360
    cells = len(kinds) + 1                  # 最後の升＝いま公開中の k5（見比べ）
    rows = (cells + 1) // 2
    sh = Image.new("RGB", (cols * cw, rows * (ch + 26)), (60, 60, 60))
    d = ImageDraw.Draw(sh)
    small = Image.new("RGB", (cells * 218 + 8, 118 + 8 + 24), (250, 250, 250))
    ds = ImageDraw.Draw(small)
    bad = 0
    names = [(k, OUTD / f"ep27_N_{k}.png") for k in kinds] + [("いま", OUTD / "ep27_A7k5_v7.png")]
    for i, (k, p) in enumerate(names):
        if k != "いま":
            BOX.clear()
            E.bake2(f"ep27/ep27_N_{k}", KINDS[k]())
            bad += check(k)
        im = Image.open(p).convert("RGB")
        if k != "いま":
            print(f"ep27_N_{k}：{im.size}・{p.stat().st_size:,} バイト")
        x, y = (i % cols) * cw, (i // cols) * (ch + 26)
        d.text((x + 6, y + 1), k, fill=(255, 255, 0), font=font)
        v = im.resize((cw, ch), Image.LANCZOS)
        # 右下の再生時間の札を重ねて見る
        o = ImageDraw.Draw(v)
        bx = [round(c * cw / W) for c in (1160, 650, 1262, 700)]
        o.rectangle(bx, fill=(0, 0, 0))
        o.text((bx[0] + 4, bx[1] + 1), "15:28", fill=(255, 255, 255), font=ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 16))
        sh.paste(v, (x, y + 26))
        ds.text((4 + i * 218, 1), k, fill=(0, 0, 0), font=font)
        small.paste(im.resize((210, 118), Image.LANCZOS), (4 + i * 218, 28))
    tag = "_".join(kinds)
    sh.save(OUTD / f"cmp_{tag}.jpg", quality=90)
    small.save(OUTD / f"cmp210_{tag}.png")
    print(OUTD / f"cmp_{tag}.jpg", "粗の合計", bad)


if __name__ == "__main__":
    main()
