# -*- coding: utf-8 -*-
"""第4章　本当に、空港へは戻れなかったのか c501–c524（23カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c5.py`）。
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
    'c501': dict(kind='図解',
               plan='SAT:試しの行き先｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：試しの行き先〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p66（`From April 14 through 16, 2009, the NTSB Operations and Human Performance Group, including members from Airbus, US Airways, the U.S. Airline Pilots Association, and the BEA, conducted flight simulations at the Airbus Training Center, Toulouse, France`）'),
    'c502': dict(kind='フリー素材',
               plan='X502｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：旅客機のシミュレーターの外観〈箱の形｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：🔴 操縦席に3人（原寸で横顔が分かる・x 0.51〜）＝窓の外｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p66（`to determine whether the accident airplane could have glided to and landed at LGA or TEB after the bird strike, considering both an immediate return to LGA and a return after a 35-second delay`）'),
    'c503': dict(kind='図解',
               plan='地：GM1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：シミュレーターの条件の札＝風・気温・機体の重さ・鳥とぶつかる少し前から始める｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p66（`The simulators were programmed to duplicate as closely as possible the conditions of the accident flight, including winds, temperature, altimeter setting, and weight and balance`）・報p67（`from a preprogrammed point shortly before the bird strike and loss of engine thrust`）'),
    'c504': dict(kind='フリー素材',
               plan='X504｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：説明を受ける操縦士の後ろ姿〈顔なし｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：後ろ姿の2人（顔なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`The pilots were fully briefed on the maneuver before they attempted to perform it in the simulator`）'),
    'c505': dict(kind='図解',
               plan='地：GM1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：表｜副題：20回 → 5回を外す → 15回＝ラガーディアの滑走路22 6回・13 7回・テターボロの19 2回｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`20 runs were performed in the engineering simulator`…`Five of the 20 runs were discarded because of poor data or simulator malfunctions`…`in 6, the pilot attempted to land on runway 22 at LGA; in 7, the pilot attempted to land on runway 13 at LGA; and in 2, the pilot attempted to land on runway 19 at TEB`）'),
    'c506': dict(kind='図解',
               plan='地：GM1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：棒｜副題：15回のうち降りられた8回＝滑走路22 2/6・13 5/7・テターボロ 1/2 の3本の棒｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`In eight of the 15 runs (53 percent), the pilot successfully landed after making an immediate turn to an airport after the loss of engine thrust`…`two of the six runs to land on runway 22 at LGA, five of the seven runs to land on runway 13 at LGA, and one of the two runs to land on runway 19 at TEB`）'),
    'c507': dict(kind='図解',
               plan='地：GM1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：降りられた8回に「直後に曲がった」の札・残る7回は「うまく降りられなかった」の印｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`the pilot successfully landed after making an immediate turn to an airport after the loss of engine thrust`）・計（15回のうち8回が降りられた＝残る7回は successful でなかった回＝滑走路の手前の回だけとは限らない〈ド#35 の表〉）'),
    'c508': dict(kind='フリー素材',
               plan='X508｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：操縦席から見た冬の街の遠景〈機種と社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`The immediate turn made by the pilots during the simulations did not reflect or account for real-world considerations, such as the time delay required to recognize the bird strike and decide on a course of action`）'),
    'c509': dict(kind='図解',
               plan='🔧 SAT:試しの行き先｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：35秒を足した試しの行き先〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜注：c303 と同じ衛星写真（G04＝滑走路13 の端が見える寄り）に別の描き足し・35秒は見出しと副題に（⑤b-3b）｜新しい画（映像方針）：🔧 図の模式（地＝衛星を暗く）→ 衛星写真＋描き足し（滑走路13 へ届かない矢印と35秒の札）＝模式の連続を切る｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`One run was made to return to an airport (runway 13 at LGA) after a 35-second delay`…`and the landing was not successful`）・ド#35p18（`Hard landing just short of threshold`）・報p67（`The 35-second delay accounted for real-world considerations, such as the time delay required to recognize the extent of the engine thrust loss and decide on a course of action`）'),
    'c510': dict(kind='図解',
               plan='🔧 地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：1549便の実際＝15:27:11 ぶつかる → 15:27:33 管制へ第一報〈22秒〉→ 15:27:50 手順書を｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈操縦室〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（15:27:11 から 15:27:33 まで＝22秒・15:27:50 まで＝39秒）'),
    'c511': dict(kind='フリー素材',
               plan='X511｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：冬のニューヨークの街を上から〈地名は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p106（`The simulations demonstrated that, to accomplish a successful flight to either airport, the airplane would have to have been turned toward the airport immediately after the bird strike`）'),
    'c512': dict(kind='図解',
               plan='SAT:ハドソン川｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：着水した所〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p106（`The one simulator flight that took into account real-world considerations (a return to LGA runway 13 was attempted after a 35-second delay) was not successful`）・ド#35p18（`Hard landing just short of threshold`）・報p137（`The captain’s decision to ditch on the Hudson River rather than attempting to land at an airport provided the highest probability that the accident would be survivable`）'),
    'c513': dict(kind='図解',
               plan='🔧 地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：機長の聴取の言葉の札＝「現実的な選択ではなかった」・「取り消せない選択」｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈操縦室〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p105（`returning to LGA would have been problematic and that it would not have been a realistic choice`）・報p106（`it would have been an irrevocable choice, eliminating all other options`）'),
    'c514': dict(kind='写真',
               plan='🔧 C35｜一覧の種類：写真｜見せ方：全面｜副題：残骸を見る NTSB の調査官〈2009年1月・陸軍工兵隊〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝甲板の残骸のそばの調査官1人（NTSB の帽子）｜権利：PD（PD-USACE）｜時期：2009-01（頁の説明）｜人：NTSB の調査官（公的な任務・名前は書かない）｜出典の行：写真：U.S. Army Corps of Engineers（public domain）／Wikimedia Commons｜注：名前は書かない（頁の説明に名がある）｜新しい画（映像方針）：🔧 副題「機体を調べる人たち」→ 写っているもの（1人）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p106（`and that TEB “was too far away.”`）'),
    'c515': dict(kind='フリー素材',
               plan='X515｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：会議の場の机とマイク〈人の顔なし〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#109p1（`Tuesday, June 9, 2009`）・ド#111p1（`Thursday, June 11, 2009`）・ド#109p18（`These flight simulations revealed that a successful return to LaGuardia or a diversion to Teterboro Airport was not assured`）'),
    'c516': dict(kind='写真',
               plan='🔧 C8｜一覧の種類：写真｜見せ方：全面｜副題：岸壁のそばの機体〈2009年1月17日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝奥の岸壁の機体と消防艇・警察の船｜権利：CC BY 2.0｜時期：2009-01-17 09:51（EXIF）｜人：船の上の人（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 [37]（[38] の切り抜き＝同じ写真）→ [8]（EXIF 1月17日 9:51）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#109p9（`there is certainly no intention by the Safety Board to diminish the crew’s and the first responder’s extraordinary success in saving the lives of all passengers and crew that day`）・ド#109p10（`fact-finding examination`）'),
    'c517': dict(kind='フリー素材',
               plan='X517｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：映画館の客席〈人なし｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='業（映画.com の作品の頁〈2026-11-09 の検索の表示〉＝原題 Sully・日本の公開 2016年9月24日）・通（`portrays investigators as more like prosecutors looking for any excuse to blame Sullenberger for the mishap`）'),
    'c518': dict(kind='図解',
               plan='地：GT1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：AP 通信の記事の要点の札＝調査を率いた元の責任者の言葉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='通（`“We weren’t out to embarrass anybody at all.”`）'),
    'c520': dict(kind='文字の頁',
               plan='R3｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010-05-04｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p3（`Adopted May 4, 2010`）・ド#109p10（`nor will any attempt be made at this time to determine the probable cause of the accident`）・計（公聴会 2009年6月＝事故から約5か月・採択 2010年5月4日）'),
    'c521': dict(kind='図解',
               plan='SAT:ニューヨーク｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：現在の衛星写真｜動き：静止｜権利：Google（Geo Guidelines）｜時期：現在｜人：なし｜出典の行：「Google」と提供元の表記を絵のすぐ近くに｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（1つ目の問いの答え）'),
    'c522': dict(kind='図解',
               plan='🔧 地：C31（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：判断の35秒の札と、届かない矢印｜注：—｜新しい画（映像方針）：🔧 地 衛星 → [31]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（1つ目の問いの答え）・報p67（`the time delay required to recognize the extent of the engine thrust loss and decide on a course of action`）・ド#35p18（`Hard landing just short of threshold`）・報p106（`provided the highest probability that the accident would be survivable`）'),
    'c523': dict(kind='フリー素材',
               plan='X523｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：冬の川の水面〈場所は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`although the pilots did not have time to complete each step of the applicable checklist, they did have sufficient time to consult the QRH, begin checklist execution, transmit radio calls, determine a landing strategy`）'),
    'c524': dict(kind='文字の頁',
               plan='🔧 R203-205｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録C｜注：—｜新しい画（映像方針）：🔧 模式（手順書の3ページの絵）→ 付録C の3頁を並べた紙面（実物）＝模式の連続を切る｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（橋の1行）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-11-10）：紙面（型は c1.py の同じ節）
_R520, _R524 = P("r3_c520"), P("r203_205")
SPEC.update({
    # c520＝報告書の題の頁（右上の「Adopted May 4, 2010」から題の「January 15, 2009」まで・下の印は入れない）。1500×1284＝高さいっぱい
    "c520": dict(photo=_R520, panel=True, ptall=True, ground=dict(photo=_R520, blur=ss.PAGE_BLUR), color=1.0,
                 t="報告書の採択", s="報告書の題の頁〈2010年5月4日の採択〉"),
    # c524＝付録C の3頁（手順書の 27・28・29 ページ）の絵を横に並べた紙面（cc06 と同じ束）。1818×1078＝高さいっぱい
    "c524": dict(photo=_R524, panel=True, ptall=True, ground=dict(photo=_R524, blur=ss.PAGE_BLUR), color=1.0,
                 t="2つ目の問い", s="手順書の3ページ〈付録C〉"),
})

# 🆕 ⑤b-3b（2026-11-10）：衛星写真（額装・静止・型は c1.py の同じ節）。
#   c501＝G01（章の頭＝card_mix=0）：試しの行き先の2つの空港 → 段2 で鳥とぶつかった所（試しの始まり）
#   c509＝G04：段2 で滑走路13 と、その手前で止まる矢印（35秒を足した1回＝報告書 p106・ドケット #35 p18 の「Hard landing just short of threshold」＝模式）
#   c512＝G07：着水した所だけ／c521＝G01：段2 で「すぐに曲がった試し」の矢印（報告書 p106＝模式）
SPEC.update({
    "c501": dict(
        **ss.sat("G01", steps=[
            [dict(k="pt", at="lga", c="INK_W", t="ラガーディア空港", lab=(24, 10, "start")),
             dict(k="pt", at="teb", c="INK_W", t="テターボロ空港", lab=(-26, 10, "end"))],
            [dict(k="x", at="bird", t="鳥とぶつかった所", lab=(30, 10, "start"))]]),
        card_mix=0, t="戻っていたら", s="試しの行き先〈現在の衛星写真〉"),
    "c509": dict(
        **ss.sat("G04", steps=[
            [dict(k="x", at="bird", t="鳥とぶつかった所", lab=(30, 10, "start"))],
            [dict(k="txt", at="lga13", c="INK_W", t="滑走路13", lab=(34, -26, "start")),   # 点は置かない＝端の上に Google の「ラガーディア空港」の字（試し焼きの原寸）
             dict(k="arrow", fr=ss.SAT_LINES["arr13_g04"][0], to="lga13", dir=True, src="FAA の滑走路13 の真方位（122度）",
                  c="ALERT", gap=42, t="手前で届かず（模式）", u=0.35, lab=(-20, -20, "end"))]],
            note="矢印は試しを描いた模式（FAA の滑走路の向き）"),
        t="35秒の遅れ", s="35秒を足した試しの行き先〈現在の衛星写真〉"),
    "c512": dict(
        **ss.sat("G07", steps=[
            [dict(k="x", at="ditch")]]),
        t="川を選んだ判断", s="着水した所〈現在の衛星写真〉"),
    "c521": dict(
        **ss.sat("G01", steps=[
            [dict(k="x", at="bird", t="鳥とぶつかった所", lab=(30, 10, "start")),
             dict(k="pt", at="lga", c="INK_W", t="ラガーディア空港", lab=(24, 10, "start")),
             dict(k="pt", at="teb", c="INK_W", t="テターボロ空港", lab=(-26, 10, "end"))],
            [dict(k="arrow", fr="bird", to="lga", c="AMBER", t="すぐに曲がった試し（模式）", u=0.5, lab=(-26, 0, "end")),
             dict(k="arrow", fr="bird", to="teb", c="AMBER")]],
            note="矢印は試しを描いた模式"),
        t="記録の答え", s="ニューヨーク〈現在の衛星写真〉"),
})

# 🆕 ⑤b-4a（2026-11-10）：イメージの写真（Pexels・全面・見出しと副題なし・原色＝c2.py の同じ節の型）
_X502, _X504, _X508, _X511, _X515, _X517, _X523 = (P(f"stock/{c}") for c in ("x502", "x504", "x508", "x511", "x515", "x517", "x523"))
SPEC.update({
    # c502＝操縦席から見た滑走路への進入（冬枯れの地面）。🔧 1本目（模擬の操縦席の外側）は人を窓の外へ出すと窓の7割が壁＝試し焼きで替えた
    "c502": dict(photo=_X502, **ss.mvz(_X502, (0.5, 0.55, 1.0), (0.5, 0.6, 1.12)), side="none", color=1.0, t="", s=""),
    # c504＝操縦席に並ぶ2人の後ろ姿（古い型の操縦室・顔なし・肩章に字なし）
    #   窓の上の端は 0・31（天井の操作盤の OCR の行 y 55〜88 を切らない＝門番 edges）・終わりの右の端は 2835（行 2693〜2812 を切らない）
    "c504": dict(photo=_X504, **ss.mvz(_X504, (0.5, 0.42, 1.0), (0.53, 0.40, 1.1)), side="none", color=1.0, t="", s=""),
    # c508＝操縦席から雲の上を見る操縦士の影（後ろ姿・顔なし）＝語り「どうするかを決めるまでの時間」
    "c508": dict(photo=_X508, **ss.mvz(_X508, (0.5, 0.5, 1.0), (0.55, 0.48, 1.1)), side="none", color=1.0, t="", s=""),
    # c511＝上から見たマンハッタンの通りと屋根（白黒＝原本の色・看板の字なし・2009年より後の高い建物は写らない）
    "c511": dict(photo=_X511, **ss.mvz(_X511, (0.5, 0.5, 1.0), (0.5, 0.5, 1.1)), side="none", color=1.0, t="", s=""),
    # c515＝会議の場の机とマイクと画面（人なし・名札は白）
    "c515": dict(photo=_X515, **ss.mvz(_X515, (0.5, 0.5, 1.0), (0.55, 0.55, 1.1)), side="none", color=1.0, t="", s=""),
    # c517＝映写の幕と赤い客席（人なし）
    "c517": dict(photo=_X517, **ss.mvz(_X517, (0.5, 0.5, 1.0), (0.5, 0.5, 1.1)), side="none", color=1.0, t="", s=""),
    # c523＝冬の川の水面と葉の落ちた木
    "c523": dict(photo=_X523, **ss.mvz(_X523, (0.5, 0.5, 1.0), (0.45, 0.5, 1.1)), side="none", color=1.0, t="", s=""),
})

# 🆕 ⑤b-5（2026-11-11）：模式（`tools/mech32.py`）。地は写真を暗くするだけ（`ss.gr`・値は `ss.GROUND`）
import mech32 as _m32  # noqa: E402
SPEC.update({
    "c503": _m32.fu_spec("c503", ss.gr("stock/gm1")),
    "c507": _m32.zu_spec("c507", ss.gr("stock/gm1")),
    "c510": _m32.zu_spec("c510", ss.gr("stock/gk1")),
    "c513": _m32.fu_spec("c513", ss.gr("stock/gk1")),
    "c518": _m32.fu_spec("c518", ss.gr("stock/gt1")),
    "c522": _m32.zu_spec("c522", ss.gr("c31")),
})
# 🆕 ⑤b-6（2026-11-11）：型の図（表・棒）＝mech32 の「⑤b-6」の節
SPEC.update({
    "c505": _m32.zu_spec("c505", ss.gr("stock/gm1")),
    "c506": _m32.zu_spec("c506", ss.gr("stock/gm1")),
})

# 🆕 ⑤b-7（2026-11-11）：写真の束の残り（型は c1.py の同じ節）
_C35, _C8 = P("c35"), P("c8")
SPEC.update({
    # c514＝[35] 甲板の残骸のそばの NTSB の調査官（公的な任務・名前は書かない）＝調査官と残骸へ寄る
    "c514": dict(photo=_C35, **ss.mv(_C35, "in", fx=0.55, fy=0.55), side="none", color=1.0,
                 t="機長の話", s="残骸を見る NTSB の調査官〈2009年1月・陸軍工兵隊〉"),
    # c516＝[8] 奥の岸壁の機体と消防艇（EXIF 1月17日 9:51）＝機体と消防艇のあいだへ寄る
    #   🔧 寄りは 1.10（1.15 だと寄り終わりの窓の上の辺〈行 418〉が左上のビルの OCR の行 405〜442 を 65% で切る＝門番 edges）
    "c516": dict(photo=_C8, **ss.mv(_C8, "in", fx=0.3, fy=0.68, z=1.10), side="none", color=1.0,
                 t="公聴会", s="岸壁のそばの機体〈2009年1月17日〉"),
})
