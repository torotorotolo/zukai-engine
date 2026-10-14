# -*- coding: utf-8 -*-
"""第9章　2022年7月15日の音 ca01–ca26（26カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/ca.py`）。
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
    'ca01': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 2022年の潜航13回を1回1点で（3,840m に届いた7回を海の青で明るく）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 TSB 付録B の表の2022年の13行（深さ「3840」の7行を明るく・欄は英字のまま）',
               src='NTSB p.35（`the Titan reached 3,840 meters (12,598 feet) seven times`）・USCG p.235〈227〉（`While 7 of the 13 dives reached the TITANIC depth of 3840 m`）・TSB 脚注75（`Dives without people on board are not included.`）'),
    'ca02': dict(kind='図解',
               plan='🔧 見る向き：横から｜注：🔧 再現→線（§0-3）｜新しい画（映像方針）：図 線 タイタニックの船首の線画（左舷の船首に潜水艇の印がぶつかる＝赤）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（2022-07-03 の行の備考 `Titan collided with the port bow of the Titanic and was disabled on recovery` を明るく）',
               src='TSB 付録B（`Titan collided with the port bow of the Titanic and was disabled on recovery`）・TSB §2.1.3（`The investigation could not conclusively quantify the extent of damage, if any, from these other sources`）'),
    'ca03': dict(kind='写真',
               plan='N08｜見せ方：額装（第三者）｜副題：台ごと海へ降ろされるタイタン（2022年）｜動き：額ごと寄る｜権利：第三者（個人の撮影・米運輸安全委員会の報告書の図）｜出典の行：（撮影者＝src/credits_private.tsv）／米運輸安全委員会の報告書 図8｜注：旧版 c109 のように地に敷かない・サムネに使わない｜台本の画：実写 NTSB 図8 2022年、母船の船尾から台ごと海へ降ろされるタイタン（MIR p.34・撮影は個人＝第三者＝額装・改変なし・サムネに使わない・旧版 c109 のように地に敷かない＝副題「台ごと海へ降ろされるタイタン（2022年）」）',
               src='TSB §2.1.3（`such as the Titan colliding with the port bow of the Titanic on 03 July 2022`）・USCG p.233〈225〉（`the TITAN became entangled in the TITANIC’s stairwell.`）'),
    'ca04': dict(kind='図解',
               plan='台本の画：図 再現 USCG p.233 の要点（「少しのあいだ動けず」「事故の報告は出されなかった」）',
               src='USCG p.233〈225〉（`For a moment, the TITAN remained trapped, but the content expert was subsequently able to work the controls to free the TITAN from the TITANIC wreckage.`）・USCG p.311〈303〉（`no incident report was filed for this event.`）'),
    'ca05': dict(kind='図解',
               plan="🔧 注：🔧 §0-3 の食い違い（④'の「15:20ごろ 0m」→図19 では15:16ごろ・音の山は15:27ごろ＝深さはもう0m付近）｜新しい画（映像方針）：図 線 80回目の深さの線（記録の点だけ＝7:35ごろ 0m → 10:05ごろ 約3,840m → 13:35ごろまで同じ深さ → 15:16ごろ 0m＝NTSB 図19 を原寸で読んだ・±2分）。音の山（15:26:45・米沿岸警備隊）の印は海面の線に置く＝水の中の深い所に置かない。左下に「元は会社の記録」｜台本の画（🔧映像方針で替えた＝元の予定）：図 線 80回目の深さの線（記録の点だけ＝10:05〜13:35 に 3,840m 付近・15:20ごろ 0m＝NTSB 図19 を記録の点で描き直す・元は OceanGate のデータ）",
               src='USCG p.234〈226〉（`which occurred as the TITAN was still submerged but nearing the surface.`）・NTSB p.36（`heard a “loud bang” as the Titan ascended`）・TSB §1.10.10.1（`a loud bang was heard by crew and passengers of the submersible while it was surfacing.`）'),
    'ca06': dict(kind='図解',
               plan='台本の画：図 模式 監視装置の配置（筒の内側に音のセンサー8つ・ひずみ計16の印）',
               src='NTSB p.31（`The system was comprised of eight acoustic emission sensors, eight circumferential (hoop) strain gages, and eight longitudinal (axial) strain gages.`）'),
    'ca07': dict(kind='図解',
               plan='台本の画：図 線 音とひずみの線（記録の点だけ＝15:17ごろから音が増える・15:26:45 に大きな山・同じ瞬間にひずみが跳ぶ＝USCG の値・NTSB 図19・20 と USCG 図215・216 を描き直す・左下に「元は会社の記録」）',
               src='USCG p.283〈275〉（`At 3:26:45 p.m., the TITAN’s RTM system recorded a major acoustic emission event`）・USCG p.286〈278〉（`occurred in a fraction of a second and coincided with the large amplitude acoustic event on Dive 80 at 3:26:45 p.m.`）'),
    'ca08': dict(kind='図解',
               plan='台本の画：図 線 同じ図（15:17ごろからの音の増えを明るく・NTSB の幅 15:15〜15:30 の帯）',
               src='USCG p.283〈275〉（`revealed increased acoustic emission activity beginning at approximately 3:17 p.m.`）・NTSB p.52（`showed a burst of acoustic activity and a sudden jump in some of the strain gages between about 1515 and 1530`）'),
    'ca09': dict(kind='図解',
               plan='台本の画：図 再現 会社の説明（NTSB p.36 の英字＝`the hull had shifted in its metal cradle`＋訳は字幕）',
               src='USCG p.233〈225〉（`was caused by a shift in the TITAN’s position within its frame.`）・NTSB p.36（`staff and mission specialists were told the hull had shifted in its metal cradle.`）'),
    'ca10': dict(kind='図解',
               plan='台本の画：図 模式 筒と内張り（外から見るだけ＝層のあいだのはがれは外から見えない）',
               src='USCG p.289〈281〉（`a cursory external examination of the TITAN was conducted following the loud bang with no visible damage identified.`）・USCG p.290〈282〉（`no effort was made to remove the TITAN’s insert or take the submersible temporarily out of service for a more detailed assessment.`）'),
    'ca11': dict(kind='図解',
               plan='台本の画：図 再現 CEO の言葉（NTSB p.36 が引く英字＋訳は字幕）',
               src='NTSB p.36（`after inspecting the strain and acoustic emission data, told the director of engineering, "Let\'s dive again and see what happens"`）'),
    'ca12': dict(kind='図解',
               plan='台本の画：図 再現 USCG p.290 の要点（「次の潜航の前にも、冬の休みのあいだにも、調べは要らないと指示」）',
               src='USCG p.290〈282〉（`directed that no further investigation or assessments were necessary ahead of the next scheduled 2022 dive or during the TITAN’s extended layup period ahead of the 2023 TITANIC Expedition.`）'),
    'ca13': dict(kind='図解',
               plan='台本の画：図 再現 USCG p.290 の要点（「権限のある誰も、ひずみのデータを読み解く専門の力を持たなかった」）',
               src='USCG p.290〈282〉（`neither the Director of Engineering nor anyone else onboard with the authority to assess the submersible’s safety possessed the necessary engineering expertise to interpret the strain gauge data`）'),
    'ca14': dict(kind='図解',
               plan='台本の画：図 帯 2022年7月の年表（15日 80回目→19日 81回目→22日 82回目→23日 83回目）',
               src='NTSB p.36（`the submersible reached 3,840 meters (12,598 feet) on dives 81 and 82 and 2,954 meters (9,692 feet) on the final dive of the expedition.`）・NTSB p.51（`The last of these dives (dive 83) took place on July 23, 2022, but at a different dive location`）・TSB §2.1.1（`4 days before the subsequent dive on 19 July 2022`）'),
    'ca15': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 コントローラーの向き（推進器の操作が逆＝矢印が逆向き → 逆さに持つ）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 付録B の 2022-07-19 の行（備考 `Thruster control mapping failure, electrical problems`）',
               src='USCG p.235〈227〉（`The pilot overcame the malfunctioning thrusters by turning the controller around and operating the controls in reverse.`）・USCG p.311〈303〉（`the dive proceeded after the pilot compensated for the failures instead of ascending for repairs in a controlled environment.`）'),
    'ca16': dict(kind='図解',
               plan='台本の画：図 線 時刻に沿って並べたひずみ（潜航ごとの線が横に並ぶ＝比べにくい形の模式）',
               src='NTSB p.51（`OceanGate analyzed hull strain by plotting it side-by-side with dive depth as a function of time.`）・NTSB p.64（`analyzing strain data in this way was flawed because it was difficult for OceanGate to compare data between dives.`）'),
    'ca17': dict(kind='図・写真の頁',
               plan='台本の画：図 NTSB 図21 の左（75回目と80回目の浅い1,000m のひずみ＝出どころの注なし＝NTSB・A・額装か記録の点で描き直す）',
               src='NTSB p.53（`Through dive 80, the strain response of the hull was linear at all depths (a typical mechanical behavior).`）'),
    'ca18': dict(kind='図・写真の頁',
               plan='台本の画：図 NTSB 図21 の右（81〜83回目の浅い所の「Non-linear behavior」を明るく）',
               src='NTSB p.53（`During dive 81, the first dive after the audible event, the strain response at low depth was non-linear.`）・NTSB p.59 脚注42（`The strain response at greater depths remained linear, similar to previous dives`）'),
    'ca19': dict(kind='図解',
               plan='台本の画：図 模式 層がはがれた筒（浅い所で線が曲がるしくみ・ひずみ計の位置＝筒の前の端）',
               src='NTSB p.59（`This change in strain response is more consistent with a delamination between layers.`）・p.59（`indicating that the damage extended to the forward end of the cylinder.`）'),
    'ca20': dict(kind='図解',
               plan='台本の画：図 棒 浅い所（10〜300m）のひずみの傾き（2021-08-05＝全体より21%大きい／2022-07-19＝98%大きい＝カナダの調べの値）',
               src='TSB §1.10.10.1（`the strain slope was found to be 98% greater than the slope for the entire dive profile.`）'),
    'ca21': dict(kind='図解',
               plan='台本の画：図 帯 3つの見方の並べ（米沿岸警備隊＝強く示す／米運輸安全委＝可能性が高い／カナダ＝決められない）',
               src='USCG p.289〈281〉（`strongly suggests that the carbon fiber hull sustained irreversible damage at the end of Dive 80.`）・USCG p.289〈281〉（`It is likely that the loud bang heard on the surface during Dive 80 was the result of a sudden delamination occurring between layers 1 and 2`）・NTSB p.59（`the NTSB concludes that the Titan pressure vessel likely sustained damage after it surfaced at the end of dive 80`）'),
    'ca22': dict(kind='図解',
               plan='台本の画：図 帯 同じ並べ（カナダの段を明るく）',
               src='TSB §1.10.10.1（`so it cannot be determined whether this event precipitated the non-linear readings on 19 July 2022.`）'),
    'ca23': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 監視装置の画面（音の数の目盛り＝30で黄・50で赤・音の警報なし＝スピーカーに×・潜航ごとにゼロへ戻る矢印）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 監視装置の決まり（30で黄・50で赤・警報の音なし・潜航ごとにゼロ）',
               src='NTSB p.31（`if the system detected 30 hits during a dive, the system issued a yellow display warning.`）・TSB §1.10.9（`The system did not have audible alarms.`）・NTSB p.31（`Hit counts did not accumulate between successive dives, and hits while at the surface were not counted.`）'),
    'ca24': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 音のセンサー8つの配置（筒の輪に8つの点＝5つは青・1・3・5番の3つは灰＝2022年に一度も音を拾わず）＝MBI 図105（NTSB の配置図）を描き直す｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 センサー8つのうち3つ（1・3・5番）が2022年の潜航で一度も音を拾わず',
               src='NTSB p.51（`Three of the eight acoustic sensors (channels 1, 3, and 5) did not register acoustic events for any of the 2022 dives.`）・USCG p.282〈274〉（`OceanGate operated TITAN with three out of eight sensors (37.5%) inoperable was reckless`）'),
    'ca25': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 警告の基準の出どころ（1つ目の船体と模型の音 → 基準 → 2つ目の船体に当てる矢印・「作り方が違う」の札）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 警告の基準の出どころ（1つ目の船体と模型の音＝作り方の違う船体）',
               src='NTSB p.31（`The warning levels were based on the acoustic activity of the v1 pressure vessel`）・NTSB p.64（`the v1 full-scale pressure vessel and sub-scale models were manufactured using a different method`）・NTSB p.65（`never produced the type of acoustic emission signal that would have triggered an alert and thus did not detect the initial damage.`）'),
    'ca26': dict(kind='図解',
               plan='台本の画：図 帯 2022年7月から2023年6月までの帯（タイタニックの深さへの最後の潜航〈7月22日〉→事故まで約11か月）',
               src='USCG p.290〈282〉（`should have been a red flag to stop all dive operations.`）・NTSB p.60（`Therefore, the pressure vessel must have sustained additional damage after dive 82 and before the casualty dive 11 months later (dive 88).`）'),
}

SPEC = {}
