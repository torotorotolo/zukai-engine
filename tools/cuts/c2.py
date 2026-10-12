# -*- coding: utf-8 -*-
"""第1章　その朝、4つの便 c201–c217（17カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c2.py`）。
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
    'c201': dict(kind='写真',
               plan='MAN01｜副題：事件の前のマンハッタン（2001年7月）｜動き：右へ流す｜権利：C＋D（Highsmith の献呈・米議会図書館蔵／知られた制限なし）｜出典の行：Carol M. Highsmith（米議会図書館蔵）｜台本の画：実写 manhattan_pre（事件の2か月前のマンハッタン・2001年7月・C＋D＝米議会図書館蔵／知られた制限なし・全画面・右へ流す＝副題「事件の前のマンハッタン（2001年7月）」）',
               src='委員会報告 p1（`nearly cloudless`）'),
    'c202': dict(kind='図解',
               plan='台本の画：図 模式 4便の経路の地図（出発の3つの空港と行き先の2つの街＝NTSB の4本の経路の図をなぞる・東から西へ線が伸びる）',
               src='委員会報告 p4（`four transcontinental flights`）'),
    'c203': dict(kind='写真',
               plan='LOGAN｜副題：ボストンのローガン空港（1973年）｜動き：ゆっくり寄る｜権利：A（EPA DOCUMERICA・NARA 548428）｜出典の行：米環境保護庁 DOCUMERICA（NARA 548428）｜台本の画：実写 logan（ボストンのローガン空港・1973年・EPA DOCUMERICA・A・全画面・ゆっくり寄る＝副題「ボストンのローガン空港（1973年）」）',
               src='委員会報告 p4（`turn them into large guided missiles, loaded with up to 11,400 gallons of jet fuel`）・第1章 注1 p451（`they simply booked heavily fueled east-to-west transcontinental flights`）・p245（`select planes departing on long flights because they would be full of fuel`）'),
    'c204': dict(kind='写真',
               plan='AA11｜副題：11便の機体（2001年4月）｜動き：額装・止め（寄り0）｜権利：F（CC BY-SA 3.0＝額装・無加工・寄り0）｜出典の行：（作者と許諾の表示は頁の通りに＝fetch21_meta.tsv）｜注：BY-SA 3.0＝額装・無加工（「写真は画面いっぱい」の例外）。登録記号 N334AA が写る｜台本の画：実写 AA11 N334AA（11便の機体の事件の前の写真・CC BY-SA 3.0・額装・無加工＝副題「11便の機体（事件の前）」）',
               src='委員会報告 p4（`Eighty-one passengers boarded the flight with them (including the five terrorists)`・`The plane took off at 7:59`・`It carried its full capacity of nine flight attendants`）'),
    'c205': dict(kind='写真',
               plan='TG99｜区間 214.0〜224.8秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：事件の前の世界貿易センター（1999年・屋上の展望台から）｜動き：額装・等速｜権利：F（CC BY-SA 3.0＋GFDL＝額装・無加工・速さも変えない）｜出典の行：（作者と許諾の表示は頁の通りに＝fetch21_meta.tsv）｜注：BY-SA 3.0＝額装・無加工・速さを変えない。もう一方の塔の屋上→港（自由の女神）。人は写らない（1秒1コマ）。⑤b-1：等速の約束＝区間をカットの実測の秒（10.751秒＝声＋前後の間）に合わせて 223.5→224.75 へ（ショット6＝173.4〜253.5 の中・伸ばした分は 224.0・224.7秒を原寸で見た＝港の遠景だけ）。台本の「720×576・額装・無加工」のまま｜台本の画：実写 Torri Gemelle（事件の前の世界貿易センター・1999年・CC BY-SA・720×576・額装・無加工＝副題「事件の前の世界貿易センター（1999年）」）',
               src='委員会報告 p7（`Fifty-six passengers boarded the flight`・`departed Logan Airport at 8:14`）'),
    'c206': dict(kind='写真',
               plan='DULLES｜副題：ワシントン・ダレス空港（1985年）｜動き：左へ流す｜権利：A（米海軍の職務）｜出典の行：米海軍（PH1 David C. Maclean）｜台本の画：実写 dulles（ワシントン・ダレス空港・1985年・A・全画面・左へ流す＝副題「ワシントン・ダレス空港（1985年）」）',
               src='委員会報告 p8（`the flight carried 58 passengers`・`took off at 8:20`・`There were four flight attendants`）'),
    'c207': dict(kind='写真',
               plan='UA93｜副題：93便の機体（1999年）｜動き：ゆっくり引く｜権利：F（CC BY 2.0）｜出典の行：（作者と許諾の表示は頁の通りに＝fetch21_meta.tsv）｜注：CC BY 2.0・幅1690｜台本の画：実写 UA93 N591UA（93便の機体の事件の前の写真・CC BY 2.0・全画面・ゆっくり寄る＝副題「93便の機体（事件の前）」）',
               src='委員会報告 p10（`At 8:42, United Airlines Flight 93 took off from Newark`・`Thirty-seven passengers, including the hijackers, boarded the plane`・`there were five flight attendants`）'),
    'c208': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（4機の離陸＝7:59・8:14・8:20・8:42＝この回の芯の帯の始まり）',
               src='委員会報告 p10（`Three of the flights had actually taken off within 10 to 15 minutes of their planned departure times`・`the flight was running more than 25 minutes late`）'),
    'c209': dict(kind='フリー素材',
               plan='B767｜副題：イメージ（2012年のアメリカン航空の767）｜動き：右へ流す｜権利：F（CC BY 2.0）｜出典の行：Valentin Hintikka（CC BY 2.0）｜注：20%に数えない｜台本の画：イメージ b767_takeoff（2012年のアメリカン航空の767・フリー素材＝副題「イメージ」）',
               src='委員会報告 p4（`The 19 men were aboard four transcontinental flights`）'),
    'c210': dict(kind='フリー素材',
               plan='SEC70｜副題：イメージ（1970年の空港）｜動き：上へ流す｜権利：F（CC BY）｜出典の行：Orange County Archives（CC BY）｜注：縦長・私人の顔だけモザイク（CC BY）・20%に数えない｜台本の画：イメージ security_pre（1970年の空港の保安検査・CC BY・私人の顔だけモザイク＝副題「イメージ（1970年の空港）」）',
               src='委員会報告 p2（`operated by Globe Security under a contract with American Airlines`・`contracted with Huntleigh USA to perform the screening`）・p3（`had contracted out the work to Argenbright Security`）・p4（`operated under contract by Argenbright Security`）・p2（`calibrated to detect items with at least the metal content of a .22-caliber handgun`）'),
    'c211': dict(kind='図解',
               plan='台本の画：図 模式 保安検査の流れ（探知機の門・手持ちの探知機・通過＝人は影だけ）',
               src='委員会報告 p3（`set it off, a screener wanded him. He passed this inspection`・`set off the alarms for both the first and second metal detectors and was then hand-wanded before being passed`・`it was clear that he did not`）'),
    'c212': dict(kind='図解',
               plan='台本の画：図 模式 刃渡りの物差し（10センチの線と刃物の影・人は描かない）',
               src='委員会報告 p84（`knives with blades under 4 inches long`・`explicitly permitted them`）'),
    'c213': dict(kind='図解',
               plan='台本の画：図 模式 同じ物差し（3つの理由の札）',
               src='委員会報告 p84（`the agency did not consider such items to be menacing`・`most local laws did not prohibit individuals from carrying such knives`・`such knives would have been difficult to detect unless the sensitivity of metal detectors had been greatly increased`）'),
    'c214': dict(kind='図解',
               plan='台本の画：図 模式 機内からの電話が伝えた道具（刃物・スプレー・「爆弾」の札に「おそらく偽物」）',
               src="委員会報告 p7（`They used knives`）・p5（`I think there's Mace`）・p13（`we believe the bombs were probably fake`）"),
    'c215': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の扉（閉めて鍵＝当時の決まり）',
               src='委員会報告 p85（`required air crews to keep the cockpit door closed and locked in flight`・`This requirement was not always observed or vigorously enforced`）'),
    'c216': dict(kind='写真',
               plan='APRON｜副題：ローガン空港の駐機場（1969年）｜動き：左へ流す｜権利：D（米議会図書館蔵／知られた制限なし）｜出典の行：Balthazar Korab（米議会図書館蔵）｜台本の画：実写 logan_apron（ローガン空港の駐機場・1969年・D＝米議会図書館蔵／知られた制限なし・全画面・ゆっくり引く＝副題「ローガン空港（1969年）」）',
               src='委員会報告 p4（`By 8:00 A.M. on the morning of Tuesday, September 11, 2001, they had defeated all the security layers`）'),
    'c217': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（8:00 の線）',
               src='—'),
}

SPEC = {}
