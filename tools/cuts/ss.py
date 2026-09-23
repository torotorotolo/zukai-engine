# -*- coding: utf-8 -*-
"""12本目（1954年3月1日 キャッスル・ブラボー水爆実験・第五福竜丸）の
章ファイルが共通で使う小道具。

**11本目（チャレンジャー号）の中身は git の `61039d2` にある**（`git show 61039d2:tools/cuts/ss.py`）。
10本目（三豊百貨店）は `46f11b3`、9本目（テネリフェ）は `e18b8f1`、8本目は `4c71bf0`、7本目は `ae30d49`。

■ 素材の名前（`ref/ep12/`。選び方と出どころは `qa_out/ep12_assets.py` の `PICK`）
  `ep12/<欄の名>.jpg` … 写真（NARA RG 678 の51点・Commons 20点から**絵を見て**採ったもの）
  `ep12/pg<頁>.png`   … 報告書の頁（頁番号は台本と同じ通し番号＝DNA p1〜・WT p1001〜・DASA p2001〜）
  `ep12/fb_<カットID>.jpg` … 動く映像を当てたカットの**ひかえの静止画**
  🔴 ⑤b-2（2026-09-23）で空にした直後は**未作成**＝`_assets()` が止める（権利を確かめずに焼かない）。

■ 🔴 この回は**報告書の頁そのものを画面に出す**（11本目は逆に1枚も出さなかった）
  台本 §7 の「報告書の実物の図（B）」26カット＋「報告書の実物をなぞる型」（09-23 カズヤくん決定）。
  ⚠️ 図の英字は焼き込み（→ [[reference-report-figures-have-burned-in-english]]）。
     **頁が主題**（表紙・英文の決め所・頁の中の図）のときは英字ごと出す＝§5b-5 の「主題そのもの」。
     **図だけが主題**のときは `BANDS` の `fig_box`（画素で測った矩形）で切る。
  `page(pr)` は `PAGES` に無い頁を呼んだら止まる（黙って別の頁を出さない）。

■ 🔴 人が写る点の扱い（この回）
  私人＝島の住民・日本の市民・漁船の乗組員（公的な任務ではない）＝**顔を出さない**。
  米軍の兵士・艦の乗組員・科学者＝公的な任務の人。→ [[feedback-jiko-photo-people-policy]]
  ⚠️ ②で落とした2点（久保山さんの病床・増田三次郎さんの病室＝私人の顔の近景）は採らない。

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep12"
EP = "ep12/"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対。片側だけにすると粗が反対側へ移る（[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
# 🔴🔴 2026-09-23（⑤b-2）：**12本目の63点で取り直した**（→ [[feedback-per-episode-constants-go-stale]]）。
#    `python qa_out/ep12_assets.py panel` の並びに**はっきりした切れ目**が1か所あった：
#      … AR 0.956 jp_fish_sign／AR 1.049 suits_adrikan
#      ── ここで 15ポイント飛ぶ ──
#      AR 1.200 dc_molala／AR 1.215 dmg_eneman／AR 1.225 dc_f4u_test …（4:3〜5:4 の普通の写真）
#    その中点を採る。⚠️ 11本目も 1.12 だったのは**たまたま**（写したのではなく、測って同じ値になった）。
PANEL_AR = 1.12                      # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.82。これ超＝横長すぎ

# 報告書の頁から切る図の矩形（`qa_out/ep12_assets.py` が書く `ref/ep12/pages.json`）。
_PAGES_FILE = REF / "pages.json"
PAGES: dict[str, dict] = (json.loads(_PAGES_FILE.read_text(encoding="utf-8"))
                          if _PAGES_FILE.exists() else {})
BANDS = {k: v for k, v in PAGES.items() if v.get("fig_box")}

# 画素で測った切り出し。⚠️ **原寸を見てから足す**（推定で置かない）。
TRIM: dict[str, tuple] = {}


def page(pr):
    """台本の通し頁番号（DNA p1〜・WT p1001〜・DASA p2001〜）→ 頁の画像のパス。

    🔴 章ファイルは**台本の頁番号だけ**を書く（`ss.page(212)`）。台本 §7 と1対1で照合できる。
    ⚠️ `PAGES` に無い頁を呼んだら止まる（黙って別の頁を出さない）。
    """
    key = f"pg{pr}"
    if key not in PAGES:
        raise KeyError(f"頁 p{pr} は焼いていない（`qa_out/ep12_assets.py` の PAGES_PICK に足して pages）")
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
#   ②の網で継承つきは外した（Commons 629→488）。**あとから手で1点足したときに素通りする**ので、
#   ここでも当てる（二重の網）。⚠️ `assets.json` が読めなければ**止める**
#   （0点にして素通りさせない）→ [[feedback-parsers-fail-closed]]
@lru_cache(maxsize=None)
def _assets():
    p = REF / "assets.json"
    if not p.exists():
        raise RuntimeError(
            "ref/ep12/assets.json が無い（`python qa_out/ep12_assets.py build`）。"
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
#       隠すなら元画像を直し、`ref/ep12/masked.json` に md5 を記録する。
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
        raise RuntimeError("cuts/ss.py の PANEL_AR が未測（12本目の束で `ep12_assets.py panel` から決める）")
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
#  動く映像（12本目は2本＝DOE 1280x720 全画面・4K 下を切って 3840x1688）
# ══════════════════════════════════════════════════════════
@lru_cache(maxsize=None)
def _clips():
    p = REF / "clips.json"
    if not p.exists():
        raise RuntimeError("ref/ep12/clips.json が無い（⑤b-2 で作る）")
    return json.loads(p.read_text(encoding="utf-8"))


def vid(cid, **kw):
    """動く映像のカット（ひかえの静止画つき）を1行で書く。秒は `footage.USE` が持つ。"""
    return dict(photo=fb(cid), **kw)
