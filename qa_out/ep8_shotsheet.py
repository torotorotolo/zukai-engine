# -*- coding: utf-8 -*-
"""ep8_shotsheet.py — 8本目（コロンビア号）の**動く映像の中身**を見るためのシート（2026-09-15・⑤b-2）。

■ なぜ要るか
    ⑤b-1 は `footage.USE` の秒を空のまま残した。この環境に OCR が無く、
    「どのショットに何が写っているか」を機械で読めなかったため
    （→ [[feedback-dont-state-inferences-as-findings]]）。
    秒を決めるには**絵を見る**しかない。このchは 640px のシートでの全数確認が
    認められている（`~/.claude/CLAUDE.md` 鉄則1の例外）。

■ ⚠️ これは検品ではない
    「そのショットに何が写っているか」を仕分ける窓であって、粗を探す目視ではない。

■ 使い方
    python qa_out/ep8_shotsheet.py shots sts1          # ショットごとに中央のコマ
    python qa_out/ep8_shotsheet.py at mct 30 90 150    # 秒を名指し
    python qa_out/ep8_shotsheet.py crop mct 300 --box 0,0,0.5,0.5   # 一部を原寸で

    出力＝ out/ep8_sheet/<clip>_<連番>.jpg（2列×3行・1枚640px）
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parents[1]
CLIPS = json.loads((HERE / "ref" / "ep8" / "clips.json").read_text(encoding="utf-8"))
SHOTS = json.loads((HERE / "ref" / "ep8" / "shots.json").read_text(encoding="utf-8"))
OUT = HERE / "out" / "ep8_sheet"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TILE_W, COLS, ROWS = 640, 2, 3
BAR = 26


SRC = OUT / "_src"


def local(clip: str) -> Path | None:
    """⚠️ `upload.wikimedia.org` は連続で叩くと **429**（実測）。
    短いクリップは1回だけ落として手元から読む（落とせなければ URL のまま）。"""
    p = SRC / f"{clip}.webm"
    if p.exists() and p.stat().st_size > 0:
        return p
    SRC.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-user_agent", UA, "-i", CLIPS[clip]["url"],
           "-c", "copy", "-y", str(p)]
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0 or not p.exists():
        print(f"  ⚠️ {clip} を落とせませんでした: "
              f"{r.stderr.decode('utf-8', 'replace')[:160]}", file=sys.stderr)
        return None
    print(f"  ↓ {p.relative_to(HERE)}  {p.stat().st_size / 1e6:.1f} MB")
    return p


def grab(clip: str, t: float, tries: int = 3) -> Image.Image | None:
    """1 コマだけ取り出す。手元にあれば手元から、無ければ URL の範囲取得。"""
    import io
    import time
    lp = local(clip)
    # ⚠️ `-user_agent` は **file: では通らない**（"Option user_agent not found." で
    #    毎コマ落ち、シートが灰色の器で埋まる。2026-09-15 に実際に出した）。
    head = ["-user_agent", UA] if lp is None else []
    src = CLIPS[clip]["url"] if lp is None else str(lp)
    for k in range(tries):
        cmd = ["ffmpeg", "-v", "error", *head, "-ss", f"{t:.2f}",
               "-i", src, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode == 0 and p.stdout:
            return Image.open(io.BytesIO(p.stdout)).convert("RGB")
        err = p.stderr.decode("utf-8", "replace")[:120]
        if k + 1 < tries:
            time.sleep(4 * (k + 1))
    print(f"  ⚠️ {clip} {t:.1f}s を取れませんでした: {err}", file=sys.stderr)
    return None


def sheet(clip: str, items: list[tuple[float, str]], tag: str) -> list[Path]:
    """(秒, 札) の並びを 2列×3行 のシートに焼く。"""
    OUT.mkdir(parents=True, exist_ok=True)
    per = COLS * ROWS
    made = []
    for page in range((len(items) + per - 1) // per):
        chunk = items[page * per:(page + 1) * per]
        tiles, miss = [], 0
        for t, lab in chunk:
            im = grab(clip, t)
            if im is None:
                im = Image.new("RGB", (TILE_W, int(TILE_W * 9 / 16)), (40, 40, 40))
                lab, miss = lab + "  ⚠️取れず", miss + 1
            h = max(1, round(TILE_W * im.height / im.width))
            im = im.resize((TILE_W, h), Image.LANCZOS)
            tiles.append((im, lab))
        th = max(im.height for im, _ in tiles)
        sh = Image.new("RGB", (TILE_W * COLS, (th + BAR) * ROWS), (16, 16, 16))
        d = ImageDraw.Draw(sh)
        for i, (im, lab) in enumerate(tiles):
            x, y = (i % COLS) * TILE_W, (i // COLS) * (th + BAR)
            sh.paste(im, (x, y + BAR))
            d.rectangle([x, y, x + TILE_W - 1, y + BAR - 1], fill=(0, 0, 0))
            d.text((x + 6, y + 6), lab, fill=(255, 220, 120))
        p = OUT / f"{clip}_{tag}{page + 1:02d}.jpg"
        sh.save(p, quality=92)
        # 🔴 自分の物差しを疑う：取れなかった枚数を**数字で**出す（灰色の器は絵ではない）
        print(f"  {'⚠️' if miss else '✓'} {p.relative_to(HERE)}  "
              f"({len(chunk)}枚中 取れず {miss})")
        made.append(p)
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("shots", "at", "crop", "mix", "fb"))
    ap.add_argument("clip", help="mix のときは 'clip:秒' を並べる（clip は無視）")
    ap.add_argument("secs", nargs="*")
    ap.add_argument("--box", default=None, help="x0,y0,x1,y1（0〜1）。crop のとき")
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()

    if a.mode == "fb":
        # `footage.USE` の各欄から**ひかえの静止画** `ref/ep8/fb_<cid>.jpg` を焼く。
        # 🔴 動画のコマが取れなかったときに出る絵。**必ず `start` のコマ**から作る
        #    （別の秒から作ると、動画とひかえで別の場面になる）。
        sys.path.insert(0, str(HERE / "tools"))
        import footage as FO
        only = set(a.secs) if a.secs else None
        made = 0
        for cid, u in sorted(FO.USE.items()):
            if only and cid not in only:
                continue
            dest = HERE / "ref" / "ep8" / f"fb_{cid}.jpg"
            if dest.exists() and "--force" not in sys.argv:
                print(f"  ・{dest.name} は在る")
                continue
            im = grab(u["clip"], float(u["start"]))
            if im is None:
                print(f"  🔴 {cid}: コマを取れなかった（0で埋めない）", file=sys.stderr)
                continue
            im.save(dest, quality=94)
            made += 1
            print(f"  ✓ {dest.name}  {im.size}  ← {u['clip']} {u['start']:.1f}秒")
        print(f"  焼いた {made} 枚")
        return
    if a.mode == "mix":
        # 複数のクリップを1枚のシートに混ぜる（1枚の中身を見分けるだけの窓）
        OUT.mkdir(parents=True, exist_ok=True)
        pairs = [(s.split(":")[0], float(s.split(":")[1]))
                 for s in [a.clip, *a.secs] if ":" in s]
        per = COLS * ROWS
        for page in range((len(pairs) + per - 1) // per):
            chunk = pairs[page * per:(page + 1) * per]
            tiles, miss = [], 0
            for clip, t in chunk:
                im, lab = grab(clip, t), f"{clip}  {t:.1f}s"
                if im is None:
                    im = Image.new("RGB", (TILE_W, 360), (40, 40, 40))
                    lab, miss = lab + "  ⚠️取れず", miss + 1
                tiles.append((im.resize((TILE_W, max(1, round(TILE_W * im.height / im.width))),
                                        Image.LANCZOS), lab))
            th = max(im.height for im, _ in tiles)
            sh = Image.new("RGB", (TILE_W * COLS, (th + BAR) * ROWS), (16, 16, 16))
            d = ImageDraw.Draw(sh)
            for i, (im, lab) in enumerate(tiles):
                x, y = (i % COLS) * TILE_W, (i // COLS) * (th + BAR)
                sh.paste(im, (x, y + BAR))
                d.text((x + 6, y + 6), lab, fill=(255, 220, 120))
            p = OUT / f"mix_{page + 1:02d}.jpg"
            sh.save(p, quality=92)
            print(f"  {'⚠️' if miss else '✓'} {p.relative_to(HERE)}  "
                  f"({len(chunk)}枚中 取れず {miss})")
        return
    a.secs = [float(s) for s in a.secs]
    if a.mode == "shots":
        sh = SHOTS[a.clip]["shots"]
        items = [(round((s["start"] + s["until"]) / 2, 1),
                  f"#{i:02d}  {s['start']:.0f}-{s['until']:.0f}s  "
                  f"mid {(s['start'] + s['until']) / 2:.1f}s  motion {s['motion']}")
                 for i, s in enumerate(sh)]
        sheet(a.clip, items, "sh")
    elif a.mode == "at":
        sheet(a.clip, [(t, f"{t:.1f}s") for t in a.secs], "at")
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        x0, y0, x1, y1 = (float(v) for v in a.box.split(","))
        for t in a.secs:
            im = grab(a.clip, t)
            if im is None:
                continue
            w, h = im.size
            im = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
            if a.scale != 1.0:
                im = im.resize((int(im.width * a.scale), int(im.height * a.scale)),
                               Image.LANCZOS)
            p = OUT / f"{a.clip}_crop_{t:.0f}.png"
            im.save(p)
            print(f"  ✓ {p.relative_to(HERE)}  {im.size}")


if __name__ == "__main__":
    main()
