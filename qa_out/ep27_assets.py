# -*- coding: utf-8 -*-
"""ep27_assets.py — 27本目（八田與一容疑者の事件）の写真の束・出典・県警の動画の台帳（⑤b-2・2026-10-30）。26本目 `ep26_assets.py` の形を、
27本目の台帳（`sources27.psv` の12列〈見出しの行で読む〉・`fetch27.tsv`〈md5 を2回・見出しは日本語〉・県警の取得の記録 `src/fetch_log.tsv`・
git の外の作者の表 `src/credits_private.tsv`〈列 code・作者＝行の鍵は sources27 の記号 CM…〉）に合わせた。頁（PDF）の道は無い（27本目は頁0）。

取得はすんでいる（映像方針＝了承②・`ref/ep27/eizou_build/fetch27.py`・記録 `fetch27.tsv`）。ここは**束を作る道**だけを持つ。
  python -P qa_out/ep27_assets.py build             # 束 ref/ep27/<名>.jpg（イメージ＝ref/ep27/stock/・県警の引用＝ref/ep27/police/）＋ 権利の台帳 ref/ep27/assets.json
  python -P qa_out/ep27_assets.py look CM045 …      # 束の写真を並べた見本（out/ep27_look/・1枚 960 幅）
  python -P qa_out/ep27_assets.py crop CM045 x0 y0 x1 y1 [倍]   # 束の画素の切り出し（原寸＝1倍・既定2倍・10px の目盛り）＝人の写りを決めるとき
  python -P qa_out/ep27_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python -P qa_out/ep27_assets.py edges             # 束の四辺の暗い帯＝門番 check_photo_edge の名簿（SLIDE_MOUNT／SLIDE_NOT_MOUNT）を決める
  python -P qa_out/ep27_assets.py credits [--write] # 画面の出典 ref/ep27/credits.json と ref/CREDITS.md の27本目の節
  python -P qa_out/ep27_assets.py stockcheck        # イメージ（Pexels）の直リンクを取り直して束と md5 が同じか（footage.stock_photos と同じ取り方）
  python -P qa_out/ep27_assets.py clips｜shots      # 県警の動画の台帳 ref/ep27/clips.json・ショットの表 ref/ep27/shots.json（YT-C は SCENES＝30コマ/秒の根拠つき）
  python -P qa_out/ep27_assets.py use [c106 c305] [--all]   # 🆕 ⑤b-3：footage.USE の EP27_USE（一覧の区間と止め＝hold・実時間）を書き出す（手で書かない）
  python -P qa_out/ep27_assets.py fb [c106 …]       # 🆕 ⑤b-3：県警の動画のひかえの静止画 ref/ep27/police/fb_<cid>.jpg（原寸・git に入れない）

🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色）＝幅 2400 か高さ 1350 の大きい方まで（小さい写真は原画のまま）。
🔴 イメージ（Pexels）＝取ったファイルそのまま（`ref/ep27/stock/`＝git に入れない＝19本目 決め⑨・焼くときに `footage.stock_photos` が台帳の
   `media`〈取ったときの直リンク〉から取り直して md5 を照らす＝23本目の型）。
🔴 県警・警察庁の引用（ポスター・似顔絵・手配の写真）＝**公開リポに置かない**（県警の頁「無断で転載することを禁じます」・大分県の頁は引用だけを
   禁止の外に置く＝引用は動画の中の主従のある使い方の話で、リポに置くのはただの複製）＝`ref/ep27/police/`（`git add` しない）・台帳の `private`。
   焼くのは Modal（保管庫 jiko-assets の `ref/ep27/police/` を clone のあとリポの同じ道へ写す＝`modal_app.pull_private`）。⚠️ Actions は保管庫を読めない。
   絵は加工しない（似顔絵の SKETCH6・SKETCH2 は並べ方だけ＝1枚ずつ縮めるだけで並べる・映像方針 sources27 の注）。
🔴 **事件の回（ルール §B2-10）**＝被害者・遺族・けがをした人・目撃者・SNS の投稿者の名前と、Commons の撮影者名を台帳・出典の行・CREDITS.md に
   書かない＝作者は印 `{作者}` だけ（焼くときに `scene_jiko._ep27_author` が git の外の表から足す）。
🔴 人の写り（了承② 決め4）＝CC BY・CC0 は顔が分かれば顔だけ升目（MASK）・**BY-SA は升目も翻案＝かけない**（遠い人と後ろ姿だけ＝使えなければ当て方を替える）。
"""
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep27"
SRC = EPD / "src"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list27.tsv"
SOURCES = BUILD / "sources27.psv"
FETCH = BUILD / "fetch27.tsv"
POLICE_LOG = SRC / "fetch_log.tsv"            # 県警・警察庁の素材の取得の記録（git の外・列＝取った日・ファイル・bytes・md5・出どころ）
PRIVATE = SRC / "credits_private.tsv"         # 🔴 git の外（作者欄）＝ここから名前を公開の物へ写さない
NAME_FILES = (SRC / "names_private.txt", SRC / "names_commons.txt")   # 🔴 git の外（出さない名前＝namecheck27 と同じ2つ）
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
SCRATCH = HERE / "out" / "ep27_look"          # look・crop の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## 八田與一容疑者の事件（2022-06-29・27本目）"
AUTHOR = "{作者}"            # CC BY・BY-SA の出典の行の印（焼くときに git の外の表から足す＝scene_jiko.ep27_credit）
EVENT_YEAR = 2022            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）
UA = "zukai-engine/1.0 (accident-documentary research; https://github.com/torotorotolo/zukai-engine)"

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 92
MOSAIC_PX = 14                         # 升目の大きさ（束の画素）
PHOTO_TYPES = ("commons-photo",)
QUOTE_TYPES = ("police-image", "npa-image", "police-frame")   # 引用の静止画（額装・加工しない・公開リポに置かない）。police-frame＝⑤b-3 の YT-A のコマ
STOCK_TYPES = ("stock",)
FILM_TYPES = ("police-video",)                       # 束に入れない（clips.json）
SAT_TYPES = ("satellite",)                           # 束に入れない（cuts/ss.SAT＝⑤b-4 で撮る）
KIND_OK = {"実写": PHOTO_TYPES, "引用": QUOTE_TYPES + FILM_TYPES, "イメージ": STOCK_TYPES, "衛星": SAT_TYPES}
PEXELS_W = 1920                        # fetch27.py finalpx の幅（直リンクの w=）

# 県警・警察庁の引用の静止画 {記号: [src からの道…]}（sources27 の file の欄は注つき・SKETCH6 は {89..94} の形＝ここに道を並べる）
POLICE_FILES = {
    "NPA01": ["police_web/npa_wanted_01.jpg"],
    "XPOST1": ["police_x/x20260629_HL8dC-vaIAAXBRK.jpg"],
    "SKETCH6": [f"police_web/2323829_46348{n}_misc.jpeg" for n in range(89, 95)],
    "SKETCH2": ["police_web/2323829_4634890_misc.jpeg", "police_web/2323829_4634891_misc.jpeg"],
    # 🆕 ⑤b-3（10-30 カズヤくん了承）：YT-A（取れない＝403）の代わりに、映像方針（10-29）で内蔵ブラウザの再生画面の中から写した 1080p のコマ
    #    （取り直しではない）を静止の引用に＝c102・c309・c303・c316。コマの秒は sources27 の get（frame:YT-A@秒）＝門番 make_list27 が BAD と照らす
    "YTA026": ["police_yt/ytA_frames/A_0026.00.jpg"],
    "YTA034": ["police_yt/ytA_frames/A_0034.00.jpg"],
    "YTA094": ["police_yt/ytA_frames/A_0094.00.jpg"],
    "YTA165": ["police_yt/ytA_frames/A_0165.00.jpg"],
}
XPOST1_MD5 = "bcfefe8dac139b9cf3ab4792f00e2763"      # X の画像は fetch_log の外（映像方針で取った・sources27 の注「md5 bcfefe8d」）
# YT-A のコマも fetch_log の外＝md5 は映像方針の見た記録（`src/seen_log.tsv` の 8・9・11・13 行＝頭12字）と同じ全桁（⑤b-3 で取り直して照らした）
FRAME_MD5 = {"YTA026": "a366365f6837861f9c56a092f3557037", "YTA034": "895680381b0e17185cafbb9cd41848cb",
             "YTA094": "26cd8c43c924ef9a5750742a08915ecb", "YTA165": "bae262202824d34316afde9bede1ad00"}
# 似顔絵を並べる形（列・行）。絵は1枚ずつ同じ倍率で縮めるだけ・すき間は無地（絵の外）
SKETCH_GRID = {"SKETCH6": (3, 2), "SKETCH2": (2, 1)}
SKETCH_H = 1200                        # 似顔絵1枚の高さ（束の画素）＝額の高さ 1080 より大きい（寄りの余地）
SKETCH_GAP = 36
SKETCH_BG = (40, 40, 40)

# 顔だけ升目 {記号: [(x0, y0, x1, y1, 誰)]}（束の画素）＝⑤b-2（10-30）に束を2倍の切り出しと 10px の目盛りで見て決めた（CC BY・CC0 だけ・
#   scratchpad `pp_a〜pp_c.jpg`・`out/ep27_look/crop_cm044_1300_2170.jpg`）。顔が約20〜35px で分かる私人だけ
#   ✕ 升目にしない（原寸で見た）：CM045 の商店街の奥の2人（顔 約10px）／CM154 の白いシャツの人（後ろ姿）・駅の入り口の人たち（顔 約10px）・
#      左のタクシーの中（暗くて分からない）／CM144 の改札の奥の人（後ろ姿）／CM044 の横断歩道の左の人たち（長い露光で流れて顔が無い）／
#      CM056・CM112 の遠くの人（数画素）
#   BY-SA（升目も翻案＝かけない）：CM022＝後ろ姿2人と顔 約15px の奥の人（額装で約10px）・CM204＝砂浜の遠くの2人（顔 数画素）・CM014＝脚と背中だけ（頭は画面の外）
#      ＝了承② 決め4「遠い人と後ろ姿だけ」のとおり＝当て方を替えない
MASK = {
    # c105（全面・寄る）・c519 の地＝JR別府駅近くの夜の通り（2022年9月）
    "CM045": [(390, 1146, 422, 1182, "コンビニの前を歩くピンクのシャツの人"), (1544, 1152, 1576, 1188, "右を歩く水色のシャツの人"),
              (1598, 1146, 1632, 1186, "右を歩く緑のシャツの人")],
    # c214（全面・寄る）・c608（右へ）＝夜の JR別府駅
    "CM154": [(1306, 1000, 1340, 1042, "右のタクシーの中の人の横顔")],
    # c204（全面・寄る＝下の通りを切り出す）・地 c201 c203 c205 c517 c518＝駅近くの夜の交差点
    "CM044": [(1640, 2226, 1672, 2262, "横断歩道を渡る黒いシャツの人")],
}
MASKED_BEFORE = {}


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _list():
    return list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))


def _sources():
    rows = [ln for ln in SOURCES.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    head = rows[0].split("|")
    if head != ["code", "type", "title", "get", "dims", "rights", "basis", "credit", "era", "people", "file", "note"]:
        raise SystemExit(f"🔴 sources27.psv の見出しの行が変わった：{rows[0][:120]}")
    out = {}
    for ln in rows[1:]:
        f = ln.split("|")
        if len(f) != 12:
            raise SystemExit(f"🔴 sources27.psv の行の欄が12でない：{ln[:80]}")
        out[f[0]] = dict(zip(head, f))
    return out


def _fetched():
    """{記号: 行}（fetch27.tsv＝取った日・記号・種類・bytes・md5・md5（読み直し）・ファイル・出どころ）。本番の取得（final・finalpx）だけ。
    Pexels の記号は「番号:ファイル名」＝PX<番号> に読み替える"""
    out = {}
    for r in csv.DictReader(FETCH.open(encoding="utf-8"), delimiter="\t"):
        k = r.get("記号") or ""
        if r.get("種類") == "final":
            out[k] = r
        elif r.get("種類") == "finalpx":
            pid, fname = k.split(":", 1)
            out[f"PX{pid}"] = dict(r, pid=pid, fname=fname)
    return out


def _police_log():
    """{src からの道: md5}（県警・警察庁の取得の記録）"""
    out = {}
    for r in csv.DictReader(POLICE_LOG.open(encoding="utf-8"), delimiter="\t"):
        if r.get("ファイル"):
            out[r["ファイル"]] = r["md5"]
    return out


def _private():
    """git の外の作者の表 {記号: 作者}。無ければ止める（束を作る手元だけで読む）"""
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の作者欄の表）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    return {r[0]: r[1] for r in rows[1:] if len(r) >= 2}


def _fold(s):
    """当てる側の形＝NFKC・小文字・空白は1つの空白に"""
    return " ".join(unicodedata.normalize("NFKC", s or "").lower().split())


def _mask_word(w):
    return w[0] + "○" * (len(w) - 1)


def _name_re(n):
    """名前1つの当て方。英字＝語の境で（語と語のあいだは空白の有無を問わない）・かなと漢字＝そのまま"""
    n = _fold(n)
    if re.search(r"[a-z]", n):
        return re.compile(r"(?<![a-z0-9])" + r"\s*".join(re.escape(p) for p in n.split()) + r"(?![a-z0-9])")
    return re.compile(re.escape(n.replace(" ", "")))


def _names():
    """git の外の出さない名前 [(伏せた形, 当て方)]（2字以上）＋作者の表の名前。無ければ止める（fail closed）"""
    out = []
    for p in NAME_FILES:
        if not p.exists():
            raise SystemExit(f"🔴 {p.relative_to(HERE).as_posix()} が無い（git の外の名前の表）")
        for ln in p.read_text(encoding="utf-8").splitlines():
            n = ln.strip()
            if n and not n.startswith("#") and len(n) >= 2:
                out.append((_mask_word(n.replace(" ", "")), _name_re(n)))
    for who in _private().values():
        w = " ".join(who.split())
        if len(w) >= 2:
            out.append((_mask_word(w.replace(" ", "")), _name_re(w)))
    if not out:
        raise SystemExit("🔴 名前の表が空（fail closed）")
    return out


def hits_in(text, names):
    t = _fold(text)
    return [w for w, rx in names if rx.search(t)]


def _code_of(main):
    """一覧の素材の欄（CM044:通り のように寄りの名がつく）→ 記号"""
    return (main or "").split(":", 1)[0].strip()


def uses():
    """{記号: dict(main=[カット], ji=[カット])}（束に入る写真・イメージ・引用の静止画）。一覧の種類と出どころの型が食い違えば止める。
    地（説明カットの地の写真＝了承② 決め1）は CC BY・CC0 だけ（BY-SA は暗くするのも翻案）"""
    src = _sources()
    out, bad = {}, []
    for r in _list():
        cid = r["cid"]
        c = _code_of(r["main"])
        if c:
            s = src.get(c)
            if not s:
                bad.append(f"{cid} {c}: 出どころの表に無い")
            elif r["kind"] in KIND_OK and s["type"] not in KIND_OK[r["kind"]]:
                bad.append(f"{cid} {c}: 一覧の種類「{r['kind']}」と出どころの型 {s['type']} が食い違う")
            elif r["kind"] not in KIND_OK:
                bad.append(f"{cid} {c}: 図の型「{r['kind']}」の素材の欄に記号がある（地は ji の欄）")
            elif s["type"] in PHOTO_TYPES + QUOTE_TYPES + STOCK_TYPES:
                out.setdefault(c, dict(main=[], ji=[]))["main"].append(cid)
        j = _code_of(r["ji"])
        if j:
            s = src.get(j)
            if not s or s["type"] not in PHOTO_TYPES:
                bad.append(f"{cid} {j}: 地の写真が Commons の写真でない（{s['type'] if s else '表に無い'}）")
            elif "BY-SA" in s["rights"]:
                bad.append(f"{cid} {j}: 地の写真が BY-SA（{s['rights']}）＝暗くするのも翻案（了承② 決め1＝CC BY・CC0 だけ）")
            else:
                out.setdefault(j, dict(main=[], ji=[]))["ji"].append(cid)
    if bad:
        raise SystemExit("🔴 " + "\n🔴 ".join(bad))
    return out


def bundle_name(code, s):
    if s["type"] in STOCK_TYPES:
        return f"stock/{code.lower()}"
    if s["type"] in QUOTE_TYPES:
        return f"police/{code.lower()}"
    return code.lower().replace("-", "_")


# ── 写真 ───────────────────────────────────────────────────────
def _shrink(im):
    from PIL import Image
    w1, h1 = im.size
    k = min(1.0, max(BUNDLE_W / w1, BUNDLE_H / h1))
    if k < 1.0:
        im = im.resize((round(w1 * k), round(h1 * k)), Image.LANCZOS)
    return im, k


def _to_srgb(im):
    """色の札が sRGB でなければ sRGB の RGB に直す。戻り＝(絵, 何をしたか)"""
    import io
    from PIL import ImageCms
    icc = im.info.get("icc_profile")
    if not icc:
        return im.convert("RGB"), "札なし（sRGB と読む）"
    src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
    desc = ImageCms.getProfileDescription(src).strip()
    if im.mode != "CMYK" and (desc.startswith("sRGB") or desc == "c2"):
        return im.convert("RGB"), f"札 {desc}（sRGB のまま）"
    if im.mode in ("L", "LA", "I", "I;16", "1") and (src.profile.xcolor_space.strip() == "GRAY" or "sRGB" in desc):
        return im.convert("L").convert("RGB"), f"{im.mode} 灰色の絵・札 {desc} → 灰色のまま RGB"
    out = ImageCms.profileToProfile(im, src, ImageCms.createProfile("sRGB"), renderingIntent=1, outputMode="RGB")
    return out, f"{im.mode} 札 {desc} → sRGB"


def load_photo(path):
    """元の写真を読む（向きの札を当て・sRGB に）＝(絵, 記録の言葉の並び)"""
    from PIL import Image, ImageOps
    notes = []
    with Image.open(path) as im0:
        ori = im0.getexif().get(274)
        im = ImageOps.exif_transpose(im0)
        if ori and ori != 1:
            notes.append(f"EXIF の向き {ori} を当てた（生の絵 {im0.size[0]}x{im0.size[1]}）")
        im.info["icc_profile"] = im0.info.get("icc_profile")
        im, how_c = _to_srgb(im)
    notes.append(how_c)
    return im, notes


def mosaic(im, boxes, n):
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）＝16・17・20・23・25・26本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def _src_path(s):
    """sources27 の file の欄（注つき「…（取得ずみ）」）の頭の道だけ＝ref/ep27 からの道"""
    m = re.match(r"(src/[^（\s|]+?\.(?:jpe?g|png|mp4))", s["file"])
    return EPD / m.group(1) if m else None


def _src_ok(code, s, fet):
    """手元の元のファイルが取得の記録（md5 を2回＝同じ）と同じか。違えば止める"""
    p = _src_path(s)
    if not p or not p.exists():
        raise SystemExit(f"🔴 {code}: 手元のファイルが無い（{s['file']}）")
    r = fet.get(code)
    if not r:
        raise SystemExit(f"🔴 {code}: 取得の記録が無い（fetch27.tsv の final／finalpx）")
    h = md5(p)
    if r["md5"] != r["md5（読み直し）"] or h != r["md5"] or (EPD / r["ファイル"]).resolve() != p.resolve():
        raise SystemExit(f"🔴 {code}: {p.name} の md5 が fetch27.tsv と合わない（取り直す）")
    return p, h


def _police_ok(code):
    """県警・警察庁の素材の道と md5（取得の記録と照らす）"""
    log = _police_log()
    out = []
    for rel in POLICE_FILES[code]:
        p = SRC / rel
        if not p.exists():
            raise SystemExit(f"🔴 {code}: 手元のファイルが無い（src/{rel}）")
        h = md5(p)
        want = log.get(rel) or (XPOST1_MD5 if code == "XPOST1" else FRAME_MD5.get(code))
        if h != want:
            raise SystemExit(f"🔴 {code}: src/{rel} の md5 {h[:8]} が取得の記録 {str(want)[:8]} と合わない")
        out.append((p, h))
    return out


def sketch_sheet(code, files):
    """似顔絵を並べた1枚（絵は1枚ずつ同じ高さに縮めるだけ＝加工しない・すき間は無地）"""
    from PIL import Image
    cols, rows = SKETCH_GRID[code]
    ims = []
    for p, _ in files:
        with Image.open(p) as im0:
            im = im0.convert("RGB")
        k = SKETCH_H / im.height
        ims.append(im.resize((round(im.width * k), SKETCH_H), Image.LANCZOS))
    cw = max(i.width for i in ims)
    W = cols * cw + (cols + 1) * SKETCH_GAP
    H = rows * SKETCH_H + (rows + 1) * SKETCH_GAP
    sheet = Image.new("RGB", (W, H), SKETCH_BG)
    for i, im in enumerate(ims):
        c, r = i % cols, i // cols
        sheet.paste(im, (SKETCH_GAP + c * (cw + SKETCH_GAP) + (cw - im.width) // 2, SKETCH_GAP + r * (SKETCH_H + SKETCH_GAP)))
    return sheet


_YEAR = re.compile(r"((?:19|20)\d\d)年")


def year_of(code, s):
    if s["type"] in STOCK_TYPES:
        return None, "この事件の物でない（イメージ）"
    m = _YEAR.search(s["era"])
    if m:
        return int(m.group(1)), f"sources27.psv の時期の欄「{s['era'][:24]}」（映像方針＝Commons の頁の撮影日・県警の頁と動画の公開日）"
    return None, f"撮影の年の出どころが無い（時期の欄「{s['era']}」）"


def screen_credit(code, s, face_mask):
    """画面の出典の行（了承② 決め4）＝sources27 の出典の欄（CC BY・BY-SA は「写真：{作者}／Wikimedia Commons（ライセンス）」・
    CC0＝「Wikimedia Commons（CC0）」・Pexels＝「イメージ（Pexels）」・県警＝「出典：大分県警察 …」）＋**改変の断りを明記**：
    BY-SA＝「／改変なし」（額装・無加工）・CC BY＝「／改変：切出」（全面＝画面の窓で切る）・顔だけ升目は「・顔にモザイク」を足す。
    🔴 ⑤b-2 の試し焼き（10-30）で見つけた：断りを書かないと `scene_jiko.credit_of` が「CC BY」を含み「改変」の無い行に古い決まり（6本目＝
       デュオトーンの頃）の「／改変：色調変更・切出」を足す＝**原色のまま・切らない BY-SA の額にも「色調変更・切出」と出ていた**（c101）。
       24・25本目と同じく断りを台帳に書く（色は変えていない＝「色調変更」は書かない）"""
    cr = s["credit"]
    if "［" in cr or "（⑤b" in cr:
        raise SystemExit(f"🔴 {code}: 出典の欄に書きかけの印が残る（{cr[:60]}）")
    if face_mask and (s["type"] not in PHOTO_TYPES or "BY-SA" in s["rights"]):
        raise SystemExit(f"🔴 {code}: 顔の升目は CC BY・CC0 の写真だけ（{s['rights']}＝BY-SA は升目も翻案）")
    if s["type"] in PHOTO_TYPES and "CC BY" in s["rights"]:
        cr = re.sub(r"／改変：.*$", "", cr)                    # sources27 の「／改変：切り出し」（CM044）は下の型に揃える
        if "BY-SA" in s["rights"]:
            cr += "／改変なし"
        else:
            cr += "／改変：切出" + ("・顔にモザイク" if face_mask else "")
    elif face_mask:
        cr += "／改変：顔にモザイク"
    return cr


def who_table(code, s):
    """CREDITS.md の撮影者の欄（名前は書かない）"""
    t, r_ = s["type"], s["rights"]
    if t in PHOTO_TYPES and r_.startswith("CC BY"):
        return "Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す）"
    if t in PHOTO_TYPES:
        return "Commons の投稿者（CC0＝表示は任意）"
    if t in STOCK_TYPES:
        return "投稿者（クレジットは任意＝書かない）"
    if t == "npa-image":
        return "警察庁の重要指名手配の頁（写真は大分県警察＝第三者の権利）"
    if t == "police-frame":
        return "大分県警察（公式 YouTube の手配の動画の1コマ）"
    return "大分県警察"


def _lic(s):
    t, r_ = s["type"], s["rights"]
    if t in STOCK_TYPES:
        return "Pexels License（イメージ）"
    if t in QUOTE_TYPES:
        return "引用（著作権法32条・大分県の頁が引用を禁止の外に置く）"
    return r_


# ── 束を作る ─────────────────────────────────────────────────
def cmd_build():
    from PIL import Image
    src, fet = _sources(), _fetched()
    db, bad = {}, 0
    us = uses()
    for code in MASK:
        if code not in us:
            print(f"🔴 MASK の {code} は一覧で使っていない")
            bad += 1
    for d in ("stock", "police"):
        (EPD / d).mkdir(exist_ok=True)
    for code, u in sorted(us.items()):
        s = src[code]
        name = bundle_name(code, s)
        dst = EPD / f"{name}.jpg"
        t = s["type"]
        box_m = MASK.get(code, [])
        extra = {}
        if t in STOCK_TYPES:
            # 🔴 イメージ＝取ったファイルそのまま（向きの札 1・色の札なし）＝焼くときに直リンクから取り直せる（footage.stock_photos が md5 を照らす）
            p, smd5 = _src_ok(code, s, fet)
            with Image.open(p) as im0:
                ori, icc, (w, h) = im0.getexif().get(274), im0.info.get("icc_profile"), im0.size
            if ori not in (None, 1) or icc or w > BUNDLE_W:
                print(f"🔴 {code}: イメージの札・寸法がそのまま使える形でない（向き {ori}・色の札 {'あり' if icc else 'なし'}・{w}x{h}）")
                bad += 1
                continue
            shutil.copyfile(p, dst)
            r = fet[code]
            extra = dict(media=f"https://images.pexels.com/photos/{r['pid']}/{r['fname']}?auto=compress&cs=tinysrgb&w={PEXELS_W}")
            notes = ["取ったファイルそのまま（git に入れない＝焼くときに直リンクから取り直す）"]
        elif t in QUOTE_TYPES:
            files = _police_ok(code)
            smd5 = " ".join(h for _, h in files)
            if code in SKETCH_GRID:
                im = sketch_sheet(code, files)
                im.save(dst, quality=JPEG_Q, optimize=True)
                cols, rows = SKETCH_GRID[code]
                notes = [f"似顔絵 {len(files)}枚を {cols}列×{rows}行に並べた（1枚ずつ高さ {SKETCH_H}px に縮めるだけ・絵は加工しない・すき間は無地）"]
            else:
                shutil.copyfile(files[0][0], dst)
                notes = ["取ったファイルそのまま（加工しない）"]
            notes.append("🔴 公開リポに置かない（git add しない・Modal の保管庫）")
            with Image.open(dst) as im0:
                w, h = im0.size
        else:
            p, smd5 = _src_ok(code, s, fet)
            im, notes = load_photo(p)
            im, k = _shrink(im)
            if k < 1.0:
                notes.append(f"縮小 ×{k:.3f}")
            notes.append("fetch27.tsv の md5 と同じ（2回とも）")
            if box_m:
                im = mosaic(im, box_m, MOSAIC_PX)
                notes.append(f"顔だけ升目 {len(box_m)}か所（升 {MOSAIC_PX}px）")
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        y, ywhy = year_of(code, s)
        cr = screen_credit(code, s, bool(box_m))
        private = t in QUOTE_TYPES
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(u["main"]), ji=" ".join(u["ji"]), credit=cr, who=who_table(code, s),
                        note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=_lic(s), frame=private or "BY-SA" in s["rights"], ground=s["basis"][:120],
                        url=(f"https://www.pexels.com/photo/{fet[code]['pid']}/" if t in STOCK_TYPES else s["get"]),
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=t in STOCK_TYPES, page=False, related=False,
                        quote_page=False, named=AUTHOR in cr, mosaic=[list(b[:4]) for b in box_m] or None, name_mosaic=None,
                        masked_before=MASKED_BEFORE.get(code), era=s["era"], people=s["people"], private=private, **extra)
        print(f"✓ {code:10} {name:18} {w}x{h:<5} 主 {' '.join(u['main']) or '—':22} 地 {' '.join(u['ji']) or '—':22} {_lic(s)[:14]}"
              f"{'  額装だけ' if db[name]['frame'] else ''}{'  🔒非公開' if private else ''}  {'・'.join(notes)[:70]}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    pub = [n for n, r in db.items() if not r["stock"] and not r["private"]]
    print(f"→ ref/ep27/assets.json（{len(db)}点＝公開リポに入る写真 {len(pub)}・イメージ {sum(r['stock'] for r in db.values())}"
          f"・県警の引用 {sum(r['private'] for r in db.values())}・額装だけ {sum(1 for r in db.values() if r['frame'])}"
          f"・作者の印 {sum(1 for r in db.values() if r['named'])}・顔の升目 {sum(1 for r in db.values() if r['mosaic'])}"
          f"・地に使う {sum(1 for r in db.values() if r['ji'])}・束の大きさ {tot / 1e6:.1f}MB／公開リポの分 "
          f"{sum((EPD / f'{n}.jpg').stat().st_size for n in pub) / 1e6:.1f}MB）")
    return 1 if bad else 0


def _find(db, c):
    ns = [n for n, r in db.items() if n == c or r["code"] == c]
    if not ns:
        raise SystemExit(f"🔴 {c} は束に無い（build を先に）")
    return ns[0]


def cmd_look(codes, out_name="look.jpg", width=960):
    """束の写真を並べた見本（2列）＝リポの外（SCRATCH）。記号（CM045）か束の名（cm045）を渡す"""
    from PIL import Image, ImageDraw
    db = json.loads(DB.read_text(encoding="utf-8"))
    ims = []
    for c in codes:
        n = _find(db, c)
        im = Image.open(EPD / f"{n}.jpg").convert("RGB")
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        ImageDraw.Draw(im).rectangle((0, 0, 200, 40), fill=(0, 0, 0))
        ImageDraw.Draw(im).text((8, 8), f"{n} {db[n]['w']}x{db[n]['h']}", fill=(255, 255, 0))
        ims.append(im)
    cols = 2 if len(ims) > 1 else 1
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    H = sum(max(x.height for x in r) for r in rows) + 8 * (len(rows) - 1)
    sheet = Image.new("RGB", (width * cols + 8 * (cols - 1), H), (40, 40, 40))
    y = 0
    for r in rows:
        for i, x in enumerate(r):
            sheet.paste(x, (i * (width + 8), y))
        y += max(x.height for x in r) + 8
    SCRATCH.mkdir(parents=True, exist_ok=True)
    p = SCRATCH / out_name
    sheet.save(p, quality=90)
    print(f"→ {p}（{sheet.size[0]}x{sheet.size[1]}）")
    return 0


def cmd_crop(code, x0, y0, x1, y1, k=2.0):
    """束の画素の切り出し（k 倍・束の画素で 10px ごとの目盛り＝升目の範囲を読むため）＝out/ep27_look/crop_<名>_<x0>_<y0>.jpg"""
    from PIL import Image, ImageDraw
    db = json.loads(DB.read_text(encoding="utf-8"))
    n = _find(db, code)
    im = Image.open(EPD / f"{n}.jpg").convert("RGB").crop((x0, y0, x1, y1))
    im = im.resize((round(im.width * k), round(im.height * k)), Image.NEAREST if k >= 2 else Image.LANCZOS)
    d = ImageDraw.Draw(im)
    for x in range((x0 // 10 + 1) * 10, x1, 10):
        X = round((x - x0) * k)
        d.line((X, 0, X, 6 if x % 50 else 14), fill=(255, 255, 0))
        if x % 50 == 0:
            d.text((X + 2, 14), str(x), fill=(255, 255, 0))
    for y in range((y0 // 10 + 1) * 10, y1, 10):
        Y = round((y - y0) * k)
        d.line((0, Y, 6 if y % 50 else 14, Y), fill=(255, 255, 0))
        if y % 50 == 0:
            d.text((16, Y + 2), str(y), fill=(255, 255, 0))
    SCRATCH.mkdir(parents=True, exist_ok=True)
    p = SCRATCH / f"crop_{Path(n).name}_{x0}_{y0}.jpg"
    im.save(p, quality=92)
    print(f"→ {p}（{im.size[0]}x{im.size[1]}・{k}倍）")
    return 0


def cmd_panel():
    """ルール 0b-34②：PANEL_AR＝束の縦横比の並びで、16:9 より縦長の側のいちばん大きな切れ目の中点。"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    ars = sorted((r["w"] / r["h"], n, r["w"], r["frame"]) for n, r in db.items())
    for a, n, w, fr in ars:
        print(f"  {a:6.3f}  {n:22} 幅 {w}{'  額装だけ' if fr else ''}{'  （1280 未満＝kind() は額装）' if w < 1280 else ''}")
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
        m = PE.margins(f"ep27/{n}.jpg")
        mx = max(m.values())
        flag = "🔴" if mx >= PE.MIN_EDGE else ("・" if mx > 0 else " ")
        if mx > 0:
            hits.append((n, m))
        print(f"{flag} {n:22} 左 {m['l'] * 100:4.1f}% 上 {m['t'] * 100:4.1f}% 右 {m['r'] * 100:4.1f}% 下 {m['b'] * 100:4.1f}%"
              f"  {db[n]['era'][:16]}")
    big = [n for n, m in hits if max(m.values()) >= PE.MIN_EDGE]
    print(f"→ 暗い帯のある点 {len(hits)}（うち {PE.MIN_EDGE * 100:.1f}% 以上 {len(big)}＝{' '.join(big) or 'なし'}）")
    return 0


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
# 出典の行の字幅の上限の目安（全角＝1・半角＝0.55）＝23本目の写真の出典の行で門番 layout を通って公開された最長 56.5。本当の物差しは門番 layout
CREDIT_W_MAX = 56.5


def _width(s):
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.55 for c in s)


def _film_rows():
    """県警の動画（sources27 の police-video）の行＝取得の状態つき（clips.json にあれば取得ずみ）"""
    src = _sources()
    cl = json.loads(CLIPS.read_text(encoding="utf-8")) if CLIPS.exists() else {}
    lst = _list()
    rows = []
    for code, s in src.items():
        if s["type"] not in FILM_TYPES:
            continue
        cuts = " ".join(r["cid"] for r in lst if _code_of(r["main"]) == code)
        # 🆕 ⑤b-3：YT-A は取れない（403・回避しない）＝動画は使わず、映像方針で写したコマ（police-frame）を静止の引用に（下の写真の表の yta…）
        frames = " ".join(sorted(k for k, v in src.items() if v["type"] == "police-frame" and v["get"].startswith(f"frame:{code}@")))
        state = ("取得ずみ（git の外・md5 は clips.json）" if code in cl else
                 f"🔴 取れない（⑤b-2 の 403・回避しない）＝動画は使わない（⑤b-3：コマ {frames} を静止の引用に）" if frames else "🔴 未取得")
        rows.append(f"| `{code}` | {cuts} | {s['credit']} | 引用（話している秒だけ・実時間・音は使わない） | {state} |")
    return rows


def cmd_credits(write=False):
    """撮影年＝year_of（出どころつき）。主に当てたカットの副題が名乗る年（「NNNN年」・「当日」＝2022）と食い違えば止める
    （地に使うカットの副題は図の中身の年＝照らさない）。作者の名乗り（scene_jiko._ep27_author）を当てて出典の行の字幅を測る（名前は出さない＝字数だけ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import scene_jiko as SJ
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    names = _names()
    cj, rows, bad = {}, [], 0
    for n, r in sorted(db.items()):
        cuts = r["cut"].split()
        claims = set()
        for c in cuts:
            claims |= {int(y) for y in re.findall(r"(1[89]\d\d|20\d\d)年(?!代|ごろ|以前)", subs.get(c, ""))}
            if "当日" in subs.get(c, ""):
                claims.add(EVENT_YEAR)
        y = r["year"]
        if claims and (y is None or claims != {y}):
            print(f"🔴 {n}: 副題の年 {sorted(claims)} と撮影年 {y} が食い違う（{' '.join(cuts)}・{subs.get(cuts[0], '')}）＝{r['year_why'][:60]}")
            bad += 1
        leak = hits_in(json.dumps(r, ensure_ascii=False), names)
        if leak:
            print(f"🔴 {n}: 台帳の行に出さない名前が入っている（{len(leak)}語）")
            bad += 1
        line = r["credit"]
        if AUTHOR in line:
            try:
                line = line.replace(AUTHOR, SJ._ep27_author(f"ep27/{n}.jpg"))
            except Exception as e:                         # noqa: BLE001  焼く前に止める
                print(f"🔴 {n}: 作者の名乗りが作れない（{e}）")
                bad += 1
        wd = _width(line)
        if wd > CREDIT_W_MAX:
            print(f"🔴 {n}: 出典の行の字幅 {wd:.1f}（{CREDIT_W_MAX} まで＝画面の左下からはみ出すおそれ）")
            bad += 1
        cj[f"ep27/{n}.jpg"] = r["credit"]
        kind = "イメージ" if r["stock"] else ("引用・非公開" if r["private"] else "この事件の土地")
        mod = "・顔に升目" if r.get("mosaic") else ""
        use = " ".join(cuts) + (f"（地 {r['ji']}）" if r["ji"] else "")
        rows.append(f"| `{Path(n).name}` | {use or '—'} | {y if y else '不明'} | {r['lic']}（{kind}{mod}） | {r['who']} | {r['url']} |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真 {len(cj)}点{'' if not bad else f'・🔴 {bad}'}")
    if bad:
        return 1
    if not write:
        return 0
    CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-10-30（⑤b-2・⑤b-3）。`qa_out/ep27_assets.py credits --write` が書く（手で直さない）。写真は映像方針の一覧 `ref/ep27/eizou_list27.md`"
        "（了承② 2026-10-29・⑤b-3 の YT-A の当て直しは 10-30 カズヤくん了承）。",
        "🔴 事件の回（ルール §B2-10）＝被害者・遺族・けがをした人・目撃者・SNS の投稿者の名前は書かない・容疑者は必ず「八田與一容疑者」。",
        "",
        "### 0. 県警の動画（引用＝話している秒だけ・カットの秒で実時間・加工しない・音は使わない＝`-an`・サムネに使わない）",
        "- 大分県の「著作権・リンク等について」は「『私的使用のための複製』や『引用』など著作権法で認められた場合を除き」無断の転載・複製・改変を禁じる"
        "＝引用は県が禁止の外に置く（`ref/ep27/materials.md` §1）。🔴 **動画も、そこから抜いたコマも公開リポに置かない**（焼くのは Modal＝保管庫）。"
        "🔴 YT-A の 0〜20秒・153.5〜159.25秒（重要指名手配のポスター＝小さな字に「犯人」）は使わない（門番 `make_list27.BAD`）",
        "",
        "| 記号 | 使うカット | 画面の出典 | 使い方 | 取得 |",
        "|---|---|---|---|---|", *_film_rows(), "",
        "### 1. 写真（Commons の CC BY・BY-SA・CC0・Pexels のイメージ・県警と警察庁の引用）",
        "- CC BY・BY-SA＝「写真：{作者}／Wikimedia Commons（ライセンス）」。🔴 撮影者の名前はこのリポに書かない＝`ref/ep27/credits.json` は印 `{作者}` だけ・"
        "焼くときに git の外の表 `ref/ep27/src/credits_private.tsv` から足す（`tools/scene_jiko.ep27_credit`）。CC0＝「Wikimedia Commons（CC0）」",
        "- BY-SA＝額装（無加工・1点1カット・升目もかけない）。CC BY・CC0 の顔の分かる人は顔だけ升目（「／改変：顔にモザイク」）。色は原本のまま",
        "- 説明カットの地（「地 c…」）＝CC BY・CC0 の写真を暗くするだけ（字と地の比 8:1 が下限＝了承② 決め1・出典の行は「地の写真：…／改変：明るさ」＝⑤b-3）",
        "- イメージ（Pexels の写真）＝`ep27/stock/` の名・画面の左上に「イメージ」・20% に数えない・git に入れない（焼くときに直リンクから取り直して md5 を照らす）",
        "- 県警・警察庁の引用（`ep27/police/` の名）＝**公開リポに置かない**（git の外・Modal の保管庫）・額装・加工しない（似顔絵は並べ方だけ）",
        "- 撮影年＝Commons の頁の撮影日・県警の頁と動画の公開日（sources27 の時期の欄）。イメージは「不明」（副題に年を書かない）",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. 地図の衛星写真（Google マップ）",
        "- G1・G2・G3・G7・G9（9カット）＝Google マップの衛星写真＋描き足し（束の外＝`cuts/ss.SAT`・⑤b-4 で撮る）。出典は画面の地図の右下の帰属の行"
        "（Google の地図の利用）。🔴 PNG は公開リポに置かない（git の外・Modal の保管庫）",
        ""])
    if CREDITS_HEAD in md:
        pre, rest = md.split(CREDITS_HEAD, 1)
        nxt = rest.find("\n## ")
        md = pre + block + (rest[nxt:] if nxt >= 0 else "")
    else:
        md = md.rstrip("\n") + "\n\n" + block
    CREDITS_MD.write_text(md, encoding="utf-8", newline="\n")
    print(f"→ {CREDITS_JSON.relative_to(HERE).as_posix()} ／ {CREDITS_MD.relative_to(HERE).as_posix()}")
    return 0


def cmd_stockcheck():
    """イメージの直リンク（assets.json の media）を取り直して、束と md5 が同じか（焼くときの footage.stock_photos と同じ取り方）＝out/ep27_look/stock/"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    db = json.loads(DB.read_text(encoding="utf-8"))
    d = SCRATCH / "stock"
    d.mkdir(parents=True, exist_ok=True)
    bad = 0
    for n, r in sorted(db.items()):
        if not r["stock"]:
            continue
        dst = d / f"{Path(n).name}.jpg"
        dst.unlink(missing_ok=True)
        FO.download_media(r["media"], dst)
        got = md5(dst)
        ok = got == r["md5"]
        bad += not ok
        print(f"{'✓' if ok else '🔴'} {n}: 取り直し {dst.stat().st_size} B・md5 {got[:8]}／束 {r['md5'][:8]}")
    return 1 if bad else 0


# ── 県警の動画（引用）＝台帳 clips.json・ショット shots.json ─────────────
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


# 県警の動画の手元のファイル {記号: src からの道}（取得の記録 fetch_log.tsv の md5 と照らす）。
# 🔴 YT-A（2024-08-01）は手元に無い（⑤b-2 の 10-30：手元の yt-dlp は配信の側から 403。別の取り方は YouTube のボット対策を回避する操作として止めた）
#    ＝ここに書かない（clips.json に載せない＝USE も書かない）。✅ ⑤b-3（10-30 カズヤくん了承）＝動画は使わず、映像方針で写したコマ4つを静止の引用に
#    （sources27 の police-frame＝束の police/yta026 ほか）・c305 は YT-C の自撮りの区間
FILM_FILES = {"YT-C": "police_yt/20251211_zj9LhnLb1So.mp4"}
FOOTAGE = HERE / "tools" / "footage.py"

# 🆕 ⑤b-3（10-30）：**YT-C の場面＝30コマ/秒で測った境目を根拠つきで書く**（26本目 SHOT_ONE の型を広げた）。
#   1秒1コマの `tools/shots.shots_of` は境目を 2・8・14・18・22・24・27秒に置いた＝自撮りの手ぶれ（18・22秒）で割れ、実の切り替え
#   （3.4〜3.5・9.07・13.73・23.90・26.5〜26.6秒）を1秒単位にずらす＝c305（自撮り）がショットをまたぐことになり、c106 の尻（9.0秒）の先の
#   似顔絵（9.37秒〜）を見落とす。測り方＝64×36 の灰色の隣のコマとの差（10コマ/秒の全体＋30コマ/秒で頭と尻）と、画面に重ねた字
#   （左の懸賞金の字の範囲）の差（自撮りの 13.77〜23.87秒は 0.00〜0.08＝場面が替わらない）・0.5秒おき60コマの OCR（「犯」0）・原寸の6コマ
#   （scratchpad `ytc_sheetA・B・D`）。⚠️ (1.0, 9.06) は県警の編集の切り替え（手配の札→罪名の字＝3.4〜3.5秒）を含む＝**根拠つきで1つに**：
#   c106 は語りの順（名前→罪名）に札が替わるのを見せる意図（⑤b-1・了承②）・頭と尻を原寸で見た（⑤b-2）・字に「犯」0
#   ＝門番 footage の exit 3（ショットまたぎ）が守る「範囲の中で絵が別物」は、区間の中を全部見て決めた
SCENES = {"YT-C": [
    (0.0, 1.0, "黒からの立ち上がり（字なし）"),
    (1.0, 9.06, "手配の札（〜3.4）→ 罪名と情報提供先の字（3.5〜9.06）＝県警の編集の切り替えを根拠つきで1つに（c106）"),
    (9.06, 13.73, "似顔絵6枚＋「警察庁指定 重要指名手配」（9.07〜9.37 は切り替えの暗転）"),
    (13.73, 23.9, "自撮り（懸賞金 上限額800万円・※八田與一の実際の音声）＝重ねた字の差 0＝同じ場面（18.4・21.9秒の差は手ぶれと寄り）"),
    (23.9, 26.6, "手配の札（c106 の頭と同じ札＝顔写真と縦の字）"),
    (26.6, 30.09, "「この顔見たら110番 大分県警察」（止まった画面＝動き 0.02）"),
]}


def cmd_clips():
    """clips.json＝県警の動画（引用・手元のファイル＝git の外＝焼くのは Modal の保管庫）"""
    src, log = _sources(), _police_log()
    out = {}
    for code, rel in FILM_FILES.items():
        s = src[code]
        p = SRC / rel
        if not p.exists():
            raise SystemExit(f"🔴 {code}: 手元の動画が無い（src/{rel}）")
        h, size = md5(p), p.stat().st_size
        if h != log.get(rel):
            raise SystemExit(f"🔴 {code}: src/{rel} の md5 {h[:8]} が取得の記録と合わない")
        loc = _probe(p)
        out[code] = dict(url=f"https://www.youtube.com/watch?v={s['get'].removeprefix('yt:')}", media=f"ref/ep27/src/{rel}", local_from=0.0,
                         private=True, stock=False, credit=s["credit"], src="local", at=0.0, date=s["era"][:8], what=s["title"][:80],
                         w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(loc["sec"], 3), size=size, md5=h,
                         dispw=loc["w"], decoded=[loc["w"], loc["h"]], license="引用（著作権法32条・大分県の頁が引用を禁止の外に置く）",
                         rights=s["basis"], scan=f"ref/ep27/src/{rel}", md5_scan=h,
                         note="🔴 公開リポに置かない（git の外・焼くのは Modal＝保管庫 jiko-assets の同じ道）。音は使わない（-an）。"
                              "話している秒だけ・実時間（速さを変えない）・加工しない")
        print(f"  {code:5} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.2f}秒 {size / 1e6:.2f}MB md5 {h[:8]}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep27/clips.json（{len(out)}本・🔴 YT-A は手元に無い＝載せていない）")
    return 0


def _gray10(p):
    """10コマ/秒・64×36 の灰色（場面の動きと境目の差を測る）"""
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", "fps=10,scale=64:36,format=gray", "-f", "rawvideo", "-"],
                       capture_output=True, timeout=600)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    n = len(a) // (64 * 36)
    return a[:n * 64 * 36].reshape(n, 36, 64).astype(float)


def cmd_shots():
    """shots.json＝SCENES に書いた回は30コマ/秒で測った場面（根拠つき）・ほかは tools/shots.shots_of（1秒1コマ）。
    場面の境目ごとに 10コマ/秒の隣の差を出す（境目＝跳ね・場面の中＝動き）＝書いた境目が測った絵と合うかを毎回見せる"""
    sys.path.insert(0, str(HERE / "tools"))
    import numpy as np
    import shots as SH
    out = {}
    for code, rel in FILM_FILES.items():
        p = SRC / rel
        if code in SCENES:
            f = _gray10(p)
            d = np.r_[0, np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))]
            dur = len(f) / 10.0
            sh, notes = [], []
            for a, b, why in SCENES[code]:
                i0, i1 = int(round(a * 10)), min(len(d), int(round(b * 10)))
                sh.append(dict(start=a, until=b, motion=round(float(d[i0 + 1:i1].mean()) if i1 > i0 + 1 else 0.0, 2), why=why))
                if a > 0:
                    k = int(round(a * 10))
                    notes.append(f"{a:g}秒の跳ね {d[max(1, k - 1):k + 2].max():.1f}")
            how = ("⑤b-3（10-30）：30コマ/秒で測った場面（qa_out/ep27_assets.py の SCENES＝根拠つき）・1秒1コマの shots_of は自撮りの手ぶれで割れ、"
                   "実の切り替えを1秒単位にずらした＝使わない／境目の跳ね（10コマ/秒の隣の差・灰色 0〜255）：" + "・".join(notes))
            print(f"  {code:5} {dur:6.1f}秒  場面 {len(sh)}（SCENES）：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh)
                  + "\n        " + "・".join(notes))
        else:
            sh, dur = SH.shots_of(p)
            how = "1秒1コマで tools/shots.shots_of（27本目・県警の動画）"
            print(f"  {code:5} {dur:6.1f}秒  ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
        out[code] = dict(src=f"src/{rel}", scan=f"ref/ep27/src/{rel}", dur=round(dur, 1), how=how, shots=sh)
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep27/shots.json（{len(out)}本）")
    return 0


def _write_block(tag, lines):
    txt = FOOTAGE.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in txt else "\n"              # 🔴 25本目 ⑤b-1 の落とし穴＝改行を見分ける
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_bytes((txt[:m.start(2)] + "".join(x + nl for x in lines) + txt[m.end(2):]).encode("utf-8"))


def cmd_use(only=None, all_=False):
    """footage.USE の27本目の欄（26本目 `cmd_use` を写した）。区間と止めは一覧 list27.tsv の動きの欄「映像 a〜b秒（＋止め n秒）」から読む
    （手で写さない）・速さは変えない（rate 1.0＝実時間）・止めは `hold`（区間の尻のコマで持たせる＝footage.overruns・_cut_stream）。
    hold は**要る秒（narration.json の実測・扉を除く）− 区間**で決め、一覧の止め（了承の上限）をこえたら止める。
    🔴 章ファイルに `ss.vid` を書いたカットだけ（`only` は書く前の鶏と卵を割るため＝ss.vid は USE の clip で private を見分ける）"""
    sys.path.insert(0, str(HERE / "tools"))
    sys.path.insert(0, str(BUILD))
    import make_list27 as ML
    if only:
        secs, spec = {r["cid"]: float(r["cont"]) for r in _list()}, {}
    else:
        import footage as FO
        import scene_jiko as S
        secs, spec = FO.secs_of(), S.SPEC
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    src = _sources()
    lines, skip = [], []
    for r in _list():
        code = _code_of(r["main"])
        if src.get(code, {}).get("type") not in FILM_TYPES:
            continue
        cid = r["cid"]
        sp = spec.get(cid) or {}
        wrote = str(sp.get("photo") or "").endswith(f"fb_{cid}.jpg")
        if not (all_ or wrote or (only and cid in only)):
            skip.append(cid)
            continue
        vw = ML.video_window(r["motion"])
        if not vw:
            raise SystemExit(f"🔴 {cid}: 一覧の動きの欄に区間「映像 a〜b秒」が無い（{r['motion']}）")
        a, b, hold_max = vw
        for blo, bhi in ML.BAD.get(code, []):
            if a < bhi and b > blo:
                raise SystemExit(f"🔴 {cid}: {code} {a}〜{b}秒が「犯人」の字の秒 {blo}〜{bhi} にかかる")
        hit = [x for x in sd[code]["shots"] if x["start"] <= a < x["until"]]
        if len(hit) != 1 or b > hit[0]["until"] + 1e-6:
            raise SystemExit(f"🔴 {cid}: 区間 {a}〜{b} が1つの場面に収まらない（場面 {[(x['start'], x['until']) for x in hit]}）")
        need = float(secs[cid])
        hold = round(max(0.0, need - (b - a)) + 0.005, 2) if need > b - a else 0.0
        if hold > hold_max + 0.05:
            raise SystemExit(f"🔴 {cid}: 止め {hold:.2f}秒が一覧の止め {hold_max:.2f}秒（了承の上限）をこえる＝要る {need:.2f}秒・区間 {b - a:.2f}秒")
        sh = hit[0]
        hs = f", hold={hold}" if hold else ""
        # 引用＝額装・地のぼかしを作らない（plain=True＝cuts/ss.check_frame_only が見る）・寄せない・等速
        lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate=1.0{hs}, plain=True),   '
                     f'# 場面 {sh["start"]:g}〜{sh["until"]:g}秒・区間 {b - a:.2f}秒{f"＋止め {hold:.2f}秒" if hold else ""}／要る {need:.2f}秒'
                     f'・実時間・音は使わない（-an）・{src[code]["credit"]}')
    _write_block("EP27_USE", lines)
    print(f"→ tools/footage.py USE {len(lines)}欄")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """県警の動画のひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）＝区間の頭のコマを**原寸のまま**（引用＝加工しない・
    寄せも切りもしない＝額装）。🔴 置き場は `ref/ep27/police/fb_<cid>.jpg`（公開リポに置かない＝`cuts/ss.PRIVATE_DIR`）。
    Modal では `footage.fetch` が切り出したコマの1枚目から同じ道に作る（保管庫に入れなくてよい）"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    bad = 0
    (EPD / "police").mkdir(exist_ok=True)
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
        c = FO.CLIPS.get(u["clip"]) or {}
        if not c.get("private"):
            continue
        p = HERE / c["media"]
        dst = EPD / "police" / f"fb_{cid}.jpg"
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{float(u['start']):.3f}", "-i", str(p), "-frames:v", "1", "-q:v", "2", str(dst)],
                           capture_output=True)
        if r.returncode or not dst.exists():
            print(f"🔴 {cid}: コマが取れない（{r.stderr.decode('utf-8', 'replace')[-120:]}）")
            bad += 1
            continue
        from PIL import Image
        with Image.open(dst) as im:
            w, h = im.size
        print(f"✓ {cid:5} {u['clip']:5} {float(u['start']):6.2f}秒 {w}x{h} → {dst.relative_to(HERE).as_posix()}（🔴 git に入れない）")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "edges": cmd_edges, "clips": cmd_clips, "shots": cmd_shots, "stockcheck": cmd_stockcheck}
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] == "use":
        sys.exit(cmd_use(set(x for x in a[1:] if not x.startswith("--")) or None, "--all" in a))
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "look":
        sys.exit(cmd_look(a[1:]))
    if a and a[0] == "crop":
        sys.exit(cmd_crop(a[1], *map(int, a[2:6]), float(a[6]) if len(a) > 6 else 2.0))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
