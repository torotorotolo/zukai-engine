# -*- coding: utf-8 -*-
"""21本目の再投稿（2026-10-24）：YouTube の動画を API で読み、`config/meta_ep21.json` と照らす（24本目 `ep24_r01_verify_upload.py` の写し）。

照らす物＝題・説明・タグ・公開設定（--at を渡せば予約の時刻も）・子ども向けでない・処理・画質・尺・サムネ
（🔴 10-24 から `upload_jiko.check_thumb`＝大きい版を原寸で取り、平均の差＋鮮明さの比で照らす。それまでの
「小さい版でも差が小さければ ✓」は、ぼやけた低解像度の絵も通した＝21本目の再投稿のきっかけ）。
本編は 10-13 に公開した r01 と同じファイル（md5 1c27c601…）を上げ直す＝尺は r01 の記録で照らす。

    python qa_out/ep21_reup_verify_upload.py <videoId> [--out=pre] [--at=2026-10-25T10:00:00+09:00] [--thumb=out/thumb/…png]
      → qa_out/ep21_reup/verify_<out>.txt
    --thumb を省くと meta の thumbnail と照らす（前の動画 rxIz2f3gqmA は v1 を渡す）
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import upload_jiko as U  # noqa: E402

# 本編 r01 の尺（10-13 の受け取りで測った値＝36分26.6秒）＝ISO 8601 の秒の切り捨て・切り上げの両方を許す
DURATIONS = ("PT36M26S", "PT36M27S")
DUR_NOTE = "r01 の記録 36分26.6秒"


def opt(name, default=None):
    return next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith(f"--{name}=")), default)


def main():
    vid = sys.argv[1]
    name = opt("out", "check")
    at = opt("at")
    meta = json.loads((HERE / "config" / "meta_ep21.json").read_text(encoding="utf-8"))
    thumb = HERE / opt("thumb", meta["thumbnail"])
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
    pa = st.get("publishAt")
    if at:
        want = datetime.fromisoformat(at).astimezone(timezone.utc)
        got = datetime.fromisoformat(pa.replace("Z", "+00:00")) if pa else None
        rows.append(("予約", st.get("privacyStatus") == "private" and got == want,
                     f"{st.get('privacyStatus')}／予約 {pa}（狙い {want:%Y-%m-%dT%H:%M:%SZ}＝{at}）"))
    else:
        rows.append(("公開設定", True, f"{st.get('privacyStatus')}" + (f"／予約 {pa}" if pa else "")))
    rows.append(("処理", pd.get("processingStatus") == "succeeded", f"{pd.get('processingStatus')}"))
    rows.append(("画質", cd.get("definition") == "hd", f"{cd.get('definition')}"))
    rows.append(("尺", cd.get("duration") in DURATIONS, f"{cd.get('duration')}（{DUR_NOTE}）"))
    # 🔴 小さい版に落ちても ✓ にしない＝大きい版を原寸で・鮮明さの比も（upload_jiko.check_thumb＝10-24 の門番）
    t_ok, t_rows = U.check_thumb(yt, vid, thumb)
    rows.append(("サムネ", t_ok, f"{thumb.name}：" + "／".join(r.lstrip("✓🔴 ") for r in t_rows)))
    out = [f"videoId {vid}  https://youtu.be/{vid}  （読んだ時刻 {datetime.now():%Y-%m-%d %H:%M:%S}）",
           f"題: {sn['title']}"] + [f"{'✓' if ok else '🔴'} {k}: {v}" for k, ok, v in rows]
    text = "\n".join(out)
    p = HERE / "qa_out" / "ep21_reup" / f"verify_{name}.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if all(ok for _k, ok, _v in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
