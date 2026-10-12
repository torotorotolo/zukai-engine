# -*- coding: utf-8 -*-
"""第8章　届かなかった命令 c901–c921（21カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c9.py`）。
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
    'c901': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（93便＝10:03:11 墜落・10:07 NEADS が知る）',
               src='委員会報告 p30（`NEADS first received a call about United 93 from the military liaison at Cleveland Center at 10:07`）'),
    'c902': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（10:15 墜落の報せ）',
               src='委員会報告 p30（`NEADS was never able to locate United 93 on radar because it was already in the ground`）・p31（`The time of notification of the crash of United 93 was 10:15`）'),
    'c903': dict(kind='図解',
               plan='🔧 ⑤b-5 模式 NEADS のレーダーの画面（探しても93便が出ない＝「捉えていない」を絵で）｜台本の画：図 模式 同じ帯（「撃墜」の札に×）',
               src='委員会報告 p31（`The NEADS air defenders never located the flight or followed it on their radar scopes. The flight had already crashed by the time they learned it was hijacked`）'),
    'c904': dict(kind='写真',
               plan='WH904｜副題：ホワイトハウスの地下の危機管理室｜動き：ゆっくり寄る｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Courtesy George W. Bush Presidential Library（NARA）｜注：副大統領と国家安全保障担当の補佐官（公職だけ）。日付は副題に書かない｜台本の画：実写 PEOC の写真（ホワイトハウスの地下の危機管理室の副大統領と政府の人たち・NARA・A・撮影の日時は NARA の目録で確かめるまで言わない・全画面・ゆっくり寄る＝副題「ホワイトハウスの地下の危機管理室」（日付は NARA の目録で確かめてから足す））',
               src='委員会報告 p40（`the Vice President arrived in the room shortly before 10:00, perhaps at 9:58`）'),
    'c905': dict(kind='写真',
               plan='WH905｜副題：ホワイトハウスの地下の危機管理室｜動き：右へ流す｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Courtesy George W. Bush Presidential Library（NARA）｜注：副大統領の妻が写る＝✅ 了承②（2026-10-12）そのまま・名前は出さない｜台本の画：実写 PEOC の写真（別の点・同じ断り＝副題「ホワイトハウスの地下の危機管理室」（日付は NARA の目録で確かめてから足す））',
               src='委員会報告 p41（`At some time between 10:10 and 10:15, a military aide told the Vice President and others that the aircraft was 80 miles out`・`The Vice President authorized fighter aircraft to engage the inbound plane`）'),
    'c906': dict(kind='写真',
               plan='WH906｜副題：ホワイトハウスの地下の危機管理室｜動き：ゆっくり引く｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Courtesy George W. Bush Presidential Library（NARA）｜注：副大統領の妻が大きく写る＝✅ 了承②（2026-10-12）そのまま・名前は出さない｜台本の画：実写 PEOC の写真（別の点・同じ断り＝副題「ホワイトハウスの地下の危機管理室」（日付は NARA の目録で確かめてから足す））',
               src='委員会報告 p41（`quick and decisive`）'),
    'c907': dict(kind='図解',
               plan='台本の画：図 模式 ワシントンへ伸びる予測の点線（実際の93便はペンシルベニアで止まっている）',
               src='委員会報告 p41（`The FAA may have been tracking the progress of United 93 on a display that showed its projected path to Washington, not its actual radar return`・`the Secret Service was relying on projections and was not aware the plane was already down in Pennsylvania`）'),
    'c908': dict(kind='写真',
               plan='F16NJ｜副題：上空を警戒するF-16（2001年10月・ニュージャージー州兵）｜動き：右へ流す｜権利：A（米空軍の職務）｜出典の行：米空軍（MSgt Don Taggart）｜注：「首都の上空」は書かない｜台本の画：実写 fighter_dc（首都の上空を警戒する F-16C・2001年10月7日・ニュージャージー州兵＝首都の部隊ではない・A・全画面・右へ流す＝副題「上空を警戒する F-16（2001年10月・ニュージャージー州兵）」）',
               src='委員会報告 p31（`he explicitly instructed the Langley fighters`）・p45（`At 10:10, the pilots over Washington were emphatically told, "negative clearance to shoot."`）'),
    'c909': dict(kind='図解',
               plan='台本の画：図 模式 NORAD の連絡の箱（副大統領から NORAD、NEADS、戦闘機へ）',
               src='委員会報告 p42（`Vice president has cleared to us to intercept tracks of interest and shoot them down if they do not respond`・`NEADS personnel first learned of the shootdown order from this message`）'),
    'c910': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱（NEADS から戦闘機への矢印に×）',
               src='委員会報告 p43（`The NEADS commander told us he did not pass along the order because he was unaware of its ramifications`・`they did not pass the order to the fighters circling Washington and New York because they were unsure how the pilots would, or should, proceed with this guidance`）'),
    'c911': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱（首都の側の「撃ち落とせ」の札と、操縦士の側の「種類と尾翼の番号を確かめよ」の札）',
               src='委員会報告 p43（`while leaders in Washington believed that the fighters above them had been instructed to "take out" hostile aircraft, the only orders actually conveyed to the pilots were to "ID type and tail."`）'),
    'c912': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱',
               src='—'),
    'c913': dict(kind='写真',
               plan='WH913｜副題：当日の夜、国家安全保障会議に出る大統領｜動き：ゆっくり寄る｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Eric Draper（Courtesy George W. Bush Presidential Library）｜注：副大統領がいるかは絵で決められない＝副題に書かない｜台本の画：実写 当日の夜の大統領と副大統領（ホワイトハウスの写真係・A・全画面・ゆっくり引く＝副題「当日の夜のホワイトハウス」）',
               src="委員会報告 p44（`The Vice President was mistaken in his belief that shootdown authorization had been passed to the pilots flying at NORAD's direction`）"),
    'c914': dict(kind='写真',
               plan='WH914｜副題：当日、大統領専用機の機内｜動き：左へ流す｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Eric Draper（Courtesy George W. Bush Presidential Library）｜注：窓の外の護衛の F-16 を見る大統領と側近＝電話は写らない｜台本の画：実写 大統領専用機の機内の大統領（電話の写っていない点）（別の点・ホワイトハウスの写真係・A・撮影の時刻は書かない＝副題「当日、大統領専用機の機内」）',
               src='委員会報告 p40（`The Vice President stated that he called the President to discuss the rules of engagement`・`The President said he remembered such a conversation`）・p41（`He told us he based this authorization on his earlier conversation with the President`）'),
    'c915': dict(kind='図解',
               plan='台本の画：図 模式 同じ（電話の線に「記録なし」の札）',
               src='委員会報告 p41（`there is no documentary evidence for this call, but the relevant sources are incomplete`）'),
    'c916': dict(kind='図解',
               plan='🔧 ⑤b-5 模式 首都の上を回る2組の輪（ワシントンの地図に重ねると基図の札と点にかかった）｜台本の画：図 模式 首都の上の2組の戦闘機（ラングレーと、アンドルーズの州兵）',
               src='委員会報告 p44（`By 10:45 there was, however, another set of fighters circling Washington that had entirely different rules of engagement`・`launched out of Andrews Air Force Base in Maryland in response to information passed to them by the Secret Service`・`the decision to shoot rests in the cockpit`）'),
    'c917': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（10:03:11 墜落・10:10 から 10:15 許可・10:31 NEADS へ）',
               src='—'),
    'c918': dict(kind='図解',
               plan='🔧 ⑤b-5 模式 撃ち落とすのに要る3つ（委員会報告 p45）と、NORAD の幹部・委員会の言い分｜台本の画：図 模式 同じ帯',
               src='委員会報告 p45（`NORAD officials have maintained that they would have intercepted and shot down United 93. We are not so sure.`）'),
    'c919': dict(kind='図解',
               plan='🔧 ⑤b-5 模式 撃ち落とすのに要る3つ（見つけて追う・撃つ許可・命令を渡す＝委員会報告 p45 の3つ）に×｜台本の画：図 模式 同じ帯（見つける・追う・命令を渡す、の3つの箱が空白）',
               src='委員会報告 p45（`to locate the flight, receive authorization to shoot it down, and communicate the order to the pilots`・`did not know where United 93 was located, and did not have shootdown authorization`）'),
    'c920': dict(kind='写真',
               plan='WH920｜副題：当日の午後、ネブラスカ州の空軍基地（画面越しの会議）｜動き：ゆっくり寄る｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Eric Draper（Courtesy George W. Bush Presidential Library）｜台本の画：実写 オファット空軍基地での会議（ホワイトハウスの写真係・当日の午後・A・全画面＝副題「当日の午後、ネブラスカ州の空軍基地」）',
               src='委員会報告 p326（`Air Force One arrived at Offutt at 2:50 P.M.`・`At about 3:15, President Bush met with his principal advisers through a secure video teleconference`）'),
    'c921': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（その朝の4機と命令の時刻をすべて重ねる）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-10-12）：図解 第8章（14カット）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「届かなかった命令」と4字以上同じ並び（「なかった」「った命令」ほか）を見出し・副題に入れない（門番 dup）。
#      人は描かない。10:03:11（墜落）は資料で割れる時刻＝時間の帯の点に出典の名（by=True）・時計の札にしない
_CM = "箱の並びは模式（流れの順は委員会報告の記録）"   # ⚠️ 門番 wording I：注に「p42」の形の頁を書かない（頁は出典の行）
_ND = "箱の並びは模式（3つは委員会報告の記録）"
SPEC.update({
    # c901（3行）＝時間の帯（撃墜の許可の寄り）。問い → 10:07 NEADS へ（p30）→ 3行目＝軍の連絡係から（字幕だけ）
    "c901": dict(
        t="知った時刻", s="NEADS に入った最初の連絡",
        fig=("axis", dict(ss.AX_ORD, steps=[dict(), dict(add=ss.ax("neads93"), cur="10:07"), dict()],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p30"]))),
    ),
    # c902（3行）＝同じ帯。墜落（割れる時刻）と約4分 → 2行目＝レーダーで見つけられない（字幕だけ）→ 3行目で 10:15 墜落の知らせ（p31）
    "c902": dict(
        t="約4分の差", s="墜落と知らせのあいだ",
        fig=("axis", dict(ss.AX_ORD, past=[ss.ax("neads93")], start=dict(cur="10:07"),
                          steps=[dict(add=[ss.ax("crash93"), ss.ax("gap4")]), dict(), dict(add=ss.ax("rpt15"), cur="10:15")],
                          note="時刻は委員会報告の記録（墜落の時刻は資料で割れる＝委員会報告の値）",
                          src=ss.src(["委員会報告 p30", "委員会報告 p31"]))),
    ),
    # c903（3行）＝🔧 NEADS の画面（模式）。問い → 一度も捉えていない → 知ったときには地上に（p31）
    "c903": dict(
        t="映らない便", s="撃墜の話と委員会の答え",
        fig=("m21", dict(view="scope", start=dict(who="neads", dots="on"),
                         steps=[dict(), dict(state=dict(search="s1"), tag=dict(t="93便を一度も捉えず", at="search")),
                                dict(state=dict(search="s2"), tag=dict(t="知ったときには地上に", at="news"))],
                         rel=[dict(t="93便", src="委員会報告 p31")], note="画面の形と点は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p30", "委員会報告 p31"]))),
    ),
    # c907（2行）＝北東部の地図。実際の93便（シャンクスビルで止まる）→ 2行目で首都への予測の線（p41）
    "c907": dict(
        t="実際と予測", s="シークレットサービスの見方",   # ⚠️ 門番 dup：「予測の線」は注（93便の線と予測の線は模式）の語
        fig=("m21", dict(view="ne",
                         steps=[dict(state=dict(r93="on", shk="on"), tag=dict(t="実際の93便", at="r93")),
                                dict(state=dict(proj="on"), tag=dict(t="首都への予測", at="proj"))],
                         rel=[dict(t="93便", src="委員会報告 p30")],
                         note="陸の形は Natural Earth・93便の線と予測の線は模式（NTSB 93便の図1の見当）",
                         src=ss.src(["委員会報告 p41", "委員会報告 p30"]))),
    ),
    # c909（2行）＝撃墜の許可の流れ。10:31 NEADS まで灯す（p42）→ 2行目で NORAD の文字の連絡
    "c909": dict(
        t="届いた許可", s="許可が流れた順",
        fig=("m21", dict(view="cmd",
                         steps=[dict(state=dict(lit="3"), tag=dict(t="10:31", d="NEADS に許可が届く", at="low1")),
                                dict(state=dict(msg="on"), tag=dict(t="NORAD の文字の連絡", at="msg"))],
                         rel=[dict(t="10:31", src="委員会報告 p42")], note=_CM, src=ss.src(["委員会報告 p42"]))),
    ),
    # c910（3行）＝NEADS から戦闘機への矢印に×（p43）→ 指揮官 → 現場の将校2人
    "c910": dict(
        t="流れない許可", s="NEADS から戦闘機へ",
        fig=("m21", dict(view="cmd", start=dict(lit="3", msg="on"),
                         steps=[dict(state=dict(x="on"), tag=dict(t="下へ流さず", at="xt")),
                                dict(tag=dict(t="NEADS の指揮官", d="影響が分からない", at="low1")),
                                dict(tag=dict(t="現場の将校2人も", d="伝えず", at="low2"))],
                         rel=[dict(t="2人", src="委員会報告 p43")], note=_CM, src=ss.src(["委員会報告 p43"]))),
    ),
    # c911（2行）＝首都の側が思っていた命令 → 2行目で操縦士に届いた命令（p43）
    "c911": dict(
        t="2つの命令", s="首都と空の上",
        fig=("m21", dict(view="cmd", start=dict(lit="3", msg="on", x="on"),
                         steps=[dict(state=dict(cap="on")), dict(state=dict(plt="on"))], note=_CM, src=ss.src(["委員会報告 p43"]))),
    ),
    # c912（2行）＝問い → 2行目で食い違いの印
    "c912": dict(
        t="命令のずれ", s="首都の考えと操縦士の命令",
        fig=("m21", dict(view="cmd", start=dict(lit="3", msg="on", x="on", cap="on", plt="on"),
                         steps=[dict(), dict(state=dict(neq="on"))], note=_CM, src=ss.src(["委員会報告 p43"]))),
    ),
    # c915（2行）＝電話の線（副大統領と大統領）。記録なし（p41）→ 2行目で資料は不完全
    "c915": dict(
        t="無い裏づけ", s="許可の前にあったという電話",
        fig=("m21", dict(view="call", start=dict(pair="vp"),
                         steps=[dict(state=dict(nolog="on"), tag=dict(t="記録なし", at="time")),
                                dict(tag=dict(t="資料は不完全（委員会）", at="first"))],
                         note="人は描かない・建物と機は模式", src=ss.src(["委員会報告 p40", "委員会報告 p41"]))),
    ),
    # c916（2行）＝🔧 首都の上を回る2組の戦闘機（模式）。10:45 2組目（撃つかは操縦士）→ 2行目でアンドルーズ基地の州兵（p44）
    "c916": dict(
        t="2組の戦闘機", s="首都の上の空",
        fig=("m21", dict(view="sky", start=dict(o1="on"),
                         steps=[dict(state=dict(o2="on"), tag=dict(t="10:45 2組目", d="撃つかは操縦士が決める", at="b")),
                                dict(state=dict(adw="on"))],
                         rel=[dict(t="10:45", src="委員会報告 p44"), dict(t="2組目", src="委員会報告 p44")],
                         note="輪の位置と大きさは模式（委員会報告は「首都の上を回る」とだけ）", src=ss.src(["委員会報告 p44"]))),
    ),
    # c917（2行）＝時間の帯。問い（墜落は前のカットの続き）→ 許可（10:10〜10:15）→ 2行目で 10:31 NEADS へ
    "c917": dict(
        t="許可の時刻", s="墜落のあとの許可",
        fig=("axis", dict(ss.AX_ORD, past=[ss.ax("crash93")], start=dict(cur="10:03:11"),
                          steps=[dict(add=ss.ax("auth"), cur="10:15"), dict(add=ss.ax("neads31"), cur="10:31")],
                          note="時刻は委員会報告の記録（墜落の時刻は資料で割れる＝委員会報告の値）",
                          src=ss.src(["委員会報告 p30", "委員会報告 p41", "委員会報告 p42"]))),
    ),
    # c918（2行）＝🔧 撃ち落とすのに要る3つ（模式）。NORAD の幹部の言い分 → 2行目で委員会の答え（p45）
    "c918": dict(
        t="割れる見方", s="追いつけたかどうか",
        fig=("m21", dict(view="need",
                         steps=[dict(tag=dict(t="NORAD の幹部", d="撃墜できた", at="l")), dict(tag=dict(t="委員会", d="言い切れない", at="r"))],
                         note=_ND, src=ss.src(["委員会報告 p45"]))),
    ),
    # c919（2行）＝要る3つを灯す → 2行目で3つとも×（p45）
    "c919": dict(
        t="3つの条件", s="委員会が挙げた3つ",   # ⚠️ 門番 dup：「撃ち落とすのに要ること」は左上の見え方の名
        fig=("m21", dict(view="need",
                         steps=[dict(state=dict(hl="on")), dict(state=dict(x="on"), tag=dict(t="その朝はどれもできず", at="low"))],
                         note=_ND, src=ss.src(["委員会報告 p45"]))),
    ),
    # c921（3行）＝時間の帯（その朝の4機と命令）。4機の衝突と墜落（割れる時刻＝出典の名）→ NEADS に許可 → 3行目（字幕だけ）
    #   ⚠️ 門番 axis：許可の帯（10:10〜10:15）も足すと札が3段目へ上がった＝c917 で見せた帯は外す
    "c921": dict(
        t="重なる時刻", s="その朝の4機と命令",
        fig=("axis", dict(ss.AX_ALL,
                          steps=[dict(add=[ss.ax("hit11", anchor="end"), ss.ax("hit175"), ss.ax("hit77"), ss.ax("crash93")], cur="10:03:11"),
                                 dict(add=ss.ax("neads31", anchor="start"), cur="10:31"), dict()],   # ⚠️ 左へ振ると 10:03:11 の縦の線が札を貫いた
                          note="時刻は委員会報告の記録（衝突と墜落の時刻は資料で割れる＝委員会報告の値）",
                          src=ss.src(["委員会報告 p7", "委員会報告 p8", "委員会報告 p10", "委員会報告 p30", "委員会報告 p42"]))),
    ),
})
