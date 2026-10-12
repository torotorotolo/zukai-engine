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

# ── 🆕 ⑤b-2（2026-10-12）：冒頭は実写だけ（記憶 feedback-jiko-opening-flashy-but-faithful・映像方針 §1＝映像7・写真2）──
#   写真＝束 `ref/ep21/`（`qa_out/ep21_assets.py build`・権利の台帳 assets.json）・映像＝DVIDS 3本・WHTV 606／1501（`footage.USE` の EP21_USE＝
#   `ep21_assets.py use`・ひかえの静止画 fb_<カット>＝`ep21_assets.py fb`＝焼くときと同じ切り口）。4:3 の SD 映像は額装＋地のぼかし・16:9 の
#   WHTV 606 は全画面（映像方針 了承② 決め4）。副題は PLAN（映像方針の一覧＝了承②）のまま＝焼いた絵を原寸で見てから最終に。
#   見出しは7字以内の名札（語りの1文の頭・尻を切り取らない＝門番 echo）。色は回の既定で原色（build_jiko.PHOTO_KEEP_EP）
_LC17 = P("lc_a05_a17")
_NASA = P("nasa_iss003_e_5388")
_NASA_END = ss.focus(_NASA, 0.555, 0.44, zoom=1.20)   # マンハッタンの南の端から南東へ流れる煙（横 0.48〜0.60・縦 0.40〜0.48＝⑤b-2 に目盛りの絵で測った）

SPEC = {
    # c101（6.5秒）＝DVIDS 122342 ショット 4（駐車場ごしのペンタゴンと煙）・0.62倍（133と134のあいだでカメラが振れる＝4秒だけ）
    "c101": ss.vid("c101", t="4機の乗っ取り", s="2001年9月11日のペンタゴン"),
    # c102（11.2秒）＝議会図書館 LC-A05-A17（スライドの走査＝四隅と左右に台紙の黒い縁 約1.3%）。全画面で右へ流す＝寄り 1.12・寄せ 0.2→0.8
    #   （pan_r は寄せ 0→1＝端の黒い縁が入る）。見える縦 0.13〜0.87＝塔1本と大きな雲・手前のミッドタウンのビル
    "c102": dict(photo=_LC17, **ss.kind(_LC17), cam={"from": (0.2, 0.5, 1.12), "to": (0.8, 0.5, 1.12)},
                 t="4機の行方", s="当日のマンハッタン"),
    # c103（3.9秒）＝NASA ISS003-E-5388。全体（寄り 1.0）から煙へ寄る（1.20）
    "c103": dict(photo=_NASA, **ss.kind(_NASA), cam={"from": (0.5, 0.5, 1.0), "to": (_NASA_END["xbias"], _NASA_END["bias"], _NASA_END["zoom"])},
                 t="犠牲者の数", s="宇宙から見たニューヨークの煙（当日）"),
    # c104（7.3秒）＝DVIDS 122343 ショット 1（芝生ごしの燃える西側・消防車・遠くの隊員）・等速
    "c104": ss.vid("c104", t="9分前の知らせ", s="当日のペンタゴン"),
    # c105（3.4秒）＝DVIDS 122342 ショット 9（消防隊の放水）・0.89倍
    "c105": ss.vid("c105", t="前触れなし", s="当日のペンタゴン"),
    # c106（7.4秒）＝聞き役の問い（赤）＋答え。WHTV 1501 ショット 13（レンウィック美術館の前・制服の警官・遠くの通行人）・等速。
    #   🔴 媒体はリポの中の切り出し（`ref/ep21/clip/`・footage.media_of の注）
    "c106": ss.vid("c106", t="気づいた管制官", s="当日のワシントン（ホワイトハウスの近くの通り）"),
    # c107（5.7秒）＝WHTV 606 ショット 41（大統領専用機と空軍兵3人）・16:9＝全画面・右端のレンズの縁の影は寄せで外す・等速
    "c107": ss.vid("c107", t="2機目の知らせ", s="当日の午後、ルイジアナ州の空軍基地"),
    # c108（8.1秒）＝DVIDS 122347 ショット 2（9月14日の空撮・壊れた西側と復旧のテント）・0.74倍
    "c108": ss.vid("c108", t="2つの問い", s="9月14日のペンタゴン（空撮）"),
    # c109（5.7秒）＝聞き役の問い（赤）＋答え。DVIDS 122343 ショット 23（規制線の中の FBI と警察）・等速
    "c109": ss.vid("c109", t="録音とレーダー", s="当日のペンタゴン"),
}
