# -*- coding: utf-8 -*-
"""32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク）の型の値＝**門番の selftest の見本**（本番の表ではない）。

■ 2026-11-15（33本目 グレンフェルタワー火災の ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `139227a3` と同じ）
  ・`cuts/ss.py` の32本目の値＝説明カットの地の写真の明るさ（GROUND＝26点）・Google の衛星写真の表（SAT＝G01〜G08 の8画）と札の場所（GEO＝13点・
    補助 `_FAA_ARP`・`_FAA_RWY`・`_D6`＝場所の出どころの文）（どちらも `SAT.update(…)`／`GEO.update(…)` の文のまま）・飛んだ道と向きの矢印の線
    （SAT_LINES＝`_SL32` と `if _SL32.exists(): SAT_LINES.update(…)` の文のまま）と線の出典の断り（SAT_LINE_NOTE＝2回の代入の並びのまま）・
    升目の名簿（NEEDS_MASK＝5点）・台紙の縁でない暗い帯の名簿（SLIDE_NOT_MOUNT）・台紙の縁も暗い帯も無い回の言い分（SLIDE_NONE＝None）。
    32本目も空のままだった表（REC_DOCS・ILLU_*・AXIS_DOCS・AXI・QG・QB・PEOPLE_*・QDOC・QWHO・SLIDE_MOUNT・OCR_NOT_TEXT）と地図の言い分（SAT_NONE＝None）も、
    32本目の状態として持つ（17・23〜31本目の見本と同じ考え方）
  ・門番の記録の表（check_mech＝REC_M32〈札の型 `mech32.py` の記録の値＝誰の記録かの名と色・原文どおりの札・数・出さない言葉・見え方の表の値〉・
    check_sat＝REC_SAT_NUM〈空の代入と `REC_SAT_NUM.update(…)` の文＝札の数の4カット c303・c317・c406・c509〉・REC_SAT_PAGES〈抜き書きの道＝git の外〉・
    check_fuda＝EXC〈札の型の札の枚数の例外＝32本目も空〉）。
    check_axis・check_qty・check_boxes・check_illu・check_photo_edge・check_photo_mask は32本目で足した表が無い（check_photo_edge の名簿は ss の SLIDE_*＝上）＝この見本に入れない。
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を32本目の実物でも確かめている（check_mech の m32）＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は33本目の空の器にした
  （fixture_ep14〜ep31・ep17 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep32
      fixture_ep32.apply(sys.modules[__name__])   # その処理の中だけ ss・この門番の記録の表が32本目になる
      try: …（検算）
      finally: fixture_ep32.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14〜31本目・17本目の見本と重ねるとき（check_mech）は
      fixture_ep32.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと33本目の画に32本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。⚠️ ほかの回の見本（fixture_ep31 ほか）の積み荷とは別＝それぞれの restore で戻す。
■ 注意:
  ⚠️ 32本目の selftest のうち、**章ファイルの SPEC を読むもの**は check_mech の `_selftest_m32`（m32 のカット＝札の型と見え方の表）。`apply(gate)`＋`apply_cuts()`（32本目の章ファイルを
     git の `CUTS_SHA`＝`139227a3` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ32本目に入れ替える・git が無い所では止める＝fail closed）を使う（
     31本目の `_selftest_m31` と同じ）。描く側の表（`tools/mech32.py` の FU・VIEWS・SRC ほか）は型のモジュールの中の値＝本番に残した（cuts.ss を読まない）。
  ⚠️ 32本目の章ファイルは git の版の `tools/cuts/ss.py`（EP＝`ep32/`・32本目の値）ごと取り出して読む＝写真の名 `P("…")` は `ep32/…` のまま（本番の ss は `ep33/`）。
     ただし `ss.vid`・`ss.head`・`ss.tailv` は本番の **`footage.CLIPS`・`footage.USE`**（と `footage.PILLAR`）を引く（沿岸警備隊の監視カメラ VTS の13カット＝台帳 `ref/ep32/clips.json`）＝
     本番の footage は33本目の表なので、`cuts_ep32()` は章ファイルを読む間だけ footage の3つを32本目の表（台帳 `ref/ep32/clips.json`・使う区間 `USE` と黒帯の
     git の `139227a3` の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}` の2文を取り出して評価）に差し、読み終えたら戻す
     （`_footage32`＝17本目の `_footage17`・24〜31本目の `_footage24`〜`_footage31` と同じ）。32本目の footage の値は**ここに写していない**（git の `139227a3` が正本＝
     USE 13欄・NOGO の VC の1区間〈背景のコンコルド〉・PILLAR は空）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep32/credits.json`）・`REC_PAGES`（32本目の本番の文のまま＝`REF / "src" / "ep31_pages.txt"`＝32本目は使っていない道）は本番では REF から導く道＝
     この見本は32本目の道を持つ。
  ⚠️ `SLIDE_NOT_MOUNT`・`NEEDS_MASK` の鍵は **`ep32/` の名を文字で書いた**（本番の ss は `P(…)` で組んでいた＝EP が ep33 になると `ep33/…`〈無い名〉に化ける。
     fixture_ep17・ep22〜ep31 と同じ扱い）。説明の文は1字も変えていない（値＝git の `139227a3` の ss を評価した値）。
     `GROUND` の鍵は束の欄の名（`c1`・`stock/gk1` ほか）＝回の名を含まない＝そのまま（🔴 だから本番は必ず空にする＝33本目に同じ名があると黙って効く）。
  ⚠️ `if _SL32.exists(): SAT_LINES.update(…)` の文は `HERE`（ss では根）を読む＝この見本では `HERE = ROOT`（同じ根）と置いて文のまま写した＝import のときに
     `ref/ep32/sat_lines32.json`（git の中）があれば開く（無い作業ツリーでは SAT_LINES は空のまま＝32本目の本番と同じ振る舞い）。
     本番の ss は33本目の ⑤b-1 でも import のときに前の回のファイルを開かない（31本目 ⑤b-1 で決めた形＝スパースの作業ツリーで落ちない）。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝32本目は 1.14）は見本に入れない（16〜31本目・17本目の見本も入れていない）＝本番の ss は今の値のまま（33本目の束で取り直す）。
  ⚠️ 写真の束の定数のうち `TRIM`（`pages.json` から読む＝REF が替われば追う）・`PRIVATE_OUT`・`NG_PHOTOS` は見本に入れない（32本目も空）。
  ⚠️ `check_blank.ON_PURPOSE`（32本目は紙面6カット）は見本に入れない（29本目と同じ＝selftest が読まない・git の `139227a3` が正本）。`build_jiko.LAB_HOLD_EP` は回の名で引く＝見本に入れない。
  ⚠️ 型として本番に残した＝ss の関数（`sat`・`ax`・`qb`・`P`・`page`・`page_hl`・`vid`・`head`・`tailv`・`mv`・`mvz`・`tcam`・`gr`・`ground_lic_ok`・`is_private`・`check_frame_only`・`check_card_…`）・
     `SAT_CREDIT`・`GROUND_LIC`・`PRIVATE_DIR`・`SNS_NOTE`・`SNS_NOTE_BOX`・`SNS_NOTE_INK`・`PAGE_BLUR`（回をまたいで同じ）・
     check_mech の `judge_m32`・`_judge_fu`（表が空なら理由を出して止める入口）・check_sat の `_rec_page`・check_fuda の物差し（字数・字の大きさのしきい値）・
     描く側の型 `tools/mech32.py`・`titan_fig.m32`・`scene_jiko` の m32 の字幕の消しと原音（`orig_hold`）・`audio_mix` の原音を混ぜる仕組み（`ORIG_REL_DB`・`active_rms`）・
     footage の Ogg の出力シーク（`_seek_after_input`）・check_slide の OCR の取りこぼしの止め（どれも cuts を読まない＝型）。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep32"
HERE = ROOT        # ss の HERE（根）と同じ＝`_SL32 = HERE / …` と `if _SL32.exists(): SAT_LINES.update(…)` の文をそのまま読むため


# ══════════════════════════════════════════════════════
#  cuts/ss.py から（git の `139227a3` の ss.py の代入文をそのまま写した・`P("…")` だけ `"ep32/….jpg"`・`f"{EP}…"` だけ `"ep32/…"` の文字に）
# ══════════════════════════════════════════════════════
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"   # 型の定数（本番の ss に残した・SAT を組むための名＝SS_NAMES に入れない）

NEEDS_MASK: dict[str, str] = {
    "ep32/d68_3.jpg": "NTSB の救助の写真3（1月17日の桟橋のフェリー）＝船体の船の名（人の名）に升目（この回の線＝船の名も読ませない）",
    "ep32/c50.jpg": "博物館の格納庫の来館者（中景・正面を向く大人2人と子ども1人・CC0）＝顔だけ升目（全面で寄る＋説明カットの地6カット）",
    "ep32/c60.jpg": "運搬に付き添った博物館の車の後ろの扉の小さな4字（人の名前の見込み・CC0）＝字に升目",
    "ep32/c32.jpg": "警察のダイバーの胸の名札2つ（試し焼きのあとの2回目の原寸の切り出しで名前が読めた・PD）＝字に升目（顔は公的な任務＝そのまま）",
    "ep32/c9.jpg": "夜の作業の警察官の左胸の札（2行の字・CC BY 2.0）＝字に升目（全面で寄ると大きくなる）",
}
SLIDE_MOUNT: dict[str, str] = {}
SLIDE_NOT_MOUNT: dict[str, str] = {
    "ep32/c9.jpg": "夜の作業の写真＝上の 5.0% は夜の空（陸軍工兵隊の船の上）",
    "ep32/stock/x818.jpg": "暗い客室の空いた座席（⑤c' で替えた Pexels 4061487）＝左の 5.0% は影の中の客室の壁と窓の板（候補の見本で見た）",
    "ep32/c40.jpg": "夜の岸壁のそばの機体＝右の 5.0% は明かりの消えたビルの壁（夜）",
    "ep32/c41.jpg": "引き上げたあとの機体（夜）＝左・上・右の 5% は夜の空と木の枝の影",
    "ep32/c46.jpg": "引き上げられる機体（夜・BY-SA＝額装だけ）＝上・右の 5% は夜の空とクレーンの影",
    # 🆕 ⑤b-3（11-10）：紙面の束（白い紙）＝暗い帯は紙面の罫（1400px のシートで見た・額装だけ＝全面にしない）
    "ep32/r203_c320.jpg": "付録C の手順書の見出し「ENG DUAL FAILURE」の上下の罫＝上の 3.4%（紙面の中身・台紙の縁でない）",
    "ep32/r40_c702.jpg": "報告書の表2 の左右の縁の罫＝左 3.3%・右 2.9%（紙面の中身・台紙の縁でない）",
    # 🆕 ⑤b-4a（11-10）：イメージの写真（Pexels・640px の全数と原寸で見た）＝暗い帯は写真の中身（暗い操縦室・客席・夕方の地面）・台紙の縁でない
    "ep32/stock/ga1.jpg": "レーダーの画面のある部屋（地）＝下の 5.0% は操作の台の暗い影",
    "ep32/stock/gk1.jpg": "ぼけた計器と推力のレバー（地）＝上の 5.0%・右の 1.5% は暗い操縦室の天井",
    "ep32/stock/gm1.jpg": "操縦席の操縦士の後ろ姿（地）＝左の 5.0% は操縦士の頭とヘッドセットの影",
    "ep32/stock/gt1.jpg": "暗い赤い客席の列（地）＝左・右・下の 5% は暗い客席",
    "ep32/stock/x310.jpg": "暗い操縦室のレバーと操作盤＝左・上・右の 5% は暗い操縦室（窓は下の y 0.54〜）",
    "ep32/stock/x314.jpg": "操縦席の2人の後ろ姿＝上・右・下の 5% は天井の操作盤と制服と座席の影",
    "ep32/stock/x420.jpg": "夕方の滑走路の灯り＝下の 5.0% は暗い地面",
    "ep32/stock/x423.jpg": "シミュレーターの操縦席＝左の 2.9%・右の 5.0% は暗い操縦席の内側",
    "ep32/stock/x502.jpg": "操縦席から見た滑走路への進入＝下の 5.0% は操縦室の窓の枠（暗い）",
    "ep32/stock/x504.jpg": "古い型の操縦室の2人の後ろ姿＝上の 4.9% は天井の操作盤・下の 5.0% は座席の影",
    "ep32/stock/x508.jpg": "操縦席から雲の上を見る操縦士の影＝暗い帯は操縦士の影と操縦室の内側（暗い）",
    "ep32/stock/x517.jpg": "映写の幕と赤い客席＝上の 2.3% は幕の上の暗い壁・下の 4.9% は座席の影",
    # 🆕 ⑤b-4b（11-11）：イメージの写真（Pexels・640px の全数と原寸で見た）＝暗い帯は写真の中身・台紙の縁でない
    "ep32/stock/gb2.jpg": "重ねた白い紙の角（地・白黒）＝左の 5.0% は紙の束の暗い影",
    "ep32/stock/x602.jpg": "手帳の見出しの札＝左・右・下の 5% は札のまわりの黒い地（暗い背景）",
    "ep32/stock/x808.jpg": "窓ぎわの空いた座席＝下の 2.6% は座席の下の暗い影",
    "ep32/stock/x914.jpg": "青い座席の列＝左・下の 5% は手前の座席の暗い背",
    "ep32/stock/xa03.jpg": "雪の岸と冬の川面＝下の 4.9% は水面に映った木の暗い影",
    "ep32/stock/xa09.jpg": "操縦席から見た雲の上の朝日＝下の 5.0% は暗い操作盤（画面の字は窓の外）",
}
SLIDE_NONE = None
OCR_NOT_TEXT: dict[str, list] = {}
SAT = {}
GEO = {}
SAT.update({
    "G01": dict(file="ep32/photo/gmap_g01_newyork.png", ll=(40.815, -73.955), z=12, md5="911610d20eac810b45c197c6d1bb0616", credit=SAT_CREDIT),
    "G02": dict(file="ep32/photo/gmap_g02_lga_city.png", ll=(40.785, -73.915), z=13, md5="20a2eb8746697e65439b57db1d4016f2", credit=SAT_CREDIT),
    "G03": dict(file="ep32/photo/gmap_g03_lga_runways.png", ll=(40.7775, -73.8725), z=14, md5="688faf508c82b5d928d0e6f5962e2033", credit=SAT_CREDIT),
    "G04": dict(file="ep32/photo/gmap_g04_birdstrike.png", ll=(40.8125, -73.882), z=13, md5="7b8b0dd89a17763f1fecb5bc0f995e35", credit=SAT_CREDIT),
    "G05": dict(file="ep32/photo/gmap_g05_top_turn.png", ll=(40.862, -73.915), z=13, md5="541260dc1838b12160042bb305a4070a", credit=SAT_CREDIT),
    "G06": dict(file="ep32/photo/gmap_g06_teterboro.png", ll=(40.835, -73.995), z=13, md5="07bbe775c9ddac181290a379ad45004c", credit=SAT_CREDIT),
    "G07": dict(file="ep32/photo/gmap_g07_hudson.png", ll=(40.805, -73.985), z=13, md5="a1fb95e9e705a506b0445f7dd4392141", credit=SAT_CREDIT),
    "G08": dict(file="ep32/photo/gmap_g08_ditch_ferry.png", ll=(40.7745, -74.006), z=14, md5="e866b5a68e405e7636e0c1a6259302e6", credit=SAT_CREDIT),
})
_FAA_ARP = "FAA の公開の資料（NASR 2026-10-29 の APT_BASE＝空港の基準点）"
_FAA_RWY = "FAA の公開の資料（NASR 2026-10-29 の APT_RWY_END＝滑走路の端の座標）"
_D6 = "報告書の座標（NTSB のドケット #6＝運航の事実の報告書 §4.0 の緯度経度）"
GEO.update({
    "lga": dict(ll=(40.77724222, -73.87260555), src="報告書（LaGuardia Airport＝出発した空港）", how=_FAA_ARP),
    "teb": dict(ll=(40.85010194, -74.06083333), src="報告書（Teterboro Airport）", how=_FAA_ARP),
    "lga04": dict(ll=(40.76916258, -73.88411902), src="報告書（離陸の滑走路4・付録B の runway four）", how=_FAA_RWY),
    "lga22": dict(ll=(40.78543666, -73.87067336), src="報告書（the approach end of runway 22 at LGA・試しの滑走路22）", how=_FAA_RWY),
    "lga13": dict(ll=(40.78229586, -73.87851916), src="報告書（付録B の runway one three・試しの滑走路13）", how=_FAA_RWY),
    "lga31": dict(ll=(40.77207144, -73.85711158), src="報告書（付録B の runway three one）", how=_FAA_RWY),
    "teb01": dict(ll=(40.83868208, -74.0603705), src="報告書（付録B の runway one at Teterboro）", how=_FAA_RWY),
    "teb19": dict(ll=(40.85785627, -74.05895641), src="報告書（試しの TEB runway 19）", how=_FAA_RWY),
    "teb24": dict(ll=(40.85773911, -74.05409561), src="報告書（the approach end of runway 24 at TEB）", how=_FAA_RWY),
    "bird": dict(ll=(40.84810, -73.876089), src="報告書（鳥とぶつかった所＝2,818 feet agl）", how=_D6),
    "ditch": dict(ll=(40.771297, -74.005697), src="報告書（ハドソン川への着水）", how=_D6),
    # いちばん高い所＝報告書 p64「1527:30 … highest altitude of about 3,060 feet」の時刻を、レーダー（#85 p22）の 15:27:27.11 と 15:27:31.76 の点のあいだに時刻で割った位置
    "top": dict(ll=(40.863805, -73.880435), src="報告書 p64（1527:30・about 3,060 feet）",
                how="報告書の時刻をレーダーの記録（NTSB のドケット #85 p22）の点のあいだに割った位置"),
    # フェリー乗り場＝Google マップの地点「Port Imperial Ferry Terminal」（検索の !3d!4d・2026-11-10。同じ検索の「Port Imperial / Weehawken」ほか3点は 50 メートルの内）
    "ferry": dict(ll=(40.7765042, -74.0113094), src="ドケット #68（フェリーの聴取の Port Imperial）",
                  how="一般の座標（Google マップの地点「Port Imperial Ferry Terminal」）"),
})
SAT_LINES = {}
SAT_LINE_NOTE = ""
_SL32 = HERE / "ref" / "ep32" / "sat_lines32.json"
if _SL32.exists():
    SAT_LINES.update({k: tuple(tuple(p) for p in v) for k, v in json.loads(_SL32.read_text(encoding="utf-8")).items()})
SAT_LINE_NOTE = "線はレーダーの記録（NTSB）から描いた"
SAT_NONE = None
REC_PAGES = REF / "src" / "ep31_pages.txt"    # 部品の出典（`rec=`）を当てる原文（git の外＝手元だけ）
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
GROUND = {"c1": 0.37, "c14": 0.30, "c16": 0.39, "c18": 0.30, "c26": 0.28, "c36": 0.28, "c61": 0.24,
          "c13": 0.29, "c21": 0.29, "c31": 0.39, "c32": 0.28, "c49": 0.28, "c50": 0.28,
          "stock/ga1": 0.29, "stock/gb1": 0.28, "stock/gb2": 0.33, "stock/gc1": 0.32, "stock/gf1": 0.28, "stock/gk1": 0.29, "stock/gk2": 0.30,
          "stock/gl1": 0.33, "stock/gm1": 0.29, "stock/gr1": 0.33, "stock/gr2": 0.32, "stock/gs1": 0.37, "stock/gt1": 0.28}

SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "QG", "QB",
            "PEOPLE_ORDER", "PEOPLE_SETS", "PEOPLE_REC", "PEOPLE_CUTS", "QDOC", "QWHO", "SAT", "GEO", "SAT_LINES", "SAT_LINE_NOTE", "SAT_NONE",
            "NEEDS_MASK", "SLIDE_MOUNT", "SLIDE_NOT_MOUNT", "SLIDE_NONE", "OCR_NOT_TEXT", "GROUND")


# ══════════════════════════════════════════════════════════
#  門番 check_sat から（git の `139227a3` の check_sat.py の代入文と update の文をそのまま写した）
# ══════════════════════════════════════════════════════════
REC_SAT_NUM = {}
REC_SAT_PAGES = Path(__file__).resolve().parent.parent / "ref" / "ep32" / "src" / "news_frag_v2.txt"
REC_SAT_NUM.update({
    "c303": {"約7キロ": (("抜き書き p19", "4.5 miles north-northwest of the approach end of runway 22"),)},
    "c317": {"約930メートル": (("抜き書き p64", "highest altitude of about 3,060 feet"),)},
    "c406": {"滑走路31": (("抜き書き p192", "left traffic for runway three one"),),
             "滑走路4": (("抜き書き p193", "runway four's available"),)},
    "c509": {"滑走路13": (("抜き書き p106", "a return to LGA runway 13 was attempted after a 35-second delay"),)},
})


# ══════════════════════════════════════════════════════════
#  門番 check_mech から（git の `139227a3` の check_mech.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
REC_M32 = dict(
    src=dict(hokoku=("NTSB の報告書", "ntsb"), docket=("NTSB の公開ドケット", "tsb"), ap=("AP 通信", "company")),
    ng=("犠牲", "死亡", "死者", "亡くな", "208秒"),
    vals=dict(
        # ── 第1章
        c203=(("報p23", "57歳", "The captain, age 57"), ("報p24", "1万9,663時間", "19,663 total flight hours"),
              ("報p24", "うち A320", "4,765 hours of which were in A320 airplanes"), ("報p24", "4,765時間", "4,765 hours of which were in A320 airplanes")),
        c205=(("報p25", "49歳", "The first officer, age 49"), ("報p25", "1万5,643時間", "15,643 total flight hours"),
              ("報p25", "うち A320", "37 hours in A320 airplanes"), ("報p25", "37時間", "The first officer had 37 hours in A320 airplanes"),
              ("報p25", "資格は2008年12月31日", "received his initial A320 type rating on December 31, 2008")),
        c207=(("報p26", "51歳・57歳", "Flight attendant A, age 51 … Flight attendant C, age 57"), ("報p26", "58歳", "Flight attendant B, age 58"),
              ("報p26", "2人", "forward jumpseat"), ("報p26", "1人", "(aft, center aisle)"), ("計", "26年以上", "初めの訓練の年から2009年1月まで＝26年・38年・28年")),
        c209=(("報p53", "4つ", "four floor-level Type I exits … Each of these exits was equipped with a door-mounted, automatically inflating Type II slide/raft"),
              ("報p55", "人数分", "a life vest for each airplane occupant")),
        c213=(("報p18", "操縦する人", "the pilot flying (PF)"), ("報p18", "見守る人", "the pilot monitoring (PM)")),
        # ── 第2章
        c311=(("報p19", "APU", "The APU provides an additional source of electrical power for the airplane"),
              ("報p19", "もう1つの電気の源", "an additional source of electrical power")),
        c313=(("報p104", "約12秒", "about 12 seconds after the bird strike"),),
        c315=(("報p19", "QRH", "get the QRH [quick reference handbook] loss of thrust on both engines"),),
        c319=(("報p19", "1549便", "the flight number was 1549"), ("報p19", "1539", "the flight number was 1549 not 1539"),
              ("報p19", "正しくは1549", "the flight number was 1549 not 1539")),
        c321=(("報p19", "時速約560キロ", "the optimum minimum airspeed of 300 kts"), ("報p19", "300ノット", "airspeed optimum relight. three hundred knots"),
              ("報p19", "時速約400キロ", "the maximum airspeed reached by the airplane after the bird ingestion was 214 knots"),
              ("報p19", "214ノット", "214 knots (kts)")),
        # ── 第3章
        c402=(("報p18", "1549便", "the flight crew"), ("報p18", "出発の管制", "LGA departure controller")),
        c405=(("報p20", "15:28:25", "At 1528:25"), ("報p20", "左のエンジンが少し戻ってきた", "The left one’s [engine] coming back up a little bit."),
              ("報p97", "飛び続ける力は出せず", "neither engine was able to produce sufficient power to sustain flight")),
        c410=(("報p20", "テターボロ", "off your right side is Teterboro Airport [TEB]"), ("報p20", "そうする", "the captain replied, “yes.”")),
        c417=(("報p196", "すまない、もう一度", "DEP I'm sorry say again Cactus?"),),
        c419=(("報p20", "15:29:53", "At 1529:53"), ("報p20", "レーダーで見失う", "he had lost radar contact with the airplane")),
        # ── 第4章
        c503=(("報p66", "風・気温", "including winds, temperature"), ("報p67", "鳥とぶつかる少し前", "shortly before the bird strike")),
        c507=(("報p67", "8回", "In eight of the 15 runs (53 percent), the pilot successfully landed after making an immediate turn"),
              ("計", "7回", "15回のうち8回が降りられた＝残る7回"), ("報p67", "15回の試し", "Of the 15 remaining runs")),
        c510=(("計", "15:27:11", "鳥とぶつかる"), ("計", "15:27:33", "管制へ第一報"), ("計", "15:27:50", "手順書を読み始める"),
              ("計", "22秒", "15:27:11 から 15:27:33 まで"), ("計", "39秒", "15:27:11 から 15:27:50 まで")),
        c513=(("報p105", "現実的な選択ではなかった", "it would not have been a realistic choice"),
              ("報p106", "ほかの道をすべて消す取り消せない選択", "it would have been an irrevocable choice, eliminating all other options")),
        c518=(("通", "調査を率いた元の責任者", "who led the National Transportation Safety Board's investigation"),
              ("通", "誰にも恥をかかせるつもりはまったくなかった", "We weren’t out to embarrass anybody at all.")),
        c522=(("報p67", "35秒", "after a 35-second delay"), ("報p67", "それを足した1回", "runway 13 at LGA) after a 35-second delay"),
              ("ド#35p18", "滑走路の手前", "Hard landing just short of threshold"),
              ("報p106", "生き残れる見込みのいちばん高い道", "provided the highest probability that the accident would be survivable")),
        # ── 第5章
        c601=(("報p68", "操縦室の画面", "displayed on the ECAM displays in the cockpit"),
              ("報p69", "紙の冊子を開く", "directed the PM to the Engine Dual Failure checklist procedures contained in the QRH")),
        c603=(("報p69", "1つ目", "Part 1"), ("報p70", "2つ目", "Part 2"), ("報p70", "3つ目", "Part 3"), ("画", "1ページ目"), ("画", "3ページ目")),
        c605=(("報p69", "飛ぶ時間の多くは高い空", "Airbus airplanes spend much more time at higher altitudes"),
              ("報p69", "検討していなかった", "it had not considered developing a dual-engine failure checklist for use at a low altitude")),
        c608=(("報p104", "2005年", "In 2005, Airbus amended the Engine Dual Failure checklist"), ("報p104", "2本立てに", "two parallel steps"),
              ("報p104", "長い手順書に", "it resulted in a lengthy checklist")),
        c610=(("報p70", "a 点火 … 入れる", "a. Start engine ignition"), ("報p70", "b 推力のレバー … 確かめる", "b. Confirm thrust levers at idle"),
              ("報p70", "c 速さ 300ノットを保つ", "c. Maintain optimum relight airspeed of 300 kts"),
              ("報p70", "d 降りる場所 … 決める", "d. Determine a landing strategy")),
        c614=(("報p104", "1つ目の大半まで", "able to complete most of part 1 of the checklist"),
              ("報p104", "2つ目と3つ目", "they were not able to start parts 2 and 3 of the checklist"), ("画", "1ページ目"), ("画", "3ページ目")),
        c617=(("報p73", "約910メートル", "configured for a ditching before 3,000 feet"), ("画", "約610メートル", "At 2000’ AGL"),
              ("報p73", "機首 約11度", "Touchdown with approximately 11 degrees of pitch")),
        c619=(("報p77", "水面より下の弁を閉じる", "closes all of the valves below the water line"),
              ("報p77", "長く浮くのを助ける", "to help the airplane float longer")),
        c621=(("ド#7p6", "地上の座学だけ", "The only training for ditching was given in ground school"),
              ("ド#7p6", "着水の訓練なし", "There was no training in the simulator"),
              ("ド#7p6", "時間がある前提", "All guidance he received for ditching implied that they had time")),
        c623=(("報p71", "APU を始動する", "k. Start APU"), ("報p70", "前に a〜j の10項目", "a. Start engine ignition … j. Verify that crew oxygen masks are ON"),
              ("報p105", "順番どおりなら行われず", "This critical step would not have been completed if the flight crew had simply followed the order"),
              ("画", "2ページ目の k"), ("画", "3ページ目")),
        c626=(("報p105", "低い所の故障用の手順書", "a checklist that addressed a dual-engine failure occurring at a low altitude"),
              ("報p105", "見込みはより高い", "they would have been more likely to have completed that checklist")),
        c628=(("報p142", "手順書の作り方の指針", "the order of critical items in the checklist"),
              ("報p142", "低い所の故障を訓練に", "include a dual-engine failure scenario occurring at a low altitude"),
              ("報p142", "座学とシミュレーター", "in initial and recurrent ground and simulator training")),
        c630=(("計", "第10章", "橋の1行"),),
        # ── 🆕 ⑤b-6 から前倒しの5カット（地 gf1・gk2・gl1・gr2 の明るさを測るため）
        c703=(("報p64", "約80メートル", "as the airplane was descending through 270 feet"),
              ("報p64", "レバーを2に", "the flap lever was moved to the CONF 2 position")),
        c705=(("報p106", "最後の約60メートル", "during the last 200 feet"),
              ("報p106", "下限より時速約30キロ遅い", "about 15 to 19 knots below VLS")),
        c711=(("報p65", "迎え角の守り", "was in alpha-protection mode from 150 feet to touchdown"),),
        ca04=(("報p96", "1つ目", "the ditching occurred in good visibility conditions on calm water"),
              ("報p96", "2つ目", "was executed by a very experienced flight crew"),
              ("報p96", "とても経験のある乗員", "a very experienced flight crew")),
        cb13=(("勧", "2018年", "A-10-085 受け入れられる対応 2018-01-19"), ("勧", "受け入れられる対応", "A-10-085 受け入れられる対応"),
              ("報p143", "救命胴衣の決まり", "Revise the life vest performance standards")),
        # ── 🆕 ⑤b-6（2026-11-11）：模式 後半28＋型の図23。記号は ⑤b-5 と同じ＋勧＝勧告の控え（`src/carol/carol_dca09ma026.json`・2026-11-09）・
        #    官＝連邦官報 2023-06413（`src/web/fr2023_06413.txt`）。書き起こしの時刻は付録の頁（p189〜p196）。換算は mech32 の ⑤b-6 の頭
        # 第1章
        c210=(("報p54", "20機", "The accident airplane was 1 of 20 A320s equipped as an EOW airplane"),
              ("報p54", "A320 75機のうち", "in the US Airways fleet of 75 A320s"),
              ("報p54", "積む決まりなし", "Non-EOW airplanes are not required to carry passenger life vests, slide/rafts, or survival kits"),
              ("報p55", "この便", "The accident flight was a non-EOW flight")),
        c214=(("報p18", "15:25:51", "The captain contacted the departure controller at 1525:51"),
              ("報p18", "約210メートル", "advising him that the airplane was at 700 feet"),
              ("報p18", "約4,600メートル", "The controller then instructed the flight to climb to and maintain 15,000 feet")),
        # 第2章
        c301=(("報p19", "15:27:10", "at 1527:10.4, the captain stated"), ("報p19", "鳥だ", "“birds.”"),
              ("画", "12"), ("画", "3"), ("画", "6"), ("画", "9")),
        c306=(("報p97", "約3.8〜4.2キロ", "The average weight of a male Canada goose is from 8.4 to 9.2 pounds"),
              ("報p97", "約3.3〜3.5キロ", "the average weight of a female goose is from 7.3 to 7.8 pounds"),
              ("報p97", "約3.6キロのガン", "Canada geese weighing about 8 pounds each"),
              ("報p97", "少なくとも2羽ずつ", "each engine ingested at least two Canada geese")),
        c307=(("報p34", "約1.8キロ", "The large-bird ingestion criterion for CFM56-5B4/P-sized engines was a single, 4-pound bird"),
              ("報p34", "1羽", "a single, 4-pound bird"), ("報p97", "約3.6キロ", "weighing about 8 pounds each"),
              ("計", "約2倍の重さ", "8ポンド÷4ポンド")),
        c308=(("報p64", "82%", "the left engine decelerated from 82 to 35 percent N1"), ("報p64", "35%", "from 82 to 35 percent N1"),
              ("報p64", "15%", "the right engine decelerated from 82 to 15 percent N1"),
              ("報p17", "押す力はほぼ残らない", "an almost complete loss of thrust in both engines")),
        c323=(("報p19", "15:27:33", "At 1527:33, the captain reported the emergency"), ("報p196", "15:29:28", "15:29:28 RDO-1"),
              ("報p196", "ハドソン川に降りる", "we're gonna be in the Hudson."), ("計", "約2分", "15:27:33 から 15:29:28 まで＝1分55秒")),
        # 第3章
        c407=(("報p19", "unable", "the captain responded, “unable.”"), ("報p196", "we can't do it", "15:29:25 RDO-1 we can't do it."),
              ("報p19", "滑走路13のとき", "asked the captain if he wanted to try to land on runway 13 at LGA if it was available"),
              ("報p19", "降りるかの問い", "if he wanted to try to land on runway 13")),
        c422=(("報p19", "15:27:33", "At 1527:33, the captain reported the emergency"),
              ("報p105", "15:28:11", "at 1528:11, the captain reported to ATC that he did not think they would be able to land at LGA"),
              ("報p192", "15:28:35", "15:28:35 RDO-1 unable."), ("報p193", "15:28:50", "15:28:49.9 RDO-1 I'm not sure we can make any runway"),
              ("報p196", "15:29:25", "15:29:25 RDO-1 we can't do it."), ("報p196", "15:29:28", "15:29:28 RDO-1 we're gonna be in the Hudson."),
              ("報p191", "滑走路13は", "15:28:10.6 RDO-1 we're unable. we may end up in the Hudson."),
              ("報p192", "滑走路31も", "its gonna be left traffic for runway three one"), ("報p193", "滑走路4も", "runway four's available"),
              ("計", "2分17秒", "15:27:11 から 15:29:28 まで")),
        # 第4章
        c505=(("報p67", "20回", "20 runs were performed in the engineering simulator"),
              ("報p67", "5回を外す", "Five of the 20 runs were discarded because of poor data or simulator malfunctions"),
              ("報p67", "15回", "Of the 15 remaining runs"), ("報p67", "滑走路22", "runway 22 at LGA"), ("報p67", "6回", "in 6, the pilot attempted to land on runway 22"),
              ("報p67", "滑走路13", "runway 13 at LGA"), ("報p67", "7回", "in 7, the pilot attempted to land on runway 13"),
              ("報p67", "滑走路19", "runway 19 at TEB"), ("報p67", "2回", "in 2, the pilot attempted to land on runway 19 at TEB")),
        c506=(("報p67", "8回・53%", "In eight of the 15 runs (53 percent)"), ("報p67", "15回のうち降りられた", "the pilot successfully landed"),
              ("報p67", "6回中2回", "two of the six runs to land on runway 22 at LGA"), ("報p67", "7回中5回", "five of the seven runs to land on runway 13 at LGA"),
              ("報p67", "2回中1回", "one of the two runs to land on runway 19 at TEB"),
              ("報p67", "滑走路22", "runway 22 at LGA"), ("報p67", "滑走路13", "runway 13 at LGA")),
        # 第5章
        c607=(("報p104", "約6,100メートル", "assuming that a dual-engine failure occurred at a high altitude (above 20,000 feet)"),
              ("報p19", "約860メートル", "2,818 feet"), ("報p18", "1549便", "US Airways flight 1549"), ("計", "約7分の1", "2,818 ÷ 20,000")),
        c615=(("報p105", "約3分の1", "only able to complete about one-third of the Engine Dual Failure checklist"),
              ("画", "1ページ目"), ("画", "2ページ目"), ("画", "3ページ目")),
        c624=(("報p105", "電気をつくる", "ensuring that a primary source of electrical power was available to the airplane"),
              ("報p105", "ノーマル・ロー", "the airplane remained in normal law"),
              ("報p105", "失速を防ぐ守り", "maintained the flight envelope protections, one of which protects against a stall")),
        # 第6章
        c707=(("報p107", "鳴らなかった", "the low-speed warning was inhibited by the GPWS warnings"),
              ("報p20", "15回", "the two systems transmitted a total of 15 alerts"), ("計", "約85秒で", "15:29:14.9 から 15:30:40.1 まで＝85.2秒")),
        c709=(("報p21", "15:30:24", "At 1530:24, the GPWS issued"),
              ("報p21", "地面、地面、機首を上げろ", "a “terrain, terrain” warning followed by “pull up,”"),
              ("報p201", "録音が終わるまで", "[\"pull up\" repeats until the end of the recording]")),
        c712=(("報p65", "約45メートルから下", "in alpha-protection mode from 150 feet to touchdown"),
              ("報p65", "約30メートルから下", "attenuated the effect of the pilot’s airplane nose-up (ANU) sidestick inputs below 100 feet radio altitude"),
              ("報p65", "エアバスの再現", "The Airbus simulation indicated")),
        c713=(("報p115", "いちばんの性能", "the airplane did provide maximum performance for the weight and configuration at that time"),
              ("報p115", "失速の心配なく引けた", "pull full aft on the sidestick without the risk of stalling the airplane"),
              ("報p65", "機首上げの効きを弱めた", "attenuated the effect of the pilot’s airplane nose-up (ANU) sidestick inputs")),
        c715=(("報p65", "15:30:43", "remaining there until touchdown at 1530:43"), ("報p65", "9.5度", "with a pitch angle of 9.5°"),
              ("報p65", "時速約230キロ", "touched down on the Hudson River at an airspeed of 125 KCAS"),
              ("報p65", "毎秒約3.8メートル", "the airplane ditched with a descent rate of 12.5 fps")),
        c716=(("報p95", "毎秒約1.1メートル", "the descent rate of 3.5 fps assumed during ditching certification"),
              ("報p95", "毎秒約3.8メートル", "the airplane’s descent rate at the time it impacted the water was 12.5 fps"),
              ("報p95", "3倍をこえる", "more than three times the descent rate"), ("報p18", "1549便", "US Airways flight 1549"),
              ("報p95", "後ろの胴体に", "resulting in external pressures on the aft fuselage")),
        c719=(("報p52", "左のすね", "laceration to her lower left leg"), ("報p52", "12センチ", "12-centimeter-long"),
              ("報p52", "5センチ", "5-centimeter-deep"), ("報p52", "手術で閉じた", "that required surgery to close")),
        c721=(("報p138", "着水の前提をすべて", "attain all of the Airbus ditching parameters"), ("報p138", "見込みは低い", "it is possible but unlikely"),
              ("報p138", "胴体の損傷の一因", "this difficulty contributed to the fuselage damage")),
        c723=(("報p140", "推力なしで届くか確かめず", "without determining whether pilots could attain the ditching parameters without engine thrust"),
              ("報p140", "着水の降り方", "guidance on ditching techniques"),
              ("報p140", "思う速さを保ちにくい", "difficulty maintaining his intended airspeed on final approach"),
              ("報p140", "緊急で手いっぱい", "the task saturation resulting from the emergency situation")),
        # 第7章
        c802=(("報p58", "15:30:43", "By using the time of initial impact as 1530:43"), ("報p58", "15:30:58", "1530:58 – left overwing exits opened"),
              ("報p58", "15:31:06", "1531:06 – door 1L opened"), ("報p58", "15:31:11", "1531:11 – door 1R opened"),
              ("報p58", "15:31:16", "1531:16 – the 1R slide/raft fully deployed"), ("報p59", "15:31:26", "1531:26 – 1L slide/raft began to inflate")),
        c804=(("報p57", "途中で閉まりかけた", "door 1R started to close during the evacuation"),
              ("報p57", "約30センチ入り込む", "intruding about 12 inches into the doorway"),
              ("報p57", "力のありそうな男性", "she assigned an “able-bodied” man to hold the door")),
        c807=(("報p58", "混み合った", "some of the passengers were bottle-necked at the overwing exits"),
              ("報p58", "呼び寄せた", "the flight attendants called them forward"),
              ("報p58", "前の右の扉から出た", "Flight attendant B also exited from door 1R")),
        c809=(("報p58", "残る人がいないか", "inspected the cabin to ensure that no more passengers or crewmembers were on board"),
              ("報p58", "前の左のすべり台へ", "exited the airplane onto the 1L slide/raft")),
        c810=(("報p124", "約64人", "about 64 occupants were rescued from the forward slide/rafts"),
              ("報p124", "約87人", "about 87 occupants were rescued from the wings and off-wing ramp/slides"),
              ("報p124", "前の2つのすべり台", "the forward slide/rafts"),
              ("報p124", "立つ場所はほぼ残らず", "the wings were very near to, if not at, standing capacity")),
        c813=(("報p41", "マイナス7度", "temperature -7° C"), ("報p41", "セントラルパーク 15:51", "Central Park … The 1551 observation"),
              ("報p41", "5.2度", "5.2° C (41.36° F)"), ("報p120", "約マイナス17度", "a 2° F wind chill factor")),
        c816=(("報p61", "2人", "Two additional passengers retrieved and donned their life vests before impact"),
              ("報p61", "10人", "5 passengers (3 percent) reported retrieving life vests from under their seats after impact … An additional 5 passengers"),
              ("報p61", "21人", "21 passengers (14 percent) reported being given a life vest"),
              ("報p61", "77人", "77 passengers (53 percent) retrieved seat cushions during the evacuation")),
        c819=(("報p59", "146人", "The NTSB contacted 146 of the 150 passengers"), ("報p59", "150人のうち", "146 of the 150 passengers"),
              ("報p61", "25人", "25 passengers (17 percent) reported watching most of the preflight safety demonstration"),
              ("報p61", "一部を見た 19人", "an additional 19 passengers (13 percent) reported watching some of the demonstration"),
              ("報p61", "12人", "12 passengers (8 percent) reported reading the safety information card")),
        c820=(("報p54", "いかだ1つ", "Each slide/raft"), ("報p54", "44人用", "Each slide/raft was rated to carry 44 passengers"),
              ("報p124", "この装備が無ければ", "If the airplane had not been EOW equipped"),
              ("報p124", "約64人のいかだは無かった", "the rafts that held those occupants would not have been available … about 64 occupants")),
        c822=(("計", "最初の船", "橋の1行"),),
        # 第8章
        c909=(("報p59", "約4分", "1534:40 – first vessel arrived on scene"), ("報p62", "最初のフェリー", "the first NY WW vessel arrived on scene about 1534"),
              ("報p120", "約20分", "all of the occupants were rescued within about 20 minutes of the ditching"),
              ("報p59", "24分", "1554:43 – last vessel departed"), ("報p59", "15:54:43", "1554:43 – last vessel departed with last rescued passengers")),
        c913=(("報p52", "足の傷", "laceration to her lower left leg"), ("報p52", "胸の骨の端の骨折", "One of the passengers sustained a fractured xiphoid process"),
              ("報p52", "低体温症", "The other passenger suffered hypothermia"),
              ("報p52", "2日後の夕方まで入院", "was not released from the hospital until about 1645 … January 17, 2009"),
              ("報p53", "2人", "one of these passengers sustained a fractured left shoulder and that the other passenger sustained a fractured right shoulder"),
              ("報p53", "肩の骨折", "a fractured left shoulder … a fractured right shoulder")),
        c918=(("報p63", "救助の指揮所", "established an incident command post in New Jersey at the Port Imperial Ferry Terminal"),
              ("報p63", "ニュージャージー側", "in New Jersey"), ("報p63", "沿岸警備隊", "the USCG assumed incident command"),
              ("報p62", "フェリー", "the first NY WW vessel arrived on scene"), ("報p63", "消防", "Marine 1 Alpha, FDNY")),
        # 第9章
        ca08=(("報p140", "判断と連携", "the decision-making of the flight crewmembers and their crew resource management"),
              ("報p140", "偶然あった", "the fortuitous use of an airplane that was equipped for an extended overwater flight"),
              ("報p140", "速い誘導", "the performance of the cabin crewmembers while expediting the evacuation of the airplane"),
              ("報p140", "近さと早さ", "the proximity of the emergency responders to the accident site and their immediate and appropriate response")),
        ca10=(("報p137", "所見15", "15. The captain’s decision to ditch on the Hudson River"),
              ("報p137", "川を選んだ判断", "The captain’s decision to ditch on the Hudson River rather than attempting to land at an airport"),
              ("報p137", "所見14", "14. Despite being unable to complete the Engine Dual Failure checklist, the captain started the auxiliary power unit"),
              ("報p137", "所見18", "18. The captain’s decision to use flaps 2 for the ditching"),
              ("報p137", "フラップ2は妥当", "use flaps 2 for the ditching, based on his experience and perception of the situation, was reasonable")),
        ca12=(("報p146", "着水には準備の時間", "Those criteria state that a ditching allows “some time” for preparation"),
              ("報p146", "1549便には、ほとんど何をする時間もなかった", "In the case of US Airways 1549, there was insufficient time for much of anything")),
        ca14=(("報p96", "よい見通しと静かな水面", "the ditching occurred in good visibility conditions on calm water"),
              ("報p96", "経験のある乗員", "was executed by a very experienced flight crew"),
              ("報p140", "積む決まりのない装備", "even though it was not required to be so equipped"),
              ("報p140", "近くの船", "the proximity of the emergency responders to the accident site")),
        # 第10章
        cb01=(("勧", "35本", "A-09-112 と A-10-062〜A-10-095"), ("勧", "報告書の34本＋先の1本", "A-10-062〜A-10-095 が34本・A-09-112 が1本"),
              ("勧", "26本", "あて先 FAA＝26本"), ("勧", "8本", "あて先 EASA＝8本"), ("勧", "1本", "あて先 USDA＝1本")),
        cb02=(("勧", "34本", "閉じた34"), ("勧", "1本", "開いている1＝A-10-087"), ("勧", "16本", "受け入れられない対応 16"),
              ("勧", "受け入れられる対応 10本", "受け入れられる対応 10"), ("勧", "別の対応 7本", "受け入れられる別の対応 7"),
              ("勧", "考え直して閉じた 1本", "NTSB が考え直して閉じた 1＝A-10-070")),
        cb03=(("勧", "受け入れられない対応", "CAROL の状態の欄＝受け入れられない対応で閉じた"), ("勧", "記録を閉じる", "CAROL の状態の欄＝閉じた")),
        cb05=(("勧", "2012年", "A-10-068 受け入れられない対応 2012-07-18"), ("勧", "受け入れられない対応", "A-10-068 受け入れられない対応"),
              ("報p142", "手順書の作り方の指針", "Develop and validate comprehensive guidelines for emergency and abnormal checklist design and development")),
        cb07=(("計", "2009年1月", "2009-01-15"), ("勧", "2025年12月", "A-10-072 受け入れられる対応 2025-12-02"),
              ("計", "17年近く", "2009-01-15 から 2025-12-02 まで＝16年10か月17日")),
        cb10=(("官", "1549便がきっかけ", "As a result of the Flight 1549 accident, the FAA began studying"),
              ("官", "鳥の吸い込みの研究", "how to improve engine durability related to core engine bird ingestion"),
              ("勧", "低い回転での鳥の試験", "A-10-064 … be conducted using the lowest expected fan speed"),
              ("勧", "2024年4月", "A-10-064 それに代わる対応 2024-04-03"), ("勧", "受け入れられる別の対応", "A-10-064 それに代わる対応")),
        cb14=(("勧", "8本", "A-10-088〜A-10-095＝あて先 EASA"), ("勧", "3本", "受け入れられる対応＝A-10-089・091・092"),
              ("勧", "1本", "受け入れられる別の対応＝A-10-088"), ("勧", "4本", "受け入れられない対応＝A-10-090・093・094・095")),
        cb15=(("勧", "低い所の手順書を使う", "A-10-067 … require … operators of turbine-powered aircraft to implement the checklist and procedure"),
              ("勧", "その手順の訓練", "A-10-069 … include a dual-engine failure scenario occurring at a low altitude in initial and recurrent ground and simulator training"),
              ("勧", "受け入れられない対応", "A-10-067・A-10-069 受け入れられない対応 2014-07-23"), ("勧", "2026年11月の時点", "CAROL の控え 2026-11-09")),
        # 第11章
        cc05=(("報p67", "判断の35秒を足すと", "after a 35-second delay"), ("ド#35p18", "届かなかった", "Hard landing just short of threshold"),
              ("報p137", "生き残れる見込みのいちばん高い道", "provided the highest probability that the accident would be survivable")),
        cc07=(("報p96", "よい見通しと静かな水面", "the ditching occurred in good visibility conditions on calm water"),
              ("報p96", "経験のある乗員", "was executed by a very experienced flight crew"),
              ("報p140", "積む決まりのない装備", "even though it was not required to be so equipped"),
              ("報p140", "近くの船", "the proximity of the emergency responders to the accident site")),
        cc09=(("計", "助かった理由", "結び"), ("計", "足りなかった所", "結び")),
    ),
)


# ══════════════════════════════════════════════════════════
#  門番 check_fuda から（git の `139227a3` の check_fuda.py の代入文をそのまま写した）＝札の枚数の例外（32本目も空）
# ══════════════════════════════════════════════════════════
EXC = {}


GATES = {
    "check_mech": dict(REC_M32=REC_M32),
    "check_sat": dict(REC_SAT_NUM=REC_SAT_NUM, REC_SAT_PAGES=REC_SAT_PAGES),
    "check_fuda": dict(EXC=EXC),
}

_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・（gate を渡せば）その門番の記録の表を32本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss は触らない）＝14〜31本目・17本目の見本と重ねるとき。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が32本目の表で
       33本目の画を測る）。apply の前に**無かった名**も覚えて、restore で**消す**＝selftest のあとに32本目の名が本番へ残らない
       （fixture_ep15〜ep31・ep17 と同じ作り）。⚠️ `titan_fig.GEO` は触らない（32本目の地点は無い）"""
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


CUTS_SHA = "139227a3"      # 32本目の章ファイルが最後に live だった版（章ファイルを33本目の器に替える前＝git の `139227a3`＝33本目 ⑤b-1 の移し替えの merge）
_CUTS32 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def _footage32():
    """32本目の映像の台帳 `CLIPS`（`ref/ep32/clips.json`）と使う区間 `USE`・器の黒帯の割合 `PILLAR`（git の CUTS_SHA の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}`）を返す。
    🔴 32本目の章ファイルは `ss.vid` で `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を引く（32本目は沿岸警備隊の監視カメラ VTS の13カット〈VC 11・V15 1・V20 1〉＝台帳 `ref/ep32/clips.json`）。
    本番の footage は33本目の表になった＝そのままだと32本目の映像のカットの区間と台帳が無い（USE・CLIPS は33本目の表）＝
    章ファイルが正しく読めない。→ 章ファイルを読む間だけ、この表を footage に差す（`cuts_ep32` が戻す）。
    footage.py の `USE`・`PILLAR` は値だけの代入＝その2文だけを取り出して評価する（footage.py 全体は import しない）。
    ⚠️ 32本目の PILLAR は空（VTS は黒帯なし＝32本目の ⑤b で書かなかった）＝空でも止めない形は残す。USE（13カット＝VTS）と台帳が読めなければ止める"""
    import ast
    import json
    import subprocess
    p = subprocess.run(["git", "-C", str(ROOT), "show", f"{CUTS_SHA}:tools/footage.py"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 32本目の映像の使う区間を git の {CUTS_SHA} の tools/footage.py から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    ns = {}
    for node in ast.parse(p.stdout.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("USE", "PILLAR") for t in node.targets):
            exec(compile(ast.Module([node], []), f"footage_{CUTS_SHA}", "exec"), ns)
    use, pillar = ns.get("USE"), ns.get("PILLAR")
    clips_file = REF / "clips.json"
    if not use or pillar is None or not clips_file.exists():
        raise RuntimeError(f"🔴 32本目の映像の表が読めていない（USE {len(use or {})}・PILLAR {'無い' if pillar is None else len(pillar)}・"
                           f"{clips_file} {'ある' if clips_file.exists() else '無い'}）")
    return json.loads(clips_file.read_text(encoding="utf-8")), use, pillar


def cuts_ep32():
    """32本目の章ファイル（git の CUTS_SHA の `tools/cuts/`＝32本目の ss.py ごと）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。
    読む間だけ `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を32本目の表にする（`_footage32`＝本番の footage は33本目の表）。読み終えたら戻す。"""
    if _CUTS32:
        return _CUTS32[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    import footage as _FO
    clips24, use24, pillar24 = _footage32()
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 32本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts32_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep32 の写真・頁を読む＝根の下の作業場所の
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
    # 🔴 32本目は 236カット＋ed01＝SPEC 237（git の 139227a3）。章ファイルが1本でも読めない（BROKEN）と SPEC が欠ける＝黙って一部で検算しない
    if broken or len(got[0]) != 236 or len(got[1]) != 237 or "c101" not in got[1]:
        raise RuntimeError(f"🔴 32本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}・読めない章 {sorted(broken)[:6]}）")
    _CUTS32.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を32本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で33本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep32()
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
        if s.get("cuts") is not None:          # apply_cuts() の分＝33本目の PLAN・SPEC へ戻す
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
