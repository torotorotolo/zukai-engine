# -*- coding: utf-8 -*-
"""make_pages25.py — 25本目 ⑤b-4：出典の頁の原文を1ファイル（`=== p<N> ===` で頁を割る）にする＝`cuts.ss.REC_PAGES`。

■ なぜ（24本目 `ref/ep24/make_pages24.py` と同じ）
  ① の写し（git の外 `ref/ep25/src/txt/*.json`＝頁ごとの pdf・printed・norm）は資料ごとのファイル＝案C の部品の `rec=` が
  「資料 p頁」で原文に在るかを門番 check_illu ① が照らすため、1つの形へ並べ直す。
■ 頁の番号（通し＝`cuts/ss.py` の REC_DOCS の注と同じ。台本 §10 の頁の書き方）
  R1＝鉄道事故調査報告書 RA2007-3-1 本文＝**印刷の頁**（PDF−11・表紙と目次は 0 以下）＝台本の「R1 p.13」がそのまま p13
  R2〜R7＝同 別冊（付図）＝**k000＋PDF の頁**（R2＝2000＋・R3＝3000＋ … R7＝7000＋）＝台本の「R5 p.23」→ p5023
  S3＝神戸地裁の判決（2012年1月）＝**8000＋PDF の頁**（PDF＝印刷）＝「S3 p.7」→ p8007
  S1＝検証報告書（2011-04-15）＝**9000＋PDF の頁**（印刷＝PDF−8）／S1k＝付録「事故調査報告書に関する解説」＝**10000＋PDF の頁**（印刷＝PDF−2）
  S2＝最高裁の決定（2017-06-12）＝**11000＋PDF の頁**（PDF＝印刷）
  🆕 ⑤b-5（2026-10-26・図解）：K05＝建議（2005-09-06）＝**12000＋PDF の頁**／F1＝消防庁 第32報（2005-05-24）＝**13000＋PDF の頁**／
  HY1＝兵庫県の検証報告書（2006-01）＝**14000＋PDF の頁**（印刷＝PDF−2）／J1＝JR西日本「事故の概要」（`jrw/outline.html`・Shift_JIS）＝**p15001**／
  Kk＝国会会議録（`kokkai/kokkai_*.json` の発言を日ごとに1頁）＝2005-05-12＝**p16001**・2005-05-17＝**p16002**（日は KK_DAYS に足す）
  🆕 ⑤b-6（2026-10-26）：K07＝建議（2007-06-28）＝**17000＋PDF の頁**／国会の日 2013-11-13＝p16003・2023-03-08＝p16004・2023-06-13＝p16005・2011-02-21＝p16006／
  M1＝国交省の報道発表（2006-03-24・省令の改正）＝**p18001**／J5＝JR西日本「将来にわたる鉄道の安全の実現に向けて」＝**19000＋PDF の頁**
■ 使い方
    python ref/ep25/make_pages25.py      → ref/ep25/src/ep25_pages.txt（git の外＝手元だけ。Actions では門番を回さない）
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
TXT = HERE / "src" / "txt"
OUT = HERE / "src" / "ep25_pages.txt"
# (資料, 文字起こしの名, 足し分)。R1 だけ印刷の頁（足し分 −11＝PDF の頁から引く）
DOCS = (("R1", "RA07-3-1-1", -11),
        ("R2", "RA07-3-1-2", 2000), ("R3", "RA07-3-1-3", 3000), ("R4", "RA07-3-1-4", 4000),
        ("R5", "RA07-3-1-5", 5000), ("R6", "RA07-3-1-6", 6000), ("R7", "RA07-3-1-7", 7000),
        ("S3", "hanrei-pdf-82178", 8000), ("S1", "fu04-finalreport", 9000), ("S1k", "fu04-finalreport-annex-2-2", 10000),
        ("S2", "hanrei-pdf-86834", 11000),
        ("K05", "kengi_170906k", 12000), ("F1", "fdma_post364", 13000), ("HY1", "hyogo_kensho_000007823", 14000),
        ("K07", "kengi_190628k", 17000))
# 🆕 ⑤b-5：頁の無い資料（HTML・国会会議録の JSON）＝1頁にまとめる
J1_HTML = HERE / "src" / "jrw" / "outline.html"
KK_DIR = HERE / "src" / "kokkai"
# 🆕 ⑤b-6（2026-10-26・図解 第5〜10章）：国会の日を足した（16003〜16006）
KK_DAYS = {"2005-05-12": 16001, "2005-05-17": 16002, "2013-11-13": 16003, "2023-03-08": 16004, "2023-06-13": 16005, "2011-02-21": 16006}
# 🆕 ⑤b-6：M1＝国交省の報道発表（2006-03-24・省令の改正・cp932 の HTML）＝p18001／J5＝JR西日本「将来にわたる鉄道の安全の実現に向けて」（PDF）＝19000＋PDF の頁
M1_HTML = HERE / "src" / "gov" / "mlit_kisha_080324_.html"
J5_PDF = HERE / "src" / "jrw" / "shourainiwataru.pdf"


def _norm(s):
    return "".join(unicodedata.normalize("NFKC", s or "").split())


def _extra_pages():
    import re
    out = {}
    t = J1_HTML.read_bytes().decode("cp932")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    out[15001] = ("J1", _norm(re.sub(r"<[^>]+>", "", t)))
    seen = set()
    by_day = {d: [] for d in KK_DAYS}
    for f in sorted(KK_DIR.glob("kokkai_*.json")):
        o = json.loads(f.read_text(encoding="utf-8"))
        for r in (o if isinstance(o, list) else (o.get("speechRecord") or [])):
            if not isinstance(r, dict) or r.get("date") not in KK_DAYS:
                continue
            key = r.get("speechID") or (r.get("date"), r.get("speechOrder"), r.get("speech", "")[:40])
            if key in seen:            # 同じ発言が複数の検索の JSON に入っている
                continue
            seen.add(key)
            # 🆕 ⑤b-6：発言者の役職（speakerPosition）を頭に【】で＝図の札の役職（鉄道局長など）を原文で照らす
            pos = r.get("speakerPosition")
            by_day[r["date"]].append((int(r.get("speechOrder") or 0), (_norm(f"【{pos}】") if pos else "") + _norm(r.get("speech"))))
    for d, n in KK_DAYS.items():
        out[n] = ("Kk", "".join(t for _o, t in sorted(by_day[d])))
    h = M1_HTML.read_bytes().decode("cp932")
    h = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    out[18001] = ("M1", _norm(re.sub(r"<[^>]+>", "", h)))
    import fitz
    with fitz.open(J5_PDF) as doc:
        for i, pg in enumerate(doc, 1):
            out[19000 + i] = ("J5", _norm(pg.get_text()) or "（文字の層なし）")
    return out


def main():
    pages, n_of = {}, {}
    for name, stem, add in DOCS:
        for pg in json.loads((TXT / f"{stem}.json").read_text(encoding="utf-8")):
            n = add + int(pg["pdf"])
            if name == "R1" and pg.get("printed") is not None and int(pg["printed"]) != n:
                raise SystemExit(f"🔴 R1 の印刷の頁が PDF−11 でない：PDF {pg['pdf']} → 印刷 {pg['printed']}")
            if n in pages:
                raise SystemExit(f"🔴 頁の番号がぶつかった：{name} PDF {pg['pdf']} → p{n}")
            # 門番と照らし合わせで探しやすいように NFKC・空白なし（norm が無い頁は raw）
            pages[n] = "".join(unicodedata.normalize("NFKC", pg.get("norm") or pg.get("raw") or "").split())
            n_of[name] = n_of.get(name, 0) + 1
    for n, (name, text) in _extra_pages().items():
        if n in pages:
            raise SystemExit(f"🔴 頁の番号がぶつかった：{name} → p{n}")
        if not text:
            raise SystemExit(f"🔴 {name} p{n} の原文が空（ファイルか日付を確かめる）")
        pages[n] = text
        n_of[name] = n_of.get(name, 0) + 1
    with OUT.open("w", encoding="utf-8", newline="\n") as fo:
        for n in sorted(pages):
            fo.write(f"=== p{n} ===\n{pages[n]}\n")
    print("✓", OUT.name, "＝", "・".join(f"{k} {v}頁" for k, v in n_of.items()), f"（計 {len(pages)}頁）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
