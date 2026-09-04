# -*- coding: utf-8 -*-
"""surfside_slides.py — 技術的知見（77分・4K）のスライドを**機械で数える**（2026-09-04）。

■ なぜ要るか
    ②素材の残りに「NIST 技術的知見のPDF／スライドの図版の点数と解像度」がある。
    実測の結果、**PDF も PPT も公開されていない**（NIST の刊行物検索・記事・調査ページの全部で0本）。
    出どころは **77.3分・3840x2160 の解説動画そのもの**しかない。
    → 動画からコマを抜いて、**別々のスライドが何枚あるか／そのうち図版を載せた枚が何枚か**を数える。

■ ⚠️ なぜ目で数えないか
    枚数が3桁ある。全部を見ると画像の費用が枚数の2乗で効く（共通ルール 鉄則1）。
    **機械で数え、正しく数えられているかだけを少数の見取り図で検算する。**

■ 測り方
    1. 一定間隔でコマを抜く（ffmpeg の範囲取得。落とさない）
    2. 同じスライドの連続を **差分ハッシュ（dHash）** でまとめる ＝ 別々のスライドの枚数
    🔴 3. 中身（図版か文字か）は**判定しない**。画素の量では決まらないと実測で分かった
       （`measure()` の説明を読むこと）。割合は目視の系統標本で数える

■ 使い方
    python tools/surfside_slides.py grab --every 25      # コマを抜く（時間がかかる）
    python tools/surfside_slides.py count                # 数える
    python tools/surfside_slides.py sheet --pick 12      # 検算用の見取り図
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
FRAMES = DIR / "slides"
TITLE = "NCST Champlain Towers South Investigation | Technical Findings"

# 本文域＝上の見出し帯（約13%）を除いた部分。帯は全スライド共通なので入れると差が出ない
BODY_TOP = 0.13


def video_row() -> dict:
    rows = json.loads((DIR / "videos.json").read_text(encoding="utf-8"))
    for r in rows:
        if r["title"].startswith(TITLE[:40]):
            return r
    raise SystemExit("🔴 videos.json に技術的知見の行が無い")


# ------------------------------------------------------------------ 抜く
def cmd_grab(a) -> int:
    r = video_row()
    url, dur = r["file_url"], float(r["sec"])
    FRAMES.mkdir(parents=True, exist_ok=True)
    times = [t for t in range(int(dur * 0.01), int(dur * 0.995), a.every)]
    print(f"{len(times)}コマ / {dur/60:.1f}分 / 間隔{a.every}秒")
    ok = 0
    for i, t in enumerate(times):
        f = FRAMES / f"t{t:05d}.jpg"
        if f.exists() and f.stat().st_size > 3000:
            ok += 1
            continue
        p = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", url,
             "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "3", str(f)],
            capture_output=True, timeout=300)
        if p.returncode == 0 and f.exists():
            ok += 1
        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{len(times)}  取れた {ok}")
    print(f"✅ {ok}/{len(times)} コマ → {FRAMES}")
    return 0


# ------------------------------------------------------------------ 数える
def dhash(im: Image.Image, s: int = 12) -> int:
    g = im.convert("L").resize((s + 1, s), Image.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for y in range(s):
        for x in range(s):
            bits = (bits << 1) | (1 if px[y * (s + 1) + x] > px[y * (s + 1) + x + 1] else 0)
    return bits


def measure(im: Image.Image) -> dict:
    """🔴 **この道具は「図版あり／文字だけ」を判定しない。**（2026-09-04 に2回外した）

    ① `ink`（白でも黒でもない画素の割合）＋色数で分けようとした
       → 断面図（車と柱番号だけの線図）は白地が多く `ink=0.07` で「文字だけ」に落ち、
         話者の顔は `ink=0.94` で「図版あり」に上がった。**両方向に外れた。**
    ② 「白い本文域があればスライド」に変えた
       → **3Dモデルのスライドは背景が黒**なので「話者」に落ちた。**また外れた。**

    ＝ **図版かどうかは画素の量では決まらない。** 数だけ機械で出し、
    　 中身の割合は**目視の系統標本**で数える（→ FINDINGS.md）。
    """
    w, h = im.size
    body = im.crop((0, int(h * BODY_TOP), w, h)).convert("RGB")
    small = body.resize((240, max(1, int(240 * body.size[1] / body.size[0]))), Image.LANCZOS)
    px = list(small.getdata())
    n = len(px)
    ink = white = 0
    for r, g, b in px:
        mx, mn = max(r, g, b), min(r, g, b)
        if mn > 232:
            white += 1
        elif mx >= 42:
            ink += 1
    colors = len(small.quantize(colors=64).convert("RGB").getcolors(65536) or [])
    return {"ink": round(ink / n, 4), "white": round(white / n, 4), "colors": colors}


def cmd_count(a) -> int:
    files = sorted(FRAMES.glob("t*.jpg"))
    if not files:
        print("🔴 コマが無い。先に grab")
        return 1
    rows, prev, cur = [], None, None
    for f in files:
        im = Image.open(f)
        hsh = dhash(im)
        # 直前と近ければ同じスライド（ハミング距離）
        same = prev is not None and bin(hsh ^ prev).count("1") <= a.tol
        if same and cur:
            cur["frames"] += 1
            cur["until"] = int(f.stem[1:])
        else:
            cur = {"at": int(f.stem[1:]), "until": int(f.stem[1:]),
                   "frames": 1, "file": f.name, **measure(im)}
            rows.append(cur)
        prev = hsh
    (DIR / "slides.json").write_text(
        json.dumps({"sampled_frames": len(files), "distinct": len(rows),
                    "note": "🔴 中身（図版か文字か）はこの道具では決めない。目視の系統標本で数える",
                    "thresh": {"tol": a.tol}, "rows": rows},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"コマ {len(files)} → **別々の画面 {len(rows)}**")
    print("  ⚠️ 中身の内訳はこの道具では出さない（検算で2回外した）→ 目視の標本で数える")
    print(f"→ {DIR/'slides.json'}")
    return 0


# ------------------------------------------------------------------ 検算
def cmd_sheet(a) -> int:
    d = json.loads((DIR / "slides.json").read_text(encoding="utf-8"))
    rows = d["rows"]
    step = max(1, len(rows) // a.pick)
    pick = rows[a.offset::step][:a.pick]
    tiles = [(r, Image.open(FRAMES / r["file"]).convert("RGB").resize((480, 270))) for r in pick]
    cols = 3
    rn = (len(tiles) + cols - 1) // cols
    pad, bar = 5, 20
    sh = Image.new("RGB", (cols * 480 + pad * (cols + 1), rn * (270 + bar) + pad * (rn + 1)), (22, 22, 24))
    dr = ImageDraw.Draw(sh)
    for i, (r, im) in enumerate(tiles):
        x = pad + (i % cols) * (480 + pad)
        y = pad + (i // cols) * (270 + bar + pad)
        sh.paste(im, (x, y))
        m, s = divmod(r["at"], 60)
        dr.text((x + 3, y + 274), f"{m}:{s:02d}  ink={r['ink']:.2f} col={r['colors']}",
                fill=(240, 240, 240))
    out = DIR / f"sheets/slides_{a.tag}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sh.save(out, quality=88)
    print(f"✅ {out}  {sh.size[0]}x{sh.size[1]}  {len(tiles)}枚")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grab"); g.add_argument("--every", type=int, default=25)
    c = sub.add_parser("count")
    c.add_argument("--tol", type=int, default=12, help="dHash のハミング距離の許容")
    s = sub.add_parser("sheet")
    s.add_argument("--pick", type=int, default=12)
    s.add_argument("--tag", default="all", help="出力ファイル名の札")
    s.add_argument("--offset", type=int, default=0, help="標本の開始位置をずらす")
    a = ap.parse_args()
    return {"grab": cmd_grab, "count": cmd_count, "sheet": cmd_sheet}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
