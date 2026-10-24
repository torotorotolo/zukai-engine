# -*- coding: utf-8 -*-
"""24本目 ⑥：概要欄に出す Wikimedia Commons の頁を「番号の URL」（https://commons.wikimedia.org/?curid=…）にするため、
写真の台帳（`ref/ep24/assets.json` の url＝Commons の頁）から頁の番号と分類（カテゴリ）を API で引いて `qa_out/ep24_commons_pageids.json` に書く
（17本目 `ep17_commons_pageids.py` の型＝ルール 6-52：題名の %xx で字数がふくらまない）。
🆕 24本目：IAEA Imagebank の写真（39点）は1点ずつ並べると概要欄の5,000字に入らない＝**全点が同じ分類に入るか**を API で照らし、
   入る分類を1つ選んで頁を出す（23本目 ⑥ の型＝BY-SA 68点を分類の頁で）。

⚠️ 書くのは記号（台帳の code）・番号の URL・ライセンス・分類の名だけ＝作者の名前は書かない（リポは公開）。
⚠️ 道具の名乗り（User-Agent）にメールや「@」を入れない。

    python qa_out/ep24_commons_pageids.py
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
ASSETS = HERE / "ref" / "ep24" / "assets.json"
OUT = HERE / "qa_out" / "ep24_commons_pageids.json"
UA = "zukai-engine-ep24-meta/1.0 (github.com/torotorotolo/zukai-engine)"
API = "https://commons.wikimedia.org/w/api.php"
PRE = "https://commons.wikimedia.org/wiki/"


def main():
    a = json.loads(ASSETS.read_text(encoding="utf-8"))
    recs = []
    for name, r in a.items():
        u = r.get("url") or ""
        if u.startswith(PRE + "File:"):
            recs.append((name, r["code"], urllib.parse.unquote(u[len(PRE):]).replace("_", " "), r.get("lic", "")))
    out, cats, bad = {}, {}, []
    for i in range(0, len(recs), 20):
        part = recs[i:i + 20]
        q = urllib.parse.urlencode({"action": "query", "format": "json", "formatversion": "2", "prop": "categories",
                                    "cllimit": "max", "titles": "|".join(t for _, _, t, _ in part)})
        req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as f:
            d = json.load(f)
        norm = {n["from"]: n["to"] for n in d["query"].get("normalized", [])}
        pages = {p["title"]: p for p in d["query"]["pages"]}
        for name, code, t, lic in part:
            p = pages.get(norm.get(t, t)) or {}
            if not p.get("pageid"):
                bad.append(code)
                continue
            out[name] = {"code": code, "url": f"https://commons.wikimedia.org/?curid={p['pageid']}", "license": lic}
            cats[name] = [c["title"] for c in p.get("categories", [])]
        time.sleep(1)
    if bad:
        raise SystemExit(f"🔴 頁の番号が取れない: {bad}。書かずに止めた。")
    # IAEA Imagebank の組（出典表記の頭が「写真：IAEA Imagebank」）が全部入る分類
    iaea = [n for n, r in a.items() if str(r.get("credit", "")).startswith("写真：IAEA Imagebank") and n in cats]
    common = set(cats[iaea[0]]) if iaea else set()
    for n in iaea[1:]:
        common &= set(cats[n])
    print(f"IAEA Imagebank の写真 {len(iaea)} 点が全部入る分類 {len(common)}：{sorted(common)}")
    OUT.write_text(json.dumps({"pages": out, "iaea_common_categories": sorted(common), "iaea": sorted(iaea)},
                              ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(HERE)}（{len(out)} 点）")


if __name__ == "__main__":
    main()
