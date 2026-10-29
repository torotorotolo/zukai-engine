# Commons のカテゴリの木を2段まで見て、各カテゴリの直下のファイル数を数える（画像は落とさない・API の目録だけ）
import json, sys, time, urllib.request, urllib.parse
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "zukai-engine-research/1.0 (contact via GitHub torotorotolo)"}
def q(**kw):
    kw.update(format="json")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(kw), headers=UA)
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception as e:
            time.sleep(5 * (i + 1))
    raise SystemExit("API failed")
def members(cat, typ):
    out, cont = [], {}
    while True:
        r = q(action="query", list="categorymembers", cmtitle=cat, cmtype=typ, cmlimit=500, **cont)
        out += [m["title"] for m in r["query"]["categorymembers"]]
        if "continue" not in r: return out
        cont = {"cmcontinue": r["continue"]["cmcontinue"]}; time.sleep(1)
root = sys.argv[1]
depth = int(sys.argv[2]) if len(sys.argv) > 2 else 1
seen, frontier = {}, [(root, 0)]
while frontier:
    c, d = frontier.pop(0)
    if c in seen: continue
    files = members(c, "file"); seen[c] = len(files)
    print("%d\t%d\t%s" % (d, len(files), c), flush=True)
    if d < depth:
        for s in members(c, "subcat"): frontier.append((s, d + 1))
    time.sleep(1)
print("TOTAL_DIRECT_FILES", sum(seen.values()), "cats", len(seen))
