# -*- coding: utf-8 -*-
"""26本目（タイタニック号沈没事故・1912-04-14〜15・北大西洋・ホワイト・スター・ライン・英国の審問〈1912年〉と英国の海難調査局 MAIB の再評価〈1992年〉ほかの報告の動画）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-30（27本目 八田與一容疑者の事件の ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `54b15e5e` と同じ）
  ・`cuts/ss.py` の26本目の値＝案C の出典の表（REC_DOCS＝G1 英国の審問の報告〈S. Doc. 933〉・G2 MAIB 1992・G7 ほか）・原文の道（REC_PAGES＝`ref/ep26/src/ep26_pages.txt`＝
    手元にある〈git の外〉）・割れる時刻（ILLU_SPLIT_TIMES＝1:10・1:15・2:00）・群れを描いてよい時刻の上限（ILLU_CROWD_UNTIL＝2:20）・置いてよい役割（ILLU_ROLES＝
    乗組員の影・乗客の群れ）・時計の時刻（ILLU_CLOCK_OK 9）・描いてよい数（ILLU_COUNTS）・縮尺を持たない上から見た絵の置き場（ILLU_TOP_NOSCALE＝K5）・
    衛星写真の地図（SAT＝G01〜G04・GEO＝寄港地と行き先・タイタニック号とカリフォルニアン号の位置・氷の知らせの15点）・航路の線（SAT_LINES＝gc・mesaba）と出典の断り（SAT_LINE_NOTE）・
    写真の束の定数（顔だけ升目にする点 NEEDS_MASK・台紙の縁 SLIDE_MOUNT・台紙の縁でない暗い帯の名簿 SLIDE_NOT_MOUNT・字でない暗い帯 OCR_NOT_TEXT）。
    26本目も空のままだった表（ILLU_SEC_OK・ILLU_ASSUME・ILLU_DESTROY_CUTS・ILLU_SUB_*・ILLU_BOOM_CUTS・ILLU_MIX_TODO・AXIS_DOCS・AXI・QG・QB・PEOPLE_*・QDOC・QWHO・
    SAT_NONE〈None〉）も、26本目の状態として持つ（17・23〜25本目の見本と同じ考え方）
  ・門番の記録の表（check_mech＝REC_M26〈図解 `mech26.py` の記録の値＝船と人の名と色・灯の色・値と比例・モールスの符号・時計・出さない言葉・原文の句と頁〉／
    check_illu＝REC_K26〈置き場 K1〜K6＝`illu26.py` の記録の値・㊽〉と、26本目の案C の正しい場面のカット K26_CUTS〈18カット〉）。
    check_axis・check_qty・check_boxes・check_sat・check_photo_edge・check_photo_mask は26本目で足した表が無い（check_sat の地図は ss の SAT／GEO、
    check_photo_edge の名簿は ss の SLIDE_*＝上）＝この見本の GATES に載せない
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を26本目の実物でも確かめている（check_illu の ㊽・check_mech の m26）＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は27本目の空の器にした
  （fixture_ep14〜ep25・ep17 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep26
      fixture_ep26.apply(sys.modules[__name__])   # その処理の中だけ ss・この門番の記録の表が26本目になる
      try: …（検算）
      finally: fixture_ep26.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14〜25本目・17本目の見本と重ねるとき（check_mech）は
      fixture_ep26.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと27本目の画に26本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。⚠️ ほかの回の見本（fixture_ep25 ほか）の積み荷とは別＝それぞれの restore で戻す
■ 注意:
  ⚠️ 見本の原文 `ref/ep26/src/ep26_pages.txt`（check_illu の `_pages26()`・cuts/ss.REC_DOCS の通し頁・check_mech の `_m26_page`）は
     **手元にだけある**（git の外）。Actions には無い＝check_illu の `_pages26()` は None を返し、check_mech の `_m26_page` は句の照合を飛ばす。
     ⚠️ `_pages26()` は原文を覚える（lru_cache）＝見本を差し込む前後で `_pages26.cache_clear()`（check_illu の selftest_ep26 がする）
  ⚠️ 26本目の selftest のうち、**章ファイルの SPEC を読むもの**は 2 つ：check_illu の `selftest_ep26`（置き場 K1〜K6 の正しい場面＝K26_CUTS の18カット）・
     check_mech の `_selftest_m26`（m26 のカット＝図解）。どちらも `apply(gate)`＋`apply_cuts()`（26本目の章ファイルを git の `CUTS_SHA`＝`54b15e5e` から
     取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ26本目に入れ替える・git が無い所では止める＝fail closed）を使う（`restore()` で27本目へ戻る・LIFO）。
  ⚠️ 26本目の章ファイルは git の版の `tools/cuts/ss.py`（EP＝`ep26/`・26本目の値）ごと取り出して読む＝写真の名 `P("…")` は `ep26/…` のまま（本番の ss の EP は ep27）。
     ただし `ss.vid`・`ss.head`・`ss.tailv` は本番の **`footage.CLIPS`・`footage.USE`**（と `footage.PILLAR`）を引く（NOAA 2004 の残骸の映像 N04 の13区間と
     Pexels の8カット＝台帳 `ref/ep26/clips.json`）＝本番の footage は27本目の表なので、`cuts_ep26()` は章ファイルを読む間だけ footage の3つを
     26本目の表（台帳 `ref/ep26/clips.json`・使う区間 `USE` と黒帯の割合 `PILLAR` は git の `54b15e5e` の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}` の
     2文を取り出して評価）に差し、読み終えたら戻す（`_footage26`＝17本目の `_footage17`・24本目の `_footage24`・25本目の `_footage25` と同じ）。
     26本目の footage の値は**ここに写していない**（git の `54b15e5e` が正本）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep26/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は26本目の道を持つ。
  ⚠️ `NEEDS_MASK`・`SLIDE_MOUNT`・`SLIDE_NOT_MOUNT`・`OCR_NOT_TEXT` の鍵と `SAT` の `file` は **`ep26/` の名を文字で書いた**（本番の ss は `P(…)`・`f"{EP}…"` で組んでいた＝
     EP が ep27 になると `ep27/…`〈無い名〉に化ける。fixture_ep17・ep22〜ep25 と同じ扱い）。説明の文は1字も変えていない（値＝git の `54b15e5e` の ss を評価した結果と同じ）。
  ⚠️ `SAT`・`GEO` は本番の ss で `SAT = {}`・`GEO = {}` のあとに `SAT.update(…)`・`GEO.update(…)` を足す形だった＝その文をそのまま写した（評価した値は同じ）。
     `SAT_LINES`・`SAT_LINE_NOTE` は本番の ss で2回代入していた（空の器 → 26本目 ⑤b-3 の値）＝2つの文を並びのまま写した（評価した値＝あとの値）。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝26本目は 1.11）は見本に入れない（16〜25本目・17本目の見本も入れていない）＝本番の ss は今の値のまま残し、27本目の束で取り直す。
  ⚠️ 写真の束の定数のうち `TRIM`（`pages.json` から読む＝REF が替われば追う）・`PRIVATE_OUT`・`NG_PHOTOS` は見本に入れない。
  ⚠️ 型として本番に残した＝ss の関数（`sat`・`ax`・`qb`・`P`・`page`・`vid`・`head`・`tailv`・`mv`・`mvz`・`tcam`・`check_frame_only`・`check_card_mix`・`src`）・`SAT_CREDIT`・
     check_mech の `_m26_min`・`_M26_PAGES`・`_m26_page`・`_m26_q`・`judge_m26`（⚠️ `_m26_page` は原文の道〈`ref/ep26/src/…`〉を直書きしている＝17本目の `_m17_page`・
     24本目の `_m24_page`・25本目の `_m25_page` と同じ例外）・check_illu の `K26_PLACES`・`K26_MARK`・`NUM_KM26`・`CLOCK26`・`QUOTE26`・`ROLE26`・`_nz26`・`_pages26`・
     `judge_k26`（表が空なら理由を出して止める入口）・描く側の型 `tools/illu26.py`・`tools/mech26.py`・`titan_fig.m26`（どれも cuts.ss の26本目の値を読まない）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep26"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から（git の `54b15e5e` の ss.py の代入文をそのまま写した・`P("…")` だけ `"ep26/….jpg"`・`f"{EP}…"` だけ `"ep26/…"` の文字に）
# ══════════════════════════════════════════════════════
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"   # 型の定数（本番の ss に残した・SAT を組むための名＝SS_NAMES に入れない）

NEEDS_MASK: dict[str, str] = {
    "ep26/s9_648.jpg": "c323・c820＝米国上院の公聴会の部屋（議員・証人・記者・傍聴の人が写真から分けられない＝顔の分かる30人・⑤c' で1人足した）",
    "ep26/s2_054.jpg": "c208・c509＝ボート甲板を歩く乗客4人（右の後ろ姿の人はそのまま）",
    "ep26/s1_057.jpg": "c219＝タイタニック号の甲板の人たち（下半分の顔の分かる10人）",
    "ep26/s6_383.jpg": "c707＝カルパチア号の横のボートの生存者（上から・こちらを向く顔11）",
    "ep26/s6_427.jpg": "c714＝カルパチア号の甲板の生存者（ほとんど後ろ姿・前と横を向く顔5）",
    "ep26/s3_671.jpg": "c636・c801・c800card＝英国の審問に着く長と息子の右を歩く女の人（私人・⑤c' で足した）",
}
SLIDE_MOUNT: dict[str, str] = {
    "ep26/s3_577.jpg": "LOC（Bain）のガラス乾板＝四辺の黒い縁と外の白い余白（c711）",
    "ep26/s3_698.jpg": "LOC（Bain）のガラス乾板＝左と下の黒い縁と白い余白（上はネガの字ごと束で切った・c819）",
    "ep26/s6_427.jpg": "LOC（Bain）のガラス乾板＝左右と下の黒い縁（c714）",
    "ep26/s6_480.jpg": "BnF（Rol）のガラス乾板＝左の黒い縁に整理番号の字（c104・c641・cb04）",
    "ep26/s6_619.jpg": "LOC の台紙（灰色の紙と外の黒い縁・2枚の小さな写真＝c713 は1枚目を章ファイルで切る）",
    "ep26/s7_594.jpg": "BnF（Rol）のガラス乾板＝左の黒い縁に整理番号の字（c808）",
    "ep26/s12_913.jpg": "LOC（National Photo）のガラス乾板＝四辺の黒い縁と外の白い余白（ca09）",
}
SLIDE_NOT_MOUNT: dict[str, str] = {
    "ep26/s11_716.jpg": "NOAA 2003 の深海の暗い水（上・右・下 5%）＝写真の中身",
    "ep26/s2_033.jpg": "下 5% は船体の黒い外板＝写真の中身",
    "ep26/s2_206.jpg": "下 2.4% は無線室の机の陰＝写真の中身",
    "ep26/s5_358.jpg": "下 2.6% は夜明けの暗い海＝写真の中身",
    "ep26/s6_379.jpg": "上・下 5% は夜の空と船体の陰＝写真の中身",
    "ep26/s4_n06.jpg": "左 1.9% は電報の用紙の黒い枠の線＝紙面の中身",
}
OCR_NOT_TEXT: dict[str, list] = {
    # 🆕 2026-10-28（26本目 ⑤b-7）：1912年の本の頁の氷原の写真（c318・c817）の手前の暗い海面＝OCR が「を を 第 朝 を…」と読んだ行
    #   （箱 1247,811〜1482,841）を原寸の切り出し（scratchpad `b7/c318_ocr.jpg`）で見た＝網点（半調）の模様で字は無い。門番 slide G-13 が c318 で鳴った
    "s5_362.jpg": [((1240, 800, 1490, 850), "氷原の手前の暗い海面の網点（半調）の模様＝字でない")],
}
SAT = {}
GEO = {}
SAT_LINES = {}
SAT_LINE_NOTE = ""
SAT.update({
    "G01": dict(file="ep26/photo/gmap_g01_atlantic.png", ll=(46.0, -34.0), z=4, md5="f8cd894a49cd015b7d5c1ae3c0d364ad", credit=SAT_CREDIT),
    "G02": dict(file="ep26/photo/gmap_g02_ice.png", ll=(41.72, -49.75), z=8, md5="1f1cd59513d12287790bbe7aff512912", credit=SAT_CREDIT),
    "G03": dict(file="ep26/photo/gmap_g03_titanic.png", ll=(41.765, -50.07), z=10, md5="18ceaf98a4453d8a410381d51af170d3", credit=SAT_CREDIT),
    "G04": dict(file="ep26/photo/gmap_g04_californian.png", ll=(41.88, -50.03), z=10, md5="b236c9aa9328c8ee34013bccd721730b", credit=SAT_CREDIT),
})
GEO.update({
    # 寄港地と行き先（G1 p.33 THE ROUTE FOLLOWED）＝一般の座標（Wikidata の P625）
    "southampton": dict(ll=(50.9067, -1.4044), src="G1 p.33（`The Titanic left Southampton on Wednesday, April 10`）", how="一般の座標（Wikidata Q79848＝市）"),
    "cherbourg": dict(ll=(49.6333, -1.6000), src="G1 p.33（`after calling at Cherbourg`）", how="一般の座標（Wikidata Q3667188＝町）"),
    "queenstown": dict(ll=(51.8510, -8.2967), src="G1 p.33（`proceeded to Queenstown`）", how="一般の座標（Wikidata Q733093＝今のコーヴ）"),
    "fastnet": dict(ll=(51.3933, -9.6049), src="G1 p.33（`from the Fastnet Light, off the southwest coast of Ireland`）", how="一般の座標（Wikidata Q3067133＝1904年からの灯台）"),
    "newyork": dict(ll=(40.7128, -74.0061), src="G1 p.33（`and from this point on to New York`）", how="一般の座標（Wikidata Q60＝市）"),
    "turning": dict(ll=(42.0, -47.0), src="G1 p.33（`a point in latitude 42° N. and 47° W. (sometimes termed the “turning point”)`）", how="報告書の値（曲がり角）"),
    # タイタニック号の位置（G2＝MAIB 1992 p.3・p.7＝頁の画像で読んだ値。文字の層は緯度経度が空白）
    "collision": dict(ll=(41 + 47 / 60, -(49 + 55 / 60)), src="G2 p.3・p.7（衝突の位置＝41°47′N 49°55′W・沈んだ位置から海流で逆算した推定）",
                      how="報告書の値（推定）"),
    "wreck": dict(ll=(41 + 43.6 / 60, -(49 + 56.9 / 60)), src="G2 p.3・p.7（ボイラーと船尾の位置＝41°43′.6N 49°56′.9W・1985年の発見）",
                  how="報告書の値（残骸）"),
    "cqd": dict(ll=(41 + 46 / 60, -(50 + 14 / 60)), src="G2 p.7・G1 p.85（タイタニック号が無線で送った位置＝41°46′N 50°14′W）", how="報告書の値（無線の位置）"),
    # カリフォルニアン号の位置の2つの見方（G2 p.3・p.11）＝どちらも「あたり」の点（見えたかの線は描かない）
    "cal_inv": dict(ll=(41 + 50 / 60, -(50 + 7 / 60)), src="G2 p.3（調査官＝41°50′N 50°07′W あたり・`probably further East and only 5 to 7 miles off`）",
                    how="報告書の値（調査官の見方）"),
    "cal_dep": dict(ll=(42.0, -(50 + 9 / 60)), src="G2 p.3・p.11（次長＝42°00′N 50°09′W あたりかやや北・`between 17 and 20 miles from TITANIC`）",
                    how="報告書の値（次長の見方）"),
    # 4月14日の氷の知らせ（G1 p.35〜37 ICE MESSAGES RECEIVED）
    "ice_caronia_w": dict(ll=(42.0, -51.0), src="G1 p.35（`bergs, growlers, and field ice in 42° N., from 49° to 51° W.`）", how="報告書の値（範囲の西の端）"),
    "ice_caronia_e": dict(ll=(42.0, -49.0), src="G1 p.35（`bergs, growlers, and field ice in 42° N., from 49° to 51° W.`）", how="報告書の値（範囲の東の端）"),
    "ice_baltic": dict(ll=(41 + 51 / 60, -(49 + 52 / 60)), src="G1 p.36（`Athenai reports passing icebergs`…`in latitude 41° 51′ N., longitude 49° 52′ W.`）",
                       how="報告書の値"),
    "ice_amerika": dict(ll=(41 + 27 / 60, -(50 + 8 / 60)), src="G1 p.36（`Amerika passed two large icebergs in 41° 27′ N., 50° 8′ W.`）", how="報告書の値"),
    "ice_californian": dict(ll=(42 + 3 / 60, -(49 + 9 / 60)), src="G1 p.37（`latitude 42° 3′ N., longitude 49° 9′ W. Three large bergs`）", how="報告書の値"),
})
SAT_LINES = dict(
    # ファストネット灯台 → 曲がり角（北緯42度・西経47度）の大圏の弧（G1 p.33 `followed the arc of a great circle`）＝球の上で両端を結んで8つに割った点（計算）
    gc=((51.393, -9.605), (50.946, -14.934), (50.261, -20.135), (49.351, -25.165), (48.232, -29.992), (46.919, -34.595), (45.432, -38.964),
        (43.786, -43.097), (42.0, -47.0)),
    # メサバ号の知らせの範囲（北緯42度〜41度25分・西経49度〜50度30分＝G1 p.37 `latitude 42° N. to 41° 25′ N., longitude 49° to longitude 50° 30′ W.`）の四角
    mesaba=((42.0, -50.5), (42.0, -49.0), (41 + 25 / 60, -49.0), (41 + 25 / 60, -50.5), (42.0, -50.5)),
)
SAT_LINE_NOTE = "航路は英国の審問の報告 p.33 の道すじを描き直した模式"
SAT_NONE = None
REC_PAGES = REF / "src" / "ep26_pages.txt"      # 部品の出典（`rec=`）を当てる原文（git の外＝手元だけ）＝`ref/ep26/make_pages26.py` が作る
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    "G1": dict(range=(1, 88), name="英国の審問の報告（1912年）", page="print", base=0),
    "G2": dict(range=(2001, 2030), name="英国 海難調査局の再評価（1992年）", page="print", base=2004),
    "G7": dict(range=(20001, 21170), name="米国上院の公聴会の記録（1912年）", page="pdf", base=20000),
    "T1": dict(range=(1, 25700), name="英国の審問の証言（書き起こし・有志のサイト）", page=None, base=0, text=False),
    # 🆕 2026-10-28（⑤b-6・図解 第6〜9章）：原文の通し頁を持たない資料（`text=False`＝頁の照合はしない・画面は名だけ・書き方は「名 p1」）。
    #   G2送＝MAIB の送り状（PDF 3頁＝印刷の頁の前＝「G2 p2003」と書くと画面が「-1頁」になる）
    "G2送": dict(range=(2003, 2003), name="英国 海難調査局の再評価（1992年）の送り状", page=None, base=0, text=False),
    "T3": dict(range=(1, 1), name="米国上院の報告（書き起こし・有志のサイト）", page=None, base=0, text=False),
    "G4": dict(range=(1, 1), name="米国の法（無線の当直の改正・1912年）", page=None, base=0, text=False),
    "G5": dict(range=(1, 1), name="米国の無線の法（遭難の通信・1912年）", page=None, base=0, text=False),
    "G6": dict(range=(1, 1), name="米国の法（船の無線・1910年）", page=None, base=0, text=False),
    "U1": dict(range=(1, 1), name="米国沿岸警備隊の歴史の記事", page=None, base=0, text=False),
}
ILLU_SPLIT_TIMES = ("1:10", "1:15", "2:00")
ILLU_CROWD_UNTIL = "2:20"                   # 群れ（タイタニック号の甲板の乗客）は沈没（2:20＝タイタニック号の時計）より前の場面だけ
ILLU_ROLES = dict(sprite=("crew",), crowd=("passengers",))   # 型紙の影＝乗組員（役職だけ）・群れ＝乗客（数えられない形）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）＝26本目は秒の札を出さない
ILLU_CLOCK_OK = ("23:00", "0:00", "0:20", "0:45", "1:00", "1:40", "2:05", "2:40", "4:10")
ILLU_COUNTS = {                             # 描いてよい数＝{部品の obj の名: (数, 出典)}（門番 check_illu ③）
    "seat": (40, "G1 p52（this was an emergency boat with a carrying capacity of 40）"),
    "filled": (12, "G1 p51（No. 1 certainly left with only 12）"),
    "flare": (3, "G1 p58（He got no reply, but the vessel fired three more white rockets）"),
}
ILLU_ASSUME = {}                            # 想定の札を出すカット＝{カットID: 札の言葉}（門番 check_illu ④）
ILLU_DESTROY_CUTS = ()                      # 壊れる物の部品を描いてよいカット（門番 check_illu ⑫＝空なら全部止める）
ILLU_TOP_NOSCALE = {"K5": "人を描かない席の印の模式（1号艇）"}   # 縮尺を持たない模式の上から見た絵の置き場（門番 check_illu ⑧ は「人が0・模式の断り」を測る）
ILLU_SUB_UNTIL = None                      # 潜水艦の時刻の上限（門番 ⑮＝無ければ潜水艦を描いたカットは止まる）
ILLU_SUB_EXC = {}                           # 上の上限の例外＝{カットID: 時刻}
ILLU_SUB_STOP = None                        # 艦の絵を止めたカット（これより後に潜水艦を置かない）
ILLU_BOOM_CUTS = ()                         # 音の輪（9時18.1分の型）を置いてよいカット（門番 ⑰）
ILLU_MIX_TODO = {}                          # 混ざりの本物の側のつなぎ待ち＝{カットID: 理由}（門番 ⑦）
ILLU_MIX_BUNDLE = REF / "credits.json"      # 束ができたか（混ざりのつなぎ待ちの終わり）を見るファイル
AXIS_DOCS = {}
AXI = {}
QG = {}
QB = {}
PEOPLE_ORDER = ()
PEOPLE_SETS = {}
PEOPLE_REC = {}
PEOPLE_CUTS = ()     # 🔴 門番 check_qty がこの外の人の形を止める（亡くなった方の数に使わない）
QDOC = {}
QWHO = {}

SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "QG", "QB",
            "PEOPLE_ORDER", "PEOPLE_SETS", "PEOPLE_REC", "PEOPLE_CUTS", "QDOC", "QWHO", "SAT", "GEO", "SAT_LINES", "SAT_LINE_NOTE", "SAT_NONE",
            "NEEDS_MASK", "SLIDE_MOUNT", "SLIDE_NOT_MOUNT", "OCR_NOT_TEXT")


# ══════════════════════════════════════════════════════════
#  門番 check_illu から（git の `54b15e5e` の check_illu.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
K26_CUTS = ("c320", "c506", "c508", "c512", "c606", "c614", "c615", "c618", "c621", "c625", "c627", "c630", "c631", "c632", "c633",
            "c701", "c712", "c936")
REC_K26 = dict(
    # 置き場ごとに描いてよい人の影の数の上限（記録の場面にいた役職だけ）と、札に書いてよい役職（名前は書かない）
    people=dict(K1=2, K2=2, K3=1, K4=1, K5=0, K6=0),
    roles=("三等航海士", "二等航海士", "見習い", "船長", "通信士", "四等航海士"),
    # 時計の札＝置き場ごとの時刻（sources.md §6・G1 p54〜59）と「どの船の時計か」
    clock=dict(K1=("23:00", "0:00", "0:20", "1:00", "1:40", "2:40"), K2=("2:05",), K3=("23:00",), K4=("0:45",), K6=("4:10",)),
    ship=dict(K1=("カリフォルニアン号の時計",), K2=("操舵室の時計",), K3=("カリフォルニアン号の時計",), K4=("タイタニック号の時計",),
              K6=("カルパチア号の時計",)),
    who={"2:05": "見習い"},             # 証言で割れる時刻は誰の話かを札に（T1 Q7565＝見習い 2:05／二等航海士の話は 2:00 の向き＝sources.md §4-2）
    flares=3,                            # G1 p58「the vessel fired three more white rockets」
    miles=(5, 6),                        # G1 p54「about 5 or 6 miles」→ 札は km（1マイル＝1.852km・四捨五入）
    bearing="南西",                      # G1 p59「disappeared bearing SW.」
    seats=40, filled=12,                 # G1 p52「a carrying capacity of 40」・G1 p51「No. 1 certainly left with only 12」
    boat=(25 + 2 / 12, 7 + 2 / 12),      # G1 p25「25 feet 2 inches long by 7 feet 2 inches broad」（emergency boat＝wood cutter）
    no_name=dict(K1="タイタニック", K4="カリフォルニアン"),   # 見えた船を名乗らない（映像方針 26本目 案C の守りの線）
)


# ══════════════════════════════════════════════════════════
#  門番 check_mech から（git の `54b15e5e` の check_mech.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
REC_M26 = dict(
    src=dict(tt=("タイタニック号", "ship"), cf=("カリフォルニアン号", "ntsb"), cp=("カルパチア号", "uscg"), cr=("ケープ・レース", "tsb"),
             an=("アンティリアン号", "city"), am=("アメリカ号", "company"), ol=("オリンピック号", "bldg_a"), rep=("報告書", "SUB"),
             maib=("1992年の調べ直し", "DOC"), cap=("船長", "bldg_a"), mate=("航海士", "city"),
             # 🆕 ⑤b-6：調査官＝紫・次長＝緑（⑤b-3 の地図 c917 と同じ）・首席＝茶・米国上院の報告＝青・米国の巡視船＝青
             insp=("調査官", "tsb"), dep=("次長", "ntsb"), chief=("首席", "DOC"), sen=("米国上院の報告", "uscg"), rcs=("米国の巡視船", "uscg")),
    light=dict(green="OK", red="ALERT", white="SUB"),
    # 画面に出してよい時刻（sources.md §6 の時計の表と G1 の時刻＝20:00〈p.37〉・22:00〈p.39〉・22:20〈p.56〉・23:00・23:30・23:40〈p.57〉・0:00〈p.58〉・
    #   0:05〈p.49〉・0:15〈p.54〉・0:30〈p.58〉・0:35〈G7 PDF 23頁〉・0:45〈p.54〉・1:10〈p.58〉・1:15〈p.59〉・2:05〈p.59〉・2:20〈p.85〉・2:40〈p.59〉・4:00〈p.59〉）
    times=("20:00", "22:00", "22:20", "23:00", "23:30", "23:40", "0:00", "0:05", "0:15", "0:30", "0:35", "0:45", "1:10", "1:15", "2:05", "2:20",
           "2:40", "4:00",
           # 🆕 ⑤b-6：1:45〈G1 p.60・信号弾のころの終わり＝タイタニック号の時計〉・18:30〈G2 p.7＝カリフォルニアン号の推測の位置〉・19:30〈G2 p.10＝北極星の観測〉
           "1:45", "18:30", "19:30"),
    split=("1:10", "1:15", "2:00", "2:05"),
    ships=("タイタニック号", "カリフォルニアン号", "カルパチア号"),
    ng=("死亡", "救命艇", "カッター", "マードック", "グローブス", "ロストロン", "スチュワート", "ボックスホール", "ライトラー", "フィリップス",
        "エバンス", "ギブソン", "ストーン", "ロード船長"),
    # カリフォルニアン号から見た画面（見えた船をタイタニック号と名乗らない＝案B の守りの線）
    no_tt=("field", "sidelights", "masts2", "morse", "views2", "watches", "bearing", "flicker", "section", "height", "memory2", "cfband", "swap",
           # 🆕 ⑤b-6：船長の話の距離の輪・第三の船・カリフォルニアン号の側の論拠（星の観測・電報）
           "rings3", "third", "polaris", "antillian"),
    views=dict(
        tons2=dict(val=((("tt", 46328), ("cf", 6223)), "約7倍", 7), pv=(46328, 6223)),
        people4=dict(val=((("一等", 325), ("二等", 285), ("三等", 706), ("乗員", 885)), 1316, 2201, (109, (6, 24, 79)), True, True, True),
                     pv=(325, 285, 706, 885, 109)),
        boats20=dict(val=((("大きなボート", 65, 14), ("小さめのボート", 40, 2), ("折りたたみ式のボート", 47, 4)), 1178, True), pv=(65, 40, 47)),
        track3=dict(val=(2201, 1178, 962), pv=(2201, 1178, 962)),
        table1894=dict(val=(1894, 10000, 46328), pv=(10000, 46328)),
        clocks2=dict(val=(0.0, 0.0)),
        busy=dict(val=("20:00",)),
        cf_side=dict(val=("レイランド社", "ロンドン", "ボストン", 0)),
        drown=dict(val=(True,)),
        watch=dict(val=("22:00",)),
        helm=dict(val=(-22.5,)),
        olympic=dict(val=((37, 466, 430, 22), 22.5), pv=(466 * 0.9144, 852.5 * 0.3048)),
        damage=dict(val=((300, 90, 10, 20), ("前", "1", "2", "3", "6", "5")), pv=(300, 852.5)),
        tray=dict(val=(5, True)),
        ttband=dict(val=(("23:40", "衝突"), ("0:05ごろ", "ボートの用意"), ("0:15", "CQD"), ("0:45ごろ", "信号弾"), ("2:20", "沈没")),
                    pm=("23:40", "0:05", "0:15", "0:45", "2:20")),
        cqd=dict(val=((("C", "−·−·"), ("Q", "−−·−"), ("D", "−··")), "0:15")),
        carp=dict(val=(("0:35", 52, 107), -52.0)),
        rockets_n=dict(val=(8, (6, 12), 5)),
        colors=dict(val=("SUB", True)),
        field=dict(val=("22:20ごろ", True)),
        drift=dict(val=((19, 35), 11.25, 191.25)),
        sidelights=dict(val=(dict(right="green", left="red", mast="white"), True, True, (5, 9))),
        masts2=dict(val=((1, 2), 2, True)),
        views2=dict(val=(("客船には見えない", "客船です"), True)),
        watches=dict(val=((("夜の当直", "三等航海士"), ("真夜中からの当直", "二等航海士"), ("朝の当直", "一等航海士")), "23:40"),
                     pm=("0:00", "4:00", "23:40")),
        section=dict(val=("0:30すぎ", 2, "1:10ごろ", 5)),
        company=dict(val=("ホワイト・スター・ライン", "OK")),
        height=dict(val=(0.5,)),
        memory2=dict(val=(("mate", "1:10ごろ", 5), ("cap", "1:15ごろ", 1))),
        cfband=dict(val=(("22:20ごろ", "止まる（氷原の手前）"), ("23:40", "灯が消える（三等航海士の話）"), ("1:10ごろ", "白い信号弾 5発（二等航海士の話）"),
                         ("2:05", "全部で8発（見習いの話）"), ("2:40ごろ", "見えなくなる（二等航海士の話）"), "23:30"),
                    pm=("22:20", "23:40", "1:10", "2:05", "2:40", "23:30")),
        swap=dict(val=("4:00ごろ", 2)),
        # 🆕 ⑤b-6（第6〜9章）：値は G1・G2 の頁と sources.md §2・§6・§7・§8（量は p＝p0＋v×k・時刻は p＝p0＋(分−t0)×k）
        boxfill=dict(val=((1178, 652), (2, 3)), pv=(1178, 1178 * 2 / 3, 652)),
        split2=dict(val=((2201, 711, 1490), True), pv=(2201, 711, 1490)),
        rates4=dict(val=(("一等", 62), ("二等", 41), ("三等", 25), ("乗員", 24)), pv=(62, 41, 25, 24)),
        decks=dict(val=(True, True, True, True)),             # 三等は船の両端・一等より下・赤い棒（語られる話）は報告書の段で消える
        flare_bow=dict(val=(True, True, "4:00まで")),         # 緑の灯は前の少し左
        custom25=dict(val=(25,)),
        before_after=dict(val=("間違い", "怠り")),
        match2=dict(val=(("衝突", "見えた船の灯が消える"), ("信号弾 約8発", "白い信号弾 8発"), ("沈む", "見えなくなる"))),
        clocks_gap=dict(val=(("tt", "0:45", "1:45"), ("cf", "0:30", "1:40")), pm=("0:45", "1:45", "0:30", "1:40")),
        rings3=dict(val=("約9キロ", "約15キロ", "約19キロ"), pv=(5, 8, 10)),
        few_min=dict(val=("23:30",)),
        appeal=dict(val=(("正式な告発", "なし"), ("資格への処分", "なし"), ("申し立ての道", "なし"))),
        years6=dict(val=(("1912年", "1950年代", "", "1985年", "1990年", "1992年"),
                         ("審問の報告", "本と映画", "船長の訴え", "残骸が見つかる", "調べ直しを命じる", "調べ直しの報告"), True)),
        four_q=dict(val=(("①", "位置と距離"), ("②", "見えていたか"), ("③", "信号と動き"), ("④", "船長の行い"))),
        book2=dict(val=(("insp", "dep"), "dep")),             # 首席が支持したのは次長
        current=dict(val=(196.0, "時速約2.4キロ", 196.0, True)),
        dist2col=dict(val=((5, 10, 5), (17, 20, 18)), pv=(5, 10, 5, 17, 20, 18)),
        drift_s=dict(val=(True, True)),                       # 流された道は計算より南・タイタニック号に近い
        polaris=dict(val=(42.083, "19:30")),                  # 北緯 42°05′（sources.md §2-1）
        antillian=dict(val=("18:30", True, True, 3)),         # 止まった位置は真西
        horizon=dict(val=(True, True)),                       # 近い船の灯は線の上・遠い船の灯は線の下
        tt_watch=dict(val=("0:30ごろまで",)),
        third=dict(val=(True, True)),                         # 東から来て氷原の東の端で止まる
        refract=dict(val=(True,)),                            # 船は海のふくらみの向こう
        swing=dict(val=("green", "red", "starboard", "green")),   # 最初は緑・のちに赤・右舷へ回る・止まったままなら緑だけ
        seen2col=dict(val=("答えは出せない", "見えたなら 異常屈折", "たぶん 別の船")),
        four_steps=dict(val=(("①", "mate", "二等航海士が"), ("②", None, "機関室へ"), ("③", None, "通信士を"), ("④", "cap", "船長は"))),
        if_go=dict(val=("0:45ごろ",)),
        law1910=dict(val=(True, True)),
        linked=dict(val=(True,)),
        ladder=dict(val=("1912年7月", "1912年8月", "1913年", "1914年", "1948年")),
        skies2=dict(val=("ALERT", "SUB", 5)),
    ),
    # 出典の英文の句（頁は ss.REC_DOCS の通し番号＝G1 1〜88・G2 2001〜2030・G7 20001〜21170）。名前の入らない所を選んだ
    quote=dict(
        tons2=(("G1 p11", "46,328 tons gross"), ("G1 p56", "a vessel of 6,223 tons")),
        people4=(("G1 p32", "In all, 2,201 persons were on board"), ("G1 p32", "or 109 in all")),
        boats20=(("G1 p25", "a total of 11,327.9 cubic feet for 1,178 persons"),),
        track3=(("G1 p62", "a provision for 962 persons"), ("G1 p62", "1,178 persons, a number far in excess of the requirements of the table")),
        table1894=(("G1 p64", "Those regulations were last revised in 1894"), ("G1 p63", "made in 1894 for vessels of 10,000 tons and upward")),
        radio3=(("G2 p2005", "in 1912 many ships did not have wireless and those that did, did not necessarily keep continuous watch"),),
        clocks2=(("G2 p2010", "It was customary in 1912 for ships to adjust their clocks so that the sun would be approximately on the meridian"),),
        aside=(("G1 p36", "to wait until the Titanic would be within call of Cape Race"), ("G1 p36", "it was never handed to any officer")),
        busy=(("G1 p37", "it does not appear to have been delivered to the master or to any of the officers"),
              ("G1 p37", "very busy from 8 o'clock onward transmitting messages via Cape Race for passengers")),
        cf_side=(("G1 p56", "the steamship Californian, of the Leyland Line"),
                 ("G1 p56", "She had a passenger certificate, but was not carrying any passengers at the time")),
        relay3=(("G1 p56", "The message was intercepted by the Titanic"), ("G1 p56", "I heard you sending it to the Antillian, and I have got it")),
        drown=(("G1 p57", "The Titanic was in communication with Cape Race"),
               ("G1 p57", "was much stronger than any message being taken in by the Titanic from Cape Race")),
        watch=(("G1 p39", "we might be up around the ice any time now"), ("G1 p39", "both the men in the crow's nest")),
        helm=(("G1 p41", "about two points to port"), ("G2 p2008", "because of the helm orders then in use, was to direct the ship's head to port")),
        olympic=(("G1 p41", "about 37 seconds would be required"), ("G1 p41", "the ship would travel about 466 yards")),
        damage=(("G1 p42", "The damage extended over a length of about 300 feet"), ("G1 p42", "she would have passed through 300 feet in less than 10 seconds"),
                ("G1 p42", "No. 6 boiler room, No. 5 boiler room"), ("G1 p42", "moving at over 20 knots")),
        tray=(("G1 p45", "and so on in succession to the other boiler rooms till the ship would ultimately fill and sink"),
              ("G1 p45", "water came into the five forward compartments")),
        ttband=(("G1 p42", "took place at 11.40 p.m."), ("G1 p49", "at about 12.05 the order was given to uncover the 14 boats under davits"),
                ("G1 p54", "At 12.15 a. m. the distress signal CQD was sent"), ("G1 p54", "No. 7 boat was lowered (12.45 a. m.)"),
                ("G1 p85", "Two twenty a. m. (ship's time) April 15")),
        cqd=(("G1 p54", "This was heard by several steamships and by Cape Race"),),
        carp=(("G7 p20023", "Yes, 12.35; that was our apparent time"), ("G7 p20024", "north 52 degrees west true 58 miles from my position")),
        rockets_n=(("G1 p54", "fired about eight rockets"),),
        colors=(("G2 p2022", "such signals could be of any colour"),
                ("G2 p2022", "there was therefore nothing immediately to distinguish them from other rockets")),
        field=(("G1 p56", "obliged to stop and reverse engines"), ("G1 p56", "which stretched as far as could then be seen to the northward and southward"),
               ("G1 p56", "until 10.20")),
        drift=(("G1 p56", "about 19 miles N. by E. of the position of the"), ("G2 p2013", "a current setting about south by west")),
        sidelights=(("G1 p57", "and also her green side light"), ("G1 p57", "at some time between 11 and 11.30 he first saw her green light; she was then about 5 miles")),
        masts2=(("G1 p57", "made out two masthead lights"), ("G1 p57", "She is evidently a passenger steamer")),
        morse=(("G1 p57", "Call her up on the Morse lamp, and see if you can get any answer"),),
        views2=(("G1 p57", "That does not look like a passenger steamer"), ("G1 p57", "It is, sir. When she stopped her lights seemed to go out")),
        watches=(("G1 p57", "these lights went out at 11.40"), ("G1 p57", "because one bell was struck to call the middle watch"), ("G1 p58", "just after midnight")),
        bearing=(("G1 p58", "with instructions to tell him if her bearings altered or if she got any closer"),),
        flicker=(("G1 p58", "He first thought her masthead light was flickering and next thought it was a Morse light"),
                 ("G1 p58", "finally came to the conclusion that it was, as he had first supposed, the masthead light flickering")),
        section=(("G1 p58", "Sometime after 12.30 a. m."), ("G1 p58", "saw two rockets fired from the ship which he had been observing"),
                 ("G1 p58", "reported to the captain by voice pipe, that he had seen five white rockets")),
        company=(("G2 p2018", "it has been suggested that these were Company signals from the other ship"), ("G1 p54", "throwing off white stars")),
        height=(("G2 p2017", "described as low-lying (quoted as rising to less than mast-head height)"),),
        memory2=(("G1 p59", "he went to the voice pipe at about 1.15, but was told then of a white rocket (not five white rockets)"),
                 ("G1 p58", "about 1.10 a. m.")),
        cfband=(("G1 p56", "until 10.20"), ("G1 p57", "went out at 11.40"), ("G1 p57", "turned in at 11.30 p.m."), ("G1 p58", "about 1.10 a. m."),
                ("G1 p59", "five minutes past two"), ("G1 p59", "At about 2.40 a. m."), ("G1 p58", "altogether we had seen eight of these white lights")),
        swap=(("G1 p59", "a steamer came in sight with two white masthead lights"), ("G1 p59", "about 4 a.m."), ("G1 p59", "This mistake was not corrected")),
        # 🆕 ⑤b-6（第6〜9章）：名前の入らない所を選んだ。G4・G5・G6・T3・U1 は原文の通し頁が無い（照らさない）
        boxfill=(("G1 p48", "Thus the total boat accommodation was for 1,178 persons"), ("G1 p76", "boat accommodation was utilized to less than two-thirds of its capacity"),
                 ("G1 p51", "of the 712 persons saved only 652 could have left the")),
        split2=(("G1 p56", "711 out of 2,201, or 32.30 per cent"), ("G1 p5", "the loss of 1,490 lives")),
        rates4=(("G1 p55", "62.46 per cent"), ("G1 p55", "41.40 per cent"), ("G1 p55", "25.21 per cent"), ("G1 p56", "212 out of 885, or 23.95 per cent")),
        decks=(("G1 p53", "There appears to have been no truth in these suggestions"), ("G1 p53", "which were at the extreme ends of the ship")),
        flare_bow=(("G1 p55", "was altering his course continually in order to avoid icebergs"), ("G7 p20025", "we were passing icebergs on every side")),
        custom25=(("G1 p40", "for a quarter of a century or more"), ("G1 p40", "to keep the course, to maintain the speed and to trust to a sharp lookout")),
        before_after=(("G1 p41", "What was a mistake in the case of the Titanic would without doubt be negligence in any similar case in the future"),),
        match2=(("G1 p60", "There are contradictions and inconsistencies in the story as told by the different witnesses"),
                ("G1 p60", "But the truth of the matter is plain"), ("G1 p60", "The Californian saw eight")),
        clocks_gap=(("G1 p60", "from about 12.45 to 1.45"), ("G1 p54", "eight rockets having been seen between 12.30 and 1.40"),
                    ("G2 p2010", "only likely to have been a few minutes")),
        rings3=(("G1 p60", "5 miles apart at the time of the disaster"), ("G1 p60", "though not more than 8 to 10 miles")),
        few_min=(("G1 p57", "turned in at 11.30"),),
        appeal=(("G2 p2005", "he requested a re-hearing of that part of the Inquiry which concerned his ship; the request was rejected"),
                ("G2 p2005", "he had no right of appeal")),
        years6=(("G2 p2005", "by then over 80 years old"), ("G2 p2005", "two petitions were made to the Board of Trade asking for the Inquiry to be re-opened; both were rejected"),
                ("G2 p2005", "in the mid-1950's"), ("G2 p2006", "In 1985 an expedition"), ("G2 p2006", "in 1990 the Secretary of State for Transport")),
        four_q=(("G2 p2007", "To establish so far as is now possible the positions of TITANIC"), ("G2 p2007", "To consider whether TITANIC was seen by CALIFORNIAN"),
                ("G2 p2007", "To consider whether distress signals from TITANIC were seen by")),
        book2=(("G2 p2003", "His report, which follows, incorporates his conclusions and those of the appointed Inspector"),
               ("G2 p2003", "full endorse the Deputy Chief Inspector's report and conclusions")),
        current=(("G2 p2013", "the Labrador current extended further south and east than is usual"), ("G2 p2013", "the direction of set was about 196"),
                 ("G2 p2013", "and the rate about 1.3 knots")),
        dist2col=(("G2 p2011", "between 5 and 10 miles apart whilst they lay stopped, and probably nearer five"), ("G2 p2011", "probably about 18 miles"),
                  ("G2 p2007", "between 17 and 20 miles")),
        drift_s=(("G2 p2013", "He considers that the current had set southerly since noon on 14 April; no allowance for this current was made"),
                 ("G2 p2007", "only 5 to 7 miles off")),
        polaris=(("G2 p2014", "The Pole Star sight taken by the Chief Officer at 1930 hrs"),
                 ("G2 p2014", "as that observed at noon on the same day, showing a course made good of west")),
        antillian=(("G2 p2011", "At 1830 hrs three large icebergs were seen some five miles to the south"),
                   ("G2 p2014", "which cannot have been fabricated is the signal sent to ANTILLIAN"),
                   ("G2 p2014", "it adds weight to the statement that CALIFORNIAN was steering westerly")),
        horizon=(("G2 p2017", "well beyond the ordinary visible horizon"), ("G2 p2015", "our respective opinions on position are undoubtedly coloured by this difference")),
        tt_watch=(("G2 p2016", "no ship was seen by TITANIC until well after the collision"), ("G2 p2016", "about 0030 hrs"),
                  ("G2 p2016", "watch was maintained with officers on the Bridge and seamen in the")),
        third=(("G2 p2017", "a third ship was present which approached from the East, stopped on meeting the field ice, and then after a period steamed away to seek a break in the ice"),),
        refract=(("G2 p2017", "at a very much greater range than her horizon because of abnormal"),),
        swing=(("G2 p2017", "later her red (port) light came into view, arguing that after stopping she swung markedly to starboard"),
               ("G2 p2017", "Her port sidelight would therefore not be seen")),
        seen2col=(("G2 p2017", "I do not consider that a definite answer to the question 'was TITANIC seen' can be given"),
                  ("G2 p2017", "the ship seen by CALIFORNIAN was another, unidentified, vessel")),
        four_steps=(("G2 p2020", "Stand By Engines"), ("G2 p2020", "The Wireless Operator should have been called"),
                    ("G2 p2020", "got under way towards the apparent source of the rockets")),
        asleep=(("G2 p2021", "I think the message from the Bridge simply did not get through"), ("G2 p2021", "the subject appears to respond to a call")),
        if_go=(("G2 p2022", "The first rocket appears to have been fired at about 0045 hrs (TITANIC time)"),
               ("G2 p2022", "given my minimum distance off of 17 miles, have reached the scene at just about the time of sinking")),
        if_flow=(("G2 p2022", "would shortly receive TITANIC'S SOS with its incorrect position"), ("G2 p2022", "CALIFORNIAN would arrive well after the sinking")),
        ice_rule=(("G1 p87", "when ice is reported in or near the track the ship should proceed in the dark hours at a moderate speed or alter her course so as to go well clear of the danger zone"),),
        ladder=(("G2 p2022", "it was not until 1948 that the rules for distress signals were amended"),),
        skies2=(("G2 p2022", "such signals could be of any colour"), ("G2 p2022", "it was not until 1948 that the rules for distress signals were amended")),
    ),
)


GATES = {
    "check_mech": dict(REC_M26=REC_M26),
    "check_illu": dict(REC_K26=REC_K26, K26_CUTS=K26_CUTS),
}

_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・（gate を渡せば）その門番の記録の表を26本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss は触らない）＝14〜25本目・17本目の見本と重ねるとき。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が26本目の表で
       27本目の画を測る）。apply の前に**無かった名**も覚えて、restore で**消す**＝selftest のあとに26本目の名が本番へ残らない
       （fixture_ep15〜ep25・ep17 と同じ作り）。⚠️ `titan_fig.GEO` は触らない（26本目の地点は無い）"""
    saved = dict(full=not tables_only, ss={}, ss_new=[], gate=gate, tables={}, tables_new=[])
    if not tables_only:
        from cuts import ss
        saved["ss"] = {n: getattr(ss, n) for n in SS_NAMES if hasattr(ss, n)}
        saved["ss_new"] = [n for n in SS_NAMES if not hasattr(ss, n)]
    tabs = {}
    if gate is not None:
        name = Path(getattr(gate, "__file__", "") or "").stem
        tabs = GATES.get(name, {})
        for k in tabs:
            if hasattr(gate, k):
                saved["tables"][k] = getattr(gate, k)
            else:
                saved["tables_new"].append(k)
    _SAVED.append(saved)         # 覚えてから差し込む＝途中で落ちても restore() が戻せる
    if not tables_only:
        g = globals()
        for n in SS_NAMES:
            setattr(ss, n, g[n])
    for k, v in tabs.items():
        setattr(gate, k, v)


CUTS_SHA = "54b15e5e"      # 26本目の章ファイルが最後に live だった版（章ファイルを27本目の器に替える前＝git の `54b15e5e`＝27本目 ⑤b-1 の移し替えの merge）
_CUTS26 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def _footage26():
    """26本目の映像の台帳 `CLIPS`（`ref/ep26/clips.json`）と使う区間 `USE`・器の黒帯の割合 `PILLAR`（git の CUTS_SHA の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}`）を返す。
    🔴 26本目の章ファイルは `ss.vid` で `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を引く（フリー素材のカットは台帳の `"stock": true` を見て、ひかえの静止画の名を
    `ep26/stock/fb_<cid>.jpg` に決める）。本番の footage は27本目の表になった＝そのままだと26本目のフリー素材のカットは `ref/ep26/fb_<cid>.jpg`（無い名）の箱を
    決めに行って章ファイルが読み込みで落ちる。→ 章ファイルを読む間だけ、この表を footage に差す（`cuts_ep26` が戻す）。
    footage.py の `USE`・`PILLAR` は値だけの代入＝その2文だけを取り出して評価する（footage.py 全体は import しない）。
    ⚠️ 26本目の PILLAR は NOAA 2004 の N04（640×426・左右の端の黒い列）を持つ（Pexels は器も中身も 1920×1080）＝空でも止めない形は残す。USE（21カット）と台帳が読めなければ止める"""
    import ast
    import json
    import subprocess
    p = subprocess.run(["git", "-C", str(ROOT), "show", f"{CUTS_SHA}:tools/footage.py"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 26本目の映像の使う区間を git の {CUTS_SHA} の tools/footage.py から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    ns = {}
    for node in ast.parse(p.stdout.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("USE", "PILLAR") for t in node.targets):
            exec(compile(ast.Module([node], []), f"footage_{CUTS_SHA}", "exec"), ns)
    use, pillar = ns.get("USE"), ns.get("PILLAR")
    clips_file = REF / "clips.json"
    if not use or pillar is None or not clips_file.exists():
        raise RuntimeError(f"🔴 26本目の映像の表が読めていない（USE {len(use or {})}・PILLAR {'無い' if pillar is None else len(pillar)}・"
                           f"{clips_file} {'ある' if clips_file.exists() else '無い'}）")
    return json.loads(clips_file.read_text(encoding="utf-8")), use, pillar


def cuts_ep26():
    """26本目の章ファイル（git の CUTS_SHA の `tools/cuts/`＝26本目の ss.py ごと）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。
    読む間だけ `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を26本目の表にする（`_footage26`＝本番の footage は27本目の表）。読み終えたら戻す。"""
    if _CUTS26:
        return _CUTS26[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    import footage as _FO
    clips24, use24, pillar24 = _footage26()
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 26本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts26_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep26 の写真・頁を読む＝根の下の作業場所の
        # フォルダ（ref・out ほか）へ一時フォルダから junction（Windows のフォルダへの道しるべ）を張る。消すときは先に道しるべだけ外す
        import _winapi
        for d in ROOT.iterdir():
            if d.is_dir() and d.name not in ("tools", ".git"):
                _winapi.CreateJunction(str(d), str(tmp / d.name))
                links.append(tmp / d.name)
        live = {k: v for k, v in sys.modules.items() if k == "cuts" or k.startswith("cuts.")}
        before = set(sys.modules)
        for k in live:
            del sys.modules[k]
        sys.path.insert(0, str(tmp / "tools"))
        keep_fo = (_FO.CLIPS, _FO.USE, _FO.PILLAR)
        _FO.CLIPS, _FO.USE, _FO.PILLAR = clips24, use24, pillar24          # 章ファイルを読む間だけ（finally で戻す）
        try:
            old = importlib.import_module("cuts")
            got = (dict(old.PLAN), dict(old.SPEC))
            broken = dict(getattr(old, "BROKEN", {}) or {})
        finally:
            _FO.CLIPS, _FO.USE, _FO.PILLAR = keep_fo
            sys.path.remove(str(tmp / "tools"))
            for k in set(sys.modules) - before:
                del sys.modules[k]
            for k in [k for k in sys.modules if k == "cuts" or k.startswith("cuts.")]:
                del sys.modules[k]
            sys.modules.update(live)
    finally:
        for ln in links:
            os.rmdir(ln)          # 道しるべだけを外す（中身＝本線のフォルダには触らない）
        if any(x.exists() for x in links):
            raise RuntimeError(f"🔴 一時フォルダの道しるべを外せない＝{tmp} を消さずに止める（本線のフォルダを消さないため）")
        shutil.rmtree(tmp, ignore_errors=True)
    # 🔴 26本目は 235カット＋ed01＝SPEC 236（git の 54b15e5e）。章ファイルが1本でも読めない（BROKEN）と SPEC が欠ける＝黙って一部で検算しない
    if broken or len(got[0]) != 235 or len(got[1]) != 236 or "c101" not in got[1]:
        raise RuntimeError(f"🔴 26本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}・読めない章 {sorted(broken)[:6]}）")
    _CUTS26.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を26本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で27本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep26()
    _SAVED.append(dict(cuts=(dict(cuts.PLAN), dict(cuts.SPEC))))
    cuts.PLAN.clear()
    cuts.PLAN.update(copy.deepcopy(plan))
    cuts.SPEC.clear()
    cuts.SPEC.update(copy.deepcopy(spec))


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。
    ss と門番の表は、apply の前に無かった名を消す。
    tables_only で差し込んだ分は ss を覚えていない＝戻さない（先に差し込んだ別の見本を壊さない）。LIFO（あとに apply した順）"""
    while _SAVED:
        s = _SAVED.pop()
        if s.get("cuts") is not None:          # apply_cuts() の分＝27本目の PLAN・SPEC へ戻す
            import cuts
            plan, spec = s["cuts"]
            cuts.PLAN.clear()
            cuts.PLAN.update(plan)
            cuts.SPEC.clear()
            cuts.SPEC.update(spec)
            continue
        if s["full"]:
            from cuts import ss
            for n, v in s["ss"].items():
                setattr(ss, n, v)
            for n in s["ss_new"]:
                if hasattr(ss, n):
                    delattr(ss, n)
        gate = s["gate"]
        for k, v in s["tables"].items():
            setattr(gate, k, v)
        for k in s["tables_new"]:
            if hasattr(gate, k):
                delattr(gate, k)
