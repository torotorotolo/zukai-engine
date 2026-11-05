# -*- coding: utf-8 -*-
"""ep30_assets.py — 30本目（地下鉄サリン事件）の写真と紙面の束・出典（⑤b-2・2026-11-05）。29本目 `ep29_assets.py` の形を、
30本目の台帳（`sources30.psv` の13列〈見出しの行で読む・「同上」は上の行〉・`fetch30.tsv`〈md5 を2回〉・頁の撮影の記録 `src/pages/log.tsv`・
git の外の表 `src/credits_private.tsv`〈Commons の撮影者＝頭の行なし〉・`src/credits_quote_private.tsv`〈資料館の個人の提供者＝頭の行あり〉）に合わせた。
イメージ（Pexels）は ⑤b-3＝束に入れない。防衛省の記録 M6 は clips.json・shots.json（`clips`・`shots`・`use`）。

  python -P qa_out/ep30_assets.py build             # 束 ref/ep30/<名>.jpg（第三者の引用＝ref/ep30/police/）＋ 権利の台帳 ref/ep30/assets.json
  python -P qa_out/ep30_assets.py pdflines JC …     # PDF の字の層の行（頁・y）を src/pages/<記号>_pdflines.txt へ（🔴 線の字が入る＝Read で開かない・切り口 PDF_CROP を選ぶ）
  python -P qa_out/ep30_assets.py look P65 …        # 束の写真を並べた見本（out/ep30_look/・1枚 960 幅）
  python -P qa_out/ep30_assets.py crop P65 x0 y0 x1 y1 [倍]   # 束の画素の切り出し（既定2倍・10px の目盛り）＝人とナンバーを決めるとき
  python -P qa_out/ep30_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python -P qa_out/ep30_assets.py edges             # 束の四辺の暗い帯＝門番 check_photo_edge の名簿（SLIDE_MOUNT／SLIDE_NOT_MOUNT）を決める
  python -P qa_out/ep30_assets.py credits [--write] # 画面の出典 ref/ep30/credits.json と ref/CREDITS.md の30本目の節
  python -P qa_out/ep30_assets.py clips｜shots｜use  # 防衛省の記録 M6 の台帳・場面の切れ目・footage.USE の6欄（一覧の動きの欄から読む）

🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色）＝幅 2400 か高さ 1350 の大きい方まで（小さい写真は原画のまま）。
🔴 第三者の引用（東京消防庁・東京地下鉄・地元の個人＝資料館の「提供：○○」・ルール §2-39）＝**公開リポに置かない**（引用は禁止の外だが、置くと再配布に見える）＝`ref/ep30/police/`
   （`git add` しない）・台帳の `private`。焼くのは Modal（保管庫 jiko-assets の同じ道＝`modal_app.pull_private`）。⚠️ Actions は保管庫を読めない。⚠️ 法律の助言ではない＝こちらの読み。
🔴 国の写真（陸上自衛隊の提供・資料館の表示に提供の無い点・法務省の写真）＝PDL1.0 の読み（§2-39）＝公開リポに置く・切り出してよい・出典の行に「加工して作成」。
🔴 公的な機関の頁（⑤b-2 に規約を読んだ）＝公開リポに置く・切り出すので出典の行に「／改変：切出」。ロゴは写さない。🔴 判決は著作権の対象外（著作権法13条の読み）。
🔴 この回の線（ルール §B2-12）と名前＝紙面の切り口に線の行と名前の行を入れない（親が絵を見て切る・`outside` で字の層でも止める）。名前は台帳・出典の行・CREDITS.md に書かない
   ＝撮影者は印 `{作者}`・個人の提供者は印 `{個人}` だけ（焼くときに `scene_jiko._ep30_person` が git の外の表から足す）。
🔴 人とナンバー（了承②）＝公的な任務の顔はそのまま。場所の写真の私人の顔とナンバーは CC BY・CC0・PD で升目（MASK）・**BY-SA は升目も翻案＝かけない**（読める顔やナンバーがあれば別の点に）。
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
EPD = HERE / "ref" / "ep30"
SRC = EPD / "src"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list30.tsv"
SOURCES = BUILD / "sources30.psv"
FETCHES = (BUILD / "fetch30.tsv",)
PAGE_LOG = SRC / "pages" / "log.tsv"          # 頁の撮影の記録（git の外・撮った日時・URL・md5）
PRIVATE = SRC / "credits_private.tsv"         # 🔴 git の外（Commons の撮影者＝頭の行なし・列 記号・ファイル・作者…）＝ここから名前を公開の物へ写さない
PRIVATE_QUOTE = SRC / "credits_quote_private.tsv"   # 🔴 git の外（資料館の個人の提供者＝頭の行あり・列 記号・名）
NAME_FILES = (SRC / "names_private.txt",)     # 🔴 git の外（出さない名前）
DB = EPD / "assets.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
FOOTAGE = HERE / "tools" / "footage.py"
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（footage.py の注）
UA = "zukai-engine/1.0 (accident-documentary research; https://github.com/torotorotolo/zukai-engine)"
SCRATCH = HERE / "out" / "ep30_look"          # look・crop の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## 地下鉄サリン事件（1995-03-20・30本目）"
AUTHOR = "{作者}"            # CC BY・BY-SA の出典の行の印（焼くときに git の外の表から足す＝scene_jiko.ep30_credit）
PERSON = "{個人}"            # 資料館の個人の提供者の印（同じ・git の外の src/credits_quote_private.tsv）
EVENT_YEAR = 1995            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 92
MOSAIC_PX = 14                         # 升目の大きさ（束の画素）
COMMONS_TYPES = ("commons-photo",)                   # 語りに出る場所の写真（CC BY・BY-SA・CC0・PD）
NATION_TYPES = ("public-photo",)                     # 国の写真（陸上自衛隊の提供・慰霊碑・立入検査）＝PDL1.0 の読み＝公開リポに置く
QUOTE_TYPES = ("quote-photo",)                       # 第三者の写真＝引用・公開リポに置かない
PHOTO_TYPES = COMMONS_TYPES + NATION_TYPES + QUOTE_TYPES
PUBLIC_TYPES = ("public-page", "public-pdf")         # 公的な機関の頁と PDF（規約を読んだ＝公開リポに置く）
PAGE_TYPES = PUBLIC_TYPES
STOCK_TYPES = ("stock",)                             # 束に入れない（⑤b-3）
KIND_OK = {"場所": COMMONS_TYPES, "陸自": NATION_TYPES, "公立": NATION_TYPES, "引用": QUOTE_TYPES, "公的": PUBLIC_TYPES}
KIND_OUT = ("映像", "衛星", "イメージ")              # 束の外＝映像は clips.json・衛星は ss.SAT・イメージは ⑤b-3

# PDF の切り口 {記号: dict(page, head, tail, outside)}＝字の層の行で決める（head の行〜tail の行の外接＋余白）。outside＝切り口に入ってはいけない行の字（名前と線の行の目印）
#   🆕 parts＝2頁にまたがる表を縦につなぐ（xbox＝pt の横の範囲を揃える）
PDF_DPI_K = 3.0                        # 描く倍率（1pt＝3画素）
PDF_FILES = {"JC": "hanrei/hanrei-pdf-5817.pdf", "FD1": "shobo/kento088_74_shiryo4.pdf"}
PDF_LOG_MD5 = {"JC": "e0168bafc8490342aa668cd20e0e1932", "FD1": "0a135937a3ee13b7c0cda4cb9e910c10"}   # ②③ に取った手元のファイル（git の外）
# white＝描く前に白で消す範囲（pt）。🔴 1行の中に前の文（JC＝弁護側の主張への答えの尻）や次の文（FD1＝これを受け…）がある＝語りの1文だけを見せる
PDF_CROP = {
    # c212 判C p.42「したがって，本件犯行は，強制捜査を一時しのぎ的に回避することを目的とするものとみるほかはなく，…いえないのである。」の1文（字の層で測った＝行 y143.9〜179.9・「したがって」x420）
    "JC": dict(page=42, head="したがって", tail="とはいえないのである", xbox=(66, 522), ybox=(144.2, 180.0), white=[(66, 144.2, 419.5, 155.9)], k=4.0),
    # c820 消防庁の資料 p.1「地下鉄サリン事件において、…消防職員135 人も負傷した。」の1文（行 y708.7〜740・「。」の右 x190.1）。🔴 次の文は切り口の外（白で消す）
    #   🔴 2行目は x85 から「135」＝左を x90 で切ると「35 人」になった（束の絵を原寸で見て気づいた）＝左は行の頭より外
    "FD1": dict(page=1, head="地下鉄サリン事件において", tail="人も負傷した", xbox=(80, 530), ybox=(708.0, 741.0), white=[(190.6, 727.5, 530, 741.0)], k=4.0),
}
PAGE_PAD = 24                          # 紙面の絵のまわりの白（束の画素）＝字が額の縁に触れない
HIDDEN = {"PA1": "・名前を隠した", "PA2": "・文を隠した"}   # 紙面の中で隠した所の断り（内蔵ブラウザの中で描くときに隠した＝src/pages/log.tsv）

# 升目 {記号: [(x0, y0, x1, y1, 札)]}（束の画素）。札が「ナンバー：」で始まる箱＝ナンバー・それ以外＝顔（出典の行の断りを分ける）。⑤b-2 に原寸で見て決める
#   ✕ 升目にしない（⑤b-2 に原寸で見た 11-05）：DIET の車は警察の車（公的な任務）でナンバーは柱の陰・SLH の銀の車はナンバーが自転車の陰・KG1 と KG2 の車は小さくて読めない・
#      KAS の人（投稿者が顔をぼかしてある・左の列は背中）・TSE の人（背中と傘）・P83 と P84 は自衛隊と警察の車。
#      🔴 第三者の引用は升目もかけない（無加工）＝P5 のバイクの札「57-32」は上の段が読めない・地名が無く持ち主を特定できない＝そのまま（⑤c で額の大きさで見る）
#      🔴 BY-SA の TKS は人もナンバーも無い＝そのまま額装で使える
MASK = {
    "KS1": [(50, 1020, 76, 1038, "ナンバー：左のワゴン")],
    "HB": [(150, 1405, 210, 1465, "左の人"), (262, 1432, 520, 1495, "奥の人の列")],
}

# 🆕 束の段で切り落とす＝絵に入れない（顔の多い人の列・看板の顔は、升目より切る方が画面がきれい＝記憶 feedback-jiko-photo-people-policy の「切り出しで人を外す」）
#   {記号: (左, 上, 右, 下)}＝元の絵に対する割合。縮める前に切る（紙面は白の余りを切る）
PRE_CROP = {
    "P62": (0.0, 0.178, 1.0, 1.0),       # 上＝写真を構える人（私人か分からない・近い）と見物の人の列（c916）
    "PA1": (0.078, 0.0, 1.0, 0.90),      # 左の余白と下の余白（線は残す）
    "PA2": (0.0, 0.0, 1.0, 0.885),       # 下の余白＝隠した文の分
}


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
    if head != ["code", "type", "grp", "title", "get", "dims", "rights", "basis", "credit", "era", "people", "file", "note"]:
        raise SystemExit(f"🔴 sources30.psv の見出しの行が変わった：{rows[0][:120]}")
    out, prev = {}, None
    for ln in rows[1:]:
        f = ln.split("|")
        if len(f) != 13:
            raise SystemExit(f"🔴 sources30.psv の行の欄が13でない：{ln[:80]}")
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
    """git の外の表 {記号: 作者か提供者}。無ければ止める（束を作る手元だけで読む）"""
    for p in (PRIVATE, PRIVATE_QUOTE):
        if not p.exists():
            raise SystemExit(f"🔴 {p.relative_to(HERE).as_posix()} が無い（git の外の表）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    out = {r[0]: r[2] for r in rows if len(r) > 2}
    rows = [r for r in csv.reader(PRIVATE_QUOTE.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    out.update({r[0]: r[1] for r in rows[1:] if len(r) >= 2})
    return out


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
_NOT_NAMES = {"投稿者", "tokyo", "artist", "panoramio", "wikipedia", "self", "photo", "own work", "flickr", "commons", "wikimedia", "user", "unknown"}


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


def uses():
    """{記号: dict(main=[カット], ji=[カット], full=全面に当てるカットがあるか)}（束に入る写真と紙面）。一覧の種類と出どころの型が食い違えば止める。
    地（説明カットの地の写真）は CC BY・CC0・PD・PDL1.0 だけ（BY-SA は暗くするのも翻案・引用は地にしない）。イメージ（X で始まる記号＝⑤b-3 に足す・G で始まる地）は束の外"""
    src = _sources()
    out, bad = {}, []
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
                u = out.setdefault(c, dict(main=[], ji=[], full=False))
                u["main"].append(cid)
                u["full"] = u["full"] or r["frame"].startswith("全面")
        j = _code_of(r["ji"])
        if j and not j.startswith("X") and (src.get(j) or {}).get("type") not in STOCK_TYPES:
            s = src.get(j)
            if not s or s["type"] not in COMMONS_TYPES + NATION_TYPES:
                bad.append(f"{cid} {j}: 地の写真が Commons か国の写真でない（{s['type'] if s else '表に無い'}）")
            elif "BY-SA" in s["rights"]:
                bad.append(f"{cid} {j}: 地の写真が BY-SA（{s['rights']}）＝暗くするのも翻案")
            else:
                out.setdefault(j, dict(main=[], ji=[], full=False))["ji"].append(cid)
    if bad:
        raise SystemExit("🔴 " + "\n🔴 ".join(bad))
    return out


def is_private(code, s):
    return s["type"] in QUOTE_TYPES


def bundle_name(code, s):
    if is_private(code, s):
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
    """範囲だけを升目にする（縮めて NEAREST で戻す）＝16〜27本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def _src_path(s):
    """sources30 の file の欄の頭の道だけ＝ref/ep30 からの道"""
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


_YEAR = re.compile(r"((?:19|20)\d\d)(?!年代|\d)")    # 30本目の時期の欄は「1995-03-20」「1994」「2012-10-20」（表示に年が無い点は年を言わない）


def year_of(code, s):
    m = _YEAR.search(s["era"])
    if m:
        return int(m.group(1)), f"sources30.psv の時期の欄「{s['era'][:24]}」（映像方針＝資料館の表示・Commons の頁の撮影日・文書の日付）"
    return None, f"撮影の年の出どころが無い（時期の欄「{s['era']}」）"


def _mask_words(boxes):
    """升目の断りの語＝「顔」「ナンバー」「顔とナンバー」（札が「ナンバー：」で始まる箱＝ナンバー）"""
    plate = any(str(b[4]).startswith("ナンバー：") for b in boxes)
    face = any(not str(b[4]).startswith("ナンバー：") for b in boxes)
    return "顔とナンバー" if face and plate else "ナンバー" if plate else "顔"


def screen_credit(code, s, boxes, full):
    """画面の出典の行（了承②）＝sources30 の出典の欄＋**改変の断りを明記**：
    BY-SA＝「／改変なし」（額装・無加工）・CC BY の全面＝「／改変：切出」・CC BY の額装だけ＝「／改変なし」・CC0 と PD＝断りなし（切っても書かなくてよい・升目だけ書く）・
    国の写真＝「加工して作成」（PDL の編集の記載＝地のぼかしも切り出しも＝欄に無ければ足す）・公的な機関の紙面＝「／改変：切出」・第三者の引用＝断りなし（無加工の額）。升目は「・〇〇にモザイク」を足す"""
    cr = s["credit"]
    if "［" in cr or "（⑤b" in cr or "⑤b" in cr or cr.startswith("同上"):
        raise SystemExit(f"🔴 {code}: 出典の欄に書きかけの印が残る（{cr[:60]}）")
    what = f"{_mask_words(boxes)}にモザイク" if boxes else ""
    if boxes and (s["type"] not in COMMONS_TYPES + NATION_TYPES or "BY-SA" in s["rights"]):
        raise SystemExit(f"🔴 {code}: 升目は CC BY・CC0・PD・PDL1.0 の写真だけ（{s['rights']}＝BY-SA は升目も翻案・引用は加工しない）")
    if s["type"] in COMMONS_TYPES and "BY-SA" in s["rights"]:
        return cr + "／改変なし"
    if s["type"] in COMMONS_TYPES and "CC BY" in s["rights"]:
        mods = (["切出"] if full else []) + ([what] if what else [])
        return cr + ("／改変：" + "・".join(mods) if mods else "／改変なし")
    if s["type"] in NATION_TYPES:
        cr = cr if "加工して作成" in cr else cr + "・加工して作成"
        return cr + (f"（{what}）" if what else "")
    if s["type"] in PUBLIC_TYPES:
        return cr + f"／改変：切出{HIDDEN.get(code, '')}" if s["rights"] != "著作権の対象外" else cr
    return cr + (f"／改変：{what}" if what else "")


def who_table(code, s):
    """CREDITS.md の撮影者の欄（名前は書かない）"""
    t, r_ = s["type"], s["rights"]
    if t in COMMONS_TYPES and r_.startswith("CC BY"):
        return "Commons の撮影者（名前は git の外 `ref/ep30/src/credits_private.tsv` の記号の行＝画面は焼くときに足す）"
    if t in COMMONS_TYPES:
        return "表示は任意（CC0・PD）"
    if PERSON in s["credit"]:
        return "地元の個人（名前は git の外 `ref/ep30/src/credits_quote_private.tsv` の記号の行＝資料館の表示のとおり画面は焼くときに足す）"
    m = re.search(r"提供：([^）]+)）", s["credit"])
    if m:
        return m.group(1)
    return "各機関（国）"


def _lic(code, s):
    t = s["type"]
    if t in QUOTE_TYPES:
        return "引用（著作権法32条・東京消防庁と東京メトロの頁は引用を禁止の外に置く・個人は資料館の表示のまま＝ルール §2-39）"
    if t in NATION_TYPES:
        return "PDL1.0 の読み（公安調査庁のコピーライトポリシー＋法務省の「第三者＝国以外」＝ルール §2-39）"
    if t in PUBLIC_TYPES:
        return s["basis"]
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


# ── 束を作る ─────────────────────────────────────────────────
def cmd_build(nopages=False):
    """`nopages`＝紙面を撮る前に写真だけ見るとき（台帳は途中の形＝commit しない）"""
    from PIL import Image, ImageOps
    src, fet = _sources(), _fetched()
    db, bad = {}, 0
    us = uses()
    if nopages:
        us = {c: u for c, u in us.items() if src[c]["type"] not in PAGE_TYPES}
    for code in MASK:
        if code not in us:
            print(f"🔴 MASK の {code} は一覧で使っていない")
            bad += 1
    (EPD / "police").mkdir(exist_ok=True)
    log = None
    for code, u in sorted(us.items()):
        s = src[code]
        name = bundle_name(code, s)
        dst = EPD / f"{name}.jpg"
        t = s["type"]
        box_m = MASK.get(code, [])
        private = is_private(code, s)
        shot = None
        if t == "public-pdf":
            p, smd5 = _pdf_ok(code, fet)
            im, how = render_pdf(code, p)
            notes = [how, "🔴 公開リポに置かない（git add しない・Modal の保管庫）" if private else "公開リポに置く（規約を読んだ）"]
            im = ImageOps.expand(im, border=PAGE_PAD, fill=(255, 255, 255))
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        elif t == "public-page":
            log = log or _page_log()
            p, smd5, shot = _page_src(code, s, log)
            with Image.open(p) as im0:
                im = im0.convert("RGB")
            notes = [f"頁の切り口を撮った（{shot}）", "🔴 公開リポに置かない（git add しない・Modal の保管庫）" if private else "公開リポに置く（規約を読んだ）"]
            if code in PRE_CROP:
                f = PRE_CROP[code]
                im = im.crop((round(im.width * f[0]), round(im.height * f[1]), round(im.width * f[2]), round(im.height * f[3])))
            im = ImageOps.expand(im, border=PAGE_PAD, fill=(255, 255, 255))
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
            notes.append("fetch30.tsv の md5 と同じ（2回とも）")
            if box_m:
                im = mosaic(im, box_m, MOSAIC_PX)
                notes.append(f"{_mask_words(box_m)}の升目 {len(box_m)}か所（升 {MOSAIC_PX}px）")
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        y, ywhy = year_of(code, s)
        cr = screen_credit(code, s, box_m, u["full"] or bool(u["ji"]))   # 地に敷く点も画面いっぱいに切る
        frame = t in PAGE_TYPES or t in QUOTE_TYPES or "BY-SA" in s["rights"]
        url = s["get"].removeprefix("web:").removeprefix("pdf:").split("（")[0]
        if url.startswith("moj:museum/"):                    # 資料館の展示の番号（頁は1つ・絵の番号で引く）
            url = f"https://www.moj.go.jp/psia/aumarchive/museum/（資料館の番号 {url[len('moj:museum/'):]}）"
        url = ("https://" + url) if url and not url.startswith(("http", "commons:")) else url
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(u["main"]), ji=" ".join(u["ji"]), credit=cr, who=who_table(code, s),
                        note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=_lic(code, s), frame=frame, ground=s["basis"][:120], url=url,
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False, page=t in PAGE_TYPES, related=False,
                        quote_page=t in QUOTE_TYPES, named=AUTHOR in cr or PERSON in cr, mosaic=[list(b[:4]) for b in box_m] or None, name_mosaic=None,
                        masked_before=None, era=s["era"], people=s["people"], private=private, shot=shot)
        print(f"✓ {code:7} {name:14} {w}x{h:<5} 主 {' '.join(u['main']) or '—':14} 地 {' '.join(u['ji']) or '—':26} {_lic(code, s)[:12]}"
              f"{'  額装だけ' if frame else ''}{'  🔒非公開' if private else ''}  {'・'.join(notes)[:50]}")
    # 🆕 ⑤b-3：イメージの写真（Pexels・地だけの点も）＝取ったファイルそのまま `ref/ep30/stock/<名>.jpg`（🔴 git に入れない＝19本目 決め⑨）。
    #    Actions・Modal は `footage.stock_photos` が台帳の media から取り直して md5 を照らす（23本目の型）
    (EPD / "stock").mkdir(exist_ok=True)
    rows = _list()
    for code, s in sorted(src.items()):
        if s["type"] not in STOCK_TYPES or not s["file"].endswith(".jpg"):
            continue
        r = fet.get(code) or {}
        p = EPD / s["file"]
        if not p.exists() or not r or md5(p) != r["md5"] or r.get("出どころ") != s["get"]:
            print(f"🔴 {code}: 手元の写真が無いか、md5 か直リンクが取得のときと違う（{s['file']}）＝fetch30e.py stock で取る")
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
    print(f"→ ref/ep30/assets.json（{len(db)}点＝公開リポに入る {len(pub)}・🔒非公開 {sum(r['private'] for r in db.values())}"
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
        m = PE.margins(f"ep30/{n}.jpg")
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
    作者と提供者の名乗り（scene_jiko._ep30_person）を当てて出典の行の字幅を測る（名前は出さない＝字数だけ）"""
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
        for mark in (AUTHOR, PERSON):
            if mark in line:
                try:
                    line = line.replace(mark, SJ._ep30_person(f"ep30/{n}.jpg", mark))
                except Exception as e:                     # noqa: BLE001  焼く前に止める
                    print(f"🔴 {n}: 名乗りが作れない（{e}）")
                    bad += 1
        wd = _width(line)
        if wd > CREDIT_W_MAX:
            print(f"🔴 {n}: 出典の行の字幅 {wd:.1f}（{CREDIT_W_MAX} まで＝画面の左下からはみ出すおそれ）")
            bad += 1
        cj[f"ep30/{n}.jpg"] = r["credit"]
        kind = "引用・非公開" if r["private"] else ("公的な機関の頁" if r["page"] else "この回の土地と物")
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
        "※2026-11-05（⑤b-2）。`qa_out/ep30_assets.py credits --write` が書く（手で直さない）。写真と紙面は映像方針の一覧 `ref/ep30/eizou_list30.md`（了承② 2026-11-05）。",
        "🔴 事件の回（ルール §B2-11・§B2-12）＝被害者・遺族・第一通報者・手記の筆者・刑を終えた人の名前は書かない。教団の宣伝物・報道の写真と映像・被害者が写る絵は使わない。この回の線の細部は台本にも画面にも書かない。",
        "",
        "### 0. 資料館の写真の読み（公安調査庁 オウム真理教問題デジタルアーカイブ・ルール §2-39）",
        "- 提供が国の機関（陸上自衛隊）・提供の表示なし＝公安調査庁のコピーライトポリシーの PDL1.0 の読み（法務省の頁と PDL1.0 は第三者＝国以外の者）＝全面の切り出し可・出典の行に「加工して作成」・公開リポに置く",
        "- 提供が東京都の機関・会社・個人＝第三者＝引用の形（著作権法32条・無加工の額・出典・語りが主・話している秒だけ・本編だけ・サムネに使わない）。東京消防庁と東京メトロの頁は引用を禁止の外に置く。"
        "🔴 **公開リポに置かない**（`ep30/police/`＝git の外・Modal の保管庫）。⚠️ 法律の助言ではない＝こちらの読み",
        "- 公的な機関の紙面＝各頁の規約を読んで切り出す（名前の行とこの回の線の行を切り口に入れない）・出典の行に URL と「／改変：切出」・ロゴは写さない・判決は著作権の対象外（著作権法13条の読み）",
        "",
        "### 1. 写真と紙面（国の写真・第三者の引用・Commons の CC BY・BY-SA・CC0・PD・公的な機関の頁）",
        "- CC BY・BY-SA＝「写真：{作者}／Wikimedia Commons（ライセンス）」。🔴 撮影者と個人の提供者の名前はこのリポに書かない＝`ref/ep30/credits.json` は印 `{作者}`・`{個人}` だけ・"
        "焼くときに git の外の表 `ref/ep30/src/credits_private.tsv`・`credits_quote_private.tsv` から足す（`tools/scene_jiko.ep30_credit`）",
        "- BY-SA＝額装（無加工・1点1カット・升目もかけない＝人とナンバーが写っていない点だけ）。CC BY・CC0・PD の私人の顔とナンバーは升目（「／改変：…にモザイク」）。公的な任務の顔はそのまま。色は原本のまま",
        "- 説明カットの地（「地 c…」）＝CC BY・CC0・PD・PDL1.0 の写真を暗くするだけ（字と地の比 8:1 が下限・出典の行は「地の写真：…／改変：切出・明るさ」・PDL1.0 は「加工して作成」）",
        "- 撮影年＝資料館の表示・Commons の頁の撮影日・文書の日付（sources30 の時期の欄）。表示に年の無い点は「不明」＝副題に年を書かない",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. 動く映像＝clips.json（防衛省の記録・イメージの Pexels）",
        "- 防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0＝公式の YouTube の表示と Commons の札）＝章「地下鉄サリン事件」の昼の区間だけ・上下を切って全面・音は使わない。夜の群衆と夜の消防は使わない",
        "- フリー素材（Pexels・AI で作った絵は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」だけ（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。"
        "20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）",
        "- イメージの写真（Pexels・地だけの点も）＝表 1 の `x…`・`g…`（`ep30/stock/`）。🔴 git に入れない＝焼くときに台帳の直リンクから取り直して md5 を照らす（`footage.stock_photos`・23本目の型）",
        "",
        "### 3. 地図の描き足し（⑤b-3）",
        "- 衛星写真＝Google マップ（帰属は地図の右下・PNG は公開リポに置かない＝保管庫）。路線の線と県の境＝「国土数値情報（鉄道データ・行政区域データ）」（国土交通省 https://nlftp.mlit.go.jp/ksj/）をもとに作成"
        "（データの頁の許諾＝オープンデータ CC BY 4.0・サイトの規約 PDL1.0・2026-11-05 に読んだ）。札の場所＝同じ鉄道データの駅・国土地理院の住所検索（`cuts/ss.GEO`）",
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


# ── 動く映像＝台帳 clips.json・ショット shots.json・見取り図・USE・ひかえ（防衛省の記録 M6＝⑤b-2・イメージ〈Pexels〉＝⑤b-3・26本目の型）──────────
# 🆕 防衛省の記録＝Commons の変換版 1080p の全体（17本目の V1 と同じファイル）。手元の src/footage/M6.webm は区間の写し（手元の秒＝素材の秒−M6_OFF）
M6_PAGE = "https://commons.wikimedia.org/wiki/File:%E5%B9%B3%E6%88%90%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm"
M6_MEDIA = ("https://upload.wikimedia.org/wikipedia/commons/transcoded/9/9d/%E5%B9%B3%E6%88%90%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm/"
            "%E5%B9%B3%E6%88%90%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm.1080p.vp9.webm")
M6_OFF = 1034.6
M6_SIZE = 561682293                    # 変換版の大きさ（17本目の台帳と同じ＝HEAD で照らす）
# 場面の切れ目（素材の秒・⑤b-1 に灰色の差で測った＝引き継ぎ §3-5）。この外は夜の群衆と夜の消防＝表に入れない（USE に書けば止まる）
M6_EDGES = (1042.4, 1049.6, 1051.2, 1056.7, 1062.7, 1073.5, 1076.46, 1079.2, 1086.8, 1091.6, 1096.8, 1103.7)


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
    """clips.json＝防衛省の記録 M6 とイメージ（Pexels）。手元の映像の md5 を取得の記録（fetch30.tsv）と照らし、記録の直リンクを HEAD で引いて大きさを見る"""
    src, fet = _sources(), _fetched()
    out = {}
    for code, cuts in _film_codes().items():
        s = src[code]
        p = EPD / s["file"]
        r = fet.get(code) or {}
        rec = r.get("出どころ") or ""
        if s["type"] == "commons-video":
            if not p.exists() or not r or md5(p) != r["md5"]:
                raise SystemExit(f"🔴 {code}: 手元の映像が無いか、md5 が取得のときと違う（{s['file']}）")
            st, n, ct = _head(M6_MEDIA)
            if st != 200 or n != M6_SIZE or not ct.startswith("video/"):
                raise SystemExit(f"🔴 {code}: 変換版の直リンクが台帳と違う（http {st}・{n} B／台帳 {M6_SIZE} B・{ct}）")
            loc = _probe(p)
            out[code] = dict(url=M6_PAGE, media=M6_MEDIA, credit=s["credit"], src="mod", at=0.0, date="1995-03-20", stock=False,
                             what="平成6年防衛庁記録（章「地下鉄サリン事件」の昼の区間 17:23〜18:23）", got=r["取った日"], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"],
                             sec=1254.286, size=M6_SIZE, dispw=loc["w"], decoded=[loc["w"], loc["h"]], license="CC BY 3.0",
                             rights="CC BY 3.0（防衛省・自衛隊の YouTube 公式・Commons の同じ版）", scan=f"ref/ep30/{s['file']}", md5_scan=r["md5"],
                             local_off=M6_OFF, note="音は使わない。手元の写しの秒＝素材の秒−local_off（⑤b-1 に Commons の本物と 0.04秒以内で一致を2か所で確かめた）")
            print(f"  {code:5} {loc['w']}x{loc['h']} {loc['fps']}fps 手元 {loc['sec']:.2f}秒 {' '.join(cuts)}  HEAD {st}（{n} B）")
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
        out[code] = dict(url=_stock_page(code, s), media=media, stock=True, file=f"ep30/{s['file']}", credit="イメージ（Pexels）", src="stock",
                         at=0.0, what=s["title"][:60], got=r["取った日"], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(loc["sec"], 3),
                         size=size, md5=r["md5"], dispw=loc["w"], decoded=[loc["w"], loc["h"]], license="Pexels License",
                         license_url="https://www.pexels.com/license/", site="Pexels")
        print(f"  {code:5} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.2f}秒 {size / 1e6:.1f}MB  {' '.join(cuts)}  HEAD {st}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep30/clips.json（{len(out)}本）")
    return 0


# フリー素材で、動きの速い素材の隣の1秒の差がしきい値を超えて出た「境目」を、根拠つきで1ショットに直す（25・26本目 SHOT_ONE の型）
#   根拠＝境目の前後の全コマの隣の差に、1コマに集まる跳ねが無い（切り替わりなら1コマに集まる）。⚠️ 記号は素材を替えても同じ＝替えたら測り直す
#   ⑤b-3（11-02）に 10コマ/秒の隣の差を測った（scratchpad clip_probe.py）・コマを並べて同じカメラの1回の撮影と見た（動きの速い手・足で 1秒の差が超えた）
#   30本目 ⑤b-3（11-05）＝同じ物差し（隣の差の最大÷中央値 X703 1.6・X710 1.3・Xc17 3.0＝前後のコマも高い）。頭・真ん中・尻を 640px で見て同じカメラの1回の撮影
SHOT_ONE = {"X703": "手持ちで通路を歩く1回の撮影", "X710": "前面の1回の撮影（速い）", "Xc17": "据えたカメラの長時間露光（人の流れの量で差が動く）"}


def cmd_shots():
    """shots.json＝防衛省の記録は M6_EDGES（灰色の差で測った）・イメージは tools/shots.shots_of（1秒1コマ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import shots as SH
    src = _sources()
    out = {}
    for code in _film_codes():
        s = src[code]
        p = EPD / s["file"]
        if s["type"] == "commons-video":
            sh = [dict(start=a, until=b, motion=0.0) for a, b in zip(M6_EDGES, M6_EDGES[1:])]
            out[code] = dict(src=M6_MEDIA, scan=f"ref/ep30/{s['file']}", dur=1254.286,
                             how="⑤b-1（11-05）：手元の写し（25コマ/秒・64×36 の灰色）の隣のコマの差の山を素材の秒に直し、3か所を25コマ/秒で詰めた・Commons の本物と 0.04秒以内で一致（2か所）。この外は夜の場面＝表に入れない＝USE に書けば止まる",
                             shots=sh)
            print(f"  {code:5} ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
            continue
        if not p.exists():
            print(f"  ⚠️ {code}: 手元に無い")
            continue
        sh, dur = SH.shots_of(p)
        how = "1秒1コマで tools/shots.shots_of（30本目・フリー素材）"
        if code in SHOT_ONE:
            sh = [dict(start=0.0, until=float(sh[-1]["until"]), motion=max(x["motion"] for x in sh))]
            how += f"・🔧 1ショットに直した（{SHOT_ONE[code]}）"
        out[code] = dict(src=_stock_page(code, s), scan=f"ref/ep30/{s['file']}", dur=round(dur, 1), how=how, shots=sh)
        print(f"  {code:5} {dur:6.1f}秒  ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep30/shots.json（{len(out)}本）")
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
STOCK_GEOM = {"c204": dict(zoom=1.06, xbias=0.0)}   # c204＝ホームの右端の人を画面の外へ（⑤b-3 に 640px で見た）
# 🆕 防衛省の記録の6カット（4:3 を横いっぱいに＝footage.PILLAR）。`edit=True`＝元の映像の編集のまま場面をまたぐ（footage.outside_shot の注）。
#    窓＝既定の真ん中（⑤b-2 に場面ごとのコマに窓の線を引いて見た＝駅の札・焼き込みの字幕・足元が窓の内側）。c107 だけ上へ（1073.5〜 の防護マスクの寄りの顔が切れる）
M6_GEOM = {"c107": dict(bias=0.3)}
# 🔴 タンクの手書きの字（全面だと数字に百分率の記号が付いたように読める）＝この回の線と混同されないよう写さない。⑤b-2 に焼いた絵で見て決めた（1059.3 から薄く読める・1062.7 で場面が替わる）
M6_NOGO = (1059.1, 1062.75, "タンクの手書きの字が読める")


def cmd_use(only=None, all_=False):
    """footage.USE の30本目の欄。区間と速さは一覧 list30.tsv の動きの欄「映像 a〜b秒（＋止め n秒）（r倍速）」から読む（make_list30 の門番 gate_video と同じ物差し）。
    イメージは区間を1つのショットに収める。🔴 章ファイルに `ss.vid` を書いたカットだけ（`only` は書く前の鶏と卵を割るため）"""
    sys.path.insert(0, str(HERE / "tools"))
    sys.path.insert(0, str(BUILD))
    import make_list30 as ML
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
        if hold:
            raise SystemExit(f"🔴 {cid}: 映像に止めを書かない（{r['motion']}）")
        need = float(r["cont"])
        if rate < STILL_BELOW:
            raise SystemExit(f"🔴 {cid}: 倍速 {rate}＜{STILL_BELOW}（止め絵になる）")
        if code == "M6":
            geo = "".join(f", {k}={v}" for k, v in M6_GEOM.get(cid, {}).items())
            cross = [e for e in M6_EDGES if a < e < b]
            lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate={rate}{geo}{", edit=True" if cross else ""}),   '
                         f'# 使う {b - a:.2f}秒／要る {need:.2f}秒・元の編集の切れ目 {" ".join(f"{e:g}" for e in cross) or "なし"}')
            continue
        hit = [x for x in sd[code]["shots"] if x["start"] <= a < x["until"]]
        if len(hit) != 1 or b > hit[0]["until"] + 1e-6:
            raise SystemExit(f"🔴 {cid}: 区間 {a}〜{b} が1つのショットに収まらない（{[(x['start'], x['until']) for x in hit]}）")
        sh = hit[0]
        geo = "".join(f", {k}={v}" for k, v in STOCK_GEOM.get(cid, {}).items())
        lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate={rate}{geo}),   '
                     f'# ショット {sh["start"]:g}〜{sh["until"]:g}秒・使う {b - a:.2f}秒／要る {need:.2f}秒')
    _write_block("EP30_USE", lines)
    _write_block("EP30_NOGO", [f'    "M6": [{M6_NOGO!r}],'])
    print(f"→ tools/footage.py USE {len(lines)}欄・NOGO 1欄")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）。イメージ＝区間の頭のコマを 1920×1080 に（寄せは USE と同じ式）＝`ref/ep30/stock/fb_<cid>.jpg`（🔴 git に入れない＝決め⑨）。
    防衛省の記録＝区間の頭のコマを器のまま（黒帯ごと）＝`ref/ep30/fb_<cid>.jpg`（CC BY 3.0・`ss.vid` が映像と同じ寄せを渡す＝17本目の型・公開リポに置く）"""
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
            Image.open(io.BytesIO(raw)).convert("RGB").save(dst, quality=92)
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
