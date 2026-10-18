# -*- coding: utf-8 -*-
"""23本目 映像方針：Commons の1995年の点（239）どうしで「同じ写真・同じ構図」の組を機械で出す（2026-10-18）。

  python ref/ep23/eizou_build/helpers/dup23.py pairs <出力.tsv> [しきい値 0.80]
  python ref/ep23/eizou_build/helpers/dup23.py file <画像> [<画像> ...]      # 手元の画像（取得したもの）を239点と突き合わせる

見る絵＝ref/ep10/src/commons_640/NNN.jpg（Commons の約960px の縮小版。番号＝commons_all.json の y95 の no）。
物差し＝縦横比が3%以内の組だけ・グレースケール 48×48 に縮めて平均と広がりをそろえた相関（1.0＝同じ）と、
160×120 で「差が16を超える画素の割合」（記憶 feedback-duplicate-art-needs-pixel-comparison＝0%＝同一・10%未満＝同じ絵に見える目安）。
"""
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
THUMBS = os.path.join(REPO, 'ref', 'ep10', 'src', 'commons_640')
ALL = os.path.join(REPO, 'ref', 'ep10', 'src', 'commons_all.json')


def sig(path):
    im = Image.open(path)
    im.load()
    g = im.convert('L')
    a = np.asarray(g.resize((48, 48), Image.BILINEAR), dtype=np.float64)
    a = (a - a.mean()) / (a.std() + 1e-6)
    b = np.asarray(g.resize((160, 120), Image.BILINEAR), dtype=np.float64)
    lo, hi = np.percentile(b, 2), np.percentile(b, 98)
    b = np.clip((b - lo) / max(hi - lo, 1) * 255, 0, 255)
    return im.size[0] / im.size[1], a.ravel(), b


def load():
    d = json.load(open(ALL, encoding='utf-8'))
    rows = [r for r in d['files'] if r.get('y95')]
    out = {}
    for r in rows:
        p = os.path.join(THUMBS, '%03d.jpg' % r['no'])
        if os.path.exists(p):
            out[r['no']] = sig(p)
    return out


def compare(s1, s2):
    ar1, a1, b1 = s1
    ar2, a2, b2 = s2
    if abs(ar1 - ar2) / max(ar1, ar2) > 0.03:
        return None
    corr = float(np.dot(a1, a2) / len(a1))
    diff = float((np.abs(b1 - b2) > 16).mean())
    return corr, diff


def orb_feats(paths, long_edge=800, n=1200):
    import cv2
    orb = cv2.ORB_create(nfeatures=n)
    out = {}
    for k, p in paths.items():
        g = np.asarray(Image.open(p).convert('L'))
        s = long_edge / max(g.shape)
        if s < 1:
            g = cv2.resize(g, (round(g.shape[1] * s), round(g.shape[0] * s)), interpolation=cv2.INTER_AREA)
        kp, des = orb.detectAndCompute(g, None)
        out[k] = ([p.pt for p in kp], des, g.shape[1] >= g.shape[0])
    return out


def orb_inliers(f1, f2):
    """特徴点（ORB）を突き合わせ、RANSAC で1つの写し方（相似変換）に乗る点を数える＝同じ写真なら数十〜百、別の写真は数点。"""
    import cv2
    p1, d1, _ = f1
    p2, d2, _ = f2
    if d1 is None or d2 is None or len(d1) < 8 or len(d2) < 8:
        return 0
    m = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d1, d2, k=2)
    good = [x[0] for x in m if len(x) == 2 and x[0].distance < 0.75 * x[1].distance]
    if len(good) < 8:
        return len(good) // 4
    src = np.float32([p1[g.queryIdx] for g in good])
    dst = np.float32([p2[g.trainIdx] for g in good])
    M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=4.0)
    return int(inl.sum()) if inl is not None else 0


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    a = sys.argv[1:]
    if a[0] == 'orb':
        # python dup23.py orb <出力.tsv> [しきい値 15] [--with 画像1,画像2,...]＝239点＋手元の画像を総当たり（向きが同じ組だけ）
        th = int(a[2]) if len(a) > 2 and not a[2].startswith('--') else 15
        d = json.load(open(ALL, encoding='utf-8'))
        paths = {'#%d' % r['no']: os.path.join(THUMBS, '%03d.jpg' % r['no']) for r in d['files'] if r.get('y95')}
        if '--with' in a:
            for p in a[a.index('--with') + 1].split(','):
                paths[os.path.basename(p)] = p
        feats = orb_feats(paths)
        keys = sorted(feats)
        res = []
        for i, x in enumerate(keys):
            for y in keys[i + 1:]:
                if feats[x][2] != feats[y][2]:
                    continue
                n = orb_inliers(feats[x], feats[y])
                if n >= th:
                    res.append((n, x, y))
        res.sort(reverse=True)
        with open(a[1], 'w', encoding='utf-8', newline='\n') as f:
            f.write('# ORB の一致点（RANSAC の内側）\t1\t2\n')
            for n, x, y in res:
                f.write('%d\t%s\t%s\n' % (n, x, y))
        print('組 %d（一致点 ≥ %d）→ %s' % (len(res), th, a[1]))
        return
    sigs = load()
    if a[0] == 'pairs':
        th = float(a[2]) if len(a) > 2 else 0.80
        nos = sorted(sigs)
        res = []
        for i, x in enumerate(nos):
            for y in nos[i + 1:]:
                c = compare(sigs[x], sigs[y])
                if c and c[0] >= th:
                    res.append((c[0], c[1], x, y))
        res.sort(reverse=True)
        with open(a[1], 'w', encoding='utf-8', newline='\n') as f:
            f.write('# 相関\t差>16の割合\t番号1\t番号2\n')
            for c, df, x, y in res:
                f.write('%.3f\t%.3f\t#%d\t#%d\n' % (c, df, x, y))
        print('組 %d（相関 ≥ %.2f）→ %s' % (len(res), th, a[1]))
    elif a[0] == 'file':
        for p in a[1:]:
            s = sig(p)
            best = sorted(((compare(s, v) or (-1, 1)), k) for k, v in sigs.items())[::-1][:3]
            print(os.path.basename(p), ' '.join('#%d 相関%.3f 差%.3f' % (k, c[0], c[1]) for c, k in best))


if __name__ == '__main__':
    main()
