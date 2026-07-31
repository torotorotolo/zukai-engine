# -*- coding: utf-8 -*-
"""★写真を地に敷くときの「暗幕の濃さ」を**測って**決める（2026-07-31 追加）。

■ なぜ要るか
  試写の指摘④「時刻をグラフで出すだけのカットが多く、競合と比べて退屈」への答えとして、
  写真を地に敷いてその上に図解を重ねられるようにした（`build_jiko.scene()`）。
  ところが図解は**細い線と小さい文字**なので、写真がそのまま出ていると読めない。

  ⚠️ 濃さを目分量で置いてはいけない。
     「余白を色で判定して失敗した」前科があり、**測れるものは測る**のがこの工程の作法。

■ 測り方
  暗幕を α で敷いたあとの地は、画素ごとに

      地 = α × J.BG + (1 − α) × デュオトーンした写真

  図の線はその上に不透明で乗るので、**線の色は変わらず、地だけが場所ごとに変わる**。
  つまり読めるかどうかは「線の色 ⇄ その場所の地」の**コントラスト比**で決まる。

  そこで α を振りながら、図で使う色ごとに WCAG のコントラスト比を全画素で出し、
  **下位1%（いちばん条件の悪い場所）** を見る。ここが基準を割ると、
  写真の明るい部分に図が重なった瞬間に読めなくなる。

  基準 … 4.5（WCAG AA の本文相当）。細い技術線なので本文と同じ厳しさで見る。
  ⚠️ ただしこれは**必要条件**であって十分条件ではない。
     最後は焼いて拡大目視する（カズヤくんの指示どおり）。ここは候補を2〜3個に絞る道具。

■ 使い方
    python tools/check_veil.py                       … 全写真 × α を一覧
    python tools/check_veil.py --photo=titan_rov_aft.jpg
    python tools/check_veil.py --alpha=0.72          … その濃さだけ詳しく
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image

import jiko_style as J

HERE = Path(__file__).parent.parent
W, H = 1920, 1080
TARGET = 4.5              # WCAG AA（本文）。細い線なのでここまで求める
PCT = 1.0                 # 下位1%の画素で判定する（いちばん条件の悪い場所）

# 図で**情報を運ぶ**色だけを見る。
# 🔴 最初は LINE_DIM（沈める色）と GRID（方眼）も入れて「絶対値 4.5 以上」で判定したが、
#    **どの濃さでも 1.00 になった**。地の明るさは BG から写真まで連続に変わるので、
#    中間の明るさを持つ GRID とは**必ずどこかで一致する**（＝コントラスト1.00）。
#    さらに ALERT は素の地の上ですら 4.2 しかない。**絶対値の基準そのものが誤りだった。**
# → 測るのは「**素の地に比べて、どれだけ読みにくくなるか**」。
#    素の地（J.BG）での読みやすさは、検品9巡が通した実績値だから基準にできる。
INKS = [("INK_W", J.INK_W), ("LINE", J.LINE), ("AMBER", J.AMBER), ("ALERT", J.ALERT)]
# 🔴 最初 0.70 に置いたら、必要な濃さが **0.90** と出た。ところがその濃さでは
#    写真の見えが L*7 まで落ちて**平らな板**になり、敷く意味が消える。
#    両方を並べて測って分かった、実際に使える帯はここ：
#      α=0.72 … 読みやすさ 0.28／写真 L*21   → 図が読めない
#      α=0.80 … 読みやすさ 0.45／写真 L*17   → ぎりぎり
#      α=0.84 … 読みやすさ 0.55／写真 L*14   → ★候補
#      α=0.88 … 読みやすさ 0.66／写真 L*10   → ★候補（図優先）
#      α=0.92 … 読みやすさ 0.77／写真 L*7    → 写真が消える
#    → 基準は 0.50 に置き、**0.80〜0.88 を焼いて目視で決める**（カズヤくん判断）。
KEEP = 0.50
ALPHAS = [0.55, 0.62, 0.68, 0.72, 0.76, 0.80, 0.84, 0.88, 0.92]


def rgb(hexs):
    return np.array([int(hexs[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float64)


# 🔴 sRGB→リニアの `** 2.4` を全画素で毎回やると**終わらない**（実際に5分で返らなかった）。
#    入力は 0〜255 の256通りしか無いので、**表を1回作って引く**。
_S = np.arange(256) / 255.0
LIN = np.where(_S <= 0.04045, _S / 12.92, ((_S + 0.055) / 1.055) ** 2.4)
COEF = np.array([0.2126, 0.7152, 0.0722])


def rel_lum(c):
    """WCAG の相対輝度。c は 0〜255 の配列（末尾の軸が RGB）。"""
    idx = np.clip(np.rint(c), 0, 255).astype(np.uint8)
    return (LIN[idx] * COEF).sum(axis=-1)


def duotone_np(im):
    """build_jiko.duotone と同じ変換を numpy で。地は BG2、明部は #e6eef2。"""
    g = np.asarray(im.convert("L"), dtype=np.float64) / 255.0
    d, l = rgb(J.BG2), rgb("#e6eef2")
    return d + (l - d) * g[..., None]


def load(name, w=640):
    """測るだけなので縮めて読む（4GBのPCで全画素を持たない）。"""
    with Image.open(HERE / "ref" / name) as im:
        im = im.convert("RGB")
        z = max(w / im.width, w * H / W / im.height)
        cw, ch = min(im.width, w / z), min(im.height, w * H / W / z)
        l, t = (im.width - cw) / 2, (im.height - ch) / 2
        im = im.crop((round(l), round(t), round(l + cw), round(t + ch)))
        return im.resize((w, round(w * H / W)), Image.LANCZOS)


def bg_lum(photo_rgb, alpha):
    """暗幕 alpha を敷いたあとの地の輝度（画素ごと）。**α ごとに1回だけ計算する。**"""
    return rel_lum(alpha * rgb(J.BG) + (1 - alpha) * photo_rgb)


def contrast_from(bl, ink):
    """地の輝度 bl に対する ink のコントラスト比。四則演算だけなので速い。"""
    a = rel_lum(rgb(ink)[None, :])[0]
    hi, lo = np.maximum(a, bl), np.minimum(a, bl)
    return (hi + 0.05) / (lo + 0.05)


def contrast(photo_rgb, alpha, ink):
    return contrast_from(bg_lum(photo_rgb, alpha), ink)


PLAIN = rel_lum(rgb(J.BG)[None, :])[0]        # 素の地（写真を敷いていないときの明るさ）


def keep_ratio(photo_rgb, alpha, bl=None):
    """素の地に比べて、コントラストの「超過分」が何割残るか（いちばん悪い色）。

    コントラスト比は最良でも 1.0（＝まったく読めない）なので、
    **1.0 からの超過分**（C − 1）で比べる。0.70 なら「7割は残っている」。
    """
    bl = bg_lum(photo_rgb, alpha) if bl is None else bl
    out = []
    for _, c in INKS:
        c0 = contrast_from(np.array([PLAIN]), c)[0]
        c1 = np.percentile(contrast_from(bl, c), PCT)
        out.append((c1 - 1.0) / max(c0 - 1.0, 1e-9))
    return min(out)


def lstar(y):
    """CIELAB の明度 L*（0〜100）。**暗いところの差を人の目のとおりに拡大する。**

    🔴 最初は線形輝度の差で「写真の見え」を測って「0.02未満なら平らな板」と書いたが、
       **これは目の性質を無視していた。** 暗部では小さな輝度差でも見える。
       Y=0.005→L*3.8 ／ Y=0.020→L*15.5 ＝ **輝度差0.015 が L* で12も開く。**
       L* は 1 がだいたい人の弁別限なので、12 は「はっきり見える」。
    """
    t = np.asarray(y, dtype=np.float64)
    f = np.where(t > 0.008856, np.cbrt(t), (903.3 * t + 16) / 116)
    return np.where(t > 0.008856, 116 * f - 16, 903.3 * t)


def photo_span(photo_rgb, alpha):
    """暗幕越しに写真がどれだけ「見えて」いるか。**L\\* の 1%〜99% の開き。**

    ⚠️ 暗幕を濃くすれば図は読めるが、濃くしすぎると写真が消えて敷く意味が無くなる。
       目安 … 8 未満＝ほぼ平らな板 ／ 15 前後＝地紋として分かる ／ 25 以上＝写真として読める
    """
    lo, hi = np.percentile(lstar(bg_lum(photo_rgb, alpha)), [1, 99])
    return float(hi - lo)


def need(photo_rgb, lo=0.30, hi=0.98):
    """基準（KEEP）を満たすいちばん薄い暗幕。**二分探索。**"""
    if keep_ratio(photo_rgb, hi) < KEEP:
        return None
    for _ in range(12):
        mid = (lo + hi) / 2
        if keep_ratio(photo_rgb, mid) >= KEEP:
            hi = mid
        else:
            lo = mid
    return round(float(np.ceil(hi * 100) / 100), 2)


def main():
    only = next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--photo=")), None)
    one = next((float(a.split("=")[1]) for a in sys.argv[1:] if a.startswith("--alpha=")), None)
    import scene_jiko as S
    names = sorted(S.PHOTO_CREDIT) if not only else [only]

    if one is not None:
        print(f"暗幕 {one} での色ごとの「読みやすさの残り」"
              f"（素の地＝1.00・下位{PCT:.0f}%の画素で判定）")
        print(f"{'写真':<28}" + "".join(f"{n:>9}" for n, _ in INKS) + "   写真の見え")
        for n in names:
            p = duotone_np(load(n))
            bl = bg_lum(p, one)
            row = []
            for _, c in INKS:
                c0 = contrast_from(np.array([PLAIN]), c)[0]
                row.append((np.percentile(contrast_from(bl, c), PCT) - 1) / (c0 - 1))
            mark = "  ✓" if min(row) >= KEEP else "  🔴"
            print(f"{n:<28}" + "".join(f"{v:9.2f}" for v in row)
                  + f"{photo_span(p, one):11.3f}{mark}")
        return 0

    print("暗幕の濃さ × 図の読みやすさ（素の地を 1.00 とした残り）")
    print(f"基準 {KEEP:.2f}＝素の地の7割。✓ が付いた中でいちばん薄いのが最小値。")
    print("下の【写真の見え】は暗幕越しの明暗の開き（L*）。"
          "8未満＝平らな板／15前後＝地紋として分かる／25以上＝写真として読める。\n")
    print(f"{'写真':<26}" + "".join(f"{a:>7.2f}" for a in ALPHAS) + "  必要な濃さ")
    worst_need = 0.0
    for n in names:
        p = duotone_np(load(n))
        vals = [keep_ratio(p, a) for a in ALPHAS]
        nd = need(p)
        worst_need = max(worst_need, nd or 1.0)
        cells = "".join(("✓" if v >= KEEP else " ") + f"{v:6.2f}" for v in vals)
        print(f"{n:<26}{cells}  {nd if nd else '0.98超'}")
    print(f"\n★どの写真でも基準を満たす濃さ = **{worst_need:.2f}**")
    print(f"   scene_jiko.VEIL の既定値は {S.VEIL}"
          f"（{'✓ 足りている' if S.VEIL >= worst_need else '🔴 薄すぎる'}）")
    print(f"\n{'写真':<26}" + "".join(f"{a:>7.2f}" for a in ALPHAS) + "  ← 写真の見え（明暗の開き）")
    for n in names:
        p = duotone_np(load(n))
        print(f"{n:<26}" + "".join(f"{photo_span(p, a):7.3f}" for a in ALPHAS))
    print("\n⚠️ これは必要条件。**最後は焼いて拡大目視で決める**"
          "（カズヤくん指示：暗幕の濃さは焼いて目視で決めること）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
