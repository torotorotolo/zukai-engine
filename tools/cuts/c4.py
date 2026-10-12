# -*- coding: utf-8 -*-
"""第3章　1機目　応答しない11便 c401–c426（26カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c4.py`）。
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
    'c401': dict(kind='図・写真の頁',
               plan='見る向き：上から｜注：NTSB 11便の経路｜台本の画：図 NTSB 11便の経路（PDF p3 の経路図をなぞる・ボストンから西へ、南へ折れてニューヨークへ）',
               src='委員会報告 p4（`Just before 8:14, it had climbed to 26,000 feet`）'),
    'c402': dict(kind='写真',
               plan='ARTCC｜副題：航空路管制センター（別のセンター・年は不明）｜動き：ゆっくり寄る｜権利：A（FAA の職務）｜出典の行：米連邦航空局（FAA）｜注：管制官＝職務｜台本の画：実写 artcc_screen_pre（FAA の航空路管制センターの卓・A・全画面・ゆっくり寄る＝副題「航空路管制センター（別のセンター・年は不明）」）',
               src='NTSB 11便（`At 8:13:29`・`The crew acknowledged`・`The crew never acknowledged`）'),
    'c403': dict(kind='図解',
               plan='台本の画：図 模式 11便の機内（前の座席と操縦室の扉＝人は描かない）',
               src='委員会報告 p4（`we believe the hijacking began at 8:14 or shortly thereafter`）・p5（`We do not know exactly how the hijackers gained access to the cockpit`）'),
    'c404': dict(kind='図解',
               plan='台本の画：図 模式 機内の電話から地上への線（人は描かない）',
               src="委員会報告 p5（`The cockpit is not answering, somebody's stabbed in business class`・`I think we're getting hijacked`）"),
    'c405': dict(kind='図解',
               plan='台本の画：図 模式 同じ線（電話の時間の帯＝約25分）',
               src='委員会報告 p5（`The emergency call lasted approximately 25 minutes`・`calmly and professionally relayed information`）'),
    'c406': dict(kind='図解',
               plan='台本の画：図 模式 同じ線（機内から操縦室への線に×）',
               src='委員会報告 p5（`took action outside the scope of their training, which emphasized that in a hijacking, they were to communicate with the cockpit crew`）'),
    # 🔧 ⑤b-3（2026-10-12）：図・写真の頁 → 図解。RG237 の 11便の動画（3-AWA-716-WTC1）は描き終えた航跡の地図だけで、便名と高度の札が
    #   写っていない（7本目の見本帳の 38.0秒を見た）＝「札が消える」はレーダーの画面の模式図（mech21 scope）で見せる。RG237 は c408 の頁に
    'c407': dict(kind='図解',
               plan='🔧 模式 レーダーの画面（点と便名・高度の札→札が消える）｜台本の画：図 RG237（ボストン・センターのレーダー再生の画面・11便の札が消える所・FAA・Unrestricted）',
               src='NTSB 11便（`At about 8:21`）・委員会報告 p18（`At 8:21, American 11 turned off its transponder, immediately degrading the information available about the aircraft`）'),
    'c408': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（同じ画面・札の無い点）',
               src='委員会報告 p18（`The controller told his supervisor that he thought something was seriously wrong with the plane, although neither suspected a hijacking`）'),
    'c409': dict(kind='図解',
               plan='台本の画：図 模式 管制の無線（ボストン・センターと11便を結ぶ線）',
               src="委員会報告 p19（`We have some planes. Just stay quiet, and you'll be okay. We are returning to the airport`）"),
    'c410': dict(kind='図解',
               plan='台本の画：図 模式 同じ線（機内の放送と管制の無線の切り替え）',
               src='委員会報告 p6（`inadvertently broadcast their message over the air traffic control channel instead of the cabin public-address channel`）・p19（`The controller only heard something unintelligible`）'),
    'c411': dict(kind='図解',
               plan='台本の画：図 模式 同じ線（2つ目の声）',
               src='委員会報告 p19（`Nobody move`・`The controller told us that he then knew it was a hijacking`）'),
    'c412': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（11便＝8:25 ボストン・センターが知る）',
               src='図表 p32（`Boston Center aware of hijacking`）・委員会報告 p19（`Between 8:25 and 8:32, in accordance with the FAA protocol, Boston Center managers started notifying their chain of command`）'),
    'c413': dict(kind='図解',
               plan='台本の画：図 模式 手順の段（上へ伸びる矢印と、横から軍へ伸びる矢印）',
               src="委員会報告 p20（`Boston Center did not follow the protocol in seeking military assistance through the prescribed chain of command`・`at 8:34, to contact the military through the FAA's Cape Cod facility`）"),
    'c414': dict(kind='図解',
               plan='台本の画：図 模式 同じ（アトランティックシティの昔の基地に×）',
               src='委員会報告 p20（`The center also tried to contact a former alert site in Atlantic City, unaware it had been phased out`）'),
    'c415': dict(kind='図解',
               plan='台本の画：図 模式 電話の線（ボストン・センターから NEADS へ・8:37:52）',
               src='委員会報告 p20（`At 8:37:52, Boston Center reached NEADS. This was the first notification received by the military`）'),
    'c416': dict(kind='図解',
               plan='台本の画：図 模式 同じ線（やりとりは字幕だけ・画面に大きく出さない）',
               src='委員会報告 p20（`We have a hijacked aircraft headed towards New York`・`Is this real-world or exercise?`・`No, this is not an exercise, not a test`）'),
    'c417': dict(kind='図解',
               plan='台本の画：図 模式 同じ線（演習の予定表の札＝旧ソ連の爆撃機の想定）',
               src='委員会報告 p458（`Vigilant Guardian`・`if anything, expedited`）'),
    'c418': dict(kind='写真',
               plan='F15B｜副題：オーティス基地のF-15（2001年秋）｜動き：左へ流す｜権利：A（米空軍の職務）｜出典の行：米空軍｜注：幅1126＝全画面で1.7倍に引き伸ばす（柔らかい）｜台本の画：実写 F-15 オーティス基地（別の点・2001年秋のニューヨーク上空の警戒・102戦闘航空団・A・全画面・左へ流す＝副題「オーティス基地のF-15（2001年秋）」）',
               src='委員会報告 p20（`NEADS ordered to battle stations the two F-15 alert aircraft at Otis Air Force Base in Falmouth, Massachusetts, 153 miles away from New York City`）'),
    'c419': dict(kind='図解',
               plan='台本の画：図 模式 北東部の地図（オーティスからの線・行き先に「？」）',
               src="委員会報告 p20（`scrambled at 8:46 from Otis Air Force Base`・`I don't know where I'm scrambling these guys to. I need a direction, a destination`）"),
    'c420': dict(kind='図解',
               plan='台本の画：図 模式 レーダーの画面（札の無い点を探す）',
               src='委員会報告 p20（`NEADS personnel spent the next minutes searching their radar scopes for the primary radar return`）'),
    'c421': dict(kind='写真',
               plan='WTCFAR｜副題：事件の前の世界貿易センター（1976年）｜動き：上へ流す｜権利：D（米議会図書館蔵／知られた制限なし）｜出典の行：Balthazar Korab（米議会図書館蔵）｜注：縦長＝全画面で上下を切る｜台本の画：実写 wtc_far（事件の前の世界貿易センター・1976年・D＝米議会図書館蔵／知られた制限なし・縦長＝全画面で上下を切る・ゆっくり上へ＝副題「事件の前の世界貿易センター（1976年）」）',
               src='委員会報告 p7（`At 8:46:40, American 11 crashed into the North Tower of the World Trade Center in New York City`）'),
    'c422': dict(kind='写真',
               plan='WTCBASE｜副題：事件の前の世界貿易センター（1976年）｜動き：下へ流す｜権利：D（米議会図書館蔵／知られた制限なし）｜出典の行：Balthazar Korab（米議会図書館蔵）｜注：縦長｜台本の画：実写 wtc_base（事件の前の世界貿易センター・1976年・D・縦長＝全画面で上下を切る・ゆっくり寄る＝副題「事件の前の世界貿易センター（1976年）」）',
               src='委員会報告 p278（`Both towers had 110 stories, were about 1,350 feet high`・`up to 50,000 office workers occupied the towers`）'),
    'c423': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（8:37:52 から 8:46:40 まで＝9分の帯・8:53 に離陸の印）',
               src="委員会報告 p20（`Radar data show the Otis fighters were airborne at 8:53`）・p21（`That nine minutes' notice before impact was the most the military would receive of any of the four hijackings`）"),
    'c424': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（NEADS のレーダーの画面を小さく重ねる）',
               src='委員会報告 p20（`while NEADS personnel were still trying to locate the flight, word reached them that a plane had hit the World Trade Center`）'),
    'c425': dict(kind='図解',
               plan='台本の画：図 模式 手順の段（ボストン・センターから上へ伸びる段と、軍への近道）',
               src='委員会報告 p19（`did not contact the NMCC to request a fighter escort`）'),
    'c426': dict(kind='図解',
               plan='台本の画：図 模式 3つの前提の箱（1つ目の「姿を消そうとはしない」に×）',
               src='委員会報告 p31（`had never handled a hijacked aircraft that attempted to disappear`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-12）：図解 第3章（19カット）＋頁2（c401 NTSB の図・c408 RG237 の1コマ）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「1機目　応答しない11便」と4字以上同じ並び（「応答しない」ほか）を見出し・副題に入れない（門番 dup）。人は描かない・
#      無線と電話の逐語は画面に出さない（語りと字幕だけ）。頁＝`ss.page`（名は pg で始まる＝門番 textscreens の「図・写真の頁」）
SPEC.update({
    # c401（12.9秒）＝NTSB 11便の飛行経路の調べ PDF 3頁（Figure 1・横倒しのスキャンを正立）。図の題から枠まで・額ごと寄る
    "c401": dict(photo=ss.page(2003), trim=ss.ptrim("c401"), bias=ss.pbias("c401"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="11便の航跡", s="NTSB の飛行経路の調べ（2002年）の図1"),
    # c403（2行）＝11便の機内（前の部分・操縦室の扉）。1行目で始まりの時刻（委員会の見立て）・2行目で扉に「？」
    "c403": dict(
        t="始まりの時刻", s="11便の機内（前の座席と操縦室の扉）",
        fig=("m21", dict(view="cabin", start=dict(zoom="front"),
                         steps=[dict(tag=dict(t="8:14か、その少しあと", d="委員会の見立て", at="start")),
                                dict(state=dict(doorq="on"), tag=dict(t="入り方は分かっていない", at="how", to="door"))],
                         rel=[dict(t="8:14", src="委員会報告 p4")], note="人は描かない・座席の並びは模式",
                         src=ss.src(["委員会報告 p4", "委員会報告 p5"]))),
    ),
    # c404（2行）＝機内の電話から予約の窓口へ（8:19）→ 2行目で操縦室に「？」（言葉は語りと字幕だけ）
    "c404": dict(
        t="機内からの電話", s="11便の客室乗務員の電話",
        fig=("m21", dict(view="phone", steps=[dict(state=dict(call="on"), tag=dict(t="8:19", at="time")), dict(state=dict(ckq="on"))],
                         rel=[dict(t="8:19", src="委員会報告 p5")], note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p5"]))),
    ),
    # c405（2行）＝電話の長さ（約25分）
    "c405": dict(
        t="続いた電話", s="地上へ伝え続けた客室乗務員",
        fig=("m21", dict(view="phone", start=dict(call="on"), steps=[dict(state=dict(dur="on"), tag=dict(t="約25分", at="dur")), dict()],
                         rel=[dict(t="約25分", src="委員会報告 p5")], note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p5"]))),
    ),
    # c406（2行）＝訓練の線（操縦室と連絡）→ 2行目で×と「地上へ伝え続けた」（訓練の外）
    "c406": dict(
        t="訓練の外", s="乗っ取りのときの訓練",
        fig=("m21", dict(view="phone", start=dict(call="on", dur="on"),
                         steps=[dict(state=dict(train="on"), tag=dict(t="訓練：操縦室と連絡", at="train")),
                                dict(state=dict(train="x"), tag=dict(t="地上へ伝え続けた", at="out"))],
                         note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p5"]))),
    ),
    # c407（3行）＝🔧 管制のレーダーの画面（模式）。点と便名・高度の札 → 3行目で札が消えて点だけ（PLAN の注）
    "c407": dict(
        t="消えた札", s="ボストン・センターの管制官が見ていた点",
        fig=("m21", dict(view="scope", start=dict(block="on"),
                         steps=[dict(tag=dict(t="8:21", at="time")), dict(tag=dict(t="便名と高度の札", at="block", to="block")),
                                dict(state=dict(block="off"), tag=dict(t="点だけが残る", at="dot", to="blip"))],
                         rel=[dict(t="8:21", src="委員会報告 p18")], note="画面の形と札は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p18"]))),
    ),
    # c408（7.0秒）＝RG237（FAA のレーダーの再生・3-AWA-716-WTC1 の 38.0秒＝動かない航跡の地図）。額ごと寄る
    "c408": dict(photo=ss.page("r11"), trim=ss.ptrim("c408"), bias=ss.pbias("c408"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="FAA の記録", s="レーダーの記録から再生した11便の航跡"),
    # c409（2行）＝管制の無線（8:24:38・言葉は語りと字幕だけ）
    "c409": dict(
        t="無線の声", s="ボストン・センターと11便",
        fig=("m21", dict(view="radio", steps=[dict(state=dict(v1="on"), tag=dict(t="8:24:38", at="time")), dict()],
                         rel=[dict(t="8:24:38", src="委員会報告 p19")], note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p19"]))),
    ),
    # c410（2行）＝機内の放送のつもり（p6）→ 2行目で管制官には聞き取れない（p19）
    "c410": dict(
        t="流れた先", s="機内の放送の言葉が無線へ",
        fig=("m21", dict(view="radio", start=dict(v1="on"),
                         steps=[dict(state=dict(pa="on"), tag=dict(t="乗客への放送（のつもり）", at="pa")),
                                dict(state=dict(garble="on"), tag=dict(t="よく聞き取れない", at="garble"))],
                         note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p6", "委員会報告 p19"]))),
    ),
    # c411（3行）＝続いた声 → 3行目で管制官が乗っ取りと分かる
    "c411": dict(
        t="2つ目の声", s="管制官が気づいた時点",
        fig=("m21", dict(view="radio", start=dict(v1="on", pa="on", garble="on"),
                         steps=[dict(), dict(state=dict(v2="on"), tag=dict(t="続いた声", at="v2")),
                                dict(state=dict(know="on"), tag=dict(t="乗っ取りと分かる", at="know"))],
                         note="人は描かない・機と線は模式", src=ss.src(["委員会報告 p19"]))),
    ),
    # c412（2行）＝11便の帯（AX_11）。8:25 ボストン・センターが知る（図表 p32）→ 8:25〜8:32 上の段へ（p19）。⚠️ 8:24:38 の声は 8:25 と 22秒＝線が札を貫く＝past に入れない
    "c412": dict(
        t="伝え始め", s="FAA の手順どおりの知らせ",
        fig=("axis", dict(ss.AX_11, past=[ss.ax("xpdr11")], start=dict(cur="8:21"),
                          steps=[dict(add=ss.ax("aware11"), cur="8:25"), dict(add=ss.ax("chain11"), cur="8:32")],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p18", "委員会報告 p19", "図表 p32"]))),
    ),
    # c413（2行）＝手順の段（ボストン・センター）と軍への近道 → 2行目でケープコッドの FAA の施設（8:34）
    "c413": dict(
        t="軍への近道", s="ボストン・センターの動き",
        fig=("m21", dict(view="chain", start=dict(who="bos", lit="3"),
                         steps=[dict(state=dict(short="on"), tag=dict(t="決められた段を飛ばす", at="tl")),
                                dict(state=dict(cape="on"), tag=dict(t="8:34", at="cape"))],
                         rel=[dict(t="8:34", src="委員会報告 p20")], note="段の形は模式", src=ss.src(["委員会報告 p20"]))),
    ),
    # c414（2行）＝同じ段にアトランティックシティの昔の待機の基地 → 2行目で×（すでに無かった）
    "c414": dict(
        t="廃止ずみの基地", s="ボストン・センターの別の電話",
        fig=("m21", dict(view="chain", start=dict(who="bos", lit="3", short="on", cape="on"),
                         steps=[dict(state=dict(ac="on")), dict(state=dict(ac="x"), tag=dict(t="すでに無かった基地", at="ac"))],
                         note="段の形は模式", src=ss.src(["委員会報告 p20"]))),
    ),
    # c415（2行）＝電話の線（ボストン・センター→NEADS・8:37:52）→ 軍への最初の知らせ
    "c415": dict(
        t="軍への電話", s="FAA の管制から防空の当直へ",
        fig=("m21", dict(view="call", steps=[dict(state=dict(link="on"), tag=dict(t="8:37:52", at="time")),
                                             dict(tag=dict(t="軍への最初の知らせ", at="first"))],
                         rel=[dict(t="8:37:52", src="委員会報告 p20")], note="人は描かない・建物の形は模式", src=ss.src(["委員会報告 p20"]))),
    ),
    # c416（2行）＝やりとり（言葉は字幕だけ＝画面は行き来の矢印と「？」）
    "c416": dict(
        t="聞き返し", s="NEADS とボストン・センターのやりとり",
        fig=("m21", dict(view="call", start=dict(link="on"), steps=[dict(state=dict(talk="ask")), dict(state=dict(talk="back"))],
                         note="人は描かない・建物の形は模式（言葉の引用は画面に出さない）", src=ss.src(["委員会報告 p20"]))),
    ),
    # c417（3行）＝その朝の演習の予定（旧ソ連の爆撃機の想定）→ 3行目で委員会の見立て（対応はむしろ早まった＝p458）
    "c417": dict(
        t="同じ朝の演習", s="NEADS の予定（委員会報告の注）",
        fig=("m21", dict(view="call", start=dict(link="on", talk="back"),
                         steps=[dict(), dict(state=dict(drill="on")),
                                dict(tag=dict(t="対応はむしろ早まった", d="委員会の見立て", at="fast"))],
                         note="人は描かない・建物の形は模式", src=ss.src(["委員会報告 p458"]))),
    ),
    # c419（2行）＝北東部の地図。オーティスからの発進の命令（8:46）と行き先の「？」→ 2行目で方角も行き先も分からない
    "c419": dict(
        t="行き先の情報", s="オーティス基地からの発進",
        fig=("m21", dict(view="ne", start=dict(neads="on", bases="on"),
                         steps=[dict(state=dict(scr="on"), tag=dict(t="8:46 発進の命令", at="scr")),
                                dict(tag=dict(t="方角も行き先も分からない", at="info"))],
                         rel=[dict(t="8:46", src="委員会報告 p20")], note="陸の形は Natural Earth・矢印は向きの見当がつかないことの模式",
                         src=ss.src(["委員会報告 p20"]))),
    ),
    # c420（2行）＝NEADS のレーダーの画面（模式）。札の無い点 → 2行目で11便を探す輪
    "c420": dict(
        t="札の無い点", s="防空の当直が見ていた点",
        fig=("m21", dict(view="scope", start=dict(who="neads"),
                         steps=[dict(state=dict(dots="on")), dict(state=dict(search="s1"), tag=dict(t="11便の点を探す", at="search"))],
                         rel=[dict(t="11便", src="委員会報告 p20")], note="画面の形と点は模式（記録の画面ではない）",
                         src=ss.src(["委員会報告 p20"]))),
    ),
    # c423（3行）＝11便の帯（AX_11）。北棟 8:46:40（割れる時刻＝出典の名）と F-15 の離陸 8:53 → 2行目で知らせから衝突までの9分
    "c423": dict(
        t="9分の知らせ", s="軍が知らされてから衝突まで",
        fig=("axis", dict(ss.AX_11, past=[ss.ax("neads11")], start=dict(cur="8:37:52"),
                          steps=[dict(add=[ss.ax("hit11"), ss.ax("air11")], cur="8:53"), dict(add=ss.ax("nine11")), dict()],
                          note="時刻は委員会報告の記録（北棟の時刻は資料で割れる＝委員会報告の値）",
                          src=ss.src(["委員会報告 p7", "委員会報告 p20", "委員会報告 p21"]))),
    ),
    # c424（3行）＝🔧 NEADS の画面（模式）で探し続ける → 3行目でビルにぶつかったという知らせ（台本の画＝帯に画面を重ねる → 画面の側に）
    "c424": dict(
        t="間に合わず", s="探し続ける NEADS（模式）",
        fig=("m21", dict(view="scope", start=dict(who="neads", dots="on", search="s1"),
                         steps=[dict(state=dict(search="s2")), dict(state=dict(search="s3")),
                                dict(tag=dict(t="ぶつかったという知らせ", at="news"))],
                         note="画面の形と点は模式（記録の画面ではない）", src=ss.src(["委員会報告 p20"]))),
    ),
    # c425（2行）＝同じ段。2行目で本部→国防総省の指揮所に×（戦闘機の護衛を頼まず＝p19）
    "c425": dict(
        t="本部の判断", s="本部が頼まなかったこと",
        fig=("m21", dict(view="chain", start=dict(who="bos", lit="3", short="on", cape="on"),
                         steps=[dict(), dict(state=dict(hqx="on"), tag=dict(t="戦闘機の護衛を頼まず", at="hqx"))],
                         note="段の形は模式", src=ss.src(["委員会報告 p19"]))),
    ),
    # c426（2行）＝3つの前提の1つ目に×（11便はトランスポンダを切った＝p31）
    "c426": dict(
        t="崩れた前提", s="1つ目の前提と11便",
        fig=("m21", dict(view="premise", start=dict(p1="on", p2="on", p3="on"),
                         steps=[dict(state=dict(x1="on"), tag=dict(t="11便：札が消えた", at="x1")), dict()],
                         rel=[dict(t="11便", src="委員会報告 p18")], note="箱の並びは模式（言葉は委員会報告から）",
                         src=ss.src(["委員会報告 p18", "委員会報告 p31"]))),
    ),
})
