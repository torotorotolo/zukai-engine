# -*- coding: utf-8 -*-
"""第6章　試験をごまかした会社 c701–c723（23カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c7.py`）。
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
    'c701': dict(kind='文字の頁',
               plan='P:c701｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「試験のやり方を操り、試験の結果を偽って伝え、市場を欺く」｜動き：静止｜見た目の型：P2V1 ¶2.19 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.19（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.19（`They engaged in deliberate and sustained strategies to manipulate the testing processes, misrepresent test data and mislead the market`）'),
    'c702': dict(kind='図解',
               plan='地：X624（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：報告が名を挙げた3社の札＝外装の板 アルコニック・断熱材 セロテックス・断熱材 キングスパン｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.21（`Arconic Architectural Products manufactured and sold the Reynobond 55 PE rainscreen panels`）・P2V1¶2.28（`Celotex manufactured RS5000, a combustible polyisocyanurate foam insulation`）・P2V1¶2.41（`one of the insulation products used on Grenfell Tower, Kingspan K15`）'),
    'c703': dict(kind='図解',
               plan='🔧 地：X624（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：比べ｜副題：同じ板の2つの形＝リベット留めの平らな板とカセット・カセットは火にとても危ない反応〈2005年の初めの試験〉｜新しい画（映像方針）：🔧 種類 模式 → 比べ（リベット留めとカセットの2つの形＝c407 と同じ型）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.22（`from early 2005 Arconic had been in possession of test data showing that in its cassette form the product reacted to fire in a very dangerous way`）'),
    'c704': dict(kind='フリー素材',
               plan='X704｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：積み重ねたアルミの板｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.22（`Arconic persisted in telling the market that the panels had been classed B-s2, d0 without drawing any distinction between the cassette and riveted forms`）・P2V1¶2.21（`From 2005 until after the Grenfell Tower fire Arconic deliberately concealed from the market the true extent of the danger of using Reynobond 55 PE in cassette form`）'),
    'c705': dict(kind='図解',
               plan='地：X704（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：規制が弱いと見た国〈イギリスを含む〉へ、カセットの形のまま売る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.23（`it was determined to exploit what it saw as weak regulatory regimes in certain countries (including the UK) to sell Reynobond 55 PE in cassette form`）'),
    'c706': dict(kind='フリー素材',
               plan='X706｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜の都市の高層ビル群｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.24（`Despite the knowledge gained from cladding fires in Dubai in 2012 and 2013, Arconic did not consider withdrawing Reynobond 55 PE in favour of the fire-resistant version then available`）'),
    'c707': dict(kind='図解',
               plan='地：X704（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：等級の札＝2013年の試験のあと、自ら等級を燃えやすい方のEにすると決める・イギリスの客と認証の機関に、わざと伝えない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.25（`Following further testing in 2013, Arconic decided that Reynobond 55 PE would be certified as Class E only, whether used in riveted or cassette form`…`it did not pass that information to its customers in the UK or to the BBA`…`That was not an oversight`）'),
    'c708': dict(kind='フリー素材',
               plan='🔧 X708｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：製品の証明書の書類｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜注：字は読めない｜新しい画（映像方針）：🔧 模式 → イメージ（模式の続きを切る）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.27（`Arconic persuaded the BBA to issue a certificate that drew no distinction between the different forms of fixing`…`It concealed important information from the BBA, in particular the test data relating to the product in cassette form`）'),
    'c709': dict(kind='フリー素材',
               plan='X709｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：断熱材の板の束｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.28（`In an attempt to break into the market for insulation suitable for use on high-rise buildings`…`Celotex embarked on a dishonest scheme to mislead its customers and the wider market`）'),
    'c710': dict(kind='写真',
               plan='F:P2V1-5.8｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：燃焼試験の装置〈報告の図〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 図5.8（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.29（`in May 2014 Celotex tested in accordance with BS 8414 a system incorporating RS5000 that contained two sets of fire-resistant magnesium oxide boards placed in critical positions to ensure that it passed`）'),
    'c711': dict(kind='文字の頁',
               plan='P:c711｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「その板について何も書かない、試験の報告」｜動き：静止｜見た目の型：P2V1 ¶2.29 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.29（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.29（`It then obtained from BRE a test report that omitted any reference to the magnesium oxide boards`）・P2V1¶2.19（`the Building Research Establishment (BRE) was complicit in that strategy`）'),
    'c712': dict(kind='図解',
               plan='地：X709（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：試験の機関の札＝1921年 国の機関として始まる・1991年から 外壁の防火の試験の仕事の多くが、ずさんで科学として甘い｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.11（`had been established in 1921 as a government body`）・P2V1¶2.15（`However, from 1991 much of the work it carried out in relation to testing the fire safety of external walls was marred by unprofessional conduct, inadequate practices, a lack of effective oversight, poor reporting and a lack of scientific rigour`）'),
    'c713': dict(kind='フリー素材',
               plan='X713｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：建材の売り込みの冊子とカタログ｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.30（`"the first PIR board to successfully test to BS 8414"`…`"acceptable for use in buildings above 18 metres in height"`）'),
    'c714': dict(kind='図解',
               plan='地：X713（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：勧めの札＝外装の下請けに「この塔にふさわしく安全」と勧める・そうでないと知りながら｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.31（`Celotex presented RS5000 to Harley as suitable and safe for use on Grenfell Tower, although it knew that was not the case`）'),
    'c715': dict(kind='図解',
               plan='地：X713（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：キングスパンの札＝2005年から調査が始まったあとまで、18メートルをこえる建物の断熱材に偽りの市場｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.32（`From 2005 until after this Inquiry had begun, Kingspan knowingly created a false market in insulation for use on buildings over 18 metres in height`）'),
    'c716': dict(kind='図解',
               plan='🔧 地：X713（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：年表｜副題：頼った試験の札＝2005年の1回の試験・2006年に中身を変えたことは言わない・2007年と2008年の試験はひどい結果｜新しい画（映像方針）：🔧 種類 模式 → 年表（2005・2006・2007・2008 の並び）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.33（`relied on the results of a single BS 8414-1 test performed in 2005`…`without disclosing that it had changed the composition of the product in 2006`…`Tests performed in 2007 and 2008 on systems incorporating the then current form of K15 were disastrous`）'),
    'c717': dict(kind='フリー素材',
               plan='X717｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：工場に積まれた断熱材の板｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.37（`Kingspan did not use the product currently on the market but used modified or trial versions`…`continued to do so until October 2020`）'),
    'c718': dict(kind='図解',
               plan='地：X717（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：認証の機関の札＝製品の証明書を出す2つの機関は、証明書の中身を確かめない・それを見守る機関は、監督が不十分｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.20（`failed to ensure that the statements in their product certificates were accurate and based on test evidence`…`standards of monitoring and supervision`）'),
    'c719': dict(kind='文字の頁',
               plan='P:c719｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「客に合わせ、証明書を信じる人を損なう」｜動き：静止｜見た目の型：P2V2 ¶29.48 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第2巻 ¶29.48（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V2¶29.48（`it was willing to accommodate the customer at the expense of those who relied on the certificates`）'),
    'c720': dict(kind='写真',
               plan='F:P2V1-5.2｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：表面の炎の広がりを見る試験〈報告の図〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 図5.2（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.121（`The use of Class 0 as a standard of fire performance for products to be used on the external wall of tall buildings was wholly inappropriate`）'),
    'c721': dict(kind='図解',
               plan='地：X717（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：小さな試料の試験と、建物の外で広がる火＝試験では分からない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.121（`Neither of the main British Standard tests relevant to that classification reflected the development of a fire on the outside of a building or provided the information needed to assess how an external wall incorporating the product would perform in a fire`）'),
    'c722': dict(kind='図解',
               plan='🔧 地：X717（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：流れ｜副題：仕組みの札＝作る・売る・試す・認める・見守る＝ばらばら・まとめられるのは国だけ｜新しい画（映像方針）：🔧 種類 模式 → 流れ（作る→売る→試す→認める→見守る）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V2¶29.58（`that system lacked the degree of integration required`）・P2V2¶29.59（`That is a task that only the government can undertake.`）'),
    'c723': dict(kind='写真',
               plan='🔧 C45｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：隣の学校と塔〈2018年5月〉｜動き：静止｜権利：CC BY-SA 4.0｜時期：2018-05-09 18:58｜人：学校の名の看板（場所の名＝可）・人なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 4.0・無加工）｜注：学校の名の看板（場所の名）｜新しい画（映像方針）：🔧 [59]（2024年8月）→ [45]（[59] は ca15 の取り壊しの話へ）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.5（`by 2016 the department was well aware of those risks, but failed to act on what it knew`）'),
}

SPEC = {}
