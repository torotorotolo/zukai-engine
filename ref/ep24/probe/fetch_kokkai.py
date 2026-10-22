# -*- coding: utf-8 -*-
"""24本目②：国会会議録 API（speech）で「チェルノブイル」「チェルノブイリ」を 1986-04-26〜1987-05-31 で全部取る。
保存＝ref/ep24/src/kokkai_<語>.json（speechRecord の配列）。1回100件・3秒あけて次の頁。"""
import json, os, sys, time, urllib.parse, urllib.request

DST = r"C:\Users\konar\Desktop\zukai-engine\ref\ep24\src"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"
API = "https://kokkai.ndl.go.jp/api/speech"


def fetch(word, frm, until):
    out, start = [], 1
    while True:
        qs = urllib.parse.urlencode({"any": word, "from": frm, "until": until, "recordPacking": "json",
                                     "maximumRecords": 100, "startRecord": start})
        req = urllib.request.Request(API + "?" + qs, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.load(r)
        out += d.get("speechRecord", [])
        print(word, start, d.get("numberOfRecords"), len(out), flush=True)
        nxt = d.get("nextRecordPosition")
        if not nxt:
            return d.get("numberOfRecords"), out
        start = nxt
        time.sleep(3)


def main():
    frm, until = "1986-04-26", "1987-05-31"
    for word in ("チェルノブイル", "チェルノブイリ"):
        n, recs = fetch(word, frm, until)
        path = os.path.join(DST, f"kokkai_{word}_{frm}_{until}.json")
        json.dump({"query": {"any": word, "from": frm, "until": until}, "numberOfRecords": n, "speechRecord": recs},
                  open(path, "w", encoding="utf-8"), ensure_ascii=False)
        print("saved", path, n, len(recs))
        if n != len(recs):
            print("MISMATCH", n, len(recs))
            sys.exit(1)


if __name__ == "__main__":
    main()
