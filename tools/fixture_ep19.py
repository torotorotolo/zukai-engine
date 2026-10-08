# -*- coding: utf-8 -*-
"""19本目（サーフサイドのマンション崩壊のリメイク・2021-06-24・NIST の技術的知見の動画）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-08（20本目 日本航空123便のリメイク ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `70c7e51` と同じ）
  ・`cuts/ss.py` の19本目の値＝案C の出典の表（REC_DOCS＝TR・AC・TF・GJ・A13・EST18・A14・B03・B05・A04・A16・MC18・MIN18・A12・B08・B01・B02・B07・
    A17・A18・A19）・描いてよい数（ILLU_COUNTS）・想定の札（ILLU_ASSUME・`_A1_ASSUME`）・壊れる物のカット（ILLU_DESTROY_CUTS）・縮尺を持たない
    上から見た絵の置き場（ILLU_TOP_NOSCALE）・軸の型（TL_NOTE・ORDER_NOTE・AX_*・SIGNS・ALL_SIGNS・AXI の項目）・棒（QG・QB）・書類の再現図
    （FORM_*＋紙の置き場 _P2〜_P4）・流れ図（FL_*・FLP・`fl()`）・並べ図（CAUSE）・決め所の出どころの札（QDOC・QWHO・QDATE_LB・`qrows()`）
    （19本目 ⑤b-2〜⑤b-8）。ILLU_SPLIT_TIMES ほか空のままだった案C の表（ILLU_ROLES・ILLU_SEC_OK・ILLU_CLOCK_OK・ILLU_SUB_*・ILLU_BOOM_CUTS・
    ILLU_MIX_TODO・AXIS_DOCS）も、19本目の状態＝空として持つ（18本目の見本と入れ子にしても19本目の状態になる）
  ・`titan_fig.GEO` の19本目の地点＝**無い**（19本目は地点の鍵を足さなかった＝`70c7e51` の GEO は `275c4d5` と同じ）。
    GEO は空の表のまま持つ（15・16・18本目の見本と同じ作り＝apply/restore の対称）
  ・門番の記録の表（check_axis＝REC_AXIS・ORDER_REF_MIN／check_qty＝REC_QTY／check_boxes＝REC_OTHER_ROLE・REC_MECH・REC_CHIP・REC_FORM・REC_CAUSE／
    check_mech＝REC_M19／check_illu＝REC_A1・REC_A23）
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を19本目の実物でも確かめている＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は20本目の空の器にした
  （fixture_ep14・fixture_ep15・fixture_ep16・fixture_ep18 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep19
      fixture_ep19.apply(sys.modules[__name__])   # その処理の中だけ ss・GEO・この門番の記録の表が19本目になる
      try: …（検算）
      finally: fixture_ep19.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14・15・16・18本目の見本と重ねるとき（check_mech は14本目の検算と15・16・18・19本目の検算を1つの処理で回す）は
      fixture_ep19.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss・GEO は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと20本目以降の画に19本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。
■ 注意:
  ⚠️ 見本の頁の原文 `ref/ep19/src/ep19_pages.txt` は git の外（本線の作業ツリーにだけある）＝無いときは頁の照合を飛ばす
     （check_illu の `_pages()` が None を返す）。
  ⚠️ 19本目の selftest（`check_axis.selftest_ep19`・`check_mech._selftest_m19`・`check_illu.selftest_a1`／`selftest_a23`）は**章ファイルの
     SPEC を読まない**（場面・図は selftest の中で組む）＝`apply()` だけで通る（18本目の `check_illu.selftest_ep18` が `cuts.SPEC["c101"]` を
     読んで `KeyError` になったのとは違う）。それでも `apply_cuts()`（19本目の章ファイルを git の `CUTS_SHA`＝`0dcaa9c` から取り出して
     `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ19本目に入れ替える・git が無い所では止める＝fail closed）を用意した＝19本目の実物の絵を
     門番にかけ直したいとき（`restore()` で20本目へ戻る・LIFO）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep19/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は19本目の道を持つ。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝19本目も 1.66＝18本目の値のまま）は見本に入れない（16・18本目の見本も入れていない）＝本番の ss は
     今の値のまま残し、20本目の束（⑤b-7）で取り直す。
  ⚠️ `check_axis.ORDER_REF_MIN`（並び order の基準＝町の頁の崩落の時刻 1:22）は19本目の記録の値＝見本の GATES["check_axis"] に入れた
     （本番は None＝空のあいだ、時刻の並びは「基準が空」で止まる）。`ORDER_UNIT`・`ORDER_NOTE`・`_REF` は型の読み方＝本番に残した。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep19"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 19本目 ⑤b-2〜⑤b-3
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：次の回は下の表を**その回の資料と時刻**に替える（頁の番号の書き方・資料の名の決め方は REC_DOCS の注）。
#   REC_PAGES … 部品の出典（`rec=`）を当てる原文（`=== p<N> ===` で頁を割った1ファイル＝④ の make_pages.py の出力）
#   REC_DOCS  … 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面に出す名前・頁の出し方（print＝印字の頁／pdf＝PDF の頁）
#   ILLU_* … 19本目は割れる時刻・時計の札・秒の札・潜水艦・音の輪・混ざりのつなぎ待ちを使わなかった＝空のまま（下の値）
REC_PAGES = REF / "src" / "ep19_pages.txt"      # ④ の make_pages.py の出力（git の外＝手元だけ）
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    # 🆕 19本目 ⑤b-2（2026-10-06）：通し頁は `ref/ep19/src/ep19_pages.txt`（④ の make_pages.py）＝TR の行 n → p(1000+n)・AC の PDF 頁 n →
    #   p(2000+n)・TF のコマ・スライド → p9001〜。TR は行（頁ではない）・TF はスライド＝画面に頁を出さない（page=None）
    "TR": dict(range=(1001, 1489), name="NIST 技術的知見の動画の語り（2026年6月）", page=None, base=0),
    "AC": dict(range=(2001, 2082), name="NIST の諮問委員会の資料（2026年9月）", page="pdf", base=2000),
    "TF": dict(range=(9001, 9808), name="NIST 技術的知見の動画のスライド（2026年6月）", page=None, base=0),
    # 🆕 ⑤b-3：大陪審の報告（GJ の PDF 頁 n → p(3000+n)・印字の頁＝PDF 頁−3）・町の発表（A13＝1頁）
    # 🔴 ⑤b-6（2026-10-06）：名の年を「（2022年）」から直した＝表紙 p3001「FILED December 15, 2021」・結び p3043「Date: December 15. 2021」・
    #   州検事の声明 A16（2021年12月15日）・台本の語り「2021年12月に出た」と合わせる
    "GJ": dict(range=(3001, 3043), name="マイアミ・デイド郡の大陪審の報告（2021年12月）", page="print", base=3003),
    "A13": dict(range=(5102, 5102), name="サーフサイド町の発表（2026年8月13日）", page=None, base=0),
    # 🆕 ⑤b-6（2026-10-06）：書類・流れ図・数の比べ・地図の出典。見積もり（EST18＝町が公開した転送メールの PDF の18頁にある添付＝
    #   🔴 その PDF は私人の情報を含む A09＝git の外・画面に頁を出さない＝見積もりの頁とずれる）・州の法律（A14＝PDF 頁）・郡の発表（B03）・
    #   町の警察の会報（B05＝PDF 頁）・NIST の発表（A04）・州検事の声明（A16）
    "EST18": dict(range=(4318, 4318), name="モラビトの見積もり（2018年10月）", page=None, base=0),
    "A14": dict(range=(6001, 6088), name="フロリダ州の法律 SB 4-D（2022年）", page="pdf", base=6000),
    "B03": dict(range=(5201, 5201), name="マイアミ・デイド郡の発表（2021年7月4日）", page=None, base=0),
    "B05": dict(range=(5301, 5303), name="サーフサイド町の警察の会報（2021年7月8日）", page="pdf", base=5300),
    "A04": dict(range=(5001, 5001), name="NIST の発表（2026年6月22日）", page=None, base=0),
    "A16": dict(range=(5801, 5801), name="マイアミ・デイド郡の州検事の声明（2021年12月15日）", page=None, base=0),
    # 🆕 ⑤b-5（2026-10-06）：軸の型（年表・時間の帯）の出典。調査の報告（MC18＝町の写しの PDF 頁＝報告の頁）・議事録（MIN18＝町の写しの PDF 頁）・
    #   町の頁（A12）・NIST の発表（B08）・GAO（B01）・FEMA（B02）・裁判所（A17・A18・A19＝PDF 頁）。⚠️ A11（MIN18）・A17 の原文は git の外のまま
    "MC18": dict(range=(4001, 4009), name="モラビトの調査の報告（2018年10月）", page="print", base=4000),
    "MIN18": dict(range=(4101, 4107), name="理事会の議事録（2018年11月15日）", page="pdf", base=4100),
    "A12": dict(range=(5101, 5101), name="サーフサイド町の頁", page=None, base=0),
    "B08": dict(range=(5005, 5005), name="NIST の発表（2024年11月21日）", page=None, base=0),
    "B01": dict(range=(5601, 5617), name="米政府説明責任局（GAO）の報告（2024年2月）", page="pdf", base=5600),
    "B02": dict(range=(5701, 5705), name="FEMA の発表（2021年7月）", page="pdf", base=5700),
    # ⑤c'（10-07）：c710 の出典を手書き（「p.2」）から src() へ＝頁の書き方をほかの41か所の「PDF N頁」にそろえるために足した
    #   名は短く（「マイアミ・デイド郡の」を付けると c710 の出典の行が 17px に縮んだ）
    "B07": dict(range=(5501, 5506), name="郡長のメモ（2023年10月26日）", page="pdf", base=5500),
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
}                                           # ✅ ⑤b-7c（10-07）：c618 の尻の頁（A01 p.47）をつないだ＝空
ILLU_MIX_BUNDLE = REF / "credits.json"      # 束ができたか（混ざりのつなぎ待ちの終わり）を見るファイル

# 🔴 2026-10-06（19本目 ⑤b-1）：空にした（18本目は割れる時刻・出典の名つきの点を使わなかった＝空のままの値＝`tools/fixture_ep18.py`）
AXIS_DOCS = {}


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：軸の型（`tools/axis.py`・門番 `check_axis`）── 19本目 ⑤b-5（年表・時間の帯・並び）
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の AX_*・AXI の項目・TL_NOTE・ORDER_NOTE・SIGNS・ALL_SIGNS は19本目の値（20本目の ⑤b-1 で見本 fixture_ep19 へ）。
#   値と頁は ref/ep19/src/ep19_pages.txt で当てた＝門番の側の表（check_axis.REC_AXIS）と照らされる（§5b-88）。
# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
AXI = {}

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
# 🆕 ⑤b-6（2026-10-06）：cc17 追悼の灯（毎年＝ともす6月24日・消す7月20日）。年は画面に出さない（点は lab=False・目盛りは日と月だけ）＝
#   軸の中の年は捜索の年（2021年）を借りる。時刻は町の頁の2023〜2025年の記録（2022年は午後8時9分＝「このところは」の語りの外）
AX_TORCH = dict(view="date", span=("2021-06-20", "2021-07-26"),          # ⚠️ 門番 layout：6月24日の目盛りの「6月」を点の線が貫いた＝目盛りを点からずらす
                ticks=("2021-06-22", "2021-06-29", "2021-07-06", "2021-07-13", "2021-07-20"))
SIGNS = ("約3週間前", "約1週間前", "約17時間前", "約9時間前", "約3時間前")                            # c523 の並び
ALL_SIGNS = ("約3週間前", "約1週間前", "約17時間前", "約9時間前", "約9分前", "約6分前", "1:16:27", "1:17:49", "1:22:14")   # c622

AXI.update({
    # ── 建物の歩み
    "build": dict(k="span", a="1979", b="1981", t="設計と建設", rec="AC p2023"),
    "done": dict(k="pt", at="1981", t="完成", rec=["TR p1005", "AC p2023"]),
    "y40": dict(k="br", a="1981", b="2021", rec=["MIN18 p4107", "GJ p3005"]),
    # ⚠️ 下見：右へ振ると「40年の点検の期限」が画面の右の外へ出た＝左へ（2018年の札の上の段）
    "due": dict(k="pt", at="2021", t="40年の点検の期限", rec=["MIN18 p4107", "GJ p3005"], anchor="end"),
    # ⑤c'（10-07）：c302「大改修」・c318「補修と防水」と同じ工事＝呼び方を「大改修」にそろえた（TR0236 major rehabilitation・c302 の語り）
    "fix": dict(k="span", a="1996", b="1997", t="大改修", rec="TR p1441"),
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
    # 🆕 ⑤b-6：cc17 追悼の灯（A12「the symbolic remembrance torch lit at 1:22 am on June 24」「July 20th at 8:03 pm」）
    "lit": dict(k="pt", at="2021-06-24", t="灯をともす（1:22）", rec="A12 p5101", lab=False, anchor="start"),
    "out": dict(k="pt", at="2021-07-20", t="灯を消す（20:03）", rec="A12 p5101", lab=False, anchor="end"),
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


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：量の型（棒）と箱の型（流れ図・書類の再現図・並べ図）・決め所の出どころの札── 19本目 ⑤b-6〜⑤b-8
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB・FORM_*・FL_*・FLP・CAUSE・QDOC・QWHO・QDATE_LB はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_QTY／check_boxes.REC_*＝§5b-88）＝回を替えたら両方を替える。
# 🆕 2026-10-06（19本目 ⑤b-6）：c408（工事の額）・c617（床の沈み）・ca07（柱にかけた重さ）。値と頁は ref/ep19/src/ep19_pages.txt で当てた＝
#   門番 check_qty.REC_QTY と照らす（門番の側にも別に持つ＝§5b-88）。群の名と行の名には数字を書かない（数は字幕＝§5b-9）
#   ・円は台本 §9 の式（1ドル≈109円＝2021年4月）・インチは×2.54・ポンドは×0.4536（棒は丸めない＝語りは「約」）
#   ・「〜を超える」（1,400万ドル）は棒をその数まで＝注で断る
#   ・🔴 ひざ・机・トラックは記録の値ではない＝棒にしない。目盛りに置いて注で「目安」と断る（c617＝目盛り 45・70／ca07＝20トンごと）
QG = {
    "cost": dict(id="cost", t="直す工事の額（億円）", ticks=(0, 5, 10, 15, 20)),
    "unit": dict(id="unit", t="部屋ごとの額（万円）", ticks=(0, 300, 600, 900, 1200)),
    "sink": dict(id="sink", t="床の沈み（センチ）", ticks=(0, 45, 70), rows=("少なく見て", "多く見て")),
    "load": dict(id="load", t="柱にかけた重さ（トン）", ticks=tuple(range(0, 301, 20))),
}
QB = {
    # c408：GJ p.18（p3021）「The proposed costs for building repairs were more than $14,000,000.」・MC18 p.1（p4001）「136-unit」
    "c_all": dict(k="bar", g="cost", t="全体", v=14e6 * 109 / 1e8, rec="GJ p3021"),
    "c_unit": dict(k="bar", g="unit", t="単純に割ると", v=14e6 * 109 / 136 / 1e4, rec=["GJ p3021", "MC18 p4001"], c="AMBER"),
    # c617：TR0348（p1348）「The total drop near grid point L-9.1 from the day before the collapse to 1:22:14 a.m. was about 18-27 inches.」
    "s_lo": dict(k="bar", g="sink", t="少なく見て", v=18 * 2.54, rec="TR p1348"),
    "s_hi": dict(k="bar", g="sink", t="多く見て", v=27 * 2.54, rec="TR p1348", c="AMBER"),
    # ca07：TR0302（p1302）「a vertical load of 650,000 pounds … representing the load in the column at the time of failure」
    "l_col": dict(k="bar", g="load", t="試験の柱", v=650000 * 0.4536 / 1000, rec="TR p1302", c="AMBER"),
}

# 🆕 2026-10-06（19本目 ⑤b-6）：書類の再現図・流れ図・並べ図。🔴 欄の値は原文の英語のまま（日本語は字幕だけ＝ルール 0b-33）・
#   欄の名は原文の文の言葉を日本語に・紙1枚に欄は4つまで（§5b-114⑤）・人の名前は出さない（議事録・手紙＝役職だけ）・
#   次のカットの語りにある事は書かない（ルール 0b-40⑤）：c403 の「とても良い状態に見える」（c404 の決め所）・cc08 の7月2日の手紙（cc09）。
#   値は ref/ep19/src/ep19_pages.txt の文字の層で当て、OCR が崩れた GJ は頁の画像の書き起こし（p9802・p9803）と照らした
_P4 = (100, 1820, 270, 840)    # 欄4つの紙（図の本体 210〜892 の内・「再現」の札は 214〜258）
_P3 = (100, 1820, 300, 760)
_P2 = (100, 1820, 330, 690)
# c212：議事録 p.7（MIN18 p4107＝p9805）「The 40 year certification for the building will be due in 2021.」／大陪審の報告 p.18（GJ p3021＝p9802）
#   「the Champlain Towers condo board hired an engineer to start the 40-year recertification process years before it was due」（紙2枚＝別の書類）
FORM_MIN40 = dict(title="理事会の議事録（2018年11月15日）", rec="MIN18 p4107", lw=150,
                  fields=[dict(t="40年の点検", v="will be due in 2021", rec="MIN18 p4107", late=True)])
FORM_GJ18 = dict(title="大陪審の報告", rec="GJ p3021", lw=150,
                 fields=[dict(t="管理組合", v="hired an engineer", rec="GJ p3021", late=True),
                         dict(t="始めた時期", v="years before it was due", rec="GJ p3021", late=True)])
# c309：調査の報告 p.1（MC18 p4001）「October 8, 2018」「Treasurer」「Structural Field Survey Report」・p.7（MC18 p4007＝p9804）
#   「the waterproofing below the Pool Deck & Entrance Drive」。🔴 会社と人の名前は出さない（あて先は役職だけ）
FORM_MC18 = dict(title="建物の調査の報告", rec=["MC18 p4001", "MC18 p4007"], paper=_P4, lw=170,
                 fields=[dict(t="日付", v="October 8, 2018", rec="MC18 p4001"),
                         dict(t="あて先", v="Treasurer", rec="MC18 p4001"),
                         dict(t="表題", v="Structural Field Survey Report", rec="MC18 p4001"),
                         dict(t="書いたこと", v="the waterproofing below the Pool Deck & Entrance Drive", rec="MC18 p4007", late=True)])
# c316：見積もり（EST18 p4318＝町が公開した転送メールの PDF の18頁の添付）「TOTAL SUMMARY OF REMEDIATION PROBABLE CONSTRUCTION COST
#   $9,128,433.60」。内わけは出さない（映像方針）
FORM_EST18 = dict(title="直す工事の見積もり", rec="EST18 p4318", paper=_P2, lw=150,
                  fields=[dict(t="合計", v="$9,128,433.60", rec="EST18 p4318", late=True)])
# c403：議事録 p.7（MIN18 p4107）「Structural engineer report was reviewed … although report was not in the format for the 40 year certification
#   he determined the necessary data was collected」。「it appears the building is in very good shape」は次の c404 の決め所＝書かない
FORM_MIN15 = dict(title="理事会の議事録（2018年11月15日）", rec="MIN18 p4107", paper=_P3, lw=150,
                  fields=[dict(t="見たもの", v="Structural engineer report was reviewed", rec="MIN18 p4107"),
                          dict(t="書式", v="report was not in the format for the 40 year certification", rec="MIN18 p4107", late=True),
                          dict(t="判断", v="the necessary data was collected", rec="MIN18 p4107", late=True)])
# c412：理事長の手紙（2021年4月）を大陪審の報告 p.18（GJ p3021）が引く「observable damage such as in the garage has gotten significantly worse
#   since the initial inspection」「would begin to multiply exponentially over the years」。🔴 名前は出さない（理事長＝役職）
FORM_LET21 = dict(title="理事長の手紙（2021年4月）", rec="GJ p3021", paper=_P2, lw=250,     # ⑤b-6 の下見：170 は欄の名が縮んだ
                  fields=[dict(t="目に見える傷み", v="has gotten significantly worse since the initial inspection", rec="GJ p3021", late=True),
                          dict(t="これから", v="would begin to multiply exponentially over the years", rec="GJ p3021", late=True)])
# c712（地図 → 書類の再現図＝§5b-116①：場所の記録は半径だけ）：郡の発表（B03 p5201）「Between 10 p.m. on Sunday, July 4, 2021 and 3 a.m. on Monday,
#   July 5」「a 300-foot radius around the center of the demolition」。屋内にいる区域（黄）は地図の画像だけ＝数の記録が無い＝書かない
FORM_B03 = dict(title="郡の発表（2021年7月4日）", rec="B03 p5201", paper=_P2, lw=250,     # ⑤b-6 の下見：190 は欄の名が縮んだ
                fields=[dict(t="取り壊し", v="Between 10 p.m. on Sunday, July 4, 2021 and 3 a.m. on Monday, July 5", rec="B03 p5201",
                             late=True),
                        dict(t="近づけない区域", v="a 300-foot radius around the center of the demolition", rec="B03 p5201", late=True)])
# cc08（数の比べ → 書類の再現図＝棒にする量が無い）：大陪審の報告 p.20（GJ p3023＝p9803）「Crestview Towers is a 10-story, 156-unit condominium
#   building.」「its 40-year recertification was due in 2012」「9 1/2 years overdue」（OCR は「9 %」＝頁の画像の書き起こし p9803 で読んだ）
FORM_CREST = dict(title="大陪審の報告（ほかの建物の例）", rec="GJ p3023", paper=_P3, lw=200,     # ⑤b-6 の下見：150 は欄の名が縮んだ
                  fields=[dict(t="建物", v="Crestview Towers is a 10-story, 156-unit condominium building.", rec="GJ p3023", late=True),
                          dict(t="40年の点検", v="its 40-year recertification was due in 2012", rec="GJ p3023", late=True),
                          dict(t="崩落のとき", v="9 1/2 years overdue", rec="GJ p3023", late=True)])
# cc14：州の法律 SB 4-D（A14 p6008・p6009）「three stories or more in height」「reaches 30 years of age」「within 3 miles of a coastline … reaches
#   25 years of age」「every 10 years thereafter」
FORM_SB4M = dict(title="州の法律 SB 4-D（節目の点検）", rec=["A14 p6008", "A14 p6009"], paper=_P4, lw=340,     # ⑤b-6 の下見：230 は縮んだ
                 fields=[dict(t="建物", v="three stories or more in height", rec="A14 p6008", late=True),
                         dict(t="最初の点検", v="reaches 30 years of age", rec="A14 p6008", late=True),
                         dict(t="海岸から3マイル以内", v="reaches 25 years of age", rec="A14 p6009", late=True),
                         dict(t="そのあと", v="every 10 years thereafter", rec="A14 p6008", late=True)])
# cc15：同じ法律（A14 p6037）「a. Roof.」「c. Floor.」「d. Foundation.」「h. Waterproofing and exterior painting.」「at least every 10 years」・
#   （A14 p6035）「Effective December 31, 2024, the members of a unit-owner controlled association may not determine to provide no reserves or
#   less reserves」
FORM_SB4R = dict(title="州の法律 SB 4-D（直すお金の備え）", rec=["A14 p6035", "A14 p6037"], paper=_P3, lw=340,     # ⑤b-6 の下見：230 は縮んだ
                 fields=[dict(t="調べるもの（一部）", v="Roof. … Floor. Foundation. … Waterproofing", rec="A14 p6037", late=True),
                         dict(t="調べる間隔", v="at least every 10 years", rec="A14 p6037", late=True),
                         dict(t="2024年12月31日から", v="may not determine to provide no reserves or less reserves", rec="A14 p6035",
                              late=True)])
# 流れ図（c203・c704・c806・c913・c914・c921・cb14・cc07・cc11・cc12・cc18）。箱の言葉は11字まで（門番 echo は12字から）・役職だけ（名前を出さない）・
#   赤を使わない。言葉と頁は門番 check_boxes の REC_OTHER_ROLE・REC_MECH・REC_CHIP と照らす
#   🔴 c704・cc07・cc18（地図 → 流れ図）＝資料に位置の値（距離・方角・座標）が無い＝§5b-116①（drift は門番 ③ を正直には通せない）
FL_DOCS = dict(heads=[], kind="この動画の資料")
FL_EMPTY = dict(heads=[])
FL_AC54 = dict(heads=[dict(id="h_ac", t="継ぎ目の壊れ（プールデッキ）", kind="head", x=(1180, 1790), y=(500, 580), rec="AC p2054")])
FL_AVE = dict(heads=[], kind="アベンチュラ市の決まり（2021年）")
FLP = {
    # c203：資料（c202 の語り）＝NIST の結果の動画（A04 p5001＝2026年6月22日・TR）・その文字起こし（TR）・諮問委員会の資料（AC p.1）・町が公開した記録
    #   （A12）／大陪審の報告（GJ p.1＝p3004・出た日＝表紙 p3001「FILED December 15, 2021」と州検事の声明 A16。⚠️ 表紙 p3001 は印字の頁が無い
#   ＝rec に書くと出典の行が「-2頁」になる）
    "d_vid": dict(k="role", id="d_vid", t="結果の動画（2026年6月）", y=430, pos=(130, 820), rec=["A04 p5001", "TR p1001"]),
    "d_tr": dict(k="role", id="d_tr", t="その文字起こし", y=550, pos=(130, 820), rec="TR p1001"),
    "d_ac": dict(k="role", id="d_ac", t="諮問委員会の資料（2026年9月）", y=670, pos=(130, 820), rec="AC p2001"),
    "d_town": dict(k="role", id="d_town", t="町が公開した記録", y=430, pos=(1100, 1790), rec="A12 p5101"),
    "d_gj": dict(k="role", id="d_gj", t="大陪審の報告（2021年12月）", y=550, pos=(1100, 1790), rec=["GJ p3004", "A16 p5801"]),
    # c704：町の警察の会報 p.2（B05 p5302）「The remainder of the condominium was evacuated and residents were escorted to the Surfside Community
    #   Center which later become the Family Reunification Center.」
    "e_res": dict(k="role", id="e_res", t="残った部分の住民", y=500, pos=(130, 700), rec="B05 p5302"),
    "e_cc": dict(k="role", id="e_cc", t="コミュニティセンター", y=500, pos=(1100, 1790), rec="B05 p5302"),
    # c806：TR0256「evaluated the demands on and capacity of the slab-column connections with three tools」・TR0257「finite element modeling;
    #   laboratory tests of slab-column connections; critical shear crack theory」
    "t_fem": dict(k="role", id="t_fem", t="コンピュータの模型", y=400, pos=(130, 700), rec="TR p1257"),
    "t_lab": dict(k="role", id="t_lab", t="実物大の試験", y=540, pos=(130, 700), rec="TR p1257"),
    "t_csct": dict(k="role", id="t_csct", t="ひびの理論", y=680, pos=(130, 700), rec="TR p1257"),
    "t_eval": dict(k="role", id="t_eval", t="継ぎ目の力と強さ", y=540, pos=(1180, 1790), rec="TR p1256"),
    # c913・c914：AC p.54（p2054）「Design understrength (largest, pervasive)」「Deviations in as-built construction from design documents and
    #   standards (pervasive)」「Heavier, more extensive planters」「Added fill and paving」「Degradation over time」・TR0277〜0280
    "a_des": dict(k="role", id="a_des", t="設計の強さの不足", y=330, pos=(110, 640), rec=["AC p2054", "TR p1279"]),
    "a_dev": dict(k="role", id="a_dev", t="図面とのずれ", y=450, pos=(110, 640), rec=["AC p2054", "TR p1279"]),
    "a_pl": dict(k="role", id="a_pl", t="重いプランター", y=560, pos=(110, 640), rec=["AC p2054", "TR p1280"]),
    "a_fill": dict(k="role", id="a_fill", t="足した砂と敷石", y=670, pos=(110, 640), rec=["AC p2054", "TR p1280"]),
    "a_deg": dict(k="role", id="a_deg", t="年月の傷み", y=780, pos=(110, 640), rec=["AC p2054", "TR p1280"]),
    # c921：AC p.61（p2061）「The requirements for recertification of structures in Florida are laudable, but they contain no requirements for
    #   establishing confidence in the original design and construction.」／40年の点検で見るもの＝調査の報告 p.1（MC18 p4001）「to understand
    #   and document the extent of structural issues that require repair」
    "r_cert": dict(k="role", id="r_cert", t="40年の点検（フロリダ）", y=470, pos=(110, 640), rec="AC p2061"),
    "r_dmg": dict(k="role", id="r_dmg", t="傷みと直す所", y=470, pos=(1240, 1790), rec="MC18 p4001"),
    "r_orig": dict(k="role", id="r_orig", t="建てたときの設計と工事", y=670, pos=(1240, 1790), rec="AC p2061"),
    # cb14：TR0476「it was the low margins of safety and degradation that started the failure in the pool deck」／TR0454（87パークの揺れ）・
    #   TR0465（基礎・陥没や沈み・嵐・衝突・爆発ほか）
    "o_mg": dict(k="role", id="o_mg", t="継ぎ目の余裕の少なさ", y=450, pos=(110, 760), rec="TR p1476"),
    "o_deg": dict(k="role", id="o_deg", t="傷み", y=570, pos=(110, 760), rec="TR p1476"),
    "x_vib": dict(k="role", id="x_vib", t="となりの工事の揺れ", y=450, pos=(1100, 1790), rec="TR p1454"),
    "x_gnd": dict(k="role", id="x_gnd", t="地面の沈みや空洞", y=570, pos=(1100, 1790), rec="TR p1465"),
    "x_ext": dict(k="role", id="x_ext", t="嵐・衝突・爆発", y=690, pos=(1100, 1790), rec="TR p1465"),
    # cc07：大陪審の報告 p.20（GJ p3023）「Following the collapse, the City of North Miami Beach … decided to conduct an audit of all buildings and
    #   structures five stories or higher … due or past due for their 40-year recertification」
    "n_col": dict(k="role", id="n_col", t="サーフサイドの崩落", y=520, pos=(110, 560), rec="GJ p3023"),
    "n_nmb": dict(k="role", id="n_nmb", t="ノースマイアミビーチ市", y=520, pos=(700, 1180), rec="GJ p3023"),
    "n_aud": dict(k="role", id="n_aud", t="5階以上の建物を調べる", y=520, pos=(1320, 1800), rec="GJ p3023"),
    # cc11：大陪審の報告 p.20（GJ p3023＝監査・7月2日に報告が市へ・すぐに退去）・p.22（GJ p3025「no notification at all was provided to the
    #   Local Building Official regarding Crestview Towers」）
    "w_aud": dict(k="role", id="w_aud", t="市が遅れを調べる", y=690, pos=(110, 560), rec="GJ p3023"),
    "w_rep": dict(k="role", id="w_rep", t="報告が市に届く", y=690, pos=(690, 1140), rec="GJ p3023"),
    "w_out": dict(k="role", id="w_out", t="すぐに退去", y=690, pos=(1290, 1800), rec="GJ p3023"),
    "w_old": dict(k="role", id="w_old", t="それまでの報告", y=420, pos=(110, 640), rec="GJ p3025"),
    "w_city": dict(k="role", id="w_city", t="市の建築の担当", y=420, pos=(1290, 1800), rec="GJ p3025"),
    # cc12：大陪審の報告 p.21〜22（GJ p3024「provide a copy of any engineering report … to the City within forty-eight hours of receiving such a
    #   report」・p3025「Ordinance No. 2021-13」）
    "v_eng": dict(k="role", id="v_eng", t="技師の報告", y=520, pos=(110, 560), rec="GJ p3024"),
    "v_board": dict(k="role", id="v_board", t="管理組合", y=520, pos=(700, 1100), rec="GJ p3024"),
    "v_city": dict(k="role", id="v_city", t="市", y=520, pos=(1420, 1800), rec="GJ p3024"),
    # cc18：町の発表（A13 p5102）「At the Special Commission Meeting held on August 6, the Surfside Town Commission gave final approval」「the street
    #   end park at 88 th Street」「For five years, the Committee worked in close partnership with victims’ families, survivors, first responders,
    #   and residents」
    "m_fam": dict(k="role", id="m_fam", t="家族", y=360, pos=(110, 500), rec="A13 p5102"),
    "m_surv": dict(k="role", id="m_surv", t="生き残った人", y=480, pos=(110, 500), rec="A13 p5102"),
    "m_resc": dict(k="role", id="m_resc", t="救助の人たち", y=600, pos=(110, 500), rec="A13 p5102"),
    "m_res": dict(k="role", id="m_res", t="住民", y=720, pos=(110, 500), rec="A13 p5102"),
    "m_com": dict(k="role", id="m_com", t="記念の委員会", y=540, pos=(680, 1120), rec="A13 p5102"),
    "m_ok": dict(k="role", id="m_ok", t="町の議会の最終の承認", y=540, pos=(1300, 1800), rec="A13 p5102"),
}


def fl(name, **kw):
    return dict(FLP[name], **kw)


# 並べ図（cb09・cb10＝NIST が崩れに大きくは関わっていないとしたもの／cc05＝大陪審の勧告の6つのねらい／cc22＝勧告の題目の候補）
CAUSE = {
    # cb09・cb10：TR0465（p1465）「foundation failure, sinkholes or differential settlement, hurricanes and storm surge effects, impulsive loads such as
    #   vehicle impact, explosion or items dropped from a crane, and accidental loads or overloads caused by the roof repair and roof anchor project」
    "n_found": dict(k="item", t="基礎の壊れ", rec="TR p1465"),
    "n_sink": dict(k="item", t="陥没や沈み", rec="TR p1465"),
    "n_storm": dict(k="item", t="ハリケーンと高潮", rec="TR p1465"),
    "n_car": dict(k="item", t="車の衝突", rec="TR p1465"),
    "n_blast": dict(k="item", t="爆発", rec="TR p1465"),
    "n_crane": dict(k="item", t="クレーンの落下物", rec="TR p1465"),
    "n_roof": dict(k="item", t="屋上の工事の重さ", rec="TR p1465"),
    # cc05：大陪審の報告 p.1（GJ p3004）「Our recommendations included below are designed to 1) improve the ability of governmental officials to timely
    #   identify and address buildings … 2) highlight environmental issues in South Florida … 3) suggest ways to identify such deterioration, ameliorate
    #   it … 4) … better compliance and timely submittals … 5) give building officials more authority/power … 6) … electronic posting and on-line
    #   access」
    "g_find": dict(k="item", t="役所が早く見つけて動く", rec="GJ p3004"),
    "g_env": dict(k="item", t="南フロリダの環境と傷み", rec="GJ p3004"),
    "g_fix": dict(k="item", t="傷みを見つけて直す", rec="GJ p3004"),
    "g_due": dict(k="item", t="報告を期限どおりに", rec="GJ p3004"),
    "g_power": dict(k="item", t="役所に強い力", rec="GJ p3004"),
    "g_web": dict(k="item", t="住民がネットで読める", rec="GJ p3004"),
    # cc22：諮問委員会の資料 p.17（AC p2017）「Quality of Design & Construction / Code Enforcement / Codes & Standards for New Buildings / Records
    #   Retention Policies & Building Inspections / Assessment, Management & Maintenance of Existing Buildings / Education & Training」
    "k_qual": dict(k="item", t="設計と工事の質", rec="AC p2017"),
    "k_enf": dict(k="item", t="決まりを守らせる", rec="AC p2017"),
    "k_new": dict(k="item", t="新しい建物の決まり", rec="AC p2017"),
    "k_rec": dict(k="item", t="記録の保管と点検", rec="AC p2017"),
    "k_old": dict(k="item", t="今ある建物の手入れ", rec="AC p2017"),
    "k_edu": dict(k="item", t="教育と訓練", rec="AC p2017"),
}


# 🆕 2026-10-07（19本目 ⑤b-8）：19本目の資料の名（札の「記録」の欄）と出た時（「公表」の欄）。
#    ⚠️ 名と年月を1つの値にすると、札の幅（全角12字＝`titan_fig.wrap(t, 12)`）で**かっこの中で割れた**
#       （「大陪審の報告（2021年｜12月）」「NIST｜の技術的知見の動画｜（2026年6月）」）＝名と年月を別の欄に分けた。
#       名は出典の行（credits.json）・語りの呼び名にそろえた。NIST は「著者」の欄（QWHO）
#    🔴 §0b（次の回は空に）：QDOC・QWHO。頁の欄＝大陪審の報告は**印字の頁**（PDF の頁＝印字＋3）・モラビトの報告は印字の「Page 7」・
#       議事録は PDF の頁・諮問委員会の資料は印字＝PDF の頁・技術的知見の動画はスライドの番号（語りの文字起こしは頁が無い＝None）
#    決め所19の原文照合（⑤b-8）＝台本 §2 の英語が通し頁ファイルのその頁に 19/19（a〜z0〜9 にそろえて照合・陰性対照＝別の頁では外れる）・
#       ★の行＝台本 §2 の言葉＝SPEC の phrase（折った行をつないだもの）
QDOC = {"GJ": ("大陪審の報告", "2021年12月"), "MC18": ("モラビトの調査の報告", "2018年10月8日"),
        "MIN18": ("管理組合の会議の議事録", "2018年11月15日"),
        "TR": ("技術的知見の動画", "2026年6月"), "AC": ("諮問委員会の資料", "2026年9月")}
QWHO = {"TR": "NIST", "AC": "NIST"}
# ⑤c'（10-07）：モラビトの報告は理事会の会計係に渡された私的な文書（c309 の語り）＝「公表」でなく「日付」（c311）
QDATE_LB = {"MIN18": "会議", "MC18": "日付"}


def qrows(doc, page, *extra):
    """決め所の出どころの札の rows＝extra（(欄, 値) の組＝箇所・話した人・日付）＋記録＋著者＋公表＋頁。
    page は画面の頁の字（None＝頁の欄なし）。欄は4つまで＝5つ目になる「公表」は落とす（札の高さ 612px に収める）"""
    import jiko_style as J
    name, when = QDOC[doc]
    rows = [(k, v, J.LINE) for k, v in extra]
    rows.append(("記録", name, J.INK_W))
    if doc in QWHO:
        rows.append(("著者", QWHO[doc], J.LINE))
    if len(rows) + bool(page) < 4:
        rows.append((QDATE_LB.get(doc, "公表"), when, J.LINE))
    if page:
        rows.append(("頁", page, J.TICK))
    return rows


# `apply()` が cuts.ss に差し込む名の全部（上の値と関数＝ss から移したもの）。ここに無い名は ss に置かない
#   （`AXI` は ss に空の `AXI = {}` が残る＝見本の AXI（19本目の項目つき）を差し込む）
SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "_A1_ASSUME", "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "TL_NOTE", "ORDER_NOTE", "AX_LIFE", "AX_RUST", "AX_REP",
            "AX_21", "AX_NIGHT", "AX_CALL", "AX_SEARCH", "AX_NIST", "AX_CODE", "AX_SALE", "AX_TORCH", "SIGNS", "ALL_SIGNS", "QG", "QB", "_P4", "_P3",
            "_P2", "FORM_MIN40", "FORM_GJ18", "FORM_MC18", "FORM_EST18", "FORM_MIN15", "FORM_LET21", "FORM_B03", "FORM_CREST", "FORM_SB4M",
            "FORM_SB4R", "FL_DOCS", "FL_EMPTY", "FL_AC54", "FL_AVE", "FLP", "fl", "CAUSE", "QDOC", "QWHO", "QDATE_LB", "qrows")


# ══════════════════════════════════════════════════════════
#  titan_fig.GEO から：19本目の地点＝無い
# ══════════════════════════════════════════════════════════
#   19本目は `titan_fig.GEO` に地点を足さなかった（地図 drift を使わず、案C の A1〜A3 と図解・模式図 mech19 に替えた）。
#   `70c7e51` の `titan_fig.GEO` は `275c4d5`（18本目の値を移した直後）と同じ（差分は模式図 `m19` の関数と quote・panel の描き方だけ）
GEO = {}


# ══════════════════════════════════════════════════════
#  門番の記録の表（19本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════
# 以下の表は、門番5本の本番の置き場にあった19本目の値を1文字も変えずに写したもの（GATES が門番ごとにまとめる）

# ── check_axis ──
# ✅ 2026-10-06（19本目 サーフサイド ⑤b-5）：19本目の値を入れた。原文＝ref/ep19/src/ep19_pages.txt（頁の番号は cuts/ss.REC_DOCS の通し番号＝
#    TR p1NNN＝NIST の技術的知見の動画の語りの行 NNN・AC p20NN＝諮問委員会の資料の PDF 頁・GJ p30NN＝大陪審の報告の PDF 頁（印字の頁＋3）・
#    MC18 p400N＝2018年10月の調査の報告・MIN18 p410N＝2018年11月15日の議事録の PDF 頁・A12 p5101＝町の頁・B01 p56NN＝GAO・B02 p57NN＝FEMA・
#    B08 p5005＝NIST の発表 2024-11-21・A17 p70NN／A18 p71NN／A19 p72NN＝裁判所の命令と告知）。引いた原文は値の右の注
REC_AXIS = {
    # ── 建物の歩み（c210・c302・c318・c918・c919）
    "1979": {"AC p2023"},                   # AC p.23 の年表「CTS Design & Construction 1979-1981」
    "1981": {"AC p2023", "TR p1005", "GJ p3005", "TR p1278", "TR p1281"},   # 同「1979-1981」・TR0005「had stood … since 1981」・
    #   GJ p.2「1981, making the 12-story condo 40 [year]s old」・TR0281「from the time construction was complete」・TR0278「before the building was even occupied」
    "1996": {"TR p1441", "TR p1236"},       # TR0441「structural repairs and waterproofing were conducted in 1996 and '97」・TR0236「15 years after the building was constructed」（1981＋15）
    "1997": {"TR p1441"},                   # 同「in 1996 and '97」
    "2018-10-08": {"MC18 p4001", "MC18 p4007", "GJ p3020"},   # 調査の報告「October 8, 2018」・GJ p.17「as early as October 8, 2018」
    "2021": {"MIN18 p4107", "GJ p3005"},    # 議事録 p.7「The 40 year certification for the building will be due in 2021」・GJ p.2 の40年の点検
    "2021-06-24": {"A12 p5101", "GJ p3004"},   # 町の頁「the Champlain Towers South building collapse of June 24, 2021」・GJ p.1「June 24, 2021」
    # ── 報告のあと（c401・c409・c415・c418）
    "2018-11-15": {"MIN18 p4106", "GJ p3020"},  # 議事録「November 15, 2018 at 7:00 pm」・GJ p.17「a month later, on November 15, 2018」
    "2021-04": {"GJ p3021"},                # GJ p.18「In April 2021, more than 29 months after the engineer's report was received」・「the April 2021 letter from the then Board president」
    "2021-06-11": {"GJ p3021"},             # GJ p.18「Thirteen days after the Board was to hold a meeting to open the bids …, the building collapsed」（6月24日の13日前）
    # ── 最後の3週間（c523・c622＝並び）。TR0156〜0160 のまとめ・TF p9061 のスライドの並べ方
    "約3週間前": {"TR p1156", "TR p1016"},   # TR0156「approximately three weeks before the collapse」・TR0016「about three weeks before the collapse」
    "約1週間前": {"TR p1157", "TR p1095"},   # TR0157「Two weeks later」（3週間前の2週間後）・TR0095「one week before the tower collapsed」
    "約17時間前": {"TR p1158"},              # TR0158「Then 17 hours before and again 11 hours before the collapse」
    "約9時間前": {"TR p1159"},               # TR0159「Then nine hours before the collapse, a water leak」
    "約3時間前": {"TR p1160"},               # TR0160「just three hours before the tower collapsed」
    "約9分前": {"TR p1161"},                 # TR0161「At approximately nine minutes before the tower collapsed, the last vehicle entered」
    "約6分前": {"TR p1170"},                 # TR0170「At approximately six minutes prior to the tower collapsing」
    "1:16:27": {"TR p1177"},                 # TR0177「at 1:16 and 27 seconds a.m.」（最初の 911 の電話）
    "1:17:49": {"TR p1189"},                 # TR0189「at 1:17 and 49 seconds a.m.」（2回目の電話）
    "1:22:14": {"TR p1347", "TR p1348"},     # TR0347「the rate of drop increased dramatically at about 1:22:14」
    # ── 崩れる前の数分（c602・c603・c605・c608＝時刻の帯・基準 1:22 からの「約○分前」）
    "1:22": {"A12 p5101"},                   # 町の頁＝崩落の時刻（台本 §1-5「the exact time of the collapse」）
    "約-9": {"TR p1161"},                    # 上の「約9分前」と同じ（最後の車）
    "約-9〜-8": {"TR p1167"},                # TR0167「approximately eight to nine minutes prior to the tower collapsing」（音）
    "約-7": {"TR p1169"},                    # TR0169「Approximately seven minutes before the tower collapsed, the building's own fire alarm logged a trouble signal」
    "約-6": {"TR p1170"},                    # 上の「約6分前」と同じ（地上の駐車場）
    "約-5": {"TR p1181", "TR p1183"},        # TR0181「approximately five minutes prior」・TR0183「from south to north, one bay at a time」
    "1:17:55": {"TR p1190"},                 # TR0190「a few seconds later at 1:17 and 55 seconds a.m.」（火災報知器の見張りの会社）
    # ── 捜索と調査（c714・c719）
    "2021-07-20": {"A12 p5101"},             # 町の頁「8:03p.m., the exact time when the final person was recovered on July 20, 2021」
    "2021-06-25": {"B02 p5702", "B08 p5005"},   # FEMA「On June 25, NIST initially deployed a team of six scientists and engineers」・B08「arrived in Surfside on June 25, 2021」
    "2021-06-30": {"B02 p5702", "B01 p5605", "B08 p5005"},   # FEMA「On June 30, the agency announced」・GAO「On June 30, 2021, NIST announced」
    "2022-01-28": {"B08 p5005"},             # B08「when the evidence custody and control transferred to NIST on Jan. 28, 2022」
    # ── 決まり（ca20）
    "1989": {"AC p2075", "AC p2076"},        # AC p.75・76「Starting in 1989, versions of the building code for structural concrete required structural integrity reinforcement」
    "2025": {"AC p2076"},                    # AC p.76「The current structural integrity provisions in ACI 318-25」（318-25＝2025年の版）
    # ── 裁判所（cc20）
    "2022-06-01": {"A18 p7104"},             # 売却を認める命令「DONE and ORDERED … on this 1st day of June, 2022」
    "2022-06-24": {"A17 p7015"},             # 最終の命令「DONE and ORDERED … on this 24th day of June, 2022」
    "2022-07-27": {"A19 p7201"},             # 売却の告知「he has concluded the sale」「Dated: July 27, 2022」
}

# 並び order の基準の時刻（分）。🔴 19本目の記録の値（町の頁の崩落の時刻）＝本番の check_axis.ORDER_REF_MIN は None（空）
# 🆕 19本目 ⑤b-5：並び（order）の値を「基準からの秒」に読む（門番の側の読み方）。基準＝町の頁の崩落の時刻 1:22（A12）
ORDER_REF_MIN = 82          # 1:22

# ── check_qty ──
REC_QTY = {          # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
    # 🆕 2026-10-06（19本目 ⑤b-6）：原文 ref/ep19/src/ep19_pages.txt で当てた（型の側 ss.QB とは別に持つ）。換算は台本 §9 の式を門番の側でも持つ
    #   （語りの「約」の丸めで描くと鳴る）
    # c408：GJ p.18（p3021「more than $14,000,000」）×109円（2021年4月）・136戸（MC18 p.1＝p4001「136-unit」）
    ("直す工事の額（億円）", "全体"): (14e6 * 109 / 1e8, {"GJ p3021"}),
    ("部屋ごとの額（万円）", "単純に割ると"): (14e6 * 109 / 136 / 1e4, {"GJ p3021", "MC18 p4001"}),
    # c617：TR0348（p1348「about 18-27 inches」）×2.54
    ("床の沈み（センチ）", "少なく見て"): (18 * 2.54, {"TR p1348"}),
    ("床の沈み（センチ）", "多く見て"): (27 * 2.54, {"TR p1348"}),
    # ca07：TR0302（p1302「a vertical load of 650,000 pounds」）×0.4536÷1000
    ("柱にかけた重さ（トン）", "試験の柱"): (650000 * 0.4536 / 1000, {"TR p1302"}),
}

# ── check_boxes ──
# 🆕 2026-10-06（19本目 ⑤b-6）：19本目の箱の言葉と頁（流れ図・書類の再現図・並べ図）。原文 ref/ep19/src/ep19_pages.txt で当てた
#    （型の側 ss.FLP・FORM_*・CAUSE とは別に持つ）。OCR が崩れた大陪審の報告は頁の画像の書き起こし p9802・p9803 と照らした
REC_OTHER_ROLE = {    # 流れ図の「role」の箱＝役職でない言葉（報告書の文の言葉）→ 頁の集合
    # c203：NIST の結果の動画（A04＝2026-06-22・TR）・文字起こし（TR）・諮問委員会の資料（AC p.1）・町の記録（A12）・大陪審の報告（GJ の表紙
    #   p3001「FILED December 15, 2021」・州検事の声明 A16）
    "結果の動画（2026年6月）": {"A04 p5001", "TR p1001"}, "その文字起こし": {"TR p1001"},
    "諮問委員会の資料（2026年9月）": {"AC p2001"}, "町が公開した記録": {"A12 p5101"},
    "大陪審の報告（2021年12月）": {"GJ p3004", "A16 p5801"},
    # c704：B05 p.2（p5302）「residents were escorted to the Surfside Community Center which later become the Family Reunification Center」
    "残った部分の住民": {"B05 p5302"}, "コミュニティセンター": {"B05 p5302"},
    # c806：TR0256（demands on and capacity of the slab-column connections with three tools）・TR0257（3つの道具）
    "コンピュータの模型": {"TR p1257"}, "実物大の試験": {"TR p1257"}, "ひびの理論": {"TR p1257"}, "継ぎ目の力と強さ": {"TR p1256"},
    # c913・c914：AC p.54（原因と後押しの5つ）・TR0279・TR0280
    "設計の強さの不足": {"AC p2054", "TR p1279"}, "図面とのずれ": {"AC p2054", "TR p1279"}, "重いプランター": {"AC p2054", "TR p1280"},
    "足した砂と敷石": {"AC p2054", "TR p1280"}, "年月の傷み": {"AC p2054", "TR p1280"},
    # c921：AC p.61（the requirements for recertification … contain no requirements for establishing confidence in the original design and
    #   construction）・40年の点検の調べ＝MC18 p.1（structural issues that require repair）
    "40年の点検（フロリダ）": {"AC p2061"}, "傷みと直す所": {"MC18 p4001"}, "建てたときの設計と工事": {"AC p2061"},
    # cb14：TR0476（low margins of safety and degradation that started the failure）・TR0454（87 Park の揺れ）・TR0465（基礎・沈み・嵐・衝突・爆発）
    "継ぎ目の余裕の少なさ": {"TR p1476"}, "傷み": {"TR p1476"}, "となりの工事の揺れ": {"TR p1454"}, "地面の沈みや空洞": {"TR p1465"},
    "嵐・衝突・爆発": {"TR p1465"},
    # cc07：GJ p.20（p3023）＝ノースマイアミビーチ市の監査（five stories or higher・40-year recertification）
    "サーフサイドの崩落": {"GJ p3023"}, "ノースマイアミビーチ市": {"GJ p3023"}, "5階以上の建物を調べる": {"GJ p3023"},
    # cc11：GJ p.20（p3023＝監査・報告が市へ・すぐに退去）・p.22（p3025「no notification at all was provided to the Local Building Official」）
    "市が遅れを調べる": {"GJ p3023"}, "報告が市に届く": {"GJ p3023"}, "すぐに退去": {"GJ p3023"}, "それまでの報告": {"GJ p3025"},
    "市の建築の担当": {"GJ p3025"},
    # cc12：GJ p.21（p3024「a copy of any engineering report … to the City within forty-eight hours」）
    "技師の報告": {"GJ p3024"}, "管理組合": {"GJ p3024"}, "市": {"GJ p3024"},
    # cc18：A13（p5102）final approval・88 th Street・families, survivors, first responders, and residents
    "家族": {"A13 p5102"}, "生き残った人": {"A13 p5102"}, "救助の人たち": {"A13 p5102"}, "住民": {"A13 p5102"},
    "記念の委員会": {"A13 p5102"}, "町の議会の最終の承認": {"A13 p5102"},
}
REC_MECH = {          # 流れ図に出してよい言葉のうち、役職・罪名でないもの（仕組み・鎖・問いの箱と矢印の札）
    # 🆕 19本目 ⑤b-6：左上の札（kind）・群の名（grp）・見出しの箱（heads）・矢印の札（lab）
    "この動画の資料", "国の研究所 NIST", "郡と町",          # c203（c202 の語り・A04・A12・GJ）
    "避難",                                               # c704（B05 p.2 evacuated）
    "継ぎ目の壊れ（プールデッキ）",                         # c913・c914 の見出しの箱（AC p.54 Initial Failures in Pool Deck）
    "見る",                                               # c921（MC18 p.1＝40年の点検の調べ）
    "起こり", "大きくは関わっていない",                     # cb14（TR0476 started the failure・TR0454／TR0465 did not contribute significantly）
    "知らされていない",                                     # cc11（GJ p.22 no notification at all）
    "アベンチュラ市の決まり（2021年）", "48時間以内に写し",   # cc12（GJ p.21〜22＝Ordinance No. 2021-13・forty-eight hours）
}
REC_CHIP = {          # 札（chip）の言葉 → 頁の集合
    "のちに家族の再会の場所": {"B05 p5302"},             # c704（later become the Family Reunification Center）
    "最も大きく、広い範囲": {"AC p2054"},                 # c914（Design understrength (largest, pervasive)）
    "ほめるべき仕組み（NIST）": {"AC p2061"},             # c921（are laudable）
    "確かめる決まりが無い": {"AC p2061"},                 # c921（they contain no requirements for establishing confidence in the original …）
    "40年の点検の遅れ": {"GJ p3023"},                     # cc07（due or past due for their 40-year recertification）
    "88番通りの端の公園": {"A13 p5102"},                  # cc18（the street end park at 88 th Street）
    "5年かけた形づくり": {"A13 p5102"},                   # cc18（For five years, the Committee worked …）
}
REC_FORM = {          # 書類の再現図（表題 → dict(fields・ends・values＝記録の文にある値だけ・rec＝頁の集合)）
    # c212・c403：議事録 p.7（MIN18 p4107＝頁の画像の書き起こし p9805）。同じ表題の紙が2つのカットにある＝欄は合わせて持つ
    "理事会の議事録（2018年11月15日）": dict(
        fields={"40年の点検", "見たもの", "書式", "判断"}, ends=set(), rec={"MIN18 p4107"},
        values={"40年の点検": "will be due in 2021", "見たもの": "Structural engineer report was reviewed",
                "書式": "report was not in the format for the 40 year certification", "判断": "the necessary data was collected"}),
    # c212：GJ p.18（p3021＝p9802「hired an engineer to start the 40-year recertification process years before it was due」）
    "大陪審の報告": dict(fields={"管理組合", "始めた時期"}, ends=set(), rec={"GJ p3021"},
                     values={"管理組合": "hired an engineer", "始めた時期": "years before it was due"}),
    # c309：MC18 p.1（p4001）・p.7（p4007＝p9804）
    "建物の調査の報告": dict(
        fields={"日付", "あて先", "表題", "書いたこと"}, ends=set(), rec={"MC18 p4001", "MC18 p4007"},
        values={"日付": "October 8, 2018", "あて先": "Treasurer", "表題": "Structural Field Survey Report",
                "書いたこと": "the waterproofing below the Pool Deck & Entrance Drive"}),
    # c316：見積もり（EST18 p4318「TOTAL SUMMARY OF REMEDIATION PROBABLE CONSTRUCTION COST $9,128,433.60」）
    "直す工事の見積もり": dict(fields={"合計"}, ends=set(), rec={"EST18 p4318"}, values={"合計": "$9,128,433.60"}),
    # c412：GJ p.18（p3021）が引く2021年4月の手紙
    "理事長の手紙（2021年4月）": dict(
        fields={"目に見える傷み", "これから"}, ends=set(), rec={"GJ p3021"},
        values={"目に見える傷み": "has gotten significantly worse since the initial inspection",
                "これから": "would begin to multiply exponentially over the years"}),
    # c712：郡の発表（B03 p5201）
    "郡の発表（2021年7月4日）": dict(
        fields={"取り壊し", "近づけない区域"}, ends=set(), rec={"B03 p5201"},
        values={"取り壊し": "Between 10 p.m. on Sunday, July 4, 2021 and 3 a.m. on Monday, July 5",
                "近づけない区域": "a 300-foot radius around the center of the demolition"}),
    # cc08：GJ p.20（p3023＝p9803「9 1/2 years overdue」）
    "大陪審の報告（ほかの建物の例）": dict(
        fields={"建物", "40年の点検", "崩落のとき"}, ends=set(), rec={"GJ p3023"},
        values={"建物": "Crestview Towers is a 10-story, 156-unit condominium building.",
                "40年の点検": "its 40-year recertification was due in 2012", "崩落のとき": "9 1/2 years overdue"}),
    # cc14：SB 4-D（A14 p6008・p6009）
    "州の法律 SB 4-D（節目の点検）": dict(
        fields={"建物", "最初の点検", "海岸から3マイル以内", "そのあと"}, ends=set(), rec={"A14 p6008", "A14 p6009"},
        values={"建物": "three stories or more in height", "最初の点検": "reaches 30 years of age",
                "海岸から3マイル以内": "reaches 25 years of age", "そのあと": "every 10 years thereafter"}),
    # cc15：SB 4-D（A14 p6037＝(g) a.〜i. と at least every 10 years・p6035＝Effective December 31, 2024 …）
    "州の法律 SB 4-D（直すお金の備え）": dict(
        fields={"調べるもの（一部）", "調べる間隔", "2024年12月31日から"}, ends=set(), rec={"A14 p6035", "A14 p6037"},
        values={"調べるもの（一部）": "Roof. … Floor. Foundation. … Waterproofing", "調べる間隔": "at least every 10 years",
                "2024年12月31日から": "may not determine to provide no reserves or less reserves"}),
}
REC_CAUSE = {         # 並べ図の項目 → 頁
    # cb09・cb10：TR0465（did not contribute significantly）
    "基礎の壊れ": {"TR p1465"}, "陥没や沈み": {"TR p1465"}, "ハリケーンと高潮": {"TR p1465"}, "車の衝突": {"TR p1465"},
    "爆発": {"TR p1465"}, "クレーンの落下物": {"TR p1465"}, "屋上の工事の重さ": {"TR p1465"},
    # cc05：GJ p.1（p3004＝勧告のねらい 1)〜6)）
    "役所が早く見つけて動く": {"GJ p3004"}, "南フロリダの環境と傷み": {"GJ p3004"}, "傷みを見つけて直す": {"GJ p3004"},
    "報告を期限どおりに": {"GJ p3004"}, "役所に強い力": {"GJ p3004"}, "住民がネットで読める": {"GJ p3004"},
    # cc22：AC p.17（p2017＝Potential Topics of NCSTAR Recommendations）
    "設計と工事の質": {"AC p2017"}, "決まりを守らせる": {"AC p2017"}, "新しい建物の決まり": {"AC p2017"},
    "記録の保管と点検": {"AC p2017"}, "今ある建物の手入れ": {"AC p2017"}, "教育と訓練": {"AC p2017"},
}

# ── check_mech ──
# 🔴 記録の値は門番の側に持つ（§5b-88）。描く側の表（mech19.CAND・AROUND・CODE_DOTS・CORE・CV・RB_C・JO_TIES…）を書き換えると鳴る。
#    位置の名（「K-13.1」）は NIST の発表のスライド（TF のコマ）から読んだ。厚さ・本数・割合は語り（TR）と諮問委員会の資料（AC）
REC_M19 = dict(
    cand=({"K-13.1", "L-13.1", "M-13.1", "K-15", "L-15", "M-15"}, "TF p9039（スライド48・TR0105＝six locations）"),
    first2=({"K-13.1", "L-13.1"}, "TR p1106（K-13.1 and L-13.1 outlined in red）"),
    around=({"I-12.1", "K-11.1", "L-11.1", "M-13.1", "K-15", "L-15"}, "TF p9052（スライド56＝丸い印の柱）"),
    code_red=({"K-13.1", "L-13.1", "M-13.1", "G.1-15", "I-15", "K-15", "L-15", "M-15"}, "TF p9082（スライド74＝severe）"),
    code_yel=({"N-13.1", "O-13.1", "O.1-13.1", "N-15"}, "TF p9082（スライド74＝moderate）"),
    leak=(("M", "N"), ("11.1", "13.1"), "TF p9057（スライド58＝M と N のあいだ・11.1 の南の楕円）"),
    water=("L-13.1", "TR p1132（grid point L-13.1）"), gate_col=("K", "TR p1123（K-13.1 の近くの門）"),
    cam_move=({"L-8", "L-9.1"}, "TR p1344（L-9.1 and L-8）"), cam_still=({"M-8", "M-9.1"}, "TR p1344（columns on grid line M＝stationary）"),
    cam_grid=(dict(L=640.0, M=710.0, **{"8": 352.0, "9.1": 420.0}), "TF p9134（スライド123 の平面＝1200px の縮小の座標）"),
    hall=({"K", "L"}, {"I"}, "TR p1354（sag around grid lines K and L）・TF p9134（I は No movement）"),
    core=((2.125, 1.375, 1.25), "TF p9090（スライド79＝2-1/8・1-3/8・1-1/4 in.）"),
    cover=((0.75, 2.0), "TR p1221（3/4 of an inch・about 2 inches）"),
    over=((4, 2), "TF p9085（スライド76＝only 2 rather than 4 top bars）"),
    space=((1.20, 1.40), "TR p1229（about 20% to 40% wider）"),
    strength=((6000.0, 4000.0), "AC p2065（Column 6000 psi・Floor 4000 psi）"),
    clock={"1:18:18", "1:21:55", "1:22:04", "1:22:14", "1:22:15"},       # 🆕 ⑤b-6：1:22:14＝TR p1347・p1348（c615）
    # 🆕 ⑤b-6（2026-10-06）：余裕（c306）・床の下がり（c615）・2本の線（c815〜c817）
    margin=("TR p1018（support much more load than they are expected to bear）・TR p1470（extra capacity … beyond the loads）"),
    drop_more=(("9.1", "8"), "TR p1347（The slab near column L-9.1 dropped more than the slab at L-8）"),
    drop_still=("TR p1344（the columns on grid line M, which appear to have been stationary）"),
    # 赤い線の型 →（交わるか, 出どころ）。high＝決まりどおりなら大きく離れる・mid＝説明の図（交われば壊れると読む）・touch＝余裕ゼロ
    curve=dict(high=(False, "TR p1073（a large margin against failure）"), mid=(True, "TR p1276（intersects … failure is predicted）"),
               touch=(True, "TR p1074（those margins against failure were zero at the time of failure）")),
    curve_gap=0.15,             # high の「大きく離れる」＝青い線の範囲で、2本の線の差が軸の高さの15%以上（模式の下限）
    neutral=("#8fa3ad", "A06（沈みは見られない＝色を付けない）"),
    # 推定で描く段＝{見え方: (欄, 値)}（front＝屋根が下がる・joint＝押しつぶれ）。その段までに「推定」の札
    assume=dict(front=("roof", "down"), joint=("crush", "on")))

# ── check_illu ──
# 🆕 19本目 ⑤b-2：㉒ A1（南から見た塔）の記録の値＝門番の側に持つ（§5b-88＝型の定数を読まない）
REC_A1 = dict(
    story_m=33.8 / 12.0,      # TF p3「12 stories 110'-10" (33.8 m)」＝1階の高さ
    drop_m=2.54,              # TR0318「about 100 inches or approximately one story height」
    drop_tag="約2.5m",        # 札に出してよい言い方（台本 c618 と同じ）
    drift_tag="約53センチ",   # TR0421「the 12th floor has moved west about 21 inches」（台本 ca18）。⑤c'（10-07）：cm→センチ（語りとほかの札にそろえた）
    sway_max=60.0,            # 揺れを大きく描く上限（画素・模式＝左下の断りと一緒に）
)

# 🆕 19本目 ⑤b-3：㉓ A2（プールデッキと地上の駐車場）・A3（地下の駐車場）の記録の並び＝門番の側に持つ（§5b-88）
REC_A23 = dict(
    park_side="west",          # TR p1176「地上の駐車場の東」に崩れが広がった＝駐車場は西・デッキは東
    gate_row="13.1",           # TR p1123「K-13.1 の近くのプランターと門」
    water_row="13.1",          # TR p1131・p1132「プランターの真東の柱 L-13.1」
    rows_south_to_north=("15", "13.1", "11.1", "9.1"),
    gate_near=60.0,            # A3：門はプランターの箱のすぐ北（画素）
)


GATES = {
    # 19本目は2段の帯（tiers）を使わなかった＝LANES_OK・REC_APPROX・REC_LANE は空（18本目の見本と入れ子にしても19本目の状態になる）
    "check_axis": dict(REC_AXIS=REC_AXIS, LANES_OK=set(), REC_APPROX=set(), REC_LANE={}, ORDER_REF_MIN=ORDER_REF_MIN),
    "check_qty": dict(REC_QTY=REC_QTY),
    "check_boxes": dict(REC_OTHER_ROLE=REC_OTHER_ROLE, REC_MECH=REC_MECH, REC_CHIP=REC_CHIP, REC_FORM=REC_FORM, REC_CAUSE=REC_CAUSE),
    "check_mech": dict(REC_M19=REC_M19),
    "check_illu": dict(REC_A1=REC_A1, REC_A23=REC_A23),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・titan_fig.GEO・（gate を渡せば）その門番の記録の表を19本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss と GEO は触らない）＝14・15・16・18本目の見本 `fixture_ep14`・
    `fixture_ep15`・`fixture_ep16`・`fixture_ep18` と重ねるとき（check_mech の selftest は14・15・16・18・19本目の検算を1つの処理で回す
    ＝先に14本目を全部差し込み、15・16・18・19本目は表だけ足す）。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が19本目の表で
       20本目の画を測る）。apply の前に**無かった名**（ss の FORM_*・FL_*・AX_*・fl・qrows …／門番の表）も覚えて、restore で**消す**
       ＝selftest のあとに19本目の名が本番へ残らない（fixture_ep15・fixture_ep16・fixture_ep18 と同じ作り）"""
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


CUTS_SHA = "0dcaa9c"       # 19本目の章ファイルが最後に本線で live だった commit（bc3255a で20本目の空の器にした）
_CUTS19 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def cuts_ep19():
    """19本目の章ファイル（git の CUTS_SHA の `tools/cuts/`）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。"""
    if _CUTS19:
        return _CUTS19[0]
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
        raise RuntimeError(f"🔴 19本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts19_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep19 の写真・頁を読む＝根の下の作業場所の
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
        raise RuntimeError(f"🔴 19本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}）")
    _CUTS19.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を19本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で20本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep19()
    _SAVED.append(dict(cuts=(dict(cuts.PLAN), dict(cuts.SPEC))))
    cuts.PLAN.clear()
    cuts.PLAN.update(copy.deepcopy(plan))
    cuts.SPEC.clear()
    cuts.SPEC.update(copy.deepcopy(spec))


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。
    ss と門番の表は、apply の前に無かった名を消す。GEO は fixture_ep14・15・16・18 と同じに、覚えた写しで入れ替える（clear → update）。
    tables_only で差し込んだ分は ss・GEO を覚えていない＝戻さない（先に差し込んだ別の見本を壊さない）。LIFO（あとに apply した順）"""
    while _SAVED:
        s = _SAVED.pop()
        if s.get("cuts") is not None:          # apply_cuts() の分＝20本目の PLAN・SPEC へ戻す
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
