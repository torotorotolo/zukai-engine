# -*- coding: utf-8 -*-
"""第11章　3つの報告書が出した答え cc01–cc13（13カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/cc.py`）。
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
    'cc01': dict(kind='写真',
               plan='🔧 C1cc｜見せ方：全面｜副題：海難調査委員会の委員たち（2024年9月・公聴会のあと）｜動き：寄る｜権利：A（米沿岸警備隊の職員の職務・DVIDS 8668382 の写し）｜出典の行：米沿岸警備隊（DVIDS 8668382）｜注：🔧 素材を替えた（公聴会の配信〈9日分から委員だけの区間を探す〉→ 委員の集合写真＝A・公的な任務）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 米沿岸警備隊の海難調査委員会の公聴会（2024年9月・USCG の公式の配信・委員会の職員だけが写る区間・A＝副題「海難調査委員会の公聴会（2024年9月）」）',
               src='USCG p.5〈v〉（`in what is considered to be a preventable tragedy.`）'),
    'cc02': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 3冊の色分けの3列（米沿岸警備隊＝青の列を明るく・主な要因8つを短い札で＝主語は「会社」と「船体」）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 主な要因8つ（USCG p.7 の8項目の要点の札＝主語は全部「会社」か「船体」・欄の英字は小さく）',
               src='USCG p.5〈v〉（`OceanGate’s failure to follow established engineering protocols for safety, testing, and maintenance of their submersible, was the primary causal factor.`）・USCG p.7〈vii〉（`The primary causal factors that directly contributed to the casualty include:`）'),
    'cc03': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 同じ3列（青の列の7つ目＝職場の文化を明るく・その他の要因＝規則の足りなさ）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ札（7つ目＝職場の文化・その他の寄与要因の4つ目＝規則の足りなさ）',
               src='USCG p.7〈vii〉（`used firings of senior staff members and the looming threat of being fired`）・USCG p.8〈viii〉（`the lack of comprehensive and effective regulations for the oversight and operation of manned submersibles`）'),
    'cc04': dict(kind='写真',
               plan='🔧 L45a｜見せ方：全面｜副題：後ろの輪に残った接着剤（米運輸安全委員会の研究所）｜動き：寄る｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図45｜注：🔧 素材を替えた（2024-09-15 の米沿岸警備隊の記者会見 → 米運輸安全委員会の研究所の写真＝語り「米運輸安全委員会は、どう書いたの？」）。c608 と同じ物＝呼び方をそろえる｜台本の画（🔧映像方針で替えた＝元の予定）：実写 米沿岸警備隊の記者会見（2024-09-15・公聴会の前・A・登壇は公的な任務の人＝副題「公聴会の前の記者会見（2024年9月）」）',
               src='NTSB p.74（`the probable cause of the hull failure and implosion of the submersible Titan was OceanGate’s inadequate engineering process,`）・NTSB p.74（`which failed to establish the actual strength and durability of the Titan pressure vessel`）'),
    'cc05': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 同じ3列（米運輸安全委員会＝緑の列を明るく・推定原因と寄与2つ）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 推定原因の「寄与」（指針と規則が足りなかった・監視の記録の読み違い）',
               src='NTSB p.74（`Contributing were US and international voluntary guidance and US small passenger vessel regulations that were insufficient to ensure OceanGate adhered to established industry standards.`）・p.74（`Also contributing was OceanGate’s flawed analysis of their pressure vessel monitoring system data`）'),
    'cc06': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 同じ3列（カナダの調べ＝紫の列を明るく・原因と寄与）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 TSB の所見（原因と寄与5＝会社と船体の札）',
               src='TSB §3.1（`The as-built properties of the Titan’s carbon fibre cylinder were never validated to ensure they met the theoretical values used in the design process,`）・§3.1（`likely led the cylinder to fail progressively with damage accumulating during each dive cycle until it imploded`）'),
    'cc07': dict(kind='図解',
               plan='台本の画：図 再現 TSB の要点（運輸省は登録が無いと知らなかった・ほかの役所の情報が届かなかった）',
               src='TSB §4.2.1（`TC was unaware that the Titan was not registered with any flag state.`）・TSB §1.28.5（`In this occurrence, both DFO and the CBSA had information about the Titan that TC was not aware of.`）'),
    'cc08': dict(kind='図解',
               plan='台本の画：図 再現 TSB の勧告6つ（宛先は6つともカナダ運輸省・番号 M26-02〜07）',
               src='TSB §4.2（`The investigation identified safety deficiencies that led the Board to issue the following 6 recommendations.`）・TSB の勧告のページ（rec-m2602・m2604〜m2607＝Date of the latest response: N/A・Not Yet Assessed／m2603 は頁なし＝2026-10-14 に見た・3冊の外・記録は src/new/tsb_rec/）'),
    'cc09': dict(kind='図解',
               plan='台本の画：図 帯 3つの答えの並べ（重なる所＝窓でなく船体の炭素繊維の側・強さと寿命を確かめず・監視の読み方）',
               src='USCG p.325〈317〉（`the probable failure point of the hull was either the adhesive joint between the TITAN’s forward dome and the titanium segment or the carbon fiber hull near the forward end of the TITAN.`）・NTSB p.73（`the company was unaware of its actual strength and durability`）・TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure.`）・TSB §3.1（`OceanGate did not know for how long the pressure hull would remain safe`）'),
    'cc10': dict(kind='図解',
               plan='台本の画：図 帯 同じ並べ（分かれる所＝2022年の音の重み・最後の数秒の順番を明るく）',
               src='USCG p.289〈281〉（`strongly suggests that the carbon fiber hull sustained irreversible damage at the end of Dive 80.`）・NTSB p.73（`The Titan pressure vessel likely sustained damage after it surfaced at the end of dive 80`）・TSB §1.10.10.1（`so it cannot be determined whether this event precipitated the non-linear readings on 19 July 2022.`）'),
    'cc11': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 同じ3列（3列それぞれに「監督の穴」の札＝主な原因の次の段に置く）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 規則と監督の穴の重み（米運輸安全委＝寄与／米沿岸警備隊＝その他の要因／カナダ＝危険の所見）',
               src='NTSB p.74（`Contributing were US and international voluntary guidance and US small passenger vessel regulations`）・USCG p.8〈viii〉（`the lack of comprehensive and effective regulations for the oversight and operation of manned submersibles`）・TSB §3.2（`Canada’s approach to regulatory oversight of vessels enabled the Titan to operate without any independent verification to identify safety deficiencies,`）・TSB §3.2（`These factors may or may not have been causal or contributing to the occurrence`）'),
    'cc12': dict(kind='写真',
               plan='U248｜区間 535.0〜545.0秒｜倍率 1.08（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：海難調査委員会を開く記者会見（2023年6月25日）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 888248）｜注：のちの委員長（調査の責任者の大佐）が話す・器も実効も1280｜台本の画：実写 米沿岸警備隊の記者会見（DVIDS 888248・2023-06-25・海難調査委員会を開くと発表・器 1280・A＝副題「海難調査委員会を開く記者会見（2023年6月25日）」）',
               src='USCG p.307〈299〉（`Had OceanGate adhered to the safety standards outlined in its own HSE Manual and fostered a culture of transparency and accountability, this tragedy would likely have been averted`）'),
    'cc13': dict(kind='図解',
               plan='台本の画：図 再現 同じ節の一節（英字＋訳は字幕）',
               src='USCG p.307〈299〉（`Encouraging employees to voice concerns without fear of retaliation and prioritizing safety over expediency could have prevented the sequence of events that led to the disaster.`）'),
}

SPEC = {}
