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
    'c407': dict(kind='図・写真の頁',
               plan='台本の画：図 RG237（ボストン・センターのレーダー再生の画面・11便の札が消える所・FAA・Unrestricted）',
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
