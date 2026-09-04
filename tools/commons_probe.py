# -*- coding: utf-8 -*-
"""commons_probe.py — 題材の素材を「実際に数える」（2026-09-04）。

■ なぜ要るか
    ②素材で**いちばん多く候補が落ちる**。「報告書があるはず」「写真は多いはず」で
    企画を通すと、台本まで進んでから物理的に埋まらないことが分かる。
    → **枚数・解像度・ライセンスを機械で数えてから判断する。**

■ 何を数えるか（1点ずつ実測。推定しない）
    - 総点数
    - 🔴 **全画面に耐える点数** ＝ 幅 >= 1280px かつ **bitdepth >= 8**（連続階調）。
      1ビット(2値)スキャンは全画面に使えない（額装パネルか暗幕をかけた地に回す）
    - ライセンスの内訳。**PD / CC BY-SA(継承) / CC BY / その他** に分ける
      🔴 PD が最も安全。CC BY-SA は「継承」が動画全体に波及する論点になる

■ 使い方
    python tools/commons_probe.py cat "Category:USS Thresher (SSN-593)"
    python tools/commons_probe.py cat "Category:Sampoong Department Store collapse" --depth 2
    python tools/commons_probe.py search "雫石 全日空"        # 題名で探す
    共通: --out analytics/materials/<name>.json

■ ⚠️ 注意
    - Commons の外（NARA・NTSB・CSB・国立公文書館など）はここでは数えられない。
      **PDの本体は Commons の外にあることが多い**（3本目の記録映画 thr_85185 は NARA）
    - ここで出る数字は「Commons にある分」の下限。**無いことの証明にはならない**
      （[[feedback-absence-of-a-word-is-not-absence]]）

■ 🔴 2026-09-04 の検算（この道具を信じてよい根拠と、信じてはいけない範囲）
    ✅ 三豊百貨店 `Category:Sampoong Department Store collapse` --depth 2
       → 267点・**全部 CC BY-SA（継承あり）・PD 0点**。
         記録「254点中250点がCC BY-SA」を再現。**落とした判断は正しかった**
    ⚠️ ただし --depth 2 は**事故と無関係な写真を引き込む**。上位10点のうち6点が
       2012〜2013年のソウル消防の行事写真だった。**「全画面72点」はその混入込みの数**
    ⚠️ ディアトロフ峠 `Category:Dyatlov Pass incident` → Commons には **44点しかない**。
       記録の「837点・幅1200px固定」は **Commons ではなく dyatlovpass.com の数**だった。
       → **矛盾ではなく別の出どころ。Commons の数だけで「素材が無い」と言わないこと**
    ✅ bitdepth の網は効いている（ディアトロフ44点中18点が2値スキャン＝事件記録の文書）
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
# ⚠️ stderr も直す。ここを忘れると **例外の日本語が cp932 で化けて読めない**
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
OUT_DIR = HERE / "analytics" / "materials"
API = "https://commons.wikimedia.org/w/api.php"
UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com) python-requests")

FULLSCREEN_MIN_W = 1280   # 全画面に耐える幅（1本目〜3本目で使ってきた基準）
MIN_BITDEPTH = 8          # 1ビット(2値)スキャンを外す

# 🔴 429 対策（2026-09-04 に実測で踏んだ）
#    ・2本を**同時に**走らせたら即 429。この道具は**直列でしか回さない**
#    ・extmetadata は重い。1回のタイトル数を 50 → 20 に落とす
#    ・毎回わずかに待つ。429 が返ったら Retry-After に従って長く待つ
BATCH = 20
SLEEP = 0.35
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip"})


def _get(params, tries=5):
    """🔴 読めなければ0で埋めずに止める（[[feedback-parsers-fail-closed]]）。"""
    p = dict(params); p["format"] = "json"; p["formatversion"] = "2"
    last = None
    for i in range(tries):
        try:
            time.sleep(SLEEP)
            r = SESSION.get(API, params=p, timeout=45)
            if r.status_code == 429:
                wait = float(r.headers.get("Retry-After", 0) or 0) or (5 * (i + 1))
                print(f"  ⏳ 429（混んでいる）。{wait:.0f}秒待って再試行 {i + 1}/{tries}")
                time.sleep(wait)
                last = f"429 (retry {i + 1})"
                continue
            r.raise_for_status()
            d = r.json()
            if "error" in d:
                raise SystemExit(f"[中止] Commons API エラー: {d['error']}")
            return d
        except SystemExit:
            raise
        except Exception as e:      # noqa: BLE001
            last = e
            time.sleep(2.0 * (i + 1))
    raise SystemExit(f"[中止] Commons API が読めない（{tries}回）: {last}")


def cat_files(cat, depth=1, limit=2000):
    """カテゴリ（必要なら子カテゴリも）に入っているファイル名を集める。"""
    if not cat.lower().startswith("category:"):
        cat = "Category:" + cat
    files, seen_cat, queue = [], set(), [(cat, 0)]
    while queue and len(files) < limit:
        c, d = queue.pop(0)
        if c in seen_cat:
            continue
        seen_cat.add(c)
        cont = {}
        while True:
            q = {"action": "query", "list": "categorymembers", "cmtitle": c,
                 "cmlimit": "500", "cmtype": "file|subcat", **cont}
            data = _get(q)
            for m in data.get("query", {}).get("categorymembers", []):
                t = m["title"]
                if t.startswith("Category:"):
                    if d + 1 < depth:
                        queue.append((t, d + 1))
                else:
                    files.append(t)
            if "continue" in data:
                cont = data["continue"]
            else:
                break
    return sorted(set(files))[:limit], sorted(seen_cat)


def search_files(term, limit=500):
    files, offset = [], 0
    while len(files) < limit:
        d = _get({"action": "query", "list": "search", "srsearch": term,
                  "srnamespace": "6", "srlimit": "500", "sroffset": offset})
        hits = d.get("query", {}).get("search", [])
        files += [h["title"] for h in hits]
        if not d.get("continue"):
            break
        offset = d["continue"]["sroffset"]
    return sorted(set(files))[:limit]


def imageinfo(titles):
    """1点ずつ 幅・高さ・bitdepth・ライセンス・出所 を取る（50件ずつ）。"""
    out = []
    for i in range(0, len(titles), BATCH):
        part = titles[i:i + BATCH]
        if i and i % (BATCH * 10) == 0:
            print(f"  …{i}/{len(titles)} 点を実測")
        d = _get({"action": "query", "prop": "imageinfo", "titles": "|".join(part),
                  "iiprop": "url|size|bitdepth|mime|extmetadata"})
        for pg in d.get("query", {}).get("pages", []):
            ii = (pg.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata") or {}
            g = lambda k: (em.get(k) or {}).get("value")     # noqa: E731
            out.append({
                "title": pg.get("title"),
                "w": ii.get("width"), "h": ii.get("height"),
                "bitdepth": ii.get("bitdepth"), "mime": ii.get("mime"),
                "license": g("LicenseShortName"),
                "usageterms": g("UsageTerms"),
                "author": g("Artist"),
                "credit": g("Credit"),
                "url": ii.get("url"),
            })
    return out


def classify_license(lic, terms):
    s = f"{lic or ''} {terms or ''}".lower()
    if "public domain" in s or s.strip().startswith("pd") or "pd-" in s or "cc0" in s:
        return "PD"
    if "sa" in s and "cc" in s:
        return "CC BY-SA（継承あり）"
    if "cc by" in s or "cc-by" in s:
        return "CC BY"
    if "fair" in s or "non-free" in s or "nc" in s:
        return "使えない可能性"
    return f"その他: {lic or '不明'}"


def summarize(name, rows, extra=None):
    lic = {}
    full, bw1, small, unknown = [], [], [], []
    for r in rows:
        k = classify_license(r["license"], r["usageterms"])
        lic[k] = lic.get(k, 0) + 1
        w, bd = r.get("w"), r.get("bitdepth")
        if not w:
            unknown.append(r); continue
        if bd is not None and bd < MIN_BITDEPTH:
            bw1.append(r); continue
        if w >= FULLSCREEN_MIN_W:
            full.append(r)
        else:
            small.append(r)
    full.sort(key=lambda r: -(r["w"] or 0))
    # 全画面に耐えるもののうち PD だけ
    full_pd = [r for r in full
               if classify_license(r["license"], r["usageterms"]) == "PD"]
    return {
        "name": name, "total": len(rows),
        "fullscreen": len(full), "fullscreen_pd": len(full_pd),
        "bitdepth1": len(bw1), "under_1280": len(small), "size_unknown": len(unknown),
        "licenses": dict(sorted(lic.items(), key=lambda kv: -kv[1])),
        "top": [{"title": r["title"], "w": r["w"], "h": r["h"],
                 "bitdepth": r["bitdepth"],
                 "license": classify_license(r["license"], r["usageterms"]),
                 "credit": (r.get("credit") or "")[:80]}
                for r in full[:20]],
        "extra": extra or {},
    }


def _print(s):
    print(f"\n===== {s['name']} =====")
    print(f"  総点数 {s['total']}")
    print(f"  🔴 全画面に耐える（幅>={FULLSCREEN_MIN_W} かつ 連続階調）: "
          f"**{s['fullscreen']}点**  うち **PD {s['fullscreen_pd']}点**")
    print(f"     1ビット(2値)スキャン {s['bitdepth1']} ／ 幅不足 {s['under_1280']} "
          f"／ 大きさ不明 {s['size_unknown']}")
    print(f"  ライセンス内訳: {s['licenses']}")
    if s["top"]:
        print(f"  {'幅x高':>12}  {'bd':>2}  ライセンス / 題")
        for r in s["top"][:10]:
            print(f"  {str(r['w']) + 'x' + str(r['h']):>12}  {str(r['bitdepth']):>2}  "
                  f"{r['license'][:18]:<18} {r['title'][5:60]}")
    if s["total"] == 0:
        print("  🔴 0点。**「無い」ではなく「このカテゴリ名では出ない」**。"
              "別名・別カテゴリ・Commons外を当たること")


def _save(name, s, rows):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)[:60]
    p = OUT_DIR / f"{safe}.json"
    p.write_text(json.dumps({"summary": s, "rows": rows}, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print(f"\n保存: {p.relative_to(HERE)}")


def cmd_cat(a) -> int:
    files, cats = cat_files(a.target, depth=a.depth, limit=a.limit)
    print(f"[{a.target}] 見たカテゴリ {len(cats)} 個／ファイル {len(files)} 点")
    rows = imageinfo(files)
    s = summarize(a.name or a.target, rows, {"categories": cats})
    _print(s); _save(a.name or a.target, s, rows)
    return 0


def cmd_search(a) -> int:
    files = search_files(a.target, limit=a.limit)
    print(f"[検索 {a.target!r}] ファイル {len(files)} 点")
    rows = imageinfo(files)
    s = summarize(a.name or a.target, rows, {"query": a.target})
    _print(s); _save(a.name or a.target, s, rows)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Commons の素材を実際に数える")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for cmd, fn, h in (("cat", cmd_cat, "カテゴリを数える"),
                       ("search", cmd_search, "題名で探して数える")):
        p = sub.add_parser(cmd, help=h)
        p.add_argument("target")
        p.add_argument("--name")
        p.add_argument("--depth", type=int, default=1, help="子カテゴリを何段まで")
        p.add_argument("--limit", type=int, default=2000)
        p.set_defaults(fn=fn)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
