# -*- coding: utf-8 -*-
"""第6章　空を閉じる c701–c716（16カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c7.py`）。
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
    'c701': dict(kind='写真',
               plan="LCA05｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：右へ流す｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：9:25 の語り｜台本の画：実写 当日の世界貿易センター（A・Commons の説明に当日の日付がある14点から・両棟が燃える時刻の点だけ・全画面・右へ流す＝副題は絵を見て書く）",
               src='図表 p33（`nationwide ground stop`）・委員会報告 p25（`the Command Center ordered one at 9:25`）'),
    'c702': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（空港の点が止まる＝離陸の停止・「本部は話し合い中」の札）',
               src='委員会報告 p25（`A manager at the Herndon Command Center asked FAA headquarters if they wanted to order a`・`While this was being discussed by executives at FAA headquarters, the Command Center ordered one at 9:25`）'),
    'c703': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（アメリカン航空の便の点が止まる＝9:00 北東部・9:05〜9:10 全米）',
               src='委員会報告 p9（`He ordered all American Airlines flights in the Northeast that had not taken off to remain on the ground`・`extended the ground stop nationwide`）・p10（`nationwide ground stop between 9:05 and 9:10`）'),
    'c704': dict(kind='図解',
               plan='台本の画：図 模式 コマンドセンターの卓の配置（人は描かない）',
               src='委員会報告 p29（`The Command Center’s national operations manager, Ben Sliney`）'),
    'c705': dict(kind='写真',
               plan='P122｜副題：当日のペンタゴンの煙（遠くから）｜動き：ゆっくり寄る｜権利：A（米海軍の職務）｜出典の行：米海軍｜台本の画：実写 当日のペンタゴン（米軍の写真・A・別の点・煙の柱の遠景＝副題は絵を見て書く）',
               src='委員会報告 p29（`At 9:42, the Command Center learned from news reports that a plane had struck the Pentagon`）・スタッフ声明 p15（`At 9:42, Command Center learned from television news reports`）'),
    'c706': dict(kind='写真',
               plan="LCA10｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：ゆっくり引く｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：9:45ごろの語り｜台本の画：実写 当日の世界貿易センター（A・別の点・両棟が燃える時刻の点だけ＝副題は絵を見て書く）",
               src='委員会報告 p29（`ordered all FAA facilities to instruct all aircraft to land at the nearest airport`）'),
    'c707': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（飛んでいる機の点が、いちばん近い空港へ向かう矢印）',
               src='—'),
    'c708': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（命令の時刻の札は空白）',
               src='委員会報告 p29（`This was an unprecedented order`）'),
    'c709': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（命令の札を2つ並べる＝報告書と証言・時刻と言葉は字幕だけ）',
               src='運輸長官の証言（`at approximately 9:45 a.m.`・`I gave the FAA the final order for all civil aircraft to land at the nearest airport as soon as possible`）'),
    'c710': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（2つの札に「報告書」「本人の証言」）',
               src='—'),
    'c711': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（点が減っていく・数の札「約4,500機」）',
               src='委員会報告 p29（`The air traffic control system handled it with great skill, as about 4,500 commercial and general aviation aircraft soon landed without incident`）'),
    'c712': dict(kind='写真',
               plan='WH712｜副題：当日、大統領専用機の機内｜動き：ゆっくり寄る｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Eric Draper（Courtesy George W. Bush Presidential Library）｜注：電話をする大統領（サラソタからの飛行中＝説明）・撮影の時刻は書かない｜台本の画：実写 大統領専用機の機内で電話をする大統領（ホワイトハウスの写真係・A・全画面・ゆっくり寄る・撮影の時刻は書かない＝副題「当日、大統領専用機の機内」）',
               src='委員会報告 p39（`Air Force One departed at about 9:54 without any fixed destination`）'),
    'c713': dict(kind='写真',
               plan='🔧 W606｜区間 195.5〜200.5秒｜倍率 1.13（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日、ルイジアナ州の空軍基地に着いた専用機｜動き：映像｜権利：A（ホワイトハウス通信局 WHCA＝国防総省の機関の職務・大統領図書館「public domain」）｜出典の行：Courtesy George W. Bush Presidential Library（WHTV 606）｜注：🔧 写真（手前に記者）→ WHTV 606 の到着の区間（タラップを降りる人・196〜200秒を1秒おき）＝モザイク不要｜台本の画（🔧映像方針で替えた＝元の予定）：実写 バークスデール空軍基地の大統領（ホワイトハウスの写真係・A・手前の記者は顔だけモザイク・全画面＝副題「当日、ルイジアナ州の空軍基地」）',
               src='委員会報告 p325（`Air Force One flew to Barksdale Air Force Base in Louisiana`）'),
    'c714': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（点が空港へ降りきる）',
               src='委員会報告 p31（`thought outside the box in recommending a nationwide alert, in ground-stopping local traffic, and, ultimately, in deciding to land all aircraft and executing that unprecedented order flawlessly`）'),
    'c715': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図',
               src='—'),
    'c716': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（9:42 に報道で知る〜9:46・93便はすでに乗っ取られている）',
               src='委員会報告 p29（`At 9:46 the Command Center updated FAA headquarters that United 93 was now "twenty-nine minutes out of Washington, D.C."`）'),
}

SPEC = {}
