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
               plan='台本の画：図 模式 同じ帯（ラングレー機の線＝実は11便の誤報で飛んだ）',
               src='委員会報告 p34（`The inaccurate accounts created the impression that the Langley scramble was a logical response to an actual hijacked aircraft`）'),
    'ca07': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（「14分」の札に×）',
               src='委員会報告 p34（`Thus the military did not have 14 minutes to respond to American 77, as testimony to the Commission in May 2003 suggested`）'),
    'ca08': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（「間に合ったように見えた」の札）',
               src='委員会報告 p34（`More than the actual events, inaccurate government accounts of those events made it appear that the military was notified in time to respond to two of the hijackings`）'),
    'ca09': dict(kind='写真',
               plan='P049｜副題：当日の夜のペンタゴン｜動き：右へ流す｜権利：A（米海軍の職務）｜出典の行：米海軍｜台本の画：実写 当日のペンタゴン（米軍の写真・A・別の点＝副題は絵を見て書く）',
               src='運輸省の監察総監の報告 CC-2006-085 p1（`did not investigate whether the inaccurate statements were knowingly false`・`referred to the Department of Defense (DOD) and Department of Transportation (DOT) Inspectors General`）'),
    'ca10': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（「誤り」の札から「監察総監」の札へ矢印）',
               src='運輸省の監察総監の報告 CC-2006-085 p2（`We did not find evidence to conclude that FAA officials knowingly made false`）・p3（`consider appropriate administrative action for the two current executives who did not act to correct the record with the Commission`）'),
    'ca11': dict(kind='写真',
               plan='🔧 WTC76N｜副題：事件の前の世界貿易センター（1976年）｜動き：上へ流す｜権利：D（米議会図書館蔵／知られた制限なし）｜出典の行：Balthazar Korab（米議会図書館蔵）｜注：🔧 語りが8:46の時刻＝両棟が燃える写真を置かない。夕暮れ・縦長｜台本の画（🔧映像方針で替えた＝元の予定）：実写 当日の世界貿易センター（A・別の点＝副題は絵を見て書く）',
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
               plan='台本の画：図 模式 同じ帯（11月の法律の札へつながる）',
               src='—'),
}

SPEC = {}
