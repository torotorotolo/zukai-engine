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
    'c602': dict(kind='図・写真の頁',
               plan='見る向き：上から｜注：NTSB 77便の経路｜台本の画：図 NTSB 77便の経路（PDF p5 の地図をなぞる・南へ曲がり、東へ戻る線）',
               src='委員会報告 p8（`The hijacking began between 8:51 and 8:54`）・p24（`American 77 began deviating from its flight plan at 8:54, with a slight turn toward the south`）'),
    'c603': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（インディアナポリス・センターのレーダー再生の画面・77便の札が消える所）',
               src='委員会報告 p25（`its transponder was turned off at 8:56`）'),
    'c604': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（同じ画面・点の無いまま時計が進む）',
               src='委員会報告 p25（`FAA radar equipment tracked the flight from the moment its transponder was turned off at 8:56`・`for 8 minutes and 13 seconds, between 8:56 and 9:05, this primary radar information on American 77 was not displayed to controllers at Indianapolis Center`）'),
    'c605': dict(kind='図解',
               plan='台本の画：図 模式 レーダーの重ね方（一次レーダーの点・札・画面＝人は描かない）',
               src='委員会報告 p25（`The reasons are technical, arising from the way the software processed radar information`）'),
    'c606': dict(kind='図・写真の頁',
               plan='見る向き：上から｜台本の画：図 NTSB 77便の経路（同じ地図・管制官が西と南西を見る矢印と、東へ向かう線）',
               src="委員会報告 p25（`looked to the west and southwest along the flight's projected path, not east`）"),
    'c607': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（9:05 に東で点が戻る所）',
               src='委員会報告 p25（`reemerged as a primary target on Indianapolis Center radar scopes at 9:05, east of its last known position`・`controllers had either stopped looking for the aircraft because they thought it had crashed or were looking toward the west`）'),
    'c608': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（西を見る矢印と、東へ伸びる線を並べる）',
               src='委員会報告 p25（`Indianapolis Center never saw Flight 77 turn around`）'),
    'c609': dict(kind='写真',
               plan="LCA09｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：右へ流す｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：9:10 の語り｜台本の画：実写 当日の世界貿易センター（A・別の点・両棟が燃える時刻の点だけ・全画面・左へ流す＝副題は絵を見て書く）",
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
    'c615': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（ダレスのレーダー再生・東へ速く動く点）',
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
               plan='P009｜副題：当日のペンタゴン（海軍別館から見た煙）｜動き：ゆっくり寄る｜権利：A（米海兵隊の職務）｜出典の行：米海兵隊（Cpl J. Ingersoll）｜注：衝突の数分後（説明）。遠くの人は原寸でも顔が分からない｜台本の画：実写 当日のペンタゴン（米軍の写真・A・Commons の説明に当日の日付・煙の上がる遠景・全画面・ゆっくり寄る＝副題は絵を見て書く）',
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
