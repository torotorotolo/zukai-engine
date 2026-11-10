# -*- coding: utf-8 -*-
"""ep32_assets.py — 32本目（USエアウェイズ1549便のハドソン川への着水）の写真の束・出典・VTS の台帳（⑤b-2・2026-11-10）。31本目 `ep31_assets.py` の写し。
31本目の紙面（判決・国会会議録）と国土地理院の空中写真・防衛庁記録の枝は外した（32本目に無い）。32本目の素材＝`sources32.psv` の13列・`fetch32.tsv`〈md5 を2回〉・
git の外の表 `src/credits_private.tsv`〈Commons の撮影者＝頭の行なし・9列＝code・title・author・rights・exif・頁・縦横・attr・許諾の札〉。
束に入れるのは Commons の写真（commons-photo）と NTSB の公開ドケットの調査の写真（docket-photo）。紙面（public-page 17点・一覧の「公的」21カット）は ⑤b-3＝数えて出すだけ。
イメージ（Pexels）は ⑤b-4＝束に入れない。VTS（沿岸警備隊の監視カメラ VC・V15・V20）は clips.json・shots.json（`clips`・`shots`・`use`・`fb`）。

  python -P qa_out/ep32_assets.py dk               # ドケットの PDF から調査の写真13点を取り出す（公的＝許可不要）＝src/ntsb/photos/<記号>.* と log.tsv（git の外）
  python -P qa_out/ep32_assets.py uses             # 束の鍵とカット（主・地）
  python -P qa_out/ep32_assets.py build            # 束 ref/ep32/<名>.jpg ＋ 権利の台帳 ref/ep32/assets.json
  python -P qa_out/ep32_assets.py sheet <名…>      # 1枚 640幅の 2列×3行のシート（out/ep32_look/・人の写りを当たる＝事故検証ch の決め）
  python -P qa_out/ep32_assets.py crop <名> x0 y0 x1 y1 [倍]   # 束の画素の切り出し（既定2倍・10px の目盛り）＝人と字を決めるとき
  python -P qa_out/ep32_assets.py panel｜edges     # ss.PANEL_AR の切れ目／門番 check_photo_edge の名簿（SLIDE_MOUNT／SLIDE_NOT_MOUNT）＝ひかえの静止画も測る
  python -P qa_out/ep32_assets.py credits [--write]  # 画面の出典 ref/ep32/credits.json と ref/CREDITS.md の32本目の節
  python -P qa_out/ep32_assets.py clips｜shots     # VTS 3本の台帳（HEAD で大きさを照らす）・場面の切れ目（コマの灰色の差）
  python -P qa_out/ep32_assets.py use [cid…|--all] # footage.USE の32本目の欄（一覧の動きの欄「映像 a〜b秒」から・等速）と NOGO
  python -P qa_out/ep32_assets.py fb [cid…]        # ひかえの静止画 ref/ep32/fb_<cid>.jpg（区間の頭のコマ・384×288 のまま＝PD-USCG＝公開リポに置く）

🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色）＝幅 2400 か高さ 1350 の大きい方まで（小さい写真は原画のまま＝引き伸ばさない）。
🔴 調査の写真＝PDF に埋め込まれた絵そのもの（JPEG はそのままの字列・JPEG 2000 と PNG は画素を解いて PNG）＝頁を描き直さない（頁の上の字や矢印は入らない）。
🔴 この回の線（台本 §1-4）＝名前を出すのは機長と副操縦士だけ＝写真の中の人の名前の字（上着・船の名）は読ませない（親が原寸で見て升目か切り落とし）。
   名前は台帳・出典の行・CREDITS.md に書かない＝撮影者は印 `{作者}` だけ（焼くときに `scene_jiko._ep32_person` が git の外の表の3列目から足す）。
🔴 人（了承②）＝公的な任務の顔はそのまま。私人の顔は CC BY・CC0・PD で升目（MASK）・**BY-SA は升目も翻案＝かけない**（読める顔があれば別の点に）。
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
EPD = HERE / "ref" / "ep32"
SRC = EPD / "src"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list32.tsv"
SOURCES = BUILD / "sources32.psv"
FETCHES = (BUILD / "fetch32.tsv",)
PRIVATE = SRC / "credits_private.tsv"         # 🔴 git の外（Commons の撮影者＝頭の行なし・9列）＝ここから名前を公開の物へ写さない
NAME_FILES = (SRC / "names_private.txt", SRC / "names_commons.txt")     # 🔴 git の外（出さない名前＝乗客・客室乗務員・管制官・救助の人・撮影者ほか）
COMMONS_PAGES = SRC / "commons" / "pages32"   # 🔴 git の外（映像方針で取った Commons の頁の写し＝許諾の箱の「Attribution:」を照らす）
COMMONS_DIR = SRC / "commons" / "c32"         # git の外（Commons の写真の原本・標準の縮小版）
DOCKET = SRC / "ntsb" / "docket"              # git の外（NTSB の公開ドケットの PDF＝② で取った・md5 の記録 `_log_1794223236.json`）
DOCKET_LOG = DOCKET / "_log_1794223236.json"
DK_OUT = SRC / "ntsb" / "photos"              # 🆕 ⑤b-2：取り出した調査の写真（git の外）
DK_LOG = DK_OUT / "log.tsv"
DB = EPD / "assets.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
FOOTAGE = HERE / "tools" / "footage.py"
UA = "zukai-engine-research/1.0 (GitHub torotorotolo/zukai-engine)"
SCRATCH = HERE / "out" / "ep32_look"          # sheet・crop の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## USエアウェイズ1549便のハドソン川への着水（2009-01-15・32本目）"
AUTHOR = "{作者}"            # CC BY・BY-SA・CC0 の出典の行の印（焼くときに git の外の表の3列目から足す＝scene_jiko.ep32_credit）
EVENT_YEAR = 2009            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 92
MOSAIC_PX = 14                         # 升目の大きさ（束の画素）
COMMONS_TYPES = ("commons-photo",)     # Commons の写真（当日〜その後のこの機体・博物館の展示＝CC BY 2.0・BY-SA 3.0・CC0・PD）
DOCKET_TYPES = ("docket-photo",)       # NTSB の公開ドケットの調査の写真（PD の見込み＝米国の連邦の業務・撮影者の記載なし）
PHOTO_TYPES = COMMONS_TYPES + DOCKET_TYPES
PAGE_TYPES = ("public-page",)          # 報告書・ドケット・連邦官報の紙面＝⑤b-3（束の外＝数えて出す）
STOCK_TYPES = ("stock",)               # 束に入れない（⑤b-4）
FILM_TYPES = ("commons-video",)        # VTS＝clips.json（束の外）
KIND_OK = {"写真": COMMONS_TYPES, "調査": DOCKET_TYPES, "公的": PAGE_TYPES}
KIND_OUT = ("映像", "衛星", "イメージ")              # 束の外＝映像は clips.json・衛星は ss.SAT（⑤b-3）・イメージは ⑤b-4
_YEAR = re.compile(r"((?:19|20)\d\d)")

# 🆕 調査の写真の取り出し {記号: (PDF の頭の番号, 頁〈1から〉, xref, 頁の札の字, 札の置き方)}。🔴 札に当たる絵が xref と同じでなければ止める（取り違え）
#    札の置き方＝"below"（札は絵の下＝#49・#101 は絵の下の端に約11pt 重なる）・"above"（札は絵の上＝#83）・"order:N"（札が1頁の2枚ぶん1つの字のかたまり
#    ＝#68＝PDF の中の写真の並び〈頁の順・上から〉の N 枚目か＝札の番号「3.」）
#    （11-10 に scratchpad の dk32.py で頁ごとの絵と札を一覧にした＝6本とも md5 が ② の記録と同じ）
DK_PICK = {
    "D76-2": ("076", 4, 11, "Photo 2", "below"),
    "D76-4": ("076", 6, 17, "Photo 4", "below"),
    "D76-9": ("076", 11, 32, "Photo 9", "below"),
    "D79-1": ("079", 3, 6, "Photo 1", "below"),
    # 写真45＝上下2枚の組。🔴 上の絵（xref 146）は座席の配置図（骨組みの番号 61〜70・床の穴の場所の札「Floor panel perforation」）＝写真でない
    #   （11-10 に 640px のシートで見て取り違えに気づいた）。写真は下の絵（xref 147・400×265・札「Attachment of vertical beam closing cargo compartment」）
    "D79-45": ("079", 47, 147, "Attachment of vertical", "below"),
    "D49-21": ("049", 12, 67, "Photo 21.", "below"),
    "D49-42": ("049", 22, 126, "Photo 42.", "below"),     # 右上に小さな差し込みの絵（xref 127＝349×375）が重なる＝取り出すのは下の絵だけ（差し込みは入らない）
    "D49-54": ("049", 28, 161, "Photo 54.", "below"),
    "D49-56": ("049", 29, 166, "Photo 56.", "below"),
    "D101-1": ("101", 12, 33, "Photograph 1.", "below"),
    "D101-2": ("101", 13, 37, "Photograph 2:", "below"),
    "D68-3": ("068", 3, 7, "3. Photograph of NY WW", "order:3"),  # 🔴 船の名（人の名）が船体に写りうる＝原寸で見て升目か切り落とし。⚠️ sources32 の寸法の欄「1024px」は p2 の絵の幅＝写真3 は 923×616
    "D83-8": ("083", 29, 92, "Figure 8", "above"),
}

# 🆕 帰属の指定の名乗りの後ろ（許諾の箱の「Attribution: …」＝表の3列目〈作者〉＋この字）。11-10 に頁の写しと照らした（名前は出さず語の形だけ＝作者の1語＋3語）。
#    [55]＝英語版ウィキペディアから移した写真の書き方「〈作者〉 at English Wikipedia」＝画面の出典の行も `{作者}` の後ろにこの字を足す（指定どおりの名乗り）
ATTR_TAIL = {"C55": " at English Wikipedia"}
# 🆕 撮影者の欄（3列目）が機関の名前の点＝印 `{作者}` を使わず、その名前を出典の行にそのまま書く（人の名前でない＝公開リポに書いてよい）。
#    11-10 に3列目と1字も同じかを道具が照らす（違えば止める）。[13]・[14]＝陸軍工兵隊ニューヨーク地区の Flickr（26字＝焼く道具の名乗りの上限 24字を超える）
AUTHOR_ORG = {"C13": "US Army Corps of Engineers", "C14": "US Army Corps of Engineers"}

# 升目 {記号: [(x0, y0, x1, y1, 札)]}（束の画素）。札が「字：」で始まる箱＝読ませない字（船の名・上着の名）・それ以外＝顔（出典の行の断りを分ける）
#   11-10（⑤b-2）に 640px のシート9枚で全51点を当たり、疑いの所を原寸（1〜3倍）で切り出して決めた（scratchpad b2/seen32b2.tsv）
MASK = {
    "D68-3": [(234, 318, 372, 338, "字：船の名（人の名）")],                 # 船体の船の名（11-10 に2倍で見た＝読める）＝この回の線（船の名も読ませない・#68）
    "C50": [(272, 1030, 316, 1075, "来館者の顔"), (558, 1030, 615, 1080, "来館者と子どもの顔")],   # 博物館の来館者（中景・正面を向く2人と子ども・CC0）＝全面で寄る＋地6カット
    "C60": [(332, 256, 362, 272, "字：車体の小さな字（人の名前の見込み）")],   # 後ろの扉の「A…」の4字（2.5倍で見て読めた）＝人の名前か分からない＝読ませない（CC0）
    # [32]＝警察のダイバーの胸の名札（右の人の左胸と真ん中の人の右胸＝1.5〜2倍で名前が読めた・11-10 の2回目の切り出し）＝救助の人は立場だけ（PD）。顔は公的な任務＝そのまま
    "C32": [(1255, 262, 1320, 325, "字：警察官の胸の名札"), (515, 335, 565, 368, "字：警察官の胸の名札")],
    # [9]＝夜の作業の警察官の左胸の札（3倍で2行の字・読めない大きさ＝全面で寄ると大きくなる＝念のため・CC BY 2.0 は升目可）
    "C9": [(630, 633, 667, 672, "字：警察官の胸の札")],
}
# ⚠️ 升目にしない点の理由：[32]・[35]・[9]・[14]・[21]・D101-1 の顔＝警察・陸軍工兵隊・NTSB の調査（公的な任務）。[57]＝横顔の中景（主役でない・BY-SA＝升目は翻案）。
#    [26]・[44]・[45]・[46]・[59] の人＝遠景（顔は分からない）。[50] の左の端の人＝髪と肩の影だけ。[50] のリュックの人＝後ろ姿

# 束の段で切り落とす＝絵に入れない {記号: (左, 上, 右, 下)}＝元の絵に対する割合。縮める前に切る
PRE_CROP = {
    "C61": (0.0, 0.0, 1.0, 0.71),      # 🔴 袋の左下の手書きの人の名前（行 855〜940）＝切り落とす（sources32 の注・PD）。行 852 まで＝羽の付け根と「1-29-09」「US Air 1549」は残す（羽の下の端の少しと「1 of 6」・物差しは落ちる）
    "D83-8": (0.0, 0.0, 1.0, 0.9379),  # 下の白い余白と札「Photo No: DSCN….tif」（行 620〜659）＝写真は行 619 まで（11-10 に白の割合で測った）
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
    # sources32.psv は見出しを頭の注の行に書く（31本目と同じ「13列＝code|type|…|note」）＝注の行の並びと照らす
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
        for k in ("basis", "credit"):
            if d[k].startswith("同上"):
                if not prev or prev[k].startswith("同上"):
                    raise SystemExit(f"🔴 {d['code']}: {k} の「同上」が指す行が無い")
                d[k] = prev[k]
        out[f[0]] = prev = d
    return out


def _fetched():
    """{記号: 行}（取得の記録＝取った日・記号・種類・bytes・md5・md5（読み直し）・縦横・ファイル・出どころ・EXIF の撮影日時）"""
    out = {}
    for p in FETCHES:
        for r in csv.DictReader(p.open(encoding="utf-8"), delimiter="\t"):
            if r.get("種類") != "look":
                out[r.get("記号") or ""] = r
    return out


def _private_rows():
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の表）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r and not r[0].startswith("#")]
    if any(len(r) != 9 for r in rows):
        raise SystemExit(f"🔴 {PRIVATE.name} の行の欄が9でない（列の並びが変わった）")
    return {r[0]: r for r in rows}


def _private():
    """git の外の表 {記号: 作者（3列目）}。無ければ止める（束を作る手元だけで読む）"""
    return {k: r[2] for k, r in _private_rows().items()}


def _attr_ok(code):
    """🔴 8列目（attr）が空でない点＝頁の写し（git の外）の許諾の箱の「Attribution: …」が表の3列目と1字も同じか（名前は出さない＝真偽と字数だけ）。
    頁に指定が無い点は True（8列目は許諾の雛形の文の取り違え＝31本目 P1・P3 と同じ形）。頁の写しが無ければ止める（照らせない＝fail closed）"""
    import html as H
    p = COMMONS_PAGES / f"{code}.html"
    if not p.exists():
        raise SystemExit(f"🔴 {code}: Commons の頁の写し {p.name} が無い（許諾の箱の帰属の指定を照らせない）")
    t = " ".join(H.unescape(re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8"))).split())
    m = re.search(r"Attribution: (.*?) You are free", t)
    if not m:
        return True, "頁に「Attribution:」の指定なし"
    same = " ".join(m.group(1).split()) == " ".join((_private().get(code, "") + ATTR_TAIL.get(code, "")).split())
    return same, (f"頁の指定 {len(m.group(1).split())}語・3列目{'＋「' + ATTR_TAIL[code].strip() + '」' if code in ATTR_TAIL else ''}と{'同じ' if same else '違う'}")


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
_NOT_NAMES = {"投稿者", "artist", "wikipedia", "self", "photo", "own work", "flickr", "commons", "wikimedia", "user", "unknown",
              "u.s. coast guard", "u.s. army corps of engineers", "ntsb", "faa", "federal aviation administration", "national transportation safety board",
              "us army corps of engineers"}       # 🆕 [13]・[14] の3列目の綴り（機関の名前＝AUTHOR_ORG）


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


GROUND_RIGHTS = ("CC BY 2.0", "CC0", "PD")      # 地にできる権利（make_list32.JI_OK から Pexels を除いた形・BY-SA は暗くするのも翻案）


def _rights_key(s):
    r = s["rights"]
    return "PD" if r.startswith("PD") else r


def uses(later=None):
    """{束の鍵: dict(code, main=[カット], ji=[カット], full=全面に当てるカットがあるか)}（束に入る写真）。一覧の種類と出どころの型が食い違えば止める。
    紙面（公的）は ⑤b-3＝`later["公的"]` に数える。地は CC BY 2.0・CC0・PD の Commons の写真だけ（イメージの地は ⑤b-4＝束の外）"""
    sys.path.insert(0, str(BUILD))
    import make_list32 as ML
    gmap = {g for _, g in ML.GMAP}                   # イメージの地（Pexels）の記号＝make_list32.GMAP（sources32 に行は無い＝⑤b-4 で取る）
    src = _sources()
    out, bad = {}, []
    later = {} if later is None else later
    for r in _list():
        cid = r["cid"]
        c = _code_of(r["main"])
        if c in ML.NG:
            later.setdefault("差し替え待ち（make_list32.NG）", []).append(cid)      # 🆕 ⑤b-2：使わないと決めた点＝束に入れない（一覧の門番が E で止める）
        elif c and r["kind"] not in KIND_OUT:
            s = src.get(c)
            if not s:
                bad.append(f"{cid} {c}: 出どころの表に無い")
            elif r["kind"] not in KIND_OK:
                bad.append(f"{cid} {c}: 図の型「{r['kind']}」の素材の欄に記号がある（地は ji の欄）")
            elif s["type"] not in KIND_OK[r["kind"]]:
                bad.append(f"{cid} {c}: 一覧の種類「{r['kind']}」と出どころの型 {s['type']} が食い違う")
            elif s["type"] in PAGE_TYPES:
                later.setdefault("公的", []).append(cid)
            else:
                u = out.setdefault(c, dict(code=c, main=[], ji=[], full=False))
                u["main"].append(cid)
                u["full"] = u["full"] or r["frame"].startswith("全面")
        j = _code_of(r["ji"])
        if j:
            s = src.get(j)
            if (s and s["type"] in STOCK_TYPES) or (not s and j in gmap):
                later.setdefault("イメージの地", []).append(cid)
                continue
            if not s or s["type"] not in COMMONS_TYPES:
                bad.append(f"{cid} {j}: 地の写真が Commons の写真でない（{s['type'] if s else '表に無い'}）")
            elif _rights_key(s) not in GROUND_RIGHTS:
                bad.append(f"{cid} {j}: 地の写真の権利 {s['rights']} は地にできない（BY-SA は暗くするのも翻案）")
            elif s["grp"] == "night":
                bad.append(f"{cid} {j}: 夜の写真は地にしない（映像方針 §5-5）")
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
    """Commons の写真の手元のファイル（src/commons/c32/<記号>.jpg）が取得の記録（md5 を2回＝同じ）と同じか。違えば止める"""
    r = fet.get(code)
    if not r:
        raise SystemExit(f"🔴 {code}: 取得の記録が無い（fetch32.tsv）")
    p = EPD / r["ファイル"]
    if not s["file"].startswith("src/commons/c32") or p.parent.resolve() != COMMONS_DIR.resolve() or not p.exists():
        raise SystemExit(f"🔴 {code}: 手元のファイルが無いか置き場が違う（{r['ファイル']}・表の file の欄 {s['file']}）")
    h = md5(p)
    if r["md5"] != r["md5（読み直し）"] or h != r["md5"]:
        raise SystemExit(f"🔴 {code}: {p.name} の md5 が取得の記録と合わない（取り直す）")
    return p, h


def _dk_log():
    if not DK_LOG.exists():
        raise SystemExit(f"🔴 {DK_LOG.relative_to(HERE).as_posix()} が無い（`dk` で取り出す）")
    return {r["記号"]: r for r in csv.DictReader(DK_LOG.open(encoding="utf-8"), delimiter="\t")}


def _docket_ok(code, log):
    r = log.get(code)
    if not r:
        raise SystemExit(f"🔴 {code}: 取り出しの記録が無い（`dk`）")
    p = EPD / r["ファイル"]
    if not p.exists() or md5(p) != r["md5"] or r["md5"] != r["md5（読み直し）"]:
        raise SystemExit(f"🔴 {code}: {p.name} が無いか md5 が取り出しの記録と合わない（`dk` をもう一度）")
    return p, r["md5"]


def cmd_dk():
    """🆕 ⑤b-2：ドケットの PDF（② で取った・md5 を記録と照らす）から調査の写真13点を取り出す。
    🔴 札の字の行（`DK_PICK` の4つ目）のすぐ上の絵が xref と同じか（取り違えを止める）。JPEG は埋め込みの字列そのまま・ほかは画素を解いて PNG"""
    import fitz
    log = {r["file"]: r for r in json.loads(DOCKET_LOG.read_text(encoding="utf-8"))}
    DK_OUT.mkdir(parents=True, exist_ok=True)
    rows, bad = [], 0
    src = _sources()
    for code, (pre, pn, xref, cap, side) in DK_PICK.items():
        if src.get(code, {}).get("type") not in DOCKET_TYPES:
            print(f"🔴 {code}: sources32 に docket-photo の行が無い")
            bad += 1
            continue
        f = next(iter(sorted(DOCKET.glob(f"{pre}_*.pdf"))), None)
        rec = log.get(f.name if f else "", {})
        if not f or md5(f) != rec.get("md5"):
            print(f"🔴 {code}: PDF {pre}_*.pdf が無いか md5 が ② の記録と違う")
            bad += 1
            continue
        doc = fitz.open(f)
        pg = doc[pn - 1]
        caps = [b for b in pg.get_text("blocks") if cap in b[4]]
        if len(caps) != 1:
            print(f"🔴 {code}: p{pn} に札「{cap}」が {len(caps)}か所（1つでない）")
            bad += 1
            continue
        c0, c1 = caps[0][1], caps[0][3]
        if side.startswith("order:"):
            seq = [x[0] for i in range(doc.page_count) for _, x in sorted((doc[i].get_image_rects(x[0])[0].y0, x) for x in doc[i].get_images(full=True))]
            k = int(side.split(":")[1])
            ok, why = len(seq) >= k and seq[k - 1] == xref, f"PDF の写真の並び {seq}"
        else:
            # below＝札の上の辺と、札より上から始まる絵の下の辺／above＝札の下の辺と、札より下で終わる絵の上の辺。いちばん近い絵が1つに決まるか（次の絵と 20pt 以上離れる）
            near = sorted((abs(c0 - r_.y1) if side == "below" else abs(c1 - r_.y0), x[0]) for x in pg.get_images(full=True) for r_ in pg.get_image_rects(x[0])
                          if (r_.y0 < c0 if side == "below" else r_.y1 > c1))
            ok = bool(near) and near[0][1] == xref and (len(near) == 1 or near[1][0] - near[0][0] >= 20)
            why = f"近い絵 {[(round(d), x) for d, x in near[:3]]}"
        if not ok:
            print(f"🔴 {code}: p{pn} の札「{cap}」（{side}）に当たる絵が xref {xref} でない（{why}）")
            bad += 1
            continue
        info = doc.extract_image(xref)
        if info["ext"] in ("jpeg", "jpg"):
            data, ext, how = info["image"], "jpg", "埋め込みの JPEG の字列そのまま"
        else:
            pix = fitz.Pixmap(doc, xref)
            if pix.alpha:
                pix = fitz.Pixmap(pix, 0)
            if pix.n not in (1, 3):
                pix = fitz.Pixmap(fitz.csRGB, pix)
            data, ext, how = pix.tobytes("png"), "png", f"埋め込みの {info['ext']} を画素に解いて PNG（{'灰色' if pix.n == 1 else 'RGB'}）"
        dst = DK_OUT / f"{code}.{ext}"
        dst.write_bytes(data)
        h1, h2 = md5(dst), hashlib.md5(dst.read_bytes()).hexdigest()
        rows.append(dict(記号=code, PDF=f.name, PDFのmd5=rec["md5"], 頁=pn, xref=xref, 札=cap, 縦横=f"{info['width']}x{info['height']}",
                         ファイル=dst.relative_to(EPD).as_posix(), md5=h1, **{"md5（読み直し）": h2}, 取り方=how))
        print(f"✓ {code:7} {f.name} p{pn:<3} xref {xref:<4} {info['width']}x{info['height']} {ext}  {how}")
    if bad:
        return 1
    with DK_LOG.open("w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"→ {DK_LOG.relative_to(HERE).as_posix()}（{len(rows)}点）")
    return 0


def year_of(code, s):
    m = _YEAR.search(s["era"])
    if m:
        return int(m.group(1)), f"{SOURCES.name} の時期の欄「{s['era'][:24]}」（映像方針＝頁の説明・EXIF・凡例）"
    return None, f"撮影の年の出どころが無い（時期の欄「{s['era']}」）"


def _base_credit(s):
    """sources32 の出典の欄を束の書きの頭の形に揃える：「・無加工」は「／改変なし」で言う・「・改変：切出」（[61]）は束の段の切り落とし（PRE_CROP）で言い直す
    ＝欄の字のまま残さない（切っていない点に「切出」と書かない）"""
    cr = s["credit"].replace("・無加工", "").replace("・改変：切出", "")
    if s["type"] in COMMONS_TYPES + DOCKET_TYPES and not cr.startswith(("写真：", "図：")):
        cr = "写真：" + cr
    return cr


def _mask_words(boxes):
    """升目の断りの語＝「顔」「字」「顔と字」（札が「字：」で始まる箱＝字）"""
    plate = any(str(b[4]).startswith("字：") for b in boxes)
    face = any(not str(b[4]).startswith("字：") for b in boxes)
    return "顔と字" if face and plate else "字" if plate else "顔"


def screen_credit(code, s, boxes, full):
    """画面の出典の行（了承②）＝sources32 の出典の欄＋**改変の断りを明記**：
    BY-SA＝「／改変なし」（額装・無加工）・CC BY の全面＝「／改変：切出」・CC BY の額装だけ＝「／改変なし」・CC0 と PD＝断りなし（升目と切り落としだけ書く）。
    調査の写真（PD の見込み）＝断りなし（束の段で切り落とせば「／改変：切出」）。升目は「・〇〇にモザイク」を足す"""
    if "［" in s["credit"] or "⑤b" in s["credit"] or s["credit"].startswith("同上") or not s["credit"].strip() or s["credit"] == "—":
        raise SystemExit(f"🔴 {code}: 出典の欄に書きかけの印が残る（{s['credit'][:60]}）")
    cr = _base_credit(s)
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
        return "Commons の撮影者（名前は git の外 `ref/ep32/src/credits_private.tsv` の記号の行の3列目＝画面は焼くときに足す）"
    if t in COMMONS_TYPES and r_.startswith("CC0"):
        return "表示は任意（CC0）＝撮影者の名乗りを焼くときに足す"
    if t in COMMONS_TYPES:
        return "米国の機関（public domain）"
    return "NTSB の調査グループ（撮影者の記載なし）"


def _lic(s):
    if s["type"] in DOCKET_TYPES:
        return "PD（米国の連邦の業務の見込み）"
    return s["rights"]


def cmd_build():
    from PIL import Image
    src, fet = _sources(), _fetched()
    db, bad = {}, 0
    later = {}
    us = uses(later)
    dk = _dk_log() if any(src[u["code"]]["type"] in DOCKET_TYPES for u in us.values()) else {}
    for code in list(MASK) + list(PRE_CROP):
        if code not in us:
            print(f"🔴 MASK・PRE_CROP の {code} は一覧で使っていない")
            bad += 1
    prv = _private_rows()
    for code, r in prv.items():                          # 🔴 8列目（attr）のある点＝頁の許諾の箱の帰属の指定を3列目と照らす（名前は出さない）
        if code in us and r[7].strip():
            ok, why = _attr_ok(code)
            print(f"{'・' if ok else '🔴'} {code}: 8列目 {len(r[7])}字＝{why}")
            if not ok:
                bad += 1
    for key, u in sorted(us.items(), key=lambda kv: (kv[0][0], int(re.sub(r"\D", "", kv[0].split("-")[0]) or 0), kv[0])):
        code = u["code"]
        s = src[code]
        name = bundle_name(key)
        dst = EPD / f"{name}.jpg"
        t = s["type"]
        box_m = MASK.get(code, [])
        if t in DOCKET_TYPES:
            p, smd5 = _docket_ok(code, dk)
            r = dk[code]
            notes = [f"ドケット {r['PDF']} p{r['頁']} の埋め込みの絵（xref {r['xref']}・{r['取り方']}）"]
            im, n2 = load_photo(p)
            notes += n2
        else:
            p, smd5 = _commons_ok(code, s, fet)
            im, notes = load_photo(p)
            notes.append(f"{FETCHES[0].name} の md5 と同じ（2回とも）")
        if code in PRE_CROP:
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
        if code in ATTR_TAIL:
            if AUTHOR not in cr:
                print(f"🔴 {code}: 帰属の指定の後ろの字を足す出典の行に {AUTHOR} が無い")
                bad += 1
            cr = cr.replace(AUTHOR, AUTHOR + ATTR_TAIL[code])
        if code in AUTHOR_ORG:
            if " ".join(prv.get(code, ["", "", ""])[2].split()) != AUTHOR_ORG[code] or AUTHOR not in cr:
                print(f"🔴 {code}: 機関の名前が git の外の表の3列目と違うか、出典の行に {AUTHOR} が無い")
                bad += 1
            cr = cr.replace(AUTHOR, AUTHOR_ORG[code])
        frame = "BY-SA" in s["rights"] or t in DOCKET_TYPES
        if frame and u["full"]:
            print(f"🔴 {key}: 額装だけの点（{s['rights'][:12]}・{t}）を全面のカット {' '.join(u['main'])} に当てている")
            bad += 1
        url = s["get"]
        if t in COMMONS_TYPES:
            url = (fet.get(code) or {}).get("出どころ") or url
        else:
            url = f"NTSB ドケット DCA09MA026・{dk[code]['PDF']} p{dk[code]['頁']}"
        db[name] = dict(code=code, part="", file=(dk[code]["ファイル"] if t in DOCKET_TYPES else fet[code]["ファイル"]), cut=" ".join(u["main"]), ji=" ".join(u["ji"]),
                        credit=cr, who=who_table(code, s), note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=_lic(s), frame=frame, ground=s["basis"][:120], url=url,
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False, page=False, related=False,
                        quote_page=False, named=AUTHOR in cr, mosaic=[list(b[:4]) for b in box_m] or None, name_mosaic=None,
                        masked_before=None, era=s["era"], people=s["people"], private=False, shot=None)
        print(f"✓ {key:7} {name:7} {w}x{h:<5} 主 {' '.join(u['main']) or '—':10} 地 {' '.join(u['ji']) or '—':30} {_lic(s)[:14]:14}"
              f"{'  額装だけ' if frame else ''}  {'・'.join(notes)[:60]}")
    for j, cs in later.items():
        where = {"公的": "⑤b-3 の紙面", "イメージの地": "⑤b-4 の Pexels"}.get(j, "差し替えの点は了承を得て Commons から取る")
        print(f"・{j}：{len(cs)}カット（{' '.join(cs[:10])}{' …' if len(cs) > 10 else ''}）＝束の外（{where}）")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    print(f"→ ref/ep32/assets.json（{len(db)}点＝Commons {sum(1 for r in db.values() if not r['code'].startswith('D'))}・調査 {sum(1 for r in db.values() if r['code'].startswith('D'))}"
          f"・額装だけ {sum(1 for r in db.values() if r['frame'])}・作者の印 {sum(1 for r in db.values() if r['named'])}・升目 {sum(1 for r in db.values() if r['mosaic'])}"
          f"・地に使う {sum(1 for r in db.values() if r['ji'])}・束の大きさ {tot / 1e6:.1f}MB＝全部公開リポ）")
    return 1 if bad else 0


def _find(db, c):
    for n, r in db.items():
        if n == c or r["code"] == c:
            return n
    raise SystemExit(f"🔴 束に {c} が無い")


def cmd_sheet(codes, tag="sheet"):
    """1枚 640幅の 2列×3行のシート（札＝束の名・寸法・人の欄）＝out/ep32_look/<tag>_NN.jpg。🔴 事故検証ch の決め＝640px 以上のシートで全数を当たり、疑いだけ原寸"""
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
    """束の画素の切り出し（k 倍・束の画素で 10px ごとの目盛り）＝out/ep32_look/crop_<名>_<x0>_<y0>.jpg"""
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
        m = PE.margins(f"ep32/{n}.jpg")
        mx = max(m.values())
        flag = "🔴" if mx >= PE.MIN_EDGE else ("・" if mx > 0 else " ")
        if mx > 0:
            hits.append((n, m))
        print(f"{flag} {n:10} 左 {m['l'] * 100:4.1f}% 上 {m['t'] * 100:4.1f}% 右 {m['r'] * 100:4.1f}% 下 {m['b'] * 100:4.1f}%"
              f"  {(db.get(n) or {}).get('era', 'VTS のひかえ')[:16]}")
    big = [n for n, m in hits if max(m.values()) >= PE.MIN_EDGE]
    print(f"→ {len(names)}点のうち暗い帯のある点 {len(hits)}（うち {PE.MIN_EDGE * 100:.1f}% 以上 {len(big)}＝{' '.join(big) or 'なし'}）")
    return 0


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
CREDIT_W_MAX = 56.5          # 出典の行の字幅の上限の目安（全角＝1・半角＝0.55）＝23本目の最長。本当の物差しは門番 layout


def _width(s):
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.55 for c in s)


def cmd_credits(write=False):
    """撮影年＝year_of（出どころつき）。主に当てたカットの副題が名乗る年（「NNNN年」）と食い違えば止める（地に使うカットの副題は図の中身＝照らさない）。
    作者の名乗り（scene_jiko._ep32_person）を当てて出典の行の字幅を測る（名前は出さない＝字数だけ）"""
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
                line = line.replace(AUTHOR, SJ._ep32_person(f"ep32/{n}.jpg", AUTHOR))
            except Exception as e:                     # noqa: BLE001  焼く前に止める
                print(f"🔴 {n}: 名乗りが作れない（{e}）")
                bad += 1
        wd = _width(line)
        if wd > CREDIT_W_MAX:
            print(f"🔴 {n}: 出典の行の字幅 {wd:.1f}（{CREDIT_W_MAX} まで＝画面の左下からはみ出すおそれ）")
            bad += 1
        cj[f"ep32/{n}.jpg"] = r["credit"]
        kind = "NTSB の調査の写真（公開ドケット）" if r["code"].startswith("D") else "この回の物と場所"
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
        "※2026-11-10（⑤b-2）。`qa_out/ep32_assets.py credits --write` が書く（手で直さない）。写真と映像は映像方針の一覧 `ref/ep32/eizou_list32.md`（了承② 2026-11-10）。",
        "🔴 この回の線（台本 §1-4）＝名前を出すのは機長と副操縦士だけ。乗客・客室乗務員・管制官・救助した人・撮影者の名前は書かない（立場だけ）。写真の中の上着や船の名の字は読ませない。",
        "",
        "### 0. 素材の読み（⚠️ 法律の助言ではない＝こちらの読み）",
        "- Commons の写真＝頁の許諾の箱（`licensetpl_short`）で読んだ（11-10）。CC BY 2.0＝帰属と改変の旨（全面は「改変：切出」）。BY-SA 3.0＝額装・無加工・1点1カット・升目もかけない。"
        "CC0＝表示は任意（撮影者の名乗りを書く）。PD（米国の沿岸警備隊・陸軍工兵隊・FAA・NTSB の業務）＝断りなし",
        "- [13]・[14] は頁に CC BY 2.0 と Public domain の両方の札＝CC BY 2.0 で表示（強いほうに寄せない）。[44]・[45]・[46]・[55] は GFDL の札もある＝BY-SA 3.0 で表示",
        "- NTSB の公開ドケット DCA09MA026 の調査の写真（構造・生存・救助・エンジン・野生動物の報告の付図）＝米国の連邦の業務の見込み（撮影者の記載なし・弱い所＝調査グループに会社の人も入る）。"
        "PDF に埋め込まれた絵をそのまま取り出した（頁の字と矢印は入らない）・額装",
        "",
        "### 1. 写真（Commons の CC BY 2.0・BY-SA 3.0・CC0・PD・NTSB の公開ドケット）",
        "- CC BY・BY-SA・CC0＝「写真：{作者}／Wikimedia Commons（ライセンス）」。🔴 撮影者の名前はこのリポに書かない＝`ref/ep32/credits.json` は印 `{作者}` だけ・"
        "焼くときに git の外の表 `ref/ep32/src/credits_private.tsv` の3列目から足す（`tools/scene_jiko.ep32_credit`）",
        "- 私人の顔は CC BY・CC0・PD で升目（「／改変：…にモザイク」）。公的な任務の顔（沿岸警備隊・陸軍工兵隊・警察・NTSB の調査官）はそのまま。色は原本のまま",
        "- 説明カットの地（「地 c…」）＝CC BY 2.0・CC0・PD の昼の写真を暗くするだけ（字と地の比 8:1 が下限・出典の行は「地の写真：…／改変：切出・明るさ」・CC0 と PD は改変を書かない）。"
        "🔴 夜の写真と Google の衛星写真は地にしない",
        "- 撮影年＝Commons の頁の説明と EXIF・ドケットの凡例（`sources32.psv` の時期の欄）。⚠️ 陸軍工兵隊のカメラの EXIF の時刻は場面と合わない＝副題は「2009年1月」まで",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. 動く映像＝clips.json（沿岸警備隊の監視カメラ VTS）",
        "- 米国沿岸警備隊の VTS（船の交通の監視カメラ）の記録（Commons の3本＝public domain・PD-USCG）＝384×288・毎秒3〜4コマ・音なし。等速（速さを変えない）・止めなし・額装（高さいっぱい）・"
        "地は同じ映像のぼかし。焼き込みのカメラの時計（約20秒進む）は語りと副題に使わない。背景のはしけに別の旅客機が写る秒（CrashAndRescue 402.5〜438.5秒）は使わない（`footage.NOGO`）",
        "- 出典の行＝「映像：U.S. Coast Guard（public domain）／Wikimedia Commons」（等速＝「再生速度」を言わない）。🔴 映像そのものは git に入れない（焼くときに Commons の原本を取る）・ひかえの静止画は公開リポに置く（PD）",
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


# ── VTS＝台帳 clips.json・ショット shots.json・USE・ひかえ ──────────
# 🆕 Commons の原本（ogv・Theora）＝384×288・正方画素・黒い帯なし（11-10 に scratchpad の vts32.py で全コマの時間の平均を測った＝黒い行・列 0・
#    焼き込みの字は上の行 10〜18 と下の行 269〜277 だけ＝帯でない）。🔴 4:3 の器そのもの＝footage.PILLAR は書かない（書くと額の中が寄って切れる＝31本目の落とし穴）・寄り 1.0
FILM = {"VC": dict(name="Flight1549CrashAndRescue", media="https://upload.wikimedia.org/wikipedia/commons/6/67/Flight1549CrashAndRescue.ogv",
                   what="沿岸警備隊の VTS のカメラ（着水・救助）"),
        "V15": dict(name="Flight1549After15Minutes", media="https://upload.wikimedia.org/wikipedia/commons/b/b0/Flight1549After15Minutes.ogv",
                    what="同じカメラ（着水の約15分後）"),
        "V20": dict(name="Flight1549After20Minutes", media="https://upload.wikimedia.org/wikipedia/commons/b/b3/Flight1549After20Minutes.ogv",
                    what="同じカメラ（着水の約20分後）")}
VTS_DIR = SRC / "commons" / "vts"
# 🔴 外す秒＝映像方針で見た 415〜427秒（背景のはしけに別の旅客機）を含むショットまるごと（切れ目 403.0〜403.3・427.3〜427.7・438.0＝`shots` の測り）＋前後 0.5秒
#    ＝make_list32.EXCLUDE（403.0〜438.0＋MARGIN 0.5）と同じ。footage.NOGO の印 EP32_NOGO のあいだに書く
FILM_NOGO = {"VC": [(402.5, 438.5, "背景のはしけの上に別の旅客機（コンコルド）＝この機体と取り違えられる")]}
# 🆕 額の中の寄りと寄せ（footage.USE の zoom・xbias・bias＝build_jiko が額装の映像のコマにも当てる）。
#    c101＝しぶきが1倍では細すぎる（11-10 の試し焼き 13.9秒の原寸で細い白い筋だけ）＝一覧の注「見えなければ ×2 の固定の切り出し」。
#    しぶきの通り道＝背景（コマの中央値）より明るい画素の塊が 9.67秒に x 2〜12・行 131〜137 で入り、15〜19秒に x 約60・行 138〜140（scratchpad spray32.py）
#    ＝窓 192×144 を左の端（xbias 0）・行 63〜207（bias 0.44＝縦の真ん中が行 136）に。焼き込みの字の行（上 10〜18・下 269〜277）も窓の外
VTS_GEOM = {"c101": dict(zoom=2.0, xbias=0.0, bias=0.44)}
# 切れ目の式（31本目 cuts31b の型）＝隣のコマとの灰色の差（96×72・焼き込みの字の行を外す）≥ max(8, 前後15コマ〈自分と隣を除く〉の中央値の4倍)・3コマ以内に続く山は1つ
CUT_MIN, CUT_K, CUT_WIN, CUT_JOIN = 8.0, 4.0, 15, 3


def _film_codes():
    """映像の記号 → 使うカット（一覧の順）"""
    src = _sources()
    out = {}
    for r in _list():
        code = _code_of(r["main"])
        if src.get(code, {}).get("type") in FILM_TYPES:
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


def _local_vts(code, s):
    f = FILM[code]
    p = VTS_DIR / f"{f['name']}.ogv"
    m = re.search(r"md5 ([0-9a-f]{32})", s["get"])
    if not p.exists() or not m or md5(p) != m.group(1):
        raise SystemExit(f"🔴 {code}: 手元の VTS が無いか md5 が sources32 の get の欄と違う（{p.name}）")
    return p, m.group(1)


def cmd_clips():
    """clips.json＝VTS 3本。手元の原本の md5 を sources32 と照らし、Commons の原本の直リンクを HEAD で引いて大きさと型を見る（取れない映像は黙って静止画に落ちる＝焼く前に引く）"""
    src = _sources()
    out = {}
    for code, cuts in _film_codes().items():
        s = src[code]
        f = FILM[code]
        p, h = _local_vts(code, s)
        st, n, ct = _head(f["media"])
        size = p.stat().st_size
        if st != 200 or n != size or not (ct.startswith("video/") or ct.startswith("application/ogg")):
            raise SystemExit(f"🔴 {code}: Commons の直リンクが手元と違う（http {st}・{n} B／手元 {size} B・{ct}）")
        loc = _probe(p)
        out[code] = dict(url=f"https://commons.wikimedia.org/wiki/File:{f['name']}.ogv", media=f["media"], credit=s["credit"], src="commons", at=0.0,
                         date="2009-01-15", stock=False, what=f["what"], got="2026-11-09", w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"],
                         sec=round(loc["sec"], 3), size=size, dispw=loc["w"], decoded=[loc["w"], loc["h"]], license="Public domain（PD-USCG）",
                         rights="PD（米国の沿岸警備隊の業務＝17 U.S.C. §105・Commons の PD-USCG）", scan=f"ref/ep32/src/commons/vts/{f['name']}.ogv", md5_scan=h,
                         local_off=0.0, content_x=[0, loc["w"]],
                         note="音は使わない。手元の原本（git の外）＝Commons の原本と同じ大きさ（HEAD）・md5 は sources32 の get の欄。"
                              "384×288 の器そのものが 4:3 の中身（黒い帯なし・焼き込みの字は上下の約10行）＝額装（高さいっぱい）・PILLAR なし・寄り 1.0")
        print(f"  {code:4} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.3f}秒 {size / 1e6:.2f}MB SAR {loc['sar']}  {' '.join(cuts)}  HEAD {st}（{ct}）")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep32/clips.json（{len(out)}本）")
    return 0


def _vts_edges(p):
    """場面の切れ目（カメラの寄り・振り）＝[(頭の秒, 尻の秒, コマ数, 差の山)]・長さ・コマの間"""
    import numpy as np
    pts = [float(x) for x in subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(p)],
                                            capture_output=True, text=True).stdout.split() if x.strip()]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", "scale=96:72:flags=area", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 72, 96)[:, 6:66, :].astype(np.int16)
    n = min(len(pts), a.shape[0])
    if n < 10 or len(set(round(x, 4) for x in np.diff(pts[:n]))) != 1:
        raise SystemExit(f"🔴 {p.name}: コマの時刻が等間隔でない・少ない（{n}コマ）")
    d = np.zeros(n)
    d[1:] = np.abs(np.diff(a[:n], axis=0)).mean(axis=(1, 2))
    peaks = []
    for i in range(1, n):
        nb = [d[j] for j in range(max(1, i - CUT_WIN), min(n, i + CUT_WIN + 1)) if abs(j - i) > 1]
        if d[i] >= max(CUT_MIN, CUT_K * float(np.median(nb)) if nb else CUT_MIN):
            peaks.append(i)
    groups = []
    for i in peaks:
        if groups and i - groups[-1][-1] <= CUT_JOIN:
            groups[-1].append(i)
        else:
            groups.append([i])
    dt = pts[1] - pts[0]
    return [(round(pts[g[0]], 3), round(pts[g[-1]], 3), len(g), round(float(max(d[k] for k in g)), 1)) for g in groups], round(pts[n - 1] + dt, 3), dt


def cmd_shots():
    """shots.json＝VTS 3本の場面の切れ目（カメラの寄り・振り＝監視カメラの操作。編集の切れ目ではない）"""
    src = _sources()
    out = {}
    for code in _film_codes():
        p, _ = _local_vts(code, src[code])
        ed, dur, dt = _vts_edges(p)
        b = [0.0] + [e[0] for e in ed] + [dur]
        sh = [dict(start=x, until=y, motion=0.0) for x, y in zip(b, b[1:])]
        out[code] = dict(src=FILM[code]["media"], scan=f"ref/ep32/src/commons/vts/{FILM[code]['name']}.ogv", dur=dur,
                         how=f"⑤b-2（11-10）：原本の全コマ（{1 / dt:.0f}コマ/秒・96×72 の灰色・焼き込みの字の行を外す）の隣のコマの差の山"
                             f"（差 ≥ max({CUT_MIN:g}, 前後{CUT_WIN}コマの中央値の{CUT_K:g}倍)・{CUT_JOIN}コマ以内に続く山は1つ）の頭＝ショットの切れ目"
                             "（カメラの寄り・振り＝監視カメラの操作・編集ではない）",
                         moves=[dict(head=h, tail=t, frames=k, peak=pk) for h, t, k, pk in ed], shots=sh)
        print(f"  {code:4} {dur:7.3f}秒  切れ目 {len(ed)}：" + " ".join(f"{h:g}{'〜' + format(t, 'g') if k > 1 else ''}" for h, t, k, pk in ed))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep32/shots.json（{len(out)}本）")
    return 0


def _write_block(tag, lines):
    txt = FOOTAGE.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in txt else "\n"              # 🔴 25本目 ⑤b-1 の落とし穴＝改行を見分ける
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_bytes((txt[:m.start(2)] + "".join(x + nl for x in lines) + txt[m.end(2):]).encode("utf-8"))


def cmd_use(only=None, all_=False):
    """footage.USE の32本目の欄。区間は一覧 list32.tsv の動きの欄「映像 a〜b秒」から読む（make_list32 の門番 gate_video と同じ物差し）＝等速・止めなし・頭から読む。
    🔴 読む秒（頭＋要る秒）が区間の尻を越えれば止める・外す秒に掛かれば止める・カメラの寄りをまたぐ欄は edit=True（監視カメラの操作のまま＝つないでいない）。
    🔴 章ファイルに `ss.vid` を書いたカットだけ（`only` は書く前の鶏と卵を割るため・`--all` は全欄＝門番に通すとき）"""
    sys.path.insert(0, str(HERE / "tools"))
    sys.path.insert(0, str(BUILD))
    import make_list32 as ML
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
        if hold or rate != 1.0:
            raise SystemExit(f"🔴 {cid}: VTS は等速・止めなし（一覧の動きの欄 {r['motion']}）")
        need = float(r["cont"])
        if a + need > b + 1e-6:
            raise SystemExit(f"🔴 {cid}: 読む秒 {need:.2f} が区間 {b - a:.2f} を越える（区間の尻を延ばすか秒を詰める）")
        for x0, x1, why in FILM_NOGO.get(code, []):
            if a + need > x0 and a < x1:
                raise SystemExit(f"🔴 {cid}: {a:g}〜{a + need:.2f} が外す秒 {x0}〜{x1}（{why}）に掛かる")
        mv = [m for m in sd[code]["moves"] if a < m["head"] < a + need or a < m["tail"] < a + need]
        sh = [x for x in sd[code]["shots"] if x["start"] <= a < x["until"]]
        geo = "".join(f", {k}={v}" for k, v in VTS_GEOM.get(cid, {}).items())
        lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate=1.0{geo}{", edit=True" if mv else ""}),   '
                     f'# 読む {need:.2f}秒（〜{a + need:.2f}）／区間 {b - a:.2f}秒・ショット {sh[0]["start"]:g}〜{sh[0]["until"]:g}'
                     + (f"・🔧 元のカメラの寄り・振り {' '.join(format(m['head'], 'g') + ('〜' + format(m['tail'], 'g') if m['frames'] > 1 else '') for m in mv)}"
                        "（監視カメラの操作のまま＝つないでいない）" if mv else ""))
    if all_:
        print("（--all＝書かずに全欄を出す）")
    else:
        _write_block("EP32_USE", lines)
        _write_block("EP32_NOGO", [f'    "{k}": {v!r},' for k, v in FILM_NOGO.items()])
        print(f"→ tools/footage.py USE {len(lines)}欄・NOGO {sum(len(v) for v in FILM_NOGO.values())}区間")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）＝区間の頭のコマ（384×288 のまま・器の黒なし）＝`ref/ep32/fb_<cid>.jpg`（PD-USCG・公開リポに置く）"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    from PIL import Image
    bad = 0
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
        c = FO.CLIPS.get(u["clip"]) or {}
        if not str(c.get("scan", "")).startswith("ref/ep32/"):
            continue
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{float(u['start']):.3f}", "-i", str(HERE / c["scan"]), "-frames:v", "1",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not raw:
            print(f"🔴 {cid}: コマが取れない")
            bad += 1
            continue
        dst = EPD / f"fb_{cid}.jpg"
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        im.save(dst, quality=92)
        print(f"✓ {cid:5} {u['clip']:4} {float(u['start']):7.2f}秒 {im.size[0]}x{im.size[1]} → {dst.relative_to(HERE).as_posix()}")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"panel": cmd_panel, "edges": cmd_edges, "clips": cmd_clips, "shots": cmd_shots, "dk": cmd_dk, "build": cmd_build}
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
