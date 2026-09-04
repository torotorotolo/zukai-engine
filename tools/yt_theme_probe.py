# -*- coding: utf-8 -*-
"""yt_theme_probe.py — 題材の「配信の当たり率」を実測する（2026-09-04）。

■ 何を測るか
    **解説系の新作（ニュースchを除く）が 1万回を超えた率／10万回を超えた率。**
    在庫（過去のヒット）ではなく「新しく出した動画がどれくらい当たるか」を測る。

■ 🔴 なぜこの測り方か（過去に6回、測り方のせいで結論を撤回している）
    1. `order=relevance` の上位50本は **在庫** を測ってしまう
    2. `order=date` は **最新50本** しか返さないので、投稿の多い題材ほど
       「積み上がる前の若い動画」ばかり見る（ja123は1か月ぶんしか見えなかった）
    3. **小標本の中央値は使えない**（分布の裾が長く、窓を変えると 425,504 → 409 と暴れた）
    4. 窓を1つしか見ないと順位が入れ替わる（東海村JCOは n=4 で「突出」→ n=27 で「最下位」）
    → **公開時期の窓を固定し、複数窓で合算し、ニュースchを除き、重複を除く。**
    → **どの窓も「6か月以上経過」した状態で比べる**（若い動画を混ぜない）

■ 🔴 道具の検算（[[feedback-verify-your-own-instrument]]）
    2026-08-07 に別の手で測った値が記録されている。同じ窓で回して近い値が出るかを見る。
        スレッシャー 1万超45% / 10万超18%（n=11）
        雫石         62% / 31%（n=13）
        ディアトロフ  6% /  0%（n=36）
        東海村JCO    30% / 19%（n=27）
        セウォル      17% /  6%（n=35）
    → `python tools/yt_theme_probe.py selftest`
    ⚠️ 完全一致は期待しない（当時の検索語・除外の仕方が同一とは限らない）。
       **向き（順位）が再現するか**を見る。再現しなければ「道具が違う」と書く。

    ── 🔴 2026-09-04 の検算の結果（**読む前にここを読む**）
      スレッシャー n 11→12・45%→41.7%・18%→16.7%   ✅ 再現
      ディアトロフ n 36→31・ 6%→ 9.7%・ 0%→ 0.0%   ✅ 再現
      雫石         n 13→27・62%→25.9%・31%→14.8%   🔴 **母集団が違う**

      雫石の27本を1本ずつ目で見た。混入は4本だけ（「ANA58便 札幌→羽田」の現在の
      搭乗動画2本／AIRDO 58便の修学旅行／広東語1本）。除いても n=23・30.4% で
      62% には戻らない。**差の実体は再生2,000回未満の小さいchの尾**で、
      2026-08-07 の測定はそこを取りきれていなかった（n=13）。

    🔴 **したがって：この道具の値を、2026-08-07 に記録された値と横並びで比べてはいけない。**
       　 比べてよいのは**同じ実行の中の題材どうし**だけ。雫石・三豊を含め、
       　 候補は全部この道具で測り直すこと。

    ── 🔴 order を viewCount にしてはいけない（2026-09-04 に踏んだ）
      各窓の「再生数上位50本」しか見ないので、**動画数の多い題材ほど当たり率が
      構造的に高く出る**。ディアトロフが 6% → 38.9% と逆転して発覚した。
      order=date なら窓の中の新しい順＝再生数と無関係な抽出になる。

■ 使い方
    python tools/yt_theme_probe.py probe --name 雫石 --q "雫石 全日空" --q "全日空58便"
    python tools/yt_theme_probe.py probe --file config/themes_ep4.json
    python tools/yt_theme_probe.py selftest
    共通: --windows orig|now   --out analytics/themes/<name>.json

■ 割り当て（quota）
    search.list = 100 単位 / 回。videos.list・channels.list = 1 単位 / 回。
    1題材 = 窓3 × 検索語k 回の search.list。**回す前に見積もりを出して確認する。**
    既定の上限は 10,000 単位/日。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
import yt_report_jiko as R  # noqa: E402  （apis / iso_seconds を借りる）

OUT_DIR = HERE / "analytics" / "themes"

# ── 窓（🔴 どれも「6か月以上経過」していること。今日は 2026-09-04）
WINDOWS = {
    # 2026-08-07 の測定と同じ窓。道具の検算に使う
    "orig": [("2023-08-01", "2024-08-01"),
             ("2024-08-01", "2025-08-01"),
             ("2025-08-01", "2026-02-01")],
    # 4本目の判断に使う窓。末尾を 2026-03-04 まで伸ばした（それでも6か月以上経過）
    "now": [("2023-09-01", "2024-09-01"),
            ("2024-09-01", "2025-09-01"),
            ("2025-09-01", "2026-03-04")],
}

# ── 除外：ニュース・報道チャンネル（**除外したものは必ず印字する**。黙って消さない）
NEWS_RE = re.compile(
    r"(ANN|TBS|日テレ|NNN|FNN|フジテレビ|テレ朝|テレビ朝日|テレビ東京|テレ東|NHK|"
    r"KYODO|共同通信|時事通信|朝日新聞|毎日新聞|読売|産経|日経|中日新聞|北海道新聞|"
    r"ニュース|NEWS|News|報道|新聞社|通信社|ABEMA|ウェザーニュース|"
    r"放送局|テレビ局|BIZ|CNN|BBC|Reuters|AFP)", re.I)
# 自分のチャンネル
OWN_HANDLE_RE = re.compile(r"そのとき、何が起きたか")

# ── 除外：解説動画でないもの（総集編・ミーム・作業用）。**題名で見る**
NOTDOC_RE = re.compile(
    r"(総集編|まとめ\d|\d+選|作業用|睡眠用|BGM|ミーム|猫マニ|ラジオ|"
    r"ゲーム実況|MAD|shorts|ショート)", re.I)

MIN_SEC = 240        # 4分未満は解説動画とみなさない（ニュース断片・ショート）
MAX_SEC = 3 * 3600   # 3時間超はまとめ配信・作業用BGM
PER_QUERY = 50       # search.list の1回あたり（＝100単位）

# 🔴 抽出の順序。既定は date。
#    viewCount にすると「その窓の再生数上位50本」しか見ないので、
#    動画数の多い題材ほど**当たり率が構造的に高く出る**（2026-09-04 の検算で
#    ディアトロフが 6% → 38.9% と逆転して発覚）。
#    date なら窓の中の新しい順＝**再生数と無関係な抽出**になる。
#    窓の終わりが6か月以上前なので「積み上がる前の若い動画」も混ざらない。
DEFAULT_ORDER = "date"

HIT1 = 10_000
HIT10 = 100_000


def _chunk(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def search_window(yt, q, after, before, order=DEFAULT_ORDER, region="JP", lang="ja"):
    """1つの検索語 × 1つの窓 で search.list を1回だけ叩く（100単位）。

    🔴 読めなければ黙って0で埋めずに例外を上げる（[[feedback-parsers-fail-closed]]）。
    """
    # 🔴 2026-09-04：429 が返ることがある。
    #    ⚠️ そのときのメッセージは "Quota exceeded ... Search Queries per day" だが、
    #    　 **少し待つと通る**ことを実測した＝日次の枯渇ではなく**短時間に叩きすぎた**制限。
    #    　 「1日の枠が枯れた」と読んで作業を止めたのは誤りだった。**待って再試行する。**
    r, last = None, None
    for i in range(5):
        try:
            r = yt.search().list(
                part="snippet", type="video", q=q, order=order,
                publishedAfter=after + "T00:00:00Z", publishedBefore=before + "T00:00:00Z",
                maxResults=PER_QUERY, regionCode=region, relevanceLanguage=lang,
            ).execute()
            break
        except Exception as e:      # noqa: BLE001
            last = e
            if "429" not in str(e) and "Quota exceeded" not in str(e):
                raise
            wait = 20 * (i + 1)
            print(f"    ⏳ 429。{wait}秒待って再試行 {i + 1}/5  （q={q!r} {after}）")
            time.sleep(wait)
    if r is None:
        raise SystemExit(f"[中止] 429 が続く。時間をおいて回し直すこと: {last}")
    time.sleep(1.2)                 # 次の呼び出しまで少し空ける（叩きすぎ防止）
    items = r.get("items")
    if items is None:
        raise SystemExit(f"[中止] search.list の返りに items が無い: q={q!r} {after}〜{before}")
    total = r.get("pageInfo", {}).get("totalResults")
    got = [it["id"]["videoId"] for it in items if it.get("id", {}).get("videoId")]
    # ⚠️ 50件ちょうど返ったら「窓が溢れている」＝標本が窓の後半に寄る。呼び出し側で警告する
    return got, (total if total is not None else -1), len(got) >= PER_QUERY


def wilson_low(k, n, z=1.96):
    """当たり率の95%下限（Wilson）。🔴 小標本の率をそのまま信じないため。"""
    if not n:
        return None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    hw = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return round(max(0.0, (c - hw) / d) * 100, 1)


def fetch_videos(yt, ids):
    """videos.list で本体を取る（50件ずつ・1単位/回）。"""
    out = {}
    for part in _chunk(sorted(set(ids)), 50):
        d = yt.videos().list(part="snippet,contentDetails,statistics",
                             id=",".join(part)).execute()
        for v in d.get("items", []):
            out[v["id"]] = v
    return out


def probe_theme(yt, name, queries, windows, musts, nots=None, order=DEFAULT_ORDER):
    """1題材を測る。戻り値は集計＋除外の内訳（**除外は必ず残す**）。"""
    raw_ids, per_window, saturated = [], [], []
    for (after, before) in windows:
        wid = []
        for q in queries:
            got, total, full = search_window(yt, q, after, before, order=order)
            wid += got
            if full:
                saturated.append(f"{after}〜{before} q={q!r}（総数{total}）")
        per_window.append({"after": after, "before": before, "found": len(set(wid))})
        raw_ids += wid

    vids = fetch_videos(yt, raw_ids)

    kept = []
    dropped = {"news": [], "short": [], "long": [], "off_topic": [],
               "not_doc": [], "excluded": [], "own": [], "no_duration": []}
    for vid, v in vids.items():
        s = v.get("snippet") or {}
        c = v.get("contentDetails") or {}
        st = v.get("statistics") or {}
        title, ch = s.get("title", ""), s.get("channelTitle", "")
        # ⚠️ 配信予定・配信中の動画には duration が無い（2026-09-04 に KeyError で落ちた）。
        #    0 で埋めると「0秒の動画」として短尺の網にかかり、**数え落としが黙って起きる**ので
        #    専用の欄に分けて残す（[[feedback-parsers-fail-closed]]）。
        if not c.get("duration"):
            dropped["no_duration"].append(
                {"id": vid, "title": title, "channel": ch, "sec": None,
                 "views": int(st.get("viewCount", 0)), "published": s.get("publishedAt", "")[:10]})
            continue
        sec = R.iso_seconds(c["duration"])
        views = int(st.get("viewCount", 0))
        row = {"id": vid, "title": title, "channel": ch, "sec": sec, "views": views,
               "published": s["publishedAt"][:10]}
        if OWN_HANDLE_RE.search(ch):
            dropped["own"].append(row); continue
        if NEWS_RE.search(ch):
            dropped["news"].append(row); continue
        if sec < MIN_SEC:
            dropped["short"].append(row); continue
        if sec > MAX_SEC:
            dropped["long"].append(row); continue
        if NOTDOC_RE.search(title):
            dropped["not_doc"].append(row); continue
        # 🔴 検索語のゆれで無関係な動画が混じる。題名に必須語が1つも無ければ落とす
        if musts and not any(m in title for m in musts):
            dropped["off_topic"].append(row); continue
        # 🔴 「日本版ディアトロフ峠」のような**別の事件**を弾く
        if nots and any(x in title for x in nots):
            dropped["excluded"].append(row); continue
        kept.append(row)

    kept.sort(key=lambda r: -r["views"])
    n = len(kept)
    h1 = sum(1 for r in kept if r["views"] >= HIT1)
    h10 = sum(1 for r in kept if r["views"] >= HIT10)
    return {
        "name": name, "queries": queries, "windows": per_window,
        "musts": musts, "nots": nots or [], "order": order,
        "n": n,
        "hit1_rate": round(h1 / n * 100, 1) if n else None,
        "hit10_rate": round(h10 / n * 100, 1) if n else None,
        "hit1_low": wilson_low(h1, n), "hit10_low": wilson_low(h10, n),
        "hit1": h1, "hit10": h10,
        "saturated": saturated,
        "top": kept[:15], "kept": kept,
        "dropped_counts": {k: len(v) for k, v in dropped.items()},
        "dropped": dropped,
    }


def _print_theme(t):
    n = t["n"]
    if not n:
        print(f"\n🔴 {t['name']}: 該当0件。**測れていない**（検索語を疑う）。"
              f"除外内訳 {t['dropped_counts']}")
        return
    print(f"\n===== {t['name']} =====")
    print(f"  解説系 n={n} ／ 1万超 {t['hit1']}本 = **{t['hit1_rate']}%**"
          f"（下限{t['hit1_low']}%）"
          f" ／ 10万超 {t['hit10']}本 = **{t['hit10_rate']}%**（下限{t['hit10_low']}%）")
    print(f"  除外: {t['dropped_counts']}（🔴 黙って消していないか目で見る）")
    if t.get("saturated"):
        print(f"  ⚠️ 窓が溢れている（50件上限に到達）＝標本が窓の後半に寄る: "
              f"{len(t['saturated'])}件 {t['saturated'][:2]}")
    print(f"  {'再生':>8}  {'尺':>7}  公開        チャンネル / 題")
    for r in t["top"][:8]:
        print(f"  {r['views']:>8}  {R.fmt_ms(r['sec']):>7}  {r['published']}  "
              f"{r['channel'][:16]} / {r['title'][:44]}")


def _yt(quota_project=None):
    """🔴 **割り当て（quota）はプロジェクトごとに1日10,000単位。**

    2026-09-04 実測：既定のプロジェクト **581571570264（フクロウ側）** の検索枠
    （search.list は1回100単位＝1日100回）を使い切った。
    ⚠️ 枯れたあとも**単発の呼び出しが時々通る**（カウンタが厳密でない）。
    　 それを見て「一時的な制限だ」と読むと間違える。**5回リトライしても429なら日次の枯渇**。
    → `--quota drift-diary` のように**別プロジェクトへ課金先を移せば、その枠が使える**。
    　 ただし移す先で **YouTube Data API v3 が有効になっている必要**がある
    　 （Analytics で同じ手を使って成功している）。
    """
    from googleapiclient.discovery import build  # noqa: PLC0415
    creds = R.get_creds()
    if quota_project:
        creds = creds.with_quota_project(quota_project)
    return build("youtube", "v3", credentials=creds)


def _rank_key(t):
    """1万超率の降順。⚠️ `rate or -1` と書くと **0% が -1 になって先頭に来る**。
    測れなかった（None）だけを最下位にする。"""
    r = t["hit1_rate"]
    return -(r if r is not None else -1.0)


def load_themes(a):
    if a.file:
        data = json.loads(Path(a.file).read_text(encoding="utf-8"))
        return [(t["name"], t["queries"], t.get("musts", []), t.get("nots", []))
                for t in data]
    if not a.name or not a.q:
        raise SystemExit("[中止] --name と --q（1つ以上）、または --file が要る")
    return [(a.name, a.q, a.must or [], a.notword or [])]


def cmd_probe(a) -> int:
    wins = WINDOWS[a.windows]
    themes = load_themes(a)
    calls = sum(len(qs) for _, qs, _, _ in themes) * len(wins)
    print(f"[見積もり] search.list {calls} 回 = **{calls * 100} 単位**"
          f"（1日の上限 10,000）／題材 {len(themes)} 件／窓 {a.windows} {wins}"
          f"／order={a.order}／課金先={a.quota or '既定(581571570264)'}")
    if calls * 100 > a.max_units:
        raise SystemExit(f"[中止] 見積もり {calls * 100} 単位が上限 {a.max_units} を超える。"
                         f"--max-units で上げるか題材を減らす")
    yt = _yt(a.quota)
    out = []
    for (name, qs, musts, nots) in themes:
        t = probe_theme(yt, name, qs, wins, musts, nots=nots, order=a.order)
        _print_theme(t)
        out.append(t)

    print("\n===== まとめ（1万超率の高い順）=====")
    print(f"  {'題材':<18} {'n':>4} {'1万超':>7} {'下限':>7} {'10万超':>7} {'下限':>7}")
    for t in sorted(out, key=_rank_key):
        f_ = lambda k: (f"{t[k]}%" if t[k] is not None else "  --")  # noqa: E731
        print(f"  {t['name']:<18} {t['n']:>4} {f_('hit1_rate'):>7} {f_('hit1_low'):>7} "
              f"{f_('hit10_rate'):>7} {f_('hit10_low'):>7}")
    print("⚠️ n が小さい題材（n<8）の率は幅が広い。**下限のほうで順位を見る**")
    thin = [t["name"] for t in out if t["n"] < 8]
    if thin:
        print(f"🔴 n<8 で率が信用できない題材: {thin}（検索語を足して測り直す）")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / f"{a.out or 'probe'}_{a.windows}.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n保存: {p.relative_to(HERE)}")
    return 0


# ── 🔴 道具の検算：2026-08-07 に別の手で出した値を再現できるか
SELFTEST = [
    dict(name="スレッシャー", queries=["スレッシャー 潜水艦", "スレッシャー号"],
         musts=["スレッシャー"], nots=[], e1=45, e10=18, en=11),
    dict(name="雫石", queries=["雫石 全日空", "全日空58便", "雫石事故 航空"],
         musts=["雫石", "58便"], nots=[], e1=62, e10=31, en=13),
    dict(name="ディアトロフ", queries=["ディアトロフ峠", "ディアトロフ 事件"],
         musts=["ディアトロフ"], nots=["日本版", "米国版", "アメリカ版", "日本の"],
         e1=6, e10=0, en=36),
    dict(name="東海村JCO", queries=["東海村 臨界事故", "JCO 臨界"],
         musts=["東海村", "JCO", "臨界"], nots=[], e1=30, e10=19, en=27),
    dict(name="セウォル号", queries=["セウォル号 沈没", "セウォル号 事故"],
         musts=["セウォル"], nots=[], e1=17, e10=6, en=35),
]


def cmd_selftest(a) -> int:
    wins = WINDOWS["orig"]
    cases = [t for t in SELFTEST if not a.only or t["name"] in a.only]
    if not cases:
        raise SystemExit(f"[中止] --only {a.only} に該当なし。"
                         f"選べるのは {[t['name'] for t in SELFTEST]}")
    calls = sum(len(t["queries"]) for t in cases) * len(wins)
    print(f"[検算] 2026-08-07 の記録値を同じ窓で再現できるかを見る（order={a.order}）。"
          f"search.list {calls} 回 = **{calls * 100} 単位**")
    print("⚠️ 完全一致は期待しない。**順位（向き）が再現するか**を見る\n")
    yt = _yt(getattr(a, "quota", None))
    rows = []
    for c in cases:
        t = probe_theme(yt, c["name"], c["queries"], wins, c["musts"],
                        nots=c["nots"], order=a.order)
        _print_theme(t)
        rows.append((c, t))

    print("\n===== 検算のまとめ =====")
    print(f"  {'題材':<14} {'n(記録)':>8} {'n(今回)':>8} "
          f"{'1万超(記録)':>11} {'1万超(今回)':>11} {'10万超(記録)':>12} {'10万超(今回)':>12}")
    for (c, t) in rows:
        g1 = f"{t['hit1_rate']}%" if t["hit1_rate"] is not None else "--"
        g10 = f"{t['hit10_rate']}%" if t["hit10_rate"] is not None else "--"
        print(f"  {c['name']:<14} {c['en']:>8} {t['n']:>8} {str(c['e1']) + '%':>11} "
              f"{g1:>11} {str(c['e10']) + '%':>12} {g10:>12}")

    # 順位が再現したか（記録の1万超率の順位 vs 今回の順位）
    rec = [c["name"] for (c, _) in sorted(rows, key=lambda x: -x[0]["e1"])]
    got = [c["name"] for (c, _) in sorted(rows, key=lambda x: _rank_key(x[1]))]
    print(f"\n  記録の順位: {' > '.join(rec)}")
    print(f"  今回の順位: {' > '.join(got)}")
    print("  ✅ 順位が一致" if rec == got else
          "  🔴 順位が一致しない＝**道具が別のものを測っている**。使う前に原因を書くこと")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / f"selftest_orig_{a.order}.json"
    p.write_text(json.dumps([t for (_, t) in rows], ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print(f"\n保存: {p.relative_to(HERE)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="題材の配信の当たり率を実測する")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("probe", help="題材を測る")
    p.add_argument("--name")
    p.add_argument("--q", action="append", help="検索語（複数可）")
    p.add_argument("--must", action="append", help="題名に含まれるべき語（複数可・OR）")
    p.add_argument("--notword", action="append",
                   help="題名に入っていたら落とす語（別事件よけ・複数可）")
    p.add_argument("--file", help="題材のJSON（name/queries/musts/nots の配列）")
    p.add_argument("--windows", choices=list(WINDOWS), default="now")
    p.add_argument("--order", choices=["date", "viewCount", "relevance"],
                   default=DEFAULT_ORDER)
    p.add_argument("--quota", help="課金先(quota project)。既定の枠が枯れたら "
                                   "--quota drift-diary のように別プロジェクトへ移す")
    p.add_argument("--out")
    p.add_argument("--max-units", type=int, default=6000)
    p.set_defaults(fn=cmd_probe)

    p = sub.add_parser("selftest", help="🔴 記録値を再現できるかを見る")
    p.add_argument("--only", action="append",
                   help="題材を絞る（割り当て節約用。複数可）")
    p.add_argument("--order", choices=["date", "viewCount", "relevance"],
                   default=DEFAULT_ORDER)
    p.add_argument("--quota", help="課金先(quota project)。既定の枠が枯れたら "
                                   "--quota drift-diary のように別プロジェクトへ移す")
    p.set_defaults(fn=cmd_selftest)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
