# -*- coding: utf-8 -*-
"""12本目②：NARA を「題を1行ずつ読める形」で落とす。

なぜ要るか
  `tools/nara_probe.py` は**数**を出すが、保存する JSON に題が残るのは大きい順の10件だけ。
  ①が踏んだ罠（`Castle Bravo` で『Castle Rock (W 383)』が300点）は
  **題を読まないと見抜けない** → [[feedback-inventory-is-not-usable-material]]

⚠️ `limit` は列挙（1/10/20/50/100 だけ）。ほかを渡すと 200 のまま HTML が返る
   → content-type を必ず見る（[[feedback-parsers-fail-closed]]）
"""
import json
import sys
import time
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")

URL = "https://catalog.archives.gov/proxy/records/search"
UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com)")
OUT = Path("ref/ep12")

QUERIES = [
    "Operation Castle",
    "Operation CASTLE Bikini",
    "Bikini Atoll 1954 fallout",
    "Rongelap 1954",
    "Joint Task Force Seven Bikini",
    "Lucky Dragon fishing boat 1954",
]


def _status(v):
    """useRestriction は dict のことも str のこともある（型が揺れる）。"""
    if isinstance(v, dict):
        s = v.get("status")
        if isinstance(s, dict):
            return s.get("name")
        return s
    return v


def fetch(q, pages=3):
    rows = []
    for page in range(1, pages + 1):
        r = requests.get(URL, params={"q": q, "limit": 100, "page": page},
                         headers={"User-Agent": UA}, timeout=90)
        ct = r.headers.get("content-type", "")
        if "application/json" not in ct:
            raise SystemExit("🔴 JSON でない応答（content-type=%s）＝止める" % ct)
        d = r.json()
        hits = (d.get("body") or d).get("hits", {})
        items = hits.get("hits") or []
        if not items:
            break
        for h in items:
            rec = (h.get("_source") or {}).get("record") or {}
            rows.append({
                "naId": rec.get("naId"),
                "title": rec.get("title", ""),
                "types": rec.get("generalRecordsTypes") or [],
                "levelOfDescription": rec.get("levelOfDescription"),
                "recordGroup": (rec.get("recordGroupNumber")
                                or (rec.get("ancestors") or [{}])[0].get("title", "")),
                "ancestors": [a.get("title", "") for a in (rec.get("ancestors") or [])],
                "coverageStart": (rec.get("coverageStartDate") or {}).get("year"),
                "useRestriction": _status(rec.get("useRestriction")),
                "digital": len(rec.get("digitalObjects") or []),
                "objTypes": sorted({(o.get("objectType") or "")
                                    for o in (rec.get("digitalObjects") or [])}),
            })
        time.sleep(1.0)
    return rows


def main():
    all_rows = {}
    for q in QUERIES:
        rows = fetch(q)
        print("== %-35s %d件" % (q, len(rows)))
        for r in rows:
            r["via"] = q
            all_rows.setdefault(r["naId"], r)
    out = sorted(all_rows.values(), key=lambda r: -(r["digital"] or 0))
    (OUT / "nara_ep12.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    # 写真・記録映像のレコードだけを題で並べる
    print("\n===== 写真・記録映像のレコード（題を読む）=====")
    n = 0
    for r in out:
        t = " ".join(r["types"])
        if "Photograph" in t or "Moving" in t:
            n += 1
            print("%-9s %-22s 物%-4d %s | %s"
                  % (r["naId"], t[:22], r["digital"] or 0,
                     (r["useRestriction"] or "?")[:12], r["title"][:88]))
    print("--- 写真・記録映像のレコード %d件 / 全 %d件" % (n, len(out)))


if __name__ == "__main__":
    main()
