# -*- coding: utf-8 -*-
"""18本目（スレッシャー号のリメイク・1963-04-10・米海軍の潜水艦の事故）の章ファイルが共通で使う小道具。

**16本目（バイオントダム災害）の中身は git の `b044b56` にある**（`git show b044b56:tools/cuts/ss.py`）。
15本目（リノ・エアレース2011）は `c646174`、14本目（セウォル号）は `dc6ecf4`、13本目（トルコ航空981便）は `b54ee4f`、
12本目（キャッスル・ブラボー）は `3832147`、11本目（チャレンジャー号）は `61039d2`、10本目（三豊百貨店）は `46f11b3`、
9本目（テネリフェ）は `e18b8f1`、8本目は `4c71bf0`、7本目は `ae30d49`。

🔴 **⑤b-1（2026-10-04・18本目）で空にした**＝§0b。16本目の束の定数（顔だけモザイクの PD 写真1点 NEEDS_MASK）は外した。
16本目の型の値（案C の出典の表・時計と想定の札・壊れる物のカット・軸の型・水位と斜面の速さの線・棒・流れ図と書類の再現図・
並べ図・決め所の出どころの札）は、門番の selftest の見本 `tools/fixture_ep16.py` へ移した（値は1つも変えていない＝git の
`b044b56` と同じ）。15本目の型の値は `tools/fixture_ep15.py`（2026-10-01 に移した・git の `c646174`）、14本目の型の値は
`tools/fixture_ep14.py`（2026-09-30 に移した・git の `dc6ecf4`）。18本目の束は写真の束のチャットで作る。
🆕 下の「素材の名前」「人が写る点の扱い」は、18本目の束を作る ⑤b-7 で書く（16本目の書きぶりは git の `b044b56`）。

■ 素材の名前・■ 人が写る点の扱い（この回）
  🔴 **18本目の束（`ref/ep18/` の写真・頁・権利の台帳）と人の扱いは ⑤b-7 のチャットで書く**。それまでは名前の決まりだけ：
  `ep18/<欄の名>.jpg`（写真）・`ep18/pg<頁>.png`（報告書の頁＝切り口はカットごと・下の `ptrim`）。
  🔴 束が無ければ `_assets()` が止める（権利を確かめずに焼かない）。
  ✅ 2026-10-04（⑤b-7a）：写真の束＝`qa_out/ep18_assets.py`（旧版 `ref/thresher/` から写した23点＋Commons の新しい8点＝了承のあと）。
     すべて米海軍の職務著作＝PD（BY-SA・引用は0＝額装だけの点は無い）。289-T の英字の札・428-N の台紙は**束の中で切り落とした**
     （`assets.json` の `crop_px`）。就役式（1961-08-03）の左の座った観客（私人）も束で切り落とした＝`NEEDS_MASK`・`PRIVATE_OUT` は空
     （私人の顔が元画像に残っていない＝門番が窓と照らす範囲ではなく、ファイルの外）
  ・人が写る点は ルール §B2-1・§B2-2・§B2-2b（私人の顔と名前は出さない・顔だけモザイクは改変を許す権利の点だけ・
    CC BY-SA は**額装・1点1カット**・遺体の写真は使わない）→ [[feedback-jiko-photo-people-policy]]

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep18"
EP = "ep18/"
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
#    ✅ 2026-09-30（15本目 ⑤b-6）に**15本目の束（写真19点＋courtesy の紙面8点）で取り直した**。
#       `python qa_out/ep15_assets.py panel` の並びで、16:9 より縦長の側のいちばん大きな切れ目は AR 1.505（事故の週の
#       tataquax の5点・3:2）→ 1.700（damage_1970）の 19.5ポイント＝中点 1.60（次は 1.353→1.385 の 3.2ポイント）。
#       ⚠️ 27点のうち額装だけでない（`kind()` が効く）のは CC BY の3点だけ（gg_nose_2010・gg_pit_2010・seminar_2016）
#    ✅ 2026-10-02（16本目 ⑤b-7）に**16本目の束（46点）で取り直した**。`python qa_out/ep16_assets.py panel` の並びで、
#       16:9 より縦長の側のいちばん大きな切れ目は AR 0.994（pirago_tower_1963）→ 1.213（aerial_slide_1963）の 21.9ポイント
#       ＝中点 1.10（次は 1.559→1.705 の 14.6・0.853→0.994 の 14.1）。幅 1280px 以上の 4:3〜3:2（いまのダム・湖・すべり面・
#       操作の建物・トック山・標識・建設前の絵はがき・天端と満水の湖）は全画面、1963年の記録写真（幅 318〜908px）は額装。
#       ⚠️ WIDE_AR＝2.87 になる＝前後の合成 `longarone_before_after`（AR 2.773・c901）が全画面で左右 36% 切れる
#          ＝c901 の SPEC に `panel=True` を明記（左右の比べを切らない）
#    🔴 2026-10-04（18本目 ⑤b-1）：下の値 1.10 は**16本目の束の値のまま**（§0b で空にする値ではなく、束ごとに取り直す定数）。
#       ⑤b-7 で18本目の束（`python qa_out/ep18_assets.py panel` の並び）で取り直す。それまで WIDE_AR も 16本目の値（2.87）から導かれる
#    ✅ 2026-10-04（18本目 ⑤b-7a）に**18本目の束（旧版から写した23点）で取り直した**。`python qa_out/ep18_assets.py panel` の並びで、
#       16:9 より縦長の側のいちばん大きな切れ目は AR 1.552（page24＝アルバムの頁全体）→ 1.778（bow_plating_t5・tracks_t41＝16:9 に
#       切った点）の 22.6ポイント＝中点 1.665 を丸めて 1.66（次は 1.387→1.525 の 13.8・0.895→1.026 の 13.1）。
#       ⚠️ 1963〜64年の海の底の写真と継ぎ写真（モザイク）・頁・記録映画のコマ（655×480）はほぼ全部が額装になる＝**全画面で寄せたい
#          カットは、章ファイルでカットごとの `trim`（16:9・幅 1280px 以上）を書く**（kind() はファイルの縦横比だけを見る）。
#       ⚠️ WIDE_AR＝1.90 になる＝横長の3点（running_t2 2.07・shipyard_sail_t14 2.07・rudder_t24 1.94）は kind() で額装
PANEL_AR = 1.66                     # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝1.98。これ超＝横長すぎ

# 報告書の頁から切る図の矩形（写真と頁の束のチャットで作る `ref/<回>/pages.json`＝15本目は `ref/ep15/pages.json`）。
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
#   🔴 2026-09-30（15本目 ⑤b-1）：14本目の写真の切り出し2点（私人の顔と名前を外した光化門 2018・救命胴衣の列 2017）は
#      git の `dc6ecf4`。残す教訓＝**私人の顔と名前は 640px のシートでは見えない**（原寸の切り出しで見つけた＝§5b-97）。
#      切り出しで外したら、外した範囲を下の `PRIVATE_OUT` にも書く（門番 photomask が全カットの窓と照らす）
TRIM: dict[str, tuple] = {
}
TRIM.update({f"{EP}{k}.png": tuple(v["trim"]) for k, v in PAGES.items() if v.get("trim")})
# 🔴 2026-09-30（15本目 ⑤b-6）：**頁の切り口はカットごと**（同じ頁を2カットで別の所を切る＝p15 c507・c611／p32 c105・c708／
#    p35 c409・c601／p37 c618・c703）。`qa_out/ep15_assets.py pages` が `pages.json` の `cuts` に書く＝章ファイルは
#    `photo=ss.page(N), trim=ss.ptrim("c…")`（頁ごとの `TRIM` は置かない＝どのカットにも黙って効く切り口を作らない）
PAGE_CUT_TRIM: dict[str, tuple] = {cid: tuple(t) for v in PAGES.values() for cid, t in (v.get("cuts") or {}).items()}


def ptrim(cid):
    """カットの頁の切り口（頁の割合 x0,y0,x1,y1）。`pages.json` に無ければ止める（黙って頁全体を出さない）。"""
    if cid not in PAGE_CUT_TRIM:
        raise KeyError(f"{cid} の頁の切り口が無い（`qa_out/{EP[:-1]}_assets.py` の PAGE_CUTS に足して pages）")
    return PAGE_CUT_TRIM[cid]


# 🆕 2026-10-05（18本目 ⑤b-7b）：**頁のカットの寄りの縦の寄せ（bias）も `pages.json` から読む**（手で写さない）。
#    行間の詰まった頁（議会の本）は上下どちらのすき間も寄りの縮みの半分に足りず、bias 0.5 のままだと端の行が寄りの終わりに
#    72〜87% しか見えなかった（門番 edges・6カット）＝`qa_out/ep18_assets.py` の `_fit_cut` が縮みをすき間の広さに比例して配る。
#    `pages.json` に bias の表が無い回（16本目まで）は 0.5＝今までどおり。表がある回で欠けていたら止める
PAGE_CUT_BIAS: dict[str, float] = {cid: float(b) for v in PAGES.values() for cid, b in (v.get("bias") or {}).items()}


def pbias(cid):
    """カットの頁の寄りの縦の寄せ（SPEC の `bias`）。"""
    if cid in PAGE_CUT_BIAS:
        return PAGE_CUT_BIAS[cid]
    if any("bias" in v for v in PAGES.values()):
        raise KeyError(f"{cid} の頁の寄せが無い（`qa_out/{EP[:-1]}_assets.py pages` をもう一度）")
    return 0.5


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


def vid(cid, **kw):
    """🆕 18本目 ⑤b-7c：カットまるごとの動く映像（記録映画＝`footage.USE`）を1行で書く。箱はひかえの静止画の縦横比
    （記録映画 655×480＝額装＋地のぼかし＝映像方針 §8）。副題は**選んだショットに写っているもの**（撮影日は分からない＝年を書かない）"""
    return dict(photo=fb(cid), **kind(fb(cid)), **kw)


def head(cid, until=1, **kw):
    """🆕 18本目 ⑤b-7c：映像の差し込み（頭）の intro＝カットの頭の until 行だけ `footage.USE[cid]`（head=True）の映像。
    ひかえの静止画＝記録映画は `fb_<cid>.jpg`・フリー素材は `stock/fb_<cid>.jpg`（`qa_out/<回>_assets.py fb`）。
    フリー素材は見出しを書かない（左上の「イメージ」と出典だけ）・記録映画は t と s（写っているもの）を書く"""
    import footage as _FO
    stock = (_FO.CLIPS.get((_FO.USE.get(cid) or {}).get("clip")) or {}).get("stock")
    return dict(foot=True, until=until, photo=f"{EP}stock/fb_{cid}.jpg" if stock else fb(cid), **kw)


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
    # 🔴 2026-10-04（18本目 ⑤b-7a）：18本目の束は**全部が米海軍の PD**＝継承つき・引用は0点（正しい）。前の網は「1点も無い」を
    #    読み損ないとして止めていた（14〜16本目は必ずあった）。読み損ないは `_assets()` が止める（ファイルが無い）ので、ここでは
    #    **束が空**（0点＝読めていない）のときだけ止め、束に点があって継承つきが0なら {} を返す。束の側の権利は assets.json の lic
    db = _assets()
    if not db:
        raise RuntimeError("assets.json が空（束が読めていない＝fail closed）")
    out = {P(n): r["lic"] for n, r in db.items() if _is_sa(r.get("lic")) or r.get("frame")}
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
        # 🆕 18本目 ⑤b-7c：写真・頁の差し込み（尻）は寄る（build_jiko.tail_frame）＝継承つきは使えない
        tail_ph = (s.get("tail") or {}).get("photo")
        if tail_ph in fo:
            bad.append(f"{cid}＝tail の {tail_ph}（{fo[tail_ph]}）: 尻の差し込みは寄る（端を切る）＝継承つきは使えない")
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


def check_card_mix(spec, heads, fo=None):
    """🔴 2026-09-30（15本目 ⑤c'・ルール §5b-110）：章の扉の地（`build_jiko.card_frame`）は、頭のカットの写真を章の色で
    **染めて全画面に拡大して**混ぜる（既定 0.36）＝額装だけの点（BY-SA・courtesy の紙面の引用＝`frame_only`）を頭に持つ章は、
    カットの SPEC に `card_mix=0` を**書く**（書かなければ既定で混ざる＝止める）。空なら合格。
    15本目 c300card（報告書の図5＝courtesy）・c400card・c800card（BY-SA）＝640px のシートで見つけた（門番は扉を見ていなかった）。
    12〜14本目の扉も同じ作り（公開ずみ＝直さない）。呼ぶ側＝`scene_jiko`（扉の一覧 CARD_HEADS が決まった直後・読み込みで止める）
    fo＝額装だけの点の表（selftest が見本を渡す＝回の台帳に左右されない）。本番は渡さない＝assets.json から読む"""
    fo = frame_only_for(spec) if fo is None else fo
    bad = []
    for cid in sorted(heads):
        s = spec.get(cid) or {}
        ph = s.get("photo") or (s.get("intro") or {}).get("photo")
        if ph in fo and float(s.get("card_mix", 1.0)) > 0:
            bad.append(f"{cid}＝{ph}（{fo[ph]}）: 扉の地に染めて拡大して混ぜる（card_mix={s.get('card_mix', '未記入＝既定 0.36')}）"
                       "＝額装の約束（無加工・丸ごと・色を変えない）を外れる → SPEC に card_mix=0")
    return bad


# ══════════════════════════════════════════════════════════
#  🔴🔴 使わない写真（シートで見て落とした。**使うと `cuts` の読み込みで止まる**）
# ══════════════════════════════════════════════════════════
#   `cuts/__init__.py` が SPEC を組んだあとに照合し、当たれば RuntimeError にする。
#   ⚠️ ここに無い点は「まだ見ていない」だけで、「危険が無い」ではありません。
NG_PHOTOS: dict[str, str] = {}

# 🔴 元画像そのものを直してから焼く点（私人の顔・名前）。
#    ⚠️ **`blur=` は書けるように見えて誰も読まない**（10本目で私人の顔が素のまま焼けた）。
#       隠すなら元画像を直し、`ref/<回>/masked.json`（`REF` から引く）に md5 を記録する。
#    → [[feedback-settings-may-not-reach-the-picture]]／[[feedback-jiko-photo-people-policy]]
#    🔴 2026-09-28（14本目 ⑤b-1）：13本目の1点（慰霊の名前の壁 names_wall・c814）を外した＝git の `b54ee4f`。
#       ⚠️ CC BY-SA の点は隠すこと自体が翻案＝使わない（ルール §B2-2）。隠せるのは改変を許す権利の点だけ
#    🔴 2026-10-01（16本目 ⑤b-1）：15本目の2点（gg_nose_2010・gg_pit_2010＝顔だけモザイク）を外した＝git の `c646174`。
#    🔴 2026-10-04（18本目 ⑤b-1）：16本目の1点（`ep16/trial_1968.jpg`＝1968年11月のラクイラの法廷・PD＝座っている人の横顔8人は
#       私人か写真では決められない＝顔だけモザイク）を外した＝git の `b044b56`（範囲は `qa_out/ep16_assets.py` の MASK）。
NEEDS_MASK: dict[str, str] = {}

# 🔴 2026-09-29（14本目 ⑤b-7a）：**切り出し（`TRIM`）で外した私人の範囲**（元画像の割合 x0,y0,x1,y1・何か）。
#    門番 photomask が「その写真を使う全カットの窓（`trim` か `TRIM`・冒頭の写真は切らない＝全体）がこの範囲に
#    1画素も入らない」を見る（NEEDS_MASK は元画像を直す点だけ＝切り出しで外した点を見ていなかった）。範囲は原寸で見て測った
#    🔴 2026-09-30（15本目 ⑤b-1）：14本目の2点（光化門 2018 の板・救命胴衣の列 2017 の奥の人）を外した＝git の `dc6ecf4`。
#       15本目は観客（私人）が写る写真が多い（事故の日の BY-SA・courtesy の頁）＝外す範囲は写真の束で原寸で見て書く
PRIVATE_OUT: dict[str, list] = {
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
# 🔴 2026-10-04（18本目 スレッシャー号 ⑤b-1・§0b）：16本目の値（出典の表 REC_DOCS・割れる時刻 ILLU_SPLIT_TIMES・時計の札 ILLU_CLOCK_OK・
#    描いてよい数 ILLU_COUNTS・想定の札 ILLU_ASSUME・壊れる物のカット ILLU_DESTROY_CUTS）は selftest の見本
#    `tools/fixture_ep16.py` へ移した（値は1つも変えていない＝git の `b044b56`）。18本目の値は、その型を初めて使う ⑤b のチャットで
#    入れる（空のあいだ、その型を使うカットは門番・型が止まる＝fail closed）。
#    ⚠️ `ILLU_ASSUME`・`ILLU_DESTROY_CUTS` は16本目で足した表＝空の器には置いていない（門番 check_illu は無ければ空として読む＝
#       想定の札・壊れる物の部品は全部止まる）。18本目で使うなら `ILLU_ASSUME = {}`・`ILLU_DESTROY_CUTS = ()` の形で足す。
#    🆕 2026-10-04（18本目 ⑤b-2）：18本目の値を入れた（下）。🔴 §0b に足す名＝`ILLU_ASSUME`・`ILLU_DESTROY_CUTS`・`ILLU_SUB_UNTIL`・
#       `ILLU_SUB_EXC`・`ILLU_SUB_STOP`・`ILLU_BOOM_CUTS`・`ILLU_MIX_TODO`（次の回は空に＝無ければ門番は空として読み、潜水艦・音の輪・
#       壊れる物の部品は全部止まる）
#    ⚠️ 16本目の決め（時計は 22:39 だけ・秒の札は出さない・群れは住民の影だけ ほか）の理由は移した注の側にある＝fixture_ep16 の
#       案C の節の上
REC_PAGES = REF / "src" / "ep18_pages.txt"      # ④ の make_pages.py の出力（git の外＝手元だけ）
# 🆕 2026-10-04（18本目 ⑤b-2＝案C を初めて使うチャット）：頁の番号は台本 第2版の冒頭の表「出典欄の略号と頁」（`ref/ep18/daihon_v2.md`）
#    ＝原文の通し頁ファイルの番号：V1＝PDF の頁のまま p1〜p300／X＝p1001〜／IR18＝p2001〜／R08＝p4001〜／R17＝p6001〜p6319（OCR）・
#    p.97 の要旨の書き起こし＝p9802（R17書）／J＝印刷頁＋8000／No.710-64＝p9801。画面の名は語りの呼び名に合わせた（査問会の記録・
#    上級の意見書・海軍研究所の報告・議会の公聴会）。🔴 V1 の43頁は見た目の字が描けていない（映さない）＝出典の頁としては文字の層で照らす
REC_DOCS = {
    "V1": dict(range=(1, 300), name="査問会の記録 第1巻（第1回公開）", page="pdf", base=0),
    "X": dict(range=(1001, 1600), name="査問会の証拠（第9・10回公開）", page="pdf", base=1000),
    "IR18": dict(range=(2001, 2203), name="上級の意見書（第18回公開）", page="pdf", base=2000),
    "R08": dict(range=(4001, 4300), name="査問会の記録（第8回公開）", page="pdf", base=4000),
    "R17": dict(range=(6001, 6319), name="海軍研究所の報告（1964年・第17回公開）", page="pdf", base=6000),
    "R17書": dict(range=(9802, 9802), name="海軍研究所の報告（1964年・第17回公開）", page="pdf", base=9705),
    "J": dict(range=(8001, 8192), name="米議会 両院原子力合同委員会の公聴会記録（1965年）", page="print", base=8000),
    "No.710-64": dict(range=(9801, 9801), name="国防総省の発表 No.710-64（1964年）", page=None, base=0),
    # 🆕 ⑤b-5（c512）：Stierman 1964（海軍の広報を調べた修士論文・付録に国防総省の発表 509-63）＝語りは「当時の海軍の広報を調べた論文」
    "D": dict(range=(9001, 9001), name="海軍の広報を調べた論文（1964年）", page=None, base=0),
    # 🆕 ⑤b-6b（c808・c912・c918・c919・c823）：AP の記事（2021-08-02・Military Times 掲載＝通し頁 p9901）／cb20：NAVSEA の記事
    #   （2023-04-06＝p9951）／c817・c818・c820・c918：元分析官の書簡（2013-04-10・個人＝p9961＝画面に使う短い一節だけを 2026-10-04 に
    #   アプリ内ブラウザの本文で1字ずつ照らして通し頁に足した）。名前は語りだけ（画面の資料名は役割で）
    "AP": dict(range=(9901, 9901), name="AP通信の記事（2021年8月2日）", page=None, base=0),
    "NAVSEA": dict(range=(9951, 9951), name="米海軍 艦艇の部門の記事（2023年4月6日）", page=None, base=0),
    "A-R": dict(range=(9961, 9961), name="元分析官の書簡（2013年4月10日・個人）", page=None, base=0),
}
# 割れる時刻＝台本 §1-5 に無い（9時18分ごろ〈認定19〉と 9時18.1分〈認定18・意見45〉は「ごろ」で合う）＝空
ILLU_SPLIT_TIMES = ()
ILLU_CROWD_UNTIL = None
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
# 🔴 秒の札は出さない（空＝全部止める）。元分析官の「約0.1秒」（A-R）は絵にも札にも使わない（映像方針 §1-3 推定の絵の約束①）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）
# 時計の札（映像方針 18本目 §12 ⑤）：7:47（認定15）・9:09（意見45）・9:13（認定16）・9:15ごろ（認定22c）・9:16ごろ・9:17ごろ（認定17）・
#   9時18.1分（認定18・意見45＝分の小数＝門番 ⑤ は小数まで読む・読めなければ止める）・9:21（認定22d）・17:30ごろ（⑤b-3 の SB）。
#   ⚠️ 9:18（「ごろ」＝認定19）は表に入れない（9時18.1分と並べると別の時刻に見える＝絵では 9時18.1分だけ）
#   🆕 ⑤b-3：7:45（認定11「at 0745R, 10 April 1963」＝c308 の待ち合わせ・R08 p.185）・5:30（認定34「at about 0530R on 11 April 1963」
#   ＝c519 の「11日 5:30ごろ」・R08 p.188）
ILLU_CLOCK_OK = ("5:30", "7:45", "7:47", "9:09", "9:13", "9:15", "9:16", "9:17", "9:18.1", "9:21", "17:30")   # 札に出してよい時計の時刻（門番 ⑤）
# 描いてよい数（映像方針 §12 ③'）：スカイラーク1・スレッシャー1（9:17まで）・救難室1。
#   🆕 ⑤b-3：リカバリー1（認定30・31）・ミザー1・トリエステ2世1・船体の一部1（R17 p.97 の要旨＝R17書 p9802）。
#   ⚠️ 描かない＝捜索の艦（認定34「additional ships and aircraft」＝数が無い）・The Fish と案内索のおもり（ca22 の語りに無い・同じ時刻に
#   動いていた記録が無い）・大きな塊（「five or six」＝数が1つに決まらない）。目印900個と壊れた船体の破片は数えない形（obj を持たない）
ILLU_COUNTS = dict(skylark=(1, "R08 p4185"), thresher=(1, "R08 p4185"), chamber=(1, "V1 p38"), recovery=(1, "R08 p4188"),
                   mizar=(1, "R17書 p9802"), trieste2=(1, "R17書 p9802"), hull_part=(1, "R17書 p9802"))
# 🆕 18本目 ⑤b-2：想定の札（門番 check_illu ④＝表のカットは札が要る・表に無いカットに札を出さない）。c103 は 9:17 から（assume_at）
ILLU_ASSUME = {"c103": "推定（査問会の見立て）", "c318": "少佐の証言（仮定）"}
# 壊れる物（潜水艦の圧壊・破片＝SA の sub が crush）を描いてよいカット（門番 ⑫＝空なら全部止める）＝冒頭 c103 だけ（10-01 案2）
ILLU_DESTROY_CUTS = ("c103",)
# 🆕 18本目 ⑤b-2：潜水艦の時刻（門番 ⑮）＝9:17 までの段だけ・例外は c103（推定の札つき・9時18.1分の圧壊まで）。
#   ILLU_SUB_STOP＝ここで艦の絵を止めるカット（本編 c411＝kousei §4-1）＝このあとのカットに潜水艦を置かない（c420・c422・c502）
ILLU_SUB_UNTIL = "9:17"
ILLU_SUB_EXC = {"c103": "9:18.1"}
ILLU_SUB_STOP = "c411"
# 9時18.1分の大きく低い音の輪（門番 ⑰）を置いてよいカット＝c103 だけ
ILLU_BOOM_CUTS = ("c103",)
# 🆕 18本目 ⑤b-2：混ざり（映像→絵・絵→写真）の**本物の側のつなぎ待ち**（門番 ⑦）。SA の段はこのチャットで作って焼く・本物の映像と
#   写真は ⑤b-7 の束で足す＝それまで画面の種類「混ざり」のカットを全面の絵で書いてよい（⚠️ 参考の行を毎回出す）。
#   🔴 束（`ref/ep18/credits.json`）ができたら、つないでいないカットは止まる（忘れ防止＝fail closed）。つないだら表から外す
#   ✅ 2026-10-05（⑤b-7c）：c102（1行目＝記録映画 85185＝intro foot）・c103（3行目＝写真 thr_t16＝tail）をつないだ＝空に
ILLU_MIX_TODO = {}
ILLU_MIX_BUNDLE = REF / "credits.json"

# 🔴 §0b：軸の型（`tools/axis.py`・14本目 ⑤b-5）の「割れる時刻の印」に添える出典の名（`rec=` の資料名 → 画面の名）。
#   語りが資料を呼ぶ名に合わせる（海審の特別調査報告＝語りは「報告書」）。ILLU_SPLIT_TIMES の時刻は、軸の型では
#   **出典の名つきでだけ**出してよい（門番 check_axis ②＝点に by=True か split）
# 🔴 2026-10-04（18本目 ⑤b-1）：空にした（16本目の値＝`tools/fixture_ep16.py`・git の `b044b56`）。REC_DOCS の資料名が決まってから、
#    語りが資料を呼ぶ名に合わせて入れる（軸の型を初めて使う ⑤b のチャットで）
AXIS_DOCS = {}   # 18本目は割れる時刻・出典の名つきの点を使わない（⑤b-5）＝空のまま

# 軸（カットをまたいで同じ軸を使う＝前のカットの点を past で沈めて続ける）。回ごとに `AX_<名> = dict(view, span, ticks)` を足す
# 🔴 2026-10-04（18本目 ⑤b-1）：16本目の軸（AX_DAY・AX_EVE＝10月9日の時刻の帯／AX_ANS・AX_ENEL・AX_PERMIT・AX_Y3・AX_EXP・AX_MERLIN・
#    AX_MODEL・AX_Y63・AX_INQ・AX_DEC・AX_CIV＝年表）・部品 AXI の16本目の項目・関数 `dot()` は `tools/fixture_ep16.py` へ移した
#    （値は1つも変えていない）。15本目の軸（AX_HIST ほか）は `tools/fixture_ep15.py`。18本目の軸は ⑤b で足す。
#    ⚠️ 軸の教訓は移した注の側にある（年だけの値は年の真ん中に置く＝fixture_ep15 の AXI の上／札が枠の端・章の札・見出しに触れた
#       layout の直し＝fixture_ep16 の AX_*・AXI の上）。⚠️ 割れる時刻の印（split）は ILLU_SPLIT_TIMES の時刻だけ・出典の名つき

# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
AXI = {}


def ax(name, **kw):
    """AXI の部品の写し（同じカットで past と add に同じ物を2回入れても別の部品になる）。"""
    return dict(AXI[name], **kw)


# ══════════════════════════════════════════════════════════
#  🆕 18本目 ⑤b-5（2026-10-04）：年表15・時間の帯15（`tools/axis.py`・門番 `check_axis`）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の AX_*・AXI の項目・TV／TM は18本目の値（19本目の ⑤b-1 で見本 fixture_ep18 へ）。
#   値と頁は ref/ep18/src/ep18_pages.txt で当てた＝門番の側の表（check_axis.REC_AXIS・REC_APPROX・REC_LANE）と照らされる（§5b-88）。
#   🔴 守りの線（映像方針 §2）：記録にある時刻と日付だけ・分の小数は「9時18.1分」・**深さの数を書かない**（c804 の約230メートルは語りと
#      字幕だけ）・原因が未決の事は「仮定／計算」の札・**次のカットの語りにある数と出来事は描かない**（0b-39③＝c501 に 9:40 以降・
#      c512 に 17:30 と翌10:30・c520 に13日・cb03 に1964年2月を出さない）・記録が about の時刻は「ごろ」（approx=True＝門番 REC_APPROX）
#   第4章の「上の段＝水中電話の声／下の段＝監視の記録」は2段の帯 tiers（axis の新しい見え方・PLAN の「上の段・下の段」）
TV, TM = "水中電話の声", "監視の記録"
AX_REL = dict(view="date", span=("2020-07", "2023-09"), ticks=("2021", "2022", "2023"))            # c108・c907 公開の23回
#   ⚠️ 軸の左右の余白＝左の端の点の札を左へ振る（anchor="end"）と、日まである札（「1963年4月10日」＝約400画素）が画面の左へ出る
#      → 軸の範囲を点の前へ広げた（c111・c615・cb03）
AX_INQ = dict(view="date", span=("1963-03-15", "1963-06-25"), ticks=("1963-04", "1963-05", "1963-06"))   # c111 査問会の日程
AX_PSA = dict(view="date", span=("1962-06", "1963-06"), ticks=("1962-07", "1962-10", "1963-01", "1963-04"))  # c205・c211・c216 整備
AX_MORN = dict(view="clock", span=("7:30", "9:30"), ticks=("7:30", "8:00", "8:30", "9:00", "9:30"))     # c309・c312・c320 4月10日の朝
AX_FIVE = dict(view="tiers", span=("9:08", "9:20"), ticks=("9:08", "9:10", "9:12", "9:14", "9:16", "9:18", "9:20"),
               lanes=(TV, TM))                                                                      # 第4章の2段の帯
AX_SKY = dict(view="clock", span=("9:00", "13:00"), ticks=("9:00", "10:00", "11:00", "12:00", "13:00"))  # c501・c504・c507 救難艦
AX_DAY = dict(view="clock", span=("9:00", "21:00"), ticks=("9:00", "12:00", "15:00", "18:00", "21:00"))  # c512 ワシントン
AX_WEEK = dict(view="date", span=("1963-04-09", "1963-04-14"),
               ticks=("1963-04-10", "1963-04-11", "1963-04-12", "1963-04-13"))                       # c520 12日
AX_PRE = dict(view="date", span=("1961-01", "1963-06"), ticks=("1961", "1962", "1963"))               # c604・c606 整備より前
AX_UT = dict(view="date", span=("1962-10", "1963-05"), ticks=("1962-11", "1963-01", "1963-03", "1963-05"))  # c615・c617 検査
AX_APR = dict(view="date", span=("1963-04-01", "1963-04-21"), ticks=("1963-04-01", "1963-04-08", "1963-04-15"))  # c620
AX_AIR = dict(view="sec", span=("-5", "36"), ticks=("0", "10", "20", "30"))                           # c717 別の30秒
AX_CALC = dict(view="clock", span=("9:08", "9:20"), ticks=("9:08", "9:10", "9:12", "9:14", "9:16", "9:18", "9:20"))  # c720・c804
AX_SAFE = dict(view="date", span=("1963-01", "1964-05"), ticks=("1963-04", "1963-07", "1963-10", "1964-01", "1964-04"))  # cb03・cb05
AXI.update({
    # ── 公開の23回（c108・c907）＝台帳（第1〜17回）と公開の棚の日付（第18〜23回＝公開日と書かない）
    "r01": dict(k="pt", at="2020-09-23", fmt="ym", t="第1回", rec="台帳"),
    "r1_17": dict(k="span", a="2020-09-23", b="2022-01-26", t="第1〜17回（第5・6回は別の本）", rec="台帳"),
    "r18_23": dict(k="span", a="2022-03-03", b="2023-05-02", t="第18〜23回（公開の棚の日付）", rec="棚", c="DOC"),
    "r23": dict(k="pt", at="2023-05-02", fmt="ym", t="第23回まで", rec="棚"),
    # ── 査問会の日程（c111）
    "acc": dict(k="pt", at="1963-04-10", t="事故", rec="R08 p4185", c="ALERT", anchor="end"),
    "open": dict(k="pt", at="1963-04-11", t="査問会が開く", rec="IR18 p2067", anchor="start"),
    "close": dict(k="pt", at="1963-06-05", t="閉じる", rec="IR18 p2067"),
    "inq": dict(k="br", a="1963-04-11", b="1963-06-05", rec="IR18 p2067"),
    # ── 9か月の整備（c205・c211・c216）
    "psa0": dict(k="pt", at="1962-07-16", fmt="ym", t="整備の始まり", rec="R08 p4181"),
    "late": dict(k="span", a="1963-01-18", b="1963-04-11", t="予定日が5回延びる", rec="R08 p4196", c="ALERT"),
    "dep": dict(k="pt", at="1963-04-09", t="出港", rec="R08 p4181", anchor="end"),
    # ⚠️ qa_all の echo：「復水器の土台のボルトの緩み」は語りの複写（12字以上で連続一致72%以上）＝言いかえて短く
    "bolt": dict(k="pt", at="1963-01", t="復水器の土台が緩む", rec="R08 p4196", anchor="end"),
    "pump": dict(k="pt", at="1963-03", t="魚雷の排出ポンプのずれ", rec="R08 p4196", anchor="end"),
    "asst": dict(k="pt", at="1962-11", t="担当の補佐", rec="R08 p4203", anchor="end"),
    "supt": dict(k="pt", at="1962-12", t="担当の監督", rec="R08 p4203"),
    "co": dict(k="pt", at="1963-01", t="艦長と副長", rec="R08 p4203", anchor="start"),
    # ── 4月10日の朝（c309・c312・c320）
    "t0745": dict(k="pt", at="7:45", t="待ち合わせ", rec="R08 p4185", anchor="end"),
    "t0900": dict(k="pt", at="9:00", t="海は穏やか", rec="R08 p4185", anchor="end"),
    "t0747": dict(k="pt", at="7:47", t="深い潜航を始める", rec="R08 p4185", anchor="start"),
    "dive": dict(k="span", a="7:47", b="9:09", t="深さを段ごとに増やす", rec=["R08 p4185", "R08 p4212"]),
    "t0909": dict(k="pt", at="9:09", t="試験深度（査問会の見立て）", rec="R08 p4212", anchor="end"),
    "t0910": dict(k="pt", at="9:10", t="針路を変える", rec="R08 p4212", anchor="start", approx=True),
    "t0913": dict(k="pt", at="9:13", t="あの声", rec="R08 p4212", anchor="start"),
    "five": dict(k="br", a="9:13", b="9:18.1", rec="R08 p4185"),
    # ── 第4章の2段の帯（AX_FIVE）。上の段＝水中電話の声（認定16・17・22c）／下の段＝監視の記録（認定18）
    "lv": dict(k="lane", lane=TV, rec="R08 p4185"),
    "lm": dict(k="lane", lane=TM, rec="R08 p4185"),
    # ⚠️ 下見：札「タンクを吹いた音でありうる」を左へ振ると段の名「監視の記録」の真上に来て1つの言葉に読めた＝短く（門番 LANE_COL）
    "blow1": dict(k="span", lane=TM, a="9:09.8", b="9:11.3", t="吹いた音でありうる", rec="R08 p4185", anchor="end"),
    # ⚠️ 試し焼き（Actions 37191779632）：右へ振ると「吹いた音でありうる」と同じ高さで「…ありうる ポンプ」と続けて読めた＝真ん中（上の段へ）
    "cool": dict(k="pt", lane=TM, at="9:11", t="ポンプ", rec="R08 p4185"),
    "v0913": dict(k="pt", lane=TV, at="9:13", t="「軽微な問題」", rec="R08 p4185"),
    "blow2": dict(k="span", lane=TM, a="9:13.5", b="9:14", t="2回目", rec="R08 p4185"),
    "q0915": dict(k="pt", lane=TV, at="9:15", t="問いかけ", rec="R08 p4186", approx=True),
    "g0916": dict(k="pt", lane=TV, at="9:16", t="崩れた声", rec="R08 p4185", approx=True),
    "g0917": dict(k="pt", lane=TV, at="9:17", t="崩れた声", rec="R08 p4185", approx=True, anchor="start"),
    "boom": dict(k="pt", lane=TM, at="9:18.1", t="内破でありうる型の音", rec="R08 p4185", c="ALERT", big=True),
    "five4": dict(k="br", a="9:13", b="9:18.1", t="約5分", rec="R08 p4185"),
    # ── 救難艦の5時間（c501・c504・c507＝AX_SKY）とワシントン（c512＝AX_DAY）
    "s0917": dict(k="pt", at="9:17", t="呼びかけ・捜索", rec="R08 p4187", approx=True, anchor="start"),
    "s0940": dict(k="pt", at="9:40", t="作戦士官が聞く", rec="R08 p4186", approx=True, anchor="start"),
    "s1045": dict(k="pt", at="10:45", t="報告を書き始める", rec="R08 p4186", approx=True),
    "s1245": dict(k="pt", at="12:45", t="陸の無線局が受け取る", rec="R08 p4186"),
    "s1435": dict(k="pt", at="14:35", t="司令官が知る", rec="R08 p4187", anchor="end"),
    "w1540": dict(k="pt", at="15:40", t="海軍作戦部長が知る", rec="D p9001", approx=True, anchor="start"),
    "w2000": dict(k="pt", at="20:00", t="行方不明とみられる（発表）", rec="D p9001", anchor="end"),
    # ── 12日（c520＝AX_WEEK）
    #   日の目盛り（「10日」「11日」）が日付を言う＝点の札は項目名だけ（lab=False＝日まである札は約400画素で隣とぶつかる）
    "d10": dict(k="pt", at="1963-04-10", t="事故", rec="R08 p4185", c="ALERT", anchor="end", lab=False),
    "d11": dict(k="pt", at="1963-04-11", t="捜索の指揮が移る", rec="R08 p4188", lab=False),
    "d12": dict(k="pt", at="1963-04-12", t="副司令官が航海士に会う", rec="R08 p4187", anchor="start", lab=False),
    # ── 整備より前（c606＝AX_PRE）。🔴 c604（6隻の故障）は年表に置けない＝認定111 に日付が無い（「prior to THRESHER's post
    #    shakedown availability」だけ）→ 書類の再現図（認定111）に替えて ⑤b-6 へ（映像方針 §19・ルール §5b-113⑥）
    "pre0": dict(k="pt", at="1962-07-16", fmt="ym", t="整備の始まり", rec="R08 p4181"),
    "trim": dict(k="pt", at="1961-05", t="傾きを整える水の系統", rec="J p8067", c="ALERT"),
    # ── 11月29日と12月4日（c615・c617＝AX_UT）・報告書が届いた日（c620＝AX_APR）
    "u1129": dict(k="pt", at="1962-11-29", t="決めてほしいと求める", rec="R08 p4197", anchor="end"),
    "u1204": dict(k="pt", at="1962-12-04", t="外さないと決める", rec="R08 p4197", anchor="start", c="ALERT"),
    "u_last": dict(k="pt", at="1962-11-29", t="この計画で最後の検査", rec="R08 p4197", anchor="end"),
    "u_none": dict(k="span", a="1962-11-29", b="1963-04-09", t="超音波の検査なし", rec=["R08 p4197", "R08 p4181"], c="ALERT"),
    "u_dep": dict(k="pt", at="1963-04-09", t="出港", rec="R08 p4181", anchor="end"),
    "a10": dict(k="pt", at="1963-04-10", t="艦が失われる", rec="R08 p4185", c="ALERT", anchor="end"),
    # ⚠️ 試し焼き：右へ振ると「1963年4月10日」「1963年4月11日」が同じ高さで1行に読めた＝真ん中（上の段へ）
    "a11": dict(k="pt", at="1963-04-11", t="報告書はこれより後", rec="J p8018"),
    # ── 別の30秒（c717＝AX_AIR・認定51）
    "e0": dict(k="pt", at="0", t="電気が落ちる", rec="R08 p4191", anchor="start", lab=False),   # 「0秒」は目盛りが言う
    "e30": dict(k="pt", at="30", t="開き切る", rec="R08 p4191", anchor="end"),
    "eopen": dict(k="span", a="0", b="30", t="残る1つがゆっくり開く", rec="R08 p4191"),
    "ebr": dict(k="br", a="0", b="30", rec="R08 p4191"),
    # ── もし止まっていたら（c720）・査問会の計算の1つ（c804）＝AX_CALC（1本の時刻の帯）
    # ⚠️ 下見：帯の札「7.1分　ふつうの推進は戻らない」と項目の札「非常用の電動機だけ」が同じ高さで1行に読めた＝帯の札は「7.1分」だけ・
    #   「ふつうの推進は戻らない」は 9:11 の項目の札（1段目）・電動機は2段目・「可能性は高くない」は 9時18.1分の下（離す）
    "h0911": dict(k="pt", at="9:11", t="ポンプが止まった（仮定）", rec="R08 p4212", anchor="end"),
    "h_span": dict(k="span", a="9:11", b="9:18.1", t="7.1分", rec="R08 p4212", c="ALERT"),
    "h0918": dict(k="pt", at="9:18.1", t="押しつぶされる深さ", rec="R08 p4212", anchor="end"),
    "k0909": dict(k="pt", at="9:09", t="試験深度", rec="R08 p4212", anchor="end"),
    "k0913": dict(k="pt", at="9:13", t="あの声", rec="R08 p4212", anchor="start"),
    # ── 安全の計画（cb03・cb05＝AX_SAFE）
    "b0603": dict(k="pt", at="1963-06-03", t="計画を命じる", rec="J p8097", anchor="end"),     # 見出し「安全の計画」と同じ語にしない（dup）
    # ⚠️ 下見：右へ振ると「安全の計画を命じる」「指示書」が同じ段で1つの言葉に読めた＝真ん中（上の段へ上がる）
    "b07": dict(k="pt", at="1963-07-08", fmt="ym", t="指示書", rec="J p8098"),
    "b6402": dict(k="pt", at="1964-02-18", fmt="ym", t="潜水艦安全センター", rec="J p8094"),
})


# ══════════════════════════════════════════════════════════
#  16本目 ⑤b-5（2026-10-01）：場面1 水位と斜面の速さの線（`tools/lv16.py`・門番 check_mech の judge_lv）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-04（18本目 ⑤b-1・§0b）：16本目の線の図の表（LV_T・LV_NOTE・LV_ALL・LV_63・VR_LO・VR_HI・LVP・LV_BRK・LV_REF・LV_REL・LV_EV・
#    LV_BAND）と関数（`lvp()`・`lv_upto()`・`_rk()`・`lv_fig()`）は `tools/fixture_ep16.py` へ移した（値は1つも変えていない＝
#    git の `b044b56`）。型の道具 `tools/lv16.py`（fig=("lv", …)）はファイルとして残す＝使う回は点の表をここに足す
#    （門番 check_mech の REC_LV＊も回の値を門番の側に別に持つ＝§5b-88）


# ══════════════════════════════════════════════════════════
#  14本目 ⑤b-4（2026-09-29）：断面F（`tools/hull.py`）と地図（drift）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の MAP_* ・HULL_NOTE・`sewol_map()` はこの回の地図と資料。
#    画面の出典は `src()`（台本の頁「海審 p1016」→ 画面の頁「…PDF 16頁」＝門番 check_wording の I が通し番号を止める）
def src(recs):
    """出典の行（「出典：」を除く）。recs＝「海審 p1016・p1017」のような台本の頁の書き方（文字列か list）。"""
    import illu
    return illu.rec_line(recs if isinstance(recs, (list, tuple)) else [recs]).replace("出典：", "", 1)


# 🔴 2026-09-30（15本目 ⑤b-1）：14本目の注（HULL_NOTE）・地図の点（MAP_*・ROUTE）・地図の関数 `sewol_map()`・2つの問いを
#    戻す型（`q_pair()`・Q1_TILT・Q2_BOARD）は `tools/fixture_ep14.py` へ移した（値は1つも変えていない）。
#    15本目の3つの問い（c109）は案C の A・B・D を小さく戻す＝⑤b-2（14本目の q_pair の型を回の関数で）


# ══════════════════════════════════════════════════════════
#  地図（drift）の段の部品をつなぐ道具（`merge`＝回をまたいで同じ）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-01（16本目 ⑤b-1・§0b）：15本目の地図（5つの範囲＝RAMP・FIELD・TOWN・FLA・USA の表と、その関数 `ramp_map()`・
#    `field_map()`・`town_map()`・`fla_map()`・`usa_map()`・空港の点の照合 RENO_REL ほか）は `tools/fixture_ep15.py` へ移した
#    （値は1つも変えていない＝git の `c646174`）。
#    🔴 2026-10-04（18本目 ⑤b-1）：16本目は地図（drift）を使わなかった（案C の VA〜VD と図解に替えた）＝地図の表は無く、
#    `titan_fig.GEO` に16本目の地点も無い（fixture_ep16 の GEO は空）。18本目の地図は ⑤b で、回の表（`*_VIEW`・`*_PTS`・`*_REL`）と
#    関数をここに足す。地点は `titan_fig.GEO`（Wikidata・回の頭の鍵）と報告書の値だけ。
#    ⚠️ 地図の教訓（線の長さと東西の並びは模式・距離の札は語りと同じ「約228メートル」の形ほか）は移した注の側にある
#       ＝fixture_ep15 の地図の節の上
_LISTS = ("route", "tag", "dim", "move", "circle", "arrow")


def _as_list(x):
    return [] if not x else (list(x) if isinstance(x, list) else [x])


def merge(*parts):
    """段の部品を1つの段にまとめる（route・tag・dim・move・circle・arrow は list をつなぐ）。"""
    out = {}
    for p in parts:
        for k, v in p.items():
            out[k] = _as_list(out.get(k)) + _as_list(v) if k in _LISTS else v
    return out


# ══════════════════════════════════════════════════════════
#  14本目 ⑤b-6（2026-09-29）：量の型（`tools/qty.py`・門番 check_qty）と箱の型（`tools/boxes.py`・門番 check_boxes）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB・PEOPLE_*・CT・CTP・RUD・FORM_PRE・CAUSE はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_*／check_boxes.REC_*＝§5b-88）＝回を替えたら両方を替える。
#    🔴 2026-09-30（15本目 ⑤b-1）：14本目の値は `tools/fixture_ep14.py` へ移した＝ここも門番の表も空。
#    🔴 2026-10-01（16本目 ⑤b-1）：15本目の値（棒＝QG・QB の速さ・時間・G ほか／箱の型の表＝鎖・答え・実況・成績・書類の再現図）は
#       `tools/fixture_ep15.py` へ移した（値は1つも変えていない＝git の `c646174`）＝ここも門番の表も空。
#    🔴 2026-10-04（18本目 ⑤b-1）：16本目の値（棒＝QG・QB のダムの高さ・量・波・動いた距離・犠牲者・刑ほか／箱の型の表＝流れ図 FL_*・FLP・
#       書類の再現図 FORM_*・並べ図 CAUSE）は `tools/fixture_ep16.py` へ移した（値は1つも変えていない＝git の `b044b56`）＝ここも
#       門番の表も空。18本目の棒と箱は ⑤b で、回の値と頁を ref/ep18/src/ep18_pages.txt に当てて入れる
# 棒の群（尺は 0 から・項目名に単位）。数字は棒に書かない（§5b-9＝数は字幕）
# 🆕 2026-10-04（18本目 ⑤b-6a）：第1〜6章の棒（c204・c207・c302・c315・c613・c614・c626）。値と頁は ref/ep18/src/ep18_pages.txt で
#   当てた＝門番 check_qty.REC_QTY と照らす（門番の側にも別に持つ＝§5b-88）。
#   ・フィートの記録は**メートルに直した長さ**で描く（×0.3048＝台本 §9-1。語りは「約」で丸める・棒は丸めない）
#   ・「〜を超える」（10万人日・3,000）は棒をその数まで＝注で「記録は〜を超える」と断る
#   ・🔴 測り方の違う割合は群を分ける（ルール §5b-114③・台本 §1-5）＝不合格（査問会 13.8%・委員会の数字 14%＝J p.14 の「145本の
#     検査で基準を下回った14%」）と、修理か交換を要した割合（中将 約10%）を同じ群に入れない
#   ・c302 の内わけは名簿（認定4＝R08 p.181〜184）の身分の欄を機械で数えた（艦の乗員108＝USS THRESHER の行・造船所の士官3＝USN と
#     PORTSMOUTH NAVAL SHIPYARD・造船所の職員13＝Civilian Employee・請け負った会社4＝Contractor's Representative・司令部の士官1＝STAFF）
#   ・c603（数の比べ）は棒1本しか無い＝認定112 の書類の再現図に替えた（映像方針 §20）
QG = {
    "work": dict(id="work", t="仕事の量（万人日）", ticks=(0, 2, 4, 6, 8, 10, 12), rows=("見込み", "実際")),
    "dist": dict(id="dist", t="艦からの距離（メートル）", ticks=(0, 100, 200, 300, 400), rows=("いちばん遠い", "いちばん近い")),
    # ⚠️ c302 は群2つ＝行が5つまで（6行だと図の高さ 682画素を越えて注に重なる＝qty._bar の行の高さの下限 48）。「全体129」は棒にしない
    #   （108と21の和）・内わけは語りの3つの言い方（造船所の士官と職員・請け負った会社の担当者・司令部の士官）
    "aboard": dict(id="aboard", t="乗っていた人（人）", ticks=(0, 30, 60, 90, 120), rows=("艦の乗員", "ほかに乗った人")),
    "others": dict(id="others", t="ほかに乗った人の内わけ（人）", ticks=(0, 5, 10, 15, 20),
                   rows=("造船所の士官と職員", "請け負った会社", "司令部の士官")),
    "depth": dict(id="depth", t="深さ（メートル）", ticks=(0, 500, 1000, 1500, 2000, 2500, 3000), rows=("救難室の限界", "海の深さ")),
    "tested": dict(id="tested", t="調べた古い継手（本）", ticks=(0, 50, 100, 150)),
    "rej": dict(id="rej", t="不合格の割合（パーセント）", ticks=(0, 20, 40, 60, 80, 100)),
    "joints": dict(id="joints", t="銀ろう付けの継手（本）", ticks=(0, 500, 1000, 1500, 2000, 2500, 3000),
                   rows=("調べた古い継手", "同じ型の艦の全体")),
    "rej15": dict(id="rej", t="不合格の割合（パーセント）", ticks=(0, 5, 10, 15), rows=("査問会", "委員会の数字")),
    "fix15": dict(id="fix", t="修理か交換を要した割合（パーセント）", ticks=(0, 5, 10, 15)),
}
QB = {
    # c204：認定92（R08 p.195）「an estimate of approximately 35,000 man-days」・認定95（p.196）「The total of man-days expended was over 100,000」
    "w_est": dict(k="bar", g="work", t="見込み", v=3.5, rec="R08 p4195"),
    "w_act": dict(k="bar", g="work", t="実際", v=10, rec="R08 p4196", c="AMBER"),
    # c207：認定80（R08 p.194）「ten thousand pound charges at ranges varying from 1180 feet to 370 feet」
    "d_far": dict(k="bar", g="dist", t="いちばん遠い", v=1180 * 0.3048, rec="R08 p4194"),
    "d_near": dict(k="bar", g="dist", t="いちばん近い", v=370 * 0.3048, rec="R08 p4194", c="AMBER"),
    # c302：認定4（名簿 R08 p.181〜184＝頁ごとに数えた：艦の乗員 p.181〜183・司令部の士官 p.181・造船所の士官 p.183・造船所の職員
    #   p.183〜184・請け負った会社 p.184）
    "a_crew": dict(k="bar", g="aboard", t="艦の乗員", v=108, rec=["R08 p4181", "R08 p4182", "R08 p4183"]),
    "a_oth": dict(k="bar", g="aboard", t="ほかに乗った人", v=21, rec=["R08 p4181", "R08 p4183", "R08 p4184"], c="AMBER"),
    # 造船所の士官3（USN・PORTSMOUTH NAVAL SHIPYARD＝p.183）＋造船所の職員13（Civilian Employee＝p.183〜184）＝16
    "o_yard": dict(k="bar", g="others", t="造船所の士官と職員", v=16, rec=["R08 p4183", "R08 p4184"], c="AMBER"),
    "o_ct": dict(k="bar", g="others", t="請け負った会社", v=4, rec="R08 p4184", c="DOC"),
    "o_st": dict(k="bar", g="others", t="司令部の士官", v=1, rec="R08 p4181", c="INST"),
    # c315：認定13・14（V1 p.38＝見える頁）「a rescue chamber with a maximum depth capability of 850 feet」「Depth of water in this area
    #   is about 8500 feet」（R08 p.185 は 850 が塗られている＝V1 p.38）
    "dp_ch": dict(k="bar", g="depth", t="救難室の限界", v=850 * 0.3048, rec="V1 p38", c="AMBER"),
    "dp_sea": dict(k="bar", g="depth", t="海の深さ", v=8500 * 0.3048, rec="V1 p38"),
    # c613・c614：認定102（R08 p.197）「by 29 November 1962, 145 old joints had been ultrasonically tested … with a rejection rate of 13.8
    #   per cent」・認定112（p.198）「over 3000 of 2-inch size and above in hazardous systems」
    "t_145": dict(k="bar", g="tested", t="11月29日", v=145, rec="R08 p4197"),
    "r_138": dict(k="bar", g="rej", t="不合格", v=13.8, rec="R08 p4197", c="AMBER"),
    "j_145": dict(k="bar", g="joints", t="調べた古い継手", v=145, rec="R08 p4197", c="AMBER"),
    "j_3000": dict(k="bar", g="joints", t="同じ型の艦の全体", v=3000, rec="R08 p4198"),
    # c626：J p.68「Representative Holifield. Our figure on this is 14 percent.」・J p.14（委員長「14 percent below standard on the
    #   examination that was made of the 145 joints」）・J p.68（中将「about 10 percent of those checked required repair or replacement」）
    "q_court": dict(k="bar", g="rej", t="査問会", v=13.8, rec="R08 p4197"),
    "q_jcae": dict(k="bar", g="rej", t="委員会の数字", v=14, rec=["J p8068", "J p8014"], c="AMBER"),
    "q_rick": dict(k="bar", g="fix", t="中将", v=10, rec="J p8068", c="INST"),
}


def qb(name, **kw):
    return dict(QB[name], **kw)


# 人の形（1つ＝1人）＝**14本目 c204〜c206 だけの例外**（ルール §C-1 #59・亡くなった方の数には使わない）。
#   15本目は使わない＝空のまま（門番 check_qty が PEOPLE_CUTS の外の人の形を止める）
PEOPLE_ORDER = ()
PEOPLE_SETS = {}
PEOPLE_REC = {}
PEOPLE_CUTS = ()     # 🔴 門番 check_qty がこの外の人の形を止める（亡くなった方の数に使わない）


def pp(who, c, parent=None):
    """人の形の部品（who の形を c の色に灯して凡例に1行）。"""
    return dict(k="lit", who=who, c=c, rec=PEOPLE_REC[who], **({"parent": parent} if parent else {}))


# 流れ図（14本目＝裁判の流れ図・第11章）。🔴 役職名だけ・名前を出さない・人の形を使わない・赤を使わない
#   🔴 2026-09-30（15本目 ⑤b-1）：14本目の CT・CTP・CREW15 は `tools/fixture_ep14.py` へ。15本目は流れ図を作らない
#   （映像方針 §11-3＝新しい型は作らない）＝空のまま。使う回は `layout=` に回の表を渡す（`tools/boxes.py` の説明）
CT = {}
CTP = {}


def ct(name, **kw):
    return dict(CTP[name], **kw)


def ce(fr, to, **kw):
    """流れ図の矢印（fr・to は部品の id か id の list）。"""
    return dict(k="edge", fr=fr, to=to, **kw)


# 仕組みの模式図の箱（14本目＝舵を動かす仕組み cc05・cc12）＝空。15本目の尾翼の板の模式図は ⑤b-3（映像方針 §4）
RUD = {}
RUDP = {}


def rud(name, **kw):
    return dict(RUDP[name], **kw)


# 書類の再現図（14本目＝c208 の出港前安全点検報告書＝fixture_ep14.FORM_PRE）。🔴 欄の名は報告書の文にあるものだけ・
#   欄に値を書かない（記録に無い値を作らない）・「再現」の札。15本目＝記録簿・参加書類・検査の用紙（c415・c524・c617・c621・
#   c704・c705・c905）＝⑤b で `FORM_<名> = dict(title, rec, fields, ends)` を回の名で足す（`form=` に渡す）
#   🔴 2026-10-04（18本目 ⑤b-1）：16本目の書類の再現図10枚（FORM_MUELLER ほか＝欄の値は原文のイタリア語）は `tools/fixture_ep16.py`
# 🆕 2026-10-04（18本目 ⑤b-6a）：第1〜6章の書類の再現図19枚。🔴 欄の値は**原文の英語のまま**（日本語は字幕だけ＝ルール 0b-33）・
#   欄の名は原文の文の言葉を日本語に・紙1枚に欄は4つまで（§5b-114⑤）。値は ref/ep18/src/ep18_pages.txt の文字の層で当て、文字の層が
#   崩れた5か所（認定111 の艦名・認定24 の電文・V1 p.140・X p.122・p.124）は頁の画像を原寸で切り出して読んだ（2026-10-04）。
#   🔴 査問会の「0913R」の書き方は画面に出さない（台本 §1-7）＝時刻は欄の名へ「9:13 の声」「9:17 から」と移し、値から外した。
#   🔴 次のカットの語りにある事は書かない（ルール 0b-40⑤）：c209 の「見つかり続けた」（c210）・c213 の「承認せず」（c214）・c217 の
#   「整備中に動かすのは好まない」（語りに無い）・c416 の「くぐもった、鈍い音」（c417）・c604 のスケートの括弧（c605）
_P4 = (100, 1820, 270, 840)    # 欄4つの紙（図の本体 210〜892 の内・「再現」の札は 214〜258）
_P3 = (100, 1820, 300, 760)
_P2 = (100, 1820, 330, 690)
# c112：査問会の結論の3つの部分（R08 p.181「FINDINGS OF FACT」・p.204「OPINIONS」・p.217「RECOMMENDATIONS」）＝紙3枚を並べる
FORM_COURT3 = [dict(title="認定", rec="R08 p4181", fields=[dict(t="見出し", v="FINDINGS OF FACT", rec="R08 p4181")], lw=110),
               dict(title="意見", rec="R08 p4204", fields=[dict(t="見出し", v="OPINIONS", rec="R08 p4204")], lw=110),
               dict(title="勧告", rec="R08 p4217", fields=[dict(t="見出し", v="RECOMMENDATIONS", rec="R08 p4217")], lw=110)]
# c209：認定96（R08 p.196）「intensively investigated by ship's force, Bureau of Ships, and Shipyard personnel」・認定86（p.195）
#   「damaged items were scheduled for repair during the post shakedown availability」
FORM_SHOCK = dict(title="衝撃試験の損傷（認定96・86）", rec=["R08 p4196", "R08 p4195"], paper=_P3, lw=190,
                  fields=[dict(t="調べた人", v="ship's force, Bureau of Ships, and Shipyard personnel", rec="R08 p4196"),
                          dict(t="調べ方", v="intensively investigated", rec="R08 p4196", late=True),
                          dict(t="直す予定", v="scheduled for repair during the post shakedown availability", rec="R08 p4195",
                               late=True)])
# c213：認定69（R08 p.193）「prepared by an outside firm under subcontract … used an SS(N) 588 Class Ship Information Book as a guide and
#   virtually copied large portions of it, although many systems on THRESHER were quite different」
FORM_SIB = dict(title="取扱説明書（認定69）", rec="R08 p4193", paper=_P4, lw=160,
                fields=[dict(t="作った所", v="an outside firm under subcontract", rec="R08 p4193"),
                        dict(t="手本", v="an SS(N) 588 Class Ship Information Book as a guide", rec="R08 p4193"),
                        dict(t="写し方", v="virtually copied large portions of it", rec="R08 p4193", late=True),
                        dict(t="違い", v="many systems on THRESHER were quite different", rec="R08 p4193", late=True)])
# c217：人事局長の証言（R08 p.107＝1963年5月21日・非公開の場）「The basic consideration was the pressure placed on the Bureau of Naval
#   Personnel to furnish experienced commanding officers for the POLARIS submarines」
FORM_SMED = dict(title="人事局長の証言（1963年5月21日）", rec="R08 p4107", paper=_P2, lw=200,
                 fields=[dict(t="理由", v="The basic consideration was the pressure", rec="R08 p4107"),
                         dict(t="何の圧力", v="to furnish experienced commanding officers for the POLARIS submarines", rec="R08 p4107",
                              late=True)])
# c219：部隊の司令の証言（R08 p.77）「I advised him that he must resist that pressure」「he would resist it」「there were some hot words
#   exchanged between the boat officer and the Ship Superintendent」「That was the only incident I know of.」
FORM_ANDR = dict(title="部隊の司令の証言（査問会）", rec="R08 p4077", paper=_P4, lw=170,
                 fields=[dict(t="助言", v="he must resist that pressure", rec="R08 p4077", late=True),
                         dict(t="答え", v="he would resist it", rec="R08 p4077", late=True),
                         dict(t="挙げた例", v="some hot words exchanged between the boat officer and the Ship Superintendent",
                              rec="R08 p4077", late=True),
                         dict(t="ほかに", v="That was the only incident I know of.", rec="R08 p4077", late=True)])
# c305：認定8（R08 p.184）「THRESHER's movement orders were CONFIDENTIAL; SKYLARK's were unclassified. Sea trial agenda … were
#   unclassified and were not held by SKYLARK.」
FORM_ORD = dict(title="2隻の命令（認定8）", rec="R08 p4184", paper=_P3, lw=230,
                fields=[dict(t="スレッシャー", v="THRESHER's movement orders were CONFIDENTIAL", rec="R08 p4184"),
                        dict(t="スカイラーク", v="SKYLARK's were unclassified", rec="R08 p4184"),
                        dict(t="予定表", v="were not held by SKYLARK", rec="R08 p4184", late=True)])
# c416：航海士の証言（V1 p.118＝記録の45頁）「I had heard a lot of ships breaking up during World War II after having been torpedoed at
#   depths. It sounded as though there was a compartment collapsing」
FORM_WATSON = dict(title="航海士の証言（査問会の記録）", rec="V1 p118", paper=_P3, lw=230,
                   fields=[dict(t="前に聞いた音", v="a lot of ships breaking up during World War II", rec="V1 p118"),
                           dict(t="どんな船", v="after having been torpedoed at depths", rec="V1 p118"),
                           dict(t="似ていた音", v="a compartment collapsing", rec="V1 p118", late=True)])
# c418：証言の割れ（V1 p.132＝甲板の当直の下士官〈水中電話の係・p.127〉「air rushing into his tanks for about four to five seconds」／
#   V1 p.140＝記録簿の係の無線員〈p.136〉への問い「like air being blown into a tank」と答え「No, sir, I don't think so.」＝頁の画像で読んだ）
FORM_SPLIT = dict(title="スカイラークの乗員の証言", rec=["V1 p132", "V1 p140"], paper=_P3, lw=230,
                  fields=[dict(t="当直の下士官", v="air rushing into his tanks for about four to five seconds", rec="V1 p132", late=True),
                          dict(t="問い", v="like air being blown into a tank", rec="V1 p140", late=True),
                          dict(t="記録簿の係", v="No, sir, I don't think so.", rec="V1 p140", late=True)])
# c509：認定24（R08 p.186＝頁の画像で読んだ）"UNABLE TO COMMUNICATE WITH THRESHER SINCE 0917R. … LAST TRANSMISSION RECD WAS GARBLED.
#   INDICATED THRESHER WAS APPROACHING TEST DEPTH. MY PRESENT POSITION … CONDUCTING EXPANDING SEARCH."
FORM_MSG = dict(title="スカイラークの電文（認定24）", rec="R08 p4186", paper=_P4, lw=200,
                fields=[dict(t="9:17 から", v="UNABLE TO COMMUNICATE WITH THRESHER", rec="R08 p4186"),
                        dict(t="最後の交信", v="LAST TRANSMISSION RECD WAS GARBLED", rec="R08 p4186"),
                        dict(t="示したこと", v="INDICATED THRESHER WAS APPROACHING TEST DEPTH", rec="R08 p4186", late=True),
                        dict(t="いま", v="CONDUCTING EXPANDING SEARCH", rec="R08 p4186", late=True)])
# c510：認定25（R08 p.186〜187）「Although inclusion of additional information such as the 0913R UQC transmission "Experiencing minor
#   difficulty..." etc., was suggested by the Operations Officer, the Commanding Officer decided not to include such information.」・
#   「SKYLARK did not include such additional information in any subsequent reports.」
FORM_F25 = dict(title="査問会の認定25", rec=["R08 p4186", "R08 p4187"], paper=_P4, lw=170,
                fields=[dict(t="9:13 の声", v="Experiencing minor difficulty", rec="R08 p4186"),
                        dict(t="勧めた人", v="suggested by the Operations Officer", rec="R08 p4186", late=True),
                        dict(t="艦長", v="the Commanding Officer decided not to include such information", rec="R08 p4186",
                             late=True),
                        dict(t="その後", v="did not include such additional information in any subsequent reports", rec="R08 p4187",
                             late=True)])
# c517：シーウルフの報告（証拠49＝X p.122・p.124＝頁の画像で読んだ）「We hear what may be interrupted keying now」（11日 12時19分）・
#   「May hear very weak voice on 8KC over RYCOM. … Unreadable.」（14時33分）
FORM_SEAWOLF = dict(title="シーウルフの報告（証拠49）", rec=["X p1122", "X p1124"], paper=_P2, lw=120,
                    fields=[dict(t="合図", v="what may be interrupted keying", rec="X p1122"),
                            dict(t="声", v="May hear very weak voice", rec="X p1124", late=True)])
# c522：意見48（R08 p.214）「the Commanding Officer, SKYLARK, failed fully to inform higher authority … for an unreasonable length of
#   time; but that this could not conceivably have contributed in any way to the loss of THRESHER」
FORM_O48 = dict(title="査問会の意見48", rec="R08 p4214", paper=_P3, lw=280,
                fields=[dict(t="伝えなかったこと", v="failed fully to inform higher authority", rec="R08 p4214", late=True),
                        dict(t="どのくらい", v="for an unreasonable length of time", rec="R08 p4214", late=True),
                        dict(t="関わり", v="could not conceivably have contributed in any way to the loss of THRESHER",
                             rec="R08 p4214", late=True)])
# c603（数の比べ → 書類の再現図＝映像方針 §20）：認定112（R08 p.198）「the approximate number of sil-braze joints in an S5W reactor
#   equipped ship is over 3000 of 2-inch size and above in hazardous systems」
FORM_F112 = dict(title="査問会の認定112", rec="R08 p4198", paper=_P4, lw=140,
                 fields=[dict(t="どの艦", v="an S5W reactor equipped ship", rec="R08 p4198"),
                         dict(t="系統", v="in hazardous systems", rec="R08 p4198"),
                         dict(t="大きさ", v="of 2-inch size and above", rec="R08 p4198", late=True),
                         dict(t="数", v="over 3000", rec="R08 p4198", late=True)])
# c604（年表 → 書類の再現図＝⑤b-5・映像方針 §19）：認定111（R08 p.198＝頁の画像で艦名を読んだ）「prior to THRESHER's post shakedown
#   availability, there had been reports of serious failures of sil-braze joints in BARBEL, SKATE, SNOOK, SCULPIN, ETHAN ALLEN and THRESHER」
FORM_F111 = dict(title="査問会の認定111", rec="R08 p4198", paper=_P3, lw=140,
                 fields=[dict(t="いつ", v="prior to THRESHER's post shakedown availability", rec="R08 p4198", late=True),
                         dict(t="どの艦", v="BARBEL, SKATE, SNOOK, SCULPIN, ETHAN ALLEN and THRESHER", rec="R08 p4198", late=True),
                         dict(t="何が", v="reports of serious failures of sil-braze joints", rec="R08 p4198", late=True)])
# c605：紙2枚＝認定111 の括弧（R08 p.198）「The SKATE casualty occurred on a polar cruise at 600 feet under the ice when a 3-inch sil-braze
#   joint parted」／大西洋艦隊の司令官の意見書（IR18 p.123）「The failure of the sil-braze joint in SKATE did not occur under the ice but
#   in open water」。🔴 深さ（600・570フィート）は語りに無い＝書かない
FORM_F111S = dict(title="査問会の認定111", rec="R08 p4198", lw=150,
                  fields=[dict(t="スケート", v="a 3-inch sil-braze joint parted", rec="R08 p4198", late=True),
                          dict(t="場所", v="under the ice", rec="R08 p4198", late=True)])
FORM_CINC = dict(title="艦隊司令官の意見書", rec="IR18 p2123", lw=110,
                 fields=[dict(t="訂正", v="did not occur under the ice", rec="IR18 p2123"),
                         dict(t="場所", v="in open water", rec="IR18 p2123")])
# c609：艦船局の手紙（認定98＝R08 p.196 が引く・1962年8月28日・証拠115）「employ a minimum of at least one ultrasonic test team throughout
#   the entire assigned post shakedown availability to examine, insofar as possible, the maximum number of sil-braze joints」
FORM_BUSHIPS = dict(title="艦船局の手紙（1962年8月28日）", rec="R08 p4196", paper=_P3, lw=160,
                    fields=[dict(t="何を", v="employ a minimum of at least one ultrasonic test team", rec="R08 p4196", late=True),
                            dict(t="いつまで", v="throughout the entire assigned post shakedown availability", rec="R08 p4196",
                                 late=True),
                            dict(t="どれだけ", v="the maximum number of sil-braze joints", rec="R08 p4196", late=True)])
# c610：認定99（R08 p.196）「job orders … called for use of one ultrasonic test team, to test first those joints not lagged, and provided
#   that if time permitted thereafter, lagging would be removed to permit tests of additional joints」
FORM_JOB = dict(title="作業の指示書（認定99）", rec="R08 p4196", paper=_P3, lw=230,
                fields=[dict(t="班", v="use of one ultrasonic test team", rec="R08 p4196"),
                        dict(t="先に", v="to test first those joints not lagged", rec="R08 p4196", late=True),
                        dict(t="時間があれば", v="lagging would be removed to permit tests of additional joints", rec="R08 p4196",
                             late=True)])
# c622：意見21（R08 p.207）「the management of the Portsmouth Naval Shipyard did not exercise good judgment in determining not to unlag
#   pipes」
FORM_O21 = dict(title="査問会の意見21", rec="R08 p4207", paper=_P3, lw=120,
                fields=[dict(t="誰が", v="the management of the Portsmouth Naval Shipyard", rec="R08 p4207"),
                        dict(t="何を", v="determining not to unlag pipes", rec="R08 p4207"),
                        dict(t="判断", v="did not exercise good judgment", rec="R08 p4207", late=True)])
# c624：原子炉の責任者の査問会での証言（1963年4月29日・非公開の場＝J p.67 が議会で読み上げた形・p.68）「about 5 percent of her
#   silver-brazed joints were ultrasonically inspected」「about 10 percent of those checked required repair or replacement」
FORM_RICK = dict(title="原子炉の責任者の証言（1963年4月29日）", rec=["J p8067", "J p8068"], paper=_P2, lw=170,
                 fields=[dict(t="調べた分", v="about 5 percent of her silver-brazed joints were ultrasonically inspected", rec="J p8068",
                              late=True),
                         dict(t="その結果", v="about 10 percent of those checked required repair or replacement", rec="J p8068",
                              late=True)])

# 🆕 2026-10-04（18本目 ⑤b-6b）：第7〜11章の書類の再現図37枚（紙1枚36・紙2枚1＝c919）。欄の値は**原文の英語のまま**・頁は
#   ref/ep18/src/ep18_pages.txt の文字の層で当て、崩れた所（認定48・IR18 p.6 の行の順・J p.32「Deptli」）と塗りの札の形は頁の画像を
#   原寸で切り出して読んだ（2026-10-04）。🔴 **この記録の塗りは白く抜いて赤い字で記号**（「b(1)」「(b) (1)」「b(3) 10 USC 130」
#   「(b) (6)」）＝値に頁に見えるとおりの記号を書く（黒い帯は描かない）。公聴会の本（1965年刊）の削除は「[classified matter deleted]」
#   と刷られている＝そのまま。🔴 次のカットの語りにある事は書かない（0b-40⑤）：c706 の除湿器（c707）・c711 の「一度も無い」（c712）・
#   c801 の4つの中身（c802・c803）・c809 の「推測が事実として通る」（c810）・c813 の「原因は決められていない」（c812）・c912 の原告の言葉
#   （c913）・c915 の計算の中身（c916）・cb16 の「怠慢には帰せられない」（cb17）・cb18 の「すべてを調べ直した」（cb19）
_P1 = (100, 1820, 360, 660)
# c703（数の比べ → 書類の再現図＝⑤b-6b・映像方針 §21）：認定46（R08 p.190）「as compared to the SKIPJACK, the immediately preceding class
#   of attack submarine, THRESHER had: a. An increase in test depth from 700 feet to b(1) … c. About the same high pressure air bank
#   capacity.」（「b(1)」は頁の画像の塗りの札）。スレッシャーの深さは塗られている＝棒にできない（棒1本）
FORM_F46A = dict(title="査問会の認定46", rec="R08 p4190", paper=_P3, lw=160,
                 fields=[dict(t="比べた艦", v="as compared to the SKIPJACK", rec="R08 p4190"),
                         dict(t="試験深度", v="An increase in test depth from 700 feet to b(1)", rec="R08 p4190", late=True),
                         dict(t="空気", v="About the same high pressure air bank capacity.", rec="R08 p4190", late=True)])
# c704：認定46 d（R08 p.190）「d. While at test depth: (1) A reduction in the amount of ballast which could be blown from (b) (1) per cent
#   to (b) (1) per cent. (2) A reduction in the rate of blowing ballast from …」。数（d(1) の塗りの札）は2行目「塗られている」で
FORM_F46D = dict(title="査問会の認定46", rec="R08 p4190", paper=_P4, lw=190,
                 fields=[dict(t="いつ", v="While at test depth:", rec="R08 p4190"),
                         dict(t="吹き出せる量", v="A reduction in the amount of ballast which could be blown", rec="R08 p4190", late=True),
                         dict(t="その数", v="from (b) (1) per cent to (b) (1) per cent", rec="R08 p4190", late=True),
                         dict(t="速さ", v="A reduction in the rate of blowing ballast", rec="R08 p4190", late=True)])
# c706：認定48（R08 p.190＝文字の層が崩れている「a4r」「blovw」ほか＝頁の画像で読んだ）。除湿器（Dehydrators were not installed）は
#   次の c707 の語り＝書かない
FORM_F48 = dict(title="艦船局の設計の基準（認定48）", rec="R08 p4190", paper=_P3, lw=150,
                fields=[dict(t="基準", v="capability to blow all main ballast tanks twice at periscope depth", rec="R08 p4190",
                             late=True),
                        dict(t="深さ", v="There is no modification to this criteria for depth of blowing", rec="R08 p4190", late=True),
                        dict(t="氷", v="There are no requirements … which would prevent the formation of blockages due to ice",
                             rec="R08 p4190", late=True)])
# c708：艦船局の長の証言（J p.32＝1963年6月27日・文字の層「Deptli」は頁の画像で Depth）・J p.35（同じ日）「It is a matter of pressure
#   differential.」
FORM_BROCK = dict(title="艦船局の長の証言（議会・1963年6月27日）", rec=["J p8032", "J p8035"], paper=_P2, lw=130,
                  fields=[dict(t="深さ", v="Depth is not significant insofar as freezeup is concerned.", rec="J p8032", late=True),
                          dict(t="決め手", v="It is a matter of pressure differential.", rec="J p8035", late=True)])
# c710：最初の試運転の前夜（R08 p.26＝大佐の証言・その場にいた〈and myself〉）。ポンプは「in high」（語りの「速い回し方」）
FORM_ZUR = dict(title="大佐の証言（査問会）", rec="R08 p4026", paper=_P3, lw=230,
                fields=[dict(t="話したこと", v="what would happen if we flooded any one area", rec="R08 p4026", late=True),
                        dict(t="ポンプの回し方", v="we were all for having them in high", rec="R08 p4026", late=True),
                        dict(t="理由", v="air was very questionable and how much good it would do at that depth", rec="R08 p4026",
                             late=True)])
# c711：元設計部長の証言（R08 p.33）。「一度も行われていない」は次の c712（J p.38）＝書かない
FORM_JACK = dict(title="元設計部長の証言（査問会）", rec="R08 p4033", paper=_P4, lw=190,
                 fields=[dict(t="話し合い", v="whether or not we should attempt to blow the main ballast tanks at deep depths",
                              rec="R08 p4033", late=True),
                         dict(t="決まったこと", v="it was decided that this would not be prudent", rec="R08 p4033", late=True),
                         dict(t="空気", v="the air would expand", rec="R08 p4033", late=True),
                         dict(t="おそれ", v="we might make an uncontrolled ascent", rec="R08 p4033", late=True)])
# c713：J p.83（1963年7月23日）「the Navy from the time of the 400-foot submarine [classified material deleted] did not basically change
#   the blowing requirements as they went deeper.」・議員「That doesn't seem right to me.」・中将「This isn't right.」
FORM_RICK83 = dict(title="原子炉の責任者の証言（議会・1963年7月23日）", rec="J p8083", paper=_P4, lw=150,
                   fields=[dict(t="いつから", v="from the time of the 400-foot submarine", rec="J p8083", late=True),
                           dict(t="決まり", v="did not basically change the blowing requirements as they went deeper", rec="J p8083",
                                late=True),
                           dict(t="議員", v="That doesn't seem right to me.", rec="J p8083", late=True),
                           dict(t="中将", v="This isn't right.", rec="J p8083", late=True)])
# c718：意見38k（R08 p.211）。「電気が切れると閉まる」は認定51（p.191）の設計＝fail-closed の語で
FORM_O38 = dict(title="査問会の意見38", rec="R08 p4211", paper=_P3, lw=170,
                fields=[dict(t="考え方", v="The fail-closed concept for the three air banks", rec="R08 p4211", late=True),
                        dict(t="試験深度で", v="is not desirable for safety of the ship at test depth", rec="R08 p4211", late=True),
                        dict(t="改め方", v="should be modified to provide fail-on-the-line; i.e., air bank valves open.", rec="R08 p4211",
                             late=True)])
# c723：意見39（R08 p.211）
FORM_O39 = dict(title="査問会の意見39", rec="R08 p4211", paper=_P2, lw=170,
                fields=[dict(t="何を", v="the high pressure blow of submarine main ballast tanks", rec="R08 p4211", late=True),
                        dict(t="どう試すか", v="tested under conditions simulating a full blow at test depth", rec="R08 p4211", late=True)])
# c801〜c803：意見1（R08 p.204）＝1つの文「in all probability due to: a. An initial flooding casualty … which continued, compounded by
#   b. … c. … and d. …」＝**a の浸水が続き、b・c・d が重なった**（a→b・c→d の因果の鎖ではない）＝流れ図の矢印にしない（映像方針 §21）
#   ・c801 は4つの中身を書かない（c802・c803 の語り）
FORM_O1 = dict(title="査問会の意見1", rec="R08 p4204", paper=_P2, lw=150,
               fields=[dict(t="何が", v="the loss of the U.S.S. THRESHER", rec="R08 p4204"),
                       dict(t="見立て", v="was in all probability due to:", rec="R08 p4204", late=True)])
_O1 = dict(a='An initial flooding casualty from an orifice between 2" and 5" in size in the engine room',
           b="Loss of reactor power due to an electrically-induced automatic shutdown",
           c="Inadequate operating procedures … a flooding casualty and the loss of reactor power",
           d="A deficient air system, susceptible to freeze-up, with low capacity and low blow rate.")
FORM_O1A = dict(title="査問会の意見1", rec="R08 p4204", paper=_P2, lw=120,
                fields=[dict(t="1つ目", v=_O1["a"], rec="R08 p4204", late=True),
                        dict(t="2つ目", v=_O1["b"], rec="R08 p4204", late=True)])
FORM_O1B = dict(title="査問会の意見1", rec="R08 p4204", paper=_P4, lw=120,
                fields=[dict(t="1つ目", v=_O1["a"], rec="R08 p4204"), dict(t="2つ目", v=_O1["b"], rec="R08 p4204"),
                        dict(t="3つ目", v=_O1["c"], rec="R08 p4204", late=True),
                        dict(t="4つ目", v=_O1["d"], rec="R08 p4204", late=True)])
# c806・c808：意見5（R08 p.204）「a flooding casualty in THRESHER could have resulted from: a. A faulty sil-braze joint. …」
#   （「次のどれからも」の語は原文に無い）。6つの候補は c807 の並べ図。c808 は「継手＝候補 a」だけ（AP の「burst pipe」は海軍の
#   見方として書かれた語＝「よく語られる話」の例に使わない）
FORM_O5 = dict(title="査問会の意見5", rec="R08 p4204", paper=_P1, lw=130,
               fields=[dict(t="浸水は", v="a flooding casualty in THRESHER could have resulted from:", rec="R08 p4204", late=True)])
FORM_O5A = dict(title="査問会の意見5", rec="R08 p4204", paper=_P2, lw=130,
                fields=[dict(t="浸水は", v="a flooding casualty in THRESHER could have resulted from:", rec="R08 p4204"),
                        dict(t="候補a", v="A faulty sil-braze joint.", rec="R08 p4204", late=True)])
# c809：意見2（R08 p.204）。🔴 中の句「conjecture may be stretched too far and become accepted as fact」は次の c810（決め所）＝書かない
FORM_O2 = dict(title="査問会の意見2", rec="R08 p4204", paper=_P2, lw=170,
               fields=[dict(t="混ぜると", v="in melding together fact and conjecture,", rec="R08 p4204", late=True),
                       dict(t="狭まるもの", v="thus narrowing the field of search for possible causes of the casualty.", rec="R08 p4204",
                            late=True)])
# c811：意見49（R08 p.215）
FORM_O49 = dict(title="査問会の意見49", rec="R08 p4215", paper=_P2, lw=270,
                fields=[dict(t="正確な原因", v="although we may never learn the exact cause", rec="R08 p4215", late=True),
                        dict(t="分かっていること",
                             v="we do know enough to make it necessary for us to explore in depth the many possible causes",
                             rec="R08 p4215", late=True)])
# c813・cb18：海軍長官の最後の意見書（第7 endorsement・1965年＝IR18 p.6 の段落11。文字の層は行の順が崩れている＝頁の画像で読んだ）。
#   「原因は決められていない・おそらく永久に分からない」は c812 の語り＝書かない／「Not knowing the exact cause, we have carefully
#   examined all phases …」は cb19 の語り＝書かない
FORM_NITZE = dict(title="海軍長官の最後の意見書（1965年）", rec="IR18 p2006", paper=_P3, lw=170,
                  fields=[dict(t="候補", v="faulty design, structural or mechanical failure or malfunction or personnel error",
                               rec="IR18 p2006", late=True),
                          dict(t="始まり", v="set in motion the chain of events which led to eventual catastrophe", rec="IR18 p2006",
                               late=True),
                          dict(t="分からない", v="We, therefore, will never know whether", rec="IR18 p2006", late=True)])
FORM_NITZE2 = dict(title="海軍長官の最後の意見書（1965年）", rec="IR18 p2006", paper=_P2, lw=130,
                   fields=[dict(t="原因", v="we have not been able to establish the cause", rec="IR18 p2006", late=True),
                           dict(t="良い面", v="has had its beneficial effects", rec="IR18 p2006", late=True)])
# c816：原子炉の責任者の声明の結び（J p.89＝1963年7月23日・「(b)」の札は文字の層で「(S)」）。前の c815 の「I do not know」は書かない
FORM_RICK89 = dict(title="原子炉の責任者の声明（議会・1963年7月23日）", rec="J p8089", paper=_P2, lw=270,
                   fields=[dict(t="分かっていること",
                                v="I do know there were weaknesses in her design, fabrication, and inspection", rec="J p8089",
                                late=True),
                           dict(t="どうするか", v="that must be corrected", rec="J p8089", late=True)])
# c817：元分析官の書簡（A-R＝2013年4月10日・個人＝短い一節だけ）。中身（筋書き）は次の c818
FORM_RULE = dict(title="元分析官の書簡（2013年4月10日）", rec="A-R p9961", paper=_P3, lw=150,
                 fields=[dict(t="書いた人", v="the Analysis Officer at the SOSUS Evaluation Center in April 1963", rec="A-R p9961",
                              late=True),
                         dict(t="宛て先", v="Deputy Chief of Naval Operations Warfare Systems", rec="A-R p9961", late=True),
                         dict(t="件名", v="Information and Security Issues Associated with the Loss of the USS THRESHER",
                              rec="A-R p9961", late=True)])
# c821：大西洋艦隊の司令官の意見書（第1 endorsement・1963年6月12日＝IR18 p.120・本文 p.122）。c605 の「艦隊司令官の意見書」と同じ書類
#   （表題は別の名＝門番の表も別の行）。⚠️ echo：「大西洋艦隊の司令官の意見書（1963年6月12日）」は字幕「大西洋艦隊の司令官も、1963年6月の
#   意見書で、」と73%（2か所に割れた一致）＝表題は「1番目の意見書」（FIRST ENDORSEMENT）・誰のかは注で
FORM_CINC2 = dict(title="1番目の意見書（1963年6月12日）", rec=["IR18 p2120", "IR18 p2122"], paper=_P3, lw=170,
                  fields=[dict(t="空気の系統", v="of inadequate capacity, susceptible to freeze-up and with an inadequate blow rate",
                               rec="IR18 p2122", late=True),
                          dict(t="評価", v="This grossly unsatisfactory situation", rec="IR18 p2122", late=True),
                          dict(t="現役の艦",
                               v="Immediate steps have been taken in operating ships to: (1) remove high pressure air reducer strainers",
                               rec="IR18 p2122", late=True)])
# c902：海軍長官の書簡（付録6＝J p.146〜147・1963年6月20日・宛て先は委員長）。「nuclear ship」（原子力艦）
FORM_KORTH1 = dict(title="海軍長官の書簡（1963年6月20日）", rec=["J p8146", "J p8147"], paper=_P3, lw=150,
                   fields=[dict(t="宛て先", v="Chairman, Joint Committee on Atomic Energy", rec="J p8146", late=True),
                           dict(t="記録", v="a considerable portion of the record is classified", rec="J p8147", late=True),
                           dict(t="漏れたら", v="Any unauthorized release would seriously affect our nuclear ship and Polaris programs.",
                                rec="J p8147", late=True)])
# c904：海軍長官の返事（J p.164・1963年8月29日・宛て先は小委員長）。出すのは公聴会の記録の事実と仮定（assumptions）
FORM_KORTH2 = dict(title="海軍長官の返事（1963年8月29日）", rec="J p8164", paper=_P4, lw=150,
                   fields=[dict(t="時期", v="it would be a poor time indeed", rec="J p8164", late=True),
                           dict(t="何を", v="to release piecemeal the facts and assumptions documented by your hearings", rec="J p8164",
                                late=True),
                           dict(t="おそれ", v="could materially downgrade our offensive-defensive submarine weapons systems",
                                rec="J p8164", late=True),
                           dict(t="誰の心で", v="both in the public mind and the minds of our officers and men that man them",
                                rec="J p8164", late=True)])
# c908：塗った理由を示す札（頁の画像の赤い字＝V1 p.38「b(1)」・V1 p.54「b(3) 10 USC 130」・R08 p.181「(b) (6)」）。欄の名は情報公開の
#   法律の除外の中身（語りの言い方）・記号は画だけ（語りでは読まない＝台本 §1-6）
FORM_CODES = dict(title="塗った理由を示す札（公開の記録）", rec=["V1 p38", "V1 p54", "R08 p4181"], paper=_P3, lw=340,
                  fields=[dict(t="国の安全", v="b(1)", rec="V1 p38"),
                          dict(t="法律で伏せてよい情報", v="b(3) 10 USC 130", rec="V1 p54"),
                          dict(t="個人の私生活", v="(b) (6)", rec="R08 p4181")])
# c912・c919（紙2枚目）：AP の記事（p9901＝2021-08-02）。原告の言葉「There's no coverup. No smoking gun」は次の c913（決め所）＝書かない。
#   名前は語りだけ
FORM_AP = dict(title="AP通信の記事（2021年8月2日）", rec="AP p9901", paper=_P2, lw=150,
               fields=[dict(t="訴えた人", v="who sued for release of the documents under the Freedom of Information Act",
                            rec="AP p9901", late=True),
                       dict(t="その人", v="himself the skipper of a Thresher-class submarine", rec="AP p9901", late=True)])
FORM_AP900 = dict(title="AP通信の記事（2021年8月2日）", rec="AP p9901", lw=130,
                  fields=[dict(t="読み方", v="900 feet beyond its test depth", rec="AP p9901", late=True)])
# c919（紙1枚目）：認定17（R08 p.185）「An additional garbled transmission was received about 0917R, reported as containing the words
#   "... nine hundred North".」＝査問会は意味を書いていない（意味の欄は作らない）
FORM_F17 = dict(title="査問会の認定17", rec="R08 p4185", lw=230,
                fields=[dict(t="9:17ごろの声", v='"... nine hundred North"', rec="R08 p4185", late=True)])
# c915：原子炉の責任者の証言（J p.122・1964年7月1日）。深さの数は刷られていない（[classified matter deleted]）。計算の中身は c916
FORM_RICK122 = dict(title="原子炉の責任者の証言（議会・1964年7月1日）", rec="J p8122", paper=_P1, lw=170,
                    fields=[dict(t="話したこと", v="how that magic number [classified matter deleted] first came about", rec="J p8122",
                                 late=True)])
# c917：潜水艦戦の部長（海軍の少将）の証言（J p.124・1964年7月1日）
FORM_WILK = dict(title="海軍の少将の証言（議会・1964年7月1日）", rec="J p8124", paper=_P3, lw=170,
                 fields=[dict(t="検討", v="one other study in the Office of Chief of Naval Operations", rec="J p8124", late=True),
                         dict(t="行く深さ", v="the depth to which we would go is what the state of the art will allow us", rec="J p8124",
                              late=True),
                         dict(t="戦術の根拠",
                              v="there is not a tactical justification for [classified matter deleted] feet or any other depth",
                              rec="J p8124", late=True)])
# ca04：捜索の指揮官の証言（R08 p.66）。たとえの高さは 8500 feet（＝約2,600メートル・語り）
FORM_ANDR2 = dict(title="捜索の指揮官の証言（査問会）", rec="R08 p4066", paper=_P3, lw=190,
                  fields=[dict(t="写すこと", v="is a very easy operation", rec="R08 p4066", late=True),
                          dict(t="カメラの位置", v="the camera must be 30 feet from the spot", rec="R08 p4066", late=True),
                          dict(t="たとえ", v="being up in an airplane 8500 feet high with a string and a camera on the end of it",
                               rec="R08 p4066", late=True)])
# cb02：意見4（R08 p.204）
FORM_O4 = dict(title="査問会の意見4", rec="R08 p4204", paper=_P2, lw=170,
               fields=[dict(t="見直すまで", v="until each individual submarine's readiness has been reassessed", rec="R08 p4204",
                            late=True),
                       dict(t="制限", v="it would be prudent to retain the current interim depth limitation", rec="R08 p4204",
                            late=True)])
# cb06：勧告20（R08 p.220＝最後の勧告・文字の層の頭の「"」は外す）
FORM_R20 = dict(title="査問会の勧告20", rec="R08 p4220", paper=_P4, lw=170,
                fields=[dict(t="組織", v="an organization, similar to that employed in Naval Aviation", rec="R08 p4220", late=True),
                        dict(t="分析", v="the analysis of events and developments which pertain to submarine safety", rec="R08 p4220",
                             late=True),
                        dict(t="伝えること", v="the timely dissemination of such information", rec="R08 p4220", late=True),
                        dict(t="検討", v="That early consideration be given", rec="R08 p4220", late=True)])
# cb08：意見42（R08 p.212）
FORM_O42 = dict(title="査問会の意見42", rec="R08 p4212", paper=_P4, lw=170,
                fields=[dict(t="情報", v="all information to be had from the BARBEL and other casualties", rec="R08 p4212", late=True),
                        dict(t="分析と伝達", v="thorough and imaginative analysis and timely dissemination", rec="R08 p4212", late=True),
                        dict(t="欠陥", v="the deficiencies which probably caused THRESHER's loss", rec="R08 p4212", late=True),
                        dict(t="結果", v="could have been reduced", rec="R08 p4212", late=True)])
# cb10：艦船局の副長の証言（J p.95・97＝1964年7月1日・綴りは Curtze＝J p.174）
FORM_CURTZE = dict(title="艦船局の副長の証言（議会・1964年7月1日）", rec=["J p8095", "J p8097"], paper=_P3, lw=170,
                   fields=[dict(t="始まり", v="The genesis of this effort was not Thresher's loss", rec="J p8095", late=True),
                           dict(t="振り返れば", v="we moved too fast and too far in areas of offensive and defensive capabilities",
                                rec="J p8097", late=True),
                           dict(t="安全", v="Submarine safety did not keep pace.", rec="J p8097", late=True)])
# cb11：艦隊の運用の担当の中将の証言（J p.94＝1964年7月1日・4月の勧告＝1964年4月）。同じ頁の安全センター（cb05）は書かない
FORM_RAMAGE = dict(title="海軍の中将の証言（議会・1964年7月1日）", rec="J p8094", paper=_P3, lw=230,
                   fields=[dict(t="4月の勧告", v="the Deep Submergence System Review Group … submitted its recommendations",
                                rec="J p8094", late=True),
                           dict(t="動けなくなる所", v="could be disabled in water too shallow to collapse the hull", rec="J p8094",
                                late=True),
                           dict(t="救難", v="still be beyond our rescue capability", rec="J p8094", late=True)])
# cb15・cb16：意見55（R08 p.216＝最後の意見・「U.S.S. Thresher」は頁の画像でも小文字まじり）。🔴「The responsibility for the loss of
#   THRESHER cannot be charged to neglect or dereliction …」は次の cb17（決め所）＝書かない
FORM_O55A = dict(title="査問会の意見55", rec="R08 p4216", paper=_P2, lw=270,
                 fields=[dict(t="水準", v="required to insure the thorough overhaul and safe operation of the U.S.S. Thresher",
                              rec="R08 p4216", late=True),
                         dict(t="届いていないもの", v="numerous practices, conditions and standards which were short of those",
                              rec="R08 p4216", late=True)])
FORM_O55B = dict(title="査問会の意見55", rec="R08 p4216", paper=_P4, lw=340,
                 fields=[dict(t="急な変化", v="the rapid changes … of submarines during the last decade", rec="R08 p4216", late=True),
                         dict(t="計画", v="the accelerated pace of the submarine program", rec="R08 p4216", late=True),
                         dict(t="誰のせいか", v="They can be blamed on no individual or individuals", rec="R08 p4216", late=True),
                         dict(t="気づかれなかったもの", v="many would not have come to notice had THRESHER not been lost",
                              rec="R08 p4216", late=True)])
# cb20（数の比べ → 書類の再現図＝映像方針 §21）：NAVSEA の記事（p9951＝2023-04-06）。「16隻」（第一次大戦〜1963年）は語りに無い＝書かない
FORM_NAVSEA = dict(title="米海軍 艦艇の部門の記事（2023年4月6日）", rec="NAVSEA p9951", paper=_P2, lw=270,
                   fields=[dict(t="サブセーフのあと", v="the U.S. Navy has only lost one submarine, USS Scorpion (SSN 589)",
                                rec="NAVSEA p9951", late=True),
                           dict(t="その艦", v="Scorpion was not SUBSAFE-certified", rec="NAVSEA p9951", late=True)])

# 🆕 18本目 ⑤b-6a：流れ図（c107・c110・c218・c421・c616・c618）。箱の言葉は記録の文の言葉・役職だけ（名前は語りだけ）・赤を使わない。
#   言葉と頁は門番 check_boxes の REC_OTHER_ROLE・REC_MECH・REC_CHIP と照らす
FL_EMPTY = dict(heads=[])
FL_CAPT = dict(heads=[], kind="スレッシャーの艦長")
FL_KNEW = dict(heads=[dict(id="d_dec", t="外さないという決定", kind="node", x=(110, 600), y=(470, 570), rec="R08 p4197")])
FL_UP = dict(heads=[])
FLP = {
    # c107「3枚の紙」（映像方針 §6）＝前の艦長の評価書（証拠111＝X p.531・認定91）・検査の数字（認定102）・検査の書類（認定104〜106）→
    #   どこまで届いたか（認定108・J p.18＝報告書は4月11日より後）
    "p_eval": dict(k="role", id="p_eval", t="前の艦長の評価書", y=380, pos=(130, 690), rec=["X p1531", "R08 p4195"]),
    "p_num": dict(k="role", id="p_num", t="検査の数字", y=520, pos=(130, 690), rec="R08 p4197"),
    "p_doc": dict(k="role", id="p_doc", t="検査の書類", y=660, pos=(130, 690), rec="R08 p4197"),
    "p_far": dict(k="role", id="p_far", t="どこまで届いたか", y=520, pos=(1180, 1760), rec=["R08 p4197", "J p8018"]),
    # c110 手がかり＝査問会の記録（R08 p.181〜）と議会の公聴会の記録（J p.1＝1963年6月26日・p.91＝1964年7月1日）
    "k_court": dict(k="role", id="k_court", t="査問会の記録", y=470, pos=(180, 800), rec="R08 p4181"),
    "k_jcae": dict(k="role", id="k_jcae", t="議会の公聴会の記録", y=470, pos=(1060, 1740), rec="J p8001"),
    # c218 艦長の行き先（R08 p.107「Prospective Commanding Officer of the JOHN C. CALHOUN」・p.109「one of the best qualified people we
    #   could find」）
    "a_old": dict(k="role", id="a_old", t="前の艦長", y=420, pos=(160, 600), rec="R08 p4107"),
    # ⚠️ echo：「ポラリス潜水艦の艦長の予定者」は字幕の丸写し（100%）＝語順を替えて連続一致を短く
    "a_pol": dict(k="role", id="a_pol", t="艦長の予定者（ポラリス）", y=420, pos=(1000, 1760), rec="R08 p4107"),
    "a_new": dict(k="role", id="a_new", t="新しい艦長", y=640, pos=(160, 600), rec="R08 p4109"),
    # c421 査問会の組み立て（意見45＝R08 p.212「assumptions and computer solutions」「a reasonable rationalization of probable events」・
    #   p.214「the most probable approximation of the sequence of events」・声＝認定16・17／音＝認定18〈R08 p.185〉）
    "z_voice": dict(k="role", id="z_voice", t="水中電話の声", y=380, pos=(130, 650), rec="R08 p4185"),
    "z_sound": dict(k="role", id="z_sound", t="監視の記録", y=520, pos=(130, 650), rec="R08 p4185"),
    "z_calc": dict(k="role", id="z_calc", t="仮定と計算", y=660, pos=(130, 650), rec="R08 p4212"),
    "z_plot": dict(k="role", id="z_plot", t="最もありうる筋書き", y=520, pos=(1180, 1760), rec=["R08 p4212", "R08 p4214"]),
    # c616 決定を知っていた人（認定105「known to the management personnel of the Shipyard, including the Production Officer and the
    #   Commander」・認定106「a copy of this decision was furnished the Commanding Officer of THRESHER」＝R08 p.197）
    "k_prod": dict(k="role", id="k_prod", t="造船所の生産の責任者", y=360, pos=(1180, 1780), rec="R08 p4197"),
    "k_cmdr": dict(k="role", id="k_cmdr", t="造船所の司令官", y=480, pos=(1180, 1780), rec="R08 p4197"),
    # ⚠️ echo：「当時のスレッシャーの艦長」は字幕の丸写し（100%）
    "k_co": dict(k="role", id="k_co", t="スレッシャーの艦長（当時）", y=660, pos=(1180, 1780), rec="R08 p4197"),
    # c618 上がっていない（認定108＝R08 p.197「neither the results of the surveillance nor the decision … was made known to the Bureau of
    #   Ships」・J p.14「no decision or no recommendation was sent to the Bureau of Ships, and the decision was made locally in the yard」）。
    #   🔴 「艦に命令を出す上の人たち」は次の c619 の語り＝描かない／当時の艦長への写しは前の c616＝描かない（映像方針 §20）
    "u_res": dict(k="role", id="u_res", t="検査の結果の数字", y=430, pos=(130, 640), rec="R08 p4197"),
    "u_dec": dict(k="role", id="u_dec", t="外さないという決定", y=590, pos=(130, 640), rec="R08 p4197"),
    "u_bu": dict(k="role", id="u_bu", t="艦船局", y=510, pos=(1280, 1760), rec=["R08 p4197", "J p8014"]),
    # ── 🆕 ⑤b-6b（2026-10-04）：第7〜11章の流れ図（c705・c818・c820・c823・c916・c918・cb04）。箱の言葉は11字まで（門番 echo は12字から）──
    # c705 認定47（R08 p.190「the increasing operating depths of submarines has compressed the time available in which to take effective
    #   damage control action with respect to flooding. The shortness of time … is not well recognized.」）
    "d_deep": dict(k="role", id="d_deep", t="潜る深さが増す", y=520, pos=(160, 760), rec="R08 p4190"),
    "d_time": dict(k="role", id="d_time", t="手を打てる時間が縮む", y=520, pos=(1100, 1760), rec="R08 p4190"),
    # c818 元分析官の推定（A-R＝個人）「the initial casualty … was the failure at 0911 of the primary (non-vital) electrical bus which shut down
    #   the submarine's Main Coolant Pumps (MCPs) resulting in the immediate scram」・「there was no flooding prior to collapse」
    "r_elec": dict(k="role", id="r_elec", t="電気の系統の故障（9:11）", y=440, pos=(100, 640), rec="A-R p9961"),
    "r_pump": dict(k="role", id="r_pump", t="ポンプが止まる", y=440, pos=(760, 1180), rec="A-R p9961"),
    "r_scram": dict(k="role", id="r_scram", t="原子炉が止まる", y=440, pos=(1300, 1800), rec="A-R p9961"),
    # c820 3つの見方がそろって挙げる所＝空気の系統（台本 §1-5：査問会＝意見1d・艦隊司令官＝IR18 p.122・元分析官＝個人の推定。「凍って吹き
    #   出せなかった」で一致とは言わない＝当日に凍ったと言うのは元分析官だけ）
    "v_court": dict(k="role", id="v_court", t="査問会の意見1", y=360, pos=(110, 720), rec="R08 p4204"),
    "v_cinc": dict(k="role", id="v_cinc", t="艦隊司令官の意見書", y=540, pos=(110, 720), rec="IR18 p2122"),
    "v_rule": dict(k="role", id="v_rule", t="元分析官の書簡（個人）", y=720, pos=(110, 720), rec="A-R p9961"),
    "v_air": dict(k="role", id="v_air", t="空気の系統", y=540, pos=(1260, 1760), rec=["R08 p4204", "IR18 p2122", "A-R p9961"]),
    # c823 次の章へ（原因は決まっていない＝IR18 p.6・意見49／塗り＝V1 p.38 の b(1)）→ ある噂（AP p9901＝coverup の疑い）。噂の中身は c901
    "n_cause": dict(k="role", id="n_cause", t="決まっていない原因", y=400, pos=(110, 700), rec=["IR18 p2006", "R08 p4215"]),
    "n_red": dict(k="role", id="n_red", t="塗られたままの記録", y=640, pos=(110, 700), rec="V1 p38"),
    "n_rumor": dict(k="role", id="n_rumor", t="ある噂", y=520, pos=(1300, 1760), rec="AP p9901"),
    # c916 数字の生まれ（J p.122「the Bureau of Ships was asked, "How deep can you go without a major increase in the cost of submarines?"
    #   They made a quick calculation and came up with [classified matter deleted].」「It was originally just on the basis of cost.」）。
    #   「その先は費用が急に上がる」「本当の評価はまだ無い」は語りに無い＝描かない
    "q_ask": dict(k="role", id="q_ask", t="艦船局への問い", y=440, pos=(110, 560), rec="J p8122"),
    "q_calc": dict(k="role", id="q_calc", t="ざっとした計算", y=440, pos=(720, 1180), rec="J p8122"),
    "q_num": dict(k="role", id="q_num", t="その数字", y=440, pos=(1340, 1780), rec="J p8122"),
    # c918 試験深度の数（数の比べ → 流れ図＝映像方針 §21）。🔴 **深さの数を絵に出さない**（守りの線＝公開の記録では塗られている＝V1 p.38
    #   の b(1)）。書簡（A-R「test-depth: 1300-feet」）と記事（AP「previously declassified documents indicated it was 1,300 feet」）は
    #   「数が書かれている」とだけ＝数は語りだけ
    "s_pub": dict(k="role", id="s_pub", t="公開の記録", y=380, pos=(110, 640), rec="V1 p38"),
    "s_red": dict(k="role", id="s_red", t="塗られている", y=380, pos=(1220, 1760), rec="V1 p38"),
    "s_rule": dict(k="role", id="s_rule", t="元分析官の書簡（2013年）", y=560, pos=(110, 640), rec="A-R p9961"),
    "s_ap": dict(k="role", id="s_ap", t="AP通信の記事（2021年）", y=720, pos=(110, 640), rec="AP p9901"),
    "s_num": dict(k="role", id="s_num", t="数が書かれている", y=640, pos=(1220, 1760), rec=["A-R p9961", "AP p9901"]),
    # cb04 1隻ずつの認め（J p.93＝1964年7月1日「will remain in effect until all subsafe measures have been accomplished and certified by
    #   the Bureau of Ships in the case of each submarine」）
    "c_fix": dict(k="role", id="c_fix", t="安全の改修を終える", y=580, pos=(100, 600), rec="J p8093"),
    "c_cert": dict(k="role", id="c_cert", t="艦船局が1隻ずつ認める", y=580, pos=(700, 1240), rec="J p8093"),
    "c_lift": dict(k="role", id="c_lift", t="深さの制限が解ける", y=580, pos=(1340, 1820), rec="J p8093"),
}
# 🆕 ⑤b-6b：流れ図の左上の札（kind）と見出しの箱（heads）
FL_RULE = dict(heads=[], kind="元分析官の推定（個人）")
FL_DEPTH = dict(heads=[], kind="試験深度の数")
FL_SS = dict(heads=[dict(id="h_ss", t="サブセーフ", kind="head", x=(660, 1260), y=(300, 370), rec="J p8093")])


def fl(name, **kw):
    return dict(FLP[name], **kw)


# 原因の並べ図（14本目＝c615・cc13）＝同じ形で並べるだけ（場面にしない）
# 🆕 18本目 ⑤b-6a：c115＝この動画の3つの問い（c114 の語り）を同じ形で並べる（流れ図 → 並べ図＝映像方針 §20）。頁＝その問いに答える記録
#   （浮き上がれなかった＝意見1 R08 p.204／伝わらなかった＝認定108 p.197・認定25 p.186／海の底＝1964年の要旨 R17書 p9802）
CAUSE = {
    "q_float": dict(k="item", t="浮き上がれなかった理由", rec="R08 p4204"),
    "q_pass": dict(k="item", t="伝わらなかった検査と声", rec=["R08 p4197", "R08 p4186"]),
    "q_sea": dict(k="item", t="海の底に残った物", rec="R17書 p9802"),
    # 🆕 ⑤b-6b：c807＝意見5（R08 p.204）の6つの候補（a〜f）を2段に同じ形で（数の比べ → 並べ図＝映像方針 §21）。言葉は語りの丸写しにしない
    #   （門番 echo＝12字から）：b「Undiscovered shock damage」＝未発見の衝撃の損傷・f「Unknowns, including component failure」＝不明（部品の故障を含む）
    "f_a": dict(k="item", t="銀ろう付けの継手の不良", rec="R08 p4204"),
    "f_b": dict(k="item", t="未発見の衝撃の損傷", rec="R08 p4204"),
    "f_c": dict(k="item", t="曲がるホースの故障", rec="R08 p4204"),
    "f_d": dict(k="item", t="鋳物か配管の故障", rec="R08 p4204"),
    "f_e": dict(k="item", t="船体の小さな破損", rec="R08 p4204"),
    "f_f": dict(k="item", t="不明（部品の故障を含む）", rec="R08 p4204"),
}


def cause(name, **kw):
    return dict(CAUSE[name], **kw)


# 🔴 2026-10-01（16本目 ⑤b-1・§0b）：15本目の箱の型の表（報告書の鎖 CHAIN1・CHAIN2・重なった要因 FACTORS・3つの問いの答え ANS・ANSP・
#    実況の担当 MC・MCP・2010年の成績 HEAT・書類の再現図 FORM_LOG11 ほか7枚）と、その関数（`chain_links()`・`ans_links()`）は
#    `tools/fixture_ep15.py` へ移した（値は1つも変えていない＝git の `c646174`）。
# 🔴 2026-10-04（18本目 ⑤b-1・§0b）：16本目の箱の型の表（流れ図 FL_SRC・FL_GROW・FL_HIDE・FL_EXP・FL_THREE・FLP と関数 `fl()`／
#    書類の再現図 FORM_MUELLER・FORM_UNITA・FORM_NOTE60・FORM_GHETTI・FORM_NOVE・FORM_GC61・FORM_LET9・FORM_LET9B・FORM_MIN2・FORM_JUDG／
#    並べ図の項目 CAUSE）は `tools/fixture_ep16.py` へ移した（値は1つも変えていない＝git の `b044b56`）。18本目の箱は ⑤b で足す
#    （門番 check_boxes の REC_MECH・REC_OTHER_ROLE・REC_CHIP・REC_FORM・REC_CAUSE も、回の値を門番の側に別に持つ＝§5b-88）


# ══════════════════════════════════════════════════════════
#  16本目 ⑤b-8（2026-10-02）：決め所の出どころの札（`fig=("quote", dict(phrase=[…], rows=ss.qrows(…), paper=True))`）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-04（18本目 ⑤b-1・§0b）：16本目の資料の名の表 QDOC・QWHO と関数 `qrows()` は `tools/fixture_ep16.py` へ移した
#    （値は1つも変えていない＝git の `b044b56`）。18本目で決め所の出どころの札を使うときは、その回の QDOC・QWHO・`qrows()` をここに足す。
#    ⚠️ 教訓は移した注の側にある（札の値は全角12字ぶんで折れる・語の途中で折れない名前にする・決め所の言葉は台本の★の行と1字も違えない
#       ＝fixture_ep16 の QDOC の上）
