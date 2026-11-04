# -*- coding: utf-8 -*-
"""29本目 ⑥ サムネの案（SAMUNE の型＝Vault Resources/サムネの型-SAMUNE分析6型-20261103・道具は qa_out/ep28_thumb2.py の部品をそのまま使う）。

言葉＝承認①の案 A「侵入から 76日 気づけず」＋「GMOへの不正アクセス」（台本 §1-2・c105 c407）。
守る線＝顔なし（§B2-11b ②）・煽り語なし・粒なし（再圧縮で鮮明さの比が下がる）・右下の再生時間の札（x≥1036・y≥598）に要の字を掛けない。

    python -P qa_out/ep29_thumb.py --kinds=L,M,E,D   … out/thumb/ep29/ep29_N_<kind>.png と並べ cmp_<kinds>.jpg（640px と 210px）
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "qa_out"))
import ep27_thumb as E  # noqa: E402
from ep28_thumb2 import GRUNGE, SHADOW, adv, boxed, stroke, txt, uri, vert  # noqa: E402

W, H = E.W, E.H
SRC = HERE / "ref" / "ep29" / "src" / "eizou"
OUTD = HERE / "out" / "thumb" / "ep29"


def photo(name, box, gamma=1.0, tone=(1, 1, 1), bright=1.0, sat=1.0):
    """写真を切り出して全面に。box＝元の写真の (左, 上, 右, 下)・16:9"""
    im = Image.open(SRC / f"{name}.jpg").convert("RGB").crop(box).resize((W, H), Image.LANCZOS)
    a = (np.asarray(im, np.float32) / 255) ** gamma
    a = a * bright * np.array(tone, np.float32)
    if sat != 1.0:
        g = a.mean(axis=2, keepdims=True)
        a = g + (a - g) * sat
    return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))


def _fade(y0, stops=((0, 0), (0.36, 0.94), (1, 1))):
    st = "".join(f'<stop offset="{o}" stop-color="#000" stop-opacity="{a}"/>' for o, a in stops)
    return (f'<linearGradient id="fb" x1="0" y1="0" x2="0" y2="1">{st}</linearGradient>',
            f'<rect y="{y0}" width="{W}" height="{H - y0}" fill="url(#fb)"/>')


def _big(s, x, y, fs, word, anchor="start"):
    """最後の語＝白＋赤と水色のずれ（サンプル 1294 の見せ方）"""
    for dx, col in ((-5, "#ff2a2a"), (5, "#22e0ff")):
        s.append(f'<g opacity="0.85">{txt(word, x + dx, y, fs, col, "NSJ", anchor)}</g>')
    s.append(txt(word, x, y, fs, "#ffffff", "NSJ", anchor))


def _sentence(g, y0=404):
    """L2 の並び＝上に写真・下を黒へ溶かして、語が段々大きくなる一文。左下に事件の名前（黄）"""
    d, r = _fade(y0)
    s = [f"<defs>{d}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>', r]
    adv("侵入から76日、", 66, "NSJ")
    s.append('<text x="1250" y="520" font-family="NSJ" fill="#ffffff" text-anchor="end"><tspan font-size="70">侵入から</tspan>'
             '<tspan font-size="132" fill="#ff2a2a" dx="10">76日</tspan><tspan font-size="70">、</tspan></text>')
    _big(s, 1030, 694, 188, "気づけず", "end")
    s.append(txt("GMOへの", 30, 630, 40, "#ffe600", "NSB"))
    s.append(txt("不正アクセス", 30, 688, 40, "#ffe600", "NSB"))
    return "".join(s)


def k_L():
    """A の看板版（28本目 L2 と同じ並び）＝ロビーの青い GMO の字を上に大きく（CM003・CC BY 4.0）。
    CM004（CC0）は札が無いが、1280 に広げると字がピンぼけで甘い＝鮮明な CM003。字の前の「関係者専用入口」の札は
    字のすぐ下から黒へ溶かして隠す＝その分、一文を上へ広げて 210px でも読める大きさにした"""
    g = photo("CM003", (700, 653, 1700, 1215), gamma=0.86, bright=1.08, sat=1.12)
    d, r = _fade(196, ((0, 0), (0.13, 0.97), (1, 1)))
    s = [f"<defs>{d}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>', r]
    s.append(txt("GMOへの", 34, 352, 52, "#ffe600", "NSB"))
    s.append(txt("不正アクセス", 34, 420, 52, "#ffe600", "NSB"))
    adv("侵入から76日、", 66, "NSJ")
    s.append('<text x="1256" y="424" font-family="NSJ" fill="#ffffff" text-anchor="end"><tspan font-size="84">侵入から</tspan>'
             '<tspan font-size="168" fill="#ff2a2a" dx="10">76日</tspan><tspan font-size="84">、</tspan></text>')
    _big(s, 1030, 690, 232, "気づけず", "end")
    return "".join(s)


def k_M():
    """同じ並びで夜の街＝渋谷フクラスの GMO の字と首都高（T230・CC0）。上の空とビルを残す"""
    return _sentence(photo("T230", (220, 0, 1700, 833), gamma=0.80, bright=1.10, sat=1.25))


def k_E():
    """E＝暗い写真に赤い巨大な題字（210px で最も読める）＝T232 の屋上の看板は小さい＝地として敷く（CC0）"""
    g = photo("T232", (0, 180, 1920, 1260), gamma=1.0, tone=(0.74, 0.82, 1.0), bright=0.92)
    grad = ('<linearGradient id="rg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a3c"/>'
            '<stop offset="0.55" stop-color="#e50c0c"/><stop offset="1" stop-color="#8f0000"/></linearGradient>'
            '<linearGradient id="dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.6"/>'
            '<stop offset="0.3" stop-color="#000" stop-opacity="0.08"/><stop offset="0.7" stop-color="#000" stop-opacity="0.08"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.85"/></linearGradient>')
    s = [f"<defs>{grad}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dk)"/>']
    s.append(stroke("GMOへの不正アクセス", W / 2, 122, 96, "#ffffff", "#000", 14, "NSJ", "middle"))
    fs, t = 340, "76日"
    adv(t, fs, "NSB")
    head = f'x="{W / 2}" y="{H / 2 + 126}" font-family="NSB" font-size="{fs}" text-anchor="middle" stroke-linejoin="round"'
    s.append(f'<text {head} fill="#000" stroke="#000" stroke-width="34" opacity="0.8">{t}</text>')
    s.append(f'<text {head} fill="#fff" stroke="#fff" stroke-width="14">{t}</text>')
    s.append(f'<text {head} fill="url(#rg)">{t}</text>')
    s.append(stroke("侵入に気づけず", 40, 684, 96, "#ffe600", "#000", 14, "NSJ"))
    return "".join(s)


def k_D():
    """28本目の公開はじめの d3 の並び＝全面の写真・赤い名前に黒い縁・白の行・黄の1句を左詰め（CM003）"""
    g = photo("CM003", (700, 560, 1700, 1122), gamma=0.80, bright=1.14, sat=1.25)
    d, r = _fade(440, ((0, 0), (0.5, 0.82), (1, 0.96)))
    s = [f"<defs>{d}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>', r]
    s.append(stroke("GMOへの不正アクセス", 40, 512, 92, "#ff1a1a", "#000", 14, "NSJ"))
    s.append(stroke("侵入から76日", 40, 606, 76, "#ffffff", "#000", 12, "NSB"))
    s.append(stroke("なぜ気づけず？", 40, 694, 76, "#ffe600", "#000", 12, "NSB"))
    return "".join(s)


def _logo(box=(700, 653, 1700, 1215)):
    return photo("CM003", box, gamma=0.86, bright=1.08, sat=1.12)


def k_J():
    """左に GMO の字・右に積んだ一文（76日 を最大に）＝L より数字が大きい。写真の右を黒へ溶かす"""
    g = photo("CM003", (420, 500, 1920, 1344), gamma=0.86, bright=1.08, sat=1.12)
    grad = ('<linearGradient id="fx" x1="0" y1="0" x2="1" y2="0"><stop offset="0.47" stop-color="#050505" stop-opacity="0"/>'
            '<stop offset="0.55" stop-color="#050505" stop-opacity="1"/></linearGradient>'
            '<linearGradient id="fy" x1="0" y1="0" x2="0" y2="1"><stop offset="0.39" stop-color="#050505" stop-opacity="0"/>'
            '<stop offset="0.46" stop-color="#050505" stop-opacity="1"/></linearGradient>')
    s = [f"<defs>{grad}</defs>", f'<rect width="{W}" height="{H}" fill="#050505"/>',
         f'<image href="{uri(g, "JPEG")}" x="-300" y="0" width="{W}" height="{H}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#fx)"/><rect width="{W}" height="{H}" fill="url(#fy)"/>']
    s.append(txt("侵入から", 1256, 112, 96, "#ffffff", "NSJ", "end"))
    adv("76日", 262, "NSJ")
    for dx, col in ((-5, "#ff2a2a"), (5, "#22e0ff")):
        s.append(f'<g opacity="0.85">{txt("76日", 1256 + dx, 348, 262, col, "NSJ", "end")}</g>')
    s.append(txt("76日", 1256, 348, 262, "#ff2020", "NSJ", "end"))
    s.append(txt("気づけず", 1256, 590, 226, "#ffffff", "NSJ", "end"))
    s.append(txt("GMOへの不正アクセス", 34, 690, 62, "#ffe600", "NSB"))
    return "".join(s)


def k_J2():
    """J のロゴを大きく（11-04 カズヤくん「Jはもっとロゴを大きく」）＝字の幅 512 → 750px。76日 は少し小さく、気づけず は大きく"""
    g = photo("CM003", (896, 612, 1920, 1188), gamma=0.86, bright=1.08, sat=1.12)
    grad = ('<linearGradient id="fx" x1="0" y1="0" x2="1" y2="0"><stop offset="0.615" stop-color="#050505" stop-opacity="0"/>'
            '<stop offset="0.64" stop-color="#050505" stop-opacity="1"/></linearGradient>'
            '<linearGradient id="fy" x1="0" y1="0" x2="0" y2="1"><stop offset="0.365" stop-color="#050505" stop-opacity="0"/>'
            '<stop offset="0.42" stop-color="#050505" stop-opacity="1"/></linearGradient>')
    s = [f"<defs>{grad}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#fx)"/><rect width="{W}" height="{H}" fill="url(#fy)"/>']
    s.append(txt("侵入から", 1256, 104, 96, "#ffffff", "NSJ", "end"))
    adv("76日", 216, "NSJ")
    for dx, col in ((-5, "#ff2a2a"), (5, "#22e0ff")):
        s.append(f'<g opacity="0.85">{txt("76日", 1256 + dx, 310, 216, col, "NSJ", "end")}</g>')
    s.append(txt("76日", 1256, 310, 216, "#ff2020", "NSJ", "end"))
    s.append(txt("気づけず", 1256, 590, 250, "#ffffff", "NSJ", "end"))
    s.append(txt("GMOへの不正アクセス", 34, 690, 62, "#ffe600", "NSB"))
    return "".join(s)


def k_L0():
    """L の1回目（CM003・札が字に重なる）＝案を消さずに残す"""
    return _sentence(photo("CM003", (700, 640, 1700, 1202), gamma=0.86, bright=1.08, sat=1.12))


def k_L1():
    """L の2回目（CM004・CC0・札は無いが字がピンぼけ）＝案を消さずに残す"""
    return _sentence(photo("CM004", (640, 640, 1820, 1304), gamma=0.86, bright=1.08, sat=1.12))


def k_B():
    """B＝地に言葉の壁（確認までの日付）・白と黄の箱の字（サンプル 12860 の作り方）。絵は GMO の字を右下に小さく"""
    words = ["8月5日", "8月17日", "9月20日", "10月14日", "10月19日", "10月20日"]
    s = [f"<defs>{SHADOW}</defs>", f'<rect width="{W}" height="{H}" fill="#0a0a0a"/>']
    fs, i = 124, 0
    for row in range(6):
        x, y = -40 - row * 70, 112 + row * 122
        while x < W:
            t = words[i % len(words)]
            i += 1
            s.append(txt(t, x, y, fs, "#ffffff", "NSB", extra='opacity="0.13"'))
            x += adv(t, fs, "NSB") + 46
    y0 = 40
    b1, _, b = boxed("GMOへの不正アクセス", 30, y0, 92, "#ffffff", "#0a0a0a")
    s.append(b1)
    b2, _, b = boxed("侵入から76日", 30, b + 14, 168, "#fbe30e", "#0a0a0a", rich=[("侵入から", "#0a0a0a"), ("76日", "#d40000")])
    s.append(b2)
    s.append(stroke("会社は気づけず", 36, b + 150, 142, "#ffffff", "#000", 18, "NSB"))
    s.append(stroke("きっかけは利用者の問い合わせ", 36, b + 262, 62, "#fbe30e", "#000", 12, "NSB"))
    return "".join(s)


def k_C():
    """C＝報道の見出し（サンプル 279 の作り方）＝写真に箱の字を積む・下に赤い帯の問い"""
    g = photo("T230", (120, 0, 1800, 945), gamma=0.86, bright=1.04, sat=1.15)
    s = [f"<defs>{SHADOW}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>']
    b0, _, b = boxed("GMOへの不正アクセス", 30, 30, 66, "#fbe30e", "#0a0a0a", pad=14)
    s.append(b0)
    b1, _, b = boxed("侵入から76日", 30, b + 18, 150, "#ffffff", "#0a0a0a", rich=[("侵入から", "#0a0a0a"), ("76日", "#d40000")])
    s.append(b1)
    b2, _, b = boxed("会社は気づけず", 30, b + 14, 150, "#ffffff", "#0a0a0a")
    s.append(b2)
    s.append(f'<rect x="0" y="{H - 158}" width="{W}" height="158" fill="#c40606"/>')
    s.append(txt("なぜ2カ月半も？", 500, H - 38, 126, "#ffffff", "NSJ", "middle"))
    return "".join(s)


def k_K():
    """D＝黒地に字だけ（サンプル 678 の作り方）＝かすれた赤の巨大な 76日。粒は入れない"""
    grad = ('<linearGradient id="rd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff1d12"/>'
            '<stop offset="1" stop-color="#9a0000"/></linearGradient>')
    s = [f"<defs>{GRUNGE}{grad}</defs>", f'<rect width="{W}" height="{H}" fill="#060606"/>']
    adv("76日", 520, "NSJ")
    s.append(f'<text x="30" y="548" font-family="NSJ" font-size="520" fill="url(#rd)" filter="url(#gr)">76日</text>')
    s.append(txt("GMOへの不正アクセス", 44, 86, 66, "#fbe30e", "NSB"))
    s.append(stroke("侵入から", 1250, 86, 66, "#ffffff", "#060606", 8, "NSJ", "end"))
    s.append(stroke("会社は、気づけず", 44, 690, 118, "#ffffff", "#060606", 10, "NSJ"))
    return "".join(s)


def k_F():
    """F＝明るい写真の右に赤い板・縦書き（サンプル 12950 の作り方）。写真が主役のまま字も大きい"""
    g = photo("CM003", (820, 606, 1920, 1225), gamma=0.80, bright=1.12, sat=1.15)     # 字の全部が赤い板より左に入る切り出し
    grad = ('<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e30d0d"/>'
            '<stop offset="1" stop-color="#a80000"/></linearGradient>')
    s = [f"<defs>{SHADOW}{grad}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>']
    s.append(f'<polygon points="848,0 {W},0 {W},{H} 776,{H}" fill="url(#pn)"/>')
    b0, _, _ = boxed("GMOへの不正アクセス", 26, 26, 58, "#fbe30e", "#0a0a0a", pad=14)
    s.append(b0)
    s.append(vert("76日", 1010, 150, 178, "#ffe600", "NSB", 14))
    s.append(vert("侵入から", 1180, 130, 112, "#ffffff", "NSB", 12))
    s.append(stroke("気づけず", 400, 660, 190, "#ffffff", "#000", 18, "NSB", "middle"))
    return "".join(s)


def k_G():
    """L の並びで言葉だけ替えた＝第8報の頼み（c101）を掴みに。台本 §1-2 の案 C を原文の字に寄せた（案 C は承認①で選ばれていない）"""
    g = _logo()
    d, r = _fade(196, ((0, 0), (0.13, 0.97), (1, 1)))
    s = [f"<defs>{d}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>', r]
    s.append(txt("GMOへの", 34, 352, 52, "#ffe600", "NSB"))
    s.append(txt("不正アクセス", 34, 420, 52, "#ffe600", "NSB"))
    adv("12時になる前に、", 66, "NSJ")
    s.append('<text x="1256" y="424" font-family="NSJ" fill="#ffffff" text-anchor="end"><tspan font-size="168" fill="#ff2a2a">12時</tspan>'
             '<tspan font-size="84" dx="6">になる前に、</tspan></text>')
    _big(s, 1030, 672, 142, "コードを抜いて", "end")
    return "".join(s)


KINDS = {"L": k_L, "M": k_M, "E": k_E, "D": k_D, "J": k_J, "J2": k_J2, "B": k_B, "C": k_C, "K": k_K, "F": k_F, "G": k_G,
         "L0": k_L0, "L1": k_L1}


def main():
    OUTD.mkdir(parents=True, exist_ok=True)
    kinds = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--kinds=")), "L").split(",")
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
    cols = 2
    rows = (len(kinds) + 1) // cols
    cw, ch = 640 + 8 + 210 + 12, 360 + 28
    sh = Image.new("RGB", (cols * cw, rows * ch), (60, 60, 60))
    d = ImageDraw.Draw(sh)
    for i, k in enumerate(kinds):
        n = f"ep29_N_{k}"
        E.bake2(f"ep29/{n}", KINDS[k]())
        p = OUTD / f"{n}.png"
        im = Image.open(p).convert("RGB")
        print(f"{n}：{im.size}・{p.stat().st_size:,} バイト")
        x, y = (i % cols) * cw, (i // cols) * ch
        d.text((x + 4, y + 2), n, fill=(255, 255, 0), font=font)
        sh.paste(im.resize((640, 360), Image.LANCZOS), (x, y + 28))
        sh.paste(im.resize((210, 118), Image.LANCZOS), (x + 648, y + 28))
    p = OUTD / f"cmp_{'_'.join(kinds)}.jpg"
    sh.save(p, quality=90)
    print(p)


if __name__ == "__main__":
    main()
