# -*- coding: utf-8 -*-
"""つかみ c101–c107（7カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c1.py`）。
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
    'c101': dict(kind='写真',
               plan='S1-002:全体｜一覧の種類：実写｜見せ方：全面｜副題：出航するタイタニック号〈1912年4月10日・サウサンプトン〉｜動き：寄る（船首へ）｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：冒頭の1枚目＝この事故の船そのもの。c217・c922 の S2-033 は同じ写真の拡大＝離した｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`exploding in the air and throwing off white stars`）'),
    'c102': dict(kind='写真',
               plan='🔧 S8-625:全体｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号〈カルパチア号の甲板から撮られたとみられる・NARA〉｜動き：右へ（船首から船尾へ）｜権利：PD｜時期：後・救助｜人：なし｜出典の行：出典：米国立公文書館（NARA）｜注：この回の核の写真。S8-625 は4回まで（c102・c605・c811・cb06＝寄りを替える）｜新しい画（映像方針）：🔧 動きを「ゆっくり寄る」→「右へ流す」（冒頭の動きを散らす）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.58（`altogether we had seen eight of these white lights like white rockets`）・G2 p.14（`The Inspector's answer is 'Yes', and I entirely agree with him`）"),
    'c103': dict(kind='写真',
               plan='S5-359:全体｜一覧の種類：実写｜見せ方：全面｜副題：1912年4月、現場の近くで撮られた氷山〈NARA〉｜動き：左へ｜権利：PD｜時期：氷｜人：なし｜出典の行：出典：米国立公文書館（NARA）｜注：「衝突した氷山」とは名乗らない（materials §1-6）｜新しい画（映像方針）：台本どおり（動きを左へ）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.5（`the loss of 1,490 lives`）'),
    'c104': dict(kind='写真',
               plan='S6-480:全体｜一覧の種類：実写｜見せ方：全面｜副題：4月15日の朝、海の上のボート〈1912年・BnF〉｜動き：右へ（2隻のボートへ）｜権利：PD｜時期：後・救助｜人：遠景（⑤b で原寸）｜出典の行：出典：フランス国立図書館（BnF）｜注：人は遠景。語りの「救えたかもしれない」は決め所の画面にしない（10-07）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`remained approximately stationary until 5.15`）・G1 p.60（`Had she done so she might have saved many if not all of the lives that were lost`）'),
    'c105': dict(kind='写真',
               plan='N04:A1｜映像の素材 8.50秒・倍率 1.02（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（12.0〜20.5秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜注：640×426 を全面＝約3倍（ぼけは差し替えの理由にしない＝10-13）。音は使わない。区間は ⑤b-1 で実測の秒に合わせて動かす｜新しい画（映像方針）：台本どおり（区間を決めた＝船首の手すりとラスティクルの寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.2（`in 1990 the Secretary of State for Transport`）・G2 p.3（`I think it possible that she was seen`）'),
    'c106': dict(kind='写真',
               plan='🔧 S8-E03:全体｜一覧の種類：実写｜見せ方：全面｜副題：カルパチア号の乗客が撮ったとされるカリフォルニアン号〈1912年4月15日〉｜動き：寄る（ダビットの向こうの船へ）｜権利：PD｜時期：後・救助｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S8-E03 は3回まで（c106・c716・c931）｜新しい画（映像方針）：🔧 額装か全面か → 全面（写真は画面いっぱい・977px＝約2倍）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.3（`The Inspector considers that TITANIC was seen by CALIFORNIAN`…`but more likely that she was not seen`）・G2 送り状（`an Inspector from outside the Branch was appointed`）'),
    'c107': dict(kind='写真',
               plan='🔧 N04:A2｜映像の素材 12.10秒・倍率 1.01（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（36.0〜48.1秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜注：c105 と別の区間（c105＝手すりの寄り・c107＝船首の正面）。あいだに c106 の写真｜新しい画（映像方針）：🔧 Pexels の夜の海（イメージ）→ NOAA 2004 の船首の正面へ進む映像（冒頭は実写＝この事故の物だけ）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.40（`There was no moon`）'),
}

SPEC = {}
