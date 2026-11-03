# -*- coding: utf-8 -*-
"""28本目 公開のあとのサムネ作り直し（11-03 カズヤくん「https://thumbnail-gallery.net/ から最適なサンプルを複数選定して、
そのモデルを参考にして完全に新しいデザインのものをつくる。これまで作成したものには依存しない」）。

SAMUNE のサンプルは作り方だけを倣う（絵・文面は流用しない。権利は各チャンネル）。
    A＝1294 暗闇に物を1つ＋語りかけの一文（最後の語がいちばん大きい）
    B＝12860 言葉の壁＋白と黄の箱の字＋小さな注釈
    C＝279 報道の見出し＝箱の字を積む（上に黄の札・下に赤い帯）
    D＝678 黒地に字だけ＝かすれた赤の巨大な字
    E＝12798 暗い写真に赤い巨大な題字（上下に白い明朝）
    F＝12950 明るい写真の右に赤い板・縦書きの白と黄の字
    L1〜L3＝A の物を会社の看板の写真に替えた版（11-03 カズヤくん「Aが最有力だが、タイムズのロゴ写真を使用したバージョンを」）。⭐ L2 を公開中の動画に貼った
他の回で使うとき＝この file を写して、言葉と素材を替える（分析と数値の正本＝Vault Resources/サムネの型-SAMUNE分析6型-20261103）。無料＝回数の制限なし。
守る線＝顔を生成しない・ロゴ単体を主役にしない・煽り語を使わない・「退会した人の画像が漏えいした」と言い切らない（c406＝会社は分けて示していない）。
⚠️ 「ロゴ単体を主役にしない」は L1〜L3 だけカズヤくんの指示で外した（この回の決め）。
素材＝CM108（免許証の見本・CC BY 4.0・顔は絵）・CM001（CC0・ナンバーはモザイク）・CM006（PD）・CM058（看板・CC BY 3.0）・CM062（夜の本社・CC0）。

    python -P qa_out/ep28_thumb2.py --kinds=A,B,C   … out/thumb/ep28/ep28_N_<kind>.png と並べ cmp2_<kinds>.jpg（640px と 210px）
"""
import base64
import io
import sys
from pathlib import Path

import numpy as np
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "qa_out"))
import ep27_thumb as E  # noqa: E402

W, H = E.W, E.H
REF = HERE / "ref" / "ep28"
OUTD = HERE / "out" / "thumb" / "ep28"
FONTS = {"NSB": "NotoSansJP-Black.woff2", "NSJ": "NotoSerifJP-Black.woff2", "DGO": "DelaGothicOne.woff2"}
_FT = {}


def _font(fam):
    if fam not in _FT:
        f = TTFont(HERE / "fonts" / FONTS[fam])
        _FT[fam] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _FT[fam]


def adv(text, fs, fam):
    """字の幅（px）。🔴 フォントに無い字は Chrome が別の書体で黙って埋める＝ここで止める"""
    cmap, hmtx, upm = _font(fam)
    miss = [c for c in text if ord(c) not in cmap]
    if miss:
        raise SystemExit(f"🔴 {FONTS[fam]} に無い字：{miss}（{text}）")
    return sum(hmtx[cmap[ord(c)]][0] for c in text) * fs / upm


def uri(im, fmt="PNG"):
    buf = io.BytesIO()
    im.save(buf, fmt, **({"quality": 92} if fmt == "JPEG" else {}))
    mime = "jpeg" if fmt == "JPEG" else "png"
    return f"data:image/{mime};base64," + base64.b64encode(buf.getvalue()).decode()


def txt(t, x, y, fs, fill, fam="NSB", anchor="start", extra=""):
    adv(t, fs, fam)
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{fs}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{t}</text>')


def stroke(t, x, y, fs, fill, sc, sw, fam="NSB", anchor="start", extra=""):
    return txt(t, x, y, fs, fill, fam, anchor,
               f'stroke="{sc}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke fill" {extra}')


def boxed(t, x, y, fs, bg, fg, fam="NSB", pad=16, rich=None):
    """箱の字。y＝箱の上。箱の幅は字の幅に合わせる。rich＝[(字, 色)] で色を分ける。返り値＝(SVG, 箱の右端, 箱の下)"""
    w = adv(t, fs, fam)
    h = fs * 1.12
    base = y + fs * 0.97
    if rich:
        spans = "".join(f'<tspan fill="{c}">{s}</tspan>' for s, c in rich)
        body = f'<text x="{x + pad}" y="{base:.1f}" font-family="{fam}" font-size="{fs}">{spans}</text>'
    else:
        body = txt(t, x + pad, f"{base:.1f}", fs, fg, fam)
    return f'<rect x="{x}" y="{y}" width="{w + 2 * pad:.1f}" height="{h:.1f}" fill="{bg}"/>' + body, x + w + 2 * pad, y + h


FACE = (452, 112, 622, 300)     # CM108 の絵の顔（681x432 の座標）＝絵でも明るい似顔絵は事件の回の絵に合わない＝モザイク


def card(width, tone=None, radius=24, block=17):
    """CM108（免許証の見本）を角丸に。顔はモザイク。tone＝(r,g,b) の倍率で色を付ける"""
    im = Image.open(REF / "cm108.jpg").convert("RGB")
    fx0, fy0, fx1, fy1 = FACE
    fw, fh = fx1 - fx0, fy1 - fy0
    im.paste(im.crop(FACE).resize((max(1, fw // block), max(1, fh // block)), Image.BOX).resize((fw, fh), Image.NEAREST), (fx0, fy0))
    k = width / im.width
    im = im.resize((width, round(im.height * k)), Image.LANCZOS)
    if tone:
        a = np.asarray(im, np.float32)
        a = a * np.array(tone, np.float32)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    m = Image.new("L", (im.width * 2, im.height * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, m.width - 1, m.height - 1), radius * 2, fill=255)
    im = im.convert("RGBA")
    im.putalpha(m.resize(im.size, Image.LANCZOS))
    return im


def img(im, x, y, rot=0, fmt="PNG", extra=""):
    w, h = im.size
    tr = f'transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
    return f'<image href="{uri(im, fmt)}" x="{x}" y="{y}" width="{w}" height="{h}" {tr} {extra}/>'


def photo(name, box, gamma=1.0, tone=(1, 1, 1), bright=1.0):
    """写真を切り出して全面に。box＝元の写真の (左, 上, 右, 下)・16:9"""
    im = Image.open(REF / f"{name}.jpg").convert("RGB").crop(box).resize((W, H), Image.LANCZOS)
    a = (np.asarray(im, np.float32) / 255) ** gamma
    a = a * bright * np.array(tone, np.float32)
    return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))


SHADOW = ('<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="16" '
          'flood-color="#000" flood-opacity="0.85"/></filter>')
# かすれ＝雑音のアルファでしきい値を切り、字の中に穴を開ける（大きな穴＋細かいかすれ）
GRUNGE = ('<filter id="gr" x="0" y="0" width="100%" height="100%" filterUnits="objectBoundingBox">'
          '<feTurbulence type="fractalNoise" baseFrequency="0.018 0.028" numOctaves="3" seed="11" result="a"/>'
          '<feColorMatrix in="a" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -8 5.45" result="ma"/>'
          '<feTurbulence type="fractalNoise" baseFrequency="0.22" numOctaves="2" seed="4" result="b"/>'
          '<feColorMatrix in="b" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -11 7.4" result="mb"/>'
          '<feComposite in="ma" in2="mb" operator="in" result="m"/>'
          '<feComposite in="SourceGraphic" in2="m" operator="in"/></filter>')
GRAIN = ('<filter id="gn"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/>'
         '<feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.09 0"/></filter>')


def k_A():
    """1294 の作り方＝黒地の左に暗い赤の物を1つ。右に白い明朝の一文。最後の語がいちばん大きい"""
    c = card(880, tone=(1.0, 0.26, 0.22))
    a = np.asarray(c, np.float32).copy()
    a[..., :3] *= 0.56
    c = Image.fromarray(a.astype(np.uint8), "RGBA")
    fade = ('<linearGradient id="fa" x1="0" y1="0" x2="1" y2="0"><stop offset="0.30" stop-color="#050505" stop-opacity="0"/>'
            '<stop offset="0.60" stop-color="#050505" stop-opacity="1"/></linearGradient>'
            '<radialGradient id="vg" cx="0.18" cy="0.55" r="0.62"><stop offset="0.45" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.9"/></radialGradient>')
    s = [f"<defs>{GRAIN}{fade}</defs>", f'<rect width="{W}" height="{H}" fill="#050505"/>']
    s.append(img(c, -312, 132, rot=-14))
    s.append(f'<rect width="{W}" height="{H}" fill="url(#vg)"/><rect width="{W}" height="{H}" fill="url(#fa)"/>')
    s.append(f'<rect width="{W}" height="{H}" filter="url(#gn)"/>')
    x = 500
    s.append(txt("タイムズカー情報漏洩 662万件", x, 76, 50, "#ffe600", "NSB"))
    s.append(txt("退会しても、", x, 196, 84, "#ffffff", "NSJ"))
    s.append(f'<text x="{x}" y="362" font-family="NSJ" fill="#ffffff"><tspan font-size="168">7年</tspan>'
             f'<tspan font-size="84" dx="10">残っていた</tspan></text>')
    big = "免許証。"
    for dx, col in ((-5, "#ff2a2a"), (5, "#22e0ff")):
        s.append(f'<g opacity="0.85">{txt(big, x + dx - 26, 622, 208, col, "NSJ")}</g>')
    s.append(txt(big, x - 26, 622, 208, "#ffffff", "NSJ"))
    return "".join(s)


def spot(name, s, c, r, fade_y=None, tone=None, fade_x=None):
    """写真（背景ごと）を s 倍にして、まわりを黒へ溶かす（切り抜かない）。c＝中心・r＝半径（元の写真の座標）。
    fade_y＝(溶け始め, 消える) の下の端。fade_x＝(左の消える所, 左の溶け終わり, 右の溶け始め, 右の消える所)"""
    im = Image.open(REF / f"{name}.jpg").convert("RGB")
    w0, h0 = im.size
    im = im.resize((round(w0 * s), round(h0 * s)), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    if tone:
        a = a * np.array(tone, np.float32)
    yy, xx = np.mgrid[0:im.height, 0:im.width]
    d = np.sqrt(((xx / s - c[0]) / r[0]) ** 2 + ((yy / s - c[1]) / r[1]) ** 2)
    al = np.clip((1.0 - d) / 0.30, 0, 1)
    if fade_y:
        al = al * np.clip((fade_y[1] - yy / s) / (fade_y[1] - fade_y[0]), 0, 1)
    if fade_x:
        al = al * np.clip((xx / s - fade_x[0]) / (fade_x[1] - fade_x[0]), 0, 1) * np.clip((fade_x[3] - xx / s) / (fade_x[3] - fade_x[2]), 0, 1)
    out = np.dstack([np.clip(a, 0, 255), al * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def _big_word(s, x, y, fs, anchor="end"):
    """最後の語＝白＋赤と水色のずれ（1294 の見せ方）"""
    big = "免許証。"
    for dx, col in ((-5, "#ff2a2a"), (5, "#22e0ff")):
        s.append(f'<g opacity="0.85">{txt(big, x + dx, y, fs, col, "NSJ", anchor)}</g>')
    s.append(txt(big, x, y, fs, "#ffffff", "NSJ", anchor))


def _name_stack(s, x=34, fs=36, fn=74):
    s.append(txt("タイムズカー情報漏洩", x, 610, fs, "#ffe600", "NSB"))
    s.append(txt("662万件", x, 688, fn, "#ffe600", "NSB"))


# CM058 の黄色は少し緑に寄っている＝赤を足して青を引く
SIGN_TONE = (1.10, 0.98, 0.82)
# CM058 の左の自動販売機・右の端の黄色い柱を溶かす
SIGN_SPOT = dict(s=0.50, c=(950, 330), r=(1180, 780), fade_y=(620, 730), tone=SIGN_TONE, fade_x=(300, 430, 1700, 1810))
SIGN_X = -110
BIG_X = 1230      # 右下の再生時間の札（目安 x≥1036）に「証」を掛けない＝隠れてよいのは「。」だけ


def _lines(s, right=1250, y1=150, y2=346):
    s.append(txt("退会しても、", right, y1, 84, "#ffffff", "NSJ", "end"))
    adv("7年残っていた", 84, "NSJ")
    s.append(f'<text x="{right}" y="{y2}" font-family="NSJ" fill="#ffffff" text-anchor="end"><tspan font-size="150">7年</tspan>'
             f'<tspan font-size="84" dx="10">残っていた</tspan></text>')


def k_L1():
    """A の看板版＝CM058 を背景ごと（まわりは黒へ溶かす）。看板は左上・字は右・最後の語は下いっぱい"""
    sg = spot("cm058", **SIGN_SPOT)
    s = [f"<defs>{GRAIN}</defs>", f'<rect width="{W}" height="{H}" fill="#050505"/>']
    s.append(img(sg, SIGN_X, 0))
    s.append(f'<rect width="{W}" height="{H}" filter="url(#gn)"/>')
    _lines(s)
    _big_word(s, BIG_X, 640, 200)
    _name_stack(s)
    return "".join(s)


def k_L2():
    """A の看板版＝CM058 を全面に大きく（背景ごと）。下を黒へ溶かして字を置く。左の自動販売機と右の柱は切り出しで外す"""
    g = photo("cm058", (340, 90, 1820, 922), tone=SIGN_TONE)     # 看板の上の端は切る＝「Times」の字を語りの行の上に出す
    fade = ('<linearGradient id="fb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="0.36" stop-color="#000" stop-opacity="0.94"/><stop offset="1" stop-color="#000" stop-opacity="1"/></linearGradient>')
    s = [f"<defs>{fade}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>',
         f'<rect y="404" width="{W}" height="316" fill="url(#fb)"/>']
    adv("退会しても、7年残っていた", 66, "NSJ")
    s.append('<text x="1250" y="530" font-family="NSJ" fill="#ffffff" text-anchor="end"><tspan font-size="66">退会しても、</tspan>'
             '<tspan font-size="116">7年</tspan><tspan font-size="66" dx="8">残っていた</tspan></text>')
    _big_word(s, 1206, 696, 178)     # 右下の再生時間の札（目安 x≥1036）に「証」を掛けない＝隠れてよいのは「。」だけ
    _name_stack(s, fs=36, fn=74)
    return "".join(s)


def k_L3():
    """L1 に免許証を足す＝看板（だれの話か）と免許証（何の話か）を左に重ねる"""
    sg = spot("cm058", **SIGN_SPOT)
    c = card(430, tone=(1.0, 0.26, 0.22))
    a = np.asarray(c, np.float32).copy()
    a[..., :3] *= 0.62
    c = Image.fromarray(a.astype(np.uint8), "RGBA")
    s = [f"<defs>{GRAIN}{SHADOW}</defs>", f'<rect width="{W}" height="{H}" fill="#050505"/>']
    s.append(img(sg, SIGN_X, 0))
    s.append(f'<g filter="url(#sh)">{img(c, -30, 396, rot=-9)}</g>')
    s.append(f'<rect width="{W}" height="{H}" filter="url(#gn)"/>')
    s.append(txt("情報漏洩662万件", 1250, 62, 50, "#ffe600", "NSB", "end"))
    _lines(s, y1=168, y2=356)
    _big_word(s, BIG_X, 640, 200)
    return "".join(s)


def k_B():
    """12860 の作り方＝黒地に大きな言葉の壁（漏えいした6つ）・白と黄の箱の字・右に物・小さな注釈"""
    words = ["名前", "住所", "生年月日", "電話番号", "メールアドレス", "運転免許の情報"]
    s = [f"<defs>{SHADOW}{GRAIN}</defs>", f'<rect width="{W}" height="{H}" fill="#0a0a0a"/>']
    fs = 124
    seq = words * 4
    i = 0
    for row in range(6):
        x = -40 - row * 70
        y = 112 + row * 122
        while x < W:
            t = seq[i % len(seq)]
            i += 1
            s.append(txt(t, x, y, fs, "#ffffff", "NSB", extra='opacity="0.13"'))
            x += adv(t, fs, "NSB") + 46
    s.append(f'<g filter="url(#sh)">{img(card(640), 648, 222, rot=7)}</g>')
    y0 = 58
    b1, _, b = boxed("タイムズカー", 30, y0, 142, "#ffffff", "#0a0a0a")
    s.append(b1)
    b2, _, b = boxed("免許証を7年", 30, b + 14, 142, "#fbe30e", "#0a0a0a")
    s.append(b2)
    s.append(stroke("退会した人の分まで", 36, b + 92, 74, "#ffffff", "#000", 14, "NSB"))
    s.append(stroke("情報漏洩 662万件", 36, b + 208, 98, "#fbe30e", "#000", 16, "NSB"))
    s.append(f'<rect width="{W}" height="{H}" filter="url(#gn)"/>')
    return "".join(s)


def k_C():
    """279 の作り方＝暗い赤の写真に箱の字を積む。上に黄の札・下に赤い帯"""
    return _C(photo("cm006", (0, 300, 1920, 1380), gamma=0.92, bright=1.04))


def k_C0():
    """C の地を暗い赤に（279 の地に近い版＝比べる）"""
    return _C(photo("cm001", (240, 0, 1920, 945), gamma=1.25, tone=(0.86, 0.30, 0.28), bright=0.95))


def _C(g):
    s = [f"<defs>{SHADOW}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>']
    s.append(f'<g filter="url(#sh)">{img(card(500), 762, 62, rot=6)}</g>')
    y0 = 30
    b0, _, b = boxed("タイムズカー情報漏洩662万件", 30, y0, 52, "#fbe30e", "#0a0a0a", pad=14)
    s.append(b0)
    b1, _, b = boxed("免許証は", 30, b + 18, 150, "#ffffff", "#0a0a0a")
    s.append(b1)
    b2, _, b = boxed("退会後も7年", 30, b + 10, 150, "#ffffff", "#0a0a0a", rich=[("退会後も", "#0a0a0a"), ("7年", "#d40000")])
    s.append(b2)
    s.append(f'<rect x="0" y="{H - 158}" width="{W}" height="158" fill="#c40606"/>')
    s.append(txt("なぜ持ち続けた？", W / 2, H - 38, 126, "#ffffff", "NSJ", "middle"))
    return "".join(s)


def k_F():
    """12950 の作り方＝明るい写真の右に赤い板。縦書きの白と黄の大きな字"""
    g = photo("cm006", (250, 360, 1690, 1170), gamma=0.92, bright=1.04)     # 手前の青い車のナンバーのモザイクは赤い板の裏へ
    grad = ('<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e30d0d"/>'
            '<stop offset="1" stop-color="#a80000"/></linearGradient>')
    s = [f"<defs>{SHADOW}{grad}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>']
    s.append(f'<polygon points="848,0 {W},0 {W},{H} 776,{H}" fill="url(#pn)"/>')
    s.append(f'<g filter="url(#sh)">{img(card(500), 26, 372, rot=-5)}</g>')
    b0, _, _ = boxed("タイムズカー情報漏洩", 26, 26, 66, "#fbe30e", "#0a0a0a", pad=14)
    s.append(b0)
    s.append(vert("免許証7年", 1000, 140, 134, "#ffe600", "NSB", 14))
    s.append(vert("退会しても", 1180, 165, 118, "#ffffff", "NSB", 12))
    return "".join(s)


def vert(t, x, y0, fs, fill, fam="NSB", sw=0):
    """縦書き＝1字ずつ置く（SVG の縦書きは数字の向きが読めない）"""
    out = []
    for i, c in enumerate(t):
        y = y0 + i * fs * 1.0
        out.append(stroke(c, x, f"{y:.1f}", fs, fill, "#000", sw, fam, "middle") if sw else txt(c, x, f"{y:.1f}", fs, fill, fam, "middle"))
    return "".join(out)


def k_D():
    """678 の作り方＝黒地に字だけ。かすれた赤の巨大な字＋白い字"""
    grad = ('<linearGradient id="rd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff1d12"/>'
            '<stop offset="1" stop-color="#9a0000"/></linearGradient>')
    s = [f"<defs>{GRUNGE}{grad}{GRAIN}</defs>", f'<rect width="{W}" height="{H}" fill="#060606"/>']
    s.append(f'<text x="36" y="600" font-family="NSJ" font-size="600" fill="url(#rd)" filter="url(#gr)">7年</text>')
    adv("7年", 600, "NSJ")
    s.append(txt("退 会 し て も", 48, 92, 64, "#ffffff", "NSJ"))
    x = 1244
    s.append(stroke("免許証は", x, 470, 104, "#ffffff", "#060606", 10, "NSJ", "end"))
    s.append(stroke("残っていた", x, 596, 104, "#ffffff", "#060606", 10, "NSJ", "end"))
    s.append(txt("タイムズカー情報漏洩 662万件", x, 690, 44, "#fbe30e", "NSB", "end"))
    s.append(f'<rect width="{W}" height="{H}" filter="url(#gn)"/>')
    return "".join(s)


def k_E():
    """12798 の作り方＝暗い写真に赤い巨大な題字（白い縁）。上下に白い明朝"""
    # 切り出し＝上の社名の明かり（y≈300）と右の広告の顔（x≥1740・y≈1300）を外す
    g = photo("cm062", (0, 360, 1740, 1339), gamma=1.05, tone=(0.72, 0.80, 1.0), bright=0.92)
    grad = ('<linearGradient id="rg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a3c"/>'
            '<stop offset="0.55" stop-color="#e50c0c"/><stop offset="1" stop-color="#8f0000"/></linearGradient>'
            '<linearGradient id="dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.55"/>'
            '<stop offset="0.3" stop-color="#000" stop-opacity="0.05"/><stop offset="0.7" stop-color="#000" stop-opacity="0.05"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.8"/></linearGradient>')
    s = [f"<defs>{grad}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dk)"/>']
    s.append(stroke("タイムズカー", W / 2, 150, 118, "#ffffff", "#000", 16, "NSJ", "middle"))
    fs = 292
    t = "情報漏洩"
    adv(t, fs, "NSB")
    head = f'x="{W / 2}" y="{H / 2 + 112}" font-family="NSB" font-size="{fs}" text-anchor="middle" stroke-linejoin="round"'
    s.append(f'<text {head} fill="#000" stroke="#000" stroke-width="34" opacity="0.8">{t}</text>')
    s.append(f'<text {head} fill="#fff" stroke="#fff" stroke-width="14">{t}</text>')
    s.append(f'<text {head} fill="url(#rg)">{t}</text>')
    adv("免許証は 退会後も7年 662万件", 76, "NSJ")
    s.append('<text x="640" y="684" font-family="NSJ" font-size="76" text-anchor="middle" fill="#ffffff" stroke="#000" stroke-width="14" '
             'stroke-linejoin="round" paint-order="stroke fill">免許証は 退会後も<tspan fill="#ffe600">7年</tspan> '
             '<tspan fill="#ffe600">662万件</tspan></text>')
    return "".join(s)


KINDS = {"A": k_A, "B": k_B, "C": k_C, "C0": k_C0, "D": k_D, "E": k_E, "F": k_F,
         "L1": k_L1, "L2": k_L2, "L3": k_L3}


def main():
    OUTD.mkdir(parents=True, exist_ok=True)
    kinds = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--kinds=")), "A").split(",")
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
    sh = Image.new("RGB", (640 + 20 + 210 + 10, len(kinds) * (360 + 30)), (60, 60, 60))
    d = ImageDraw.Draw(sh)
    for i, k in enumerate(kinds):
        n = f"ep28_N_{k}"
        E.bake2(f"ep28/{n}", KINDS[k]())
        p = OUTD / f"{n}.png"
        im = Image.open(p).convert("RGB")
        print(f"{n}：{im.size}・{p.stat().st_size:,} バイト")
        y = i * 390
        d.text((4, y + 2), n, fill=(255, 255, 0), font=font)
        sh.paste(im.resize((640, 360), Image.LANCZOS), (0, y + 28))
        sh.paste(im.resize((210, 118), Image.LANCZOS), (660, y + 28))
    p = OUTD / f"cmp2_{'_'.join(kinds)}.jpg"
    sh.save(p, quality=90)
    print(p)


if __name__ == "__main__":
    main()
