# -*- coding: utf-8 -*-
"""国会会議録API（中華航空・1994-04-26〜1997-12-31）・連邦官報（AD 94-21-07）・NTSB 勧告書を取る。"""
import json, time, hashlib, urllib.request, urllib.parse, os
S = r"C:\Users\konar\Desktop\zukai-engine\ref\ep17\src"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"
log = open(os.path.join(S, "fetch_log.tsv"), "a", encoding="utf-8")

def get(u, ref=None):
    h = {"User-Agent": UA}
    if ref: h["Referer"] = ref
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=120)
        return r.status, r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, b"", ""
    except Exception as e:
        return -1, str(e).encode(), ""

def save(fn, u, st, b, ct):
    if st == 200 and b:
        open(os.path.join(S, fn), "wb").write(b)
    log.write(f"{fn}\t{st}\t{len(b)}\t{hashlib.md5(b).hexdigest() if b else ''}\t{ct.split(';')[0]}\t(new)\t{u}\n")
    print(fn, st, len(b), flush=True)

# 1) 国会会議録
recs, start = [], 1
while True:
    q = urllib.parse.urlencode({"any": "中華航空", "from": "1994-04-26", "until": "1997-12-31",
                                "maximumRecords": 100, "startRecord": start, "recordPacking": "json"})
    u = "https://kokkai.ndl.go.jp/api/speech?" + q
    st, b, ct = get(u)
    if st != 200: print("kokkai", st); break
    j = json.loads(b.decode("utf-8"))
    recs += j.get("speechRecord", [])
    print("kokkai total", j.get("numberOfRecords"), "got", len(recs), flush=True)
    nxt = j.get("nextRecordPosition")
    if not nxt: break
    start = nxt; time.sleep(3)
open(os.path.join(S, "kokkai_1994-1997_chuka.json"), "w", encoding="utf-8").write(json.dumps(recs, ensure_ascii=False, indent=1))
log.write(f"kokkai_1994-1997_chuka.json\t200\t{len(recs)}recs\t\tapplication/json\t(new)\thttps://kokkai.ndl.go.jp/api/speech?any=中華航空&from=1994-04-26&until=1997-12-31\n")

# 2) 連邦官報：AD 94-21-07（federalregister.gov は1994年以降を収録）
q = urllib.parse.urlencode({"conditions[term]": "\"94-21-07\"", "per_page": 20})
st, b, ct = get("https://www.federalregister.gov/api/v1/documents.json?" + q)
print("FR search", st, len(b))
if st == 200:
    j = json.loads(b.decode("utf-8"))
    for d in j.get("results", []):
        print("  ", d.get("publication_date"), d.get("document_number"), d.get("title")[:90], d.get("pdf_url"))
    open(os.path.join(S, "fr_search_94-21-07.json"), "wb").write(b)

# 3) NTSB 勧告書 A-94-164〜166
for u in ["https://www.ntsb.gov/safety/safety-recs/recletters/A94_164_166.pdf",
          "https://www.ntsb.gov/safety/safety-recs/RecLetters/A94_164_166.pdf"]:
    st, b, ct = get(u, ref="https://www.ntsb.gov/")
    print("NTSB", u, st, len(b), ct)
    if st == 200 and b[:4] == b"%PDF":
        save("ntsb_A94-164-166.pdf", u, st, b, ct); break
    time.sleep(2)
log.close()
