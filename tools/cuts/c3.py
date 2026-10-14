# -*- coding: utf-8 -*-
"""第2章　6月18日の朝 c301–c319（19カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c3.py`）。
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
    'c301': dict(kind='写真',
               plan='M03｜見せ方：全面｜副題：母船ポーラープリンス（事故の後の6月25日に撮影）｜動き：右へ｜権利：A（MBI＝米沿岸警備隊が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図3｜注：幅1202＝全面は1.6倍の引き伸ばし（ボケは差し替えの理由にしない）｜台本の画：実写 MBI 図3 ポーラープリンス（セントジョンズの岸壁・USCG 報告 p.14・2023-06-25 に MBI が撮影＝事故の後・A・幅1202＝寄り弱め＝副題「母船ポーラープリンス（事故の後の6月25日に撮影）」）',
               src='TSB §1.2.2（`The Polar Prince (Figure 4) is a Canadian-flagged general cargo vessel.`）・TSB §1.1（`“Year built” refers to the date the keel of the vessel was laid`）・NTSB p.14（`the 220-foot-long, Canadian-flagged vessel Polar Prince`）'),
    'c302': dict(kind='図解',
               plan='台本の画：図 棒 乗客の数（貨物船の決まりの上限12人／この航海24人＝カナダの調べの数）',
               src='TSB §1.20.1.2（`it was permitted to carry up to 12 passengers.`）・§1.20.1.2（`on the occurrence voyage, it was carrying 24 passengers.`）'),
    'c303': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3 人の数）｜新しい画（映像方針）：図 模式 人の図（会社の関係24＝橙・乗組員17＝水色の人の印で並べ、乗客に数える24を枠で囲む）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 乗っていた人の内わけ（TSB §1.3.1 の数＝会社の関係24・乗組員17）',
               src='TSB §1.20.1.1（`OceanGate passengers, who consisted of the Titan passengers and their family members.`）・TSB §1.3.1（`There were 41 people on board the Polar Prince in total: 24 people associated with OceanGate and 17 Polar Prince crew members.`）'),
    'c304': dict(kind='図解',
               plan='🔧 G02｜注：🔧 自作の地図→衛星写真（了承②）｜新しい画（映像方針）：図 地図 衛星写真 G02＋c219 と同じ線・「6月16日に出る」「6月18日に着く」の札・母船が台を引く線｜台本の画（🔧映像方針で替えた＝元の予定）：図 地図 セントジョンズから現場まで（6月16日に出る・6月18日に着く・約685km＝c219 と同じ地図の続き＝母船が台を引く線）',
               src='TSB §1.3.1（`the Polar Prince departed St. John’s, Newfoundland and Labrador, for the Titanic wreck site (Figure 5) towing the Titan on the LARS.`）'),
    'c305': dict(kind='写真',
               plan='M05｜見せ方：全面｜副題：潜水艇を出し入れする台（事故の後に撮影）｜動き：寄る｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図5｜台本の画：実写 MBI 図5 台（LARS）が岸壁に（白い浮き・USCG 報告 p.16・2023-06-25 撮影・A＝副題「潜水艇を出し入れする台（事故の後に撮影）」）',
               src='TSB §1.2.1.1（`During launching, the tanks could be flooded with water in order to submerge the LARS and allow the Titan to detach underwater.`）'),
    'c306': dict(kind='図解',
               plan='台本の画：図 帯 6月18日の朝の時刻の帯（左下に「時刻はニューファンドランドの夏時間」）',
               src='TSB 脚注13（`All times are Newfoundland Daylight Time (Coordinated Universal Time minus 2.5 hours).`）・TSB §1.3.1（`arrived with the Titan in tow on the LARS at 0400 on 18 June`）'),
    'c307': dict(kind='写真',
               plan='M18｜見せ方：額装（報告書の図）｜副題：母船の航海日誌（6月18日の早朝）｜動き：額ごと右へ（細長い頁を左から右へ）｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図18｜注：1099×246 の細長い書類の頁（黒い塗りは MBI）｜台本の画：実写 MBI 図18 航海日誌 6/18 00:00〜06:00（黒い塗りは MBI の物・額装・USCG 報告 p.23・A＝副題「母船の航海日誌（6月18日の早朝）」）',
               src='TSB §1.3.1（`At 0534, OceanGate held a briefing that provided an overview of the plan for the upcoming dive.`）・TSB §1.3（`the Titan’s pilot, who was OceanGate’s chief executive officer (CEO); the copilot, who was an expert on deep-sea exploration and the Titanic; and 3 passengers`）'),
    'c308': dict(kind='写真',
               plan='M21｜見せ方：額装（報告書の図）｜副題：説明が行われた母船の格納庫（事故の後に撮影）｜動き：額ごと左へ｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図21｜注：2枚組・黄の丸は MBI・幅776｜台本の画：実写 MBI 図21 母船のヘリの格納庫と、中に並ぶ椅子（USCG 報告 p.25・2023-06-25 撮影・A・小さい＝額装＝副題「説明が行われた母船の格納庫（事故の後に撮影）」）',
               src='TSB §1.3.1（`At 0545, the 5 people boarding the Titan and their personal effects were weighed so that OceanGate could calculate the weight needed for the submersible to descend.`）'),
    'c309': dict(kind='写真',
               plan='M24｜見せ方：額装（報告書の図）｜副題：母船の小舟（事故の後に撮影）｜動き：額ごと寄る｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図24｜注：黄の丸は MBI・幅780｜台本の画：実写 MBI 図24 母船の小舟2隻（USCG 報告 p.27・2023-06-23 撮影・A＝副題「母船の小舟（事故の後に撮影）」）',
               src='TSB §1.3.1（`From 0600 to 0800, OceanGate used rigid inflatable boats (RIBs) to transfer the Titan pilot, copilot, and other OceanGate personnel to the LARS`）・§1.3.1（`At approximately 0800, the 3 passengers were transferred from the Polar Prince to the LARS.`）'),
    'c310': dict(kind='図解',
               plan='見る向き：上から｜台本の画：図 線 上から見た台と艇（NTSB 図4 の上の線画をなぞる・出どころの注なし＝NTSB）',
               src='TSB §1.3.1（`All 5 people were on board the Titan by 0820.`）・§1.3.1（`At 0824, OceanGate personnel on the LARS closed the Titan’s forward dome, bolted it shut, and used a torque wrench to tighten the bolts.`）'),
    'c311': dict(kind='図解',
               plan='見る向き：横から｜合図：🔁 上から→横から（前の図 c310）＝左上に見る向きの札・替わる瞬間に「横から見ると」｜台本の画：図 線 タイタンの横の線画（前のドームの縁に、外から留めるボルトの札）',
               src='TSB §1.2.1（`The forward dome could be bolted and unbolted from outside the submersible to provide access to the cabin; this was the only way that people could enter and exit the submersible.`）・TSB §2.5（`could not egress on the surface without the Titan first being reattached to the LARS and the forward dome being unbolted by people outside the submersible`）'),
    'c312': dict(kind='図解',
               plan='台本の画：図 帯 同じ時刻の帯（08:24 に「艇の中の生命維持へ」の札）',
               src='TSB §1.3.1（`At this point, the Titan crew and passengers were sealed inside the cabin, and the submersible was using its internal life support system.`）・TSB §1.2.1（`The cabin had an internal life support system that consisted of oxygen tanks`）・§1.2.1（`CO2 scrubbing capability for the same occupancy`）'),
    'c313': dict(kind='図解',
               plan='台本の画：図 帯 同じ帯（08:59 5分の一時停止）',
               src='TSB §1.3.1（`At 0859, all OceanGate personnel took a scheduled 5-minute pause in operations to consider the progress and safety of the operations so far.`）'),
    'c314': dict(kind='図解',
               plan='見る向き：横から｜台本の画：図 模式 台が沈む3段（水を入れる→台ごと水面の下→艇を切り離す）',
               src='TSB §1.3.1（`At 0904, OceanGate divers began to fill the LARS’s ballast tanks with water to submerge it.`）・§1.3.1（`By 0905, the LARS and the Titan were submerged.`）・§1.3.1（`At 0914, divers detached the Titan from the LARS, and the Titan began its descent.`）'),
    'c315': dict(kind='図解',
               plan='見る向き：横から｜台本の画：図 模式 重りで沈む潜水艇（線画・下向きの矢印だけ）',
               src="USCG p.6〈vi〉（`The descent was a free fall through the water column, controlled by the vessel's ballast condition.`）・TSB §1.3（`The occurrence dive on 18 June was the Titan’s first dive to the Titanic`）・NTSB p.16（`It was the first dive of the 2023 expedition to descend below 33 feet (10 meters).`）"),
    'c316': dict(kind='図解',
               plan='台本の画：図 模式 音で文字を送る（母船の下の送受信機と艇のあいだに音の波・電波は水を通りにくいの札）',
               src='USCG p.32〈24〉（`Since radio waves do not travel well through water, these modems rely on acoustics to send and receive information`）・p.30〈22〉（`The installed system used abbreviated text fields to communicate between the POLAR PRINCE and the TITAN.`）・p.30〈22〉（`The TITAN was not fitted with a voice communications system capable of communicating while the submersible was operating below the surface.`）'),
    'c317': dict(kind='図解',
               plan='🔧 注：🔧 再現→吹き出し（§0-3 交信の記録＝4つは吹き出しで残す）｜新しい画（映像方針）：図 吹き出し 付録A の最初の4行（潜水艇の文＝左の白の吹き出し・母船の文＝右の水色の吹き出し・打ち間違いのまま `I hsvr trscking` ほか・訳は字幕）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 付録A の表の最初の4行（09:19:36〜09:20:02・打ち間違いのまま＝`I hsvr trscking`・`descendingb thru 235`・`i have tracking`・`yeah`・訳は字幕）',
               src='TSB 付録A（`I hsvr trscking`）・付録A（`descendingb thru 235`）・TSB §1.3.2（`The Titan crew then transmitted a message stating that they were descending through 235 m.`）・TSB §1.3.2（`The surface support team sent a message back stating that they had tracking of the submersible.`）・USCG p.32〈24〉（`the POLAR PRINCE communicated to the TITAN that they have tracking`）'),
    'c318': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 2つの通信の箱（文字を送る装置＝動く・水色／予備の通信と追跡の装置＝灰に「動いていない」の赤の札）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 付録A の表（09:23:03〜09:24:05 の3行＝`no atm are you on`・`atm is on`・`do not read you on atm`）',
               src='TSB §1.3.2（`At 0923, the surface support team received a message from the Titan crew stating that the 2nd acoustic communication and tracking system was not functioning.`）・TSB 脚注16（`It is not known why this system was not functioning.`）'),
    'c319': dict(kind='図解',
               plan='台本の画：図 線 深さの線（記録の点だけ＝9:19 235m・9:23 436m・9:31 680m・あいだは直線＝模式と左下で断る）',
               src='TSB §1.3.2（`they could see the Titan descending at 33 m per minute on their display`）・§1.3.2（`At 0953, the surface support team asked the Titan crew if they could see the Polar Prince on their display. The surface support team kept sending this message until 1010 without receiving a response.`）'),
}

SPEC = {}
