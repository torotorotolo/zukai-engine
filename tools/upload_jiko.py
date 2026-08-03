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
    python tools/upload_jiko.py up                       # 非公開で上げるだけ
    python tools/upload_jiko.py status <videoId>         # 処理の進み具合を見る
    python tools/upload_jiko.py schedule <videoId> --at "2026-08-03T19:00:00+09:00"
    python tools/upload_jiko.py thumb <videoId>          # サムネだけ貼り直す

■ 前提
  - `config/meta_titan.json` にタイトル・説明・タグ・サムネのパス
  - OAuth クライアントは zunda-5ch の client_secret.json を流用（同一Googleアカウント）
  - トークンは事故検証ch専用の `config/token_jiko.json` に分離
    → 初回だけブラウザ同意が要る。
      **同意画面で必ず「そのとき、何が起きたか」を選ぶこと。**
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
ZUNDA = Path(r"C:\Users\konar\Desktop\zunda-5ch")   # OAuthクライアント資産の場所

CLIENT_SECRET = ZUNDA / "config" / "client_secret.json"
TOKEN = HERE / "config" / "token_jiko.json"
META = HERE / "config" / "meta_titan.json"
MP4 = HERE / "out" / "jiko" / "titan_audio-r29.mp4"

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CATEGORY_EDUCATION = "27"
CHANNEL = "そのとき、何が起きたか"


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


def set_thumb(yt, video_id: str, meta: dict) -> None:
    p = meta.get("thumbnail")
    if not p:
        return
    thumb = Path(p)
    if not thumb.is_absolute():
        thumb = HERE / thumb
    if not thumb.exists():
        print(f"[警告] サムネが無い: {thumb}")
        return
    mime = "image/jpeg" if thumb.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    try:
        yt.thumbnails().set(videoId=video_id,
                            media_body=MediaFileUpload(str(thumb), mimetype=mime)).execute()
        print(f"サムネを貼った: {thumb.name}")
    except Exception as e:
        # 新規チャンネルは電話番号認証（youtube.com/verify）まで
        # カスタムサムネが使えず 403 になる。落ちても後続は続ける。
        print(f"[警告] サムネを貼れなかった（あとで `thumb` で貼り直せる）: {e}")


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
    set_thumb(yt, vid, meta)

    log = HERE / "config" / "uploaded.json"
    rec = json.loads(log.read_text(encoding="utf-8")) if log.exists() else []
    rec.append({"id": vid, "file": mp4.name, "title": meta["title"],
                "uploaded_at": datetime.now().isoformat(timespec="seconds")})
    log.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n次: python tools/upload_jiko.py status {vid}")
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


def cmd_thumb(args) -> int:
    yt = api()
    set_thumb(yt, args.video_id, load_meta())
    return 0


def cmd_who(args) -> int:
    who = whoami(api())
    print(f"{who['title']}（{who['handle']}）／チャンネルID {who['id']}／動画{who['videos']}本")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="事故検証ch の投稿・予約")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("up", help="非公開で上げる")
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

    p = sub.add_parser("thumb", help="サムネを貼り直す")
    p.add_argument("video_id")
    p.set_defaults(fn=cmd_thumb)

    p = sub.add_parser("who", help="どのチャンネルに繋がっているか")
    p.set_defaults(fn=cmd_who)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
