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

from PIL import Image

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
    if style == "v6c":                                 # ⑥'：v6 の地の別色版（明るい赤・白・紺）を焼いて v6 と並べる
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
