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
               plan='🆕 N21:左｜見せ方：額装（報告書の図）｜副題：75回目と80回目のひずみ（浅い1,000メートル）｜動き：額ごと寄る｜権利：A（NTSB）｜出典の行：米運輸安全委員会の報告書 図21｜注：⑤b-7 で額装に決めた（束で左右に割る）・英字の札は訳の札｜台本の画：図 NTSB 図21 の左（75回目と80回目の浅い1,000m のひずみ＝出どころの注なし＝NTSB・A・額装か記録の点で描き直す）',
               src='NTSB p.53（`Through dive 80, the strain response of the hull was linear at all depths (a typical mechanical behavior).`）'),
    'ca18': dict(kind='図・写真の頁',
               plan='🆕 N21:右｜見せ方：額装（報告書の図）｜副題：81〜83回目のひずみ（浅い1,000メートル）｜動き：止め（語りの1行目で曲がった所を印で明るく）｜権利：A（NTSB）｜出典の行：米運輸安全委員会の報告書 図21｜注：⑤b-7 で額装に決めた・英字の札は訳の札｜台本の画：図 NTSB 図21 の右（81〜83回目の浅い所の「Non-linear behavior」を明るく）',
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

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-10-15）：図解 第9章（23カット）＝模式図 `tools/mech22.py`・時間の帯（axis）・棒（qty）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「2022年7月15日の音」と4字以上同じ並び（「2022年」「7月15日」）を見出し・副題に入れない（門番 dup）。字は12字未満（門番 echo）。
#      写真 ca03 と NTSB 図21 の頁 ca17・ca18 は ⑤b-7
_N_PP = "句は米沿岸警備隊の報告書（英字のまま・模式）"
_N_SAY = "人の形は模式（顔は描かない）"
SPEC.update({
    # ca01（2行）＝🔧 再現→点（付録B の潜航・2022年の段だけ残す）。聞き役の問い→人が乗った潜航13回のうち7回がタイタニックの深さまで
    "ca01": dict(
        t="次の年の夏", s="人が乗った潜航",
        fig=("m22", dict(view="dives", steps=[dict(state=dict(y22="on")), dict(state=dict(reach="on"), tag=dict(t="13回のうち7回", at="t"))],
                         rel=[dict(t="13回のうち7回", src="USCG p235")],
                         note="点の並びは模式（カナダの報告書 付録B の行）", src=ss.src(["TSB §付録B", "USCG p235", "NTSB p1035"]))),
    ),
    # ca02（3行）＝🔧 再現→上から見た船首（見る向き＝上から・北が上）。7月3日、左舷の船首にぶつかる→回収のときに動けず→聞き役
    "ca02": dict(
        t="船首にぶつかる", s="7月3日の潜航",
        fig=("m22", dict(view="bow", steps=[dict(state=dict(hit="on"), tag=dict(t="左舷の船首", at="hit", col=J.ALERT)),
                                            dict(tag=dict(t="回収で動けず", at="hit2")), dict()],
                         note="位置は模式（カナダの報告書 付録B の備考）", src=ss.src(["TSB §付録B", "TSB §2.1.3"]))),
    ),
    # ca04（2行）＝米沿岸警備隊の報告書の要点（80回目＝7月15日の階段の吹き抜け）。少しのあいだ動けず→事故の報告は出されなかった
    #   紙の見出しで「80回目（2022年7月15日）」と出す（次の ca05「その帰り」と合う）
    #   ✅ ⑤c'（10-15）：語りは ca03 の「そして7月15日…階段に引っかかった」の続き＝80回目（USCG p233 4.34.8「Dive 80」・p311）と合う
    #      ＝⑤b-5 の「ca02（7月3日）の続きに聞こえる」は今の語りに当てはまらない（係の照合）
    "ca04": dict(
        t="引っかかった艇", s="報告されず",
        fig=("m22", dict(view="paper", start=dict(doc="u80"), steps=[dict(state=dict(hl1="on", hl2="on")), dict(state=dict(hl3="on"))],
                         note=_N_PP, src=ss.src(["USCG p233", "USCG p311"]))),
    ),
    # ca05（2行）＝🔧 80回目の深さの線（NTSB 図19 を原寸で読んだ点）。浮上の終わりの大きな音（海面の線）→中の人と海面の小舟の人が聞いた
    "ca05": dict(
        t="海面の近くの音", s="その日の帰り",
        fig=("m22", dict(view="d80", steps=[dict(state=dict(line="on", bang="on"), tag=dict(t="大きな音", at="bang", col=J.ALERT)),
                                            dict(state=dict(who="on"), tag=[dict(t="海面の小舟", at="boat", col=J.SHIP), dict(t="艇の中", at="inner", col=J.SUB)])],
                         note="線は米運輸安全委員会の図19 を原寸で読んだ点（±2分・あいだは直線＝模式）・元は会社の記録",
                         src=ss.src(["NTSB p1052", "USCG p283", "USCG p234", "NTSB p1036"]))),
    ),
    # ca06（3行）＝聞き役の問い→音のセンサー8・ひずみ計16→ひずみ＝押されて少し縮む
    "ca06": dict(
        t="監視の装置", s="音とひずみ",
        fig=("m22", dict(view="rtm", steps=[dict(), dict(state=dict(ae="on", sg="on"), tag=[dict(t="音のセンサー 8", at="t1", col=J.INK_W),
                                                                                        dict(t="ひずみ計 16", at="t2", col=J.AMBER)]),
                                            dict(state=dict(squeeze="on"), tag=dict(t="押されて少し縮む", at="l2", col=J.INK_W))],
                         rel=[dict(t="8", src="NTSB p1031"), dict(t="16", src="NTSB p1031（輪の向き8・長さの向き8）")],
                         note="位置は模式（米沿岸警備隊の報告書 図105 をもとに）・ひずみ計は1か所に2つ", src=ss.src(["NTSB p1031", "USCG p139"]))),
    ),
    # ca07（2行）＝米沿岸警備隊の分析。15:26:45 に大きな音の山→同じ瞬間にひずみも跳ぶ
    "ca07": dict(
        t="音の山", s="装置がとらえた",          # ⚠️ 門番 echo：「米沿岸警備隊の分析」は語りの写し
        fig=("m22", dict(view="ae", steps=[dict(state=dict(peak="on"), tag=dict(t="15:26:45", at="peak", col=J.ALERT)),
                                           dict(state=dict(jump="on"), tag=dict(t="同じ瞬間に跳ぶ", at="jump", col=J.ALERT))],
                         rel=[dict(t="15:26:45", src="USCG p283")],
                         note="線の形は模式（記録の時刻だけ）・元は会社の記録", src=ss.src(["USCG p283", "USCG p286"]))),
    ),
    # ca08（2行）＝同じ図。15:17ごろから増え始め（米沿岸警備隊）→米運輸安全委員会は 15:15〜15:30ごろの幅
    "ca08": dict(
        t="増え始め", s="2つの書き方",
        fig=("m22", dict(view="ae", start=dict(peak="on", jump="on"),
                         steps=[dict(state=dict(up="on"), tag=dict(t="15:17ごろから", at="up", col=J.USCG)),
                                dict(state=dict(band="on"), tag=dict(t="15:15〜15:30ごろ", d="米運輸安全委員会", at="band", col=J.OK))],
                         rel=[dict(t="15:17", src="USCG p283"), dict(t="15:15〜15:30", src="NTSB p1052")],
                         note="線の形は模式（記録の時刻だけ）・元は会社の記録", src=ss.src(["USCG p283", "NTSB p1052"]))),
    ),
    # ca09（2行）＝会社の説明（艇が枠の中でずれた）→社員と客にもそう伝えられた
    "ca09": dict(
        t="会社の結論", s="ずれた音",
        fig=("m22", dict(view="paper", start=dict(doc="shift"), steps=[dict(state=dict(hl1="on")), dict(state=dict(hl2="on"))],
                         note="句は米国の2つの報告書の記述（英字のまま・模式）", src=ss.src(["USCG p233", "NTSB p1036"]))),
    ),
    # ca10（3行）＝聞き役の問い→外から見ただけ・内張りは外さず（×）→休ませて詳しく調べることもしなかった（×）
    "ca10": dict(
        t="見なかった所", s="内張りの内側",
        fig=("m22", dict(view="none", start=dict(set="insp"),
                         steps=[dict(), dict(state=dict(n="1"), tag=dict(t="外から見ただけ", at="t", col=J.COMPANY)), dict(state=dict(n="2"))],
                         note="欄は要点（模式）", src=ss.src(["USCG p289", "USCG p290"]))),
    ),
    # ca11（2行）＝人の言葉（CEO が当時の技術部長に）。2行目で吹き出し
    "ca11": dict(
        t="CEO の言葉", s="技術部長へ",
        fig=("m22", dict(view="say", start=dict(set="again"), steps=[dict(), dict(state=dict(n="1"))],
                         note=_N_SAY + "・英字は米運輸安全委員会の報告書が引く言葉", src=ss.src(["NTSB p1036"]))),
    ),
    # ca12（2行）＝CEO の指示（次の潜航の前・冬の休みのあいだ）→それ以上の調べは要らない
    "ca12": dict(
        t="調べは要らない", s="冬の休みも",
        fig=("m22", dict(view="paper", start=dict(doc="u290a"), steps=[dict(state=dict(hl2="on", hl3="on")), dict(state=dict(hl1="on"))],
                         note=_N_PP, src=ss.src(["USCG p290"]))),
    ),
    # ca13（3行）＝米沿岸警備隊の見方（技術部長も、判断する立場の誰も→ひずみのデータを読み解く専門の力が無かった）→聞き役
    "ca13": dict(
        t="読める人がいない", s="専門の力",
        fig=("m22", dict(view="paper", start=dict(doc="u290b"),
                         steps=[dict(state=dict(hl1="on", hl2="on", hl3="on")), dict(state=dict(hl4="on", hl5="on")), dict()],
                         note=_N_PP, src=ss.src(["USCG p290"]))),
    ),
    # ca14（2行）＝年表（2022年7月）。80回目（15日）のあと 19日 81回目・22日 82回目→23日 83回目（別の場所・2,954メートル）
    "ca14": dict(
        t="続けた潜航", s="4日後から",
        fig=("axis", dict(ss.AX_J22, past=[ss.ax("d80")], start=dict(cur="2022-07-15"),
                          steps=[dict(add=[ss.ax("d81"), ss.ax("d82")], cur="2022-07-22"), dict(add=[ss.ax("d83"), ss.ax("d83m")], cur="2022-07-23")],
                          note="日付は米国の2つの報告書とカナダの報告書 付録B", src=ss.src(["NTSB p1036", "USCG p235", "TSB §付録B", "NTSB p1051"]))),
    ),
    # ca15（1行）＝🔧 再現→模式。81回目＝推進器の操作が逆→操縦士はコントローラーを逆さに持って続けた
    "ca15": dict(
        t="操作の向き", s="19日の潜航",
        fig=("m22", dict(view="ctrl", steps=[dict(state=dict(flip="on"), tag=dict(t="逆さに持って続ける", at="flip", col=J.SUB))],
                         note="形は模式（米沿岸警備隊の報告書の記述）", src=ss.src(["USCG p235", "USCG p311"]))),
    ),
    # ca16（2行）＝会社はひずみを時刻に沿って並べた→米運輸安全委員会＝潜航どうしを比べにくい
    "ca16": dict(
        t="時刻に沿った線", s="潜航ごとに横並び",
        fig=("m22", dict(view="stime", steps=[dict(state=dict(on="on")), dict(state=dict(hard="on"), tag=dict(t="比べにくい", d="米運輸安全委員会", at="hard", col=J.OK))],
                         note="線の形は模式（値ではない）", src=ss.src(["NTSB p1051", "NTSB p1064"]))),
    ),
    # ca19（3行）＝聞き役の問い→層のはがれ＝浅い所は別々に動き、深い所はまとまって動く→計器は筒の前の端＝傷みはそこまで
    "ca19": dict(
        t="浅い所の曲がり", s="層のはがれ",
        fig=("m22", dict(view="nonlin", steps=[dict(), dict(state=dict(bend="on", zones="on"), tag=[dict(t="浅い所＝別々に動く", at="sh", col=J.ALERT),
                                                                                                dict(t="深い所＝まとまる", at="deep", col=J.INK_W)]),
                                               dict(state=dict(fwd="on"), tag=dict(t="計器は筒の前の端", at="fwd", col=J.AMBER))],
                         note="線と形は模式（米運輸安全委員会の説明）", src=ss.src(["NTSB p1059"]))),
    ),
    # ca20（2行）＝棒（浅い所 10〜300m の傾きの増え）。カナダの調べも計算→2021年8月5日 21%・2022年7月19日 98%
    "ca20": dict(
        t="傾きの比べ", s="カナダの計算",
        fig=("qty", dict(view="bar", groups=[ss.QG["slope"]], steps=[dict(), dict(add=[ss.qb("slope21"), ss.qb("slope22")])],
                         note="その潜航の全体の傾きと比べた増え（10〜300メートル）", src=ss.src(["TSB §1.10.10.1"]))),
    ),
    # ca21（2行）＝3つの見方。アメリカの2つの調べ＝あの潜航の終わりに層のはがれの形で傷んだ可能性が高い
    "ca21": dict(
        t="アメリカの見方", s="2つの調べ",
        fig=("m22", dict(view="cards", start=dict(set="views"), steps=[dict(state=dict(n="2")), dict(tag=dict(t="80回目の終わり", d="層のはがれ", at="low"))],
                         rel=[dict(t="80回目", src="USCG p289・NTSB p1059")],
                         note="要点（模式）", src=ss.src(["USCG p289", "NTSB p1059"]))),
    ),
    # ca22（3行）＝同じ並び。カナダの調べ＝決められない（会社が音のあと船体をきちんと調べなかった）→聞き役
    "ca22": dict(
        t="決めない理由", s="会社が調べず",
        fig=("m22", dict(view="cards", start=dict(set="views", n="2"),
                         steps=[dict(state=dict(n="3")), dict(tag=dict(t="船体を調べず", d="カナダの調べ", at="low3", col=J.INST)), dict()],
                         note="要点（模式）", src=ss.src(["TSB §1.10.10.1"]))),
    ),
    # ca23（2行）＝🔧 再現→模式（画面）。音の数 30で黄・50で赤→警報の音なし・潜航ごとにゼロへ
    "ca23": dict(
        t="画面の色", s="監視の決まり",
        fig=("m22", dict(view="screen", steps=[dict(state=dict(lv="on")),
                                               dict(state=dict(mute="on", reset="on"), tag=[dict(t="警報の音なし", at="mute", col=J.ALERT),
                                                                                           dict(t="潜航ごとに0へ", at="reset")])],
                         rel=[dict(t="0", src="NTSB p1031")],
                         note="画面の形は模式（決まりは米運輸安全委員会とカナダの報告書）", src=ss.src(["NTSB p1031", "TSB §1.10.9"]))),
    ),
    # ca24（3行）＝🔧 再現→模式。音のセンサー8つのうち3つ→2022年の潜航で一度も拾わず（灰）→米沿岸警備隊＝無謀
    "ca24": dict(
        t="拾わない3つ", s="黙ったまま",
        fig=("m22", dict(view="rtm", start=dict(ae="on"),
                         steps=[dict(tag=dict(t="8つのうち3つ", at="t1", col=J.INK_W)),
                                dict(state=dict(dead="on"), tag=dict(t="一度も拾わず", d="2022年の潜航", at="t2", col=J.TICK)),
                                dict(tag=dict(t="無謀だった", d="米沿岸警備隊", at="l2", col=J.USCG))],
                         rel=[dict(t="8つのうち3つ", src="NTSB p1051"), dict(t="2022年", src="NTSB p1051")],
                         note="位置は模式（米沿岸警備隊の報告書 図105 をもとに・番号は描いていない）", src=ss.src(["NTSB p1051", "USCG p282", "USCG p139"]))),
    ),
    # ca25（3行）＝🔧 再現→模式（流れ）。警告の基準＝作り方の違う1つ目の船体と模型の音で決めた→2つ目の船体には警告にならず→聞き役
    "ca25": dict(
        t="基準の出どころ", s="別の作りの船体",
        fig=("m22", dict(view="cards", start=dict(set="base"),
                         steps=[dict(state=dict(n="2"), tag=dict(t="作り方が違う", at="a23", col=J.ALERT)), dict(state=dict(n="3")), dict()],
                         note="流れは模式（米運輸安全委員会の報告書）", src=ss.src(["NTSB p1031", "NTSB p1064", "NTSB p1065"]))),
    ),
    # ca26（3行）＝年表（2022年7月〜2023年6月）。80回目の音→止めるべき赤信号（米沿岸警備隊）→最後の深い潜航（7月22日）から事故の潜航まで約11か月
    "ca26": dict(
        t="見送られた合図", s="次の夏まで",
        fig=("axis", dict(ss.AX_2223, steps=[dict(add=[ss.ax("bang15")], cur="2022-07-15"), dict(add=[ss.ax("flag")]),
                                              dict(add=[ss.ax("last82"), ss.ax("occ23"), ss.ax("m11")], cur="2023-06-18")],
                          note="日付はカナダの報告書 付録B・赤信号は米沿岸警備隊の書き方", src=ss.src(["USCG p290", "NTSB p1060", "TSB §付録B"]))),
    ),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-15）：写真と NTSB 図21（3カット）＝映像方針の一覧（了承②）。副題は焼いた絵を原寸で見てから最終に
# ══════════════════════════════════════════════════════════
#   ca03＝第三者（個人の撮影＝NTSB 図8）＝額装だけ・色を変えない（color=1.0）・額ごと動かす・サムネに使わない。
#   ca17・ca18＝NTSB 図21（ひずみ計の出力と深さ＝浅い1,000メートル・PDF 53頁の埋め込みの画像 1430×515）を束で左右に割った（黒い帯の割り目）。
#   英字の札は訳の札を添える（ルール §B1-4）。ca18 は語りの1行目「浅い所で線が曲がっていた」で、曲がった所（81〜83回目の深さ 0〜約400メートル）を
#   頁の上の印（hl）で明るく＝印の範囲は図の目盛りから（右の図の x＝2,480〜2,560 mV・y＝深さ 0〜約400 m＝図の割合）
_LAUNCH = P("ntsb_fig08_launch_2022")
_STR_L = P("ntsb_fig21_strain_l")
_STR_R = P("ntsb_fig21_strain_r")
SPEC.update({
    # ca03（12.2秒）＝台ごと海へ降ろされるタイタン（2022年・個人の撮影＝NTSB 図8）・額ごと寄る
    "ca03": dict(photo=_LAUNCH, panel=True, color=1.0, fmove=ss.fm("in"), t="階段に引っかかる", s="台ごと海へ降ろされるタイタン（2022年）"),
    # ca17（7.8秒）＝NTSB 図21 の左（75回目と80回目＝潜る線と浮かぶ線がまっすぐ）・額ごと寄る
    "ca17": dict(photo=_STR_L, panel=True, fmove=ss.fm("in"), t="まっすぐな線", s="75回目と80回目のひずみ（浅い1,000メートル）",
                 ann=[dict(t="青と赤の点", d="75回目と80回目の潜航"), dict(t="縦の目盛り", d="海の深さ（メートル）"),
                      dict(t="横の目盛り", d="ひずみ計の出力"), dict(t="2本の矢印", d="潜る・浮かぶ")]),
    # ca18（7.5秒）＝NTSB 図21 の右（81〜83回目＝浅い所で曲がる「Non-linear behavior」の矢印は NTSB の物）。
    #   額は動かさない（門番 fmove＝額ごと動かすカットに hl を混ぜない）＝動きは語りと同時に走る印
    "ca18": dict(photo=_STR_R, panel=True, t="音のあとの潜航", s="81〜83回目のひずみ（浅い1,000メートル）",
                 hl=[(0, 0.5, 1.0, (0.32, 0.52, 0.57, 0.89))],
                 ann=[dict(t="黄・水色・紫の点", d="81〜83回目の潜航"), dict(t="左下の札と矢印", d="まっすぐでない線"),
                      dict(t="縦の目盛り", d="海の深さ（メートル）"), dict(t="2本の矢印", d="潜る・浮かぶ")]),
})
