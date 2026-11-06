# -*- coding: utf-8 -*-
"""30本目 ⑥：サムネの H 型の反転版（`qa_out/ep28_thumb_hx.py` の写し・言葉と地だけ替えた）。
11-06 カズヤくん「サムネはH反転型を作成して。また、他の案でも作って」。
Vault の hx.py・hx3.py の lay()・hx2()・pieces()・inv_pair()・compare() を読み込んで使う（Vault の道具は書き換えない）。
言葉＝題 A の芯（前の年に同じ毒）と事件名（台本 §1-1・c105）。「死亡」の語なし（犠牲で言い換え＝c105 の公安調査庁の数 14人）。
地＝陸上自衛隊の除染の写真（アーカイブ・PDL1.0 の読み＝サムネの地も可）＝#65（防護マスクと背負いのタンク）・#66（電車の中）。顔なし（防護マスク）。
案は版ごとに名前を分ける（同じ名前へ焼き直さない）。

    python -P qa_out/ep30_thumb_hx.py cand    … A・B を #65・#66 で並べる（640／210／168px）・字の中と外・塊の検査
    python -P qa_out/ep30_thumb_hx.py gap A   … 上下の行と大きな語の縁のすき間（6px 以上）
"""
import sys
from pathlib import Path

RES = Path(r"C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証-サムネ海外競合5ch-20261012")
sys.path.insert(0, str(RES))
import hx  # noqa: E402
import hx3  # noqa: E402
from hx import T, WHT, YEL, RED, txt, lay, bake2, compare  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent.parent / "out" / "thumb" / "ep30"
T.OUT = OUT
hx3.OUT = OUT

BAND = (128, 580)                                    # 16・24〜28本目と同じ帯
ADJ = (1.20, 1.25, 1.15)                             # 26・28本目と同じ（字の外＝vivid_adj＋H_VIVID_ADD）
# 言葉の案。太らせ：画の多い字は 0・点のある「ン」は控えめ（`pieces` で塊を見る）
WORDS = {
    "A": dict(giant="地下鉄サリン", bold={"地": 8, "下": 16, "鉄": 0, "サ": 16, "リ": 16, "ン": 8},
              top=[("犠牲14人 ", WHT), ("前の年にも同じ毒", RED)], bottom="事件の真相"),
    "B": dict(giant="サリン", bold={"サ": 16, "リ": 16, "ン": 8},
              top=[("前の年にも ", WHT), ("同じ毒", RED)], bottom="地下鉄サリン事件"),
    # 🔧 1回目の塊の検査＝「地」の太らせ 8 で中のすき間がつぶれた（塊 2 → 窓 1）＝0 にした版（名前は A…b）
    "Ab": dict(giant="地下鉄サリン", bold={"地": 0, "下": 16, "鉄": 0, "サ": 16, "リ": 16, "ン": 8},
               top=[("犠牲14人 ", WHT), ("前の年にも同じ毒", RED)], bottom="事件の真相"),
    # ✅ 11-06 カズヤくん「H反転A65で決まり。上の行は「前の年にも同じ毒」に変更」＝Ab から「犠牲14人」を外しただけ（赤の句はそのまま）
    "Ac": dict(giant="地下鉄サリン", bold={"地": 0, "下": 16, "鉄": 0, "サ": 16, "リ": 16, "ン": 8},
               top=[("前の年にも同じ毒", RED)], bottom="事件の真相"),
    # ✅ 11-06 カズヤくん「サムネ上部の赤字は「同じ毒」だけ」＝「前の年にも」を白に（上の行の決まり＝要の語だけ赤）
    "Ad": dict(giant="地下鉄サリン", bold={"地": 0, "下": 16, "鉄": 0, "サ": 16, "リ": 16, "ン": 8},
               top=[("前の年にも", WHT), ("同じ毒", RED)], bottom="事件の真相"),
}
# 地と切り出し（thumb_jiko.photo の zoom・cx・cy）＝隊員の防護マスクが字のすき間に出る位置を探す
GROUNDS = {
    "65": ("ep30/p65.jpg", dict(zoom=1.00, cx=0.50, cy=0.42)),
    "66": ("ep30/p66.jpg", dict(zoom=1.00, cx=0.50, cy=0.52)),
}


def glyphs(k):
    w = WORDS[k]
    return lay(w["giant"], BAND[0], BAND[1], gap=4, bold=w["bold"])


def extra(k):
    w = WORDS[k]
    tfs = hx3.top_fs("".join(s for s, _ in w["top"]))
    return [txt(w["top"], 40, 104, tfs, WHT), txt(w["bottom"], 40, 692, 112, YEL, sw=16)], tfs


def bake(k, g, bright=1.15, tag=""):
    src, crop = GROUNDS[g]
    gl, fs, sx = glyphs(k)
    ex, tfs = extra(k)
    fit = f"_fit_ep30_{k}"
    hx3.rim_only(fit, gl)
    inside, red = hx3.inside_mask(fit)
    d, c = hx3.inv_pair(src, ADJ, crop, out_bright=bright)
    name = f"ep30_Hinv_{k}{g}{tag}"
    bake2(name, hx.hx2(d, c, gl, ex))
    i, o, df = hx3.lum(name, inside, red)
    bad = hx3.pieces(gl)
    print(f"  {name}: 大きさ {fs:.0f}・長体 {sx:.3f}・上の行 {tfs}・字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}・塊 {''.join(bad) if bad else '0件'}")
    return OUT / f"{name}.png"


def gap(k):
    # Vault gap.py と同じ式（上下の行〈黒フチこみ〉と大きな語の赤い縁のすき間を列ごとに）
    import numpy as np
    from PIL import Image
    gl, _, _ = glyphs(k)
    ex, _ = extra(k)
    bake2("_txt_ep30", f'<rect width="{T.W}" height="{T.H}" fill="#fff"/>' + "".join(ex))
    t = np.asarray(Image.open(OUT / "_txt_ep30.png").convert("L")) < 250
    hx3.rim_only(f"_fit_ep30_{k}", gl)
    a = np.asarray(Image.open(OUT / f"_fit_ep30_{k}.png").convert("RGB")).astype(int)
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
        for k, g in (("A", "65"), ("B", "65"), ("A", "66"), ("B", "66")):
            p = bake(k, g)
            rows.append((p, f"H反転 案{k}\n{WORDS[k]['giant']}\n陸自 #{g}"))
        compare(rows, "cmp30_hinv1.png")
        print(OUT / "cmp30_hinv1.png")
    if "cand2" in sys.argv:
        for k, g in (("Ab", "65"), ("Ab", "66")):
            bake(k, g)
    if "final" in sys.argv:
        p = bake("Ac", "65")
        rows = [(p, "H反転 A65（決め）\n地下鉄サリン\n上＝前の年にも同じ毒")]
        compare(rows, "cmp30_hinv_final.png")
        print(OUT / "cmp30_hinv_final.png")
    if "final2" in sys.argv:
        p = bake("Ad", "65")
        rows = [(p, "H反転 A65（決め）\n地下鉄サリン\n上＝赤は同じ毒だけ")]
        compare(rows, "cmp30_hinv_final2.png")
        print(OUT / "cmp30_hinv_final2.png")
