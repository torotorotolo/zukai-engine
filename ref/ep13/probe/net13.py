"""13本目②: commons_ep13.json に網の3段（権利→大きさ→撮影年）を当て、欄ごとに1点1行で出す。
権利の区分（ルール §2-10・2-13）: PD-A=米連邦§105 / PD-B=自主宣言(PDM・CC0) / PD-C=米国で更新なし / PD-他 / BY=継承なし / BY-SA=額装のみ / 他
年は desc・date・title から4桁を拾う（取り込みの年が混じる＝最後は題名と絵で確かめる）。
"""
import json, re, sys
from collections import Counter

J = r"C:/Users/konar/Desktop/zukai-engine/ref/ep13/commons_ep13.json"
recs = json.load(open(J, encoding="utf-8"))


def right(r):
    lic = (r["license"] or "").lower(); hid = " ".join(r["hidden"]).lower()
    if "pd-usgov" in hid or "pd us government" in hid or "pd-usgov" in lic or "works of the united states" in hid:
        return "PD-A"
    if "cc0" in lic or "public domain mark" in lic or "cc-zero" in hid or "pdm" in lic:
        return "PD-B"
    if "not renewed" in hid or "not renewed" in lic or "pd-us-not renewed" in hid:
        return "PD-C"
    if lic.startswith("public domain") or "pd-" in hid:
        return "PD-他"
    if "by-sa" in lic:
        return "BY-SA"
    if lic.startswith("cc by") or lic.startswith("cc-by"):
        return "BY"
    if "no known copyright" in hid or "flickr-no known" in hid:
        return "NKCR"
    return "他:" + (r["license"] or "?")[:20]


def year(r):
    for s in (r["date"], r["title"], r["desc"]):
        m = re.search(r"\b(19[4-9]\d|20[0-2]\d)\b", s or "")
        if m:
            return int(m.group(1))
    return None


def group(r):
    s = " ".join(r["src"])
    for key, g in [("Flight 981 memorial", "memorial"), ("Turkish Airlines Flight 981", "thy981"), ("TC-JAV", "tcjav"),
                   ("American Airlines Flight 96", "aa96"), ("N103AA", "n103aa"), ("Turkish Airlines", "thy_dc10"),
                   ("TC-JA", "thy_dc10"), ("Orly", "orly70s"), ("KLM", "klm_dc10"), ("PH-DT", "klm_dc10"),
                   ("Saint-Pathus", "stpathus"), ("Ermenonville", "foret"), ("American Airlines", "aa_dc10")]:
        if key in s:
            return g
    return "search"


rows = []
for r in recs:
    r["R"], r["Y"], r["G"] = right(r), year(r), group(r)
    rows.append(r)

print("総数", len(rows), "／欄ごと:", dict(Counter(r["G"] for r in rows)))
print("権利:", dict(Counter(r["R"] for r in rows)))
big = [r for r in rows if (r["w"] or 0) >= 1280 and (r["mime"] or "").startswith("image/")]
print("幅1280以上の静止画:", len(big), "／うち継承なし(PD/BY/NKCR):", sum(r["R"] not in ("BY-SA",) and not r["R"].startswith("他") for r in big))
print("1974年:", sum(r["Y"] == 1974 for r in rows), "／1970-74年:", sum(1970 <= (r["Y"] or 0) <= 1974 for r in rows))
print()
want = sys.argv[1:] or ["tcjav", "thy981", "memorial", "aa96", "n103aa", "thy_dc10", "orly70s", "klm_dc10", "aa_dc10", "stpathus", "search"]
for g in want:
    sel = sorted([r for r in rows if r["G"] == g], key=lambda r: (r["Y"] or 9999, r["title"]))
    if g == "search":
        sel = [r for r in sel if (r["Y"] or 9999) <= 1980]
    print(f"### {g}  {len(sel)}点")
    for r in sel:
        d = re.sub(r"\s+", " ", r["desc"])[:110]
        print(f"  {r['Y'] or '----'} {r['w']}x{r['h']} {r['R']:6s} {r['title'][5:][:70]} | {d}")
fo = [r for r in rows if r["G"] == "foret"]
print(f"### foret {len(fo)}点  権利={dict(Counter(r['R'] for r in fo))}  幅1280以上={sum((r['w'] or 0)>=1280 for r in fo)}")
for r in fo:
    if re.search(r"st[eè]le|m[ée]morial|DC-?10|catastrophe|1974|turk|crash|accident|monument", r["title"] + r["desc"], re.I):
        print(f"  {r['Y'] or '----'} {r['w']}x{r['h']} {r['R']:6s} {r['title'][5:][:70]} | {re.sub(chr(10),' ',r['desc'])[:100]}")
