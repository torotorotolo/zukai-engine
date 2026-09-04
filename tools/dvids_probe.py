# -*- coding: utf-8 -*-
"""dvids_probe.py — DVIDS（米国防総省の映像配信）の写真を1点ずつ実測する（2026-09-04）。

■ なぜ要るか
    ②素材で「FEMA・DVIDS の写真を数える」が残っていた。
    サーフサイドは **FEMA の写真班が現場に入っている**ので、ここが
    「事故そのものの絵」の主力になりうる。**枚数と実寸を数える。**

■ ⚠️ 踏んだ穴（2026-09-04）
    - `api.dvidshub.net` は **APIキーが要る**（鍵なしは 403）
    - 検索ページは **初回 202 を返す**（ボット判定）。素の requests では本文が空
      → 一覧はブラウザで採り、**ここには実測の口だけ**を残す
    - `www.dvidshub.net/download/image/<id>` は **403**（要ログイン）
    - ⭐ **CDN の `2000w_q95.jpg` は認証なしで通る**（実測 2000px 幅・約1MB）
      ＝ 1920x1080 に十分。原寸（2776px 等）は要らない

■ ⚠️ 権利（2026-09-04 に本文で確認）
    「米国政府の職員が職務として作った著作物は米国で著作権の対象にならない」＝PD。
    ただし **非DoD の権利が混ざりうる**ので1点ずつ出典を見る。
    🔴 **DoD（現 Department of War）の映像を使うと、非推奨の断り書きの表示義務が付く。**
       → FEMA（国土安全保障省）撮影のものだけ使えば、この義務は生じない。

■ 使い方
    python tools/dvids_probe.py measure --ids 6718327,6718324 --name surfside
    python tools/dvids_probe.py selftest
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import time
from pathlib import Path

import requests
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
OUT = HERE / "analytics" / "materials"
# ⚠️ CDN は素の requests でも通るが、Referer が無いと弾かれることがある
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
CDN = "https://d1ldvf68ux039x.cloudfront.net/thumbs/photos/{yymm}/{id}/{size}_q95.jpg"
FULL_W = 1280
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA})


def cdn_url(img_id: str, yymm: str, size: str = "2000w") -> str:
    return CDN.format(yymm=yymm, id=img_id, size=size)


def probe(img_id: str, yymm: str, orig: tuple[int, int] | None = None) -> dict:
    """実体を取って **PIL で測る**（ページに書いてある寸法を信じない）。

    🔴 **ただし CDN の `2000w` は小さい原本を引き伸ばして返す。**（2026-09-04 実測）
       例＝原寸 768x1024 の1点が `2000x2667` で返ってきた（2.6倍の水増し）。
       ＝ **取れたファイルの幅だけを見ると「全点が全画面に耐える」と嘘をつく。**
       → ページに出ている原寸（`orig`）を渡し、**小さいほうを採る**。
    """
    row = {"id": img_id, "yymm": yymm}
    if orig:
        row["orig_w"], row["orig_h"] = orig
    for size in ("2000w", "1000w"):
        u = cdn_url(img_id, yymm, size)
        try:
            r = SESSION.get(u, timeout=90,
                            headers={"Referer": f"https://www.dvidshub.net/image/{img_id}/"})
        except Exception as e:                    # noqa: BLE001
            row["err"] = f"{type(e).__name__}"
            continue
        if r.status_code != 200 or not r.headers.get("Content-Type", "").startswith("image"):
            continue
        im = Image.open(io.BytesIO(r.content))
        w, h = im.size
        # 🔴 実効の幅＝配信物と原本の**小さいほう**（引き伸ばしを実力に数えない）
        ew = min(w, row["orig_w"]) if orig else w
        row.update({"size": size, "url": u, "w": w, "h": h,
                    "eff_w": ew, "upscaled": bool(orig and w > row["orig_w"]),
                    "mode": im.mode, "bytes": len(r.content),
                    "fullscreen": ew >= FULL_W,
                    "landscape": w >= h})
        return row
    row.setdefault("err", "取れず")
    return row


def cmd_measure(a) -> int:
    """`--ids` は `id:origW x origH` の形も受ける（原寸を渡すと引き伸ばしを弾ける）。"""
    items = []
    for tok in (x.strip() for x in a.ids.split(",")):
        if not tok:
            continue
        if ":" in tok:
            i, wh = tok.split(":", 1)
            w, h = wh.lower().split("x")
            items.append((i, (int(w), int(h))))
        else:
            items.append((tok, None))
    yymms = [x.strip() for x in a.yymm.split(",")] if "," in a.yymm else [a.yymm] * len(items)
    rows = []
    for i, ((img_id, orig), ym) in enumerate(zip(items, yymms), 1):
        r = probe(img_id, ym, orig)
        rows.append(r)
        mark = " ⚠️引き伸ばし" if r.get("upscaled") else ""
        print(f"{i:>3}/{len(items)} 配信{r.get('w',0)}x{r.get('h',0)} "
              f"実効幅{r.get('eff_w',0):>5}  {r.get('bytes',0)/1e6:.2f}MB  {img_id}{mark}"
              f"{'  🔴 ' + r['err'] if r.get('err') else ''}")
        time.sleep(0.4)
    ok = [r for r in rows if r.get("fullscreen")]
    land = [r for r in rows if r.get("landscape")]
    up = [r for r in rows if r.get("upscaled")]
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / f"dvids_{a.name}.json"
    f.write_text(json.dumps(
        {"total": len(rows), "fullscreen": len(ok), "landscape": len(land),
         "upscaled": len(up), "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n計 {len(rows)}点 / **実効で幅1280px以上 {len(ok)}点** / 横長 {len(land)}点 "
          f"/ ⚠️CDNが引き伸ばしていた {len(up)}点")
    print(f"→ {f}")
    return 0


def selftest() -> int:
    """答えの分かっている問題を解かせる（共通ルール：道具は使う前に検算する）。"""
    bad = 0
    # ① ページ表示が 2776x2082 の1点。CDN の 2000w は幅2000のはず
    r = probe("6718327", "2107")
    if r.get("w") == 2000 and r.get("h") == 1500:
        print(f"✅ 6718327 = {r['w']}x{r['h']}（原寸 2776x2082 と同じ 4:3）")
    else:
        print(f"🔴 6718327 の実測が想定と違う: {r}")
        bad += 1
    # ② 存在しない id は静かに 0 を返さず err を立てること（fail closed）
    n = probe("999999999", "2107")
    if n.get("err") and not n.get("w"):
        print("✅ 無い id は err を立てる（0で埋めない）")
    else:
        print(f"🔴 無い id で寸法を返した: {n}")
        bad += 1
    print(f"{'🔴 検算 NG' if bad else '✅ 検算 OK'}（{bad}件）")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure")
    m.add_argument("--ids", required=True, help="画像IDをカンマ区切りで")
    m.add_argument("--yymm", required=True, help="配信年月 YYMM（IDと同数か1つ）")
    m.add_argument("--name", default="out")
    sub.add_parser("selftest")
    a = ap.parse_args()
    return selftest() if a.cmd == "selftest" else cmd_measure(a)


if __name__ == "__main__":
    sys.exit(main())
