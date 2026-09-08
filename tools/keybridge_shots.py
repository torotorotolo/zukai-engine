# -*- coding: utf-8 -*-
"""keybridge_shots.py — 6本目（キー橋）の PD 動画を **1秒刻み**でショットに割る（2026-09-08・②素材）。

■ なぜ要るか
    5本目までは記録映像が1本だったので `shots.py probe <1本>` で足りた。
    6本目は Commons だけで **29本**あり、しかも DVIDS の B-roll なので
    「1本の中に別の場所・別の日のショートカットが並ぶ」。**本数ぶん回す口**が要る。
    → 3秒刻みの見取り図では中身が別物になる（[[feedback-measure-the-source-before-choosing-the-crop]]）

■ ⚠️ 落とさない
    `shots.py` に URL をそのまま渡す（`-user_agent` 付き）。C: に 4.5GB を置かないため。
    ⚠️ Commons は名乗らないと 429。UA は shots.UA / footage.UA と同じ。

■ 使い方
    python tools/keybridge_shots.py --skip "White House"    … 全部（既定・約30〜60分）
    python tools/keybridge_shots.py --only 6                … 尺の長い順に6本だけ
    python tools/keybridge_shots.py --show                  … 出た結果を読む
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import shots  # noqa: E402

SRC = ROOT / "analytics/materials/keybridge_videos_probe.json"
OUT = ROOT / "analytics/materials/keybridge_shots.json"


def key_of(title: str) -> str:
    """DVIDS の識別子（240407-A-PA223-1003）があればそれ、無ければ題名を詰める。"""
    import re
    m = re.search(r"\((\d{6}-[A-Z]-[A-Z0-9]+-\d+)\)", title)
    if m:
        return m.group(1)
    return re.sub(r"[^A-Za-z0-9]+", "_", title)[:40].strip("_")


def run(only, skip, force):
    vids = json.loads(SRC.read_text(encoding="utf-8"))
    vids = [v for v in vids if not any(s.lower() in v["title"].lower() for s in skip)]
    vids.sort(key=lambda v: -v["sec"])
    if only:
        vids = vids[:only]
    res = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for i, v in enumerate(vids, 1):
        k = key_of(v["title"])
        if k in res and not force:
            print(f"[{i}/{len(vids)}] 済 {k}")
            continue
        t0 = time.time()
        try:
            sh, dur = shots.shots_of(v["url"])
        except Exception as e:                                  # noqa: BLE001
            print(f"[{i}/{len(vids)}] 🔴 {k}: {type(e).__name__}: {e}", flush=True)
            continue
        res[k] = dict(src=v["title"], title=v["title"], url=v["url"],
                      w=v["w"], h=v["h"], fps=v["fps"],
                      dur=round(dur, 2), shots=sh)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[{i}/{len(vids)}] {k} {v['sec']:.0f}秒 → ショット {len(sh)}本 "
              f"（中央値 {_med([s['until']-s['start'] for s in sh]):.1f}秒／"
              f"{time.time()-t0:.0f}秒かかった）", flush=True)
    show(res)


def _med(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else 0.0


def show(res=None):
    res = res or json.loads(OUT.read_text(encoding="utf-8"))
    tot_s = tot_n = 0
    still = 0
    print(f"\n{'鍵':22s} {'尺':>7s} {'本':>4s} {'中央値':>7s} {'静止ぎみ':>8s}  題")
    for k, d in sorted(res.items(), key=lambda x: -x[1].get("dur", 0)):
        sh = d.get("shots", [])
        ln = [s["until"] - s["start"] for s in sh]
        st = sum(1 for s in sh if s.get("motion", 99) < 2.0)
        tot_s += d.get("dur", 0)
        tot_n += len(sh)
        still += st
        print(f"{k:22s} {d.get('dur',0):7.0f} {len(sh):4d} {_med(ln):7.1f} {st:8d}  {d.get('title','')[:44]}")
    print(f"\n合計 {tot_s:.0f}秒 = {tot_s/60:.1f}分 / ショット {tot_n}本 / 静止ぎみ {still}本")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int, default=0)
    ap.add_argument("--skip", nargs="*", default=["White House"])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--show", action="store_true")
    a = ap.parse_args()
    if a.show:
        show()
        return 0
    run(a.only, a.skip, a.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
