# 指定カテゴリ（下位2段まで）のファイルの目録＝撮影日・幅高・ライセンス・作者（画像は落とさない）
import json, sys, time, re, urllib.request, urllib.parse
UA = {"User-Agent": "zukai-engine-research/1.0 (GitHub torotorotolo)"}
def q(**kw):
    kw["format"] = "json"
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(kw)
    for i in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:
            print("ERR", e, file=sys.stderr); time.sleep(15 * (i + 1))
    raise SystemExit("API failed")
def subcats(cat):
    r = q(action="query", list="categorymembers", cmtitle=cat, cmtype="subcat", cmlimit=500)
    return [m["title"] for m in r["query"]["categorymembers"]]
def files(cat):
    out, cont = [], {}
    while True:
        r = q(action="query", generator="categorymembers", gcmtitle=cat, gcmtype="file", gcmlimit=50,
              prop="imageinfo", iiprop="size|extmetadata|mime", iiextmetadatafilter="DateTimeOriginal|LicenseShortName|Artist|ImageDescription", **cont)
        for p in r.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [{}])[0]; em = ii.get("extmetadata", {})
            g = lambda k: re.sub(r"<[^>]+>", "", em.get(k, {}).get("value", ""))[:80].replace("\t", " ").replace("\n", " ")
            out.append((p["title"], ii.get("width", 0), ii.get("height", 0), ii.get("mime", ""), g("DateTimeOriginal"), g("LicenseShortName"), g("Artist")))
        if "continue" not in r: return out
        cont = {"gcmcontinue": r["continue"]["gcmcontinue"], "continue": r["continue"]["continue"]}; time.sleep(2)
roots = sys.argv[1:]
seen = set(); rows = []
frontier = [(c, 0) for c in roots]
while frontier:
    c, d = frontier.pop(0)
    if c in seen: continue
    seen.add(c)
    fs = files(c); time.sleep(2)
    for f in fs: rows.append((c,) + f)
    print("%d\t%d\t%s" % (d, len(fs), c), file=sys.stderr, flush=True)
    if d < 2:
        for s in subcats(c): frontier.append((s, d + 1))
        time.sleep(2)
dedup = {}
for r in rows: dedup.setdefault(r[1], r)
for r in dedup.values(): print("\t".join(str(x) for x in r))
print("FILES", len(dedup), "CATS", len(seen), file=sys.stderr)
