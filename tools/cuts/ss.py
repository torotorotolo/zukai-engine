# -*- coding: utf-8 -*-
"""10本目（1995年6月29日 三豊百貨店崩壊事故）の
章ファイルが共通で使う小道具。

**9本目（テネリフェ）の中身は git の `e18b8f1` にある**（`git show e18b8f1:tools/cuts/ss.py`）。
8本目（コロンビア号）は `4c71bf0`、7本目（9.11）は `ae30d49`。

■ 素材の名前（`ref/ep10/`。選び方と出どころは `qa_out/ep10_assets.py` の `PICK`）
  `ep10/<欄の名>.jpg` … 92点。**この回は前の回と権利の形がまるで違う**：
    - **82点＝ウィキメディア・コモンズの CC BY-SA 4.0**（ソウル特別市消防災難本部ほか）
    - **10点＝公共ヌリ（KOGL）第1類型**（ソウル歴史編纂院・ソウル研究院）
  ⚠️ 動く映像は **0本**。`fb()`・`vid()` は呼ばない。

■ 🔴🔴 **CC BY-SA の82点は「額装だけ」。切る・寄る・色を変える・上に重ねるが禁止。**
  継承（ShareAlike）が動画全体に掛かるかは「翻案物を作ったか」で決まる。
  **無加工・丸ごと・独立した要素なら掛からない**（許諾 3(b)・1(a)・2(a)(4)、CC 公式の
  ShareAlike_interpretation。原文は `ref/ep10/materials.md` §1）。
  → 切った時点で翻案＝**動画全体を BY-SA にしなければならなくなる**。
  → [[reference-cc-by-sa-unmodified-in-video]]（2026-09-20 カズヤくん決定＝額装で進める）
  🔴 **これは書き方の約束ではなく、下の `FRAME_ONLY` と `check_frame_only()` が機械で止める。**
     `cuts/__init__.py` が SPEC を組んだあとに照合する＝当たれば全部の門番が落ちる。
     → [[feedback-rules-need-gates]]

■ 🔴🔴 この回も**報告書から取り出した図を画面に出さない**（`BANDS` が空）
  白書（ソウル特別市『삼풍백화점 붕괴사고 백서』）の図版は**韓国語が焼き込まれている**
  （→ [[reference-report-figures-have-burned-in-english]]）。
  下敷きは寸法と位置を取るためだけに使い、**`titan_fig` の型で描き直して日本語にする**
  （`ref/ep10/kousei.md` §2）。⚠️ だから `page()` は呼べない。呼んだら止まる。

■ 🔴🔴 額装に回す敷居（`PANEL_AR`）は**この回の素材から取り直す**
  → [[feedback-per-episode-constants-go-stale]]
  ⚠️ **この回は敷居の意味が薄い**（82点は縦横比にかかわらず額装）。
     効くのは公共ヌリの10点だけ。それでも**取り直した値を置く**（前の回の値を残さない）。

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  「画像のこの点を画面の中央に置きたい」と書けるように、点（0〜1）から逆算する。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
  ⚠️ **寄せを変えても絵が変わらないことがある**（遊びが足りないとき）。
     → [[feedback-video-qa-index]] §4「切り出しの遊びを先に測る」
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep10"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対。片側だけにすると粗が反対側へ移る（[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
# 🔴 2026-09-20（10本目 ⑤b-1）：**この回の素材で取り直した。結果は 4:3 のまま。**
#    ⚠️ この回は **`PANEL_AR` が効くのが「手直し可の10点」だけ**（残り82点は BY-SA ＝
#       縦横比にかかわらず無条件で額装）。だから測るのもその10点：
#         AR 0.660（62.9% 切れる）… `wreck_ground_04` 1点だけ（縦位置）
#         AR 1.495〜1.522（14.4〜15.9% 切れる）… 9点
#    → **0.660 と 1.495 の間に、はっきりした切れ目がある**（9本目は間が埋まっていて
#      切れ目が無く、意味で決めるしかなかった）。4:3 はその間に入る＝この回の実測でも正しい。
#    参考：82点を仮に全画面にすると 15.6〜61.6%（中央値 18.6%）切れる。
#         **額装にしないこと自体が権利の事故**なので、ここは縦横比の話ではない。
PANEL_AR = round(4 / 3, 4)          # ＝1.3333。これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.37。これ超＝横長すぎ

# 🔴 この回は報告書の図版を1枚も画面に出さない。**空であることが正しい状態**。
BANDS = {}

# 🔴🔴 切り出し窓（x0, y0, x1, y1・元画像に対する割合）。**この回はほぼ使えない。**
#    82点は CC BY-SA ＝切った時点で翻案になる（下の `FRAME_ONLY`）。
#    切ってよいのは**公共ヌリ第1類型の10点だけ**（第1類型は変形・二次的著作物の作成を許す）。
#    ⚠️ ただし公共ヌリの10点は 809×534 ほどしかないので、**切ると 1920 に伸ばす余裕が無い**。
#    ⚠️ `scene_jiko.TRIM_BY_PHOTO` がこの表を読む＝**写真ファイル単位**で効く（同じ写真の全カット）。
TRIM = {
    # 🔴 まだ空です。⑤b-2 で、公共ヌリの点に窓が要るときだけ足す。
}

def page(pr):
    """🔴 この回は報告書の図版を焼かないので**呼べない**（黙って別の絵を出さない）。"""
    raise KeyError(
        f"印字 p{pr}: 10本目は白書の図版を画面に出さない（BANDS が空／"
        f"白書の図は韓国語が焼き込み）。図は `titan_fig` の型で描き直す")


def P(name):
    """欄の名前 → `ref/` から見た写真のパス。"""
    return f"ep10/{name}.jpg"


def fb(cid):
    """動く映像を当てたカットの**ひかえの静止画**。⚠️ 10本目は動く映像0本＝呼ばない。"""
    return f"ep10/fb_{cid}.jpg"


# ══════════════════════════════════════════════════════════
#  🔴🔴 CC BY-SA の点＝**額装だけ**（切る・寄る・色を変える・上に重ねるを機械で止める）
# ══════════════════════════════════════════════════════════
#   正本＝`ref/ep10/slots_commons.json` の `mode`（"frame"＝額装だけ／"free"＝手直し可）。
#   ここでは**その json から起動時に読む**（表を手で写さない＝写し間違いが起きない）。
#   ⚠️ json が読めなければ**止める**（0点にして素通りさせない）→ [[feedback-parsers-fail-closed]]
def _frame_only():
    j = json.loads((REF / "slots_commons.json").read_text(encoding="utf-8"))
    out = {}
    for slot, items in j["slots"].items():
        for i, it in enumerate(items, 1):
            if it.get("mode") == "frame" or it.get("share_alike"):
                out[P(f"{slot}_{i:02d}")] = it.get("lic", "?")
    if not out:
        raise RuntimeError("slots_commons.json から額装専用の点が1つも読めない（fail closed）")
    return out


FRAME_ONLY = _frame_only()

# 額装の約束を破る書き方。`cuts/__init__.py` がカットの dict をこの目で照合する。
# 🔴 `zoom` は 1.0 ちょうどなら可（`fit()` が切らない）。`panel=True` は必須。
_BREAKS_FRAME = ("trim", "veil", "vignette", "focus", "xbias", "bias", "ann", "mark", "blur")


def check_frame_only(spec):
    """額装専用の点を、切る・重ねる型に渡しているカットを挙げる（空なら合格）。"""
    bad = []
    for cid, s in sorted(spec.items()):
        lic = FRAME_ONLY.get(s.get("photo"))
        if lic is None:
            continue
        why = [k for k in _BREAKS_FRAME if s.get(k) is not None]
        if not s.get("panel"):
            why.append("panel=True が無い（全画面＝上下左右が切れる）")
        if float(s.get("zoom") or 1.0) != 1.0:
            why.append(f"zoom={s.get('zoom')}（1.0 以外は切る）")
        if why:
            bad.append(f"{cid}＝{s['photo']}（{lic}）: " + "・".join(why))
    return bad


# ══════════════════════════════════════════════════════════
#  🔴🔴 置き場所を縛る点（⑤b-1 で 640px のシートを見て決めた）
# ══════════════════════════════════════════════════════════
#   **大きな袋が写っている3点**。原本は中身を書いていないので副題では断定できないが、
#   **置き場所によっては見ている人がそう受け取る**。
#   事務・補償・裁判のカットに当てると、**お金と遺体を並べた画面**になる。
#   ⚠️ これは規約の話ではない（YouTube が止めるのは生々しい損傷のある遺体）。番組としての置き方。
#   → `qa_out/ep10_sheet_notes.md`／[[feedback-subtitle-must-match-what-is-visible]]
#   値＝**当ててよいカットID**。ここに無いカットに当てたら読み込みで止まる。
RESTRICTED = {
    P("site_cleanup_02"): ("c803", "c805", "c807", "c809", "c812", "c813", "c815",
                           "c816", "c817", "c821", "c903"),
    P("site_cleanup_06"): ("c803", "c805", "c807", "c809", "c812", "c813", "c815",
                           "c816", "c817", "c821", "c903"),
    P("rescue_work_19"): ("c803", "c805", "c807", "c809", "c812", "c813", "c815",
                          "c816", "c817", "c821", "c903"),
}


def check_restricted(spec):
    """置き場所を縛った点を、許していないカットに当てていれば挙げる（空なら合格）。"""
    bad = []
    for cid, s in sorted(spec.items()):
        allow = RESTRICTED.get(s.get("photo"))
        if allow is not None and cid not in allow:
            bad.append(f"{cid}＝{s['photo']}: 救助・行方不明を語るカットだけに当てる"
                        f"（許しているのは {'・'.join(allow)}）")
    return bad


@lru_cache(maxsize=None)
def size_of(name):
    from PIL import Image
    with Image.open(HERE / "ref" / name) as im:
        return im.size


@lru_cache(maxsize=None)
def trimmed_size(name):
    """切り出しを当てたあとの寸法（画素）。切っていなければ原寸。

    🔴 2026-09-16（⑤b-2）：`TRIM`（事故現場6点の窓）も勘定に入れる。
       入れないと `kind()` と `focus()` が**台紙ごとの縦横比**で額装と寄せを決める。

    ⚠️ **`scene_jiko` を import しない。** `scene_jiko` は起動時に `cuts` を読むので、
       ここから import すると循環参照になり、章ファイルが**丸ごと黙って読めなくなる**
       （2026-09-08 に実際に起きた。`check_layout` は空の SPEC を調べて
       「✓ 全部おさまっている」を出した）→ [[feedback-gates-blind-to-the-new-material]]
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


def kind(name):
    """`dict(panel=True)` か `dict()` を返す。**縦横比で決める。目で決めない。**

    ⚠️ 縦長すぎ（< PANEL_AR）だけでなく**横長すぎ（> WIDE_AR）も額装**に回す。
    """
    a = aspect(name)
    return dict(panel=True) if (a < PANEL_AR or a > WIDE_AR) else dict()


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


@lru_cache(maxsize=None)
def _clips():
    """⚠️ 10本目は `ref/ep10/clips.json` が無い（動く映像0本）。呼ばれたら止まる。"""
    return json.loads((REF / "clips.json").read_text(encoding="utf-8"))


def bars_trim(clip, tol=2):
    """器の左右の黒帯を、額の箱の**縦横比そのもの**から追い出す `trim`。無ければ None。

    🔴 **`zoom`（＝`PILLAR`）で追い出してはいけない。**`fit()` の zoom は縦横を
       同じ率で切るので、額装で 1/PILLAR を掛けると**上下も同じ率だけ落ちる**。
    ⚠️ 幅は器の札ではなく **`clips.json` の `dispw`（②で測った絵の幅）**を使う
       → [[feedback-container-labels-lie-about-the-picture]]
    """
    c = _clips()[clip]
    w, dw = int(c["w"]), int(c.get("dispw") or c["w"])
    if dw >= w - tol:
        return None
    m = (w - dw) / 2 / w
    return (round(m, 4), 0.0, round(1 - m, 4), 1.0)


def vid(cid, pw, clip=None, **kw):
    """動く映像のカット（額装パネル＋ひかえの静止画）を1行で書く。⚠️ 10本目は使わない。"""
    t = kw.pop("trim", None) or (bars_trim(clip) if clip else None)
    d = dict(photo=fb(cid), panel=True, pw=pw, **kw)
    if t:
        d["trim"] = t
    return d


# ══════════════════════════════════════════════════════════
#  欄の名前（`qa_out/ep10_assets.py` の PICK と1対1）
# ══════════════════════════════════════════════════════════
# 🔴 ここに書いた名前が `ref/ep10/<名>.jpg` と `ref/ep10/credits.json` の鍵になる。
#    3つが食い違うと出典が出ないか、写真が出ない。
#    検算＝`python qa_out/ep10_assets.py check` と `python tools/check_credits.py`。
#    名前は `<欄>_<NN>`（`slots_commons.json` の並びのまま。手で付け直さない）。
#
# ⚠️ **この回の写真は1点残らず「崩れたあと」か「崩れる前」のどちらか**で、
#    見分けが画の意味そのものになる。副題は**写っているもの**に合わせる
#    （→ [[feedback-subtitle-must-match-what-is-visible]]／[[feedback-fallback-stills-must-match-the-era]]）。
#    🔴 崩壊前は `sampoong_before_01` `_02` の**2点だけ**。`sign_sampoong_*` は
#       看板が読めるが**どれも崩壊後**＝「開店当時の店」などと書かない。
# 🔴 2026-09-20（⑤b-1）：92点の中身・焼き込み文字・向く場面の正本＝`ref/ep10/photos.md`。
#    ⚠️ 章ファイルは `ss.P("wreck_aerial_10")` のように**名前で直に**書く（定数を増やさない）。

# ══════════════════════════════════════════════════════════
#  🔴🔴 使わない写真（シートで見て落とした。**使うと `cuts` の読み込みで止まる**）
# ══════════════════════════════════════════════════════════
#   `cuts/__init__.py` が SPEC を組んだあとに照合し、当たれば RuntimeError にする
#   ＝ 門番を1本足す代わりに、**全部の門番が落ちる**形で止める（黙って焼けない）。
#   ⚠️ ここから外すときは、理由の欄の粗が本当に消える切り方を `photos.md` に書いてから。
NG_PHOTOS = {
    # 🔴 まだ空です。⑤b-1 のシートで落とした点をここに足します。
    #    ⚠️ ②b は 222点を見て 47点を × にしており、`slots_commons.json` の92点は
    #       その網を**通ったもの**（`ref/ep10/src/seen.tsv` が記録）。
    #       ここに入るのは「②b では通ったが、⑤b で当てようとして初めて落とした点」だけ。
}
