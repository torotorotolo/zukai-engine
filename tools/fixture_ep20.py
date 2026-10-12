# -*- coding: utf-8 -*-
"""20本目（日本航空123便のリメイク・1985-08-12・運輸安全委員会の航空事故調査報告書と解説の動画）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-12（21本目 米国同時多発テロ〈9.11〉のリメイク ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `cbf40ec` と同じ）
  ・`cuts/ss.py` の20本目の値＝案C の出典の表（REC_DOCS＝報告書・解説・解説はじめに・建議・勧告・FAA・産経・会見・検索）・割れる時刻（ILLU_SPLIT_TIMES＝18:56）・
    札に出してよい時計の時刻（ILLU_CLOCK_OK）・想定の札（ILLU_ASSUME・`_S3_NOTE`）・壊れる物のカット（ILLU_DESTROY_CUTS）・軸の型（AX_ALARM・AX_CVR・AX_SQ・
    AX_DAY20・AX_FIX78・AX_7Y・AX_NEWS・AXI の項目）・棒（QG＝pol・jda・cyc／QB＝pol12・pol13・jda12・jda13・cyc_need・cyc_fly）
    （20本目 ⑤b-3〜⑤b-6b）。ILLU_CROWD_UNTIL ほか空のままだった案C の表（ILLU_ROLES・ILLU_SEC_OK・ILLU_COUNTS・ILLU_TOP_NOSCALE・ILLU_SUB_*・
    ILLU_BOOM_CUTS・ILLU_MIX_TODO・ILLU_MIX_BUNDLE・AXIS_DOCS）も、20本目の状態として持つ（19本目の見本と同じ考え方）
  ・`titan_fig.GEO` の20本目の地点＝**無い**（20本目は地点の鍵を足さなかった＝地図 drift を使わず、案C の S1〜S7 と模式図 mech20 に替えた）。
    GEO は空の表のまま持つ（15・16・18・19本目の見本と同じ作り＝apply/restore の対称）
  ・門番の記録の表（check_axis＝REC_AXIS・REC_APPROX／check_qty＝REC_QTY／check_boxes＝REC_CAUSE／check_mech＝REC_M20／check_illu＝REC_S1〜REC_S7）。
    LANES_OK・REC_LANE・ORDER_REF_MIN・REC_OTHER_ROLE・REC_MECH・REC_CHIP・REC_FORM は20本目も使わなかった＝空（None）の状態として持つ
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を20本目の実物でも確かめている＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は21本目の空の器にした
  （fixture_ep14・fixture_ep15・fixture_ep16・fixture_ep18・fixture_ep19 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep20
      fixture_ep20.apply(sys.modules[__name__])   # その処理の中だけ ss・GEO・この門番の記録の表が20本目になる
      try: …（検算）
      finally: fixture_ep20.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14・15・16・18・19本目の見本と重ねるとき（check_mech は14本目の検算と15・16・18・19・20本目の検算を1つの処理で回す）は
      fixture_ep20.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss・GEO は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと21本目以降の画に20本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。
■ 注意:
  ⚠️ 見本の頁の原文 `ref/ep20/src/ep20_pages.txt` は git の外（本線の作業ツリーにだけある）＝無いときは頁の照合を飛ばす
     （check_illu の `_pages()` が None を返す）。
  ⚠️ 20本目の selftest（`check_illu.selftest_ep20`／`selftest_ep20b`・`check_mech._selftest_m20`）は**章ファイルの SPEC を読まない**
     （場面・図は selftest の中で `IL.scene`／`F.m20` で組む）＝`apply()` だけで通る。それでも `apply_cuts()`（20本目の章ファイルを git の `CUTS_SHA`＝
     `f0095bd` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ20本目に入れ替える・git が無い所では止める＝fail closed）を用意した＝
     20本目の実物の絵を門番にかけ直したいとき（`restore()` で21本目へ戻る・LIFO）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep20/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は20本目の道を持つ。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝20本目は 0.99）は見本に入れない（16・18・19本目の見本も入れていない）＝本番の ss は
     今の値のまま残し、21本目の束で取り直す。
  ⚠️ 写真の束の定数（`TRIM` の写真-9〈p009〉の左18%・`NEEDS_MASK` の写真-14〈p014〉の顔だけモザイク・`PRIVATE_OUT` の写真-9 の左端の白い形）は
     見本に入れない（前の回までと同じく、本番の ss から外しただけ＝git の `f0095bd`〈章ファイルの最後の版〉と `cbf40ec`〈ss の最後の版〉）。
  ⚠️ `check_mech.FT`（フィート→メートル 0.3048）は単位の型＝本番に残した（見本に入れていない）。
  ⚠️ `check_illu` の ㉕ S2 が読む `ref/ep20/route20.json`（付図-1 の時刻の点）は記録から読んだデータ＝型の側の `_route20()` に残した
     （`_map16()` が `ref/ep16` の json をじかに読むのと同じ扱い）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep20"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・`tools/illu20.py`・門番 `check_illu`）── 20本目 ⑤b-3〜⑤b-6b
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：次の回は下の表を**その回の資料と時刻**に替える（頁の番号の書き方・資料の名の決め方は REC_DOCS の注）。
#   REC_PAGES … 部品の出典（`rec=`）を当てる原文（`=== p<N> ===` で頁を割った1ファイル＝④ の make_pages.py の出力）
#   REC_DOCS  … 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面に出す名前・頁の出し方（print＝印字の頁／pdf＝PDF の頁）
#   ILLU_* … 20本目は人・秒の札・描いてよい数・縮尺を持たない上から見た絵・潜水艦・音の輪・混ざりのつなぎ待ちを使わなかった＝空のまま（下の値）
# 🆕 2026-10-08（20本目 ⑤b-3）：20本目の値を入れた（置き場 S1・S2・S3＝`tools/illu20.py`・門番 check_illu ㉔㉕㉖）。
#   通し頁＝`ref/ep20/make_pages20.py` の `ref/ep20/src/ep20_pages.txt`（git の外）：報告書＝印刷の頁の番号そのまま（p1〜p343・
#   p310〜p343＝別添6 CVR の OCR）・解説＝1000＋印刷の頁。台本の出典の「別添6 p.311」は報告書の印刷の頁＝「報告書 p311」と書く
REC_PAGES = REF / "src" / "ep20_pages.txt"      # make_pages20.py の出力（git の外＝手元だけ）
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    "報告書": dict(range=(1, 343), name="航空事故調査報告書（1987年）", page="print", base=0),
    "解説": dict(range=(1001, 1034), name="運輸安全委員会の解説（2011年）", page="print", base=1000),
    # 🆕 ⑤b-6b：頁の番号を出さない資料（解説の「はじめに」p.i・記事・会見・FAA の頁・検索）と、報告書の前付けの建議（ja_01 の PDF6）
    "解説はじめに": dict(range=(1, 1), name="運輸安全委員会の解説（2011年）「はじめに」", page=None, base=0),
    "建議": dict(range=(6, 6), name="航空事故調査報告書（1987年）の建議", page="pdf", base=0),
    # 🆕 ⑤b-7：勧告第1号（ja_01 の PDF 3〜4頁＝前付け）＝文字の頁 cc06（`qa_out/ep20_assets.py` の PAGE_SRC 3004＝「勧告 p4」）
    "勧告": dict(range=(3, 4), name="航空事故調査報告書（1987年）の勧告", page="pdf", base=0),
    "FAA": dict(range=(1, 1), name="FAA「Lessons Learned」JA8119（2025年9月3日 更新）", page=None, base=0),
    "産経": dict(range=(1, 3), name="産経新聞（2026年8月12日・ITmedia ビジネスオンライン転載）", page=None, base=0),
    "会見": dict(range=(1, 1), name="国土交通大臣の会見（2026年8月25日）", page=None, base=0),
    "検索": dict(range=(1, 1), name="国土交通省の公表の検索（2026年10月8日）", page=None, base=0),
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


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：軸の型（`tools/axis.py`・門番 `check_axis`）── 20本目 ⑤b-5〜⑤b-6b（時間の帯・年表）
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の AX_*・AXI の項目は20本目の値（21本目の ⑤b-1 で見本 fixture_ep20 へ）。
#   値と頁は ref/ep20/src/ep20_pages.txt で当てた＝門番の側の表（check_axis.REC_AXIS）と照らされる（§5b-88）。
# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
AXI = {}

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
    # 🆕 ⑤c'：23秒あとのドーン（boom_s）の線まで 12px＝既定の off 8 だと札「18:24:12ごろ」の右の端と赤い線が 4px（geom_gap）→ off 3（すき間 9px）
    "cvr0": dict(k="pt", at="18:24:12", t="ここより前は消えていた", rec="報告書 p91", approx=True, anchor="end", off=3),
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
#   🔴 間の C整備（No.6C〜No.10C）の日付は報告書に無い＝点を打たない（推測で置かない）。年表は最初（No.5C＝1978年7月）と最後
#      （No.11C＝1984年11月20日〜12月5日）のあいだの括弧。🆕 ⑤c'（2026-10-11）：括弧だけでは語りの「7回」が画面に出なかった＝括弧に回数の札
#      「C整備 7回」（日付の無い回に点は打たないまま・axis の br の t）
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
    "c_all": dict(k="br", a="1978-07", b="1984-12-05", t="C整備 7回", rec=["報告書 p104", "報告書 p18"]),
    "fly7": dict(k="span", a="1978-07-12", b="1985-08-12", t="修理のあとの飛行", rec=["報告書 p18", "報告書 p1"], c="INST"),
    "acc85": dict(k="pt", at="1985-08-12", t="事故", rec="報告書 p1", c="ALERT", anchor="end"),
})
# 🆕 2026-10-10（20本目 ⑤b-6b）：ca16・ca17＝警報の帯の戻り（AX_ALARM）に、止まった理由（解説 p15＝付録8-2）・一時的な故障の可能性（p16）・
#   最も無理がない推論（p16＝異常事態の発生のすぐあと＝18:24:35 に点・時刻の札なし）。cc11〜cc14＝ボーイングの説明と削除・大臣の会見・
#   公表を待つ（sources.md §8）。🔴 月だけの記録は fmt="ym"（日を足さない）・2026-10 は「この動画を作った時点」
#   ⚠️ 門番 axis：右の端を 2026年12月にすると、2026年8月・8月25日・10月の札が3段に積まれ、右上の章の札に触れた（cc14）＝
#      軸を 2027年6月まで延ばし、「公表を待つ」を右へ振る（右の端の先は待っている時間＝点は打たない）。
#      ⚠️ 門番 layout：2027年3月までだと「2026年10月」の札の右の端が 1885（上限 1848）
AX_NEWS = dict(view="date", span=("2024-06", "2027-06"), ticks=("2025", "2026", "2027"))                # cc11〜cc14
AXI.update({
    "al_q": dict(k="span", a="18:24:38", b="18:25:04", t="止まった理由は明らかにできなかった", rec=["報告書 p88", "解説 p1015"], c="DOC"),
    "al_f": dict(k="span", a="18:24:38", b="18:25:04", t="一時的な故障の可能性", rec="解説 p1016", c="DOC"),
    # ⚠️ 門番 axis：ドーンの点（boom）と同じ所に置くと、縦の線がドーンの札を貫いた＝ca17 は boom を沈めずに外す（点の札が「ごく早い時点」）
    "inf": dict(k="pt", at="18:24:35", lab=False, t="ごく早い時点で急減圧（推論）", rec="解説 p1016", c="DOC", anchor="start"),
    "boe24": dict(k="pt", at="2024-09", t="ボーイングのサイトに説明", rec="産経 p1", fmt="ym", anchor="start"),
    "pub": dict(k="span", a="2024-09", b="2026-08", t="載せていた", rec="産経 p1", c="LINE"),
    "del26": dict(k="pt", at="2026-08", t="削除が分かる（報道）", rec="産経 p1", fmt="ym", anchor="end"),
    "min25": dict(k="pt", at="2026-08-25", t="大臣の会見", rec="会見 p1", fmt="md", anchor="end"),
    "now": dict(k="pt", at="2026-10", t="公表を待つ", rec="検索 p1", fmt="ym", anchor="start"),
})


# ══════════════════════════════════════════════════════
#  cuts/ss.py から：量の型（棒）── 20本目 ⑤b-5〜⑤b-6
# ══════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_QTY＝§5b-88）＝回を替えたら両方を替える。
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


# `apply()` が cuts.ss に差し込む名の全部（上の値＝ss から移したもの）。ここに無い名は ss に置かない
#   （`AXI`・`QG`・`QB` などは ss に空の器が残る＝見本の値〈20本目の項目つき〉を差し込む。`_S3_NOTE` と `AX_*` は本番の ss に無い名
#   ＝restore で消す）。20本目は関数を ss へ足さなかった（`ax()`・`qb()` は型の道具＝本番に残した）
SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "_S3_NOTE", "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "AX_ALARM", "AX_CVR", "AX_SQ", "AX_DAY20",
            "AX_FIX78", "AX_7Y", "AX_NEWS", "QG", "QB")


# ══════════════════════════════════════════════════════════
#  titan_fig.GEO から：20本目の地点＝無い
# ══════════════════════════════════════════════════════════
#   20本目は `titan_fig.GEO` に地点を足さなかった（地図 drift を使わず、案C の S1〜S7 と模式図 mech20 に替えた）。
#   `cbf40ec` の `titan_fig.GEO` は `ed7ebc3`（19本目の値を移した直後）と同じ（差分は模式図 `m20` の関数だけ）
GEO = {}


# ══════════════════════════════════════════════════════
#  門番の記録の表（20本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════
# 以下の表は、門番5本の本番の置き場にあった20本目の値を1文字も変えずに写したもの（GATES が門番ごとにまとめる）

# ── check_axis ──
# 🆕 2026-10-10（20本目 ⑤b-5）：時間の帯4カット（c210・c212・c214・c519）の値と頁（ref/ep20/src/ep20_pages.txt で当てた）。
#    報告書＝印刷の頁（別添6 は p310〜343）・解説＝1000＋印刷の頁
#    p6「18時24分35秒…「ドーン」というような音」・p88「18時24分37秒から約1秒間鳴り、26秒間中断した後18時25分04秒に再び鳴りだし」
#    （18:24:38＝37＋約1秒＝その終わり・38＋26＝18:25:04 と合う）・p91「18時24分12秒ごろから18時56分28秒ごろまで」・
#    p311（別添6）18:24:42「(CAP)スコーク77」・18:24:47「(COP)スコーク77」・解説 p19 表3「日没；12日18:40 日出；13日04:55」・
#    p23「墜落地点における日没は、18時40分ごろ」・p8「18時56分ごろ」（割れる＝付図-1「18:56'30」）・p26「8月13日04時39分日航機の残骸を発見し、
#    墜落現場を確認」・p28「8月13日10時45分ごろ…生存者が発見された」
REC_AXIS = {"18:24:35": {"報告書 p6"}, "18:24:37": {"報告書 p88"}, "18:24:38": {"報告書 p88"}, "18:25:04": {"報告書 p88"},
            "18:24:12": {"報告書 p91"}, "18:56:28": {"報告書 p91"}, "18:24:42": {"報告書 p311"}, "18:24:47": {"報告書 p311"},
            "18:40": {"解説 p1019", "報告書 p23"}, "18:56": {"報告書 p8"}, "翌4:39": {"報告書 p26"}, "翌4:55": {"解説 p1019"},
            "翌10:45": {"報告書 p28"}}
# 🆕 2026-10-10（20本目 ⑤b-6）：年表2つ（c815・c819＝1978年の修理の日付／c824〜c826＝修理のあとの7年）。別添1 本文 p246〜249 は文字の層が
#    無い＝`ref/ep20/src/ja_09_p15-18_ocr200.txt`（OCR）で読んだ：p247「修理作業は、昭和53年6月17日～7月11日の間に行われた」・
#    p248「この作業は6月26日に行われ、6月27日に修理チーム検査員の検査を受けた」・p249「飛行試験は、7月10日及び11日の両日」・
#    「7月11日付けで完了の確認」・「7月12日合格と判定された」／報告書 p18「昭和53年7月12日、同検査に合格した」・「昭和59年11月20日～
#    12月5日に実施されたC整備」・p104「昭和53年7月の修理と同時に行われたC整備（No.5C）」・p1「昭和60年8月12日」
#    🔴 間の C整備（No.6C〜No.10C）の日付は報告書に無い＝表に入れない（年表に点を打たせない）
REC_AXIS.update({"1978-06-17": {"報告書 p247"}, "1978-07-11": {"報告書 p247", "報告書 p249"}, "1978-06-26": {"報告書 p248"},
                 "1978-06-27": {"報告書 p248"}, "1978-07-10": {"報告書 p249"}, "1978-07-12": {"報告書 p249", "報告書 p18"},
                 "1978-07": {"報告書 p104"}, "1984-11-20": {"報告書 p18"}, "1984-12-05": {"報告書 p18"},
                 "1985-08-12": {"報告書 p1", "報告書 p18"}})
# 🆕 2026-10-10（20本目 ⑤b-6b）：ca16・ca17（同じ警報の帯）＝解説 p15「付録8-2 では…その理由を明らかにすることはできなかった」・
#    p16「ダイヤフラム等が…一時的に故障していた可能性も全くないとはいえません」「異常事態発生後、極めて早い時点で急激に客室高度が上昇した、
#    とするのが最も無理がない推論」（18:24:35＝異常事態の発生）。cc11〜cc14 の年表＝sources.md §8（産経新聞 2026-08-12＝ボーイングは2024年9月に
#    自社サイトに説明・2026年8月に削除と謝罪が分かる／国土交通大臣の会見 2026-08-25／2026-10-08 の検索で公表は見つからない）。
#    🔴 月だけの記録（2024年9月・2026年8月）は月の値で置く（日を推測で足さない）
REC_AXIS["18:24:35"] = REC_AXIS["18:24:35"] | {"解説 p1016"}
REC_AXIS["18:24:38"] = REC_AXIS["18:24:38"] | {"解説 p1015", "解説 p1016"}
REC_AXIS["18:25:04"] = REC_AXIS["18:25:04"] | {"解説 p1015", "解説 p1016"}
REC_AXIS.update({"2024-09": {"産経 p1"}, "2026-08": {"産経 p1"}, "2026-08-25": {"会見 p1"}, "2026-10": {"検索 p1"}})
REC_APPROX = {"18:24:12", "18:56:28", "18:56", "翌10:45"}      # 記録が about の時刻（「ごろ」が要る）

# 並び order の基準の時刻（分）。🔴 20本目は時計の時刻を含む並び（"1:16:27" の形）を使わなかった＝空（None）。本番も None
ORDER_REF_MIN = None

# ── check_qty ──
# 🆕 2026-10-10（20本目 ⑤b-5）：c523 捜索に出た人＝p26（2.14.1.3 警察「8月12日 約2,500名 8月13日 約3,500名」）・
#    p27（2.14.1.4 防衛庁「8月12日 約1,000名 … 8月13日 約3,200名」）。行の名＝12日は「事故の夜」・13日は「翌日」（日付の数字を書かない）
REC_QTY = {("警察（人）", "事故の夜"): (2500, {"報告書 p26"}), ("警察（人）", "翌日"): (3500, {"報告書 p26"}),
           ("防衛庁（人）", "事故の夜"): (1000, {"報告書 p27"}), ("防衛庁（人）", "翌日"): (3200, {"報告書 p27"})}   # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
# 🆕 2026-10-10（20本目 ⑤b-6）：c708 回数の比べ＝p105（3.2.3.1(1)「これらの疲労亀裂進展に要する内圧の負荷回数は1万回程度と推定され、これは、
#    昭和53年に行われた後部圧力隔壁の修理後の飛行回数(2.7.1参照)12,319回とほぼ一致する」）・p18（修理後の着陸回数 12,319回）
REC_QTY.update({("回数（回）", "亀裂の伸び（推定）"): (10000, {"報告書 p105"}),
                ("回数（回）", "修理後の飛行"): (12319, {"報告書 p105", "報告書 p18"})})

# ── check_boxes ──
# 20本目は流れ図（role の箱・仕組みの言葉・札）と書類の再現図を使わなかった＝REC_OTHER_ROLE・REC_MECH・REC_CHIP・REC_FORM は空。並べ図（REC_CAUSE）だけ使った
REC_OTHER_ROLE = {}   # 流れ図の「role」の箱＝役職でない言葉（報告書の文の言葉）→ 頁の集合
REC_MECH = set()      # 流れ図に出してよい言葉のうち、役職・罪名でないもの（仕組み・鎖・問いの箱と矢印の札）
REC_CHIP = {}         # 札（chip）の言葉 → 頁の集合
REC_FORM = {}         # 書類の再現図（表題 → dict(fields・ends・values＝記録の文にある値だけ・rec＝頁の集合)）
# 🆕 2026-10-10（20本目 ⑤b-5）：c522 山へ入った組（並べ図＝同じ形で並べるだけ・数は c523）。p28（2.14.2「警察、自衛隊、上野村消防団、
#    上野村猟友会及び多野藤岡広域消防本部その他による生存者の捜索・救難活動」・2.14.1.9 上野村消防団・2.14.1.10 上野村猟友会）・
#    p27（2.14.1.7 日本赤十字社群馬県支部「救護班3班に待機命令」）・p26（2.14.1.3 警察庁）
REC_CAUSE = {"警察": {"報告書 p28", "報告書 p26"}, "自衛隊": {"報告書 p28"}, "上野村消防団": {"報告書 p28"},
             "上野村猟友会": {"報告書 p28"}, "日本赤十字社の救護班": {"報告書 p27"}}        # 並べ図の項目 → 頁
# 🆕 2026-10-10（20本目 ⑤b-6）：c817 修理の3つの検査＝p102（3.2.2(1)(キ)「ボーイング社の検査員により…ボーイング社の規定に従って行われた。
#    日航は…領収検査を行った。航空局は…修理改造検査の申請に基づき…検査を行った」）／c818 航空局の検査で確かめたもの＝p103「申請者が提出した
#    図面等による修理計画の審査及び作業記録による修理過程の審査並びに作業完了後の現状についての一般的外観検査、地上における機能試験及び
#    飛行試験等」／c820 作業の管理＝p102（エ）「指示」・（オ）「実際の修正作業」・p103（ケ）「作業工程における検査を含む作業管理方法」
REC_CAUSE.update({"ボーイング社の検査員": {"報告書 p102"}, "日本航空の領収検査": {"報告書 p102"}, "航空局の検査": {"報告書 p102"},
                  "図面による修理計画の審査": {"報告書 p103"}, "作業記録による修理過程の審査": {"報告書 p103"},
                  "外観検査・機能試験・飛行試験": {"報告書 p103"},
                  "指示": {"報告書 p102"}, "作業": {"報告書 p102"}, "検査": {"報告書 p103"}})
# 🆕 2026-10-10（20本目 ⑤b-6b）：ca03 寄せられた疑問の3つ＝解説 p.i「はじめに」（「客室内に猛烈な風が吹き抜けるはずであり、また、室温も低下する
#    のに」「パイロットは酸素マスクを付けるように訓練されているのに付けていないのはなぜか」）・cc07 建議の2つ＝報告書の前付け PDF6
#    （「緊急又は異常な事態における乗組員の対応能力を高めるための方策を検討すること」「目視点検による亀裂の発見に関し検討すること」）
REC_CAUSE.update({"猛烈な風": {"解説はじめに p1"}, "室温の低下": {"解説はじめに p1"}, "酸素マスク": {"解説はじめに p1"},
                  "乗組員の対応能力を高める方策": {"建議 p6"}, "目視点検による亀裂の発見": {"建議 p6"}})

# ── check_mech ──
# 🆕 20本目 ⑤b-5（2026-10-10）：模式図（m20＝`tools/mech20.py`・11の見え方）
# 🔴 記録の値は門番の側に持つ（§5b-88＝描く側の表 mech20.TOP_ENG_Y・HY_CUT・AL_PTS・FX_PLANE・PR_BULK…を書き換えると鳴る）。
#    頁＝`ref/ep20/src/ep20_pages.txt`（報告書＝印刷の頁・別添6 は p310〜343・解説＝1000＋頁）で当てた。
REC_M20 = dict(
    # 操縦室の席（p6「副操縦士の機長昇格訓練のため、機長が右操縦士席、副操縦士が左操縦士席に位置し」・p148 付図-12＝P4 機関士計器は右の壁）
    seats=dict(day=("副操縦士", "機長"), usual_left="機長", src="報告書 p6・p148"),
    xpdr_digits=(4, "報告書 p6（緊急コード番号7700）"),
    # エンジンの横の位置（付図-4「有効エンジン・モーメントアーム」内側 Y_EI 12.07m・外側 Y_EO 21.15m）・左の2基＝No.1・No.2（p82）
    eng_y=((12.07, 21.15), "報告書 p140（付図-4）"),
    left_engines=({1, 2}, "報告書 p82（左側第1、第2エンジン・右側第3、第4エンジン）"),
    hyd_n=(4, "報告書 p112（配管を4系統）"),
    # 管が切れる所＝垂直尾翼の中（p113「垂直尾翼の損壊に伴う操縦系統油圧配管の切断」）＝後部圧力隔壁 BS2360（p29＝57.66m）より後ろ・
    #   垂直尾翼の後縁の根元（付図-4 の横の図＝71.2m）より前
    hyd_cut=((57.66, 71.2), "報告書 p113・p29・p140"),
    cg_x=(31.75, "報告書 p140（付図-4「104 FT 2 IN」＝機首から 0.25 MAC まで）"),
    # 高さの記録の点（時刻, フィート）＝cruise は付図-1 の時刻と高度の札（p137）・final は p82（18:55:57ごろ 約10,000フィート・
    #   18:56:17ごろ 約5,500フィート）と付図-1（18:56:03 8,400）
    alt=dict(cruise=[("18:24:12", 23400), ("18:24:35", 23900), ("18:25:18", 23900), ("18:27:07", 24400), ("18:28:36", 22100),
                     ("18:31:08", 24900), ("18:34:53", 21400), ("18:38:06", 22400), ("18:40:30", 22400), ("18:41:59", 20900),
                     ("18:43:05", 18600), ("18:44:09", 17000), ("18:45:48", 13500), ("18:47:17", 9000), ("18:48:03", 6800)],
             final=[("18:55:57", 10000), ("18:56:03", 8400), ("18:56:17", 5500)]),
    alt_src="報告書 p137（付図-1）・p82",
    # 印の時刻＝18:25:21（p6・p115 降下の要求）・18:40（p115「実際に降下を始めたのは18時40分以降」）・18:56:07（p82 頭下げ約36度）・
    #   18:56:17（p82 地上接近警報）
    alt_marks=dict(cruise=dict(m1="18:25:21", m2="18:40:00"), final=dict(m1="18:56:07", m2="18:56:17")),
    alt_rate=(15000.0, "報告書 p82（降下率は平均15,000フィート/分）"),
    gear=(25.59, "報告書 p140（付図-4「83 FT 11.5 IN」＝前の脚から主脚まで）・p117（18時38分以降脚下げ・18時44分以降フラップ下げ）"),
    radio=dict(names=dict(left="東京コントロール", right="羽田"), src="報告書 p6（東京管制区管制所＝東京コントロール）・p333（羽田にコンタクトしますか？）"),
    fix=dict(plane=(5.0, 1.0), heli=(1.0, 0.1), ray=(305.0, 35.0), src="解説 p1018（方位は5度、距離は1マイル／方位1度、距離0.1マイル）・p1019（①）"),
    bulk_x=(57.66, "報告書 p29（BS2360）"),
    # 3つの空港（p117「目的地の大阪国際空港や予定飛行経路から比較的近い名古屋空港ではなく東京国際空港を選んだことは、空港の規模、
    #   滑走路長及びその他の施設環境からみて妥当な選択」）・経度は一般の地図の値（東西の順を照らすだけ）
    apt=dict(lons={"大阪国際空港": 135.44, "名古屋空港": 136.92, "東京国際空港": 139.78}, picked="東京国際空港",
             why=("空港の規模", "滑走路長", "その他の施設環境"), src="報告書 p117"),
    clock={"18:25:21", "18:50:50", "18:42:53", "18:44:43", "18:56:07", "18:56:17", "18:55:57", "18:46:09"},
    # 🆕 ⑤b-6（第6〜8章）：p44「上側ウエブの下端から2列目のリベット孔を縫って破断…付図―38(a)」・p45「第1から第3ストラップの間の、
    #   ダブラ・プレートにより補強された部分の断面構造は、付図-38(b)」（上側ウエブの下端から1列目）・p102「この部分の強度は本来の強度の
    #   70パーセント程度に低下」・p124（同）・p65「1列リベットの場合の疲労亀裂は2列リベットの場合と比較すると、2倍強の速さで進展する」・
    #   別添1 p248「左側の第一ストラップと第3ストラップ間の2べイ分の結合が1列リベット結合」・p110「1ベイ・フェール・セーフ」・
    #   別添1 p246「後部圧力隔壁については、下半部（コレクタ・リングを含む。）の交換」・p103「当該接続部分の縁がフィレット・シールで覆われている」・
    #   p104「後部圧力隔壁後面全体の目視検査（G2レベル相当）」・p100「リベット孔両側平均で10ミリメートル（可視亀裂長さ8ミリメートル）」・
    #   「1つの疲労亀裂の発見確率は、10パーセント程度」・「少なくとも1つを発見できる確率は14～60パーセント程度」・p105（コ）・p103（ウ）
    #   「客室最後部位置の化粧室」「客室後部コートルーム」
    fatigue=dict(src="報告書 p65（多数のリベット孔縁より疲労亀裂が発生）"),
    rows=dict(n=dict(a=2, b=1), ratio=0.70, src="報告書 p44・p45（付図-38(a)(b)）・p102・p124（70パーセント程度に低下）"),
    grow=dict(ratio=(2.0, 2.5), src="報告書 p65（2倍強の速さで進展）"),
    fs=dict(one=(1, 3), src="報告書 p248（左側の第1ストラップと第3ストラップ間の2ベイ分）・p110（1ベイ・フェール・セーフ）"),
    half=dict(new="lo", src="報告書 p246（後部圧力隔壁については、下半部…の交換）"),
    edge=dict(src="報告書 p248（エッジ・マージンが構造修理マニュアルに記載された値より不足）"),
    seal=dict(ends=("upper", "splice", "lower"), src="報告書 p103（接続部分の縁がフィレット・シールで覆われている）・p174（付図-38）"),
    rear=dict(src="報告書 p104（後部圧力隔壁後面全体の目視検査）"),
    clen=dict(ratio=0.8, src="報告書 p100（リベット孔両側平均で10ミリメートル（可視亀裂長さ8ミリメートル））"),
    prob=dict(one=10.0, many=(14.0, 60.0), src="報告書 p100（10パーセント程度・14～60パーセント程度）"),
    two=dict(src="報告書 p105（隔壁が正規に製作されている場合、またその修理が適正に行われている場合には…妥当な点検方法）"),
    lav=dict(src="報告書 p103（客室最後部位置の化粧室・客室後部コートルーム）"),
    # 🆕 ⑤b-6b（第9章〜終章）：解説 p2「客室の天井(座席20列目付近)に約0.135m2の穴」・p6「開口部から2m離れた場所に着座していたとします」・
    #   p3「穴から少し離れると客室内での風はそれほど激しく吹かず」・p7「客室断面積を19.6m2とすると風速はほぼ10m/秒…風速は天井の上側で
    #   大きく、座席付近ではこの値よりかなり小さくなる」（報告書 付録4 の引用）・p8「100mを10秒」・p9「概ね2分後には0°C、3分後には10°C、
    #   5分後には20°C程度まで回復」「開口面積1.8m2を基準のケース」・p3 表2「B737-3H4…0.135m2…2.9秒」・p4「基準のケースでは約1.7秒…
    #   緩やかな減圧時のケースでは約5.0秒」・p23（サイド・スキャン・ソナー）・p24「分解能…1.1m×1.3m」「5.5m×6.5m程度必要」・
    #   p25「えい航高度 約1.5m・撮影幅 約1.5m」・p26「約25km2…4,500時間…1日6時間…750日」「認められる・推定される・考えられる・
    #   可能性が考えられる」・報告書 p130「垂直尾翼点検孔へのカバー装着」・p131「No.4油圧系統が垂直安定板へ入る上流にフューズ」・
    #   p126 4.1.7.3「20,000フィート以上の高度で…約18分間」・FAA の頁（sources.md §8＝2025年9月3日 更新の一文）
    cab=dict(area=0.135, R=2.0, src="解説 p1002・p1006"),
    flow=dict(src="解説 p1007（報告書 付録4＝天井の上側で大きく、座席付近ではかなり小さい）"),
    run=dict(m=100.0, src="解説 p1008（100mを10秒）"),
    temp=dict(pts=((2.0, 0.0), (3.0, 10.0), (5.0, 20.0)), src="解説 p1009（概ね2分後 0°C・3分後 10°C・5分後 20°C）"),
    dect=dict(j123=(1.7, 5.0), b737=2.9, src="解説 p1003（表2）・p1004（1.7秒・5.0秒・約2.9秒）"),
    holes=dict(j123=1.8, b737=0.135, src="解説 p1009（開口面積1.8m2を基準のケース）・p1002（約0.135m2）"),
    dcam=dict(h=1.5, w=1.5, src="解説 p1025（えい航高度 約1.5m・撮影幅 約1.5m）"),
    res=dict(cell=(1.1, 1.3), need=(5.5, 6.5), src="解説 p1024（分解能 1.1m×1.3m・5.5m×6.5m程度）"),
    area=dict(km2=25.0, days=750.0, src="解説 p1026（約25km2・1日6時間・750日）"),
    cover=dict(src="報告書 p130・p131（垂直尾翼点検孔へのカバー装着）"),
    word=dict(rows=(("認められる", "断定できる場合"), ("推定される", "断定できないが、ほぼ間違いない場合"),
                    ("考えられる", "可能性が高い場合"), ("可能性が考えられる", "可能性がある場合")), pick="推定される",
              src="解説 p1026"),
    faa=dict(sentence=("During the bulkhead repair, difficulty in installation of a splice plate resulted in the Boeing repair crew "
                       "dividing the plate and installing it in two pieces - a deviation from the repair instructions that, when "
                       "complete, with sealant applied on both fore and aft surfaces, had the same appearance as a correctly "
                       "installed splice plate."),
             hl="dividing the plate and installing it in two pieces", src="FAA の頁（2025年9月3日 更新・sources.md §8）"),
    ans=dict(n=3, wait="公表を待つ"),
    hyd_fuse=(4, 58.8, "報告書 p131（No.4油圧系統が垂直安定板へ入る上流にフューズ）・p140（付図-4＝垂直尾翼の根元）"),
    alt_band=(20000.0, "報告書 p126（20,000フィート以上の高度で…約18分間飛行）"),
    assume=dict(hyd=("cut", "on"), thrust=("nose", "up"), rows=("bars", "on"), clen=("len", "on")),
    # 🆕 ⑤b-6b：報告書・解説が「考えられる」と書く段＝札に「考え」が要る（推定ではない）
    think=dict(seats=("hyp", "on"), hyd=("fuse", "stop")))

# ── check_illu ──
# 🆕 20本目 ⑤b-3（2026-10-08）：㉔ S1（横から見た機体）・㉕ S2（上から見た経路の地図）・㉖ S3（2つの揺れの模式）＝`tools/illu20.py`
# 🔴 記録の値は門番の側に持つ（§5b-88＝illu20 の定数を読まない）。経路と時刻の点は記録から読んだデータ `ref/ep20/route20.json`
#    （付図-1 を Natural Earth の海岸線に重ねて読んだ値＝`ref/ep20/route20.py`）を読む（型の定数ではない）
REC_S1 = dict(len_m=70.51, len_rec="報告書 p140（付図-4「231 FT 4 IN」）", bs_nose=90.0, bs_bulk=2360.0, bs_cone=2658.0,
              bs_rec="報告書 p9（BS90〜・BS2658 以降のテールコーン）・p29（BS2360＝後部圧力隔壁の取付部）")
REC_S2 = dict(
    pts=dict(haneda=(139.780, 35.549), yokota=(139.348, 35.749), kumagaya=(139.388, 36.147), nagoya=(136.924, 35.255)),
    crash=(138 + 41 / 60 + 49 / 3600, 35 + 59 / 60 + 54 / 3600),        # 報告書 p8「北緯35度59分54秒、東経138度41分49秒」
    t0="18:12:00",                                                       # p6「18時12分滑走路15Lから離陸」
    nagoya_km=72 * 1.852, nagoya_tol=0.06)                               # p7「名古屋空港から72海里の地点」
REC_S3 = dict(pitch=15.0, roll=40.0, nums=("15度", "40度", "1,200メートル", "185キロ"),
              rec="報告書 p113（縦揺れ角±約15度・速度変化約100ノット・高度変化約4,000フィート）・p114（横揺れ角±約40度）")
# 🆕 20本目 ⑤b-4（2026-10-08）：㉗ S4（夜の地図）・㉘ S5（尾部が壊れていく推定）・㉙ S6（隔壁の継ぎ目）・㉚ S7（相模湾の地図）
# 🔴 記録の値は門番の側に持つ（§5b-88＝illu20 の定数・night20.json・sagami20.json を読まない）
REC_S4 = dict(
    crash=(138 + 41 / 60 + 49 / 3600, 35 + 59 / 60 + 54 / 3600),        # 報告書 p8
    fig_crash=(448.8, 827.8), fig_km=105.0,                              # 解説 図13 の拡大図（墜落位置の◎・目盛り 0〜5km＝103〜628画素）
    # 点 n：(時刻＝表3, 図13 の画素, 誤差 km＝表3)
    pts={1: ("19:15", (648.6, 567.7), 3.0), 2: ("19:21", (918.2, 1276.6), 6.0), 3: ("20:42", (198.5, 1134.2), 4.0),
         4: ("1:00", (378.5, 1057.5), 2.0), 5: ("4:39", (173.0, 1028.0), 3.0), 6: ("5:00", (492.9, 887.4), 1.0),
         7: ("5:33", (506.9, 720.6), 1.0)},
    le=(6,), err_tol=0.6,                                                # ⑥ は表3「1km 以下」
    peaks=dict(mikuni=(639.8, 1006.2), ougi=(168.6, 1133.3), touge=(640.0, 1069.0)),
    mikuni_km=2.5,                                                       # 報告書 p8「三国山の北北西約2.5キロメートル」（距離だけ照らす）
    wit=(202.5, 3.0, 4.0),                                               # 報告書 p7「墜落地点の南南西3～4キロメートル」
    # 表3 の TACAN の方位（磁方位）と距離（海里）＝図13 の点と照らす（偏差は西へ 7度・横田と入間の TACAN は飛行場の点）
    tacan=dict(st=dict(yok=(139.348, 35.749), iru=(139.410, 35.842)), var=7.0, tol=1.4,
               pts={1: ("yok", 305.0, 35.0), 2: ("yok", 300.0, 32.0), 3: ("yok", 299.0, 35.5), 4: ("iru", 291.0, 36.3)}),
    rings=(2.0, 4.0, 6.0),
    nums=("305度", "65キロ", "35海里", "2キロ", "3キロ", "4キロ", "6キロ"),
    rec="解説 p1019（表3）・p1020（図13）・報告書 p7・p8・p25")
REC_S5 = dict(bs_nose=90.0, bs_bulk=2360.0, bs_fw=2658.0, hyd=4, rud=2, area=("2〜3",),
              rec="報告書 p29（BS2360・BS2658）・p112（配管を4系統）・p125（開口面積は2~3平方メートル程度）・解説 p1025（表5 上方・下方方向舵）")
REC_S6 = dict(
    # 付図-3（p.252）の板の重なり（インチ・下が正・列の間＝1インチ）。None＝絵の端まで続く
    layers=dict(plan=dict(lower=(-0.50, None), splice=(-1.34, 1.32), upper=(None, 0.34), filler=None),
                real=dict(lower=(-0.58, None), splice=(-0.55, 1.32), upper=(None, 0.39), filler=(-1.32, -0.61))),
    tol=0.08, rows=(-1.0, 0.0, 1.0), join=dict(plan=2, real=1), l18_tol=0.1, n_stiff=36,
    rec="報告書 p252（別添1 付図-3）・p248（2列リベットで結合されるべきものが…1列リベット結合）・p168（付図-32）")
REC_S7 = dict(n_deb=28, n_pts=17, n_obj=6, n_area=8, bearing=244.0, brg_tol=1.5, nums=("17か所",),
              rec="報告書 p156（付図-20 ①〜㉘）・p157（付図-21 調査区域・①〜⑰・推定飛行経路244度）・解説 p1025（表5 の6つ）")


GATES = {
    # 20本目は2段の帯（tiers）・交信の帯（lanes）・時計の時刻を含む並び（order）を使わなかった＝LANES_OK・REC_LANE は空・ORDER_REF_MIN は None
    "check_axis": dict(REC_AXIS=REC_AXIS, LANES_OK=set(), REC_APPROX=REC_APPROX, REC_LANE={}, ORDER_REF_MIN=ORDER_REF_MIN),
    "check_qty": dict(REC_QTY=REC_QTY),
    "check_boxes": dict(REC_OTHER_ROLE=REC_OTHER_ROLE, REC_MECH=REC_MECH, REC_CHIP=REC_CHIP, REC_FORM=REC_FORM, REC_CAUSE=REC_CAUSE),
    "check_mech": dict(REC_M20=REC_M20),
    "check_illu": dict(REC_S1=REC_S1, REC_S2=REC_S2, REC_S3=REC_S3, REC_S4=REC_S4, REC_S5=REC_S5, REC_S6=REC_S6, REC_S7=REC_S7),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・titan_fig.GEO・（gate を渡せば）その門番の記録の表を20本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss と GEO は触らない）＝14・15・16・18・19本目の見本 `fixture_ep14`・
    `fixture_ep15`・`fixture_ep16`・`fixture_ep18`・`fixture_ep19` と重ねるとき（check_mech の selftest は14・15・16・18・19・20本目の検算を
    1つの処理で回す＝先に14本目を全部差し込み、15・16・18・19・20本目は表だけ足す）。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が20本目の表で
       21本目の画を測る）。apply の前に**無かった名**（ss の AX_*・`_S3_NOTE` …／門番の表）も覚えて、restore で**消す**
       ＝selftest のあとに20本目の名が本番へ残らない（fixture_ep15・fixture_ep16・fixture_ep18・fixture_ep19 と同じ作り）"""
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


CUTS_SHA = "f0095bd"       # 20本目の章ファイルが最後に live だった版（章ファイルを21本目の空の器に替える前＝git の `f0095bd`）
_CUTS20 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def cuts_ep20():
    """20本目の章ファイル（git の CUTS_SHA の `tools/cuts/`）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。"""
    if _CUTS20:
        return _CUTS20[0]
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
        raise RuntimeError(f"🔴 20本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts20_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep20 の写真・頁を読む＝根の下の作業場所の
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
        raise RuntimeError(f"🔴 20本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}）")
    _CUTS20.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を20本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で21本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep20()
    _SAVED.append(dict(cuts=(dict(cuts.PLAN), dict(cuts.SPEC))))
    cuts.PLAN.clear()
    cuts.PLAN.update(copy.deepcopy(plan))
    cuts.SPEC.clear()
    cuts.SPEC.update(copy.deepcopy(spec))


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。
    ss と門番の表は、apply の前に無かった名を消す。GEO は fixture_ep14・15・16・18・19 と同じに、覚えた写しで入れ替える（clear → update）。
    tables_only で差し込んだ分は ss・GEO を覚えていない＝戻さない（先に差し込んだ別の見本を壊さない）。LIFO（あとに apply した順）"""
    while _SAVED:
        s = _SAVED.pop()
        if s.get("cuts") is not None:          # apply_cuts() の分＝21本目の PLAN・SPEC へ戻す
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
