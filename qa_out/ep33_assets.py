# -*- coding: utf-8 -*-
"""ep33_assets.py — 33本目（グレンフェルタワー火災）の写真の束・出典・#15 の台帳（⑤b-2・2026-11-15）。32本目 `ep32_assets.py` の写し。
32本目の NTSB のドケットの調査の写真・管制の録音・連邦官報の枝は外した（33本目に無い）。33本目の素材＝`sources33.psv` の13列・`fetch33.tsv`〈md5 を2回〉・
git の外の表 `src/credits_private.tsv`〈Commons の撮影者＝頭の行なし・🆕 **4列＝code・author・lic・頁の URL**＝32本目の9列と違う〉。
束に入れるのは Commons の写真（commons-photo）と公開調査の報告の図（紙面＝`PAGE_CUT` に書いたカットだけ＝⑤b-2 は冒頭の夜の図4つ・残りの34は ⑤b-3）。
文字の頁（一覧の「公的」34カット）は ⑤b-3b・イメージ（Pexels）は ⑤b-4＝束に入れない（数えて出すだけ）。#15（Commons の映像 GRENFELL.webm）は clips.json・shots.json。

  python -P qa_out/ep33_assets.py uses             # 束の鍵とカット（主・地）
  python -P qa_out/ep33_assets.py build            # 束 ref/ep33/<名>.jpg ＋ 権利の台帳 ref/ep33/assets.json
  python -P qa_out/ep33_assets.py sheet <名…>      # 1枚 640幅の 2列×3行のシート（out/ep33_look/・人の写りを当たる＝事故検証ch の決め）
  python -P qa_out/ep33_assets.py crop <名> x0 y0 x1 y1 [倍]   # 束の画素の切り出し（既定2倍・10px の目盛り）＝人と字を決めるとき
  python -P qa_out/ep33_assets.py panel｜edges     # ss.PANEL_AR の切れ目／門番 check_photo_edge の名簿（SLIDE_MOUNT／SLIDE_NOT_MOUNT）＝ひかえの静止画も測る
  python -P qa_out/ep33_assets.py credits [--write]  # 画面の出典 ref/ep33/credits.json と ref/CREDITS.md の33本目の節
  python -P qa_out/ep33_assets.py clips｜shots     # #15 の台帳（HEAD で大きさを照らす）・場面の切れ目（make_list33.SCENE_CUTS を写す＝測り直さない）
  python -P qa_out/ep33_assets.py use [cid…|--all] # footage.USE の33本目の欄（一覧の動きの欄「映像 a〜b秒」から・等速）と NOGO（make_list33.EXCLUDE）
  python -P qa_out/ep33_assets.py fb [cid…]        # ひかえの静止画 ref/ep33/fb_<cid>.jpg（区間の頭のコマ・1920×1080・CC BY 3.0＝公開リポに置く）

🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色・[21]・[23]・[24]・[25] は白黒の原本）＝幅 2400 か高さ 1350 の大きい方まで（小さい写真は原画のまま）。
🔴 報告の図＝PDF の頁を描いて、図の番号と題の行（「Figure n.n」）ごと切る（紙面の引用・額装・無加工）。埋め込みの絵だけを抜かない。
🔴 この回の線（台本 §1-4）＝住民・消防士・社員・専門家・撮影者の名前は出さない（人数・立場・役職だけ）＝写真の中の名札・車の番号の字は読ませない
   （親が原寸で見て升目）。名前は台帳・出典の行・CREDITS.md に書かない＝撮影者は印 `{作者}` だけ（焼くときに `scene_jiko._ep33_person` が
   git の外の表の2列目〈番号1〉から足す）。追悼の場と支援の掲示は使わない（[59]・[60] は外した・[58] は下の追悼の壁を切る）。
🔴 人（了承②）＝公的な任務の顔はそのまま。私人の顔は CC BY・CC0 で升目（MASK）・**BY-SA は升目も翻案＝かけない**（読める顔があれば別の点に）。
⚠️ 権利の読みは法律の助言ではない＝こちらの読み。
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
EPD = HERE / "ref" / "ep33"
SRC = EPD / "src"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list33.tsv"
SOURCES = BUILD / "sources33.psv"
FETCHES = (BUILD / "fetch33.tsv",)
PRIVATE = SRC / "credits_private.tsv"         # 🔴 git の外（Commons の撮影者＝頭の行なし・4列＝code・author・lic・頁の URL）＝ここから名前を公開の物へ写さない
PRIVATE_COLS, AUTHOR_COL, PAGE_COL = 4, 1, 3  # 🔴 33本目の列（scene_jiko._EP33_PRIVATE の番号 1 と同じ）＝違えば止める
NAME_FILES = (SRC / "names_private.txt", SRC / "names_commons.txt")     # 🔴 git の外（出さない名前＝住民・消防士・社員・専門家・証人・撮影者ほか）
COMMONS_PAGES = SRC / "commons" / "html"      # 🔴 git の外（映像方針で取った Commons の頁の写し「File_<題>.html」＝許諾の箱の「Attribution:」を照らす）
COMMONS_DIR = SRC / "commons" / "c33"         # git の外（Commons の写真の原本・標準の縮小版）
CAND = SRC / "commons" / "cand33.json"        # 🔴 git の外（映像方針の Commons の候補の表＝撮影者の名前を含む＝丸ごと表示しない）
DB = EPD / "assets.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
FOOTAGE = HERE / "tools" / "footage.py"
UA = "zukai-engine-research/1.0 (GitHub torotorotolo/zukai-engine)"
SCRATCH = HERE / "out" / "ep33_look"          # sheet・crop の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## グレンフェルタワー火災（2017-06-14・33本目）"
AUTHOR = "{作者}"            # CC BY・BY-SA・CC0 の出典の行の印（焼くときに git の外の表の2列目〈番号1〉から足す＝scene_jiko.ep33_credit）
EVENT_YEAR = 2017            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 92
MOSAIC_PX = 14                         # 升目の大きさ（束の画素）
COMMONS_TYPES = ("commons-photo",)     # Commons の写真（2017-06-14 の夜明け〜2024年の覆われた塔＝CC BY 2.0・CC BY 4.0・BY-SA 2.0／4.0・CC0）
FIG_TYPES = ("report-fig",)            # 公開調査の報告の図（紙面の引用＝OGL v3.0・第三者のコマや図を含む）＝PAGE_CUT に書いたカットだけ束に入れる
PHOTO_TYPES = COMMONS_TYPES
PAGE_TYPES = FIG_TYPES                 # 紙面（頁を描いて切る＝render_page）
STOCK_TYPES = ("stock",)               # 束に入れない（⑤b-4）
FILM_TYPES = ("commons-video",)        # #15＝clips.json（束の外）
KIND_OK = {"写真": COMMONS_TYPES, "紙面": FIG_TYPES}
KIND_OUT = ("映像", "衛星", "イメージ", "公的")     # 束の外＝映像は clips.json・衛星は ss.SAT（⑤b-3）・イメージは ⑤b-4・文字の頁（公的）は ⑤b-3b
_YEAR = re.compile(r"((?:19|20)\d\d)")

# 帰属の指定（許諾の箱の「Attribution: …」）＝ATTR_HEAD＋表の2列目〈作者〉＋ATTR_TAIL と1字も同じか（`build` が頁の写しと照らす）。
#   🆕 ⑤b-2（11-15）：geograph の2点は「〈写真の題〉 by 〈作者〉」の指定（CC BY-SA 2.0 の「題が示されていれば題も」）＝画面の出典の行も題ごと書く。
#   題の部分は名前の網 0件（scratchpad attr33b.py＝作者の語を出さずに型で見てから、題だけを網に当てて見た）＝場所の語だけ
ATTR_HEAD = {"C33": "Grenfell Tower by ", "C68": "On Westway (A40) looking to Grenfell Tower by "}
ATTR_TAIL = {}
# 撮影者の欄が機関の名前の点＝印 `{作者}` を使わず、その名前を出典の行にそのまま書く（33本目は無い見込み＝`build` が照らす）
AUTHOR_ORG = {}

# 升目 {記号: [(x0, y0, x1, y1, 札)]}（束の画素）。札が「字：」で始まる箱＝読ませない字（名札・車の番号）・それ以外＝顔（出典の行の断りを分ける）
#   ⑤b-2（11-15）に 640px のシート7枚で全39点を当たり、疑いの13か所を原寸（1〜2倍・50px の目盛り）で切り出して決めた（scratchpad の seen33b2.tsv・out/ep33_look/mix_*.jpg）
MASK = {
    # [32]（CC BY 2.0・c113 は全面で寄る）＝奥の黒い車の前の番号板（2倍で字の一部が読めた）＝この回の線（車の番号の字は読ませない）
    "C32": [(752, 1198, 808, 1242, "字：車の番号板"),
            # 右下の柵の際の茂みの中の茶色の丸いもの（4倍で見ても人の頭と腕か、枯れた花か決められない）＝念のため（c113 の窓と地の窓の外）
            (1515, 1262, 1550, 1300, "人の見込み（茂みの中・4倍でも決められない）")],
    # [64]（CC BY 2.0・c620＋地2カット）＝下の端の私人＝右の2人（スマホを構える人の横顔・右の端の人の横顔）。左の人は後ろ姿（顔なし）＝かけない
    "C64": [(1815, 2330, 1920, 2445, "私人の顔（2人）")],
}
# ⚠️ 升目にしない点の理由（11-15 の原寸）：[31]（BY-SA・額装・静止）の通りの車の番号板2枚と小さな人＝1倍で番号は読めるが、額の倍率 0.305（高さ 2724→830）で
#    画面の字は約2px・顔は約4px＝読めない（BY-SA は升目も翻案＝かけない）。[62] の車の番号板は枠の外。[23] の電車の窓・[21]・[33]・[67] の窓に人の顔なし。
#    [30] の団地の案内板＝通路の名と部屋番号だけ。[40] の消防車の運転席に人なし。[45] の学校の入口に人なし（学校の名は場所の名）。[7]・[8]・[12] の地上の消防士は遠景

# 束の段で切り落とす＝絵に入れない {記号: (左, 上, 右, 下)}＝元の絵に対する割合。縮める前に切る（CC BY・CC0 だけ＝BY-SA は切り落としも翻案）
PRE_CROP = {
    # [58]（CC0）＝覆われた塔と幕の下に追悼の壁（人の顔の絵の掲示）＝映像方針 §5-10「上の 1920×1700 だけ」（1920×2560 の 0.6641）＝⑤b-2 に原寸で壁の頭を測って決める
    "C58": (0.0, 0.0, 1.0, 0.6641),
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
    rows = [ln for ln in SOURCES.read_text(encoding="utf-8").replace("\r", "").splitlines() if ln.strip() and not ln.startswith("#")]
    # sources33.psv は見出しを頭の注の下の1行に書く（「code|type|…|note」＝make_list33.SKEYS）＝その行と照らしてから外す
    head = ["code", "type", "grp", "title", "get", "dims", "rights", "basis", "credit", "era", "people", "file", "note"]
    if not rows or rows[0] != "|".join(head):
        raise SystemExit(f"🔴 {SOURCES.name} の見出しの行（13列）が変わった：{(rows or [''])[0][:120]}")
    rows = rows[1:]
    out, prev = {}, None
    for ln in rows:
        f = ln.split("|")
        if len(f) != 13:
            raise SystemExit(f"🔴 {SOURCES.name} の行の欄が13でない：{ln[:80]}")
        d = dict(zip(head, f))
        for k in ("basis", "credit"):
            if d[k].startswith("同上"):
                if not prev or prev[k].startswith("同上"):
                    raise SystemExit(f"🔴 {d['code']}: {k} の「同上」が指す行が無い")
                d[k] = prev[k]
        out[f[0]] = prev = d
    return out


def _fetched():
    """{記号: 行}（取得の記録 fetch33.tsv＝date・code・kind・bytes・md5_1・md5_2・wxh・file・source）"""
    out = {}
    for p in FETCHES:
        for r in csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"):
            out[(r.get("code") or "").strip()] = r
    return out


def _private_rows():
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の表）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    if any(len(r) != PRIVATE_COLS for r in rows):
        raise SystemExit(f"🔴 {PRIVATE.name} の行の欄が{PRIVATE_COLS}でない（列の並びが変わった）")
    return {r[0]: r for r in rows}


def _private():
    """git の外の表 {記号: 作者（2列目＝番号1）}。無ければ止める（束を作る手元だけで読む）"""
    return {k: r[AUTHOR_COL] for k, r in _private_rows().items()}


def _page_of(code):
    """Commons の頁の URL（git の外の表の4列目）と頁の写し（映像方針の `src/commons/html/File_<題>.html`）"""
    r = _private_rows().get(code)
    if not r or not r[PAGE_COL].startswith("https://commons.wikimedia.org/wiki/File:"):
        raise SystemExit(f"🔴 {code}: git の外の表に Commons の頁の URL が無い")
    url = r[PAGE_COL]
    from urllib.parse import unquote
    title = unquote(url.rsplit("/wiki/", 1)[1])
    p = COMMONS_PAGES / (re.sub(r"[^A-Za-z0-9.\-]", "_", title) + ".html")
    return url, p


def _attr_ok(code):
    """🔴 頁の写し（git の外）の許諾の箱に「Attribution: …」の指定があれば、表の2列目（＋ATTR_TAIL）と1字も同じか（名前は出さない＝真偽と字数だけ）。
    指定が無い点は True。頁の写しが無ければ止める（照らせない＝fail closed）"""
    import html as H
    _, p = _page_of(code)
    if not p.exists():
        raise SystemExit(f"🔴 {code}: Commons の頁の写し {p.name[:40]}… が無い（許諾の箱の帰属の指定を照らせない）")
    t = " ".join(H.unescape(re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8"))).split())
    m = re.search(r"Attribution: (.*?) You are free", t)
    if not m:
        return True, "頁に「Attribution:」の指定なし"
    same = " ".join(m.group(1).split()) == " ".join((ATTR_HEAD.get(code, "") + _private().get(code, "") + ATTR_TAIL.get(code, "")).split())
    return same, (f"頁の指定 {len(m.group(1).split())}語・{'「' + ATTR_HEAD[code].strip() + '」＋' if code in ATTR_HEAD else ''}2列目"
                  f"{'＋「' + ATTR_TAIL[code].strip() + '」' if code in ATTR_TAIL else ''}と{'同じ' if same else '違う'}")


def _fold(s):
    return " ".join(unicodedata.normalize("NFKC", s or "").lower().split())


def _mask_word(w):
    return w[0] + "○" * (len(w) - 1)


def _name_re(n):
    n = _fold(n)
    if re.search(r"[a-z]", n):
        return re.compile(r"(?<![a-z0-9])" + r"\s*".join(re.escape(p) for p in n.split()) + r"(?![a-z0-9])")
    return re.compile(re.escape(n.replace(" ", "")))


# 目録の作者の欄に入っていた機関名と一般の語＝名前でない
_NOT_NAMES = {"投稿者", "artist", "wikipedia", "self", "photo", "own work", "flickr", "commons", "wikimedia", "user", "unknown"}


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
    return (main or "").split(":", 1)[0].strip()


GROUND_RIGHTS = ("CC BY 2.0", "CC BY 4.0", "CC0", "PD")      # 地にできる権利（make_list33.JI_OK から映像と Pexels を除いた形・BY-SA は暗くするのも翻案）
NO_GROUND = ("night", "dawn", "noground")      # 地にしない組（夜明けと夜の写真・[24] と [58]＝sources33 の grp の語）＝make_list33.ground_ok と同じ向き


def _rights_key(s):
    r = s["rights"]
    return "PD" if r.startswith("PD") else r


def _fig_row(code):
    """報告の図（F:P1V2-10.9 の形）の出どころの行＝make_list33.auto_rows と同じ中身（sources33.psv に行は無い＝一覧の道具が台本の出典の行から足す）"""
    sys.path.insert(0, str(BUILD))
    import make_list33 as ML
    fig = code[2:]
    return dict(code=code, type="report-fig", grp="night" if fig in ML.FIG_NIGHT else "report", title=f"報告の図 {fig}",
                get="手元の報告の PDF から頁を描いて切る（図の番号と題の行ごと）", dims="", rights="OGL v3.0（第三者のコマ・図を含む）",
                basis="紙面の引用（§2-6c・§2-42）＝額装・無加工・サムネに使わない", credit="出典：" + ML.fig_credit(code),
                era=("2017-06-14 " + "／".join(ML.FIG_ERA[fig])) if fig in ML.FIG_ERA else "報告の図",
                people="", file=f"src/inquiry/{fig.split('-')[0]}.pdf", note="")


def uses(later=None):
    """{束の鍵: dict(code, main=[カット], ji=[カット], full=全面に当てるカットがあるか)}（束に入る写真と紙面）。一覧の種類と出どころの型が食い違えば止める。
    紙面（報告の図）は PAGE_CUT に書いたカットだけ束に入れる（残りは `later["紙面（⑤b-3）"]`）。文字の頁（公的）は ⑤b-3b＝数えるだけ。
    地は CC BY・CC0 の昼の Commons の写真だけ（イメージの地は ⑤b-4＝束の外）"""
    src = _sources()
    sys.path.insert(0, str(BUILD))
    import make_list33 as ML
    out, bad = {}, []
    later = {} if later is None else later
    for r in _list():
        cid = r["cid"]
        main = (r["main"] or "").strip()
        c = _code_of(main)
        if c in ML.NG:
            later.setdefault("差し替え待ち（make_list33.NG）", []).append(cid)      # 使わないと決めた点＝束に入れない（一覧の門番が E で止める）
        elif r["kind"] == "公的":
            later.setdefault("公的（⑤b-3b の文字の頁）", []).append(cid)
        elif r["kind"] == "紙面":                       # 報告の図＝記号は「F:P1V2-10.9」の形（頭の F: ごと）
            ks = [k for k, sp in PAGE_CUT.items() if sp["code"] == main and cid in sp["cuts"]]
            if len(ks) > 1:
                bad.append(f"{cid} {main}: 紙面の切り口 PAGE_CUT が2つある")
            elif not ks:
                later.setdefault("紙面（⑤b-3 の報告の図）", []).append(cid)
            else:
                out.setdefault(ks[0], dict(code=main, main=[], ji=[], full=False, page=True))["main"].append(cid)
        elif c and r["kind"] not in KIND_OUT:
            s = src.get(c)
            if not s:
                bad.append(f"{cid} {c}: 出どころの表に無い")
            elif r["kind"] not in KIND_OK:
                bad.append(f"{cid} {c}: 図の型「{r['kind']}」の素材の欄に記号がある（地は ji の欄）")
            elif s["type"] not in KIND_OK[r["kind"]]:
                bad.append(f"{cid} {c}: 一覧の種類「{r['kind']}」と出どころの型 {s['type']} が食い違う")
            else:
                u = out.setdefault(c, dict(code=c, main=[], ji=[], full=False))
                u["main"].append(cid)
                u["full"] = u["full"] or r["frame"].startswith("全面")
        j = _code_of(r["ji"])
        if j:
            s = src.get(j)
            if (s and s["type"] in STOCK_TYPES) or (not s and re.fullmatch(r"[XG][0-9a-c][0-9]{2}|GJ\d+", j)):   # イメージ（Pexels）の記号＝make_list33.auto_rows が足す X<カット>・G…
                later.setdefault("イメージの地", []).append(cid)
                continue
            if not s or s["type"] not in COMMONS_TYPES:
                bad.append(f"{cid} {j}: 地の写真が Commons の写真でない（{s['type'] if s else '表に無い'}）")
            elif _rights_key(s) not in GROUND_RIGHTS:
                bad.append(f"{cid} {j}: 地の写真の権利 {s['rights']} は地にできない（BY-SA は暗くするのも翻案）")
            elif any(w in s["grp"].split() for w in NO_GROUND):
                bad.append(f"{cid} {j}: 夜明けと夜の写真・地に向かない点（{s['grp']}）は地にしない（映像方針 §5-5）")
            else:
                out.setdefault(j, dict(code=j, main=[], ji=[], full=False))["ji"].append(cid)
    if bad:
        raise SystemExit("🔴 " + "\n🔴 ".join(bad))
    return out


def bundle_name(key):
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
    """範囲だけを升目にする（縮めて NEAREST で戻す）＝16〜31本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def _commons_ok(code, s, fet):
    """Commons の写真の手元のファイル（src/commons/c33/<記号>.jpg）が取得の記録 fetch33.tsv（md5 を2回＝同じ）と同じか。違えば止める"""
    r = fet.get(code)
    if not r:
        raise SystemExit(f"🔴 {code}: 取得の記録が無い（fetch33.tsv）")
    p = EPD / r["file"]
    if not s["file"].startswith("src/commons/c33") or p.parent.resolve() != COMMONS_DIR.resolve() or not p.exists():
        raise SystemExit(f"🔴 {code}: 手元のファイルが無いか置き場が違う（{r['file']}・表の file の欄 {s['file']}）")
    h = md5(p)
    if r["md5_1"] != r["md5_2"] or h != r["md5_1"]:
        raise SystemExit(f"🔴 {code}: {p.name} の md5 が取得の記録と合わない（取り直す）")
    return p, h


# ── 紙面（報告の図）──────────────────────────────────────────────
# 🆕 ⑤b-2（11-15）：一覧の「紙面」38カット（記号 F:<巻>-<図>）＝公開調査の報告の PDF の頁を描いて、図の絵と題の行「Figure n.n」ごと切る
#    （公的な機関の PDF＝許可不要・図の中身は第三者のコマを含む＝紙面の引用・額装・無加工）。32本目の紙面の切り口（字の層の行で決める）の型のまま。
#    箱は表示の向きの pt（1pt＝PAGE_K 画素で描く）。⑤b-2 は冒頭の夜の図4つ（c101〜c104）だけ・残りの34は ⑤b-3（PAGE_CUT に無い＝束の外で数える）。
#    頁と箱＝11-15 に scratchpad の figfind33.py で「Figure n.n」の行と同じ頁の埋め込みの絵の箱を測った（題の行は「Figure n.n」の1行だけ＝名前が載らない）。
#    名前＝切り口の中の字（字の層）を名前の網に当てる（焼き込みのコマの時刻の字は字の層に無い＝絵を原寸で見る）。
PDF_SRC = {"P1V2": ("inquiry/P1V2.pdf", "5ceca426290821c1e2d452bea2d6faae",       # md5＝手元の2つの写し（src/web/p1/…volume_2.pdf と同じ）・240頁
                    "https://assets.publishing.service.gov.uk/media/66d822b97a73423428aa2ee8/Grenfell_Tower_Inquiry_-_Phase_1_report_-_volume_2.pdf"),
           # 🆕 ⑤b-3（11-15）：md5 は2回取って同じ。第1段階の第1・3・4巻は src/web/p1/ の写しと同じ・第2段階の第1巻は src/web/avoid/gti_p2_vol1.pdf と同じ・
           #    第7巻は手元の1つだけ（URL は gov.uk の頁の写し src/web/avoid/p2pub.html の直リンク）
           "P1V1": ("inquiry/P1V1.pdf", "f55f93ab9d6fbe8d62fb409f84347b2d",
                    "https://assets.publishing.service.gov.uk/media/66d822a87a73423428aa2ee7/Grenfell_Tower_Inquiry_-_Phase_1_report_-_volume_1.pdf"),
           "P1V3": ("inquiry/P1V3.pdf", "2aef4ecee5d50ab294db2f7351f12c3e",
                    "https://assets.publishing.service.gov.uk/media/66d822c9a399e0dcf5200b31/Grenfell_Tower_Inquiry_-_Phase_1_report_-_volume_3.pdf"),
           "P1V4": ("inquiry/P1V4.pdf", "d1135fa0c5f06d8a23c25c4aa028b538",
                    "https://assets.publishing.service.gov.uk/media/66d822e07a73423428aa2ee9/Grenfell_Tower_Inquiry_-_Phase_1_report_-_volume_4.pdf"),
           "P2V1": ("inquiry/P2V1.pdf", "b03083c17741dc6893ed80a213b40d79",
                    "https://assets.publishing.service.gov.uk/media/66d817aa701781e1b341dbd3/CCS0923434692-004_GTI_Phase_2_Volume_1_BOOKMARKED.pdf"),
           "P2V7": ("inquiry/P2V7.pdf", "17262768140a3da01bb30c23bb0b6d11",
                    "https://assets.publishing.service.gov.uk/media/66d818059084b18b95709f86/CCS0923434692-004_GTI_Phase_2_Volume_7_BOOKMARKED.pdf")}
OCR_DIR = SRC / "ocr"                   # 33本目は使わない（走査の絵の頁は無い見込み）
PAGE_K = 3.0                            # 描く倍率（1pt＝3画素＝31本目の判決と同じ）
PAGE_PAD = 24                           # 紙面の絵のまわりの白（束の画素）
PART_GAP = 30                           # つないだ切り口のあいだの白（束の画素）
PX300 = 72 / 300                        # 300dpi の頁の画素 → pt
INK = 120                               # 縁の黒の物差し（灰色の値・これより暗い画素が縁の2画素にあれば「行か罫を切った」）
# {束の鍵: dict(code, cuts, parts=[(頁, 箱|"img")], unit="pt"|"px300", stack="v"|"h", align, k, must, out, ocr_must, ocr_out, no_img, hl={cid: (頁, 箱)})}
#   must＝切り口の中に丸ごと入るべき行の字（字の層）・out＝切り口に入ってはいけない行の字（隣の段・名前の行の目印）
#   箱＝図の絵の箱の外 1.4〜4pt・題の行の下 4pt（左は本文の段の頭 99.2 の外の 96・右は 542＝段の右の端 541.3 の外）。上下の本文の行と重なれば render_page が止める
PAGE_CUT = {
    # c101＝図10.9（p22・絵 879×937＝住人が真下から携帯電話で撮った映像のコマ 01:09:31・01:09:36〈本文 ¶10.36〉）
    "P1V2_F10_9": dict(code="F:P1V2-10.9", cuts=["c101"], parts=[(22, (96, 68.2, 542, 565.2))], must=["Figure 10.9"]),
    # c102＝図10.14（p34・絵 879×495・01:19）
    "P1V2_F10_14": dict(code="F:P1V2-10.14", cuts=["c102"], parts=[(34, (96, 211.9, 542, 489.1))], must=["Figure 10.14"]),
    # c103＝図10.22（p47・絵 885×830・01:27）
    "P1V2_F10_22": dict(code="F:P1V2-10.22", cuts=["c103"], parts=[(47, (96, 105.4, 542, 549.9))], must=["Figure 10.22"]),
    # c104＝図14.1（p180・絵 881×749・警視庁のヘリコプターの映像のコマ 02:06）
    "P1V2_F14_1": dict(code="F:P1V2-14.1", cuts=["c104"], parts=[(180, (96, 253.4, 542, 657.6))], must=["Figure 14.1"]),
    # 🆕 ⑤b-3（11-15）：残りの32の図（34カット）。頁と箱＝scratchpad の figfind33b.py（「Figure n.n」の行と同じ頁の埋め込みの絵）・pgprobe33.py（走査の絵の頁の非白の帯）。
    #    箱の決め＝絵の左 −3・上 −2.5・右 +3.4（題の行が広ければその右）・題の行の下 +4（上下の本文・隣の絵と重ならないかは render_page が照らす）。
    #    題の行は第1段階＝「Figure n.n」だけ（7.2 は「The Stratford Control Room」＝指令室の場所の名）・第2段階＝試験の名と実験の番号（名前の網 0件）
    # ── 第1段階 第1巻
    "P1V1_F3_2": dict(code="F:P1V1-3.2", cuts=["c203"], parts=[(26, (95.6, 310.4, 340.2, 697.6))], must=["Figure 3.2"]),
    "P1V1_F6_1": dict(code="F:P1V1-6.1", cuts=["c210", "c619"], parts=[(39, (96.2, 171.4, 542, 580.8))], must=["Figure 6.1"]),
    "P1V1_F6_11": dict(code="F:P1V1-6.11", cuts=["c213"], parts=[(52, (96.2, 239.4, 542, 522.3))], must=["Figure 6.11"]),
    "P1V1_F6_7": dict(code="F:P1V1-6.7", cuts=["c405", "c629"], parts=[(48, (96.2, 173.7, 535.4, 606.0))], must=["Figure 6.7"]),
    "P1V1_F7_2": dict(code="F:P1V1-7.2", cuts=["c501"], parts=[(62, (96.2, 68.7, 542, 427.5))], must=["Figure 7.2 The Stratford Control Room"]),
    # ── 第1段階 第2巻（10.7 と 10.8 は p21 の上下・11.6 は p100 の右上・11.7 は p100 の左下＝4枚の組のうち1枚ずつ）
    "P1V2_F10_5": dict(code="F:P1V2-10.5", cuts=["c206"], parts=[(17, (96.2, 367.3, 541.2, 631.1))], must=["Figure 10.5"]),
    "P1V2_F10_6": dict(code="F:P1V2-10.6", cuts=["c305"], parts=[(20, (96.2, 360.9, 542, 723.8))], must=["Figure 10.6"]),
    "P1V2_F10_7": dict(code="F:P1V2-10.7", cuts=["c307"], parts=[(21, (96.2, 69.7, 542, 356.7))], must=["Figure 10.7"], out=["Figure 10.8"]),
    "P1V2_F10_8": dict(code="F:P1V2-10.8", cuts=["c309"], parts=[(21, (95.1, 362.1, 542, 641.7))], must=["Figure 10.8"], out=["Figure 10.7"]),
    "P1V2_F10_15": dict(code="F:P1V2-10.15", cuts=["c312"], parts=[(37, (94.6, 68.1, 308.0, 505.9))], must=["Figure 10.15"]),
    "P1V2_F10_17": dict(code="F:P1V2-10.17", cuts=["c314"], parts=[(40, (94.8, 206.5, 305.4, 634.6))], must=["Figure 10.17"]),
    "P1V2_F10_24": dict(code="F:P1V2-10.24", cuts=["c315"], parts=[(49, (95.0, 133.4, 544.0, 460.2))], must=["Figure 10.24"]),
    "P1V2_F11_6": dict(code="F:P1V2-11.6", cuts=["c319"], parts=[(100, (330.8, 69.7, 541.3, 392.0))], must=["Figure 11.6"], out=["Figure 11.5", "Figure 11.7", "Figure 11.8"]),
    "P1V2_F11_7": dict(code="F:P1V2-11.7", cuts=["c411"], parts=[(100, (96.2, 409.2, 306.7, 733.2))], must=["Figure 11.7"], out=["Figure 11.5", "Figure 11.6", "Figure 11.8"]),
    "P1V2_F12_1": dict(code="F:P1V2-12.1", cuts=["c424"], parts=[(130, (96.2, 268.9, 514.3, 761.4))], must=["Figure 12.1"]),
    "P1V2_F12_7": dict(code="F:P1V2-12.7", cuts=["c414"], parts=[(140, (96.2, 69.7, 315.2, 465.3))], must=["Figure 12.7"]),
    "P1V2_F13_1": dict(code="F:P1V2-13.1", cuts=["c413"], parts=[(158, (96.2, 305.4, 409.5, 687.3))], must=["Figure 13.1"]),
    # ── 第1段階 第3巻（17.3 と 17.4 は p78 の上下）
    "P1V3_F17_3": dict(code="F:P1V3-17.3", cuts=["c417"], parts=[(78, (96.2, 134.9, 467.6, 441.4))], must=["Figure 17.3"], out=["Figure 17.4"]),
    "P1V3_F17_4": dict(code="F:P1V3-17.4", cuts=["c425"], parts=[(78, (96.2, 445.5, 476.1, 754.4))], must=["Figure 17.4"], out=["Figure 17.3"]),
    "P1V3_F18_1": dict(code="F:P1V3-18.1", cuts=["c415"], parts=[(108, (96.2, 268.9, 356.4, 726.8))], must=["Figure 18.1"]),
    "P1V3_F19_1": dict(code="F:P1V3-19.1", cuts=["c418"], parts=[(130, (96.2, 239.5, 542, 720.3))], must=["Figure 19.1"]),
    # ── 第1段階 第4巻（21.1 は p8 の下の絵＝上の絵は題の行が無い＝⑤b-3 のシートで見て決める・21.4 は p10 の上・22.8 は p27 の下・22.15 は p33 の下）
    "P1V4_F21_1": dict(code="F:P1V4-21.1", cuts=["c301"], parts=[(8, (96.2, 382.9, 542.4, 714.5))], must=["Figure 21.1"]),
    "P1V4_F21_4": dict(code="F:P1V4-21.4", cuts=["c302"], parts=[(10, (96.2, 92.9, 542.1, 368.5))], must=["Figure 21.4"], out=["Figure 21.5"]),
    "P1V4_F21_6": dict(code="F:P1V4-21.6", cuts=["c303"], parts=[(12, (94.8, 68.3, 533.1, 689.1))], must=["Figure 21.6"]),
    "P1V4_F22_8": dict(code="F:P1V4-22.8", cuts=["c310"], parts=[(27, (94.8, 432.1, 509.4, 762.1))], must=["Figure 22.8"], out=["Figure 22.7"]),
    "P1V4_F22_15": dict(code="F:P1V4-22.15", cuts=["c311"], parts=[(33, (95.1, 449.2, 539.9, 743.0))], must=["Figure 22.15"]),
    # ── 第2段階 第1巻（5.8 の頁は 642×889pt＝ほかの頁と大きさが違う）
    "P2V1_F5_2": dict(code="F:P2V1-5.2", cuts=["c720"], parts=[(60, (96.2, 400.4, 541, 707.6))], must=["Figure 5.2: Image of BS 476-7 test in operation", "Class 1"]),
    "P2V1_F5_8": dict(code="F:P2V1-5.8", cuts=["c710"], parts=[(73, (119.7, 95.8, 564.6, 331.9))], must=["Figure 5.8: Diagram and picture", "Thermocouple"]),
    "P2V1_F5_9": dict(code="F:P2V1-5.9", cuts=["c630"], parts=[(74, (94.5, 72.7, 544.4, 303.1))], must=["Figure 5.9: photographs of a BS 8414 test in operation"]),
    # ── 第2段階 第7巻（頁いっぱいの走査の絵の上に字の層＝箱は描いた絵の非白の帯で測った・109.1 の題は2行）
    "P2V7_F109_1": dict(code="F:P2V7-109.1", cuts=["c320"], parts=[(185, (96, 106.5, 542, 552.5))], must=["Figure 109.1", "experiment"], out=["Aims and objectives"]),
    "P2V7_F109_2": dict(code="F:P2V7-109.2", cuts=["c401"], parts=[(189, (96, 316.5, 542, 595.1))], must=["Figure 109.2 – Experiment 21 (time 9.44 minutes)"]),
    "P2V7_F109_3": dict(code="F:P2V7-109.3", cuts=["c403"], parts=[(190, (96, 105.5, 542, 384.5))], must=["Figure 109.3 – Experiment 21 (time 10.50 minutes)"]),
}


def _pdf_of(code):
    vol = code[2:].split("-")[0] if code.startswith("F:") else code
    if vol not in PDF_SRC:
        raise SystemExit(f"🔴 {code}: PDF_SRC に巻 {vol} が無い")
    rel, want, url = PDF_SRC[vol]
    p = SRC / rel
    if not p.exists():
        raise SystemExit(f"🔴 {code}: PDF が無い（{p}）")
    h = md5(p)
    if h != want:
        raise SystemExit(f"🔴 {code}: {p.name} の md5 {h[:8]} が記録 {want[:8]} と合わない（取り直す）")
    return p, h, url


def _lines_disp(pg):
    """字の層の行＝[(字, 表示の向きの箱)]。🔴 横向きの頁（/Rotate 90）の字の層は回す前の座標＝rotation_matrix で直す"""
    import fitz
    rm = pg.rotation_matrix
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            t = "".join(s["text"] for s in ln["spans"]).strip()
            if t:
                out.append((t, fitz.Rect(ln["bbox"]) * rm))
    return out


def _ocr_lines(n):
    """付録C の OCR の行＝[(字, x_pt, y_pt)]（[x,y]＝300dpi の頁の画素の行の頭）"""
    p = OCR_DIR / f"p{n}.txt"
    out = []
    if p.exists():
        for ln in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\[(\d+),(\d+)\]\s*(.*)", ln)
            if m:
                out.append((m.group(3), int(m.group(1)) * PX300, int(m.group(2)) * PX300))
    return out


def _edge_ink(im, w=2):
    """切り口の縁 w 画素の暗い画素の数 {辺: 数}（0 の辺は出さない）＝行や罫を縁で切っていないか"""
    import numpy as np
    a = np.asarray(im.convert("L"))
    sides = {"上": a[:w], "下": a[-w:], "左": a[:, :w], "右": a[:, -w:]}
    return {k: int((v < INK).sum()) for k, v in sides.items() if int((v < INK).sum())}


def frame_of(w, h):
    """額の選び方（scene_jiko.photo_box と同じ幾何）＝高さいっぱい（ptall・幅 1128 まで・高さ 830 まで）と幅いっぱい（pw=1776・高さ 648 まで）の面積の大きい方"""
    a = w / h
    pt = (min(1128, 830 * a), min(830, 1128 / a))
    pw = (min(1776, 648 * a), min(648, 1776 / a))
    return ("ptall", pt) if pt[0] * pt[1] >= pw[0] * pw[1] else ("pw=1776", pw)


def render_page(key):
    """紙面の切り口を描く＝(RGB の絵, PDF の md5, 記録の言葉, 印 {cid: [x0,y0,x1,y1]＝束の絵の割合}, 出どころ)。照らしが1つでも外れれば止める"""
    import fitz
    from PIL import Image
    sp = PAGE_CUT[key]
    p, h, url = _pdf_of(sp["code"])
    doc = fitz.open(p)
    k = sp.get("k", PAGE_K)
    u = PX300 if sp.get("unit") == "px300" else 1.0
    bad, ims, boxes, words, pages = [], [], [], [], {}
    seen_txt, seen_ocr, near_txt, near_ocr = [], [], [], []
    allowed = []
    for part in sp["parts"]:
        n, box = part[0], part[1]
        ok = part[2] if len(part) > 2 else {}                # 縁の黒を許す辺 {辺: 理由}（罫の線だけ＝理由を記録に残す）
        pg = doc[n - 1]
        if box == "img":
            rr = [fitz.Rect(r) * pg.rotation_matrix for x in pg.get_images(full=True) for r in pg.get_image_rects(x[0])]
            if len(rr) != 1:
                raise SystemExit(f"🔴 {key}: p{n} の絵が1枚でない（{len(rr)}枚）")
            R = rr[0] + (1.5, 1.5, -1.5, -1.5)                 # 走査の絵の縁（黒い点がある）は 1.5pt 内側で切る
        else:
            R = fitz.Rect(*(v * u for v in box))
        if not pg.rect.contains(R):
            bad.append(f"p{n}: 切り口 {tuple(round(v, 1) for v in R)} が頁 {tuple(pg.rect)} の外にはみ出す")
        Rin = fitz.Rect(R.x0 - 0.6, R.y0 - 0.6, R.x1 + 0.6, R.y1 + 0.6)
        lines = [(" ".join(t.replace(" ", " ").split()), r) for t, r in _lines_disp(pg)]   # 改行しない空白（表紙）をふつうの空白に
        inside = [t for t, r in lines if Rin.contains(r)]
        cut = [t for t, r in lines if r.intersects(R) and not Rin.contains(r)]
        if cut:
            bad.append(f"p{n}: 切り口の縁が字の層の行を切る（{len(cut)}行・「{cut[0][:40]}」）")
        if sp.get("no_img"):
            for x in pg.get_images(full=True):
                for r in pg.get_image_rects(x[0]):
                    if (fitz.Rect(r) * pg.rotation_matrix).intersects(R):
                        bad.append(f"p{n}: 切り口が頁の絵（xref {x[0]}・{tuple(round(v) for v in r)}）に重なる（表紙の飾りの写真を入れない）")
        ocr = [t for t, x, y in _ocr_lines(n) if R.contains(fitz.Point(x, y))]
        seen_txt += inside
        seen_ocr += ocr
        near_txt += [t for t, r in lines if r.intersects(R)]
        near_ocr += ocr
        words += inside + ocr
        if n not in pages:
            pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), alpha=False)            # 頁を表示の向きで丸ごと描いてから切る（clip の座標の向きに頼らない）
            pages[n] = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im = pages[n].crop((round(R.x0 * k), round(R.y0 * k), round(R.x1 * k), round(R.y1 * k)))
        e = _edge_ink(im)
        for side in [s_ for s_ in e if s_ in ok]:
            if e[side] > 60:
                bad.append(f"p{n}: 許した辺「{side}」の黒が {e[side]} 画素（罫の線の幅を超える＝字を切っている見込み）")
            allowed.append(f"p{n} の{side}の縁の黒 {e.pop(side)} 画素＝{ok[side]}")
        if e:
            bad.append(f"p{n}: 切り口の縁に黒 {e}（行か罫を切っている）")
        ims.append(im)
        boxes.append((n, R))
    for a in sp.get("must", []):
        if not any(a in t for t in seen_txt):
            bad.append(f"丸ごと入るべき行「{a}」が切り口の中に無い")
    for a in sp.get("out", []):
        if any(a in t for t in near_txt):
            bad.append(f"入ってはいけない行「{a}」が切り口にかかる")
    for a in sp.get("ocr_must", []):
        if not any(a in t for t in seen_ocr):
            bad.append(f"OCR の行「{a}」が切り口の中に無い")
    for a in sp.get("ocr_out", []):
        if any(a in t for t in near_ocr):
            bad.append(f"入ってはいけない OCR の行「{a}」が切り口に入る")
    leak = hits_in(" ".join(words), _names())
    if leak:
        bad.append(f"切り口の字に名前の網の語 {len(leak)}語（表示しない）")
    if bad:
        raise SystemExit(f"🔴 {key}:\n  " + "\n  ".join(bad))
    # つなぐ（縦＝align で左右を揃える・横＝上で揃える）
    if sp.get("stack") == "h":
        W = sum(i.width for i in ims) + PART_GAP * (len(ims) - 1)
        H = max(i.height for i in ims)
        offs, x = [], 0
        for i in ims:
            offs.append((x, 0))
            x += i.width + PART_GAP
    else:
        W = max(i.width for i in ims)
        H = sum(i.height for i in ims) + PART_GAP * (len(ims) - 1)
        offs, y = [], 0
        for i in ims:
            x = {"right": W - i.width, "center": (W - i.width) // 2}.get(sp.get("align"), 0)
            offs.append((x, y))
            y += i.height + PART_GAP
    out = Image.new("RGB", (W, H), (255, 255, 255))
    for i, o in zip(ims, offs):
        out.paste(i, o)
    from PIL import ImageOps
    out = ImageOps.expand(out, border=PAGE_PAD, fill=(255, 255, 255))
    hl = {}
    for cid, (n, box) in (sp.get("hl") or {}).items():
        r = fitz.Rect(*(v * u for v in box))
        j = next((j for j, (m, R) in enumerate(boxes) if m == n and R.contains(r)), None)
        if j is None:
            raise SystemExit(f"🔴 {key}: 印 {cid} の箱が切り口の中に無い")
        R = boxes[j][1]
        ox, oy = offs[j]
        x0, y0 = PAGE_PAD + ox + (r.x0 - R.x0) * k, PAGE_PAD + oy + (r.y0 - R.y0) * k
        x1, y1 = PAGE_PAD + ox + (r.x1 - R.x0) * k, PAGE_PAD + oy + (r.y1 - R.y0) * k
        hl[cid] = [round(x0 / out.width, 4), round(y0 / out.height, 4), round(x1 / out.width, 4), round(y1 / out.height, 4)]
    how = "・".join(f"p{n} の切り口（{R.x0:.0f},{R.y0:.0f}〜{R.x1:.0f},{R.y1:.0f}pt）" for n, R in boxes)
    how += f"を{'横' if sp.get('stack') == 'h' else '縦'}につないだ" if len(boxes) > 1 else "を描いた"
    how += f"（1pt＝{k:g}画素・表示の向き）" + "".join(f"・{a}" for a in allowed)
    return out, h, how, hl, url


def year_of(code, s):
    m = _YEAR.search(s["era"])
    if m:
        return int(m.group(1)), f"{SOURCES.name} の時期の欄「{s['era'][:24]}」（映像方針＝頁の説明・EXIF・凡例）"
    return None, f"撮影の年の出どころが無い（時期の欄「{s['era']}」）"


def _base_credit(s):
    """sources33 の出典の欄を束の書きの頭の形に揃える：「・無加工」は「／改変なし」で言う・「・改変：切出」（[7]・[58]）は全面と束の段の切り落とし（PRE_CROP）で言い直す
    ＝欄の字のまま残さない（切っていない点に「切出」と書かない）。CC0（[58]）は表示が任意＝撮影者の名乗りを書かない（記憶 feedback-no-optional-credits・sources33 の欄のまま）"""
    cr = s["credit"].replace("・無加工", "").replace("・改変：切出", "")
    if s["type"] in COMMONS_TYPES and not cr.startswith(("写真：", "図：")):
        cr = "写真：" + cr
    return cr


def _mask_words(boxes):
    """升目の断りの語＝「顔」「字」「顔と字」（札が「字：」で始まる箱＝字）"""
    plate = any(str(b[4]).startswith("字：") for b in boxes)
    face = any(not str(b[4]).startswith("字：") for b in boxes)
    return "顔と字" if face and plate else "字" if plate else "顔"


def screen_credit(code, s, boxes, full):
    """画面の出典の行（了承②）＝sources33 の出典の欄＋**改変の断りを明記**：
    BY-SA＝「／改変なし」（額装・無加工）・CC BY の全面＝「／改変：切出」・CC BY の額装だけ＝「／改変なし」・CC0 と PD＝断りなし（升目と切り落としだけ書く）。
    報告の図＝紙面の引用（図の番号と題の行ごと・額装・無加工）＝「出典：グレンフェル・タワー調査 …巻 図n.n（年）」だけ。升目は「・〇〇にモザイク」を足す"""
    if "［" in s["credit"] or "⑤b" in s["credit"] or s["credit"].startswith("同上") or not s["credit"].strip() or s["credit"] == "—":
        raise SystemExit(f"🔴 {code}: 出典の欄に書きかけの印が残る（{s['credit'][:60]}）")
    cr = _base_credit(s)
    if s["type"] in PAGE_TYPES:                          # 紙面の引用＝改変の断りを書かない（引用は手を入れない・頁から図の箱だけを切った）
        if boxes:
            raise SystemExit(f"🔴 {code}: 紙面の引用に升目はかけない（引用は無加工）＝別の図に替える")
        return cr
    what = f"{_mask_words(boxes)}にモザイク" if boxes else ""
    if boxes and "BY-SA" in s["rights"]:
        raise SystemExit(f"🔴 {code}: 升目は CC BY・CC0・PD の写真だけ（{s['rights']}＝BY-SA は升目も翻案）")
    if "BY-SA" in s["rights"]:
        if code in PRE_CROP:
            raise SystemExit(f"🔴 {code}: BY-SA は切り落としも翻案（PRE_CROP に書かない）")
        return cr + "／改変なし"
    if s["rights"].startswith("CC BY"):
        mods = (["切出"] if full or code in PRE_CROP else []) + ([what] if what else [])
        return cr + ("／改変：" + "・".join(mods) if mods else "／改変なし")
    mods = (["切出"] if code in PRE_CROP else []) + ([what] if what else [])
    return cr + ("／改変：" + "・".join(mods) if mods else "")


def who_table(code, s):
    """CREDITS.md の撮影者の欄（名前は書かない）"""
    t, r_ = s["type"], s["rights"]
    if t in COMMONS_TYPES and r_.startswith("CC BY"):
        return "Commons の撮影者（名前は git の外 `ref/ep33/src/credits_private.tsv` の記号の行の2列目＝画面は焼くときに足す）"
    if t in COMMONS_TYPES and r_.startswith("CC0"):
        return "表示は任意（CC0）＝撮影者の名乗りは書かない"
    if t in PAGE_TYPES:
        return "グレンフェル・タワー調査（公開調査の報告）＝図の中のコマの撮り手は報告の本文の範囲（名前は書かない）"
    raise SystemExit(f"🔴 {code}: 撮影者の欄の型が分からない（{t}・{r_}）")


def _lic(s):
    if s["type"] in PAGE_TYPES:
        return "紙面の引用（報告は OGL v3.0・図の中に第三者のコマ）"
    return s["rights"]


def cmd_build():
    from PIL import Image
    src, fet = _sources(), _fetched()
    db, bad = {}, 0
    later = {}
    us = uses(later)
    for code in list(MASK) + list(PRE_CROP) + list(PAGE_CUT):
        if code not in us:
            print(f"🔴 MASK・PRE_CROP・PAGE_CUT の {code} は一覧で使っていない（カットを替えたときの取り残し）")
            bad += 1
    prv = _private_rows()
    n_attr = 0
    for code in sorted(c for c in us if c in prv):        # 🔴 頁の許諾の箱に帰属の指定があれば2列目と照らす（33本目の表に attr の列は無い＝全点の頁の写しで見る・名前は出さない）
        ok, why = _attr_ok(code)
        if why != "頁に「Attribution:」の指定なし" or not ok:
            print(f"{'・' if ok else '🔴'} {code}: {why}")
            n_attr += 1
        if not ok:
            bad += 1
    print(f"・帰属の指定（頁の写しの「Attribution:」）＝{n_attr}点{'（ほかは指定なし）' if n_attr else '＝全点 指定なし'}")
    for key, u in sorted(us.items(), key=lambda kv: (kv[1].get("page", False), 0 if kv[1].get("page") else int(re.sub(r"\D", "", kv[0]) or 0), kv[0])):
        code = u["code"]
        s = _fig_row(code) if code.startswith("F:") else src[code]
        name = bundle_name(key)
        dst = EPD / f"{name}.jpg"
        t = s["type"]
        box_m = MASK.get(code, [])
        if t in PAGE_TYPES:                              # 紙面（PDF の頁の切り口＝render_page が照らす）
            try:
                im, smd5, how, hl, url = render_page(key)
            except SystemExit as e:
                print(e)
                bad += 1
                continue
            fr, size = frame_of(*im.size)
            im.save(dst, quality=JPEG_Q, optimize=True)
            w, h = im.size
            y, ywhy = year_of(code, s)
            cr = screen_credit(key, s, [], False)
            db[name] = dict(code=code, part="", file=PDF_SRC[code[2:].split("-")[0]][0], cut=" ".join(u["main"]), ji="",
                            credit=cr, who=who_table(code, s), note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                            md5=md5(dst), src_md5=smd5, lic=_lic(s), frame=True, ground=s["basis"][:120], url=url,
                            blur=[], how=how + f"・額＝{fr}（約{size[0]:.0f}×{size[1]:.0f}）", year=y, year_why=ywhy, stock=False, page=True, related=False,
                            quote_page=False, named=False, mosaic=None, name_mosaic=None, masked_before=None, era=s["era"], people=s["people"],
                            private=False, shot=None, hl=hl or None, fit=fr, fig=True)    # fig＝報告の図（絵が主の紙面）＝check_page_edges の対照に使わない
            print(f"✓ {key:12} {name:12} {w}x{h:<5} 主 {' '.join(u['main']):10} 額 {fr:8} {cr[:40]}")
            continue
        p, smd5 = _commons_ok(code, s, fet)
        im, notes = load_photo(p)
        notes.append(f"{FETCHES[0].name} の md5 と同じ（2回とも）")
        if code in PRE_CROP:
            if "BY-SA" in s["rights"]:
                print(f"🔴 {code}: BY-SA は切り落としも翻案（PRE_CROP に書かない）")
                bad += 1
                continue
            f = PRE_CROP[code]
            im = im.crop((round(im.width * f[0]), round(im.height * f[1]), round(im.width * f[2]), round(im.height * f[3])))
            notes.append(f"束の段で切り落とした {f}")
        im, k = _shrink(im)
        if k < 1.0:
            notes.append(f"縮小 ×{k:.3f}")
        if box_m:
            im = mosaic(im, box_m, MOSAIC_PX)
            notes.append(f"{_mask_words(box_m)}の升目 {len(box_m)}か所（升 {MOSAIC_PX}px）")
        im.save(dst, quality=JPEG_Q, optimize=True)
        w, h = im.size
        y, ywhy = year_of(code, s)
        cr = screen_credit(code, s, box_m, u["full"])
        if code in ATTR_TAIL or code in ATTR_HEAD:
            if AUTHOR not in cr:
                print(f"🔴 {code}: 帰属の指定の字を足す出典の行に {AUTHOR} が無い")
                bad += 1
            cr = cr.replace(AUTHOR, ATTR_HEAD.get(code, "") + AUTHOR + ATTR_TAIL.get(code, ""))
        if code in AUTHOR_ORG:
            if " ".join(prv.get(code, ["", ""])[AUTHOR_COL].split()) != AUTHOR_ORG[code] or AUTHOR not in cr:
                print(f"🔴 {code}: 機関の名前が git の外の表の2列目と違うか、出典の行に {AUTHOR} が無い")
                bad += 1
            cr = cr.replace(AUTHOR, AUTHOR_ORG[code])
        frame = "BY-SA" in s["rights"]
        if frame and u["full"]:
            print(f"🔴 {key}: 額装だけの点（{s['rights'][:12]}・{t}）を全面のカット {' '.join(u['main'])} に当てている")
            bad += 1
        url, _ = _page_of(code)                          # Commons の頁（git の外の表の4列目＝公開の頁の URL）
        db[name] = dict(code=code, part="", file=fet[code]["file"], cut=" ".join(u["main"]), ji=" ".join(u["ji"]),
                        credit=cr, who=who_table(code, s), note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=_lic(s), frame=frame, ground=s["basis"][:120], url=url,
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False, page=False, related=False,
                        quote_page=False, named=AUTHOR in cr, mosaic=[list(b[:4]) for b in box_m] or None, name_mosaic=None,
                        masked_before=None, era=s["era"], people=s["people"], private=False, shot=None)
        print(f"✓ {key:7} {name:7} {w}x{h:<5} 主 {' '.join(u['main']) or '—':10} 地 {' '.join(u['ji']) or '—':30} {_lic(s)[:14]:14}"
              f"{'  額装だけ' if frame else ''}  {'・'.join(notes)[:60]}")
    for j, cs in later.items():
        print(f"・{j}：{len(cs)}カット（{' '.join(cs[:10])}{' …' if len(cs) > 10 else ''}）＝束の外")
    # イメージの写真（Pexels）＝⑤b-4 で取ったファイルそのまま `ref/ep33/stock/<名>.jpg`（🔴 git に入れない＝19本目 決め⑨）。
    #    Actions・Modal は `footage.stock_photos` が台帳の media から取り直して md5 を照らす（32本目の写し）。sources33 に行が無い記号は数えて出すだけ
    (EPD / "stock").mkdir(exist_ok=True)
    rows = _list()
    n_stock = 0
    for code, s in sorted(src.items()):
        if s["type"] not in STOCK_TYPES or not s["file"].endswith(".jpg"):
            continue
        r = fet.get(code) or {}
        p = EPD / s["file"]
        if not p.exists() or not r or md5(p) != r["md5"] or r.get("出どころ") != s["get"]:
            print(f"🔴 {code}: 手元の写真が無いか、md5 か直リンクが取得のときと違う（{s['file']}）＝fetch32e.py stock で取る")
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
                        ground=s["rights"], url=_stock_page(code, s), blur=[], how=f"取ったファイルそのまま（{w}x{h}）", year=None, year_why="この事故の物でない（イメージ）",
                        stock=True, page=False, related=False, quote_page=False, named=False, mosaic=None, name_mosaic=None, masked_before=None, era=s["era"], people=s["people"],
                        private=False, shot=None, media=s["get"][len("stock:"):])
        n_stock += 1
        print(f"✓ {code:7} {name:14} {w}x{h:<5} 主 {' '.join(main) or '—':10} 地 {' '.join(ji) or '—':30} Pexels（git に入れない）")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    pub = [n for n, r in db.items() if not r.get("stock")]
    print(f"→ ref/ep33/assets.json（{len(db)}点＝Commons {sum(1 for r in db.values() if r['code'].startswith('C'))}"
          f"・紙面 {sum(1 for r in db.values() if r.get('page'))}・イメージ {n_stock}（git の外）"
          f"・額装だけ {sum(1 for r in db.values() if r['frame'])}・作者の印 {sum(1 for r in db.values() if r['named'])}・升目 {sum(1 for r in db.values() if r['mosaic'])}"
          f"・地に使う {sum(1 for r in db.values() if r['ji'])}・束の大きさ {tot / 1e6:.1f}MB／公開リポの分 "
          f"{sum((EPD / f'{n}.jpg').stat().st_size for n in pub) / 1e6:.1f}MB）")
    return 1 if bad else 0


def _stock_page(code, s):
    """頁の URL＝sources33 の basis の頭（13列のまま＝get は直リンクが持つ）＝32本目 ep32_assets._stock_page の写し（⚠️ ⑤b-4 で fetch33 の列名に合わせる）"""
    m = re.match(r"https://www\.pexels\.com/(?:video|photo)/\S+?/(?=[（ ]|$)", s["basis"])
    if not m:
        raise SystemExit(f"🔴 {code}: basis の頭に Pexels の頁の URL が無い（{s['basis'][:60]}）")
    return m.group(0)


def _find(db, c):
    for n, r in db.items():
        if n == c or r["code"] == c:
            return n
    raise SystemExit(f"🔴 束に {c} が無い")


def cmd_sheet(codes, tag="sheet"):
    """1枚 640幅の 2列×3行のシート（札＝束の名・寸法・人の欄）＝out/ep33_look/<tag>_NN.jpg。🔴 事故検証ch の決め＝640px 以上のシートで全数を当たり、疑いだけ原寸"""
    from PIL import Image, ImageDraw
    db = json.loads(DB.read_text(encoding="utf-8"))
    names = [_find(db, c) for c in codes] if codes else sorted(db)
    TW, TH, LAB = 640, 480, 22
    SCRATCH.mkdir(parents=True, exist_ok=True)
    outs = []
    for i in range(0, len(names), 6):
        part = names[i:i + 6]
        sheet = Image.new("RGB", (2 * TW + 8, 3 * (TH + LAB) + 16), (40, 40, 40))
        for k, n in enumerate(part):
            im = Image.open(EPD / f"{n}.jpg").convert("RGB")
            im.thumbnail((TW, TH), Image.LANCZOS)
            x, y = (k % 2) * (TW + 8), (k // 2) * (TH + LAB + 8)
            sheet.paste(im, (x + (TW - im.width) // 2, y + LAB + (TH - im.height) // 2))
            d = ImageDraw.Draw(sheet)
            r = db[n]
            d.text((x + 4, y + 4), f"{n}  {r['w']}x{r['h']}  {r['cut']}  {'額' if r['frame'] else ''}", fill=(255, 255, 0))
        p = SCRATCH / f"{tag}_{i // 6 + 1:02d}.jpg"
        sheet.save(p, quality=90)
        outs.append(p)
        print(f"→ {p}（{' '.join(part)}）")
    return 0


def cmd_crop(code, x0, y0, x1, y1, k=2.0):
    """束の画素の切り出し（k 倍・束の画素で 10px ごとの目盛り）＝out/ep33_look/crop_<名>_<x0>_<y0>.jpg"""
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
    p = SCRATCH / f"crop_{n}_{x0}_{y0}.jpg"
    im.save(p, quality=92)
    print(f"→ {p}（{im.size[0]}x{im.size[1]}・{k}倍）")
    return 0


def cmd_panel():
    """ルール 0b-34②：PANEL_AR＝束の縦横比の並びで、16:9 より縦長の側のいちばん大きな切れ目の中点。"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    ars = sorted((r["w"] / r["h"], n, r["w"], r["frame"]) for n, r in db.items())
    for a, n, w, fr in ars:
        print(f"  {a:6.3f}  {n:8} 幅 {w}{'  額装だけ' if fr else ''}{'  （1280 未満＝kind() は額装）' if w < 1280 else ''}")
    side = [x for x in ars if x[0] < 16 / 9]
    gaps = sorted(((side[i + 1][0] - side[i][0], side[i], side[i + 1]) for i in range(len(side) - 1)), reverse=True)
    for g, a, b in gaps[:4]:
        print(f"切れ目 {g * 100:5.1f}ポイント：{a[0]:.3f}（{a[1]}）→ {b[0]:.3f}（{b[1]}）＝中点 {(a[0] + b[0]) / 2:.4f}")
    return 0


def cmd_edges():
    """束の全点＋VTS のひかえの静止画の四辺の暗い帯（門番 check_photo_edge.margins と同じ物差し）＝スライドの台紙の縁がある写真の名簿を決める"""
    sys.path.insert(0, str(HERE / "tools"))
    import check_photo_edge as PE
    db = json.loads(DB.read_text(encoding="utf-8"))
    hits = []
    names = sorted(db) + sorted(p.stem for p in EPD.glob("fb_*.jpg"))
    for n in names:
        m = PE.margins(f"ep33/{n}.jpg")
        mx = max(m.values())
        flag = "🔴" if mx >= PE.MIN_EDGE else ("・" if mx > 0 else " ")
        if mx > 0:
            hits.append((n, m))
        print(f"{flag} {n:10} 左 {m['l'] * 100:4.1f}% 上 {m['t'] * 100:4.1f}% 右 {m['r'] * 100:4.1f}% 下 {m['b'] * 100:4.1f}%"
              f"  {(db.get(n) or {}).get('era', '#15 のひかえ')[:16]}")
    big = [n for n, m in hits if max(m.values()) >= PE.MIN_EDGE]
    print(f"→ {len(names)}点のうち暗い帯のある点 {len(hits)}（うち {PE.MIN_EDGE * 100:.1f}% 以上 {len(big)}＝{' '.join(big) or 'なし'}）")
    return 0


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
CREDIT_W_MAX = 56.5          # 出典の行の字幅の上限の目安（全角＝1・半角＝0.55）＝23本目の最長。本当の物差しは門番 layout


def _width(s):
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.55 for c in s)


def cmd_credits(write=False):
    """撮影年＝year_of（出どころつき）。主に当てたカットの副題が名乗る年（「NNNN年」）と食い違えば止める（地に使うカットの副題は図の中身＝照らさない）。
    作者の名乗り（scene_jiko._ep33_person）を当てて出典の行の字幅を測る（名前は出さない＝字数だけ）"""
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
        leak = hits_in(json.dumps(r, ensure_ascii=False), names)      # 33本目は頁の URL（Commons の題）も当てる（Flickr の直リンクは書かない）
        if leak:
            print(f"🔴 {n}: 台帳の行に出さない名前が入っている（{len(leak)}語）")
            bad += 1
        line = r["credit"]
        if "{帰属}" in line:
            print(f"🔴 {n}: 印 {{帰属}} は使わない（8列目は許諾の雛形の取り違え＝画面は {AUTHOR}）")
            bad += 1
        if AUTHOR in line:
            try:
                line = line.replace(AUTHOR, SJ._ep33_person(f"ep33/{n}.jpg", AUTHOR))
            except Exception as e:                     # noqa: BLE001  焼く前に止める
                print(f"🔴 {n}: 名乗りが作れない（{e}）")
                bad += 1
        wd = _width(line)
        # 🆕 ⑤b-2（11-15）：字数の目安（56.5）でなく、描く道具の物差し（scene_jiko.fm.width・24px の Noto）で測った幅で止める。
        #    置ける幅＝画面の右の余白 RIGHT から左の余白 MG まで（全面は MG から左寄せ・額装は RIGHT へ右寄せ＝どちらも同じ幅）から暗い地の余白 28px を引いた幅
        px = SJ.fm.width(line, 24, "Noto")
        room = SJ.J.RIGHT - SJ.J.MG - 28
        if px > room:
            print(f"🔴 {n}: 出典の行の幅 {px:.0f}px（置ける幅 {room}px を越える＝画面の外へ出る）")
            bad += 1
        elif wd > CREDIT_W_MAX:
            print(f"⚠️ {n}: 出典の行の字幅 {wd:.1f}（目安 {CREDIT_W_MAX} を越える）・本物の幅 {px:.0f}px（置ける幅 {room}px の内）")
        cj[f"ep33/{n}.jpg"] = r["credit"]
        kind = ("公開調査の報告の図（紙面の引用）" if r.get("page")
                else "イメージ＝この回の物でない・束の外" if r.get("stock") else "この回の物と場所")     # 🆕 ⑤b-4a：Pexels は「イメージ」
        mod = ("・顔と字に升目" if "顔と字" in r["credit"] else "・字に升目" if "字にモザイク" in r["credit"] else "・顔に升目") if r.get("mosaic") else ""
        use = " ".join(cuts) + (f"（地 {r['ji']}）" if r["ji"] else "")
        url = r["url"]
        rows.append(f"| `{Path(n).name}` | {use or '—'} | {y if y else '不明'} | {r['lic']}（{kind}{mod}） | {r['who']} | {url} |")
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
        films = _film_codes()
        for k, v in json.loads(CLIPS.read_text(encoding="utf-8")).items():
            film_rows.append(f"| `{k}` | {' '.join(films.get(k, []))} | {v['credit']} | {v['license']} | {v['url']} | {v['got']} |")
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-11-15（⑤b-2）。`qa_out/ep33_assets.py credits --write` が書く（手で直さない）。写真と映像は映像方針の一覧 `ref/ep33/eizou_list33.md`（了承② 2026-11-15）。",
        "🔴 この回の線（台本 §1-4）＝住民（亡くなった人・生き残った人・出火した部屋の住人）は名前なし・消防士と指揮者は立場・調査の委員長と大臣と区の幹部は役職・"
        "社員と専門家は役職。撮影者の名前もこのリポに書かない。写真の中の名札と車の番号の字は読ませない。追悼の場と支援の掲示は使わない。",
        "",
        "### 0. 素材の読み（⚠️ 法律の助言ではない＝こちらの読み）",
        "- Commons の写真＝頁の許諾の箱で読んだ（11-14〜15）。CC BY 2.0・4.0＝帰属と改変の旨（全面は「改変：切出」）。BY-SA 2.0・4.0＝額装・無加工・1点1カット・升目もかけない。"
        "CC0＝表示は任意（撮影者の名乗りは書かない）",
        "- 公開調査の報告の図（グレンフェル・タワー調査 第1段階の報告〈2019〉ほか）＝紙面の引用。報告そのものは英国の公的な機関の刊行物（OGL v3.0）だが、"
        "図の中のコマは住人の携帯電話の映像・警視庁のヘリコプターの映像など第三者のもの＝図の番号と題の行ごと・額装・無加工・サムネに使わない（ルール §2-6c・§2-42）",
        "",
        "### 1. 写真と報告の図（Commons の CC BY 2.0・4.0・BY-SA 2.0・4.0・CC0／公開調査の報告の図）",
        "- CC BY・BY-SA＝「写真：{作者}／Wikimedia Commons（ライセンス）」。🔴 撮影者の名前はこのリポに書かない＝`ref/ep33/credits.json` は印 `{作者}` だけ・"
        "焼くときに git の外の表 `ref/ep33/src/credits_private.tsv` の2列目から足す（`tools/scene_jiko.ep33_credit`）",
        "- 私人の顔は CC BY・CC0 で升目（「／改変：…にモザイク」）。BY-SA に読める私人の顔があれば使わない。色は原本のまま（[21]・[23]・[24]・[25] は白黒の原本）",
        "- 説明カットの地（「地 c…」）＝CC BY・CC0 の昼の写真を暗くするだけ（字と地の比 8:1 が下限・出典の行は「地の写真：…／改変：切出・明るさ」）。"
        "🔴 夜明けと夜の写真・BY-SA・Google の衛星写真・[24]（枝が細かい）・[58] は地にしない",
        "- 撮影年＝Commons の頁の撮影日（`sources33.psv` の時期の欄）。報告の図＝コマの時刻は図の前の本文の1文（`make_list33.FIG_ERA`）",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. 動く映像＝clips.json（#15 GRENFELL.webm）",
        "- Commons の映像 1本（CC BY 3.0・1920×1080・毎秒25コマ・Vimeo の公開 2017-07-10）＝ロンドンの空撮と焼けた塔。等速（速さを変えない）・止めなし・頭から使う・同じ秒を2回使わない・"
        "場面の切れ目をまたがない（`make_list33.SCENE_CUTS`）。人の写る秒・ビルの広告と建物の名の看板・頭と尻の黒は使わない（`footage.NOGO`）。音は使わない",
        "- 出典の行＝「映像：{作者}／Wikimedia Commons（CC BY 3.0）／改変：切出」（撮影者は git の外の表から焼くときに足す）。🔴 映像そのものは git に入れない（焼くときに Commons の 1080p の版を取る）・"
        "ひかえの静止画は公開リポに置く（CC BY 3.0）",
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


# ── #15＝台帳 clips.json・ショット shots.json・USE・ひかえ ──────────
# 🆕 ⑤b-2（11-15）：Commons の映像 GRENFELL.webm（CC BY 3.0・250.38秒・Vimeo の公開 2017-07-10）＝台帳の鍵は **GV15**
#    （🔴 32本目の台帳の鍵 V15〈VTS の15分後〉と名が同じ＝取り違えないよう33本目は GV15。一覧の記号 V15 は FILM_KEY で引く）。
#    媒体＝Commons の 1080p の版（VP9・1920×1080・毎秒25コマ・正方画素・74,187,211 B＝11-15 に HEAD で 200・video/webm）。
#    手元の写し＝了承②で取った 1080p の区間3つ（`-c copy`＝ファイルの0秒は元の 18.327・118.207・172.327秒の手前のキーフレーム＝`HEADS`）と 240p の全体。
#    🔴 黒い帯なし（11-15 に使う6区間の6コマずつの平均＝暗い行・列 0＝scratchpad v15probe33.py）＝footage.PILLAR は書かない・寄り 1.0。音は使わない
FILM_KEY = {"V15": "GV15"}
FILM = {"GV15": dict(name="GRENFELL", page="https://commons.wikimedia.org/wiki/File:GRENFELL.webm",
                     media="https://upload.wikimedia.org/wikipedia/commons/transcoded/1/14/GRENFELL.webm/GRENFELL.webm.1080p.vp9.webm",
                     size=74187211, what="ロンドンの空撮と焼けた塔（Vimeo の公開 2017-07-10＝撮影の日は分からない）")}
V15_DIR = SRC / "commons" / "c33"
HEADS = {"V15_1080p_0019_0037.webm": 18.327, "V15_1080p_0123_0140.webm": 118.207, "V15_1080p_0174_0236.webm": 172.327}
V15_FULL = "V15_240p.webm"
# 外す秒＝make_list33.EXCLUDE（元の映像の秒・前後 MARGIN 0.25秒は一覧の門番が足す）＝footage.NOGO の印 EP33_NOGO のあいだに書く
# 額の中の寄りと寄せ＝33本目の #15 は全面・1倍（書かない）
VTS_GEOM = {}


def _film_codes():
    """台帳の鍵（GV15）→ 使うカット（一覧の順）。一覧の記号（V15）は FILM_KEY で引く"""
    src = _sources()
    out = {}
    for r in _list():
        code = _code_of(r["main"])
        if src.get(code, {}).get("type") in FILM_TYPES:
            if code not in FILM_KEY:
                raise SystemExit(f"🔴 {r['cid']} {code}: 映像の記号が FILM_KEY に無い")
            out.setdefault(FILM_KEY[code], []).append(r["cid"])
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
    """HEAD（中身を取らずに大きさと型だけ聞く）。🆕 11-10：Commons は続けて引くと 429（多すぎる）を返した＝待って4回まで引き直す（1本ごとに2秒あける）"""
    import time
    import urllib.error
    for k in range(4):
        time.sleep(2 + 15 * k)
        try:
            req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, int(r.headers.get("Content-Length") or 0), r.headers.get("Content-Type") or ""
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == 3:
                raise
            print(f"     ⚠️ 429（{k + 1}回目）＝待って引き直す")


def _local_v15():
    """手元の写し（1080p の区間3つと 240p の全体）が取得の記録 fetch33.tsv の md5（2回）と同じか＝[(ファイル, 元の映像の頭の秒, 長さ)]"""
    fet = {Path(r["file"]).name: r for r in _fetched().values() if (r.get("kind") or "") == "video"}
    out = []
    for name in list(HEADS) + [V15_FULL]:
        p = V15_DIR / name
        r = fet.get(name)
        if not p.exists() or not r or r["md5_1"] != r["md5_2"] or md5(p) != r["md5_1"]:
            raise SystemExit(f"🔴 #15 の手元の写し {name} が無いか md5 が fetch33.tsv と違う")
        out.append((p, HEADS.get(name, 0.0), _probe(p)["sec"]))
    return out


def cmd_clips():
    """clips.json＝#15 の1本。手元の写しの md5 を fetch33.tsv と照らし、1080p の版の直リンクを HEAD で引いて大きさと型を見る（取れない映像は黙って静止画に落ちる＝焼く前に引く）。
    🔴 出典の行は印 `{作者}`（git の外の表の V15 の行の2列目＝焼くときに scene_jiko.credit_of が差す）"""
    src = _sources()
    out = {}
    loc_files = _local_v15()
    prv = _private_rows()
    for key, cuts in _film_codes().items():
        code = next(c for c, k in FILM_KEY.items() if k == key)
        s = src[code]
        f = FILM[key]
        if code not in prv or not prv[code][AUTHOR_COL].strip():
            raise SystemExit(f"🔴 {code}: git の外の表に #15 の撮影者の行が無い（出典の行に名前が要る＝CC BY 3.0）")
        st, n, ct = _head(f["media"])
        if st != 200 or n != f["size"] or not ct.startswith("video/"):
            raise SystemExit(f"🔴 {key}: Commons の 1080p の版の直リンクが記録と違う（http {st}・{n} B／記録 {f['size']} B・{ct}）")
        loc = _probe(loc_files[0][0])
        full = _probe(V15_DIR / V15_FULL)
        cr = s["credit"].replace("（CC BY 3.0）", "（CC BY 3.0）／改変：切出") if "改変" not in s["credit"] else s["credit"]
        out[key] = dict(url=f["page"], media=f["media"], credit=cr, src="commons", at=0.0, date="2017-07-10", stock=False, what=f["what"], got="2026-11-15",
                        w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(full["sec"], 3), size=f["size"], dispw=loc["w"],
                        decoded=[loc["w"], loc["h"]], license="CC BY 3.0", rights="CC BY 3.0（Commons の頁の許諾の箱＋Vimeo のライセンスの照合＝映像方針）",
                        scan="ref/ep33/src/commons/c33/" + V15_FULL, local_off=0.0, content_x=[0, loc["w"]], person=code,
                        sections={p.name: dict(head=h, sec=round(d, 3)) for p, h, d in loc_files if p.name in HEADS},
                        note="音は使わない。手元の写し（git の外）＝1080p の区間3つ（`-c copy`・0秒は元の 18.327・118.207・172.327秒）と 240p の全体（md5 は fetch33.tsv）。"
                             "黒い帯なし（6区間を測った）＝全面・PILLAR なし・寄り 1.0。等速・止めなし・場面の切れ目をまたがない（make_list33.SCENE_CUTS）")
        print(f"  {key:5} {loc['w']}x{loc['h']} {loc['fps']}fps 全体 {full['sec']:7.3f}秒 {f['size'] / 1e6:.1f}MB SAR {loc['sar']}  {' '.join(cuts)}  HEAD {st}（{ct}）")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep33/clips.json（{len(out)}本）")
    return 0


def cmd_shots():
    """shots.json＝#15 の場面の切れ目（`make_list33.SCENE_CUTS`＝⑤b-1 に 240p の全体を ffmpeg の場面の変わり目〈scene＞0.20〉で測った32か所）を写す＝測り直さない。
    🔴 1080p の区間3つでも同じ秒だった（⑤b-1）。切れ目と切れ目のあいだを1本のショットに（動く空撮から T1 へのつなぎ 174.887〜175.767 の4つも1つずつ）"""
    sys.path.insert(0, str(BUILD))
    import make_list33 as ML
    out = {}
    for key in _film_codes():
        code = next(c for c, k in FILM_KEY.items() if k == key)
        cuts = list(ML.SCENE_CUTS[code])
        if cuts != sorted(cuts) or len(set(cuts)) != len(cuts):
            raise SystemExit(f"🔴 make_list33.SCENE_CUTS の {code} が昇順でないか重なる")
        dur = round(_probe(V15_DIR / V15_FULL)["sec"], 3)
        b = [0.0] + cuts + [dur]
        sh = [dict(start=x, until=y, motion=0.0) for x, y in zip(b, b[1:])]
        out[key] = dict(src=FILM[key]["media"], scan="ref/ep33/src/commons/c33/" + V15_FULL, dur=dur,
                        how="⑤b-1（11-15）：240p の全体を ffmpeg の場面の変わり目（scene＞0.20）で測った32か所（make_list33.SCENE_CUTS）＝編集の切れ目"
                            "（20.967・28.327・35.567・216.647 は隣のコマの差が1コマだけ跳ねる硬いカット・1080p の区間3つでも同じ秒）。⑤b-2 は写しただけ",
                        moves=[dict(head=t, tail=t, frames=1, peak=0.0) for t in cuts], shots=sh)
        print(f"  {key:5} {dur:7.3f}秒  切れ目 {len(cuts)}：" + " ".join(format(t, "g") for t in cuts))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep33/shots.json（{len(out)}本）")
    return 0


def _write_block(tag, lines):
    txt = FOOTAGE.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in txt else "\n"              # 🔴 25本目 ⑤b-1 の落とし穴＝改行を見分ける
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_bytes((txt[:m.start(2)] + "".join(x + nl for x in lines) + txt[m.end(2):]).encode("utf-8"))


def film_nogo():
    """外す秒 {台帳の鍵: [(頭, 尻, 理由)]}＝make_list33.EXCLUDE（元の映像の秒）を、その秒を含む場面まるごとに広げる（場面の切れ目＝SCENE_CUTS）。
    頭（尻）のすぐ内側 0.3秒に切れ目があれば、EXCLUDE の秒のまま（0.25秒きざみで決めた秒が切れ目の手前に丸まっている＝隣の場面まで広げない）。
    それ以外は場面の頭（尻）まで広げる＝狭めない（EXCLUDE の秒より内側にはしない）"""
    sys.path.insert(0, str(BUILD))
    import make_list33 as ML
    out = {}
    for code, a, b, why in ML.EXCLUDE:
        key = FILM_KEY[code]
        cuts = [0.0] + list(ML.SCENE_CUTS[code]) + [round(_probe(V15_DIR / V15_FULL)["sec"], 3)]
        if any(a < c <= a + 0.3 for c in cuts):
            s0 = a
        else:
            s0 = max(c for c in cuts if c <= a)
        if any(b - 0.3 <= c < b for c in cuts):
            s1 = b
        else:
            s1 = min(c for c in cuts if c >= b)
        out.setdefault(key, []).append((round(min(a, s0), 3), round(max(b, s1), 3), why))
    return out


def cmd_use(only=None, all_=False):
    """footage.USE の33本目の欄。区間は一覧 list33.tsv の動きの欄「映像 a〜b秒」から読む（make_list33 の門番 gate_video と同じ物差し）＝等速・止めなし・頭から読む。
    🔴 読む秒（頭＋要る秒）が区間の尻を越えれば止める・外す秒に掛かれば止める・場面の切れ目をまたぐ欄は ALLOW_CROSS（決めた替わり）だけ＝edit=True。
    🔴 章ファイルに `ss.vid` を書いたカットだけ（`only` は書く前の鶏と卵を割るため・`--all` は全欄＝門番に通すとき）"""
    sys.path.insert(0, str(HERE / "tools"))
    sys.path.insert(0, str(BUILD))
    import make_list33 as ML
    if only or all_:
        spec = {}
    else:
        import scene_jiko as S
        import cuts as CU
        # 🔴 11-10：章ファイルが読めないと SPEC からその章が黙って抜ける＝「映像を書いたカット0」と読んで USE を0欄で書いた（fail open）＝読めない章があれば止める
        if CU.BROKEN:
            raise SystemExit(f"🔴 章ファイルが読めない（{', '.join(f'{k}: {v}' for k, v in CU.BROKEN.items())}）＝USE を書かない")
        spec = S.SPEC
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    lines, skip = [], []
    films = _film_codes()
    nogo = film_nogo()
    for r in _list():
        code = FILM_KEY.get(_code_of(r["main"]))
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
        if re.search(r"止め|倍|速", r["motion"]):
            raise SystemExit(f"🔴 {cid}: #15 は等速・止めなし（一覧の動きの欄 {r['motion']}）")
        need = float(r["cont"])
        if a + need > b + 1e-6:
            raise SystemExit(f"🔴 {cid}: 読む秒 {need:.2f} が区間 {b - a:.2f} を越える（区間の尻を延ばすか秒を詰める）")
        for x0, x1, why in nogo.get(code, []):
            if a + need > x0 and a < x1:
                raise SystemExit(f"🔴 {cid}: {a:g}〜{a + need:.2f} が外す秒 {x0}〜{x1}（{why}）に掛かる")
        mv = [m for m in sd[code]["moves"] if a + ML.SCENE_EDGE < m["head"] < a + need - ML.SCENE_EDGE]
        allow = set(ML.ALLOW_CROSS.get(cid, ()))
        if {m["head"] for m in mv} - allow:
            raise SystemExit(f"🔴 {cid}: {a:g}〜{a + need:.2f} が場面の切れ目 {sorted({m['head'] for m in mv} - allow)} をまたぐ（決めた替わり ALLOW_CROSS に無い）")
        if allow - {m["head"] for m in mv}:
            raise SystemExit(f"🔴 {cid}: 決めた替わり {sorted(allow)} が読む秒の中に無い（区間が替わった＝ALLOW_CROSS を直す）")
        sh = [x for x in sd[code]["shots"] if x["start"] <= a < x["until"]]
        geo = "".join(f", {k}={v}" for k, v in VTS_GEOM.get(cid, {}).items())
        lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate=1.0{geo}{", edit=True" if mv else ""}),   '
                     f'# 読む {need:.2f}秒（〜{a + need:.2f}）／区間 {b - a:.2f}秒・場面 {sh[0]["start"]:g}〜{sh[0]["until"]:g}'
                     + (f"・🔧 決めた場面の替わり {' '.join(format(m['head'], 'g') for m in mv)}（decisions33e §5-9）" if mv else ""))
    if all_:
        print("（--all＝書かずに全欄を出す）")
    else:
        _write_block("EP33_USE", lines)
        _write_block("EP33_NOGO", [f'    "{k}": {v!r},' for k, v in nogo.items()])
        print(f"→ tools/footage.py USE {len(lines)}欄・NOGO {sum(len(v) for v in nogo.values())}区間")
    for k, v in nogo.items():
        for x0, x1, why in v:
            print(f"  NOGO {k} {x0:g}〜{x1:g}（{why}）")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵・章の扉の地）＝区間の頭のコマ（手元の 1080p の区間ファイル・1920×1080）
    ＝`ref/ep33/fb_<cid>.jpg`（CC BY 3.0・公開リポに置く）。🔴 区間ファイルの0秒は元の 18.327・118.207・172.327秒＝その差を引いて出力シークで取る"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    from PIL import Image
    bad = 0
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
        c = FO.CLIPS.get(u["clip"]) or {}
        if not str(c.get("scan", "")).startswith("ref/ep33/"):
            continue
        st = float(u["start"])
        sec = [(n, d) for n, d in (c.get("sections") or {}).items() if d["head"] <= st < d["head"] + d["sec"]]
        if len(sec) != 1:
            print(f"🔴 {cid}: {st:.2f}秒を含む手元の区間ファイルが1つでない（{[n for n, _ in sec]}）")
            bad += 1
            continue
        name, d = sec[0]
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(V15_DIR / name), "-ss", f"{st - d['head']:.3f}", "-frames:v", "1",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not raw:
            print(f"🔴 {cid}: コマが取れない")
            bad += 1
            continue
        dst = EPD / f"fb_{cid}.jpg"
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        im.save(dst, quality=92)
        print(f"✓ {cid:5} {u['clip']:5} {st:7.2f}秒（{name} の {st - d['head']:.3f}秒）{im.size[0]}x{im.size[1]} → {dst.relative_to(HERE).as_posix()}")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"panel": cmd_panel, "edges": cmd_edges, "clips": cmd_clips, "shots": cmd_shots, "build": cmd_build}
    if a and a[0] == "uses":
        _later = {}
        for _k, _u in sorted(uses(_later).items()):
            print(f"{_k:8} 主 {' '.join(_u['main']) or '—':24} 地 {' '.join(_u['ji']) or '—'}")
        for _j, _cs in _later.items():
            print(f"・{_j}：{len(_cs)}カット")
        sys.exit(0)
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] == "use":
        sys.exit(cmd_use(set(x for x in a[1:] if not x.startswith("--")) or None, "--all" in a))
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "sheet":
        sys.exit(cmd_sheet(a[1:]))
    if a and a[0] == "crop":
        sys.exit(cmd_crop(a[1], *map(int, a[2:6]), float(a[6]) if len(a) > 6 else 2.0))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
