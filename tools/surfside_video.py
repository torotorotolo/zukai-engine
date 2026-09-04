# -*- coding: utf-8 -*-
"""surfside_video.py — 4本目（サーフサイド）の記録映像を1本ずつ実測する（2026-09-04）。

■ なぜ要るか
    制作ルール §3「動画は写真より優先される」。②素材で動画の実寸を測らずに進むと、
    「NIST に B-Roll がある」だけで企画が通ってしまう。**尺と解像度と中身を数える。**

■ 何を数えるか
    NIST の Champlain Towers South ページに載っている動画（Kaltura 埋め込み）を全点：
      - entry_id / 題 / 説明 / ページ上のどの節にあるか
      - 🔴 **実寸**（幅・高さ・秒数・fps・ビットレート）＝ ffprobe で実測。ページの表記は信じない
      - ダウンロードできるか（Kaltura の playManifest が実ファイルを返すか）

■ なぜ figure 境界で切るか（2026-09-04 に踏んだ）
    `data-media-id` から固定長で前方を読むと、**次の figure の entry_id を拾って重複する**
    （NCST Insider の Ken Hover が Youssef Hashash と同じ id に見えた）。
    → `<figure ...> ... </figure>` の中だけを見る。

■ 使い方
    python tools/surfside_video.py list           # 一覧（ページから抽出するだけ）
    python tools/surfside_video.py probe          # ffprobe で全点実測（ネットワーク）
    python tools/surfside_video.py probe --only BRoll
    python tools/surfside_video.py selftest       # 道具の検算
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
OUT = HERE / "analytics" / "materials" / "surfside"
UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com)")
PAGE = ("https://www.nist.gov/disaster-and-failure-studies/"
        "champlain-towers-south-collapse/news-and-updates")
PARTNER = "684682"          # NIST の Kaltura パートナーID（ページの embed から）
SUBP = "68468200"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA})


# ---------------------------------------------------------------- 抽出
def fetch_page(cache=True) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / "news_and_updates.html"
    if cache and f.exists():
        return f.read_text(encoding="utf-8")
    r = SESSION.get(PAGE, timeout=60)
    r.raise_for_status()
    f.write_text(r.text, encoding="utf-8")
    return r.text


def _text(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ").strip()


def extract(h: str) -> list[dict]:
    """figure 単位で切ってから entry_id を探す（固定長で読むと隣の id を拾う）。"""
    secs = [(m.start(), m.group(1))
            for m in re.finditer(r'<a class="ck-anchor" id="([^"]+)"></a>', h)]

    def sec_of(pos: int) -> str:
        cur = "(top)"
        for p, name in secs:
            if p <= pos:
                cur = name
            else:
                break
        return cur

    out = []
    for m in re.finditer(r"<figure\b.*?</figure>", h, re.S):
        seg = m.group(0)
        if "nist-video" not in seg:
            continue
        eid = re.search(r"entry_id=(?:&amp;)?([0-9a-z_]+)", seg)
        # ⚠️ 2本だけ Kaltura でなく YouTube 埋め込み（Nikolaou / Hashash）。
        #    entry_id が無いのはバグではない。host を分けて記録する。
        yid = re.search(r"youtube\.com/embed/([A-Za-z0-9_-]{11})", seg)
        mid = re.search(r'data-media-id="(\d+)"', seg)
        ttl = re.search(r'video-embed-field-lazy-title">(.*?)</div>', seg, re.S)
        cap = re.search(r'nist-image__caption">(.*?)</figcaption>', seg, re.S)
        out.append(dict(
            media_id=mid.group(1) if mid else "",
            entry=eid.group(1) if eid else "",
            youtube=yid.group(1) if yid else "",
            host="kaltura" if eid else ("youtube" if yid else "?"),
            section=sec_of(m.start()),
            title=_text(ttl.group(1)) if ttl else "",
            caption=_text(cap.group(1)) if cap else "",
        ))
    return out


# ---------------------------------------------------------------- 実測
def manifest_url(entry: str, fmt: str = "download") -> str:
    return (f"https://cdnapisec.kaltura.com/p/{PARTNER}/sp/{SUBP}/playManifest"
            f"/entryId/{entry}/format/{fmt}/protocol/https/flavorParamId/0")


def resolve(entry: str) -> tuple[str, int]:
    """実ファイルの URL とバイト数。取れなければ ("",0)。"""
    for fmt in ("download", "url"):
        try:
            r = SESSION.get(manifest_url(entry, fmt), timeout=60,
                            allow_redirects=True, stream=True)
            ct = r.headers.get("Content-Type", "")
            n = int(r.headers.get("Content-Length") or 0)
            r.close()
            if r.status_code == 200 and ("video" in ct or "octet" in ct or n > 100000):
                return r.url, n
        except Exception:
            pass
    return "", 0


def ffprobe(url: str) -> dict:
    cmd = ["ffprobe", "-v", "error", "-user_agent", UA,
           "-print_format", "json", "-show_streams", "-show_format", url]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=180)
        if p.returncode != 0:
            return {"err": p.stderr.decode("utf-8", "replace")[:200]}
        d = json.loads(p.stdout.decode("utf-8", "replace"))
    except Exception as e:                       # noqa: BLE001
        return {"err": f"{type(e).__name__}: {e}"[:200]}
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), {})
    fps = 0.0
    if v.get("avg_frame_rate", "0/0") not in ("0/0", ""):
        num, _, den = v["avg_frame_rate"].partition("/")
        fps = round(float(num) / float(den or 1), 3)
    return {
        "w": v.get("width", 0), "h": v.get("height", 0),
        "vcodec": v.get("codec_name", ""), "fps": fps,
        "sec": round(float(d.get("format", {}).get("duration", 0) or 0), 1),
        "bitrate_kbps": round(int(d.get("format", {}).get("bit_rate", 0) or 0) / 1000),
        "acodec": a.get("codec_name", ""),
    }


def probe_youtube(vid: str) -> dict:
    """YouTube 側の2本。⚠️ 落とさずに**メタだけ**読む（-J はダウンロードしない）。"""
    try:
        p = subprocess.run(["yt-dlp", "-J", "--no-warnings", "--skip-download",
                            f"https://www.youtube.com/watch?v={vid}"],
                           capture_output=True, timeout=180)
        if p.returncode != 0:
            return {"err": p.stderr.decode("utf-8", "replace")[:200]}
        d = json.loads(p.stdout.decode("utf-8", "replace"))
    except Exception as e:                       # noqa: BLE001
        return {"err": f"{type(e).__name__}: {e}"[:200]}
    return {"w": d.get("width", 0), "h": d.get("height", 0),
            "sec": round(float(d.get("duration", 0) or 0), 1),
            "fps": d.get("fps", 0), "vcodec": d.get("vcodec", ""),
            "bitrate_kbps": round((d.get("tbr") or 0)),
            "file_url": f"https://www.youtube.com/watch?v={vid}"}


# ---------------------------------------------------------------- 検算
def selftest() -> int:
    bad = 0
    # ① figure 境界で切ると entry_id が重複しないこと
    rows = extract(fetch_page())
    ids = [r["entry"] for r in rows if r["entry"]]
    if len(ids) != len(set(ids)):
        dup = [i for i in set(ids) if ids.count(i) > 1]
        print(f"🔴 entry_id が重複: {dup}")
        bad += 1
    else:
        print(f"✅ entry_id は全点ユニーク（{len(ids)}件）")
    # ①b 🔴 「見ていない物」を疑う＝どこにも紐づかない figure が残っていないか
    orphan = [r["title"][:40] for r in rows if r["host"] == "?"]
    if orphan:
        print(f"🔴 entry_id も YouTube id も無い figure: {orphan}")
        bad += 1
    else:
        n_kal = sum(1 for r in rows if r["host"] == "kaltura")
        n_yt = sum(1 for r in rows if r["host"] == "youtube")
        print(f"✅ 全 figure が host を持つ（Kaltura {n_kal} / YouTube {n_yt}）")
    # ② 節の数が想定どおり（BRoll が 8 本）
    n_broll = sum(1 for r in rows if r["section"] == "BRoll")
    if n_broll != 8:
        print(f"🔴 B-Roll が 8 本でない: {n_broll}")
        bad += 1
    else:
        print("✅ B-Roll 8本")
    # ③ 空の題が無い
    empty = [r["media_id"] for r in rows if not r["title"]]
    if empty:
        print(f"🔴 題の取れない figure: {empty}")
        bad += 1
    else:
        print("✅ 題は全点取れている")
    # ④ ffprobe が動くこと（既知の1本で幅が正の整数になる）
    u, n = resolve("1_ju6nndhb")
    if not u:
        print("🔴 Kaltura から実ファイルの URL が取れない")
        bad += 1
    else:
        pr = ffprobe(u)
        if pr.get("w", 0) > 0 and pr.get("sec", 0) > 0:
            print(f"✅ ffprobe 実測できる（B-Roll#1 = {pr['w']}x{pr['h']} {pr['sec']}秒）")
        else:
            print(f"🔴 ffprobe が実寸を返さない: {pr}")
            bad += 1
    print(f"{'🔴 検算 NG' if bad else '✅ 検算 OK'}（{bad}件）")
    return bad


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "probe", "selftest"])
    ap.add_argument("--only", default="", help="節で絞る（BRoll / NCSTInsider / time-lapse ...）")
    ap.add_argument("--fresh", action="store_true", help="HTML を取り直す")
    a = ap.parse_args()

    if a.cmd == "selftest":
        return selftest()

    rows = extract(fetch_page(cache=not a.fresh))
    if a.only:
        rows = [r for r in rows if r["section"] == a.only]

    if a.cmd == "list":
        for r in rows:
            print(f"[{r['section']:<13}] {r['entry']:<12} {r['title'][:78]}")
        print(f"計 {len(rows)} 本")
        return 0

    for i, r in enumerate(rows, 1):
        if r["host"] == "youtube":
            r.update(probe_youtube(r["youtube"]))
        else:
            u, n = resolve(r["entry"])
            r["file_url"] = u
            r["bytes"] = n
            r.update(ffprobe(u) if u else {"err": "no url"})
        print(f"{i:>2}/{len(rows)} [{r['section']:<13}] {r.get('w',0)}x{r.get('h',0)} "
              f"{r.get('sec',0)}秒 {r.get('bitrate_kbps',0)}kbps  {r['title'][:52]}")
        time.sleep(0.6)

    OUT.mkdir(parents=True, exist_ok=True)
    f = OUT / ("videos.json" if not a.only else f"videos_{a.only}.json")
    f.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = [r for r in rows if r.get("w", 0) >= 1280]
    tot = sum(r.get("sec", 0) for r in rows)
    print(f"→ {f}")
    print(f"計 {len(rows)}本 / 1280px以上 {len(ok)}本 / 総尺 {tot/60:.1f}分")
    return 0


if __name__ == "__main__":
    sys.exit(main())
