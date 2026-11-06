# -*- coding: utf-8 -*-
"""30本目 ⑥ サムネの案（SAMUNE の型＝Vault Resources/サムネの型-SAMUNE分析6型-20261103・道具は qa_out/ep28_thumb2.py の部品をそのまま使う）。

言葉＝承認①の題 A の芯「前の年に（松本で）同じ毒」＋問い「止められず」（台本 §1-1・§1-2・c105 c106）＋事件名「地下鉄サリン事件」。
地＝陸上自衛隊の除染の写真（PDL1.0 の読み＝サムネの地も可・① §B2-12・materials.md の #65 が本命）。
守る線＝顔なし（教祖の写真は使わない＝防護マスクの隊員は公的な任務）・「死亡」の語なし・煽り語なし・粒なし
（再圧縮で鮮明さの比が下がる）・右下の再生時間の札（x≥1036・y≥598）に要の字を掛けない。
案は版ごとに名前を分ける（同じ名前へ焼き直さない＝カズヤくんが見比べた絵が消える）。

    python -P qa_out/ep30_thumb.py --kinds=A65,E65,D66,A66   … out/thumb/ep30/ep30_N_<kind>.png と並べ cmp_<kinds>.jpg（640px と 210px）
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "qa_out"))
import ep27_thumb as E  # noqa: E402
from ep28_thumb2 import SHADOW, adv, boxed, stroke, txt, uri, vert  # noqa: E402

W, H = E.W, E.H
SRC = HERE / "ref" / "ep30"
OUTD = HERE / "out" / "thumb" / "ep30"


def photo(name, box, gamma=1.0, tone=(1, 1, 1), bright=1.0, sat=1.0):
    """写真を切り出して全面に。box＝元の写真の (左, 上, 右, 下)・16:9"""
    im = Image.open(SRC / f"{name}.jpg").convert("RGB").crop(box).resize((W, H), Image.LANCZOS)
    a = (np.asarray(im, np.float32) / 255) ** gamma
    a = a * bright * np.array(tone, np.float32)
    if sat != 1.0:
        g = a.mean(axis=2, keepdims=True)
        a = g + (a - g) * sat
    return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))


def _fade(y0, stops=((0, 0), (0.36, 0.94), (1, 1)), gid="fb"):
    st = "".join(f'<stop offset="{o}" stop-color="#000" stop-opacity="{a}"/>' for o, a in stops)
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{st}</linearGradient>',
            f'<rect y="{y0}" width="{W}" height="{H - y0}" fill="url(#{gid})"/>')


def _big(s, x, y, fs, word, anchor="start", col="#ffffff"):
    """最後の語＝白＋赤と水色のずれ（サンプル 1294 の見せ方）"""
    for dx, c in ((-5, "#ff2a2a"), (5, "#22e0ff")):
        s.append(f'<g opacity="0.85">{txt(word, x + dx, y, fs, c, "NSJ", anchor)}</g>')
    s.append(txt(word, x, y, fs, col, "NSJ", anchor))


def _sentence(g, y0):
    """A の並び（28本目 L2・29本目 L）＝上に写真・下を黒へ溶かして、語が段々大きくなる一文。左上に事件の名前（黄に黒い縁）"""
    d, r = _fade(y0)
    s = [f"<defs>{d}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>', r]
    s.append(stroke("地下鉄サリン事件", 36, 84, 60, "#ffe600", "#000", 12, "NSB"))
    adv("前の年にも、同じ毒", 72, "NSJ")
    s.append('<text x="1250" y="548" font-family="NSJ" fill="#ffffff" text-anchor="end"><tspan font-size="72">前の年にも、</tspan>'
             '<tspan font-size="140" fill="#ff2a2a" dx="8">同じ毒</tspan></text>')
    _big(s, 1030, 696, 180, "止められず", "end")
    return "".join(s)


def k_A65():
    """A＝#65（除染活動に向かう隊員の防護マスクと背負いのタンク）を上に大きく・左の人だかりは切る"""
    return _sentence(photo("p65", (420, 200, 1920, 1044), gamma=0.92, bright=1.04, sat=1.08), 430)


def k_A66():
    """A＝#66（電車の中で除染する隊員）＝地下鉄の車内が分かる。上の中吊りの広告は暗くする"""
    g = photo("p66", (300, 190, 1800, 1034), gamma=0.92, bright=1.04, sat=1.08)
    s = _sentence(g, 430)
    top = ('<linearGradient id="ft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.85"/>'
           '<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>')
    return s.replace("<defs>", f"<defs>{top}", 1).replace(
        '<rect y="430"', f'<rect width="{W}" height="130" fill="url(#ft)"/><rect y="430"', 1)


def k_E65():
    """E＝暗い写真に赤い巨大な題字（210px で最も読める）＝#65 を地に・上に事件名・下に黄の1句"""
    g = photo("p65", (300, 100, 1800, 944), gamma=1.0, tone=(0.86, 0.92, 1.0), bright=0.92)
    grad = ('<linearGradient id="rg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5a3c"/>'
            '<stop offset="0.55" stop-color="#e50c0c"/><stop offset="1" stop-color="#8f0000"/></linearGradient>'
            '<linearGradient id="dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.62"/>'
            '<stop offset="0.3" stop-color="#000" stop-opacity="0.12"/><stop offset="0.7" stop-color="#000" stop-opacity="0.12"/>'
            '<stop offset="1" stop-color="#000" stop-opacity="0.86"/></linearGradient>')
    s = [f"<defs>{grad}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dk)"/>']
    s.append(stroke("地下鉄サリン事件", W / 2, 122, 96, "#ffffff", "#000", 14, "NSJ", "middle"))
    fs, t = 330, "同じ毒"
    adv(t, fs, "NSB")
    head = f'x="{W / 2}" y="{H / 2 + 126}" font-family="NSB" font-size="{fs}" text-anchor="middle" stroke-linejoin="round"'
    s.append(f'<text {head} fill="#000" stroke="#000" stroke-width="34" opacity="0.8">{t}</text>')
    s.append(f'<text {head} fill="#fff" stroke="#fff" stroke-width="14">{t}</text>')
    s.append(f'<text {head} fill="url(#rg)">{t}</text>')
    s.append(stroke("前の年にも使われていた", 40, 684, 76, "#ffe600", "#000", 12, "NSJ"))
    return "".join(s)


def k_D66():
    """28本目の公開はじめの d3 の並び＝全面の写真（#66 の車内）・赤い事件名に黒い縁・白の行・黄の1句を左詰め"""
    g = photo("p66", (380, 190, 1780, 978), gamma=0.80, bright=1.12, sat=1.20)
    d, r = _fade(420, ((0, 0), (0.5, 0.82), (1, 0.96)))
    top = ('<linearGradient id="ft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.8"/>'
           '<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>')
    s = [f"<defs>{d}{top}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>',
         f'<rect width="{W}" height="120" fill="url(#ft)"/>', r]
    s.append(stroke("地下鉄サリン事件", 40, 512, 92, "#ff1a1a", "#000", 14, "NSJ"))
    s.append(stroke("前の年にも同じ毒", 40, 606, 76, "#ffffff", "#000", 12, "NSB"))
    s.append(stroke("なぜ止められず？", 40, 694, 76, "#ffe600", "#000", 12, "NSB"))
    return "".join(s)


def k_J65():
    """J2（29本目で選ばれた型）＝左に写真・右と下を黒へ溶かし、右に積んだ一文（同じ毒 を赤で大きく）・左下に黄の事件名"""
    g = photo("p65", (420, 160, 1920, 1004), gamma=0.92, bright=1.04, sat=1.08)
    grad = ('<linearGradient id="fx" x1="0" y1="0" x2="1" y2="0"><stop offset="0.50" stop-color="#050505" stop-opacity="0"/>'
            '<stop offset="0.62" stop-color="#050505" stop-opacity="1"/></linearGradient>'
            '<linearGradient id="fy" x1="0" y1="0" x2="0" y2="1"><stop offset="0.50" stop-color="#050505" stop-opacity="0"/>'
            '<stop offset="0.64" stop-color="#050505" stop-opacity="1"/></linearGradient>')
    s = [f"<defs>{grad}</defs>", f'<image href="{uri(g, "JPEG")}" x="-200" width="{W}" height="{H}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#fx)"/><rect width="{W}" height="{H}" fill="url(#fy)"/>']
    s.append(txt("前の年にも", 1256, 112, 96, "#ffffff", "NSJ", "end"))
    adv("同じ毒", 216, "NSJ")
    for dx, col in ((-5, "#ff2a2a"), (5, "#22e0ff")):
        s.append(f'<g opacity="0.85">{txt("同じ毒", 1256 + dx, 336, 216, col, "NSJ", "end")}</g>')
    s.append(txt("同じ毒", 1256, 336, 216, "#ff2020", "NSJ", "end"))
    s.append(txt("止められず", 1256, 590, 200, "#ffffff", "NSJ", "end"))
    s.append(txt("地下鉄サリン事件", 34, 690, 62, "#ffe600", "NSB"))
    return "".join(s)


def k_C65():
    """C（報道の見出し）＝写真に箱の字を積む。上に黄の札・下に赤い帯の問い（28本目 k_C の作り）"""
    g = photo("p65", (300, 120, 1800, 964), gamma=0.92, bright=1.04)
    s = [f"<defs>{SHADOW}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>']
    b0, _, b = boxed("地下鉄サリン事件（1995年）", 30, 30, 52, "#fbe30e", "#0a0a0a", pad=14)
    s.append(b0)
    b1, _, b = boxed("前の年にも", 30, b + 18, 140, "#ffffff", "#0a0a0a")
    s.append(b1)
    b2, _, b = boxed("同じ毒", 30, b + 10, 140, "#ffffff", "#0a0a0a", rich=[("同じ毒", "#d40000")])
    s.append(b2)
    s.append(f'<rect x="0" y="{H - 158}" width="{W}" height="158" fill="#c40606"/>')
    s.append(txt("なぜ止められなかった？", W / 2, H - 40, 108, "#ffffff", "NSJ", "middle"))
    return "".join(s)


def k_F65():
    """F（赤板の縦書き＝最も華やか）＝明るい写真の右に赤い板・縦書きの黄と白の大きな字（28本目 k_F の作り）"""
    g = photo("p65", (180, 100, 1680, 944), gamma=0.90, bright=1.06, sat=1.10)
    grad = ('<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e30d0d"/>'
            '<stop offset="1" stop-color="#a80000"/></linearGradient>')
    s = [f"<defs>{SHADOW}{grad}</defs>", f'<image href="{uri(g, "JPEG")}" width="{W}" height="{H}"/>']
    s.append(f'<polygon points="868,0 {W},0 {W},{H} 796,{H}" fill="url(#pn)"/>')
    b0, _, _ = boxed("地下鉄サリン事件", 26, 26, 66, "#fbe30e", "#0a0a0a", pad=14)
    s.append(b0)
    s.append(vert("同じ毒", 1016, 150, 140, "#ffe600", "NSB", 14))
    s.append(vert("前の年にも", 1190, 140, 100, "#ffffff", "NSB", 12))
    return "".join(s)


KINDS = {"A65": k_A65, "A66": k_A66, "E65": k_E65, "D66": k_D66, "J65": k_J65, "C65": k_C65, "F65": k_F65}


def main():
    OUTD.mkdir(parents=True, exist_ok=True)
    kinds = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--kinds=")), "A65").split(",")
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
    cols = 2
    rows = (len(kinds) + 1) // cols
    cw, ch = 640 + 8 + 210 + 12, 360 + 28
    sh = Image.new("RGB", (cols * cw, rows * ch), (60, 60, 60))
    d = ImageDraw.Draw(sh)
    for i, k in enumerate(kinds):
        n = f"ep30_N_{k}"
        E.bake2(f"ep30/{n}", KINDS[k]())
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
