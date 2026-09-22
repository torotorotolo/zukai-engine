# -*- coding: utf-8 -*-
"""Commons にある「PD の動く映像」を題材の側から探す。

なぜ逆に探すか＝このchで当たった回（SL-1・スレッシャー・コロンビア号・9.11・キー橋）は
すべて**動く映像を持っていた**。写真は後から足せるが、動く映像は在るか無いかしかない。
→ 先に「動く映像が在る事故」を列挙し、そこへ需要を当てる。

使い方:
  python pd_videos.py cats "Chemical Safety"        # カテゴリ名を探す
  python pd_videos.py vids "Category:..." [深さ]    # そのカテゴリの動画を測る
  python pd_videos.py search "<語>"                 # 動画だけを題名で探す
"""
import sys, json, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "zukai-engine-theme-probe/1.0 (research; contact via github torotorotolo)"


def get(**params):
    params.setdefault("format", "json")
    params.setdefault("formatversion", "2")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def show(items):
    """1点1行。幅x高 / 秒 / ライセンス / 題"""
    n_ok = 0
    for it in items:
        ii = (it.get("imageinfo") or [{}])[0]
        md = (ii.get("extmetadata") or {})
        lic = (md.get("LicenseShortName", {}) or {}).get("value", "?")
        w, h = ii.get("width", 0), ii.get("height", 0)
        dur = ii.get("duration") or 0
        mime = ii.get("mime", "")
        if not mime.startswith("video"):
            continue
        mark = "🔴" if w >= 1280 else "  "
        sa = "SA継承" if "SA" in lic.upper().replace("-", "") and "BY" in lic.upper() else ""
        if w >= 1280 and not sa:
            n_ok += 1
        print(f"{mark} {w:>5}x{h:<5} {dur:>7.1f}s {lic:<22}{sa:<6} "
              f"{it['title'][5:90]}")
    print(f"--- 幅1280以上かつ継承なし: {n_ok}点 / 動画 "
          f"{sum(1 for i in items if (i.get('imageinfo') or [{}])[0].get('mime','').startswith('video'))}点")


mode = sys.argv[1]
arg = sys.argv[2]

if mode == "cats":
    d = get(action="query", list="search", srsearch=arg,
            srnamespace=14, srlimit=40)
    for s in d["query"]["search"]:
        print(s["title"])

elif mode == "vids":
    depth = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    cats, seen, out = [arg], set(), []
    for _ in range(depth + 1):
        nxt = []
        for c in cats:
            if c in seen:
                continue
            seen.add(c)
            d = get(action="query", generator="categorymembers", gcmtitle=c,
                    gcmlimit=500, gcmtype="file|subcat", prop="imageinfo",
                    iiprop="url|size|mime|extmetadata", iilimit=1)
            for p in (d.get("query", {}).get("pages") or []):
                if p["title"].startswith("Category:"):
                    nxt.append(p["title"])
                else:
                    out.append(p)
        cats = nxt
    show(out)

elif mode == "search":
    d = get(action="query", generator="search",
            gsrsearch=f"filetype:video {arg}", gsrnamespace=6, gsrlimit=60,
            prop="imageinfo", iiprop="url|size|mime|extmetadata", iilimit=1)
    show(list((d.get("query", {}).get("pages") or [])))
