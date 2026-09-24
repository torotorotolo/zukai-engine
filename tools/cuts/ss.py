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
# 🔴🔴 **12本目の値のまま＝13本目では未測**（2026-09-24 ⑤b-1）。⑤b-2 で13本目の束を作ったら
#    `python qa_out/ep13_assets.py panel` の並びの切れ目から**取り直す**（→ [[feedback-per-episode-constants-go-stale]]）。
#    12本目の根拠＝AR 1.049 と 1.200 のあいだで 15ポイント飛ぶ切れ目の中点（11本目も測って同じ 1.12）。
#    ⚠️ いまは写真を1点も当てていないので効いていない。**写真を当てる前に**取り直すこと。
PANEL_AR = 1.12                      # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.82。これ超＝横長すぎ

# 報告書の頁から切る図の矩形（⑤b-2 で作る `ref/ep13/pages.json`）。
_PAGES_FILE = REF / "pages.json"
PAGES: dict[str, dict] = (json.loads(_PAGES_FILE.read_text(encoding="utf-8"))
                          if _PAGES_FILE.exists() else {})
BANDS = {k: v for k, v in PAGES.items() if v.get("fig_box")}

# 画素で測った切り出し。⚠️ **原寸を見てから足す**（推定で置かない）。
#   12本目の4点（fo_tray・fo_tank・rongelap_booties・jp_fish_sign）は git の `3832147`。
TRIM: dict[str, tuple] = {}


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
#  継承（ShareAlike）は入れない ── 焼く側でももう一度照合する
# ══════════════════════════════════════════════════════════
#   12本目は②の網で継承つきを外した（Commons 629→488）。**あとから手で1点足したときに素通りする**ので、
#   ここでも当てる（二重の網）。⚠️ `assets.json` が読めなければ**止める**
#   （0点にして素通りさせない）→ [[feedback-parsers-fail-closed]]
#   ⚠️ 13本目の②の網が継承つきを外したかは ⑤b-2 で確かめる（外していなければ、この網の扱いを決め直す
#      ＝BY-SA は額装なら可 → [[reference-cc-by-sa-unmodified-in-video]]）。
@lru_cache(maxsize=None)
def _assets():
    p = REF / "assets.json"
    if not p.exists():
        raise RuntimeError(
            "ref/ep13/assets.json が無い（⑤b-2 で `python qa_out/ep13_assets.py build`）。"
            "権利を確かめずに焼かない → feedback-parsers-fail-closed")
    return json.loads(p.read_text(encoding="utf-8"))


def check_share_alike(spec):
    """継承つきの点を当てているカットを挙げる（空なら合格）。"""
    used = [(cid, s.get("photo")) for cid, s in sorted(spec.items())
            if (s.get("photo") or "").startswith(EP)]
    if not used:
        return []
    db = _assets()
    bad = []
    for cid, ph in used:
        r = db.get(Path(ph).stem)
        lic = str((r or {}).get("lic", "")).upper().replace("-", " ")
        if "SA" in lic.split():
            bad.append(f"{cid}＝{ph}（{r['lic']}）: この回は継承つきを入れない")
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
#   13本目で使うなら、色味と演出の相談のあとで**13本目の緯度経度と報告書の値だけ**で足す
#   （地点＝`titan_fig.GEO`・宣言＝`*_REL`・門番 `check_drift` が照合する＝ルール §5b-35・38・45）。
