# -*- coding: utf-8 -*-
"""14本目（2014年4月16日 セウォル号沈没・韓国 チンド沖・304名）の章ファイルが共通で使う小道具。

**13本目（トルコ航空981便）の中身は git の `b54ee4f` にある**（`git show b54ee4f:tools/cuts/ss.py`）。
12本目（キャッスル・ブラボー）は `3832147`、11本目（チャレンジャー号）は `61039d2`、10本目（三豊百貨店）は `46f11b3`、
9本目（テネリフェ）は `e18b8f1`、8本目は `4c71bf0`、7本目は `ae30d49`。

🔴 **⑤b-1（2026-09-28）で空にした**＝§0b。13本目の束の定数（頁の切り方 TRIM 23点・隠す点 names_wall・
動く模式図の地図 PARIS／ROUTE／AA96／EUROPE の範囲と照合の宣言と `paris_map()` ほか4つ）は外した。
14本目の束は ⑤b-2 で作る（`qa_out/ep13_assets.py` を写して `qa_out/ep14_assets.py`）。

■ 素材の名前（`ref/ep14/`。選び方と出どころは台本 `ref/ep14/daihon_v2.md` §7・②の台帳 `ref/ep14/materials.md`）
  `ep14/<欄の名>.jpg` … 写真
  `ep14/pg<頁>.png`   … 報告書・判決・裁決の頁（台本の頁番号＝判決 p1〜81・海審 p1001〜・裁決 p2001〜・特調委 p3001〜）
  `ep14/fb_<カットID>.jpg` … 動く映像を当てたカットの**ひかえの静止画**
  🔴 空にした直後は**未作成**＝`_assets()` が止める（権利を確かめずに焼かない）。
     ⚠️ 写真を1点も当てていないうちは `cuts/__init__.py` が額装の網を呼ばない（照合する点が無い）。1点でも当てたら要る

■ 🔴 人が写る点の扱い（この回）＝ルール §B2-2・台本 §1-3／§7
  ・犠牲者の多くが高校生（私人）＝**顔と名前は出さない**。救助の写真のうち家族の顔が写る点は ✕（②の台帳）
  ・捜索（韓国国防部・BY-SA）11点は**額装・1点1カット**（台本 §1-4）。✕の点（#7・#9・#43・#73）は使わない
  ・`cd01` #46・`cd05` #52 は副題の中身が写っているかを原寸で（台本 §0-9）→ [[feedback-jiko-photo-people-policy]]

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep14"
EP = "ep14/"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対。片側だけにすると粗が反対側へ移る（[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
# ✅ 2026-09-24（13本目 ⑤b-2）に**13本目の束で取り直した**（→ [[feedback-per-episode-constants-go-stale]]）。
#    `python qa_out/ep13_assets.py panel` の22点の並びで、いちばん大きな切れ目は AR 0.992（finnair_dc10）→
#    1.263（dc10_cabin・dc10_flight_1971）の 27ポイント＝その中点 1.1275 を丸めて 1.13。
#    （12本目は 1.049→1.200 の中点 1.12。値が近いのは偶然）
#    ⚠️ BY-SA の点は縦横比にかかわらず額装だけ（下の `FRAME_ONLY`）。
#    ✅ 2026-09-29（14本目 ⑤b-7a）に**14本目の束（22点）で取り直した**。`python qa_out/ep14_assets.py panel` の並びで、
#       16:9 より縦長の側のいちばん大きな切れ目は AR 1.517（search_divers_0504）→ 1.650（search_ship21_0419）の 13ポイント
#       ＝中点 1.58（次は 1.351→1.473 の 12ポイント）。4:3 の3点（学校2・ソウル広場）と K1 は額装、3:2 の BY-SA は額装だけ（権利）。
#       WIDE_AR＝2.00＝site_0418（2.21・PD）は額装（横に 19.5% 切れるのを避ける）。gwanghwamun_2018 は切り出しのあと 1.97＝全画面
PANEL_AR = 1.58                     # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.00。これ超＝横長すぎ

# 報告書の頁から切る図の矩形（⑤b-2 で作る `ref/ep14/pages.json`）。
_PAGES_FILE = REF / "pages.json"
PAGES: dict[str, dict] = (json.loads(_PAGES_FILE.read_text(encoding="utf-8"))
                          if _PAGES_FILE.exists() else {})
BANDS = {k: v for k, v in PAGES.items() if v.get("fig_box")}

# 画素で測った切り出し。⚠️ **原寸を見てから足す**（推定で置かない）。
#   12本目の4点（fo_tray・fo_tank・rongelap_booties・jp_fish_sign）は git の `3832147`。
#   🔴 2026-09-28（14本目 ⑤b-1）：13本目の23点（仏の報告書・上院・SB・AD の頁と、人の顔を外した写真2点）は
#      git の `b54ee4f`（`git show b54ee4f:tools/cuts/ss.py`）。次の回にも効く教訓だけ残す：
#     ・頁の切り口は「その近くでインクが最も少ない行」＝行の途中で切らない。寄り（窓が尺の間に縮む）で端の行が
#       欠けるので、切り口は寄りの掃きが届かない所へ（13本目 c504・c520＝門番 `edges` が拾った）
#     ・写真の頁は写真だけ（頁番号・印・説明文を落とす）。斜めの写真は水平の切り口で分けきれない（13本目 p95）
#     ・人の顔を外す切り出しは 16:9 ちょうどに（13本目 dc10_cabin・klm_cockpit_1972）
#   🔴 2026-09-29（14本目 ⑤b-7a）：**頁の切り出しは `pages.json` の `trim` から読む**（下の update＝手で写さない）。
#      `qa_out/ep14_assets.py pages` が、文字の頁は目印の語の行（`ANCHOR`）から、図の頁は測った行・画像の位置（`FIGVEC`）
#      から決めて書く。ここに手で書くのは写真の切り出しだけ
TRIM: dict[str, tuple] = {
    # 🔴 私人の顔と名前を外す（09-29・原寸で見た）。権利は Attribution／CC BY＝切り出しは可（改変の旨は出典の行に出る）
    #   光化門 2018：下の黄色い板（y 0.776〜0.863）に**見つかっていない5人の顔写真と名前**＝板の上端より上だけ
    "ep14/gwanghwamun_2018.jpg": (0.0, 0.0, 1.0, 0.76),
    #   救命胴衣の列 2017：奥の集会の人の顔（足もとが y 0.51〜0.57）＝胴衣の列だけ（y 0.60 から下・横長＝額装）
    "ep14/lifejackets_2017.jpg": (0.0, 0.60, 1.0, 1.0),
}
TRIM.update({f"{EP}{k}.png": tuple(v["trim"]) for k, v in PAGES.items() if v.get("trim")})


def page(pr):
    """台本の頁番号 → 頁の画像のパス。

    🔴 章ファイルは**台本の頁番号だけ**を書く（`ss.page(N)`）。台本 §7 と1対1で照合できる。
    ⚠️ `PAGES` に無い頁を呼んだら止まる（黙って別の頁を出さない）。
    """
    key = f"pg{pr}"
    if key not in PAGES:
        raise KeyError(f"頁 p{pr} は焼いていない（`qa_out/{EP[:-1]}_assets.py` の PAGES_PICK に足して pages）")
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
            f"ref/{EP}assets.json が無い（⑤b-2 で `python qa_out/{EP[:-1]}_assets.py build`）。"
            "権利を確かめずに焼かない → feedback-parsers-fail-closed")
    return json.loads(p.read_text(encoding="utf-8"))


def _is_sa(lic):
    return "SA" in str(lic or "").upper().replace("-", " ").split()


def frame_only():
    """額装だけの点 {`ep14/<名>.jpg`: 権利}＝継承つき（BY-SA）と**引用**（`assets.json` の `frame`）。
    1点も読めなければ止める（14本目は捜索11点・J1・M1・AN74 の BY-SA と H1 の引用がある）。
    🔴 2026-09-29（14本目 ⑤b-7a）：引用（当日の沈む船 H1＝Commons の表示に根拠が無い）も「改変しない＝色も切り出しもせず
       額装で置く」（ルール §2-5b）＝BY-SA と同じ網に入れた。読む側＝門番 `check_frame_only`・合成 `build_jiko.meta_of`（寄りとディゾルブを止める）"""
    out = {P(n): r["lic"] for n, r in _assets().items() if _is_sa(r.get("lic")) or r.get("frame")}
    if not out:
        raise RuntimeError("assets.json から継承つきの点が1つも読めない（14本目は捜索の11点ほかがある＝fail closed）")
    return out


def uses_photo(spec):
    """SPEC が写真を1点でも当てているか（`photo=` か `intro=dict(photo=…)`）。"""
    return any(s.get("photo") or (s.get("intro") or {}).get("photo") for s in spec.values())


def frame_only_for(spec):
    """🔴 2026-09-28（14本目 ⑤b-1）：**写真を1点も当てていなければ {}（台帳 `assets.json` を読まない）**。
    1点でも当てたら `frame_only()`＝台帳が無ければ止まる（fail closed のまま）。

    回を切り替えた直後は台帳（⑤b-2 で作る）が無い。ここを通さずに `frame_only()` を呼ぶと、
    `import cuts`（`check_frame_only`）と合成（`build_jiko.meta_of`）が落ち、写真を使わない試し焼きも門番も全部止まった
    （14本目 ⑤b-1 の Actions で合成の側が落ちた＝呼び出し元は2か所・ここに1か所でまとめた）。
    """
    return frame_only() if uses_photo(spec) else {}


# 額装の約束を破る書き方（10本目の一覧＋`cam`）。🔴 `zoom` は 1.0 ちょうどなら可・`panel=True` と `color=1.0` は必須
_BREAKS_FRAME = ("trim", "veil", "vignette", "focus", "xbias", "bias", "ann", "mark", "blur", "cam", "intro")


def check_frame_only(spec):
    """継承つきの点を、切る・色を変える・重ねる型に渡しているカット／2回使っているカットを挙げる（空なら合格）。

    ⚠️ `intro=dict(photo=…)`（冒頭の秒だけ写真を全画面）も**全画面＝切る**ので、継承つきの点を渡したら止める。
    ⚠️ 写真を1点も当てていなければ照合する点が無い＝台帳を読まずに合格（`frame_only_for`）。
    """
    fo = frame_only_for(spec)
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
#       隠すなら元画像を直し、`ref/ep14/masked.json` に md5 を記録する。
#    → [[feedback-settings-may-not-reach-the-picture]]／[[feedback-jiko-photo-people-policy]]
#    🔴 2026-09-28（14本目 ⑤b-1）：13本目の1点（慰霊の名前の壁 names_wall・c814）を外した＝git の `b54ee4f`。
#       ⚠️ CC BY-SA の点は隠すこと自体が翻案＝使わない（ルール §B2-2）。隠せるのは改変を許す権利の点だけ
NEEDS_MASK: dict[str, str] = {
}

# 🔴 2026-09-29（14本目 ⑤b-7a）：**切り出し（`TRIM`）で外した私人の範囲**（元画像の割合 x0,y0,x1,y1・何か）。
#    門番 photomask が「その写真を使う全カットの窓（`trim` か `TRIM`・冒頭の写真は切らない＝全体）がこの範囲に
#    1画素も入らない」を見る（NEEDS_MASK は元画像を直す点だけ＝切り出しで外した点を見ていなかった）。範囲は原寸で見て測った
PRIVATE_OUT: dict[str, list] = {
    # 光化門 2018：下の黄色い板＝見つかっていない5人の顔写真と名前（x 0.159〜0.293・y 0.776〜0.863）
    "ep14/gwanghwamun_2018.jpg": [(0.15, 0.77, 0.30, 0.87, "見つかっていない5人の顔写真と名前の板")],
    # 救命胴衣の列 2017：奥の集会の人の顔（足もとは y 0.51〜0.57）
    "ep14/lifejackets_2017.jpg": [(0.0, 0.0, 1.0, 0.575, "集会の人の顔（足もとまで）")],
}


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
        raise RuntimeError(f"cuts/ss.py の PANEL_AR が未測（この回の束で `qa_out/{EP[:-1]}_assets.py panel` から決める）")
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
#  動く映像（14本目＝米海軍の捜索の映像 PD・⑤b で決める。13本目は0本・12本目は2本）
# ══════════════════════════════════════════════════════════
@lru_cache(maxsize=None)
def _clips():
    p = REF / "clips.json"
    if not p.exists():
        raise RuntimeError(f"ref/{EP}clips.json が無い（動く映像を使うなら ⑤b で作る）")
    return json.loads(p.read_text(encoding="utf-8"))


def vid(cid, **kw):
    """動く映像のカット（ひかえの静止画つき）を1行で書く。秒は `footage.USE` が持つ。"""
    return dict(photo=fb(cid), **kw)


# ══════════════════════════════════════════════════════════
#  動く模式図（drift）の地図
# ══════════════════════════════════════════════════════════
#   🔴 12本目のもの（ビキニ・船・捜索・艦隊・島の表示範囲と照合の宣言 `*_REL`、`drift_map()`・`isles_map()`）は
#      ⑤b-1（2026-09-24）で外した＝git の `3832147`。
#   🔴 13本目のもの（PARIS・ROUTE・AA96・EUROPE の範囲・札の置き場・照合の宣言と `paris_map()`・`route_map()`・
#      `aa96_map()`・`europe_map()`）は ⑤b-1（2026-09-28）で外した＝git の `b54ee4f`。
#   14本目は ⑤b-4 で作る（承認ずみの地図6＝航路 c111・変針と航跡 c604〜c611・集まる船 c812＋追補の地図6）。
#   次の回にも効く教訓（13本目）：
#     ・札を線から逃がす（線が名札を貫く＝§5b-39）。札どうしがくっつくと1語に読める＝dx で離す
#     ・`view` の経度の幅は枠（1696×582）の縦横比に合わせる（経緯線が枠いっぱいに出る）
#     ・報告書の方角が8方位の言い方なら `sector=8` で照合（`check_drift`）
#     ・都市の位置が報告書に無いときは Wikidata の座標＝照合の宣言に入れない（地点は `titan_fig.GEO`）


# ══════════════════════════════════════════════════════════
#  案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 14本目 ⑤b-2（2026-09-28）新設
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：次の回は下の4つを**その回の資料と時刻**に替える。
#   REC_PAGES … 部品の出典（`rec=`）を当てる原文（`=== p<N> ===` で頁を割った1ファイル＝④ の make_pages.py の出力）
#   REC_DOCS  … 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面に出す名前・頁の出し方（print＝印字の頁／pdf＝PDF の頁）
#   ILLU_SPLIT_TIMES … 資料で割れる時刻（台本 §1-5）＝**画面に時計・時刻の札として出さない**（ルール §5b-74①）
#   ILLU_CROWD_UNTIL … 乗客の群れを描いてよい場面の時刻の上限（この時刻**より前**だけ）。14本目＝3階の手すりが水に
#                      つかった 9時47分（判決 p18「09:47경 세월호의 3층 난간이」）＝水が入った後の船内に乗客を描かない（§5b-74②）
REC_PAGES = REF / "src" / "sewol_pages.txt"
REC_DOCS = {
    "判決": dict(range=(1, 81), name="大法院 判決（2015年）", page="print", base=0),
    "海審": dict(range=(1001, 1138), name="海洋安全審判院 特別調査報告（2014年）", page="pdf", base=1000),
    "裁決": dict(range=(2001, 2174), name="中央海洋安全審判院 裁決（2026年）", page="pdf", base=2000),
    "特調委": dict(range=(3001, 3330), name="社会的惨事特別調査委員会 報告（2022年）", page="pdf", base=3000),
    "特調委小": dict(range=(4001, 4486), name="社会的惨事特別調査委員会 小委員会報告（2022年）", page="pdf", base=4000),
    "艇長の判決": dict(range=(5001, 5002), name="123艇の艇長の判決", page=None, base=0),
    "幹部の判決": dict(range=(5003, 5004), name="海洋警察の幹部の判決", page=None, base=0),
    "会社の判決": dict(range=(5005, 5005), name="清海鎮海運の判決", page=None, base=0),
    "船員の1審": dict(range=(5006, 5006), name="船員の1審判決（光州地裁）", page=None, base=0),
    "船員の2審": dict(range=(5007, 5007), name="船員の2審判決（光州高裁）", page=None, base=0),
}
ILLU_SPLIT_TIMES = ("8:48", "8:49", "8:52", "8:54", "8:56", "8:58", "9:30", "9:32", "9:33", "9:35", "9:46", "9:48")
ILLU_CROWD_UNTIL = "9:47"

# 🔴 §0b：軸の型（`tools/axis.py`・14本目 ⑤b-5）の「割れる時刻の印」に添える出典の名（`rec=` の資料名 → 画面の名）。
#   語りが資料を呼ぶ名に合わせる（海審の特別調査報告＝語りは「報告書」）。ILLU_SPLIT_TIMES の時刻は、軸の型では
#   **出典の名つきでだけ**出してよい（門番 check_axis ②＝点に by=True か split）
AXIS_DOCS = {"判決": "判決", "海審": "報告書", "艇長の判決": "艇長の判決", "特調委": "特別調査委",
             "幹部の判決": "幹部の判決", "裁決": "裁決", "船員の2審": "2審の判決"}

# 軸（カットをまたいで同じ軸を使う＝前のカットの点を past で沈めて続ける）
AX_SHIP = dict(view="date", span=("1993", "2015"), ticks=("1994", "1998", "2002", "2006", "2010", "2014"))
AX_BUILD = dict(view="date", span=("1993-12", "1994-06"),
                ticks=("1994-01", "1994-02", "1994-03", "1994-04", "1994-05", "1994-06"))
AX_KAIZO = dict(view="date", span=("2012-09", "2013-05"),
                ticks=("2012-09", "2012-10", "2012-11", "2012-12", "2013-01", "2013-02", "2013-03", "2013-04", "2013-05"))
AX_CAUSE = dict(view="date", span=("2012-07", "2027"), ticks=("2014", "2016", "2018", "2020", "2022", "2024", "2026"))
AX_NIGHT = dict(view="clock", span=("18:00", "翌10:00"),
                ticks=("18:00", "20:00", "22:00", "翌0:00", "翌2:00", "翌4:00", "翌6:00", "翌8:00", "翌10:00"))
AX_0850 = dict(view="clock", span=("8:48", "9:02"), ticks=("8:50", "8:55", "9:00"))
AX_TALK = dict(view="lanes", span=("9:04", "9:40"), ticks=("9:05", "9:10", "9:15", "9:20", "9:25", "9:30", "9:35", "9:40"),
               lanes=("管制", "近くの船", "セウォル号"))

# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
AXI = {
    "accident": dict(k="pt", at="2014-04-16", t="事故", rec="海審 p1008", c="ALERT"),
    "keel": dict(k="pt", at="1994-01-25", t="工事の始まり", rec="海審 p1013"),
    "launch": dict(k="pt", at="1994-04-01", t="進水", rec="海審 p1013"),
    "japan": dict(k="span", a="1994-04-01", b="2012-10-08", t="日本", rec=["海審 p1013", "海審 p1016"], c="INST"),
    "naminoue": dict(k="span", a="1994-04-01", b="2012-10-08", t="なみのうえ", rec=["海審 p1013", "海審 p1016"], c="INST"),
    "import": dict(k="pt", at="2012-10-08", t="導入", rec="海審 p1016"),
    "kaizo": dict(k="span", a="2012-10-12", b="2013-02-12", t="改造", rec="海審 p1016", c="AMBER"),
    "first": dict(k="pt", at="2013-03-16", t="初めての運航", rec="海審 p1026"),
    "incline": dict(k="pt", at="2013-01-24", t="傾斜試験", rec="海審 p1022"),
    # 原因の年表（機関の名だけ・原因は項目の札で並べるだけ）
    # 2014-12-29 と 2015（年の真ん中）は半年しか離れていない＝札を左右に振る（anchor）
    # 札の日付は年月まで（fmt="ym"＝語りの細かさ。位置は日まで）
    "kmst": dict(k="pt", at="2014-12-29", t="海洋安全審判院", rec="海審 p1001", c="INST", anchor="end", fmt="ym"),
    "court": dict(k="pt", at="2015", t="裁判所", rec="船員の2審 p5007", c="INST", anchor="start"),
    "raise": dict(k="pt", at="2017-03-23", t="引き揚げ", rec="特調委 p3061", c="INST", anchor="end", fmt="ym"),
    "hull18": dict(k="pt", at="2018-08", t="船体調査委員会", rec="特調委 p3073", c="INST", anchor="start"),
    "sccc": dict(k="pt", at="2022-09", t="特別調査委員会", rec="特調委 p3006", c="INST"),
    "kmst26": dict(k="pt", at="2026-01-28", t="中央海洋安全審判院", rec="裁決 p2001", c="INST", fmt="ym"),
    # 出港の夜（予定は曜日の決まった運航＝海審 p1026）
    "dep_plan": dict(k="pt", at="18:30", t="出港の予定", rec="海審 p1026"),
    "arr_plan": dict(k="pt", at="翌9:10", t="着く予定", rec="海審 p1026"),
    "plan": dict(k="span", a="18:30", b="翌9:10", t="予定の航海", rec="海審 p1026"),
    # 交信の帯（段の名だけ・言葉は字幕）
    "t0906": dict(k="link", at="9:06", fr="管制", to="セウォル号", rec="海審 p1059"),
    "t0913": dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13"),
    "t0914": dict(k="link", at="9:14", fr="管制", to="セウォル号", rec="海審 p1059"),
    "t0924": dict(k="link", at="9:24", fr="近くの船", to="セウォル号", rec="判決 p14"),
    "t0937": dict(k="link", at="9:37", fr="セウォル号", to="管制", rec="海審 p1061"),
}


CAUSE_NOTE = "年表：機関の名と、その機関が挙げた原因の項目だけ（原因は今も1つに決まっていない）"


def ax(name, **kw):
    """AXI の部品の写し（同じカットで past と add に同じ物を2回入れても別の部品になる）。"""
    return dict(AXI[name], **kw)


# ══════════════════════════════════════════════════════════
#  14本目 ⑤b-4（2026-09-29）：断面F（`tools/hull.py`）と地図（drift）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の MAP_* ・HULL_NOTE・`sewol_map()` はこの回の地図と資料。
#    画面の出典は `src()`（台本の頁「海審 p1016」→ 画面の頁「…PDF 16頁」＝門番 check_wording の I が通し番号を止める）
def src(recs):
    """出典の行（「出典：」を除く）。recs＝「海審 p1016・p1017」のような台本の頁の書き方（文字列か list）。"""
    import illu
    return illu.rec_line(recs if isinstance(recs, (list, tuple)) else [recs]).replace("出典：", "", 1)


HULL_NOTE = "模式図：形は報告書の要目と構造の文から（部屋の前後の位置・通路の幅は模式）"

# 地図（drift）の点。🔴 地点＝Wikidata（`titan_fig.GEO`）と報告書の値だけ（§5b-35・§5b-38）
MAP_PTS = {
    # 8時50分ごろ（傾いて荷が寄った時点）＝海審 p1065「병풍도 북동쪽 1.3마일(북위34도09분34초, 동경125도57분56초)」
    "acc": dict(lat=34 + 9 / 60 + 34 / 3600, lon=125 + 57 / 60 + 56 / 3600),
    # メンゴル水道＝海審 p1046「맹골수도(진도군 거차도와 맹골도 사이)」＝2つの島の真ん中
    "ch": dict(mid=["maenggoldo", "seogeochado"]),
    # 水道の手前（針路 約160度で近づいた＝p1046「대략 160도 정도이었던 세월호 침로를 서서히 변침」）。🔴 位置は模式（7キロは描く都合）
    "appr": dict(of="ch", km=7.0, deg=340),
    # 8時46分＝ピョンプンドを右 約0.9マイルに見て通った（p1046「병풍도를 우현 약 0.9마일로 통과」・針路 約136度）
    #   ＝島は船の右の真横（136＋90＝226度）＝船は島から46度の向き 0.9マイル（1.667キロ）。「真横」は読み方（記録は距離と右）
    "t0846": dict(of="byeongpungdo", km=1.667, deg=46),
}
MAP_REL_ACC = dict(a="acc", lat=MAP_PTS["acc"]["lat"], lon=MAP_PTS["acc"]["lon"], tol_km=0.3, src="海審 p1065")
# ピョンプンドの点（Wikidata の島の中心）から事故の地点まで＝報告書「북동쪽 1.3마일」（8方位の言い方＝sector=8）
MAP_REL_NE = dict(a="byeongpungdo", b="acc", km=2.41, dir="北東", sector=8, src="海審 p1065")
MAP_REL_0846 = dict(a="t0846", b="byeongpungdo", km=1.667, src="海審 p1046")
# 通った島の順（海審 p1045：옹도 00:35・어청도 02:20・대흑산도 07:00 → p1046 맹골수도 08:27 → 병풍도 08:46）。
#   p1045 の「신안군 매물도」は Wikidata に同じ島が見つからない＝点にしない（直線で結ぶ＝模式）。予定の残り＝p1034 の報告の地点
ROUTE = ["incheon", "palmido", "ongdo", "eocheongdo", "heuksando", "ch", "t0846", "acc"]
ROUTE_PLAN = ["acc", "chujado", "jeju"]
MAP_VIEWS = {
    "wide": dict(view=dict(lon=(125.2, 126.9), lat=(33.40, 37.66)), scale_km=100, grid=1.0,
                 # インチョン港の札は輪の下・右へ（上に置くと枠の上の端に出る・船の札「セウォル号」と重なった＝⑤b-4 の layout）
                 places=[dict(k="incheon", dx=130), dict(k="jeju", dx=60), dict(k="jindo", side="above", dx=40)],
                 rel=[MAP_REL_ACC], note="模式図：航路は報告書の通った島を直線で結んだもの（実際の線ではない）。港と島は中心の1点"),
    "local": dict(view=dict(lon=(125.62, 126.28), lat=(34.10, 34.30)), scale_km=5, grid=0.1,
                  places=["maenggoldo", dict(k="seogeochado", side="above"), "byeongpungdo"],
                  rel=[MAP_REL_ACC, MAP_REL_NE], note="模式図：島は中心の1点（形は描いていない）。船の位置は報告書の値から"),
    "near": dict(view=dict(lon=(125.86, 126.06), lat=(34.125, 34.195)), scale_km=1, grid=0.05,
                 places=["byeongpungdo"], rel=[MAP_REL_ACC, MAP_REL_NE, MAP_REL_0846],
                 note="模式図：島は中心の1点（形は描いていない）。船の位置は報告書の値から"),
}
# 札を置くための点（地名ではない・輪を描かない）
MAP_LAB = {"wide": dict(_l1=dict(lat=36.9, lon=125.35), _r1=dict(lat=35.2, lon=126.75)),
           "local": dict(_l1=dict(lat=34.285, lon=125.66), _r1=dict(lat=34.285, lon=126.12)),
           "near": dict(_l1=dict(lat=34.19, lon=125.875), _r1=dict(lat=34.137, lon=126.035))}


def sewol_map(which, steps, rel=None, note=None, recs=None, dial=None, places=None):
    """14本目の地図（drift）。which＝wide（インチョン〜チェジュ）／local（メンゴル水道のまわり）／near（ピョンプンドの寄り）。
    places＝その見え方の地点に足す地点（⑤b-7a の cc09＝モッポ）。"""
    m = MAP_VIEWS[which]
    pts = dict(MAP_PTS, **MAP_LAB[which])
    return ("drift", dict(view=m["view"], places=list(m["places"]) + list(places or []), pts=pts,
                          rel=list(m["rel"]) + list(rel or []),
                          steps=steps, note=note or m["note"], src=src(recs or ["海審 p1065"]), scale_km=m["scale_km"],
                          grid=m["grid"], dial=dial))


# ══════════════════════════════════════════════════════════
#  14本目 ⑤b-6（2026-09-29）：量の型（`tools/qty.py`・門番 check_qty）と箱の型（`tools/boxes.py`・門番 check_boxes）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB・PEOPLE_*・CT・CTP・RUD・FORM_PRE・CAUSE はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_*／check_boxes.REC_*＝§5b-88）＝回を替えたら両方を替える。
#    頁は ref/ep14/src/sewol_pages.txt で当てた（2026-09-29 ⑤b-6）
# 棒の群（尺は 0 から・項目名に単位）。数字は棒に書かない（§5b-9＝数は字幕）
QG = {
    "cargo": dict(id="cargo", t="積める貨物の上限（トン）", ticks=(0, 500, 1000, 1500, 2000, 2500)),
    "pax": dict(id="pax", t="乗せられる人の数（人）", ticks=(0, 200, 400, 600, 800, 1000)),
    "load": dict(id="load", t="貨物の重さ（トン）", ticks=(0, 500, 1000, 1500, 2000, 2500), rows=("上限", "積み荷")),
    "pair": dict(id="pair", t="重さ（トン）", ticks=(0, 500, 1000, 1500, 2000, 2500)),
}
QB = {
    # 表1（海審 p1018）：화물적재최대량 2,437톤→987톤・최대승선인원 840명→956명。
    #   色＝改造の前 LINE・改造の後 AMBER（下見で TICK と LINE がほぼ同じ色に見えた）。987 は第5章まで同じ AMBER で戻す
    "cargo_before": dict(k="bar", g="cargo", t="改造の前", v=2437, rec="海審 p1018"),
    "cargo_after": dict(k="bar", g="cargo", t="改造の後", v=987, rec="海審 p1018", c="AMBER"),
    "pax_before": dict(k="bar", g="pax", t="改造の前", v=840, rec="海審 p1018"),
    "pax_after": dict(k="bar", g="pax", t="改造の後", v=956, rec="海審 p1018", c="AMBER"),
    # p1041 3.1.4.1：최대 약987톤 적재 승인・사고당시 약2,142.7톤（語りは「約2143トン」）＝積みすぎは会社の選んだ危ないほう＝赤
    "load_limit": dict(k="bar", g="load", t="上限", v=987, rec="海審 p1041", c="AMBER"),
    "load_real": dict(k="bar", g="load", t="積み荷", v=2142.7, rec="海審 p1041", c="ALERT"),
    # p1043 3.1.5.1：화물 약987톤 실을 경우 선박평형수는 약1,703톤（出港のときの 761.2 は決め所 c508）
    "pair_cargo": dict(k="bar", g="pair", t="貨物", v=987, rec="海審 p1043", c="AMBER"),
    "pair_water": dict(k="bar", g="pair", t="バラスト", v=1703, rec="海審 p1043"),
}


def qb(name, **kw):
    return dict(QB[name], **kw)


# 人の形（1つ＝1人・c204〜c206 だけ＝ルール §C-1 #59）。並び＝この順に左上から（3カットとも同じ並び）
#   海審 p1038：총승선인원 476명・여객 443명（학생 325・교사 14・일반승객 104）・선원및승무원 33명
#   （선박운항 선원 15・지원부서 선원 8〈조리장・사무장〉・아르바이트 학생・가수・불꽃놀이 직원 등 기타 승무원 10＝p1039 に続く）
PEOPLE_ORDER = (("生徒", 325), ("先生", 14), ("一般の乗客", 104), ("船員", 15), ("調理・事務の係", 8),
                ("ほか（アルバイトなど）", 10))
PEOPLE_SETS = {"乗客": ("生徒", "先生", "一般の乗客"), "船で働く人": ("船員", "調理・事務の係", "ほか（アルバイトなど）")}
PEOPLE_REC = {"乗客": "海審 p1038", "生徒": "海審 p1038", "先生": "海審 p1038", "一般の乗客": "海審 p1038",
              "船で働く人": "海審 p1038", "船員": "海審 p1038", "調理・事務の係": "海審 p1038",
              "ほか（アルバイトなど）": "海審 p1038・p1039"}
PEOPLE_CUTS = ("c204", "c205", "c206")     # 🔴 門番 check_qty がこの外の人の形を止める（亡くなった方の数に使わない）


def pp(who, c, parent=None):
    """人の形の部品（who の形を c の色に灯して凡例に1行）。"""
    return dict(k="lit", who=who, c=c, rec=PEOPLE_REC[who], **({"parent": parent} if parent else {}))


# 裁判の流れ図（第11章）。🔴 役職名だけ（判決 p2〜3 の書き方）・名前を出さない・人の形を使わない・赤を使わない
#   列＝役職（who）・罪名（crime）・1審・2審・大法院。結果は決めた裁判所の列に（刑は大法院の列＝上告を退けて確定）
CT = dict(
    cols=dict(who=(84, 304), crime=(364, 604), c1=(680, 960), c2=(1040, 1320), c3=(1400, 1760)),
    heads=[dict(id="c1", t="1審", col="c1", rec="船員の1審 p5006"), dict(id="c2", t="2審", col="c2", rec="船員の2審 p5007"),
           dict(id="c3", t="大法院", col="c3", rec="判決 p1")],
    head_y=(232, 292), chain=True,
    # 裁判官13人＝대법원장 1＋대법관 12（判決 p79〜81 の署名）
    seats=dict(col="c3", n=13, y=306, t="裁判官", rec=["判決 p79", "判決 p80", "判決 p81"]),
    bounds=(642, 1000, 1360), guide_y=(346, 850),
    rows={"船長": 392, "1等航海士": 444, "2等航海士": 496, "機関長": 548, "3等航海士": 600, "操舵手（当直）": 652,
          "会社の代表": 744, "123艇の艇長": 796},
)


def _cr(i, t, row, rec="判決 p2"):
    return dict(k="role", id=i, t=t, row=row, rec=rec)


CTP = {
    # 役職（判決 p2〜3：피고인1 선장・2 1등항해사・3 2등항해사・4 3등항해사・5 조타수・9 기관장）
    "r_captain": _cr("r_captain", "船長", "船長"),
    "r_mate1": _cr("r_mate1", "1等航海士", "1等航海士"),
    "r_mate2": _cr("r_mate2", "2等航海士", "2等航海士"),
    "r_chief": _cr("r_chief", "機関長", "機関長"),
    "r_mate3": _cr("r_mate3", "3等航海士", "3等航海士"),
    # 当直の操舵手＝피고인5（判決 p33「피고인5가 피고인4의 지시에 따라 … 변침」）
    "r_helm": _cr("r_helm", "操舵手（当直）", "操舵手（当直）", ["判決 p2", "判決 p33"]),
    # 会社の代表の刑は p5005 に無い＝民事の判決 N（2015가합579799）の表（台本 §G6-10）
    "r_ceo": _cr("r_ceo", "会社の代表", "会社の代表", ["会社の判決 p5005", "民事の判決 N"]),
    "r_123": _cr("r_123", "123艇の艇長", "123艇の艇長", ["艇長の判決 p5001", "艇長の判決 p5002"]),
    # 罪名（箱の中の文字）
    "x_cap": dict(k="crime", id="x_cap", t="殺人・殺人未遂", row="船長", rec=["判決 p18", "判決 p21"]),
    "x_murder": dict(k="crime", id="x_murder", t="殺人", y=470, rec="判決 p24"),
    "x_aband": dict(k="crime", id="x_aband", t="遺棄致死など", y=522, rec="判決 p1"),
    "x_rudder": dict(k="crime", id="x_rudder", t="舵の過失", rows=("3等航海士", "操舵手（当直）"), rec="判決 p33"),
    # 結果（判決 p39：船長の殺人の有罪は反対意見なし・p24〜25：航海士と機関長に殺人の故意は認めにくい・
    #   p1：遺棄致死・p34：2審が1審の有罪を破棄して無罪・大法院も）
    "o_cap": dict(k="res", id="o_cap", t="有罪", col="c3", row="船長", rec="判決 p39"),
    "o_murder": dict(k="res", id="o_murder", t="無罪", col="c3", y=470, rec="判決 p24"),
    "o_aband": dict(k="res", id="o_aband", t="有罪", col="c3", y=522, rec="判決 p1"),
    "o_rud2": dict(k="res", id="o_rud2", t="無罪", col="c2", rows=("3等航海士", "操舵手（当直）"), rec="判決 p34"),
    "o_rud3": dict(k="res", id="o_rud3", t="無罪", col="c3", rows=("3等航海士", "操舵手（当直）"), rec="判決 p34"),
    # 刑（船員の2審 p5007 の主文：피고인1 무기징역・2 징역12년・3 징역7년・4,5 각 징역5년・9 징역10년＝大法院で確定）
    "s_captain": dict(k="res", id="s_captain", t="無期懲役", col="c3", row="船長", rec="船員の2審 p5007"),
    "s_mate1": dict(k="res", id="s_mate1", t="懲役12年", col="c3", row="1等航海士", rec="船員の2審 p5007"),
    "s_mate2": dict(k="res", id="s_mate2", t="懲役7年", col="c3", row="2等航海士", rec="船員の2審 p5007"),
    "s_chief": dict(k="res", id="s_chief", t="懲役10年", col="c3", row="機関長", rec="船員の2審 p5007"),
    "s_mate3": dict(k="res", id="s_mate3", t="懲役5年", col="c3", row="3等航海士", rec="船員の2審 p5007"),
    "s_helm": dict(k="res", id="s_helm", t="懲役5年", col="c3", row="操舵手（当直）", rec="船員の2審 p5007"),
    "s_ceo": dict(k="res", id="s_ceo", t="懲役7年", col="c3", row="会社の代表", rec="民事の判決 N"),
    # 艇長＝2審（p5002）「피고인을 징역3년에 처한다」→ 大法院（p5001）「상고를 모두 기각한다」
    "s_123": dict(k="res", id="s_123", t="懲役3年", col="c3", row="123艇の艇長", rec="艇長の判決 p5002"),
}


def ct(name, **kw):
    return dict(CTP[name], **kw)


def ce(fr, to, **kw):
    """流れ図の矢印（fr・to は部品の id か id の list）。"""
    return dict(k="edge", fr=fr, to=to, **kw)


# cb02 の船員15人（判決 p2〜3 の順を 甲板部 8・機関部 7 に分けて2列に＝役職名だけ）
CREW15 = [dict(k="grp", t="甲板部", x=84, y=372)]
for _i, (_t, _y, _c) in enumerate([("船長", 412, "who"), ("1等航海士", 412, "crime"), ("2等航海士", 460, "who"),
                                   ("3等航海士", 460, "crime"), ("操舵手（当直）", 508, "who"), ("航海士", 508, "crime"),
                                   ("操舵手", 556, "who"), ("操舵手", 556, "crime")]):
    CREW15.append(dict(k="role", id=f"d{_i + 1}", t=_t, y=_y, pos=CT["cols"][_c], grp="甲板部",
                       rec=["判決 p2", "判決 p33"] if _t == "操舵手（当直）" else "判決 p2"))
CREW15.append(dict(k="grp", t="機関部", x=84, y=626))
for _i, (_t, _y, _c) in enumerate([("機関長", 666, "who"), ("1等機関士", 666, "crime"), ("3等機関士", 714, "who"),
                                   ("操機長", 714, "crime"), ("操機手", 762, "who"), ("操機手", 762, "crime"),
                                   ("操機手", 810, "who")]):
    CREW15.append(dict(k="role", id=f"e{_i + 1}", t=_t, y=_y, pos=CT["cols"][_c], grp="機関部",
                       rec="判決 p2" if _i < 3 else "判決 p3"))
CREW15.append(dict(k="bracket", id="br15", over=[f"d{i}" for i in range(1, 9)] + [f"e{i}" for i in range(1, 8)]))
CREW15.append(ce("br15", "c1"))

# 舵を動かす仕組み（cc05・cc12）＝模式。海審 p1118 の注60「조타기 사용에 의한 전기적 신호에 따라 타를 작동하기 위한
#   유압의 흐름을 제어하는 밸브」＝操舵の電気の信号 → 弁が油の流れを切りかえる → 舵
RUD = dict(kind="模式図",
           heads=[dict(id="helm", t="操舵台", kind="node", x=(150, 470), y=(470, 570), rec="海審 p1118"),
                  dict(id="valve", t="ソレノイド弁", kind="node", x=(760, 1160), y=(470, 570), rec="海審 p1118"),
                  dict(id="rudder", t="舵", kind="node", x=(1450, 1770), y=(470, 570), rec="海審 p1118")])
RUDP = {
    "q_valve": dict(k="mark", at="valve", t="？"),
    "e_elec": dict(k="edge", fr="helm", to="valve", lab="電気の信号", rec="海審 p1118"),
    "e_oil": dict(k="edge", fr="valve", to="rudder", lab="油の流れ", rec="海審 p1118"),
    # 海審 p1118 5.3.4〜5.3.5（当直の操舵手の話・事故のあと舵が真ん中）＝固着の説を退けた
    "c_kmst": dict(k="chip", id="c_kmst", at="valve", t="報告書：退けた", dy=60, rec="海審 p1118"),
    # 特調委 p3013「솔레노이드밸브 고착이 … 급격한 우선회와 횡경사를 유발했을 가능성은 매우 낮다」
    #   （PLAN の出典は p3088＝外からの力の頁。弁の結論は p3013）
    "c_sccc": dict(k="chip", id="c_sccc", at="valve", t="特別調査委：可能性は非常に低い", dy=130, rec="特調委 p3013"),
}


def rud(name, **kw):
    return dict(RUDP[name], **kw)


# 書類の再現図（c208）。🔴 欄の名は報告書の文にあるものだけ＝海審 p1037「보고서에는 승선인원, 화물량 등이 기재되어 있지 않았다」
FORM_PRE = dict(title="出港前安全点検報告書", rec="海審 p1037",
                fields=[dict(t="乗船人員", rec="海審 p1037"), dict(t="貨物量", rec="海審 p1037")],
                ends=dict(ship=dict(t="セウォル号", rec="海審 p1037"), office=dict(t="運航管理室", rec="海審 p1037")))

# 原因の並べ図（c615・cc13）＝同じ形で並べるだけ（場面にしない）。札の言葉は原因の年表（⑤b-5 の chips）と同じ
CAUSE = {
    "rudder": dict(k="item", t="舵の使い方？", rec=["海審 p1091", "裁決 p2087"]),
    "fault": dict(k="item", t="装置の故障？", rec=["判決 p33", "特調委 p3073"]),
    # cc13 の出典（PLAN は「特調委 p4161」＝頁は小委員会の報告）＝特調委小 p4161「외부충격일 가능성을 배제할 수 없다」・p3013
    "outer": dict(k="item", t="外からの力？", rec=["特調委 p3013", "特調委小 p4161"]),
}


def cause(name, **kw):
    return dict(CAUSE[name], **kw)
