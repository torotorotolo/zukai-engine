# -*- coding: utf-8 -*-
"""22本目（タイタン号のリメイク・2023-06-18・米沿岸警備隊の報告書〈USCG〉・米国運輸安全委員会の報告書〈NTSB〉・カナダ運輸安全委員会の報告書〈TSB〉の動画）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-18（23本目 三豊百貨店のリメイク ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `adbe2d5` と同じ）
  ・`cuts/ss.py` の22本目の値＝案C の出典の表（REC_DOCS＝USCG・NTSB・TSB の3資料。TSB は頁でなく**節**〈page="sec"〉）・原文の道（REC_PAGES）・
    軸の型（AX_MORN22・AX_END・AX_1047・AX_TWO・AX_PM22・AX_CLASS・AX_Y18・AX_Y19・AX_Y20・AX_J22・AX_2223・AX_OUT・AX_RTM・AX_23・AXI の項目）・
    棒（QG＝fee・pax・o2・sf・sf2・slope・tow・dep23／QB＝その19本）・人の形（PEOPLE_ORDER・PEOPLE_REC・PEOPLE_CUTS＝c303 の母船の41人）・
    地図（衛星写真の表 SAT＝6点・場所の表 GEO＝7点）・台紙の縁でない暗い帯の名簿（SLIDE_NOT_MOUNT＝3点）（22本目 ⑤b-2〜⑤b-6）。
    ILLU_* ほか22本目も空のままだった表（ILLU_SPLIT_TIMES・ILLU_CROWD_UNTIL・ILLU_ROLES …）・AXIS_DOCS・SLIDE_MOUNT（22本目は台紙の縁のある写真が0点＝空）も、
    22本目の状態として持つ（21本目の見本と同じ考え方）
  ・`GEO`（地図の場所7点）は **ss の名**（`cuts/ss.GEO`）＝`SS_NAMES` に入れた。fixture_ep14〜ep21 の GEO は `titan_fig.GEO` だった（22本目から地図の型 `satmap.py` が
    ss の表を読む）。**`titan_fig.GEO` の22本目の地点は無い**（git の `e7564b8`〈22本目 ⑤b-1 の終わり〉と `adbe2d5` の `tools/titan_fig.py` の差分は模式図 `m22` の関数だけ＝GEO の
    差分は0）＝この見本は titan_fig.GEO を触らない（apply/restore の対象外）
  ・門番の記録の表（check_axis＝REC_AXIS・LANES_OK・REC_APPROX・REC_LANE・REC_ROLE・LANE_ROLE・TIER_ALERT／check_qty＝REC_QTY・REC_QTY_ROLE・REC_PEOPLE・REC_PEOPLE_PAGES・
    REC_PEOPLE_ROLE・PEOPLE_CUTS／check_mech＝REC_M22〈と、その中の `appb` の元表 `_TW_ROWS`〉）。REC_WRONG（×の印を置いてよい値）・ORDER_REF_MIN は22本目も使わなかった＝
    空（{}／None）の状態として持つ。check_boxes（REC_*）・check_illu は22本目で足した値が無い（git の `e7564b8`〜`adbe2d5` で両ファイルの差分は0）＝この見本の GATES に載せない
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を22本目の実物でも確かめている＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は23本目の空の器にした
  （fixture_ep14・fixture_ep15・fixture_ep16・fixture_ep18・fixture_ep19・fixture_ep20・fixture_ep21 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep22
      fixture_ep22.apply(sys.modules[__name__])   # その処理の中だけ ss・この門番の記録の表が22本目になる
      try: …（検算）
      finally: fixture_ep22.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14・15・16・18・19・20・21本目の見本と重ねるとき（check_mech は14本目の検算と15・16・18・19・20・21・22本目の検算を1つの処理で回す）は
      fixture_ep22.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと23本目以降の画に22本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。
■ 注意:
  ⚠️ 見本の頁の原文 `ref/ep22/src/ep22_pages.txt` と衛星写真 `ref/ep22/photo/gmap_g0*.png`（SAT の6点）は git の外（本線の作業ツリーにだけある）。
     原文が無いときは頁の照合を飛ばす（check_illu の `_pages()` が None を返す）。衛星写真が無いときは check_sat の md5 の陽性対照を飛ばす（Actions）。
  ⚠️ 22本目の selftest のうち、**章ファイルの SPEC を読むのは check_sat の selftest だけ**（地図のカット9つ＝c204 c219 c304 c514 c515 c812 c813 cb01 cb09）。
     `check_axis.selftest_ep22`・`check_mech._selftest_m22` は場面・図を selftest の中で `ss.ax`／`mech22.m22` で組む＝`apply()` だけで通る。
     check_photo_edge の `_selftest_none` は `apply()` ＋ REF・EP の差し替え（束 `ref/ep22/assets.json` を読む）だけ。それでも `apply_cuts()`
     （22本目の章ファイルを git の `CUTS_SHA`＝`adbe2d5` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ22本目に入れ替える・git が無い所では止める＝
     fail closed）を用意した＝check_sat の selftest が22本目の地図のカットを使う（`restore()` で23本目へ戻る・LIFO）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep22/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は22本目の道を持つ。
  ⚠️ `SAT`・`SLIDE_NOT_MOUNT` の鍵・値は **`ep22/` の名を文字で書いた**（本番の ss は `f"{EP}…"`／`P(…)` で組む＝EP が ep23 になると `ep23/…`〈無い名〉に化ける。
     fixture_ep21 の SLIDE_MOUNT と同じ扱い）。説明の文は1字も変えていない。`SAT_CREDIT`（Google の帰属の決まり文句）は本番の ss に**残した**型の定数
     〈回をまたいで同じ〉＝この見本は同じ文を文字で持つ（`SAT` の credit が使う名・SS_NAMES には入れない）。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝22本目は 0.99）は見本に入れない（16・18・19・20・21本目の見本も入れていない）＝本番の ss は
     今の値のまま残し、23本目の束で取り直す。
  ⚠️ 写真の束の定数（`TRIM`・`NEEDS_MASK`・`PRIVATE_OUT`・`OCR_NOT_TEXT`）は22本目も空のまま＝見本に入れない。
  ⚠️ `check_mech._M22_NEED`（模式図 m22 の「先に起きることが先」の筋の表）・`NUM_M22`（札の数と時刻を拾う正規表現）は**見本に入れず本番の check_mech に残した**
     （理由は check_mech の `REC_M22` の注＝`_M21_NEED` と同じ判断：見え方〈view〉と欄の名の約束で、記録の値〈時刻・数・座標・頁〉を持たない型の側の規則）。
  ⚠️ `check_axis` の役の色の判定（`_role_check`・`_hex`）・目盛りの「1日」の検査・秒の小数の読み方は型＝本番の check_axis に残した（表 REC_ROLE・LANE_ROLE・TIER_ALERT だけ見本）。
     `check_qty` の役の色の判定（`judge_bar`・`judge_people` の中）も型。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep22"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 22本目 ⑤b-3b
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：次の回は下の表を**その回の資料と時刻**に替える（頁の番号の書き方・資料の名の決め方は REC_DOCS の注）。
#   REC_PAGES … 部品の出典（`rec=`）を当てる原文（`=== p<N> ===` で頁を割った1ファイル＝`ref/ep22/make_pages22.py` の出力）
#   REC_DOCS  … 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面に出す名前・頁の出し方（pdf＝PDF の頁／sec＝節）
#   ILLU_* … 22本目は人・秒の札・時計の札・描いてよい数・想定の札・壊れる物・縮尺を持たない上から見た絵・潜水艦・音の輪・混ざりのつなぎ待ちを使わなかった＝
#            空のまま（下の値）。割れる時刻（ILLU_SPLIT_TIMES）も22本目は使わなかった（空）
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
#    入れた→ `tools/fixture_ep21.py` へ移して空にした。22本目も割れる時刻の札を使わなかった＝空のまま
AXIS_DOCS = {}


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：軸の型（`tools/axis.py`・門番 `check_axis`）── 22本目 ⑤b-3b〜⑤b-6（時間の帯・年表・2段の帯）
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の AX_*・AXI の項目は22本目の値（23本目の ⑤b-1 で見本 fixture_ep22 へ）。
#   値と頁は3つの報告書の原文（`ref/ep22/src/ep22_pages.txt`）で当てた＝門番の側の表（check_axis.REC_AXIS）と照らされる（§5b-88）。
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
#     🔧 ⑤c'（10-15）：目盛りが「1日／1月」と日まで出て年が無かった（⑤c の 640px）＝AX_Y20 と同じく月で書く（「1月／2018年」）
AX_Y18 = dict(view="date", span=("2017-12-10", "2019-01-10"), ticks=("2018-01", "2018-04", "2018-07", "2018-10", "2019-01"))
#   AX_Y19＝2019年（c817・c818）。USCG p164「On July 26, 2019, OceanGate fired the Director of Engineering」・TSB §1.12.1「On 15 October, the Titan was tested in the
#     Deep Ocean Test Facility」「Following that test, further cracks and delamination were found」「On 18 November, the Titan’s depth rating was reduced … not to dive
#     below 2000 m」「This carbon fibre cylinder was not subsequently used for any more dives」。札は語りの細かさ（年月＝fmt="ym"）
#     🔧 ⑤c'（10-15）：AX_Y18 と同じ（「1日／6月」→ 月で書く）
AX_Y19 = dict(view="date", span=("2019-05-20", "2019-12-31"), ticks=("2019-06", "2019-07", "2019-08", "2019-09", "2019-10", "2019-11", "2019-12"))
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
# 🆕 2026-10-15（22本目 ⑤b-6）：第10章の帯（門番 check_axis の REC_AXIS・REC_ROLE が値・頁・役の色を照らす）
#   AX_OUT＝屋外に置かれた期間（cb03）。USCG p236「On July 26, 2022, the TITAN, the LARS, and associated equipment were demobilized at the A Harvey Marine Base」
#     「placed in the parking lot of the facility for approximately 7 months of storage」・p238「unprotected from the elements until February 6, 2023」・
#     TSB §1.22「stored outdoors from the end of July 2022 until 06 February 2023」（括弧の札は語りの「半年あまり」＝数字は書かない）
AX_OUT = dict(view="date", span=("2022-07-01", "2023-03-15"), ticks=("2022-08", "2022-10", "2022-12", "2023-02"))
#   AX_RTM＝監視装置の記録が残っている期間（cb16）。TSB §1.10.9「This data spanned from February 2021 to 23 July 2022. There was no data available for the 2023
#     season」・USCG p139「No real-time monitoring data was available to the MBI from Expedition 2023 (Dives 84-88)」・NTSB p1051「no data were available for the
#     2023 expedition」。🔧 映像方針の「2022年＝記録あり」→ 原文の期間（2021年2月〜2022年7月23日）。2023年の段＝付録B の人が乗った潜航（5月31日〜6月18日）
AX_RTM = dict(view="date", span=("2020-12-01", "2023-08-31"), ticks=("2021-01", "2021-07", "2022-01", "2022-07", "2023-01", "2023-07"))
#   AX_23＝2023年6月（cb19）。TSB 付録B（2023-05-31・06-05・06-13＝深さ10・06-18＝3346）・USCG p256「10 m dives were dives which did not leave the LARS platform」・
#     USCG p295「Dive 88 was the first dive to leave the LARS platform」・NTSB p1016「the first dive of the 2023 expedition to descend below 33 feet (10 meters)」
AX_23 = dict(view="date", span=("2023-05-26", "2023-06-24"), ticks=("2023-05-28", "2023-06-02", "2023-06-07", "2023-06-12", "2023-06-17", "2023-06-22"))
AXI.update({
    # 屋外（AX_OUT）＝置いたのは会社の決め（TSB §1.22「OceanGate opted to keep the Titan and the LARS in St. John’s」）
    "out22": dict(k="span", a="2022-07-26", b="2023-02-06", t="屋外に置かれた", rec=["USCG p236", "USCG p238"], c="COMPANY"),
    "half": dict(k="br", a="2022-07-26", b="2023-02-06", t="半年あまり", rec=["USCG p236", "USCG p238"]),
    # 監視の記録（AX_RTM）＝装置は会社の物・記録が無い＝灰
    "rtm_on": dict(k="span", a="2021-02", b="2022-07-23", t="記録がある", rec="TSB §1.10.9", c="COMPANY"),
    "rtm_off": dict(k="span", a="2023-05-31", b="2023-06-18", t="記録なし", rec=["TSB §1.10.9", "TSB §付録B"], c="TICK"),
    # 2023年6月（AX_23）＝台を離れない10メートルの潜航（潜水艇）・事故の潜航（赤）
    "s0531": dict(k="pt", at="2023-05-31", t="", lab=False, rec="TSB §付録B", c="SUB"),
    "s0605": dict(k="pt", at="2023-06-05", t="", lab=False, rec="TSB §付録B", c="SUB"),
    "s0613": dict(k="pt", at="2023-06-13", t="", lab=False, rec="TSB §付録B", c="SUB"),
    # 🔧 ⑤c'（10-15）：札が真ん中の点だけ＝両端の点の意味が伝わらない（⑤b-6 §5-3）＝数を添えて3つの点を1つの札で受ける（付録B の3行）
    "s10m": dict(k="chips", at="2023-06-05", chips=["台の上の潜航3回"], rec=["TSB §付録B", "USCG p256"]),
    "first88": dict(k="chips", at="2023-06-18", chips=["初めて台を離れる"], rec=["TSB §付録B", "USCG p295", "NTSB p1016"]),
})


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：量の型（棒・人の形）── 22本目 ⑤b-3b〜⑤b-6
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB・PEOPLE_* はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_QTY・REC_PEOPLE＝§5b-88）＝回を替えたら両方を替える。
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
    # ⚠️ 門番 qty ⑪：同じ群の棒は色を ΔE 25 以上離す（4本とも会社の橙だと鳴った）
    #    （第6章は白黒＝灰 TICK が #aca69a に置き換わる＝書類の色 DOC とは ΔE 21 で鳴った・白 INK_W とは 27）
    #    🔧 ⑤c'（10-15）：前は チタン 橙・炭素繊維 黄・目標 白＝会社の目標が潜水艇の白・設計書の値が会社の橙に読めた（役の色の逆）→
    #       設計書の2つの値（潜水艇の筒の計算）＝白と黄（黄＝数）・会社の目標＝会社の橙・規格の最低＝灰
    "sf_ti": dict(k="bar", g="sf", t="チタンのドームのとき", v=2.19, rec="TSB §1.12.1", c="SUB"),
    "sf_cf": dict(k="bar", g="sf", t="炭素繊維のドームのとき", v=2.21, rec="TSB §1.12.1", c="AMBER"),
    "sf_goal": dict(k="bar", g="sf", t="会社の目標", v=2.25, rec="TSB §1.12.1", c="COMPANY"),
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


# 🆕 2026-10-15（22本目 ⑤b-6）：cb10 母船の綱につながれていた時間（TSB §1.20.2.2「towed by or tethered to, via a towline, the Polar Prince in the North Atlantic for
#   approximately 950 hours in the 2023 season」）。行の名は年だけ・色＝母船（引いたのは母船）。
#   ⚠️ 道のり（USCG p294「more than 2,900 NM」）は描かない＝NTSB p1060 は「about 2,900 miles」と単位が違う・語りに無い
QG.update({"tow": dict(id="tow", t="綱でつながれていた時間（時間）", ticks=(0, 250, 500, 750, 1000), rows=("2023年",))})
QB.update({"tow23": dict(k="bar", g="tow", t="2023年", v=950, rec="TSB §1.20.2.2", c="SHIP")})
# 🆕 22本目 ⑤b-6：cb14 2023年の人が乗った潜航の深さ（TSB §1.21.4「aborted at a depth of 10 m」・NTSB p1014「None of the dives exceeded 33 feet (10 meters) depth」・
#   付録B の 2023年の3行＝10）とタイタニックの深さ（TSB §1.3「approximately 3800 m」＝目安の灰）。🔧 映像方針の「10m の短い棒3本」→ 1本（同じ群の棒は色を
#   ΔE 25 以上離す＝同じ値の3本を3色にすると別の物に見える）＝3回とも同じ深さは note で断る。行の名に数字を書かない
QG.update({"dep23": dict(id="dep23", t="潜った深さ（メートル）", ticks=(0, 1000, 2000, 3000, 4000), rows=("事故の年の潜航", "タイタニック"))})
QB.update({
    "dep23_sub": dict(k="bar", g="dep23", t="事故の年の潜航", v=10, rec=["TSB §1.21.4", "NTSB p1014", "TSB §付録B"], c="SUB"),
    "dep23_tt": dict(k="bar", g="dep23", t="タイタニック", v=3800, rec="TSB §1.3", c="TICK"),
})

# 人の形（1つ＝1人）＝**14本目 c204〜c206 だけの例外**（ルール §C-1 #59・亡くなった方の数には使わない）。
# 🆕 2026-10-14（22本目 ⑤b-3b）：c303 だけ（映像方針 了承②「会社の関係24＝橙・乗組員17＝水色の人の印」）＝母船に乗っていた41人（TSB §1.3.1「There were 41 people
#   on board the Polar Prince in total: 24 people associated with OceanGate and 17 Polar Prince crew members」）。🔴 亡くなった方を分けない・後の章で戻して灰色にしない
PEOPLE_ORDER = (("乗客に数える人（会社の関係）", 24), ("母船の乗組員", 17))
PEOPLE_REC = {"乗客に数える人（会社の関係）": ["TSB §1.3.1", "TSB §1.20.1.1"], "母船の乗組員": "TSB §1.3.1"}
PEOPLE_CUTS = ("c303",)     # 🔴 門番 check_qty がこの外の人の形を止める（亡くなった方の数に使わない）


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：地図の型「衛星写真＋描き足し」（`tools/satmap.py`・門番 `tools/check_sat.py`）── 22本目 ⑤b-3
# ══════════════════════════════════════════════════════
#   SAT＝撮った衛星写真（`ref/ep22/eizou_build/helpers/gshot22.py`・中心 ll とズーム z は sources22.tsv の media と同じ）。
#     🔴 写真そのものは公開リポに置かない（git の外・Modal の保管庫 `jiko-assets` の `ref/ep22/photo/`＝`modal_app.pull_private`）。
#        ここに置けるのは md5 だけ＝門番が手元の絵と照らす（撮り直したら md5 と描き足しの座標を見直す）。
#     🔴 Actions は保管庫を読めない＝地図のカットは理由を出して飛ばす（`build_jiko.drop_missing_sat`）・検品画像は Modal の `qa`。
#     G06 は ⑤b-3 で撮り直した（⑤b-1 の中心 47.563,-52.705・ズーム16 は A. Harvey の基地が画の上の端の外＝2回撮って `gseam22.py`
#     ＝1回目に y 973 の継ぎ目〈A 25.5／B 0.0〉→ 2回目を採った）
#   GEO＝描き足しに使う場所。src＝報告書でその場所の名が出る所・how＝座標の出どころ（「報告書の値」か「一般の座標」）。
#     🔴 確かめていない場所に点を置かない（門番）。×は報告書の座標の場所だけ・一般の座標を使ったカットは断りに「一般の座標」
#   ⚠️ `SAT` の file は本番では `f"{EP}photo/…"`＝この見本は `ep22/` の名を文字で書いた（EP が ep23 になっても22本目の絵を指す）。
#      credit の `SAT_CREDIT`＝Google の帰属の決まり文句は本番の ss にも残してある型の定数（同じ文）
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"
SAT = {
    "G01": dict(file="ep22/photo/gmap_g01_north_america.png", ll=(45.0, -87.0), z=4, md5="70ff2619fdbaf91c3b1c5651b82d7c8e", credit=SAT_CREDIT),
    "G02": dict(file="ep22/photo/gmap_g02_newfoundland_site.png", ll=(44.6, -51.3), z=6, md5="4c9a76312ec1bb0053611ec20add3068", credit=SAT_CREDIT),
    "G03": dict(file="ep22/photo/gmap_g03_buffalo_newfoundland.png", ll=(45.5, -65.8), z=5, md5="57eb70a4722acc83aa5653315a0171ec", credit=SAT_CREDIT),
    "G04": dict(file="ep22/photo/gmap_g04_north_atlantic.png", ll=(45.0, -47.0), z=5, md5="67507f0134ae97af6abac1dcafc49299", credit=SAT_CREDIT),
    "G05": dict(file="ep22/photo/gmap_g05_bahamas.png", ll=(25.0, -77.0), z=7, md5="35b8c66417c27d9d68155c244a7d0337", credit=SAT_CREDIT),
    "G06": dict(file="ep22/photo/gmap_g06_stjohns_pier14.png", ll=(47.5675, -52.7010), z=17, md5="2ac970d434b7b1a7c735a8f334926ab7", credit=SAT_CREDIT),
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


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：スライドの台紙の黒い縁がある写真の名簿 ── 22本目 ⑤b-2
# ══════════════════════════════════════════════════════
# 🆕 2026-10-14（22本目 ⑤b-2）：22本目の束は DVIDS のデジタル写真・報告書の図・Commons＝スライドの走査が無い＝**SLIDE_MOUNT は空**（台紙の縁のある写真は0点）。
#    門番 `tools/check_photo_edge.py` は SLIDE_MOUNT が空のとき、束の全点を測って「暗い帯のある点が SLIDE_NOT_MOUNT に全部載っているか」を見る（載っていない点が出たら止める）。
SLIDE_MOUNT = {}
# 🆕 2026-10-14（22本目 ⑤b-2）：**四辺に暗い帯があっても、台紙の縁ではない写真**（名 → 何か）＝数と絵で決めた（`python qa_out/ep22_assets.py edges`＝
#    門番の物差し `check_photo_edge.margins` で束の全43点を測り、MIN_EDGE〈1.2%〉以上の3点を帯の明るさの分け方で見た）。
#    本番の ss は `P("…")` で組んでいた＝EP が ep23 になると鍵が `ep23/…`（無い名）に化ける＝見本は **`ep22/` の名を文字で書いた**（値＝git の `adbe2d5` の
#    ss.SLIDE_NOT_MOUNT を評価した結果と同じ3点・説明の文は1字も変えていない）。check_photo_edge の selftest（`_selftest_none`）が `apply()` で使う
SLIDE_NOT_MOUNT = {
    "ep22/commons_titanic_wreck_bow.jpg": "右 5% は深い海の暗い水（帯の中央値 20・95 パーセンタイル 28〜30・ばらつき 4〜5＝なだらか）＝写真の中身・額装（共同）",
    "ep22/commons_uscg_mbi_8668382.jpg": "下 3.5% は委員の濃い色の服と床（いちばん下の行の 95 パーセンタイル 137・ばらつき 50〜65）＝写真の中身",
    "ep22/ntsb_fig16_wrinkle_t.jpg": "上・右・下 5% は研究所の写真の黒い背景（明るさ 7・左から暗くなって続く）＝写真の中身（束でも切らない＝`qa_out/ep22_assets.py` の _trim_white の注）",
}


# `apply()` が cuts.ss に差し込む名の全部（上の値＝ss から移したもの）。ここに無い名は ss に置かない
#   （`AXI`・`QG`・`QB`・`REC_DOCS`・`AXIS_DOCS`・`PEOPLE_*`・`SAT`・`GEO`・`SLIDE_*`・`ILLU_*` などは ss に空の器が残る＝見本の値〈22本目の項目つき〉を差し込む。
#   `AX_MORN22` ほかの `AX_*` は本番の ss に無い名＝restore で消す）。22本目は関数を ss へ足した（`sat()`＝地図のカットの SPEC の頭）が、それは型の道具＝本番に残した。
#   `check_frame_only(spec, use)`・`check_card_mix` の拡張〈地図のカット〉・`mv`・`MV_Z`・`MV_IN`・`src`・`SAT_CREDIT` も型。
#   `_TU`・`_TC`（2段の帯の段の名の略）・`SAT_CREDIT` は上の AXI・SAT を組むための名＝ss には差し込まない
SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "AX_MORN22", "AX_END", "AX_1047", "AX_TWO",
            "AX_PM22", "AX_CLASS", "AX_Y18", "AX_Y19", "AX_Y20", "AX_J22", "AX_2223", "AX_OUT", "AX_RTM", "AX_23", "QG", "QB",
            "PEOPLE_ORDER", "PEOPLE_REC", "PEOPLE_CUTS", "SAT", "GEO", "SLIDE_MOUNT", "SLIDE_NOT_MOUNT")


# ══════════════════════════════════════════════════════════
#  titan_fig.GEO から：22本目の地点＝無い
# ══════════════════════════════════════════════════════════
#   22本目は `titan_fig.GEO` に地点を足さなかった（地図は衛星写真の型 `satmap.py`＝場所の表は ss の `GEO`〈上〉）。
#   `adbe2d5` の `titan_fig.GEO` は `e7564b8`（22本目 ⑤b-1 の終わり）と同じ（差分は模式図 `m22` の関数だけ）＝この見本は titan_fig を import しない・触らない


# ══════════════════════════════════════════════════════════
#  門番の記録の表（22本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════════
# 以下の表は、門番3本の本番の置き場にあった22本目の値を1文字も変えずに写したもの（GATES が門番ごとにまとめる）

# ── check_axis ──
# ✅ 2026-10-14（22本目 ⑤b-3b）：22本目の値を入れた。原文＝ref/ep22/src/ep22_pages.txt（頁の番号は cuts/ss.REC_DOCS の通し番号＝USCG p35＝PDF 35頁・
#    NTSB p1017＝PDF 17頁・TSB §1.3.1＝節）。時刻はニューファンドランドの夏時間（TSB 脚注13）。
#    TSB §1.3.1「arrived … at 0400 on 18 June」「At 0534 … briefing」「At 0545 … weighed」「From 0600 to 0800 … RIBs」「by 0820」「At 0824 … closed the Titan’s forward dome」
#      「At 0859 … a scheduled 5-minute pause」「At 0904 … fill the LARS’s ballast tanks」
#    TSB 付録A「10:41:07.2 SST ack no niskin」「10:42:01.4 T a」「10:47:26.9 T dropped two wts」／NTSB p.17「At 1048 … acknowledge」「At 1049 … “lost tracking”」
#    USCG p35「At approximately 10:47:02 a.m.」「At approximately 10:47:08 a.m. … final ping」「At approximately 10:47:09 a.m. … catastrophic implosion」
#      「At 10:47:11 a.m. … “bang”」「At 10:47:26 a.m. … received a message」（p36「This was the last message」）・p37「At 10:47:32 a.m., the POLAR PRINCE received the ping」
#    TSB §1.3.2「At 1047:26.903 … a message appeared」「At 1047:32.066 … the last automated position update」「the sound was generated at 1047:32.3」
#      「At 1047:34.522, a loud sound … reverberated through the hull」・§2.1「5.397 seconds after the text message … appeared」
#    ⚠️ 秒の小数は画面に1桁（32.066→「10:47:32.1」・34.522→「10:47:34.5」）＝門番の幅（書いた桁の半分 ±0.05秒）に原文の値が入る
REC_AXIS = {
    "4:00": {"TSB §1.3.1"}, "5:34": {"TSB §1.3.1"}, "5:45": {"TSB §1.3.1"}, "6:00": {"TSB §1.3.1"}, "8:00": {"TSB §1.3.1"},
    "8:20": {"TSB §1.3.1"}, "8:24": {"TSB §1.3.1"}, "8:59": {"TSB §1.3.1"}, "9:04": {"TSB §1.3.1"},
    "10:41:07": {"TSB §付録A"}, "10:42:01": {"TSB §付録A"}, "10:47:26.9": {"TSB §付録A", "TSB §1.3.2", "TSB §2.1"},
    "10:48": {"NTSB p1017"}, "10:49": {"NTSB p1017"},
    "10:47:02": {"USCG p35"}, "10:47:08": {"USCG p35"}, "10:47:09": {"USCG p35"}, "10:47:11": {"USCG p35"},
    "10:47:26": {"USCG p35", "USCG p36"}, "10:47:32": {"USCG p37"},
    "10:47:32.1": {"TSB §1.3.2"}, "10:47:32.3": {"TSB §1.3.2", "TSB §2.1"}, "10:47:34.5": {"TSB §1.3.2"},
    # 🆕 2026-10-15（22本目 ⑤b-4）：USCG p38「as of approximately 10:47 a.m., there was a loss of communication」・TSB §1.3.3「(at 1500)」「At 1500 … commenced the
    #   3-hour surface search」「At 1634, … called the Horizon Maritime Services Ltd. shore-based emergency team」「By 1800, the surface search had found no signs」
    #   「At 1855, the master … called the Joint Rescue and Coordination Centre」・USCG p39「At (6:27 p.m.) … cut-off」・TSB §2.5「8 hours and 8 minutes」
    "10:47": {"USCG p38", "TSB §2.5"}, "15:00": {"TSB §1.3.3"}, "16:34": {"TSB §1.3.3"}, "18:00": {"TSB §1.3.3"}, "18:27": {"USCG p39"},
    "18:55": {"TSB §1.3.3", "TSB §2.5"},
    #   NTSB p1022「when he was hired in 2016, the company planned to class」・p1023「In 2018, OceanGate abandoned classing efforts」
    "2016": {"NTSB p1022"}, "2018": {"NTSB p1023"},
    #   USCG p149「On January 23, 2018, OceanGate fired」「on February 6, 2018」・p150「on June 25, 2018」・p151「On December 13, 2018」・TSB §1.12.1・NTSB p1048
    "2018-01-23": {"USCG p149", "TSB §1.12.1"}, "2018-02-06": {"USCG p149", "NTSB p1048"}, "2018-06-25": {"USCG p150"}, "2018-12-13": {"USCG p151"},
    #   USCG p164「On July 26, 2019, OceanGate fired the Director of Engineering」・TSB §1.12.1「On 15 October」「On 18 November」
    "2019-07-26": {"USCG p164"}, "2019-10-15": {"TSB §1.12.1"}, "2019-11-18": {"TSB §1.12.1"},
    # 🆕 2026-10-15（22本目 ⑤b-5）：NTSB p1028「between November 2020 and January 2021」・p1062「did not build or test any new sub-scale models」
    "2020-11": {"NTSB p1028"}, "2021-01": {"NTSB p1028", "NTSB p1062"},
    #   NTSB p1036「On July 15, 2022 (mission 3, dive 80)」「2,954 meters (9,692 feet) on the final dive」・USCG p235「On July 19, 2022 … commenced Dive 81」・
    #   TSB 付録B（2022-07-22・2023-06-18 の行）・NTSB p1051「(dive 83) took place on July 23, 2022」・USCG p290「a red flag」・NTSB p1060「11 months later」
    "2022-07-15": {"NTSB p1036", "USCG p290"}, "2022-07-19": {"USCG p235"}, "2022-07-22": {"TSB §付録B", "NTSB p1060"},
    "2022-07-23": {"NTSB p1051", "NTSB p1036", "TSB §1.10.9"}, "2023-06-18": {"TSB §付録B", "NTSB p1060"},
    # 🆕 2026-10-15（22本目 ⑤b-6）：USCG p236「On July 26, 2022, … were demobilized at the A Harvey Marine Base」・p238「until February 6, 2023」・
    #   TSB §1.10.9「This data spanned from February 2021 to 23 July 2022」・TSB 付録B（2023-05-31・2023-06-05・2023-06-13＝10）
    "2022-07-26": {"USCG p236"}, "2023-02-06": {"USCG p238"}, "2021-02": {"TSB §1.10.9"},
    "2023-05-31": {"TSB §付録B"}, "2023-06-05": {"TSB §付録B"}, "2023-06-13": {"TSB §付録B"},
}
LANES_OK = {_TU, _TC}
REC_APPROX = {"10:47:02", "10:47:08", "10:47:09", "10:47"}      # 記録が about の時刻（「ごろ」が要る）＝USCG p35・p38 の approximately
REC_LANE = {"10:47:02": _TU, "10:47:08": _TU, "10:47:09": _TU, "10:47:11": _TU, "10:47:26": _TU, "10:47:32": _TU,
            "10:47:26.9": _TC, "10:47:32.1": _TC, "10:47:32.3": _TC, "10:47:34.5": _TC}   # 2段の帯の記録ごとの段（値 → 段の名）
REC_WRONG = {}            # 22本目は×の印を使わなかった＝空（21本目 ⑤b-6 で足した表＝fixture_ep21 の GATES が値を持つ）
# 🆕 2026-10-14（22本目 ⑤b-3b）：**役の色**（記憶 feedback-jiko-diagrams-more-color・`jiko_style.ROLE`）。型の側の色（AXI の c）と別に、門番の側で
#    「その値はだれの動きか」を持つ＝描いた部品の色の値が役の色の値と同じか照らす（[[feedback-settings-may-not-reach-the-picture]]＝設定でなく描いた値）。
#    REC_ROLE＝1段の帯（clock）の値 → 役（ROLE の名か意味の色の名）・帯 span は「始め〜終わり」の鍵。LANE_ROLE＝2段の帯の段 → 役（段の点は段の調べの色）・
#    TIER_ALERT＝2段の帯で赤（壊れた）にしてよい値。表に無い値は本番（main）で止める（selftest の前の回の見本は表を持たない＝照らさない）
REC_ROLE = {
    "4:00": "ship", "5:34": "company", "5:45": "company", "6:00〜8:00": "company", "8:20": "sub", "8:24": "sub", "8:59": "company",
    "10:41:07": "ship", "10:42:01": "sub", "10:42:01〜10:47:26.9": "LINE", "10:48": "ship", "10:49": "ship",
    "10:47:02": "sub", "10:47:08": "sub", "10:47:09": "ALERT", "10:47:11": "ship", "10:47:26": "ship",
    # 🆕 2026-10-15（22本目 ⑤b-4）：途絶＝だれの動きでもない（LINE）・浮上の見込み＝会社の手順・捜索と電話＝母船（船長）／会社の決め＝会社・元運航部長＝LINE
    "10:47": "LINE", "15:00": "company", "15:00〜18:00": "ship", "16:34": "ship", "18:00": "ship", "18:27": "ship", "18:55": "ship",
    "2016": "company", "2018": "company", "2018-01-23": "company", "2018-02-06": "LINE", "2018-06-25": "company", "2018-12-13": "LINE",
    "2019-07-26": "company", "2019-10-15": "company", "2019-11-18": "company",
    # 🆕 2026-10-15（22本目 ⑤b-5）：筒を作る＝会社（作り手に頼んだ）・80回目の音と事故の潜航＝赤・81〜83回目と最後の深い潜航＝潜水艇
    "2020-11〜2021-01": "company", "2021-01": "company", "2022-07-15": "ALERT", "2022-07-19": "sub", "2022-07-22": "sub", "2022-07-23": "sub", "2023-06-18": "ALERT",
    # 🆕 2026-10-15（22本目 ⑤b-6）：屋外に置いた＝会社の決め・記録がある期間＝会社の装置・記録なし＝灰・台の上の10メートルの潜航＝潜水艇
    "2022-07-26〜2023-02-06": "company", "2021-02〜2022-07-23": "company", "2023-05-31〜2023-06-18": "TICK",
    "2023-05-31": "sub", "2023-06-05": "sub", "2023-06-13": "sub",
}
LANE_ROLE = {_TU: "uscg", _TC: "tsb"}
TIER_ALERT = {"10:47:09", "10:47:32.3"}
# 並び order の基準の時刻（分）。🔴 22本目は時計の時刻を含む並び（"1:16:27" の形）を使わなかった＝空（None）。本番も None
ORDER_REF_MIN = None

# ── check_qty ──
# ✅ 2026-10-14（22本目 ⑤b-3b）：22本目の値を入れた（頁は cuts/ss.REC_DOCS の通し番号）。
#    c210 参加費＝USCG p64「rising from $105,129 in 2021 to $250,000 for both 2022 and 2023」（万ドル＝10.5129・25・25）・TSB §1.23「up to 250 000」
#    c302 乗客＝TSB §1.20.1.2「it was permitted to carry up to 12 passengers」「on the occurrence voyage, it was carrying 24 passengers」
#    c303 人の形＝TSB §1.3.1「There were 41 people on board the Polar Prince in total: 24 people associated with OceanGate and 17 Polar Prince crew members」
#      （乗客に数える＝§1.20.1.1「OceanGate passengers, who consisted of the Titan passengers and their family members」）
#    🆕 役の色（REC_QTY_ROLE・REC_PEOPLE_ROLE）＝描いた棒・凡例の色の値が役の色（jiko_style.ROLE）か（会社＝橙・母船＝水色）
REC_QTY = {          # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
    ("参加費（万ドル）", "2021年"): (10.5129, {"USCG p64"}),
    ("参加費（万ドル）", "2022年"): (25.0, {"USCG p64"}),
    ("参加費（万ドル）", "2023年"): (25.0, {"USCG p64", "TSB §1.23"}),
    ("乗客として乗る人（人）", "貨物船の決まりの上限"): (12.0, {"TSB §1.20.1.2"}),
    ("乗客として乗る人（人）", "この航海"): (24.0, {"TSB §1.20.1.2"}),
    # 🆕 2026-10-15（22本目 ⑤b-4）：c518＝TSB §1.2.1「approximately 96 hours based on an occupancy of 5 people」・§2.5「98 hours and 16 minutes after life support
    #   had been started」／c708＝TSB §1.12.1「a safety factor of 2.19 with grade 5 titanium end domes and a safety factor of 2.21 with carbon fibre end domes」
    #   「a goal of 2.25 for the safety factor」・脚注45「a minimum safety factor of 1.5」
    ("生命維持の開始からの時間", "酸素の目安"): (96.0, {"TSB §1.2.1", "TSB §2.5"}),
    ("生命維持の開始からの時間", "見つかるまで"): (98.0 + 16.0 / 60.0, {"TSB §2.5"}),
    ("安全率（倍）", "チタンのドームのとき"): (2.19, {"TSB §1.12.1"}),
    ("安全率（倍）", "炭素繊維のドームのとき"): (2.21, {"TSB §1.12.1"}),
    ("安全率（倍）", "会社の目標"): (2.25, {"TSB §1.12.1"}),
    ("安全率（倍）", "規格の最低"): (1.5, {"TSB §脚注45"}),
    # 🆕 2026-10-15（22本目 ⑤b-5）：c917＝TSB §1.12.2「changed its safety factor to 1.25」・§1.15「the calculated safety factor of 3.05」
    #   「the calculated safety factor was 1.11」／ca20＝TSB §1.10.10.1「on the 05 August 2021 dive … 21% greater」「on 19 July 2022 dive … 98% greater」
    ("安全率（倍）", "会社の基準"): (1.25, {"TSB §1.12.2", "TSB §1.15"}),
    ("安全率（倍）", "長さの向き"): (3.05, {"TSB §1.15"}),
    ("安全率（倍）", "周りの向き"): (1.11, {"TSB §1.15"}),
    ("浅い所の傾きの増え（%）", "前の年の夏の潜航"): (21.0, {"TSB §1.10.10.1"}),     # 2021年8月5日
    ("浅い所の傾きの増え（%）", "音のあとの潜航"): (98.0, {"TSB §1.10.10.1"}),       # 2022年7月19日（81回目）
    # 🆕 2026-10-15（22本目 ⑤b-6）：cb10＝TSB §1.20.2.2「for approximately 950 hours in the 2023 season」／cb14＝TSB §1.21.4「aborted at a depth of 10 m」・
    #   NTSB p1014「None of the dives exceeded 33 feet (10 meters) depth」・付録B（2023年の3行＝10）・TSB §1.3「approximately 3800 m」
    ("綱でつながれていた時間（時間）", "2023年"): (950.0, {"TSB §1.20.2.2"}),
    ("潜った深さ（メートル）", "事故の年の潜航"): (10.0, {"TSB §1.21.4", "NTSB p1014", "TSB §付録B"}),
    ("潜った深さ（メートル）", "タイタニック"): (3800.0, {"TSB §1.3"}),
}
REC_QTY_ROLE = {("参加費（万ドル）", "2021年"): "company", ("参加費（万ドル）", "2022年"): "company",
                ("参加費（万ドル）", "2023年"): "company", ("乗客として乗る人（人）", "この航海"): "company",
                ("生命維持の開始からの時間", "酸素の目安"): "sub", ("生命維持の開始からの時間", "見つかるまで"): "tsb",
                # 🔧 22本目 ⑤c'（10-15）：チタン＝会社の橙だと会社の目標（白）と役が逆に読めた＝設計書の値は潜水艇の筒の計算＝sub・目標＝company
                #    （炭素繊維は ⑪（ΔE 25）で黄＝数・規格の最低は灰＝役の色を持たない）
                ("安全率（倍）", "チタンのドームのとき"): "sub", ("安全率（倍）", "会社の目標"): "company",
                # 🆕 22本目 ⑤b-5：基準＝会社・長さの向き＝カナダの研究所の計算・2022年の傾き＝カナダの調べの値（周りの向き＝赤・2021年＝灰は役を持たない）
                ("安全率（倍）", "会社の基準"): "company", ("安全率（倍）", "長さの向き"): "tsb", ("浅い所の傾きの増え（%）", "音のあとの潜航"): "tsb",
                # 🆕 22本目 ⑤b-6：引いたのは母船・潜ったのは潜水艇（タイタニック＝目安の灰は役を持たない）
                ("綱でつながれていた時間（時間）", "2023年"): "ship", ("潜った深さ（メートル）", "事故の年の潜航"): "sub"}
REC_PEOPLE = {"乗っていた人": 41, "乗客に数える人（会社の関係）": 24, "母船の乗組員": 17}   # 人の形（§C-1 #59 の例外＝22本目は c303 だけ）
REC_PEOPLE_PAGES = {"TSB §1.3.1", "TSB §1.20.1.1"}
REC_PEOPLE_ROLE = {"乗客に数える人（会社の関係）": "company", "母船の乗組員": "ship"}
PEOPLE_CUTS_QTY = {"c303"}   # 🔴 ルール §C-1 #59（型の側の ss.PEOPLE_CUTS とは別に持つ）＝22本目は c303 だけ（母船に乗っていた41人の内わけ）
#                              ⚠️ check_qty の表の名は `PEOPLE_CUTS`（上の ss の `PEOPLE_CUTS`〈タプル〉と同じ名＝この見本の中で区別するため `_QTY` を付けた。GATES で戻す）

# ── check_mech ──
# 🆕 22本目 ⑤b-3b（2026-10-14）：模式図（m22＝`tools/mech22.py`・17の見え方）。⑤b-4〜⑤b-6 で見え方と記録の値を足した
# 🔴 記録の値は門番の側に別に持つ（§5b-88＝描く側の表 mech22.FUJI_M・RP_T・SD_BOLTS・ORG・PP_DOC・APPB・APPA・DEPTH・BW_DIR・TW_SEABED…を書き換えると鳴る）。
#    頁の番号は cuts/ss.REC_DOCS の通し番号（USCG p71＝PDF 71頁・NTSB p1010＝PDF 10頁・TSB §1.23＝節）。引いた原文：
#    NTSB p10「water pressure is 5,554.5 pounds per square inch」「The 22-foot-long submersible Titan」・TSB §1.3「approximately 3800 m」・
#    USCG p5「August 4, 2025」・NTSB p76「Report Date: October 2, 2025」・TSB §4.2.4「officially released on 17 June 2026」・TSB §1.2.1「up to 5 people」・
#    TSB 脚注39「OceanGate began using 18 securing bolts」・TSB §1.23 表4（CEO／Chief Operating Officer／Director of Engineering＝Vacant／Director of
#    Communications／Operations Manager／Director of Logistics and Quality Assurance／Expedition Manager／Director of Administration）・「15 employees」・
#    USCG p71「experimental submersible vessel」「not been certified by any regulatory body」「mentions death 9 times」・NTSB p15「guests who help fund
#    OceanGate expeditions」・TSB 付録B 表B1（27行）・付録A（文）・TSB §1.3.2「235 m」「680 m」・USCG p32「9:23:04 … 436 m」・p34「2,203 m … 2,289 m」
#    「Four minutes later … 3,149 m」・p35「approximately 10:47:02 … 3,341 m」「approximately 10:47:08 … 3,346.28 m」・TSB §1.3.2「approximately 500 m from the seabed」
#    ・付録A「east south east of the nbow」「east north east of the bow」。富士山 3,776m＝国土地理院・1円玉の直径 20mm＝造幣局（一般の値）
_TW_ROWS = (
    ("2021-06-30", "7", "2.6", "5", "Horizon Arctic", "Test", "Forward dome fell off the submersible during recovery"),
    ("2021-07-03", "1700", "5.8", "4", "Horizon Arctic", "Test", "Starboard thrusters failed"),
    ("2021-07-09", "3840", "16", "3", "Horizon Arctic", "Test", "Incident with drop weight"),
    ("2021-07-13", "89", "4.9", "5", "Horizon Arctic", "Test", ""),
    ("2021-07-19", "3500", "11.3", "5", "Horizon Arctic", "Titanic", "Incident with drop weight"),
    ("2021-07-24", "3840", "10.7", "5", "Horizon Arctic", "Titanic", "Incident with drop weight"),
    ("2021-07-27", "3840", "9.5", "5", "Horizon Arctic", "Titanic", "Titan too light, had to thrust to bottom and then starboard battery failed"),
    ("2021-07-28", "3840", "11.1", "5", "Horizon Arctic", "Titanic", ""),
    ("2021-08-04", "3840", "10.7", "5", "Horizon Arctic", "Titanic", ""),
    ("2021-08-05", "3840", "10.8", "5", "Horizon Arctic", "Titanic", ""),
    ("2022-06-16", "7", "3.5", "5", "Horizon Arctic", "Test", ""),
    ("2022-06-18", "1380", "6.3", "5", "Horizon Arctic", "Titanic", ""),
    ("2022-06-20", "3840", "27", "5", "Horizon Arctic", "Titanic", "Batteries died on approach to LARS"),
    ("2022-07-01", "25", "5", "4", "Horizon Arctic", "Test", ""),
    ("2022-07-03", "3840", "13", "5", "Horizon Arctic", "Titanic",
     "Battery and control problems; Titan collided with the port bow of the Titanic and was disabled on recovery"),
    ("2022-07-06", "3840", "12", "5", "Horizon Arctic", "Titanic", ""),
    ("2022-07-08", "30", "4.2", "5", "Horizon Arctic", "Test", ""),
    ("2022-07-11", "10", "3.5", "5", "Horizon Arctic", "Cameron Canyon", ""),
    ("2022-07-14", "3840", "11.9", "5", "Horizon Arctic", "Titanic", "Issues with tracking and communications"),
    ("2022-07-15", "3840", "10.9", "5", "Horizon Arctic", "Titanic",
     "Power failure on the bottom. There was also a loud bang heard by those inside the submersible on surfacing"),
    ("2022-07-19", "3840", "12.75", "5", "Horizon Arctic", "Titanic", "Thruster control mapping failure, electrical problems"),
    ("2022-07-22", "3840", "11.1", "5", "Horizon Arctic", "Titanic", "Port horizontal thruster flooded"),
    ("2022-07-23", "2954", "12.1", "5", "Horizon Arctic", "Hydrographic feature", ""),
    ("2023-05-31", "10", "2", "5", "Polar Prince", "Test", "Software and camera issues"),
    ("2023-06-05", "10", "2", "5", "Polar Prince", "Southeast of Cape Race", "Poor visibility on the surface"),
    ("2023-06-13", "10", "2", "5", "Polar Prince", "Northeast of the Gully", "Ballast system issue"),
    ("2023-06-18", "3346", "2.05", "5", "Polar Prince", "Titanic", "Occurrence dive"),
)
REC_M22 = dict(
    fuji=dict(fuji_m=3776.0, depth_m=3800.0, psi=5554.5, coin_mm=20.0),
    reports=[("米沿岸警備隊", "2025年8月", "uscg"), ("米国の運輸安全委員会", "2025年10月", "ntsb"), ("カナダの運輸安全委員会", "2026年6月", "tsb")],
    side=dict(len_ft=22.0, len_m=6.7, seats=5, bolts=18),
    org=dict(n=8, vacant={"技術部長"}, first="CEO", staff=15),
    paper=dict(waiver=["experimental submersible vessel", "not been certified by any regulatory body"],
               plan=["guests who help fund OceanGate expeditions"], death=9,
               # 🆕 ⑤b-4（2026-10-15）：NTSB p1063・TSB §1.26.3.1＋NTSB p1024（ブログの引用）・NTSB p1023（脚注17）・NTSB p1047・TSB §1.12.1（点検の報告）・
               #   NTSB p1023＋TSB §1.12.1（業界の委員会の手紙）。英字は原文のまま（行の切れ目だけ入れた）
               model=["theoretical models of composite structures", "that assumed perfect geometry and fiber orientation",
                      "should have validated them through physical testing"],
               blog=["Why Isn’t Titan Classed?", "by itself, classing is not sufficient to ensure safety"],
               fn17=["a path for owners to prove seaworthiness of new technology", "no “experimental” design endorsement",
                     "for vessels carrying passengers or cargo"],
               emp=["paying clients as “mission specialists.”", "you can’t just change the title of a person", "when you’re receiving compensation."],
               qa18=["visible voids and delaminations", "end segments that had been cut off", "a full inspection of the cylinder and the bond lines",
                     "before any dives were conducted with people on board"],
               mts=["unanimous concern regarding the development of ‘TITAN’", "the current “experimental” approach adopted by OceanGate",
                    "could result in negative outcomes (from minor to catastrophic)", "a prototype testing program that was reviewed",
                    "and witnessed by a classification society"]),
    appb=_TW_ROWS, deep="3840", n_deep=13, years={"2021": 10, "2022": 13, "2023": 4},
    marks=dict(dome={"2021-06-30"}, batt={"2022-06-20"}, thr={"2021-07-03", "2022-07-19", "2022-07-22"},
               wt={"2021-07-09", "2021-07-19", "2021-07-24"}, com={"2022-07-14"}),
    appa=dict(descent=(("9:19:36", "SST", "I hsvr trscking"), ("9:19:43", "T", "descendingb thru 235"), ("9:19:49", "SST", "i have tracking"),
                    ("9:20:02", "T", "yeah")),
              restore=(("10:11:55", "T", "lost system oand chat settings"), ("10:14:17", "T", "yes"), ("10:14:35", "T", "all good here"),
                    ("10:15:39", "SST", "ack all good")),
              niskin=(("10:36:50", "SST", "remember to write down the location and time of niskin deployment"), ("10:38:06", "T", "n?"),
                    ("10:38:30", "SST", "remember to write down the location and time when you deploy the niskin bottle"),
                    ("10:39:36", "T", "when? messages truncated"), ("10:39:57", "SST", "when you deploy niskin"), ("10:40:01", "SST", "write down time"),
                    ("10:40:04", "SST", "andn location"), ("10:40:56", "T", "no niskin. never cleaned and string baf")),
              last=(("10:47:26", "T", "dropped two wts"),)),
    depth=(("9:19", 235.0), ("9:23", 436.0), ("9:31", 680.0), ("10:11", 2203.0), ("10:15", 2289.0), ("10:40:50", 3149.0), ("10:47:02", 3341.0),
           ("10:47:08", 3346.28)),
    seabed=3800.0, gap=("9:53", "10:10"),
    bow=dict(ese=112.5, ene=67.5),
    two=dict(seabed=500),
    clock={"8:20", "8:24", "9:04", "9:05", "9:14", "9:23", "10:47:02"},
    # 🆕 ⑤b-4（2026-10-15）：第4〜7章。原文＝ref/ep22/src/ep22_pages.txt（頁は cuts/ss.REC_DOCS の通し番号）
    #   send＝NTSB p1017「sent two to three messages every minute」（印の間隔は模式＝この幅の中なら通す）
    send=dict(lo=2.0, hi=3.0),
    #   proto＝USCG p39「Internal contacts and backup personnel will be called following 1 hour of no communications plus required surface time」
    #     「An additional 3 hours of local surface search will be done before contacting outside emergency personnel」・TSB §1.3.3（at 1500・3-hour surface search）
    proto=("連絡が途絶える", "浮き上がるのを待つ", "近くの海面を探す", "外に知らせる"), proto_role=("LINE", "company", "company", "company"),
    #   none＝TSB §2.5「did not have a means of determining where the Titan was underwater」「did not have any contracts in place with these ROV operators」／
    #     USCG p162「OceanGate did not make any external notifications」・p164「The letter, nor any other separate correspondence, disclosed that there was a crack found」
    none=dict(rescue=("水の中の位置を知る手段", "ROV の会社との救助の契約"), told=("客", "当局", "船級協会")),
    #   say＝NTSB p1025・USCG p111・USCG p301・NTSB p1048（報告書が引く英字のまま・行の切れ目だけ入れた）・色＝話した人の役
    say=dict(comp=("LINE", (("“better in compression than tension”",),)),
             letter=("company", (("there was no damage to the main cylindrical section,", "which is the critical part and a shape",
                                  "that is far better understood"),)),
             tv=("company", (("I’d like to be remembered as an innovator.",), ("I’ve broken some rules to make this.",))),
             rec=("company", (("there is not a lot of confidence on your part", "in the engineering that went into this vessel"),))),
    #   layers＝NTSB p1059「the five 1-inch-thick layers」・p1040「between layers 1 and 2 and the other was between layers 3 and 4」・
    #     p1041「layer 1, the innermost co- bonded layer」・p1059「these adhesive interfaces contained long extended voids」
    layers=dict(n=5, inch=1.0, sep={(1, 2), (3, 4)}, void={(1, 2), (3, 4)}),
    #   ruler＝TSB §1.3「approximately 3800 m」・TSB §1.12.1「rated up to 6000 m」「a goal of 2.25 for the safety factor」・
    #     USCG p114「the 4,500 m (14,764 feet) that was the target max pressure depth」・NTSB p1025「an implosion depth about 13,200 meters」
    ruler=dict(titanic=3800.0, goal=6000.0, op=4500.0, fail=13200.0, sf=2.25),
    model=dict(dome_m=3000.0),                 # TSB §1.12.1「failed at pressures equivalent to depths of around 3000 m」
    #   klass＝NTSB p1022「reviewing plans and documentation before and during construction … witnessing critical testing」
    klass=("設計を確かめる", "工事を確かめる", "試験に立ち会う"),
    meet=("CEO", "運航部長", "社員", "社員", "社員"),     # TSB §1.12.1「the CEO, the director of operations, and 3 other OceanGate employees」
    crack=3,                                    # TSB §1.12.1「3 interior cracks on the forward port side of the cylinder」
    shell=dict(left="鋼かチタンの球", right="炭素繊維の筒"),   # TSB §1.13「typically constructed of steel or titanium」「typically spherical」
    #   tc＝USCG p274「where the material is primarily under tension」（旅客機の胴体＝中から外へ押す）・「less effective」（深い海の殻＝外から押しつぶす）
    tc={"旅客機の胴体": True, "深い海の殻": False},         # 矢印が外向きか
    # 🆕 ⑤b-5（2026-10-15）：第8〜9章（原文＝ref/ep22/src/ep22_pages.txt・頁は cuts/ss.REC_DOCS の通し番号）
    #   cards＝(題, 中身, 役)。USCG p118「Grafil 37-800, supplied by Mitsubishi Chemical Carbon Fiber & Composites Inc.」・p174「Toray Composite Materials
    #     America’s」（期限切れの材料の話は3冊に無い＝台本 ②）・NTSB p1027「The model pressure vessel … imploded」「stopped at 2,500 meters … going to fail」・
    #     TSB §1.12.2「creating the cylinder in 5 layers, each of which was cured separately」「a layer of adhesive was applied」・§1.16「would reasonably have been
    #     expected to survive」「more than 82% of its fatigue life」・§1.12.2「detect damage in real time」・§2.1「was therefore unknown」・USCG p289「strongly
    #     suggests」・NTSB p1059「likely sustained damage」・TSB §1.10.10.1「it cannot be determined」・NTSB p1031「based on the acoustic activity of the v1 pressure
    #     vessel … and of the sub-scale pre-preg pressure vessels」・p1065「never produced the type of acoustic emission signal that would have triggered an alert」
    cards=dict(wind2=(("1つ目の筒", "樹脂の槽をくぐる糸", "LINE"), ("2つ目の筒", "樹脂を含ませたテープ", "sub")),
               mat=(("1つ目の筒の糸", "三菱ケミカル系", "LINE"), ("2つ目の筒のテープ", "東レの米国の会社", "sub"), ("期限切れの材料の話", "3つの報告書に無い", "ALERT")),
               m20=(("1つ目の模型", "壊れた", "ALERT"), ("2つ目の模型", "寸前で試験を止めた", "ALERT")),
               cure=(("1層を巻く", "テープを巻く", "INK_W"), ("固める", "真空の袋で", "INK_W"), ("接着剤の膜", "表面に塗る", "INK_W"), ("次の層へ", "上に重ねる", "INK_W")),
               life=(("いちばん強い試料", "耐えた見込み", "tsb"), ("いちばん弱い試料", "82%超を使った可能性", "ALERT")),
               path=(("壊れるまでの回数", "", "LINE"), ("音の監視", "その場で分かる", "company")),
               views=(("米沿岸警備隊", "強く示す", "uscg"), ("米運輸安全委員会", "可能性が高い", "ntsb"), ("カナダの調べ", "決められない", "tsb")),
               base=(("1つ目の船体と模型", "その音を使う", "company"), ("警告の基準", "30回で黄・50回で赤", "company"), ("2つ目の船体", "警告にならず", "sub"))),
    life=0.82,
    groove=dict(groove_in=5.0, end_in=5.166),   # NTSB p1043「could only accommodate a 5-inch-thick cylinder」「5.166 inches and 5.175 inches thick」
    coupons=(9, 9),                             # TSB §1.15「18 samples, 9 in the axial direction and 9 in the circumferential direction」
    shelf=dict(req=1.25, circ=1.11),            # TSB §1.12.2「changed its safety factor to 1.25」・§1.15「the calculated safety factor was 1.11」
    #   d80＝NTSB 図19（p1052）を原寸で読んだ点（映像方針・±2分）・音の山＝USCG p283「At 3:26:45 p.m.」（浮上の終わり＝USCG p234「nearing the surface」）
    d80=(("7:35", 0.0), ("10:05", 3840.0), ("13:35", 3840.0), ("15:16", 0.0)), d80_bang="15:26:45",
    rtm=dict(ae=8, dead=3, sg=8),               # NTSB p1031「eight acoustic emission sensors, eight circumferential (hoop) strain gages, and eight longitudinal」
    #                                             「Hoop and longitudinal strain gages were co-located」・p1051「Three of the eight acoustic sensors」
    ae=dict(up="15:17", esc="15:25:56", peak="15:26:45", band=("15:15", "15:30")),   # USCG p283・p286・NTSB p1052「between about 1515 and 1530」
    grind={1: 1, 2: 8, 3: 14, 4: 24},          # USCG 図143（p180）の表「Ground wrinkles」1・8・14・24・N/A（原寸で読んだ）
    year22=dict(year="2022", n=13, deep=7),     # USCG p235「While 7 of the 13 dives reached the TITANIC depth of 3840 m」・NTSB p1035「seven times」
    screen=dict(y=30, r=50),                    # NTSB p1031「30 hits … a yellow display warning. If 50 hits were detected, a red warning」
    ruler_role=dict(goal="company", op="company", fail="company", test="company", w650="uscg", w1k="ntsb"),
)
REC_M22["paper"].update(
    # 🆕 ⑤b-5：TSB §1.15・USCG p233＋p311（80回目）・USCG p233＋NTSB p1036（会社の説明）・USCG p290（CEO の指示・見方）。英字は原文のまま（行の切れ目だけ入れた）
    tsb115=["Assuming that the test results from the samples", "are representative of the properties of the carbon fibre cylinder",
            "it was unsafe for the Titan to have been repeatedly exposed", "to pressures equivalent to the depth of the Titanic or deeper"],
    u80=["the TITAN became entangled in the TITANIC’s stairwell", "For a moment, the TITAN remained trapped", "no incident report was filed for this event."],
    shift=["a shift in the TITAN’s position within its frame", "told the hull had shifted in its metal cradle"],
    u290a=["directed that no further investigation or assessments", "were necessary ahead of the next scheduled 2022 dive",
           "or during the TITAN’s extended layup period"],
    u290b=["neither the Director of Engineering", "nor anyone else onboard with the authority", "to assess the submersible’s safety",
           "possessed the necessary engineering expertise", "to interpret the strain gauge data"])
REC_M22["say"]["again"] = ("company", (("“Let’s dive again and see what happens”",),))       # NTSB p1036
REC_M22["none"]["insp"] = ("内張りを外して見る", "休ませて詳しく調べる")                       # USCG p290「remove the TITAN’s insert or take … out of service」
REC_M22["ruler"].update(test=4200.0, w650=650.0, w1k=1000.0)   # NTSB p1030「simulated maximum depth of 4,200 meters」・USCG p278「only 650 m」・NTSB p1030「1,000 meters」
REC_M22["clock"] |= {"15:15", "15:17", "15:30", "15:26:45"}
# 🆕 ⑤b-6（2026-10-15）：第10〜11章・終章（原文＝ref/ep22/src/ep22_pages.txt・頁は cuts/ss.REC_DOCS の通し番号）
REC_M22["paper"].update(
    #   USCG p237（基地のメール）・USCG p328＋p7（結論と要因の8つ目）・NTSB p1073＝p1060（所見2）・TSB §4.2.1＋§1.28.5・USCG p307・TSB §1.30.2（英字は原文のまま・行の切れ目だけ）
    tarp=["a quote for a tarp for the submersible had been provided", "they had not received approval to proceed", "so the tarp was not purchased."],
    u8=["unprotected in inclement weather", "compromised the TITAN’s hull integrity.", "failure to conduct preventative maintenance on the TITAN’s hull",
        "or protect it from the elements"],
    n73=["After dive 82, the Titan sustained additional damage", "—of unknown origin—that further deteriorated", "and weakened the pressure vessel to a point",
         "where it could not survive a dive to the depth of the Titanic."],
    tc=["TC was unaware that the Titan was not registered", "with any flag state.", "both DFO and the CBSA had information about the Titan", "that TC was not aware of."],
    u307=["Encouraging employees to voice concerns", "without fear of retaliation", "and prioritizing safety over expediency", "could have prevented the sequence of events",
          "that led to the disaster."],
    drift=["past success is not a guarantee of future success,", "because this drift occurs gradually,", "it is not easily identifiable",
           "and may go unnoticed as risk levels grow over time."])
REC_M22["cards"].update(
    #   USCG p295「further weakened」・TSB §2.1.3「may have exacerbated existing damage」／TSB §4.2.1〜§4.2.4「the Board recommends that the Department of Transport」
    #   M26-02〜M26-07／c107 の問い（語り）と答え＝NTSB p1074「local buckling failure of the pressure vessel」・TSB §2.1「carbon fibre cylinder was the likeliest point
    #   of failure」／USCG p290「directed that no further investigation or assessments were necessary」／USCG p307・NTSB p1074・TSB §3.1（会社）
    tow=(("米沿岸警備隊", "さらに弱った", "uscg"), ("カナダの調べ", "傷を広げたかも", "tsb")),
    rec6=tuple((f"M26-0{k}", "運輸省へ", "tsb") for k in range(2, 8)),
    q3=(("何が壊れたのか", "窓でなく炭素繊維の側", "sub"), ("なぜ潜り続けたのか", "調べずに続けた", "company"), ("誰なら止められたのか", "まず会社自身", "company")))
#   temp＝TSB §1.22「the average high … was -0.5° and the average low was -5.5°」（単位は「°」だけ＝℃ と書かない）
REC_M22["temp"] = dict(hi=-0.5, lo=-5.5)
#   risk＝TSB §1.17.12.1「a risk index of greater than 48 was considered to be a strike」「had a risk index of 35」・USCG p78「three or more “strikes”」
REC_M22["risk"] = dict(day=35, strike=48, n=3)
#   cols＝列（調べの役の色）・段の名・札（字・主語の役）。USCG p5「failure to follow established engineering protocols … was the primary causal factor」・
#     p7 の 1)〜8)（1 設計と試験・2 cycle-life・3 real-time monitoring に頼る・4 incidents のあとも使う・5 hull design and construction の flaws・6 mishaps を調べず・
#     7 toxic workplace environment・8 preventative maintenance をせず外に）・p8 の 4)「the lack of comprehensive and effective regulations」・
#     NTSB p1074「failed to establish the actual strength and durability」「Contributing were … voluntary guidance and … regulations that were insufficient」
#     「Also contributing was OceanGate’s flawed analysis of their pressure vessel monitoring system data」・TSB §3.1「never validated」「fail progressively with
#     damage accumulating during each dive cycle」・§3.2「without any independent verification」
REC_M22["cols"] = dict(
    heads=(("米沿岸警備隊", "uscg"), ("米運輸安全委員会", "ntsb"), ("カナダの調べ", "tsb")),
    #   🔧 ⑤c'（10-15）：t2 は likely＝「とみられる」（TSB §3.1）。段の名は ed3ffec のまま（「（一部）」は ⑥ の前の注意＝mech22 の CL_TIER の注）
    #   🔧 ⑥（10-15）：図が一部だけの3段に「（一部）」（USCG p8 のその他の要因4つのうち1つ・TSB §3.1 の5段落のうち2つ・§3.2 の4段落のうち1つ）
    tiers=(("主な要因", "その他の要因（一部）"), ("推定原因", "寄与"), ("原因と寄与（一部）", "危険の所見（一部）")),
    items=dict(u0=(0, 1, (("確立した手順に従わず", "company"),)),
               u8=(0, 1, (("設計と試験が不十分", "company"), ("寿命を調べず", "company"), ("監視の装置に頼りすぎ", "company"), ("傷のあとも使い続けた", "company"),
                          ("船体の作りの欠陥", "sub"), ("不具合を詳しく調べず", "company"), ("懸念を言えない職場", "company"), ("整備せず外に置いた", "company"))),
               #   🔧 ⑤b-6 の門番 box：NTSB p1074 の推定原因の3つの部分（failed to establish the actual strength and durability・delamination damage that was
               #     subsequently exacerbated by additional damage of unknown origin・a local buckling failure）・TSB §3.1 の2つ目（did not follow standard engineering practices）
               ux=(0, 2, (("規則の足りなさ", "LINE"),)),
               n1=(1, 1, (("強さと寿命を確かめず", "company"), ("層のはがれと別の傷", "sub"), ("局所の座屈で壊れた", "sub"))), n2=(1, 2, (("規則と指針の足りなさ", "LINE"),)),
               n3=(1, 2, (("監視の記録の読み違い", "company"),)), t1=(2, 1, (("強さを確かめず", "company"), ("作りと試験が標準外", "company"))),
               t2=(2, 1, (("傷が積もって壊れたとみられる", "sub"),)),
               tx=(2, 2, (("独立した確認なし", "LINE"),))),
    gap=("ux", "n2", "tx"), u7=("u8", 6))
#   cmp＝重なる所3つ（USCG p7・NTSB p1073〜p1074・TSB §2.1・§3.1）・分かれる所2つ（2022年の音＝ca21・ca22 と同じ言葉＝USCG p289・NTSB p1059・TSB §1.10.10.1）
REC_M22["cmp"] = dict(heads=(("米沿岸警備隊", "uscg"), ("米運輸安全委員会", "ntsb"), ("カナダの調べ", "tsb")),
                      rows=(("same", "壊れたのは炭素繊維の筒", None), ("same", "強さと寿命を確かめず", None), ("same", "監視の記録を生かせず", None),
                            ("cells", "2022年の音の重み", ("強く示す", "可能性が高い", "決められない")), ("band", "最後の数秒の順番", "書き方が違う")))

# ── check_boxes・check_illu ──
# 22本目は両ファイルに足した値が無い（`git diff e7564b8 adbe2d5 -- tools/check_boxes.py tools/check_illu.py` は空）＝GATES に載せない。


GATES = {
    # 22本目は時計の時刻を含む並び（order）も×の印も使わなかった＝ORDER_REF_MIN は None・REC_WRONG は空。2段の帯（tiers）と役の色を使った＝
    # LANES_OK・REC_LANE・REC_ROLE・LANE_ROLE・TIER_ALERT が入る
    "check_axis": dict(REC_AXIS=REC_AXIS, LANES_OK=LANES_OK, REC_APPROX=REC_APPROX, REC_LANE=REC_LANE, REC_WRONG=REC_WRONG,
                       REC_ROLE=REC_ROLE, LANE_ROLE=LANE_ROLE, TIER_ALERT=TIER_ALERT, ORDER_REF_MIN=ORDER_REF_MIN),
    "check_qty": dict(REC_QTY=REC_QTY, REC_QTY_ROLE=REC_QTY_ROLE, REC_PEOPLE=REC_PEOPLE, REC_PEOPLE_PAGES=REC_PEOPLE_PAGES,
                      REC_PEOPLE_ROLE=REC_PEOPLE_ROLE, PEOPLE_CUTS=PEOPLE_CUTS_QTY),
    "check_mech": dict(REC_M22=REC_M22),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・（gate を渡せば）その門番の記録の表を22本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss は触らない）＝14・15・16・18・19・20・21本目の見本 `fixture_ep14`・
    `fixture_ep15`・`fixture_ep16`・`fixture_ep18`・`fixture_ep19`・`fixture_ep20`・`fixture_ep21` と重ねるとき（check_mech の selftest は14本目の検算と
    15・16・18・19・20・21・22本目の検算を1つの処理で回す＝先に14本目を全部差し込み、15・16・18・19・20・21・22本目は表だけ足す）。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が22本目の表で
       23本目の画を測る）。apply の前に**無かった名**（ss の AX_* …／門番の表）も覚えて、restore で**消す**
       ＝selftest のあとに22本目の名が本番へ残らない（fixture_ep15・fixture_ep16・fixture_ep18・fixture_ep19・fixture_ep20・fixture_ep21 と同じ作り）。
    ⚠️ fixture_ep21 までと違い、`titan_fig.GEO` は触らない（22本目の地点は無い・場所の表は ss の `GEO`＝SS_NAMES で差し込む）"""
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


CUTS_SHA = "adbe2d5"       # 22本目の章ファイルが最後に live だった版（章ファイルを23本目の空の器に替える前＝git の `adbe2d5`）
_CUTS22 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def cuts_ep22():
    """22本目の章ファイル（git の CUTS_SHA の `tools/cuts/`）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。"""
    if _CUTS22:
        return _CUTS22[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 22本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts22_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep22 の写真・頁を読む＝根の下の作業場所の
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
        try:
            old = importlib.import_module("cuts")
            got = (dict(old.PLAN), dict(old.SPEC))
        finally:
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
    if len(got[0]) < 200 or "c101" not in got[1]:
        raise RuntimeError(f"🔴 22本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}）")
    _CUTS22.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を22本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で23本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep22()
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
        if s.get("cuts") is not None:          # apply_cuts() の分＝23本目の PLAN・SPEC へ戻す
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
