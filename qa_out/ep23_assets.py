# -*- coding: utf-8 -*-
"""ep23_assets.py — 23本目（三豊百貨店崩壊事故のリメイク）の写真・映像の束（⑤b-2・2026-10-18）。22本目 `ep22_assets.py` の形。

取得はすんでいる（映像方針＝了承②・`ref/ep23/eizou_build/fetch23.py`・記録 `fetch23.tsv`＝md5 2回）。ここは**束を作る道**だけを持つ。
  python qa_out/ep23_assets.py build             # 写真の束 ref/ep23/<名>.jpg（イメージは ref/ep23/stock/<名>.jpg）＋ 権利の台帳 ref/ep23/assets.json
  python qa_out/ep23_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python qa_out/ep23_assets.py edges             # 束の四辺の暗い帯（スライドの台紙の縁）＝門番 check_photo_edge の名簿を決める
  python qa_out/ep23_assets.py credits [--write] # 画面の出典 ref/ep23/credits.json と ref/CREDITS.md の23本目の節
  python qa_out/ep23_assets.py shots             # ref/ep23/shots.json（フリー素材の映像のショット＝tools/shots.shots_of で1秒1コマ）
  python qa_out/ep23_assets.py clips             # ref/ep23/clips.json（フリー素材の映像の台帳）
  python qa_out/ep23_assets.py fb [c205 …]       # フリー素材の映像のひかえの静止画 ref/ep23/stock/fb_<cid>.jpg（手元の mp4 の区間の頭の1コマ）
  python qa_out/ep23_assets.py use               # tools/footage.py の EP23_USE（🔴 章ファイルに `ss.vid` を書いたカットだけ＝門番 slots は両側を見る）

入力＝映像方針の一覧 `ref/ep23/eizou_build/list23.tsv`（生成物・秒は narration.json の実測＝⑤b-1）・出どころ `sources23.psv`（区切り「|」）・
取得の記録 `fetch23.tsv`・顔の範囲 `mask23.tsv`。元の画像は `ref/ep23/src/`・`ref/ep10/src/kogl/`・`ref/stock/media/`（どれも git の外）。
🔴 束の写真は長辺を縮めるだけ（色・切り口はそのまま）＝幅 2400 か高さ 1350 の大きい方まで。それ以下は縮めない。
   ・EXIF の向きの札は絵に当てる（23本目の使う点はどれも札 1 か札なし＝2026-10-18 に全点で読んだ・scratchpad `probe23.py`）
   ・🔴 **歴史編纂院の8点は CMYK（色の札 Japan Color 2001 Coated）＝札を使って sRGB の RGB に写す**（映像方針 §6-3「CMYK は RGB に＝技術の変換」）
   ・色の札 c2（Commons の小さな sRGB の札）・sRGB はそのまま
🔴 **イメージ（フリー素材の写真＝Pexels の8点）は git に入れない**（19本目 決め⑨＝フリー素材の静止画を公開リポに置かない・映像のひかえと同じ）。
   束は取ったファイルそのまま（向きの札 1・色の札なし・幅 1920＝縮めない＝md5 が取得のときと同じ）。Actions・Modal の上では
   `tools/footage.py` の `stock_photos()` が台帳の `media`（直リンク）から取り直して md5 を照らす（違えば止める）。
🔴 **個人名義の Commons の10点（作者欄が個人）は、画面の出典の行に作者欄の名前を出す（了承② 決め4＝クレジット A）が、名前は公開リポに書かない**
   （10-17 カズヤくん「名前0」）＝credits.json の行は印 `{作者}` だけを持ち、焼くときに `scene_jiko.ep23_credit` が git の外の表
   `ref/ep23/src/credits_private.tsv`（Modal は保管庫 `jiko-assets` の同じ道＝`modal_app.pull_private`）から名前を足す。表が無ければ止める
   （Actions の試し焼きだけ仮の字「〇〇〇」＝検品の焼き。本編は Modal）。CREDITS.md の節は「作者欄のとおり」と Commons の頁の URL。
🔴 顔だけモザイク（了承② 決め2）＝`mask23.tsv` の範囲（元の画像の画素）を束で升目にする＝元の画像そのものを直す（`ss.NEEDS_MASK`・`ref/ep23/masked.json`）。
   歴史編纂院 104（行方を探す掲示板）は10本目に顔と名前を隠した版（`ref/ep10/missing_board_01.jpg`）をそのまま使う＝NEEDS_MASK にも載せる。
"""
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep23"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list23.tsv"
SOURCES = BUILD / "sources23.psv"
FETCH = BUILD / "fetch23.tsv"
MASKS = BUILD / "mask23.tsv"
CAND = BUILD / "stock23_cand.psv"
PRIVATE = EPD / "src" / "credits_private.tsv"      # 🔴 git の外（作者欄・題）＝ここから名前を公開の物へ写さない
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
FOOTAGE = HERE / "tools" / "footage.py"
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## 三豊百貨店崩壊事故のリメイク（1995-06-29・23本目）"
AUTHOR = "{作者}"            # 個人名義の点の画面の出典の行の印（焼くときに git の外の表から足す＝scene_jiko.ep23_credit）
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（footage.py の注）
EVENT_YEAR = 1995            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 92
MOSAIC_PX = 14                         # 顔のモザイクの升（束の画素）＝10本目と同じ目安（mask23.tsv の注）
FRAME_RIGHTS = ("BY-SA",)              # 額装だけ（了承② 決め3＝BY-SA は高さいっぱいの額装・寄り0・色は原本）
MASKED_BEFORE = {"H104m": "顔と名前にモザイク（10本目に隠した版 `ref/ep10/missing_board_01.jpg`）"}

LIC = {"A（公共ヌリ第1類型＋CC BY 4.0）": "公共ヌリ第1類型＋CC BY 4.0", "A（公共ヌリ第1類型）": "公共ヌリ第1類型",
       "BY-SA 4.0（本部）": "CC BY-SA 4.0", "BY-SA 4.0（own＝作者は個人）": "CC BY-SA 4.0",
       "フリー素材（Pexels License）": "Pexels License", "フリー素材（Pixabay Content License）": "Pixabay Content License"}
LIC_URL = {"Pexels License": "https://www.pexels.com/license/", "Pixabay Content License": "https://pixabay.com/service/license-summary/"}
OWN = "BY-SA 4.0（own＝作者は個人）"


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _list():
    return list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))


def _sources():
    out = {}
    for ln in SOURCES.read_text(encoding="utf-8").splitlines():
        if ln.startswith("#") or ln.startswith("code|") or not ln.strip():
            continue
        f = ln.split("|")
        if len(f) < 11:
            raise SystemExit(f"🔴 sources23.psv の行の欄が足りない：{ln[:80]}")
        out[f[0]] = dict(zip(["code", "class", "file", "page", "media", "get", "dims", "bytes", "rights", "credit", "note"], f))
    return out


def _fetched():
    out = {}
    for ln in FETCH.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if ln.startswith("#") or len(f) < 7 or f[0] == "code":
            continue
        out[(f[0], f[1])] = dict(zip(["code", "file", "bytes", "md5", "md5_check", "dims", "get"], f))
    return out


def _private():
    """git の外の表 {記号: {title, artist, credit, license, page}}。無ければ止める（束を作る手元だけで読む）"""
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の作者欄の表＝映像方針の fetch23.py credits）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    head = rows[0]
    return {r[0]: dict(zip(head, r)) for r in rows[1:]}


def _masks():
    out = {}
    for ln in MASKS.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if ln.startswith("#") or len(f) < 5 or f[0] == "code":
            continue
        x0, y0, x1, y1 = (int(v) for v in f[2].split(","))
        out.setdefault(f[0], []).append((x0, y0, x1, y1, f[4]))
    return out


def uses():
    """{記号: [カット]}（一覧の素材の欄から・写真とフリー素材の写真だけ＝映像は台帳 clips.json の側）。"""
    src = _sources()
    out = {}
    for r in _list():
        c = r["code"]
        if c and src.get(c, {}).get("file", "").lower().endswith(".jpg"):
            out.setdefault(c, []).append(r["cid"])
    return out


def is_stock(s):
    return s["class"] == "stock"


def name_of(code, s):
    stem = Path(s["file"]).stem
    return f"stock/{stem}" if is_stock(s) else stem


# 撮影年（副題の年の主張と照らす＝check_credits）。出どころ：Commons の題（本部の「19950629…」）・研究院と歴史編纂院の頁の注（sources23 の note）・
#   写真の中身。分からない点は None（表は「不明」・副題に年を書かない）
def year_of(code, s, priv):
    note = s["note"]
    if is_stock(s):
        return None, "この事故の物でない（イメージ）"
    if code.startswith(("S", "H")):
        m = re.search(r"・((?:19|20)\d\d)-\d\d", note)
        if not m:
            raise SystemExit(f"🔴 {code}: 頁の注に撮影の年月が無い（{note}）")
        return int(m.group(1)), f"{'研究院' if code[0] == 'S' else '歴史編纂院'}の頁の注「{m.group(0)[1:]}」（sources23 の note）"
    t = priv.get(code, {}).get("title", "")
    if t.startswith("19950629") or t.startswith("1995년 6월 29일"):
        return 1995, f"Commons の題が「{t[:8] if t[0] == '1' and t[4] != '년' else t[:12]}」で始まる（本部の崩壊の写真の連番）"
    if code == "C2K001":
        return 1995, ("写っているのは崩壊の現場の救助（担架を運ぶ人）＝1995年。題の「2000年代初頭」と EXIF の撮影日 2001-03-02 は"
                      "写真の中身と合わない＝写真をまとめた時期と走査の日と推定（10-18 Commons の API・焼いた絵で確かめる）")
    if s["rights"] == OWN:
        return 1995, "Commons に撮影日の記載なし（説明は Sampoong Department Store Collapse・EXIF なし）＝写っている崩壊直後の現場と救助から1995年"
    raise SystemExit(f"🔴 {code}: 撮影年の出どころが決められない（題「{t}」）")


def screen_credit(code, s, cuts_rows, mask):
    """画面の出典の行＝一覧（了承②）の credit の欄から。研究院は「改変：切出」（全面と額の中の寄りで端を切る）・モザイクは「顔にモザイク」"""
    cr = {r["credit"] for r in cuts_rows}
    if len(cr) != 1:
        raise SystemExit(f"🔴 {code}: 同じ素材の出典の行が一覧で {len(cr)} 通り（{cr}）")
    cr = cr.pop()
    r = s["rights"]
    if r == OWN:
        if cr != "写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0":
            raise SystemExit(f"🔴 {code}: 個人名義の出典の行が一覧の形と違う（{cr}）")
        return f"写真：{AUTHOR}（CC BY-SA 4.0）"
    if code in MASKED_BEFORE:
        if "改変：顔と名前にモザイク" not in cr:
            raise SystemExit(f"🔴 {code}: 隠した版なのに出典の行に改変の表示が無い（{cr}）")
        return cr
    mod = []
    if code.startswith("S"):
        mod.append("切出")
    if mask:
        mod.append("顔にモザイク")
    return cr + (f"・改変：{'・'.join(mod)}" if mod else "")


def who_of(code, s):
    r = s["rights"]
    return {"A（公共ヌリ第1類型＋CC BY 4.0）": "ソウル研究院（서울연구데이터서비스）",
            "A（公共ヌリ第1類型）": "ソウル歴史編纂院",
            "BY-SA 4.0（本部）": "ソウル特別市 消防災難本部",
            OWN: "作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`）"}.get(
        r, "投稿者（クレジットは任意＝書かない）" if is_stock(s) else None)


# ── 写真の束 ───────────────────────────────────────────────
def _to_srgb(im):
    """色の札が sRGB でなければ sRGB の RGB に直す（CMYK の札＝歴史編纂院も）。戻り＝(絵, 何をしたか)"""
    from PIL import ImageCms
    icc = im.info.get("icc_profile")
    if not icc:
        if im.mode == "CMYK":
            raise SystemExit("🔴 CMYK なのに色の札が無い（写し方が決められない）")
        return im.convert("RGB"), "札なし（sRGB と読む）"
    src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
    desc = ImageCms.getProfileDescription(src).strip()
    if im.mode != "CMYK" and (desc.startswith("sRGB") or desc == "c2"):
        return im.convert("RGB"), f"札 {desc}（sRGB のまま）"
    out = ImageCms.profileToProfile(im, src, ImageCms.createProfile("sRGB"), renderingIntent=1, outputMode="RGB")
    return out, f"{im.mode} 札 {desc} → sRGB"


def mosaic(im, boxes, n):
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）＝16本目・20本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def cmd_build():
    from PIL import Image, ImageOps
    src, fet, priv, masks, rows = _sources(), _fetched(), _private(), _masks(), _list()
    by_cut = {}
    for r in rows:
        by_cut.setdefault(r["code"], []).append(r)
    db, bad = {}, 0
    (EPD / "stock").mkdir(exist_ok=True)
    for code, cuts in sorted(uses().items()):
        s = src[code]
        f, sp = fet.get((code, s["file"])), HERE / s["file"]
        if not f or not sp.exists():
            print(f"🔴 {code}: fetch23.tsv の行か手元のファイルが無い（{s['file']}）")
            bad += 1
            continue
        if md5(sp) != f["md5"]:
            print(f"🔴 {code}: {sp.name} の md5 が取得のときと違う（取り直す）")
            bad += 1
            continue
        name = name_of(code, s)
        dst = EPD / f"{name}.jpg"
        notes, box_m = [], []
        if is_stock(s):
            # 🔴 イメージ＝取ったファイルそのまま（向きの札 1・色の札なし・幅 1920 を確かめてから写す）＝焼くときに直リンクから取り直せる
            with Image.open(sp) as im0:
                ori, icc, (w, h) = im0.getexif().get(274), im0.info.get("icc_profile"), im0.size
            if (ori not in (None, 1)) or icc or w > BUNDLE_W or h > BUNDLE_H * 2:
                print(f"🔴 {code}: イメージの札・寸法がそのまま使える形でない（向き {ori}・色の札 {'あり' if icc else 'なし'}・{w}x{h}）")
                bad += 1
                continue
            shutil.copyfile(sp, dst)
            notes.append(f"取ったファイルそのまま（{w}x{h}・向きの札 {ori}・色の札なし）")
        else:
            with Image.open(sp) as im0:
                ori = im0.getexif().get(274)
                im = ImageOps.exif_transpose(im0)
                if ori and ori != 1:
                    notes.append(f"EXIF の向き {ori} を当てた（生の絵 {im0.size[0]}x{im0.size[1]}）")
                im.info["icc_profile"] = im0.info.get("icc_profile")
                im, how_c = _to_srgb(im)
            notes.append(how_c)
            w1, h1 = im.size
            k = min(1.0, max(BUNDLE_W / w1, BUNDLE_H / h1))
            if k < 1.0:
                im = im.resize((round(w1 * k), round(h1 * k)), Image.LANCZOS)
                notes.append(f"縮小 {w1}x{h1}→{im.size[0]}x{im.size[1]}")
            if code in masks:
                box_m = [(round(x0 * k), round(y0 * k), round(x1 * k), round(y1 * k), why) for x0, y0, x1, y1, why in masks[code]]
                im = mosaic(im, box_m, MOSAIC_PX)
                notes.append(f"顔だけモザイク {len(box_m)}か所（升 {MOSAIC_PX}px・mask23.tsv）")
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        y, ywhy = year_of(code, s, priv)
        r = s["rights"]
        lic = LIC.get(r)
        if not lic:
            print(f"🔴 {code}: 権利の記号が読めない（{r}）")
            bad += 1
            continue
        if r == OWN and not priv.get(code, {}).get("artist"):
            print(f"🔴 {code}: 個人名義なのに git の外の表に作者欄が無い")
            bad += 1
        cr = screen_credit(code, s, by_cut[code], bool(box_m))
        frame = r.startswith(FRAME_RIGHTS)
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(cuts), credit=cr, who=who_of(code, s), note=s["note"][:200],
                        box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h, md5=md5(dst), src_md5=f["md5"],
                        lic=lic, frame=frame, ground=r, url=s["page"], blur=[], how="・".join(notes), year=y, year_why=ywhy,
                        stock=is_stock(s), quote_page=False, named=r == OWN,
                        mosaic=[list(b[:4]) for b in box_m] or None, masked_before=MASKED_BEFORE.get(code))
        if is_stock(s):
            db[name]["media"] = s["media"]            # 🔴 焼くときに取り直す直リンク（footage.stock_photos が md5 を照らす）
        print(f"✓ {code:7} {name:26} {w}x{h:<5} {' '.join(cuts):10} {lic}{'  額装だけ' if frame else ''}  {'・'.join(notes)}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    print(f"→ ref/ep23/assets.json（{len(db)}点・額装だけ {sum(1 for r in db.values() if r['frame'])}・イメージ "
          f"{sum(1 for r in db.values() if r['stock'])}・名前を足す点 {sum(1 for r in db.values() if r['named'])}・モザイク "
          f"{sum(1 for r in db.values() if r['mosaic'] or r['masked_before'])}・束の大きさ {tot / 1e6:.1f}MB）")
    return 1 if bad else 0


def cmd_panel():
    """ルール 0b-34②：PANEL_AR＝束の縦横比の並びで、16:9 より縦長の側のいちばん大きな切れ目の中点。"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    ars = sorted((r["w"] / r["h"], n, r["w"]) for n, r in db.items() if not Path(n).name.startswith("fb_"))
    for a, n, w in ars:
        print(f"  {a:6.3f}  {n:30} 幅 {w}{'  （1280 未満＝kind() は額装）' if w < 1280 else ''}")
    side = [x for x in ars if x[0] < 16 / 9]
    gaps = sorted(((side[i + 1][0] - side[i][0], side[i], side[i + 1]) for i in range(len(side) - 1)), reverse=True)
    for g, a, b in gaps[:4]:
        print(f"切れ目 {g * 100:5.1f}ポイント：{a[0]:.3f}（{a[1]}）→ {b[0]:.3f}（{b[1]}）＝中点 {(a[0] + b[0]) / 2:.4f}")
    return 0


def cmd_edges():
    """束の全点の四辺の暗い帯（門番 check_photo_edge.margins と同じ物差し）＝スライドの台紙の縁がある写真の名簿を決める"""
    sys.path.insert(0, str(HERE / "tools"))
    import check_photo_edge as PE
    db = json.loads(DB.read_text(encoding="utf-8"))
    hits = []
    for n in sorted(db):
        m = PE.margins(f"ep23/{n}.jpg")
        mx = max(m.values())
        flag = "🔴" if mx >= PE.MIN_EDGE else ("・" if mx > 0 else " ")
        if mx > 0:
            hits.append((n, m))
        print(f"{flag} {n:30} 左 {m['l'] * 100:4.1f}% 上 {m['t'] * 100:4.1f}% 右 {m['r'] * 100:4.1f}% 下 {m['b'] * 100:4.1f}%")
    big = [n for n, m in hits if max(m.values()) >= PE.MIN_EDGE]
    print(f"→ 暗い帯のある点 {len(hits)}（うち {PE.MIN_EDGE * 100:.1f}% 以上 {len(big)}＝{' '.join(big) or 'なし'}）")
    return 0


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
def cmd_credits(write=False):
    """撮影年＝year_of（出どころつき）。当てたカットの副題が名乗る年（「NNNN年」・「当日」＝1995）と食い違えば止める"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    cj, rows, bad = {}, [], 0
    for n, r in sorted(db.items()):
        cuts = r["cut"].split()
        claims = set()
        for c in cuts:
            claims |= {int(y) for y in re.findall(r"(1[89]\d\d|20\d\d)年", subs.get(c, ""))}
            if "当日" in subs.get(c, ""):
                claims.add(EVENT_YEAR)
        y = r["year"]
        if claims and (y is None or claims != {y}):
            print(f"🔴 {n}: 副題の年 {sorted(claims)} と撮影年 {y} が食い違う（{' '.join(cuts)}）")
            bad += 1
        if re.search(r"[가-힣]", r["credit"].replace("서울연구데이터서비스", "")):
            print(f"🔴 {n}: 画面の出典の行に名前らしいハングルが残る（{r['credit']}）＝名前は印 {AUTHOR} で")
            bad += 1
        cj[f"ep23/{n}.jpg"] = r["credit"]
        gk = "イメージ" if r["stock"] else re.match(r"A|BY-SA", r["ground"]).group(0)
        mod = "・顔にモザイク" if r.get("mosaic") else ("・顔と名前にモザイク（隠した版）" if r.get("masked_before") else "")
        rows.append(f"| `{Path(n).name}` | {' '.join(cuts)} | {y if y else '不明'} | {r['lic']}（{gk}{mod}） | {r['who']} | {r['url']} |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真 {len(cj)}点{'' if not bad else f'・🔴 {bad}'}")
    if bad:
        return 1
    if not write:
        return 0
    CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    film_rows = []
    if CLIPS.exists():
        cl = json.loads(CLIPS.read_text(encoding="utf-8"))
        lst = _list()
        for k, v in cl.items():
            film_rows.append(f"| `{k}` | {' '.join(sorted({r['cid'] for r in lst if r['code'] == k}))} | {v['credit']} | {v['license']} | {v['url']} |")
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-10-18（⑤b-2）。`qa_out/ep23_assets.py credits --write` が書く（手で直さない）。旧版の節は上の「三豊百貨店崩壊事故（1995-06-29・10本目）」＝直さない。",
        "写真は映像方針の一覧 `ref/ep23/eizou_list23.md`（了承② 2026-10-18）。この事故の動く映像は使わない（写真の動きだけ）。",
        "",
        "### 0. フリー素材の映像（イメージ・この事故の物でない・音はすべて使わない＝`-an`）",
        "- Pexels・Pixabay（生成AI は使わない＝Pexels は規約で投稿を認めない）。画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」"
        "「イメージ（Pixabay）」だけ（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない",
        "- 🔴 映像そのものも、ひかえの静止画も git に入れない（19本目 決め⑨）。焼くときに台帳 `ref/ep23/clips.json` の `media` から取る",
        "",
        "| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |",
        "|---|---|---|---|---|", *film_rows, "",
        "### 1. 写真（ソウル研究院・ソウル歴史編纂院・Commons〈ソウル特別市 消防災難本部・個人名義〉・イメージ）",
        "- 束＝元の画像（git の外）の長辺を幅 2400／高さ 1350 まで縮めただけ（色・切り口はそのまま）。歴史編纂院の8点は CMYK＝色の札で sRGB に写した（技術の変換）",
        "- ソウル研究院（서울연구데이터서비스）＝公共ヌリ第1類型＋CC BY 4.0（頁の「이용목적」で 상업적 활용 を選んで 1600px を取った）。全面と額の中の寄りで"
        "端を切る＝画面の出典に「改変：切出」",
        "- ソウル歴史編纂院＝公共ヌリ第1類型（頁の「자료 이용 조건 동의서」で商業の出版・出典を書くことに同意）。幅1000未満＝額装（額の中で寄る）",
        "- 🔴 **CC BY-SA 4.0（ソウル特別市 消防災難本部・個人名義）は額装だけ**（了承② 決め3＝高さいっぱいの額装・寄り0・色は原本・上に重ねない・"
        "額ごと動かす・1点1カット＝`cuts/ss.check_frame_only`・サムネに使わない）",
        "- 🔴 **個人名義の10点は画面の出典の行に作者欄の名前**（了承② 決め4＝クレジット A）。名前はこのリポに書かない（10-17「名前0」）＝"
        "`ref/ep23/credits.json` は印 `{作者}` だけ・焼くときに git の外の表から足す（`tools/scene_jiko.ep23_credit`）。名前は各行の Commons の頁の作者欄",
        "- 顔だけモザイク（了承② 決め2）＝研究院 52400（右を歩く男性）・歴史編纂院 077（写真展を見る男性と子ども）＝元の画像を直した"
        "（`cuts/ss.NEEDS_MASK`・`ref/ep23/masked.json`）。歴史編纂院 104（行方を探す掲示板）は10本目に顔と名前を隠した版",
        "- イメージ（Pexels の写真8点）＝`ep23/stock/` の名・画面の左上に「イメージ」・20% に数えない・git に入れない（焼くときに取り直して md5 を照らす）",
        "- 撮影年＝本部の写真は Commons の題（「19950629…」）・研究院と歴史編纂院は頁の注・個人名義は Commons に撮影日の記載なし＝写っている"
        "崩壊直後の救助から1995年（`qa_out/ep23_assets.py` の year_of＝出どころつき）",
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


# ── フリー素材の映像（台帳・ショット・ひかえ・USE） ─────────────
def _film_codes():
    """フリー素材の映像の記号 → 使うカット（一覧の順）"""
    src = _sources()
    out = {}
    for r in _list():
        c = r["code"]
        if c and src.get(c, {}).get("file", "").lower().endswith(".mp4"):
            out.setdefault(c, []).append(r["cid"])
    return out


def _cand_title(media):
    for ln in CAND.read_text(encoding="utf-8").splitlines():
        f = ln.split("|")
        if len(f) >= 8 and f[5] == media and not f[7].startswith("❌"):
            return f[7].split("（")[0]
    return ""


def _probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,sample_aspect_ratio:format=duration", "-of", "json", str(p)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode:
        raise SystemExit(f"🔴 ffprobe が読めない：{p}（{r.stderr[-200:]}）")
    j = json.loads(r.stdout)
    st = j["streams"][0]
    a, b = st["r_frame_rate"].split("/")
    return dict(w=int(st["width"]), h=int(st["height"]), fps=round(int(a) / int(b), 3),
                sar=st.get("sample_aspect_ratio") or "1:1", sec=float(j["format"]["duration"]))


def cmd_clips():
    src, fet = _sources(), _fetched()
    out = {}
    for code, cuts in _film_codes().items():
        s = src[code]
        p = HERE / s["file"]
        f = fet.get((code, s["file"]))
        if not f or not p.exists() or md5(p) != f["md5"]:
            raise SystemExit(f"🔴 {code}: 手元の mp4 が無いか md5 が取得のときと違う（{s['file']}）")
        loc = _probe(p)
        lic = LIC[s["rights"]]
        site = "Pixabay" if "Pixabay" in lic else "Pexels"
        e = dict(url=s["page"], media=s["media"], stock=True, file=s["file"].removeprefix("ref/"), credit=f"イメージ（{site}）", src="stock",
                 at=0.0, what=_cand_title(s["media"]) or s["note"][:60], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"],
                 sec=round(loc["sec"], 3), size=int(f["bytes"]), md5=f["md5"], dispw=loc["w"], decoded=[loc["w"], loc["h"]],
                 license=lic, license_url=LIC_URL[lic], site=site)
        if s["file"].startswith("ref/stock/media/"):
            e["stock_id"] = Path(s["file"]).stem          # 共用の棚 ref/stock/stock.json の鍵
        out[code] = e
        print(f"  {code:10} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.2f}秒  {' '.join(cuts):10} {e['credit']}  {e['what'][:40]}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep23/clips.json（{len(out)}本）")
    return 0


def cmd_shots():
    """shots.json＝フリー素材の映像のショットの境目（tools/shots.shots_of＝1秒1コマの差）。footage の門番（outside_shot・unknown_clip）が読む"""
    sys.path.insert(0, str(HERE / "tools"))
    import shots as SH
    src = _sources()
    out = {}
    for code in _film_codes():
        s = src[code]
        sh, dur = SH.shots_of(HERE / s["file"])
        how = "1秒1コマで tools/shots.shots_of（2026-10-18 ⑤b-2・フリー素材）"
        if code in SHOT_ONE:
            sh = [dict(start=0.0, until=float(sh[-1]["until"]), motion=max(x["motion"] for x in sh))]
            how += f"・🔧 1ショットに直した（{SHOT_ONE[code]}）"
        out[code] = dict(src=s["media"], scan=s["file"], dur=round(dur, 1), how=how, shots=sh)
        print(f"  {code:10} {dur:6.1f}秒  ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep23/shots.json（{len(out)}本）")
    return 0


# 🔴 動きの速い・ゆっくり流れる素材は、隣の1秒の差がしきい値を超えて「境目」が出る（18本目 0b-45⑥）＝前後のコマを並べて見て1ショットに直す（根拠つき）
SHOT_ONE = {
    "Xc613a": "10秒の境目の前後 9.2秒・10.8秒のコマを並べて見た＝同じ工事中の建物を回り込むドローンの続き（光も建物も同じ・切り替わりでない）",
    "Xc712a": "5秒の境目の前後 4.4秒・5.6秒のコマを並べて見た＝錆びた鉄筋の網の上をゆっくり動く続き（切り替わりでない）",
}
# 中身の切り口（全画面・寄り）。🔴 字を外す寄せはカットごと（GEOM_CUT）＝使う区間のコマを見て決める
GEOM = dict(full=True, zoom=1.0)
GEOM_CUT = {
    # c308（図面の映像）：左の紙に大きな薄い英字「…tructures B…」が区間じゅう出る（1・6.4・11.5・16.6・21.5秒のコマ＝右の端は x 約880〜900）
    #   ＝右へ寄せて寄り 1.9（見える幅 1010px＝x 910〜1920）・縦はやや下（三角定規と表の側）。⚠️ 焼いた絵で英字の端が残らないかを見る（⑤b-7）
    "c308": dict(zoom=1.9, xbias=1.0, bias=0.7),
}
EDGE_S = 0.3                   # ショットの境目から離す秒（境目のなじみのコマを使わない）


def _need():
    """{cid: 映像が要る秒}＝footage.secs_of（扉を除いた中身の秒）。🔴 SPEC に `ss.vid` を書いたのに USE がまだ空のあいだは章ファイルが
    読めない（ss.vid がひかえを開けない）＝一覧の cont（make_list23.py が同じ式で narration.json から出した秒）で受け、USE を書いたあとに
    もう一度 `use` を回して本物の秒と同じ行になるかを見る"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    try:
        return FO.secs_of()
    except Exception as e:                                    # noqa: BLE001
        print(f"・章ファイルが読めない（{type(e).__name__}: {str(e)[:80]}）＝一覧の cont の秒で受ける（USE を書いたあと `use` をもう一度）")
        return {r["cid"]: float(r["cont"]) for r in _list() if r["cont"]}


def pick(code, need, shots):
    """等速（rate 1.0）で入る区間＝need が入るショットのうち、いちばん長いショットの真ん中。入らなければ一番長いショットで倍率を下げる"""
    best = max(shots, key=lambda x: x["until"] - x["start"])
    room = best["until"] - best["start"] - 2 * EDGE_S
    if room >= need:
        a = round(best["start"] + EDGE_S + (room - need) / 2, 2)
        return a, round(a + need + 0.05, 2), 1.0, best
    a = round(best["start"] + EDGE_S, 2)
    return a, round(best["until"] - EDGE_S, 2), min(1.0, int(room / need * 100) / 100), best


WINDOW = {}                    # カット → (始め, 終わり)＝pick を使わずに決めた区間（字を外す・絵を選ぶ）


def _window(cid, code, need, shots):
    if cid in WINDOW:
        a, b = WINDOW[cid]
        sh = [x for x in shots if x["start"] <= a < x["until"]][0]
        return a, b, min(1.0, int((b - a) / need * 100) / 100), sh
    return pick(code, need, shots)


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）＝区間の頭の1コマを焼くときと同じ切り口（全画面・寄り）で 1920×1080"""
    from PIL import Image
    shots = json.loads(SHOTS.read_text(encoding="utf-8"))
    src, secs, bad = _sources(), _need(), 0
    for code, cuts in _film_codes().items():
        for cid in cuts:
            if only and cid not in only:
                continue
            a, b, rate, sh = _window(cid, code, float(secs[cid]), shots[code]["shots"])
            p = HERE / src[code]["file"]
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-i", str(p), "-frames:v", "1",
                                  "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            if not raw:
                print(f"🔴 {cid}: コマが取れない")
                bad += 1
                continue
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            g = dict(GEOM, **GEOM_CUT.get(cid, {}))
            sw, sh_ = im.size
            z = max(1920 / sw, 1080 / sh_) * g.get("zoom", 1.0)
            cw, ch = min(sw, 1920 / z), min(sh_, 1080 / z)
            l, t = (sw - cw) * g.get("xbias", 0.5), (sh_ - ch) * g.get("bias", 0.5)
            im = im.crop((round(l), round(t), round(l + cw), round(t + ch))).resize((1920, 1080), Image.LANCZOS)
            dst = EPD / "stock" / f"fb_{cid}.jpg"
            dst.parent.mkdir(exist_ok=True)
            im.save(dst, quality=92)
            print(f"✓ {cid:5} {code:10} {a:6.2f}秒 {sw}x{sh_} → {dst.relative_to(HERE).as_posix()}")
    return 1 if bad else 0


def _write_block(tag, lines):
    txt = FOOTAGE.read_text(encoding="utf-8")
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_text(txt[:m.start(2)] + "".join(x + "\n" for x in lines) + txt[m.end(2):], encoding="utf-8")


def cmd_use():
    """footage.USE の23本目の欄（🔴 章ファイルに `ss.vid` を書いたカットだけ＝門番 slots）。等速で入る区間を選ぶ（pick）・
    入らなければ rate＝使える秒÷要る秒（切り捨て）・0.6 未満は止め絵。寄りと寄せは GEOM_CUT"""
    sys.path.insert(0, str(HERE / "tools"))
    import check_footage_slots as SL
    shots = json.loads(SHOTS.read_text(encoding="utf-8"))
    secs, want = _need(), set(SL.slots())
    lines, skip = [], []
    for code, cuts in _film_codes().items():
        for cid in cuts:
            if cid not in want:
                skip.append(cid)
                continue
            need = float(secs[cid])
            a, b, rate, sh = _window(cid, code, need, shots[code]["shots"])
            g = GEOM_CUT.get(cid, {})
            geo = "".join(f", {k}={v}" for k, v in g.items())
            where = f"ショット {sh['start']:g}〜{sh['until']:g}秒"
            if rate < STILL_BELOW:
                s0 = round((a + b) / 2, 2)
                lines.append(f'    "{cid}": dict(clip="{code}", start={s0:.2f}, still=True, until={min(b, s0 + 1.0):.2f}{geo}),   # {where}・止め絵（使える {b - a:.2f}秒／要る {need:.2f}秒）')
            else:
                lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate={rate}{geo}),   # {where}・使える {b - a:.2f}秒（{a:g}〜{b:g}）／要る {need:.2f}秒')
    _write_block("EP23_USE", lines)
    print(f"→ tools/footage.py USE {len(lines)}欄（等速でないもの {sum('rate=1.0' not in x for x in lines)}）")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルに ss.vid がまだ無い：{' '.join(skip)}")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "edges": cmd_edges, "shots": cmd_shots, "clips": cmd_clips, "use": cmd_use}
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
