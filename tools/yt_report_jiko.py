# -*- coding: utf-8 -*-
"""yt_report_jiko.py — 事故検証ch「そのとき、何が起きたか」の成績を読む（2026-08-07）。

深読みフクロウの `zankoku-sekkeizu/tools/yt_report.py` を土台に移植した。違いは4つ。

  1. 🔴 **維持率を「秒」で出す。** 尺が違うと % は自動で動くので、%だけで
     本どうしを比べると評価が逆転する（[[feedback-retention-compare-seconds-not-percent]]）。
     `retention` は `elapsedVideoTimeRatio`(0〜1) を**尺に掛けて秒に直してから**並べる。
  2. 🔴 **再生数が少ないうちは「まだ判断しない」と自分から言う。**
     カーブは数十再生では使えない。しきい値は `MIN_VIEWS_CURVE`。
  3. 🔴 **このリポジトリは public** なので、トークンを書く前に `git check-ignore` で
     無視を実測する（`upload_jiko.assert_ignored` をそのまま使う）。
  4. トークンは投稿用 `token_jiko.json` と**分ける**（スコープが違う）。
     投稿用を上書きすると、次の投稿で同意し直しになるため。

■ 使い方
    python tools/yt_report_jiko.py auth              # 初回だけ（ブラウザで同意）
    python tools/yt_report_jiko.py report            # 全期間の総括＋動画別
    python tools/yt_report_jiko.py report --days 28
    python tools/yt_report_jiko.py retention <videoId>   # 維持率カーブ（秒）

■ ⚠️ CTR とインプレッションは **YouTube の公開APIに存在しない**
    （Analytics API は 400 を返し、Reporting API にも該当レポートが無い）。
    唯一の入手経路が Studio のエクスポートなので、ZIP を Downloads に置いたまま
    `report` を回せば自動で取り込む（`analytics/studio_csv/` に展開される）。
      YouTube Studio → アナリティクス → 右上「詳細モード」→ 右上「エクスポート」
      → 「カンマ区切り値(.csv)」
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import zipfile
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
import upload_jiko as U  # noqa: E402  （assert_ignored と CLIENT_SECRET を借りる）

TOKEN = HERE / "config" / "token_jiko_analytics.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/yt-analytics.readonly"]
# 🔴 課金先(quota project)は既定で**触らない**。
#    フクロウの `yt_report.py` は `with_quota_project("zunda-5ch")` を無条件で当てているが、
#    あれは**フクロウのGoogleアカウントが zunda-5ch の持ち主だから**成立している。
#    事故検証chは `torotorotolo@gmail.com` で、このアカウントには zunda-5ch の
#    serviceusage 権限が無い → **403「Caller does not have required permission」**で落ちる
#    （2026-08-07 に実測。引き継ぎの作りをそのまま引き写して踏んだ）。
#    → 既定は None（＝クライアントの所属プロジェクトに課金）。必要なら --quota で渡す。
# 🔴 2026-09-04 に決着。既定を None から "drift-diary" に変えた。
#    ・OAuth クライアントの所属は **project 581571570264（＝zunda-5ch／フクロウ側）**。
#      そこでは YouTube Analytics API が**無効**で、403 accessNotConfigured になる。
#      しかも torotorotolo@gmail.com には zunda-5ch の権限が無いので**有効化できない**
#      （--quota zunda-5ch は "Caller does not have required permission"）。
#    ・カズヤくんの Cloud プロジェクト **drift-diary では Analytics API が有効**で、
#      torotorotolo@gmail.com に serviceusage の権限もある → **ここへ課金先を移すと通る**（実測）。
#    ⚠️ Data API v3（動画別の再生数・チャンネル情報）は既定のままでも通る。
#       効かないのは Analytics（維持率カーブ・流入元・日別）だけ。
QUOTA_PROJECT = "drift-diary"
CSV_DIR = HERE / "analytics" / "studio_csv"
SNAP_DIR = HERE / "analytics" / "snapshots"
CHANNEL = "そのとき、何が起きたか"

# 🔴 これ未満はカーブを読まない（十数〜数十再生ではノイズしか出ない）
MIN_VIEWS_CURVE = 200
# これ未満は平均維持秒すら参考値にとどめる
MIN_VIEWS_AVG = 50


# ─────────────────────────────────────────────── 認証
def get_creds(interactive: bool = False) -> Credentials:
    U.assert_ignored(TOKEN)          # ★読む前に確かめる
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif interactive:
            if not U.CLIENT_SECRET.exists():
                raise SystemExit(f"client_secret.json が無い: {U.CLIENT_SECRET}")
            print("ブラウザで同意画面が開きます。")
            print(f"★必ず『{CHANNEL}』（torotorotolo@gmail.com）を選んでください。")
            flow = InstalledAppFlow.from_client_secrets_file(str(U.CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(
                port=0, prompt="consent",
                authorization_prompt_message=f"ブラウザで『{CHANNEL}』のGoogleアカウントを選んで承認してください…")
        else:
            raise SystemExit(
                "Analytics のトークンが無い（または失効）。\n"
                "  → python tools/yt_report_jiko.py auth")
        TOKEN.parent.mkdir(parents=True, exist_ok=True)
        U.assert_ignored(TOKEN)      # ★書く直前にもう一度
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return creds


def apis(interactive: bool = False):
    """🔴 **API ごとに課金先を分ける。**（2026-09-04 実測で必要になった）

    ・YouTube **Analytics** API … 581571570264(zunda-5ch) では無効・権限も無い。
      　　　　　　　　　　　　　　 → `drift-diary` へ移すと通る
    ・YouTube **Data** API v3 …… 581571570264 では有効。
      　　　　　　　　　　　　　　 → `drift-diary` では**無効**なので**移すと逆に落ちる**
    どちらか一方に揃えようとすると必ず片方が落ちる。**分けるのが正しい。**
    """
    c = get_creds(interactive)
    ca = c.with_quota_project(QUOTA_PROJECT) if QUOTA_PROJECT else c
    return (build("youtubeAnalytics", "v2", credentials=ca),
            build("youtube", "v3", credentials=c))


def guard_channel(yt) -> dict:
    """★どのチャンネルを読んでいるかを、数字を出す前に必ず確かめる。"""
    ch = yt.channels().list(part="snippet,statistics", mine=True).execute()["items"][0]
    if ch["snippet"]["title"] != CHANNEL:
        raise SystemExit(f"[中止] 繋がっているのが『{ch['snippet']['title']}』。"
                         f"狙いは『{CHANNEL}』。→ {TOKEN} を消して auth し直す。")
    return ch


# ─────────────────────────────────────────────── 取得
def q(ya, start, end, metrics, dimensions="", sort="", filters="", maxr=0):
    kw = dict(ids="channel==MINE", startDate=start, endDate=end, metrics=metrics)
    for k, v in (("dimensions", dimensions), ("sort", sort), ("filters", filters)):
        if v:
            kw[k] = v
    if maxr:
        kw["maxResults"] = maxr
    r = ya.reports().query(**kw).execute()
    return [c["name"] for c in r["columnHeaders"]], r.get("rows", [])


def iso_seconds(iso: str) -> int:
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", iso or "")
    if not m:
        return 0
    h, mi, s = (int(g or 0) for g in m.groups())
    return h * 3600 + mi * 60 + s


def fmt_ms(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 60}分{sec % 60:02d}秒"


# ─────────────────────────────────────────────── Studio CSV（CTR）
# 🔴 2026-09-04：**Studio が列名を変えていた。**古い名前で探していたので、
#    新しいエクスポートが**黙って取り込まれずに素通り**していた（エラーも出ない）。
#      旧「インプレッション数」           → 新「サムネイルのインプレッション」（"数"が無い）
#      旧「インプレッションのクリック率」  → 新「サムネイルのクリック率 (%)」（"インプレッション"が付かない）
#      動画IDの列は 旧・新とも「コンテンツ」で、`^動画$` では**一度も当たっていなかった**
#    → 三つとも受ける形にする。⚠️ また変わる。**取り込み0件なら黙らずに言う**
#    （[[feedback-gates-go-stale-when-upstream-changes]]）
_IMP = re.compile(r"(インプレッション|impressions)", re.I)
_CTR = re.compile(r"(クリック率|click-?through rate|\bctr\b)", re.I)
_ID = re.compile(r"^(動画|コンテンツ|content|video)$", re.I)
_TTL = re.compile(r"(動画のタイトル|video title)", re.I)
# CSV から取れるものは全部取る（Analytics API が無効でも表を出すため）
_VIEWS = re.compile(r"(^視聴回数$|^views$)", re.I)
_AVGT = re.compile(r"(平均視聴時間|average view duration)", re.I)
_AVGP = re.compile(r"(平均視聴率|average percentage viewed)", re.I)
_DUR = re.compile(r"(^長さ$|^duration$)", re.I)
_SUBS = re.compile(r"(チャンネル登録者|^subscribers$)", re.I)


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", (s or "")).lower()


def _span(a: str, b: str) -> int:
    """CSV の期間の日数。広い窓のほうを勝たせるために使う。"""
    try:
        return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days
    except ValueError:
        return 0


def _hms(s: str) -> int:
    """"0:11:47" → 707 秒。🔴 維持は秒で見る。読めなければ 0 でなく -1 を返す
    （0だと「0秒だった」と見分けが付かない）。"""
    parts = (s or "").strip().split(":")
    if not parts or not all(p.strip().isdigit() for p in parts):
        return -1
    v = 0
    for p in parts:
        v = v * 60 + int(p)
    return v


def auto_ingest_downloads(max_age_days: int = 60) -> int:
    """Downloads の Studio エクスポート ZIP を自動で取り込む。
    ZIP 内のファイル名は文字化けすることがあるので、**中身のヘッダ行**で選ぶ。"""
    dl = Path.home() / "Downloads"
    if not dl.exists():
        return 0
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    limit = dt.datetime.now() - dt.timedelta(days=max_age_days)
    got = 0
    for z in sorted(dl.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True):
        if dt.datetime.fromtimestamp(z.stat().st_mtime) < limit:
            continue
        try:
            with zipfile.ZipFile(z) as zf:
                for name in zf.namelist():
                    if not name.lower().endswith(".csv"):
                        continue
                    try:
                        text = zf.read(name).decode("utf-8-sig")
                    except UnicodeDecodeError:
                        continue
                    head = text.splitlines()[0] if text else ""
                    if not (_IMP.search(head) and _CTR.search(head)):
                        continue
                    (CSV_DIR / f"studio_{z.stem[:40]}.csv").write_text(text, encoding="utf-8")
                    got += 1
        except zipfile.BadZipFile:
            continue
    return got


def load_studio_csv(only_channel: str | None = None) -> dict:
    """🔴 `only_channel` を渡すと、**そのチャンネルの CSV だけ**読む。

    `analytics/studio_csv/` には**深読みフクロウの CSV も入っている**。
    動画IDで引くだけなら混ざっても害は無かったが、一覧として並べると
    **他チャンネルの動画が混ざる**（2026-09-04 に実際に出した）。
    Studio のエクスポートはファイル名にチャンネル名が入るので、それで絞る。
    """
    if not CSV_DIR.exists():
        return {}
    out: dict[str, dict] = {}
    # 🔴 同じ動画が複数の CSV に出る。**あとから読んだものが勝つ**ので、
    #    「期間が新しく・広い」ものを最後に読む。
    #    ⚠️ mtime で並べると、同じ実行で取り込んだ CSV どうしの順序が不定になり、
    #    　 8/1〜8/6 の古い窓（1本目が57再生）が 90日窓を上書きしていた（2026-09-04）。
    def _rank(p):
        m = re.search(r"(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})", p.name)
        if not m:
            return ("", "", p.stat().st_mtime)
        return (m.group(2), m.group(1) and _span(m.group(1), m.group(2)), p.stat().st_mtime)

    for path in sorted(CSV_DIR.glob("*.csv"), key=_rank):
        if only_channel and only_channel not in path.name:
            continue
        try:
            with path.open(encoding="utf-8-sig", newline="") as f:
                rows = list(csv.reader(f))
        except Exception:
            continue
        if not rows:
            continue
        # 🔴 Analytics API が無効でも表が出せるよう、**CSV から取れるものは全部取る**
        pats = {"imp": _IMP, "ctr": _CTR, "id": _ID, "ttl": _TTL,
                "views": _VIEWS, "avgsec": _AVGT, "avgpct": _AVGP,
                "dur": _DUR, "subs": _SUBS}
        idx = {k: None for k in pats}
        for i, h in enumerate(rows[0]):
            h = h.strip()
            for k, pat in pats.items():
                if idx[k] is None and pat.search(h):
                    idx[k] = i
                    break
        if idx["imp"] is None or idx["ctr"] is None:
            continue
        need = max(v for v in idx.values() if v is not None)
        for r in rows[1:]:
            if len(r) <= need:
                continue
            key = (r[idx["id"]].strip() if idx["id"] is not None and r[idx["id"]].strip()
                   else _norm(r[idx["ttl"]]) if idx["ttl"] is not None else None)
            if not key or key.lower() in ("total", "合計"):
                continue
            try:
                rec = {"impressions": int(float(r[idx["imp"]] or 0)),
                       "ctr": float(r[idx["ctr"]] or 0)}
            except ValueError:
                continue
            if idx["ttl"] is not None:
                rec["csvTitle"] = r[idx["ttl"]]
            for k, cast in (("views", int), ("avgpct", float),
                            ("dur", int), ("subs", int)):
                if idx[k] is not None:
                    try:
                        rec[k] = cast(float(r[idx[k]] or 0))
                    except ValueError:
                        pass
            if idx["avgsec"] is not None:      # "0:11:47" 形式
                rec["avgsec"] = _hms(r[idx["avgsec"]])
            out[key] = rec
    return out


# ─────────────────────────────────────────────── report
def cmd_report(a) -> int:
    ya, yt = apis()
    ch = guard_channel(yt)
    # Analytics は 2〜3日の反映ラグがあるので既定の終端は「今日」。
    # 途中経過も見たいので until は今日にし、ラグがあることを但し書きで出す。
    until = a.until or dt.date.today().isoformat()
    since = a.since or (dt.date.fromisoformat(until) - dt.timedelta(days=a.days)).isoformat()

    ingested = auto_ingest_downloads()
    print(f"===== {ch['snippet']['title']}（{ch['snippet'].get('customUrl')}）"
          f" {since} 〜 {until} =====")
    print(f"登録者(現在) {ch['statistics'].get('subscriberCount')} 人"
          f" ／ 総再生(全期間) {ch['statistics'].get('viewCount')} 回"
          f" ／ 公開本数 {ch['statistics'].get('videoCount')}")
    print("⚠️ Analytics は直近1〜3日ぶんが未確定（あとから増える）")

    # 🔴 Analytics API が無効でも、Studio CSV の数字までは出す。
    #    2026-09-04：403 ひとつで全部落ちて、取れている CSV すら見られなかった。
    #    **片方が死んでも、もう片方は出す**（[[feedback-parsers-fail-closed]] の逆側の教訓＝
    #    「読めないものは0で埋めない」が「読めるものまで捨てる」ことにならないように）
    def try_q(*args, **kw):
        try:
            return q(ya, *args, **kw), None
        except Exception as e:      # noqa: BLE001
            msg = str(e)
            if "has not been used in project" in msg or "accessNotConfigured" in msg:
                return None, ("🔴 **YouTube Analytics API がこのプロジェクトで無効**。"
                              "維持率カーブ・流入元・日別は取れない。"
                              "→ Cloud Console で有効化するか --quota で別プロジェクトを指定")
            return None, f"取得できず: {msg[:200]}"

    ANALYTICS_OFF = []
    res, err = try_q(since, until,
                     "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,"
                     "subscribersGained,subscribersLost,likes,comments,shares")
    if err:
        print(f"\n[期間合計] {err}")
        ANALYTICS_OFF.append(err)
        cols, rows = [], []
    else:
        cols, rows = res
    tot = dict(zip(cols, rows[0])) if rows else {}
    if tot:
        net = int(tot["subscribersGained"]) - int(tot["subscribersLost"])
        print(f"\n[期間合計] 再生 {int(tot['views'])} / 視聴 {int(tot['estimatedMinutesWatched'])}分"
              f" / 平均視聴 {fmt_ms(float(tot['averageViewDuration']))}"
              f"（{float(tot['averageViewPercentage']):.1f}%）"
              f" / 登録 純{net:+d}（+{int(tot['subscribersGained'])} / -{int(tot['subscribersLost'])}）"
              f" / 高評価 {int(tot['likes'])} コメント {int(tot['comments'])} 共有 {int(tot['shares'])}")

    # 日別
    res, err = try_q(since, until, "views,estimatedMinutesWatched,subscribersGained", "day")
    drows = res[1] if res else []
    if drows:
        print("\n[日別]")
        for r in drows:
            print(f"  {r[0]}  再生 {int(r[1]):>5}  視聴 {int(r[2]):>5}分  登録 +{int(r[3])}")

    # 流入元 ← 「そもそも配信されているか」はここに出る
    res, err = try_q(since, until, "views,estimatedMinutesWatched",
                     "insightTrafficSourceType", "-views")
    if err:
        print(f"\n[流入元] {err}")
    else:
        trows = res[1]
        tv = sum(int(r[1]) for r in trows) or 1
        print("\n[流入元]  ← 配信されているかはここに出る")
        for r in trows:
            print(f"  {r[0]:<26} {int(r[1]):>5} 回 ({int(r[1])/tv*100:5.1f}%)"
                  f"  視聴 {int(r[2]):>5}分")

    # 動画別
    ctr_map = load_studio_csv(only_channel=CHANNEL)   # ★他chの CSV を混ぜない
    print(f"\n[Studio CSV] {len(ctr_map)} 行ぶんの CTR/インプレッションを読み込み"
          f"（今回取り込んだ ZIP: {ingested}／`{CHANNEL}` のCSVだけ）")
    if not ctr_map:
        print("  🔴 **0本。取り込めていない。** Studio の列名が変わった可能性がある。"
              "`analytics/studio_csv/` の1行目を見て _IMP/_CTR/_ID を直すこと")
    res, err = try_q(since, until,
                     "views,averageViewPercentage,averageViewDuration,subscribersGained,"
                     "estimatedMinutesWatched,likes",
                     "video", "-views", maxr=50)
    if err:
        print(f"\n[動画別] {err}")
        vrows = []
    else:
        vrows = res[1]
    videos = []
    if vrows:
        ids = [r[0] for r in vrows]
        meta = {}
        d = yt.videos().list(part="snippet,contentDetails,statistics",
                             id=",".join(ids)).execute()
        for v in d["items"]:
            meta[v["id"]] = (v["snippet"]["title"], v["contentDetails"]["duration"],
                             v["snippet"]["publishedAt"])
        print("\n[動画別]  🔴 維持は秒で見る（%は尺で自動に動く）")
        print(f"  {'再生':>5} {'維持秒':>8} {'(%)':>6} {'尺':>8} {'登録':>5} {'CTR':>7}  公開       タイトル")
        for r in vrows:
            vid = r[0]
            title, dur, pub = meta.get(vid, ("(取得不可)", "", ""))
            sec = iso_seconds(dur)
            rec = {"videoId": vid, "title": title, "duration": dur, "durSec": sec,
                   "publishedAt": pub, "views": int(r[1]),
                   "avgViewPct": round(float(r[2]), 1), "avgViewSec": int(r[3]),
                   "subsGained": int(r[4]), "minutesWatched": int(r[5]), "likes": int(r[6])}
            hit = ctr_map.get(vid) or ctr_map.get(_norm(title))
            if hit:
                rec.update(hit)
            videos.append(rec)
            ctr = f"{rec['ctr']:.1f}%" if "ctr" in rec else "  --   "
            flag = "" if rec["views"] >= MIN_VIEWS_AVG else "  ※参考値"
            print(f"  {rec['views']:>5} {fmt_ms(rec['avgViewSec']):>8} {rec['avgViewPct']:>5.1f}%"
                  f" {fmt_ms(sec):>8} {rec['subsGained']:>+5} {ctr:>7}"
                  f"  {pub[:10]} {title[:34]}{flag}")

    # 🔴 Analytics が使えないときは Studio CSV だけで表を作る。
    #    CSV には 視聴回数・平均視聴時間・平均視聴率・尺・登録者・インプレ・CTR が入っている。
    #    取れないのは **維持率カーブ（離脱点）と流入元と日別** だけ。
    if not videos and ctr_map:
        print("\n[動画別（Studio CSV だけで作成）]  🔴 維持は秒で見る（%は尺で自動に動く）")
        print(f"  {'再生':>5} {'維持秒':>8} {'(%)':>6} {'尺':>8} {'登録':>5} "
              f"{'インプレ':>7} {'CTR':>6}  タイトル")
        for key, c in sorted(ctr_map.items(), key=lambda kv: -(kv[1].get("views") or 0)):
            if not re.fullmatch(r"[A-Za-z0-9_-]{11}", key):
                continue          # 題名キーの行（同じ動画の重複）は出さない
            sec = c.get("dur") or 0
            rec = {"videoId": key, "title": c.get("csvTitle", ""),
                   "durSec": sec, "views": c.get("views", 0),
                   "avgViewSec": c.get("avgsec", -1),
                   "avgViewPct": c.get("avgpct", 0.0),
                   "subsGained": c.get("subs", 0),
                   "impressions": c.get("impressions"), "ctr": c.get("ctr"),
                   "source": "studio_csv"}
            videos.append(rec)
            flag = "" if rec["views"] >= MIN_VIEWS_AVG else "  ※参考値"
            print(f"  {rec['views']:>5} {fmt_ms(rec['avgViewSec']):>8} "
                  f"{rec['avgViewPct']:>5.1f}% {fmt_ms(sec):>8} {rec['subsGained']:>+5} "
                  f"{rec['impressions']:>7} {rec['ctr']:>5.1f}%  {rec['title'][:38]}{flag}")
        print("  ⚠️ この表は Studio の CSV が出どころ。**離脱点・流入元・日別は入っていない**")

    if not ctr_map:
        print("\n※ CTR とインプレッションは YouTube の公開APIに無い。"
              "Studio →アナリティクス→詳細モード→エクスポート→CSV を")
        print("   Downloads に置いたまま report を回せば自動で取り込む"
              f"（取り込んだZIP: {ingested}）")

    # 判断してよいかどうかを、道具の側から言う
    print("\n[判断してよいか]")
    for v in videos:
        if v["views"] < MIN_VIEWS_AVG:
            print(f"  {v['videoId']}: {v['views']}回 → 🔴 まだ判断しない"
                  f"（平均維持秒すら参考値。{MIN_VIEWS_AVG}回未満）")
        elif v["views"] < MIN_VIEWS_CURVE:
            print(f"  {v['videoId']}: {v['views']}回 → ⚠️ 平均維持秒までは見てよい。"
                  f"**カーブは読まない**（{MIN_VIEWS_CURVE}回未満）")
        else:
            print(f"  {v['videoId']}: {v['views']}回 → ✅ カーブも読んでよい")

    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    snap = {"generatedAt": dt.datetime.now().isoformat(timespec="seconds"),
            "range": {"since": since, "until": until},
            "channel": {"title": ch["snippet"]["title"],
                        "subscribers": ch["statistics"].get("subscriberCount"),
                        "totalViews": ch["statistics"].get("viewCount")},
            "totals": tot, "videos": videos}
    out = SNAP_DIR / f"{dt.date.today().isoformat()}.json"
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n保存: {out.relative_to(HERE)}")
    return 0


# ─────────────────────────────────────────────── retention（秒で出す）
def cmd_retention(a) -> int:
    ya, yt = apis()
    guard_channel(yt)
    d = yt.videos().list(part="snippet,contentDetails,statistics", id=a.video_id).execute()
    if not d.get("items"):
        raise SystemExit(f"動画が無い: {a.video_id}")
    it = d["items"][0]
    dur = iso_seconds(it["contentDetails"]["duration"])
    views = int(it["statistics"].get("viewCount", 0))
    print(f"{it['snippet']['title'][:50]}")
    print(f"尺 {fmt_ms(dur)}（{dur}秒）／再生 {views} 回")

    if views < MIN_VIEWS_CURVE:
        print(f"\n🔴 再生 {views} 回はカーブを読むには少なすぎる（目安 {MIN_VIEWS_CURVE} 回）。")
        print("   数字は出すが、**離脱点の判断には使わない**。")

    pub = it["snippet"]["publishedAt"][:10]
    since = a.since or pub
    until = a.until or dt.date.today().isoformat()
    try:
        cols, rows = q(ya, since, until, "audienceWatchRatio,relativeRetentionPerformance",
                       "elapsedVideoTimeRatio", filters=f"video=={a.video_id}")
    except Exception:
        cols, rows = q(ya, since, until, "audienceWatchRatio",
                       "elapsedVideoTimeRatio", filters=f"video=={a.video_id}")
    if not rows:
        print("\nカーブのデータがまだ無い。")
        return 0

    step = max(1, len(rows) // 40)
    print(f"\n  {'経過':>9} {'割合':>7}  （行={len(rows)}点・{step}点ごとに表示）")
    prev = None
    for i, r in enumerate(rows):
        ratio, watch = float(r[0]), float(r[1])
        sec = ratio * dur
        if i % step and i != len(rows) - 1:
            prev = watch
            continue
        bar = "█" * int(round(min(watch, 1.2) * 40))
        rel = f" rel {float(r[2]):.2f}" if len(r) > 2 else ""
        print(f"  {fmt_ms(sec):>9} {watch*100:6.1f}%  {bar}{rel}")
        prev = watch
    # 節目
    print("\n[節目]")
    for mark in (0.0, 0.02, 0.05, 0.10, 0.25, 0.50, 0.75, 1.0):
        near = min(rows, key=lambda r: abs(float(r[0]) - mark))
        print(f"  {fmt_ms(float(near[0]) * dur):>9}（{mark*100:5.1f}%地点） 残り {float(near[1])*100:5.1f}%")
    return 0


def cmd_auth(a) -> int:
    ya, yt = apis(interactive=True)
    ch = guard_channel(yt)
    _, rows = q(ya, "2020-01-01", dt.date.today().isoformat(), "views")
    print(f"ANALYTICS_TOKEN_OK -> {TOKEN}")
    print(f"  チャンネル: {ch['snippet']['title']}（{ch['snippet'].get('customUrl')}）")
    print(f"  全期間の再生: {rows}")
    return 0


def main() -> int:
    global QUOTA_PROJECT
    ap = argparse.ArgumentParser(description="事故検証ch の成績を読む")
    ap.add_argument("--quota", default=QUOTA_PROJECT,
                    help="課金先(quota project)。既定 drift-diary。"
                         "🔴 ここを None にすると Analytics が 403 になる（上のコメント参照）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("auth", help="Analytics 用トークンを発行（初回だけ）")
    p.set_defaults(fn=cmd_auth)

    p = sub.add_parser("report", help="総括＋動画別")
    p.add_argument("--days", type=int, default=90)
    p.add_argument("--since")
    p.add_argument("--until")
    p.set_defaults(fn=cmd_report)

    p = sub.add_parser("retention", help="維持率カーブ（🔴秒で出す）")
    p.add_argument("video_id")
    p.add_argument("--since")
    p.add_argument("--until")
    p.set_defaults(fn=cmd_retention)

    a = ap.parse_args()
    QUOTA_PROJECT = a.quota or None
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
