# -*- coding: utf-8 -*-
"""ep28_assets.py — 28本目（タイムズカー情報漏えい）の写真と紙面の束・出典（⑤b-2・2026-11-01）。27本目 `ep27_assets.py` の形を、
28本目の台帳（`sources28.psv` の13列〈見出しの行で読む〉・`fetch28.tsv`・`fetch28_company.tsv`〈md5 を2回〉・頁の撮影の記録 `src/pages/log.tsv`・
git の外の作者の表 `src/credits_private.tsv`〈列 code・作者〉）に合わせた。県警の動画の道は無い。イメージ（Pexels の映像）は ⑤b-3（clips.json）＝束に入れない。

  python -P qa_out/ep28_assets.py build             # 束 ref/ep28/<名>.jpg（会社の引用と規約の無い頁＝ref/ep28/police/）＋ 権利の台帳 ref/ep28/assets.json
  python -P qa_out/ep28_assets.py pdflines D0928 …  # PDF の字の層の行（頁・y）を src/pages/<記号>_pdflines.txt へ（切り口 PDF_CROP を選ぶ）
  python -P qa_out/ep28_assets.py look CM045 …      # 束の写真を並べた見本（out/ep28_look/・1枚 960 幅）
  python -P qa_out/ep28_assets.py crop CM045 x0 y0 x1 y1 [倍]   # 束の画素の切り出し（既定2倍・10px の目盛り）＝人とナンバーを決めるとき
  python -P qa_out/ep28_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python -P qa_out/ep28_assets.py edges             # 束の四辺の暗い帯＝門番 check_photo_edge の名簿（SLIDE_MOUNT／SLIDE_NOT_MOUNT）を決める
  python -P qa_out/ep28_assets.py credits [--write] # 画面の出典 ref/ep28/credits.json と ref/CREDITS.md の28本目の節

🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色）＝幅 2400 か高さ 1350 の大きい方まで（小さい写真は原画のまま）。
🔴 会社の頁・適時開示（引用）＝**公開リポに置かない**（会社の規約が「私的利用だけ」＝置くと再配布に見える・ルール §2-34）＝`ref/ep28/police/`（`git add` しない）・
   台帳の `private`。焼くのは Modal（保管庫 jiko-assets の同じ道＝`modal_app.pull_private`）。⚠️ Actions は保管庫を読めない。⚠️ 法律の助言ではない＝こちらの読み。
🔴 公的な機関の頁（⑤b-2 に規約を読んだ 2026-11-01）＝金融庁・個人情報保護委員会・首相官邸・国家サイバー統括室・e-Gov は公共データ利用規約 PDL1.0・福岡県警は
   政府標準利用規約（CC BY 4.0 互換）＝出典と編集の断りを書けば使える＝公開リポに置く。**三重県警は規約の頁が見つからない＝引用の型＝`police/`**。
   切り出すので出典の行に「／改変：切出」（PDL の「編集・加工等を行ったことの記載」）。ロゴは写さない（PDL の適用外）。
🔴 事件の回（ルール §B2-11）＝会員・SNS の投稿者・役員・弁護士の名前と、Commons の撮影者名を台帳・出典の行・CREDITS.md に書かない＝作者は印 `{作者}` だけ
   （焼くときに `scene_jiko._ep28_author` が git の外の表から足す）。適時開示の頁の頭（代表者名・問合せ先）は切り口の外（PDF_CROP の outside が止める）。
🔴 人とナンバー（了承② 決め4）＝CC BY・CC0・PD は私人の顔とナンバーだけ升目（MASK）・**BY-SA は升目も翻案＝かけない**（写っていない点だけ使う）。
"""
import csv
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep28"
SRC = EPD / "src"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list28.tsv"
SOURCES = BUILD / "sources28.psv"
FETCHES = (BUILD / "fetch28.tsv", BUILD / "fetch28_company.tsv")
PAGE_LOG = SRC / "pages" / "log.tsv"          # 頁の撮影の記録（git の外・撮った日時・URL・md5）
PRIVATE = SRC / "credits_private.tsv"         # 🔴 git の外（作者欄）＝ここから名前を公開の物へ写さない
NAME_FILES = (SRC / "names_private.txt", SRC / "names_commons.txt")   # 🔴 git の外（出さない名前）
DB = EPD / "assets.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
SCRATCH = HERE / "out" / "ep28_look"          # look・crop の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## タイムズカー情報漏えい（2026-09-25・28本目）"
AUTHOR = "{作者}"            # CC BY・BY-SA の出典の行の印（焼くときに git の外の表から足す＝scene_jiko.ep28_credit）
EVENT_YEAR = 2026            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 92
MOSAIC_PX = 14                         # 升目の大きさ（束の画素）
PHOTO_TYPES = ("commons-photo",)
COMPANY_TYPES = ("company-page", "company-pdf")      # 引用・公開リポに置かない
PUBLIC_TYPES = ("public-page", "public-pdf")         # 公的な機関（規約を読んだ＝公開リポに置く・三重県警だけ PRIVATE_PUBLIC）
PAGE_TYPES = COMPANY_TYPES + PUBLIC_TYPES
STOCK_TYPES = ("stock",)                             # 束に入れない（⑤b-3 の clips.json）
KIND_OK = {"実写": PHOTO_TYPES, "引用": COMPANY_TYPES, "公的": PUBLIC_TYPES, "イメージ": STOCK_TYPES}
PRIVATE_PUBLIC = {"MIE"}                             # 公的な機関でも規約の頁が見つからない＝引用の型＝公開リポに置かない

# PDF の切り口 {記号: dict(page, head, tail, outside)}＝字の層の行で決める（head の行〜tail の行の外接＋余白）。outside＝切り口に入ってはいけない行の字（代表者名ほか）
#   rect があれば字の層でなく pt の箱で切る（縦書きの e-Gov の本文）
PDF_DPI_K = 3.0                        # 描く倍率（1pt＝3画素）
PDF_FILES = {"D0928": "company/D0928.pdf", "D1023a": "company/D1023a.pdf", "D1023b": "company/D1023b.pdf", "PPC": "public/ppc_261007_houdou.pdf",
             "EGOV": "public/egov_pcm_0000294591_kekka.pdf", "NISC": "public/nco_taiou_20261009.pdf"}
PDF_LOG_MD5 = {"PPC": "78d228eaf9d4c66327b1ff7dc85df999", "EGOV": "d9beae25bb4cad1a8f9d152dfeeacb31", "NISC": "f6110a560ab559a6e6d4576f197f6b08"}   # sources28 と src/public/fetch_log.tsv
PDF_CROP = {
    "D0928": dict(page=1, head="連結子会社における不正アクセス", tail="認しております", outside=["代表者名", "問合せ先"]),      # c205 題と経緯
    "D1023a": dict(page=4, head="C) お見舞金のお支払い", tail="なるお客様へご案内いたします", outside=[]),                        # c601 見舞金の段
    "D1023b": dict(page=1, head="１． 特別損失の計上", tail="93.28", outside=["代表者名", "問合せ先"]),                            # c606 特別損失と修正の表
    "PPC": dict(page=3, head="３ 不要となった個人データの消去", tail="の法令等の根拠とともに", outside=[]),                       # c411
    "NISC": dict(page=1, head="不正アクセスによる漏えい等の事案", tail="一層の対策の徹底を", outside=[]),                          # c515
    "EGOV": dict(page=1, head="令和７年６月", tail="の考え方を次のとおり公表いたします", outside=[]),                              # c505 結果の1頁目（文書の日付は「令和７年６月」）
}

# 升目 {記号: [(x0, y0, x1, y1, 札)]}（束の画素）。札が「ナンバー：」で始まる箱＝ナンバー・それ以外＝顔（出典の行の断りを分ける）。⑤b-2 に原寸で見て決めた
#   ✕ 升目にしない（原寸で見た）：CM007（ナンバーは札で隠れる）・CM029（札の裏で見えない）・CM041（札で隠れる・白い端だけ）・CM023（車の下は画面の外）・CM030（ワゴンは横腹）・
#      CM065 の奥の人たち（顔 約8px）と後ろ姿の黒い服の人・遠い車
MASK = {
    "CM001": [(1232, 788, 1295, 864, "ナンバー：デミオ（カラーコーンから出た半分）")],
    "CM006": [(1155, 885, 1278, 1025, "ナンバー：手前の青い車"), (568, 766, 618, 858, "ナンバー：赤いミニ"), (424, 692, 468, 762, "ナンバー：銀の車"),
              (172, 622, 200, 676, "ナンバー：奥の白い車")],
    "CM034": [(360, 842, 442, 890, "ナンバー：左の銀の車"), (1015, 1030, 1205, 1080, "ナンバー：札の下の車")],
    "CM036": [(0, 1328, 74, 1426, "ナンバー：左の白い車"), (1708, 1394, 1884, 1442, "ナンバー：右の軽自動車")],
    "CM039": [(508, 918, 532, 938, "ナンバー：手前の白い車"), (606, 910, 626, 928, "ナンバー：銀のワゴン"), (813, 892, 834, 907, "ナンバー：奥の白い車"),
              (856, 892, 874, 907, "ナンバー：奥の黒い車"), (898, 892, 914, 907, "ナンバー：奥の赤い車"), (941, 900, 958, 915, "ナンバー：奥の紺の車")],
    "CM045": [(452, 1350, 564, 1420, "ナンバー：左の軽自動車"), (1240, 1268, 1330, 1350, "ナンバー：右の銀の車")],
    "CM046": [(278, 788, 322, 816, "ナンバー：白い車"), (482, 750, 516, 772, "ナンバー：灰色のワゴン"), (680, 776, 710, 797, "ナンバー：黒いワゴン")],
    "CM047": [(934, 800, 964, 820, "ナンバー：白い軽自動車")],
    "CM049": [(267, 830, 320, 862, "ナンバー：白い軽ワゴン"), (578, 800, 612, 826, "ナンバー：銀のワゴン")],
    "CM054": [(155, 698, 200, 723, "ナンバー：左の銀の車"), (880, 697, 920, 728, "ナンバー：赤いプリウス")],
    "CM057": [(300, 887, 362, 930, "ナンバー：白い軽自動車"), (1128, 783, 1152, 809, "ナンバー：銀のワゴン"), (956, 814, 982, 842, "ナンバー：銀の小さい車")],
    "CM065": [(1700, 1168, 1764, 1228, "自転車の人"), (1362, 1142, 1396, 1178, "黒いコートの人"), (1438, 1130, 1472, 1170, "薄い色のコートの人"),
              (1736, 1150, 1762, 1170, "ナンバー：白い軽ワゴン"), (1542, 1096, 1564, 1111, "ナンバー：黒い車")],
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
        raise SystemExit(f"🔴 sources28.psv の見出しの行が変わった：{rows[0][:120]}")
    out = {}
    for ln in rows[1:]:
        f = ln.split("|")
        if len(f) != 13:
            raise SystemExit(f"🔴 sources28.psv の行の欄が13でない：{ln[:80]}")
        out[f[0]] = dict(zip(head, f))
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


# 目録の作者の欄に入っていた機関名と一般の語＝名前でない（`eizou_build/authors28.SKIP` と同じ扱い＝映像方針の落とし穴）
_NOT_NAMES = {"国土交通省", "投稿者", "警察庁", "park24", "tokyo", "artist", "times", "panoramio", "kyoto", "yokohama", "mazda", "wikipedia", "self", "photo",
              "own work", "flickr", "commons", "wikimedia", "user", "unknown"}


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
    地（説明カットの地の写真）は CC BY・CC0・PD だけ（BY-SA は暗くするのも翻案）"""
    src = _sources()
    out, bad = {}, []
    for r in _list():
        cid = r["cid"]
        c = _code_of(r["main"])
        if c:
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
        if j:
            s = src.get(j)
            if not s or s["type"] not in PHOTO_TYPES:
                bad.append(f"{cid} {j}: 地の写真が Commons の写真でない（{s['type'] if s else '表に無い'}）")
            elif "BY-SA" in s["rights"]:
                bad.append(f"{cid} {j}: 地の写真が BY-SA（{s['rights']}）＝暗くするのも翻案")
            else:
                out.setdefault(j, dict(main=[], ji=[], full=False))["ji"].append(cid)
    if bad:
        raise SystemExit("🔴 " + "\n🔴 ".join(bad))
    return out


def is_private(code, s):
    return s["type"] in COMPANY_TYPES or code in PRIVATE_PUBLIC


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
    """sources28 の file の欄の頭の道だけ＝ref/ep28 からの道"""
    m = re.match(r"(src/[^（\s|]+?\.(?:jpe?g|png|pdf))", s["file"])
    return EPD / m.group(1) if m else None


def _src_ok(code, s, fet):
    """手元の元のファイルが取得の記録（md5 を2回＝同じ）と同じか。違えば止める"""
    p = _src_path(s)
    if not p or not p.exists():
        raise SystemExit(f"🔴 {code}: 手元のファイルが無い（{s['file']}）")
    r = fet.get(code)
    if not r:
        raise SystemExit(f"🔴 {code}: 取得の記録が無い（fetch28.tsv の final）")
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
    """PDF の切り口を描く＝(RGB の絵, 記録の言葉)。outside の行が切り口に入れば止める"""
    import fitz
    from PIL import Image
    sp = PDF_CROP[code]
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
    for anc in sp.get("outside", []):
        hit = [b for t, b in lines if anc in t]
        if not hit:
            raise SystemExit(f"🔴 {code}: 目印の行「{anc}」が字の層に無い（外に出したことを測れない）")
        if any(b[1] < box[3] and b[3] > box[1] for b in hit):
            raise SystemExit(f"🔴 {code}: 切り口の外にあるべき行「{anc}」が束の絵に入る")
    pix = pg.get_pixmap(matrix=fitz.Matrix(PDF_DPI_K, PDF_DPI_K), clip=fitz.Rect(*box), alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return im, f"PDF の {sp['page']}頁の切り口（y {box[1]:.0f}〜{box[3]:.0f}pt）を描いた（1pt＝{PDF_DPI_K:g}画素）"


_YEAR = re.compile(r"((?:19|20)\d\d)年")


def year_of(code, s):
    m = _YEAR.search(s["era"])
    if m:
        return int(m.group(1)), f"sources28.psv の時期の欄「{s['era'][:24]}」（映像方針＝Commons の頁の撮影日・会社と機関の文書の日付）"
    return None, f"撮影の年の出どころが無い（時期の欄「{s['era']}」）"


def _mask_words(boxes):
    """升目の断りの語＝「顔」「ナンバー」「顔とナンバー」（札が「ナンバー：」で始まる箱＝ナンバー）"""
    plate = any(str(b[4]).startswith("ナンバー：") for b in boxes)
    face = any(not str(b[4]).startswith("ナンバー：") for b in boxes)
    return "顔とナンバー" if face and plate else "ナンバー" if plate else "顔"


def screen_credit(code, s, boxes, full):
    """画面の出典の行（了承② 決め4）＝sources28 の出典の欄＋**改変の断りを明記**：
    BY-SA＝「／改変なし」（額装・無加工）・CC BY の全面＝「／改変：切出」・CC BY の額装だけ＝「／改変なし」・CC0 と PD＝断りなし（切っても書かなくてよい・升目だけ書く）・
    公的な機関（公開リポ）＝「／改変：切出」（PDL の編集の記載）・会社の引用と三重県警＝断りなし（引用＝元のまま・切り口は範囲の選び方）。升目は「・〇〇にモザイク」を足す"""
    cr = s["credit"]
    if "［" in cr or "（⑤b" in cr or "⑤b" in cr:
        raise SystemExit(f"🔴 {code}: 出典の欄に書きかけの印が残る（{cr[:60]}）")
    what = f"{_mask_words(boxes)}にモザイク" if boxes else ""
    if boxes and (s["type"] not in PHOTO_TYPES or "BY-SA" in s["rights"]):
        raise SystemExit(f"🔴 {code}: 升目は CC BY・CC0・PD の写真だけ（{s['rights']}＝BY-SA は升目も翻案）")
    if s["type"] in PHOTO_TYPES and "BY-SA" in s["rights"]:
        return cr + "／改変なし"
    if s["type"] in PHOTO_TYPES and "CC BY" in s["rights"]:
        mods = (["切出"] if full else []) + ([what] if what else [])
        return cr + ("／改変：" + "・".join(mods) if mods else "／改変なし")
    if s["type"] in PUBLIC_TYPES and code not in PRIVATE_PUBLIC:
        return cr + "／改変：切出"
    return cr + (f"／改変：{what}" if what else "")


def who_table(code, s):
    """CREDITS.md の撮影者の欄（名前は書かない）"""
    t, r_ = s["type"], s["rights"]
    if t in PHOTO_TYPES and r_.startswith("CC BY"):
        return "Commons の撮影者（名前は git の外 `ref/ep28/src/credits_private.tsv` の記号の行＝画面は焼くときに足す）"
    if t in PHOTO_TYPES:
        return "表示は任意（CC0・PD）"
    if t == "company-page":
        return "タイムズモビリティ"
    if t == "company-pdf":
        return "パーク24"
    return "各機関（国・県）"


def _lic(code, s):
    t = s["type"]
    if t in COMPANY_TYPES:
        return "引用（著作権法32条・会社の規約は私的利用だけ・引用に触れない）"
    if code in PRIVATE_PUBLIC:
        return "引用（著作権法32条・頁に規約が見つからない）"
    if t in PUBLIC_TYPES:
        return "PDL1.0 か政府標準利用規約（2026-11-01 に各頁で読んだ）＝出典と編集の断り"
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
def cmd_build():
    from PIL import Image
    src, fet = _sources(), _fetched()
    db, bad = {}, 0
    us = uses()
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
        if t in ("company-pdf", "public-pdf"):
            p, smd5 = _pdf_ok(code, fet)
            im, how = render_pdf(code, p)
            notes = [how, "🔴 公開リポに置かない（git add しない・Modal の保管庫）" if private else "公開リポに置く（規約を読んだ）"]
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        elif t in ("company-page", "public-page"):
            log = log or _page_log()
            p, smd5, shot = _page_src(code, s, log)
            with Image.open(p) as im0:
                im = im0.convert("RGB")
            notes = [f"頁の切り口を撮った（{shot}）", "🔴 公開リポに置かない（git add しない・Modal の保管庫）" if private else "公開リポに置く（規約を読んだ）"]
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        else:
            p, smd5 = _src_ok(code, s, fet)
            im, notes = load_photo(p)
            im, k = _shrink(im)
            if k < 1.0:
                notes.append(f"縮小 ×{k:.3f}")
            notes.append("fetch28.tsv の md5 と同じ（2回とも）")
            if box_m:
                im = mosaic(im, box_m, MOSAIC_PX)
                notes.append(f"{_mask_words(box_m)}の升目 {len(box_m)}か所（升 {MOSAIC_PX}px）")
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
        y, ywhy = year_of(code, s)
        cr = screen_credit(code, s, box_m, u["full"])
        frame = t in PAGE_TYPES or "BY-SA" in s["rights"]
        url = s["get"].removeprefix("web:").split("（")[0]
        url = ("https://" + url) if url and not url.startswith(("http", "commons:", "tdnet:")) else url
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(u["main"]), ji=" ".join(u["ji"]), credit=cr, who=who_table(code, s),
                        note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=_lic(code, s), frame=frame, ground=s["basis"][:120], url=url,
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False, page=t in PAGE_TYPES, related=False,
                        quote_page=t in COMPANY_TYPES or code in PRIVATE_PUBLIC, named=AUTHOR in cr, mosaic=[list(b[:4]) for b in box_m] or None, name_mosaic=None,
                        masked_before=None, era=s["era"], people=s["people"], private=private, shot=shot)
        print(f"✓ {code:7} {name:14} {w}x{h:<5} 主 {' '.join(u['main']) or '—':14} 地 {' '.join(u['ji']) or '—':26} {_lic(code, s)[:12]}"
              f"{'  額装だけ' if frame else ''}{'  🔒非公開' if private else ''}  {'・'.join(notes)[:50]}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    pub = [n for n, r in db.items() if not r["private"]]
    print(f"→ ref/ep28/assets.json（{len(db)}点＝公開リポに入る {len(pub)}・🔒非公開 {sum(r['private'] for r in db.values())}"
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
        print(f"→ {out.relative_to(HERE).as_posix()}（{len(d)}頁）")
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
    """束の画素の切り出し（k 倍・束の画素で 10px ごとの目盛り＝升目の範囲を読むため）＝out/ep28_look/crop_<名>_<x0>_<y0>.jpg"""
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
        m = PE.margins(f"ep28/{n}.jpg")
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
    作者の名乗り（scene_jiko._ep28_author）を当てて出典の行の字幅を測る（名前は出さない＝字数だけ）"""
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
        if AUTHOR in line:
            try:
                line = line.replace(AUTHOR, SJ._ep28_author(f"ep28/{n}.jpg"))
            except Exception as e:                         # noqa: BLE001  焼く前に止める
                print(f"🔴 {n}: 作者の名乗りが作れない（{e}）")
                bad += 1
        wd = _width(line)
        if wd > CREDIT_W_MAX:
            print(f"🔴 {n}: 出典の行の字幅 {wd:.1f}（{CREDIT_W_MAX} まで＝画面の左下からはみ出すおそれ）")
            bad += 1
        cj[f"ep28/{n}.jpg"] = r["credit"]
        kind = "引用・非公開" if r["private"] else ("公的な機関の頁" if r["page"] else "この回の土地と物")
        cr_ = r.get("credit") or ""
        mod = ("・顔とナンバーに升目" if "顔とナンバー" in cr_ else "・ナンバーに升目" if "ナンバーにモザイク" in cr_ else "・顔に升目") if r.get("mosaic") else ""
        use = " ".join(cuts) + (f"（地 {r['ji']}）" if r["ji"] else "")
        url = r["url"] if not r["url"].startswith("commons:") else f"Commons（記号 {r['code']}＝git の外の目録 `src/commons/geo28.json`）"
        rows.append(f"| `{Path(n).name}` | {use or '—'} | {y if y else '不明'} | {r['lic']}（{kind}{mod}） | {r['who']} | {url} |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真と紙面 {len(cj)}点{'' if not bad else f'・🔴 {bad}'}")
    if bad:
        return 1
    if not write:
        return 0
    CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-11-01（⑤b-2）。`qa_out/ep28_assets.py credits --write` が書く（手で直さない）。写真と紙面は映像方針の一覧 `ref/ep28/eizou_list28.md`（了承② 2026-11-01）。",
        "🔴 会社の事件の回（ルール §B2-11）＝会員・SNS の投稿者・役員・弁護士の名前は書かない・攻撃した者は「第三者」「攻撃した者」・会社を犯人と言わない。",
        "",
        "### 0. 会社の頁・適時開示と公的な機関の頁",
        "- 会社（タイムズモビリティの新着情報・パーク24 の適時開示）＝規約は私的利用だけで引用に触れない＝著作権法32条の引用の型（出典・日付・語りが主・話している秒だけ・無加工の額装・"
        "頁の頭と代表者名を写さない）。🔴 **公開リポに置かない**（`ep28/police/`＝git の外・Modal の保管庫）。⚠️ 法律の助言ではない＝こちらの読み",
        "- 公的な機関（2026-11-01 に各頁で規約を読んだ）＝金融庁・個人情報保護委員会・首相官邸・国家サイバー統括室・e-Gov＝公共データ利用規約 PDL1.0／福岡県警＝政府標準利用規約（CC BY 4.0 互換）"
        "＝出典と編集の断り（「／改変：切出」）で利用する・ロゴは写さない・公開リポに置く。三重県警＝規約の頁が見つからない＝引用の型・`ep28/police/`",
        "",
        "### 1. 写真と紙面（Commons の CC BY・BY-SA・CC0・PD・会社の引用・公的な機関の頁）",
        "- CC BY・BY-SA＝「写真：{作者}／Wikimedia Commons（ライセンス）」。🔴 撮影者の名前はこのリポに書かない＝`ref/ep28/credits.json` は印 `{作者}` だけ・"
        "焼くときに git の外の表 `ref/ep28/src/credits_private.tsv` から足す（`tools/scene_jiko.ep28_credit`）。CC0・PD＝「Wikimedia Commons（CC0／パブリックドメイン）」",
        "- BY-SA＝額装（無加工・1点1カット・升目もかけない＝人とナンバーが写っていない点だけ）。CC BY・CC0・PD の私人の顔とナンバーは升目（「／改変：…にモザイク」）。色は原本のまま",
        "- 説明カットの地（「地 c…」）＝CC BY・CC0・PD の写真を暗くするだけ（字と地の比 8:1 が下限・出典の行は「地の写真：…／改変：明るさ」）",
        "- 撮影年＝Commons の頁の撮影日・文書の日付（sources28 の時期の欄）",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. イメージ（Pexels の映像）＝⑤b-3 で足す（clips.json）",
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


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "edges": cmd_edges}
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
