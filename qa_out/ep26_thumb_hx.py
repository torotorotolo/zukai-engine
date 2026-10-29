# -*- coding: utf-8 -*-
"""26本目 ⑥：サムネの H 型の反転版（承認①＝上「犠牲1490人 信号弾を見た船」・大きな語「タイタニック号」・下「沈没事故の真相」）。
Vault の hx.py・hx3.py（14〜16本目の反転版の横展開の道具）の lay()・hx2()・pieces()・inv_pair()・compare() を読むだけで使う
（Vault の道具は書き換えない・焼くのは qa_out/out/）。25本目 `qa_out/ep25_thumb_hx.py` の写し（JR の緑は外した）。
地＝materials.md §7 の T1（S1-002 出航するタイタニック号・PD）・T2（S8-625 カリフォルニアン号・NARA・PD）＝1912年の白黒
    python qa_out/ep26_thumb_hx.py pieces   … 字ごとの塊の検査（縁でくっつかないか）
    python qa_out/ep26_thumb_hx.py cand     … T1・T2 の寄せなし＋寄せ＋並べ（640／210／168px）・字の中と外の明るさの差
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

GIANT = "タイタニック号"
# 太らせ：小さい「ッ」と画の多い「号」は0（18本目の決め・「ッ」が「ウ」に見えた＝10-20）・ほかは16（細い画が縁で埋まらない）
BOLD = {"タ": 16, "イ": 16, "ニ": 16, "ッ": 0, "ク": 16, "号": 0}
TOP = [("犠牲1490人 ", WHT), ("信号弾を見た船", RED)]   # 承認①の D・10-20 の型（「犠牲N人」は白・核心の語だけ赤）
BOTTOM = "沈没事故の真相"
BAND = (128, 580)                                    # 16・24・25本目と同じ帯（上下の行とのすき間 6px 以上を gap で測る）
ADJ = (1.20, 1.25, 1.15)                             # 本線 h_type_inv の字の外＝vivid_adj (1.15,1.15,1.0)＋H_VIVID_ADD (0.05,0.10,0.15)


def glyphs():
    return lay(GIANT, BAND[0], BAND[1], gap=4, bold=BOLD)


def extra():
    tfs = hx3.top_fs("".join(s for s, _ in TOP))
    return [txt(TOP, 40, 104, tfs, WHT), txt(BOTTOM, 40, 692, 112, YEL, sw=16)], tfs


# 地の段：(札, 元, 切り出し, 字の外の明るさ, 並べの札)
GROUNDS = (
    ("t1_z100", "ep26/s1_002.jpg", dict(zoom=1.00, cx=0.50, cy=0.50), 1.15, "T1 S1-002\n出航する\nタイタニック号\n寄せなし"),
    ("t1_z140", "ep26/s1_002.jpg", dict(zoom=1.40, cx=0.50, cy=0.45), 1.15, "T1 S1-002\n1.40倍"),
    ("t2_z100", "ep26/s8_625.jpg", dict(zoom=1.00, cx=0.50, cy=0.50), 1.15, "T2 S8-625\nカリフォルニアン号\n寄せなし"),
    ("t2_z140", "ep26/s8_625.jpg", dict(zoom=1.40, cx=0.50, cy=0.50), 1.15, "T2 S8-625\n1.40倍"),
)


# 🆕 10-28 カズヤくん（cand の並べを見て）「T1 最有力候補。生成AIも作る。AI案は、沈みゆくタイタニック号のインパクトがある実写イラスト」
#    ＝`gen_thumb_ai ttn_a`（夜）。夜の地は字の外の明るさを段で並べる（16本目＝1.60）・寄せは生成の原寸から（24本目）
AI_SRC = "ep26/ai/ep26_ttn_a_orig.png"


def bright_center(src, top=0.03):
    """地のいちばん明るい画素（上位 top）の重心を、T.photo の cx・cy（余りのうちの割合）に直す＝灯と信号弾を寄せの中心に。"""
    import numpy as np
    from PIL import Image
    im = Image.open(Path(__file__).resolve().parent.parent / "ref" / src).convert("L")
    a = np.asarray(im, float)
    ys, xs = np.nonzero(a >= np.quantile(a, 1 - top))
    return im.size, xs.mean(), ys.mean()


def crop_at(src, zoom, px, py):
    """(px, py) を寄せたあとの画面の中心に置く cx・cy（端に当たれば 0／1 で止める）。"""
    (w, h), _, _ = bright_center(src)
    z = max(T.W / w, T.H / h) * zoom
    cw, ch = min(w, T.W / z), min(h, T.H / z)
    cx = 0.5 if w <= cw else min(1.0, max(0.0, (px - cw / 2) / (w - cw)))
    cy = 0.5 if h <= ch else min(1.0, max(0.0, (py - ch / 2) / (h - ch)))
    return dict(zoom=zoom, cx=round(cx, 3), cy=round(cy, 3))


# 🆕 10-28 カズヤくん（cand2 の並べを見て）「AI写真を再生成。もっと派手で目を引くような写真にして。誇張もOK。生成前に案を出して、私の承認後にGO」
#    → 3案から案A「船尾が空へ立ち上がる」＝`gen_thumb_ai ttn_b`。夜の地＝字の外の明るさ 1.00／1.30／1.60（16本目の型）＋明るい所への寄せ
AI_SRC_B = "ep26/ai/ep26_ttn_b_orig.png"
# 🆕 10-28 カズヤくん「A/B：1.60をA・T1をB」→ 生成の原寸を見たら船尾の曲面に金色の字のような列（札の「字を描かない」が守られていない）
#    ＝原寸 x1633〜1669・y87〜122 の金色の画素だけを3画素ふくらませて周りから埋める（cv2.inpaint）＝`fix` で別名に（元の生成は残す）
AI_SRC_BF = "ep26/ai/ep26_ttn_b_fix_orig.png"
STERN_BOX = (1600, 80, 1710, 175)                    # (x0, y0, x1, y1) 金色の字を探す箱（原寸）


def fix_stern():
    import cv2
    import numpy as np
    from PIL import Image
    ref = Path(__file__).resolve().parent.parent / "ref"
    a = np.asarray(Image.open(ref / AI_SRC_B).convert("RGB"))
    x0, y0, x1, y1 = STERN_BOX
    s = a[y0:y1, x0:x1].astype(int)
    R, G, B = s[..., 0], s[..., 1], s[..., 2]
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = ((R > 110) & (G > 80) & (B < R - 25) & (R - B > 40)).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    out = cv2.inpaint(np.ascontiguousarray(a[..., ::-1]), m, 5, cv2.INPAINT_TELEA)[..., ::-1]
    Image.fromarray(out).save(ref / AI_SRC_BF)
    s2 = out[y0:y1, x0:x1].astype(int)
    left = ((s2[..., 0] > 110) & (s2[..., 1] > 80) & (s2[..., 2] < s2[..., 0] - 25) & (s2[..., 0] - s2[..., 2] > 40)).sum()
    print(f"埋めた画素 {int((m > 0).sum())}・直したあとの金色の画素 {int(left)}（箱 {STERN_BOX}）→ ref/{AI_SRC_BF}")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    gl, fs, sx = glyphs()
    if "fix" in sys.argv:
        fix_stern()
        sys.exit(0)
    if "gap" in sys.argv:
        # Vault gap.py と同じ式（上下の行〈黒フチこみ〉と大きな語の赤い縁のすき間を列ごとに）＝置き場だけ qa_out/out（目安 6px 以上）
        import numpy as np
        from PIL import Image
        ex, tfs = extra()
        bake2("_txt_ep26", f'<rect width="{T.W}" height="{T.H}" fill="#fff"/>' + "".join(ex))
        t = np.asarray(Image.open(OUT / "_txt_ep26.png").convert("L")) < 250
        hx3.rim_only("_fit_ep26", gl)
        a = np.asarray(Image.open(OUT / "_fit_ep26.png").convert("RGB")).astype(int)
        r = (abs(a[..., 0] - 0xd8) < 40) & (a[..., 1] < 60) & (a[..., 2] < 70)
        up, dn = [], []
        for x in range(T.W):
            ty, ry = np.nonzero(t[:, x])[0], np.nonzero(r[:, x])[0]
            if len(ry) == 0:
                continue
            tu, td = ty[ty < 360], ty[ty >= 360]
            if len(tu):
                up.append((int(ry.min() - tu.max() - 1), x))
            if len(td):
                dn.append((int(td.min() - ry.max() - 1), x))
        print(f"  上の行の下端 → 大きな語の縁の上端：最小 {min(up)[0]}px（x{min(up)[1]}）")
        print(f"  大きな語の縁の下端 → 下の行の上端：最小 {min(dn)[0]}px（x{min(dn)[1]}）")
        sys.exit(0 if min(up)[0] >= 6 and min(dn)[0] >= 6 else 1)
    if "final" in sys.argv:
        # A＝ttn_b（直した版）寄せなし・字の外 1.60／B＝T1 寄せなし（カズヤくんが Studio で手動）＝out/thumb/ep26/ へ写すのは別の手で
        ex, tfs = extra()
        hx3.rim_only("_fit_ep26", gl)
        inside, red = hx3.inside_mask("_fit_ep26")
        rows = []
        for tag, src, crop, b, lb in (
                ("A_ttn_b_fix_z100_b160", AI_SRC_BF, dict(zoom=1.00, cx=0.50, cy=0.50), 1.60, "A 生成AI ttn_b\n（船尾の字を消した版）\n寄せなし 字の外 1.60"),
                ("B_t1_z100", "ep26/s1_002.jpg", dict(zoom=1.00, cx=0.50, cy=0.50), 1.15, "B T1 S1-002\n寄せなし\n（Studio で手動）")):
            d, c = hx3.inv_pair(src, ADJ, crop, out_bright=b)
            name = f"ep26_{tag}"
            bake2(name, hx.hx2(d, c, gl, ex))
            i, o, df = hx3.lum(name, inside, red)
            print(f"  {name}: 字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}")
            rows.append((OUT / f"{name}.png", lb))
        compare(rows, "cmp26_final.png")
        sys.exit(0)
    if "cand3" in sys.argv:
        ex, tfs = extra()
        hx3.rim_only("_fit_ep26", gl)
        inside, red = hx3.inside_mask("_fit_ep26")
        _, bx, by = bright_center(AI_SRC_B)
        z125 = crop_at(AI_SRC_B, 1.25, bx, by)
        print(f"生成の地 ttn_b の明るい所の重心 x{bx:.0f}・y{by:.0f}（原寸）→ 1.25倍の切り出し {z125}")
        grounds = (
            ("b_z100_b100", AI_SRC_B, dict(zoom=1.00, cx=0.50, cy=0.50), 1.00, "生成AI ttn_b（案A）\n寄せなし\n字の外 1.00"),
            ("b_z100_b130", AI_SRC_B, dict(zoom=1.00, cx=0.50, cy=0.50), 1.30, "生成AI ttn_b\n寄せなし\n字の外 1.30"),
            ("b_z100_b160", AI_SRC_B, dict(zoom=1.00, cx=0.50, cy=0.50), 1.60, "生成AI ttn_b\n寄せなし\n字の外 1.60"),
            ("b_z125_b130", AI_SRC_B, z125, 1.30, "生成AI ttn_b\n1.25倍（明るい所）\n字の外 1.30"),
        )
        rows = [(Path(__file__).resolve().parent.parent / "ref" / "ep26" / "ai" / "ep26_ttn_b.jpg", "生成の地 ttn_b\nそのもの\n（字・顔の確認）")]
        for tag, src, crop, b, lb in grounds:
            d, c = hx3.inv_pair(src, ADJ, crop, out_bright=b)
            name = f"ep26_Hinv_{tag}"
            bake2(name, hx.hx2(d, c, gl, ex))
            i, o, df = hx3.lum(name, inside, red)
            print(f"  {name}: 字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}")
            rows.append((OUT / f"{name}.png", lb))
        compare(rows, "cmp26_c.png")
        sys.exit(0)
    if "cand2" in sys.argv:
        ex, tfs = extra()
        hx3.rim_only("_fit_ep26", gl)
        inside, red = hx3.inside_mask("_fit_ep26")
        _, bx, by = bright_center(AI_SRC)
        z135 = crop_at(AI_SRC, 1.35, bx, by)
        print(f"生成の地の明るい所の重心 x{bx:.0f}・y{by:.0f}（原寸）→ 1.35倍の切り出し {z135}")
        grounds = (
            ("ai_z100_b130", AI_SRC, dict(zoom=1.00, cx=0.50, cy=0.50), 1.30, "生成AI ttn_a\n寄せなし\n字の外 1.30"),
            ("ai_z100_b160", AI_SRC, dict(zoom=1.00, cx=0.50, cy=0.50), 1.60, "生成AI ttn_a\n寄せなし\n字の外 1.60"),
            ("ai_z135_b160", AI_SRC, z135, 1.60, "生成AI ttn_a\n1.35倍（明るい所）\n字の外 1.60"),
            ("t1_z100", "ep26/s1_002.jpg", dict(zoom=1.00, cx=0.50, cy=0.50), 1.15, "T1 S1-002\n寄せなし\n（比べ）"),
        )
        rows = [(Path(__file__).resolve().parent.parent / "ref" / "ep26" / "ai" / "ep26_ttn_a.jpg", "生成の地そのもの\n（字・顔の確認）")]
        for tag, src, crop, b, lb in grounds:
            d, c = hx3.inv_pair(src, ADJ, crop, out_bright=b)
            name = f"ep26_Hinv_{tag}"
            bake2(name, hx.hx2(d, c, gl, ex))
            i, o, df = hx3.lum(name, inside, red)
            print(f"  {name}: 字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}")
            rows.append((OUT / f"{name}.png", lb))
        compare(rows, "cmp26_b.png")
        sys.exit(0)
    if "pieces" in sys.argv or "cand" in sys.argv:
        print(f"{GIANT}：大きさ {fs:.0f}・長体 {sx:.3f}")
        bad = hx3.pieces(gl)
        print("塊の検査：", "⚠️ " + "".join(bad) if bad else "0件")
    if "cand" in sys.argv:
        ex, tfs = extra()
        print(f"上の行の大きさ {tfs}・幅 {T.h_adv(''.join(s for s, _ in TOP), tfs):.0f}px")
        hx3.rim_only("_fit_ep26", gl)
        inside, red = hx3.inside_mask("_fit_ep26")
        rows = []
        for tag, src, crop, b, lb in GROUNDS:
            d, c = hx3.inv_pair(src, ADJ, crop, out_bright=b)
            name = f"ep26_Hinv_{tag}"
            bake2(name, hx.hx2(d, c, gl, ex))
            i, o, df = hx3.lum(name, inside, red)
            print(f"  {name}: 字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}")
            rows.append((OUT / f"{name}.png", lb))
        compare(rows, "cmp26_a.png")
