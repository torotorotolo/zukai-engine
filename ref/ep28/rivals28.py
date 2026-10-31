# 28本目 ① 競合の数え（YouTube の検索結果だけを読む・動画は落とさない・API 0単位）
# 使い方: python ep28_rivals.py <出力フォルダ>
import json, os, shutil, statistics, subprocess, sys, unicodedata
from collections import Counter, defaultdict

OUT = sys.argv[1]
WORDS = [
    "タイムズカー 情報漏洩", "タイムズカー 不正アクセス", "タイムズカー 個人情報",
    "タイムズカー 免許証", "タイムズカー 流出", "パーク24 不正アクセス",
    "パーク24 情報漏洩", "タイムズカー 見舞金", "タイムズカー 集団訴訟",
    "カーシェア 情報漏洩 免許証",
]
HIT = ["タイムズ", "パーク24", "TIMESCAR", "TIMES CAR", "PARK24", "カーシェア"]
# yt-dlp は Windows の端末の文字コード（cp932）で書き出す＝UTF-8 で書かせる（1回目はここで落ちた）
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

def nf(s):
    return unicodedata.normalize("NFKC", s or "").upper()

def ytdlp():
    exe = shutil.which("yt-dlp")
    return [exe] if exe else [sys.executable, "-m", "yt_dlp"]

def search(word):
    cmd = ytdlp() + ["--flat-playlist", "-J", f"ytsearch40:{word}"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180, env=ENV)
    if r.returncode != 0 or not r.stdout:
        print(f"!! 検索失敗 {word}: {r.stderr[-300:]}", file=sys.stderr)
        return []
    return json.loads(r.stdout).get("entries") or []

seen, rows = set(), []
for w in WORDS:
    ents = search(w)
    print(f"{w}: {len(ents)}件", file=sys.stderr)
    for e in ents:
        vid = e.get("id")
        if not vid or vid in seen:
            continue
        seen.add(vid)
        rows.append({"id": vid, "word": w, "title": e.get("title"), "channel": e.get("channel"),
                     "duration": e.get("duration"), "view_count": e.get("view_count")})

hits = [r for r in rows if any(k in nf(r["title"]) for k in HIT)]
print(f"検索の和={len(rows)}本・題に語がある={len(hits)}本", file=sys.stderr)

# 公開日と登録者数は1本ずつ（まとめて1回の呼び出し・動画は落とさない）
fmt = "%(id)s\t%(upload_date)s\t%(duration)s\t%(view_count)s\t%(channel_follower_count)s\t%(channel)s"
detail = {}
ids = [r["id"] for r in hits]
for i in range(0, len(ids), 25):
    chunk = ids[i:i + 25]
    cmd = ytdlp() + ["--skip-download", "--ignore-errors", "--no-warnings", "--print", fmt] + \
        [f"https://www.youtube.com/watch?v={v}" for v in chunk]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900, env=ENV)
    for line in (r.stdout or "").splitlines():
        p = line.split("\t")
        if len(p) >= 6:
            detail[p[0]] = p
    if r.returncode != 0:
        print(f"!! 詳細の一部が取れない（exit {r.returncode}）: {r.stderr[-300:]}", file=sys.stderr)

for h in hits:
    d = detail.get(h["id"])
    if d:
        h["upload_date"] = d[1]
        h["duration"] = int(d[2]) if d[2].isdigit() else h["duration"]
        h["view_count"] = int(d[3]) if d[3].isdigit() else h["view_count"]
        h["followers"] = int(d[4]) if d[4].isdigit() else None
    else:
        h["upload_date"] = None
        h["followers"] = None

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "ep28_rivals.json"), "w", encoding="utf-8") as f:
    json.dump({"words": WORDS, "all": len(rows), "hits": hits}, f, ensure_ascii=False, indent=1)

def band(sec):
    if sec is None:
        return "不明"
    m = sec / 60
    for lim, name in [(1, "〜1分"), (8, "1〜8分"), (20, "8〜20分（B）"), (27, "20〜27分"), (40, "27〜40分（A）")]:
        if m < lim:
            return name
    return "40分超"

by = defaultdict(list)
for h in hits:
    by[band(h["duration"])].append(h["view_count"] or 0)
print("\n尺の帯\t本数\t再生の中央")
for k in ["〜1分", "1〜8分", "8〜20分（B）", "20〜27分", "27〜40分（A）", "40分超", "不明"]:
    if by[k]:
        print(f"{k}\t{len(by[k])}\t{int(statistics.median(by[k]))}")
months = Counter((h.get("upload_date") or "????????")[:6] for h in hits)
print("\n公開の月\t本数")
for k in sorted(months):
    print(f"{k}\t{months[k]}")
print("\n再生の多い順（全部）")
for h in sorted(hits, key=lambda x: -(x["view_count"] or 0)):
    dur = h["duration"]
    mmss = f"{dur // 60}:{dur % 60:02d}" if isinstance(dur, int) else "?"
    print(f"{h['view_count']}\t{mmss}\t{h.get('upload_date')}\t{h.get('followers')}\t{h['channel']}\t{h['title']}\t{h['id']}")
