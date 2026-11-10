# -*- coding: utf-8 -*-
"""第3章　「ハドソン川に降りる」 c401–c423（23カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c4.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep32/make_plan32.py` で
  映像方針の一覧（`ref/ep32/eizou_build/make_list32.py`＝了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep32/eizou_list32.md`＝⑤b は一覧に従う）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  🔴 額装・帯の写真は静止（`build_jiko.FRAME_STILL_EP` に ep32）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。
  🔴 写真は画面いっぱい・色は原本（`build_jiko.PHOTO_KEEP_EP` に ep32）・BY-SA は額装・紙面と調査の写真も額装。説明カットの地は写真を暗くするだけ（8:1・衛星と夜の写真は地にしない）。
  🔴 VTS（沿岸警備隊の監視カメラ）は等速・止めなし・頭から使う・同じ秒を2回使わない（区間は一覧の動きの欄＝make_list32 の門番）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  🔴 この回の線＝語りと画面に名前を出すのは機長と副操縦士だけ（初出 c203・c205）・客室乗務員・管制官・救助の人は立場だけ・乗客は名前なし・
     NTSB・FAA・議員・知事・監督・俳優は役職で・「犠牲」「死亡」は言わない・「208秒」は使わず「約3分半」・映画は c517〜c518・c520 だけ
     ＝図でも同じ（紙面・写真に名前の字が写る＝親が絵を見て切る・船の名も読ませない）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c401': dict(kind='図解',
               plan='SAT:飛んだ道｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：飛んだ道〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p189（`DEP ok uh, you need to return to LaGuardia? turn left heading of uh two two zero.`）'),
    'c402': dict(kind='図解',
               plan='🔧 地：GA1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：交信の相手の札＝出発の管制〈レーダー〉・ラガーディアの管制塔・テターボロの管制・1549便｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈管制室のレーダーの画面〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`instructed the flight crew to contact the New York Terminal Radar Approach Control (TRACON) LGA departure controller`）'),
    'c403': dict(kind='文字の頁',
               plan='R191｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録B｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p191（`do you want to try to land runway one three?`）・ド#40p10（`runway 13 would be best and he suggested that runway to the pilot`）'),
    'c404': dict(kind='フリー素材',
               plan='X404｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：冬の川を上から〈場所は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src="報p191（`RDO-1 we're unable. we may end up in the Hudson.`）・報p105（`About 1 minute after the bird strike, it was evident to the flight crew that landing at an airport may not be an option`）"),
    'c405': dict(kind='図解',
               plan='🔧 地：GS1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：左のエンジンの札＝機長の言葉「少し戻ってきた」｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈冬の空〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`At 1528:25, the captain stated, “The left one’s [engine] coming back up a little bit.”`）・報p97（`neither engine was able to produce sufficient power to sustain flight after ingesting these birds`）'),
    'c406': dict(kind='図解',
               plan='SAT:ラガーディア空港 滑走路｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：ラガーディア空港の滑走路〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`At 1528:31, the LGA departure controller stated that it was going to be “left traffic for runway three one,” and the captain responded, “unable.”`）・報p44（`At 1528:37, the ATCT cab coordinator advised the LGA departure controller that`…`runway 4 is also available, if he needs it`）・ド#40p10（`heard LGA tower state that runway 4 was available which he offered to the pilot`）'),
    'c407': dict(kind='図解',
               plan="🔧 地：GA1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：言葉｜副題：よく言われる話「管制の指示を断った」→ 記録の言葉「unable」〈できない〉・「we can't do it」〈無理だ｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈管制室のレーダーの画面〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）",
               src='報p19（`the LGA departure controller asked the captain if he wanted to try to land on runway 13 at LGA if it was available`）'),
    'c408': dict(kind='フリー素材',
               plan='X408｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：空を飛ぶヘリコプターの遠景｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`At 1528:36, the traffic collision avoidance system (TCAS) on the airplane transmitted, “traffic traffic.”`）・報p20（`the alert was caused when the airplane passed close above a helicopter operating in the area`）'),
    'c409': dict(kind='図解',
               plan='SAT:テターボロ空港｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：テターボロ空港〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`At 1528:46, the controller stated that runway 4 at LGA was available`）・報p20（`I’m not sure we can make any runway. Uh what’s over to our right anything in New Jersey maybe Teterboro?`）'),
    'c410': dict(kind='図解',
               plan='🔧 地：GR1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：3つの案の札＝ラガーディア・テターボロ・ハドソン川｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈冬の川を上から〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`The controller replied, “ok yeah, off your right side is Teterboro Airport [TEB].”`…`the departure controller asked the captain if he wanted to try going to TEB, and the captain replied, “yes.”`）'),
    'c411': dict(kind='フリー素材',
               plan='X411｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：管制室のレーダーの画面〈場所は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#40p10（`He left the speaker line open so those controllers could hear the communication with the pilot because there was no time to relay information to them`）'),
    'c412': dict(kind='フリー素材',
               plan='X412｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：空港の管制塔の遠景〈ラガーディアとは名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p61（`LGA ATCT personnel activated the Emergency Alert Notification System using the red crash phone at 1528:53`）'),
    'c413': dict(kind='文字の頁',
               plan='R195｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録B｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p195（`PA-1 this is the Captain brace for impact.`）'),
    'c414': dict(kind='フリー素材',
               plan='X414｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：旅客機の客室の座席の列〈人の顔なし〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p195（`15:29:11 PA-1 this is the Captain brace for impact.`）・計（付録B の PA-1 の行は 15:02:51・15:17:30・15:29:11 の3つ＝鳥とぶつかったあとは1つ）・ド#7p5（`The captain made one PA announcement when it was obvious they were ditching`）'),
    'c415': dict(kind='図解',
               plan='🔧 SAT:テターボロ空港｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：テターボロ空港の滑走路1〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜注：c409 と同じ衛星写真に別の描き足し｜新しい画（映像方針）：🔧 図の模式（地＝衛星を暗く）→ 衛星写真＋描き足し（右へ曲がる矢印と届かない印）＝地図は衛星写真で（25本目の決め）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`At 1529:21, the CVR recorded the LGA departure controller instructing the captain to turn right 280° and stating that the airplane could land on runway 1 at TEB`…`In response to the controller, the captain stated, “we can’t do it.”`）・ド#40p10（`He coordinated with TEB thinking runway 1 was the best option due to the wind`）'),
    'c416': dict(kind='文字の頁',
               plan="R196｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録B｜注：＋音 A1（FAA の管制の録音）の数秒＝機長の「we're gonna be in the Hudson」（秒は ⑤b で聞いて決める）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）",
               src="報p196（`RDO-1 we're gonna be in the Hudson.`）・報p105（`At 1529:25, the captain told ATC that they would also be unable to land at TEB. Three seconds later, he stated to ATC that the airplane was going to be in the Hudson`）"),
    'c417': dict(kind='図解',
               plan='🔧 地：GA1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：声の札＝管制「すまない、もう一度」｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈管制室のレーダーの画面〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src="報p196（`DEP I'm sorry say again Cactus?`）"),
    'c418': dict(kind='フリー素材',
               plan='X418｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：管制室の無線の機器〈場所は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#40p10（`He believed the response was “can’t do it, going in the river”. That was the last transmission he heard from the flight crew`）'),
    'c419': dict(kind='図解',
               plan='🔧 地：C13（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：レーダーの電波が建物にさえぎられる絵｜注：—｜新しい画（映像方針）：🔧 地 衛星 → [13]（マンハッタンの建物＝レーダーをさえぎる建物）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`At 1529:53, the LGA departure controller stated that he had lost radar contact with the airplane`）・報p21（`If the airplane descends low enough to have the line-of-sight obstructed by buildings or other obstructions, radar contact will be lost`）'),
    'c420': dict(kind='フリー素材',
               plan='X420｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夕方の空港の滑走路〈場所は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`but he continued`）・報p21（`trying to communicate with the captain, stating, “you also got Newark airport off your two o’clock in about seven miles.”`）'),
    'c421': dict(kind='図解',
               plan='SAT:ハドソン川｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：ハドソン川〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p105（`both pilots indicated that they thought the Hudson River was the best and safest landing option given the airplane’s airspeed, altitude, and position`）'),
    'c422': dict(kind='図解',
               plan='🔧 地：GA1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：年表｜副題：交信の並び＝15:27:33 戻る → 15:28:11 できない〈13〉→ 15:28:35 できない〈31〉→ 15｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈管制室のレーダーの画面〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（15:27:11 から 15:29:28 まで＝2分17秒）・報p105（`at 1528:11, the captain reported to ATC`）'),
    'c423': dict(kind='フリー素材',
               plan='X423｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：シミュレーターの操縦席〈機種と社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（橋の1行）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-11-10）：紙面（型は c1.py の同じ節）
_R403, _R413, _R416 = P("r191_c403"), P("r195_c413"), P("r196_c416")
SPEC.update({
    # c403＝付録B p191 の右の半分の頭＋15:28:05（DEP の問い）と 15:28:10.6（RDO-1）の行（間の空白は表のまま）。1065×717＝高さいっぱい
    "c403": dict(photo=_R403, panel=True, ptall=True, ground=dict(photo=_R403, blur=ss.PAGE_BLUR), color=1.0,
                 t="管制の問い", s="管制との無線の書き起こし〈付録B〉"),
    # c413＝付録B p195 の左の半分（操縦室の中）の頭＋15:29:11 の PA-1 の行。1050×384＝幅いっぱい
    "c413": dict(photo=_R413, panel=True, pw=1776, ground=dict(photo=_R413, blur=ss.PAGE_BLUR), color=1.0,
                 t="客室への放送", s="操縦室の中の書き起こし〈付録B〉"),
    # c416＝付録B p196 の右の半分の頭＋15:29:28（RDO-1）と 15:29:33（DEP）の行。1065×534＝幅いっぱい。
    #   ⚠️ 本物の音（A1 の 116.55〜118.10秒＝`qa_out/ep32_assets.py` の AUDIO_PICK・耳の確かめは試写）を混ぜる仕組みは ⑤b-7（audio_mix に無い）
    "c416": dict(photo=_R416, panel=True, pw=1776, ground=dict(photo=_R416, blur=ss.PAGE_BLUR), color=1.0,
                 t="機長の答え", s="管制との無線の書き起こし〈付録B〉"),
})

# 🆕 ⑤b-3b（2026-11-10）：衛星写真（額装・静止・型は c1.py の同じ節）。矢印＝向きの模式（長さに意味は無い）。
#   管制の向き（220度・280度）は磁方位＝FAA の偏差 12度西を引いて真北の上の地図に描いた（lines32.py）・尾はその時刻の機体の位置（レーダーの点のあいだ）
#   c401＝G05（章の頭＝card_mix=0）：15:27:42 までの道 → 段2 で管制の示した向き／c406＝G03：滑走路31 へ降りる向き → 段2 で滑走路4 へ降りる向き（FAA の真方位）
#   c409・c415＝G06 テターボロ（ズーム13）／c421＝G07 ハドソン川（ズーム13）
_SRC220 = "付録B p189（15:27:42 turn left heading of uh two two zero）＝磁方位から偏差 12度西を引いた向き"
_SRC280 = "付録B p195（15:29:21 turn right two eight zero）＝磁方位から偏差 12度西を引いた向き"
SPEC.update({
    "c401": dict(
        **ss.sat("G05", steps=[
            [dict(k="line", path=ss.SAT_LINES["path_g05_to2742"], c="INK_W")],
            [dict(k="arrow", fr=ss.SAT_LINES["arr220_g05"][0], to=ss.SAT_LINES["arr220_g05"][1], dir=True, src=_SRC220,
                  c="AMBER", t="管制の示した向き", u=0.6, lab=(-24, 0, "end"))]],
            note=ss.SAT_LINE_NOTE + "・矢印は向きの模式"),
        card_mix=0, t="管制の答え", s="飛んだ道〈現在の衛星写真〉"),
    "c406": dict(
        **ss.sat("G03", steps=[
            [dict(k="arrow", fr=ss.SAT_LINES["arr31_g03"][0], to="lga31", dir=True, src="FAA の滑走路31 の真方位（302度）",
                  c="AMBER", t="滑走路31", u=0.45, lab=(24, 30, "start"))],
            [dict(k="arrow", fr=ss.SAT_LINES["arr04_g03"][0], to="lga04", dir=True, src="FAA の滑走路4 の真方位（32度）",
                  c="AMBER", t="滑走路4", u=0.4, lab=(-24, 0, "end"))]],
            note="矢印は降りる向きの模式（FAA の滑走路の向き）"),
        t="示された滑走路", s="ラガーディア空港の滑走路〈現在の衛星写真〉"),
    "c409": dict(
        **ss.sat("G06", steps=[
            [dict(k="line", path=ss.SAT_LINES["path_g06_to2846"], c="INK_W")],
            [dict(k="pt", at="teb", c="INK_W", t="右手の空港", lab=(26, 10, "start"))]],
            note=ss.SAT_LINE_NOTE),
        t="もう1つの空港", s="テターボロ空港〈現在の衛星写真〉"),
    "c415": dict(
        **ss.sat("G06", steps=[
            [dict(k="arrow", fr=ss.SAT_LINES["arr01_g06"][0], to="teb01", dir=True, src="FAA の滑走路1 の真方位（3度）",
                  c="AMBER", t="降りる向き", u=0.5, lab=(-24, 0, "end"))],
            [dict(k="arrow", fr=ss.SAT_LINES["arr280_g06"][0], to=ss.SAT_LINES["arr280_g06"][1], dir=True, src=_SRC280,
                  c="AMBER", t="右へ曲がる向き", u=0.5, lab=(0, -22, "middle"))],
            [dict(k="line", path=ss.SAT_LINES["path_g06_from2921"], c="INK_W", t="実際の道", u=0.6, lab=(24, 0, "start"))]],
            note=ss.SAT_LINE_NOTE + "・矢印は向きの模式"),
        t="管制の次の案", s="テターボロ空港の滑走路1〈現在の衛星写真〉"),
    "c421": dict(
        **ss.sat("G07", steps=[
            [dict(k="line", path=ss.SAT_LINES["path_g07"], c="INK_W", t="飛んだ道", u=0.3, lab=(-24, 0, "end"))],   # 東は Google の地名が多い＝門番 slide G-14
            [dict(k="x", at="ditch", t="着水した所", lab=(-30, -16, "end"))]],
            note=ss.SAT_LINE_NOTE),
        t="2人の考え", s="マンハッタンの西〈現在の衛星写真〉"),   # 川の名は章の札（「ハドソン川に降りる」）にある＝門番 dup
})
