# 26本目 ②：① の scratchpad から写した一次資料を、サーバの大きさ（HEAD）と突き合わせ、md5 を src/fetch_log.tsv に残す
# 落とし直さない（大きさが合えば写しを使う）。使い方: python -P ref/ep26/probe/head26.py
import hashlib, os, sys, urllib.error, urllib.request

UA = {"User-Agent": "zukai-engine-research/1.0 (source check)"}
SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
ITEMS = [
    ("G1", "gov/SERIALSET-06179_00_00-019-0933-0000.pdf",
     "https://www.govinfo.gov/content/pkg/SERIALSET-06179_00_00-019-0933-0000/pdf/SERIALSET-06179_00_00-019-0933-0000.pdf"),
    ("G2", "gov/maib1992.pdf",
     "https://assets.publishing.service.gov.uk/media/54c15bf240f0b6158d000027/MAIBReport_ReappraisalOfEvidence-SSCalifornian-Titanic-1992.pdf"),
    ("G3", "gov/nistir6118.pdf", "https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir6118.pdf"),
    ("G4", "gov/stat37_199.pdf", "https://www.govinfo.gov/link/statute/37/199"),
    ("G5", "gov/stat37_302.pdf", "https://www.govinfo.gov/link/statute/37/302"),
    ("G6", "gov/stat36_629.pdf", "https://www.govinfo.gov/link/statute/36/629"),
]


def server_size(url):
    """HEAD で大きさを聞く。HEAD を断られたら Range: bytes=0-0 の GET で Content-Range から読む"""
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        with urllib.request.urlopen(req, timeout=60) as r:
            n = r.headers.get("Content-Length")
            if n:
                return r.status, r.geturl(), int(n), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError:
        pass  # nvlpubs.nist.gov は HEAD にだけ 404 を返す（GET は 206）＝断られ方を問わず GET で測る
    req = urllib.request.Request(url, headers=dict(UA, Range="bytes=0-0"))
    with urllib.request.urlopen(req, timeout=60) as r:
        cr = r.headers.get("Content-Range", "")
        n = int(cr.rsplit("/", 1)[1]) if "/" in cr else None
        return r.status, r.geturl(), n, r.headers.get("Content-Type", "")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    rows, bad = [], 0
    for key, rel, url in ITEMS:
        p = os.path.join(SRC, rel)
        loc = os.path.getsize(p) if os.path.exists(p) else None
        try:
            st, final, srv, ctype = server_size(url)
        except Exception as e:  # 読めなければ止める側に倒す
            st, final, srv, ctype = f"ERR {type(e).__name__}", url, None, ""
        ok = loc is not None and srv is not None and loc == srv
        bad += 0 if ok else 1
        rows.append([key, rel, str(loc), md5(p) if loc else "-", url, final, str(st), str(srv), ctype, "OK" if ok else "NG"])
        print(key, rel, loc, srv, st, "OK" if ok else "NG")
    with open(os.path.join(SRC, "fetch_log.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(["id", "local", "bytes_local", "md5", "url", "final_url", "status", "bytes_server", "type", "match"]) + "\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print("bad", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
