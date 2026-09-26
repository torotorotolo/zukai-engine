# -*- coding: utf-8 -*-
"""17本目②：一次資料を ref/ep17/src/ へ取り直す。http・大きさ・md5 を fetch_log.tsv に残す。
①の写し（別セッションの scratchpad/cal140）と md5 を比べ、サーバの中身が変わっていないかも見る。"""
import hashlib, os, sys, time, urllib.request, urllib.error

DST = r"C:\Users\konar\Desktop\zukai-engine\ref\ep17\src"
OLD = r"C:\Users\konar\AppData\Local\Temp\claude\C--Users-konar-Documents-Obsidian-Vault\40b5ab2d-cd91-4546-b886-bd10b2abd87f\scratchpad\cal140"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"

J = "https://jtsb.mlit.go.jp"
ITEMS = [(f"jtsb_96-5_ja_{i:02d}.pdf", f"{J}/aircraft/download/96-5-B1816-{i:02d}.pdf", f"ja_{i:02d}.pdf") for i in range(1, 13)]
ITEMS += [
    ("jtsb_96-5_en.pdf", f"{J}/eng-air_report/B1816.pdf", "en_jtsb.pdf"),
    ("jtsb_detail851.html", f"{J}/jtsb/aircraft/detail.php?id=851", "detail851.html"),
    ("jtsb_bunkatsu.html", f"{J}/jtsb/aircraft/download/bunkatsu.html", "bunkatsu.html"),
    ("jtsb_cyo.html", f"{J}/cyo.html", "jtsb_cyo.html"),
    ("pdl1.0.html", "https://www.digital.go.jp/resources/open_data/public_data_license_v1.0", None),
    ("faa_ll_B1816.html", "https://www.faa.gov/lessons_learned/transport_airplane/accidents/B1816", "faa_ll.html"),
    ("faa_hf_team_1996.pdf", "https://www.faa.gov/sites/faa.gov/files/2022-11/interfac.pdf", "faa_hft.pdf"),
    ("faa_ad98-17-09.pdf", "https://www.faa.gov/sites/faa.gov/files/2022-11/AD98-17-09.pdf", "ad98-17-09.pdf"),
    ("caa_pl_list.pdf", "https://www.caa.go.jp/policies/policy/consumer_safety/other/product_liability_act/assets/consumer_safety_cms206_250326_01.pdf", "caa_pl.pdf"),
]

def md5(b):
    return hashlib.md5(b).hexdigest()

def get(url, referer=None, tries=3):
    last = None
    for k in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, **({"Referer": referer} if referer else {})})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.status, r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            last = (e.code, b"", "")
        except Exception as e:  # noqa
            last = (-1, str(e).encode(), "")
        time.sleep(3 + 3 * k)
    return last

def main():
    os.makedirs(DST, exist_ok=True)
    rows = []
    for name, url, oldname in ITEMS:
        ref = "https://www.faa.gov/" if "faa.gov" in url else None
        st, body, ct = get(url, referer=ref)
        p = os.path.join(DST, name)
        if st == 200 and body:
            with open(p, "wb") as f:
                f.write(body)
        old = ""
        if oldname and os.path.exists(os.path.join(OLD, oldname)):
            with open(os.path.join(OLD, oldname), "rb") as f:
                ob = f.read()
            old = "same" if md5(ob) == md5(body) else f"DIFF(old {len(ob)}B)"
        rows.append((name, st, len(body), md5(body) if body else "", ct.split(";")[0], old, url))
        print(f"{name}\t{st}\t{len(body)}\t{old}", flush=True)
        time.sleep(1.5)
    with open(os.path.join(DST, "fetch_log.tsv"), "w", encoding="utf-8") as f:
        f.write("file\thttp\tbytes\tmd5\tcontent_type\tvs_ep17_1st_copy\turl\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    bad = [r for r in rows if r[1] != 200]
    print("NG:", len(bad))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
