# -*- coding: utf-8 -*-
"""終章　3つの問いの答え cd01–cd09（9カット）。22本目（タイタン号のリメイク）。

■ 🆕 2026-10-14（⑤b-1）：新しいファイル（22本目は つかみ＋11章＋終章＝区切り13＝21本目より1つ多い）。
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
    'cd01': dict(kind='写真',
               plan='R04｜区間 41.8〜47.32秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：海の底で見つかった尾部（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：右端に尾部の横（OceanGate の字）→ 終章の扉は方眼だけ｜台本の画：実写 ROV「尾部」（04・c101・c108・c517 と別の区間・第三者＝引用・額装＝副題「海の底の残骸（2023年6月22日）」）',
               src='—'),
    'cd02': dict(kind='図解',
               plan='🔧 注：🔧 再現→問いのカード（§0-3）｜新しい画（映像方針）：図 問い 3つの問いのカード（①何が壊れたのか を明るく＝「窓ではなく船体の炭素繊維の側」）＝c107 の3つの問いと同じ並び｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 3つの問いの札（①何が壊れたのか＝「窓ではなく船体の炭素繊維の側」を明るく）',
               src='NTSB p.74（`resulting in a damaged internal structure that subsequently led to a local buckling failure of the pressure vessel.`）・TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure.`）'),
    'cd03': dict(kind='図解',
               plan='🔧 注：🔧 再現→問いのカード（§0-3）｜新しい画（映像方針）：図 問い 同じカード（②なぜ潜り続けたのか を明るく）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ札（②なぜ潜り続けたのか）',
               src='USCG p.290〈282〉（`should have been a red flag to stop all dive operations. However, OceanGate proceeded to continue scheduled dive operations afterward,`）・USCG p.289〈281〉（`a cursory external examination of the TITAN was conducted following the loud bang with no visible damage identified.`）・USCG p.290〈282〉（`directed that no further investigation or assessments were necessary`）・USCG p.290〈282〉（`neither the Director of Engineering nor anyone else onboard with the authority to assess the submersible’s safety possessed the necessary engineering expertise to interpret the strain gauge data`）'),
    'cd04': dict(kind='図解',
               plan='🔧 注：🔧 再現→問いのカード（§0-3）｜新しい画（映像方針）：図 問い 同じカード（③誰が止められたのか を明るく）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ札（③誰が止められたのか）',
               src='USCG p.307〈299〉（`this tragedy would likely have been averted`）・NTSB p.74（`the probable cause of the hull failure and implosion of the submersible Titan was OceanGate’s inadequate engineering process,`）・TSB §3.1（`These are the factors that were found to have caused or contributed to the occurrence.`）・TSB §1.23.1（`some OceanGate employees with expertise in specific areas left the company or were dismissed after raising safety-related concerns`）・NTSB p.70（`the existing regulations and voluntary guidance, as currently written, enabled OceanGate’s operation of the Titan in an unsafe manner.`）'),
    'cd05': dict(kind='図解',
               plan='台本の画：図 再現 TSB の一節（過去の成功は将来の成功を約束しない＝英字＋訳は字幕）',
               src='TSB §1.23.1（`On each occasion, OceanGate had been able to recover the Titan.`）・TSB §1.30.2（`However, past success is not a guarantee of future success,`）'),
    'cd06': dict(kind='図解',
               plan='台本の画：図 再現 同じ節の続き（ずれは少しずつで気づきにくい）',
               src='TSB §1.30.2（`because this drift occurs gradually, it is not easily identifiable and may go unnoticed as risk levels grow over time.`）'),
    'cd07': dict(kind='写真',
               plan='L43b｜見せ方：全面｜副題：回収された後ろのチタンの輪（研究所）｜動き：引く｜権利：A（NTSB の研究所）｜出典の行：米運輸安全委員会 研究所の報告 24-011 図43｜注：c607 の FBI 図157 と同じ物＝呼び方をそろえる｜台本の画：実写 24-011 図43 前部と後部のセグメント（パレットの上・NTSB 研究所・A・c606 の FBI 図159 とは別の写真＝副題「回収された前と後ろのチタンの輪（研究所）」）',
               src='USCG p.307〈299〉（`This tragedy serves as a stark reminder of the critical importance of prioritizing safety in high-risk operations`）'),
    'cd08': dict(kind='写真',
               plan='R07｜区間 18.0〜27.26秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：残骸が詰まった後ろのドーム（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜台本の画：実写 ROV「後ろのドーム」（07・c105・c523・c602 と別の区間・第三者＝引用・額装）',
               src='NTSB p.9（`All five persons on board the vessel died.`）'),
    'cd09': dict(kind='パネル',
               plan='台本の画：panel コメントの問い（文字だけ＝問いの2行・ed01 の直前）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-15）：図解 終章（5カット）＋パネル（cd09）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「3つの問いの答え」と4字以上同じ並び（「3つの問い」「問いの答え」）を見出し・副題に入れない（門番 dup）。問いの言葉（c107 の語り）は箱の題＝見出しに入れない。
#      3つの問いは「図解」（cards）＝パネルにすると文字だけが cd02〜cd04 で3つ続く（3つまで）。写真・映像 cd01・cd07・cd08 は ⑤b-7
_N_Q3 = "問いは冒頭と同じ言葉・答えは報告書の要点（模式）"
_N_DR = "句はカナダの報告書（英字のまま・模式）"
SPEC.update({
    # cd02（2行）＝🔧 再現→問いの箱。1つ目＝窓でなく船体の炭素繊維の側→層がはがれ、傷が重なって押しつぶされた
    "cd02": dict(
        t="1つ目の答え", s="壊れた場所",
        fig=("m22", dict(view="cards", start=dict(set="q3"),
                         steps=[dict(state=dict(n="1")), dict(tag=dict(t="層がはがれて弱る", d="押しつぶされた", at="b1", col=J.SUB))],
                         note=_N_Q3, src=ss.src(["NTSB p1074", "TSB §2.1"]))),
    ),
    # cd03（2行）＝2つ目＝音のあと CEO は調べは要らないと指示→読み解ける人がいないまま、外から見ただけで潜った
    "cd03": dict(
        t="2つ目の答え", s="続けた理由",
        fig=("m22", dict(view="cards", start=dict(set="q3", n="1"),
                         steps=[dict(state=dict(n="2"), tag=dict(t="調べは要らない", d="CEO の指示", at="b2", col=J.COMPANY)), dict()],
                         note=_N_Q3, src=ss.src(["USCG p290", "USCG p289"]))),
    ),
    # cd04（3行）＝3つ目＝会社自身→懸念を言った社員は辞めた・辞めさせられた→外から止める仕組みは主な原因の次
    "cd04": dict(
        t="3つ目の答え", s="会社の中と外",
        fig=("m22", dict(view="cards", start=dict(set="q3", n="2"),
                         steps=[dict(state=dict(n="3")), dict(), dict(tag=dict(t="外の仕組み", d="主な原因の次に置く", at="b3", col=J.INK_W))],
                         note=_N_Q3, src=ss.src(["USCG p307", "NTSB p1074", "TSB §3.1", "TSB §1.23.1", "NTSB p1070"]))),
    ),
    # cd05（2行）＝うまくいかないことがあっても艇は戻った（カナダの調べ）→過去の成功は将来の成功を約束しない（下線）
    "cd05": dict(
        t="戻り続けた艇", s="成功と安全",
        fig=("m22", dict(view="paper", start=dict(doc="drift"), steps=[dict(), dict(state=dict(hl1="on"))],
                         note=_N_DR, src=ss.src(["TSB §1.23.1", "TSB §1.30.2"]))),
    ),
    # cd06（2行）＝同じ節の続き（ずれは少しずつで気づきにくい）→聞き役
    "cd06": dict(
        t="気づきにくさ", s="少しずつのずれ",
        fig=("m22", dict(view="paper", start=dict(doc="drift", hl1="on"), steps=[dict(state=dict(hl2="on", hl3="on", hl4="on")), dict()],
                         note=_N_DR, src=ss.src(["TSB §1.30.2"]))),
    ),
    # cd09（2行）＝コメントの問い（ed01 の直前・文字だけ）。誰でも気軽に答えられる形（§B3-7b）。「この動画」は画面に出さない
    "cd09": dict(
        t="深い海の底", s="コメント欄で聞かせてください",
        fig=("panel", dict(blocks=[dict(k="問い", t="自分の目で見たいですか", v="もし乗れるとしたら", c=J.AMBER)], cols=1)),
    ),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-15）：写真・映像 終章（3カット）＝映像方針の一覧（了承②）。副題は焼いた絵を原寸で見てから最終に
# ══════════════════════════════════════════════════════════
_AFTSEG = P("lab24011_p71_fig43b")
SPEC.update({
    # cd01（4.7秒）＝聞き役の問い＋答え。ROV 04 の 41.8〜47.32秒（右の端に尾部の横）・等速 → 終章の扉は方眼だけ
    #   🔧 ⑤c'（10-15）：尾部が画に入るのは区間の約半分（途中のコマ 0.2・0.5＝尾部・0.75＝端だけ・尻＝海の底だけ）。替えの区間は無い
    #      （R04 の 0〜8秒は海の底と腕だけ＝原寸の1秒おきのシートで確かめた・尾部の写る 8〜37.3秒は c101・c517・c108 が使う）
    #      ＝副題を区間の全部に合わせる（c101 と同じ名の別の絵も解ける）
    "cd01": ss.vid("cd01", color=1.0, card_mix=0, t="答え合わせ", s="尾部が見つかった海の底（6月22日）"),
    # cd07（7.2秒）＝回収された後ろのチタンの輪（24-011 図43 の下・1320×880）・全面・引く。c607 の FBI 図157 と同じ物＝呼び方をそろえる
    "cd07": dict(photo=_AFTSEG, **ss.mv(_AFTSEG, "out"), side="none", t="安全を先に", s="回収された後ろのチタンの輪（研究所）"),
    # cd08（8.4秒）＝ROV 07 の 18.0〜27.26秒（後ろのドーム）・等速
    "cd08": ss.vid("cd08", color=1.0, t="6月18日の海", s="遠くから近づく後ろのドーム（6月22日）"),   # 🔧 ⑤c'＝c6.py の c602 の注（書き分け）
})
