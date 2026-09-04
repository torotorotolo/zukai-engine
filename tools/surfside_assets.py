# -*- coding: utf-8 -*-
"""surfside_assets.py — 4本目（サーフサイド）の素材を1点ずつ実測する（2026-09-04）。

■ なぜ要るか
    ②素材でいちばん多く候補が落ちる。**枚数を実際に数える**のが規則
    （「報告書があるはず」で企画を通さない）。

■ 何を数えるか
    NIST の Champlain Towers South 調査ページに出ている画像を**全点**取り、
      - 幅・高さ・色（全画面に耐えるか＝幅1280px以上かつ連続階調）
      - 🔴 **撮影時期で「現場」と「試験・調査」に分ける**
        現場＝2021-06/07（崩落直後の現地）／それ以降＝研究所での試験・部材・会議
    に仕分ける。
    ⚠️ 「その写真が、そのカットで話している対象そのものであること」は維持する規則なので、
    　 **試験の写真を崩落の章に敷くことはできない**。だから分けて数える。

■ 使い方
    python tools/surfside_assets.py nist
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

import requests
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
OUT = HERE / "analytics" / "materials"
UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com)")
PAGES = [
    "https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse/news-and-updates",
    "https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse",
]
FULL_W = 1280
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA})

# 画像URLに埋まっている日付（/images/YYYY/MM/DD/）で現場と試験を分ける
DATE_RE = re.compile(r"/images/(\d{4})/(\d{2})/(\d{2})/")
ONSITE_MONTHS = {("2021", "06"), ("2021", "07"), ("2021", "08")}


def collect_urls():
    urls = set()
    for p in PAGES:
        r = SESSION.get(p, timeout=45)
        r.raise_for_status()
        for u in re.findall(r"https?://[^\"'\s>]+?\.(?:jpg|jpeg|png|JPG|JPEG|PNG)", r.text):
            if "nist_mark" in u or "/themes/" in u:
                continue
            urls.add(u)
        time.sleep(0.5)
    return sorted(urls)


def measure(url):
    r = SESSION.get(url, timeout=60)
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content))
    w, h = im.size
    m = DATE_RE.search(url)
    ym = (m.group(1), m.group(2)) if m else ("?", "?")
    return {
        "url": url, "name": unquote(url.split("/")[-1]),
        "w": w, "h": h, "mode": im.mode,
        "bytes": len(r.content),
        "date": f"{ym[0]}-{ym[1]}" if m else "不明",
        "onsite": ym in ONSITE_MONTHS,
        "fullscreen": w >= FULL_W and im.mode != "1",
        "landscape": w >= h,
    }


def cmd_nist(a) -> int:
    urls = collect_urls()
    print(f"[NIST] 画像URL {len(urls)} 種。全点を実測します")
    rows = []
    for i, u in enumerate(urls, 1):
        try:
            rows.append(measure(u))
        except Exception as e:      # noqa: BLE001
            print(f"  🔴 {i}/{len(urls)} 取得できず: {u[-46:]} {e}")
            continue
        if i % 20 == 0:
            print(f"  …{i}/{len(urls)}")
        time.sleep(0.25)

    full = [r for r in rows if r["fullscreen"]]
    onsite = [r for r in full if r["onsite"]]
    lab = [r for r in full if not r["onsite"]]
    wide = [r for r in full if r["landscape"]]
    by_date = Counter(r["date"] for r in rows)

    print(f"\n===== NIST サーフサイド 画像の実測 =====")
    print(f"  総点数 {len(rows)}")
    print(f"  🔴 全画面に耐える（幅>={FULL_W}・連続階調）: **{len(full)}点**")
    print(f"     うち **現場（2021年6〜8月）= {len(onsite)}点** ／ 試験・調査 = {len(lab)}点")
    print(f"     うち 横長（16:9に素直に入る）= {len(wide)}点")
    print(f"  撮影時期の内訳: {dict(sorted(by_date.items()))}")
    print(f"\n  {'幅x高':>11}  {'時期':<8} {'現場':<4} 題")
    for r in sorted(full, key=lambda x: (not x["onsite"], x["date"]))[:16]:
        print(f"  {str(r['w']) + 'x' + str(r['h']):>11}  {r['date']:<8} "
              f"{'現場' if r['onsite'] else '試験':<4} {r['name'][:52]}")

    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "nist_surfside.json"
    p.write_text(json.dumps(
        {"total": len(rows), "fullscreen": len(full), "onsite": len(onsite),
         "lab": len(lab), "landscape": len(wide), "rows": rows},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n保存: {p.relative_to(HERE)}")
    print("⚠️ 出どころは NIST（米連邦機関）。職務著作はPDだが、"
          "**外部から提供された写真は権利が別**なので、使う前に1点ずつ出典表示を見ること")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="サーフサイドの素材を実測する")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("nist", help="NIST の画像を全点測る")
    p.set_defaults(fn=cmd_nist)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
