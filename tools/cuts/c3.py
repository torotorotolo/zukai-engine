# -*- coding: utf-8 -*-
"""第2章　高さ約860メートルの群れ c301–c323（23カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c3.py`）。
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
    'c301': dict(kind='図解',
               plan='🔧 地：GS1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：時計｜副題：「15:27:10」の札と針｜注：—｜新しい画（映像方針）：🔧 地 衛星（Google を暗く）→ イメージ〈冬の空〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`at 1527:10.4, the captain stated, “birds.”`）'),
    'c302': dict(kind='フリー素材',
               plan='X302｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：正面から飛んでくるガンの群れ｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#7p3（`saw the birds go down below the windscreen and thought they would miss the birds`）・報p19（`One second later, the CVR recorded the sound of thumps and thuds followed by a shuddering sound`）・ド#7p3（`Then he heard birds hit`）'),
    'c303': dict(kind='図解',
               plan='SAT:鳥とぶつかった所｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：鳥とぶつかった所〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`the bird encounter occurred when the airplane was at an altitude of 2,818 feet above ground level (agl)`…`a distance of about 4.5 miles north-northwest of the approach end of runway 22 at LGA`）・報p115（`about 4.3 miles from LGA`）'),
    'c304': dict(kind='フリー素材',
               plan='X304｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：空を飛ぶカナダガンの群れ｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p66（`contained viable DNA and matched 99 percent or more to the Barcode of Life Database`…`for Canada goose (Branta canadensis)`）'),
    'c305': dict(kind='写真',
               plan='🔧 C61｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：エンジンから集めた羽〈NTSB〉｜動き：静止｜見た目の型：11-10 640px＝袋の羽・エンジン1 の札・左下に手書きの人の名前｜権利：PD（PD-NTSB）｜時期：2009-01-29（袋の字）｜人：なし｜出典の行：写真：NTSB（public domain）／Wikimedia Commons・改変：切出｜注：🔴 左下の手書きの人の名前を切る（PD＝切出可）｜新しい画（映像方針）：🔧 全面 → 額装（縦長）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p66（`the feathers from the airplane engines were similar to samples of known migratory geese`）・報p52（`inspections of both engine cores revealed that foreign material consistent with bird feathers and tissue was inside the engine`）・報p52（`will fluoresce green when illuminated with ultraviolet light`）'),
    'c306': dict(kind='図解',
               plan='地：C61（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：比べ｜副題：ガンの重さ＝オス 約3.8〜4.2キロ・メス 約3.3〜3.5キロ｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p97（`The average weight of a male Canada goose is from 8.4 to 9.2 pounds, and the average weight of a female goose is from 7.3 to 7.8 pounds`）・報p97（`each engine ingested at least two Canada geese weighing about 8 pounds each`）'),
    'c307': dict(kind='図解',
               plan='地：C61（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：並べ｜副題：大きな鳥の試験＝約1.8キロ〈4ポンド〉1羽・当たったガン＝約3.6キロ〈8ポンド〉が2羽ずつ｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p34（`The large-bird ingestion criterion for CFM56-5B4/P-sized engines was a single, 4-pound bird`）・報p97（`which significantly exceeded the certification standards`）'),
    'c308': dict(kind='図解',
               plan='地：GS1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：線｜副題：エンジンの回る速さ＝左 82%→35%・右 82%→15% の2本の線｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p64（`the left engine decelerated from 82 to 35 percent N1, the right engine decelerated from 82 to 15 percent N1`）・報p17（`an almost complete loss of thrust in both engines`）'),
    'c309': dict(kind='写真',
               plan='🔧 D76-4｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：鳥が当たった跡〈NTSB の調査の写真〉｜動き：静止｜見た目の型：11-10 640px＝ピンクの丸の中の凹み｜権利：PD の見込み（NTSB の調査グループの写真・撮影者の記載なし）｜時期：2009-01（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（構造の写真 写真4）｜注：—｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#76 写真4）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`At 1527:14, the first officer stated, “uh oh,” followed by the captain stating, “we got one rol- both of ‘em rolling back.”`）'),
    'c310': dict(kind='フリー素材',
               plan='X310｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：旅客機の操縦室のスイッチ〈機種は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`At 1527:19, the captain stated, “[engine] ignition, start,” and, about 2 seconds later, “I’m starting the APU [auxiliary power unit].”`）・報p71（`The captain stated that he accomplished step a by memory`）・計（15:27:11 から 15:27:21 まで＝10秒）'),
    'c311': dict(kind='図解',
               plan='地：C49（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：APU＝機体の後ろの小さなエンジン・電気をつくる矢印｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`The APU provides an additional source of electrical power for the airplane`）'),
    'c312': dict(kind='写真',
               plan='🔧 D76-2｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：機首の覆いの割れ〈NTSB の調査の写真〉｜動き：静止｜見た目の型：11-10 640px＝割れた機首の覆い・開いた扉｜権利：同上｜時期：2009-01（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（構造の写真 写真2）｜注：—｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#76 写真2）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p105（`immediately after the bird strike, the captain did accomplish one critical item that the flight crew did not reach in the checklist: starting the APU`）・報p105（`This critical step would not have been completed if the flight crew had simply followed the order of the items in the checklist`）'),
    'c313': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：2人の役の札＝操縦と交信と降りる場所〈機長〉・手順書〈副操縦士〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`At 1527:23, the captain took over control of the airplane, stating, “my aircraft.”`）・報p104（`At 1527:23, about 12 seconds after the bird strike, the captain took control of the airplane`）'),
    'c314': dict(kind='フリー素材',
               plan='X314｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：操縦席に並ぶ2人の後ろ姿〈顔なし｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：後ろ姿の2人（顔なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p108（`The first officer progressed through the checklist while the captain was flying the airplane, communicating with ATC, and determining a suitable landing point`）'),
    'c315': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：冊子の札「QRH＝緊急のときの手順をまとめた冊子」・推力の矢印〈エンジンが機体を前へ押す〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`At 1527:28, the captain instructed the first officer to “get the QRH [quick reference handbook] loss of thrust on both engines.”`）'),
    'c316': dict(kind='フリー素材',
               plan='X316｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：冊子をめくる手〈社名と機種は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：手だけ｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p108（`when he called for the QRH, about 17 seconds after the bird strike, the first officer already had the checklist out`）・報p108（`he and the first officer had to work almost intuitively in a very close-knit fashion`）'),
    'c317': dict(kind='図解',
               plan='SAT:いちばん高い所｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：いちばん高くなった所〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p64（`until 1527:30, when the airplane reached its highest altitude of about 3,060 feet`…`The altitude then started to decrease`）・報p64（`the airplane’s altitude continued to increase while the airspeed decreased`）'),
    'c318': dict(kind='文字の頁',
               plan='R189｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録B｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`we’ve lost thrust in both engines, we’re turning back towards LaGuardia`）'),
    'c319': dict(kind='図解',
               plan='🔧 地：GA1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：無線が重なる絵＝2つの機の声が同じ周波数でぶつかる｜注：—｜新しい画（映像方針）：🔧 地 衛星（Google を暗く）→ イメージ〈管制室のレーダーの画面〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`portion of the captain’s statement was not transmitted to the air traffic controller because another pilot was transmitting on the same frequency at the same time`）・報p19（`The NTSB notes that the flight number was 1549 not 1539`）'),
    'c320': dict(kind='文字の頁',
               plan='R203｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録C｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`At 1527:50, the first officer began conducting Part 1 of the QRH ENG DUAL FAILURE checklist`）・計（15:27:11 から 15:27:50 まで＝39秒）'),
    'c321': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：速さの札＝エンジンをかけ直すのに向く速さ 時速約560キロ〈300ノット〉・ぶつかったあとの最高 時速約400キロ〈21｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`airspeed optimum relight. three hundred knots. we don’t have that,`）・報p19（`the maximum airspeed reached by the airplane after the bird ingestion was 214 knots (kts), which was below the optimum minimum airspeed of 300 kts for an engine windmill relight`）'),
    'c322': dict(kind='写真',
               plan='🔧 D101-2｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：翼の溝に残った羽〈NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009-01（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（野生動物の報告 写真2）｜注：② で見た｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#101 写真2）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p104（`the first officer spent about 30 to 40 seconds attempting to relight the engines`…`because he did not know the extent of the engine damage`）・報p99（`The flight crew was unaware that the extent and type of the engine damage precluded any pilot action from returning them to operational status`）'),
    'c323': dict(kind='図解',
               plan='地：GS1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：帯｜副題：約2分の帯＝15:27:33 管制へ第一報 → 15:29:28「ハドソン川に降りる」｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（15:27:33 から 15:29:28 まで＝1分55秒）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-11-10）：紙面（型は c1.py の同じ節）
_R318, _R320 = P("r189_c318"), P("r203_c320")
SPEC.update({
    # c318＝付録B p189 の右の半分（管制との無線）の頭＋15:27:32.9（RDO-1 の mayday）と 15:27:42（DEP）の行。1065×657＝高さいっぱい
    "c318": dict(photo=_R318, panel=True, ptall=True, ground=dict(photo=_R318, blur=ss.PAGE_BLUR), color=1.0,
                 t="機長から管制へ", s="管制との無線の書き起こし〈付録B〉"),
    # c320＝付録C p203 の見出し「ENG DUAL FAILURE」＋「If fuel remaining」から「Cont'd」まで（左上の縦線は分かれ道の括弧の線）
    "c320": dict(photo=_R320, panel=True, ptall=True, ground=dict(photo=_R320, blur=ss.PAGE_BLUR), color=1.0,
                 t="手順書の最初", s="両方のエンジンの故障の手順書〈付録C〉"),
})

# 🆕 ⑤b-3b（2026-11-10）：衛星写真（額装・静止・型は c1.py の同じ節）。
#   c303＝G04（ズーム13）：飛んだ道（最初のレーダーの点から鳥とぶつかった所まで）・×・段2 で「約7キロ」＝滑走路22 の進入端から（報告書 p19 の 4.5マイル）。
#     ⚠️ 向きの語は札に書かない（報告書の north-northwest と、座標から出す向き 356度が合わない＝ss.GEO の注）
#   c317＝G05（ズーム13）：鳥とぶつかった所 → いちばん高い所（報告書 p64 の 15:27:30・約3,060フィート＝約930メートル）→ 段2 で下がりながら左へ
SPEC.update({
    "c303": dict(
        **ss.sat("G04", steps=[
            [dict(k="line", path=ss.SAT_LINES["path_g04"], c="INK_W"),
             dict(k="pt", at="lga", c="INK_W", t="出発した空港", lab=(24, 10, "start")),
             dict(k="x", at="bird", t="鳥とぶつかった所", lab=(30, 10, "start"))],
            [dict(k="line", path=("lga22", "bird"), c="AMBER", dash=True, w=3, t="約7キロ", u=0.55, lab=(-22, 0, "end"))]],
            note=ss.SAT_LINE_NOTE),
        t="高さと場所", s="ラガーディア空港の北〈現在の衛星写真〉"),   # 「鳥とぶつかった空」は札の写し＝門番 dup
    "c317": dict(
        **ss.sat("G05", steps=[
            [dict(k="line", path=ss.SAT_LINES["path_g05_up"], c="INK_W"),
             dict(k="pt", at="bird", c="INK_W", dot=7),
             dict(k="pt", at="top", c="INK_W", t="約930メートル", lab=(26, 0, "start"))],
            [dict(k="line", path=ss.SAT_LINES["path_g05_down"], c="INK_W")]],
            note=ss.SAT_LINE_NOTE),
        t="上がって、下がる", s="いちばん高くなった所〈現在の衛星写真〉"),
})

# 🆕 ⑤b-4a（2026-11-10）：イメージの写真（Pexels・全面・見出しと副題なし・原色＝c2.py の同じ節の型）
_X302, _X304, _X310, _X314, _X316 = (P(f"stock/{c}") for c in ("x302", "x304", "x310", "x314", "x316"))
SPEC.update({
    # c302＝こちらへ飛んでくるカナダガン4羽＝右下の1羽を字幕の帯（下 約17%）より上に（fy 0.55）
    "c302": dict(photo=_X302, **ss.mvz(_X302, (0.5, 0.55, 1.0), (0.5, 0.55, 1.08)), side="none", color=1.0, t="", s=""),
    # c304＝青空を群れで飛ぶカナダガン
    "c304": dict(photo=_X304, **ss.mvz(_X304, (0.45, 0.5, 1.0), (0.42, 0.45, 1.12)), side="none", color=1.0, t="", s=""),
    # c310＝暗い操縦室のレバーと ENG 1／ENG 2 のスイッチ。🔴 レバーの間の紙の札（字が読める・y 0.43〜0.51）は窓の上の外（窓の上の端 y 0.53〜）。
    #   窓の左の端は操作盤の札の行のあいだ（x 653・666＝OCR の箱 615〜683 のすき間）・終わりの下の端は 1810（行 1817〜1836 を切らない＝門番 slide G-10）
    "c310": dict(photo=_X310, **ss.mvz(_X310, (0.49, 0.76, 1.9), (0.475, 0.737, 2.05)), side="none", color=1.0, t="", s=""),
    # c314＝操縦席に並ぶ2人の後ろ姿（顔は写らない・名札なし）
    "c314": dict(photo=_X314, **ss.mvz(_X314, (0.5, 0.5, 1.0), (0.5, 0.45, 1.1)), side="none", color=1.0, t="", s=""),
    # c316＝白い頁をめくる手（字なし）
    "c316": dict(photo=_X316, **ss.mvz(_X316, (0.5, 0.5, 1.0), (0.55, 0.5, 1.1)), side="none", color=1.0, t="", s=""),
})

# 🆕 ⑤b-5（2026-11-11）：模式（`tools/mech32.py`）。地は写真を暗くするだけ（`ss.gr`・値は `ss.GROUND`）
import mech32 as _m32  # noqa: E402
SPEC.update({
    "c311": _m32.fu_spec("c311", ss.gr("c49")),
    "c313": _m32.fu_spec("c313", ss.gr("stock/gk1")),
    "c315": _m32.zu_spec("c315", ss.gr("stock/gk1")),
    "c319": _m32.fu_spec("c319", ss.gr("stock/ga1")),
    "c321": _m32.zu_spec("c321", ss.gr("stock/gk1")),
})
# 🆕 ⑤b-6（2026-11-11）：型の図（時計・比べ・並べ・線・帯）＝mech32 の「⑤b-6」の節
SPEC.update({
    "c301": _m32.zu_spec("c301", ss.gr("stock/gs1")),
    "c306": _m32.zu_spec("c306", ss.gr("c61")),
    "c307": _m32.zu_spec("c307", ss.gr("c61")),
    "c308": _m32.zu_spec("c308", ss.gr("stock/gs1")),
    "c323": _m32.zu_spec("c323", ss.gr("stock/gs1")),
})

# 🆕 ⑤b-7（2026-11-11）：写真の束の残り（型は c1.py の同じ節）
_C61, _D76_4, _D76_2, _D101_2 = P("c61"), P("d76_4"), P("d76_2"), P("d101_2")
SPEC.update({
    # c305＝[61] 袋の羽（エンジン1 の札・「1-29-09」・左下の手書きの人の名前は束の段で切り落とした）
    "c305": dict(photo=_C61, panel=True, ptall=True, ground=dict(photo=_C61), color=1.0,
                 t="羽の分析", s="エンジンから集めた羽〈NTSB〉"),
    # c309＝#76 写真4 ピンクの丸の中の凹み
    "c309": dict(photo=_D76_4, panel=True, ptall=True, ground=dict(photo=_D76_4), color=1.0,
                 t="両方のエンジン", s="鳥が当たった跡〈NTSB の調査の写真〉"),
    # c312＝#76 写真2 割れた機首の覆い
    "c312": dict(photo=_D76_2, panel=True, ptall=True, ground=dict(photo=_D76_2), color=1.0,
                 t="APU の始動", s="機首の覆いの割れ〈NTSB の調査の写真〉"),
    # c322＝#101 写真2 翼の溝に残った羽
    "c322": dict(photo=_D101_2, panel=True, ptall=True, ground=dict(photo=_D101_2), color=1.0,
                 t="再始動の試み", s="翼の溝に残った羽〈NTSB の調査の写真〉"),
})
