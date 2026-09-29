# -*- coding: utf-8 -*-
"""14本目 ⑥-2 字幕デザインの見本。

本番（tools/scene_jiko.py の sub_row・sub_ys・sub_band）と同じ置き方：
  帯 y900〜1080 真っ黒（SUB_BAND "solid"）・56px・1行 y1000・2行 y968／1044・x960 中央・
  stroke-linejoin round・paint-order "stroke fill"。折り目は本番の wrap2（書体の字幅で測る）。

使い方:
  python make_samples.py --check            … 「いま」を描いて r01 の本物のコマと画素で比べる（見本の置き方の検算）
  python make_samples.py --kei <font> A B C … 案ごとのシート（1920×(44+300×3)）を書く
"""
import base64
import sys
from pathlib import Path

REPO = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(REPO / "tools"))
import render                                   # noqa: E402
import fontmetrics as fm                        # noqa: E402
import scene_jiko as S                          # noqa: E402

import numpy as np                              # noqa: E402
from PIL import Image                           # noqa: E402

SP = Path(__file__).resolve().parent
W, H, SUB_Y, SIZE = 1920, 1080, 900, 56
CROP = (780, 300)                                # シートに出す範囲（y780〜1080）

# 見本の3段（地のコマ・話し手・字幕）＝ c103 と c101 の本物の字幕
CASES = [
    ("r01_at_19.0.png", "q", "船長たちは？"),
    ("r01_at_21.0.png", None, "その数分前、助けに来た海洋警察の船に乗り移っていた。"),
    ("r01_at_1.5.png", None, "2014年4月16日の朝。韓国の南西の海で、旅客船セウォル号が傾いた。"),
]

# 話し手ごとの字の色・フチの色・フチの太さ（56px で）。outer＝2重フチの外側（色, 太さ）
DESIGNS = {
    "now": dict(label="いま（r01）　語り＝白＋黒フチ／聞き役＝水色＋黒フチ・Noto Sans JP Bold",
                fam="Noto", a=dict(fill="#eaf2f6", stroke="#000", sw=10),
                q=dict(fill="#8fb6c9", stroke="#000", sw=10)),
    "A": dict(label="案A 字に色（競合と同じ型）　まりさ＝黄の字＋黒フチ／れいむ＝赤の字＋白フチ・けいふぉんと",
              fam="Kei", a=dict(fill="#ffe600", stroke="#000", sw=10),
              q=dict(fill="#ff3030", stroke="#ffffff", sw=10)),
    "A2": dict(label="決定（案A＋黄の字も白フチ）　まりさ＝黄の字＋白フチ／れいむ＝赤の字＋白フチ・けいふぉんと",
               fam="Kei", a=dict(fill="#ffe600", stroke="#ffffff", sw=10),
               q=dict(fill="#ff3030", stroke="#ffffff", sw=10)),
    "B": dict(label="案B フチに色（YMM4 の初期設定の型）　白い字＋まりさ＝黄のフチ／れいむ＝赤のフチ・けいふぉんと",
              fam="Kei", a=dict(fill="#ffffff", stroke="#ffd900", sw=12),
              q=dict(fill="#ffffff", stroke="#e00000", sw=12)),
    "C": dict(label="案C 黄を淡く　まりさ＝淡い黄の字＋黒フチ／れいむ＝赤の字＋白フチ・けいふぉんと",
              fam="Kei", a=dict(fill="#fff2a8", stroke="#000", sw=10),
              q=dict(fill="#ff3030", stroke="#ffffff", sw=10)),
}


def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()


def face(name, path):
    p = Path(path)
    mime, fmt = {".woff2": ("font/woff2", "woff2"), ".otf": ("font/otf", "opentype")}.get(
        p.suffix.lower(), ("font/ttf", "truetype"))
    return (f"@font-face{{font-family:'{name}';src:url(data:{mime};base64,{b64(p)}) "
            f"format('{fmt}');font-weight:400;font-display:block;}}")


def ys(n):
    return [SUB_Y + v for v in ([100.0] if n == 1 else [68.0, 144.0])]


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def use_font_for_wrap(fam, path):
    """本番の wrap2 は fm の "Noto" で測る＝見本の間だけ "Noto" の物差しを見本の書体に差し替える。"""
    if fam == "Noto":
        return
    from fontTools.ttLib import TTFont
    ft = TTFont(path, lazy=True)
    fm._FONTS["Noto"] = (ft, ft.getBestCmap(), ft["hmtx"], ft["head"].unitsPerEm, ft.getGlyphSet())
    fm.adv.cache_clear()


def text_svg(lines, fam, st):
    out = []
    for t, y in zip(lines, ys(len(lines))):
        if st.get("outer"):
            oc, ow = st["outer"]
            out.append(f'<text x="960" y="{y:.0f}" font-family="{fam}" font-size="{SIZE}" fill="{oc}" '
                       f'text-anchor="middle" stroke="{oc}" stroke-width="{ow}" '
                       f'stroke-linejoin="round">{esc(t)}</text>')
        out.append(f'<text x="960" y="{y:.0f}" font-family="{fam}" font-size="{SIZE}" fill="{st["fill"]}" '
                   f'text-anchor="middle" stroke="{st["stroke"]}" stroke-width="{st["sw"]}" '
                   f'stroke-linejoin="round" paint-order="stroke fill">{esc(t)}</text>')
    return "".join(out)


def frame_svg(bg, lines, fam, st, crop=None):
    vb, h = (f"0 {crop[0]} {W} {crop[1]}", crop[1]) if crop else (f"0 0 {W} {H}", H)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="{vb}" '
            f'style="display:block">'
            f'<image href="data:image/png;base64,{bg}" x="0" y="0" width="{W}" height="{H}"/>'
            f'<rect x="0" y="{SUB_Y}" width="{W}" height="{H - SUB_Y}" fill="#000"/>'
            + text_svg(lines, fam, st) + "</svg>")


def css(fam, font_path):
    c = S.face_css("NotoM", "NotoSansJP-Medium.woff2") + S.face_css("Noto", "NotoSansJP-Bold.woff2")
    if fam != "Noto":
        c += face(fam, font_path)
    return c


def lines_of(text):
    return S.wrap2(text)


def check():
    """「いま」を本番の置き方で描き、r01 の本物のコマと帯の中を比べる（字の外接枠・平均の差）。"""
    d = DESIGNS["now"]
    for i, (bgname, who, text) in enumerate(CASES):
        bg = SP / bgname
        lines = lines_of(text)
        st = d["q"] if who == "q" else d["a"]
        html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css("Noto", None)}'
                f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>'
                f'{frame_svg(b64(bg), lines, "Noto", st)}</body></html>')
        out = SP / f"check_now_{i}.png"
        render.png(html, out, W, H)
        a = np.asarray(Image.open(out).convert("RGB")).astype(int)[SUB_Y:]
        b = np.asarray(Image.open(bg).convert("RGB")).astype(int)[SUB_Y:]

        def bbox(x):
            m = x.max(axis=2) > 80
            yy, xx = np.where(m)
            return (xx.min(), yy.min() + SUB_Y, xx.max(), yy.max() + SUB_Y) if len(xx) else None
        mad = np.abs(a - b).mean()
        big = (np.abs(a - b).max(axis=2) > 64).mean() * 100
        print(f"case{i} 行={lines} 見本の枠={bbox(a)} r01の枠={bbox(b)} 平均の差={mad:.2f} 差>64の画素={big:.2f}%")


def sheet(key, font_path):
    d = DESIGNS[key]
    fam = d["fam"]
    use_font_for_wrap(fam, font_path)
    parts = []
    for bgname, who, text in CASES:
        lines = lines_of(text)
        st = d["q"] if who == "q" else d["a"]
        parts.append(frame_svg(b64(SP / bgname), lines, fam, st, crop=CROP))
        print(f"  {key} {'れいむ' if who == 'q' else 'まりさ'}: {' ／ '.join(lines)}")
    hh = 44 + CROP[1] * len(CASES)
    html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css(fam, font_path)}'
            f'body{{width:{W}px;height:{hh}px;overflow:hidden;background:#000}}'
            f'.lb{{height:44px;line-height:44px;background:#2a2f36;color:#fff;font:26px NotoM;padding-left:18px}}'
            f'</style></head><body><div class="lb">{esc(d["label"])}</div>{"".join(parts)}</body></html>')
    out = SP / f"sheet_{key}.png"
    render.png(html, out, W, hh)
    print(f"  → {out.name}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--check" in args:
        check()
    else:
        kei = args[args.index("--kei") + 1] if "--kei" in args else None
        keys = [a for a in args if a in DESIGNS]
        for k in keys:
            sheet(k, kei)
