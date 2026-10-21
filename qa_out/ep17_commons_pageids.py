# -*- coding: utf-8 -*-
"""17本目 ⑥：概要欄に出す Wikimedia Commons の頁を「番号の URL」（https://commons.wikimedia.org/?curid=…）にするため、
git の外の作者の表（`ref/ep17/src/credits_private.tsv`）の題名から頁の番号を API で1回引いて `qa_out/ep17_commons_pageids.json` に書く
（20本目 `ep20_commons_pageids.json` の型＝ルール 6-52：題名の %xx で字数がふくらまない）。

⚠️ 書くのは記号（表の code）・番号の URL・ライセンスだけ＝作者の名前と題名は書かない（リポは公開）。
⚠️ 道具の名乗り（User-Agent）にメールや「@」を入れない。

    python qa_out/ep17_commons_pageids.py
"""
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
TSV = HERE / "ref" / "ep17" / "src" / "credits_private.tsv"
OUT = HERE / "qa_out" / "ep17_commons_pageids.json"
UA = "zukai-engine-ep17-meta/1.0 (github.com/torotorotolo/zukai-engine)"
API = "https://commons.wikimedia.org/w/api.php"


def main():
    rows = [r for r in csv.reader(TSV.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    head = rows[0]
    recs = [dict(zip(head, r)) for r in rows[1:]]
    out, bad = {}, []
    for i in range(0, len(recs), 20):
        part = recs[i:i + 20]
        q = urllib.parse.urlencode({"action": "query", "format": "json", "formatversion": "2",
                                    "titles": "|".join("File:" + r["title"] for r in part)})
        req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as f:
            d = json.load(f)
        norm = {n["from"]: n["to"] for n in d["query"].get("normalized", [])}
        pid = {p["title"]: p.get("pageid") for p in d["query"]["pages"]}
        for r in part:
            t = "File:" + r["title"]
            p = pid.get(norm.get(t, t))
            if not p:
                bad.append(r["code"])
                continue
            out[r["code"]] = {"url": f"https://commons.wikimedia.org/?curid={p}", "license": r["license"]}
        time.sleep(1)
    if bad:
        raise SystemExit(f"🔴 頁の番号が取れない: {bad}。書かずに止めた。")
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(HERE)}（{len(out)} 点）")


if __name__ == "__main__":
    main()
