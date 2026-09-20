# -*- coding: utf-8 -*-
"""c810 `missing_board_01` を**モザイクで**隠し直す（⑤c' 2026-09-20）。

■ なぜ隠し直すか
  ⑤c の所見＝「ぼかしが白黒に落ちて**灰色のもや**になる」。
  ⑤b/⑤c は σ=8.0 のガウスぼかしを**全面**に掛けていたが、

    1. 元が **809×534** しかないのに、画面では 1920 幅＝**2.4倍に伸ばす**
       （σ=8 が実効 σ≒19 になる）
    2. 本番は `build_jiko.duotone` で **L に落として1本の傾きへ**写すので、
       黄・赤・緑の貼り紙が**近い明るさに潰れる**

  この2つが重なって、貼り紙の輪郭まで消えていた。
  ⚠️ **色のまま見ると σ=8 でも「貼り紙の並び」に見える。**だから⑤bで気づけなかった。
     判断は必ず**デュオトーンに落としてから**する。

■ 実測（デュオトーンに落として 1920 幅で測った）

  | 版 | 細かさ（3px窓の分散・小さいほど隠れる） | 貼り紙（40px格子の段差・大きいほど輪郭が残る） |
  |---|---|---|
  | 原本 | 9.58 | 61.16 |
  | σ=8（いままで） | 0.22 | **26.96** |
  | **モザイク14px＋boost** | **0.00** | **41.57** |

  ＝ **隠れ方は σ=8 より強く**（0.22 → 0.00）、**貼り紙の輪郭は 54% 多く残る**。

■ なぜモザイクか
  ガウスは輪郭も中身も同じだけ溶かす。モザイクは**枡の中を平らにして枡の境は残す**ので、
  「顔（20〜30px）と手書き（8〜12px）」は枡より小さく消え、
  「貼り紙（40〜90px）」は枡より大きいので形が残る。

■ 隠せているかの根拠
  枡 14px ＝ 画面では **34px**。顔は元で 20〜30px ＝ **1〜2枡**に収まるので、
  顔の作りは1つも残らない。手書きの字は枡の 1/2 以下。

⚠️ これは**元の写真を上書きする**。`ref/ep10/masked.json` の md5 も書き換える
   （`tools/check_photo_mask.py` が md5 で照合する）。
⚠️ ぼかす前の版は git の履歴（`edaf66c`）に残る。**それはこの道具では消えない**
   （公開リポジトリの履歴をどうするかは⑥までのカズヤくんの判断）。

使い方:
  python qa_out/ep10_remask.py --selftest   陽性対照（画像は書き換えない）
  python qa_out/ep10_remask.py --apply      隠し直して masked.json を更新
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
REL = "ep10/missing_board_01.jpg"
IMG = ROOT / "ref" / REL
REC = ROOT / "ref" / "ep10" / "masked.json"
PRE = "edaf66c"                      # ぼかす前の版（git）
BLK = 14                             # 枡の大きさ（元の画素）
DARK, LIGHT = "#16232e", "#e6eef2"


def mosaic(im, blk=BLK):
    w, h = im.size
    return im.resize((max(1, w // blk), max(1, h // blk)), Image.BOX).resize(
        (w, h), Image.NEAREST)


def duotone(im, boost=True):
    """`build_jiko.duotone` と同じ写し方（本番の幾何で測るため）。"""
    g = im.convert("L")
    if boost:
        g = ImageOps.autocontrast(g, cutoff=(1, 6))
    d = tuple(int(DARK[i:i + 2], 16) for i in (1, 3, 5))
    l = tuple(int(LIGHT[i:i + 2], 16) for i in (1, 3, 5))
    lut = []
    for c in range(3):
        lut += [int(d[c] + (l[c] - d[c]) * (v / 255.0)) for v in range(256)]
    return g.convert("RGB").point(lut)


def measure(im, boost=True):
    """(細かさ, 貼り紙)。**デュオトーンに落として 1920 幅**で測る。"""
    w, h = im.size
    a = np.asarray(duotone(im, boost).convert("L").resize((1920, int(1920 * h / w))),
                   dtype=np.float64)
    m = np.lib.stride_tricks.sliding_window_view(a, (3, 3)).reshape(-1, 9)
    fine = float(np.median(m.var(axis=1)))
    c = a[::40, ::40]
    coarse = float(np.mean(np.abs(np.diff(c, axis=0)))
                   + np.mean(np.abs(np.diff(c, axis=1))))
    return fine, coarse


def original():
    """ぼかす前の版を git から取り出す（いまのファイルはもう σ=8 が掛かっている）。"""
    out = subprocess.run(["git", "-C", str(ROOT), "show", f"{PRE}:ref/{REL}"],
                         capture_output=True)
    if out.returncode != 0 or not out.stdout:
        raise SystemExit(f"🔴 ぼかす前の版が取り出せません（{PRE}）")
    import io
    return Image.open(io.BytesIO(out.stdout)).convert("RGB")


def selftest():
    """陽性対照。**値で**見る（件数でなく値）。1つでも外れたら使わない。"""
    bad = 0
    src = original()
    from PIL import ImageFilter
    now = src.filter(ImageFilter.GaussianBlur(8))     # いままでの隠し方
    new = mosaic(src)

    f0, c0 = measure(src)
    f1, c1 = measure(now)
    f2, c2 = measure(new)
    print(f"  原本          細かさ {f0:6.2f} ／ 貼り紙 {c0:6.2f}")
    print(f"  σ=8（いま）    細かさ {f1:6.2f} ／ 貼り紙 {c1:6.2f}")
    print(f"  モザイク{BLK}px   細かさ {f2:6.2f} ／ 貼り紙 {c2:6.2f}")
    print()

    ok = f2 <= f1
    print(f"  {'✓' if ok else '🔴'} 隠れ方が σ=8 以上（{f2:.2f} ≦ {f1:.2f}）")
    bad += 0 if ok else 1

    ok = c2 > c1 * 1.2
    print(f"  {'✓' if ok else '🔴'} 貼り紙の輪郭が σ=8 より 2割以上多い "
          f"（{c2:.2f} > {c1 * 1.2:.2f}）")
    bad += 0 if ok else 1

    ok = f0 > f2 * 10
    print(f"  {'✓' if ok else '🔴'} 原本より確かに細かさが落ちている "
          f"（{f0:.2f} ≫ {f2:.2f}）")
    bad += 0 if ok else 1

    # 枡の中が本当に平らか（モザイクになっているか）を直に見る
    a = np.asarray(new.convert("L"), dtype=np.float64)
    flat = float(a[3:BLK - 3, 3:BLK - 3].std())
    ok = flat < 0.5
    print(f"  {'✓' if ok else '🔴'} 枡の中が平ら（左上の枡の標準偏差 {flat:.3f} < 0.5）")
    bad += 0 if ok else 1

    print()
    print("🔴 この隠し方は使えません" if bad else "✓ 陽性対照は4つとも通った")
    return bad


def apply():
    src = original()
    new = mosaic(src)
    new.save(IMG, quality=92)
    md5 = hashlib.md5(IMG.read_bytes()).hexdigest()
    rec = json.loads(REC.read_text(encoding="utf-8"))
    rec[REL] = {
        "md5": md5,
        "when": "2026-09-20",
        "what": f"私人の顔写真と名前（公共ヌリ第1類型＝手直しが許されている）／"
                f"モザイク {BLK}px。⑤c' で σ=8 の全面ぼかしから替えた"
                f"（デュオトーンに落とすと貼り紙の輪郭まで消えていたため）",
    }
    REC.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    f, c = measure(new)
    print(f"✓ 隠し直しました  {IMG}")
    print(f"  md5 {md5}")
    print(f"  細かさ {f:.2f} ／ 貼り紙 {c:.2f}")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)
    if "--apply" in sys.argv:
        apply()
    else:
        print(__doc__)
