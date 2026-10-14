# -*- coding: utf-8 -*-
"""第5章　海の底の残骸 c601–c619（19カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c6.py`）。
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
    'c601': dict(kind='写真',
               plan='R07｜区間 85.0〜94.44秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：海の底の残骸（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：後ろの残骸が左へ去り、前のドームへ近づく（語り「尾部と2つのドームと破片」）｜台本の画：実写 ROV「前のドーム」（NTSB ドケットの Pelagic video 2 of 2・c104・c522 と別の区間・第三者＝引用・額装・焼き込みは残る＝副題「海の底の残骸（6月22日）」）',
               src='NTSB p.20（`including the tail cone and both titanium domes`）・NTSB p.38（`ROVs discovered the wreckage about 330 meters (1,083 feet) east-northeast of the Titanic’s bow.`）・NTSB p.39（`Other pressure vessel fragments, likely from the middle or forward portion of the cylinder, were scattered about the ocean floor.`）'),
    'c602': dict(kind='写真',
               plan='R07｜区間 60.0〜68.23秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：残骸が詰まった後ろのドーム（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜台本の画：実写 ROV「後ろのドーム」（07・c105・c523 と別の区間・第三者＝引用・額装）',
               src='NTSB p.39（`were located together in a comingled mass that included compressed metal, plastic, electronic components, and other materials; the forward dome was located by itself`）'),
    'c603': dict(kind='写真',
               plan='D342｜見せ方：全面｜副題：9月の回収（回収船の甲板）｜動き：下へ｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 9057342）｜注：縦長3024×4032＝全面で上下を切って縦に流す（21本目の型）｜台本の画：実写 DVIDS 9057342 回収船の甲板で破片を調べる隊員（2023-09-30・白い防護服・米沿岸警備隊の撮影・A・縦長＝額装＝副題「9月の回収（回収船の甲板）」）',
               src='TSB §1.6（`The U.S. Coast Guard returned to the site in September 2023 and recovered additional debris. Not all of the debris was recovered.`）'),
    'c604': dict(kind='写真',
               plan='M270｜見せ方：額装（報告書の図）｜副題：前のドームの窓の押さえの輪（FBI 撮影）｜動き：額ごと引く｜権利：A（FBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図270（FBI）｜注：3枚組・赤い丸と矢印・幅556｜台本の画：実写 FBI 図270 前のドームの窓の押さえの輪（ボルトが切れている所に赤い丸と矢印・USCG 報告 p.294・3枚組で小さい＝額装・A＝副題「前のドームの窓の押さえの輪（FBI 撮影）」）',
               src='TSB §1.6（`the retaining ring for the viewport was deformed in a manner that indicated the viewport had blown outward. The viewport was not found.`）・USCG p.293〈285〉（`the viewport was ejected outward during the implosion`）'),
    'c605': dict(kind='写真',
               plan='🔧 L47b｜見せ方：全面｜副題：前のドームの窓の座（研究所）｜動き：寄る｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図47｜注：🔧 紙面の引用→全面（1320×880 の単独の画像）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 24-011 図47 の下（前のドームの窓の座・NTSB 研究所の撮影・A＝紙面の引用の型＝副題「前のドームの窓の座（研究所）」）',
               src='TSB §2.1（`the manner in which the retaining ring was deformed suggested that the viewport had not failed`）・USCG p.280〈272〉（`it is unlikely that the acrylic window itself caused the implosion`）・p.280〈272〉（`the most probable failure mode for the acrylic window would have been inward. In such a scenario, fragments of acrylic would likely have been found in the debris.`）'),
    'c606': dict(kind='写真',
               plan='M159｜見せ方：全面｜副題：前のチタンの輪（FBI 撮影）｜動き：右へ｜権利：A（FBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図159（FBI）｜台本の画：実写 FBI 図159 前部セグメント（青いシートの上・証拠の札・USCG 報告 p.189・A＝副題「前のチタンの輪（FBI 撮影）」）',
               src='TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure`）・USCG p.269〈261〉（`a loss of structural integrity of the carbon fiber or glue joint within the TITAN’s cylindrical pressure hull`）・NTSB p.61（`The postcasualty condition of the Titan pressure vessel was consistent with a local buckling failure.`）'),
    'c607': dict(kind='写真',
               plan='M157｜見せ方：全面｜副題：後ろのチタンの輪（FBI 撮影）｜動き：左へ｜権利：A（FBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図157（FBI）｜台本の画：実写 FBI 図157 後部セグメント（チタンの輪・貫通部・炭素繊維の残り・USCG 報告 p.188・2023-07-05・A＝副題「後ろのチタンの輪（FBI 撮影）」）',
               src='USCG p.292〈284〉（`the adhesive used to bond the hull to the titanium segments had disbonded from the entire forward segment`）'),
    'c608': dict(kind='写真',
               plan='M268｜見せ方：額装（報告書の図）｜副題：後ろの輪に残った接着剤｜動き：額ごと寄る｜権利：A（米沿岸警備隊が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図268｜注：675×841｜台本の画：実写 USCG 図268 後部セグメントに残った接着剤（USCG 報告 p.292・A＝副題「後ろの輪に残った接着剤」）',
               src='USCG p.292〈284〉（`The adhesive was mostly disbonded from the aft segment, except for an approximately 90-degree arc`）・p.293〈285〉（`could be an indicator that the partial separation of the inner layers already existed`）'),
    'c609': dict(kind='写真',
               plan='🔧 R07｜区間 68.24〜74.5秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：残骸が詰まった後ろのドーム（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：🔧 素材を替えた（DVIDS 9057369＝9月の回収のあとに並べた破片 → ROV の海底の映像＝語り「海の底の映像を見ると」）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 DVIDS 9057369 証拠として並べた炭素繊維の破片（9月の回収のあと・米沿岸警備隊・A・🔴 副題に撮影日を書かない・2022年の札を付けない＝副題「回収された炭素繊維の破片」）',
               src='NTSB p.40（`had delaminated into multiple layers nearly around the entire circumference`）'),
    'c610': dict(kind='図解',
               plan='台本の画：図 模式 筒の断面（5枚の層を内側から1〜5・分かれ目＝1と2・3と4のあいだを赤で）',
               src='NTSB p.40（`One delamination was between layers 1 and 2 and the other was between layers 3 and 4.`）・NTSB p.59（`the five 1-inch-thick layers`）'),
    'c611': dict(kind='写真',
               plan='N13｜見せ方：額装（報告書の図）｜副題：回収された破片（研究所で撮影）｜動き：額ごと上へ｜権利：A（NTSB の研究所・出どころの注なし）｜出典の行：米運輸安全委員会の報告書 図13｜注：上下2枚（外面・内面）｜台本の画：実写 NTSB 図13 回収片の外面と内面（NTSB 研究所・A・🔴「海底に残された円筒部」と書かない＝副題「回収された破片（研究所で撮影）」）',
               src='NTSB p.41（`which had been recovered about 350 feet (107 meters) from the main wreckage and measured about 61 inches long by 20 inches wide by 1 inch thick`）・p.41（`indicating that the piece originated from layer 1, the innermost co-bonded layer`）'),
    'c612': dict(kind='写真',
               plan='L15｜見せ方：紙面の引用｜副題：接着剤の面（研究所）｜動き：額ごと右へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図15｜注：頁の画像の中の図・英字の札（§B1-4＝訳の札を添える）｜台本の画：実写 24-011 図15 接着の面（つや消しの擦れた所・光る所・空隙＝英字の札は §B1-4・研究所・A＝紙面の引用の型）',
               src='NTSB p.44（`The adhesive regions were rubbed flat and adhesive wear debris was found collecting in the voids.`）'),
    'c613': dict(kind='写真',
               plan='L22｜見せ方：紙面の引用｜副題：空隙にたまった削り粉（研究所）｜動き：額ごと上へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図22｜注：洗う前と後・🔴 旧版 c627（1つ目の船体の端材）の差し替え｜台本の画：実写 24-011 図22 空隙に詰まった削り粉（洗う前と後・研究所・A＝紙面の引用の型・🔴 旧版 c627 の写真〈1つ目の船体の端材〉の差し替え）',
               src='NTSB p.44（`The rub marks in the adhesive were oriented in the lengthwise direction.`）'),
    'c614': dict(kind='写真',
               plan='L21｜見せ方：紙面の引用｜副題：電子顕微鏡で見たこすれた跡（研究所）｜動き：額ごと寄る｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図21｜台本の画：実写 24-011 図21 電子顕微鏡で見た縦向きのこすれた跡（研究所・A＝紙面の引用の型）',
               src='USCG p.289〈281〉（`could only have been created by the longitudinal independent movement of the carbon fiber layers`）'),
    'c615': dict(kind='図解',
               plan='台本の画：図 模式 2枚の層が別々にずれてこすれる（矢印・断面の拡大）',
               src='NTSB p.59（`indicating that the delamination existed before the implosion`）・NTSB p.44（`had likely failed before the casualty`）'),
    'c616': dict(kind='写真',
               plan='L48｜見せ方：紙面の引用｜副題：4枚目と5枚目の層の破片（研究所）｜動き：額ごと寄る｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図48｜台本の画：実写 24-011 図48 4枚目と5枚目の層の大きな破片（外面・内面・研究所・A）',
               src='NTSB p.59（`The extent of the delamination at the second interface before the implosion could not be determined.`）'),
    'c617': dict(kind='図解',
               plan='台本の画：図 模式 局所座屈（厚い1枚→薄い2枚に分かれる→押されて内へ曲がる）',
               src='NTSB p.61（`Delaminations are a known cause of local buckling failures. The delamination divides a single thicker composite layer into two thinner layers.`）'),
    'c618': dict(kind='写真',
               plan='N14｜見せ方：額装（報告書の図）｜副題：回収された破片の断面（研究所）｜動き：額ごと下へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会の報告書 図14｜注：上下2枚（削った端面・破断面）｜台本の画：実写 NTSB 図14 回収片の端面と中央の破断面（研究所・A＝副題「回収された破片の断面」）',
               src='NTSB p.61（`likely resulted in a local buckling failure that led to the implosion of the Titan`）'),
    'c619': dict(kind='図解',
               plan='台本の画：図 模式 筒の端の断面（剥離の起きた2つの面に、長い空隙が並ぶ＝c610 の図の拡大）',
               src='NTSB p.59（`these adhesive interfaces contained long extended voids`）・NTSB p.42（`end pieces that had been trimmed from the v2 full-scale cylinder during the construction/production process`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-15）：図解 第5章（4カット）＝模式図 `tools/mech22.py`（layers・buckle）
# ══════════════════════════════════════════════════════════
#   🔴 層の番号は内側から（層1＝いちばん内側＝NTSB p.41）。剥離＝赤（壊れた）・空隙とこすれの線は模式。章の札「海の底の残骸」と同じ並びを見出し・副題に入れない
_N_LY = "層の厚さと線は模式（層1がいちばん内側）"
SPEC.update({
    # c610（3行）＝筒の壁の断面（5枚の層・1枚＝約2.5センチ）→聞き役の問い→剥離の面（1と2・3と4）
    "c610": dict(
        t="層の貼り合わせ", s="筒の壁を切ると",
        fig=("m22", dict(view="layers", steps=[dict(tag=dict(t="約2.5センチ", at="th")), dict(), dict(state=dict(sep="on"))],
                         rel=[dict(t="約2.5センチ", src="NTSB p1059（1-inch-thick）")],
                         note=_N_LY, src=ss.src(["NTSB p1059", "NTSB p1040", "NTSB p1041"]))),
    ),
    # c615（2行）＝同じ断面。層1と層2が別々にずれてこすれた跡（長さの向き）＝爆縮の前から→聞き役
    "c615": dict(
        t="前からの剥離", s="内側の2枚",          # ⚠️ 門番 echo：「1枚目と2枚目の層」は語りの文の頭の写し
        fig=("m22", dict(view="layers", start=dict(sep="on"),
                         steps=[dict(state=dict(rub="on"), tag=dict(t="爆縮の前から", at="t", col=J.ALERT)), dict()],
                         note="こすれた跡の線は模式（向きは筒の長さの方向）", src=ss.src(["NTSB p1059", "NTSB p1044"]))),
    ),
    # c617（2行）＝厚い1枚が薄い2枚に分かれる（剥離）→外から押されて内へ曲がる（座屈）＝動く部品
    "c617": dict(
        t="薄くなる板", s="外から押されると",
        fig=("m22", dict(view="buckle", steps=[dict(state=dict(split="on"), tag=dict(t="薄い板に分かれる", at="r1")),
                                               dict(state=dict(press="on"), tag=dict(t="座屈", at="r2", col=J.ALERT))],
                         note="曲がり方は模式（米運輸安全委員会の報告書の説明）", src=ss.src(["NTSB p1061"]))),
    ),
    # c619（2行）＝同じ断面。剥離した2つの面に長い空隙が並ぶ（作られたときから）→次の章への問い
    "c619": dict(
        t="作ったときの空隙", s="剥離の面に",
        fig=("m22", dict(view="layers", start=dict(sep="on"), steps=[dict(state=dict(void="on"), tag=dict(t="最初から", at="t")), dict()],
                         note="空隙の形と並びは模式（剥離した2つの面だけ）", src=ss.src(["NTSB p1059", "NTSB p1042"]))),
    ),
})
