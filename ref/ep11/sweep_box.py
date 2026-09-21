# -*- coding: utf-8 -*-
"""抜いた帯を**1秒おきに全部**測って、「本当に絵が出ている幅」の地図を作る。

🔴🔴 なぜ要るか（2026-09-21 ⑤c-2 で踏んだ）
   ⑤c は代表のコマだけを `measure_box.py` で測って `footage_map.md` §2-2 の表を作った。
   ⑤c-2 で**使う予定の帯を測り直したら、表に無い額入りが4件出た**：
     `launch` 45秒＝546x434（**上下も切れている**）／`accident` 49秒＝84.2%／
     `srb` 20秒＝**52.4%**（いちばん狭い。しかも `c603` に当てる予定だった帯）／
     `commission` 1秒＝89.4%
   ＝ **額は「帯ごと」ではなく「コマごと」に変わる。**器は 720x480 のままなので
     **門番は1本も鳴らない。**→ 記憶 [[feedback-container-labels-lie-about-the-picture]]

🔴🔴 measure_box.py の「最長の連なり」は**暗いコマで壊れる**（2026-09-21 ⑤c-2 で実測）
   `accident.mpg` を1秒おきに当てたら **90コマ中88コマが額入り・幅は最小2%** と出た。
   原因＝火球のあとの**空が真っ暗なコマ**では、ばらつきのある列が画面の一部にしか無く、
   「ばらつきのある列の最長の連なり」＝絵の幅、という前提が成り立たない。
   ⚠️ **⑤c の6コマの対照（明るい氷・煙）では当たっていた。**
      対照が明るいコマばかりだったので、この穴が見えなかった
      → 記憶 [[feedback-verify-your-own-instrument]]／[[feedback-scale-one-visual-finding-to-a-full-count]]

   → **端から内へ削る**測り方に変えた。額（ピラーボックス）は必ず**画面の端**から始まるので、
     「端から連続して、縦にほぼ一様な列」を帯とみなす。暗い絵の中身は端に接していないので削られない。
   ⚠️ ⑤c が踏んだ「青でない最初の列」の罠は起きない。**黒い走査端も一様なので一緒に削られる**から。

■ 出すもの … `ref/ep11/boxes.json`

使い方:
    python ref/ep11/sweep_box.py --selftest      # 🔴 まずこれ（⑤c が実測した6コマで当てる）
    python ref/ep11/sweep_box.py                 # 全帯を1秒おき
    python ref/ep11/sweep_box.py --runs          # 全画面が続く区間だけ出す（当て先を選ぶ用）
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "boxes.json"

FULL = 0.95          # これ以上なら「全画面」とみなす（実測 97.9% と 89.4% の間）
FLAT = 6.0           # 縦のばらつきがこれ未満の列＝帯とみなす（measure_box.py と同じ）

# 🔴 陽性対照と陰性対照を**同時に**当てる（片側だけだと壊れた道具でも合格して見える）
#    値は 2026-09-21 ⑤c が `measure_box.py` で実測したもの（`footage_map.md` §2-2）。
CONTROL = [
    ("t_ice",  9.0, 470, "🔴 額入り（水受けの氷）"),
    ("t_ice", 28.0, 472, "🔴 額入り（構造材のつらら）"),
    ("t_ice", 14.0, 705, "✅ 全画面（氷の配管）"),
    ("t_ice", 19.0, 705, "✅ 全画面（通信箱）"),
    ("t_ice", 24.0, 705, "✅ 全画面（霜の梁）"),
    ("smoke", 11.0, 705, "✅ 全画面（黒い煙の本体）"),
]


def _edge_trim(flat):
    """端から連続する「一様な列（＝帯）」の数を、左右それぞれ返す。"""
    n = len(flat)
    l = 0
    while l < n and flat[l]:
        l += 1
    r = n - 1
    while r > l and flat[r]:
        r -= 1
    return l, r


def box_of(a):
    """端から内へ削って、絵の長方形を出す。"""
    g = a.mean(axis=2)
    x0, x1 = _edge_trim(g.std(axis=0) < FLAT)
    y0, y1 = _edge_trim(g.std(axis=1) < FLAT)
    return dict(x=int(x0), y=int(y0), w=int(x1 - x0 + 1), h=int(y1 - y0 + 1))


def frames(path, step):
    """🔴 1コマずつ流して読む（全部を1つの袋に読むと MemoryError。実際に踏んだ）。"""
    p = subprocess.Popen(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", str(path),
         "-vf", f"fps=1/{step}", "-f", "image2pipe", "-vcodec", "ppm", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1 << 20)

    def tok():
        """PPM のヘッダを1語ずつ読む（空白・改行・コメント区切り）。"""
        s = b""
        while True:
            c = p.stdout.read(1)
            if not c:
                return None
            if c.isspace():
                if s:
                    return s
                continue
            s += c

    n = 0
    while True:
        magic = tok()
        if magic is None:
            break
        if magic != b"P6":
            raise SystemExit(f"🔴 PPM が読めない（{magic!r}）: {path.name}")
        w, h, _mx = int(tok()), int(tok()), int(tok())
        need = w * h * 3
        buf = bytearray()
        while len(buf) < need:
            chunk = p.stdout.read(need - len(buf))
            if not chunk:
                break
            buf += chunk
        if len(buf) < need:
            break
        yield n, np.frombuffer(bytes(buf), dtype=np.uint8).reshape(h, w, 3).astype(float)
        n += 1
    err = p.stderr.read().decode("utf-8", "replace")
    p.wait()
    if n == 0:
        raise SystemExit(f"🔴 1コマも抜けなかった: {path.name}（fail closed）\n{err[:300]}")


def measure(clips, key, step):
    src = HERE.parent / clips[key]["file"]      # `file` は `ref/` から見た相対
    rows = []
    for i, arr in frames(src, step):
        b = box_of(arr)
        rows.append(dict(t=round(i * step, 2), frac=round(b["w"] / arr.shape[1], 3), **b))
    return rows


def selftest(clips):
    """🔴 全部OK／全部NG と出たら道具を疑う。だから両側の対照を当てる。"""
    want = {}
    for key, t, w, note in CONTROL:
        want.setdefault(key, []).append((t, w, note))
    ng = 0
    for key, items in want.items():
        step = 1.0
        rows = measure(clips, key, step)
        for t, w, note in items:
            got = next((r for r in rows if abs(r["t"] - t) < 0.51), None)
            if got is None:
                print(f"  🔴 {key} {t}s のコマが無い")
                ng += 1
                continue
            ok = abs(got["w"] - w) <= 8
            print(f"  {'OK ' if ok else '🔴 '} {key} {t:5.1f}s  絵の幅 {got['w']:4}"
                  f"（⑤cの実測 {w}）  {note}")
            ng += 0 if ok else 1
    n_frame = sum(1 for _, _, w, _ in CONTROL if w < 600)
    print(f"\n  陽性対照（額入り）{n_frame}件・陰性対照（全画面）{len(CONTROL) - n_frame}件")
    print("selftest: " + ("通った" if ng == 0 else f"🔴 {ng}件 合わない"))
    return 0 if ng == 0 else 2


def runs_of(rows, step):
    out, cur = [], None
    for f in rows:
        full = f["frac"] >= FULL
        if full and cur is None:
            cur = f["t"]
        elif not full and cur is not None:
            out.append((cur, f["t"]))
            cur = None
    if cur is not None:
        out.append((cur, rows[-1]["t"] + step))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", type=float, default=1.0)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--runs", action="store_true")
    a = ap.parse_args()

    clips = json.loads((HERE / "clips.json").read_text(encoding="utf-8"))

    if a.selftest:
        return selftest(clips)

    if a.runs:
        db = json.loads(OUT.read_text(encoding="utf-8"))
    else:
        db = {}
        for key in sorted(clips):
            rows = measure(clips, key, a.step)
            db[key] = dict(at=clips[key]["at"], step=a.step, frames=rows)
            nf = sum(1 for r in rows if r["frac"] < FULL)
            print(f"  {key:11} {len(rows):3}コマ  額入り {nf:3}  "
                  f"幅 {min(r['frac'] for r in rows):.0%}〜{max(r['frac'] for r in rows):.0%}")
        OUT.write_text(json.dumps(db, ensure_ascii=False), encoding="utf-8")
        print(f"✓ {OUT}")

    print(f"\n== 全画面（幅 {FULL:.0%} 以上）が2秒以上つづく区間 ==")
    for key in sorted(db):
        e = db[key]
        rr = [(x, y) for x, y in runs_of(e["frames"], e["step"]) if y - x >= 2]
        print(f"  {key:11} 元の{e['at']}秒〜")
        for x, y in rr:
            print(f"      局所 {x:6.0f}-{y:6.0f} ({y - x:4.0f}s)   "
                  f"元 {e['at'] + x:6.0f}-{e['at'] + y:6.0f}")
        if not rr:
            print("      🔴 2秒以上つづく全画面が無い")
    return 0


if __name__ == "__main__":
    sys.exit(main())
