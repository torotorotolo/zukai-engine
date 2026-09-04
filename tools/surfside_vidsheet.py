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


def main() -> int:
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
