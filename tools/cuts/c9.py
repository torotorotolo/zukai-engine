# -*- coding: utf-8 -*-
"""第8章　2つ目の船体 c901–c923（23カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c9.py`）。
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
    'c901': dict(kind='図解',
               plan='🔧 注：🔧 実写→模式（NTSB 図18 の右＝模型の端は語り「代わりの筒を頼んだ・テープに変えた」と合わない → c904 へ）｜新しい画（映像方針）：図 模式 2つの巻き方の並べ図（1つ目＝樹脂の槽をくぐらせた糸・橙／2つ目＝樹脂をあらかじめ含ませたテープ・青）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 NTSB 図18 の右＝1/3 模型の切り落とした端のしわと剥離（NTSB 研究所・A・c803 は同じ図の左＝別の写真＝副題「3分の1の模型の端（研究所）」）',
               src='TSB §1.12.2（`In early 2020, OceanGate engaged a new company, Electroimpact Inc., to construct a replacement carbon-fibre cylinder.`）・TSB §1.12.2（`The layers were made using a unidirectional carbon fibre tape that was pre-impregnated with epoxy resin`）'),
    'c902': dict(kind='図解',
               plan='台本の画：図 再現 材料の発注の要点（2020年・東レのアメリカの会社・テープの品名は出さない）',
               src='USCG p.118〈110〉（`The carbon fiber material used for the first TITAN hull was standard-modulus Grafil 37-800`）・p.174〈166〉（`The specific pre-preg system used was Toray Composite Materials America’s P2362W-19L`）・p.174〈166〉（`On February 21, 2020, OceanGate issued a purchase order for 7,700 lbs of P2362W-190U-013 composite material from Toray Composites`）'),
    'c903': dict(kind='図解',
               plan='台本の画：図 模式 2020年の1/3 模型2つ（1つ目＝壊れた・2つ目＝壊れる寸前で試験を止めた＝米運輸安全委の書き方・深さの数は描かない）',
               src='NTSB p.62（`either imploded or nearly imploded at depths less than 3,000 meters (9,843 feet), significantly less than the depth needed to reach the Titanic wreckage.`）'),
    'c904': dict(kind='写真',
               plan='🔧 N18:右｜見せ方：全面｜副題：3分の1の模型の端に見えるうねり（研究所）｜動き：左へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会の報告書 図18｜注：🔧 模式→実写（NTSB 図18 の右＝v1 の後・v2 の前に作った2つの3分の1の模型＝NTSB p.37／語り「うねり」）。図18 の右を切り出す｜台本の画（🔧映像方針で替えた＝元の予定）：図 模式 層のうねり（まっすぐな繊維と、波打った繊維の並べ図）',
               src='TSB §1.12.2（`identified that ply waviness in localized areas in the carbon fibre cylinder was the cause of each failure.`）・§1.12.2（`Ply waviness reduces the compressive strength and buckling resistance of a laminate composite.`）'),
    'c905': dict(kind='図解',
               plan='台本の画：図 模式 1層ずつ固める作り方（巻く→固める→接着剤の膜→次の層・5回くり返す）',
               src='TSB §1.12.2（`The manufacturing process therefore involved Electroimpact Inc. creating the cylinder in 5 layers, each of which was cured separately.`）・TSB 脚注50（`A multi-cure method allows for the layers of carbon fibre to be thinner, which reduces the probability of ply waviness.`）'),
    'c906': dict(kind='写真',
               plan='M255｜見せ方：額装（報告書の図）｜副題：事故の船体の筒の断面（5つの層）｜動き：額ごと左へ｜権利：A（NTSB の研究所が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図255（米運輸安全委員会）｜注：英字の札と定規＝訳の札を添える（§B1-4）・幅814｜台本の画：実写 MBI 図255 5層の断面（英字の札と定規・NTSB の撮影・USCG 報告 p.276・A・英字の札は §B1-4＝映像方針で＝副題「事故の船体の筒の断面（5つの層）」）',
               src='TSB §1.12.2（`Each layer contained 133 fibre plies.`）・§1.12.2（`The laminate stacking sequence was 2 cylindrical plies first, followed by 1 longitudinal ply.`）'),
    'c907': dict(kind='図解',
               plan='台本の画：図 模式 同じ作り方の図（「作り手が強く求めた」「費用は作り手が持った」の札）',
               src='TSB §1.12.2（`OceanGate initially rejected this recommendation because it would cost more, but Electroimpact Inc. insisted on it and agreed to cover the cost of it.`）'),
    'c908': dict(kind='図解',
               plan='台本の画：図 帯 年表（2020年11月〜2021年1月 実物大の筒・模型は作らず）',
               src='NTSB p.28（`between November 2020 and January 2021.`）・NTSB p.62（`OceanGate did not build or test any new sub-scale models using the co-bonding process`）・p.62（`the only article produced using the co-bonding process was the v2 full-scale cylinder ultimately used in the casualty dive.`）'),
    'c909': dict(kind='写真',
               plan='N16:下｜見せ方：全面｜副題：しわを削った跡（事故の船体の端材）｜動き：右へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会の報告書 図16｜注：NTSB 図16 の下を切り出す｜台本の画：実写 NTSB 図16 の下＝事故の船体の端材のしわの削り跡（研究所・A＝副題「しわを削った跡（事故の船体の端材）」）',
               src='TSB §1.12.2（`The carbon fibre plies in these areas were ground down by OceanGate to make them flush with the rest of the outer surface before the next layer was added.`）・§1.12.2（`Grinding down the carbon fibre severed some of the fibres and introduced defects on the surface.`）・§1.12.2（`Grinding did not mitigate ply waviness below the outer surface of each layer of the cylinder.`）'),
    'c910': dict(kind='図解',
               plan='🔧 注：🔧 札を足した（§0-3＝事故のあとに端材で数えた物）｜新しい画（映像方針）：図 棒 層ごとの「削ったしわ」の数（1・8・14・24＝MBI 図143）・左下の札「事故のあと、端材で数えた」｜台本の画（🔧映像方針で替えた＝元の予定）：図 棒 MBI 図143 の数（層ごとの「削ったしわ」の数＝⑤b で原寸から読む・文字の層に無い）',
               src='TSB §2.1（`The overall extent of the grinding was not documented and therefore could not be determined.`）'),
    'c911': dict(kind='写真',
               plan='N15｜見せ方：全面｜副題：事故の船体の筒の切り落とした端（研究所）｜動き：左へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会の報告書 図15｜台本の画：実写 NTSB 図15 事故の船体の端材の側面（研究所・A＝副題「事故の船体の筒の切り落とした端（研究所）」）',
               src='NTSB p.29（`The cylinder was manufactured with excess material at both ends, which was subsequently trimmed off.`）・NTSB p.42（`We also examined end pieces that had been trimmed from the v2 full-scale cylinder during the construction/production process`）'),
    'c912': dict(kind='図解',
               plan='台本の画：図 模式 筒の厚さ（設計＝約12.7cm〈5インチ〉の溝・端材＝約13.1cm・外側を削って溝に入れた）',
               src='NTSB p.43（`The excess porosity resulted in an increase in layer thickness.`）・p.43（`which could only accommodate a 5-inch-thick cylinder.`）'),
    'c913': dict(kind='写真',
               plan='N17:下｜見せ方：全面｜副題：層のあいだの接着剤のすき間（事故の船体の端材）｜動き：寄る｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会の報告書 図17｜注：NTSB 図17 の下を切り出す｜台本の画：実写 NTSB 図17 の下＝1枚目と2枚目の層のあいだの接着剤の空隙（研究所・A＝副題「層のあいだの接着剤のすき間（事故の船体の端材）」）',
               src='NTSB p.43（`The voids were present in all layers but were significantly greater in size and number at the interface between the first and second layers and the third and fourth layers.`）'),
    'c914': dict(kind='写真',
               plan='N16:上｜見せ方：全面｜副題：しわのまわりのすき間（事故の船体の端材）｜動き：引く｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会の報告書 図16｜注：NTSB 図16 の上を切り出す（c909 と別の写真）｜台本の画：実写 NTSB 図16 の上＝しわのまわりで接着剤がテントのように浮いた空隙（研究所・A＝副題「しわのまわりのすき間（事故の船体の端材）」）',
               src='NTSB p.62（`the co-bonding process did not completely eliminate the wrinkles and, at the same time, introduced additional anomalies.`）'),
    'c915': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 端材を18の試料に切る図（長さの向き9＝青・周りの向き9＝橙）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 TSB の研究所の試験の要点（端材を18の試料に・長さの向き9・周りの向き9）',
               src='TSB §1.14（`The TSB Laboratory was able to obtain a trimmed-off end piece that came from the 2nd construction of Titan’s carbon fibre cylinder`）・TSB §1.15（`The TSB Laboratory cut and machined the end piece into 18 samples, 9 in the axial direction and 9 in the circumferential direction.`）'),
    'c916': dict(kind='写真',
               plan="L28｜見せ方：全面｜副題：端面に見える層のうねり（米運輸安全委員会の研究所）｜動き：右へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図28｜注：c915 がカナダの研究所＝取り違えないよう研究所の名を残す（④'）｜台本の画：実写 24-011 図28 2つ目の筒の切り落とした端面のうねり（黄の目盛り・NTSB 研究所・A＝副題「端面に見える層のうねり（米運輸安全委員会の研究所）」）",
               src='TSB §1.15（`there was a general waviness in the plies.`）'),
    'c917': dict(kind='図解',
               plan='台本の画：図 棒 安全率（長さの向き3.05・周りの向き1.11・必要な1.25 の線＝何メートルでの値かは書かない）',
               src='TSB §1.12.2（`OceanGate also changed its safety factor to 1.25`）・§1.15（`as evidenced by the calculated safety factor of 3.05, which was greater than the required 1.25.`）・§1.15（`the calculated safety factor was 1.11, which did not meet the required safety factor of 1.25.`）'),
    'c918': dict(kind='図解',
               plan='台本の画：図 模式 棚のたとえ（いつも100キロを載せる棚＝基準は125キロまで耐える／この筒の周りの向き＝111キロまで・式は §9）',
               src='—'),
    'c919': dict(kind='図解',
               plan='台本の画：図 再現 TSB §1.15 の一節（前提の「試料が実物を代表するなら」と、結論の文を英字で＋訳は字幕）',
               src='TSB §1.15（`Assuming that the test results from the samples are representative of the properties of the carbon fibre cylinder used in the Titan`）・§1.15（`it was unsafe for the Titan to have been repeatedly exposed to pressures equivalent to the depth of the Titanic or deeper (which occurred during pressure tests).`）'),
    'c920': dict(kind='図解',
               plan='台本の画：図 棒 疲れの寿命（米運輸安全委が試した試料でカナダの研究所が計算、いちばん強い物＝耐えた見込み／いちばん弱い物＝82% を超えて使った可能性）',
               src='TSB §1.16（`would reasonably have been expected to survive based on the sample with the highest compressive strength value`）・§1.16（`it could have used more than 82% of its fatigue life in the time up to the occurrence dive based on the sample with the lowest compressive strength value.`）'),
    'c921': dict(kind='図解',
               plan='台本の画：図 帯 2021年2〜3月の加圧試験4回（4,000m 前後・4,200m は1回・20分＝米沿岸警備隊の書き方・タイタニックの約3,840m の線）',
               src='TSB §1.12.2（`In February and March 2021, the pressure hull was tested at the Deep Ocean Test Facility. Four tests were done.`）・TSB §1.15（`the Titan had 4 successful pressure tests at the Deep Ocean Test Facility`）・NTSB p.58（`marginally greater than the 3,840-meter (12,598-foot) dive depth required to reach the Titanic.`）'),
    'c922': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 2つの道（くり返しの計算＝空欄の「？」／音の監視＝「その場で分かる」と会社）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 TSB §1.12.2・§2.1 の要点（「疲れの計算の代わりに音の監視」「耐えられる回数は分からない」）',
               src='TSB §1.12.2（`the acoustic emission monitoring system would be used to detect damage in real time`）・TSB §2.1（`The number of cycles at extreme pressure that the full-scale pressure hull could withstand was therefore unknown.`）'),
    'c923': dict(kind='図解',
               plan='台本の画：図 模式 前のドームの窓（内側が平ら・外側がふくらんだ形・等級の札＝約650m〈米沿岸警備隊・カナダ〉／1,000m の認証〈米運輸安全委〉）',
               src='USCG p.278〈270〉（`certified the window to a pressure rating of 945 psi, corresponding to a depth of only 650 m (2,133 feet).`）・NTSB p.30（`an acrylic window certified to 1,000 meters (3,281 feet).`）・TSB §1.12.1（`only a fraction of what OceanGate required for dives to the Titanic`）・§1.12.2（`The new viewport from Germany was installed in this construction`）'),
}

SPEC = {}
