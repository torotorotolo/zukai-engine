# -*- coding: utf-8 -*-
"""第4章　2機目　気づいていた管制官 c501–c520（20カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c5.py`）。
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
    'c501': dict(kind='写真',
               plan='WTCSOUTH｜副題：事件の前の世界貿易センター（1976年）｜動き：上へ流す｜権利：D（米議会図書館蔵／知られた制限なし）｜出典の行：Balthazar Korab（米議会図書館蔵）｜注：縦長｜台本の画：実写 wtc_south（事件の前の世界貿易センター・1976年・D・縦長＝全画面で上下を切る・右へ流す＝副題「事件の前の世界貿易センター（1976年）」）',
               src="委員会報告 p21（`At approximately 8:42, shortly after entering New York Center's airspace, the pilot of United 175 broke in`）"),
    'c502': dict(kind='図解',
               plan='台本の画：図 模式 管制の無線（ニューヨーク・センターと175便を結ぶ線）',
               src='委員会報告 p7（`a "suspicious transmission" overheard from another plane (which turned out to have been Flight 11) just after takeoff`・`This was United 175\'s last communication with the ground`）'),
    'c503': dict(kind='図解',
               plan='台本の画：図 模式 175便の機内（前の座席と操縦室の扉＝人は描かない）',
               src='委員会報告 p7（`The hijackers attacked sometime between 8:42 and 8:46`）・NTSB 175便（`at 8:47, when the aircraft changed beacon codes twice within a one-minute period`）'),
    # 🔧 ⑤b-4（2026-10-12）：c504・c509・c512 は図・写真の頁 → 図解。RG237 の175便の動画（4-AWA-716-WTC2）は描き終えた航跡の地図だけで、
    #   札も番号の変化も写っておらず、線はマンハッタンまで届いていない（7本目の見本帳の代表コマを見た）。213番台（ny_best）は NORAD の立体の
    #   アニメーション＝レーダーの画面ではなく、塔へ入る線（衝突の瞬間）が写る＝使わない。→ レーダーの画面の模式図（mech21 scope）で見せる
    'c504': dict(kind='図解',
               plan='🔧 模式 レーダーの画面（札の番号が変わる）｜台本の画：図 RG237（ニューヨーク・センターのレーダー再生の画面・175便の札の番号が変わる所）',
               src='委員会報告 p21（`The New York Center controller and manager were unaware that American 11 had already crashed`・`At 8:51, the controller noticed the transponder change from United 175 and tried to contact the aircraft. There was no response`）'),
    'c505': dict(kind='図解',
               plan='台本の画：図 模式 機内の電話から地上への線（人は描かない）',
               src='委員会報告 p7（`a male flight attendant called a United office in San Francisco`・`both pilots had been killed, a flight attendant had been stabbed`）・p8（`the hijackers were probably flying the plane`）'),
    # 🔧 ⑤b-4：c506 は RG237 → NTSB 175便の飛行経路の調べ PDF 3頁の図1（175便が南西へ進んでから北東のニューヨークへ向きを変えた航跡＝頁のまま）
    'c506': dict(kind='図・写真の頁',
               plan='🔧 NTSB 175便 図1（航跡が向きを変える）｜台本の画：図 RG237（同じ画面・175便の点が向きを変える）',
               src='委員会報告 p22（`saying that "we may have a hijack" and that he could not find the aircraft`）'),
    'c507': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（175便＝8:53「乗っ取りかもしれない」・8:55 上司へ）',
               src='委員会報告 p22（`At about 8:55, the controller in charge notified a New York Center manager that she believed United 175 had also been hijacked`）'),
    'c508': dict(kind='図解',
               plan='台本の画：図 模式 手順の段（ニューヨーク・センターの上司から地域の管理職へ＝扉が閉じている）',
               src='委員会報告 p22（`The manager tried to notify the regional managers and was told that they were discussing a hijacked aircraft (presumably American 11) and refused to be disturbed`）'),
    'c509': dict(kind='図解',
               plan='🔧 模式 レーダーの画面（2機の「？」）｜台本の画：図 RG237（同じ画面）',
               src='委員会報告 p22（`we might have a hijack over here, two of them`）'),
    'c510': dict(kind='図解',
               plan='台本の画：図 模式 電話の線（ニューヨーク・センターからハーンドンのコマンドセンターへ）',
               src="委員会報告 p22（`Between 9:01 and 9:02, a manager from New York Center told the Command Center in Herndon`・`We have several situations going on here. It's escalating big, big time. We need to get the military involved with us`）"),
    'c511': dict(kind='図解',
               plan='台本の画：図 模式 北アメリカの地図（バージニア州ハーンドンの印）',
               src='委員会報告 p14（`Command Center, located in Herndon`）・p16（`Virginia, which oversees daily traffic flow within the entire airspace system`）'),
    'c512': dict(kind='図解',
               plan='🔧 模式 レーダーの画面（点が途切れる）｜台本の画：図 RG237（175便の点がマンハッタンの南部の上で途切れる）',
               src='委員会報告 p22（`Heads up man, it looks like another one coming in`・`the radar data terminated over Lower Manhattan`）'),
    'c513': dict(kind='写真',
               plan="LCA01｜副題：燃える世界貿易センター（当日）｜動き：ゆっくり寄る｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：旧版の wtc_smoke_day の原本（議会図書館 A01）＝両棟が燃える（②③）・サムネの地｜台本の画：実写 wtc_smoke_day（LC-A05-A01・エンパイア・ステート・ビルの向こうで燃える両棟・C'＝米議会図書館蔵（撮影者不詳）・全画面・ゆっくり寄る＝副題「燃える世界貿易センター（当日）」）",
               src='委員会報告 p8（`At 9:03:11, United Airlines Flight 175 struck the South Tower of the World Trade Center`）'),
    'c514': dict(kind='写真',
               plan="LCA03｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：左へ流す｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：9:03 の語り。塔は重なる角度＝「両棟」と副題に書かない｜台本の画：実写 当日の世界貿易センター（A・Commons の説明に当日の日付がある14点から選ぶ・全画面・左へ流す＝副題は絵を見て書く）",
               src='委員会報告 p23（`came in a phone call from New York Center to NEADS at 9:03`・`The notice came at about the time the plane was hitting the South Tower`）'),
    'c515': dict(kind='写真',
               plan="WTC71｜副題：事件の前の世界貿易センター（1971年）｜動き：上へ流す｜権利：D（U.S. News & World Report の写真＝米議会図書館へ譲渡）｜出典の行：Thomas J. O'Halloran（米議会図書館蔵）｜注：9:03 より前の語り＝北棟だけが燃える写真は見つからない（議会図書館の A ロールは A02〜A10 が崩壊前・2本が重なる角度で原寸でも決められない）。白黒・縦長｜台本の画：実写 事件の前の世界貿易センター（D・別の点＝語りは 8:51〜9:02＝両棟が燃える写真は置かない。北棟だけが燃える点が見つかればそれ＝副題は絵を見て書く）",
               src='委員会報告 p22（`refused to be disturbed`・`Between 9:01 and 9:02, a manager from New York Center told the Command Center`）・p23（`came in a phone call from New York Center to NEADS at 9:03`）'),
    'c516': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（11便と175便を並べる・FAA が知った印＝乗っ取りから11分後と9分後）',
               src='委員会報告 p455（`The FAA knew or strongly suspected that Flight 11 was a hijacking 11 minutes after it was taken over; Flight 175, 9 minutes after it was taken over`）'),
    'c517': dict(kind='図解',
               plan='台本の画：図 模式 北東部の地図（ロングアイランドの沖の軍の空域・F-15の線）',
               src='委員会報告 p20（`Lacking a target, they were vectored toward military-controlled airspace off the Long Island coast`）・p23（`decided against holding the fighters in military airspace away from Manhattan`）'),
    'c518': dict(kind='写真',
               plan='WH518｜副題：当日の朝、フロリダ州の小学校（報道を見る大統領）｜動き：2点を順に寄る｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Eric Draper（Courtesy George W. Bush Presidential Library）｜注：説明＝教室で175便の衝突の報道を見る（時刻の記載なし）。子どもは写らない。WHTV 598 の耳打ちの秒には差し替えない（子どもの顔が多い）｜台本の画：実写 小学校の部屋のテレビに映る燃える両棟（ホワイトハウスの写真係・説明「9:10ごろ」・A の見込み＝権利の札は映像方針で確かめる・子どもが写るなら顔だけモザイク・全画面＝副題「フロリダ州の小学校（当日）」）',
               src='委員会報告 p38（`The President was seated in a classroom when, at 9:05`・`A second plane hit the second tower. America is under attack`）'),
    'c519': dict(kind='写真',
               plan="LCA06｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：ゆっくり引く｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜台本の画：実写 当日の世界貿易センター（A・別の点＝副題は絵を見て書く）",
               src='委員会報告 p35（`nearly everyone in the White House told us, they immediately knew it was not an accident`）'),
    'c520': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（11便と175便＝軍に届いた時刻の印）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-12）：図解 第4章（13カット）＋頁1（c506 NTSB 175便の図1）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「2機目　気づいていた管制官」と4字以上同じ並びを見出し・副題に入れない（門番 dup）。人は描かない・無線と電話の逐語は
#      画面に出さない（語りと字幕だけ）。時刻は委員会報告の文字の層で当てた（門番 check_mech の REC_M21・check_axis の REC_AXIS）
SPEC.update({
    # c502（3行）＝管制の無線（ニューヨーク・センターと175便）。8:42 の交信 → 聞いた声は11便から → 地上との最後の交信（p7）
    "c502": dict(
        t="175便の無線", s="ニューヨーク・センターの受け持ちで",
        fig=("m21", dict(view="radio", start=dict(ctr="ny"),
                         steps=[dict(state=dict(v1="on"), tag=dict(t="8:42", at="time")),
                                dict(tag=dict(t="聞いた声は11便から", at="v2")),
                                dict(tag=dict(t="地上との最後の交信", at=(112.0, 530.0, "start", 460.0)))],
                         rel=[dict(t="8:42", src="委員会報告 p7"), dict(t="11便", src="委員会報告 p7")],
                         note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p7", "委員会報告 p21"]))),
    ),
    # c503（2行）＝175便の機内（前の部分）。乗っ取りの始まり 8:42〜8:46（p7）→ 8:47 番号が1分で2回（p7）
    "c503": dict(
        t="始まった時間", s="175便の機内（前の座席と操縦室の扉）",
        fig=("m21", dict(view="cabin", start=dict(zoom="front"),
                         # 🔧 試し焼き：先の出来事を右・後の出来事を左に置くと、左から読んで時間が逆になった＝左に 8:42〜8:46・右に 8:47
                         steps=[dict(tag=dict(t="8:42〜8:46 のあいだ", d="委員会の記録", at="how")),
                                dict(tag=dict(t="8:47 番号が1分で2回変わる", at="start"))],
                         rel=[dict(t="8:42〜8:46", src="委員会報告 p7"), dict(t="8:47", src="委員会報告 p7"), dict(t="1分で2回", src="委員会報告 p7")],
                         note="人は描かない・座席の並びは模式", src=ss.src(["委員会報告 p7", "NTSB 175便 p3002"]))),
    ),
    # c504（2行）＝🔧 管制のレーダーの画面（模式）。11便を探す → 8:51 札の番号の変化に気づく（p21）
    "c504": dict(
        t="番号の変化", s="ニューヨーク・センターの管制官が見ていた点",
        fig=("m21", dict(view="scope", start=dict(block="on"),
                         steps=[dict(tag=dict(t="11便を探し続ける", at="time")),
                                dict(state=dict(code="on"), tag=dict(t="8:51 管制官が気づく", d="呼びかけに応答なし", at="block", to="block"))],
                         rel=[dict(t="11便", src="委員会報告 p21"), dict(t="8:51", src="委員会報告 p21")],
                         note="画面の形と札は模式（記録の画面ではない）", src=ss.src(["委員会報告 p21"]))),
    ),
    # c505（2行）＝機内の電話から航空会社の事務所へ（8:52・p7）→ 2行目で操縦室に「？」（言葉は語りと字幕だけ）
    "c505": dict(
        t="事務所への電話", s="175便の客室乗務員の電話",
        fig=("m21", dict(view="phone", start=dict(to="office"),
                         steps=[dict(state=dict(call="on"), tag=dict(t="8:52", at="time")),
                                dict(state=dict(ckq="on"), tag=dict(t="操縦は乗っ取った側の手に", at="out"))],   # ⚠️ 門番 echo：「犯人が操縦している見込み」は字幕の写し
                         rel=[dict(t="8:52", src="委員会報告 p7")], note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p7", "委員会報告 p8"]))),
    ),
    # c506（7.2秒）＝🔧 NTSB 175便の飛行経路の調べ PDF 3頁（Figure 1・横倒しのスキャンを正立）。南西へ進んで北東へ向きを変えた航跡
    "c506": dict(photo=ss.page(3003), trim=ss.ptrim("c506"), bias=ss.pbias("c506"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="向きを変えた機", s="NTSB の飛行経路の調べ（2002年）の図1"),
    # c507（3行）＝175便の帯（AX_175）。8:51 気づく（沈める）→ 8:53 乗っ取りを疑う → 8:55ごろ 上司へ（p22）。
    #   ⚠️ 8:47 の点（番号が変わる）は置かない＝c503・c504 で語りずみ・置くと 8:51 の縦の線が札を貫いた（門番 axis）
    "c507": dict(
        t="伝わった疑い", s="175便をめぐる地上の動き（アメリカ東部の夏の時間）",
        fig=("axis", dict(ss.AX_175, past=[ss.ax("see175")], start=dict(cur="8:51"),
                          steps=[dict(add=ss.ax("may175"), cur="8:53"), dict(add=ss.ax("mgr175"), cur="8:55"), dict()],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p7", "委員会報告 p21", "委員会報告 p22"]))),
    ),
    # c508（3行）＝手順の段（ニューヨーク・センター）。上司 → 地域の管理職へ → 11便の話し合いの最中 → 取り次ぎを断る（p22）
    "c508": dict(
        t="断られた知らせ", s="ニューヨーク・センターの上司の動き",
        fig=("m21", dict(view="chain", start=dict(who="ny"),
                         steps=[dict(state=dict(lit="2", reg="on")), dict(tag=dict(t="11便の話し合いの最中", at="tl")),
                                dict(state=dict(reg="x"), tag=dict(t="取り次ぎを断る", at="reg"))],
                         rel=[dict(t="11便", src="委員会報告 p22")], note="段の形は模式", src=ss.src(["委員会報告 p22"]))),
    ),
    # c509（2行）＝🔧 同じ画面（模式）。8:58 → 2行目で2つの点に「？」（言葉は語りと字幕だけ）
    "c509": dict(
        t="2機の乗っ取り", s="175便を探す管制官の画面",
        fig=("m21", dict(view="scope", start=dict(block="on", code="on"),
                         steps=[dict(tag=dict(t="8:58", at="time")), dict(state=dict(two="on"))],
                         rel=[dict(t="8:58", src="委員会報告 p22")], note="画面の形と点は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p22"]))),
    ),
    # c510（3行）＝電話の線（ニューヨーク・センター → ハーンドンのコマンドセンター・9:01〜9:02・p22）。やりとりは字幕だけ
    "c510": dict(
        t="軍の助けを", s="管制の現場から全米の司令塔へ",
        fig=("m21", dict(view="call", start=dict(pair="ny"),
                         steps=[dict(state=dict(link="on"), tag=dict(t="9:01〜9:02", at="time")), dict(state=dict(talk="ask")), dict()],
                         rel=[dict(t="9:01〜9:02", src="委員会報告 p22")], note="人は描かない・建物の形は模式（言葉の引用は画面に出さない）",
                         src=ss.src(["委員会報告 p22"]))),
    ),
    # c511（3行）＝北アメリカの地図。2行目で全米の空港の点 → 3行目でハーンドン（p14・p16）
    "c511": dict(
        t="空の司令塔", s="コマンドセンターの場所",
        fig=("m21", dict(view="us", steps=[dict(), dict(state=dict(air="on")),
                                           dict(state=dict(herndon="on"), tag=dict(t="ハーンドン", d="バージニア州", at="herndon", to="herndon"))],
                         note="陸の形は Natural Earth・空港の点は大きな空港の一般の座標（模式）",
                         src=ss.src(["委員会報告 p14", "委員会報告 p16"]))),
    ),
    # c512（2行）＝🔧 同じ画面（模式）。9:02 → 2行目で点と札が途切れる（p22「the radar data terminated over Lower Manhattan」）
    "c512": dict(
        t="途切れた点", s="175便を追っていた画面",
        fig=("m21", dict(view="scope", start=dict(block="on", code="on"),
                         steps=[dict(tag=dict(t="9:02", at="time")),
                                dict(state=dict(block="off", blip="off", code="off"), tag=dict(t="点と札が途切れる", at="dot", to="blip"))],
                         rel=[dict(t="9:02", src="委員会報告 p22")], note="画面の形と点は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p22"]))),
    ),
    # c516（2行）＝棒（乗っ取りから FAA が知る・強く疑うまで＝11分・9分＝委員会報告 p455）。数字は画面に書かない（目盛りだけ）
    "c516": dict(
        t="気づくまで", s="FAA が乗っ取りと知った早さ",
        fig=("qty", dict(view="bar", groups=[ss.QG["faa"]], steps=[dict(add=ss.qb("faa11")), dict(add=ss.qb("faa175"))],
                         note="分は委員会報告の注の記録", src=ss.src(["委員会報告 p455"]))),
    ),
    # c517（3行）＝北東部の地図。8:53 F-15 → ロングアイランドの沖の軍の空域 → 2機目のあと、マンハッタンの方へ（p20・p23）
    "c517": dict(
        t="待たせた戦闘機", s="オーティスの F-15 の行き先",
        fig=("m21", dict(view="ne", start=dict(bases="on"),
                         steps=[dict(state=dict(f15="on"), tag=dict(t="8:53 F-15 が飛び立つ", at="f15")),
                                dict(tag=dict(t="沖の軍の空域", at="w105")),
                                dict(state=dict(mnh="on"))],     # 🔧 試し焼き：札「マンハッタンの方へ」は右の海に離れて浮いた＝矢印と語りだけ
                         rel=[dict(t="8:53", src="委員会報告 p20"), dict(t="F-15", src="委員会報告 p20")],
                         note="陸の形は Natural Earth・空域の位置と線は模式", src=ss.src(["委員会報告 p20", "委員会報告 p23"]))),
    ),
    # c520（2行）＝その朝の帯（AX_MORN）。軍に届いた時刻（11便 8:37:52・175便 9:03）→ 2行目で77便が画面から消えた 8:56
    "c520": dict(
        t="遅れた知らせ", s="軍に届いた時刻と3機目",
        fig=("axis", dict(ss.AX_MORN, start=dict(cur="8:37:52"),
                          steps=[dict(add=[ss.ax("mil11"), ss.ax("mil175")], cur="9:03"), dict(add=ss.ax("off77"))],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p20", "委員会報告 p23", "委員会報告 p24", "委員会報告 p25"]))),
    ),
})
