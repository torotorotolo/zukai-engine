# -*- coding: utf-8 -*-
"""12本目②：Commons の素材を1点1行の生データで落とす（重複を除いた実数を出すため）。

なぜ専用の採取が要るか
  - `commons_catlist.py` は読むための一覧で、**ライセンスの根拠**（米連邦§105 か
    日本の旧法PDか）を分けていない → [[feedback-pd-label-hides-two-different-grounds]]
  - 3つの検索語・8つの分類が重なっているので、**pageid で重複を除かないと実数が出ない**

出すもの: ref/ep12/commons_ep12.json（1点1レコード・生の値）
  pageid / title / width / height / mime / duration / bitdepth
  license_short / usage_terms / credit / artist / date_original / desc
  cats（隠しカテゴリ込み。PD-USGov か PD-Japan かはここで分かる）
  via（どの分類から来たか。複数可）
"""
import json
import sys
import time
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "zukai-engine-ep12-probe/1.0 (research; contact via github torotorotolo)"

# 深さ2で歩く（この回の題材そのもの）
CATS = [
    "Category:Castle Bravo",
    "Category:Operation Castle",
    "Category:Daigo Fukuryū Maru Incident",
    "Category:Victims of the Daigo Fukuryū Maru Incident",
    "Category:Aikichi Kuboyama",
    "Category:Rongelap Atoll",
    "Category:Daigo Fukuryū Maru (ship, 1947)",
    "Category:Atomic tuna",
]
# ⚠️ 深さ0でしか歩かない（子まで降りると数千点＝Commons に 429 で止められる。実際に止まった）
CATS_SHALLOW = [
    "Category:Bikini Atoll",
    "Category:Nuclear weapon tests of the United States",
    "Category:Castle Romeo",
]
# 分類に入っていない物を拾うための全文検索（題名のみ）
SEARCHES = [
    "Castle Bravo",
    "Operation Castle 1954",
    "Bikini Atoll 1954",
    "Daigo Fukuryu Maru",
    "Lucky Dragon 1954",
    "Rongelap 1954",
    "Bravo fallout",
]


def get(**params):
    params.setdefault("format", "json")
    params.setdefault("formatversion", "2")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
            time.sleep(2.5)  # 429（要求が多すぎ）に当たったので間を空ける
            return d
        except Exception as e:  # 通信は落ちる。待って再試行
            if attempt == 5:
                raise
            wait = 5 * (attempt + 1)
            sys.stderr.write("retry %s (%ss): %s\n" % (attempt, wait, e))
            time.sleep(wait)


def walk_cat(cat, depth, seen_cats, out):
    """cat 以下のファイル名を out（title -> 由来の集合）に足す。"""
    if cat in seen_cats:
        return
    seen_cats.add(cat)
    cont = {}
    while True:
        d = get(action="query", list="categorymembers", cmtitle=cat,
                cmlimit=500, cmtype="file|subcat", **cont)
        for m in d.get("query", {}).get("categorymembers", []):
            if m["title"].startswith("Category:"):
                if depth > 0:
                    walk_cat(m["title"], depth - 1, seen_cats, out)
            else:
                out.setdefault(m["title"], set()).add(cat)
        if "continue" in d:
            cont = d["continue"]
        else:
            break


def walk_search(q, out):
    """題名で当てる（intitle: は使わない＝Commons の索引が弱いので全文）。"""
    cont = {}
    got = 0
    while got < 200:
        d = get(action="query", list="search", srsearch=q, srnamespace=6,
                srlimit=100, **cont)
        hits = d.get("query", {}).get("search", [])
        for s in hits:
            out.setdefault(s["title"], set()).add("search:" + q)
        got += len(hits)
        if "continue" in d and hits:
            cont = d["continue"]
        else:
            break


def detail(titles):
    """50点ずつ imageinfo と categories を取る。"""
    rows = []
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        d = get(action="query", titles="|".join(chunk),
                prop="imageinfo|categories",
                iiprop="url|size|mime|extmetadata|bitdepth|mediatype",
                iiextmetadatafilter=("LicenseShortName|UsageTerms|Credit|Artist"
                                     "|DateTimeOriginal|ImageDescription"
                                     "|ObjectName|DateTime|Permission"),
                cllimit=500, clshow="!hidden")
        for p in d.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]
            md = ii.get("extmetadata") or {}

            def v(k):
                return (md.get(k) or {}).get("value", "")

            rows.append({
                "pageid": p.get("pageid"),
                "title": p.get("title", ""),
                "width": ii.get("width", 0),
                "height": ii.get("height", 0),
                "mime": ii.get("mime", ""),
                "mediatype": ii.get("mediatype", ""),
                "bitdepth": ii.get("bitdepth"),
                "duration": ii.get("duration"),
                "url": ii.get("url", ""),
                "license_short": v("LicenseShortName"),
                "usage_terms": v("UsageTerms"),
                "credit": v("Credit"),
                "artist": v("Artist"),
                "date_original": v("DateTimeOriginal") or v("DateTime"),
                "desc": v("ImageDescription"),
                "object": v("ObjectName"),
                "cats": [c["title"][9:] for c in (p.get("categories") or [])],
            })
        sys.stderr.write("detail %d/%d\n" % (min(i + 50, len(titles)), len(titles)))
    return rows


def main():
    out = {}
    for c in CATS:
        walk_cat(c, 2, set(), out)
        sys.stderr.write("cat %s -> %d\n" % (c, len(out)))
    for c in CATS_SHALLOW:
        walk_cat(c, 0, set(), out)
        sys.stderr.write("cat0 %s -> %d\n" % (c, len(out)))
    for q in SEARCHES:
        walk_search(q, out)
        sys.stderr.write("search %s -> %d\n" % (q, len(out)))

    titles = sorted(out)
    rows = detail(titles)
    for r in rows:
        r["via"] = sorted(out.get(r["title"], []))
    with open("ref/ep12/commons_ep12.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print("集めた題名 %d / 明細 %d" % (len(titles), len(rows)))


if __name__ == "__main__":
    main()
