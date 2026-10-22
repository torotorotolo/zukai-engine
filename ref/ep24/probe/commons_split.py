# -*- coding: utf-8 -*-
"""24本目②：Commons の台帳（cmx.py files の TSV）を 権利 → 大きさ → 撮影年 → 場面（分類）で割る。
網は候補を絞る道具＝最後は一覧を1行ずつ読み、絵は 640px の見本帳で見る（記憶 feedback-inventory-is-not-usable-material）。
使い方: commons_split.py <台帳.tsv> <出力.txt>"""
import csv, re, sys
from collections import Counter, defaultdict

FLICKR_SEEN = {"5394722509", "8389777094", "5395341220", "5395399280", "5613115146", "8388691703",
               "5613126700", "5613114630", "5612542985", "8388691899", "8388691973", "28615021352"}


def lic_class(lic):
    l = (lic or "").lower()
    if not l:
        return "?"
    if "nc" in l.split() or "-nc" in l or "noncommercial" in l:
        return "NC"
    if "sa" in l.split() or "by-sa" in l or "share" in l:
        return "BY-SA"
    if "gfdl" in l:
        return "GFDL"
    if "cc0" in l or "public domain" in l or l.startswith("pd") or "pdm" in l:
        return "PD/CC0"
    if "cc by" in l or "cc-by" in l or "attribution" in l:
        return "CC BY"
    if "licence ouverte" in l or "etalab" in l or "open licence" in l:
        return "LO"
    return "other:" + lic[:20]


def year(r):
    for s in (r.get("dto", ""), r.get("title", ""), r.get("desc", "")):
        m = re.search(r"\b(19[4-9]\d|20[0-2]\d)\b", s or "")
        if m:
            return m.group(1), ("dto" if s == r.get("dto") else "text")
    return "?", ""


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter="\t"))
    out = open(sys.argv[2], "w", encoding="utf-8")
    p = lambda *a: print(*a, file=out)
    p(f"台帳 {len(rows)}点")
    for r in rows:
        r["L"] = lic_class(r.get("lic"))
        r["Y"], r["Ysrc"] = year(r)
        try:
            r["W"] = int(r.get("w") or 0)
        except ValueError:
            r["W"] = 0
        m = re.search(r"\((\d{9,11})\)", r["title"])
        r["FL"] = m.group(1) if m else ""
        r["video"] = r.get("mime", "").startswith("video") or r.get("mime", "").startswith("audio")
    p("権利:", Counter(r["L"] for r in rows).most_common())
    p("動画・音声:", [(r["title"], r["mime"], r["W"]) for r in rows if r["video"]])
    y86 = [r for r in rows if r["Y"] == "1986"]
    p(f"\n## 撮影年 1986（DateTimeOriginal か題・説明の年）＝{len(y86)}点（権利 {Counter(r['L'] for r in y86).most_common()}）")
    for r in sorted(y86, key=lambda r: (r["L"], r["cat"], r["title"])):
        p(f"- {r['L']:6} {r['W']:>5}x{r.get('h','')} [{r['Ysrc']}] {r['title'][5:90]} | {r['artist'][:30]} | {r['cat'][9:50]} | {r['dto'][:16]}{' | FL'+r['FL'] if r['FL'] else ''}{' (Flickr で見た)' if r['FL'] in FLICKR_SEEN else ''}")
    for y in ("1987", "1988", "1989"):
        ys = [r for r in rows if r["Y"] == y]
        p(f"\n## 撮影年 {y}＝{len(ys)}点")
        for r in ys[:40]:
            p(f"- {r['L']:6} {r['W']:>5}x{r.get('h','')} {r['title'][5:90]} | {r['cat'][9:45]}")
    groups = defaultdict(list)
    for r in rows:
        groups[r["cat"]].append(r)
    for key in ("Category:Reactor 4 in Chernobyl Nuclear Power Plant", "Category:Chernobyl Nuclear Power Plant New Safe Confinement",
                "Category:Maps of the Chernobyl disaster", "Category:Radiation maps of the Chernobyl disaster",
                "Category:SVG maps of the Chernobyl disaster", "Category:Chernobyl liquidators",
                "Category:People associated with the Chernobyl disaster", "Category:Chernobyl Forum", "Category:Chernobyl disaster"):
        g = groups.get(key, [])
        p(f"\n## {key}＝{len(g)}点（年 {Counter(r['Y'] for r in g).most_common(12)}／権利 {Counter(r['L'] for r in g).most_common()}）")
        for r in sorted(g, key=lambda r: (r["Y"], r["L"], r["title"]))[:160]:
            p(f"- {r['Y']} {r['L']:6} {r['W']:>5}x{r.get('h','')} {r['title'][5:95]} | {r['artist'][:24]}")
    fl = [r for r in rows if r["FL"] in FLICKR_SEEN]
    p(f"\n## Flickr で見た12点のうち Commons にあるもの＝{len(fl)}点")
    for r in fl:
        p(f"- FL{r['FL']} {r['title'][5:80]} | {r['L']} | {r['cat'][9:50]}")


if __name__ == "__main__":
    main()
