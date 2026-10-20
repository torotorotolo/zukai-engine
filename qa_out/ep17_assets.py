# -*- coding: utf-8 -*-
"""ep17_assets.py — 17本目（中華航空140便墜落事故）の写真・頁・映像の束（⑤b-2・2026-10-20）。23本目 `ep23_assets.py`（Commons の作者の印・
フリー素材）と20本目 `ep20_assets.py`（報告書の写真・防衛庁記録）・21本目 `ep21_assets.py`（使わない窓）の形を合わせた。

取得はすんでいる（映像方針＝了承②・`ref/ep17/eizou_build/fetch17.py`・記録 `fetch17.tsv`＝md5 2回）。ここは**束を作る道**だけを持つ。
  python qa_out/ep17_assets.py build             # 写真・頁の束 ref/ep17/<名>.jpg（イメージは ref/ep17/stock/<名>.jpg）＋ 権利の台帳 ref/ep17/assets.json
  python qa_out/ep17_assets.py look R01 R02 …    # 束の写真を並べた見本（scratchpad へ・1枚 960 幅）＝選ぶとき・確かめるとき
  python qa_out/ep17_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python qa_out/ep17_assets.py edges             # 束の四辺の暗い帯（スライドの台紙の縁）＝門番 check_photo_edge の名簿を決める
  python qa_out/ep17_assets.py credits [--write] # 画面の出典 ref/ep17/credits.json と ref/CREDITS.md の17本目の節
  python qa_out/ep17_assets.py shots             # ref/ep17/shots.json（記録映像 V1＝使う区間のまわりをコマごとに・フリー素材＝1秒1コマ）
  python qa_out/ep17_assets.py clips             # ref/ep17/clips.json（記録映像 V1・フリー素材の映像の台帳）
  python qa_out/ep17_assets.py nogo              # tools/footage.py の EP17_NOGO（映像方針の「使わない」窓＝その秒を含むショットまるごと）
  python qa_out/ep17_assets.py use               # tools/footage.py の EP17_USE（🔴 章ファイルに `ss.vid`／`ss.head` を書いたカットだけ）
  python qa_out/ep17_assets.py fb [c101 …]       # 映像のひかえの静止画（記録映像＝ref/ep17/fb_<cid>.jpg・フリー素材＝ref/ep17/stock/fb_<cid>.jpg）

入力＝映像方針の一覧 `ref/ep17/eizou_build/list17.tsv`（生成物・秒は narration.json の実測＝⑤b-1）・出どころ `sources17.psv`（区切り「|」）・
取得の記録 `fetch17.tsv`。元は `ref/ep17/src/`（git の外＝報告書の PDF・Commons・フリー素材・記録映像）。
🔴 **報告書の写真（R＝写真N）と頁（F＝付図N）は PDF の頁の画像（8ビットの灰色・約400dpi の走査）から切る**＝頁の文字の層の題「写真N」の位置で
   写真の矩形を当てる（`tools/extract_photos.py` の photo_boxes・assign・clip_text＝升目ごとのばらつきで写真を探す・題の帯を外す）。
   白黒のまま（原本の色＝了承② 決め・PHOTO_KEEP）・長辺を縮めるだけ（幅 2400 か高さ 1350 の大きい方まで）。
🔴 束の写真は長辺を縮めるだけ（色・切り口はそのまま）＝幅 2400 か高さ 1350 の大きい方まで。それ以下は縮めない（Commons の 960〜1280px の点はそのまま）。
🔴 **イメージ（フリー素材の写真＝Pexels の4点）は git に入れない**（19本目 決め⑨）＝取ったファイルそのまま（md5 が取得のときと同じ）。
   Actions・Modal の上では `tools/footage.py` の `stock_photos()` が台帳の `media`（直リンク）から取り直して md5 を照らす（違えば止める）。
🔴 **個人名義の Commons の点（作者欄が個人）は、画面の出典の行に作者欄の名前を出すが、名前は公開リポに書かない**（23本目の型）
   ＝credits.json の行は印 `{作者}` だけ・焼くときに `scene_jiko.ep17_credit` が git の外の表 `ref/ep17/src/credits_private.tsv` から足す
   （Modal は保管庫 `jiko-assets` の同じ道・Actions の試し焼きだけ仮の字）。CC0・PD は表示が任意＝名前を出さない（記憶 no-optional-credits）。
🔴 **「関連」の写真（事故そのものではない実物＝同じ型の操縦室・機関の建物・空港・消防車・中華航空のほかの機体）は台帳に `related: true`**
   ＝一覧の種類「関連」から（同じ記号を「実写」と「関連」の両方に当てていたら止める）。門番 check_text_screens が PLAN の注と照らし、
   20% の数（この事故の写真）から外す。報告書の頁（F・P）・判決（J）・FAA の報告（L）の頁は台帳に `page: true`（写真に数えない）。
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
EPD = HERE / "ref" / "ep17"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list17.tsv"
SOURCES = BUILD / "sources17.psv"
FETCH = BUILD / "fetch17.tsv"
PRIVATE = EPD / "src" / "credits_private.tsv"      # 🔴 git の外（作者欄・題）＝ここから名前を公開の物へ写さない
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
FOOTAGE = HERE / "tools" / "footage.py"
SCRATCH = HERE / "out" / "ep17_look"           # look の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## 中華航空140便墜落事故（1994-04-26・17本目）"
AUTHOR = "{作者}"            # 個人名義の点の画面の出典の行の印（焼くときに git の外の表から足す＝scene_jiko.ep17_credit）
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（footage.py の注）
EVENT_YEAR = 1994            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）
CR_JTSB = "出典：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』"

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
PAGE_LONG = 3600                       # 頁（付図）は長辺 3600 まで＝欄の切り出し（c106 の「GO AROUND」の欄）で字を読める大きさを残す
JPEG_Q = 92
MOSAIC_PX = 14                         # 顔のモザイクの升（束の画素）
FRAME_RIGHTS = ("BY-SA", "GFDL")       # 額装だけ（了承② 決め7＝BY-SA・GFDL は額装・無加工・額ごと動かす・1点1カット）
# 🔴 頁は使うチャットで足す（その章の切り口と一緒に決める）。⑤b-2 は冒頭の c106（と同じ頁の c113・c309）が使う付図29 だけ
#   🆕 ⑤b-7（10-21）：残りの頁を全部（報告書の付図10・写真51・本文 p95／FAA の報告 3頁／判決 2頁）
PAGES_NOW = ("F29", "F01", "F03", "F04", "F05", "F08", "F09", "F11", "F12", "F28", "P51", "P95", "L64", "L80", "L03", "J1", "J98")
# 🆕 ⑤b-7：報告書の本文の頁（文字の頁）＝題「付図N」「写真N」が無い＝頁の字の層の目印で当てる（1頁だけ当たらなければ止める）
TEXT_ANCHOR = {"P95": "４原因", "P51": "写真５１分割した"}     # P51＝題の番号のすぐ後ろに字が続く（_CAP の「番号のあとに空白」に合わない）
# 🆕 ⑤b-7：報告書でない頁（FAA の報告・判決）＝文字の PDF の頁を絵にする（PDF の頁番号は sources17 の page 欄「PDF p.N」）
DOC = {
    "L": dict(credit="出典：アメリカ連邦航空局『The Interfaces Between Flightcrews and Modern Flight Deck Systems』（1996年）",
              who="アメリカ連邦航空局（FAA Human Factors Team・1996年6月）", url="https://www.faa.gov/sites/faa.gov/files/2022-11/interfac.pdf",
              year=(1996, "報告の日付（June 18, 1996）")),
    "J": dict(credit="出典：名古屋地方裁判所 2003年12月26日判決（平成7年(ワ)第4179号）",
              who="名古屋地方裁判所（判決＝著作権の目的とならない・著作権法13条）", url="https://www.courts.go.jp/hanrei/7587/detail4/index.html",
              year=(2003, "判決の日（裁判所の判例の頁）")),
}
DOC_PART = {"L64": "図4", "L80": "本文", "L03": "序文"}      # ⚠️「p80」の形は門番 wording が鳴る＝資料の中の名で
PAGE_DPI_LONG = 3600                   # 文字の PDF の頁を絵にするときの長辺（報告書の頁の束と同じ）

# 撮影年（副題の年の主張と照らす＝check_credits）。出どころ＝sources17.psv の note（Commons の頁の撮影日・題）。分からない点は None
#   （表は「不明」・副題に年を書かない）。報告書の写真は1994年（写真1〜4＝事故の直後・ほかは焼き込みの日付「5 13 '94」など＝5月の調査）
YEAR = {
    "E1": (1993, "note「1993-04-13・名古屋空港」"), "E2": (None, "note「撮影日不明」"), "E3": (1991, "note「1991-09-30」"),
    "T1": (1993, "題「19 OCT 1993」"), "K05": (2005, "題「20050925」"), "K04": (2004, "題「20041023」"), "K05b": (2005, "題「20050429」"),
    "B192": (1998, "題「FEB 1998」"), "B194": (1998, "題「FEB 1998」"), "N1810": (None, "note「1992年ごろ」＝撮影日の記載なし"),
    "QA": (2004, "note「2004年」"), "QB": (2003, "note「2003年」"), "QC": (2020, "note「2020年」"), "JAS": (1999, "題「Oct99」"),
    "AB1": (2024, "note「2024年撮影」"), "AB2": (2024, "note「2024年」"), "AB3": (2024, "note「2024年」"), "FAA": (2016, "note「2016年」"),
    "NTSB": (2026, "note「2026年」"), "CT1": (2021, "note「2021年」"), "HEL": (1981, "題「lentoasemaa 1981」"),
    "ARF": (2014, "note「2014年」"), "ARF2": (2014, "題「February 23, 2014」"), "B747": (1996, "note「1996年11月」"),
    "A310": (1982, "題「11-9-82」"),
}
# 画面の出典の行の名（個人名義でない点）。CC0・PD は表示が任意＝作者の名前は出さない（Commons と所蔵の機関だけ）
ORG = {"HEL": "ヘルシンキ市立博物館", "FAA": "米議会図書館"}
LIC = {"PDL1.0": "PDL1.0", "BY-SA 2.0": "CC BY-SA 2.0", "BY-SA 3.0": "CC BY-SA 3.0", "BY-SA 4.0": "CC BY-SA 4.0", "GFDL 1.2": "GFDL 1.2",
       "CC BY 2.0": "CC BY 2.0", "CC BY 3.0": "CC BY 3.0", "CC BY 4.0": "CC BY 4.0", "CC0": "CC0", "PD": "パブリックドメイン",
       "Pexels License": "Pexels License", "Pixabay Content License": "Pixabay Content License",
       "PD（米連邦政府）": "パブリックドメイン（米連邦政府）", "判決（著作権の目的とならない・著作権法13条）": "判決（著作権の目的とならない）"}
LIC_URL = {"Pexels License": "https://www.pexels.com/license/", "Pixabay Content License": "https://pixabay.com/service/license-summary/"}
# 顔だけモザイク {記号: [(x0, y0, x1, y1, 誰)]}（元の画像の画素）＝原寸で見てから書く（⑤b-2・2026-10-20＝scratchpad の切り出しを1〜2倍で見た）
#   ARF（c802・CC BY 3.0＝改変を許す）＝消防車の右の見物の人5人の頭（真ん中の男性は Commons の投稿の時点でぼかしてある＝重ねて升目に）。
#   見て外した点＝QC の窓の外の2人（背中＝顔は写っていない・c105 の窓の外）・ARF2 の左と右の人（緑の上着・迷彩のズボン＝航空祭の隊員＝公的な任務）・
#   A310 の見物の人（顔 約7px＝見分けられない）・R04（白い防護服の作業の人＝顔は分からない・担架と覆われた物は見分けられない）
MASK = {
    "ARF": [(1028, 575, 1056, 609, "左の人"), (1051, 575, 1077, 609, "真ん中の男性（もとからぼかし）"), (1088, 595, 1114, 622, "白い帽子の人"),
            (1215, 622, 1254, 656, "右のかがんだ人"), (999, 673, 1036, 704, "左下のかがんだ人")],
}
DESCREEN = 1.6                         # 🔴 報告書の写真の網点をほどくぼかし（縮める前・約400dpi で）＝0 だと粒が画面いっぱいに（⑤b-2 に R11・R04 を 0・1.0・1.6 で見比べた）


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
            raise SystemExit(f"🔴 sources17.psv の行の欄が足りない：{ln[:80]}")
        out[f[0]] = dict(zip(["code", "class", "file", "page", "media", "get", "dims", "bytes", "rights", "credit", "note"], f))
    return out


def _fetched():
    out = {}
    for ln in FETCH.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if ln.startswith("#") or len(f) < 7 or f[0] == "code":
            continue
        out[f[0]] = dict(zip(["code", "file", "bytes", "md5", "md5_check", "dims", "get"], f))
    return out


def _private():
    """git の外の表 {記号: {title, artist, license, date, page}}。無ければ止める（束を作る手元だけで読む）"""
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の作者欄の表＝映像方針の fetch17.py credits）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    return {r[0]: dict(zip(rows[0], r)) for r in rows[1:]}


def _codes_of(r):
    """一覧の1行の素材の記号（主＋頭の差し込みの写真など「+」で足した記号）＝[(記号, 寄りの名)]"""
    out = [(r["code"], r["part"])] if r["code"] else []
    for x in (r.get("extra") or "").split("+"):
        if x.strip():
            c, p = (x.strip().split(":", 1) + [""])[:2]
            out.append((c, p))
    return out


def uses():
    """{記号: [カット]}（一覧の素材の欄から・写真・頁・イメージの静止画だけ＝映像は台帳 clips.json の側）。頁は PAGES_NOW だけ"""
    src = _sources()
    out = {}
    for r in _list():
        for c, _ in _codes_of(r):
            s = src.get(c, {})
            if s.get("class") == "page" and c not in PAGES_NOW:
                continue
            if s.get("class") in ("photo", "page") or (s.get("class") == "stock" and s["file"].lower().endswith(".jpg")):
                out.setdefault(c, []).append(r["cid"])
    return out


def related_of(code):
    """一覧の種類「関連」の記号か。同じ記号を「関連」と「実写」の両方に当てていたら止める（20% の数が揺れる）"""
    kinds = {r["kind"] for r in _list() for c, _ in _codes_of(r) if c == code}
    if "関連" in kinds and kinds - {"関連"}:
        raise SystemExit(f"🔴 {code}: 一覧の種類が「関連」と {sorted(kinds - {'関連'})} に割れる（20% の数が決まらない）")
    return kinds == {"関連"}


def name_of(code, s):
    if s["class"] == "stock":
        return f"stock/{Path(s['file']).stem.lower()}"
    return code.lower()


# ── 報告書の写真・頁（PDF の頁の画像から） ───────────────────────────
_CAP = re.compile(r"^(写真|付図)\s*([0-9０-９]+)(?=[\s　]|$)")
_ZEN = str.maketrans("０１２３４５６７８９", "0123456789")


def _page_image(page, tol=1):
    """頁の画像（1頁1枚の走査）＝(灰色の PIL 画像, 頁の点→画素の倍率 (sx, sy))。画像が1枚でなければ止める"""
    import fitz
    from PIL import Image
    imgs = page.get_images(full=True)
    if len(imgs) != 1:
        raise SystemExit(f"🔴 頁 {page.number + 1}: 画像が {len(imgs)} 枚（1頁1枚の走査を前提にしている）")
    xref = imgs[0][0]
    pix = fitz.Pixmap(page.parent, xref)
    if pix.n != 1:
        pix = fitz.Pixmap(fitz.csGRAY, pix)
    im = Image.frombytes("L", (pix.width, pix.height), pix.samples)
    rect = page.get_image_rects(xref)[0]
    if tol is not None and (abs(rect.x0) > tol or abs(rect.y0) > tol or abs(rect.x1 - page.rect.width) > tol or abs(rect.y1 - page.rect.height) > tol):
        raise SystemExit(f"🔴 頁 {page.number + 1}: 画像が頁いっぱいに置かれていない（{rect}）＝座標の当て方を確かめる")
    return im, (pix.width / page.rect.width, pix.height / page.rect.height)


def _find_page(pdf, kind, num):
    """題「写真N」「付図N」（行の頭）がある頁＝(doc, page, 題の行の箱〈点〉の並び)。無いか2頁以上なら止める"""
    import fitz
    d = fitz.open(pdf)
    hits = []
    for pg in d:
        pg.set_rotation(0)
        caps = []
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                t = "".join(s["text"] for s in ln["spans"]).strip()
                m = _CAP.match(t)
                if m:
                    caps.append((tuple(ln["bbox"]), m.group(1), int(m.group(2).translate(_ZEN))))
        if any(k == kind and n == num for _, k, n in caps):
            hits.append((pg, caps))
    if len(hits) != 1:
        raise SystemExit(f"🔴 {Path(pdf).name}: 題「{kind}{num}」の頁が {len(hits)} 頁")
    return d, hits[0][0], hits[0][1]


def _find_text_page(pdf, anchor):
    """🆕 ⑤b-7：字の層（空白を詰めた字）に目印がある頁＝(doc, page)。1頁でなければ止める"""
    import fitz
    d = fitz.open(pdf)
    hits = [pg for pg in d if anchor in re.sub(r"[\s　]", "", pg.get_text())]
    if len(hits) != 1:
        raise SystemExit(f"🔴 {Path(pdf).name}: 目印「{anchor}」の頁が {len(hits)} 頁")
    return d, hits[0]


def doc_page(code, s):
    """🆕 ⑤b-7：報告書でない頁（FAA の報告・判決＝文字の PDF）を絵にする＝(RGB の PIL 画像, 記録の dict)。
    PDF の頁番号＝sources17 の page 欄「PDF p.N」。長辺 PAGE_DPI_LONG で描いて、インクの外接（四辺 24px の余白）で切る"""
    import fitz
    import numpy as np
    from PIL import Image
    m = re.search(r"PDF p\.(\d+)", s["page"])
    if not m:
        raise SystemExit(f"🔴 {code}: 頁の欄に「PDF p.N」が無い（{s['page']}）")
    pdf = HERE / s["file"]
    d = fitz.open(pdf)
    pg = d[int(m.group(1)) - 1]
    k = PAGE_DPI_LONG / max(pg.rect.width, pg.rect.height)
    pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    a = np.asarray(im.convert("L"))
    ys, xs = np.where(a < 200)
    h, w = a.shape
    box = (max(0, xs.min() - 24), max(0, ys.min() - 24), min(w, xs.max() + 24), min(h, ys.max() + 24))
    rec = dict(pdf=s["file"], pdf_page=pg.number + 1, pdf_md5=md5(pdf), box_px=[int(v) for v in box],
               how=f"文字の PDF の頁を描いた（長辺 {PAGE_DPI_LONG}px）・インクの外接")
    return im.crop(box), rec


def ja_crop(code, s):
    """報告書の写真（R）・頁（F・P）を頁の画像から切る＝(灰色の PIL 画像, 記録の dict)。
    写真＝題の下の矩形（升目のばらつき）・頁（付図）＝題を含めた頁のインクの外接（題「付図N」を画面に残す＝何の図か分かる）"""
    sys.path.insert(0, str(HERE / "tools"))
    import numpy as np
    import extract_photos as EX
    kind = "付図" if code.startswith("F") else "写真"       # P51＝報告書の「写真51」（線画の入った頁ごと見せる）
    num = int(re.sub(r"\D", "", code))
    pdf = HERE / s["file"]
    if code in TEXT_ANCHOR:
        d, pg = _find_text_page(pdf, TEXT_ANCHOR[code])     # 🆕 ⑤b-7：本文の頁（題が無い）＝字の層の目印で当てる
        caps = []
    else:
        d, pg, caps = _find_page(pdf, kind, num)
    # 🆕 ⑤b-7：頁（付図・写真51・本文）は字の層の座標を使わず、画像のインクの外接だけで切る＝置き場の数ポイントのずれ
    #   （付図1＝左 1.08pt 内側・付図3＝下へ 2.45pt・付図8＝6.1pt はみ出し）は効かない＝頁は置き場を確かめない（写真は 1pt のまま＝題の箱で当てる）
    im, (sx, sy) = _page_image(pg, tol=None if (kind == "付図" or s["class"] == "page") else 1)
    a = np.asarray(im).copy()
    tboxes = []
    for b in pg.get_text("blocks"):
        x0, y0, x1, y1 = int(b[0] * sx), int(b[1] * sy), int(b[2] * sx), int(b[3] * sy)
        a[max(y0 - 6, 0):y1 + 6, max(x0 - 6, 0):x1 + 6] = 255
        tboxes.append((x0, y0, x1, y1))
    rec = dict(pdf=s["file"], pdf_page=pg.number + 1, pdf_md5=md5(pdf))
    if kind == "付図" or s["class"] == "page":
        # 頁＝インクの外接（題の行も入れる＝白で消す前の画像で測る）。走査の縁の影（端の 0.5% の黒い帯）は外す
        b = np.asarray(im)
        h, w = b.shape
        m = int(min(h, w) * 0.005)
        ys, xs = np.where(b[m:h - m, m:w - m] < EX.INK)
        box = (max(0, xs.min() + m - 24), max(0, ys.min() + m - 24), min(w, xs.max() + m + 24), min(h, ys.max() + m + 24))
        rec.update(box_px=[int(v) for v in box], how="頁のインクの外接（題を含む）")
        return im.crop(box), rec
    boxes = EX.photo_boxes(a)
    cps = [(tuple(v * (sx if i % 2 == 0 else sy) for i, v in enumerate(c[0])), "写真", c[2], 0) for c in caps if c[1] == "写真"]
    want = [i for i, c in enumerate(cps) if c[2] == num]
    if len(cps) == 1:
        if not boxes:
            raise SystemExit(f"🔴 {code}: 頁 {pg.number + 1} に写真の矩形が無い")
        box = EX.union(boxes)
    else:
        idx, left = EX.assign(cps, boxes)
        j = idx[want[0]]
        if j is None:
            raise SystemExit(f"🔴 {code}: 頁 {pg.number + 1} の題「写真{num}」に当たる矩形が無い（矩形 {len(boxes)}・余り {left}）")
        box = boxes[j]
        cx = (cps[want[0]][0][0] + cps[want[0]][0][2]) / 2
        if not box[0] - 60 <= cx <= box[2] + 60:
            raise SystemExit(f"🔴 {code}: 題の真下に写真が無い（題 x={cx:.0f}・写真 x={box[0]}〜{box[2]}）＝当て方を確かめる")
    box = EX.clip_text(box, tboxes)
    # 🔴 矩形は升目（32px）の格子＝写真のまわりの紙の白が最大 31px 残る（⑤b-2 の見本 R01〜R04 の右と下に白い帯）
    #    →四辺から、紙の行・列（明るく平ら＝平均 PAPER_MEAN 超・ばらつき PAPER_STD 未満）を内へ削る（各辺 PAPER_MAX まで）
    box, cut = _trim_paper(np.asarray(im), box)
    rec.update(box_px=[int(v) for v in box], paper_px=cut, how=f"題「写真{num}」の下の矩形（升目のばらつき・題の帯と紙の白を外した）")
    return im.crop(box), rec


PAPER_MEAN, PAPER_STD, PAPER_MAX = 228.0, 14.0, 0.06


def _trim_paper(a, box):
    """box の四辺から紙の白の行・列を削る＝(新しい box, {辺: 削った px})。削りすぎ（各辺 PAPER_MAX 超）は止めずに上限で止める"""
    x0, y0, x1, y1 = (int(v) for v in box)
    cut = {}

    def paper(v):
        return v.mean() > PAPER_MEAN and v.std() < PAPER_STD

    lim_x, lim_y = int((x1 - x0) * PAPER_MAX), int((y1 - y0) * PAPER_MAX)
    n = 0
    while n < lim_y and paper(a[y0 + n, x0:x1]):
        n += 1
    cut["t"], y0 = n, y0 + n
    n = 0
    while n < lim_y and paper(a[y1 - 1 - n, x0:x1]):
        n += 1
    cut["b"], y1 = n, y1 - n
    n = 0
    while n < lim_x and paper(a[y0:y1, x0 + n]):
        n += 1
    cut["l"], x0 = n, x0 + n
    n = 0
    while n < lim_x and paper(a[y0:y1, x1 - 1 - n]):
        n += 1
    cut["r"], x1 = n, x1 - n
    return (x0, y0, x1, y1), cut


def _shrink(im, long_side=None):
    from PIL import Image
    w1, h1 = im.size
    k = (min(1.0, long_side / max(w1, h1)) if long_side else min(1.0, max(BUNDLE_W / w1, BUNDLE_H / h1)))
    if k < 1.0:
        im = im.resize((round(w1 * k), round(h1 * k)), Image.LANCZOS)
    return im, k


def _to_srgb(im):
    """色の札が sRGB でなければ sRGB の RGB に直す。戻り＝(絵, 何をしたか)"""
    from PIL import ImageCms
    icc = im.info.get("icc_profile")
    if not icc:
        return im.convert("RGB"), "札なし（sRGB と読む）"
    src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
    desc = ImageCms.getProfileDescription(src).strip()
    if im.mode != "CMYK" and (desc.startswith("sRGB") or desc == "c2"):
        return im.convert("RGB"), f"札 {desc}（sRGB のまま）"
    out = ImageCms.profileToProfile(im, src, ImageCms.createProfile("sRGB"), renderingIntent=1, outputMode="RGB")
    return out, f"{im.mode} 札 {desc} → sRGB"


def mosaic(im, boxes, n):
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）＝16本目・20本目・23本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def personal(s):
    """画面の出典の行に作者欄の名前を出す点＝個人名義で、表示が要る権利（CC0・PD は表示が任意＝名前を出さない）"""
    return "作者は src/credits_private.tsv" in s["credit"] and s["rights"] not in ("CC0", "PD")


def screen_credit(code, s, frame, mask):
    """画面の出典の行。🔴 CC BY・BY-SA は必ず「改変」の語を書く＝`scene_jiko.credit_of` の古い決まり（6本目）が「CC BY」があって「改変」の
    語が無い行に「／改変：色調変更・切出」を黙って足す（23本目 ⑤b-2 の試し焼きで出た）"""
    r = s["rights"]
    if s["class"] == "page" and code[0] in DOC:
        return DOC[code[0]]["credit"] + (DOC_PART.get(code, "") if code[0] == "L" else "") + ("（パブリックドメイン）" if code[0] == "L" else "")
    if r == "PDL1.0":
        m = re.search(r"『航空事故調査報告書 96-5』(.+)$", s["credit"])
        if not m:
            raise SystemExit(f"🔴 {code}: 報告書の出典の欄が読めない（{s['credit']}）")
        return CR_JTSB + m.group(1) + ("・顔にモザイク" if mask else "")
    if s["class"] == "stock":
        return f"イメージ（{'Pixabay' if 'Pixabay' in r else 'Pexels'}）"
    lic = LIC[r]
    who = AUTHOR if personal(s) else ORG.get(code, "Wikimedia Commons")
    if r in ("CC0", "PD"):
        return f"写真：{who}（{lic}）"
    if frame:
        return f"写真：{who}（{lic}）・改変なし"
    return f"写真：{who}（{lic}）・改変：切出" + ("・顔にモザイク" if mask else "")


def who_of(code, s):
    if s["class"] == "page" and code[0] in DOC:
        return DOC[code[0]]["who"]
    if s["rights"] == "PDL1.0":
        return "運輸省 航空事故調査委員会（報告書 96-5・1996年）"
    if s["class"] == "stock":
        return "投稿者（クレジットは任意＝書かない）"
    if personal(s):
        return "作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`）"
    if code in ORG:
        return ORG[code]
    return "Commons の投稿者（CC0・PD＝表示は任意）"


def year_of(code, s):
    if s["class"] == "stock":
        return None, "この事故の物でない（イメージ）"
    if s["class"] == "page" and code[0] in DOC:
        return DOC[code[0]]["year"]
    if s["rights"] == "PDL1.0":
        if s["class"] == "page":
            return 1996, "報告書 96-5 の公表（1996年7月）＝頁"
        return 1994, "報告書の写真（写真1〜4＝事故の直後・ほか＝1994年5月の調査の焼き込みの日付）"
    if code not in YEAR:
        raise SystemExit(f"🔴 {code}: 撮影年の出どころが表 YEAR に無い")
    return YEAR[code]


# ── 束を作る ─────────────────────────────────────────────────
def cmd_build():
    from PIL import Image, ImageOps
    src, fet, priv = _sources(), _fetched(), _private()
    db, bad = {}, 0
    (EPD / "stock").mkdir(exist_ok=True)
    for code, cuts in sorted(uses().items()):
        s = src[code]
        name = name_of(code, s)
        dst = EPD / f"{name}.jpg"
        notes, box_m, rec = [], [], {}
        rel = related_of(code)
        if s["class"] == "page" and code[0] in DOC:
            # 🆕 ⑤b-7：FAA の報告・判決の頁（文字の PDF）＝描いて切るだけ（色・字はそのまま）
            im, rec = doc_page(code, s)
            notes.append(rec["how"])
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
            smd5 = rec["pdf_md5"]
        elif s["rights"] == "PDL1.0":
            im, rec = ja_crop(code, s)
            notes.append(rec["how"])
            if s["class"] == "photo":
                from PIL import ImageFilter
                im = im.filter(ImageFilter.GaussianBlur(DESCREEN))
                notes.append(f"網点をほどくぼかし {DESCREEN}（縮める前）")
            im, k = _shrink(im, PAGE_LONG if s["class"] == "page" else None)
            if k < 1.0:
                notes.append(f"縮小 ×{k:.3f}")
            if code in MASK:
                box_m = [(round(x0 * k), round(y0 * k), round(x1 * k), round(y1 * k), why) for x0, y0, x1, y1, why in MASK[code]]
                im = mosaic(im, box_m, MOSAIC_PX)
                notes.append(f"顔だけモザイク {len(box_m)}か所（升 {MOSAIC_PX}px）")
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
            smd5 = rec["pdf_md5"]
        else:
            f, sp = fet.get(code), HERE / s["file"]
            if not f or not sp.exists():
                print(f"🔴 {code}: fetch17.tsv の行か手元のファイルが無い（{s['file']}）")
                bad += 1
                continue
            if md5(sp) != f["md5"]:
                print(f"🔴 {code}: {sp.name} の md5 が取得のときと違う（取り直す）")
                bad += 1
                continue
            smd5 = f["md5"]
            if s["class"] == "stock":
                # 🔴 イメージ＝取ったファイルそのまま（向きの札 1 か無し・色の札は sRGB か無し）＝焼くときに直リンクから取り直せる
                with Image.open(sp) as im0:
                    ori, icc, (w, h) = im0.getexif().get(274), im0.info.get("icc_profile"), im0.size
                    _, how_c = _to_srgb(im0) if icc else (None, "色の札なし")
                if ori not in (None, 1) or (icc and "sRGB のまま" not in how_c):
                    print(f"🔴 {code}: イメージの札がそのまま使える形でない（向き {ori}・{how_c}）")
                    bad += 1
                    continue
                shutil.copyfile(sp, dst)
                notes.append(f"取ったファイルそのまま（{w}x{h}・向きの札 {ori}・{how_c}）")
            else:
                with Image.open(sp) as im0:
                    ori = im0.getexif().get(274)
                    im = ImageOps.exif_transpose(im0)
                    if ori and ori != 1:
                        notes.append(f"EXIF の向き {ori} を当てた（生の絵 {im0.size[0]}x{im0.size[1]}）")
                    im.info["icc_profile"] = im0.info.get("icc_profile")
                    im, how_c = _to_srgb(im)
                notes.append(how_c)
                im, k = _shrink(im)
                if k < 1.0:
                    notes.append(f"縮小 ×{k:.3f}")
                if code in MASK:
                    box_m = [(round(x0 * k), round(y0 * k), round(x1 * k), round(y1 * k), why) for x0, y0, x1, y1, why in MASK[code]]
                    im = mosaic(im, box_m, MOSAIC_PX)
                    notes.append(f"顔だけモザイク {len(box_m)}か所（升 {MOSAIC_PX}px）")
                im.save(dst, quality=JPEG_Q, optimize=True)
                w, h = im.size
        if personal(s) and not priv.get(code, {}).get("artist"):
            print(f"🔴 {code}: 個人名義なのに git の外の表に作者欄が無い")
            bad += 1
        frame = s["rights"].startswith(FRAME_RIGHTS)
        y, ywhy = year_of(code, s)
        lic = LIC.get(s["rights"])
        if not lic:
            print(f"🔴 {code}: 権利の記号が読めない（{s['rights']}）")
            bad += 1
            continue
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(cuts), credit=screen_credit(code, s, frame, bool(box_m)),
                        who=who_of(code, s), note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=lic, frame=frame, ground=s["rights"], url=s["page"] if s["page"].startswith("http") else
                        DOC[code[0]]["url"] if s["class"] == "page" and code[0] in DOC else "https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851", blur=[], how="・".join(notes), year=y, year_why=ywhy,
                        stock=s["class"] == "stock", page=s["class"] == "page", related=rel, quote_page=False, named=personal(s),
                        mosaic=[list(b[:4]) for b in box_m] or None, masked_before=None, **({"src_rec": rec} if rec else {}))
        if s["class"] == "stock":
            db[name]["media"] = s["media"]            # 🔴 焼くときに取り直す直リンク（footage.stock_photos が md5 を照らす）
        print(f"✓ {code:6} {name:12} {w}x{h:<5} {' '.join(cuts):16} {lic}{'  額装だけ' if frame else ''}{'  関連' if rel else ''}"
              f"{'  頁' if s['class'] == 'page' else ''}  {'・'.join(notes)[:90]}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    print(f"→ ref/ep17/assets.json（{len(db)}点・額装だけ {sum(1 for r in db.values() if r['frame'])}・関連 {sum(1 for r in db.values() if r['related'])}"
          f"・頁 {sum(1 for r in db.values() if r['page'])}・イメージ {sum(1 for r in db.values() if r['stock'])}・名前を足す点 "
          f"{sum(1 for r in db.values() if r['named'])}・モザイク {sum(1 for r in db.values() if r['mosaic'])}・束の大きさ {tot / 1e6:.1f}MB）")
    return 1 if bad else 0


def cmd_look(codes, out_name="look.jpg", width=960):
    """束の写真を並べた見本（2列）＝リポの外（SCRATCH）。記号を渡す（R01 など）"""
    from PIL import Image, ImageDraw
    db = json.loads(DB.read_text(encoding="utf-8"))
    by_code = {r["code"]: n for n, r in db.items()}
    ims = []
    for c in codes:
        n = by_code.get(c)
        if not n:
            raise SystemExit(f"🔴 {c} は束に無い（build を先に）")
        im = Image.open(EPD / f"{n}.jpg").convert("RGB")
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        ImageDraw.Draw(im).rectangle((0, 0, 150, 40), fill=(0, 0, 0))
        ImageDraw.Draw(im).text((8, 8), c, fill=(255, 255, 0))
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
        m = PE.margins(f"ep17/{n}.jpg")
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
    """撮影年＝year_of（出どころつき）。当てたカットの副題が名乗る年（「NNNN年」・「当日」＝1994）と食い違えば止める"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    priv = _private()
    names = {v.get("artist", "").strip() for v in priv.values()} - {""}
    cj, rows, bad = {}, [], 0
    for n, r in sorted(db.items()):
        cuts = r["cut"].split()
        claims = set()
        for c in cuts:
            # 「1992年ごろ」「1980年代」は撮影年の主張でない（check_credits と同じ＝ごろは ⚠️ で目で決める）
            claims |= {int(y) for y in re.findall(r"(1[89]\d\d|20\d\d)年(?!代|ごろ)", subs.get(c, ""))}
            if "当日" in subs.get(c, ""):
                claims.add(EVENT_YEAR)
        y = r["year"]
        if claims and (y is None or claims != {y}):
            print(f"🔴 {n}: 副題の年 {sorted(claims)} と撮影年 {y} が食い違う（{' '.join(cuts)}）")
            bad += 1
        leak = [x for x in names if x and x in json.dumps(r, ensure_ascii=False)]
        if leak:
            print(f"🔴 {n}: 台帳の行に作者の名前が入っている（{len(leak)}語）＝名前は印 {AUTHOR} で")
            bad += 1
        cj[f"ep17/{n}.jpg"] = r["credit"]
        mod = "・顔にモザイク" if r.get("mosaic") else ""
        kind = "イメージ" if r["stock"] else ("頁" if r["page"] else ("関連" if r["related"] else "この事故"))
        rows.append(f"| `{Path(n).name}` | {' '.join(cuts)} | {y if y else '不明'} | {r['lic']}（{kind}{mod}） | {r['who']} | {r['url']} |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真・頁 {len(cj)}点{'' if not bad else f'・🔴 {bad}'}")
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
        "※2026-10-20（⑤b-2）。`qa_out/ep17_assets.py credits --write` が書く（手で直さない）。写真と映像は映像方針の一覧 `ref/ep17/eizou_list17.md`（了承② 2026-10-19）。",
        "",
        "### 0. 映像（記録映像 V1・フリー素材＝音はすべて使わない＝`-an`）",
        "- 記録映像 V1＝防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0・防衛省の YouTube 公式・Commons にも同じ版）。4:3 の中身を横いっぱい・"
        "上を残して下を切る（焼き込みの字幕と日付を外す）・再生の速さを変えることがある＝画面の出典に「改変：切出・再生速度」",
        "- フリー素材（Pexels・Pixabay・生成AI は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」「イメージ（Pixabay）」だけ"
        "（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）",
        "",
        "| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |",
        "|---|---|---|---|---|", *film_rows, "",
        "### 1. 写真・頁（報告書 96-5〈PDL1.0〉・Commons・イメージ）",
        "- 報告書の写真と付図＝運輸省 航空事故調査委員会『航空事故調査報告書 96-5』（1996年・公共データ利用規約 PDL1.0＝出典と加工の旨）。"
        "頁の走査（灰色・約400dpi）から切り出し、白黒のまま縮めた＝画面の出典に「（加工して作成）」",
        "- 🔴 **CC BY-SA・GFDL は額装だけ**（了承② 決め7＝無加工・額ごと動かす・1点1カット＝`cuts/ss.check_frame_only`）",
        "- 🔴 **個人名義の点は画面の出典の行に作者欄の名前**。名前はこのリポに書かない＝`ref/ep17/credits.json` は印 `{作者}` だけ・焼くときに"
        " git の外の表から足す（`tools/scene_jiko.ep17_credit`）。名前は各行の Commons の頁の作者欄。CC0・PD は表示が任意＝名前を出さない",
        "- 「関連」＝事故そのものではない実物（同じ型の操縦室・機関の建物・空港・消防車・中華航空のほかの機体）＝20% の数（この事故の写真）に入れない",
        "- イメージ（Pexels の写真）＝`ep17/stock/` の名・画面の左上に「イメージ」・20% に数えない・git に入れない（焼くときに取り直して md5 を照らす）",
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


# ── 映像（記録映像 V1・フリー素材）：台帳・ショット・使わない窓・USE・ひかえ ──────────────
V1_LOCAL = EPD / "src" / "v1" / "heisei6_bouei_kiroku.mp4"      # YouTube の原本（git の外）＝秒の正本（映像方針・⑤b-1 の境目）
# 🔴 焼くときは Commons の同じ版の 1080p（webm・VP9）を1回 GET して切る（`footage.local_media`＝区間読みは Commons が 429 を返す）。
#    ⑤b-2（10-20）に丸ごと取って YouTube 版と照らした＝**Commons の秒＝YouTube の秒＋0.034秒（1コマ）**（755秒と1000秒の2か所で同じ・
#    8秒＝239コマの平均差 1.66・1.24 ＝次に合うずれの半分以下）＝台帳の `at`
V1_MEDIA = ("https://upload.wikimedia.org/wikipedia/commons/transcoded/9/9d/%E5%B9%B3%E6%88%90%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm/"
            "%E5%B9%B3%E6%88%90%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm.1080p.vp9.webm")
V1_AT = 0.034
V1_PAGE = "https://commons.wikimedia.org/wiki/File:%E5%B9%B3%E6%88%90%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm"
V1_CREDIT = "出典：防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0）・改変：切出・再生速度"
# ショットの表を作る窓（使う区間 c101・c805・c807 と使わない窓のまわり）＝この外の秒を USE に書けば outside_shot が止める（fail closed）
V1_SCAN = (745.0, 800.0)
V1_DIFF_K = 6.0                 # 隣のコマとの差がその窓の中央値の K 倍を超えたら場面の境目（⑤b-1 の 756.70・762.135 を再現する値）
# 映像方針の「使わない」窓（秒＝YouTube 版）＝(秒, 終わり, なぜ)。終わりが None＝その秒を含むショットまるごと（nogo）・
#   数＝そのショットの中の窓（場面が続いたまま中身が替わる所＝⑤b-2 に 1.5秒ごとのコマを原寸〈中身 960 幅〉で見た）
V1_NOGO_AT = [(762.5, None, "12:42.1〜 自衛隊員が集まる寄り（12:44 の運ぶ画の入り口）"),
              *[(float(t), None, "12:45〜12:50 覆われたものの近景") for t in range(765, 771)],
              (771.0, None, "12:51 黄色いシート"),
              # 🔴 ⑤b-2：776.4秒（12:56.4）で隊員2人がしゃがんで何かに手をかける＝777.0・777.5秒は持ち上げる寄り（映像方針の 12:57）＝同じショットの尻
              (776.4, "end", "12:56.4〜 しゃがんで何かを持ち上げる（12:57 の寄りの入り）"),
              # 🔴 ⑤b-2：784.0〜784.4秒にカメラの照明が正面から当たって白飛び（縦の筋つき）＝隣のコマの差が跳んで境目 784.339 が出た（場面は続く）
              (783.9, 784.6, "13:03.9〜13:04.6 照明の白飛び（場面の切り替わりではない）"),
              *[(float(t), None, "13:06〜 使わない（映像方針 §6）") for t in range(786, 793)]]
EDGE_S = 0.10                   # 場面の境目から離す秒（境目のなじみのコマを使わない）


def _film_codes():
    """映像の記号 → 使うカット（一覧の順）"""
    src = _sources()
    out = {}
    for r in _list():
        c = r["code"]
        s = src.get(c, {})
        if s.get("class") in ("video", "stock") and s.get("file", "").lower().endswith((".mp4", ".webm")):
            out.setdefault(c, []).append(r["cid"])
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


def cmd_clips():
    src, fet = _sources(), _fetched()
    out = {}
    for code, cuts in _film_codes().items():
        s = src[code]
        p = HERE / s["file"]
        f = fet.get(code)
        if not f or not p.exists() or md5(p) != f["md5"]:
            raise SystemExit(f"🔴 {code}: 手元の映像が無いか md5 が取得のときと違う（{s['file']}）")
        loc = _probe(p)
        if code == "V1":
            # 🔴 effw（実効の幅）は書かない＝`scene_jiko.foot_box` が額装にする（20本目の型）。17本目は了承② 決め7＝**横いっぱい**
            #    （4:3 の中身 x 250〜1666 を footage.PILLAR で横に満たし、上を残して下を切る＝焼き込みの字幕と日付を外す）
            e = dict(url=V1_PAGE, media=V1_MEDIA, credit=V1_CREDIT, src="mod", at=V1_AT, date="1994-04-26", stock=False,
                     what="平成6年防衛庁記録（中華航空機墜落事故への対応の部分 12:37〜13:12）", w=loc["w"], h=loc["h"], fps=loc["fps"],
                     sar=loc["sar"], sec=round(loc["sec"], 3), size=561682293, dispw=loc["w"], decoded=[loc["w"], loc["h"]],
                     license="CC BY 3.0", rights="CC BY 3.0（防衛省・自衛隊の YouTube 公式・Commons の同じ版＝Commons:YouTube files）",
                     scan=s["file"], md5_scan=f["md5"],
                     note="器 1920x1080・中身は 4:3（x 250〜1666＝⑤b-2 に 757.5・761.5・774・783秒のコマで測った）＝footage.PILLAR 0.7375 で横いっぱい・"
                          "USE の bias 0（上を残す）。焼き込みの字幕は y 825〜985（12:41.5〜＝761.6秒のコマを原寸で見た）・実効は標準画質")
        else:
            lic = LIC[s["rights"]]
            site = "Pixabay" if "Pixabay" in lic else "Pexels"
            e = dict(url=s["page"], media=s["media"], stock=True, file=s["file"].removeprefix("ref/"), credit=f"イメージ（{site}）", src="stock",
                     at=0.0, what=s["note"][:60], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(loc["sec"], 3),
                     size=int(f["bytes"] or 0), md5=f["md5"], dispw=loc["w"], decoded=[loc["w"], loc["h"]],
                     license=lic, license_url=LIC_URL[lic], site=site)
        out[code] = e
        print(f"  {code:6} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:8.2f}秒  {' '.join(cuts):16} {e['credit']}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep17/clips.json（{len(out)}本）")
    return 0


def _v1_cuts():
    """V1 の V1_SCAN の窓をコマごとに読み、隣のコマとの差（中身 x 250〜1666・下の字幕の帯 y 800〜 を除く・160×90 の灰色）で場面の境目を測る。
    戻り＝境目の秒の並び（YouTube 版の秒・境目の後ろ側のコマの頭）"""
    import numpy as np
    a0, a1 = V1_SCAN
    W, H = 160, 90
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a0:.3f}", "-i", str(V1_LOCAL), "-t", f"{a1 - a0:.3f}",
                        "-vf", f"crop=1416:800:250:0,scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True, timeout=900)
    raw = r.stdout
    n = len(raw) // (W * H)
    fr = np.frombuffer(raw[:n * W * H], np.uint8).reshape(n, H, W).astype(np.float32)
    fps = 30000 / 1001
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    thr = float(np.median(d)) * V1_DIFF_K
    cuts = [round(a0 + (i + 1) / fps, 3) for i in np.where(d > thr)[0]]
    # 続く2コマ以上の跳び（ディゾルブ・揺れ）は最初の1つに畳む
    out = []
    for t in cuts:
        if out and t - out[-1] < 0.2:
            continue
        out.append(t)
    return out, thr, n


def cmd_shots():
    """shots.json＝V1 は V1_SCAN の窓をコマごと（場面の境目＝_v1_cuts）・フリー素材は tools/shots.shots_of（1秒1コマ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import shots as SH
    src = _sources()
    out = {}
    for code in _film_codes():
        s = src[code]
        if code == "V1":
            cuts, thr, n = _v1_cuts()
            edges = [V1_SCAN[0]] + cuts + [V1_SCAN[1]]
            sh = [dict(start=round(edges[i], 3), until=round(edges[i + 1], 3), motion=0.0) for i in range(len(edges) - 1)]
            out[code] = dict(src=V1_MEDIA, scan=s["file"], dur=1254.286,
                             how=f"⑤b-2（10-20）：{V1_SCAN[0]:g}〜{V1_SCAN[1]:g}秒をコマごと（{n}コマ）・隣のコマとの差がその窓の中央値の {V1_DIFF_K:g}倍"
                                 f"（{thr:.2f}）を超えた所＝境目（中身 x 250〜1666・字幕の帯 y 800〜 を除く）。この窓の外は表に無い＝USE に書けば止まる",
                             shots=sh)
            print(f"  V1  {V1_SCAN[0]:g}〜{V1_SCAN[1]:g}秒 {n}コマ  境目 {len(cuts)}：" + " ".join(f"{t:.3f}" for t in cuts))
            continue
        sh, dur = SH.shots_of(HERE / s["file"])
        out[code] = dict(src=s["media"], scan=s["file"], dur=round(dur, 1), how="1秒1コマで tools/shots.shots_of（2026-10-20 ⑤b-2・フリー素材）",
                         shots=sh)
        print(f"  {code:6} {dur:6.1f}秒  ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep17/shots.json（{len(out)}本）")
    return 0


def _write_block(tag, lines):
    txt = FOOTAGE.read_text(encoding="utf-8")
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_text(txt[:m.start(2)] + "".join(x + "\n" for x in lines) + txt[m.end(2):], encoding="utf-8")


def cmd_nogo():
    """footage.NOGO の V1 の欄＝映像方針の「使わない」秒を含むショットまるごと（重なりは1つにまとめる）"""
    sh = json.loads(SHOTS.read_text(encoding="utf-8"))["V1"]["shots"]
    win = {}
    for t, t1, why in V1_NOGO_AT:
        s = [x for x in sh if x["start"] <= t < x["until"]]
        if len(s) != 1:
            raise SystemExit(f"🔴 V1 {t}秒：ショットが {len(s)} 本（表の窓 {V1_SCAN} の外か境目が重なる）")
        k = ((s[0]["start"], s[0]["until"]) if t1 is None else (t, s[0]["until"]) if t1 == "end" else (t, float(t1)))
        win.setdefault(k, [])
        if why not in win[k]:
            win[k].append(why)
    items = [f'({a:.3f}, {b:.3f}, "{"／".join(w)}")' for (a, b), w in sorted(win.items())]
    _write_block("EP17_NOGO", ['    "V1": [' + ",\n           ".join(items) + "],"])
    print(f"→ tools/footage.py NOGO（V1 {len(items)}窓）")
    for x in items:
        print("  ", x)
    return 0


# 寄りと寄せ（V1＝横いっぱいは footage.PILLAR・ここでは字幕の帯から逃がす寄りの足しと上寄せ）
V1_GEOM = dict(zoom=1.04, bias=0.0)       # zoom_of＝1.04÷0.7375＝1.41（見える縦 766px＜字幕の上の端 825）
# 🆕 ⑤b-7（10-21）：V1 の区間を一覧の動きの欄から変えたカット＝{cid: (始め, 終わり, 理由)}（YouTube 版の秒）
V1_WINDOW = {
    "c805": (771.99, 776.30, "ショット 771.894〜777.733 の頭から、使わない窓 776.4〜（しゃがんで持ち上げる）の手前まで＝⑤b-2 の申し送り「776.3 まで」"),
    # c807：ショット 777.733〜784.339 は背広の人（役目が分からない）が 780.6〜781.6秒ごろ左から入り、783.9〜 は照明の白飛び（使わない窓）。
    #   人を避けて 0.6倍以上で足りる区間が無い（777.83〜780.2＝2.4秒／要る 6.55秒）＝778.0秒のコマの止め絵（⑤b-7 に 778〜783.4秒を約1秒おきに見た）
    "c807": (778.00, 779.00, "止め絵＝778.0秒のコマ（背広の人が入る 780.6秒より前・救助の人は顔が分からない）", "still"),
}
# 🆕 ⑤b-7：フリー素材の映像（23本目の型）。STOCK_WINDOW＝pick を使わずに決めた区間・STOCK_GEOM＝寄りと寄せ（字を外す）
STOCK_WINDOW = {}
STOCK_GEOM = {}
STOCK_EDGE = 0.3                # ショットの境目から離す秒（フリー素材＝1秒1コマで測った境目＝23本目と同じ）


def cmd_use(all_=False):
    """footage.USE の17本目の欄（🔴 章ファイルに `ss.vid`（カットまるごと）か `ss.head`（頭の差し込み）を書いたカットだけ＝門番 slots は両側を見る）。
    V1＝一覧の動きの欄の区間（YouTube 版の秒）を、その区間を含むショットの境目から EDGE_S 離して切り、rate＝使える秒÷要る秒（切り捨て）
    🆕 ⑤b-7（10-21）：`use --all`＝章ファイルに書く前に、一覧の映像のカットを全部書く（`ss.vid` は USE の欄が無いと章ファイルの読み込みで
    ひかえを開けずに止まる＝鶏と卵）。書いたあと章ファイルに `ss.vid` を足して、ふつうの `use` で同じ行になるかを見る"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    import scene_jiko as S
    secs = FO.secs_of()
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    lines, skip = [], []
    for r in _list():
        if r["code"] not in _film_codes():
            continue
        cid, code = r["cid"], r["code"]
        sp = S.SPEC.get(cid) or {}
        head = bool((sp.get("intro") or {}).get("foot"))
        if not head and not all_ and not str(sp.get("photo") or "").endswith(f"fb_{cid}.jpg"):
            skip.append(cid)
            continue
        if code != "V1":
            # 🆕 ⑤b-7（10-21）：フリー素材の映像（23本目の pick の型）＝要る秒が等速で入るショットのうち、いちばん長いショットの真ん中。
            #   入らなければいちばん長いショットで倍率を下げる（0.6 未満は止める）。STOCK_WINDOW に書いたカットはその区間（字を外す・絵を選ぶ）
            need = float(secs[cid])
            shs = sd[code]["shots"]
            if cid in STOCK_WINDOW:
                a, b = STOCK_WINDOW[cid]
                sh = [x for x in shs if x["start"] <= a < x["until"]][0]
                rate = min(1.0, int((b - a) / need * 100) / 100)
            else:
                sh = max(shs, key=lambda x: x["until"] - x["start"])
                room = sh["until"] - sh["start"] - 2 * STOCK_EDGE
                if room >= need:
                    a = round(sh["start"] + STOCK_EDGE + (room - need) / 2, 2)
                    b, rate = round(a + need + 0.05, 2), 1.0
                else:
                    a, b = round(sh["start"] + STOCK_EDGE, 2), round(sh["until"] - STOCK_EDGE, 2)
                    rate = min(1.0, int(room / need * 100) / 100)
            if rate < STILL_BELOW:
                raise SystemExit(f"🔴 {cid}: 使える {b - a:.2f}秒／要る {need:.2f}秒＝{rate}＜{STILL_BELOW}（止め絵になる）")
            geo = "".join(f", {k}={v}" for k, v in STOCK_GEOM.get(cid, {}).items())
            lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate={rate}{geo}),   '
                         f'# ショット {sh["start"]:g}〜{sh["until"]:g}秒・使える {b - a:.2f}秒／要る {need:.2f}秒（フリー素材）')
            continue
        m = re.search(r"映像（(\d+(?:\.\d+)?)〜(\d+(?:\.\d+)?)秒", r["motion"])
        a, b = float(m.group(1)), float(m.group(2))
        sh = [x for x in sd["V1"]["shots"] if x["start"] <= (a + b) / 2 < x["until"]][0]
        a, b = max(a, sh["start"] + EDGE_S), min(b, sh["until"] - EDGE_S)
        if cid in V1_WINDOW:
            a, b = V1_WINDOW[cid][:2]          # 🆕 ⑤b-7：使わない窓・人の顔を避けた区間（理由は表の3つ目）
            if V1_WINDOW[cid][3:] == ("still",):
                geo = "".join(f", {k}={v}" for k, v in V1_GEOM.items())
                lines.append(f'    "{cid}": dict(clip="V1", start={a:.2f}, still=True, until={b:.2f}{geo}),   '
                             f'# ショット {sh["start"]:.3f}〜{sh["until"]:.3f}秒・{V1_WINDOW[cid][2]}')
                continue
        # 頭の差し込みは差し込みが画面に出る秒（scene_jiko.head_secs）＝USE にまだ head が無いあいだ footage.secs_of はカットの尺を返す
        need = float(S.head_secs(cid) if head else secs[cid])
        rate = min(1.0, int((b - a) / need * 100) / 100)
        if rate < STILL_BELOW:
            raise SystemExit(f"🔴 {cid}: 使える {b - a:.2f}秒／要る {need:.2f}秒＝{rate}＜{STILL_BELOW}（止め絵になる）")
        geo = "".join(f", {k}={v}" for k, v in V1_GEOM.items())
        lines.append(f'    "{cid}": dict(clip="V1", start={a:.2f}, until={b:.2f}, rate={rate}{geo}{", head=True" if head else ""}),   '
                     f'# ショット {sh["start"]:.3f}〜{sh["until"]:.3f}秒・使える {b - a:.2f}秒／要る {need:.2f}秒{"（頭の差し込み）" if head else ""}')
    _write_block("EP17_USE", lines)
    print(f"→ tools/footage.py USE {len(lines)}欄")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない（⑤b-7）：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）＝USE の start の1コマ（YouTube 版）を器のまま 1920×1080
    （焼くときと同じ fit が PILLAR・zoom・bias で切る＝コマと同じ幾何）。記録映像は ref/ep17/fb_<cid>.jpg（git に入れる・CC BY 3.0 の1コマ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    bad = 0
    from PIL import Image
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
        if u["clip"] != "V1":
            # 🆕 ⑤b-7：フリー素材＝区間の頭の1コマを焼くときと同じ切り口（全画面・寄り）で 1920×1080 → ref/ep17/stock/fb_<cid>.jpg（git に入れない）
            c = FO.CLIPS.get(u["clip"]) or {}
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
            l, t = (sw - cw) * float(u.get("xbias", 0.5)), (sh_ - ch) * float(u.get("bias", 0.5))
            im = im.crop((round(l), round(t), round(l + cw), round(t + ch))).resize((1920, 1080), Image.LANCZOS)
            dst = EPD / "stock" / f"fb_{cid}.jpg"
            im.save(dst, quality=92)
            print(f"✓ {cid:5} {u['clip']:5} {float(u['start']):6.2f}秒 {sw}x{sh_} → {dst.relative_to(HERE).as_posix()}")
            continue
        dst = EPD / f"fb_{cid}.jpg"
        r = subprocess.run(["ffmpeg", "-y", "-nostdin", "-v", "error", "-ss", f"{float(u['start']):.3f}", "-i", str(V1_LOCAL),
                            "-frames:v", "1", "-q:v", "2", str(dst)], capture_output=True, text=True)
        if r.returncode or not dst.exists():
            print(f"🔴 {cid}: ひかえの静止画が作れない（{r.stderr[-160:]}）")
            bad += 1
            continue
        print(f"✓ {cid:5} V1 {float(u['start']):7.2f}秒 → {dst.relative_to(HERE).as_posix()}（器 1920x1080 のまま）")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "edges": cmd_edges, "clips": cmd_clips, "shots": cmd_shots, "nogo": cmd_nogo,
            "use": lambda: cmd_use("--all" in sys.argv)}
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "look":
        sys.exit(cmd_look(a[1:]))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
