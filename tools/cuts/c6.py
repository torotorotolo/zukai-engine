# -*- coding: utf-8 -*-
"""第5章　3ページの手順書 c601–c630（30カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c6.py`）。
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
    'c601': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：画面と冊子＝ふだんは故障とやることが操縦室の画面に出る・両方のエンジンの故障は例外で紙の冊子を開く｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p68（`If the flight warning computer (FWC) detects an airplane system failure, the failure type and the flight crew actions to be taken are displayed on the ECAM displays in the cockpit`）・報p69（`The ECAM exception index indicated that a dual-engine failure was an ECAM exception and directed the PM to the Engine Dual Failure checklist procedures contained in the QRH`）'),
    'c602': dict(kind='フリー素材',
               plan='X602｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：冊子の裏表紙の目次〈機種と社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p69（`because he had just completed training, he immediately recognized that the event was an ECAM exception; therefore, he was able to promptly locate the procedure listed on the back cover of the QRH, turn to the appropriate page, and start executing the checklist`）'),
    'c603': dict(kind='図解',
               plan='地：GB1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：手順書の3つの部分＝1 エンジンをかけ直す・2 かかったときとかからないとき・3 不時着と着水・3ページの絵｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p69（`Part 1 required the flight crew to differentiate between a no fuel remaining and a fuel remaining condition and included steps to attempt an engine restart`）・報p70（`Part 2 contained guidance for the flight crew to follow if an engine restart was successful or if an engine restart was not possible`…`Part 3 contained guidance for the flight crew to follow if a forced landing or a ditching was anticipated`）'),
    'c604': dict(kind='フリー素材',
               plan='X604｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：雲の上を飛ぶ旅客機〈社名と機種は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p69（`Airbus designed the Engine Dual Failure checklist for the occurrence of a dual-engine failure above 20,000 feet`）'),
    'c605': dict(kind='図解',
               plan='地：GC1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：飛ぶ時間の多くは高い空・故障が起きる見込みも高い空の札｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p69（`Because Airbus airplanes spend much more time at higher altitudes and, therefore, a dual-engine failure had the highest probability of occurring at a high rather than a low altitude`）・報p69（`Airbus indicated that it had not considered developing a dual-engine failure checklist for use at a low altitude`）'),
    'c606': dict(kind='フリー素材',
               plan='X606｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：並んだ旅客機の尾翼〈社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p104（`Discussions with A320 operators and a manufacturer also indicated that low-altitude, dual-engine failure checklists are not readily available in the industry`）'),
    'c607': dict(kind='図解',
               plan='地：GS1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：比べ｜副題：高さの比べ＝手順書の前提 約6,100メートルより上・鳥とぶつかった高さ 約860メートル｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p104（`The Engine Dual Failure checklist was designed assuming that a dual-engine failure occurred at a high altitude (above 20,000 feet)`）・計（2,818÷20,000＝約7分の1）'),
    'c608': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：2005年の改訂＝燃料が残る場合と残らない場合の2本立て・別の手順書にあった着水の手順をこの手順書へ入れる矢印・ページが｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p104（`In 2005, Airbus amended the Engine Dual Failure checklist by including two parallel steps, one for a fuel remaining scenario`…`by incorporating the ditching procedures, which had previously been located in a separate checklist`…`it resulted in a lengthy checklist`）'),
    'c609': dict(kind='フリー素材',
               plan='X609｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：分厚い冊子の束〈字は読ませない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p104（`the Engine Dual Failure checklist did not fully apply to a low-altitude, dual-engine failure and was unduly long for such an event given the limited time available`）'),
    'c610': dict(kind='図解',
               plan='地：GB2（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：燃料が残っている場合の手順の札＝点火を入れる・推力のレバーを確かめる・かけ直しに向く速さを保つ・降りる場所を決める｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p70（`In response to Part 1, the pilots followed the steps for a fuel remaining condition`）・報p70（`a. Start engine ignition b. Confirm thrust levers at idle c. Maintain optimum relight airspeed of 300 kts d. Determine a landing strategy`）'),
    'c611': dict(kind='写真',
               plan='🔧 C62｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：保管中のこの機体の操縦室｜動き：静止｜見た目の型：11-10 640px＝泥の跡の操縦席・計器｜権利：CC BY-SA 3.0｜時期：2011-02-25（EXIF＝博物館へ移す前の保管中）｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 3.0）・無加工｜注：BY-SA＝額装・無加工｜新しい画（映像方針）：🔧 副題の「2010年」は頁で確かめられない＝外した｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`At 1528:14, the first officer stated, “emergency electrical power...emergency generator not online.” At 1528:19, the captain stated, “it’s online.”`）・報p20（`At 1528:45, while the captain was communicating with ATC, the first officer stated, “FAC [flight augmentation computer] one off, then on.”`）'),
    'c612': dict(kind='写真',
               plan='R204｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録C｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`Fifteen seconds later, the first officer stated, “no relight after thirty seconds, engine master one and two confirm.”`）・報p20（`the steps included turning the engine master switches 1 and 2 to OFF and then waiting 30 more seconds before turning the switches back to ON`）'),
    'c613': dict(kind='写真',
               plan='🔧 D83-8｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：はしけの上の右のエンジン〈NTSB の調査の写真〉｜動き：静止｜見た目の型：11-10 640px＝雪のはしけの上の右のエンジン・壊れた覆い｜権利：同上｜時期：2009-01（凡例＝はしけの上）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（エンジンの報告 図8）｜注：下の「Photo No」の帯は切る｜新しい画（映像方針）：🔧 #83 の写真を見て決めた（図8＝右のエンジン＝語りの「2番」）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`At 1529:16, the first officer stated, “engine master two, back on,”`）・報p20（`At 1529:36, the first officer stated, “I put it [the engine master switch] back on,”`）・報p20（`At 1529:44, the first officer stated, “no relight,”`）'),
    'c614': dict(kind='図解',
               plan='地：GB2（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：手順書の3ページの絵に、進めた所を塗る＝1つ目の部分〈1ページ目と2ページ目の上〉の大半・2つ目と3つ目は白いまま｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p104（`Although the flight crewmembers were able to complete most of part 1 of the checklist, they were not able to start parts 2 and 3 of the checklist because of the airplane’s low altitude and the limited time available`）'),
    'c615': dict(kind='図解',
               plan='🔧 地：GB2（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：割合｜副題：手順書の全体のうち約3分の1を塗った3ページの絵｜注：—｜新しい画（映像方針）：🔧 模式（3ページの絵をもう一度）→ 割合の帯（全体の約3分の1）＝c614 と同じ絵を2度描かない｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p105（`the flight crew was only able to complete about one-third of the Engine Dual Failure checklist`）'),
    'c616': dict(kind='写真',
               plan='R205｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録C｜注：枠＝「If Ditching is anticipated」から下・「At 2000’ AGL c. Ditching pb ... ON」に印（頁の画像の座標 約 y 1870〜2600）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p104（`the flight crew never reached the ditching portion of the checklist, which most directly applied to the accident situation`）'),
    'c617': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：3ページ目の段取りの札＝約910メートルまでに翼を降りる形に・約610メートルで着水のボタン・約150メートルで衝撃に備｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='画（`Prior to 3000’ AGL`…`FLAPS`…`Configure for Landing`…`At 2000’ AGL`…`Ditching pb`）・報p73（`the airplane should be configured for a ditching before 3,000 feet (flaps 3 selected and landing gear up)`）'),
    'c618': dict(kind='写真',
               plan='R205｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜見た目の型：11-10 原寸の切り出し（p205 の 500,2140〜2060,2470）｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録C｜注：枠＝注の「Touchdown with approximately 11 degrees of pitch and minimum vertical speed.」（約 y 2200〜2280）と「At 500’AGL: d. Brace Signal ... Command」（約 y 2285〜2380）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='画（`At 500’AGL`…`Brace Signal`…`Command`…`Touchdown with approximately 11 degrees of pitch and minimum vertical speed`）'),
    'c619': dict(kind='図解',
               plan='地：C49（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：着水のボタンの働き＝水面より下の弁をすべて閉じる・長く浮くのを助ける｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p77（`Pushing the ditching pushbutton closes all of the valves below the water line (such as the outflow, avionics, ram air, and pack inlet valves) to help the airplane float longer`）'),
    'c620': dict(kind='フリー素材',
               plan='X620｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：操縦室の天井のボタンの列〈機種は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#7p5（`The Airbus had a ditching button, but he did not push it`）・ド#7p10（`they did not have time to get to the ditching push button`）'),
    'c621': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：訓練の札＝地上の座学で習う・シミュレーターの着水の訓練は無し・教わった着水は時間がある前提｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#7p6（`The only training for ditching was given in ground school`…`There was no training in the simulator`…`All guidance he received for ditching implied that they had time`）'),
    'c622': dict(kind='写真',
               plan='🔧 C32｜一覧の種類：写真｜見せ方：全面｜副題：警察のダイバーが渡すエンジンの覆い〈2009年1月・陸軍工兵隊〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝青い覆いを運ぶ警察のダイバーと工兵隊｜権利：PD（PD-USACE）｜時期：2009-01（頁の説明）｜人：警察のダイバーと工兵隊（顔が見える・公的な任務）｜出典の行：写真：U.S. Army Corps of Engineers（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 副題を写っているものに（頁の説明）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='画（`When below FL250`…`APU`…`START`）・ド#6p17（`When below FL250: k. APU`）・報p105（`immediately after the bird strike, the captain did accomplish one critical item that the flight crew did not reach in the checklist: starting the APU`）'),
    'c623': dict(kind='図解',
               plan='地：C32（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：手順書の2ページ目の絵＝k の行に印・そこまでの項目の数を見せる｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p105（`This critical step would not have been completed if the flight crew had simply followed the order of the items in the checklist`）'),
    'c624': dict(kind='図解',
               plan='地：C32（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：流れ｜副題：APU が電気をつくる → ふだんの制御の形〈ノーマル・ロー〉が保たれる → 失速を防ぐ守りが働く｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p105（`ensuring that a primary source of electrical power was available to the airplane and that the airplane remained in normal law and maintained the flight envelope protections, one of which protects against a stall`）'),
    'c625': dict(kind='フリー素材',
               plan='X625｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：操縦席から見た冬の川〈機種は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#7p32（`he felt that there needed to be a low level altitude, imminent landing checklist that could be done quicker with a couple of memory items`）・ド#7p32（`did a few memory items that helped them because they did not get to them on the checklist`）'),
    'c626': dict(kind='図解',
               plan='地：C32（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：低い所での故障の手順書があれば、の札｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p105（`if a checklist that addressed a dual-engine failure occurring at a low altitude had been available to the flight crewmembers, they would have been more likely to have completed that checklist`）'),
    'c627': dict(kind='写真',
               plan='R141｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）勧告｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p141（`Require manufacturers of turbine-powered aircraft to develop a checklist and procedure for a dual-engine failure occurring at a low altitude. (A-10-66)`）・報p141（`operators of turbine-powered aircraft to implement the checklist and procedure. (A-10-67)`）'),
    'c628': dict(kind='図解',
               plan='地：C32（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：勧告の札＝手順書の作り方の指針〈APU の始動のような大事な項目の順番・長さ・かかる時間〉・低い所での故障を訓練に入れる｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p142（`the order of critical items in the checklist (for example, starting the auxiliary power unit)`…`the length of the checklist`…`the time needed to complete the checklist`）・報p142（`include a dual-engine failure scenario occurring at a low altitude in initial and recurrent ground and simulator training`）'),
    'c629': dict(kind='写真',
               plan='🔧 C44｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：雪の公園の柵ごしに見た、はしけの上の機体〈2009年1月18日〉｜動き：静止｜見た目の型：11-10 640px＝雪の公園の柵・奥のはしけの機体｜権利：CC BY-SA 3.0｜時期：2009-01-18（頁の説明）｜人：はしけの人（遠景・小さい）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 3.0）・無加工｜注：BY-SA＝額装・無加工｜新しい画（映像方針）：🔧 副題に撮影の日（頁の説明 1月18日）・[45] と分ける｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（2つ目の問いの答え）・報p104（`designed assuming that a dual-engine failure occurred at a high altitude`）・報p104（`was unduly long for such an event given the limited time available`）'),
    'c630': dict(kind='図解',
               plan='地：C32（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：勧告の4本の札に「第10章」の印｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（橋の1行）'),
}

SPEC = {}
