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

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-10-15）：図解 第8章（16カット）＝模式図 `tools/mech22.py`・時間の帯（axis）・棒（qty）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「2つ目の船体」と4字以上同じ並びを見出し・副題に入れない（門番 dup）。字は12字未満（門番 echo）。写真7（c904・c906・c909・c911・c913・
#      c914・c916）は ⑤b-7
_N_CD = "要点の箱（模式）"
SPEC.update({
    # c901（3行）＝聞き役の問い→2020年の初め、別の会社に代わりの筒を頼む→材料は樹脂を含ませたテープに（2つ目の箱）
    "c901": dict(
        t="代わりの筒", s="作り手を替える",          # ⚠️ 門番 echo：「2020年の初め」は語りの写し
        fig=("m22", dict(view="cards", start=dict(set="wind2", n="1"),
                         steps=[dict(), dict(tag=dict(t="別の会社へ頼む", at="t")), dict(state=dict(n="2"))],
                         note="作り方の絵は模式（カナダの報告書・米運輸安全委員会の報告書）", src=ss.src(["TSB §1.12.2", "NTSB p1027"]))),
    ),
    # c902（2行）＝1つ目の糸（三菱ケミカル系）・2つ目のテープ（東レの米国の会社＝品名は出さない）→「期限切れの安い材料」の話は3冊に無い（×）
    "c902": dict(
        t="材料の出どころ", s="2つの筒の材料",
        fig=("m22", dict(view="cards", start=dict(set="mat"), steps=[dict(state=dict(n="2")), dict(state=dict(n="3"))],
                         note=_N_CD + "・会社の名は米沿岸警備隊の報告書の記述", src=ss.src(["USCG p118", "USCG p174"]))),
    ),
    # c903（3行）＝聞き役の問い→2020年の3分の1の模型2つ（1つ目＝壊れた・2つ目＝壊れると分かって試験を止めた）→どちらもタイタニックの深さの手前
    "c903": dict(
        t="模型の結果", s="新しい材料で",          # ⚠️ 門番 echo：「2020年の試験」は語りの写し
        fig=("m22", dict(view="cards", start=dict(set="m20"),
                         steps=[dict(), dict(state=dict(n="2")), dict(tag=dict(t="どちらも届かず", d="タイタニックの深さ", at="t"))],
                         note="形は模式・深さの数は描いていない（米運輸安全委員会の報告書）", src=ss.src(["NTSB p1027", "NTSB p1062"]))),
    ),
    # c905（2行）＝5つの層に分け、1層ずつ固めて重ねる（巻く→固める→接着剤の膜→次の層・5回）→1層は硬化の前に約2.5センチまで（うねりを減らす）
    "c905": dict(
        t="1層ずつ固める", s="5つに分けて",
        fig=("m22", dict(view="cards", start=dict(set="cure"),
                         steps=[dict(state=dict(n="4", loop="on")), dict(tag=dict(t="1層は約2.5センチまで", at="tl"))],
                         rel=[dict(t="1層・約2.5センチ", src="TSB §1.12.2（the layers were limited to 25.4 mm in thickness before curing）")],
                         note="流れは模式（カナダの報告書の記述）", src=ss.src(["TSB §1.12.2", "TSB §脚注50"]))),
    ),
    # c907（2行）＝同じ流れ。作り手が強く求めた（カナダの調べ）→会社は費用で一度断り、作り手が費用を持った
    "c907": dict(
        t="作り手の求め", s="費用の持ち方",
        fig=("m22", dict(view="cards", start=dict(set="cure", n="4", loop="on"),
                         steps=[dict(tag=dict(t="作り手が強く求めた", d="カナダの調べ", at="tl", col=J.INST)),
                                dict(tag=dict(t="費用は作り手が持つ", d="会社は一度断った", at="t", col=J.INK_W))],
                         note="流れは模式（カナダの報告書の記述）", src=ss.src(["TSB §1.12.2"]))),
    ),
    # c908（3行）＝年表（2020〜21年）。2020年11月〜2021年1月 実物大の筒を作る→新しい作り方の模型なし→聞き役
    "c908": dict(
        t="本物を先に", s="模型を飛ばして",
        #   🔧 試し焼き：cur を書かないと今の位置の赤い▼が帯の左の端（2020年6月）に出た
        fig=("axis", dict(ss.AX_Y20, steps=[dict(add=[ss.ax("build20")], cur="2020-11"), dict(add=[ss.ax("nomodel")], cur="2021-01"), dict()],
                          note="月は米運輸安全委員会の報告書（月までの記録）", src=ss.src(["NTSB p1028", "NTSB p1062"]))),
    ),
    # c910（2行）＝筒の壁の断面に層ごとの「削ったしわ」の数（1・8・14・24＝事故のあとに端材で数えた）→どこまで削ったかの記録は無い
    "c910": dict(
        t="しわを削った数", s="層ごとに数える",
        fig=("m22", dict(view="layers", steps=[dict(state=dict(grind="on")), dict(tag=dict(t="削った範囲は記録なし", at="t"))],
                         note="数は事故のあとに端材で数えた値（米沿岸警備隊の報告書 図143）・印の並びは模式", src=ss.src(["USCG p180", "TSB §2.1"]))),
    ),
    # c912（2行）＝思ったより厚い端（約13.1センチ）→チタンの輪の溝（5インチ）に入らず、外側を削って入れた
    "c912": dict(
        t="溝に入らない", s="厚すぎた筒",
        fig=("m22", dict(view="groove", steps=[dict(state=dict(thick="on"), tag=dict(t="端材 約13.1センチ", at="w")),
                                               dict(state=dict(cut="on"), tag=dict(t="外側を削った", at="cut", col=J.ALERT))],
                         rel=[dict(t="約13.1センチ", src="NTSB p1043（5.166インチ）")],
                         note="幅は縮尺どおり・層と泡の穴は模式（米運輸安全委員会の報告書）", src=ss.src(["NTSB p1043"]))),
    ),
    # c915（1行）＝カナダの研究所が端材を18の試料に（長さの向き9・周りの向き9）
    "c915": dict(
        t="18の試料", s="カナダの研究所",
        fig=("m22", dict(view="coupons", steps=[dict(state=dict(cut="on"), tag=[dict(t="長さの向き 9", at="a", col=J.INST),
                                                                             dict(t="周りの向き 9", at="c", col=J.INST)])],
                         rel=[dict(t="9", src="TSB §1.15")],
                         note="切り方の並びは模式（数はカナダの報告書）", src=ss.src(["TSB §1.14", "TSB §1.15"]))),
    ),
    # c917（3行）＝棒（安全率）。会社の基準 1.25（国際規格に合わせた）→長さの向き 3.05→周りの向き 1.11（届かない＝赤）
    "c917": dict(
        t="試料の計算", s="基準に届かず",
        fig=("qty", dict(view="bar", groups=[ss.QG["sf2"]],
                         steps=[dict(add=[ss.qb("sf2_req")]), dict(add=[ss.qb("sf2_ax")]), dict(add=[ss.qb("sf2_ci")])],
                         note="基準は国際標準化機構に合わせた値・計算はカナダの研究所", src=ss.src(["TSB §1.12.2", "TSB §1.15"]))),
    ),
    # c918（3行）＝聞き役の問い→いつも100キロを載せる棚＝基準なら125キロまで→この筒の周りの向き＝111キロまで（余裕は半分も無い）
    "c918": dict(
        t="棚のたとえ", s="余裕の大きさ",
        fig=("m22", dict(view="shelf", steps=[dict(), dict(state=dict(load="on", std="on")), dict(state=dict(tube="on", spare="on"))],
                         note="たとえ（模式）＝重さは安全率の比で計算", src=ss.src(["TSB §1.12.2", "TSB §1.15"]))),
    ),
    # c919（2行）＝カナダの報告書の一節（前提＝試料が実物を代表するなら→結論＝くり返しさらされるのは安全ではなかった）
    "c919": dict(
        t="結論の一節", s="試料が代表なら",
        fig=("m22", dict(view="paper", start=dict(doc="tsb115"), steps=[dict(state=dict(hl1="on", hl2="on")), dict(state=dict(hl3="on", hl4="on"))],
                         note="一節はカナダの報告書（英字のまま・模式）", src=ss.src(["TSB §1.15"]))),
    ),
    # c920（3行）＝米運輸安全委員会が試した試料でカナダの研究所が計算→いちばん強い試料＝耐えた見込み→いちばん弱い試料＝寿命の82%超を使った可能性
    "c920": dict(
        t="くり返しの寿命", s="試料しだいで",
        fig=("m22", dict(view="cards", start=dict(set="life"),
                         steps=[dict(tag=dict(t="米運輸安全委の試料で", d="カナダの研究所の計算", at="t", col=J.INST)),
                                dict(state=dict(n="1")), dict(state=dict(n="2"))],
                         rel=[dict(t="82%", src="TSB §1.16")],
                         note="寿命の目盛りは模式（82%はカナダの報告書）", src=ss.src(["TSB §1.16"]))),
    ),
    # c921（3行）＝🔧 帯→深さの物差し（0〜4,500m・縮尺どおり）。2021年2〜3月の加圧の試験4回→最も深い 4,200m→タイタニックの深さを少し上回るだけ
    "c921": dict(
        t="加圧の試験", s="2021年の2月と3月",
        fig=("m22", dict(view="ruler", start=dict(z="mid"),
                         #   🔧 試し焼き：「4,200メートル」の札が物差しの約2,500mの高さに並んだ＝数は線の札（mech22 の RL_M）に・札は言葉だけ
                         steps=[dict(tag=dict(t="4回の加圧", at="r1")), dict(state=dict(test="on"), tag=dict(t="4回とも通った", at="r2")),
                                dict(tag=dict(t="少し上回るだけ", at="r3"))],
                         rel=[dict(t="4回", src="TSB §1.12.2"), dict(t="4,200メートル", src="NTSB p1030")],
                         note="深さは縮尺どおり（タイタニックは約3,800メートル）", src=ss.src(["TSB §1.12.2", "NTSB p1030", "NTSB p1058", "TSB §1.3"]))),
    ),
    # c922（3行）＝聞き役→何回くり返せば壊れるかは分からない（？）→会社は「音の監視でその場で分かる」と答えた
    "c922": dict(
        t="2つの道", s="計算の代わりに",
        fig=("m22", dict(view="cards", start=dict(set="path"),
                         steps=[dict(), dict(state=dict(n="1")), dict(state=dict(n="2"), tag=dict(t="会社の答え", at="t", col=J.COMPANY))],
                         note=_N_CD + "・カナダの報告書の記述", src=ss.src(["TSB §1.12.2", "TSB §2.1"]))),
    ),
    # c923（3行）＝🔧 模式→深さの物差し（0〜4,500m）。最初の窓の等級 約650m（米沿岸警備隊・カナダ）→1,000m（米運輸安全委員会）→事故のときの窓は見方が割れる
    "c923": dict(
        t="前の窓", s="値が割れる",
        fig=("m22", dict(view="ruler", start=dict(z="mid"),
                         #   🔧 試し焼き：数の札が物差しの別の深さの高さに並んだ＝数は線の札（RL_M）に・札は調べの名だけ（色は線と同じ）
                         steps=[dict(state=dict(w650="on"), tag=dict(t="米沿岸警備隊・カナダ", at="r1", col=J.USCG)),
                                dict(state=dict(w1k="on"), tag=dict(t="米運輸安全委員会", at="r2", col=J.OK)),
                                dict(tag=dict(t="事故のときの窓は？", at="r3"))],
                         rel=[dict(t="約650メートル", src="USCG p278・TSB §1.12.1（649.08 m）"), dict(t="1,000メートル", src="NTSB p1030")],
                         note="深さは縮尺どおり（タイタニックは約3,800メートル）", src=ss.src(["USCG p278", "NTSB p1030", "TSB §1.12.1", "TSB §1.12.2"]))),
    ),
})
