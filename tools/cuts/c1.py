# -*- coding: utf-8 -*-
"""冒頭 c101–c113（13カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c1.py`）。
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
    'c101': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：沿岸警備隊の監視カメラ〈2009年1月15日・ハドソン川〉｜動き：映像 7.00〜20.50秒｜見た目の型：11-10 原寸 7・10・14・18秒＝川の向こう岸の高いビル・9秒から白いしぶきが左から右へ｜印：冒頭｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：しぶきに丸の囲み（9秒〜）・拡大しない（⑤b の試し焼きで見えなければ ×2 の固定の切り出し）・高さいっぱいの額＋同じ映像のぼかしの地｜新しい画（映像方針）：🔧 区間 0〜20秒 → 7.0秒から（しぶきは 9秒から＝語りの「白いしぶきは」より前に入る）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`was subsequently ditched on the Hudson River`）'),
    'c102': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：川に浮かぶ機体と翼の上の人〈沿岸警備隊の監視カメラ〉｜動き：映像 82.00〜95.50秒｜見た目の型：11-10 原寸 50・66・82・95秒＝×32 の寄り・82秒から翼の上に人の列｜印：冒頭｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：人は遠景で顔は分からない｜新しい画（映像方針）：🔧 区間 50秒〜1分30秒 → 82.0秒から（翼の上の人がいちばん見える・カメラが落ち着いた 81〜96秒）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`US Airways flight 1549, an Airbus Industrie A320-214`…`The 150 passengers, including a lap-held child, and 5 crewmembers evacuated the airplane via the forward and overwing exits`）'),
    'c103': dict(kind='写真',
               plan='🔧 C26｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：翼の上に並んだ人たち〈2009年1月15日〉｜動き：静止｜見た目の型：11-10 640px＝浮かぶ機体と両方の翼と前に並ぶ人（遠景）｜印：冒頭｜権利：CC BY 2.0｜時期：2009-01-15（頁の説明）｜人：翼の上の乗客（遠景・顔は分からない）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：地は同じ写真のぼかし｜新しい画（映像方針）：🔧 全面 → 高さいっぱいの額（1289×1243＝ほぼ正方形）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`resulting in very few serious injuries and no fatalities`）・報p17（`One flight attendant and four passengers were seriously injured`）'),
    'c104': dict(kind='写真',
               plan='🔧 C31｜一覧の種類：写真｜見せ方：全面｜副題：着水の直後の機体〈2009年1月15日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝白い航跡を引いてすべる機体｜印：冒頭｜権利：CC BY 2.0｜時期：2009-01-15（頁の説明＝着水の直後）｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 副題を写っているものに（頁の説明「shortly after landing」）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p97（`until about 1 minute 37 seconds into the flight`）・報p17（`experienced an almost complete loss of thrust in both engines after encountering a flock of birds`）'),
    'c105': dict(kind='写真',
               plan='C15｜一覧の種類：写真｜見せ方：全面｜副題：機体に寄せたフェリー〈2009年1月15日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝機体の前にフェリー（高い所から）｜印：冒頭｜権利：CC BY 2.0｜時期：2009-01-15（頁の説明）｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：引きは c105 の終わり 43.9秒（46秒まで）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`In eight of the 15 runs (53 percent), the pilot successfully landed after making an immediate turn to an airport`…`One run was made to return to an airport (runway 13 at LGA) after a 35-second delay`…`and the landing was not successful`）・ド#35p6（`The 8 successful runs were made following an immediate turn to an airport after the bird strike`）・ド#35p18（`Hard landing just short of threshold`）'),
    'c106': dict(kind='写真',
               plan='🔧 C18｜一覧の種類：写真｜見せ方：全面｜副題：集まった船とヘリコプター〈2009年1月15日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝フェリーの群れの中の機体・左上にヘリコプター｜印：冒頭｜権利：CC BY 2.0｜時期：2009-01-15（頁の説明）｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 [17]（切って色を直した版・1840px）→ 原本の [18]（2144px）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p106（`the captain’s decision to ditch on the Hudson River rather than attempting to land at an airport provided the highest probability that the accident would be survivable`）・計（15:27:11 から 15:30:43 まで＝3分32秒）'),
    'c107': dict(kind='写真',
               plan='C21｜一覧の種類：写真｜見せ方：全面｜副題：機体のまわりの消防艇と小舟〈2009年1月15日・陸軍工兵隊〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝消防艇と小舟・沈みかけの翼と尾翼・AIRWAYS の字｜印：冒頭｜権利：PD（PD-USACE）｜時期：2009-01-15（頁の説明）｜人：消防・救助の人（中景・公的な任務）｜出典の行：写真：U.S. Army Corps of Engineers（public domain）／Wikimedia Commons｜注：PD（陸軍工兵隊）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`this accident has been portrayed as a “successful” ditching`…`the success of this ditching mostly resulted from a series of fortuitous circumstances`）・計（報告書の文字の層で「miracle」は0件）'),
    'c108': dict(kind='写真',
               plan='C1｜一覧の種類：写真｜見せ方：全面｜副題：川に集まった船〈2009年1月15日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝川一面の船・手前に艦のマストと桟橋｜権利：CC BY 2.0｜時期：2009-01-15（頁の説明）｜人：船の上の人（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p17（`The National Transportation Safety Board determines that the probable cause of this accident`）・計（この動画の問い）'),
    'c109': dict(kind='図解',
               plan='SAT:ニューヨーク｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：現在の衛星写真｜動き：静止｜権利：Google（Geo Guidelines）｜時期：現在｜人：なし｜出典の行：「Google」と提供元の表記を絵のすぐ近くに｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#6p13（`The accident airplane collided with birds about 40° 50’ 53.16” N, 73° 52’ 33.92” W`…`The point of touchdown in the Hudson River was about 40° 46’ 16.67” N, 74° 00’ 20.51” W`）'),
    'c110': dict(kind='写真',
               plan='C49｜一覧の種類：写真｜見せ方：全面｜副題：この機体の操縦室の天井〈博物館の展示〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝ENG 1・APU・ENG 2 の赤いボタン｜権利：CC0｜時期：2011-02-25（頁の説明）｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC0）｜注：2011年2月の撮影（博物館）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p104（`the flight crew did not complete the Engine Dual Failure checklist, which had 3 parts and was 3 pages long`）・報p105（`the flight crew was only able to complete about one-third of the Engine Dual Failure checklist`）'),
    'c111': dict(kind='写真',
               plan='🔧 C36｜一覧の種類：写真｜見せ方：全面｜副題：岸壁のそばの機体と沿岸警備隊の小舟〈2009年1月16日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝晴れた昼・沿岸警備隊の小舟 25640・奥に沈みかけの機体｜権利：PD（PD-USCG）｜時期：2009-01-16 13:57（EXIF）｜人：乗り組みの人（中景・公的な任務）｜出典の行：写真：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 副題に撮影の日（EXIF 1月16日 13:57）・台本の画の欄の「夜」は誤り｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`including that the ditching occurred in good visibility conditions on calm water`）'),
    'c112': dict(kind='写真',
               plan='🔧 R1｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD（米国の連邦の業務）｜時期：2010-05-04（採択）｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）表紙｜注：—｜新しい画（映像方針）：🔧 [8]（EXIF 1月17日 9:51＝台本の「夕方・1月15日」と合わない）→ 報告書の表紙（語り「報告書は200ページをこえる」）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（報告書の PDF は213頁）・報p186（`INTRA-COCKPIT COMMUNICATION`）・報p18（`public docket for this accident investigation is available online`）'),
    'c113': dict(kind='写真',
               plan='🔧 C13｜一覧の種類：写真｜見せ方：全面｜副題：氷の浮かぶハドソン川の警察の船と作業船〈2009年1月〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝氷の川・警察の船と引き船・奥にマンハッタン（機体は写っていない）｜権利：CC BY 2.0｜時期：2009-01（頁の説明）｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 副題「機体のまわりの船」→ 写っているもの｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`January 15, 2009, about 1527 eastern standard time (EST)`）・報p96（`the ditching occurred in good visibility conditions`）・報p41（`visibility 10 miles`）'),
}

SPEC = {}
