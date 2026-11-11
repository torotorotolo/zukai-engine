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
               plan='🔧 C15｜一覧の種類：写真｜見せ方：全面｜副題：機体のそばのフェリー〈2009年1月15日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝機体の前にフェリー（高い所から）｜印：冒頭｜権利：CC BY 2.0｜時期：2009-01-15（頁の説明）｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：引きは c105 の終わり 43.5秒（46秒まで）｜新しい画（映像方針）：🔧 ⑤b-2：副題「機体に寄せたフェリー」→ 写っているもの（門番 check_credits＝「寄せ」は作り手の言葉）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`In eight of the 15 runs (53 percent), the pilot successfully landed after making an immediate turn to an airport`…`One run was made to return to an airport (runway 13 at LGA) after a 35-second delay`…`and the landing was not successful`）・ド#35p6（`The 8 successful runs were made following an immediate turn to an airport after the bird strike`）・ド#35p18（`Hard landing just short of threshold`）'),
    'c106': dict(kind='写真',
               plan='🔧 C18｜一覧の種類：写真｜見せ方：全面｜副題：集まったフェリー〈2009年1月15日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝フェリーの群れの中の機体・左上にヘリコプター｜印：冒頭｜権利：CC BY 2.0｜時期：2009-01-15（頁の説明）｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 [17]（切って色を直した版・1840px）→ 原本の [18]（2144px）／🔧 ⑤b-2：副題からヘリコプターを外した（試し焼きの原寸＝左上のヘリコプターは見出しの字の下に隠れる）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
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
    'c112': dict(kind='文字の頁',
               plan='🔧 R1｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD（米国の連邦の業務）｜時期：2010-05-04（採択）｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）表紙｜注：—｜新しい画（映像方針）：🔧 [8]（EXIF 1月17日 9:51＝台本の「夕方・1月15日」と合わない）→ 報告書の表紙（語り「報告書は200ページをこえる」）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（報告書の PDF は213頁）・報p186（`INTRA-COCKPIT COMMUNICATION`）・報p18（`public docket for this accident investigation is available online`）'),
    'c113': dict(kind='写真',
               plan='🔧 C13｜一覧の種類：写真｜見せ方：全面｜副題：氷の浮かぶハドソン川の警察の船と作業船〈2009年1月〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝氷の川・警察の船と引き船・奥にマンハッタン（機体は写っていない）｜権利：CC BY 2.0｜時期：2009-01（頁の説明）｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 副題「機体のまわりの船」→ 写っているもの｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`January 15, 2009, about 1527 eastern standard time (EST)`）・報p96（`the ditching occurred in good visibility conditions`）・報p41（`visibility 10 miles`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-2（2026-11-10）：冒頭の実写 c101〜c107（PLAN の予定どおり＝再現の絵・動く模式・効果音は使わない）
# ══════════════════════════════════════════════════════════
#   束＝`qa_out/ep32_assets.py build`（`ref/ep32/assets.json`）。VTS＝`ss.vid`（🔴 額装・高さいっぱい＝ptall を明記〈ひかえの静止画は 384×288＝幅1280未満＝
#   kind() が panel を返す＝panel を重ねて書くと「multiple values」で章ファイルが読めない〉・
#   静止＝FRAME_STILL_EP・地は同じ映像のぼかし・等速・止めなし・区間は一覧の動きの欄 → `qa_out/ep32_assets.py use`・PILLAR なし〈器そのものが 4:3＝黒い帯なし〉）。
#   見出し（t）は話題の札（12字未満＝語りの丸写しにしない・門番 echo）・副題（s）は一覧 list32.tsv の sub（写っているもの）＝額の左に収まる長さに。
#   🔴 c101 の「しぶきに丸の囲み」（一覧の注）は描かない：映像の上に丸を描く部品が無い（`ann` は字だけ・circle は地図と模式の段）。
#   🔧 試し焼き（Actions 42776414038）の原寸で、1倍ではしぶきが細い白い筋だけ＝一覧の注どおり「×2 の固定の切り出し」（footage.USE の zoom 2.0・xbias 0・bias 0.44
#   ＝`qa_out/ep32_assets.py` の VTS_GEOM・通り道は背景との差で測った）。焼き込みのカメラの時計（約20秒進む）は語りと副題に使わない（×2 の窓の外）
#   ✅ 人の写り＝[26]（翼の上の人＝遠景・顔は分からない）・[31]・[15]・[18]＝遠景・[21]＝消防の人（中景・公的な任務）＝640px のシートで見た（11-10）
_C26, _C31, _C15, _C18, _C21 = P("c26"), P("c31"), P("c15"), P("c18"), P("c21")
SPEC.update({
    # c101＝VTS CrashAndRescue 7.0秒〜（引き・9秒から白いしぶきが左から右へ）。等速・読む 9.17秒（〜16.17）
    "c101": ss.vid("c101", ptall=True, t="2009年1月15日", s="沿岸警備隊の監視カメラ〈ハドソン川〉"),
    # c102＝同じ映像 82.0秒〜（×32 の寄り・浮かぶ機体と翼の上の人の列＝遠景）。等速・読む 9.75秒（〜91.75）
    "c102": ss.vid("c102", ptall=True, t="乗客と乗員 155人", s="翼の上の人〈沿岸警備隊の監視カメラ〉"),
    # c103＝[26] 翼の上に並ぶ人（1289×1243＝ほぼ正方形・CC BY 2.0）＝高さいっぱいの額・静止・地は同じ写真のぼかし。最初の聞き役 c103-1（19.3秒）
    "c103": dict(photo=_C26, panel=True, ptall=True, ground=dict(photo=_C26), color=1.0,
                 t="全員の生還", s="翼の上に並んだ人たち〈2009年1月15日〉"),
    # c104＝[31] 白い航跡を引く機体（全面・ゆっくり寄る＝機体へ）
    "c104": dict(photo=_C31, **ss.mv(_C31, "in", fx=0.48, fy=0.49), side="none", color=1.0,
                 t="鳥の群れ", s="着水の直後の機体〈2009年1月15日〉"),
    # c105＝[15] 機体に寄せたフェリー（全面・ゆっくり寄る）。🔴 芯の引き＝この画の終わり 43.5秒（46秒より前）
    "c105": dict(photo=_C15, **ss.mv(_C15, "in", fx=0.55, fy=0.44), side="none", color=1.0,
                 t="シミュレーター", s="機体のそばのフェリー〈2009年1月15日〉"),   # 🔧 「寄せた」は作り手の言葉（門番 check_credits）＝一覧も over32.psv で直した
    # c106＝[18] フェリーの群れ（全面・ゆっくり寄る）。🔧 試し焼き（Actions 42776414038）の原寸で、左上のヘリコプターは見出し「報告書の結論」の字の下に
    #   隠れた（写真の左上の端＝どの寄せでも見出しの帯に入る）＝副題からヘリコプターを外した（一覧も over32.psv で直した）
    "c106": dict(photo=_C18, **ss.mv(_C18, "in", fx=0.45, fy=0.45), side="none", color=1.0,
                 t="報告書の結論", s="集まったフェリー〈2009年1月15日〉"),
    # c107＝[21] 消防艇と小舟・翼と尾翼（PD-USACE・全面・ゆっくり寄る）。見出しに「奇跡」を書かない（語りの言わない語＝make_list32.SAY_NOT）
    "c107": dict(photo=_C21, **ss.mv(_C21, "in", fx=0.55, fy=0.59), side="none", color=1.0,
                 t="報告書の言葉", s="機体のまわりの消防艇と小舟〈2009年1月15日・陸軍工兵隊〉"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-11-10）：紙面（報告書 NTSB/AAR-10/03・連邦官報）＝21カットの型（c1・c3〜c7・ca〜cc の同じ節）
# ══════════════════════════════════════════════════════════
#   束＝`qa_out/ep32_assets.py` の PAGE_CUT（PDF の頁の切り口＝字の層と OCR で行を照らし、縁の黒・隣の段・名前の網を測った）。PLAN の kind＝「文字の頁」（31本目の型）。
#   額は静止・地は同じ紙面のぼかし（ss.PAGE_BLUR）・額の大きさは面積の大きい方（縦横比 1.74 まで＝高さいっぱい ptall・それより横長＝幅いっぱい pw=1776
#   ＝台帳 assets.json の fit・一覧の「額装（高さいっぱい）」から横長だけ替えた）。見出し（t）は話題の札・副題（s）は写っている紙面の名
_R112 = P("r1_c112")
SPEC.update({
    # c112＝報告書の表紙の題の段＋右下の番号（🔴 飾りの写真は入れない＝報告書の雛形の絵・この事故の写真でない）。1722×816＝幅いっぱい
    "c112": dict(photo=_R112, panel=True, pw=1776, ground=dict(photo=_R112, blur=ss.PAGE_BLUR), color=1.0,
                 t="公開された記録", s="NTSB の事故の報告書の表紙"),
})

# 🆕 ⑤b-3b（2026-11-10）：衛星写真（額装・静止・`ss.sat`＝帰属の行は地図の右下・色を変えない）。点は ss.GEO（出どころつき）・線は ss.SAT_LINES（lines32.py）。
#   c109＝G01 ニューヨーク（ズーム12）：飛んだ道（レーダーの記録）・出発した空港・着水した所（×＝報告書の座標）
SPEC.update({
    "c109": dict(
        **ss.sat("G01", steps=[
            [dict(k="line", path=ss.SAT_LINES["path_g01"], c="INK_W", t="飛んだ道", u=0.12, lab=(24, 0, "start")),
             dict(k="pt", at="lga", c="INK_W", t="ラガーディア空港", lab=(24, 10, "start")),
             dict(k="x", at="ditch", t="着水した所", lab=(-30, 40, "end"))]],
            note=ss.SAT_LINE_NOTE),
        t="空港か、川か", s="ニューヨーク〈現在の衛星写真〉"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-11-11）：写真の束の残り（c1〜cc の同じ節＝46カット）
# ══════════════════════════════════════════════════════════
#   全面（一覧の見せ方「全面」・動き「ゆっくり寄る」）＝`ss.mv(…, "in", fx, fy)`（c104〜c107 の型）。寄る先 (fx, fy) は 11-11 に 640px の並べ
#   （10% の目盛り・16:9 の窓の枠＝scratchpad `sheet46.py`）で見て決めた。額装（「額装（高さいっぱい）」・静止）＝panel・ptall・地は同じ写真のぼかし
#   （c103 の型・BY-SA と調査の写真は額装だけ＝check_frame_only）。見出し（t）は話題の札（12字未満・語りの丸写しにしない＝echo）・
#   副題（s）は一覧 list32.tsv の sub（写っているもの＝映像方針で頁の説明・EXIF と照らした）
_C1, _C49, _C36, _C13 = P("c1"), P("c49"), P("c36"), P("c13")
SPEC.update({
    # c108＝[1] 川一面の船（手前に艦のマストと桟橋）＝船の列へ寄る
    "c108": dict(photo=_C1, **ss.mv(_C1, "in", fx=0.45, fy=0.45), side="none", color=1.0,
                 t="NTSB の調査", s="川に集まった船〈2009年1月15日〉"),
    # c110＝[49] この機体の操縦室の天井（上の帯に ENG 1・APU・ENG 2 の赤い覆い）＝その帯へ寄る
    "c110": dict(photo=_C49, **ss.mv(_C49, "in", fx=0.45, fy=0.3), side="none", color=1.0,
                 t="手順書の3分の1", s="この機体の操縦室の天井〈博物館の展示〉"),
    # c111＝[36] 沿岸警備隊の小舟 25640 と左の奥の沈みかけの機体（晴れた昼・EXIF 1月16日）＝両方が入る所へ
    "c111": dict(photo=_C36, **ss.mv(_C36, "in", fx=0.45, fy=0.55), side="none", color=1.0,
                 t="偶然と勧告", s="岸壁のそばの機体と沿岸警備隊の小舟〈2009年1月16日〉"),
    # c113＝[13] 氷の川の警察の船と引き船（機体は写っていない）＝船へ寄る。冒頭の終わり（次は第1章の扉）
    "c113": dict(photo=_C13, **ss.mv(_C13, "in", fx=0.45, fy=0.62), side="none", color=1.0,
                 t="冬の午後3時", s="氷の浮かぶハドソン川の警察の船と作業船〈2009年1月〉"),
})
