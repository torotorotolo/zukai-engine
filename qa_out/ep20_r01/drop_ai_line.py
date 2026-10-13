# -*- coding: utf-8 -*-
"""20本目（87-AJdfgvok）の概要欄から「サムネは生成AI」の1行だけを外す（2026-10-13・21本目 ⑥ のチャット）。
なぜ：10-13 にサムネを H 型 v1（地＝報告書の写真-124＝実際の写真）に差し替えた＝この行が事実と合わなくなった。
      カズヤくんの決め「その行を消すだけ」（題・ほかの行・タグは触らない）。
やり方：公開中の snippet をそのまま読み、description からその1行だけを取り除いて送り返す（題・タグ・カテゴリ・言語は読んだ値のまま）。
      videos.update は part を丸ごと置き換える＝読んだ値を全部入れて送る。送ったあと読み直して、変わったのがその1行だけかを確かめる。
    python qa_out/ep20_r01/drop_ai_line.py          # 確かめるだけ（書かない）
    python qa_out/ep20_r01/drop_ai_line.py --write  # 書く
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import upload_jiko as U          # noqa: E402

VID = "87-AJdfgvok"
LINE = "※ サムネイルの画像は、生成AIで作ったイメージです。実際の写真ではありません。本編の写真と映像は、すべて実際の記録です。"
KEEP = ("title", "description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage")

yt = U.api()
it = yt.videos().list(part="snippet,status", id=VID).execute()["items"][0]
sn, st = it["snippet"], it["status"]
lines = sn["description"].split("\n")
hits = [i for i, l in enumerate(lines) if l == LINE]
print(f"題　: {sn['title']}")
print(f"説明: {len(sn['description'])}字・その行 {len(hits)}件（行 {hits}）・公開設定 {st['privacyStatus']}")
if len(hits) != 1:
    raise SystemExit("🔴 その行がちょうど1件ではない。書かずに止めた。")
new_desc = "\n".join(l for i, l in enumerate(lines) if i != hits[0])
print(f"直したあと: {len(new_desc)}字（−{len(sn['description']) - len(new_desc)}）")
if "--write" not in sys.argv:
    print("（--write を付けると書く）")
    raise SystemExit(0)
body = {k: sn[k] for k in KEEP if k in sn}
body["description"] = new_desc
yt.videos().update(part="snippet", body={"id": VID, "snippet": body}).execute()
after = yt.videos().list(part="snippet,status", id=VID).execute()["items"][0]
a, s2 = after["snippet"], after["status"]
checks = [("題", a["title"] == sn["title"]), ("説明＝その1行だけ外した物", a["description"] == new_desc),
          ("タグ", a.get("tags") == sn.get("tags")), ("カテゴリ", a.get("categoryId") == sn.get("categoryId")),
          ("言語", (a.get("defaultLanguage"), a.get("defaultAudioLanguage")) == (sn.get("defaultLanguage"), sn.get("defaultAudioLanguage"))),
          ("公開設定", s2["privacyStatus"] == st["privacyStatus"])]
for n, ok in checks:
    print(f"{'✓' if ok else '🔴'} {n}")
sys.exit(0 if all(ok for _, ok in checks) else 1)
