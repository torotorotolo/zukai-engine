# -*- coding: utf-8 -*-
"""事故検証チャンネル：サムネ生成器 v4。

■ 縦を稼ぐ理屈（v3の敗因）
v3は「幅いっぱい」を font-size で作っていたので、文字数が多いほど字が小さくなった。
競合の桜木町は7文字なので大きく見えるだけで、11文字を同じ高さで並べたら横に溢れる。
→ **級数は高さで決め打ちし、横は textLength で圧縮する**（縦長のコンデンス書体化）。
   これで文字数に関係なく「幅いっぱい × 縦もでかい」が両立する。

■ 模倣に見せないための独自要素（毎回必ず入る＝チャンネルの顔）
1. **左端の検証タブ** … 縦書きのカテゴリ（鉄道／航空／化学／宇宙…）。
   競合には無く、機能もある（視聴者が系統を覚える）。
2. **ハザードストライプの罫** … 事故調査の警戒色。写真と事故名の境界に1本だけ引く。
3. **原因チップ** … 「原因：〇〇」を先出しする。
   このチャンネルの約束＝「なぜ壊れたかを図解する」を、サムネの時点で宣言する。
   競合は煽り文と事故名だけなので、ここが一番はっきりした差になる。
"""
import base64
import io
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent
W, H = 1280, 720
EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
FONTS = Path(r"C:\Users\konar\Desktop\zankoku-sekkeizu\public\fonts")

TAB_W = 66                      # 左の検証タブ
DELA_EM, HALF_EM = 1.016, 0.55


def fit(text, target_w, want_h, lo=0.66, hi=1.10):
    """高さ want_h を狙い、横は target_w に収める。

    戻り値は font-size。実際の横圧縮は textLength に任せる。
    圧縮率が lo を下回る（潰れすぎる）ときだけ級数を落とす。
    """
    units = sum(HALF_EM if ord(c) < 0x3000 else 1.0 for c in text)
    natural = units * DELA_EM * want_h
    ratio = target_w / natural
    if ratio < lo:
        return target_w / (units * DELA_EM * lo)
    if ratio > hi:
        return target_w / (units * DELA_EM * hi)
    return want_h


def _face(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


def _photo(src, cy=0.34, contrast=1.22, color=1.34, bright=0.90):
    im = Image.open(src).convert("RGB")
    th = int(im.width * 9 / 16)
    if th > im.height:
        tw = int(im.height * 16 / 9)
        box = ((im.width - tw) // 2, 0, (im.width - tw) // 2 + tw, im.height)
    else:
        y = int((im.height - th) * cy)
        box = (0, y, im.width, y + th)
    im = im.crop(box).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(color)
    im = ImageEnhance.Brightness(im).enhance(bright)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def _svg(uri, hook_red, hook_white, sub, title, cause, category, badge):
    hook_w, title_w = 812, 1152
    hk = fit(hook_red + hook_white, hook_w, 96)
    tt = fit(title, title_w, 150)
    stripe_y = 522
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="sT" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#03060a" stop-opacity="0.88"/>
    <stop offset="40%" stop-color="#03060a" stop-opacity="0.62"/>
    <stop offset="100%" stop-color="#03060a" stop-opacity="0"/></linearGradient>
  <linearGradient id="sB" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0%" stop-color="#03060a" stop-opacity="0.96"/>
    <stop offset="46%" stop-color="#03060a" stop-opacity="0.74"/>
    <stop offset="100%" stop-color="#03060a" stop-opacity="0"/></linearGradient>
  <radialGradient id="vig" cx="52%" cy="44%" r="74%">
    <stop offset="46%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity="0.60"/></radialGradient>
  <linearGradient id="red" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ff7a52"/><stop offset="44%" stop-color="#f0250f"/>
    <stop offset="100%" stop-color="#960c03"/></linearGradient>
  <linearGradient id="ylw" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#fff8c2"/><stop offset="44%" stop-color="#ffd21c"/>
    <stop offset="100%" stop-color="#cf8203"/></linearGradient>
  <linearGradient id="wht" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#c5cdd6"/></linearGradient>
  <pattern id="hz" width="30" height="30" patternUnits="userSpaceOnUse"
           patternTransform="rotate(45)">
    <rect width="30" height="30" fill="#14161a"/><rect width="15" height="30" fill="#ffd21c"/>
  </pattern>
  <filter id="sh" x="-14%" y="-14%" width="132%" height="132%">
    <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000" flood-opacity="0.72"/></filter>
</defs>

<image href="{uri}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/>
<rect x="0" y="0" width="{W}" height="286" fill="url(#sT)"/>
<rect x="0" y="{H - 300}" width="{W}" height="300" fill="url(#sB)"/>

<!-- ① 左の検証タブ（毎回入るチャンネルの顔） -->
<rect x="0" y="0" width="{TAB_W}" height="{H}" fill="#101317" opacity="0.94"/>
<rect x="{TAB_W - 7}" y="0" width="7" height="{H}" fill="#ffd21c"/>
<rect x="14" y="26" width="38" height="38" rx="6" fill="#f0250f"/>
<text x="33" y="54" font-family="Dela" font-size="26" fill="#fff" text-anchor="middle">検</text>
<text x="33" y="112" font-family="Noto" font-size="40" font-weight="700" fill="#eef1f4"
      letter-spacing="10" text-anchor="middle"
      style="writing-mode:vertical-rl;text-orientation:upright">{category}</text>

<!-- ② ハザードストライプ（事故調査の警戒色。写真と事故名の境目に1本だけ） -->
<rect x="{TAB_W}" y="{stripe_y}" width="{W - TAB_W}" height="11" fill="url(#hz)" opacity="0.92"/>

<!-- 見出し -->
<text x="{TAB_W + 24}" y="{40 + hk * 0.84:.0f}" font-family="Dela" font-size="{hk:.1f}"
      textLength="{hook_w}" lengthAdjust="spacingAndGlyphs" stroke="#07090c"
      stroke-width="{hk * 0.20:.1f}" stroke-linejoin="round" paint-order="stroke fill"
      filter="url(#sh)"><tspan fill="url(#red)">{hook_red}</tspan
      ><tspan fill="url(#wht)">{hook_white}</tspan></text>

<text x="{TAB_W + 28}" y="{40 + hk * 0.84 + 62:.0f}" font-family="Noto" font-size="44"
      font-weight="700" letter-spacing="-1" fill="url(#wht)" stroke="#07090c" stroke-width="11"
      stroke-linejoin="round" paint-order="stroke fill" filter="url(#sh)">{sub}</text>

<!-- ③ 原因チップ＝このチャンネルの約束を先出しする -->
<g filter="url(#sh)">
  <rect x="{TAB_W + 24}" y="{stripe_y - 82}" width="{18 + len(cause) * 27}" height="56" rx="6"
        fill="#101317" opacity="0.92"/>
  <rect x="{TAB_W + 24}" y="{stripe_y - 82}" width="7" height="56" fill="#ffd21c"/>
  <text x="{TAB_W + 44}" y="{stripe_y - 42}" font-family="Noto" font-size="30" font-weight="700"
        fill="#eef1f4" letter-spacing="0">原因：{cause}</text>
</g>

<!-- 事故名（高さで級数を決め、横は圧縮して幅いっぱいに） -->
<text x="{TAB_W + (W - TAB_W) // 2}" y="676" font-family="Dela" font-size="{tt:.1f}"
      text-anchor="middle" textLength="{title_w}" lengthAdjust="spacingAndGlyphs"
      fill="url(#ylw)" stroke="#07090c" stroke-width="{tt * 0.20:.1f}" stroke-linejoin="round"
      paint-order="stroke fill" filter="url(#sh)">{title}</text>

<!-- 年・場所 -->
<g filter="url(#sh)">
  <rect x="964" y="28" width="286" height="58" rx="8" fill="#101317" opacity="0.92"/>
  <rect x="964" y="28" width="7" height="58" fill="#f0250f"/>
  <text x="1112" y="69" font-family="Noto" font-size="32" font-weight="700" fill="#eef1f4"
        text-anchor="middle" letter-spacing="1">{badge}</text>
</g>
</svg>'''


def make(photo, hook_red, hook_white, sub, title, cause, category, badge, out,
         *, cy=0.34, **grade):
    body = _svg(_photo(HERE / photo, cy=cy, **grade),
                hook_red, hook_white, sub, title, cause, category, badge)
    css = _face("Dela", "DelaGothicOne.woff2") + _face("Noto", "NotoSansJP-Bold.woff2")
    html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
            f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{body}</body></html>')
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "t.html"
        p.write_text(html, encoding="utf-8")
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={W},{H}",
                        f"--screenshot={HERE / out}", "--virtual-time-budget=4000",
                        p.resolve().as_uri()],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("→", out)


if __name__ == "__main__":
    make("dwh.jpg", "87日間", "止まらなかった", "作業員11名死亡・史上最悪の原油流出",
         "メキシコ湾原油流出事故", "セメントの不良", "海洋", "2010・アメリカ", "v4_dwh.png")
    make("chal.jpg", "73秒後", "に空中分解", "乗員7名全員死亡・技術者の警告は退けられた",
         "チャレンジャー号爆発事故", "Oリングの硬化", "宇宙", "1986・アメリカ", "v4_chal.png",
         cy=0.30, contrast=1.16, color=1.10, bright=0.96)
