# -*- coding: utf-8 -*-
"""13本目⑤b-2：Commons の写真を `ref/ep13/img/` に取る（2026-09-24・カズヤくん許可＝21点＋未見9点の見本）。

■ なぜ幅3000pxの版か
  束（`qa_out/ep13_assets.py build`）はどのみち幅3000px（MAXW）に縮める＝絵は同じ。
  原寸だと計75MB（D6 は TIFF 37MB）・C: は 99%。API の imageinfo（iiurlwidth）で版の URL を取る。
■ 控え＝`ref/ep13/img/fetched.json`（題名 → 取った URL・幅・原寸・原本の SHA-1・権利）
  ⚠️ 原本の SHA-1 は Commons の原寸ファイルのもの（取ったのは縮小版＝ファイルの md5 は別に持つ）。

    python ref/ep13/probe/fetch13_img.py use      # 束に入れる21点（幅3000px の版）
    python ref/ep13/probe/fetch13_img.py preview  # 未見9点＋C4 の見本（幅640px）→ ref/ep13/img/preview/
"""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
IMG = HERE / "img"
API = "https://commons.wikimedia.org/w/api.php"
UA = "zukai-engine-research/0.1 (https://github.com/; konariri8 research) python-urllib"

USE = {  # materials.md §3 の番号 → Commons の題名
    "A1": "TC-JAV (5920254289) (2).jpg",
    "A2": "TC-JAV (6004629408).jpg",
    "A3": "TC-JAV, Turkish DC-10 (6060110163).jpg",
    "A4": "THY Türk Hava Yolları - Turkish Airlines McDonnell Douglas DC-10-10 London - Heathrow 1973.jpg",
    "A5": "N103AA American DC-10-10 at KSFO.jpg",
    "A6": "Photo of American Airlines Flight 96 cargo door.jpg",
    "B1": "Paris DC-10 Crash- March 3, 1974.jpg",
    "B2": "Paris DC-10 Crash, Names.jpg",
    "B3": "Stèle du crash aérien de 1974 (parcelle 144).jpg",
    "B4": "Monument DC10 Ermenonville-1.jpg",
    "C1": "Eerste DC 10 voor KLM landt op Schiphol, Bestanddeelnr 926-1070.jpg",
    "C2": "Eerste DC 10 voor KLM landt op Schiphol, DC 10 op platform, Bestanddeelnr 926-1071.jpg",
    "C3": "Eerste DC 10 voor KLM landt op Schiphol, cockpit en interieur, Bestanddeelnr 926-1073.jpg",
    "C4": "Vlucht met DC-10 naar Nice, cockpit DC-10 met piloten, Bestanddeelnr 926-2653.jpg",
    "C5": "American Airlines McDonnell Douglas DC-10 01.jpg",
    "C6": "Korean Air Lines McDonnell Douglas DC-10 N198 01.jpg",
    "D1": "United Airlines DC-10 N1826U.jpg",
    "D2": "McDonnell Douglas DC-10 N1803U (C15-10).jpg",
    "D3": "McDonnell Douglas DC-10 interior (CJ406257).jpg",
    "D5": "Douglas DC-10-10 TC-JAU THY FRA 28.07.74 edited-2.jpg",
    "D6": "Finnairin DC-10 lentokone lentokentällä 1970 (HK7137-875).tif",
    # ⑤b-2 で見本（640px）を見て採った（c209・1970年ごろのオルリーの出発ロビー・BY-SA＝額装）
    "O1": "Departure hall at Paris-Orly airport (LBS SR04-038169).tif",
}
PREVIEW = {  # 未見（materials.md §3-4・§3-5）＋ C4（題名は「操縦室」・台帳は「タラップ」＝絵で確かめる）
    "O1": "Departure hall at Paris-Orly airport (LBS SR04-038169).tif",
    "O2": "Air France 747 (6074711768).jpg",
    "O3": "ORY 4X-ATR 5 73 Dietrich Eggert.jpg",
    "K1": "Eerste DC 10 voor KLM landt op Schiphol, DC 10 op platform, Bestanddeelnr 926-1072.jpg",
    "K2": "Eerste DC 10 voor KLM landt op Schiphol, cockpit en interieur, Bestanddeelnr 926-1074.jpg",
    "K3": "Vlucht met DC-10 naar Nice, interieur vliegtuig, Bestanddeelnr 926-2651.jpg",
    "K4": "Vlucht met DC-10 naar Nice, ontvangst door stadsbestuur van Nice, Bestanddeelnr 926-2652.jpg",
    "K5": "Vlucht met DC-10 naar Nice, gasten kijken uit over Nice, Bestanddeelnr 926-2654.jpg",
    "K6": "Vlucht met DC-10 naar Nice, groepsfoto voor DC-10 in Nice, Bestanddeelnr 926-2655.jpg",
    "C4": USE["C4"],
}


def get(url, tries=5):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            print(f"   429 → {20 * (k + 1)}秒待つ")
            time.sleep(20 * (k + 1))


def info(titles, width):
    q = urllib.parse.urlencode(dict(action="query", titles="|".join("File:" + t for t in titles),
                                    prop="imageinfo", iiprop="url|size|sha1|mime|extmetadata",
                                    iiurlwidth=width, format="json"))
    js = json.loads(get(API + "?" + q))
    norm = {n["to"]: n["from"] for n in js["query"].get("normalized", [])}
    out = {}
    for p in js["query"]["pages"].values():
        t = norm.get(p["title"], p["title"])[5:]
        ii = (p.get("imageinfo") or [None])[0]
        if not ii:
            raise SystemExit(f"🔴 {t}: imageinfo が無い（題名の誤り？）")
        em = ii.get("extmetadata", {})
        out[t] = dict(orig=ii["url"], w=ii["width"], h=ii["height"], sha1=ii["sha1"], mime=ii["mime"],
                      thumb=ii.get("thumburl"), tw=ii.get("thumbwidth"), th=ii.get("thumbheight"),
                      lic=(em.get("LicenseShortName") or {}).get("value", ""),
                      artist=(em.get("Artist") or {}).get("value", ""),
                      date=(em.get("DateTimeOriginal") or {}).get("value", ""))
    return out


def run(table, width, dest, big_only):
    dest.mkdir(parents=True, exist_ok=True)
    man_p = dest / "fetched.json"
    man = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}
    titles = list(table.values())
    meta = {}
    # ⚠️ 20件まとめて（extmetadata つき）問うと 429 が5回続いた（09-24）。1件なら通る＝5件ずつに割る
    for i in range(0, len(titles), 5):
        meta.update(info(titles[i:i + 5], width))
        time.sleep(3)
    tot = 0
    for key, t in table.items():
        m = meta[t]
        use_orig = big_only and m["w"] <= width and m["mime"] == "image/jpeg"
        url = m["orig"] if use_orig else m["thumb"]
        stem = t.rsplit(".", 1)[0]
        out = dest / f"{stem}.jpg"
        if out.exists() and man.get(t, {}).get("url") == url:
            print(f"= {key} {out.name}（取得ずみ）")
            continue
        data = get(url)
        out.write_bytes(data)
        tot += len(data)
        man[t] = dict(key=key, url=url, file=out.name, bytes=len(data), md5=hashlib.md5(data).hexdigest(),
                      got_w=m["w"] if use_orig else m["tw"], orig_w=m["w"], orig_h=m["h"],
                      orig_sha1=m["sha1"], orig_url=m["orig"], lic=m["lic"], artist=m["artist"], date=m["date"],
                      fetched="2026-09-24")
        print(f"✓ {key} {len(data) / 1e6:5.2f}MB  {man[t]['got_w']}px（原寸 {m['w']}x{m['h']}・{m['lic']}）  {out.name}")
        time.sleep(1.0)
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"計 {tot / 1e6:.1f}MB → {dest}")


def run_direct(table, dest):
    """API を通さず、②の控え（`sheet13_index.tsv` の原本 URL）から直接取る（09-24・API が 429 を返し続けた）。

    ⚠️ API は「You are making too many requests to the API」（Retry-After 1〜8秒）を、20〜80秒待っても返し続けた。
       原本のファイルは upload.wikimedia.org の静的な配信＝API の回数制限の外。
    大きい2点（B2 12.4MB・D6 TIFF 37MB）は標準の 1920px 版（どちらも額装で小さく出す点）。
    権利・撮影者・日付は②の生データ `commons_ep13.json` から引く（取ったファイルの md5 は控えに）。
    """
    import re
    dest.mkdir(parents=True, exist_ok=True)
    man_p = dest / "fetched.json"
    man = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}
    idx = {}
    for ln in (HERE / "sheet13_index.tsv").read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        idx[f[0]] = dict(title=f[1][5:], wh=f[2], lic=f[3], url=f[4].split("?")[0])
    raw = {x["title"][5:]: x for x in json.loads((HERE / "commons_ep13.json").read_text(encoding="utf-8"))}
    # O1＝⑤b-2 で見本を見て採った点（②の控え sheet13_index.tsv に無い）＝Commons の生データの URL から引く
    for key, t in table.items():
        if key not in idx:
            x = raw[t]
            idx[key] = dict(title=t, wh=f"{x['w']}x{x['h']}", lic=x.get("license", ""), url=x["url"].split("?")[0])
    THUMB1920 = {"B2", "D6", "O1"}
    tot = 0
    for key, t in table.items():
        r = idx[key]
        if r["title"] != t:
            raise SystemExit(f"🔴 {key}: 控えの題名 {r['title']!r} が表 {t!r} と違う")
        u = r["url"]
        if key in THUMB1920:
            m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$", u)
            name = m.group(3)
            pre = "lossy-page1-" if name.lower().endswith((".tif", ".tiff")) else ""
            suf = ".jpg" if pre else ""
            u = (f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{name}/"
                 f"{pre}1920px-{name}{suf}")
        stem = t.rsplit(".", 1)[0]
        out = dest / f"{stem}.jpg"
        if out.exists() and man.get(t, {}).get("url") == u:
            print(f"= {key} {out.name}（取得ずみ）")
            continue
        data = get(u)
        out.write_bytes(data)
        tot += len(data)
        x = raw.get(t, {})
        man[t] = dict(key=key, url=u, file=out.name, bytes=len(data), md5=hashlib.md5(data).hexdigest(),
                      orig_wh=r["wh"], lic=x.get("license") or r["lic"], artist=x.get("artist", ""),
                      date=x.get("date", ""), credit=x.get("credit", ""), fetched="2026-09-24",
                      thumb1920=key in THUMB1920)
        print(f"✓ {key} {len(data) / 1e6:5.2f}MB  {'1920px 版' if key in THUMB1920 else '原本 ' + r['wh']}"
              f"（{man[t]['lic']}）  {out.name}")
        time.sleep(2.0)
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"計 {tot / 1e6:.1f}MB → {dest}")


if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["use"])[0]
    if cmd == "use":
        run_direct(USE, IMG)
    elif cmd == "preview":
        run(PREVIEW, 640, IMG / "preview", big_only=False)
    else:
        raise SystemExit(f"知らない命令: {cmd}")
