# -*- coding: utf-8 -*-
"""20本目（日本航空123便のリメイク・1985-08-12）の章ファイルが共通で使う小道具。

**19本目（サーフサイドのマンション崩壊のリメイク）の中身は git の `70c7e51`（この ss.py と門番の最後の版）と `0dcaa9c`（章ファイルの最後の版）にある**
（`git show 70c7e51:tools/cuts/ss.py`）。
**18本目（スレッシャー号のリメイク）の中身は git の `2d627a2`（章ファイルの空の器より前は `b11797a`）にある**
（`git show b11797a:tools/cuts/ss.py`）。**16本目（バイオントダム災害）は git の `b044b56`**（`git show b044b56:tools/cuts/ss.py`）。
15本目（リノ・エアレース2011）は `c646174`、14本目（セウォル号）は `dc6ecf4`、13本目（トルコ航空981便）は `b54ee4f`、
12本目（キャッスル・ブラボー）は `3832147`、11本目（チャレンジャー号）は `61039d2`、10本目（三豊百貨店）は `46f11b3`、
9本目（テネリフェ）は `e18b8f1`、8本目は `4c71bf0`、7本目は `ae30d49`。

🔴 **⑤b-1（2026-10-08・20本目）で空にした**＝§0b（その2）。19本目の型の値（案C の出典の表 REC_DOCS・描いてよい数・想定の札・壊れる物のカット・
縮尺を持たない上から見た絵・軸の型〈TL_NOTE・ORDER_NOTE・AX_*・SIGNS・ALL_SIGNS・AXI の項目〉・棒〈QG・QB〉・書類の再現図〈FORM_*＋紙の置き場 _P2〜_P4〉・
流れ図〈FL_*・FLP・`fl()`〉・並べ図〈CAUSE〉・決め所の出どころの札〈QDOC・QWHO・QDATE_LB・`qrows()`〉）は、門番の selftest の見本
`tools/fixture_ep19.py` へ移した（値は1つも変えていない＝git の `70c7e51` と同じ）。本番の ss は20本目の空の器（REF／EP＝ep20・
REC_PAGES＝ep20_pages.txt）。型の道具（`tailv`・`vid`・`head`・`fb`・`ax`・`qb`・`pp`・`ct`・`ce`・`rud`・`cause`・`src`・`merge`・
`check_frame_only`・`check_card_mix` ほか）と、束ごとに取り直す定数 `PANEL_AR`（19本目も 1.66 のまま）は残した。
（以下は ⑤b-1・2026-10-06＝19本目のとき）
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
🆕 下の「素材の名前」「人が写る点の扱い」は 20本目 ⑤b-2（2026-10-08）で20本目に書き直した（18本目の書きぶりは git の `70c7e51`・
16本目は `b044b56`。19本目の束の扱いは `70c7e51` の `tools/scene_jiko.py`・`qa_out/ep19_assets.py`）。

■ 素材の名前・■ 人が写る点の扱い（この回）
  写真の束＝`qa_out/ep20_assets.py build`（権利の台帳 `ref/ep20/assets.json`・画面の出典 `credits.json`・`ref/CREDITS.md` の20本目の節）：
  ・`ep20/<名>.jpg`＝報告書 62-2 の写真・付図・解説の図（旧版の取り出し `ref/ja123/` の名＝p015・f004・a1p001・kz018 …・PDL1.0・
    1ビットのスキャンの縮小＝白黒・幅 1200 以下＝`kind()` で額装）／Commons の写真（取得のファイル名＝j1_…・o1_…・CC BY 2.0／3.0）
  ・🔴 額装だけの点＝BY-SA の2点（J2・J3＝c201・c721）と引用の写真-124（c408）＝`frame_only()`。動きは**額ごと**（`fm()`・`fmove`）
  ・映像のひかえ＝`ep20/fb_<カット>.jpg`（防衛庁記録の1コマ・黒帯を外した 4:3・幅 1024＝額装＋地のぼかし）
  ・`ep20/pg<頁>.png`（文字の頁＝⑤b-7 で作る＝切り口はカットごと・下の `ptrim`）
  🔴 束が無ければ `_assets()` が止める（権利を確かめずに焼かない）。
  ・人が写る点は ルール §B2-1・§B2-2・§B2-2b（私人の顔と名前は出さない・顔だけモザイクは改変を許す権利の点だけ・
    CC BY-SA は**額装・1点1カット**・遺体の写真は使わない）→ [[feedback-jiko-photo-people-policy]]。20本目＝生存者の吊り上げは
    遠景だけ（c104＝ショット D・人は約25px）・寄り・担架・捜索・新聞・報道陣の顔は使わない（`footage.NOGO`）。自衛隊員は公的な任務。
    写真-9 は左18% を切る（⑤b-7）。私人の顔のモザイク（NEEDS_MASK）・切り落とし（PRIVATE_OUT）は今のところ0点

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep20"
EP = "ep20/"
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
#    🔴 2026-10-08（20本目 ⑤b-1）：下の値 1.66 は**今の値のまま**（git の `70c7e51` でも 1.66＝19本目の中で値は変わっていない）。§0b で空にする値ではなく、
#       束ごとに取り直す定数＝⑤b-7 で20本目の束（`python qa_out/ep20_assets.py panel` の並び）で取り直す。見本 `tools/fixture_ep19.py` には入れていない
#    ✅ 2026-10-08（20本目 ⑤b-2）に**20本目の束（79点＝報告書の写真・付図・解説の図70・Commons 9）で取り直した**。
#       `python qa_out/ep20_assets.py panel` の並びで、16:9 より縦長の側のいちばん大きな切れ目は AR 0.892（a1f003＝別添1 付図-3）→
#       1.087（kz018＝解説の図18）の 19.4ポイント＝中点 0.9897 を丸めて 0.99（次は 1.087→1.192 の 10.5・0.828→0.892 の 6.5）。
#       報告書の70点は幅 1200 以下＝MIN_FULL_W で全部が額装（1ビットのスキャン＝全画面にできない＝2本目の決め）。
#       幅 1280 以上の 4:3〜3:2（daipresents の6点 1.333・J1 1.501）は全画面。BY-SA の J2・J3 は権利で額装だけ。
#       ⚠️ 防衛庁記録（中身 4:3・実効 約544px）は全画面にしない＝ひかえの静止画を幅 1024 にして額装（`qa_out/ep20_assets.py fb`）
#       ⚠️ WIDE_AR＝3.19 になる（横長の付図 3.279 は幅 1200＝額装のまま）
PANEL_AR = 0.99                  # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝3.19（20本目）。これ超＝横長すぎ

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
    （記録映画 655×480＝額装＋地のぼかし＝映像方針 §8）。副題は**選んだショットに写っているもの**（撮影日は分からない＝年を書かない）

    🆕 19本目 ⑤b-7b（2026-10-06）：**カットまるごとのフリー素材**（clips.json の `"stock": true`）＝ひかえの静止画は
    `<回>/stock/fb_<cid>.jpg`（🔴 git に入れない＝決め⑨。Actions では `footage.fetch` が切り出したコマの1枚目から作る）
    ＝**ファイルを読まずに**箱を決める（読み込みの時点で無い＝import が落ちて門番も焼きも止まる）。幅は台帳の `dispw`（1280以上＝全画面）。
    見出し・副題は書かない（左上の「イメージ」の札と出典だけ＝写っていない物を名乗らない・`scene_jiko.full_top`）"""
    import footage as _FO
    c = _FO.CLIPS.get((_FO.USE.get(cid) or {}).get("clip")) or {}
    if c.get("stock"):
        if kw.get("t") or kw.get("s"):
            raise ValueError(f"{cid}: フリー素材のカットに見出し・副題は書かない（左上の「イメージ」と出典だけ）")
        w, h = int(c.get("dispw") or c["w"]), int(c["h"])
        if w < MIN_FULL_W or not PANEL_AR <= w / h <= WIDE_AR:
            raise ValueError(f"{cid}: フリー素材 {w}×{h} は全画面の箱に合わない（台帳の dispw を確かめる）")
        return dict(photo=f"{EP}stock/fb_{cid}.jpg", t="", s="", **kw)
    return dict(photo=fb(cid), **kind(fb(cid)), **kw)


def head(cid, until=1, **kw):
    """🆕 18本目 ⑤b-7c：映像の差し込み（頭）の intro＝カットの頭の until 行だけ `footage.USE[cid]`（head=True）の映像。
    ひかえの静止画＝記録映画は `fb_<cid>.jpg`・フリー素材は `stock/fb_<cid>.jpg`（`qa_out/<回>_assets.py fb`）。
    フリー素材は見出しを書かない（左上の「イメージ」と出典だけ）・記録映画は t と s（写っているもの）を書く"""
    import footage as _FO
    stock = (_FO.CLIPS.get((_FO.USE.get(cid) or {}).get("clip")) or {}).get("stock")
    return dict(foot=True, until=until, photo=f"{EP}stock/fb_{cid}.jpg" if stock else fb(cid), **kw)


def tailv(cid, at, **kw):
    """🆕 19本目 ⑤b-7c（2026-10-07）：映像の差し込み（尻）の tail＝カットの at 行目（0 から）を読み始める少し前から最後まで
    `footage.USE["<cid>~t"]`（tail=True）の映像。ひかえの静止画＝`fb_<cid>~t.jpg`（`qa_out/<回>_assets.py fb`）。
    記録映画は t と s（写っているもの）を書く・フリー素材は書かない（頭の映像と同じ板＝scene_jiko._foot_top）"""
    import footage as _FO
    stock = (_FO.CLIPS.get((_FO.USE.get(cid + "~t") or {}).get("clip")) or {}).get("stock")
    return dict(foot=True, at=at, photo=f"{EP}stock/fb_{cid}~t.jpg" if stock else fb(cid + "~t"), **kw)


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
            # 🆕 19本目 ⑤b-7c（2026-10-07）：`still=True`（寄らない＝build_jiko.tail_frame）・panel=True・color=1.0 で、切る・重ねる
            #   書き方が無ければ額装の約束どおり（c618＝諮問委員会の資料 p.47・映像のコマは引用）。それ以外は今までどおり止める
            tl = s["tail"]
            tw = [k for k in _BREAKS_FRAME + ("zoom", "hl") if tl.get(k) is not None]
            if not (tl.get("still") and tl.get("panel") and float(tl.get("color", 0.0)) == 1.0) or tw:
                bad.append(f"{cid}＝tail の {tail_ph}（{fo[tail_ph]}）: 尻の差し込みは寄る（端を切る）＝額装だけの点は "
                           f"still=True・panel=True・color=1.0 で切る書き方なしのときだけ{('（' + '・'.join(tw) + '）') if tw else ''}")
            seen.setdefault(tail_ph, []).append(cid)
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


# 🆕 2026-10-08（20本目 ⑤b-2）：**額ごと動かす**の書き方（`scene_jiko.fmove_at`・映像方針 §5-3）。絵は切らず・色も変えず・上に重ねず、
#    額の箱の位置と大きさだけを尺の中で動かす＝BY-SA（額装だけの点）でも使える（`check_frame_only` は fmove を止めない）。
#    門番＝`tools/check_fmove.py`（額の箱が尺の頭・真ん中・終わりで画面の外・見出し・章の札・出典・字幕の帯にかからないか）
FM_PX = 80          # 左右に流す片側の量（px）＝尺 7〜15秒で 10〜20px/秒（ゆっくり）
FM_S = 0.90         # 寄る・引くの小さい側の大きさ


def fm(kind, px=FM_PX, s=FM_S):
    """`fmove=ss.fm("in")` のように書く。in＝寄る（s→1.0）・out＝引く（1.0→s）・r＝右へ流す・l＝左へ流す（大きさ 1.0 のまま ±px）・
    u＝上へ・d＝下へ（額の高さが本体の帯いっぱい＝648px なので、大きさ s に縮めて上下の空き (1−s)×324 の内で動かす）"""
    v = max(0, round((1 - s) * 324) - 2)
    return {"in": dict(frm=(0, 0, s), to=(0, 0, 1.0)), "out": dict(frm=(0, 0, 1.0), to=(0, 0, s)),
            "r": dict(frm=(-px, 0, 1.0), to=(px, 0, 1.0)), "l": dict(frm=(px, 0, 1.0), to=(-px, 0, 1.0)),
            "u": dict(frm=(0, v, s), to=(0, -v, s)), "d": dict(frm=(0, -v, s), to=(0, v, s))}[kind]


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
# 🔴 2026-10-08（20本目 ⑤b-1・§0b）：19本目の値（出典の表 REC_DOCS＝TR・AC・TF・GJ ほか21資料・描いてよい数 ILLU_COUNTS・想定の札 ILLU_ASSUME／
#    `_A1_ASSUME`・壊れる物のカット ILLU_DESTROY_CUTS・縮尺を持たない上から見た絵の置き場 ILLU_TOP_NOSCALE）は selftest の見本
#    `tools/fixture_ep19.py` へ移した（値は1つも変えていない＝git の `70c7e51`）。20本目の値は、その型を初めて使う ⑤b のチャットで入れる
#    （空のあいだ、その型を使うカットは門番・型が止まる＝fail closed）。頁の番号の書き方・資料の名の決め方・守りの線の理由（19本目の例）は
#    移した注の側にある＝fixture_ep19 の REC_DOCS の注。`ILLU_TOP_NOSCALE` は19本目で足した表（門番 check_illu の ⑧が読む）＝空の器で残す
# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の値（出典の表 REC_DOCS・割れる時刻・時計と秒の札・描いてよい数・想定の札・壊れる物のカット・
#    潜水艦の時刻・音の輪・混ざりのつなぎ待ち）は selftest の見本 `tools/fixture_ep18.py` へ移した（値は1つも変えていない＝git の
#    `2d627a2`）。19本目の値は、その型を初めて使う ⑤b のチャットで入れる（空のあいだ、その型を使うカットは門番・型が止まる＝fail closed）。
#    頁の番号の書き方・資料の名の決め方・守りの線の理由（18本目の例）は移した注の側にある＝fixture_ep18 の案C の節の上
# 🆕 2026-10-08（20本目 ⑤b-3）：20本目の値を入れた（置き場 S1・S2・S3＝`tools/illu20.py`・門番 check_illu ㉔㉕㉖）。
#   通し頁＝`ref/ep20/make_pages20.py` の `ref/ep20/src/ep20_pages.txt`（git の外）：報告書＝印刷の頁の番号そのまま（p1〜p343・
#   p310〜p343＝別添6 CVR の OCR）・解説＝1000＋印刷の頁。台本の出典の「別添6 p.311」は報告書の印刷の頁＝「報告書 p311」と書く
REC_PAGES = REF / "src" / "ep20_pages.txt"      # make_pages20.py の出力（git の外＝手元だけ）
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    "報告書": dict(range=(1, 343), name="航空事故調査報告書（1987年）", page="print", base=0),
    "解説": dict(range=(1001, 1034), name="運輸安全委員会の解説（2011年）", page="print", base=1000),
}
# 墜落の時刻は資料で割れる（付図-1「18:56'30」・2.1 p.8「18時56分ごろ」＝台本 c421 の言い方）＝絵の札に出さない
ILLU_SPLIT_TIMES = ("18:56",)
ILLU_CROWD_UNTIL = None                     # 乗客の群れを描いてよい場面の時刻の上限（20本目は人を描かない＝None のまま）
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）＝20本目は秒の札を出さない
# 札に出してよい時計の時刻（S2 の機の印の札＝台本の語りの時刻だけ。秒まで書く札も「時:分」で照らす）
ILLU_CLOCK_OK = ("18:24", "18:25", "18:27", "18:28", "18:31", "18:46", "18:47", "18:48", "18:50", "18:53", "18:54", "18:55",
                 # 🆕 ⑤b-4：S4 の測位の点＝解説 表3 の時刻（19:15・19:21・20:42・01:00・04:39・05:00・05:33＝札は「時:分」で頭の0なし）
                 "19:15", "19:21", "20:42", "1:00", "4:39", "5:00", "5:33")
ILLU_COUNTS = {}                            # 描いてよい数＝{部品の obj の名: (数, 出典)}（20本目の S1〜S3 は数を持たない＝空）
_S3_NOTE = "模式（記録のグラフではない）"
ILLU_ASSUME = {"c312": "推定",                # 欠けた垂直尾翼と尾部胴体（報告書 p.107「詳細を特定することはできなかった」）
               "c303": _S3_NOTE, "c304": _S3_NOTE, "c305": _S3_NOTE, "c410": _S3_NOTE,   # S3 の揺れの模式（台本の画の欄の札）
               # 🆕 ⑤b-4：S5 尾部が壊れていく絵＝報告書 4.1.6 の推定（台本の画の欄「推定」の札）
               "c616": "推定", "c617": "推定", "c618": "推定", "c619": "推定", "c621": "推定", "ca05": "推定"}
# 壊れる物の部品を描いてよいカット（S1 の欠けた機体・🆕 ⑤b-4：S5 の隔壁の裂け目と開いた半分・外れる尾部と方向舵・切れる配管）
ILLU_DESTROY_CUTS = ("c312", "c616", "c617", "c618", "c619", "c621", "ca05")
ILLU_TOP_NOSCALE = {}                       # 縮尺を持たない模式の上から見た絵の置き場＝{置き場: 理由}（門番 check_illu ⑧ は縮尺の代わりに「人が0・模式の断り」を測る）
ILLU_SUB_UNTIL = None                      # 潜水艦の時刻の上限（門番 ⑮＝無ければ潜水艦を描いたカットは止まる）
ILLU_SUB_EXC = {}                           # 上の上限の例外＝{カットID: 時刻}
ILLU_SUB_STOP = None                        # 艦の絵を止めたカット（これより後に潜水艦を置かない）
ILLU_BOOM_CUTS = ()                         # 音の輪（9時18.1分の型）を置いてよいカット（門番 ⑰）
ILLU_MIX_TODO = {}                          # 混ざりの本物の側のつなぎ待ち＝{カットID: 理由}（門番 ⑦）
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
# 🔴 2026-10-08（20本目 ⑤b-1・§0b）：19本目の軸（TL_NOTE・ORDER_NOTE・AX_LIFE・AX_RUST・AX_REP・AX_21・AX_NIGHT・AX_CALL・AX_SEARCH・AX_NIST・
#    AX_CODE・AX_SALE・AX_TORCH・SIGNS・ALL_SIGNS）と部品 AXI の19本目の項目は `tools/fixture_ep19.py` へ移した（値は1つも変えていない＝
#    git の `70c7e51` と同じ）。20本目の軸は ⑤b で `AX_<名> = dict(view, span, ticks)` を足し、`AXI.update({…})` に項目を足す。
#    ⚠️ 19本目の軸の教訓（下見で札が画面の外へ出た直し・「約○分前」は時計の時刻に直さない・並び order は間隔が時間に比例しない断りつき）は
#       移した注の側にある＝fixture_ep19 の AX_*・AXI の上。並び order・基準 ref・秒まである時刻の物差しは門番 check_axis の型の側
#       （`ORDER_UNIT`・`ORDER_NOTE`・`_order_checks`）に残した
# 🆕 2026-10-10（20本目 ⑤b-5）：時間の帯4カット（c210 警報・c212 CVR の録音・c214 CVR の寄り・c519 夜と昼）。値と頁は
#   ref/ep20/src/ep20_pages.txt で当てた＝門番の側の表（check_axis.REC_AXIS）と照らされる（§5b-88）。
#   🔴 墜落の時刻 18:56 は割れる時刻（ILLU_SPLIT_TIMES＝付図-1「18:56'30」・2.1 p.8「18時56分ごろ」）＝点に出典の名（by=True）・「ごろ」
#   ⚠️ 18:24:38＝18:24:37 から「約1秒間」鳴った終わり（p88「18時24分37秒から約1秒間鳴り、26秒間中断した後18時25分04秒に再び鳴りだし」＝
#      37＋1＋26＝64秒＝18:25:04 と合う）
AX_ALARM = dict(view="clock", span=("18:24:30", "18:25:10"), ticks=("18:24:30", "18:24:40", "18:24:50", "18:25:00", "18:25:10"))  # c210
AX_CVR = dict(view="clock", span=("18:10", "19:00"), ticks=("18:10", "18:20", "18:30", "18:40", "18:50", "19:00"))                 # c212
AX_SQ = dict(view="clock", span=("18:24:30", "18:24:55"),
             ticks=("18:24:30", "18:24:35", "18:24:40", "18:24:45", "18:24:50", "18:24:55"))                                    # c214
#   ⚠️ 門番 layout：左の端を 18:00 にすると、左へ振った「18:40」の札が画面の左の外へ出た＝17:30 から
AX_DAY20 = dict(view="clock", span=("17:30", "翌11:00"), ticks=("18:00", "21:00", "翌0:00", "翌3:00", "翌6:00", "翌9:00"))       # c519
AXI.update({
    "boom": dict(k="pt", at="18:24:35", t="ドーンという音", rec="報告書 p6", c="ALERT"),
    "al1": dict(k="span", a="18:24:37", b="18:24:38", t="警報", rec="報告書 p88", c="ALERT"),
    "al_gap": dict(k="br", a="18:24:38", b="18:25:04", rec="報告書 p88"),
    "al2": dict(k="pt", at="18:25:04", t="また鳴る", rec="報告書 p88", c="ALERT", anchor="end"),
    "cvr": dict(k="span", a="18:24:12", b="18:56:28", t="残っていた録音", rec="報告書 p91", c="INST"),
    "cvr0": dict(k="pt", at="18:24:12", t="ここより前は消えていた", rec="報告書 p91", approx=True, anchor="end"),
    "boom_s": dict(k="pt", at="18:24:35", t="ドーンという音", rec="報告書 p6", c="ALERT", anchor="start"),
    "sq_cap": dict(k="pt", at="18:24:42", t="機長", rec="報告書 p311", anchor="end"),
    "sq_cop": dict(k="pt", at="18:24:47", t="副操縦士", rec="報告書 p311", anchor="start"),
    "sunset": dict(k="pt", at="18:40", t="日没", rec=["解説 p1019", "報告書 p23"], anchor="end"),
    "crash": dict(k="pt", at="18:56", t="墜落", rec="報告書 p8", c="ALERT", by=True, approx=True, anchor="start"),
    "night": dict(k="span", a="18:40", b="翌4:55", t="夜", rec="解説 p1019", c="INST"),
    "found": dict(k="pt", at="翌4:39", t="現場の確認", rec="報告書 p26", anchor="end"),
    "sunrise": dict(k="pt", at="翌4:55", t="日の出", rec="解説 p1019", anchor="start"),
    "alive": dict(k="pt", at="翌10:45", t="生存者の発見", rec="報告書 p28", approx=True, anchor="end"),
})
# 🆕 2026-10-10（20本目 ⑤b-6）：年表2つ（c815・c819＝1978年の修理の日付／c824〜c826＝修理のあとの7年）。値と頁は門番の側の表
#   （check_axis.REC_AXIS の ⑤b-6 の注＝別添1 本文 p246〜249 は文字の層が無い＝OCR `ref/ep20/src/ja_09_p15-18_ocr200.txt` で読んだ）と照らされる。
#   🔴 間の C整備（No.6C〜No.10C）の日付は報告書に無い＝点を打たない（推測で置かない）。「7回」は語りと字幕に任せ、年表は最初（No.5C＝
#      1978年7月）と最後（No.11C＝1984年11月20日〜12月5日）のあいだの括弧だけ
#   ⚠️ 同じ月の近い日（6月26日・27日）は年を省いた札（fmt="md"＝語りの細かさ）
AX_FIX78 = dict(view="date", span=("1978-06-12", "1978-07-17"),
                ticks=("1978-06-15", "1978-06-22", "1978-07-01", "1978-07-08", "1978-07-15"))                  # c815・c819
AX_7Y = dict(view="date", span=("1978-01", "1986-01"), ticks=("1978", "1980", "1982", "1984", "1986"))      # c824〜c826
AXI.update({
    "rep78": dict(k="span", a="1978-06-17", b="1978-07-11", t="羽田での修理", rec="報告書 p247", c="INST"),
    "w26": dict(k="pt", at="1978-06-26", t="L18 の作業", rec="報告書 p248", fmt="md", anchor="end"),
    "i27": dict(k="pt", at="1978-06-27", t="修理チームの検査", rec="報告書 p248", fmt="md", anchor="start"),
    "flt78": dict(k="span", a="1978-07-10", b="1978-07-11", t="飛行試験", rec="報告書 p249", c="LINE"),
    "ok78": dict(k="pt", at="1978-07-12", t="検査に合格", rec=["報告書 p249", "報告書 p18"], fmt="md", anchor="end"),
    "c5": dict(k="pt", at="1978-07", t="修理と同時の C整備", rec="報告書 p104", fmt="ym", anchor="start"),
    "c11": dict(k="span", a="1984-11-20", b="1984-12-05", t="最後の C整備", rec="報告書 p18", c="LINE"),
    "c_all": dict(k="br", a="1978-07", b="1984-12-05", rec=["報告書 p104", "報告書 p18"]),
    "fly7": dict(k="span", a="1978-07-12", b="1985-08-12", t="修理のあとの飛行", rec=["報告書 p18", "報告書 p1"], c="INST"),
    "acc85": dict(k="pt", at="1985-08-12", t="事故", rec="報告書 p1", c="ALERT", anchor="end"),
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
# 🔴 2026-10-08（20本目 ⑤b-1・§0b）：19本目の棒の群 QG・棒 QB（c408 工事の額・c617 床の沈み・ca07 柱にかけた重さ）は `tools/fixture_ep19.py` へ
#    移した（値は1つも変えていない＝git の `70c7e51` と同じ）＝ここも門番 check_qty の表も空。20本目の棒は ⑤b で、値と頁を
#    ref/ep20/src/ep20_pages.txt に当てて入れる
#    ⚠️ 棒の教訓（群の名と行の名には数字を書かない＝数は字幕・円は台本 §9 の式で換算・「〜を超える」は棒をその数まで＋注で断る・
#       記録の値でない物は棒にせず目盛りに置いて「目安」と断る）は移した注の側にある＝fixture_ep19 の QG・QB の上
QG = {}
QB = {}
# 🆕 2026-10-10（20本目 ⑤b-5）：c523 捜索に出た人（2.14.1.3 p.26 警察「8月12日 約2,500名・8月13日 約3,500名」・
#   2.14.1.4 p.27 防衛庁「8月12日 約1,000名・8月13日 約3,200名」）。🔴 数字は画面に書かない（目盛りだけ）・行の名に日付の数字を書かない
#   （12日＝事故の夜・13日＝翌日）。群は同じ尺（0〜4,000）＝警察と防衛庁を同じ物差しで比べる
QG.update({
    "pol": dict(id="pol", t="警察（人）", ticks=(0, 1000, 2000, 3000, 4000), rows=("事故の夜", "翌日")),
    "jda": dict(id="jda", t="防衛庁（人）", ticks=(0, 1000, 2000, 3000, 4000), rows=("事故の夜", "翌日")),
})
QB.update({
    "pol12": dict(k="bar", g="pol", t="事故の夜", v=2500, rec="報告書 p26", c="TICK"),
    "pol13": dict(k="bar", g="pol", t="翌日", v=3500, rec="報告書 p26", c="AMBER"),
    "jda12": dict(k="bar", g="jda", t="事故の夜", v=1000, rec="報告書 p27", c="TICK"),
    "jda13": dict(k="bar", g="jda", t="翌日", v=3200, rec="報告書 p27", c="AMBER"),
})
# 🆕 2026-10-10（20本目 ⑤b-6）：c708 回数の比べ（3.2.3.1(1) p.105「疲労亀裂進展に要する内圧の負荷回数は1万回程度と推定され、これは…修理後の
#   飛行回数…12,319回とほぼ一致する」）。🔴 数字は画面に書かない（目盛りだけ）・「1万回程度」は推定＝行の名に「（推定）」
QG.update({"cyc": dict(id="cyc", t="回数（回）", ticks=(0, 5000, 10000, 15000), rows=("亀裂の伸び（推定）", "修理後の飛行"))})
QB.update({
    "cyc_need": dict(k="bar", g="cyc", t="亀裂の伸び（推定）", v=10000, rec="報告書 p105", c="AMBER"),
    "cyc_fly": dict(k="bar", g="cyc", t="修理後の飛行", v=12319, rec="報告書 p105", c="LINE"),
})


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
# 🔴 2026-10-08（20本目 ⑤b-1・§0b）：19本目の箱の型の表（書類の再現図 FORM_*＝欄の値は原文の英語・紙の置き場 _P2〜_P4・流れ図 FL_*・FLP と関数 `fl()`・
#    並べ図の項目 CAUSE）は `tools/fixture_ep19.py` へ移した（値は1つも変えていない＝git の `70c7e51` と同じ）＝ここも門番 check_boxes の表も空
#    （`cause()` は型の道具＝残す）。20本目の箱は ⑤b で足す（門番 check_boxes の REC_MECH・REC_OTHER_ROLE・REC_CHIP・REC_FORM・REC_CAUSE も、
#    回の値を門番の側に別に持つ＝§5b-88）。
#    ⚠️ 箱の教訓（欄の値は原文の言葉のまま・欄の名は原文の文の言葉を日本語に・紙1枚に欄は4つまで・人の名前は出さない・次のカットの語りにある事は
#       書かない・欄の名が縮んだら lw を広げる・地図にする量が無いカットは書類の再現図か流れ図に替える）は移した注の側にある＝fixture_ep19 の FORM_*・FLP の上
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
# 🔴 2026-10-08（20本目 ⑤b-1・§0b）：19本目の資料の名 QDOC（名と出た時の組）・QWHO・QDATE_LB（「公表」の欄の言い換え）と関数 `qrows()` は
#    `tools/fixture_ep19.py` へ移した（値は1つも変えていない＝git の `70c7e51` と同じ）。20本目で決め所の出どころの札を使うときは、その回の
#    QDOC・QWHO（と、必要なら QDATE_LB）・`qrows()` をここに足す。
#    ⚠️ 札の教訓（名と年月を1つの値にすると札の幅〈全角12字〉でかっこの中で割れた＝別の欄に分ける・欄は4つまで・決め所の言葉は台本の★の行と
#       1字も違えない・原文照合）は移した注の側にある＝fixture_ep19 の QDOC の上
QDOC = {}
QWHO = {}

