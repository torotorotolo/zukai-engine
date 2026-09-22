# -*- coding: utf-8 -*-
"""12本目②：NARA の「系列（series）を丸ごと」数える。

①の罠は全文検索が別物を返すことだった。系列を名指しで歩けば、
**その系列に何点あるか**は検索語の当たり外れと無関係に数えられる。

対象＝RG 374（国防脅威削減局 DTRA）の
  Series: Photographs of Atmospheric Nuclear Testing at Pacific Island and Nevada Test Sites
  File Unit: PROJECT 22 - OPERATION CASTLE (Bikini/Enewetak) Detonation / Test Activities

使い方: python ref/ep12/probe_nara_series.py <naId> [出力名]
        python ref/ep12/probe_nara_series.py find "<題の一部>"   # naId を探す
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


def api(**params):
    params.setdefault("limit", 100)
    r = requests.get(URL, params=params, headers={"User-Agent": UA}, timeout=90)
    ct = r.headers.get("content-type", "")
    if "application/json" not in ct:
        raise SystemExit("🔴 JSON でない応答（content-type=%s）＝止める" % ct)
    return r.json()


def hits(d):
    return ((d.get("body") or d).get("hits", {}) or {})


def find(q):
    d = api(q=q, limit=50)
    h = hits(d)
    print("総数", h.get("total", {}).get("value"))
    for it in h.get("hits") or []:
        rec = (it.get("_source") or {}).get("record") or {}
        print("%-10s %-14s %s" % (rec.get("naId"), rec.get("levelOfDescription"),
                                  rec.get("title", "")[:100]))


def walk(parent):
    """⚠️ NARA は知らない絞り込みの引数を**黙って無視する**（200 で JSON が返る）。
    無視されると総数がカタログ全体（2,500万件）になるので、**そこで止める**。
    → [[feedback-parsers-fail-closed]]／[[feedback-gates-go-stale-when-upstream-changes]]"""
    rows, page = [], 1
    while page <= 30:
        d = api(q="*", ancestorNaId=parent, limit=100, page=page)
        h = hits(d)
        total = (h.get("total") or {}).get("value")
        if total and total > 5000:
            raise SystemExit(
                "🔴 絞り込みが効いていない（総数 %s）＝引数 ancestorNaIds が無視された。止める"
                % total)
        items = h.get("hits") or []
        if not items:
            break
        for it in items:
            rec = (it.get("_source") or {}).get("record") or {}
            objs = rec.get("digitalObjects") or []
            rows.append({
                "naId": rec.get("naId"),
                "level": rec.get("levelOfDescription"),
                "title": rec.get("title", ""),
                "scope": (rec.get("scopeAndContentNote") or "")[:400],
                "types": rec.get("generalRecordsTypes") or [],
                "objects": [{"type": o.get("objectType"),
                             "url": o.get("objectUrl"),
                             "bytes": o.get("byteSize"),
                             "desc": o.get("objectDescription", "")} for o in objs],
            })
        print("  page %d  取得 %d / 総数 %s" % (page, len(rows), total))
        if total and len(rows) >= total:
            break
        page += 1
        time.sleep(1.0)
    return rows


if __name__ == "__main__":
    if sys.argv[1] == "find":
        find(sys.argv[2])
    else:
        naid = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else naid
        rows = walk(naid)
        (OUT / ("nara_%s.json" % name)).write_text(
            json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        n_obj = sum(len(r["objects"]) for r in rows)
        print("== %s: レコード %d件 / デジタル物 %d点" % (name, len(rows), n_obj))
