# -*- coding: utf-8 -*-
"""18本目（スレッシャー号のリメイク・1963-04-10・米海軍の潜水艦の事故）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-06（19本目 サーフサイドのリメイク ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `2d627a2` と同じ）
  ・`cuts/ss.py` の後半＝案C の出典の表（REC_DOCS）・時計と秒の札・描いてよい数・想定の札・壊れる物のカット・潜水艦の時刻（ILLU_SUB_*）・
    音の輪（ILLU_BOOM_CUTS）・混ざりのつなぎ待ち（ILLU_MIX_*）・軸の型（TV／TM・AX_*・AXI の項目）・棒（QG・QB）・書類の再現図（FORM_*＝欄の値は
    原文の英語）・流れ図（FL_*・FLP・`fl()`）・並べ図（CAUSE）・決め所の出どころの札（QDOC・QWHO・`qrows()`）（18本目 ⑤b-2〜⑤b-8）
  ・`titan_fig.GEO` の18本目の地点＝**無い**（18本目は地点の鍵 `thresher_` を足さなかった＝`b11797a` の GEO は `23c5094` と同じ）。
    GEO は空の表のまま持つ（15・16本目の見本と同じ作り＝apply/restore の対称）
  ・門番の記録の表（check_axis・check_qty・check_boxes・check_mech・check_illu）
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を18本目の実物でも確かめている＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は19本目の空の器にした
  （fixture_ep14・fixture_ep15・fixture_ep16 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep18
      fixture_ep18.apply(sys.modules[__name__])   # その処理の中だけ ss・GEO・この門番の記録の表が18本目になる
      try: …（検算）
      finally: fixture_ep18.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14・15・16本目の見本と重ねるとき（check_mech は14本目の検算と15・16本目の検算を1つの処理で回す）は
      fixture_ep18.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss・GEO は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと19本目以降の画に18本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ 見本の頁の原文 `ref/ep18/src/ep18_pages.txt` は git の外（本線の作業ツリーにだけある）＝無いときは頁の照合を飛ばす
     （check_illu の `_pages()` が None を返す）。
  ⚠️ 18本目の selftest のうち `check_illu.selftest_ep18`・`selftest_ep18_sbcd` は、18本目の章ファイルの SPEC（`cuts.SPEC["c101"]` ほか）を
     読む＝章ファイルが19本目の空の器になった本線では KeyError で落ちていた（見本の値ではなく、読む先の SPEC が無いため）。
     ✅ 2026-10-06（19本目 チャット6）：`apply_cuts()` を足した＝18本目の章ファイルを git の `CUTS_SHA`（`b11797a`）から取り出して読み、
     `cuts.PLAN`・`cuts.SPEC` の中身をその処理の中だけ18本目に入れ替える（`restore()` で19本目へ戻す・LIFO）。git が無い所では止める
     （黙って飛ばすと「検算が通った」と嘘になる＝fail closed）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep18/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は18本目の道を持つ。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝18本目 1.66）は見本に入れない（16本目の見本も入れていない）＝本番の ss は18本目の値のまま残し、
     19本目の束（⑤b-7）で取り直す。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep18"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 18本目 ⑤b-2〜⑤b-3
# ══════════════════════════════════════════════════════
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


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：軸の型（`tools/axis.py`・門番 `check_axis`）── 18本目 ⑤b-5（年表・時間の帯・2段の帯）
# ══════════════════════════════════════════════════════
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
AXI = {}

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


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：量の型（棒）と箱の型（流れ図・書類の再現図・並べ図）・決め所の出どころの札── 18本目 ⑤b-6a〜⑤b-8
# ══════════════════════════════════════════════════════
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
    # 🆕 ⑤b-8：c402 海の音の監視の仕組み（PLAN は地図＝場所は描かない模式 → 流れ図＝映像方針 §25・ルール §5b-116①）。V1 p.277（分析官の
    #   証言「analysis of targets which are contacted by passive means by the hydrophone arrays at the fifteen monitoring stations within the
    #   Oceanographic Systems Atlantic」「Analysis Officer for Commander Oceanographic Systems Atlantic in Norfolk」）・認定18（R08 p.185
    #   「Commander Oceanographic Systems Atlantic obtained information that …」）
    "m_arr": dict(k="role", id="m_arr", t="聴音機の列", y=470, pos=(100, 470), rec="V1 p277"),
    "m_sta": dict(k="role", id="m_sta", t="15の監視所", y=470, pos=(560, 930), rec="V1 p277"),
    "m_ana": dict(k="role", id="m_ana", t="司令部で分析", y=470, pos=(1020, 1390), rec=["V1 p277", "R08 p4185"]),
    "m_inq": dict(k="role", id="m_inq", t="査問会の認定", y=470, pos=(1480, 1820), rec="R08 p4185"),
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
# 🔴 2026-10-04（18本目 ⑤b-1・§0b）：16本目の資料の名の表 QDOC・QWHO と関数 `qrows()` は `tools/fixture_ep16.py` へ移した
#    （値は1つも変えていない＝git の `b044b56`）。18本目で決め所の出どころの札を使うときは、その回の QDOC・QWHO・`qrows()` をここに足す。
#    ⚠️ 教訓は移した注の側にある（札の値は全角12字ぶんで折れる・語の途中で折れない名前にする・決め所の言葉は台本の★の行と1字も違えない
#       ＝fixture_ep16 の QDOC の上）
# 🆕 2026-10-05（18本目 ⑤b-8）：18本目の資料の名（札の「記録」の欄）。名は語りの呼び名と REC_DOCS の画面の名にそろえ、`F.wrap(t, 12)` で
#    折って確かめた（「海軍長官の意見書／（1965年）」「海軍研究所の報告／（1964年）」＝かっこの中で割れない・ほかは1行）。
#    🔴 §0b（次の回は空に）：QDOC・QWHO。頁の欄＝PDF の頁（V1・R08・IR18＝「PDF 196頁」）・印刷の頁（J＝「68頁」）・頁の無い資料は None
#    🔴 査問会の認定・意見の頁は**第8回の公開（R08 p.181〜220 の再録）**で書く＝第1回の写し（V1）の p.44・p.49 は見た目の字が描けて
#       いない頁（台本 §2・映像方針 §9）＝札で指す頁は、視聴者が開いて読める版。証言は第1回（V1）の頁
#    決め所17の原文照合（⑤b-8）＝台本 §2 の英語が通し頁ファイルのその頁に 17/17（a〜z0〜9 にそろえて一致率 1.00）・★の行＝台本 §2 の言葉
#    （17/17）＝scratchpad `quotes18.py`。頁の画像での照合は④（台本 §0-5・17件）
QDOC = {"V1": "査問会の記録（第1回公開）", "R08": "査問会の記録（第8回公開）", "IR18": "海軍長官の意見書（1965年）",
        "J": "議会の公聴会（1963年）", "AP": "AP通信の記事（2021年）", "No.710-64": "国防総省の発表（1964年）",
        "R17書": "海軍研究所の報告（1964年）"}
QWHO = {}
def qrows(doc, page, *extra):
    """決め所の出どころの札の rows＝extra（(欄, 値) の組＝箇所・話した人・日付）＋記録＋著者＋頁。page は画面の頁の字（None＝頁の欄なし）"""
    import jiko_style as J
    rows = [(k, v, J.LINE) for k, v in extra]
    rows.append(("記録", QDOC[doc], J.INK_W))
    if doc in QWHO:
        rows.append(("著者", QWHO[doc], J.LINE))
    if page:
        rows.append(("頁", page, J.TICK))
    return rows


# `apply()` が cuts.ss に差し込む名の全部（上の値と関数＝ss から移したもの）。ここに無い名は ss に置かない
#   （`AXI` は ss に空の `AXI = {}` が残る＝見本の AXI（18本目の項目つき）を差し込む）
SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK",
            "ILLU_COUNTS", "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "TV", "TM", "AX_REL", "AX_INQ", "AX_PSA",
            "AX_MORN", "AX_FIVE", "AX_SKY", "AX_DAY", "AX_WEEK", "AX_PRE", "AX_UT", "AX_APR", "AX_AIR", "AX_CALC", "AX_SAFE",
            "QG", "QB", "_P4", "_P3", "_P2", "FORM_COURT3", "FORM_SHOCK", "FORM_SIB", "FORM_SMED", "FORM_ANDR", "FORM_ORD",
            "FORM_WATSON", "FORM_SPLIT", "FORM_MSG", "FORM_F25", "FORM_SEAWOLF", "FORM_O48", "FORM_F112", "FORM_F111",
            "FORM_F111S", "FORM_CINC", "FORM_BUSHIPS", "FORM_JOB", "FORM_O21", "FORM_RICK", "_P1", "FORM_F46A", "FORM_F46D",
            "FORM_F48", "FORM_BROCK", "FORM_ZUR", "FORM_JACK", "FORM_RICK83", "FORM_O38", "FORM_O39", "FORM_O1", "_O1",
            "FORM_O1A", "FORM_O1B", "FORM_O5", "FORM_O5A", "FORM_O2", "FORM_O49", "FORM_NITZE", "FORM_NITZE2", "FORM_RICK89",
            "FORM_RULE", "FORM_CINC2", "FORM_KORTH1", "FORM_KORTH2", "FORM_CODES", "FORM_AP", "FORM_AP900", "FORM_F17",
            "FORM_RICK122", "FORM_WILK", "FORM_ANDR2", "FORM_O4", "FORM_R20", "FORM_O42", "FORM_CURTZE", "FORM_RAMAGE",
            "FORM_O55A", "FORM_O55B", "FORM_NAVSEA", "FL_EMPTY", "FL_CAPT", "FL_KNEW", "FL_UP", "FLP", "FL_RULE", "FL_DEPTH",
            "FL_SS", "fl", "CAUSE", "QDOC", "QWHO", "qrows", "AXI")


# ══════════════════════════════════════════════════════════
#  titan_fig.GEO から：18本目の地点＝無い
# ══════════════════════════════════════════════════════════
#   18本目は `thresher_` の頭の地点を足さなかった（地図 drift を使わず、案C の SA〜SD と図解・模式図 mech18 に替えた）。
#   `b11797a` の `titan_fig.GEO` は `23c5094`（16本目の値を移した直後）と同じ（差分は模式図 `m18` の関数だけ）
GEO = {}


# ══════════════════════════════════════════════════════════
#  門番の記録の表（18本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════════
# 2段の帯の段の名（check_axis の LANES_OK・REC_LANE が使う＝18本目の第4章「水中電話の声」と「監視の記録」）
_V, _M = "水中電話の声", "監視の記録"

GATES = {
    "check_axis": dict(
        # 🆕 2026-10-04（18本目 ⑤b-5）：18本目の値を入れた＝4月10日の朝・9時9分〜18分の2段の帯・救難艦の5時間・年表・公開の23回・秒の帯。
        #    原文 ref/ep18/src/ep18_pages.txt で当てた（R08＝査問会の記録 第8回公開 p4001〜・IR18・J・D）。2段の帯の段の名は上の `_V`・`_M`
        REC_AXIS={
            # ── 4月10日の朝（c309・c312・c320）。R08 p4185＝認定10〜20・p4212＝意見45
            "7:45": {"R08 p4185"},                  # 認定11「That at 0745R, 10 April 1963, SKYLARK was in the vicinity of Latitude 41-46 North」
            "7:47": {"R08 p4185"},                  # 認定15「That at 0747R, THRESHER reported by underwater telephone that she was starting a deep dive」
            "9:00": {"R08 p4185"},                  # 認定14「That the sea was calm, with a slight swell, at 0900R on 10 April. Wind was from 015 True at seven knots」
            "9:09": {"R08 p4212"},                  # 意見45「It is known with reasonable certainty that at 0909R the THRESHER was at test depth」（V1 p65・IR18 p106 も同文）
            "9:10": {"R08 p4212"},                  # 意見45「At about 0910R a message from THRESHER announced a course change to 090 T from 000 T and gave no indication of any difficulty」
            "9:13": {"R08 p4185", "R08 p4212"},     # 認定16「until about 0913R, when THRESHER reported … "Experiencing minor difficulties"」・意見45「message at 0913R」
            # ── 9時9分〜18分（第4章の2段の帯・c720）。認定18＝監視の記録（Commander Oceanographic Systems Atlantic）
            "9:09.8": {"R08 p4185"},                # 認定18「two disturbances, one extending from 0909.8R to 0911.3R, the other from 0913.5R to 0914R,
            "9:11.3": {"R08 p4185"},                #   which could have been made by the blowing of the ballast tanks」
            "9:13.5": {"R08 p4185"},
            "9:14": {"R08 p4185"},
            "9:11": {"R08 p4185", "R08 p4212"},     # 認定18「main coolant pumps ceased functioning in "FAST mode" of operation at 0911R」・意見45（7.1 minutes between 0911R…）
            "9:18.1": {"R08 p4185", "R08 p4212"},   # 認定18「noise disturbance of the type which could have been made by an implosion emanated from THRESHER at 0918.1R」
            #                                         ・意見45「the actual hull collapse occurred at 0918.1R」（c720 の「押しつぶされる深さ」）
            "9:15": {"R08 p4186"},                  # 認定22c「Asked THRESHER at about 0915R, "Are you in control?" and repeated this query」
            "9:16": {"R08 p4185"},                  # 認定17「at about 0916R, SKYLARK heard a garbled transmission … "... test depth"」
            "9:17": {"R08 p4185", "R08 p4186", "R08 p4187"},   # 認定17「An additional garbled transmission was received about 0917R」・認定24（電文「SINCE 0917R」）・
            #                                         認定29「shortly after 0917R, when efforts to communicate with THRESHER had been unsuccessful, SKYLARK commenced an expanding」
            # ── 救難艦の5時間とワシントン（第5章）。R08 p4186＝認定22〜24・p4187＝認定26〜29。D p9001＝Stierman 1964（付録の国防総省の発表 509-63 も同じ頁）
            "9:40": {"R08 p4186"},                  # 認定23a「At about 0940R, when the Operations Officer had asked the Commanding Officer if he should send such a message」
            "10:40": {"R08 p4186"},                 # 認定22f「At 1040R commenced dropping series of hand grenades」
            "10:45": {"R08 p4186"},                 # 認定23「That at about 1045R, SKYLARK began preparation of a message」・23b
            "12:45": {"R08 p4186"},                 # 認定23d「NBL receipted for the message at 1245R」（23c 無線の不調・alternate frequency）
            "14:35": {"R08 p4187"},                 # 認定26「At 1435R he was advised of THRESHER's status」（大西洋の潜水艦部隊の司令官）
            "15:40": {"D p9001"},                   # 「the Chief of Naval Operations learned at 3:40 p.m. that THRESHER might be in difficulty」・「at about 3:40」
            "20:00": {"D p9001"},                   # 「At 8:00 p.m that night … "overdue and presumed missing."」・NO. 509-63「April 10, 1963, 8:00 p.m.」
            # ── 年表（date）
            "1963-04-10": {"R08 p4185"},            # 認定19「THRESHER was lost … at about 0918R on 10 April 1963」
            "1963-04-11": {"IR18 p2067", "R08 p4188", "R08 p4181", "R08 p4196", "J p8018"},
            #   IR18 p67「The Court met for the first time at 8:25 p.m. on Thursday, 11 April 1963」／認定34（11日 0530R 捜索の指揮が移る＝R08 p188）／
            #   認定2・95（整備の完成の予定日の最後＝11 April）／J p18（ブロケット少将「it was received after the 11th of April」）
            "1963-06-05": {"IR18 p2067", "R08 p4180"},  # IR18 p67「Before the Court closed on 5 June 1963, it heard 179 separate appearances」・R08 p180「The court closed at 0921, 5 June 1963」
            "1962-07-16": {"R08 p4181", "R08 p4195"},   # 認定2「a post shakedown availability which extended from 16 July 1962 to 11 April 1963」・認定92「commenced on 16 July 1962」
            "1963-01-18": {"R08 p4196"},            # 認定95「completion date was successively extended from 18 January to 15 February, to 28 February, to 30 March,
            #                                         to 2 April, and finally to 11 April, because of work added and the under-estimation of the effects」
            "1963-04-09": {"R08 p4181"},            # 認定2「departed Portsmouth Naval Shipyard, on the morning of 9 April 1963」
            "1963-01": {"R08 p4196", "R08 p4203"},  # 認定96「loose condenser foundation bolts in January, 1963」・認定166a/b（艦長・副長 January, 1963）
            "1963-03": {"R08 p4196"},               # 認定96「a misaligned torpedo ejection pump in March, 1963」
            "1962-12": {"R08 p4203"},               # 認定166c「a change of THRESHER's Ship Superintendent in December, 1962」
            "1962-11": {"R08 p4203"},               # 認定166d「a change of THRESHER's Assistant Ship Superintendent in November, 1962」
            "1963-04-12": {"R08 p4187"},            # 認定28「on 12 April 1963」・28b「Rear Admiral Ramage interviewed Lieutenant (jg) Watson and examined the UQC log」
            "1961-05": {"J p8067"},                 # J p67（リッコーヴァー中将）「a … silver-brazed joint in the trim system of the Thresher in May 1961」
            "1962-11-29": {"R08 p4197"},            # 認定104「on 29 November 1962, the Quality Assurance Division … requested decision as to whether lagged joints
            #                                         should be unlagged」・認定107「no further ultrasonic testing … after 29 November 1962」
            "1962-12-04": {"R08 p4197"},            # 認定105「decision was made on 4 December 1962 not to unlag」
            "1963-06-03": {"J p8097"},              # J p97「the Chief of the Bureau of Ships on June 3, 1963, directed the establishment within the Bureau of a
            #                                         submarine safety program」
            "1963-07-08": {"J p8098"},              # J p98「BuShips Instruction 5100.18 of July 8,1963」（語りは「7月には」＝札は年月まで）
            "1964-02-18": {"J p8094"},              # J p94「On February 18, 1964, the Secretary of the Navy established the Submarine Safety Center at Groton」
            # 公開の23回（c108・c907）。台帳＝navy_running_release_inventory.xlsx（B 列の Excel の日付）・棚＝閲覧室 THRESHER RELEASE の更新日
            "2020-09-23": {"台帳"},                 # Interim Release 1（COI Volume 1＝認定・意見・勧告）
            "2022-01-26": {"台帳"},                 # Interim Release 17（台帳の最後）
            "2021-01-27": {"台帳"},                 # Interim Release 5「Sea-Based Airborne Anti-Submarine Warfare」（事故の記録ではない）
            "2021-02-24": {"台帳"},                 # Interim Release 6（同上）
            "2022-03-03": {"棚"},                   # Interim Release 18 の更新日 3/3/2022（台帳に無い）
            "2023-05-02": {"棚"},                   # Interim Release 21・22・23 の更新日 5/2/2023（台帳に無い）
            # ── 秒の帯（c717）。認定51＝R08 p4191
            "0": {"R08 p4191"},                     # 認定51「in event of loss of electrical power … air banks 2, 3 and 4 would automatically be shut off and
            "30": {"R08 p4191"},                    #   air bank #1 would be opened up slowly. It takes thirty seconds to get valves fully open again」
        },
        LANES_OK={_V, _M},
        # 🆕 2026-10-04（18本目 ⑤b-5）：①**記録が about の時刻**（「ごろ」が要る＝札に「ごろ」が無ければ止める・about でない時刻に
        #    「ごろ」を付けても止める）②**2段の帯（tiers）の記録ごとの段**（値 → 段の名＝その値を拾った記録。違う段に置けば止める）。
        #    🔴 §0b：次の回は REC_AXIS・LANES_OK と一緒に空にする（空のあいだ、2段の帯の部品は「段の記録に無い値」で止まる＝fail closed）
        #    9:13 は意見45 が「at 0913R」＝「ごろ」なし（語りも「9時13分」）。9:17 は認定17 が about＝第5章の「9時17分のあと」も「ごろ」
        REC_APPROX={"9:10", "9:15", "9:16", "9:17", "9:40", "10:45", "15:40"},
        REC_LANE={"9:13": _V, "9:15": _V, "9:16": _V, "9:17": _V,
                    "9:09.8": _M, "9:11.3": _M, "9:11": _M, "9:13.5": _M, "9:14": _M, "9:18.1": _M},
    ),
    "check_qty": dict(
        # 🆕 2026-10-04（18本目 ⑤b-6a）：18本目の棒の値を入れた（原文 ref/ep18/src/ep18_pages.txt で当てた＝型の側 ss.QB とは別に持つ）
        #     🆕 2026-10-04（18本目 ⑤b-6a）：第1〜6章の棒（c204・c207・c302・c315・c613・c614・c626）の値と頁を入れた（原文
        #        ref/ep18/src/ep18_pages.txt で当てた＝型の側 ss.QB とは別に持つ）。フィートの記録は門番の側でも ×0.3048 で持つ（語りの「約」の
        #        丸めで描くと鳴る＝陽性対照）。🔴 19本目の ⑤b-1 で空にし、値は見本 `tools/fixture_ep18.py` へ（selftest_ep18 も見本を差す形に）
        REC_QTY={          # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
            # c204：認定92（R08 p.195）「an estimate of approximately 35,000 man-days」・認定95（p.196）「The total of man-days expended was over
            #   100,000」（「超えた」＝棒は10万まで・注で断る）
            ("仕事の量（万人日）", "見込み"): (3.5, {"R08 p4195"}),
            ("仕事の量（万人日）", "実際"): (10, {"R08 p4196"}),
            # c207：認定80（R08 p.194）「ten thousand pound charges at ranges varying from 1180 feet to 370 feet」
            ("艦からの距離（メートル）", "いちばん遠い"): (1180 * 0.3048, {"R08 p4194"}),
            ("艦からの距離（メートル）", "いちばん近い"): (370 * 0.3048, {"R08 p4194"}),
            # c302：認定4 の名簿（R08 p.181〜184）の身分の欄を数えた＝USS THRESHER 108（p.181〜183）／ほか21＝STAFF 1（p.181）・USN と PORTSMOUTH
            #   NAVAL SHIPYARD 3（p.183）・Civilian Employee 13（p.183〜184）・Contractor's Representative 4（p.184）
            ("乗っていた人（人）", "艦の乗員"): (108, {"R08 p4181", "R08 p4182", "R08 p4183"}),
            ("乗っていた人（人）", "ほかに乗った人"): (21, {"R08 p4181", "R08 p4183", "R08 p4184"}),
            ("ほかに乗った人の内わけ（人）", "造船所の士官と職員"): (3 + 13, {"R08 p4183", "R08 p4184"}),
            ("ほかに乗った人の内わけ（人）", "請け負った会社"): (4, {"R08 p4184"}),
            ("ほかに乗った人の内わけ（人）", "司令部の士官"): (1, {"R08 p4181"}),
            # c315：認定13・14（V1 p.38）「a rescue chamber with a maximum depth capability of 850 feet」「Depth of water in this area is about 8500
            #   feet」（試験深度は描かない＝守りの線）
            ("深さ（メートル）", "救難室の限界"): (850 * 0.3048, {"V1 p38"}),
            ("深さ（メートル）", "海の深さ"): (8500 * 0.3048, {"V1 p38"}),
            # c613・c614：認定102（R08 p.197）「by 29 November 1962, 145 old joints had been ultrasonically tested … rejection rate of 13.8 per cent」・
            #   認定112（p.198）「is over 3000 of 2-inch size and above in hazardous systems」（「超える」＝棒は3,000まで・注で断る）
            ("調べた古い継手（本）", "11月29日"): (145, {"R08 p4197"}),
            ("不合格の割合（パーセント）", "不合格"): (13.8, {"R08 p4197"}),
            ("銀ろう付けの継手（本）", "調べた古い継手"): (145, {"R08 p4197"}),
            ("銀ろう付けの継手（本）", "同じ型の艦の全体"): (3000, {"R08 p4198"}),
            # c626：🔴 測り方の違う割合は群を分ける（§5b-114③）＝不合格（査問会 13.8・委員会の数字 14＝J p.14「14 percent below standard on the
            #   examination that was made of the 145 joints」・p.68「Our figure on this is 14 percent.」）／修理か交換を要した（中将 約10＝J p.68）
            ("不合格の割合（パーセント）", "査問会"): (13.8, {"R08 p4197"}),
            ("不合格の割合（パーセント）", "委員会の数字"): (14, {"J p8068", "J p8014"}),
            ("修理か交換を要した割合（パーセント）", "中将"): (10, {"J p8068"}),
        },
    ),
    "check_boxes": dict(
        # 🆕 2026-10-04（18本目 ⑤b-6a・⑤b-6b・⑤b-8）：18本目の箱の言葉と頁（流れ図・書類の再現図・並べ図）。原文 ref/ep18/src/ep18_pages.txt で当てた
        REC_OTHER_ROLE={    # 流れ図の「role」の箱＝役職でない言葉（報告書の文の言葉）→ 頁の集合
            # c107「3枚の紙」：前の艦長の評価書＝証拠111（X p.531）・認定91（R08 p.195）／検査の数字＝認定102（p.197「145 old joints … rejection
            #   rate of 13.8 per cent」）／検査の書類＝認定104〜106（p.197＝品質保証の部署の報告・12月4日の決定・その写し）／どこまで届いたか＝
            #   認定108（p.197「neither the results … nor the decision … was made known to the Bureau of Ships」）・J p.18（報告書は4月11日より後）
            "前の艦長の評価書": {"X p1531", "R08 p4195"}, "検査の数字": {"R08 p4197"}, "検査の書類": {"R08 p4197"},
            "どこまで届いたか": {"R08 p4197", "J p8018"},
            # c110：査問会の記録（R08 p.181〜＝認定）・議会の公聴会の記録（J p.1「Joint Committee on Atomic Energy」1963年6月26日）
            "査問会の記録": {"R08 p4181"}, "議会の公聴会の記録": {"J p8001"},
            # c218：R08 p.107「we had to have him as Prospective Commanding Officer of the JOHN C. CALHOUN SSB(N) 630」・p.109「I felt that Harvey
            #   was one of the best qualified people we could find.」
            "前の艦長": {"R08 p4107"}, "艦長の予定者（ポラリス）": {"R08 p4107"}, "新しい艦長": {"R08 p4109"},
            # c421：認定16・17（水中電話の声）・認定18（監視の記録の音）＝R08 p.185／意見45（p.212「assumptions and computer solutions」
            #   「a reasonable rationalization of probable events」・p.214「the most probable approximation of the sequence of events」）
            "水中電話の声": {"R08 p4185"}, "監視の記録": {"R08 p4185"}, "仮定と計算": {"R08 p4212"},
            "最もありうる筋書き": {"R08 p4212", "R08 p4214"},
            # c616：認定105（p.197「known to the management personnel of the Shipyard, including the Production Officer and the Commander」）・
            #   認定106（「a copy of this decision was furnished the Commanding Officer of THRESHER」）
            "造船所の生産の責任者": {"R08 p4197"}, "造船所の司令官": {"R08 p4197"}, "スレッシャーの艦長（当時）": {"R08 p4197"},
            # c618：認定102・105・108（p.197）・J p.14「no decision or no recommendation was sent to the Bureau of Ships」
            "検査の結果の数字": {"R08 p4197"}, "外さないという決定": {"R08 p4197"}, "艦船局": {"R08 p4197", "J p8014"},
            # ── 🆕 2026-10-04（18本目 ⑤b-6b）：第7〜11章の流れ図 ──
            # c705：認定47（R08 p.190「the increasing operating depths of submarines has compressed the time available in which to take effective
            #   damage control action with respect to flooding」）
            "潜る深さが増す": {"R08 p4190"}, "手を打てる時間が縮む": {"R08 p4190"},
            # c818：元分析官の書簡（A-R p9961＝個人の推定「the failure at 0911 of the primary (non-vital) electrical bus which shut down the
            #   submarine's Main Coolant Pumps (MCPs) resulting in the immediate scram」）
            "電気の系統の故障（9:11）": {"A-R p9961"}, "ポンプが止まる": {"A-R p9961"}, "原子炉が止まる": {"A-R p9961"},
            # c820：3つの見方（意見1d＝R08 p.204・艦隊司令官の意見書＝IR18 p.122・元分析官の書簡＝A-R）がそろって挙げる空気の系統
            "査問会の意見1": {"R08 p4204"}, "艦隊司令官の意見書": {"IR18 p2122"}, "元分析官の書簡（個人）": {"A-R p9961"},
            "空気の系統": {"R08 p4204", "IR18 p2122", "A-R p9961"},
            # c823：原因は決まっていない（IR18 p.6・意見49 R08 p.215）・塗り（V1 p.38 の b(1)）→ ある噂（AP p9901「no coverup」の記事）
            "決まっていない原因": {"IR18 p2006", "R08 p4215"}, "塗られたままの記録": {"V1 p38"}, "ある噂": {"AP p9901"},
            # c916：J p.122（「the Bureau of Ships was asked, "How deep can you go without a major increase in the cost of submarines?" They made
            #   a quick calculation and came up with [classified matter deleted].」）
            "艦船局への問い": {"J p8122"}, "ざっとした計算": {"J p8122"}, "その数字": {"J p8122"},
            # c918：🔴 深さの数を書かない（公開の記録＝V1 p.38 の b(1)・書簡 A-R と記事 AP p9901 は「数が書かれている」とだけ）
            "公開の記録": {"V1 p38"}, "塗られている": {"V1 p38"}, "元分析官の書簡（2013年）": {"A-R p9961"},
            "AP通信の記事（2021年）": {"AP p9901"}, "数が書かれている": {"A-R p9961", "AP p9901"},
            # cb04：J p.93（1964年7月1日「until all subsafe measures have been accomplished and certified by the Bureau of Ships in the case of
            #   each submarine」）
            "安全の改修を終える": {"J p8093"}, "艦船局が1隻ずつ認める": {"J p8093"}, "深さの制限が解ける": {"J p8093"},
            # ── 🆕 2026-10-05（18本目 ⑤b-8）：c402 海の音の監視の仕組み（地図 → 流れ図＝場所の記録が無い）──
            #   V1 p.277（分析官の証言「passive means by the hydrophone arrays at the fifteen monitoring stations within the Oceanographic
            #   Systems Atlantic」「Analysis Officer for Commander Oceanographic Systems Atlantic in Norfolk」）・認定18（R08 p.185「Commander
            #   Oceanographic Systems Atlantic obtained information that …」＝音の時刻）
            "聴音機の列": {"V1 p277"}, "15の監視所": {"V1 p277"}, "司令部で分析": {"V1 p277", "R08 p4185"}, "査問会の認定": {"R08 p4185"},
        },
        REC_MECH={          # 流れ図に出してよい言葉のうち、役職・罪名でないもの（仕組み・鎖・問いの箱と矢印の札）
            "スレッシャーの艦長",      # c218 の左上の札（R08 p.107＝艦長と副長の交代の問い）
            "外さないという決定",      # c616 の見出しの箱（認定105＝R08 p.197「decision was made on 4 December 1962 not to unlag」）
            "上がっていない", "造船所の中",   # c618 の矢印の札・群の名（認定108・J p.14「the decision was made locally in the yard」）
            # 🆕 ⑤b-6b：c818 の左上の札（A-R＝個人の推定）・c918 の左上の札・cb04 の見出しの箱（J p.93「DEPTH RESTRICTION AND SUBSAFE PACKAGE」）
            "元分析官の推定（個人）", "試験深度の数", "サブセーフ",
        },
        REC_CHIP={          # 札（chip）の言葉 → 頁の集合
            "両院原子力合同委員会・1963年と1964年": {"J p8001", "J p8091"},   # c110（J p.1＝1963年6月26日・p.91＝1964年7月1日）
            "最も資格のある1人（人事局長）": {"R08 p4109"},                    # c218（one of the best qualified people we could find）
            "決定の写し": {"R08 p4197"},                                        # c616（認定106 a copy of this decision）
            # 🆕 ⑤b-6b
            "よく知られていない": {"R08 p4190"},                  # c705（認定47 is not well recognized）
            "圧壊の前に浸水なし": {"A-R p9961"},                  # c818（no flooding prior to collapse of the THRESHER pressure-hull）
            "査問会の始まりは浸水": {"R08 p4204"},                # c818（意見1a An initial flooding casualty）
            "おそらく原因の1つ": {"R08 p4204"},                   # c820（意見1 in all probability due to … d.）
            "氷で吹けなかった（推定）": {"A-R p9961"},            # c820（unable to deballast because of the formation of ice）
            "費用を増やさずに行ける深さ": {"J p8122"},            # c916（How deep can you go without a major increase in the cost）
            "元は費用だけが根拠": {"J p8122"},                    # c916（It was originally just on the basis of cost.）
            "前に機密を解かれた文書": {"AP p9901"},               # c918（previously declassified documents）
            "それまで制限は続く": {"J p8093"},                    # cb04（will remain in effect until …）
            # 🆕 ⑤b-8
            "自分は音を出さない": {"V1 p277"},                    # c402（contacted by passive means）
            "音の時刻": {"R08 p4185"},                            # c402（認定18＝監視の記録の時刻・時刻そのものは次のカットの語り）
        },
        # 書類の再現図（表題 → dict(fields・ends・values＝記録の文にある値だけ・rec＝頁の集合)）。🆕 18本目は欄の値に**原文の英語**をそのまま
        #   書く（日本語は字幕だけ＝ルール 0b-33）。🔴 査問会の「0913R」の形は画面に出さない（台本 §1-7）＝時刻は欄の名へ。
        #   ⚠️ 文字の層の崩れを頁の画像で直した所：認定111「SCULPIN8 ETHAN' ALLEN」→ SCULPIN, ETHAN ALLEN・認定24「COMMIUNICATE」→
        #   COMMUNICATE・V1 p.140「No, sirs I don 9 t thifilk so.」→ No, sir, I don't think so.・X p.122「trv be interrupted」→ may be
        #   interrupted・X p.124「May bear very weak voice」→ May hear very weak voice（2026-10-04 に原寸の切り出しで読んだ）
        REC_FORM={
            # c112：R08 p.181「FINDINGS OF FACT」・p.204「OPINIONS」・p.217「RECOMMENDATIONS」（紙3枚）
            "認定": dict(fields={"見出し"}, ends=set(), rec={"R08 p4181"}, values={"見出し": "FINDINGS OF FACT"}),
            "意見": dict(fields={"見出し"}, ends=set(), rec={"R08 p4204"}, values={"見出し": "OPINIONS"}),
            "勧告": dict(fields={"見出し"}, ends=set(), rec={"R08 p4217"}, values={"見出し": "RECOMMENDATIONS"}),
            # c209：認定96（R08 p.196）・認定86（p.195）
            "衝撃試験の損傷（認定96・86）": dict(
                fields={"調べた人", "調べ方", "直す予定"}, ends=set(), rec={"R08 p4196", "R08 p4195"},
                values={"調べた人": "ship's force, Bureau of Ships, and Shipyard personnel", "調べ方": "intensively investigated",
                        "直す予定": "scheduled for repair during the post shakedown availability"}),
            # c213：認定69（R08 p.193）
            "取扱説明書（認定69）": dict(
                fields={"作った所", "手本", "写し方", "違い"}, ends=set(), rec={"R08 p4193"},
                values={"作った所": "an outside firm under subcontract", "手本": "an SS(N) 588 Class Ship Information Book as a guide",
                        "写し方": "virtually copied large portions of it", "違い": "many systems on THRESHER were quite different"}),
            # c217：R08 p.107（1963年5月21日・非公開の場＝THIRTY-THIRD DAY・Tuesday, 21 May 1963）
            "人事局長の証言（1963年5月21日）": dict(
                fields={"理由", "何の圧力"}, ends=set(), rec={"R08 p4107"},
                values={"理由": "The basic consideration was the pressure",
                        "何の圧力": "to furnish experienced commanding officers for the POLARIS submarines"}),
            # c219：R08 p.77
            "部隊の司令の証言（査問会）": dict(
                fields={"助言", "答え", "挙げた例", "ほかに"}, ends=set(), rec={"R08 p4077"},
                values={"助言": "he must resist that pressure", "答え": "he would resist it",
                        "挙げた例": "some hot words exchanged between the boat officer and the Ship Superintendent",
                        "ほかに": "That was the only incident I know of."}),
            # c305：認定8（R08 p.184）
            "2隻の命令（認定8）": dict(
                fields={"スレッシャー", "スカイラーク", "予定表"}, ends=set(), rec={"R08 p4184"},
                values={"スレッシャー": "THRESHER's movement orders were CONFIDENTIAL", "スカイラーク": "SKYLARK's were unclassified",
                        "予定表": "were not held by SKYLARK"}),
            # c416：V1 p.118（記録の45頁・航海士）
            "航海士の証言（査問会の記録）": dict(
                fields={"前に聞いた音", "どんな船", "似ていた音"}, ends=set(), rec={"V1 p118"},
                values={"前に聞いた音": "a lot of ships breaking up during World War II", "どんな船": "after having been torpedoed at depths",
                        "似ていた音": "a compartment collapsing"}),
            # c418：V1 p.132（甲板の当直の下士官＝p.127 で証言台に）・p.140（記録簿の係の無線員＝p.136）
            "スカイラークの乗員の証言": dict(
                fields={"当直の下士官", "問い", "記録簿の係"}, ends=set(), rec={"V1 p132", "V1 p140"},
                values={"当直の下士官": "air rushing into his tanks for about four to five seconds",
                        "問い": "like air being blown into a tank", "記録簿の係": "No, sir, I don't think so."}),
            # c509：認定24（R08 p.186＝頁の画像で読んだ）
            "スカイラークの電文（認定24）": dict(
                fields={"9:17 から", "最後の交信", "示したこと", "いま"}, ends=set(), rec={"R08 p4186"},
                values={"9:17 から": "UNABLE TO COMMUNICATE WITH THRESHER", "最後の交信": "LAST TRANSMISSION RECD WAS GARBLED",
                        "示したこと": "INDICATED THRESHER WAS APPROACHING TEST DEPTH", "いま": "CONDUCTING EXPANDING SEARCH"}),
            # c510：認定25（R08 p.186〜187）
            "査問会の認定25": dict(
                fields={"9:13 の声", "勧めた人", "艦長", "その後"}, ends=set(), rec={"R08 p4186", "R08 p4187"},
                values={"9:13 の声": "Experiencing minor difficulty", "勧めた人": "suggested by the Operations Officer",
                        "艦長": "the Commanding Officer decided not to include such information",
                        "その後": "did not include such additional information in any subsequent reports"}),
            # c517：証拠49（X p.122＝11日 12時19分・p.124＝14時33分）
            "シーウルフの報告（証拠49）": dict(
                fields={"合図", "声"}, ends=set(), rec={"X p1122", "X p1124"},
                values={"合図": "what may be interrupted keying", "声": "May hear very weak voice"}),
            # c522：意見48（R08 p.214）
            "査問会の意見48": dict(
                fields={"伝えなかったこと", "どのくらい", "関わり"}, ends=set(), rec={"R08 p4214"},
                values={"伝えなかったこと": "failed fully to inform higher authority", "どのくらい": "for an unreasonable length of time",
                        "関わり": "could not conceivably have contributed in any way to the loss of THRESHER"}),
            # c603：認定112（R08 p.198）
            "査問会の認定112": dict(
                fields={"どの艦", "系統", "大きさ", "数"}, ends=set(), rec={"R08 p4198"},
                values={"どの艦": "an S5W reactor equipped ship", "系統": "in hazardous systems", "大きさ": "of 2-inch size and above",
                        "数": "over 3000"}),
            # c604・c605（紙1枚目）：認定111（R08 p.198＝頁の画像で艦名を読んだ）。c604＝本文の一文／c605＝スケートの括弧（深さは語りに無い＝書かない）
            "査問会の認定111": dict(
                fields={"いつ", "どの艦", "何が", "スケート", "場所"}, ends=set(), rec={"R08 p4198"},
                values={"いつ": "prior to THRESHER's post shakedown availability",
                        "どの艦": "BARBEL, SKATE, SNOOK, SCULPIN, ETHAN ALLEN and THRESHER",
                        "何が": "reports of serious failures of sil-braze joints",
                        "スケート": "a 3-inch sil-braze joint parted", "場所": "under the ice"}),
            # c605（紙2枚目）：大西洋艦隊の司令官の意見書（IR18 p.123「The failure of the sil-braze joint in SKATE did not occur under the ice but in
            #   open water」）
            "艦隊司令官の意見書": dict(
                fields={"訂正", "場所"}, ends=set(), rec={"IR18 p2123"},
                values={"訂正": "did not occur under the ice", "場所": "in open water"}),
            # c609：認定98（R08 p.196＝艦船局の手紙 1962年8月28日を引く）
            "艦船局の手紙（1962年8月28日）": dict(
                fields={"何を", "いつまで", "どれだけ"}, ends=set(), rec={"R08 p4196"},
                values={"何を": "employ a minimum of at least one ultrasonic test team",
                        "いつまで": "throughout the entire assigned post shakedown availability",
                        "どれだけ": "the maximum number of sil-braze joints"}),
            # c610：認定99（R08 p.196）
            "作業の指示書（認定99）": dict(
                fields={"班", "先に", "時間があれば"}, ends=set(), rec={"R08 p4196"},
                values={"班": "use of one ultrasonic test team", "先に": "to test first those joints not lagged",
                        "時間があれば": "lagging would be removed to permit tests of additional joints"}),
            # c622：意見21（R08 p.207）
            "査問会の意見21": dict(
                fields={"誰が", "何を", "判断"}, ends=set(), rec={"R08 p4207"},
                values={"誰が": "the management of the Portsmouth Naval Shipyard", "何を": "determining not to unlag pipes",
                        "判断": "did not exercise good judgment"}),
            # c624：J p.67（「the testimony I gave in closed session to the court of inquiry on April 29, 1963」）・p.68
            "原子炉の責任者の証言（1963年4月29日）": dict(
                fields={"調べた分", "その結果"}, ends=set(), rec={"J p8067", "J p8068"},
                values={"調べた分": "about 5 percent of her silver-brazed joints were ultrasonically inspected",
                        "その結果": "about 10 percent of those checked required repair or replacement"}),
            # ── 🆕 2026-10-04（18本目 ⑤b-6b）：第7〜11章の書類の再現図37枚（ref/ep18/src/ep18_pages.txt で当てた・文字の層が崩れた所と塗りの
            #   札は頁の画像で読んだ）。🔴 この記録の塗りは**白く抜いて赤い字の記号**（b(1)・(b) (1)・b(3) 10 USC 130・(b) (6)）＝値に頁に見える
            #   とおりの記号／公聴会の本の削除は「[classified matter deleted]」と刷られている
            # c703・c704：認定46（R08 p.190＝頁の画像で「from 700 feet to b(1)」「from (b) (1) per cent to (b) (1) per cent」）
            "査問会の認定46": dict(
                fields={"比べた艦", "試験深度", "空気", "いつ", "吹き出せる量", "その数", "速さ"}, ends=set(), rec={"R08 p4190"},
                values={"比べた艦": "as compared to the SKIPJACK", "試験深度": "An increase in test depth from 700 feet to b(1)",
                        "空気": "About the same high pressure air bank capacity.", "いつ": "While at test depth:",
                        "吹き出せる量": "A reduction in the amount of ballast which could be blown",
                        "その数": "from (b) (1) per cent to (b) (1) per cent", "速さ": "A reduction in the rate of blowing ballast"}),
            # c706：認定48（R08 p.190＝文字の層「blovw」ほか＝頁の画像で読んだ）。除湿器は c707
            "艦船局の設計の基準（認定48）": dict(
                fields={"基準", "深さ", "氷"}, ends=set(), rec={"R08 p4190"},
                values={"基準": "capability to blow all main ballast tanks twice at periscope depth",
                        "深さ": "There is no modification to this criteria for depth of blowing",
                        "氷": "There are no requirements … which would prevent the formation of blockages due to ice"}),
            # c708：J p.32（「Deptli」＝頁の画像で Depth）・p.35（1963年6月27日・艦船局の長）
            "艦船局の長の証言（議会・1963年6月27日）": dict(
                fields={"深さ", "決め手"}, ends=set(), rec={"J p8032", "J p8035"},
                values={"深さ": "Depth is not significant insofar as freezeup is concerned.",
                        "決め手": "It is a matter of pressure differential."}),
            # c710：R08 p.26（最初の試運転の前夜のはしけの会議）
            "大佐の証言（査問会）": dict(
                fields={"話したこと", "ポンプの回し方", "理由"}, ends=set(), rec={"R08 p4026"},
                values={"話したこと": "what would happen if we flooded any one area", "ポンプの回し方": "we were all for having them in high",
                        "理由": "air was very questionable and how much good it would do at that depth"}),
            # c711：R08 p.33（元設計部長）
            "元設計部長の証言（査問会）": dict(
                fields={"話し合い", "決まったこと", "空気", "おそれ"}, ends=set(), rec={"R08 p4033"},
                values={"話し合い": "whether or not we should attempt to blow the main ballast tanks at deep depths",
                        "決まったこと": "it was decided that this would not be prudent", "空気": "the air would expand",
                        "おそれ": "we might make an uncontrolled ascent"}),
            # c713：J p.83（1963年7月23日）
            "原子炉の責任者の証言（議会・1963年7月23日）": dict(
                fields={"いつから", "決まり", "議員", "中将"}, ends=set(), rec={"J p8083"},
                values={"いつから": "from the time of the 400-foot submarine",
                        "決まり": "did not basically change the blowing requirements as they went deeper",
                        "議員": "That doesn't seem right to me.", "中将": "This isn't right."}),
            # c718：意見38k・c723：意見39（R08 p.211）
            "査問会の意見38": dict(
                fields={"考え方", "試験深度で", "改め方"}, ends=set(), rec={"R08 p4211"},
                values={"考え方": "The fail-closed concept for the three air banks",
                        "試験深度で": "is not desirable for safety of the ship at test depth",
                        "改め方": "should be modified to provide fail-on-the-line; i.e., air bank valves open."}),
            "査問会の意見39": dict(
                fields={"何を", "どう試すか"}, ends=set(), rec={"R08 p4211"},
                values={"何を": "the high pressure blow of submarine main ballast tanks",
                        "どう試すか": "tested under conditions simulating a full blow at test depth"}),
            # c801〜c803：意見1（R08 p.204＝a の浸水が続き b〜d が重なった＝1つの文）
            "査問会の意見1": dict(
                fields={"何が", "見立て", "1つ目", "2つ目", "3つ目", "4つ目"}, ends=set(), rec={"R08 p4204"},
                values={"何が": "the loss of the U.S.S. THRESHER", "見立て": "was in all probability due to:",
                        "1つ目": 'An initial flooding casualty from an orifice between 2" and 5" in size in the engine room',
                        "2つ目": "Loss of reactor power due to an electrically-induced automatic shutdown",
                        "3つ目": "Inadequate operating procedures … a flooding casualty and the loss of reactor power",
                        "4つ目": "A deficient air system, susceptible to freeze-up, with low capacity and low blow rate."}),
            # c806・c808：意見5（R08 p.204）
            "査問会の意見5": dict(
                fields={"浸水は", "候補a"}, ends=set(), rec={"R08 p4204"},
                values={"浸水は": "a flooding casualty in THRESHER could have resulted from:", "候補a": "A faulty sil-braze joint."}),
            # c809：意見2（R08 p.204）＝c810 の決め所の句は書かない
            "査問会の意見2": dict(
                fields={"混ぜると", "狭まるもの"}, ends=set(), rec={"R08 p4204"},
                values={"混ぜると": "in melding together fact and conjecture,",
                        "狭まるもの": "thus narrowing the field of search for possible causes of the casualty."}),
            # c811：意見49（R08 p.215）
            "査問会の意見49": dict(
                fields={"正確な原因", "分かっていること"}, ends=set(), rec={"R08 p4215"},
                values={"正確な原因": "although we may never learn the exact cause",
                        "分かっていること": "we do know enough to make it necessary for us to explore in depth the many possible causes"}),
            # c813・cb18：海軍長官の最後の意見書（IR18 p.6＝頁の画像で行の順を読んだ）
            "海軍長官の最後の意見書（1965年）": dict(
                fields={"候補", "始まり", "分からない", "原因", "良い面"}, ends=set(), rec={"IR18 p2006"},
                values={"候補": "faulty design, structural or mechanical failure or malfunction or personnel error",
                        "始まり": "set in motion the chain of events which led to eventual catastrophe",
                        "分からない": "We, therefore, will never know whether",
                        "原因": "we have not been able to establish the cause", "良い面": "has had its beneficial effects"}),
            # c816：J p.89（1963年7月23日の声明の結び）
            "原子炉の責任者の声明（議会・1963年7月23日）": dict(
                fields={"分かっていること", "どうするか"}, ends=set(), rec={"J p8089"},
                values={"分かっていること": "I do know there were weaknesses in her design, fabrication, and inspection",
                        "どうするか": "that must be corrected"}),
            # c817：元分析官の書簡（A-R p9961＝個人・短い一節）
            "元分析官の書簡（2013年4月10日）": dict(
                fields={"書いた人", "宛て先", "件名"}, ends=set(), rec={"A-R p9961"},
                values={"書いた人": "the Analysis Officer at the SOSUS Evaluation Center in April 1963",
                        "宛て先": "Deputy Chief of Naval Operations Warfare Systems",
                        "件名": "Information and Security Issues Associated with the Loss of the USS THRESHER"}),
            # c821：大西洋艦隊の司令官の意見書（IR18 p.120 の頭書き「FIRST ENDORSEMENT」＝1963年6月12日・本文 p.122）
            "1番目の意見書（1963年6月12日）": dict(
                fields={"空気の系統", "評価", "現役の艦"}, ends=set(), rec={"IR18 p2120", "IR18 p2122"},
                values={"空気の系統": "of inadequate capacity, susceptible to freeze-up and with an inadequate blow rate",
                        "評価": "This grossly unsatisfactory situation",
                        "現役の艦": "Immediate steps have been taken in operating ships to: (1) remove high pressure air reducer strainers"}),
            # c902：J p.146〜147（付録6・1963年6月20日）・c904：J p.164（1963年8月29日）
            "海軍長官の書簡（1963年6月20日）": dict(
                fields={"宛て先", "記録", "漏れたら"}, ends=set(), rec={"J p8146", "J p8147"},
                values={"宛て先": "Chairman, Joint Committee on Atomic Energy",
                        "記録": "a considerable portion of the record is classified",
                        "漏れたら": "Any unauthorized release would seriously affect our nuclear ship and Polaris programs."}),
            "海軍長官の返事（1963年8月29日）": dict(
                fields={"時期", "何を", "おそれ", "誰の心で"}, ends=set(), rec={"J p8164"},
                values={"時期": "it would be a poor time indeed",
                        "何を": "to release piecemeal the facts and assumptions documented by your hearings",
                        "おそれ": "could materially downgrade our offensive-defensive submarine weapons systems",
                        "誰の心で": "both in the public mind and the minds of our officers and men that man them"}),
            # c908：塗りの札（頁の画像の赤い字）
            "塗った理由を示す札（公開の記録）": dict(
                fields={"国の安全", "法律で伏せてよい情報", "個人の私生活"}, ends=set(), rec={"V1 p38", "V1 p54", "R08 p4181"},
                values={"国の安全": "b(1)", "法律で伏せてよい情報": "b(3) 10 USC 130", "個人の私生活": "(b) (6)"}),
            # c912・c919：AP の記事（p9901）＝原告の言葉（c913）は書かない
            "AP通信の記事（2021年8月2日）": dict(
                fields={"訴えた人", "その人", "読み方"}, ends=set(), rec={"AP p9901"},
                values={"訴えた人": "who sued for release of the documents under the Freedom of Information Act",
                        "その人": "himself the skipper of a Thresher-class submarine", "読み方": "900 feet beyond its test depth"}),
            # c919：認定17（R08 p.185）＝査問会は意味を書いていない
            "査問会の認定17": dict(
                fields={"9:17ごろの声"}, ends=set(), rec={"R08 p4185"}, values={"9:17ごろの声": '"... nine hundred North"'}),
            # c915：J p.122・c917：J p.124（1964年7月1日）
            "原子炉の責任者の証言（議会・1964年7月1日）": dict(
                fields={"話したこと"}, ends=set(), rec={"J p8122"},
                values={"話したこと": "how that magic number [classified matter deleted] first came about"}),
            "海軍の少将の証言（議会・1964年7月1日）": dict(
                fields={"検討", "行く深さ", "戦術の根拠"}, ends=set(), rec={"J p8124"},
                values={"検討": "one other study in the Office of Chief of Naval Operations",
                        "行く深さ": "the depth to which we would go is what the state of the art will allow us",
                        "戦術の根拠": "there is not a tactical justification for [classified matter deleted] feet or any other depth"}),
            # ca04：R08 p.66（捜索の指揮官）
            "捜索の指揮官の証言（査問会）": dict(
                fields={"写すこと", "カメラの位置", "たとえ"}, ends=set(), rec={"R08 p4066"},
                values={"写すこと": "is a very easy operation", "カメラの位置": "the camera must be 30 feet from the spot",
                        "たとえ": "being up in an airplane 8500 feet high with a string and a camera on the end of it"}),
            # cb02：意見4（R08 p.204）・cb06：勧告20（p.220）・cb08：意見42（p.212）
            "査問会の意見4": dict(
                fields={"見直すまで", "制限"}, ends=set(), rec={"R08 p4204"},
                values={"見直すまで": "until each individual submarine's readiness has been reassessed",
                        "制限": "it would be prudent to retain the current interim depth limitation"}),
            "査問会の勧告20": dict(
                fields={"組織", "分析", "伝えること", "検討"}, ends=set(), rec={"R08 p4220"},
                values={"組織": "an organization, similar to that employed in Naval Aviation",
                        "分析": "the analysis of events and developments which pertain to submarine safety",
                        "伝えること": "the timely dissemination of such information", "検討": "That early consideration be given"}),
            "査問会の意見42": dict(
                fields={"情報", "分析と伝達", "欠陥", "結果"}, ends=set(), rec={"R08 p4212"},
                values={"情報": "all information to be had from the BARBEL and other casualties",
                        "分析と伝達": "thorough and imaginative analysis and timely dissemination",
                        "欠陥": "the deficiencies which probably caused THRESHER's loss", "結果": "could have been reduced"}),
            # cb10：J p.95・97（艦船局の副長）・cb11：J p.94（艦隊の運用の担当の中将）＝1964年7月1日
            "艦船局の副長の証言（議会・1964年7月1日）": dict(
                fields={"始まり", "振り返れば", "安全"}, ends=set(), rec={"J p8095", "J p8097"},
                values={"始まり": "The genesis of this effort was not Thresher's loss",
                        "振り返れば": "we moved too fast and too far in areas of offensive and defensive capabilities",
                        "安全": "Submarine safety did not keep pace."}),
            "海軍の中将の証言（議会・1964年7月1日）": dict(
                fields={"4月の勧告", "動けなくなる所", "救難"}, ends=set(), rec={"J p8094"},
                values={"4月の勧告": "the Deep Submergence System Review Group … submitted its recommendations",
                        "動けなくなる所": "could be disabled in water too shallow to collapse the hull",
                        "救難": "still be beyond our rescue capability"}),
            # cb15・cb16：意見55（R08 p.216）＝cb17 の決め所の文は書かない
            "査問会の意見55": dict(
                fields={"水準", "届いていないもの", "急な変化", "計画", "誰のせいか", "気づかれなかったもの"}, ends=set(), rec={"R08 p4216"},
                values={"水準": "required to insure the thorough overhaul and safe operation of the U.S.S. Thresher",
                        "届いていないもの": "numerous practices, conditions and standards which were short of those",
                        "急な変化": "the rapid changes … of submarines during the last decade",
                        "計画": "the accelerated pace of the submarine program",
                        "誰のせいか": "They can be blamed on no individual or individuals",
                        "気づかれなかったもの": "many would not have come to notice had THRESHER not been lost"}),
            # cb20：NAVSEA の記事（p9951）＝「16隻」は語りに無い＝書かない
            "米海軍 艦艇の部門の記事（2023年4月6日）": dict(
                fields={"サブセーフのあと", "その艦"}, ends=set(), rec={"NAVSEA p9951"},
                values={"サブセーフのあと": "the U.S. Navy has only lost one submarine, USS Scorpion (SSN 589)",
                        "その艦": "Scorpion was not SUBSAFE-certified"}),
        },
        REC_CAUSE={         # 並べ図の項目 → 頁
            # c115：この動画の3つの問い（c114 の語り）＝その問いに答える記録の頁（意見1・認定108／25・1964年の要旨）
            "浮き上がれなかった理由": {"R08 p4204"}, "伝わらなかった検査と声": {"R08 p4197", "R08 p4186"},
            "海の底に残った物": {"R17書 p9802"},
            # 🆕 ⑤b-6b：c807＝意見5（R08 p.204）の6つの候補（a〜f）
            "銀ろう付けの継手の不良": {"R08 p4204"}, "未発見の衝撃の損傷": {"R08 p4204"}, "曲がるホースの故障": {"R08 p4204"},
            "鋳物か配管の故障": {"R08 p4204"}, "船体の小さな破損": {"R08 p4204"}, "不明（部品の故障を含む）": {"R08 p4204"},
        },
    ),
    "check_mech": dict(
        # 🆕 2026-10-04（18本目 ⑤b-4）：仕組みの模式図（m18＝`tools/mech18.py`）の記録。原文 ref/ep18/src/ep18_pages.txt で当てた
        # 🔴 記録＝門番の側（§5b-88＝型〈mech18 の CRIT_AVG・BANKS_N・JT・CONE_APEX ほか〉を読まない）。原文 ref/ep18/src/ep18_pages.txt で当てた
        #    （R08＝査問会の記録 第8回公開 p4001〜・X＝査問会の証拠 第9・10回公開 p1001〜・J＝議会の公聴会 印刷頁＋8000）。
        #    🔴 §0b（題材を替えるとき空にする場所）：19本目以降の ⑤b-1 で見本 `tools/fixture_ep18.py` へ移して空にする（18本目の型＝mech18 だけの表）
        REC_M18=dict(
            lands=(2, "X p1171（40% Average・25% Min. each land）・R08 p4197（認定103：either land）"),
            avg=(40.0, "R08 p4197（認定103：40 per cent bond）"),
            land=(25.0, "R08 p4197（認定103：25 per cent minimum, either land）"),
            banks=(4, "R08 p4191（認定51：air banks 2, 3 and 4 … air bank #1）"),
            cone=(0.25, "R08 p4190（認定49：conical mesh strainers）"),          # 先の高さ÷底の高さ の上限（円すい＝先がすぼまる）
            clock={"9:11": "R08 p4185（認定18：ceased functioning in FAST mode at 0911R）"},
            pct={"40%": "R08 p4197", "25%": "R08 p4197"},
            # 語りに無い出来事（次のカットの語り）＝札に出さない語（ルール 0b-38③）
            ng=dict(shock=("フィート", "メートル", "トン", "ポンド", "m"),          # 距離と重さは c207（数の比べ）
                    loop=("7.1", "電動機", "時速", "ノット"),                       # 7.1分・非常用の電動機は c720（時間の帯）
                    ice=("破",)),                                                   # 網が破れる（認定50）は c715 の決め所
        ),
    ),
    "check_illu": dict(
        # 🆕 2026-10-04（18本目 ⑤b-2〜⑤b-3）：置き場 SA・SB・SC・SD の記録（深さ・上げ・音の輪・点・円・目印・札の言い方）＝頁は ss.REC_DOCS の通し番号
        # 🔴 記録の値は門番の側に持つ（型の定数 SA_RESCUE_M・SA_ROPE_M・SA_SEABED_M・SA_UP を読まない＝§5b-88）。頁は ss.REC_DOCS の通し番号
        REC_DEPTH=dict(rescue=(260.0, "V1 p38（認定13：850フィート）"), rope=(2200.0, "V1 p183（7,200フィートの綱）"),
                         seabed=(2600.0, "R08 p4185（認定14：約8,500フィート）")),
        REC_UP_MAX=(15.0, "R08 p4214（意見45 Case III：15° up angle＝頁の画像で確かめた）"),
        REC_BOOM_CLK=("9:18.1", "R08 p4185（認定18：0918.1R）"),
        # 9時18.1分の段の札に要る言い方（認定18 と意見45 の言い方＝映像方針 §1-3・§12 ⑰）
        REC_BOOM_WORDS=(("内破でありうる", "認定18「of the type which could have been made by an implosion」"),
                          ("大きく低い音", "認定18「high energy, low frequency noise」"),
                          ("船体の圧壊", "意見45「the actual hull collapse occurred at 0918.1R」"),
                          ("見立て", "意見45＝査問会の見立て（推定）")),
        # 🔴 記録の値は門番の側に持つ（型の SB_PTS・SB_TS・SB_OIL・SC_CIRCLE_M を読まない＝§5b-88）。頁は ss.REC_DOCS の通し番号
        REC_SB=dict(meet=((-65.05, 41.0 + 46.0 / 60.0), "R08 p4185（認定11：41-46 North, 65-03 West）"),
                      datum=((-65.0, 41.75), "R08 p4065（datum：65 degrees west and 41 degrees, 45 minutes north）"),
                      loran=((-(64.0 + 59.0 / 60.0), 41.75), "R08 p4186（認定22d：logged at 0921R as 41-45N 64-59W）")),
        REC_SB_TS=(147.0, 3400 * 0.9144, "R08 p4185（認定11：SKYLARK bore 147 True, 3400 yards from THRESHER）"),
        # 認定31「about seven miles to the Southeast of SKYLARK's 0917R position」＝マイルの種類が書いていない＝法定マイルと海里の両方の幅
        REC_SB_OIL=(135.0, (7 * 1609.344, 7 * 1852.0), "R08 p4188（認定31）"),
        # 🆕 ⑤b-8（ca02）：捜索の海域「10 miles by 10 miles centered at the point called datum」（R08 p.65）＝マイルの種類が書いていない＝幅
        REC_SB_SQ=((10 * 1609.344, 10 * 1852.0), "R08 p4065（10 miles by 10 miles centered at the point called datum）"),
        # 距離の札＝言ってよい言い方と、その札が指す線（約3.1km＝3,400ヤード・十数キロ＝7マイルのどちらでも合う幅＝台本 §9-1）
        SB_DIST_TAGS=(("約3.1km", "mid_ts"), ("十数キロ", "mid_se")),
        REC_SC_CIRCLE=(400 * 0.9144, "R17書 p9802（a circle of diameter 400 yd）"),
        REC_SC_MARKERS=(900, "No.710-64 p9801（900 markers）"),
        SC_NUMS={"900", "370", "5", "6", "710", "64"},      # SC の札に出してよい数（目印900・直径約370m・5つか6つ・発表 No.710-64）
        REC_SD_ON="R17書 p9802（TRIESTE II … was able to locate on top of a portion of the THRESHER hull）",
    ),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・titan_fig.GEO・（gate を渡せば）その門番の記録の表を18本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss と GEO は触らない）＝14・15・16本目の見本 `fixture_ep14`・
    `fixture_ep15`・`fixture_ep16` と重ねるとき（check_mech の selftest は14・15・16・18本目の検算を1つの処理で回す＝先に14本目を全部差し込み、
    15・16・18本目は表だけ足す）。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が18本目の表で
       19本目の画を測る）。apply の前に**無かった名**（ss の FORM_*・FL_*・AX_*・fl・qrows …／門番の表）も覚えて、restore で**消す**
       ＝selftest のあとに18本目の名が本番へ残らない（fixture_ep15・fixture_ep16 と同じ作り）"""
    saved = dict(ss={}, ss_new=[], geo=None, gate=gate, tables={}, tables_new=[])
    if not tables_only:
        import titan_fig as F
        from cuts import ss
        saved["ss"] = {n: getattr(ss, n) for n in SS_NAMES if hasattr(ss, n)}
        saved["ss_new"] = [n for n in SS_NAMES if not hasattr(ss, n)]
        saved["geo"] = dict(F.GEO)
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
        F.GEO.update(GEO)
    for k, v in tabs.items():
        setattr(gate, k, v)


CUTS_SHA = "b11797a"       # 18本目の章ファイルが最後に本線で live だった commit（2d627a2 で19本目の空の器にした）
_CUTS18 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def cuts_ep18():
    """18本目の章ファイル（git の CUTS_SHA の `tools/cuts/`）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。"""
    if _CUTS18:
        return _CUTS18[0]
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
        raise RuntimeError(f"🔴 18本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts18_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep18 の写真・頁を読む＝根の下の作業場所の
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
        raise RuntimeError(f"🔴 18本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}）")
    _CUTS18.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を18本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で19本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep18()
    _SAVED.append(dict(cuts=(dict(cuts.PLAN), dict(cuts.SPEC))))
    cuts.PLAN.clear()
    cuts.PLAN.update(copy.deepcopy(plan))
    cuts.SPEC.clear()
    cuts.SPEC.update(copy.deepcopy(spec))


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。
    ss と門番の表は、apply の前に無かった名を消す。GEO は fixture_ep14・15・16 と同じに、覚えた写しで入れ替える（clear → update）。
    tables_only で差し込んだ分は ss・GEO を覚えていない＝戻さない（先に差し込んだ別の見本を壊さない）。LIFO（あとに apply した順）"""
    while _SAVED:
        s = _SAVED.pop()
        if s.get("cuts") is not None:          # apply_cuts() の分＝19本目の PLAN・SPEC へ戻す
            import cuts
            plan, spec = s["cuts"]
            cuts.PLAN.clear()
            cuts.PLAN.update(plan)
            cuts.SPEC.clear()
            cuts.SPEC.update(spec)
            continue
        if s["geo"] is not None:
            import titan_fig as F
            from cuts import ss
            for n, v in s["ss"].items():
                setattr(ss, n, v)
            for n in s["ss_new"]:
                if hasattr(ss, n):
                    delattr(ss, n)
            F.GEO.clear()
            F.GEO.update(s["geo"])
        gate = s["gate"]
        for k, v in s["tables"].items():
            setattr(gate, k, v)
        for k in s["tables_new"]:
            if hasattr(gate, k):
                delattr(gate, k)
