# -*- coding: utf-8 -*-
"""第7章　1つ目の船体 c801–c819（19カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c8.py`）。
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
    'c801': dict(kind='図解',
               plan='台本の画：図 模式 筒の作り方（樹脂の槽をくぐった炭素繊維の糸を、回る芯に巻きつける）',
               src='TSB §1.12.1（`the carbon fibre cylinder was manufactured through a process known as filament winding, which involved winding a continuous strand of carbon fibre on a mandrel.`）・USCG p.152〈144〉（`The assembly of the first TITAN submersible was completed in January 2018.`）'),
    'c802': dict(kind='図解',
               plan='台本の画：図 再現 品質点検の報告の要点（2018年1月18日・「切り落とした筒の端に空隙と剥離」の1行を明るく）',
               src='USCG p.146〈138〉（`on January 18, 2018, submitted a report highlighting critical safety concerns.`）・TSB §1.12.1（`visible voids and delaminations were present in the carbon fibre end segments that had been cut off after the manufacturing process.`）'),
    'c803': dict(kind='写真',
               plan='N18:左｜見せ方：全面｜副題：1つ目の船体の切り落とした端（事故のあとに調べた物）｜動き：右へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会の報告書 図18｜注：NTSB 図18 の左（約48%）を切り出す＝A｜台本の画：実写 NTSB 図18 の左＝1つ目の船体の切り落とした端の剥離（事故のあと NTSB の研究所が調べた・A・🔴 旧版 c307・c627 の副題「回収された破片」は取り違え＝副題「1つ目の船体の切り落とした端（事故のあとに調べた物）」）',
               src='NTSB p.44（`The v1 pressure vessel cylinder’s trimmed end contained multiple delaminations and voids.`）'),
    'c804': dict(kind='図解',
               plan='台本の画：図 再現 同じ報告の要点（「筒と接着の線を全部点検」「結果は人が乗る潜航の前に」）',
               src='TSB §1.12.1（`The report noted that a full inspection of the cylinder and the bond lines between the cylinder and the titanium rings was needed to verify their integrity.`）・§1.12.1（`the results of this inspection needed to be provided to the director of operations before any dives were conducted with people on board.`）'),
    'c805': dict(kind='図解',
               plan='台本の画：図 模式 会合の席（CEO・運航部長・社員3人の札と、録音の印）',
               src='TSB §1.12.1（`The following day, a meeting was held between the CEO, the director of operations, and 3 other OceanGate employees.`）・USCG p.149〈141〉（`argued for additional testing of the TITAN submersible’s hull`）・p.149〈141〉（`was audio recorded by the CEO.`）'),
    'c806': dict(kind='図解',
               plan='🔧 注：🔧 人の言葉＝輪郭＋吹き出し（§0-3）｜新しい画（映像方針）：図 再現 人の輪郭（CEO と会合の席＝顔は描かない）＋吹き出しの英字（NTSB p.48 が引く録音）・訳は字幕｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 録音の一節（NTSB p.48 が引く英字＋訳は字幕）',
               src='NTSB p.48（`“it’s clear that there is not a lot of confidence on your part in the engineering that went into this vessel`）'),
    'c807': dict(kind='図解',
               plan='台本の画：図 帯 2018年の年表（1/18 報告→1/19 会合→1/23 解任）',
               src='USCG p.149〈141〉（`On January 23, 2018, OceanGate fired the Director of Marine Operations.`）・TSB §1.12.1（`because he held different opinions from the CEO on the safety of the Titan.`）'),
    'c808': dict(kind='図解',
               plan='台本の画：図 帯 同じ年表（2/6 労働安全衛生局へ申し立て）',
               src='NTSB p.48（`filed a complaint with the Occupational Safety and Health Administration (OSHA) under the Seaman’s Protection Act.`）・p.48（`He told an OSHA investigator that cut-off sections of the carbon fiber cylinder were “like Swiss cheese”`）'),
    'c809': dict(kind='図解',
               plan='台本の画：図 帯 同じ年表（6/25 会社が訴える→12/13 申し立ての取り下げ）',
               src='USCG p.150〈142〉（`OceanGate filed a lawsuit against him on June 25, 2018`）・p.151〈143〉（`withdrew his SPA complaint against OceanGate`）'),
    'c810': dict(kind='図解',
               plan='台本の画：図 再現 業界の委員会の手紙の一節（NTSB p.23 が引く英字＋訳は字幕）',
               src='NTSB p.23（`expressing “unanimous concern regarding the development of ‘TITAN’ and the planned Titanic Expedition.”`）・p.23（`could result in negative outcomes (from minor to catastrophic)`）'),
    'c811': dict(kind='図解',
               plan='台本の画：図 再現 同じ手紙（「船級協会が見て立ち会う試作の試験を」の1行）',
               src='TSB §1.12.1（`The letter recommended that OceanGate institute a prototype testing program that was reviewed and witnessed by a classification society.`）・§1.12.1（`the MUV committee chair relayed the contents of the letter verbally to OceanGate’s CEO.`）'),
    'c812': dict(kind='図解',
               plan='🔧 G05｜注：🔧 自作の地図→衛星写真（了承②）｜新しい画（映像方針）：図 地図 衛星写真 G05（バハマ）＋「2018年5月〜2019年4月の試しの潜航」の札（場所の点は ⑤b-1 で報告書の字から）｜台本の画（🔧映像方針で替えた＝元の予定）：図 地図 バハマ（2018年5月〜2019年4月の試しの潜航の場所）',
               src='TSB §1.12.1（`During this time, OceanGate conducted 20 dives with people on board, the deepest one being 3939 m.`）'),
    'c813': dict(kind='図解',
               plan='🔧 G05｜注：🔧 再現→衛星写真の地図（§0-3・了承②）｜新しい画（映像方針）：図 地図 衛星写真 G05（バハマ・必要なら寄った別の画）＋2019年の潜航の場所に点・「ひび割れるような音」の赤の波の印・番号の列は画面に出さない｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 NTSB 表2（1つ目の船体の潜航の表＝場所ごとの3行・番号の列は「回数」と読ませない）',
               src='NTSB p.26（`persons aboard the Titan reported hearing cracking sounds.`）'),
    'c814': dict(kind='写真',
               plan='D367｜見せ方：全面｜副題：1つ目の船体（2023年8月、委員会が撮影）｜動き：寄る｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 9057367）｜注：DVIDS の撮影日欄「05.29.2019」は亀裂の日＝副題に写さない｜台本の画：実写 DVIDS 9057367 1つ目の船体（エバレットの会社の施設・内側の亀裂を削った跡・2023-08-02 に米沿岸警備隊の委員会が撮影＝MBI 図132 と同じ場面・A・全画面・🔴 DVIDS の撮影日欄「05.29.2019」は亀裂の日＝副題に写さない＝副題「1つ目の船体（2023年8月、委員会が撮影）」）',
               src='TSB §1.12.1（`a crack was found in the carbon fibre cylinder after a dive.`）・NTSB p.26（`it had originated from a sub-surface delamination (an internal separation within the carbon fiber cylinder).`）'),
    'c815': dict(kind='図解',
               plan='台本の画：図 模式 筒の内側の亀裂の位置（前の左舷に3つ＝カナダの調べの値・剥離の札）',
               src='NTSB p.26（`the first director of engineering stated that he told the CEO that because there was a crack, the pressure vessel hull was “done,”`）・p.26（`The director of engineering stated that he would not sign off on the planned 2019 expedition.`）・USCG p.161〈153〉（`However, the Director of Engineering refused`）'),
    'c816': dict(kind='図解',
               plan='台本の画：図 再現 客への手紙の要点（2019年の遠征の中止・亀裂の語が無い）',
               src='USCG p.162〈154〉（`OceanGate did not make any external notifications`）・NTSB p.26（`The planned 2019 expedition to the Titanic wreck site was cancelled.`）・USCG p.164〈156〉（`The letter, nor any other separate correspondence, disclosed that there was a crack found`）'),
    'c817': dict(kind='図解',
               plan='台本の画：図 帯 2019年の年表（7月 技術部長の解任・10月 加圧試験・11月 等級を下げる）',
               src='USCG p.164〈156〉（`On July 26, 2019, OceanGate fired the Director of Engineering.`）'),
    'c818': dict(kind='図解',
               plan='台本の画：図 帯 同じ年表（10月・11月を明るく）',
               src='TSB §1.12.1（`Following that test, further cracks and delamination were found in the carbon fibre cylinder.`）・§1.12.1（`from 4000 m to 3000 m with an understanding not to dive below 2000 m.`）・§1.12.1（`This carbon fibre cylinder was not subsequently used for any more dives.`）'),
    'c819': dict(kind='写真',
               plan='L39｜見せ方：額装（報告書の図）｜副題：1つ目（左）と2つ目の筒の端（研究所）｜動き：額ごと上へ｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図39｜注：比べの図・定規＝切らない｜台本の画：実写 24-011 図39 1つ目と2つ目の筒の切り落とした端の厚さの比べ（定規・青い背景・NTSB 研究所・A＝副題「1つ目（左）と2つ目の筒の端（研究所）」）',
               src='NTSB p.62（`after the failure of the v1 full-scale pressure vessel, OceanGate used different materials (pre-preg carbon fiber) and manufacturing methods`）'),
}

SPEC = {}

# ── 🆕 ⑤b-3（2026-10-14）：地図のカット（衛星写真＋描き足し＝`tools/satmap.py`・c2.py の注）──
SPEC.update({
    # c812（2行）＝1行目でバハマの試しの潜航の拠点（マーシュハーバー＝USCG 4.22.1・地図の側に地名がある＝札は役目）・2行目で数（黄）
    "c812": dict(**ss.sat("G05", note="マーシュハーバーは一般の座標", steps=[
        [dict(k="pt", at="marsh", role="company", t="試しの潜航の拠点", lab=(24, -14, "start"))],
        [dict(k="txt", at="marsh", t="人が乗った潜航 20回", lc="AMBER", lab=(24, 34, "start")),
         dict(k="txt", at="marsh", t="最も深く 3,939メートル", lc="AMBER", lab=(24, 78, "start"))]]),
        t="バハマの試験", s="グレートアバコ島のあたり（現在の衛星写真）"),
    # c813（2行）＝1行目で 2019年の潜航の海（47回目＝リトルハーバーの沖 約10マイル＝USCG 4.22.14・点は模式）・2行目で「ひび割れるような音」（赤の波）
    #   ⚠️ 音を聞いたのは 42〜44・45.1〜47回目（NTSB 表2 の下の文）＝場所が書いてあるのは 47回目だけ＝点は1つ
    "c813": dict(**ss.sat("G05", note="点は「リトルハーバーの沖 約10マイル」（米沿岸警備隊）を一般の座標から置いた模式", steps=[
        [dict(k="pt", at="abaco47", role="company", t="2019年の潜航の海", lab=(24, -16, "start"))],
        [dict(k="wave", at="abaco47", t="ひび割れるような音", lab=(30, 72, "start"))]]),
        t="ひび割れの音", s="2019年の試しの潜航（現在の衛星写真）"),
})
