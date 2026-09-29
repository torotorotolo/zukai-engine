# -*- coding: utf-8 -*-
"""14本目⑤b-7a：Commons の写真を `ref/ep14/img/` に取る（2026-09-29・13本目の `ref/ep13/probe/fetch13_img.py` の形）。

■ ②の控え（scratchpad の `cm14.json`・482点）は消えていた＝題名は②の台帳 `ref/ep14/materials.md` §3 の
  番号・Flickr ID・VIRIN から**Commons に問い合わせて引き直す**（`meta`＝情報だけ・画像は落とさない）。
■ 取るのは **カズヤくんの許可のあと**（`use`）。**原寸を取り、Commons の SHA-1 と照合する**（合計 約30MB・
  束 `qa_out/ep14_assets.py build` は幅3000px に縮める）。縮小版にしない理由＝指紋で「落としかけ」と取り違えを止められる
  （→ [[feedback-download-size-is-not-completion]]）。
■ 控え＝`ref/ep14/img/meta.json`（鍵 → 題名・原寸・権利・撮影者・日付・原本の SHA-1・URL）と
  `ref/ep14/img/fetched.json`（題名 → 取った URL・バイト数・md5）

    python ref/ep14/probe/fetch14_img.py meta     # 題名を引き直して情報だけ（画像は落とさない）
    python ref/ep14/probe/fetch14_img.py use      # 許可のあと：束に入れる点を取る
"""
import hashlib
import json
import re
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
# ⚠️ 名乗りにメールアドレス（とその前半）を入れない（13本目の道具から写したら入っていた＝09-29 に替えた）
UA = "zukai-engine-research/0.1 (https://github.com/torotorotolo/zukai-engine) python-urllib"
BIG = 3840   # これを超える原寸は標準の縮小版（3840px）を取る

# 鍵（materials.md §3 の記号・番号）→ 題名（"File:" なし）か、("search", 検索語)
WANT = {
    # 船そのもの（§3-3）・当日（§3-4）
    "H1": "South-Korea-Ferry-Sewol-sinking.jpg",
    "K1": "Ferry Sewol 1.jpg",
    "J1": "Ferry Naminoue 20100214.jpg",
    "M1": "2017 MV Sewol in Mokpo New Port.jpg",
    # 米軍（§3-2・PD）
    "N28": ("search", "140418-N-LM312-287"),
    "N34": ("search", "140420-N-NT265-348"),
    # 捜索（§3-1・韓国国防部・CC BY-SA 2.0）＝Flickr ID で引く
    "F2": ("search", "13947445037"),
    "F4": ("search", "13947458749"),
    "F6": ("search", "13956410506"),
    "F8": ("search", "13976287932"),
    "F11": ("search", "13979938264"),
    "F12": ("search", "13979939304"),
    "F13": ("search", "13999503253"),
    "F15": ("search", "13999504453"),
    "F17": ("search", "14134129785"),
    "F19": ("search", "14134384094"),
    "F20": ("search", "14154193263"),
    # 追悼・その後（§3-5）
    "TW46": "Tanwon School 5.jpg",
    "TW48": "Tanwon School 7.jpg",
    "P1": "Sewol memorial ribbons, Seoul Plaza, 2014-06-22.jpg",
    "AN74": "Memorial for the victims of the sinking of the MV Sewol 01.JPG",   # 拡張子は大文字（09-29 に検索で確かめた）
    "G2": "Memorial place of the MV Sewol on Gwanghwamun Plaza in 2018 - 2.jpg",
    "L1": "Lost Children (191940227).jpeg",
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


def api(**q):
    q.setdefault("format", "json")
    return json.loads(get(API + "?" + urllib.parse.urlencode(q)))


def search(term):
    js = api(action="query", list="search", srsearch=term, srnamespace=6, srlimit=5)
    return [h["title"][5:] for h in js["query"]["search"]]


def _plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(s or ""))).strip()


def info(titles):
    js = api(action="query", titles="|".join("File:" + t for t in titles), prop="imageinfo",
             iiprop="url|size|sha1|mime|extmetadata", iiurlwidth=BIG)
    norm = {n["to"]: n["from"] for n in js["query"].get("normalized", [])}
    out = {}
    for p in js["query"]["pages"].values():
        t = norm.get(p["title"], p["title"])[5:]
        ii = (p.get("imageinfo") or [None])[0]
        if not ii:
            out[t] = None   # 無い（削除された・題名の誤り）
            continue
        em = ii.get("extmetadata", {})
        g = lambda k: _plain((em.get(k) or {}).get("value", ""))
        out[t] = dict(orig=ii["url"], w=ii["width"], h=ii["height"], bytes=ii["size"], sha1=ii["sha1"],
                      mime=ii["mime"], thumb=ii.get("thumburl"), tw=ii.get("thumbwidth"),
                      lic=g("LicenseShortName"), artist=g("Artist"), credit=g("Credit")[:200],
                      date=g("DateTimeOriginal"), desc=g("ImageDescription")[:300],
                      page="https://commons.wikimedia.org/wiki/File:" + t.replace(" ", "_"))
    return out


def cmd_meta():
    IMG.mkdir(parents=True, exist_ok=True)
    titles = {}
    for key, v in WANT.items():
        if isinstance(v, tuple):
            hits = search(v[1])
            time.sleep(1.0)
            if len(hits) != 1:
                print(f"⚠️ {key} 「{v[1]}」の検索が {len(hits)}件: {hits}")
            if not hits:
                continue
            titles[key] = hits[0]
        else:
            titles[key] = v
    meta = {}
    ks = list(titles)
    for i in range(0, len(ks), 5):
        got = info([titles[k] for k in ks[i:i + 5]])
        for k in ks[i:i + 5]:
            meta[k] = dict(title=titles[k], **(got.get(titles[k]) or dict(missing=True)))
        time.sleep(3)
    (IMG / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = 0
    for k, m in meta.items():
        if m.get("missing"):
            print(f"🔴 {k:5} 無い: {m['title']}")
            continue
        tot += m["bytes"]
        print(f"{k:5} {m['w']}x{m['h']} {m['bytes'] / 1e6:5.1f}MB {m['lic']:14} {m['date'][:10]:10} {m['title']}")
    print(f"原寸の合計 {tot / 1e6:.1f}MB・{sum(1 for m in meta.values() if not m.get('missing'))}点 → {IMG / 'meta.json'}")
    return 0


def cmd_use():
    meta = json.loads((IMG / "meta.json").read_text(encoding="utf-8"))
    man_p = IMG / "fetched.json"
    man = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}
    tot = 0
    for key, m in meta.items():
        if m.get("missing"):
            print(f"🔴 {key}: 無い＝取らない（{m['title']}）")
            continue
        url = m["orig"]
        stem = m["title"].rsplit(".", 1)[0]
        out = IMG / f"{stem}.jpg"
        if out.exists() and man.get(m["title"], {}).get("url") == url:
            print(f"= {key} {out.name}（取得ずみ）")
            continue
        data = get(url)
        sha1 = hashlib.sha1(data).hexdigest()
        if sha1 != m["sha1"] or len(data) != m["bytes"]:
            raise SystemExit(f"🔴 {key}: 取った {len(data)}B・SHA-1 {sha1} が Commons の {m['bytes']}B・{m['sha1']} と違う")
        out.write_bytes(data)
        tot += len(data)
        man[m["title"]] = dict(key=key, url=url, file=out.name, bytes=len(data), md5=hashlib.md5(data).hexdigest(),
                               sha1=sha1, orig_w=m["w"], orig_h=m["h"], lic=m["lic"], artist=m["artist"],
                               date=m["date"], page=m["page"], fetched="2026-09-29")
        print(f"✓ {key:5} {len(data) / 1e6:5.2f}MB  原寸 {m['w']}x{m['h']}・SHA-1 一致・{m['lic']}")
        time.sleep(1.5)
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"計 {tot / 1e6:.1f}MB → {IMG}")
    return 0


# 動く映像（DVIDS・米国の職務著作＝PD）。頁の窓「Download Video」の 1920x1080 は www.dvidshub.net の窓口が
#   curl に 403（検問）＝配信の置き場 CloudFront の**原本**（`DOD_<番号>.mp4`）を取る。大きさは窓の表示と一致を HEAD で確かめた
#   （E-1＝111,457,456B・窓「106 MB」／E-2＝144,787,410B）。09-29 カズヤくん許可
VIDS = {
    "e1": dict(page="https://www.dvidshub.net/video/330919/", dvids=330919, date="2014-04-18", sec="1:30",
               media="https://d34w7g4gy10iej.cloudfront.net/video/1404/DOD_101385880/DOD_101385880.mp4",
               bytes=111457456, title="USS Bonhomme Richard (LHD 6) Assists in Capsized ROK Ferry Search and Rescue Efforts",
               by="MC3 Christian Senyk（米海軍）"),
    "e2": dict(page="https://www.dvidshub.net/video/332722/sewol-ferry-sar-efforts-31st-meu", dvids=332722,
               date="2014-04-19", sec="2:02",
               media="https://d34w7g4gy10iej.cloudfront.net/video/1404/DOD_101470723/DOD_101470723.mp4",
               bytes=144787410, title="Sewol Ferry SAR Efforts 31st MEU", by="LCpl Alexander Pool（米海兵隊）"),
}


def cmd_vid():
    """⚠️ 落としかけのファイルを測らない＝大きさの一致と md5 を2回（→ [[feedback-download-size-is-not-completion]]）。"""
    vd = HERE / "vid"
    vd.mkdir(parents=True, exist_ok=True)
    man_p = vd / "fetched.json"
    man = json.loads(man_p.read_text(encoding="utf-8")) if man_p.exists() else {}
    for key, v in VIDS.items():
        out = vd / f"{key}.mp4"
        if out.exists() and out.stat().st_size == v["bytes"] and man.get(key, {}).get("md5"):
            print(f"= {key} 取得ずみ（{v['bytes']}B）")
            continue
        tmp = out.with_suffix(".part")
        with urllib.request.urlopen(urllib.request.Request(v["media"], headers={"User-Agent": UA}), timeout=120) as r, \
                open(tmp, "wb") as f:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
        n = tmp.stat().st_size
        if n != v["bytes"]:
            raise SystemExit(f"🔴 {key}: {n}B（HEAD の {v['bytes']}B と違う＝落としかけ）")
        md5a = hashlib.md5(tmp.read_bytes()).hexdigest()
        md5b = hashlib.md5(tmp.read_bytes()).hexdigest()
        if md5a != md5b:
            raise SystemExit(f"🔴 {key}: md5 が2回で違う")
        tmp.replace(out)
        man[key] = dict(v, file=f"ep14/vid/{key}.mp4", md5=md5a, fetched="2026-09-29")
        print(f"✓ {key} {n / 1e6:.1f}MB md5 {md5a}")
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["meta"])[0]
    sys.exit({"meta": cmd_meta, "use": cmd_use, "vid": cmd_vid}[cmd]())
