# -*- coding: utf-8 -*-
"""事故検証チャンネルのサムネイル。**必ず写真を使う**（2026-07-30 カズヤくん指示）。

■ 2026-07-30：競合のサムネを**画素で実測**して型を作り直した
指示は「競合を徹底的に分析して、ヒットしている動画と型をそろえる。その後でオリジナリティを足す」。
`ゆっくり事故検証`（登録7.3万）の全期間人気順から上位12本＋下位8本の maxresdefault を落とし、
彩度と色相で赤い行・黄色い行を検出して寸法を測った。

■ 実測した競合の型（上位12本／下位8本ともまったく同じ＝これは「守って当然の土俵」）

    ┌─────────────────────────────┐  ← 写真は**全面**。上下に黒帯は無い
    │ 赤1行  上端に密着 y=15〜170          │     字面の高さ **約150px**（画面の21%）
    │        全幅 x=16〜1264（画面の97%）  │     色 **#c30a08**（純赤ではなく濃い臙脂）
    │                                     │     **白フチ**（太い）
    │   写真（左右に2枚並べることが多い）   │  ← 事故前／事故後、本体／残骸 の対比
    │                                     │
    │ 黄1行  下端に密着 y=525〜705         │     字面の高さ **約180px**（25%）
    │        全幅                          │     色 **#fbfb0e** ／ **黒フチ**
    └─────────────────────────────┘

    ⚠️ **副題・カテゴリタブ・原因チップ・年代バッジ・出典は competitor には1つも無い。**
       文字は赤1行と黄1行の**2行だけ**。それぞれを画面幅いっぱいまで潰して最大化している。
    ⚠️ 書体は**角張った極太**（Noto Sans JP Black 相当）。Dela Gothic One の丸ゴシックではない。
    ⚠️ 文字数は赤・黄とも **10〜14字**。

■ 第1稿・第2稿が外していた点（全部直した）
    | | 競合 | こちらの旧案 |
    |---|---|---|
    | 赤の字面 | 150px | 96px（1.6倍小さい） |
    | 赤の幅 | 画面の97% | 63% |
    | 赤のフチ | **白** | 黒 |
    | 黄の字面 | 180px | 148px |
    | 余計な要素 | **ゼロ** | 副題・タブ・原因チップ・バッジ・出典の5つ |
    | 書体 | 角張った極太 | Dela（丸い） |
    | 写真 | 2枚並べ | 1枚 |

■ オリジナリティ（型を壊さない範囲でだけ足す）
    型は competitor と同一のまま、**写真の中身だけ**を唯一無二にする。
      左＝タイタニックの船首（NOAA・PD）／右＝**回収された耐圧殻の破断面**（NTSB・PD）
    右は2025年10月公開の報告書の写真で、**競合の96万本（2025-02-16公開）には存在しない**。
    枠は横並び＝競合の型そのもの。中身だけが誰も持っていない。

使い方： python tools/thumb_jiko.py
"""
import base64
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageEnhance

import render

HERE = Path(__file__).parent.parent
FONTS = HERE / "fonts"
OUT = HERE / "out" / "thumb"
W, H = 1280, 720

# ── 実測した競合の値。**ここは競合に合わせる。勝手に動かさない** ────
RED = "#c30a08"          # 上の行。純赤ではなく濃い臙脂
YEL = "#fbfb0e"          # 下の行。緑寄りの純黄
MG = 16                  # 左右の余白（実測 13〜26 の中央値）
TXT_W = W - MG * 2       # 1248
RED_CAP = 150            # 赤の字面の高さ
RED_BASE = 168           # 赤のベースライン（字面 15〜170）
YEL_CAP = 180            # 黄の字面の高さ
YEL_BASE = 703           # 黄のベースライン（字面 523〜705）

# Noto Sans JP Black の実測字幅（em）。全角はほぼ 1.0、半角数字は 0.56
FULL, HALF = 1.0, 0.56


def face(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:900;font-display:block;}}")


def units(t):
    return sum(HALF if ord(c) < 0x2E80 else FULL for c in t)


def size_for(t, cap):
    """字面の高さ cap になる font-size。Noto Sans JP の字面はおよそ 0.72em。

    横は textLength で全幅に潰すので、**級数は高さだけで決める**。
    ⚠️ 文字数が多いと横に潰れすぎて読めなくなる。10〜14字に収めること
       （競合も全部そこに収めている）。
    """
    return cap / 0.72


def line(t, base, cap, fill, stroke, sw):
    return (f'<text x="{MG}" y="{base}" font-family="NSB" font-size="{size_for(t, cap):.1f}" '
            f'textLength="{TXT_W}" lengthAdjust="spacingAndGlyphs" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" '
            f'paint-order="stroke fill">{t}</text>')


def photo(src, cy=0.5, contrast=1.18, color=1.12, bright=0.96, w=W, h=H):
    """写真を箱いっぱいに切り出して data URI にする。"""
    im = Image.open(HERE / "ref" / src).convert("RGB")
    z = max(w / im.width, h / im.height)
    cw, ch = min(im.width, w / z), min(im.height, h / z)
    l, t = (im.width - cw) / 2, (im.height - ch) * cy
    im = im.crop((round(l), round(t), round(l + cw), round(t + ch))).resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(color)
    im = ImageEnhance.Brightness(im).enhance(bright)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def rival_type(hero, red, yellow, split=None, extra=""):
    """競合と同一の型。**赤1行・黄1行・写真だけ。**

    hero  … 全面に敷く写真の data URI
    split … (右半分の data URI, 継ぎ目のx) を渡すと左右2枚並べになる
    extra … オリジナリティを足すときだけ使う。**空が既定**
    """
    g = [f'<image href="{hero}" x="0" y="0" width="{W}" height="{H}" '
         f'preserveAspectRatio="xMidYMid slice"/>']
    if split:
        # ⚠️ 右半分の写真は**その枠の寸法(640×720)で作ったもの**を渡すこと。
        #    1280×720 で作った画像を 640幅の枠に slice で入れると倍に寄って、
        #    耐圧殻が「木の板と黄色いテープ」にしか見えなくなった（t4の失敗）。
        uri, sx = split
        g.append(f'<image href="{uri}" x="{sx}" y="0" width="{W - sx}" height="{H}" '
                 f'preserveAspectRatio="xMidYMid slice"/>')
    # 黄色の行だけ下地に負けやすいので、下端に薄い暗幕を敷く（競合も暗い写真を選んでいる）。
    # 型を変えるものではなく、明るい写真を使ったときの保険。
    g.append(f'<linearGradient id="sb" x1="0" y1="1" x2="0" y2="0">'
             f'<stop offset="0" stop-color="#000" stop-opacity="0.46"/>'
             f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
             f'<rect x="0" y="{H - 260}" width="{W}" height="260" fill="url(#sb)"/>')
    g.append(extra)
    # 赤は白フチ、黄は黒フチ（実測）。フチは太くしないと写真の上で消える。
    # 赤が「濃い臙脂＋白フチ」なのは、明るい下地では文字色が・暗い下地ではフチが効くから。
    g.append(line(red, RED_BASE, RED_CAP, RED, "#ffffff", 17))
    g.append(line(yellow, YEL_BASE, YEL_CAP, YEL, "#000000", 20))
    return "".join(g)


def bake(name, body):
    css = face("NSB", "NotoSansJP-Black.woff2")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">{body}</svg>')
    html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
            f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')
    OUT.mkdir(parents=True, exist_ok=True)
    render.png(html, OUT / f"{name}.png", W, H)
    print(name, len(body) // 1024, "KB", flush=True)


# ── 素材（すべてパブリックドメイン。出所は ref/CREDITS.md） ────────
PH_BOW = "titan_titanic_bow.jpg"    # NOAA/IFE/URI 2004年調査：タイタニックの船首
PH_HULL = "titan_hull_edge.jpg"     # NTSB図14下：耐圧殻の中央破断面。層が刃のように裂けている
PH_INNER = "titan_hull_inner.jpg"   # NTSB図13下：耐圧殻の内面。白い部分が繊維の破断


def titan():
    """⚠️ 数字は**すべて NTSB/MIR-25-36 の本文で確認したもの**だけ。

    引き継ぎメモの「約0.001秒で爆縮」は報告書に無い（全文検索で `0.001` も
    `millisecond` も出ない）。「8回潜り続けた」も不正確で、潜航記録は
      81 = 3,840m ／ 82 = 3,840m ／ 83 = 2,954m ／ 84〜87 = 10m以下 ／ 88 = 爆縮。

    決め語は競合に合わせて **赤10〜14字・黄10〜14字**。
    競合のタイタン号（96万回）は 赤「乗客5名 爆縮の瞬間」／黄「タイタン号事故の真相」。
    同じ土俵に乗せたうえで、**赤の中身を「報告書で初めて分かったこと」に差し替える**。
    """
    SX = 620                       # 継ぎ目。競合は左右ぴったり半々ではない（実測 283〜977）
    RW = W - SX
    bow_full = photo(PH_BOW, cy=0.46, contrast=1.22, color=1.18, bright=0.98)
    bow_left = photo(PH_BOW, cy=0.46, contrast=1.22, color=1.18, bright=0.98, w=SX, h=H)
    hull_r = photo(PH_HULL, cy=0.52, contrast=1.34, color=1.02, bright=1.04, w=RW, h=H)
    inner_r = photo(PH_INNER, cy=0.50, contrast=1.30, color=1.06, bright=1.02, w=RW, h=H)

    # R1：型どおり・写真1枚（競合の最小形）。決め語も競合と同型
    bake("titan_R1", rival_type(
        bow_full, "乗客5名 爆縮の瞬間", "タイタン号事故の真相"))

    # R2：型どおり・写真2枚並べ＋決め語をこちらの切り口に
    #     ← **これが本命。**枠は競合と同一、中身だけが報告書の写真で唯一無二
    bake("titan_R2", rival_type(
        bow_left, "壊れた船体で3回潜航", "タイタン号事故の真相", split=(hull_r, SX)))

    # R3：R2 の右を「耐圧殻の内面」に。白い破断面のほうが遠目で目立つか比較する
    bake("titan_R3", rival_type(
        bow_left, "壊れた船体で3回潜航", "タイタン号事故の真相", split=(inner_r, SX)))

    # R4：赤を死者数の型に寄せる（競合の最頻パターン＝数字＋死者数＋「の瞬間」）
    bake("titan_R4", rival_type(
        bow_left, "5名死亡 爆縮の瞬間", "タイタン号事故の真相", split=(hull_r, SX)))

    # R5：黄色をこちらの切り口に寄せる（競合は事故名で固定だが、ここは差を作れる余地）
    bake("titan_R5", rival_type(
        bow_left, "報告書が示した8回目", "タイタン号 爆縮の真相", split=(hull_r, SX)))


if __name__ == "__main__":
    titan()
