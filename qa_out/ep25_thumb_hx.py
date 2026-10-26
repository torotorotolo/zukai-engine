# -*- coding: utf-8 -*-
"""25本目 ⑥：サムネの H 型の反転版（承認①＝上「犠牲107人 遅れたブレーキ」・大きな語「JR福知山線」（「JR」は緑）・下「脱線事故の真相」）。
Vault の hx.py・hx3.py（14〜16本目の反転版の横展開の道具）の lay()・hx2() の骨組み・pieces()・inv_pair()・compare() を読むだけで使う
（Vault の道具は書き換えない・焼くのは qa_out/out/）。24本目 `qa_out/ep24_thumb_hx.py` の写し。
🆕「JR」は緑（承認① カズヤくん「「JR」は緑文字」）＝反転版の字の中は暗い白黒の写真＝J・R の2字だけ、字の中を緑に染めた暗い写真・縁も緑
   （ほかの4字は今までどおり暗い白黒・赤い縁）。
地＝10-26 カズヤくん「T2（付図12 の空撮）の拡大が最有力。T2 をより派手に再現した AI イラストを生成」
    T2＝`ref/ep25/f12.jpg`（653×449・PDL1.0）を寄せる段／AI＝`gen_thumb_ai fuk_a`（1792×1008 の原寸から）
    python qa_out/ep25_thumb_hx.py pieces   … 字ごとの塊の検査（縁でくっつかないか）
    python qa_out/ep25_thumb_hx.py cand     … T2 の寄せ3段＋AI の2段＋並べ（640／210／168px）＝大きな語「JR福知山線」（JR を緑の字の中と縁）
    python qa_out/ep25_thumb_hx.py cand2    … 2枚目の生成 fuk_b・大きな語「福知山線」＋緑の「JR」を左上に（右寄せ）
    python qa_out/ep25_thumb_hx.py cand3    … 大きな語を中央揃え（帯 40／110／180）＋JR との重なりを画素で測る
✅ 10-26 カズヤくんの決め：cand の5案 →「もっと車両に寄せて、横転した車両で画面がいっぱいになるようなイラストを生成」「JR は福知山線の左上に小さく」
   → cand2 →「福知山線は中央揃え。JR は福知山線の視認性を損なわない程度に少し被らせて OK」→ cand3 →「帯 110〜1170・1.20倍」
   ＝**`ep25_Hinv3_b_z120_L110.png`**（→ out/thumb/ep25/ep25_Hinv_fuk_b_z120_L110.png・md5 396949b4…・JR の字の 44% が「福」の縁に重なる）
"""
import sys
from pathlib import Path

RES = Path(r"C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証-サムネ海外競合5ch-20261012")
sys.path.insert(0, str(RES))
import hx  # noqa: E402
import hx3  # noqa: E402
from hx import T, WHT, YEL, RED, txt, lay, bake2, compare  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).parent / "out"
T.OUT = OUT
hx3.OUT = OUT

GIANT = "JR福知山線"
GREEN = "#19a33a"                                    # 「JR」の緑（縁と字の中の染め）
GREEN_RGB = (0x19, 0xa3, 0x3a)
# 太らせ：画の多い字（福・線）は0・知も0（8 だと「矢」と「口」が縁でくっついた＝pieces）・ほかは16（14〜19本目の決め＝細い画が縁で埋まらない）
BOLD = {"J": 16, "R": 16, "福": 0, "知": 0, "山": 16, "線": 0}
TOP = [("犠牲107人 ", WHT), ("遅れたブレーキ", RED)]   # 承認①の A・10-20 の型（「犠牲N人」は白・核心の語だけ赤）
BOTTOM = "脱線事故の真相"
BAND = (128, 580)                                    # 16本目・24本目と同じ帯（上下の行とのすき間 6px 以上を gap で測る）
ADJ = (1.20, 1.25, 1.15)                             # 本線 h_type_inv の字の外＝vivid_adj (1.15,1.15,1.0)＋H_VIVID_ADD (0.05,0.10,0.15)


def glyphs():
    gl, fs, sx = lay(GIANT, BAND[0], BAND[1], gap=4, bold=BOLD)
    return gl, fs, sx


def extra():
    tfs = hx3.top_fs("".join(s for s, _ in TOP))
    return [txt(TOP, 40, 104, tfs, WHT), txt(BOTTOM, 40, 692, 112, YEL, sw=16)], tfs


def green_of(dark_uri):
    """字の中の暗い白黒（data URI）を緑に染める（明るさ×緑）＝J・R の字の中。"""
    import base64
    import io
    from PIL import Image
    b = base64.b64decode(dark_uri.split(",", 1)[1])
    g = Image.open(io.BytesIO(b)).convert("L")
    lut = [tuple(min(255, int(c * (0.35 + 1.45 * v / 255))) for c in GREEN_RGB) for v in range(256)]
    im = Image.merge("RGB", [g.point([lut[v][k] for v in range(256)]) for k in range(3)])
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def hx2_jr(vivid, dim, glyphs, extra, green=None, rim=18):
    """hx.hx2 と同じ骨組み＋J・R の2字だけ縁を緑・字の中を緑の染め（green＝染めた暗い写真の data URI）。"""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen

    def tx(g, paint):
        c, x, b, f, sx, bd, font = g
        hx.ink(c, font)                               # 書体を読み込む
        gs, cmap, upm = hx._FT[font]
        sp = SVGPathPen(gs)
        gs[cmap[ord(c)]].draw(TransformPen(sp, (f * sx / upm, 0, 0, -f / upm, x, b)))
        return f'<path d="{sp.getCommands()}" {paint(bd)}/>'
    ve = 'stroke-linejoin="round"'
    jr = [g for g in glyphs if g[0] in "JR"]
    rest = [g for g in glyphs if g[0] not in "JR"]

    def white(bd):
        return f'fill="#fff" stroke="#fff" stroke-width="{bd}" {ve}' if bd else 'fill="#fff"'
    mask = "".join(tx(g, white) for g in rest)
    mask_jr = "".join(tx(g, white) for g in jr)
    rimt = "".join(tx(g, lambda bd, col=(GREEN if g[0] in "JR" else RED): f'fill="{col}" stroke="{col}" stroke-width="{rim + bd}" {ve}')
                   for g in glyphs)
    W, H = T.W, T.H
    return (f'<defs>{T.EP21_GRAD}'
            f'<mask id="km" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000"/>{mask}</mask>'
            f'<mask id="kj" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000"/>{mask_jr}</mask></defs>'
            f'{T.ep21_img(dim)}'
            f'<rect x="0" y="470" width="{W}" height="250" fill="url(#bt)"/>{rimt}'
            f'<image href="{vivid}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" mask="url(#km)"/>'
            f'<image href="{green or vivid}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" mask="url(#kj)"/>'
            + "".join(extra))


def rim_only_jr(name, gl):
    """地を無地の灰にして縁だけ（赤＋J・R は緑）＝字の中の範囲を取る（hx3.rim_only の写し・赤の画素で字の中を出すので J・R も赤で焼く）。"""
    g = T._ep21_jpeg(hx.Image.new("RGB", (T.W, T.H), (128, 128, 128)))
    bake2(name, hx.hx2(g, g, gl, []))
    hx.fit(name)


# 地の段：(札, 元, 切り出し, 字の外の明るさ, 並べの札)
GROUNDS = (
    ("t2_z100", "ep25/f12.jpg", dict(zoom=1.00, cx=0.50, cy=0.50), 1.15, "T2 付図12\n寄せなし\n（653px→1280）"),
    ("t2_z130", "ep25/f12.jpg", dict(zoom=1.30, cx=0.55, cy=0.40), 1.15, "T2 付図12\n1.30倍"),
    ("t2_z160", "ep25/f12.jpg", dict(zoom=1.60, cx=0.55, cy=0.35), 1.15, "T2 付図12\n1.60倍"),
    ("ai_z100", "ep25/ai/ep25_fuk_a_orig.png", dict(zoom=1.00, cx=0.50, cy=0.50), 1.15, "生成AI fuk_a\n寄せなし"),
    ("ai_z125", "ep25/ai/ep25_fuk_a_orig.png", dict(zoom=1.25, cx=0.45, cy=0.45), 1.15, "生成AI fuk_a\n1.25倍"),
)


# 🆕 10-26 カズヤくん（cand の並べを見て）「もっと車両に寄せて、横転した車両で画面がいっぱいになるようなイラストを生成」
#    「「JR」の文字は福知山線の左上に小さく表示」＝大きな語は「福知山線」の4字（型抜き・赤い縁）・「JR」は緑の字（黒フチ）を左の上の角に。
#    大きな語は「JR」の右から（左の端 JR2_LEFT）＝字の幅が広がる（6字の長体 0.49 → 4字）
GIANT2 = "福知山線"
BOLD2 = {"福": 0, "知": 0, "山": 16, "線": 0}
JR2_FS = 140                                         # 字の形の高さ 104px（J・R の上の端 0.74em）
JR2_X, JR2_BASE = 40, 128 + 9 + 104                  # 大きな語の帯の上の端（縁の外 128）＋縁の半分＋字の高さ
JR2_LEFT = 40 + 181 + 14                             # 「JR」の幅 181px（h_adv）＋すき間 14px


def glyphs2():
    return lay(GIANT2, BAND[0], BAND[1], left=JR2_LEFT, gap=6, bold=BOLD2)


def extra2():
    ex, tfs = extra()
    return ex + [txt("JR", JR2_X, JR2_BASE, JR2_FS, GREEN, sw=14)], tfs


GROUNDS2 = (
    ("b_z100", "ep25/ai/ep25_fuk_b_orig.png", dict(zoom=1.00, cx=0.50, cy=0.50), 1.15, "生成AI fuk_b\n寄せなし"),
    ("b_z120", "ep25/ai/ep25_fuk_b_orig.png", dict(zoom=1.20, cx=0.40, cy=0.55), 1.15, "生成AI fuk_b\n1.20倍"),
)


# 🆕 10-26 カズヤくん（cand2 の並べを見て）「「福知山線」は中央揃え。JRは「福知山線」の視認性を損なわない程度に少し被らせてOK」
#    ＝大きな語を左右対称の帯（左 L・右 1280−L）に置き、「JR」は左上の角のまま（x40・基線 241）＝重なりを画素で測る
#    （JR の字＋黒フチの範囲と、大きな語の字＋赤い縁の範囲の重なり）。L を3段で並べる
def masks_overlap(gl, tag):
    """JR の字（フチこみ）の範囲 × 大きな語（字の中＋赤い縁）の範囲の重なりの画素。"""
    import numpy as np
    from PIL import Image
    hx3.rim_only(f"_fit_{tag}", gl)
    inside, red = hx3.inside_mask(f"_fit_{tag}")
    giant = inside | red
    W, H = T.W, T.H
    body = (f'<rect x="0" y="0" width="{W}" height="{H}" fill="#000"/>'
            f'<text x="{JR2_X}" y="{JR2_BASE}" font-family="NSB" font-size="{JR2_FS}" fill="#fff" stroke="#fff" '
            f'stroke-width="14" stroke-linejoin="round" paint-order="stroke fill">JR</text>')
    bake2(f"_jr_{tag}", body)
    jr = np.asarray(Image.open(OUT / f"_jr_{tag}.png").convert("L")) > 128
    ov = jr & giant
    return int(ov.sum()), int(jr.sum()), int(giant.sum())


LEFTS3 = (40, 110, 180)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if "cand3" in sys.argv:
        ex2, tfs = extra2()
        for gtag, src, crop, b, glb in GROUNDS2:
            rows = []
            for L in LEFTS3:
                gl3, fs3, sx3 = lay(GIANT2, BAND[0], BAND[1], left=L, right=T.W - L, gap=6, bold=BOLD2)
                bad = hx3.pieces(gl3)
                ov, jr, gi = masks_overlap(gl3, f"ep25c_{L}")
                d, c = hx3.inv_pair(src, ADJ, crop, out_bright=b)
                name = f"ep25_Hinv3_{gtag}_L{L}"
                bake2(name, hx.hx2(d, c, gl3, ex2))
                print(f"  {name}: 長体 {sx3:.3f}・塊の検査 {'⚠️ ' + ''.join(bad) if bad else '0件'}・"
                      f"JR と大きな語の重なり {ov}px（JR の {100 * ov / jr:.1f}%・大きな語の {100 * ov / gi:.2f}%）")
                rows.append((OUT / f"{name}.png", f"{glb.splitlines()[0]}\n{glb.splitlines()[1]}\n帯 {L}〜{T.W - L}\n重なり {100 * ov / jr:.0f}%"))
            compare(rows, f"cmp25_c_{gtag}.png")
        sys.exit(0)
    if "cand2" in sys.argv:
        gl2, fs2, sx2 = glyphs2()
        print(f"{GIANT2}：大きさ {fs2:.0f}・長体 {sx2:.3f}")
        bad = hx3.pieces(gl2)
        print("塊の検査：", "⚠️ " + "".join(bad) if bad else "0件")
        ex2, tfs = extra2()
        hx3.rim_only("_fit_ep25b", gl2)
        inside, red = hx3.inside_mask("_fit_ep25b")
        rows = []
        for tag, src, crop, b, lb in GROUNDS2:
            d, c = hx3.inv_pair(src, ADJ, crop, out_bright=b)
            name = f"ep25_Hinv2_{tag}"
            bake2(name, hx.hx2(d, c, gl2, ex2))
            i, o, df = hx3.lum(name, inside, red)
            print(f"  {name}: 字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}")
            rows.append((OUT / f"{name}.png", lb))
        compare(rows, "cmp25_b.png")
        sys.exit(0)
    gl, fs, sx = glyphs()
    if "pieces" in sys.argv:
        print(f"{GIANT}：大きさ {fs:.0f}・長体 {sx:.3f}")
        bad = hx3.pieces(gl)
        print("塊の検査：", "⚠️ " + "".join(bad) if bad else "0件")
    if "cand" in sys.argv:
        ex, tfs = extra()
        print(f"上の行の大きさ {tfs}・幅 {T.h_adv(''.join(s for s, _ in TOP), tfs):.0f}px")
        rim_only_jr("_fit_ep25", gl)
        inside, red = hx3.inside_mask("_fit_ep25")
        rows = []
        for tag, src, crop, b, lb in GROUNDS:
            d, c = hx3.inv_pair(src, ADJ, crop, out_bright=b)
            name = f"ep25_Hinv_{tag}"
            bake2(name, hx2_jr(d, c, gl, ex, green=green_of(d)))
            i, o, df = hx3.lum(name, inside, red)
            print(f"  {name}: 字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}")
            rows.append((OUT / f"{name}.png", lb))
        compare(rows[:3], "cmp25_t2.png")
        compare(rows[3:], "cmp25_ai.png")
