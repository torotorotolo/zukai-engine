"""13本目②: 一次資料を落として本文を抜く（1回で全部）。
出力: ref/ep13/src/<name>.pdf / .txt（頁区切り '=== p N ===')、標準出力に 1件1行の実測。
"""
import hashlib, json, os, re, sys, time, urllib.request, urllib.parse

import fitz  # PyMuPDF

ROOT = r"C:/Users/konar/Desktop/zukai-engine/ref/ep13/src"
os.makedirs(ROOT, exist_ok=True)
UA = "zukai-engine-research/0.1 (konariri8 research; contact via github toro)"

SRC = [
    ("aib_8-76_TC-JAV", "https://assets.publishing.service.gov.uk/media/5422eedde5274a1317000247/8-1976_TC-JAV.pdf"),
    ("ntsb_AAR73-02_N103AA", "https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR7302.pdf"),
    ("ntsb_AAR73-02_N103AA_erau", "http://libraryonline.erau.edu/online-full-text/ntsb/aircraft-accident-reports/AAR73-02.pdf"),
    ("senate_cprt93_dc10", "https://www.govinfo.gov/content/pkg/CPRT-93SPRT33379O/pdf/CPRT-93SPRT33379O.pdf"),
]

COMMON = set("the of and to in a is that for was on with as by at from this be it were or which an are not".split())


def get(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        code = r.status
        ctype = r.headers.get("Content-Type", "")
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return code, ctype, len(data), time.time() - t0


def extract(pdf, txt):
    doc = fitz.open(pdf)
    words = hits = 0
    empty = []
    with open(txt, "w", encoding="utf-8") as f:
        for i, page in enumerate(doc, 1):
            t = page.get_text()
            f.write(f"\n=== p {i} ===\n{t}")
            ws = re.findall(r"[A-Za-z]+", t.lower())
            words += len(ws)
            hits += sum(1 for w in ws if w in COMMON)
            if len(t.strip()) < 40:
                empty.append(i)
    n = len(doc)
    imgs = sum(len(p.get_images()) for p in doc)
    return n, words, (hits / words if words else 0.0), empty, imgs


for name, url in SRC:
    pdf = os.path.join(ROOT, name + ".pdf")
    try:
        code, ctype, size, dt = get(url, pdf)
    except Exception as e:  # fail closed: 取れなければ行に書いて次へ
        print(f"NG  {name}  {url}  err={type(e).__name__}: {e}")
        continue
    md5 = hashlib.md5(open(pdf, "rb").read()).hexdigest()
    if not open(pdf, "rb").read(5).startswith(b"%PDF"):
        print(f"NG  {name}  http={code} ctype={ctype} size={size} (PDFでない) md5={md5}")
        continue
    n, words, rate, empty, imgs = extract(pdf, os.path.join(ROOT, name + ".txt"))
    print(f"OK  {name}  http={code} size={size} md5={md5} pages={n} words={words} common={rate:.3f} "
          f"textless_pages={len(empty)}{(' e.g. ' + str(empty[:12])) if empty else ''} images={imgs}")
    time.sleep(2)

# 国会会議録（日本側の一次資料の当たり）: 1974-03〜06 の「トルコ航空」
q = urllib.parse.urlencode({"any": "トルコ航空", "from": "1974-03-01", "until": "1974-12-31",
                            "recordPacking": "json", "maximumRecords": 30})
try:
    req = urllib.request.Request("https://kokkai.ndl.go.jp/api/speech?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        js = json.loads(r.read().decode("utf-8"))
    print("KOKKAI numberOfRecords=", js.get("numberOfRecords"))
    out = []
    for s in js.get("speechRecord", []):
        out.append({k: s.get(k) for k in ("date", "nameOfHouse", "nameOfMeeting", "speaker", "speechURL")}
                   | {"speech": s.get("speech", "")})
        sp = s.get("speech", "")
        i = sp.find("トルコ航空")
        print(f"  {s.get('date')} {s.get('nameOfHouse')} {s.get('nameOfMeeting')} {s.get('speaker')} "
              f"{s.get('speechURL')}\n    …{sp[max(0, i - 120): i + 220].replace(chr(10), ' ')}…")
    with open(os.path.join(ROOT, "kokkai_1974_turkish.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
except Exception as e:
    print("KOKKAI NG", type(e).__name__, e)
