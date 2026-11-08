# -*- coding: utf-8 -*-
"""ep31_assets.py — 31本目（全日空機雫石衝突事故）の写真と紙面の束・出典・防衛庁記録の台帳（⑤b-2・2026-11-08）。30本目 `ep30_assets.py` の写し。
31本目の台帳（`sources31.psv` の13列・`fetch31.tsv`〈md5 を2回〉・git の外の表 `src/credits_private.tsv`〈Commons の撮影者＝頭の行なし・8列〉）に合わせた。
第三者の引用は無い（31本目の写真は Commons と国土地理院だけ）。イメージ（Pexels）は ⑤b-3a＝束に入れない。防衛庁記録 MS・MK は clips.json・shots.json（`clips`・`shots`・`use`）。

  python -P qa_out/ep31_assets.py gsi               # 地理院タイルを z+1・8×6枚で取る（公的＝許可不要・1秒あける）＝src/gsi/tiles/ と src/gsi/tiles_log.tsv
  python -P qa_out/ep31_assets.py build [--nopages] # 束 ref/ep31/<名>.jpg ＋ 権利の台帳 ref/ep31/assets.json（--nopages＝紙面を撮る前・commit しない）
  python -P qa_out/ep31_assets.py pdflines JS       # PDF の字の層の行（頁・y）を src/pages/<記号>_pdflines.txt へ（🔴 名前の字が入る＝Read で開かない）
  python -P qa_out/ep31_assets.py look P1 …         # 束の写真を並べた見本（out/ep31_look/・1枚 960 幅）
  python -P qa_out/ep31_assets.py crop P1 x0 y0 x1 y1 [倍]   # 束の画素の切り出し（既定2倍・10px の目盛り）＝人とナンバーを決めるとき
  python -P qa_out/ep31_assets.py panel｜edges      # ss.PANEL_AR の切れ目／門番 check_photo_edge の名簿（SLIDE_MOUNT／SLIDE_NOT_MOUNT）
  python -P qa_out/ep31_assets.py credits [--write] # 画面の出典 ref/ep31/credits.json と ref/CREDITS.md の31本目の節
  python -P qa_out/ep31_assets.py clips｜shots｜use  # 防衛庁記録 MS・MK の台帳・場面の切れ目・footage.USE の13欄（一覧の動きの欄から読む）

🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色）＝幅 2400 か高さ 1350 の大きい方まで（小さい写真は原画のまま）。
🔴 国土地理院の空中写真（PDL1.0）＝公開リポに置く・切り出してよい・出典の行に「加工して作成」（印は描かない）。
🔴 公的な機関の紙面＝公開リポに置く・切り出すので出典の行に「／改変：切出」。判決と法令は著作権法13条・国会の答弁は40条の読み（⚠️ 法律の助言ではない＝こちらの読み）。
🔴 この回の線（台本 §1-4）＝語りと画面に人の名前を出さない＝紙面の切り口に名前の行を入れない・同じ行の名前は字だけ隠す（親が絵を見て切る）。
   名前は台帳・出典の行・CREDITS.md に書かない＝撮影者は印 `{作者}` だけ（焼くときに `scene_jiko._ep31_person` が git の外の表の3列目から足す）。
   🔴 P1・P3 の許諾の箱の「Attribution:」の指定は3列目と1字も違わない（11-08 に頁の写しで照らした＝`_attr_ok`）＝画面は `{作者}`。8列目（160字）は許諾の雛形の文の取り違え＝使わない。
🔴 人とナンバー（了承②）＝公的な任務の顔はそのまま。私人の顔とナンバーは CC BY・CC0・PD で升目（MASK）・**BY-SA は升目も翻案＝かけない**（読める顔やナンバーがあれば別の点に）。
"""
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import unicodedata
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep31"
SRC = EPD / "src"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list31.tsv"
SOURCES = BUILD / "sources31.psv"
FETCHES = (BUILD / "fetch31.tsv",)
PAGE_LOG = SRC / "pages" / "log.tsv"          # 頁の撮影の記録（git の外・撮った日時・URL・md5）
PRIVATE = SRC / "credits_private.tsv"         # 🔴 git の外（Commons の撮影者＝頭の行なし・8列＝記号・ファイル・作者…・帰属）＝ここから名前を公開の物へ写さない
NAME_FILES = (SRC / "names_private.txt", SRC / "names_commons.txt")     # 🔴 git の外（出さない名前＝亡くなった方・遺族・操縦者・乗員・役人・裁判官・弁護人・撮影者）
COMMONS_PAGES = SRC / "commons" / "pages"     # 🔴 git の外（映像方針で取った Commons の頁の写し＝許諾の箱の「Attribution:」を照らす）
GSI_TILES = SRC / "gsi" / "tiles"             # 地理院タイル（git の外）
GSI_LOG = SRC / "gsi" / "tiles_log.tsv"       # 🆕 ⑤b-2：z+1 で取った枚の記録（取った日・層・z・x・y・bytes・md5・md5（読み直し））
DB = EPD / "assets.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
FOOTAGE = HERE / "tools" / "footage.py"
STILL_BELOW = 0.4            # 🔴 31本目：防衛庁記録のスローは 0.40倍まで（§5b-17b・了承②）＝これより遅い欄は止め絵にする
UA = "zukai-engine-research/1.0 (GitHub torotorotolo/zukai-engine)"
SCRATCH = HERE / "out" / "ep31_look"          # look・crop の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## 全日空機雫石衝突事故（1971-07-30・31本目）"
AUTHOR = "{作者}"            # CC BY・BY-SA・CC0 の出典の行の印（焼くときに git の外の表の3列目から足す＝scene_jiko.ep31_credit）
EVENT_YEAR = 1971            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 92
MOSAIC_PX = 14                         # 升目の大きさ（束の画素）
COMMONS_TYPES = ("commons-photo",)                   # Commons の写真（事故機・同型機・保存機・裁判所の建物＝CC BY・BY-SA・CC0・SDASM）
NATION_TYPES = ("public-photo",)                     # 国土地理院の空中写真（PDL1.0＝公開リポに置く・切り出してよい）
QUOTE_TYPES = ()                                     # 31本目は第三者の引用なし
PHOTO_TYPES = COMMONS_TYPES + NATION_TYPES + QUOTE_TYPES
PUBLIC_TYPES = ("public-page", "public-pdf")         # 公的な機関の頁と PDF（規約を読んだ＝公開リポに置く）
PAGE_TYPES = PUBLIC_TYPES
STOCK_TYPES = ("stock",)                             # 束に入れない（⑤b-3a）
FILM_TYPES = ("commons-video",)                      # 防衛庁記録 MS・MK＝clips.json（束の外）
KIND_OK = {"写真": COMMONS_TYPES, "場所": COMMONS_TYPES, "空中": NATION_TYPES, "公的": PUBLIC_TYPES}
KIND_OUT = ("映像", "衛星", "イメージ")              # 束の外＝映像は clips.json・衛星は ss.SAT・イメージは ⑤b-3a
# 🆕 31本目：地（説明カットの地）に一覧が「G:…」（イメージの地＝⑤b-3a で Pexels の記号を当てる）と「MS」（防衛庁記録の映像＝⑤b-4 でコマを選んで
#    束の静止画 `ms_g…` にする）を書いたカット＝束では止めずに数えて出す（どちらも札の型のカット＝⑤b-4 で地を当てるときに必ず当たる＝`ss.gr` が束に無ければ止める）
JI_LATER = {"G": "イメージの地（⑤b-3a で Pexels を当てる）", "MS": "防衛庁記録の映像のコマ（⑤b-4 でコマを選んで束へ・CC BY 3.0）"}

# 🆕 国土地理院の空中写真＝z+1 の 8×6枚（2048×1536）を組んで 16:9（2048×1152）に切る。映像方針の見本（z の 3×3＝768px）と同じ真ん中・横は 4/3 倍・縦は 3/4 倍
#   {記号: (層, z, 左の x, 上の y, 横の枚数, 縦の枚数, 窓（左, 上, 幅）＝組んだ全体 2048×1536 の画素・高さは幅の 9/16)}。🔴 印（赤い丸）は描かない
#   🔴 窓＝1枚の写真の中だけ（11-08 に scratchpad の gsiwin.py で、(B−R) の色の組と黒で割り、少ない側が 0.5% 未満のいちばん大きな窓を探した）：
#     A1＝右下の写真の外（黒・24%）を外す／A2＝上の緑の写真だけ（下の青い写真〈39%〉との継ぎ目を入れない＝映像方針の申し送り）／A3・A7＝1枚＝真ん中。
#     A6＝青と黄の写真が入りまじる（1枚の中の窓は幅 670px 以下＝×2.9 以上）＝地にだけ使う（暗くする）ので真ん中のまま＝🔴 ⑤c で継ぎ目を見る
GSI_COMPOSE = {"A1": ("gazo1", 15, 2 * 14617 - 1, 2 * 6295, 8, 6, (0, 0, 1568)),   # 8×8 の塊の平均が黒い面 0個の窓（1648 幅は下の端に黒の面が入った）
               "A2": ("gazo1", 17, 2 * 58435 - 1, 2 * 24890, 8, 6, (624, 0, 1352)),   # 青い写真の塊 0個の窓（1376 幅は下の左右の角に 36個＝束の絵で見えた）
               "A3": ("seamlessphoto", 17, 2 * 58435 - 1, 2 * 24890, 8, 6, (0, 192, 2048)),
               "A6": ("gazo1", 16, 2 * 29230 - 1, 2 * 12439, 8, 6, (0, 192, 2048)),
               "A7": ("gazo1", 16, 2 * 29214 - 1, 2 * 12440, 8, 6, (0, 192, 2048))}
GSI_URL = "https://cyberjapandata.gsi.go.jp/xyz/{layer}/{z}/{x}/{y}.jpg"
GSI_ONE_PHOTO = {"A2"}                 # 窓の中に青い写真（B−R＞15 の 8×8 の塊）が1つでも入れば止める点

# PDF の切り口 {束の名: dict(code, page, head, tail, outside, white)}＝字の層の行で決める（head の行〜tail の行の外接＋余白）。outside＝切り口に入ってはいけない行の字（名前の行の目印）
PDF_DPI_K = 3.0                        # 描く倍率（1pt＝3画素）
PDF_FILES = {"JS": "hanrei/hanrei-pdf-58088.pdf"}
PDF_LOG_MD5 = {}                       # ② に取った手元のファイル（git の外）＝取得の記録に無ければここに写す
PDF_CROP = {}                          # ⑤b-2 の紙面の段で書く（カットごとに切り口が違う＝束の名は「記号_カット」）
PAGE_PAD = 24                          # 紙面の絵のまわりの白（束の画素）＝字が額の縁に触れない
HIDDEN = {}                            # 紙面の中で隠した所の断り（束の名 → 「・名前を隠した」）

# 升目 {記号: [(x0, y0, x1, y1, 札)]}（束の画素）。札が「ナンバー：」で始まる箱＝ナンバー・それ以外＝顔（出典の行の断りを分ける）。⑤b-2 に原寸で見て決める
MASK = {}

# 束の段で切り落とす＝絵に入れない {記号: (左, 上, 右, 下)}＝元の絵に対する割合。縮める前に切る
PRE_CROP = {}


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
    # 🆕 31本目：sources31.psv は見出しを頭の注の行に書く（「13列＝code|type|…|note」）＝注の行の並びと照らす
    head = ["code", "type", "grp", "title", "get", "dims", "rights", "basis", "credit", "era", "people", "file", "note"]
    note = next((ln for ln in SOURCES.read_text(encoding="utf-8").splitlines() if ln.startswith("#") and "13列＝" in ln), "")
    if "13列＝" + "|".join(head) not in note:
        raise SystemExit(f"🔴 {SOURCES.name} の見出し（頭の注の13列）が変わった：{note[:120]}")
    out, prev = {}, None
    for ln in rows:
        f = ln.split("|")
        if len(f) != 13:
            raise SystemExit(f"🔴 {SOURCES.name} の行の欄が13でない：{ln[:80]}")
        d = dict(zip(head, f))
        # 「同上」＝すぐ上の行と同じ（出典の欄「同上（提供：{個人}）」も上の行が同じ字を持つ）
        for k in ("basis", "credit"):
            if d[k].startswith("同上"):
                if not prev or prev[k].startswith("同上"):
                    raise SystemExit(f"🔴 {d['code']}: {k} の「同上」が指す行が無い")
                d[k] = prev[k]
        out[f[0]] = prev = d
    return out


def _fetched():
    """{記号: 行}（取得の記録＝取った日・記号・種類・bytes・md5・md5（読み直し）・ファイル・出どころ）。本番の取得だけ（look は見本帳）"""
    out = {}
    for p in FETCHES:
        for r in csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"):
            if r.get("種類") != "look":
                out[r.get("記号") or ""] = r
    return out


def _page_log():
    """{記号: 行}（頁の撮影の記録の、その記号のいちばん新しい行）"""
    if not PAGE_LOG.exists():
        raise SystemExit(f"🔴 {PAGE_LOG.relative_to(HERE).as_posix()} が無い（頁を撮っていない）")
    return {r["記号"]: r for r in csv.DictReader(PAGE_LOG.open(encoding="utf-8"), delimiter="\t")}


def _private():
    """git の外の表 {記号: 作者（3列目）}。無ければ止める（束を作る手元だけで読む）"""
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の表）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    return {r[0]: r[2] for r in rows if len(r) > 2}


def _attr_ok(code):
    """🔴 BY-SA の P1・P3 は許諾の箱に「Attribution: …」の指定がある＝頁の写し（git の外）の指定が表の3列目と1字も同じか（名前は出さない＝真偽だけ）。
    頁に指定が無い点は True（3列目＝撮影者の名乗りのまま）。頁の写しが無ければ止める（照らせない＝fail closed）"""
    import html as H
    p = COMMONS_PAGES / f"{code}.html"
    if not p.exists():
        raise SystemExit(f"🔴 {code}: Commons の頁の写し {p.name} が無い（許諾の箱の帰属の指定を照らせない）")
    t = " ".join(H.unescape(re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8"))).split())
    m = re.search(r"Attribution: (.*?) You are free", t)
    if not m:
        return True
    return " ".join(m.group(1).split()) == " ".join(_private().get(code, "").split())


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


# 目録の作者の欄に入っていた機関名と一般の語＝名前でない（29本目の `eizou_build/authors29.SKIP` と同じ扱い）
_NOT_NAMES = {"投稿者", "tokyo", "artist", "panoramio", "wikipedia", "self", "photo", "own work", "flickr", "commons", "wikimedia", "user", "unknown",
              "sdasm archives"}   # 🆕 31本目：P5 の作者の欄＝サンディエゴ航空宇宙博物館の資料室（機関名・11-08 に表の3列目と1字も同じと照らした）


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
        if len(w) >= 2 and _fold(w) not in _NOT_NAMES:
            out.append((_mask_word(w.replace(" ", "")), _name_re(w)))
    if not out:
        raise SystemExit("🔴 名前の表が空（fail closed）")
    return out


def hits_in(text, names):
    t = _fold(text)
    return [w for w, rx in names if rx.search(t)]


def _code_of(main):
    """一覧の素材の欄（CM009:札寄り のように寄りの名がつく）→ 記号"""
    return (main or "").split(":", 1)[0].strip()


GROUND_RIGHTS = ("CC BY 2.0", "CC BY 2.5", "CC BY 3.0", "CC BY 4.0", "CC0", "PD", "PDL1.0")   # 地にできる権利（`ss.GROUND_LIC` から Pexels を除いた形・SDASM は地にしない）


def uses(later=None):
    """{束の鍵: dict(code, main=[カット], ji=[カット], full=全面に当てるカットがあるか)}（束に入る写真と紙面）。一覧の種類と出どころの型が食い違えば止める。
    🆕 31本目：紙面はカットごとに切り口が違う＝鍵は「記号_カット」（写真は記号のまま）。
    地（説明カットの地の写真）は CC BY・CC0・PD・PDL1.0 だけ（BY-SA は暗くするのも翻案・SDASM は地にしない）。JI_LATER の地は束の外＝`later` に {記号: [カット]}"""
    src = _sources()
    out, bad = {}, []
    later = {} if later is None else later
    for r in _list():
        cid = r["cid"]
        c = _code_of(r["main"])
        if c and r["kind"] not in KIND_OUT:
            s = src.get(c)
            if not s:
                bad.append(f"{cid} {c}: 出どころの表に無い")
            elif r["kind"] not in KIND_OK:
                bad.append(f"{cid} {c}: 図の型「{r['kind']}」の素材の欄に記号がある（地は ji の欄）")
            elif s["type"] not in KIND_OK[r["kind"]]:
                bad.append(f"{cid} {c}: 一覧の種類「{r['kind']}」と出どころの型 {s['type']} が食い違う")
            elif s["type"] in PHOTO_TYPES + PAGE_TYPES:
                key = f"{c}_{cid}" if s["type"] in PAGE_TYPES else c
                u = out.setdefault(key, dict(code=c, main=[], ji=[], full=False))
                u["main"].append(cid)
                u["full"] = u["full"] or r["frame"].startswith("全面")
        j = _code_of(r["ji"])
        if j in JI_LATER:
            later.setdefault(j, []).append(cid)
        elif j:
            s = src.get(j)
            if not s or s["type"] not in COMMONS_TYPES + NATION_TYPES:
                bad.append(f"{cid} {j}: 地の写真が Commons か国の写真でない（{s['type'] if s else '表に無い'}）")
            elif s["rights"] not in GROUND_RIGHTS:
                bad.append(f"{cid} {j}: 地の写真の権利 {s['rights']} は地にできない（BY-SA は暗くするのも翻案・SDASM は地にしない）")
            else:
                out.setdefault(j, dict(code=j, main=[], ji=[], full=False))["ji"].append(cid)
    if bad:
        raise SystemExit("🔴 " + "\n🔴 ".join(bad))
    return out


def is_private(code, s):
    return s["type"] in QUOTE_TYPES


def bundle_name(key, s):
    return key.lower().replace("-", "_")


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
    """範囲だけを升目にする（縮めて NEAREST で戻す）＝16〜27本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def _src_path(s):
    """sources31 の file の欄の頭の道だけ＝ref/ep31 からの道"""
    m = re.match(r"(src/[^（\s|]+?\.(?:jpe?g|png|pdf))", s["file"])
    return EPD / m.group(1) if m else None


def _src_ok(code, s, fet):
    """手元の元のファイルが取得の記録（md5 を2回＝同じ）と同じか。違えば止める"""
    p = _src_path(s)
    if not p or not p.exists():
        raise SystemExit(f"🔴 {code}: 手元のファイルが無い（{s['file']}）")
    r = fet.get(code)
    if not r:
        raise SystemExit(f"🔴 {code}: 取得の記録が無い（fetch30.tsv）")
    h = md5(p)
    if r["md5"] != r["md5（読み直し）"] or h != r["md5"] or (EPD / r["ファイル"]).resolve() != p.resolve():
        raise SystemExit(f"🔴 {code}: {p.name} の md5 が取得の記録と合わない（取り直す）")
    return p, h


def _pdf_ok(code, fet):
    p = SRC / PDF_FILES[code]
    if not p.exists():
        raise SystemExit(f"🔴 {code}: PDF が無い（{p}）")
    h = md5(p)
    want = (fet.get(code) or {}).get("md5") or PDF_LOG_MD5.get(code)
    if h != want:
        raise SystemExit(f"🔴 {code}: {p.name} の md5 {h[:8]} が取得の記録 {str(want)[:8]} と合わない")
    return p, h


def _pdf_lines(pg):
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                out.append((t, l["bbox"]))
    return sorted(out, key=lambda x: (round(x[1][1]), x[1][0]))


def render_pdf(code, p):
    """PDF の切り口を描く＝(RGB の絵, 記録の言葉)。parts があれば頁ごとの切り口を縦につなぐ"""
    from PIL import Image
    sp = PDF_CROP[code]
    if "parts" not in sp:
        return _render_part(code, p, sp)
    got = [_render_part(code, p, x) for x in sp["parts"]]
    H = sum(g[0].height for g in got)
    W = max(g[0].width for g in got)
    im = Image.new("RGB", (W, H), (255, 255, 255))
    y = 0
    for g, _ in got:
        im.paste(g, (0, y))
        y += g.height
    return im, "・".join(g[1] for g in got) + "（縦につないだ）"


def _render_part(code, p, sp):
    """PDF の切り口を1つ描く。outside の行が切り口に入れば止める"""
    import fitz
    from PIL import Image
    pg = fitz.open(p)[sp["page"] - 1]
    lines = _pdf_lines(pg)
    if sp.get("head"):
        i0 = next((i for i, (t, _) in enumerate(lines) if sp["head"] in t), None)
        if i0 is None:
            raise SystemExit(f"🔴 {code}: 「{sp['head']}」の行が字の層に無い")
        i1 = next((i for i in range(i0, len(lines)) if sp["tail"] in lines[i][0]), None)
        if i1 is None:
            raise SystemExit(f"🔴 {code}: 「{sp['head']}」より後に「{sp['tail']}」の行が無い")
        top, bot = min(b[1] for _, b in lines[i0:i1 + 1]), max(b[3] for _, b in lines[i0:i1 + 1])
    else:
        top, bot = min(b[1] for _, b in lines), max(b[3] for _, b in lines)
    if sp.get("head"):
        sel = [b for _, b in lines if b[1] >= top - 1 and b[3] <= bot + 1]
    else:
        sel = [b for _, b in lines]
    # 頁番号（下の欄外）は外接に入れない
    sel = [b for b in sel if b[1] < pg.rect.height * 0.92]
    x0, x1 = min(b[0] for b in sel), max(b[2] for b in sel)
    top, bot = min(b[1] for b in sel), max(b[3] for b in sel)
    # 上下の余白は 12pt まで・前後の行とのすき間の真ん中まで（次の行の頭が絵に入らない＝D1023a で「D) 継続的な対応」が半分写った）
    above = [b[3] for _, b in lines if b[3] <= top + 1]
    below = [b[1] for _, b in lines if b[1] >= bot - 1]
    yt = max(top - 12, (max(above) + top) / 2) if above else top - 12
    yb = min(bot + 12, (min(below) + bot) / 2) if below else bot + 12
    box = (max(0, x0 - 14), max(0, yt), min(pg.rect.width, x1 + 14), min(pg.rect.height, yb))
    if sp.get("xbox"):
        box = (sp["xbox"][0], box[1], sp["xbox"][1], box[3])
    if sp.get("ybox"):
        box = (box[0], sp["ybox"][0], box[2], sp["ybox"][1])
    for anc in sp.get("outside", []):
        hit = [b for t, b in lines if anc in t]
        if not hit:
            raise SystemExit(f"🔴 {code}: 目印の行「{anc}」が字の層に無い（外に出したことを測れない）")
        if any(b[1] < box[3] and b[3] > box[1] for b in hit):
            raise SystemExit(f"🔴 {code}: 切り口の外にあるべき行「{anc}」が束の絵に入る")
    for r in sp.get("white", []):                        # メモリの中の頁だけ（元のファイルは変えない）
        pg.draw_rect(fitz.Rect(*r), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
    k = sp.get("k", PDF_DPI_K)
    pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), clip=fitz.Rect(*box), alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return im, f"PDF の {sp['page']}頁の切り口（y {box[1]:.0f}〜{box[3]:.0f}pt）を描いた（1pt＝{k:g}画素）"


_YEAR = re.compile(r"((?:19|20)\d\d)(?!年代|\d)")    # 31本目の時期の欄は「1971年5月」「1974〜78年」「撮影年は不明」「最新（…）」（表示に年が無い点は年を言わない）


def year_of(code, s):
    m = _YEAR.search(s["era"])
    if m:
        return int(m.group(1)), f"{SOURCES.name} の時期の欄「{s['era'][:24]}」（映像方針＝Commons の頁の撮影日・地理院の層・文書の日付）"
    return None, f"撮影の年の出どころが無い（時期の欄「{s['era']}」）"


GSI_CREDIT = {"gazo1": "出典：国土地理院ウェブサイト（地理院タイル・空中写真 1974〜1978年）・加工して作成",
              "seamlessphoto": "出典：国土地理院ウェブサイト（地理院タイル・シームレス空中写真）・加工して作成"}


def _base_credit(code, s):
    """sources31 の出典の欄を束の書きの頭の形に揃える（🆕 31本目）：「（地：同じ写真のぼかし）」は `scene_jiko.credit_of` が足す・
    「・無加工」は「／改変なし」で言う（「改変」の字が無いと credit_of が「／改変：色調変更・切出」を足す）・地だけの点の「地の写真：…・改変：切出・明るさ」は
    `ground_credit` が作る＝「写真：…」に戻す・国土地理院は層ごとに1つの形（地に敷くときも同じ字＝ground_credit が「地の写真：」に替える）"""
    cr = s["credit"].replace("（地：同じ写真のぼかし）", "").replace("・無加工", "")
    if s["type"] in NATION_TYPES:
        return GSI_CREDIT[GSI_COMPOSE[code][0]]
    if cr.startswith("地の写真："):
        cr = "写真：" + cr[len("地の写真："):].replace("・改変：切出・明るさ", "")
    if s["type"] in COMMONS_TYPES and not cr.startswith("写真："):
        cr = "写真：" + cr
    if s["type"] in PAGE_TYPES and not cr.startswith("出典："):
        cr = "出典：" + cr
    return cr


def _mask_words(boxes):
    """升目の断りの語＝「顔」「ナンバー」「顔とナンバー」（札が「ナンバー：」で始まる箱＝ナンバー）"""
    plate = any(str(b[4]).startswith("ナンバー：") for b in boxes)
    face = any(not str(b[4]).startswith("ナンバー：") for b in boxes)
    return "顔とナンバー" if face and plate else "ナンバー" if plate else "顔"


def screen_credit(code, s, boxes, full):
    """画面の出典の行（了承②）＝sources30 の出典の欄＋**改変の断りを明記**：
    BY-SA＝「／改変なし」（額装・無加工）・CC BY の全面＝「／改変：切出」・CC BY の額装だけ＝「／改変なし」・CC0 と PD＝断りなし（切っても書かなくてよい・升目だけ書く）・
    国の写真＝「加工して作成」（PDL の編集の記載＝地のぼかしも切り出しも＝欄に無ければ足す）・公的な機関の紙面＝「／改変：切出」・第三者の引用＝断りなし（無加工の額）。升目は「・〇〇にモザイク」を足す"""
    if "［" in s["credit"] or "⑤b" in s["credit"] or s["credit"].startswith("同上"):
        raise SystemExit(f"🔴 {code}: 出典の欄に書きかけの印が残る（{s['credit'][:60]}）")
    cr = _base_credit(code.split("_c")[0] if s["type"] in PAGE_TYPES else code, s)
    what = f"{_mask_words(boxes)}にモザイク" if boxes else ""
    if boxes and (s["type"] not in COMMONS_TYPES + NATION_TYPES or "BY-SA" in s["rights"]):
        raise SystemExit(f"🔴 {code}: 升目は CC BY・CC0・PD・PDL1.0 の写真だけ（{s['rights']}＝BY-SA は升目も翻案）")
    if s["type"] in COMMONS_TYPES and "BY-SA" in s["rights"]:
        return cr + "／改変なし"
    if s["type"] in COMMONS_TYPES and "CC BY" in s["rights"]:
        mods = (["切出"] if full else []) + ([what] if what else [])
        return cr + ("／改変：" + "・".join(mods) if mods else "／改変なし")
    if s["type"] in NATION_TYPES:
        return cr + (f"（{what}）" if what else "")
    if s["type"] in PUBLIC_TYPES:
        return cr + f"／改変：切出{HIDDEN.get(code, '')}"
    return cr + (f"／改変：{what}" if what else "")


def who_table(code, s):
    """CREDITS.md の撮影者の欄（名前は書かない）"""
    t, r_ = s["type"], s["rights"]
    if t in COMMONS_TYPES and r_.startswith("CC BY"):
        return "Commons の撮影者（名前は git の外 `ref/ep31/src/credits_private.tsv` の記号の行の3列目＝画面は焼くときに足す）"
    if t in COMMONS_TYPES and r_.startswith("SDASM"):
        return "SDASM Archives（Flickr の The Commons）"
    if t in COMMONS_TYPES:
        return "表示は任意（CC0）"
    if t in NATION_TYPES:
        return "国土地理院"
    return "各機関（国）"


def _lic(code, s):
    t = s["type"]
    if t in NATION_TYPES:
        return "PDL1.0"
    if t in PUBLIC_TYPES:
        return s["basis"] if t == "public-pdf" else s["rights"]
    return s["rights"]


def _page_src(code, s, log):
    """撮った頁の元のファイル＝(道, md5, 撮った日時)。記録の md5 と違えば止める"""
    r = log.get(code)
    p = SRC / "pages" / f"{code}.png"
    if not r or not p.exists():
        raise SystemExit(f"🔴 {code}: 頁を撮っていない（src/pages/log.tsv・{p.name}）")
    h = md5(p)
    if h != r["md5"]:
        raise SystemExit(f"🔴 {code}: {p.name} の md5 が撮影の記録と合わない")
    return p, h, r["撮った日時"]


# ── 国土地理院の空中写真（🆕 31本目 ⑤b-2）────────────────────────
def _gsi_tiles(code):
    layer, z, x0, y0, nx, ny, _ = GSI_COMPOSE[code]
    return [(layer, z, x, y) for y in range(y0, y0 + ny) for x in range(x0, x0 + nx)]


def _gsi_path(layer, z, x, y):
    return GSI_TILES / layer / str(z) / f"{x}_{y}.jpg"


def _gsi_log():
    """{(層, z, x, y): 行}（取った枚の記録・404 の枚は bytes 0）"""
    if not GSI_LOG.exists():
        return {}
    return {(r["層"], int(r["z"]), int(r["x"]), int(r["y"])): r for r in csv.DictReader(GSI_LOG.open(encoding="utf-8"), delimiter="\t")}


def cmd_gsi(only=None):
    """z+1 の 8×6枚を取る（無い枚だけ・1秒あける・404＝写真の外＝記録に bytes 0）。公的な機関（国土地理院）＝許可不要・robots.txt は無い（11-08 に 404 を確かめた）"""
    import datetime
    import time
    log = _gsi_log()
    new = []
    for code in GSI_COMPOSE:
        if only and code not in only:
            continue
        got = miss = 0
        for layer, z, x, y in _gsi_tiles(code):
            p = _gsi_path(layer, z, x, y)
            if (layer, z, x, y) in log and (p.exists() or log[(layer, z, x, y)]["bytes"] == "0"):
                continue
            url = GSI_URL.format(layer=layer, z=z, x=x, y=y)
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                    b = r.read()
                    ct = r.headers.get("Content-Type") or ""
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    raise SystemExit(f"🔴 {code}: {url} が HTTP {e.code}")
                b, ct = b"", "404"
            time.sleep(1.0)
            if b and not ct.startswith("image/"):
                raise SystemExit(f"🔴 {code}: {url} が画像でない（{ct}）")
            m1 = hashlib.md5(b).hexdigest() if b else ""
            if b:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b)
                got += 1
            else:
                miss += 1
            m2 = md5(p) if b else ""
            if m1 != m2:
                raise SystemExit(f"🔴 {code}: {p.name} の md5 が読み直しで違う")
            new.append([datetime.date.today().isoformat(), layer, str(z), str(x), str(y), str(len(b)), m1, m2, url])
        print(f"  {code}: 取った {got}枚・写真の外（404）{miss}枚")
    if new:
        head = not GSI_LOG.exists()
        with GSI_LOG.open("a", encoding="utf-8", newline="\n") as f:
            if head:
                f.write("\t".join(["取った日", "層", "z", "x", "y", "bytes", "md5", "md5（読み直し）", "URL"]) + "\n")
            for r in new:
                f.write("\t".join(r) + "\n")
    print(f"→ {GSI_LOG.relative_to(HERE).as_posix()}（足した {len(new)}行）")
    return 0


def gsi_compose(code):
    """z+1 の枚を組んで 16:9 に切る＝(RGB の絵, 枚の md5 を並べた md5, 記録の言葉)。記録の md5 と違う枚・記録に無い枚があれば止める（fail closed）"""
    from PIL import Image
    layer, z, x0, y0, nx, ny, (wx, wy, ww) = GSI_COMPOSE[code]
    log = _gsi_log()
    im = Image.new("RGB", (256 * nx, 256 * ny), (0, 0, 0))
    hs, miss = [], []
    for lay, zz, x, y in _gsi_tiles(code):
        r = log.get((lay, zz, x, y))
        if not r:
            raise SystemExit(f"🔴 {code}: 枚 {lay}/{zz}/{x}/{y} を取っていない（`gsi` を先に）")
        if r["bytes"] == "0":
            miss.append(f"{x}_{y}")
            hs.append("404")
            continue
        p = _gsi_path(lay, zz, x, y)
        h = md5(p)
        if h != r["md5"]:
            raise SystemExit(f"🔴 {code}: 枚 {p.name} の md5 が取得の記録と違う")
        hs.append(h)
        with Image.open(p) as t:
            im.paste(t.convert("RGB"), ((x - x0) * 256, (y - y0) * 256))
    wh = round(ww * 9 / 16)
    if wx < 0 or wy < 0 or wx + ww > im.width or wy + wh > im.height:
        raise SystemExit(f"🔴 {code}: 窓 {wx},{wy},{ww}x{wh} が組んだ絵 {im.width}x{im.height} の外へ出る")
    im = im.crop((wx, wy, wx + ww, wy + wh))
    # 写真の外＝真っ黒な面（8×8画素の塊の平均がほぼ0）。森の影や川の暗い画素は1つずつは黒いが塊の平均は上がる（1画素ずつ数えると 3% 前後が出た）
    blocks = list(im.resize((ww // 8, wh // 8), Image.BOX).getdata())
    if sum(1 for p in blocks if sum(p) < 10) / len(blocks) > 0.005:
        raise SystemExit(f"🔴 {code}: 窓の中に写真の外（黒い面）が 0.5% を超えて入る")
    if code in GSI_ONE_PHOTO and any(p[2] - p[0] > 15 for p in blocks):
        raise SystemExit(f"🔴 {code}: 窓の中に青い写真の塊が入る（継ぎ目を入れない窓のはず）")
    how = (f"地理院タイル {layer} z{z} の {nx}×{ny}枚（x {x0}〜{x0 + nx - 1}・y {y0}〜{y0 + ny - 1}）を組み、窓 x{wx} y{wy} {ww}x{wh} を切った・印なし"
           + (f"・写真の外の枚 {len(miss)}（窓の外）" if miss else ""))
    return im, hashlib.md5("".join(hs).encode()).hexdigest(), how


# ── 束を作る ─────────────────────────────────────────────────
def cmd_build(nopages=False):
    """`nopages`＝紙面を撮る前に写真だけ見るとき（台帳は途中の形＝commit しない）"""
    from PIL import Image, ImageOps
    src, fet = _sources(), _fetched()
    db, bad = {}, 0
    later = {}
    us = uses(later)
    if nopages:
        us = {c: u for c, u in us.items() if src[u["code"]]["type"] not in PAGE_TYPES}
    for code in MASK:
        if code not in us:
            print(f"🔴 MASK の {code} は一覧で使っていない")
            bad += 1
    for code in ("P1", "P3"):                            # 🔴 許諾の箱の帰属の指定＝表の3列目（名前は出さない）
        if code in us and not _attr_ok(code):
            print(f"🔴 {code}: 頁の許諾の箱の「Attribution:」の指定が git の外の表の3列目と違う＝画面の {AUTHOR} の字を決め直す")
            bad += 1
    log = None
    for key, u in sorted(us.items()):
        code = u["code"]
        s = src[code]
        name = bundle_name(key, s)
        dst = EPD / f"{name}.jpg"
        t = s["type"]
        box_m = MASK.get(code, [])
        private = is_private(code, s)
        shot = None
        if t in PAGE_TYPES and code in PDF_FILES:
            if key not in PDF_CROP:
                print(f"🔴 {key}: PDF の切り口 PDF_CROP が無い（紙面の段で書く）")
                bad += 1
                continue
            p, smd5 = _pdf_ok(code, fet)
            im, how = render_pdf(key, p)
            notes = [how, "公開リポに置く（著作権法13条の読み）"]
            im = ImageOps.expand(im, border=PAGE_PAD, fill=(255, 255, 255))
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        elif t in PAGE_TYPES:
            log = log or _page_log()
            p, smd5, shot = _page_src(key, s, log)
            with Image.open(p) as im0:
                im = im0.convert("RGB")
            notes = [f"頁の切り口を撮った（{shot}）", "公開リポに置く（規約を読んだ）"]
            if key in PRE_CROP:
                f = PRE_CROP[key]
                im = im.crop((round(im.width * f[0]), round(im.height * f[1]), round(im.width * f[2]), round(im.height * f[3])))
            im = ImageOps.expand(im, border=PAGE_PAD, fill=(255, 255, 255))
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        elif t in NATION_TYPES:
            im, smd5, how = gsi_compose(code)
            notes = [how, "公開リポに置く（PDL1.0・印は描かない）"]
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        else:
            p, smd5 = _src_ok(code, s, fet)
            im, notes = load_photo(p)
            if code in PRE_CROP:
                f = PRE_CROP[code]
                im = im.crop((round(im.width * f[0]), round(im.height * f[1]), round(im.width * f[2]), round(im.height * f[3])))
                notes.append(f"束の段で切り落とした {f}")
            im, k = _shrink(im)
            if k < 1.0:
                notes.append(f"縮小 ×{k:.3f}")
            notes.append(f"{FETCHES[0].name} の md5 と同じ（2回とも）")
            if box_m:
                im = mosaic(im, box_m, MOSAIC_PX)
                notes.append(f"{_mask_words(box_m)}の升目 {len(box_m)}か所（升 {MOSAIC_PX}px）")
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        y, ywhy = year_of(code, s)
        cr = screen_credit(key, s, box_m, u["full"])      # 🆕 31本目：地に敷く切り出しは ground_credit が「／改変なし」→「／改変：切出」に直す（額のカットは無加工のまま）
        frame = t in PAGE_TYPES or t in QUOTE_TYPES or "BY-SA" in s["rights"] or s["rights"].startswith("SDASM")
        url = s["get"].removeprefix("web:").removeprefix("pdf:").split("（")[0]
        url = ("https://" + url) if url and not url.startswith(("http", "commons:", "⑤b", "②")) else url
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(u["main"]), ji=" ".join(u["ji"]), credit=cr, who=who_table(code, s),
                        note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=_lic(code, s), frame=frame, ground=s["basis"][:120], url=url,
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False, page=t in PAGE_TYPES, related=False,
                        quote_page=t in QUOTE_TYPES, named=AUTHOR in cr, mosaic=[list(b[:4]) for b in box_m] or None, name_mosaic=None,
                        masked_before=None, era=s["era"], people=s["people"], private=private, shot=shot)
        print(f"✓ {key:18} {name:18} {w}x{h:<5} 主 {' '.join(u['main']) or '—':14} 地 {' '.join(u['ji']) or '—':26} {_lic(code, s)[:12]}"
              f"{'  額装だけ' if frame else ''}  {'・'.join(notes)[:50]}")
    for j, cs in later.items():
        print(f"・地 {j}＝{JI_LATER[j]}：{len(cs)}カット（{' '.join(cs[:8])}{' …' if len(cs) > 8 else ''}）＝束の外")
    # 🆕 ⑤b-3：イメージの写真（Pexels・地だけの点も）＝取ったファイルそのまま `ref/ep31/stock/<名>.jpg`（🔴 git に入れない＝19本目 決め⑨）。
    #    Actions・Modal は `footage.stock_photos` が台帳の media から取り直して md5 を照らす（23本目の型）
    (EPD / "stock").mkdir(exist_ok=True)
    rows = _list()
    for code, s in sorted(src.items()):
        if s["type"] not in STOCK_TYPES or not s["file"].endswith(".jpg"):
            continue
        r = fet.get(code) or {}
        p = EPD / s["file"]
        if not p.exists() or not r or md5(p) != r["md5"] or r.get("出どころ") != s["get"]:
            print(f"🔴 {code}: 手元の写真が無いか、md5 か直リンクが取得のときと違う（{s['file']}）＝fetch31e.py stock で取る")
            bad += 1
            continue
        main = [x["cid"] for x in rows if _code_of(x["main"]) == code]
        ji = [x["cid"] for x in rows if _code_of(x["ji"]) == code]
        if not main and not ji:
            print(f"🔴 {code}: イメージの写真をどのカットにも当てていない")
            bad += 1
            continue
        name = f"stock/{code.lower()}"
        dst = EPD / f"{name}.jpg"
        dst.write_bytes(p.read_bytes())
        with Image.open(dst) as im:
            w, h = im.size
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(main), ji=" ".join(ji), credit="イメージ（Pexels）", who="投稿者（クレジットは任意＝書かない）",
                        note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h, md5=r["md5"], src_md5=r["md5"], lic="Pexels", frame=False,
                        ground=s["rights"], url=_stock_page(code, s), blur=[], how=f"取ったファイルそのまま（{w}x{h}）", year=None, year_why="この事件の物でない（イメージ）",
                        stock=True, page=False, related=False, quote_page=False, named=False, mosaic=None, name_mosaic=None, masked_before=None, era=s["era"], people=s["people"],
                        private=False, shot=None, media=s["get"][len("stock:"):])
        print(f"✓ {code:7} {name:14} {w}x{h:<5} 主 {' '.join(main) or '—':14} 地 {' '.join(ji) or '—':26} Pexels（git に入れない）")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    pub = [n for n, r in db.items() if not r["private"] and not r["stock"]]
    print(f"→ ref/ep31/assets.json（{len(db)}点＝公開リポに入る {len(pub)}・🔒非公開 {sum(r['private'] for r in db.values())}"
          f"・額装だけ {sum(1 for r in db.values() if r['frame'])}・作者の印 {sum(1 for r in db.values() if r['named'])}・升目 {sum(1 for r in db.values() if r['mosaic'])}"
          f"・地に使う {sum(1 for r in db.values() if r['ji'])}・束の大きさ {tot / 1e6:.1f}MB／公開リポの分 "
          f"{sum((EPD / f'{n}.jpg').stat().st_size for n in pub) / 1e6:.1f}MB）")
    return 1 if bad else 0


def cmd_pdflines(codes):
    import fitz
    (SRC / "pages").mkdir(exist_ok=True)
    for code in codes:
        d = fitz.open(SRC / PDF_FILES[code])
        out = SRC / "pages" / f"{code}_pdflines.txt"
        with out.open("w", encoding="utf-8", newline="\n") as f:
            for i, pg in enumerate(d):
                for t, b in _pdf_lines(pg):
                    f.write(f"p{i + 1} y{b[1]:5.0f}-{b[3]:4.0f} x{b[0]:4.0f}-{b[2]:4.0f} {t[:70]}\n")
        print(f"→ {out.relative_to(HERE).as_posix()}（{len(d)}頁・🔴 線の字が入る＝Read で開かない）")
    return 0


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
    """束の画素の切り出し（k 倍・束の画素で 10px ごとの目盛り＝升目の範囲を読むため）＝out/ep30_look/crop_<名>_<x0>_<y0>.jpg"""
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
        m = PE.margins(f"ep31/{n}.jpg")
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


def cmd_credits(write=False):
    """撮影年＝year_of（出どころつき）。主に当てたカットの副題が名乗る年（「NNNN年」）と食い違えば止める（地に使うカットの副題は図の中身の年＝照らさない）。
    作者の名乗り（scene_jiko._ep31_person）を当てて出典の行の字幅を測る（名前は出さない＝字数だけ）"""
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
        leak = hits_in(json.dumps({k: v for k, v in r.items() if k != "url"}, ensure_ascii=False), names)
        if leak:
            print(f"🔴 {n}: 台帳の行に出さない名前が入っている（{len(leak)}語）")
            bad += 1
        line = r["credit"]
        if "{帰属}" in line:
            print(f"🔴 {n}: 印 {{帰属}} は使わない（8列目は許諾の雛形の取り違え＝画面は {AUTHOR}）")
            bad += 1
        if AUTHOR in line:
            try:
                line = line.replace(AUTHOR, SJ._ep31_person(f"ep31/{n}.jpg", AUTHOR))
            except Exception as e:                     # noqa: BLE001  焼く前に止める
                print(f"🔴 {n}: 名乗りが作れない（{e}）")
                bad += 1
        wd = _width(line)
        if wd > CREDIT_W_MAX:
            print(f"🔴 {n}: 出典の行の字幅 {wd:.1f}（{CREDIT_W_MAX} まで＝画面の左下からはみ出すおそれ）")
            bad += 1
        cj[f"ep31/{n}.jpg"] = r["credit"]
        kind = "公的な機関の頁" if r["page"] else ("国土地理院の空中写真" if r["lic"] == "PDL1.0" else "この回の物と場所")
        cr_ = r.get("credit") or ""
        mod = ("・顔とナンバーに升目" if "顔とナンバー" in cr_ else "・ナンバーに升目" if "ナンバーにモザイク" in cr_ else "・顔に升目") if r.get("mosaic") else ""
        use = " ".join(cuts) + (f"（地 {r['ji']}）" if r["ji"] else "")
        url = r["url"]                                       # Commons は「commons:ファイル名」（頁の URL は git の外の表）。撮影者の名はファイル名に無い点だけ＝網で見る
        rows.append(f"| `{Path(n).name}` | {use or '—'} | {y if y else '不明'} | {r['lic']}（{kind}{mod}） | {r['who']} | {url} |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真と紙面 {len(cj)}点{'' if not bad else f'・🔴 {bad}'}")
    if bad:
        return 1
    if not write:
        return 0
    CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    film_rows = []
    if CLIPS.exists():
        films = _film_codes()
        for k, v in json.loads(CLIPS.read_text(encoding="utf-8")).items():
            film_rows.append(f"| `{k}` | {' '.join(films.get(k, []))} | {v['credit']} | {v['license']} | {v['url']} | {v['got']} |")
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-11-08（⑤b-2）。`qa_out/ep31_assets.py credits --write` が書く（手で直さない）。写真と紙面は映像方針の一覧 `ref/ep31/eizou_list31.md`（了承② 2026-11-08）。",
        "🔴 この回の線（台本 §1-4）＝亡くなった方・遺族・操縦者・乗員・役人・裁判官・弁護人の名前は書かない（立場だけ）。報道の写真・遺体・遺品・搬送の秒は使わない。",
        "",
        "### 0. 素材の読み（⚠️ 法律の助言ではない＝こちらの読み）",
        "- Commons の写真＝頁の許諾の箱（`licensetpl_short`）で読んだ（11-08）。BY-SA＝額装・無加工・1点1カット（P1 事故機 JA8329 は冒頭 c103 だけ）。P1・P3 は許諾の箱の「Attribution:」の指定どおりの名乗り（git の外の表の3列目と同じ＝束の道具が照らす）",
        "- SDASM Archives（P5）＝Flickr の The Commons（著作権の制限は知られていない）＝PD と書かない・地にしない",
        "- 国土地理院の空中写真＝地理院タイル（PDL1.0 の読み・公共データ利用規約 第1.0版）＝組んで切り出す・印は描かない・出典の行に「加工して作成」",
        "- 公的な機関の紙面＝判決・法令（著作権法13条の読み）・国会会議録の答弁（40条の読み）・運輸白書と国交省の記者発表（PDL1.0）＝切り出す・名前の行を切り口に入れない（同じ行の名前は字だけ隠す）・出典の行に「／改変：切出」",
        "",
        "### 1. 写真と紙面（Commons の CC BY・BY-SA・CC0・SDASM・国土地理院の空中写真・公的な機関の紙面）",
        "- CC BY・BY-SA・CC0＝「写真：{作者}／Wikimedia Commons（ライセンス）」。🔴 撮影者の名前はこのリポに書かない＝`ref/ep31/credits.json` は印 `{作者}` だけ・"
        "焼くときに git の外の表 `ref/ep31/src/credits_private.tsv` の3列目から足す（`tools/scene_jiko.ep31_credit`）",
        "- BY-SA＝額装（無加工・1点1カット・升目もかけない＝人とナンバーが写っていない点だけ）。CC BY・CC0 の私人の顔とナンバーは升目（「／改変：…にモザイク」）。公的な任務の顔はそのまま。色は原本のまま",
        "- 説明カットの地（「地 c…」）＝CC BY・CC0・PDL1.0 の写真を暗くするだけ（字と地の比 8:1 が下限・出典の行は「地の写真：…／改変：切出・明るさ」・国土地理院は「加工して作成」）",
        "- 撮影年＝Commons の頁の撮影日・地理院の層（gazo1＝1974〜1978年）・文書の日付（`sources31.psv` の時期の欄）。表示に年の無い点は「不明」＝副題に年を書かない",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. 動く映像＝clips.json（防衛庁記録・イメージの Pexels）",
        "- 防衛省・自衛隊『昭和46年防衛庁記録』（CC BY 3.0＝公式の YouTube `HK0v9n-PTIM` の表示と Commons の写し）＝章「雫石事故」と章「航空自衛隊部隊改編」の区間だけ・4:3 の白黒・音は使わない。"
        "新聞の紙面・積み込み・参列者の近景の秒は使わない（`footage.NOGO`）。出典の行に「改変：切出・再生速度」",
        "- フリー素材（Pexels・AI で作った絵は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」だけ（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。"
        "20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）",
        "",
        "### 3. 地図の描き足し（⑤b-3b）",
        "- 衛星写真＝Google マップ（帰属は地図の右下・PNG は公開リポに置かない＝保管庫）。J11L の線と空域「盛岡」の円は概略（資料の言葉から描いた）",
        "",
        "| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 | 取った日 |",
        "|---|---|---|---|---|---|", *film_rows,
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


# ── 動く映像＝台帳 clips.json・ショット shots.json・見取り図・USE・ひかえ（防衛庁記録 MS・MK＝⑤b-2・イメージ〈Pexels〉＝⑤b-3a・26本目の型）──────────
# 🆕 防衛庁記録『昭和46年』＝Commons の変換版 1080p の全体（MS・MK は同じファイルの2つの章）。手元の src/bouei/ は区間の写し（手元の秒＝元の秒−off）
S46_PAGE = "https://commons.wikimedia.org/wiki/File:%E6%98%AD%E5%92%8C%EF%BC%94%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm"
S46_MEDIA = ("https://upload.wikimedia.org/wikipedia/commons/transcoded/a/a7/%E6%98%AD%E5%92%8C%EF%BC%94%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm/"
             "%E6%98%AD%E5%92%8C%EF%BC%94%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm.1080p.vp9.webm")
S46_SIZE = 930511405                   # 変換版の大きさ（11-08 に HEAD で読んだ＝clips で照らす）
S46_SEC = 2006.834                     # 変換版の長さ（11-08 に ffprobe の format=duration で読んだ）＝footage の「動画の終端を越える」の物差し
# 🔴 off＝手元の写しの頭のキーフレームの元の秒（11-08 に変換版を ffprobe の範囲読みで測った＝MS 1097.997・MK 996.195。materials.md の MS 1098.5 は 0.503秒ずれていた）
# edges＝場面の切れ目（元の秒＝切り替えのコマの頭・手元の写しの隣のコマの灰色の差＝64×36・中身の列だけ）。章の外は表に入れない
#   🔧 11-08 の測り直し（scratchpad cuts31b.py）：1本目（cuts31.py＝隣の3倍）は2コマ続く切り替えを打ち消して落とした（半旗 1208.874・式 1136.469）＝
#      差 ≥ max(8, 前後15コマの中央値の4倍)・3コマ以内に続く山は1つ。区間は切り替えの尻（頭＋続くコマ）より後から始める
FILM = {"MS": dict(off=1097.997, file="src/bouei/s46_1105-1245_1080p.webm", md5="eb5364d81a2bd3b2f8f0d87e2d6f01ff",
                   what="昭和46年防衛庁記録（章「雫石事故」元 18:34〜20:38）",
                   edges=(1117.350, 1120.486, 1123.322, 1130.663, 1134.700, 1136.469, 1144.377, 1145.378, 1146.712, 1147.680, 1148.381, 1157.223,
                          1161.827, 1164.830, 1169.902, 1174.106, 1183.950, 1193.893, 1194.226, 1194.393, 1198.931, 1205.371, 1208.874, 1212.078,
                          1217.083, 1220.953, 1227.059, 1230.429, 1237.470)),
        "MK": dict(off=996.195, file="src/bouei/s46_1005-1077_1080p.webm", md5="3b29ef6d79f3d945460516bbc47bc09c",
                   what="昭和46年防衛庁記録（章「航空自衛隊部隊改編」元 16:50〜17:54）",
                   edges=(1009.275, 1019.752, 1026.959, 1030.963, 1034.066, 1038.437, 1048.814, 1058.758, 1063.763, 1067.833, 1073.305))}
# 🔴 外す秒＝その秒を含むショットまるごと（切り替えの尻まで）＋前後 0.5秒（make_list31.EXCLUDE と同じ切れ目）。footage.NOGO の印 EP31_NOGO のあいだに書く
FILM_NOGO = {"MS": [(1113.346, 1117.917, "新聞の紙面（報道と犠牲者の顔写真）"), (1130.163, 1135.267, "包んだ物の積み込み（搬送と見る）"),
                    (1220.453, 1227.626, "参列者の近景（遺族が含まれうる）")]}
# 🔴 31本目の MS・MK は15カットとも額装（高さいっぱい）＝footage.PILLAR は書かない（書くと額の中が 1/PILLAR 倍に寄って上下が切れる）。
#    器 1920×1080 の中身は x 252〜1660（幅1409＝4:3 より細い・11-08 に7＋5コマの列の中央値で測った）＝箱（ひかえの静止画の縦横比）に当てると
#    左右の内側に器の黒が 4px ほど残る＝寄り 1.02（切り口 x 270〜1650）。ひかえの静止画は中身の x 254〜1658 を切る
FILM_ZOOM = 1.02
FB_BOX = (254, 0, 1658, 1080)


def _film_codes():
    """映像の記号 → 使うカット（一覧の順）。イメージの写真（src/stock/*.jpg）は映像でない＝束の `stock/`（cmd_build）"""
    src = _sources()
    out = {}
    for r in _list():
        code = _code_of(r["main"])
        s = src.get(code, {})
        if s.get("type") == "commons-video" or (s.get("type") in STOCK_TYPES and s.get("file", "").endswith(".mp4")):
            out.setdefault(code, []).append(r["cid"])
    return out


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


def _head(u):
    req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, int(r.headers.get("Content-Length") or 0), r.headers.get("Content-Type") or ""


def _stock_page(code, s):
    """頁の URL＝sources30 の basis の頭（13列のまま＝get は直リンクが持つ）"""
    m = re.match(r"https://www\.pexels\.com/(?:video|photo)/\S+?/(?=[（ ]|$)", s["basis"])
    if not m:
        raise SystemExit(f"🔴 {code}: basis の頭に Pexels の頁の URL が無い（{s['basis'][:60]}）")
    return m.group(0)


def cmd_clips():
    """clips.json＝防衛庁記録 MS・MK とイメージ（Pexels・⑤b-3a）。手元の写しの md5 を FILM と照らし、変換版の直リンクを HEAD で引いて大きさを見る"""
    src, fet = _sources(), _fetched()
    out = {}
    head = None
    for code, cuts in _film_codes().items():
        s = src[code]
        r = fet.get(code) or {}
        rec = r.get("出どころ") or ""
        if s["type"] == "commons-video":
            f = FILM[code]
            p = EPD / f["file"]
            if not p.exists() or md5(p) != f["md5"]:
                raise SystemExit(f"🔴 {code}: 手元の写しが無いか、md5 が materials.md の記録と違う（{f['file']}）")
            head = head or _head(S46_MEDIA)
            st, n, ct = head
            if st != 200 or n != S46_SIZE or not ct.startswith("video/"):
                raise SystemExit(f"🔴 {code}: 変換版の直リンクが台帳と違う（http {st}・{n} B／台帳 {S46_SIZE} B・{ct}）")
            loc = _probe(p)
            out[code] = dict(url=S46_PAGE, media=S46_MEDIA, credit=s["credit"], src="mod", at=0.0, date="1971", stock=False,
                             what=f["what"], got="2026-11-07", w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"],
                             sec=S46_SEC, size=S46_SIZE, dispw=loc["w"], decoded=[loc["w"], loc["h"]], license="CC BY 3.0",
                             rights="CC BY 3.0（防衛省・自衛隊の YouTube 公式 HK0v9n-PTIM・Commons の同じ版）", scan=f"ref/ep31/{f['file']}", md5_scan=f["md5"],
                             local_off=f["off"], content_x=[252, 1660],
                             note="音は使わない。手元の写しの秒＝元の秒−local_off（⑤b-2 に変換版のキーフレームを ffprobe の範囲読みで測った）。"
                                  "器 1920×1080 に4:3 の白黒（中身 x 252〜1660）＝31本目は額装だけ（PILLAR なし・寄り 1.02）")
            print(f"  {code:5} {loc['w']}x{loc['h']} {loc['fps']}fps 手元 {loc['sec']:.2f}秒 off {f['off']} {' '.join(cuts)}  HEAD {st}（{n} B）")
            continue
        if not p.exists() or not r or md5(p) != r["md5"] or not rec.startswith("stock:http") or rec != s["get"]:
            raise SystemExit(f"🔴 {code}: 手元の映像が無いか、md5 か直リンクが取得のときと違う（{s['file']}）＝fetch30.py stock で取る")
        size, media = p.stat().st_size, rec[6:]
        try:
            st, n, ct = _head(media)
        except Exception as e:                               # noqa: BLE001
            raise SystemExit(f"🔴 {code}: 記録の直リンクを引けない（{media}・{e}）")
        if st != 200 or n != size or not ct.startswith("video/"):
            raise SystemExit(f"🔴 {code}: 記録の直リンクが手元と違う（http {st}・{n} B／手元 {size} B・{ct}）")
        loc = _probe(p)
        out[code] = dict(url=_stock_page(code, s), media=media, stock=True, file=f"ep31/{s['file']}", credit="イメージ（Pexels）", src="stock",
                         at=0.0, what=s["title"][:60], got=r["取った日"], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(loc["sec"], 3),
                         size=size, md5=r["md5"], dispw=loc["w"], decoded=[loc["w"], loc["h"]], license="Pexels License",
                         license_url="https://www.pexels.com/license/", site="Pexels")
        print(f"  {code:5} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.2f}秒 {size / 1e6:.1f}MB  {' '.join(cuts)}  HEAD {st}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep31/clips.json（{len(out)}本）")
    return 0


# フリー素材で、動きの速い素材の隣の1秒の差がしきい値を超えて出た「境目」を、根拠つきで1ショットに直す（25・26本目 SHOT_ONE の型）
#   根拠＝境目の前後の全コマの隣の差に、1コマに集まる跳ねが無い（切り替わりなら1コマに集まる）。⚠️ 記号は素材を替えても同じ＝替えたら測り直す
#   ⑤b-3（11-02）に 10コマ/秒の隣の差を測った（scratchpad clip_probe.py）・コマを並べて同じカメラの1回の撮影と見た（動きの速い手・足で 1秒の差が超えた）
#   30本目 ⑤b-3（11-05）＝同じ物差し（隣の差の最大÷中央値 X703 1.6・X710 1.3・Xc17 3.0＝前後のコマも高い）。頭・真ん中・尻を 640px で見て同じカメラの1回の撮影
SHOT_ONE = {"X703": "手持ちで通路を歩く1回の撮影", "X710": "前面の1回の撮影（速い）", "Xc17": "据えたカメラの長時間露光（人の流れの量で差が動く）"}


def cmd_shots():
    """shots.json＝防衛庁記録は FILM の edges（灰色の差で測った）・イメージは tools/shots.shots_of（1秒1コマ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import shots as SH
    src = _sources()
    out = {}
    for code in _film_codes():
        s = src[code]
        p = EPD / s["file"]
        if s["type"] == "commons-video":
            ed = FILM[code]["edges"]
            sh = [dict(start=a, until=b, motion=0.0) for a, b in zip(ed, ed[1:])]
            out[code] = dict(src=S46_MEDIA, scan=f"ref/ep31/{FILM[code]['file']}", dur=round(ed[-1] - ed[0], 3),
                             how="⑤b-2（11-08）：手元の写し（29.97コマ/秒・64×36 の灰色・中身の列だけ）の隣のコマの差の山（差 8 以上・隣の3倍の 0.8倍以上）を"
                                 "キーフレームで測った off で元の秒に直した。章の外は表に入れない＝USE に書けば止まる",
                             shots=sh)
            print(f"  {code:5} ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
            continue
        if not p.exists():
            print(f"  ⚠️ {code}: 手元に無い")
            continue
        sh, dur = SH.shots_of(p)
        how = "1秒1コマで tools/shots.shots_of（31本目・フリー素材）"
        if code in SHOT_ONE:
            sh = [dict(start=0.0, until=float(sh[-1]["until"]), motion=max(x["motion"] for x in sh))]
            how += f"・🔧 1ショットに直した（{SHOT_ONE[code]}）"
        out[code] = dict(src=_stock_page(code, s), scan=f"ref/ep31/{s['file']}", dur=round(dur, 1), how=how, shots=sh)
        print(f"  {code:5} {dur:6.1f}秒  ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep31/shots.json（{len(out)}本）")
    return 0


def cmd_frames(code, step=1.0, width=384, cols=5):
    """映像の step 秒ごとのコマを並べた見取り図（秒の札つき）＝区間を選ぶとき（out/ep30_look/frames_<記号>.jpg）"""
    from PIL import Image, ImageDraw
    p = EPD / _sources()[code]["file"]
    loc = _probe(p)
    hh = round(width * loc["h"] / loc["w"])
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"fps=1/{step},scale={width}:{hh}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, timeout=600)
    n = len(r.stdout) // (width * hh * 3)
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * width + (cols - 1) * 4, rows * hh + (rows - 1) * 4), (30, 30, 30))
    for i in range(n):
        im = Image.frombytes("RGB", (width, hh), r.stdout[i * width * hh * 3:(i + 1) * width * hh * 3])
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 70, 20), fill=(0, 0, 0))
        d.text((4, 4), f"{i * step + step / 2:5.1f}s", fill=(255, 255, 0))
        sheet.paste(im, ((i % cols) * (width + 4), (i // cols) * (hh + 4)))
    SCRATCH.mkdir(parents=True, exist_ok=True)
    out = SCRATCH / f"frames_{code}.jpg"
    sheet.save(out, quality=88)
    print(f"→ {out}（{n}コマ・{sheet.size[0]}x{sheet.size[1]}・{loc['sec']:.2f}秒）")
    return 0


def _write_block(tag, lines):
    txt = FOOTAGE.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in txt else "\n"              # 🔴 25本目 ⑤b-1 の落とし穴＝改行を見分ける
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_bytes((txt[:m.start(2)] + "".join(x + nl for x in lines) + txt[m.end(2):]).encode("utf-8"))


# 寄せ（footage.USE の zoom・bias・xbias）＝写したくない物を窓の外へ（🔴 区間は一覧 list30.tsv の動きの欄「映像 a〜b秒」から読む＝手で写さない）
STOCK_GEOM = {"c204": dict(zoom=1.06, xbias=0.0),    # c204＝ホームの右端の人を画面の外へ（⑤b-3 に 640px で見た）
              "cb20": dict(zoom=1.7, bias=0.0)}      # cb20＝柵の張り紙（駅名と時刻が読める）と車内の人を画面の外へ（⑤b-3 に焼いた絵で見た・1.4 では車内の人が残った＝幅2560の版で寄る）
def cmd_use(only=None, all_=False):
    """footage.USE の31本目の欄。区間・速さ・止めは一覧 list31.tsv の動きの欄「映像 a〜b秒（r倍速）（＋止め n秒）」から読む（make_list31 の門番 gate_video と同じ物差し）。
    防衛庁記録＝額装（寄り FILM_ZOOM）・止めは hold・ショットをまたぐ欄は edit=True（元の記録映画の編集のまま）。イメージは区間を1つのショットに収める。
    🔴 章ファイルに `ss.vid` を書いたカットだけ（`only` は書く前の鶏と卵を割るため・`--all` は全欄）"""
    sys.path.insert(0, str(HERE / "tools"))
    sys.path.insert(0, str(BUILD))
    import make_list31 as ML
    if only:
        spec = {}
    else:
        import scene_jiko as S
        spec = S.SPEC
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    lines, skip = [], []
    films = _film_codes()
    for r in _list():
        code = _code_of(r["main"])
        if code not in films:
            continue
        cid = r["cid"]
        wrote = str((spec.get(cid) or {}).get("photo") or "").endswith(f"fb_{cid}.jpg")
        if not (all_ or wrote or (only and cid in only)):
            skip.append(cid)
            continue
        win = ML.windows(r["motion"])
        if len(win) != 1:
            raise SystemExit(f"🔴 {cid}: 一覧の動きの欄に区間「映像 a〜b秒」が1つでない（{r['motion']}）")
        a, b = win[0]
        hold, rate = ML.video_opts(r["motion"])
        need = float(r["cont"])
        if rate < STILL_BELOW:
            raise SystemExit(f"🔴 {cid}: 倍速 {rate}＜{STILL_BELOW}（§5b-17b＝静止画に替える）")
        if code in FILM:
            ed = FILM[code]["edges"]
            if not ed[0] <= a < b <= ed[-1]:
                raise SystemExit(f"🔴 {cid}: 区間 {a}〜{b} が章の中（{ed[0]}〜{ed[-1]}）でない")
            cross = [e for e in ed if a < e < b]
            reads = (need - hold) * rate
            if a + reads > b + 1e-6:
                raise SystemExit(f"🔴 {cid}: 読む秒 {reads:.2f} が区間 {b - a:.2f} を越える（止めか速さを直す）")
            lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate={rate}{f", hold={hold}" if hold else ""}, zoom={FILM_ZOOM}'
                         f'{", edit=True" if cross else ""}),   '
                         f'# 読む {reads:.2f}秒（〜{a + reads:.2f}）／区間 {b - a:.2f}秒・要る {need:.2f}秒・元の編集の切れ目 {" ".join(f"{e:g}" for e in cross) or "なし"}')
            continue
        hit = [x for x in sd[code]["shots"] if x["start"] <= a < x["until"]]
        if len(hit) != 1 or b > hit[0]["until"] + 1e-6:
            raise SystemExit(f"🔴 {cid}: 区間 {a}〜{b} が1つのショットに収まらない（{[(x['start'], x['until']) for x in hit]}）")
        sh = hit[0]
        geo = "".join(f", {k}={v}" for k, v in STOCK_GEOM.get(cid, {}).items())
        lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate={rate}{geo}),   '
                     f'# ショット {sh["start"]:g}〜{sh["until"]:g}秒・使う {b - a:.2f}秒／要る {need:.2f}秒')
    _write_block("EP31_USE", lines)
    _write_block("EP31_NOGO", [f'    "{k}": {v!r},' for k, v in FILM_NOGO.items()])
    print(f"→ tools/footage.py USE {len(lines)}欄・NOGO {sum(len(v) for v in FILM_NOGO.values())}区間")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）。イメージ＝区間の頭のコマを 1920×1080 に（寄せは USE と同じ式）＝`ref/ep31/stock/fb_<cid>.jpg`（🔴 git に入れない＝決め⑨）。
    防衛庁記録＝区間の頭のコマの中身（FB_BOX＝器の黒帯を外す・20本目の型）＝`ref/ep31/fb_<cid>.jpg`（CC BY 3.0・公開リポに置く）＝箱の縦横比になる（額装）"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    from PIL import Image
    bad = 0
    (EPD / "stock").mkdir(exist_ok=True)
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
        c = FO.CLIPS.get(u["clip"]) or {}
        if c.get("local_off") is not None:
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{float(u['start']) - float(c['local_off']):.3f}", "-i", str(HERE / c["scan"]), "-frames:v", "1",
                                  "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
            if not raw:
                print(f"🔴 {cid}: コマが取れない")
                bad += 1
                continue
            dst = EPD / f"fb_{cid}.jpg"
            Image.open(io.BytesIO(raw)).convert("RGB").crop(FB_BOX).save(dst, quality=92)
            print(f"✓ {cid:5} {u['clip']:5} {float(u['start']):7.2f}秒 → {dst.relative_to(HERE).as_posix()}")
            continue
        if not c.get("stock"):
            continue
        p = HERE / "ref" / c["file"]
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{float(u['start']):.3f}", "-i", str(p), "-frames:v", "1",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not raw:
            print(f"🔴 {cid}: コマが取れない")
            bad += 1
            continue
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        sw, sh_ = im.size
        z = max(1920 / sw, 1080 / sh_) * float(u.get("zoom", 1.0))
        cw, ch = min(sw, 1920 / z), min(sh_, 1080 / z)
        lft, top = (sw - cw) * float(u.get("xbias", 0.5)), (sh_ - ch) * float(u.get("bias", 0.5))
        im = im.crop((round(lft), round(top), round(lft + cw), round(top + ch))).resize((1920, 1080), Image.LANCZOS)
        dst = EPD / "stock" / f"fb_{cid}.jpg"
        im.save(dst, quality=92)
        print(f"✓ {cid:5} {u['clip']:5} {float(u['start']):6.2f}秒 {sw}x{sh_} → {dst.relative_to(HERE).as_posix()}")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"panel": cmd_panel, "edges": cmd_edges, "clips": cmd_clips, "shots": cmd_shots}
    if a and a[0] == "gsi":
        sys.exit(cmd_gsi(set(a[1:]) or None))
    if a and a[0] == "uses":
        _later = {}
        for _k, _u in sorted(uses(_later).items()):
            print(f"{_k:20} 主 {' '.join(_u['main']) or '—':24} 地 {' '.join(_u['ji']) or '—'}")
        for _j, _cs in _later.items():
            print(f"・地 {_j}＝{JI_LATER[_j]}：{len(_cs)}カット")
        sys.exit(0)
    if a and a[0] == "build":
        sys.exit(cmd_build("--nopages" in a))
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] == "use":
        sys.exit(cmd_use(set(x for x in a[1:] if not x.startswith("--")) or None, "--all" in a))
    if a and a[0] == "frames":
        sys.exit(cmd_frames(a[1], float(a[2]) if len(a) > 2 else 1.0))
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "pdflines":
        sys.exit(cmd_pdflines(a[1:]))
    if a and a[0] == "look":
        sys.exit(cmd_look(a[1:]))
    if a and a[0] == "crop":
        sys.exit(cmd_crop(a[1], *map(int, a[2:6]), float(a[6]) if len(a) > 6 else 2.0))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
