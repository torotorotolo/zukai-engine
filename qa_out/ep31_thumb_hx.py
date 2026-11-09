# -*- coding: utf-8 -*-
"""31本目 ⑥：サムネの H 型の反転版（`qa_out/ep30_thumb_hx.py` の写し・言葉と地だけ替えた）。
記憶 feedback-jiko-thumbnail-rival-format＝H 型は反転だけを作る（10-20）・事件と事故の回は H 反転版を最初の並べに入れる（11-06）。
Vault の hx.py・hx3.py の lay()・hx2()・pieces()・inv_pair()・compare() を読み込んで使う（Vault の道具は書き換えない）。
言葉＝題 A の芯（その朝の訓練の空は、旅客機の道が載っていない地図の上で、幹部が指で示して決めていた）と事故名。
  「死亡」の語なし（犠牲で言い換え＝c105・cc18 の 162人）。🔴 この回の線＝人の名前・判決の記号・「無罪」・報道の写真を出さない。
地（権利＝字を重ねてよい物だけ）：
  f6＝保存機 F-86F（P6・CC0・公園・銀色）／c10＝その操縦席（P10・CC0）／w1＝旅客機の窓と翼の向こうの雲の上（GW1・Pexels）
  ⚠️ P1（事故機 JA8329）・P3 は CC BY-SA＝一覧の決めで「サムネの地にしない」
案は版ごとに名前を分ける（同じ名前へ焼き直さない）。

    python -P qa_out/ep31_thumb_hx.py cand    … A・B を地の候補で並べる（640／210／168px）・字の中と外・塊の検査
    python -P qa_out/ep31_thumb_hx.py gap A   … 上下の行と大きな語の縁のすき間（6px 以上）
"""
import sys
from pathlib import Path

RES = Path(r"C:\Users\konar\Documents\Obsidian Vault\Resources\事故検証-サムネ海外競合5ch-20261012")
sys.path.insert(0, str(RES))
import hx  # noqa: E402
import hx3  # noqa: E402
from hx import T, WHT, YEL, RED, txt, lay, bake2, compare  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent.parent / "out" / "thumb" / "ep31"
T.OUT = OUT
hx3.OUT = OUT

BAND = (128, 580)                                    # 16・24〜30本目と同じ帯
ADJ = (1.20, 1.25, 1.15)                             # 26・28・30本目と同じ（字の外＝vivid_adj＋H_VIVID_ADD）
# 言葉の案。太らせ：画の多い字（雫）は 0・画の少ない字（石）は 16（`pieces` で塊を見る）
WORDS = {
    "A": dict(giant="雫石", bold={"雫": 0, "石": 16},
              top=[("犠牲162人 ", WHT), ("空域は指で決めた", RED)], bottom="全日空機衝突事故の真相"),
    "B": dict(giant="雫石", bold={"雫": 0, "石": 16},
              top=[("訓練の空は", WHT), ("指で決めた", RED)], bottom="全日空機衝突事故の真相"),
    # 🆕 11-09 カズヤくん「サムネ上部の文言を変更してください」「文字縁は今回は赤で決定」＝上の行だけ替えた4案（縁は赤・地は A で並べる）
    #    言葉は台本と判決の範囲（c105・c307・c308＝漠然と手指で指し示して／J11L の記載のない地図・c505＝約8,500m・cc18＝162人）。
    #    「指1本」「なぞって」は資料に無い＝使わない。「死亡」は使わない（犠牲・生存者なし）
    "C1": dict(giant="雫石", bold={"雫": 0, "石": 16},
               top=[("犠牲162人 ", WHT), ("指で決めた空域", RED)], bottom="全日空機衝突事故の真相"),
    "C2": dict(giant="雫石", bold={"雫": 0, "石": 16},
               top=[("道の載らない地図で", WHT), ("空域を決めた", RED)], bottom="全日空機衝突事故の真相"),
    "C3": dict(giant="雫石", bold={"雫": 0, "石": 16},
               top=[("乗員乗客162人 ", WHT), ("生存者なし", RED)], bottom="全日空機衝突事故の真相"),
    "C5": dict(giant="雫石", bold={"雫": 0, "石": 16},
               top=[("高度8500mで", WHT), ("自衛隊機と接触", RED)], bottom="全日空機衝突事故の真相"),
}
TOPNOTE = {"C1": "犠牲の数＋芯", "C2": "題Aの芯（地図）", "C3": "22本目の型", "C5": "何が起きたか"}
# 地と切り出し（thumb_jiko.photo の zoom・cx・cy）
GROUNDS = {
    "f6": ("ep31/src/eizou/P6.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "c10": ("ep31/src/eizou/P10.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "w1": ("ep31/stock/gw1.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    # 🆕 11-09 カズヤくん「生成AIの地を作る」→「AとBの2枚」＝`tools/gen_thumb_ai.py szk_a|szk_b`（gpt-image-2.5-flare high・各 約$0.2）
    "ga": ("ep31/ai/ep31_szk_a.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "gb": ("ep31/ai/ep31_szk_b.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    # 🆕 11-09 カズヤくん「当時の写真の質感を再現するように、白黒で作成」「色だけでなく質感も」＝`qa_out/ep31_thumb_bw.py`
    #    （地 A を決めの 1.15倍で先に切り出し済み＝ここは zoom 1.0）
    "bw1": ("ep31/ai/ep31_szk_a_bw1.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "bw2": ("ep31/ai/ep31_szk_a_bw2.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    # 🆕 11-09「生成AIで作り直し。構成も再考」→「案① 下から見上げる」「案② 機首から迫る」＝`gen_thumb_ai.py szk_c|szk_d`（白黒・1971年の報道写真の質感）
    "gc": ("ep31/ai/ep31_szk_c.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "gd": ("ep31/ai/ep31_szk_d.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    # 🆕 11-09「案①をもっと荒い質感に編集」＝`qa_out/ep31_thumb_bw.py c`（r1 やや荒い・r2 荒い・r3 かなり荒い）
    "cr1": ("ep31/ai/ep31_szk_c_r1.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "cr2": ("ep31/ai/ep31_szk_c_r2.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "cr3": ("ep31/ai/ep31_szk_c_r3.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "bw3": ("ep31/ai/ep31_szk_a_bw3.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
    "bw4": ("ep31/ai/ep31_szk_a_bw4.jpg", dict(zoom=1.00, cx=0.50, cy=0.50)),
}
GNAME = {"f6": "保存機 F-86F（CC0）", "c10": "F-86F の操縦席（CC0）", "w1": "旅客機の窓の外（Pexels）",
         "ga": "生成 A（横から）", "gb": "生成 B（斜め上から）",
         "bw1": "A 1.15倍 白黒・控えめ", "bw2": "A 1.15倍 白黒・強め",
         "bw3": "A 1.15倍 白黒・自然な写真", "bw4": "A 1.15倍 白黒・新聞の写真寄り",
         "gc": "生成 案①（下から見上げる・白黒）", "gd": "生成 案②（機首から迫る・白黒）",
         "cr1": "案① r1 やや荒い", "cr2": "案① r2 荒い", "cr3": "案① r3 かなり荒い"}


def glyphs(k):
    w = WORDS[k]
    return lay(w["giant"], BAND[0], BAND[1], gap=4, bold=w["bold"])


def extra(k):
    w = WORDS[k]
    tfs = hx3.top_fs("".join(s for s, _ in w["top"]))
    return [txt(w["top"], 40, 104, tfs, WHT), txt(w["bottom"], 40, 692, 112, YEL, sw=16)], tfs


# 🆕 11-09 カズヤくん「H反転型の中心部の文字縁は、赤以外にも青版も作成して。他にもおすすめ色があればお願い」
#    縁の色は Vault の hx.py の `RED`（hx2 の中で縁に使う）＝Vault は書き換えず、焼く間だけ hx.RED を差し替える。
#    字の中と外の測り（inside_mask）は赤い縁の絵（rim_only）から取る＝形は同じ・色だけ違う
RIMS = {"r": None, "b": "#1e64ff", "w": "#ffffff", "y": "#fbfb0e", "o": "#ff8c00"}
RIMNAME = {"r": "赤（いま）", "b": "青", "w": "白", "y": "黄（下の行と同じ）", "o": "オレンジ（青の補色）"}


def _lab(a):
    """sRGB（0〜255）→ CIELAB（D65）。縁の色と字の外の色の差 ΔE76 を測るため"""
    import numpy as np
    c = np.asarray(a, dtype=float) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def rim_contrast(name, inside, red):
    """縁の画素の色 と、縁のすぐ外（8px の輪）・すぐ内（6px の輪）の画素の色の差 ΔE76＝中央値と下位10%（溶ける所）"""
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    a = np.asarray(Image.open(OUT / f"{name}.png").convert("RGB")).astype(float)
    filled = inside | red
    out_ring = ndimage.binary_dilation(filled, iterations=8) & ~filled
    in_ring = inside & ndimage.binary_dilation(red, iterations=6)
    rim_lab = _lab(a[red].mean(0))
    res = []
    for ring in (out_ring, in_ring):
        de = np.sqrt(((_lab(a[ring]) - rim_lab) ** 2).sum(-1))
        res.append((float(np.median(de)), float(np.percentile(de, 10))))
    return res


def bake(k, g, bright=1.15, tag="", rim=None, crop=None):
    src, crop0 = GROUNDS[g]
    crop = crop or crop0
    gl, fs, sx = glyphs(k)
    ex, tfs = extra(k)
    fit = f"_fit_ep31_{k}"
    hx3.rim_only(fit, gl)
    inside, red = hx3.inside_mask(fit)
    d, c = hx3.inv_pair(src, ADJ, crop, out_bright=bright)
    name = f"ep31_Hinv_{k}{g}{tag}"
    old = hx.RED
    try:
        if rim:
            hx.RED = rim
        bake2(name, hx.hx2(d, c, gl, ex))
    finally:
        hx.RED = old
    i, o, df = hx3.lum(name, inside, red)
    bad = hx3.pieces(gl)
    (om, o10), (im_, i10) = rim_contrast(name, inside, red)
    print(f"  {name}: 大きさ {fs:.0f}・長体 {sx:.3f}・上の行 {tfs}・字の中 {i:.0f}・字の外 {o:.0f}・差 {df:+.0f}・塊 {''.join(bad) if bad else '0件'}"
          f"・縁と外 ΔE 中央 {om:.0f}／下位10% {o10:.0f}・縁と中 ΔE 中央 {im_:.0f}／下位10% {i10:.0f}")
    return OUT / f"{name}.png"


# 🆕 11-09 カズヤくん「背景の写真の存在感が薄いので、もっと大きく表示。もしくはもっとインパクトのある画像を生成」
#    → 機体（`qa_out/ep31_thumb_plane.py` の透明つき PNG）を大きな字の手前・上下の行の奥に重ねる（17本目 `thumb_jiko.ep17_h_over` と同じ順）。
#    重ねの色は字の外と同じ調整（photo と同じ順＝コントラスト → 彩度 → 明るさ）・切り出しも地と同じ式（ずれない）
PLANE = {"ga": "ep31/ai/ep31_szk_a_plane.png", "gb": "ep31/ai/ep31_szk_b_plane.png"}


def plane_uri(g, crop, bright=1.15):
    import base64
    import io
    from PIL import Image, ImageEnhance
    im = Image.open(Path(hx.T.HERE) / "ref" / PLANE[g]).convert("RGBA")
    z = max(T.W / im.width, T.H / im.height) * crop.get("zoom", 1.0)
    cw, ch = min(im.width, T.W / z), min(im.height, T.H / z)
    l, t = (im.width - cw) * crop.get("cx", 0.5), (im.height - ch) * crop.get("cy", 0.5)
    im = im.crop((round(l), round(t), round(l + cw), round(t + ch)))
    im = im.convert("RGBa").resize((T.W, T.H), Image.LANCZOS).convert("RGBA")     # 縁のにじみを出さない（前乗算で縮める）
    a = im.getchannel("A")
    rgb = im.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(ADJ[0])
    rgb = ImageEnhance.Color(rgb).enhance(ADJ[1])
    rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    rgb.putalpha(a)
    buf = io.BytesIO()
    rgb.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def bake_over(k, g, bright=1.15, tag="", crop=None):
    src, crop0 = GROUNDS[g]
    crop = crop or crop0
    gl, fs, sx = glyphs(k)
    ex, tfs = extra(k)
    d, c = hx3.inv_pair(src, ADJ, crop, out_bright=bright)
    over = f'<image href="{plane_uri(g, crop, bright)}" x="0" y="0" width="{T.W}" height="{T.H}"/>'
    name = f"ep31_Hinv_{k}{g}_over{tag}"
    bake2(name, hx.hx2(d, c, gl, []) + over + "".join(ex))
    print(f"  {name}: 大きさ {fs:.0f}・上の行 {tfs}・機体を字の手前に（切り出し {crop}）")
    return OUT / f"{name}.png"


def gap(k):
    # Vault gap.py と同じ式（上下の行〈黒フチこみ〉と大きな語の赤い縁のすき間を列ごとに）
    import numpy as np
    from PIL import Image
    gl, _, _ = glyphs(k)
    ex, _ = extra(k)
    bake2("_txt_ep31", f'<rect width="{T.W}" height="{T.H}" fill="#fff"/>' + "".join(ex))
    t = np.asarray(Image.open(OUT / "_txt_ep31.png").convert("L")) < 250
    hx3.rim_only(f"_fit_ep31_{k}", gl)
    a = np.asarray(Image.open(OUT / f"_fit_ep31_{k}.png").convert("RGB")).astype(int)
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
        for k, g in (("A", "f6"), ("A", "c10"), ("A", "w1"), ("B", "f6")):
            p = bake(k, g)
            rows.append((p, f"H反転 案{k}\n{WORDS[k]['giant']}\n{GNAME[g]}"))
        compare(rows, "cmp31_hinv1.png")
        print(OUT / "cmp31_hinv1.png")
    if "cand2" in sys.argv:
        # 生の地2枚（字を重ねる前＝字・印・形の崩れを見る）と、案B の H 反転版2枚
        rows = [(Path(hx.T.HERE) / "ref" / GROUNDS[g][0], f"生の地\n{GNAME[g]}") for g in ("ga", "gb")]
        for k, g in (("B", "ga"), ("B", "gb")):
            p = bake(k, g)
            rows.append((p, f"H反転 案{k}\n{WORDS[k]['giant']}\n{GNAME[g]}"))
        compare(rows, "cmp31_hinv2.png")
        print(OUT / "cmp31_hinv2.png")
    if "tops" in sys.argv:
        # 上の行の4案（縁は赤＝決め・地は A）
        rows = []
        for k in ("C1", "C2", "C3", "C5"):
            p = bake(k, "ga")
            rows.append((p, f"上の行 {k}\n{TOPNOTE[k]}\n{GNAME['ga']}"))
        compare(rows, "cmp31_top_ga.png")
        print(OUT / "cmp31_top_ga.png")
    if "rough" in sys.argv:
        # 案①の荒さ3段（H 反転・縁は赤・上の行は C3）＋生の地 r2（粒の見え方）
        rows = [(Path(hx.T.HERE) / "ref" / GROUNDS["cr2"][0], f"生の地\n{GNAME['cr2']}")]
        for g in ("cr1", "cr2", "cr3"):
            rows.append((bake("C3", g), f"H反転・縁は赤\n{GNAME[g]}"))
        compare(rows, "cmp31_rough.png")
        print(OUT / "cmp31_rough.png")
    if "gen2" in sys.argv:
        rows = [(Path(hx.T.HERE) / "ref" / GROUNDS[g][0], f"生の地\n{GNAME[g]}") for g in ("gc", "gd")]
        for g in ("gc", "gd"):
            rows.append((bake("C3", g), f"H反転・縁は赤\n{GNAME[g]}"))
        compare(rows, "cmp31_gen2.png")
        print(OUT / "cmp31_gen2.png")
    if "bw" in sys.argv:
        # 白黒の質感の2段（生の地と、H 反転版）。縁は赤・上の行は C3・機体は字の後ろ
        gs = ("bw3", "bw4") if "2" in sys.argv else ("bw1", "bw2")
        rows = [(Path(hx.T.HERE) / "ref" / GROUNDS[g][0], f"生の地\n{GNAME[g]}") for g in gs]
        for g in gs:
            rows.append((bake("C3", g), f"H反転・縁は赤\n{GNAME[g]}"))
        nm = "cmp31_bw2.png" if "2" in sys.argv else "cmp31_bw.png"
        compare(rows, nm)
        print(OUT / nm)
    if "zooms" in sys.argv:
        # 🆕 11-09 カズヤくん「サムネの飛行機は文字の後ろ。写真をもう少し大きく」＝重ねをやめ、地 A を寄せる（縁は赤・上の行は C3）。
        #    A の2機は横 x90〜1255（1280 のうち）・縦 y123〜411＝1.1倍より寄せるとどこかが切れる → 残すものを変えた4段。
        #    縦は cy=0（上から切る）＝2機が真ん中の帯（字の帯 y136〜579）へ下がる。cx＝左の端 l÷(1280−切る幅)
        def cx_for(z, l):
            return round(l / (T.W - T.W / z), 3)
        ZOOMS = [
            ("z115", dict(zoom=1.15, cx=cx_for(1.15, 152), cy=0.0), "1.15倍・旅客機の機首まで全部（戦闘機の後ろが少し切れる）"),
            ("z130a", dict(zoom=1.30, cx=cx_for(1.30, 200), cy=0.0), "1.30倍・2機とも少しずつ切れる"),
            ("z130b", dict(zoom=1.30, cx=1.0, cy=0.0), "1.30倍・旅客機を全部（戦闘機は外）"),
            ("z145", dict(zoom=1.45, cx=cx_for(1.45, 382), cy=0.0), "1.45倍・旅客機だけを大きく"),
        ]
        rows = []
        for tag, cr, note in ZOOMS:
            p = bake("C3", "ga", tag=f"_{tag}", crop=cr)
            rows.append((p, f"寄せ {tag}\n{note}\n機体は字の後ろ"))
        compare(rows, "cmp31_zoom.png")
        print(OUT / "cmp31_zoom.png")
    if "final" in sys.argv:
        # ✅ 11-09 カズヤくん「文字縁は今回は赤で決定」・上の行＝「C3 乗員乗客162人／生存者なし」・地＝A（横から）
        #    → 「サムネの飛行機は文字の後ろ。写真をもう少し大きく」→ 寄せ4段から「① 1.15倍」（重ねの版 ep31_Hinv_C3ga_over は残した）
        #    → 「サムネの写真変更」「当時の写真の質感を再現するように、白黒で作成」「色だけでなく質感も」→「生成AIで作り直し。構成も再考」
        #    →「案① 下から見上げる」→「案①をもっと荒い質感に編集」→「r2 荒い」＝決め（z115 の版 ep31_Hinv_C3ga_z115 は残した）
        p = bake("C3", "cr2")
        compare([(p, "決め\n縁＝赤・地＝生成 案①（白黒）r2 荒い\n上＝乗員乗客162人／生存者なし")], "cmp31_final.png")
        print(OUT / "cmp31_final.png", f"{p.stat().st_size / 1e6:.2f}MB")
    if "over" in sys.argv:
        # 機体を字の手前に重ねた版（縁は赤＝決め・上の行は C1 で並べる＝言葉は別に選ぶ）＋比べる元（重ねなし）
        rows = [(bake("C1", "ga"), f"重ねなし（いま）\n{GNAME['ga']}")]
        for g in ("ga", "gb"):
            rows.append((bake_over("C1", g), f"機体を字の手前に\n{GNAME[g]}"))
        compare(rows, "cmp31_over.png")
        print(OUT / "cmp31_over.png")
    if "rims" in sys.argv:
        # 縁の色の5版（赤・青・白・黄・オレンジ）を地ごとに1枚の並べへ
        for g in ("ga", "gb"):
            rows = []
            for r, col in RIMS.items():
                p = bake("B", g, tag=f"_rim{r}", rim=col)
                rows.append((p, f"縁＝{RIMNAME[r]}\n{GNAME[g]}"))
            compare(rows, f"cmp31_rim_{g}.png")
            print(OUT / f"cmp31_rim_{g}.png")
