# -*- coding: utf-8 -*-
"""第9章　あの夜のあとに、変わったこと ca01–ca17（17カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/ca.py`）。
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
    'ca01': dict(kind='文字の頁',
               plan='P:ca01｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「混乱し、遅く、決められず、場当たりだった」｜動き：静止｜見た目の型：P2V1 ¶2.103 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.103（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.103（`In the first week after the fire at Grenfell Tower the response of the government and RBKC was muddled, slow, indecisive and piecemeal`）'),
    'ca02': dict(kind='フリー素材',
               plan='Xa02｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：ロンドンの住宅街の遠景｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V7¶98.1（`hundreds of people were displaced from their homes in the tower and surrounding`）・P2V1¶2.104（`Certain aspects of the response demonstrated a marked lack of respect for human decency and dignity`）'),
    'ca03': dict(kind='フリー素材',
               plan='Xa03｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：支援の物資を仕分ける手もと｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.114（`With the support of local voluntary organisations, they provided support in the hours immediately following the fire when the authorities were conspicuous by their absence`）'),
    'ca04': dict(kind='文字の頁',
               plan='P:ca04｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「規制の仕組みは、目的に合っていない」｜動き：静止｜見た目の型：中｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：建築規制と防火の独立の見直し 中間報告（2017年12月・英国政府）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='中（`the current regulatory system for ensuring fire safety in high-rise and complex buildings is not fit for purpose`）'),
    'ca05': dict(kind='図解',
               plan='地：Xa03（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：「底辺への競争」の札＝安く早くを競う・知らないか、無関心か、仕組みが良いやり方を助けないか｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="終（`can be described as a 'race to the bottom' caused either through ignorance, indifference, or because the system does not facilitate good practice`）"),
    'ca06': dict(kind='文字の頁',
               plan='P:ca06｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：（訳なし・頁だけ）｜動き：静止｜見た目の型：報告の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第1段階の報告（2019）・第2段階の報告（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第1段階の報告＝2019-10-30・第2段階の報告＝2024-09-04）'),
    'ca07': dict(kind='文字の頁',
               plan='P:ca07｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「高さ18メートル以上か7階建て以上・住戸2つ以上」｜動き：静止｜見た目の型：法｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：Building Safety Act 2022 第65条（英国）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='法（`28th April 2022`…`at least 18 metres in height or has at least 7 storeys`…`contains at least 2 residential units`）'),
    'ca08': dict(kind='図解',
               plan='地：Xa03（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：第2段階の報告の勧告の札＝58・国へ37・ほかの組織へ21｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='応（`The Inquiry made 58 recommendations, of which 37 were directed at the government and 21 were directed at other bodies and institutions`）'),
    'ca09': dict(kind='文字の頁',
               plan='P:ca09｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「起きた死は、すべて避けられた」｜動き：静止｜見た目の型：首｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：首相の議会での声明（2024年9月4日・英国政府）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='首（`concluded this morning`…`the simple truth is that the deaths that occurred were all avoidable`）'),
    'ca10': dict(kind='写真',
               plan='C18｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：火事から1年の塔〈2018年6月〉｜動き：静止｜権利：CC BY-SA 4.0｜時期：2018-06-18 17:59｜人：なし（幕は標語だけ＝11-15 に見た）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 4.0・無加工）｜注：幕の字は標語だけ（GRENFELL FOREVER IN OUR HEARTS＝11-15 に見た）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='首（`I want to start with an apology on behalf of the British state to each and every one of you`…`It should never have happened`）'),
    'ca11': dict(kind='文字の頁',
               plan='P:ca11｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「49は全面で、残る9は考え方として受け入れる」｜動き：静止｜見た目の型：応｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告への政府の応答（2025年2月）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='応（`49 of the recommendations are being accepted in full by the government and other responsible organisations`…`As regards the remaining 9, which are all directed at government, the government accepts them in principle`）'),
    'ca12': dict(kind='図解',
               plan='地：Xa03（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：変わった決まりの札＝18メートルをこえる住宅などの外壁に燃える材料を禁止〈イングランド〉・新しい共同住宅のスプリンクラー｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='応（`The use of combustible materials in and on external walls of buildings, including flats, hospitals and student accommodation over 18 metres in height, has been banned`…`The threshold for the provision of sprinklers in new blocks of flats has been lowered from over 30 metres to over 11 metres`）'),
    'ca13': dict(kind='フリー素材',
               plan='🔧 Xa13｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：共同住宅の階段｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜注：字・標識・人は見せない｜新しい画（映像方針）：🔧 模式 → イメージ（2つ目の階段の指針）＝模式の続きを切る｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='応（`There will be statutory guidance on the need for a second staircase in all new buildings over 18 metres coming into force in 2026`…`By the end of 2029, all buildings over 18 metres with unsafe cladding in a government funded scheme will have been remediated`）'),
    'ca14': dict(kind='文字の頁',
               plan='P:ca14｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「61件のうち30件が済み」｜動き：静止｜見た目の型：進｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査への政府の進捗報告（2026年9月）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='進（`Total 61 31 30`…`We continue to expect that all recommendations will be implemented by the end of 2029`）'),
    'ca15': dict(kind='写真',
               plan='🔧 C58｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：覆われた塔〈2024年8月〉｜動き：静止｜見た目の型：原寸を11-15に見た｜権利：CC0｜時期：2024-08-17 14:09｜人：なし（下の追悼の壁は切って入れない）｜出典の行：写真：Wikimedia Commons（CC0・改変：切出）｜注：上の 1920×1700 だけ（壁に人の顔の絵の掲示＝11-15 に原寸で見た）・地のぼかしも切った絵から｜新しい画（映像方針）：🔧 [45]（2018年5月）→ [58]（2024年8月＝取り壊しの前のいちばん新しい姿・CC0）＝下の追悼の壁は切って入れない（改変：切出）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='塔（`will be carefully taken down to the ground`…`commenced in September 2025`）・年（`We expect the work to continue until at least spring 2027`）'),
    'ca16': dict(kind='図解',
               plan='地：Xa13（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：変わったことの札＝見直し・建築安全法・2つの報告・勧告の半分近く・取り壊し｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第9章のまとめ）'),
    'ca17': dict(kind='図解',
               plan='地：Xa13（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：問いの札＝誰かが、罪に問われるのか｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第10章へのつなぎ）'),
}

SPEC = {}
