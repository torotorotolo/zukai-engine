# -*- coding: utf-8 -*-
"""upload_jiko.py — 事故検証ch「そのとき、何が起きたか」の投稿と予約。

深読みフクロウの `upload.py`（zankoku-sekkeizu）を土台に移植した。違いは3つ。

  1. 🔴 **このリポジトリは public** なので、トークンを書く前に
     `git check-ignore` で**本当に無視されるかを実測**する。無視されていなければ
     **書かずに落ちる**（.gitignore の `config/` を消したら落ちる、という作り）。
  2. **上げるのと予約するのを分けた。** 35分155MB は YouTube 側の処理に時間がかかり、
     処理の途中で公開すると**初速の視聴者に低い解像度が配信される**。
     → `up` で非公開のまま上げ、`status` で処理の完了を見てから `schedule` で予約する。
  3. 再生リストは作らない（テーマを固定して見えるため・開設用一式 §6）。

■ 使い方
    python tools/upload_jiko.py up                       # 非公開で上げる → 処理の完了を待ってサムネを貼り、原寸で測る
    python tools/upload_jiko.py status <videoId>         # 処理の進み具合を見る
    python tools/upload_jiko.py schedule <videoId> --at "2026-08-03T19:00:00+09:00"
    python tools/upload_jiko.py thumb <videoId>          # サムネだけ貼り直す（貼ったあと原寸で測る）
    python tools/upload_jiko.py thumbcheck <videoId>     # 貼られたサムネが高解像度かを測るだけ（何も変えない）
    python tools/upload_jiko.py thumbcheck --selftest    # 物差しの陽性対照（YouTube にもネットにも出ない）

  🔴 2026-10-24：**サムネの解像度の門番**＝`up`・`thumb` は貼ったあと、`schedule`・`public` は変える前に、
     YouTube の大きい版を原寸で取って手元の絵と照らす（平均の差＋鮮明さの比）。通らなければ止まる（`check_thumb()`）。

■ 前提
  - `config/meta_titan.json` にタイトル・説明・タグ・サムネのパス
  - OAuth クライアントは zunda-5ch の client_secret.json を流用（同一Googleアカウント）
  - トークンは事故検証ch専用の `config/token_jiko.json` に分離
    → 初回だけブラウザ同意が要る。
      **同意画面で必ず「ゆっくり事故調査ノート」を選ぶこと。**
      （2026-10-05 に「仕事帰りの事故調査ノート」から改名・ハンドルは @jikochosa（旧 @shigotogaeri）。
       2026-09-24 にも「そのとき、何が起きたか」から改名している。チャンネルID UCb36M92_3zO76IFAm27UPiA は不変）
"""
import argparse
import io
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
ZUNDA = Path(r"C:\Users\konar\Desktop\zunda-5ch")   # OAuthクライアント資産の場所

CLIENT_SECRET = ZUNDA / "config" / "client_secret.json"
TOKEN = HERE / "config" / "token_jiko.json"
META = HERE / "config" / "meta_titan.json"
MP4 = HERE / "out" / "jiko" / "titan_audio-r29.mp4"

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CATEGORY_EDUCATION = "27"
# 🔴 名前が違えば cmd_up は止まる＝改名したらここも直す（2026-09-24「そのとき、何が起きたか」→「仕事帰りの事故調査ノート」・
#    2026-10-05 →「ゆっくり事故調査ノート」@jikochosa＝カズヤくんが Studio で改名・API の who で確かめた）
CHANNEL = "ゆっくり事故調査ノート"


# ── 🔴 トークンを public リポジトリへ置いてしまわないための門番 ──────────
def assert_ignored(path: Path) -> None:
    """`path` が git に無視されることを**実測**する。

    ⚠️ 「.gitignore に config/ と書いたから大丈夫」は確認ではない。
       書き間違い・打ち消しの `!` ・別の .gitignore で簡単にひっくり返る。
       git 自身に聞くのが唯一の確認方法。
    """
    r = subprocess.run(["git", "check-ignore", "-q", str(path)],
                       cwd=HERE, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(
            f"[中止] {path} が git に無視されていない。\n"
            "  このリポジトリは public。トークンを push したら、その瞬間に\n"
            "  チャンネルを他人へ渡したのと同じになる（git の履歴は消せない）。\n"
            "  → .gitignore に `config/` があるか確かめてから、もう一度。")


def get_credentials() -> Credentials:
    assert_ignored(TOKEN)          # ★読む前に確かめる（書くのは同意のあとなので）
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                raise SystemExit(f"client_secret.json が無い: {CLIENT_SECRET}")
            print("ブラウザで同意画面が開きます。")
            print(f"★必ず『{CHANNEL}』を選んでください（他のチャンネルを選ぶと、そちらへ上がります）。")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN.parent.mkdir(parents=True, exist_ok=True)
        assert_ignored(TOKEN)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return creds


def api():
    return build("youtube", "v3", credentials=get_credentials())


def whoami(yt) -> dict:
    """★どのチャンネルに繋がっているかを、上げる前に必ず出す。"""
    r = yt.channels().list(part="snippet,contentDetails,statistics,status", mine=True).execute()
    if not r.get("items"):
        raise SystemExit("[中止] チャンネルが取れない。同意したアカウントを確かめる。")
    it = r["items"][0]
    return {"id": it["id"], "title": it["snippet"]["title"],
            "handle": it["snippet"].get("customUrl", "（未設定）"),
            "videos": it["statistics"].get("videoCount", "?"),
            # 🔴 15分より長い動画を上げられるか。新しいチャンネルは
            #    youtube.com/verify の電話番号認証を通すまで allowed にならない。
            #    本編は35分なので、ここが allowed でないと**上げた時点で弾かれる**。
            "long": it["status"].get("longUploadsStatus", "?")}


def load_meta() -> dict:
    if not META.exists():
        raise SystemExit(f"メタファイルが無い: {META}")
    return json.loads(META.read_text(encoding="utf-8"))


def thumb_path(meta: dict):
    p = meta.get("thumbnail")
    if not p:
        return None
    thumb = Path(p)
    return thumb if thumb.is_absolute() else HERE / thumb


def set_thumb(yt, video_id: str, meta: dict) -> bool:
    thumb = thumb_path(meta)
    if thumb is None:
        print("[警告] メタに thumbnail が無い")
        return False
    if not thumb.exists():
        print(f"[警告] サムネが無い: {thumb}")
        return False
    # 🔴 2026-10-24：貼る前に手元の絵を確かめる＝YouTube の上限 2MB・1280x720 以上の 16:9
    #    （小さい絵を貼れば、YouTube がどう扱っても低解像度にしかならない）
    w, h = Image.open(thumb).size
    if thumb.stat().st_size > 2_000_000 or w < 1280 or h < 720 or w * 9 != h * 16:
        print(f"🔴 手元のサムネが条件（2MB 以下・1280x720 以上の 16:9）に合わない: "
              f"{thumb.stat().st_size:,} バイト・{w}x{h}")
        return False
    mime = "image/jpeg" if thumb.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    try:
        yt.thumbnails().set(videoId=video_id,
                            media_body=MediaFileUpload(str(thumb), mimetype=mime)).execute()
        print(f"サムネを貼った: {thumb.name}")
        return True
    except Exception as e:
        # 新規チャンネルは電話番号認証（youtube.com/verify）まで
        # カスタムサムネが使えず 403 になる。Studio の「テストと比較」の最中も 403。
        print(f"[警告] サムネを貼れなかった（あとで `thumb` で貼り直せる）: {e}")
        return False


# ── 🔴 サムネの解像度の門番（2026-10-24 追加） ──────────────────────────
#   カズヤくん（10-24）「稀にサムネイルの画像が低解像度でアップされることがあります」＝21本目 rxIz2f3gqmA は
#   公開から1週間ほど低解像度のまま出ていて CTR が悪く、高解像度に直したら大きく改善 → 再投稿（GLppqima2ts）。
#   それまでの照合は絵を**縮めてから**比べていた（ep21_r01「縮小して平均の差 0.2」）／1280x720 でも平均の差だけ
#   （640x360 から引き伸ばした絵でも差 4.06＝しきい値 8 の内）＝**ぼやけた絵でも ✓ になった**。
#   ここでは YouTube の大きい版を原寸で取り、手元の絵を同じ大きさにした物と
#   ①平均の差（同じ絵か） ②鮮明さの比（ラプラシアン＝となりの点との明るさの差の平均・YouTube ÷ 手元）で照らす。
#   較正（10-24・qa_out/ep21_reup/thumb_calib.txt・thumb_audit.txt）＝正しく貼られた版の maxres 1.04〜1.11（24本）・
#   webp の版 0.93〜0.98／陽性対照（手元の絵を落として 1280x720 へ戻した物）960x540 0.85・854x480 0.79・
#   640x360 0.66・480x270 0.54。
#   ⚠️ 原因は分かっていない（処理の途中〈sd〉で貼ると起きる？＝推測。10-24 の GLppqima2ts は sd のうちに貼って 1.08）
#   ＝原因に頼らず、貼るのは処理が終わってから・貼ったら必ず測る・予約と公開の前にも測る。
THUMB_MAD_MAX = 8.0          # 平均の差（0〜255）。別の絵なら 40 以上（21本目の H と H_inv で 47）
THUMB_SHARP_MIN = 0.95       # 鮮明さの比（jpg の版）
THUMB_SHARP_MIN_WEBP = 0.85  # webp の版は同じ絵でも 0.93〜0.98 に下がる


def _lap(img) -> float:
    a = np.asarray(img.convert("L"), np.float32)
    return float(np.abs(4 * a[1:-1, 1:-1] - a[:-2, 1:-1] - a[2:, 1:-1]
                        - a[1:-1, :-2] - a[1:-1, 2:]).mean())


def thumb_compare(img, local, smin: float) -> tuple:
    """YouTube の版 `img` と手元の絵 `local`（同じ大きさに縮める）→ (良いか, 平均の差, 鮮明さの比)。"""
    ref = local.resize(img.size, Image.LANCZOS)
    mad = float(np.abs(np.asarray(img, np.int16) - np.asarray(ref, np.int16)).mean())
    sharp = _lap(img) / max(_lap(ref), 1e-6)
    return img.size == (1280, 720) and mad < THUMB_MAD_MAX and sharp >= smin, mad, sharp


def _fetch_img(url: str):
    # 貼った直後の素の URL は前の画像を返す＝?t= を足す（記憶 reference-youtube-thumb-cache-bust）。
    # 非公開の動画の URL は署名の「?sqp=…」つき＝切ると 404＝そのまま & で足す
    sep = "&" if "?" in url else "?"
    req = urllib.request.Request(f"{url}{sep}t={int(time.time())}",
                                 headers={"User-Agent": "Mozilla/5.0 (zukai-engine)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")


def check_thumb(yt, video_id: str, local_path) -> tuple:
    """🔴 貼られているサムネが手元の絵と同じで、**高解像度のまま**か → (ok, 表の行)。測れなければ ok=False。"""
    if local_path is None or not Path(local_path).exists():
        return False, [f"🔴 手元のサムネが無い: {local_path}"]
    local = Image.open(local_path).convert("RGB")
    r = yt.videos().list(part="snippet,status", id=video_id).execute()
    if not r.get("items"):
        return False, [f"🔴 動画が見つからない: {video_id}"]
    it = r["items"][0]
    th = it["snippet"].get("thumbnails", {})
    mx = th.get("maxres")
    if not mx or (mx.get("width"), mx.get("height")) != (1280, 720):
        return False, [f"🔴 maxres（1280x720）の版が無い＝低解像度のまま（ある版 {sorted(th)}）"]
    urls = [("maxres", mx["url"], THUMB_SHARP_MIN)]
    if it["status"].get("privacyStatus") == "public":
        # ホーム・検索で配る版。公開中だけ素の URL で取れる（非公開・予約中は署名が要る）
        urls += [("hq720.jpg", f"https://i.ytimg.com/vi/{video_id}/hq720.jpg", THUMB_SHARP_MIN),
                 ("maxres.webp", f"https://i.ytimg.com/vi_webp/{video_id}/maxresdefault.webp", THUMB_SHARP_MIN_WEBP),
                 ("hq720.webp", f"https://i.ytimg.com/vi_webp/{video_id}/hq720.webp", THUMB_SHARP_MIN_WEBP)]
    ok, rows = True, []
    for name, url, smin in urls:
        try:
            img = _fetch_img(url)
        except urllib.error.HTTPError as e:
            ok = False
            rows.append(f"🔴 {name}: 取れない（HTTP {e.code}）")
            continue
        good, mad, sharp = thumb_compare(img, local, smin)
        ok = ok and good
        rows.append(f"{'✓' if good else '🔴'} {name} {img.size[0]}x{img.size[1]}：平均の差 {mad:.2f}"
                    f"（{THUMB_MAD_MAX:g} 未満）・鮮明さの比 {sharp:.2f}（{smin:g} 以上）")
    return ok, rows


def wait_thumb(yt, video_id: str, local_path, tries: int = 8, every: int = 15) -> tuple:
    """貼った直後は前の絵が返ることがある＝15秒ごとに最大 tries 回測る。"""
    for i in range(tries):
        ok, rows = check_thumb(yt, video_id, local_path)
        if ok or i + 1 == tries:
            return ok, rows
        time.sleep(every)


def apply_thumb(yt, video_id: str, meta: dict) -> bool:
    """貼る → 原寸で測る。通らなければ1回だけ貼り直して測る。"""
    for attempt in (1, 2):
        if not set_thumb(yt, video_id, meta):
            return False
        ok, rows = wait_thumb(yt, video_id, thumb_path(meta))
        print("\n".join("  " + r for r in rows))
        if ok:
            print("✓ サムネは高解像度で貼れている")
            return True
        print(f"🔴 サムネが高解像度で貼れていない（{attempt} 回目）" + ("＝貼り直す" if attempt == 1 else ""))
    return False


def wait_processed(yt, video_id: str, limit_s: int = 1800, every: int = 20) -> bool:
    """処理が succeeded・hd になるまで待つ（hd でもまだ processing のことがある＝両方を見る）。"""
    t0 = time.time()
    while True:
        it = yt.videos().list(part="processingDetails,contentDetails", id=video_id).execute()["items"][0]
        ps = it["processingDetails"].get("processingStatus")
        df = it["contentDetails"].get("definition")
        print(f"  処理 {ps}・画質 {df}（{time.time() - t0:.0f}秒）", flush=True)
        if ps == "succeeded" and df == "hd":
            return True
        if ps in ("failed", "rejected", "terminated") or time.time() - t0 > limit_s:
            return False
        time.sleep(every)


def thumb_gate(yt, video_id: str) -> None:
    """🔴 予約・公開の前の門番：サムネが高解像度で貼れていなければ止める（--force でも通さない）。"""
    ok, rows = wait_thumb(yt, video_id, thumb_path(load_meta()), tries=3)
    print("サムネの門番:\n" + "\n".join("  " + r for r in rows))
    if not ok:
        raise SystemExit(
            "[中止] サムネが高解像度で貼れていない（低解像度のまま出すと CTR が落ちる＝21本目で実際に起きた）。\n"
            f"  → `python tools/upload_jiko.py --meta <メタ> thumb {video_id}` で貼り直してから、もう一度。")


def cmd_up(args) -> int:
    mp4 = Path(args.mp4) if args.mp4 else MP4
    if not mp4.is_absolute():
        mp4 = HERE / mp4
    if not mp4.exists():
        raise SystemExit(f"動画が無い: {mp4}")
    meta = load_meta()

    yt = api()
    who = whoami(yt)
    print(f"接続先: {who['title']}（{who['handle']}／動画{who['videos']}本）")
    if who["title"] != CHANNEL:
        raise SystemExit(
            f"[中止] 繋がっているのが『{who['title']}』で、狙いの『{CHANNEL}』ではない。\n"
            f"  → {TOKEN} を消して、同意し直す。")
    if who["long"] != "allowed" and not args.force:
        raise SystemExit(
            f"[中止] 15分より長い動画を上げられない（longUploadsStatus={who['long']}）。\n"
            "  本編は35分なので、このまま上げても弾かれる。\n"
            "  → https://www.youtube.com/verify で電話番号認証を通してから、もう一度。\n"
            "  ⚠️ --force で無視できるが、それは**弾かれるかどうかを実測する**ためのもの。\n"
            "     弾かれた動画は非公開のまま残るので、あとで手で消す。")
    if who["long"] != "allowed":
        print(f"[!] longUploadsStatus={who['long']} のまま --force で進む（弾かれるか実測する）")

    print(f"動画: {mp4.name}（{mp4.stat().st_size / 1e6:.1f} MB）")
    print(f"題　: {meta['title']}")
    print("非公開で上げる（予約はあとで `schedule`）")

    body = {
        "snippet": {"title": meta["title"], "description": meta["description"],
                    "tags": meta.get("tags", []), "categoryId": CATEGORY_EDUCATION,
                    "defaultLanguage": "ja", "defaultAudioLanguage": "ja"},
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                   "license": "youtube", "embeddable": True},
    }
    media = MediaFileUpload(str(mp4), chunksize=8 * 1024 * 1024, resumable=True,
                            mimetype="video/mp4")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    resp, last = None, -1
    while resp is None:
        st, resp = req.next_chunk()
        if st and int(st.progress() * 100) != last:
            last = int(st.progress() * 100)
            print(f"  {last}%", end="\r", flush=True)

    vid = resp["id"]
    print(f"\n上がった: https://youtu.be/{vid}")
    print(f"管理　　: https://studio.youtube.com/video/{vid}/edit")

    log = HERE / "config" / "uploaded.json"
    rec = json.loads(log.read_text(encoding="utf-8")) if log.exists() else []
    rec.append({"id": vid, "file": mp4.name, "title": meta["title"],
                "uploaded_at": datetime.now().isoformat(timespec="seconds")})
    log.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")

    # 🔴 2026-10-24：サムネは処理が終わって hd になってから貼り、貼ったら原寸で測る（上の「サムネの解像度の門番」）
    print("処理が終わるのを待つ（サムネは hd になってから貼る）")
    if not wait_processed(yt, vid):
        print(f"[!] 処理が終わらない・失敗した＝サムネはまだ貼っていない。終わったら `thumb {vid}`")
        return 1
    if not apply_thumb(yt, vid, meta):
        print(f"🔴 サムネが高解像度で貼れていない＝このままでは `schedule`／`public` は止まる。`thumb {vid}` で貼り直す")
        return 1
    print(f"\n次: python tools/upload_jiko.py schedule {vid} --at \"…+09:00\"（または public）")
    return 0


def cmd_status(args) -> int:
    yt = api()
    r = yt.videos().list(part="status,processingDetails,contentDetails,snippet",
                         id=args.video_id).execute()
    if not r.get("items"):
        raise SystemExit(f"動画が見つからない: {args.video_id}")
    it = r["items"][0]
    pd, st, cd = it["processingDetails"], it["status"], it["contentDetails"]
    prog = pd.get("processingProgress") or {}
    print(f"題　　　: {it['snippet']['title'][:40]}…")
    print(f"処理　　: {pd.get('processingStatus')}"
          + (f"（{prog.get('partsProcessed')}/{prog.get('partsTotal')}）" if prog else ""))
    print(f"画質　　: {cd.get('definition')}（hd＝高解像度の版が出来ている）")
    print(f"公開設定: {st.get('privacyStatus')}"
          + (f"／予約 {st.get('publishAt')}" if st.get("publishAt") else ""))
    if pd.get("processingFailureReason"):
        print(f"[!] 失敗理由: {pd['processingFailureReason']}")
    return 0


def cmd_schedule(args) -> int:
    at = datetime.fromisoformat(args.at)
    if at.tzinfo is None:
        raise SystemExit('時刻に時差を付ける。例 "2026-08-03T19:00:00+09:00"')
    if at <= datetime.now(timezone.utc).astimezone(at.tzinfo):
        raise SystemExit(f"[中止] 予約時刻が過去: {args.at}")

    yt = api()
    r = yt.videos().list(part="status,processingDetails,snippet", id=args.video_id).execute()
    if not r.get("items"):
        raise SystemExit(f"動画が見つからない: {args.video_id}")
    it = r["items"][0]
    ps = it["processingDetails"].get("processingStatus")
    if ps != "succeeded" and not args.force:
        raise SystemExit(
            f"[中止] 処理がまだ終わっていない（{ps}）。\n"
            "  この状態で予約すると、初速の視聴者に低い解像度が配信されて\n"
            "  維持率が実力より低く出る。終わるまで待つ（--force で無視できる）。")
    thumb_gate(yt, args.video_id)   # 🔴 2026-10-24：サムネが高解像度でなければ予約しない

    # ⚠️ videos.update は**その part を丸ごと置き換える**。いま入っている status を
    #    読んでから足りない分だけ足す（消すと「子ども向け」などが既定に戻る）。
    #    uploadStatus / madeForKids は読み取り専用なので送らない。
    WRITABLE = ("privacyStatus", "license", "embeddable", "publicStatsViewable",
                "selfDeclaredMadeForKids")
    st = {k: v for k, v in it["status"].items() if k in WRITABLE}
    st.update(privacyStatus="private",
              publishAt=at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"))

    yt.videos().update(part="status", body={"id": args.video_id, "status": st}).execute()
    print(f"予約した: {args.at}")
    print(f"  UTC   : {st['publishAt']}")
    print(f"  確認  : https://studio.youtube.com/video/{args.video_id}/edit")
    return 0


def cmd_public(args) -> int:
    """🔴 いますぐ公開する（予約ではない）。2026-08-16 追加。

    `schedule` は**未来の時刻しか受け付けない**ので「いますぐ出す」ができなかった。
    ⚠️ `schedule` と同じ門番を残す：**処理が終わる前に公開すると、初速の視聴者に
       低い解像度が配信されて維持率が実力より低く出る。**--force で無視できる。
    ⚠️ `videos.update` は part を丸ごと置き換えるので、いまの status を読んでから
       書ける項目だけ差し替える（消すと「子ども向け」などが既定に戻る）。
       `publishAt` は送らない＝予約が入っていたら外れる。
    """
    yt = api()
    r = yt.videos().list(part="status,processingDetails,snippet",
                         id=args.video_id).execute()
    if not r.get("items"):
        raise SystemExit(f"動画が見つからない: {args.video_id}")
    it = r["items"][0]
    ps = it["processingDetails"].get("processingStatus")
    if ps != "succeeded" and not args.force:
        raise SystemExit(
            f"[中止] 処理がまだ終わっていない（{ps}）。\n"
            "  この状態で公開すると、初速の視聴者に低い解像度が配信されて\n"
            "  維持率が実力より低く出る。終わるまで待つ（--force で無視できる）。")
    thumb_gate(yt, args.video_id)   # 🔴 2026-10-24：サムネが高解像度でなければ公開しない

    WRITABLE = ("license", "embeddable", "publicStatsViewable",
                "selfDeclaredMadeForKids")
    st = {k: v for k, v in it["status"].items() if k in WRITABLE}
    st["privacyStatus"] = "public"
    yt.videos().update(part="status",
                       body={"id": args.video_id, "status": st}).execute()
    print(f"公開した: https://youtu.be/{args.video_id}")
    print(f"  題　　: {it['snippet']['title']}")
    print(f"  確認  : https://studio.youtube.com/video/{args.video_id}/edit")
    return 0


def cmd_private(args) -> int:
    """🔴 公開中の動画を非公開に戻す（2026-10-05 追加・18本目＝リメイクの公開と同時に旧版 3本目を非公開にするため）。

    ⚠️ `videos.update` は part を丸ごと置き換えるので、いまの status を読んでから書ける項目だけ差し替える
       （消すと「子ども向け」などが既定に戻る）。`publishAt` は送らない＝予約が入っていたら外れる。
    ⚠️ 題・説明・タグ・サムネには触らない（`part=status` だけ）。前後で読んで、公開設定だけが変わったことを確かめる。
    ⚠️ **公開ずみの動画は直さない**（記憶 feedback-published-videos-are-not-revised）＝これは中身を直す操作ではない。
       カズヤくんの GO があったときだけ回す。
    """
    yt = api()
    r = yt.videos().list(part="status,snippet", id=args.video_id).execute()
    if not r.get("items"):
        raise SystemExit(f"動画が見つからない: {args.video_id}")
    it = r["items"][0]
    before = dict(it["status"])
    print(f"題　　　: {it['snippet']['title'][:50]}…")
    print(f"変更前　: {before.get('privacyStatus')}")
    if before.get("privacyStatus") == "private":
        print("✓ もう非公開（何もしない）")
        return 0
    WRITABLE = ("license", "embeddable", "publicStatsViewable", "selfDeclaredMadeForKids")
    st = {k: v for k, v in before.items() if k in WRITABLE}
    st["privacyStatus"] = "private"
    yt.videos().update(part="status", body={"id": args.video_id, "status": st}).execute()
    after = yt.videos().list(part="status", id=args.video_id).execute()["items"][0]["status"]
    print(f"変更後　: {after.get('privacyStatus')}")
    for k in ("license", "embeddable", "publicStatsViewable", "madeForKids"):
        if before.get(k) != after.get(k):
            raise SystemExit(f"🔴 {k} が変わってしまった: {before.get(k)} → {after.get(k)}")
    if after.get("privacyStatus") != "private":
        raise SystemExit("🔴 非公開になっていない")
    print(f"✓ 非公開にした: https://studio.youtube.com/video/{args.video_id}/edit")
    return 0


def cmd_retitle(args) -> int:
    """🔴 タイトル・説明・タグだけを差し替える（2026-09-08 追加）。

    ⚠️⚠️ **予約（`publishAt`）を落とさないための作り。**
       `videos.update` は**渡した part を丸ごと置き換える**。予約は `status` 側に
       入っているので、**`status` を送らなければ予約は無傷**である。
       ここでは `part=snippet` だけを送る。⚠️ それでも `snippet` の中は全部置き換わるので、
       **いまの snippet を読んでから、書ける項目をそのまま載せ直す**
       （`categoryId` を落とすと既定に戻り、`defaultAudioLanguage` は消える）。

    ⚠️ **前後で `status` を読んで表に出す。**「消えていないはず」で済ませない
       （[[feedback-verify-your-own-instrument]]）。予約が変わっていたら 🔴 で落ちる。
    """
    m = load_meta()
    yt = api()
    r = yt.videos().list(part="snippet,status", id=args.video_id).execute()
    if not r.get("items"):
        raise SystemExit(f"動画が見つからない: {args.video_id}")
    it = r["items"][0]
    before = dict(it["status"])
    sn = it["snippet"]
    print(f"変更前の題　: {sn['title']}")
    print(f"変更前の状態: {before.get('privacyStatus')}"
          f"／予約 {before.get('publishAt', 'なし')}")

    KEEP = ("categoryId", "defaultLanguage", "defaultAudioLanguage")
    body = {k: sn[k] for k in KEEP if k in sn}
    body["title"] = m["title"]
    body["description"] = m["description"]
    body["tags"] = m.get("tags", [])
    yt.videos().update(part="snippet",
                       body={"id": args.video_id, "snippet": body}).execute()

    r2 = yt.videos().list(part="snippet,status", id=args.video_id).execute()
    it2 = r2["items"][0]
    after = it2["status"]
    print(f"変更後の題　: {it2['snippet']['title']}")
    print(f"変更後の状態: {after.get('privacyStatus')}"
          f"／予約 {after.get('publishAt', 'なし')}")

    # 🔴 予約と公開設定が1文字でも変わっていたら落とす（fail closed）
    for k in ("privacyStatus", "publishAt"):
        if before.get(k) != after.get(k):
            raise SystemExit(
                f"🔴 {k} が変わってしまった: {before.get(k)} → {after.get(k)}\n"
                f"   すぐ直すこと: upload_jiko.py schedule {args.video_id} "
                f'--at "<元の時刻>"')
    print("✓ 予約と公開設定は変わっていない")
    print(f"  確認: https://studio.youtube.com/video/{args.video_id}/edit")
    return 0


def cmd_thumb(args) -> int:
    yt = api()
    return 0 if apply_thumb(yt, args.video_id, load_meta()) else 1


def cmd_thumbcheck(args) -> int:
    """貼られているサムネが高解像度かを測るだけ（何も変えない）。--selftest は物差しの陽性対照。"""
    if args.selftest:
        return thumb_selftest()
    if not args.video_id:
        raise SystemExit("videoId を渡す（または --selftest）")
    local = Path(args.local) if args.local else thumb_path(load_meta())
    if local is not None and not local.is_absolute():
        local = HERE / local
    ok, rows = check_thumb(api(), args.video_id, local)
    print(f"手元: {local.relative_to(HERE).as_posix() if local and local.is_relative_to(HERE) else local}")
    print("\n".join(rows))
    print("✓ 高解像度で貼れている" if ok else "🔴 高解像度で貼れていない（または手元と違う絵）")
    return 0 if ok else 1


def thumb_selftest() -> int:
    """物差しの陽性対照：作った絵をわざと小さくして 1280x720 へ戻した物（JPEG）を 🔴、落としていない物を ✓ と
    判定できるか。絵はその場で作る＝out/ に頼らない・YouTube にもネットにも出ない
    （記憶 feedback-selftest-must-not-reach-real-side-effects）。"""
    rng = np.random.default_rng(911)
    img = Image.fromarray(rng.integers(0, 256, (90, 160, 3), dtype=np.uint8)).resize((1280, 720), Image.BICUBIC)
    d = ImageDraw.Draw(img)
    for _ in range(14):   # サムネの太い字の縁のような、くっきりした線
        x, y = int(rng.integers(0, 1100)), int(rng.integers(0, 600))
        d.rectangle((x, y, x + 170, y + 110), outline=(220, 20, 30), width=14)
        d.ellipse((x + 25, y + 15, x + 135, y + 95), outline=(255, 255, 255), width=10)
    bad = 0
    for w in (1280, 960, 854, 640, 480):
        deg = img.resize((w, round(w * 9 / 16)), Image.LANCZOS).resize((1280, 720), Image.BICUBIC)
        b = io.BytesIO()
        deg.save(b, "JPEG", quality=90)
        good, mad, sharp = thumb_compare(Image.open(b).convert("RGB"), img, THUMB_SHARP_MIN)
        want = w == 1280
        bad += good != want
        print(f"{'✓' if good == want else '🔴'} {w}x{round(w * 9 / 16)} → 1280x720：平均の差 {mad:.2f}・"
              f"鮮明さの比 {sharp:.2f} → {'通す' if good else '止める'}（狙い {'通す' if want else '止める'}）")
    print("✓ 物差しは低解像度を止め、正しい版を通す" if bad == 0 else f"🔴 物差しの判定が {bad} 件外れた")
    return 0 if bad == 0 else 1


def cmd_who(args) -> int:
    who = whoami(api())
    print(f"{who['title']}（{who['handle']}）／チャンネルID {who['id']}／動画{who['videos']}本")
    return 0


def main() -> int:
    global META
    ap = argparse.ArgumentParser(description="事故検証ch の投稿・予約")
    # 🔴 2026-08-06：2本目（123便）から**題材ごとにメタを分ける**。
    #    それまで META は1本目に固定で、`thumb` も `up` も
    #    **黙って1本目のタイトルとサムネを当てる**作りだった。
    #    → どのコマンドでも `--meta config/meta_ja123.json` を渡せるようにする。
    ap.add_argument("--meta", help=f"省略時 {META.name}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("up", help="非公開で上げる（処理を待ってサムネを貼り、原寸で測る）")
    p.add_argument("mp4", nargs="?", help=f"省略時 {MP4.name}")
    p.add_argument("--force", action="store_true",
                   help="15分超が未解禁でも上げてみる（弾かれるかの実測用）")
    p.set_defaults(fn=cmd_up)

    p = sub.add_parser("status", help="処理の進み具合")
    p.add_argument("video_id")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("schedule", help="予約公開の時刻を入れる")
    p.add_argument("video_id")
    p.add_argument("--at", required=True, help='例 "2026-08-03T19:00:00+09:00"')
    p.add_argument("--force", action="store_true", help="処理未完でも入れる")
    p.set_defaults(fn=cmd_schedule)

    p = sub.add_parser("public", help="いますぐ公開する（予約ではない）")
    p.add_argument("video_id")
    p.add_argument("--force", action="store_true", help="処理未完でも公開する")
    p.set_defaults(fn=cmd_public)

    p = sub.add_parser("private", help="公開中の動画を非公開に戻す（題・説明・サムネは触らない・GO のあとだけ）")
    p.add_argument("video_id")
    p.set_defaults(fn=cmd_private)

    p = sub.add_parser("retitle",
                       help="題・説明・タグをメタから貼り直す（予約は保つ）")
    p.add_argument("video_id")
    p.set_defaults(fn=cmd_retitle)

    p = sub.add_parser("thumb", help="サムネを貼り直す（貼ったあと原寸で測る・だめなら1回だけ貼り直す）")
    p.add_argument("video_id")
    p.set_defaults(fn=cmd_thumb)

    p = sub.add_parser("thumbcheck", help="貼られたサムネが高解像度かを測るだけ（何も変えない）")
    p.add_argument("video_id", nargs="?")
    p.add_argument("--local", help="照らす手元の絵（省略時はメタの thumbnail）")
    p.add_argument("--selftest", action="store_true", help="物差しの陽性対照（YouTube にもネットにも出ない）")
    p.set_defaults(fn=cmd_thumbcheck)

    p = sub.add_parser("who", help="どのチャンネルに繋がっているか")
    p.set_defaults(fn=cmd_who)

    args = ap.parse_args()
    if args.meta:
        META = Path(args.meta) if Path(args.meta).is_absolute() else HERE / args.meta
        if not META.exists():
            raise SystemExit(f"メタファイルが無い: {META}")
    print(f"メタ: {META.name}")
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
