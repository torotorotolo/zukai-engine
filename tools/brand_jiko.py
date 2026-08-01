# -*- coding: utf-8 -*-
"""チャンネル「そのとき、何が起きたか」のアイコンとバナー。

■ なぜ AI 生成画像を使わないか（2026-08-01）
  カズヤくんから「OpenAI API を使ってもよい」と言われたが、使わない判断をした。
  1. **無料**なので納得まで作り直せる（課金APIは2回で止める決まりがある）
  2. このチャンネルの正体は**図解**。AI生成画像は本編と質感が合わず浮く
     （スカッとで実証済み：[[feedback-no-ai-images-sukatto]]）
  3. **数値で置ける**。バナーは端末ごとに見える範囲が変わるので、
     安全領域を px で管理できることが決定的に効く

■ アイコンの考え方
  チャンネル名の「そのとき」＝**時間軸上の一点**。
  本編の `timeline` 型がまさにその形なので、**本編とアイコンが同じ語彙になる**。
  テーマ（事故・事件・心霊スポットの由来…）を一切限定しないのも条件に合う。

  🔴 アイコンは**24px でも判別できること**が最優先。
     コメント欄・登録リストではその大きさでしか出ない。
     細い線や文字は消えるので、**太い横線＋赤い縦マーカー**という
     いちばん単純な形にした。`--check` で 24px まで縮めて確認できる。

  ⚠️ YouTube はアイコンを**円形に切り抜く**。800×800 の四隅は必ず切れる。
     大事なものは内接円（半径400）のさらに内側に置く。

■ バナーの考え方
  🔴 YouTube のバナーは端末で見える範囲が違う。
       テレビ      2048×1152（全部見える）
       パソコン    2048× 423
       **全端末で安全なのは中央の 1235×338 だけ**
     → 文字は**必ず 1235×338 の中**に入れる。外側は模様だけにする。

  ⚠️ 写真を敷かない。写真を敷くとテーマが1つに固定されて見える
     （潜水艇の写真を敷いたら「潜水艇のチャンネル」に見える）。

使い方:
    python tools/brand_jiko.py            … アイコンとバナーを焼く
    python tools/brand_jiko.py --check    … 24px まで縮めた確認シートも出す
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw

import jiko_style as J
import render

HERE = Path(__file__).parent.parent
FONTS = HERE / "fonts"
OUT = HERE / "out" / "brand"

NAME = "そのとき、何が起きたか"
TAGLINE = "一次資料と図解で、実際に起きたことを追う"

# ── アイコン ──────────────────────────────────────────────
IC = 800                      # YouTube の推奨は 800×800
IC_SAFE = 0.86                # 円で切られるので、この割合の内側だけ使う

# ── バナー ────────────────────────────────────────────────
BN_W, BN_H = 2048, 1152
SAFE_W, SAFE_H = 1235, 338    # 全端末で見える中央の箱
SAFE_X, SAFE_Y = (BN_W - SAFE_W) // 2, (BN_H - SAFE_H) // 2


def face(name, filename, weight=400):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:{weight};font-display:block;}}")


def css():
    return (face("Dela", "DelaGothicOne.woff2")
            + face("Noto", "NotoSansJP-Bold.woff2")
            + face("NotoM", "NotoSansJP-Medium.woff2"))


def bake(name, inner, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}">{inner}</svg>')
    html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css()}'
            f'body{{width:{w}px;height:{h}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')
    OUT.mkdir(parents=True, exist_ok=True)
    render.png(html, OUT / f"{name}.png", w, h)
    print(f"  {name}.png  {w}×{h}", flush=True)
    return OUT / f"{name}.png"


def grid(w, h, pitch, heavy, op=1.0, col=None):
    """方眼。本編の地とそろえる（`jiko_style.frame` と同じ考え方）。"""
    c = col or J.GRID
    g = [f'<g opacity="{op}">']
    for x in range(0, w + 1, pitch):
        g.append(f'<path d="M{x} 0 V{h}" stroke="{c}" stroke-width="{w/1920*1.6:.1f}"/>')
    for y in range(0, h + 1, pitch):
        g.append(f'<path d="M0 {y} H{w}" stroke="{c}" stroke-width="{w/1920*1.6:.1f}"/>')
    for x in range(0, w + 1, heavy):
        g.append(f'<path d="M{x} 0 V{h}" stroke="{c}" stroke-width="{w/1920*3.4:.1f}"/>')
    for y in range(0, h + 1, heavy):
        g.append(f'<path d="M0 {y} H{w}" stroke="{c}" stroke-width="{w/1920*3.4:.1f}"/>')
    return "".join(g) + "</g>"


# ══════════════════════════════════════════════════════════
#  アイコン
# ══════════════════════════════════════════════════════════
def _icon_ground(ticks=True):
    cx = cy = IC / 2
    r = IC / 2 * IC_SAFE
    g = [f'<rect width="{IC}" height="{IC}" fill="{J.BG}"/>',
         grid(IC, IC, 50, 200, 0.85),
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{J.BG2}" opacity="0.55"/>']
    return g, cx, cy, r


def icon_moment(ticks=True):
    """A案：時間軸の上の「その一点」。

    🔴 最初の版は 24px で赤い点が沈んだ。**線を太く・印を大きく**した。
       目安：印の縦幅を円の 62%、線の太さを画像の 5.5% まで上げる。
       小さく出たときに残るのは「太い横線を赤い縦棒が貫いている」形だけ。
    """
    g, cx, cy, r = _icon_ground()
    x0, x1 = cx - r * 0.88, cx + r * 0.88
    g.append(f'<path d="M{x0:.0f} {cy:.0f} H{x1:.0f}" stroke="{J.LINE}" '
             f'stroke-width="{IC*0.064:.1f}" stroke-linecap="round"/>')
    if ticks:
        for k in (-2, -1, 1, 2):
            x = cx + k * r * 0.36
            g.append(f'<path d="M{x:.0f} {cy - IC*0.062:.0f} V{cy + IC*0.062:.0f}" '
                     f'stroke="{J.LINE_DIM}" stroke-width="{IC*0.024:.1f}" '
                     f'stroke-linecap="round"/>')
    # 🔴 縦の印は**円の高さの7割**まで伸ばす。24px で残るのはこの1本だけ。
    g.append(f'<path d="M{cx:.0f} {cy - r*0.72:.0f} V{cy + r*0.46:.0f}" '
             f'stroke="{J.ALERT}" stroke-width="{IC*0.125:.1f}" stroke-linecap="round"/>')
    # 「その一点」を示す丸。中を地の色で抜いて、縦線と別のものだと分かるようにする
    g.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{IC*0.152:.0f}" fill="{J.ALERT}"/>')
    g.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{IC*0.060:.0f}" fill="{J.BG}"/>')
    return "".join(g)


def icon_section():
    """B案：断面。厚い層を赤い破断線が横切る。

    「図解で構造を見る」チャンネルであることが一目で出る。
    層＝どんな題材にも当てはまる抽象（建物・機体・地層・組織）。
    """
    g, cx, cy, r = _icon_ground()
    lay, h = 4, IC * 0.088
    top = cy - (lay * h + (lay - 1) * IC * 0.026) / 2
    w = r * 1.42
    for i in range(lay):
        y = top + i * (h + IC * 0.026)
        col = J.LINE if i % 2 == 0 else J.LINE_DIM
        g.append(f'<rect x="{cx - w/2:.0f}" y="{y:.0f}" width="{w:.0f}" '
                 f'height="{h:.0f}" rx="{IC*0.014:.0f}" fill="{col}"/>')
    # 赤い破断線（層を斜めに割る）
    g.append(f'<path d="M{cx - w*0.34:.0f} {cy - IC*0.30:.0f} '
             f'L{cx + w*0.10:.0f} {cy:.0f} L{cx - w*0.16:.0f} {cy + IC*0.30:.0f}" '
             f'stroke="{J.ALERT}" stroke-width="{IC*0.075:.1f}" fill="none" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(g)


def icon_question():
    """C案：赤い縦線1本だけ。**いちばん強く、いちばん抽象的。**

    「ここ」という指し示しだけを残した形。24px でも絶対に消えない。
    ただし何のチャンネルかは伝わらないので、名前とセットで効く。
    """
    g, cx, cy, r = _icon_ground()
    g.append(f'<path d="M{cx - r*0.86:.0f} {cy:.0f} H{cx + r*0.86:.0f}" '
             f'stroke="{J.LINE}" stroke-width="{IC*0.072:.1f}" stroke-linecap="round"/>')
    g.append(f'<path d="M{cx:.0f} {cy - r*0.80:.0f} V{cy + r*0.80:.0f}" '
             f'stroke="{J.ALERT}" stroke-width="{IC*0.135:.1f}" stroke-linecap="round"/>')
    return "".join(g)


# ══════════════════════════════════════════════════════════
#  バナー
# ══════════════════════════════════════════════════════════
def banner():
    """🔴 文字は**必ず安全領域（中央 1235×338）の中**に収める。

    ⚠️ 最初の版は見出しを 104px と**当て推量**で置いたので、
       12文字 ＝ 1,248px になり、**安全領域を右に47px はみ出した**
       （さらに右端の赤い印とも重なった）。
       級数は推定で置かない ── フォントから実測して収める。
    """
    import fontmetrics as fm

    g = [f'<rect width="{BN_W}" height="{BN_H}" fill="{J.BG}"/>',
         grid(BN_W, BN_H, 64, 320, 0.8)]
    # 全幅を横切る時間軸（テレビでだけ端まで見える。切れても困らない模様）
    ay = BN_H * 0.5
    g.append(f'<path d="M0 {ay:.0f} H{BN_W}" stroke="{J.LINE_DIM}" stroke-width="5"/>')
    for k in range(-9, 10):
        x = BN_W / 2 + k * 104
        g.append(f'<path d="M{x:.0f} {ay-16:.0f} V{ay+16:.0f}" '
                 f'stroke="{J.LINE_DIM}" stroke-width="4"/>')

    # ── 安全領域の中だけを使う ──────────────────────────
    pad = 40
    mark_w = 150                      # 右に置く印のぶんを先に取っておく
    tx = SAFE_X + pad
    maxw = SAFE_W - pad * 2 - mark_w
    size = fm.fit(NAME, maxw, "Dela", cap=104, floor=48)
    tw = fm.width(NAME, size, "Dela")
    sub = fm.fit(TAGLINE, maxw, "NotoM", cap=42, floor=24)
    g.append(f'<path d="M{tx - 24:.0f} {SAFE_Y + 74:.0f} V{SAFE_Y + 262:.0f}" '
             f'stroke="{J.ALERT}" stroke-width="10"/>')
    g.append(f'<text x="{tx}" y="{SAFE_Y + 150}" font-family="Dela" '
             f'font-size="{size:.0f}" fill="{J.INK_W}">{NAME}</text>')
    g.append(f'<path d="M{tx} {SAFE_Y + 186} h{tw:.0f}" stroke="{J.ALERT}" '
             f'stroke-width="6"/>')
    g.append(f'<text x="{tx}" y="{SAFE_Y + 250}" font-family="NotoM" '
             f'font-size="{sub:.0f}" fill="{J.LINE}">{TAGLINE}</text>')

    # 右端に「その一点」の印（アイコンと同じ語彙）。**文字の右端より右**に置く
    mx = SAFE_X + SAFE_W - pad - 34
    g.append(f'<path d="M{mx} {ay - 96:.0f} V{ay + 60:.0f}" stroke="{J.ALERT}" '
             f'stroke-width="16" stroke-linecap="round"/>')
    g.append(f'<circle cx="{mx}" cy="{ay:.0f}" r="30" fill="{J.ALERT}"/>')
    g.append(f'<circle cx="{mx}" cy="{ay:.0f}" r="11" fill="{J.BG}"/>')
    print(f"    見出し {size:.0f}px＝{tw:.0f}px（使える幅 {maxw}px）"
          f" ／ 右端 {tx + tw:.0f} < 印 {mx}", flush=True)
    if tx + tw > mx - 20:
        print("    🔴 見出しが印に届いている", flush=True)
    return "".join(g)


# ══════════════════════════════════════════════════════════
#  確認：小さくしても判別できるか
# ══════════════════════════════════════════════════════════
def check_sheet(paths):
    """アイコンを実際の表示サイズまで縮めて並べる。**ここが本番の判定基準。**

    YouTube でアイコンが出る大きさ：
      チャンネルページ 176px ／ 動画の下 48px ／ コメント欄 32px ／ 登録リスト 24px
    """
    sizes = [176, 88, 48, 32, 24]
    pad = 24
    W = sum(sizes) + pad * (len(sizes) + 1)
    H = max(sizes) + pad * 2 + 26 * len(paths)
    sheet = Image.new("RGB", (W, (max(sizes) + pad * 2) * len(paths)), "#202020")
    for row, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        x = pad
        y0 = row * (max(sizes) + pad * 2)
        for s in sizes:
            th = im.resize((s, s), Image.LANCZOS)
            # YouTube は円に切り抜くので、確認も円で行う
            mask = Image.new("L", (s, s), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
            sheet.paste(th, (x, y0 + pad + (max(sizes) - s) // 2), mask)
            x += s + pad
    out = OUT / "icon_sizes.png"
    sheet.save(out)
    print(f"  icon_sizes.png  {sheet.width}×{sheet.height}"
          f"（{'／'.join(str(s) + 'px' for s in sizes)}・円で切り抜き）", flush=True)


def banner_crops(p):
    """バナーが**端末ごとにどう切られるか**を並べて出す。

    🔴 ここを見ずに出すと、パソコンで見出しが切れていることに気づけない。
       テレビ      2048×1152（全部）
       パソコン    2048× 423（上下が切られる）
       スマホ      1546× 423 相当（さらに左右も切られる）
    """
    im = Image.open(p).convert("RGB")
    rows = [("テレビ 2048×1152", im.copy()),
            ("パソコン 2048×423", im.crop((0, (BN_H - 423) // 2, BN_W,
                                           (BN_H + 423) // 2))),
            ("スマホ 1546×423", im.crop(((BN_W - 1546) // 2, (BN_H - 423) // 2,
                                          (BN_W + 1546) // 2, (BN_H + 423) // 2)))]
    W = 1024
    parts = []
    for label, crop in rows:
        s = crop.resize((W, round(W * crop.height / crop.width)), Image.LANCZOS)
        parts.append((label, s))
    H = sum(s.height + 34 for _, s in parts) + 20
    sheet = Image.new("RGB", (W, H), "#101010")
    d = ImageDraw.Draw(sheet)
    y = 10
    for label, s in parts:
        d.text((8, y), label, fill="#cccccc")
        y += 26
        sheet.paste(s, (0, y))
        y += s.height + 8
    sheet.save(OUT / "banner_crops.png")
    print(f"  banner_crops.png（端末ごとの切り取り）", flush=True)


def main():
    print("チャンネル素材を焼く", flush=True)
    # ★2026-08-01 カズヤくん採用＝A案・目盛りなし。**これが本番**
    #   24px（登録リスト・コメント欄）で残るのが「赤い縦棒＋点」だけになり、
    #   目盛りありは同じ大きさで潰れて汚れに見えたため。
    paths = [bake("icon", icon_moment(ticks=False), IC, IC),          # ★本番
             bake("icon_alt_A_ticks", icon_moment(), IC, IC),         # 以下は比較用
             bake("icon_alt_B_section", icon_section(), IC, IC),
             bake("icon_alt_C_mark", icon_question(), IC, IC)]
    bn = bake("banner", banner(), BN_W, BN_H)
    if "--check" in sys.argv:
        check_sheet(paths)
        banner_crops(bn)
    print("→ out/brand/", flush=True)


if __name__ == "__main__":
    main()
