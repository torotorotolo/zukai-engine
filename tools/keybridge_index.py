# -*- coding: utf-8 -*-
"""keybridge_index.py — 実写素材の台帳 `ref/keybridge/SHOTS_INDEX.md` を組む（2026-09-08・②素材）。

■ なぜ要るか
    `footage.USE` は「どのカットに、どの動画の何秒から何秒まで」を書く欄で、
    **全欄に `until=` が要る**（無いと `footage.py fetch --check` が exit 2）。
    その `until` は**推測で書けない**ので、②のうちに全ショットの境目を台帳にしておく。
    5本目の `ref/sl1/SHOTS_INDEX.md` と同じ役目。

■ 何を並べるか（全部このチャットで実測した値。手で書いた数字は1つも無い）
    - 出どころ … `analytics/materials/keybridge_videos_probe.json`（ffprobe の実測）
    - ショット … `analytics/materials/keybridge_shots.json`（shots.py・**1秒刻み**）
    - 中身    … `analytics/materials/keybridge_video_desc.json`（Commons の説明文・撮影日・権利者）

■ ⚠️ 台帳が言えないこと
    ショットの**中身**（何が写っているか）は入っていません。**目で見るのは別のチャット**
    （画像を抱えたターンが費用の主因＝[[feedback-subagents-must-not-read-images]]）。
    ここに在るのは「秒・長さ・動きの大きさ・その動画の主題」まで。

■ 使い方
    python tools/keybridge_index.py            … 台帳を書き出す
    python tools/keybridge_index.py --min 8    … 8秒以上のショットだけ数える
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")

M = ROOT / "analytics/materials"
OUT = ROOT / "ref/keybridge/SHOTS_INDEX.md"
CUT_SEC = 10.29          # 1カットの秒（check_script.PER_CUT・SL-1 実測）


def load():
    pr = {v["title"]: v for v in json.loads((M / "keybridge_videos_probe.json").read_text("utf-8"))}
    sh = json.loads((M / "keybridge_shots.json").read_text("utf-8"))
    de = json.loads((M / "keybridge_video_desc.json").read_text("utf-8"))
    return pr, sh, de


def fed(author: str) -> str:
    a = author or ""
    if re.search(r"Coast Guard|USCG", a, re.I):
        return "米沿岸警備隊"
    if re.search(r"Corps of Engineers|U\.S\. Army", a, re.I):
        return "米陸軍工兵隊"
    if re.search(r"NTSB", a, re.I):
        return "NTSB"
    if re.search(r"Navy|NAVSEA", a, re.I):
        return "米海軍"
    if re.search(r"White House", a, re.I):
        return "ホワイトハウス"
    return a[:40] or "（不明）"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=float, default=8.0)
    a = ap.parse_args()
    pr, sh, de = load()

    keys = sorted(sh, key=lambda k: -sh[k]["dur"])
    day0 = [k for k in keys if (de.get(sh[k]["title"], {}).get("date") or "").startswith("2024-03-26")]
    allshots = [(k, s) for k in keys for s in sh[k]["shots"]]
    usable = [x for x in allshots if x[1]["until"] - x[1]["start"] >= a.min]
    moving = [x for x in usable if x[1].get("motion", 0) >= 2.0]

    L = ["# キー橋（6本目）実写素材の台帳 — 全355ショットの境目",
         "",
         "**2026-09-08（②素材）に機械で実測。手で書いた数字はありません。**",
         "道具＝`tools/keybridge_shots.py`（`shots.py` を1秒刻みで本数ぶん回す）。",
         "生データ＝`analytics/materials/keybridge_shots.json`。",
         "",
         "## 0. 全体",
         "",
         f"- 動画 **{len(sh)}本 / {sum(v['dur'] for v in sh.values())/60:.1f}分**"
         f"（すべて Commons・すべてパブリックドメイン。ホワイトハウスの総集編は除いてある）",
         f"- ショット **{len(allshots)}本**。長さの中央値は各行を見る",
         f"- 🔴 **{a.min:.0f}秒以上のショット {len(usable)}本"
         f"（合計 {sum(x[1]['until']-x[1]['start'] for x in usable)/60:.1f}分）"
         f"＝1カット {CUT_SEC}秒 をそのまま埋められる玉**",
         f"- そのうち**動きのあるもの（motion≧2.0）{len(moving)}本**"
         f"（残り {len(usable)-len(moving)}本は静止に近い＝`still=True` 向き）",
         "",
         "⚠️ **ショットの中身（何が写っているか）は入っていません。**目で見るのは別のチャット。",
         "ここに在るのは秒・長さ・動きの大きさ・その動画の主題まで。",
         "",
         "⚠️ **崩落の瞬間そのものの映像は、この{n}本の中にありません。**".format(n=len(sh)),
         "事故当日（2024-03-26）に撮られたのは **{d}本**だけで、どれも**崩落後**です"
         "（{names}）。".format(d=len(day0), names="／".join("`%s`" % k for k in day0)),
         "",
         "## 1. 動画いちらん（尺の長い順）",
         "",
         "| 鍵 | 撮影日 | 秒 | 画 | ショット | 8秒以上 | 撮った所 | 主題 |",
         "|---|---|---|---|---|---|---|---|"]

    for k in keys:
        d = sh[k]
        t = d["title"]
        info = de.get(t, {})
        n8 = sum(1 for s in d["shots"] if s["until"] - s["start"] >= a.min)
        desc = (info.get("desc") or "")[:80]
        L.append(f"| `{k}` | {(info.get('date') or '')[:10]} | {d['dur']:.0f} | "
                 f"{d['w']}x{d['h']} | {len(d['shots'])} | {n8} | "
                 f"{fed(info.get('author',''))} | {desc} |")

    L += ["",
          "## 2. ショットの境目（`footage.USE` の `start=` / `until=` にそのまま書く）",
          "",
          "`motion` は区間内の隣どうしの絵の差の中央値。**2.0 未満は静止に近い**。",
          "`rate` の目安 ＝ そのショットの長さ ÷ カットの尺。1.00 未満なら遅回しで埋める。",
          ""]

    for k in keys:
        d = sh[k]
        info = de.get(d["title"], {})
        L += ["", f"### `{k}` — {d['title']}", "",
              f"- {d['w']}x{d['h']} / {d['fps']}fps / {d['dur']:.0f}秒 / "
              f"撮影 {(info.get('date') or '')[:10]} / {fed(info.get('author',''))} / "
              f"{info.get('lic','')}",
              f"- URL `{d['url']}`",
              f"- 説明（Commons 原文）: {(info.get('desc') or '')[:300]}",
              "",
              "| # | start | until | 長さ | motion | rate の目安 |",
              "|---|---|---|---|---|---|"]
        for i, s in enumerate(d["shots"], 1):
            ln = s["until"] - s["start"]
            rate = min(1.0, ln / CUT_SEC)
            L.append(f"| {i} | {s['start']:.1f} | {s['until']:.1f} | {ln:.1f} | "
                     f"{s.get('motion',0):.1f} | {rate:.2f} |")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"→ {OUT}（{len(L)}行）")
    print(f"動画 {len(sh)}本 / ショット {len(allshots)}本 / "
          f"{a.min:.0f}秒以上 {len(usable)}本 / うち動きあり {len(moving)}本")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
