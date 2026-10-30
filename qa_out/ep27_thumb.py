# -*- coding: utf-8 -*-
"""27本目 ⑥：サムネの刷新（カズヤくん 10-30「八田與一について扱ったヒットしている他の動画のサムネイルを分析して…写真は八田與一の写真を使います」）。

決め（10-30 カズヤくん・どちらも推奨どおり）：
  写真＝警察庁 重要指名手配の頁の正面写真（`ref/ep27/police/npa01.jpg`＝git の外）を**縮めるだけ**（切り抜き・色の変更・字の重ねなし）・白い額で囲む・
        下に出典「写真：警察庁（大分県警察手配）」。使える根拠は著作権法の引用だけ＝大分県「著作権・リンク等について」（引用など法の認める場合を除き
        無断の転載・複製・改変は不可）・県警の頁（無断で転載することを禁じます）・警察庁 利用規約 1.2（第三者＝各都道府県警察の写真は別・引用は許諾なしの場合あり）
        ⚠️ `thumb_jiko.photo()` はコントラストと彩度を上げる＝改変になるので使わない
  文言＝「重要指名手配／八田與一 容疑者／情報1万3978件／なぜ見つからない？」（題 A2 と最後の問いにそろう・競合 #5 の「情報は多いのに、なぜ」の型）
        「容疑者」は必ず付ける（事件の回の決まり②）・名の6割の高さ（承認① の条件＝4割以上）・「犯人」「死亡」「真相」は書かない
競合の分析（10-30・再生の多い順12本）＝顔写真を大きく・左上に名前・下に特大の1句・赤と黄に黒か白のフチ・暗い地（scratchpad の並べ図）

    python -P qa_out/ep27_thumb.py [--name=ep27_A_v1]   → out/thumb/ep27/<name>.png と <name>_check.png（640px と 210px の見え方）
"""
import base64
import io
import sys
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import thumb_jiko as T  # noqa: E402

W, H = T.W, T.H
PHOTO = HERE / "ref" / "ep27" / "police" / "npa01.jpg"
PH_H, PH_TOP, PH_RIGHT, FRAME = 640, 30, 30, 5     # 写真の高さ・上の余白・右の余白・額の太さ
CREDIT = "写真：警察庁（大分県警察手配）"
X0 = 40                                            # 字の左端

RED_TOP, RED_BOT = "#f04338", "#b80a06"            # thumb_jiko の b_grad と同じ系統
YEL = T.YEL


def arg(k, d):
    for a in sys.argv[1:]:
        if a.startswith(f"--{k}="):
            return a.split("=", 1)[1]
    return d


def photo_uri():
    """縮めるだけ（LANCZOS）。切り抜き・色・明るさは元のまま"""
    im = Image.open(PHOTO).convert("RGB")
    w = round(im.width * PH_H / im.height)
    im = im.resize((w, PH_H), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return w, "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def txt(t, x, base, size, fill, inner, sw_in, outer=None, sw_out=0, fam="NSB"):
    head = f'<text x="{x}" y="{base}" font-family="{fam}" font-size="{size:.1f}"'
    g = []
    if outer:
        g.append(f'{head} fill="none" stroke="{outer}" stroke-width="{sw_out}" stroke-linejoin="round">{t}</text>')
    g.append(f'{head} fill="none" stroke="{inner}" stroke-width="{sw_in}" stroke-linejoin="round">{t}</text>')
    g.append(f'{head} fill="{fill}">{t}</text>')
    return "".join(g)


def body():
    pw, uri = photo_uri()
    px = W - PH_RIGHT - pw
    s = ['<defs>',
         '<radialGradient id="bg" cx="0.30" cy="0.60" r="0.85">'
         '<stop offset="0" stop-color="#2b0707"/><stop offset="1" stop-color="#050505"/></radialGradient>',
         T.grad("rg", RED_TOP, RED_BOT), '</defs>',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    # 写真（額＋影）
    s.append(f'<rect x="{px - FRAME + 8}" y="{PH_TOP - FRAME + 8}" width="{pw + 2 * FRAME}" height="{PH_H + 2 * FRAME}" '
             f'fill="#000000" opacity="0.55"/>')
    s.append(f'<rect x="{px - FRAME}" y="{PH_TOP - FRAME}" width="{pw + 2 * FRAME}" height="{PH_H + 2 * FRAME}" fill="#ffffff"/>')
    s.append(f'<image x="{px}" y="{PH_TOP}" width="{pw}" height="{PH_H}" href="{uri}"/>')
    s.append(f'<text x="{px}" y="{PH_TOP + PH_H + FRAME + 24}" font-family="NSB" font-size="22" fill="#e6e6e6">{CREDIT}</text>')
    # 札「重要指名手配」
    tag_fs = 44
    tag_w = 6 * tag_fs + 28
    s.append(f'<rect x="{X0}" y="34" width="{tag_w}" height="62" rx="4" fill="#d0101e"/>')
    s.append(f'<text x="{X0 + 14}" y="{65 + 0.855 * tag_fs - 0.95 * tag_fs / 2:.1f}" font-family="NSB" '
             f'font-size="{tag_fs}" fill="#ffffff">重要指名手配</text>')
    # 名前＋容疑者（6割の高さ）
    n_fs = 118
    y_fs = round(n_fs * 0.6)
    n_base = 236
    s.append(txt("八田與一", X0, n_base, n_fs, "#ffffff", "#000000", 16))
    s.append(txt("容疑者", X0 + 4 * n_fs + 10, n_base, y_fs, "#ffffff", "#000000", 12))
    # 情報の数（黄）
    s.append(txt("情報1万3978件", X0, 340, 80, YEL, "#000000", 14))
    # 1句（赤・2段）。v2＝「なぜ」を 112→150（v1 は右に大きな空き＝1句が弱かった）。2段目は 7字×100＝700px が額までの上限
    s.append(txt("なぜ", X0, 495, 150, "url(#rg)", "#ffffff", 16, "#1a0000", 32))
    s.append(txt("見つからない？", X0, 640, 100, "url(#rg)", "#ffffff", 14, "#1a0000", 28))
    return "".join(s), px


# ══════════════════════════════════════════════════════════
#  v3（10-30 カズヤくん「サムネに派手さや独創性がないため、インパクトがない。もっと工夫して」）
#  決まりの枠はそのまま＝写真は縮めるだけ・額の外に字・「容疑者」つき・文言は承認どおり（重要指名手配／八田與一 容疑者／情報1万3978件／なぜ見つからない？）
#  足すのは見た目だけ＝極太の書体（Dela Gothic One）・立体の字・光・規制テープ・赤い板・巨大な「？」
# ══════════════════════════════════════════════════════════
def bake2(name, body):
    """T.bake と同じ（Chrome で焼く）＋ Dela Gothic One（DGO）を足す"""
    css = (T.face("NSB", "NotoSansJP-Black.woff2") + T.face("DGO", "DelaGothicOne.woff2")
           + T.face("NSJ", "NotoSerifJP-Black.woff2"))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
    html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
            f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head><body>{svg}</body></html>')
    T.OUT.mkdir(parents=True, exist_ok=True)
    T.render.png(html, T.OUT / f"{name}.png", W, H)


def extrude(t, x, base, size, col, n, step, fam, sw, op=1.0):
    """右下へ n 枚ずらして重ねる＝字の厚み（立体）"""
    return "".join(f'<text x="{x + i * step:.1f}" y="{base + i * step:.1f}" font-family="{fam}" font-size="{size:.1f}" '
                   f'fill="{col}" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" opacity="{op}">{t}</text>'
                   for i in range(n, 0, -1))


def defs3():
    return ('<defs>'
            '<filter id="blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>'
            '<filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>'
            '<pattern id="streak" width="46" height="46" patternUnits="userSpaceOnUse" patternTransform="rotate(-32)">'
            '<rect x="0" y="0" width="7" height="46" fill="#ffffff" opacity="0.045"/></pattern>'
            '<radialGradient id="bg3" cx="0.28" cy="0.62" r="0.9"><stop offset="0" stop-color="#5c0b0b"/>'
            '<stop offset="0.55" stop-color="#1c0303"/><stop offset="1" stop-color="#030303"/></radialGradient>'
            '<radialGradient id="spot" cx="0.5" cy="0.45" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity="0.32"/>'
            '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3241d"/>'
            '<stop offset="1" stop-color="#7a0301"/></linearGradient>'
            + T.grad("rg", "#ff4a3d", "#a80804") + T.grad("yg", "#fffb8a", "#e8b400")
            + '<clipPath id="left"><rect x="0" y="0" width="768" height="720"/></clipPath>'
            '</defs>')


def photo3(pw, uri, px, glow=None, spot=False):
    s = []
    if spot:
        s.append(f'<ellipse cx="{px + pw / 2:.0f}" cy="{PH_TOP + PH_H * 0.45:.0f}" rx="{pw * 0.95:.0f}" ry="{PH_H * 0.75:.0f}" fill="url(#spot)"/>')
    if glow:
        s.append(f'<rect x="{px - 26}" y="{PH_TOP - 26}" width="{pw + 52}" height="{PH_H + 52}" fill="{glow}" opacity="0.75" filter="url(#blur)"/>')
    s.append(f'<rect x="{px - FRAME + 9}" y="{PH_TOP - FRAME + 9}" width="{pw + 2 * FRAME}" height="{PH_H + 2 * FRAME}" fill="#000" opacity="0.6"/>')
    s.append(f'<rect x="{px - FRAME}" y="{PH_TOP - FRAME}" width="{pw + 2 * FRAME}" height="{PH_H + 2 * FRAME}" fill="#ffffff"/>')
    s.append(f'<image x="{px}" y="{PH_TOP}" width="{pw}" height="{PH_H}" href="{uri}"/>')
    s.append(f'<text x="{px}" y="{PH_TOP + PH_H + FRAME + 24}" font-family="NSB" font-size="22" fill="#e6e6e6">{CREDIT}</text>')
    return "".join(s)


def name3(base, fill="#ffffff"):
    n_fs, y_fs = 118, 71
    return (txt("八田與一", X0 + 6, base + 6, n_fs, "#000", "#000", 16).replace('fill="#000">', 'fill="#000" opacity="0.6">')
            + txt("八田與一", X0, base, n_fs, fill, "#000000", 16)
            + txt("容疑者", X0 + 4 * n_fs + 10, base, y_fs, fill, "#000000", 12))


def body_a3():
    """A3 捜査線：規制テープ（「重要指名手配」の繰り返し）・赤い光・立体の赤い1句"""
    pw, uri = photo_uri()
    px = W - PH_RIGHT - pw
    s = [defs3(), f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>', f'<rect width="{W}" height="{H}" fill="url(#streak)"/>',
         photo3(pw, uri, px, glow="#ff2a1a")]
    tape = "重要指名手配　" * 4
    s.append('<g clip-path="url(#left)"><g transform="rotate(7 380 70)">'
             '<rect x="-80" y="36" width="980" height="72" fill="#ffd60a"/>'
             '<rect x="-80" y="36" width="980" height="7" fill="#111"/><rect x="-80" y="101" width="980" height="7" fill="#111"/>'
             f'<text x="-30" y="89" font-family="NSB" font-size="40" fill="#111">{tape}</text></g></g>')
    s.append(name3(268))
    s.append('<g transform="rotate(-3 270 330)"><rect x="40" y="292" width="452" height="76" fill="#fbfb0e" stroke="#000" stroke-width="5"/>'
             '<text x="58" y="350" font-family="NSB" font-size="58" fill="#111">情報1万3978件</text></g>')
    s.append(extrude("なぜ", X0, 548, 168, "#3d0000", 8, 1.7, "DGO", 26))
    s.append(txt("なぜ", X0, 548, 168, "url(#rg)", "#ffffff", 12, "#000000", 26, fam="DGO"))
    s.append(extrude("見つからない？", X0, 672, 100, "#3d0000", 6, 1.5, "DGO", 22))
    s.append(txt("見つからない？", X0, 672, 100, "url(#rg)", "#ffffff", 10, "#000000", 22, fam="DGO"))
    return "".join(s), px


def body_b3():
    """B3 赤い板：左を斜めに切った赤い板・黄と白の極太字・黒い札"""
    pw, uri = photo_uri()
    px = W - PH_RIGHT - pw
    s = [defs3(), f'<rect width="{W}" height="{H}" fill="#050505"/>',
         '<polygon points="0,0 800,0 742,720 0,720" fill="url(#panel)"/>',
         '<polygon points="0,0 800,0 742,720 0,720" fill="url(#streak)"/>',
         photo3(pw, uri, px)]
    s.append(f'<rect x="{X0}" y="34" width="{6 * 44 + 28}" height="62" fill="#0a0a0a"/>'
             f'<text x="{X0 + 14}" y="{65 + 0.855 * 44 - 0.95 * 44 / 2:.1f}" font-family="NSB" font-size="44" fill="#fbfb0e">重要指名手配</text>')
    s.append(name3(240))
    s.append('<rect x="40" y="276" width="452" height="76" fill="#0a0a0a"/>'
             '<text x="58" y="334" font-family="NSB" font-size="58" fill="#fbfb0e">情報1万3978件</text>')
    s.append(extrude("なぜ", X0, 540, 168, "#000000", 8, 1.7, "DGO", 26, 0.75))
    s.append(txt("なぜ", X0, 540, 168, "url(#yg)", "#000000", 26, fam="DGO"))
    s.append(extrude("見つからない？", X0, 670, 100, "#000000", 6, 1.5, "DGO", 22, 0.75))
    s.append(txt("見つからない？", X0, 670, 100, "#ffffff", "#000000", 22, fam="DGO"))
    return "".join(s), px


def body_c3():
    """C3 巨大な？：背景に巨大な赤い「？」・写真にスポットライト・光る赤い1句"""
    pw, uri = photo_uri()
    px = W - PH_RIGHT - pw
    s = [defs3(), f'<rect width="{W}" height="{H}" fill="#040404"/>', f'<rect width="{W}" height="{H}" fill="url(#bg3)" opacity="0.7"/>',
         '<text x="250" y="700" font-family="DGO" font-size="820" fill="#c30a08" opacity="0.28">？</text>',
         photo3(pw, uri, px, spot=True)]
    s.append(f'<rect x="{X0}" y="34" width="{6 * 44 + 28}" height="62" rx="4" fill="#d0101e"/>'
             f'<text x="{X0 + 14}" y="{65 + 0.855 * 44 - 0.95 * 44 / 2:.1f}" font-family="NSB" font-size="44" fill="#ffffff">重要指名手配</text>')
    s.append(name3(236))
    s.append(txt("情報1万3978件", X0, 340, 80, "url(#yg)", "#000000", 14))
    for t, b, fs in (("なぜ", 520, 168), ("見つからない？", 662, 100)):
        s.append(f'<text x="{X0}" y="{b}" font-family="DGO" font-size="{fs}" fill="#ff2a1a" stroke="#ff2a1a" stroke-width="18" '
                 f'filter="url(#glow)" opacity="0.9">{t}</text>')
        s.append(txt(t, X0, b, fs, "url(#rg)", "#ffffff", 12, "#000000", 24, fam="DGO"))
    return "".join(s), px


# ══════════════════════════════════════════════════════════
#  v4（10-30 カズヤくん「A3が最有力だが、どれも微妙。顔写真を横断するように文字を表示するなど、大幅にアレンジを加えて
#  ください。他の動画がそのような編集を施しているので、気にせず編集して構いません。」）
#  ＝写真の「縮めるだけ・字を重ねない」を**カズヤくんの判断で解いた**（引用として弱い点は 10-30 の1問で伝えた上で）。
#  残す線＝顔（目・鼻・口）に字をかけない（本人と分かる形＝人違いを広げない）・「容疑者」つき・出典の札
#  写真＝顔に寄せて画面の高さいっぱい（元の y 60〜1260 を切って 720px に）・左端を地へ溶かす・縁を暗い赤に落とす
# ══════════════════════════════════════════════════════════
CROP4 = (0, 60, 1109, 1260)                            # 元の写真（1109x1505）の切り口＝髪の上〜胸


def photo4():
    im = Image.open(PHOTO).convert("RGB").crop(CROP4)
    w = round(im.width * H / im.height)
    im = im.resize((w, H), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return w, "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def body_a5(band=True):
    """v5（10-30 カズヤくん「A4bの『なぜ見つからない？』を右下がりでもっと大きく。文字の背景は黒に変更」）
    1句＝右下がり（+6度）・150px を 1220px に詰める（9字＝1350px が1行に入らない）。
    band=True＝1句の後ろに黒い帯（字の地を黒に）・False＝左の地を黒に（帯なし）。
    顔にかけない線＝あご（720px で y≈485・x 748〜1154）より下＝帯の上端は x=748 で y≈495"""
    b, px = body_a4(False)
    hf, hb, ang, x0, ln = 150, 560, 6, 32, 1220
    a, z = b.split('<g transform="rotate(-2 640 620)">', 1)
    rest = z.split('</g>', 1)[1]
    if not band:
        a = a.replace('fill="url(#bg3)"/>', 'fill="#050505"/>', 1)
    g = [f'<g transform="rotate({ang} {x0} {hb})">']
    if band:
        g.append(f'<rect x="{x0 - 40}" y="{hb - round(0.86 * hf) - 20}" width="1400" height="{round(1.0 * hf) + 40}" fill="#000" opacity="0.92"/>')
    for i in range(8, 0, -1):                          # 厚み（奥）→ 黒のフチ → 白のフチ → 赤の塗り の順に重ねる
        g.append(f'<text x="{x0 + i * 1.8:.1f}" y="{hb + i * 1.8:.1f}" font-family="DGO" font-size="{hf}" textLength="{ln}" '
                 f'lengthAdjust="spacingAndGlyphs" fill="#3a0000" stroke="#3a0000" stroke-width="22" stroke-linejoin="round">なぜ見つからない？</text>')
    g.append(f'<text x="{x0}" y="{hb}" font-family="DGO" font-size="{hf}" textLength="{ln}" lengthAdjust="spacingAndGlyphs" '
             f'fill="none" stroke="#000000" stroke-width="30" stroke-linejoin="round">なぜ見つからない？</text>')
    g.append(f'<text x="{x0}" y="{hb}" font-family="DGO" font-size="{hf}" textLength="{ln}" lengthAdjust="spacingAndGlyphs" '
             f'fill="none" stroke="#ffffff" stroke-width="12" stroke-linejoin="round">なぜ見つからない？</text>')
    g.append(f'<text x="{x0}" y="{hb}" font-family="DGO" font-size="{hf}" textLength="{ln}" lengthAdjust="spacingAndGlyphs" '
             f'fill="url(#rg)">なぜ見つからない？</text>')
    g.append('</g>')
    return a + "".join(g) + rest, px


def body_a6():
    """v6（10-30 カズヤくん「フォントを『キリンをもう一度』の動画のサムネイルと同じものにしてください。A5aの『重要指名手配』を右上がりに。」）
    書体＝キリンをもう一度【公式】`_Z26yksEZTk` のサムネ（原寸で見た）＝極太の明朝（「一」のうろこ・払い・仮名の形）＝源ノ明朝 Heavy
    ＝Noto Serif JP Black（`fonts/NotoSerifJP-Black.woff2`＝リポにある）。名前・容疑者・件数・1句・テープを替える（出典の小さな札はゴシックのまま）。
    テープ＝rotate(+7)（右下がり）→ rotate(-7)（右上がり）＝左端の下端 y≈143 と名前の字の上端 y≈159 は 16px 空く"""
    b, px = body_a5(True)
    b = b.replace('rotate(7 380 64)', 'rotate(-7 380 64)')
    b = b.replace('font-family="DGO"', 'font-family="NSJ"')
    for fs in ('120.0', '72.0'):
        b = b.replace(f'font-family="NSB" font-size="{fs}"', f'font-family="NSJ" font-size="{fs}"')
    b = b.replace('font-family="NSB" font-size="58"', 'font-family="NSJ" font-size="58"')
    b = b.replace('font-family="NSB" font-size="40"', 'font-family="NSJ" font-size="40"')
    b = b.replace('stroke="#ffffff" stroke-width="12"', 'stroke="#ffffff" stroke-width="8"')
    b = b.replace('stroke="#000000" stroke-width="30"', 'stroke="#000000" stroke-width="24"')
    return b, px


def body_a6b():
    """v6b（10-30 カズヤくん「v6をキープします。背景が黒版も作ってください。今の黒帯もそれに合わせて修正」）
    地＝暗い赤の光（bg3）→ 黒・写真の縁を落とす色も黒に・帯は地と同じ黒（不透明）＝左で地とつながり、黒い地が写真を斜めに横切る形"""
    b, px = body_a6()
    b = b.replace(f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>', f'<rect width="{W}" height="{H}" fill="#050505"/>', 1)
    b = b.replace('<stop offset="1" stop-color="#2a0000" stop-opacity="0.72"/>', '<stop offset="1" stop-color="#000000" stop-opacity="0.72"/>')
    b = b.replace('fill="#000" opacity="0.92"/>', 'fill="#050505" opacity="1"/>')
    return b, px


# 🆕 ⑥'（10-30 カズヤくん「サムネの暗い赤の地の、別色版をいくつか作って。・明るい赤 ・白（今の白字部分は読みやすいように色を修正）・その他おすすめ」）
#   配置・字・写真は v6 のまま＝地（bg3）と写真の縁の影（vig）の色だけ替える。白地は白い字（名前・容疑者・右上の出典）を黒字に白フチへ、名前の影を薄い灰に。
#   おすすめ＝紺（警察の青）：競合12本の多くが赤と黒（10-30 の分析）＝並んだときに目立つ・赤い1句と黄色のテープが反対色で浮く
V6C = {   # 記号: (名, 地の放射のぼかし＝中心・0.55・外, 写真の縁の影の色, 影の濃さ)
    "r": ("明るい赤", ("#ff4136", "#d81810", "#8c0805"), "#b80a06", 0.6),
    "w": ("白", ("#ffffff", "#f2f2f2", "#cfcfcf"), "#ffffff", 0.55),
    "n": ("紺（警察の青・おすすめ）", ("#24479c", "#0c2257", "#030914"), "#000d33", 0.72),
}


def _swap(b, old, new):
    """1か所だけ替える（当たらない・2か所以上なら止める＝黙って v6 のまま焼かない）"""
    n = b.count(old)
    if n != 1:
        raise SystemExit(f"🔴 替える所が {n} か所（1か所のはず）: {old[:80]}")
    return b.replace(old, new)


def body_a6c(kind):
    b, px = body_a6()
    _, (c0, c1, c2), vig, vop = V6C[kind]
    b = b.replace('</defs>', f'<radialGradient id="bg6c" cx="0.28" cy="0.62" r="0.9"><stop offset="0" stop-color="{c0}"/>'
                  f'<stop offset="0.55" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient></defs>', 1)
    b = _swap(b, f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>', f'<rect width="{W}" height="{H}" fill="url(#bg6c)"/>')
    b = _swap(b, '<stop offset="1" stop-color="#2a0000" stop-opacity="0.72"/>', f'<stop offset="1" stop-color="{vig}" stop-opacity="{vop}"/>')
    if kind == "w":
        for t, fs, sw, sw2 in (("八田與一", "120.0", 16, 12), ("容疑者", "72.0", 12, 10)):
            b = _swap(b, f'font-size="{fs}" fill="none" stroke="#000000" stroke-width="{sw}" stroke-linejoin="round">{t}</text>',
                      f'font-size="{fs}" fill="none" stroke="#ffffff" stroke-width="{sw2}" stroke-linejoin="round">{t}</text>')
            b = _swap(b, f'font-size="{fs}" fill="#ffffff">{t}</text>', f'font-size="{fs}" fill="#111111">{t}</text>')
        b = _swap(b, 'stroke="#000" stroke-width="16" stroke-linejoin="round">八田與一</text>',
                  'stroke="#9e9e9e" stroke-width="16" stroke-opacity="0.5" stroke-linejoin="round">八田與一</text>')
        b = _swap(b, 'fill="#000" opacity="0.6">八田與一</text>', 'fill="#9e9e9e" opacity="0.5">八田與一</text>')
        b = _swap(b, f'fill="#ffffff" stroke="#000" stroke-width="5" paint-order="stroke fill">{CREDIT}',
                  f'fill="#111111" stroke="#ffffff" stroke-width="5" paint-order="stroke fill">{CREDIT}')
    return b, px


def body_a4(two_tone=True):
    pw, uri = photo4()
    px = W - pw
    s = [defs3().replace('</defs>',
         '<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
         '<stop offset="0.3" stop-color="#fff" stop-opacity="1"/></linearGradient>'
         f'<mask id="phm" maskUnits="userSpaceOnUse" x="{px}" y="0" width="{pw}" height="{H}">'
         f'<rect x="{px}" y="0" width="{pw}" height="{H}" fill="url(#fadeL)"/></mask>'
         '<radialGradient id="vig" cx="0.58" cy="0.36" r="0.78"><stop offset="0.5" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#2a0000" stop-opacity="0.72"/></radialGradient></defs>'),
         f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>', f'<rect width="{W}" height="{H}" fill="url(#streak)"/>',
         f'<g mask="url(#phm)"><image x="{px}" y="0" width="{pw}" height="{H}" href="{uri}"/>'
         f'<rect x="{px}" y="0" width="{pw}" height="{H}" fill="url(#vig)"/></g>']
    tape = "重要指名手配　" * 4
    s.append('<g clip-path="url(#tapeclip)"><g transform="rotate(7 380 64)">'
             '<rect x="-80" y="30" width="980" height="72" fill="#ffd60a"/>'
             '<rect x="-80" y="30" width="980" height="7" fill="#111"/><rect x="-80" y="95" width="980" height="7" fill="#111"/>'
             f'<text x="-30" y="83" font-family="NSB" font-size="40" fill="#111">{tape}</text></g></g>')
    s[0] = s[0].replace('</defs>', '<clipPath id="tapeclip"><rect x="0" y="0" width="790" height="720"/></clipPath></defs>')
    n_fs, y_fs, nb = 120, 72, 262
    s.append(txt("八田與一", X0 + 6, nb + 6, n_fs, "#000", "#000", 16).replace('fill="#000">', 'fill="#000" opacity="0.6">'))
    s.append(txt("八田與一", X0, nb, n_fs, "#ffffff", "#000000", 16))
    s.append(txt("容疑者", X0 + 4 * n_fs + 10, nb, y_fs, "#ffffff", "#000000", 12))
    s.append('<g transform="rotate(-3 270 326)"><rect x="40" y="290" width="452" height="76" fill="#fbfb0e" stroke="#000" stroke-width="5"/>'
             '<text x="58" y="348" font-family="NSB" font-size="58" fill="#111">情報1万3978件</text></g>')
    # 1句＝写真の胸の上を横断する1行（顔＝元の y 900 より上＝720px で y≈504 より上にかけない）
    hb, hf = 668, 128
    s.append('<g transform="rotate(-2 640 620)">')
    s.append(extrude("なぜ見つからない？", X0, hb, hf, "#2a0000", 9, 1.8, "DGO", 30))
    if two_tone:
        s.append(f'<text x="{X0}" y="{hb}" font-family="DGO" font-size="{hf}" fill="none" stroke="#000" stroke-width="30" '
                 f'stroke-linejoin="round">なぜ見つからない？</text>')
        s.append(f'<text x="{X0}" y="{hb}" font-family="DGO" font-size="{hf}" fill="none" stroke="#fff" stroke-width="12" '
                 f'stroke-linejoin="round">なぜ見つからない？</text>')
        s.append(f'<text x="{X0}" y="{hb}" font-family="DGO" font-size="{hf}"><tspan fill="url(#yg)">なぜ</tspan>'
                 f'<tspan fill="url(#rg)">見つからない？</tspan></text>')
    else:
        s.append(txt("なぜ見つからない？", X0, hb, hf, "url(#rg)", "#ffffff", 12, "#000000", 30, fam="DGO"))
    s.append('</g>')
    s.append(f'<text x="{W - 16}" y="30" text-anchor="end" font-family="NSB" font-size="20" fill="#ffffff" '
             f'stroke="#000" stroke-width="5" paint-order="stroke fill">{CREDIT}</text>')
    return "".join(s), px


# ══════════════════════════════════════════════════════════
#  v7（10-31・公開のあと カズヤくん「27本目のサムネを修正します」）
#  ①「重要指名手配」の帯は字をなくしてトラテープ（黄と黒の斜めの縞）
#  ②「容疑者」を省いて名前をもっと大きく（10-31 カズヤくんの決め＝事件の回の決まり②より新しい・題と概要欄は「容疑者」つきのまま）
#  ③顔写真を切り抜き、地は全部単色（A＝v6 の暗い赤・B＝紺＝10-30 の A／B と同じ色）
#  ④「八田與一」＝他の回と同じ透ける大きな字（H 型の反転版＝字の外は地のまま・字の中は暗い白黒・赤い縁＝26本目と同じ hx2）
#  ⑤その右下に他の回と同じ形の「なぜ見つからない？」（黄 #fbfb0e・黒フチ16・NSB 112・基線 692）⑥2行の間に「情報1万3978件」（白・黒フチ）
#  顔に字をかけない＝元の写真で髪 y74〜450・目 y≈515・口 y≈760（行ごとの暗さで測った）。名前を顔に重ねると「一」の横の画が
#  目にかかり、顔を隠す黒い帯（目線）に見える → 名前は顔の左に収める
# ══════════════════════════════════════════════════════════
CUT = HERE / "ref" / "ep27" / "police" / "npa01_cut.png"   # 切り抜き（透明つき・git の外＝警察の写真から作った物）
S7, FX7, FY7 = 0.6, 680, -36                               # 顔の倍率・左上の位置（v6 と同じ大きさ・65px 右へ＝名前の幅を空ける）
FADE7 = 150                                                # 元の写真の左の端から 150px で体を地へ溶かす（端で体が縦に切れて見えない）
BAND7 = (160, 440, 40, 800)                                # 名前の縁の外側が収まる枠（上・下・左・右）＝テープの下端 y143（x=40）より下・髪の左端 x811 より左
BOLD7 = {"八": 16, "田": 16, "與": 0, "一": 16}             # 太らせ（画の多い「與」は0＝縁で埋まらない）
# 🆕 同じ日（v7 を焼いている途中）カズヤくん「サムネの文字フォントは『キリンをもう一度』の『事態が動いています』の動画サムネと同じものに。
#    背景が単色なので文字の透け感は無しで良い」＝見本 `TFHX_1QXSMI`「事態が動いています 確認してください【八田與一】」のサムネをブラウザで見た
#    ＝極太の明朝（点がしずく形・横画の右端にうろこ・細く抜ける払い）＝v6 の見本 `_Z26yksEZTk`（八田與一に関する全ての情報）と同じ系統
#    → 名前・件数・1句を Noto Serif JP Black（NSJ）に。名前は透けない塗り（字の中＝下の色 INK7・赤い縁はそのまま）。出典の小さな札はゴシックのまま（v6 と同じ）
FONT7 = "NotoSerifJP-Black.woff2"
# 🆕 同じ日（明朝の1版を見て）カズヤくん「背景は黒。名前は赤にして。青版は不要」＝k 版。地＝v6b の黒と同じ #050505。
#    名前の赤＝見本 `TFHX_1QXSMI` のサムネの「最新 情報」の赤い画素の中央値 (246,4,4)（ブラウザの画面から測った）。縁なし＝黒い地では暗い縁は
#    見えず、同じ赤の縁は字を太らせて「與」の中をつぶす。前の2版は消さずに残す（選ばれ直すことがある＝サムネの型の記憶）
# 🆕 同じ日（k 版を見て）カズヤくん「『八田與一』のフォントが指定していたものと異なって見えます。『八田』が大きく、『與一』が小さく見えます。
#    文字の大きさの見え方を統一してください。文字色の赤も指定したモデル（キリン）と同じ赤を」＝k2 版。見本を等倍にして測った：
#    ・書体＝見本と同じ字の高さ・横幅・黒フチで候補を並べると Noto Serif JP Black が「八」の払い・「田」の角・「一」の大きなうろこまで一番そろう
#      （しっぽり明朝 B1・Zen Old Mincho は「八」「一」の形が違う）＝書体は合っていた。違って見えたのは加工＝横の詰め 0.66（見本は約 0.83）と
#      「八」「田」だけの太らせ 16（「與」は 0）。見本は白い字に太い黒フチ（「一」の白い芯 3〜5px の上下に黒 12px）＝細い横画もフチで太く見える
#      → 黒い地ではフチが見えない → 4字とも同じだけ太らせる（BOLD7K）・詰めは見本と同じ 0.83（SX7K）
#    ・赤＝見本の「最新 情報」の芯は上から下まで (240〜248, 3〜6, 3〜7)＝色の上下差なし＝k 版の (246,4,4) と同じ値のまま
BOLD7K = {c: 10 for c in "八田與一"}                       # 4字そろえて太らせる（横画 約7px → 約17px＝210px で約3px）
SX7K = 0.83                                                # 横の詰め＝見本（「八田與一」の4字で 586px・字の高さ 158px）と同じ
# k2 を原寸で見たら、今度は「與」がいちばん大きく見えた＝書体の作りで「與」は「田」より 1.067 倍高い（k2 で 222px 対 208px）うえ、
# 太らせで墨の量も最多（赤の画素 26928・田 23362・八 12266・一 3882）・太らせ 10 で「與」の離れた2つの塊がくっついた（hx3.pieces）
# → k3：「與」を「八」「田」と同じ高さへ縮めて字の縦のまん中を「田」にそろえる・「與」の太らせは 8・画が1本の「一」は 14
BOLD7K3 = {"八": 10, "田": 10, "與": 8, "一": 14}
HSC7K3 = {"與": 208 / 222}
STYLE7 = {   # 記号: (地, 名前の字の中, 名前の縁の太さ, 太らせ, 横の詰め＝None なら枠いっぱいに合わせる, 字ごとの大きさ)
    "": ("#5c0b0b", "#111111", 18, BOLD7, None, None),      # 明朝の1版 A：暗い赤の地（v6 の bg3 の中心）・黒い字に赤い縁（ep27_A7_v7.png＝dfb9da22…）
    "n": ("#0f2a66", "#111111", 18, BOLD7, None, None),     # 明朝の1版 B：紺（ep27_A7n_v7.png＝0b164756…）＝「青版は不要」
    "k": ("#050505", "#f60404", 0, BOLD7, None, None),      # 2版：黒い地・赤い名前（ep27_A7k_v7.png＝c86ee837…）
    "k2": ("#050505", "#f60404", 0, BOLD7K, SX7K, None),    # 3版：k の名前を見本の形に（4字同じ太らせ・詰め 0.83）（ep27_A7k2_v7.png＝f223acd8…）
    "k3": ("#050505", "#f60404", 0, BOLD7K3, SX7K, HSC7K3),  # 4版：k2 の4字の高さをそろえる（ep27_A7k3_v7.png＝8b169b92…）
    "k4": ("#050505", "#f60404", 0, None, "kirin", None),    # 5版：見本の「八田與一」をそのまま写す（下の KIRIN7）（ep27_A7k4_v7.png＝35b81f64…）
    "k5": ("#050505", "#f60404", 0, None, "kirin", None),    # 6版：k4 を縦にだけ伸ばす（KIRIN7_SY）
}
# 🆕 同じ日（k4 を見て）カズヤくん「名前の縦幅をもう少し大きく」＝横は顔の髪で決まる（白い縁が x811 に届かない最大）→ 縦にだけ伸ばす。
#    1.15倍＝「田」186px → 約214px（k3 の約210px と同じくらい）。縁（太らせ・ぼかし）は伸ばさない＝字の形を座標で伸ばしてから縁を描く
KIRIN7_SY = {"k5": 1.15}
# 🆕 同じ日（k3 を見て）カズヤくん「キリンは文字の縁にぼやけたようなエフェクトが入っているので、それも完全再現。『八田與一』の部分のみ完全コピー。
#    背景が黒なので縁は白で」＝k4。見本（TFHX_1QXSMI のサムネ・1280x720）の「八田與一」をページの画素で直に測った：
#    ・4字の白い字の箱（RGB の最小 >150）＝八 x11〜157・y20〜149／田 x171〜299・y22〜154／與 x310〜457・y12〜159／一 x463〜602・y67〜88
#    ・Noto Serif JP Black の字の形を1字ずつ箱に当てはめた（大きさ・横の詰め・原点・基線）＝KIRIN7。重ね図で輪郭は見本の白い字の縁に沿う
#      （白の重なり IoU 0.73〜0.81＝細い画の 1〜2px のずれと JPEG のにじみの分）。字ごとの大きさは 134〜155px とばらつく＝見本の並びのまま写す
#    ・縁＝白い字からの距離ごとの暗さ（地で割った値の中央値）が d≦7 で 0.97〜1・d=10 0.91・12 0.79・16 0.44・20 0.13・24 0.03
#      ＝字を外へ R 太らせた形をぼかし σ で（まっすぐな縁なら Φ((R−d)/σ)）＝R 14.8・σ 4.3（等倍で焼いて同じ物差しで照らした）
#    → 色だけ替える：字＝見本の「最新 情報」の赤（k と同じ）・縁＝白（地が黒）。倍率は縁の見える幅こみで髪の左の端に届かない最大
KIRIN7 = {"八": (145.41, 1.041, 7.32, 138.88), "田": (148.44, 1.013, 156.82, 143.22),
          "與": (154.81, 0.977, 306.48, 144.48), "一": (134.15, 1.097, 458.23, 140.28)}   # 字: (大きさ, 横の詰め, 原点 x, 基線 y)＝見本の等倍
KIRIN7_INK = (10.5, 602.5, 11.5, 159.5)                    # 4字の字の外接（左・右・上・下）＝見本の等倍
KIRIN7_GLOW = (14.8, 4.3)                                  # 縁の太らせ R・ぼかし σ（見本の等倍）
KIRIN7_SEEN = 22                                           # 縁が見える幅（暗さ 0.05 まで＝見本の等倍）
HAIR7_LEFT = FX7 + 219 * S7                                # 髪の左の端（元の写真の x219＝いちばん広い行）＝x 811
NAME7_CY = 300                                             # 名前の字の縦のまん中（k3 と同じ）


def name_kirin7(hx, ink, sy=1.0):
    """見本の「八田與一」を KIRIN7 の並びのまま k 倍して置く（白いぼかしの縁＋字）。sy＝縦にだけ伸ばす倍率（字の縦のまん中 NAME7_CY を中心に）。
    返り値＝SVG・字の並び（hx.lay と同じ形・基線は伸ばしたあと）・倍率"""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    k = (HAIR7_LEFT - BAND7[2]) / (KIRIN7_INK[1] - KIRIN7_INK[0] + KIRIN7_SEEN)
    dx, dy = BAND7[2] - KIRIN7_INK[0] * k, NAME7_CY - (KIRIN7_INK[2] + KIRIN7_INK[3]) / 2 * k
    gl = [(c, X * k + dx, NAME7_CY + (b * k + dy - NAME7_CY) * sy, f * k, s, 0, FONT7) for c, (f, s, X, b) in KIRIN7.items()]
    hx.ink("八", FONT7)                                 # 書体を読み込む（hx._FT）
    gs, cmap, upm = hx._FT[FONT7]
    ds = []
    for c, x, b, f, s, _, _ in gl:
        sp = SVGPathPen(gs)
        gs[cmap[ord(c)]].draw(TransformPen(sp, (f * s / upm, 0, 0, -f * sy / upm, x, b)))
        ds.append(f'<path d="{sp.getCommands()}"/>')
    p = "".join(ds)
    r, sig = (v * k for v in KIRIN7_GLOW)
    svg = (f'<defs><filter id="kg" x="0" y="0" width="{W}" height="{H}" filterUnits="userSpaceOnUse">'
           f'<feGaussianBlur stdDeviation="{sig:.2f}"/></filter></defs>'
           f'<g fill="#ffffff" stroke="#ffffff" stroke-width="{2 * r:.2f}" stroke-linejoin="round" filter="url(#kg)">{p}</g>'
           f'<g fill="{ink}">{p}</g>')
    return svg, gl, k


def lay7(hx, top, bot, left, right, rim, bold, sx_want=None, hsc=None):
    """名前の字を並べる。sx_want＝None なら枠いっぱい（hx.lay のまま）。数なら、横の詰めがその値になる字の高さを二分で探し、枠の縦のまん中に置く。
    hsc＝字ごとの大きさ（hx.lay は基線をそろえるだけ）＝大きさを変えた字は、字の形の縦のまん中を「田」にそろえ直す"""
    kw = dict(left=left, right=right, rim=rim, bold=bold, font=FONT7, hsc=hsc or {})
    if sx_want is None:
        gl, fs, sx = hx.lay("八田與一", top, bot, **kw)
    else:
        lo, hi = 40.0, float(bot - top)
        for _ in range(40):
            h = (lo + hi) / 2
            lo, hi = (h, hi) if hx.lay("八田與一", top, top + h, **kw)[2] > sx_want else (lo, h)
        off = ((bot - top) - h) / 2
        gl, fs, sx = hx.lay("八田與一", top + off, top + off + h, **kw)
    if hsc:
        def mid(c, b, f, font):                        # 字の形の縦のまん中（画面の y）
            i = hx.ink(c, font)
            return b - (i[1] + i[3]) / 2 * f
        ref = next(mid(c, b, f, font) for c, x, b, f, s, bd, font in gl if c == "田")
        gl = [(c, x, b + ref - mid(c, b, f, font) if c in hsc else b, f, s, bd, font) for c, x, b, f, s, bd, font in gl]
    return gl, fs, sx


def _hx():
    """Vault の hx・hx3（26本目と同じ H 型の反転版の道具）を読むだけで使う。hx は読み込むと T.OUT を Vault へ向ける＝ここで戻す"""
    res = Path(r"C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証-サムネ海外競合5ch-20261012")
    if str(res) not in sys.path:
        sys.path.insert(0, str(res))
    import hx
    import hx3
    T.OUT = HERE / "out" / "thumb"
    hx3.OUT = T.OUT
    return hx, hx3


def cutout():
    """正面写真から人だけを切り抜く（透明つき PNG・一度作ったら使い回す＝`--recut` で作り直す）。地はクリーム色の無地（上の端の色の幅 3〜7）
    → Lab の距離で地の種（端につながる所だけ）→ GrabCut（cv2）で縁を決める → 縁の段々をならす → 1px 削って 1.6px ぼかす（クリーム色のにじみを残さない）
    1回目（10-31 07:55）は襟のフリース（地と色が近い）の縁が段々に見えた（原寸で x760〜790・y470〜540）＝開いて閉じる（菱形の半径4）を足した"""
    if CUT.exists() and "--recut" not in sys.argv:
        return Image.open(CUT).convert("RGBA")
    import cv2
    import numpy as np
    from scipy import ndimage as nd
    rgb = np.asarray(Image.open(PHOTO).convert("RGB"))
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(float)
    d = np.sqrt(((lab - np.median(lab[:10].reshape(-1, 3), 0)) ** 2).sum(-1))

    def edge(m):                                       # 上・左・右の端につながる所だけ（顔の中の明るい所を地にしない）
        lb, _ = nd.label(m)
        keep = (set(np.unique(lb[0])) | set(np.unique(lb[:, 0])) | set(np.unique(lb[:, -1]))) - {0}
        return np.isin(lb, list(keep))
    m = np.full(d.shape, cv2.GC_PR_FGD, np.uint8)
    m[edge(d < 25)] = cv2.GC_PR_BGD
    m[edge(d < 12)] = cv2.GC_BGD
    m[nd.binary_erosion(~edge(d < 30), iterations=25)] = cv2.GC_FGD
    cv2.grabCut(rgb[:, :, ::-1].copy(), m, None, np.zeros((1, 65)), np.zeros((1, 65)), 6, cv2.GC_INIT_WITH_MASK)
    fg = (m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD)
    lb, n = nd.label(fg)
    fg = nd.binary_fill_holes(lb == 1 + int(np.argmax(nd.sum(fg, lb, range(1, n + 1)))))
    st = nd.generate_binary_structure(2, 1)
    fg = nd.binary_fill_holes(nd.binary_closing(nd.binary_opening(fg, st, iterations=4), st, iterations=4))
    # 髪の縁の明るい画素＝クリーム色の地のにじみ（暗い地で白い毛羽に見えた＝てっぺん y78〜94・明るさ105〜119／髪は40〜50）を外す。
    # 元の y 440 より上は髪だけ（額は y≈450 から＝行ごとの暗さで測った）＝肌を削らない
    rim = fg & ~nd.binary_erosion(fg, iterations=6)
    rim[440:] = False
    fg &= ~(rim & (rgb.mean(-1) > 90))
    fg = nd.binary_erosion(fg, iterations=1)
    # 髪の縁の色のにじみを髪の色へ落とす（黒い地で髪の輪郭が明るく浮いた＝縁の 1〜3px の明るさ中央値 54・髪の内側 27＝10-31 の k 版）
    # ＝縁から内へ 10px と外（ぼかしで半透明になる所）の色を、髪の内側（縁から 12px より内・元の y100〜440）の 75% 点で頭打ちにする
    zone = ~nd.binary_erosion(fg, iterations=10)
    zone[440:] = False
    hair = nd.binary_erosion(fg, iterations=12)
    hair[440:] = False
    hair[:100] = False
    rgb = rgb.copy()
    rgb[zone] = np.minimum(rgb[zone], np.percentile(rgb[hair], 75, axis=0)).astype(np.uint8)
    im = Image.fromarray(rgb).convert("RGBA")
    im.putalpha(Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)))
    im.save(CUT)
    return im


def _uri(im, fmt="PNG"):
    buf = io.BytesIO()
    im.save(buf, fmt)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def face7():
    """切り抜きを v6 と同じ大きさへ縮め、元の写真の左の端の体だけを地へ溶かす（FADE7）"""
    import numpy as np
    cut = cutout()
    a = np.asarray(cut.getchannel("A"), float) * np.clip(np.arange(cut.width) / FADE7, 0, 1)[None, :]
    cut.putalpha(Image.fromarray(a.astype(np.uint8)))
    return cut.resize((round(cut.width * S7), round(cut.height * S7)), Image.LANCZOS)


def tape7(base, cy, k=2):
    """地の画へトラテープ（黄と黒の斜めの縞・字なし・太さ 72）を描く。x=380 で中心の高さ cy・右上がり 7度（SVG の rotate(-7) と同じ向き）。
    2倍で描いて縮める（縁と縞のぎざぎざを消す）。縞の幅は SVG の版と同じ 32px（45度の縞を x+y で切る＝周期 32√2）"""
    import math
    import numpy as np
    from PIL import ImageDraw
    yy, xx = np.mgrid[0:H * k, 0:W * k]
    s = ((xx + yy) // round(32 * math.sqrt(2) * k)) % 2
    st = Image.fromarray(np.where(s[..., None] == 0, (0xff, 0xd6, 0x0a), (0x11, 0x11, 0x11)).astype(np.uint8))
    a = math.radians(-7)
    pts = [((380 + (x - 380) * math.cos(a) - (y - cy) * math.sin(a)) * k, (cy + (x - 380) * math.sin(a) + (y - cy) * math.cos(a)) * k)
           for x, y in ((-80, cy - 36), (1520, cy - 36), (1520, cy + 36), (-80, cy + 36))]
    m = Image.new("L", (W * k, H * k), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    base.paste(st.resize((W, H), Image.LANCZOS), (0, 0), m.resize((W, H), Image.LANCZOS))


TAPE7_BEHIND = 235                                         # 案 C：テープを名前の後ろに通す高さ（x=380 の中心）＝八・田・與の上半分を横切り、髪の奥を通って右の端へ


def body_a7(kind="k", behind=False):
    """kind＝STYLE7 の記号。behind=False＝テープは v6 の位置（名前の上）。True＝案 C：テープを名前の後ろに通す（字の中にテープの縞が暗く透ける）"""
    hx, _ = _hx()
    bg, ink, rim, bold, sx_want, hsc = STYLE7[kind]
    face = face7()
    base = Image.new("RGB", (W, H), bg)
    if behind:
        tape7(base, TAPE7_BEHIND)
    base.paste(face.convert("RGB"), (FX7, FY7), face.getchannel("A"))
    col = _uri(base)
    ns = 'font-family="NSB" font-size="18" fill="#ffffff" stroke="#000" stroke-width="4" paint-order="stroke fill"'
    ex = [] if behind else [
          '<defs><pattern id="tiger" patternUnits="userSpaceOnUse" width="64" height="64" patternTransform="rotate(45)">'
          '<rect width="32" height="64" fill="#ffd60a"/><rect x="32" width="32" height="64" fill="#111111"/></pattern>'
          '<clipPath id="tp7"><rect x="-80" y="30" width="1600" height="72" transform="rotate(-7 380 64)"/></clipPath></defs>',
          # テープ＝v6 と同じ位置と傾き（右上がり 7度）・字なし。右は顔の奥を通って上の端へ抜ける（テープの所だけ顔を描き直す）
          '<g transform="rotate(-7 380 64)"><rect x="-80" y="30" width="1600" height="72" fill="url(#tiger)"/></g>',
          f'<g clip-path="url(#tp7)"><image href="{_uri(face)}" x="{FX7}" y="{FY7}" width="{face.width}" height="{face.height}"/></g>']
    post = ['<text x="40" y="546" font-family="NSJ" font-size="76" fill="#ffffff" stroke="#000" stroke-width="14" '
            'stroke-linejoin="round" paint-order="stroke fill">情報1万3978件</text>',
            '<text x="1240" y="692" text-anchor="end" font-family="NSJ" font-size="112" fill="#fbfb0e" stroke="#000" '
            'stroke-width="16" stroke-linejoin="round" paint-order="stroke fill">なぜ見つからない？</text>',
            f'<text x="16" y="684" {ns}>写真：警察庁</text><text x="16" y="706" {ns}>（大分県警察手配）</text>']
    if sx_want == "kirin":                             # k4：見本の「八田與一」を写す（型抜きの窓は使わない＝地の上にテープ → 名前 → 字）
        name, gl, k = name_kirin7(hx, ink, KIRIN7_SY.get(kind, 1.0))
        return (f'<image href="{col}" x="0" y="0" width="{W}" height="{H}"/>' + "".join(ex) + name + "".join(post),
                (gl, KIRIN7["田"][0] * k, KIRIN7["田"][1], 0))
    dark = _uri(Image.new("RGB", (W, H), ink))         # 字の中＝透けない塗り（10-31 カズヤくん「透け感は無しで良い」）＝hx2 の型抜きの窓に無地を置く
    gl, fs, sx = lay7(hx, *BAND7, rim, bold, sx_want, hsc)
    svg = _swap(hx.hx2(dark, col, gl, ex + post, rim=rim), f'<rect x="0" y="470" width="{W}" height="250" fill="url(#bt)"/>', "")  # 下の暗幕なし＝地は全部単色
    return svg, (gl, fs, sx, rim)


def sheet3(names, outp):
    """案ごとに 640px と 210px（実寸）を横に並べ、縦に積む"""
    from PIL import ImageDraw, ImageFont
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 18)
    rows = [(n, Image.open(T.OUT / "ep27" / f"{n}.png").convert("RGB")) for n in names]
    sh = Image.new("RGB", (640 + 20 + 210 + 10, len(rows) * (360 + 34)), (60, 60, 60))
    d = ImageDraw.Draw(sh)
    for i, (n, im) in enumerate(rows):
        y = i * (360 + 34)
        d.text((4, y + 4), n, fill=(255, 255, 0), font=font)
        sh.paste(im.resize((640, 360), Image.LANCZOS), (0, y + 28))
        sh.paste(im.resize((210, 118), Image.LANCZOS), (660, y + 28))
    sh.save(outp)


def check(png, outp):
    im = Image.open(png).convert("RGB")
    a = im.resize((640, 360), Image.LANCZOS)
    b = im.resize((210, 118), Image.LANCZOS)
    c = b.resize((420, 236), Image.NEAREST)
    sheet = Image.new("RGB", (640 + 20 + 420, 380), (60, 60, 60))
    sheet.paste(a, (0, 10))
    sheet.paste(b, (660, 10))
    sheet.paste(c, (660, 140))
    sheet.save(outp)


def main():
    name = arg("name", "ep27_A_v1")
    (T.OUT / "ep27").mkdir(parents=True, exist_ok=True)
    style = arg("style", "v2")
    if style == "v7":                                  # 🆕 10-31：切り抜き＋単色の地＋大きな名前。--kinds＝STYLE7 の記号（既定 k＝黒い地・赤い名前）
        # 案 C（テープを名前の後ろ＝透け感を出す案）は「透け感は無しで良い」で見送り＝body_a7(behind=True) は残すだけ
        for kind in arg("kinds", "k").split(","):
            b, (gl, fs, sx, rim) = body_a7(kind)
            n = f"ep27_A7{kind}_v7"
            bake2(f"ep27/{n}", b)
            check(T.OUT / "ep27" / f"{n}.png", T.OUT / "ep27" / f"{n}_check.png")
            print(f"{n}：名前 大きさ {fs:.1f}px・長体 {sx:.3f}・縁 {rim}・字の原点 x＝" + "・".join(f"{c}{x:.0f}" for c, x, *_ in gl))
            hx, hx3 = _hx()
            print("  赤い字（と縁）の外接の箱（x0, x1, y0, y1）：", hx.red_box(f"ep27/{n}"))
            print("  塊の数（点や画が縁でくっつかないか）：")
            hx3.pieces(gl, rim=rim)
            print(" ", T.OUT / "ep27" / f"{n}_check.png")
        return
    if style == "v6c":                                # ⑥'：v6 の地の別色版（明るい赤・白・紺）を焼いて v6 と並べる
        names = ["ep27_A6_v6"]
        for kind in V6C:
            b, px = body_a6c(kind)
            n = f"ep27_A6{kind}_v6"
            bake2(f"ep27/{n}", b)
            names.append(n)
        sheet3(names, T.OUT / "ep27" / "ep27_v6c_sheet.png")
        print(T.OUT / "ep27" / "ep27_v6c_sheet.png")
        return
    if style == "v6b":                                 # v6（キープ）と黒地版 v6b を焼いて並べる
        b, px = body_a6b()
        bake2("ep27/ep27_A6b_v6", b)
        sheet3(["ep27_A6_v6", "ep27_A6b_v6"], T.OUT / "ep27" / "ep27_v6_sheet.png")
        print(T.OUT / "ep27" / "ep27_v6_sheet.png")
        return
    if style == "v6":                                  # A6＝A5a の書体を明朝（キリンをもう一度と同じ）・テープを右上がり
        b, px = body_a6()
        n = arg("name", "ep27_A6_v6")
        bake2(f"ep27/{n}", b)
        check(T.OUT / "ep27" / f"{n}.png", T.OUT / "ep27" / f"{n}_check.png")
        print(T.OUT / "ep27" / f"{n}_check.png")
        return
    if style == "v5":                                  # A5a（1句の後ろに黒い帯）・A5b（左の地を黒に）
        names = []
        for key, bd in (("A5a", True), ("A5b", False)):
            b, px = body_a5(bd)
            n = f"ep27_{key}_v5"
            bake2(f"ep27/{n}", b)
            names.append(n)
        sheet3(names, T.OUT / "ep27" / "ep27_v5_sheet.png")
        print(T.OUT / "ep27" / "ep27_v5_sheet.png")
        return
    if style == "v4":                                  # A4a（なぜ＝黄）・A4b（全部赤）
        names = []
        for key, tt in (("A4a", True), ("A4b", False)):
            b, px = body_a4(tt)
            n = f"ep27_{key}_v4"
            bake2(f"ep27/{n}", b)
            names.append(n)
        sheet3(names, T.OUT / "ep27" / "ep27_v4_sheet.png")
        print(T.OUT / "ep27" / "ep27_v4_sheet.png")
        return
    if style == "v3":                                  # A3・B3・C3 を焼いて見比べの1枚に
        names = []
        for key, fn in (("A3", body_a3), ("B3", body_b3), ("C3", body_c3)):
            b, px = fn()
            n = f"ep27_{key}_v3"
            bake2(f"ep27/{n}", b)
            names.append(n)
        sheet3(names, T.OUT / "ep27" / "ep27_v3_sheet.png")
        print(T.OUT / "ep27" / "ep27_v3_sheet.png")
        return
    b, px = body()
    T.bake(f"ep27/{name}", b)
    png = T.OUT / "ep27" / f"{name}.png"
    check(png, T.OUT / "ep27" / f"{name}_check.png")
    print(f"写真の左端 x={px}・字の右端の上限 x={px - FRAME}")
    print(png)


if __name__ == "__main__":
    main()
