# -*- coding: utf-8 -*-
"""第1章　タイタニックへの観光潜航 c201–c219（19カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c2.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep22/make_plan22.py` で
  映像方針の一覧 `ref/ep22/eizou_build/list22.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典から
  機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット（台本の画は元の予定）。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c201': dict(kind='写真',
               plan='C201｜見せ方：額装（共同）｜副題：タイタニックの船首（2004年の調査）｜動き：額ごと寄る｜権利：共同（NOAA と Institute for Exploration・University of Rhode Island＝連邦の外の機関を含む＝A の見込みは弱い）｜出典の行：NOAA/Institute for Exploration/University of Rhode Island（2004年）｜注：2004年6月 ROV「Hercules」が撮影（Commons の説明）・NOAA と連邦の外の機関の共同＝額装・サムネに使わない｜台本の画：実写 タイタニックの船首（Commons「Titanic wreck bow.jpg」・2004年の調査・クレジット「Courtesy of NOAA/Institute for Exploration/University of Rhode Island」＝A の見込みは弱い＝出典の書き方と額装か全面かは映像方針で＝副題「タイタニックの船首（2004年の調査）」）',
               src='TSB §1.3（`a descent of approximately 3800 m`）'),
    'c202': dict(kind='図解',
               plan='台本の画：図 模式 富士山（3,776m）を逆さにした高さと、タイタニックの深さ（約3,800m）の比べ・横に1円玉と乗用車の札（式は §9）',
               src='NTSB p.10（`At the depth of the Titanic wreckage site, water pressure is 5,554.5 pounds per square inch.`）'),
    'c203': dict(kind='図解',
               plan='台本の画：図 再現 3つの報告書（表紙の題と日付だけを並べた図＝米沿岸警備隊の海難調査委員会 2025年8月／米国の運輸安全委員会 2025年10月／カナダの運輸安全委員会 2026年6月）',
               src='USCG p.5〈v〉（`August 4, 2025`）・NTSB p.76（`Report Date: October 2, 2025`）・TSB §4.2.4（`It was officially released on 17 June 2026.`）'),
    'c204': dict(kind='図解',
               plan='🔧 G01｜注：🔧 自作の地図→衛星写真（了承② 10-14 カズヤくん「衛星写真・撮るのは⑤b-1」）｜新しい画（映像方針）：図 地図 Google マップの衛星写真 G01（北米の東半分）＋描き足し＝会社の本社エバレット（白の点）・母船の港セントジョンズ（白の点）・タイタニックの位置（赤の×）の3点だけ・副題「現在の衛星写真」・右下の帰属の行を残す｜台本の画（🔧映像方針で替えた＝元の予定）：図 地図 北米の東半分（会社の本社＝米国ワシントン州エバレット・母船の港＝カナダのセントジョンズ・タイタニックの位置の3点だけ）',
               src='TSB §1.23（`OceanGate was first established as a limited liability company in 2009`）・§1.23（`OceanGate was headquartered in Everett, Washington`）'),
    'c205': dict(kind='図解',
               plan='台本の画：図 線 タイタンの横から見た線画（NTSB 図3 をなぞる・全長6.7m と「5人まで」の札だけ）',
               src='NTSB p.10（`The 22-foot-long submersible Titan was designed, built, and operated by OceanGate Inc.`）・TSB §1.2.1（`designed to accommodate up to 5 people`）'),
    'c206': dict(kind='図解',
               plan='台本の画：図 線 同じ線画（人が乗る部分＝筒と両端のドームを明るく・札「炭素繊維の筒」「チタンのドーム」）',
               src='TSB §1.10.1（`The Titan’s pressure hull consisted of a carbon fibre cylinder that was capped at either end by titanium domes.`）・§1.2.1（`Two hemispherical domes made of titanium were fitted to either end of the cylinder.`）'),
    'c207': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3 職の表）｜新しい画（映像方針）：図 模式 組織の図（2023年の上級の8つの職を席の箱で並べる＝埋まった席は会社の橙・空いた席は灰の点線・CEO の席を明るく・TSB 表4 の値・英字の表は画面に出さない）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 TSB 表4（2023年の上級の8つの職と、その席が埋まっていたか＝欄は英字のまま・CEO の行を明るく）',
               src='TSB §1.3（`the Titan’s pilot, who was OceanGate’s chief executive officer (CEO)`）・§1.9.1（`had piloted it on numerous previous dives, including dives to the Titanic in 2021 and 2022`）・§1.23.1（`As a small company, OceanGate was led primarily by the CEO.`）・§1.23.1（`The CEO was integrated into all aspects of the company, including human resources, finance, operations, and submersible design and construction.`）'),
    'c208': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 同じ組織の図＋社員の人の印15（数は黄）と「実験的」の札｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表4（2023年の潜航の季節の初めの社員の数「15」の札を足す）',
               src='TSB §1.23（`At the beginning of the 2023 operating season, OceanGate had 15 employees`）・§1.23.1（`viewed the design, development, and operation of the Titan as being experimental`）・§1.23.1（`There was no precedent for diving a human-occupied carbon fibre submersible to the deep ocean`）'),
    'c209': dict(kind='図解',
               plan='台本の画：図 再現 同意書の要点（USCG p.71 の箇条の英字＝`experimental submersible vessel`・`not been certified by any regulatory body`・「death」の数え＝9）',
               src='USCG p.71〈63〉（`The submersible had not been certified by any regulatory body.`）・p.71〈63〉（`A portion of the expedition would be conducted inside an experimental submersible vessel.`）・p.71〈63〉（`The liability waiver mentions death 9 times`）'),
    'c210': dict(kind='図解',
               plan='台本の画：図 棒 参加費（2021年 105,129ドル → 2022年・2023年 25万ドル＝円は1ドル140円で計算と左下に）',
               src='USCG p.64〈56〉（`rising from $105,129 in 2021 to $250,000 for both 2022 and 2023.`）・TSB §1.23（`the cost for 1 passenger to join was up to 250 000 U.S. dollars`）'),
    'c211': dict(kind='図解',
               plan='台本の画：図 再現 会社の計画書の一節（NTSB 脚注8 が引く `guests who help fund OceanGate expeditions` の英字＋訳は字幕）',
               src='NTSB p.15（`OceanGate referred to its clients as “mission specialists.”`）・USCG p.300〈292〉（`reclassifying their passengers as “mission specialists” to conceal their illegal passenger operations`）・USCG p.317〈309〉（`to conceal that their mission specialists were actually paying passengers`）'),
    'c212': dict(kind='図解',
               plan='台本の画：図 再現 TSB 付録B の表（27行・欄は英字のまま＝日付・深さ・時間・人数・母船・目的・備考）',
               src='TSB 付録B（`The term “dive” refers to dives to any depth where there were people on board the submersible and the submersible was on life support.`）・付録B（`Dives made by the Titan between 2021 and the occurrence at the Titanic wreck site, in Canadian waters, or in Canada’s exclusive economic zone`）'),
    'c213': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3 潜航の表は c212 の1回だけ）｜新しい画（映像方針）：図 模式 点の並び（付録B の潜航を1回1点で年ごとに並べ、深さ3,840m に届いた13回を海の青で明るく・届かなかった回は灰）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（深さ「3840」の13行を明るく）',
               src='NTSB p.14（`only successfully completed 13 dives to the wreck`）'),
    'c214': dict(kind='図解',
               plan='🔧 注：🔧 再現→帯（§0-3）｜新しい画（映像方針）：図 帯 2021年の潜航の年表（1つ目の点に赤の印「回収のときに前のドームが外れた」→「留めるボルトを18本に」の札）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（1行目の備考 `Forward dome fell off the submersible during recovery` を明るく）',
               src='TSB 付録B（`Forward dome fell off the submersible during recovery`）・TSB（`Following this dive, OceanGate began using 18 securing bolts.`）'),
    'c215': dict(kind='図解',
               plan='🔧 注：🔧 再現→帯（§0-3）｜新しい画（映像方針）：図 帯 同じ年表（赤の印「電池が切れた」・「27時間」は黄）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（`Batteries died on approach to LARS`・時間「27」を明るく）',
               src='TSB 付録B（`Batteries died on approach to LARS`）・NTSB p.36（`so the Titan remained on the surface with occupants aboard overnight.`）'),
    'c216': dict(kind='図解',
               plan='🔧 注：🔧 再現→帯（§0-3）｜新しい画（映像方針）：図 帯 同じ年表（推進器・重り・通信の不具合の赤の印が並ぶ）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（推進器・重り・追跡と通信の備考を明るく）',
               src='TSB 付録B（`Starboard thrusters failed`）・付録B（`Incident with drop weight`）・TSB §1.23.1（`OceanGate primarily used a trial-and-error approach to operations`）'),
    'c217': dict(kind='写真',
               plan='M65｜見せ方：全面｜副題：前の艇 サイクロプス1 の操縦の道具（2023年10月撮影）｜動き：右へ｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図65｜注：MBI 図65 の凡例＝2023-10-26 に MBI が撮影（Logitech のゲーム機用のコントローラー）｜台本の画：実写 MBI 図65 前の艇 Cyclops I の中のコントローラーとキーボード（USCG 報告 p.103・2023年10月に MBI が撮影・A＝副題「前の艇 サイクロプス1 の操縦の道具（2023年10月撮影）」）',
               src='TSB §1.10.5（`The pilot operated the thrusters using a handheld wireless controller`）・NTSB p.11（`a wireless, battery-operated controller that communicated with control software`）・USCG p.103〈95〉（`the CYCLOPS I being operated with a PlayStation® controller`）・USCG p.103〈95〉（`Photo of the Logitech PlayStation controller inside CYCLOPS I taken by the MBI`）'),
    'c218': dict(kind='写真',
               plan='C218｜見せ方：額装（BY-SA）｜副題：2021・22年の遠征の母船（写真は2022年）｜動き：額ごと寄る（写真は常に全部見える）｜権利：BY-SA 4.0｜出典の行：（撮影者＝src/credits_private.tsv）／CC BY-SA 4.0｜注：CC BY-SA 4.0＝無加工・切らない・色も重ねもしない・寄り0（額ごと動かす）。Commons の 2022-08-21 02（01 は船尾に橙の物）｜台本の画：実写 ホライゾン・アークティック（Commons・CC BY-SA 4.0・2022年＝第三者＝額装・改変なし・サムネに使わない＝副題「2021・22年の遠征の母船」）',
               src='TSB §1.2.2（`In previous years, OceanGate had chartered another vessel, the Horizon Arctic`）'),
    'c219': dict(kind='図解',
               plan='🔧 G02｜注：🔧 自作の地図→衛星写真（了承②）｜新しい画（映像方針）：図 地図 衛星写真 G02（セントジョンズ→タイタニックの眠る海）＋水色の点線（母船）・白の点・赤の×・黄の「約700〜800km」＝見本 sat_c219 の形｜台本の画（🔧映像方針で替えた＝元の予定）：図 地図 セントジョンズからタイタニックの現場まで（約685km の線）',
               src='TSB §1.2.2（`OceanGate first chartered the Polar Prince in March 2023.`）・USCG p.5〈v〉（`approximately 370 nautical miles`）'),
}

SPEC = {}
