# -*- coding: utf-8 -*-
"""32本目 ⑥：サムネの H 型の反転版（`qa_out/ep31_thumb_hx.py` の写し・言葉と地だけ替えた）。
記憶 feedback-jiko-thumbnail-rival-format＝H 型は反転だけを作る（10-20）・事件と事故の回は H 反転版を最初の並べに入れる（11-06）。
Vault の hx.py・hx3.py の lay()・hx2()・pieces()・inv_pair()・compare() を読み込んで使う（Vault の道具は書き換えない）。
言葉＝承認①の題 A'（ハドソン川の奇跡の真相。判断の35秒を足して空港へ戻るシミュレーターの試しは、滑走路に届かなかった）と事故の呼び名。
  🔴 この回の線＝「犠牲」「死亡」を使わない（全員が生きて帰った回）・名前を出すのは機長と副操縦士だけ（サムネには出さない）・人の形を描かない。
  上の行の数＝台本 c103「155人は、全員が生きて帰った」。
地（権利＝字を重ねてよい物だけ＝PD・CC BY。BY-SA は使わない＝重ねると翻案）：
  c26＝翼の上に人が並ぶ機体（CC BY 2.0・遠景＝顔は分からない）／c21＝消防艇と機体の尾翼（PD-USACE）／c15＝機体とフェリー（CC BY 2.0）
  ⚠️ CC BY は概要欄に作者・ライセンス・改変（切出・文字入れ・色の調整）を書く
案は版ごとに名前を分ける（同じ名前へ焼き直さない）。

    python -P qa_out/ep32_thumb_hx.py cand    … A・B を地の候補で並べる（640／210／168px）・字の中と外・塊の検査
    python -P qa_out/ep32_thumb_hx.py zooms   … c26 の寄せ 1.5／1.75／2.0倍（機体の幅＝画面の約78／91／104%）
    python -P qa_out/ep32_thumb_hx.py gap A   … 上下の行と大きな語の縁のすき間（6px 以上）
✅ 決め（11-12 カズヤくん「2倍」）＝`out/thumb/ep32/ep32_Hinv_Ac26_z200.png`（md5 eaf74635…・0.70MB）＝地 c26・寄せ 2.0倍
   （zoom 2.0・cx 0.62・cy 0.459＝機体の中心を画面の (640, 370) へ）・上の行 A・縁は赤・機体は字の後ろ。原寸で人影の顔は分からない・字や印なし
"""
import sys
from pathlib import Path

RES = Path(r"C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証-サムネ海外競合5ch-20261012")
sys.path.insert(0, str(RES))
import hx  # noqa: E402
import hx3  # noqa: E402
from hx import T, WHT, YEL, RED, txt, lay, bake2, compare  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent.parent / "out" / "thumb" / "ep32"
T.OUT = OUT
hx3.OUT = OUT

BAND = (128, 580)                                    # 16・24〜31本目と同じ帯
ADJ = (1.20, 1.25, 1.15)                             # 26・28・30・31本目と同じ（字の外＝vivid_adj＋H_VIVID_ADD）
# 太らせ：画の少ないカタカナと「川」は 16・小さな点の多い字（ド＝濁点）は 0・ンは 8（30本目「サリン」の値）＝`pieces` で塊を見る
GIANT = dict(giant="ハドソン川", bold={"ハ": 16, "ド": 0, "ソ": 16, "ン": 8, "川": 16})
WORDS = {
    # A＝22本目・31本目の型（乗員乗客の数＋その人たちがどうなったか）＝台本 c103
    "A": dict(GIANT, top=[("乗員乗客155人 ", WHT), ("全員生還", RED)], bottom="奇跡の真相"),
    # B＝芯 A の問い（第4章の題「本当に、空港へは戻れなかったのか」）
    "B": dict(GIANT, top=[("空港へ ", WHT), ("戻れたのか", RED)], bottom="奇跡の真相"),
}
TOPNOTE = {"A": "22・31本目の型（人数＋どうなったか）", "B": "芯Aの問い（第4章）"}
# 地と切り出し（thumb_jiko.photo の zoom・cx・cy＝cx・cy は余りの幅の何割を左・上で切るか）
GROUNDS = {
    "c26": ("ep32/c26.jpg", dict(zoom=1.15, cx=1.00, cy=0.45)),
    "c21": ("ep32/c21.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "c15": ("ep32/c15.jpg", dict(zoom=1.60, cx=0.61, cy=0.38)),
}
GNAME = {"c26": "c26 翼の上に人（CC BY 2.0）", "c21": "c21 消防艇と尾翼（PD）", "c15": "c15 機体とフェリー（CC BY 2.0）"}


def glyphs(k):
    w = WORDS[k]
    return lay(w["giant"], BAND[0], BAND[1], gap=4, bold=w["bold"])


def extra(k):
    w = WORDS[k]
    tfs = hx3.top_fs("".join(s for s, _ in w["top"]))
    return [txt(w["top"], 40, 104, tfs, WHT), txt(w["bottom"], 40, 692, 112, YEL, sw=16)], tfs


def bake(k, g, bright=1.15, tag="", crop=None):
    src, crop0 = GROUNDS[g]
    crop = crop or crop0
    gl, fs, sx = glyphs(k)
    ex, tfs = extra(k)
    fit = f"_fit_ep32_{k}"
    hx3.rim_only(fit, gl)
    inside, red = hx3.inside_mask(fit)
    d, c = hx3.inv_pair(src, ADJ, crop, out_bright=bright)
    name = f"ep32_Hinv_{k}{g}{tag}"
    bake2(name, hx.hx2(d, c, gl, ex))
    i, o, df = hx3.lum(name, inside, red)
    bad = hx3.pieces(gl)
    print(f"  {name}: 大きさ {fs:.0f}・長体 {sx:.3f}・上の行 {tfs}・字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}・塊 {''.join(bad) if bad else '0件'}"
          f"・切り出し {crop}")
    return OUT / f"{name}.png"


def gap(k):
    # Vault gap.py と同じ式（上下の行〈黒フチこみ〉と大きな語の赤い縁のすき間を列ごとに）
    import numpy as np
    from PIL import Image
    gl, _, _ = glyphs(k)
    ex, _ = extra(k)
    bake2("_txt_ep32", f'<rect width="{T.W}" height="{T.H}" fill="#fff"/>' + "".join(ex))
    t = np.asarray(Image.open(OUT / "_txt_ep32.png").convert("L")) < 250
    hx3.rim_only(f"_fit_ep32_{k}", gl)
    a = np.asarray(Image.open(OUT / f"_fit_ep32_{k}.png").convert("RGB")).astype(int)
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
    print(f"  {k} 上の行の下端 → 大きな語の縁の上端：最小 {min(up)[0]}px（x{min(up)[1]}）")
    print(f"  {k} 大きな語の縁の下端 → 下の行の上端：最小 {min(dn)[0]}px（x{min(dn)[1]}）")
    return min(up)[0] >= 6 and min(dn)[0] >= 6


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if "gap" in sys.argv:
        k = sys.argv[sys.argv.index("gap") + 1]
        sys.exit(0 if gap(k) else 1)
    if "cand" in sys.argv:
        rows = []
        for k, g in (("A", "c26"), ("A", "c21"), ("A", "c15"), ("B", "c26")):
            p = bake(k, g)
            rows.append((p, f"H反転 案{k}\n{WORDS[k]['giant']}\n{GNAME[g]}"))
        compare(rows, "cmp32_hinv1.png")
        print(OUT / "cmp32_hinv1.png")
    if "zooms" in sys.argv:
        # 🆕 11-12 カズヤくん「c26の背景写真をもっと拡大して飛行機が大きく見えるように表示」＝寄せの3段（上の行は A）。
        #    機体の範囲＝元の画素で横 387〜1056・縦 491〜690（川の中央値からの外れ＝`qa_out/ep32_r01/thumb_c26_box.txt`）・中心 (722, 590)。
        #    元は 1289×1243＝寄せるほど引き伸ばしになる（1.5倍で約1.5倍・2.0倍で約2.0倍）。
        #    機体の中心を画面の (640, 370)＝大きな語の帯（y131〜579）のまん中より少し下へ置く（上の行に尾翼をかぶせない）
        W0, H0, PX, PY, X, Y = 1289, 1243, 722, 590, 640, 370
        base = max(T.W / W0, T.H / H0)

        def crop_for(zoom):
            z = base * zoom
            cw, ch = T.W / z, T.H / z
            cx = min(1.0, max(0.0, (PX - X / z) / (W0 - cw)))
            cy = min(1.0, max(0.0, (PY - Y / z) / (H0 - ch)))
            return dict(zoom=zoom, cx=round(cx, 3), cy=round(cy, 3)), round(670 * z / T.W * 100)
        rows = [(OUT / "ep32_Hinv_Ac26.png", "いま 1.15倍\n機体の幅 画面の約6割\n（1回目の版）")]
        for zoom in (1.5, 1.75, 2.0):
            cr, pct = crop_for(zoom)
            tag = f"_z{int(round(zoom * 100))}"
            p = bake("A", "c26", tag=tag, crop=cr)
            rows.append((p, f"寄せ {zoom}倍\n機体の幅 画面の約{pct}%\n（引き伸ばし約{base * zoom:.1f}倍）"))
        compare(rows, "cmp32_zoom.png")
        print(OUT / "cmp32_zoom.png")
