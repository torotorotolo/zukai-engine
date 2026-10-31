# 28本目 ② SNS の声の材料＝Yahoo!リアルタイム検索の頁（サーバーが組んだ __NEXT_DATA__）から投稿の本文・日時・投稿の番号だけを取る
# 使い方: python -X utf8 ref/ep28/probe/yrt28.py <出力tsv> 語1 語2 ...
# 🔴 アカウント名・アイコン・プロフィールは取らない（ルール §B2-9）。本文の @名前 は「@○」に伏せる。投稿の頁は x.com/i/status/<番号> で開ける
# 🔴 出力は git の外（ref/ep28/src/sns/）だけ。リポに入れない
import json, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta
UA = {"User-Agent": "zukai-engine-research/1.0 (GitHub torotorotolo)"}
JST = timezone(timedelta(hours=9))
def fetch(term):
    url = "https://search.yahoo.co.jp/realtime/search?" + urllib.parse.urlencode({"p": term})
    s = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "replace")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S)
    if not m:
        raise SystemExit("__NEXT_DATA__ が無い（頁の作りが変わった）＝止める: " + term)
    tl = json.loads(m.group(1))["props"]["pageProps"]["pageData"].get("timeline", {})
    return tl.get("entry", [])
def when(e):
    for k in ("createdAt", "created_at", "postedAt"):
        v = e.get(k)
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v, JST).strftime("%Y-%m-%d %H:%M")
        if isinstance(v, str) and v:
            return v
    return ""
dst, terms = sys.argv[1], sys.argv[2:]
rows, seen = [], set()
for t in terms:
    es = fetch(t)
    print("term\t%d\t%s" % (len(es), t), file=sys.stderr, flush=True)
    for e in es:
        pid = str(e.get("id", ""))
        if not pid or pid in seen:
            continue
        seen.add(pid)
        text = re.sub(r"@\w+", "@○", e.get("displayText", "") or "").replace("\t", " ").replace("\n", " ")
        links = " / ".join((u.get("title") or "")[:50] for u in e.get("urls", []) if isinstance(u, dict))
        rows.append((t, pid, when(e), text, links.replace("\t", " ")))
    time.sleep(3)
with open(dst, "w", encoding="utf-8") as f:
    f.write("term\tpost_id\twhen\ttext\tlink_titles\n")
    for r in rows:
        f.write("\t".join(r) + "\n")
print("POSTS", len(rows), "keys_of_entry=", sorted(es[0].keys()) if es else [], file=sys.stderr)
