# -*- coding: utf-8 -*-
"""surfside_vidsheet.py — 記録映像の**中身**を数えるための見取り図を作る（2026-09-04）。

■ なぜ要るか
    ②素材で決めたいのは解像度ではなく「**何が映っているか**」。
    B-Roll #1〜#4 は題が `Champlain Tower South NIST Investigation` としか書いていないので、
    **崩落現場の映像が入っているのか、研究所の試験だけなのか**が分からない。
    弱点（事故そのものの絵が21点しかない）を埋められるかは、ここで決まる。

■ 🔴 なぜ落とさずに抜くか
    B-Roll は1本 600MB 級。C ドライブの空きが 4.1GB しかない（2026-09-04 実測）。
    Kaltura の実ファイルは HTTP の範囲取得（range request）に対応しているので、
    **ffmpeg が該当の1コマだけを取りに行ける**（1枚あたり実測3.5秒）。

■ ⚠️ これは検品ではない
    作るのは「中身の仕分け」用の見取り図。**粗を探す目視の代わりにはしない**
    （検品は原寸・全数が規則）。1コマ640px は「瓦礫か研究室か」を分けるには足りる。

■ 使い方
    python tools/surfside_vidsheet.py --title "B-Roll Video Reel #1" --n 6
    python tools/surfside_vidsheet.py --section BRoll --n 6

■ 🔴 1秒刻みの見取り図（2026-09-06 追加。⑤c' 直す #2）
    ショットの**境目**と「その秒に何が写っているか」を決めるための窓。
    ⑤c 見る B・C で「3秒刻みの見取り図はショットの中の切り替わりを見ていない」と
    分かった（c322 c325 c328 c628 の4件が、範囲の中なのに対象を写していなかった）。
    `footage.USE` の `clip` の名前で呼ぶ（署名付き URL は毎回取り直す）。

    python tools/surfside_vidsheet.py sec ss_b1 8 19          # 1秒刻み・3列
    python tools/surfside_vidsheet.py sec ss_b8 128 134 --step 0.5 --cols 3
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
DIR = HERE / "analytics" / "materials" / "surfside"
SHEETS = DIR / "sheets"
TILE_W = 640


def grab(url: str, sec: float, dst: Path) -> bool:
    p = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", f"{sec:.2f}", "-i", url,
         "-frames:v", "1", "-vf", f"scale={TILE_W}:-2", str(dst)],
        capture_output=True, timeout=300)
    return p.returncode == 0 and dst.exists() and dst.stat().st_size > 2000


def sheet(row: dict, n: int) -> Path | None:
    url, dur = row.get("file_url", ""), float(row.get("sec", 0) or 0)
    if not url or dur <= 0:
        print(f"🔴 実ファイルが無い: {row['title'][:50]}")
        return None
    if row["host"] == "youtube":
        print(f"（飛ばす）YouTube 側: {row['title'][:50]}")
        return None
    SHEETS.mkdir(parents=True, exist_ok=True)
    lo, hi = dur * 0.03, dur * 0.97
    times = [lo + (hi - lo) * i / max(1, n - 1) for i in range(n)]
    tiles = []
    for i, t in enumerate(times):
        f = SHEETS / f"_t{i}.jpg"
        if grab(url, t, f):
            tiles.append((t, Image.open(f).convert("RGB")))
        else:
            print(f"   🔴 {t:.0f}秒 が抜けない")
    if not tiles:
        return None
    cols = 2
    rows_n = (len(tiles) + cols - 1) // cols
    tw, th = tiles[0][1].size
    pad, bar = 6, 22
    sh = Image.new("RGB", (cols * tw + pad * (cols + 1),
                           rows_n * (th + bar) + pad * (rows_n + 1)), (24, 24, 26))
    d = ImageDraw.Draw(sh)
    for i, (t, im) in enumerate(tiles):
        c, r = i % cols, i // cols
        x = pad + c * (tw + pad)
        y = pad + r * (th + bar + pad)
        sh.paste(im.resize((tw, th)), (x, y))
        m, s = divmod(int(t), 60)
        d.text((x + 4, y + th + 4), f"{m}:{s:02d}", fill=(235, 235, 235))
    safe = "".join(ch if ch.isalnum() else "_" for ch in row["title"])[:48]
    out = SHEETS / f"{safe}.jpg"
    sh.save(out, quality=88)
    for i in range(len(times)):
        (SHEETS / f"_t{i}.jpg").unlink(missing_ok=True)
    print(f"✅ {out.name}  {sh.size[0]}x{sh.size[1]}  ({len(tiles)}コマ / {dur:.0f}秒)")
    return out


def sheet_seconds(clip, t0, t1, step=1.0, cols=3, out=None):
    """`footage.CLIPS` の1本から、t0〜t1 を step 秒刻みで抜いて1枚に組む。"""
    sys.path.insert(0, str(Path(__file__).parent))
    import footage as F
    if clip not in F.CLIPS:
        raise SystemExit(f"🔴 {clip} は footage.CLIPS に無い（{', '.join(F.CLIPS)}）")
    url = F.urls_of(clip)[0]
    tmp = SHEETS
    tmp.mkdir(parents=True, exist_ok=True)
    times, t = [], float(t0)
    while t <= float(t1) + 1e-6:
        times.append(round(t, 2))
        t += float(step)
    tiles = []
    for i, tt in enumerate(times):
        f = tmp / f"_s{i}.jpg"
        if grab(url, tt, f):
            tiles.append((tt, Image.open(f).convert("RGB")))
        else:
            print(f"   🔴 {tt:.1f}秒 が抜けない")
    if not tiles:
        raise SystemExit("🔴 1コマも抜けなかった（署名 URL の期限切れ？）")
    tw, th = tiles[0][1].size
    pad, bar = 6, 26
    rows_n = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (cols * tw + pad * (cols + 1),
                           rows_n * (th + bar) + pad * (rows_n + 1)), (24, 24, 26))
    d = ImageDraw.Draw(sh)
    for i, (tt, im) in enumerate(tiles):
        c, r = i % cols, i // cols
        x = pad + c * (tw + pad)
        y = pad + r * (th + bar + pad)
        sh.paste(im.resize((tw, th)), (x, y))
        d.text((x + 4, y + th + 5), f"{tt:.1f}s", fill=(255, 220, 120))
    out = Path(out) if out else (SHEETS / f"sheet_{clip}_{t0}_{t1}.jpg")
    out.parent.mkdir(parents=True, exist_ok=True)
    sh.save(out, quality=90)
    for i in range(len(times)):
        (tmp / f"_s{i}.jpg").unlink(missing_ok=True)
    print(f"✅ {out}  {sh.size[0]}x{sh.size[1]}  {len(tiles)}コマ "
          f"（{t0}〜{t1}秒・{step}秒刻み）")
    return out


def shot_cuts(clip, t0, t1, step=0.25, thr=0.25):
    """ショットの**境目**を、画像を1枚も見ずに見つける（2026-09-06 追加）。

    となり合うコマのエッジ画像の相関を測る。同じショットの中は 0.4〜1.0、
    ショットが変わると 0.0 付近に落ちる（実測：ss_b8 の 70.0秒と 70.14秒で 0.001）。
    ⚠️ `footage.USE` の注記の「N〜M秒」は目で見て書いたので **0.5〜1秒ずれている**
       （c328 は「64〜71秒」と書いてあったが実際の境目は 70.1秒。c325 は 52.5→51.9）。
       `until=` はここで測った値を入れる。
    """
    import numpy as np
    sys.path.insert(0, str(Path(__file__).parent))
    import footage as F
    url = F.urls_of(clip)[0]
    tmp = SHEETS / "_cuts"
    tmp.mkdir(parents=True, exist_ok=True)
    times, t = [], float(t0)
    while t <= float(t1) + 1e-6:
        times.append(round(t, 3))
        t += float(step)
    arrs = []
    for i, tt in enumerate(times):
        f = tmp / f"_c{i}.jpg"
        if not grab(url, tt, f):
            print(f"   🔴 {tt}秒 が抜けない")
            arrs.append(None)
            continue
        a = np.asarray(Image.open(f).convert("L"), dtype=float)
        arrs.append(np.abs(np.diff(a, axis=0)))
    print(f"■ {clip} {t0}〜{t1}秒（{step}秒刻み・{len(times)}コマ）")
    bounds = []
    for i in range(1, len(arrs)):
        a, b = arrs[i - 1], arrs[i]
        if a is None or b is None or a.shape != b.shape:
            continue
        x, y = a - a.mean(), b - b.mean()
        r = float((x * y).sum() / np.sqrt((x * x).sum() * (y * y).sum()))
        mark = ""
        if r < thr:
            mark = "  ← ここで切り替わる"
            bounds.append((times[i - 1], times[i], r))
        print(f"   {times[i-1]:7.2f} → {times[i]:7.2f}  相関 {r:5.3f}{mark}")
    for i in range(len(times)):
        (tmp / f"_c{i}.jpg").unlink(missing_ok=True)
    # ⚠️ **カメラが動いているショットは、となり合うコマも相関が落ちる**（2026-09-06 実測。
    #    B-Roll #1 の 13〜16秒は手持ちの寄りで、0.25秒ごとに全部「境目」に見えた）。
    #    → 低い値が**3つ以上続いたら「カメラが動いている」**と読む。1つだけ落ちたら切り替わり。
    runs, cur = [], []
    for i in range(1, len(arrs)):
        low = any(abs(b[0] - times[i - 1]) < 1e-9 for b in bounds)
        if low:
            cur.append(times[i - 1])
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    real = [r for r in runs if len(r) <= 2]
    moving = [r for r in runs if len(r) > 2]
    if real:
        print("🔴 切り替わり: " + "／".join(f"{r[0]}〜{r[-1] + step}秒" for r in real))
    if moving:
        print("⚠️ カメラが動いている（境目ではない）: "
              + "／".join(f"{r[0]}〜{r[-1] + step}秒" for r in moving))
    if not bounds:
        print(f"✓ {t0}〜{t1}秒 は1つのショット（相関はどこも {thr} 以上）")
    elif not real:
        print(f"✓ 切り替わりは無い（{t0}〜{t1}秒 はカメラが動いているだけ）")
    return real


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "cuts":
        ap = argparse.ArgumentParser(prog="surfside_vidsheet.py cuts")
        ap.add_argument("clip")
        ap.add_argument("t0", type=float)
        ap.add_argument("t1", type=float)
        ap.add_argument("--step", type=float, default=0.25)
        ap.add_argument("--thr", type=float, default=0.25)
        a = ap.parse_args(sys.argv[2:])
        shot_cuts(a.clip, a.t0, a.t1, a.step, a.thr)
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "sec":
        ap = argparse.ArgumentParser(prog="surfside_vidsheet.py sec")
        ap.add_argument("clip")
        ap.add_argument("t0", type=float)
        ap.add_argument("t1", type=float)
        ap.add_argument("--step", type=float, default=1.0)
        ap.add_argument("--cols", type=int, default=3)
        ap.add_argument("--out", default="")
        a = ap.parse_args(sys.argv[2:])
        sheet_seconds(a.clip, a.t0, a.t1, a.step, a.cols, a.out or None)
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default="")
    ap.add_argument("--section", default="")
    ap.add_argument("--n", type=int, default=6)
    a = ap.parse_args()
    rows = json.loads((DIR / "videos.json").read_text(encoding="utf-8"))
    sel = [r for r in rows
           if (not a.title or r["title"].startswith(a.title))
           and (not a.section or r["section"] == a.section)]
    if not sel:
        print("🔴 該当なし")
        return 1
    for r in sel:
        print(f"■ {r['title'][:70]}")
        sheet(r, a.n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
