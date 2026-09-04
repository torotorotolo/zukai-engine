# -*- coding: utf-8 -*-
"""yt_genre_scan.py — 事故解説chの投稿を丸ごと読み、題材ごとの「母数と当たり」を数える（2026-09-04）。

■ なぜ別の道具が要るか
    `yt_theme_probe.py` は `search.list` を使う。あれは **1回100単位**で、
    1日100回で枯れる（2026-09-04 に実際に枯らした）。
    こちらは **playlistItems.list（1単位）と videos.list（1単位）だけ**で回るので、
    同じ日に何度でも測れる。

■ 何を測るか（theme_probe とは母集団が違う。混ぜて比べないこと）
    - theme_probe … 「日本語で検索して出てくる解説動画」全体の当たり率
    - **この道具** … 「**事故解説chとして名の通った N 局が、その題材を何本出し、何回再生されたか**」
      🔴 この ch の流入は **74.4%が関連動画**。関連欄に載る先＝**同じジャンルのchの動画**なので、
      　 実はこちらのほうが効く数字。「母数が0の題材は、載る先が無い」

■ 使い方
    python tools/yt_genre_scan.py channels          # 手元の測定結果から ch を集めてIDを出す
    python tools/yt_genre_scan.py scan              # 集めた ch の全投稿を読み、題材ごとに数える
    共通: --min-subs 3000  --max-channels 14

■ 🔴 割り当て
    playlistItems.list = 1単位/50件、videos.list = 1単位/50件、channels.list = 1単位。
    14局×各300本でも **約200単位**。1日10,000単位のうち2%で済む。
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
import yt_report_jiko as R  # noqa: E402

THEME_DIR = HERE / "analytics" / "themes"
CH_FILE = THEME_DIR / "genre_channels.json"
MIN_SEC = 240
MAX_SEC = 3 * 3600

HIT1 = 10_000
HIT10 = 100_000

# 除外：ニュース・報道（theme_probe と同じ網）
import re  # noqa: E402
NEWS_RE = re.compile(
    r"(ANN|TBS|日テレ|NNN|FNN|フジテレビ|テレ朝|テレビ朝日|テレビ東京|テレ東|NHK|"
    r"KYODO|共同通信|時事通信|朝日新聞|毎日新聞|読売|産経|日経|"
    r"ニュース|NEWS|News|報道|新聞社|通信社|ABEMA|ウェザーニュース|CNN|BBC)", re.I)
NOTDOC_RE = re.compile(r"(総集編|まとめ\d|\d+選|作業用|睡眠用|BGM|ミーム|猫マニ|shorts)", re.I)


def _chunk(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


# 🔴 日本語のチャンネルだけに絞る網。
#    2026-09-04：SL-1 の測定で英語動画を拾ったため、出現数の上位を
#    History Gone Mad / Discovery UK / The Lore Lodge が占めた。
#    このchの関連欄に載るのは**日本語の事故解説ch**なので、英語圏は母集団に入れない。
JA_RE = re.compile(r"[ぁ-んァ-ヴ一-龥]")

# 🔴 さらに「事故解説ジャンルか」をチャンネル名で絞る。
#    2026-09-04：出現数で並べたら オカルト／都市伝説／ホラー／猫ミーム／まとめ系が上位に来た。
#    出現数は「私の検索語に引っかかった回数」であってジャンルではない。
#    ⚠️ この網は**取りこぼす**（ジャンルchでも名前に語が無いものは落ちる）。
#    　 落としたぶんは --show-dropped で目で見て、必要なら --extra-id で足すこと。
GENRE_RE = re.compile(
    r"(事故|災害|遭難|海難|墜落|沈没|崩落|検証|事件と事故|軌跡|資料館|ジコ|"
    r"ヒコーキ|フライト|ブラックボックス|航空|鉄道|事故解説|災難)")


def collect_channels(yt, min_subs, max_channels, ja_only=True):
    """これまでの測定結果に出てきた動画から、チャンネルを集める。

    🔴 `search.list` を使わずに ch を見つけるための回り道。
    手元の JSON にある videoId を videos.list に投げれば channelId が取れる（1単位/50件）。
    """
    vids = set()
    for p in THEME_DIR.glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        stack = [data]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                if isinstance(o.get("id"), str) and re.fullmatch(r"[A-Za-z0-9_-]{11}", o["id"]):
                    vids.add(o["id"])
                stack += list(o.values())
            elif isinstance(o, list):
                stack += o
    print(f"[集めた] 手元の測定結果から動画 {len(vids)} 件")
    if not vids:
        raise SystemExit("[中止] 動画が1件も無い。先に yt_theme_probe.py を回すこと")

    ch_count = Counter()
    ch_title = {}
    for part in _chunk(sorted(vids), 50):
        d = yt.videos().list(part="snippet", id=",".join(part)).execute()
        for v in d.get("items", []):
            s = v["snippet"]
            ch_count[s["channelId"]] += 1
            ch_title[s["channelId"]] = s["channelTitle"]
    print(f"[集めた] チャンネル {len(ch_count)} 局")

    # 登録者数とアップロード用プレイリストを引く
    out, dropped_names = [], []
    for part in _chunk([c for c, _ in ch_count.most_common()], 50):
        d = yt.channels().list(part="snippet,statistics,contentDetails",
                               id=",".join(part)).execute()
        for c in d.get("items", []):
            st, sn = c["statistics"], c["snippet"]
            if NEWS_RE.search(sn["title"]):
                continue
            if ja_only and not JA_RE.search(sn["title"]):
                continue
            if ja_only and not GENRE_RE.search(sn["title"]):
                dropped_names.append(f"{sn['title']}({st.get('subscriberCount')})")
                continue
            subs = int(st.get("subscriberCount", 0) or 0)
            if subs < min_subs:
                continue
            out.append({
                "id": c["id"], "title": sn["title"], "subs": subs,
                "videos": int(st.get("videoCount", 0) or 0),
                "views": int(st.get("viewCount", 0) or 0),
                "uploads": c["contentDetails"]["relatedPlaylists"]["uploads"],
                "seen": ch_count[c["id"]],
            })
    # 🔴 並べ替えは「出現数」でなく**登録者数**。出現数は私の検索語のクセを写すだけ
    out.sort(key=lambda c: -c["subs"])
    print(f"[絞った] ジャンル名の網で {len(dropped_names)} 局を外した"
          f"（例: {', '.join(dropped_names[:6])}）")
    out = out[:max_channels]
    CH_FILE.parent.mkdir(parents=True, exist_ok=True)
    CH_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{'登録':>8} {'本数':>5} {'出現':>4}  チャンネル")
    for c in out:
        print(f"{c['subs']:>8} {c['videos']:>5} {c['seen']:>4}  {c['title']}")
    print(f"\n保存: {CH_FILE.relative_to(HERE)}")
    return out


def channel_videos(yt, uploads, cap=600):
    ids, tok = [], None
    while len(ids) < cap:
        kw = dict(part="contentDetails", playlistId=uploads, maxResults=50)
        if tok:
            kw["pageToken"] = tok
        d = yt.playlistItems().list(**kw).execute()
        ids += [it["contentDetails"]["videoId"] for it in d.get("items", [])]
        tok = d.get("nextPageToken")
        if not tok:
            break
    rows = []
    for part in _chunk(ids[:cap], 50):
        d = yt.videos().list(part="snippet,contentDetails,statistics",
                             id=",".join(part)).execute()
        for v in d.get("items", []):
            s, c, st = v["snippet"], v["contentDetails"], v.get("statistics", {})
            if not c.get("duration"):
                continue
            sec = R.iso_seconds(c["duration"])
            if sec < MIN_SEC or sec > MAX_SEC:
                continue
            if NOTDOC_RE.search(s["title"]):
                continue
            rows.append({"id": v["id"], "title": s["title"], "channel": s["channelTitle"],
                         "sec": sec, "views": int(st.get("viewCount", 0) or 0),
                         "published": s["publishedAt"][:10]})
    return rows


def cmd_channels(a) -> int:
    _, yt = R.apis()
    collect_channels(yt, a.min_subs, a.max_channels)
    return 0


def cmd_scan(a) -> int:
    if not CH_FILE.exists():
        raise SystemExit(f"[中止] {CH_FILE} が無い。先に `channels` を回すこと")
    chans = json.loads(CH_FILE.read_text(encoding="utf-8"))
    themes = json.loads(Path(a.themes).read_text(encoding="utf-8"))
    _, yt = R.apis()

    allrows = []
    for c in chans:
        rows = channel_videos(yt, c["uploads"], cap=a.cap)
        print(f"  {c['title'][:22]:<24} 登録{c['subs']:>7} … 解説動画 {len(rows):>4} 本")
        allrows += rows
    print(f"\n[母集団] {len(chans)} 局 ／ 解説動画 **{len(allrows)} 本**")

    out = []
    for t in themes:
        words = t["words"]
        hit = [r for r in allrows if any(w in r["title"] for w in words)]
        if t.get("nots"):
            hit = [r for r in hit if not any(x in r["title"] for x in t["nots"])]
        hit.sort(key=lambda r: -r["views"])
        n = len(hit)
        h1 = sum(1 for r in hit if r["views"] >= HIT1)
        h10 = sum(1 for r in hit if r["views"] >= HIT10)
        out.append({"name": t["name"], "n": n, "hit1": h1, "hit10": h10,
                    "median": int(statistics.median([r["views"] for r in hit])) if hit else None,
                    "max": hit[0]["views"] if hit else 0,
                    "channels": sorted({r["channel"] for r in hit}),
                    "top": hit[:8]})

    print(f"\n{'題材':<18} {'本数':>4} {'1万超':>5} {'10万超':>6} {'中央値':>8} {'最高':>9}  出している局")
    for s in sorted(out, key=lambda x: -x["n"]):
        med = s["median"] if s["median"] is not None else "-"
        print(f"{s['name'][:17]:<18} {s['n']:>4} {s['hit1']:>5} {s['hit10']:>6} "
              f"{str(med):>8} {s['max']:>9}  {len(s['channels'])}局")
    print("🔴 **本数0＝関連欄に載る先が無い**。率より先に本数を見る")

    for s in out:
        if not s["top"]:
            print(f"\n■ {s['name']}: 🔴 このジャンルの主要局が**1本も出していない**")
            continue
        print(f"\n■ {s['name']}（{s['n']}本・{len(s['channels'])}局）")
        for r in s["top"][:5]:
            print(f"   {r['views']:>8}  {r['published']}  {r['channel'][:14]:<15} {r['title'][:44]}")

    p = THEME_DIR / f"{a.out or 'genre_scan'}.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n保存: {p.relative_to(HERE)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="事故解説chの投稿を丸ごと読んで題材を数える")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("channels", help="手元の測定結果から ch を集める")
    p.add_argument("--min-subs", type=int, default=3000)
    p.add_argument("--max-channels", type=int, default=14)
    p.set_defaults(fn=cmd_channels)
    p = sub.add_parser("scan", help="集めた ch の全投稿を題材で数える")
    p.add_argument("--themes", default=str(THEME_DIR / "ep4_keywords.json"))
    p.add_argument("--cap", type=int, default=600, help="1局あたりの上限本数")
    p.add_argument("--out")
    p.set_defaults(fn=cmd_scan)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
