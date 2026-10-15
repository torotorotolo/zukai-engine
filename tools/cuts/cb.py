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
        #   🔧 ⑤b-3 の試し焼き：「台（タイタン）」が台の四角から離れて左下に浮いた＝札は船の印からの位置＝台（船の後ろ 約62px）の左へ
        [dict(k="icon", what="ship", on=("stjohns", "site", 0.5), role="ship", tow=True, t="台（タイタン）", lab=(-40, -50, "end"))]]),
        t="引いて運ぶ", s="セントジョンズから現場へ（現在の衛星写真）"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-15）：図解 第10章（13カット）＝模式図 `tools/mech22.py`・時間の帯（axis）・棒（qty）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「最後の冬と2023年」と4字以上同じ並び（「最後の冬」「2023年」）を見出し・副題に入れない（門番 dup）。字は12字未満（門番 echo）。
#      写真 cb07・cb11・cb12・cb15 は ⑤b-7・地図 cb01・cb09 は ⑤b-3
_N_PU = "句は米沿岸警備隊の報告書（英字のまま・模式）"
SPEC.update({
    # cb02（2行）＝基地のメール（覆いの見積もりは出したが、会社の承認が無く買わなかった）→前の冬は本社の屋内（米運輸安全委員会）
    "cb02": dict(
        t="覆いの見積もり", s="返事が無いまま",
        fig=("m22", dict(view="paper", start=dict(doc="tarp"),
                         steps=[dict(state=dict(hl1="on", hl2="on", hl3="on")), dict(tag=dict(t="前の冬は屋内", d="アメリカの会社の建物", at="r2", col=J.COMPANY))],
                         note=_N_PU + "・前の冬は米運輸安全委員会の報告書", src=ss.src(["USCG p237", "NTSB p1035"]))),
    ),
    # cb03（1行）＝帯（2022年7月26日〜2023年2月6日＝屋外・覆いなし）。括弧は語りの「半年あまり」
    "cb03": dict(
        t="外にあった期間", s="港の基地の駐車場",
        fig=("axis", dict(ss.AX_OUT, steps=[dict(add=[ss.ax("out22"), ss.ax("half")], cur="2023-02-06")],
                          note="日付は米沿岸警備隊の報告書（覆いの無い屋外）", src=ss.src(["USCG p236", "USCG p238", "TSB §1.22"]))),
    ),
    # cb04（2行）＝🔧 棒→目盛りの点（気温は 0 より下＝棒は 0 から右へしか描けない）。最高の平均 −0.5°・最低の平均 −5.5°→雪・強い風・凍る雨
    "cb04": dict(
        t="冬のセントジョンズ", s="カナダの調べの値",
        fig=("m22", dict(view="temp", steps=[dict(state=dict(avg="on"), tag=[dict(t="−0.5°", d="最高気温の平均", at="hi"), dict(t="−5.5°", d="最低気温の平均", at="lo")]),
                                             dict(state=dict(wx="on"), tag=dict(t="雪・強い風・凍る雨", d="海に面した町", at="wx", col=J.INK_W))],
                         rel=[dict(t="−0.5°", src="TSB §1.22"), dict(t="−5.5°", src="TSB §1.22")],
                         note="点はカナダの報告書の値（単位の書き方もそのまま）・模式", src=ss.src(["TSB §1.22"]))),
    ),
    # cb05（2行）＝船体のすき間の水が凍ってふくらむ（米運輸安全委員会の見立て）→2つの調べは「あり得る」まで
    "cb05": dict(
        t="冬の傷み", s="水が凍ると",          # ⚠️ 門番 dup：「すき間の水」は note の写し
        fig=("m22", dict(view="layers", steps=[dict(state=dict(ice="on"), tag=dict(t="凍ってふくらむ", at="t", col=J.ALERT)),
                                               dict(tag=dict(t="あり得る、まで", d="2つの調べ", at="r2", col=J.INK_W))],
                         rel=[dict(t="2つの調べ", src="NTSB p1060・TSB §2.1.3")],
                         note="すき間の場所と形は模式（水が入った所は報告書に無い）・2つの調べ＝米運輸安全委員会とカナダ",
                         src=ss.src(["NTSB p1060", "TSB §2.1.3"]))),
    ),
    # cb06（2行）＝米沿岸警備隊の結論（屋外に置いて船体を損ねた）→主な要因の8つ目
    "cb06": dict(
        t="外での保管", s="8つ目の要因",
        fig=("m22", dict(view="paper", start=dict(doc="u8"), steps=[dict(state=dict(hl1="on", hl2="on")), dict(state=dict(hl3="on", hl4="on"))],
                         note=_N_PU, src=ss.src(["USCG p328", "USCG p7"]))),
    ),
    # cb08（3行）＝🔧 再現→模式（c207 と同じ席）。聞き役の問い→計画書の技術部長＝「未定」→正式には空いたまま（枠）
    "cb08": dict(
        t="技術の責任者", s="遠征の人の欄",
        fig=("m22", dict(view="org", start=dict(seats="on"),
                         steps=[dict(), dict(tag=dict(t="未定（TBD）", d="遠征の計画書", at="eng", to="eng", col=J.AMBER)), dict(state=dict(vac="on"))],
                         note="席の並びは模式（空席はカナダの報告書の表4・計画書は米沿岸警備隊の報告書）",
                         src=ss.src(["USCG p246", "TSB §1.23.1", "TSB §1.23"]))),
    ),
    # cb10（1行）＝棒（綱につながれていた時間 約950時間＝カナダの調べ）。道のりは描かない（2冊で単位が違う・語りに無い）
    "cb10": dict(
        t="引かれた時間", s="カナダの調べの値",
        fig=("qty", dict(view="bar", groups=[ss.QG["tow"]], steps=[dict(add=[ss.qb("tow23")])],
                         note="綱で引かれたか、綱でつながれていた時間の合計（約950時間）", src=ss.src(["TSB §1.20.2.2"]))),
    ),
    # cb13（3行）＝引かれたことの影響の見方（米沿岸警備隊＝さらに弱った・カナダ＝引くだけでは原因の見込みは低い／傷を広げたかも）
    "cb13": dict(
        t="引いた影響", s="見方の違い",
        fig=("m22", dict(view="cards", start=dict(set="tow"),
                         steps=[dict(), dict(state=dict(n="1")),
                                dict(state=dict(n="2"), tag=dict(t="引くだけでは低い", d="原因になった見込み", at="low", col=J.INST))],
                         note="要点（模式）・米運輸安全委員会は「影響は分からない」", src=ss.src(["USCG p295", "TSB §2.1.3", "NTSB p1060"]))),
    ),
    # cb14（2行）＝🔧 再現→棒。聞き役の問い→人が乗った3回とも10メートル（台を離れず）とタイタニックの深さ
    "cb14": dict(
        t="浅い潜航", s="台を離れず",
        fig=("qty", dict(view="bar", groups=[ss.QG["dep23"]], steps=[dict(), dict(add=[ss.qb("dep23_sub"), ss.qb("dep23_tt")])],
                         note="人が乗った3回とも10メートル（カナダの報告書 付録B）・タイタニックは目安",
                         src=ss.src(["TSB §1.21.4", "NTSB p1014", "TSB §付録B", "TSB §1.3"]))),
    ),
    # cb16（1行）＝🔧 再現→帯。監視装置の記録が残るのは 2021年2月〜2022年7月23日（カナダの調べ）＝2023年の潜航は記録なし
    "cb16": dict(
        t="監視の記録", s="残った期間",
        fig=("axis", dict(ss.AX_RTM, steps=[dict(add=[ss.ax("rtm_on"), ss.ax("rtm_off")], cur="2023-06-18")],
                          note="期間はカナダの報告書（記録なしの帯は付録B の人が乗った潜航）", src=ss.src(["TSB §1.10.9", "USCG p139", "TSB §付録B"]))),
    ),
    # cb17（2行）＝🔧 再現→模式。事故の潜航の計画の危険度＝35→48を超えるとストライク1つ・3つで その日は中止
    "cb17": dict(
        t="潜航の前の点数", s="会社の決まり",
        fig=("m22", dict(view="risk", steps=[dict(state=dict(day="on"), tag=dict(t="この日 35", at="day", col=J.AMBER)),
                                             dict(state=dict(line="on", three="on"), tag=[dict(t="48を超えると", d="ストライク1つ", at="line", col=J.ALERT),
                                                                                         dict(t="3つで中止", d="その日の潜航", at="three", col=J.ALERT)])],
                         rel=[dict(t="この日 35", src="TSB §1.17.12.1"), dict(t="48を超えると", src="TSB §1.17.12.1"),
                              dict(t="ストライク1つ", src="TSB §1.17.12.1"), dict(t="3つで中止", src="USCG p78")],
                         note="目盛りの右の端は模式（点数の出し方は分からない＝カナダの調べ）", src=ss.src(["TSB §1.17.12.1", "USCG p78"]))),
    ),
    # cb18（3行）＝米運輸安全委員会の所見（82回目のあと・出どころの分からない傷み・タイタニックの深さに耐えられない）
    "cb18": dict(
        t="加わった傷み", s="最後の深い潜航のあと",
        fig=("m22", dict(view="paper", start=dict(doc="n73"),
                         steps=[dict(state=dict(hl1="on")), dict(state=dict(hl2="on")), dict(state=dict(hl3="on", hl4="on"))],
                         note="句は米運輸安全委員会の報告書（英字のまま・模式）", src=ss.src(["NTSB p1073", "NTSB p1060"]))),
    ),
    # cb19（2行）＝帯（台の上の10メートルの潜航3回→6月18日＝初めて台を離れて深く潜る）→聞き役
    "cb19": dict(
        t="その日の潜航", s="この年で初めて",
        fig=("axis", dict(ss.AX_23, steps=[dict(add=[ss.ax("s0531"), ss.ax("s0605"), ss.ax("s0613"), ss.ax("s10m"), ss.ax("occ23"), ss.ax("first88")],
                                                cur="2023-06-18"), dict(cur="2023-06-18")],
                          note="日付はカナダの報告書 付録B（台の上の潜航＝深さ10メートル）",
                          src=ss.src(["TSB §付録B", "USCG p256", "USCG p295", "NTSB p1016"]))),
    ),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-15）：写真 第10章（4カット）＝映像方針の一覧（了承②）。副題は焼いた絵を原寸で見てから最終に
# ══════════════════════════════════════════════════════════
#   cb11＝第三者（個人の撮影＝NTSB 図10・縦長2枚の組）＝額装だけ・色を変えない・額ごと動かす。日付は図10 の凡例（5月20日と27日）
#   ＝語りの5月24日（cb12）の横に置かない（映像方針で cb11 へ移した）
_DOCK = P("mbi_fig109_lars_dock")
_TIPPED = P("ntsb_fig10_lars_tipped")
_VALVE = P("mbi_fig112_ballast_valve")
_AIR = P("mbi_fig115_air_regulator")
SPEC.update({
    # cb07（7.8秒）＝潜水艇を載せる台（MBI 図109＝c305 の図5 と同じ場面の別の写真・幅 1221）・全面・左へ
    "cb07": dict(photo=_DOCK, **ss.mv(_DOCK, "l"), side="none", t="見たかった内側", s="潜水艇を載せる台（事故の後に撮影）"),
    # cb11（7.3秒）＝傾いた台（NTSB 図10＝個人の撮影・縦長2枚）・額ごと右へ
    "cb11": dict(photo=_TIPPED, panel=True, color=1.0, fmove=ss.fm("r"), t="大きな揺れ", s="傾いた台（2023年5月20日と27日）"),
    # cb12（11.0秒）＝聞き役の反応つき。台の浮き沈みを決める弁（MBI 図112・黄の丸は MBI・828×437）・額ごと引く
    "cb12": dict(photo=_VALVE, panel=True, fmove=ss.fm("out"), t="半ば沈む", s="台の浮き沈みを決める弁（事故の後に撮影）"),
    # cb15（9.9秒）＝台を浮かせる空気の装置（MBI 図115・960×817）・全面・上へ
    "cb15": dict(photo=_AIR, **ss.mv(_AIR, "u"), side="none", t="打ちつけられた艇", s="台を浮かせる空気の装置（事故の後に撮影）"),
})
