# -*- coding: utf-8 -*-
"""第5章　3機目　画面から消えた点 c601–c624（24カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c6.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep21/make_plan21.py` で
  映像方針の一覧 `ref/ep21/eizou_build/list21.tsv`（了承②ずみ・E 0）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット（台本の画は元の予定）。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c601': dict(kind='写真',
               plan='PENT98｜副題：事件の前のペンタゴン（1998年）｜動き：ゆっくり寄る｜権利：A（国防総省の職務）｜出典の行：米国防総省（MSgt Ken Hammond, USAF）｜台本の画：実写 pentagon_ext_pre（事件の前のペンタゴン・1998年・A・全画面・ゆっくり寄る＝副題「事件の前のペンタゴン（1998年）」）',
               src='委員会報告 p8（`At 8:51, American 77 transmitted its last routine radio communication`）'),
    # 🔧 ⑤b-4（2026-10-12）：台本の画の欄の「PDF p5」は中身から見て p3（図1＝全体の経路）。p5 は図3（ワシントンの辺り＝c617）
    'c602': dict(kind='図・写真の頁',
               plan='見る向き：上から｜注：NTSB 77便の経路（🔧 PDF p3 の図1）｜台本の画：図 NTSB 77便の経路（PDF p5 の地図をなぞる・南へ曲がり、東へ戻る線）',
               src='委員会報告 p8（`The hijacking began between 8:51 and 8:54`）・p24（`American 77 began deviating from its flight plan at 8:54, with a slight turn toward the south`）'),
    # 🔧 ⑤b-4：c603・c604・c607・c615 は図・写真の頁 → 図解。RG237 の77便の動画（1-AWA-716-Pentagon）は描き終えた航跡の地図だけで、
    #   札も「点が消える・戻る」も写っていない。213番台（Pentagon_more2）は NORAD の立体のアニメーション（「AA 77」の札つき＝c615「正体も
    #   分からない」と食い違う）＝レーダーの画面の模式図（mech21 scope）で見せる。c606 は NTSB の頁 → 北東部の地図の模式（77便の線と探した向き）
    'c603': dict(kind='図解',
               plan='🔧 模式 レーダーの画面（札が消え、点も消える）｜台本の画：図 RG237（インディアナポリス・センターのレーダー再生の画面・77便の札が消える所）',
               src='委員会報告 p25（`its transponder was turned off at 8:56`）'),
    'c604': dict(kind='図解',
               plan='🔧 模式 レーダーの画面（点の無いまま・記録に残っていた点）｜台本の画：図 RG237（同じ画面・点の無いまま時計が進む）',
               src='委員会報告 p25（`FAA radar equipment tracked the flight from the moment its transponder was turned off at 8:56`・`for 8 minutes and 13 seconds, between 8:56 and 9:05, this primary radar information on American 77 was not displayed to controllers at Indianapolis Center`）'),
    'c605': dict(kind='図解',
               plan='台本の画：図 模式 レーダーの重ね方（一次レーダーの点・札・画面＝人は描かない）',
               src='委員会報告 p25（`The reasons are technical, arising from the way the software processed radar information`）'),
    'c606': dict(kind='図解',
               plan='見る向き：上から｜🔧 模式 北東部の地図（77便の線・西と南西を見る矢印・東への線）｜台本の画：図 NTSB 77便の経路（同じ地図・管制官が西と南西を見る矢印と、東へ向かう線）',
               src="委員会報告 p25（`looked to the west and southwest along the flight's projected path, not east`）"),
    'c607': dict(kind='図解',
               plan='見る向き：上から｜🔧 模式 北東部の地図（9:05 に東で点が戻る）｜台本の画：図 RG237（9:05 に東で点が戻る所）',
               src='委員会報告 p25（`reemerged as a primary target on Indianapolis Center radar scopes at 9:05, east of its last known position`・`controllers had either stopped looking for the aircraft because they thought it had crashed or were looking toward the west`）'),
    'c608': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（西を見る矢印と、東へ伸びる線を並べる）',
               src='委員会報告 p25（`Indianapolis Center never saw Flight 77 turn around`）'),
    'c609': dict(kind='写真',
               plan="LCA09｜副題：当日の世界貿易センター（ビルのあいだに見える塔と煙）｜動き：右へ流す｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：9:10 の語り。⑤b-7：副題を写っているものに（寄った画＝中ほどに塔）｜台本の画：実写 当日の世界貿易センター（A・別の点・両棟が燃える時刻の点だけ・全画面・左へ流す＝副題は絵を見て書く）",
               src='委員会報告 p9（`Shortly before 9:10, suspecting that American 77 had been hijacked, American headquarters concluded that the second aircraft to hit the World Trade Center might have been Flight 77`）・p455（`There is no evidence to indicate that the FAA recognized Flight 77 as a hijacking until it crashed into the Pentagon`）'),
    'c610': dict(kind='図解',
               plan='台本の画：図 模式 機内の電話から地上への線（人は描かない）',
               src='委員会報告 p9（`the hijackers had knives and box cutters`・`they had put all the passengers in the back of the plane`）'),
    'c611': dict(kind='図解',
               plan='台本の画：図 模式 北東部の地図（ボストン・センターから NEADS への電話・「9:21 ボストン・センター→NEADS」の札＝電話の言葉は字幕だけ）',
               src="委員会報告 p26（`I just had a report that American 11 is still in the air, and it's on its way towards`）"),
    'c612': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（北棟に×・11便の札）',
               src='委員会報告 p26（`We have been unable to identify the source of this mistaken FAA information`）'),
    'c613': dict(kind='図解',
               plan='台本の画：図 模式 ラングレーから東の海へ伸びる線',
               src='委員会報告 p27（`That order was processed and transmitted to Langley Air Force Base at 9:24`・`Radar data show the Langley fighters airborne at 9:30`・`not headed north toward the Baltimore area as instructed, but east over the ocean`）'),
    'c614': dict(kind='図解',
               plan='台本の画：図 模式 同じ線（3つの理由の札＝目標の場所が無い・決まった飛び方の型・読み違え）',
               src="委員会報告 p27（`The Langley fighters were heading east, not north, for three reasons`・`this order did not include a distance to the target or the target's location`）"),
    'c615': dict(kind='図解',
               plan='🔧 模式 空港の管制のレーダーの画面（東へ速く動く札の無い点）｜台本の画：図 RG237（ダレスのレーダー再生・東へ速く動く点）',
               src="委員会報告 p25（`observed a primary radar target tracking eastbound at a high rate of speed`・`The aircraft's identity or type was unknown`）"),
    'c616': dict(kind='図解',
               plan='台本の画：図 模式 ワシントンの地図（ホワイトハウス・ペンタゴン・レーガン空港・点の動き）',
               src='委員会報告 p27（`it had come by chance`）・p34（`It was notified at 9:34 that American 77 was lost`・`an unknown plane was 6 miles southwest of the White House`）'),
    'c617': dict(kind='図・写真の頁',
               plan='見る向き：上から｜台本の画：図 NTSB 77便の経路（ペンタゴンの西南西で時計回りに大きく回る線）',
               src='委員会報告 p9（`American 77 was then 5 miles west-southwest of the Pentagon and began a 330-degree turn`）'),
    'c618': dict(kind='図・写真の頁',
               plan='見る向き：横から｜合図：🔁 上から→横から（前の図 c617）＝左上に見る向きの札・替わる瞬間に「横から見ると」｜注：NTSB 77便 図2（高度）｜台本の画：図 NTSB 77便 図2（PDF p4・飛行の記録装置の高度を、点を結んで順に描く）',
               src='委員会報告 p9（`descending through 2,200 feet, pointed toward the Pentagon and downtown Washington`）・NTSB 77便（`Altitude Profile`）'),
    'c619': dict(kind='図解',
               plan='見る向き：上から｜合図：🔁 横から→上から（前の図 c618）＝左上に見る向きの札・替わる瞬間に「上から見ると」｜注：ワシントン上空の地図として描く｜台本の画：図 模式 ワシントン上空（低く飛ぶ軍の輸送機 C-130H と77便の線）',
               src='委員会報告 p25（`vectored an unarmed National Guard C-130H cargo aircraft`）・p26（`identified it as a Boeing 757`）'),
    'c620': dict(kind='写真',
               plan='P009｜副題：当日のペンタゴン（海軍別館から見た煙・手前に街灯）｜動き：ゆっくり寄る｜権利：A（米海兵隊の職務）｜出典の行：米海兵隊（Cpl J. Ingersoll）｜注：衝突の数分後（説明）。遠くの人は原寸でも顔が分からない｜台本の画：実写 当日のペンタゴン（米軍の写真・A・Commons の説明に当日の日付・煙の上がる遠景・全画面・ゆっくり寄る＝副題は絵を見て書く）',
               src='委員会報告 p10（`At 9:37:46, American Airlines Flight 77 crashed into the Pentagon, traveling at approximately 530 miles per hour`）'),
    'c621': dict(kind='写真',
               plan='P000｜副題：当日のペンタゴン｜動き：左へ流す｜権利：A（米空軍の職務）｜出典の行：米空軍（TSgt Jim Varhegyi）｜注：②③で見た｜台本の画：実写 DF-SD-02-09094（米空軍・当日・放水と救急車・軍人と消防・A・全画面・左へ流す＝副題「当日のペンタゴン」）',
               src='委員会報告 p26（`at 9:38, seconds after impact, reported to the control tower`・`looks like that aircraft crashed into the Pentagon sir`）'),
    'c622': dict(kind='写真',
               plan='P032｜副題：当日のペンタゴン（煙が晴れたあとの西側）｜動き：下へ流す｜権利：A（米海兵隊の職務）｜出典の行：米海兵隊（Cpl J. Ingersoll）｜注：原寸の中央2か所＝壊れた内部と配線だけ（遺体なし）｜台本の画：実写 pentagon_west_day（DM-SD-02-03925・米海兵隊・煙が晴れたあとの建物の内側の環・A・全画面・使う窓だけ原寸で見る＝副題「当日のペンタゴン」）',
               src='記念館（`184 people were killed at the Pentagon`）・委員会報告 p552 注188（`attack killed 184 nonterrorists`）'),
    'c623': dict(kind='写真',
               plan='P012｜副題：当日のペンタゴン（炎と放水）｜動き：右へ流す｜権利：A（米海兵隊の職務）｜出典の行：米海兵隊（Cpl J. Ingersoll）｜注：原寸＝消防隊（公務）・負傷者なし｜台本の画：実写 当日のペンタゴン（米軍の写真・A・別の点・衝突のすぐ後の煙＝副題は絵を見て書く）',
               src='委員会報告 p27（`The Langley fighters were about 150 miles away`）'),
    'c624': dict(kind='写真',
               plan='P076｜副題：当日の夕方のペンタゴン｜動き：ゆっくり引く｜権利：A（米海軍の職務）｜出典の行：米海軍（PH2 Jim Watson）｜注：②③で見た｜台本の画：実写 DN-SD-03-11447（米海軍・夕方の西側と消防車・崩れた外の環・A・全画面・右へ流す＝副題「当日の夕方のペンタゴン」）',
               src='委員会報告 p26（`identified it as a Boeing 757`）・注154 p461（`Commission analysis of FDR`）・NTSB 77便 図2（`FDR Pressure Altitude`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-12）：図解 第5章（15カット）＋頁3（c602・c617・c618＝NTSB 77便の図1〜3）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「3機目　画面から消えた点」と4字以上同じ並び（「画面から消」ほか）を見出し・副題に入れない（門番 dup）。人は描かない・
#      無線と電話の逐語は画面に出さない。見る向き：c617（上から）→ c618（横から＝副題の頭「横から見ると」）→ c619（上から＝副題の頭「上から見ると」）
_W = "陸の形は Natural Earth・77便の線と矢印は模式（NTSB 77便の図1の見当）"
SPEC.update({
    # c602（8.1秒）＝NTSB 77便の飛行経路の調べ PDF 3頁（Figure 1・横倒しのスキャンを正立）。南へ曲がって東へ戻る線（点 C・D）
    "c602": dict(photo=ss.page(4003), trim=ss.ptrim("c602"), bias=ss.pbias("c602"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="77便の経路", s="NTSB の飛行経路の調べの図1（77便）"),   # ⑤c'：4便の図1が同じ名だった＝便を足す（年は出典の行）
    # c603（3行）＝🔧 管制のレーダーの画面（模式）。8:56 札が消える → インディアナポリス・センター → 3行目で点も消える（p24・p25）
    "c603": dict(
        t="消えた札と点", s="77便を見守っていた管制の画面",
        fig=("m21", dict(view="scope", start=dict(block="on"),
                         steps=[dict(state=dict(block="off"), tag=dict(t="8:56", at="time")),
                                dict(tag=dict(t="インディアナポリス・センター", at="block")),
                                dict(state=dict(blip="off"), tag=dict(t="点も消える", at="dot", to="blip"))],
                         rel=[dict(t="8:56", src="委員会報告 p25")], note="画面の形と点は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p24", "委員会報告 p25"]))),
    ),
    # c604（3行）＝🔧 同じ画面（点の無いまま）。2行目で記録に残っていた点（あとの調べ）→ 3行目で 8分13秒（p25）
    "c604": dict(
        t="出なかった点", s="インディアナポリス・センターの画面",
        fig=("m21", dict(view="scope", start=dict(block="off", blip="off"),
                         steps=[dict(), dict(state=dict(ghost="on"), tag=dict(t="レーダーの記録には残る", d="あとの調べ", at="ghost")),
                                dict(tag=dict(t="画面に出ない：8分13秒", at="low"))],
                         rel=[dict(t="8分13秒", src="委員会報告 p25")], note="画面の形と点は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p25"]))),
    ),
    # c605（2行）＝レーダーの情報が画面に出るまで。管制のソフトの扱いで画面に出ない → 2行目でその辺りのレーダーの弱さ（p25）
    "c605": dict(
        t="技術の理由", s="レーダーと画面のあいだ",
        fig=("m21", dict(view="soft", steps=[dict(state=dict(rec="on", cut="on"), tag=dict(t="ソフトの扱いで出ない", at="cut")),
                                             dict(state=dict(weak="on"), tag=dict(t="77便の辺りはレーダーが弱い", at="weak"))],
                         rel=[dict(t="77便", src="委員会報告 p25")], note="箱の並びは模式（言葉は委員会報告から）", src=ss.src(["委員会報告 p25"]))),
    ),
    # c606（2行）＝北東部の地図（77便の線＝西へ→消えた所）。管制官が探した西と南西 → 2行目で東への線（p25）
    "c606": dict(
        t="逆の向き", s="インディアナポリス・センターの捜索",
        fig=("m21", dict(view="ne", start=dict(r77="west"),
                         steps=[dict(state=dict(look="on"), tag=dict(t="管制官が探した向き", at="look")),
                                dict(state=dict(r77="east"), tag=dict(t="77便は東へ", at="reapp"))],
                         rel=[dict(t="77便", src="委員会報告 p25")], note=_W, src=ss.src(["委員会報告 p25"]))),
    ),
    # c607（2行）＝同じ地図。9:05 東で点が戻る（p25）→ 2行目で管制官は西を見ていた
    "c607": dict(
        t="戻った点", s="東の方で画面に出た77便",
        fig=("m21", dict(view="ne", start=dict(r77="east", look="on"),
                         steps=[dict(state=dict(reapp="on"), tag=dict(t="9:05", at="reapp", to="r77_reapp")),
                                dict(tag=dict(t="管制官は西を見ていた", at="look"))],
                         rel=[dict(t="9:05", src="委員会報告 p25")], note=_W, src=ss.src(["委員会報告 p25"]))),
    ),
    # c608（3行）＝同じ地図。2行目で向きを変えた所（画面に出ないあいだ）
    "c608": dict(
        t="見ていない旋回", s="77便が向きを変えた所",
        fig=("m21", dict(view="ne", start=dict(r77="east", look="on", reapp="on"),
                         steps=[dict(), dict(state=dict(turn="on"), tag=dict(t="ここで向きを変えた", at="turn", to="r77_turn")), dict()],
                         note=_W, src=ss.src(["委員会報告 p25"]))),
    ),
    # c610（2行）＝機内の電話から地上の家族へ（p9）。言葉は語りと字幕だけ
    "c610": dict(
        t="家族への電話", s="77便の機内から地上へ",
        fig=("m21", dict(view="phone", start=dict(to="family"),
                         steps=[dict(state=dict(call="on"), tag=dict(t="乗客の1人から", at="time")), dict()],
                         rel=[dict(t="1人", src="委員会報告 p9")], note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p9"]))),
    ),
    # c611（3行）＝北東部の地図。2行目でボストン・センター → NEADS の電話（9:21・p26）。言葉は字幕だけ
    "c611": dict(
        t="別の知らせ", s="ボストン・センターから NEADS への電話",
        fig=("m21", dict(view="ne", start=dict(neads="on"),
                         steps=[dict(), dict(state=dict(call="on"), tag=dict(t="9:21", at="call")), dict()],
                         rel=[dict(t="9:21", src="委員会報告 p26")], note="陸の形は Natural Earth・線は模式", src=ss.src(["委員会報告 p26"]))),
    ),
    # c612（3行）＝同じ地図。2行目でニューヨークに×（11便はもう北棟へ）→ 3行目で出どころは分からない（p26）
    "c612": dict(
        t="誤った知らせ", s="NEADS に届いた11便の話",
        fig=("m21", dict(view="ne", start=dict(neads="on", call="on"),
                         steps=[dict(), dict(state=dict(x11="on"), tag=dict(t="11便：30分以上前に北棟へ", at="x11", to="nyc")),
                                dict(tag=dict(t="出どころは分からない", at="src"))],
                         rel=[dict(t="11便", src="委員会報告 p7"), dict(t="30分以上前", src="委員会報告 p7・p26（8:46:40 から 9:21）")],
                         note="陸の形は Natural Earth・線は模式", src=ss.src(["委員会報告 p7", "委員会報告 p26"]))),
    ),
    # c613（2行）＝同じ地図。9:24 ラングレーへ命令 → 2行目で 9:30 東の海へ（命令の向きは北＝ボルチモアの方・p27）
    "c613": dict(
        t="東へ出た戦闘機", s="ラングレー基地からの発進",
        fig=("m21", dict(view="ne", start=dict(bases="on"),
                         steps=[dict(tag=dict(t="9:24 ラングレーへ命令", at="lang_t")),
                                dict(state=dict(lang="on"), tag=dict(t="9:30 東の海の上へ", at="lang"))],
                         rel=[dict(t="9:24", src="委員会報告 p27"), dict(t="9:30", src="委員会報告 p27")],
                         note="陸の形は Natural Earth・線は向きの模式", src=ss.src(["委員会報告 p27"]))),
    ),
    # c614（2行）＝同じ線。2行目で3つの理由（p27）
    "c614": dict(
        t="3つの理由", s="戦闘機が東へ向かったわけ",
        fig=("m21", dict(view="ne", start=dict(bases="on", lang="on"),
                         steps=[dict(), dict(tag=[dict(t="① 行き先と距離の指示なし", at="w1"), dict(t="② 東へ出る決まった飛び方", at="w2"),
                                                  dict(t="③ それを命令より先と思う", at="w3")])],
                         note="陸の形は Natural Earth・線は向きの模式", src=ss.src(["委員会報告 p27"]))),
    ),
    # c615（2行）＝🔧 空港の管制のレーダーの画面（模式）。9:32 東へ速く動く札の無い点 → 2行目で正体の分からない点（p25）
    "c615": dict(
        t="速い点", s="ダレス空港の管制官が見た点",
        fig=("m21", dict(view="scope", start=dict(who="app"),
                         steps=[dict(state=dict(fast="on"), tag=dict(t="9:32", at="time")), dict(tag=dict(t="正体の分からない点", at="dot"))],
                         rel=[dict(t="9:32", src="委員会報告 p25")], note="画面の形と点は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p25"]))),
    ),
    # c616（2行）＝ワシントンの辺りの地図。9:34 NEADS が77便を見失ったと知る → 2行目でホワイトハウスの南西 約10キロ（6マイル）に正体不明の機（p34）
    "c616": dict(
        t="首都の近くに", s="ホワイトハウスの南西に現れた機",
        fig=("m21", dict(view="dc", steps=[dict(tag=dict(t="9:34 NEADS が知る", at="time")),
                                           dict(state=dict(unk="on"), tag=dict(t="約10キロ（6マイル）", d="正体不明の機", at="unk", to="unk"))],
                         rel=[dict(t="9:34", src="委員会報告 p27"), dict(t="約10キロ（6マイル）", src="委員会報告 p34")],
                         note="地点は一般の座標・川は描かない（模式）", src=ss.src(["委員会報告 p27", "委員会報告 p34"]))),
    ),
    # c617（8.7秒）＝NTSB 77便の飛行経路の調べ PDF 5頁（Figure 3・ワシントンの辺り＝330度の旋回）。上から
    "c617": dict(photo=ss.page(4005), trim=ss.ptrim("c617"), bias=ss.pbias("c617"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="最後の旋回", s="NTSB の飛行経路の調べ（2002年）の図3"),
    # c618（11.8秒）＝NTSB 77便 PDF 4頁（Figure 2・飛行の記録装置の気圧高度）。🔁 上から→横から＝副題の頭「横から見ると」
    "c618": dict(photo=ss.page(4004), trim=ss.ptrim("c618"), bias=ss.pbias("c618"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="高度の記録", s="横から見ると：NTSB の飛行経路の調べの図2（77便）"),   # ⑤c'：c806 と同じ名だった＝便を足す
    # c619（2行）＝🔁 横から→上から（副題の頭「上から見ると」）。軍の輸送機 → 2行目で追って見分ける（p25・p26）
    "c619": dict(
        t="輸送機の目", s="上から見ると：ワシントンの辺りの空",
        fig=("m21", dict(view="dc", steps=[dict(state=dict(t77="on", c130="on"), tag=dict(t="軍の輸送機 C-130H", at="c130", to="c130")),
                                           dict(state=dict(follow="on"), tag=dict(t="ボーイング757と見分ける", at="follow"))],
                         rel=[dict(t="C-130H", src="委員会報告 p25"), dict(t="757", src="委員会報告 p26")],
                         note="地点は一般の座標・線は模式", src=ss.src(["委員会報告 p25", "委員会報告 p26"]))),
    ),
})

# ── 🆕 ⑤b-7（2026-10-13）：写真（PLAN＝映像方針の一覧・了承②／書き方は c2.py の ⑤b-7 の注）──
_P98 = P("pentagon_1998")
_A09 = P("lc_a05_a09")
_P009 = P("pen_010911_m_ci426_009")
_P000 = P("df_sd_02_09094")
_P032 = P("dm_sd_02_03925")
_P012 = P("pen_010911_m_ci426_021")
_P076 = P("dn_sd_03_11447")
SPEC.update({
    # c601（9.5秒・章の頭）＝事件の前のペンタゴン（1998年・国防総省）。建物へゆっくり寄る（横 0.55・縦 0.62）
    "c601": dict(photo=_P98, **ss.mv(_P98, "in", 0.55, 0.62), side="none", t="77便の位置", s="事件の前のペンタゴン（1998年）"),
    # c609（15.0秒）＝ビルのあいだに見える塔と煙（議会図書館 A09＝台紙の縁）・右へ流す
    "c609": dict(photo=_A09, **ss.mv(_A09, "r"), side="none", t="本社の疑い", s="当日の世界貿易センター（ビルのあいだに見える塔と煙）"),
    # c620（8.0秒）＝海軍別館から見た煙（米海兵隊・衝突の数分後）。右の煙へゆっくり寄る（遠くの人は原寸でも顔が分からない）
    "c620": dict(photo=_P009, **ss.mv(_P009, "in", 0.6, 0.45), side="none", t="ペンタゴンへ", s="当日のペンタゴン（海軍別館から見た煙・手前に街灯）"),   # ⑤c'：cc02 と書き分け
    # c621（6.1秒）＝放水と救急車・軍人と消防（米空軍）・左へ流す
    "c621": dict(photo=_P000, **ss.mv(_P000, "l"), side="none", t="輸送機の報告", s="当日のペンタゴン"),
    # c622（7.4秒）＝煙が晴れたあとの西側（米海兵隊・壊れた内部と配線だけ）・下へ流す（縦の余地 180px）
    "c622": dict(photo=_P032, **ss.mv(_P032, "d", span=(0.15, 0.85)), side="none", t="184人", s="当日のペンタゴン（煙が晴れたあとの西側）"),
    # c623（7.1秒）＝炎と放水・消防隊（米海兵隊・公務）・右へ流す
    "c623": dict(photo=_P012, **ss.mv(_P012, "r"), side="none", t="戦闘機の位置", s="当日のペンタゴン（炎と放水）"),
    # c624（11.3秒）＝夕方の西側と消防車（米海軍）・ゆっくり引く
    "c624": dict(photo=_P076, **ss.mv(_P076, "out"), side="none", t="旅客機の確認", s="当日の夕方のペンタゴン"),
})
