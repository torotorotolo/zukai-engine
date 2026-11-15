# -*- coding: utf-8 -*-
"""第2章　午前0時54分、4階の台所 c301–c320（20カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c3.py`）。
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
    'c301': dict(kind='図・写真の頁',
               plan='F:P1V4-21.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：出火した台所〈火事のあと〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第4巻 図21.1（2019）｜注：火のあとの台所の角（警察の写真＝本文の脚注）・人なし・右の写しに赤い線と札 A・B（紙面のまま）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`calls 999 to report a fire in Flat 16, floor 4 Grenfell Tower`）'),
    'c302': dict(kind='図・写真の頁',
               plan='F:P1V4-21.4｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：冷凍冷蔵庫の下の床の焼け跡｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第4巻 図21.4（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.12（`it was started by an electrical fault in a large fridge-freezer in the kitchen of Flat 16`）'),
    'c303': dict(kind='図・写真の頁',
               plan='F:P1V4-21.6｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：部屋の配電盤｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第4巻 図21.6（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.12（`I have not been able to establish the precise nature of the fault in the fridge`…`how the failure of a common domestic appliance could have had such disastrous consequences`）'),
    'c304': dict(kind='図解',
               plan='地：C19（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：台所の間取り＝冷凍冷蔵庫・窓・換気扇の板・ドアの位置の札｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.12（`bears no blame`）'),
    'c305': dict(kind='図・写真の頁',
               plan='F:P1V2-10.6｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：台所の窓の中の火〈1:05〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:05｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.6（2019）｜注：本文「01.05、01.06、01.08、01.09」の順＝10.6 は 01:05:43 の2コマ｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V2¶10.36（`After he had alerted his neighbours`…`From that position he filmed the development of the fire using his mobile telephone`）'),
    'c306': dict(kind='フリー素材',
               plan='X306｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜の街を走る消防車｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`First firefighters reach the tower`…`having made up from 4 to 6, to 8, to 10 and to 15 between 01.13 and 01.28`）・P1V2¶10.22（`The four appliances arrived within the targets set by the 2017 London Safety Plan`）'),
    'c307': dict(kind='図・写真の頁',
               plan='F:P1V2-10.7｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：台所の窓の中の火〈1:06〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:06｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.7（2019）｜注：10.7＝01:06:01〜01:06:05 の4コマ｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V2¶10.37（`When the firefighters reached floor 4 they found the visibility`…`While they were waiting for the dry rising main to be charged with water`）'),
    'c308': dict(kind='図解',
               plan='地：C19（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：窓のわきの樹脂の枠が熱い煙でゆがみ、外壁の中のすき間へ火の通り道ができるまで〈報告の見立て〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.12（`The fire is most likely to have entered the cladding as a result of hot smoke impinging on the uPVC window jamb, causing it to deform and collapse`）'),
    'c309': dict(kind='図・写真の頁',
               plan='🔧 F:P1V2-10.8｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：台所の窓の中の火〈1:08〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:08｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.8（2019）｜注：語りは「開いていた台所の窓から炎が外の板へ」＝窓の中の炎のコマ｜新しい画（映像方針）：🔧 模式（もう1つの道＝開いた窓から炎）→ 図10.8（01:08:10〜01:08:18 の5コマ＝窓の中の炎）＝模式の続きを切る・使っていなかった図｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.12（`It is, however, possible (but less likely) that flames from the fire in the fridge-freezer passed through the open kitchen window and impinged on the ACM cladding panels above`）'),
    'c310': dict(kind='図・写真の頁',
               plan='🔧 F:P1V4-22.8｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：換気扇の板の上の炎〈1:09〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:09｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第4巻 図22.8（2019）｜注：本文 ¶22.20（01.09.30〜01.09.40 のコマ）｜新しい画（映像方針）：🔧 図10.9 → 図22.8（10.9 は c101 へ・22.8 の札 Flames at top of fan infill panel）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`Fire breaks out of Flat 16 into exterior cladding and starts to climb the east facade rapidly`）'),
    'c311': dict(kind='図・写真の頁',
               plan='F:P1V4-22.15｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：部屋の上へ伸びる炎〈1:15ごろ〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:15｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第4巻 図22.15（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶22.27（`cladding can be seen to be burning with some intensity and external flames are extending approximately two floors above Flat 16`）・P1V4¶22.27（`there is a noise which is likely to be the breaking of at least one pane of glazing within the kitchen window`）'),
    'c312': dict(kind='図・写真の頁',
               plan='F:P1V2-10.15｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：東の面の外の火〈1:21〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:21｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.15（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.12（`A kitchen fire of that relatively modest size was perfectly foreseeable`）・P1V1¶4.2（`The principle of the design known as "compartmentation" lies at the heart of these safety features`）'),
    'c313': dict(kind='図解',
               plan='地：C19（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：帯｜副題：時刻の帯＝0:54 通報・0:59 隊が着く・1:09 外壁へ・1:13 5階・1:14 台所のドア・1:21 塔の中か｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.14（`It had reached floor 5 by 01.13`…`very top of the building by 01.26, i.e. in under 20 minutes`）'),
    'c314': dict(kind='図・写真の頁',
               plan='F:P1V2-10.17｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：柱にそって上る炎〈1:27〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:27｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.17（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`First 999 call to the control room from an occupant in the tower`…`First 999 call to report smoke coming into flat from lobby`）・P1V2¶10.90（`said that there was a fire in her kitchen`）'),
    'c315': dict(kind='図・写真の頁',
               plan='F:P1V2-10.24｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：横へ回る炎｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.24（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`makes pumps 20`…`having made up from 4 to 6, to 8, to 10 and to 15 between 01.13 and 01.28`…`makes pumps 25`…`First NPAS (police) helicopter arrives at the scene`）'),
    'c316': dict(kind='写真',
               plan='🔧 C30｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：棟の奥の焼けた塔〈2017年6月18日〉｜動き：静止｜見た目の型：原寸を11-15に見た｜権利：CC BY-SA 2.0｜時期：2017-06-18 09:56・朝｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 2.0・無加工）｜注：⑤b-2 の原寸＝手前に木と低い棟・左下に団地の案内板（通路の名と部屋番号だけ・人の名なし）｜新しい画（映像方針）：🔧 副題を写っているものに（[31] と同じ朝の写真＝書き分けた）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.14（`A total of 112 people had left the tower in the 35 minutes that followed`）'),
    'c317': dict(kind='図解',
               plan='地：C19（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：「部屋で待て」の考え方＝火や煙が来ない限り、部屋にとどまる・部屋ごとに火を閉じこめる区画｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶4.3（`The concept of compartmentation, combined with other supporting fire safety provisions, has given rise to the "stay put" strategy`…`unless they are directly affected by fire, heat or smoke`）'),
    'c318': dict(kind='写真',
               plan='C69｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：焼けた塔〈2017年6月20日〉｜動き：静止｜権利：CC BY 2.0｜時期：2017-06-20 16:47｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.14（`The fire on the outside of the building quickly entered many flats and smoke spread rapidly through the interior of the building`）'),
    'c319': dict(kind='図・写真の頁',
               plan='🔧 F:P1V2-11.6｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：消防の幹部が撮った塔〈1:40ごろ〉｜動き：静止｜見た目の型：図を11-15に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:40／01:43｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図11.6（2019）｜注：5枚の1枚＝署長級の消防士が着いてすぐ撮り 01:43 に送った（本文 ¶11.17）・窓の明かりと1本の炎の柱｜新しい画（映像方針）：🔧 図11.5 → 図11.6（11.5・11.7・11.8 はほぼ同じ「2本の柱」の絵＝c411 の 11.7 と重ねない）・副題を約20字に｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（1つ目の問いへのつなぎ）'),
    'c320': dict(kind='図・写真の頁',
               plan='F:P2V7-109.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：外壁の材料を燃やす実験の装置｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第7巻 図109.1（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.116（`In a series of experiments designed by`…`and carried out at Edinburgh University`）'),
}

SPEC = {}
