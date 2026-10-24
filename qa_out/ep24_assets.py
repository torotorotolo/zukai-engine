# -*- coding: utf-8 -*-
"""ep24_assets.py — 24本目（チェルノブイリ原発事故）の写真・頁・映像の束（⑤b-2・2026-10-22）。17本目 `ep17_assets.py`（Commons の作者の印・
関連の写真・頁・フリー素材）の形を、24本目の台帳（`sources24.psv` の13列・`fetch24.tsv`・git の外の作者の表の `e24:` の行）に合わせた。

取得はすんでいる（映像方針＝了承②・`ref/ep24/eizou_build/fetch24.py`・記録 `fetch24.tsv`＝md5 2回）。ここは**束を作る道**だけを持つ。
  python qa_out/ep24_assets.py build             # 写真・頁の束 ref/ep24/<名>.jpg ＋ 権利の台帳 ref/ep24/assets.json
  python qa_out/ep24_assets.py look I15 U1 …     # 束の写真を並べた見本（out/ep24_look/・1枚 960 幅）＝選ぶとき・確かめるとき（記号か束の名）
  python qa_out/ep24_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python qa_out/ep24_assets.py edges             # 束の四辺の暗い帯（スライドの台紙の縁）＝門番 check_photo_edge の名簿を決める
  python qa_out/ep24_assets.py credits [--write] # 画面の出典 ref/ep24/credits.json と ref/CREDITS.md の24本目の節
  python qa_out/ep24_assets.py pbox S1p34 "(6)" "causing the accident"   # 頁の字の層の行から切り口（束の割合）を測る
  python qa_out/ep24_assets.py clips             # ref/ep24/clips.json（フリー素材の映像の台帳＝置き場の直リンクは HEAD で大きさを照らす）
  python qa_out/ep24_assets.py shots             # ref/ep24/shots.json（フリー素材＝1秒1コマ）
  python qa_out/ep24_assets.py frames X13188726  # 映像の1秒ごとのコマの見取り図（out/ep24_look/）＝区間を選ぶとき
  python qa_out/ep24_assets.py use [c101 …]      # tools/footage.py の EP24_USE（🔴 章ファイルに `ss.vid` を書いたカットだけ・`--all` で一覧の全部）
  python qa_out/ep24_assets.py fb [c101 …]       # フリー素材のひかえの静止画 ref/ep24/stock/fb_<cid>.jpg（git に入れない）

入力＝映像方針の一覧 `ref/ep24/eizou_build/list24.tsv`（生成物・秒は narration.json の実測＝⑤b-1）・出どころ `sources24.psv`（区切り「|」）・
取得の記録 `fetch24.tsv`・Commons の API の控え `api24.json`（撮影日 dto）。元は `ref/ep24/src/`（git の外）。
🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色・了承②）＝幅 2400 か高さ 1350 の大きい方まで。切り出しは表 CROP の点だけ
   （USGS の掲示の2つの欄・1984年の偵察衛星の写真の原本〈21634×16500〉の2か所・CR4B の学生を外した盤）。
🔴 **個人名義の Commons の点は、画面の出典の行に作者欄の名前を出すが、名前は公開リポに書かない**（17・23本目の型）
   ＝credits.json の行は印 `{作者}` だけ・焼くときに `scene_jiko.ep24_credit` が git の外の表 `ref/ep24/src/credits_private.tsv` から足す
   （名乗りの短い形＝`scene_jiko._ep24_short`）。CC0・PD は表示が任意＝名前を出さない（記憶 no-optional-credits）。
🔴 **「参考」の写真（同じ型の炉＝ほかの発電所）は台帳に `related: true`**＝一覧の種類「参考」から（同じ記号を「参考」とほかの種類の両方に
   当てていたら止める）。門番 check_text_screens が PLAN の注「関連（」と照らし、20% の数（この事故の写真）から外す。
   報告書・会議録の頁と一覧の種類「頁」の点（CIA の地図・USGS の図12）は台帳に `page: true`（写真に数えない）。
🔴 撮影年＝`api24.json` の dto（Commons の撮影日の欄）。⚠️ IAEA 0279 の組（USFCRFC の歴史の写真）の多くは欄が**取り込みの日（2005・2006年）**
   ＝ルール 2-24 の罠＝年は「分からない」（説明に年が無い＝10-22 に Commons の説明を API で読んだ）。副題の年と食い違えば credits が止める。
"""
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep24"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list24.tsv"
SOURCES = BUILD / "sources24.psv"
FETCH = BUILD / "fetch24.tsv"
API = BUILD / "api24.json"
PRIVATE = EPD / "src" / "credits_private.tsv"      # 🔴 git の外（作者欄・題）＝ここから名前を公開の物へ写さない
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
FOOTAGE = HERE / "tools" / "footage.py"
SCRATCH = HERE / "out" / "ep24_look"           # look・frames の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## チェルノブイリ原発事故（1986-04-26・24本目）"
AUTHOR = "{作者}"            # 個人名義の点の画面の出典の行の印（焼くときに git の外の表から足す＝scene_jiko.ep24_credit）
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（footage.py の注）
EVENT_YEAR = 1986            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）
UA = "zukai-engine/1.0 (ep24 visual plan research)"

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
PAGE_LONG = 3600                       # 頁は長辺 3600 で描く（寄りで字を読める大きさを残す＝17本目と同じ）
JPEG_Q = 92
MOSAIC_PX = 14                         # 顔のモザイクの升（束の画素）
FRAME_RIGHTS = ("CC BY-SA",)           # 額装だけ（了承② 決め4＝BY-SA は額装・無加工・額ごと動かす・1点1カット）
NO_NAME = ("CC0", "Public domain", "PD")   # 表示が任意＝作者の名前を出さない
# 🔴 頁は使うチャットで足す（その章の切り口と一緒に決める）。⑤b-2 は冒頭の c104（INSAG-7 p.34）だけ
#   🆕 ⑤b-7（10-23）：残りの頁を全部足した（文字の頁11・図の頁13＝一覧の頁26 のうち CIA の地図は束の写真の側＝page: true）
PAGES_NOW = ("S1p34", "S3p19+S1p62", "S1p63", "S1p65", "S2p39", "S1p28", "S3p26", "S2p18", "S3p28", "S1p41", "K19860507", "K19861127",
             "S1p127", "GCp142", "S1p128", "GCp140", "S1p129", "GCp43", "S1p15", "S1p133", "S1p141", "S1p138", "L1p8", "L1p15", "U4F12")
# 🆕 ⑤b-7：頁を PDF でなく手元の画像から描く点＝国会会議録（NDL の会議録の画像・字の層なし＝fetch24.tsv の md5 で照らす）。答弁の頁＝OCR で決めた
PAGE_IMAGE = {"K19860507": ("ref/ep24/src/eizou/pages/K19860507_1.png", "参議院 科学技術特別委員会 第6号の1頁目（答弁は下の段）"),
              "K19861127": ("ref/ep24/src/eizou/pages/K19861127_1.png", "衆議院 科学技術委員会 第4号の1頁目（答弁は下の段）")}
# 🆕 ⑤b-7：2頁を「+」でつないだ記号のうち、先（左）の頁だけを描く点 {記号: 理由}
PAGE_FIRST = {"S3p19+S1p62": "c217 の語り3行は1986年のソ連の報告だけ（右の S1p62 は次の c218 の語り＝先に答えを見せない）"}
# 🆕 ⑤b-7：画面の出典の行を sources24.psv の欄から替える頁（sources24 は make_sources24.py の生成物＝回し直さない＝§4-7）
PAGE_CREDIT = {"S3p19+S1p62": "出典：ソ連の報告 Part I（1986年8月）p.19",
               # c304 は上の図 II-3 だけ（下の図 II-4 は切り口の外）＝出典の行に II-4 を名乗らない（試し焼き 39912142820 で見た）
               "S1p127": "出典：INSAG-7 付属書II の図 II-3",
               "K19861127": "出典：国会会議録 1986-11-27 衆議院 科学技術委員会 第4号"}
# 頁の資料の年（副題の年と照らす）＝記号の頭で
PAGE_YEAR = {"S1": (1992, "INSAG-7（1992年）"), "S2": (1986, "INSAG-1＝GC(SPL.I)/3（1986年9月）"), "GC": (1986, "INSAG-1＝GC(SPL.I)/3（1986年9月）"),
             "S3": (1986, "ソ連の報告 Part I（1986年8月）"), "L1": (2006, "チェルノブイリ・フォーラム『Chernobyl's Legacy』（2006年）"),
             "K1": (1986, "国会会議録（1986年5月・11月）"), "U4": (1987, "USGS Bulletin 1785（1987年）")}

# 切り出し {束の名: dict(code, cuts, box, how, auto=暗い地を画素で外すか, decode=JPEG を何分の1で読むか)}。box＝元の絵（向きの札を当てたあと）の割合
#   ⑤b-2（10-22）に縮小＋目盛りの見本（scratchpad の look_*.jpg）を見て決めた。🔴 PD・CC0 だけ（BY-SA は切らない＝check_frame_only）
CROP = {
    # USGS の掲示（5288×3000・黒い地に3つの欄＋本文）＝左の欄「Landsat 5 April 22, 1986 Pre-explosion」・真ん中の欄「April 29, 1986 3 days
    #   post-explosion」。欄の外の黒い地は画素で外す（auto）。⚠️ 4月29日の欄には掲示の白い引き出し線（発電所→下の拡大図）が写る＝そのまま
    "u1_0422": dict(code="U1", cuts=("c102",), box=(0.020, 0.100, 0.340, 0.520), auto=True, how="掲示の左の欄（1986年4月22日）"),
    "u1_0429": dict(code="U1", cuts=("c102",), box=(0.340, 0.100, 0.660, 0.520), auto=True, how="掲示の真ん中の欄（1986年4月29日）"),
    # 1984年1月29日の偵察衛星の写真の原本（PD）＝1/8 の見本で発電所（x 0.51〜0.60・y 0.31〜0.48）と町（x 0.28〜0.47・y 0.18〜0.42）
    #   ⚠️ どの建屋が4号機かは絵で決められない＝印を付けない（映像方針）
    #   ⑤b-2：初めの窓（中心 0.555・0.40）は建屋の固まりが左上に寄った＝切ったあとの絵を見て中心を 0.53・0.38 へ
    "p84_plant": dict(code="P84", cuts=("c223",), box=(0.4117, 0.2927, 0.6483, 0.4673), decode=2, how="原本を 1/2 で読み発電所のまわりを 16:9"),
    "p84_town": dict(code="P84", cuts=("c705",), box=(0.2500, 0.1700, 0.6500, 0.4650), decode=4, how="原本を 1/4 で読みプリピャチの町と発電所を 16:9"),
    # 4号機の制御室（2025・CC0）＝学生が真ん中に立つ（了承② 決め3＝学生を外して切り出す）。向きの札 6 を当てたあと、学生のヘルメットの上の端
    #   （y 0.305）より上の盤だけ（y 0.02〜0.275・横は真ん中の 84%）＝出典の行に「改変：切出」
    "cr4b": dict(code="CR4B", cuts=("cc16",), box=(0.080, 0.020, 0.920, 0.275), how="学生の頭より上の盤だけ（向きの札 6 を当てたあと）"),
    # 🆕 ⑤b-7（10-23）：c418＝学生の左の盤（ランプと切り替えの並ぶ所）。白衣の左の端は y 0.45 で x 0.40・y 0.62 で x 0.375（1280 幅の目盛りの見本で見た）
    #   ＝x 0.355 より左だけ・上はランプの段の上（y 0.285）・下は机の手前（y 0.615）
    "cr4b2": dict(code="CR4B", cuts=("c418",), box=(0.000, 0.285, 0.355, 0.615), how="学生の左の盤だけ（向きの札 6 を当てたあと・白衣の外）"),
}
# 画面の出典の行の名（個人名義でない点・表示が任意の点の機関）。sources24 の出典の欄の頭（「（」の前）で足りない点だけ
#   R1＝出どころの欄は「RIA Novosti archive」だが、Commons の作者欄はオランダの通信社の撮影者＝オランダ国立公文書館の写真（10-22 に API で読んだ）
ORG = {"P84": "USGS EarthExplorer（アメリカの偵察衛星）", "R1": "オランダ国立公文書館", "C3313": "NASA", "CIA": "CIA"}
LIC = {"CC BY-SA 2.0": "CC BY-SA 2.0", "CC BY-SA 3.0": "CC BY-SA 3.0", "CC BY-SA 4.0": "CC BY-SA 4.0", "CC BY 2.0": "CC BY 2.0",
       "CC BY 3.0": "CC BY 3.0", "CC0": "CC0", "Public domain": "パブリックドメイン", "PD": "パブリックドメイン",
       "Pexels License": "Pexels License", "引用（頁）": "引用（著作権法32条）"}
LIC_URL = {"Pexels License": "https://www.pexels.com/license/"}
# 撮影年の手当て {記号: (年 か None, 出どころ)}＝dto の読みで決まらない点だけ
YEAR_FIX = {
    "I26": (None, "撮影日の欄「before 26 April 1986」・説明「Pripyat before the accident」＝事故の前（年は分からない）"),
    "CIA": (1996, "dto 1996（CIA の地図の版）"),
    # 🆕 ⑤b-7（10-23）：INSAG-7（1992年）の付属書I＝ソ連の委員会の1991年の報告そのもの（英訳が1992年に載った）＝頁の中身の年は1991
    "S1p41": (1991, "INSAG-7 付属書I＝1991年のソ連の委員会の報告（1992年に INSAG-7 に載った）"),
    "S1p63": (1991, "INSAG-7 付属書I の表I-I＝1991年のソ連の委員会の報告（1992年に INSAG-7 に載った）"),
    "S1p65": (1991, "INSAG-7 付属書I の表I-I の続き＝1991年のソ連の委員会の報告（1992年に INSAG-7 に載った）"),
}
# 顔だけモザイク {記号: [(x0, y0, x1, y1, 誰)]}＝⑤b-2（10-22）は0点：人の写る点は BY-SA（額装・無加工＝公的な任務・公人・遠景・背中＝了承② 決め3）
#   と R1（CC0・オランダの公的な測定の職員＝公的な任務）だけ・CR4B の学生は切り出しで外した（CROP）
MASK = {}


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
        if len(f) != 13:
            raise SystemExit(f"🔴 sources24.psv の行の欄が13でない：{ln[:80]}")
        d = dict(zip(["code", "class", "title", "page", "get", "dims", "rights", "basis", "credit", "era", "people", "file", "note"], f))
        out[d["code"]] = d
    return out


def _fetched():
    out = {}
    for ln in FETCH.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if ln.startswith("#") or len(f) < 7 or f[0] == "code":
            continue
        out[f[0]] = dict(zip(["code", "file", "bytes", "dims", "magic", "md5", "twice"], f))
    return out


def _private():
    """git の外の表 {記号: {title, license, author, credit, page}}（行頭 `e24:`）。無ければ止める（束を作る手元だけで読む）"""
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の作者欄の表＝映像方針の make_sources24.py）")
    out = {}
    for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t"):
        if r and r[0].startswith("e24:"):
            out[r[0][4:]] = dict(zip(["title", "license", "author", "credit", "page"], r[1:]))
    return out


def _api():
    return json.loads(API.read_text(encoding="utf-8"))


def uses():
    """{記号: [カット]}（一覧の素材の欄から・写真・頁の静止画だけ＝映像は台帳 clips.json の側）。頁は PAGES_NOW だけ"""
    src = _sources()
    out = {}
    for r in _list():
        c = r["code"]
        s = src.get(c)
        if not s:
            continue
        pdf = "#" in s["file"]
        if (s["class"] == "page" or pdf) and c not in PAGES_NOW:
            continue
        if s["class"] in ("commons", "local", "page"):
            out.setdefault(c, []).append(r["cid"])
    return out


def _kinds(code):
    return {r["kind"] for r in _list() if r["code"] == code}


def related_of(code):
    """一覧の種類「参考」の記号か。同じ記号を「参考」とほかの種類の両方に当てていたら止める（20% の数が揺れる）"""
    k = _kinds(code)
    if "参考" in k and k - {"参考"}:
        raise SystemExit(f"🔴 {code}: 一覧の種類が「参考」と {sorted(k - {'参考'})} に割れる（20% の数が決まらない）")
    return k == {"参考"}


def page_of(code, s):
    """頁（写真に数えない）＝出どころが頁・一覧の種類が「頁」だけ（CIA の地図・USGS の図12）。割れたら止める"""
    k = _kinds(code)
    if "頁" in k and k - {"頁"}:
        raise SystemExit(f"🔴 {code}: 一覧の種類が「頁」と {sorted(k - {'頁'})} に割れる")
    return s["class"] == "page" or k == {"頁"}


def names_of(code):
    """記号 → [(束の名, 切り出しの dict か None, カット)]"""
    crops = [(n, c) for n, c in CROP.items() if c["code"] == code]
    if crops:
        return [(n, c, list(c["cuts"])) for n, c in crops]
    return [(code.lower().replace("+", "_"), None, None)]


# ── 頁 ─────────────────────────────────────────────────────────
def _pdf_of(s):
    f = s["file"].split("+")[0] if s["code"] in PAGE_FIRST else s["file"]
    m = re.fullmatch(r"(.+\.pdf)#(\d+)", f)
    if not m:
        raise SystemExit(f"🔴 {s['code']}: 頁の欄が「<pdf>#<頁>」でない（{s['file']}）")
    return HERE / m.group(1), int(m.group(2))


def render_page(code, s):
    """頁（PDF の1頁）を長辺 PAGE_LONG で描き、インクの外接（四辺 24px の余白）で切る＝(RGB の PIL 画像, 記録の dict)"""
    import numpy as np
    from PIL import Image
    if code in PAGE_IMAGE:
        # 🆕 ⑤b-7：国会会議録の頁＝手元の画像（PDF でない）。md5 は取得の記録と照らす（違えば止める）
        rel, why = PAGE_IMAGE[code]
        p = HERE / rel
        f = next((r for r in FETCH.read_text(encoding="utf-8").splitlines() if r.split("\t")[:2] == [code, rel]), None)
        if not f or f.split("\t")[5] != md5(p):
            raise SystemExit(f"🔴 {code}: {rel} の md5 が fetch24.tsv と合わない（取り直す）")
        im = Image.open(p).convert("RGB")
        k, rec0 = 1.0, dict(img=rel, img_md5=md5(p), how=f"手元の画像（{why}）・インクの外接")
    else:
        import fitz
        pdf, no = _pdf_of(s)
        d = fitz.open(pdf)
        pg = d[no - 1]
        k = PAGE_LONG / max(pg.rect.width, pg.rect.height)
        pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), alpha=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        rec0 = dict(pdf=pdf.relative_to(HERE).as_posix(), pdf_page=no, pdf_md5=md5(pdf), how=f"PDF の頁を描いた（長辺 {PAGE_LONG}px）・インクの外接"
                    + (f"・「+」の先の頁だけ（{PAGE_FIRST[code]}）" if code in PAGE_FIRST else ""))
    a = np.asarray(im.convert("L"))
    h, w = a.shape
    m = int(min(h, w) * 0.01)               # 走査の縁の影（端の 1% の暗い帯）は外接に入れない
    ys, xs = np.where(a[m:h - m, m:w - m] < 160)
    box = (max(0, xs.min() + m - 24), max(0, ys.min() + m - 24), min(w, xs.max() + m + 24), min(h, ys.max() + m + 24))
    rec = dict(rec0, scale=round(k, 5), box_px=[int(v) for v in box])
    return im.crop(box), rec


def cmd_pbox(code, head, tail, pad=18):
    """頁の字の層で、head を含む最初の行から tail を含む行までの箱＝束の絵の割合 (x0, y0, x1, y1)。章ファイルの trim に写す値"""
    import fitz
    db = json.loads(DB.read_text(encoding="utf-8"))
    rec = next((r for r in db.values() if r["code"] == code), None)
    if not rec or "src_rec" not in rec:
        raise SystemExit(f"🔴 {code} は束に頁として無い（build を先に）")
    sr = rec["src_rec"]
    pg = fitz.open(HERE / sr["pdf"])[sr["pdf_page"] - 1]
    lines = []
    for b in pg.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            t = "".join(s["text"] for s in ln["spans"]).strip()
            if t:
                lines.append((t, ln["bbox"]))
    i0 = next((i for i, (t, _) in enumerate(lines) if head in t), None)
    if i0 is None:
        raise SystemExit(f"🔴 {code}: 「{head}」の行が無い")
    i1 = next((i for i in range(i0, len(lines)) if tail in lines[i][0]), None)
    if i1 is None:
        raise SystemExit(f"🔴 {code}: 「{head}」より後に「{tail}」の行が無い")
    sel = lines[i0:i1 + 1]
    k, (bx, by, _, _) = sr["scale"], sr["box_px"]
    sx0, sx1 = min(b[0] for _, b in sel), max(b[2] for _, b in sel)
    top, bot = min(b[1] for _, b in sel), max(b[3] for _, b in sel)
    # 🔴 ⑤b-2（10-22）：上下は**行と行のすき間の真ん中**で切る（行の箱に余白を足すと、行間の詰まった頁は隣の行の字の頭まで入る＝c104 の
    #    初めの切り口で9行目の頭が額の下の辺に帯で見えた・門番 edges は OCR の箱で 7.5%＜下限 8% を「外」と数えて通した）
    over = [b for _, b in lines if b[0] < sx1 and b[2] > sx0]
    above = [b[3] for b in over if b[3] <= top + 1 and b[1] < top - 1]
    below = [b[1] for b in over if b[1] >= bot - 1 and b[3] > bot + 1]
    yt = (max(above) + top) / 2 if above else top - pad / k
    yb = (min(below) + bot) / 2 if below else bot + pad / k
    x0, x1 = sx0 * k - bx - pad, sx1 * k - bx + pad
    y0, y1 = yt * k - by, yb * k - by
    w, h = rec["w"], rec["h"]
    box = [max(0.0, x0 / w), max(0.0, y0 / h), min(1.0, x1 / w), min(1.0, y1 / h)]
    print(f"{code}: 行 {i0}〜{i1}（{len(sel)}行）「{sel[0][0][:40]}」〜「{sel[-1][0][-40:]}」")
    # 🔴 PDF の字の層（走査に重ねた OCR）は絵の行と数 px ずれる（c104＝字の層の行の下の端が絵の次の行の頭より下）＝上下の辺は
    #    **束の絵の OCR**（ref/ep24/ocr_slides.json＝門番 edges・slide と同じ読み置き）の行の箱で、行と行のすき間の真ん中に寄せ直す
    name = next(n for n, r in db.items() if r["code"] == code)
    o = (json.loads((EPD / "ocr_slides.json").read_text(encoding="utf-8")).get(f"{name}.jpg")
         if (EPD / "ocr_slides.json").exists() else None)
    if not o:
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
    # すき間の中で**インクがいちばん少ない行**（13本目の教え・束の絵の画素＝OCR の箱は字の頭より下に来ることがある）
    import numpy as np
    from PIL import Image
    ink = (np.asarray(Image.open(EPD / f"{name}.jpg").convert("L"))[:, int(L):int(R)] < 160).sum(axis=1)

    def calm(a, b):
        a, b = int(a), int(b)
        if b <= a:
            return (a + b) / 2
        seg = ink[a:b + 1]
        lo = seg.min()
        idx = np.where(seg == lo)[0]
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


def _auto_box(im, box, thr=24, inset=6):
    """box（割合）の中で、暗い地（輝度の平均 thr 以下の行・列）を外した外接＝画素の箱。欄の写真の黒い枠を画素で外す"""
    import numpy as np
    w, h = im.size
    x0, y0, x1, y1 = (round(box[0] * w), round(box[1] * h), round(box[2] * w), round(box[3] * h))
    a = np.asarray(im.convert("L").crop((x0, y0, x1, y1)), dtype=np.float32)
    rows = np.where(a.mean(axis=1) > thr)[0]
    cols = np.where(a.mean(axis=0) > thr)[0]
    if not len(rows) or not len(cols):
        raise SystemExit("🔴 切り出しの窓に明るい行・列が無い（box を確かめる）")
    return (x0 + cols[0] + inset, y0 + rows[0] + inset, x0 + cols[-1] + 1 - inset, y0 + rows[-1] + 1 - inset)


def load_photo(s, crop=None):
    """元の写真を読む（向きの札を当て・sRGB に・切り出し）＝(絵, 記録の言葉の並び, 切り出しの画素の箱)"""
    from PIL import Image, ImageOps
    sp = HERE / s["file"]
    notes, px = [], None
    dec = (crop or {}).get("decode", 1)
    if dec > 1:
        Image.MAX_IMAGE_PIXELS = None           # 偵察衛星の写真の原本（21634×16500）＝JPEG の draft で 1/dec に縮めて読む（全部を読むと約1GB）
    with Image.open(sp) as im0:
        full = im0.size
        if dec > 1:
            im0.draft("RGB", (full[0] // dec, full[1] // dec))
            notes.append(f"原本 {full[0]}x{full[1]} を 1/{dec} で読んだ（{im0.size[0]}x{im0.size[1]}）")
        ori = im0.getexif().get(274)
        im = ImageOps.exif_transpose(im0)
        if ori and ori != 1:
            notes.append(f"EXIF の向き {ori} を当てた（生の絵 {im0.size[0]}x{im0.size[1]}）")
        im.info["icc_profile"] = im0.info.get("icc_profile")
        im, how_c = _to_srgb(im)
    notes.append(how_c)
    if crop:
        w, h = im.size
        b = crop["box"]
        px = _auto_box(im, b) if crop.get("auto") else (round(b[0] * w), round(b[1] * h), round(b[2] * w), round(b[3] * h))
        im = im.crop(px)
        notes.append(f"切り出し {crop['how']}（{px[2] - px[0]}x{px[3] - px[1]}）")
    return im, notes, px


def mosaic(im, boxes, n):
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）＝16・17・20・23本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def name_mode(code, s, priv):
    """出典の行の名乗りの型：none（表示が任意＝CC0・PD）・org（機関だけ）・name（作者欄の名前だけ）・org+name（機関／作者欄の名前）。
    🔴 「撮影者は作者欄のとおり」でも作者欄が空の点（IAEA Imagebank の6点＝Commons の作者欄が機関名だけ）は org"""
    if code in ORG or s["class"] == "page":
        return "org"
    if s["rights"] in NO_NAME:
        return "none"
    cr = s["credit"]
    pv = priv.get(code, {})
    if cr.startswith("写真：作者欄のとおり"):
        return "name"               # 作者欄が空なら Flickr の投稿者の ID（scene_jiko._ep24_author）＝C3309
    # ⚠️ 機関つきの点は作者欄の名前だけで決める（IAEA Imagebank の6点の出典の欄は IAEA の Flickr の頁＝ID を名乗りにしない）
    if "作者欄のとおり" in cr and (pv.get("author") or "").strip():
        return "org+name"
    return "org"


def who_screen(code, s, priv):
    """出典の行の「写真：○○」の○○。名前は印 AUTHOR だけ（焼くときに足す）"""
    if code in ORG:
        return ORG[code]
    mode, cr = name_mode(code, s, priv), s["credit"]
    if cr.startswith("写真：作者欄のとおり"):
        return AUTHOR if mode == "name" else "Wikimedia Commons"
    org = cr.split("（", 1)[0]
    return f"{org}／{AUTHOR}" if mode == "org+name" else org


def screen_credit(code, s, priv, frame, crop, mask):
    """画面の出典の行。🔴 CC BY・BY-SA は必ず「改変」の語を書く＝`scene_jiko.credit_of` の古い決まり（6本目）が「CC BY」があって「改変」の
    語が無い行に「／改変：色調変更・切出」を黙って足す（23本目 ⑤b-2 の試し焼きで出た）"""
    if s["class"] == "page":
        return PAGE_CREDIT.get(code, s["credit"])
    r = s["rights"]
    lic = LIC[r]
    who = who_screen(code, s, priv)
    if code == "CIA":
        return f"出典：{who}（{lic}）"     # 🔧 ⑤c'：地図＝写真ではない（図の頁の出典の行と同じ「出典：」）
    if r in NO_NAME:
        return f"写真：{who}（{lic}）" + ("・改変：切出" if crop else "")
    if frame:
        return f"写真：{who}（{lic}）・改変なし"
    return f"写真：{who}（{lic}）・改変：切出" + ("・顔にモザイク" if mask else "")


def who_table(code, s, priv):
    """CREDITS.md の撮影者の欄（名前は書かない）"""
    if s["class"] == "page":
        return s["credit"].removeprefix("出典：")
    w = who_screen(code, s, priv)
    if AUTHOR in w:
        return w.replace(AUTHOR, "作者欄のとおり") + "（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`）"
    if s["rights"] in NO_NAME and w == "Wikimedia Commons":
        return "Commons の投稿者（CC0・PD＝表示は任意）"
    return w


_DTO_YEAR = re.compile(r"(1[89]\d\d|20\d\d)")


def year_of(code, s, api):
    if code in YEAR_FIX:
        return YEAR_FIX[code]
    if s["class"] == "page" or "#" in s["file"]:
        k = code[:2]
        if k not in PAGE_YEAR:
            raise SystemExit(f"🔴 {code}: 頁の資料の年が表 PAGE_YEAR に無い")
        return PAGE_YEAR[k]
    if s["class"] == "local":
        return 1986, "Landsat 5 の1986年4月22日・29日（掲示の字）"
    a = api.get("File:" + s["title"])
    if not a:
        raise SystemExit(f"🔴 {code}: api24.json に {s['title']} が無い（撮影日が分からない）")
    dto = a.get("dto", "")
    m = _DTO_YEAR.search(dto)
    if not m:
        return None, f"撮影日の欄「{dto}」に年が無い"
    y = int(m.group(1))
    if "USFCRFC" in s["credit"] and y in (2005, 2006):
        return None, f"撮影日の欄「{dto}」＝取り込みの日（IAEA 0279 の組・説明に年が無い＝10-22 に Commons の説明を読んだ）"
    return y, f"Commons の撮影日の欄「{dto}」"


# ── 束を作る ─────────────────────────────────────────────────
def cmd_build():
    src, fet, priv, api = _sources(), _fetched(), _private(), _api()
    db, bad = {}, 0
    us = uses()
    for code in CROP.values():
        if code["code"] not in us:
            print(f"🔴 CROP の {code['code']} は一覧で使っていない")
            bad += 1
    for code, cuts in sorted(us.items()):
        s = src[code]
        nm = names_of(code)
        crop_cuts = sorted(c for _, cr, cs in nm if cr for c in cs)
        if nm[0][1] and sorted(set(crop_cuts)) != sorted(set(cuts)):
            print(f"🔴 {code}: 切り出しのカット {crop_cuts} と一覧のカット {cuts} が合わない")
            bad += 1
            continue
        rel, pg_ = related_of(code), page_of(code, s)
        for name, crop, ccuts in nm:
            dst = EPD / f"{name}.jpg"
            rec = {}
            if s["class"] == "page" or "#" in s["file"]:
                im, rec = render_page(code, s)
                notes = [rec["how"]]
                smd5 = rec.get("pdf_md5") or rec["img_md5"]
            else:
                f, sp = fet.get(code), HERE / s["file"]
                if not f or not sp.exists():
                    print(f"🔴 {code}: fetch24.tsv の行か手元のファイルが無い（{s['file']}）")
                    bad += 1
                    continue
                if md5(sp) != f["md5"]:
                    print(f"🔴 {code}: {sp.name} の md5 が取得のときと違う（取り直す）")
                    bad += 1
                    continue
                smd5 = f["md5"]
                im, notes, _px = load_photo(s, crop)
                im, k = _shrink(im)
                if k < 1.0:
                    notes.append(f"縮小 ×{k:.3f}")
            box_m = []
            if code in MASK:
                box_m = MASK[code]
                im = mosaic(im, box_m, MOSAIC_PX)
                notes.append(f"顔だけモザイク {len(box_m)}か所（升 {MOSAIC_PX}px）")
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
            mode = name_mode(code, s, priv)
            pv = priv.get(code, {})
            if mode == "name" and not ((pv.get("author") or "").strip() or _flickr_id(pv)):
                print(f"🔴 {code}: 個人名義なのに git の外の表に作者欄が無い")
                bad += 1
            frame = s["rights"].startswith(FRAME_RIGHTS)
            if frame and crop:
                print(f"🔴 {code}: 継承つき（{s['rights']}）を切り出している（額装だけ・無加工）")
                bad += 1
            y, ywhy = year_of(code, s, api)
            lic = LIC.get(s["rights"])
            if not lic:
                print(f"🔴 {code}: 権利の記号が読めない（{s['rights']}）")
                bad += 1
                continue
            cuts_here = ccuts or cuts
            db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(cuts_here),
                            credit=screen_credit(code, s, priv, frame, bool(crop), bool(box_m)),
                            who=who_table(code, s, priv), note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                            md5=md5(dst), src_md5=smd5, lic=lic, frame=frame, ground=s["rights"], url=s["page"] or s["file"],
                            blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False, page=pg_, related=rel, quote_page=s["class"] == "page",
                            named=mode in ("name", "org+name"), mosaic=[list(b[:4]) for b in box_m] or None, masked_before=None,
                            era=s["era"], people=s["people"], **({"src_rec": rec} if rec else {}))
            print(f"✓ {code:7} {name:11} {w}x{h:<5} {' '.join(cuts_here):10} {lic}{'  額装だけ' if frame else ''}{'  参考' if rel else ''}"
                  f"{'  頁' if pg_ else ''}  {'・'.join(notes)[:90]}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    print(f"→ ref/ep24/assets.json（{len(db)}点・額装だけ {sum(1 for r in db.values() if r['frame'])}・参考 {sum(1 for r in db.values() if r['related'])}"
          f"・頁 {sum(1 for r in db.values() if r['page'])}・名前を足す点 {sum(1 for r in db.values() if r['named'])}"
          f"・モザイク {sum(1 for r in db.values() if r['mosaic'])}・束の大きさ {tot / 1e6:.1f}MB）")
    return 1 if bad else 0


def _flickr_id(pv):
    """作者欄が空で、出典の欄が Flickr の投稿者の頁（名前の無い ID だけ）のとき、その ID の形があるか（値は返さない＝名前の扱い）"""
    return bool(re.search(r"flickr\.com/photos/[^/\s]+", pv.get("credit") or ""))


def cmd_look(codes, out_name="look.jpg", width=960):
    """束の写真を並べた見本（2列）＝リポの外（SCRATCH）。記号（I15）か束の名（u1_0422）を渡す"""
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
        m = PE.margins(f"ep24/{n}.jpg")
        mx = max(m.values())
        flag = "🔴" if mx >= PE.MIN_EDGE else ("・" if mx > 0 else " ")
        if mx > 0:
            hits.append((n, m))
        print(f"{flag} {n:30} 左 {m['l'] * 100:4.1f}% 上 {m['t'] * 100:4.1f}% 右 {m['r'] * 100:4.1f}% 下 {m['b'] * 100:4.1f}%")
    big = [n for n, m in hits if max(m.values()) >= PE.MIN_EDGE]
    print(f"→ 暗い帯のある点 {len(hits)}（うち {PE.MIN_EDGE * 100:.1f}% 以上 {len(big)}＝{' '.join(big) or 'なし'}）")
    return 0


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
# 出典の行の字幅の上限の目安（全角＝1・半角＝0.55）＝23本目の写真の出典の行で門番 layout を通って公開された最長 56.5
#   （ソウル研究院の CC BY 4.0・顔にモザイク）。17本目の FAA の頁の 68 も通った。本当の物差しは門番 layout（写真のカットを書いたら測る）
CREDIT_W_MAX = 56.5


def _width(s):
    import unicodedata
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.55 for c in s)


def cmd_credits(write=False):
    """撮影年＝year_of（出どころつき）。当てたカットの副題が名乗る年（「NNNN年」・「当日」＝1986）と食い違えば止める。
    名前の短い形（scene_jiko._ep24_short）を作者の表の全行に当て、長すぎ・字の崩れを止める（名前は出さない＝字数だけ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import scene_jiko as SJ
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    priv = _private()
    names = set()
    for v in priv.values():
        a = (v.get("author") or "").strip()
        if a:
            names |= {a, SJ._ep24_short(a)}
            names |= {x for x in re.split(r"[\s/()]+", a) if len(x) >= 4 and x[0].isupper()}
    cj, rows, bad = {}, [], 0
    for n, r in sorted(db.items()):
        cuts = r["cut"].split()
        claims = set()
        for c in cuts:
            # 「1980年代」「1986年ごろ」は撮影年の主張でない（check_credits と同じ）
            claims |= {int(y) for y in re.findall(r"(1[89]\d\d|20\d\d)年(?!代|ごろ)", subs.get(c, ""))}
            if "当日" in subs.get(c, ""):
                claims.add(EVENT_YEAR)
        y = r["year"]
        if claims and (y is None or claims != {y}) and not r["page"]:
            print(f"🔴 {n}: 副題の年 {sorted(claims)} と撮影年 {y} が食い違う（{' '.join(cuts)}・{subs.get(cuts[0], '')}）＝{r['year_why'][:60]}")
            bad += 1
        leak = [x for x in names if x and x in json.dumps(r, ensure_ascii=False)]
        if leak:
            print(f"🔴 {n}: 台帳の行に作者の名前が入っている（{len(leak)}語）＝名前は印 {AUTHOR} で")
            bad += 1
        if AUTHOR in r["credit"]:
            try:
                who = SJ._ep24_author(f"ep24/{n}.jpg")
            except Exception as e:                         # noqa: BLE001  焼く前に止める
                print(f"🔴 {n}: 作者の名乗りが作れない（{e}）")
                bad += 1
            else:
                line = r["credit"].replace(AUTHOR, who)
                wd = _width(line)
                if wd > CREDIT_W_MAX:
                    print(f"🔴 {n}: 出典の行の字幅 {wd:.1f}（{CREDIT_W_MAX} まで＝画面の左下からはみ出すおそれ）")
                    bad += 1
        cj[f"ep24/{n}.jpg"] = r["credit"]
        mod = "・顔にモザイク" if r.get("mosaic") else ""
        kind = "頁" if r["page"] else ("参考" if r["related"] else "この事故")
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
        "※2026-10-22（⑤b-2）。`qa_out/ep24_assets.py credits --write` が書く（手で直さない）。写真と映像は映像方針の一覧 `ref/ep24/eizou_list24.md`（了承② 2026-10-22）。",
        "",
        "### 0. 映像（フリー素材＝音はすべて使わない＝`-an`）",
        "- フリー素材（Pexels・生成AI は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」だけ"
        "（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）",
        "",
        "| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |",
        "|---|---|---|---|---|", *film_rows, "",
        "### 1. 写真・頁（IAEA Imagebank・Commons・USGS・報告書と会議録の頁）",
        "- 🔴 **CC BY-SA は額装だけ**（了承② 決め4＝無加工・額ごと動かす・1点1カット＝`cuts/ss.check_frame_only`）。IAEA 0279 の34点は全部 CC BY-SA 2.0",
        "- 🔴 **個人名義の点は画面の出典の行に作者欄の名前**。名前はこのリポに書かない＝`ref/ep24/credits.json` は印 `{作者}` だけ・焼くときに"
        " git の外の表から足す（`tools/scene_jiko.ep24_credit`・名乗りの短い形＝`_ep24_short`）。CC0・PD は表示が任意＝名前を出さない",
        "- 「参考」＝この事故の物ではない実物（同じ型の炉＝レニングラード・クルスク・イグナリナ）＝20% の数（この事故の写真）に入れない",
        "- 報告書・会議録の頁＝引用（著作権法32条＝無加工・出典）。頁は使う章のチャットで足す（⑤b-2 は c104 の INSAG-7 p.34 だけ）",
        "- 撮影年＝Commons の撮影日の欄。IAEA 0279 の組の多くは欄が取り込みの日（2005・2006年）で説明に年が無い＝「不明」（副題に年を書かない）",
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


# ── 映像（フリー素材）：台帳・ショット・見取り図・USE・ひかえ ──────────────
def _film_codes():
    """映像の記号 → 使うカット（一覧の順）"""
    src = _sources()
    out = {}
    for r in _list():
        s = src.get(r["code"], {})
        if s.get("class") == "stock":
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


def _media_url(code, loc, size):
    """Pexels の置き場の直リンク（fetch24.py の当て方と同じ形）を HEAD で当て、大きさが手元と同じ版を返す（違えば止める）"""
    pid = code[1:]
    label = {1920: "hd_1920_1080", 2560: "uhd_2560_1440", 3840: "uhd_3840_2160"}.get(loc["w"])
    if not label:
        raise SystemExit(f"🔴 {code}: 幅 {loc['w']} の版の名の形が分からない")
    fps0 = round(loc["fps"])
    for fps in [fps0] + [f for f in (30, 25, 24, 60, 50) if f != fps0]:
        u = f"https://videos.pexels.com/video-files/{pid}/{pid}-{label}_{fps}fps.mp4"
        try:
            req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                n = int(r.headers.get("Content-Length") or 0)
                if r.status == 200 and n == size:
                    return u
                if r.status == 200:
                    print(f"  {code}: {u.rsplit('/', 1)[-1]} は {n} B（手元 {size} B）＝別の版")
        except Exception:                                    # noqa: BLE001  形が違えば 403/404＝次の形
            pass
    raise SystemExit(f"🔴 {code}: 手元と同じ大きさの直リンクが見つからない（{size} B）")


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
        size = p.stat().st_size
        media = _media_url(code, loc, size)
        lic = LIC[s["rights"]]
        e = dict(url=s["page"], media=media, stock=True, file=s["file"].removeprefix("ref/"), credit="イメージ（Pexels）", src="stock",
                 at=0.0, what=s["note"][:60], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(loc["sec"], 3),
                 size=size, md5=f["md5"], dispw=loc["w"], decoded=[loc["w"], loc["h"]], license=lic, license_url=LIC_URL[lic], site="Pexels")
        out[code] = e
        print(f"  {code:10} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.2f}秒  {' '.join(cuts):12} {media.rsplit('/', 1)[-1]}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep24/clips.json（{len(out)}本）")
    return 0


# 🔴 動きの速い素材は、隣の1秒の差がしきい値を超えて「境目」が出る（18本目 0b-45⑥・23本目の SHOT_ONE）＝根拠つきで1ショットに直す
#   🆕 ⑤b-7（10-23）：X12191470（c621）＝3秒の境目。全コマ（25コマ/秒・160×90 の灰色）の隣のコマとの差は中央値 8.5・大きい順に
#      3.60秒 16.1・3.52秒 15.6・3.64秒 15.4・3.32秒 15.4＝1コマだけ跳ねる所が無い（切り替わりなら1コマに集まる）＝空撮の速い動きの続き
#      ＝⑤b-1 の 0.83倍（素材まるごと 6.0秒）のまま。⚠️ 絵は試し焼きのコマで目で確かめる
SHOT_ONE = {
    "X12191470": "3秒の境目の前後の全コマの差を測った＝跳ねる1コマが無い（最大 16.1・中央値 8.5・3.3〜3.6秒に散る）＝空撮の速い動きの続き",
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
        how = "1秒1コマで tools/shots.shots_of（2026-10-22 ⑤b-2・フリー素材）"
        if code in SHOT_ONE:
            sh = [dict(start=0.0, until=float(sh[-1]["until"]), motion=max(x["motion"] for x in sh))]
            how += f"・🔧 1ショットに直した（{SHOT_ONE[code]}）"
        out[code] = dict(src=s["page"], scan=s["file"], dur=round(dur, 1), how=how, shots=sh)
        print(f"  {code:10} {dur:6.1f}秒  ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep24/shots.json（{len(out)}本）")
    return 0


def cmd_frames(code, step=1.0, width=384, cols=5):
    """映像の step 秒ごとのコマを並べた見取り図（秒の札つき）＝区間を選ぶとき（out/ep24_look/frames_<記号>.jpg）"""
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
    txt = FOOTAGE.read_text(encoding="utf-8")
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_text(txt[:m.start(2)] + "".join(x + "\n" for x in lines) + txt[m.end(2):], encoding="utf-8")


# 🆕 ⑤b-2（10-22）：フリー素材の映像の区間 {cid: (始め, 終わり, 理由)}＝1秒ごとの見取り図（frames）と shots.json の境目を見て決めた。
#   書いていないカットは「要る秒が等速で入るショットのうち、いちばん長いショットの真ん中」（23・17本目の pick の型）
#   地平線の帯を原寸で見た（scratchpad の horizon_*.jpg）＝X13188726 は全時刻で左の地平線に新しい覆いと排気筒が写る（ショット 0〜15・15〜25）／
#   X13188723 は2・8・14・20秒のどれにも覆いが写らない（プリピャチの団地だけ・1ショット 0〜22）
STOCK_WINDOW = {
    "c101": (3.00, 11.45, "X13188726 の前のショット（覆いと排気筒が左の地平線）"),
    "cb23": (17.00, 20.45, "X13188726 の後のショット（覆いが写る＝⑤b-2 で X13188723 から移した）"),
    "c927": (0.30, 9.00, "X13188723 の前（覆いの写らない団地）"),
    "cc20": (9.60, 21.70, "X13188723 の後ろ（30560421 の代わり・覆いの写らない団地）"),
    # 🆕 ⑤b-7（10-23）：素材まるごとの1ショット＝頭と尻はショットの境目でない（STOCK_EDGE で削ると 0.76倍まで遅くなる）。
    #   ⚠️ 台帳の長さ 6.0秒は丸め＝試し焼き 39912142820 で c621 がコマ 205/213（8コマ足りず静止画に落ちた）・cb22 が 208/210
    #   ＝実の長さは約 5.77秒・約 5.94秒（コマ数から逆算）→ 終わりを 5.76秒・5.85秒に
    "c621": (0.00, 5.76, "X12191470 まるごと（1ショット＝SHOT_ONE・実の長さ約 5.77秒）"),
    "cb22": (0.00, 5.85, "X13183773 まるごと（1ショット・実の長さ約 5.94秒）"),
}
STOCK_GEOM = {}
STOCK_EDGE = 0.3                # ショットの境目から離す秒（フリー素材＝1秒1コマで測った境目＝23・17本目と同じ）


def cmd_use(only=None, all_=False):
    """footage.USE の24本目の欄（🔴 章ファイルに `ss.vid` を書いたカットだけ＝門番 slots は両側を見る・`only` は書く前の鶏と卵を割るため）。
    フリー素材＝STOCK_WINDOW の区間か、いちばん長いショットの真ん中。rate＝使える秒÷要る秒（切り捨て・1.0 まで）"""
    sys.path.insert(0, str(HERE / "tools"))
    if only:
        # 鶏と卵：`ss.vid` は章ファイルの読み込みの時点で USE の欄を読む＝名指しのときは章ファイルを読まず、一覧の cont（扉を除いた中身の秒
        #   ＝footage.secs_of と同じ値・カットまるごとの映像）で書く。書いたあと名指しなしの `use` で同じ行になるかを照らす
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
    _write_block("EP24_USE", lines)
    print(f"→ tools/footage.py USE {len(lines)}欄")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）＝USE の start の1コマを焼くときと同じ切り口（全画面・寄り）で 1920×1080
    → ref/ep24/stock/fb_<cid>.jpg（🔴 git に入れない＝決め⑨。Actions では footage.fetch が切り出したコマの1枚目から作る）"""
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
        print(f"✓ {cid:5} {u['clip']:10} {float(u['start']):6.2f}秒 {sw}x{sh_} → {dst.relative_to(HERE).as_posix()}")
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
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
