"""13本目②: Commons の素材を網の4段（権利→大きさ→撮影年→場面）の前3段まで機械で測る。
使い方: python commons13.py cats   … カテゴリの実在と点数
        python commons13.py pull   … 下の CATS と SEARCH の全点を取り、ref/ep13/commons_ep13.json に保存
429 対策: User-Agent で名乗る・1回ごとに sleep・429 なら 20秒待って最大4回。
"""
import json, os, re, sys, time, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "zukai-engine-research/0.1 (https://github.com/; konariri8 research) python-urllib"
OUT = r"C:/Users/konar/Desktop/zukai-engine/ref/ep13/commons_ep13.json"

CATS = [
    "Category:TC-JAV (aircraft)",
    "Category:Turkish Airlines Flight 981",
    "Category:Turkish Airlines Flight 981 memorial",
    "Category:American Airlines Flight 96",
    "Category:N103AA (aircraft)",
    "Category:McDonnell Douglas DC-10 of Turkish Airlines",
    "Category:TC-JAU (aircraft)",
    "Category:TC-JAY (aircraft)",
    "Category:McDonnell Douglas DC-10 cargo doors",
    "Category:McDonnell Douglas DC-10 (interior)",
    "Category:McDonnell Douglas DC-10 cockpits",
    "Category:McDonnell Douglas DC-10-10",
    "Category:McDonnell Douglas DC-10 in the 1970s",
    "Category:McDonnell Douglas DC-10 of American Airlines",
    "Category:McDonnell Douglas DC-10 of KLM",
    "Category:Paris-Orly Airport in the 1970s",
    "Category:Paris-Orly Airport in 1974",
    "Category:Forêt d'Ermenonville",
    "Category:Saint-Pathus",
    "Category:Douglas Aircraft Company plant, Long Beach",
    "Category:Aircraft accidents in France in 1974",
    "Category:1974 aviation accidents",
    "Category:Accident de l'avion DC-10 de la Turkish Airlines",
]
SEARCH = [
    'intitle:"DC-10" 1974', 'intitle:"DC-10" 1973', 'intitle:"DC-10" 1972', 'intitle:"DC-10" Anefo',
    '"DC-10" "cargo door"', '"Ermenonville" 1974', '"Turkish Airlines" "DC-10"', '"THY" "DC-10"',
    '"McDonnell Douglas DC-10" Long Beach 1971', '"DC 10" KLM Schiphol', '"Orly" 1974 aéroport',
]


def call(params, tries=4):
    params = dict(params, format="json", formatversion=2)
    url = API + "?" + urllib.parse.urlencode(params)
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                js = json.loads(r.read().decode("utf-8"))
            time.sleep(1.5)
            return js
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 * (k + 1))
                continue
            raise
    raise RuntimeError("429 が続いた: " + url)


def cats():
    for i in range(0, len(CATS), 20):
        js = call({"action": "query", "prop": "categoryinfo", "titles": "|".join(CATS[i:i + 20])})
        for p in js["query"]["pages"]:
            ci = p.get("categoryinfo")
            print(("✓" if ci else "✗"), p["title"], ci and f"files={ci.get('files')} subcats={ci.get('subcats')}")


PROPS = {"prop": "imageinfo|categories", "iiprop": "url|size|mime|extmetadata|timestamp",
         "iiextmetadatafilter": "LicenseShortName|Artist|Credit|DateTimeOriginal|ImageDescription|ObjectName|UsageTerms|Copyrighted",
         "iiurlwidth": 640, "clshow": "hidden", "cllimit": "max"}


PULL = ["Category:TC-JAV (aircraft)", "Category:Turkish Airlines Flight 981",
        "Category:Turkish Airlines Flight 981 memorial", "Category:American Airlines Flight 96",
        "Category:N103AA (aircraft)", "Category:McDonnell Douglas DC-10 of Turkish Airlines",
        "Category:Paris-Orly Airport in the 1970s", "Category:McDonnell Douglas DC-10 of KLM",
        "Category:Saint-Pathus", "Category:Forêt d'Ermenonville",
        "Category:McDonnell Douglas DC-10 of American Airlines"]
DEEP = set(PULL[:8])  # 子カテゴリを1段たどる


def subcats(c):
    js = call({"action": "query", "list": "categorymembers", "cmtitle": c, "cmtype": "subcat", "cmlimit": 100})
    return [m["title"] for m in js["query"]["categorymembers"]]


def pull():
    global CATS
    todo = []
    for c in PULL:
        todo.append(c)
        if c in DEEP:
            todo += subcats(c)
    CATS = list(dict.fromkeys(todo))
    print("categories:", len(CATS)); [print("  ", c) for c in CATS]
    got = {}
    def eat(js, src):
        for p in js.get("query", {}).get("pages", []):
            if p.get("ns") != 6 or "imageinfo" not in p:
                continue
            ii = p["imageinfo"][0]; em = ii.get("extmetadata", {})
            g = lambda k: re.sub(r"<[^>]+>", "", (em.get(k) or {}).get("value", "")).strip()
            rec = got.setdefault(p["pageid"], {"title": p["title"], "w": ii.get("width"), "h": ii.get("height"),
                   "mime": ii.get("mime"), "url": ii.get("url"), "thumb": ii.get("thumburl"),
                   "license": g("LicenseShortName"), "artist": g("Artist")[:120], "credit": g("Credit")[:160],
                   "date": g("DateTimeOriginal")[:60], "desc": g("ImageDescription")[:400],
                   "hidden": [c["title"] for c in p.get("categories", [])], "src": []})
            rec["src"].append(src)
    for c in CATS:
        cont = {}
        while True:
            js = call({"action": "query", "generator": "categorymembers", "gcmtitle": c, "gcmtype": "file",
                       "gcmlimit": 50, **PROPS, **cont})
            eat(js, c)
            if "continue" not in js:
                break
            cont = js["continue"]
    for q in SEARCH:
        js = call({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 50, **PROPS})
        eat(js, "search:" + q)
    json.dump(list(got.values()), open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", len(got), "files ->", OUT)


if __name__ == "__main__":
    {"cats": cats, "pull": pull}[sys.argv[1]]()
