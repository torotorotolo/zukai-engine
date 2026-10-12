# -*- coding: utf-8 -*-
"""第7章　4機目　93便の35分 c801–c835（35カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c8.py`）。
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
    'c801': dict(kind='写真',
               plan='EWR｜副題：ニューアーク空港の93便の搭乗口（2006年）｜動き：上へ流す｜権利：C（PD-self＝撮影者の献呈）｜出典の行：Tshevlin（パブリックドメイン）｜注：17番搭乗口の上の旗｜台本の画：実写 ニューアーク空港の93便の搭乗口の記念の旗（後年・C・全画面・ゆっくり寄る＝副題「現在のニューアーク空港・93便の搭乗口」）',
               src="委員会報告 p10（`As United 93 left Newark, the flight's crew members were unaware of the hijacking of American 11`）"),
    'c802': dict(kind='図・写真の頁',
               plan='見る向き：上から｜注：NTSB 93便の経路｜台本の画：図 NTSB 93便の経路（PDF p3 の地図をなぞる・ニューアークから西へ）',
               src='委員会報告 p10（`Around 9:00, the FAA, American, and United were facing the staggering realization of apparent multiple hijackings`）'),
    'c803': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の画面に届く文字の連絡（人は描かない）',
               src='委員会報告 p11（`Beware any cockpit intrusion`）'),
    'c804': dict(kind='図解',
               plan='台本の画：図 模式 同じ（93便の画面に届く＝9:24）',
               src='委員会報告 p11（`warning to United 93 was received in the cockpit`）'),
    'c805': dict(kind='図解',
               plan='台本の画：図 模式 同じ（返信の文字＝字幕だけ）',
               src='委員会報告 p11（`responded with a note of puzzlement`・`confirm latest mssg plz`）'),
    'c806': dict(kind='図・写真の頁',
               plan='見る向き：横から｜合図：🔁 上から→横から（前の図 c802）＝左上に見る向きの札・替わる瞬間に「横から見ると」｜注：NTSB 93便の高度｜台本の画：図 NTSB 93便の高度（9:28 の小さな降下の印）',
               src='委員会報告 p11（`The hijackers attacked at 9:28`・`While traveling 35,000 feet above eastern Ohio, United 93 suddenly dropped 700 feet`）・NTSB 93便（`a brief descent of about 600 feet starting at 9:28`）'),
    'c807': dict(kind='図解',
               plan='台本の画：図 模式 管制の無線（クリーブランド・センターと93便を結ぶ線）',
               src='委員会報告 p11（`could be heard declaring "Mayday" amid the sounds of a physical struggle in the cockpit`・`Hey get out of here`）'),
    'c808': dict(kind='図解',
               plan='台本の画：図 模式 同じ（機内の放送が無線に流れる線）',
               src='委員会報告 p12（`made or attempted to make the following announcement to the passengers`・`We have a bomb on board`）・p28（`At 9:32, a third radio transmission came over the frequency`）・p13（`we believe the bombs were probably fake`）'),
    'c809': dict(kind='図・写真の頁',
               plan='見る向き：上から｜合図：🔁 横から→上から（前の図 c806）＝左上に見る向きの札・替わる瞬間に「上から見ると」｜台本の画：図 NTSB 93便の経路（オハイオの上で向きを変え、東へ戻る線）',
               src="委員会報告 p12（`instructed the plane's autopilot to turn the aircraft around and head east`）"),
    'c810': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（93便＝9:28 乗っ取り・9:34 FAA 本部へ）',
               src='委員会報告 p28（`By 9:34, word of the hijacking had reached FAA headquarters`）'),
    'c811': dict(kind='図解',
               plan='台本の画：図 模式 手順の段（FAA 本部から国防総省への矢印が途中で止まる）',
               src='委員会報告 p29（`At 9:49, 13 minutes after Cleveland Center had asked about getting military help, the Command Center suggested that someone at headquarters should decide whether to request military assistance`）'),
    'c812': dict(kind='図解',
               plan='台本の画：図 模式 同じ（矢印に×）',
               src='委員会報告 p30（`no one from FAA headquarters requested military assistance regarding United 93. Nor did any manager at FAA headquarters pass any of the information it had about United 93 to the military`）'),
    'c813': dict(kind='図解',
               plan='🔧 ⑤b-5 模式 管制のレーダーの画面（9:41 札が消える・点を追い続ける＝帯より「札は消えたが点は追えた」が見える）｜台本の画：図 模式 時間の帯（9:41 トランスポンダの印）',
               src='NTSB 93便（`stopped receiving transponder returns`）・委員会報告 p29（`The controller located it on primary radar`・`tracked the flight as it turned east, then south`）'),
    'c814': dict(kind='図解',
               plan='台本の画：図 模式 機内の座席（後ろの席と座席の背の電話＝人は描かない）',
               src='国立公園局（`thirty-seven phone calls were placed from on board Flight 93`・`Thirty-five of these calls were made on the Airfones located on the back of the seats in the last nine rows of the plane`）'),
    'c815': dict(kind='図解',
               plan='台本の画：図 模式 同じ（後ろの9列に印）',
               src='国立公園局（`Unless noted, the calls were made on Airfones`・`used her cell phone to call`・`used a cell phone to dial 911 and was connected for 70 seconds`）'),
    'c816': dict(kind='図解',
               plan='台本の画：図 模式 地上の側（家族・航空会社・当局の3つの箱）',
               src="委員会報告 p13（`During at least five of the passengers' phone calls, information was shared about the attacks that had occurred earlier that morning at the World Trade Center`）"),
    'c817': dict(kind='図解',
               plan='台本の画：図 模式 機内の座席（話し合いの印）',
               src='委員会報告 p13（`Five calls described the intent of passengers and surviving crew members to revolt against the hijackers`・`According to one call, they voted on whether to rush the terrorists in an attempt to retake the plane`）'),
    'c818': dict(kind='図解',
               plan='台本の画：図 模式 同じ',
               src='委員会報告 p13（`They decided, and acted`）'),
    'c819': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（9:57 反撃）',
               src='委員会報告 p13（`At 9:57, the passenger assault began`・`Several passengers had terminated phone calls with loved ones in order to join the revolt`）'),
    'c820': dict(kind='図解',
               plan='台本の画：図 模式 機の向き（左右に傾く記号＝人は描かない）',
               src='委員会報告 p13（`immediately began to roll the airplane to the left and right, attempting to knock the passengers off balance`・`But the assault was sustained`）'),
    'c821': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の扉（扉の内と外＝人は描かない）',
               src='委員会報告 p13（`told another hijacker in the cockpit to block the door`）'),
    'c822': dict(kind='図解',
               plan='台本の画：図 模式 同じ扉（扉の外からの音の波）',
               src='委員会報告 p13（`The cockpit voice recorder captured the sounds of the passenger assault muffled by the intervening cockpit door`）'),
    'c823': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の音声の時刻の帯（10:00:25・10:00:42＝字幕だけ・画面に大きく出さない）',
               src="CVR p7（`In the cockpit. If we don't, we'll die.`）・委員会報告 p14（`a passenger in the background said`）"),
    'c824': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯',
               src='CVR p7（`Roll it.`）・委員会報告 p14（`Sixteen seconds later, a passenger yelled, "Roll it!"`）'),
    'c825': dict(kind='図解',
               plan='台本の画：図 模式 機の向き（傾きが止まる記号）',
               src='委員会報告 p14（`stopped the violent maneuvers at about 10:01:00`）'),
    'c826': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（10:02 前後）',
               src='委員会報告 p14（`The hijackers remained at the controls but must have judged that the passengers were only seconds from overcoming them`・`The airplane headed down`）'),
    'c827': dict(kind='写真',
               plan='SHANK15｜副題：現在の93便の墜落現場（追悼の場・2015年）｜動き：ゆっくり引く｜権利：F（CC BY 3.0）｜出典の行：Ron Shawley（CC BY 3.0）｜注：⑤b-7：2倍で測った＝来訪者は右端の遠く（顔 約4px）の遠景＝モザイク不要｜台本の画：実写 shanksville_day（ペンシルベニア州シャンクスビルの93便の追悼の場・2015年・F・全画面・来訪者は顔だけモザイク・ゆっくり引く＝副題「現在の93便の墜落現場（追悼の場）」）',
               src="委員会報告 p30（`United 93 crashed in Pennsylvania at 10:03:11, 125 miles from Washington, D.C.`）・p14（`about 20 minutes' flying time from Washington, D.C.`）"),
    'c828': dict(kind='写真',
               plan='MEM24A｜副題：現在の93便の墜落現場（追悼の場・2024年の空撮）｜動き：右へ流す｜権利：C（CC0）｜出典の行：Designism（CC0）｜注：CC0｜台本の画：実写 93便の追悼の場（別の点・後年・全画面・右へ流す＝副題「現在の93便の墜落現場（追悼の場）」）',
               src='記念館（`40 people were killed on Flight 93`）'),
    'c829': dict(kind='写真',
               plan='MEM15｜副題：現在の93便の追悼の場（2015年）｜動き：左へ流す｜権利：F（CC BY 3.0）｜出典の行：Ron Shawley（CC BY 3.0）｜注：名前の壁は写らない｜台本の画：実写 93便の追悼の場（別の点・後年・名前の壁は写さない＝副題「現在の93便の追悼の場」）',
               src='委員会報告 p14（`symbols of the American Republic, the Capitol or the White House`）'),
    'c830': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（9:28 から 10:03 まで＝35分）',
               src='委員会報告 p14（`He was defeated by the alerted, unarmed passengers of United 93`）'),
    'c831': dict(kind='図解',
               plan='🔧 ⑤b-5 模式 操縦室の扉の内と外（扉に「？」・操縦は犯人のまま＝「操縦室に入ったか」の問いに帯は答えない）｜台本の画：図 模式 同じ帯',
               src='—'),
    'c832': dict(kind='図解',
               plan="🔧 ⑤b-5 模式 地上で聞かれた言葉の出どころ（機内の電話→電話会社の係員→AP 通信の記事）＝言葉の札は出さない（機内の電話の言葉＝字幕だけ）｜台本の画：図 模式 操縦室の音声の時刻の帯（「Let's roll」の札に「電話の向こうで聞かれた言葉」）",
               src="AP（`Let's roll`・`leaving the line open. It was then that the operator heard his words`）"),
    'c833': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯',
               src='CVR p7（`Roll it.`）'),
    'c834': dict(kind='図解',
               plan='🔧 ⑤b-5 模式 ワシントンの地図（議事堂とホワイトハウスに輪＝委員会の見立ての2か所）｜台本の画：図 模式 同じ帯',
               src='委員会報告 p45（`We are sure that the nation owes a debt to the passengers of United 93`・`Their actions saved the lives of countless others, and may have saved either the Capitol or the White House from destruction`）'),
    'c835': dict(kind='図解',
               plan='台本の画：図 模式 4機の行き先の地図（3つの印と、野原の印）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-10-12）：図解 第7章（28カット）＋頁3（c802・c809＝NTSB 93便の図1・c806＝図2）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「4機目　93便の35分」と4字以上同じ並び（「93便の」「便の35」ほか）を見出し・副題に入れない（門番 dup）。人は描かない・
#      操縦室の音声の記録（CVR）の逐語と機内の電話の言葉は画面に出さない（語りと字幕だけ＝「Let's roll」「Roll it」も札にしない）。
#      見る向き：c802（上から）→ c806（横から＝副題の頭「横から見ると」）→ c809（上から＝副題の頭「上から見ると」）
_W93 = "陸の形は Natural Earth・93便の線と予測の線は模式（NTSB 93便の図1の見当）"
_CB = "人は描かない・座席の並びは模式（ボーイング757 の普通席 3-3）"
_CV = "人は描かない・波の形と印の位置は模式"      # ⚠️ 門番 dup：「（時刻は字幕）」は制作の用語
_AC = "人は描かない・便の並びは模式（便の数は委員会報告の記録）"   # ⚠️ 門番 wording I：注に「p11」の形の頁を書かない（頁は出典の行）
SPEC.update({
    # c802（6.2秒）＝NTSB 93便の飛行経路の調べ PDF 3頁（Figure 1・横倒しのスキャンを正立）。ニューアーク（A）から西へ
    "c802": dict(photo=ss.page(5003), trim=ss.ptrim("c802"), bias=ss.pbias("c802"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="西への航跡", s="NTSB の飛行経路の調べ（2002年）の図1"),
    # c803（2行）＝運航管理から受け持つ16便へ文字の警告（9:19・p11）。2行目＝警告の文（字幕だけ）
    "c803": dict(
        t="文字の警告", s="9時19分に始めた連絡",
        fig=("m21", dict(view="acars", steps=[dict(state=dict(send="on"), tag=dict(t="9:19", d="受け持つ便へ送り始める", at="time")), dict()],
                         rel=[dict(t="9:19", src="委員会報告 p11"), dict(t="16便", src="委員会報告 p11")],
                         note=_AC, src=ss.src(["委員会報告 p11"]))),
    ),
    # c804（2行）＝9:24 93便の操縦室に届く（p11）→ 2行目＝問い
    "c804": dict(
        t="届いた警告", s="4機目の操縦室へ",
        fig=("m21", dict(view="acars", start=dict(send="on"),
                         steps=[dict(state=dict(recv93="on"), tag=dict(t="9:24", at="t2")), dict()],
                         rel=[dict(t="9:24", src="委員会報告 p11")], note=_AC,
                         src=ss.src(["委員会報告 p11"]))),
    ),
    # c805（2行）＝9:26 返信（p11）→ 2行目＝返信の文（字幕だけ）
    "c805": dict(
        t="戸惑う返信", s="9時26分の返事",
        fig=("m21", dict(view="acars", start=dict(send="on", recv93="on"),
                         steps=[dict(state=dict(reply="on"), tag=dict(t="9:26", d="機長からの返信", at="time")), dict()],
                         rel=[dict(t="9:26", src="委員会報告 p11")], note=_AC,
                         src=ss.src(["委員会報告 p11"]))),
    ),
    # c806（10.3秒）＝NTSB 93便 PDF 4頁（Figure 2・高度）。🔁 上から→横から＝副題の頭「横から見ると」。点 C＝9:28 の小さな降下
    "c806": dict(photo=ss.page(5004), trim=ss.ptrim("c806"), bias=ss.pbias("c806"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="小さな降下", s="横から見ると：NTSB の調べの図2"),
    # c807（2行）＝クリーブランド・センターの無線。9:28 1つ目の無線 → 2つ目の無線（p11）。言葉は字幕だけ
    "c807": dict(
        t="2つの無線", s="クリーブランドに届いた声",
        fig=("m21", dict(view="radio", start=dict(ctr="cle"),
                         steps=[dict(state=dict(v1="on"), tag=dict(t="9:28", d="機からの1つ目の無線", at="time")),
                                dict(state=dict(v2="on"), tag=dict(t="2つ目の無線", at="v2"))],
                         rel=[dict(t="9:28", src="委員会報告 p11"), dict(t="1つ目・2つ目", src="委員会報告 p11")],
                         note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p11"]))),
    ),
    # c808（3行）＝9:32 機内の放送のつもりの声が無線に流れる（p28）→ 2行目＝言葉（字幕だけ）→ 3行目＝爆弾はおそらく偽物（p13）
    "c808": dict(
        t="機内の放送", s="管制にも聞こえた声",
        fig=("m21", dict(view="radio", start=dict(ctr="cle", v1="on", v2="on"),
                         steps=[dict(state=dict(pa="on"), tag=dict(t="9:32", d="乗客へ向けたつもりの放送", at="time")), dict(),
                                dict(tag=dict(t="爆弾はおそらく偽物", d="委員会の見立て", at="v2"))],
                         rel=[dict(t="9:32", src="委員会報告 p28")], note="人は描かない・機と線は模式",
                         src=ss.src(["委員会報告 p12", "委員会報告 p28", "委員会報告 p13"]))),
    ),
    # c809（9.0秒）＝NTSB 93便 PDF 3頁（Figure 1）の枠の中（向きを変えた E の辺りが左）。🔁 横から→上から＝副題の頭「上から見ると」
    "c809": dict(photo=ss.page(5003), trim=ss.ptrim("c809"), bias=ss.pbias("c809"), panel=True, color=1.0, fmove=ss.fm("l"),
                 t="引き返す線", s="上から見ると：NTSB の調べの図1（左が向きを変えた所）"),
    # c810（2行）＝時間の帯（93便の寄り）。9:28 乗っ取り → 9:34 FAA の本部へ（p28）→ 2行目＝問い
    "c810": dict(
        t="本部へ届く", s="FAA の中の知らせ",
        fig=("axis", dict(ss.AX_93, past=[ss.ax("hj93")], start=dict(cur="9:28"),
                          steps=[dict(add=ss.ax("hq93"), cur="9:34"), dict()],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p11", "委員会報告 p28"]))),
    ),
    # c811（2行）＝手順の段（クリーブランド・センター）。9:49 本部まで灯す → 2行目で本部から先に「？」（p29）
    "c811": dict(
        t="促しただけ", s="コマンドセンターの動き",
        fig=("m21", dict(view="chain", start=dict(who="cle"),
                         steps=[dict(state=dict(lit="3"), tag=dict(t="9:49", d="本部で決めるよう促す", at="tl")), dict(state=dict(hqq="on"))],
                         rel=[dict(t="9:49", src="委員会報告 p29")], note="段の形は模式", src=ss.src(["委員会報告 p28", "委員会報告 p29"]))),
    ),
    # c812（2行）＝本部から軍への矢印に×（p30）→ 2行目で知らせも渡さず
    "c812": dict(
        t="渡らない知らせ", s="本部から軍へ",
        fig=("m21", dict(view="chain", start=dict(who="cle", lit="3", hqq="on"),
                         steps=[dict(state=dict(hqx="on"), tag=dict(t="軍へ頼まず", at="hqx")),
                                dict(tag=dict(t="93便の知らせも渡さず", at="br"))],
                         rel=[dict(t="93便", src="委員会報告 p30")], note="段の形は模式", src=ss.src(["委員会報告 p30"]))),
    ),
    # c813（2行）＝🔧 管制のレーダーの画面（模式）。9:41 札が消える（p29）→ 2行目で点を追い続ける（p29「primary radar」）
    "c813": dict(
        t="札だけ消える", s="クリーブランドの管制官の画面",
        fig=("m21", dict(view="scope", start=dict(block="on"),
                         steps=[dict(state=dict(block="off"), tag=dict(t="9:41", d="トランスポンダが切られる", at="time")),
                                dict(tag=dict(t="点を追い続ける", at="dot", to="blip"))],
                         rel=[dict(t="9:41", src="委員会報告 p29")], note="画面の形と点は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p29"]))),
    ),
    # c814（3行）＝上から見た機内（757）。地上へ電話 → 37本 → 35本は座席の背の電話（後ろの9列に電話の印）
    "c814": dict(
        t="機内の電話", s="乗客と乗員がかけた電話",
        fig=("m21", dict(view="cabin", start=dict(plane="757"),
                         steps=[dict(state=dict(calls="on"), tag=dict(t="機内から地上へ", at="a")), dict(tag=dict(t="37本（FBI）", at="b")),
                                dict(state=dict(fones="on"), tag=dict(t="35本：座席の背の電話", at="r"))],
                         rel=[dict(t="37本", src="国立公園局"), dict(t="35本", src="国立公園局")], note=_CB, src=ss.src(["国立公園局"]))),
    ),
    # c815（2行）＝問い → 2行目で携帯電話2本・後ろの9列の枠
    "c815": dict(
        t="つながった電話", s="座席の背の電話の場所",
        fig=("m21", dict(view="cabin", start=dict(plane="757", calls="on", fones="on"),
                         steps=[dict(), dict(state=dict(rear9="on"), tag=[dict(t="携帯電話：2本", at="a"), dict(t="後ろの9列", at="r")])],
                         rel=[dict(t="2本", src="国立公園局"), dict(t="9列", src="国立公園局")], note=_CB, src=ss.src(["国立公園局"]))),
    ),
    # c816（2行）＝機内の電話と地上の3つの箱。少なくとも5本で世界貿易センターのこと → 2行目で機内に伝わる（p13）
    "c816": dict(
        t="地上から機内へ", s="電話で伝わった朝の出来事",
        fig=("m21", dict(view="ground",
                         steps=[dict(state=dict(calls="on"), tag=dict(t="少なくとも5本", d="世界貿易センターのこと", at="a")),
                                dict(state=dict(back="on"), tag=dict(t="機内に伝わる", at="b"))],
                         rel=[dict(t="5本", src="委員会報告 p13")], note="人は描かない・箱の並びは模式", src=ss.src(["委員会報告 p13"]))),
    ),
    # c817（3行）＝問い → 5本：反撃するつもり → 1本：決をとった（p13）
    "c817": dict(
        t="反撃の相談", s="電話が伝えた機内のようす",
        fig=("m21", dict(view="cabin", start=dict(plane="757", fones="on"),
                         steps=[dict(), dict(tag=dict(t="5本：反撃するつもり", at="a")),
                                dict(state=dict(vote="on"), tag=dict(t="1本：決をとった", at="r"))],
                         rel=[dict(t="5本", src="委員会報告 p13"), dict(t="1本", src="委員会報告 p13")], note=_CB,
                         src=ss.src(["委員会報告 p13"]))),
    ),
    # c818（1行）＝決めて、動いた（p13）＝前（操縦室の扉）へ向かう矢印
    "c818": dict(
        t="決めて動く", s="委員会の短い言葉",
        fig=("m21", dict(view="cabin", start=dict(plane="757", fones="on", vote="on"), steps=[dict(state=dict(rush="on"))],
                         note=_CB, src=ss.src(["委員会報告 p13"]))),
    ),
    # c819（2行）＝時間の帯（93便の寄り）。9:57 乗客の反撃（p13）→ 2行目＝電話を切って加わる（字幕だけ）
    "c819": dict(
        t="反撃の始まり", s="9時57分の機内",
        fig=("axis", dict(ss.AX_93, past=[ss.ax("hj93"), ss.ax("hq93")], start=dict(cur="9:34"),
                          steps=[dict(add=ss.ax("as57"), cur="9:57"), dict()],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p11", "委員会報告 p28", "委員会報告 p13"]))),
    ),
    # c820（2行）＝正面から見た機。左右に大きく傾ける → 2行目で反撃は続く（p13）
    "c820": dict(
        t="揺さぶる操縦", s="左右に振られる機体",
        fig=("m21", dict(view="roll",
                         steps=[dict(state=dict(tilt="left", rock="on"), tag=dict(t="左右に大きく傾ける", at="a")),
                                dict(state=dict(tilt="right"), tag=dict(t="反撃は続く", at="b"))],
                         note="人は描かない・機の形と傾きの角度は模式", src=ss.src(["委員会報告 p13"]))),
    ),
    # c821（1行）＝扉の内と外。9:58:57 扉を押さえる指示（p13）。言葉は字幕だけ
    "c821": dict(
        t="閉ざす扉", s="操縦していた犯人の指示",
        fig=("m21", dict(view="wall", steps=[dict(state=dict(block="on"), tag=dict(t="9:58:57", d="扉を押さえる指示", at="ck"))],
                         rel=[dict(t="9:58:57", src="委員会報告 p13")], note="人は描かない・扉と部屋の形は模式",
                         src=ss.src(["委員会報告 p13"]))),
    ),
    # c822（3行）＝問い → 操縦室の音声の記録装置 → こもった音（p13）
    "c822": dict(
        t="扉ごしの音", s="記録に残った反撃",
        fig=("m21", dict(view="wall", start=dict(block="on"),
                         steps=[dict(), dict(state=dict(rec="on"), tag=dict(t="操縦室の音声の記録装置", at="low")),
                                dict(state=dict(noise="on"), tag=dict(t="こもった音", at="ck"))],   # ⚠️ geom_gap：cab は音の弧が字を通った
                         note="人は描かない・扉と部屋の形は模式", src=ss.src(["委員会報告 p13"]))),
    ),
    # c823（2行）＝🔧 操縦室の音声の記録の帯（模式）。乗客の声の印 → 2行目＝言葉と時刻（字幕だけ）
    "c823": dict(
        t="録音の中の声", s="扉の外からの声",
        fig=("m21", dict(view="cvr", steps=[dict(state=dict(v1="on"), tag=dict(t="乗客の声", at="m1", to="m1")), dict()],
                         note=_CV, src=ss.src(["CVR p6007", "委員会報告 p14"]))),
    ),
    # c824（1行）＝別の叫びの印（言葉と時刻は字幕だけ）
    "c824": dict(
        t="続く叫び", s="同じ録音のすぐあと",
        fig=("m21", dict(view="cvr", start=dict(v1="on"), steps=[dict(state=dict(v2="on"), tag=dict(t="別の叫び", at="m2", to="m2"))],
                         note=_CV, src=ss.src(["CVR p6007", "委員会報告 p14"]))),
    ),
    # c825（1行）＝正面から見た機。10:01ごろ 揺さぶりが止まる（p14「at about 10:01:00」＝「ごろ」）
    "c825": dict(
        t="止まった揺れ", s="10時1分ごろの機体",
        fig=("m21", dict(view="roll", start=dict(tilt="right", rock="on"),
                         steps=[dict(state=dict(tilt="level", calm="on"), tag=dict(t="10:01ごろ", d="揺さぶりが止まる", at="a"))],
                         rel=[dict(t="10:01ごろ", src="委員会報告 p14")], note="人は描かない・機の形と傾きの角度は模式",
                         src=ss.src(["委員会報告 p14"]))),
    ),
    # c826（2行）＝🔧 同じ録音の帯。反撃の音が続く（p14）→ 2行目で機は下へ（p14「The airplane headed down」）
    "c826": dict(
        t="下へ向かう機", s="録音の最後の場面",
        fig=("m21", dict(view="cvr", start=dict(v1="on", v2="on"),
                         steps=[dict(state=dict(push="on"), tag=dict(t="反撃の音が続く", at="pt")),
                                dict(state=dict(down="on"), tag=dict(t="機は下へ", at="md"))],
                         note=_CV, src=ss.src(["委員会報告 p14"]))),
    ),
    # c830（2行）＝時間の帯（93便の寄り）。10:03:11 墜落（割れる時刻＝出典の名）と 9:28 からの35分 → 2行目＝委員会の言葉（字幕だけ）
    "c830": dict(
        t="敗れた犯人", s="9時28分から墜落まで",
        fig=("axis", dict(ss.AX_93, past=[ss.ax("hj93"), ss.ax("as57")], start=dict(cur="9:57"),
                          steps=[dict(add=[ss.ax("crash93"), ss.ax("min35")], cur="10:03:11"), dict()],
                          note="時刻は委員会報告の記録（墜落の時刻は資料で割れる＝委員会報告の値）",
                          src=ss.src(["委員会報告 p11", "委員会報告 p13", "委員会報告 p14", "委員会報告 p30"]))),
    ),
    # c831（3行）＝🔧 扉の内と外。問い（扉に「？」）→ 委員会は書いていない → 操縦は犯人のまま・機は下へ（p14）
    "c831": dict(
        t="書かれた範囲", s="委員会の記述の範囲",
        fig=("m21", dict(view="wall", start=dict(block="on"),
                         steps=[dict(state=dict(q="on")), dict(tag=dict(t="委員会は書いていない", at="cablow")),   # ⚠️ 門番 layout：cab は「？」に重なった
                                dict(state=dict(down="on"), tag=dict(t="操縦は犯人のまま", at="low"))],
                         note="人は描かない・扉と部屋の形は模式", src=ss.src(["委員会報告 p14"]))),
    ),
    # c832（3行）＝🔧 地上で聞かれた言葉の出どころ（言葉そのものは字幕だけ）。問い → AP 通信の記事（6日後）→ 機内の電話→電話会社の係員
    "c832": dict(
        t="2つの言葉", s="新聞が伝えた言葉",
        fig=("m21", dict(view="cvr", start=dict(v1="on", v2="on"),
                         steps=[dict(), dict(state=dict(ap="on"), tag=dict(t="事件の6日後", at="apd")),
                                dict(state=dict(phone="on"), tag=dict(t="電話の向こうで聞かれた言葉", at="phd"))],
                         rel=[dict(t="6日後", src="AP")], note=_CV, src=ss.src(["AP"]))),
    ),
    # c833（1行）＝録音の帯の2つ目の叫びの印に輪（書き起こしにある言葉＝字幕だけ）
    "c833": dict(
        t="録音の言葉", s="電話の言葉との違い",
        fig=("m21", dict(view="cvr", start=dict(v1="on", v2="on", ap="on", phone="on"),
                         steps=[dict(state=dict(hl2="on"), tag=dict(t="録音に残った言葉", at="m2", to="m2"))],
                         note=_CV, src=ss.src(["CVR p6007"]))),
    ),
    # c834（3行）＝🔧 ワシントンの辺りの地図。2行目で議事堂とホワイトハウスに輪（狙い＝委員会の見立て・p14）→ 3行目（p45）
    "c834": dict(
        t="乗客への恩", s="議事堂とホワイトハウスの位置",
        fig=("m21", dict(view="dc",
                         steps=[dict(), dict(state=dict(tgt="on"), tag=dict(t="狙い（委員会の見立て）", at="time")),
                                dict(tag=dict(t="壊されずにすんだかもしれない", at="o2"))],
                         note="地点は一般の座標・陸の形は描かない（模式）", src=ss.src(["委員会報告 p14", "委員会報告 p45"]))),
    ),
    # c835（2行）＝北東部の地図。3つの印（北棟・南棟・ペンタゴン）→ 2行目でシャンクスビル（93便だけ届かず）
    "c835": dict(
        t="届いたのは3機", s="4機の行き先",
        fig=("m21", dict(view="ne", start=dict(dclab="se"),    # 🔧 試し焼き（原寸）：左の「ワシントン」の札がシャンクスビルの輪の名に読めた
                         steps=[dict(state=dict(hits="on"), tag=dict(t="世界貿易センターとペンタゴン", at="w3")),   # ⚠️ geom_gap：hits は陸の輪郭に乗った＝海の上
                                dict(state=dict(shk="on"), tag=dict(t="93便だけ届かず", at="proj"))],
                         rel=[dict(t="93便", src="委員会報告 p30")], note="陸の形は Natural Earth・印の位置は一般の座標（模式）",
                         src=ss.src(["委員会報告 p7", "委員会報告 p8", "委員会報告 p10", "委員会報告 p30"]))),
    ),
})

# ── 🆕 ⑤b-7（2026-10-13）：写真（PLAN＝映像方針の一覧・了承②／書き方は c2.py の ⑤b-7 の注）──
_EWR = P("ewr_gate17_flag_2006")
_SH15A = P("shanksville_2015a")
_M24A = P("flight93_memorial_aerial_2024_05")
_SH15B = P("shanksville_2015b")
SPEC.update({
    # c801（9.8秒・章の頭）＝ニューアーク空港 A ターミナル17番搭乗口の上の旗（2006年・PD-self）・上へ流す
    "c801": dict(photo=_EWR, **ss.mv(_EWR, "u", span=(0.2, 0.8)), side="none", t="93便の出発", s="ニューアーク空港の93便の搭乗口（2006年）"),
    # c827（9.5秒）＝追悼の場（2015年・CC BY 3.0）。🔴 来訪者は右端の遠く（x 2180〜2345・顔 約4px）＝顔の分からない遠景＝モザイク不要
    #   （⑤b-7 に2倍で測った・qa_out/ep21_assets.py の HOLD の注）・ゆっくり引く
    "c827": dict(photo=_SH15A, **ss.mv(_SH15A, "out"), side="none", t="シャンクスビル", s="現在の93便の墜落現場（追悼の場・2015年）"),
    # c828（4.3秒）＝追悼の場の空撮（2024年・CC0）・右へ流す
    "c828": dict(photo=_M24A, **ss.mv(_M24A, "r"), side="none", t="40人", s="現在の93便の墜落現場（追悼の場・2024年の空撮）"),
    # c829（7.2秒）＝追悼の場の建物（2015年・CC BY 3.0・名前の壁は写らない）・左へ流す
    "c829": dict(photo=_SH15B, **ss.mv(_SH15B, "l"), side="none", t="墜落まで35分", s="現在の93便の追悼の場（2015年）"),
})
