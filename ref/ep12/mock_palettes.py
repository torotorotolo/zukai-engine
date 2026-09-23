# -*- coding: utf-8 -*-
"""⑤b 相談用の見本（本番には入れない）。
章ごとの色の候補を、本番と同じ経路（jiko_style の SVG → headless Chrome）で焼いて 3×3 に並べる。
あわせて測る：①色を差し替えたときの文字のコントラスト（地との比）
              ②描画コードに直書きされた色（トークンを差し替えても変わらない色）の数
              ③1コマを Chrome で焼く秒数（コマごとに SVG が要る演出の費用の見立て）
"""
import base64
import io
import re
import sys
import time
from pathlib import Path

REPO = Path(r"C:/Users/konar/Desktop/zukai-engine")
sys.path.insert(0, str(REPO / "tools"))
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

import jiko_style as J
import render

# 2026-09-23 ⑤bの相談で使った見本（決定＝記憶 project-jiko-visual-variety-from-ep12）。
# 出力は git の外（out/ は .gitignore）。
OUTD = REPO / "out" / "style_mock"
OUTD.mkdir(parents=True, exist_ok=True)
IMG = REPO / "ref" / "ep12" / "img"

try:
    import scene_jiko as S
    PAGE = S.page
    print("page: scene_jiko.page を使用")
except Exception as e:  # import の副作用で落ちたら、同じ書体で自前に組む
    print("page: scene_jiko の import に失敗 → 自前の CSS:", repr(e)[:160])

    def _ff(name, f):
        b = base64.b64encode((REPO / "fonts" / f).read_bytes()).decode()
        return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
                f"format('woff2');font-weight:400;font-display:block;}}")
    _CSS = _ff("Dela", "DelaGothicOne.woff2") + _ff("Noto", "NotoSansJP-Bold.woff2")

    def PAGE(inner, w=1920, h=1080):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
               f'viewBox="0 0 {w} {h}">{inner}</svg>')
        return (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{_CSS}'
                f'body{{width:{w}px;height:{h}px;overflow:hidden}}</style></head>'
                f'<body>{svg}</body></html>')

TOK = ["BG", "BG2", "GRID", "LINE", "LINE_DIM", "TICK", "INK_W", "ALERT", "ALERT_DIM",
       "AMBER", "OK", "INST", "INST_DIM", "DOC", "DOC_DIM"]
BASE = {k: getattr(J, k).lower() for k in TOK}

PAL = {
    "navy":   dict(ov={}, duo=("#16232e", "#e6eef2")),
    "mono":   dict(ov=dict(BG="#111111", BG2="#1b1b1b", GRID="#2b2b2b", LINE="#bcbcbc",
                           LINE_DIM="#5c5c5c", TICK="#a6a6a6", INK_W="#f2f2f2"),
                   duo=("#161616", "#efefef")),
    "night":  dict(ov=dict(BG="#0a0d1f", BG2="#111633", GRID="#1b2246", LINE="#a3b1e6",
                           LINE_DIM="#3d4880", TICK="#8c9ad0", INK_W="#eef0fb"),
                   duo=("#0e1330", "#dfe4fb")),
    "copper": dict(ov=dict(BG="#1b0f0c", BG2="#2a1713", GRID="#3d231c", LINE="#e2b39b",
                           LINE_DIM="#744536", TICK="#cf9f88", INK_W="#faece4"),
                   duo=("#2a1511", "#fbe3cf")),
    "sepia":  dict(ov=dict(BG="#17120c", BG2="#241c13", GRID="#362a1c", LINE="#d8c19c",
                           LINE_DIM="#6d5a40", TICK="#bca57f", INK_W="#f6eee0"),
                   duo=("#241a10", "#f3e7cf")),
    "teal":   dict(ov=dict(BG="#0a1a1a", BG2="#112626", GRID="#1c3837", LINE="#8ccbbf",
                           LINE_DIM="#3b6b64", TICK="#7cb3aa", INK_W="#e6f6f2"),
                   duo=("#0f2423", "#def3ee")),
    "paper":  dict(ov=dict(BG="#efe9dc", BG2="#e3dccb", GRID="#d6cdb8", LINE="#34414b",
                           LINE_DIM="#9b927f", TICK="#4e5a63", INK_W="#161b20", ALERT="#b3301c",
                           ALERT_DIM="#d9a193", AMBER="#8a5d00", OK="#2e7d57", INST="#5f4590",
                           INST_DIM="#c9bfe0", DOC="#6e4f1f", DOC_DIM="#cdbb98"),
                   duo=("#2b2a26", "#f4efe4")),
}


def remap(svg, pal):
    m = {BASE[k]: v for k, v in PAL[pal]["ov"].items()}
    return re.sub(r"#[0-9a-fA-F]{6}", lambda x: m.get(x.group(0).lower(), x.group(0)), svg)


def load(name, maxside=2400):
    im = Image.open(IMG / name)
    if im.format == "JPEG":
        im.draft("RGB", (maxside, maxside))
    im = im.convert("RGB")
    if max(im.size) > maxside:
        s = maxside / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return im


def cover(im, w, h, bias=0.5, xbias=0.5):
    sw, sh = im.size
    z = max(w / sw, h / sh)
    cw, ch = w / z, h / z
    l, t = (sw - cw) * xbias, (sh - ch) * bias
    return im.crop((round(l), round(t), round(l + cw), round(t + ch))).resize((w, h), Image.LANCZOS)


def duo(im, dark, light):  # build_jiko.duotone と同じ式
    g = im.convert("L")
    d = [int(dark[i:i + 2], 16) for i in (1, 3, 5)]
    lt = [int(light[i:i + 2], 16) for i in (1, 3, 5)]
    lut = []
    for c in range(3):
        lut += [int(d[c] + (lt[c] - d[c]) * (v / 255.0)) for v in range(256)]
    return g.convert("RGB").point(lut)


def uri(im):
    b = io.BytesIO()
    im.save(b, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def subband(line):
    return ('<defs><linearGradient id="sb" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#000000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000000" stop-opacity="0.78"/></linearGradient></defs>'
            '<rect x="0" y="900" width="1920" height="180" fill="url(#sb)"/>'
            f'<text x="960" y="1032" font-family="Noto" font-size="38" fill="#ffffff" '
            f'text-anchor="middle" stroke="#000000" stroke-width="7" stroke-linejoin="round" '
            f'paint-order="stroke fill">{line}</text>')


def frame_svg(photo, t, sub, chn, chname, big, lab, src, inst, line):
    x0, y0, w, h = J.MG, J.BAND_T, J.PHOTO_W, J.PHOTO_H
    cx = J.COL_R[0]
    return "".join([
        J.frame(1920, 1080),
        f'<image href="{uri(photo)}" x="{x0}" y="{y0}" width="{w}" height="{h}" '
        f'preserveAspectRatio="none"/>',
        f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="{J.LINE}" '
        f'stroke-width="3"/>',
        J.label(cx, 300, lab, col=J.TICK, size=30),
        J.big(cx, 405, big, col=J.AMBER, size=92),
        J.rule(cx, J.RIGHT, 450, col=J.ALERT, w=4),
        J.label(cx, 520, src, col=J.DOC, size=30),
        J.label(cx, 575, inst, col=J.INST, size=30),
        J.title(t, sub),
        J.chapter(chn, 9, chname),
        subband(line),
    ])


def card_svg(photo, n, name):
    return (f'<rect width="1920" height="1080" fill="{J.BG}"/>'
            f'<image href="{uri(photo)}" x="0" y="0" width="1920" height="1080" '
            f'preserveAspectRatio="none" opacity="0.42"/>'
            + J.grid_only(1920, 1080, op=0.35) +
            f'<text x="960" y="470" font-family="Dela" font-size="64" fill="{J.AMBER}" '
            f'text-anchor="middle">第{n}章</text>'
            f'<text x="960" y="640" font-family="Noto" font-size="132" fill="{J.INK_W}" '
            f'text-anchor="middle" stroke="{J.BG}" stroke-width="10" stroke-linejoin="round" '
            f'paint-order="stroke fill">{name}</text>'
            f'<path d="M660 700 H1260" stroke="{J.ALERT}" stroke-width="6"/>')


PW, PH = J.PHOTO_W, J.PHOTO_H
blast = load("Castle Bravo Blast.jpg")
C1 = ("爆発は予想をはるかに超えた", "ブラボーの火球（1954年3月1日）", 1, "予想をはるかに超えた爆発",
      "1500万トン", "TNT火薬に直した威力", "出典：国防総省の機関の報告書", "アメリカ原子力委員会",
      "爆発は、広島の原爆のおよそ1000倍。")
TILES = [
    ("① 現行（11本目まで）＝紺の設計図", "navy", "frame", cover(blast, PW, PH, 0.4), C1),
    ("② 紺の地＋写真は原色（同じ火球）", "navy", "frame_raw", cover(blast, PW, PH, 0.4), C1),
    ("③ 赤銅＝爆発の章（同じ火球）", "copper", "frame", cover(blast, PW, PH, 0.4),
     C1[:2] + (5, "1500万トン") + C1[4:]),
    ("④ 白黒＝水爆の歴史の章", "mono", "frame",
     cover(load("Castle Bravo Shrimp Device 002.jpg"), PW, PH, 0.5),
     ("運べる大きさの水爆を目指した", "シュリンプ装置", 2, "水素爆弾と、キャッスル作戦", "1954年",
      "キャッスル作戦", "出典：国防総省の機関の報告書", "アメリカ原子力委員会",
      "爆発したのは、「シュリンプ」と呼ばれた装置である。")),
    ("⑤ 夜の藍＝撃つ前の夜の章", "night", "frame",
     cover(load("BravoShotCab.jpg"), PW, PH, 0.5),
     ("撃つ前の夜の風", "撃つ装置を置いた小屋", 4, "撃つ前の夜の風", "午前6時45分",
      "撃った時刻（現地）", "出典：国防総省の機関の報告書", "アメリカ原子力委員会",
      "1954年3月1日、午前6時45分。太平洋のまん中の、ビキニ環礁。")),
    ("⑥ セピア＝日本の章", "sepia", "frame",
     cover(load("Technical experts checking contamination by nuclear fallout of Tunas after Dai5 "
                "Fukuryū maru Incident - 1954 - The Yomiuri Shimbun.png"), PW, PH, 0.5),
     ("灰は日本の漁船にも降った", "マグロの放射線を測る（1954年）", 6, "第五福竜丸", "157キロ",
      "ビキニ環礁から船まで", "出典：日本政府の当時の記録", "国会の議事録",
      "その先の海にいたのが、日本のマグロ漁船「第五福竜丸」である。")),
    ("⑦ 青緑＝島に降った灰の章", "teal", "frame",
     cover(load("Bikini Atoll - NARA - 140696551.jpg"), PW, PH, 0.5),
     ("灰は東の島々にも降った", "ビキニ環礁の空撮", 7, "島に降った灰", "239人",
      "灰の放射線を浴びた住民", "出典：国防総省の機関の報告書", "アメリカ原子力委員会",
      "東の島々でも、住民239人とアメリカ兵28人が、灰の放射線を浴びた。")),
    ("⑧ 紙の地＝報告書を読む場面", "paper", "frame",
     cover(load("AEC Authorization for Operation Castle.png"), PW, PH, 0.15),
     ("報告書を英語の原文で読む", "キャッスル作戦を認めた文書", 1, "予想をはるかに超えた爆発",
      "1982年", "国防総省の機関の報告書", "出典：国防総省の機関の報告書", "アメリカ原子力委員会",
      "この動画は、アメリカ政府の報告書を、英語の原文で読んで作っている。")),
    ("⑨ 章の扉（見本）＝赤銅で第5章の頭", "copper", "card",
     cover(load("Castle Bravo 005.jpg"), 1920, 1080, 0.5), (5, "1500万トン")),
]

times = []
frames = []
for i, (cap, pal, kind, ph, a) in enumerate(TILES, 1):
    d = PAL[pal]["duo"]
    if kind == "frame_raw":
        photo = ph
    else:
        photo = duo(ph, *d)
    svg = card_svg(photo, *a) if kind == "card" else frame_svg(photo, *a)
    svg = remap(svg, pal)
    out = OUTD / f"tile{i}_{pal}.png"
    t0 = time.time()
    render.png(PAGE(svg), out, 1920, 1080)
    times.append(time.time() - t0)
    frames.append((cap, out))
    print(f"tile{i} {pal:6s} {kind:9s} {times[-1]:.2f}s  {out.name}")

# ── 3×3 のシート ───────────────────────────────
FONT = None
for f in ["C:/Windows/Fonts/YuGothB.ttc", "C:/Windows/Fonts/meiryob.ttc",
          "C:/Windows/Fonts/meiryo.ttc", "C:/Windows/Fonts/msgothic.ttc"]:
    if Path(f).exists():
        FONT = ImageFont.truetype(f, 34)
        break
TW, TH = 960, 540
sheet = Image.new("RGB", (TW * 3, TH * 3), "#000000")
dr = ImageDraw.Draw(sheet)
for i, (cap, out) in enumerate(frames):
    im = Image.open(out).convert("RGB").resize((TW, TH), Image.LANCZOS)
    x, y = (i % 3) * TW, (i // 3) * TH
    sheet.paste(im, (x, y))
    bb = dr.textbbox((0, 0), cap, font=FONT)
    dr.rectangle((x, y, x + bb[2] + 24, y + bb[3] + 16), fill="#000000")
    dr.text((x + 12, y + 6), cap, font=FONT, fill="#ffe14d")
    dr.rectangle((x, y, x + TW - 1, y + TH - 1), outline="#ffffff", width=2)
sp = OUTD / "palette_sheet.jpg"
sheet.save(sp, quality=90)
print("sheet:", sp, sheet.size)


# ── ①コントラスト（WCAG・地 BG に対して） ────────────────
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


print("\n== 文字の色と地の比（4.5未満は × ）")
TXT = ["INK_W", "LINE", "TICK", "AMBER", "ALERT", "DOC", "INST", "OK"]
print("palette  " + "  ".join(f"{k:>6s}" for k in TXT))
for p in PAL:
    col = dict(BASE, **{k: v.lower() for k, v in PAL[p]["ov"].items()})
    row = []
    for k in TXT:
        r = ratio(col[k], col["BG"])
        row.append(f"{r:5.2f}{'×' if r < 4.5 else ' '}")
    print(f"{p:8s} " + "  ".join(row))

# ── ②直書きの色（トークンを差し替えても変わらない色） ──────
print("\n== 描画コードに直書きされた6桁の色（トークン以外）")
vals = set(BASE.values())
files = [REPO / "tools" / f for f in ("titan_fig.py", "scene_jiko.py", "build_jiko.py", "jiko_style.py")]
files += sorted((REPO / "tools" / "cuts").glob("*.py"))
for f in files:
    txt = f.read_text(encoding="utf-8")
    hx = [h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}\b", txt)]
    other = [h for h in hx if h not in vals]
    from collections import Counter
    top = Counter(other).most_common(6)
    print(f"{f.name:16s} 全{len(hx):4d}  トークン以外 {len(other):3d}  {top}")

print(f"\n== Chrome 1コマ: 平均 {sum(times)/len(times):.2f}s  最大 {max(times):.2f}s  (n={len(times)})")
