# 26本目 ②：Commons の素材の台帳（文字の情報だけ・絵は落とさない）。fetch＝カテゴリの中のファイルを説明・撮影日・権利つきで取る／list＝網を掛けて読む行に
# 使い方: python -P ref/ep26/probe/commons26.py fetch <出力.json> "Category:A" ...  ／  list <入力.json> <出力.tsv>
import html, json, re, sys, time, urllib.error, urllib.parse, urllib.request

UA = {"User-Agent": "zukai-engine-research/1.0 (ep26 materials)"}
API = "https://commons.wikimedia.org/w/api.php"
META = "DateTimeOriginal|LicenseShortName|ImageDescription|Artist|Credit|UsageTerms|Copyrighted|AttributionRequired"


def get(params):
    url = API + "?" + urllib.parse.urlencode(dict(params, format="json", formatversion=2))
    for n in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(8 * (n + 1))
                continue
            raise
    raise RuntimeError("429/503 が続いた")


def plain(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def fetch(out, cats):
    rows, seen = [], set()
    for cat in cats:
        cont, n = {}, 0
        while True:
            d = get(dict(action="query", generator="categorymembers", gcmtitle=cat, gcmtype="file", gcmlimit=50,
                         prop="imageinfo", iiprop="size|mime|extmetadata|url", iiurlwidth=640,
                         iiextmetadatafilter=META, **cont))
            for p in (d.get("query") or {}).get("pages", []):
                ii = (p.get("imageinfo") or [{}])[0]
                em = ii.get("extmetadata") or {}
                t = p["title"]
                if t in seen:
                    continue
                seen.add(t)
                n += 1
                rows.append(dict(
                    title=t, cat=cat, w=ii.get("width"), h=ii.get("height"), mime=ii.get("mime"), bytes=ii.get("size"),
                    date=plain((em.get("DateTimeOriginal") or {}).get("value")),
                    lic=plain((em.get("LicenseShortName") or {}).get("value")),
                    desc=plain((em.get("ImageDescription") or {}).get("value"))[:600],
                    artist=plain((em.get("Artist") or {}).get("value"))[:200],
                    credit=plain((em.get("Credit") or {}).get("value"))[:300],
                    thumb=ii.get("thumburl"), tw=ii.get("thumbwidth"), th=ii.get("thumbheight"),
                    page=ii.get("descriptionurl")))
            if "continue" not in d:
                break
            cont = {k: v for k, v in d["continue"].items() if k != "continue"}
            time.sleep(3.0)  # 0.6秒おきで 429 が出た（10-26）
        print(f"{n:4d}  {cat}", flush=True)
        time.sleep(3.0)
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("files", len(rows), "->", out)


NG = re.compile(r"model|replica|exhibit|museum|memorial|monument|statue|plaque|grave|cemetery|anniversar|centenary|"
                r"\b(19[3-9]\d|20\d\d)\b|film|movie|poster|stamp|coin|lego|\btoy|game|cake|titanic ii|titan sub|oceangate|"
                r"\b3d\b|render|cgi|painting|stöwer|stower|drawing|illustration|cartoon|sheet music|song|postcard of the film", re.I)


def list_rows(inp, out):
    rows = json.load(open(inp, encoding="utf-8"))
    keep = []
    for r in rows:
        t = r["title"][5:]
        if NG.search(t):
            continue
        if (r.get("mime") or "").startswith(("audio", "application/ogg")):
            continue
        if (r.get("w") or 0) < 400:  # 画面に使えない小ささ
            continue
        yr = re.search(r"\b(1[89]\d\d|20\d\d)\b", r.get("date") or "")
        if "International Ice Patrol" in r["cat"] and not (yr and int(yr.group(1)) <= 1925) and not re.search(r"191[2-4]|titanic", t, re.I):
            continue  # 氷山監視は始まりのころだけ
        keep.append(r)
    for i, r in enumerate(keep, 1):
        r["i"] = i
    json.dump(keep, open(out.replace(".tsv", ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        last = None
        for r in keep:
            if r["cat"] != last:
                f.write(f"## {r['cat'][9:]}\n")
                last = r["cat"]
            f.write(f"{r['i']}\t{(r['date'] or '')[:10]}\t{r['w']}x{r['h']}\t{(r['lic'] or '')[:9]}\t{re.sub(r'[.](jpe?g|png|tiff?|gif|svg|pdf|djvu|webm|ogv)$', '', r['title'][5:], flags=re.I)[:80]}\n")
    print("rows", len(rows), "keep", len(keep), "->", out)


def pick(inp, out, spec, extras):
    """spec="S1:2,6;S2:33" ＝ list の番号を欄ごとに選ぶ。extras="S2|File:…" ＝分類の外の点を題名で足す"""
    rows = {r["i"]: r for r in json.load(open(inp, encoding="utf-8"))}
    picks = []
    for part in spec.split(";"):
        slot, ids = part.split(":")
        for i in ids.split(","):
            picks.append(dict(rows[int(i)], slot=slot, key=f"{slot}-{int(i):03d}"))
    for k, ex in enumerate(extras, 1):
        slot, title = ex.split("|", 1)
        d = get(dict(action="query", titles=title, prop="imageinfo", iiprop="size|mime|extmetadata|url", iiurlwidth=640,
                     iiextmetadatafilter=META))
        p = d["query"]["pages"][0]
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata") or {}
        picks.append(dict(title=p["title"], cat="(分類の外・題名の検索)", w=ii.get("width"), h=ii.get("height"), mime=ii.get("mime"),
                          bytes=ii.get("size"), date=plain((em.get("DateTimeOriginal") or {}).get("value")),
                          lic=plain((em.get("LicenseShortName") or {}).get("value")),
                          desc=plain((em.get("ImageDescription") or {}).get("value"))[:600],
                          artist=plain((em.get("Artist") or {}).get("value"))[:200],
                          credit=plain((em.get("Credit") or {}).get("value"))[:300],
                          thumb=ii.get("thumburl"), tw=ii.get("thumbwidth"), th=ii.get("thumbheight"),
                          page=ii.get("descriptionurl"), slot=slot, key=f"{slot}-E{k:02d}", i=f"E{k:02d}"))
        time.sleep(3.0)
    json.dump(picks, open(out.replace(".tsv", ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("key\tdate\tsize\tlic\ttitle\tthumb\n")
        for r in picks:
            f.write(f"{r['key']}\t{(r['date'] or '')[:10]}\t{r['w']}x{r['h']}\t{r['lic']}\t{r['title'][5:]}\t{r['thumb']}\n")
    print("picks", len(picks), "->", out)


def thumbs(inp, outdir):
    """pick の縮小版（幅640）を落とす。10-26 カズヤくん了承（114点・約10MB・git の外）。index.tsv に大きさと md5"""
    import hashlib, os
    os.makedirs(outdir, exist_ok=True)
    picks = json.load(open(inp, encoding="utf-8"))
    log = []
    for r in picks:
        if "/thumb/" not in r["thumb"]:
            # 画像が960px より小さいと API は原本の URL を返す＝原本は数点で 429（記憶 reference-commons-standard-thumbnail-sizes）
            # → 画像の幅より小さい標準の幅で頼み直す
            std = max([s for s in (120, 250, 330, 500) if s < (r.get("w") or 0)] or [120])
            d = get(dict(action="query", titles=r["title"], prop="imageinfo", iiprop="url", iiurlwidth=std))
            r["thumb"] = d["query"]["pages"][0]["imageinfo"][0]["thumburl"]
            time.sleep(3.0)
        ext = os.path.splitext(urllib.parse.urlparse(r["thumb"]).path)[1].lower() or ".jpg"
        path = os.path.join(outdir, r["key"] + ext)
        if not any(os.path.exists(os.path.join(outdir, r["key"] + e)) for e in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif")) and not os.path.exists(path):
            for n in range(5):
                try:
                    with urllib.request.urlopen(urllib.request.Request(r["thumb"], headers=UA), timeout=60) as resp:
                        data = resp.read()
                    break
                except urllib.error.HTTPError as e:
                    if e.code in (429, 503):
                        time.sleep(30 * (n + 1))  # 2秒おきだと52点目で 429 が続いた（10-27）
                        continue
                    raise
            else:
                raise RuntimeError("429/503 が続いた: " + r["key"])
            with open(path, "wb") as f:
                f.write(data)
            time.sleep(5.0)  # 記憶 feedback の「1点ごとに5秒」
        b = open(path, "rb").read()
        log.append(f"{r['key']}\t{os.path.basename(path)}\t{len(b)}\t{hashlib.md5(b).hexdigest()}\t{r['thumb']}")
    with open(os.path.join(outdir, "index.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("key\tfile\tbytes\tmd5\turl\n" + "\n".join(log) + "\n")
    print("thumbs", len(log), "bytes", sum(int(x.split("\t")[2]) for x in log))


if __name__ == "__main__":
    if sys.argv[1] == "thumbs":
        thumbs(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "fetch":
        fetch(sys.argv[2], sys.argv[3:])
    elif sys.argv[1] == "list":
        list_rows(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "pick":
        pick(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
