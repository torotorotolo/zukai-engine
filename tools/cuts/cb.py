# -*- coding: utf-8 -*-
"""第10章　最後の冬と2023年 cb01–cb19（19カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/cb.py`）。
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
    'cb01': dict(kind='図解',
               plan='🔧 G06｜注：🔧 実写→衛星写真の地図（NTSB 図9 は地図会社の透かしの見込み＝使わない・了承②）｜新しい画（映像方針）：図 地図 衛星写真 G06（セントジョンズ港の寄り）＋タイタンと2つのコンテナを置いた屋外の駐車場に印（NTSB 図9 の形を当てる）・副題「現在の衛星写真」｜台本の画（🔧映像方針で替えた＝元の予定）：実写 NTSB 図9 港の基地の屋外の駐車場に置かれたタイタンと台（MIR p.36 の図・撮影は基地の会社＝第三者＝額装・改変なし・サムネに使わない＝副題「屋外に置かれたタイタン（2022年の秋から冬）」）',
               src='TSB §1.22（`OceanGate opted to keep the Titan and the LARS in St. John’s because OceanGate did not have enough money to transport them back to Everett.`）・NTSB p.36（`It was left in a parking lot, outside, uncovered (see figure 9).`）'),
    'cb02': dict(kind='図解',
               plan='台本の画：図 再現 覆いの見積もり（基地からのメール・会社の返事なし）',
               src='USCG p.237〈229〉（`they had not received approval to proceed, so the tarp was not purchased.`）・NTSB p.35（`OceanGate shipped the Titan and LARS to Everett, where they were stowed indoors at an OceanGate facility during the winter season.`）'),
    'cb03': dict(kind='図解',
               plan='台本の画：図 帯 屋外の期間（2022年7月26日〜2023年2月6日＝195日）',
               src='USCG p.236〈228〉（`On July 26, 2022, the TITAN, the LARS, and associated equipment were demobilized at the A Harvey Marine Base in St. John’s, Canada.`）・USCG p.238〈230〉（`unprotected from the elements until February 6, 2023.`）'),
    'cb04': dict(kind='図解',
               plan='🔧 注：🔧 §0-3（TSB は「°」だけ＝摂氏は推測）｜新しい画（映像方針）：図 棒 セントジョンズの冬の気温（12月〜2月・最高気温の平均 −0.5°・最低気温の平均 −5.5°＝カナダの調べの書き方のまま「°」＝℃ と書かない）｜台本の画（🔧映像方針で替えた＝元の予定）：図 棒 セントジョンズの冬の気温（2022年12月〜2023年2月の最高気温の平均 −0.5℃・最低気温の平均 −5.5℃＝カナダの調べの値）',
               src='TSB §1.22（`The average high temperature in St. John’s between December 2022 and February 2023 was -0.5° and the average low was -5.5°.`）・§1.22（`experiences snow, strong winds, freezing rain, and hail.`）'),
    'cb05': dict(kind='図解',
               plan='台本の画：図 模式 水が入って凍る（船体のすき間の水が氷になってふくらむ・溶けて縮む・くり返す）',
               src='NTSB p.60（`If water had penetrated any part of the pressure vessel and frozen, the expansion that occurs due to the phase change to ice could have caused additional damage.`）・TSB §2.1.3（`The investigation could not conclusively quantify the extent of damage, if any, from these other sources`）'),
    'cb06': dict(kind='図解',
               plan='台本の画：図 再現 米沿岸警備隊の主たる要因の8つ目（英字＋訳は字幕）',
               src='USCG p.328〈320〉（`compromised the TITAN’s hull integrity.`）・USCG p.7〈vii〉（`OceanGate’s failure to conduct preventative maintenance on the TITAN’s hull or protect it from the elements during the extended offseason layup period`）'),
    'cb07': dict(kind='写真',
               plan='M109｜見せ方：全面｜副題：潜水艇を載せる台（事故の後に撮影）｜動き：左へ｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図109｜注：c305 の図5 と同じ場面の別の写真＝呼び方をそろえる（台）｜台本の画：実写 MBI 図109 岸壁の台（LARS）と白い浮き（USCG 報告 p.142・2023-06-25 撮影・c305 の図5 と同じ場面の別の写真・A＝副題「潜水艇を載せる台（事故の後に撮影）」）',
               src='USCG p.238〈230〉（`what we really wanted to do was bring the sub back, at least, to Everett and pull the insert and look at`）'),
    'cb08': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 2023年の組織の図（技術部長の席＝空の点線の箱に「未定（TBD）」）＝c207 と同じ形｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 2023年の計画書の人の欄（技術部長＝「TBD」）',
               src='USCG p.246〈238〉（`OceanGate’s Director of Engineering position for the expedition was listed as To Be Determined (TBD).`）・TSB §1.23.1（`there was no one formally in the position of director of engineering for the remainder of the 2023 season.`）'),
    'cb09': dict(kind='図解',
               plan='🔧 G02｜注：🔧 自作の地図→衛星写真（了承②）｜新しい画（映像方針）：図 地図 衛星写真 G02＋母船の後ろに台ごと引く線（水色の線の後ろに台の印）｜台本の画（🔧映像方針で替えた＝元の予定）：図 地図 セントジョンズから現場まで（母船の後ろに台ごと引く線）',
               src='TSB §1.20.2（`because the Polar Prince did not have equipment to lift the Titan and the LARS on and off the deck.`）・USCG p.246〈238〉（`the LARS and TITAN had to be towed behind the POLAR PRINCE for the entirety of each 2023 TITANIC mission.`）'),
    'cb10': dict(kind='図解',
               plan='台本の画：図 棒 引かれていた時間（約950時間＝カナダの調べ）と道のり（2,900海里あまり＝約5,400km＝米沿岸警備隊）',
               src='TSB §1.20.2.2（`towed by or tethered to, via a towline, the Polar Prince in the North Atlantic for approximately 950 hours in the 2023 season.`）・USCG p.294〈286〉（`towed behind the POLAR PRINCE for a total distance of more than 2,900 NM.`）'),
    'cb11': dict(kind='写真',
               plan='🔧 N10｜見せ方：額装（第三者）｜副題：傾いた台（2023年5月20日と27日）｜動き：額ごと右へ｜権利：第三者（個人の撮影・米運輸安全委員会の報告書の図）｜出典の行：（撮影者＝src/credits_private.tsv）／米運輸安全委員会の報告書 図10｜注：🔧 cb12 から移した（NTSB 図10 の凡例の日付＝5月20日・27日＝語りの5月24日の横に置かない）。縦長2枚を1つの額に｜台本の画（🔧映像方針で替えた＝元の予定）：実写 MBI 図112 台の注水弁（黄の丸＝MBI・USCG 報告 p.144・A＝副題「台の注水弁（事故の後に撮影）」）',
               src='TSB §1.20.2.2（`were subjected to considerably higher accelerations than those recommended by DNV`）・§1.20.2.2（`The Titan was also towed through significant wave heights of up to 3.35 m on the LARS`）'),
    'cb12': dict(kind='写真',
               plan="🔧 M112｜見せ方：額装（報告書の図）｜副題：台の浮き沈みを決める弁（事故の後に撮影）｜動き：額ごと引く｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図112｜注：🔧 cb11 から移した（語り「半ば沈んだ」＝台の浮き沈みの弁）・黄の丸は MBI｜台本の画（🔧映像方針で替えた＝元の予定）：実写 NTSB 図10 傾いた台（撮影は個人＝第三者＝額装・改変なし・④' と映像方針で使うか確かめる＝副題「傾いた台（2023年5月20日と27日）」＝NTSB 図10 の凡例の日付・5月24日に半ば沈んだ場面ではない＝語りの5月24日と並べない（引かれて揺れた cb11 へ移す案））",
               src='TSB §1.21.1（`On the morning of 24 May, while en route to the wreck site, the LARS and the Titan partially submerged while under tow.`）・§1.21.1（`The Titan and the LARS partially submerged again on the return to St. John’s.`）'),
    'cb13': dict(kind='図解',
               plan='台本の画：図 帯 3つの見方（引かれたことの影響＝米沿岸警備隊「さらに弱った可能性が高い」／米運輸安全委「影響は分からない」／カナダ「引いただけでは原因でない・すでにあった傷を広げたかもしれない」）',
               src='USCG p.295〈287〉（`subjected the TITAN to repeated impact damage that further weakened its structural integrity of its hull.`）・NTSB p.60（`their actual effects are unknown.`）・TSB §2.1.3（`towing the Titan and submerging it while under tow may have exacerbated existing damage.`）'),
    'cb14': dict(kind='図解',
               plan='🔧 注：🔧 再現→棒（§0-3）｜新しい画（映像方針）：図 棒 2023年の人が乗った潜航3回の深さ（10m の短い棒3本）と、タイタニックの深さ約3,800m の破線｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 TSB 付録B の2023年の4行（10・10・10・3346）',
               src='TSB §1.21.4（`The dive was aborted at a depth of 10 m. The Titan did not disconnect from the LARS on this dive.`）・NTSB p.14（`None of the dives exceeded 33 feet (10 meters) depth.`）・USCG p.256〈248〉（`10 m dives were dives which did not leave the LARS platform.`）'),
    'cb15': dict(kind='写真',
               plan='M115｜見せ方：全面｜副題：台を浮かせる空気の装置（事故の後に撮影）｜動き：上へ｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図115｜台本の画：実写 MBI 図115 台を浮かせる空気の装置（黄と赤の浮き袋・USCG 報告 p.145・A＝副題「台を浮かせる空気の装置（事故の後に撮影）」）',
               src='USCG p.295〈287〉（`repeatedly slammed against the LARS platform for approximately 45-minutes by passing ocean swells`）・p.295〈287〉（`There is no evidence that OceanGate conducted a post-incident hull inspection or incident report`）'),
    'cb16': dict(kind='図解',
               plan='🔧 注：🔧 再現→帯（§0-3）｜新しい画（映像方針）：図 帯 監視装置の記録（2022年＝記録あり＝青の帯／2023年＝記録なし＝灰の空白）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 監視装置の記録の有無（2022年＝あり／2023年＝なし）',
               src='USCG p.139〈131〉（`No real-time monitoring data was available to the MBI from Expedition 2023 (Dives 84-88).`）・TSB §1.10.9（`There was no data available for the 2023 season.`）'),
    'cb17': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 危険度の点数の目盛り（この日の35＝黄の点・48の線＝「ストライク」・3つで中止の札）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 危険度の点数（事故の回＝35・「48を超えるとストライク」の決まり＝TSB 図16 は使わず数だけ）',
               src='TSB §1.17.12.1（`The mission director checklist specified that a risk index of greater than 48 was considered to be a strike. The risk assessment for the occurrence dive (Figure 16) had a risk index of 35.`）・USCG p.78〈70〉（`If there was a total of three or more “strikes” encountered during a dive evolution, the Mission Director was required to cancel the day’s dive operation.`）'),
    'cb18': dict(kind='図解',
               plan='台本の画：図 再現 NTSB の所見2（英字＋訳は字幕）',
               src='NTSB p.73（`After dive 82, the Titan sustained additional damage—of unknown origin—that further deteriorated and weakened the pressure vessel to a point where it could not survive a dive to the depth of the Titanic.`）'),
    'cb19': dict(kind='図解',
               plan='台本の画：図 帯 2023年6月18日（この年初めて台を離れて深く潜る潜航）',
               src='USCG p.295〈287〉（`Dive 88 was the first dive to leave the LARS platform for the TITANIC Survey Expedition 2023`）・NTSB p.16（`It was the first dive of the 2023 expedition to descend below 33 feet (10 meters).`）'),
}

SPEC = {}

# ── 🆕 ⑤b-3（2026-10-14）：地図のカット（衛星写真＋描き足し＝`tools/satmap.py`・c2.py の注）──
SPEC.update({
    # cb01（3行）＝1行目は聞き役の問い（描き足しなし）・2行目で A. Harvey の基地のあたりを囲む（USCG 4.35.2・NTSB 図9）。
    #   🔴 NTSB 図9（空からの駐車場・×の印）と衛星写真 G06 は特徴点の照合が取れなかった＝駐車場の中の位置は描かない（基地のあたり＝住所から）
    "cb01": dict(**ss.sat("G06", note="囲みは基地の住所のあたり（一般の座標・駐車場の中の位置は描かない）", steps=[
        [],
        [dict(k="area", at="harvey", r=160, role="company", t="A. ハーヴィーの基地", lab=(0, 128, "middle"))]]),
        t="冬の置き場", s="セントジョンズの港（現在の衛星写真）"),
    # cb09（2行）＝母船の後ろに台ごと引く（船と台の印は模式・線は2点を結んだだけ）
    "cb09": dict(**ss.sat("G02", note="セントジョンズは一般の座標・×は最後に受けた位置・線と船の印は模式（実際の航路ではない）", steps=[
        [dict(k="line", path=("stjohns", "site"), role="ship"),
         dict(k="icon", what="ship", on=("stjohns", "site", 0.5), role="ship", tow=True, t="母船", lab=(34, -8, "start")),
         dict(k="x", at="site")],
        [dict(k="icon", what="ship", on=("stjohns", "site", 0.5), role="ship", tow=True, t="台（タイタン）", lab=(-60, 40, "end"))]]),
        t="引いて運ぶ", s="セントジョンズから現場へ（現在の衛星写真）"),
})
