# -*- coding: utf-8 -*-
"""19本目 ⑤b-1：記録映像の1秒1コマの走査と、区間を選ぶための見取り図（2026-10-06）。

■ 何をするか
    probe   … 走査用の版（`out/jiko/foot/ep19_scan/<記号>.mp4`・1080）を `tools/shots.shots_of` に通し、
              ショットの境目を `ref/ep19/shots.json` に書く（秒はどの版でも同じ＝Kaltura の flavor は同じ尺）
    shots   … ショットごとに真ん中の1コマ（640px）を2列×3行に並べた見取り図＝「どのショットに何が写るか」
    sec     … 秒の窓を1秒ごと（`--step` で細かく）に640px で2列×3行＝区間の中で絵が替わらないか・人や字が入らないか
    ⚠️ 見取り図は `scratchpad/scan19/` に書き、作った枚は `ref/ep19/v1_build/tools19/seen19.tsv` に機械で足す
       （作った枚は全部読む＝見た枚と同じ。読まない枚は作らない）

■ 使い方
    python qa_out/ep19_scan.py probe
    python qa_out/ep19_scan.py shots B2 [--from 0] [--n 6]
    python qa_out/ep19_scan.py sec B2 8 14 [--step 1]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import shots as SH  # noqa: E402

SCAN = HERE / "out" / "jiko" / "foot" / "ep19_scan"
SHOTS_JSON = HERE / "ref" / "ep19" / "shots.json"
SEEN = HERE / "ref" / "ep19" / "v1_build" / "tools19" / "seen19.tsv"
STOCK_JSON = HERE / "ref" / "stock" / "stock.json"
OUT = Path(os.environ.get("SCAN19_OUT", r"C:\Users\konar\AppData\Local\Temp\claude\C--Users-konar-Documents-Obsidian-Vault\bf956a18-0a74-480b-8c62-9ded79d59f31\scratchpad\scan19"))
KAL = "https://cdnapisec.kaltura.com/p/684682/sp/68468200/playManifest/entryId/{e}/format/url/protocol/https/flavorParamId/0"
TILE = 640
COLS, ROWS = 2, 3


def _font(sz):
    for f in (r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\msgothic.ttc"):
        if Path(f).exists():
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def _src(clip):
    """記録映像は走査の版・フリー素材（S#n）は棚の media"""
    if clip.startswith("S#"):
        for k, v in json.loads(STOCK_JSON.read_text(encoding="utf-8")).items():
            if v.get("code19") == clip:
                return STOCK_JSON.parent / "media" / f"{k}.mp4"
        raise SystemExit(f"🔴 棚に {clip} が無い")
    return SCAN / f"{clip}.mp4"


def grab(clip, t):
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", str(_src(clip)),
                        "-frames:v", "1", "-vf", f"scale={TILE}:-2", "-f", "image2pipe", "-vcodec", "png", "-"],
                       capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise SystemExit(f"🔴 {clip} {t:.2f}秒のコマが取れない: {p.stderr.decode('utf-8', 'replace')[:300]}")
    from io import BytesIO
    return Image.open(BytesIO(p.stdout)).convert("RGB")


def sheet(clip, items, name, note):
    """items＝[(秒, 札)]・6枚まで。作った枚は seen19.tsv に足す。"""
    tiles = [(grab(clip, t), lab) for t, lab in items]
    th = max(im.height for im, _ in tiles)
    canvas = Image.new("RGB", (TILE * COLS, (th + 34) * ROWS), (20, 20, 20))
    d = ImageDraw.Draw(canvas)
    f = _font(22)
    for i, (im, lab) in enumerate(tiles):
        x, y = (i % COLS) * TILE, (i // COLS) * (th + 34)
        d.text((x + 8, y + 4), lab, fill=(255, 230, 120), font=f)
        canvas.paste(im, (x, y + 34))
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{name}.jpg"
    canvas.save(dst, quality=88)
    _seen(dst, name, note + "（チャット6・⑤b-1 走査）")


def _seen(dst, name, note):
    lines = SEEN.read_text(encoding="utf-8").splitlines()
    n = sum(1 for ln in lines if ln and not ln.startswith("#")) + 1
    with SEEN.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{n}\t{name}\t{note}\n")
    print(f"{dst}  ＝見た枚 {n}")


PHOTO = HERE / "ref" / "ep19" / "photo"


def _photo(key):
    v = json.loads((PHOTO / "fetched.json").read_text(encoding="utf-8"))[key]
    return v["file"], Image.open(PHOTO / v["file"]).convert("RGB")


def cmd_photo(key, edge=1600):
    """写真の全体を長辺 edge に（読む側の上限に合わせる）。細部は crop で原寸を切り出す。"""
    fn, im = _photo(key)
    w, h = im.size
    s = min(1.0, edge / max(w, h))
    v = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    name = "ph_" + key.replace("#", "").replace(":", "")
    dst = OUT / f"{name}.jpg"
    v.save(dst, quality=90)
    _seen(dst, name, f"{key} {fn} {w}x{h} の全体（長辺{v.size[0] if w >= h else v.size[1]}px）（チャット6・⑤b-1 写真の全数）")
    return 0


def cmd_crop(key, x0, y0, x1, y1):
    """原寸の座標で切り出す（拡大しない）。"""
    fn, im = _photo(key)
    c = im.crop((x0, y0, x1, y1))
    name = "phc_" + key.replace("#", "").replace(":", "") + f"_{x0}_{y0}"
    dst = OUT / f"{name}.jpg"
    c.save(dst, quality=92)
    _seen(dst, name, f"{key} の原寸の切り出し ({x0},{y0})–({x1},{y1})（チャット6・⑤b-1 写真の全数）")
    return 0


def cmd_probe():
    fetched = json.loads((SCAN / "fetched.json").read_text(encoding="utf-8"))
    out = {}
    for k, v in fetched.items():
        shots, dur = SH.shots_of(SCAN / f"{k}.mp4")
        out[k] = dict(src=KAL.format(e=v["entry"]), scan=f"out/jiko/foot/ep19_scan/{k}.mp4", dur=round(dur, 1),
                      how="1秒1コマを tools/shots.boundaries（2026-10-06 ⑤b-1・走査の版＝flavorParamId 487091・秒は元の版と同じ）",
                      shots=shots)
        L = [s["until"] - s["start"] for s in shots]
        print(f"{k:4} {dur:7.0f}秒 ショット {len(shots):3} 本・最長 {max(L):.0f}秒・6秒以上 {sum(1 for x in L if x >= 6)}")
    SHOTS_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("→", SHOTS_JSON.relative_to(HERE).as_posix())
    return 0


def cmd_shots(clip, frm=0, n=6):
    sd = json.loads(SHOTS_JSON.read_text(encoding="utf-8"))[clip]["shots"]
    sel = list(enumerate(sd))[frm:frm + n]
    items = [((s["start"] + s["until"]) / 2, f"{clip} #{i} {s['start']:.0f}–{s['until']:.0f}s m{s['motion']}") for i, s in sel]
    sheet(clip, items, f"{clip}_shots_{frm:03d}", f"{clip} のショット #{sel[0][0]}〜#{sel[-1][0]} の真ん中")
    return 0


def cmd_sec(clip, a, b, step=1.0):
    ts, t = [], a
    while t <= b + 1e-6 and len(ts) < COLS * ROWS:
        ts.append(round(t, 2))
        t += step
    sheet(clip, [(x, f"{clip} {x:.2f}s") for x in ts], f"{clip}_sec_{a:06.2f}_{step:g}", f"{clip} の {a}〜{ts[-1]}秒（{step:g}秒刻み）")
    return 0


def cmd_stock(code, a, b):
    """フリー素材の使う区間を1秒1コマ（640px・2列×3行）で全部並べる＝字・顔・商標を探す（棚の ok_ranges の根拠）"""
    ts, t = [], a
    while t <= b + 1e-6:
        ts.append(round(t, 2))
        t += 1.0
    for i in range(0, len(ts), COLS * ROWS):
        part = ts[i:i + COLS * ROWS]
        sheet(code, [(x, f"{code} {x:.1f}s") for x in part], f"stk_{code[2:]}_{part[0]:05.1f}",
              f"フリー素材 {code} の {part[0]}〜{part[-1]}秒（1秒1コマ）")
    return 0


def cmd_fcrop(clip, t, x0, y0, x1, y1):
    """映像の1コマを原寸で切り出す（座標は元の画素）＝シートの疑いを確かめる"""
    OUT.mkdir(parents=True, exist_ok=True)
    name = f"fc_{clip.replace('#', '')}_{t:05.1f}_{x0}_{y0}"
    dst = OUT / f"{name}.jpg"
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(_src(clip)), "-frames:v", "1",
                        "-vf", f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0}", "-q:v", "2", str(dst)], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.decode("utf-8", "replace")[:300])
    _seen(dst, name, f"{clip} の {t}秒の原寸の切り出し ({x0},{y0})-({x1},{y1})（チャット6・⑤b-1 疑いの確かめ）")
    return 0


def cmd_fine(clip, a, b, fps=10):
    """窓の中を 1/fps 秒刻みで署名にし、隣どうしの距離の大きい順に出す（画像を見ずに境目の秒を詰める）。
    手持ちの B1 は 1秒刻みの境目が当てにならない（#4 の 30〜45秒の中に人の寄りとがれきの引きが混ざる）。"""
    import numpy as np
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}",
                        "-i", str(SCAN / f"{clip}.mp4"), "-vf", f"fps={fps},scale=64:36,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    buf = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(buf) // (64 * 36)
    sig = buf[:n * 64 * 36].reshape(n, 36, 64).astype(np.int16)
    d = np.abs(np.diff(sig, axis=0)).mean(axis=(1, 2))
    med = float(np.median(d))
    top = sorted(range(len(d)), key=lambda i: -d[i])[:4]
    print(f"{clip} {a}〜{b}秒 {n}コマ 距離の中央値 {med:.1f}・大きい順 " +
          "・".join(f"{a + (i + 1) / fps:.1f}s={d[i]:.1f}" for i in sorted(top)))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = {a[i][2:]: a[i + 1] for i in range(len(a)) if a[i].startswith("--")}
    pos = [x for i, x in enumerate(a) if not x.startswith("--") and not (i and a[i - 1].startswith("--"))]
    if pos[0] == "probe":
        sys.exit(cmd_probe())
    if pos[0] == "shots":
        sys.exit(cmd_shots(pos[1], int(opt.get("from", 0)), int(opt.get("n", 6))))
    if pos[0] == "sec":
        sys.exit(cmd_sec(pos[1], float(pos[2]), float(pos[3]), float(opt.get("step", 1))))
    if pos[0] == "photo":
        sys.exit(cmd_photo(pos[1], int(opt.get("edge", 1600))))
    if pos[0] == "crop":
        sys.exit(cmd_crop(pos[1], *map(int, pos[2:6])))
    if pos[0] == "fcrop":
        sys.exit(cmd_fcrop(pos[1], float(pos[2]), *map(int, pos[3:7])))
    if pos[0] == "stock":
        sys.exit(cmd_stock(pos[1], float(pos[2]), float(pos[3])))
    if pos[0] == "fine":
        sys.exit(cmd_fine(pos[1], float(pos[2]), float(pos[3])))
    raise SystemExit(__doc__)
