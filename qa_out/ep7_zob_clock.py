# -*- coding: utf-8 -*-
"""ep7_zob_clock.py — ZOB-ARTCC の画面収録の**どの秒が何時なのか**を OCR で当てる。

■ なぜ要るか
    `footage.USE` に秒を書くには「その秒の画面が、話のどの時点か」が要る。
    ZOB-ARTCC は 613〜1,514秒の**連続した1ショット**なので、ショットの境目からは
    何も分からない。**当てずっぽうで秒を書いてはいけない**
    （[[feedback-measure-the-source-before-choosing-the-crop]]）。
    → レーダー卓の画面には時刻の表示が焼き込まれているはずなので、
      一定間隔でコマを取り、OCR で `hh:mm` を拾って**秒 → 時刻**の対応を作る。

■ ⚠️ OCR は `powershell.exe`（Windows PowerShell 5.1）。`pwsh` は WinRT を読めず
   **全ページ null のまま exit 0**。受け取りは**バイト**で（cp932 で書かれる）。

■ 使い方
    python qa_out/ep7_zob_clock.py grab --clip=<鍵> --step=60
    python qa_out/ep7_zob_clock.py ocr  --clip=<鍵>
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import footage as F                                            # noqa: E402

DIR = HERE / "out" / "ep7_zob"
OCR_PS1 = HERE / "tools" / "ocr_win.ps1"
CLOCK = re.compile(r"(\d{1,2})\s*[:：]\s*(\d{2})(?:\s*[:：]\s*(\d{2}))?")


def _dec(b):
    for enc in ("utf-8", "cp932", "mbcs"):
        try:
            return b.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return b.decode("utf-8", errors="replace")


def cmd_grab(clip, step):
    c = F.CLIPS[clip]
    DIR.mkdir(parents=True, exist_ok=True)
    stem = clip.rsplit(".", 1)[0]
    secs = list(range(0, int(float(c["sec"])), step))
    print(f"■ {clip}  {c['sec']:.0f}秒 → {len(secs)}枚（{step}秒ごと）")
    vf = []
    if int(c.get("dispw") or c["w"]) != int(c["w"]):
        vf += ["scale=iw*sar:ih", "setsar=1"]
    ng = 0
    for s in secs:
        dest = DIR / f"{stem}__t{s:05d}.png"
        if dest.exists():
            continue
        cmd = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
               "-user_agent", F.UA, "-ss", f"{s}", "-i", c["url"], "-an",
               "-frames:v", "1", *(["-vf", ",".join(vf)] if vf else []), str(dest)]
        p = subprocess.run(cmd, capture_output=True, timeout=900)
        if p.returncode != 0 or not dest.exists():
            print(f"  🔴 {s}秒: {_dec(p.stderr or b'')[-120:]}", flush=True); ng += 1
        else:
            print(f"  ✓ {s}秒", flush=True)
    return 2 if ng else 0


def cmd_ocr(clip):
    stem = clip.rsplit(".", 1)[0]
    pngs = sorted(DIR.glob(f"{stem}__t*.png"))
    if not pngs:
        print("🔴 コマが無い。まず grab"); return 2
    out, got = [], 0
    for i in range(0, len(pngs), 30):
        part = pngs[i:i + 30]
        p = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", str(OCR_PS1), "-Files", ",".join(str(x) for x in part)],
            capture_output=True, timeout=1800)
        out.append(_dec(p.stdout or b""))
    txt = "\n".join(out)
    cur = None
    print(f"{'秒':>7}  拾えた時刻（OCR）")
    for ln in txt.splitlines():
        if ln.startswith("##"):
            cur = Path(ln.split()[1]).name
            got += 1
            sec = int(re.search(r"__t(\d+)\.png$", cur).group(1))
            print(f"{sec:>7}  ", end="")
            hits = []
        elif cur and ln.startswith("["):
            body = ln.split("] ", 1)[-1]
            for m in CLOCK.finditer(body.replace(" ", "")):
                h, mi = int(m.group(1)), int(m.group(2))
                if 0 <= h <= 23 and 0 <= mi <= 59:
                    hits.append(m.group(0))
            if ln is not None:
                pass
        if ln.startswith("##") is False and cur and ln == "":
            pass
    # ⚠️ 上の逐次印字は読みにくいので、まとめ直して出す
    print("\n── まとめ ──")
    blocks = txt.split("## ")
    for b in blocks[1:]:
        head, *rest = b.splitlines()
        name = Path(head.split()[0]).name
        m = re.search(r"__t(\d+)\.png$", name)
        if not m:
            continue
        sec = int(m.group(1))
        body = " ".join(r.split("] ", 1)[-1] for r in rest if r.startswith("["))
        flat = body.replace(" ", "")
        hits = sorted({mm.group(0) for mm in CLOCK.finditer(flat)
                       if 0 <= int(mm.group(1)) <= 23 and 0 <= int(mm.group(2)) <= 59})
        print(f"  {sec:>5}秒  {'／'.join(hits[:8]) if hits else '（時刻なし）'}"
              f"    {body[:90]}")
    print(f"\n■ 読めた {got}/{len(pngs)}枚")
    return 0 if got == len(pngs) else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["grab", "ocr"])
    ap.add_argument("--clip", required=True)
    ap.add_argument("--step", type=int, default=60)
    a = ap.parse_args()
    return cmd_grab(a.clip, a.step) if a.cmd == "grab" else cmd_ocr(a.clip)


if __name__ == "__main__":
    sys.exit(main())
