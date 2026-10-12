# -*- coding: utf-8 -*-
"""第6章　空を閉じる c701–c716（16カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c7.py`）。
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
    'c701': dict(kind='写真',
               plan="LCA05｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：右へ流す｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：9:25 の語り｜台本の画：実写 当日の世界貿易センター（A・Commons の説明に当日の日付がある14点から・両棟が燃える時刻の点だけ・全画面・右へ流す＝副題は絵を見て書く）",
               src='図表 p33（`nationwide ground stop`）・委員会報告 p25（`the Command Center ordered one at 9:25`）'),
    'c702': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（空港の点が止まる＝離陸の停止・「本部は話し合い中」の札）',
               src='委員会報告 p25（`A manager at the Herndon Command Center asked FAA headquarters if they wanted to order a`・`While this was being discussed by executives at FAA headquarters, the Command Center ordered one at 9:25`）'),
    'c703': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（アメリカン航空の便の点が止まる＝9:00 北東部・9:05〜9:10 全米）',
               src='委員会報告 p9（`He ordered all American Airlines flights in the Northeast that had not taken off to remain on the ground`・`extended the ground stop nationwide`）・p10（`nationwide ground stop between 9:05 and 9:10`）'),
    'c704': dict(kind='図解',
               plan='台本の画：図 模式 コマンドセンターの卓の配置（人は描かない）',
               src='委員会報告 p29（`The Command Center’s national operations manager, Ben Sliney`）'),
    'c705': dict(kind='写真',
               plan='P122｜副題：当日のペンタゴンの煙（遠くから）｜動き：ゆっくり寄る｜権利：A（米海軍の職務）｜出典の行：米海軍｜台本の画：実写 当日のペンタゴン（米軍の写真・A・別の点・煙の柱の遠景＝副題は絵を見て書く）',
               src='委員会報告 p29（`At 9:42, the Command Center learned from news reports that a plane had struck the Pentagon`）・スタッフ声明 p15（`At 9:42, Command Center learned from television news reports`）'),
    'c706': dict(kind='写真',
               plan="LCA10｜副題：当日の世界貿易センター（ミッドタウンから見た煙）｜動き：ゆっくり引く｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：9:45ごろの語り｜台本の画：実写 当日の世界貿易センター（A・別の点・両棟が燃える時刻の点だけ＝副題は絵を見て書く）",
               src='委員会報告 p29（`ordered all FAA facilities to instruct all aircraft to land at the nearest airport`）'),
    'c707': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（飛んでいる機の点が、いちばん近い空港へ向かう矢印）',
               src='—'),
    'c708': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（命令の時刻の札は空白）',
               src='委員会報告 p29（`This was an unprecedented order`）'),
    'c709': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（命令の札を2つ並べる＝報告書と証言・時刻と言葉は字幕だけ）',
               src='運輸長官の証言（`at approximately 9:45 a.m.`・`I gave the FAA the final order for all civil aircraft to land at the nearest airport as soon as possible`）'),
    'c710': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（2つの札に「報告書」「本人の証言」）',
               src='—'),
    'c711': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（点が減っていく・数の札「約4,500機」）',
               src='委員会報告 p29（`The air traffic control system handled it with great skill, as about 4,500 commercial and general aviation aircraft soon landed without incident`）'),
    'c712': dict(kind='写真',
               plan='WH712｜副題：当日、大統領専用機の機内｜動き：ゆっくり寄る｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Eric Draper（Courtesy George W. Bush Presidential Library）｜注：電話をする大統領（サラソタからの飛行中＝説明）・撮影の時刻は書かない｜台本の画：実写 大統領専用機の機内で電話をする大統領（ホワイトハウスの写真係・A・全画面・ゆっくり寄る・撮影の時刻は書かない＝副題「当日、大統領専用機の機内」）',
               src='委員会報告 p39（`Air Force One departed at about 9:54 without any fixed destination`）'),
    'c713': dict(kind='写真',
               plan='🔧 W606｜区間 195.5〜200.5秒｜倍率 1.13（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日、ルイジアナ州の空軍基地に着いた専用機｜動き：映像｜権利：A（ホワイトハウス通信局 WHCA＝国防総省の機関の職務・大統領図書館「public domain」）｜出典の行：Courtesy George W. Bush Presidential Library（WHTV 606）｜注：🔧 写真（手前に記者）→ WHTV 606 の到着の区間（タラップを降りる人・196〜200秒を1秒おき）＝モザイク不要｜台本の画（🔧映像方針で替えた＝元の予定）：実写 バークスデール空軍基地の大統領（ホワイトハウスの写真係・A・手前の記者は顔だけモザイク・全画面＝副題「当日、ルイジアナ州の空軍基地」）',
               src='委員会報告 p325（`Air Force One flew to Barksdale Air Force Base in Louisiana`）'),
    'c714': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（点が空港へ降りきる）',
               src='委員会報告 p31（`thought outside the box in recommending a nationwide alert, in ground-stopping local traffic, and, ultimately, in deciding to land all aircraft and executing that unprecedented order flawlessly`）'),
    'c715': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図',
               src='—'),
    'c716': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（9:42 に報道で知る〜9:46・93便はすでに乗っ取られている）',
               src='委員会報告 p29（`At 9:46 the Command Center updated FAA headquarters that United 93 was now "twenty-nine minutes out of Washington, D.C."`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-12）：図解 第6章（11カット）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「空を閉じる」と4字以上同じ並びを見出し・副題に入れない（門番 dup）。人は描かない・人の名前を画面に出さない（役職だけ）。
#      命令の時刻と言葉は字幕だけ（c708〜c710 の札は「時刻：――」）。全米の空港と空の機の点は模式（数は記録ではない＝「約4,500機」は札と字幕）
_U = "陸の形は Natural Earth・空港と機の点は模式（数は記録ではない）"
SPEC.update({
    # c702（2行）＝全米の地図（空港の点）。本部は話し合い中 → 2行目で 9:25 コマンドセンターが離陸を止める（p25）
    "c702": dict(
        t="離陸の停止", s="全米の空港の点",
        fig=("m21", dict(view="us", start=dict(air="on"),
                         steps=[dict(tag=dict(t="本部は話し合い中", at="top")),
                                dict(state=dict(stop="on"), tag=dict(t="9:25 離陸を止める", at="top2"))],
                         rel=[dict(t="9:25", src="委員会報告 p25")], note=_U, src=ss.src(["委員会報告 p25"]))),
    ),
    # c703（2行）＝同じ地図。9:00ごろ アメリカン航空が北東部で止める → 2行目で 9:05〜9:10 全米へ（p9・p10）
    "c703": dict(
        t="航空会社の判断", s="アメリカン航空の離陸の停止",
        fig=("m21", dict(view="us", start=dict(air="on"),
                         steps=[dict(state=dict(aa="ne"), tag=dict(t="9:00ごろ 北東部で", at="top")),
                                dict(state=dict(aa="all"), tag=dict(t="9:05〜9:10 全米へ", at="top2"))],
                         rel=[dict(t="9:00", src="委員会報告 p9"), dict(t="9:05〜9:10", src="委員会報告 p10")], note=_U,
                         src=ss.src(["委員会報告 p9", "委員会報告 p10"]))),
    ),
    # c704（2行）＝コマンドセンターの運用の部屋（上から・模式）。2行目で全米の運用の責任者の席（名前は画面に出さない）
    "c704": dict(
        t="運用のまとめ役", s="全米の空を見渡す部屋",
        fig=("m21", dict(view="desk", steps=[dict(), dict(state=dict(lead="on"), tag=dict(t="全米の運用の責任者の席", at="lead"))],
                         note="人は描かない・卓の並びは模式（写真や図面によらない）", src=ss.src(["委員会報告 p29"]))),
    ),
    # c707（2行）＝全米の地図。空の機の点 → 2行目でいちばん近い空港への矢印（p29）
    "c707": dict(
        t="全機を降ろす", s="空の機と全米の空港",
        fig=("m21", dict(view="us", start=dict(air="on"),
                         steps=[dict(state=dict(fly="on")), dict(state=dict(land="arrow"), tag=dict(t="いちばん近い空港へ", at="top"))],
                         note=_U, src=ss.src(["委員会報告 p29"]))),
    ),
    # c708（2行）＝同じ地図＋命令の札（時刻は空白）→ 2行目で報告書に時刻の記載なし（p29）
    "c708": dict(
        t="命令の時刻", s="報告書に書かれた命令",
        fig=("m21", dict(view="us", start=dict(air="on", fly="on", land="arrow"),
                         steps=[dict(state=dict(order="one")), dict(tag=dict(t="時刻の記載なし", at="b1"))],
                         note=_U, src=ss.src(["委員会報告 p29"]))),
    ),
    # c709（2行）＝同じ地図。もう1つの命令の札（運輸長官の証言＝時刻と言葉は字幕だけ）
    "c709": dict(
        t="もう1つの命令", s="のちの公聴会での証言",
        fig=("m21", dict(view="us", start=dict(air="on", fly="on", land="arrow", order="one"),
                         steps=[dict(state=dict(order="two")), dict()],
                         note=_U, src=ss.src(["運輸長官の証言"]))),
    ),
    # c710（3行）＝同じ地図。2行目で「報告書」→ 3行目で「本人の証言」
    "c710": dict(
        t="誰の命令か", s="2つの命令の札",
        fig=("m21", dict(view="us", start=dict(air="on", fly="on", land="arrow", order="two"),
                         steps=[dict(), dict(tag=dict(t="報告書", at="b1")), dict(tag=dict(t="本人の証言", at="b2"))],
                         note=_U, src=ss.src(["委員会報告 p29", "運輸長官の証言"]))),
    ),
    # c711（2行）＝同じ地図。空の機が空港へ降りきる → 2行目で約4,500機（p29）
    "c711": dict(
        t="降りた機", s="空から全米の空港へ",
        fig=("m21", dict(view="us", start=dict(air="on", fly="on", land="arrow"),
                         steps=[dict(state=dict(land="down")), dict(tag=dict(t="約4,500機", d="事故なく降りる", at="top"))],
                         rel=[dict(t="約4,500機", src="委員会報告 p29")], note=_U, src=ss.src(["委員会報告 p29"]))),
    ),
    # c714（2行）＝同じ地図（空に機が無い・離陸は止まったまま）。2行目で委員会の評価（p31）
    "c714": dict(
        t="管制の対応", s="空の機が降りたあとの全米",
        fig=("m21", dict(view="us", start=dict(air="on", stop="on", fly="on", land="down"),
                         steps=[dict(), dict(tag=dict(t="空の流れを止めきる", d="委員会の評価", at="top"))],
                         note=_U, src=ss.src(["委員会報告 p31"]))),
    ),
    # c715（2行）＝同じ地図。2行目で軍への知らせは遅れたまま
    "c715": dict(
        t="陰の遅れ", s="空を止めた朝の、もう1つの面",
        fig=("m21", dict(view="us", start=dict(air="on", stop="on", fly="on", land="down"),
                         steps=[dict(), dict(tag=dict(t="軍への知らせは遅れたまま", at="top"))],
                         note=_U, src=ss.src(["委員会報告 p31"]))),
    ),
    # c716（3行）＝その朝の帯（AX_MORN）。9:42 報道で知る（沈める）→ 9:28 93便の乗っ取り → 9:46 93便の位置を本部へ（p11・p29）
    "c716": dict(
        t="4機目は", s="空の機が降りていくあいだの93便",
        fig=("axis", dict(ss.AX_MORN, past=[ss.ax("news42")], start=dict(cur="9:42"),
                          steps=[dict(add=ss.ax("hj93")), dict(add=ss.ax("upd93"), cur="9:46"), dict()],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p11", "委員会報告 p29"]))),
    ),
})
