# 28本目 ② Commons の目録（画像は落とさない）＝語でファイルとカテゴリを引き、撮影日・幅高・ライセンス・作者を並べる
# 使い方: python -X utf8 ref/ep28/probe/commons_probe28.py <出力tsv> 語1 語2 ...
#   語が "Category:" で始まれば、そのカテゴリ（下位1段まで）のファイルを数える。ほかは名前空間6（ファイル）と14（カテゴリ）を全文検索
# ⚠️ Windows の端末は cp932＝必ず -X utf8 で回す（① で落ちた）。Commons は続けて聞くと429＝2秒ずつ空ける
import json, sys, time, re, urllib.request, urllib.parse
UA = {"User-Agent": "zukai-engine-research/1.0 (GitHub torotorotolo)"}
META = "DateTimeOriginal|LicenseShortName|Artist|ImageDescription"
def q(**kw):
    kw["format"] = "json"
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(kw)
    for i in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:
            print("ERR", e, file=sys.stderr); time.sleep(15 * (i + 1))
    raise SystemExit("API failed")
def rows_of(r, src):
    out = []
    for p in r.get("query", {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [{}])[0]; em = ii.get("extmetadata", {})
        g = lambda k: re.sub(r"<[^>]+>", "", em.get(k, {}).get("value", ""))[:90].replace("\t", " ").replace("\n", " ")
        out.append((src, p["title"], ii.get("width", 0), ii.get("height", 0), ii.get("mime", ""),
                    g("DateTimeOriginal"), g("LicenseShortName"), g("Artist"), g("ImageDescription")))
    return out
def search_files(term):
    out, cont = [], {}
    while True:
        r = q(action="query", generator="search", gsrsearch=term, gsrnamespace=6, gsrlimit=50,
              prop="imageinfo", iiprop="size|extmetadata|mime", iiextmetadatafilter=META, **cont)
        out += rows_of(r, "search:" + term)
        if "continue" not in r or len(out) >= 200: return out
        cont = dict(r["continue"]); time.sleep(2)  # 検索の続きは gsroffset（gsrcontinue ではない）
def search_cats(term):
    r = q(action="query", list="search", srsearch=term, srnamespace=14, srlimit=20)
    return [m["title"] for m in r.get("query", {}).get("search", [])]
def cat_files(cat):
    out, cont = [], {}
    while True:
        r = q(action="query", generator="categorymembers", gcmtitle=cat, gcmtype="file", gcmlimit=50,
              prop="imageinfo", iiprop="size|extmetadata|mime", iiextmetadatafilter=META, **cont)
        out += rows_of(r, cat)
        if "continue" not in r: return out
        cont = {"gcmcontinue": r["continue"]["gcmcontinue"], "continue": r["continue"]["continue"]}; time.sleep(2)
def subcats(cat):
    r = q(action="query", list="categorymembers", cmtitle=cat, cmtype="subcat", cmlimit=500)
    return [m["title"] for m in r["query"]["categorymembers"]]
dst, terms = sys.argv[1], sys.argv[2:]
rows, cats_found = [], []
for t in terms:
    if t.startswith("Category:"):
        todo = [t] + subcats(t); time.sleep(2)
        for c in todo:
            fs = cat_files(c); rows += fs; time.sleep(2)
            print("cat\t%d\t%s" % (len(fs), c), file=sys.stderr, flush=True)
    else:
        fs = search_files(t); rows += fs; time.sleep(2)
        cs = search_cats(t); cats_found += [(t, c) for c in cs]; time.sleep(2)
        print("term\t%d\t%s\tcats=%s" % (len(fs), t, " / ".join(cs[:8])), file=sys.stderr, flush=True)
dedup = {}
for r in rows: dedup.setdefault(r[1], r)
with open(dst, "w", encoding="utf-8") as f:
    f.write("src\ttitle\tw\th\tmime\tdate\tlicense\tartist\tdesc\n")
    for r in dedup.values(): f.write("\t".join(str(x) for x in r) + "\n")
print("FILES", len(dedup), "ROWS", len(rows), file=sys.stderr)
