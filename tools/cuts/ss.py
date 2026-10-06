# -*- coding: utf-8 -*-
"""19本目（サーフサイドのマンション崩壊のリメイク・2021-06-24）の章ファイルが共通で使う小道具。

**18本目（スレッシャー号のリメイク）の中身は git の `2d627a2`（章ファイルの空の器より前は `b11797a`）にある**
（`git show b11797a:tools/cuts/ss.py`）。**16本目（バイオントダム災害）は git の `b044b56`**（`git show b044b56:tools/cuts/ss.py`）。
15本目（リノ・エアレース2011）は `c646174`、14本目（セウォル号）は `dc6ecf4`、13本目（トルコ航空981便）は `b54ee4f`、
12本目（キャッスル・ブラボー）は `3832147`、11本目（チャレンジャー号）は `61039d2`、10本目（三豊百貨店）は `46f11b3`、
9本目（テネリフェ）は `e18b8f1`、8本目は `4c71bf0`、7本目は `ae30d49`。

🔴 **⑤b-1（2026-10-06・19本目）で空にした**＝§0b。18本目の型の値（案C の出典の表 REC_DOCS・時計と秒の札・描いてよい数・想定の札・
壊れる物のカット・潜水艦の時刻 ILLU_SUB_*・音の輪・混ざりのつなぎ待ち・軸の型〈TV／TM・AX_*・AXI の項目〉・棒〈QG・QB〉・
書類の再現図〈FORM_*・欄の値は原文の英語〉・流れ図〈FL_*・FLP・`fl()`〉・並べ図〈CAUSE〉・決め所の出どころの札〈QDOC・QWHO・`qrows()`〉）は、
門番の selftest の見本 `tools/fixture_ep18.py` へ移した（値は1つも変えていない＝git の `2d627a2` と同じ）。本番の ss は19本目の空の器
（REF／EP＝ep19・REC_PAGES＝ep19_pages.txt）。`PANEL_AR`（束ごとに取り直す定数）だけは18本目の値 1.66 のまま＝⑤b-7 で19本目の束で取り直す。
（以下は ⑤b-1・2026-10-04＝18本目のとき）16本目の束の定数（顔だけモザイクの PD 写真1点 NEEDS_MASK）は外した。
16本目の型の値（案C の出典の表・時計と想定の札・壊れる物のカット・軸の型・水位と斜面の速さの線・棒・流れ図と書類の再現図・
並べ図・決め所の出どころの札）は、門番の selftest の見本 `tools/fixture_ep16.py` へ移した（値は1つも変えていない＝git の
`b044b56` と同じ）。15本目の型の値は `tools/fixture_ep15.py`（2026-10-01 に移した・git の `c646174`）、14本目の型の値は
`tools/fixture_ep14.py`（2026-09-30 に移した・git の `dc6ecf4`）。18本目の束は写真の束のチャットで作る。
🆕 下の「素材の名前」「人が写る点の扱い」は18本目の書きぶり（19本目の束を作る ⑤b-7 で、`ep18` を `ep19` に替えて書き直す）。
16本目の書きぶりは git の `b044b56`。

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
REF = HERE / "ref" / "ep19"
EP = "ep19/"
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
#    🔴 2026-10-06（19本目 ⑤b-1）：下の値 1.66 は**18本目の束の値のまま**（§0b で空にする値ではなく、束ごとに取り直す定数＝数なので空の器が
#       作れない。16→18本目のときの 1.10 と同じ扱い）。⑤b-7 で19本目の束（`python qa_out/ep19_assets.py panel` の並び）で取り直す。
#       それまで WIDE_AR も18本目の値（1.90）から導かれる。見本 `tools/fixture_ep18.py` には入れていない（16本目の見本も入れていない）
PANEL_AR = 1.66                   # これ未満＝縦長すぎ（上下が切れる）
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


# 🔴 2026-10-05（18本目 ⑤b-7c）：ここにあった前の回の `vid`（panel を付けない版＝`dict(photo=fb(cid), **kw)`）は外した。
#    上（fb のすぐ下）の新しい `vid` を**あとから上書きしていた**＝記録映画（655×480）が全画面に引き伸ばされて焼けた
#    （試し焼き 37246867517・21カット全部）。同じ名前の関数を2つ置かない（`grep -n "^def " tools/cuts/ss.py` で重なりを見る）


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
# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の値（出典の表 REC_DOCS・割れる時刻・時計と秒の札・描いてよい数・想定の札・壊れる物のカット・
#    潜水艦の時刻・音の輪・混ざりのつなぎ待ち）は selftest の見本 `tools/fixture_ep18.py` へ移した（値は1つも変えていない＝git の
#    `2d627a2`）。19本目の値は、その型を初めて使う ⑤b のチャットで入れる（空のあいだ、その型を使うカットは門番・型が止まる＝fail closed）。
#    頁の番号の書き方・資料の名の決め方・守りの線の理由（18本目の例）は移した注の側にある＝fixture_ep18 の案C の節の上
REC_PAGES = REF / "src" / "ep19_pages.txt"      # ④ の make_pages.py の出力（git の外＝手元だけ）
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    # 🆕 19本目 ⑤b-2（2026-10-06）：通し頁は `ref/ep19/src/ep19_pages.txt`（④ の make_pages.py）＝TR の行 n → p(1000+n)・AC の PDF 頁 n →
    #   p(2000+n)・TF のコマ・スライド → p9001〜。TR は行（頁ではない）・TF はスライド＝画面に頁を出さない（page=None）
    "TR": dict(range=(1001, 1489), name="NIST 技術的知見の動画の語り（2026年6月）", page=None, base=0),
    "AC": dict(range=(2001, 2082), name="NIST の諮問委員会の資料（2026年9月）", page="pdf", base=2000),
    "TF": dict(range=(9001, 9808), name="NIST 技術的知見の動画のスライド（2026年6月）", page=None, base=0),
    # 🆕 ⑤b-3：大陪審の報告（GJ の PDF 頁 n → p(3000+n)・印字の頁＝PDF 頁−3）・町の発表（A13＝1頁）
    "GJ": dict(range=(3001, 3043), name="マイアミ・デイド郡の大陪審の報告（2022年）", page="print", base=3003),
    "A13": dict(range=(5102, 5102), name="サーフサイド町の発表（2026年8月13日）", page=None, base=0),
    # 🆕 ⑤b-5（2026-10-06）：軸の型（年表・時間の帯）の出典。調査の報告（MC18＝町の写しの PDF 頁＝報告の頁）・議事録（MIN18＝町の写しの PDF 頁）・
    #   町の頁（A12）・NIST の発表（B08）・GAO（B01）・FEMA（B02）・裁判所（A17・A18・A19＝PDF 頁）。⚠️ A11（MIN18）・A17 の原文は git の外のまま
    "MC18": dict(range=(4001, 4009), name="モラビトの調査の報告（2018年10月）", page="print", base=4000),
    "MIN18": dict(range=(4101, 4107), name="理事会の議事録（2018年11月15日）", page="pdf", base=4100),
    "A12": dict(range=(5101, 5101), name="サーフサイド町の頁", page=None, base=0),
    "B08": dict(range=(5005, 5005), name="NIST の発表（2024年11月21日）", page=None, base=0),
    "B01": dict(range=(5601, 5617), name="米政府説明責任局（GAO）の報告（2024年2月）", page="pdf", base=5600),
    "B02": dict(range=(5701, 5705), name="FEMA の発表（2021年7月）", page="pdf", base=5700),
    "A17": dict(range=(7001, 7024), name="裁判所の最終の命令（2022年6月24日）", page="pdf", base=7000),
    "A18": dict(range=(7101, 7115), name="裁判所の売却を認める命令（2022年6月1日）", page="pdf", base=7100),
    "A19": dict(range=(7201, 7202), name="管財人の売却の告知（2022年7月27日）", page="pdf", base=7200),
}
ILLU_SPLIT_TIMES = ()                       # 資料で割れる時刻＝画面に時計・時刻の札として出さない
ILLU_CROWD_UNTIL = None                     # 乗客の群れを描いてよい場面の時刻の上限
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）
ILLU_CLOCK_OK = ()                          # 札に出してよい時計の時刻（門番 check_illu ⑤）
ILLU_COUNTS = {                             # 描いてよい数＝{部品の obj の名: (数, 出典)}（門番 check_illu ③）
    # 🆕 19本目 ⑤b-2：A1 の塔＝12階＋ペントハウス（TR0004「12 stories tall plus a penthouse」）
    "story": (12, "TR p1004"), "penthouse": (1, "TR p1004"),
    # 🆕 ⑤b-3：A4 の別の建物＝10階建て（GJ p.20「a 10-story, 156-unit condominium building」）・A5 の光の柱＝13本（A13）
    "story_other": (10, "GJ p3023"), "pillar": (13, "A13 p5102"),
}
_A1_ASSUME = "推定（NIST の見立て）"            # 🆕 19本目 ⑤b-2：NIST の読み（映像から・most likely）で描いた崩れ方
ILLU_ASSUME = {c: _A1_ASSUME for c in ("c619", "c620", "ca01", "ca18", "cc25")}   # 想定の札を出すカット（門番 check_illu ④）
# 🆕 19本目 ⑤b-3：A2・A3＝目撃した人の話だけが元の絵（門・柱の水・プランターの隙間）と、落ちた範囲が記録に無い絵（駐車場・デッキの一部）
ILLU_ASSUME.update({c: "目撃した人の話にもとづく" for c in ("c503", "c511", "c518")})
ILLU_ASSUME.update({c: "崩れた範囲は推定" for c in ("c604", "c609")})
# 壊れる物の部品を描いてよいカット（門番 check_illu ⑫＝空なら全部止める）。🆕 19本目 ⑤b-2：A1 の崩れ（真ん中・東・プールデッキ）
#   🆕 ⑤b-3：A2 の落ちた地上の駐車場・デッキの一部・沈んだ車（c604・c609）
ILLU_DESTROY_CUTS = ("c618", "c619", "c620", "ca01", "ca18", "cc25", "c604", "c609")
# 縮尺を持たない模式の上から見た絵の置き場＝{置き場: 理由}（門番 check_illu ⑧ は縮尺の代わりに「人が0・模式の断り」を測る）
#   🆕 19本目 ⑤b-3：A2（NIST の図から並びだけを描いた敷地＝寸法の記録が無い・人は決め⑤で描かない）
ILLU_TOP_NOSCALE = {"A2": "敷地の並びの模式・人は描かない（決め⑤）"}
ILLU_SUB_UNTIL = None                      # 潜水艦の時刻の上限（門番 ⑮＝無ければ潜水艦を描いたカットは止まる）
ILLU_SUB_EXC = {}                           # 上の上限の例外＝{カットID: 時刻}
ILLU_SUB_STOP = None                        # 艦の絵を止めたカット（これより後に潜水艦を置かない）
ILLU_BOOM_CUTS = ()                         # 音の輪（9時18.1分の型）を置いてよいカット（門番 ⑰）
ILLU_MIX_TODO = {                           # 混ざりの本物の側のつなぎ待ち＝{カットID: 理由}（門番 ⑦）
    "c618": "2行目からの尻の頁（NIST の資料 A01 p.47〜51・監視カメラのコマに NIST の印＝決め②）は ⑤b-7b",
}
ILLU_MIX_BUNDLE = REF / "credits.json"      # 束ができたか（混ざりのつなぎ待ちの終わり）を見るファイル

# 🔴 2026-10-06（19本目 ⑤b-1）：空にした（18本目は割れる時刻・出典の名つきの点を使わなかった＝空のままの値＝`tools/fixture_ep18.py`）
AXIS_DOCS = {}

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
# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の軸（TV・TM＝2段の帯の段の名／AX_REL・AX_INQ・AX_PSA・AX_MORN・AX_FIVE・AX_SKY・AX_DAY・AX_WEEK・
#    AX_PRE・AX_UT・AX_APR・AX_AIR・AX_CALC・AX_SAFE）と部品 AXI の18本目の項目は `tools/fixture_ep18.py` へ移した（値は1つも変えていない＝
#    git の `2d627a2`）。19本目の軸は ⑤b で `AX_<名> = dict(view, span, ticks)` を足し、`AXI.update({…})` に項目を足す。
#    ⚠️ 軸の教訓（軸の左右の余白・札を線から逃がす・次のカットの語りにある時刻は描かない・下見で1つの言葉に読めた札）は移した注の側にある
#       ＝fixture_ep18 の AX_*・AXI の上
# 🆕 2026-10-06（19本目 ⑤b-5）：年表・時間の帯 19カット（c210 c302 c318 c401 c409 c415 c418 c523 c602 c603 c605 c608 c622 c714 c719 c918 c919
#    ca20 cc20）。値と頁は ref/ep19/src/ep19_pages.txt で当てた＝門番の側の表（check_axis.REC_AXIS）と照らされる（§5b-88）。
#    🔴 守りの線：記録にある年月日・時刻だけ・NIST の「約○分前」は時計の時刻に直さない（基準 1:22 からの位置に置き、札は「約7分前」）・
#       最後の3週間（c523・c622）は NIST のスライド p9061 と同じ**並び**（間隔は時間に比例しない＝途切れの印と断り）・
#       入札の会議（6月11日）は記録が「崩れる13日前」としか書かない＝日付の札を出さない（lab=False）
TL_NOTE = "時刻は現地（アメリカ東部）"
ORDER_NOTE = "間隔は時間に比例しない（NIST のスライドの並べ方）"
AX_LIFE = dict(view="date", span=("1976", "2025"), ticks=("1980", "1990", "2000", "2010", "2020"))   # c210・c302・c918・c919 建物の歩み
AX_RUST = dict(view="date", span=("1993", "2023"), ticks=("1995", "2000", "2005", "2010", "2015", "2020"))   # c318 25年以上
#   ⚠️ 下見：左の端を 2018年7月にすると、左へ振った「2018年10月」の札が画面の左の外へ出た＝2017年10月から
#   ⚠️ 門番 check_axis：c418 の崩落の札を左へ振ると3段目まで積み上がり右上の章の札に触れた＝右の端を2022年4月まで広げ、c418 は右へ振る
AX_REP = dict(view="date", span=("2017-10", "2022-04"), ticks=("2018", "2019", "2020", "2021", "2022"))   # c401・c409・c418 報告のあと
AX_21 = dict(view="date", span=("2021-03-10", "2021-07-10"), ticks=("2021-04", "2021-05", "2021-06", "2021-07"))   # c415 2021年
AX_NIGHT = dict(view="clock", span=("1:11", "1:23"), ticks=("1:12", "1:14", "1:16", "1:18", "1:20", "1:22"),
                ref="1:22", ref_rec="A12 p5101")                                                       # c602〜c608 最後の数分
#   ⚠️ 門番 check_axis：AX_NIGHT に2回目の電話（1:17:49）と見張りの会社（1:17:55＝6秒差）まで並べると札が3段に収まらなかった＝c608 は3分の帯
AX_CALL = dict(view="clock", span=("1:16", "1:19"), ticks=("1:16", "1:17", "1:18", "1:19"))           # c608 1時17分台
AX_SEARCH = dict(view="date", span=("2021-06-20", "2021-07-26"),
                 ticks=("2021-06-24", "2021-07-01", "2021-07-08", "2021-07-15", "2021-07-22"))       # c714 26日
AX_NIST = dict(view="date", span=("2021-01", "2022-04"), ticks=("2021-01", "2021-04", "2021-07", "2021-10", "2022-01", "2022-04"))  # c719
AX_CODE = dict(view="date", span=("1975", "2030"), ticks=("1980", "1990", "2000", "2010", "2020", "2030"))   # ca20 決まり
AX_SALE = dict(view="date", span=("2022-05-10", "2022-08-10"), ticks=("2022-06", "2022-07", "2022-08"))     # cc20 土地の売却
SIGNS = ("約3週間前", "約1週間前", "約17時間前", "約9時間前", "約3時間前")                            # c523 の並び
ALL_SIGNS = ("約3週間前", "約1週間前", "約17時間前", "約9時間前", "約9分前", "約6分前", "1:16:27", "1:17:49", "1:22:14")   # c622

AXI.update({
    # ── 建物の歩み
    "build": dict(k="span", a="1979", b="1981", t="設計と建設", rec="AC p2023"),
    "done": dict(k="pt", at="1981", t="完成", rec=["TR p1005", "AC p2023"]),
    "y40": dict(k="br", a="1981", b="2021", rec=["MIN18 p4107", "GJ p3005"]),
    # ⚠️ 下見：右へ振ると「40年の点検の期限」が画面の右の外へ出た＝左へ（2018年の札の上の段）
    "due": dict(k="pt", at="2021", t="40年の点検の期限", rec=["MIN18 p4107", "GJ p3005"], anchor="end"),
    "fix": dict(k="span", a="1996", b="1997", t="補修", rec="TR p1441"),
    # ⚠️ 門番 check_axis：2018年（調査）と2021年（期限・崩落）は約90画素＝札を左右へ振る（真ん中だと2021年の線が2018年の札を貫いた）
    "survey": dict(k="pt", at="2018-10-08", fmt="y", t="調査の報告", rec="MC18 p4001", anchor="end"),
    # ⚠️ 門番 check_axis：括弧 br の rec は両端の値の記録に合うこと（片方の頁だけだと「1981 の rec が合わない」で止まった）
    "y15": dict(k="br", a="1981", b="1996", rec=["TR p1236", "TR p1005"]),
    "rehab": dict(k="span", a="1996", b="1997", t="大改修", rec=["TR p1236", "TR p1441"]),
    "y25": dict(k="br", a="1996", b="2021-06-24", rec=["TR p1441", "A12 p5101"]),
    # ⚠️ 下見：右へ振ると「2021年6月」が画面の右の外へ出た（c318・c918）＝左へ
    "fall": dict(k="pt", at="2021-06-24", fmt="ym", t="崩落", rec="A12 p5101", c="ALERT", anchor="end"),
    # ── 報告のあと（AX_REP・AX_21）
    "rep": dict(k="pt", at="2018-10-08", t="調査の報告", rec=["MC18 p4001", "GJ p3020"], anchor="start"),
    "mtg": dict(k="pt", at="2018-11-15", t="理事会", rec=["MIN18 p4106", "GJ p3020"], anchor="start"),
    "m29": dict(k="br", a="2018-10-08", b="2021-04", rec=["GJ p3021", "GJ p3020"]),
    "letter": dict(k="pt", at="2021-04", fmt="ym", t="理事長の手紙", rec="GJ p3021", anchor="end"),
    "bid": dict(k="pt", at="2021-06-11", lab=False, t="入札を開く会議（予定）", rec="GJ p3021", anchor="end"),
    "d13": dict(k="br", a="2021-06-11", b="2021-06-24", rec=["GJ p3021", "A12 p5101"]),
    # ⚠️ 下見：右へ振ると「2021年6月24日」が画面の右の外へ出た＝左へ（AX_REP では年月まで＝c401・c418 の fmt="ym"）
    "fall_d": dict(k="pt", at="2021-06-24", t="崩落", rec="A12 p5101", c="ALERT", anchor="end"),
    # ── 最後の3週間（並び）
    "s3w": dict(k="pt", at="約3週間前", t="門・プランター", rec="TR p1156"),
    "s1w": dict(k="pt", at="約1週間前", t="門・柱の水", rec="TR p1157"),
    "s17h": dict(k="pt", at="約17時間前", t="床の隙間", rec="TR p1158"),
    "s9h": dict(k="pt", at="約9時間前", t="天井の漏れ", rec="TR p1159"),
    "s3h": dict(k="pt", at="約3時間前", t="漏れが増す", rec="TR p1160"),
    "s9m": dict(k="pt", at="約9分前", t="最後の車", rec="TR p1161"),
    "s6m": dict(k="pt", at="約6分前", t="駐車場が落ちる", rec="TR p1170"),
    "s1627": dict(k="pt", at="1:16:27", t="1回目の電話", rec="TR p1177"),
    "s1749": dict(k="pt", at="1:17:49", t="2回目の電話", rec="TR p1189"),
    "s2214": dict(k="pt", at="1:22:14", t="沈みが速まる", rec="TR p1347"),
    # ── 最後の数分（AX_NIGHT・基準 1:22）
    "n22": dict(k="pt", at="1:22", t="塔が崩れる", rec="A12 p5101", c="ALERT", anchor="end"),
    "n9": dict(k="pt", at="約-9", t="最後の車", rec="TR p1161", anchor="end"),
    "n89": dict(k="pt", at="約-9〜-8", t="気になる音", rec="TR p1167", anchor="start"),
    "n7": dict(k="pt", at="約-7", t="トラブル信号", rec="TR p1169"),
    "n6": dict(k="pt", at="約-6", t="地上の駐車場が落ちる", rec="TR p1170", anchor="end"),
    "n1627": dict(k="pt", at="1:16:27", t="1回目の電話", rec="TR p1177", anchor="start"),
    "n1749": dict(k="pt", at="1:17:49", t="2回目の電話", rec="TR p1189", anchor="end"),
    "n1755": dict(k="pt", at="1:17:55", t="見張りの会社の電話", rec="TR p1190", anchor="start"),
    # ── 捜索（AX_SEARCH）・調査（AX_NIST）
    "f624": dict(k="pt", at="2021-06-24", t="崩落", rec="A12 p5101", c="ALERT", anchor="start"),
    "last": dict(k="pt", at="2021-07-20", t="最後の1人", rec="A12 p5101", anchor="end"),
    "d26": dict(k="br", a="2021-06-24", b="2021-07-20", rec="A12 p5101"),
    "team": dict(k="pt", at="2021-06-25", t="6人を送る", rec="B02 p5702", anchor="end"),
    "ann": dict(k="pt", at="2021-06-30", t="調査を発表", rec=["B02 p5702", "B01 p5605"], anchor="start"),
    "evid": dict(k="pt", at="2022-01-28", t="証拠を NIST が預かる", rec="B08 p5005", anchor="end"),
    # ── 決まり（AX_CODE）
    "cd79": dict(k="span", a="1979", b="1981", t="設計：連鎖を止める定め無し", rec=["AC p2023", "AC p2076"], c="ALERT"),
    "cd89": dict(k="pt", at="1989", t="連鎖に強くする鉄筋", rec="AC p2076"),
    "cd25": dict(k="pt", at="2025", t="今の決まり", rec="AC p2076", anchor="end"),
    # ── 土地の売却（AX_SALE）
    "sale": dict(k="pt", at="2022-06-01", t="土地の売却を認める", rec="A18 p7104", anchor="end"),
    "final": dict(k="pt", at="2022-06-24", t="和解の最終の命令", rec="A17 p7015", anchor="start"),
    # ⚠️ 下見：右へ振ると「2022年7月27日」が画面の右の外へ出た＝左へ（6月24日の札の上の段）
    "sold": dict(k="pt", at="2022-07-27", t="売却を終えたと報告", rec="A19 p7201", anchor="end"),
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
# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の棒の群 QG・棒 QB（c204・c207・c302・c315・c613・c614・c626）は `tools/fixture_ep18.py` へ
#    移した（値は1つも変えていない＝git の `2d627a2`）＝ここも門番 check_qty の表も空。19本目の棒は ⑤b で、値と頁を
#    ref/ep19/src/ep19_pages.txt に当てて入れる
QG = {}
QB = {}


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


# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の箱の型の表（書類の再現図 FORM_*＝欄の値は原文の英語・流れ図 FL_*・FLP と関数 `fl()`・
#    紙の置き場 _P1〜_P4・_O1）と並べ図の項目 CAUSE は `tools/fixture_ep18.py` へ移した（値は1つも変えていない＝git の `2d627a2`）＝
#    ここも門番 check_boxes の表も空（`cause()` は型の道具＝残す）。19本目の箱は ⑤b で足す
#    （門番 check_boxes の REC_MECH・REC_OTHER_ROLE・REC_CHIP・REC_FORM・REC_CAUSE も、回の値を門番の側に別に持つ＝§5b-88）
FLP = {}


CAUSE = {}


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
# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の資料の名 QDOC・QWHO と関数 `qrows()` は `tools/fixture_ep18.py` へ移した（値は1つも変えて
#    いない＝git の `2d627a2`）。19本目で決め所の出どころの札を使うときは、その回の QDOC・QWHO・`qrows()` をここに足す
QDOC = {}
QWHO = {}

