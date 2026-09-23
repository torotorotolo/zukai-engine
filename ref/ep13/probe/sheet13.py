"""13本目②: 候補を 640px のシート（2列×3行）にする。セルの下に 番号・題・原寸・権利。
あわせて動画2本と archive.org 2点の器の値を測る（絵は見ない＝値だけ）。
"""
import io, json, re, time, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont

SP = r"C:/Users/konar/AppData/Local/Temp/claude/C--Users-konar-Documents-Obsidian-Vault/3febce82-d020-45c6-b4de-0b38ceece0fa/scratchpad"
UA = "zukai-engine-research/0.1 (konariri8 research)"
recs = {r["title"]: r for r in json.load(open(r"C:/Users/konar/Desktop/zukai-engine/ref/ep13/commons_ep13.json", encoding="utf-8"))}
seen = {}


def pick(prefix):
    for t in recs:
        if t.startswith("File:" + prefix):
            return recs[t]
    raise SystemExit("見つからない: " + prefix)


SHEETS = {
    "A_jiko_ki": ["TC-JAV (5920254289) (2)", "TC-JAV (6004629408).jpg", "TC-JAV, Turkish DC-10",
                  "THY Türk Hava Yolları", "N103AA American DC-10-10 at KSFO.jpg", "Photo of American Airlines Flight 96"],
    "B_genba": ["Paris DC-10 Crash- March", "Paris DC-10 Crash, Names", "Stèle du crash", "Monument DC10 Ermenonville-1",
                "TK981 crash site", "TurkHava accident still"],
    "C_dokei_1": ["Eerste DC 10 voor KLM landt op Schiphol, Bestanddeelnr 926-1070", "Eerste DC 10 voor KLM landt op Schiphol, DC 10 op platform",
                  "Eerste DC 10 voor KLM landt op Schiphol, cockpit en interieur", "Vlucht met DC-10 naar Nice, cockpit",
                  "American Airlines McDonnell Douglas DC-10 01", "Korean Air Lines McDonnell Douglas DC-10 N198"],
    "D_dokei_2": ["United Airlines DC-10 N1826U", "McDonnell Douglas DC-10 N1803U (C15-10)", "McDonnell Douglas DC-10 interior (CJ406257)",
                  "DOUGLAS DC-10 AIRCRAFT - NARA - 17498081", "Douglas DC-10-10 TC-JAU THY FRA 28.07.74 edited-2.jpg",
                  "Finnairin DC-10 lentokone lentokentällä 1970"],
}
try:
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 17)
except Exception:
    font = ImageFont.load_default()
CW, CH, LH = 640, 430, 46
log = []
for name, prefixes in SHEETS.items():
    sheet = Image.new("RGB", (2 * CW + 30, 3 * (CH + LH) + 40), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for i, pre in enumerate(prefixes):
        r = pick(pre)
        url = r["thumb"] or r["url"]
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        for k in range(4):
            try:
                data = urllib.request.urlopen(req, timeout=60).read(); break
            except urllib.error.HTTPError as e:
                if e.code == 429: time.sleep(15 * (k + 1)); continue
                raise
        im = Image.open(io.BytesIO(data)).convert("RGB")
        im.thumbnail((CW, CH))
        x = 10 + (i % 2) * (CW + 10); y = 10 + (i // 2) * (CH + LH + 5)
        sheet.paste(im, (x + (CW - im.width) // 2, y))
        lab = f"{name[0]}{i + 1} {r['title'][5:][:52]}"
        d.text((x, y + CH + 2), lab, fill=(255, 255, 160), font=font)
        d.text((x, y + CH + 22), f"   原寸 {r['w']}x{r['h']}  {r['license'][:22]}", fill=(200, 230, 255), font=font)
        log.append(f"{name[0]}{i + 1}\t{r['title']}\t{r['w']}x{r['h']}\t{r['license']}\t{r['url']}")
        time.sleep(1.2)
    out = f"{SP}/sheet13_{name}.png"
    sheet.save(out)
    print("sheet", out, sheet.size)
open(f"{SP}/sheet13_index.tsv", "w", encoding="utf-8").write("\n".join(log))

# 器の値（絵は見ない）
API = "https://commons.wikimedia.org/w/api.php"
for t in ['File:1971 American Airlines "DC-10 LuxuryLiner" Commercial.webm', "File:FedEx Express DC-10-30 Landing at PDX.ogv",
          "File:FedEx N556FE MD-10-10 (DC-10) Takeoff Portland Airport (PDX).ogv"]:
    q = urllib.parse.urlencode({"action": "query", "titles": t, "prop": "imageinfo|categories", "clshow": "hidden",
                                "iiprop": "size|mime|extmetadata|url", "iiextmetadatafilter": "LicenseShortName|Artist|DateTimeOriginal|ImageDescription",
                                "format": "json", "formatversion": 2})
    js = json.loads(urllib.request.urlopen(urllib.request.Request(API + "?" + q, headers={"User-Agent": UA})).read())
    p = js["query"]["pages"][0]; ii = (p.get("imageinfo") or [{}])[0]; em = ii.get("extmetadata", {})
    print("VIDEO", t[5:70], ii.get("width"), "x", ii.get("height"), ii.get("mime"), "dur?", ii.get("duration"),
          (em.get("LicenseShortName") or {}).get("value"), "|", re.sub("<[^>]+>", "", (em.get("Artist") or {}).get("value", ""))[:60],
          "| hidden:", [c["title"][9:] for c in p.get("categories", [])][:6])
    time.sleep(1.5)
fj = json.load(open(f"{SP}/footage13.json", encoding="utf-8"))
ids = [d["identifier"] for k, v in fj.items() if k.startswith("ia:") for d in v.get("docs", [])
       if re.search(r"american-airlines-dc-10-delivery|turkish-airlines-douglas-dc-10", d["identifier"])]
for ident in ids:
    js = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://archive.org/metadata/{ident}", headers={"User-Agent": UA})).read())
    md = js.get("metadata", {})
    files = [(f["name"], f.get("width"), f.get("height")) for f in js.get("files", []) if f.get("format", "").lower() in ("jpeg", "png", "jpeg 2000")][:4]
    print("IA", ident, "|", str(md.get("title"))[:60], "| date", md.get("date"), "| rights", str(md.get("rights") or md.get("licenseurl"))[:80],
          "| creator", str(md.get("creator"))[:40], "| desc", re.sub(r"\s+", " ", str(md.get("description")))[:200], "| files", files)
