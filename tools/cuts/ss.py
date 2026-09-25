# -*- coding: utf-8 -*-
"""13本目（1974年3月3日 トルコ航空981便・DC-10・パリ近郊エルムノンヴィルの森）の
章ファイルが共通で使う小道具。

**12本目（キャッスル・ブラボー）の中身は git の `3832147` にある**（`git show 3832147:tools/cuts/ss.py`）。
11本目（チャレンジャー号）は `61039d2`、10本目（三豊百貨店）は `46f11b3`、9本目（テネリフェ）は `e18b8f1`、
8本目は `4c71bf0`、7本目は `ae30d49`。

🔴 **⑤b-1（2026-09-24）で空にした**＝§0b。12本目の束の定数（頁30枚・TRIM 4点・動く模式図の地図
（ビキニ・船・捜索・艦隊・島の範囲と照合の宣言）と `drift_map()`・`isles_map()`）は外した。
13本目の束は ⑤b-2 で作る。

■ 素材の名前（`ref/ep13/`。選び方と出どころは ⑤b-2 で作る `qa_out/ep13_assets.py`＝12本目の `ep12_assets.py` を写して使う）
  `ep13/<欄の名>.jpg` … 写真
  `ep13/pg<頁>.png`   … 報告書・資料の頁
  `ep13/fb_<カットID>.jpg` … 動く映像を当てたカットの**ひかえの静止画**
  🔴 空にした直後は**未作成**＝`_assets()` が止める（権利を確かめずに焼かない）。

■ 🔴 人が写る点の扱い（この回）
  ⚠️ ⑤b-2 で13本目の決めを書く。台本 §1-2 の実名の線＝ドアを閉めた地上係員と同乗の整備士は**役割だけ**
     （p146・p147・p149 の紙面は出さない）。→ [[feedback-jiko-photo-people-policy]]

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep13"
EP = "ep13/"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対。片側だけにすると粗が反対側へ移る（[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
# ✅ 2026-09-24（13本目 ⑤b-2）に**13本目の束で取り直した**（→ [[feedback-per-episode-constants-go-stale]]）。
#    `python qa_out/ep13_assets.py panel` の22点の並びで、いちばん大きな切れ目は AR 0.992（finnair_dc10）→
#    1.263（dc10_cabin・dc10_flight_1971）の 27ポイント＝その中点 1.1275 を丸めて 1.13。
#    （12本目は 1.049→1.200 の中点 1.12。値が近いのは偶然）
#    ⚠️ BY-SA の点は縦横比にかかわらず額装だけ（下の `FRAME_ONLY`）。
PANEL_AR = 1.13                      # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.82。これ超＝横長すぎ

# 報告書の頁から切る図の矩形（⑤b-2 で作る `ref/ep13/pages.json`）。
_PAGES_FILE = REF / "pages.json"
PAGES: dict[str, dict] = (json.loads(_PAGES_FILE.read_text(encoding="utf-8"))
                          if _PAGES_FILE.exists() else {})
BANDS = {k: v for k, v in PAGES.items() if v.get("fig_box")}

# 画素で測った切り出し。⚠️ **原寸を見てから足す**（推定で置かない）。
#   12本目の4点（fo_tray・fo_tank・rongelap_booties・jp_fish_sign）は git の `3832147`。
TRIM: dict[str, tuple] = {
    # 仏 p15（c110）：航空写真＋機体が入ってきた向きの矢印だけ（頁の見出し・頁番号「14」・説明文を落とす）。
    #   ⑤b-2（09-24）に画素で測った：写真＝暗い画素が50%を超える行 y962〜1904・列 x280〜1434（1726x2352）／
    #   矢印の上端 y368／説明文は y1948 から。＝ x 270〜1444・y 350〜1920 で切る。
    #   ⚠️ 引用（仏の公文書）＝**切るのは写真の部分を取り出すまで**。色は変えない（c110 は color=1.0）
    "ep13/pg15.png": (0.1564, 0.1488, 0.8366, 0.8163),
    # ⑤b-3（09-25）：第3〜5章の頁。**画素で測った**（`blocks`＝字でも絵でも何かある行の帯と左右の端）。
    #   写真の頁は写真だけ（頁番号・BEA の印・仏語の説明文を落とす）。⚠️ p95 は写真と説明文のあいだに白い行が無い
    #   ＝説明文ごと。p88（図7）は題「FERMETURE FORCÉE」から図の下まで（「FIG. 7」と右端の汚れは落とす＝副題が「図7」を名乗る）
    "ep13/pg88.png": (0.03, 0.050, 0.87, 0.945),
    "ep13/pg90.png": (0.11, 0.268, 0.91, 0.675),      # 写真 y0.276〜0.663・説明文 0.687〜
    "ep13/pg91.png": (0.33, 0.030, 0.96, 0.828),      # 写真は頁の右（x0.343〜0.947）・頁番号 y0.021〜0.025
    "ep13/pg92.png": (0.21, 0.146, 0.87, 0.662),      # 写真 y0.152〜0.633・説明文 0.690〜
    "ep13/pg94.png": (0.195, 0.090, 0.84, 0.705),     # 写真 y0.099〜0.674・説明文 0.734〜
    "ep13/pg95.png": (0.17, 0.106, 0.84, 0.745),      # 写真＋説明文（y0.114〜0.734）
    #   上院の頁（100dpi・行の箱が上下に重なる）＝切り口は「その近くでインクが最も少ない行」（09-25 に測った）
    "ep13/pg2017.png": (0.08, 0.0819, 0.92, 0.2369),  # c422：NTSB の報告書の表題〜「NEAR WINDSOR … JUNE 12, 1972」
    "ep13/pg2030.png": (0.08, 0.7745, 0.93, 0.858),   # c504：「Prior to Mr. Shaffer's call … Western Region … was preparing」の段
    #   ⚠️ 下の辺は本文の最後の行（0.835〜0.852）の直後。最初は 0.9217（インク0の行）で切り、
    #      頁の下の余白まで入れて check_blank が「端の47%が無地」で止めた（09-25）
    "ep13/pg2033.png": (0.08, 0.0719, 0.92, 0.4726),  # c515：電報の頭（For Official Use Only・6月16日）と宛先4社
    "ep13/pg2046.png": (0.08, 0.0768, 0.94, 0.3894),  # c520：勧告の送り（7月6日）〜「SAFETY RECOMMENDATIONS A-72-97 AND 98」
    "ep13/pg2055.png": (0.06, 0.6331, 0.87, 0.7740),  # c522：「honestly and in good faith」〜「the only proper way」
}


def page(pr):
    """台本の頁番号 → 頁の画像のパス。

    🔴 章ファイルは**台本の頁番号だけ**を書く（`ss.page(N)`）。台本 §7 と1対1で照合できる。
    ⚠️ `PAGES` に無い頁を呼んだら止まる（黙って別の頁を出さない）。
    """
    key = f"pg{pr}"
    if key not in PAGES:
        raise KeyError(f"頁 p{pr} は焼いていない（`qa_out/ep13_assets.py` の PAGES_PICK に足して pages）")
    return f"{EP}{key}.png"


def P(name):
    """欄の名前 → `ref/` から見た写真のパス。"""
    return f"{EP}{name}.jpg"


def fb(cid):
    """動く映像を当てたカットの**ひかえの静止画**（`footage.USE` が取れなかったとき）。

    ⚠️ 取れなかったことは**黙って静止画に落ちる**＝⑥で `✓ 切り出し完了 N/N` を数える
    → [[feedback-fetch-failure-falls-back-to-a-still]]
    """
    return f"{EP}fb_{cid}.jpg"


# ══════════════════════════════════════════════════════════
#  🔴🔴 継承（ShareAlike）つきの点＝**額装だけ**（13本目・10本目の決めと同じ）
# ══════════════════════════════════════════════════════════
#   13本目の②は継承つきを外していない（事故機 TC-JAV の4点は全部 CC BY-SA）＝台帳 §10-2「額装で進める」。
#   ⚠️ 11・12本目の「継承つきは1点も入れない」網のままだと、TC-JAV を当てた時点で読み込みが止まる
#      ＝⑤b-2（09-24）で**額装の網へ戻した**（10本目 `edaf66c` の `FRAME_ONLY`／`check_frame_only`）。
#   🔴 10本目との違い：**色を変えない（`color=1.0` 必須）とカメラ（`cam=`）も止める**。
#      10本目は額装でもデュオトーンをかけていた（`build_jiko.tone()`＝色の置き換え＝改変）。
#      記憶 [[reference-cc-by-sa-unmodified-in-video]]「無加工・丸ごと・色を変えない・上に重ねない」に合わせた。
#   🔴 **1点1カット**（切れない＝寄りを変えて同じ点を2回使う逃げ道が無い）。
#   額装専用かは `assets.json` の権利から**起動時に読む**（表を手で写さない）。
#   ⚠️ `assets.json` が読めなければ**止める**（0点にして素通りさせない）→ [[feedback-parsers-fail-closed]]
@lru_cache(maxsize=None)
def _assets():
    p = REF / "assets.json"
    if not p.exists():
        raise RuntimeError(
            "ref/ep13/assets.json が無い（⑤b-2 で `python qa_out/ep13_assets.py build`）。"
            "権利を確かめずに焼かない → feedback-parsers-fail-closed")
    return json.loads(p.read_text(encoding="utf-8"))


def _is_sa(lic):
    return "SA" in str(lic or "").upper().replace("-", " ").split()


def frame_only():
    """継承つき（BY-SA）の点 {`ep13/<名>.jpg`: 権利}。1点も読めなければ止める（13本目は TC-JAV 4点ほかがある）。"""
    out = {P(n): r["lic"] for n, r in _assets().items() if _is_sa(r.get("lic"))}
    if not out:
        raise RuntimeError("assets.json から継承つきの点が1つも読めない（13本目は TC-JAV の4点がある＝fail closed）")
    return out


# 額装の約束を破る書き方（10本目の一覧＋`cam`）。🔴 `zoom` は 1.0 ちょうどなら可・`panel=True` と `color=1.0` は必須
_BREAKS_FRAME = ("trim", "veil", "vignette", "focus", "xbias", "bias", "ann", "mark", "blur", "cam", "intro")


def check_frame_only(spec):
    """継承つきの点を、切る・色を変える・重ねる型に渡しているカット／2回使っているカットを挙げる（空なら合格）。

    ⚠️ `intro=dict(photo=…)`（冒頭の秒だけ写真を全画面）も**全画面＝切る**ので、継承つきの点を渡したら止める。
    """
    fo = frame_only()
    bad, seen = [], {}
    for cid, s in sorted(spec.items()):
        ph = s.get("photo")
        intro_ph = (s.get("intro") or {}).get("photo")
        if intro_ph in fo:
            bad.append(f"{cid}＝intro の {intro_ph}（{fo[intro_ph]}）: 冒頭の全画面は切る＝継承つきは使えない")
        lic = fo.get(ph)
        if lic is None:
            continue
        seen.setdefault(ph, []).append(cid)
        why = [k for k in _BREAKS_FRAME if s.get(k) is not None]
        if not s.get("panel"):
            why.append("panel=True が無い（全画面＝上下左右が切れる）")
        if float(s.get("zoom") or 1.0) != 1.0:
            why.append(f"zoom={s.get('zoom')}（1.0 以外は切る）")
        if float(s.get("color") or 0.0) < 1.0:
            why.append(f"color={s.get('color')}（1.0 未満はデュオトーンで色を置き換える＝改変）")
        if why:
            bad.append(f"{cid}＝{ph}（{lic}）: " + "・".join(why))
    for ph, cids in sorted(seen.items()):
        if len(cids) > 1:
            bad.append(f"{ph}（{fo[ph]}）を {len(cids)}カットで使っている（{'・'.join(cids)}）＝1点1カット")
    return bad


# ══════════════════════════════════════════════════════════
#  🔴🔴 使わない写真（シートで見て落とした。**使うと `cuts` の読み込みで止まる**）
# ══════════════════════════════════════════════════════════
#   `cuts/__init__.py` が SPEC を組んだあとに照合し、当たれば RuntimeError にする。
#   ⚠️ ここに無い点は「まだ見ていない」だけで、「危険が無い」ではありません。
NG_PHOTOS: dict[str, str] = {}

# 🔴 元画像そのものを直してから焼く点（私人の顔・名前）。
#    ⚠️ **`blur=` は書けるように見えて誰も読まない**（10本目で私人の顔が素のまま焼けた）。
#       隠すなら元画像を直し、`ref/ep13/masked.json` に md5 を記録する。
#    → [[feedback-settings-may-not-reach-the-picture]]／[[feedback-jiko-photo-people-policy]]
NEEDS_MASK: dict[str, str] = {}


@lru_cache(maxsize=None)
def size_of(name):
    from PIL import Image
    with Image.open(HERE / "ref" / name) as im:
        return im.size


@lru_cache(maxsize=None)
def trimmed_size(name):
    """切り出しを当てたあとの寸法（画素）。切っていなければ原寸。

    ⚠️ **`scene_jiko` を import しない。** `scene_jiko` は起動時に `cuts` を読むので、
       ここから import すると循環参照になり、章ファイルが**丸ごと黙って読めなくなる**
       （2026-09-08 に実際に起きた）→ [[feedback-gates-blind-to-the-new-material]]
    """
    sw, sh = size_of(name)
    t = TRIM.get(name)
    if t:
        x0, y0, x1, y1 = t
        return max(1, int(sw * (x1 - x0))), max(1, int(sh * (y1 - y0)))
    b = BANDS.get(name.split("/", 1)[-1].rsplit(".", 1)[0])
    if not b or not b.get("fig_box"):
        return sw, sh
    x0, y0, x1, y1 = b["fig_box"]
    return max(1, int(sw * (x1 - x0))), max(1, int(sh * (y1 - y0)))


def aspect(name):
    """切ったあとの縦横比（横÷縦）。"""
    w, h = trimmed_size(name)
    return w / h


def crop_loss(name):
    """全画面にしたとき、絵の**何割が枠の外へ出るか**（0〜1）。額装なら 0。"""
    a = aspect(name)
    return 1 - (a / SCREEN_AR if a < SCREEN_AR else SCREEN_AR / a)


# 画素が足りない点も額装に回す（伸ばせないものを伸ばさない）。
# ⚠️ 上限と下限は対（[[feedback-kinsoku-needs-both-ends]]）＝縦横比と画素の両方で見る。
MIN_FULL_W = 1280        # 全画面にしてよい最小の幅（②の網の敷居と同じ値）


def kind(name):
    """`dict(panel=True)` か `dict()` を返す。**縦横比と画素で決める。目で決めない。**"""
    if PANEL_AR is None:
        raise RuntimeError("cuts/ss.py の PANEL_AR が未測（13本目の束で `qa_out/ep13_assets.py panel` から決める）")
    a = aspect(name)
    w, _ = trimmed_size(name)
    return (dict(panel=True)
            if (a < PANEL_AR or a > WIDE_AR or w < MIN_FULL_W) else dict())


def focus(name, fx, fy, zoom=1.0, box=(W, H)):
    """画像の点 (fx, fy)（0〜1・**切ったあとの絵の中での位置**）を画面中央に置く寄せ。

    `fit()`：z = max(w/sw, h/sh)*zoom ／ 切り出し幅 cw = w/z ／ 左端 l = (sw-cw)*xbias。
    中央に置く → l = fx*sw - cw/2 → xbias = (fx*sw - cw/2) / (sw - cw)。0〜1 に丸める。
    """
    sw, sh = trimmed_size(name)
    w, h = box
    z = max(w / sw, h / sh) * zoom
    cw, ch = min(sw, w / z), min(sh, h / z)
    xb = 0.5 if sw - cw < 1 else (fx * sw - cw / 2) / (sw - cw)
    yb = 0.5 if sh - ch < 1 else (fy * sh - ch / 2) / (sh - ch)
    return dict(xbias=round(min(1.0, max(0.0, xb)), 3),
                bias=round(min(1.0, max(0.0, yb)), 3), zoom=zoom)


# ══════════════════════════════════════════════════════════
#  動く映像（13本目は ⑤b-2 で決める。12本目は2本＝DOE 1280x720 全画面・4K 下を切って 3840x1688）
# ══════════════════════════════════════════════════════════
@lru_cache(maxsize=None)
def _clips():
    p = REF / "clips.json"
    if not p.exists():
        raise RuntimeError("ref/ep13/clips.json が無い（動く映像を使うなら ⑤b-2 で作る）")
    return json.loads(p.read_text(encoding="utf-8"))


def vid(cid, **kw):
    """動く映像のカット（ひかえの静止画つき）を1行で書く。秒は `footage.USE` が持つ。"""
    return dict(photo=fb(cid), **kw)


# ══════════════════════════════════════════════════════════
#  動く模式図（drift）の地図
# ══════════════════════════════════════════════════════════
#   🔴 12本目のもの（ビキニ・船・捜索・艦隊・島の表示範囲と照合の宣言 `*_REL`、`drift_map()`・`isles_map()`）は
#      ⑤b-1（2026-09-24）で外した＝git の `3832147`。
#   13本目（⑤b-2・2026-09-24）＝**地図2枚**（⑤b-1 の相談で決めた3か所）：
#     PARIS … 冒頭 c101（パリ→北東37キロの森）→ 第7章で**同じ地図が戻り**、オルリー→サン・パテュス→森の経路
#     AA96  … 第4章（デトロイトの空港→ウィンザーの近く→デトロイトへ戻る）
#   地点＝`titan_fig.GEO`（Wikidata）・宣言＝`*_REL`（報告書の値）・門番 `check_drift` が照合する（§5b-35・38・45）。
#   ⚠️ 枠は 1696×582px（横長）。パリ周辺は南北に長い（オルリー〜森 46キロ）ので縮尺は南北で決まり、
#      左右は空く。`view` の経度の幅は**枠の縦横比に合わせた**（経緯線が枠いっぱいに出る）。
#   ⚠️ 報告書の方角は**8方位の言い方**（仏 p12「nord-est」＝測ると32.8度／NTSB「southwest」＝測ると242度）
#      ＝`sector=8` で照合（`check_drift` の注）。
MAP_PARIS_VIEW = dict(lon=(1.21, 3.94), lat=(48.62, 49.24))
MAP_PARIS_PLACES = ["paris", dict(k="crash", side="above")]
# 第7章の経路の地図は同じ範囲に2地点を足す（サン・パテュスの札は輪の下＝経路の線は左上から来て右上へ抜ける）
MAP_ROUTE_PLACES = ["paris", "orly", dict(k="crash", side="above"), "stpathus"]
MAP_PARIS_REL = [
    dict(a="crash", lat=49 + 8.5 / 60, lon=2 + 38 / 60, src="仏 p5（墜落地点の座標 49°08'30\"N・02°38'00\"E）"),
    dict(a="paris", b="crash", km=37, dir="北東", sector=8, src="仏 p12「à 37 km dans le nord-est de Paris」"),
]
MAP_ROUTE_REL = MAP_PARIS_REL + [
    dict(a="stpathus", b="crash", km=15, src="仏 p12「environ 15 kilomètres du village de Saint-Pathus」"),
    dict(a="orly", lat=48 + 43 / 60, lon=2 + 23 / 60, src="仏 p37（オルリーの敷地の VOR 48°43'N・02°23'E）"),
]
MAP_PARIS_NOTE = "模式図：地点は緯度経度から（墜落地点は報告書の座標）。距離は報告書の値"
MAP_ROUTE_NOTE = "模式図：経路は報告書の地点を直線で結んだもの（実際の飛び方の線ではない）"

MAP_AA96_VIEW = dict(lon=(-83.84, -82.55), lat=(42.10, 42.43))
# ⑤b-3（09-25）：ウィンザーの札は上（下だと空港→ウィンザーの線が札の左の端から 14px を通る＝計算で確かめた）
MAP_AA96_PLACES = ["dtw", dict(k="windsor", side="above")]
MAP_AA96_REL = [
    dict(a="dtw", lat=42 + 13.1 / 60, lon=-(83 + 20.9 / 60), src="NTSB p3009 §1.10（空港の位置）"),
    dict(a="detroit", b="dtw", km=27.4, dir="南西", sector=8,
         src="NTSB p3009「approximately 17 statute miles southwest of Detroit」"),
]
MAP_AA96_NOTE = "模式図：地点は緯度経度から。ドアが外れた正確な位置は報告書に無い（「ウィンザーの近く」）"


# c201（⑤b-3・09-25）：981便の経路＝イスタンブール→パリ（オルリー）→ロンドン（仏 p9）。**Googleアースの代わり**
#   （取り方・表示の置き方が未定＝1通目「決まらなければ地図か紙面で代える」）。
#   範囲は枠の縦横比（1696×582）に合わせた：緯度 39.6〜53.0（イスタンブールの札が枠の下端 816 の内・
#   ロンドンの札が上端 234 の内）→ 同じ縮尺で経度 56.14度ぶん＝2都市の真ん中 14.42 を中心に。
#   ⚠️ 札の置き場は線から逃がした：ロンドンは上（下だとオルリー→ロンドンの線が名前を貫く）・
#      オルリーは下で左へ 70px（真下だとイスタンブールからの線が「空港」の字の右肩を通る）
#   照合＝オルリーの位置（仏 p37 の VOR）。都市2つの位置は報告書に無い（Wikidata の座標）
MAP_EUROPE_VIEW = dict(lon=(-13.65, 42.49), lat=(39.6, 53.0))
MAP_EUROPE_PLACES = ["istanbul", dict(k="orly", dx=-70), dict(k="london", side="above")]
MAP_EUROPE_REL = [MAP_ROUTE_REL[-1]]
MAP_EUROPE_NOTE = "模式図：都市は緯度経度から（都市の中心）。経路は地点を直線で結んだもの"


def europe_map(steps, src="仏の報告書 PDF 9・37頁"):
    """c201：981便の経路（ヨーロッパの広い範囲）。"""
    return ("drift", dict(view=MAP_EUROPE_VIEW, places=MAP_EUROPE_PLACES, pts={}, rel=list(MAP_EUROPE_REL),
                          steps=steps, note=MAP_EUROPE_NOTE, src=src, scale_km=500, grid=5.0))


def paris_map(steps, places=None, rel=None, note=None, src="仏の報告書 PDF 5・12頁"):
    """パリ周辺の地図（c101 → 第7章で戻る）。宣言は既定に**足す**（墜落地点とパリの照合は必ず残る）。"""
    return ("drift", dict(view=MAP_PARIS_VIEW, places=places or MAP_PARIS_PLACES, pts={},
                          rel=MAP_PARIS_REL + list(rel or []), steps=steps, note=note or MAP_PARIS_NOTE,
                          src=src, scale_km=20, grid=0.2))


def route_map(steps, note=None, src="仏の報告書 PDF 5・12・37頁"):
    """第7章：同じ地図にオルリーとサン・パテュスを足した経路の地図。"""
    return ("drift", dict(view=MAP_PARIS_VIEW, places=MAP_ROUTE_PLACES, pts={}, rel=list(MAP_ROUTE_REL),
                          steps=steps, note=note or MAP_ROUTE_NOTE, src=src, scale_km=20, grid=0.2))


def aa96_map(steps, rel=None, note=None, src="NTSB AAR-73-02 PDF 9頁"):
    """第4章：デトロイトの空港とウィンザー。デトロイトの市街は輪を描かない（ウィンザーと1.9キロ＝輪が重なる）。"""
    return ("drift", dict(view=MAP_AA96_VIEW, places=MAP_AA96_PLACES, pts={},
                          rel=MAP_AA96_REL + list(rel or []), steps=steps, note=note or MAP_AA96_NOTE,
                          src=src, scale_km=10, grid=0.1))
