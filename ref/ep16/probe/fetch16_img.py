# -*- coding: utf-8 -*-
"""16本目⑤b-7：Commons の写真を `ref/ep16/img/` に取る（2026-10-02・15本目の `ref/ep15/probe/fetch15_img.py` の形）。

■ 題名は**手で写さない**：章ファイルの PLAN（kind＝写真）の画の欄にある `#NNN` → ②の台帳 `ref/ep16/photos_commons.tsv`
  （1点1行の正本）の title から機械で引く。Google Earth のカット（番号なし）は入らない。
■ 取るのは **カズヤくんの許可のあと**（`use`）。**原寸を取り、Commons の SHA-1 と照合する**
  （束 `qa_out/ep16_assets.py build` は幅3000px に縮める）。縮小版にしない理由＝指紋で「落としかけ」と取り違えを止められる
  （→ [[feedback-download-size-is-not-completion]]）。
■ #100（IGM 1934年の地形図）は ⑤b-1 に取った `ref/ep16/src/igm1934.jpg` を Commons の SHA-1 と照らすだけ（取り直さない）。
■ 控え＝`ref/ep16/img/meta.json`（鍵 → 題名・原寸・権利・撮影者・日付・原本の SHA-1・URL・使うカット）と
  `ref/ep16/img/fetched.json`（題名 → 取った URL・バイト数・md5・SHA-1）

    python ref/ep16/probe/fetch16_img.py meta     # 題名を引いて情報だけ（画像は落とさない）
    python ref/ep16/probe/fetch16_img.py use      # 許可のあと：束に入れる点を取る
"""
import csv
import hashlib
import importlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]          # ref/ep16
REPO = HERE.parents[1]
IMG = HERE / "img"
API = "https://commons.wikimedia.org/w/api.php"
# ⚠️ 名乗りにメールアドレス（とその前半）を入れない（13本目の道具から写したら入っていた＝09-29 に替えた）
UA = "zukai-engine-research/0.1 (https://github.com/torotorotolo/zukai-engine) python-urllib"
BIG = 3840   # 情報の縮小版の幅（取るのは原寸）
LOCAL = {"#100": HERE / "src" / "igm1934.jpg"}     # すでに手元にある点（取らない・SHA-1 を照らすだけ）
CHAPTERS = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ca", "cb"]
# PLAN に無いが見比べる候補（2026-10-02 ⑤b-7）：PLAN の c206「#073 建設中のダム」・c208「#075 建設中のダム」は、
#   台帳では #073＝1956年のアーチ橋の工事・#075＝1958年の管の橋＝ダムが写っているか分からない →
#   同じ記録（BY-SA）のダムの点を並べて見て、語りに合う方を使う（BY-SA は1点1カット）
EXTRA = {"#074": "c206", "#080": "c208"}


def want():
    """PLAN（kind＝写真）の画の欄の #NNN → {鍵: (題名, [カット])}。台帳に無い番号は止める。"""
    sys.path.insert(0, str(REPO / "tools"))
    plan = {}
    for ch in CHAPTERS:
        plan.update(importlib.import_module("cuts." + ch).PLAN)
    uses = {}
    for cid, v in sorted(plan.items()):
        if v["kind"] != "写真":
            continue
        for n in dict.fromkeys(re.findall(r"#(\d{3})", v["plan"])):
            uses.setdefault("#" + n, []).append(cid)
    for k, cid in EXTRA.items():
        uses.setdefault(k, []).append(cid + "（候補）")
    with open(HERE / "photos_commons.tsv", encoding="utf-8") as f:
        rows = {r["id"]: r for r in csv.DictReader(f, delimiter="\t")}
    miss = sorted(set(uses) - set(rows))
    if miss:
        raise SystemExit(f"🔴 台帳 photos_commons.tsv に無い番号: {miss}")
    return {k: (rows[k]["title"], uses[k]) for k in sorted(uses)}


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
    W = want()
    meta = {}
    ks = list(W)
    for i in range(0, len(ks), 5):
        got = info([W[k][0] for k in ks[i:i + 5]])
        for k in ks[i:i + 5]:
            meta[k] = dict(title=W[k][0], cuts=W[k][1], **(got.get(W[k][0]) or dict(missing=True)))
        time.sleep(3)
    (IMG / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = n = 0
    for k, m in meta.items():
        if m.get("missing"):
            print(f"🔴 {k:5} 無い: {m['title']}")
            continue
        if k in LOCAL:
            have = hashlib.sha1(LOCAL[k].read_bytes()).hexdigest() if LOCAL[k].exists() else "（無い）"
            print(f"{k:5} {m['w']}x{m['h']} 手元 {LOCAL[k].name}＝SHA-1 {'一致' if have == m['sha1'] else '🔴 違う ' + have}"
                  f"（取らない）  {m['lic']:14} {m['title']}")
            continue
        tot += m["bytes"]
        n += 1
        print(f"{k:5} {m['w']}x{m['h']} {m['bytes'] / 1e6:5.2f}MB {m['lic']:16} {m['date'][:16]:16} "
              f"{m['title']}  ← {' '.join(m['cuts'])}")
    print(f"取る点 {n}・原寸の合計 {tot / 1e6:.1f}MB → {IMG / 'meta.json'}")
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
        if key in LOCAL:
            have = hashlib.sha1(LOCAL[key].read_bytes()).hexdigest()
            if have != m["sha1"]:
                raise SystemExit(f"🔴 {key}: 手元の {LOCAL[key].name} の SHA-1 が Commons の原本と違う")
            print(f"= {key} {LOCAL[key].name}（手元・SHA-1 一致＝取らない）")
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
                               date=m["date"], page=m["page"], fetched="2026-10-02")
        print(f"✓ {key:5} {len(data) / 1e6:5.2f}MB  原寸 {m['w']}x{m['h']}・SHA-1 一致・{m['lic']}")
        time.sleep(1.5)
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"計 {tot / 1e6:.1f}MB → {IMG}")
    return 0


if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["meta"])[0]
    sys.exit({"meta": cmd_meta, "use": cmd_use}[cmd]())
