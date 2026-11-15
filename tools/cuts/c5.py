# -*- coding: utf-8 -*-
"""第4章　「部屋で待て」 c501–c526（26カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c5.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep33/make_plan33.py` で
  映像方針の一覧（`ref/ep33/eizou_build/make_list33.py`＝了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep33/eizou_list33.md`＝⑤b は一覧に従う）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。公的な機関の頁（訳の札つき）は最初から「文字の頁」。
  🔴 額装・帯の写真は静止（`build_jiko.FRAME_STILL_EP` に ep33）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。
  🔴 写真は画面いっぱい・色は原本（`build_jiko.PHOTO_KEEP_EP` に ep33）・BY-SA は額装・報告の図と頁も額装。説明カットの地は昼の写真を暗くするだけ（8:1・衛星・夜・BY-SA は地にしない）。
  🔴 #15（Commons の映像）は等速・止めなし・頭から使う・同じ秒を2回使わない・場面の切れ目をまたがない（区間は一覧の動きの欄＝make_list33 の門番）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針（と ⑤b-1 の c526）で台本の画の欄から替えたカット。
  🔴 この回の線＝住民（亡くなった人・生き残った人・出火した部屋の住人）は名前なし（人数だけ）・消防士と指揮者は立場・調査の委員長と大臣と区の幹部は役職・
     会社と団体は報告が名指しした結論の範囲で名前・社員と専門家は役職・刑事は警視庁の発表の数と日付だけ・「見捨てた」「英国史上最悪」「60時間」は使わない・
     追悼の場と支援の掲示は使わない＝図でも同じ（報告の図・頁・写真に名前の字が写る＝親が絵を見て切る）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c501': dict(kind='図・写真の頁',
               plan='F:P1V1-7.2｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：指令室の中〈報告の図〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第1巻 図7.2（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.9（`those calls requiring potentially life-saving fire survival guidance (FSG calls)`）・P1ES¶2.11（`Control room decides to revoke the "stay put" advice and tell all occupants calling 999 to leave the tower`）'),
    'c502': dict(kind='図解',
               plan='地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：国の指針の札＝火が部屋の外へ広がり「部屋で待て」が成り立たなくなったときの避難の計画を、消防が前もって用意する｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.17（`National guidance requires fire and rescue services to draw up contingency evacuation plans for dealing with fires in high-rise buildings that spread beyond the compartment of origin causing a "stay put" strategy to become untenable`）'),
    'c503': dict(kind='文字の頁',
               plan='P:c503｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「その時点は、早くて1時30分、遅くとも1時50分には来ていた」｜動き：静止｜見た目の型：P1V4 ¶28.6 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第4巻 ¶28.6（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.6（`That point had been reached by 01.30 at the earliest and by 01.50 at the latest`）'),
    'c504': dict(kind='図解',
               plan='地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：時計｜副題：文字盤に4つの時刻の札＝1:26 てっぺん・1:30〜1:50 切り替えるべき時・2:35 指令室・2:47 現場｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.14（`very top of the building by 01.26`）・P1ES¶2.11（`Control room decides to revoke the "stay put" advice`）・P1V4¶28.6（`by 02.47 when the "stay put" advice was withdrawn`）'),
    'c505': dict(kind='図解',
               plan='地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：1:50 の札＝168人が逃げた・階段はまだ通れた・全員を逃がすことだけが命を守る現実の道｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.19（`By 01.50 168 of the 297 occupants of the building had escaped`）・P1V4¶28.20（`a full evacuation of the building had become the only realistic way of minimising loss of life and serious injury`）・P1V4¶28.27（`at least up to 01.50 the stairs remained passable`）'),
    'c506': dict(kind='図解',
               plan='地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：最初の現場の指揮者の札＝経験はある・階級は高くない・台所の火への出動・名前なし｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.19（`the first incident commanders, although experienced, were of relatively junior rank`）・P1V4¶28.4（`wholly outside his experience and training`）'),
    'c507': dict(kind='図解',
               plan='地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：指揮者の考えの外にあった2つの札＝区画が全体で崩れる・大勢をまとめて逃がす｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.19（`None of them seem to have been able to conceive of the possibility of a general failure of compartmentation or of a need for mass evacuation`）'),
    'c508': dict(kind='フリー素材',
               plan='X508｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：並んだ防火服とヘルメット｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.54（`the "stay put" concept had become an article of faith within the LFB so powerful that to depart from it was to all intents and purposes unthinkable`）'),
    'c509': dict(kind='図解',
               plan='地：X508（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：訓練の札＝いつ避難に切り替えるかの見きわめ方・避難の進め方＝どちらも教わっていない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.45（`it was due to deficiencies in his training which failed to equip him with the means of deciding when to switch from the "stay put" strategy to one of partial or total evacuation`）・P1ES¶2.18（`LFB incident commanders had received no training in how to recognise the need for an evacuation or how to organise one`）'),
    'c510': dict(kind='文字の頁',
               plan='P:c510｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「グレンフェル・タワーの避難の計画は無かった」｜動き：静止｜見た目の型：P1ES ¶2.18 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第1段階の報告 要約 ¶2.18（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.18（`There was no contingency plan for the evacuation of Grenfell Tower`…`had received no training in the particular dangers associated with combustible cladding`）'),
    'c511': dict(kind='図解',
               plan='地：X508（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：情報の流れ＝指令室に入る通報の数と部屋・塔の中の火の広がり・警察のヘリの映像 → 現場の指揮者に届かない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.19（`No systematic arrangements were made for information about the number and source of FSG calls to be communicated to the incident commanders`…`pictures from the police helicopter were not available to them`）'),
    'c512': dict(kind='図解',
               plan='地：X508（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：流れ｜副題：現場の指揮者の交代の札＝1:50・1:58・2:04・2:11・2:44〈立場だけ・名前なし〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`hands over incident command to`…`not knowing that`…`has already assumed command`…`takes handover from`）'),
    'c513': dict(kind='フリー素材',
               plan='X513｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜の高層住宅の窓の明かり｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.74（`at or shortly after 02.00 that the "stay put" advice should be revoked and a full evacuation ordered`）'),
    'c514': dict(kind='文字の頁',
               plan='P:c514｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「2時までに避難の命令が出ていれば、亡くなる人は、まず間違いなく、より少なかった」｜動き：静止｜見た目の型：P1V4 ¶28.63 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第4巻 ¶28.63（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.63（`I have little doubt that fewer people would have died if the order to evacuate had been given by 02.00`）'),
    'c515': dict(kind='フリー素材',
               plan='X515｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：電話の受話器とヘッドセット｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.75（`taken at around 02.35`…`nowhere in the building could be regarded as a place of safety and that the "stay put" advice should be revoked`）'),
    'c516': dict(kind='写真',
               plan='C26｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：塔〈2018年6月〉｜動き：静止｜権利：CC BY-SA 2.0｜時期：2018-06-29 15:40｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 2.0・無加工）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`takes over incident command from`…`revokes the "stay put" advice`）'),
    'c517': dict(kind='図解',
               plan='地：X515（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：時計｜副題：文字盤＝遅くとも1:50 から 2:47 までを塗る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.6（`by 02.47 when the "stay put" advice was withdrawn the best part of an hour had been lost without any evacuation plan having been considered`）'),
    'c518': dict(kind='図解',
               plan='地：X515（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：2:44 の札＝階段の様子が悪くなり、全員をまとめて逃がすのは、もう間に合わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.77（`it was no longer practicable to carry out a supervised mass evacuation due primarily to the deterioration in conditions in the stairs`）'),
    'c519': dict(kind='図解',
               plan='地：X515（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：棒｜副題：2:35 より前に逃げた181人・2:35 より後に逃げた46人＝うち 2:53〜8:07 に約36人｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.81注72（`The total number of occupants escaping after the control room revoked the "stay put" advice at around 02.35 was 46`）・P1V4¶28.81（`some 36 occupants escaped from the tower between 02.53 and 08.07`）・計（227−46＝181）'),
    'c520': dict(kind='写真',
               plan='C23｜一覧の種類：写真｜見せ方：全面｜副題：地下鉄と焼けた塔〈2018年1月〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2018-01-05 12:36｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.19（`The firefighters who attended the tower displayed extraordinary courage and selfless devotion to duty`）・P1V4¶28.1（`displayed enormous courage and selfless devotion to duty`）'),
    'c521': dict(kind='図解',
               plan='地：C23（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：2つの札＝隊員の勇気と、指揮と作戦の欠け〈前者は後者を覆い隠さない〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.5（`The bravery and commitment to duty shown by individual firefighters cannot mask or excuse the deficiencies in the command and conduct of operations`）'),
    'c522': dict(kind='図解',
               plan='SAT:ラカナル・ハウス｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：ラカナル・ハウス〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：撮影の時点は ⑤b で｜人：なし｜出典の行：Google の表示（絵のそば）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・撮影の時点は副題に書かない・帰属は地図の右下・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.9（`On 3 July 2009 a fire broke out on floor 9 of Lakanal House, a 14-floor building in Southwark`…`Six people died`）・P2V5¶83.1（`had all been foreshadowed by previous fires, most particularly, the Lakanal House fire on 3 July 2009`）'),
    'c523': dict(kind='文字の頁',
               plan='P:c523｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「指導力の長年の欠け・慢心の文化」｜動き：静止｜見た目の型：P2V5 ¶83.3 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第5巻 ¶83.3（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="P2V5¶83.3（`The LFB's failure lay in its inability to implement any effective response`…`a chronic lack of effective leadership, combined with an undue emphasis on process and a culture of complacency`）"),
    'c524': dict(kind='図解',
               plan='地：C23（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：指令室の訓練の札＝取り残された人への助言の定期の学び直しの訓練＝2009年も2017年も無し・お金の不足が原因と述べた証｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V5¶83.6（`In 2009, no structured or regular fire survival guidance refresher training was provided by the LFB and this was still the case at the time of the Grenfell Tower fire in 2017`）・P2V5¶83.12（`none of the witnesses from whom we heard told us that insufficient financial or other resources had caused or contributed to the failings`）'),
    'c525': dict(kind='写真',
               plan='C68｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：高速道路から見た塔〈2021年〉｜動き：静止｜権利：CC BY-SA 2.0｜時期：2021-10-10｜人：なし（車）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 2.0・無加工）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（2つ目の問いの答え）'),
    'c526': dict(kind='写真',
               plan='🔧 C24｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：枝の向こうの焼けた塔〈2018年1月〉｜動き：静止｜権利：CC BY 2.0｜時期：2018-01-05 12:41｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：白黒の原本（色は原本のまま）・縦＝高さいっぱいの額＋同じ写真のぼかしの地・静止（額装は静止）・副題は ⑤b で原寸を見て直す｜新しい画（映像方針）：🔧 #15 の T6 は実測 7.36秒（場面の切れ目 209.287〜216.647）＜カットの画面 7.57秒＝T7（家並みの通り＝別の構図）が 0.47秒入る＝⑤b-1（11-15）に 1080p の切れ目の前後のコマで見た → 控えの [67] は c816 の替え（[60] を外したとき）で使っている＝使っていない [24]（T6 と同じ「枝の向こうの塔」）へ｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（3つ目の問いへのつなぎ）'),
}

SPEC = {}
