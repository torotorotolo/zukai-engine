# -*- coding: utf-8 -*-
"""12本目②：4段の網（権利 → 大きさ → 撮影年 → 場面）を Commons の629点に当てる。

→ [[feedback-inventory-is-not-usable-material]]
   ⚠️ 4段目（場面）は機械では割れない。ここが出すのは**読むべき一覧**であって在庫ではない。

⚠️ ライセンスの**根拠**（米連邦§105 か／日本の旧法 PD か／更新されなかった US 著作物か）は
   Commons の**隠しカテゴリ**にある。`clshow=!hidden` で取ると入らないので、
   絞った点だけ取り直す（`--fetch-hidden`）。
   → [[feedback-pd-label-hides-two-different-grounds]]
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

API = "https://commons.wikimedia.org/w/api.php"
UA = "zukai-engine-ep12-probe/1.0 (research; contact via github torotorotolo)"
ROWS = Path("ref/ep12/commons_ep12.json")
HID = Path("ref/ep12/commons_hidden.json")

SA = ("SA",)  # 継承つき＝動画全体に伝染するので使えない


def is_sa(lic):
    u = (lic or "").upper().replace("-", "").replace(" ", "")
    return "BY" in u and "SA" in u


def year_of(r):
    """撮影年。⚠️ 取り込みの年が混じるので、題と説明の 1954 も見る。"""
    d = (r.get("date_original") or "")[:64]
    for y in range(1946, 2027):
        if str(y) in d:
            return y
    return None


def main():
    rows = json.loads(ROWS.read_text(encoding="utf-8"))
    print("集めた点数 %d（pageid で重複を除いたあとの実数）\n" % len(rows))

    # 段1 権利
    a1 = [r for r in rows if not is_sa(r["license_short"])]
    print("段1 権利（継承 CC BY-SA を外す）     %4d → %4d" % (len(rows), len(a1)))
    print("     ライセンスの生の値: %s"
          % dict(Counter(r["license_short"] for r in rows).most_common(8)))

    # 段2 大きさ（幅1280以上・連続階調）
    a2 = [r for r in a1 if r["width"] >= 1280 and (r["bitdepth"] or 8) >= 8
          and r["mime"].startswith("image")]
    vids = [r for r in a1 if r["mime"].startswith(("video", "application/ogg"))]
    print("段2 大きさ（幅1280以上・連続階調）   %4d → %4d   ［動く映像は別枠 %d］"
          % (len(a1), len(a2), len(vids)))

    # 段3 撮影年
    a3 = [r for r in a2 if year_of(r) == 1954]
    print("段3 撮影年（1954年）                %4d → %4d" % (len(a2), len(a3)))

    if "--fetch-hidden" in sys.argv:
        fetch_hidden([r["title"] for r in a3] + [r["title"] for r in vids])

    hidden = json.loads(HID.read_text(encoding="utf-8")) if HID.exists() else {}
    print("\n段4 場面＝ここから先は題を1行ずつ読む（機械では割れない）")
    print("-" * 108)
    for r in sorted(a3, key=lambda r: -r["width"]):
        g = ground(hidden.get(r["title"], []))
        print("%5dx%-5d %-11s %-14s %s"
              % (r["width"], r["height"], r["license_short"][:11], g,
                 (r["title"][5:] + " | " + strip(r["desc"]))[:70]))
    print("-" * 108)
    print("1954年・幅1280以上・継承なし＝ **%d点**" % len(a3))
    print("  権利の根拠の内訳: %s"
          % dict(Counter(ground(hidden.get(r["title"], [])) for r in a3)))

    print("\n== 動く映像（幅は別の物差し）==")
    for r in sorted(vids, key=lambda r: -(r["width"] or 0)):
        g = ground(hidden.get(r["title"], []))
        print("%5dx%-5d %7.1fs %-11s %-14s %s"
              % (r["width"], r["height"], r["duration"] or 0,
                 r["license_short"][:11], g, r["title"][5:][:60]))


def strip(s):
    import re
    return re.sub(r"<[^>]+>", "", s or "").replace("\n", " ").strip()


def ground(cats):
    """隠しカテゴリから権利の根拠を決める。分からなければ「?」（0で埋めない）。"""
    c = " | ".join(cats)
    if "PD US Government" in c or "PD USGov" in c:
        return "米連邦§105"
    if "PD US DOE" in c or "PD US DOD" in c or "PD US Navy" in c or "PD US Air Force" in c:
        return "米連邦§105"
    if "PD US not renewed" in c or "not renewed" in c:
        return "US更新なし"
    if "PD Japan" in c or "PD-Japan" in c:
        return "日本旧法PD"
    if "CC0" in c:
        return "CC0自主放棄"
    if "PD-old" in c or "PD old" in c:
        return "保護期間満了"
    if "PD US" in c:
        return "US（他）"
    return "?" if cats else "(未取得)"


def fetch_hidden(titles):
    out = {}
    for i in range(0, len(titles), 50):
        url = API + "?" + urllib.parse.urlencode({
            "action": "query", "format": "json", "formatversion": "2",
            "titles": "|".join(titles[i:i + 50]),
            "prop": "categories", "cllimit": 500, "clshow": "hidden"})
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        for p in d.get("query", {}).get("pages", []):
            out[p["title"]] = [c["title"][9:] for c in (p.get("categories") or [])]
        sys.stderr.write("hidden %d/%d\n" % (min(i + 50, len(titles)), len(titles)))
        time.sleep(2.5)
    HID.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
