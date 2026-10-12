# -*- coding: utf-8 -*-
"""第9章　「9分」は、どう分かったか ca01–ca20（20カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/ca.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep21/make_plan21.py` で
  映像方針の一覧 `ref/ep21/eizou_build/list21.tsv`（了承②ずみ・E 0）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット（台本の画は元の予定）。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'ca01': dict(kind='図解',
               plan='台本の画：図 模式 委員会の調べの数（文書の山・話を聞いた人・国の数の札）',
               src='委員会報告 p.xv（`Public Law 107-306, November 27, 2002`・`we have reviewed more than 2.5 million pages of documents and interviewed more than 1,200 individuals in ten countries`）'),
    'ca02': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（FAA のレーダー再生の画面の収録・委員会が使った記録のひとつ）',
               src='委員会報告 p457（`Times assigned to audio transmissions were derived by the Commission from files provided by the FAA and the Northeast Air Defense Sector (NEADS) based on audio time stamps`）'),
    'ca03': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（2003年5月の証言の3つの札）',
               src='委員会報告 p34（`In public testimony before this Commission in May 2003, NORAD officials stated that at 9:16, NEADS received hijack notification of United 93 from the FAA`）'),
    'ca04': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（9:16 の札に×・93便の乗っ取りは 9:28）',
               src='委員会報告 p34（`This statement was incorrect. There was no hijack to report at 9:16. United 93 was proceeding normally at that time`）'),
    'ca05': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（9:24 の札に×）',
               src='委員会報告 p34（`NORAD officials stated that at 9:24, NEADS received notification of the hijacking of American 77`・`NEADS never received notice that American 77 was hijacked`）'),
    'ca06': dict(kind='図解',
               plan='🔧 ⑤b-6 模式 同じ2段の帯に、ラングレーへ発進の命令（9:23）と11便の誤報（9:21）の点（帯に飛んだ線は描かない＝時刻の点で）｜台本の画：図 模式 同じ帯（ラングレー機の線＝実は11便の誤報で飛んだ）',
               src='委員会報告 p34（`The inaccurate accounts created the impression that the Langley scramble was a logical response to an actual hijacked aircraft`）'),
    'ca07': dict(kind='図解',
               plan='🔧 ⑤b-6 模式 同じ2段の帯に「証言のとおりなら14分」の括弧と、記録の1〜2分（9:36→9:37:46）の赤い帯（括弧の札に×を重ねると字に触れる＝2つを並べて比べる）｜台本の画：図 模式 同じ帯（「14分」の札に×）',
               src='委員会報告 p34（`Thus the military did not have 14 minutes to respond to American 77, as testimony to the Commission in May 2003 suggested`）'),
    'ca08': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（「間に合ったように見えた」の札）',
               src='委員会報告 p34（`More than the actual events, inaccurate government accounts of those events made it appear that the military was notified in time to respond to two of the hijackings`）'),
    'ca09': dict(kind='写真',
               plan='P049｜副題：当日の夜のペンタゴン｜動き：右へ流す｜権利：A（米海軍の職務）｜出典の行：米海軍｜台本の画：実写 当日のペンタゴン（米軍の写真・A・別の点＝副題は絵を見て書く）',
               src='運輸省の監察総監の報告 CC-2006-085 p1（`did not investigate whether the inaccurate statements were knowingly false`・`referred to the Department of Defense (DOD) and Department of Transportation (DOT) Inspectors General`）'),
    'ca10': dict(kind='図解',
               plan='🔧 ⑤b-6 模式 箱の図（委員会の報告書→国防総省と運輸省の監察総監→運輸省の2つの答え）＝2006年の報告は時刻の帯に載らない｜台本の画：図 模式 同じ帯（「誤り」の札から「監察総監」の札へ矢印）',
               src='運輸省の監察総監の報告 CC-2006-085 p2（`We did not find evidence to conclude that FAA officials knowingly made false`）・p3（`consider appropriate administrative action for the two current executives who did not act to correct the record with the Commission`）'),
    'ca11': dict(kind='写真',
               plan='🔧 WTC76N｜副題：事件の前の世界貿易センター（1976年・夕暮れ）｜動き：上へ流す｜権利：D（米議会図書館蔵／知られた制限なし）｜出典の行：Balthazar Korab（米議会図書館蔵）｜注：🔧 語りが8:46の時刻＝両棟が燃える写真を置かない。夕暮れ・縦長。⑤b-7：副題を写っているものに（題 Night view・金色に照らされた2つの塔）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 当日の世界貿易センター（A・別の点＝副題は絵を見て書く）',
               src='委員会報告 p7（`At 8:46:40`）・NIST NCSTAR 1 表6-1 印字 p84（`8:46:30`）・NCSTAR 1-6 表6-1 印字 p156（`8:46:26`）'),
    'ca12': dict(kind='図解',
               plan='台本の画：図 模式 同じ3つの値の帯（どれも数秒の幅に並ぶ）',
               src='委員会報告 p454 注39（`Flight Path Study`）・NTSB 11便（`impacted the North tower at approximately 8:46:40`）・NIST（`established from the time stamps in the September 11 telecasts`）'),
    'ca13': dict(kind='図解',
               plan='台本の画：図 模式 記録装置の表（4機それぞれの、操縦室の音声と飛行の記録）',
               src='委員会報告 p456（`The CVRs and FDRs from American 11 and United 175 were not found, and the CVR from American Flight 77 was badly burned and not recoverable`）・p12（`The flight data recorder (also recovered)`）・NTSB 77便 図2（`FDR Pressure Altitude`＝sources §11-1 #4）'),
    'ca14': dict(kind='図解',
               plan='台本の画：図 模式 同じ表（93便の音声の記録装置に印）',
               src="委員会報告 p456（`United 93's cockpit voice recorder recorded the last 31 minutes of sounds from the cockpit`・`A transcript of the CVR recording was prepared by the NTSB and the FBI`）"),
    'ca15': dict(kind='図解',
               plan='台本の画：図 模式 同じ表',
               src='委員会報告 p462（`Commission analysis of FDR, CVR, radar, and impact data`）・sources §5（P200056T＝93便の CVR の逐語・裁判の証拠として公開）'),
    'ca16': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（9:21 の誤報の札＝出どころ不明）',
               src='委員会報告 p26（`We have been unable to identify the source of this mistaken FAA information`）'),
    'ca17': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯',
               src='—'),
    'ca18': dict(kind='文字の頁',
               plan='台本の画：図 p34（文字の頁・2003年の証言の誤りを書いた段落を寄る）',
               src='委員会報告 p34（`This statement was incorrect`）'),
    'ca19': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（4機と、軍に届いた知らせの印をすべて重ねる）',
               src="委員会報告 p31（`the NEADS air defenders had nine minutes' notice on the first hijacked plane, no advance notice on the second, no advance notice on the third, and no advance notice on the fourth`）"),
    'ca20': dict(kind='図解',
               plan='🔧 ⑤b-6 模式 年表（2001年の「この朝」から始まる＝第10章の法律・委員会の年表へつながる）｜台本の画：図 模式 同じ帯（11月の法律の札へつながる）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-13）：図解 第9章（16カット）＋頁（ca02＝RG237 の1コマ）・文字の頁（ca18＝委員会報告 p34）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「「9分」は、どう分かったか」と4字以上同じ並びを見出し・副題に入れない（門番 dup）。人は描かない。
#      録音の逐語・証言の言葉そのものは画面に出さない（項目の名だけ）。割れる時刻（8:46:40・9:37:46・10:03:11）は出典の名（by=True）
#   2段の帯 AX_TESTI＝上は2003年5月の公聴会の証言（p34）・下は委員会が記録で当てた時刻＝ca03〜ca08・ca16・ca17 で使い回す
_ax = ss.ax
_TS, _TR = "2003年の証言", "委員会の記録"
_TN = "上の段は公聴会の証言・下の段は委員会が記録で当てた時刻"
_TREC = ("t916", "t916x", "t924", "t924x", "r928", "r923", "r946", "r936", "s936")   # 9:21 の誤報（r921／r921q）を除いた全部


def _tp(*names):
    return [_ax(n) for n in names]

_FN = "表の形は模式（中身は委員会報告の記録）"
SPEC.update({
    # ca01（2行）＝委員会の調べの規模（序文）。法律で設置 → 2行目で文書・人・国のカード
    "ca01": dict(
        t="調べの規模", s="序文が記す委員会の作業",
        fig=("m21", dict(view="probe", steps=[dict(state=dict(law="on")), dict(state=dict(n="on"))],
                         note="カードの絵は模式（数は委員会報告の序文）", src=ss.src(["委員会報告の序文 p15"]))),
    ),
    # ca02（9.1秒）＝RG237（FAA のレーダーの再生・5-AWA-716-All-4-AC の 37.5秒＝動かない4機の航跡の地図）。額ごと寄る
    "ca02": dict(photo=ss.page("r4"), trim=ss.ptrim("ca02"), bias=ss.pbias("ca02"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="使われた記録", s="FAA のレーダーの記録から再生した4機の航跡"),
    # ca03（3行）＝2段の帯。前置き → 2行目で証言の段を灯す → 3行目で 9:16（93便の知らせ・証言）
    "ca03": dict(
        t="証言と記録", s="NORAD の幹部が述べた時刻",
        fig=("axis", dict(ss.AX_TESTI, steps=[dict(), dict(add=dict(k="lane", lane=_TS, rec="委員会報告 p34")),
                                              dict(add=_ax("t916"), cur="9:16")],
                          note=_TN, src=ss.src(["委員会報告 p34"]))),
    ),
    # ca04（2行）＝9:16 に×（p34「This statement was incorrect」）→ 2行目で 93便の乗っ取りは 9:28（p11）
    "ca04": dict(
        t="誤りの時刻", s="証言の時刻と乗っ取りの時刻",
        fig=("axis", dict(ss.AX_TESTI, past=[_ax("t916", keep=True)], start=dict(cur="9:16"),
                          steps=[dict(add=_ax("t916x")), dict(add=_ax("r928"), cur="9:28")],
                          note=_TN, src=ss.src(["委員会報告 p34", "委員会報告 p11"]))),
    ),
    # ca05（2行）＝9:24（77便の知らせ・証言）→ 2行目で×（p34「also incorrect」）
    "ca05": dict(
        t="もう1つの誤り", s="77便についての証言",
        fig=("axis", dict(ss.AX_TESTI, past=[_ax("t916"), _ax("t916x"), _ax("r928")], start=dict(cur="9:28"),
                          steps=[dict(add=_ax("t924"), cur="9:24"), dict(add=_ax("t924x"))],
                          note=_TN, src=ss.src(["委員会報告 p34"]))),
    ),
    # ca06（2行）＝ラングレーへ発進の命令（9:23・p27）→ 2行目で11便の誤報（9:21・p26）
    "ca06": dict(
        t="発進の理由", s="ラングレーの戦闘機が飛んだわけ",
        fig=("axis", dict(ss.AX_TESTI, past=[_ax("t916"), _ax("t916x"), _ax("t924"), _ax("t924x"), _ax("r928")], start=dict(cur="9:24"),
                          steps=[dict(add=_ax("r923"), cur="9:23"), dict(add=_ax("r921"), cur="9:21")],
                          note=_TN, src=ss.src(["委員会報告 p34", "委員会報告 p26", "委員会報告 p27"]))),
    ),
    # ca07（3行）＝問い → 2行目で「証言のとおりなら14分」（9:24→9:37:46）→ 3行目で記録の1〜2分（9:36→9:37:46・p27・p34）
    "ca07": dict(
        t="備える時間", s="証言の14分と記録の1〜2分",
        fig=("axis", dict(ss.AX_TESTI, past=[_ax("t916"), _ax("t916x"), _ax("t924"), _ax("t924x"), _ax("r928"), _ax("r923"), _ax("r921")],
                          start=dict(cur="9:21"),
                          steps=[dict(), dict(add=[_ax("b14"), _ax("r946")], cur="9:37:46"), dict(add=[_ax("r936"), _ax("s936")], cur="9:36")],
                          note=_TN, src=ss.src(["委員会報告 p34", "委員会報告 p27", "委員会報告 p10"]))),
    ),
    # ca08（2行）＝まとめ（p34）。証言の2つ（×つき）を残し、2行目で証言の段を灯す
    "ca08": dict(
        t="見せた姿", s="間に合ったように見えた説明",
        fig=("axis", dict(ss.AX_TESTI, past=[_ax("t916", keep=True), _ax("t916x", keep=True), _ax("t924", keep=True), _ax("t924x", keep=True),
                                             _ax("r928"), _ax("r923"), _ax("r921"), _ax("r946"), _ax("r936"), _ax("s936")],
                          start=dict(cur="9:36"),
                          steps=[dict(), dict(add=dict(k="lane", lane=_TS, rec="委員会報告 p34"))],
                          note=_TN, src=ss.src(["委員会報告 p34"]))),
    ),
    # ca10（3行）＝🔧 箱の図。2006年の運輸省の監察総監の報告 → わざとの証拠は無い（p2）→ 幹部2人の処分の検討（p3）
    "ca10": dict(
        t="運輸省の答え", s="FAA の職員についての調べ",
        fig=("m21", dict(view="ig", steps=[dict(state=dict(dot="on"), tag=dict(t="2006年の報告", at="yr")), dict(state=dict(r1="on")),
                                           dict(state=dict(r2="on"))],
                         rel=[dict(t="2006年", src="運輸省の監察総監の報告 p1")],
                         note="箱の並びは模式（答えは運輸省の監察総監の報告）", src=ss.src(["運輸省の監察総監の報告 p1"]))),
    ),
    # ca12（3行）＝1機目の衝突の3つの値（割れる時刻の印＝出典の名だけ・どれが正しいとは描かない）。委員会（NTSB の調べ）→ NIST の2つ →
    #   3行目で NIST の値の出どころ（テレビの時刻表示）
    "ca12": dict(
        t="3つの時刻", s="1機目の衝突を記した資料",
        fig=("axis", dict(ss.AX_HIT1, steps=[dict(add=[_ax("sp840"), _ax("ch840")], cur="8:46:40"),
                                             dict(add=[_ax("sp830"), _ax("sp826")], cur="8:46:26"),
                                             dict(add=_ax("ch830"), cur="8:46:30")],
                          note="時刻は資料ごとの記録（どれが正しいかは描かない）",
                          src=ss.src(["委員会報告 p7", "委員会報告 p454", "NIST p7134", "NIST 1-6 p9240"]))),
    ),
    # ca13（2行）＝4機の記録装置の表。読めたもの（93便の2つ・77便の飛行）→ 2行目で見つからず・焼けた（p456）
    "ca13": dict(
        t="機体の記録", s="どの装置が読めたか",
        fig=("m21", dict(view="fdr", steps=[dict(state=dict(st="ok")), dict(state=dict(st="all"))], note=_FN,
                         src=ss.src(["委員会報告 p456", "委員会報告 p12", "NTSB 77便 p4004"]))),
    ),
    # ca14（2行）＝93便の音声の記録装置に印（最後の31分・p456）→ 2行目で書き起こした機関
    "ca14": dict(
        t="93便の音声", s="墜落まで録られた音",
        fig=("m21", dict(view="fdr", start=dict(st="all"),
                         steps=[dict(state=dict(hl93="on"), tag=dict(t="最後の31分の音", at="low")),
                                dict(tag=dict(t="書き起こし：NTSB・FBI", at="low2"))],   # 🔧 試し焼き（原寸）：d の「NTSB と FBI」は 21px の灰色＝要の情報が弱い
                         rel=[dict(t="最後の31分", src="委員会報告 p456")], note=_FN, src=ss.src(["委員会報告 p456"]))),
    ),
    # ca15（3行）＝問い → 2行目で読めた記録に印 → 3行目で報告書と裁判の証拠へ（p462・CVR の逐語＝P200056T）
    "ca15": dict(
        t="残った記録", s="読めた記録の使われ方",
        fig=("m21", dict(view="fdr", start=dict(st="all", hl93="on"),
                         steps=[dict(), dict(state=dict(okhl="on")), dict(state=dict(use="on", court="on"))],
                         note=_FN, src=ss.src(["委員会報告 p462", "CVR p6001"]))),
    ),
    # ca16（2行）＝2段の帯。前置き → 2行目で 9:21 の誤報の出どころは不明（p26）
    "ca16": dict(
        t="分からない所", s="誤った知らせの出どころ",
        fig=("axis", dict(ss.AX_TESTI, past=_tp(*_TREC), start=dict(cur="9:36"),
                          steps=[dict(), dict(add=_ax("r921q"), cur="9:21")],
                          note=_TN, src=ss.src(["委員会報告 p26"]))),
    ),
    # ca17（2行）＝問い → 2行目で記録の段を灯す（分からない所も書き、説明を書き改めた）
    "ca17": dict(
        t="記録で正す", s="分からない所も書いた報告",
        fig=("axis", dict(ss.AX_TESTI, past=_tp(*_TREC, "r921q"), start=dict(cur="9:21"),
                          steps=[dict(), dict(add=dict(k="lane", lane=_TR, rec="委員会報告 p34"))],
                          note=_TN, src=ss.src(["委員会報告 p34", "委員会報告 p26"]))),
    ),
    # ca18（5.2秒）＝委員会報告 p34 の文字の頁（GPO の PDF 52頁）。「This statement was incorrect.」に印（語りの「記録で正した」と同時）
    "ca18": dict(photo=ss.page(34), trim=ss.ptrim("ca18"), bias=ss.pbias("ca18"), panel=True, color=1.0, hl=ss.phl("ca18"),
                 t="報告書の頁", s="証言の誤りを記録で正した段"),
    # ca19（2行）＝その朝の4機と軍への知らせ。1機目は9分前（p20・p21）→ 2行目で残る3機は「知らせ無し」（p31）
    "ca19": dict(
        t="届いた知らせ", s="4機の衝突と軍への知らせ",
        fig=("axis", dict(ss.AX_ALL, steps=[dict(add=[_ax("neads11"), _ax("nine11"), _ax("hit11"), _ax("hit175"), _ax("hit77"),
                                                      _ax("crash93")], cur="8:46:40"),
                                            dict(add=[_ax("nn175"), _ax("nn77"), _ax("nn93")], cur="10:03:11")],
                          note="時刻は委員会報告の記録（衝突と墜落の時刻は資料で割れる＝委員会報告の値）",
                          src=ss.src(["委員会報告 p7", "委員会報告 p8", "委員会報告 p10", "委員会報告 p20", "委員会報告 p30",
                                      "委員会報告 p31"]))),
    ),
    # ca20（1行）＝🔧 年表（2001年の「この朝」から）＝第10章の年表へつながる
    "ca20": dict(
        t="あの朝のあと", s="2001年からの年表",
        fig=("axis", dict(ss.AX_AFTER, steps=[dict(add=_ax("day911", anchor="end"), cur="2001-09-11")],
                          note="年月は記録の値", src=ss.src(["委員会報告 p1"]))),
    ),
})

# ── 🆕 ⑤b-7（2026-10-13）：写真（PLAN＝映像方針の一覧・了承②／書き方は c2.py の ⑤b-7 の注）──
_P049 = P("pen_010911_n_pu293_077")
_WNIT = P("wtc_night_1976")
SPEC.update({
    # ca09（11.6秒）＝夜のペンタゴンの煙（米海軍・奥に議事堂の丸屋根＝説明）・右へ流す
    "ca09": dict(photo=_P049, **ss.mv(_P049, "r"), side="none", t="監察総監へ", s="当日の夜のペンタゴン"),
    # ca11（11.9秒）＝金色に照らされた夕暮れの2つの塔（Korab・1976年・縦長 1920×2908）。🔧 語りが 8:46 の時刻＝燃える写真を置かない。
    #   上へ流す（暗い街並み→塔の上の方）
    "ca11": dict(photo=_WNIT, **ss.mv(_WNIT, "u", span=(0.05, 0.65)), side="none", t="食い違う記録",
                 s="事件の前の世界貿易センター（1976年・夕暮れ）"),
})
