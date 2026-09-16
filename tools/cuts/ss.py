# -*- coding: utf-8 -*-
"""9本目（1977年3月27日 テネリフェ空港衝突事故）の
章ファイルが共通で使う小道具。

**8本目（コロンビア号）の中身は git の `4c71bf0` にある**（`git show 4c71bf0:tools/cuts/ss.py`）。
7本目（9.11）は `ae30d49`。

■ 素材の名前（`ref/ep9/`。選び方と出どころは `qa_out/ep9_assets.py` の `PICK`）
  `ep9/<欄の名>.jpg` … ウィキメディア・コモンズの写真。
                       **継承なし（CC0／PD／CC BY）だけ**。CC BY-SA は1点も入れない
                       （継承が動画全体に伝染する＝`ref/ep9/materials.md` §2）。
  ⚠️ 動く映像は **0本**（`ref/ep9/materials.md` §3）。`fb()`・`vid()` は呼ばない。

■ 🔴🔴 この回も**報告書から取り出した図を画面に出さない**（`BANDS` が空）
  報告書 p58（両機の位置関係・951x1567）と p59（空港平面図・795x1760）は
  **スペイン語と英語が焼き込まれている**（→ [[reference-report-figures-have-burned-in-english]]）。
  下敷きは寸法と位置を取るためだけに使い、**`titan_fig` の型で描き直して日本語にする**
  （`ref/ep9/kousei.md` §2）。⚠️ だから `page()` は呼べない。呼んだら止まる。

■ 🔴🔴 額装に回す敷居（`PANEL_AR`）は**この回の素材から取り直す**
  → [[feedback-per-episode-constants-go-stale]]
  8本目は 4:3（＝画の4分の1を超えて切るなら額装）。**切れ目が実在しなければ意味で決める**
  （8本目の⑤b-1 で「切れ目がある」と書いて外した → [[feedback-dont-state-inferences-as-findings]]）。

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
REF = HERE / "ref" / "ep9"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対。片側だけにすると粗が反対側へ移る（[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
# 🔴 2026-09-16（9本目 ⑤b-1）：**9本目の126点で取り直した。結果は 4:3 のまま。**
#    `python qa_out/ep9_assets.py panel` の切り落とし率（小さい順・全点）:
#      0.0% …6点（16:9）／4.9〜18.7% …88点（3:2 が主）／21.4・23.8・23.8・24.8 …4点／
#      **25.0% …13点（4:3）**／25.5・26.5・27.6・29.8・29.9・31.1・33.4・34.3・34.8・35.6 …10点／
#      43.7・43.8・48.0・57.8・62.6 …5点（縦位置）
#    ⚠️ **間は埋まっていて、はっきりした切れ目は無い**（いちばん広い間は 35.6→43.7 だが、
#       そこで切ると 3:4 に近い縦長まで全画面になり、上下が3割以上消える）。
#    → 8本目と同じく**意味で決める**：画の4分の1を超えて切るなら額装＝**4:3**。
#    ⚠️ 4:3 ちょうどの13点（`losrodeos_now_10`・`_11` ほか）は **a=1.33333 > 1.3333** で全画面に入る
#       ＝上下が12.5%ずつ切れる。⑤c の原寸目視で、主題（管制塔の頭・機体の尾）が切れていないか見る。
PANEL_AR = round(4 / 3, 4)          # ＝1.3333。これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.37。これ超＝横長すぎ

# 🔴 この回は報告書の図版を1枚も画面に出さない。**空であることが正しい状態**。
BANDS = {}

# 🔴🔴 2026-09-16（⑤b-2）**事故現場6点の切り出し窓**（x0, y0, x1, y1・元画像に対する割合）。
#    6点とも「焼き付けを器具に挟んで撮った複写」で、黒い台紙・金属の留め具・角の番号札・
#    左端に縦書きの「PATERSON」（器具の商標）が写っている（`ref/ep9/photos.md` §3-6）。
#    測り方（見当で置かない）：
#      ① 焼き付けの中央帯（見当の内側 30〜70%）の**列平均・行平均の輝度**を 15px でならす
#      ② 見当 ±4% の中で「p[i+d]−p[i−d]」がいちばん大きい所＝台紙→焼き付けの段差
#         （d＝短辺の0.4%。段差の大きさ＝輝度 57〜181。どの辺もはっきり取れた）
#      ③ 段差から**内側へ 1.5%** 入れる（台紙の縁・留め具の影を残さない）
#    検算：切り出した6枚を 640px のシート1枚で見た＝台紙・留め具・「PATERSON」は6枚とも窓の外。
#      切り出した絵の縦横比は 1.316〜1.344（klm_02 は縦 0.759）＝4:3 の焼き付けそのものの比。
#      ⚠️ 焼き付け自体に小さなほこりが数点（klm_01・klm_03・both_02 の右上の空）＝⑤c で原寸を見る。
#    ⚠️ 道具（使い捨て）：⑤b-2 のスクラッチ `wreck_trim.py`。値はここが正本。
#    ⚠️ `scene_jiko.TRIM_BY_PHOTO` がこの表を読む＝**写真ファイル単位**で効く（同じ写真の全カット）。
TRIM = {
    "ep9/wreck_klm_01.jpg": (0.198, 0.1986, 0.8286, 0.7652),      # 3241×2739 → 2043×1552
    "ep9/wreck_klm_02.jpg": (0.2412, 0.1319, 0.7999, 0.8119),     # 2778×3007 → 1552×2044（縦）
    "ep9/wreck_klm_03.jpg": (0.197, 0.2102, 0.8468, 0.7687),      # 5000×4366 → 3248×2438
    "ep9/wreck_both_01.jpg": (0.1716, 0.1865, 0.7788, 0.7469),    # 3367×2749 → 2044×1540
    "ep9/wreck_both_02.jpg": (0.2008, 0.1996, 0.8413, 0.7563),    # 3206×2744 → 2053×1527
    "ep9/wreck_engine_01.jpg": (0.2052, 0.1766, 0.8528, 0.7424),  # 5052×4360 → 3271×2466
}


def page(pr):
    """🔴 この回は報告書の図版を焼かないので**呼べない**（黙って別の絵を出さない）。"""
    raise KeyError(
        f"印字 p{pr}: 9本目は報告書の図版を画面に出さない（BANDS が空／"
        f"p58・p59 はスペイン語と英語が焼き込み）。図は `titan_fig` の型で描き直す")


def P(name):
    """欄の名前 → `ref/` から見た写真のパス。"""
    return f"ep9/{name}.jpg"


def fb(cid):
    """動く映像を当てたカットの**ひかえの静止画**。⚠️ 9本目は動く映像0本＝呼ばない。"""
    return f"ep9/fb_{cid}.jpg"


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
    """⚠️ 9本目は `ref/ep9/clips.json` が無い（動く映像0本）。呼ばれたら止まる。"""
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
    """動く映像のカット（額装パネル＋ひかえの静止画）を1行で書く。⚠️ 9本目は使わない。"""
    t = kw.pop("trim", None) or (bars_trim(clip) if clip else None)
    d = dict(photo=fb(cid), panel=True, pw=pw, **kw)
    if t:
        d["trim"] = t
    return d


# ══════════════════════════════════════════════════════════
#  欄の名前（`qa_out/ep9_assets.py` の PICK と1対1）
# ══════════════════════════════════════════════════════════
# 🔴 ここに書いた名前が `ref/ep9/<名>.jpg` と `scene_jiko.EP9_PHOTO` の鍵になる。
#    3つが食い違うと出典が出ないか、写真が出ない。
#    検算＝`python qa_out/ep9_assets.py check` と `python tools/check_credits.py`。
#
# ⚠️ `losrodeos_now_*` と `laspalmas_now_*` は**全部いまの空港**。副題に必ず「現在の…」と書く
#    （→ [[feedback-fallback-stills-must-match-the-era]]／[[feedback-subtitle-must-match-what-is-visible]]。
#    門番は被写体の年の食い違いを見ない）。
# 🔴 2026-09-16（⑤b-1）：126点を落とし、**640px のシート24枚で全点を見た**。
#    1点ずつの中身・主題の位置・焼き込み文字・向く場面の正本＝`ref/ep9/photos.md`。
#    ⚠️ 章ファイルは `ss.P("losrodeos_now_09")` のように**名前で直に**書く（定数を増やさない）。

# ══════════════════════════════════════════════════════════
#  🔴🔴 使わない写真（シートで見て落とした。**使うと `cuts` の読み込みで止まる**）
# ══════════════════════════════════════════════════════════
#   `cuts/__init__.py` が SPEC を組んだあとに照合し、当たれば RuntimeError にする
#   ＝ 門番を1本足す代わりに、**全部の門番が落ちる**形で止める（黙って焼けない）。
#   ⚠️ ここから外すときは、理由の欄の粗が本当に消える切り方を `photos.md` に書いてから。
NG_PHOTOS = {
    P("cockpit_747_01"): "747-400 のガラス画面の操縦室（1977年の型ではない）。操縦桿に「DANGER」の札が焼き込み",
    P("engine_747_01"): "737 のエンジン（747 ではない）",
    P("cockpit_747_14"): "米空軍 E-4B。顔の分かる軍人が主役",
    P("panam_747_same_type_02"): "`panam_747_same_type_01` を切り抜いた同じ写真（画素が重複）",
    P("panam_747_same_type_03"): "1975年のフォード大統領とベトナム孤児の空輸。主題が別で、子どもの顔が写る",
    P("panam_747_same_type_04"): "1970年のパンナムの人物の肖像。機体は手に持った写真だけ",
    P("jumbo_era_05"): "`cockpit_747_06` の縮小複製（586×392）",
    P("klm_747_1971_02"): "見物客（私人）の顔が画面の下半分を占める",
    P("laspalmas_now_03"): "私人の顔が大写しの群衆",
    P("laspalmas_now_04"): "私人の顔が大写し。搭乗口の番号札（A30ほか）も焼き込み",
    P("laspalmas_now_06"): "私人（喫煙する男性）の顔が主役",
    P("laspalmas_now_10"): "ガラス面に描かれた人物のイラスト（空港の絵にならない）",
    P("nl_mourning_05"): "遺族（私人）の顔が大写しの悲嘆の場面",
    P("memorial_04"): "犠牲者（私人）の名前が読める銘板（チャンネルの線引き：私人は名前を出さない）",
}
