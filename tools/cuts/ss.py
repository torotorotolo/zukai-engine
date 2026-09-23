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
#   ⑤b-4（2026-09-23）で 2×2 の並べ画像（1枚 950px）と原寸の切り出しで見て足した：
TRIM: dict[str, tuple] = {
    # 右 0.887 から先がフィルムの黒い縁と手書きの印（NARA #46）
    "ep12/fo_tray.jpg": (0.0, 0.0, 0.88, 1.0),
    # 焼き付けの白い余白＋右上「65%」・右「CROP」・右下「Fig 28」の書き込み（NARA #31）
    "ep12/fo_tank.jpg": (0.03, 0.035, 0.97, 0.965),
    # 焼き付けの白い縁（NARA #29）
    "ep12/rongelap_booties.jpg": (0.05, 0.04, 0.945, 0.955),
    # 🔴 看板の上の暗い戸口に**私人の顔が2つ**（原寸 y 120〜220 ＝ 0.12〜0.21）＝看板の上端 0.25 より上を落とす。
    #    右の店の女性2人は束の道具（`ep12_assets.py` の PICK の trim）で落としてある → [[feedback-jiko-photo-people-policy]]
    "ep12/jp_fish_sign.jpg": (0.0, 0.25, 1.0, 1.0),
}


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


# ══════════════════════════════════════════════════════════
#  🔴 動く模式図（drift）の地図 ── 冒頭（c104・c105）の1枚を、第4〜7章の要所で**戻す**
# ══════════════════════════════════════════════════════════
#   葦の分析を受けた決定（案B）：冒頭の物が締めで戻る骨組みを、事実の地図でやる
#   （記憶 project-jiko-visual-variety-from-ep12）。⑤b-3（2026-09-23）で c1.py から移した。
#   ⚠️ 位置と距離は `titan_fig.GEO`（緯度経度の表）と**報告書の値**だけ。`MAP_REL` を門番 `check_drift` が照合する。
SRC_DNA = "DNA 6035F（国防原子力局 1982年）"
# ⚠️ 表示の範囲は主役（ビキニ→船）が大きく見えるように詰めた（最初の 164.3〜168.9 だと画面の3割＝⑤b-2 の試し焼きで実測）
MAP_VIEW = dict(lon=(164.9, 167.95), lat=(10.98, 12.30))
# ⚠️ ロンゲラップとロンゲリックは 180px しか離れていない＝札を上下に分ける（check_layout で実測 42×22px 重なった）
MAP_PLACES = ["bikini", dict(k="rongelap", side="above"), "ailinginae", "rongerik"]
# 🔴🔴 船の位置は**どの章でも1つ**＝DNA p212「85 nmi (157 km) east-northeast of Bikini」（⑤b-3 で決めた）。
#    日本政府の文書（DNA p477 の附録）は「北緯11度52分半・東経166度35分（03:42）」＝ビキニから約135キロ。
#    ナレーションは c104・c509・c606 とも「157キロ」と読む＝地図に2つ目の船を出すと**音と絵が食い違う**。
#    → 船は157キロの1隻だけ。日本側の位置は `ship_jp`（描かない点）として置き、c605 の注で「約135キロ」と断る。
#      注の数は `MAP_REL_JP` を門番が照合する（書いた数と、緯度経度から測った距離が ±5%）。
MAP_PTS = dict(ship=dict(of="bikini", km=157, dir="東北東"))
MAP_REL = [dict(a="bikini", b="ship", km=157, dir="東北東", src="DNA p212"),
           dict(a="gz", b="rongerik", km=250, dir="東", src="DNA p212")]
MAP_PTS_JP = dict(ship_jp=dict(lat=11 + 52.5 / 60, lon=166 + 35 / 60))
MAP_REL_JP = [dict(a="ship_jp", lat=11 + 52.5 / 60, lon=166 + 35 / 60, src="DNA p477（日本政府の文書）"),
              dict(a="bikini", b="ship_jp", km=135, dir="東北東", src="DNA p477（緯度経度から測った距離）")]
MAP_NOTE = "模式図：島は環礁の中心・船はビキニから東北東へ157キロ（報告書の値）。灰の広がりの形は描いていない"

# ── 地図の範囲（⑤b-3 で足した。**同じ範囲を章をまたいで使い回す**＝同じ地図が戻る）──────
#   NEAR  … 冒頭の1枚（MAP_VIEW）。c104・c105・c509・c510（第6・7章でも戻す）
#   EAST  … NEAR を東のウトリックまで広げた1枚。c402（人の住む島々）＝第7章の島の灰でも戻せる
#   FLEET … ビキニの西の駆逐艦と南東の艦隊が入る1枚。c412・c419（第5章の艦隊の灰でも戻せる）
#   WIDE  … 1,000キロを超える船の捜索が入る1枚。c408（前の2日間・北西）・c416（当日・東北東）
#   ⚠️ 範囲の外の点も計算はされる（門番の照合は緯度経度で測る）。**描く点は範囲の中に置く**
MAP_VIEW_EAST = dict(lon=(164.9, 170.3), lat=(10.40, 12.30))
MAP_PLACES_EAST = MAP_PLACES + ["utirik"]
MAP_VIEW_FLEET = dict(lon=(163.5, 166.8), lat=(10.35, 12.25))
MAP_VIEW_WIDE = dict(lon=(152.5, 176.0), lat=(8.0, 21.5))
# ⚠️ WIDE ではビキニとエニウェトクが 126px しか離れない。上に置くと北西へ伸びる捜索の線が札を横切った
#    （⑤b-3 の試し焼き c408・c416）＝両方下に置き、エニウェトクの札だけ左へずらす
MAP_PLACES_WIDE = ["bikini", dict(k="enewetak", dx=-90)]
# ⚠️ 爆心→ロンゲリックへ線を引く地図（c509・c510）は、ロンゲラップの札を上に置くと線が札を貫く
#    （⑤b-3 の試し焼き）＝札を全部下に置く。冒頭の c104・c105 は線が無いので MAP_PLACES のまま
MAP_PLACES_LINE = ["bikini", "rongelap", "ailinginae", "rongerik"]
# 船の捜索（DNA p208・p209）。**方位角（度）と距離は報告書の値そのもの**
SEARCH_PTS = dict(srch2=dict(of="gz", km=1480, deg=300),      # 2日前：300°・800海里（1,480キロ）
                  srch1=dict(of="gz", km=1110, deg=330),      # 前の日：330°・600海里（1,110キロ）
                  srch0=dict(of="gz", km=1110, deg=65))       # 当日（追加）：65°・600海里（1,110キロ）
SEARCH_REL = [dict(a="gz", b="srch2", km=1480, deg=300, src="DNA p208"),
              dict(a="gz", b="srch1", km=1110, deg=330, src="DNA p208"),
              dict(a="gz", b="srch0", km=1110, deg=65, src="DNA p209")]
SEARCH_NOTE = "模式図：捜索の向きと長さ（報告書の値）。捜索した幅は描いていない"
# 駆逐艦レンショー（DNA p209）と艦隊の待つ所（同 p209「southeast of Bikini … 30 to 50 nmi (56 to 93 km)」）
FLEET_PTS = dict(dd_old=dict(of="bikini", km=167, deg=270), dd_new=dict(of="bikini", km=167, deg=230),
                 fl56=dict(of="bikini", km=56, dir="南東"), fl93=dict(of="bikini", km=93, dir="南東"))
FLEET_REL = [dict(a="bikini", b="dd_old", km=167, deg=270, src="DNA p209"),
             dict(a="bikini", b="dd_new", km=167, deg=230, src="DNA p209"),
             dict(a="bikini", b="fl56", km=56, dir="南東", src="DNA p209"),
             dict(a="bikini", b="fl93", km=93, dir="南東", src="DNA p209")]
FLEET_NOTE = "模式図：船の位置はビキニからの方角と距離（報告書の値）。艦の数と形は描いていない"

# ── ⑤b-4（2026-09-23）で足した範囲3つ ─────────────────────────────
#   ISLES … ロンゲラップとロンゲリックに寄った1枚（c626 島に降る灰・c702 ロンゲリックに灰）
#           🔴 降る灰（fall）は点の真上に幅約48pxの柱で落ちる（`build_jiko.draw_moves`）＝その点の札は**左**に置くしかない。
#              NEAR ではロンゲリックの左 180px にロンゲラップの輪があり、左の札が輪を貫く（計算で確かめた）＝寄った範囲を作った
#           ⚠️ 縮尺 100キロだと棒がアイリングナエの名札にかかる＝`scale_km=50`
#   WEST  … 西のエニウェトクまで（c705 ロンゲリック→エニウェトクの知らせ）
#           ⚠️ その線はロンゲラップの輪の 9px 横を通る＝ロンゲラップは置かない。線はビキニの輪の 29px 下＝ビキニの札は上
#   SOUTH … ロンゲリックから南のクェゼリンまで（c718 避難）。線はほぼ真南
#           ⚠️ ロンゲリックの札は上（線が下へ伸びる）・ロンゲラップの札は左へ 60px（線から 21px 離す）・アイリングナエは置かない
MAP_VIEW_ISLES = dict(lon=(166.0, 168.2), lat=(10.95, 11.85))
# ⚠️ アイリングナエの名札が縮尺の「50キロ」に 11×13px 重なった（check_layout・c626）＝札だけ右へ 90px
MAP_PLACES_ISLES = ["rongelap", dict(k="ailinginae", dx=90), "rongerik"]
MAP_VIEW_WEST = dict(lon=(161.9, 168.1), lat=(10.75, 12.45))
MAP_PLACES_WEST = ["enewetak", dict(k="bikini", side="above"), "rongerik"]
MAP_VIEW_SOUTH = dict(lon=(160.4, 174.6), lat=(8.0, 12.0))
MAP_PLACES_SOUTH = [dict(k="rongelap", dx=-60), dict(k="rongerik", side="above"), "kwajalein"]
ISLES_NOTE = "模式図：島は環礁の中心（緯度経度の表）。人数と時刻は報告書の値。灰の広がりの形は描いていない"
# 捜索の飛行機が引き返した所（DNA p220「reached a position approximately 65 nmi due east of [the burst point]
#   by 0950M only to abort」＝**爆心から真東へ 120キロ**。報告書は「記録のひとつ」と断る＝台本 c616 も同じ）
ABORT_PTS = dict(abort=dict(of="gz", km=120, dir="東"))
ABORT_REL = [dict(a="gz", b="abort", km=120, dir="東", src="DNA p220")]


def isles_map(steps, src="WT 1004頁・DNA p223", note=ISLES_NOTE):
    """ロンゲラップとロンゲリックに寄った地図（c626・c702 で同じ地図が戻る）。札は降る灰の柱を避けて左か上。"""
    return ("drift", drift_map(steps, view=MAP_VIEW_ISLES, places=MAP_PLACES_ISLES,
                               note=note, src=src, scale_km=50))


def drift_map(steps, pts=None, rel=None, note=None, src="DNA p212", **kw):
    """冒頭の地図（`MAP_*`）に段を載せた `drift` の引数。

    足す点（`pts`）と宣言（`rel`）は既定に**足す**（置き換えない＝船と島の照合は必ず残る）。
    表示の範囲・環礁を替えるときは `view=`・`places=` を渡す（例：1,000キロを超える捜索の地図）。
    """
    return dict(view=kw.pop("view", MAP_VIEW), places=kw.pop("places", MAP_PLACES),
                pts={**MAP_PTS, **(pts or {})}, rel=MAP_REL + list(rel or []),
                steps=steps, note=note or MAP_NOTE, src=src, **kw)
