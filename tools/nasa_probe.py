# -*- coding: utf-8 -*-
"""NASA 画像庫（images.nasa.gov）を **撮影年で割って** 束にする（②素材）。

■ なぜ要るか
    `commons_probe.py` は Wikimedia Commons しか見ない。8本目（コロンビア号）の①で
    NASA 画像庫に「Columbia Debris Hangar 総370件」が見つかったが、
    **370 は「あいまい検索のヒット数」であって在庫ではない。**
    → [[feedback-inventory-is-not-usable-material]]

■ この道具が守る3つの決まり（①で3回踏んだ失敗への手当て）
    1. 🔴 **MUST／NG の網は「キャプション（写真の説明そのもの）」にだけ当てる。**
       ⚠️ Commons では題名がキャプションなので「題名だけに当てる」が正しい
       （[[feedback-inventory-is-not-usable-material]]）。**NASA 画像庫は構造が違う。**
       2026-09-14 の実測＝8本目の778件のうち **543件（70%）は `title` が資産IDそのもの**
       （`KSC-03PD-0436`）で、写真の説明は `description` に入っている。
       ここで「題名だけ」を機械的に守ると**本物が全部落ちる**ので、
       既定は `--field caption`＝`title` が ID のときだけ `description` を見る。
       ⚠️ それでも「説明に語が出てくるだけ」の取り違えは残るので、最後は `--list` を1行ずつ読む。
    2. 🔴 **撮影年（`date_created`）で割る。**
       API の `year_start/year_end` は**登録側の申告**なので、返ってきた `date_created` で
       もう一度自分で割る（申告と中身が食い違う件があった）。
    3. 🔴 **実寸は原本の画素で測る。**`links` のサムネや `description` の記述を信じない。
       原本 JPEG/PNG の**先頭だけ**を Range で取ってヘッダから w×h を読む（全部は落とさない）。

■ ⚠️ この道具が見ていないもの
    - **何が写っているか（意味）。** 網は候補を絞る道具であって、選ぶ道具ではない。
      最後は `--list` の一覧を人が1行ずつ読む。
    - インク率・余白。⇒ `src_probe.py` の担当（絞ったあとに回す）

■ 権利
    NASA の画像は原則 PD（米連邦職員の職務著作）だが、**例外がある**
    （契約企業の撮影・ESA/JAXA 提供・ロゴ・人物の肖像）。
    `--list` に `center` と `photographer/secondary_creator` を出すので、**採る前に見る**。

■ 使い方
    python tools/nasa_probe.py search --q "Columbia debris" --year 2003 --key col_debris \
        --out analytics/materials/ep8_nasa.json
    python tools/nasa_probe.py net  analytics/materials/ep8_nasa.json --net ref/ep8/nets.json
    python tools/nasa_probe.py dims analytics/materials/ep8_nasa.json --key col_debris --limit 60
    python tools/nasa_probe.py list analytics/materials/ep8_nasa.json --key col_debris
    python tools/nasa_probe.py selftest
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

API = "https://images-api.nasa.gov/search"
ASSET = "https://images-api.nasa.gov/asset/"
UA = "Mozilla/5.0 (compatible; zukai-engine/1.0; +research)"
HEAD_BYTES = 196608          # 原本の先頭だけ（192KB）。JPEG の SOF はふつうここまでに来る
PAGE_MAX = 100               # API の1ページの上限


# ────────────────────────────────────────────────────────────── HTTP

def _get(url: str, headers: dict | None = None, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _get_json(url: str, timeout: int = 60):
    return json.loads(_get(url, timeout=timeout).decode("utf-8", "replace"))


# ─────────────────────────────────────────────────── 画像の実寸（ヘッダだけ読む）

def dims_from_bytes(buf: bytes) -> tuple[int, int] | None:
    """JPEG / PNG / GIF / TIFF の先頭バイト列から (w, h) を返す。読めなければ None。"""
    if buf[:8] == b"\x89PNG\r\n\x1a\n" and buf[12:16] == b"IHDR":
        w, h = struct.unpack(">II", buf[16:24])
        return int(w), int(h)
    if buf[:6] in (b"GIF87a", b"GIF89a"):
        w, h = struct.unpack("<HH", buf[6:10])
        return int(w), int(h)
    if buf[:2] == b"\xff\xd8":                                   # JPEG
        i, n = 2, len(buf)
        while i + 3 < n:
            if buf[i] != 0xFF:
                i += 1
                continue
            m = buf[i + 1]
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            if i + 4 > n:
                break
            seglen = struct.unpack(">H", buf[i + 2:i + 4])[0]
            # SOF0..SOF15（DHT=C4 / JPG=C8 / DAC=CC は除く）
            if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                if i + 9 > n:
                    break
                h, w = struct.unpack(">HH", buf[i + 5:i + 9])
                return int(w), int(h)
            i += 2 + seglen
        return None
    if buf[:4] in (b"II*\x00", b"MM\x00*"):                       # TIFF
        le = buf[:2] == b"II"
        e = "<" if le else ">"
        off = struct.unpack(e + "I", buf[4:8])[0]
        if off + 2 > len(buf):
            return None
        cnt = struct.unpack(e + "H", buf[off:off + 2])[0]
        w = h = None
        for k in range(cnt):
            p = off + 2 + k * 12
            if p + 12 > len(buf):
                break
            tag, typ = struct.unpack(e + "HH", buf[p:p + 4])
            val = struct.unpack(e + "I", buf[p + 8:p + 12])[0]
            if typ == 3:
                val = struct.unpack(e + "H", buf[p + 8:p + 10])[0]
            if tag == 256:
                w = val
            elif tag == 257:
                h = val
        return (int(w), int(h)) if w and h else None
    return None


def dims_from_url(url: str, timeout: int = 60) -> tuple[int, int] | None:
    """原本の先頭 HEAD_BYTES だけを Range で取って w×h を読む。"""
    try:
        buf = _get(url, headers={"Range": f"bytes=0-{HEAD_BYTES - 1}"}, timeout=timeout)
    except Exception:
        try:                                                     # Range 非対応なら諦めて全部
            buf = _get(url, timeout=timeout)[:HEAD_BYTES]
        except Exception:
            return None
    return dims_from_bytes(buf)


# ────────────────────────────────────────────────────────────── search

def _year_of(s: str | None) -> int | None:
    if not s:
        return None
    m = re.match(r"(\d{4})", str(s))
    return int(m.group(1)) if m else None


def cmd_search(a) -> int:
    out = Path(a.out)
    db = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    items: dict[str, dict] = {}
    page, total = 1, None
    while True:
        q = {"q": a.q, "media_type": a.media_type, "page": str(page)}
        if a.year:
            q["year_start"] = q["year_end"] = str(a.year)
        url = API + "?" + urllib.parse.urlencode(q)
        try:
            j = _get_json(url)
        except urllib.error.HTTPError as e:
            print(f"  ⚠️ HTTP {e.code} page={page}")
            break
        col = j.get("collection", {})
        if total is None:
            total = col.get("metadata", {}).get("total_hits")
            print(f"  総ヒット {total}")
        got = col.get("items", [])
        if not got:
            break
        for it in got:
            d = (it.get("data") or [{}])[0]
            nid = d.get("nasa_id")
            if not nid:
                continue
            items[nid] = {
                "nasa_id": nid,
                "title": (d.get("title") or "").strip(),
                "date_created": d.get("date_created"),
                "year": _year_of(d.get("date_created")),
                "center": d.get("center"),
                "creator": d.get("photographer") or d.get("secondary_creator"),
                "keywords": d.get("keywords") or [],
                "desc_head": (d.get("description") or "")[:1200],
                "href": it.get("href"),
            }
        page += 1
        if page > a.max_pages or len(got) < PAGE_MAX:
            break
        time.sleep(0.2)

    rec = db.setdefault(a.key, {})
    rec.setdefault("queries", [])
    rec["queries"].append({"q": a.q, "year": a.year, "total_hits": total, "got": len(items)})
    pool = {x["nasa_id"]: x for x in rec.get("items", [])}
    pool.update(items)
    rec["items"] = sorted(pool.values(), key=lambda x: x["nasa_id"])
    rec["measured"] = time.strftime("%Y-%m-%d")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")

    yr = {}
    for x in rec["items"]:
        yr[x["year"]] = yr.get(x["year"], 0) + 1
    print(f"  拾った {len(items)} / 束の累計 {len(rec['items'])}")
    print("  撮影年の内訳:", dict(sorted(yr.items(), key=lambda kv: (kv[0] is None, kv[0]))))
    return 0


# ───────────────────────────────────────────────── net（MUST／NG を題名だけに当てる）

ID_TITLE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9\-_]{3,23}$")


def caption(x: dict) -> str:
    """写真の説明そのもの。NASA 画像庫は `title` が資産IDのことが多いので、そのときだけ
    `description` を使う。⚠️ 両方をつなげて当てると「説明に語が出るだけ」を拾うのでつなげない。"""
    t = (x.get("title") or "").strip()
    if ID_TITLE.match(t) and len(t.split()) <= 2:
        return (x.get("desc_head") or "").strip()
    return t


_WORD_CACHE: dict[str, re.Pattern] = {}


def word_re(w: str) -> re.Pattern:
    """🔴 **語境界で当てる。**素の `in` は短い語で偽陽性を出す
    （2026-09-14 実測＝`"iss"` が `mission` に当たって850件中366件を拾った。
    7本目でも `"ft"` が `left`/`shift` に当たっている → [[feedback-verify-your-own-instrument]]）。
    多語（`"leading edge"`）もそのまま書ける。"""
    p = _WORD_CACHE.get(w)
    if p is None:
        p = _WORD_CACHE[w] = re.compile(r"(?<!\w)" + re.escape(w.lower().strip()) + r"(?!\w)")
    return p


def hit(t: str, words: list[str]) -> str | None:
    for w in words:
        if word_re(w).search(t):
            return w
    return None


def apply_net(items: list[dict], must: list[str], ng: list[str], year: int | None,
              field: str = "caption") -> list[dict]:
    """🔴 当てるのはキャプション1本だけ（`field="title"` で題名に固定できる）。"""
    keep = []
    for x in items:
        t = ((x.get("title") or "") if field == "title" else caption(x)).lower()
        if year is not None and x.get("year") != year:
            x["drop"] = f"year={x.get('year')}"
            continue
        h = hit(t, ng)
        if h:
            x["drop"] = "ng:" + h
            continue
        if must and not hit(t, must):
            x["drop"] = "must"
            continue
        x.pop("drop", None)
        keep.append(x)
    return keep


def cmd_net(a) -> int:
    db = json.loads(Path(a.db).read_text(encoding="utf-8"))
    net = json.loads(Path(a.net).read_text(encoding="utf-8"))
    for key, rec in db.items():
        if a.key and key != a.key:
            continue
        n = net.get(key) or net.get("_default") or {}
        kept = apply_net(rec["items"], n.get("must", []), n.get("ng", []), n.get("year"), a.field)
        rec["kept"] = [x["nasa_id"] for x in kept]
        # 🔴 陽性対照＝網を外したら何件になるか（値で見る。件数が動かない網は効いていない）
        base = len(apply_net([dict(i) for i in rec["items"]], [], [], None, a.field))
        print(f"{key:18s} 全{len(rec['items']):4d} → 網を通った {len(kept):4d}"
              f"（網なし {base}）must={len(n.get('must', []))} ng={len(n.get('ng', []))} year={n.get('year')}")
    Path(a.db).write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


# ────────────────────────────────── archive.org の NASA 束（images.nasa.gov に無いものがある）
#
# 🔴 2026-09-14（8本目②）の実測。images.nasa.gov を全部当たっても **0件** だった
#    CAIB の衝突試験写真（JSC2003-E-40558 ほか）が、archive.org の
#    `humanspaceflightcollection`（NASA の旧 spaceflight.nasa.gov のアーカイブ）に
#    **1536x1017** で在った。⚠️ **「NASA の画像庫を当たった」＝NASA の画像を当たった、ではない。**

IA_SEARCH = "https://archive.org/advancedsearch.php?"
IA_META = "https://archive.org/metadata/"
IA_DL = "https://archive.org/download/"


def cmd_search_ia(a) -> int:
    out = Path(a.out)
    db = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    rows, page, got_all = [], 1, 0
    while True:
        u = (IA_SEARCH + urllib.parse.urlencode(
            {"q": a.q, "rows": "500", "page": str(page), "output": "json"})
            + "&fl%5B%5D=identifier&fl%5B%5D=description&fl%5B%5D=date&fl%5B%5D=title")
        j = _get_json(u, timeout=180)["response"]
        if page == 1:
            print(f"  総ヒット {j['numFound']}")
        docs = j.get("docs", [])
        if not docs:
            break
        rows += docs
        got_all += len(docs)
        if got_all >= j["numFound"] or page >= a.max_pages:
            break
        page += 1
        time.sleep(0.3)

    items: dict[str, dict] = {}
    for d in rows:
        desc = d.get("description") or ""
        if isinstance(desc, list):
            desc = " ".join(desc)
        items[d["identifier"]] = {
            "nasa_id": d["identifier"],
            "title": (d.get("title") or "").strip(),
            "date_created": str(d.get("date") or ""),
            "year": _year_of(d.get("date")),
            "center": "IA",
            "creator": None,
            "keywords": [],
            "desc_head": desc[:1200],
            "href": IA_META + d["identifier"],
        }
    rec = db.setdefault(a.key, {})
    rec.setdefault("queries", []).append({"q": a.q, "src": "archive.org", "got": len(items)})
    pool = {x["nasa_id"]: x for x in rec.get("items", [])}
    pool.update(items)
    rec["items"] = sorted(pool.values(), key=lambda x: x["nasa_id"])
    rec["measured"] = time.strftime("%Y-%m-%d")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    yr: dict = {}
    for x in rec["items"]:
        yr[x["year"]] = yr.get(x["year"], 0) + 1
    print(f"  拾った {len(items)} / 束の累計 {len(rec['items'])}")
    print("  撮影年の内訳:", dict(sorted(yr.items(), key=lambda kv: (kv[0] is None, kv[0]))))
    return 0


def ia_orig_url(ident: str) -> str | None:
    """archive.org の item から**原本**の画像1点を選ぶ。派生（_thumb / __ia_thumb）は採らない。"""
    try:
        j = _get_json(IA_META + ident, timeout=120)
    except Exception:
        return None
    best = None
    for f in j.get("files", []):
        n = f.get("name", "")
        if n.startswith("__") or "_thumb" in n or "_files.xml" in n:
            continue
        if (f.get("format") or "").lower() in ("jpeg", "jpg", "png", "tiff"):
            sz = int(f.get("size") or 0)
            if best is None or sz > best[0]:
                best = (sz, n)
    return IA_DL + f"{ident}/{urllib.parse.quote(best[1])}" if best else None


# ──────────────────────────────────────────────── buckets（章ごとの欄に振り分ける）

def cmd_buckets(a) -> int:
    """章（＝台本の欄）ごとに MUST／NG を当てて、**欄ごとの在庫**を数える。

    ⚠️ ここで出る数は「候補」であって在庫ではない。`--list-slot` で1行ずつ読んで初めて素材になる。
    """
    db = json.loads(Path(a.db).read_text(encoding="utf-8"))
    rec = db[a.key]
    slots = json.loads(Path(a.slots).read_text(encoding="utf-8"))
    gng = slots.get("_global_ng", [])
    yr = slots.get("_year")
    base = [x for x in rec["items"] if yr is None or x.get("year") == yr]
    items = [x for x in base if not hit(caption(x).lower(), gng)]
    print(f"全{len(rec['items'])}件 − 年{yr}で外れた {len(rec['items']) - len(base)}件 "
          f"− 全体NG {len(base) - len(items)}件 = {len(items)}件\n")
    assign: dict[str, list[str]] = {}
    used: set[str] = set()
    print(f"{'欄':22s} {'候補':>5s} {'w>=1280':>8s} {'未測':>5s}")
    for name, n in slots.items():
        if name.startswith("_"):
            continue
        got = apply_net([dict(x) for x in items], n.get("must", []),
                        n.get("ng", []) + gng, yr)
        ids = [x["nasa_id"] for x in got]
        assign[name] = ids
        used |= set(ids)
        by = {x["nasa_id"]: x for x in rec["items"]}
        big = sum(1 for i in ids if (by[i].get("w") or 0) >= 1280)
        un = sum(1 for i in ids if by[i].get("w") is None)
        mark = "🔴" if len(ids) == 0 else ("⚠️" if len(ids) < 3 else "  ")
        print(f"{mark}{name:20s} {len(ids):5d} {big:8d} {un:5d}")
    rec["slots"] = assign
    orphan = [x["nasa_id"] for x in items if x["nasa_id"] not in used]
    rec["slot_orphans"] = orphan
    print(f"\nどの欄にも入らなかった: {len(orphan)}件（`--list-slot _orphan` で読む）")
    Path(a.db).write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


# ────────────────────────────────────────────────────────────── dims

def orig_url(nasa_id: str) -> str | None:
    try:
        j = _get_json(ASSET + urllib.parse.quote(nasa_id))
    except Exception:
        return None
    hrefs = [i.get("href", "") for i in j.get("collection", {}).get("items", [])]
    for tag in ("~orig.", "~large.", "~medium."):
        for h in hrefs:
            if tag in h and h.lower().rsplit(".", 1)[-1] in ("jpg", "jpeg", "png", "tif", "tiff"):
                return h
    return None


def cmd_dims(a) -> int:
    db = json.loads(Path(a.db).read_text(encoding="utf-8"))
    rec = db[a.key]
    by = {x["nasa_id"]: x for x in rec["items"]}
    if a.slot:
        ids = rec.get("slots", {}).get(a.slot, [])
    else:
        ids = rec.get("kept") or [x["nasa_id"] for x in rec["items"]]
    if a.limit:
        ids = ids[:a.limit]
    done = ok = 0

    def save() -> None:
        """🔴 **db を読み直してから、この key の分だけ書き戻す。**
        丸ごと書き戻すと、走っているあいだに別の key が足されていた場合に**黙って消す**
        （2026-09-14 に踏みかけた）。途中保存もするので、途中で止めても測った分は残る。"""
        cur = json.loads(Path(a.db).read_text(encoding="utf-8")) if Path(a.db).exists() else {}
        cur[a.key] = rec
        Path(a.db).write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding="utf-8")

    todo = [n for n in ids if a.force or not by[n].get("w")]

    def one(nid: str):
        x = by[nid]
        u = ia_orig_url(nid) if x.get("center") == "IA" else orig_url(nid)
        return nid, u, (dims_from_url(u) if u else None)

    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for nid, u, d in ex.map(one, todo):
            x = by[nid]
            x["orig"] = u
            x["w"], x["h"] = d if d else (None, None)
            ok += bool(d)
            done += 1
            if done % 40 == 0:
                print(f"  …{done}/{len(todo)} 読めた {ok}", flush=True)
                save()
    save()
    ws = [x["w"] for x in by.values() if x.get("w")]
    big = [w for w in ws if w >= 1280]
    print(f"  測った {done}（読めた {ok}）／幅1280以上 {len(big)} / {len(ws)}")
    return 0


# ────────────────────────────────────────────────────────────── list

def cmd_list(a) -> int:
    db = json.loads(Path(a.db).read_text(encoding="utf-8"))
    rec = db[a.key]
    by = {x["nasa_id"]: x for x in rec["items"]}
    if a.slot == "_orphan":
        ids = rec.get("slot_orphans", [])
    elif a.slot:
        ids = rec.get("slots", {}).get(a.slot, [])
    else:
        ids = rec.get("kept") or [x["nasa_id"] for x in rec["items"]]
    for nid in ids:
        x = by[nid]
        if a.min_w and not (x.get("w") and x["w"] >= a.min_w):
            continue
        wh = f"{x.get('w') or '?'}x{x.get('h') or '?'}"
        print(f"{nid:22s} {wh:>11s} {x.get('date_created', '')[:10]:10s} "
              f"{(x.get('center') or ''):5s} {caption(x)[:a.chars]}")
    return 0


# ────────────────────────────────────────────────────────────── selftest

def cmd_selftest(a) -> int:
    """陽性対照＝**値**で見る（件数だけの対照は全件該当の指標で動かない）。"""
    import io
    from PIL import Image
    bad = 0

    # 1. ヘッダの読み取り：作った画像の実寸を当てられるか（値で照合）
    for fmt, wh in (("JPEG", (1913, 1251)), ("PNG", (640, 480)), ("GIF", (321, 77))):
        b = io.BytesIO()
        Image.new("RGB", wh).save(b, fmt)
        got = dims_from_bytes(b.getvalue())
        print(f"  dims {fmt:5s} 期待={wh} 実測={got} {'OK' if got == wh else '🔴NG'}")
        bad += got != wh
    # 1b. 先頭 HEAD_BYTES しか渡さなくても読めるか（本番と同じ経路）
    b = io.BytesIO()
    Image.new("RGB", (1920, 1251)).save(b, "JPEG", quality=95)
    got = dims_from_bytes(b.getvalue()[:HEAD_BYTES])
    print(f"  dims 先頭{HEAD_BYTES}バイトだけ 期待=(1920, 1251) 実測={got} "
          f"{'OK' if got == (1920, 1251) else '🔴NG'}")
    bad += got != (1920, 1251)

    # 2. 網：題名だけに当たること。**説明文に語があっても落ちる**のが正解
    items = [
        {"nasa_id": "a", "title": "Columbia debris in the hangar", "year": 2003, "desc_head": ""},
        {"nasa_id": "b", "title": "STS-107 crew portrait", "year": 2003, "desc_head": "debris"},
        {"nasa_id": "c", "title": "Columbia debris memorial service", "year": 2003, "desc_head": ""},
        {"nasa_id": "d", "title": "Columbia debris in the hangar", "year": 2005, "desc_head": ""},
    ]
    kept = [x["nasa_id"] for x in apply_net([dict(i) for i in items],
                                            must=["debris"], ng=["memorial"], year=2003, field="title")]
    print(f"  net  期待=['a'] 実測={kept} {'OK' if kept == ['a'] else '🔴NG'}")
    bad += kept != ["a"]
    # 2b. 網を外したら**増える**こと（＝網が本当に効いているかを値で見る）
    allk = [x["nasa_id"] for x in apply_net([dict(i) for i in items], [], [], None)]
    print(f"  net  網なし 期待=4件 実測={len(allk)}件 {'OK' if len(allk) == 4 else '🔴NG'}")
    bad += len(allk) != 4

    # 2c. 🔴 キャプションの取り出し：題名が資産IDのときだけ description を見る
    idrow = {"nasa_id": "e", "title": "KSC-03PD-0436", "year": 2003,
             "desc_head": "Columbia Reconstruction Project Team members study debris in the RLV Hangar."}
    caprow = {"nasa_id": "f", "title": "Columbia debris arrives at KSC", "year": 2003,
              "desc_head": "memorial service for the crew"}
    got = (caption(idrow)[:8], caption(caprow)[:8])
    print(f"  cap  期待=('Columbia', 'Columbia') 実測={got} "
          f"{'OK' if got == ('Columbia', 'Columbia') else '🔴NG'}")
    bad += got != ("Columbia", "Columbia")
    # 題名がキャプションの行は description を見ない＝NG 語 'memorial' で落ちない
    k2 = [x["nasa_id"] for x in apply_net([dict(idrow), dict(caprow)],
                                          must=["debris", "columbia"], ng=["memorial"], year=2003)]
    print(f"  cap  期待=['e', 'f'] 実測={k2} {'OK' if k2 == ['e', 'f'] else '🔴NG'}")
    bad += k2 != ["e", "f"]

    # 3. 壊れたバイト列では None（0 で埋めない＝fail closed）
    got = dims_from_bytes(b"\xff\xd8notajpegatall")
    print(f"  dims 壊れた入力 期待=None 実測={got} {'OK' if got is None else '🔴NG'}")
    bad += got is not None

    print("  →", "全部OK" if not bad else f"🔴 {bad}件NG")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search"); s.set_defaults(f=cmd_search)
    s.add_argument("--q", required=True); s.add_argument("--year", type=int)
    s.add_argument("--key", required=True); s.add_argument("--out", required=True)
    s.add_argument("--media-type", default="image"); s.add_argument("--max-pages", type=int, default=30)

    s = sub.add_parser("net"); s.set_defaults(f=cmd_net)
    s.add_argument("db"); s.add_argument("--net", required=True); s.add_argument("--key")
    s.add_argument("--field", choices=("caption", "title"), default="caption")

    s = sub.add_parser("dims"); s.set_defaults(f=cmd_dims)
    s.add_argument("db"); s.add_argument("--key", required=True); s.add_argument("--slot")
    s.add_argument("--limit", type=int, default=0); s.add_argument("--force", action="store_true")
    s.add_argument("--jobs", type=int, default=12)

    s = sub.add_parser("search-ia"); s.set_defaults(f=cmd_search_ia)
    s.add_argument("--q", required=True); s.add_argument("--key", required=True)
    s.add_argument("--out", required=True); s.add_argument("--max-pages", type=int, default=20)

    s = sub.add_parser("buckets"); s.set_defaults(f=cmd_buckets)
    s.add_argument("db"); s.add_argument("--key", required=True); s.add_argument("--slots", required=True)

    s = sub.add_parser("list"); s.set_defaults(f=cmd_list)
    s.add_argument("db"); s.add_argument("--key", required=True); s.add_argument("--min-w", type=int, default=0)
    s.add_argument("--chars", type=int, default=110); s.add_argument("--slot")

    s = sub.add_parser("selftest"); s.set_defaults(f=cmd_selftest)

    a = ap.parse_args()
    return a.f(a)


if __name__ == "__main__":
    raise SystemExit(main())
