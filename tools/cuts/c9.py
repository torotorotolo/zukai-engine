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
               plan='台本の画：図 模式 同じ帯（「撃墜」の札に×）',
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
               plan='台本の画：図 模式 首都の上の2組の戦闘機（ラングレーと、アンドルーズの州兵）',
               src='委員会報告 p44（`By 10:45 there was, however, another set of fighters circling Washington that had entirely different rules of engagement`・`launched out of Andrews Air Force Base in Maryland in response to information passed to them by the Secret Service`・`the decision to shoot rests in the cockpit`）'),
    'c917': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（10:03:11 墜落・10:10 から 10:15 許可・10:31 NEADS へ）',
               src='—'),
    'c918': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯',
               src='委員会報告 p45（`NORAD officials have maintained that they would have intercepted and shot down United 93. We are not so sure.`）'),
    'c919': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（見つける・追う・命令を渡す、の3つの箱が空白）',
               src='委員会報告 p45（`to locate the flight, receive authorization to shoot it down, and communicate the order to the pilots`・`did not know where United 93 was located, and did not have shootdown authorization`）'),
    'c920': dict(kind='写真',
               plan='WH920｜副題：当日の午後、ネブラスカ州の空軍基地（画面越しの会議）｜動き：ゆっくり寄る｜権利：A（ホワイトハウスの写真係の職務）｜出典の行：Eric Draper（Courtesy George W. Bush Presidential Library）｜台本の画：実写 オファット空軍基地での会議（ホワイトハウスの写真係・当日の午後・A・全画面＝副題「当日の午後、ネブラスカ州の空軍基地」）',
               src='委員会報告 p326（`Air Force One arrived at Offutt at 2:50 P.M.`・`At about 3:15, President Bush met with his principal advisers through a secure video teleconference`）'),
    'c921': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（その朝の4機と命令の時刻をすべて重ねる）',
               src='—'),
}

SPEC = {}
