# -*- coding: utf-8 -*-
"""終章　あの朝、持ち場にいた人たち cc01–cc10（10カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/cc.py`）。
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
    'cc01': dict(kind='写真',
               plan='P109｜副題：当日の夜のペンタゴン（崩れた西側）｜動き：ゆっくり寄る｜権利：A（米海軍の職務）｜出典の行：米海軍（PH2 Robert Houlihan）｜注：語りは NEADS・FAA の人＝人の写らない点｜台本の画：実写 当日のペンタゴン（米軍の写真・A・救助にあたる隊員・別の点＝副題は「当日のペンタゴンの救助」のように写っている人を書き、語りの NEADS・FAA の人と取り違えさせない。合わなければ人の写らない点か図）',
               src='委員会報告 p31（`We do not believe that the true picture of that morning reflects discredit on the operational personnel at NEADS or FAA facilities`）'),
    'cc02': dict(kind='写真',
               plan='P084｜副題：当日のペンタゴン（海軍別館から見た煙）｜動き：左へ流す｜権利：A（米海兵隊の職務）｜出典の行：米海兵隊（Cpl J. Ingersoll）｜注：語りは NEADS の将校＝人のほぼ写らない点｜台本の画：実写 当日のペンタゴン（米軍の写真・A・別の点＝副題は絵を見て書く）',
               src='委員会報告 p31（`NEADS commanders and officers actively sought out information, and made the best judgments they could on the basis of what they knew`）'),
    'cc03': dict(kind='写真',
               plan="LC210｜副題：当日の世界貿易センターの跡（第7ビルの足元の消防士）｜動き：2点を順に寄る｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：消防の犠牲の語り＝消防士（公務）｜台本の画：実写 当日の世界貿易センター（A・別の点・消防の人の顔＝職務＝副題は絵を見て書く）",
               src='委員会報告 p311（`The FDNY suffered 343 fatalities`・`the largest loss of life of any emergency response agency in history`・`The PAPD suffered 37 fatalities`・`The NYPD suffered 23 fatalities`）'),
    'cc04': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（4機と、軍に届いた知らせの印）',
               src='委員会報告 p45（`NORAD and the FAA were unprepared for the type of attacks launched against the United States on September 11, 2001`・`an unprecedented challenge they had never before encountered and had never trained to meet`）'),
    'cc05': dict(kind='写真',
               plan='🔧 P043｜副題：当日のペンタゴン（炎と救急車）｜動き：右へ流す｜権利：A（米海兵隊の職務）｜出典の行：米海兵隊（Cpl J. Ingersoll）｜注：🔧 DVIDS の別の窓 → 写真（運転席の人の方へ寄らない）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 DVIDS 122342（別の窓・隊員と消防＝副題「当日のペンタゴン」）',
               src="委員会報告 p31（`the NEADS air defenders had nine minutes' notice on the first hijacked plane`）"),
    'cc06': dict(kind='写真',
               plan="LCB20｜副題：当日のマンハッタン｜動き：左へ流す｜権利：C'（撮影者不詳・権利を放棄）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：遠くの通行人は顔の分からない遠景｜台本の画：実写 議会図書館 LC-B20（車内から見た通りと煙の柱・C'＝米議会図書館蔵（撮影者不詳）・遠くの人は顔の分からない遠景だけ・全画面＝副題「当日のマンハッタン」）",
               src='記念館（`The attacks killed 2,977 people from 90 nations: 2,753 people were killed in New York; 184 people were killed at the Pentagon; and 40 people were killed on Flight 93`）'),
    'cc07': dict(kind='図解',
               plan='台本の画：図 模式 数の帯（2,973＝2004年7月の委員会・2,977＝いまの数）',
               src='委員会報告 p311（`the nation suffered the largest loss of life—2,973—on its soil as a result of hostile attack in its history`）'),
    'cc08': dict(kind='図解',
               plan='台本の画：図 模式 同じ帯（2026年8月の札）',
               src='検視局（`announced the identification of a previously unknown victim of the September 11, 2001 terror attacks on the World Trade Center using the breakthrough technique of forensic investigative genetic genealogy`）'),
    'cc09': dict(kind='図解',
               plan='台本の画：図 模式 委員会報告の表紙の絵と「米政府の印刷局のサイト」の札',
               src='sources §1（govinfo の PDF＝200・md5 が手元と同じ・2026-10-11。⑥の時点でもう一度開く）'),
    'cc10': dict(kind='写真',
               plan='DV47｜区間 15.0〜21.0秒｜倍率 0.90（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：9月14日のペンタゴン（空撮）｜動き：映像｜権利：A（米空軍 第1戦闘カメラ隊の職務・DVIDS「PUBLIC DOMAIN」）｜出典の行：米空軍（DVIDS 122347）｜注：中庭の真上を回る（0.81倍・1秒1コマ）｜台本の画：実写 DVIDS 122347「Noble Eagle, Sep 14」空撮（別の窓・PD・SD＝全画面・ゆっくり引く＝副題「9月14日のペンタゴン（空撮）」）',
               src='—'),
}

SPEC = {}
