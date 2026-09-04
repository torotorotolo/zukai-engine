# -*- coding: utf-8 -*-
"""nara_probe.py — NARA（米国立公文書館）の所蔵を「実際に数える」（2026-09-04）。

■ なぜ要るか
    3本目スレッシャー号が成功した最大の理由は「**素材が全部PDで、記録映画のカラーの
    コマまで使えた**」こと。その本体は Commons ではなく **NARA** にあった
    （記録映画 thr_85185 ＝ naId 85185・789秒）。
    → 題材を決める前に「NARA に何がどれだけあるか」を機械で数える。

■ 🔴 API の実測（2026-09-04・鍵は要らない）
    使える口 : https://catalog.archives.gov/proxy/records/search
      ⚠️ `/api/v2/records/search` と `/api/v1` は **HTML を返す**（鍵が要る）
    ⚠️⚠️ **`limit` は範囲でなく列挙。使えるのは 1 / 10 / 20 / 50 / 100 だけ。**
      2・3・5・25・200 を渡すと **HTTP 200 のまま HTML** が返る＝
      「200なら成功」と読むと**黙って間違った答え**になる
      （[[feedback-parsers-fail-closed]] / [[feedback-verify-your-own-instrument]]）。
      → この道具は毎回 **content-type が application/json か**を見て、違えば止まる。

■ 何を数えるか
    - 該当レコード総数（total）
    - **デジタル化ずみ**のレコード数と、その中の画像／動画／PDFの点数
    - `generalRecordsTypes` の内訳（Photographs / Moving Images / Textual Records …）
    - 🔴 `useRestriction.status` の内訳
      **"Unrestricted" が「使ってよい」の目印**。"Restricted - Possibly" は要確認
    - ファイルサイズの分布（解像度の代わり。**大きさは実物を見るまで断定しない**）

■ 使い方
    python tools/nara_probe.py search "USS Thresher SSN-593"
    python tools/nara_probe.py search "Texas City refinery explosion" --pages 5
    python tools/nara_probe.py search "Thresher" --type "Moving Images"
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
OUT_DIR = HERE / "analytics" / "materials"
URL = "https://catalog.archives.gov/proxy/records/search"
UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com)")

# 🔴 列挙。ここに無い値を渡すと HTML が返る（2026-09-04 実測）
VALID_LIMITS = (1, 10, 20, 50, 100)
PAGE = 100
SLEEP = 0.4

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA})


def _get(params, tries=4):
    """🔴 content-type を必ず見る。HTML が返ったら**止める**（0で埋めない）。"""
    last = None
    for i in range(tries):
        try:
            time.sleep(SLEEP)
            r = SESSION.get(URL, params=params, timeout=45)
            ct = r.headers.get("content-type", "")
            if not ct.startswith("application/json"):
                raise SystemExit(
                    f"[中止] NARA が JSON を返さない（HTTP {r.status_code} / {ct}）。"
                    f"params={params}\n"
                    f"　→ limit は 1/10/20/50/100 のいずれか。それ以外だと"
                    f" **200のままHTML**が返る")
            r.raise_for_status()
            return r.json()
        except SystemExit:
            raise
        except Exception as e:      # noqa: BLE001
            last = e
            time.sleep(2.0 * (i + 1))
    raise SystemExit(f"[中止] NARA API が読めない（{tries}回）: {last}")


def search(q, pages=3):
    """🔴 サーバ側の種類フィルタは**使わない**。

    `generalRecordsTypes` を params に足しても NARA は**黙って無視**する
    （2026-09-04 実測。フィルタ有無で結果が1件も変わらなかった）。
    「効いたつもりで数える」のがいちばん危ないので、絞るのは手元（`--type`）でやる。
    """
    if PAGE not in VALID_LIMITS:
        raise SystemExit(f"[中止] PAGE={PAGE} は使えない。{VALID_LIMITS} のいずれか")
    recs, total = [], None
    for p in range(pages):
        params = {"q": q, "limit": PAGE, "offset": p * PAGE}
        d = _get(params)
        hits = d.get("body", {}).get("hits", {})
        if total is None:
            total = (hits.get("total") or {}).get("value")
        got = hits.get("hits")
        if got is None:
            raise SystemExit(f"[中止] hits が読めない: {json.dumps(d)[:300]}")
        recs += [h.get("_source", {}).get("record", {}) for h in got]
        if len(got) < PAGE:
            break
    return total, recs


def summarize(name, q, total, recs):
    types, use, access, obj_types = Counter(), Counter(), Counter(), Counter()
    # 🔴 資料の種類ごとに数え分ける。混ぜると報告書PDFのページ画像が
    #    「写真の点数」に化ける（スレッシャーで 30,113点 のうち大半が Textual）
    by_type = Counter()
    n_digital, sizes = 0, []
    big, seen_url = [], set()
    for r in recs:
        rtypes = r.get("generalRecordsTypes") or ["(不明)"]
        for t in rtypes:
            types[t] += 1
        use[((r.get("useRestriction") or {}).get("status")) or "(記載なし)"] += 1
        access[((r.get("accessRestriction") or {}).get("status")) or "(記載なし)"] += 1
        objs = r.get("digitalObjects") or []
        if objs:
            n_digital += 1
        for o in objs:
            url = o.get("objectUrl")
            if url and url in seen_url:      # ⚠️ 同じ実体が複数回ぶら下がる
                continue
            if url:
                seen_url.add(url)
            ot = o.get("objectType") or "(不明)"
            obj_types[ot] += 1
            for t in rtypes:
                by_type[t] += 1
            sz = o.get("objectFileSize") or 0
            sizes.append(sz)
            if sz >= 500_000:
                big.append({"naId": r.get("naId"), "title": (r.get("title") or "")[:70],
                            "recordType": rtypes[0], "objectType": ot,
                            "sizeMB": round(sz / 1e6, 1), "url": url})
    sizes.sort()
    big.sort(key=lambda x: -x["sizeMB"])
    photo_like = sum(v for k, v in by_type.items()
                     if "Photograph" in k or "Moving Image" in k)
    return {
        "name": name, "query": q,
        "total_hits": total, "inspected": len(recs),
        "records_with_digital": n_digital, "digital_objects": len(sizes),
        "objects_by_record_type": dict(by_type.most_common()),
        "photo_and_film_objects": photo_like,
        "record_types": dict(types.most_common()),
        "object_types": dict(obj_types.most_common()),
        "use_restriction": dict(use.most_common()),
        "access_restriction": dict(access.most_common()),
        "size_median_MB": round(sizes[len(sizes) // 2] / 1e6, 2) if sizes else None,
        "objects_over_500KB": len(big),
        "big": big[:25],
    }


def _print(s):
    print(f"\n===== {s['name']}（NARA）=====")
    print(f"  該当 **{s['total_hits']}** 件中 {s['inspected']} 件を実測")
    print(f"  デジタル化ずみのレコード {s['records_with_digital']} 件"
          f"／デジタル物 {s['digital_objects']}点"
          f"（500KB超 {s['objects_over_500KB']}点・中央値 {s['size_median_MB']}MB）")
    print(f"  🔴 うち**写真・記録映像だけ**で **{s['photo_and_film_objects']}点**"
          f"（残りは報告書のページ画像。混ぜて数えない）")
    print(f"  種類ごとのデジタル物: {s['objects_by_record_type']}")
    print(f"  資料の種類（レコード数）: {s['record_types']}")
    print(f"  デジタル物の種類: {s['object_types']}")
    print(f"  🔴 利用制限: {s['use_restriction']}")
    print(f"     閲覧制限: {s['access_restriction']}")
    if s["big"]:
        print(f"  {'MB':>7}  {'naId':>10}  種類 / 題")
        for b in s["big"][:10]:
            print(f"  {b['sizeMB']:>7}  {str(b['naId']):>10}  "
                  f"{b['objectType'][:14]:<14} {b['title']}")
    if not s["total_hits"]:
        print("  🔴 0件。**「無い」ではなく「この語では出ない」**。"
              "艦名・地名・機関名・年号を替えて当たり直す"
              "（[[feedback-absence-of-a-word-is-not-absence]]）")


def cmd_search(a) -> int:
    total, recs = search(a.q, pages=a.pages)
    if a.type:   # 手元で絞る（サーバ側は無視されるため）
        before = len(recs)
        recs = [r for r in recs
                if any(a.type.lower() in (t or "").lower()
                       for t in (r.get("generalRecordsTypes") or []))]
        print(f"[手元で絞った] 種類 {a.type!r}: {before} → {len(recs)} 件"
              f"（⚠️ NARA のサーバ側フィルタは効かないので手元でやっている）")
    s = summarize(a.name or a.q, a.q, total, recs)
    _print(s)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in (a.name or a.q))[:60]
    p = OUT_DIR / f"nara_{safe}.json"
    p.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n保存: {p.relative_to(HERE)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="NARA の所蔵を実際に数える")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("search", help="語で探して数える")
    p.add_argument("q")
    p.add_argument("--name")
    p.add_argument("--pages", type=int, default=3, help=f"1ページ {PAGE} 件")
    p.add_argument("--type",
                   help="🔴 **手元で**絞る（NARAのサーバ側フィルタは黙って無視される）。"
                        "Photographs / Moving Images / Textual など部分一致")
    p.set_defaults(fn=cmd_search)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
