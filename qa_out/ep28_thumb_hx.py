# -*- coding: utf-8 -*-
"""28本目 ⑥：サムネの H 型の反転版（`qa_out/ep26_thumb_hx.py` の写し・言葉と地だけ替えた）。
Vault の hx.py・hx3.py の lay()・hx2()・pieces()・inv_pair()・compare() を読み込んで使う（Vault の道具は書き換えない）。
言葉の案＝台本 §1-2（A 免許証・B 漏えい・C 10万人）。地＝Commons（ロゴ単体は使わない＝ルール §B2-11 ③）。

    python -P qa_out/ep28_thumb_hx.py cand    … A・B・C を CM006 の地で並べる（640／210／168px）・字の中と外・塊の検査
    python -P qa_out/ep28_thumb_hx.py gap A   … 上下の行と大きな語の縁のすき間（6px 以上）
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

BAND = (128, 580)                                    # 16・24・25・26本目と同じ帯
ADJ = (1.20, 1.25, 1.15)                             # 26本目と同じ（字の外＝vivid_adj＋H_VIVID_ADD）
# 言葉の案（台本 §1-2）。太らせ：画の多い字は 0（`pieces` で塊を見る）
WORDS = {
    "A": dict(giant="免許証", bold={"免": 8, "許": 0, "証": 0},
              top=[("退会しても ", WHT), ("7年", RED)], bottom="タイムズカー情報漏洩"),
    "B": dict(giant="漏えい", bold={"漏": 0, "え": 16, "い": 16},
              top=[("会員400万人に ", WHT), ("662万件", RED)], bottom="タイムズカー"),
    "C": dict(giant="10万人", bold={"1": 16, "0": 16, "万": 12, "人": 16},
              top=[("見舞金 ", WHT), ("3000円", RED)], bottom="タイムズカー情報漏洩"),
}
GROUND = "ep28/cm006.jpg"
CROP = dict(zoom=1.00, cx=0.50, cy=0.50)


def glyphs(k):
    w = WORDS[k]
    return lay(w["giant"], BAND[0], BAND[1], gap=4, bold=w["bold"])


def extra(k):
    w = WORDS[k]
    tfs = hx3.top_fs("".join(s for s, _ in w["top"]))
    return [txt(w["top"], 40, 104, tfs, WHT), txt(w["bottom"], 40, 692, 112, YEL, sw=16)], tfs


def bake(k, src=GROUND, crop=CROP, bright=1.15, tag=""):
    gl, fs, sx = glyphs(k)
    ex, tfs = extra(k)
    fit = f"_fit_ep28_{k}"
    hx3.rim_only(fit, gl)
    inside, red = hx3.inside_mask(fit)
    d, c = hx3.inv_pair(src, ADJ, crop, out_bright=bright)
    name = f"ep28_Hinv_{k}{tag}"
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
    bake2("_txt_ep28", f'<rect width="{T.W}" height="{T.H}" fill="#fff"/>' + "".join(ex))
    t = np.asarray(Image.open(OUT / "_txt_ep28.png").convert("L")) < 250
    hx3.rim_only(f"_fit_ep28_{k}", gl)
    a = np.asarray(Image.open(OUT / f"_fit_ep28_{k}.png").convert("RGB")).astype(int)
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
        for k in "ABC":
            p = bake(k)
            rows.append((p, f"案{k}\n{WORDS[k]['giant']}\nCM006 寄せなし"))
        compare(rows, "cmp28_a.png")
        print(OUT / "cmp28_a.png")
