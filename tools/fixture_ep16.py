# -*- coding: utf-8 -*-
"""16本目（バイオントダム災害・1963年）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-04（18本目 スレッシャー号 ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `b044b56` と同じ）
  ・`cuts/ss.py` の後半＝案C の出典の表・時計の札・想定の札・壊れる物のカット・軸の型・水位と斜面の速さの線（lv）・棒・
    流れ図と書類の再現図・並べ図・決め所の出どころの札（16本目 ⑤b-2〜⑤b-8）
  ・`titan_fig.GEO` の16本目の地点＝**無い**（16本目は地点の鍵 `vajont_` を足さなかった＝`b044b56` の GEO は `abbde47` と同じ・
    差分は断面 `vsec`・線 `lv` の関数だけ）。GEO は空の表のまま持つ（15本目の見本と同じ作り＝apply/restore の対称）
  ・門番の記録の表（check_axis・check_qty・check_boxes・check_mech・check_illu）
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を16本目の実物でも確かめている＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は18本目の空の器にした
  （fixture_ep14・fixture_ep15 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep16
      fixture_ep16.apply(sys.modules[__name__])   # その処理の中だけ ss・GEO・この門番の記録の表が16本目になる
      try: …（検算）
      finally: fixture_ep16.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14・15本目の見本と重ねるとき（check_mech は14本目の検算と15本目の検算を1つの処理で回す）は
      fixture_ep16.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss・GEO は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと18本目以降の画に16本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ 見本の頁の原文 `ref/ep16/src/ep16_pages.txt` は git の外（本線の作業ツリーにだけある）＝無いときは頁の照合を飛ばす
     （check_illu の `_pages()` が None を返す）。
  ⚠️ 見本の「正本」`ref/ep16/map16.json`（#100 の地形図を目で読んだ点）は git の中＝check_illu の selftest が illu.py の VA・断面の
     定数と照らす（この見本の値ではなく型の側＝`tools/illu.py` の `VA_*`・`VB_*`・`VC_*`・`VD_*` を照らす）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep16"


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 16本目 ⑤b-2〜⑤b-4・⑤b-8
# ══════════════════════════════════════════════════════════
# 🆕 2026-10-01（16本目 ⑤b-2）：16本目の値を入れた（案C を初めて使うチャット）。頁の番号は台本 第2版の冒頭の表
#    （`ref/ep16/daihon_v2.md`「出典欄の略号と頁」）＝原文の通し頁ファイルの番号：S1＝PDF の頁のまま p1〜p248（PDF98＝印刷98・
#    🔴 PDF146＝印刷147・PDF147＝印刷146）・S8＝冊子の頁 41〜52＝p1041〜p1052・S9＝PDF の頁 p2001〜p2019・S10＝PDF の頁
#    p3001〜p3025（PDF20＝印刷21）。#100＝形のもと（1934年の地形図＝画像・原文の頁ファイルに無い＝`text=False` で頁の照合を飛ばす
#    ＝範囲 p1 だけ見る）。画面の名は語りの呼び名に合わせた（議会の調査委員会・学術の総説・バイオント財団の年表・歴史家）
REC_PAGES = REF / "src" / "ep16_pages.txt"      # ④ の make_pages.py の出力（git の外＝手元だけ）
REC_DOCS = {
    "S1": dict(range=(1, 248), name="イタリア議会 調査委員会 最終報告（1965年）", page="pdf", base=0),
    "S8": dict(range=(1041, 1052), name="学術の総説（Genevois・Ghirotti 2005）", page="print", base=1000),
    "S9": dict(range=(2001, 2019), name="バイオント財団の年表", page="pdf", base=2000),
    "S10": dict(range=(3001, 3025), name="歴史家 Reberschak ほか（2023年）", page="pdf", base=3000),
    "#100": dict(range=(1, 1), name="イタリア軍地理院 地形図（1934年）", page=None, base=0, text=False),
}
# 割れる時刻＝最後の電話（財団の年表 22時＝S9 PDF17／少数派の報告 22時15分＝S1 PDF228）＝画面に時計の札として出さない
ILLU_SPLIT_TIMES = ("22:00", "22:15")
ILLU_CROWD_UNTIL = None
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
# 🔴 秒の札は出さない（空＝全部止める＝門番 check_illu ⑤ `judge_labels`）。崩れて湖に入るまでの「45秒足らず」（S8 p.41）・
#    波が町に届くまでの時間（記録に無い）を札にしない＝冒頭は「動きの速さは縮めてある」と出典の行で断る（映像方針 §1-3）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）
# 時計の札は 22時39分だけ（S1 PDF98・PDF147・PDF207・S8 p.41・S9 PDF17 が一致＝資料が1つに決まる時刻）
ILLU_CLOCK_OK = ("22:39",)                  # 札に出してよい時計の時刻（門番 check_illu ⑤）
# 描いてよい数＝{部品の obj の名: (数, 出典)}（門番 check_illu ③'＝場面ごとに部品の obj を足した数が記録と同じ）。
#   🆕 16本目 ⑤b-2（置き場 VA）：ダム1・崩れたあとの塊1・北の岸の印2・迂回トンネル1・道の入口2。町と村と湖岸の集落は建物の面
#   （数えない形＝obj を持たない）。⚠️ 模型の想定の2つの塊（VB の c508・c509・c807）は別の名で足す（⑤b-3〜⑤b-4）
ILLU_COUNTS = dict(dam=(1, "S1 p171"), block=(1, "S1 p147"), north_marks=(2, "S1 p146"), tunnel=(1, "S1 p85"),
                   road_gates=(2, "S1 p98"),
                   # 🆕 ⑤b-4（VD）：模型の想定の2つの塊＝マッサレッツァの沢の東と西（実際の塊 block とは別の名）・1960年11月4日の崩落の2か所
                   model_blocks=(2, "S1 p224"), collapse1960=(2, "S1 p72"))
# 🆕 16本目 ⑤b-2：想定の札（起きた事ではない絵＝左上「再現イラスト」の下の琥珀の札）を出すカットと札の言葉（門番 check_illu ④＝
#   表のカットは札が要る・表に無いカットに札を出さない）。🆕 ⑤b-4：模型の想定（VD の c507〜c509・c513）。⚠️ c807 の左は
#   小さく戻す絵＝左上の札を出せない＝パネルの文「模型の想定」で言う（表に入れない）
ILLU_ASSUME = {"c316": "会社の説明（想定）", "c507": "模型の想定", "c508": "模型の想定", "c509": "模型の想定",
               "c513": "模型の想定"}
# 🆕 16本目 ⑤b-3：壊れる物の部品（町と集落の建物の面が消える＝VA の towns／shore が gone・mud／水が町を覆う＝flood／湖の岸の集落へ
#   届く波＝wave_e）を描いてよいカット（門番 check_illu ⑫＝ほかのカットで使えば止める・映像方針 §9 ⑫・10-01 カズヤくん「本編でも
#   町に届くまで描く」）。⚠️ wave_w（ダムを越えて峡谷へ＝町に届かない・c815）は入れない。空なら全部止める（fail closed）
# 🆕 ⑤b-8（2026-10-02）：cb08（Google Earth⑤ の替え＝崩れたあとの谷・語り「湖に近い集落は、あの夜の波で失われた」＝c814 の状態）を
#   足した。ca26・cb11（今に近い谷）は壊れる部品を使わない（建て直された町は泥の色にしない・集落は画面の外）
ILLU_DESTROY_CUTS = ("c102", "c814", "c823", "cb08")

# 🔴 §0b：軸の型（`tools/axis.py`・14本目 ⑤b-5）の「割れる時刻の印」に添える出典の名（`rec=` の資料名 → 画面の名）。
#   語りが資料を呼ぶ名に合わせる（海審の特別調査報告＝語りは「報告書」）。ILLU_SPLIT_TIMES の時刻は、軸の型では
#   **出典の名つきでだけ**出してよい（門番 check_axis ②＝点に by=True か split）
# 🆕 2026-10-01（16本目 ⑤b-5）：語りの呼び名（c701「財団の年表」・c712「少数派の報告」）。"S1 p228"＝頁ごとの名が先（axis.doc_names）
# 🆕 ⑤b-6a：c518 の割れる日（模型の研究所の委員会の意見＝S9 p2012 は3月30日・S1 p225〈少数派〉は4月30日）
AXIS_DOCS = {"S1 p228": "少数派の報告", "S1 p225": "少数派の報告", "S1": "議会の報告書", "S9": "財団の年表"}


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：軸の型（`tools/axis.py`・門番 `check_axis`）── 16本目 ⑤b-5・⑤b-6a・⑤b-6b
# ══════════════════════════════════════════════════════════
# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
# 🆕 2026-10-01（16本目 ⑤b-5）：場面4 10月9日の時刻の帯（c701〜c723 の9カット）。値と頁は ref/ep16/src/ep16_pages.txt で当てた
#   （S9 p2016〜2017＝財団の年表・S1 p98・p228）。🔴 22:00 と 22:15 は割れる時刻の印（split＝出典の名つき・カーソルを置かない）。
#   ⚠️ 目盛りは奇数の時（9〜23時）＝22時の目盛りの字が割れる時刻の印の横に出ない。時計の絵は描かない（映像方針 §6）
AX_DAY = dict(view="clock", span=("9:00", "23:00"),
              ticks=("9:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00", "23:00"))
# ⚠️ ⑤b-5 の門番：22:00・22:15・22:39 は一日の帯では約70画素に3つ＝札が3段に収まらない → 割れる時刻の印は夕方の寄り（c720）だけ。
#   目盛りに22時を置かない（割れる時刻の印の横に時刻の字を出さない）
AX_EVE = dict(view="clock", span=("20:00", "23:00"), ticks=("20:00", "21:00", "23:00"))
# ⚠️ 近い2点の札は左右に振る（§5b-93＝12時↔13時・17時↔17時50分）・札は短く（同じ段に並べる）
AXI = {
    "t0945": dict(k="pt", at="9:45", t="35家族が離れる", rec="S1 p98"),
    "t1200": dict(k="pt", at="12:00", t="動きが見える", rec="S9 p2016", anchor="end"),
    "t1300": dict(k="pt", at="13:00", t="割れ目", rec="S9 p2016", anchor="start"),
    "t1316": dict(k="span", a="13:00", b="16:00", rec="S9 p2016"),                       # 3時間で割れ目が広がる（札は c710 の項目の札）
    "t1516": dict(k="span", a="15:00", b="16:00", t="木が倒れる", rec="S9 p2016", c="ALERT"),
    "t1700": dict(k="pt", at="17:00", t="本部の指示", rec=["S9 p2016", "S1 p228"], anchor="end"),
    "t1750": dict(k="pt", at="17:50", t="電話", rec="S9 p2016", anchor="start"),
    "t2000": dict(k="pt", at="20:00", t="道をふさぐ", rec="S9 p2016"),
    "phone": dict(k="span", a="22:00", b="22:15", t="電話", rec=["S9 p2017", "S1 p228"]),   # 札に時刻を書かない（割れる時刻）
    "s2200": dict(k="split", at="22:00", rec="S9 p2017"),
    "s2215": dict(k="split", at="22:15", rec="S1 p228"),
    "nowarn": dict(k="span", a="20:00", b="22:39", t="下流の町に呼びかけなし", rec=["S1 p228", "S1 p98"], c="ALERT"),
    "t2239": dict(k="pt", at="22:39", t="崩落", rec=["S1 p98", "S9 p2017"], c="ALERT"),
    "day": dict(k="br", a="9:45", b="22:39", rec=["S1 p98", "S9 p2017"]),
}


# 🆕 2026-10-01（16本目 ⑤b-6a）：年表（date）＝第1〜6章の12カット。値と頁は ref/ep16/src/ep16_pages.txt で当てた＝門番
#   check_axis の REC_AXIS と照らす。札は語りの細かさまで（fmt="ym"／"y"＝§5b-93）・近い2点は左右に振る（anchor）
#   ANS＝答えの割れ方（c110）・ENEL＝サーデからエネルへ（c217・c218）・PERMIT＝許された水位（c318）・Y3＝3年の流れ（c322）・
#   EXP＝専門家の報告（c401・c402・c407）・MERLIN＝メルリンの記事（c421）・MODEL＝模型の歩み（c518・c523）・Y63＝1963年（c604）
AX_ANS = dict(view="date", span=("1963-01", "1972-06"), ticks=("1964", "1966", "1968", "1970", "1972"))
AX_ENEL = dict(view="date", span=("1962-10", "1963-06"), ticks=("1962-11", "1963-01", "1963-03", "1963-05"))
AX_PERMIT = dict(view="date", span=("1961-10", "1962-07"),
                 ticks=("1961-11", "1962-01", "1962-03", "1962-05", "1962-07"))
# ⚠️ ⑤b-6a の qa_all（layout）：1960年7月からだと左の端の点（崩落）の札が画面の左へはみ出した＝軸の左に余白（§5b-107④）
AX_Y3 = dict(view="date", span=("1960-01", "1963-07"), ticks=("1960", "1961", "1962", "1963"))
AX_EXP = dict(view="date", span=("1959-10", "1961-05"),
              ticks=("1960-01", "1960-04", "1960-07", "1960-10", "1961-01", "1961-04"))
AX_MERLIN = dict(view="date", span=("1959-01", "1961-04"), ticks=("1959", "1960", "1961"))
AX_MODEL = dict(view="date", span=("1960-09", "1963-12"), ticks=("1961", "1962", "1963"))
AX_Y63 = dict(view="date", span=("1962-05", "1963-11"), ticks=("1962-07", "1963-01", "1963-07"))
AXI.update({
    # ── c110 答えの割れ方（S1 p26＝19対8で多数派の報告を可決・通らなかった2つの案は最終報告に添える／S9 p2018＝判決3回）
    #    判決の名（一審・控訴審・破毀院）は後の章で初めて説明する＝ここは「判決」とだけ
    "a_fall": dict(k="pt", at="1963-10-09", t="崩落", rec=["S1 p98", "S9 p2017"], c="ALERT", fmt="y"),
    "a_parl": dict(k="pt", at="1965", t="議会の報告書", rec="S1 p26", c="INST"),
    "a_j1": dict(k="pt", at="1969-12-17", t="判決", rec="S9 p2018", fmt="y", anchor="end"),
    "a_j2": dict(k="pt", at="1970-10-03", t="判決", rec="S9 p2018", fmt="y"),
    "a_j3": dict(k="pt", at="1971-03", t="判決", rec=["S9 p2018", "S10 p3020"], fmt="y", anchor="start"),
    # ── c217・c218（S1 p90＝1962年12月6日の法律でエネルを設立・p91＝1963年3月14日の大統領令でサーデの事業をエネルへ）
    "n_enel": dict(k="pt", at="1962-12-06", t="エネルができる", rec="S1 p90", fmt="ym", c="INST"),
    "n_move": dict(k="pt", at="1963-03-14", t="事業がエネルへ", rec="S1 p91", fmt="ym", c="INST"),
    # ── c318 ダム局の許可（S9 p2011・p2012・S1 p92）＝札は水位だけ（月は目盛りで読む）・最後の700m だけ年月（語りが言う）
    "p640": dict(k="pt", at="1961-11-16", t="640m", rec="S9 p2011", lab=False),
    "p655": dict(k="pt", at="1961-12-23", t="655m", rec="S9 p2012", lab=False),
    "p675": dict(k="pt", at="1962-02-06", t="675m", rec="S9 p2012", lab=False),
    "p700": dict(k="pt", at="1962-06-08", t="700m", rec=["S1 p92", "S1 p33"], fmt="ym", big=True),
    # ── c322 3年の流れ（崩落 S1 p72・ミュラーの報告 p76・模型の報告 p89・715m を求める p92）
    "y_fall": dict(k="pt", at="1960-11-04", t="崩落", rec="S1 p72", c="ALERT", fmt="ym", anchor="end"),
    "y_mul": dict(k="pt", at="1961-02-03", t="ミュラーの報告", rec="S1 p76", fmt="ym", big=True, anchor="start"),
    "y_model": dict(k="pt", at="1962-07-03", t="模型の報告", rec="S1 p89", fmt="ym"),
    "y_715": dict(k="pt", at="1963-03-20", t="715mを求める", rec="S1 p92", fmt="ym"),
    # ── c401・c402・c407 崩落の前の専門家の報告（揺れで地下を調べた報告 S1 p36〈1960年2月4日〉・2人の地質学者 p73〈1960年6月〉・
    #    ミュラー p76〈1961年2月3日〉）。c407 の「1957年から」は S9 p2004（1957年8月6日＝会社が頼んだ2本目の報告）＝項目の札
    "e_caloi": dict(k="pt", at="1960-02-04", t="揺れで地下を調べる", rec=["S1 p36", "S9 p2006"], fmt="ym"),
    "e_geo": dict(k="pt", at="1960-06", t="2人の地質学者", rec="S1 p73", fmt="ym"),
    "e_fall": dict(k="pt", at="1960-11-04", t="崩落", rec="S1 p72", c="ALERT", fmt="ym"),
    "e_mul": dict(k="pt", at="1961-02-03", t="ミュラーの報告", rec="S1 p76", fmt="ym"),
    # ── c421 メルリンの記事（S1 p39＝1959年5月5日の記事・1960年11月30日 ミラノの裁判所で無罪／S9 p2005・S1 p220＝訴えの名）
    "m_art": dict(k="pt", at="1959-05-05", t="ウニタの記事", rec=["S1 p39", "S9 p2005"], fmt="ym"),
    "m_free": dict(k="pt", at="1960-11-30", t="無罪", rec="S1 p39", c="OK"),
    # ── c518・c523 模型の歩み（会社の記録 S1 p75・模型をつくる p89〈1961年の夏＝年の真ん中〉・委員会の意見＝🔴 月が割れる
    #    〈S9 p2012＝3月30日・S1 p225＝4月30日〉＝割れる日の印2つ・同じ札・出典の名つき・ゲッティの報告 p89）
    "md_note": dict(k="pt", at="1960-11-16", t="会社の記録", rec="S1 p75", fmt="ym"),
    "md_build": dict(k="pt", at="1961", t="模型をつくる", rec="S1 p89"),
    # ⚠️ ⑤b-6a の門番 check_axis：4月の印の札を右へ出すと、すぐ右のゲッティの報告（段が上）の縦の線が札を貫いた＝割れる日の札は
    #   2つとも左へ（段を分ける）・ゲッティの報告は年月まで（語りの c511 が日まで言う）で右へ＝札が 1963年3月の縦の線に届かない
    "md_s1": dict(k="split", at="1962-03-30", t="委員会の意見", rec="S9 p2012", fmt="ym", anchor="end"),
    "md_s2": dict(k="split", at="1962-04-30", t="委員会の意見", rec="S1 p225", fmt="ym", anchor="end"),
    "md_rep": dict(k="pt", at="1962-07-03", t="ゲッティの報告", rec="S1 p89", big=True, fmt="ym", anchor="start"),
    "md_715": dict(k="pt", at="1963-03-20", t="700mより上を求める", rec="S1 p92", fmt="y", big=True),
    "md_br": dict(k="br", a="1963-03-20", b="1963-10-09", rec=["S1 p92", "S1 p98"]),
    # ── c604 1963年（700m までの許可＝S1 p92〈1962年6月8日〉・715m を求める p92〈1963年3月20日〉）
    "q_700": dict(k="pt", at="1962-06-08", t="700mまでの許可", rec="S1 p92", fmt="ym"),
    "q_715": dict(k="pt", at="1963-03-20", t="715mを求める", rec=["S1 p92", "S1 p33"], big=True),
})


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：🆕 16本目 ⑤b-5（2026-10-01）：場面1 水位と斜面の速さの線（`tools/lv16.py`・門番 check_mech の judge_lv）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の LV_*・LVP は16本目の値（次の回は見本へ移して空にする）。
#   値と頁は ref/ep16/src/ep16_pages.txt で当てた＝門番の側の表（check_mech.REC_LV）と照らされる（§5b-88）。
#   置く日＝月だけの記録は15日・「primi」＝5日・「metà」＝15日・「fine」＝28日（門番の窓の内）。
#   🔴 1962年12月の速さは台本どおり S8 p.46「1.5センチ超」（S1 p90 は「約1センチ」＝資料で割れる・台本の確かめ G2）。
#   🔴 10月8日の報告の「9月の終わりに1日5センチ」は描かない（c611 の26日22ミリと食い違って聞こえる＝台本の確かめ G3-21）
LV_T = "水位と斜面の速さ"      # 見出し＝c619 の合図（断面の図解からグラフへ戻る札・映像方針 §6）。図の札と4字以上の語を重ねない
LV_NOTE = "点＝記録の値・あいだは直線でつないだ模式"
LV_ALL = dict(span=("1960-01-01", "1963-11-01"), ticks=("1960", "1961", "1962", "1963"), zr=(560, 740), zt=(600, 650, 700))
LV_63 = dict(span=("1963-03-01", "1963-10-20"),
             ticks=("1963-03", "1963-04", "1963-05", "1963-06", "1963-07", "1963-08", "1963-09", "1963-10"),
             zr=(640, 730), zt=(650, 675, 700))
VR_LO = dict(vr=(0, 50), vt=(0, 10, 20, 30, 40, 50))       # 1963年10月3日まで（1960年の山＝4センチ近く）
VR_HI = dict(vr=(0, 210), vt=(0, 50, 100, 150, 200))        # 10月8日（約100ミリ）・9日（200ミリ）まで
LVP = {
    # ── 湖の水位（m）──
    "z6003": dict(k="pt", s="z", at="1960-03-15", v=580, rec="S1 p72"),
    "z6010": dict(k="pt", s="z", at="1960-10-05", v=630, rec="S1 p73"),
    "z6011": dict(k="pt", s="z", at="1960-11-04", v=650, rec="S1 p72"),
    "z6101": dict(k="pt", s="z", at="1961-01-08", v=600, rec="S8 p1046"),
    "z6110": dict(k="pt", s="z", at="1961-10-15", v=600, rec=["S1 p88", "S1 p90"]),
    "z6201": dict(k="pt", s="z", at="1962-01-28", v=655, rec="S1 p87"),
    "z6210": dict(k="pt", s="z", at="1962-10-28", v=690, rec="S1 p90"),
    "z6212": dict(k="pt", s="z", at="1962-12-15", v=700, rec=["S1 p90", "S8 p1046"]),
    "z6302": dict(k="pt", s="z", at="1963-02-15", v=680, rec="S1 p90"),
    "z6303": dict(k="pt", s="z", at="1963-03-15", v=650, rec=["S1 p93", "S8 p1046"]),
    "z6304": dict(k="pt", s="z", at="1963-04-10", v=647.5, rec="S1 p226"),
    "z6308": dict(k="pt", s="z", at="1963-08-14", v=705.5, rec="S1 p226"),
    "z6309": dict(k="pt", s="z", at="1963-09-01", v=709.4, rec="S9 p2014"),
    "z6326": dict(k="pt", s="z", at="1963-09-26", v=710, rec="S9 p2014"),
    "z6308o": dict(k="pt", s="z", at="1963-10-08", v=702.5, rec="S1 p96"),
    "z6309o": dict(k="pt", s="z", at="1963-10-09", v=700.4, rec=["S1 p96", "S9 p2017"]),
    # ── 斜面の目印が1日に動く距離（ミリ）。「ほぼ0」は 0 に置く ──
    "v6003": dict(k="pt", s="v", at="1960-03-15", v=0, rec="S1 p72"),
    "v6010": dict(k="pt", s="v", at="1960-10-05", v=0, rec="S1 p73"),
    "v6011": dict(k="pt", s="v", at="1960-11-04", v=40, rec="S1 p73"),
    "v6101": dict(k="pt", s="v", at="1961-01-08", v=0, rec="S1 p85"),
    "v6209": dict(k="pt", s="v", at="1962-09-01", v=0, rec="S1 p92"),
    "v6212": dict(k="pt", s="v", at="1962-12-15", v=15, rec="S8 p1046"),
    "v6303": dict(k="pt", s="v", at="1963-03-15", v=0, rec="S1 p93"),
    "v6302s": dict(k="pt", s="v", at="1963-09-02", v=6.5, rec="S9 p2014"),
    "v6315s": dict(k="pt", s="v", at="1963-09-15", v=12, rec="S9 p2014"),
    "v6326s": dict(k="pt", s="v", at="1963-09-26", v=22, rec="S9 p2014"),
    "v6302o": dict(k="pt", s="v", at="1963-10-02", v=40, rec="S9 p2014"),
    "v6308o": dict(k="pt", s="v", at="1963-10-08", v=100, rec="S1 p96"),
    "v6309o": dict(k="pt", s="v", at="1963-10-09", v=200, rec="S9 p2014"),
}
LV_BRK = dict(k="brk", s="v", a="1963-03-15", b="1963-09-02", rec="S1 p93")   # 3月〜9月2日＝数の記録が無い（「目立った速まり無し」）
LV_REF = {
    "model": dict(k="ref", s="z", v=700, t="700m（模型）", rec="S1 p89", c="DOC", lab="l"),
    # ⚠️ 札は線の左の端（5月4日の側）＝右の端だと c619 の縦の線の札「下げると決める」と横に並んで1つの言葉に読めた（下見）
    "permit": dict(k="ref", s="z", v=715, a="1963-05-04", t="715mの許可", rec="S1 p92", c="INST", lab="l"),
    "crest": dict(k="ref", s="z", v=725.5, t="天端725.5m", rec="S9 p2006", c="LINE"),
    # ALERT_DIM は文字に使わない。⚠️ qa_all の echo：「1960年11月の崩落のとき」は c614 の語りの写し → 短く
    "v1960": dict(k="ref", s="v", v=40, t="1960年の山", rec="S1 p73", c="TICK", lab="l"),
}
LV_REL = {"model": dict(t="700m（模型）", src="S1 p89"), "permit": dict(t="715mの許可", src="S1 p92"),
          "crest": dict(t="天端725.5m", src="S9 p2006")}
# 縦の線（出来事の日）と帯。⚠️ 札は図の上の端（top）か下の端（bot）・近い札は dy でずらす（715m の許可の札＝線の左の端）
LV_EV = {
    "fall60": dict(k="ev", at="1960-11-04", t="崩落", rec="S1 p72", c="ALERT"),
    "fill3": dict(k="ev", s="z", at="1963-04-10", t="3回目の水ため", rec="S1 p226", c="LINE", dy=34),
    "acc": dict(k="ev", s="v", at="1963-08-15", t="速まり始める", rec=["S1 p93", "S1 p96"], c="ALERT"),
    # ⚠️ 試し焼き（36857375434）：上の端の札が715m の許可の破線の真上に乗り「715m の札」に読めた → 上の段だけ・札は下の端
    "lower": dict(k="ev", s="z", at="1963-09-26", t="下げると決める", rec="S9 p2015", c="LINE", pos="bot"),
    "rep": dict(k="ev", at="1963-10-08", t="10月8日の報告", rec="S1 p96", c="DOC", pos="bot"),
}
LV_BAND = {"calm63": dict(k="band", s="v", a="1963-05-01", b="1963-08-31", t="大きな速まりなし", rec="S1 p93")}


def lvp(*names, **kw):
    """LVP の点の写し（名を並べた順）。"""
    return [dict(LVP[n], **kw) for n in names]


def lv_upto(date, rows="zv", skip=()):
    """date（その日を含む）までの点（日付の順・rows の段だけ）。前のカットまでに出した点＝past に使う。"""
    import axis as _A
    d = _A.val("date", date)[0]
    out = [n for n, p in LVP.items() if p["s"] in rows and _A.val("date", p["at"])[0] <= d + 1e-9 and n not in skip]
    return [dict(LVP[n]) for n in sorted(out, key=lambda n: _A.val("date", LVP[n]["at"])[0])]


def _rk(r):
    d, _, p = str(r).partition(" p")
    return ({"S1": 0, "S8": 1, "S9": 2}.get(d, 9), int(p) if p.isdigit() else 0)


def lv_fig(view, steps, past=(), vr=None, rows="zv", rel=()):
    """線の図の fig＝("lv", …)。出典の行は描いた部品の rec から組む（左下）。"""
    import titan_fig as _F
    items = list(past) + [x for st in steps for x in _F._many(st.get("add"))]
    recs = sorted({r for it in items for r in (it.get("rec") if isinstance(it.get("rec"), list) else [it.get("rec")]) if r},
                  key=_rk)
    vv = (vr or VR_LO) if "v" in rows else dict(vr=None, vt=())
    return ("lv", dict(view, **vv, rows=rows, past=list(past), steps=list(steps), rel=list(rel), note=LV_NOTE, src=src(recs)))


# ss.src の橋（上の `lv_fig` が `src(...)` と書いてあるまま動くように）。fixture_ep15 の地図の関数と同じ理由・同じ作り
#   （ss.src は apply() の対象でない＝本番の関数のまま）
def src(recs):
    """ss.src の橋。"""
    from cuts import ss
    return ss.src(recs)


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：量の型（`tools/qty.py`・門番 check_qty）の棒 ── 16本目 ⑤b-6a・⑤b-6b
# ══════════════════════════════════════════════════════════
# 棒の群（尺は 0 から・項目名に単位）。数字は棒に書かない（§5b-9＝数は字幕）
# 🆕 2026-10-01（16本目 ⑤b-6a）：第1〜6章の棒（c205・c311・c410・c515・c611・c613）。値と頁は門番 check_qty.REC_QTY と照らす
#   ⚠️ 同じ群の灯した棒は色を分ける（ΔE 25 以上＝門番 ⑪）。日付を名にした行（同じ物差しの時間の並び＝c611）だけ同じ色でよい
#   ⚠️ 行の名に数字を書かない（⑩）＝日付だけ例外（「9月2日」）。「8階建てのビル」は数字＝棒にしない（c515 は語りだけ）
QG = {
    "dam_h": dict(id="dam_h", t="ダムの高さ（メートル）", ticks=(0, 50, 100, 150, 200, 250, 300), rows=("もとの計画", "変えた計画")),
    "lake_max": dict(id="lake_max", t="いちばん高い水位（メートル）", ticks=(0, 200, 400, 600, 800),
                     rows=("もとの計画", "変えた計画")),
    "vol": dict(id="vol", t="量（万立方メートル）", ticks=(0, 25, 50, 75, 100, 125), rows=("崩れた量", "東京ドーム")),
    # c410＝同じ群の尺を 2億まで（崩れた量と東京ドームは細い線になる＝300倍・160杯の差がそのまま見える）
    "vol_big": dict(id="vol", t="量（万立方メートル）", ticks=(0, 5000, 10000, 15000, 20000),
                    rows=("崩れた量", "東京ドーム", "動いている塊")),
    "wave": dict(id="wave", t="波の高さ（メートル）", ticks=(0, 5, 10, 15, 20, 25, 30)),
    # ⚠️ ⑤b-6a の門番 ⑩：群の名「1日に動いた距離」の「1」が数字の網に当たった＝言い方を変えた（1日あたりは注で言う）
    "speed": dict(id="speed", t="日ごとに動いた距離（ミリ）", ticks=(0, 10, 20, 30, 40, 50),
                  rows=("9月2日", "9月15日", "9月26日", "10月2〜3日")),
    # c613＝同じ群の尺を 200 まで（10月9日の棒を足す＝9月2日の30倍）
    "speed_hi": dict(id="speed", t="日ごとに動いた距離（ミリ）", ticks=(0, 50, 100, 150, 200),
                     rows=("9月2日", "9月15日", "9月26日", "10月2〜3日", "10月9日")),
}
QB = {
    # c205：S1 p63（1957年の変更＝高さ 202→266m・いちばん高い水位 677→722.50m）
    "h_old": dict(k="bar", g="dam_h", t="もとの計画", v=202, rec="S1 p63"),
    "h_new": dict(k="bar", g="dam_h", t="変えた計画", v=266, rec="S1 p63", c="AMBER"),
    "l_old": dict(k="bar", g="lake_max", t="もとの計画", v=677, rec="S1 p63"),
    "l_new": dict(k="bar", g="lake_max", t="変えた計画", v=722.5, rec="S1 p63", c="AMBER"),
    # c311・c410：崩れた量 70万（S1 p72）・東京ドーム 124万（一般の事実）・ミュラーの見積もり 2億（S1 p77）
    "v_fall": dict(k="bar", g="vol", t="崩れた量", v=70, rec="S1 p72", c="AMBER"),
    "v_dome": dict(k="bar", g="vol", t="東京ドーム", v=124, rec="一般の事実"),
    "v_mass": dict(k="bar", g="vol", t="動いている塊", v=20000, rec="S1 p77", c="ALERT"),
    # c515：模型の波 25m（S1 p97＝10月8日の国の監督の報告が引く）
    "w_model": dict(k="bar", g="wave", t="模型の波", v=25, rec="S1 p97", c="AMBER"),
    # c611・c613：1日に動いた距離（S1 p226・S9 p2014・S1 p93）
    "s0902": dict(k="bar", g="speed", t="9月2日", v=6.5, rec="S1 p226"),
    "s0915": dict(k="bar", g="speed", t="9月15日", v=12, rec="S1 p226"),
    "s0926": dict(k="bar", g="speed", t="9月26日", v=22, rec="S1 p226"),
    "s1002": dict(k="bar", g="speed", t="10月2〜3日", v=40, rec="S1 p226", c="AMBER"),
    "s1009": dict(k="bar", g="speed", t="10月9日", v=200, rec="S1 p93", c="ALERT"),
}

# 棒（第8〜10章）。⚠️ 同じ群の灯した棒は色を分ける（ΔE 25 以上＝門番 ⑪）。第9章（白黒）は LINE と DOC が 22.2・
#   第8章（夜の藍）は LINE と INST が 9.4＝その組を同じ群に灯さない（scratchpad の de_pairs.py で章の色ごとに測った）
QG.update({
    # c803：崩れた量（S1 p144＝280〜300百万立方メートル）とミュラーの見積もり（S1 p77＝約2億）・東京ドーム（細い線＝約230杯）
    "vol_63": dict(id="vol", t="量（万立方メートル）", ticks=(0, 10000, 20000, 30000),
                   rows=("東京ドーム", "ミュラーの見積もり", "崩れた斜面")),
    # c813：模型の波（c515 と同じ群・尺を 250 まで）と、実際に北の岸を駆け上がった高さ（S1 p146＝崩れる前の水面より「ゆうに200m」）。
    #   🔴 測り方が同じでない（波そのものの高さ／斜面を駆け上がった高さ）＝群を分け、尺だけそろえる（長さは比べられる）
    "wave_all": dict(id="wave", t="波の高さ（メートル）", ticks=(0, 50, 100, 150, 200, 250)),
    "runup": dict(id="runup", t="北の岸で水面から上がった高さ（メートル）", ticks=(0, 50, 100, 150, 200, 250)),
    # c907・c908：犠牲者（S1 p98＝内務省の調べ 1,917人・町ごと／S9 p2017・S10 p3020＝1,910人）。🔴 人の形は使わない（§C-1 #59）
    "victims": dict(id="victims", t="犠牲者（人）", ticks=(0, 500, 1000, 1500, 2000),
                    rows=("ロンガローネ", "カステッラヴァッツォ", "エルトとカッソ", "ほかの町の出身")),
    "victims_sum": dict(id="victims", t="犠牲者（人）", ticks=(0, 500, 1000, 1500, 2000),
                        rows=("ロンガローネ", "全体（内務省）", "全体（財団と歴史家）")),
    # ca22：刑の長さ（S9 p2018・S10 p3020＝ビアデーネ 5年うち3年免除・センシドーニ 3年8か月うち3年免除）。人で色を分ける
    "sentence": dict(id="sentence", t="言い渡された刑（年）", ticks=(0, 1, 2, 3, 4, 5, 6), rows=("ビアデーネ", "センシドーニ")),
    "pardon": dict(id="pardon", t="恩赦で免除（年）", ticks=(0, 1, 2, 3, 4, 5, 6), rows=("ビアデーネ", "センシドーニ")),
})
QB.update({
    "v_mul": dict(k="bar", g="vol", t="ミュラーの見積もり", v=20000, rec="S1 p77", c="AMBER"),
    "v_63": dict(k="bar", g="vol", t="崩れた斜面", v=28000, rec="S1 p144", c="ALERT"),
    # 見積もりの幅の上の端（S1 p144「fra 280 e 300 milioni」）＝破線の枠（注で「破線＝見積もりの幅の上の端」と言う）
    "v_63hi": dict(k="ghost", g="vol", row="崩れた斜面", v=30000, rec="S1 p144"),
    "w_real": dict(k="bar", g="runup", t="実際の波", v=200, rec="S1 p146", c="ALERT"),
    "k_lon": dict(k="bar", g="victims", t="ロンガローネ", v=1450, rec="S1 p98", c="ALERT"),
    "k_cas": dict(k="bar", g="victims", t="カステッラヴァッツォ", v=109, rec="S1 p98", c="AMBER"),
    "k_erto": dict(k="bar", g="victims", t="エルトとカッソ", v=158, rec="S1 p98", c="INST"),
    "k_other": dict(k="bar", g="victims", t="ほかの町の出身", v=200, rec="S1 p98"),
    "k_tot": dict(k="bar", g="victims", t="全体（内務省）", v=1917, rec="S1 p98"),
    "k_tot2": dict(k="bar", g="victims", t="全体（財団と歴史家）", v=1910, rec=["S9 p2017", "S10 p3020"], c="INST"),
    "j_bia": dict(k="bar", g="sentence", t="ビアデーネ", v=5, rec=["S9 p2018", "S10 p3020"], c="AMBER"),
    "j_sen": dict(k="bar", g="sentence", t="センシドーニ", v=44 / 12, rec=["S9 p2018", "S10 p3020"]),
    "p_bia": dict(k="bar", g="pardon", t="ビアデーネ", v=3, rec=["S9 p2018", "S10 p3020"], c="AMBER"),
    "p_sen": dict(k="bar", g="pardon", t="センシドーニ", v=3, rec=["S9 p2018", "S10 p3020"]),
})


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：🆕 16本目 ⑤b-6a・⑤b-6b（2026-10-01）：箱の型の16本目の表（門番 check_boxes の REC_OTHER_ROLE・REC_MECH・
#  REC_CHIP・REC_FORM・REC_CAUSE と照らす）＝流れ図・書類の再現図・並べ図
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の FL_*・FLP・FORM_* は16本目の記録（言葉と頁＝門番 check_boxes の REC_* と照らす）。
#   流れ図は役職でなく報告書の文の言葉（16本目は名前を箱に書かない＝実名は語りだけ）・赤を使わない・人の形を使わない
# c113 資料のつながり（S1 p99＝公共事業大臣の令 1963年10月11日・エネルが 11月1日に別の委員会）
FL_SRC = dict(heads=[dict(id="parl", t="議会の報告書", kind="node", x=(1360, 1800), y=(450, 550), rec="S1 p99")])
# c207 計画を大きくすると（S1 p63＝容量と年間の発電量が上がった）。箱は基図・段で矢印が出る
FL_GROW = dict(heads=[dict(id="g1", t="ダムを高くする", kind="node", x=(120, 600), y=(470, 570), rec="S1 p63"),
                      dict(id="g2", t="ためる水が増える", kind="node", x=(720, 1200), y=(470, 570), rec="S1 p63"),
                      dict(id="g3", t="つくれる電気が増える", kind="node", x=(1320, 1800), y=(470, 570), rec="S1 p63")])
# c418 報告の行き先（S1 p179 多数派＝役所は知っていたが正式に送られたとは確認できない・p232 少数派＝役所・地方の長官・土木局に隠した）
FL_HIDE = dict(heads=[dict(id="co", t="会社", kind="node", x=(780, 1100), y=(470, 570), rec="S1 p232")])
# c510 模型の実験（S1 p89＝22回・2つの進め方・最も破局的な崩れ／S9 p2010＝水位680〜720m／S1 p224＝少数派「いつも2つの塊」）
FL_EXP = dict(heads=[dict(id="x22", t="22回の実験", kind="node", x=(110, 470), y=(430, 530), rec="S1 p89"),
                     dict(id="xw", t="波の高さ", kind="node", x=(1500, 1810), y=(430, 530), rec="S9 p2010")])
# c621 3回の比べ（左）と10月8日の報告（右＝S1 p96〜p97）。左の年は見出しの箱・右は縦の矢印（箱が真下＝§5b-110②）
FL_THREE = dict(heads=[dict(id="y60", t="1960年", kind="head", x=(110, 360), y=(300, 360), rec="S1 p85"),
                       dict(id="y62", t="1962年", kind="head", x=(110, 360), y=(440, 500), rec="S1 p93"),
                       dict(id="y63", t="1963年", kind="head", x=(110, 360), y=(580, 640), rec="S1 p96")],
                bounds=(990,), guide_y=(280, 820))
FLP = {
    # c113
    "c_state": dict(k="role", id="c_state", t="国の調査委員会", y=380, pos=(760, 1180), rec="S1 p99"),
    "c_enel": dict(k="role", id="c_enel", t="電力公社の調査委員会", y=620, pos=(760, 1180), rec="S1 p99"),
    "o_min": dict(k="role", id="o_min", t="公共事業大臣", y=380, pos=(160, 580), rec="S1 p99"),
    "o_enel": dict(k="role", id="o_enel", t="電力公社", y=620, pos=(160, 580), rec="S1 p99"),
    # c418
    "r_geo": dict(k="role", id="r_geo", t="2人の地質学者の報告", y=380, pos=(110, 560), rec="S1 p232"),
    "r_mul": dict(k="role", id="r_mul", t="ミュラーの報告", y=520, pos=(110, 560), rec="S1 p232"),
    "r_mod": dict(k="role", id="r_mod", t="模型の報告", y=660, pos=(110, 560), rec="S1 p232"),
    "g_gov": dict(k="role", id="g_gov", t="国の役所", y=380, pos=(1340, 1800), rec="S1 p232"),
    "g_pref": dict(k="role", id="g_pref", t="地方の長官", y=520, pos=(1340, 1800), rec="S1 p232"),
    "g_gc": dict(k="role", id="g_gc", t="土木局", y=660, pos=(1340, 1800), rec="S1 p232"),
    # c510
    "x_grav": dict(k="role", id="x_grav", t="重力で崩す", y=400, pos=(600, 980), rec="S1 p89"),
    "x_geo": dict(k="role", id="x_geo", t="地質の予想どおりに崩す", y=560, pos=(600, 980), rec="S1 p89"),
    "x_lvl": dict(k="role", id="x_lvl", t="水位680〜720m", y=480, pos=(1100, 1400), rec="S9 p2010"),
    # c621（左＝3回の比べ・右＝10月8日の報告の手当て）
    "t60": dict(k="role", id="t60", t="下げると止まった", y=330, pos=(460, 880), rec="S1 p85"),
    "t62": dict(k="role", id="t62", t="下げると止まった", y=470, pos=(460, 880), rec="S1 p93"),
    "t63": dict(k="role", id="t63", t="下げても速まった", y=610, pos=(460, 880), rec="S1 p96"),
    "k_co": dict(k="role", id="k_co", t="会社", y=360, pos=(1160, 1660), rec="S1 p96"),
    "k_off": dict(k="role", id="k_off", t="役所", y=480, pos=(1160, 1660), rec="S1 p96"),
    "k_may": dict(k="role", id="k_may", t="村長", y=600, pos=(1160, 1660), rec="S1 p96"),
    "k_ord": dict(k="role", id="k_ord", t="危ない区域から人を出す", y=720, pos=(1160, 1660), rec="S1 p97"),
}


def fl(name, **kw):
    return dict(FLP[name], **kw)


# 書類の再現図（16本目）。🔴 欄の値は**原文のイタリア語のまま**（日本語は字幕だけ＝映像方針の c413・c422 の決めを、書類の再現図の
#   6カットにそろえた）・欄の名は原文の文の言葉・「再現」の札（様式は抽象）。値は門番 check_boxes.REC_FORM の values と照らす
FORM_MUELLER = dict(title="ミュラーの報告（少数派の報告が引く）", rec="S1 p217",
                    fields=[dict(t="問い", v="se questi franamenti possono venire arrestati mediante misure artificiali",
                                 rec="S1 p217"),
                            dict(t="答え", v="deve essere risposto negativamente in linea generale", rec="S1 p217", late=True)],
                    paper=(140, 1780, 330, 690), lw=120)
FORM_UNITA = dict(title="ウニタの記事（1961年2月21日）", rec="S1 p39",
                  fields=[dict(t="見出し", rec="S1 p39", late=True,
                               v="Una enorme massa di 50 milioni di metri cubi minaccia la vita e gli averi degli abitanti di Erto")],
                  paper=(100, 1820, 360, 640), lw=130)
FORM_NOTE60 = dict(title="会社の記録（1960年11月16日）", rec="S1 p75",
                   fields=[dict(t="第一の心配", v="garantire l'incolumità delle persone che abitano nella valle", rec="S1 p75"),
                           dict(t="必要なこと", v="abbassare il livello del serbatoio", rec="S1 p75", late=True),
                           dict(t="波", v="non possano assolutamente raggiungere la zona abitata", rec="S1 p75", late=True)],
                   paper=(200, 1720, 300, 760), lw=220)
FORM_GHETTI = dict(title="ゲッティの報告（1962年7月3日）", rec="S1 p89",
                   fields=[dict(t="結論", v="la quota 700 può considerarsi di assoluta sicurezza", rec="S1 p89", late=True),
                           dict(t="何に対して", v="del più catastrofico prevedibile evento di frana", rec="S1 p89", late=True)],
                   paper=(240, 1680, 330, 690), lw=220)
# ⚠️ ⑤b-6a の qa_all（echo）：表題「模型の研究所の委員会（1962年の春）」は c517 の1行目と2か所に割れて 100% 一致＝日付は注へ
FORM_NOVE = dict(title="模型の研究所の委員会", rec="S1 p225",
                 fields=[dict(t="意見", v="almeno per il momento non siano da compiere ricerche", rec=["S1 p225", "S9 p2012"],
                              late=True),
                         dict(t="研究", v="propagarsi di una onda di piena a valle della diga", rec=["S1 p225", "S9 p2012"],
                              late=True)],
                 paper=(240, 1680, 330, 690), lw=160)
FORM_GC61 = dict(title="土木局の手紙（1961年1月7日）", rec="S1 p79",
                 fields=[dict(t="湖が満ちたとき", v="le acque, eventualmente infiltratesi nel terreno", rec="S1 p79", late=True),
                         dict(t="急に下げるとき", v="possano mettersi in pressione", rec="S1 p79", late=True),
                         dict(t="斜面", v="pregiudicando la stabilità del versante", rec="S1 p79", late=True)],
                 paper=(200, 1720, 300, 760), lw=280)


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：🆕 2026-10-01（16本目 ⑤b-6b）：第7〜11章の年表・量・箱（27カット）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の AX_*・AXI の追加・QG／QB の追加・FORM_*・CAUSE の追加は16本目の記録。
#   値と頁は ref/ep16/src/ep16_pages.txt で当てた＝門番の側の表（check_axis.REC_AXIS・check_qty.REC_QTY／REC_GHOST・
#   check_boxes.REC_FORM／REC_CAUSE）と照らす。数の中身は台本の確かめ（④' の照合表＝daihon_v2.md の G4〜G6）が当てた頁で決めた。
#   🔴 一審・控訴審・破毀院の言葉は c719・ca16・ca18 で初めて説明する＝その前のカットの画面に出さない（ca14 の「一審」は c719 の後）
#   🔴 ca18・ca19 の PLAN の出典 S2 p.718（破毀院の判決の複写＝画像だけ・文字の層が無い＝REC_DOCS に無い＝照らせない）は、同じ中身の
#      財団の年表 S9 p2018「un unico disastro: inondazione aggravata dalla previsione dell'evento compresa la frana」に当て直した

# 年表の軸。第10章の裁判の年表（ca02〜ca21）は c110 と同じ AX_ANS（答えの割れ方の続き）
# ⚠️ c918・c919：10月11日と11月1日は21日＝札を左右に振る（左の点は "end"）＝左の点の札が画面の左へ出ないよう軸を8月から
AX_INQ = dict(view="date", span=("1963-08", "1964-03"), ticks=("1963-08", "1963-10", "1963-12", "1964-02"))
# cb14〜cb16 決める場面。⚠️ ⑤b-6b の試し焼き 36880658544（原寸）：軸の右の端が1963年12月だと、cb16 の3つの札（3月・9月・10月9日）が
#   3段に積まれ、いちばん上の「1963年10月9日」が右上の章の札（11 / 11）に接して1つの塊に読めた＝軸を1964年6月まで延ばし、崩落の札を
#   右へ（年月まで）＝2段に収める。⚠️ 1964年6月までだと右向きの札「1963年10月」の右の端が 1877（上限 1848）＝qa_all の layout
#   ＝1964年9月まで（Dela 56px の「1963年10月」は約370画素）
AX_DEC = dict(view="date", span=("1960-01", "1964-09"), ticks=("1960", "1961", "1962", "1963", "1964"))
AX_CIV = dict(view="date", span=("1968-01", "1977-01"), ticks=("1969", "1971", "1973", "1975"))      # ca25 償いの裁判


def dot(name, **kw):
    """前のカットの点を札なしの点で沈める（§5b-107④＝札は消して沈める・lab=False・t=""）。"""
    return dict(AXI[name], lab=False, t="", **kw)


AXI.update({
    # ── c918・c919 事故のあとの2つの調査委員会（S1 p99＝大臣の令 1963年10月11日・報告は1964年1月／エネルが 11月1日に別の委員会・
    #    報告は1964年1月16日。S9 p2017＝「le cause, prossime e remote」・90日で報告）。報告は c919 の3行目に1つの点（どちらも1月）
    "i_state": dict(k="pt", at="1963-10-11", t="国の調査委員会", rec=["S1 p99", "S9 p2017"], c="INST", anchor="end"),
    "i_br": dict(k="br", a="1963-10-11", b="1964-01", rec=["S1 p99", "S9 p2017"]),
    # ⚠️ ⑤b-6b の門番 check_axis：11月1日の札を日まで書くと幅が広がり、「2つの報告」の縦の線が札を貫いた＝年月まで・報告の札は右へ
    "i_enel": dict(k="pt", at="1963-11-01", t="電力公社の調査委員会", rec="S1 p99", c="INST", fmt="ym", anchor="start"),
    "i_rep": dict(k="pt", at="1964-01", t="2つの報告", rec="S1 p99", fmt="ym", big=True, anchor="start"),
    # ── 第10章 議会と裁判（AX_ANS）。議会＝S1 p1（法律 1964年5月22日 第370号・委員は上院と下院の議員）・p26（1965年の最終報告）／
    #    裁判＝S9 p2017（1968年2月20日 予審判事ファッブリが判決を出す・11月29日 ラクイラで一審が始まる）・p2018（判決3つ・時効）
    "l_parl": dict(k="pt", at="1964-05-22", t="議会の調査委員会", rec="S1 p1", fmt="ym", c="INST", anchor="start"),
    "l_pre": dict(k="pt", at="1968-02-20", t="予審", rec="S9 p2017", fmt="ym", anchor="end"),   # 札は括弧の右の端の上へ
    "l_prebr": dict(k="br", a="1963-10-09", b="1968-02-20", rec=["S1 p98", "S9 p2017"]),
    "l_start": dict(k="pt", at="1968-11-29", t="一審が始まる", rec="S9 p2017", fmt="ym", anchor="start"),
    "l_j1": dict(k="pt", at="1969-12-17", t="一審の判決", rec="S9 p2018", fmt="ym", anchor="start"),
    "l_j2": dict(k="pt", at="1970-10-03", t="控訴審の判決", rec="S9 p2018", fmt="ym", anchor="start"),
    # 破毀院＝S9 p2018「15-25 marzo. Processo di Cassazione」（25日＝判決の日・S2 の表紙も 1971-03-25）。札は年月まで（語りの細かさ）
    "l_j3": dict(k="pt", at="1971-03-25", t="破毀院の判決", rec=["S9 p2018", "S10 p3020"], fmt="ym", anchor="end"),
    # 時効＝崩落の7年半後（S9 p2018「Dopo quindici giorni sarebbero scaduti i 7 anni e mezzo」＝3月25日＋15日＝4月9日・S10 p3020）。
    #   ⚠️ 破毀院の判決と約7画素しか離れない＝点に札を立てると判決の札を縦の線が貫く → 札は点の下の項目の札（chips）
    "l_pres": dict(k="pt", at="1971-04-09", t="", lab=False, rec=["S9 p2018", "S10 p3020"], c="LINE"),
    "l_presbr": dict(k="br", a="1963-10-09", b="1971-04-09", rec=["S1 p98", "S9 p2017", "S9 p2018", "S10 p3020"]),
    # ── ca25 償いの裁判（S9 p2018＝1975年12月16日 ラクイラの控訴院がエネルに公の機関の損害の償いを命じ、ロンガローネの町の訴えは退けた）
    "v_crim": dict(k="span", a="1968-11-29", b="1971-03-25", t="罪を問う裁判", rec=["S9 p2017", "S9 p2018"]),
    "v_1975": dict(k="pt", at="1975-12-16", t="ラクイラの控訴院", rec="S9 p2018", fmt="y", big=True),
    # ── cb14〜cb16 決める場面（④' の照合 G6＝PDF72・PDF76〈PDF174 も 1961-02-03〉・PDF225／S9 p2012・PDF92・PDF93）
    "d_fall60": dict(k="pt", at="1960-11-04", t="崩落のあと", rec="S1 p72", fmt="ym", anchor="end"),
    "d_mul": dict(k="pt", at="1961-02-03", t="ミュラーの報告", rec="S1 p76", fmt="ym", anchor="start"),
    # 1962年の春＝月が資料で割れる（S9 p2012 は3月30日・S1 p225〈少数派〉は4月30日）＝割れる日の印2つ（c518 と同じ・札は2つとも左へ）。
    #   cb14・cb16 の札なしの点は「1962年4月」（S1 p225 の月）の1つ（札を出さない＝割れる日の印は cb15 だけ）
    "d_s1": dict(k="split", at="1962-03-30", t="下流の研究を見送る", rec="S9 p2012", fmt="ym", anchor="end"),
    "d_s2": dict(k="split", at="1962-04-30", t="下流の研究を見送る", rec="S1 p225", fmt="ym", anchor="end"),
    "d_spr": dict(k="pt", at="1962-04", t="", lab=False, rec="S1 p225"),
    "d_715": dict(k="pt", at="1963-03-20", t="715mを求める", rec="S1 p92", fmt="ym", anchor="end"),
    # 9月＝S1 p93「da mm/g 6,5 del 2 settembre a 200 mm/g del 9 ottobre」（速さが増し始めた日）
    "d_speed": dict(k="pt", at="1963-09-02", t="速さが増す", rec=["S1 p93", "S1 p226"], fmt="ym", anchor="end"),
    "d_end": dict(k="pt", at="1963-10-09", t="崩落", rec=["S1 p98", "S9 p2017"], c="ALERT", big=True, fmt="ym", anchor="start"),
})

# 書類の再現図（第7・10章）。欄の値は原文のイタリア語のまま（⑤b-6a と同じ）・欄の名は原文の文の言葉を日本語に
# c705・c707＝ビアデーネの10月9日朝の手紙（議会の報告書 S1 p96 が引く形＝財団の年表 S9 p2016 の写しとは綴りが少し違う
#   〈sul terreno／del terreno〉＝S1 の綴り・Pineda の引用符は外した）。🔴 紙1枚に欄は4つまで（図の高さ 682画素）＝7つの欄は
#   入らない → c707 は「続き」の紙（映像方針 §16）
FORM_LET9 = dict(title="ビアデーネの手紙（議会の報告書が引く）", rec="S1 p96",
                 fields=[dict(t="地面と道と木", rec="S1 p96", late=True,
                              v="Le fessure sul terreno, gli avvallamenti sulla strada, la evidente inclinazione degli alberi"),
                         dict(t="大きな亀裂", v="l'aprirsi della grande fessura che delimita la zona franosa", rec="S1 p96",
                              late=True),
                         dict(t="目印", v="il muoversi dei punti anche verso la Pineda che finora erano rimasti fermi",
                              rec="S1 p96", late=True)],
                 paper=(100, 1820, 300, 760), lw=230)
FORM_LET9B = dict(title="ビアデーネの手紙（続き）", rec="S1 p96",
                  fields=[dict(t="今朝の水位", v="questa mattina dovrebbe essere a quota 700", rec="S1 p96", late=True),
                          dict(t="下げる先", v="Penso di raggiungere quota 695", rec="S1 p96", late=True),
                          dict(t="ねらい", v="creare una fascia di sicurezza per le ondate", rec="S1 p96", late=True)],
                  paper=(240, 1680, 300, 760), lw=200)
# ca09＝もう1つの少数派の報告（S1 p241）。⚠️ 原文の PDF の文字は「assòluta」＝assoluta の崩れ（門番の表の注に書いて直した）
FORM_MIN2 = dict(title="もう1つの少数派の報告", rec="S1 p241",
                 fields=[dict(t="退ける説", rec="S1 p241", late=True,
                              v="la sciagura del Vajont ha avuto tutti i caratteri della assoluta imprevedibilità"),
                         dict(t="その説は", v="piuttosto affermata che dimostrata", rec="S1 p241", late=True)],
                 paper=(100, 1820, 330, 690), lw=170)
# ca19＝判決（財団の年表 S9 p2018 が記す）。🔴 PLAN の S2 p.718 は照らせない（上の注）。3行目「最初の判決から、予見についての答えは、
#   大きく変わった」＝一審の欄（同じ頁の1969年の行）を最後に書き込む（映像方針 §16）
FORM_JUDG = dict(title="判決（財団の年表が記す）", rec="S9 p2018",
                 fields=[dict(t="一審", v="Non viene riconosciuta la prevedibilità della frana", rec="S9 p2018", late=True),
                         dict(t="破毀院", v="inondazione aggravata dalla previsione dell'evento compresa la frana",
                              rec="S9 p2018", late=True)],
                 paper=(140, 1780, 330, 690), lw=150)

# 原因の並べ図（14本目＝c615・cc13）＝同じ形で並べるだけ（場面にしない）
# 🆕 16本目 ⑤b-6a：c419＝議会の中の2つの見方（S1 p179 多数派・p232 少数派）を同じ形で並べる（どちらかに決めない）
CAUSE = {
    "majority": dict(k="item", t="多数派「確認できない」", rec="S1 p179"),
    "minority": dict(k="item", t="少数派「隠した」", rec="S1 p232"),
}
# 並べ図（第10・11章）＝同じ形で並べるだけ（どれかを目立たせない・場面にしない）
CAUSE.update({
    # ca04・ca10：議会の3つの報告（S1 p26＝多数派の報告を19対8で決め、2つの少数派の報告を添えた・p178・p207・p241）
    "rep_maj": dict(k="item", t="多数派の報告", rec=["S1 p26", "S1 p178"]),
    "rep_min1": dict(k="item", t="少数派の報告", rec=["S1 p26", "S1 p207"]),
    "rep_min2": dict(k="item", t="もう1つの少数派の報告", rec=["S1 p26", "S1 p241"]),
    # ca17：控訴審の結果（S9 p2018＝ビアデーネ・センシドーニ有罪／フロジーニ・ヴィオリン・マリン・トニーニ・ゲッティ無罪／バティーニは
    #   病気で外れた＝11−亡くなった3＝8人）。名前は語りだけ・顔は描かない
    "ap_guilty": dict(k="item", t="有罪 2人", rec="S9 p2018"),
    "ap_free": dict(k="item", t="無罪 5人", rec="S9 p2018"),
    "ap_out": dict(k="item", t="裁判から外れた 1人", rec="S9 p2018"),
    # cb12・cb13：3つの答え（多数派 S1 p178「l'evento, così come si è manifestato, non fu previsto da nessuno」・少数派 p207
    #   「prevedibile e probabile, e quindi evitabile」・破毀院 S9 p2018「aggravata dalla previsione dell'evento compresa la frana」）
    "ans_maj": dict(k="item", t="多数派「その形は誰も予見せず」", rec="S1 p178"),
    # ⚠️ ⑤b-6b の qa_all（echo）：「予見でき、避けられた」は cb13 の語りの複写（連続一致 0.75）＝evitabile を「防げた」と言い換えた
    "ans_min": dict(k="item", t="少数派「予見でき、防げた」", rec="S1 p207"),
    "ans_cass": dict(k="item", t="破毀院「予見していた重い過失」", rec="S9 p2018"),
})


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：🆕 16本目 ⑤b-8（2026-10-02）：決め所の出どころの札（`fig=("quote", dict(phrase=[…], rows=ss.qrows(…), paper=True))`）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：QDOC・QWHO はこの回の資料の名。
#    札の値は全角12字ぶんで折れる（`titan_fig.quote` の para）＝日付・かっこが行で割れない言い方にした（§5b-110⑤・`F.wrap(t, 12)` で
#    確かめた）：S1「議会の調査委員会の／最終報告（1965年）」・S8「学術の総説（2005年）」＋著者・S10「歴史家の論文（2023年）」＋著者。
#    REC_DOCS の画面の名（「学術の総説（Genevois・Ghirotti 2005）」）は12字で折るとかっこの中で割れる。
#    ⚠️ ⑤b-8 の qa_all（wrap）：「イタリア議会 調査委員会 ／最終報告（1965年）」は空白で折れても漢字と漢字（会｜最）の間＝語の途中に見える
#    ＝ひらがな「の」の後で折れる名前にした
#    決め所の言葉（phrase）は台本の★の行と1字も違えない（字幕はその行を落とす＝scene_jiko.SUB_MUTE）。原文の照合＝⑤b-8 の引き継ぎ §3
QDOC = {"S1": "議会の調査委員会の最終報告（1965年）", "S8": "学術の総説（2005年）", "S10": "歴史家の論文（2023年）"}
QWHO = {"S8": "Genevois・Ghirotti", "S10": "Reberschak ほか"}


def qrows(doc, page, *extra):
    """決め所の出どころの札の rows＝extra（(欄, 値) の組＝書いた人・日付・出どころ）＋記録＋著者＋頁。page は画面の頁の字。"""
    import jiko_style as J
    rows = [(k, v, J.LINE) for k, v in extra]
    rows.append(("記録", QDOC[doc], J.INK_W))
    if doc in QWHO:
        rows.append(("著者", QWHO[doc], J.LINE))
    rows.append(("頁", page, J.TICK))
    return rows


# `apply()` が cuts.ss に差し込む名の全部（上の値と関数＝ss から移したもの）。ここに無い名は ss に置かない
#   （`src` は橋＝ss.src をそのまま使う＝差し込まない）
SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK",
            "ILLU_COUNTS", "ILLU_ASSUME", "ILLU_DESTROY_CUTS",
            "AXIS_DOCS",
            "AX_DAY", "AX_EVE", "AXI", "AX_ANS", "AX_ENEL", "AX_PERMIT", "AX_Y3", "AX_EXP", "AX_MERLIN", "AX_MODEL", "AX_Y63",
            "AX_INQ", "AX_DEC", "AX_CIV", "dot",
            "LV_T", "LV_NOTE", "LV_ALL", "LV_63", "VR_LO", "VR_HI", "LVP", "LV_BRK", "LV_REF", "LV_REL", "LV_EV", "LV_BAND",
            "lvp", "lv_upto", "_rk", "lv_fig",
            "QG", "QB",
            "FL_SRC", "FL_GROW", "FL_HIDE", "FL_EXP", "FL_THREE", "FLP", "fl",
            "FORM_MUELLER", "FORM_UNITA", "FORM_NOTE60", "FORM_GHETTI", "FORM_NOVE", "FORM_GC61",
            "FORM_LET9", "FORM_LET9B", "FORM_MIN2", "FORM_JUDG",
            "CAUSE", "QDOC", "QWHO", "qrows")


# ══════════════════════════════════════════════════════════
#  titan_fig.GEO から：16本目の地点＝無い
# ══════════════════════════════════════════════════════════
#   16本目は `vajont_` の頭の地点を足さなかった（地図 drift を使わない回＝⑤b-8 で地図は断面・上から見た谷＝案C の VA〜VD に替えた）。
#   `b044b56` の `titan_fig.GEO` は `abbde47`（16本目の ⑤b-1）と同じ（差分は `vsec`・`lv` の関数だけ）
GEO = {}


# ══════════════════════════════════════════════════════════
#  門番の記録の表（16本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════════
GATES = {
    "check_axis": dict(
        # 🆕 2026-10-01（16本目 ⑤b-5）：16本目の値を入れた＝10月9日の時刻の帯（場面4）。原文 ref/ep16/src/ep16_pages.txt で当てた
        #    （S1＝議会の調査委員会の最終報告 PDF の頁・S9＝バイオント財団の年表 PDF の頁 p2001〜）
        REC_AXIS={
            "9:45": {"S1 p98"},                    # p98「Il successivo 9 ottobre alle ore 9,45 del mattino … tutte le 35 famiglie … sistemandosi provvisoriamente a Casso」
            "12:00": {"S9 p2016"},                 # p2016「Ore 12. Durante la pausa pranzo alcuni operai ENEL fermi sul coronamento della diga vedono …」
            "13:00": {"S9 p2016"},                 # 「Ore 13. Dietro le baracche degli operai in sponda sinistra, si apre una crepa larga 50 centimetri e lunga 5 metri」
            "16:00": {"S9 p2016"},                 # 「Dopo tre ore la crepa ha progredito di 40-50 centimetri」（13時＋3時間）／「Ore 15-16.」の尻
            "15:00": {"S9 p2016"},                 # 「Ore 15-16. un operaio attraversando la zona del Massalezza … vede alberi cadere」
            "17:00": {"S9 p2016", "S1 p228"},      # 「Ore 17. Caruso riceve da Venezia le direttive …」・S1 p228（少数派「ma non per fare sgomberare la popolazione」）
            "17:50": {"S9 p2016"},                 # 「Ore 17.50. Biadene telefona a Penta … per la prima volta, informa Penta degli esperimenti su modello … quota 700」
            "20:00": {"S9 p2016", "S1 p228"},      # 「Ore 20. I camion non sono più in grado di transitare … La strada per il Toc viene sbarrata」・p228「Alle ore 20 …」
            "22:00": {"S9 p2017"},                 # 割れる時刻 S9「Ore 22. Rittmeyer telefona a Biadene, a Venezia」
            "22:15": {"S1 p228"},                  # 割れる時刻 S1 p228（少数派）「Alle 22,15 — come hanno affermato le telefoniste di Longarone」
            "22:39": {"S1 p98", "S9 p2017"},       # S9 p2017「Ore 22.39. La frana si stacca」・S1 p98
            # 🆕 2026-10-01（16本目 ⑤b-6a）：年表（date）＝第1〜6章。原文 ref/ep16/src/ep16_pages.txt で当てた
            "1963-10-09": {"S1 p98", "S9 p2017"},  # 崩落の日
            "1965": {"S1 p26"},                    # p26「La Commissione ha approvato — con 19 voti favorevoli e 8 contrari — la relazione redatta dal Presidente」（6月8日の会議の後）
            "1969-12-17": {"S9 p2018"},            # 「1969 17 dicembre. Si conclude il processo di primo grado」
            "1970-10-03": {"S9 p2018"},            # 「3 ottobre. La sentenza riconosce la totale colpevolezza di Biadene e Sensidoni」（控訴審）
            "1971-03": {"S9 p2018", "S10 p3020"},  # S9「1971 15-25 marzo. Processo di Cassazione」・S10 p3020「la sentenza finale della Cassazione venne emessa nel marzo 1971」
            "1962-12-06": {"S1 p90"},              # p90「Con la legge 6 dicembre 1962, n. 1643 … fu istituito l'Ente nazionale energia elettrica (ENEL)」
            "1963-03-14": {"S1 p91"},              # p91「Con decreto presidenziale 14 marzo 1963, n. 221, venne disposto il trasferimento della impresa elettrica della SADE all'ENEL」
            "1961-11-16": {"S9 p2011"},            # S9「16 novembre. Autorizzazione alla ripresa dell'invaso, ma solo fino a quota 640」（1961年＝31 ottobre の Semenza の死のあと）
            "1961-12-23": {"S9 p2012"},            # 「23 dicembre. Il Servizio Dighe autorizza quota 655」（1962 の見出しの前）
            "1962-02-06": {"S9 p2012"},            # 「1962 … 6 febbraio. Il Servizio Dighe autorizza quota 675」
            "1962-06-08": {"S1 p92", "S1 p33"},    # p92「dalla quota 700 (consentita in data 8 giugno 1962)」・p33「autorizzazione Servizio dighe dell'8 giugno 1962 … fino a quota 700」
            "1960-11-04": {"S1 p72"},              # p72「il 4 novembre 1960 una frana di circa 700.000 metri cubi si distaccava」
            "1961-02-03": {"S1 p76", "S1 p36"},    # p76「« Rapporto geologico preparato per conto della SADE » datato 3 febbraio 1961」（ミュラー）
            "1962-07-03": {"S1 p89", "S9 p2012"},  # p89「Il 3 luglio 1962 il professor Augusto Ghetti … completava la relazione」
            "1963-03-20": {"S1 p92", "S1 p33"},    # p92「Il 20 marzo 1963 venne chiesta l'autorizzazione ad elevare l'invaso sperimentale dalla quota 700 … alla quota 715」
            "1960-02-04": {"S1 p36", "S9 p2006"},  # p36「P. CALOI — relazione geofisica su indagini condotte nel novembre-dicembre 1959 (4 febbraio 1960)」
            "1960-06": {"S1 p73", "S1 p36", "S9 p2007"},  # p73「Lo « Studio geologico sul serbatoio del Vajont » datato giugno 1960 dei geologi Giudici e Semenza」
            "1959-05-05": {"S1 p39", "S9 p2005"},  # p39「Tina Merlin, sull'Unità del 5 maggio 1959」
            "1960-11-30": {"S1 p39"},              # p39「Tribunale di Milano il 30 novembre 1960 … conclusosi con sentenza di assoluzione」
            "1960-11-16": {"S1 p75"},              # p75「una nota datata 16 novembre 1960」（会社の記録）
            "1961": {"S1 p89"},                    # p89「il modello era stato costruito nell'estate del 1961 in scala 1:200」
            "1962-03-30": {"S9 p2012"},            # 割れる日 S9「30 marzo. Il Comitato direttivo del Centro Modelli Idraulici di Nove è del parere …」
            "1962-04-30": {"S1 p225"},             # 割れる日 S1 p225（少数派）「nella sua riunione del 30 aprile 1962 espresse il parere …」
            # 🆕 2026-10-01（16本目 ⑤b-6b）：年表（date）＝第9〜11章。原文 ref/ep16/src/ep16_pages.txt で当てた
            "1963-10-11": {"S1 p99", "S9 p2017"},  # p99「Il Ministro dei lavori pubblici, con suo decreto dell'11 ottobre 1963 … costituì una Commissione」
            "1963-11-01": {"S1 p99"},              # p99「l'ENEL nominò il 1° novembre 1963 altra Commissione di inchiesta」
            "1964-01": {"S1 p99"},                 # p99「presentò, nel gennaio 1964, la sua relazione」・エネルの委員会「il 16 gennaio 1964, presentò la relazione」
            "1964-05-22": {"S1 p1"},               # p1「(LEGGE 22 MAGGIO 1964, n. 370)」（議会の調査委員会をつくった法律）
            "1968-02-20": {"S9 p2017"},            # S9「1968 20 febbraio. Il Giudice istruttore Mario Fabbri deposita la sentenza」
            "1968-11-29": {"S9 p2017"},            # 「29 novembre. Inizia all'Aquila il processo di primo grado」
            "1971-03-25": {"S9 p2018", "S10 p3020"},  # S9「1971 15-25 marzo. Processo di Cassazione a Roma」（25日＝判決）・S10 p3020「nel marzo 1971」
            # 時効の日＝崩落の7年半後（計算：1963-10-09＋7年6か月＝1971-04-09＝判決の15日後）。S9「Dopo quindici giorni sarebbero scaduti i
            #   7 anni e mezzo dall'avvenimento contestato」・S10 p3020「a soli 15 giorni dalla data che avrebbe fatto scattare la prescrizione」
            "1971-04-09": {"S9 p2018", "S10 p3020"},
            "1975-12-16": {"S9 p2018"},            # 「1975 16 dicembre. La Corte d'appello dell'Aquila rigetta la richiesta del comune di Longarone」
            "1962-04": {"S1 p225"},                # cb14・cb16 の札なしの点（S1 p225＝4月30日＝少数派の報告の月）。割れる日の印は cb15
            "1963-09-02": {"S1 p93", "S1 p226"},   # p93「da mm/g 6,5 del 2 settembre a 200 mm/g del 9 ottobre」（速さが増し始めた日）
        },
    ),
    "check_qty": dict(
        # 🆕 2026-10-01（16本目 ⑤b-6a）：16本目の棒の値を入れた（原文 ref/ep16/src/ep16_pages.txt で当てた＝型の側 ss.QB とは別に持つ）
        REC_QTY={          # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
            # c205：S1 p63「aumentata l'altezza da 202 a 266 metri ed il livello di massimo invaso portato dalla quota 677 alla quota 722,50」
            ("ダムの高さ（メートル）", "もとの計画"): (202, {"S1 p63"}),
            ("ダムの高さ（メートル）", "変えた計画"): (266, {"S1 p63"}),
            ("いちばん高い水位（メートル）", "もとの計画"): (677, {"S1 p63"}),
            ("いちばん高い水位（メートル）", "変えた計画"): (722.5, {"S1 p63"}),
            # c311・c410：S1 p72「una frana di circa 700.000 metri cubi」・p77「circa 200 milioni di metri cubi」（ミュラー）・
            #   東京ドームの容積 124万立方メートル（一般の事実＝台本 c206・c311・c410 の「120杯」「半分を少し超える」「160杯」の元）
            ("量（万立方メートル）", "崩れた量"): (70, {"S1 p72"}),
            ("量（万立方メートル）", "東京ドーム"): (124, {"一般の事実"}),
            ("量（万立方メートル）", "動いている塊"): (20000, {"S1 p77"}),
            # c515：S1 p97「con il massimo invaso e con il crollo istantaneo della frana l'onda conseguente raggiungerebbe una altezza
            #   di 25 metri」（10月8日の国の監督の報告が引く模型の結果）
            ("波の高さ（メートル）", "模型の波"): (25, {"S1 p97"}),
            # c611・c613：S1 p226「il 2 settembre 6,5 millimetri, il 15 settembre 12 millimetri, il 26 settembre 22 millimetri, il 2 e il
            #   3 ottobre 40 millimetri, il 9 ottobre …」・S9 p2014「fino ai 200 mm del 9 ottobre」・S1 p93「da mm/g 6,5 … a 200 mm/g」
            ("日ごとに動いた距離（ミリ）", "9月2日"): (6.5, {"S1 p226", "S9 p2014", "S1 p93"}),
            ("日ごとに動いた距離（ミリ）", "9月15日"): (12, {"S1 p226", "S9 p2014"}),
            ("日ごとに動いた距離（ミリ）", "9月26日"): (22, {"S1 p226", "S9 p2014"}),
            ("日ごとに動いた距離（ミリ）", "10月2〜3日"): (40, {"S1 p226", "S9 p2014"}),
            ("日ごとに動いた距離（ミリ）", "10月9日"): (200, {"S1 p93", "S9 p2014"}),
            # 🆕 2026-10-01（16本目 ⑤b-6b）：第8〜10章の棒（原文 ref/ep16/src/ep16_pages.txt で当てた）
            # c803：S1 p144「per un volume compreso fra 280 e 300 milioni di metri cubi」（国の調査委員会の専門家）・p77（ミュラー）
            ("量（万立方メートル）", "崩れた斜面"): (28000, {"S1 p144"}),
            ("量（万立方メートル）", "ミュラーの見積もり"): (20000, {"S1 p77"}),
            # c813：S1 p146「raggiunse la quota massima di 930 metri sul livello mare « di ben 200 metri superiore al livello dell'acqua
            #   preesistente alla frana »」（崩れる前の水面から測った高さ＝波そのものの高さ〈模型の25m〉とは測り方が違う＝群を分けた）
            ("北の岸で水面から上がった高さ（メートル）", "実際の波"): (200, {"S1 p146"}),
            # c907・c908：S1 p98「da una accurata indagine del Ministero dell'interno, risultò che le vittime furono 1.917, delle quali 1.450 a
            #   Longarone, 109 a Castellavazzo, 158 a Erto e Casso e 200 persone originarie di altri comuni」・S9 p2017「la morte di 1910
            #   persone」・S10 p3020「1910」
            ("犠牲者（人）", "ロンガローネ"): (1450, {"S1 p98"}),
            ("犠牲者（人）", "カステッラヴァッツォ"): (109, {"S1 p98"}),
            ("犠牲者（人）", "エルトとカッソ"): (158, {"S1 p98"}),
            ("犠牲者（人）", "ほかの町の出身"): (200, {"S1 p98"}),
            ("犠牲者（人）", "全体（内務省）"): (1917, {"S1 p98"}),
            ("犠牲者（人）", "全体（財団と歴史家）"): (1910, {"S9 p2017", "S10 p3020"}),
            # ca22：S9 p2018「Biadene viene condannato a 5 anni (di cui 3 condonati), Sensidoni a 3 anni e 8 mesi (di cui tre condonati)」・
            #   S10 p3020（同じ）。3年8か月＝44/12年
            ("言い渡された刑（年）", "ビアデーネ"): (5, {"S9 p2018", "S10 p3020"}),
            ("言い渡された刑（年）", "センシドーニ"): (44 / 12, {"S9 p2018", "S10 p3020"}),
            ("恩赦で免除（年）", "ビアデーネ"): (3, {"S9 p2018", "S10 p3020"}),
            ("恩赦で免除（年）", "センシドーニ"): (3, {"S9 p2018", "S10 p3020"}),
        },
        # 「後」の行に「前」の長さを薄く残す棒（14本目）。🆕 16本目 ⑤b-6b：見積もりの幅の上の端にも使う（c803＝S1 p144「fra 280 e 300」の
        #   300＝崩れた斜面の棒〈下の端 280〉の外の破線の枠・注で「破線＝見積もりの幅の上の端」と言う）
        REC_GHOST={
            ("量（万立方メートル）", "崩れた斜面"): (30000, {"S1 p144"}),
        },
    ),
    "check_boxes": dict(
        # 🆕 2026-10-01（16本目 ⑤b-6a）：第1〜6章の箱（流れ図・書類の再現図・並べ図）の言葉と頁を入れた（原文で当てた）
        REC_OTHER_ROLE={    # 流れ図の「role」の箱＝役職でない言葉（報告書の文の言葉）→ 頁の集合
            # c113：S1 p99「Il Ministro dei lavori pubblici, con suo decreto dell'11 ottobre 1963 … costituì una Commissione di inchiesta」・
            #   「l'ENEL nominò il 1° novembre 1963 altra Commissione di inchiesta」
            "国の調査委員会": {"S1 p99"}, "電力公社の調査委員会": {"S1 p99"}, "公共事業大臣": {"S1 p99"}, "電力公社": {"S1 p99"},
            # c418：S1 p232（少数派）「all'occultamento alle autorità, ai Prefetti, e al Genio civile di Belluno e di Udine della relazione
            #   Ghetti come delle relazioni Semenza-Giudici e Müller」・p179（多数派）「conosciuti alla Pubblica Amministrazione, benché non
            #   consti che le relazioni siano state ufficialmente trasmesse」
            "2人の地質学者の報告": {"S1 p232"}, "ミュラーの報告": {"S1 p232"}, "模型の報告": {"S1 p232"},
            "国の役所": {"S1 p179", "S1 p232"}, "地方の長官": {"S1 p232"}, "土木局": {"S1 p232"},
            # c510：S1 p89「le prove erano state svolte secondo due diversi indirizzi」＝①「facendolo avvenire per azione della gravità」
            #   ②「rimettersi alle previsioni che poteva fornire lo studio geologico」（④' の照合 G3＝2通りは p89）・S9 p2010「con invaso a
            #   quote comprese tra i 680 e 720 metri」
            "重力で崩す": {"S1 p89"}, "地質の予想どおりに崩す": {"S1 p89"}, "水位680〜720m": {"S9 p2010"},
            # c621：1960年と1962年は下げると止まった（S1 p85＝1961年1月にほぼ0・p93＝1963年3月にほぼ0）／1963年は下げても速まった
            #   （p96「il serbatoio sta calando un metro al giorno」と速さの増え）・p96〜p97（10月8日の報告）「hanno tempestivamente informato le
            #   Autorità competenti … il Sindaco, su invito del Prefetto e del Genio civile, ha emesso una ordinanza per la evacuazione di
            #   persone ed animali dalla zona pericolante」
            "下げると止まった": {"S1 p85", "S1 p93"}, "下げても速まった": {"S1 p96", "S1 p93"},
            "会社": {"S1 p96"}, "役所": {"S1 p96"}, "村長": {"S1 p96"}, "危ない区域から人を出す": {"S1 p96", "S1 p97"},
            # 🆕 ⑤b-8（2026-10-02）：c204（地図 drift の替え）＝S1 p51「la sezione della valle del Vajont presa in considerazione per la
            #   costruzione della diga di sbarramento」・「dal serbatoio del Vajont … addotte alla grande centrale di Soverzene」（下流の町）
            "谷をせき止めるダム": {"S1 p51"}, "下流の発電所": {"S1 p51"},
            # ca13（地図 drift の替え）＝S10 p3019「avrebbe dovuto svolgersi a Belluno … trasferito per «rimessione» al Tribunale dell'Aquila
            #   su ordinanza della Cassazione … per conseguenza ad una mancata serenità dei giudici」
            #   ・「esacerbazione degli stati d'animo della popolazione」（住民の気持ちの高ぶり）
            "ベッルーノの裁判所": {"S10 p3019"}, "ラクイラの裁判所": {"S10 p3019"}, "住民の気持ちの高ぶり": {"S10 p3019"},
        },
        REC_MECH={          # 流れ図に出してよい言葉のうち、役職・罪名でないもの（仕組み・鎖・問いの箱と矢印の札）
            "議会の報告書",                                         # c113（S1＝議会の調査委員会の最終報告）
            "ダムを高くする", "ためる水が増える", "つくれる電気が増える",   # c207（S1 p63「capacità … elevata」「producibilità annua」）
            "会社",                                                 # c418
            "22回の実験", "波の高さ",                               # c510（S1 p89「i 22 esperimenti compiuti」・S9 p2010「l'entità dell'onda」）
            "1960年", "1962年", "1963年", "10月8日の報告",          # c621（S1 p96＝国の監督の担当者の10月8日の報告）
            "大きな湖",                                             # 🆕 ⑤b-8 c204（S1 p51「serbatoio del Vajont」）
        },
        REC_CHIP={          # 札（chip）の言葉 → 頁の集合
            "1963年10月11日": {"S1 p99"}, "1963年11月1日": {"S1 p99"},                 # c113
            "少数派「隠した」": {"S1 p232"},                                            # c418（occultamento）
            "最も破局的な崩れ": {"S1 p89"},                                            # c510「il più catastrofico prevedibile crollo franoso」
            "いつも2つの塊（少数派）": {"S1 p224"},                                    # c510「sempre partendo dall'ipotesi che si trattasse di due frane distinte」
            # 🆕 ⑤b-8：c204（S1 p51「centrale」「serbatoio」）・ca13（S10 p3019「giudice naturale」＝地元の裁判所・「su ordinanza della
            #   Cassazione adducendo il motivo」）
            "電気をつくる": {"S1 p51"}, "発電のための水がめ": {"S1 p51"},
            "地元": {"S10 p3019"}, "最高裁判所が挙げた理由": {"S10 p3019"},
        },
        # 書類の再現図（表題 → dict(fields・ends・values＝記録の文にある値だけ・rec＝頁の集合)）。🆕 16本目は欄の値に**原文のイタリア語**を
        #   そのまま書く（日本語は字幕だけ＝映像方針の c413・c422 の決め）。欄の名は原文の文の言葉（domanda→問い・risposto→答え・titolo→見出し・
        #   prima preoccupazione→第一の心配・è necessario→必要なこと・ondate→波・concludeva→結論・nei riguardi→何に対して・parere→意見・
        #   ricerche→研究・lago pieno→湖が満ちたとき・svaso rapido→急に下げるとき・versante→斜面）
        REC_FORM={
            "ミュラーの報告（少数派の報告が引く）": dict(                                       # c413：S1 p217
                fields={"問い", "答え"}, ends=set(), rec={"S1 p217"},
                values={"問い": "se questi franamenti possono venire arrestati mediante misure artificiali",
                        "答え": "deve essere risposto negativamente in linea generale"}),
            "ウニタの記事（1961年2月21日）": dict(                                            # c422：S1 p39
                fields={"見出し"}, ends=set(), rec={"S1 p39"},
                values={"見出し": "Una enorme massa di 50 milioni di metri cubi minaccia la vita e gli averi degli abitanti di Erto"}),
            "会社の記録（1960年11月16日）": dict(                                             # c502：S1 p75（⚠️ 原文の PDF の文字は「divello」＝livello の崩れ）
                fields={"第一の心配", "必要なこと", "波"}, ends=set(), rec={"S1 p75"},
                values={"第一の心配": "garantire l'incolumità delle persone che abitano nella valle",
                        "必要なこと": "abbassare il livello del serbatoio",
                        "波": "non possano assolutamente raggiungere la zona abitata"}),
            "ゲッティの報告（1962年7月3日）": dict(                                           # c512：S1 p89
                fields={"結論", "何に対して"}, ends=set(), rec={"S1 p89"},
                values={"結論": "la quota 700 può considerarsi di assoluta sicurezza",
                        "何に対して": "del più catastrofico prevedibile evento di frana"}),
            "模型の研究所の委員会": dict(                                                    # c517：S1 p225（4月30日）・S9 p2012（3月30日）＝月が割れる
                fields={"意見", "研究"}, ends=set(), rec={"S1 p225", "S9 p2012"},
                values={"意見": "almeno per il momento non siano da compiere ricerche",
                        "研究": "propagarsi di una onda di piena a valle della diga"}),
            "土木局の手紙（1961年1月7日）": dict(                                             # c617：S1 p78〜p79（lettera 7 gennaio 1961）
                fields={"湖が満ちたとき", "急に下げるとき", "斜面"}, ends=set(), rec={"S1 p79", "S1 p78"},
                values={"湖が満ちたとき": "le acque, eventualmente infiltratesi nel terreno",
                        "急に下げるとき": "possano mettersi in pressione",
                        "斜面": "pregiudicando la stabilità del versante"}),
            # 🆕 2026-10-01（16本目 ⑤b-6b）：第7・10章の書類の再現図（欄の値＝原文のイタリア語）
            # c705・c707：S1 p96（議会の報告書が引くビアデーネの10月9日の手紙）「Le fessure sul terreno, gli avvallamenti sulla strada, la evidente
            #   inclinazione degli alberi sulla costa che sovrasta la " Pozza ", l'aprirsi della grande fessura che delimita la zona franosa, il
            #   muoversi dei punti anche verso la " Pineda " che finora erano rimasti fermi, fanno pensare al peggio」（Pineda の引用符は外した）・
            #   「questa mattina dovrebbe essere a quota 700. « Penso di raggiungere quota 695 sempre allo scopo di creare una fascia di sicurezza
            #   per le ondate」。欄の名＝fessure・avvallamenti・alberi→地面と道と木・grande fessura→大きな亀裂・punti→目印・questa mattina→
            #   今朝の水位・raggiungere quota→下げる先・allo scopo di→ねらい
            "ビアデーネの手紙（議会の報告書が引く）": dict(
                fields={"地面と道と木", "大きな亀裂", "目印"}, ends=set(), rec={"S1 p96"},
                values={"地面と道と木": "Le fessure sul terreno, gli avvallamenti sulla strada, la evidente inclinazione degli alberi",
                        "大きな亀裂": "l'aprirsi della grande fessura che delimita la zona franosa",
                        "目印": "il muoversi dei punti anche verso la Pineda che finora erano rimasti fermi"}),
            "ビアデーネの手紙（続き）": dict(
                fields={"今朝の水位", "下げる先", "ねらい"}, ends=set(), rec={"S1 p96"},
                values={"今朝の水位": "questa mattina dovrebbe essere a quota 700",
                        "下げる先": "Penso di raggiungere quota 695",
                        "ねらい": "creare una fascia di sicurezza per le ondate"}),
            # ca09：S1 p241（もう1つの少数派の報告）「dalla tesi, piuttosto affermata che dimostrata, secondo cui la sciagura del Vajont ha avuto
            #   tutti i caratteri della assòluta imprevedibilità」（⚠️ 原文の PDF の文字「assòluta」＝assoluta の崩れ＝直して書いた）。
            #   欄の名＝tesi→退ける説（「non accettazione … dei giudizi conclusivi」が退ける説）・piuttosto affermata→その説は
            "もう1つの少数派の報告": dict(
                fields={"退ける説", "その説は"}, ends=set(), rec={"S1 p241"},
                values={"退ける説": "la sciagura del Vajont ha avuto tutti i caratteri della assoluta imprevedibilità",
                        "その説は": "piuttosto affermata che dimostrata"}),
            # ca19：S9 p2018（財団の年表が記す判決）「1969 … Non viene riconosciuta la prevedibilità della frana」・「1971 … colpevoli di un unico
            #   disastro: inondazione aggravata dalla previsione dell'evento compresa la frana e gli omicidi」。🔴 PLAN の S2 p.718（判決の複写＝
            #   画像だけ）は照らせない＝この頁に当て直した。欄の名＝processo di primo grado→一審・Processo di Cassazione→破毀院
            "判決（財団の年表が記す）": dict(
                fields={"一審", "破毀院"}, ends=set(), rec={"S9 p2018"},
                values={"一審": "Non viene riconosciuta la prevedibilità della frana",
                        "破毀院": "inondazione aggravata dalla previsione dell'evento compresa la frana"}),
        },
        REC_CAUSE={         # 並べ図の項目 → 頁（c419＝2つの見方を同じ形で並べる・どちらかに決めない）
            "多数派「確認できない」": {"S1 p179"}, "少数派「隠した」": {"S1 p232"},
            # 🆕 2026-10-01（16本目 ⑤b-6b）
            # ca04・ca10：S1 p26「La Commissione ha approvato — con 19 voti favorevoli e 8 contrari — la relazione … alla relazione finale siano
            #   allegate le due relazioni di minoranza」（多数派 p178・少数派 p207・もう1つの少数派 p241）
            "多数派の報告": {"S1 p26", "S1 p178"}, "少数派の報告": {"S1 p26", "S1 p207"}, "もう1つの少数派の報告": {"S1 p26", "S1 p241"},
            # ca17：S9 p2018（控訴審）「riconosce la totale colpevolezza di Biadene e Sensidoni … Frosini e Violin vengono assolti per insufficienza
            #   di prove; Marin e Tonini assolti perché il fatto non costituisce reato; Ghetti per non aver commesso il fatto」・「con lo stralcio
            #   della posizione di Batini, gravemente ammalato」＝有罪2・無罪5・外れた1（11−亡くなった3＝8）
            "有罪 2人": {"S9 p2018"}, "無罪 5人": {"S9 p2018"}, "裁判から外れた 1人": {"S9 p2018"},
            # cb12・cb13：多数派 S1 p178「l'evento, così come si è manifestato, non fu previsto da nessuno」・少数派 S1 p207「un evento prevedibile
            #   e probabile, e quindi evitabile」・破毀院 S9 p2018「inondazione aggravata dalla previsione dell'evento compresa la frana」
            "多数派「その形は誰も予見せず」": {"S1 p178"}, "少数派「予見でき、防げた」": {"S1 p207"},
            "破毀院「予見していた重い過失」": {"S9 p2018"},
        },
    ),
    "check_mech": dict(
        # 🆕 16本目 ⑤b-4：断面の図解（vsec）の記録＝門番の側（§5b-88＝型の定数〈vsec16・illu〉を読まない）
        REC_VSEC=dict(dam=dict(height=261.6, crest=725.5, base=22.11, top=3.40, lake=722.5, src="S9 p2006・S1 p63"),
                      # 🆕 ⑤b-6a：c209 の上から見た弓＝天端の弦・天端の長さ・上の厚さ（S9 p2006「190,15 metri di lunghezza al coronamento …
                      #   3,40 metri di spessore alla sommità; 168 metri di corda in sommità」）
                      arch=dict(chord=168.0, length=190.15, top=3.40, src="S9 p2006"),
                      lake=dict(marks=650.0, two=650.0, pair=650.0, probe=650.0, model=700.0, seep=702.5),
                      cover=(10.0, 20.0, "S1 p74（崩れた土の厚さ10〜20m）"), borings=(3, "S1 p148（試し掘り3本）"),
                      tunnels=(2, "S1 p148（横穴2本）")),
        # 🆕 16本目 ⑤b-5（2026-10-01）：水位と斜面の速さの線（lv＝`tools/lv16.py`）
        # 🔴 記録＝門番の側（§5b-88＝型〈lv16〉も ss の点の表〈LVP〉も読まない）。原文 ref/ep16/src/ep16_pages.txt で当てた
        #    （S1＝議会の調査委員会の最終報告 PDF の頁 p1〜p248・S8＝学術の総説の冊子の頁 p1041〜・S9＝財団の年表 PDF p2001〜）。
        #    行＝((日付の窓の頭, 尻), (値の下限, 上限), {頁})。月だけの記録（「nel marzo 1960」）は窓をその月まるごと・
        #    「primi di ottobre」＝1〜10日・「metà」＝11〜20日・「fine」＝21〜末日。値の「circa」は書いた値のまま（幅は丸めの外に広げない）
        REC_LV=dict(
            z=[  # 湖の水位（m）
                (("1960-03-01", "1960-03-31"), (580, 580), {"S1 p72"}),             # p72「iniziate dalla quota 580 nel marzo 1960」
                (("1960-10-01", "1960-10-10"), (630, 630), {"S1 p73"}),             # p73「fino all'ottobre 1960, quando il lago raggiunse la quota 630 circa. Dai primi di ottobre」
                (("1960-11-04", "1960-11-04"), (650, 650), {"S1 p72", "S1 p73", "S8 p1046"}),  # p72「La frana del 4 novembre 1960 … raggiunse quota 650」
                (("1961-01-01", "1961-01-15"), (600, 600), {"S8 p1046"}),           # 「slowly reduced to 600 m a.s.l. (reached at the beginning of January 1961)」
                (("1961-10-11", "1961-10-20"), (600, 600), {"S1 p88", "S1 p90"}),   # p90「Dalla metà dell'ottobre 1961, cioè da quando fu ripreso l'invaso」・p88「reinvaso dalla quota 600」
                (("1962-01-28", "1962-01-28"), (655, 655), {"S1 p87"}),             # p87「La detta quota di m. 655 venne gradualmente raggiunta il 28 gennaio」
                (("1962-10-21", "1962-10-31"), (690, 690), {"S1 p90"}),             # p90「alla fine di ottobre 1962, quando il livello del lago venne portato dalla quota 690 alla quota 700」
                (("1962-12-01", "1962-12-31"), (700, 700), {"S1 p90", "S8 p1046"}), # p90「nel dicembre 1962, col lago alla quota 700」・S8「in December 1962, it reached 700 m」
                (("1963-02-01", "1963-02-28"), (680, 680), {"S1 p90"}),             # p90「nel febbraio 1963, col lago a quota 680 circa」
                (("1963-03-01", "1963-03-31"), (650, 650), {"S1 p90", "S1 p93", "S8 p1046"}),  # p93「nel marzo successivo, col lago alla quota di 650 circa」
                (("1963-04-10", "1963-04-10"), (647.5, 647.5), {"S1 p226"}),        # p226「Dal 10 aprile … il terzo invaso … partendo da quota 647,5」
                (("1963-08-14", "1963-08-14"), (705, 706), {"S1 p226"}),            # p226「alla data del 14 agosto a quota 705-706 metri」
                (("1963-09-01", "1963-09-01"), (709.4, 709.4), {"S9 p2014", "S1 p93"}),  # S9「1° settembre. La quota dell'acqua raggiunge m. 709,40」
                (("1963-09-26", "1963-09-26"), (710, 710), {"S9 p2014", "S1 p226"}),     # S9「con piccole oscillazioni fino a m 710, l'acqua resterà fino al 26 settembre」
                (("1963-10-08", "1963-10-08"), (702.5, 702.5), {"S1 p96"}),         # p96「a quota 702,50 (8 ottobre 1963) con decremento di un metro al giorno」
                (("1963-10-09", "1963-10-09"), (700, 700.42), {"S1 p96", "S9 p2017"}),   # p96「questa mattina dovrebbe essere a quota 700」・S9 p2017「a quota 700,42」
            ],
            v=[  # 斜面の目印が1日に動く距離（ミリ）。「ほぼ0」＝(0, 1)
                (("1960-03-01", "1960-03-31"), (0, 1), {"S1 p72"}),                 # p72〜73「non diedero luogo ad alcuna rilevabile accelerazione … velocità che rimase pressoché nulla fino all'ottobre 1960」
                (("1960-10-01", "1960-10-10"), (0, 1), {"S1 p73"}),                 # p73「Dai primi di ottobre … da quasi zero」
                (("1960-11-04", "1960-11-04"), (35, 40), {"S1 p73"}),               # p73「raggiunse quasi 4 centimetri al giorno fra i primi di ottobre ed il 4 novembre」
                (("1961-01-01", "1961-01-15"), (0, 1), {"S1 p85"}),                 # p85「fino a praticamente annullarsi nella prima metà del gennaio 1961」
                (("1962-08-01", "1962-10-10"), (0, 1), {"S1 p92", "S1 p90"}),       # p92「Dal gennaio 1961 fino al settembre-ottobre 1962 … velocità pressocchè nulle」
                (("1962-12-01", "1962-12-31"), (15, 15), {"S8 p1046"}),             # S8「in December 1962 … the displacement rates exceeded 1.5 cm per day」（S1 p90 は約1cm＝台本は S8）
                (("1963-03-01", "1963-03-31"), (0, 1), {"S1 p93", "S8 p1046"}),     # p93「nel marzo successivo … era pressoché nulla」・S8「the movements on the slope stopped」
                (("1963-09-02", "1963-09-02"), (6.5, 6.5), {"S9 p2014", "S1 p93"}), # S9「il 2 6,5 mm」・p93「da mm/g 6,5 del 2 settembre」
                (("1963-09-15", "1963-09-15"), (12, 12), {"S9 p2014"}),             # S9「il 15 settembre 12 mm」
                (("1963-09-26", "1963-09-26"), (22, 22), {"S9 p2014"}),             # S9「il 26 22 mm」
                (("1963-10-02", "1963-10-03"), (40, 40), {"S9 p2014"}),             # S9「il 2 ed il 3 ottobre 40 mm」
                (("1963-10-08", "1963-10-08"), (100, 100), {"S1 p96"}),             # p96（10月8日の報告）「toccando oggi il valore di circa 10 cm/giorno」
                (("1963-10-09", "1963-10-09"), (200, 200), {"S9 p2014", "S1 p93"}), # S9「fino ai 200 mm del 9 ottobre」
            ],
        ),
        # 横の線＝(段, 下限, 上限, 引き始めてよい日〈None＝軸の端から〉, {頁})
        REC_LV_REF=[
            ("z", 700, 700, None, {"S1 p89"}),              # 模型の結論 p89「la quota 700 può considerarsi di assoluta sicurezza」
            ("z", 715, 715, "1963-05-04", {"S1 p92"}),      # p92「alla quota 715 e l'autorizzazione venne concessa il 4 maggio 1963」
            ("z", 725.5, 725.5, None, {"S9 p2006"}),        # 天端 S9 p2006「725,50 metri di quota del coronamento」
            ("v", 35, 40, None, {"S1 p73", "S1 p93"}),      # 1960年11月の崩落のときの速さ（p73 quasi 4 cm）＝p93「avvicinarsi … ai valori … della frana del novembre 1960」
        ],
        # 縦の線（ev）と帯（band）の日＝(窓, {頁})
        REC_LV_DATE=[
            (("1960-11-04", "1960-11-04"), {"S1 p72", "S1 p73"}),           # 1960年11月4日の崩落
            (("1961-01-01", "1961-01-15"), {"S1 p85", "S8 p1046"}),         # 1961年1月の前半（止まる）
            (("1963-04-10", "1963-04-10"), {"S1 p226"}),                    # 3回目の水ための始まり
            (("1963-05-01", "1963-05-31"), {"S1 p93"}),                     # p93「tra il maggio e l'agosto 1963 segnò accelerazioni non rilevanti」の頭
            (("1963-08-01", "1963-08-31"), {"S1 p93"}),                     # 同じ区間の尻
            (("1963-08-11", "1963-08-20"), {"S1 p93", "S1 p96"}),           # 8月の半ば＝速まり始め（p93「Nella metà dell'agosto」・p96「Dalla metà di agosto」）
            (("1963-09-26", "1963-09-26"), {"S9 p2015", "S9 p2014"}),       # S9 p2015「26 settembre. Biadene decide di iniziare l'opera di svaso」
            (("1963-10-08", "1963-10-08"), {"S1 p96"}),                     # 国の監督の担当者の10月8日の報告
        ],
        # 線を切ってよい区間＝(段, 頭の窓, 尻の窓, {頁})＝数の記録が無い区間だけ
        REC_LV_BRK=[
            ("v", ("1963-03-01", "1963-03-31"), ("1963-09-02", "1963-09-02"), {"S1 p93", "S8 p1046"}),  # 5〜8月は「目立った速まり無し」だけ・数は9月2日から
        ],
    ),
    "check_illu": dict(
        # 🔴 記録の値は門番の側に持つ（型の定数を読まない＝§5b-88）。頁は ss.REC_DOCS の通し番号
        REC_ELEV={700.0: "S1 p96（その朝・その夜の水位＝約700m）", 695.0: "S1 p96（695mまで下げるつもり）",
                  725.5: "S9 p2006（天端725.50m）", 866.0: "S1 p146（積もった土砂の頂上＝866m）", 930.0: "S1 p146（北の岸で930m）・S1 p72（亀裂の谷）",
                  # 🆕 ⑤b-4（VD）：亀裂の折れ目・1960年の水位・模型の範囲・1961年の水位・最高水位
                  1200.0: "S1 p72（亀裂は1,200mまで上り）・S1 p89（模型は1,200mまで）", 1260.0: "S1 p72（また1,260mまで）",
                  1030.0: "S1 p72（1,030mへ）", 650.0: "S1 p72（1960年11月4日の水位650m）",
                  600.0: "S1 p89（模型は600mから）・S8 p1046（1961年1月に600m）", 722.5: "S1 p224（最高水位722.5m）"},
        REC_GAP={25.0: (725.5 - 700.0, "S9 p2006・S1 p96（天端まで25mあまり）"),
                 165.0: (866.0 - 700.0, "S1 p146（崩れる前の水面より165m）"),
                 200.0: (930.0 - 700.0, "S1 p146（崩れる前の水面より200m）")},
        REC_RANGE={(300.0, 400.0): "S8 p1046（水平に300〜400m）"},
        REC_SEC=dict(north=(930.0, "S1 p146"), peak=(846.0, 866.0, "S1 p146（866m）"), shift=(300.0, 400.0, "S8 p1046"),
                     thick=(330.0, "S1 p144（厚さ最大約330m）"), over=(100.0, 140.0, "S8 p1041（140m）・p1047（100m以上）"),
                     crest=(725.5, "S9 p2006"), height=(261.6, "S9 p2006"), lake=(700.0, "S1 p96"), l695=(695.0, "S1 p96")),
        # 🆕 ⑤b-4：VD（正面から見た斜面）の記録（門番の側＝§5b-88。型の VD_CRACK・VD_1960・VD_MODEL_Z・VD_PEAK・VD_WAVE_H を読まない）
        REC_VD=dict(crack=((1200.0, 930.0, 1260.0), 1030.0, "S1 p72（1,200m まで上り・930m まで下り・1,260m・1,030m）"),
                    c1960_top=(850.0, "S1 p72（400〜850m の間）"), c1960_from_dam=(400.0, 600.0, "S1 p82（ダムの約500m上流）"),
                    model_z=(600.0, 1200.0, "S1 p89（標高600〜1,200m）"), model_split="S1 p224（マッサレッツァの沢の東と西）",
                    peak=(846.0, 866.0, "S1 p146（積もった土砂の頂上866m）"), wave=(25.0, "S1 p97（波は25メートル）"),
                    water={600.0: "S8 p1046", 650.0: "S1 p72", 700.0: "S1 p96・S1 p224", 722.5: "S1 p224"}),
        REC_LEN_KM={1.8: (1800.0, "S1 p89（前の幅1.8キロ）")},
        # 🔴 16本目 ⑤b-2：置き場 VA の記録の値を**門番の側に**持つ（型の定数を読まない＝ルール §5b-88。型の点を壊すと捕まる）
        REC_VA=dict(tunnel_km=(2.5, 0.25, "S1 p85（入口はダムの約2,500m上流）"),
                    marks_km=(1.1, 0.15, "S1 p146（ダムの真横と約1.1km上流）"),
                    slide_km=(1.7, 0.2, "S1 p144（幅およそ1.7キロ）"),
                    slide_km2=(1.9, 0.19, "S1 p144（面積およそ1.9平方キロ）"),
                    shift_m=(300.0, 400.0, "S8 p1046（水平に300〜400m）")),
        VA_GRID_PX=185.9,                   # #100 の 1 km 方眼（measure_map16.py grid の実測）
    ),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・titan_fig.GEO・（gate を渡せば）その門番の記録の表を16本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss と GEO は触らない）＝14・15本目の見本 `fixture_ep14`・
    `fixture_ep15` と重ねるとき（check_mech の selftest は14・15・16本目の検算を1つの処理で回す＝先に14本目を全部差し込み、
    15・16本目は表だけ足す）。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が16本目の表で
       18本目の画を測る）。apply の前に**無かった名**（ss の LVP・FLP・FORM_MUELLER …／門番の表）も覚えて、restore で**消す**
       ＝selftest のあとに16本目の名が本番へ残らない（fixture_ep15 と同じ作り）"""
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


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。
    ss と門番の表は、apply の前に無かった名を消す。GEO は fixture_ep14・15 と同じに、覚えた写しで入れ替える（clear → update）。
    tables_only で差し込んだ分は ss・GEO を覚えていない＝戻さない（先に差し込んだ別の見本を壊さない）。LIFO（あとに apply した順）"""
    while _SAVED:
        s = _SAVED.pop()
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
