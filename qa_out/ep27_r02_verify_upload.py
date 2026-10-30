# -*- coding: utf-8 -*-
"""27本目 ⑥'：YouTube に上げた動画を API で読み、`config/meta_ep27.json` と照らす（26本目 `ep26_r01_verify_upload.py` の写し）。

照らす物＝題・説明・タグ・公開設定・子ども向けでない・処理・画質・尺・サムネの画素（maxres を ?t= 付きで取る＝
記憶 reference-youtube-thumb-cache-bust：貼った直後の素の URL は前の画像を返す）。
⚠️ 27本目はサムネの A/B テスト（10-30 カズヤくん）＝A（`config/meta_ep27.json` の thumbnail＝v6）を Claude が貼り、B（紺＝ep27_A6n_v6.png）は
   カズヤくんが Studio で手動。B を入れたあとは YouTube が返すサムネが A と違うことがある＝照らすのは A を貼った直後と予約の前後だけ。

    python qa_out/ep27_r02_verify_upload.py <videoId> [--out=pre]   → qa_out/ep27_r02/verify_<out>.txt
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import upload_jiko as U  # noqa: E402

# 本編 r02 の尺（設計 930.05秒＝15分30.05秒・受け取りの check_final で確かめる）＝ISO 8601 の秒の切り捨て・切り上げの両方を許す
DURATIONS = ("PT15M30S", "PT15M31S")
DUR_NOTE = "手元 15分30.1秒"


def main():
    vid = sys.argv[1]
    name = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--out=")), "check")
    if not DURATIONS:
        print("🔴 DURATIONS が未記入（本編を受け取って尺を測ってから）")
        return 1
    meta = json.loads((HERE / "config" / "meta_ep27.json").read_text(encoding="utf-8"))
    yt = U.api()
    it = yt.videos().list(part="snippet,status,processingDetails,contentDetails", id=vid).execute()["items"][0]
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
    # 🔴 2026-10-24：小さい版に落ちても ✓ にしない＝大きい版を原寸で・鮮明さの比も（upload_jiko.check_thumb）
    t_ok, t_rows = U.check_thumb(yt, vid, HERE / meta["thumbnail"])
    rows.append(("サムネ", t_ok, "／".join(r.lstrip("✓🔴 ") for r in t_rows)))
    out = [f"videoId {vid}  https://youtu.be/{vid}"] + [f"{'✓' if ok else '🔴'} {k}: {v}" for k, ok, v in rows]
    text = "\n".join(out)
    p = HERE / "qa_out" / "ep27_r02" / f"verify_{name}.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if all(ok for _k, ok, _v in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
