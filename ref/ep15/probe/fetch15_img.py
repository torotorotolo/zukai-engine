# -*- coding: utf-8 -*-
"""15本目⑤b-6：Commons の写真を `ref/ep15/img/` に取る（2026-09-30・14本目の `ref/ep14/probe/fetch14_img.py` の形）。

■ 題名は②の台帳 `ref/ep15/materials.md` §3 の記号 → ②の生データ `ref/ep15/commons_ep15.json`（466点）から機械で引いた。
■ 取るのは **カズヤくんの許可のあと**（`use`）。**原寸を取り、Commons の SHA-1 と照合する**
  （束 `qa_out/ep15_assets.py build` は幅3000px に縮める）。縮小版にしない理由＝指紋で「落としかけ」と取り違えを止められる
  （→ [[feedback-download-size-is-not-completion]]）。
■ 控え＝`ref/ep15/img/meta.json`（鍵 → 題名・原寸・権利・撮影者・日付・原本の SHA-1・URL）と
  `ref/ep15/img/fetched.json`（題名 → 取った URL・バイト数・md5）

    python ref/ep15/probe/fetch15_img.py meta     # 題名を引いて情報だけ（画像は落とさない）
    python ref/ep15/probe/fetch15_img.py use      # 許可のあと：束に入れる点を取る
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
BIG = 3840   # 情報の縮小版の幅（取るのは原寸）

# 鍵（materials.md §3 の記号）→ 題名（"File:" なし）。当てるカットは `qa_out/ep15_assets.py` の PICK
WANT = {
    # 事故の週の事故機（tataquax・CC BY-SA 2.0＝額装・1点1カット）§3-1
    "B4": "Reno Air Races 2011 (6452065839).jpg",     # c205 飛んでいる事故機を真下から（事故のレースの周回中＝推定）
    "A5": "Reno Air Races 2011 (6452065605).jpg",     # c208 最後の離陸の滑走
    "A6": "Jimmy Leeward's Galloping Ghost at 2011 Reno Air Races.jpg",   # c401 前日（9/15）の地上を走る事故機
    "B5": "Reno Air Races 2011 (6452063939).jpg",     # c419 事故の日の朝のピットの機首
    "B6": "Reno Air Races 2011 (6452062347).jpg",     # c504 事故の週（9/14）のピットの全身
    # 事故の日の会場と同じレースの機（tataquax・BY-SA 2.0）§3-2
    "A1": "Reno Air Races 2011 (6361173745).jpg",     # c207 ストレガのタキシング
    "A3": "Reno Air Races 2011 (6450673359).jpg",     # c203 ヴードゥーのタキシング
    "A4": "Reno Air Races 2011 (6361174323).jpg",     # c202 ストレガの離陸の滑走
    "B2": "Reno Air Races 2011 (6361174465).jpg",     # c219 ストレガを真下から
    "B3": "Reno Air Races 2011 (6450673505).jpg",     # c318 ヴードゥーを真下から
    "E70": "Reno Air Races 2011 (6179482685).jpg",    # c801 ピットの機体の奥の満員の観客席（遠景）
    "E85": "Reno Air Races 2011 (6225303046).jpg",    # c204 レースのパイロンと上に立つ審判
    # 来歴（Bill Larkins・BY-SA 2.0）§3-3
    "C1": "P-51n79111side69 (5658262832).jpg",        # c405 1969年の「ミス・キャンディス」
    "C2": "P-51n79111side70 (5658262932).jpg",        # c406 1970年のタキシング
    "C3": "P-51 N79111 after damage 1970 (6161387830).jpg",   # c407 1970年・損傷のあと
    # 2010年の事故機（jeggernot・CC BY 2.0）§3-4
    "C4": "Galloping Ghost.jpg",                      # c417 機首（右の人を切り落とす）
    "C5": "GallopingGhost 2010-09-18.jpg",            # c416 ピットの全身
    # 会場（§3-5）
    "D4": "Reno Stead Field (3392833169).jpg",        # c112 空港の空撮（2009・BY-SA 2.0）
    "D5": "2016 National Championship Air Races Pylon Racing Seminar by Don Ramey Logan.jpg",   # c906（2016・CC BY 4.0）
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
    meta = {}
    ks = list(WANT)
    for i in range(0, len(ks), 5):
        got = info([WANT[k] for k in ks[i:i + 5]])
        for k in ks[i:i + 5]:
            meta[k] = dict(title=WANT[k], **(got.get(WANT[k]) or dict(missing=True)))
        time.sleep(3)
    (IMG / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = 0
    for k, m in meta.items():
        if m.get("missing"):
            print(f"🔴 {k:5} 無い: {m['title']}")
            continue
        tot += m["bytes"]
        print(f"{k:5} {m['w']}x{m['h']} {m['bytes'] / 1e6:5.2f}MB {m['lic']:14} {m['date'][:16]:16} {m['title']}")
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
                               date=m["date"], page=m["page"], fetched="2026-09-30")
        print(f"✓ {key:5} {len(data) / 1e6:5.2f}MB  原寸 {m['w']}x{m['h']}・SHA-1 一致・{m['lic']}")
        time.sleep(1.5)
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"計 {tot / 1e6:.1f}MB → {IMG}")
    return 0


if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["meta"])[0]
    sys.exit({"meta": cmd_meta, "use": cmd_use}[cmd]())
