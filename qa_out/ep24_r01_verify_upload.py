# -*- coding: utf-8 -*-
"""24本目 ⑥：YouTube に上げた動画を API で読み、`config/meta_ep24.json` と照らす（23本目 `ep23_r01_verify_upload.py` の写し）。

照らす物＝題・説明・タグ・公開設定・子ども向けでない・処理・画質・尺・サムネの画素（maxres を ?t= 付きで取る＝
記憶 reference-youtube-thumb-cache-bust：貼った直後の素の URL は前の画像を返す）。

    python qa_out/ep24_r01_verify_upload.py <videoId> [--out=pre]   → qa_out/ep24_r01/verify_<out>.txt
"""
import io
import json
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import upload_jiko as U  # noqa: E402

# 本編 r01 の尺（受け取りで測った値＝2,222.43秒）＝ISO 8601 の秒の切り捨て・切り上げの両方を許す
DURATIONS = ("PT37M2S", "PT37M3S")
DUR_NOTE = "手元 37分02.4秒"


def thumb_mad(url, local):
    # ⚠️ 非公開の動画のサムネの URL は署名つきの「?sqp=…」を持つ＝切り落とすと 404（22本目 10-15 の1回目）。そのまま使い、印は & で足す
    sep = "&" if "?" in url else "?"
    req = urllib.request.Request(f"{url}{sep}t={int(time.time())}", headers={"User-Agent": "Mozilla/5.0 (zukai-engine)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        yt = Image.open(io.BytesIO(r.read())).convert("RGB")
    lo = Image.open(local).convert("RGB").resize(yt.size, Image.LANCZOS)
    return float(np.abs(np.asarray(yt, np.int16) - np.asarray(lo, np.int16)).mean()), yt.size


def main():
    vid = sys.argv[1]
    name = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--out=")), "check")
    meta = json.loads((HERE / "config" / "meta_ep24.json").read_text(encoding="utf-8"))
    it = U.api().videos().list(part="snippet,status,processingDetails,contentDetails", id=vid).execute()["items"][0]
    sn, st, pd, cd = it["snippet"], it["status"], it["processingDetails"], it["contentDetails"]
    rows = []
    rows.append(("題", sn["title"] == meta["title"], f"{len(sn['title'])}字"))
    d_ok = sn["description"] == meta["description"]
    if not d_ok:
        a, b = sn["description"], meta["description"]
        k = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        note = f"{len(a)}字／手元 {len(b)}字・最初の違い {k} 字目：YouTube {a[k:k + 20]!r}／手元 {b[k:k + 20]!r}"
    else:
        note = f"{len(sn['description'])}字"
    rows.append(("説明", d_ok, note))
    # ⚠️ YouTube はタグを並べ替えて返す（22本目 10-15 実測）＝並びは比べない
    rows.append(("タグ", sorted(sn.get("tags", [])) == sorted(meta["tags"]), f"{len(sn.get('tags', []))}個"))
    rows.append(("子ども向けでない", st.get("selfDeclaredMadeForKids") is False and st.get("madeForKids") is False,
                 f"self={st.get('selfDeclaredMadeForKids')} made={st.get('madeForKids')}"))
    rows.append(("公開設定", True, f"{st.get('privacyStatus')}" + (f"／予約 {st.get('publishAt')}" if st.get("publishAt") else "")))
    rows.append(("処理", pd.get("processingStatus") == "succeeded", f"{pd.get('processingStatus')}"))
    rows.append(("画質", cd.get("definition") == "hd", f"{cd.get('definition')}"))
    rows.append(("尺", cd.get("duration") in DURATIONS, f"{cd.get('duration')}（{DUR_NOTE}）"))
    th = sn.get("thumbnails", {})
    best = th.get("maxres") or th.get("standard") or th.get("high")
    if best:
        mad, size = thumb_mad(best["url"], HERE / meta["thumbnail"])
        rows.append(("サムネ", mad < 8.0, f"画素の差の平均 {mad:.2f}（{size[0]}x{size[1]}・{'maxres' if 'maxres' in th else '小さい版'}）"))
    else:
        rows.append(("サムネ", False, "サムネの URL が無い"))
    out = [f"videoId {vid}  https://youtu.be/{vid}"] + [f"{'✓' if ok else '🔴'} {k}: {v}" for k, ok, v in rows]
    text = "\n".join(out)
    p = HERE / "qa_out" / "ep24_r01" / f"verify_{name}.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if all(ok for _k, ok, _v in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
