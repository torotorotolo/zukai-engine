# -*- coding: utf-8 -*-
"""第4章　96時間 c501–c523（23カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c5.py`）。
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
    'c501': dict(kind='図解',
               plan='🔧 注：🔧 実写→帯（語りは「母船にいた会社の担当」＝米沿岸警備隊の指令センターの映像を出すと取り違える）｜新しい画（映像方針）：図 帯 母船から送り続けた文（1分に2〜3回の水色の印が並ぶ・潜水艇の返事の段は空のまま）＝c316 の模式の続き｜台本の画（🔧映像方針で替えた＝元の予定）：実写 指令センターの B-roll（DVIDS 887734・2023-06-20・c107 と別の区間・A＝副題「米沿岸警備隊の指令センター（6月20日）」）',
               src='NTSB p.17（`first assumed there was an issue with the acoustic communications equipment`…`sent two to three messages every minute`）・USCG p.39〈31〉（`None of the messages were answered and the TITAN’s location was never reacquired by the POLAR PRINCE.`）'),
    'c502': dict(kind='図解',
               plan='台本の画：図 帯 会社の手順の流れ（途絶→1時間＋浮上にかかる時間→社内へ連絡→さらに3時間の海面の捜索→外へ・札「事情によっては短くしてよい」）',
               src='USCG p.39〈31〉（`Internal contacts and backup personnel will be called following 1 hour of no communications plus required surface time`）・p.39〈31〉（`An additional 3 hours of local surface search will be done before contacting outside emergency personnel unless circumstances merit a shorter delay.`）'),
    'c503': dict(kind='図解',
               plan='台本の画：図 帯 6月18日の午後の時刻の帯（15:00 浮上の見込み・海面の捜索を始める）',
               src='TSB §1.3.3（`the estimated resurfacing time was approximately 3 hours and 13 minutes (at 1500)`）・§1.3.3（`At 1500, with no communication from the Titan, the Polar Prince commenced the 3-hour surface search.`）'),
    'c504': dict(kind='図解',
               plan='台本の画：図 帯 同じ帯（16:34 陸の班へ電話・18:00 手がかりなし）',
               src='TSB §1.3.3（`At 1634, as the surface search was ongoing, the master of the Polar Prince called the Horizon Maritime Services Ltd. shore-based emergency team`）・§1.3.3（`By 1800, the surface search had found no signs of the submersible.`）'),
    'c505': dict(kind='図解',
               plan='台本の画：図 帯 同じ帯（18:27 電話が切れた・18:55 カナダの救難調整センターへ→ボストンへ）',
               src='USCG p.39〈31〉（`I called the Joint Rescue Coordination Centre (JRCC) Halifax by sat phone but communications with JRCC were shortly thereafter cut-off.`）・TSB §1.3.3（`At 1855, the master of the Polar Prince called the Joint Rescue and Coordination Centre (JRCC) in Halifax`…`JRCC transferred the call to the Rescue Coordination Centre (RCC) in Boston`）'),
    'c506': dict(kind='図解',
               plan='台本の画：図 帯 同じ帯（10:47 から 18:55 までを1本の矢印に・「8時間8分」の札）',
               src='TSB §2.5（`This was 8 hours and 8 minutes after communication and tracking had been lost`）'),
    'c507': dict(kind='図解',
               plan='台本の画：図 模式 母船の上の2つの組（会社の潜航の班と、船の会社の船長＝取り決めの書類が無い・船長の権限がはっきりしない）',
               src='TSB §2.5（`the situation with the Titan initially appeared to be a communication and tracking loss, and so the surface support team followed the missed communications protocol.`）・TSB §2.6（`the master’s authority in the loss of communication emergency with the Titan was unclear`）・§2.6（`Without a bridging document`）・§2.6（`missed communications protocol ended up taking precedence even though it did not follow the maritime best practice of notifying SAR authorities as soon as possible once the potential need for help developed`）'),
    'c508': dict(kind='写真',
               plan='🔧 U734｜区間 54.2〜66.6秒｜倍率 1.15（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：米沿岸警備隊の指令センター（6月20日）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 887734）｜注：🔧 素材を替えた（記者会見 887718 → 指令センター＝語り「知らせを受けた米沿岸警備隊は」）・眼鏡の隊員の席（ショット10）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 USCG の記者会見（DVIDS 887718・2023-06-20・A＝副題「6月20日の記者会見（米沿岸警備隊）」）',
               src='USCG p.40〈32〉（`The United States Coast Guard First District was not aware of the TITAN’s TITANIC Expedition dive operations on this date`）・p.40〈32〉（`entered the distress phase`）'),
    'c509': dict(kind='写真',
               plan='🔧 D471｜見せ方：全面｜副題：捜索に加わった米沿岸警備隊の輸送機｜動き：右へ｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 7875471）｜注：🔧 素材を替えた（888011＝米空軍州兵の機体 → 米沿岸警備隊の HC-130＝語り「米沿岸警備隊の輸送機が飛び立ち」）。格納庫の写真＝飛ぶ所ではない＝副題に日時を書かない｜台本の画（🔧映像方針で替えた＝元の予定）：実写 HC-130J の B-roll（DVIDS 888011・2023-06-21・第106救難航空団・A＝副題「捜索に加わった米軍の輸送機（6月21日）」）',
               src='NTSB p.19（`At 2200, a US Coast Guard C-130 Hercules`）・p.19（`At 2325, the C-130 arrived on scene and began conducting an overflight air search.`）'),
    'c510': dict(kind='写真',
               plan='D444｜見せ方：全面｜副題：捜索中の米沿岸警備隊の輸送機の操縦席（6月21日）｜動き：上へ｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 7875444）｜注：背中だけ・顔は写らない｜台本の画：実写 DVIDS 7875444 HC-130 の操縦席（2023-06-21・背中だけ・顔は写らない・A＝副題「捜索中の輸送機の操縦席（6月21日）」）',
               src='TSB §1.3.3（`In total, the SAR response involved 11 vessels and 4 aircraft, which searched approximately 12 000 square nautical miles of ocean.`）'),
    'c511': dict(kind='写真',
               plan='D448｜見せ方：全面｜副題：捜索の機内から見た海（6月21日）｜動き：右へ｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 7875448）｜注：原本が487KB＝幅は取ってから測る（小さければ額装）｜台本の画：実写 DVIDS 7875448 機内から見た海と船（2023-06-21・A＝副題「捜索の機内から見た海（6月21日）」）',
               src='USCG p.40〈32〉（`later to be joined by P-3 aircraft with sonobuoys`）'),
    'c512': dict(kind='写真',
               plan='U852｜区間 493.5〜501.0秒｜倍率 0.74（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：6月21日の記者会見（米沿岸警備隊）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 887852）｜注：第1管区の担当の大佐・器も実効も1280・倍率0.69（502秒からカメラが動く＝その前）｜台本の画：実写 USCG の記者会見（DVIDS 887852・2023-06-21・器 1280・A＝副題「6月21日の記者会見（米沿岸警備隊）」）',
               src='USCG p.325〈317〉（`due to the instantaneous implosion occurring prior to the initial distress call`）'),
    'c513': dict(kind='写真',
               plan='U597｜区間 535.0〜547.5秒｜倍率 1.07（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：6月19日の記者会見（米沿岸警備隊）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 887597）｜注：司令官の寄り（動かないカメラ）｜台本の画：実写 USCG の記者会見（DVIDS 887597・2023-06-19・A＝副題「6月19日の記者会見（米沿岸警備隊）」）',
               src='NTSB p.20（`with two ROVs capable of reaching 9,843 feet (3,000 meters)`）・p.20（`they dove the ROV beyond its rated depth, almost another 3,281 feet (1,000 meters); the ROV was destroyed in the process.`）'),
    'c514': dict(kind='図解',
               plan='🔧 G03｜注：🔧 実写→衛星写真の地図（格納庫の HC-130 は別の機体・了承②）｜新しい画（映像方針）：図 地図 衛星写真 G03（バッファロー→ニューファンドランド）＋線と輸送機の印・「6,000mまで潜れるROV」の札｜台本の画（🔧映像方針で替えた＝元の予定）：実写 DVIDS 7875471 格納庫の HC-130（A＝副題「捜索に出た米沿岸警備隊の輸送機」）',
               src='NTSB p.18（`which was capable of reaching 19,685 feet (6,000 meters). (The Odysseus was in Buffalo, New York, at the time.)`）・USCG p.41〈33〉（`emergency transportation of a Pelagic® Odysseus ROV from Buffalo, NY`）・NTSB p.20（`flew the ROV Odysseus on a C-130 to Newfoundland and Labrador, where it was loaded aboard the Horizon Arctic`）'),
    'c515': dict(kind='図解',
               plan='🔧 G04｜注：🔧 自作の地図→衛星写真（了承②）｜新しい画（映像方針）：図 地図 衛星写真 G04（北大西洋）＋セントジョンズ・現場の点・フランスの調査船が向かってきた向きの矢印だけ｜台本の画（🔧映像方針で替えた＝元の予定）：図 地図 北大西洋（セントジョンズ・現場・フランスの調査船が向かってきた向き＝矢印だけ）',
               src='USCG p.42〈34〉（`The French research vessel ATALANTE responded from mid-ocean, carrying the 6,000-meter-capable ROV VICTOR 6000.`）・NTSB p.20（`On June 22, both the Atalante (with the Victor 6000) and the Horizon Arctic (with the Odysseus) were in position over the site.`）'),
    'c516': dict(kind='写真',
               plan='🔧 U011｜区間 136.0〜142.2秒｜倍率 0.96（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：捜索に向かう米空軍州兵の隊員（6月21日）｜動き：映像｜権利：A（米空軍州兵＝第106救難航空団の職務・連邦の任務の扱いが弱い所）｜出典の行：米空軍州兵 第106救難航空団（DVIDS 888011）｜注：🔧 素材を替えた（888012 の別の区間 → 888011＝隊員が機体へ歩く＝語り「支度を数日で」）・後ろ姿｜台本の画（🔧映像方針で替えた＝元の予定）：実写 HC-130J の B-roll（DVIDS 888012・c103 と別の区間・A）',
               src='USCG p.41〈33〉（`what would typically take two weeks—mobilizing an ROV, modifying a vessel, and assembling a crew—was achieved in days.`）'),
    'c517': dict(kind='写真',
               plan='R04｜区間 18.52〜28.61秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：海の底で見つかった尾部（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：尾部に近づく（26秒に照明が少し変わる＝目立たない・1秒1コマで見た）｜台本の画：実写 ROV「尾部」（04 の中ほど・c101・c108 と別の区間・第三者＝引用・額装＝副題「6月22日、海の底で見つかった尾部」）',
               src='USCG p.7〈vii〉（`On June 22, 2023, at approximately 9:40 a.m.`）・TSB §1.3.3（`At approximately 1040, the ROV discovered the Titan’s forward dome and tail piece on the seabed.`）'),
    'c518': dict(kind='図解',
               plan='台本の画：図 帯 96時間の帯（6/18 08:24 ドームを閉めた→6/22 08:24＝96時間→05:40 ROV を降ろす〈93時間16分〉→10:40ごろ 発見〈98時間16分〉＝カナダの調べの値）',
               src='TSB §1.2.1（`enough oxygen to last approximately 96 hours based on an occupancy of 5 people`）・TSB §2.5（`98 hours and 16 minutes after life support had been started on the Titan`）'),
    'c519': dict(kind='写真',
               plan='U022｜区間 468.0〜477.5秒｜倍率 0.98（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：6月22日の記者会見（米沿岸警備隊）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 888022）｜注：米海軍の引き揚げの職員が身ぶりで話す（公的な任務）｜台本の画：実写 USCG の記者会見「残骸の発見」（DVIDS 888022・c102・c106・c109 と別の区間・A）',
               src='TSB §2.5（`neither the actual response nor any other response would have changed the outcome given that the Titan’s crew and passengers were fatally injured at the time of the implosion`）'),
    'c520': dict(kind='図解',
               plan='見る向き：横から｜台本の画：図 線 タイタンの線画（前のドームを明るく＝外から留めるボルトの位置の札・ハッチなし）',
               src='TSB §2.5（`Other aspects of the Titan’s design and operations may also have hindered a rescue.`）・§2.5（`the Titan did not have a hatch so its crew and passengers could not egress on the surface without the Titan first being reattached to the LARS`）'),
    'c521': dict(kind='図解',
               plan='台本の画：図 模式 救助の備え（「水の中の位置を知る手段」「ROV の会社との契約」の2つの欄が空）',
               src='TSB §2.5（`OceanGate also did not have a means of determining where the Titan was underwater if the tracking and communication systems on the submersible were not functioning.`）・§2.5（`When conducting diving operations, OceanGate also did not have any contracts in place with these ROV operators.`）'),
    'c522': dict(kind='写真',
               plan='R07｜区間 2.0〜9.72秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：海の底に残った前のドーム（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：散らばった破片→遠くに前のドーム｜台本の画：実写 ROV「前のドーム」（07・c104 と別の区間・第三者＝引用・額装）',
               src='NTSB p.66（`they likely would have had emergency response assets standing by and the Titan likely would have been found sooner`）'),
    'c523': dict(kind='写真',
               plan='R07｜区間 54.25〜60.0秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：残骸が詰まった後ろのドーム（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：→ 次の章の扉（頭の c601 が ROV＝扉の地は方眼だけ）｜台本の画：実写 ROV「後ろのドーム」（07・c105 と別の区間・第三者＝引用・額装）→ 次の章の扉',
               src='—'),
}

SPEC = {}

# ── 🆕 ⑤b-3（2026-10-14）：地図のカット（衛星写真＋描き足し＝`tools/satmap.py`・c2.py の注）──
SPEC.update({
    # c514（2行）＝1行目でバッファローの ROV・2行目で米空軍の輸送機（C-130＝NTSB p.20）でニューファンドランドへ（線は2点を結んだだけ）
    "c514": dict(**ss.sat("G03", note="地点は一般の座標・線は2点を結んだだけ（実際の飛行の経路ではない）", steps=[
        #   🔧 ⑤b-3 の試し焼き（Modal qa-ep22_b3_map）：「ROV の置き場」が点の右上で線に貫かれ、「米空軍の輸送機」が「ニューファンドランド」の
        #      すぐ下で1つの札に読めた＝ROV は点の下・輸送機は印の下へ
        [dict(k="pt", at="buffalo", c="INK_W", t="ROV の置き場", lab=(0, 58, "middle"))],
        [dict(k="line", path=("buffalo", "stjohns"), c="INK_W", dash=True),
         dict(k="icon", what="plane", on=("buffalo", "stjohns", 0.55), c="INK_W", t="米空軍の輸送機", lab=(0, 58, "middle")),
         dict(k="pt", at="stjohns", c="INK_W", t="ニューファンドランド", lab=(-18, -24, "end"))]]),
        t="ROVの空輸", s="バッファローからニューファンドランドへ（現在の衛星写真）"),
    # c515（2行）＝1行目でフランスの調査船（「大西洋の中ほどから」＝向きだけの矢印）・2行目でバッファローの ROV を積んだ船と現場にそろう（6月22日）
    "c515": dict(**ss.sat("G04", note="×は最後に受けた位置・矢印は「大西洋の中ほどから」の向きだけ・港は一般の座標", steps=[
        [dict(k="arrow", fr=(42.68, -32.35), to="site", dir=True, src="USCG p.42〈34〉（`responded from mid-ocean`）",
              c="INK_W", t="フランスの調査船", lab=(0, -30, "middle")),
         dict(k="x", at="site")],
        [dict(k="line", path=("stjohns", "site"), c="INK_W", dash=True, t="ROV を積んだ船", lab=(-24, 0, "end")),
         dict(k="txt", at="site", t="6月22日にそろう", lab=(0, 56, "middle"))]]),
        t="2つのROV", s="北大西洋（現在の衛星写真）"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-15）：図解 第4章（10カット）＝模式図 `tools/mech22.py`・時間の帯（axis）・棒（qty）
# ══════════════════════════════════════════════════════════
#   🔴 色は役の色（母船＝水色・会社＝橙・潜水艇＝白・米沿岸警備隊＝青・カナダ＝紫）。章の札「96時間」と同じ並びを見出し・副題に入れない（門番 dup）。
#      段の数＝語りの行の数。帯の past で沈めるだけの点は札なし（`t="", lab=False`）
#   🔧 c518：映像方針の「帯」（6/18 08:24→6/22）→ **棒**（生命維持を始めてからの時間＝酸素の目安 96 と見つかるまで 98時間16分）＝4日にまたがる時刻の帯では
#      2時間16分の差が読めない・語りは2つの長さの比べ（目盛りは24時間ごと）
_N_PM = "時刻はカナダの報告書（電話が切れた時刻は米沿岸警備隊の報告書の船長の陳述）"
_PM_PAST = [ss.ax("lost47", t="", lab=False), ss.ax("surf15", t="", lab=False)]
SPEC.update({
    # c501（3行）＝聞き役の問い→会社の担当はまず通信の装置を疑う→母船の文の印（1分に2〜3回）・潜水艇の段は返事なし
    "c501": dict(
        t="すぐには呼ばない", s="母船の画面から送った文",
        fig=("m22", dict(view="send", steps=[dict(), dict(tag=dict(t="まず通信の装置を疑う", at="doubt", col=J.COMPANY)),
                                             dict(state=dict(send="on", none="on"))],
                         note="印の数と間隔は模式（記録は1分に2〜3回の文＝米運輸安全委員会の報告書）", src=ss.src(["NTSB p1017", "USCG p39"]))),
    ),
    # c502（3行）＝会社の手順（待つ→3時間 海面を探す→外へ）→「事情によっては縮めてよい」
    "c502": dict(
        t="待ってから探す", s="途絶えたときの決まり",
        fig=("m22", dict(view="proto", steps=[dict(state=dict(wait="on")), dict(state=dict(search="on", out="on"), tag=dict(t="3時間", at="t3")),
                                              dict(tag=dict(t="事情によっては短く", at="cut", col=J.COMPANY))],
                         rel=[dict(t="3時間", src="USCG p39")],
                         note="流れは会社の手順の要点（模式）", src=ss.src(["USCG p39", "TSB §1.3.3"]))),
    ),
    # c503（2行）＝時間の帯（10:47ごろ 途絶→15:00 浮上の見込み→15:00〜18:00 海面の捜索）
    "c503": dict(
        t="午後3時", s="浮かんでこない艇",
        fig=("axis", dict(ss.AX_PM22, past=[ss.ax("lost47")], start=dict(cur="10:47"),
                          steps=[dict(add=[ss.ax("surf15")], cur="15:00"), dict(add=[ss.ax("srch")])],
                          note=_N_PM, src=ss.src(["TSB §1.3.3", "USCG p38"]))),
    ),
    # c504（2行）＝同じ帯。16:34 船長が陸の班へ電話→18:00 手がかりなし
    "c504": dict(
        t="陸への電話", s="母船の船長の動き",
        fig=("axis", dict(ss.AX_PM22, past=_PM_PAST + [ss.ax("srch")], start=dict(cur="15:00"),
                          steps=[dict(add=[ss.ax("call1634")], cur="16:34"), dict(add=[ss.ax("none18")], cur="18:00")],
                          note=_N_PM, src=ss.src(["TSB §1.3.3"]))),
    ),
    # c505（2行）＝同じ帯。18:27 救難調整センターへの電話がすぐ切れる（船長の陳述）→18:55 の電話からボストンへ
    "c505": dict(
        t="ボストンへ", s="救難調整センターへの電話",
        fig=("axis", dict(ss.AX_PM22, past=_PM_PAST + [ss.ax("srch", t=""), ss.ax("call1634", t="", lab=False), ss.ax("none18", t="", lab=False)],
                          start=dict(cur="18:00"),
                          steps=[dict(add=[ss.ax("cut1827")], cur="18:27"), dict(add=[ss.ax("rcc1855")], cur="18:55")],
                          note=_N_PM, src=ss.src(["USCG p39", "TSB §1.3.3"]))),
    ),
    # c506（2行）＝同じ帯。10:47ごろ から 18:55 までの括弧「8時間8分」（カナダの調べ）→聞き役の問い
    "c506": dict(
        t="長い待ち", s="途絶えてから外に知らせるまで",
        #   ⚠️ geom_gap：15:00 の点の縦の線が括弧の札「8時間8分」（括弧の真ん中＝14:51 のあたり）を貫いた＝15:00 の点は沈めない
        fig=("axis", dict(ss.AX_PM22, past=[ss.ax("srch", t=""), ss.ax("call1634", t="", lab=False),
                                            ss.ax("none18", t="", lab=False), ss.ax("cut1827", t="", lab=False)],
                          start=dict(cur="18:27"),
                          steps=[dict(add=[ss.ax("lost47"), ss.ax("rcc1855"), ss.ax("b88")], cur="18:55"), dict()],
                          note="時刻と長さはカナダの報告書（途絶の時刻は米沿岸警備隊の報告書）", src=ss.src(["TSB §2.5", "TSB §1.3.3", "USCG p38"]))),
    ),
    # c507（3行）＝同じ手順＋「見えたのは通信の途絶」→ 海の上のならい（できるだけ早く救難の当局へ）→ 沿っていない（カナダ）
    "c507": dict(
        t="沿わない手順", s="初めの見立て",
        fig=("m22", dict(view="proto", start=dict(wait="on", search="on", out="on"),
                         steps=[dict(tag=dict(t="見えたのは通信の途絶", at="look")), dict(state=dict(best="on")),
                                dict(tag=dict(t="沿っていない", d="カナダの調べ", at="bad", col=J.INST))],
                         note="流れは要点（模式）", src=ss.src(["TSB §2.5", "TSB §2.6"]))),
    ),
    # c518（3行）＝🔧 棒（生命維持を始めてからの時間）。酸素の目安 96時間（潜水艇）→見つかるまで 98時間16分（カナダの調べ）→聞き役
    "c518": dict(
        t="過ぎた目安", s="見つかったとき",
        fig=("qty", dict(view="bar", groups=[ss.QG["o2"]],
                         steps=[dict(add=[ss.qb("o2_lim")]), dict(add=[ss.qb("o2_find")]), dict()],
                         note="酸素の目安は乗っていた人数のときの値（カナダの報告書）", src=ss.src(["TSB §1.2.1", "TSB §2.5"]))),
    ),
    # c520（3行）＝横から見たタイタン。ハッチは無い（前のドームのボルト）→台に戻して外からボルトを外す→聞き役
    "c520": dict(
        t="出られない艇", s="前のドーム",
        fig=("m22", dict(view="side", steps=[dict(state=dict(bolts="on"), tag=dict(t="ハッチは無い", at="tag")),
                                             dict(state=dict(only="on"), tag=dict(t="台に戻して外から開ける", at="only")), dict()],   # ⚠️ 門番 echo：「台に戻し外からボルトを外す」は語りの写し
                         note="形は NTSB 図3 の比（模式）", src=ss.src(["TSB §2.5", "TSB §脚注39"]))),
    ),
    # c521（2行）＝救助の備えの2つの欄が空（水の中の位置を知る手段・ROV の会社との救助の契約）
    "c521": dict(
        t="無かった備え", s="捜索と救助の前に",
        fig=("m22", dict(view="none", start=dict(set="rescue"), steps=[dict(state=dict(n="1")), dict(state=dict(n="2"))],
                         note="欄は要点（模式）", src=ss.src(["TSB §2.5"]))),
    ),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-15）：写真・映像 第4章（11カット）＝映像方針の一覧（了承②）。副題は焼いた絵を原寸で見てから最終に
# ══════════════════════════════════════════════════════════
#   映像＝`ss.vid`（区間と倍率は list22.tsv＝narration.json の実測・USE は `qa_out/ep22_assets.py use` が書く）。
#   DVIDS は全面（side="none"）・ROV は第三者＝額装・等速・無加工（color=1.0）。写真は全面＝`ss.mv`（PLAN の「動き」）
_HANGAR = P("dvids7875471_hc130_hangar")
_COCKPIT = P("dvids7875444_hc130_cockpit")
_SEA = P("dvids7875448_sea_from_aircraft")
SPEC.update({
    # c508（9.9秒）＝聞き役の反応つき。DVIDS 887734 の 54.2〜66.6秒（指令センターの席）
    "c508": ss.vid("c508", side="none", t="遭難の扱い", s="米沿岸警備隊の指令センター（6月20日）"),
    # c509（6.8秒）＝米沿岸警備隊の HC-130（格納庫の写真＝飛ぶ所ではない＝副題に日時を書かない）・右へ
    "c509": dict(photo=_HANGAR, **ss.mv(_HANGAR, "r"), side="none", t="空からの捜索", s="捜索に加わった米沿岸警備隊の輸送機"),
    # c510（7.8秒）＝操縦席（背中だけ・顔は写らない）・上へ
    "c510": dict(photo=_COCKPIT, **ss.mv(_COCKPIT, "u"), side="none", t="探した海の広さ", s="捜索中の米沿岸警備隊の輸送機の操縦席（6月21日）"),
    # c511（8.3秒）＝機内から見た海（幅 1600）・右へ
    "c511": dict(photo=_SEA, **ss.mv(_SEA, "r"), side="none", t="叩く音の話", s="捜索の機内から見た海（6月21日）"),
    # c512（9.4秒）＝聞き役の問い＋答え。DVIDS 887852 の 493.5〜501.0秒（第1管区の担当の大佐）
    "c512": ss.vid("c512", side="none", t="爆縮の時刻", s="6月21日の記者会見（米沿岸警備隊）"),
    # c513（10.8秒）＝聞き役の問い＋答え。DVIDS 887597 の 535.0〜547.5秒（司令官の寄り）
    "c513": ss.vid("c513", side="none", t="壊れた探査機", s="6月19日の記者会見（米沿岸警備隊）"),
    # c516（5.6秒）＝DVIDS 888011 の 136.0〜142.2秒（隊員が機体へ歩く・後ろ姿）
    "c516": ss.vid("c516", side="none", t="急いだ支度", s="捜索に向かう米空軍州兵の隊員（6月21日）"),
    # c517（9.2秒）＝ROV 04 の 18.52〜28.61秒（尾部に近づく）・等速
    "c517": ss.vid("c517", color=1.0, t="発見の時刻", s="近づいて見た尾部（6月22日）"),
    # c519（8.9秒）＝DVIDS 888022 の 468.0〜477.5秒（米海軍の引き揚げの担当が身ぶりで話す）
    "c519": ss.vid("c519", side="none", t="変わらない結果", s="6月22日の記者会見（米海軍の担当者）"),
    # c522（6.9秒）＝ROV 07 の 2.0〜9.72秒（散らばった破片 → 遠くに前のドーム）・等速
    "c522": ss.vid("c522", color=1.0, t="指針どおりなら", s="散らばった破片と前のドーム（6月22日）"),
    # c523（4.9秒）＝ROV 07 の 54.25〜60.0秒（後ろのドーム）・等速 → 第5章の扉
    "c523": ss.vid("c523", color=1.0, t="最初の問い", s="後ろのドームのまわりの残骸（6月22日）"),
})
