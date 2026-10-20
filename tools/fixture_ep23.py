# -*- coding: utf-8 -*-
"""23本目（三豊百貨店崩壊事故のリメイク・1995-06-29・国会の三豊特別委員会 第6号の会議録〈K6〉・大法院とソウル高等法院の判決・ソウル市の白書の動画）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-20（17本目 中華航空140便墜落事故の ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `b800dbdb` と同じ）
  ・`cuts/ss.py` の23本目の値＝案C の出典の表（REC_DOCS＝K6-R・K6-市・K6-区・K6-検・K6-市b・K6-区b・大96・白書・国監内・大99・高96・法令・市告の13資料）・原文の道（REC_PAGES）・
    軸の型（AX_PM23・AX_P23・AX_Y23・AX_J23・AXI の項目 18）・棒（QG＝roofkg／QB＝kg240・kg400＝c804）・
    地図（衛星写真の表 SAT＝2点〈c511・c602〉・場所の表 GEO＝2点〈site・seocho〉）・
    写真の束の定数（顔だけモザイクの名簿 NEEDS_MASK＝4点・台紙の縁でない暗い帯の名簿 SLIDE_NOT_MOUNT＝5点）（23本目 ⑤b-2〜⑤b-7）。
    ILLU_* ほか23本目も空のままだった表（ILLU_SPLIT_TIMES・ILLU_CROWD_UNTIL・ILLU_ROLES …）・AXIS_DOCS・PEOPLE_*（人の形は23本目が使わなかった）・QDOC・QWHO・SLIDE_MOUNT（23本目は
    台紙の縁のある写真が0点＝空）も、23本目の状態として持つ（22本目の見本と同じ考え方）
  ・`GEO`（地図の場所2点）は **ss の名**（`cuts/ss.GEO`）＝`SS_NAMES` に入れた（fixture_ep22 と同じ。`titan_fig.GEO` ではない）。この見本は titan_fig.GEO を触らない
  ・門番の記録の表（check_axis＝REC_AXIS・REC_APPROX・REC_ROLE〈と、23本目も使わなかった LANES_OK・REC_LANE・REC_WRONG・LANE_ROLE・TIER_ALERT・ORDER_REF_MIN＝空の状態〉／
    check_qty＝REC_QTY〈と、23本目も使わなかった REC_QTY_ROLE・REC_PEOPLE・REC_PEOPLE_PAGES・REC_PEOPLE_ROLE・PEOPLE_CUTS＝空の状態〉／
    check_mech＝REC_M23〈模式図 `mech23.py` の記録の値〉／check_sat＝REC_SAT_AREA〈c511 の囲みの面積〉）。
    check_boxes（REC_*）・check_illu・check_photo_edge は23本目で足した値が無い（check_photo_edge の名簿は ss の SLIDE_*＝上）＝この見本の GATES に載せない
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を23本目の実物でも確かめている（check_mech の m23・check_sat の囲みの面積）＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は17本目の空の器にした
  （fixture_ep14〜ep22 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep23
      fixture_ep23.apply(sys.modules[__name__])   # その処理の中だけ ss・この門番の記録の表が23本目になる
      try: …（検算）
      finally: fixture_ep23.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14〜22本目の見本と重ねるとき（check_mech は14本目の検算と15〜23本目の検算を1つの処理で回す）は
      fixture_ep23.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと17本目以降の画に23本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。
■ 注意:
  ⚠️ 見本の頁の原文 `ref/ep23/src/ep23_pages.txt` は**23本目では作らなかった**（ss.REC_PAGES の道は残っていたが、ファイルが無い）＝check_illu の `_pages()` は None を返す。
     衛星写真 `ref/ep23/photo/gmap_g0*.png`（SAT の2点）は git の外（本線の作業ツリーにだけある）。無いときは check_sat の md5 の陽性対照を飛ばす（Actions）。
  ⚠️ 23本目の selftest のうち、**章ファイルの SPEC を読むのは check_sat の `_selftest_area` だけ**（地図のカット c511＝囲みの面積の記録）。
     check_mech の `_selftest_m23` は場面を selftest の中で `mech23.m23` で組む＝`apply(gate, tables_only=True)` だけで通る。
     check_sat は `apply(gate)`＋`apply_cuts()`（23本目の章ファイルを git の `CUTS_SHA`＝`b800dbdb` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ
     23本目に入れ替える・git が無い所では止める＝fail closed）を使う（`restore()` で17本目へ戻る・LIFO）。
  ⚠️ 23本目の章ファイルは `ss.vid`・`ss.head`・`ss.tailv` で **`footage.CLIPS`・`footage.USE`**（フリー素材の映像17カット＝c205・c211・c219・c308・c613・c704・c712・c817・c903・c905・c909・ca04・ca07・
     ca12・cb09・cb12・cc04）を引く＝本番の footage は17本目の表（`USE` 空・`CLIPS` は `ref/ep17/clips.json`）なので、`cuts_ep23()` は章ファイルを読む間だけ footage の2つを23本目の表
     （台帳 `ref/ep23/clips.json`・使う区間は git の `b800dbdb` の `tools/footage.py` の `USE = {…}` の1文を取り出して評価）に差し、読み終えたら戻す（`_footage23`）。
     これを差さないと22本目と違って23本目の章ファイル13本のうち9本（c2・c3・c6〜cc）が読み込みで落ちる（`ref/ep23/fb_<cid>.jpg`＝無い名を開きに行く）。23本目の footage の値は**ここに写していない**（git の `b800dbdb` が正本）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep23/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は23本目の道を持つ。
  ⚠️ `SAT`・`NEEDS_MASK`・`SLIDE_NOT_MOUNT` の鍵・値は **`ep23/` の名を文字で書いた**（本番の ss は `f"{EP}…"`／`P(…)` で組んでいた＝EP が ep17 になると `ep17/…`〈無い名〉に化ける。
     fixture_ep22 の SAT・SLIDE_NOT_MOUNT と同じ扱い）。説明の文は1字も変えていない（値＝git の `b800dbdb` の ss を評価した結果と同じ）。
     `SAT_CREDIT`（Google の帰属の決まり文句）は本番の ss に**残した**型の定数〈回をまたいで同じ〉＝この見本は同じ文を文字で持つ（`SAT` の credit が使う名・SS_NAMES には入れない）。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝23本目は 1.04）は見本に入れない（16・18〜22本目の見本も入れていない）＝本番の ss は今の値のまま残し、17本目の束で取り直す。
  ⚠️ 写真の束の定数のうち `TRIM`（`pages.json` から読む＝REF が替われば追う）・`OCR_NOT_TEXT`・`PRIVATE_OUT` は23本目も空のまま＝見本に入れない。
  ⚠️ `check_mech._M23_NEED`（＋ `_M23_NEED_B4`・`_M23_NEED_B5`・`_M23_NEED_B6`＝模式図 m23 の「先に起きることが先」の筋の表）・`NUM_M23`（札の数と時刻を拾う正規表現）・`VIEW_HEADS`・
     `view_dir_check`・`_m23_src_page` は**見本に入れず本番の check_mech に残した**（理由は check_mech の `REC_M23` の注＝`_M22_NEED`・`_M21_NEED` と同じ判断：
     見え方〈view〉と欄の名の約束で、記録の値〈時刻・数・座標・頁〉を持たない型の側の規則）。
  ⚠️ `check_axis` の役の色の判定（`_role_check`・`_hex`）・目盛りの「1日」の検査・秒の小数の読み方は型＝本番の check_axis に残した（表 REC_AXIS・REC_APPROX・REC_ROLE だけ見本）。
     `check_qty` の役の色の判定（`judge_bar`・`judge_people` の中）も型。`check_sat.area_check`（面積の照合の関数）も型＝本番に残した（表 REC_SAT_AREA だけ見本）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep23"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 23本目 ⑤b-3〜⑤b-6
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：次の回は下の表を**その回の資料と時刻**に替える（頁の番号の書き方・資料の名の決め方は REC_DOCS の注）。
#   REC_PAGES … 部品の出典（`rec=`）を当てる原文（`=== p<N> ===` で頁を割った1ファイル）＝23本目では**作らなかった**（この道のファイルは無い）
#   REC_DOCS  … 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面に出す名前・頁の出し方（print＝印刷の頁・none＝頁の無い資料）
#   ILLU_* … 23本目は人・秒の札・時計の札・描いてよい数・想定の札・壊れる物・縮尺を持たない上から見た絵・潜水艦・音の輪・混ざりのつなぎ待ちを使わなかった＝
#            空のまま（下の値）。割れる時刻（ILLU_SPLIT_TIMES）も23本目は使わなかった（空）
REC_PAGES = REF / "src" / "ep23_pages.txt"      # 部品の出典（`rec=`）を当てる原文（git の外＝手元だけ）。その型を初めて使う ⑤b のチャットで作る（23本目では作らなかった）
# 🆕 2026-10-18（23本目 ⑤b-3）：23本目の資料の表（台本 第2版 §10 の略号のまま）。K6-＊は**国会の三豊特別委員会 第6号の会議録1冊**（国政調査の報告書と、
#    その添付＝ソウル市・瑞草区・ソウル地検の報告）＝頁は**会議録の PDF の頁＝印刷の頁**（`ref/ep10/src/assembly_sampoong_tokui_no6_19950912_id19114.txt` の
#    `=== [PDF p.N] ===`）。台本の「K6-検 p.47」→ SPEC は「K6-検 p47」（点を落とす＝parse_rec は「p数字」）。範囲＝その報告の頁（市b・区b は8月9日の添付）。
#    大96（大法院の判決 96도1231）は頁の無い資料＝「大96 p1」（画面は名だけ）。⚠️「K6-市b」は「K6-市」を含む＝parse_rec は長い名から当てる
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    "K6-R": dict(range=(1, 34), name="国会の調査報告（1995年）", page="print", base=0),
    "K6-市": dict(range=(34, 41), name="ソウル市の報告（国会の会議録）", page="print", base=0),
    "K6-区": dict(range=(42, 45), name="瑞草区の報告（国会の会議録）", page="print", base=0),
    "K6-検": dict(range=(45, 53), name="ソウル地検の報告（国会の会議録）", page="print", base=0),
    "K6-市b": dict(range=(53, 58), name="ソウル市の報告（国会の会議録）", page="print", base=0),
    "K6-区b": dict(range=(58, 59), name="瑞草区の報告（国会の会議録）", page="print", base=0),
    "大96": dict(range=(1, 1), name="大法院の判決（1996年）", page="none", base=0),
    "白書": dict(range=(1, 700), name="ソウル市の白書（1996年）", page="print", base=0),
    # 🆕 2026-10-19（⑤b-6）：第10〜11章・終章で初めて使う資料（原文＝ref/ep10/src/＝git の外）
    "国監内": dict(range=(1, 200), name="国政監査のソウル市の報告（1995年）", page="print", base=0),   # assembly_audit1995_naemu_seoul（内務委 1995-10-10）
    "大99": dict(range=(1, 1), name="大法院の判決（1999年）", page="none", base=0),                   # 98다29797（区の国家賠償）
    "高96": dict(range=(1, 1), name="ソウル高等法院の判決（1996年）", page="none", base=0),           # 96노118（公開の部分）
    "法令": dict(range=(1, 1), name="韓国の法令（国家法令情報センター）", page="none", base=0),        # 1995-12-30 の5つの法律
    "市告": dict(range=(1, 1), name="ソウル市の公告（2026年）", page="none", base=0),                 # 事故を悼む造形の作品の公募の結果
}
ILLU_SPLIT_TIMES = ()                      # 資料で割れる時刻＝画面に時計・時刻の札として出さない
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
#    入れた→ `tools/fixture_ep21.py` へ移して空にした。23本目も割れる時刻の札を使わなかった＝空のまま
AXIS_DOCS = {}


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：軸の型（`tools/axis.py`・門番 `check_axis`）── 23本目 ⑤b-3〜⑤b-6（時間の帯・年表）
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の AX_*・AXI の項目は23本目の値（17本目の ⑤b-1 で見本 fixture_ep23 へ）。
#   値と頁は国会の三豊特別委員会 第6号の会議録・高等法院の判決の原文（ref/ep10/src/）で当てた＝門番の側の表（check_axis.REC_AXIS）と照らされる（§5b-88）。
# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
AXI = {}

# 🆕 2026-10-18（23本目 ⑤b-3）：第2章の時間の帯（c319）。時刻は事故の日（1995-06-29）のソウル。色＝**役の色**（だれの動きか＝会社 COMPANY・構造技術者 ENGINEER〈水色〉・
#   崩れる＝ALERT）＝門番 check_axis が記録の表（REC_AXIS・REC_ROLE・REC_APPROX）で値・頁・色を照らす（§5b-88）。
#   原文＝検察の報告 p.47「14:00 : 대책회의 개최」「도착(15:10)」「16:00 : 대책회의 계속」「17:30 : … 야간보강작업 준비 착수」・別紙2 p.52「16:40경 대책회의에서」・
#     ソウル市 p.34「17:55경」・瑞草区 p.42「17:55경」（崩れはじめの時刻は記録で割れる＝台本 §1-5＝この動画は 17:55ごろ・幅は次の c402 の時計で言う）。
#   ⚠️ 15:10〜17:55 の括弧は札なし（語りの「およそ2時間45分」は字幕＝数と単位の札は echo で鳴る＝22本目の教訓）
AX_PM23 = dict(view="clock", span=("13:40", "18:20"), ticks=("14:00", "15:00", "16:00", "17:00", "18:00"))
AXI.update({
    "m1400": dict(k="pt", at="14:00", t="対策の会議", rec="K6-検 p47", c="company", anchor="end"),
    "a1510": dict(k="pt", at="15:10", t="構造技術者が着く", rec="K6-検 p47", c="engineer", anchor="end"),   # ⚠️ 門番 axis：start だと 16:00 の縦の線が札を貫いた
    "m1600": dict(k="pt", at="16:00", t="会議の続き", rec="K6-検 p47", c="company", anchor="end"),
    "r1640": dict(k="pt", at="16:40", t="「危険はない」", rec="K6-検 p52", c="engineer", approx=True, anchor="end"),
    # ⚠️ 門番 axis：16:40・17:30 の札の向きを総当たりで試した（scratchpad の axtry.py）＝「夜の補強の準備」はどの向きでも縦の線が隣の札を貫く＝「補強の準備」
    "p1730": dict(k="pt", at="17:30", t="補強の準備", rec="K6-検 p47", c="company", anchor="end"),
    "f1755": dict(k="pt", at="17:55", t="崩れはじめる", rec=["K6-市 p34", "K6-区 p42"], c="ALERT", approx=True, big=True, anchor="end"),   # ⚠️ 門番 layout：start だと「17:55ごろ」が右の端 1848 の外
    "b1510": dict(k="br", a="15:10", b="17:55", t="", rec=["K6-検 p47", "K6-市 p34"]),
})
# 🆕 2026-10-18（23本目 ⑤b-4）：第5章の許可の年表（c604）。🔧 一覧の「1976〜1994 の7点」→ **語りにある3点だけ**（1976・1986＝前の c603 の語り＝沈めて・
#   1987年7月＝c604 の語り）。1989年11月の仮使用・12月の開店・1990年の竣工・1994年の用途の変更は後ろのカット（c614・c616・c617）の語り＝描かない（軸の教訓）。
#   原文＝国会の報告 p.30「아파트지구로 지정:1976.8.29.건설부」「아파트지구개발기본계획변경:1986.4.24.건설부-주택용지를 … 지구중심지역으로 변경」「승인:1987.7.21.서울특별시」・
#     ソウル市 p.35「76.8.구획정리사업시 아파트지구지정(서울시)」「86.5.아파트개발계획(아파트용지→지구중심)」「87.7.21.사업계획승인(지하4,지상5,연면적71,136㎡)」・
#     瑞草区 p.43「76.8.29.:아파트지구지정(건설부장관)」「백화점건축허가–87.7.18.(서울특별시장)」・検察 p.48「86.4.24.」「87.7.21.」
#   ⚠️ 記録が割れる＝1976年の指定は建設部（国会・区）／ソウル市（市）・1986年は4月24日・建設部（国会・検察）／5月・ソウル市（市）・1987年の承認は7月21日（国会・市・検察）／
#      7月18日（区）＝**1976年と1986年は年だけ・色は中立（線の色＝だれかを言わない）・1987年は月まで（語りの「1987年7月」）・市の紫（語り「ソウル市が承認」）**
AX_P23 = dict(view="date", span=("1974-06-01", "1990-06-01"), ticks=("1975", "1980", "1985", "1990"))
AXI.update({
    "apt76": dict(k="pt", at="1976-08-29", t="マンションを建てる地区", rec=["K6-R p30", "K6-区 p43", "K6-検 p48"], c="LINE", fmt="y", anchor="start"),
    "ctr86": dict(k="pt", at="1986", t="地区の中心の土地へ", rec=["K6-R p30", "K6-市 p35", "K6-検 p48"], c="LINE", fmt="y", anchor="end"),
    "ok87": dict(k="pt", at="1987-07", t="事業の計画の承認", rec=["K6-市 p35", "K6-R p30", "K6-検 p48"], c="city", fmt="ym", anchor="end", big=True),
})
# 🆕 2026-10-19（23本目 ⑤b-5）：第9章の年表（ca02＝帯の2回目）。竣工（1990年7月）→ 崩れた日（1995年6月29日）＝およそ5年（括弧＝数は語り）・
#   そのあいだの合図は区間の帯だけ（🔴 1995年4月の水漏れ・6月初めの照明・6月21日の工事は後ろのカット〈ca06・ca08・ca10〉の語り＝点を描かない）。
#   原文＝国会の報告 p.31「사용검사:1990.7.27.서초구청」・ソウル市 p.35「90.7.27.사용검사」・瑞草区 p.44「90.7.27.:건축물시설준공」・検察 p.46「90.7.27.준공검사」・
#     国会の報告 p.4「1995.6.29.발생한」。⚠️ 検察 p.46 は「89.11.완공」（工事の終わり）も書く＝竣工の検査の日で置く・月まで（c616 の語り「竣工の検査は、翌年の7月」）。
#   色＝中立（竣工＝線の色）・崩れた日＝赤
AX_Y23 = dict(view="date", span=("1989-06-01", "1996-01-01"), ticks=("1990", "1991", "1992", "1993", "1994", "1995"))
AXI.update({
    "done90": dict(k="pt", at="1990-07", t="竣工", rec=["K6-R p31", "K6-市 p35", "K6-区 p44", "K6-検 p46"], c="LINE", fmt="ym", anchor="start"),
    "fall95": dict(k="pt", at="1995-06-29", t="崩れた日", rec="K6-R p4", c="ALERT", anchor="end", big=True),
    "br9095": dict(k="br", a="1990-07", b="1995-06-29", t="", rec=["K6-R p31", "K6-R p4"]),
    "sig9095": dict(k="span", a="1990-07", b="1995-06-29", t="合図の記録", rec=["K6-R p31", "K6-R p4"], c="AMBER"),
})
# 🆕 2026-10-19（23本目 ⑤b-6）：第11章の判決の年表（cc16＝年表の2回目）。起訴（1995-07-26＝前の cc02 の語り）→ 1審（1995-12-27）→ 2審（1996-05-10）・
#   2審で被告人19人のうち1人に懲役7年6か月（いくつもの罪を合わせた刑＝語り）。🔴 大法院の日付（1996-08-23）は次の cc17・災難管理法（1995-07-18）は cc22・
#   5つの法律（1995-12-30）は cc23 の語り＝点を描かない。原文＝検察の報告 p.48「기소일자:7.26.」・高96「원심판결 서울지방법원 1995.12.27.선고」
#   「서울고등법원 1996.5.10.선고 96노118판결」「피고인B을 징역 7년6월에」（被告人は A〜S の19人）。色＝起訴と判決は国（検察・裁判所＝青）
AX_J23 = dict(view="date", span=("1995-06-15", "1996-07-01"), ticks=("1995-07", "1995-10", "1996-01", "1996-04"))
AXI.update({
    "kiso95": dict(k="pt", at="1995-07-26", t="起訴", rec="K6-検 p48", c="state", anchor="start"),
    "j1_95": dict(k="pt", at="1995-12-27", t="1審の判決", rec="高96 p1", c="state", anchor="end"),
    # 🔧 門番 layout：札が3段だと3段目「罪を合わせた刑」が下の注に触れた＝2段（「19人のうち」は語り＝字幕）
    "j2_96": dict(k="pt", at="1996-05-10", t="2審の判決", rec="高96 p1", c="state", anchor="end", big=True, chips=["懲役7年6か月（1人）"]),
    "j2_sum": dict(k="chips", at="1996-05-10", chips=["罪を合わせた刑"], rec="高96 p1", i0=1),
})


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：量の型（棒・人の形）・決め所の出どころの札 ── 23本目 ⑤b-4
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_QTY＝§5b-88）＝回を替えたら両方を替える。
#    人の形（PEOPLE_*）・決め所の出どころの札（QDOC・QWHO）は23本目は使わなかった＝空（22本目の状態＝空の状態として持つ）
QG = {}
QB = {}
# 🆕 2026-10-18（23本目 ⑤b-4）：c804 屋上の床が前提にした重さと冷却塔の重さ（判決 大96 理由2.가「지붕층 슬래브는 … 적재하중이 240㎏/㎡로 설계, 시공되어 있으므로
#   등분포하중이 400㎏/㎡인 냉각탑을 설치하려면」）＝頁の無い資料＝「大96 p1」。色＝前提は線の色（設計の値）・冷却塔は赤（前提を超える＝欠陥）
#   ⚠️ 群の名に数字を書かない（22本目の門番 qty の教訓）＝「1平方メートルあたり」は単位の書き方「キログラム／平方メートル」に
QG.update({"roofkg": dict(id="roofkg", t="床にかかる重さ（キログラム／平方メートル）", ticks=(0, 100, 200, 300, 400, 500), rows=("屋上の床の前提", "冷却塔"))})
QB.update({
    "kg240": dict(k="bar", g="roofkg", t="屋上の床の前提", v=240, rec="大96 p1", c="LINE"),
    "kg400": dict(k="bar", g="roofkg", t="冷却塔", v=400, rec="大96 p1", c="ALERT"),
})

# 人の形（1つ＝1人）＝**14本目 c204〜c206 と22本目 c303 だけの例外**（ルール §C-1 #59・亡くなった方の数には使わない）。23本目は使わない＝空のまま
PEOPLE_ORDER = ()
PEOPLE_SETS = {}
PEOPLE_REC = {}
PEOPLE_CUTS = ()     # 🔴 門番 check_qty がこの外の人の形を止める（亡くなった方の数に使わない）

# 決め所の出どころの札（`fig=("quote", …)`）の資料の名＝23本目は使わなかった
QDOC = {}
QWHO = {}


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：地図の型「衛星写真＋描き足し」（`tools/satmap.py`・門番 `tools/check_sat.py`）── 23本目 ⑤b-4
# ══════════════════════════════════════════════════════
#   SAT＝撮った衛星写真（`ref/ep23/eizou_build/helpers/gshot23.py`）。
#     🔴 写真そのものは公開リポに置かない（git の外・Modal の保管庫 `jiko-assets` の `ref/ep23/photo/`＝`modal_app.pull_private`）。
#        ここに置けるのは md5 だけ＝門番が手元の絵と照らす（撮り直したら md5 と描き足しの座標を見直す）。
#     🔴 Actions は保管庫を読めない＝地図のカットは理由を出して飛ばす（`build_jiko.drop_missing_sat`）・検品画像は Modal の `qa`。
#   GEO＝描き足しに使う場所。src＝報告書でその場所の名が出る所・how＝座標の出どころ（「報告書の値」か「一般の座標」）。
#     🔴 確かめていない場所に点を置かない（門番）。×は報告書の座標の場所だけ・一般の座標を使ったカットは断りに「一般の座標」
#   ⚠️ `SAT` の file は本番では `f"{EP}photo/…"`＝この見本は `ep23/` の名を文字で書いた（EP が ep17 になっても23本目の絵を指す）。
#      credit の `SAT_CREDIT`＝Google の帰属の決まり文句は本番の ss にも残してある型の定数（同じ文）
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"
# 🆕 2026-10-18（23本目 ⑤b-4）：地図2カット（c511・c602）の衛星写真＝`ref/ep23/eizou_build/helpers/gshot23.py` で2回撮り、`gseam22.py` で比べて
#    線の無い方（2回目）を採った（G02 の1回目は y 947〜951 に読み込みの継ぎ目＝飛び出し 27.0）。保管庫 `jiko-assets` の `ref/ep23/photo/…` に入れ、
#    取り戻して md5 が一致（modal の exit 1 は成功のあとの「✓」を cp932 で出せないだけ＝PYTHONIOENCODING=utf-8 で消える）。
#    G01＝百貨店の跡を中心・ズーム17（横 約1.2キロ＝記録の面積と同じ面積の円が半径 約231画素）／G02＝ズーム13（横 約19キロ＝北に漢江・ソウルの南）
SAT = {
    "G01": dict(file="ep23/photo/gmap_g01_sampoong_site.png", ll=(37.4981551, 127.0131528), z=17, md5="05821c46bc69db60864865c9125d3dd8", credit=SAT_CREDIT),
    "G02": dict(file="ep23/photo/gmap_g02_seoul_seocho.png", ll=(37.512, 127.010), z=13, md5="4636dc104ade382aa7062dcda2d3d5fb", credit=SAT_CREDIT),
}
# 🆕 2026-10-18（23本目 ⑤b-4）：描き足しの場所＝確かめた座標だけ。
#    ⚠️ 法院（ソウル中央地方法院）の Wikidata の座標（Q16097683＝37.4937, 127.0086＝小数4桁）は、撮った G01 の Google の印（跡地の南西 約275メートル）から
#       約400メートルずれていた＝使わない。G02（ズーム13）では跡地と法院が 27画素（画面で16画素）しか離れず点が重なる＝c602 は跡地の点だけ（法院は c601 の写真）
GEO = {
    "site": dict(ll=(37.4981551, 127.0131528), src="K6-検 p45（`서울 서초구 서초동 1685-3`）",
                 how="一般の座標（跡地に建った建物＝Wikidata Q14927038〈三豊百貨店〉・Q28699527〈アクロビスタ〉の座標）"),
    "seocho": dict(ll=(37.48373, 127.032441), src="K6-検 p45（`서울 서초구`）", how="一般の座標（区の代表点＝Wikidata Q20395〈瑞草区〉）"),
}


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：写真の束の定数（顔だけモザイクの名簿・スライドの台紙の黒い縁の名簿）── 23本目 ⑤b-2
# ══════════════════════════════════════════════════════
# 🆕 2026-10-18（23本目 ⑤b-2）：了承② 決め2（研究院・歴史編纂院の私人は顔だけモザイク）＝範囲は `ref/ep23/eizou_build/mask23.tsv`（⑤b-1 に原寸で測った・
#    元の画像の画素）→ 束（`qa_out/ep23_assets.py build`）で升 14px の升目にした。歴史編纂院 104 は10本目に顔と名前を隠した版をそのまま使う
#    本番の ss は `P("…")` で組んでいた＝EP が ep17 になると鍵が `ep17/…`（無い名）に化ける＝見本は **`ep23/` の名を文字で書いた**（値＝git の `b800dbdb` の
#    ss.NEEDS_MASK を評価した結果と同じ4点・説明の文は1字も変えていない）。🔴 門番 check_photo_mask の本番は、この名簿を `ss.NEEDS_MASK` から読む（selftest の対象ではない）
NEEDS_MASK = {
    "ep23/sire_52400.jpg": "研究院 52400（c104・cd08）＝手前の右を歩く男性（私人）の横顔だけモザイク（左の男性は後ろ姿）",
    "ep23/hs_2301030077_0.jpg": "歴史編纂院 077（cb06）＝写真展を見る大人の男性と子ども（私人）の顔だけモザイク＋⑤c'（10-19）右の展示の写真9枚（人の顔）",
    "ep23/hs_2301030100_0.jpg": "歴史編纂院 100（cd06）＝⑤c'（10-19）慰霊塔の除幕の参列者・立っている人・たすきの2人・カメラの人（私人）の顔だけモザイク（後ろ姿は隠さない）",
    "ep23/missing_board_01.jpg": "歴史編纂院 104（cb03）＝行方を探す掲示板の顔写真と名前を隠した版（10本目 `ref/ep10/missing_board_01.jpg`）",
}
# 🆕 2026-10-13（21本目 ⑤b-7）：**スライドの台紙の黒い縁がある写真**（名 → 何か）。23本目の束は研究院・歴史編纂院・本部・Commons・イメージ＝スライドの走査が無い＝**SLIDE_MOUNT は空**
#    （台紙の縁のある写真は0点）。門番 `tools/check_photo_edge.py` は SLIDE_MOUNT が空のとき、束の全点を測って「暗い帯のある点が SLIDE_NOT_MOUNT に全部載っているか」を見る
SLIDE_MOUNT = {}
# 🆕 2026-10-18（23本目 ⑤b-2）：`python qa_out/ep23_assets.py edges` で束の全101点を測った＝MIN_EDGE 以上は5点。帯の中の1px ごとの明るさとばらつき
#    （scratchpad `band23.py`）で、ばらつきの大きい3点は写真の中身・ほぼ一様に暗い2点（31740 の下・c216b の左右）は絵で見た（原寸の帯と全体）＝台紙の縁は0点
#    本番の ss は `P("…")` で組んでいた＝見本は **`ep23/` の名を文字で書いた**（値＝git の `b800dbdb` の ss.SLIDE_NOT_MOUNT を評価した結果と同じ5点・説明の文は1字も変えていない）
SLIDE_NOT_MOUNT = {
    "ep23/c203.jpg": "夜の救急車の列＝右 4.9%・下 5.0% は夜の暗がり（帯の中の明るさのばらつき 30〜50＝写真の中身）",
    "ep23/sire_31733.jpg": "跡地（2000年2月）＝下 5.0% は手前の地面の陰（ばらつき 18〜47）",
    "ep23/sire_31740.jpg": "跡地の空き地（2000年2月）＝下 5.0% は舗装の上の影（撮影者の影が伸びる・原寸の帯で見た）",
    "ep23/sire_50279.jpg": "瑞草洞の通り（1995年）＝左 4.5% は通りの暗い建物の陰（ばらつき 38〜57）",
    "ep23/stock/c216b.jpg": "イメージ（黄色いバルブ）＝左右 5% は暗くぼけた背景（全体で見た・縁でない）",
}


# `apply()` が cuts.ss に差し込む名の全部（上の値＝ss から移したもの）。ここに無い名は ss に置かない
#   （`AXI`・`QG`・`QB`・`REC_DOCS`・`AXIS_DOCS`・`PEOPLE_*`・`QDOC`・`QWHO`・`SAT`・`GEO`・`NEEDS_MASK`・`SLIDE_*`・`ILLU_*` などは ss に空の器が残る＝見本の値〈23本目の項目つき〉を差し込む。
#   `AX_PM23` ほかの `AX_*` は本番の ss に無い名＝restore で消す）。23本目は関数を ss へ足した（`mvz()`＝全画面の写真の窓を2つ書く）が、それは型の道具＝本番に残した。
#   `sat`・`ax`・`qb`・`P`・`page`・`vid`・`head`・`tailv`・`mv`・`MV_Z`・`MV_IN`・`check_frame_only(spec, use)`・`check_card_mix`・`src`・`SAT_CREDIT` も型。
#   `SAT_CREDIT`（Google の帰属の決まり文句）は上の SAT を組むための名＝ss には差し込まない
SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "AX_PM23", "AX_P23", "AX_Y23", "AX_J23", "QG", "QB",
            "PEOPLE_ORDER", "PEOPLE_SETS", "PEOPLE_REC", "PEOPLE_CUTS", "QDOC", "QWHO", "SAT", "GEO", "NEEDS_MASK", "SLIDE_MOUNT", "SLIDE_NOT_MOUNT")


# ══════════════════════════════════════════════════════════
#  門番の記録の表（23本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════════
# 以下の表は、門番4本の本番の置き場にあった23本目の値を1文字も変えずに写したもの（GATES が門番ごとにまとめる）

# ── check_axis ──
# ✅ 2026-10-18（23本目 ⑤b-3）：23本目の値（第2章の時間の帯 c319）。頁＝cuts/ss.REC_DOCS（国会 三豊特別委員会 第6号の会議録の PDF の頁＝印刷の頁）。
#    原文＝`ref/ep10/src/assembly_sampoong_tokui_no6_19950912_id19114.txt`（git の外）：検察の報告 p.47「14:00 : 대책회의 개최」「구조사 … 도착(15:10)」
#      「16:00 : 대책회의 계속」「17:30 : 시설부 차장 … 야간보강작업 준비 착수」・p.52（別紙2）「16:40경 대책회의에서」・ソウル市 p.34「17:55경」・瑞草区 p.42「17:55경」
#      （「경」＝ごろ＝REC_APPROX）。国会の報告 p.30 も「14:00～16:00 … 대책회의를 개최」「16:00～17:52 … 대책회의를 속개」と同じ時刻
REC_AXIS = {
    "14:00": {"K6-検 p47", "K6-R p30"}, "15:10": {"K6-検 p47", "K6-検 p52"}, "16:00": {"K6-検 p47", "K6-R p30"},
    "16:40": {"K6-検 p52"}, "17:30": {"K6-検 p47"}, "17:55": {"K6-市 p34", "K6-区 p42"},
    # 🆕 2026-10-18（23本目 ⑤b-4）：c604 許可の年表。国会の報告 p.30「아파트지구로지정:1976.8.29.」・区 p.43「76.8.29.」・検察 p.48「76.8.29.」／
    #   1986 は記録で月日が割れる（4月24日＝国会・検察／5月＝市 p.35）＝年だけ／1987-07＝国会 p.30・市 p.35・検察 p.48「87.7.21.」（区 p.43 は 87.7.18＝月まで）
    "1976-08-29": {"K6-R p30", "K6-区 p43", "K6-検 p48"}, "1986": {"K6-R p30", "K6-市 p35", "K6-検 p48"}, "1987-07": {"K6-R p30", "K6-市 p35", "K6-検 p48"},
    # 🆕 2026-10-19（23本目 ⑤b-5）：ca02 竣工から崩れた日まで。国会の報告 p.31「사용검사:1990.7.27.서초구청」・市 p.35「90.7.27.사용검사」・区 p.44「90.7.27.:건축물시설준공」・
    #   検察 p.46「90.7.27.준공검사」（月まで＝c616 の語り「翌年の7月」）／国会の報告 p.4「1995.6.29.발생한」
    "1990-07": {"K6-R p31", "K6-市 p35", "K6-区 p44", "K6-検 p46"}, "1995-06-29": {"K6-R p4"},
    # 🆕 2026-10-19（23本目 ⑤b-6）：cc16 判決の年表。検察の報告 p.48「기소일자:7.26.」・高96「원심판결 서울지방법원 1995.12.27.선고」「서울고등법원 1996.5.10.선고 96노118판결」
    #   （頁の無い資料＝「高96 p1」）。🔴 1996-08-23（大法院＝cc17）・1995-07-18（災難管理法＝cc22）・1995-12-30（5つの法律＝cc23）は次のカットの語り＝表に入れない
    "1995-07-26": {"K6-検 p48"}, "1995-12-27": {"高96 p1"}, "1996-05-10": {"高96 p1"},
}
LANES_OK = set()
REC_APPROX = {"16:40", "17:55"}      # 記録が about の時刻（「ごろ」が要る）
REC_LANE = {}             # 2段の帯の記録ごとの段（値 → 段の名）＝23本目は2段の帯を使わなかった＝空
REC_WRONG = {}            # 23本目は×の印を使わなかった＝空（21本目 ⑤b-6 で足した表＝fixture_ep21 の GATES が値を持つ）
# 🆕 2026-10-14（22本目 ⑤b-3b）：**役の色**（記憶 feedback-jiko-diagrams-more-color・`jiko_style.ROLE`）。型の側の色（AXI の c）と別に、門番の側で
#    「その値はだれの動きか」を持つ＝描いた部品の色の値が役の色の値と同じか照らす（[[feedback-settings-may-not-reach-the-picture]]＝設定でなく描いた値）。
#    REC_ROLE＝1段の帯（clock）の値 → 役（ROLE の名か意味の色の名）・帯 span は「始め〜終わり」の鍵。LANE_ROLE＝2段の帯の段 → 役（段の点は段の調べの色）・
#    TIER_ALERT＝2段の帯で赤（壊れた）にしてよい値。表に無い値は本番（main）で止める（selftest の前の回の見本は表を持たない＝照らさない）
# ✅ 2026-10-18（23本目 ⑤b-3）：会議と準備＝会社（三豊）・着いた／報告した＝構造技術者・崩れはじめ＝赤（だれの動きでもない＝壊れる）
REC_ROLE = {"14:00": "company", "15:10": "engineer", "16:00": "company", "16:40": "engineer", "17:30": "company", "17:55": "ALERT",
            # 🆕 ⑤b-4（c604）：1976・1986 は記録で役所が割れる（建設部／ソウル市）＝中立の線の色・1987年7月はソウル市の承認＝市の紫
            "1976-08-29": "LINE", "1986": "LINE", "1987-07": "city",
            # 🆕 ⑤b-5（ca02）：竣工＝中立の線の色・崩れた日＝赤・そのあいだの合図の区間＝黄（数でなく「記録がある区間」の印＝だれの動きでもない）
            "1990-07": "LINE", "1995-06-29": "ALERT", "1990-07〜1995-06-29": "AMBER",
            # 🆕 ⑤b-6（cc16）：起訴＝検察・判決＝裁判所＝国の青
            "1995-07-26": "state", "1995-12-27": "state", "1996-05-10": "state"}
LANE_ROLE = {}
TIER_ALERT = set()
# 並び order の基準の時刻（分）。🔴 23本目は時計の時刻を含む並び（"1:16:27" の形）を使わなかった＝空（None）。本番も None
ORDER_REF_MIN = None

# ── check_qty ──
# ✅ 2026-10-18（23本目 ⑤b-4）：23本目の値を入れた（頁は cuts/ss.REC_DOCS の頁の無い資料＝「大96 p1」）。
#    c804 判決 大96 理由2.가「적재하중이240㎏/㎡로설계」「등분포하중이400㎏/㎡인냉각탑」。役の色（REC_QTY_ROLE）・人の形（REC_PEOPLE ほか）は23本目は使わなかった＝空
REC_QTY = {          # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
    # 🆕 2026-10-18（23本目 ⑤b-4）：c804 判決 大96 理由2.가「적재하중이240㎏/㎡로설계」「등분포하중이400㎏/㎡인냉각탑」（頁の無い資料＝「大96 p1」）
    ("床にかかる重さ（キログラム／平方メートル）", "屋上の床の前提"): (240.0, {"大96 p1"}),
    ("床にかかる重さ（キログラム／平方メートル）", "冷却塔"): (400.0, {"大96 p1"}),
}
REC_QTY_ROLE = {}     # (群の項目名, 行の名) → 役（jiko_style.ROLE の名）＝描いた棒の色の値が役の色か
REC_PEOPLE = {}       # 人の形（14本目 c204〜c206・22本目 c303 だけの例外＝§C-1 #59）＝23本目は使わなかった
REC_PEOPLE_PAGES = set()
REC_PEOPLE_ROLE = {}  # 凡例の名 → 役の色
PEOPLE_CUTS_QTY = set()   # 🔴 ルール §C-1 #59（型の側の ss.PEOPLE_CUTS とは別に持つ）＝23本目は人の形を使わなかった＝空
#                           ⚠️ check_qty の表の名は `PEOPLE_CUTS`（上の ss の `PEOPLE_CUTS`〈タプル〉と同じ名＝この見本の中で区別するため `_QTY` を付けた。GATES で戻す）

# ── check_mech ──
# 🆕 23本目 ⑤b-3（2026-10-18）：模式図（m23＝`tools/mech23.py`・章をまたぐ型4つ＋第1〜3章の10の見え方）。⑤b-4〜⑤b-6 で見え方と記録の値を足した
#   記録の値は門番の側（§5b-88＝描く側の表 mech23.SC_USE・CLOSED・SINK_PTS・GRID・CK_SET・FORM・FLOW・TB_ROWS・BK_* を書き換えると鳴る）。
#   原文＝国会 三豊特別委員会 第6号の会議録（`ref/ep10/src/assembly_sampoong_tokui_no6_19950912_id19114.txt`＝git の外・頁＝PDF の頁＝印刷の頁）・
#   大法院の判決 96도1231（`ref/ep10/src/lawgokr_prec114109_96do1231.txt`）。引いた原文：
#     ソウル市 p.34「지하4층 지상5층」・断面図の札（A동 5층「식당가」・1〜4층「매장」／B동 4〜5층「운동시설 동」・1〜3층「판매시설」／지하1층「식품」「수퍼마켓」／
#       지하2〜3층「주차장」／지하4층「기계실」）・「건물 2개동 중 북측 A동」・p.37「A동 북측 잔여벽체」・p.39 現場図（북측・남측 잔여벽체）・p.35「18:00」「18:50경」
#     国会の報告 p.28「옥상과 5층 슬래브가 1차 붕괴되고 … 하위층이 차례로 순식간에 연쇄붕괴」・p.30「08:00～10:00 … A동 5층」「10:00～12:00」「12:00～14:00」「17:52」
#     検察の報告 p.45「붕괴부분 : … A동 및 중앙연결통로」「17:57경」・p.47「5층 식당 대부분, 신용판매부, 4층 귀금속 코너 영업 중단」「옥상 바닥 4곳」「14:00」「(15:10)」
#       「16:00」「17:30」・p.52（別紙2）「삼풍백화점의 ‘무량판공법’으로 계산 설계한 건축구조기술사로서」「16:40경」
#     瑞草区の報告 p.42「17:55경」・p.45「1차(해빙기 안전대비) : 95.3.13.～3.30.」「2차(테러, 가스폭발 대비) : 95.6.12.～6.30.」「소방, 전기 및 승강기 안전관리자 상근」
#     判決 理由1「5열 E행, 5열 F행 둘레를 따라 전단파괴」（同じ理由に「4열 E행」「4열 G행」）
#   ⚠️ 名前は書かない（原文の人名・店の名は表に入れない）
REC_M23 = dict(
    floors=dict(above=5, below=4),
    use=dict(a=(((5, 5), "食堂街"), ((1, 4), "売り場")), b=(((4, 5), "運動の施設"), ((1, 3), "売り場")),
             under=(((-1, -1), "食品の売り場"), ((-2, -2), "駐車場"), ((-3, -3), "駐車場"), ((-4, -4), "機械室"))),
    first_fall=(0, 1),                 # 屋上（0）と5階（1）の床の板が先
    closed=dict(a5=("大部分", 0.5, 1.0), a4=("一部", 0.0, 0.5)),     # 帯の中の閉めた割合の幅（大部分＝半分より多い・貴金属の売り場＝一部）
    hi_a5=(("a", 5),),
    sink=4,
    b1_chk=("消防の受け持ち", "電気の受け持ち", "昇降機の受け持ち"),
    grid=dict(cols={"4", "5"}, rows={"E", "F", "G"}, hit={("5", "E"), ("5", "F")}),
    bunko=dict(sink_cm=15.0, book_mm=(105.0, 148.0)),
    meeting=("社長", "会長", "役員たち"),
    form=dict(title="별지 2", head="유지·관리 관련 피의자 및 범죄사항 요지", cols=("성명", "직책", "범죄사항"),
              quote="삼풍백화점의 ‘무량판공법’으로 계산 설계한 건축구조기술사로서", page=52),
    flow=dict(head=("国会の報告の判断", "state"), boxes=(("崩れるのを甘く見た", "company"), ("経営の事情も考えた", "company"),
                                                   ("営業のあとに直すだけと決めた", "company")), ng=("惨事",)),
    table=dict(rows=(((3, 13), (3, 30)), ((6, 12), (6, 30))), day=(6, 29), why="テロとガス爆発への備え"),
    clocks=dict(fall=(("17:52", "", "state"), ("17:55", "ごろ", "city"), ("17:57", "ごろ", "state")),
                after=(("17:55", "ごろ", "ALERT"), ("18:00", "", "city"), ("18:50", "ごろ", "city"))),
    clock={"8:00", "10:00", "12:00", "14:00", "15:10", "16:00", "16:40", "17:30", "17:52", "17:55", "17:57", "18:00", "18:50"},
)
# 🆕 2026-10-18（23本目 ⑤b-4）：第4〜7章の記録（描く側の表 mech23.WL・CAL_SET・CARDS・NUMS・SH・RANK・CX_COLS・SP_LONG_M・PQ・VS_SET・USE5・HI["temp"]・AREA・
#   DP_MISS・CT・TW3・LD を書き換えると鳴る）。引いた原文（q23 で頁を当てた）：
#     ソウル市 p.37「95.7.4.북측잔여벽체와이어로프10개설치」「95.7.12.북측벽체추가보강(H-BEAM2개소및와이어로프8개)」「7.19일현재총932명구조」「7.19.현재459명발굴」・
#       p.39「7.19일현재380명이76개병원에분산입원중」「사법연수원에 … 유실물관리센터설치운영」「총1,087건을접수하여301건을확인후인계」・p.35「89.12.1.백화점개설」
#     国会の報告 p.29「구조계산서에는800㎜에16개로되어있으나설계도면상에는600㎜에8개」「주철근이정상위치(표면에서50㎜임)」「허가도서상으로는연면적71,136㎡ …
#       시공도서상으로는2,069㎡가늘어난73,205㎡」「허가도서상으로는롤러스케이트장 … 시공도서상으로는식당가」
#     瑞草区 p.43「73,205㎡중55,257㎡(지하1～지상3층)」・検察 p.46「89.7.∼89.12.옥상의냉각탑이전」
#     判決 大96「냉각탑3개」「각28.7t(물의하중까지포함하면45.5t)」「적재하중이240㎏/㎡」「등분포하중이400㎏/㎡」「20여회에걸쳐서수시로구조계산을추가」「간격(Span)이 … 10.8m」
#       「5층4열E행부위에해당하는기둥상부에시공하도록되어있던15㎝두께의지판시공이누락」「표면상으로만운동시설로사용할것처럼가장」
#     白書 p.643（7月9日・230時間）・p.69（7位・2位）・p.90（4台）＝頁の画像（② で読んだ・sources.md §7）
REC_M23.update(
    wall=dict(hbeam=2),
    cal=dict(rescue=dict(fall=(1995, 6, 29), mark=(1995, 7, 9), last=(1995, 7, 15)), move89=dict(band=((1989, 7), (1989, 12)), open=(1989, 12, 1))),
    cards=dict(head="7月19日の時点", rows=(("救助された人", "932人"), ("入院（76の病院）", "380人"), ("見つかった遺体", "459人"))),
    nums=dict(place="司法研修院", boxes=(("受け付け", "1,087件"), ("確かめて引き渡し", "301件"))),
    sheets=(20, 29),                     # 「20여회」＝20より多く30より少ない
    rank=(("売り上げ", 7), ("売り場の大きさ", 2)),
    colx=(("計算書", 80.0, 16), ("図面", 60.0, 8)), colx_cover_cm=5.0,
    spans_m=10.8,
    persq=dict(n=(6, 4), kg=(400.0, 240.0), per=65.0, tol=0.10),
    vs=dict(count=(("判決", "3基"), ("白書", "4台")), rumor_rec=(("判決", "1基28.7トン"), ("検察の記録", "移したのは1989年"))),
    use5=dict(permit="運動の施設", actual="食堂街"),
    temp=frozenset({("a", 1), ("a", 2), ("a", 3), ("b", 1), ("b", 2), ("b", 3), ("u", -1)}),
    area=dict(permit=71136, plan=73205, add=2069),
    dp_miss={("4", "E")},
    towers=3,
)
# 🆕 2026-10-19（23本目 ⑤b-5）：第8〜9章の記録（描く側の表 mech23.LISTS・OVER_KG・DU_CUT・JT_CM・HK_CM・SK_ITEMS・SK_COL_MM・HI["f4"]・P3・RL_LINE・RL_PT・
#   ITEMS・sc_walls・TG を書き換えると鳴る）。引いた原文（q23 で頁を当てた）：
#     国会の報告 p.29「칸막이 및 대형냉장고·주방기기와 공용부분에 화단 및 분수대 등」「옥상바닥을 받치는 북측 코아 내력벽을 수평방향으로 절단(벽체길이 160㎝ 중 98㎝ 절단)」
#       「슬래브 속의 두 가닥 철근을 내력벽 속으로 각각 64㎝·40㎝씩 ‘ㄱ’자 형태로 꺾어 넣고 끝부분은 갈고리 모양으로 처리(HOOK장치)하여야 하는데도 ‘ㅣ’자형으로
#       갈고리장치 없이 짧게 시공」・p.30「4층 조명코너에서 건물 진동으로 조명등이 추락」（棟は書いていない）
#     判決 大96「예정된 하중보다 360㎏/㎡ 이상의 과하중」「정착길이는 철근지름의 40배인 64㎝를 확보하여야 함에도 15-18㎝ 정도로 짧게 정착」「대리석 및 화강석의
#       마감재공사, 15㎝ 두께의 주방 바닥콘크리트공사, 벽돌을 사용한 칸막이 벽체공사, 온돌공사, 대형냉장고 등」・「긴 10.8m」
#     ソウル市 p.37「A동 북측 잔여벽체」「A동 남측 벽체」・検察 p.50「층수가 16층 이상이거나 기둥과 기둥 사이 거리가 30m 이상」・p.45「지상 5층」
#     瑞草区 p.45「소방안전관리 … 전기안전관리 … 가스안전관리 … 건축물안전관리 : 승강기, 축대·난간 관리, 노후건물·간판 관리상태」
#     白書 p.89（大きな冷蔵庫・れんがの壁・石の庭）＝頁の画像（② で読んだ・台本の出典の欄）
REC_M23.update(
    lists=(("国会の報告", "state", ("間仕切り", "大きな冷蔵庫", "厨房の機器", "花壇と噴水")), ("白書", "city", ("大きな冷蔵庫", "れんがの壁", "石の庭"))),
    over_kg=360.0,
    duct=(98.0, 160.0),
    joint=dict(need=64.0, got=(15.0, 18.0)),
    hook=(64.0, 40.0),
    stack=frozenset({"冷蔵庫", "れんがの壁", "石の庭", "大理石", "厨房の床", "オンドル"}),
    f4=frozenset({("a", 4), ("b", 4)}),
    three=("4階", "5階", "屋上"),
    rule=dict(floors=16, span=30.0, pt=(10.8, 5)),
    items=("消防", "電気", "ガス", "エレベーター", "看板"),
)
# 🆕 2026-10-19（23本目 ⑤b-6）：第10〜11章・終章の記録（描く側の表 mech23.DESK・TALLY・TOLL・KOSEKI・FINAL・AGES・MOST・PEN・HAUL・PAY・Q3・FORMS3・ACTS・CHAIR・
#   FAKE・BRIBE・CARD_SETS・SHELF・STAGES・CHAIN・GAP・CAUSES・OPEN・BLOCKS・STOP を書き換えると鳴る）。引いた原文（scratchpad の q23 で頁を当てた）：
#     国会の報告 p.32「실종자신고의 접수를 서울특별시사고대책본부와 서초구청 실종신고가족안내소로 이분화 … 하루 만에 207명에서 410명으로 수정 발표」・
#       「유골과 유품의 일부가 건물잔해와 함께 난지도와 염곡동의 집하장 등으로 실려감」（場所の名は画面に出さない）・「영업종료 후 보수·보강공사만 하기로 결정」・
#       p.28「설계·시공·감리 및 유지·관리상의 결함과 행정관청의 감독부실 등이 복합적 요인으로」
#     ソウル市の報告 95.8.9（会議録 p.53 の下の段）「(95.8.8. 24:00 현재) … 1,566 1,485 … 81」
#     国政監査（内務委 1995-10-10）p.24「사망자 501명(사망확인 471명, 사망인정 30명)」「잔재검색은 8.14 최종완료 … 골편 등 142점과 유품 3,419점」
#     検察の報告 p.48「※추가죄명 - 뇌물공여 : 회장 … 사장 …」「기소일자:7.26.」・p.49「설계도면 등의 보존연한이 5년에 불과 … 구청에서만 설계도면 보존」・
#       p.50「준공후 일정기간내에 손괴가 발생한 경우 5년이하의 징역」・p.51〜53 の別紙1〜3 の題・p.52 会長の欄・p.53 の15人の額（300・1,300・1,200・300・200・400・
#       1,000・1,300・1,050・1,400・150・100・100・180・100 万ウォン＝4〜6行目が市の職員）
#     判決 大96 判示事項[1]「건축계획의 수립, 건축설계, 건축공사공정, 건물 완공 후의 유지관리 … 각 단계별 관련자들을 … 공동정범으로 처단」・[5]「허위의 복명서」
#     判決 大99「상당인과관계가 있다고 인정할 수는 없다」「서울고등법원에 환송」・高96「1995.12.27.선고」「1996.5.10.선고 96노118」「피고인B을 징역 7년6월」
#     白書 p.92・p.93（502・937・1948年の建国・1970年の沈没 326人・11月29日の戸籍の30人・年代の表〈10-19 に原寸で読んだ〉・補償）＝頁の画像
REC_M23.update(
    desk=dict(two=(("市の事故対策本部", "city"), ("区の家族の案内所", "ward")), fix=(207, 410)),
    tally=dict(head="8月8日の時点", total=1566, done=1485, left=81),
    toll=dict(total=501, parts=(471, 30), role="city"),
    koseki=dict(n=30, day=(11, 29)),
    final=dict(cards=(502, 937), koseki=30, oct=471),
    ages=(("0〜10歳", 14), ("11〜20歳", 71), ("21〜30歳", 258), ("31〜40歳", 80), ("41〜50歳", 52), ("51〜60歳", 21), ("60歳以上", 6)), ages_sum=502,
    most=(("三豊百貨店", "1995年", 502), ("船の沈没", "1970年", 326)),
    pen=(("事故の前", 0.0, 5.0, "5年以下の懲役"), ("1995年12月30日から", 3.0, None, "無期か3年以上の懲役")),   # 「무기 또는 3년이상의 징역」（echo＝「または」を「か」に）
    haul=dict(found=(("骨片など", 142), ("遺品", 3419)), day=(8, 14), ng=("난지도", "염곡동", "蘭芝島", "難芝島", "廉谷洞", "ナンジド")),
    pay=dict(head="1996年6月14日", rows=(("亡くなった人", "464人分", "1,758億ウォン"), ("けがをした人", "709人", "1,003億ウォン")),
             avg="3億8千万ウォン", yen="およそ240億円"),
    q3=("なぜ店は開いたままだったのか", "なぜ建物は崩れたのか", "誰なら止められたのか"),
    forms3=dict(add="추가죄명 - 뇌물공여", roles=("회장", "사장"),
                sheets=(("별지 1", "설계·시공 및 감리 관련 피의자 및 영장범죄사실 요지", 51), ("별지 2", "유지·관리 관련 피의자 및 범죄사항 요지", 52),
                        ("별지 3", "수뢰 공무원 범죄사실 요지", 53)), add_page=48),
    acts=dict(cards=("ドロップパネルを薄く", "上の鉄筋を沈めた", "冷却塔を計算に入れず", "耐力壁を切った"), ch=("第6章", "第6章", "第7章", "第8章")),
    chair=dict(head=("2つ目の表・会長の欄", "company"), cards=("梁の無い作りと知っていた", "ひびの報告を受けた", "逃がさず放っておいた"), ng=("14:30",)),
    fake=("city",),
    bribe=dict(rumor=1300, ward=(12, 8180), city=(3, 900),
               amounts=(300, 1300, 1200, 300, 200, 400, 1000, 1300, 1050, 1400, 150, 100, 100, 180, 100), city_rows=(3, 4, 5)),
    cards_bribe=(("1人あたり", "100万〜1,400万ウォン"), ("15人の合計", "9,080万ウォン"), ("1995年のレートで", "およそ1,100万円")),
    cards_art=dict(head=("2026年6月", "city"), rows=(("ソウル市が選んだ", "新しい造形の作品"),)),
    shelf=dict(years=5, r_role="ward"),
    stages=("計画", "設計", "工事", "建ったあとの管理"),
    gap=dict(l=("区の職員の違反", "ward"), r=("崩壊", "ALERT")),
    causes=dict(cards=("設計", "工事", "監理", "建ったあとの管理"), gov="役所の監督", marks=("欠陥", "不備")),
    blocks=dict(low=("細い柱", "薄い板", "沈んだ鉄筋"), up=("冷却塔の重さ", "食堂街の重さ"), wall="重さを支える壁"),
    stop=dict(cards=("設計", "工事", "監理", "建ったあとの管理", "役所の監督"), marks=("欠陥", "欠陥", "欠陥", "欠陥", "不備")),
    open=dict(sign="営業のあとに直す", who="客と従業員"),
)

# ── check_sat ──
# 🆕 2026-10-18（23本目 ⑤b-4）：囲み（area）の面積の記録＝{カット: (平方メートル, 出典)}。境の線が記録に無く「面積が同じ円」で描くカットだけ
#    （記録の値は門番の側＝§5b-88。描く側は `satmap.r_of_area` で半径を出す）。囲みの面積が記録から 1% より外れたら鳴る
REC_SAT_AREA = {"c511": (67100, "K6-市 p40（`부지와 그 주변지역을 포함한 67,100㎡`）")}

# ── check_boxes・check_illu・check_photo_edge ──
# 23本目は check_boxes・check_illu に足した値が無い（git の `b800dbdb` までの23本目の作業で両ファイルは22本目〈`adbe2d5`〉から変わっていない）。
# check_photo_edge の名簿は ss の SLIDE_MOUNT・SLIDE_NOT_MOUNT（上＝SS_NAMES）＝門番の側に表を持たない。GATES に載せない。


GATES = {
    # 23本目は時計の時刻を含む並び（order）も×の印も2段の帯（tiers）も使わなかった＝ORDER_REF_MIN は None・REC_WRONG・REC_LANE・LANE_ROLE は空・LANES_OK・TIER_ALERT は空の集合。
    # 1段の帯・年表の値（REC_AXIS・REC_APPROX）と役の色（REC_ROLE）が入る
    "check_axis": dict(REC_AXIS=REC_AXIS, LANES_OK=LANES_OK, REC_APPROX=REC_APPROX, REC_LANE=REC_LANE, REC_WRONG=REC_WRONG,
                       REC_ROLE=REC_ROLE, LANE_ROLE=LANE_ROLE, TIER_ALERT=TIER_ALERT, ORDER_REF_MIN=ORDER_REF_MIN),
    "check_qty": dict(REC_QTY=REC_QTY, REC_QTY_ROLE=REC_QTY_ROLE, REC_PEOPLE=REC_PEOPLE, REC_PEOPLE_PAGES=REC_PEOPLE_PAGES,
                      REC_PEOPLE_ROLE=REC_PEOPLE_ROLE, PEOPLE_CUTS=PEOPLE_CUTS_QTY),
    "check_mech": dict(REC_M23=REC_M23),
    "check_sat": dict(REC_SAT_AREA=REC_SAT_AREA),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・（gate を渡せば）その門番の記録の表を23本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss は触らない）＝14〜22本目の見本 `fixture_ep14`・`fixture_ep15`・`fixture_ep16`・`fixture_ep18`〜`fixture_ep22` と
    重ねるとき（check_mech の selftest は14本目の検算と15〜23本目の検算を1つの処理で回す＝先に14本目を全部差し込み、15〜23本目は表だけ足す）。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が23本目の表で
       17本目の画を測る）。apply の前に**無かった名**（ss の AX_* …／門番の表）も覚えて、restore で**消す**
       ＝selftest のあとに23本目の名が本番へ残らない（fixture_ep15〜ep22 と同じ作り）。
    ⚠️ fixture_ep22 と同じく、`titan_fig.GEO` は触らない（23本目の地点は無い・場所の表は ss の `GEO`＝SS_NAMES で差し込む）"""
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


CUTS_SHA = "b800dbdb"      # 23本目の章ファイルが最後に live だった版（章ファイルを17本目の空の器に替える前＝git の `b800dbdb`）
_CUTS23 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def _footage23():
    """23本目の映像の台帳 `CLIPS`（`ref/ep23/clips.json`）と使う区間 `USE`（git の CUTS_SHA の `tools/footage.py` の `USE = {…}`）を返す。
    🔴 23本目の章ファイルは `ss.vid`・`ss.head`・`ss.tailv` で `footage.CLIPS`・`footage.USE` を引く（フリー素材のカットは台帳の `"stock": true` を見て、ひかえの静止画の名を
    `ep23/stock/fb_<cid>.jpg` に決める）。本番の footage は17本目の表になった（`USE` は空・`CLIPS` は `ref/ep17/clips.json`）＝そのままだと 23本目のフリー素材のカットは
    `ref/ep23/fb_<cid>.jpg`（無い名）を開きに行って章ファイルが読み込みで落ちる。→ 章ファイルを読む間だけ、この表を footage に差す（`cuts_ep23` が戻す）。
    footage.py の `USE` は値だけの代入（`dict(clip=…)` の並び）＝その1文だけを取り出して評価する（footage.py 全体は import しない）"""
    import ast
    import json
    import subprocess
    p = subprocess.run(["git", "-C", str(ROOT), "show", f"{CUTS_SHA}:tools/footage.py"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 23本目の映像の使う区間を git の {CUTS_SHA} の tools/footage.py から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    ns = {}
    for node in ast.parse(p.stdout.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "USE" for t in node.targets):
            exec(compile(ast.Module([node], []), f"footage_{CUTS_SHA}", "exec"), ns)
    use = ns.get("USE")
    clips_file = REF / "clips.json"
    if not use or not clips_file.exists():
        raise RuntimeError(f"🔴 23本目の映像の表が読めていない（USE {len(use or {})}・{clips_file} {'ある' if clips_file.exists() else '無い'}）")
    return json.loads(clips_file.read_text(encoding="utf-8")), use


def cuts_ep23():
    """23本目の章ファイル（git の CUTS_SHA の `tools/cuts/`）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。
    読む間だけ `footage.CLIPS`・`footage.USE` を23本目の表にする（`_footage23`＝本番の footage は17本目の表）。読み終えたら戻す。"""
    if _CUTS23:
        return _CUTS23[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    import footage as _FO
    clips23, use23 = _footage23()
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 23本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts23_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep23 の写真・頁を読む＝根の下の作業場所の
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
        keep_fo = (_FO.CLIPS, _FO.USE)
        _FO.CLIPS, _FO.USE = clips23, use23          # 章ファイルを読む間だけ（finally で戻す）
        try:
            old = importlib.import_module("cuts")
            got = (dict(old.PLAN), dict(old.SPEC))
        finally:
            _FO.CLIPS, _FO.USE = keep_fo
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
        raise RuntimeError(f"🔴 23本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}）")
    _CUTS23.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を23本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で17本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep23()
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
        if s.get("cuts") is not None:          # apply_cuts() の分＝17本目の PLAN・SPEC へ戻す
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
