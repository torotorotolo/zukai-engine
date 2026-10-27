# -*- coding: utf-8 -*-
"""第3章　衝突 c401–c416（16カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c4.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep26/make_plan26.py` で
  映像方針の一覧 `ref/ep26/eizou_build/list26.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep26/eizou_list26.md`）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  🔴 額装・帯の写真は静止（26本目から＝`build_jiko.FRAME_STILL`）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  ⚠️ 人＝乗員・ほかの船の船長と航海士と通信士・審問の長は名前＋役職／会社の人とドンキーマンは役職だけ／乗客は名前なし（①・承認①）。
     名前の載る紙面・頁は注の「…外」のとおり寄る範囲から名前を外す
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c401': dict(kind='フリー素材',
               plan='X-sea-stars｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 9.27秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：星の夜の海｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：⑤b で1本ずつ原寸｜新しい画（映像方針）：台本どおり（月の写らないもの）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.40（`There was no moon, the stars were out`）・G1 p.39（`there is not much wind`…`a flat calm`）'),
    'c402': dict(kind='写真',
               plan='S3-736:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：二等航海士と一等航海士〈1912年4月11日・クイーンズタウン〉｜動き：静止｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S3-736 は c513 と2回｜新しい画（映像方針）：台本どおり（縦長・小さい＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.39（`if it becomes at all doubtful let me know at once`…`at 9.30 the master went to his room`…`to keep a sharp lookout for ice, particularly small ice and growlers`）'),
    'c403': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：船橋と見張り台の当直（航海士・操舵手・見張り・鐘と電話の線）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.39（`at 10 o'clock Mr. Lightoller handed over the watch to Mr. Murdoch, the first officer`…`we might be up around the ice any time now`）"),
    'c404': dict(kind='写真',
               plan='🔧 S1-076:全体｜一覧の種類：実写｜見せ方：全面｜副題：クイーンズタウンに着くタイタニック号〈1912年4月11日〉｜動き：左へ｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S1-017 は c415 へ｜新しい画（映像方針）：🔧 S1-017（岸壁に止まった船）→ 海を進む船（語り＝全速のまま）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.80（`about 22 knots`）・G2 p.4（`normal full speed (about 22 knots) was maintained`）'),
    'c405': dict(kind='写真',
               plan='🔧 S3-810:全体｜一覧の種類：実写｜見せ方：全面｜副題：見張りのフレデリック・フリート｜動き：寄る（顔へ）｜権利：PD｜時期：後・審問｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：撮影の時と所は ⑤b で（分かれば副題に年）｜時期の門番の例外＝見張り本人の肖像（審問のころの写真）＝場面の写真ではない（衝突の場面は c406〜c411 の模式）｜新しい画（映像方針）：🔧 額装 → 全面（2560px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.41（`three blows on the gong`…`Iceberg right ahead`）・G2 p.1（`at about 2340 hrs ship's time`）"),
    'c406': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：舵の号令（ハード・ア・スターボード）と左へ回る船首の矢印｜合図：🔁 横から→上から（前の図 c403）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.41（`almost simultaneously with the three-gong signal Mr. Murdoch, the officer of the watch, gave the order`）・G2 p.4（`because of the helm orders then in use, was to direct the ship's head to port`）"),
    'c407': dict(kind='写真',
               plan='S1-020:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：タイタニック号の船首〈1912年4月4日・サウサンプトン〉｜動き：静止｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（縦長＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.41（`Stop. full speed astern`…`the ship's head had fallen off about two points to port, when she collided with an iceberg well forward on her starboard side`）"),
    'c408': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：37秒の見積もり（オリンピック号の試験・約430メートル・約460メートル手前）｜新しい画（映像方針）：台本どおり（札に「見積もり」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`from various experiments subsequently made with the steamship Olympic, a sister ship to the Titanic`…`about 37 seconds would be required`）'),
    'c409': dict(kind='写真',
               plan='🔧 S5-365:全体｜一覧の種類：実写｜見せ方：全面｜副題：1912年4月20日の氷山〈ブレーメン号の船員が撮った〉｜動き：右へ｜権利：PD｜時期：氷｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 額装 → 全面｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`500 yards was about the distance at which the`）'),
    'c410': dict(kind='写真',
               plan='🔧 S2-724:全体｜一覧の種類：実写｜見せ方：全面｜副題：船橋の船長〈1912年4月10日の朝〉｜動き：寄る｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 額装 → 全面（2040px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`The master rushed out onto the bridge`…`I hard-a-starboarded and reversed the engines, and I was going to hard-a-port round it, but she was too close`）'),
    'c411': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：船首から約90メートルの傷の範囲と前から6つの区画の名・10秒の帯｜合図：🔁 上から→横から（前の図 c408）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.42（`the damage extended over a length of about 300 feet`…`she would have passed through 300 feet in less than 10 seconds`）'),
    'c412': dict(kind='写真',
               plan='🔧 S10-871:全体｜一覧の種類：実写｜見せ方：全面｜副題：1912年の本の図〈An Unsinkable Titanic・p.129〉＝裂け目の札は本の見立て｜動き：右へ（区画に沿って）｜権利：PD｜時期：文書｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：⚠️ 「裂け目」は1912年の本の見立て（NIST は継ぎ目の開き＝legend §3-2）＝副題で断る｜新しい画（映像方針）：🔧 額装 → 全面（3170px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.45（`water came into the five forward compartments to a height of about 14 feet above the keel in the first 10 minutes`…`the ship's pumps could not possibly have coped`）"),
    'c413': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：壁で仕切った区画の並び・前の5つに水・壁を越えて後ろへ｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.45（`and so on in succession to the other boiler rooms till the ship would ultimately fill and sink`）'),
    'c414': dict(kind='フリー素材',
               plan='X-sea-calm｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 8.10秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：静かな夜の海｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜新しい画（映像方針）：台本どおり（月の写らないもの）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.4（`Between collision and foundering the ship lay stopped`）・G2 p.7（`the ship must have drifted some distance before she foundered`…`it is an important feature in this reappraisal`）'),
    'c415': dict(kind='写真',
               plan='🔧 S1-017:全体｜一覧の種類：実写｜見せ方：全面｜副題：サウサンプトンのタイタニック号〈1912年4月9日〉｜動き：右へ｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 S1-008（c304 の S1-013 と同じ写真）→ S1-017（別の写真）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.60（`The Titanic collided with the berg at 11.40`）・G1 p.49（`The collision took place at 11.40 p. m. (ship’s time)`）・G2 p.1（`at about 2340 hrs ship's time`）・G2 p.3（`struck the iceberg at 2345 hrs`）"),
    'c416': dict(kind='図解',
               plan='一覧の種類：帯｜見る向き：時間の線｜見た目の型：タイタニック号の時計の夜の帯（11:40・0:15・0:45ごろ・2:20）｜合図：🔁 横から→時間の線（前の図 c413）｜新しい画（映像方針）：台本どおり（札は「タイタニック号の時計」・ほかの船の時刻は並べない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.49（`at about 12.05 the order was given to uncover the 14 boats under davits`）・G1 p.54（`At 12.15 a. m. the distress signal CQD was sent`）・G1 p.85（`Two twenty a. m. (ship's time) April 15`）"),
}

SPEC = {}

# 🆕 ⑤b-2（2026-10-27）：c404 だけ先に書いた＝字幕の試し焼き（聞き役の赤「速さは、落としていたの？」と括弧つきの行「時速約41キロ（22ノット）」が
#   1カットにそろう＝冒頭 c101〜c107 に括弧の行が無い）。一覧どおり（全面・左へ・副題は list26 の sub）。⚠️ ⑤b-7 で写真をつなぐときに動きと寄せを見直してよい
_S1076 = P("s1_076")
SPEC.update({
    # c404（2行・4.6秒）＝クイーンズタウンに着くタイタニック号（船は y 0.30〜0.65）＝船の高さで左へ
    "c404": dict(photo=_S1076, **ss.mv(_S1076, "l", fy=0.47), side="none", color=1.0,
                 t="全速のまま", s="クイーンズタウンに着くタイタニック号〈1912年4月11日〉"),
})
