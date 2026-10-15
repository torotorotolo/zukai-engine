# -*- coding: utf-8 -*-
"""22本目（タイタン号のリメイク）の章ファイルが共通で使う小道具。

**21本目（米国同時多発テロ〈9.11〉のリメイク・2001-09-11）の中身は git の `35fab37`（この ss.py・門番・章ファイルの最後の版）にある**
（`git show 35fab37:tools/cuts/ss.py`）。
**20本目（日本航空123便のリメイク）の中身は git の `cbf40ec`（この ss.py と門番の最後の版）と `f0095bd`（章ファイルの最後の版）にある**
（`git show cbf40ec:tools/cuts/ss.py`）。
**19本目（サーフサイドのマンション崩壊のリメイク）の中身は git の `70c7e51`（ss.py と門番の最後の版）と `0dcaa9c`（章ファイルの最後の版）にある**
（`git show 70c7e51:tools/cuts/ss.py`）。
**18本目（スレッシャー号のリメイク）の中身は git の `2d627a2`（章ファイルの空の器より前は `b11797a`）にある**
（`git show b11797a:tools/cuts/ss.py`）。**16本目（バイオントダム災害）は git の `b044b56`**（`git show b044b56:tools/cuts/ss.py`）。
15本目（リノ・エアレース2011）は `c646174`、14本目（セウォル号）は `dc6ecf4`、13本目（トルコ航空981便）は `b54ee4f`、
12本目（キャッスル・ブラボー）は `3832147`、11本目（チャレンジャー号）は `61039d2`、10本目（三豊百貨店）は `46f11b3`、
9本目（テネリフェ）は `e18b8f1`、8本目は `4c71bf0`、7本目は `ae30d49`。

🔴 **⑤b-1（2026-10-14・22本目）で空にした**＝§0b（その2）。21本目の型の値（案C の出典の表 REC_DOCS〈委員会報告・図表・スタッフ声明・NTSB 11便／175便／77便／93便・
CVR・NIST・運輸長官の証言・国立公園局・AP・法律・検視局・記念館・運輸省の監察総監の報告・RG237・NIST 1-6・委員会報告の序文・govinfo の20資料〉・割れる時刻 ILLU_SPLIT_TIMES
〈8:46:40・9:03:11・9:37:46・10:03:11〉・軸の型〈AXIS_DOCS＝NIST の2つの巻の名・AX_MORN・AX_11・AX_HIST・AX_175・AX_93・AX_ORD・AX_ALL・AX_TESTI・AX_HIT1・AX_AFTER・
AXI の項目〉・棒〈QG＝alert・faa／QB＝alert_cw・alert_911・faa11・faa175〉・原寸で見て字でないと決めた OCR の範囲 OCR_NOT_TEXT）は、門番の selftest の見本
`tools/fixture_ep21.py` へ移した（値は1つも変えていない＝git の `35fab37` と同じ）。本番の ss は22本目の空の器（REF／EP＝ep22・REC_PAGES＝ep22_pages.txt＝まだ無い。
その型を初めて使う ⑤b のチャットで作る）。型の道具（`tailv`・`vid`・`head`・`fb`・`ax`・`qb`・`pp`・`ct`・`ce`・`rud`・`cause`・`src`〈頁の無い書き方を止める拡張つき〉・`merge`・
`phl`・`pf`・`pfk`・`fm`・`mv`・`MV_Z`・`MV_IN`・`check_frame_only`〈映像の欄 use を見る拡張つき〉・`check_card_mix` ほか）と、束ごとに取り直す定数 `PANEL_AR`（21本目の値
1.02 のまま）は残した。
⚠️ 写真の束の定数 `SLIDE_MOUNT`（スライドの台紙の縁がある写真の名簿＝21本目の束の名〈`P("lc_a05_a01")` ほか〉に結んだ定数）は**今の値のまま残した**（見本に入れていない・
このチャットでは判断しない）。EP が ep22 になったので鍵は `ep22/…` の名に変わっている＝22本目の束のチャットで名簿を作り直す。それまで門番 check_photo_edge は
「名簿にあるが ref/ に無い」で止まる（黙って21本目の名簿で測らない）。`NEEDS_MASK`・`PRIVATE_OUT`・`TRIM` の頁の切り口は21本目も空（`TRIM` の頁の切り口は `pages.json` から読む）。
（以下は ⑤b-1・2026-10-12＝21本目のとき）
🔴 **⑤b-1（2026-10-12・21本目）で空にした**＝§0b（その2）。20本目の型の値（案C の出典の表 REC_DOCS〈報告書・解説・解説はじめに・建議・勧告・FAA・産経・
会見・検索〉・割れる時刻 ILLU_SPLIT_TIMES・札に出してよい時計の時刻 ILLU_CLOCK_OK・想定の札 ILLU_ASSUME／`_S3_NOTE`・壊れる物のカット ILLU_DESTROY_CUTS・
軸の型〈AX_ALARM・AX_CVR・AX_SQ・AX_DAY20・AX_FIX78・AX_7Y・AX_NEWS・AXI の項目〉・棒〈QG＝pol・jda・cyc／QB＝pol12・pol13・jda12・jda13・cyc_need・
cyc_fly〉）は、門番の selftest の見本 `tools/fixture_ep20.py` へ移した（値は1つも変えていない＝git の `cbf40ec` と同じ）。本番の ss は21本目の空の器
（REF／EP＝ep21・REC_PAGES＝ep21_pages.txt＝まだ無い。その型を初めて使う ⑤b のチャットで作る）。型の道具（`tailv`・`vid`・`head`・`fb`・`ax`・`qb`・
`pp`・`ct`・`ce`・`rud`・`cause`・`src`・`merge`・`phl`・`pf`・`pfk`・`fm`・`check_frame_only`・`check_card_mix` ほか）と、束ごとに取り直す定数 `PANEL_AR`
（20本目の値 0.99 のまま）は残した。
20本目の写真の束の定数（`TRIM` の写真-9〈p009〉の左18%＝c520・`NEEDS_MASK` の写真-14〈p014〉の顔だけモザイク＝c310・`PRIVATE_OUT` の写真-9 の
左端の白い形）は外した＝git の `f0095bd`（章ファイルの最後の版）と `cbf40ec`（この ss.py の最後の版）。
（以下は ⑤b-1・2026-10-08＝20本目のとき）
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
🆕 下の「素材の名前」「人が写る点の扱い」は21本目の束の書きぶりのまま（git の `35fab37`）＝**22本目の束のチャットで書き直す**。
（以下は 2026-10-12＝21本目のとき）下の「素材の名前」「人が写る点の扱い」は **21本目の束のチャットで書き直す**（20本目の書きぶりは git の `cbf40ec`＝`git show cbf40ec:tools/cuts/ss.py`・
18本目は `70c7e51`・16本目は `b044b56`。20本目の束の扱いは `cbf40ec` の `qa_out/ep20_assets.py`・`tools/footage.py`）。

■ 素材の名前・■ 人が写る点の扱い（この回）
  ✅ **21本目の束は ⑤b-2（2026-10-12）に作った**＝`python qa_out/ep21_assets.py build`（写真54点＋BY-SA の映像のひかえ fb_c205・権利の台帳
  `ref/ep21/assets.json`・画面の出典 `credits.json`・`ref/CREDITS.md` の21本目の節）。名前＝`ep21/<元のファイルの名>.jpg`（写真）・
  `ep21/stock/<名>.jpg`（イメージ＝c209・cb08＝束にある2点）・`ep21/fb_<カット>.jpg`（映像のひかえ）・`ep21/pg<頁>.png`（頁＝⑤b-3 から）。
  🔴 顔だけモザイクの3点（c210 の1970年の空港・c827 の追悼の場の来訪者・cb06 の保安検査の客）は**束に入れていない**＝⑤b-7 で範囲を決めて
  `qa_out/ep21_assets.py` の MASK に書き、ここの NEEDS_MASK と `ref/ep21/masked.json` を足す。BY-SA＝c204（写真）・c205（映像）は額装・無加工・
  c205 は等速・地は無地（footage.USE の `plain=True`）。
  🔴 束が無ければ `_assets()` が止める（権利を確かめずに焼かない）。
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
REF = HERE / "ref" / "ep22"
EP = "ep22/"
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
#    🔴 2026-10-12（21本目 ⑤b-1）：下の値 0.99 は**20本目の束の値のまま**（§0b で空にする値ではなく、束ごとに取り直す定数＝数なので空の器が
#       作れない。16→18本目のときの 1.10 と同じ扱い）。⑤b-7 で21本目の束（`python qa_out/ep21_assets.py panel` の並び）で取り直す。
#       それまで WIDE_AR も20本目の値（3.19）から導かれる。見本 `tools/fixture_ep20.py` には入れていない（16・18・19本目の見本も入れていない）
#    ✅ 2026-10-12（21本目 ⑤b-2）に**21本目の束（写真54点＋顔だけモザイクで保留の3点の縦横比）で取り直した**。
#       `python qa_out/ep21_assets.py panel` の並びで、16:9 より縦長の側のいちばん大きな切れ目は AR 0.788（wtc_south_1976＝縦長の塔）→
#       1.250（f15_otis_nyc_2001_11）の 46.2ポイント＝中点 1.0190 を丸めて 1.02（次は 1.333→1.441 の 10.8・1.637→1.724 の 8.8）。
#       ⚠️ 縦長の6点（1976年・1971年の塔・操縦室の扉＝イメージ）は kind() で額装になる＝映像方針 了承② 決め4「縦長の写真は全画面で上下を
#          切って縦に流す」＝⑤b-7 で章ファイルに panel を書かず cam（tilt）を明記する（kind() はファイルの縦横比だけを見る）
#       ⚠️ 映像のひかえ（fb_<cid>）は額装＝幅 1024（4:3）・全画面＝1920×1080（16:9 の WHTV 606・NARA 6171390）＝`qa_out/ep21_assets.py fb`
#       ⚠️ WIDE_AR＝3.10 になる（いちばん横長は stock/n352aa_2012 の 1.778）
#    🔴 2026-10-14（22本目 ⑤b-1）：下の値 1.02 は**21本目の束の値のまま**（§0b で空にする値ではなく、束ごとに取り直す定数＝数なので空の器が
#       作れない。16→18本目のときの 1.10 と同じ扱い）。⑤b-7 で22本目の束（`python qa_out/ep22_assets.py panel` の並び）で取り直す。
#       それまで WIDE_AR も21本目の値（3.10）から導かれる。見本 `tools/fixture_ep21.py` には入れていない（16・18・19・20本目の見本も入れていない）
#    ✅ 2026-10-14（22本目 ⑤b-2）に**22本目の束（写真と報告書の図 43点のうち、頁まるごとの3点〈研究所の報告 24-011 の図15・21・48＝⑤b-4 で
#       図と説明の行まで切る〉を除いた40点）で取り直した**。`python qa_out/ep22_assets.py panel` の並びで、16:9 より縦長の側のいちばん大きな
#       切れ目は AR 0.898（lab24011_p67_fig39）→ 1.080（ntsb_fig13_recovered_piece）の 18.2ポイント＝中点 0.9888 を丸めて 0.99
#       （次は 1.175→1.276 の 10.1・1.080→1.175 の 9.5）。
#       ⚠️ 報告書の図は幅 1280 未満が多い＝MIN_FULL_W で kind() は額装（了承② の「全面」の図＝幅 1000 以上は、章ファイルで panel を書かずに全面）
#       ⚠️ 縦長の DVIDS 2点（D342 回収船の甲板・D367 1つ目の船体＝EXIF の向きの札を当てて縦長）は kind() で額装＝了承② 決め3 の例外⑤
#          「縦長は全面で上下を切って縦に流す」＝章ファイルで cam（tilt）を明記（kind() はファイルの縦横比だけを見る）
#       ⚠️ WIDE_AR＝3.19 になる（航海日誌の細長い頁 4.47・4.94・NTSB 図17 の下 5.00 は額装）
PANEL_AR = 0.99                  # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝3.19（22本目の値から）。これ超＝横長すぎ

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
#   🔴 2026-10-12（21本目 ⑤b-1）：20本目の1点（写真-9〈`ep20/p009.jpg`・No.3エンジン・c520 だけ〉の左 18% を切る＝左端の白い形が人か物か
#      決められない）を外した＝git の `f0095bd`（章ファイルの最後の版。ss.py は `cbf40ec` でも同じ）。外した範囲は `PRIVATE_OUT` の側にも書いてあった
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


# 🆕 2026-10-11（20本目 ⑤b-7）：**頁の上の印（hl）も `pages.json` から読む**（手で写さない）。`qa_out/ep20_assets.py pages` が、
#    頁の句（文字の層）の行を頁の絵の字の帯に当てて箱を決め、字幕の句の位置から塗る割合を書く（`PAGE_HL`）
def phl(cid):
    """カットの頁の上の印＝[(字幕の行, 始めの割合, 終わりの割合, (x0, y0, x1, y1)＝頁の割合), …]。無ければ止める"""
    for v in PAGES.values():
        h = (v.get("hl") or {}).get(cid)
        if h:
            return [(int(k), float(f0), float(f1), tuple(float(x) for x in r)) for k, f0, f1, r in h]
    raise KeyError(f"{cid} の頁の上の印が無い（`qa_out/{EP[:-1]}_assets.py` の PAGE_HL に足して pages）")


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


def check_frame_only(spec, use=None):
    """継承つきの点を、切る・色を変える・重ねる型に渡しているカット／2回使っているカットを挙げる（空なら合格）。

    ⚠️ `intro=dict(photo=…)`（冒頭の秒だけ写真を全画面）も**全画面＝切る**ので、継承つきの点を渡したら止める。
    ⚠️ 写真を1点も当てていなければ照合する点が無い＝台帳を読まずに合格（`frame_only_for`）。
    🆕 2026-10-13（21本目 ⑤b-7）：額装だけの点を**映像のひかえ**として当てたカット（c205＝1999年の塔・BY-SA）は、焼く絵は映像＝
       `footage.USE` の欄も見る（寄り zoom 1.0・等速 rate 1.0・地を作らない plain=True・寄せ・止め絵・差し込みなし）。⑤b-2 の宿題
       「check_frame_only は SPEC しか見ない」（規則を書いたら門番も）。use＝selftest が渡す表（本番は footage.USE）
    """
    fo = frame_only_for(spec)
    if use is None and fo:
        import footage as _FO
        use = _FO.USE
    use = use or {}
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
        u = use.get(cid)
        if u:
            if float(u.get("zoom", 1.0)) != 1.0:
                why.append(f"映像の zoom={u.get('zoom')}（1.0 以外は切る）")
            if float(u.get("rate", 1.0)) != 1.0 or u.get("still"):
                why.append(f"映像の rate={u.get('rate')}{'・止め絵' if u.get('still') else ''}（速さを変えない＝等速）")
            if not u.get("plain"):
                why.append("映像の plain=True が無い（地のぼかしを作る＝色と切り口を変えた絵を重ねる）")
            why += [f"映像の {k}={u[k]}（寄せ・差し込みは切る）" for k in ("xbias", "bias", "head", "tail") if u.get(k)]
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


# 🆕 2026-10-13（21本目 ⑤b-7）：**全画面の静止写真の動き**＝PLAN の「動き」の語 → `cam`（2点移動＝build_jiko.cam_ends の dict の形）。
#    額装の写真は `fm`（額ごと動かす）・映像は `vid`。プリセットの "pan_r" は寄り 1.22 で寄せ 0→1＝端まで振り切る（スライドの台紙の黒い縁が入る・
#    寄りすぎ）＝冒頭 c102 の手書きの値（寄り 1.12・寄せ 0.2→0.8）を型にした。縁のある写真は下の SLIDE_MOUNT・門番 tools/check_photo_edge.py
MV_Z = 1.12         # 流す（r・l）・2点（two）の寄り
MV_IN = 1.15        # 寄る・引く（in・out）の寄った側


def mv(name, how, fx=0.5, fy=0.5, z=None, lo=1.0, span=(0.2, 0.8), to=None):
    """SPEC に `**ss.mv(P(名), "r")` と書く＝dict(cam=…)。how：
      r 右へ流す・l 左へ流す＝寄り z（既定 MV_Z）・横の寄せ span[0]→span[1]（l は逆）・縦は fy を真ん中に
      u 上へ流す・d 下へ流す＝寄り z（既定 lo）・縦の寄せ span[1]→span[0]（u）／span[0]→span[1]（d）・横は fx を真ん中に
      in ゆっくり寄る・out ゆっくり引く＝寄り lo で絵の真ん中 ↔ 寄り z（既定 MV_IN）で (fx, fy) を真ん中
        （引いた側も (fx, fy) に寄せると、寄り lo が 1.0 を超える台紙の縁のある写真で窓が端に張り付く＝門番 photo_edge の c513・⑤b-7）
      two 2点を順に寄る＝寄り z（既定 MV_Z）で (fx, fy) → to=(fx2, fy2)
    lo＝いちばん引いた側の寄り（スライドの台紙の縁がある写真は 1.06 ほど＝門番 photo_edge が測る）。(fx, fy) は切ったあとの絵の割合"""
    if how in ("r", "l"):
        f = focus(name, 0.5, fy, z or MV_Z)
        a, b = (span[0], f["bias"], f["zoom"]), (span[1], f["bias"], f["zoom"])
        return dict(cam={"from": a, "to": b} if how == "r" else {"from": b, "to": a})
    if how in ("u", "d"):
        f = focus(name, fx, 0.5, z or lo)
        a, b = (f["xbias"], span[1], f["zoom"]), (f["xbias"], span[0], f["zoom"])
        return dict(cam={"from": a, "to": b} if how == "u" else {"from": b, "to": a})
    if how in ("in", "out"):
        f0, f1 = focus(name, 0.5, 0.5, lo), focus(name, fx, fy, z or MV_IN)
        a, b = (f0["xbias"], f0["bias"], f0["zoom"]), (f1["xbias"], f1["bias"], f1["zoom"])
        return dict(cam={"from": a, "to": b} if how == "in" else {"from": b, "to": a})
    if how == "two":
        f0, f1 = focus(name, fx, fy, z or MV_Z), focus(name, to[0], to[1], z or MV_Z)
        return dict(cam={"from": (f0["xbias"], f0["bias"], f0["zoom"]), "to": (f1["xbias"], f1["bias"], f1["zoom"])})
    raise ValueError(f"mv: 動きの語 {how!r} が無い（r・l・u・d・in・out・two）")


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
#    🔴 2026-10-12（21本目 ⑤b-1）：20本目の1点（`ep20/p014.jpg`＝写真-14・c310 の白いシャツの男性の顔〈制服が無く公的な任務の人か写真から決められない〉＝
#       顔だけモザイク）を外した＝git の `f0095bd`（範囲は `qa_out/ep20_assets.py` の MASK・記録は `ref/ep20/masked.json`）
#    🔴 2026-10-13（21本目 ⑤b-7）：保留していた顔だけモザイクの3点（SEC70・SHANK15・TSA20）は2倍に拡大して測った＝**私人の分かる顔は0**
#       （制服の保安係＝公務・追悼の場の来訪者の顔 約4px の遠景・TSA20 は手前の列の客を束の段階で切り落とした＝`qa_out/ep21_assets.py` の CROP の注）
#       ＝ここは空のまま（門番 photomask の「0件」は調べた結果）
NEEDS_MASK: dict[str, str] = {}

# 🆕 2026-10-13（21本目 ⑤b-7）：**スライドの台紙の黒い縁がある写真**（名 → 何か）。全画面で流す・寄る窓が縁に入らないかを門番
#    `tools/check_photo_edge.py` が測る（縁の幅は**絵から毎回測る**＝ここには書かない）。夜空など縁でない暗い所の写真は入れない。
#    額装の写真は縁ごと見せる＝門番は見ない。⑤b-7 に束の全57点の四辺の暗い帯を測り（scratchpad `borders.py`）、構図の下見で絵を見て分けた
#    🔴 2026-10-14（22本目 ⑤b-1）：この名簿は**21本目の束の名**（LC-A05・loc_item210・logan_1973・logan_apron_1969）に結んだ定数＝今の値のまま残した（見本 `tools/fixture_ep21.py` には
#       入れていない）。EP が ep22 になったので鍵は `ep22/…` の名に変わっている＝`ref/` に無い名は門番 check_photo_edge が「名簿にあるが ref/ に無い」で止める。
#       22本目の束のチャットで名簿を作り直す（回を替えるとき空にする場所＝§0b）
#    🔴 2026-10-14（22本目 ⑤b-1・親の決め）：上の「今の値のまま残した」をやめ、**空にした**（§0b）。21本目の8＋3点は見本 `tools/fixture_ep21.py`
#       の SLIDE_MOUNT（`ep21/` の名を文字で書いた・説明は1字も変えていない＝git の `35fab37`）。check_photo_edge の selftest は見本を差して
#       21本目の c102（LC-A17）で回す。⚠️ 空のあいだ門番 check_photo_edge は「SLIDE_MOUNT が空」で止まる（fail closed）＝22本目の束の
#       チャットで、台紙の縁がある写真があれば名簿を書く（無い回なら「無い」を名簿の注で言う形に門番を直す＝⑤b-2 の宿題）
SLIDE_MOUNT: dict[str, str] = {}

# 🆕 2026-10-14（22本目 ⑤b-2）：**四辺に暗い帯があっても、台紙の縁ではない写真**（名 → 何か）＝数と絵で決めた（`python qa_out/ep22_assets.py edges`＝
#    門番の物差し `check_photo_edge.margins` で束の全43点を測り、MIN_EDGE〈1.2%〉以上の3点を帯の明るさの分け方で見た）。
#    22本目の束は DVIDS のデジタル写真・報告書の図・Commons＝スライドの走査が無い＝**SLIDE_MOUNT は空のまま**（台紙の縁のある写真は0点）。
#    門番 check_photo_edge は SLIDE_MOUNT が空のとき、束の全点を測って「暗い帯のある点がここに全部載っているか」を見る（載っていない点が出たら止める
#    ＝新しい点を見ずに「縁は無い」と言わない）。ここも空なら今までどおり「名簿が読めていない」で止める（fail closed）。§0b＝回を替えるとき空にする
SLIDE_NOT_MOUNT: dict[str, str] = {
    P("commons_titanic_wreck_bow"): "右 5% は深い海の暗い水（帯の中央値 20・95 パーセンタイル 28〜30・ばらつき 4〜5＝なだらか）＝写真の中身・額装（共同）",
    P("commons_uscg_mbi_8668382"): "下 3.5% は委員の濃い色の服と床（いちばん下の行の 95 パーセンタイル 137・ばらつき 50〜65）＝写真の中身",
    P("ntsb_fig16_wrinkle_t"): "上・右・下 5% は研究所の写真の黒い背景（明るさ 7・左から暗くなって続く）＝写真の中身（束でも切らない＝`qa_out/ep22_assets.py` の _trim_white の注）",
}

# 🆕 2026-10-13（21本目 ⑤b-7）：**原寸で見て字でないと決めた OCR の範囲**（OCR の読み置きのファイル名 → [((x0, y0, x1, y1)＝束の画素, 何か)]）。
#    `check_slide.load_ocr` がこの中に真ん中のある行を外す（外した行は「文字行と見なさなかった」の表に理由つきで出る）。
#    宣言が何の行にも当たらなければ止める（読み置きの取り直し・写真の差し替えで古くなった宣言を残さない）。§0b＝回を替えるとき空にする
#    🔴 2026-10-14（22本目 ⑤b-1・§0b）：21本目の2点（`wtc_far_1976.jpg` の左右の塔の壁面の窓の明かりの列・`flight93_memorial_aerial_2024_12.jpg` の
#       追悼の場のまわりの雪の上の木立＝⑤b-7 に門番 edges〈c421・cb18〉・slide G-13〈cb18〉が鳴った行を原寸の2倍で見て決めた）は selftest の見本
#       `tools/fixture_ep21.py` へ移した（値は1つも変えていない＝git の `35fab37`）。22本目で字でない範囲を決めたら、ここに足す
OCR_NOT_TEXT: dict[str, list] = {
}

# 🔴 2026-09-29（14本目 ⑤b-7a）：**切り出し（`TRIM`）で外した私人の範囲**（元画像の割合 x0,y0,x1,y1・何か）。
#    門番 photomask が「その写真を使う全カットの窓（`trim` か `TRIM`・冒頭の写真は切らない＝全体）がこの範囲に
#    1画素も入らない」を見る（NEEDS_MASK は元画像を直す点だけ＝切り出しで外した点を見ていなかった）。範囲は原寸で見て測った
#    🔴 2026-09-30（15本目 ⑤b-1）：14本目の2点（光化門 2018 の板・救命胴衣の列 2017 の奥の人）を外した＝git の `dc6ecf4`。
#       15本目は観客（私人）が写る写真が多い（事故の日の BY-SA・courtesy の頁）＝外す範囲は写真の束で原寸で見て書く
#    🔴 2026-10-12（21本目 ⑤b-1）：20本目の1点（`ep20/p009.jpg`＝写真-9 の左端の白い形〈x 0〜0.175・y 0.25〜0.75＝人か物か決められない〉）を外した
#       ＝git の `f0095bd`（上の `TRIM` の写真-9 の左 18% と対）
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


def pf(name, fx, fy, zoom):
    """🆕 20本目 ⑤b-7：**額装の写真**の中の点 (fx, fy)（切ったあとの絵の割合）を窓の真ん中に置く寄せ＝(xbias, bias, zoom)。
    `cam={"from": ss.pf(…), "to": ss.pf(…)}`（2点・順に寄る）に書く。箱＝絵の縦横比（額装の箱は絵の縦横比のまま＝`focus` の既定の
    箱 1920×1080 で測ると、16:9 でない絵は窓の高さを取り違える）"""
    f = focus(name, fx, fy, zoom, box=trimmed_size(name))
    return (f["xbias"], f["bias"], f["zoom"])


def pfk(name, fx, fy, zoom):
    """`pf` の dict 版＝SPEC に `**ss.pfk(…)`（cam を書かない＝既定のわずかな寄りのまま、窓の真ん中を (fx, fy) に置く）"""
    x, b, z = pf(name, fx, fy, zoom)
    return dict(xbias=x, bias=b, zoom=z)


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
# 🔴 2026-10-12（21本目 ⑤b-1・§0b）：20本目の値（出典の表 REC_DOCS＝報告書・解説・解説はじめに・建議・勧告・FAA・産経・会見・検索の9資料・割れる時刻
#    ILLU_SPLIT_TIMES＝18:56・札に出してよい時計の時刻 ILLU_CLOCK_OK・想定の札 ILLU_ASSUME／`_S3_NOTE`・壊れる物のカット ILLU_DESTROY_CUTS）は selftest の見本
#    `tools/fixture_ep20.py` へ移した（値は1つも変えていない＝git の `cbf40ec`）。21本目の値は、その型を初めて使う ⑤b のチャットで入れる
#    （空のあいだ、その型を使うカットは門番・型が止まる＝fail closed）。頁の番号の書き方・資料の名の決め方・守りの線の理由（20本目の例）は
#    移した注の側にある＝fixture_ep20 の REC_DOCS の注。ILLU_CROWD_UNTIL・ILLU_ROLES・ILLU_SEC_OK・ILLU_COUNTS・ILLU_TOP_NOSCALE・ILLU_SUB_*・ILLU_BOOM_CUTS・
#    ILLU_MIX_TODO は20本目も空のままだった表＝空の器で残す（見本の側も20本目の状態＝空として持つ）
# 🔴 2026-10-14（22本目 ⑤b-1・§0b）：21本目の値（出典の表 REC_DOCS＝委員会報告・図表・スタッフ声明・NTSB 11便／175便／77便／93便・CVR・NIST・運輸長官の証言・
#    国立公園局・AP・法律・検視局・記念館・運輸省の監察総監の報告・RG237・NIST 1-6・委員会報告の序文・govinfo の20資料・割れる時刻 ILLU_SPLIT_TIMES＝8:46:40・9:03:11・
#    9:37:46・10:03:11）は selftest の見本 `tools/fixture_ep21.py` へ移した（値は1つも変えていない＝git の `35fab37`）。22本目の値は、その型を初めて使う ⑤b のチャットで入れる
#    （空のあいだ、その型を使うカットは門番・型が止まる＝fail closed）。頁の番号の書き方（通し番号・印字の頁と PDF の頁・頁の無い資料は「名 p1」）・資料の名の決め方・
#    割れる時刻の扱いは移した注の側にある＝fixture_ep21 の REC_DOCS の注。ILLU_CROWD_UNTIL・ILLU_ROLES・ILLU_SEC_OK・ILLU_CLOCK_OK・ILLU_COUNTS・ILLU_ASSUME・
#    ILLU_DESTROY_CUTS・ILLU_TOP_NOSCALE・ILLU_SUB_*・ILLU_BOOM_CUTS・ILLU_MIX_TODO は21本目も空のままだった表＝空の器で残す（見本の側も21本目の状態＝空として持つ）
# ══════════════════════════════════════════════════════════
#  🆕 2026-10-14（22本目 ⑤b-3）：地図の型「衛星写真＋描き足し」（`tools/satmap.py`・門番 `tools/check_sat.py`）＝§0b（回を替えたら空にする）
# ══════════════════════════════════════════════════════════
#   SAT＝撮った衛星写真（`ref/ep22/eizou_build/helpers/gshot22.py`・中心 ll とズーム z は sources22.tsv の media と同じ）。
#     🔴 写真そのものは公開リポに置かない（git の外・Modal の保管庫 `jiko-assets` の `ref/ep22/photo/`＝`modal_app.pull_private`）。
#        ここに置けるのは md5 だけ＝門番が手元の絵と照らす（撮り直したら md5 と描き足しの座標を見直す）。
#     🔴 Actions は保管庫を読めない＝地図のカットは理由を出して飛ばす（`build_jiko.drop_missing_sat`）・検品画像は Modal の `qa`。
#     G06 は ⑤b-3 で撮り直した（⑤b-1 の中心 47.563,-52.705・ズーム16 は A. Harvey の基地が画の上の端の外＝2回撮って `gseam22.py`
#     ＝1回目に y 973 の継ぎ目〈A 25.5／B 0.0〉→ 2回目を採った）
#   GEO＝描き足しに使う場所。src＝報告書でその場所の名が出る所・how＝座標の出どころ（「報告書の値」か「一般の座標」）。
#     🔴 確かめていない場所に点を置かない（門番）。×は報告書の座標の場所だけ・一般の座標を使ったカットは断りに「一般の座標」
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"
SAT = {
    "G01": dict(file=f"{EP}photo/gmap_g01_north_america.png", ll=(45.0, -87.0), z=4, md5="70ff2619fdbaf91c3b1c5651b82d7c8e", credit=SAT_CREDIT),
    "G02": dict(file=f"{EP}photo/gmap_g02_newfoundland_site.png", ll=(44.6, -51.3), z=6, md5="4c9a76312ec1bb0053611ec20add3068", credit=SAT_CREDIT),
    "G03": dict(file=f"{EP}photo/gmap_g03_buffalo_newfoundland.png", ll=(45.5, -65.8), z=5, md5="57eb70a4722acc83aa5653315a0171ec", credit=SAT_CREDIT),
    "G04": dict(file=f"{EP}photo/gmap_g04_north_atlantic.png", ll=(45.0, -47.0), z=5, md5="67507f0134ae97af6abac1dcafc49299", credit=SAT_CREDIT),
    "G05": dict(file=f"{EP}photo/gmap_g05_bahamas.png", ll=(25.0, -77.0), z=7, md5="35b8c66417c27d9d68155c244a7d0337", credit=SAT_CREDIT),
    "G06": dict(file=f"{EP}photo/gmap_g06_stjohns_pier14.png", ll=(47.5675, -52.7010), z=17, md5="2ac970d434b7b1a7c735a8f334926ab7", credit=SAT_CREDIT),
}
GEO = {
    "everett": dict(ll=(47.979, -122.202), src="TSB §1.23（`OceanGate was headquartered in Everett, Washington`）", how="一般の座標（市の中心）"),
    "stjohns": dict(ll=(47.5615, -52.7126), src="TSB §1.3.1（`the Polar Prince departed St. John’s`）", how="一般の座標（港）"),
    "site": dict(ll=(41 + 44.06 / 60, -(49 + 56.54 / 60)), src="USCG p.6〈vi〉（`41° 44.06’ North; 49° 56.54’West`＝最後の位置）",
                 how="報告書の値（最後に受けた位置）"),
    "buffalo": dict(ll=(42.886, -78.878), src="NTSB p.18（`The Odysseus was in Buffalo, New York, at the time.`）", how="一般の座標（市の中心）"),
    "marsh": dict(ll=(26.541, -77.063), src="USCG p.152〈144〉（`OceanGate took their operation to Marsh Harbour, Bahamas to conduct test dives`）",
                  how="一般の座標（町）"),
    # 47回目の潜航（2019年4月17日）の海＝「リトルハーバー〈26.326, -76.999〉の沖 約10マイル・大西洋」＝東へ約16キロ（模式）
    "abaco47": dict(ll=(26.326, -76.838), src="USCG p.157〈149〉（`approximately 10 miles off Little Harbour, Great Abaco, in the Atlantic Ocean`）",
                    how="一般の座標（リトルハーバー）から東へ約16キロ（模式）"),
    # A. Harvey の基地（Pier 14・71 Water St.＝会社の頁）。NTSB 図9 と衛星写真は特徴点の照合が取れなかった（⑤b-3・SIFT の inlier 13 以下）
    #   ＝駐車場の中の位置（図9 の×）は描かず、基地のあたりを囲む（中心＝G06 の画素 (930, 270)＝住所の点 (803, 281) と岸の舗装の間）
    "harvey": dict(ll=(47.5688, -52.70121), src="USCG p.236〈228〉（`demobilized at the A Harvey Marine Base in St. John’s` ・`placed in the parking lot of the facility`）・NTSB p.36〈28〉 図9",
                   how="一般の座標（基地の住所 Pier 14・71 Water St. のあたり＝会社の頁）"),
}


def sat(code, steps, note="", **kw):
    """🆕 22本目 ⑤b-3：地図のカット（衛星写真の額装＋描き足し）の SPEC の頭。t・s は呼ぶ側で（副題に「現在の衛星写真」＝門番）。"""
    return dict(photo=SAT[code]["file"], panel=True, pw=1152, color=1.0, sat=dict(code=code, steps=steps, note=note), **kw)


REC_PAGES = REF / "src" / "ep22_pages.txt"      # `ref/ep22/make_pages22.py` の出力（git の外＝手元だけ・⑤b-3b で作った）
# 🆕 2026-10-14（22本目 ⑤b-3b）：22本目の資料の表＝3つの報告書。頁の番号＝**通し番号**（`ref/ep22/make_pages22.py` が同じ番号で REC_PAGES を書く）：
#    USCG＝米沿岸警備隊 海難調査委員会の報告書の PDF の頁（台本の「USCG p.71〈63〉」→「USCG p71」）・NTSB＝1000＋PDF の頁（「NTSB p.36〈28〉」→「NTSB p1036」）・
#    TSB＝カナダ運輸安全委員会の報告書（ウェブの頁＝頁なし）＝**節**で書く（「TSB §1.3.1」「TSB §付録B」「TSB §脚注13」＝`illu.sec_num`・page="sec"）。
#    画面の出典の行＝`illu.rec_line`（pdf＝「PDF 71頁」・sec＝「1.3.1節」「付録B」）。⚠️「NTSB」は「TSB」を含む＝parse_rec は長い名から当てる
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    "USCG": dict(range=(1, 335), name="米沿岸警備隊 海難調査委員会の報告書（2025年）", page="pdf", base=0),
    "NTSB": dict(range=(1001, 1087), name="米運輸安全委員会の報告書（2025年）", page="pdf", base=1000),
    "TSB": dict(range=(100_000_000, 999_999_999), name="カナダ運輸安全委員会の報告書（2026年）", page="sec", base=0),
}
ILLU_SPLIT_TIMES = ()                       # 資料で割れる時刻＝画面に時計・時刻の札として出さない
ILLU_CROWD_UNTIL = None                     # 乗客の群れを描いてよい場面の時刻の上限
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）
ILLU_CLOCK_OK = ()                          # 札に出してよい時計の時刻（門番 check_illu ⑤）
ILLU_COUNTS = {}                            # 描いてよい数＝{部品の obj の名: (数, 出典)}（門番 check_illu ③）
ILLU_ASSUME = {}                            # 想定の札を出すカット＝{カットID: 札の言葉}（門番 check_illu ④）
ILLU_DESTROY_CUTS = ()                      # 壊れる物の部品を描いてよいカット（門番 check_illu ⑫＝空なら全部止める）
ILLU_TOP_NOSCALE = {}                       # 縮尺を持たない模式の上から見た絵の置き場＝{置き場: 理由}（門番 check_illu ⑧ は縮尺の代わりに「人が0・模式の断り」を測る）
ILLU_SUB_UNTIL = None                      # 潜水艦の時刻の上限（門番 ⑮＝無ければ潜水艦を描いたカットは止まる）
ILLU_SUB_EXC = {}                           # 上の上限の例外＝{カットID: 時刻}
ILLU_SUB_STOP = None                        # 艦の絵を止めたカット（これより後に潜水艦を置かない）
ILLU_BOOM_CUTS = ()                         # 音の輪（9時18.1分の型）を置いてよいカット（門番 ⑰）
ILLU_MIX_TODO = {}                          # 混ざりの本物の側のつなぎ待ち＝{カットID: 理由}（門番 ⑦）
ILLU_MIX_BUNDLE = REF / "credits.json"      # 束ができたか（混ざりのつなぎ待ちの終わり）を見るファイル

# 🔴 2026-10-06（19本目 ⑤b-1）：空にした（18本目は割れる時刻・出典の名つきの点を使わなかった＝空のままの値＝`tools/fixture_ep18.py`）
# 🔴 2026-10-14（22本目 ⑤b-1・§0b）：21本目は NIST の2つの巻の名（`{"NIST": "NIST（本編）", "NIST 1-6": "NIST（別冊）"}`＝ca12 の割れる時刻の札で2つの巻を見分ける）を
#    入れた→ `tools/fixture_ep21.py` へ移して空にした（値は1つも変えていない＝git の `35fab37`）
AXIS_DOCS = {}

# 軸（カットをまたいで同じ軸を使う＝前のカットの点を past で沈めて続ける）。回ごとに `AX_<名> = dict(view, span, ticks)` を足す
# 🔴 2026-10-04（18本目 ⑤b-1）：16本目の軸（AX_DAY・AX_EVE＝10月9日の時刻の帯／AX_ANS・AX_ENEL・AX_PERMIT・AX_Y3・AX_EXP・AX_MERLIN・
#    AX_MODEL・AX_Y63・AX_INQ・AX_DEC・AX_CIV＝年表）・部品 AXI の16本目の項目・関数 `dot()` は `tools/fixture_ep16.py` へ移した
#    （値は1つも変えていない）。15本目の軸（AX_HIST ほか）は `tools/fixture_ep15.py`。18本目の軸は ⑤b で足す。
#    ⚠️ 軸の教訓は移した注の側にある（年だけの値は年の真ん中に置く＝fixture_ep15 の AXI の上／札が枠の端・章の札・見出しに触れた
#       layout の直し＝fixture_ep16 の AX_*・AXI の上）。⚠️ 割れる時刻の印（split）は ILLU_SPLIT_TIMES の時刻だけ・出典の名つき

# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
AXI = {}

# 🆕 2026-10-14（22本目 ⑤b-3b）：第2〜3章の時間の帯。時刻は**ニューファンドランドの夏時間**（TSB 脚注13＝協定世界時−2.5時間・米国の2つの報告書も同じ時計）。
#   色＝**役の色**（だれがしたか＝母船 SHIP・会社 COMPANY・潜水艇 SUB・壊れた＝ALERT）／2段の帯は段＝調べの色（米沿岸警備隊 USCG・カナダ INST）。
#   門番 check_axis が記録の表（REC_AXIS・REC_ROLE・LANE_ROLE）で値・頁・色を照らす（§5b-88＝ここを書き換えると鳴る）
#   AX_MORN22＝6月18日の朝（c306・c312・c313）。原文 TSB §1.3.1「arrived … at 0400 on 18 June」「At 0534, OceanGate held a briefing」「At 0545, the 5 people
#     boarding the Titan … were weighed」「From 0600 to 0800, OceanGate used rigid inflatable boats」「All 5 people were on board the Titan by 0820」
#     「At 0824 … closed the Titan’s forward dome … using its internal life support system」「At 0859 … a scheduled 5-minute pause」「At 0904 … fill the LARS’s ballast tanks」
#     ⚠️ 9:04 は次のカット（c314）の語りの時刻＝括弧の端だけ（札を出さない）。past で沈めるだけの点は札なし（`lab=False, t=""`＝21本目の教訓）
AX_MORN22 = dict(view="clock", span=("3:30", "9:40"), ticks=("4:00", "5:00", "6:00", "7:00", "8:00", "9:00"))
#   AX_END＝10時40分〜51分（c407・c416）。原文 TSB 付録A「10:41:07.2 SST ack no niskin」「10:42:01.4 T a」「10:47:26.9 T dropped two wts」・
#     NTSB p.17（p1017）「At 1048, the Polar Prince sent a message back to acknowledge」「At 1049, the Polar Prince sent the Titan a “lost tracking” message but received no response」
#     ⚠️ 門番 layout：左の端 10:40 だと 10:41:07 の札（左へ振る）が枠の外へ出た＝10:39:30
AX_END = dict(view="clock", span=("10:39:30", "10:51"), ticks=("10:40", "10:42", "10:44", "10:46", "10:48", "10:50"))
#   AX_1047＝10時47分の秒（c411・c412）＝米沿岸警備隊の記録。原文 USCG p35「At approximately 10:47:02 a.m., the TITAN sent a message」
#     「At approximately 10:47:08 a.m., the TITAN transmitted its final ping」「At approximately 10:47:09 a.m., the TITAN submersible suffered a catastrophic implosion」
#     「At 10:47:11 a.m. … heard a sound described … as a “bang”」「At 10:47:26 a.m. … received a message from the TITAN」（approximately の3つは「ごろ」＝REC_APPROX）
AX_1047 = dict(view="clock", span=("10:46:50", "10:47:34"), ticks=("10:47:00", "10:47:10", "10:47:20", "10:47:30"))
#   AX_TWO＝2段の帯（c413〜c415）＝上の段 米沿岸警備隊（USCG p35〜p37）・下の段 カナダの調べ（TSB §1.3.2「At 1047:26.903 … a message appeared」
#     「At 1047:32.066, … received the last automated position update」「it was calculated that the sound was generated at 1047:32.3」「At 1047:34.522, a loud sound
#     … reverberated through the hull of the Polar Prince」・§2.1「5.397 seconds after the text message … appeared」）。🆕 秒の小数（axis の clock＝「10:47:26.9」）。
#     ⚠️ 32.066・34.522 は画面に小数1桁（「10:47:32.1」「10:47:34.5」）＝門番の幅は書いた桁の半分（±0.05秒）に原文の値が入る
_TU, _TC = "米沿岸警備隊の調べ", "カナダの調べ"
#     ⚠️ 門番 axis：左の端 10:46:58 だと 10:47:02 の札（左へ振る）が段の名の列にかかった＝10:46:50
AX_TWO = dict(view="tiers", span=("10:46:50", "10:47:38"), ticks=("10:47:00", "10:47:10", "10:47:20", "10:47:30"), lanes=(_TU, _TC))
AXI.update({
    # 朝（AX_MORN22）
    "arr18": dict(k="pt", at="4:00", t="母船が現場に着く", rec="TSB §1.3.1", c="SHIP"),
    "brief": dict(k="pt", at="5:34", t="潜航の説明", rec="TSB §1.3.1", c="COMPANY", anchor="end"),
    "weigh": dict(k="pt", at="5:45", t="重さを量る", rec="TSB §1.3.1", c="COMPANY", anchor="start"),
    "rib": dict(k="span", a="6:00", b="8:00", t="小舟で台へ", rec="TSB §1.3.1", c="COMPANY"),
    "aboard": dict(k="pt", at="8:20", t="5人が乗り終える", rec="TSB §1.3.1", c="SUB", anchor="end"),
    "seal": dict(k="pt", at="8:24", t="艇の中の生命維持へ", rec="TSB §1.3.1", c="SUB", anchor="start"),
    "pause": dict(k="pt", at="8:59", t="作業を止めて確かめる", rec="TSB §1.3.1", c="COMPANY", anchor="end"),
    "p5": dict(k="br", a="8:59", b="9:04", t="", rec="TSB §1.3.1"),   # ⚠️ geom_gap：括弧の札「5分」が 8:59 の札と縦の線に触れた＝札なし（5分は副題と語り）
    # 10時40分〜51分（AX_END）
    "nisk": dict(k="pt", at="10:41:07", t="母船「了解」", rec="TSB §付録A", c="SHIP", anchor="end"),
    "a42": dict(k="pt", at="10:42:01", t="潜水艇「a」", rec="TSB §付録A", c="SUB", anchor="start"),
    "quiet": dict(k="span", a="10:42:01", b="10:47:26.9", t="文字のやりとりが途切れる", rec="TSB §付録A", c="LINE"),
    "q5": dict(k="br", a="10:42:01", b="10:47:26.9", t="5分あまり", rec="TSB §付録A"),
    "ack48": dict(k="pt", at="10:48", t="「受け取った」と返す", rec="NTSB p1017", c="SHIP", anchor="end"),
    "lost49": dict(k="pt", at="10:49", t="「追跡を失った」", rec="NTSB p1017", c="SHIP", anchor="start"),
    # 10時47分の秒（AX_1047）
    "snd": dict(k="pt", at="10:47:02", t="文を送る", rec="USCG p35", c="SUB", approx=True, anchor="end"),
    "ping": dict(k="pt", at="10:47:08", t="最後の位置を送る", rec="USCG p35", c="SUB", approx=True, anchor="end"),
    "imp": dict(k="pt", at="10:47:09", t="壊れる", rec="USCG p35", c="ALERT", approx=True, big=True, anchor="start"),
    "bang": dict(k="pt", at="10:47:11", t="「バン」の音", rec="USCG p35", c="SHIP", anchor="start"),
    "recv": dict(k="pt", at="10:47:26", t="文が届く", rec=["USCG p35", "USCG p36"], c="SHIP", anchor="start"),
    # 2段の帯（AX_TWO）
    "u02": dict(k="pt", at="10:47:02", t="送った", rec="USCG p35", c="USCG", lane=_TU, approx=True, anchor="end"),
    "u09": dict(k="pt", at="10:47:09", t="壊れた", rec="USCG p35", c="ALERT", lane=_TU, approx=True, big=True, anchor="start"),
    "u26": dict(k="pt", at="10:47:26", t="文が届いた", rec=["USCG p35", "USCG p36"], c="USCG", lane=_TU, anchor="end"),
    "u32": dict(k="pt", at="10:47:32", t="最後の位置が届いた", rec="USCG p37", c="USCG", lane=_TU, anchor="start"),
    "c269": dict(k="pt", at="10:47:26.9", t="画面に出た", rec="TSB §1.3.2", c="INST", lane=_TC, anchor="end"),
    "c321": dict(k="pt", at="10:47:32.1", t="最後の位置", rec="TSB §1.3.2", c="INST", lane=_TC, anchor="end"),
    # ⚠️ 門番 layout：右へ振ると右の端（x 1848）の外へ出た＝左へ（10:47:26.9 の札と重なる分は上の段へ振られる）
    "c323": dict(k="pt", at="10:47:32.3", t="壊れた", rec=["TSB §1.3.2", "TSB §2.1"], c="ALERT", lane=_TC, big=True, anchor="end"),
    "c345": dict(k="pt", at="10:47:34.5", t="船体に音", rec="TSB §1.3.2", c="INST", lane=_TC, anchor="end"),
    "c54": dict(k="br", a="10:47:26.9", b="10:47:32.3", t="約5.4秒", rec="TSB §2.1"),
    "lane_c": dict(k="lane", lane=_TC, rec="TSB §1.3.2", c="INST"),
    "lane_u": dict(k="lane", lane=_TU, rec="USCG p35", c="USCG"),
})
# 🆕 2026-10-15（22本目 ⑤b-4）：第4・6・7章の帯（門番 check_axis の REC_AXIS・REC_ROLE が値・頁・役の色を照らす）
#   AX_PM22＝6月18日の昼から夜（c503〜c506）。原文 USCG p38「as of approximately 10:47 a.m., there was a loss of communication」・
#     TSB §1.3.3「the estimated resurfacing time was approximately 3 hours and 13 minutes (at 1500)」「At 1500 … commenced the 3-hour surface search」
#     「At 1634 … the master of the Polar Prince called the Horizon Maritime Services Ltd. shore-based emergency team」「By 1800, the surface search had found no signs」
#     「At 1855, the master of the Polar Prince called the Joint Rescue and Coordination Centre (JRCC) in Halifax」・USCG p39（船長の陳述「At (6:27 p.m.) … communications
#     with JRCC were shortly thereafter cut-off」）・TSB §2.5「8 hours and 8 minutes after communication and tracking had been lost」
AX_PM22 = dict(view="clock", span=("10:20", "19:30"), ticks=("11:00", "13:00", "15:00", "17:00", "19:00"))
#   AX_CLASS＝船級（c715）。NTSB p1022「when he was hired in 2016, the company planned to class the submersible」・p1023「In 2018, OceanGate abandoned classing efforts」
AX_CLASS = dict(view="date", span=("2015-06-01", "2019-06-01"), ticks=("2016", "2017", "2018", "2019"))
#   AX_Y18＝2018年（c807〜c809）。USCG p149「On January 23, 2018, OceanGate fired the Director of Marine Operations」「filed a retaliation complaint with … (OSHA) on
#     February 6, 2018」・p150「OceanGate filed a lawsuit against him on June 25, 2018」・p151「On December 13, 2018 … withdrew his SPA complaint」・
#     TSB §1.12.1「because he held different opinions from the CEO on the safety of the Titan」・NTSB p1048「“like Swiss cheese”」
AX_Y18 = dict(view="date", span=("2017-12-10", "2019-01-10"), ticks=("2018-01-01", "2018-04-01", "2018-07-01", "2018-10-01", "2019-01-01"))
#   AX_Y19＝2019年（c817・c818）。USCG p164「On July 26, 2019, OceanGate fired the Director of Engineering」・TSB §1.12.1「On 15 October, the Titan was tested in the
#     Deep Ocean Test Facility」「Following that test, further cracks and delamination were found」「On 18 November, the Titan’s depth rating was reduced … not to dive
#     below 2000 m」「This carbon fibre cylinder was not subsequently used for any more dives」。札は語りの細かさ（年月＝fmt="ym"）
AX_Y19 = dict(view="date", span=("2019-05-20", "2019-12-31"), ticks=("2019-06-01", "2019-07-01", "2019-08-01", "2019-09-01", "2019-10-01", "2019-11-01", "2019-12-01"))
AXI.update({
    # 6月18日の昼から夜（AX_PM22）
    "lost47": dict(k="pt", at="10:47", t="連絡と追跡が途絶える", rec="USCG p38", c="LINE", approx=True, anchor="start"),
    "surf15": dict(k="pt", at="15:00", t="浮上の見込み", rec="TSB §1.3.3", c="COMPANY", anchor="end"),
    "srch": dict(k="span", a="15:00", b="18:00", t="海面の捜索", rec="TSB §1.3.3", c="SHIP"),
    "call1634": dict(k="pt", at="16:34", t="陸の班へ電話", rec="TSB §1.3.3", c="SHIP"),
    "none18": dict(k="pt", at="18:00", t="手がかりなし", rec="TSB §1.3.3", c="SHIP", anchor="end"),
    "cut1827": dict(k="pt", at="18:27", t="電話がすぐ切れる", rec="USCG p39", c="SHIP", anchor="end"),
    "rcc1855": dict(k="pt", at="18:55", t="救難の当局へ", rec="TSB §1.3.3", c="SHIP", anchor="end"),
    "b88": dict(k="br", a="10:47", b="18:55", t="8時間8分", rec="TSB §2.5"),
    # 船級（AX_CLASS）
    "cls16": dict(k="pt", at="2016", t="船級を取るつもり", rec="NTSB p1022", c="COMPANY", fmt="y"),
    "cls18": dict(k="pt", at="2018", t="船級をあきらめる", rec="NTSB p1023", c="COMPANY", fmt="y"),
    # 2018年（AX_Y18）＝元運航部長の動きは LINE（会社の外の1人＝役の色を持たない）
    "fire18": dict(k="pt", at="2018-01-23", t="運航部長を解任", rec="USCG p149", c="COMPANY", fmt="md", anchor="start"),
    "why18": dict(k="chips", at="2018-01-23", chips=["安全の考えの違い"], rec="TSB §1.12.1"),
    "osha18": dict(k="pt", at="2018-02-06", t="労働安全衛生局へ", rec="USCG p149", c="LINE", fmt="md", anchor="start"),
    "swiss": dict(k="chips", at="2018-02-06", chips=["“like Swiss cheese”"], rec="NTSB p1048"),
    "sue18": dict(k="pt", at="2018-06-25", t="会社が訴える", rec="USCG p150", c="COMPANY", fmt="md"),
    "wd18": dict(k="pt", at="2018-12-13", t="申し立てを取り下げ", rec="USCG p151", c="LINE", fmt="md", anchor="end"),
    # 2019年（AX_Y19）
    "fire19": dict(k="pt", at="2019-07-26", t="技術部長を解任", rec="USCG p164", c="COMPANY", fmt="ym"),
    "test19": dict(k="pt", at="2019-10-15", t="加圧の試験", rec="TSB §1.12.1", c="COMPANY", fmt="ym", anchor="end"),
    "crk19": dict(k="chips", at="2019-10-15", chips=["亀裂と剥離"], rec="TSB §1.12.1"),   # ⚠️ geom_gap：「…がさらに」だと11月の項目の札と重なった
    "der19": dict(k="pt", at="2019-11-18", t="潜る深さを下げる", rec="TSB §1.12.1", c="COMPANY", fmt="ym", anchor="start"),
    "last19": dict(k="chips", at="2019-11-18", chips=["それきり潜らず"], rec="TSB §1.12.1"),
})
# 🆕 2026-10-15（22本目 ⑤b-5）：第8〜9章の帯（門番 check_axis の REC_AXIS・REC_ROLE が値・頁・役の色を照らす）
#   AX_Y20＝2020〜21年（c908）。NTSB p1028「between November 2020 and January 2021」（月だけの記録＝月の値で置く）・
#     p1062「OceanGate did not build or test any new sub-scale models using the co-bonding process」
#     🔧 ⑤b-5 の試し焼き：目盛りを「2020-07-01」と日まで書くと「1日／7月」と出て年が読めなかった＝月で書く（「7月／2020年」）
AX_Y20 = dict(view="date", span=("2020-06-01", "2021-05-31"), ticks=("2020-07", "2020-10", "2021-01", "2021-04"))
#   AX_J22＝2022年7月（ca14）。NTSB p1036「On July 15, 2022 (mission 3, dive 80)」・USCG p235「On July 19, 2022, the TITAN and its crew commenced Dive 81」・
#     TSB 付録B（2022-07-22 の行＝3840）・NTSB p1051「The last of these dives (dive 83) took place on July 23, 2022」・p1036「2,954 meters (9,692 feet) on the final dive」
AX_J22 = dict(view="date", span=("2022-07-12", "2022-07-26"), ticks=("2022-07-13", "2022-07-15", "2022-07-17", "2022-07-19", "2022-07-21", "2022-07-23",
                                                                     "2022-07-25"))
#   AX_2223＝2022年7月〜2023年6月（ca26）。USCG p290「should have been a red flag to stop all dive operations」・NTSB p1060「after dive 82 and before the casualty
#     dive 11 months later (dive 88)」・TSB 付録B（2022-07-22・2023-06-18 の行）
AX_2223 = dict(view="date", span=("2022-06-01", "2023-07-31"), ticks=("2022-07", "2022-10", "2023-01", "2023-04", "2023-07"))   # 🔧 同上（年をまたぐ）
AXI.update({
    # 2020〜21年（AX_Y20）
    "build20": dict(k="span", a="2020-11", b="2021-01", t="実物大の筒を作る", rec="NTSB p1028", c="COMPANY"),
    #   ⚠️ 門番 layout：項目の札（chips）にすると帯の札「実物大の筒を作る」と重なり、線が「1月」の目盛りを貫いた＝点にする
    "nomodel": dict(k="pt", at="2021-01", t="模型は作らず", rec="NTSB p1062", c="COMPANY", fmt="ym", anchor="start"),
    # 2022年7月（AX_J22）＝80回目は大きな音（赤）・81〜83回目は潜水艇
    "d80": dict(k="pt", at="2022-07-15", t="80回目", rec="NTSB p1036", c="ALERT", fmt="md", anchor="end"),
    "d81": dict(k="pt", at="2022-07-19", t="81回目", rec="USCG p235", c="SUB", fmt="md", anchor="end"),
    "d82": dict(k="pt", at="2022-07-22", t="82回目", rec="TSB §付録B", c="SUB", fmt="md", anchor="end"),
    "d83": dict(k="pt", at="2022-07-23", t="83回目", rec="NTSB p1051", c="SUB", fmt="md", anchor="start"),
    "d83m": dict(k="chips", at="2022-07-23", chips=["別の場所", "2,954メートル"], rec="NTSB p1036"),
    # 2022年7月〜2023年6月（AX_2223）
    "bang15": dict(k="pt", at="2022-07-15", t="80回目の音", rec="NTSB p1036", c="ALERT", fmt="md", anchor="end"),
    "flag": dict(k="chips", at="2022-07-15", chips=["止めるべき赤信号"], rec="USCG p290"),
    "last82": dict(k="pt", at="2022-07-22", t="最後の深い潜航", rec="TSB §付録B", c="SUB", fmt="md", anchor="start"),
    "occ23": dict(k="pt", at="2023-06-18", t="事故の潜航", rec="TSB §付録B", c="ALERT", fmt="md", anchor="end"),
    "m11": dict(k="br", a="2022-07-22", b="2023-06-18", t="約11か月", rec="NTSB p1060"),
})


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
# 🔴 2026-10-12（21本目 ⑤b-1・§0b）：20本目の軸（AX_ALARM・AX_CVR・AX_SQ・AX_DAY20＝時間の帯／AX_FIX78・AX_7Y・AX_NEWS＝年表）と部品 AXI の20本目の項目
#    （boom・al1・al_gap・al2・cvr・cvr0・boom_s・sq_cap・sq_cop・sunset・crash・night・found・sunrise・alive／rep78・w26・i27・flt78・ok78・c5・c11・
#    c_all・fly7・acc85／al_q・al_f・inf・boe24・pub・del26・min25・now）は `tools/fixture_ep20.py` へ移した（値は1つも変えていない＝git の `cbf40ec` と同じ）。
#    21本目の軸は ⑤b で `AX_<名> = dict(view, span, ticks)` を足し、`AXI.update({…})` に項目を足す。
#    ⚠️ 20本目の軸の教訓（左の端を 18:00 にすると左へ振った札が画面の外へ出た・近い日は年を省いた札 fmt="md"・割れる時刻 18:56 の点は出典の名＋「ごろ」・
#       月だけの記録は月の値で置く〈日を足さない〉・右の端を延ばして右上の章の札を避ける・点と同じ所に置くと縦の線が札を貫く）は移した注の側にある
#       ＝fixture_ep20 の AX_*・AXI の上
# 🔴 2026-10-14（22本目 ⑤b-1・§0b）：21本目の軸（AX_MORN・AX_11・AX_HIST・AX_175・AX_93・AX_ORD・AX_ALL＝時間の帯と年表／AX_TESTI＝2段の帯／AX_HIT1＝1機目の衝突の3つの値／
#    AX_AFTER＝その後の年表）と部品 AXI の21本目の項目（67項目＝dep11〜dep93・hj11〜nine11・cs60〜day911・code175〜upd93・hq93〜hit77・t916〜rep04 ほか）は
#    `tools/fixture_ep21.py` へ移した（値は1つも変えていない＝git の `35fab37` と同じ）。22本目の軸は ⑤b で `AX_<名> = dict(view, span, ticks)` を足し、
#    `AXI.update({…})` に項目を足す。
#    ⚠️ 21本目の軸の教訓（1分約11画素の帯は札が重なる＝左右に振り分ける・past で沈めるだけの点は札を出さない〈`ss.ax("dep175", t="", lab=False)`〉・右の端を右上の章の札を避けて
#       延ばす・左の端は左へ振った札が画面の外へ出ない所に・目盛りを割れる時刻の印〈軸の下へ 22px 伸びる〉に合わせない〈geom_gap〉・近い点は同じ所に置くと縦の線が札を貫く・
#       ×の印〈x=True・札なし〉は記録が「誤り」とした値だけ〈REC_WRONG〉・年表の札は語りの細かさ〈fmt="ym"〉）は移した注の側にある＝fixture_ep21 の AX_*・AXI の上


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
    recs = recs if isinstance(recs, (list, tuple)) else [recs]
    # 🆕 ⑤c'（2026-10-13・21本目）：頁の無い書き方（"AP"・"国立公園局"・"運輸長官の証言"）は parse_rec が拾わず、出典の行から黙って落ちた
    #   （c709・c814・c815・c832 が空・c710 は証言が欠けた）＝頁の無い資料も「名 p1」（REC_DOCS の range）で書く。拾えない rec は止める
    bad = [r for r in recs if not illu.parse_rec(r)]
    if bad:
        raise ValueError(f"ss.src：{bad} から資料と頁が読めない＝出典の行から落ちる（頁の無い資料は「名 p1」・運輸長官の証言は「p8001」＝REC_DOCS の range）")
    return illu.rec_line(recs).replace("出典：", "", 1)


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
# 🔴 2026-10-12（21本目 ⑤b-1・§0b）：20本目の棒の群 QG（pol・jda・cyc）・棒 QB（pol12・pol13・jda12・jda13・cyc_need・cyc_fly＝c523 捜索に出た人・
#    c708 回数の比べ）は `tools/fixture_ep20.py` へ移した（値は1つも変えていない＝git の `cbf40ec` と同じ）＝ここも門番 check_qty の表も空。
#    21本目の棒は ⑤b で、値と頁を ref/ep21/src/ep21_pages.txt に当てて入れる
#    ⚠️ 棒の教訓（群の名と行の名には数字を書かない＝数は字幕・円は台本 §9 の式で換算・「〜を超える」は棒をその数まで＋注で断る・
#       記録の値でない物は棒にせず目盛りに置いて「目安」と断る）は移した注の側にある＝fixture_ep19 の QG・QB の上。20本目の棒の教訓
#       （数字は画面に書かない〈目盛りだけ〉・行の名に日付の数字を書かない・「1万回程度」は推定＝行の名に「（推定）」・群は同じ尺にして比べる）は
#       fixture_ep20 の QG・QB の注
# 🔴 2026-10-14（22本目 ⑤b-1・§0b）：21本目の棒の群 QG（alert・faa）・棒 QB（alert_cw・alert_911・faa11・faa175＝c317 すぐ飛び立てる待機の基地・
#    c516 乗っ取りから FAA が知るまで）は `tools/fixture_ep21.py` へ移した（値は1つも変えていない＝git の `35fab37` と同じ）＝ここも門番 check_qty の表も空。
#    22本目の棒は ⑤b で、値と頁を ref/ep22/src/ep22_pages.txt に当てて入れる
#    ⚠️ 21本目の棒の教訓（数字は画面に書かない〈目盛りだけ〉・行の名に日付の数字を書かない・行の名に便の数字を書かない〈「北棟の便」「南棟の便」と呼ぶ〉・
#       時刻の帯にしない点は棒にする）は移した注の側にある＝fixture_ep21 の QG・QB の注
QG = {}
QB = {}
# 🆕 2026-10-14（22本目 ⑤b-3b）：c210 参加費（USCG p64「rising from $105,129 in 2021 to $250,000 for both 2022 and 2023」・TSB §1.23「the cost for
#   1 passenger to join was up to 250 000 U.S. dollars」）＝万ドルの目盛り・行の名は年だけ（日付の行＝同じ色でよい・check_qty の DATE_ROW）。色＝会社
#   ⚠️ 門番 qty：群の名に数字を書かない（「1人の」は副題へ）
QG.update({"fee": dict(id="fee", t="参加費（万ドル）", ticks=(0, 10, 20, 30), rows=("2021年", "2022年", "2023年"))})
QB.update({
    "fee21": dict(k="bar", g="fee", t="2021年", v=10.5129, rec="USCG p64", c="COMPANY"),
    "fee22": dict(k="bar", g="fee", t="2022年", v=25, rec="USCG p64", c="COMPANY"),
    "fee23": dict(k="bar", g="fee", t="2023年", v=25, rec=["USCG p64", "TSB §1.23"], c="COMPANY"),
})
# 🆕 22本目 ⑤b-3b：c302 乗客として乗せられる人（TSB §1.20.1.2「it was permitted to carry up to 12 passengers」「on the occurrence voyage, it was carrying
#   24 passengers」）。上限＝目安の灰・この航海＝会社の色（乗客に数える24人は会社の関係の人＝c303 と同じ色）
QG.update({"pax": dict(id="pax", t="乗客として乗る人（人）", ticks=(0, 10, 20, 30), rows=("貨物船の決まりの上限", "この航海"))})
QB.update({
    "pax_lim": dict(k="bar", g="pax", t="貨物船の決まりの上限", v=12, rec="TSB §1.20.1.2", c="TICK"),
    "pax_now": dict(k="bar", g="pax", t="この航海", v=24, rec="TSB §1.20.1.2", c="COMPANY"),
})


# 🆕 2026-10-15（22本目 ⑤b-4）：c518 生命維持を始めてからの時間（TSB §1.2.1「enough oxygen to last approximately 96 hours based on an occupancy of 5 people」・
#   §2.5「located the Titan debris 98 hours and 16 minutes after life support had been started on the Titan, which exceeded the 96 hours」）。
#   目盛りは24時間ごと（1日）。色＝酸素は潜水艇・見つかるまでの時間はカナダの調べの値（語り「カナダの調べで」）
#   ⚠️ 門番 echo：群の名「生命維持を始めてから（時間）」は語り「生命維持を始めてから98時間16分後」の写し
QG.update({"o2": dict(id="o2", t="生命維持の開始からの時間", ticks=(0, 24, 48, 72, 96, 120), rows=("酸素の目安", "見つかるまで"))})
QB.update({
    "o2_lim": dict(k="bar", g="o2", t="酸素の目安", v=96, rec=["TSB §1.2.1", "TSB §2.5"], c="SUB"),
    "o2_find": dict(k="bar", g="o2", t="見つかるまで", v=98 + 16 / 60, rec="TSB §2.5", c="INST"),
})
# 🆕 22本目 ⑤b-4：c708 設計書の安全率（TSB §1.12.1「had a safety factor of 2.19 with grade 5 titanium end domes and a safety factor of 2.21 with carbon fibre end
#   domes」「OceanGate had a goal of 2.25 for the safety factor」・脚注45「that required a minimum safety factor of 1.5」）。行の名に数字を書かない
QG.update({"sf": dict(id="sf", t="安全率（倍）", ticks=(0, 1, 2, 3), rows=("チタンのドームのとき", "炭素繊維のドームのとき", "会社の目標", "規格の最低"))})
QB.update({
    "sf_ti": dict(k="bar", g="sf", t="チタンのドームのとき", v=2.19, rec="TSB §1.12.1", c="COMPANY"),
    # ⚠️ 門番 qty ⑪：同じ群の棒は色を ΔE 25 以上離す（4本とも会社の橙だと鳴った）＝チタン 橙・炭素繊維 黄（ΔE 29）・目標 白・最低 灰
    #    （第6章は白黒＝灰 TICK が #aca69a に置き換わる＝書類の色 DOC とは ΔE 21 で鳴った・白 INK_W とは 27）
    "sf_cf": dict(k="bar", g="sf", t="炭素繊維のドームのとき", v=2.21, rec="TSB §1.12.1", c="AMBER"),
    "sf_goal": dict(k="bar", g="sf", t="会社の目標", v=2.25, rec="TSB §1.12.1", c="INK_W"),
    "sf_min": dict(k="bar", g="sf", t="規格の最低", v=1.5, rec="TSB §脚注45", c="TICK"),
})
# 🆕 2026-10-15（22本目 ⑤b-5）：c917 2つ目の筒の安全率（TSB §1.12.2「OceanGate also changed its safety factor to 1.25, which aligned with the safety factor
#   established by the International Organization for Standardization」・§1.15「the calculated safety factor of 3.05, which was greater than the required 1.25」
#   「the calculated safety factor was 1.11, which did not meet the required safety factor of 1.25」）。何メートルでの値かは書かない（映像方針）。
#   色＝基準は会社・長さの向きはカナダの研究所の計算・周りの向きは届かない＝赤
QG.update({"sf2": dict(id="sf2", t="安全率（倍）", ticks=(0, 1, 2, 3, 4), rows=("会社の基準", "長さの向き", "周りの向き"))})
QB.update({
    "sf2_req": dict(k="bar", g="sf2", t="会社の基準", v=1.25, rec=["TSB §1.12.2", "TSB §1.15"], c="COMPANY"),
    "sf2_ax": dict(k="bar", g="sf2", t="長さの向き", v=3.05, rec="TSB §1.15", c="INST"),
    "sf2_ci": dict(k="bar", g="sf2", t="周りの向き", v=1.11, rec="TSB §1.15", c="ALERT"),
})
# 🆕 22本目 ⑤b-5：ca20 浅い所（10〜300m）のひずみの傾きが全体より何%大きいか（TSB §1.10.10.1「on the 05 August 2021 dive for the 10 m to 300 m range,
#   the strain slope was found to be 21% greater」「on 19 July 2022 dive … 98% greater than the slope for the entire dive profile」）。行の名は年だけ
#   ⚠️ 門番 qty：行の名「2021年の潜航」は画面の数字（§5b-9）＝日付は語りにある＝「前の年の夏」（2021年8月5日）・「音のあと」（2022年7月19日＝81回目）
QG.update({"slope": dict(id="slope", t="浅い所の傾きの増え（%）", ticks=(0, 25, 50, 75, 100), rows=("前の年の夏の潜航", "音のあとの潜航"))})
QB.update({
    "slope21": dict(k="bar", g="slope", t="前の年の夏の潜航", v=21, rec="TSB §1.10.10.1", c="TICK"),
    "slope22": dict(k="bar", g="slope", t="音のあとの潜航", v=98, rec="TSB §1.10.10.1", c="INST"),
})


def qb(name, **kw):
    return dict(QB[name], **kw)


# 人の形（1つ＝1人）＝**14本目 c204〜c206 だけの例外**（ルール §C-1 #59・亡くなった方の数には使わない）。
#   15本目は使わない＝空のまま（門番 check_qty が PEOPLE_CUTS の外の人の形を止める）
# 🆕 2026-10-14（22本目 ⑤b-3b）：c303 だけ（映像方針 了承②「会社の関係24＝橙・乗組員17＝水色の人の印」）＝母船に乗っていた41人（TSB §1.3.1「There were 41 people
#   on board the Polar Prince in total: 24 people associated with OceanGate and 17 Polar Prince crew members」）。🔴 亡くなった方を分けない・後の章で戻して灰色にしない
PEOPLE_ORDER = (("乗客に数える人（会社の関係）", 24), ("母船の乗組員", 17))
PEOPLE_SETS = {}
PEOPLE_REC = {"乗客に数える人（会社の関係）": ["TSB §1.3.1", "TSB §1.20.1.1"], "母船の乗組員": "TSB §1.3.1"}
PEOPLE_CUTS = ("c303",)     # 🔴 門番 check_qty がこの外の人の形を止める（亡くなった方の数に使わない）


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

