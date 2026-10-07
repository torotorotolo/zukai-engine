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
# 🆕 ⑤b-7c（2026-10-07）：映像の寄せ（USE の zoom・xbias・bias＝build_jiko の `fit`／`_fit_geom` の幾何）。箱は元の画素で、
#   原寸の切り出し（`ep19_scan.py fcrop`・4コマの目盛り `grid`）で外す物の位置を測ってから決めた
FRAME = {
    # c202＝B1 1920×1014 → 全画面 1920×1080：切り口 x 17〜1090・y 172〜776（銘板 640〜1065×240〜512 が入る）。
    #   左の作業員のヘルメットは x 1110 から・Ford の印は y 800 から（fc_B1_009.8_960_300／620_700）＝どちらも切り口の外
    "c202": dict(zoom=1.68, xbias=0.02, bias=0.42),
    # cb02＝pb_52888 2560×1440：切り口 x 0〜1652・y 250〜1179（genzaichi の (0,250)-(1650,1178)）。重機の LIEBHERR の字は
    #   1〜6.1秒のどのコマでも x 1877 より右（4コマの目盛り grid_pb_52888_001.0）＝切り口の外
    "cb02": dict(zoom=1.55, xbias=0.0, bias=0.49),
    # ca06＝TLS 1920×1080：切り口 x 359〜1920・y 0〜878。高所作業車の社名「Genie GS-1930」（3.46秒から x 100〜330・y 860〜960）を
    #   切り口の外へ（4コマの目盛り grid_TLS_000.0）。右下の NIST の印（y 900〜1000）も外れる
    "ca06": dict(zoom=1.23, xbias=1.0, bias=0.0),
    # 🆕 試し焼き try1 の所見：NIST の動画のスライド（TFV 1920×1080）は上の帯（題と NIST の印＝y 0〜145）がこちらの見出し・
    #   副題と重なった（c606・ca12・ca15・ca17＝シート 7・13・14）。全画面で寄せると柱の札（D〜M＝y 158〜222・原寸 fc_TFV_3485.0_0_0）が
    #   切れるか見出しと重なる（try2）＝**額装（ss.vid の panel=True）**にして額の中で題の帯だけ外す（y 149〜1080・Source と札は残る）
    **{c: dict(zoom=1.16, xbias=0.5, bias=1.0) for c in ("c606", "ca12", "ca15", "ca17")},
}


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
        # 🆕 ⑤b-7c（2026-10-07）：尻の映像の差し込みは USE の別の欄 `<cid>~t`（scene_jiko.TAIL_KEY）＝tail=True
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
        out.append((u["cid"], u["code"], *ab, _need(u["cid"], u["role"], float(u["secs"])), u["role"]))
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
    if role == "tail":
        # 🆕 ⑤b-7c：尻の映像＝差し込みが入る秒（ins_k 行目＝`at=k−1`）からカットの終わりまで（build_jiko.tail_frame の t−sec）
        return round(secs[cid] - SJ.card_of(cid) - SJ.ins_sec(cid, k - 1), 3)
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
        # 🆕 ⑤b-7c（2026-10-07）：NIST の素材で表に無いもの（c802 の GIF＝走査の版 GIF.mp4）も同じ物差しで足す
        if not v.get("stock") and k not in sd and (SCAN / f"{k}.mp4").exists():
            sh, dur = SH.shots_of(SCAN / f"{k}.mp4")
            sd[k] = dict(src=v["media"], scan=f"out/jiko/foot/ep19_scan/{k}.mp4", dur=round(dur, 1),
                         how="1秒1コマを tools/shots.boundaries（2026-10-07 ⑤b-7c）", shots=sh)
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
    "B5": {"move": {28.0: (28.4, "c106 の尻：コンクリートのコア抜きの刃は 28.4秒から（fine 28〜39＝28.4秒 52.4・10-07 ⑤b-7c）"),
                    38.0: (38.5, "c106 の尻：コア抜きは 38.5秒まで（fine 28〜39＝38.5秒 43.0・10-07 ⑤b-7c）")},
           "join": {32.0: "c106 の尻：32.7秒の跳び（9.2）は人の足が動いただけ＝同じショット（4コマ grid_B5_032.3 を目で見た・10-07 ⑤b-7c）",
                    105.0: "c912：倉庫の部材のあいだは 100〜109.2秒の1本・104〜105秒はカメラが右へ振れただけ（1秒刻み B5_sec_102.00 を目で見た・10-06 ⑤b-2）"}},
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
    for cid0, code, a, b, need, role in _uses():
        cid = cid0 + "~t" if role == "tail" else cid0          # 🆕 ⑤b-7c：尻の映像の差し込みの欄（scene_jiko.TAIL_KEY）
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
        opt += ", head=True" if role == "head" else ", tail=True" if role == "tail" else ""
        opt += "".join(f", {k}={v}" for k, v in FRAME.get(cid, {}).items())
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
    # 🆕 ⑤b-7a（2026-10-06）：⑤b-1 の原寸で見て決めた箱（list19 の注）＝もとから在る大きな商標・社名・電話番号・顔の近い人を切り口の外へ
    "N#33": (0, 580, 4032, 2848),    # c317：上の真ん中のドリルの商標（DEWALT）・右上のバケツの字
    "N#12": (0, 300, 2900, 1931),    # c319：右の人のベストの「Milwaukee」・ヘルメットの「MSA」
    "N#10": (252, 588, 5082, 4480),  # c419：左上の黄色い重機の字（上）・右奥の人の列（右）＝⑤b-7a で全体を見て決めた（縦横 1.24＝額装）
    "F:6717686": (325, 125, 2000, 1068),   # c707：左の重機の「CAT 336E」
    "N#16": (0, 1386, 5124, 4267),   # c715：上の赤いテントの「Milwaukee」・右の Hyundai
    "N#20": (0, 1008, 3583, 3024),   # c717：奥のトラックの会社名と電話番号
    "N#17": (0, 0, 4032, 2268),      # ca13：右下の郡警察の鑑識3人の顔が近い
    "N#11": (1260, 630, 6720, 3700),  # ca19：左の重機の「CAT 980K」
    "N#53": (389, 137, 2972, 1591),  # cc27：右の KOMATSU・左の GS-1930（壊れ方を寄せて見せる）
}
# 🆕 ⑤b-7a：切り口の中に残る読める字（車のナンバー）＝元の画素の箱をモザイク（PD の写真だけ＝§B2-2b の考え方。BY・BY-SA には当てない）
BLUR = {
    "C6": [(298, 774, 350, 802)],    # c703：灰色の車のナンバー（⑤b-1 の原寸）
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
        for bx in BLUR.get(code, ()):
            if lic != "Public domain":
                print(f"🔴 {code}: モザイクは PD の写真だけ（{lic}＝改変になる）")
                bad += 1
                continue
            x0, y0, x1, y1 = bx[0] - 6, bx[1] - 6, bx[2] + 6, bx[3] + 6     # 縁の字の欠片も残さない
            part = im.crop((x0, y0, x1, y1))
            part = part.resize((max(1, (x1 - x0) // 10), max(1, (y1 - y0) // 10)), Image.BILINEAR)
            im.paste(part.resize((x1 - x0, y1 - y0), Image.NEAREST), (x0, y0))
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
                        lic=lic, frame=False, ground=f[7].strip(), url=fe.get("page") or fe.get("url"),
                        blur=[list(b) for b in BLUR.get(code, ())])
        print(f"✓ {code:10} {name:22} {im.width}x{im.height}  {' '.join(cuts[code])}  {lic}{'  切り=' + str(box) if code in CROP else ''}"
              f"{'  モザイク=' + str(BLUR[code]) if code in BLUR else ''}")
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


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7b（2026-10-06）：頁のカット＝NIST のスライドの切り抜き（旧版の束から写す）と、資料の頁（大陪審の報告・2018年の調査の報告）
# ══════════════════════════════════════════════════════════
#   スライド＝旧版（4本目）の `ref/surfside/tf_p*.jpg`（NIST の技術的知見の動画のスライド＝©2021 の写真は旧版で切り落とし済み・
#   ⑤b-7b でシート2枚で見た）を `ref/ep19/` へ写す（`ref/surfside/` は読むだけ）。
#   🔴 下地が他者の図面のスライド（管財人の原図＝p57・p58／町の図面＝p77）は**紙面の引用**＝額装・無加工・色を変えない（frame=True）
SLIDES = {
    # 名: (使うカット, 額装だけ, 出典の行)
    "tf_p003_model": ("c205 c206", False, "出典：NIST（技術的知見の動画のスライド3）"),
    "tf_p050_3d": ("c502", False, "出典：NIST（技術的知見の動画のスライド50）"),
    "tf_p050_gate": ("c504", False, "出典：NIST（技術的知見の動画のスライド50・目撃談にもとづく絵）"),
    "tf_p052_gate": ("c509", False, "出典：NIST（技術的知見の動画のスライド52・目撃談にもとづく絵）"),
    "tf_p057_3d": ("c515", False, "出典：NIST（技術的知見の動画のスライド57）"),
    "tf_p057_memo": ("c516", True, "出典：NIST（技術的知見の動画のスライド57）・下地の図：管財人（CTS Receiver）"),
    "tf_p058_note": ("c520", True, "出典：NIST（技術的知見の動画のスライド58）・下地の図：管財人（CTS Receiver）"),
    "tf_p084_salt": ("c811", False, "出典：NIST（技術的知見の動画のスライド84）"),
    "tf_p075_cover": ("c906", False, "出典：NIST（技術的知見の動画のスライド75）"),
    "tf_p076_bars": ("c909", True, "出典：NIST（技術的知見の動画のスライド77）・図面：Town of Surfside"),
    "tf_p174_corr": ("c307", False, "出典：NIST（技術的知見の動画のスライド174）"),
    "tf_p185_87park": ("cb07", False, "出典：NIST（技術的知見の動画のスライド185）"),
}


def cmd_slides():
    import shutil
    db_path = HERE / "ref" / "ep19" / "assets.json"
    db = json.loads(db_path.read_text(encoding="utf-8"))
    from PIL import Image
    for n, (cuts, frame, cr) in SLIDES.items():
        src, dst = HERE / "ref" / "surfside" / f"{n}.jpg", HERE / "ref" / "ep19" / f"{n}.jpg"
        shutil.copyfile(src, dst)
        with Image.open(dst) as im:
            w, h = im.size
        db[n] = dict(code="TF頁", file=f"surfside/{n}.jpg", cut=cuts, credit=cr, note="旧版の束から写した（⑤b-7b）",
                     box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h, md5=md5(dst), src_md5=md5(src),
                     lic="Public domain" if not frame else "Public domain（下地の図は引用）", frame=frame,
                     ground="A" if not frame else "A＋第三者（引用）", url="NIST 技術的知見の動画（2026年6月）", blur=[])
        print(f"✓ {n:16} {w}x{h}  {cuts}{'  額装だけ（引用）' if frame else ''}")
    # 🆕 ⑤b-7c（2026-10-07）：諮問委員会の資料（A01・文字の層あり）の頁を 1920×1080 に焼く。決め②＝崩落の瞬間は p.47〜51 の頁で引用
    #   （動く映像は使わない・頁ごと・額装・無加工）。p.47＝南東の防犯カメラのコマ（1:22:19 AM・真ん中の部分が崩れ東の部分へ進む・
    #   K〜P の柱の印は NIST）＝語りの「最初のコマ」（TR0317）そのものではない＝見出しで「最初のコマ」と名乗らない（c618）
    import fitz
    pdf_path = SRC / "nist_ncstac_2026-09_CTSupdate.pdf"
    pdf = fitz.open(str(pdf_path))
    for n, (pg, cuts, cr) in NCST_PAGES.items():
        dst = HERE / "ref" / "ep19" / f"{n}.jpg"
        pm = pdf[pg - 1].get_pixmap(matrix=fitz.Matrix(2, 2))         # 960×540 pt → 1920×1080
        Image.frombytes("RGB", (pm.width, pm.height), pm.samples).save(dst, quality=92)
        w, h = pm.width, pm.height
        db[n] = dict(code="TF頁", file=f"ep19/src/{pdf_path.name}#p{pg}", cut=cuts, credit=cr,
                     note="諮問委員会の資料の頁を焼いた（⑤b-7c・決め②）", box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                     md5=md5(dst), src_md5=md5(pdf_path), lic="Public domain（映像のコマは引用）", frame=True,
                     ground="A＋第三者（引用）", url="NIST 諮問委員会（NCST Advisory Committee）2026年9月の資料", blur=[],
                     year=2021)          # 頁のコマの日付（左下「6/24/2021」）＝撮影の年
        print(f"✓ {n:16} {w}x{h}  {cuts}  額装だけ（引用）")
    db_path.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


NCST_PAGES = {   # 名: (頁, 使うカット, 出典の行)
    "ncst_p047": (47, "c618", "出典：NIST（諮問委員会の資料 2026年9月 p.47）・映像のコマ：© 2021 Used with permission"),
}


#   資料の頁＝スキャンの PDF（文字の層 0字）＝頁を 200dpi の灰色に焼き、Windows の OCR の行で目印を探して切る。
#   切り口の上下と寄りの縦の寄せ（bias）は 18本目の `_fit_cut`（寄りの縮みを上下のすき間で受ける）をそのまま使う
SRC = HERE / "ref" / "ep19" / "src"
PAGE_DOCS19 = {"GJ": (SRC / "miamidade_grandjury_2021spring_report_redacted.pdf", 3000),
               "MC18": (SRC / "surfside_morabito_2018-10-08_structural_field_survey.pdf", 4000)}
PAGE_DPI = 200
# カット → (通し頁, 始めの目印, 終わりの目印, 追加)。目印＝OCR の行の字（a〜z・0〜9 だけにした字）への正規表現
PAGE_CUTS = {
    # 2018年の調査の報告 p.7＝防水が寿命を過ぎ、下の床版に大きな傷み（1段落目の頭の4行・🔴 a. の設計者の会社名は入れない）
    "c310": (4007, r"observedt.bebeyond", r"slabbel.wtheseareas", dict(hi=r"failuret.replace")),   # OCR は to を「t0」と読む
    # 大陪審の報告 p.17＝節 V の見出しから「遅くとも2018年10月8日には…知っていた」の文まで
    "c402": (3020, r"thedangerofneglect", r"inspectthebuilding", {}),
    # p.18＝「何十年も日ごろの補修と手入れをしてこなかった」〜「見積もりは1,400万ドル超」
    "c407": (3021, r"decadesleading", r"posedcosts", {}),     # OCR は「The PI ℃ posed costs」と読む
    # p.18＝「29か月たっても…町も何の手も打っていなかった」
    "c410": (3021, r"29months", r"safety\w{0,4}thebuilding", {}),
    # p.1＝「原因探しではなく仕組みを調べた」〜「どの段階でも、すべての関係者に落ち度」
    "cc02": (3004, r"forourfocus", r"participants$", {}),
}


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _ocr19():
    p = HERE / "ref" / "ep19" / "ocr_slides.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def _anchor_line(lines, pat, pr, last=False):
    joined, owner = "", []
    for i, ln in enumerate(lines):
        t = _norm(ln["text"])
        joined += t
        owner += [i] * len(t)
    pat2 = pat.replace("$", "") if pat.endswith("$") else pat
    ms = list(re.finditer(pat2, joined))
    if pat.endswith("$"):        # 「…$」＝その語で終わる行（段落の終わり）
        ms = [m for m in ms if m.end() == len(joined) or owner[m.end()] != owner[m.end() - 1]]
    if len(ms) != 1:
        raise SystemExit(f"🔴 p{pr}：目印「{pat}」が {len(ms)} か所＝1か所でないと切らない")
    m = ms[0]
    return owner[m.end() - 1] if last else owner[m.start()]


def cmd_pages(only=None):
    import fitz
    import numpy as np
    sys.path.insert(0, str(HERE / "qa_out"))
    sys.path.insert(0, str(HERE / "tools"))
    import ep18_assets as E18
    import check_slide as CS
    pj_path = HERE / "ref" / "ep19" / "pages.json"
    pj = json.loads(pj_path.read_text(encoding="utf-8")) if pj_path.exists() else {}
    want_pages = sorted({v[0] for v in PAGE_CUTS.values()})
    ocr = _ocr19()
    fresh = []
    for pr in want_pages:
        if only and pr not in only:
            continue
        doc = "GJ" if 3001 <= pr <= 3043 else "MC18"
        fn, base = PAGE_DOCS19[doc]
        out = HERE / "ref" / "ep19" / f"pg{pr}.png"
        with fitz.open(fn) as d:
            pix = d[pr - base - 1].get_pixmap(dpi=PAGE_DPI, colorspace=fitz.csGRAY)
            pix.save(out)
        if f"pg{pr}.png" not in ocr:
            fresh.append(out)
    if fresh:
        got = CS.run_ocr(fresh)
        ocr.update(got)
        (HERE / "ref" / "ep19" / "ocr_slides.json").write_text(json.dumps(ocr, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"OCR {len(got)}頁")
    for pr in want_pages:
        if only and pr not in only:
            continue
        doc = "GJ" if 3001 <= pr <= 3043 else "MC18"
        out = HERE / "ref" / "ep19" / f"pg{pr}.png"
        from PIL import Image
        with Image.open(out) as im:
            a = np.asarray(im.convert("L"))
        Hp, Wp = a.shape
        v = ocr[f"pg{pr}.png"]
        lines = sorted([ln for ln in v["lines"] if ln["box"][3] - ln["box"][1] >= 10], key=lambda ln: (ln["box"][1] + ln["box"][3]) / 2)
        core = [(ln["box"][1] / Hp + 0.07 * (ln["box"][3] - ln["box"][1]) / Hp, ln["box"][3] / Hp - 0.07 * (ln["box"][3] - ln["box"][1]) / Hp)
                for ln in lines if E18.COLS[0] <= (ln["box"][0] + ln["box"][2]) / 2 / Wp < E18.COLS[1]]
        bands = E18._occupied(E18._bands(a, *E18.COLS), core)

        def band_of(i):
            c = (lines[i]["box"][1] + lines[i]["box"][3]) / 2 / Hp
            k = min(range(len(bands)), key=lambda j: abs((bands[j][0] + bands[j][1]) / 2 - c))
            if not bands[k][0] - 0.012 <= c <= bands[k][1] + 0.012:
                raise SystemExit(f"🔴 p{pr}：OCR の行（y {c:.4f}）に近い字の帯が無い")
            return k
        cuts, biases = {}, {}
        for cid, (p2, a_from, a_to, opt) in PAGE_CUTS.items():
            if p2 != pr:
                continue
            j0, j1 = band_of(_anchor_line(lines, a_from, pr)), band_of(_anchor_line(lines, a_to, pr, last=True))
            lo, hi = 0, len(bands) - 1
            if opt.get("hi"):
                hi = band_of(_anchor_line(lines, opt["hi"], pr)) - 1
            if opt.get("lo"):
                lo = band_of(_anchor_line(lines, opt["lo"], pr))
            x0, x1 = E18._ink_x(a, bands[max(lo, j0 - 4)][0], bands[min(hi, j1 + 4)][1], *E18.COLS)
            pad = (10 * PAGE_DPI / 72) / Wp
            x0, x1 = max(0.0, x0 - pad), min(1.0, x1 + pad)
            want = (x1 - x0) * Wp / E18.PANEL_AR_T / Hp
            j0, j1, top, bot, bias = E18._fit_cut(bands, j0, j1, lo, hi, 1 / Hp, want)
            x0, x1 = E18._ink_x(a, top, bot, *E18.COLS)
            x0, x1 = max(0.0, x0 - pad), min(1.0, x1 + pad)
            box = [round(float(t), 4) for t in (x0, max(0.0, top), x1, min(1.0, bot))]
            cuts[cid], biases[cid] = box, bias
            print(f"✓ pg{pr} {cid}  trim={box}  帯 {j0}〜{j1}  bias={bias}  縦横比 {round((box[2] - box[0]) * Wp / ((box[3] - box[1]) * Hp), 2)}")
        pj[f"pg{pr}"] = dict(doc=doc, pdf=PAGE_DOCS19[doc][0].name, pdf_page=pr - PAGE_DOCS19[doc][1], w=Wp, h=Hp, dpi=PAGE_DPI,
                             md5=md5(out), cuts=cuts, bias=biases)
    pj_path.write_text(json.dumps(pj, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


CREDITS_JSON = HERE / "ref" / "ep19" / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②）
CREDITS_HEAD = "## サーフサイドのマンション崩壊のリメイク（2021-06-24・19本目）"
_PD_SHOW = {"A": "パブリックドメイン", "A（FEMA）": "パブリックドメイン", "A（DHS）": "パブリックドメイン"}


def credit_line(r):
    """画面の出典。🔴 決め①＝郡の消防（PD-FLGov の可能性）は「PD」と書かない＝台帳の credit のまま。
    CC BY は章の色のデュオトーン（色の置き換え）＝改変＝「色調を変更」を添える（BY の表示の条件）"""
    c = r["credit"]
    g = r["ground"]
    if g in _PD_SHOW:
        return c[:-1] + f"・{_PD_SHOW[g]}）" if c.endswith("）") else f"{c}（{_PD_SHOW[g]}）"
    if r["lic"].startswith("CC BY"):
        return c[:-1] + "・色調を変更）" if c.endswith("）") else f"{c}（{r['lic']}・色調を変更）"
    return c


def cmd_credits(write=False):
    """`ref/ep19/credits.json`（画面の出典）と `ref/CREDITS.md` の19本目の節（§1 写真の表＝門番 check_credits が副題の年と照らす）。
    撮影年＝その写真を当てたカットの list19 の副題の年（副題は映像方針で写真の説明から書いた＝NIST・DVIDS・Commons の説明）。
    副題に年の無い写真は「不明」（副題も年を名乗らない）"""
    db = json.loads((HERE / "ref" / "ep19" / "assets.json").read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    cj, rows = {}, []
    for n, r in sorted(db.items()):
        cuts = r["cut"].split()
        ys = sorted({m.group(1) for c in cuts for m in re.finditer(r"(20\d\d)年", subs.get(c, ""))})
        if r.get("year"):                 # 🆕 ⑤b-7c：台帳に年を持つ点（ncst_p047＝コマの日付 6/24/2021）は副題でなくそれ
            ys = [str(r["year"])]
        if len(ys) > 1:
            raise SystemExit(f"🔴 {n}: 当てたカットの副題で年が割れる（{ys}）")
        cj[f"ep19/{n}.jpg"] = credit_line(r)
        how = "・".join(x for x in [f"切り出し {r['crop_px']}" if r["box"] != [0.0, 0.0, 1.0, 1.0] else "",
                                    f"モザイク {r['blur']}" if r.get("blur") else ""] if x)
        rows.append(f"| `{n}` | {' '.join(cuts)} | {ys[0] if ys else '不明'} | {r['lic']}（{r['ground']}） | "
                    f"{r['credit'].replace('出典：', '')} | {r['url']}{'　' + how if how else ''} |")
    # 🆕 ⑤b-7b：資料の頁（pages.json）＝出典の行は資料の名と頁（`illu.rec_line`＝図のカットの出典と同じ書き方）
    sys.path.insert(0, str(HERE / "tools"))
    import illu
    pj_path = HERE / "ref" / "ep19" / "pages.json"
    pages = json.loads(pj_path.read_text(encoding="utf-8")) if pj_path.exists() else {}
    PAGE_YEAR = {"GJ": 2021, "MC18": 2018}
    PAGE_WHO = {"GJ": ("マイアミ・デイド郡の大陪審", "フロリダ州の公記録（郡の州検事局が公開）"),
                "MC18": ("モラビト社（構造技術者）", "サーフサイド町が公開した記録（フロリダ州の公記録）")}
    for k, p in sorted(pages.items()):
        pr = int(k[2:])
        line = illu.rec_line([f"{p['doc']} p{pr}"])
        if not line:
            raise SystemExit(f"🔴 p{pr} の出典の行が作れない（`cuts/ss.REC_DOCS` に資料が無い）")
        cj[f"ep19/{k}.png"] = line                 # rec_line は「出典：」から始まる
        rows.append(f"| `{k}` | {' '.join(sorted(p.get('cuts', {})))} | {PAGE_YEAR[p['doc']]} | {PAGE_WHO[p['doc']][1]} | "
                    f"{PAGE_WHO[p['doc']][0]} | {p['pdf']} PDF {p['pdf_page']}頁 |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真 {len(db)}点・頁 {len(pages)}枚")
    if write:
        CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
        md = CREDITS_MD.read_text(encoding="utf-8")
        block = "\n".join([
            CREDITS_HEAD, "",
            "※2026-10-06（⑤b-7a）。`qa_out/ep19_assets.py credits --write` が書く（手で直さない）。旧版の節は上の"
            "「4本目：サーフサイド（Champlain Towers South・2021-06-24）」＝直さない（公開ずみ）。",
            "",
            "### 1. 写真（NIST・FEMA〈DVIDS〉・DHS＝米連邦の職務著作 PD／マイアミ・デイド郡消防＝フロリダ州の公記録／CC BY 2.0）",
            "- 🔴 **郡の消防の写真（Commons の PD-FLGov）は画面に「PD」と書かない**（決め①・10-06 カズヤくん）＝「マイアミ・デイド郡消防（フロリダ州の公記録）」",
            "- 🔴 CC BY-SA は使わない（決め③）。CC BY 2.0 の1点（Steve Jurvetson）は章の色のデュオトーン＝色の改変＝出典に「色調を変更」",
            "- 🔴 もとから在る大きな商標・社名・電話番号・顔の近い人（郡警察の鑑識）は束の中で**切り落とした**（`qa_out/ep19_assets.py` の CROP＝"
            "⑤b-1 の原寸で決めた箱）。車のナンバー1つは**モザイク**（PD の写真だけ・BLUR）",
            "- 🔴 人が写る写真（§B2-2）：救助隊・調査員は公務。住戸の中は引きだけ（決め⑤）・追悼の場は DHS の引きだけ（決め⑥）",
            "- 撮影年＝写真の説明（NIST・DVIDS・Commons）から映像方針で書いた副題の年。副題に年の無い写真は「不明」",
            "",
            "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
            "|---|---|---|---|---|---|", *rows, ""])
        if CREDITS_HEAD in md:
            pre, rest = md.split(CREDITS_HEAD, 1)
            nxt = rest.find("\n## ")
            md = pre + block + (rest[nxt:] if nxt >= 0 else "")
        else:
            md = md.rstrip("\n") + "\n\n" + block
        CREDITS_MD.write_text(md, encoding="utf-8")
        print(f"→ {CREDITS_JSON.relative_to(HERE).as_posix()} ／ {CREDITS_MD.relative_to(HERE).as_posix()}")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "slides":
        sys.exit(cmd_slides())
    if a and a[0] == "pages":
        sys.exit(cmd_pages({int(x) for x in a[1:]} or None))
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
