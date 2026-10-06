# -*- coding: utf-8 -*-
"""ep19_assets.py — 19本目（サーフサイドのリメイク）の素材の取得（⑤b-1・2026-10-06）。決め⑧（了承ずみ・軽い道 約2GB）。

正本＝映像方針の取得の一覧 `ref/ep19/eizou_build/fetch19.tsv`（使う58点＋代わり6点）。ここは「落とす道」だけを持つ。
  python qa_out/ep19_assets.py scan            # NIST の記録映像・動く図の走査用の版（1080＝flavorParamId 487091）の大きさを HEAD で
  python qa_out/ep19_assets.py scan --yes      # 落とす → out/jiko/foot/ep19_scan/<記号>.mp4（git の外）
  python qa_out/ep19_assets.py photos          # 写真（NIST・Commons・DVIDS）の一覧と大きさ
  python qa_out/ep19_assets.py photos --yes    # 落とす → ref/ep19/photo/<file>（git の外）
落としかけを測らない＝ディスクから md5 を2回（記憶 feedback-download-size-is-not-completion）・Content-Length と照らす・
Commons は API の SHA-1 と照らす。記録＝各置き場の `fetched.json`。
⚠️ 元の画質（flavor 0＝4K）は丸ごと落とさない＝使う秒だけ `footage.fetch` が切り出す（決め⑧）。
⚠️ 名乗り（User-Agent）にメールや @ を入れない（記憶 feedback-no-email-in-tool-headers）。
"""
import csv
import hashlib
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
FETCH = HERE / "ref" / "ep19" / "eizou_build" / "fetch19.tsv"
SCAN = HERE / "out" / "jiko" / "foot" / "ep19_scan"
PHOTO = HERE / "ref" / "ep19" / "photo"
# ⚠️ 2026-10-06：連絡先（URL）の無い名乗りは Wikimedia が 429 で断り続けた（d06・2分待っても）＝18本目と同じ名乗り（リポの URL・@ なし）
UA = "zukai-engine/1.0 (accident-documentary research; https://github.com/torotorotolo/zukai-engine)"
KAL = "https://cdnapisec.kaltura.com/p/684682/sp/68468200/playManifest/entryId/{e}/format/url/protocol/https/flavorParamId/{p}"
SCAN_PARAM = 487091          # 1080 の版（2026-10-06 に HEAD で確かめた：B2 121.1MB・B1 118.6MB）
LOW_PARAM = 487041           # 無い版を頼むとこの版が返る＝大きさが同じなら「1080 の版は無い」


def rows():
    return list(csv.DictReader(FETCH.open(encoding="utf-8"), delimiter="\t"))


def _req(url, method="GET"):
    return urllib.request.Request(url, headers={"User-Agent": UA}, method=method)


def head_len(url):
    with urllib.request.urlopen(_req(url, "HEAD"), timeout=60) as r:
        return int(r.headers.get("Content-Length") or 0), r.geturl()


def get(url, timeout=120):
    with urllib.request.urlopen(_req(url), timeout=timeout) as r:
        return r.read()


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def download(url, dst, want=None, tries=4):
    """URL → dst（.part に書いてから名前を替える）。大きさを照らし、md5 を2回取る。"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    part = dst.with_suffix(dst.suffix + ".part")
    for k in range(tries):
        try:
            with urllib.request.urlopen(_req(url), timeout=120) as r, open(part, "wb") as f:
                n = 0
                for b in iter(lambda: r.read(1 << 20), b""):
                    f.write(b)
                    n += len(b)
            if want and n != want:
                raise IOError(f"大きさが違う {n} / {want}")
            part.replace(dst)
            m1 = md5(dst)
            time.sleep(0.5)
            m2 = md5(dst)
            if m1 != m2:
                raise IOError(f"md5 が2回で違う {m1} / {m2}")
            return n, m1
        except Exception as e:  # noqa: BLE001
            wait = 30 * (k + 1) if "429" in str(e) else 5 * (k + 1)
            print(f"  … {dst.name}: {e}（{wait}秒待って取り直す）")
            time.sleep(wait)
    raise SystemExit(f"🔴 {dst.name}: 取れなかった")


def probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(p)],
                         capture_output=True, text=True)
    d = json.loads(out.stdout or "{}")
    s = (d.get("streams") or [{}])[0]
    return dict(w=s.get("width"), h=s.get("height"), fps=s.get("r_frame_rate"),
                sec=round(float(d.get("format", {}).get("duration", 0)), 2))


# ── 記録映像・動く図（Kaltura）────────────────────────────────
def kal_rows():
    out = []
    for r in rows():
        m = re.search(r"entryId/([0-9a-z_]+)/", r["url"])
        if m and "kaltura" in r["url"]:
            out.append((r["code"], m.group(1), r))
    return out


def cmd_scan(yes):
    rec_p = SCAN / "fetched.json"
    rec = json.loads(rec_p.read_text(encoding="utf-8")) if rec_p.exists() else {}
    plan, tot = [], 0
    for code, e, r in kal_rows():
        n, _ = head_len(KAL.format(e=e, p=SCAN_PARAM))
        lo, _ = head_len(KAL.format(e=e, p=LOW_PARAM))
        p = SCAN_PARAM if n != lo else 0           # 1080 の版が無い（低い版が返る）＝元の画質（小さい物だけ）
        if p == 0:
            n, _ = head_len(KAL.format(e=e, p=0))
        plan.append((code, e, p, n))
        tot += n
        print(f"{code:4} {e}  版 {p or '0（元の画質）'}  {n / 1e6:7.1f}MB  元の表 {r['dims']} {r['mb']}MB")
    print(f"計 {tot / 1e6:.1f}MB・{len(plan)}本")
    if not yes:
        print("（落としていない＝ --yes）")
        return 0
    for code, e, p, n in plan:
        dst = SCAN / f"{code}.mp4"
        if dst.exists() and rec.get(code, {}).get("size") == n and md5(dst) == rec[code].get("md5"):
            print(f"= {code} 済み")
            continue
        size, m = download(KAL.format(e=e, p=p), dst, want=n)
        info = probe(dst)
        rec[code] = dict(entry=e, param=p, size=size, md5=m, fetched=time.strftime("%Y-%m-%d"), **info)
        rec_p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ {code} {size / 1e6:.1f}MB md5 {m} {info}")
    return 0


# ── 写真（NIST・Commons・DVIDS）──────────────────────────────
def commons_info(titles):
    out = {}
    for i in range(0, len(titles), 40):
        q = urllib.parse.urlencode(dict(action="query", format="json", prop="imageinfo", iiprop="size|sha1|url",
                                        titles="|".join(titles[i:i + 40])))
        d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))
        for pg in d["query"]["pages"].values():
            ii = pg["imageinfo"][0]
            out[pg["title"]] = dict(size=ii["size"], w=ii["width"], h=ii["height"], sha1=ii["sha1"], url=ii["url"])
    return out


def dhs_titles():
    """DHS の15点（決め⑥）。⚠️ 一覧の「Category:Surfside condominium building collapse」には入っていない（2026-10-06 に
    分類の13点を見て0件）＝題で検索する。番号の順（d01〜d15）は題の並び＝Flickr の番号の順。"""
    q = urllib.parse.urlencode(dict(action="query", format="json", list="search", srnamespace="6", srlimit="50",
                                    srsearch='intitle:"Mayorkas Visits Surfside"'))
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))
    ts = sorted(m["title"] for m in d["query"]["search"]
                if m["title"].startswith("File:DHS Secretary Alejandro Mayorkas Visits Surfside"))
    if len(ts) != 15:
        raise SystemExit(f"🔴 DHS の写真が15点でない: {len(ts)}")
    return ts


def dvids_url(page):
    t = get(page).decode("utf-8", "replace")
    cands = set(re.findall(r"https://d1ldvf68ux039x\.cloudfront\.net/thumbs/photos/\d+/\d+/[0-9a-z_]+\.jpg", t))
    # いちばん大きい配信（2000w > 1000w …）を選ぶ
    def wid(u):
        m = re.search(r"/(\d+)w_q\d+\.jpg$", u)
        return int(m.group(1)) if m else 0
    if not cands:
        raise SystemExit(f"🔴 DVIDS の頁に画像の URL が無い: {page}")
    best = max(cands, key=wid)
    who = re.search(r"Photo by ([^<|]+?)(?:<|\|| - )", html.unescape(t))
    return best, (who.group(1).strip() if who else "")


def photo_plan():
    plan = []                   # (code, file, kind, url, extra)
    com = []
    for r in rows():
        if r["class"] != "photo":
            continue
        u, f = r["url"], r["file"]
        if "nist.gov" in u:
            plan.append((r["code"], f, "nist", u, {}))
        elif "dvidshub" in u:
            plan.append((r["code"], f, "dvids", u, {}))
        elif "commons.wikimedia.org/wiki/File:" in u:
            t = "File:" + urllib.parse.unquote(u.split("/wiki/File:")[1]).replace("_", " ")
            plan.append((r["code"], f, "commons", t, {}))
            com.append(t)
        elif r["code"] == "D":
            for i, t in enumerate(dhs_titles(), 1):
                plan.append((f"D{i:02d}", f"d{i:02d}_dhs.jpg", "commons", t, {}))
                com.append(t)
        else:
            print(f"⚠️ {r['code']}: 取り先が分からない {u[:80]}")
    info = commons_info(com) if com else {}
    return plan, info


def cmd_photos(yes):
    plan, info = photo_plan()
    rec_p = PHOTO / "fetched.json"
    rec = json.loads(rec_p.read_text(encoding="utf-8")) if rec_p.exists() else {}
    tot = 0
    resolved = []
    for code, f, kind, u, _ in plan:
        if kind == "commons":
            ii = info.get(u)
            if not ii:
                raise SystemExit(f"🔴 Commons に無い: {u}")
            resolved.append((code, f, kind, ii["url"], dict(page=u, sha1=ii["sha1"], want=ii["size"], dims=f"{ii['w']}x{ii['h']}")))
            n = ii["size"]
        elif kind == "dvids":
            img, who = dvids_url(u)
            n, _ = head_len(img)
            resolved.append((code, f, kind, img, dict(page=u, want=n, photographer=who)))
        else:
            n, _ = head_len(u)
            resolved.append((code, f, kind, u, dict(page=u, want=n)))
        tot += n
        print(f"{code:10} {kind:7} {n / 1e6:6.2f}MB  {f}")
    print(f"計 {tot / 1e6:.1f}MB・{len(resolved)}点")
    if not yes:
        print("（落としていない＝ --yes）")
        return 0
    for code, f, kind, url, ex in resolved:
        dst = PHOTO / f
        if dst.exists() and rec.get(code, {}).get("md5") == md5(dst) and rec[code].get("size") == ex["want"]:
            print(f"= {code} 済み")
            continue
        size, m = download(url, dst, want=ex["want"])
        if kind == "commons":
            s1 = hashlib.sha1(dst.read_bytes()).hexdigest()
            if s1 != ex["sha1"]:
                raise SystemExit(f"🔴 {code}: SHA-1 が Commons と違う")
        rec[code] = dict(file=f, kind=kind, url=url, size=size, md5=m, fetched=time.strftime("%Y-%m-%d"),
                         **{k: v for k, v in ex.items() if k != "want"})
        rec_p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ {code} {f} {size / 1e6:.2f}MB md5 {m}")
        # ⚠️ 2026-10-06：Commons は続けて取ると 429（Too many requests）で断る（d03〜d06 で踏んだ）＝1点ごとに5秒空ける
        time.sleep(5.0 if kind == "commons" else 0.5)
    return 0


# ── フリー素材の共通の棚 ref/stock/（設計＝ref/ep19/stock_shelf_design.md）─────────────
# 頁の情報＝2026-10-06 に内蔵ブラウザで各頁の VideoObject（JSON-LD：contentUrl・license・uploadDate・duration・寸法）と
# 作者の欄（a[href^="/@"]）から読んだ。Pixabay は頁の HTML に AI の印（isAiGenerated・AI generated）が0件＝2020年10月の投稿。
# Pexels は規約で生成AIの投稿を認めない（18本目 ⑤b-7b と同じ判断）。動画は git に入れない（`ref/*`）＝台帳 stock.json だけ名指しで commit
STOCK = HERE / "ref" / "stock"
LIC = {"Pexels": ("Pexels License", "https://www.pexels.com/license/"),
       "Pixabay": ("Pixabay Content License", "https://pixabay.com/service/license-summary/")}


def _s(code, site, page, media, author, posted, sec, w, h, what, cuts):
    return dict(code=code, site=site, page=page, media=media, author=author, posted=posted, sec=sec, w=w, h=h, what=what, cuts=cuts)


STOCK19 = {
    "px_15204737": _s("S#1", "Pexels", "https://www.pexels.com/video/white-concrete-buildings-near-the-beach-15204737/",
                      "https://videos.pexels.com/video-files/15204737/15204737-hd_1920_1080_30fps.mp4", "CAPTKHO kho",
                      "2023-01-19", 31, 1920, 1080, "浜辺の白いコンクリートの建物（空撮）", ["cc14"]),
    "px_9431778": _s("S#4", "Pexels", "https://www.pexels.com/video/aerial-footage-of-buildings-near-a-shore-9431778/",
                     "https://videos.pexels.com/video-files/9431778/9431778-uhd_2560_1440_24fps.mp4", "Mikhail Nilov",
                     "2021-09-03", 12, 2688, 1512, "海岸の建物の空撮", ["cc13"]),
    "px_11287848": _s("S#6", "Pexels", "https://www.pexels.com/video/water-with-waves-11287848/",
                      "https://videos.pexels.com/video-files/11287848/11287848-uhd_2560_1440_24fps.mp4", "Şaban Karabeli",
                      "2022-02-24", 30, 3840, 2160, "波のある水面", ["c526"]),
    "px_7830155": _s("S#8", "Pexels", "https://www.pexels.com/video/a-crack-on-the-wall-7830155/",
                     "https://videos.pexels.com/video-files/7830155/7830155-uhd_2560_1440_30fps.mp4", "Monstera Production",
                     "2021-05-08", 28, 3840, 2160, "壁のひび", ["c411"]),
    "px_7829491": _s("S#9", "Pexels", "https://www.pexels.com/video/close-up-video-of-a-rusty-metal-7829491/",
                     "https://videos.pexels.com/video-files/7829491/7829491-uhd_2560_1440_30fps.mp4", "Monstera Production",
                     "2021-05-08", 30, 3840, 2160, "錆びた金属の寄り", ["c308"]),
    "px_5571839": _s("S#11", "Pexels", "https://www.pexels.com/video/water-dripping-on-welded-metal-pipes-5571839/",
                     "https://videos.pexels.com/video-files/5571839/5571839-hd_1920_1080_24fps.mp4", "Monsieur Sylvain",
                     "2020-10-10", 10, 1920, 1080, "溶接した金属の管に落ちる水", ["c519"]),
    "px_29880216": _s("S#12", "Pexels", "https://www.pexels.com/video/water-cascading-over-weathered-concrete-edge-29880216/",
                      "https://videos.pexels.com/video-files/29880216/12828546_2560_1440_30fps.mp4", "Aamir Somewhere",
                      "2024-12-21", 30, 3840, 2160, "古びたコンクリートの縁を流れ落ちる水", ["c510"]),
    "px_8478951": _s("S#16", "Pexels", "https://www.pexels.com/video/a-person-working-with-paperworks-8478951/",
                     "https://videos.pexels.com/video-files/8478951/8478951-uhd_2560_1440_25fps.mp4", "ArtHouse Studio",
                     "2021-06-25", 11, 3840, 2160, "書類の仕事（手元）", ["c405"]),
    "px_6028858": _s("S#20", "Pexels", "https://www.pexels.com/video/empty-parking-lot-6028858/",
                     "https://videos.pexels.com/video-files/6028858/6028858-hd_1920_1080_25fps.mp4", "Артем Ковальчук",
                     "2020-11-30", 13, 1920, 1080, "空の地下駐車場", ["c315"]),
    "pb_52888": _s("S#38", "Pixabay", "https://pixabay.com/videos/construction-cranes-foundation-52888/",
                   "https://cdn.pixabay.com/video/2020/10/19/52888-471156118_large.mp4", "LadislavBur",
                   "2020-10-22", 32, 2720, 1530, "建設のクレーンと基礎", ["cb02"]),
    "px_9431584": _s("S#27", "Pexels", "https://www.pexels.com/video/an-apartment-building-at-night-9431584/",
                     "https://videos.pexels.com/video-files/9431584/9431584-hd_1920_1080_25fps.mp4",
                     "mohammad hassan tabatabaei jafari", "2021-09-03", 11, 1920, 1080, "夜の集合住宅（代わり）", []),
}


def _ep18_shelf():
    """18本目の11本（ref/ep18/stock.json）を棚の鍵に直す（ref/ep18/ の中身は書き換えない＝読むだけ）。"""
    src = HERE / "ref" / "ep18" / "stock.json"
    d = json.loads(src.read_text(encoding="utf-8"))
    out = {}
    for k, r in d.items():
        n = re.search(r"(\d+)$", k).group(1)
        key = ("px_" if r["site"] == "Pexels" else "pb_") + n
        out[key] = (k, r)
    return out


def cmd_stock(yes):
    STOCK.mkdir(parents=True, exist_ok=True)
    shelf_p = STOCK / "stock.json"
    shelf = json.loads(shelf_p.read_text(encoding="utf-8")) if shelf_p.exists() else {}
    tot = 0
    for key, s in STOCK19.items():
        n, _ = head_len(s["media"])
        tot += n
        print(f"{key:13} {s['code']:5} {n / 1e6:6.1f}MB  {s['what']}")
    print(f"19本目 計 {tot / 1e6:.1f}MB・{len(STOCK19)}本／18本目から移す {len(_ep18_shelf())}本（手元の複写）")
    if not yes:
        print("（落としていない＝ --yes）")
        return 0
    today = time.strftime("%Y-%m-%d")
    for key, s in STOCK19.items():
        dst = STOCK / "media" / f"{key}.mp4"
        n, _ = head_len(s["media"])
        if dst.exists() and shelf.get(key, {}).get("md5") == md5(dst):
            print(f"= {key} 済み")
        else:
            size, m = download(s["media"], dst, want=n)
            info = probe(dst)
            lic, lic_url = LIC[s["site"]]
            r = shelf.get(key, {})
            r.update(site=s["site"], page=s["page"], media=s["media"], rendition=f"{info['w']}x{info['h']}", md5=m, size=size,
                     w=info["w"], h=info["h"], fps=info["fps"], sec=info["sec"], title=s["what"], author=s["author"],
                     posted=s["posted"], license=lic, license_url=lic_url, license_checked=today,
                     ai=("頁に AI の印なし（Pixabay の頁の HTML を検索・2020年の投稿）" if s["site"] == "Pixabay"
                         else "Pexels は規約で生成AIの投稿を認めない（頁に AI の記載なし）"),
                     what=s["what"], place="", era_note="", ok_ranges=r.get("ok_ranges", []), ng_ranges=r.get("ng_ranges", []),
                     used_in=r.get("used_in", []), claims=r.get("claims", []),
                     credit=f"イメージ（フリー素材）：{s['site']}／{s['author']}", fetched=today, code19=s["code"])
            ui = [u for u in r["used_in"] if u.get("ep") != 19] + [dict(ep=19, cid=c, role="本体（⑤b-1 で区間を選ぶ）") for c in s["cuts"]]
            r["used_in"] = ui
            shelf[key] = r
            print(f"✓ {key} {size / 1e6:.1f}MB md5 {m} {info}")
        shelf_p.write_text(json.dumps(shelf, ensure_ascii=False, indent=1), encoding="utf-8")
    for key, (old, r) in _ep18_shelf().items():
        srcf = HERE / "ref" / "ep18" / r["file"]
        dst = STOCK / "media" / f"{key}.mp4"
        if not (dst.exists() and md5(dst) == r["md5"]):
            dst.write_bytes(srcf.read_bytes())
        m1, m2 = md5(dst), md5(dst)
        if not (m1 == m2 == r["md5"]):
            raise SystemExit(f"🔴 {key}: 18本目の md5 と違う")
        e = shelf.get(key, {})
        e.update(site=r["site"], page=r["page"], media=r["url"], rendition=f"{r['w']}x{r['h']}", md5=r["md5"], size=r["size"],
                 w=r["w"], h=r["h"], fps=r["fps"], sec=r["dur"], title=r["what"], author=r["author"], posted=r["up"],
                 license=r["license"], license_url=r["license_url"], license_checked=r["fetched"],
                 ai=e.get("ai", "18本目 ⑤b-7b で確かめた（Pexels 規約・Pixabay の印なし）"), what=r["what"], place="", era_note="",
                 ok_ranges=e.get("ok_ranges", []), ng_ranges=e.get("ng_ranges", []), claims=e.get("claims", []),
                 used_in=[dict(ep=18, cid=r["cut"], role="頭の差し込み（⑤b-7c）", key18=old)], credit=r["credit"],
                 fetched=r["fetched"])
        shelf[key] = e
        print(f"✓ {key} ← 18本目 {old}（md5 一致）")
    shelf_p.write_text(json.dumps(shelf, ensure_ascii=False, indent=1), encoding="utf-8")
    mb = sum(f.stat().st_size for f in (STOCK / "media").glob("*.mp4")) / 1e6
    print(f"棚 {len(shelf)}本・media の計 {mb:.1f}MB")
    return 0


LIST = HERE / "ref" / "ep19" / "eizou_build" / "list19.tsv"
SOURCES = HERE / "ref" / "ep19" / "eizou_build" / "sources19.tsv"
STOCK = HERE / "ref" / "stock" / "stock.json"
CLIPS = HERE / "ref" / "ep19" / "clips.json"
SHOTS = HERE / "ref" / "ep19" / "shots.json"
FOOTAGE = HERE / "tools" / "footage.py"
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（12本目の教訓＝footage.py の注）


def _list():
    return [r for r in csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t")]


def _sources():
    out = {}
    for ln in SOURCES.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if len(f) >= 9 and not ln.startswith("#") and f[0] != "code":
            out[f[0]] = f
    return out


def _stock_by_code():
    return {v["code19"]: (k, v) for k, v in json.loads(STOCK.read_text(encoding="utf-8")).items() if v.get("code19")}


def _rng(s):
    m = re.fullmatch(r"\s*([0-9.]+)\s*[–-]\s*([0-9.]+)\s*", s or "")
    return (float(m.group(1)), float(m.group(2))) if m else None


def _uses():
    """(cid, 記号, a, b, 要る秒, head) を出す。本体＝尺−差し込みの秒・頭の差し込み＝k 行ぶん。
    要る秒は門番（make_list19）の計算をそのまま使う（2か所に書くとずれる＝10-06 に c106 が 4.8秒と 14.5秒で食い違った）"""
    sys.path.insert(0, str(LIST.parent))
    import make_list19 as ML
    rows, _ = ML.build(ML.parse_daihon(ML.DAIHON), ML.read_tsv(ML.ASSIGN))
    out, stk = [], _stock_by_code()
    for u in ML.uses_of(rows):
        if ML.class_of(u["code"]) not in ("film", "anim", "stock"):
            continue
        if u["role"] == "tail":
            print(f"⚠️ {u['cid']} 尻の映像の差し込み {u['code']}@{u['rng']}：USE は1カット1欄＝⑤b-7 で差し込みの層として作る（ここには書かない）")
            continue
        ab = _rng(u["rng"])
        if ab is None and u["code"] in stk:
            # フリー素材の区間は一覧でなく棚（stock.json）にある＝used_in の「a〜b秒」→ 無ければ ok_ranges の頭から要る秒ぶん
            v = stk[u["code"]][1]
            for x in v.get("used_in", []):
                m = re.search(r"([0-9.]+)\s*〜\s*([0-9.]+)\s*秒", x.get("role", "")) if x.get("cid") == u["cid"] else None
                if m:
                    ab = (float(m.group(1)), float(m.group(2)))
            if ab is None and v.get("ok_ranges"):
                r0 = v["ok_ranges"][0]                               # 棚の ok_ranges は {from, to, …}
                a0, b0 = float(r0["from"]), float(r0["to"])
                ab = (a0, min(b0, a0 + u["secs"]))
        if ab is None:
            print(f"⚠️ {u['cid']} {u['code']}：区間が決まっていない＝USE に書けない")
            continue
        out.append((u["cid"], u["code"], *ab, _need(u["cid"], u["role"], float(u["secs"])), u["role"] == "head"))
    return out


_INS = None


def _need(cid, role, est):
    """要る秒＝**焼く尺**（10-06 ⑤b-2：scene_jiko が19本目になった＝list19 の見込み〈÷365〉から取り直した。前後の間 0.35＋0.5 秒と
    扉の分で見込みより長い＝c106 が 8.3秒はみ出した）。本体＝`footage.secs_of` と同じ式（尺−扉）。差し込みは scene_jiko の入れ替えの式
    （`ins_sec`＋`INTRO_X`）：頭＝list19 の ins_k 行ぶん（`ss.head(until=k)`）／尻のあるカットの本体＝尻が入る行（ins_k 行目＝`at=k−1`）まで"""
    global _INS
    sys.path.insert(0, str(HERE / "tools"))
    import scene_jiko as SJ
    if _INS is None:
        _INS = {r["cid"]: (r["ins_pos"], int(r["ins_k"])) for r in _list() if r.get("ins_pos") and r.get("ins_k")}
    secs = dict(SJ.CUTS)
    if cid not in secs:
        print(f"⚠️ {cid}：scene_jiko の尺に無い＝見込みの {est:.2f}秒で書く")
        return est
    pos, k = _INS.get(cid, (None, 0))
    if role == "head":
        return round(SJ.ins_sec(cid, k) + SJ.INTRO_X, 3)
    if pos == "tail":
        return round(SJ.ins_sec(cid, k - 1) + SJ.INTRO_X, 3)
    return round(secs[cid] - SJ.card_of(cid), 3)


def cmd_clips():
    """ref/ep19/clips.json（footage.CLIPS）＝NIST の記録映像・動く図（Kaltura の元の版を区間読み）＋フリー素材（棚の実測）。
    stock の鍵は棚の鍵（px_<id>）＝footage の門番 check_text_screens・check_cuts が 20% の数と別に数える（"stock": true）"""
    src, stk = _sources(), _stock_by_code()
    fetched = json.loads((SCAN / "fetched.json").read_text(encoding="utf-8"))
    used = {c for _, c, *_ in _uses()}
    out = {}
    for code in sorted(used):
        if code in stk:
            k, v = stk[code]
            fn, _, fd = str(v["fps"]).partition("/")            # 棚の fps は「24/1」と「29.97」の2通りの書き方がある
            v = dict(v, fps=float(fn) / float(fd or 1))
            out[k] = dict(url=v["page"], media=v["media"], stock=True, file=f"stock/media/{k}.mp4", credit=v["credit"], src="stock",
                          at=0.0, date=v.get("posted") or None, what=v.get("what") or v.get("title"), w=v["w"], h=v["h"],
                          fps=float(v["fps"]), sar="1:1", sec=v["sec"], size=v["size"], md5=v["md5"], dispw=v["w"],
                          decoded=[v["w"], v["h"]], license=v["license"], license_url=v["license_url"], author=v["author"],
                          site=v["site"], code19=code)
            continue
        f = src[code]
        w, h = (int(x) for x in f[4].split("x"))
        fe = fetched.get(code, {})
        num, den = (int(x) for x in str(fe.get("fps", "30/1")).split("/"))
        out[code] = dict(url=f"https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse/news-and-updates",
                         media=f[3], range=True, credit=f[8], src="nist", at=0.0, date=None, what=f[9][:80], w=w, h=h,
                         fps=round(num / den, 3), sar="1:1", sec=float(f[5]), size=int(float(f[6]) * 1e6), dispw=w, decoded=[w, h],
                         rights=f[7], scan=f"out/jiko/foot/ep19_scan/{code}.mp4")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {CLIPS.relative_to(HERE).as_posix()}（{len(out)}本：" + " ".join(out) + "）")
    # フリー素材のショット表＝footage.unknown_clip が止めないように shots.json に足す（1秒1コマの境目・tools/shots.py）
    sys.path.insert(0, str(HERE / "tools"))
    import shots as SH
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    for k, v in out.items():
        if v.get("stock") and k not in sd:
            sh, dur = SH.shots_of(HERE / "ref" / "stock" / "media" / f"{k}.mp4")
            sd[k] = dict(src=v["media"], scan=f"ref/stock/media/{k}.mp4", dur=round(dur, 1),
                         how="1秒1コマを tools/shots.boundaries（2026-10-06 ⑤b-1・フリー素材）", shots=sh)
            print(f"  shots.json + {k}（{len(sh)} ショット）")
    SHOTS.write_text(json.dumps(sd, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


# 🔴 1秒刻みの境目の物差し（tools/shots.boundaries）が実際の切り替わりとずれる所＝直す（秒・根拠と目で確かめた事）。
#    move＝境目を実測の秒へ動かす（0.1秒刻みで見た）／join＝境目でない（同じ絵が続く）のでつなぐ
SHOT_FIX = {
    "B7": {"move": {46.0: (46.4, "c106：錆びた鉄筋の標本は 46.4秒で切り替わる（0.1秒刻みで実測・10-06 ⑤b-1）")}},
    "TFV": {"move": {3525.0: (3525.3, "ca15：スライド134 は 3525.3秒で次のスライド（0.1秒刻みで実測・10-06 ⑤b-1）")}},
    "B2": {"move": {11.0: (11.2, "c101：海岸線の空撮は 7.1〜11.2秒の1本（0.1秒刻みで実測・10-06 ⑤b-1）"),
                    104.0: (99.0, "c406：99.0秒で空撮に切り替わり 109秒まで切れ目なし（fine 98〜109＝99.0秒だけ 43.9・ほかは 5.3 以下・10-06 ⑤b-2）")},
           "split": {110.0: "c104：現場の引きの空撮は 110.0秒で切り替わる（⑤b-1 の 0.1秒刻みの実測・assign19 の c104）",
                     113.5: "c104：113.5秒から表題のカード（⑤b-1 の実測・assign19 の c104）"}},
    "B1": {"move": {55.0: (53.4, "c705：がれきの山の寄りは 53.4〜57.3秒の1本（fine 49〜67・1秒刻み B1_sec_050.50 を目で見た・10-06 ⑤b-2）")},
           "split": {57.3: "c705：がれきの山の寄りは 57.3秒で次のショット（fine 53〜67＝55.4・10-06 ⑤b-2）"}},
    "B5": {"join": {105.0: "c912：倉庫の部材のあいだは 100〜109.2秒の1本・104〜105秒はカメラが右へ振れただけ（1秒刻み B5_sec_102.00 を目で見た・10-06 ⑤b-2）"}},
    "px_8060076": {"join": {8.0: "S#46：0〜12秒はドローンが浜の上を引いていく1本（1秒1コマ stk_46_000・006 を目で見た・10-06）"}},
    "px_39933092": {"join": {2.0: "S#49：2〜3秒は黄色い筒が上から入ってくる動き＝同じ寄りの続き（1秒1コマ stk_49_000 を目で見た・10-06）"}},
}


def cmd_shotfix():
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    for key, fx in SHOT_FIX.items():
        sh = sd[key]["shots"]
        for old, (new, why) in fx.get("move", {}).items():
            for i, s in enumerate(sh[:-1]):
                if abs(s["until"] - old) < 1e-6:
                    s["until"] = sh[i + 1]["start"] = new
                    sh[i + 1]["fixed"] = s["fixed"] = why
                    print(f"{key} 境目 {old} → {new}")
        for t, why in fx.get("join", {}).items():
            for i, s in enumerate(sh[:-1]):
                if abs(s["until"] - t) < 1e-6:
                    s["until"] = sh[i + 1]["until"]
                    s["motion"] = max(s["motion"], sh[i + 1]["motion"])
                    s["fixed"] = why
                    del sh[i + 1]
                    print(f"{key} 境目 {t} をつないだ")
                    break
        for t, why in fx.get("split", {}).items():
            for i, s in enumerate(sh):
                if s["start"] + 1e-6 < t < s["until"] - 1e-6:
                    sh.insert(i + 1, {"start": t, "until": s["until"], "motion": s["motion"], "fixed": why})
                    s["until"], s["fixed"] = t, why
                    print(f"{key} {t} で割った")
                    break
    SHOTS.write_text(json.dumps(sd, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


def cmd_use():
    """footage.USE の19本目の欄を list19 から書き出す。rate＝使える秒÷要る秒（切り捨て・1.0まで）・0.6未満は止め絵。
    ⚠️ 要る秒は list19 の尺（⑤b-2 で scene_jiko が19本目になったら `footage.py --check` の尺で取り直す）"""
    stk = _stock_by_code()
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    lines, warn = [], []
    for cid, code, a, b, need, head in _uses():
        key = stk[code][0] if code in stk else code
        avail = b - a
        rate = min(1.0, int(avail / need * 100) / 100)
        sh = [s for s in sd.get(key, {}).get("shots", []) if s["start"] <= a < s["until"]]
        where = f"#{sd[key]['shots'].index(sh[0])}（{sh[0]['start']:.0f}〜{sh[0]['until']:.0f}秒）" if sh else "ショット表の外"
        if sh and 0 < b - sh[0]["until"] <= 0.2:
            b = sh[0]["until"]                    # 0.2秒以内のはみ出し＝区間の書き方の丸め（素材の尻・1秒刻みの境目）＝ショットの終わりに合わせる
            avail = b - a
            rate = min(1.0, int(avail / need * 100) / 100)
        if sh and b > sh[0]["until"]:
            warn.append(f"{cid} {key}@{a}–{b} がショット {where} の外へ出る")
        # 止め絵は区間の**真ん中のコマ**（10-06 ⑤b-2：区間の頭は手持ちのぶれ・ピント送りの途中のことがある＝c102 の33秒台）
        #   cb01＝B2@12–14 → 13.0秒（⑤b-1 で決めたコマ ss_b2_87park と同じ）
        s0 = round((a + b) / 2, 2) if rate < STILL_BELOW else a
        opt = (f", still=True, until={min(b, s0 + 1.0):.2f}" if rate < STILL_BELOW else f", until={b:.2f}, rate={rate}")
        opt += ", head=True" if head else ""
        lines.append(f'    "{cid}": dict(clip="{key}", start={s0:.2f}{opt}),   # {where}・使える {avail:.2f}秒（{a:g}〜{b:g}）／要る {need:.2f}秒')
    txt = FOOTAGE.read_text(encoding="utf-8")
    m = re.search(r"(    # EP19_USE>>> ここから[^\n]*\n)(.*?)(    # EP19_USE>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit("🔴 footage.py に EP19_USE の目印が無い")
    FOOTAGE.write_text(txt[:m.start(2)] + "\n".join(lines) + "\n" + txt[m.end(2):], encoding="utf-8")
    print(f"→ tools/footage.py USE {len(lines)}欄（止め絵 {sum('still=True' in x for x in lines)}・頭の差し込み {sum('head=True' in x for x in lines)}）")
    for w in warn:
        print("⚠️", w)
    return 0


# 写真の束（`ref/ep19/<名>.jpg`＋台帳 `ref/ep19/assets.json`）。18本目の `ep18_assets.py build` の型。
#   🔴 19本目は冒頭が実写＝映像のカット（`ss.vid`）を書いた時点で合成と門番が台帳を読む（`ss.frame_only_for`）＝⑤b-2 で作る。
#   切り抜き CROP（元の画素の箱）は ⑤b-7a で写真ごとに決める（いまは決まっているものだけ）。束に入れるのは list19 で当てた写真だけ
CROP = {
    "D13": (1500, 0, 2500, 562),     # cc06：海沿いの高い建物＝上の右（assign19・⑤b-1）
}
MAXW = 3000
LIC = {"A": "Public domain", "A（FEMA）": "Public domain", "A（DHS）": "Public domain",
       "PD-FLGov の可能性": "Public domain", "CC BY 2.0": "CC BY 2.0", "CC BY 3.0": "CC BY 3.0"}


def cmd_build(only=None):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    sys.path.insert(0, str(LIST.parent))
    import make_list19 as ML
    rows, _ = ML.build(ML.parse_daihon(ML.DAIHON), ML.read_tsv(ML.ASSIGN))
    cuts = {}
    for u in ML.uses_of(rows):
        if ML.class_of(u["code"]) == "photo":
            cuts.setdefault(u["code"], []).append(u["cid"])
    src, fetched = _sources(), json.loads((PHOTO / "fetched.json").read_text(encoding="utf-8"))
    db_path = HERE / "ref" / "ep19" / "assets.json"
    db = json.loads(db_path.read_text(encoding="utf-8")) if db_path.exists() else {}
    bad = 0
    for code in sorted(cuts):
        if only and code not in only:
            continue
        f = src.get(code)
        fe = fetched.get(code)
        if not f or not fe:
            print(f"🔴 {code}: sources19 か fetched.json に行が無い")
            bad += 1
            continue
        lic = LIC.get(f[7].strip())
        if not lic:
            print(f"🔴 {code}: 権利「{f[7]}」を台帳の言い方に直せない（LIC に足す）")
            bad += 1
            continue
        sp = PHOTO / fe["file"]
        if fe.get("sha1") and hashlib.sha1(sp.read_bytes()).hexdigest() != fe["sha1"]:
            print(f"🔴 {code}: {sp.name} の SHA-1 が取得のときと違う（取り直す）")
            bad += 1
            continue
        with Image.open(sp) as im0:
            im = im0.convert("RGB")
        w0, h0 = im.size
        box = CROP.get(code) or (0, 0, w0, h0)
        im = im.crop(box)
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        name = Path(fe["file"]).stem
        out = HERE / "ref" / "ep19" / f"{name}.jpg"
        im.save(out, quality=92)
        db[name] = dict(code=code, file=sp.name, cut=" ".join(cuts[code]), credit=f[8], note=f[9] if len(f) > 9 else "",
                        box=[round(box[0] / w0, 4), round(box[1] / h0, 4), round(box[2] / w0, 4), round(box[3] / h0, 4)],
                        crop_px=list(box), w=im.width, h=im.height, md5=md5(out), src_md5=md5(sp),
                        lic=lic, frame=False, ground=f[7].strip(), url=fe.get("page") or fe.get("url"))
        print(f"✓ {code:10} {name:22} {im.width}x{im.height}  {' '.join(cuts[code])}  {lic}{'  切り=' + str(box) if code in CROP else ''}")
    db_path.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep19/assets.json（{len(db)}点）")
    return 1 if bad else 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵＝`cuts.ss.vid`・`ss.head` の photo）＝footage.USE の start の1コマ。
    NIST の映像＝`ref/ep19/fb_<カット>.jpg`（走査の版 `out/jiko/foot/ep19_scan/<記号>.mp4` から＝秒は元の版と同じ・幅1920）
    ／フリー素材＝`ref/ep19/stock/fb_<カット>.jpg`（棚の mp4 から）。🔴 フリー素材の控えは git に入れない（決め⑨・棚の設計 §2）
    ＝Actions では無い＝⑤b-7 で Actions の上で作る道を足す。`fb c101 c102` のように書けばそのカットだけ（ほかの md5 を動かさない）"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    clips = json.loads(CLIPS.read_text(encoding="utf-8"))
    bad = 0
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
        c = clips[u["clip"]]
        if c.get("stock"):
            src, dst = HERE / "ref" / c["file"], HERE / "ref" / "ep19" / "stock" / f"fb_{cid}.jpg"
        else:
            src, dst = SCAN / f"{u['clip']}.mp4", HERE / "ref" / "ep19" / f"fb_{cid}.jpg"
        if not src.exists():
            print(f"🔴 {cid}: 元の動画が手元に無い（{src.relative_to(HERE).as_posix()}）")
            bad += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["ffmpeg", "-y", "-nostdin", "-v", "error", "-ss", f"{float(u['start']):.2f}", "-i", str(src),
                            "-frames:v", "1", "-vf", "scale=1920:-2", "-q:v", "3", str(dst)], capture_output=True, text=True)
        if r.returncode or not dst.exists():
            print(f"🔴 {cid}: ひかえの静止画が作れない（{r.stderr[-160:]}）")
            bad += 1
            continue
        print(f"✓ {cid:5} {u['clip']:14} {float(u['start']):7.1f}秒 → {dst.relative_to(HERE).as_posix()}")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] == "build":
        sys.exit(cmd_build(set(a[1:]) or None))
    yes = "--yes" in a
    if a and a[0] == "clips":
        sys.exit(cmd_clips())
    if a and a[0] == "use":
        sys.exit(cmd_use())
    if a and a[0] == "shotfix":
        sys.exit(cmd_shotfix())
    if a and a[0] == "stock":
        sys.exit(cmd_stock(yes))
    if a and a[0] == "scan":
        sys.exit(cmd_scan(yes))
    if a and a[0] == "photos":
        sys.exit(cmd_photos(yes))
    print(__doc__)
