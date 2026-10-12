# -*- coding: utf-8 -*-
"""つかみ c101–c109（9カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c1.py`）。
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
    'c101': dict(kind='写真',
               plan='DV42｜区間 130.0〜134.0秒｜倍率 0.62（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：2001年9月11日のペンタゴン｜動き：映像｜権利：A（米空軍 第11通信隊の職務・DVIDS「PUBLIC DOMAIN」）｜出典の行：米空軍（DVIDS 122342）｜注：駐車場ごしのペンタゴンと煙。133秒と134秒のあいだでカメラが振れる＝4秒だけ（÷365 の見込み0.68倍→⑤a の実測で0.62倍＝下限0.6の内。130秒より前はカメラが動く＝区間は伸ばさない・⑤b-1）｜台本の画：実写 DVIDS 122342「Noble Eagle, Sep 11 Part 1」（米空軍 第11通信隊・PD・SD＝全画面・煙と消防車の遠景・ゆっくり寄る・秒は映像方針で＝副題「2001年9月11日のペンタゴン」）',
               src='委員会報告 p1（`Tuesday, September 11, 2001, dawned temperate and nearly cloudless`）・p4（`The 19 men were aboard four transcontinental flights`）'),
    'c102': dict(kind='写真',
               plan="LC17｜副題：当日のマンハッタン｜動き：右へ流す｜権利：C'（撮影者不詳・権利を放棄＝議会図書館の説明）｜出典の行：米議会図書館蔵（撮影者不詳）｜注：塔1本と大きな雲＝時刻は言わない（②③の見本帳で見た）｜台本の画：実写 議会図書館 LC-A05-A17（ミッドタウンの向こうに立ちのぼる煙の雲・C'＝米議会図書館蔵（撮影者不詳）・全画面・右へ流す・時刻は言わない＝副題「当日のマンハッタン」）",
               src='委員会報告 p7（`crashed into the North Tower`）・p8（`struck the South Tower`）・p10（`crashed into the Pentagon`）・p14（`plowed into an empty field in Shanksville`）'),
    'c103': dict(kind='写真',
               plan='NASA｜副題：宇宙から見たニューヨークの煙（当日）｜動き：ゆっくり寄る｜権利：A（NASA の職務）｜出典の行：NASA｜注：②③の見本帳で見た｜台本の画：実写 NASA ISS003-E-5388（国際宇宙ステーションから見たニューヨーク一帯と南東へ流れる煙・A・全画面・ゆっくり寄る・時刻は言わない＝副題「宇宙から見たニューヨークの煙（当日）」）',
               src='記念館（`The attacks killed 2,977 people`）'),
    'c104': dict(kind='写真',
               plan='DV43｜区間 9.0〜17.0秒｜倍率 1.10（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日のペンタゴン｜動き：映像｜権利：A（米空軍の職務・DVIDS「PUBLIC DOMAIN」）｜出典の行：米空軍（DVIDS 122343）｜注：芝生ごしの燃える西側・消防車・遠くの隊員（負傷者なし＝1秒1コマ）｜台本の画：実写 DVIDS 122343「Noble Eagle, Sep 11 Part 2」（米空軍・PD・SD＝全画面・救助にあたる隊員・負傷者と遺体の写らない窓だけ＝副題「当日のペンタゴン」）',
               src='委員会報告 p21（`NEADS received notice of the hijacking nine minutes before it struck the North Tower`）'),
    'c105': dict(kind='写真',
               plan='DV42｜区間 332.0〜335.0秒｜倍率 0.89（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日のペンタゴン｜動き：映像｜権利：A（米空軍 第11通信隊の職務・DVIDS「PUBLIC DOMAIN」）｜出典の行：米空軍（DVIDS 122342）｜注：消防隊の放水（1秒1コマ）｜台本の画：実写 DVIDS 122342（別の窓・放水する消防車＝副題「当日のペンタゴン」）',
               src='委員会報告 p31（`no advance notice on the second, no advance notice on the third, and no advance notice on the fourth`）'),
    'c106': dict(kind='写真',
               plan='W1501｜区間 382.0〜390.0秒｜倍率 1.07（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日のワシントン（ホワイトハウスの近くの通り）｜動き：映像｜権利：A（WHCA の職務・大統領図書館「Records of White House Evacuation on September 11, 2001」）｜出典の行：Courtesy George W. Bush Presidential Library（WHTV 1501）｜注：レンウィック美術館の前・制服の警官（公務）・通行人は遠く小さい＝モザイク不要。ホワイトハウスそのものは写らない｜台本の画：実写 WHTV 1501 ホワイトハウスからの退避（WHCA・A・SD＝全画面・私人の近景は顔だけモザイク・音は使わない＝副題「当日のホワイトハウス」）',
               src='委員会報告 p22（`we may have a hijack`）'),
    'c107': dict(kind='写真',
               plan='W606｜区間 499.0〜506.0秒｜倍率 1.24（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日の午後、ルイジアナ州の空軍基地｜動き：映像｜権利：A（ホワイトハウス通信局 WHCA＝国防総省の機関の職務・大統領図書館「public domain」）｜出典の行：Courtesy George W. Bush Presidential Library（WHTV 606）｜注：大統領専用機と空軍兵3人（テープの順＝現地11:36の声明のあと）。右端のレンズの縁の影＝右を少し切る（PD）｜台本の画：実写 WHTV 606 バークスデール空軍基地に着いた大統領専用機（WHCA・NARA 6171389・A・SD＝全画面・手前の記者は顔だけモザイク＝副題「当日の午後、ルイジアナ州の空軍基地」）',
               src='委員会報告 p23（`The notice came at about the time the plane was hitting the South Tower`）'),
    'c108': dict(kind='写真',
               plan='DV47｜区間 79.0〜85.0秒｜倍率 0.74（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：9月14日のペンタゴン（空撮）｜動き：映像｜権利：A（米空軍 第1戦闘カメラ隊の職務・DVIDS「PUBLIC DOMAIN」）｜出典の行：米空軍（DVIDS 122347）｜注：壊れた西側と復旧のテント（÷365 の見込み0.78倍→⑤a の実測で0.74倍）｜台本の画：実写 DVIDS 122347「Noble Eagle, Sep 14」空撮（米空軍 第1戦闘カメラ隊・PD・SD＝全画面・ゆっくり回り込む＝副題「9月14日のペンタゴン（空撮）」）',
               src='—'),
    'c109': dict(kind='写真',
               plan='DV43｜区間 484.0〜490.0秒｜倍率 1.06（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日のペンタゴン｜動き：映像｜権利：A（米空軍の職務・DVIDS「PUBLIC DOMAIN」）｜出典の行：米空軍（DVIDS 122343）｜注：規制線の中の FBI と警察（公務）・487秒に制服の人が横切る｜台本の画：実写 DVIDS 122343（別の窓・建物の西側と隊員＝副題「当日のペンタゴン」）',
               src='委員会報告 p20（`Radar data show the Otis fighters were airborne at 8:53`）・p20（`NEADS: Is this real-world or exercise?`）・スタッフ声明 p18（`taped conversations at NEADS, but in taped conversations at FAA centers`）'),
}

SPEC = {}
