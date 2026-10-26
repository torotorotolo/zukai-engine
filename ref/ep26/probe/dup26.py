# 26本目 ②：縮小版どうしを特徴点（ORB）で総当たりし、同じ写真の別の版・切り抜きを拾う（ファイル名や題では決まらない＝記憶 feedback-duplicate-art-needs-pixel-comparison）
# 使い方: python -P ref/ep26/probe/dup26.py <縮小版のフォルダ> <出力.tsv> [--min 25]
import argparse, itertools, os, sys

import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tdir")
    ap.add_argument("out")
    ap.add_argument("--min", type=int, default=25)
    a = ap.parse_args()
    orb = cv2.ORB_create(nfeatures=1500)
    feats = {}
    for f in sorted(os.listdir(a.tdir)):
        if f.endswith(".tsv"):
            continue
        im = cv2.imdecode(np.fromfile(os.path.join(a.tdir, f), np.uint8), cv2.IMREAD_GRAYSCALE)
        if im is None:
            continue
        kp, des = orb.detectAndCompute(im, None)
        if des is not None and len(kp) >= 20:
            feats[os.path.splitext(f)[0]] = (kp, des)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    rows = []
    for (k1, (p1, d1)), (k2, (p2, d2)) in itertools.combinations(feats.items(), 2):
        m = bf.knnMatch(d1, d2, k=2)
        good = [x[0] for x in m if len(x) == 2 and x[0].distance < 0.75 * x[1].distance]
        if len(good) < 10:
            continue
        src = np.float32([p1[g.queryIdx].pt for g in good]).reshape(-1, 1, 2)
        dst = np.float32([p2[g.trainIdx].pt for g in good]).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        inl = int(mask.sum()) if mask is not None else 0
        if inl >= a.min:
            rows.append((inl, k1, k2, len(good)))
    rows.sort(reverse=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("inliers\ta\tb\tgood\n")
        for r in rows:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n")
    print("images", len(feats), "pairs>=min", len(rows), "->", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
