# -*- coding: utf-8 -*-
"""第4章　2機目　気づいていた管制官 c501–c520（20カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c5.py`）。
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
    'c501': dict(kind='写真',
               plan='WTCSOUTH｜副題：事件の前の世界貿易センター（1976年）｜動き：上へ流す｜権利：D（米議会図書館蔵／知られた制限なし）｜出典の行：Balthazar Korab（米議会図書館蔵）｜注：縦長｜台本の画：実写 wtc_south（事件の前の世界貿易センター・1976年・D・縦長＝全画面で上下を切る・右へ流す＝副題「事件の前の世界貿易センター（1976年）」）',
               src="委員会報告 p21（`At approximately 8:42, shortly after entering New York Center's airspace, the pilot of United 175 broke in`）"),
    'c502': dict(kind='図解',
               plan='台本の画：図 模式 管制の無線（ニューヨーク・センターと175便を結ぶ線）',
               src='委員会報告 p7（`a "suspicious transmission" overheard from another plane (which turned out to have been Flight 11) just after takeoff`・`This was United 175\'s last communication with the ground`）'),
    'c503': dict(kind='図解',
               plan='台本の画：図 模式 175便の機内（前の座席と操縦室の扉＝人は描かない）',
               src='委員会報告 p7（`The hijackers attacked sometime between 8:42 and 8:46`）・NTSB 175便（`at 8:47, when the aircraft changed beacon codes twice within a one-minute period`）'),
    'c504': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（ニューヨーク・センターのレーダー再生の画面・175便の札の番号が変わる所）',
               src='委員会報告 p21（`The New York Center controller and manager were unaware that American 11 had already crashed`・`At 8:51, the controller noticed the transponder change from United 175 and tried to contact the aircraft. There was no response`）'),
    'c505': dict(kind='図解',
               plan='台本の画：図 模式 機内の電話から地上への線（人は描かない）',
               src='委員会報告 p7（`a male flight attendant called a United office in San Francisco`・`both pilots had been killed, a flight attendant had been stabbed`）・p8（`the hijackers were probably flying the plane`）'),
    'c506': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（同じ画面・175便の点が向きを変える）',
               src='委員会報告 p22（`saying that "we may have a hijack" and that he could not find the aircraft`）'),
    'c507': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（175便＝8:53「乗っ取りかもしれない」・8:55 上司へ）',
               src='委員会報告 p22（`At about 8:55, the controller in charge notified a New York Center manager that she believed United 175 had also been hijacked`）'),
    'c508': dict(kind='図解',
               plan='台本の画：図 模式 手順の段（ニューヨーク・センターの上司から地域の管理職へ＝扉が閉じている）',
               src='委員会報告 p22（`The manager tried to notify the regional managers and was told that they were discussing a hijacked aircraft (presumably American 11) and refused to be disturbed`）'),
    'c509': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（同じ画面）',
               src='委員会報告 p22（`we might have a hijack over here, two of them`）'),
    'c510': dict(kind='図解',
               plan='台本の画：図 模式 電話の線（ニューヨーク・センターからハーンドンのコマンドセンターへ）',
               src="委員会報告 p22（`Between 9:01 and 9:02, a manager from New York Center told the Command Center in Herndon`・`We have several situations going on here. It's escalating big, big time. We need to get the military involved with us`）"),
    'c511': dict(kind='図解',
               plan='台本の画：図 模式 北アメリカの地図（バージニア州ハーンドンの印）',
               src='委員会報告 p14（`Command Center, located in Herndon`）・p16（`Virginia, which oversees daily traffic flow within the entire airspace system`）'),
    'c512': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（175便の点がマンハッタンの南部の上で途切れる）',
               src='委員会報告 p22（`Heads up man, it looks like another one coming in`・`the radar data terminated over Lower Manhattan`）'),
    'c513': dict(kind='写真',
               plan="LCA01｜副題：燃える世界貿易センター（当日）｜動き：ゆっくり寄る｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：旧版の wtc_smoke_day の原本（議会図書館 A01）＝両棟が燃える（②③）・サムネの地｜台本の画：実写 wtc_smoke_day（LC-A05-A01・エンパイア・ステート・ビルの向こうで燃える両棟・C'＝米議会図書館蔵（撮影者不詳）・全画面・ゆっくり寄る＝副題「燃える世界貿易センター（当日）」）",
               src='委員会報告 p8（`At 9:03:11, United Airlines Flight 175 struck the South Tower of the World Trade Center`）'),
    'c514': dict(kind='写真',
               plan="LCA03｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：左へ流す｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：9:03 の語り。塔は重なる角度＝「両棟」と副題に書かない｜台本の画：実写 当日の世界貿易センター（A・Commons の説明に当日の日付がある14点から選ぶ・全画面・左へ流す＝副題は絵を見て書く）",
               src='委員会報告 p23（`came in a phone call from New York Center to NEADS at 9:03`・`The notice came at about the time the plane was hitting the South Tower`）'),
    'c515': dict(kind='写真',
               plan="WTC71｜副題：事件の前の世界貿易センター（1971年）｜動き：上へ流す｜権利：D（U.S. News & World Report の写真＝米議会図書館へ譲渡）｜出典の行：Thomas J. O'Halloran（米議会図書館蔵）｜注：9:03 より前の語り＝北棟だけが燃える写真は見つからない（議会図書館の A ロールは A02〜A10 が崩壊前・2本が重なる角度で原寸でも決められない）。白黒・縦長｜台本の画：実写 事件の前の世界貿易センター（D・別の点＝語りは 8:51〜9:02＝両棟が燃える写真は置かない。北棟だけが燃える点が見つかればそれ＝副題は絵を見て書く）",
               src='委員会報告 p22（`refused to be disturbed`・`Between 9:01 and 9:02, a manager from New York Center told the Command Center`）・p23（`came in a phone call from New York Center to NEADS at 9:03`）'),
    'c516': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（11便と175便を並べる・FAA が知った印＝乗っ取りから11分後と9分後）',
               src='委員会報告 p455（`The FAA knew or strongly suspected that Flight 11 was a hijacking 11 minutes after it was taken over; Flight 175, 9 minutes after it was taken over`）'),
    'c517': dict(kind='図解',
               plan='台本の画：図 模式 北東部の地図（ロングアイランドの沖の軍の空域・F-15の線）',
               src='委員会報告 p20（`Lacking a target, they were vectored toward military-controlled airspace off the Long Island coast`）・p23（`decided against holding the fighters in military airspace away from Manhattan`）'),
    'c518': dict(kind='写真',
               plan='WH518｜副題：当日の朝、フロリダ州の小学校（報道を見る大統領）｜動き：2点を順に寄る｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Eric Draper（Courtesy George W. Bush Presidential Library）｜注：説明＝教室で175便の衝突の報道を見る（時刻の記載なし）。子どもは写らない。WHTV 598 の耳打ちの秒には差し替えない（子どもの顔が多い）｜台本の画：実写 小学校の部屋のテレビに映る燃える両棟（ホワイトハウスの写真係・説明「9:10ごろ」・A の見込み＝権利の札は映像方針で確かめる・子どもが写るなら顔だけモザイク・全画面＝副題「フロリダ州の小学校（当日）」）',
               src='委員会報告 p38（`The President was seated in a classroom when, at 9:05`・`A second plane hit the second tower. America is under attack`）'),
    'c519': dict(kind='写真',
               plan="LCA06｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：ゆっくり引く｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜台本の画：実写 当日の世界貿易センター（A・別の点＝副題は絵を見て書く）",
               src='委員会報告 p35（`nearly everyone in the White House told us, they immediately knew it was not an accident`）'),
    'c520': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（11便と175便＝軍に届いた時刻の印）',
               src='—'),
}

SPEC = {}
