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

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-15）：図解 第11章（10カット）＝模式図 `tools/mech22.py`（cols・cmp・paper・cards）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「3つの報告書が出した答え」と4字以上同じ並び（「3つの報告」「した答え」）を見出し・副題に入れない（門番 dup）。
#      列の名（米沿岸警備隊・米運輸安全委員会・カナダの調べ）と段の名（主な要因・推定原因 ほか）も見出しに入れない（図の言葉）。
#      写真 cc01・cc04 と映像 cc12 は ⑤b-7
_N_CL = "要点（模式）・札の色＝主語（会社 橙・船体 白・規則 灰）"      # ⚠️ 門番 layout：cc11 の6冊の出典と合わせて右の端を越えた＝短く
_CL_SRC = ["USCG p5", "USCG p7", "USCG p8", "NTSB p1074", "TSB §3.1", "TSB §3.2"]
SPEC.update({
    # cc02（2行）＝🔧 再現→模式（3列）。米沿岸警備隊＝主な原因（手順に従わず）→主な要因8つ（主語は会社と船体）
    "cc02": dict(
        t="1つ目の調べ", s="8つの要因",       # ⚠️ 門番 dup：「海難調査委員会」は出典の行の写し
        fig=("m22", dict(view="cols", steps=[dict(state=dict(u0="on")), dict(state=dict(u8="on"))], note=_N_CL, src=ss.src(["USCG p5", "USCG p7"]))),
    ),
    # cc03（2行）＝同じ3列。7つ目＝解雇と脅しの職場（下線）→その他の要因＝規則の足りなさ
    "cc03": dict(
        t="職場の文化", s="要因の7つ目",
        #   ⚠️ ⑤c'（10-15）：その他の要因は4つ（図は規則だけ）＝⑥ の前の注意（mech22 の CL_TIER の注）
        fig=("m22", dict(view="cols", start=dict(u0="on", u8="on"), steps=[dict(state=dict(u7="on")), dict(state=dict(ux="on"))],
                         note=_N_CL, src=ss.src(["USCG p7", "USCG p8"]))),
    ),
    # cc05（2行）＝同じ3列。米運輸安全委員会＝推定原因（cc04 の語り＝頭で出す）→寄与1（規則と指針）→寄与2（監視の記録の読み違い）
    "cc05": dict(
        t="2つ目の調べ", s="寄与したこと",
        fig=("m22", dict(view="cols", start=dict(u0="on", u8="on", u7="on", ux="on", n1="on"), steps=[dict(state=dict(n2="on")), dict(state=dict(n3="on"))],
                         note=_N_CL, src=ss.src(["NTSB p1074"]))),
    ),
    # cc06（2行）＝同じ3列。カナダの調べ＝強さを確かめず→潜るたびに傷が積もって壊れた
    "cc06": dict(
        t="3つ目の調べ", s="筒の強さ",
        #   🔧 ⑤c'（10-15）：t2「傷が積もって壊れたとみられる」（likely）。⚠️ TSB §3.1 の所見は5段落（図は2つ）＝⑥ の前の注意（mech22 の CL_TIER の注）
        fig=("m22", dict(view="cols", start=dict(u0="on", u8="on", u7="on", ux="on", n1="on", n2="on", n3="on"),
                         steps=[dict(state=dict(t1="on")), dict(state=dict(t2="on"))], note=_N_CL, src=ss.src(["TSB §3.1"]))),
    ),
    # cc07（2行）＝カナダの調べの要点（運輸省は登録が無いと知らなかった→ほかの役所の情報が届かなかった）
    "cc07": dict(
        t="知らなかった役所", s="登録の無い艇",
        fig=("m22", dict(view="paper", start=dict(doc="tc"), steps=[dict(state=dict(hl1="on", hl2="on")), dict(state=dict(hl3="on", hl4="on"))],
                         note="句はカナダの報告書（英字のまま・模式）・TC＝カナダ運輸省・DFO＝漁業海洋省・CBSA＝国境サービス庁",
                         src=ss.src(["TSB §4.2.1", "TSB §1.28.5"]))),
    ),
    # cc08（2行）＝勧告6つ（宛先は6つとも運輸省）→運輸省の返事は勧告のページにまだ無い（2026年10月）
    "cc08": dict(
        t="勧告の宛先", s="6つとも同じ役所",
        fig=("m22", dict(view="cards", start=dict(set="rec6"),
                         steps=[dict(state=dict(n="6")), dict(tag=dict(t="返事はまだ載らず", d="2026年10月の時点", at="low", col=J.INST))],
                         rel=[dict(t="2026年10月の時点", src="TSB の勧告のページ（2026年10月14日に見た）")],
                         note="番号はカナダの調べの勧告（模式）・返事の欄は勧告のページ（3つの報告書の外）", src=ss.src(["TSB §4.2"]))),
    ),
    # cc09（3行）＝3つの答えの並べ。聞き役の問い→重なる所（炭素繊維の側）→強さと寿命を確かめず・監視の記録を生かせず
    "cc09": dict(
        t="重なる答え", s="壊れた所と理由",
        fig=("m22", dict(view="cmp", steps=[dict(), dict(state=dict(n="1")), dict(state=dict(n="3"))],
                         note="並べは要点（模式）", src=ss.src(["USCG p7", "NTSB p1073", "NTSB p1074", "TSB §2.1", "TSB §3.1"]))),
    ),
    # cc10（2行）＝同じ並べ。聞き役の問い→分かれる所（2022年の音の重み・最後の数秒の順番）
    "cc10": dict(
        t="分かれる答え", s="重みと順番",
        fig=("m22", dict(view="cmp", start=dict(n="3"), steps=[dict(), dict(state=dict(n="5"))],
                         note="並べは要点（模式）",
                         src=ss.src(["USCG p289", "NTSB p1059", "TSB §1.10.10.1", "USCG p37", "TSB §1.3.2"]))),
    ),
    # cc11（3行）＝🔧 再現→模式（同じ3列）。3列それぞれの下の段に「監督の穴」の枠（カナダの危険の所見を足す）→主な原因ではない→聞き役
    "cc11": dict(
        t="監督の穴", s="次の段に置く",
        fig=("m22", dict(view="cols", start=dict(u0="on", u8="on", u7="on", ux="on", n1="on", n2="on", n3="on", t1="on", t2="on"),
                         steps=[dict(state=dict(tx="on", gap="on")), dict(), dict()], note=_N_CL, src=ss.src(_CL_SRC))),
    ),
    # cc13（2行）＝米沿岸警備隊の報告書の一節（社員が仕返しを恐れず懸念を言える場・早さより安全→防げたかもしれない）
    "cc13": dict(
        t="社員の声", s="結びの一節",
        fig=("m22", dict(view="paper", start=dict(doc="u307"), steps=[dict(state=dict(hl1="on", hl2="on", hl3="on")), dict(state=dict(hl4="on", hl5="on"))],
                         note="句は米沿岸警備隊の報告書（英字のまま・模式）", src=ss.src(["USCG p307"]))),
    ),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-15）：写真・映像 第11章（3カット）＝映像方針の一覧（了承②）。副題は焼いた絵を原寸で見てから最終に
# ══════════════════════════════════════════════════════════
_BOARD = P("commons_uscg_mbi_8668382")
_GROOVE = P("lab24011_p73_fig45a")
SPEC.update({
    # cc01（8.6秒）＝海難調査委員会の委員たち（DVIDS 8668382 の写し・公的な任務）・全面・寄る
    "cc01": dict(photo=_BOARD, **ss.mv(_BOARD, "in"), side="none", t="防げた事故", s="海難調査委員会の委員たち（2024年9月・公聴会のあと）"),
    # cc04（10.0秒）＝聞き役の問い＋答え。後ろの輪に残った接着剤（24-011 図45 の上・1320×880）・全面・寄る。c608 と同じ物＝呼び方をそろえる
    "cc04": dict(photo=_GROOVE, **ss.mv(_GROOVE, "in"), side="none", t="確かめない強さ", s="後ろの輪に残った接着剤（米運輸安全委員会の研究所）"),
    # cc12（8.4秒）＝DVIDS 888248 の 535.0〜545.0秒（のちの委員長の大佐が話す・器も実効も 1280）
    "cc12": ss.vid("cc12", side="none", t="安全の文化", s="海難調査委員会を開く記者会見（2023年6月25日）"),
})
