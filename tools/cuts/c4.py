# -*- coding: utf-8 -*-
"""第3章　3時間足らずで、塔を包んだ火 c401–c432（32カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c4.py`）。
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
    'c401': dict(kind='図・写真の頁',
               plan='F:P2V7-109.2｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：外壁の材料を燃やす実験〈9分44秒〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第7巻 図109.2（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.115（`The first concerned the respective contributions to the fire made by the ACM rainscreen panels and the polyisocyanurate and phenolic insulation boards`）'),
    'c402': dict(kind='図解',
               plan='地：C69（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：アルミ複合板の芯が熱で溶け、流れ、燃える＝薄いアルミの板が熱を広げ、溶ける芯が増えていく｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V7¶109.19（`Once the polyethylene begins to melt, flow and ignite a complex heat transfer process occurs within the system`…`leading to the melting and involvement of ever greater quantities of polyethylene that then becomes available to burn`）'),
    'c403': dict(kind='図・写真の頁',
               plan='F:P2V7-109.3｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：板がすっかり燃えた実験｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第7巻 図109.3（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.116（`the ACM panels were shown to have been by far the largest potential contributor to energy release in the external wall system at Grenfell Tower`）'),
    'c404': dict(kind='図解',
               plan='地：C69（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：外壁の中＝板と断熱材のあいだのすき間・断熱材が熱をため、燃えて熱を足す・燃えない断熱材でも板はすっかり燃えた｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.117（`Insulation also needs to be present, either to retain energy in the system or to burn and contribute additional energy`…`Even non-combustible insulation in the form of mineral wool resulted in the growth of the fire to full involvement of the ACM panel`）'),
    'c405': dict(kind='図・写真の頁',
               plan='🔧 F:P1V1-6.7｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：窓のまわりの断熱材〈報告の図〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第1巻 図6.7（2019）｜注：図の札は英語のまま（紙面）｜新しい画（映像方針）：🔧 模式 → 図6.7（窓のまわりの燃える断熱材と柔らかくなった樹脂の枠＝語りの「2種類の断熱材と窓のまわりの部材」）＝c629 と2回｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.13（`The presence of polyisocyanurate (PIR) and phenolic foam insulation boards behind the ACM panels, and perhaps components of the window surrounds, contributed to the rate and extent of vertical flame spread`）'),
    'c406': dict(kind='図解',
               plan='地：C69（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：報告の結論の札＝いちばんの理由は芯のポリエチレン・断熱材は火を育てた決め手｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.118（`the principal factor which led to the rapid growth of the fire was the presence of unmodified polyethylene in the cores of the ACM panels rather than the insulation`…`a decisive factor in promoting the growth of the fire`）'),
    'c407': dict(kind='図解',
               plan='地：C69（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：比べ｜副題：板の留め方＝平らな板をリベットで留める形と、箱の形に折った板を引っかける形〈カセット〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.21（`either as flat panels by rivets or as three-dimensional structures, known as cassettes`）・P2V1¶2.117（`Panels in cassette form behave far worse than panels in riveted form`）'),
    'c408': dict(kind='写真',
               plan='C72｜一覧の種類：写真｜見せ方：全面｜副題：焼けた外壁〈2017年6月16日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-16｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.117（`Panels in cassette form behave far worse than panels in riveted form`）・P2V4¶55.34（`the Reynobond panels installed at Grenfell Tower were cassette-fixed`）'),
    'c409': dict(kind='写真',
               plan='🔧 C71｜一覧の種類：写真｜見せ方：全面｜副題：焼けた塔の上部〈2017年6月20日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-20 16:38｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：語り「冠を伝って左右へ」｜新しい画（映像方針）：🔧 模式 → [71]（焼けた冠が写る・c214 と2回）＝模式の続きを切る｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.13（`The crown was primarily responsible for the spread of the fire horizontally`）'),
    'c410': dict(kind='図解',
               plan='地：C71（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：上から溶けて落ちる燃えたポリエチレン → 下の階の外壁に火がつく → 火がまた上へ → 斜めに進む炎の前線｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.13（`The principal mechanism for the spread of the fire horizontally and downwards was the melting and dripping of burning polyethylene from the crown and from the spandrel and column panels, which ignited fires lower down the building`…`thereby allowing the flame front to progress diagonally across each face of the tower`）'),
    'c411': dict(kind='図・写真の頁',
               plan='🔧 F:P1V2-11.7｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：2本の柱にそって燃える塔〈1:40ごろ〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:40／01:43｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図11.7（2019）｜注：5枚の1枚（本文 ¶11.17）｜新しい画（映像方針）：🔧 図11.6（見本帳で端しか見ていない・暗い）→ 図11.7（2本の柱の炎＝語り「柱が火を運ぶ」）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.13（`the columns were a principal route of downwards fire spread`）'),
    'c412': dict(kind='図解',
               plan='地：C71（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：方位｜副題：塔の4つの面＝東・北・南・西と、炎が回った時刻の札〈1:09 東・1:31 北・2:20 南・3:00 西・4:02 合｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`the fire starts to spread to the north elevation of the tower`…`Flames start to spread to south elevation`…`Fire starts to spread across the west elevation of tower, from north to south`）'),
    'c413': dict(kind='図・写真の頁',
               plan='🔧 F:P1V2-13.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：冠で燃える炎〈2:00〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 02:00｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図13.1（2019）｜注：本文の1文（At 02.00 there were flames on the crown）｜新しい画（映像方針）：🔧 副題を写っているものに（図の札 Burning at architectural crown）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`Flames travel across the north and east elevations of the tower, and start to spread around the crown and diagonally across the face of the building`）'),
    'c414': dict(kind='図・写真の頁',
               plan='F:P1V2-12.7｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：東の面のはしご車〈2:05〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 02:05｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図12.7（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V2¶12.22（`turntable ladder had been set up with a water supply on the east side of the tower`）・P1V4¶28.133（`could reach a maximum height of 32 metres, which meant that they could not reach beyond floor 10 of the tower`）'),
    'c415': dict(kind='図・写真の頁',
               plan='🔧 F:P1V3-18.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：燃え広がる塔〈3:34〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 03:34｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第3巻 図18.1（2019）｜新しい画（映像方針）：🔧 [2]（朝8時5分の遠景＝語りの2時50分〜3時半と合わない）→ 図18.1（03:34 のコマ・本文 the first taken at 03.34）＝[2] は取らない｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`Fire spreads horizontally across the south elevation at the crown`…`Flames continue to spread across the south and west elevations of the tower`）'),
    'c416': dict(kind='文字の頁',
               plan='P:c416｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「燃える外装が付けられたことを、消防は知らされていなかった」｜動き：静止｜見た目の型：P1V4 ¶28.3 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第4巻 ¶28.3（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.3（`the fire brigade had never been informed that a combustible rainscreen system had been installed in the first place`）'),
    'c417': dict(kind='図・写真の頁',
               plan='F:P1V3-17.3｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：下の階に出た新しい火〈3:28〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 03:28｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第3巻 図17.3（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V3¶17.4（`caused fires to break out on previously uninvolved external areas`）'),
    'c418': dict(kind='図・写真の頁',
               plan='F:P1V3-19.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：合わさりはじめる炎〈4:02〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 04:02｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第3巻 図19.1（2019）｜注：夜明けの空・図の札 Possible gap between flames（紙面のまま）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V3¶19.1（`began converging at the top of the southern corner of the west face`）・P1ES¶2.11（`Fires on the south and west elevations start to converge at the top of the southern corner of the west face`）'),
    'c419': dict(kind='図解',
               plan='地：C71（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：年表｜副題：1:09 外壁へ → 1:26 てっぺん → 1:31 北 → 2:00 冠と斜め → 2:20 南 → 3:00 西 ｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.13（`It then spread around the top of the building in both directions and down the sides until the advancing flame fronts converged on the west face near the south-west corner, enveloping the entire building in under three hours`）'),
    'c420': dict(kind='写真',
               plan='🔧 C31｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：尖塔と焼けた塔〈2017年6月18日〉｜動き：静止｜見た目の型：原寸を11-15に見た｜権利：CC BY-SA 2.0｜時期：2017-06-18 09:45・朝｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 2.0・無加工）｜注：⑤b-2 の原寸＝並木の通りの奥・尖塔のすぐ後ろに塔・下の通りの車の番号板は額の倍率 0.305 で約2px＝読めない（BY-SA＝加工しない）｜新しい画（映像方針）：🔧 副題を写っているものに（[30] と同じ朝の写真＝書き分けた）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.14（`effective compartmentation was lost at an early stage`）'),
    'c421': dict(kind='図解',
               plan='地：C71（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：区画が崩れたわけ＝熱で窓のガラスが割れる・台所の換気扇の箱がゆがんで外れる・閉じない防火の扉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.14（`The intensity of the heat was such that the glass in the windows inevitably failed, allowing the fire to penetrate flats`…`Extractor fan units in the kitchens had a propensity to deform and become dislodged, providing a point of entry`）'),
    'c422': dict(kind='フリー素材',
               plan='🔧 X422｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：建物の廊下の防火の扉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜注：字・標識・人は見せない｜新しい画（映像方針）：🔧 模式 → イメージ（模式の続きを切る・扉の3つの型は語りが言う）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.14（`Some were left open and failed to close because they lacked effective self-closing devices`…`others were broken down by firefighters or wedged open with firefighting equipment`）・P1V4¶24.36（`some doors to flats had to be broken down to enable firefighters to gain entry`）'),
    'c423': dict(kind='図解',
               plan='地：X422（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：帯｜副題：廊下の煙の帯＝1:20 ごろ多くの廊下に煙・1:40 一部でかなりの煙・2:00 多くの階で濃い煙｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.15（`Many lobbies had started to fill with smoke by around 01.20 and some were significantly smoke-logged by 01.40`…`By 02.00 a significant number were heavily smoke-logged`）'),
    'c424': dict(kind='図・写真の頁',
               plan='🔧 F:P1V2-12.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：燃え広がる塔〈1:44〉｜動き：静止｜見た目の型：図を11-15に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:44｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図12.1（2019）｜注：本文（第12章の頭＝taken at 01.44）・図12.2（01:48）はアプリの飾り枠の字が焼き込み＝使わない｜新しい画（映像方針）：🔧 図11.8（11.7 とほぼ同じ絵）→ 図12.1（01:44・札 Burning at architectural crown・Lateral spread…＝紙面のまま）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.15（`Until around 01.50 there was less smoke in the stairs; by then 168 people had been able to escape`…`After that time the stairs started to fill with smoke, particularly at lower levels`）'),
    'c425': dict(kind='図・写真の頁',
               plan='F:P1V3-17.4｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：燃え広がる塔〈3:27〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 03:27｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第3巻 図17.4（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.15（`At some levels the smoke was thick and the heat considerable`）'),
    'c426': dict(kind='フリー素材',
               plan='X426｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：煙の立ちこめる暗い階段｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.15（`By 02.20 the smoke in the stairs did pose a risk to life, but the stairs were not absolutely impassable to all even after that time`）'),
    'c427': dict(kind='図解',
               plan='地：X422（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：棒｜副題：逃げた人の数＝1:30 112人・1:50 168人・合わせて227人・その夜塔にいた297人〈数は札にも〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.14（`A total of 112 people had left the tower in the 35 minutes that followed`）・P1ES¶2.11（`By this time 168 of 297 occupants had escaped`）・P1V1¶1.3（`A total of 227 people in all (residents and visitors) escaped from the tower`）'),
    'c428': dict(kind='写真',
               plan='C20｜一覧の種類：写真｜見せ方：全面｜副題：火事から1年の塔〈2018年7月〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2018-07-13｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶32.1（`70 people failed to escape from the building and lost their lives`）・P1V1¶1.3（`a child who was stillborn shortly after his mother had escaped`…`Another resident who had escaped from the building`…`died seven months later`）'),
    'c429': dict(kind='写真',
               plan='C33｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：焼けた塔〈2017年7月19日〉｜動き：静止｜権利：CC BY-SA 2.0｜時期：2017-07-19｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 2.0・無加工）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`the last survivor to leave the tower, is evacuated`）'),
    'c430': dict(kind='図解',
               plan='地：C20（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：1つ目の答えの札＝燃えるプラスチックの芯の板・熱をためる断熱材・火の中で危ないカセットの形・横へ広げた飾りの冠｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（1つ目の問いの答え）'),
    'c431': dict(kind='写真',
               plan='🔧 V15｜一覧の種類：映像｜見せ方：全面｜副題：焼けた塔〈2017年7月公開の映像〉｜動き：映像 195.05〜208.95秒｜見た目の型：240p を11-15に見た｜権利：CC BY 3.0｜時期：2017-07（Vimeo の公開 2017-07-10＝撮影の日は分からない）｜人：なし（人の写る秒は外す＝75〜82.5 歩く人・187.75〜194.75 窓の作業の人）｜出典の行：映像：{作者}／Wikimedia Commons（CC BY 3.0）｜注：T4 焼け残りの境目と木 → T5 木の幹の向こうの塔（202.0 で替わる）・人なし｜新しい画（映像方針）：🔧 副題の時点（Vimeo の公開）・区間＝11-15｜🔴 #15（Commons の映像・CC BY 3.0）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（頭と尻の黒・ビルの広告の幕・歩く人の顔・建物の名の看板・窓の作業の人）に触れない・場面の切れ目をまたがない＝make_list33 の門番｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.16（`there was compelling evidence that the external walls of the building failed to comply with Requirement B4(1) of Schedule 1 to the Building Regulations 2010`）'),
    'c432': dict(kind='写真',
               plan='C21｜一覧の種類：写真｜見せ方：全面｜副題：焼けた塔〈2018年1月〉｜動き：ゆっくり寄る｜見た目の型：原寸を11-15に見た｜権利：CC BY 2.0｜時期：2018-01-05 12:23｜人：なし（窓の掲示は標語 JUSTICE FOR GRENFELL＝11-15 に見た）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：窓の掲示は標語（JUSTICE FOR GRENFELL＝11-15 に見た）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（2つ目の問いへのつなぎ）'),
}

SPEC = {}

# 🆕 ⑤b-2（2026-11-15）：#15 の欄だけ先に書いた（USE と章ファイルを両側から照らす門番 check_footage_slots のため）。ほかのカットは ⑤b-3 以降
#   c431＝焼けた塔（T4 焼け残りの境目と木 → 202.087秒で T5 木の幹の向こう＝決めた場面の替わり・等速・読む 9.86秒〈195.05〜204.91〉）
SPEC.update({
    "c431": ss.vid("c431", t="建物の規則", s="焼けた塔〈2017年7月公開の映像〉"),
})

# 🆕 ⑤b-3（2026-11-15）：報告の図（紙面）11カット＝型は c1.py の c101〜c104 と同じ（額装・静止・地は同じ紙面のぼかし・額＝束の fit）。
#   副題の時刻＝本文の時刻（11-15 に字の層で照らした＝12.1 は 01.44・12.7 は「timed at 02.05」・17.3 は 03.28・17.4 は 03.27・13.1 は 02.00・18.1 は 03.34・19.1 は 04.02）
_F1092, _F1093, _F67, _F117 = P("p2v7_f109_2"), P("p2v7_f109_3"), P("p1v1_f6_7"), P("p1v2_f11_7")
_F131, _F127, _F181, _F173 = P("p1v2_f13_1"), P("p1v2_f12_7"), P("p1v3_f18_1"), P("p1v3_f17_3")
_F191, _F121, _F174 = P("p1v3_f19_1"), P("p1v2_f12_1"), P("p1v3_f17_4")
SPEC.update({
    # c401＝図109.2（実験21・3つのカメラ・焼き込み 09:44＝題の「time 9.44 minutes」）
    "c401": dict(photo=_F1092, panel=True, ptall=True, ground=dict(photo=_F1092, blur=ss.PAGE_BLUR), color=1.0,
                 card_mix=0, t="同じ材料を燃やす", s="外壁の材料を燃やす実験〈9分44秒〉"),   # 章の頭＝扉の地に紙面を混ぜない
    # c403＝図109.3（実験21・焼き込み 10:50＝熱の出方の頂の時刻）
    "c403": dict(photo=_F1093, panel=True, ptall=True, ground=dict(photo=_F1093, blur=ss.PAGE_BLUR), color=1.0,
                 t="熱を出した板", s="板がすっかり燃えた実験"),
    # c405＝図6.7（窓のまわりの焼けた断熱材と柔らかくなった樹脂の枠・断熱材の板の写真＝会社の名は報告の結論の範囲）
    "c405": dict(photo=_F67, panel=True, ptall=True, ground=dict(photo=_F67, blur=ss.PAGE_BLUR), color=1.0,
                 t="前の報告でも", s="窓のまわりの断熱材〈報告の図〉"),   # 🔧「2019年の報告」＝字幕の頭と同文（echo）・「第1段階の報告」＝出典の行の写し（dup）
    # c411＝図11.7（2本の柱にそって燃える塔）
    "c411": dict(photo=_F117, panel=True, ptall=True, ground=dict(photo=_F117, blur=ss.PAGE_BLUR), color=1.0,
                 t="張り出した柱", s="2本の柱にそって燃える塔〈1:40ごろ〉"),
    # c413＝図13.1（札 Burning at architectural crown）
    "c413": dict(photo=_F131, panel=True, ptall=True, ground=dict(photo=_F131, blur=ss.PAGE_BLUR), color=1.0,
                 t="斜めに広がる火", s="冠で燃える炎〈2:00〉"),
    # c414＝図12.7（はしご車・札 Level 10・Level 4・D5）
    "c414": dict(photo=_F127, panel=True, ptall=True, ground=dict(photo=_F127, blur=ss.PAGE_BLUR), color=1.0,
                 t="32メートルのはしご", s="東の面のはしご車〈2:05〉"),
    # c415＝図18.1（札 Burning below architectural crown）
    "c415": dict(photo=_F181, panel=True, ptall=True, ground=dict(photo=_F181, blur=ss.PAGE_BLUR), color=1.0,
                 t="南と西の面", s="燃え広がる塔〈3:34〉"),
    # c417＝図17.3（札 Dripping, burning material）
    "c417": dict(photo=_F173, panel=True, ptall=True, ground=dict(photo=_F173, blur=ss.PAGE_BLUR), color=1.0,
                 t="落ちるかけら", s="下の階に出た新しい火〈3:28〉"),
    # c418＝図19.1（夜明けの空・札 Possible gap between flames from South and Flames from West・通りの車と人はぼけて読めない＝原寸で見た）
    "c418": dict(photo=_F191, panel=True, ptall=True, ground=dict(photo=_F191, blur=ss.PAGE_BLUR), color=1.0,
                 t="2つの面の炎", s="合わさりはじめる炎〈4:02〉"),
    # c424＝図12.1（札 Burning at architectural crown ほか3つ）
    "c424": dict(photo=_F121, panel=True, ptall=True, ground=dict(photo=_F121, blur=ss.PAGE_BLUR), color=1.0,
                 t="168人の避難", s="燃え広がる塔〈1:44〉"),
    # c425＝図17.4（札 Burning material falls on window detail）
    "c425": dict(photo=_F174, panel=True, ptall=True, ground=dict(photo=_F174, blur=ss.PAGE_BLUR), color=1.0,
                 t="階段の煙", s="燃え広がる塔〈3:27〉"),
})
