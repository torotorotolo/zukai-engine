# -*- coding: utf-8 -*-
"""19本目の YouTube 上の値を config/meta_ep19.json と全項目で照合する（2026-10-07・⑥）。読むだけ（書き込みはしない）。
18本目の qa_out/ep18_r01/verify_upload.py の写し（違い＝読む設定の名前・設計の尺 2,227.9秒）。
使い方: python qa_out/ep19_r01/verify_upload.py <videoId> [予約の時刻 UTC 例 2026-10-08T08:00:00Z]
"""
import io
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import upload_jiko as U          # noqa: E402

vid = sys.argv[1]
want_at = sys.argv[2] if len(sys.argv) > 2 else None
meta = json.loads((HERE / "config" / "meta_ep19.json").read_text(encoding="utf-8"))
yt = U.api()
it = yt.videos().list(part="snippet,status,contentDetails,processingDetails", id=vid).execute()["items"][0]
sn, st = it["snippet"], it["status"]
checks = [
    ("題", sn["title"] == meta["title"], f"{len(sn['title'])}字"),
    ("説明", sn["description"] == meta["description"], f"{len(sn['description'])}字"),
    ("タグ（集合）", set(sn.get("tags", [])) == set(meta["tags"]), f"{len(sn.get('tags', []))}件／設定 {len(meta['tags'])}件"),
    ("カテゴリ", sn.get("categoryId") == U.CATEGORY_EDUCATION, sn.get("categoryId")),
    ("言語", sn.get("defaultLanguage") == "ja" and sn.get("defaultAudioLanguage") == "ja",
     f"{sn.get('defaultLanguage')}／音声 {sn.get('defaultAudioLanguage')}"),
    ("子ども向けでない", st.get("selfDeclaredMadeForKids") is False or st.get("madeForKids") is False,
     f"madeForKids={st.get('madeForKids')}"),
    ("ライセンス・埋め込み", st.get("license") == "youtube" and st.get("embeddable") is True,
     f"{st.get('license')}・{st.get('embeddable')}"),
    # ⚠️ YouTube の尺は秒を切り上げる（2,288.33秒＝38分08.33秒 → PT38M9S）＝1回目は「PT38M8S と完全一致」を求めて
    #    🔴 を出した（物差しの誤り）。設計の秒と1秒以内で照らす
    ("尺", abs(sum(int(n) * {"H": 3600, "M": 60, "S": 1}[u] for n, u in
                  __import__("re").findall(r"(\d+)([HMS])", it["contentDetails"].get("duration", ""))) - 2227.9) <= 1.0,
     f"{it['contentDetails'].get('duration')}（設計 2,227.9秒）"),
    ("処理", it.get("processingDetails", {}).get("processingStatus") == "succeeded",
     it.get("processingDetails", {}).get("processingStatus")),
]
if want_at:
    checks.append(("予約", st.get("privacyStatus") == "private" and st.get("publishAt", "").startswith(want_at.rstrip("Z")),
                   f"{st.get('privacyStatus')}・publishAt {st.get('publishAt')}（狙い {want_at}）"))
else:
    checks.append(("公開設定", True, f"{st.get('privacyStatus')}" + (f"・予約 {st['publishAt']}" if st.get("publishAt") else "")))
# サムネ＝YouTube の最大の版を落として、手元の PNG と縮小して比べる（貼り間違いを見る）
try:
    from PIL import Image
    th = sn["thumbnails"]
    url = (th.get("maxres") or th.get("standard") or th.get("high"))["url"]
    with urllib.request.urlopen(url, timeout=30) as r:
        a = Image.open(io.BytesIO(r.read())).convert("L").resize((64, 36))
    b = Image.open(HERE / meta["thumbnail"]).convert("L").resize((64, 36))
    diff = sum(abs(x - y) for x, y in zip(a.getdata(), b.getdata())) / (64 * 36)
    checks.append(("サムネ", diff < 12, f"縮小して平均の差 {diff:.1f}（{url.rsplit('/', 1)[-1]}）"))
except Exception as e:                   # noqa: BLE001
    checks.append(("サムネ", False, f"読めない: {type(e).__name__}: {e}"))
for name, ok, note in checks:
    print(f"{'✓' if ok else '🔴'} {name}：{note}")
bad = [n for n, ok, _ in checks if not ok]
print("✓ 全項目一致" if not bad else f"🔴 食い違い {bad}")
sys.exit(1 if bad else 0)
