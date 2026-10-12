# -*- coding: utf-8 -*-
"""第2章　乗っ取りの「常識」 c301–c320（20カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c3.py`）。
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
    'c301': dict(kind='写真',
               plan='F15A｜副題：ニューヨーク上空を警戒するオーティス基地のF-15（2001年11月）｜動き：右へ流す｜権利：A（米空軍の職務）｜出典の行：米空軍｜台本の画：実写 F-15 オーティス基地（102戦闘航空団 101戦闘飛行隊・尾翼「MA」・A・VIRIN で 2001-11-06・全画面・右へ流す＝副題「オーティス基地のF-15（2001年11月）」）',
               src='—'),
    'c302': dict(kind='図解',
               plan='台本の画：図 模式 乗員の手引きの年表（1960年代から2001年まで）',
               src='委員会報告 p85（`The FAA-approved "Common Strategy" had been elaborated over decades of experience with scores of hijackings, beginning in the 1960s`）'),
    'c303': dict(kind='図解',
               plan='台本の画：図 模式 昔ながらの乗っ取り（要求・着陸・あとは警察と軍の3つの箱）',
               src='委員会報告 p85（`accommodate their demands, get the plane to land safely, and then let law enforcement or the military handle the situation`・`the longer a hijacking persisted, the more likely it was to end peacefully`）'),
    'c304': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱（「要求」に亡命・仲間の釈放の札）',
               src="委員会報告 p85（`hijackers issue negotiable demands (most often for asylum or the release of prisoners)`・`suicide wasn't in the game plan`）"),
    'c305': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱（「暴力が起きたら」の箱だけ空白）',
               src='委員会報告 p85（`FAA training material provided no guidance for flight crews should violence occur`）'),
    'c306': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の扉（金庫の扉の絵記号）',
               src='委員会報告 p85（`proposals were made in early 2001 to install reinforced cockpit doors`）'),
    'c307': dict(kind='図解',
               plan='台本の画：図 模式 同じ扉（鍵が外れる）',
               src="委員会報告 p85（`Even if you make a vault out of the door, if they have a noose around my flight attendant's neck, I'm going to open the door`）"),
    'c308': dict(kind='図解',
               plan='台本の画：図 模式 同じ扉と箱（「要求に従う」の矢印）',
               src='委員会報告 p85（`even a hardened cockpit door would have made little difference in a hijacking`）'),
    'c309': dict(kind='図解',
               plan='台本の画：図 模式 年表（1986年の印から2001年まで）',
               src='委員会報告 p85（`no terrorist had hijacked a U.S. commercial aircraft anywhere in the world since 1986`）'),
    'c310': dict(kind='図解',
               plan='台本の画：図 模式 機内の座席（保安官の席に印が無い）',
               src='委員会報告 p85（`only 33 armed and trained federal air marshals as of 9/11`・`They were not deployed on U.S. domestic flights`）'),
    'c311': dict(kind='図解',
               plan='台本の画：図 模式 手順の段（管制官→上司→FAA 本部→国防総省の指揮所→国防長官の許し→NORAD→戦闘機）',
               src='委員会報告 p17（`Controllers would notify their supervisors, who in turn would inform management all the way up to FAA headquarters in Washington`）'),
    'c312': dict(kind='図解',
               plan='台本の画：図 模式 同じ段（下の段へ光が進む）',
               src="委員会報告 p18（`to contact the Pentagon's National Military Command Center`・`seek approval from the Office of the Secretary of Defense`・`transmitted down NORAD's chain of command`）"),
    'c313': dict(kind='図解',
               plan='台本の画：図 模式 乗っ取られた機と後ろの戦闘機（約8キロの間隔）',
               src='委員会報告 p18（`five miles directly behind the hijacked aircraft`・`The protocols did not contemplate an intercept`）'),
    'c314': dict(kind='図解',
               plan='台本の画：図 模式 同じ（段と後ろの戦闘機を1枚に）',
               src='—'),
    'c315': dict(kind='図解',
               plan='台本の画：図 模式 3つの前提の箱（1つ目に印＝すぐに見分けがつき、姿を消そうとはしない）',
               src='委員会報告 p18（`the hijacked aircraft would be readily identifiable and would not attempt to disappear`）'),
    'c316': dict(kind='図解',
               plan='台本の画：図 模式 3つの前提の箱（2つ目と3つ目に印）',
               src='委員会報告 p18（`there would be time to address the problem through the appropriate FAA and NORAD chains of command`・`the hijacking would take the traditional form`）'),
    'c317': dict(kind='図解',
               plan='台本の画：図 模式 待機の基地の数（冷戦の最大26か所から7か所への棒）',
               src='委員会報告 p16（`reduced from its Cold War high of 26`）・p17（`only seven alert sites left in the United States, each with two fighter aircraft on alert`）'),
    'c318': dict(kind='図解',
               plan='台本の画：図 模式 北東部の地図（NEADS のあるローム・オーティス・ラングレー・ニューヨーク・ワシントン）',
               src='委員会報告 p17（`Northeast Air Defense Sector (also known as NEADS), which is based in Rome, New York`・`NEADS could call on two alert sites, each with one pair of ready fighters`）'),
    'c319': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（海の外から来る矢印だけ）',
               src='委員会報告 p352（`only aircraft that were coming from overseas`）・p17（`was not recognized by NORAD before 9/11`）'),
    'c320': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（7:59 から先が空白のまま伸びる）',
               src='委員会報告 p18（`unsuited in every respect`）'),
}

SPEC = {}
