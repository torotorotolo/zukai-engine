"""13本目②: 記録映像と NARA の静止画の当たり（1回で全部）。結果は scratchpad/footage13.json と標準出力。
- NARA: catalog proxy（鍵不要）で語ごとの件数と上位の題・日付・種類
- archive.org: advancedsearch（movies）で題・年・権利の欄
- Commons: 動画（video/*・application/ogg）の検索
"""
import json, time, urllib.parse, urllib.request

UA = "zukai-engine-research/0.1 (konariri8 research)"
OUT = r"C:/Users/konar/AppData/Local/Temp/claude/C--Users-konar-Documents-Obsidian-Vault/3febce82-d020-45c6-b4de-0b38ceece0fa/scratchpad/footage13.json"
res = {}


def get(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 * (k + 1)); continue
            return {"_err": f"HTTP {e.code}"}
        except Exception as e:
            return {"_err": f"{type(e).__name__}: {e}"}
    return {"_err": "429"}


# --- NARA
for q in ["DC-10", "DC-10 cargo door", "Turkish Airlines", "Ermenonville", "McDonnell Douglas DC-10", "DC-10 crash 1974",
          "American Airlines DC-10 Windsor", "cargo door decompression"]:
    js = get("https://catalog.archives.gov/proxy/records/search?" + urllib.parse.urlencode({"q": q, "limit": 50}))
    hits = (js.get("body") or {}).get("hits") or {}
    tot = (hits.get("total") or {}).get("value") if isinstance(hits.get("total"), dict) else hits.get("total")
    rows = []
    for h in hits.get("hits", []):
        rec = (h.get("_source") or {}).get("record") or {}
        rows.append({"naId": rec.get("naId"), "title": (rec.get("title") or "")[:140],
                     "level": rec.get("levelOfDescription"), "type": rec.get("generalRecordsTypes"),
                     "date": str(rec.get("productionDates") or rec.get("coverageStartDate") or "")[:80],
                     "access": rec.get("accessRestriction", {}).get("status") if isinstance(rec.get("accessRestriction"), dict) else None,
                     "objects": len(rec.get("digitalObjects") or [])})
    res["nara:" + q] = {"total": tot, "rows": rows, "err": js.get("_err")}
    print(f"NARA [{q}] total={tot} err={js.get('_err')}")
    for r in rows[:12]:
        print(f"   {r['naId']} {r['level']} {r['type']} obj={r['objects']} {r['date'][:30]} | {r['title'][:100]}")
    time.sleep(2)

# --- archive.org
for q in ['(title:"DC-10" OR description:"DC-10") AND mediatype:movies',
          '("Turkish Airlines" OR "Ermenonville") AND mediatype:movies',
          '(title:"McDonnell Douglas" OR title:"Douglas Aircraft") AND mediatype:movies AND year:[1968 TO 1980]',
          '("DC-10" OR "DC10") AND mediatype:image AND year:[1970 TO 1976]']:
    url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": q, "fl[]": ["identifier", "title", "year", "licenseurl", "rights", "mediatype"], "rows": 60, "output": "json"}, doseq=True)
    js = get(url)
    docs = (js.get("response") or {}).get("docs", [])
    res["ia:" + q] = {"n": (js.get("response") or {}).get("numFound"), "docs": docs, "err": js.get("_err")}
    print(f"IA [{q[:70]}] numFound={(js.get('response') or {}).get('numFound')} err={js.get('_err')}")
    for d in docs[:25]:
        print(f"   {d.get('year')} {d.get('identifier')[:50]} | {str(d.get('title'))[:80]} | {str(d.get('licenseurl') or d.get('rights') or '')[:50]}")
    time.sleep(2)

# --- Commons 動画
API = "https://commons.wikimedia.org/w/api.php"
for q in ['"DC-10" filetype:video', '"DC 10" filetype:video', 'Weeknummer 74-10', 'Weeknummer 74-11', 'Weeknummer 74-12',
          '"Parijs" vliegtuig 1974 filetype:video', '"Turkish Airlines" filetype:video', '"cargo door" filetype:video',
          'Ermenonville filetype:video', 'Orly 1974 filetype:video']:
    url = API + "?" + urllib.parse.urlencode({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6,
                                              "srlimit": 30, "format": "json", "formatversion": 2})
    js = get(url)
    rows = [s["title"] for s in (js.get("query") or {}).get("search", [])]
    res["commons:" + q] = rows
    print(f"COMMONS [{q}] {len(rows)}")
    for t in rows[:15]:
        print("   ", t[:120])
    time.sleep(2)

json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", OUT)
