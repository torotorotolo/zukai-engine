# -*- coding: utf-8 -*-
"""ep25_assets.py — 25本目（JR福知山線脱線事故）の写真・頁の束（⑤b-2・2026-10-25）。24本目 `ep24_assets.py` の形を、25本目の台帳
（`sources25.psv` の13列〈見出しの行で読む〉・`fetch25.tsv`・git の外の作者の表 `credits_private.tsv`〈列 source・no・title・license・author・…〉）に合わせた。

取得はすんでいる（映像方針＝了承②・`ref/ep25/eizou_build/fetch25.py`・記録 `fetch25.tsv`＝md5 2回）。ここは**束を作る道**だけを持つ。
  python qa_out/ep25_assets.py build             # 写真・頁の束 ref/ep25/<名>.jpg ＋ 権利の台帳 ref/ep25/assets.json
  python qa_out/ep25_assets.py look F12 …        # 束の写真を並べた見本（out/ep25_look/・1枚 960 幅）＝選ぶとき・確かめるとき（記号か束の名）
  python qa_out/ep25_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python qa_out/ep25_assets.py edges             # 束の四辺の暗い帯（スライドの台紙の縁）＝門番 check_photo_edge の名簿を決める
  python qa_out/ep25_assets.py credits [--write] # 画面の出典 ref/ep25/credits.json と ref/CREDITS.md の25本目の節
  python qa_out/ep25_assets.py pbox P-R1-222 "事故現場の右曲線" "低いものと考えられる"   # 頁の字の層の行から切り口（束の割合）を測る
  python qa_out/ep25_assets.py names [<画像かフォルダ> …]   # 🆕 名前の門番＝絵の OCR × git の外の名前の表（既定＝束の頁の全部）
  python qa_out/ep25_assets.py names --selftest  # 陽性対照＝名前の載る頁をまるごと描いて OCR が名前を拾うか
  python qa_out/ep25_assets.py clips｜shots｜frames X-…｜use [c… ]｜fb [c… ]   # フリー素材（Pexels）＝⑤b-3 で初めて回す（24本目の形のまま）

入力＝映像方針の一覧 `ref/ep25/eizou_build/list25.tsv`（生成物・秒は narration.json の実測＝⑤b-1）・出どころ `sources25.psv`（区切り「|」）・
取得の記録 `fetch25.tsv`（地理院の3点は `src/gsi/gsi_log.txt`＝md5 なし＝束の台帳に元の md5 を書く）。元は `ref/ep25/src/`（git の外）。
🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色・了承②）＝幅 2400 か高さ 1350 の大きい方まで（報告書の小さい写真は縮まない＝原画のまま）。
🔴 頁は PDF から長辺 3600px で描き直す（fetch25 の 200dpi の PNG は下見用＝寄りで字を読める大きさを残す・24本目と同じ）。
🔴 **人は役職だけ（①の承認）**＝名前の載る頁（K05 p.1・R1 PDF2・S2 p.1・S1 p.50・p.53）は**束の段で名前の外を切り出す**（表 PAGE_CROP）
   ＝公開リポの束にも動画の絵にも名前が出ない。切り口は字の層の行（名前の字の箱が切り口に入れば止める）・S1 p.53 は判断の一文が名前の行と
   同じ行にまたがる＝姓の字だけ升目（役職の「社長」「委員」は残す）。門番＝`names`（絵の OCR × git の外の名前の表 `src/names_private.txt`）。
🔴 **個人名義の Commons の点（CC BY 3.0 の C3）は、画面の出典の行に作者欄の名前を出すが、名前は公開リポに書かない**（17・23・24本目の型）
   ＝credits.json の行は印 `{作者}` だけ・焼くときに `scene_jiko.ep25_credit` が git の外の表の `commons 3` の行から足す。CC0 は名前を出さない。
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
EPD = HERE / "ref" / "ep25"
SRC = EPD / "src"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list25.tsv"
SOURCES = BUILD / "sources25.psv"
FETCH = BUILD / "fetch25.tsv"
GSI_LOG = SRC / "gsi" / "gsi_log.txt"
PRIVATE = SRC / "credits_private.tsv"      # 🔴 git の外（作者欄）＝ここから名前を公開の物へ写さない
NAMES = SRC / "names_private.txt"          # 🔴 git の外（出さない名前）
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
FOOTAGE = HERE / "tools" / "footage.py"
SCRATCH = HERE / "out" / "ep25_look"           # look・frames・names の陽性対照の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## JR福知山線脱線事故（2005-04-25・25本目）"
AUTHOR = "{作者}"            # 個人名義の点の画面の出典の行の印（焼くときに git の外の表から足す＝scene_jiko.ep25_credit）
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（footage.py の注）
EVENT_YEAR = 2005            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）
UA = "zukai-engine/1.0 (ep25 visual plan research)"

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
PAGE_LONG = 3600                       # 頁は長辺 3600 で描く（寄りで字を読める大きさを残す＝17・24本目と同じ）
CLIP_DPI = 400                         # 頁の一部（clip:＝報告書の写真の説明の字ごと）は 400dpi（fetch25 の2倍・長辺は PAGE_LONG まで）
JPEG_Q = 92
MOSAIC_PX = 14                         # 升目の大きさ（束の画素）
PHOTO_TYPES = ("report-photo", "mlit-photo", "commons", "gsi")
PAGE_TYPES = ("report-page", "mlit-page", "court-page")
OTHER_TYPES = ("google", "stock")      # 束に入れない（衛星写真＝ss.SAT・フリー素材＝clips.json）
NO_NAME = ("CC0",)                     # 表示が任意＝作者の名前を出さない
NAMED = ("C3",)                        # 画面の出典の行に作者の名前を出す点（CC BY 3.0＝了承② 決め4「作者名と許諾」）
# PDF の名 → src からの道（fetch25.py の pdf_path と同じ）
PDFS = {"RA2007-3-1_cover": "jtsb/RA2007-3-1_cover.pdf", "fu04-finalreport": "jtsb/fu04-finalreport.pdf",
        "fu04-finalreport-annex-2-2": "jtsb/fu04-finalreport-annex-2-2.pdf", "iken20070201-an01-honbun": "jtsb/iken20070201-an01-honbun.pdf",
        "kengi_170906k": "jtsb/kengi_170906k.pdf", "hanrei-pdf-82178": "courts/hanrei-pdf-82178.pdf", "hanrei-pdf-86834": "courts/hanrei-pdf-86834.pdf"}
# 頁の資料の年（副題の年と照らす）＝PDF の名の頭で（sources.md の資料の表）
DOC_YEAR = {"RA07-3-1-": (2007, "鉄道事故調査報告書 RA2007-3（2007年6月28日）"), "RA2007-3-1_cover": (2007, "鉄道事故調査報告書 RA2007-3 の表紙（2007年6月28日）"),
            "fu04-finalreport": (2011, "検証報告書（2011年4月15日）"), "kengi_170906k": (2005, "建議 国空委第15号（2005年9月6日）"),
            "iken20070201-an01-honbun": (2006, "意見聴取会用「事実調査に関する報告書の案」（2006年12月20日の表紙）"),
            "hanrei-pdf-82178": (2012, "神戸地裁の判決（2012年1月）"), "hanrei-pdf-86834": (2017, "最高裁 第二小法廷の決定（2017年6月12日）"),
            "mlit2005/": (2005, "国土交通省の発表（2005年・事故のあと）")}

# 🔴 名前の載る頁＝束の段で名前の外を切り出す {記号: dict(head, tail, why, mosaic)}。head〜tail＝字の層の行（その行を含む・上下は行と行のすき間の真ん中）。
#   ⑤b-2（10-25）に字の層の行と名前の字の箱（scratchpad の namepos25）を見て決めた。mosaic＝切り口の中の名前の字を升目にする（役職の字は残す）
PAGE_CROP = {
    # c805（寄る＝ATS の項へ）＝頁の頭の宛先「国土交通大臣」と差出の「委員長」の行に名前（y 0.23・0.30）＝建議の題の行から下
    "P-K05-1": dict(head="福知山線列車脱線事故に係る建議について", tail="機能向上を図るべきである",
                    why="頁の頭の宛先と差出の行（大臣と委員長の名前）を外す"),
    # c910（寄る＝主文へ）＝理由の1行目に指定弁護士3人の名前（y 0.31）＝事件の番号の行から主文まで
    "P-S2-1": dict(head="業務上過失致死傷被告事件", tail="本件各上告を棄却する",
                   why="理由の1行目（指定弁護士の名前）から下を外す"),
    # c919（寄る＝断り書きへ）＝下の差出「委員長」の行に名前（y 0.67）＝断り書きの段落だけ
    "P-R1-002": dict(head="本報告書の調査は", tail="責任を問うために行われたものではない",
                     why="下の差出の行（委員長の名前）を外す"),
    # ca14（寄る＝要請の中身へ）＝本文に社長と委員の姓が16か所＝要請の中身の4行（名前の無い行だけ・y 0.54〜0.62）
    "P-S1-50": dict(head="線速照機能の整備は優先的に", tail="というものであった",
                    why="社長と委員の姓の無い4行（要請の中身）だけ"),
    # ca19（寄る）＝判断の一文「…影響はなかったと判断する」が姓の入る行にまたがる（名前の外だけでは文が切れる）
    #   ＝評価の段落の頭の4行を切り出し、姓の字だけ升目（「社長」「委員」は残す＝役職だけ）
    "P-S1-53": dict(head="審議音声を確認した結果", tail="審議音声やヒアリング結果を総合すると", mosaic=True,
                    why="評価の段落の頭の4行・姓の字だけ升目（判断の一文が姓の入る行にまたがる）"),
}
# 撮影年の手当て {記号: (年 か None, 出どころ)}＝決まりの読みで決まらない点
YEAR_FIX = {
    "P-F47": (2003, "報告書の付図47＝2003年9月の会社の会議の資料の写し（副題の年＝資料の中身の年）"),
    "P-F48": (2003, "報告書の付図48＝2003年9月の会社の会議の資料の写し（副題の年＝資料の中身の年）"),
    "C12": (2025, "Commons の日付の欄 2025-04-30・分類 2025-04-25（sources25.psv の注＝②③ に Commons の頁で読んだ）"),
    "Msikensoukou": (None, "国交省の頁の現車走行試験の資料＝撮影の日の記載を読んでいない"),
}
# 顔だけ升目 {記号: [(x0, y0, x1, y1, 誰)]}（束の画素）。⑤b-2（10-25）に原寸の2倍と目盛りで見て決めた（scratchpad の c10_people_2x）
#   C10（cb04・CC0・報道の人たち＝私人）＝**元の写真で投稿者が顔をぼかしてある**が、横顔と輪郭が残る＝了承② 決め2「顔が見えたら顔だけ」で
#   こちらを向く人・横顔の人の頭7か所。背中だけの2人（帽子の人・台の上でカメラを覗く人）と遠くの通行人（顔 10px 未満）は升目にしない
#   C13（2012年・踏切の向こうの自転車の人＝顔 10px 未満）・C3（自転車の人の後ろ姿）・Msikensoukou（人なし）は升目にしない
MASK = {"C10": [(100, 648, 138, 688, "左の台の上でカメラの横に立つ人"), (310, 770, 350, 815, "ノートを開く人"),
                (355, 930, 392, 968, "かがむ人"), (533, 788, 572, 828, "真ん中の人"), (600, 790, 632, 828, "脚立の横の人"),
                (654, 783, 702, 834, "奥の2人"), (1646, 796, 1682, 840, "右の電柱の横の人")]}
MASKED_BEFORE = {"C10": "元の写真で投稿者が顔をぼかしてある（Commons の版）"}


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
    if head != ["code", "type", "title", "page", "get", "dims", "rights", "basis", "credit", "era", "people", "file", "note"]:
        raise SystemExit(f"🔴 sources25.psv の見出しの行が変わった：{rows[0][:120]}")
    out = {}
    for ln in rows[1:]:
        f = ln.split("|")
        if len(f) != 13:
            raise SystemExit(f"🔴 sources25.psv の行の欄が13でない：{ln[:80]}")
        out[f[0]] = dict(zip(head, f))
    return out


def _fetched():
    """{記号: [行, …]}（同じ記号が2行ある点＝Msikensoukou）"""
    out = {}
    for ln in FETCH.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if ln.startswith("#") or len(f) < 8 or f[1] == "code":
            continue
        out.setdefault(f[1], []).append(dict(zip(["time", "code", "how", "file", "px", "bytes", "md5", "source"], f)))
    return out


def _private():
    """git の外の表 {(source, no): {列: 値}}。無ければ止める（束を作る手元だけで読む）"""
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の作者欄の表）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r]
    head = rows[0]
    return {(r[0], r[1]): dict(zip(head, r)) for r in rows[1:] if len(r) >= 2}


def _names():
    """git の外の出さない名前（NFKC・空白なし・2字以上）。無ければ止める（fail closed）"""
    if not NAMES.exists():
        raise SystemExit(f"🔴 {NAMES.relative_to(HERE).as_posix()} が無い（git の外の名前の表）")
    out = []
    for ln in NAMES.read_text(encoding="utf-8").splitlines():
        n = _norm(ln)
        if n and not ln.startswith("#") and len(n) >= 2:
            out.append(n)
    if not out:
        raise SystemExit("🔴 名前の表が空（fail closed）")
    return sorted(set(out), key=len, reverse=True)


def _norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s or ""))


def _mask_word(w):
    return w[0] + "○" * (len(w) - 1)


def uses():
    """{記号: [カット]}（一覧の素材の欄から・束に入る写真と頁だけ）。種類と出どころの型が食い違えば止める"""
    src = _sources()
    out, bad = {}, []
    for r in _list():
        c = r["code"]
        s = src.get(c)
        if not s or s["type"] in OTHER_TYPES:
            continue
        if s["type"] in PAGE_TYPES and r["kind"] != "頁" or s["type"] in PHOTO_TYPES and r["kind"] != "実写":
            bad.append(f"{r['cid']} {c}: 一覧の種類「{r['kind']}」と出どころの型 {s['type']} が食い違う")
        if s["type"] not in PAGE_TYPES + PHOTO_TYPES:
            bad.append(f"{r['cid']} {c}: 出どころの型 {s['type']} を束の道が知らない")
        out.setdefault(c, []).append(r["cid"])
    if bad:
        raise SystemExit("🔴 " + "\n🔴 ".join(bad))
    return out


def bundle_name(code):
    return code.lower().replace("-", "_")


# ── 頁 ─────────────────────────────────────────────────────────
def pdf_path(name):
    if name in PDFS:
        return SRC / PDFS[name]
    if name.startswith("mlit2005/"):
        return SRC / name
    return SRC / "jtsb" / f"{name}.pdf"


def _page_ref(s):
    """出どころの get → (PDF の名, 頁, clip の矩形 pt か None)"""
    g = s["get"]
    parts = g.split(":")
    if g.startswith("page:"):
        return ":".join(parts[1:-1]), int(parts[-1]), None
    if g.startswith("clip:"):
        return parts[1], int(parts[2]), tuple(float(v) for v in parts[3].split(","))
    raise SystemExit(f"🔴 {s['code']}: 頁の get が page: か clip: でない（{g}）")


def doc_year(name):
    for k, v in DOC_YEAR.items():
        if name.startswith(k):
            return v
    raise SystemExit(f"🔴 頁の資料の年が表 DOC_YEAR に無い（{name}）")


def _lines(pg):
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            t = "".join(s["text"] for s in ln["spans"]).strip()
            if t:
                out.append((t, ln["bbox"]))
    return out


def name_boxes(pg, names):
    """頁の字の層で、出さない名前の字の箱（pt）＝[(名前の頭1字＋○, (x0, y0, x1, y1)), …]。行をまたぐ名前は字ごとの箱を全部返す"""
    chars = []
    for b in pg.get_text("rawdict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln["spans"]:
                for c in sp["chars"]:
                    t = unicodedata.normalize("NFKC", c["c"])
                    if t.strip():
                        chars.append((t, c["bbox"]))
    txt = "".join(c for c, _ in chars)
    out = []
    for n in names:
        for m in re.finditer(re.escape(n), txt):
            for i in range(m.start(), m.end()):
                out.append((_mask_word(n), tuple(chars[i][1])))
    return out


def _crop_box_pt(pg, spec, code):
    """PAGE_CROP の head〜tail の行の箱（pt）。上下は前後の行とのすき間の真ん中・左右は選んだ行の外接＋8pt"""
    lines = _lines(pg)
    i0 = next((i for i, (t, _) in enumerate(lines) if spec["head"] in t), None)
    if i0 is None:
        raise SystemExit(f"🔴 {code}: 「{spec['head']}」の行が字の層に無い")
    i1 = next((i for i in range(i0, len(lines)) if spec["tail"] in lines[i][0]), None)
    if i1 is None:
        raise SystemExit(f"🔴 {code}: 「{spec['head']}」より後に「{spec['tail']}」の行が無い")
    sel = [b for _, b in lines[i0:i1 + 1]]
    x0, x1 = min(b[0] for b in sel), max(b[2] for b in sel)
    top, bot = min(b[1] for b in sel), max(b[3] for b in sel)
    over = [b for _, b in lines if b[0] < x1 and b[2] > x0 and b not in sel]
    above = [b[3] for b in over if b[3] <= top + 1]
    below = [b[1] for b in over if b[1] >= bot - 1]
    # 前後の行が遠い（白い余白が広い）ときは 12pt まで（束の絵に白い帯を作らない）
    yt = max((max(above) + top) / 2, top - 12) if above else top - 8
    yb = min((min(below) + bot) / 2, bot + 12) if below else bot + 8
    return (max(0, x0 - 8), max(0, yt), min(pg.rect.width, x1 + 8), min(pg.rect.height, yb)), lines[i0][0], lines[i1][0]


def render_page(code, s, names):
    """頁を描く＝(RGB の PIL 画像, 記録の dict, 升目にした名前の数)。名前の字の箱が束の絵に入れば止める（升目にした分を除く）"""
    import fitz
    import numpy as np
    from PIL import Image
    name, no, clip = _page_ref(s)
    pdf = pdf_path(name)
    if not pdf.exists():
        raise SystemExit(f"🔴 {code}: PDF {pdf.relative_to(HERE).as_posix()} が無い")
    pg = fitz.open(pdf)[no - 1]
    nb = name_boxes(pg, names)
    rec0 = dict(pdf=pdf.relative_to(HERE).as_posix(), pdf_page=no, pdf_md5=md5(pdf))
    crop = PAGE_CROP.get(code)
    if clip:
        r = fitz.Rect(*clip)
        k = min(CLIP_DPI / 72, PAGE_LONG / max(r.width, r.height))
        pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), clip=r, alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        region = (r.x0, r.y0, r.x1, r.y1)
        rec = dict(rec0, scale=round(k, 5), clip_pt=[round(v, 2) for v in clip], box_px=[0, 0, pix.width, pix.height],
                   how=f"PDF の頁の一部（clip・{k * 72:.0f}dpi）")
    else:
        k = PAGE_LONG / max(pg.rect.width, pg.rect.height)
        pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if crop:
            bpt, _l0, _l1 = _crop_box_pt(pg, crop, code)
            box = tuple(int(round(v * k)) for v in bpt)
            # ⚠️ 行の字を記録に写さない（S1 p.53 の行には姓が入る＝台帳 assets.json は公開リポ）＝目印の語（PAGE_CROP の head・tail）だけ
            how = f"PDF の頁を描いた（長辺 {PAGE_LONG}px）・🔴 名前の外を切り出し（{crop['why']}）＝字の層の行「{crop['head']}」〜「{crop['tail']}」"
        else:
            a = np.asarray(im.convert("L"))
            h, w = a.shape
            m = int(min(h, w) * 0.01)               # 走査の縁の影（端の 1% の暗い帯）は外接に入れない
            ys, xs = np.where(a[m:h - m, m:w - m] < 160)
            box = (max(0, xs.min() + m - 24), max(0, ys.min() + m - 24), min(w, xs.max() + m + 24), min(h, ys.max() + m + 24))
            how = f"PDF の頁を描いた（長辺 {PAGE_LONG}px）・インクの外接"
        region = tuple(v / k for v in box)
        im = im.crop(box)
        rec = dict(rec0, scale=round(k, 5), box_px=[int(v) for v in box], how=how)
    # 名前の字の箱が束の絵（region＝pt）に入るか
    inside = [(w_, b) for w_, b in nb if b[0] < region[2] and b[2] > region[0] and b[1] < region[3] and b[3] > region[1]]
    nmos = 0
    if inside and crop and crop.get("mosaic"):
        from PIL import Image as _I
        for _w, b in inside:
            x0, y0 = int((b[0] - region[0]) * k) - 4, int((b[1] - region[1]) * k) - 4
            x1, y1 = int((b[2] - region[0]) * k) + 4, int((b[3] - region[1]) * k) + 4
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(im.width, x1), min(im.height, y1)
            reg = im.crop((x0, y0, x1, y1))
            small = reg.resize((max(1, reg.width // MOSAIC_PX), max(1, reg.height // MOSAIC_PX)), _I.BOX)
            im.paste(small.resize(reg.size, _I.NEAREST), (x0, y0))
            nmos += 1
        rec["how"] += f"・姓の字 {nmos}字を升目（升 {MOSAIC_PX}px・役職の字は残す）"
    elif inside:
        raise SystemExit(f"🔴 {code}: 束の絵に出さない名前の字が入る（{sorted({w_ for w_, _ in inside})}）＝PAGE_CROP で外す")
    return im, rec, nmos


def cmd_pbox(code, head, tail, pad=18):
    """頁の字の層で、head を含む最初の行から tail を含む行までの箱＝束の絵の割合 (x0, y0, x1, y1)。章ファイルの trim に写す値
    （24本目と同じ＝上下の辺は束の絵の OCR〈ocr_slides.json〉の行のすき間でインクのいちばん少ない行）"""
    import fitz
    import numpy as np
    from PIL import Image
    db = json.loads(DB.read_text(encoding="utf-8"))
    name = next((n for n, r in db.items() if r["code"] == code), None)
    rec = db.get(name) if name else None
    if not rec or "src_rec" not in rec:
        raise SystemExit(f"🔴 {code} は束に頁として無い（build を先に）")
    sr = rec["src_rec"]
    pg = fitz.open(HERE / sr["pdf"])[sr["pdf_page"] - 1]
    lines = _lines(pg)
    i0 = next((i for i, (t, _) in enumerate(lines) if head in t), None)
    if i0 is None:
        raise SystemExit(f"🔴 {code}: 「{head}」の行が無い")
    i1 = next((i for i in range(i0, len(lines)) if tail in lines[i][0]), None)
    if i1 is None:
        raise SystemExit(f"🔴 {code}: 「{head}」より後に「{tail}」の行が無い")
    sel = lines[i0:i1 + 1]
    k, (bx, by, _, _) = sr["scale"], sr["box_px"]
    ox, oy = (sr["clip_pt"][0], sr["clip_pt"][1]) if sr.get("clip_pt") else (0.0, 0.0)
    sx0, sx1 = min(b[0] for _, b in sel), max(b[2] for _, b in sel)
    top, bot = min(b[1] for _, b in sel), max(b[3] for _, b in sel)
    over = [b for _, b in lines if b[0] < sx1 and b[2] > sx0]
    above = [b[3] for b in over if b[3] <= top + 1 and b[1] < top - 1]
    below = [b[1] for b in over if b[1] >= bot - 1 and b[3] > bot + 1]
    yt = (max(above) + top) / 2 if above else top - pad / k
    yb = (min(below) + bot) / 2 if below else bot + pad / k
    x0, x1 = (sx0 - ox) * k - bx - pad, (sx1 - ox) * k - bx + pad
    y0, y1 = (yt - oy) * k - by, (yb - oy) * k - by
    w, h = rec["w"], rec["h"]
    box = [max(0.0, x0 / w), max(0.0, y0 / h), min(1.0, x1 / w), min(1.0, y1 / h)]
    print(f"{code}: 行 {i0}〜{i1}（{len(sel)}行）「{sel[0][0][:30]}」〜「{sel[-1][0][-30:]}」")
    o = (json.loads((EPD / "ocr_slides.json").read_text(encoding="utf-8")).get(f"{name}.jpg")
         if (EPD / "ocr_slides.json").exists() else None)
    if not o:
        print(f"  trim=({box[0]:.3f}, {box[1]:.3f}, {box[2]:.3f}, {box[3]:.3f})（字の層だけ）")
        print("  🔴 OCR の読み置きが無い＝絵の行で寄せ直せない（`python tools/check_slide.py --ocr` のあとでもう一度）")
        return 1
    ow, oh = o["size"]
    L, R = box[0] * ow, box[2] * ow
    rows = sorted(ln["box"] for ln in o["lines"] if ln["box"][0] < R and ln["box"][2] > L)
    inside = [b for b in rows if box[1] * oh <= (b[1] + b[3]) / 2 <= box[3] * oh]
    if not inside:
        print("  🔴 切り口の中に OCR の行が無い")
        return 1
    t_o, b_o = min(b[1] for b in inside), max(b[3] for b in inside)
    prev = [b[3] for b in rows if b[3] <= t_o and b not in inside]
    nxt = [b[1] for b in rows if b[1] >= b_o and b not in inside]
    ink = (np.asarray(Image.open(EPD / f"{name}.jpg").convert("L"))[:, int(L):int(R)] < 160).sum(axis=1)

    def calm(a, b):
        a, b = int(a), int(b)
        if b <= a:
            return (a + b) / 2
        seg = ink[a:b + 1]
        idx = np.where(seg == seg.min())[0]
        return a + float(idx[len(idx) // 2])
    box[1] = (calm(max(prev), t_o) if prev else t_o - pad) / oh
    box[3] = (calm(b_o, min(nxt)) if nxt else b_o + pad) / oh
    print(f"  trim=({box[0]:.3f}, {box[1]:.3f}, {box[2]:.3f}, {box[3]:.3f})  縦横比 {(box[2] - box[0]) * w / ((box[3] - box[1]) * h):.2f}"
          f"（絵の行 {len(inside)}・上のすき間 {(t_o - max(prev)) if prev else '—'}px・下のすき間 {(min(nxt) - b_o) if nxt else '—'}px）")
    T, B = box[1] * oh, box[3] * oh
    hit = [ln["text"][:40] for ln in o["lines"] if ln["box"][0] < R and ln["box"][2] > L
           and any(ln["box"][1] < e < ln["box"][3] for e in (T, B))]
    print(f"  {'🔴' if hit else '✓'} 上下の辺にかかる OCR の行 {len(hit)}" + (f"：{hit}" if hit else ""))
    return 1 if hit else 0


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
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）＝16・17・20・23本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def _src_ok(code, s, fet):
    """手元の元のファイルが取得の記録と同じか＝(md5, 何で照らしたか)。違えば止める"""
    p = HERE / s["file"]
    if not p.exists():
        raise SystemExit(f"🔴 {code}: 手元のファイルが無い（{s['file']}）")
    h = md5(p)
    rows = fet.get(code) or []
    if rows:
        if not any((EPD / r["file"]).resolve() == p.resolve() and r["md5"] == h for r in rows):
            raise SystemExit(f"🔴 {code}: {p.name} の md5 が fetch25.tsv と合わない（取り直す）")
        return h, "fetch25.tsv の md5 と同じ"
    if s["type"] == "gsi":
        log = GSI_LOG.read_text(encoding="utf-8") if GSI_LOG.exists() else ""
        if p.name not in log:
            raise SystemExit(f"🔴 {code}: 地理院の記録 gsi_log.txt に {p.name} が無い")
        return h, "gsi_log.txt（16/16 タイル・md5 の記録なし＝この md5 を元とする）"
    raise SystemExit(f"🔴 {code}: 取得の記録が無い（fetch25.tsv）")


def year_of(code, s):
    if code in YEAR_FIX:
        return YEAR_FIX[code]
    t = s["type"]
    if t in PAGE_TYPES:
        return doc_year(_page_ref(s)[0])
    m = re.fullmatch(r"M05(\d\d)(\d\d)(?:_\d)?", code)
    if t == "mlit-photo" and m:
        return 2005, f"国交省の発表 2005-{m.group(1)}-{m.group(2)}（事故 2005-04-25 のあと）"
    if t == "commons":
        d = re.search(r"((?:19|20)\d\d)-\d\d-\d\d", s["title"])
        if d:
            return int(d.group(1)), f"Commons の撮影日（sources25.psv の題の欄 {d.group(0)}＝②③ に Commons の頁で読んだ）"
        return None, "Commons の撮影日を読んでいない"
    if t == "report-photo":
        return None, "報告書の付図の写真＝撮影の日の記載なし（事故のあと・報告書の公表 2007年6月より前）"
    if t == "gsi":
        return None, f"地理院タイルの層＝{s['title'].split('（', 1)[-1].rstrip('）')}（1枚ごとの撮影年は読んでいない）"
    return None, "撮影の日の出どころが無い"


def screen_credit(code, s, rec_how, face_mask, name_mask):
    """画面の出典の行（了承② 決め4）。報告書・国交省・地理院・判決＝sources25 の出典の欄のまま（写真は「を加工して作成」入り）。
    🔴 名前の外を切り出した頁（PDL1.0）は「を加工して作成」を足す。Commons＝「写真：…（許諾）」＋ CC BY は必ず「改変」の語
    （`scene_jiko.credit_of` の古い決まりが「CC BY」があって「改変」の語の無い行に「／改変：色調変更・切出」を黙って足す＝23本目 ⑤b-2）"""
    t, r = s["type"], s["rights"]
    if t == "commons":
        who = f"{AUTHOR}／Wikimedia Commons" if code in NAMED else "Wikimedia Commons"
        line = f"写真：{who}（{r}）"
        if r.startswith("CC BY"):
            return line + "・改変：切出" + ("・顔にモザイク" if face_mask else "")
        return line + ("・改変：顔にモザイク" if face_mask else "")
    cr = s["credit"]
    if code in PAGE_CROP and r == "PDL1.0" and not cr.endswith("を加工して作成"):
        cr += "を加工して作成"
    if face_mask:
        raise SystemExit(f"🔴 {code}: 公的な機関の写真に顔の升目（出典の行の決まりを先に）")
    return cr


def who_table(code, s):
    """CREDITS.md の撮影者の欄（名前は書かない）"""
    t = s["type"]
    if t == "commons":
        return ("作者欄のとおり（Commons の頁・名前は git の外 `ref/ep25/src/credits_private.tsv` の commons の行）" if code in NAMED
                else "Commons の投稿者（CC0＝表示は任意）")
    if t.startswith("report"):
        return "運輸安全委員会（旧 航空・鉄道事故調査委員会）"
    if t.startswith("mlit"):
        return "国土交通省（航空・鉄道事故調査委員会の発表）"
    if t == "gsi":
        return "国土地理院"
    if t == "court-page":
        return "裁判所"
    return s["credit"]


# ── 束を作る ─────────────────────────────────────────────────
def cmd_build():
    src, fet, names = _sources(), _fetched(), _names()
    db, bad = {}, 0
    us = uses()
    for code in PAGE_CROP:
        if code not in us:
            print(f"🔴 PAGE_CROP の {code} は一覧で使っていない")
            bad += 1
    for code, cuts in sorted(us.items()):
        s = src[code]
        name = bundle_name(code)
        dst = EPD / f"{name}.jpg"
        page = s["type"] in PAGE_TYPES
        rec, nmos = {}, 0
        if page:
            im, rec, nmos = render_page(code, s, names)
            notes = [rec["how"]]
            smd5 = rec["pdf_md5"]
        else:
            smd5, how_src = _src_ok(code, s, fet)
            im, notes = load_photo(HERE / s["file"])
            im, k = _shrink(im)
            if k < 1.0:
                notes.append(f"縮小 ×{k:.3f}")
            notes.append(how_src)
        box_m = MASK.get(code, [])
        if box_m:
            im = mosaic(im, box_m, MOSAIC_PX)
            notes.append(f"顔だけ升目 {len(box_m)}か所（升 {MOSAIC_PX}px）")
        im.save(dst, quality=JPEG_Q, optimize=True)
        w, h = im.size
        if s["rights"] not in ("PDL1.0", "CC0", "CC BY 3.0", "引用（第三者の資料）", "著作権法13条"):
            print(f"🔴 {code}: 権利の記号が読めない（{s['rights']}）")
            bad += 1
            continue
        frame = s["rights"] == "引用（第三者の資料）"          # 会社の資料（付図35・47・48）＝頁ごと引用＝無加工・額装
        y, ywhy = year_of(code, s)
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(cuts),
                        credit=screen_credit(code, s, rec.get("how", ""), bool(box_m), bool(nmos)),
                        who=who_table(code, s), note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=s["rights"], frame=frame, ground=s["rights"], url=s["page"] or s["file"],
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False, page=page, related=False,
                        quote_page=page, named=code in NAMED, mosaic=[list(b[:4]) for b in box_m] or None, name_mosaic=nmos or None,
                        masked_before=MASKED_BEFORE.get(code), era=s["era"], people=s["people"], **({"src_rec": rec} if rec else {}))
        print(f"✓ {code:12} {name:13} {w}x{h:<5} {' '.join(cuts):10} {s['rights']}{'  額装だけ' if frame else ''}"
              f"{'  頁' if page else ''}  {'・'.join(notes)[:100]}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    print(f"→ ref/ep25/assets.json（{len(db)}点・写真 {sum(1 for r in db.values() if not r['page'])}・頁 {sum(1 for r in db.values() if r['page'])}"
          f"・額装だけ {sum(1 for r in db.values() if r['frame'])}・名前を足す点 {sum(1 for r in db.values() if r['named'])}"
          f"・顔の升目 {sum(1 for r in db.values() if r['mosaic'])}・名前の升目 {sum(1 for r in db.values() if r['name_mosaic'])}"
          f"・束の大きさ {tot / 1e6:.1f}MB）")
    return 1 if bad else 0


def cmd_look(codes, out_name="look.jpg", width=960):
    """束の写真を並べた見本（2列）＝リポの外（SCRATCH）。記号（F12）か束の名（f12）を渡す"""
    from PIL import Image, ImageDraw
    db = json.loads(DB.read_text(encoding="utf-8"))
    ims = []
    for c in codes:
        ns = [n for n, r in db.items() if n == c or r["code"] == c]
        if not ns:
            raise SystemExit(f"🔴 {c} は束に無い（build を先に）")
        for n in ns:
            im = Image.open(EPD / f"{n}.jpg").convert("RGB")
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            ImageDraw.Draw(im).rectangle((0, 0, 170, 40), fill=(0, 0, 0))
            ImageDraw.Draw(im).text((8, 8), n, fill=(255, 255, 0))
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
    ars = sorted((r["w"] / r["h"], n, r["w"], r["page"]) for n, r in db.items() if not Path(n).name.startswith("fb_"))
    for a, n, w, pg in ars:
        print(f"  {a:6.3f}  {n:30} 幅 {w}{'  頁' if pg else ''}{'  （1280 未満＝kind() は額装）' if w < 1280 else ''}")
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
        m = PE.margins(f"ep25/{n}.jpg")
        mx = max(m.values())
        flag = "🔴" if mx >= PE.MIN_EDGE else ("・" if mx > 0 else " ")
        if mx > 0:
            hits.append((n, m))
        print(f"{flag} {n:30} 左 {m['l'] * 100:4.1f}% 上 {m['t'] * 100:4.1f}% 右 {m['r'] * 100:4.1f}% 下 {m['b'] * 100:4.1f}%{'  頁' if db[n]['page'] else ''}")
    big = [n for n, m in hits if max(m.values()) >= PE.MIN_EDGE]
    print(f"→ 暗い帯のある点 {len(hits)}（うち {PE.MIN_EDGE * 100:.1f}% 以上 {len(big)}＝{' '.join(big) or 'なし'}）")
    return 0


# ── 名前の門番（絵の OCR × git の外の名前の表）──────────────────────
def _ocr(files):
    sys.path.insert(0, str(HERE / "tools"))
    import check_slide as CS
    out = {}
    for i in range(0, len(files), 12):              # ocr_win.ps1 は1回の引数が長すぎると落ちる＝12枚ずつ
        out.update(CS.run_ocr(files[i:i + 12]))
    return out


def scan_names(files, names):
    """{ファイル名: [(名前の頭1字＋○, 行の箱), …]}＝OCR の行（空白なし・NFKC）と、ファイル全体をつないだ字（行をまたぐ名前）の両方で探す"""
    o = _ocr([str(f) for f in files])
    hits = {}
    for f in files:
        v = o.get(Path(f).name)
        if v is None:
            raise SystemExit(f"🔴 {Path(f).name} の OCR が返らない（fail closed）")
        found = []
        for ln in v["lines"]:
            t = _norm(ln["text"])
            found += [(_mask_word(n), ln["box"]) for n in names if n in t]
        whole = "".join(_norm(ln["text"]) for ln in v["lines"])
        found += [(_mask_word(n), None) for n in names if n in whole and not any(w == _mask_word(n) for w, _ in found)]
        hits[Path(f).name] = (found, len(v["lines"]))
    return hits


def cmd_names(args):
    names = _names()
    if args and args[0] == "--selftest":
        return names_selftest(names)
    files = []
    for a in args:
        p = Path(a)
        files += sorted(p.glob("*.png")) + sorted(p.glob("*.jpg")) if p.is_dir() else [p]
    if not args:
        db = json.loads(DB.read_text(encoding="utf-8"))
        files = [EPD / f"{n}.jpg" for n, r in sorted(db.items()) if r["page"]]
    if not files:
        print("🔴 絵が0枚（fail closed）")
        return 2
    res = scan_names(files, names)
    bad = 0
    for fn, (found, nl) in res.items():
        if found:
            bad += 1
            print(f"🔴 {fn}: 名前 {len(found)}件（{sorted({w for w, _ in found})}）")
        elif nl == 0:
            print(f"⚠️ {fn}: OCR の行 0（字の無い絵か読めない絵＝名前も無い）")
    print(f"→ 名前の門番：絵 {len(res)}枚・名前の表 {len(names)}語・当たり {bad}枚" + ("" if bad else "＝✓"))
    return 1 if bad else 0


# 🔴 OCR の見落とし（⑤b-2 の selftest で測った）：R1 PDF2 の差出の委員長の名前は**字の間を広く空けた署名**（1字ずつ別の箱）＝Windows の OCR は
#    2行を縦の列と読み違えて名前を拾わない（陽性対照で 0件）。＝名前の網は2つ重ねる：① 字の層の網（`render_page`＝名前の字の箱が束の絵に入れば
#    束を作らずに止める・PDF の頁だけ）② 絵の OCR の網（この `names`＝焼いた絵も見られる・字の層の無い絵も見られる）。① の陽性対照は下で
OCR_BLIND = {"P-R1-002": "差出の署名は字の間が広い＝OCR が縦の列と読み違える（字の層の網が受け持つ）"}


def names_selftest(names):
    """陽性対照＝名前の載る頁をまるごと（切らずに）描いた絵で、OCR が名前を拾うか（拾わなければ門番は何も測っていない）。
    陰性対照＝同じ頁の束（名前の外を切り出した絵）で 0件。＋字の層の網の陽性対照＝PAGE_CROP の5頁のまるごとに名前の字の箱がある"""
    import fitz
    from PIL import Image
    src = _sources()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    pos = []
    for code in ("P-K05-1", "P-R1-002", "P-S2-1"):
        name, no, _ = _page_ref(src[code])
        pg = fitz.open(pdf_path(name))[no - 1]
        k = PAGE_LONG / max(pg.rect.width, pg.rect.height)
        pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), alpha=False)
        p = SCRATCH / f"names_pos_{bundle_name(code)}.jpg"
        Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(p, quality=JPEG_Q)
        pos.append((code, p))
    neg = [EPD / f"{bundle_name(c)}.jpg" for c in PAGE_CROP]
    res = scan_names([p for _, p in pos] + neg, names)
    ok = True
    for code, p in pos:
        found, _ = res[p.name]
        if code in OCR_BLIND:
            print(f"  ⚠️ 陽性対照 {p.name}：名前 {len(found)}件＝OCR の見落としの型（{OCR_BLIND[code]}）")
            continue
        print(f"  {'OK' if found else '🔴 NG'} 陽性対照 {p.name}：名前 {len(found)}件")
        ok &= bool(found)
    for p in neg:
        found, _ = res[p.name]
        print(f"  {'OK' if not found else '🔴 NG'} 陰性対照 {p.name}（束）：名前 {len(found)}件")
        ok &= not found
    for code in PAGE_CROP:
        name, no, _ = _page_ref(src[code])
        nb = name_boxes(fitz.open(pdf_path(name))[no - 1], names)
        print(f"  {'OK' if nb else '🔴 NG'} 字の層の網の陽性対照 {code}（頁まるごと）：名前の字 {len(nb)}字")
        ok &= bool(nb)
    print("→ selftest " + ("合格" if ok else "🔴 不合格"))
    return 0 if ok else 1


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
# 出典の行の字幅の上限の目安（全角＝1・半角＝0.55）＝23本目の写真の出典の行で門番 layout を通って公開された最長 56.5。本当の物差しは門番 layout
CREDIT_W_MAX = 56.5


def _width(s):
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.55 for c in s)


def cmd_credits(write=False):
    """撮影年＝year_of（出どころつき）。当てたカットの副題が名乗る年（「NNNN年」・「当日」＝2005）と食い違えば止める（写真も頁も＝check_credits と同じ）。
    作者の名乗り（scene_jiko._ep25_author）を当てて出典の行の字幅を測る（名前は出さない＝字数だけ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import scene_jiko as SJ
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    names = set(_names())
    for v in _private().values():
        a = (v.get("author") or "").strip()
        if a:
            names |= {x for x in re.split(r"[\s/()]+", a) if len(x) >= 4 and x[0].isupper()}
    cj, rows, bad = {}, [], 0
    for n, r in sorted(db.items()):
        cuts = r["cut"].split()
        claims = set()
        for c in cuts:
            claims |= {int(y) for y in re.findall(r"(1[89]\d\d|20\d\d)年(?!代|ごろ)", subs.get(c, ""))}
            if "当日" in subs.get(c, ""):
                claims.add(EVENT_YEAR)
        y = r["year"]
        if claims and (y is None or claims != {y}):
            print(f"🔴 {n}: 副題の年 {sorted(claims)} と撮影年 {y} が食い違う（{' '.join(cuts)}・{subs.get(cuts[0], '')}）＝{r['year_why'][:60]}")
            bad += 1
        blob = _norm(json.dumps(r, ensure_ascii=False))
        leak = [x for x in names if x and _norm(x) in blob]
        if leak:
            print(f"🔴 {n}: 台帳の行に出さない名前が入っている（{len(leak)}語）")
            bad += 1
        line = r["credit"]
        if AUTHOR in line:
            try:
                line = line.replace(AUTHOR, SJ._ep25_author(f"ep25/{n}.jpg"))
            except Exception as e:                         # noqa: BLE001  焼く前に止める
                print(f"🔴 {n}: 作者の名乗りが作れない（{e}）")
                bad += 1
        wd = _width(line)
        if wd > CREDIT_W_MAX:
            print(f"🔴 {n}: 出典の行の字幅 {wd:.1f}（{CREDIT_W_MAX} まで＝画面の左下からはみ出すおそれ）")
            bad += 1
        cj[f"ep25/{n}.jpg"] = r["credit"]
        kind = "頁" if r["page"] else "この事故"
        mod = "・顔に升目" if r.get("mosaic") else ("・姓に升目" if r.get("name_mosaic") else "")
        rows.append(f"| `{n}` | {' '.join(cuts)} | {y if y else '不明'} | {r['lic']}（{kind}{mod}） | {r['who']} | {r['url']} |")
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
        "※2026-10-25（⑤b-2）。`qa_out/ep25_assets.py credits --write` が書く（手で直さない）。写真と頁は映像方針の一覧 `ref/ep25/eizou_list25.md`（了承② 2026-10-25）。",
        "",
        "### 0. 映像（フリー素材＝音はすべて使わない＝`-an`）",
        "- フリー素材（Pexels・生成AI は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」だけ"
        "（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）",
        "- 25本目は18カット＝⑤b-3 で取った（2026-10-25・カズヤくんの了承＝候補の名前・出どころ・大きさを示して先に聞いた・幅1920の版）。"
        "使う区間と寄せ（人の顔・字・ロゴ・会社の塗装を画面の外へ）は `qa_out/ep25_assets.py` の STOCK_WINDOW・STOCK_GEOM",
        "",
        "| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |",
        "|---|---|---|---|---|", *film_rows, "",
        "### 1. 写真・頁（運輸安全委員会の報告書・国土交通省の頁・国土地理院・裁判所・Commons）",
        "- 報告書 RA2007-3・検証報告書・建議・国交省の発表＝公共データ利用規約（PDL1.0）＝出典の行「出典：…（運輸安全委員会の頁）を加工して作成」"
        "／「出典：国土交通省ウェブサイト（URL）」（了承② 決め4）。報告書の小さい写真も全面（原画＝PDF の上の注記は入らない）",
        "- 会社の資料の写し（付図35・47・48）＝報告書に載った第三者の資料＝**頁ごと引用**（無加工・額装＝`frame`）",
        "- 判決・決定＝著作権法13条（権利の目的とならない）。地理院の空中写真＝国土地理院コンテンツ利用規約（PDL1.0 準拠）",
        "- 🔴 **人は役職だけ（①の承認）**＝名前の載る頁（建議 p.1・報告書の表紙の裏・最高裁の決定 p.1・検証報告書 p.50・p.53）は束の段で名前の外を"
        "切り出した（検証報告書 p.53 だけ姓の字に升目＝役職は残す）＝門番 `qa_out/ep25_assets.py names`（絵の OCR × git の外の名前の表）",
        "- 🔴 **CC BY 3.0 の点は画面の出典の行に作者欄の名前**。名前はこのリポに書かない＝`ref/ep25/credits.json` は印 `{作者}` だけ・焼くときに"
        " git の外の表から足す（`tools/scene_jiko.ep25_credit`）。CC0 は表示が任意＝名前を出さない",
        "- 撮影年＝Commons の撮影日・国交省の発表の日・資料の日。報告書の付図の写真は撮影の日の記載が無い＝「不明」（副題に年を書かない）",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. 地図の衛星写真（Google マップ）",
        "- c101・c328・c517・ca23・cb03＝Google マップの衛星写真（束の外＝`cuts/ss.SAT`）。出典は画面の地図の右下の帰属の行（Google の地図の利用）＋"
        "出典の行「地図：Google マップの衛星写真（帰属は地図の右下）」。🔴 PNG は公開リポに置かない（git の外・md5 と出どころは `cuts/ss.SAT`・`GEO`）",
        "- 🆕 ⑤b-3：描き足した線路の位置（c328・c517・ca23）＝国土地理院「地理院地図Vector」（experimental_bvmap・鉄道の中心線）を加工して作成"
        "（国土地理院コンテンツ利用規約＝出典の明示）＝額の下の断りに「線路の位置：地理院地図Vector（国土地理院）」・線の点は `cuts/ss.SAT_LINES`。"
        "駅と事故の現場の点＝Wikidata の座標（一般の座標＝断りに「一般の座標」）",
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


# ── 映像（フリー素材）：台帳・ショット・見取り図・USE・ひかえ ── ⑤b-3 で初めて回す（24本目の形） ──────────────
def _film_codes():
    """映像の記号 → 使うカット（一覧の順）"""
    src = _sources()
    out = {}
    for r in _list():
        s = src.get(r["code"], {})
        if s.get("type") == "stock":
            out.setdefault(r["code"], []).append(r["cid"])
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


def _media_url(pid, loc, size, rec=None):
    """Pexels の置き場の直リンクを HEAD で当て、大きさが手元と同じ版を返す（違えば止める）。
    🆕 ⑤b-3（10-25）：2024年ごろからの素材は直リンクの名の形が `<番号>/<ファイルの番号>_1920_1080_<fps>fps.mp4`（番号から組めない）
    ＝取得の記録（fetch25.tsv の source＝`stock:<直リンク>`）の URL を HEAD で照らす。記録が無いときだけ古い名の形を組む"""
    if rec:
        try:
            st, n, ct = _head(rec)
        except Exception as e:                               # noqa: BLE001
            raise SystemExit(f"🔴 {pid}: 記録の直リンクを引けない（{rec}・{e}）")
        if st != 200 or n != size or not ct.startswith("video/"):
            raise SystemExit(f"🔴 {pid}: 記録の直リンクが手元と違う（http {st}・{n} B／手元 {size} B・{ct}）")
        return rec
    label = {1920: "hd_1920_1080", 2560: "uhd_2560_1440", 3840: "uhd_3840_2160"}.get(loc["w"])
    if not label:
        raise SystemExit(f"🔴 {pid}: 幅 {loc['w']} の版の名の形が分からない")
    fps0 = round(loc["fps"])
    for fps in [fps0] + [f for f in (30, 25, 24, 60, 50) if f != fps0]:
        u = f"https://videos.pexels.com/video-files/{pid}/{pid}-{label}_{fps}fps.mp4"
        try:
            req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                n = int(r.headers.get("Content-Length") or 0)
                if r.status == 200 and n == size:
                    return u
        except Exception:                                    # noqa: BLE001  形が違えば 403/404＝次の形
            pass
    raise SystemExit(f"🔴 {pid}: 手元と同じ大きさの直リンクが見つからない（{size} B）")


def cmd_clips():
    src, fet = _sources(), _fetched()
    out = {}
    for code, cuts in _film_codes().items():
        s = src[code]
        p = HERE / s["file"]
        rows = fet.get(code) or []
        if not rows or not p.exists() or md5(p) not in {r["md5"] for r in rows}:
            raise SystemExit(f"🔴 {code}: 手元の映像が無いか md5 が取得のときと違う（{s['file']}）＝⑤b-3 で取る")
        loc = _probe(p)
        size = p.stat().st_size
        pid = re.search(r"(\d{5,})", s["page"]).group(1)
        rec = next((r["source"][6:] for r in reversed(rows) if r["md5"] == md5(p) and r["source"].startswith("stock:http")), None)
        media = _media_url(pid, loc, size, rec)
        e = dict(url=s["page"], media=media, stock=True, file=s["file"].removeprefix("ref/"), credit="イメージ（Pexels）", src="stock",
                 at=0.0, what=s["note"][:60], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(loc["sec"], 3),
                 size=size, md5=md5(p), dispw=loc["w"], decoded=[loc["w"], loc["h"]], license="Pexels License",
                 license_url="https://www.pexels.com/license/", site="Pexels")
        out[code] = e
        print(f"  {code:12} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.2f}秒  {' '.join(cuts):12} {media.rsplit('/', 1)[-1]}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep25/clips.json（{len(out)}本）")
    return 0


# 🔴 動きの速い素材は、隣の1秒の差がしきい値を超えて「境目」が出る（18本目 0b-45⑥・23・24本目の SHOT_ONE）＝根拠つきで1ショットに直す
#   🆕 ⑤b-3（10-25）：境目の前後±1.2秒の全コマ（160×90 の灰色）の隣のコマとの差＝跳ねる1コマが無い（切り替わりなら1コマに集まって
#      中央値の何倍にもなる）＝手・カメラ・電車の動きの続き（scratchpad の cutspike.py）。⚠️ 絵は見取り図と試し焼きのコマで目で確かめる
#   ⚠️ 記号は素材を替えても同じ（X-desk は第1候補 6781564 → 第2候補 7685212）＝替えたら境目を測り直して書き直す（前の素材の根拠を残さない）
SHOT_ONE = {
    "X-training": "2・12秒の境目＝最大 1.6・中央値の 1.2倍＝ゆっくり動くカメラの続き",
    "X-court": "6秒の境目＝最大 2.7・中央値の 1.9倍＝カメラの動きの続き",
    "X-depart": "4秒の境目＝最大 11.0・中央値の 1.3倍＝近づく電車の動きの続き（第2候補 37420614＝⑤b-3 の試し焼きで第1候補を落とした）",
    "X-papers": "2・7・9・12秒の境目＝最大 7.2・中央値の 1.2〜3.2倍＝ページをめくる手の動きの続き",
    "X-phone": "4秒の境目＝最大 4.3・中央値の 1.2倍＝カメラの動きの続き",
    "X-table": "1・4・11・13・16秒の境目＝最大 4.5・中央値の 2.7〜5.6倍（山の高さは 3〜4.5 で小さい）＝カメラの動きの続き",
    "X-train": "7秒の境目＝最大 9.3・中央値の 1.6倍＝走る電車の動きの続き",
}


def cmd_shots():
    """shots.json＝フリー素材は tools/shots.shots_of（1秒1コマ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import shots as SH
    src = _sources()
    out = {}
    for code in _film_codes():
        s = src[code]
        sh, dur = SH.shots_of(HERE / s["file"])
        how = "1秒1コマで tools/shots.shots_of（25本目・フリー素材）"
        if code in SHOT_ONE:
            sh = [dict(start=0.0, until=float(sh[-1]["until"]), motion=max(x["motion"] for x in sh))]
            how += f"・🔧 1ショットに直した（{SHOT_ONE[code]}）"
        out[code] = dict(src=s["page"], scan=s["file"], dur=round(dur, 1), how=how, shots=sh)
        print(f"  {code:12} {dur:6.1f}秒  ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep25/shots.json（{len(out)}本）")
    return 0


def cmd_frames(code, step=1.0, width=384, cols=5):
    """映像の step 秒ごとのコマを並べた見取り図（秒の札つき）＝区間を選ぶとき（out/ep25_look/frames_<記号>.jpg）"""
    from PIL import Image, ImageDraw
    s = _sources()[code]
    p = HERE / s["file"]
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
    nl = "\r\n" if "\r\n" in txt else "\n"              # 🔴 ⑤b-1 の落とし穴＝改行を見分ける（作業ツリーは autocrlf=true でもファイルは LF）
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_bytes((txt[:m.start(2)] + "".join(x + nl for x in lines) + txt[m.end(2):]).encode("utf-8"))


# フリー素材の映像の区間 {cid: (始め, 終わり, 理由)}＝⑤b-3 で見取り図（frames）と shots.json の境目を見て決める
#   🆕 ⑤b-3（10-25）：区間の 640px のシート（頭・真ん中・尻）と原寸の切り出しで決めた（scratchpad の stocksheet.py・pairsheet.py）
STOCK_WINDOW = {
    # c210＝第2候補 37420614（7.64秒）。第1候補 30423319 は試し焼きの原寸でホームの駅名標「豪徳寺」が読めた（語りは宝塚駅）＝落とした。
    #   🔴 第2候補も使えない（見取り図＝路面電車の運転室からの眺め・対向の電車の運転士・終わりに駅の札＝「宝塚駅を出た」と合わない）
    #   ＝⑤b-4 で新しい候補を探し、名前・出どころ・大きさを示してカズヤくんに聞いてから取り直す（それまでの置き場＝門番を通すだけ）
    #   ⚠️ shots の終わりは1秒に丸めた 8.0秒＝実の長さ 7.64秒を越える＝区間を手で書く（端の 0.3秒を外す＝0.92倍）
    "c210": (0.30, 7.34, "素材まるごと（端の 0.3秒を外す）"),
    "c532": (8.40, 15.71, "壁の英語の貼り紙が入らない区間（0〜8秒は上の端に貼り紙の字）"),
    "c707": (0.30, 8.53, "看板の少ない前半（後半は駐車場と店の看板が増える）"),
    "c724": (4.30, 12.93, "JR西日本の電車が入らない区間（0.3秒の頭と16秒・21秒に JR西日本の電車）"),
}
# 寄せ（footage.USE の zoom・bias・xbias＝build_jiko が映像のカットに使う〈fzm・fbias・fxb〉・ひかえの静止画は cmd_fb が同じ式）
#   c707＝下の駐車場と店の看板を外へ／c726＝下の「Information」の字と交通局のロゴを外へ
#   （c210 の第1候補には右端のホームの人を外す寄せ〈zoom 1.2・xbias 0〉を書いていた＝第2候補に替えて外した）
#   c902＝正面の上の建物の名の字（PALÁCIO DA JUSTIÇA）を外へ（字の帯は高さの 0.15〜0.17＝bias 1.0 で見える範囲は 0.2〜1.0）
STOCK_GEOM = {
    "c707": dict(zoom=1.15, bias=0.0),
    "c726": dict(zoom=1.2, bias=0.0),
    "c902": dict(zoom=1.25, bias=1.0),
}
STOCK_EDGE = 0.3                # ショットの境目から離す秒（フリー素材＝1秒1コマで測った境目＝23・17・24本目と同じ）


def cmd_use(only=None, all_=False):
    """footage.USE の25本目の欄（🔴 章ファイルに `ss.vid` を書いたカットだけ・`only` は書く前の鶏と卵を割るため）"""
    sys.path.insert(0, str(HERE / "tools"))
    if only:
        secs, spec = {r["cid"]: float(r["cont"]) for r in _list()}, {}
    else:
        import footage as FO
        import scene_jiko as S
        secs, spec = FO.secs_of(), S.SPEC
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    lines, skip = [], []
    films = _film_codes()
    for r in _list():
        if r["code"] not in films:
            continue
        cid, code = r["cid"], r["code"]
        sp = spec.get(cid) or {}
        wrote = str(sp.get("photo") or "").endswith(f"stock/fb_{cid}.jpg")
        if not (all_ or wrote or (only and cid in only)):
            skip.append(cid)
            continue
        need = float(secs[cid])
        shs = sd[code]["shots"]
        if cid in STOCK_WINDOW:
            a, b = STOCK_WINDOW[cid][:2]
            hit = [x for x in shs if x["start"] <= a < x["until"]]
            if len(hit) != 1 or b > hit[0]["until"]:
                raise SystemExit(f"🔴 {cid}: 区間 {a}〜{b} が1つのショットに収まらない")
            sh = hit[0]
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
        why = f"・{STOCK_WINDOW[cid][2]}" if cid in STOCK_WINDOW else ""
        lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate={rate}{geo}),   '
                     f'# ショット {sh["start"]:g}〜{sh["until"]:g}秒・使える {b - a:.2f}秒／要る {need:.2f}秒{why}')
    _write_block("EP25_USE", lines)
    print(f"→ tools/footage.py USE {len(lines)}欄")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）→ ref/ep25/stock/fb_<cid>.jpg（🔴 git に入れない＝決め⑨）"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    from PIL import Image
    bad = 0
    (EPD / "stock").mkdir(exist_ok=True)
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
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
        lft, top = (sw - cw) * float(u.get("xbias", 0.5)), (sh_ - ch) * float(u.get("bias", 0.5))
        im = im.crop((round(lft), round(top), round(lft + cw), round(top + ch))).resize((1920, 1080), Image.LANCZOS)
        dst = EPD / "stock" / f"fb_{cid}.jpg"
        im.save(dst, quality=92)
        print(f"✓ {cid:5} {u['clip']:12} {float(u['start']):6.2f}秒 {sw}x{sh_} → {dst.relative_to(HERE).as_posix()}")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "edges": cmd_edges, "clips": cmd_clips, "shots": cmd_shots}
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] == "use":
        sys.exit(cmd_use(set(x for x in a[1:] if not x.startswith("--")) or None, "--all" in a))
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "look":
        sys.exit(cmd_look(a[1:]))
    if a and a[0] == "frames":
        sys.exit(cmd_frames(a[1], float(a[2]) if len(a) > 2 else 1.0))
    if a and a[0] == "pbox":
        sys.exit(cmd_pbox(a[1], a[2], a[3]))
    if a and a[0] == "names":
        sys.exit(cmd_names(a[1:]))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
