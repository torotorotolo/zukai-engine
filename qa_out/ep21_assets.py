# -*- coding: utf-8 -*-
"""ep21_assets.py — 21本目（9.11 米国同時多発テロのリメイク）の写真・映像の束（⑤b-2・2026-10-12）。20本目 `ep20_assets.py` の形。

取得はすんでいる（映像方針＝了承②・`ref/ep21/eizou_build/fetch21.py`・記録 `fetch21.tsv`・頁の作者と許諾 `ref/ep21/src/fetch21_meta.tsv`）。
ここは**束を作る道**だけを持つ。
  python qa_out/ep21_assets.py build             # 写真の束 ref/ep21/<名>.jpg（イメージは ref/ep21/stock/<名>.jpg）＋ 権利の台帳 ref/ep21/assets.json
  python qa_out/ep21_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python qa_out/ep21_assets.py credits [--write] # 画面の出典 ref/ep21/credits.json と ref/CREDITS.md の21本目の節
  python qa_out/ep21_assets.py clip1501          # WHTV 1501 の使う区間だけの切り出し ref/ep21/clip/（リポに入れる＝下の CLIP1501 の注）
  python qa_out/ep21_assets.py shots             # ref/ep21/shots.json（映像7本のショット＝shots21.tsv から）
  python qa_out/ep21_assets.py clips             # ref/ep21/clips.json（映像7本の台帳）
  python qa_out/ep21_assets.py nogo              # tools/footage.py の EP21_NOGO（映像方針 §2 の「使わない」窓＝その秒を含むショットまるごと）
  python qa_out/ep21_assets.py fb [c101 …]       # 映像のひかえの静止画 ref/ep21/fb_<cid>.jpg（手元の元ファイルの1コマ・焼くときと同じ切り口）
  python qa_out/ep21_assets.py use               # tools/footage.py の EP21_USE（🔴 章ファイルに `ss.vid` を書いたカットだけ＝門番 slots は両側を見る）

入力＝映像方針の一覧 `ref/ep21/eizou_build/list21.tsv`（生成物・秒は narration.json の実測）・出どころ `sources21.tsv`・取得の記録 `fetch21.tsv`・
ショット `shots21.tsv`。写真の元は `ref/ep21/photo/`（git の外・原本8＋Commons の標準の縮小版49）。
🔴 束の写真は長辺を縮めるだけ（色・切り口はそのまま）＝幅 2400（寄る 1.25倍で 1920 を 1:1 で埋める）か高さ 1350 の大きい方まで。それ以下は写すだけ
   （再圧縮しない）。元の 57点は 513MB＝そのまま git に入れない（.git は 1.7GB）。
🔴 額装だけの点＝BY-SA の2点（AA11＝c204 の写真・TG99＝c205 の映像のひかえ fb_c205）＝`frame=True`（`ss.frame_only`）。
🔴 保留（束に入れない）＝顔だけモザイクの3点（SEC70＝c210・SHANK15＝c827・TSA20＝cb06）＝⑤b-7 で原寸2倍＋10px の目盛りで顔の範囲を
   決めてから MASK に書いて入れる（了承② 決め3）。私人の顔を素のままリポに積まない。縦横比だけは panel に数える。
⚠️ NTSB の図（8）・RG237 の画面（11）・文字の頁（ca18）は素材の欄が空＝頁のチャット（⑤b-3〜）で `pages` を足す。
"""
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep21"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list21.tsv"
SOURCES = BUILD / "sources21.tsv"
FETCH = BUILD / "fetch21.tsv"
SHOTS_TSV = BUILD / "shots21.tsv"
META = EPD / "src" / "fetch21_meta.tsv"
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
FOOTAGE = HERE / "tools" / "footage.py"
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## 9.11 米国同時多発テロのリメイク（2001-09-11・21本目）"
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（12本目の教訓＝footage.py の注）
EVENT_YEAR = 2001            # 副題の「当日」「9月14日」＝この年（check_credits の CLAIM_TOUJITSU と同じ物差し）

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 90
STOCK = {"B767", "SEC70", "TSA20", "DOOR15"}          # イメージ＝この事件の物でない写真（`ep21/stock/`＝check_text_screens.is_stock）
HOLD = {"SEC70": "c210 の1970年の空港の保安係と客（私人の顔だけモザイク）",
        "SHANK15": "c827 の93便の追悼の場の来訪者（顔だけモザイク）",
        "TSA20": "cb06 の保安検査の客（原寸で顔が分かるときだけモザイク）"}

# ── 画面の出典（PD は「パブリックドメイン」と書ける A・C・C'／D は PD の宣言ではない＝「知られた制限なし」＝CREDITS.md §2-12b）──
#   CC BY（継承なし）は額・寄り・流しで端を切る＝「改変：切出」をこちらで書く（`scene_jiko.credit_of` は「改変」の無い CC BY に
#   「色調変更・切出」を足す＝21本目は原色なので色調変更は嘘になる＝20本目と同じ）。BY-SA は額装・無加工＝「改変なし」
ORG = [   # sources21 の credit の頭 → 画面の機関名と、かっこの中に足す略号（A＝米連邦の職務）
    ("米空軍", "米空軍", ""), ("米海兵隊", "米海兵隊", ""), ("米海軍", "米海軍", ""), ("米国防総省", "米国防総省", ""), ("NASA", "NASA", ""),
    ("米連邦航空局", "米連邦航空局", "FAA・"), ("FEMA", "米連邦緊急事態管理庁", "FEMA・"),
    ("米環境保護庁", "米環境保護庁", "DOCUMERICA・"),
    ("Eric Draper", "ジョージ・W・ブッシュ大統領図書館", ""), ("Courtesy George W. Bush", "ジョージ・W・ブッシュ大統領図書館", ""),
]
# 撮影年（Commons の頁の日付が「上げた日」「公開の日」「不明」の点だけ、出どころの説明から）
YEAR_FIX = {"F15A": (2001, "題「after September 11, 2001」・sources21 の注「2001年11月」（頁の日付は上げた日）"),
            "EWR": (2006, "頁の日付は上げた日（2006-07-16）＝撮影もそのころ（sources21 の注「2006年」）"),
            "PENT98": (1998, "国防総省の公開 1998-04-10"),
            "ARTCC": (None, "頁は Unknown date＝副題も年を名乗らない")}


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _list():
    return list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))


def _tsv(path, keys, minf):
    out = {}
    for ln in path.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if len(f) >= minf and not ln.startswith("#") and f[0] not in ("code", "film", ""):
            out[f[0]] = dict(zip(keys, f))
    return out


def _sources():
    return _tsv(SOURCES, ["code", "class", "file", "page", "media", "dims", "dur", "mb", "rights", "credit", "note"], 10)


def _fetched():
    return _tsv(FETCH, ["code", "class", "file", "bytes", "md5", "md5_check", "dims", "dur", "exif", "page"], 9)


def _meta():
    """Commons の頁の題 → (作者, 許諾, 日付)。同じ題が何度も出る（取り直しのたびに足す）＝最後の行"""
    out = {}
    for r in csv.reader(META.open(encoding="utf-8"), delimiter="\t"):
        if len(r) >= 8 and r[0].startswith("File:"):
            out[r[0][5:]] = dict(artist=r[3], lic=r[4], date=r[6])
    return out


def _meta_of(src):
    t = src["page"].rsplit("/File:", 1)[-1].replace("_", " ")
    from urllib.parse import unquote
    return _meta().get(unquote(t))


def codes_of(main):
    return [p.strip().split("@")[0] for p in (main or "").split("+") if p.strip()]


def uses():
    """{記号: [カット]}（一覧の素材の欄から）。"""
    out = {}
    for r in _list():
        for c in codes_of(r["main"]):
            out.setdefault(c, []).append(r["cid"])
    return out


def name_of(code, src):
    stem = Path(src["file"]).stem
    return f"stock/{stem}" if code in STOCK else stem


def _year_of(code, src):
    if code in YEAR_FIX:
        return YEAR_FIX[code][0]
    m = _meta_of(src)
    d = (m or {}).get("date") or ""
    if re.search(r"upload|Released|Unknown", d, re.I) or not d:
        raise SystemExit(f"🔴 {code}: 撮影年が決まらない（頁の日付「{d}」）＝YEAR_FIX に出どころつきで書く")
    y = re.search(r"(1[89]\d\d|20\d\d)", d)
    return int(y.group(1)) if y else None


def screen_credit(code, src):
    """画面の出典の行（権利の記号＝sources21 の rights の頭）"""
    r, cr = src["rights"], src["credit"]
    m = _meta_of(src) or {}
    if r.startswith("A"):
        hit = next(((v, tag) for k, v, tag in ORG if cr.startswith(k) or k in cr), None)
        if not hit:
            raise SystemExit(f"🔴 {code}: 機関の名が決まらない（credit「{cr}」）＝ORG に足す")
        return f"出典：{hit[0]}（{hit[1]}パブリックドメイン）", hit[0]
    if r.startswith("C'"):
        return "出典：米議会図書館蔵（撮影者不詳・パブリックドメイン）", "撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄）"
    if r.startswith("C＋D"):
        return f"出典：{m['artist']}（米議会図書館蔵・パブリックドメイン）", m["artist"]
    if r.startswith("C（CC0）"):
        return f"出典：{m['artist']}（CC0）", m["artist"]
    if r.startswith("C"):
        a = re.sub(r" at English Wikipedia$", "", m["artist"])
        return f"出典：{a}（パブリックドメイン）", a
    if r.startswith("D"):
        a = m.get("artist") or cr.split("（")[0]
        return f"出典：{a}（米議会図書館蔵／知られた制限なし）", a
    if r.startswith("F"):
        a = re.sub(r"^User:", "", re.sub(r" from Finland$", "", m["artist"]))
        lic = m["lic"]
        if "SA" in lic:
            return f"出典：{a}（Flickr）／{lic}／改変なし", a
        return f"出典：{a}／{lic}／改変：切出", a
    raise SystemExit(f"🔴 {code}: 権利の記号が読めない（{r}）")


# ── 写真の束 ───────────────────────────────────────────────
def cmd_build():
    from PIL import Image
    src, fe = _sources(), _fetched()
    db, bad, held = {}, 0, []
    for code, cuts in sorted(uses().items()):
        s = src.get(code)
        if not s:
            print(f"🔴 {code}: sources21.tsv に無い")
            bad += 1
            continue
        if s["class"] != "photo":
            continue
        if code in HOLD:
            held.append(code)
            print(f"⏸ {code:8} {Path(s['file']).name:40} 保留＝{HOLD[code]}（⑤b-7 で MASK）")
            continue
        f, sp = fe.get(code), HERE / s["file"]
        if not f or not sp.exists():
            print(f"🔴 {code}: fetch21.tsv の行か手元のファイルが無い")
            bad += 1
            continue
        if md5(sp) != f["md5"]:
            print(f"🔴 {code}: {sp.name} の md5 が取得のときと違う（取り直す）")
            bad += 1
            continue
        name = name_of(code, s)
        dst = EPD / f"{name}.jpg"
        dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(sp) as im:
            w0, h0 = im.size
            k = min(1.0, max(BUNDLE_W / w0, BUNDLE_H / h0))
            if k < 1.0:
                w, h = round(w0 * k), round(h0 * k)
                im.convert("RGB").resize((w, h), Image.LANCZOS).save(dst, quality=JPEG_Q, optimize=True)
                how = f"縮小 {w0}x{h0}→{w}x{h}"
            else:
                w, h = w0, h0
                shutil.copyfile(sp, dst)
                how = "写すだけ"
        cr, who = screen_credit(code, s)
        if s["rights"].startswith("A"):
            who = s["credit"]                  # 記録の表は撮影の部局と撮影者まで（画面は機関名だけ）
        lic = (s["rights"].split("（", 1)[1].rstrip("）") if s["rights"].startswith("F") else
               "PD（米連邦の職務・17 U.S.C. §105）" if s["rights"].startswith("A") else
               "PD（撮影者が権利を放棄）" if s["rights"].startswith("C'") else
               "PD（CC0）" if "CC0" in s["rights"] else
               "米議会図書館蔵／知られた制限なし" if s["rights"].startswith("D") else "PD（自主宣言）")
        if s["rights"].startswith("F"):
            lic = (_meta_of(s) or {}).get("lic") or lic
        frame = "SA" in lic
        db[name] = dict(code=code, file=s["file"], cut=" ".join(cuts), credit=cr, who=who, note=s["note"][:200],
                        box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h, md5=md5(dst), src_md5=f["md5"],
                        lic=lic, frame=frame, ground=s["rights"], url=s["page"], blur=[], how=how,
                        year=_year_of(code, s), stock=code in STOCK)
        print(f"✓ {code:8} {name:40} {w}x{h}  {' '.join(cuts):10} {lic}{'  額装だけ' if frame else ''}  {how}")
    # 🔴 BY-SA の映像（TG99＝c205）のひかえの静止画も額装だけ（fb_c205 を `ss.vid` が写真として当てる＝`check_frame_only` が見る）
    fb205 = EPD / "fb_c205.jpg"
    if fb205.exists():
        from PIL import Image
        with Image.open(fb205) as im:
            w, h = im.size
        db["fb_c205"] = dict(code="TG99", file="ref/ep21/src/film/torri_gemelle_1999.ogv", cut="c205",
                             credit=CLIP_CREDIT["TG99"], who="Zaqq72（Wikimedia Commons）", note="映像のひかえの静止画（1コマ・切らない）",
                             box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h, md5=md5(fb205), src_md5=_fetched()["TG99"]["md5"],
                             lic="CC BY-SA 3.0", frame=True, ground="F（CC BY-SA 3.0＋GFDL）", url=_sources()["TG99"]["page"],
                             blur=[], how="映像の1コマ", year=1999, stock=False)
        print(f"✓ TG99     fb_c205（ひかえ）                        {w}x{h}  c205       CC BY-SA 3.0  額装だけ")
    else:
        print("⚠️ fb_c205.jpg がまだ無い（`fb c205` のあとに build をもう一度）")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    print(f"→ ref/ep21/assets.json（{len(db)}点・額装だけ {sum(1 for r in db.values() if r['frame'])}・イメージ "
          f"{sum(1 for r in db.values() if r['stock'])}・保留 {len(held)}＝{' '.join(held)}・束の大きさ {tot / 1e6:.1f}MB）")
    return 1 if bad else 0


def cmd_panel():
    """ルール 0b-34②：PANEL_AR＝束の縦横比の並びで、16:9 より縦長の側のいちばん大きな切れ目の中点。保留の点は取得の寸法の縦横比で数える"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    ars = [(r["w"] / r["h"], n, r["w"]) for n, r in db.items() if not n.startswith("fb_")]
    fe = _fetched()
    for code in HOLD:
        w, h = (int(x) for x in fe[code]["dims"].split("x"))
        k = min(1.0, max(BUNDLE_W / w, BUNDLE_H / h))
        ars.append((w / h, f"（保留）{code}", round(w * k)))
    ars.sort()
    for a, n, w in ars:
        print(f"  {a:6.3f}  {n:40} 幅 {w}")
    side = [x for x in ars if x[0] < 16 / 9]
    gaps = sorted(((side[i + 1][0] - side[i][0], side[i], side[i + 1]) for i in range(len(side) - 1)), reverse=True)
    for g, a, b in gaps[:4]:
        print(f"切れ目 {g * 100:5.1f}ポイント：{a[0]:.3f}（{a[1]}）→ {b[0]:.3f}（{b[1]}）＝中点 {(a[0] + b[0]) / 2:.4f}")
    return 0


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
CLIP_CREDIT = {
    "DV42": "出典：米空軍（DVIDS 122342・パブリックドメイン）",
    "DV43": "出典：米空軍（DVIDS 122343・パブリックドメイン）",
    "DV47": "出典：米空軍（DVIDS 122347・パブリックドメイン）",
    "W606": "出典：ジョージ・W・ブッシュ大統領図書館（WHTV 606・パブリックドメイン）",
    "W1501": "出典：ジョージ・W・ブッシュ大統領図書館（WHTV 1501・パブリックドメイン）",
    "W593": "出典：ジョージ・W・ブッシュ大統領図書館（NARA 6171390・パブリックドメイン）",
    "TG99": "出典：Zaqq72（Wikimedia Commons）／CC BY-SA 3.0／改変なし",
}


def _claims(sub):
    """副題が名乗る年の集合（「NNNN年」と「当日」「9月14日」のような年の無い当日まわりの日付）"""
    ys = {int(y) for y in re.findall(r"(1[89]\d\d|20\d\d)年", sub)}
    if "当日" in sub or re.match(r"9月1[1-4]日", sub):
        ys.add(EVENT_YEAR)
    return ys


def cmd_credits(write=False):
    """撮影年＝Commons の頁の日付（上げた日・不明は YEAR_FIX）。当てたカットの副題が名乗る年（「当日」＝2001）と食い違えば止める"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    cj, rows, bad = {}, [], 0
    for n, r in sorted(db.items()):
        if n.startswith("fb_"):
            continue
        cuts = r["cut"].split()
        claims = set().union(*(_claims(subs.get(c, "")) for c in cuts))
        y = r["year"]
        if claims and (y is None or claims != {y}):
            print(f"🔴 {n}: 副題の年 {sorted(claims)} と撮影年 {y} が食い違う（{' '.join(cuts)}）")
            bad += 1
        cj[f"ep21/{n}.jpg"] = r["credit"]
        who = r["who"]
        gk = re.match(r"C'|C＋D|[A-F]", r["ground"]).group(0)
        rows.append(f"| `{Path(n).name}` | {' '.join(cuts)} | {y if y else '不明'} | {r['lic']}（{gk}）{'・イメージ' if r['stock'] else ''} "
                    f"| {who} | {r['url']} |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真 {len(cj)}点{'' if not bad else f'・🔴 食い違い {bad}'}")
    if bad:
        return 1
    if not write:
        return 0
    CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    src = _sources()
    film_rows = [f"| `{c}` | {' '.join(sorted({r['cid'] for r in _list() if codes_of(r['main'])[:1] == [c]}))} | "
                 f"{CLIP_CREDIT[c]} | {src[c]['rights']} | {src[c]['page']} |" for c in CLIP_CREDIT]
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-10-12（⑤b-2）。`qa_out/ep21_assets.py credits --write` が書く（手で直さない）。旧版の節は上の"
        "「9.11 米国同時多発テロ（2001-09-11・7本目）」＝直さない（旧版は 10-05 に非公開）。",
        "",
        "### 0. 動く映像（7本・音はすべて使わない＝`-an`）",
        "- DVIDS 122342／122343／122347＝米空軍（第11通信隊・第1戦闘カメラ隊ほか）の職務＝PD（DVIDS の表示「PUBLIC DOMAIN」）。640×480・"
        "画素は正方形でない（SAR 131:128＝表示の幅 655）＝4:3 の額装＋地のぼかし・左右の黒い縁を寄り 1.03 で外す",
        "- WHTV 606・1501＝ホワイトハウス通信局（WHCA＝国防総省の機関）の職務＝PD（ジョージ・W・ブッシュ大統領図書館）。606 は Commons の webm"
        "（854×474・16:9＝全画面・右端のレンズの縁の影を寄せで外す）。🔴 **1501 は大統領図書館の YouTube にしか無い**＝使う区間（もとの"
        "380〜392秒）だけを `ref/ep21/clip/` に切り出してリポに入れた（Actions・Modal は網から取れない・md5 は clips.json）",
        "- NARA 6171390（大統領の夜の演説・cb01）＝WHCA の職務＝PD（use=Unrestricted）。16:9＝全画面",
        "- 🔴 **1999年の塔（TG99・c205）は CC BY-SA 3.0＋GFDL（Zaqq72）**＝額装・無加工・寄り0・等速・地は無地（`plain=True`）・音なし・1点1カット",
        "- 🔴 使わない窓（`tools/footage.py` の NOGO＝映像方針 §2）：担架と運ばれる人・助けられる人・記者の寄り＝その秒を含むショットまるごと",
        "",
        "| 記号 | 使うカット | 画面の出典 | 権利 | 出どころ |",
        "|---|---|---|---|---|", *film_rows, "",
        "### 1. 写真（米連邦の職務〈A〉・議会図書館の撮影者不詳〈C'＝撮影者が権利を放棄〉・知られた制限なし〈D〉・CC BY／BY-SA／CC0）",
        "- 束＝`ref/ep21/photo/`（git の外）の長辺を幅 2400／高さ 1350 まで縮めただけ（色・切り口はそのまま＝原色）。",
        "- 🔴 **D（米議会図書館の「知られた制限なし」）は PD の宣言ではない**＝画面は「米議会図書館蔵／知られた制限なし」（§2-12b）",
        "- 🔴 **CC BY-SA の写真（AA11＝c204）は額装・無加工・色そのまま・上に重ねない・寄り0・1点1カット**（`cuts/ss.check_frame_only`）",
        "- CC BY は額・寄り・流しで端を切ることがある＝画面の出典に「改変：切出」",
        "- 🔴 **イメージ（この事件の物でない写真）**＝`ep21/stock/` の名・画面の左上に「イメージ」・20% に数えない。"
        "顔だけモザイクの3点（SEC70・SHANK15・TSA20）は ⑤b-7 で範囲を決めてから束に入れる（いまは保留）",
        "- 撮影年＝Commons の頁の日付（上げた日・公開の日・不明のものは出どころの説明から＝`qa_out/ep21_assets.py` の YEAR_FIX）。"
        "副題の「当日」は 2001年として照らした",
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


# ── 映像（切り出し・ショット・台帳・使わない窓・ひかえ・USE） ─────────────
FILM = {   # 記号 → (表示の幅, 高さ, コマ/秒, SAR, 何か, 出どころの種類, 撮影の日)
    "DV42": (655, 480, 29.97, "131:128", "Noble Eagle, Sep 11 Part 1（ペンタゴン・当日）", "dvids", "2001-09-11"),
    "DV43": (655, 480, 29.97, "131:128", "Noble Eagle, Sep 11 Part 2（ペンタゴン・当日）", "dvids", "2001-09-11"),
    "DV47": (655, 480, 29.97, "131:128", "Noble Eagle, Sep 14（ペンタゴンの空撮）", "dvids", "2001-09-14"),
    "W606": (854, 474, 29.97, "1:1", "WHTV 606（バークスデール空軍基地の到着と出発）", "commons", "2001-09-11"),
    "W1501": (650, 480, 29.97, "1:1", "WHTV 1501（ホワイトハウスからの退避・近くの通り）", "local", "2001-09-11"),
    "W593": (640, 360, 29.97, "1:1", "大統領の国民への演説（NARA 6171390）", "commons", "2001-09-11"),
    "TG99": (720, 576, 25.0, "1:1", "1999年の世界貿易センター（屋上の展望台から）", "commons", "1999-09"),
}
# 🔴 WHTV 1501 はリポの中の切り出し（footage.media_of の注）。使う区間 382.0〜390.0（ショット 13＝378.28〜393.96）の前後に余白
CLIP1501 = dict(src="ref/ep21/src/film/whtv1501_20010911_crowd.mp4", dst="ref/ep21/clip/w1501_0380_0392.mp4", t0=380.0, t1=392.0)

# 中身の切り口（⑤b-2 に使う区間のコマを 0.5秒おきに測った＝scratchpad `measure_box21.py`）。
#   DVIDS＝表示の幅 655 の左 4〜8px・右 1〜3px が黒い縁（DV47 は左 8px まで）＝寄り 1.03（真ん中から左右 9.5px・上下 7px 外す）。
#   WHTV 1501＝四辺 1〜2px＝寄り 1.02。WHTV 606＝左 1〜2px・右端のレンズの縁の影（c107 の区間は 23px・c713 の区間は 38〜64px）＝
#   16:9 の全画面の箱で影を外す寄せ（c107 は x 4.5〜826.6・c713 は x 2.6〜804）。NARA 6171390 は縁なし。TG99 は BY-SA＝切らない
GEOM = {
    "DV42": dict(full=False, zoom=1.03), "DV43": dict(full=False, zoom=1.03), "DV47": dict(full=False, zoom=1.03),
    "W1501": dict(full=False, zoom=1.02),
    "W606": dict(full=True, zoom=1.025, xbias=0.14),
    "W593": dict(full=True, zoom=1.0),
    "TG99": dict(full=False, zoom=1.0, plain=True),
}
GEOM_CUT = {"c713": dict(full=True, zoom=1.05, xbias=0.05)}      # ⚠️ c713 の影は区間で幅が変わる＝⑤b-7 で原寸
FB_W = 1024                     # 額装の映像のひかえの幅（1280 未満＝`ss.kind` が額装を返す）
# 映像方針 §2 の「使わない」窓（mm:ss）＝その秒を含むショットまるごとを NOGO に
NOGO_AT = {"DV42": [("7:27", "ヘリと担架"), ("8:26", "担架で運ばれる人")],
           "DV43": [("1:11", "担架の板・助けられる人"), ("4:33", "担架の板・助けられる人"), ("4:47", "担架の板・助けられる人"),
                    ("6:25", "担架の板・助けられる人"), ("6:51", "担架の板・助けられる人")],
           "W606": [("2:04", "記者の寄り")]}


def _shots():
    out = {}
    for ln in SHOTS_TSV.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if ln.startswith("#") or len(f) < 5 or f[0] == "film":
            continue
        out.setdefault(f[0], []).append(dict(shot=int(f[1]), start=float(f[2]), until=float(f[3])))
    return out


def cmd_clip1501():
    """WHTV 1501 の使う区間だけを切り出してリポに入れる（音なし・H.264・コマは元のまま 650×480・29.97）。
    🔴 なぜリポに入れるか：大統領図書館の YouTube にしか無い（Commons・archive.org を 10-12 に語で引いて0件）＝Actions・Modal の機械は
       網から取れない（取れない映像は黙って静止画に落ちる）。12秒・数 MB＝リポの重さの約束（動画を入れない＝wav 163MB の教訓）の趣旨の内。
    確かめ＝切り出しの 2.0秒のコマと、元の 382.0秒のコマの画素の差（同じ秒なら小さい・±10コマずらすと大きい）"""
    import numpy as np
    from PIL import Image
    import io
    c = CLIP1501
    src, dst = HERE / c["src"], HERE / c["dst"]
    dst.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["ffmpeg", "-y", "-nostdin", "-v", "error", "-ss", f"{c['t0']:.3f}", "-i", str(src), "-t", f"{c['t1'] - c['t0']:.3f}",
                        "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-g", "15",
                        "-movflags", "+faststart", str(dst)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"🔴 切り出しに失敗：{r.stderr[-300:]}")

    def frame(p, t):
        b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(p), "-frames:v", "1", "-f", "image2pipe",
                            "-vcodec", "png", "-"], capture_output=True).stdout
        return np.asarray(Image.open(io.BytesIO(b)).convert("L")).astype(float)
    ref = frame(dst, 2.0)
    diffs = {k: round(float(np.abs(frame(src, 382.0 + k / 29.97) - ref).mean()), 2) for k in (-10, -1, 0, 1, 10)}
    print(f"✓ {dst.relative_to(HERE).as_posix()}  {dst.stat().st_size / 1e6:.2f}MB  md5 {md5(dst)}")
    print(f"  切り出しの 2.0秒 × 元の 382.0秒±コマ の画素の差（平均）：{diffs}")
    if min(diffs, key=diffs.get) != 0:
        raise SystemExit("🔴 切り出しの秒が元とずれている（0コマの差がいちばん小さくない）")
    return 0


def cmd_shots():
    """shots.json＝映像方針の scene 0.30 の境目（shots21.tsv）。footage の門番（outside_shot・unknown_clip）が読む"""
    sh = _shots()
    src = _sources()
    out = {}
    for code, rows in sh.items():
        out[code] = dict(src=src[code]["page"], scan=src[code]["file"], dur=float(src[code]["dur"]),
                         how="映像方針（10-12）：ffmpeg の scene 0.30＋1ショット1コマの見本帳・使う区間は1秒1コマ（shots21.tsv）",
                         shots=[dict(start=r["start"], until=r["until"], motion=0.0, shot=r["shot"]) for r in rows])
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep21/shots.json（{' '.join(f'{k} {len(v)}' for k, v in sh.items())}）")
    return 0


def cmd_clips():
    src, fe = _sources(), _fetched()
    out = {}
    for code, (dw, h, fps, sar, what, kind, date) in FILM.items():
        s = src[code]
        w = 640 if code.startswith("DV") else dw
        e = dict(url=s["page"], media=s["media"], credit=CLIP_CREDIT[code], src=kind, at=0.0, date=date, what=what,
                 w=w, h=h, fps=fps, sar=sar, sec=float(s["dur"]), size=int(fe[code]["bytes"]), dispw=dw, decoded=[w, h],
                 rights=s["rights"], scan=s["file"], effw=dw,
                 note=f"中身の切り口＝{GEOM[code]}（qa_out/ep21_assets.py の GEOM）")
        if code == "W1501":
            p = HERE / CLIP1501["dst"]
            if not p.exists():
                raise SystemExit("🔴 W1501 の切り出しが無い（先に `clip1501`）")
            e.update(media=CLIP1501["dst"], local_from=CLIP1501["t0"], sec=CLIP1501["t1"], size=p.stat().st_size, md5=md5(p),
                     note=e["note"] + "／🔴 媒体はリポの中の切り出し（もとの 380〜392秒・YouTube の手元のファイル md5 "
                                      f"{fe[code]['md5']} から）")
        out[code] = e
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep21/clips.json（{len(out)}本）")
    for k, v in out.items():
        print(f"  {k:6} {v['w']}x{v['h']} dispw {v['dispw']} sar {v['sar']} {v['sec']}秒  {v['media'][:70]}")
    return 0


def _mmss(t):
    m, s = t.split(":")
    return int(m) * 60 + int(s)


def _write_block(tag, lines):
    txt = FOOTAGE.read_text(encoding="utf-8")
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_text(txt[:m.start(2)] + "".join(x + "\n" for x in lines) + txt[m.end(2):], encoding="utf-8")


def cmd_nogo():
    sh = _shots()
    lines = []
    for code, ats in NOGO_AT.items():
        items = []
        for at, why in ats:
            t = _mmss(at)
            s = [r for r in sh[code] if r["start"] <= t < r["until"]]
            if len(s) != 1:
                raise SystemExit(f"🔴 {code} {at}：ショットが {len(s)} 本")
            s = s[0]
            items.append(f'({s["start"]:.2f}, {s["until"]:.2f}, "映像方針 §2 の {at}＝{why}（ショット {s["shot"]}）")')
        lines.append(f'    "{code}": [' + ", ".join(items) + "],")
    _write_block("EP21_NOGO", lines)
    print("→ tools/footage.py NOGO")
    for x in lines:
        print(x.strip())
    return 0


def _geom(cid, code):
    g = dict(GEOM[code])
    g.update(GEOM_CUT.get(cid, {}))
    return g


def _crop_box(sw, sh, g):
    """焼くときの切り口（`build_jiko._fit_geom` と同じ式）＝(左, 上, 幅, 高さ)。額装は箱の縦横比＝中身の縦横比（真ん中から寄り）"""
    zoom, xb, yb = g.get("zoom", 1.0), g.get("xbias", 0.5), g.get("bias", 0.5)
    if g["full"]:
        z = max(1920 / sw, 1080 / sh) * zoom
        cw, ch = min(sw, 1920 / z), min(sh, 1080 / z)
    else:
        cw, ch = sw / zoom, sh / zoom
    return (sw - cw) * xb, (sh - ch) * yb, cw, ch


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵＝`ss.vid` の photo）＝一覧の区間の頭の1コマ（手元の元ファイル）を、
    焼くときと同じ幾何（SAR を正方画素に・`_crop_box`）で切った中身。箱（`ss.kind`）もこの絵から決まる＝額装は幅 FB_W（1280 未満）・
    全画面は 1920×1080。🔴 BY-SA（TG99）は切らずにそのまま（720×576）"""
    from PIL import Image
    import io
    src = _sources()
    bad = 0
    for r in _list():
        if not r["window"]:
            continue
        cid = r["cid"]
        if only and cid not in only:
            continue
        code = codes_of(r["main"])[0]
        a = float(r["window"].split("〜")[0])
        b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-i", str(HERE / src[code]["file"]), "-frames:v", "1",
                            "-vf", "scale=iw*sar:ih,setsar=1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not b:
            print(f"🔴 {cid}: コマが取れない")
            bad += 1
            continue
        im = Image.open(io.BytesIO(b)).convert("RGB")
        sw, sh = im.size
        g = _geom(cid, code)
        l, t, cw, ch = _crop_box(sw, sh, g)
        im = im.crop((round(l), round(t), round(l + cw), round(t + ch)))
        if g["full"]:
            im = im.resize((1920, 1080), Image.LANCZOS)
        elif code != "TG99":
            im = im.resize((FB_W, round(FB_W * im.height / im.width)), Image.LANCZOS)
        dst = EPD / f"fb_{cid}.jpg"
        im.save(dst, quality=92)
        print(f"✓ {cid:5} {code:6} {a:7.2f}秒 {sw}x{sh} → 切り口 ({l:.1f},{t:.1f},{cw:.1f}x{ch:.1f}) → {im.width}x{im.height}  {dst.name}")
    return 1 if bad else 0


def cmd_use():
    """footage.USE の21本目の欄（🔴 章ファイルに `ss.vid` を書いたカットだけ＝門番 slots）。rate＝使える秒÷要る秒（切り捨て・1.0まで）・
    0.6未満は止め絵。要る秒＝footage.secs_of（尺−扉）。寄りと寄せは GEOM（ひかえの静止画と同じ幾何）"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    import check_footage_slots as SL
    secs = FO.secs_of()
    want = set(SL.slots())
    sh = _shots()
    lines, skip = [], []
    for r in _list():
        if not r["window"]:
            continue
        cid = r["cid"]
        if cid not in want:
            skip.append(cid)
            continue
        code = codes_of(r["main"])[0]
        a, b = (float(x) for x in r["window"].split("〜"))
        need = float(secs[cid])
        avail = b - a
        rate = min(1.0, int(avail / need * 100) / 100)
        s = [x for x in sh[code] if x["start"] <= a < x["until"]]
        where = f"ショット {s[0]['shot']}（{s[0]['start']:.2f}〜{s[0]['until']:.2f}秒）" if s else "ショット表の外"
        g = _geom(cid, code)
        geo = f", zoom={g['zoom']}" + (f", xbias={g['xbias']}" if "xbias" in g else "") + (", plain=True" if g.get("plain") else "")
        if rate < STILL_BELOW:
            s0 = round((a + b) / 2, 2)
            opt = f", still=True, until={min(b, s0 + 1.0):.2f}"
        else:
            s0 = a
            opt = f", until={b:.2f}, rate={rate}"
        lines.append(f'    "{cid}": dict(clip="{code}", start={s0:.2f}{opt}{geo}),   # {where}・使える {avail:.2f}秒（{a:g}〜{b:g}）／要る {need:.2f}秒')
    _write_block("EP21_USE", lines)
    print(f"→ tools/footage.py USE {len(lines)}欄（止め絵 {sum('still=True' in x for x in lines)}）")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルに ss.vid がまだ無い（⑤b-7）：{' '.join(skip)}")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "clip1501": cmd_clip1501, "shots": cmd_shots, "clips": cmd_clips,
            "nogo": cmd_nogo, "use": cmd_use}
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
