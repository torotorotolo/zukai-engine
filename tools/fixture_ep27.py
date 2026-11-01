# -*- coding: utf-8 -*-
"""27本目（八田與一容疑者の事件・2022-06-29・大分県別府市のひき逃げ死亡事件・重要指名手配中＝事件の回の1本目の報道と県警の公表の動画）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-11-01（28本目 タイムズカー情報漏えいの ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `b62a7f94` と同じ）
  ・`cuts/ss.py` の27本目の値＝衛星写真の地図（SAT＝G1・G2W・G2N・G3・G7N・G7W・G9・GEO＝事件の場所と地方の札の置き場の10点）・道すじの断り（SAT_LINE_NOTE）・
    説明カットの地の写真の明るさ（GROUND＝17点）・写真の束の定数（顔と店名だけ升目にする点 NEEDS_MASK 7・台紙の縁でない暗い帯の名簿 SLIDE_NOT_MOUNT 16）。
    27本目も空のままだった表（REC_DOCS・ILLU_*・AXIS_DOCS・AXI・QG・QB・PEOPLE_*・QDOC・QWHO・SLIDE_MOUNT・OCR_NOT_TEXT・SAT_LINES・SAT_NONE〈None〉）も、
    27本目の状態として持つ（17・23〜26本目の見本と同じ考え方）
  ・門番の記録の表（check_mech＝REC_M27〈図解 `mech27.py` の記録の値＝誰か・何かの名と色・値と比例・SNS の札の原文・元刑事と県警の言葉・電話番号・出さない言葉〉／
    check_sat＝REC_SAT_NUM〈c212・c504 の札の数と抜き書きの句〉・REC_SAT_PAGES〈抜き書きの道＝git の外〉）。
    check_axis・check_qty・check_boxes・check_illu・check_photo_edge・check_photo_mask は27本目で足した表が無い（check_photo_edge の名簿は ss の SLIDE_*＝上）＝この見本の GATES に載せない
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を27本目の実物でも確かめている（check_mech の m27）＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は28本目の空の器にした
  （fixture_ep14〜ep26・ep17 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep27
      fixture_ep27.apply(sys.modules[__name__])   # その処理の中だけ ss・この門番の記録の表が27本目になる
      try: …（検算）
      finally: fixture_ep27.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14〜26本目・17本目の見本と重ねるとき（check_mech）は
      fixture_ep27.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと28本目の画に27本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。⚠️ ほかの回の見本（fixture_ep26 ほか）の積み荷とは別＝それぞれの restore で戻す
■ 注意:
  ⚠️ 見本の原文 `ref/ep27/src/news_frag_v2.txt`（check_sat の `_rec_page`）は**手元にだけある**（git の外）。Actions には無い＝句の照合を飛ばす（表に載っているかは照らす）。
  ⚠️ 27本目の selftest のうち、**章ファイルの SPEC を読むもの**は check_mech の `_selftest_m27`（m27 のカット＝図解）。`apply(gate)`＋`apply_cuts()`（27本目の章ファイルを
     git の `CUTS_SHA`＝`b62a7f94` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ27本目に入れ替える・git が無い所では止める＝fail closed）を使う（`restore()` で28本目へ戻る・LIFO）。
  ⚠️ 27本目の章ファイルは git の版の `tools/cuts/ss.py`（EP＝`ep27/`・27本目の値）ごと取り出して読む＝写真の名 `P("…")` は `ep27/…` のまま（本番の ss の EP は ep28）。
     ただし `ss.vid`・`ss.head`・`ss.tailv` は本番の **`footage.CLIPS`・`footage.USE`**（と `footage.PILLAR`）を引く（県警の動画の引用 YT-C の2区間＝台帳 `ref/ep27/clips.json`）＝
     本番の footage は28本目の表なので、`cuts_ep27()` は章ファイルを読む間だけ footage の3つを27本目の表（台帳 `ref/ep27/clips.json`・使う区間 `USE` と黒帯の割合 `PILLAR` は
     git の `b62a7f94` の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}` の2文を取り出して評価）に差し、読み終えたら戻す
     （`_footage27`＝17本目の `_footage17`・24本目の `_footage24`・25本目の `_footage25`・26本目の `_footage26` と同じ）。27本目の footage の値は**ここに写していない**（git の `b62a7f94` が正本）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep27/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は27本目の道を持つ。
  ⚠️ `NEEDS_MASK`・`SLIDE_MOUNT`・`SLIDE_NOT_MOUNT`・`OCR_NOT_TEXT` の鍵と `SAT` の `file` は **`ep27/` の名を文字で書いた**（本番の ss は `P(…)`・`f"{EP}…"` で組んでいた＝
     EP が ep28 になると `ep28/…`〈無い名〉に化ける。fixture_ep17・ep22〜ep26 と同じ扱い）。説明の文は1字も変えていない（値＝git の `b62a7f94` の ss を評価した結果と同じ）。
  ⚠️ `SAT`・`GEO` は本番の ss で `SAT = {}`・`GEO = {}` のあとに `SAT.update(…)`・`GEO.update(…)` を足す形だった＝その文をそのまま写した（評価した値は同じ）。
     `SAT_LINE_NOTE` は本番の ss で2回代入していた（空の器 → 27本目 ⑤b-5 の値）＝2つの文を並びのまま写した（評価した値＝あとの値）。
     check_sat の `REC_SAT_NUM` も `{}` のあとに `REC_SAT_NUM.update(…)` を足す形だった＝同じ。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝27本目は 0.93）は見本に入れない（16〜26本目・17本目の見本も入れていない）＝本番の ss は今の値のまま残し、28本目の束で取り直す。
  ⚠️ 写真の束の定数のうち `TRIM`（`pages.json` から読む＝REF が替われば追う）・`PRIVATE_OUT`・`NG_PHOTOS` は見本に入れない。
  ⚠️ 型として本番に残した＝ss の関数（`sat`・`ax`・`qb`・`P`・`page`・`vid`・`head`・`tailv`・`mv`・`mvz`・`tcam`・`gr`・`is_private`・`check_frame_only`・`check_card_mix`・`src`）・
     `SAT_CREDIT`・`GROUND_LIC`・`PRIVATE_DIR`・`SNS_NOTE`・`SNS_NOTE_BOX`・`SNS_NOTE_INK`（回をまたいで同じ）・
     check_mech の `SNS_VIEWS27`・`_ym27`・`judge_m27`（表が空なら理由を出して止める入口）・check_sat の `_rec_page`・描く側の型 `tools/mech27.py`・`titan_fig.m27`（どれも cuts.ss の27本目の値を読まない）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep27"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から（git の `b62a7f94` の ss.py の代入文をそのまま写した・`P("…")` だけ `"ep27/….jpg"`・`f"{EP}…"` だけ `"ep27/…"` の文字に）
# ══════════════════════════════════════════════════════
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"   # 型の定数（本番の ss に残した・SAT を組むための名＝SS_NAMES に入れない）

NEEDS_MASK: dict[str, str] = {
    "ep27/cm045.jpg": "JR別府駅近くの夜の通り（CC BY 2.0）＝コンビニの前と右を歩く私人3人の顔・右のバー2軒の店名（c105・地 c519）",
    "ep27/cm154.jpg": "夜の JR別府駅（CC BY 2.0）＝右のタクシーの中の人の横顔・札を持って座る人の顔（c214・c608）",
    "ep27/cm044.jpg": "駅近くの夜の交差点（CC BY 2.0）＝横断歩道を渡る黒いシャツの人の顔（c204・地 c201 c203 c205 c517 c518）",
    "ep27/cm254.jpg": "北浜の国道10号（CC BY 2.0）＝焼肉店の店名（c404・地 c405 c406 c407 c605 c606 ほか）",
    "ep27/cm259.jpg": "別府タワーから見た南の街並み（CC BY 3.0）＝焼肉店の店名と URL（c402 は寄りで窓の外・地 c403）",
    "ep27/cm112.jpg": "別府観光港の交通センター（CC0）＝1階の食堂の店名（c411）",
    "ep27/cm106.jpg": "別府観光港の交通センター（CC0）＝1階の食堂の店名（c506・地 c501 c502 c503 c508）",
}
SLIDE_MOUNT: dict[str, str] = {}
SLIDE_NOT_MOUNT: dict[str, str] = {
    "ep27/cm001.jpg": "下 5.0%＝駅のホームの手前の暗い柵と壁（夕方の青山通り）",
    "ep27/cm040.jpg": "左 5.0%・上 3.1%＝ホームの屋根の暗い梁（駅名の看板の上）",
    "ep27/cm045.jpg": "上 5.0%＝夜空（2022年9月の夜の通り）",
    "ep27/cm046.jpg": "上 5.0%＝夜空（北浜の国道10号の交差点）",
    "ep27/cm051.jpg": "四辺＝夜の埠頭の暗い空と駐車場（2015年2月の夜）",
    "ep27/cm112.jpg": "下 5.0%＝手前の暗い舗装（夕方の交通センター）",
    "ep27/cm151.jpg": "上 5.0%＝夜空と架線（夜のホーム）",
    "ep27/cm154.jpg": "上 5.0%＝夜空（夜の駅舎）",
    "ep27/cm156.jpg": "上 5.0%＝夜空と街灯（2011年の夜の駅）",
    "ep27/cm198.jpg": "下 5.0%＝手前の暗い山の斜面（十文字原からの夜景）",
    "ep27/cm283.jpg": "左 2.8%＝手前の暗い柱（駐車場の案内とバス）",
    "ep27/police/xpost1.jpg": "四辺＝手配のポスターの黒い地の図柄（引用＝額装・加工しない）",
    # 🆕 ⑤b-3（10-30）：YT-A のコマ＝県警の動画の画のまま（引用＝切らない）。960px の並べ（scratchpad `ytA_sheet.jpg`）で見た
    "ep27/police/yta026.jpg": "左右＝縦長のスマホの映像を横長に収めた県警の動画の外の黒（引用＝額装・加工しない）",
    "ep27/police/yta034.jpg": "左＝夜の暗い歩道に大きな字・右＝縦長の映像の外の黒（県警の動画の画のまま）",
    "ep27/police/yta165.jpg": "四辺＝黒地に白い字の結び（県警の動画の画のまま）",
    "ep27/stock/px30037331.jpg": "左・上・右＝夜の商店街のアーケードの暗い天井と店の戸（イメージ）",
    "ep27/stock/px7553959.jpg": "四辺＝夜の車の中の暗い内装（イメージ）",
}
OCR_NOT_TEXT: dict[str, list] = {}
SAT = {}
GEO = {}
SAT_LINES = {}
SAT_LINE_NOTE = ""
GEO.update({
    "noguchibaru": dict(ll=(33.284962, 131.486786), src="西日本 2022-11-30・台本 c202（`別府市野口原の県道の交差点`）",
                        how="一般の座標（住所検索 gsi＝野口原の代表点・交差点の位置ではない）"),
    "aoyama": dict(ll=(33.27795, 131.491745), src="抜き書き p114（T230526-11＝`住宅が立ち並ぶ青山町を通ったあと`）",
                   how="一般の座標（住所検索 gsi＝青山町の代表点）"),
    "kamitanoyu": dict(ll=(33.278145, 131.495758), src="台本 c213（`青山町を抜けて、上田の湯町へ`＝④' で照合）",
                       how="一般の座標（住所検索 gsi＝上田の湯町の代表点）"),
    "station": dict(ll=(33.279537, 131.500458), src="抜き書き p114（T230526-11＝`ＪＲ別府駅のそばを通過し`）",
                    how="一般の座標（住所検索 gsi＝駅前町の代表点）"),
    "kitahama": dict(ll=(33.278667, 131.504868), src="抜き書き p115（`国道１０号を横切って逃走を続けました`）・台本 c214",
                     how="一般の座標（住所検索 gsi＝北浜一丁目の代表点）"),
    "yacht": dict(ll=(33.27823, 131.50798), src="T261021-03・OBS 2024-06-04（`約2キロ離れたヨットハーバーで足取りが途絶えました`）",
                  how="一般の座標（OpenStreetMap＝別府北浜ヨットハーバー）"),
    "kanto": dict(ll=(36.0, 139.6), src="抜き書き p41（`関東が最多で約4950件`）", how="一般の座標（地方の目安の位置＝札を置く所）"),
    "kinki": dict(ll=(34.7, 135.6), src="抜き書き p41（`近畿が約1830件`）", how="一般の座標（地方の目安の位置＝札を置く所）"),
    "kyushu": dict(ll=(31.9, 130.5), src="抜き書き p41（`大分を除く九州が約1680件`）", how="一般の座標（地方の目安の位置＝札を置く所）"),
    "oita": dict(ll=(33.2, 131.6), src="抜き書き p41（`大分県内が約740件`）", how="一般の座標（地方の目安の位置＝札を置く所）"),
})
SAT_LINE_NOTE = "道すじは町の代表点を結んだ模式（警察が公表した経路の形ではない）"
SAT.update({
    "G1": dict(file="ep27/photo/gmap_g1_route.png", ll=(33.2816, 131.4974), z=16, md5="c6f3e346d8318b07a982681271145a2b", credit=SAT_CREDIT),
    "G2W": dict(file="ep27/photo/gmap_g2w_noguchibaru.png", ll=(33.284962, 131.486786), z=17, md5="1983fcf8f0f97be29ed5edce922af7c4", credit=SAT_CREDIT),
    "G2N": dict(file="ep27/photo/gmap_g2n_noguchibaru.png", ll=(33.284962, 131.486786), z=18, md5="3615df6e648d1bee5cb7163404433508", credit=SAT_CREDIT),
    "G3": dict(file="ep27/photo/gmap_g3_aoyama.png", ll=(33.27805, 131.49375), z=17, md5="81abb0c21a1a41f15384712d831a28ec", credit=SAT_CREDIT),
    "G7N": dict(file="ep27/photo/gmap_g7n_yacht.png", ll=(33.27823, 131.50798), z=17, md5="9e1655c29f0ae024cbf4f631a931357e", credit=SAT_CREDIT),
    "G7W": dict(file="ep27/photo/gmap_g7w_bay.png", ll=(33.27823, 131.50798), z=15, md5="9493a553276e0ba09bd80f645321dee0", credit=SAT_CREDIT),
    "G9": dict(file="ep27/photo/gmap_g9_japan.png", ll=(36.5, 136.0), z=5, md5="cfa4be0d33baf93f25250a35cb329891", credit=SAT_CREDIT),
})
SAT_NONE = None
REC_PAGES = REF / "src" / "ep27_pages.txt"      # 部品の出典（`rec=`）を当てる原文（git の外＝手元だけ）
REC_DOCS = {}                               # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
ILLU_SPLIT_TIMES = ()                       # 割れる時刻（2つの資料で時刻が割れる所＝札は秒で見る）
ILLU_CROWD_UNTIL = None                     # 群れを描いてよい場面の時刻の上限（None＝群れを描かない）
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）
ILLU_CLOCK_OK = ()                          # 札に出してよい時計の時刻（「時:分」まで）＝空なら時計の札を出せない
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
GROUND = {"cm044": 0.28, "cm045": 0.28, "cm056": 0.29, "cm106": 0.28, "cm110": 0.28, "cm144": 0.28, "cm151": 0.28,
          "cm152": 0.28, "cm153": 0.28, "cm156": 0.28, "cm198": 0.28, "cm205": 0.28, "cm208": 0.29, "cm254": 0.28, "cm257": 0.29,
          "cm258": 0.30, "cm259": 0.29}

SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "QG", "QB",
            "PEOPLE_ORDER", "PEOPLE_SETS", "PEOPLE_REC", "PEOPLE_CUTS", "QDOC", "QWHO", "SAT", "GEO", "SAT_LINES", "SAT_LINE_NOTE", "SAT_NONE",
            "NEEDS_MASK", "SLIDE_MOUNT", "SLIDE_NOT_MOUNT", "OCR_NOT_TEXT", "GROUND")


# ══════════════════════════════════════════════════════════
#  門番 check_sat から（git の `b62a7f94` の check_sat.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
REC_SAT_NUM = {}
REC_SAT_PAGES = Path(__file__).resolve().parent.parent / "ref" / "ep27" / "src" / "news_frag_v2.txt"
REC_SAT_NUM.update({
    "c212": {"防犯カメラ8台の映像から〈警察の公表〉": (("抜き書き p114", "８台の防犯カメラが捉えていました"),)},
    "c504": {
        "関東 約4950件": (("抜き書き p41", "関東が最多で約4950件"),),
        "近畿 約1830件": (("抜き書き p41", "近畿が約1830件"),),
        "大分県をのぞく九州 約1680件": (("抜き書き p41", "大分を除く九州が約1680件"),),
        "大分県 約740件": (("抜き書き p41", "大分県内が約740件"),),
        "その他の地域 約2810件": (("抜き書き p41", "その他の地域が約2810件"),),
        "ネットの動画や画像 約1230件": (("抜き書き p53", "累計約1230件"),),
    },
})


# ══════════════════════════════════════════════════════════
#  門番 check_mech から（git の `b62a7f94` の check_mech.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
REC_M27 = dict(
    src=dict(police=("警察", "uscg"), npa=("警察庁", "tsb"), kuni=("国", "tsb"), family=("遺族ら", "bldg_a"), news=("報道", "DOC"),
             expert=("専門家", "DOC"), car=("容疑者の車", "company"), mini=("ミニバイク", "ship"), moto=("オートバイ", "ntsb"),
             court=("裁判", "INST"), civil=("民事", "ntsb"), seen=("目撃の情報", "company"), sns=("SNS の声", "SUB")),
    views=dict(
        bignum=dict(val=("1万3978件", "2026年9月末まで")),
        talk=dict(val=(15, 30), pv=(15, 30)),
        speed=dict(val=(40, 70), pv=(40, 70)),          # 🔧 ⑤c'：100（2023年の報道）は c211 の語り＝c210 の図から外した
        reward=dict(val=((300, 500, 800), True), pv=(300, 500, 800)),
        steps5=dict(val=(("2022年7月", "名前と顔写真"), ("2023年5月", "動画10本"), ("2023年9月", "重要指名手配・報奨金"), ("2024年6月", "似顔絵"),
                         ("2024年8月", "手配の動画")), pm=("2022年7月", "2023年5月", "2023年9月", "2024年6月", "2024年8月")),
        limit=dict(val=(7,), pv=(7,)),
        # 🔧 ⑤c'：語り「2年あまりで6937件」の点（2024年8月末＝① §2）を足した
        cumline=dict(val=(("2022年7月28日", 36), ("2023年6月29日", 854), ("2023年12月末", 4052), ("2024年8月末", 6937), ("2025年4月末", 9430),
                          ("2025年12月末", 12029), ("2026年9月末", 13978)), pv=(36, 854, 4052, 6937, 9430, 12029, 13978),
                     pd=("2022-07-28", "2023-06-29", "2023-12-31", "2024-08-31", "2025-04-30", "2025-12-31", "2026-09-30"), d0="2022-06-29"),
        monthly=dict(val=(("2023年9月15〜30日", 884), ("2023年10月", 915), ("2024年7月", 660), ("2025年6月", 706), ("2026年6月", 401)),
                     pv=(884, 915, 660, 706, 401)),
        share=dict(val=((13978, 13240), 95)),
        detective=dict(val=(("声をかけない", "追い詰めない", "すぐに110番"), "違っていたからといって怒られるわけじゃない")),
        post=dict(val=("あなたのそばに潜んでいるかも。",)),
        contact=dict(val=("0977-21-2131",)),
    ),
    # SNS の札の原文（Yahoo!リアルタイム検索で見た投稿の字＝控え ref/ep27/src/sns_posts.tsv〈git の外〉・アカウント名は持たない）
    sns=dict(k1=("なんか八田與一にめっちゃ似てる人とすれ違ったんだけどたぶん違う", "X の投稿（2026年10月29日）"),
             k3=("関東で目撃情報が寄せられているから、重点的に調べるべきではないか", "X の投稿（2026年10月25日）"),
             k4=("八田與一容疑者、警察が海を捜索してるけど死んだ説が濃厚だと思う。", "X の投稿（2026年10月22日）")),
    ng=("犯人",),
    note="※SNS の投稿。事実かは確かめられていません",      # 了承②（10-29）の文言＝描く側の cuts.ss.SNS_NOTE と別に持つ
    rel_src=r"^(T\d{6}-\d{2}|(OAB|OBS|西日本|共|日経|日テレ|NPS|ABEMA|X|県警X|県警YT) \d{4}-\d{2}-\d{2}|県警|警察庁|願う会|① §\d)$",
)


GATES = {
    "check_mech": dict(REC_M27=REC_M27),
    "check_sat": dict(REC_SAT_NUM=REC_SAT_NUM, REC_SAT_PAGES=REC_SAT_PAGES),
}

_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・（gate を渡せば）その門番の記録の表を27本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss は触らない）＝14〜26本目・17本目の見本と重ねるとき。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が27本目の表で
       28本目の画を測る）。apply の前に**無かった名**も覚えて、restore で**消す**＝selftest のあとに27本目の名が本番へ残らない
       （fixture_ep15〜ep26・ep17 と同じ作り）。⚠️ `titan_fig.GEO` は触らない（27本目の地点は無い）"""
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


CUTS_SHA = "b62a7f94"      # 27本目の章ファイルが最後に live だった版（章ファイルを28本目の器に替える前＝git の `b62a7f94`＝28本目 ⑤b-1 の移し替えの merge）
_CUTS27 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def _footage27():
    """27本目の映像の台帳 `CLIPS`（`ref/ep27/clips.json`）と使う区間 `USE`・器の黒帯の割合 `PILLAR`（git の CUTS_SHA の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}`）を返す。
    🔴 27本目の章ファイルは `ss.vid` で `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を引く（フリー素材のカットは台帳の `"stock": true` を見て、ひかえの静止画の名を
    `ep27/stock/fb_<cid>.jpg` に決める）。本番の footage は28本目の表になった＝そのままだと27本目のフリー素材のカットは `ref/ep27/fb_<cid>.jpg`（無い名）の箱を
    決めに行って章ファイルが読み込みで落ちる。→ 章ファイルを読む間だけ、この表を footage に差す（`cuts_ep27` が戻す）。
    footage.py の `USE`・`PILLAR` は値だけの代入＝その2文だけを取り出して評価する（footage.py 全体は import しない）。
    ⚠️ 27本目の PILLAR は空（27本目 ⑤b-1 で空にしたまま・額装の引用は器の黒帯を額の中に見せる）＝空でも止めない形は残す。USE（2カット＝県警の動画の引用）と台帳が読めなければ止める"""
    import ast
    import json
    import subprocess
    p = subprocess.run(["git", "-C", str(ROOT), "show", f"{CUTS_SHA}:tools/footage.py"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 27本目の映像の使う区間を git の {CUTS_SHA} の tools/footage.py から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    ns = {}
    for node in ast.parse(p.stdout.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("USE", "PILLAR") for t in node.targets):
            exec(compile(ast.Module([node], []), f"footage_{CUTS_SHA}", "exec"), ns)
    use, pillar = ns.get("USE"), ns.get("PILLAR")
    clips_file = REF / "clips.json"
    if not use or pillar is None or not clips_file.exists():
        raise RuntimeError(f"🔴 27本目の映像の表が読めていない（USE {len(use or {})}・PILLAR {'無い' if pillar is None else len(pillar)}・"
                           f"{clips_file} {'ある' if clips_file.exists() else '無い'}）")
    return json.loads(clips_file.read_text(encoding="utf-8")), use, pillar


def cuts_ep27():
    """27本目の章ファイル（git の CUTS_SHA の `tools/cuts/`＝27本目の ss.py ごと）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。
    読む間だけ `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を27本目の表にする（`_footage27`＝本番の footage は28本目の表）。読み終えたら戻す。"""
    if _CUTS27:
        return _CUTS27[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    import footage as _FO
    clips24, use24, pillar24 = _footage27()
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 27本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts27_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep27 の写真・頁を読む＝根の下の作業場所の
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
    # 🔴 27本目は 107カット＋ed01＝SPEC 108（git の b62a7f94）。章ファイルが1本でも読めない（BROKEN）と SPEC が欠ける＝黙って一部で検算しない
    if broken or len(got[0]) != 107 or len(got[1]) != 108 or "c101" not in got[1]:
        raise RuntimeError(f"🔴 27本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}・読めない章 {sorted(broken)[:6]}）")
    _CUTS27.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を27本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で28本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep27()
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
        if s.get("cuts") is not None:          # apply_cuts() の分＝28本目の PLAN・SPEC へ戻す
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
