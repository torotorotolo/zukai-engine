# -*- coding: utf-8 -*-
"""27本目 ⑥：説明カットの地の写真（dim）の 8:1 を**本編の画素**でも測る（⑤b-4 §5「Modal の本編でも check_ground を回す」）。

なぜ：`tools/check_ground.py` は「焼いた層のα」と「写真を本番の式（build_jiko.ground_dim）で暗くした地」から比を出す＝設計の絵を測る。
     Modal の本編（full）の手順には check_ground が無い＝本編の地が設計の式どおりに暗いかは測っていなかった。
測り方：check_ground と**同じ関数**（ring_of・worst・lum）で、地だけを本編のコマ（`qa_out/ep27_r01_cutframes.py` が抜いた cut_<cid>.jpg＝
     検品の静止画といちばん合う瞬間＝カットの終わり）に差し替える。層は手元の焼き（qa_all の ground が使ったもの）。
⚠️ 本編は H.264（と抜いたコマの JPEG）＝白い字の縁のにじみが帯（字から10px）に乗り、比は設計より低めに出る＝設計の比と並べて、差が大きいカットだけを見る。
⚠️ 層は手元（Windows の Chrome）の焼き・本編は Modal（Linux の Chrome）の焼き＝右上の出典の行（地の写真の出どころ・y≈173〜200）の字の位置が
   数px ずれ、手元の層の帯に本編の**字そのもの**が入って 1.9:1 と出た（10-30 の1回目＝9カット）＝`--cred` で出典の行の帯を除く。
   `--halo=N`＝字の縁から N px（にじみ）を帯から除く（帯は N〜10px になる）。

    python -P qa_out/ep27_r01_ground.py [--frames=out/jiko/ep27_r01_frames] [--cred] [--halo=3]   → qa_out/ep27_r01/ground[_cred][_haloN].tsv と要約
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import check_ground as G  # noqa: E402


def arg(k, d):
    for a in sys.argv[1:]:
        if a.startswith(f"--{k}="):
            return a.split("=", 1)[1]
    return d


def main():
    frames = HERE / arg("frames", "out/jiko/ep27_r01_frames")
    cred = "--cred" in sys.argv
    halo = int(arg("halo", "0"))
    S, B, idx, _ = G._load()
    cy = S.CRED_BACK_Y                                  # 地の写真の出典の行の基線（右上）
    cids = G._dim_cuts(S, idx)
    rows, bad = [], []
    for c in cids:
        fp = frames / f"cut_{c}.jpg"
        try:
            ph, a, k = G._cut_inputs(c, idx, B, S)
        except Exception as e:                       # noqa: BLE001
            bad.append(f"{c}: 層か写真が読めない（{e}）")
            continue
        if not fp.exists():
            bad.append(f"{c}: 本編のコマが無い {fp.name}")
            continue
        ring = G.ring_of(a)
        if halo:
            ring &= ~G.dilate(a >= G.INK_A, halo)
        if cred:
            ring[cy - 36:cy + 10, :] = False
        rd, at_d, n_d, med_d = G.worst(G.lum(G.dimmed(ph, k)), ring)
        fr = np.asarray(Image.open(fp).convert("RGB")).astype(np.float64)
        rf, at_f, n_f, med_f = G.worst(G.lum(fr), ring)
        rows.append((c, k, rd, rf, med_d, med_f, at_f, n_f))
    out = HERE / "qa_out" / "ep27_r01" / f"ground{'_cred' if cred else ''}{f'_halo{halo}' if halo else ''}.tsv"
    with out.open("w", encoding="utf-8") as f:
        f.write("cut\tdim\t設計の最悪\t本編の最悪\t設計の中央値\t本編の中央値\t本編の最悪の升\t升の数\n")
        for c, k, rd, rf, md, mf, at, n in rows:
            f.write(f"{c}\t{k}\t{rd:.2f}\t{rf:.2f}\t{md:.2f}\t{mf:.2f}\t{at}\t{n}\n")
    under = [r for r in rows if r[3] < G.TARGET]
    print(f"地の写真のカット {len(cids)}・測れた {len(rows)}・測れない {len(bad)}")
    for b in bad:
        print("  🔴", b)
    if rows:
        d = [r[3] - r[2] for r in rows]
        print(f"最悪の升の比：設計 {min(r[2] for r in rows):.2f}〜{max(r[2] for r in rows):.2f}・"
              f"本編 {min(r[3] for r in rows):.2f}〜{max(r[3] for r in rows):.2f}・本編−設計 中央値 {np.median(d):+.2f}")
        print(f"本編で {G.TARGET:.0f}:1 を下回った升のあるカット {len(under)}")
        for c, k, rd, rf, md, mf, at, n in sorted(under, key=lambda r: r[3]):
            print(f"  ⚠️ {c}  設計 {rd:.2f}・本編 {rf:.2f}（升 {at}）")
    print(f"→ {out}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
