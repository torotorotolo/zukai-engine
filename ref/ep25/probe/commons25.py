# -*- coding: utf-8 -*-
"""25本目②：Commons の Category:Amagasaki derailment（と下の分類）の全点の台帳と縮小版（幅640px）を取る。
2005年の CC BY 4.0 の2点だけ原寸も取る（10-25 カズヤくん了承）。隠しカテゴリ（clshow=hidden）＝ライセンスの根拠も取る（ルール 2-11）。
Commons は続けて聞くと 429＝1点ごとに5秒空ける。出力は src/commons/（git の外）。
使い方: python commons25.py <出力フォルダ>"""
import json, os, re, sys, time, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"
ROOT = "Category:Amagasaki derailment"
ORIG = {"File:Amagasaki derailment damage to the first car.jpg", "File:Amagasaki derailment aerial view of the accident site.jpg"}


def get(params):
    params = dict(params, format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(15 * (i + 1))
                continue
            raise
    raise RuntimeError("429 が続いた")


def fetch(url, path):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                b = r.read()
            open(path, "wb").write(b)
            return len(b)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(15 * (i + 1))
                continue
            return f"http{e.code}"
    return "429"


def members(cat):
    out, cont = [], {}
    while True:
        j = get(dict(action="query", list="categorymembers", cmtitle=cat, cmtype="file|subcat", cmlimit="500", **cont))
        out += j["query"]["categorymembers"]
        if "continue" not in j:
            return out
        cont = j["continue"]


def main():
    outdir = sys.argv[1]
    os.makedirs(os.path.join(outdir, "thumb"), exist_ok=True)
    files, cats, seen = [], [ROOT], set()
    while cats:
        c = cats.pop(0)
        if c in seen:
            continue
        seen.add(c)
        for m in members(c):
            if m["ns"] == 14:
                cats.append(m["title"])
            elif m["ns"] == 6:
                files.append((m["title"], c))
        time.sleep(2)
    titles = sorted({t for t, _ in files})
    meta = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        j = get(dict(action="query", prop="imageinfo|categories", titles="|".join(chunk), iiprop="url|size|mime|extmetadata|timestamp",
                     iiurlwidth="640", clshow="hidden", cllimit="500"))
        for p in j["query"]["pages"]:
            meta[p["title"]] = p
        time.sleep(3)
    json.dump({"files": files, "meta": meta}, open(os.path.join(outdir, "commons_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rows = ["no\ttitle\tw\th\tmime\tlicense\tdate\tartist\tcredit\thidden_cats\tthumb\torig"]
    for n, t in enumerate(titles, 1):
        p = meta.get(t, {})
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        val = lambda k: re.sub(r"<[^>]+>", "", (em.get(k) or {}).get("value", "")).strip().replace("\t", " ").replace("\n", " ")[:160]
        hid = ",".join(c["title"].replace("Category:", "") for c in p.get("categories", []))[:300]
        safe = re.sub(r"[^\w.-]", "_", t.replace("File:", ""))[:90]
        th = ""
        if ii.get("thumburl") and ii.get("mime", "").startswith("image/"):
            r = fetch(ii["thumburl"], os.path.join(outdir, "thumb", f"{n:02d}_{safe}" + (".png" if ii["mime"] == "image/png" else ".jpg")))
            th = str(r)
            time.sleep(5)
        org = ""
        if t in ORIG and ii.get("url"):
            r = fetch(ii["url"], os.path.join(outdir, f"orig_{safe}"))
            org = str(r)
            time.sleep(5)
        rows.append("\t".join([str(n), t, str(ii.get("width", "")), str(ii.get("height", "")), ii.get("mime", ""), val("LicenseShortName"),
                               val("DateTimeOriginal"), val("Artist"), val("Credit"), hid, th, org]))
        print(n, t, th, org, flush=True)
    open(os.path.join(outdir, "commons_list.tsv"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    print("files", len(titles), "cats", len(seen))


if __name__ == "__main__":
    main()
