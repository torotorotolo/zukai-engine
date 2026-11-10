# -*- coding: utf-8 -*-
"""第8章　4分後のフェリー c901–c920（20カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c9.py`）。
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
    'c901': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：最初のフェリー〈沿岸警備隊の監視カメラ〉｜動き：映像 230.00〜240.00秒｜見た目の型：11-10 原寸 230・234・237・240秒＝×9.0 の引きで右からフェリーが寄る・235〜237秒にカメラの寄り｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：カメラの寄り（元の映像のまま）が入る｜新しい画（映像方針）：🔧 区間 3分52秒〜4分 → 230.0秒から（引きの絵でフェリーが寄る）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p59（`1534:40 – first vessel arrived on scene`）・計（15:30:43 から 15:34:40 まで＝3分57秒）'),
    'c902': dict(kind='図解',
               plan='SAT:着水した所｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：着水した所とフェリー乗り場〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p62（`The airplane was ditched on the Hudson River near the NY WW Port Imperial Ferry Terminal in Weehawken, New Jersey`）・報p120（`ferry captains either witnessed the accident or were notified about it by the director of ferry operations`）'),
    'c903': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：横付けした船〈沿岸警備隊の監視カメラ〉｜動き：映像 273.00〜283.10秒｜見た目の型：11-10 原寸 273・283秒＝×16.5・機体の横のフェリー／⑤b-1 原寸 272.7・273.0・280.3・281.3・282.3・283.0秒＝280〜282秒は方位 283→284 のわずかな振れ（倍率 ×16.5 のまま）・283.0秒は 282.3秒と同じ絵｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 区間 4分〜5分 → 273.0秒から（カメラが落ち着いた 273〜283秒）・⑤b-1 実測 10.05秒＝尻を 283.10 へ（283.0秒のコマを 0.1秒足すだけ・次の切れ目 283.67→284.0秒の手前・等速・頭は動かさない）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p120（`Although the ferry captains were not trained to respond to a commercial airplane accident`…`they were the first to arrive on scene and rescue the occupants from the airplane wings, slide/rafts, and cold water`）'),
    'c904': dict(kind='フリー素材',
               plan='X904｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：フェリーの甲板と手すり〈社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p64（`Before the accident, NY WW had asked to participate in the mass-casualty exercises with the New York and New Jersey response agencies; however, the request was not granted`）・報p64（`The day after the accident, the Port Authority of NY and NJ informed the NY WW that they would be included in future mass-casualty emergency response exercises`）'),
    'c905': dict(kind='写真',
               plan='🔧 D68-3｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：救助に加わったフェリー〈2009年1月17日・NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009-01-17（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（救助の写真3）｜注：🔴 船の名（人の名）は読ませない＝⑤b で原寸｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#68 写真3）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p64（`NY WW also conducted a series of monthly drills, live exercises, and actual rescues before the accident`）・報p139（`and their training before the accident`）'),
    'c906': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：翼の上の人と船〈沿岸警備隊の監視カメラ〉｜動き：映像 306.00〜325.00秒｜見た目の型：11-10 原寸 306・324秒＝×17.2・翼の上の人とフェリー｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 区間 5分〜6分 → 306.0秒から・副題を写っているものに｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p120（`the other six ferries arrived on scene within 10 minutes`…`one FDNY fire rescue boat arrived on scene within 8 minutes, and two USCG boats were on scene within 17 minutes`）・報p62（`the first NY WW vessel arrived on scene about 1534, and the six other NY WW ferries arrived on scene by about 1540`）・報p62（`one FDNY fire rescue boat and two small USCG boats arrived on scene about 1539 and 1548, respectively`）'),
    'c907': dict(kind='写真',
               plan='C3｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：機体のまわりの船〈2009年1月15日・沿岸警備隊〉｜動き：静止｜見た目の型：11-10 640px＝沈みかけの翼と尾翼・消防艇｜権利：CC BY 2.0｜時期：2009-01-15 17:43（EXIF）｜人：乗り組みの人（中景・小さい）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：600px＝額装｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p63（`The USCG incident commander shut down vessel traffic on the Hudson River about 1535`）'),
    'c908': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：翼の上に並ぶ人〈沿岸警備隊の監視カメラ〉｜動き：映像 335.00〜347.50秒｜見た目の型：11-10 原寸 334・348秒＝×31・翼の上の人の列・右にフェリー｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 区間 6分〜7分 → 335.0秒から・副題を写っているものに｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p120（`According to video footage obtained by the NTSB, all of the occupants were rescued within about 20 minutes of the ditching`）'),
    'c909': dict(kind='図解',
               plan='🔧 地：C1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：救助の時刻の札＝約4分 最初のフェリー・約20分 全員・24分 最後の船が離れる｜注：—｜新しい画（映像方針）：🔧 地 [3]（600px）→ [1]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p120（`all of the occupants were rescued within about 20 minutes of the ditching`）・報p59（`1554:43 – last vessel departed with last rescued passengers off left off-wing slide`）・計（15:30:43 から 15:54:43 まで＝24分）'),
    'c910': dict(kind='写真',
               plan='🔧 V15｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：船のそばの機体〈沿岸警備隊の監視カメラ〉｜動き：映像 7.00〜17.00秒｜見た目の型：11-10 原寸 7・17秒＝×23.5・フェリーと消防艇のあいだの機体｜権利：PD（PD-USCG）｜時期：2009-01-15 15:46ごろ｜人：なし（遠景の船）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 区間を決めた（カメラが落ち着いた 7〜17秒）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p120（`if the rescue vessels had not been near the accident site, it is likely that some of the airplane occupants would have drowned due to cold shock or swimming failure`）'),
    'c911': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：機体を囲む船〈沿岸警備隊の監視カメラ〉｜動き：映像 464.50〜474.00秒｜見た目の型：11-10 原寸 465・474秒＝×19.6・3隻のフェリー｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：ゆとりが少ない＝⑤b-1 の実測で足りなければ 450〜462秒（未見）を見る｜新しい画（映像方針）：🔧 区間 7分〜8分 → 464.5秒から（415〜427秒は背景にコンコルド＝外した）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p139（`The emergency response was timely and efficient because of the proximity of the emergency responders to the accident site, their immediate response to the accident, and their training before the accident`）'),
    'c912': dict(kind='写真',
               plan='🔧 C4｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：尾翼のまわりの消防艇と小舟〈2009年1月15日・沿岸警備隊〉｜動き：静止｜見た目の型：11-10 640px＝消防艇と警察の船・尾翼・奥にビル｜権利：CC BY 2.0｜時期：2009-01-15（絵＝川の中の機体と消防艇）｜人：乗り組みの人（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：746px＝額装｜新しい画（映像方針）：🔧 副題を写っているものに｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p52（`Forty-five passengers and all 5 crewmembers were transported to hospitals after the accident`）'),
    'c913': dict(kind='図解',
               plan='🔧 地：C18（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：重いけがの5人の札＝胸の骨の端の骨折・低体温症・肩の骨折2人〈あとで申し出た〉・客室乗務員の足の傷・顔は描かない｜注：—｜新しい画（映像方針）：🔧 地 [4]（746px）→ [18]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p52（`One of the passengers sustained a fractured xiphoid process`…`The other passenger suffered hypothermia and was not released from the hospital until about 1645`…`January 17, 2009`）・報p53（`one of these passengers sustained a fractured left shoulder and that the other passenger sustained a fractured right shoulder`）'),
    'c914': dict(kind='フリー素材',
               plan='X914｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：旅客機の座席の列を横から〈人なし〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p139（`The Federal Aviation Administration’s (FAA) current recommended brace positions do not take into account newly designed seats that do not have a breakover feature, and, in this accident, the FAA-recommended brace position might have contributed to the shoulder fractures of two passengers`）'),
    'c915': dict(kind='写真',
               plan='🔧 C38｜一覧の種類：写真｜見せ方：全面｜副題：翌日、岸壁につながれた機体〈2009年1月16日・沿岸警備隊〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝岸壁へ綱でつながれた翼と尾翼・沿岸警備隊の小舟｜権利：PD（PD-USCG）｜時期：2009-01-16（[37]＝同じ写真の切り抜きの頁の説明「tied up next to Battery Park City on Jan. 16」）｜人：乗り組みの人（中景・公的な任務）｜出典の行：写真：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：全面は左寄りの切り出し（翼・尾翼・綱が入る）｜新しい画（映像方針）：🔧 [7]（EXIF 1月17日・はしけの上）→ [38]（1月16日・岸壁に綱）＝語りを「その日の夕方の写真」→「翌日の写真」に（V2-184）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（Commons の頁の説明と撮影日＝映像方針 11-10）・報p41（`the current was ebbing at 1.4 kts`）'),
    'c916': dict(kind='写真',
               plan='C46｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：引き上げられる機体〈2009年1月〉｜動き：静止｜見た目の型：11-10 640px＝夜・クレーンで吊られる機体・氷の川｜権利：CC BY-SA 3.0｜時期：2009-01（頁の説明）・夜｜人：作業の人（遠景・小さい）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 3.0）・無加工｜注：BY-SA＝額装・無加工｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p30（`when the airplane was recovered from the water`）'),
    'c917': dict(kind='写真',
               plan='C33｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：引き上げられた左のエンジン〈2009年1月・陸軍工兵隊〉｜動き：静止｜見た目の型：11-10 640px＝吊られた左のエンジン・工兵隊の引き船｜権利：PD（PD-USACE）｜時期：2009-01-23（報告書 p50＝事故の8日後）｜人：作業の人（遠景）｜出典の行：写真：U.S. Army Corps of Engineers（public domain）／Wikimedia Commons｜注：640px＝額装・事故の8日後（報告書 p50）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p47（`The right engine was found attached to the wing`）・報p50（`The left engine was found near the initial impact location of the airplane with the water`…`January 23, 2009 (8 days after the accident)`）'),
    'c918': dict(kind='図解',
               plan='🔧 地：C1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：救助の流れ＝フェリー・消防・沿岸警備隊の3つの札と岸の札｜注：—｜新しい画（映像方針）：🔧 地 [7]（地のためだけに取る写真）→ [1]（c909 と同じ地・救助の船）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p63（`The WPD established an incident command post in New Jersey at the Port Imperial Ferry Terminal`）・報p63（`indicated that they were dropped off on the New York side of the Hudson River, and 55 of them indicated that they were dropped off on the New Jersey side of the river`）'),
    'c919': dict(kind='写真',
               plan='🔧 V20｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：集まった船〈沿岸警備隊の監視カメラ〉｜動き：映像 37.00〜68.00秒｜見た目の型：11-10 原寸 37・69秒＝×20.4・フェリーの群れ｜権利：PD（PD-USCG）｜時期：2009-01-15 15:50ごろ｜人：なし（遠景の船）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 区間を決めた（36〜69秒）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`and that the airplane was ditched near vessels immediately available to rescue the passengers and crewmembers`）'),
    'c920': dict(kind='写真',
               plan='🔧 V20｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：引き船と機体〈沿岸警備隊の監視カメラ〉｜動き：映像 133.50〜144.00秒｜見た目の型：11-10 原寸 133・144秒＝×25.6・クレーンの船と引き船のそばの機体｜権利：PD（PD-USCG）｜時期：2009-01-15 15:50ごろ｜人：なし（遠景の船）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 区間を決めた（133〜144秒）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（橋の1行）'),
}

SPEC = {}

# 🆕 ⑤b-3b（2026-11-10）：衛星写真（額装・静止・型は c1.py の同じ節）。c902＝G08（ズーム14）：着水した所（×＝報告書の座標）→ 段2 でフェリー乗り場
#   （Google マップの地点「Port Imperial Ferry Terminal」＝一般の座標・着水した所から北西へ 約750メートル）
SPEC.update({
    "c902": dict(
        **ss.sat("G08", steps=[
            [dict(k="x", at="ditch", t="着水した所", lab=(30, 10, "start"))],
            [dict(k="pt", at="ferry", c="INK_W", t="フェリー乗り場", lab=(-26, -8, "end"))]],
            note="点は一般の座標・×は報告書の座標"),
        t="乗り場の近く", s="ハドソン川のウィーホーケンの前〈現在の衛星写真〉"),
})

# 🆕 ⑤b-3b（2026-11-10）：VTS（沿岸警備隊の監視カメラ・PD-USCG）＝型は c8.py の同じ節（c101・c102 と同じ書き方）
SPEC.update({
    # 副題は〈沿岸警備隊の監視カメラ〉の前を7字まで（額の左端 x738・副題は x72 から1字 32px＝門番 check_fmove）
    "c901": ss.vid("c901", ptall=True, t="着水から約4分", s="最初のフェリー〈沿岸警備隊の監視カメラ〉"),
    "c903": ss.vid("c903", ptall=True, t="訓練のない救助", s="横付けした船〈沿岸警備隊の監視カメラ〉"),
    "c906": ss.vid("c906", ptall=True, t="7隻のフェリー", s="翼の上の人と船〈沿岸警備隊の監視カメラ〉"),
    "c908": ss.vid("c908", ptall=True, t="約20分で全員", s="翼の上に並ぶ人〈沿岸警備隊の監視カメラ〉"),
    "c910": ss.vid("c910", ptall=True, t="報告書の見立て", s="船のそばの機体〈沿岸警備隊の監視カメラ〉"),
    "c911": ss.vid("c911", ptall=True, t="救助の所見", s="機体を囲む船〈沿岸警備隊の監視カメラ〉"),
    "c919": ss.vid("c919", ptall=True, t="船の近さ", s="集まった船〈沿岸警備隊の監視カメラ〉"),
    "c920": ss.vid("c920", ptall=True, t="成功と偶然", s="引き船と機体〈沿岸警備隊の監視カメラ〉"),
})
