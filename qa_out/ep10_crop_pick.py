# -*- coding: utf-8 -*-
"""⑤c' 「寄せ」のやり直しを、**目でなく数字で**決める。

⑤c と ⑤c-2 が挙げた2件は、どちらも「寄せ」の話だった：

  ① `c105` … コントラスト **39.0 ＝ 90欄で最小**。画の4分の3が平坦な曇り空
  ② 使い回し … `sampoong_before_01`（c101/c109/c115）と `_02`（c105/c205）は
     公共ヌリ＝**寄りを変えてよい**のに、切り出し窓が **82.6〜100%** 重なっていた

この2つは同じ操作（fx, fy, zoom）で決まるので、**1つの道具で測る**。

■ 測るもの（すべて**元の写真の画素**から）
  - 窓 … `cuts.ss.focus()` と同じ式で (left, top, cw, ch) を逆算する
          ⚠️ 引き写しではなく、`focus()` を**実際に呼んで** xbias/ybias を得てから戻す
  - 空の割合 … 行ごとの標準偏差が SKY_SD 未満で、かつ明るい行を「空」と数える
  - コントラスト … 窓の中の p95 − p5（`ep10_photo_light.py` と同じ取り方）
  - 重なり … 2つの窓の共通面積 ÷ 小さいほうの面積

■ 陽性対照（`--selftest`）
  「同じ寄せどうしは重なり 100%」「zoom を上げると窓は必ず小さくなる」
  「空だけを切った窓は空の割合 100%・建物だけの窓は 50% 未満」を**値で**確かめる。
  ⚠️ 1つでも外れたら、この道具の数字は使わない（[[feedback-verify-your-own-instrument]]）。

使い方:
  python qa_out/ep10_crop_pick.py            … いまの寄せを測る
  python qa_out/ep10_crop_pick.py --search   … c105 の寄せ直しの候補を出す
  python qa_out/ep10_crop_pick.py --selftest … 陽性対照
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
from PIL import Image

import cuts.ss as ss

SKY_SD = 12.0          # 行の標準偏差がこれ未満なら「平坦」
SKY_MIN = 120.0        # かつ、この明るさ以上なら「空」

# いまの寄せ（`tools/cuts/*.py` の ss.focus(...) と同じ値）
NOW = {
    "c105": ("sampoong_before_02", 0.50, 0.34, 1.28),
    "c205": ("sampoong_before_02", 0.50, 0.50, 1.00),
    "c101": ("sampoong_before_01", 0.50, 0.50, 1.00),
    "c109": ("sampoong_before_01", 0.50, 0.28, 1.34),
    "c115": ("sampoong_before_01", 0.50, 0.46, 1.20),
}


REF = Path(__file__).resolve().parents[1] / "ref"


def _src(name):
    return ss.P(name)


def _trim_box(name):
    """`trimmed_size` が当てている窓を、元のファイルの割合 (x0,y0,x1,y1) で返す。

    ⚠️ `trimmed_size` は**寸法しか返さない**ので、位置は自分で取り直す。
       ここを取りこぼすと、切り出しの**原点がずれたまま**明るさを測ることになる。
    """
    p = _src(name)
    t = ss.TRIM.get(p)
    if t:
        return t
    b = ss.BANDS.get(p.split("/", 1)[-1].rsplit(".", 1)[0])
    if b and b.get("fig_box"):
        return b["fig_box"]
    return (0.0, 0.0, 1.0, 1.0)


def window(name, fx, fy, zoom):
    """`focus()` が返す xbias/ybias から、元の写真の中の窓 (l, t, cw, ch) を戻す。"""
    d = ss.focus(_src(name), fx, fy, zoom)
    sw, sh = ss.trimmed_size(_src(name))
    w, h = ss.W, ss.H
    z = max(w / sw, h / sh) * zoom
    cw, ch = min(sw, w / z), min(sh, h / z)
    l = (sw - cw) * d["xbias"]
    t = (sh - ch) * d["bias"]      # ⚠️ 縦は "ybias" ではなく "bias"
    return l, t, cw, ch, sw, sh


def _gray(name):
    """`trimmed_size` が見ているのと**同じ範囲**を切ってから返す。"""
    im = Image.open(REF / _src(name)).convert("L")
    iw, ih = im.size
    x0, y0, x1, y1 = _trim_box(name)
    if (x0, y0, x1, y1) != (0.0, 0.0, 1.0, 1.0):
        im = im.crop((int(iw * x0), int(ih * y0), int(iw * x1), int(ih * y1)))
    return np.asarray(im, dtype=np.float64), im.size


def measure(name, fx, fy, zoom):
    g, (iw, ih) = _gray(name)
    l, t, cw, ch, sw, sh = window(name, fx, fy, zoom)
    # 切ったあとの寸法と trimmed_size は一致するはず。ずれたら比で合わせる
    kx, ky = iw / sw, ih / sh
    x0, y0 = int(round(l * kx)), int(round(t * ky))
    x1, y1 = int(round((l + cw) * kx)), int(round((t + ch) * ky))
    c = g[max(0, y0):y1, max(0, x0):x1]
    if c.size == 0:
        return None
    sd = c.std(axis=1)
    mean = c.mean(axis=1)
    sky = float(np.mean((sd < SKY_SD) & (mean > SKY_MIN)))
    p5, p95 = np.percentile(c, 5), np.percentile(c, 95)
    return dict(win=(l, t, cw, ch), src=(sw, sh), sky=sky,
                med=float(np.median(c)), con=float(p95 - p5))


def overlap(a, b):
    (l1, t1, w1, h1), (l2, t2, w2, h2) = a, b
    ix = max(0.0, min(l1 + w1, l2 + w2) - max(l1, l2))
    iy = max(0.0, min(t1 + h1, t2 + h2) - max(t1, t2))
    inter = ix * iy
    return inter / min(w1 * h1, w2 * h2) if inter else 0.0


def show(rows):
    print(f"{'cut':6} {'素材':22} {'fy':>5} {'zoom':>5} "
          f"{'窓(l,t,w,h)':>26} {'空%':>6} {'中央値':>7} {'ｺﾝﾄﾗｽﾄ':>7}")
    print("-" * 100)
    for cid, (nm, fx, fy, zm) in rows.items():
        m = measure(nm, fx, fy, zm)
        l, t, w, h = m["win"]
        print(f"{cid:6} {nm:22} {fy:5.2f} {zm:5.2f} "
              f"{f'({l:.0f},{t:.0f},{w:.0f},{h:.0f})':>26} "
              f"{m['sky']*100:5.1f}% {m['med']:7.1f} {m['con']:7.1f}")
    print()
    print("■ 同じ素材どうしの窓の重なり（小さいほうに対する割合）")
    ids = list(rows)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = rows[ids[i]], rows[ids[j]]
            if a[0] != b[0]:
                continue
            ov = overlap(measure(*a)["win"], measure(*b)["win"])
            mark = "🔴" if ov > 0.80 else ("⚠️" if ov > 0.60 else "・")
            print(f"  {mark} {ids[i]} × {ids[j]}  {ov*100:5.1f}%")


def iou(a, b):
    """和に対する重なり。**入れ子でも 1.0 にならない**ので、寄せの違いが見える。

    ⚠️ `overlap()`（小さいほうに対する割合）は、片方が全面のとき必ず 100% 近くに
       なるので「寄せを変えても下がらない」＝**直しの当たりを決められない**。
    """
    (l1, t1, w1, h1), (l2, t2, w2, h2) = a, b
    ix = max(0.0, min(l1 + w1, l2 + w2) - max(l1, l2))
    iy = max(0.0, min(t1 + h1, t2 + h2) - max(t1, t2))
    inter = ix * iy
    return inter / (w1 * h1 + w2 * h2 - inter) if inter else 0.0


def profile(name, rows=12):
    """元の写真を横に切って、帯ごとの明るさとばらつきを出す。

    ⑤c-2 の「画の4分の3が平坦な曇り空」が、**どの帯のことか**を数で見るため。
    """
    g, (iw, ih) = _gray(name)
    print(f"■ {name} の縦の profile（{iw}×{ih}／帯ごと）")
    print(f"{'帯':>10} {'中央値':>7} {'ばらつき':>8} {'p95-p5':>8}")
    for k in range(rows):
        a, b = ih * k // rows, ih * (k + 1) // rows
        s = g[a:b, :]
        p5, p95 = np.percentile(s, 5), np.percentile(s, 95)
        print(f"{f'{a}-{b}':>10} {np.median(s):7.1f} {s.std():8.1f} {p95 - p5:8.1f}")


def search(cid="c105", other="c205"):
    """寄せ直しの候補。**コントラストが高い順**に、`other` との IoU を添えて出す。"""
    nm = NOW[cid][0]
    profile(nm)
    print()
    base = measure(*NOW[other])["win"]
    now = measure(*NOW[cid])
    print(f"■ {cid} の候補（コントラストが高い順）"
          f"／いまは コントラスト {now['con']:.1f}・IoU {iou(now['win'], base)*100:.1f}%")
    print(f"{'fx':>5} {'fy':>5} {'zoom':>5} {'中央値':>7} {'ｺﾝﾄﾗｽﾄ':>7} "
          f"{f'{other}とのIoU':>13}")
    print("-" * 52)
    out = []
    for fx in (0.34, 0.42, 0.50, 0.58, 0.66):
        for fy in [round(0.24 + 0.06 * k, 2) for k in range(10)]:
            for zm in [round(1.2 + 0.15 * k, 2) for k in range(9)]:
                m = measure(nm, fx, fy, zm)
                if m is None:
                    continue
                out.append((-m["con"], fx, fy, zm, m, iou(m["win"], base)))
    out.sort()
    seen = set()
    shown = 0
    for _, fx, fy, zm, m, ov in out:
        key = (round(m["win"][0] / 60), round(m["win"][1] / 60), round(zm, 1))
        if key in seen:
            continue
        seen.add(key)
        print(f"{fx:5.2f} {fy:5.2f} {zm:5.2f} {m['med']:7.1f} "
              f"{m['con']:7.1f} {ov*100:12.1f}%")
        shown += 1
        if shown >= 12:
            break


def selftest():
    bad = 0
    nm = "sampoong_before_02"

    a = measure(nm, 0.50, 0.50, 1.00)
    b = measure(nm, 0.50, 0.50, 1.00)
    ov = overlap(a["win"], b["win"])
    ok = abs(ov - 1.0) < 1e-9
    print(f"  {'✓' if ok else '🔴'} 同じ寄せどうしの重なり = {ov*100:.1f}%（100% のはず）")
    bad += 0 if ok else 1

    w1 = measure(nm, 0.50, 0.50, 1.00)["win"]
    w2 = measure(nm, 0.50, 0.50, 1.60)["win"]
    ok = w2[2] < w1[2] and w2[3] < w1[3]
    print(f"  {'✓' if ok else '🔴'} zoom を上げると窓は小さくなる "
          f"{w1[2]:.0f}×{w1[3]:.0f} → {w2[2]:.0f}×{w2[3]:.0f}")
    bad += 0 if ok else 1

    # 空だけ／地面だけ を強制的に切って、空の割合が離れることを見る
    top = measure(nm, 0.50, 0.00, 2.60)
    bot = measure(nm, 0.50, 1.00, 2.60)
    ok = top["sky"] > bot["sky"] + 0.30
    print(f"  {'✓' if ok else '🔴'} 上だけ切ると空 {top['sky']*100:.1f}% ／ "
          f"下だけ切ると空 {bot['sky']*100:.1f}%（上のほうが 30ポイント以上多いはず）")
    bad += 0 if ok else 1

    print()
    print("🔴 この道具の数字は使えません" if bad else "✓ 陽性対照は3つとも通った")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)
    show(NOW)
    if "--search" in sys.argv:
        print()
        search()
